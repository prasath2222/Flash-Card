import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";
import { initializeApp, getApps } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc } from "firebase/firestore";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize Firestore connection for cross-container & worldwide persistence
let firestoreDb: ReturnType<typeof getFirestore> | null = null;
try {
  const cfgPath = path.join(__dirname, "firebase-applet-config.json");
  if (fs.existsSync(cfgPath)) {
    const firebaseConfig = JSON.parse(fs.readFileSync(cfgPath, "utf8"));
    const fbApp = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
    firestoreDb = getFirestore(fbApp, firebaseConfig.firestoreDatabaseId);
  }
} catch (err) {
  console.warn("Firestore initialization notice in server.ts:", err);
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json({ limit: "25mb" }));

  // Load pre-verified image mappings
  let accurateImages: Record<string, string> = {};
  let wikiThumbs: Record<string, string> = {};
  try {
    const accPath = path.join(__dirname, "scripts", "accurate_images.json");
    if (fs.existsSync(accPath)) {
      accurateImages = JSON.parse(fs.readFileSync(accPath, "utf8"));
    }
    const wikiPath = path.join(__dirname, "scripts", "wiki_thumbs.json");
    if (fs.existsSync(wikiPath)) {
      wikiThumbs = JSON.parse(fs.readFileSync(wikiPath, "utf8"));
    }
  } catch (e) {
    console.warn("Could not load static image maps:", e);
  }

  const runtimeImageCache: Record<string, string> = {};

  async function resolveRealWorldPhoto(word: string, num?: string): Promise<string | null> {
    if (num && accurateImages[num]) return accurateImages[num];
    if (num && wikiThumbs[num]) return wikiThumbs[num];

    const cleanWord = String(word || "")
      .replace(/[^\p{L}\p{N}\s-]/gu, "")
      .trim()
      .toLowerCase();
    if (!cleanWord) return null;

    if (runtimeImageCache[cleanWord]) return runtimeImageCache[cleanWord];

    const headers = {
      "User-Agent": "Mozilla/5.0 (SequentialMultilingualFlashcards/2.0; Educational App)"
    };

    try {
      const capWord = cleanWord.charAt(0).toUpperCase() + cleanWord.slice(1);
      const summaryRes = await fetch(
        `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(capWord)}`,
        { headers }
      );
      if (summaryRes.ok) {
        const data: any = await summaryRes.json();
        const imgUrl = data?.thumbnail?.source || data?.originalimage?.source;
        if (imgUrl && !imgUrl.endsWith(".svg") && !imgUrl.includes("Commons-logo")) {
          runtimeImageCache[cleanWord] = imgUrl;
          return imgUrl;
        }
      }
    } catch (e) {}

    try {
      const wikiSearchUrl = `https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(
        cleanWord
      )}&gsrlimit=3&prop=pageimages&pithumbsize=960&format=json&origin=*`;
      const searchRes = await fetch(wikiSearchUrl, { headers });
      if (searchRes.ok) {
        const sData: any = await searchRes.json();
        const pages = sData?.query?.pages;
        if (pages) {
          for (const p of Object.values(pages) as any[]) {
            const thumb = p?.thumbnail?.source;
            if (thumb && !thumb.endsWith(".svg") && !thumb.includes("Commons-logo")) {
              runtimeImageCache[cleanWord] = thumb;
              return thumb;
            }
          }
        }
      }
    } catch (e) {}

    try {
      const commonsUrl = `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(
        `filetype:bitmap ${cleanWord}`
      )}&gsrnamespace=6&gsrlimit=3&prop=imageinfo&iiprop=url&iiurlwidth=960&format=json&origin=*`;
      const cRes = await fetch(commonsUrl, { headers });
      if (cRes.ok) {
        const cData: any = await cRes.json();
        const pages = cData?.query?.pages;
        if (pages) {
          for (const p of Object.values(pages) as any[]) {
            const thumb = p?.imageinfo?.[0]?.thumburl || p?.imageinfo?.[0]?.url;
            if (thumb && !thumb.endsWith(".svg")) {
              runtimeImageCache[cleanWord] = thumb;
              return thumb;
            }
          }
        }
      }
    } catch (e) {}

    return null;
  }

  app.get("/api/image", async (req, res) => {
    try {
      const num = String(req.query.num || "").trim();
      const q = String(req.query.q || "").trim();

      const resolvedUrl = await resolveRealWorldPhoto(q, num);
      if (resolvedUrl) {
        res.setHeader("Cache-Control", "public, max-age=86400");
        return res.redirect(302, resolvedUrl);
      }

      const displayLabel = (q || `#${num || "?"}`).toUpperCase().replace(/[<>&"']/g, "");
      const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
        <defs>
          <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0f172a"/>
            <stop offset="50%" stop-color="#1e293b"/>
            <stop offset="100%" stop-color="#090d16"/>
          </linearGradient>
        </defs>
        <rect width="800" height="600" fill="url(#bg)"/>
        <circle cx="400" cy="240" r="90" fill="rgba(56, 189, 248, 0.12)" stroke="rgba(56, 189, 248, 0.35)" stroke-width="3"/>
        <text x="400" y="265" font-family="system-ui, sans-serif" font-size="72" font-weight="800" fill="#38bdf8" text-anchor="middle">${displayLabel.slice(0, 2)}</text>
        <text x="400" y="420" font-family="system-ui, sans-serif" font-size="44" font-weight="800" fill="#f8fafc" text-anchor="middle" letter-spacing="2">${displayLabel}</text>
      </svg>`;
      res.setHeader("Content-Type", "image/svg+xml");
      res.setHeader("Cache-Control", "public, max-age=3600");
      return res.status(200).send(svg);
    } catch (err) {
      res.status(500).end();
    }
  });

  app.get("/api/find-image", async (req, res) => {
    try {
      const q = String(req.query.q || "").trim();
      const num = String(req.query.num || "").trim();
      const url = await resolveRealWorldPhoto(q, num);
      res.json({ ok: true, word: q, imageUrl: url || `/api/image?q=${encodeURIComponent(q)}` });
    } catch (e) {
      res.json({ ok: false, imageUrl: `/api/image?q=${encodeURIComponent(String(req.query.q || ""))}` });
    }
  });

  // =========================================================================
  // PRODUCTION PER-ACCOUNT CLOUD SYNC API (ISOLATED PER GOOGLE ACCOUNT)
  // Backed by Google Cloud Firestore + Local Disk Cache
  // =========================================================================
  const dataDir = path.join(__dirname, "data");
  const profilesFilePath = path.join(dataDir, "user_profiles.json");

  function sanitizeEmailKey(rawEmail: unknown): string {
    const clean = String(rawEmail || "")
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9@._+-]/g, "")
      .slice(0, 120);
    if (!clean || !clean.includes("@")) {
      return "";
    }
    return clean;
  }

  function emailToFirestoreDocId(email: string): string {
    return `acct_${email.replace(/[^a-z0-9]/g, "_")}`.slice(0, 120);
  }

  function normalizeProfilePayload(rawEntry: any): any {
    if (!rawEntry || typeof rawEntry !== "object") return null;
    const inner = rawEntry.payload && typeof rawEntry.payload === "object" ? rawEntry.payload : rawEntry;
    const learnedCardNums = Array.isArray(inner.learnedCardNums)
      ? inner.learnedCardNums
      : Array.isArray(inner.learnedCards)
      ? inner.learnedCards
      : [];
    const deletedCardNums = Array.isArray(inner.deletedCardNums)
      ? inner.deletedCardNums
      : Array.isArray(inner.deletedCards)
      ? inner.deletedCards
      : [];
    const activeDeckId = inner.activeDeckId || "deck-800-1000";
    const lastActiveCardNum = Number(inner.lastActiveCardNum ?? inner.lastCard ?? 800);
    const streakCount = Number(inner.streakCount ?? inner.streak ?? 1);
    const customShortcuts =
      inner.customShortcuts && typeof inner.customShortcuts === "object" ? inner.customShortcuts : {};
    const customDecks =
      inner.customDecks && typeof inner.customDecks === "object" ? inner.customDecks : {};
    const customSections = Array.isArray(inner.customSections) ? inner.customSections : [];
    const audioPrefs =
      inner.audioPrefs && typeof inner.audioPrefs === "object" ? inner.audioPrefs : {};
    const updatedAt = rawEntry.updatedAt || inner.updatedAt || new Date().toISOString();

    return {
      learnedCardNums,
      learnedCards: learnedCardNums,
      deletedCardNums,
      deletedCards: deletedCardNums,
      activeDeckId,
      lastActiveCardNum,
      lastCard: lastActiveCardNum,
      streakCount,
      streak: streakCount,
      customShortcuts,
      customDecks,
      customSections,
      audioPrefs,
      updatedAt
    };
  }

  function readUserProfiles(): Record<string, any> {
    try {
      if (fs.existsSync(profilesFilePath)) {
        const raw = JSON.parse(fs.readFileSync(profilesFilePath, "utf8"));
        if (raw && typeof raw === "object") {
          return raw;
        }
      }
    } catch (e) {
      console.warn("Could not read user_profiles.json:", e);
    }
    return {};
  }

  function writeUserProfiles(profiles: Record<string, any>) {
    try {
      if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
      }
      fs.writeFileSync(profilesFilePath, JSON.stringify(profiles, null, 2), "utf8");
    } catch (e) {
      console.warn("Could not write user_profiles.json:", e);
    }
  }

  async function saveProfileData(
    rawEmail: unknown,
    incomingBody: any
  ): Promise<{ email: string; exists: boolean; updatedAt: string; payload: any }> {
    const email = sanitizeEmailKey(rawEmail);
    if (!email) {
      return { email: "", exists: false, updatedAt: "", payload: null };
    }

    const profiles = readUserProfiles();
    const existingNorm = normalizeProfilePayload(profiles[email]) || normalizeProfilePayload({});

    const incoming =
      incomingBody?.payload && typeof incomingBody.payload === "object"
        ? incomingBody.payload
        : incomingBody || {};
    const replaceArrays = incomingBody?.replaceArrays !== false;

    const inLearned = Array.isArray(incoming.learnedCardNums)
      ? incoming.learnedCardNums
      : Array.isArray(incoming.learnedCards)
      ? incoming.learnedCards
      : null;

    const inDeleted = Array.isArray(incoming.deletedCardNums)
      ? incoming.deletedCardNums
      : Array.isArray(incoming.deletedCards)
      ? incoming.deletedCards
      : null;

    const learnedCardNums =
      inLearned !== null
        ? replaceArrays
          ? inLearned
          : Array.from(new Set([...(existingNorm.learnedCardNums || []), ...inLearned]))
        : existingNorm.learnedCardNums || [];

    const deletedCardNums =
      inDeleted !== null
        ? replaceArrays
          ? inDeleted
          : Array.from(new Set([...(existingNorm.deletedCardNums || []), ...inDeleted]))
        : existingNorm.deletedCardNums || [];

    const customShortcuts =
      incoming.customShortcuts && typeof incoming.customShortcuts === "object"
        ? replaceArrays
          ? incoming.customShortcuts
          : { ...(existingNorm.customShortcuts || {}), ...incoming.customShortcuts }
        : existingNorm.customShortcuts || {};

    const customDecks =
      incoming.customDecks && typeof incoming.customDecks === "object"
        ? replaceArrays
          ? incoming.customDecks
          : { ...(existingNorm.customDecks || {}), ...incoming.customDecks }
        : existingNorm.customDecks || {};

    const customSections = Array.isArray(incoming.customSections)
      ? incoming.customSections
      : existingNorm.customSections || [];

    const audioPrefs =
      incoming.audioPrefs && typeof incoming.audioPrefs === "object"
        ? { ...(existingNorm.audioPrefs || {}), ...incoming.audioPrefs }
        : existingNorm.audioPrefs || {};

    const activeDeckId = incoming.activeDeckId || existingNorm.activeDeckId || "deck-800-1000";
    const lastActiveCardNum = Number(
      incoming.lastActiveCardNum ?? incoming.lastCard ?? existingNorm.lastActiveCardNum ?? 800
    );
    const streakCount = Number(
      incoming.streakCount ?? incoming.streak ?? existingNorm.streakCount ?? 1
    );
    const updatedAt = new Date().toISOString();

    const savedPayload = {
      email,
      learnedCardNums,
      learnedCards: learnedCardNums,
      deletedCardNums,
      deletedCards: deletedCardNums,
      activeDeckId,
      lastActiveCardNum,
      lastCard: lastActiveCardNum,
      streakCount,
      streak: streakCount,
      customShortcuts,
      customDecks,
      customSections,
      audioPrefs,
      updatedAt
    };

    profiles[email] = {
      updatedAt,
      payload: savedPayload
    };
    writeUserProfiles(profiles);

    // Also persist to Google Cloud Firestore under isolated account document
    if (firestoreDb) {
      try {
        const docId = emailToFirestoreDocId(email);
        await setDoc(doc(firestoreDb, "study_state", docId), {
          email,
          updatedAt,
          payload: savedPayload
        });
      } catch (err) {
        console.warn("Firestore save notice:", err);
      }
    }

    return { email, exists: true, updatedAt, payload: savedPayload };
  }

  async function loadProfileData(
    rawEmail: unknown
  ): Promise<{ email: string; exists: boolean; updatedAt: string; payload: any }> {
    const email = sanitizeEmailKey(rawEmail);
    if (!email) {
      return { email: "", exists: false, updatedAt: "", payload: null };
    }

    const profiles = readUserProfiles();
    let localNorm = profiles[email] ? normalizeProfilePayload(profiles[email]) : null;
    let firestoreNorm: any = null;

    if (firestoreDb) {
      try {
        const docId = emailToFirestoreDocId(email);
        const snap = await getDoc(doc(firestoreDb, "study_state", docId));
        if (snap.exists()) {
          firestoreNorm = normalizeProfilePayload(snap.data());
        }
      } catch (err) {
        console.warn("Firestore load notice:", err);
      }
    }

    let chosen: any = null;
    if (localNorm && firestoreNorm) {
      const localTime = Date.parse(localNorm.updatedAt || "") || 0;
      const remoteTime = Date.parse(firestoreNorm.updatedAt || "") || 0;
      chosen = remoteTime >= localTime ? firestoreNorm : localNorm;
    } else {
      chosen = firestoreNorm || localNorm;
    }

    if (!chosen) {
      return {
        email,
        exists: false,
        updatedAt: "",
        payload: null
      };
    }

    // Keep local cache in sync with latest Firestore state
    if (!localNorm || chosen === firestoreNorm) {
      profiles[email] = {
        updatedAt: chosen.updatedAt,
        payload: chosen
      };
      writeUserProfiles(profiles);
    }

    return {
      email,
      exists: true,
      updatedAt: chosen.updatedAt || new Date().toISOString(),
      payload: chosen
    };
  }

  // Endpoints used by index.html (/api/user/save, /api/user/load, /api/user/poll)
  app.post("/api/user/save", async (req, res) => {
    const result = await saveProfileData(req.body?.email, req.body);
    res.json({ ok: true, success: true, ...result });
  });

  app.get("/api/user/load", async (req, res) => {
    const result = await loadProfileData(req.query.email);
    res.json({ ok: true, success: true, ...result });
  });

  app.get("/api/user/poll", async (req, res) => {
    const since = String(req.query.since || "").trim();
    const result = await loadProfileData(req.query.email);
    if (!result.exists || !result.payload) {
      return res.json({
        ok: true,
        success: true,
        hasUpdates: false,
        updatedAt: "",
        payload: null
      });
    }
    const sinceMs = Date.parse(since) || 0;
    const updatedMs = Date.parse(result.updatedAt) || 0;
    const hasUpdates = Boolean(!since || updatedMs > sinceMs);
    res.json({
      ok: true,
      success: true,
      hasUpdates,
      updatedAt: result.updatedAt,
      payload: hasUpdates ? result.payload : null
    });
  });

  // Endpoints used by firebase-sync.ts & legacy callers
  app.get("/api/account-sync", async (req, res) => {
    const result = await loadProfileData(req.query.email);
    res.json({ ok: true, success: true, ...result });
  });

  app.post("/api/account-sync", async (req, res) => {
    const result = await saveProfileData(req.body?.email, req.body);
    res.json({ ok: true, success: true, ...result });
  });

  app.get("/api/sync-pull", async (req, res) => {
    const result = await loadProfileData(req.query.syncId || req.query.email);
    res.json({ ok: true, syncId: result.email, exists: result.exists, payload: result.payload });
  });

  app.post("/api/sync-push", async (req, res) => {
    const result = await saveProfileData(req.body?.syncId || req.body?.email, req.body);
    res.json({ ok: true, syncId: result.email, exists: result.exists, payload: result.payload });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa"
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*all", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();

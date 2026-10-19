import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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
  // PRODUCTION CROSS-DEVICE SYNC & UNIVERSAL PERSISTENCE API
  // Automatically reflects all saves across all devices & browsers
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
      return "default_global_profile";
    }
    return clean;
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

  // Ensure default_global_profile is initialized and synced with existing user profiles on startup
  function ensureUnifiedGlobalProfile() {
    const profiles = readUserProfiles();
    let latestTime = 0;
    let bestPayload: any = null;

    const mergedLearned = new Set<any>();
    const mergedDeleted = new Set<any>();
    const mergedShortcuts: Record<string, any> = {};
    const mergedDecks: Record<string, any> = {};
    let mergedSections: any[] = [];
    let mergedAudioPrefs: Record<string, any> = {};
    let activeDeckId = "deck-800-1000";
    let lastActiveCardNum = 800;
    let streakCount = 1;

    for (const [key, val] of Object.entries(profiles)) {
      const norm = normalizeProfilePayload(val);
      if (!norm) continue;
      (norm.learnedCardNums || []).forEach((n: any) => mergedLearned.add(n));
      (norm.deletedCardNums || []).forEach((n: any) => mergedDeleted.add(n));
      Object.assign(mergedShortcuts, norm.customShortcuts || {});
      Object.assign(mergedDecks, norm.customDecks || {});
      if (Array.isArray(norm.customSections) && norm.customSections.length > mergedSections.length) {
        mergedSections = norm.customSections;
      }
      Object.assign(mergedAudioPrefs, norm.audioPrefs || {});
      const t = Date.parse(norm.updatedAt || "") || 0;
      if (t >= latestTime) {
        latestTime = t;
        bestPayload = norm;
      }
    }

    if (bestPayload) {
      activeDeckId = bestPayload.activeDeckId || activeDeckId;
      lastActiveCardNum = bestPayload.lastActiveCardNum || lastActiveCardNum;
      streakCount = Math.max(streakCount, bestPayload.streakCount || 1);
    }

    const updatedAt = latestTime > 0 ? new Date(latestTime).toISOString() : new Date().toISOString();
    const unifiedPayload = {
      learnedCardNums: Array.from(mergedLearned),
      learnedCards: Array.from(mergedLearned),
      deletedCardNums: Array.from(mergedDeleted),
      deletedCards: Array.from(mergedDeleted),
      activeDeckId,
      lastActiveCardNum,
      lastCard: lastActiveCardNum,
      streakCount,
      streak: streakCount,
      customShortcuts: mergedShortcuts,
      customDecks: mergedDecks,
      customSections: mergedSections,
      audioPrefs: mergedAudioPrefs,
      updatedAt
    };

    profiles["default_global_profile"] = {
      updatedAt,
      payload: unifiedPayload
    };
    writeUserProfiles(profiles);
  }

  ensureUnifiedGlobalProfile();

  function saveProfileData(rawEmail: unknown, incomingBody: any): { email: string; updatedAt: string; payload: any } {
    const email = sanitizeEmailKey(rawEmail);
    const profiles = readUserProfiles();
    const existingNorm =
      normalizeProfilePayload(profiles[email]) ||
      normalizeProfilePayload(profiles["default_global_profile"]) ||
      normalizeProfilePayload({});

    const incoming = incomingBody?.payload && typeof incomingBody.payload === "object" ? incomingBody.payload : incomingBody || {};
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
        ? { ...(existingNorm.customDecks || {}), ...incoming.customDecks }
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

    // Always mirror to default_global_profile so opening the app on any device reflects changes immediately
    profiles["default_global_profile"] = {
      updatedAt,
      payload: savedPayload
    };

    writeUserProfiles(profiles);
    return { email, updatedAt, payload: savedPayload };
  }

  function loadProfileData(rawEmail: unknown): { email: string; updatedAt: string; payload: any } {
    const email = sanitizeEmailKey(rawEmail);
    const profiles = readUserProfiles();
    const userNorm = normalizeProfilePayload(profiles[email]);
    const globalNorm = normalizeProfilePayload(profiles["default_global_profile"]);

    let chosen = userNorm || globalNorm;
    if (userNorm && globalNorm) {
      const userTime = Date.parse(userNorm.updatedAt || "") || 0;
      const globalTime = Date.parse(globalNorm.updatedAt || "") || 0;
      chosen = globalTime > userTime ? globalNorm : userNorm;
    }

    if (!chosen) {
      const now = new Date().toISOString();
      chosen = normalizeProfilePayload({ updatedAt: now });
    }

    return {
      email,
      updatedAt: chosen.updatedAt || new Date().toISOString(),
      payload: chosen
    };
  }

  // Endpoints used by index.html (/api/user/save, /api/user/load, /api/user/poll)
  app.post("/api/user/save", (req, res) => {
    const result = saveProfileData(req.body?.email, req.body);
    res.json({ ok: true, success: true, ...result });
  });

  app.get("/api/user/load", (req, res) => {
    const result = loadProfileData(req.query.email);
    res.json({ ok: true, success: true, ...result });
  });

  app.get("/api/user/poll", (req, res) => {
    const since = String(req.query.since || "").trim();
    const result = loadProfileData(req.query.email);
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

  // Endpoints used by firebase-sync.ts & legacy callers (/api/account-sync, /api/sync-pull, /api/sync-push)
  app.get("/api/account-sync", (req, res) => {
    const result = loadProfileData(req.query.email);
    res.json({ ok: true, success: true, ...result });
  });

  app.post("/api/account-sync", (req, res) => {
    const result = saveProfileData(req.body?.email, req.body);
    res.json({ ok: true, success: true, ...result });
  });

  app.get("/api/sync-pull", (req, res) => {
    const result = loadProfileData(req.query.syncId || req.query.email);
    res.json({ ok: true, syncId: result.email, payload: result.payload });
  });

  app.post("/api/sync-push", (req, res) => {
    const result = saveProfileData(req.body?.syncId || req.body?.email, req.body);
    res.json({ ok: true, syncId: result.email, payload: result.payload });
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

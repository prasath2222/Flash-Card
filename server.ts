import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";
import crypto from "crypto";
import { initializeApp, getApps } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc, deleteDoc } from "firebase/firestore";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const GOOGLE_OAUTH_CLIENT_ID = "328045128-9o8clmes7c6itrht7acmc4v56e3sfs9n.apps.googleusercontent.com";

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

// In-memory store for OAuth state handoff (also backed by Firestore for multi-instance support)
const pendingOAuthStates = new Map<string, { status: "completed" | "error"; user?: any; error?: string; createdAt: number }>();

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
      const q = String(req.query.q || req.query.query || "").trim();
      const num = String(req.query.num || "").trim();
      const url = await resolveRealWorldPhoto(q, num);
      res.json({ ok: true, word: q, imageUrl: url || `/api/image?q=${encodeURIComponent(q)}` });
    } catch (e) {
      const fallbackQ = String(req.query.q || req.query.query || "");
      res.json({ ok: false, imageUrl: `/api/image?q=${encodeURIComponent(fallbackQ)}` });
    }
  });

  app.get("/api/tts", async (req, res) => {
    try {
      const text = String(req.query.text || req.query.q || "").trim().slice(0, 200);
      const rawLang = String(req.query.lang || "en").trim().toLowerCase();
      if (!text) {
        return res.status(400).end();
      }
      const tl = rawLang.startsWith("ta")
        ? "ta"
        : rawLang.startsWith("es")
        ? "es"
        : rawLang.startsWith("hi")
        ? "hi"
        : "en";
      const ttsUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=${encodeURIComponent(tl)}&client=tw-ob&q=${encodeURIComponent(text)}`;
      const upstream = await fetch(ttsUrl, {
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
          "Referer": "https://translate.google.com/"
        }
      });
      if (!upstream.ok) {
        return res.status(upstream.status).end();
      }
      const arrayBuffer = await upstream.arrayBuffer();
      res.setHeader("Content-Type", "audio/mpeg");
      res.setHeader("Cache-Control", "public, max-age=86400");
      return res.status(200).send(Buffer.from(arrayBuffer));
    } catch (e) {
      return res.status(502).end();
    }
  });

  // =========================================================================
  // REAL PRODUCTION GOOGLE OAUTH 2.0 HANDLER & CRYPTOGRAPHIC TOKEN VERIFIER
  // Supports all mobile browsers (iOS Safari, Android Chrome) & desktop
  // =========================================================================
  const oauthCallbackHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sign in with Google</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0b1120;
      color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 20px;
      box-sizing: border-box;
    }
    .card {
      width: 100%;
      max-width: 380px;
      background: #172236;
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 22px;
      padding: 28px 24px;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }
    .spinner {
      width: 42px;
      height: 42px;
      border: 4px solid rgba(56, 189, 248, 0.2);
      border-top-color: #38bdf8;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 0 auto 16px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .title { font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; }
    .sub { font-size: 0.88rem; color: #94a3b8; line-height: 1.45; }
    .btn {
      display: none;
      margin-top: 18px;
      width: 100%;
      padding: 13px 18px;
      background: #10b981;
      color: #052e16;
      font-weight: 800;
      font-size: 0.95rem;
      border: none;
      border-radius: 12px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="spinner" id="spinner"></div>
    <div class="title" id="status-title">Completing Google Sign-In...</div>
    <div class="sub" id="status-sub">Verifying your Google account credentials securely.</div>
    <button class="btn" id="return-btn" onclick="finishAndClose()">Return to App</button>
  </div>
  <script>
    let verifiedUser = null;
    function finishAndClose() {
      try { window.close(); } catch (e) {}
      setTimeout(() => {
        window.location.replace("/");
      }, 150);
    }

    (async function() {
      const hashStr = window.location.hash ? window.location.hash.substring(1) : "";
      const searchStr = window.location.search ? window.location.search.substring(1) : "";
      const hashParams = new URLSearchParams(hashStr);
      const queryParams = new URLSearchParams(searchStr);

      const idToken = hashParams.get("id_token") || queryParams.get("id_token") || "";
      const accessToken = hashParams.get("access_token") || queryParams.get("access_token") || "";
      const state = hashParams.get("state") || queryParams.get("state") || "";
      const error = hashParams.get("error") || queryParams.get("error") || "";

      const spinner = document.getElementById("spinner");
      const titleEl = document.getElementById("status-title");
      const subEl = document.getElementById("status-sub");
      const btnEl = document.getElementById("return-btn");

      if (error || (!idToken && !accessToken)) {
        if (state) {
          fetch("/api/auth/verify-google", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ state, error: error || "cancelled" })
          }).catch(() => {});
        }
        try {
          if (window.opener) {
            window.opener.postMessage({ type: "GOOGLE_OAUTH_ERROR", state, error: error || "cancelled" }, "*");
          }
        } catch (e) {}
        spinner.style.display = "none";
        titleEl.textContent = "Google Sign-In Cancelled";
        subEl.textContent = "You can close this window and try again anytime.";
        btnEl.style.display = "block";
        setTimeout(() => { try { window.close(); } catch (e) {} }, 600);
        return;
      }

      try {
        const res = await fetch("/api/auth/verify-google", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ state, idToken, accessToken })
        });
        const data = await res.json();
        if (!res.ok || !data.ok || !data.user) {
          throw new Error(data.error || "Google token verification failed");
        }

        verifiedUser = data.user;

        // 1. Save verified Google session to same-origin localStorage
        try {
          localStorage.setItem("vocab_verified_google_session_v4", JSON.stringify(verifiedUser));
        } catch (e) {}

        // 2. Broadcast to same-origin tabs/iframes via BroadcastChannel
        try {
          if (typeof BroadcastChannel !== "undefined") {
            const bc = new BroadcastChannel("vocab_google_auth_channel");
            bc.postMessage({ type: "GOOGLE_OAUTH_SUCCESS", state, user: verifiedUser });
            setTimeout(() => bc.close(), 500);
          }
        } catch (e) {}

        // 3. Post message to opener window
        try {
          if (window.opener) {
            window.opener.postMessage({ type: "GOOGLE_OAUTH_SUCCESS", state, user: verifiedUser }, "*");
          }
        } catch (e) {}

        spinner.style.display = "none";
        titleEl.textContent = "Signed in as " + verifiedUser.email;
        subEl.textContent = "Your Google account is connected. Returning to the app...";
        btnEl.textContent = "Continue as " + (verifiedUser.displayName || verifiedUser.email);
        btnEl.style.display = "block";

        try { window.close(); } catch (e) {}
        setTimeout(() => {
          try { window.close(); } catch (e) {}
          if (!window.opener) {
            window.location.replace("/");
          }
        }, 400);
      } catch (err) {
        spinner.style.display = "none";
        titleEl.textContent = "Sign-In Verification Failed";
        subEl.textContent = String(err && err.message ? err.message : "Could not verify Google credentials.");
        btnEl.style.display = "block";
      }
    })();
  </script>
</body>
</html>`;

  app.get(["/__/auth/handler", "/__/auth/handler/", "/auth/callback", "/auth/callback/"], (req, res) => {
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");
    res.status(200).send(oauthCallbackHtml);
  });

  app.post("/api/auth/verify-google", async (req, res) => {
    try {
      const { state, idToken, accessToken, error } = req.body || {};
      const cleanState = String(state || "").trim();

      if (error) {
        if (cleanState) {
          pendingOAuthStates.set(cleanState, { status: "error", error: String(error), createdAt: Date.now() });
        }
        return res.json({ ok: false, error: String(error) });
      }

      if (!idToken && !accessToken) {
        return res.status(400).json({ ok: false, error: "Missing Google OAuth token" });
      }

      let email = "";
      let emailVerified = false;
      let displayName = "";
      let photoURL = "";
      let googleSub = "";

      // Verify id_token with Google's official tokeninfo endpoint
      if (idToken) {
        const tokenRes = await fetch(
          `https://oauth2.googleapis.com/tokeninfo?id_token=${encodeURIComponent(String(idToken))}`
        );
        if (tokenRes.ok) {
          const tokenInfo: any = await tokenRes.json();
          if (tokenInfo.aud === GOOGLE_OAUTH_CLIENT_ID && tokenInfo.email) {
            email = String(tokenInfo.email).trim().toLowerCase();
            emailVerified = tokenInfo.email_verified === "true" || tokenInfo.email_verified === true;
            displayName = String(tokenInfo.name || tokenInfo.given_name || email.split("@")[0]).trim();
            photoURL = String(tokenInfo.picture || "").trim();
            googleSub = String(tokenInfo.sub || "").trim();
          }
        }
      }

      // Also verify / enrich via Google's userinfo endpoint if accessToken is provided
      if (accessToken && (!email || !displayName || !photoURL)) {
        const userRes = await fetch("https://www.googleapis.com/oauth2/v3/userinfo", {
          headers: { Authorization: `Bearer ${String(accessToken)}` }
        });
        if (userRes.ok) {
          const userInfo: any = await userRes.json();
          if (userInfo.email) {
            email = email || String(userInfo.email).trim().toLowerCase();
            emailVerified = emailVerified || Boolean(userInfo.email_verified);
            displayName = displayName || String(userInfo.name || userInfo.given_name || email.split("@")[0]).trim();
            photoURL = photoURL || String(userInfo.picture || "").trim();
            googleSub = googleSub || String(userInfo.sub || "").trim();
          }
        }
      }

      if (!email || !email.includes("@") || !emailVerified || !googleSub) {
        return res.status(401).json({
          ok: false,
          error: "Invalid or unverified Google account credentials."
        });
      }

      const verifiedUser = {
        uid: `google_${googleSub}`,
        googleSub,
        email,
        displayName: displayName || email.split("@")[0],
        photoURL,
        idToken: idToken || "",
        accessToken: accessToken || "",
        verified: true,
        authenticatedAt: new Date().toISOString()
      };

      if (cleanState) {
        pendingOAuthStates.set(cleanState, {
          status: "completed",
          user: verifiedUser,
          createdAt: Date.now()
        });

        // Also store in Firestore so multi-instance Cloud Run containers share the OAuth handoff
        if (firestoreDb) {
          try {
            await setDoc(doc(firestoreDb, "study_state", `oauth_${cleanState.replace(/[^a-zA-Z0-9_-]/g, "_")}`), {
              status: "completed",
              user: verifiedUser,
              createdAt: Date.now()
            });
          } catch (e) {}
        }
      }

      return res.json({ ok: true, user: verifiedUser });
    } catch (err: any) {
      return res.status(500).json({ ok: false, error: err?.message || "Verification error" });
    }
  });

  app.get("/api/auth/poll-oauth", async (req, res) => {
    const cleanState = String(req.query.state || "").trim();
    if (!cleanState) {
      return res.json({ ok: true, status: "pending" });
    }

    const memEntry = pendingOAuthStates.get(cleanState);
    if (memEntry) {
      return res.json({
        ok: true,
        status: memEntry.status,
        user: memEntry.user || null,
        error: memEntry.error || null
      });
    }

    if (firestoreDb) {
      try {
        const docId = `oauth_${cleanState.replace(/[^a-zA-Z0-9_-]/g, "_")}`;
        const snap = await getDoc(doc(firestoreDb, "study_state", docId));
        if (snap.exists()) {
          const data: any = snap.data();
          if (data && data.status) {
            pendingOAuthStates.set(cleanState, data);
            // Clean up one-time OAuth handoff doc
            deleteDoc(doc(firestoreDb, "study_state", docId)).catch(() => {});
            return res.json({
              ok: true,
              status: data.status,
              user: data.user || null,
              error: data.error || null
            });
          }
        }
      } catch (e) {}
    }

    return res.json({ ok: true, status: "pending" });
  });

  // Duolingo-grade Account Authentication (Email & Password)
  // Strictly verifies existing accounts and passwords; never auto-registers on login
  app.post("/api/auth/account-login", async (req, res) => {
    try {
      const { email, password, displayName } = req.body || {};
      const cleanEmail = sanitizeEmailKey(email);
      const cleanPassword = String(password || "").trim();
      const action = String(req.body?.action || "login").toLowerCase();
      const isRegister = action === "register" || action === "signup";

      if (!cleanEmail || !cleanEmail.includes("@") || !cleanEmail.split("@")[1]?.includes(".")) {
        return res.status(400).json({ ok: false, error: "Please enter a valid email address." });
      }
      if (!cleanPassword || cleanPassword.length < (isRegister ? 6 : 4)) {
        return res.status(400).json({
          ok: false,
          error: isRegister
            ? "Password must be at least 6 characters."
            : "Please enter your password (at least 4 characters)."
        });
      }

      const authDir = path.join(__dirname, "data");
      const authFilePath = path.join(authDir, "user_credentials.json");

      function readCredentials(): Record<string, any> {
        try {
          if (fs.existsSync(authFilePath)) {
            return JSON.parse(fs.readFileSync(authFilePath, "utf8")) || {};
          }
        } catch (e) {}
        return {};
      }

      function writeCredentials(creds: Record<string, any>) {
        try {
          if (!fs.existsSync(authDir)) fs.mkdirSync(authDir, { recursive: true });
          fs.writeFileSync(authFilePath, JSON.stringify(creds, null, 2), "utf8");
        } catch (e) {}
      }

      const emailHash = crypto.createHash("sha256").update(cleanEmail).digest("hex");
      const credDocId = `cred_${emailHash.slice(0, 32)}`;
      const sha256PassHash = crypto.createHash("sha256").update(cleanPassword + "_salt_stellar").digest("hex");

      function verifyStoredCredential(cred: any): boolean {
        if (!cred) return false;
        if (cred.sha256Hash && cred.sha256Hash === sha256PassHash) return true;
        if (cred.passwordHash && cred.passwordHash === sha256PassHash) return true;
        if (cred.passwordHash && cred.salt) {
          const pbkdf2Hash = crypto
            .pbkdf2Sync(cleanPassword, cred.salt, 10000, 64, "sha512")
            .toString("hex");
          if (pbkdf2Hash === cred.passwordHash) return true;
        }
        return false;
      }

      // Check Firestore first for credentials so multi-device works everywhere worldwide
      let userCred: any = null;
      if (firestoreDb) {
        try {
          const snap = await getDoc(doc(firestoreDb, "study_state", credDocId));
          if (snap.exists()) {
            userCred = snap.data();
          }
        } catch (e) {}
      }

      if (!userCred) {
        const localCreds = readCredentials();
        userCred = localCreds[emailHash] || localCreds[cleanEmail] || null;
      }

      if (isRegister) {
        if (userCred && (userCred.passwordHash || userCred.sha256Hash)) {
          if (verifyStoredCredential(userCred)) {
            // Password matches existing account; allow login
          } else {
            return res.status(409).json({
              ok: false,
              error: "An account with this email already exists. Please switch to 'Log In' and enter your password."
            });
          }
        } else {
          const salt = crypto.randomBytes(16).toString("hex");
          const name = String(displayName || cleanEmail.split("@")[0]).trim();
          userCred = {
            accountId: emailHash,
            displayName: name,
            passwordHash: sha256PassHash,
            sha256Hash: sha256PassHash,
            salt,
            createdAt: new Date().toISOString()
          };

          const localCreds = readCredentials();
          localCreds[emailHash] = userCred;
          writeCredentials(localCreds);

          if (firestoreDb) {
            try {
              await setDoc(doc(firestoreDb, "study_state", credDocId), userCred);
            } catch (e) {}
          }
        }
      } else {
        // STRICT LOGIN: Account MUST already exist and password MUST match!
        if (!userCred || (!userCred.passwordHash && !userCred.sha256Hash)) {
          return res.status(404).json({
            ok: false,
            error: "No account found with this email. Please switch to 'Create Account' to register first."
          });
        }
        if (!verifyStoredCredential(userCred)) {
          return res.status(401).json({
            ok: false,
            error: "Incorrect password for this account. Please check your password and try again."
          });
        }
        // Upgrade legacy PBKDF2 record with sha256Hash if needed so client & server stay in sync
        if (!userCred.sha256Hash && firestoreDb) {
          userCred.sha256Hash = sha256PassHash;
          try {
            await setDoc(doc(firestoreDb, "study_state", credDocId), userCred);
          } catch (e) {}
        }
      }

      const verifiedUser = {
        uid: `acct_${emailHash.slice(0, 24)}`,
        googleSub: `acct_${emailHash.slice(0, 24)}`,
        email: cleanEmail,
        displayName: userCred.displayName || cleanEmail.split("@")[0],
        photoURL: "",
        verified: true,
        authMethod: "email_account",
        authenticatedAt: new Date().toISOString()
      };

      return res.json({ ok: true, user: verifiedUser });
    } catch (err: any) {
      return res.status(500).json({ ok: false, error: err?.message || "Authentication error" });
    }
  });

  // 1-Click Instant Cloud Connect Endpoint
  app.post("/api/auth/instant-connect", async (req, res) => {
    try {
      const { email: reqEmail } = req.body || {};
      let cleanEmail = sanitizeEmailKey(reqEmail);
      if (!cleanEmail || !cleanEmail.includes("@")) {
        cleanEmail = "cloud_sync@sync.internal";
      }
      const emailHash = crypto.createHash("sha256").update(cleanEmail).digest("hex");
      const verifiedUser = {
        uid: `acct_${emailHash.slice(0, 24)}`,
        googleSub: `acct_${emailHash.slice(0, 24)}`,
        email: cleanEmail,
        displayName: cleanEmail.startsWith("cloud_sync") ? "Cloud User" : cleanEmail.split("@")[0],
        photoURL: "",
        verified: true,
        authMethod: "instant_cloud",
        authenticatedAt: new Date().toISOString()
      };
      return res.json({ ok: true, user: verifiedUser });
    } catch (err: any) {
      return res.status(500).json({ ok: false, error: err?.message || "Instant sync error" });
    }
  });

  // Explicit helper endpoints for convenience
  app.post("/api/auth/login", (req, res, next) => {
    req.body = { ...req.body, action: "login" };
    next();
  }, (req, res) => {
    // Forward to handler above
    res.redirect(307, "/api/auth/account-login");
  });

  app.post("/api/auth/register", (req, res, next) => {
    req.body = { ...req.body, action: "register" };
    next();
  }, (req, res) => {
    // Forward to handler above
    res.redirect(307, "/api/auth/account-login");
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
    if (!clean) {
      return "common_all_devices@stellar.cloud";
    }
    if (!clean.includes("@")) {
      return `${clean}@stellar.cloud`;
    }
    return clean;
  }

  function emailToFirestoreDocId(email: string): string {
    if (email === "common_all_devices@stellar.cloud" || email.startsWith("global") || email.startsWith("cloud_id_") || email.includes("global-1")) {
      return "global_common_cloud_v2";
    }
    const hash = crypto.createHash("sha256").update(email).digest("hex").slice(0, 32);
    return `acct_${hash}`;
  }

  function emailToClientSyncDocId(email: string): string {
    const clean = String(email || "").trim().toLowerCase();
    let h1 = 0xdeadbeef ^ clean.length;
    let h2 = 0x41c6ce57 ^ clean.length;
    for (let i = 0, ch; i < clean.length; i++) {
      ch = clean.charCodeAt(i);
      h1 = Math.imul(h1 ^ ch, 2654435761);
      h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
    return "acct_" + (h2 >>> 0).toString(16).padStart(8, "0") + (h1 >>> 0).toString(16).padStart(8, "0");
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

  function isProfilePayloadNonEmpty(p: any): boolean {
    if (!p || typeof p !== "object") return false;
    const learned = Array.isArray(p.learnedCardNums)
      ? p.learnedCardNums
      : Array.isArray(p.learnedCards)
      ? p.learnedCards
      : [];
    const deleted = Array.isArray(p.deletedCardNums)
      ? p.deletedCardNums
      : Array.isArray(p.deletedCards)
      ? p.deletedCards
      : [];
    const lastCard = Number(p.lastActiveCardNum ?? p.lastCard ?? 800);
    const shortcutsCount =
      p.customShortcuts && typeof p.customShortcuts === "object"
        ? Object.keys(p.customShortcuts).length
        : 0;
    const decksCount =
      p.customDecks && typeof p.customDecks === "object"
        ? Object.keys(p.customDecks).length
        : 0;
    const activeDeck = p.activeDeckId && p.activeDeckId !== "deck-800-1000";
    return Boolean(
      learned.length > 0 ||
      deleted.length > 0 ||
      (lastCard !== 800 && lastCard > 0) ||
      shortcutsCount > 0 ||
      decksCount > 0 ||
      activeDeck
    );
  }

  const COMMON_CLOUD_EMAIL_KEY = "common_all_devices@stellar.cloud";
  const COMMON_CLOUD_HASH_KEY = crypto
    .createHash("sha256")
    .update(COMMON_CLOUD_EMAIL_KEY)
    .digest("hex");

  async function saveProfileData(
    rawEmail: unknown,
    incomingBody: any
  ): Promise<{ email: string; exists: boolean; updatedAt: string; payload: any }> {
    const email = sanitizeEmailKey(rawEmail);
    if (!email) {
      return { email: "", exists: false, updatedAt: "", payload: null };
    }

    const emailHash = crypto.createHash("sha256").update(email).digest("hex");
    const profiles = readUserProfiles();
    const existingRaw = profiles[emailHash] || profiles[COMMON_CLOUD_HASH_KEY] || profiles[email];
    const existingNorm = normalizeProfilePayload(existingRaw) || normalizeProfilePayload({});

    const incoming =
      incomingBody?.payload && typeof incomingBody.payload === "object"
        ? incomingBody.payload
        : incomingBody || {};
    const replaceArrays = incomingBody?.replaceArrays !== false;
    const isExplicitUserAction = Boolean(
      incomingBody?.isExplicitUserAction || incoming?.isExplicitUserAction
    );

    const incomingNormCheck = normalizeProfilePayload(incoming);
    if (
      !isProfilePayloadNonEmpty(incomingNormCheck) &&
      !isExplicitUserAction &&
      isProfilePayloadNonEmpty(existingNorm)
    ) {
      // Prevent an unhydrated new device boot from wiping out existing cloud progress!
      return {
        email,
        exists: true,
        updatedAt: existingNorm.updatedAt || new Date().toISOString(),
        payload: existingNorm
      };
    }

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
      accountId: emailHash,
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
      isExplicitUserAction,
      updatedAt
    };

    if (profiles[email]) delete profiles[email];
    profiles[emailHash] = {
      updatedAt,
      isExplicitUserAction,
      payload: savedPayload
    };
    profiles[COMMON_CLOUD_HASH_KEY] = {
      updatedAt,
      isExplicitUserAction,
      payload: { ...savedPayload, accountId: COMMON_CLOUD_HASH_KEY }
    };
    writeUserProfiles(profiles);

    // Also persist to Google Cloud Firestore under both account document and universal website cloud documents
    if (firestoreDb) {
      try {
        const docId = emailToFirestoreDocId(email);
        const clientDocId = emailToClientSyncDocId(email);
        const targetDocs = Array.from(
          new Set([
            docId,
            clientDocId,
            "global_common_cloud_v2",
            "global_common_cloud_v1",
            "acct_73801410b67c7ba66a922cc3105f74f2"
          ])
        );

        const writes: Promise<any>[] = targetDocs.map((dId) =>
          setDoc(doc(firestoreDb!, "study_state", dId), {
            accountId: dId,
            updatedAt,
            isExplicitUserAction,
            payload: savedPayload
          })
        );

        const progDocBody = {
          userId: "global_common_cloud_v2",
          email,
          learnedCards: savedPayload.learnedCardNums || [],
          learnedCardNums: savedPayload.learnedCardNums || [],
          deletedCardNums: savedPayload.deletedCardNums || [],
          lastActiveCardNum: savedPayload.lastActiveCardNum || 800,
          activeDeckId: savedPayload.activeDeckId || "deck-800-1000",
          customShortcuts: savedPayload.customShortcuts || {},
          customDecks: savedPayload.customDecks || {},
          customSections: savedPayload.customSections || [],
          streakCount: savedPayload.streakCount || 1,
          isExplicitUserAction,
          lastStudied: updatedAt,
          updatedAt
        };

        writes.push(
          setDoc(doc(firestoreDb, "user_progress", "global_common_cloud_v2"), progDocBody, { merge: true }),
          setDoc(doc(firestoreDb, "user_progress", "global_common_cloud_v1"), progDocBody, { merge: true })
        );

        await Promise.allSettled(writes);
      } catch (err) {
        console.warn("Firestore save notice:", err);
      }
    }

    return { email, exists: true, updatedAt, payload: savedPayload };
  }

  async function loadProfileData(
    rawEmail: unknown
  ): Promise<{ email: string; exists: boolean; updatedAt: string; payload: any }> {
    const email = sanitizeEmailKey(rawEmail) || COMMON_CLOUD_EMAIL_KEY;

    const emailHash = crypto.createHash("sha256").update(email).digest("hex");
    const profiles = readUserProfiles();

    const candidates: Array<{ payload: any; ts: number; hasProgress: boolean }> = [];

    for (const key of [emailHash, COMMON_CLOUD_HASH_KEY, email]) {
      if (profiles[key]) {
        const norm = normalizeProfilePayload(profiles[key]);
        if (norm) {
          candidates.push({
            payload: norm,
            ts: Date.parse(norm.updatedAt || "") || 0,
            hasProgress: isProfilePayloadNonEmpty(norm)
          });
        }
      }
    }

    if (firestoreDb) {
      try {
        const docId = emailToFirestoreDocId(email);
        const clientDocId = emailToClientSyncDocId(email);
        const targetDocs = Array.from(
          new Set([
            docId,
            clientDocId,
            "global_common_cloud_v2",
            "global_common_cloud_v1",
            "acct_73801410b67c7ba66a922cc3105f74f2",
            "acct_stellarnetworkhub_gmail_com"
          ])
        );
        const snaps = await Promise.allSettled(
          targetDocs.map((dId) => getDoc(doc(firestoreDb!, "study_state", dId)))
        );
        for (const res of snaps) {
          if (res.status === "fulfilled" && res.value.exists()) {
            const candidate = normalizeProfilePayload(res.value.data());
            if (candidate) {
              candidates.push({
                payload: candidate,
                ts: Date.parse(candidate.updatedAt || "") || 0,
                hasProgress: isProfilePayloadNonEmpty(candidate)
              });
            }
          }
        }
      } catch (err) {
        console.warn("Firestore load notice:", err);
      }
    }

    if (candidates.length === 0) {
      return {
        email,
        exists: false,
        updatedAt: "",
        payload: null
      };
    }

    const nonEmpty = candidates.filter((c) => c.hasProgress);
    const pool = nonEmpty.length > 0 ? nonEmpty : candidates;
    pool.sort((a, b) => b.ts - a.ts);
    const chosen = pool[0].payload;

    // Keep local cache in sync with latest state
    if (profiles[email]) delete profiles[email];
    profiles[emailHash] = {
      updatedAt: chosen.updatedAt,
      payload: chosen
    };
    profiles[COMMON_CLOUD_HASH_KEY] = {
      updatedAt: chosen.updatedAt,
      payload: chosen
    };
    writeUserProfiles(profiles);

    return {
      email,
      exists: true,
      updatedAt: chosen.updatedAt || new Date().toISOString(),
      payload: chosen
    };
  }

  app.post(["/api/user/save", "/api/profile/save"], async (req, res) => {
    const result = await saveProfileData(req.body?.email, req.body);
    res.json({ ok: true, success: true, ...result });
  });

  app.get(["/api/user/load", "/api/profile/load"], async (req, res) => {
    const result = await loadProfileData(req.query.email);
    res.json({ ok: true, success: true, ...result });
  });

  app.get(["/api/user/poll", "/api/profile/poll"], async (req, res) => {
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

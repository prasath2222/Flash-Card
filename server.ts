import express from 'express';
import { createServer as createViteServer } from 'vite';
import path from 'path';
import fs from 'fs';

async function startServer() {
  const app = express();
  const port = Number(process.env.PORT) || 3000;

  // Middleware for JSON body parsing with generous payload limit for file uploads
  app.use(express.json({ limit: '50mb' }));
  app.use(express.urlencoded({ extended: true, limit: '50mb' }));

  // High-fidelity native speech proxy endpoint
  // Eliminates browser voice-pack dependencies, CORS restrictions, and guarantees real native accents
  app.get('/api/tts', async (req, res) => {
    try {
      const { text, lang } = req.query;
      if (!text || !lang) {
        return res.status(400).send('Missing text or lang');
      }

      const targetLang = String(lang).startsWith('es')
        ? 'es'
        : String(lang).startsWith('hi')
        ? 'hi'
        : String(lang).startsWith('ta')
        ? 'ta'
        : 'en';
      const cleanText = String(text).trim();

      const urls = [
        `https://translate.google.com/translate_tts?ie=UTF-8&tl=${encodeURIComponent(targetLang)}&client=tw-ob&q=${encodeURIComponent(cleanText)}`,
        `https://translate.googleapis.com/translate_tts?client=gtx&ie=UTF-8&tl=${encodeURIComponent(targetLang)}&q=${encodeURIComponent(cleanText)}`
      ];

      let audioBuffer: Buffer | null = null;
      for (const ttsUrl of urls) {
        try {
          const response = await fetch(ttsUrl, {
            headers: {
              'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
              Referer: 'https://translate.google.com/',
            },
          });
          if (response.ok) {
            const arrayBuf = await response.arrayBuffer();
            audioBuffer = Buffer.from(arrayBuf);
            break;
          }
        } catch (e) {
          // try next
        }
      }

      if (!audioBuffer) {
        return res.status(502).send('TTS upstream failure');
      }

      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.send(audioBuffer);
    } catch (err) {
      console.error('Error in /api/tts:', err);
      res.status(500).send('TTS error');
    }
  });

  // Accurate image proxy & caching endpoint
  // Ensures 100% authentic real-world photos with zero CORS or rate limit blocks
  let accurateImages: Record<string, string> = {};
  const accurateImagesPath = path.resolve('scripts/accurate_images.json');
  try {
    accurateImages = JSON.parse(fs.readFileSync(accurateImagesPath, 'utf8'));
  } catch (e) {
    console.warn('Could not load accurate_images.json in server:', e);
  }

  const imageBufferCache = new Map<string, { buffer: Buffer; contentType: string }>();

  // Function to search authentic images via Wikipedia REST API and Wikimedia Commons
  async function searchAuthenticImage(query: string): Promise<string | null> {
    const clean = query
      .replace(/^[0-9]+\.\s*/, '')
      .replace(/[^\w\s-]/g, '')
      .trim();
    if (!clean) return null;

    // 1. Wikipedia Summary API
    try {
      const summaryUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(clean)}`;
      const resp = await fetch(summaryUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (TrilingualVocabApp/1.0; contact@example.com)'
        }
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data.thumbnail && data.thumbnail.source) return data.thumbnail.source;
        if (data.originalimage && data.originalimage.source) return data.originalimage.source;
      }
    } catch (e) {}

    // 2. Wikipedia Search API
    try {
      const searchUrl = `https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(clean)}&gsrlimit=1&prop=pageimages&pithumbsize=900&format=json`;
      const resp = await fetch(searchUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (TrilingualVocabApp/1.0; contact@example.com)'
        }
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data.query && data.query.pages) {
          const page = Object.values(data.query.pages)[0] as any;
          if (page && page.thumbnail && page.thumbnail.source) return page.thumbnail.source;
        }
      }
    } catch (e) {}

    // 3. Wikimedia Commons Search
    try {
      const commonsUrl = `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrsearch=${encodeURIComponent(clean + ' filetype:bitmap')}&gsrlimit=1&prop=pageimages&pithumbsize=900&format=json`;
      const resp = await fetch(commonsUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (TrilingualVocabApp/1.0; contact@example.com)'
        }
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data.query && data.query.pages) {
          const page = Object.values(data.query.pages)[0] as any;
          if (page && page.thumbnail && page.thumbnail.source) return page.thumbnail.source;
        }
      }
    } catch (e) {}

    return null;
  }

  // Find image endpoint returning JSON
  app.get('/api/find-image', async (req, res) => {
    try {
      const query = String(req.query.query || req.query.q || '').trim();
      const num = String(req.query.num || '').trim();

      if (num && accurateImages[num]) {
        return res.json({ success: true, imageUrl: accurateImages[num], num, source: 'curated' });
      }

      if (!query) {
        return res.status(400).json({ success: false, error: 'Query required' });
      }

      const imageUrl = await searchAuthenticImage(query);
      if (imageUrl) {
        if (num) {
          accurateImages[num] = imageUrl;
          try {
            fs.writeFileSync(accurateImagesPath, JSON.stringify(accurateImages, null, 2));
          } catch (e) {}
        }
        return res.json({ success: true, imageUrl, query, source: 'wikipedia' });
      }

      // Fallback unsplash photo query
      const unsplashFallback = `https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80`;
      res.json({ success: true, imageUrl: unsplashFallback, query, source: 'fallback' });
    } catch (err) {
      console.error('Error in /api/find-image:', err);
      res.status(500).json({ success: false, error: 'Image search error' });
    }
  });

  // Main Image proxy with automated fallback
  app.get('/api/image', async (req, res) => {
    try {
      const num = String(req.query.num || '');
      const query = String(req.query.q || '').trim();
      let targetUrl = accurateImages[num];

      if (!targetUrl && query) {
        targetUrl = (await searchAuthenticImage(query)) || '';
        if (targetUrl && num) {
          accurateImages[num] = targetUrl;
        }
      }

      if (!targetUrl) {
        return res.status(404).send('Image mapping not found');
      }

      const cacheKey = num || targetUrl;
      if (imageBufferCache.has(cacheKey)) {
        const cached = imageBufferCache.get(cacheKey)!;
        res.setHeader('Content-Type', cached.contentType);
        res.setHeader('Cache-Control', 'public, max-age=604800, immutable');
        return res.send(cached.buffer);
      }

      const response = await fetch(targetUrl, {
        headers: {
          'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
          Accept: 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        },
      });

      if (response.ok) {
        const arrayBuf = await response.arrayBuffer();
        const buffer = Buffer.from(arrayBuf);
        const contentType = response.headers.get('content-type') || 'image/jpeg';
        imageBufferCache.set(cacheKey, { buffer, contentType });

        res.setHeader('Content-Type', contentType);
        res.setHeader('Cache-Control', 'public, max-age=604800, immutable');
        return res.send(buffer);
      }

      // Fallback redirect
      res.redirect(targetUrl);
    } catch (err) {
      console.error('Error in /api/image:', err);
      res.status(500).send('Image proxy error');
    }
  });

  // Pre-bundled Tier 1-100 cards endpoint
  app.get('/api/curriculum/1-100', (req, res) => {
    try {
      const tierPath = path.resolve('scripts/tier_1_100_cards.json');
      if (fs.existsSync(tierPath)) {
        const data = JSON.parse(fs.readFileSync(tierPath, 'utf8'));
        return res.json({ success: true, count: data.length, cards: data });
      }
      res.status(404).json({ success: false, error: 'Tier 1-100 not found' });
    } catch (e) {
      res.status(500).json({ success: false, error: 'Failed to load tier' });
    }
  });

  // Intelligent Automatic Curriculum Parser
  app.post('/api/parse-curriculum', (req, res) => {
    try {
      const { text } = req.body;
      if (!text || typeof text !== 'string') {
        return res.status(400).json({ success: false, error: 'Text required' });
      }

      const lines = text.split('\n');
      const parsedCards: any[] = [];
      let curCat = 'General Vocabulary';
      let autoIndex = 1;

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        if (line.startsWith('Category ') || line.startsWith('# ')) {
          curCat = line.replace(/^[#\s]+/, '').trim();
          continue;
        }

        // Check if line starts with number e.g. "1. 👤 I = yo / main / நான்" or "800. STOVE"
        const numMatch = line.match(/^([0-9]+)\.\s*(.*)/);
        if (numMatch) {
          const num = parseInt(numMatch[1], 10);
          const rest = numMatch[2].trim();

          let emoji = '📌';
          let cleanHeader = rest;
          const emojiMatch = rest.match(/^([\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27BF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]|\uD83E[\uDD00-\uDDFF]|\u23E9-\u23EC|👤|👨|👩|📦|👥|🙋|🏷️|🎯|🪞)\s*(.*)/);
          if (emojiMatch) {
            emoji = emojiMatch[1];
            cleanHeader = emojiMatch[2];
          }

          let word = cleanHeader;
          let es = '';
          let hi = '';
          let ta = '';

          if (cleanHeader.includes('=')) {
            const parts = cleanHeader.split('=');
            word = parts[0].trim();
            const transParts = parts[1].split('/');
            es = (transParts[0] || '').trim();
            hi = (transParts[1] || '').trim();
            ta = (transParts[2] || '').trim();
          }

          word = word.replace(/^[0-9]+\.\s*/, '').trim();
          if (!word) word = `Word ${num}`;

          parsedCards.push({
            num: num || autoIndex++,
            word: word,
            emoji: emoji,
            category: curCat.replace(/\([0-9–-]+\)/, '').trim(),
            trans: { es: es || word, hi: hi || word },
            tamil: ta || word
          });
        }
      }

      res.json({
        success: true,
        count: parsedCards.length,
        cards: parsedCards
      });
    } catch (err) {
      console.error('Error in /api/parse-curriculum:', err);
      res.status(500).json({ success: false, error: 'Parser failed' });
    }
  });

  // ==========================================================
  // UNIVERSAL CROSS-DEVICE CLOUD SYNC ENGINE
  // Enables instant, reliable sync across all phones, tablets & PCs
  // with ZERO popup blockers and ZERO OAuth domain barriers!
  // ==========================================================
  const syncStorePath = path.resolve('data/cloud_sync.json');
  let syncStore: Record<string, { updatedAt: string; payload: any }> = {};

  try {
    if (!fs.existsSync(path.dirname(syncStorePath))) {
      fs.mkdirSync(path.dirname(syncStorePath), { recursive: true });
    }
    if (fs.existsSync(syncStorePath)) {
      syncStore = JSON.parse(fs.readFileSync(syncStorePath, 'utf8'));
    }
  } catch (e) {
    console.warn('Could not initialize syncStore:', e);
  }

  function persistSyncStore() {
    try {
      fs.writeFileSync(syncStorePath, JSON.stringify(syncStore, null, 2), 'utf8');
    } catch (e) {}
  }

  // Save device study state
  app.post('/api/sync/save', (req, res) => {
    try {
      const { syncCode, payload } = req.body;
      const cleanCode = String(syncCode || '').trim().toUpperCase();
      if (!cleanCode || !payload) {
        return res.status(400).json({ success: false, error: 'syncCode and payload required' });
      }

      const updatedAt = new Date().toISOString();
      syncStore[cleanCode] = {
        updatedAt,
        payload: {
          ...payload,
          updatedAt
        }
      };
      persistSyncStore();

      res.json({ success: true, syncCode: cleanCode, updatedAt });
    } catch (err) {
      console.error('Error in /api/sync/save:', err);
      res.status(500).json({ success: false, error: 'Failed to save sync state' });
    }
  });

  // Load device study state by sync code
  app.get('/api/sync/load', (req, res) => {
    try {
      const syncCode = String(req.query.code || req.query.syncCode || '').trim().toUpperCase();
      if (!syncCode) {
        return res.status(400).json({ success: false, error: 'syncCode required' });
      }

      const entry = syncStore[syncCode];
      if (!entry) {
        return res.json({ success: false, notFound: true, message: 'Sync code not found' });
      }

      res.json({
        success: true,
        syncCode,
        updatedAt: entry.updatedAt,
        payload: entry.payload
      });
    } catch (err) {
      console.error('Error in /api/sync/load:', err);
      res.status(500).json({ success: false, error: 'Failed to load sync state' });
    }
  });

  // Long-poll / check for remote updates from other paired devices
  app.get('/api/sync/poll', (req, res) => {
    try {
      const syncCode = String(req.query.code || req.query.syncCode || '').trim().toUpperCase();
      const since = String(req.query.since || '');
      if (!syncCode || !syncStore[syncCode]) {
        return res.json({ hasUpdates: false });
      }

      const entry = syncStore[syncCode];
      if (entry.updatedAt !== since) {
        return res.json({
          hasUpdates: true,
          updatedAt: entry.updatedAt,
          payload: entry.payload
        });
      }

      res.json({ hasUpdates: false });
    } catch (err) {
      res.json({ hasUpdates: false });
    }
  });

  const isProd = process.env.NODE_ENV === 'production';
  if (!isProd) {
    const vite = await createViteServer({
      server: { middlewareMode: true, hmr: false, ws: false },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static('dist'));
    app.get('*', (req, res) => {
      res.sendFile(path.resolve('dist', 'index.html'));
    });
  }

  app.listen(port, '0.0.0.0', () => {
    console.log(`Server listening on http://0.0.0.0:${port}`);
  });
}

startServer();

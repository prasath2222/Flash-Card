import express from 'express';
import { createServer as createViteServer } from 'vite';
import path from 'path';

async function startServer() {
  const app = express();
  const port = Number(process.env.PORT) || 3000;

  // Middleware for JSON body parsing if needed
  app.use(express.json());

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
  try {
    const fs = await import('fs');
    accurateImages = JSON.parse(fs.readFileSync(path.resolve('scripts/accurate_images.json'), 'utf8'));
  } catch (e) {
    console.warn('Could not load accurate_images.json in server:', e);
  }

  const imageBufferCache = new Map<string, { buffer: Buffer; contentType: string }>();

  app.get('/api/image', async (req, res) => {
    try {
      const num = String(req.query.num || '');
      const targetUrl = accurateImages[num];
      if (!targetUrl) {
        return res.status(404).send('Image mapping not found');
      }

      if (imageBufferCache.has(num)) {
        const cached = imageBufferCache.get(num)!;
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
        imageBufferCache.set(num, { buffer, contentType });

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

  const isProd = process.env.NODE_ENV === 'production';
  if (!isProd) {
    const vite = await createViteServer({
      server: { middlewareMode: true, hmr: false },
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

import path from 'path';
import {defineConfig} from 'vite';

export default defineConfig(() => {
  return {
    plugins: [],
    resolve: {
      alias: {
        '@': path.resolve(process.cwd(), '.'),
      },
    },
    server: {
      // HMR is disabled in preview environments to prevent websocket errors in iframes.
      hmr: false,
      ws: false as const,
      watch: null,
    },
  };
});


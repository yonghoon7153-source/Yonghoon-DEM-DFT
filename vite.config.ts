import { defineConfig } from 'vite';

// BASE_PATH lets the same build be served from a sub-path (GitHub Pages project site)
// or from the root (Cloudflare Pages, local preview).
export default defineConfig({
  base: process.env.BASE_PATH ?? '/',
  build: {
    target: 'es2022',
    sourcemap: false,
    assetsInlineLimit: 0,
  },
  server: { port: 5004, host: true },
  preview: { port: 5004, host: true },
});

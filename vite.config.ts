import { createHash } from 'node:crypto';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, type Plugin } from 'vite';

// Mascot pictures live in public/, which Vite does not fingerprint: a replaced picture kept its URL and browsers
// went on showing the copy they had cached (せんとくん, 10차 요청). `virtual:asset-versions` gives every file a
// short content hash that the page puts in the picture's URL (?v=…), so a new picture is always a new URL.
function assetVersions(): Plugin {
  const id = 'virtual:asset-versions';
  const dir = fileURLToPath(new URL('./public/mascots', import.meta.url));
  return {
    name: 'nihon-asset-versions',
    resolveId: (source) => (source === id ? `\0${id}` : null),
    load(resolved) {
      if (resolved !== `\0${id}`) return null;
      const versions: Record<string, string> = {};
      for (const f of readdirSync(dir).sort()) {
        versions[`mascots/${f}`] = createHash('sha1').update(readFileSync(join(dir, f))).digest('hex').slice(0, 10);
      }
      return `export default ${JSON.stringify(versions)};`;
    },
  };
}

// BASE_PATH lets the same build be served from a sub-path (GitHub Pages project site)
// or from the root (Cloudflare Pages, local preview).
export default defineConfig({
  base: process.env.BASE_PATH ?? '/',
  plugins: [assetVersions()],
  build: {
    target: 'es2022',
    sourcemap: false,
    assetsInlineLimit: 0,
  },
  server: { port: 5004, host: true },
  preview: { port: 5004, host: true },
});

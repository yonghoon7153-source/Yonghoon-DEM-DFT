import { createHash } from 'node:crypto';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, type Plugin } from 'vite';

// Mascot pictures and the map data live in public/, which Vite does not fingerprint: a replaced file kept its URL and
// browsers went on showing the copy they had cached (せんとくん, 10차 요청; the map without 北方領土 still showed the
// old shape after F5, because /geo/* may be cached for a day — see public/_headers). `virtual:asset-versions` gives
// every file a short content hash that the page puts in its URL (?v=…), so new data is always a new URL.
const VERSIONED_DIRS = ['mascots', 'geo'];
function assetVersions(): Plugin {
  const id = 'virtual:asset-versions';
  return {
    name: 'nihon-asset-versions',
    resolveId: (source) => (source === id ? `\0${id}` : null),
    load(resolved) {
      if (resolved !== `\0${id}`) return null;
      const versions: Record<string, string> = {};
      for (const sub of VERSIONED_DIRS) {
        const dir = fileURLToPath(new URL(`./public/${sub}`, import.meta.url));
        for (const f of readdirSync(dir).sort()) {
          versions[`${sub}/${f}`] = createHash('sha1').update(readFileSync(join(dir, f))).digest('hex').slice(0, 10);
        }
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

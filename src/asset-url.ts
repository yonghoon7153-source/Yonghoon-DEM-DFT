// A file in public/ with its content hash (?v=…, from vite.config.ts): new content is a new URL, so no browser
// keeps showing the copy it cached — mascot pictures (せんとくん) and the map data (北方領土, 甲信越 …) alike.
import versions from 'virtual:asset-versions';

export function assetUrl(path: string): string {
  const v = versions[path];
  return `${import.meta.env.BASE_URL}${path}${v ? `?v=${v}` : ''}`;
}

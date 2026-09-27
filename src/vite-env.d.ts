/// <reference types="vite/client" />

declare module 'virtual:asset-versions' {
  /** Short content hash of each mascot picture, by its path under public/ ("mascots/kumamon.webp" → "3f2a…"). */
  const versions: Record<string, string>;
  export default versions;
}

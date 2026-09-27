// Real local mascots (ご当地キャラ), drawn as likenesses in the site's style — see ADR 0003.
// Keyed by data/mascots.json id. Split in two files to keep each readable.
import { artA } from './art-a';
import { artB } from './art-b';

export const mascotArt: Record<string, string> = { ...artA, ...artB };

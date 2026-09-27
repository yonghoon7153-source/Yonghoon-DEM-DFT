// One place that decides how a mascot is shown: the official image when we have one, else the drawn likeness.
import { mascots } from '../data';
import type { Mascot } from '../types';

// The drawn likenesses are only a fallback now that every mascot has a picture, so they live in their own
// chunk and are fetched only while some mascot still has no image. `artReady` settles once they are usable.
let mascotArt: Record<string, string> = {};
export const artReady: Promise<void> = mascots.some((m) => !m.image)
  ? import('./art').then((a) => { mascotArt = a.mascotArt; })
  : Promise.resolve();

/** HTML for an <img> or the inline SVG likeness. */
export function mascotVisualHtml(m: Mascot): string {
  if (m.image) return `<img src="${import.meta.env.BASE_URL}${m.image}" alt="" loading="lazy" decoding="async" />`;
  return mascotArt[m.id] ?? '';
}

/** What the map sticker should draw: an image URL or SVG markup. */
export function mascotSticker(m: Mascot): { image?: string; svg?: string } {
  if (m.image) return { image: `${import.meta.env.BASE_URL}${m.image}` };
  const svg = mascotArt[m.id];
  return svg ? { svg } : {};
}

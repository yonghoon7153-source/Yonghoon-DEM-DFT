// One place that decides how a mascot is shown: the official image when we have one, else the drawn likeness.
import type { Mascot } from '../types';
import { mascotArt } from './art';

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

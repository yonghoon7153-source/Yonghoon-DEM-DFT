// Shared drawing helpers for the mascot likenesses (100×100 canvas, warm brown outline).
export const INK = '#5a4a44';
export const S = `stroke="${INK}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"`;
export const THIN = `stroke="${INK}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"`;

export function svg(inner: string): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100" role="img">${inner}</svg>`;
}

/** Two eyes. `sclera` draws white eyeballs (Kumamon-style), `r` is the pupil radius. */
export function eyes(cx: number, cy: number, o: { gap?: number; r?: number; sclera?: number; dx?: number; dy?: number; color?: string } = {}): string {
  const gap = o.gap ?? 9, r = o.r ?? 2.7, dx = o.dx ?? 0, dy = o.dy ?? 0, c = o.color ?? INK;
  const one = (x: number) =>
    `${o.sclera ? `<ellipse cx="${x}" cy="${cy}" rx="${o.sclera}" ry="${o.sclera * 1.15}" fill="#fff" ${THIN}/>` : ''}<circle cx="${x + dx}" cy="${cy + dy}" r="${r}" fill="${c}"/><circle cx="${x + dx - r * 0.35}" cy="${cy + dy - r * 0.38}" r="${Math.max(0.6, r * 0.34)}" fill="#fff"/>`;
  return one(cx - gap) + one(cx + gap);
}

export function blush(cx: number, cy: number, gap = 15, rx = 4.6, ry = 2.6, color = '#f5a3b3'): string {
  return `<ellipse cx="${cx - gap}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${color}" opacity=".75"/><ellipse cx="${cx + gap}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${color}" opacity=".75"/>`;
}

export type MouthKind = 'smile' | 'w' | 'o' | 'grin' | 'flat' | 'wide';
export function mouth(cx: number, cy: number, kind: MouthKind = 'smile', w = 8): string {
  const h = w / 2;
  switch (kind) {
    case 'smile': return `<path d="M${cx - h} ${cy} q${h} ${h * 0.9} ${w} 0" fill="none" ${THIN}/>`;
    case 'w': return `<path d="M${cx - h} ${cy - 1} q${h / 2} 3.5 ${h} 0 q${h / 2} 3.5 ${h} 0" fill="none" ${THIN}/>`;
    case 'o': return `<ellipse cx="${cx}" cy="${cy}" rx="2.4" ry="3" fill="${INK}"/>`;
    case 'grin': return `<path d="M${cx - h} ${cy - 1} q${h} ${w * 0.9} ${w} 0 z" fill="#c9525a" ${THIN}/>`;
    case 'wide': return `<path d="M${cx - h} ${cy - 2} q${h} ${w} ${w} 0 z" fill="#fff" ${THIN}/>`;
    case 'flat': return `<path d="M${cx - h * 0.6} ${cy} h${w * 0.6}" fill="none" ${THIN}/>`;
  }
}

/** Convenience: eyes + mouth + blush in one go (kawaii default). */
export function face(cx: number, cy: number, o: { gap?: number; mouth?: MouthKind; blush?: boolean; blushDy?: number; eyeR?: number; sclera?: number; mouthDy?: number; mouthW?: number } = {}): string {
  return (
    eyes(cx, cy, { gap: o.gap, r: o.eyeR, sclera: o.sclera }) +
    mouth(cx, cy + (o.mouthDy ?? 7), o.mouth ?? 'smile', o.mouthW) +
    (o.blush === false ? '' : blush(cx, cy + (o.blushDy ?? 5), (o.gap ?? 9) + 6))
  );
}

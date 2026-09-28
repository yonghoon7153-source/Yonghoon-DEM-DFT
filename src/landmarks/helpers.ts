// Shared drawing bits for the landmark stickers — the same hand as the mascot likenesses (100×100, warm brown outline),
// a little bolder because a sticker is drawn at ~30 px (ADR 0011).
import { INK } from '../mascots/helpers';

export { INK };
export const O = `stroke="${INK}" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"`;
export const T = `stroke="${INK}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"`;
export const N = 'fill="none"';

export const C = {
  red: '#e0544b', verm: '#ea6a45', gold: '#f2c94c', white: '#fffdf9', cream: '#f3ead9', wood: '#c69262', dwood: '#8a6d5a',
  roof: '#5a4a44', teal: '#6fb0a6', water: '#a9d8ec', sea: '#6fb6e0', green: '#8fc47b', dgreen: '#5e9c6a', sand: '#f3d9a4',
  stone: '#cfc8bf', brick: '#c8553d', pink: '#f9c8d6', sky: '#dfeef7', steel: '#dfe3e8', navy: '#3d4a73',
} as const;

/** Water across the bottom, from `y` down: a soft blob with two white wave marks. */
export function water(y: number, fill: string = C.water): string {
  return (
    `<path d="M10 ${y} Q50 ${y - 6} 90 ${y} Q93 ${y + 12} 82 ${y + 16} Q50 ${y + 22} 18 ${y + 16} Q7 ${y + 12} 10 ${y} Z" fill="${fill}" ${O}/>` +
    `<path d="M26 ${y + 8} q6 -3 12 0 M58 ${y + 10} q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`
  );
}
/** Grass (or sand, gravel) across the bottom, from `y` down. */
export function ground(y: number, fill: string = C.green): string {
  return `<path d="M10 ${y} Q50 ${y - 6} 90 ${y} Q93 ${y + 12} 82 ${y + 16} Q50 ${y + 22} 18 ${y + 16} Q7 ${y + 12} 10 ${y} Z" fill="${fill}" ${O}/>`;
}
/** A torii: two posts, the nuki tie beam, the little centre strut and the bowed kasagi on top. */
export function torii(color: string, x = 50, top = 24, w = 72, h = 62): string {
  const L = x - w / 2, R = x + w / 2, px = w * 0.29;
  return (
    `<rect x="${x - px - 4}" y="${top + 8}" width="8" height="${h - 8}" fill="${color}" ${O}/>` +
    `<rect x="${x + px - 4}" y="${top + 8}" width="8" height="${h - 8}" fill="${color}" ${O}/>` +
    `<rect x="${L + 7}" y="${top + 18}" width="${w - 14}" height="6" fill="${color}" ${O}/>` +
    `<rect x="${x - 3.5}" y="${top + 8}" width="7" height="10" fill="${color}" ${O}/>` +
    `<path d="M${L} ${top + 1} Q${x} ${top - 6} ${R} ${top + 1} L${R - 3} ${top + 8} H${L + 3} Z" fill="${color}" ${O}/>`
  );
}
/**
 * A castle keep in three tiers on its stone base. `trim` puts shachihoko (gold on 大阪城 · 鶴ヶ城) on the top roof;
 * `band` draws a white plaster band on dark walls (松江城's black boards).
 */
export function castle(wall: string, roof: string, o: { trim?: string; band?: string } = {}): string {
  const band = (x: number, y: number, w: number) => (o.band ? `<rect x="${x}" y="${y}" width="${w}" height="3.4" fill="${o.band}"/>` : '');
  return (
    `<path d="M16 90 L24 72 H76 L84 90 Z" fill="${C.stone}" ${O}/>` +
    `<path d="M30 80 h14 M52 84 h16 M36 87 h10" ${N} ${T}/>` +
    `<rect x="29" y="58" width="42" height="14" fill="${wall}" ${O}/>${band(30.7, 59.7, 38.6)}` +
    `<path d="M38 64.5 h5 M48 64.5 h5 M58 64.5 h5" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>` +
    `<path d="M17 59 Q20 54 26 52 L32 47 H68 L74 52 Q80 54 83 59 Z" fill="${roof}" ${O}/>` +
    `<rect x="34" y="37" width="32" height="10" fill="${wall}" ${O}/>${band(35.7, 38.7, 28.6)}` +
    `<path d="M24 38 Q27 34 32 32 L37 28 H63 L68 32 Q73 34 76 38 Z" fill="${roof}" ${O}/>` +
    `<rect x="39" y="20" width="22" height="8" fill="${wall}" ${O}/>${band(40.7, 21.7, 18.6)}` +
    `<path d="M31 21 Q34 17 38 15 L42 11 H58 L62 15 Q66 17 69 21 Z" fill="${roof}" ${O}/>` +
    (o.trim ? `<path d="M41 11 q-4 -5 0 -8 M59 11 q4 -5 0 -8" ${N} stroke="${o.trim}" stroke-width="3.6" stroke-linecap="round"/>` : '')
  );
}
/** A stroke with a brown outline around it (arms, rails, tassels): the outline first, the colour on top. */
export function line(d: string, color: string, w = 5): string {
  return `<path d="${d}" ${N} stroke="${INK}" stroke-width="${w + 2.8}" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" ${N} stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
}

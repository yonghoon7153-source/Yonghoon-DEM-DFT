// Landmark stickers, 東海 · 近畿 · 中国 — the 기본 정보 観光 spots (ADR 0011, #93).
// Look-alikes drawn from memory in the mascot likenesses' hand — not photos, not official art.
import { C, INK, N, O, T, ground, line, water } from './helpers';

type P = [number, number];
const r1 = (n: number) => Math.round(n * 10) / 10;

/** A Japanese cedar (杉): a straight trunk under a tall, narrow dark-green crown. */
const cedar = (x: number, top: number, w: number, foot = 84) =>
  `<rect x="${x - 2.6}" y="${top + 30}" width="5.2" height="${foot - top - 30}" fill="${C.dwood}" ${T}/>` +
  `<path d="M${x} ${top} Q${x + w * 0.3} ${top + 12} ${x + w / 2} ${top + 36} Q${x + w * 0.2} ${top + 42} ${x} ${top + 41} Q${x - w * 0.2} ${top + 42} ${x - w / 2} ${top + 36} Q${x - w * 0.3} ${top + 12} ${x} ${top} Z" fill="#3f7a52" ${O}/>`;

/** A bamboo stalk bending from (x0,y0) over (cx,cy) to (x1,y1), outlined, with node lines across it. */
function stalk(x0: number, y0: number, cx: number, cy: number, x1: number, y1: number, color: string, w = 6): string {
  const k = w / 2 + 1.4;
  const node = (t: number) => {
    const u = 1 - t;
    const px = u * u * x0 + 2 * t * u * cx + t * t * x1, py = u * u * y0 + 2 * t * u * cy + t * t * y1;
    const dx = 2 * u * (cx - x0) + 2 * t * (x1 - cx), dy = 2 * u * (cy - y0) + 2 * t * (y1 - cy), l = Math.hypot(dx, dy);
    return `M${r1(px + (dy / l) * k)} ${r1(py - (dx / l) * k)} L${r1(px - (dy / l) * k)} ${r1(py + (dx / l) * k)}`;
  };
  return (
    line(`M${x0} ${y0} Q${cx} ${cy} ${x1} ${y1}`, color, w) +
    `<path d="${[0.2, 0.4, 0.6, 0.8].map(node).join(' ')}" ${N} stroke="${INK}" stroke-width="2.2" stroke-linecap="round"/>`
  );
}

/** A pointed leaf `len` long starting at (x,y), turned `a` degrees. */
const leaf = (x: number, y: number, a: number, color: string, len = 13) =>
  `<path d="M0 0 Q${len / 2} ${r1(-len * 0.28)} ${len} 0 Q${len / 2} ${r1(len * 0.28)} 0 0 Z" transform="translate(${x} ${y}) rotate(${a})" fill="${color}" ${T}/>`;

/** 海鼠壁 (namako): dark tiles under a white diagonal grid, the lines cut to the box by hand. */
function namako(x: number, y: number, w: number, h: number, step = 6): string {
  let d = '';
  for (let c = -h + step / 2; c < w; c += step) {
    const s0 = Math.max(0, -c), s1 = Math.min(h, w - c);
    if (s1 > s0) d += `M${r1(x + c + s0)} ${r1(y + s0)} L${r1(x + c + s1)} ${r1(y + s1)} `;
  }
  for (let c = step / 2; c < w + h; c += step) {
    const s0 = Math.max(0, c - w), s1 = Math.min(h, c);
    if (s1 > s0) d += `M${r1(x + c - s0)} ${r1(y + s0)} L${r1(x + c - s1)} ${r1(y + s1)} `;
  }
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#5d6068"/><path d="${d.trim()}" ${N} stroke="${C.white}" stroke-width="2"/><rect x="${x}" y="${y}" width="${w}" height="${h}" ${N} ${T}/>`;
}

/** A 千鳥破風: the white triangular gable standing on a roof, base `w` wide at `y`, `h` tall. */
const gable = (x: number, y: number, w: number, h: number) =>
  `<path d="M${x - w / 2} ${y} L${x} ${y - h} L${x + w / 2} ${y} Z" fill="${C.white}" ${O}/>`;

/** A small torii for the 元乃隅 line: two posts under the kasagi. */
const miniTorii = ([x, y]: P, w = 11) =>
  line(`M${r1(x - w * 0.3)} ${y + 1} V${r1(y + w * 0.95)} M${r1(x + w * 0.3)} ${y + 1} V${r1(y + w * 0.95)}`, C.red, 2.6) +
  line(`M${r1(x - w / 2)} ${y} H${r1(x + w / 2)}`, C.red, 3);

/** One rimstone pool of 百枚皿: a round rim holding a disc of blue water. */
const pool = (x: number, y: number, w: number) =>
  `<path d="M${x - w / 2} ${y} A${w / 2} 6.5 0 0 0 ${x + w / 2} ${y} Z" fill="#e8d5b0" ${T}/><ellipse cx="${x}" cy="${y}" rx="${w / 2 - 1.4}" ry="3.2" fill="${C.water}" ${T}/>`;

/** The cubic segment of a round hump ending at (b,y), from x `a` at the same height, rising `rise` — a half-sine,
 * so the top is round and the feet are not too steep. Works right-to-left too. */
const hump = (a: number, b: number, y: number, rise: number) => {
  const k = (b - a) * 0.4244, h = r1(y - rise * 1.333);
  return `C${r1(a + k)} ${h} ${r1(b - k)} ${h} ${b} ${y}`;
};
/** 錦帯橋's five arches [from, to, rise]: two low end spans, three high ones; the deck runs flat over each pier. */
const SPANS: [number, number, number][] = [[6, 16, 5], [21, 37, 10], [42, 58, 10], [63, 79, 10], [84, 94, 5]];
const PIERS = [18.5, 39.5, 60.5, 81.5];
/** The line along the whole bridge at height `y` — humps over the spans (each `drop` lower, or dipping when `dir` is
 * -1, for the reflection), flat over the piers; `back` runs it right-to-left to close the wooden band. */
function kintai(y: number, drop = 0, back = false, dir = 1): string {
  const s = back ? [...SPANS].reverse() : SPANS;
  return s
    .map(([a, b, h], i) => {
      const [p, q] = back ? [b, a] : [a, b];
      return `${i ? 'L' : 'M'}${p} ${y} ${hump(p, q, y, (h - drop) * dir)}`;
    })
    .join(' ');
}

const HIMEJI = '#bcc4ca'; // 姫路城's pale grey tiles

export const artE: Record<string, string> = {
  // ジブリパーク — an old Showa house with an orange-red roof under a huge camphor tree (just a house in the woods)
  moriie: `
    ${ground(78)}
    <path d="M24 86 Q27 70 26 54 H34 Q34 70 38 86 Z" fill="#9a7358" ${O}/>
    <path d="M10 46 Q2 34 12 26 Q12 12 28 12 Q36 2 50 8 Q64 6 66 20 Q76 26 70 38 Q70 50 56 50 Q48 58 36 54 Q24 60 16 54 Q8 54 10 46 Z" fill="${C.dgreen}" ${O}/>
    <path d="M16 34 Q18 24 28 24 M38 16 Q46 12 54 16 M52 36 Q58 32 64 36 M22 46 Q28 42 34 46" ${N} stroke="${C.green}" stroke-width="3" stroke-linecap="round"/>
    <circle cx="86" cy="60" r="8" fill="${C.green}" ${O}/>
    <rect x="48" y="58" width="38" height="24" fill="${C.cream}" ${O}/>
    <path d="M49 66 H85 M49 74 H85" ${N} stroke="#d9cbb0" stroke-width="2"/>
    <path d="M42 60 L67 36 L92 60 Z" fill="${C.verm}" ${O}/>
    <circle cx="67" cy="50" r="3" fill="${C.white}" ${T}/>
    <rect x="54" y="64" width="11" height="12" fill="${C.sky}" ${T}/>
    <path d="M59.5 64 V76 M54 70 H65" stroke="${C.white}" stroke-width="2"/>
    <rect x="71" y="66" width="9" height="16" fill="${C.wood}" ${T}/>`,
  // 鳥羽水族館 — a chubby dugong (ジュゴン): the big round snout, little flippers, the whale-like fluke, bubbles
  jugon: `
    <circle cx="50" cy="50" r="41" fill="${C.sea}" ${O}/>
    ${line('M24 88 Q20 80 24 72 M32 90 Q34 82 30 76 M68 90 Q66 82 70 76 M76 88 Q80 80 76 72', C.green, 3)}
    <path d="M73 50 Q80 44 84 36 Q90 31 92 38 Q92 46 86 51 Q92 56 92 64 Q90 71 84 66 Q80 58 73 56 Z" fill="#aab1b8" ${O}/>
    <path d="M20 40 Q30 25 50 26 Q68 27 76 42 Q79 47 81 51 Q77 55 72 56 Q60 71 40 71 Q24 71 18 60 Z" fill="#aab1b8" ${O}/>
    <path d="M32 64 Q48 70 64 60" ${N} stroke="#cdd3d8" stroke-width="3" stroke-linecap="round"/>
    <path d="M47 64 Q42 76 52 79 Q58 73 56 64 Z" fill="#aab1b8" ${T}/>
    <path d="M8 57 Q7 45 19 43 Q31 43 32 54 Q32 66 21 67 Q9 68 8 57 Z" fill="#c9cfd4" ${O}/>
    <path d="M13 62 Q20 65 27 61" ${N} ${T}/>
    <circle cx="15" cy="50" r="1.4" fill="${INK}"/><circle cx="21" cy="49" r="1.4" fill="${INK}"/>
    <circle cx="33" cy="40" r="2.8" fill="${INK}"/><circle cx="32.1" cy="39.1" r="1" fill="#fff"/>
    <ellipse cx="38" cy="48" rx="3.6" ry="2.2" fill="#f5a3b3" opacity=".8"/>
    <circle cx="24" cy="24" r="4.4" ${N} stroke="${C.white}" stroke-width="2.6"/><circle cx="33" cy="15" r="2.8" ${N} stroke="${C.white}" stroke-width="2.4"/><circle cx="62" cy="17" r="3" ${N} stroke="${C.white}" stroke-width="2.4"/>`,
  // 熊野古道 — the mossy stone steps winding up between tall straight cedars
  kodo: `
    ${ground(78, '#7fae6a')}
    ${cedar(14, 5, 16, 86)}${cedar(86, 5, 16, 86)}${cedar(28, 14, 15, 82)}${cedar(72, 14, 15, 82)}
    <path d="M28 92 Q39 80 39.5 74 Q40 68 39.5 62 Q39 56 42 51 L45 45 H54 L53 51 Q53 56 56.5 62 Q60 68 64.5 74 Q69 80 72 92 Z" fill="${C.stone}" ${O}/>
    <path d="M35 86 H67 M41 80 H66 M42 74 H62 M42 68 H58 M42 62 H55 M42 56.5 H52.5 M44 51 H52" ${N} ${T}/>
    <path d="M31 90 q4 -4 8 -2 M61 78 q3 -3 6 0 M41 65 q2 -3 5 -1 M52 60 q2 -2 4 0" ${N} stroke="#6f9e5a" stroke-width="3" stroke-linecap="round"/>`,
  // 琵琶湖 — the wide calm lake, a white sailboat, far hills
  lake: `
    <path d="M8 60 Q18 40 32 46 Q44 30 60 42 Q74 34 92 58 Z" fill="#9dbfd8" ${O}/>
    <path d="M58 60 Q68 46 80 48 Q88 52 92 60 Z" fill="${C.green}" ${O}/>
    <path d="M8 58 Q50 50 92 58 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <path d="M16 66 h12 M68 64 h12 M20 80 h14 M58 82 h16 M72 72 h10" stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M48 70 V22" ${N} ${O}/>
    <path d="M46 26 V64 H24 Z" fill="${C.white}" ${O}/>
    <path d="M51 32 V64 H66 Z" fill="${C.white}" ${O}/>
    <path d="M28 68 H70 L64 77 H34 Z" fill="${C.white}" ${O}/>
    <path d="M32 72.5 H66" stroke="#3f6fb5" stroke-width="2.6"/>
    <path d="M48 22 l9 3 -9 3 Z" fill="${C.red}" ${T}/>`,
  // 嵐山の竹林 — tall bamboo on both sides of the path, bending in overhead like a tunnel
  chikurin: `
    <path d="M36 92 L46 48 H54 L64 92 Z" fill="#e8dcc2" ${T}/>
    ${stalk(10, 92, 10, 38, 34, 10, '#9fd08a')}${stalk(20, 92, 22, 42, 42, 14, '#6fae70')}${stalk(32, 92, 35, 52, 47, 24, '#9fd08a', 5)}
    ${stalk(90, 92, 90, 38, 66, 10, '#9fd08a')}${stalk(80, 92, 78, 42, 58, 14, '#6fae70')}${stalk(68, 92, 65, 52, 53, 24, '#9fd08a', 5)}
    ${leaf(34, 10, 165, C.dgreen, 15)}${leaf(34, 10, 195, C.green, 13)}${leaf(42, 14, 125, C.green)}${leaf(47, 24, 100, C.dgreen, 11)}
    ${leaf(66, 10, 15, C.dgreen, 15)}${leaf(66, 10, -15, C.green, 13)}${leaf(58, 14, 55, C.green)}${leaf(53, 24, 80, C.dgreen, 11)}
    ${leaf(50, 14, -55, C.dgreen, 10)}${leaf(50, 14, 235, C.green, 10)}`,
  // 姫路城 — the white heron castle: a tall white keep, white triangular gables on pale grey tiles
  himejijo: `
    <path d="M16 92 L24 80 H76 L84 92 Z" fill="${C.stone}" ${O}/>
    <path d="M30 86 h12 M50 88 h14 M58 84 h8" ${N} ${T}/>
    <rect x="26" y="64" width="48" height="16" fill="${C.white}" ${O}/>
    <path d="M34 72 h4 M48 72 h4 M62 72 h4" stroke="${INK}" stroke-width="2.8" stroke-linecap="round"/>
    <path d="M14 66 Q18 62 23 61 L28 57 H72 L77 61 Q82 62 86 66 Z" fill="${HIMEJI}" ${O}/>
    <rect x="31" y="46" width="38" height="11" fill="${C.white}" ${O}/>
    ${gable(36, 61, 14, 9)}${gable(64, 61, 14, 9)}
    <path d="M19 48 Q23 44 28 43 L33 40 H67 L72 43 Q77 44 81 48 Z" fill="${HIMEJI}" ${O}/>
    <rect x="35" y="30" width="30" height="10" fill="${C.white}" ${O}/>
    ${gable(50, 44, 24, 11)}
    <path d="M25 32 Q29 28 33 27 L37 24 H63 L67 27 Q71 28 75 32 Z" fill="${HIMEJI}" ${O}/>
    <rect x="39" y="15" width="22" height="9" fill="${C.white}" ${O}/>
    <path d="M42 28 Q50 19 58 28 Z" fill="${C.white}" ${O}/>
    <path d="M30 16 Q33 12 37 11 L41 8 H59 L63 11 Q67 12 70 16 Z" fill="${HIMEJI}" ${O}/>
    ${gable(50, 13, 13, 7)}`,
  // 神戸ポートタワー — the red hourglass lattice tower by the harbour
  porttower: `
    ${water(76)}
    <rect x="24" y="72" width="52" height="9" rx="2" fill="${C.stone}" ${O}/>
    <path d="M31 74 Q45 62 45 48 Q45 34 37 22 H63 Q55 34 55 48 Q55 62 69 74 Z" fill="${C.red}" ${O}/>
    <path d="M36 70 L60 26 M64 70 L40 26 M38 62 H62 M44 36 H56" ${N} stroke="#f7b3a8" stroke-width="2"/>
    <rect x="33" y="14" width="34" height="10" rx="3" fill="${C.white}" ${O}/>
    <path d="M38 19 H62" stroke="${C.sea}" stroke-width="3.4" stroke-linecap="round"/>
    <rect x="43" y="8" width="14" height="6" rx="2" fill="${C.white}" ${O}/>
    <path d="M50 8 V5" ${N} ${O}/>`,
  // 竹田城跡 — the bare stone walls stepping up the hilltop above a sea of clouds, morning sun
  unkai: `
    <circle cx="50" cy="50" r="40" fill="#bfe0f2" ${O}/>
    <circle cx="72" cy="25" r="6" fill="${C.gold}" ${T}/>
    <path d="M12 58 Q18 48 26 54 L30 58 Z" fill="#9dbfd8" ${T}/>
    <path d="M14 62 Q26 48 36 45 H64 Q74 48 86 62 Z" fill="${C.dgreen}" ${O}/>
    <path d="M18 54 Q24 51 25 46 H75 Q76 51 82 54 Z" fill="${C.stone}" ${O}/>
    <path d="M25 46 Q29 44 29 39 H49 Q49 44 52 46 Z" fill="${C.stone}" ${O}/>
    <path d="M56 46 Q59 44 59 41 H70 Q70 44 73 46 Z" fill="${C.stone}" ${O}/>
    <path d="M32 39 Q35 37 35 32 H45 Q45 37 48 39 Z" fill="${C.stone}" ${O}/>
    <path d="M26 50 H74 M31 42.5 H47 M34 46 V50 M48 46 V50 M62 46 V50 M40 39 V42.5" ${N} stroke="#a39a90" stroke-width="2"/>
    <circle cx="64" cy="37.5" r="3.6" fill="${C.green}" ${T}/><circle cx="80" cy="49" r="3.4" fill="${C.green}" ${T}/>
    <path d="M10.8 58 Q16 50 24 55 Q30 48 40 53 Q48 47 56 53 Q64 47 72 53 Q80 49 89.2 58 A40 40 0 0 1 10.8 58 Z" fill="${C.white}" ${O}/>
    <path d="M22 72 q8 -5 16 0 q8 -5 16 0 M52 82 q8 -5 16 0" ${N} stroke="#cfe3ee" stroke-width="2.6" stroke-linecap="round"/>`,
  // 東大寺 — the 大仏殿: a very wide dark roof, golden shibi on the ridge, the golden window in the middle
  todaiji: `
    <path d="M10 86 H90 L94 92 H6 Z" fill="${C.stone}" ${O}/>
    <rect x="14" y="60" width="72" height="26" fill="${C.white}" ${O}/>
    ${[20, 30, 70, 80].map((x) => `<rect x="${x - 1.8}" y="61.5" width="3.6" height="23" fill="${C.wood}"/>`).join('')}
    <rect x="40" y="64" width="20" height="22" fill="${C.dwood}" ${T}/>
    <path d="M50 64 V86" ${N} ${T}/>
    <path d="M6 62 Q12 58 18 56 L24 50 H76 L82 56 Q88 58 94 62 Z" fill="${C.roof}" ${O}/>
    <rect x="22" y="36" width="56" height="14" fill="${C.white}" ${O}/>
    ${[28, 36, 64, 72].map((x) => `<rect x="${x - 1.6}" y="37.5" width="3.2" height="11" fill="${C.wood}"/>`).join('')}
    <rect x="41" y="38" width="18" height="10" fill="${C.gold}" ${T}/>
    <path d="M47 38 V48 M53 38 V48" ${N} stroke="#c9a032" stroke-width="2"/>
    <path d="M6 38 Q14 34 22 32 L30 20 H70 L78 32 Q86 34 94 38 Z" fill="${C.roof}" ${O}/>
    <path d="M27 21 Q22 10 32 4 Q31 14 36 21 Z" fill="${C.gold}" ${T}/>
    <path d="M73 21 Q78 10 68 4 Q69 14 64 21 Z" fill="${C.gold}" ${T}/>`,
  // 高野山 根本大塔 — the vermilion 多宝塔: square roofs, the white dome between, the gold-ringed spire
  daito: `
    <path d="M18 92 L22 86 H78 L82 92 Z" fill="${C.stone}" ${O}/>
    <rect x="26" y="64" width="48" height="22" fill="${C.verm}" ${O}/>
    <path d="M36 64 V86 M64 64 V86" ${N} ${T}/>
    <rect x="44" y="70" width="12" height="16" fill="#b8392f" ${T}/>
    <path d="M8 66 Q16 61 24 59 L30 53 H70 L76 59 Q84 61 92 66 Z" fill="${C.roof}" ${O}/>
    <path d="M32 54 Q32 42 50 40 Q68 42 68 54 Z" fill="${C.white}" ${O}/>
    <rect x="40" y="30" width="20" height="11" fill="${C.verm}" ${O}/>
    <path d="M14 32 Q22 28 28 26 L35 20 H65 L72 26 Q78 28 86 32 Z" fill="${C.roof}" ${O}/>
    <rect x="47.5" y="8" width="5" height="13" fill="${C.gold}" ${T}/>
    <rect x="44" y="10" width="12" height="2.6" rx="1" fill="${C.gold}" ${T}/><rect x="44" y="15" width="12" height="2.6" rx="1" fill="${C.gold}" ${T}/>
    <circle cx="50" cy="7" r="2.8" fill="${C.gold}" ${T}/>`,
  // 白浜 — white sand, a turquoise-to-blue sea with a wave, a striped parasol and a palm
  beach: `
    <path d="M8 38 Q50 30 92 38 L92 64 H8 Z" fill="${C.sea}" ${O}/>
    <path d="M9.7 51 Q50 45 90.3 51 L90.3 63 H9.7 Z" fill="#7fd6c9"/>
    <path d="M58 48 q8 -8 16 0 q-6 -3 -8 3" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M6 64 Q50 56 94 64 L92 84 Q50 94 8 84 Z" fill="#fbf1dc" ${O}/>
    ${line('M22 84 Q16 60 26 35', '#b08858', 4.4)}
    ${leaf(26, 35, 188, C.green, 18)}${leaf(26, 35, 225, C.green, 17)}${leaf(26, 35, -30, C.green, 19)}${leaf(26, 35, 10, C.green, 18)}${leaf(26, 35, -80, C.dgreen, 13)}
    ${line('M66 86 L60 36', C.white, 2.4)}
    <path d="M60 22 Q40 24 36 44 Q42 40 48 44 Z" fill="${C.red}" ${O}/>
    <path d="M60 22 Q52 30 48 44 Q54 40 60 44 Z" fill="${C.white}" ${O}/>
    <path d="M60 22 Q66 30 70 44 Q64 40 60 44 Z" fill="${C.gold}" ${O}/>
    <path d="M60 22 Q80 24 82 44 Q76 40 70 44 Z" fill="#8fc3ea" ${O}/>`,
  // 水木しげるロード — a kasa-obake (the old one-eyed umbrella yokai) hopping on one leg, tongue out
  yokai: `
    <ellipse cx="52" cy="91" rx="16" ry="3.4" fill="#cfc3ad" opacity=".7"/>
    <g transform="translate(0 2.5) rotate(-10 50 50)">
      ${line('M50 60 V78', '#e8cfae', 4)}
      <path d="M40 80 H60 V84 H40 Z" fill="${C.wood}" ${O}/>
      <path d="M43 85 v4 M57 85 v4" stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/>
      <path d="M50 8 Q56 22 74 50 Q82 58 76 62 Q70 58 64 62 Q57 57 50 62 Q43 57 36 62 Q30 58 24 62 Q18 58 26 50 Q44 22 50 8 Z" fill="#b59ad8" ${O}/>
      <path d="M50 12 Q45 38 36 60 M50 12 Q55 38 64 60" ${N} stroke="#8e74b8" stroke-width="2"/>
      <path d="M48 9 L50 3 L52 9 Z" fill="${C.wood}" ${T}/>
      <ellipse cx="50" cy="32" rx="9" ry="10" fill="${C.white}" ${O}/>
      <circle cx="51" cy="34" r="4.6" fill="${INK}"/><circle cx="49.4" cy="32" r="1.6" fill="#fff"/>
      <path d="M46.5 49 Q45 63 52 68 Q59 64 55.5 49 Z" fill="#f28a9a" ${T}/>
      <path d="M43 48 Q50 52 57 48" ${N} ${T}/>
    </g>`,
  // 大山 — 伯耆富士 from the side: green slopes, the grey-brown rocky top, snow on a jagged ridge, woods at the foot
  yama: `
    <path d="M6 78 Q14 66 22 54 L32 32 L38 22 L43 26 L48 19 L54 28 L60 25 L66 34 L72 31 L78 42 Q86 56 94 70 V78 Z" fill="${C.green}" ${O}/>
    <path d="M25 48 L32 32 L38 22 L43 26 L48 19 L54 28 L60 25 L66 34 L72 31 L78 42 L81 47 Q74 52 66 47 Q58 53 50 47 Q42 53 34 47 Q30 50 25 48 Z" fill="#a08c80" ${T}/>
    <path d="M40 38 v6 M52 36 v8 M62 38 v6 M72 40 v5" ${N} stroke="#86736a" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M34 28 L38 22 L43 26 L48 19 L54 28 L60 25 L63 29 L59 31 L55 33 L51 30 L47 33 L43 30 L39 32 Z" fill="${C.white}" ${T}/>
    <path d="M8 76 Q8 69 14 69 Q17 63 23 66 Q27 61 33 65 Q37 61 43 65 Q47 61 53 65 Q57 61 63 65 Q67 61 73 65 Q77 61 83 66 Q90 64 91 71 Q94 82 84 86 Q50 94 16 86 Q6 82 8 76 Z" fill="${C.dgreen}" ${O}/>
    <path d="M20 76 q5 -4 10 0 M46 78 q5 -4 10 0 M70 76 q5 -4 10 0" ${N} stroke="${C.green}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 石見銀山 — a 間歩 mine mouth framed in timber in the green hill, a paper lantern, silver sparkling stones
  kozan: `
    <path d="M6 88 Q6 46 30 32 Q50 20 72 26 Q94 34 94 88 Z" fill="${C.green}" ${O}/>
    <path d="M16 52 q6 -8 14 -4 M60 30 q8 -6 16 0" ${N} stroke="${C.dgreen}" stroke-width="3" stroke-linecap="round"/>
    <path d="M36 86 V58 Q36 50 50 50 Q64 50 64 58 V86 Z" fill="#3f3a3a" ${O}/>
    <rect x="28" y="46" width="8" height="40" fill="${C.wood}" ${O}/>
    <rect x="64" y="46" width="8" height="40" fill="${C.wood}" ${O}/>
    <rect x="22" y="40" width="56" height="8" rx="1.5" fill="${C.wood}" ${O}/>
    <path d="M82 48 V51" ${N} ${T}/>
    <ellipse cx="82" cy="59" rx="6.4" ry="7.6" fill="#fbe39a" ${O}/>
    <path d="M76.4 56 H87.6 M76.2 62 H87.8" ${N} stroke="#e0a64b" stroke-width="2"/>
    <rect x="78" y="50" width="8" height="3" rx="1" fill="${INK}"/><rect x="78" y="65.6" width="8" height="3" rx="1" fill="${INK}"/>
    <path d="M40 86 Q42 78 50 79 Q56 80 58 86 Z" fill="#c9ced6" ${T}/>
    <path d="M12 86 Q14 80 20 80 Q24 82 24 86 Z" fill="#c9ced6" ${T}/>
    <path d="M48 67 l1.4 3.6 3.6 1.4 -3.6 1.4 -1.4 3.6 -1.4 -3.6 -3.6 -1.4 3.6 -1.4 Z M18 71 l1.2 3 3 1.2 -3 1.2 -1.2 3 -1.2 -3 -3 -1.2 3 -1.2 Z" fill="${C.white}" ${T}/>`,
  // 日本庭園 (足立美術館 · 後楽園 · 栗林公園) — a pond, a little arched bridge, a pruned pine, a stone lantern, raked gravel
  teien: `
    ${ground(72, '#efe6d4')}
    <path d="M14 80 q8 -3 16 0 M62 90 q8 -3 16 0 M16 88 q8 -3 16 0" ${N} stroke="#cfc3ad" stroke-width="2.2"/>
    <path d="M30 80 Q32 70 50 70 Q70 68 80 76 Q84 86 66 88 Q46 92 34 88 Q28 86 30 80 Z" fill="${C.water}" ${O}/>
    ${line('M34 80 Q56 58 78 80', C.red, 4.4)}
    <path d="M42 73 V67 M56 69 V63 M70 73 V67" ${N} ${T}/>
    ${line('M40 68 Q56 54 72 68', C.red, 2.2)}
    ${line('M24 78 Q16 62 24 50 Q32 40 26 28', '#9a7358', 5)}
    <path d="M8 34 Q10 24 24 24 Q38 22 42 30 Q40 36 26 36 Q10 38 8 34 Z" fill="${C.dgreen}" ${O}/>
    <path d="M22 48 Q24 40 36 40 Q48 40 48 46 Q46 52 34 52 Q22 54 22 48 Z" fill="${C.dgreen}" ${O}/>
    <path d="M8 56 Q10 48 20 48 Q28 50 28 54 Q26 60 16 60 Q8 60 8 56 Z" fill="${C.dgreen}" ${O}/>
    <rect x="76" y="72" width="12" height="4" fill="${C.stone}" ${T}/>
    <rect x="79" y="60" width="6" height="12" fill="${C.stone}" ${O}/>
    <rect x="76" y="50" width="12" height="10" fill="${C.stone}" ${O}/>
    <rect x="79" y="53" width="6" height="4" fill="${C.gold}"/>
    <path d="M70 51 Q82 40 94 51 Z" fill="${C.stone}" ${O}/>
    <circle cx="82" cy="42" r="2.6" fill="${C.stone}" ${T}/>`,
  // 倉敷美観地区 — white storehouses with namako walls along the canal, a weeping willow, a boat
  kurashiki: `
    ${water(74)}
    <rect x="36" y="42" width="26" height="32" fill="${C.white}" ${O}/>
    ${namako(36, 58, 26, 16)}
    <rect x="44" y="46" width="10" height="7" fill="${INK}"/>
    <path d="M32 44 L49 24 L66 44 Z" fill="${C.roof}" ${O}/>
    <rect x="64" y="48" width="26" height="26" fill="${C.white}" ${O}/>
    ${namako(64, 60, 26, 14)}
    <path d="M60 50 L66 40 H88 L94 50 Z" fill="${C.roof}" ${O}/>
    <rect x="72" y="51" width="10" height="5" fill="${INK}"/>
    ${line('M20 78 Q22 58 18 36', '#9a7358', 4)}
    <path d="M6 30 Q10 16 22 16 Q34 16 36 28 Q30 30 22 28 Q12 30 6 30 Z" fill="${C.green}" ${O}/>
    ${line('M10 30 Q6 42 8 56 M16 30 Q14 44 16 62 M26 30 Q26 44 28 58 M33 29 Q36 38 36 50', C.green, 3.4)}
    <path d="M44 80 H74 L68 86 H50 Z" fill="${C.wood}" ${O}/>`,
  // 瀬戸大橋 · しまなみ海道 — a suspension bridge: two towers, the sweeping cable and hangers, green islands
  bridge: `
    <path d="M6 60 Q50 52 94 60 L92 84 Q50 94 8 84 Z" fill="${C.sea}" ${O}/>
    <path d="M6 62 Q10 46 24 49 Q34 52 36 62 Z" fill="${C.green}" ${O}/>
    <path d="M62 62 Q70 47 84 49 Q94 52 94 62 Z" fill="${C.green}" ${O}/>
    <path d="M40 84 Q46 76 54 78 Q60 80 60 84 Z" fill="${C.green}" ${T}/>
    <path d="M18 76 q6 -3 12 0 M66 78 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    <rect x="22" y="12" width="9" height="66" rx="1.5" fill="${C.white}" ${O}/><rect x="69" y="12" width="9" height="66" rx="1.5" fill="${C.white}" ${O}/>
    <path d="M22 26 h9 M22 42 h9 M69 26 h9 M69 42 h9" ${N} ${T}/>
    ${[35, 42, 50, 58, 65].map((x) => { const t = (x - 26.5) / 47; const y = (1 - t) * (1 - t) * 14 + 2 * t * (1 - t) * 84 + t * t * 14; return `<path d="M${x} ${r1(y + 1)} V58" ${N} stroke="${INK}" stroke-width="2.2"/>`; }).join('')}
    ${line('M7 56 L26.5 14 Q50 84 73.5 14 L93 56', C.steel, 2.4)}
    <rect x="6" y="58" width="88" height="8" fill="${C.white}" ${O}/>
    <path d="M8 64.6 L13 59.4 L18 64.6 L23 59.4 L28 64.6 L33 59.4 L38 64.6 L43 59.4 L48 64.6 L53 59.4 L58 64.6 L63 59.4 L68 64.6 L73 59.4 L78 64.6 L83 59.4 L88 64.6 L92 60" ${N} stroke="${C.stone}" stroke-width="2"/>`,
  // 尾道 — the hillside town: steep stone steps, little houses, the pagoda on top, a cat sitting on the steps
  sakamachi: `
    <path d="M6 90 V54 Q24 42 42 38 Q64 32 78 20 Q88 12 94 14 V90 Z" fill="${C.green}" ${O}/>
    <rect x="74" y="30" width="12" height="7" fill="${C.dwood}" ${O}/><path d="M68 31 L73 26 H87 L92 31 Z" fill="${C.roof}" ${O}/>
    <rect x="75.5" y="21" width="9" height="5" fill="${C.dwood}" ${O}/><path d="M70 22 L75 17 H85 L90 22 Z" fill="${C.roof}" ${O}/>
    <rect x="77" y="13" width="6" height="4" fill="${C.dwood}" ${O}/><path d="M72 13 L76 9 H84 L88 13 Z" fill="${C.roof}" ${O}/>
    <path d="M80 9 V5" ${N} ${O}/>
    <path d="M22 92 L62 40 H72 L38 92 Z" fill="${C.stone}" ${O}/>
    <path d="M28 85 H43 M33.5 78 H47.5 M39 71 H52 M44.5 64 H56.5 M50 57 H61 M55.5 50 H65.5 M60.5 44 H69.5" ${N} ${T}/>
    <rect x="8" y="62" width="20" height="14" fill="${C.cream}" ${O}/><path d="M6 64 L11.5 55 H25 L31 64 Z" fill="${C.brick}" ${O}/>
    <rect x="28" y="44" width="16" height="11" fill="${C.cream}" ${O}/><path d="M25 46 L30 39 H42 L47 46 Z" fill="${C.roof}" ${O}/>
    <rect x="66" y="58" width="22" height="14" fill="${C.cream}" ${O}/><path d="M63 60 L69 51 H85 L91 60 Z" fill="${C.roof}" ${O}/>
    ${line('M47 86 Q56 84 54 74', '#f3b36d', 3.2)}
    <path d="M30 89 Q29 77 34 73 H42 Q47 77 46 89 Z" fill="#f3b36d" ${O}/>
    <path d="M31 66 L32 57 L37 62 Z M45 66 L44 57 L39 62 Z" fill="#f3b36d" ${T}/>
    <circle cx="38" cy="67" r="7.6" fill="#f3b36d" ${O}/>
    <circle cx="35.2" cy="67" r="1.4" fill="${INK}"/><circle cx="40.8" cy="67" r="1.4" fill="${INK}"/>
    <path d="M37 70 h2" stroke="#e5708d" stroke-width="2" stroke-linecap="round"/>
    <path d="M34 80 v8 M42 80 v8" ${N} stroke="#d99450" stroke-width="2"/>`,
  // 角島大橋 · 古宇利島 — the long low straight bridge over emerald sea to a small green island
  emerald: `
    <path d="M6 36 Q50 26 94 36 V82 Q50 96 6 82 Z" fill="#35bfb8" ${O}/>
    <path d="M7.7 37.6 Q50 28 92.3 37.6 V46 Q50 39 7.7 47 Z" fill="#3f8fd0"/>
    <path d="M58 41 Q62 22 76 21 Q90 22 92 40 Z" fill="${C.green}" ${O}/>
    <path d="M54 42 Q74 36 93 41 L92.3 45 Q74 41 57 46 Z" fill="#fbf1dc" ${T}/>
    <path d="M22 56 q10 -4 20 0 M52 74 q10 -4 20 0 M72 56 q6 -3 12 0" ${N} stroke="#a8ece4" stroke-width="2.6" stroke-linecap="round"/>
    ${[0.2, 0.36, 0.52, 0.68, 0.84].map((t) => { const x = 10.5 + (60.7 - 10.5) * t, y = 81.8 + (45 - 81.8) * t; return `<path d="M${r1(x)} ${r1(y)} v${r1(7 - 4.5 * t)}" ${N} stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>`; }).join('')}
    <path d="M5.5 74.2 L59.3 43 L60.7 45 L10.5 81.8 Z" fill="#f3efe8" ${O}/>`,
  // 錦帯橋 — five humped wooden arches in a row on grey stone piers over the clear river
  kintaikyo: `
    <path d="M6 58 Q50 52 94 58 L92 84 Q50 94 8 84 Z" fill="#8fd0e8" ${O}/>
    <path d="${kintai(62, 4, false, -1)}" ${N} stroke="#6fb6d8" stroke-width="3" stroke-linecap="round"/>
    ${PIERS.map((x) => `<path d="M${r1(x - 6)} 65 L${r1(x - 4.5)} 51 H${r1(x + 4.5)} L${r1(x + 6)} 65 Z" fill="${C.stone}" ${O}/><path d="M${r1(x - 5)} 58.5 h10" ${N} stroke="#a39a90" stroke-width="2"/>`).join('')}
    <path d="${kintai(45)} L94 52.5 ${kintai(52.5, 1, true).replace(/^M/, 'L')} Z" fill="${C.wood}" ${O}/>
    <path d="${kintai(47.5, 0.2)}" ${N} stroke="#e8c49a" stroke-width="2.2"/>
    <path d="${kintai(50.3, 0.6)}" ${N} stroke="#9a7358" stroke-width="2"/>
    <path d="M16 78 q6 -3 12 0 M62 81 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 秋芳洞 — the limestone cave mouth, stalactites hanging from its roof, the terraced rimstone pools (百枚皿) below
  cave: `
    <path d="M6 90 V46 Q6 16 30 10 Q50 5 70 10 Q94 16 94 46 V90 Z" fill="#e2d2b4" ${O}/>
    <path d="M12 30 q6 -5 12 -2 M72 16 q7 -2 12 3 M88 56 v10 M11 62 v12" ${N} stroke="#c4ae8a" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M16 90 V56 Q17 44 22 38 L25 35 L28 47 L31 32 Q35 29 37 28.5 L40 44 L43 27.4 Q47 26 49 26 L52 38 L55 26 Q58 26.5 60 27 L62.5 49 L65 28.5 Q69 30 71 32 L73.5 44 L76 36 Q82 44 84 56 V90 Z" fill="#5d4a40" ${O}/>
    ${pool(39, 67, 22)}${pool(61, 67, 22)}
    ${pool(28, 80, 22)}${pool(50, 80, 22)}${pool(72, 80, 22)}`,
  // 元乃隅神社 — the long line of little red torii zig-zagging down the green cliff to the deep-blue sea
  motonosumi: `
    <path d="M6 76 V18 Q30 8 60 12 Q86 16 94 26 V70 Q70 80 40 78 Q20 78 6 76 Z" fill="${C.green}" ${O}/>
    ${water(74, '#3f7cc0')}
    <path d="M16 78 q4 -5 10 -2 M70 76 q5 -4 10 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    ${([[22, 16], [34, 19], [46, 22], [58, 25], [70, 28]] as P[]).map((p) => miniTorii(p)).join('')}
    ${([[72, 38], [60, 41], [48, 44], [36, 47], [24, 50]] as P[]).map((p) => miniTorii(p)).join('')}
    ${([[28, 58], [40, 61], [52, 64], [64, 67]] as P[]).map((p) => miniTorii(p)).join('')}`,
};

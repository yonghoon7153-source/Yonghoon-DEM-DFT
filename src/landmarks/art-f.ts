// Landmark stickers, 四国 · 九州 · 沖縄 — the 기본 정보 観光 spots (ADR 0011, #93).
// Look-alikes drawn from memory in the mascot likenesses' hand — not photos, not official art.
import { C, INK, N, O, T, ground, line, torii, water } from './helpers';

type P = [number, number];
type Curve = [P, P, P]; // a quadratic curve: start, control, end
/** One decimal is plenty on a 100×100 canvas. */
const f = (n: number) => Math.round(n * 10) / 10;
/** A point on the quadratic curve a → (b) → c at t. */
const qp = ([a, b, c]: Curve, t: number): P => {
  const u = 1 - t;
  return [u * u * a[0] + 2 * u * t * b[0] + t * t * c[0], u * u * a[1] + 2 * u * t * b[1] + t * t * c[1]];
};
/** The direction of that curve at t, in degrees (for `rotate`). */
const qa = ([a, b, c]: Curve, t: number) =>
  (Math.atan2(2 * (1 - t) * (b[1] - a[1]) + 2 * t * (c[1] - b[1]), 2 * (1 - t) * (b[0] - a[0]) + 2 * t * (c[0] - b[0])) * 180) / Math.PI;
/** Points turned around a centre (degrees, clockwise on screen). */
const turn = (ps: P[], deg: number, [cx, cy]: P): P[] => {
  const a = (deg * Math.PI) / 180, c = Math.cos(a), s = Math.sin(a);
  return ps.map(([x, y]) => [cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c]);
};
/** Points as a polygon `points` list. */
const pts = (ps: P[]) => ps.map(([x, y]) => `${f(x)},${f(y)}`).join(' ');

const AKA = '#e57b58'; // Okinawan red roof tiles (赤瓦), laid in white mortar
const SHU = '#d9432f'; // 首里城's vermilion lacquer
const BRONZE = '#5f7f6f'; // 龍馬像's dark green bronze
const CLAY = '#e39a5f'; // シーサー's fired red clay

/** A five-petal flower (plum blossom, hibiscus): round petals around a small heart. */
const flower = (x: number, y: number, r: number, fill: string, heart: string = C.gold) =>
  [0, 1, 2, 3, 4]
    .map((k) => {
      const a = ((-90 + k * 72) * Math.PI) / 180;
      return `<circle cx="${f(x + Math.cos(a) * r * 0.55)}" cy="${f(y + Math.sin(a) * r * 0.55)}" r="${f(r * 0.5)}" fill="${fill}" ${T}/>`;
    })
    .join('') + `<circle cx="${x}" cy="${y}" r="${f(r * 0.42)}" fill="${fill}"/><circle cx="${x}" cy="${y}" r="${f(r * 0.2)}" fill="${heart}"/>`;

/** A sunflower head: a ring of pointed petals and a brown middle. */
const sunflower = (x: number, y: number, r: number) =>
  `<polygon points="${pts(Array.from({ length: 20 }, (_, i): P => {
    const a = (i * Math.PI) / 10 - Math.PI / 2, rr = i % 2 ? r * 0.66 : r;
    return [x + Math.cos(a) * rr, y + Math.sin(a) * rr];
  }))}" fill="${C.gold}" ${T}/><circle cx="${x}" cy="${y}" r="${f(r * 0.45)}" fill="#9a6a3a"/>`;

/** A leaping dolphin facing right; (x, y) is the top-left of its ~66×50 box, s the scale. */
const dolphin = (x: number, y: number, s: number, body = '#8fb0cc') => {
  const p = (px: number, py: number) => `${f(x + px * s)} ${f(y + py * s)}`;
  const d = `M${p(8, 38)} Q${p(14, 10)} ${p(36, 9)} Q${p(52, 8)} ${p(58, 19)} Q${p(60, 22)} ${p(65, 23)} Q${p(67, 26)} ${p(62, 27)} Q${p(56, 28)} ${p(51, 26)} Q${p(40, 21)} ${p(29, 25)} Q${p(18, 30)} ${p(12, 40)} Z`;
  return (
    `<path d="M${p(9, 38)} L${p(0, 35)} Q${p(3, 43)} ${p(10, 42)} L${p(11, 50)} Q${p(16, 43)} ${p(12, 39)} Z" fill="${body}" ${T}/>` +
    `<path d="M${p(38, 10)} Q${p(31, 1)} ${p(24, 0)} Q${p(27, 6)} ${p(27, 13)} Z" fill="${body}" ${T}/>` +
    `<path d="${d}" fill="${body}"/>` +
    `<path d="M${p(52, 26)} Q${p(40, 20.5)} ${p(29, 24.5)} Q${p(18, 29.5)} ${p(12, 40)} Q${p(20, 27)} ${p(30, 21)} Q${p(42, 17)} ${p(54, 23)} Z" fill="${C.white}"/>` +
    `<path d="${d}" ${N} ${O}/>` +
    `<path d="M${p(46, 23)} Q${p(46, 31)} ${p(39, 33)} Q${p(41, 28)} ${p(40, 23)} Z" fill="${body}" ${T}/>` +
    `<circle cx="${f(x + 53 * s)}" cy="${f(y + 16 * s)}" r="${f(2.2 * s)}" fill="${INK}"/>` +
    `<ellipse cx="${f(x + 55 * s)}" cy="${f(y + 21.5 * s)}" rx="${f(2.6 * s)}" ry="${f(1.5 * s)}" fill="${C.pink}"/>`
  );
};

/** A moai: long face under a heavy brow, long nose, tight lips, ears down the sides. */
const moai = (x: number, top: number, w: number) => {
  const l = x - w / 2, r = x + w / 2;
  return (
    `<rect x="${l - 2.5}" y="${top + 12}" width="4.4" height="17" rx="2.2" fill="#998b7a" ${T}/>` +
    `<rect x="${r - 1.9}" y="${top + 12}" width="4.4" height="17" rx="2.2" fill="#998b7a" ${T}/>` +
    `<path d="M${l} 80 L${l + 1} ${top + 6} Q${l + 1} ${top} ${l + 7} ${top} H${r - 7} Q${r - 1} ${top} ${r - 1} ${top + 6} L${r} 80 Z" fill="#a89a88" ${O}/>` +
    `<rect x="${l + 2.5}" y="${top + 11}" width="${w - 5}" height="5" rx="2" fill="#6f6358"/>` +
    `<path d="M${l + 1.6} ${top + 10.5} H${r - 1.6}" ${N} stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/>` +
    `<path d="M${x} ${top + 13} L${x - 4} ${top + 28} Q${x} ${top + 30} ${x + 4} ${top + 28} Z" fill="#bcae9b" ${T}/>` +
    `<path d="M${x - 5} ${top + 34} H${x + 5}" ${N} ${T}/>` +
    `<path d="M${l + 3} ${top + 41} Q${x} ${top + 45} ${r - 3} ${top + 41}" ${N} ${T}/>`
  );
};

// かずら橋 — the sagging vine bridge: its handrail, the side ties and the gapped planks
const KZ_HAND: Curve = [[12, 24], [50, 58], [88, 24]];
const KZ_DECK: Curve = [[14, 40], [50, 70], [86, 40]];
const KZ_T = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9];
const kzTies = KZ_T.map((t) => {
  const [x1, y1] = qp(KZ_HAND, t), [x2, y2] = qp(KZ_DECK, t);
  return `M${f(x1)} ${f(y1)} L${f(x2)} ${f(y2 + 6)}`;
}).join(' ');
const kzPlanks = KZ_T.map((t) => {
  const [x, y] = qp(KZ_DECK, t);
  return `<rect x="${f(x - 2.6)}" y="${f(y - 1)}" width="5.2" height="9" rx="1" fill="${C.wood}" ${T} transform="rotate(${f(qa(KZ_DECK, t))} ${f(x)} ${f(y)})"/>`;
}).join('');

// 九重“夢”大吊橋 — hangers from the main cable down to the deck
const TB_CABLE: Curve = [[24.5, 23], [50, 50], [75.5, 23]];
const tbHangers = [0.15, 0.3, 0.5, 0.7, 0.85]
  .map((t) => {
    const [x, y] = qp(TB_CABLE, t);
    return `M${f(x)} ${f(y)} V44`;
  })
  .join(' ');

// ハウステンボス — one lattice sail, pointing up from the hub, then turned
const WM_HUB: P = [50, 36];
const sail = (deg: number) => {
  const box = turn([[44.5, 3], [55.5, 3], [55.5, 30], [44.5, 30]], deg, WM_HUB);
  const bars = [9, 15, 21, 27].map((y) => turn([[44.5, y], [55.5, y]], deg, WM_HUB));
  const stock = turn([[50, 3], [50, 32]], deg, WM_HUB);
  const seg = (a: P[]) => `M${a.map(([x, y]) => `${f(x)} ${f(y)}`).join(' L')}`;
  return `<polygon points="${pts(box)}" fill="${C.white}" ${O}/><path d="${[stock, ...bars].map(seg).join(' ')}" ${N} ${T}/>`;
};

// 青島 — the parallel ridges of the 鬼の洗濯板 on the rock shelf (chords of its ellipse)
const AO = { cx: 50, cy: 66, rx: 36, ry: 16 };
const AO_DX = Math.cos(Math.PI / 6), AO_DY = Math.sin(Math.PI / 6); // the ridges run at 30°
const aoRidges = [-24, -18, -12, -6, 0, 6, 12, 18, 24]
  .map((k) => {
    // the line through the centre shifted k along its normal; solve for where it meets the ellipse, keep 86 % of it
    const x0 = AO.cx - AO_DY * k, y0 = AO.cy + AO_DX * k;
    const a = (AO_DX / AO.rx) ** 2 + (AO_DY / AO.ry) ** 2;
    const b = 2 * (((x0 - AO.cx) * AO_DX) / AO.rx ** 2 + ((y0 - AO.cy) * AO_DY) / AO.ry ** 2);
    const c = ((x0 - AO.cx) / AO.rx) ** 2 + ((y0 - AO.cy) / AO.ry) ** 2 - 1;
    const disc = b * b - 4 * a * c;
    if (disc <= 0) return '';
    const t1 = ((-b - Math.sqrt(disc)) / (2 * a)) * 0.86, t2 = ((-b + Math.sqrt(disc)) / (2 * a)) * 0.86;
    return `M${f(x0 + AO_DX * t1)} ${f(y0 + AO_DY * t1)} L${f(x0 + AO_DX * t2)} ${f(y0 + AO_DY * t2)}`;
  })
  .join(' ');

/** A fan palm's crown (青島's ビロウ): leaves sprung from one point. */
const palm = (x: number, y: number) =>
  line(`M${x} ${y} q-6 -1 -10 3 M${x} ${y} q-5 -4 -8 -9 M${x} ${y} q0 -6 1 -10 M${x} ${y} q5 -4 8 -8 M${x} ${y} q6 -1 10 3`, C.dgreen, 3);

// 軍艦島 — small dark windows in a grid on each block
const grid = (x: number, y: number, cols: number, rows: number) =>
  Array.from({ length: rows }, (_, j) => Array.from({ length: cols }, (_, i) => `<rect x="${f(x + i * 4.6)}" y="${y + j * 5}" width="2.6" height="2.6" fill="${INK}"/>`).join('')).join('');

export const artF: Record<string, string> = {
  // 祖谷のかずら橋 — the sagging bridge of twisted vines, gapped planks, over the green gorge and its turquoise river
  kazurabashi: `
    <path d="M8 78 V38 Q8 30 15 30 Q19 23 27 26 Q33 25 35 33 Q39 56 50 78 Z" fill="${C.dgreen}" ${O}/>
    <path d="M92 78 V38 Q92 30 85 30 Q81 23 73 26 Q67 25 65 33 Q61 56 50 78 Z" fill="${C.dgreen}" ${O}/>
    <path d="M12 58 q4 -6 8 -2 q4 -3 6 2 Z M20 70 q4 -6 8 -2 q4 -3 6 2 Z M74 58 q4 -6 8 -2 q4 -3 6 2 Z M66 70 q4 -6 8 -2 q4 -3 6 2 Z" fill="${C.green}" ${T}/>
    ${water(72, '#5cc3bd')}
    <path d="${kzTies}" ${N} ${T}/>
    ${line('M14 40 Q50 70 86 40', '#8a6d5a', 2.6)}
    ${kzPlanks}
    ${line('M14 47 Q50 77 86 47', '#8a6d5a', 3.6)}
    ${line('M12 24 Q50 58 88 24', '#8a6d5a', 4)}
    <path d="M12 24 Q50 58 88 24 M14 47 Q50 77 86 47" ${N} stroke="#c4a27c" stroke-width="2.2" stroke-dasharray="3 3"/>`,
  // 大塚国際美術館 — a gold ornate frame on a wooden easel, sunflowers in a vase (a painting in general)
  gakubuchi: `
    ${line('M50 12 V86', C.dwood, 3.6)}
    ${line('M47 10 L22 90 M53 10 L78 90', C.wood, 4.6)}
    <rect x="12" y="66" width="76" height="7" rx="2" fill="${C.wood}" ${O}/>
    <path d="M40 16 Q41 7.5 50 7 Q59 7.5 60 16 Z" fill="${C.gold}" ${O}/>
    <path d="M45 14 L47 10 M50 14 V9.5 M55 14 L53 10" ${N} ${T}/>
    <rect x="16" y="14" width="68" height="52" rx="3" fill="${C.gold}" ${O}/>
    <rect x="22" y="20" width="56" height="40" fill="#e0ad3c" ${T}/>
    <rect x="26" y="24" width="48" height="32" fill="#a9d0e6" ${T}/>
    <circle cx="16" cy="14" r="4.6" fill="${C.gold}" ${T}/><circle cx="84" cy="14" r="4.6" fill="${C.gold}" ${T}/>
    <circle cx="16" cy="66" r="4.6" fill="${C.gold}" ${T}/><circle cx="84" cy="66" r="4.6" fill="${C.gold}" ${T}/>
    <path d="M50 48 L41 39 M50 48 V34 M50 48 L59 40" ${N} stroke="${C.dgreen}" stroke-width="2.6" stroke-linecap="round"/>
    ${sunflower(40, 39, 6.4)}${sunflower(60, 40, 6.4)}${sunflower(50, 33, 6.8)}
    <path d="M43 56 Q40 50 44 46 H56 Q60 50 57 56 Z" fill="${C.white}" ${T}/>`,
  // 直島 — a plain pumpkin with its ridges at the end of the little pier, the sea around (no dots: not the artwork)
  kabocha: `
    <path d="M8 46 Q50 38 92 46 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <path d="M16 56 q6 -3 12 0 M20 82 q6 -3 12 0 M66 84 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    <rect x="22" y="72" width="5" height="10" fill="${C.stone}" ${T}/><rect x="48" y="72" width="5" height="10" fill="${C.stone}" ${T}/><rect x="74" y="72" width="5" height="10" fill="${C.stone}" ${T}/>
    <rect x="8" y="66" width="80" height="8" rx="1.5" fill="#dcd6cd" ${O}/>
    <path d="M60 30 C52 22 38 24 36 38 C34 50 40 64 50 66 Q55 68 60 66 Q65 68 70 66 C80 64 86 50 84 38 C82 24 68 22 60 30 Z" fill="#f4a93c" ${O}/>
    <path d="M48 27 C40 36 40 56 50 66 M72 27 C80 36 80 56 70 66 M56 30 C52 40 52 56 55 67 M64 30 C68 40 68 56 65 67" ${N} ${T}/>
    <path d="M57 30 Q56 22 59 17 L64 18 Q61 23 62 30 Z" fill="#7a8a4a" ${T}/>
    <path d="M41 40 q1 -6 5 -9" ${N} stroke="#fbe0a8" stroke-width="3" stroke-linecap="round"/>`,
  // 小豆島 エンジェルロード — the white sandbar that appears at low tide, linking the islets; a little pink heart
  angel: `
    <path d="M8 38 Q50 30 92 38 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <path d="M62 80 q6 -3 12 0 M70 64 q5 -3 10 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    ${line('M19 87 Q18 70 30 60 Q40 52 54 50 Q68 48 82 46', '#f7ead0', 8)}
    <path d="M14 56 Q26 32 40 56 Q27 60 14 56 Z" fill="${C.green}" ${O}/>
    <path d="M44 51 Q57 24 70 51 Q57 55 44 51 Z" fill="${C.green}" ${O}/>
    <path d="M74 48 Q82 32 91 48 Q82 51 74 48 Z" fill="${C.green}" ${O}/>
    <path d="M20 46 q4 -7 9 -4 q4 -2 5 3 Z M50 40 q4 -8 10 -5 q4 -2 6 4 Z M78 41 q3 -5 7 -3 q3 -1 4 3 Z" fill="${C.dgreen}" ${T}/>
    <path d="M36 28 C22 20 24 5 36 11 C48 5 50 20 36 28 Z" fill="#f7a6c0" ${O}/>
    <path d="M29 13 q2 -2 4 -1" ${N} stroke="${C.white}" stroke-width="2.2" stroke-linecap="round"/>`,
  // 下灘駅 — the little platform right on the sea: a bench under its roof, the blank name board, the setting sun
  umieki: `
    <rect x="8" y="8" width="84" height="56" rx="10" fill="#f6ad7e" ${O}/>
    <path d="M9.7 38 H90.3 V50 H9.7 Z" fill="#f9c89a"/>
    <circle cx="46" cy="50" r="11" fill="${C.gold}" ${T}/>
    <rect x="9.7" y="50" width="80.6" height="12" fill="#6f8fc9"/>
    <path d="M9.7 50 H90.3" ${N} ${T}/>
    <path d="M36 55 h20 M40 59.5 h12" ${N} stroke="${C.gold}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M8 62 H92 V78 Q50 90 8 78 Z" fill="${C.stone}" ${O}/>
    <path d="M10 66 H90" ${N} stroke="${C.gold}" stroke-width="3"/>
    <rect x="15" y="44" width="3.4" height="20" fill="#8a9098" ${T}/><rect x="28" y="44" width="3.4" height="20" fill="#8a9098" ${T}/>
    <rect x="10" y="30" width="27" height="15" rx="2" fill="${C.white}" ${O}/>
    <rect x="11.7" y="39.5" width="23.6" height="3.8" fill="#6fb6e0"/>
    <rect x="58" y="30" width="4.4" height="36" fill="${C.dwood}" ${T}/><rect x="83" y="30" width="4.4" height="36" fill="${C.dwood}" ${T}/>
    <path d="M52 32 L57 23 H88 L92 32 Z" fill="${C.roof}" ${O}/>
    <path d="M63 58 V68 M82 58 V68" ${N} stroke="${INK}" stroke-width="3" stroke-linecap="round"/>
    <rect x="60" y="46" width="25" height="6" rx="1.5" fill="${C.wood}" ${O}/>
    <rect x="60" y="55" width="25" height="4" rx="1" fill="${C.wood}" ${T}/>
    <path d="M64 52 V55 M81 52 V55" ${N} ${T}/>`,
  // 桂浜 — 坂本龍馬像: the bronze figure in hakama, arms folded, on his tall pedestal; pine and the Pacific
  ryoma: `
    <path d="M8 60 Q50 54 92 60 L92 78 H8 Z" fill="${C.sea}" ${O}/>
    ${ground(74)}
    ${line('M24 82 Q18 64 26 46', '#9a7358', 4)}
    <path d="M8 50 Q10 42 20 42 Q26 36 34 42 Q40 44 38 50 Q30 54 20 52 Q10 54 8 50 Z" fill="${C.dgreen}" ${O}/>
    <path d="M14 36 Q18 28 26 30 Q32 26 36 32 Q34 38 26 38 Q16 40 14 36 Z" fill="${C.dgreen}" ${O}/>
    <path d="M41 84 L43 52 H57 L59 84 Z" fill="${C.stone}" ${O}/>
    <path d="M45 62 h10 M44 72 h12" ${N} ${T}/>
    <rect x="36" y="82" width="28" height="6" rx="1" fill="${C.stone}" ${O}/>
    <rect x="38" y="48" width="24" height="6" rx="1" fill="${C.stone}" ${O}/>
    <path d="M39 49 L43 32 H57 L61 49 Z" fill="${BRONZE}" ${O}/>
    <path d="M50 34 V48 M45 36 L43 48 M55 36 L57 48" ${N} stroke="#43594e" stroke-width="2.2"/>
    <path d="M42 34 Q41 22 50 21 Q59 22 58 34 Z" fill="${BRONZE}" ${O}/>
    <rect x="39" y="25.5" width="22" height="7" rx="3.5" fill="${BRONZE}" ${O}/>
    <path d="M46 21.5 L50 27 L54 21.5" ${N} stroke="#43594e" stroke-width="2.2"/>
    <circle cx="50" cy="14" r="6.4" fill="${BRONZE}" ${O}/>
    <path d="M44 12 Q44 6 50 6.5 Q56 7 56 12 M56 10 q4 1 3 5" ${N} stroke="#43594e" stroke-width="2.4" stroke-linecap="round"/>`,
  // 太宰府天満宮 — the lying bronze ox, its head rubbed to gold, under a branch of plum blossom
  ushi: `
    ${line('M9 38 Q16 26 28 20 Q42 14 56 20 Q64 24 72 20', C.dwood, 3.4)}${line('M38 17 Q40 13 46 12.5', C.dwood, 2.4)}
    ${flower(16, 31, 7.2, C.white, '#e5708d')}${flower(28, 21, 7.2, '#f7a6c0')}${flower(46, 12.5, 4.8, C.white, '#e5708d')}${flower(50, 18, 7.2, C.white, '#e5708d')}${flower(66, 22, 6.8, '#f7a6c0')}
    <path d="M8 90 L12 78 H88 L92 90 Z" fill="${C.stone}" ${O}/>
    <path d="M14 62 q-6 3 -4 12" ${N} stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M14 78 Q10 62 20 54 Q32 46 52 47 Q64 47 70 54 L72 78 Z" fill="#7a6c62" ${O}/>
    <path d="M22 58 Q36 50 54 51" ${N} stroke="#9a8a7c" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M22 78 Q24 69 34 70 Q40 72 40 78 M56 78 Q58 71 66 71" ${N} ${T}/>
    <path d="M71 50 Q62 47 57 52 Q64 55 71 53 Z" fill="#d9ab4f" ${T}/>
    <path d="M73 47 Q71 39 78 36 Q85 34 89 38 Q83 38 80 41 Q78 44 79 47 Z" fill="#d8c49a" ${T}/>
    <path d="M67 52 Q71 43 80 44 Q85 46 88 55 Q93 62 89 68 Q84 73 77 69 L70 63 Q65 58 67 52 Z" fill="#e2b75a" ${O}/>
    <ellipse cx="86" cy="64" rx="5.6" ry="5" fill="#f0cf7a" ${T}/>
    <circle cx="88" cy="63" r="1.4" fill="${INK}"/>
    <path d="M76 53 q2.4 2 5 0" ${N} stroke="${INK}" stroke-width="2.4" stroke-linecap="round"/>`,
  // 糸島 二見ヶ浦 — the wedded rocks in the sea tied with a great straw rope, the white torii in front
  meoto: `
    <path d="M8 46 Q50 38 92 46 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <path d="M30 72 L31 52 Q32 42 38 41 Q44 42 45 52 L45 72 Z" fill="#a89c8f" ${O}/>
    <path d="M55 72 L55 54 Q56 45 62 44 Q68 45 69 54 L70 72 Z" fill="#b3a89b" ${O}/>
    <path d="M34 43.5 q2 -3 4 -2.4 q3 -0.6 4 2.4 Z M59 46.5 q2 -3 4 -2.4 q3 -0.6 4 2.4 Z" fill="${C.dgreen}" ${T}/>
    ${line('M37 52 Q50 61 63 55', '#e2c275', 4.4)}
    ${line('M44 57.5 l1.8 2.2 l-1.8 2.2 l1.8 2.2 M50 58.5 l1.8 2.2 l-1.8 2.2 l1.8 2.2 M56 58 l1.8 2.2 l-1.8 2.2 l1.8 2.2', C.white, 2)}
    <path d="M10 72 Q50 66 90 72 L88 84 Q50 94 12 84 Z" fill="${C.sea}"/>
    ${torii(C.white, 50, 12, 84, 78)}
    <path d="M34 80 q6 -3 12 0 M54 84 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 門司港レトロ — the old 門司港駅: symmetric wooden station, cream walls, steep grey-green roofs, the clock
  retro: `
    <rect x="12" y="46" width="76" height="40" fill="#f3e3c3" ${O}/>
    <path d="M8 38 L14 16 H28 L34 38 Z M66 38 L72 16 H86 L92 38 Z" fill="#6f8c86" ${O}/>
    <path d="M21 16 V10 M79 16 V10" ${N} ${O}/>
    <rect x="10" y="36" width="22" height="50" fill="#f3e3c3" ${O}/><rect x="68" y="36" width="22" height="50" fill="#f3e3c3" ${O}/>
    <path d="M36 40 L41 26 H59 L64 40 Z" fill="#6f8c86" ${O}/>
    <rect x="38" y="38" width="24" height="48" fill="#f3e3c3" ${O}/>
    <path d="M12 62 H88 M16 38 V86 M26 38 V86 M74 38 V86 M84 38 V86 M42 40 V86 M58 40 V86" ${N} stroke="#a07a5a" stroke-width="2.2"/>
    <path d="M18.5 44 h5 v8 h-5 Z M18.5 68 h5 v10 h-5 Z M76.5 44 h5 v8 h-5 Z M76.5 68 h5 v10 h-5 Z M31 50 h5 v8 h-5 Z M64 50 h5 v8 h-5 Z M31 68 h5 v10 h-5 Z M64 68 h5 v10 h-5 Z" fill="${C.sky}" ${T}/>
    <circle cx="50" cy="50" r="6.4" fill="${C.white}" ${O}/>
    <path d="M50 50 V46 M50 50 L53 52" ${N} stroke="${INK}" stroke-width="2.2" stroke-linecap="round"/>
    <rect x="44" y="70" width="12" height="16" fill="${C.dwood}" ${T}/>
    <path d="M8 86 H92" ${N} ${O}/>`,
  // 吉野ヶ里遺跡 — the tall watchtower on stilts, a thatched pit dwelling and the pointed palisade
  yayoi: `
    ${ground(76)}
    <path d="M49 80 Q57 58 71 42 Q85 58 92 80 Z" fill="#d6b46e" ${O}/>
    <path d="M57 70 q14 -6 28 0 M62 60 q9 -5 18 0" ${N} stroke="#b08d4e" stroke-width="2.4"/>
    <path d="M67 44 L71 36 L75 44 Z" fill="#d6b46e" ${T}/>
    ${line('M19 86 L21 42 M39 86 L37 42', C.dwood, 3.4)}
    <path d="M21 72 L37 58 M37 72 L21 58" ${N} ${T}/>
    <rect x="14" y="38" width="30" height="5" fill="${C.wood}" ${O}/>
    <rect x="19" y="28" width="20" height="10" fill="${C.wood}" ${O}/>
    <path d="M10 30 L22 12 H36 L48 30 Z" fill="#d6b46e" ${O}/>
    <path d="M18 24 h22" ${N} stroke="#b08d4e" stroke-width="2.4"/>
    <path d="M8 90 V78 L11 73 L14 78 L17 73 L20 78 L23 73 L26 78 L29 73 L32 78 L35 73 L38 78 L41 73 L44 78 L47 73 L50 78 L53 73 L56 78 L59 73 L62 78 L65 73 L68 78 L71 73 L74 78 L77 73 L80 78 L83 73 L86 78 L89 73 L92 78 V90 Z" fill="${C.wood}" ${O}/>
    <path d="M14 78 V90 M20 78 V90 M26 78 V90 M32 78 V90 M38 78 V90 M44 78 V90 M50 78 V90 M56 78 V90 M62 78 V90 M68 78 V90 M74 78 V90 M80 78 V90 M86 78 V90" ${N} ${T}/>`,
  // 武雄温泉 楼門 — the vermilion two-storey gate, white-walled upper floor, the curved dark roof
  romon: `
    <path d="M12 90 L16 84 H84 L88 90 Z" fill="${C.stone}" ${O}/>
    <rect x="18" y="56" width="64" height="28" fill="${C.verm}" ${O}/>
    <rect x="38" y="62" width="24" height="22" fill="#7f2d27" ${T}/>
    <path d="M28 60 V84 M72 60 V84" ${N} ${T}/>
    <path d="M10 58 Q14 54 20 52 L24 48 H76 L80 52 Q86 54 90 58 Z" fill="${C.roof}" ${O}/>
    <rect x="28" y="34" width="44" height="14" fill="${C.white}" ${O}/>
    <path d="M39 34 V48 M50 34 V48 M61 34 V48" ${N} stroke="${C.verm}" stroke-width="3"/>
    <path d="M8 34 Q15 32 22 28 Q34 16 50 14 Q66 16 78 28 Q85 32 92 34 L87 37 H13 Z" fill="${C.roof}" ${O}/>
    <path d="M40 15.5 H60" ${N} ${O}/>`,
  // ハウステンボス — a Dutch windmill, four white lattice sails, tulips in front (a windmill in general)
  windmill: `
    ${ground(74)}
    <path d="M36 80 L42 40 H58 L64 80 Z" fill="#a8704f" ${O}/>
    <path d="M46 80 V71 Q50 67 54 71 V80 Z" fill="${C.dwood}" ${T}/>
    <rect x="47.5" y="52" width="5" height="6" rx="1" fill="${C.sky}" ${T}/>
    <path d="M40 42 Q41 30 50 28 Q59 30 60 42 Z" fill="${C.roof}" ${O}/>
    ${sail(45)}${sail(135)}${sail(225)}${sail(315)}
    <circle cx="50" cy="36" r="4" fill="${C.roof}" ${T}/>
    ${[[16, C.red], [27, C.gold], [38, C.red], [62, C.gold], [73, C.red], [84, C.gold]].map(([x, c]) => `
      <path d="M${x} 84 V90" ${N} stroke="${C.dgreen}" stroke-width="3" stroke-linecap="round"/>
      <path d="M${Number(x) - 4.5} 84 Q${Number(x) - 5} 77 ${Number(x) - 3} 75.5 L${x} 78 L${Number(x) + 3} 75.5 Q${Number(x) + 5} 77 ${Number(x) + 4.5} 84 Q${x} 87.5 ${Number(x) - 4.5} 84 Z" fill="${c}" ${T}/>`).join('')}`,
  // 軍艦島（端島）— the island packed with concrete blocks behind its sea wall, a battleship on the sea
  gunkanjima: `
    <path d="M8 58 Q50 50 92 58 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <rect x="12" y="42" width="14" height="20" fill="#c3bdb4" ${O}/>
    <rect x="72" y="38" width="14" height="24" fill="#c3bdb4" ${O}/>
    <rect x="24" y="30" width="16" height="32" fill="#aba59d" ${O}/>
    <rect x="58" y="28" width="16" height="34" fill="#aba59d" ${O}/>
    <rect x="38" y="18" width="22" height="44" fill="#bdb7ae" ${O}/>
    <rect x="46" y="9" width="5" height="9" fill="${C.white}" ${T}/>
    ${grid(15, 46, 3, 3)}${grid(27, 34, 3, 5)}${grid(41.5, 22, 4, 7)}${grid(61, 32, 3, 5)}${grid(75, 42, 3, 4)}
    <path d="M8 60 H86 L92 55 L85 72 H16 Q8 70 8 60 Z" fill="#8f8983" ${O}/>
    <path d="M14 66 H84" ${N} stroke="#a9a39c" stroke-width="2.2"/>
    <path d="M22 82 q6 -3 12 0 M60 84 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // グラバー園 — the Western bungalow with its wide white veranda, grey tiled roof, flowers in front
  yokan: `
    ${ground(76)}
    <rect x="66" y="24" width="7" height="14" fill="${C.brick}" ${T}/>
    <path d="M8 52 L21 32 H79 L92 52 Z" fill="#8c949c" ${O}/>
    <rect x="12" y="50" width="76" height="28" fill="#cfe3c8" ${O}/>
    <path d="M20 60 h8 v16 h-8 Z M36 60 h8 v16 h-8 Z M56 60 h8 v16 h-8 Z M72 60 h8 v16 h-8 Z" fill="${C.sky}" ${T}/>
    <rect x="10" y="50" width="80" height="5" fill="${C.white}" ${T}/>
    ${[12, 30, 48, 66, 84].map((x) => `<rect x="${x}" y="55" width="4" height="22" fill="${C.white}" ${T}/>`).join('')}
    <rect x="10" y="76" width="80" height="4" fill="${C.stone}" ${T}/>
    <path d="M8 88 Q10 80 18 81 Q24 76 30 82 Q36 78 42 84 L40 90 H12 Z M58 84 Q64 78 70 82 Q76 76 82 81 Q90 80 92 88 L88 90 H60 Z" fill="${C.dgreen}" ${T}/>
    <g fill="#f7a6c0"><circle cx="18" cy="84" r="2.4"/><circle cx="32" cy="84" r="2.4"/><circle cx="70" cy="84" r="2.4"/><circle cx="84" cy="85" r="2.4"/></g>
    <g fill="${C.red}"><circle cx="25" cy="81" r="2.2"/><circle cx="77" cy="81" r="2.2"/></g>`,
  // 阿蘇山 — the green caldera, the grey crater puffing white smoke, a horse on the 草千里 grass
  aso: `
    <path d="M8 70 Q17 50 30 42 L38 35 H64 L72 42 Q85 50 92 70 Z" fill="#7fae6a" ${O}/>
    <path d="M36 37 L40 33 H62 L66 37 L60 44 H42 Z" fill="#a39b93" ${T}/>
    <ellipse cx="51" cy="37" rx="9" ry="2.6" fill="#6f6358"/>
    <path d="M44 36 Q36 28 42 22 Q42 12 54 14 Q62 7 69 15 Q79 15 77 25 Q81 33 71 33 Q63 37 57 33 Q51 39 44 36 Z" fill="${C.white}" ${O}/>
    ${ground(64)}
    <ellipse cx="72" cy="78" rx="13" ry="4.4" fill="${C.water}" ${T}/>
    ${line('M25 80 V88 M30 81 V89 M40 81 V89 M44 80 V88', '#a0673f', 2.4)}
    <path d="M20 74 q-6 3 -4 10" ${N} stroke="#6b4a33" stroke-width="3" stroke-linecap="round"/>
    <path d="M20 76 Q20 70 28 70 H40 Q46 70 46 76 Q46 82 40 82 H26 Q20 82 20 76 Z" fill="#a0673f" ${T}/>
    <path d="M41 72 L46 61 Q48 57 52 59 L55 64 Q54 67 50 66 L47 75 Z" fill="#a0673f" ${T}/>
    <path d="M45 62 L41 71" ${N} stroke="#6b4a33" stroke-width="2.6" stroke-linecap="round"/>`,
  // 天草 — two dolphins leaping together over the waves
  iruka: `
    <path d="M8 70 Q20 64 32 70 Q44 76 56 70 Q68 64 80 70 Q88 74 92 70 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    ${dolphin(38, 10, 0.82, '#9ab9d2')}
    ${dolphin(8, 28, 1)}
    <circle cx="16" cy="70" r="2.4" fill="${C.white}" ${T}/><circle cx="24" cy="66" r="1.8" fill="${C.white}" ${T}/>
    <path d="M26 82 q6 -3 12 0 M62 82 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 九重“夢”大吊橋 — the long footbridge on its two towers high over the forested gorge, a thin fall below
  tsuribashi: `
    <path d="M8 90 V38 Q9 31 16 32 Q20 26 27 29 Q32 28 33 35 Q36 64 47 90 Z" fill="#4f8a5b" ${O}/>
    <path d="M92 90 V38 Q91 31 84 32 Q80 26 73 29 Q68 28 67 35 Q64 64 53 90 Z" fill="#4f8a5b" ${O}/>
    <path d="M11 54 q5 -4 10 0 M17 70 q5 -4 10 0 M12 82 q5 -4 10 0 M80 52 q5 -4 10 0 M78 68 q5 -4 10 0 M80 84 q5 -4 10 0" ${N} stroke="#7fae6a" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M67 46 H73 V82 H67 Z" fill="${C.white}" ${O}/>
    <path d="M62 84 Q70 79 78 84 Q70 88 62 84 Z" fill="${C.white}" ${T}/>
    <path d="M40 86 Q50 82 60 86 Q62 90 50 91 Q38 90 40 86 Z" fill="${C.water}" ${T}/>
    <path d="M8 40 L24.5 23 Q50 50 75.5 23 L92 40" ${N} stroke="${INK}" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="${tbHangers}" ${N} stroke="${INK}" stroke-width="2"/>
    <rect x="22" y="20" width="5" height="27" rx="1" fill="${C.white}" ${O}/><rect x="73" y="20" width="5" height="27" rx="1" fill="${C.white}" ${O}/>
    ${line('M9 44 H91', C.white, 3.2)}`,
  // 青島 — the round island of palms (a red shrine roof among them) inside the ridged 鬼の洗濯板 rocks
  aoshima: `
    <path d="M8 44 Q50 34 92 44 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <ellipse cx="${AO.cx}" cy="${AO.cy}" rx="${AO.rx}" ry="${AO.ry}" fill="#c2ad8e" ${O}/>
    <path d="${aoRidges}" ${N} stroke="#8f7a60" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M28 66 Q26 44 50 40 Q74 44 72 66 Q50 72 28 66 Z" fill="${C.green}" ${O}/>
    ${line('M36 56 Q35 44 37 34 M50 50 Q49 36 51 24 M63 56 Q64 44 62 34', '#9a7358', 2)}
    ${palm(37, 34)}${palm(62, 34)}${palm(51, 24)}
    <path d="M38 64 L42 59 H52 L56 64 Z" fill="${C.verm}" ${T}/>`,
  // サンメッセ日南 — three moai in a row on the green hill over the sea
  moai: `
    <path d="M8 44 Q50 38 92 44 L92 72 H8 Z" fill="${C.sea}" ${O}/>
    ${ground(72)}
    ${moai(22, 24, 21)}${moai(78, 24, 21)}${moai(50, 12, 24)}`,
  // 指宿 砂むし温泉 — someone buried in the black sand to the neck, towel on the head, under a parasol
  sunamushi: `
    <path d="M8 50 Q50 44 92 50 L92 66 H8 Z" fill="${C.sea}" ${T}/>
    ${line('M66 30 L62 72', '#9a7358', 2.6)}
    <path d="M38 36 Q42 12 64 11 Q86 12 90 36 Q85 32 80 35 Q74 31 68 35 Q62 31 56 35 Q50 31 44 35 Q41 33 38 36 Z" fill="${C.red}" ${O}/>
    <path d="M64 11 Q54 18 52 33 L57 35 Q58 20 64 11 Z M64 11 Q74 18 76 33 L71 35 Q70 20 64 11 Z" fill="${C.white}" ${T}/>
    <circle cx="28" cy="58" r="11" fill="#f7dcc4" ${O}/>
    <path d="M16 57 Q16 44 28 44 Q40 44 40 57 Q34 52 28 52 Q22 52 16 57 Z" fill="${C.white}" ${T}/>
    <path d="M22 59 q2.5 -2.5 5 0 M30 59 q2.5 -2.5 5 0 M25 63 q3.5 3 7 0" ${N} ${T}/>
    <ellipse cx="21" cy="63" rx="2.6" ry="1.6" fill="#f5a3b3"/><ellipse cx="36" cy="63" rx="2.6" ry="1.6" fill="#f5a3b3"/>
    <path d="M8 70 Q18 67 26 69 Q34 70 40 64 Q52 54 66 56 Q80 55 90 62 Q93 64 92 68 L90 84 Q50 94 10 84 Z" fill="#7a716a" ${O}/>
    <g fill="#9a918a"><circle cx="30" cy="80" r="1.8"/><circle cx="52" cy="72" r="1.8"/><circle cx="70" cy="80" r="1.8"/><circle cx="80" cy="68" r="1.6"/><circle cx="44" cy="84" r="1.6"/></g>`,
  // 美ら海水族館 — the whale shark in the big blue tank: dark, white-spotted, its wide flat mouth
  jinbei: `
    <rect x="8" y="8" width="84" height="84" rx="18" fill="#5aa6d6" ${O}/>
    <path d="M30 10 L22 90 M58 10 L52 90" ${N} stroke="#7fbfe4" stroke-width="6" opacity=".55"/>
    <path d="M30 58 Q34 70 44 74 Q40 66 40 58 Z" fill="#4f6488" ${T}/>
    <path d="M14 44 Q22 36 38 36 Q56 35 64 38 L66 26 Q68 24 70 27 L74 40 Q80 42 84 44 L90 28 Q92 26 92 30 L88 50 L92 64 Q92 67 90 66 L84 54 Q74 58 56 60 Q34 62 20 58 Q12 56 12 50 Q12 46 14 44 Z" fill="#4f6488"/>
    <path d="M14 52 Q34 54 56 53 Q72 52 84 50 L84 54 Q74 58 56 60 Q34 62 20 58 Q14 56 14 52 Z" fill="#dfe6ee"/>
    <path d="M14 44 Q22 36 38 36 Q56 35 64 38 L66 26 Q68 24 70 27 L74 40 Q80 42 84 44 L90 28 Q92 26 92 30 L88 50 L92 64 Q92 67 90 66 L84 54 Q74 58 56 60 Q34 62 20 58 Q12 56 12 50 Q12 46 14 44 Z" ${N} ${O}/>
    <path d="M13 51 H25" ${N} ${T}/>
    <path d="M31 42 q-2 5 0 10 M35 41 q-2 5 0 10" ${N} stroke="#8fa2c0" stroke-width="2"/>
    <circle cx="23" cy="45" r="1.8" fill="${INK}"/>
    <g fill="${C.white}"><circle cx="42" cy="40" r="1.8"/><circle cx="50" cy="39.5" r="1.8"/><circle cx="58" cy="40.5" r="1.8"/><circle cx="66" cy="43" r="1.8"/><circle cx="74" cy="45" r="1.6"/><circle cx="46" cy="46" r="1.8"/><circle cx="54" cy="46" r="1.8"/><circle cx="62" cy="47" r="1.8"/><circle cx="70" cy="48" r="1.6"/><circle cx="40" cy="48" r="1.6"/></g>
    <g fill="${C.white}" opacity=".85"><circle cx="24" cy="26" r="2.6"/><circle cx="30" cy="18" r="1.8"/><circle cx="20" cy="16" r="1.5"/><circle cx="80" cy="76" r="1.8"/></g>`,
  // 首里城 — the vermilion Seiden: red-tiled roofs, the big curved 唐破風 at the front with its gold, stone steps
  shurijo: `
    <path d="M8 90 L12 80 H88 L92 90 Z" fill="${C.stone}" ${O}/>
    <path d="M38 90 L40 80 H60 L62 90 Z" fill="#ece5da" ${T}/><path d="M39 84 H61 M38 87 H62" ${N} ${T}/>
    <rect x="12" y="58" width="76" height="22" fill="${SHU}" ${O}/>
    <path d="M20 62 V80 M30 62 V80 M70 62 V80 M80 62 V80" ${N} stroke="${C.gold}" stroke-width="2.4"/>
    <rect x="22" y="36" width="56" height="16" fill="${SHU}" ${O}/>
    <path d="M32 38 V52 M44 38 V52 M56 38 V52 M68 38 V52" ${N} stroke="${C.gold}" stroke-width="2.2"/>
    <path d="M8 38 Q16 34 22 32 L32 20 H68 L78 32 Q84 34 92 38 Z" fill="${AKA}" ${O}/>
    <path d="M24 32 H76 M30 24 H70" ${N} stroke="${C.white}" stroke-width="2.2"/>
    <path d="M31 21 Q29 16 32 14 Q36 13 37 16 Q34.5 16 34.5 18 L35 21 Z M69 21 Q71 16 68 14 Q64 13 63 16 Q65.5 16 65.5 18 L65 21 Z" fill="${C.gold}" ${T}/>
    <path d="M8 60 Q13 56 18 54 L22 50 H78 L82 54 Q87 56 92 60 Z" fill="${AKA}" ${O}/>
    <path d="M28 60 Q38 60 41 50 Q45 38 50 38 Q55 38 59 50 Q62 60 72 60 Z" fill="${AKA}" ${O}/>
    <path d="M36 58 Q42 57 44 51 Q47 44 50 44 Q53 44 56 51 Q58 57 64 58 Z" fill="${SHU}" ${T}/>
    <circle cx="50" cy="52" r="3.6" fill="${C.gold}" ${T}/>
    <path d="M42 56 q4 -3 8 0 q4 -3 8 0" ${N} stroke="${C.gold}" stroke-width="2.4" stroke-linecap="round"/>`,
  // 国際通り — a shisa of red clay, curly mane and a big grin, sitting on a red-tiled Okinawan roof
  shisa: `
    <path d="M8 90 L19 72 H81 L92 90 Z" fill="${AKA}" ${O}/>
    <path d="M27 74 L19 89 M36 74 L32 89 M45.5 74 L45 89 M54.5 74 L55 89 M64 74 L68 89 M73 74 L81 89" ${N} stroke="${C.white}" stroke-width="2.4"/>
    <rect x="14" y="68" width="72" height="6" rx="2" fill="${C.white}" ${O}/>
    <path d="M64 64 Q80 62 80 48 Q86 54 84 62 Q88 60 88 54 Q92 66 80 70 Z" fill="${CLAY}" ${T}/>
    <path d="M32 72 Q30 56 40 50 H60 Q70 56 68 72 Z" fill="${CLAY}" ${O}/>
    <rect x="37" y="56" width="10" height="16" rx="4" fill="${CLAY}" ${T}/><rect x="53" y="56" width="10" height="16" rx="4" fill="${CLAY}" ${T}/>
    ${[150, 180, 210, 240, 270, 300, 330, 360, 390].map((a) => `<circle cx="${f(50 + Math.cos((a * Math.PI) / 180) * 19)}" cy="${f(34 + Math.sin((a * Math.PI) / 180) * 19)}" r="6.6" fill="#c8683e" ${T}/>`).join('')}
    <circle cx="50" cy="36" r="17" fill="${CLAY}" ${O}/>
    <path d="M36 28 q4 -5 9 -1 M55 27 q5 -4 9 1" ${N} stroke="${INK}" stroke-width="3" stroke-linecap="round"/>
    <circle cx="42" cy="33" r="4.4" fill="${C.white}" ${T}/><circle cx="43" cy="33.5" r="2.2" fill="${INK}"/>
    <circle cx="58" cy="33" r="4.4" fill="${C.white}" ${T}/><circle cx="57" cy="33.5" r="2.2" fill="${INK}"/>
    <ellipse cx="50" cy="39" rx="5" ry="3.6" fill="#c8683e" ${T}/>
    <path d="M36 43 Q50 58 64 43 Q50 47 36 43 Z" fill="#c9525a" ${T}/>
    <path d="M38.5 44.5 Q50 49 61.5 44.5" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 竹富島 · 石垣島 — a grey water buffalo pulling the canopied cart past the coral stone wall and a red-tiled house
  suigyu: `
    <path d="M12 42 L26 22 H74 L88 42 Z" fill="${AKA}" ${O}/>
    <path d="M33 24 L24 41 M42 24 L37 41 M50 24 V41 M58 24 L63 41 M67 24 L76 41" ${N} stroke="${C.white}" stroke-width="2.2"/>
    <rect x="24" y="19" width="52" height="4.6" rx="1.5" fill="${C.white}" ${T}/>
    <path d="M8 68 V46 Q8 41 13 41 H87 Q92 41 92 46 V68 Z" fill="#dcd4c6" ${O}/>
    <path d="M8 54 H26 M30 51 H56 M60 56 H92 M18 41 V54 M42 41 V51 M68 46 V56 M82 41 V56 M28 54 V68 M50 58 V68 M76 56 V68" ${N} stroke="#a89f92" stroke-width="2.2"/>
    ${ground(72, '#f3eee4')}
    ${line('M60 58 V44 M86 58 V44', C.dwood, 2.4)}
    <path d="M54 46 L60 39 H86 L92 46 Z" fill="${C.cream}" ${O}/>
    <rect x="56" y="58" width="35" height="10" rx="2" fill="${C.wood}" ${O}/>
    ${line('M45 60 L60 64', C.dwood, 2.6)}
    <circle cx="76" cy="76" r="11" fill="${C.dwood}" ${O}/>
    <path d="M76 66 V86 M66 76 H86 M69 69 L83 83 M83 69 L69 83" ${N} stroke="#c9a57f" stroke-width="2"/>
    <circle cx="76" cy="76" r="3" fill="${C.wood}" ${T}/>
    ${line('M23 74 V87 M29 76 V88 M43 76 V88 M49 74 V87', '#66656a', 3.8)}
    <path d="M55 62 q5 3 3 12" ${N} stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M19 66 Q21 54 35 54 H45 Q56 55 56 66 V70 Q54 78 45 78 H29 Q19 78 19 70 Z" fill="#77767b" ${O}/>
    <path d="M8 66 Q6 58 12 55 Q20 52 25 58 L27 68 Q23 76 15 75 Q8 73 8 66 Z" fill="#77767b" ${O}/>
    <path d="M12 56 Q11 44 22 39 Q32 36 38 43 Q30 42 24 47 Q20 51 20 56 Z" fill="#efe6d6" ${T}/>
    <circle cx="14" cy="62" r="1.8" fill="${INK}"/>
    <ellipse cx="11" cy="70" rx="2.6" ry="1.8" fill="#55545a"/>`,
};

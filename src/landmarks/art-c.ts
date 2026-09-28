// Landmark stickers, 北海道 · 東北 · 北関東 — the 기본 정보 観光 spots (ADR 0011, #93).
// Look-alikes drawn from memory in the mascot likenesses' hand — not photos, not official art.
import { C, INK, N, O, T, ground, line, water } from './helpers';

const r1 = (n: number) => Math.round(n * 10) / 10;

/** A gas lamp on its post: a soft warm glow, the lit glass box and its little dark cap. */
const lamp = (x: number, top: number, bot: number) =>
  `<circle cx="${x}" cy="${top + 5}" r="7.5" fill="#ffd86b" opacity=".55"/>` +
  `<path d="M${x} ${bot} V${top + 9}" ${N} stroke="${INK}" stroke-width="3" stroke-linecap="round"/>` +
  `<rect x="${x - 3.5}" y="${top + 1}" width="7" height="8" rx="1.5" fill="${C.gold}" ${T}/>` +
  `<path d="M${x - 5} ${top + 1.5} L${x} ${top - 3} L${x + 5} ${top + 1.5} Z" fill="${INK}" ${T}/>`;

/** Lit windows: a row of small warm rectangles. */
const lit = (xs: number[], y: number, w = 4, h = 5, fill: string = C.gold) =>
  xs.map((x) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}"/>`).join('');

/** A little four-point twinkle of a star. */
const twinkle = (x: number, y: number, s: number, fill: string = C.white) =>
  `<path d="M${x} ${y - s} Q${x} ${y} ${x + s} ${y} Q${x} ${y} ${x} ${y + s} Q${x} ${y} ${x - s} ${y} Q${x} ${y} ${x} ${y - s} Z" fill="${fill}"/>`;

/** 函館's lights — half-width of the lit land at height y: the far shore, the narrow waist, the town under the mountain. */
const waist = (y: number) => (y < 60 ? 6 + 36 * ((60 - y) / 10) ** 2 : 6 + 28 * ((y - 60) / 24) ** 1.3);
const hakodate = (() => {
  const ys: number[] = [];
  for (let y = 50; y <= 84; y += 1.5) ys.push(y);
  const right = ys.map((y) => `${r1(50 + waist(y))} ${y}`);
  const left = [...ys].reverse().map((y) => `${r1(50 - waist(y))} ${y}`);
  let dots = '';
  for (let row = 0, y = 45.5; y <= 80; row++, y += 3.3) {
    const w = y < 50 ? 40 : waist(y) - 1.8;
    for (let col = 0, x = 50 - w + (row % 2) * 2.1; x <= 50 + w; col++, x += 4.2) {
      const k = (row * 5 + col * 3) % 7;
      dots += `<circle cx="${r1(x)}" cy="${r1(y)}" r="${k < 2 ? 1.7 : 1.2}" fill="${k % 3 ? C.gold : '#fff4cf'}"/>`;
    }
  }
  return { land: `M8 44 H92 V50 L${right.join(' L')} L${left.join(' L')} Z`, dots };
})();

/** A plum blossom: five round petals under one outline, a gold heart ringed with red stamen dots. */
const plum = (cx: number, cy: number, r: number, fill: string) => {
  const at = (k: number, d: number) => {
    const a = ((-90 + k * 72) * Math.PI) / 180;
    return `cx="${r1(cx + d * Math.cos(a))}" cy="${r1(cy + d * Math.sin(a))}"`;
  };
  const ring = (attrs: string, pr: number) => [0, 1, 2, 3, 4].map((k) => `<circle ${at(k, r * 0.56)} r="${r1(pr)}" ${attrs}/>`).join('');
  return (
    ring(`fill="${fill}" ${T}`, r * 0.47) +
    ring(`fill="${fill}"`, r * 0.47 - 1.2) +
    [0, 1, 2, 3, 4].map((k) => `<circle ${at(k + 0.5, r * 0.34)} r="1.3" fill="#d0506a"/>`).join('') +
    `<circle cx="${cx}" cy="${cy}" r="${r1(r * 0.2)}" fill="${C.gold}"/>`
  );
};

/** Points of a spiky ring: n spikes between an outer and an inner radius (the namahage's straw cape). */
const spiky = (cx: number, cy: number, ro: number, ri: number, n: number) => {
  const pts: string[] = [];
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2 - Math.PI / 2, r = i % 2 ? ri : ro;
    pts.push(`${r1(cx + r * Math.cos(a))},${r1(cy + r * Math.sin(a))}`);
  }
  return pts.join(' ');
};

/** Nemophila: pale flower dots scattered over the blue hill (inside the dome, off its edges). */
const nemoDots = (() => {
  let s = '';
  for (let row = 0, y = 47; y <= 88; row++, y += 4.4) {
    for (let x = 12 + (row % 2) * 2.6; x <= 88; x += 5.2) {
      const top = 40 + 40 * (Math.abs(x - 50) / 42) ** 3;
      if (y < top + 3.5 || Math.abs(x - 50) > (y > 84 ? 30 : 99)) continue;
      const k = (row * 7 + Math.round(x)) % 5;
      s += `<circle cx="${r1(x)}" cy="${r1(y)}" r="${k === 0 ? 1.2 : 1.7}" fill="${k === 0 ? C.white : k === 3 ? '#5f9edb' : '#d3ebfb'}"/>`;
    }
  }
  return s;
})();

/** A hanging wisteria bunch, long and tapering, with paler flowers down it. */
const bunch = (x: number, top: number, len: number, fill: string, dot: string) => {
  let dots = '';
  for (let i = 0, y = top + 6; y < top + len - 5; i++, y += 5) {
    const off = (i % 2 ? -1 : 1) * 2.4 * (1 - (y - top) / len);
    dots += `<circle cx="${r1(x + off)}" cy="${r1(y)}" r="1.7" fill="${dot}"/>`;
  }
  return `<path d="M${x - 6} ${top} Q${x - 8} ${r1(top + len * 0.5)} ${x} ${top + len} Q${x + 8} ${r1(top + len * 0.5)} ${x + 6} ${top} Z" fill="${fill}" ${O}/>${dots}`;
};

/** 湯畑: five channels of milky-green water in the wooden frame (top 15–72 at y 44, bottom 8–79 at y 70), and the
 *  湯滝 spilling from each channel's end into the pool below. */
const troughs = (() => {
  const xL = (y: number) => 15 - (7 * (y - 44)) / 26, xR = (y: number) => 72 + (7 * (y - 44)) / 26;
  const cut = (y: number, g: number) => {
    const a = xL(y) + g, w = (xR(y) - g - a - 4 * g) / 5;
    return [0, 1, 2, 3, 4].map((i) => [a + i * (w + g), a + i * (w + g) + w] as const);
  };
  const top = cut(46.5, 1.7), bot = cut(67.5, 2.6);
  const ch = top.map(([a, b], i) => {
    const [c, d] = bot[i] ?? [0, 0];
    return `<path d="M${r1(a)} 46.5 H${r1(b)} L${r1(d)} 67.5 H${r1(c)} Z" fill="#a7dcc6"/>`;
  });
  const falls = bot.map(([c, d]) => `<rect x="${r1(c + 1.5)}" y="75" width="${r1(d - c - 3)}" height="8" fill="${C.white}" ${T}/>`);
  return { ch: ch.join(''), falls: falls.join('') };
})();

/** The stone steps: tread lines closer and closer together as they climb. */
const treads = (() => {
  let s = '';
  for (let y = 84, gap = 6.2; y > 34; gap *= 0.9, y -= gap) {
    const k = (90 - y) * (14 / 58);
    s += `M${r1(30 + k + 1)} ${r1(y)} H${r1(70 - k - 1)} `;
  }
  return s.trim();
})();

/** 陽明門's bracket band: little blocks in red, green, blue and white. */
const brackets = (x0: number, x1: number, y: number, h: number) => {
  const cols = [C.red, '#4fa37e', '#5b8fd6', C.white];
  let s = '';
  for (let i = 0, x = x0; x < x1 - 3; i++, x += 5) s += `<rect x="${x}" y="${y}" width="3.6" height="${h}" fill="${cols[i % 4] ?? C.red}"/>`;
  return s;
};

export const artC: Record<string, string> = {
  // 小樽運河 — old stone warehouses along the canal, gas lamps glowing on the bank
  otaru: `
    <path d="M47 36 L52 24 H88 L93 36 Z" fill="#4a4040" ${O}/>
    <rect x="50" y="36" width="40" height="32" fill="#a6957f" ${O}/>
    <path d="M52 46 H88 M52 56 H88 M60 36 V46 M78 36 V46 M69 46 V56 M56 56 V68 M84 56 V68" ${N} stroke="#8c7b67" stroke-width="2"/>
    <rect x="57" y="39" width="6" height="5" fill="${INK}"/><rect x="77" y="39" width="6" height="5" fill="${INK}"/>
    <path d="M64 68 V59 Q70 52 76 59 V68 Z" fill="${INK}"/>
    <path d="M7 44 L11 33 H47 L52 44 Z" fill="${C.roof}" ${O}/>
    <rect x="9" y="44" width="40" height="24" fill="#b8a791" ${O}/>
    <path d="M11 52 H47 M11 60 H47 M20 44 V52 M38 44 V52 M29 52 V60 M16 60 V68 M42 60 V68" ${N} stroke="#9c8a74" stroke-width="2"/>
    <path d="M24 68 V60 Q29 54 34 60 V68 Z" fill="${INK}"/>
    <path d="M8 68 H92 L90 76 H10 Z" fill="#e2d8c8" ${O}/>
    ${water(76)}
    ${lamp(15, 46, 70)}${lamp(50, 44, 70)}${lamp(85, 46, 70)}
    <path d="M12 82 h6 M47 84 h6 M82 82 h6" stroke="${C.gold}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 函館山 · 稲佐山の夜景 — the night view from the top: an hourglass of lights between two dark bays
  yakei: `
    <rect x="8" y="8" width="84" height="84" rx="16" fill="${C.navy}"/>
    ${twinkle(24, 20, 4.4)}${twinkle(70, 16, 3.4, C.gold)}${twinkle(82, 30, 2.6)}
    <circle cx="44" cy="15" r="1.3" fill="${C.white}"/><circle cx="56" cy="27" r="1.1" fill="${C.white}"/>
    <path d="M8 44 H92 V76 A16 16 0 0 1 76 92 H24 A16 16 0 0 1 8 76 Z" fill="#27325c"/>
    <path d="M8 40 Q16 33 25 37 Q35 29 46 35 Q57 28 68 35 Q79 31 92 38 V46 H8 Z" fill="#1f2743"/>
    <path d="${hakodate.land}" fill="#4d3f55"/>
    ${hakodate.dots}
    <path d="M14 60 h8 M78 60 h8 M12 68 h6 M82 68 h6" stroke="#4a5a8c" stroke-width="2" stroke-linecap="round"/>
    <path d="M8 78 Q22 74 34 80 Q44 86 54 84 Q66 80 76 84 Q86 80 92 76 A16 16 0 0 1 76 92 H24 A16 16 0 0 1 8 76 Z" fill="#1b2238"/>
    <rect x="8" y="8" width="84" height="84" rx="16" ${N} ${O}/>`,
  // 富良野のラベンダー畑 — the rolling hill striped with purple rows, a tree on the crest
  lavender: `
    <path d="M8 50 Q18 36 28 40 Q38 28 50 36 Q62 28 74 38 Q84 34 92 44 V60 H8 Z" fill="#b8c4e2" ${O}/>
    <path d="M8 62 Q30 44 56 50 Q78 54 92 46 V80 Q92 90 80 92 Q50 96 20 92 Q8 90 8 80 Z" fill="${C.green}" ${O}/>
    <path d="M12 66 Q32 52 56 57 Q76 61 88 53 M12 82 Q36 68 60 73 Q80 77 88 69" ${N} stroke="#b59ad8" stroke-width="5.6" stroke-linecap="round"/>
    <path d="M12 74 Q34 60 58 65 Q78 69 88 61 M18 89 Q38 77 62 81 Q80 85 86 78" ${N} stroke="#9c7fcc" stroke-width="5.6" stroke-linecap="round"/>
    <path d="M32 50 V42" ${N} stroke="${C.dwood}" stroke-width="3.4"/>
    <circle cx="32" cy="37" r="7" fill="${C.dgreen}" ${O}/>`,
  // 旭山動物園 — a king penguin on its ice floe: orange ear patches, the pale gold chest
  penguin: `
    <path d="M12 84 Q14 77 26 77 H74 Q86 77 88 84 L84 90 Q50 95 16 90 Z" fill="#e4f2f9" ${O}/>
    <path d="M24 87 q6 -2 12 0 M64 88 q6 -2 12 0" ${N} stroke="#b9d9ea" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M50 10 Q66 10 68 28 Q78 46 76 64 Q74 84 50 84 Q26 84 24 64 Q22 46 32 28 Q34 10 50 10 Z" fill="#3e4659" ${O}/>
    <path d="M50 30 Q62 32 64 52 Q66 78 50 80 Q34 78 36 52 Q38 32 50 30 Z" fill="${C.white}" ${T}/>
    <path d="M40 41 Q43 33 50 33 Q57 33 60 41 Q55 46 50 46 Q45 46 40 41 Z" fill="#f7d774"/>
    <path d="M30 42 Q16 54 18 72 Q28 66 32 54 Z" fill="#3e4659" ${O}/>
    <path d="M70 42 Q84 54 82 72 Q72 66 68 54 Z" fill="#3e4659" ${O}/>
    <path d="M35 21 Q31 27 37 33 Q39 26 35 21 Z M65 21 Q69 27 63 33 Q61 26 65 21 Z" fill="#f29a3a"/>
    <circle cx="43" cy="21" r="3.2" fill="${C.white}"/><circle cx="57" cy="21" r="3.2" fill="${C.white}"/>
    <circle cx="43.6" cy="21.6" r="1.8" fill="${INK}"/><circle cx="56.4" cy="21.6" r="1.8" fill="${INK}"/>
    <path d="M45.5 26 Q50 24 54.5 26 L50 33 Z" fill="${C.verm}" ${T}/>
    <ellipse cx="41" cy="84" rx="7" ry="3.6" fill="${C.verm}" ${T}/><ellipse cx="59" cy="84" rx="7" ry="3.6" fill="${C.verm}" ${T}/>`,
  // 弘前城 — the small white keep with copper-green roofs, framed in cherry blossom, the red bridge in front
  sakurajo: `
    ${water(76)}
    <path d="M22 72 L28 58 H72 L78 72 Z" fill="${C.stone}" ${O}/>
    <path d="M34 64 h10 M54 67 h10" ${N} ${T}/>
    <rect x="31" y="45" width="38" height="13" fill="${C.white}" ${O}/>
    <path d="M37 51 h5 M47.5 51 h5 M58 51 h5" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>
    <path d="M22 46 Q26 43 30 42 L35 36 H65 L70 42 Q74 43 78 46 Z" fill="#7fb3a4" ${O}/>
    <rect x="36" y="29" width="28" height="7" fill="${C.white}" ${O}/>
    <path d="M44 32.5 h4 M52 32.5 h4" stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M27 30 Q31 27 35 26 L39 21 H61 L65 26 Q69 27 73 30 Z" fill="#7fb3a4" ${O}/>
    <rect x="40" y="15" width="20" height="6" fill="${C.white}" ${O}/>
    <path d="M32 16 Q35 13 39 12 L42 8 H58 L61 12 Q65 13 68 16 Z" fill="#7fb3a4" ${O}/>
    <path d="M8 62 Q6 48 13 44 Q11 32 20 30 Q24 22 32 26 Q38 30 36 38 Q42 46 34 52 Q36 62 28 66 Q18 72 11 68 Q8 66 8 62 Z" fill="${C.pink}" ${O}/>
    <path d="M92 62 Q94 48 87 44 Q89 32 80 30 Q76 22 68 26 Q62 30 64 38 Q58 46 66 52 Q64 62 72 66 Q82 72 89 68 Q92 66 92 62 Z" fill="${C.pink}" ${O}/>
    <g fill="${C.white}"><circle cx="18" cy="40" r="2.4"/><circle cx="28" cy="54" r="2.4"/><circle cx="13" cy="58" r="2"/><circle cx="82" cy="40" r="2.4"/><circle cx="72" cy="54" r="2.4"/><circle cx="87" cy="58" r="2"/></g>
    <g fill="#e5708d"><circle cx="24" cy="44" r="1.8"/><circle cx="76" cy="44" r="1.8"/><circle cx="18" cy="62" r="1.6"/><circle cx="82" cy="62" r="1.6"/></g>
    ${line('M14 64 Q50 48 86 64', C.red, 3)}
    <path d="M24 67 V61 M37 64.5 V58 M50 63.5 V57 M63 64.5 V58 M76 67 V61" ${N} stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>
    ${line('M12 72 Q50 56 88 72', C.red, 5.5)}`,
  // 奥入瀬渓流 · 昇仙峡 — the clear stream over mossy rocks, a little white cascade, trees on both banks
  keiryu: `
    <path d="M9 66 Q5 56 10 49 Q7 40 12 34 Q11 24 20 22 Q25 13 34 17 Q43 16 44 26 Q51 32 45 40 Q50 49 43 55 Q45 64 36 66 Z" fill="${C.dgreen}" ${O}/>
    <path d="M91 66 Q95 56 90 49 Q93 40 88 34 Q89 24 80 22 Q75 13 66 17 Q57 16 56 26 Q49 32 55 40 Q50 49 57 55 Q55 64 64 66 Z" fill="${C.dgreen}" ${O}/>
    <path d="M13 40 q1 -7 8 -9 M25 25 q3 -4 8 -4 M87 40 q-1 -7 -8 -9 M75 25 q-3 -4 -8 -4" ${N} stroke="${C.green}" stroke-width="3" stroke-linecap="round"/>
    <path d="M45 36 Q50 34 55 36 Q58 50 67 60 Q79 72 88 82 Q88 90 78 92 H22 Q12 90 12 82 Q21 72 33 60 Q42 50 45 36 Z" fill="#9dd6df" ${O}/>
    <path d="M47 42 v6 M53 44 v5" stroke="${C.white}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M28 63 Q50 55 72 63 L72 68 Q50 61 28 68 Z" fill="#9b978e" ${T}/>
    <path d="M29 63 Q50 55 71 63" ${N} stroke="#7fae6a" stroke-width="3.2" stroke-linecap="round"/>
    <path d="M38 60 Q50 57 62 60 L64 73 Q50 70 36 73 Z" fill="${C.white}" ${T}/>
    <path d="M43 62 v8 M50 61 v9 M57 62 v8" stroke="#9dd6df" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M34 76 q4 -4 8 0 q4 -4 8 0 q4 -4 8 0 q4 -4 8 0" ${N} stroke="${C.white}" stroke-width="3" stroke-linecap="round"/>
    <path d="M8 86 Q8 74 18 72 Q30 72 32 84 Q30 92 20 92 Q10 92 8 86 Z" fill="#9b978e" ${O}/>
    <path d="M10 78 Q16 71 26 72 Q31 74 32 79 Q20 76 10 78 Z" fill="#7fae6a" ${T}/>
    <path d="M92 86 Q92 76 84 74 Q72 74 70 84 Q72 92 82 92 Q90 92 92 86 Z" fill="#9b978e" ${O}/>
    <path d="M90 79 Q84 73 76 74 Q71 76 70 81 Q80 78 90 79 Z" fill="#7fae6a" ${T}/>
    <path d="M42 86 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 中尊寺金色堂 — the little hall all in gold: gold walls, the gold pyramid roof and its jewel, cedars behind
  konjiki: `
    <path d="M8 80 Q10 60 14 44 Q16 30 20 16 Q24 30 26 44 Q30 60 32 80 Z" fill="#4f8a5b" ${O}/>
    <path d="M92 80 Q90 60 86 44 Q84 30 80 16 Q76 30 74 44 Q70 60 68 80 Z" fill="#4f8a5b" ${O}/>
    <path d="M16 90 L20 80 H80 L84 90 Z" fill="${C.stone}" ${O}/>
    <rect x="26" y="56" width="48" height="24" fill="${C.gold}" ${O}/>
    <path d="M34 57 V79 M66 57 V79" stroke="#d9a33a" stroke-width="3"/>
    <rect x="42" y="60" width="16" height="20" fill="#e8b33c" ${T}/>
    <path d="M50 60 V80" ${N} ${T}/>
    <path d="M10 58 Q22 54 28 48 L50 28 L72 48 Q78 54 90 58 Z" fill="${C.gold}" ${O}/>
    <path d="M24 53 L50 33 L76 53" ${N} stroke="#d9a33a" stroke-width="2.4"/>
    <path d="M45 29 H55 L53 24 H47 Z" fill="${C.gold}" ${T}/>
    <path d="M50 9 Q57 16 50 24 Q43 16 50 9 Z" fill="${C.gold}" ${O}/>
    <path d="M30 62 v10 M40 44 l6 -5" stroke="#fff6d6" stroke-width="2.6" stroke-linecap="round"/>`,
  // 浄土ヶ浜 — jagged white rock spires rising from the calm blue sea, little pines on top
  shiroiwa: `
    <path d="M8 60 Q50 54 92 60 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <path d="M10 74 L13 58 L19 50 L23 54 L27 38 L33 34 L38 42 L42 40 L47 54 L49 74 Z" fill="#f6f2ea" ${O}/>
    <path d="M34.5 36 L38 42 L42 40 L47 54 L48.5 72 H41 L38 50 Z" fill="#ddd5c8"/>
    <path d="M46 74 L50 54 L55 42 L58 30 L64 28 L68 38 L72 36 L77 50 L80 48 L87 74 Z" fill="#f6f2ea" ${O}/>
    <path d="M65.5 31 L68 38 L72 36 L77 50 L80 48 L85.5 72 H74 L70 50 Z" fill="#ddd5c8"/>
    <path d="M29 38 V33 M60 30 V25 M73 38 V33" ${N} stroke="${C.dwood}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M22 34 Q23 28 29 28 Q33 24 38 28 Q42 29 40 33 Q31 36 22 34 Z M53 25 Q54 19 60 19 Q64 15 69 19 Q73 20 71 24 Q62 27 53 25 Z M67 34 Q68 29 73 29 Q77 27 80 31 Q81 34 77 35 Q71 37 67 34 Z" fill="${C.dgreen}" ${T}/>
    <path d="M10 71 Q50 65 90 71 L88 84 Q50 94 12 84 Z" fill="${C.sea}"/>
    <path d="M22 80 q6 -3 12 0 M58 82 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 小岩井農場 · 那須高原 — a red barn with white trim, the silo, a black-and-white cow on the pasture
  farm: `
    ${ground(76)}
    <path d="M62 78 V32 Q62 20 70 20 Q78 20 78 32 V78 Z" fill="#e6e0d6" ${O}/>
    <path d="M62 32 Q70 28 78 32 M62 46 H78 M62 60 H78" ${N} ${T}/>
    <path d="M12 78 V48 L20 34 L36 25 L52 34 L60 48 V78 Z" fill="${C.red}" ${O}/>
    <path d="M17 47 L23 37 L36 30 L49 37 L55 47" ${N} stroke="${C.white}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="31" y="37" width="10" height="8" fill="${C.white}" ${T}/>
    <rect x="25" y="56" width="22" height="22" fill="#b8392f" stroke="${C.white}" stroke-width="2.8"/>
    <path d="M25 56 L47 78 M47 56 L25 78" ${N} stroke="${C.white}" stroke-width="2.6"/>
    <path d="M58 86 V78 M64 86 V78 M76 86 V78 M82 86 V78" ${N} stroke="${INK}" stroke-width="4.6" stroke-linecap="round"/>
    <path d="M54 70 Q54 60 64 60 H78 Q86 60 86 68 Q86 78 78 78 H62 Q54 78 54 70 Z" fill="${C.white}" ${O}/>
    <path d="M60 62 Q67 61 68 67 Q66 73 59 70 Z M74 66 Q80 62 83 69 Q80 76 73 72 Z" fill="#4a4040"/>
    <path d="M54 66 q-4 4 -2 10" ${N} ${T}/>
    <path d="M81 56 Q89 53 92 60 Q93 70 87 72 Q81 72 81 64 Z" fill="${C.white}" ${O}/>
    <ellipse cx="88" cy="68" rx="4" ry="3" fill="#f7c5c9" ${T}/>
    <circle cx="85" cy="61" r="1.6" fill="${INK}"/>
    <path d="M83 55 l-2 -4 M89 54 l2 -4" ${N} ${T}/>`,
  // 蔵王の御釜 — the round emerald crater lake inside its ridged grey-brown walls
  okama: `
    <path d="M8 68 Q8 52 14 46 L22 36 L32 34 L40 24 L50 27 L60 21 L70 30 L80 32 L88 44 Q92 52 92 68 Z" fill="#a38b78" ${O}/>
    <path d="M14 56 Q30 40 50 40 Q70 40 86 56 M18 48 Q34 32 50 33" ${N} stroke="#c7b09b" stroke-width="3" stroke-linecap="round"/>
    <path d="M13 62 Q30 48 50 47 Q70 48 87 62" ${N} stroke="#86705f" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M30 36 v6 M62 26 v8 M76 36 v7" ${N} stroke="#86705f" stroke-width="2.4" stroke-linecap="round"/>
    <ellipse cx="50" cy="66" rx="34" ry="15" fill="#4cbf9f" ${O}/>
    <path d="M28 61 Q38 56 52 56.5" ${N} stroke="#c4f2e2" stroke-width="3" stroke-linecap="round"/>
    <path d="M8 76 Q13 72 20 75 Q28 79 36 75 Q44 72 52 76 Q60 79 68 75 Q76 72 84 76 Q89 78 92 75 V84 Q91 92 80 92 H20 Q9 92 8 84 Z" fill="#8e7766" ${O}/>
    <path d="M18 84 h8 M44 86 h10 M72 84 h8" ${N} stroke="#6f5847" stroke-width="2.4" stroke-linecap="round"/>`,
  // 角館の武家屋敷 — the black board fence and its roofed gate, a weeping cherry hanging over it
  bukeyashiki: `
    ${ground(76, '#e6dccb')}
    <rect x="8" y="58" width="84" height="20" fill="#3f3a3a" ${O}/>
    <path d="M15 60 V78 M22 60 V78 M29 60 V78 M36 60 V78 M43 60 V78 M50 60 V78 M57 60 V78 M64 60 V78" ${N} stroke="#5f5857" stroke-width="2"/>
    <path d="M7 59 L11 53 H89 L93 59 Z" fill="${C.roof}" ${O}/>
    <rect x="68" y="50" width="20" height="28" fill="#6b5044" ${O}/>
    <path d="M78 55 V78" ${N} ${T}/>
    <path d="M62 51 Q66 47 70 45 L73 39 H83 L86 45 Q89 47 93 51 Z" fill="${C.roof}" ${O}/>
    ${line('M33 58 Q31 42 34 26', '#7a5646', 5)}
    ${line('M34 27 Q22 13 10 24 M34 27 Q46 11 60 22', '#7a5646', 3)}
    ${line('M12 25 Q9 42 11 62', C.pink, 5)}${line('M18 18 Q14 42 17 69', C.pink, 5)}${line('M25 15 Q22 42 25 73', C.pink, 5)}
    ${line('M42 15 Q45 42 42 73', C.pink, 5)}${line('M49 15 Q53 42 50 69', C.pink, 5)}${line('M56 19 Q61 40 58 62', C.pink, 5)}
    <path d="M8 26 Q9 16 16 16 Q20 9 28 11 Q34 6 40 10 Q48 7 52 13 Q60 13 62 21 Q62 27 56 26 Q50 22 44 24 Q38 20 34 25 Q28 20 22 24 Q16 21 12 27 Q9 30 8 26 Z" fill="${C.pink}" ${O}/>
    <g fill="${C.white}"><circle cx="18" cy="17" r="2.2"/><circle cx="34" cy="12" r="2.2"/><circle cx="52" cy="17" r="2"/><circle cx="11" cy="46" r="1.5"/><circle cx="16" cy="56" r="1.5"/><circle cx="24" cy="40" r="1.5"/><circle cx="43" cy="50" r="1.5"/><circle cx="51" cy="36" r="1.5"/><circle cx="58" cy="50" r="1.5"/></g>`,
  // 田沢湖 — the little golden たつこ statue on her rock in the deep-blue lake, green hills behind
  tatsuko: `
    <path d="M8 58 Q20 36 36 44 Q50 30 66 42 Q80 34 92 54 Z" fill="${C.dgreen}" ${O}/>
    <path d="M8 58 Q50 52 92 58 L90 84 Q50 94 10 84 Z" fill="#4a86cc" ${O}/>
    <path d="M20 80 q6 -3 12 0 M66 82 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M34 76 Q36 66 45 64 H57 Q66 66 67 76 Q50 80 34 76 Z" fill="#a9a399" ${O}/>
    <path d="M44.6 23 Q43 31 45.5 41 H54.5 Q57 31 55.4 23 Z" fill="#d9a93a" ${T}/>
    <path d="M47 33 Q43 34 43 38.5 L44.5 48 Q42 58 41 67 H59 Q58 58 55.5 48 L57 38.5 Q57 34 53 33 Z" fill="${C.gold}" ${O}/>
    <circle cx="50" cy="26" r="5.4" fill="${C.gold}" ${O}/>
    <path d="M45 38 Q47 43 50 42 Q53 43 55 38" ${N} ${T}/>
    <path d="M47.5 50 L46 64 M52.5 50 L54 64" ${N} stroke="#d9a93a" stroke-width="2" stroke-linecap="round"/>
    <path d="M47 83 h6 M46 87 h8" stroke="${C.gold}" stroke-width="2.4" stroke-linecap="round"/>`,
  // 男鹿のなまはげ — the red demon face: short horns, glaring eyes, white fangs, in its shaggy straw cape
  namahage: `
    <polygon points="${spiky(50, 52, 41, 32, 15)}" fill="#dcb96c" ${O}/>
    <path d="M18 34 L26 40 M12 54 L22 54 M16 74 L25 68 M82 34 L74 40 M88 54 L78 54 M84 74 L75 68 M30 86 L35 78 M70 86 L65 78 M50 92 V84" ${N} stroke="#b08f45" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M34 26 Q27 16 30 7 Q38 13 41 22 Z M66 26 Q73 16 70 7 Q62 13 59 22 Z" fill="${C.cream}" ${O}/>
    <path d="M29 40 Q29 18 50 18 Q71 18 71 40 V58 Q71 80 50 80 Q29 80 29 58 Z" fill="${C.red}" ${O}/>
    <path d="M32 35 L46 41 M68 35 L54 41" ${N} stroke="${INK}" stroke-width="5" stroke-linecap="round"/>
    <circle cx="40" cy="47" r="6.6" fill="${C.white}" ${O}/><circle cx="60" cy="47" r="6.6" fill="${C.white}" ${O}/>
    <circle cx="41" cy="48" r="3" fill="${INK}"/><circle cx="59" cy="48" r="3" fill="${INK}"/>
    <path d="M45 52 Q50 48 55 52 Q57 59 50 59 Q43 59 45 52 Z" fill="#c2423a" ${T}/>
    <path d="M35 63 Q50 60 65 63 Q63 77 50 77 Q37 77 35 63 Z" fill="${INK}" ${T}/>
    <path d="M37 63.5 Q50 61 63 63.5 L62 67 Q50 65 38 67 Z" fill="${C.white}"/>
    <path d="M39 75 L41.5 68 L44.5 75.5 Z M61 75 L58.5 68 L55.5 75.5 Z" fill="${C.white}"/>`,
  // 山寺（立石寺）— the little 五大堂 with its open balcony, perched on top of the steep grey rock
  yamadera: `
    <path d="M14 92 L20 62 Q22 50 32 46 L40 44 H66 Q76 48 78 60 L86 92 Z" fill="#b2aca3" ${O}/>
    <path d="M30 58 L27 76 M44 52 L46 70 M60 54 L57 72 M70 64 L74 84 M38 80 L36 90" ${N} stroke="#8e887f" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M10 76 Q6 66 14 62 Q16 54 24 58 Q32 58 30 68 Q34 76 26 78 Z" fill="${C.green}" ${O}/>
    <path d="M68 82 Q64 72 72 68 Q76 60 84 64 Q92 66 90 76 Q92 84 82 84 Z" fill="${C.dgreen}" ${O}/>
    <path d="M62 44 Q60 34 68 32 Q74 26 80 32 Q88 34 84 42 Q80 48 70 46 Z" fill="${C.dgreen}" ${O}/>
    <path d="M28 44 L32 56 M38 44 L40 52" ${N} stroke="${C.dwood}" stroke-width="3" stroke-linecap="round"/>
    <rect x="18" y="40" width="44" height="5" fill="${C.wood}" ${O}/>
    <rect x="26" y="26" width="30" height="14" fill="${C.wood}" ${O}/>
    <rect x="30" y="29" width="22" height="11" fill="${C.dwood}"/>
    <path d="M18 35 H62 M22 35 V40 M30 35 V40 M38 35 V40 M46 35 V40 M54 35 V40" ${N} ${T}/>
    <path d="M14 28 Q22 24 26 22 L32 14 H50 L56 22 Q60 24 68 28 Z" fill="${C.roof}" ${O}/>`,
  // 銀山温泉 — tall wooden inns facing each other over the narrow river: lit windows, gas lamps, snow on the roofs
  ginzan: `
    <path d="M12 86 V22 Q12 12 22 12 H78 Q88 12 88 22 V86 Z" fill="#5d70a6"/>
    <g fill="${C.white}"><circle cx="46" cy="20" r="1.4"/><circle cx="56" cy="28" r="1.2"/><circle cx="50" cy="36" r="1.3"/></g>
    <rect x="42" y="46" width="16" height="16" fill="#9c6a45" ${T}/>${lit([45, 51], 50, 4, 5)}
    <path d="M40 47 L44 42 H56 L60 47 Z" fill="${C.roof}" ${T}/><path d="M44 42 Q50 39 56 42" ${N} stroke="${C.white}" stroke-width="2.6"/>
    <path d="M44 62 H56 L66 92 H34 Z" fill="#7fb0dc" ${O}/>
    <rect x="8" y="30" width="30" height="58" fill="#a0704a" ${O}/>
    <path d="M7 32 L12 23 H34 L39 32 Z" fill="${C.roof}" ${O}/><path d="M12 23 Q22 18 34 23 Z" fill="${C.white}" ${T}/>
    <path d="M7.5 50 H38.5 M7.5 68 H38.5" ${N} stroke="${INK}" stroke-width="4"/><path d="M8 48 H38 M8 66 H38" ${N} stroke="${C.white}" stroke-width="2.6"/>
    ${lit([12, 20, 28], 36, 5, 8)}${lit([12, 20, 28], 54, 5, 8)}${lit([12, 20, 28], 73, 5, 9)}
    <rect x="62" y="26" width="30" height="62" fill="#a0704a" ${O}/>
    <path d="M61 28 L66 19 H88 L93 28 Z" fill="${C.roof}" ${O}/><path d="M66 19 Q77 14 88 19 Z" fill="${C.white}" ${T}/>
    <path d="M61.5 46 H92.5 M61.5 66 H92.5" ${N} stroke="${INK}" stroke-width="4"/><path d="M62 44 H92 M62 64 H92" ${N} stroke="${C.white}" stroke-width="2.6"/>
    ${lit([67, 75, 83], 32, 5, 8)}${lit([67, 75, 83], 51, 5, 9)}${lit([67, 75, 83], 72, 5, 9)}
    ${lamp(40, 60, 90)}${lamp(60, 60, 90)}`,
  // 蔵王の樹氷 — the snow monsters: three bulky white rime-covered trees on the snowy slope
  juhyo: `
    <rect x="8" y="10" width="84" height="76" rx="18" fill="#c5d5e6"/>
    <g fill="${C.white}"><circle cx="20" cy="22" r="1.6"/><circle cx="84" cy="24" r="1.6"/><circle cx="72" cy="16" r="1.3"/><circle cx="30" cy="14" r="1.3"/></g>
    <path d="M8 72 Q40 62 92 68 V80 Q92 90 80 92 H20 Q8 90 8 80 Z" fill="${C.white}" ${O}/>
    <path d="M18 84 q10 -4 20 -2 M58 86 q10 -4 20 -2" ${N} stroke="#c3d6ea" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M9 76 Q5 66 11 60 Q6 52 13 46 Q10 37 18 34 Q19 26 27 28 Q35 28 34 36 Q41 40 37 48 Q44 54 38 61 Q43 68 38 76 Z" fill="${C.white}" ${O}/>
    <path d="M64 74 Q59 66 65 60 Q61 52 67 47 Q66 39 73 38 Q80 36 82 44 Q89 48 85 56 Q92 62 87 74 Z" fill="${C.white}" ${O}/>
    <path d="M35 73 Q29 63 35 56 Q30 48 36 41 Q33 32 40 28 Q40 19 48 17 Q56 15 59 23 Q66 26 63 35 Q70 41 65 49 Q72 56 66 64 Q70 70 66 73 Z" fill="${C.white}" ${O}/>
    <path d="M31 38 Q35 43 32 48 M34 55 Q37 61 33 67 M58 27 Q61 32 58 37 M60 45 Q64 51 60 56 M61 61 Q64 66 61 70 M81 49 Q84 54 81 58 M82 63 Q85 67 82 71" ${N} stroke="#bcd3ea" stroke-width="3.6" stroke-linecap="round"/>
    <path d="M33 45 q3 1 3 4 q-3 0 -3 -4 Z M59 40 q3 1 3 4 q-3 0 -3 -4 Z M60 60 q3 1 3 4 q-3 0 -3 -4 Z M81 53 q3 1 2.6 4 q-2.8 -0.4 -2.6 -4 Z" fill="${C.dgreen}" ${T}/>`,
  // 大内宿 — the row of houses under thick hipped thatch, the dirt road in front
  kayabuki: `
    ${ground(78, '#dcc6a2')}
    <rect x="71" y="58" width="19" height="20" fill="#efe3cc" ${O}/>
    <path d="M67 60 Q68 56 71 54 L74 48 Q75 46 77 46 H85 Q87 46 88 48 L90.5 54 Q92.5 56 93 60 Z" fill="#c99f62" ${O}/>
    <rect x="44" y="60" width="28" height="20" fill="#efe3cc" ${O}/>
    <path d="M53 60 V80 M63 60 V80" ${N} stroke="#6b5044" stroke-width="2.4"/>
    <path d="M40 62 Q41 57 44 55 L48 46 Q49 43 52 43 H62 Q65 43 66 46 L70 55 Q73 57 74 62 Z" fill="#c99f62" ${O}/>
    <path d="M41 61 Q42 58.5 44 57 H70 Q72 58.5 73 61 Z" fill="#a37b45"/>
    <rect x="9" y="62" width="36" height="20" fill="#efe3cc" ${O}/>
    <path d="M19 62 V82 M35 62 V82" ${N} stroke="#6b5044" stroke-width="2.4"/>
    <rect x="21" y="67" width="12" height="15" fill="#6b5044"/>
    <path d="M7 65 Q8 60 11 57 L15.5 45 Q16.5 41 20.5 41 H33.5 Q37.5 41 38.5 45 L44 57 Q48 60 49 65 Z" fill="#c99f62" ${O}/>
    <path d="M8 64 Q9 60.5 11 58.5 H44.5 Q47 60.5 48 64 Z" fill="#a37b45"/>
    <path d="M17 50 v5 M24 47 v7 M31 47 v7 M38 50 v5 M52 49 v5 M58 48 v6 M64 49 v5 M79 50 v4 M84 50 v4" stroke="#a37b45" stroke-width="2.2" stroke-linecap="round"/>
    <rect x="18" y="38" width="18" height="4.4" rx="2" fill="${INK}"/><rect x="50" y="40.5" width="14" height="3.8" rx="1.8" fill="${INK}"/><rect x="76" y="43.6" width="10" height="3.4" rx="1.6" fill="${INK}"/>`,
  // 五色沼 — three ponds in different vivid colours among the green forest, 磐梯山 behind
  numa: `
    <path d="M8 50 L28 24 Q34 16 40 22 L54 36 L62 30 L92 52 Z" fill="#8f9c7c" ${O}/>
    <path d="M8 50 Q50 40 92 52 V80 Q92 90 80 92 H20 Q8 90 8 80 Z" fill="${C.green}" ${O}/>
    <path d="M14 64 Q16 56 28 56 Q42 56 44 64 Q42 72 28 72 Q14 72 14 64 Z" fill="#3f73cf" ${O}/>
    <path d="M54 60 Q56 52 68 53 Q82 54 84 61 Q82 68 68 68 Q56 68 54 60 Z" fill="#4cc5c8" ${O}/>
    <path d="M30 82 Q32 75 46 75 Q62 75 64 82 Q62 89 46 89 Q32 89 30 82 Z" fill="#2fa37f" ${O}/>
    <path d="M20 62 q5 -3 10 -2 M60 58 q5 -3 10 -2 M38 80 q5 -3 10 -2" ${N} stroke="${C.white}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M44 64 Q42 58 47 56 Q48 51 53 53 Q57 55 55 60 Q57 65 50 65 Z M71 84 Q68 78 73 76 Q75 71 80 73 Q85 75 83 80 Q85 86 78 86 Z M13 84 Q11 78 16 76 Q18 72 22 74 Q26 76 25 80 Q26 86 20 86 Z" fill="${C.dgreen}" ${T}/>`,
  // 国営ひたち海浜公園 — みはらしの丘 carpeted in sky-blue nemophila, trees on top
  nemophila: `
    <path d="M12 70 Q8 30 34 22 Q50 16 66 22 Q92 30 88 70 Z" fill="${C.sky}"/>
    <path d="M8 80 Q12 46 50 40 Q88 46 92 80 Q92 90 80 92 H20 Q8 90 8 80 Z" fill="#86bff0" ${O}/>
    ${nemoDots}
    <path d="M46 42 V32 M57 42 V34" ${N} stroke="${C.dwood}" stroke-width="3.4"/>
    <circle cx="46" cy="28" r="7" fill="${C.dgreen}" ${O}/>
    <circle cx="57" cy="31" r="5.5" fill="${C.dgreen}" ${O}/>`,
  // 偕楽園 — a dark twisted plum branch with round white and pink blossoms
  ume: `
    ${line('M12 90 Q18 76 28 70 Q40 62 42 50 Q44 38 58 32 Q70 28 76 16', '#6e4d3d', 6)}
    ${line('M42 52 Q54 56 64 52 Q74 48 86 52', '#6e4d3d', 4)}
    ${line('M58 33 Q60 24 54 16', '#6e4d3d', 3.4)}
    ${plum(30, 66, 14, C.white)}
    ${plum(62, 30, 12, '#f7b3c6')}
    ${plum(76, 54, 11, C.white)}
    ${plum(40, 40, 9, '#f7b3c6')}
    <circle cx="78" cy="15" r="3.6" fill="#e8708f" ${T}/><circle cx="87" cy="50" r="3" fill="#e8708f" ${T}/><circle cx="53" cy="15" r="3" fill="#e8708f" ${T}/>`,
  // 牛久大仏 — the giant standing bronze Buddha against the open sky (no halo, like the real one): one hand raised, long
  // robe, lotus pedestal; a tiny tree for scale
  ushiku: `
    <path d="M26 90 L30 82 H70 L74 90 Z" fill="${C.stone}" ${O}/>
    <path d="M30 82 Q34 76 40 79 Q45 74 50 78 Q55 74 60 79 Q66 76 70 82 Z" fill="#e9c9cf" ${T}/>
    <path d="M34 80 L37 44 Q38 34 46 32 H54 Q62 34 63 44 L66 80 Z" fill="#8fa697" ${O}/>
    <path d="M40 52 Q50 58 60 52 M39 62 Q50 70 61 62 M38 72 Q50 78 62 72" ${N} stroke="#6d8578" stroke-width="2.2"/>
    ${line('M40 52 Q35 48 36 40', '#8fa697', 5)}<ellipse cx="36" cy="37" rx="3.4" ry="4.2" fill="#8fa697" ${T}/>
    ${line('M60 52 Q64 58 63 64', '#8fa697', 5)}<ellipse cx="63" cy="67" rx="3.4" ry="4" fill="#8fa697" ${T}/>
    <circle cx="50" cy="22" r="8" fill="#8fa697" ${O}/>
    <circle cx="50" cy="13.5" r="3.6" fill="#8fa697" ${T}/>
    <path d="M45.6 23 h3.2 M51.2 23 h3.2" stroke="#5f766a" stroke-width="2" stroke-linecap="round"/>
    <path d="M84 90 V84" ${N} stroke="${C.dwood}" stroke-width="2.4"/><circle cx="84" cy="81" r="4.5" fill="${C.dgreen}" ${T}/>`,
  // 日光東照宮 陽明門 — the ornate two-storey gate: white pillars, gold and coloured brackets, dark roofs edged in gold
  yomeimon: `
    <path d="M12 90 L16 84 H84 L88 90 Z" fill="${C.stone}" ${O}/>
    <rect x="20" y="60" width="60" height="24" fill="${C.white}" ${O}/>
    <rect x="40" y="64" width="20" height="20" fill="#4a3f3b"/>
    <path d="M30 60 V84 M40 60 V84 M60 60 V84 M70 60 V84" ${N} ${T}/>
    <path d="M23 67 h4 M73 67 h4 M23 75 h4 M73 75 h4" stroke="${C.gold}" stroke-width="2.6" stroke-linecap="round"/>
    <rect x="18" y="53" width="64" height="7" fill="${C.gold}" ${O}/>
    ${brackets(21, 80, 54.8, 3.4)}
    <path d="M8 55 Q14 51 20 49 L26 43 H74 L80 49 Q86 51 92 55 Z" fill="#403a3a" ${O}/>
    <path d="M12 53.4 H88" ${N} stroke="${C.gold}" stroke-width="2.2"/>
    <rect x="24" y="37" width="52" height="6" fill="${C.white}" ${O}/>
    <path d="M32 37 V43 M41 37 V43 M50 37 V43 M59 37 V43 M68 37 V43" ${N} ${T}/>
    <rect x="30" y="29" width="40" height="8" fill="${C.gold}" ${O}/>
    ${brackets(33, 70, 31, 4)}
    <path d="M12 31 Q18 27 24 25 L30 17 H70 L76 25 Q82 27 88 31 Z" fill="#403a3a" ${O}/>
    <path d="M16 29.4 H84" ${N} stroke="${C.gold}" stroke-width="2.2"/>
    <path d="M40 29 Q44 21 50 21 Q56 21 60 29" ${N} stroke="${C.gold}" stroke-width="2.6"/>
    <path d="M44 17 L47 12 H53 L56 17 Z" fill="${C.gold}" ${T}/>`,
  // あしかがフラワーパーク — the wooden trellis under long hanging purple (and a few white) wisteria
  wisteria: `
    <rect x="12" y="20" width="7" height="70" fill="${C.wood}" ${O}/>
    <rect x="81" y="20" width="7" height="70" fill="${C.wood}" ${O}/>
    ${bunch(26, 18, 42, '#a98bd8', '#d7c6f0')}${bunch(38, 18, 56, '#9676cc', '#cdb9ee')}${bunch(50, 18, 46, C.white, '#e6dcf5')}
    ${bunch(62, 18, 58, '#a98bd8', '#d7c6f0')}${bunch(74, 18, 40, '#9676cc', '#cdb9ee')}
    <rect x="8" y="14" width="84" height="8" rx="2" fill="${C.wood}" ${O}/>
    <path d="M10 14 Q14 8 20 11 Q26 6 32 10 Q38 6 44 10 Q50 5 56 10 Q62 6 68 10 Q74 6 80 11 Q86 8 90 14 Z" fill="${C.green}" ${T}/>`,
  // 草津温泉 湯畑 — the wooden troughs of milky-green hot water under white steam, a wooden lantern beside
  yubatake: `
    <rect x="83.5" y="38" width="5" height="40" fill="${C.wood}" ${O}/>
    <rect x="80" y="26" width="12" height="13" fill="#fff4dc" ${O}/>
    <path d="M86 26 V39" ${N} ${T}/>
    <path d="M79 27 L86 20 L93 27 Z" fill="${C.roof}" ${O}/>
    ${line('M26 38 q-5 -6 0 -12 q5 -6 0 -12', C.white, 4)}${line('M44 36 q-5 -6 0 -12 q5 -6 0 -12', C.white, 4)}${line('M62 38 q-5 -6 0 -12 q5 -6 0 -12', C.white, 4)}
    <path d="M15 44 H72 L79 70 H8 Z" fill="${C.wood}" ${O}/>
    ${troughs.ch}
    <path d="M10 84 Q44 78 82 84 Q86 92 74 93 H20 Q6 92 10 84 Z" fill="#5fc9b0" ${O}/>
    ${troughs.falls}
    <rect x="7" y="69" width="74" height="7" rx="1.5" fill="${C.dwood}" ${O}/>`,
  // 伊香保温泉の石段街 · 金刀比羅宮 — the stone steps straight up, houses along both sides, a shrine at the top
  ishidan: `
    <path d="M30 90 L44 32 H56 L70 90 Z" fill="${C.stone}" ${O}/>
    <path d="${treads}" ${N} ${T}/>
    <rect x="8" y="70" width="22" height="20" fill="${C.cream}" ${O}/><path d="M7 71 L10 63 H30 L32 71 Z" fill="${C.roof}" ${O}/>
    <rect x="14" y="52" width="22" height="14" fill="${C.cream}" ${O}/><path d="M12 53 L16 46 H36 L38 53 Z" fill="${C.roof}" ${O}/>
    <rect x="70" y="70" width="22" height="20" fill="${C.cream}" ${O}/><path d="M68 71 L70 63 H90 L93 71 Z" fill="${C.roof}" ${O}/>
    <rect x="64" y="52" width="22" height="14" fill="${C.cream}" ${O}/><path d="M62 53 L64 46 H84 L88 53 Z" fill="${C.roof}" ${O}/>
    ${lit([12, 20], 76, 5, 7)}${lit([75, 83], 76, 5, 7)}${lit([19, 27], 56, 4, 6)}${lit([69, 77], 56, 4, 6)}
    <ellipse cx="29" cy="75" rx="3" ry="4" fill="${C.red}" ${T}/><ellipse cx="71" cy="75" rx="3" ry="4" fill="${C.red}" ${T}/>
    <rect x="42" y="20" width="16" height="12" fill="${C.verm}" ${O}/>
    <path d="M34 22 Q40 18 42 16 L46 10 H54 L58 16 Q60 18 66 22 Z" fill="${C.roof}" ${O}/>`,
  // 川越 時の鐘 — the tall dark-wood bell tower in three tiers with its bell at the top, a black kura beside it
  tokinokane: `
    <rect x="16" y="46" width="30" height="21" fill="#3f3a3a" ${O}/>
    <rect x="24" y="50" width="14" height="11" fill="${C.cream}" ${T}/><rect x="27.5" y="52.5" width="7" height="6" fill="${INK}"/>
    <path d="M12 48 L18 38 H44 L50 48 Z" fill="${C.roof}" ${O}/>
    <path d="M16 39 Q16 32.5 21 32.5 H41 Q46 32.5 46 39 Z" fill="${INK}"/>
    <rect x="18" y="68" width="26" height="20" fill="${C.dwood}" ${O}/>
    <path d="M24.5 70 V88 M31 70 V88 M37.5 70 V88" ${N} stroke="#6b5044" stroke-width="2.2"/>
    <path d="M13 71 L17 64 H45 L49 71 Z" fill="${C.roof}" ${O}/>
    <path d="M52 90 L56 80 H80 L84 90 Z" fill="${C.stone}" ${O}/>
    <rect x="58" y="58" width="20" height="22" fill="#7a5c48" ${O}/>
    <path d="M63 60 V80 M68 60 V80 M73 60 V80" ${N} stroke="#5f463a" stroke-width="2"/>
    <path d="M52 60 L58 53 H78 L84 60 Z" fill="${C.roof}" ${O}/>
    <rect x="60" y="40" width="16" height="13" fill="#7a5c48" ${O}/>
    <path d="M54 42 L60 35 H76 L82 42 Z" fill="${C.roof}" ${O}/>
    <rect x="60.5" y="22" width="15" height="13" fill="#5f463a" ${O}/>
    <path d="M63.5 25.5 Q63.5 23.5 68 23.5 Q72.5 23.5 72.5 25.5 L74 34 H62 Z" fill="#d4a94a" ${T}/>
    <path d="M55 24 Q61 17 68 13 Q75 17 81 24 Z" fill="${C.roof}" ${O}/>
    <path d="M68 13 V9" ${N} ${T}/>`,
  // 秩父の芝桜 — stripes of pink, magenta and white moss phlox across the slope, 武甲山 behind
  shibazakura: `
    <path d="M8 56 Q16 46 26 40 L40 22 Q44 18 50 19 L60 24 Q70 30 78 38 Q88 46 92 56 V64 H8 Z" fill="#6f8c73" ${O}/>
    <path d="M42 24 L50 21 L58 26 L62 38 Q52 42 40 38 Z" fill="#c3c7bd"/>
    <path d="M44 28 H56 M42 33 H59 M41 37.5 H61" ${N} stroke="#9aa196" stroke-width="2" stroke-linecap="round"/>
    <path d="M8 66 Q24 54 44 56 Q68 58 92 54 V80 Q92 90 80 92 H20 Q8 90 8 80 Z" fill="${C.green}" ${O}/>
    <path d="M22 62 Q34 58 48 61 Q62 64 80 59" ${N} stroke="#f7a6c0" stroke-width="3.8" stroke-linecap="round"/>
    <path d="M13 70 Q28 64 46 68 Q64 72 78 66 Q84 64 88 65" ${N} stroke="#e05a98" stroke-width="4.8" stroke-linecap="round"/>
    <path d="M12 78.5 Q28 72 46 77 Q64 82 78 75 Q84 72.5 88 73.5" ${N} stroke="${C.white}" stroke-width="6" stroke-linecap="round"/>
    <path d="M16 87 Q32 80 50 85 Q68 90 86 82" ${N} stroke="#f7a6c0" stroke-width="7" stroke-linecap="round"/>
    <path d="M16 60 V53" ${N} stroke="${C.dwood}" stroke-width="3"/><circle cx="16" cy="49" r="5.5" fill="${C.dgreen}" ${T}/>`,
};

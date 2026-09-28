// Landmark stickers, 南関東 · 中部 — the 기본 정보 観光 spots (ADR 0011, #93).
// Look-alikes drawn from memory in the mascot likenesses' hand — not photos, not official art.
import { C, INK, N, O, T, ground, line, torii, water } from './helpers';

const BLACK = '#3f3a3a';
const FUJI = '#7fa7d4';
const THATCH = '#b99a64';
const STRAW = '#e2c275';
const FUR = '#a38c78';
const FACE = '#ef9a92';
const PATINA = '#7d9f9a';
const FOREST = '#4f8a5b';

const r1 = (v: number) => +v.toFixed(1);

/** A cute eye — a dark dot with a white glint, as on the mascot likenesses. */
const eye = (x: number, y: number, r = 2.8) =>
  `<circle cx="${x}" cy="${y}" r="${r}" fill="${INK}"/><circle cx="${r1(x - r * 0.35)}" cy="${r1(y - r * 0.4)}" r="${r1(Math.max(0.9, r * 0.36))}" fill="#fff"/>`;
const cheek = (x: number, y: number, rx = 4, ry = 2.4) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#f5a3b3" opacity=".8"/>`;

/** 富士山 — the blue cone with its white cap: shoulders at y `s`, foot at y `foot`, half-width `hw` at the foot. */
function fujisan(x: number, s: number, foot: number, hw: number, fill: string = FUJI, edge: string = O, capEdge: string = T): string {
  const a = hw * 0.24, cy = s - hw * 0.19, ys = s + (foot - s) * 0.33, e = a + (hw - a) * 0.33, z = hw / 42;
  return (
    `<path d="M${r1(x - hw)} ${foot} L${r1(x - a)} ${s} Q${x} ${r1(cy)} ${r1(x + a)} ${s} L${r1(x + hw)} ${foot} Z" fill="${fill}" ${edge}/>` +
    `<path d="M${r1(x - e)} ${r1(ys)} L${r1(x - a)} ${s} Q${x} ${r1(cy)} ${r1(x + a)} ${s} L${r1(x + e)} ${r1(ys)} L${r1(x + e * 0.67)} ${r1(ys - 4 * z)} ` +
    `L${r1(x + e * 0.33)} ${r1(ys + 2 * z)} L${x} ${r1(ys - 5 * z)} L${r1(x - e * 0.33)} ${r1(ys + 2 * z)} L${r1(x - e * 0.67)} ${r1(ys - 4 * z)} Z" fill="${C.white}" ${capEdge}/>`
  );
}

/** A flat, bumpy pad of pine needles centred at (x, y), `w` wide. */
const pad = (x: number, y: number, w: number, h = 9, fill: string = C.dgreen) =>
  `<path d="M${r1(x - w / 2)} ${y} Q${r1(x - w / 2)} ${r1(y - h * 0.6)} ${r1(x - w / 3)} ${r1(y - h * 0.7)} Q${r1(x - w / 4)} ${r1(y - h * 1.1)} ${r1(x - w / 12)} ${r1(y - h * 0.85)} ` +
  `Q${r1(x + w / 12)} ${r1(y - h * 1.2)} ${r1(x + w / 4)} ${r1(y - h * 0.85)} Q${r1(x + w / 2)} ${r1(y - h * 0.9)} ${r1(x + w / 2)} ${y} Q${x} ${r1(y + h * 0.2)} ${r1(x - w / 2)} ${y} Z" fill="${fill}" ${O}/>`;

/** A pagoda roof: eave tips at L / R (turned up), eave line at y `e`, top at y `t`. */
const eave = (L: number, R: number, e: number, t: number, fill: string = C.roof) =>
  `<path d="M${L} ${e - 4} Q${L + 6} ${e - 4} ${L + 12} ${t} H${R - 12} Q${R - 6} ${e - 4} ${R} ${e - 4} Q${R - 3} ${e} ${R - 10} ${e} H${L + 10} Q${L + 3} ${e} ${L} ${e - 4} Z" fill="${fill}" ${O}/>`;

// 渋谷 — the crossing seen from a window above: ground (u, v ∈ 0..1) drawn as a trapezoid, far edge at the top.
const P = (u: number, v: number) => {
  const y = 38 + 52 * v, l = 20 - 12 * v, w = 60 + 24 * v;
  return `${r1(l + u * w)} ${r1(y)}`;
};
function zebra(u0: number, v0: number, u1: number, v1: number, n: number, h = 0.075): string {
  const du = u1 - u0, dv = v1 - v0, len = Math.hypot(du, dv), pu = (-dv / len) * h, pv = (du / len) * h;
  let d = '';
  for (let i = 0; i < n; i++) {
    const a = (i + 0.16) / n, b = (i + 0.84) / n;
    const au = u0 + du * a, av = v0 + dv * a, bu = u0 + du * b, bv = v0 + dv * b;
    d += `M${P(au + pu, av + pv)} L${P(bu + pu, bv + pv)} L${P(bu - pu, bv - pv)} L${P(au - pu, av - pv)} Z `;
  }
  return `<path d="${d.trim()}" fill="${C.white}"/>`;
}
const walker = (u: number, v: number, c: string) => {
  const [x, y] = P(u, v).split(' ');
  return `<circle cx="${x}" cy="${y}" r="2.8" fill="${c}" ${T}/>`;
};

export const artD: Record<string, string> = {
  // 鉄道博物館 — a black steam locomotive with red wheels and a puff of white smoke
  locomotive: `
    <path d="M8 86 H92" ${N} ${O}/>
    <path d="M22 28 Q13 27 15 19 Q17 11 27 13 Q31 5 41 8 Q50 4 55 12 Q63 13 61 21 Q60 28 51 27 Q45 32 37 28 Q29 32 22 28 Z" fill="${C.white}" ${O}/>
    <path d="M23 31 H35 V34 L33 35 V44 H25 V35 L23 34 Z" fill="${BLACK}" ${O}/>
    <path d="M41 44 Q41 35 47 35 Q53 35 53 44 Z" fill="${BLACK}" ${O}/>
    <rect x="15" y="43" width="51" height="22" rx="4" fill="${BLACK}" ${O}/>
    <path d="M30 44 V64 M58 44 V64" stroke="${C.gold}" stroke-width="2.4"/>
    <circle cx="19" cy="40" r="3.4" fill="${C.gold}" ${T}/>
    <rect x="62" y="31" width="24" height="35" fill="${BLACK}" ${O}/>
    <path d="M58 32 Q72 25 90 30 V34 H58 Z" fill="${BLACK}" ${O}/>
    <rect x="67" y="39" width="13" height="11" rx="2" fill="${C.gold}" ${T}/>
    <rect x="12" y="64" width="76" height="7" fill="${BLACK}" ${O}/>
    <path d="M8 83 L14 70 H21 V83 Z" fill="${C.red}" ${O}/>
    <circle cx="26" cy="80" r="6" fill="${C.red}" ${O}/><circle cx="41" cy="76" r="10" fill="${C.red}" ${O}/>
    <circle cx="61" cy="76" r="10" fill="${C.red}" ${O}/><circle cx="78" cy="79" r="7" fill="${C.red}" ${O}/>
    <g fill="${C.white}" ${T}><circle cx="41" cy="76" r="3"/><circle cx="61" cy="76" r="3"/></g>
    ${line('M41 76 H61', C.steel, 3)}`,

  // 成田山 · 法隆寺 — the five-storied pagoda: dark roofs, cream walls, the tall spire on top
  pagoda: `
    <path d="M18 90 L22 84 H78 L82 90 Z" fill="${C.stone}" ${O}/>
    ${[
      [35, 65, 72, 84, 10, 90, 74, 69.5],
      [37, 63, 59.5, 69.5, 15, 85, 61.5, 57],
      [39, 61, 47, 57, 20, 80, 49, 44.5],
      [41, 59, 34.5, 44.5, 25, 75, 36.5, 32],
      [43, 57, 22, 32, 30, 70, 24, 19.5],
    ].map(([wl = 0, wr = 0, wt = 0, wb = 0, L = 0, R = 0, e = 0, t = 0]) =>
      `<rect x="${wl}" y="${wt}" width="${wr - wl}" height="${wb - wt}" fill="${C.cream}" ${T}/>` +
      `<path d="M${r1(wl + (wr - wl) / 3)} ${wt} V${wb} M${r1(wr - (wr - wl) / 3)} ${wt} V${wb}" ${N} stroke="${C.dwood}" stroke-width="2.2"/>` + eave(L, R, e, t)).join('')}
    <rect x="45.5" y="16" width="9" height="4" fill="${INK}"/>
    <path d="M50 17 V8" ${N} stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/>
    <path d="M46 14.5 h8 M46.5 11.5 h7 M47 8.5 h6" ${N} stroke="${INK}" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="50" cy="5.5" r="2.4" fill="${C.gold}" ${T}/>`,

  // 鴨川シーワールド — an orca leaping out of the water: black back, white belly and eye patch
  orca: `
    ${water(74)}
    <path d="M12 80 L16 69 L22 77 L28 65 L33 76 L38 70 L38 80 Z" fill="${C.white}" ${T}/>
    <g transform="rotate(-26 50 50)">
      <path d="M31 49 L14 38 Q10 46 17 51 Q10 56 14 64 L31 53 Z" fill="${BLACK}" ${O}/>
      <path d="M52 36 Q50 24 44 13 Q58 19 66 35 Z" fill="${BLACK}" ${O}/>
      <path d="M88 50 Q88 35 68 34 Q48 33 30 47 L29 51 L30 54 Q48 66 68 65 Q88 64 88 50 Z" fill="${BLACK}" ${O}/>
      <path d="M87.5 52 Q82 62 67 62 Q54 62 44 57 Q58 58 68 57 Q80 56 87.5 52 Z" fill="${C.white}" ${T}/>
      <ellipse cx="72" cy="43" rx="6.5" ry="3.2" fill="${C.white}" transform="rotate(8 72 43)"/>
      <path d="M62 60 Q66 72 58 75 Q55 67 58 60 Z" fill="${BLACK}" ${O}/>
      ${eye(76.5, 44, 2.1)}
    </g>`,

  // 犬吠埼 — the white lighthouse on the dark rocks, the sun rising out of the sea
  lighthouse: `
    <path d="M10 60 A15 15 0 0 1 40 60 Z" fill="#f39a4b" ${O}/>
    <path d="M25 39 v-6 M12 47 l-5 -3 M38 47 l5 -3" ${N} stroke="#f39a4b" stroke-width="3.4" stroke-linecap="round"/>
    <path d="M8 60 H92 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <path d="M16 67 h18 M20 74 h10" ${N} stroke="#f7c46b" stroke-width="3" stroke-linecap="round"/>
    <path d="M52 70 L55 30 H67 L70 70 Z" fill="${C.white}" ${O}/>
    <rect x="59.5" y="40" width="3" height="5" rx="1" fill="${INK}"/><rect x="59.5" y="54" width="3" height="5" rx="1" fill="${INK}"/>
    <rect x="55" y="16" width="12" height="11" fill="${C.gold}" ${O}/>
    <path d="M61 17 V26" ${N} ${T}/>
    <rect x="51" y="26" width="20" height="4" rx="1" fill="${C.white}" ${O}/>
    <path d="M53 17 Q61 6 69 17 Z" fill="${BLACK}" ${O}/>
    <path d="M40 88 Q38 76 48 70 Q56 64 64 68 Q74 64 82 70 Q92 76 90 86 Q66 94 40 88 Z" fill="#7d726b" ${O}/>
    <path d="M36 82 q4 -6 8 -1 q3 -5 7 0 M84 80 q3 -5 6 -1" ${N} stroke="${C.white}" stroke-width="3.4" stroke-linecap="round"/>`,

  // 渋谷スクランブル交差点 — from above: the X of zebra stripes, people crossing, the big screen on the corner
  scramble: `
    <rect x="8" y="6" width="34" height="36" rx="2" fill="#cfe6f2" ${O}/>
    <rect x="12" y="10" width="26" height="19" rx="1.5" fill="#8fc3ea" ${T}/>
    <path d="M15 26 L22 17 L27 22 L30 19 L35 26 Z" fill="${C.pink}"/><circle cx="31" cy="15" r="2.4" fill="${C.gold}"/>
    <rect x="58" y="14" width="34" height="28" rx="2" fill="${C.cream}" ${O}/>
    <path d="M63 21 h6 M73 21 h6 M83 21 h4 M63 29 h6 M73 29 h6 M83 29 h4" stroke="${C.sky}" stroke-width="3" stroke-linecap="round"/>
    <path d="M${P(0, 0)} L${P(1, 0)} L${P(1, 1)} Q50 94 ${P(0, 1)} Z" fill="#77747c" ${O}/>
    ${zebra(0.07, 0.07, 0.93, 0.93, 6, 0.1)}${zebra(0.93, 0.07, 0.07, 0.93, 6, 0.1)}
    ${zebra(0.05, 0.24, 0.05, 0.76, 4, 0.04)}${zebra(0.95, 0.24, 0.95, 0.76, 4, 0.04)}${zebra(0.24, 0.955, 0.76, 0.955, 5, 0.035)}
    ${walker(0.3, 0.28, C.red)}${walker(0.7, 0.3, C.gold)}${walker(0.4, 0.66, '#8fc3ea')}${walker(0.76, 0.76, C.pink)}${walker(0.2, 0.8, '#b7e0a8')}${walker(0.56, 0.47, C.white)}`,

  // 明治神宮 · 熱田神宮 — the huge plain wooden torii in the deep forest, the gravel path
  kitorii: `
    <circle cx="17" cy="42" r="13" fill="${C.dgreen}" ${O}/><circle cx="83" cy="42" r="13" fill="${C.dgreen}" ${O}/>
    <circle cx="32" cy="28" r="15" fill="${FOREST}" ${O}/><circle cx="68" cy="28" r="15" fill="${FOREST}" ${O}/>
    <circle cx="50" cy="22" r="15" fill="${C.dgreen}" ${O}/>
    <rect x="6" y="40" width="88" height="40" rx="6" fill="${FOREST}" ${O}/>
    ${ground(80, '#e8e1d4')}
    <path d="M42 94 L46 78 H54 L58 94 Z" fill="#d6cdbd"/>
    ${torii('#d9b27c', 50, 26, 72, 60)}`,

  // 鎌倉の大仏 — the seated bronze Buddha, green with patina, eyes half closed, trees behind
  daibutsu: `
    <path d="M8 74 Q4 58 14 52 Q12 38 26 38 Q34 40 34 52 L30 74 Z" fill="${C.green}" ${O}/>
    <path d="M92 74 Q96 58 86 52 Q88 38 74 38 Q66 40 66 52 L70 74 Z" fill="${C.green}" ${O}/>
    <path d="M14 90 L18 82 H82 L86 90 Z" fill="${C.stone}" ${O}/>
    <path d="M18 84 Q14 70 26 64 Q30 52 38 48 Q44 46 50 46 Q56 46 62 48 Q70 52 74 64 Q86 70 82 84 Z" fill="${PATINA}" ${O}/>
    <path d="M22 82 Q26 70 50 70 Q74 70 78 82 M38 50 Q42 60 44 68 M62 50 Q58 60 56 68" ${N} stroke="#5f8a7c" stroke-width="2.4" stroke-linecap="round"/>
    <ellipse cx="50" cy="72" rx="10" ry="5" fill="${PATINA}" ${T}/>
    <ellipse cx="35" cy="37" rx="3.6" ry="9" fill="${PATINA}" ${T}/><ellipse cx="65" cy="37" rx="3.6" ry="9" fill="${PATINA}" ${T}/>
    <circle cx="50" cy="19" r="7" fill="${PATINA}" ${O}/>
    <circle cx="50" cy="33" r="15" fill="${PATINA}" ${O}/>
    <g fill="#5f8a7c"><circle cx="42" cy="23" r="1.8"/><circle cx="50" cy="21" r="1.8"/><circle cx="58" cy="23" r="1.8"/><circle cx="46" cy="16" r="1.8"/><circle cx="54" cy="16" r="1.8"/><circle cx="38" cy="28" r="1.8"/><circle cx="62" cy="28" r="1.8"/></g>
    <path d="M41 35 q3 2.6 6 0 M53 35 q3 2.6 6 0 M46.5 42 q3.5 2 7 0" ${N} stroke="${INK}" stroke-width="2.2" stroke-linecap="round"/>
    <circle cx="50" cy="30" r="1.5" fill="${INK}"/>`,

  // 江の島 — the green island and its Sea Candle tower, the long bridge from the shore
  enoshima: `
    <path d="M8 58 Q50 52 92 58 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <path d="M34 72 Q34 50 50 42 Q62 34 76 42 Q90 50 90 70 Q64 78 34 72 Z" fill="${C.green}" ${O}/>
    <path d="M42 58 q5 -7 12 -4 M72 52 q7 -2 11 5 M52 66 q6 -5 12 -2" ${N} stroke="${C.dgreen}" stroke-width="3" stroke-linecap="round"/>
    <rect x="61" y="22" width="6" height="18" fill="${C.white}" ${O}/>
    <path d="M54 16 H74 L71 24 H57 Z" fill="${C.sky}" ${O}/>
    <path d="M58 16 L64 7 L70 16 Z" fill="${C.white}" ${T}/>
    <circle cx="64" cy="12.5" r="2" fill="${C.gold}"/>
    <path d="M14 66 V73 M24 66 V73 M34 66 V73" ${N} ${O}/>
    <rect x="8" y="61" width="30" height="6" rx="1.5" fill="#ebe5dc" ${O}/>
    <path d="M20 82 q6 -3 12 0 M62 84 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,

  // 佐渡島 たらい舟 — the round tub boat, a woman in a sedge hat and blue kimono rowing
  taraibune: `
    ${water(68)}
    <ellipse cx="50" cy="60" rx="36" ry="10" fill="#a8744f" ${O}/>
    <path d="M30 62 Q30 42 44 40 Q58 40 60 62 Z" fill="#3f5f9a" ${O}/>
    <path d="M36 50 l3 3 M47 47 l3 3 M40 57 l3 3 M52 54 l3 3" ${N} stroke="${C.white}" stroke-width="2.2" stroke-linecap="round"/>
    <circle cx="45" cy="33" r="7.5" fill="#f6dcc4" ${T}/>
    ${cheek(40.5, 36.5, 2.4, 1.5)}${cheek(49.5, 36.5, 2.4, 1.5)}
    <path d="M43 38 q2 1.6 4 0" ${N} stroke="${INK}" stroke-width="2" stroke-linecap="round"/>
    <path d="M22 30 Q44 5 68 30 Q45 35 22 30 Z" fill="${STRAW}" ${O}/>
    <path d="M45 17 L34 30 M45 17 L56 31" ${N} stroke="#b89548" stroke-width="2"/>
    ${line('M28 42 L86 86', C.wood, 3.2)}
    <path d="M14 60 Q14 82 50 82 Q86 82 86 60 Q86 70 50 70 Q14 70 14 60 Z" fill="${C.wood}" ${O}/>
    <path d="M16 69 Q50 81 84 69" ${N} stroke="${STRAW}" stroke-width="3"/>
    <circle cx="39" cy="47" r="3.2" fill="#f6dcc4" ${T}/><circle cx="55" cy="59" r="3.2" fill="#f6dcc4" ${T}/>`,

  // 越後湯沢 — a pair of skis and poles stuck upright in the snow, snowflakes
  ski: `
    <path d="M8 62 L24 36 L34 46 L62 20 L92 56 V68 H8 Z" fill="#9fb4d4" ${O}/>
    <path d="M18 46 L24 36 L34 46 L62 20 L74 34 L66 32 L60 38 L52 33 L44 40 L36 36 L30 42 L24 40 Z" fill="${C.white}" ${T}/>
    <path d="M8 64 Q40 54 92 66 L90 86 Q50 94 10 86 Z" fill="${C.white}" ${O}/>
    <path d="M16 80 q8 -3 16 0 M66 82 q8 -3 16 0" ${N} stroke="#b9d6e8" stroke-width="2.6" stroke-linecap="round"/>
    ${line('M26 80 L70 20', C.navy, 2.6)}${line('M74 80 L30 20', C.navy, 2.6)}
    <path d="M25 72 l8 4 M75 72 l-8 4" ${N} ${O}/>
    ${[43, 57].map((x) => `
      <path d="M${x - 4} 78 V22 Q${x - 4} 12 ${x} 10 Q${x + 4} 12 ${x + 4} 22 V78 Z" fill="${C.red}" ${O}/>
      <path d="M${x} 20 V72" ${N} stroke="${C.white}" stroke-width="2.2"/>
      <rect x="${x - 4}" y="52" width="8" height="5" fill="${INK}"/>`).join('')}
    <path d="M34 78 q5 -5 10 -1 q6 -5 12 0 q5 -4 10 1 Z" fill="${C.white}" ${T}/>
    <path d="M16 12 v10 M11.7 14.5 l8.6 5 M11.7 19.5 l8.6 -5 M84 14 v10 M79.7 16.5 l8.6 5 M79.7 21.5 l8.6 -5" ${N} stroke="#8fc3ea" stroke-width="2.4" stroke-linecap="round"/>`,

  // 黒部ダム — the curved concrete arch dam between the mountains, the big white spray and a rainbow
  dam: `
    <path d="M24 26 Q50 12 76 26 Z" fill="${C.sea}" ${O}/>
    <path d="M8 90 V30 Q12 14 24 12 Q34 14 36 28 L40 76 L30 90 Z" fill="#7f9c70" ${O}/>
    <path d="M92 90 V30 Q88 14 76 12 Q66 14 64 28 L60 76 L70 90 Z" fill="#7f9c70" ${O}/>
    <path d="M28 26 Q50 18 72 26 L62 74 Q50 76 38 74 Z" fill="#d9d2c7" ${O}/>
    <path d="M29 30 Q50 22 71 30" ${N} stroke="#a8a096" stroke-width="2.4"/>
    <path d="M38 32 L42 72 M62 32 L58 72" ${N} stroke="#bdb4a8" stroke-width="2"/>
    ${water(80, '#7cc4c0')}
    <path d="M45 44 H55 Q60 54 68 62 Q78 72 70 80 Q60 86 50 82 Q40 86 30 80 Q22 72 32 62 Q40 54 45 44 Z" fill="${C.white}" ${T}/>
    <path d="M44 42 h12" ${N} stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/>
    <path d="M48 50 L42 66 M52 50 L58 66" ${N} stroke="${C.water}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M31 78 A19 19 0 0 1 69 78" ${N} stroke="${C.red}" stroke-width="2.6" opacity=".85"/>
    <path d="M33.6 78 A16.4 16.4 0 0 1 66.4 78" ${N} stroke="${C.gold}" stroke-width="2.6" opacity=".85"/>
    <path d="M36.2 78 A13.8 13.8 0 0 1 63.8 78" ${N} stroke="${C.sea}" stroke-width="2.6" opacity=".85"/>`,

  // 白川郷 · 五箇山 — the steep thatched gassho-zukuri house, little windows on the gable, rice fields
  gassho: `
    ${ground(78, C.green)}
    <path d="M22 84 h14 M44 87 h14 M66 84 h12" ${N} stroke="#b7e0a8" stroke-width="2.4" stroke-linecap="round"/>
    <rect x="24" y="68" width="52" height="12" fill="${C.cream}" ${O}/>
    <path d="M37 68 V80 M50 68 V80 M63 68 V80" ${N} ${T}/>
    <path d="M8 72 L50 8 L92 72 Q86 75 80 72 L50 24 L20 72 Q14 75 8 72 Z" fill="${THATCH}" ${O}/>
    <path d="M20 72 L50 24 L80 72 Z" fill="${C.dwood}" ${O}/>
    <path d="M47 38 h6 v6 h-6 Z M40 50 h6 v6 h-6 Z M54 50 h6 v6 h-6 Z M33 62 h6 v6 h-6 Z M47 62 h6 v6 h-6 Z M61 62 h6 v6 h-6 Z" fill="${C.cream}" ${T}/>
    <path d="M22 58 L36 36 M78 58 L64 36" ${N} stroke="#9a7c4c" stroke-width="2.2" stroke-linecap="round"/>`,

  // 兼六園 — the two-legged 徽軫灯籠 at the pond's edge, a pine under its 雪吊り rope cone
  kenrokuen: `
    <path d="M60 64 Q56 50 64 44 Q62 34 74 34 Q86 34 86 44 Q94 50 90 64 Z" fill="${C.dgreen}" ${O}/>
    <path d="M73 8 L58 60 M73 8 L64 62 M73 8 L71 63 M73 8 L78 63 M73 8 L84 62 M73 8 L90 60" ${N} stroke="${STRAW}" stroke-width="2.2"/>
    ${line('M73 7 V66', C.wood, 3)}
    ${water(70)}
    <path d="M44 76 Q44 66 54 64 Q64 64 66 74 Z" fill="#b9b1a7" ${O}/>
    ${line('M26 50 L16 84', C.stone, 5)}${line('M38 50 L50 66', C.stone, 5)}
    <rect x="16" y="45" width="28" height="6" rx="1.5" fill="${C.stone}" ${O}/>
    <rect x="22" y="34" width="16" height="11" fill="${C.stone}" ${O}/>
    <rect x="26" y="37" width="8" height="5" fill="${INK}"/>
    <path d="M6 37 Q8 31 17 28 Q30 20 43 28 Q52 31 54 37 Q30 40 6 37 Z" fill="${C.stone}" ${O}/>
    <ellipse cx="30" cy="20" rx="4" ry="4" fill="${C.stone}" ${O}/>`,

  // ひがし茶屋街 · 飛騨高山 — two-storey wooden houses with fine lattices, tiled eaves, stone paving
  machiya: `
    ${ground(80, C.stone)}
    <path d="M22 86 h10 M44 88 h12 M68 86 h10" ${N} ${T}/>
    <rect x="10" y="58" width="40" height="24" fill="#a8513f" ${O}/>
    <path d="M15 60 V82 M20 60 V82 M25 60 V82 M30 60 V82 M35 60 V82 M40 60 V82 M45 60 V82" stroke="#7a3a2e" stroke-width="2.2"/>
    <rect x="12" y="38" width="36" height="14" fill="#a8513f" ${O}/>
    <path d="M17 40 V52 M22 40 V52 M27 40 V52 M32 40 V52 M37 40 V52 M42 40 V52" stroke="#7a3a2e" stroke-width="2.2"/>
    <path d="M6 60 L12 51 H50 L53 60 Z" fill="#6b6a70" ${O}/>
    <path d="M8 40 L14 30 H48 L52 40 Z" fill="#6b6a70" ${O}/>
    <rect x="50" y="56" width="40" height="26" fill="#6f5446" ${O}/>
    <path d="M55 58 V82 M60 58 V82 M65 58 V82 M75 58 V82 M80 58 V82 M85 58 V82" stroke="#c9a57f" stroke-width="2.2"/>
    <rect x="67" y="62" width="6" height="20" fill="${C.cream}" ${T}/>
    <rect x="52" y="36" width="36" height="14" fill="#6f5446" ${O}/>
    <path d="M57 38 V50 M62 38 V50 M67 38 V50 M72 38 V50 M77 38 V50 M82 38 V50" stroke="#c9a57f" stroke-width="2.2"/>
    <path d="M47 58 L50 49 H90 L94 58 Z" fill="#6b6a70" ${O}/>
    <path d="M48 38 L52 28 H88 L92 38 Z" fill="#6b6a70" ${O}/>`,

  // 金沢21世紀美術館 — the low round white glass building on the lawn, colourful boxes rising from its roof
  kanazawa: `
    ${ground(74, C.green)}
    <path d="M10 56 V64 Q50 86 90 64 V56 Q50 78 10 56 Z" fill="#cfe6f2" ${O}/>
    <path d="M22 64 V71 M36 68 V76 M50 69 V78 M64 68 V76 M78 64 V71" ${N} stroke="#9cc4da" stroke-width="2.2"/>
    <ellipse cx="50" cy="56" rx="40" ry="11" fill="${C.white}" ${O}/>
    <rect x="22" y="40" width="13" height="16" fill="#f7a6c0" ${O}/>
    <rect x="39" y="28" width="14" height="28" fill="${C.white}" ${O}/>
    <rect x="57" y="36" width="12" height="18" fill="#8fc3ea" ${O}/>
    <rect x="72" y="44" width="10" height="11" fill="${C.gold}" ${O}/>`,

  // 東尋坊 · 伊豆 — the columnar basalt cliffs, waves breaking in white foam, a pine on top
  cliff: `
    <path d="M8 62 Q50 56 92 62 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    ${[
      [8, 36, '#9a8b7e'], [18, 30, '#8a7b6e'], [28, 28, '#9a8b7e'], [38, 32, '#8a7b6e'], [48, 40, '#9a8b7e'], [58, 52, '#8a7b6e'],
    ].map(([x = 0, top = 0, c = '']) => `<rect x="${x}" y="${top}" width="10" height="${84 - Number(top)}" fill="${c}" ${O}/>`).join('')}
    <path d="M13 44 V80 M23 36 V80 M33 34 V80 M43 38 V80 M53 46 V80" ${N} stroke="#7a6c60" stroke-width="2"/>
    <path d="M8 36 V33 Q14 29 22 31 Q30 26 40 29 Q46 31 48 37 Z" fill="${C.green}" ${T}/>
    ${line('M28 30 Q24 22 30 14', '#9a7358', 3.4)}
    ${pad(21, 23, 14, 7)}${pad(33, 15, 22, 8)}
    <path d="M60 82 Q58 62 74 56 Q90 54 91 68 Q84 62 78 64 Q72 68 76 74 Q70 80 60 82 Z" fill="${C.sea}" ${O}/>
    <path d="M66 60 Q76 52 88 58" ${N} stroke="${C.white}" stroke-width="3.4" stroke-linecap="round"/>
    <path d="M48 78 Q52 66 60 70 Q64 62 72 68 Q76 74 70 78 Q62 82 48 78 Z" fill="${C.white}" ${T}/>
    <path d="M24 86 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,

  // 福井県立恐竜博物館 — a happy green dinosaur: big head, tiny arms, and an egg
  dino: `
    <path d="M34 70 Q20 72 8 84 Q24 86 42 80 Z" fill="${C.green}" ${O}/>
    ${line('M42 78 V88 M58 78 V88', C.green, 7)}
    <path d="M30 70 Q28 50 42 44 L60 42 Q70 48 70 62 Q70 78 56 82 H42 Q32 80 30 70 Z" fill="${C.green}" ${O}/>
    <path d="M44 56 Q46 76 58 76 Q66 72 64 58 Z" fill="#e3f0c0" ${T}/>
    <path d="M48 44 Q42 24 56 16 Q66 10 80 14 Q92 18 90 30 Q90 40 78 42 Q66 44 58 48 Z" fill="${C.green}" ${O}/>
    ${line('M64 54 q4 2 6 -2', C.green, 3.4)}
    ${eye(68, 24, 3.2)}
    <path d="M66 34 Q76 40 86 30" ${N} ${T}/>
    ${cheek(64, 32, 3.6, 2.2)}
    <circle cx="86" cy="22" r="1.4" fill="${INK}"/>
    <g fill="${C.dgreen}"><circle cx="40" cy="54" r="2.4"/><circle cx="36" cy="64" r="2"/><circle cx="58" cy="22" r="2.2"/></g>
    <ellipse cx="82" cy="78" rx="9" ry="11" fill="${C.cream}" ${O}/>
    <g fill="${C.green}"><circle cx="79" cy="74" r="2"/><circle cx="85" cy="81" r="2"/></g>`,

  // 河口湖 — 逆さ富士: Mt. Fuji and its upside-down twin in the lake
  sakasafuji: `
    <path d="M9 50 H91 L89 80 Q50 94 11 80 Z" fill="${C.water}" ${O}/>
    <g transform="matrix(1 0 0 -1 0 100)" opacity=".7">${fujisan(50, 17, 50, 40, '#8fb0d8', 'stroke="none"', 'stroke="none"')}</g>
    ${fujisan(50, 17, 50, 40)}
    <path d="M6 53 Q10 46 17 49 Q23 44 30 48 Q36 45 42 50 H58 Q64 45 70 48 Q77 44 83 49 Q90 46 94 53 Q50 56 6 53 Z" fill="${C.dgreen}" ${O}/>
    <path d="M22 64 h14 M62 70 h14 M40 78 h12" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,

  // 忍野八海 — the clear spring pond (you can see the pebbles and a fish), a thatched hut, Fuji's snowy top
  oshino: `
    ${fujisan(42, 18, 50, 34)}
    <path d="M8 56 Q50 48 92 56 L90 84 Q50 94 10 84 Z" fill="${C.green}" ${O}/>
    <rect x="68" y="50" width="20" height="18" fill="${C.wood}" ${O}/>
    <rect x="75" y="56" width="7" height="12" fill="${C.dwood}" ${T}/>
    <path d="M60 52 L78 32 L94 52 Z" fill="${THATCH}" ${O}/>
    <ellipse cx="42" cy="72" rx="32" ry="14" fill="#8fdcec" ${O}/>
    <g fill="#c7e6de"><ellipse cx="28" cy="74" rx="4" ry="2.6"/><ellipse cx="52" cy="80" rx="4.4" ry="2.6"/><ellipse cx="60" cy="70" rx="3.4" ry="2.2"/><ellipse cx="36" cy="80" rx="3" ry="2"/></g>
    <path d="M36 68 Q42 63 48 68 Q42 73 36 68 Z M36 68 L31 65 V71 Z" fill="#f2a04b" ${T}/>`,

  // 松本城 — the black keep with white trim over its moat, the little red bridge, snowy Alps behind
  kurojo: `
    <path d="M8 60 L22 26 L34 42 L50 22 L66 40 L80 24 L92 60 Z" fill="#9fb4d4" ${O}/>
    <path d="M16 40 L22 26 L28 34 Z M74 38 L80 24 L86 36 Z" fill="${C.white}" ${T}/>
    ${water(70)}
    <path d="M10 71 L13 63 H31 L34 71 Z" fill="${C.stone}" ${O}/>
    <rect x="15" y="52" width="15" height="11" fill="${BLACK}" ${O}/><rect x="16.7" y="53.7" width="11.6" height="3" fill="${C.white}"/>
    <path d="M9 53 L14 47 H31 L36 53 Z" fill="#55595e" ${O}/>
    <path d="M30 71 L34 60 H66 L70 71 Z" fill="${C.stone}" ${O}/>
    <rect x="36" y="48" width="28" height="12" fill="${BLACK}" ${O}/><rect x="37.7" y="49.7" width="24.6" height="3" fill="${C.white}"/>
    <path d="M26 49 Q29 45 33 44 L37 40 H63 L67 44 Q71 45 74 49 Z" fill="#55595e" ${O}/>
    <rect x="40" y="32" width="20" height="8" fill="${BLACK}" ${O}/><rect x="41.7" y="33.7" width="16.6" height="3" fill="${C.white}"/>
    <path d="M31 33 Q34 29 37 28 L41 25 H59 L63 28 Q66 29 69 33 Z" fill="#55595e" ${O}/>
    <rect x="43" y="18" width="14" height="7" fill="${BLACK}" ${O}/><rect x="44.7" y="19.7" width="10.6" height="2.6" fill="${C.white}"/>
    <path d="M35 19 Q38 15 41 14 L44 11 H56 L59 14 Q62 15 65 19 Z" fill="#55595e" ${O}/>
    ${line('M52 76 Q68 64 86 76', C.red, 2.6)}
    <path d="M58 73 V78 M68 69.5 V75 M78 71 V77" ${N} stroke="${INK}" stroke-width="2.4" stroke-linecap="round"/>
    ${line('M50 82 Q68 70 88 82', C.red, 5)}`,

  // 高崎山自然動物園 — a Japanese macaque sitting: grey-brown fur, pink-red face and ears
  saru: `
    ${ground(80, C.green)}
    <path d="M24 86 Q18 64 32 54 Q40 50 50 50 Q60 50 68 54 Q82 64 76 86 Z" fill="${FUR}" ${O}/>
    <ellipse cx="50" cy="70" rx="10" ry="13" fill="#c9b8a6" ${T}/>
    <ellipse cx="33" cy="78" rx="8" ry="7" fill="${FUR}" ${O}/><ellipse cx="67" cy="78" rx="8" ry="7" fill="${FUR}" ${O}/>
    <ellipse cx="36" cy="72" rx="4" ry="3" fill="${FACE}" ${T}/><ellipse cx="64" cy="72" rx="4" ry="3" fill="${FACE}" ${T}/>
    <ellipse cx="40" cy="86" rx="5" ry="2.6" fill="${FACE}" ${T}/><ellipse cx="60" cy="86" rx="5" ry="2.6" fill="${FACE}" ${T}/>
    <circle cx="28" cy="34" r="6" fill="${FACE}" ${O}/><circle cx="72" cy="34" r="6" fill="${FACE}" ${O}/>
    <circle cx="50" cy="34" r="21" fill="${FUR}" ${O}/>
    <path d="M42 15 L46 10 L50 14 L54 10 L58 15" fill="${FUR}" ${T}/>
    <path d="M50 28 Q56 22 62 26 Q68 32 64 42 Q58 50 50 50 Q42 50 36 42 Q32 32 38 26 Q44 22 50 28 Z" fill="${FACE}" ${T}/>
    ${eye(44, 36, 2.6)}${eye(56, 36, 2.6)}
    <path d="M48 42 h.1 M52 42 h.1" ${N} stroke="${INK}" stroke-width="2" stroke-linecap="round"/>
    <path d="M46 46 q4 2.6 8 0" ${N} stroke="${INK}" stroke-width="2" stroke-linecap="round"/>`,

  // 地獄谷野猿公苑 — a snow monkey soaking in the steaming hot spring, snow on its head
  jigokudani: `
    <path d="M18 52 q-6 -7 0 -14 q6 -7 0 -14 M82 52 q-6 -7 0 -14 q6 -7 0 -14 M30 22 q-5 -6 0 -12 M70 22 q-5 -6 0 -12" ${N} stroke="#b9c6cf" stroke-width="4" stroke-linecap="round"/>
    <path d="M8 74 Q6 58 18 54 Q30 52 32 64 L30 80 Z" fill="#9a948e" ${O}/>
    <path d="M92 74 Q94 58 82 54 Q70 52 68 64 L70 80 Z" fill="#9a948e" ${O}/>
    <path d="M10 60 Q16 52 26 55 Q30 58 30 62 Q20 58 10 60 Z M90 60 Q84 52 74 55 Q70 58 70 62 Q80 58 90 60 Z" fill="${C.white}" ${T}/>
    <path d="M10 68 Q50 60 90 68 Q94 80 82 86 Q50 94 18 86 Q6 80 10 68 Z" fill="#9fd3e0" ${O}/>
    <path d="M32 70 Q32 56 50 56 Q68 56 68 70 Z" fill="${FUR}" ${O}/>
    <circle cx="33" cy="42" r="5" fill="${FACE}" ${O}/><circle cx="67" cy="42" r="5" fill="${FACE}" ${O}/>
    <circle cx="50" cy="42" r="17" fill="${FUR}" ${O}/>
    <path d="M50 38 Q55 33 60 36 Q65 41 61 49 Q56 55 50 55 Q44 55 39 49 Q35 41 40 36 Q45 33 50 38 Z" fill="${FACE}" ${T}/>
    <path d="M41 44 q3 -3 6 0 M53 44 q3 -3 6 0 M46 50 q4 2.4 8 0" ${N} stroke="${INK}" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M37 32 Q40 22 50 22 Q60 22 63 32 Q57 29 50 31 Q43 29 37 32 Z" fill="${C.white}" ${T}/>
    <path d="M30 70 Q50 76 70 70" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,

  // 上高地 河童橋 — the wooden suspension bridge over the clear river, the jagged snowy Hotaka peaks
  kappabashi: `
    <path d="M8 52 L18 32 L24 38 L32 18 L40 30 L48 14 L56 28 L64 16 L72 30 L80 22 L92 46 V56 H8 Z" fill="#8d9bb0" ${O}/>
    <path d="M28 28 L32 18 L36 24 Z M44 22 L48 14 L52 21 Z M60 23 L64 16 L68 24 Z" fill="${C.white}" ${T}/>
    ${[14, 86].map((x) => `<path d="M${x} 24 L${x + 6} 38 H${x + 3} L${x + 9} 52 H${x + 5} L${x + 10} 68 H${x - 10} L${x - 5} 52 H${x - 9} L${x - 3} 38 H${x - 6} Z" fill="#7fae6a" ${O}/>`).join('')}
    <path d="M8 64 Q50 58 92 64 L90 84 Q50 94 10 84 Z" fill="#7cc4c0" ${O}/>
    <path d="M24 78 q6 -3 12 0 M62 81 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M22 44 Q50 70 78 44" ${N} stroke="${INK}" stroke-width="3"/>
    <path d="M32 52.5 V60 M41 55.5 V60 M50 57 V60 M59 55.5 V60 M68 52.5 V60" ${N} ${T}/>
    <path d="M19 62 V42 M25 62 V42 M75 62 V42 M81 62 V42" ${N} stroke="${INK}" stroke-width="7.4" stroke-linecap="round"/>
    <path d="M19 62 V42 M25 62 V42 M75 62 V42 M81 62 V42" ${N} stroke="${C.wood}" stroke-width="4" stroke-linecap="round"/>
    <path d="M17 44 H27 M73 44 H83" ${N} ${O}/>
    <rect x="8" y="58" width="84" height="7" rx="2.5" fill="${C.wood}" ${O}/>`,

  // 軽井沢 — the little wooden chapel with its steep roof and bell tower among the larches
  church: `
    <path d="M8 80 L17 20 L26 80 Z M74 80 L83 20 L92 80 Z" fill="#7fae6a" ${O}/>
    ${ground(80, C.green)}
    <rect x="30" y="52" width="34" height="30" fill="${C.white}" ${O}/>
    <path d="M30 60 H64 M40 52 V82 M54 52 V82" ${N} stroke="${C.dwood}" stroke-width="2.2"/>
    <path d="M26 54 L47 22 L68 54 Z" fill="#6b5a52" ${O}/>
    <path d="M43 82 V72 Q47 66 51 72 V82 Z" fill="${C.dwood}" ${T}/>
    <rect x="62" y="36" width="12" height="46" fill="${C.white}" ${O}/>
    <path d="M65 42 H71 V50 H65 Z" fill="${INK}"/><circle cx="68" cy="47" r="2" fill="${C.gold}"/>
    <path d="M60 37 L68 18 L76 37 Z" fill="#6b5a52" ${O}/>
    <path d="M68 18 V7 M64 11 H72" ${N} ${O}/>`,

  // 長良川の鵜飼 — at night: the long boat, the blazing fire basket at the bow, a cormorant in the water
  ukai: `
    <rect x="8" y="10" width="84" height="80" rx="14" fill="${C.navy}" ${O}/>
    <path d="M9.7 60 H90.3 V76 Q90.3 88.3 78 88.3 H22 Q9.7 88.3 9.7 76 Z" fill="#26304f"/>
    <path d="M20 17 a8 8 0 1 0 8 10 a6.5 6.5 0 1 1 -8 -10 Z" fill="${C.gold}" ${T}/>
    <circle cx="74" cy="34" r="19" fill="#f39a4b" opacity=".3"/>
    <ellipse cx="72" cy="73" rx="16" ry="6.5" fill="#f39a4b" opacity=".55"/>
    <path d="M60 66 q6 -2 12 0 M72 82 q5 -2 10 0" ${N} stroke="${C.gold}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M10 58 H64 Q70 58 74 52 L72 64 H16 Q10 64 10 58 Z" fill="${C.wood}" ${O}/>
    ${line('M64 58 L74 44', C.dwood, 2.6)}
    <path d="M64 42 H84 L81 52 H67 Z" fill="${BLACK}" ${O}/>
    <path d="M70 43 V51 M74 43 V51 M78 43 V51" ${N} stroke="#8a7d74" stroke-width="2"/>
    <path d="M63 42 Q58 28 68 12 Q70 22 74 16 Q78 22 80 18 Q90 30 85 42 Z" fill="#f39a4b" ${O}/>
    <path d="M68 42 Q65 32 70 24 Q72 30 75 26 Q81 34 80 42 Z" fill="${C.gold}"/>
    <g fill="${C.gold}"><circle cx="60" cy="18" r="1.8"/><circle cx="88" cy="24" r="1.8"/><circle cx="84" cy="12" r="1.5"/></g>
    <circle cx="50" cy="33" r="5" fill="#f6dcc4" ${T}/>
    <path d="M45 31 Q50 22 56 30 Z" fill="${BLACK}" ${T}/>
    <path d="M44 48 Q44 38 50 38 Q56 38 56 48 Z" fill="#3f5f9a" ${T}/>
    <path d="M43 46 H57 L59 58 H41 Z" fill="${STRAW}" ${T}/>
    <path d="M46 49 V57 M50 49 V57 M54 49 V57" ${N} stroke="#b89548" stroke-width="2"/>
    <path d="M56 44 Q64 58 69 69" ${N} stroke="${STRAW}" stroke-width="2"/>
    <ellipse cx="68" cy="74" rx="9" ry="4.4" fill="#1f1f24" ${T}/>
    ${line('M74 73 Q79 66 75 62', '#1f1f24', 3.6)}
    <path d="M76 60 l7 2 l-6 2 Z" fill="${C.gold}" ${T}/>
    <circle cx="74.5" cy="62" r="1.6" fill="${C.white}"/>`,

  // 三保松原 — the twisted pines on the sandy beach, Mt. Fuji across the sea
  matsubara: `
    ${fujisan(54, 22, 52, 36)}
    <path d="M8 52 Q50 48 92 52 V66 H8 Z" fill="${C.sea}" ${O}/>
    <path d="M40 58 h10 M64 59 h10" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M8 64 Q50 58 92 64 L90 84 Q50 94 10 84 Z" fill="${C.sand}" ${O}/>
    ${line('M20 88 Q14 70 26 56 Q32 48 28 40 M26 56 Q18 54 14 50 M29 50 Q36 50 40 46', '#9a7358', 4)}
    ${pad(14, 52, 18, 8)}${pad(40, 48, 20, 8)}${pad(27, 38, 32, 11)}
    ${line('M82 88 Q88 74 78 62 Q72 56 76 48 M78 62 Q86 62 88 58', '#9a7358', 4)}
    ${pad(87, 60, 12, 7)}${pad(74, 48, 28, 10)}`,

  // 名古屋城 — the keep under copper-green roofs, with its big golden shachihoko on top
  nagoyajo: `
    <path d="M16 90 L23 78 H77 L84 90 Z" fill="${C.stone}" ${O}/>
    <path d="M30 84 h14 M52 87 h16" ${N} ${T}/>
    <rect x="28" y="66" width="44" height="12" fill="${C.white}" ${O}/>
    <path d="M37 71.5 h5 M47.5 71.5 h5 M58 71.5 h5" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>
    <path d="M15 67 Q18 62 24 60 L30 55 H70 L76 60 Q82 62 85 67 Z" fill="${C.teal}" ${O}/>
    <path d="M42 60 L50 52 L58 60 Z" fill="${C.teal}" ${O}/>
    <rect x="33" y="46" width="34" height="9" fill="${C.white}" ${O}/>
    <path d="M23 47 Q26 43 31 41 L36 37 H64 L69 41 Q74 43 77 47 Z" fill="${C.teal}" ${O}/>
    <rect x="38" y="31" width="24" height="6" fill="${C.white}" ${O}/>
    <path d="M30 32 Q33 28 37 27 L41 24 H59 L63 27 Q67 28 70 32 Z" fill="${C.teal}" ${O}/>
    ${[1, -1].map((s) => `<g transform="matrix(${s} 0 0 1 ${s === 1 ? 0 : 100} 0)">
      <path d="M49 25 Q49 17 43 13 Q39 10 40 6 L34 9 L28 6 Q31 12 33 14 Q32 21 38 25 Q43 28 49 25 Z" fill="${C.gold}" ${O}/>
      <path d="M34.5 19 l-4 -1 M35 15 l-3.6 -2" ${N} stroke="${INK}" stroke-width="2.2" stroke-linecap="round"/>
      <path d="M49 22.5 q-3 1 -5 -1" ${N} stroke="${INK}" stroke-width="2" stroke-linecap="round"/>
      <circle cx="43.5" cy="18.5" r="1.6" fill="${INK}"/></g>`).join('')}`,
};

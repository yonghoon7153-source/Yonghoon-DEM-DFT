// Original kawaii mascots, one per prefecture that has one (see data/mascots.json).
// Each is a self-contained 100×100 SVG string. Style: round shapes, dot eyes, rosy cheeks,
// warm brown outline. Keep new characters in the same style so the sticker book feels like a set.

const INK = '#5a4a44';
const S = `stroke="${INK}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"`;
const THIN = `stroke="${INK}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"`;

type Mouth = 'smile' | 'w' | 'o' | 'grin' | 'flat';

function face(cx: number, cy: number, o: { gap?: number; mouth?: Mouth; blush?: boolean; blushDy?: number; eyeR?: number; sclera?: boolean } = {}): string {
  const gap = o.gap ?? 9;
  const r = o.eyeR ?? 2.7;
  const eye = (x: number) =>
    `${o.sclera ? `<circle cx="${x}" cy="${cy}" r="${r + 2.4}" fill="#fff"/>` : ''}<circle cx="${x}" cy="${cy}" r="${r}" fill="${INK}"/><circle cx="${x - 0.9}" cy="${cy - 1}" r="${r * 0.36}" fill="#fff"/>`;
  const my = cy + 7;
  const mouths: Record<Mouth, string> = {
    smile: `<path d="M${cx - 4} ${my} q4 3.5 8 0" fill="none" ${THIN}/>`,
    w: `<path d="M${cx - 5} ${my - 1} q2.5 3.5 5 0 q2.5 3.5 5 0" fill="none" ${THIN}/>`,
    o: `<ellipse cx="${cx}" cy="${my + 0.5}" rx="2.4" ry="3" fill="${INK}"/>`,
    grin: `<path d="M${cx - 7} ${my - 1} q7 9 14 0 z" fill="#c9525a" ${THIN}/>`,
    flat: `<path d="M${cx - 3.5} ${my} h7" fill="none" ${THIN}/>`,
  };
  const blush = o.blush === false ? '' : `<ellipse cx="${cx - gap - 6}" cy="${cy + (o.blushDy ?? 5)}" rx="4.6" ry="2.6" fill="#f5a3b3" opacity=".72"/><ellipse cx="${cx + gap + 6}" cy="${cy + (o.blushDy ?? 5)}" rx="4.6" ry="2.6" fill="#f5a3b3" opacity=".72"/>`;
  return eye(cx - gap) + eye(cx + gap) + mouths[o.mouth ?? 'smile'] + blush;
}

function svg(inner: string): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100" role="img">${inner}</svg>`;
}

export const mascotArt: Record<string, string> = {
  // 北海道 — seal on an ice floe
  azarashi: svg(`
    <rect x="12" y="76" width="76" height="14" rx="7" fill="#dceefb" ${S}/>
    <path d="M78 60 q14 -6 12 -18 q-6 6 -10 4" fill="#eef1f4" ${S}/>
    <ellipse cx="48" cy="60" rx="30" ry="22" fill="#f3f5f7" ${S}/>
    <ellipse cx="30" cy="78" rx="9" ry="4" fill="#e6eaee" ${S}/>
    <ellipse cx="62" cy="79" rx="9" ry="4" fill="#e6eaee" ${S}/>
    ${face(46, 55, { gap: 9, mouth: 'w', blushDy: 6 })}
    <ellipse cx="46" cy="61" rx="2.6" ry="1.8" fill="${INK}"/>
    <path d="M28 60 h9 M28 64 h9 M55 60 h9 M55 64 h9" fill="none" ${THIN} opacity=".7"/>
    <path d="M80 18 v10 M75 23 h10 M76.5 19.5 l7 7 M83.5 19.5 l-7 7" fill="none" stroke="#9ec6e6" stroke-width="1.6" stroke-linecap="round"/>
  `),
  // 青森 — apple
  ringo: svg(`
    <path d="M50 24 v-9" fill="none" stroke="#7a5230" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="60" cy="19" rx="9" ry="4.5" transform="rotate(-28 60 19)" fill="#8fc47b" ${S}/>
    <path d="M50 30 C38 22 20 30 20 54 C20 74 34 88 50 86 C66 88 80 74 80 54 C80 30 62 22 50 30 Z" fill="#f26d6d" ${S}/>
    <ellipse cx="34" cy="44" rx="4" ry="7" transform="rotate(20 34 44)" fill="#fff" opacity=".55"/>
    ${face(50, 56, { gap: 10, mouth: 'smile' })}
  `),
  // 秋田 — a tiny, friendly namahage
  namahage: svg(`
    <path d="M20 90 L32 56 H68 L80 90 Z" fill="#e8d5a3" ${S}/>
    <path d="M38 62 v24 M50 60 v28 M62 62 v24" fill="none" stroke="#c9b27a" stroke-width="2" stroke-linecap="round"/>
    <path d="M40 30 L34 12 L46 26 Z M60 30 L66 12 L54 26 Z" fill="#f2c94c" ${S}/>
    <circle cx="50" cy="46" r="23" fill="#e0554b" ${S}/>
    <path d="M28 40 Q34 20 50 26 Q66 20 72 40 Q60 30 50 34 Q40 30 28 40 Z" fill="#fff" ${S}/>
    <path d="M36 42 l8 3 M64 42 l-8 3" fill="none" ${THIN}/>
    ${face(50, 48, { gap: 9, mouth: 'grin', blushDy: 6 })}
    <path d="M45 54 l2 4 l2 -4 M51 54 l2 4 l2 -4" fill="#fff" ${THIN}/>
  `),
  // 宮城 — zunda mochi
  zunda: svg(`
    <rect x="16" y="80" width="68" height="9" rx="4.5" fill="#fff" ${S}/>
    <path d="M22 62 C22 42 40 36 50 38 C62 36 78 44 78 62 C78 78 62 84 50 84 C36 84 22 78 22 62 Z" fill="#c9e6a7" ${S}/>
    <path d="M30 56 C34 46 44 42 52 44" fill="none" stroke="#e5f3d2" stroke-width="4" stroke-linecap="round"/>
    <circle cx="66" cy="70" r="2" fill="#9cc47c"/><circle cx="34" cy="72" r="1.6" fill="#9cc47c"/><circle cx="70" cy="56" r="1.6" fill="#9cc47c"/>
    ${face(50, 60, { gap: 9, mouth: 'w' })}
  `),
  // 東京 — Hachi, the loyal dog
  hachi: svg(`
    <path d="M30 40 L34 12 L50 32 Z M70 40 L66 12 L50 32 Z" fill="#dcae74" ${S}/>
    <path d="M35 34 L36 20 L46 31 Z M65 34 L64 20 L54 31 Z" fill="#f3d2ad"/>
    <circle cx="50" cy="52" r="26" fill="#dcae74" ${S}/>
    <path d="M26 58 Q34 44 50 46 Q66 44 74 58 Q74 78 50 78 Q26 78 26 58 Z" fill="#f8efdf"/>
    <path d="M78 66 q14 -6 8 -18 q-4 6 -10 5" fill="#dcae74" ${S}/>
    ${face(50, 52, { gap: 10, mouth: 'w' })}
    <ellipse cx="50" cy="59" rx="3" ry="2.2" fill="${INK}"/>
    <path d="M30 74 Q50 86 70 74 L72 84 Q50 96 28 84 Z" fill="#e5708d" ${S}/>
  `),
  // 新潟 — onigiri
  onigiri: svg(`
    <path d="M50 16 Q55 16 58 22 L85 68 Q88 76 80 78 L20 78 Q12 76 15 68 L42 22 Q45 16 50 16 Z" fill="#fff" ${S}/>
    <rect x="35" y="56" width="30" height="22" rx="3" fill="#3a3a3a" ${S}/>
    <circle cx="30" cy="66" r="1.3" fill="#8b6b4a"/><circle cx="70" cy="60" r="1.3" fill="#8b6b4a"/><circle cx="36" cy="46" r="1.3" fill="#8b6b4a"/>
    ${face(50, 44, { gap: 9, mouth: 'smile' })}
  `),
  // 山梨 — grapes
  budou: svg(`
    <path d="M52 30 v-10" fill="none" stroke="#7a5230" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="62" cy="22" rx="10" ry="5" transform="rotate(-20 62 22)" fill="#8fc47b" ${S}/>
    <g fill="#b9a1e3" ${S}>
      <circle cx="38" cy="42" r="10"/><circle cx="66" cy="42" r="10"/><circle cx="52" cy="38" r="10"/>
      <circle cx="31" cy="60" r="10"/><circle cx="73" cy="60" r="10"/>
      <circle cx="45" cy="56" r="11"/><circle cx="59" cy="56" r="11"/>
      <circle cx="40" cy="73" r="10"/><circle cx="64" cy="73" r="10"/>
      <circle cx="52" cy="84" r="9"/>
    </g>
    <circle cx="41" cy="52" r="2.4" fill="#fff" opacity=".6"/><circle cx="55" cy="52" r="2.4" fill="#fff" opacity=".6"/>
    ${face(52, 58, { gap: 7, mouth: 'smile', blush: false })}
    <ellipse cx="36" cy="64" rx="3.6" ry="2.2" fill="#f5a3b3" opacity=".8"/><ellipse cx="68" cy="64" rx="3.6" ry="2.2" fill="#f5a3b3" opacity=".8"/>
  `),
  // 長野 — snow monkey in an onsen
  saru: svg(`
    <path d="M34 26 q4 -8 0 -14 M50 22 q4 -8 0 -14 M66 26 q4 -8 0 -14" fill="none" stroke="#cbd5dd" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="30" cy="58" r="7" fill="#b98a63" ${S}/><circle cx="70" cy="58" r="7" fill="#b98a63" ${S}/>
    <circle cx="30" cy="58" r="3.2" fill="#f4c3b0"/><circle cx="70" cy="58" r="3.2" fill="#f4c3b0"/>
    <circle cx="50" cy="60" r="24" fill="#b98a63" ${S}/>
    <path d="M30 44 Q40 30 50 36 Q60 30 70 44 Q60 40 50 42 Q40 40 30 44 Z" fill="#fff" ${S}/>
    <ellipse cx="50" cy="60" rx="16" ry="13" fill="#f4c3b0"/>
    ${face(50, 57, { gap: 7, mouth: 'smile', blushDy: 6 })}
    <circle cx="48.5" cy="63" r="1" fill="${INK}"/><circle cx="51.5" cy="63" r="1" fill="${INK}"/>
    <ellipse cx="50" cy="84" rx="40" ry="10" fill="#bfdcec" ${S}/>
    <path d="M22 84 q10 -4 20 0 q10 4 20 0 q10 -4 16 0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".8"/>
  `),
  // 静岡 — Mt. Fuji
  fujisan: svg(`
    <ellipse cx="24" cy="40" rx="9" ry="5" fill="#fff" ${S}/><ellipse cx="32" cy="36" rx="7" ry="4.5" fill="#fff" ${S}/><ellipse cx="18" cy="37" rx="6" ry="4" fill="#fff" ${S}/>
    <path d="M50 20 L90 86 H10 Z" fill="#8fb4dd" ${S}/>
    <path d="M50 20 L69 52 Q64 46 60 54 Q55 45 50 54 Q45 45 40 54 Q36 46 31 52 Z" fill="#fff" ${S}/>
    ${face(50, 66, { gap: 9, mouth: 'smile' })}
  `),
  // 京都 — Inari fox
  kitsune: svg(`
    <path d="M74 70 q20 -8 14 -26 q-8 10 -16 12" fill="#fff8f0" ${S}/>
    <path d="M30 40 L24 12 L48 30 Z M70 40 L76 12 L52 30 Z" fill="#fff8f0" ${S}/>
    <path d="M32 36 L29 20 L43 31 Z M68 36 L71 20 L57 31 Z" fill="#f0a0a0"/>
    <circle cx="50" cy="54" r="24" fill="#fff8f0" ${S}/>
    <path d="M33 44 l6 6 M67 44 l-6 6" fill="none" stroke="#e0554b" stroke-width="2.6" stroke-linecap="round"/>
    ${face(50, 54, { gap: 10, mouth: 'w', blushDy: 6 })}
    <ellipse cx="50" cy="61" rx="2.4" ry="1.8" fill="${INK}"/>
    <path d="M34 76 Q50 84 66 76 L68 86 Q50 94 32 86 Z" fill="#e0554b" ${S}/>
  `),
  // 大阪 — takoyaki
  takoyaki: svg(`
    <path d="M62 34 q8 -14 16 -2" fill="none" stroke="#e5748a" stroke-width="5" stroke-linecap="round"/>
    <circle cx="50" cy="58" r="27" fill="#d8a15c" ${S}/>
    <path d="M25 50 Q50 62 75 50 Q78 66 50 72 Q22 66 25 50 Z" fill="#8a4b25"/>
    <path d="M30 60 q10 4 20 0 q10 -4 20 0" fill="none" stroke="#fff6dc" stroke-width="2" stroke-linecap="round" opacity=".9"/>
    <circle cx="36" cy="44" r="1.6" fill="#5c8a3c"/><circle cx="62" cy="40" r="1.6" fill="#5c8a3c"/><circle cx="48" cy="38" r="1.4" fill="#5c8a3c"/>
    <path d="M40 34 l4 -3 M56 32 l4 -2" fill="none" stroke="#c98b52" stroke-width="2"/>
    ${face(50, 60, { gap: 9, mouth: 'smile', sclera: true, blushDy: 6 })}
  `),
  // 奈良 — deer with a senbei
  shika: svg(`
    <path d="M36 34 q-4 -12 -12 -14 M36 34 q-2 -12 2 -18 M64 34 q4 -12 12 -14 M64 34 q2 -12 -2 -18" fill="none" stroke="#8b6b4a" stroke-width="3.2" stroke-linecap="round"/>
    <ellipse cx="26" cy="50" rx="9" ry="5" transform="rotate(-20 26 50)" fill="#d8a874" ${S}/><ellipse cx="74" cy="50" rx="9" ry="5" transform="rotate(20 74 50)" fill="#d8a874" ${S}/>
    <circle cx="50" cy="56" r="24" fill="#d8a874" ${S}/>
    <circle cx="36" cy="68" r="1.8" fill="#fff"/><circle cx="64" cy="68" r="1.8" fill="#fff"/><circle cx="43" cy="75" r="1.5" fill="#fff"/><circle cx="57" cy="75" r="1.5" fill="#fff"/>
    ${face(50, 54, { gap: 10, mouth: 'w', blushDy: 6 })}
    <ellipse cx="50" cy="62" rx="3" ry="2.2" fill="${INK}"/>
    <circle cx="50" cy="86" r="10" fill="#e9c79a" ${S}/>
    <path d="M44 86 h12 M50 80 v12" fill="none" stroke="#d9b07c" stroke-width="1.5"/>
    <ellipse cx="38" cy="84" rx="5" ry="3.5" fill="#d8a874" ${S}/><ellipse cx="62" cy="84" rx="5" ry="3.5" fill="#d8a874" ${S}/>
  `),
  // 鳥取 — camel on the dunes
  rakuda: svg(`
    <ellipse cx="50" cy="88" rx="44" ry="7" fill="#f0dfb0"/>
    <circle cx="58" cy="50" r="13" fill="#e3bf85" ${S}/>
    <rect x="28" y="52" width="54" height="30" rx="15" fill="#e3bf85" ${S}/>
    <rect x="36" y="78" width="7" height="10" rx="3" fill="#d6ad70" ${S}/><rect x="50" y="78" width="7" height="10" rx="3" fill="#d6ad70" ${S}/><rect x="64" y="78" width="7" height="10" rx="3" fill="#d6ad70" ${S}/>
    <path d="M80 66 q10 4 8 14" fill="none" ${S}/>
    <path d="M30 56 q-6 -10 -2 -18" fill="none" stroke="#e3bf85" stroke-width="10" stroke-linecap="round"/><path d="M30 56 q-6 -10 -2 -18" fill="none" ${S} stroke-width="0"/>
    <circle cx="27" cy="36" r="13" fill="#e3bf85" ${S}/>
    <ellipse cx="20" cy="26" rx="3" ry="5" fill="#d6ad70" ${S}/>
    ${face(26, 36, { gap: 5, mouth: 'smile', blushDy: 5, eyeR: 2.3 })}
  `),
  // 広島 — momiji manju
  momiji: svg(`
    <path d="M50 14 L57 36 L78 28 L66 48 L86 60 L62 60 L54 88 L46 88 L38 60 L14 60 L34 48 L22 28 L43 36 Z" fill="#d9a066" ${S}/>
    <path d="M50 24 L55 40 L68 36 L60 48 L72 56 L58 56 L52 74 L48 74 L42 56 L28 56 L40 48 L32 36 L45 40 Z" fill="#e6b47c" opacity=".8"/>
    ${face(50, 54, { gap: 8, mouth: 'smile', blushDy: 6 })}
  `),
  // 香川 — udon bowl
  udon: svg(`
    <path d="M40 22 q4 -8 0 -14 M50 20 q4 -8 0 -14 M60 22 q4 -8 0 -14" fill="none" stroke="#cbd5dd" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M70 22 L90 46 M74 20 L94 44" fill="none" stroke="#b8865b" stroke-width="3" stroke-linecap="round"/>
    <path d="M18 50 H82 Q82 88 50 88 Q18 88 18 50 Z" fill="#fff" ${S}/>
    <path d="M22 64 H78" fill="none" stroke="#7fa8d6" stroke-width="3.5"/>
    <ellipse cx="50" cy="50" rx="32" ry="9" fill="#fdf0c8" ${S}/>
    <path d="M26 50 q8 -5 16 0 q8 5 16 0 q8 -5 16 0" fill="none" stroke="#f0d79a" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M30 46 q10 -4 20 0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
    <circle cx="62" cy="46" r="5" fill="#fff" ${THIN}/><circle cx="62" cy="46" r="2.6" fill="#f5a3b3"/>
    <circle cx="40" cy="44" r="1.6" fill="#7fb36b"/><circle cx="48" cy="47" r="1.4" fill="#7fb36b"/><circle cx="34" cy="49" r="1.4" fill="#7fb36b"/>
    ${face(50, 70, { gap: 9, mouth: 'w' })}
  `),
  // 愛媛 — mikan
  mikan: svg(`
    <path d="M52 30 v-10" fill="none" stroke="#7a5230" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="62" cy="22" rx="10" ry="5" transform="rotate(-25 62 22)" fill="#8fc47b" ${S}/>
    <circle cx="50" cy="58" r="27" fill="#f7a63b" ${S}/>
    <circle cx="52" cy="32" r="2.4" fill="#e08a2c"/>
    <circle cx="30" cy="66" r="1.3" fill="#e08a2c" opacity=".7"/><circle cx="70" cy="66" r="1.3" fill="#e08a2c" opacity=".7"/><circle cx="38" cy="78" r="1.3" fill="#e08a2c" opacity=".7"/><circle cx="62" cy="78" r="1.3" fill="#e08a2c" opacity=".7"/>
    ${face(50, 58, { gap: 10, mouth: 'smile' })}
  `),
  // 福岡 — tonkotsu ramen
  ramen: svg(`
    <path d="M42 20 q4 -8 0 -14 M54 18 q4 -8 0 -14" fill="none" stroke="#cbd5dd" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M70 20 L90 44 M74 18 L94 42" fill="none" stroke="#b8865b" stroke-width="3" stroke-linecap="round"/>
    <path d="M18 50 H82 Q82 88 50 88 Q18 88 18 50 Z" fill="#fff" ${S}/>
    <path d="M24 66 l5 -5 l5 5 l5 -5 l5 5 l5 -5 l5 5 l5 -5 l5 5 l5 -5 l5 5" fill="none" stroke="#e0554b" stroke-width="2.4"/>
    <ellipse cx="50" cy="50" rx="32" ry="9" fill="#f6ecd9" ${S}/>
    <rect x="66" y="36" width="12" height="16" rx="1.5" fill="#2f3a2e" ${THIN}/>
    <circle cx="36" cy="49" r="7" fill="#fff" ${THIN}/><circle cx="36" cy="49" r="3.6" fill="#f2b84b"/>
    <circle cx="54" cy="50" r="7.5" fill="#c98b6b" ${THIN}/><circle cx="54" cy="50" r="4" fill="#f0c9b0"/>
    <circle cx="45" cy="44" r="1.5" fill="#7fb36b"/><circle cx="60" cy="43" r="1.4" fill="#7fb36b"/><circle cx="28" cy="46" r="1.3" fill="#7fb36b"/>
    ${face(50, 70, { gap: 9, mouth: 'smile' })}
  `),
  // 長崎 — castella
  castella: svg(`
    <path d="M22 46 L36 28 H92 L78 46 Z" fill="#8b5a2b" ${S}/>
    <path d="M78 46 L92 28 V64 L78 82 Z" fill="#e9c25a" ${S}/>
    <rect x="22" y="46" width="56" height="36" fill="#f5d36c" ${S}/>
    <path d="M22 78 H78" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="2 3" opacity=".9"/>
    <circle cx="30" cy="34" r="1.2" fill="#fff" opacity=".8"/><circle cx="60" cy="32" r="1.2" fill="#fff" opacity=".8"/>
    ${face(50, 62, { gap: 9, mouth: 'smile' })}
  `),
  // 熊本 — bear
  kuma: svg(`
    <circle cx="30" cy="34" r="9" fill="#a9714f" ${S}/><circle cx="70" cy="34" r="9" fill="#a9714f" ${S}/>
    <circle cx="30" cy="34" r="4" fill="#d9a98a"/><circle cx="70" cy="34" r="4" fill="#d9a98a"/>
    <circle cx="50" cy="54" r="26" fill="#a9714f" ${S}/>
    <ellipse cx="50" cy="62" rx="12" ry="9" fill="#e6c8a6"/>
    ${face(50, 51, { gap: 10, mouth: 'w', blushDy: 7 })}
    <ellipse cx="50" cy="59" rx="3.4" ry="2.4" fill="${INK}"/>
    <circle cx="34" cy="82" r="8" fill="#a9714f" ${S}/><circle cx="66" cy="82" r="8" fill="#a9714f" ${S}/>
    <path d="M50 92 C42 86 40 80 45 78 C48 77 50 80 50 81 C50 80 52 77 55 78 C60 80 58 86 50 92 Z" fill="#e5708d" ${S}/>
  `),
  // 鹿児島 — "shirokuma" shaved-ice bear
  shirokuma: svg(`
    <circle cx="28" cy="42" r="8" fill="#fff" ${S}/><circle cx="72" cy="42" r="8" fill="#fff" ${S}/>
    <circle cx="28" cy="42" r="3.5" fill="#f7d5dc"/><circle cx="72" cy="42" r="3.5" fill="#f7d5dc"/>
    <circle cx="50" cy="60" r="25" fill="#fff" ${S}/>
    <path d="M30 42 Q34 22 50 24 Q66 22 70 42 Q60 38 50 40 Q40 38 30 42 Z" fill="#fff" ${S}/>
    <path d="M38 40 q2 8 0 12 M50 40 q2 10 0 16 M62 40 q-2 8 0 12" fill="none" stroke="#f3e6c8" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="24" r="5" fill="#e0554b" ${THIN}/><path d="M50 19 q2 -6 6 -8" fill="none" ${THIN}/>
    <ellipse cx="38" cy="30" rx="4" ry="2.6" fill="#f7a63b" ${THIN}/><ellipse cx="62" cy="30" rx="4" ry="2.6" fill="#f2c94c" ${THIN}/>
    <circle cx="44" cy="35" r="1.6" fill="#7a3b3b"/><circle cx="57" cy="35" r="1.6" fill="#7a3b3b"/><circle cx="50" cy="32" r="1.8" fill="#8fc47b"/>
    <ellipse cx="50" cy="68" rx="11" ry="8" fill="#fbeee4"/>
    ${face(50, 58, { gap: 10, mouth: 'w', blushDy: 7 })}
    <ellipse cx="50" cy="65" rx="3.2" ry="2.2" fill="${INK}"/>
  `),
  // 沖縄 — shisa
  shisa: svg(`
    <g fill="#d17a2a" ${S}>
      <circle cx="26" cy="40" r="7"/><circle cx="34" cy="28" r="7"/><circle cx="50" cy="22" r="7"/><circle cx="66" cy="28" r="7"/><circle cx="74" cy="40" r="7"/>
      <circle cx="22" cy="56" r="7"/><circle cx="78" cy="56" r="7"/>
    </g>
    <circle cx="50" cy="54" r="26" fill="#e8a24a" ${S}/>
    <path d="M34 42 q8 -6 14 0 M52 42 q8 -6 14 0" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>
    ${face(50, 52, { gap: 10, mouth: 'grin', sclera: true, blushDy: 7 })}
    <path d="M42 60 q8 8 16 0" fill="none" ${THIN}/>
    <circle cx="36" cy="82" r="8" fill="#e8a24a" ${S}/><circle cx="64" cy="82" r="8" fill="#e8a24a" ${S}/>
  `),
};

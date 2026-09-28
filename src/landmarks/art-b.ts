// Landmark stickers, west half (近畿 · 中国 · 四国 · 九州) + the shared kinds (寺, 神社).
// Look-alikes drawn from memory in the mascot likenesses' hand (ADR 0011) — not photos, not official art.
import { C, INK, N, O, T, castle, ground, line, torii, water } from './helpers';

export const artB: Record<string, string> = {
  // a temple hall under its big curved roof (霊山寺 and other temples)
  temple: `
    <path d="M14 84 H86 L90 92 H10 Z" fill="${C.stone}" ${O}/>
    <rect x="22" y="54" width="56" height="30" fill="${C.wood}" ${O}/>
    <path d="M36 54 V84 M50 54 V84 M64 54 V84" ${N} ${T}/>
    <rect x="42" y="62" width="16" height="22" fill="${C.dwood}" ${T}/>
    <path d="M8 56 Q14 52 22 50 Q34 36 50 32 Q66 36 78 50 Q86 52 92 56 Z" fill="${C.roof}" ${O}/>
    <circle cx="50" cy="28" r="4" fill="${C.gold}" ${T}/>`,
  // a vermilion torii over a stone path (宇佐神宮, 天岩戸神社 and other shrines)
  shrine: `
    <path d="M40 90 L45 64 H55 L60 90 Z" fill="${C.stone}" ${T}/>
    ${torii(C.verm, 50, 24, 74, 62)}`,

  // 伊勢神宮 — plain hinoki under a thatched roof, crossed chigi and katsuogi logs on the ridge
  ise: `
    ${ground(80, '#e4ddd0')}
    <rect x="26" y="50" width="48" height="30" fill="#ead9b8" ${O}/>
    <path d="M36 50 V80 M50 50 V80 M64 50 V80" ${N} ${T}/>
    <path d="M14 52 L30 30 H70 L86 52 Z" fill="#cdb48a" ${O}/>
    <path d="M22 46 H78 M26 40 H74" ${N} stroke="#a8906a" stroke-width="2.2"/>
    ${[37, 45, 53, 61].map((x) => `<rect x="${x - 1}" y="23" width="6" height="7" rx="2.5" fill="${C.gold}" ${T}/>`).join('')}
    ${line('M24 34 L33 14 M34 34 L25 14 M66 34 L75 14 M76 34 L67 14', C.wood, 3.6)}`,
  // 賢島 — the pearls of 英虞湾: an open oyster with its pearl, on the water
  pearl: `
    ${water(72)}
    <path d="M18 64 Q20 84 50 86 Q80 84 82 64 Z" fill="#d9c9e6" ${O}/>
    <path d="M18 62 Q24 28 50 24 Q76 28 82 62 Q50 50 18 62 Z" fill="#ece2f5" ${O}/>
    <path d="M30 55 Q36 36 50 30 M50 30 V49 M70 55 Q64 36 50 30" ${N} ${T}/>
    <circle cx="50" cy="67" r="9" fill="${C.white}" ${O}/><circle cx="47" cy="64" r="2.4" fill="#fff"/>`,
  // 京都タワー — the white candle of a tower on its building, a red band under the deck
  kyototower: `
    <rect x="20" y="70" width="60" height="18" fill="${C.white}" ${O}/>
    <path d="M26 76 h48 M26 82 h48" ${N} stroke="#b9d6e8" stroke-width="2.6"/>
    <path d="M45 70 Q43 52 46 40 H54 Q57 52 55 70 Z" fill="${C.white}" ${O}/>
    <path d="M39 41 Q39 30 50 30 Q61 30 61 41 Z" fill="${C.white}" ${O}/>
    <rect x="41" y="37" width="18" height="3.4" fill="${C.red}"/>
    <path d="M50 30 V14" ${N} ${O}/><circle cx="50" cy="12" r="2.8" fill="${C.red}"/>`,
  // 伏見稲荷大社 — 千本鳥居: vermilion torii one behind the other, black feet
  senbontorii: `
    <path d="M42 90 L46 44 H54 L58 90 Z" fill="${C.stone}" ${T}/>
    ${[[41, 43, 4, 14, 36, 64], [30, 35, 6, 34, 27, 74], [17, 27, 9, 57, 17, 88]].map(([xl, top, pw, span, ky, kx]) => `
      <rect x="${xl}" y="${top}" width="${pw}" height="${92 - Number(top) - 2}" fill="${C.verm}" ${O}/>
      <rect x="${Number(xl) + Number(span)}" y="${top}" width="${pw}" height="${92 - Number(top) - 2}" fill="${C.verm}" ${O}/>
      <rect x="${xl}" y="${86 - 4}" width="${pw}" height="6" fill="${INK}"/><rect x="${Number(xl) + Number(span)}" y="${86 - 4}" width="${pw}" height="6" fill="${INK}"/>
      <rect x="${Number(xl) - 2}" y="${Number(top) + 6}" width="${Number(span) + Number(pw) + 4}" height="${Number(pw) * 0.6}" fill="${C.verm}" ${T}/>
      <path d="M${100 - Number(kx)} ${Number(ky) + 3} Q50 ${Number(ky) - 3} ${kx} ${Number(ky) + 3} L${Number(kx) - 2} ${Number(ky) + 8} H${102 - Number(kx)} Z" fill="${C.verm}" ${O}/>`).join('')}`,
  // 清水寺 — the hall on its wooden stage over the trees (autumn colours)
  kiyomizu: `
    <path d="M22 58 V86 M34 58 V86 M46 58 V86 M58 58 V86 M70 58 V86 M80 58 V86 M20 70 H82 M20 80 H82" ${N} stroke="${C.dwood}" stroke-width="3"/>
    <path d="M8 86 Q16 70 30 78 Q40 66 52 78 Q64 66 76 78 Q86 70 92 86 L88 92 H12 Z" fill="${C.green}" ${O}/>
    <circle cx="24" cy="82" r="5" fill="#f2a04b"/><circle cx="60" cy="80" r="5" fill="${C.red}"/><circle cx="80" cy="84" r="4" fill="#f2a04b"/>
    <rect x="16" y="54" width="68" height="5" fill="${C.wood}" ${O}/>
    <rect x="24" y="40" width="52" height="14" fill="${C.wood}" ${O}/>
    <path d="M34 40 V54 M50 40 V54 M66 40 V54" ${N} ${T}/>
    <path d="M12 42 Q20 38 26 36 L34 26 H66 L74 36 Q80 38 88 42 Z" fill="${C.dwood}" ${O}/>`,
  // 金閣寺 — the golden pavilion over its pond, a phoenix on the roof
  kinkaku: `
    ${water(74)}
    <path d="M36 80 h10 M54 80 h10" stroke="${C.gold}" stroke-width="3" stroke-linecap="round" opacity=".8"/>
    <rect x="26" y="60" width="48" height="14" fill="#f3e2b8" ${O}/>
    <path d="M34 60 V74 M50 60 V74 M66 60 V74" ${N} ${T}/>
    <path d="M16 61 L28 54 H72 L84 61 Z" fill="${C.roof}" ${O}/>
    <rect x="30" y="42" width="40" height="12" fill="${C.gold}" ${O}/>
    <path d="M18 43 L30 36 H70 L82 43 Z" fill="${C.roof}" ${O}/>
    <rect x="37" y="26" width="26" height="10" fill="${C.gold}" ${O}/>
    <path d="M26 27 L37 20 H63 L74 27 Z" fill="${C.roof}" ${O}/>
    <path d="M50 20 V13" ${N} ${O}/><path d="M45 13 q5 -7 10 0" fill="${C.gold}" ${T}/>`,
  // 銀閣寺 — the dark two-storey pavilion and the cone of sand (向月台) in front
  ginkaku: `
    ${ground(76, '#efe6d4')}
    <path d="M20 84 q8 -3 16 0 M40 86 q8 -3 16 0" ${N} stroke="#cfc3ad" stroke-width="2.2"/>
    <rect x="24" y="52" width="46" height="22" fill="#8a7564" ${O}/>
    <rect x="29" y="56" width="36" height="12" fill="${C.cream}" ${T}/>
    <path d="M38 56 V68 M47 56 V68 M56 56 V68" ${N} ${T}/>
    <path d="M14 53 L26 45 H68 L80 53 Z" fill="${C.roof}" ${O}/>
    <rect x="34" y="34" width="26" height="11" fill="#8a7564" ${O}/>
    <path d="M26 36 L36 27 H58 L68 36 Z" fill="${C.roof}" ${O}/>
    <path d="M47 27 V20" ${N} ${O}/><path d="M43 20 q4 -6 8 0" fill="#b9b1a7" ${T}/>
    <path d="M70 86 L74 74 H84 L88 86 Z" fill="#efe6d4" ${O}/>`,
  // 平等院 — the Phoenix Hall with its two wings, mirrored in the pond (the 10-yen coin)
  byodoin: `
    ${water(74)}
    <rect x="12" y="60" width="24" height="12" fill="${C.verm}" ${O}/><rect x="64" y="60" width="24" height="12" fill="${C.verm}" ${O}/>
    <path d="M8 61 L14 55 H38 L40 61 Z M60 61 L62 55 H86 L92 61 Z" fill="${C.roof}" ${O}/>
    <path d="M8 55 L12 48 H18 L22 55 Z M78 55 L82 48 H88 L92 55 Z" fill="${C.roof}" ${O}/>
    <rect x="36" y="50" width="28" height="22" fill="${C.verm}" ${O}/>
    <path d="M42 54 v16 M50 54 v16 M58 54 v16" stroke="${C.white}" stroke-width="2.6"/>
    <path d="M24 52 Q30 48 36 46 L40 38 H60 L64 46 Q70 48 76 52 Z" fill="${C.roof}" ${O}/>
    <path d="M36 38 L42 30 H58 L64 38 Z" fill="${C.roof}" ${O}/>
    <path d="M40 30 q2 -6 6 -4 M60 30 q-2 -6 -6 -4" ${N} stroke="${C.gold}" stroke-width="3.2" stroke-linecap="round"/>`,
  // 祇園 — a machiya street front: dark wood lattice, noren and red lanterns
  gion: `
    <rect x="12" y="46" width="76" height="40" fill="${C.dwood}" ${O}/>
    <path d="M20 56 V86 M26 56 V86 M32 56 V86 M38 56 V86 M62 56 V86 M68 56 V86 M74 56 V86 M80 56 V86" stroke="#c9a57f" stroke-width="2.2"/>
    <rect x="43" y="52" width="14" height="12" fill="${C.cream}" ${T}/><path d="M50 52 V64" ${N} ${T}/>
    <path d="M8 48 L14 38 H86 L92 48 Z" fill="${C.roof}" ${O}/>
    <ellipse cx="22" cy="58" rx="6" ry="8" fill="${C.red}" ${T}/><ellipse cx="78" cy="58" rx="6" ry="8" fill="${C.red}" ${T}/>
    <path d="M22 48 v2 M78 48 v2" ${N} ${T}/>`,
  // 大阪城 — white walls, green copper roofs, gold shachihoko and bands
  osakajo: `${castle(C.white, C.teal, { trim: C.gold })}
    <path d="M36 43 h28 M41 25 h18" stroke="${C.gold}" stroke-width="2.4"/>`,
  // 道頓堀 — neon boards on the buildings along the canal
  dotonbori: `
    ${water(74)}
    <rect x="10" y="30" width="26" height="46" fill="#ece6dd" ${O}/>
    <rect x="36" y="20" width="28" height="56" fill="#ddd5ca" ${O}/>
    <rect x="64" y="36" width="26" height="40" fill="#ece6dd" ${O}/>
    <rect x="14" y="36" width="18" height="10" rx="2" fill="#f7a6c0" ${T}/>
    <rect x="40" y="26" width="20" height="14" rx="2" fill="${C.gold}" ${T}/>
    <rect x="40" y="46" width="9" height="22" rx="2" fill="#8fc3ea" ${T}/><rect x="51" y="46" width="9" height="22" rx="2" fill="#f7a6c0" ${T}/>
    <rect x="68" y="42" width="18" height="10" rx="2" fill="#b7e0a8" ${T}/>
    <path d="M44 32 h12 M18 41 h10 M72 47 h10" stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 通天閣 — the steel tower standing astride the street, its deck and neon band
  tsutenkaku: `
    <path d="M22 90 Q30 72 40 64 M78 90 Q70 72 60 64" ${N} stroke="${INK}" stroke-width="8.4" stroke-linecap="round"/>
    <path d="M22 90 Q30 72 40 64 M78 90 Q70 72 60 64" ${N} stroke="#aab1b8" stroke-width="5" stroke-linecap="round"/>
    <path d="M40 64 L44 30 H56 L60 64 Z" fill="${C.steel}" ${O}/>
    <path d="M42 58 L58 48 M42 48 L58 58 M44 40 L56 33" ${N} ${T}/>
    <rect x="41" y="44" width="18" height="5" fill="${C.sea}"/>
    <rect x="37" y="22" width="26" height="10" rx="2" fill="${C.white}" ${O}/>
    <path d="M43 22 L46 12 H54 L57 22 Z" fill="${C.steel}" ${O}/><path d="M50 12 V5" ${N} ${O}/>`,
  // あべのハルカス — the stepped glass skyscraper
  harukas: `
    <path d="M28 90 V40 H42 V26 H55 V12 H70 V90 Z" fill="#cfe6f2" ${O}/>
    <path d="M42 40 V90 M55 26 V90" ${N} ${T}/>
    <path d="M30 50 h10 M30 60 h10 M30 70 h10 M30 80 h10 M44 34 h9 M44 46 h9 M44 58 h9 M44 70 h9 M44 82 h9 M57 20 h11 M57 32 h11 M57 44 h11 M57 56 h11 M57 68 h11 M57 80 h11" ${N} stroke="#9cc4da" stroke-width="2.2"/>
    <path d="M22 90 H76" ${N} ${O}/>`,
  // 万博記念公園 — 太陽の塔: arms out, the golden face on top, the sun face on the belly
  taiyo: `
    <path d="M41 50 Q28 48 16 36 Q14 30 20 30 Q30 40 42 42 Z" fill="#f3efe8" ${O}/>
    <path d="M59 50 Q72 48 84 36 Q86 30 80 30 Q70 40 58 42 Z" fill="#f3efe8" ${O}/>
    <path d="M24 38 L30 43 L34 39 M76 38 L70 43 L66 39" ${N} stroke="#d9483b" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M37 90 L40 50 Q38 32 50 26 Q62 32 60 50 L63 90 Z" fill="#f3efe8" ${O}/>
    <circle cx="50" cy="26" r="9" fill="${C.gold}" ${O}/>
    <path d="M45.5 25 h3 M51.5 25 h3 M47 30 q3 2 6 0" ${N} stroke="${INK}" stroke-width="2" stroke-linecap="round"/>
    <circle cx="50" cy="64" r="9" fill="#c9c3bb" ${O}/>
    <path d="M50 50 v4 M50 74 v4 M36 64 h4 M60 64 h4" ${N} stroke="${INK}" stroke-width="2" stroke-linecap="round"/>`,
  // ユニバーサル・スタジオ・ジャパン — a roller coaster with a loop (a theme park in general)
  coaster: `
    <path d="M22 90 V62 M42 90 V54 M80 90 V58" ${N} stroke="${C.stone}" stroke-width="4.4" stroke-linecap="round"/>
    ${line('M8 62 Q20 40 32 56 Q44 72 56 48 A15 15 0 1 1 72 50 Q80 62 92 58', C.red, 5.2)}
    <rect x="24" y="44" width="12" height="7" rx="2" fill="#8fc3ea" ${T} transform="rotate(38 30 47)"/>`,
  // 奈良公園 — a sika deer with its spots, and a deer cracker
  deer: `
    <path d="M34 66 V86 M44 66 V86 M60 66 V86 M68 64 V86" ${N} stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
    <path d="M34 66 V86 M44 66 V86 M60 66 V86 M68 64 V86" ${N} stroke="${C.wood}" stroke-width="3" stroke-linecap="round"/>
    <path d="M24 58 Q26 46 42 46 H62 Q72 46 74 56 Q74 66 64 67 H34 Q24 67 24 58 Z" fill="${C.wood}" ${O}/>
    <path d="M66 52 L71 32 Q73 25 80 26 Q88 28 86 35 L77 39 L73 54 Z" fill="${C.wood}" ${O}/>
    <path d="M74 27 L68 19 L77 24 Z" fill="${C.wood}" ${T}/>
    ${line('M79 26 L81 13 M80.5 18 L87 13', C.dwood, 2.6)}
    <circle cx="80" cy="31" r="2" fill="${INK}"/><circle cx="86.5" cy="34" r="1.6" fill="${INK}"/>
    <g fill="${C.white}"><circle cx="36" cy="54" r="2.2"/><circle cx="46" cy="52" r="2.2"/><circle cx="56" cy="54" r="2.2"/><circle cx="42" cy="60" r="1.8"/><circle cx="52" cy="61" r="1.8"/></g>
    <path d="M24 56 q-5 -2 -4 -7" ${N} ${T}/>
    <circle cx="18" cy="80" r="9" fill="#e8c98a" ${O}/><g fill="#c69b52"><circle cx="15" cy="78" r="1.3"/><circle cx="21" cy="80" r="1.3"/><circle cx="17" cy="84" r="1.3"/></g>`,
  // 熊野三山 — the huge dark 大鳥居 of 大斎原 over the fields
  otorii: `
    ${ground(80)}
    ${torii('#4a4f4a', 50, 20, 82, 64)}`,
  // 熊野川舟下り — a wooden boat, the boatman's pole, green hills
  boat: `
    <path d="M8 62 Q22 34 40 50 Q56 30 74 46 Q86 40 92 58 Z" fill="${C.dgreen}" ${O}/>
    ${water(62)}
    <path d="M18 66 H82 L75 77 H27 Z" fill="${C.wood}" ${O}/>
    <circle cx="36" cy="61" r="4" fill="${C.cream}" ${T}/><circle cx="48" cy="61" r="4" fill="${C.cream}" ${T}/>
    <path d="M66 66 V50" ${N} ${O}/><circle cx="66" cy="45" r="4.4" fill="${C.cream}" ${T}/>
    <path d="M60 42 q6 -6 12 0 Z" fill="#e2c275" ${T}/>
    ${line('M58 36 L78 84', C.dwood, 2.6)}`,
  // 那智の大滝 — the long white fall on the green cliff, the red three-storey pagoda in front
  nachi: `
    <path d="M40 8 Q64 4 80 18 L86 90 H44 Z" fill="#6f9a5e" ${O}/>
    <path d="M58 14 Q62 12 66 14 L68 90 H58 Z" fill="${C.white}" ${O}/>
    <path d="M61 20 V86 M65 20 V86" stroke="${C.water}" stroke-width="2"/>
    <rect x="17" y="80" width="24" height="6" fill="${C.stone}" ${T}/>
    <rect x="21" y="68" width="16" height="12" fill="${C.verm}" ${O}/><path d="M12 69 L20 62 H38 L46 69 Z" fill="${C.roof}" ${O}/>
    <rect x="23" y="53" width="12" height="9" fill="${C.verm}" ${O}/><path d="M15 54 L22 47 H36 L43 54 Z" fill="${C.roof}" ${O}/>
    <rect x="25" y="39" width="8" height="8" fill="${C.verm}" ${O}/><path d="M18 40 L24 33 H34 L40 40 Z" fill="${C.roof}" ${O}/>
    <path d="M29 33 V20" ${N} ${O}/>`,
  // 鳥取砂丘 — sand dunes by the sea, ripples and a camel on the crest
  sakyu: `
    <path d="M10 44 Q50 38 90 44 L90 58 H10 Z" fill="${C.sea}" ${T}/>
    <path d="M8 62 Q28 40 54 56 Q72 44 92 60 L90 84 Q50 94 10 84 Z" fill="${C.sand}" ${O}/>
    <path d="M20 72 q8 -4 16 0 M46 78 q8 -4 16 0 M66 66 q7 -4 14 0" ${N} stroke="#d8b878" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M28 52 Q30 44 35 46 Q37 40 41 44 Q43 40 47 44 Q50 44 52 40 L56 40 L55 44 L51 47 Q49 52 45 52 Z" fill="#a8734a" ${T}/>
    <path d="M32 52 v6 M36 52 v6 M44 52 v6 M48 51 v6" ${N} stroke="#8a6d5a" stroke-width="2.2" stroke-linecap="round"/>`,
  // 松江城 — the black-boarded keep with its white plaster bands, dark tiles
  matsuejo: castle('#3f3a38', '#66696d', { band: C.white }),
  // 出雲大社 — the great straw rope (しめ縄) hanging in front of the hall, crossed chigi on the roof
  izumo: `
    ${line('M43 22 L57 6 M57 22 L43 6', C.wood, 3.6)}
    <path d="M12 44 L50 18 L88 44 Z" fill="#6b5a52" ${O}/>
    <rect x="24" y="44" width="52" height="16" fill="#e8d5b0" ${O}/>
    ${line('M34 80 V90 M50 83 V93 M66 80 V90', '#e2c275', 4.6)}
    <path d="M14 60 Q50 72 86 60 Q90 70 82 74 Q50 86 18 74 Q10 70 14 60 Z" fill="#e2c275" ${O}/>
    <path d="M26 66 L30 76 M38 69 L41 80 M50 71 L52 82 M62 69 L63 80 M74 66 L74 76" ${N} stroke="#b89548" stroke-width="2.6"/>`,
  // 原爆ドーム — the ruined hall and the bare frame of its dome (drawn quietly, in stone colours)
  genbaku: `
    <path d="M16 88 V62 L20 58 V52 H34 V44 L38 40 H62 L66 44 V52 H80 V58 L84 62 V88 Z" fill="#d8cfc4" ${O}/>
    <path d="M24 66 h6 v8 h-6 Z M36 66 h6 v8 h-6 Z M58 66 h6 v8 h-6 Z M70 66 h6 v8 h-6 Z M44 50 h4 v8 h-4 Z M52 50 h4 v8 h-4 Z M24 78 h6 v6 h-6 Z M70 78 h6 v6 h-6 Z" fill="#6b5f58"/>
    <path d="M36 41 Q36 18 50 16 Q64 18 64 41" ${N} ${O}/>
    <path d="M43 41 Q43 22 50 16 M57 41 Q57 22 50 16" ${N} ${T}/>
    <path d="M37.5 30 H62.5" ${N} ${T}/>`,
  // 厳島神社 — the great vermilion torii standing in the sea, its extra legs, the waves
  itsukushima: `
    <path d="M8 56 Q50 48 92 56 L90 84 Q50 94 10 84 Z" fill="${C.sea}" ${O}/>
    <rect x="20" y="52" width="5" height="22" fill="${C.verm}" ${T}/><rect x="75" y="52" width="5" height="22" fill="${C.verm}" ${T}/>
    <rect x="18" y="56" width="14" height="4" fill="${C.verm}" ${T}/><rect x="68" y="56" width="14" height="4" fill="${C.verm}" ${T}/>
    ${torii(C.verm, 50, 18, 76, 56)}
    <path d="M10 72 Q50 66 90 72 L88 84 Q50 94 12 84 Z" fill="${C.sea}" opacity=".7"/>
    <path d="M22 80 q6 -3 12 0 M44 84 q6 -3 12 0 M66 80 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 眉山 — the eyebrow-shaped hill and its ropeway gondola
  bizan: `
    <path d="M8 80 Q30 42 60 44 Q80 46 92 70 L92 84 Q50 94 8 84 Z" fill="${C.green}" ${O}/>
    <path d="M12 28 L88 52" ${N} stroke="${INK}" stroke-width="2.2"/>
    <path d="M50 40 V45" ${N} ${T}/>
    <rect x="42" y="45" width="16" height="12" rx="3" fill="${C.red}" ${O}/><rect x="45" y="48" width="10" height="4" rx="1" fill="${C.sky}"/>`,
  // 鳴門の渦潮 — the whirlpool, white spirals on blue water
  uzushio: `
    <circle cx="50" cy="52" r="38" fill="${C.sea}" ${O}/>
    <path d="M50 52 m-4 0 a4 4 0 1 1 8 0 a8 8 0 1 1 -16 0 a12 12 0 1 1 24 0 a16 16 0 1 1 -32 0 a20 20 0 1 1 40 0 a24 24 0 1 1 -48 0" ${N} stroke="${C.white}" stroke-width="4" stroke-linecap="round"/>
    <path d="M18 34 q6 -4 10 0 M72 78 q6 -4 10 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 道後温泉本館 — the wooden bathhouse in tiers, the little tower with its red glass and white heron
  dogo: `
    <rect x="14" y="60" width="72" height="26" fill="#e8d5b0" ${O}/>
    <path d="M22 66 h12 v10 h-12 Z M44 66 h12 v10 h-12 Z M66 66 h12 v10 h-12 Z" fill="${C.gold}" ${T}/>
    <path d="M8 62 Q14 58 20 56 L26 50 H74 L80 56 Q86 58 92 62 Z" fill="${C.roof}" ${O}/>
    <rect x="24" y="40" width="52" height="10" fill="#e8d5b0" ${O}/>
    <path d="M30 43 h8 M46 43 h8 M62 43 h8" stroke="${C.gold}" stroke-width="3"/>
    <path d="M16 42 L24 34 H76 L84 42 Z" fill="${C.roof}" ${O}/>
    <rect x="42" y="22" width="16" height="12" fill="#e8d5b0" ${O}/><rect x="45" y="25" width="10" height="6" fill="${C.red}"/>
    <path d="M38 23 L50 12 L62 23 Z" fill="${C.roof}" ${O}/>
    <path d="M50 12 l-5 -4 l7 1 Z" fill="${C.white}" ${T}/>`,
  // はりまや橋 — the small red arched bridge (famous for being smaller than you expect)
  harimaya: `
    ${water(70)}
    ${line('M14 56 Q50 30 86 56', C.red, 3.2)}
    <path d="M24 59 V49 M37 54.5 V44.5 M50 53 V43 M63 54.5 V44.5 M76 59 V49" ${N} stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>
    ${line('M12 66 Q50 40 88 66', C.red, 6)}`,
  // 沈下橋 — the low bridge without rails just above the clear 四万十川, green hills behind
  chinkabashi: `
    <path d="M8 56 Q26 30 46 44 Q62 28 80 40 Q88 44 92 54 Z" fill="${C.dgreen}" ${O}/>
    <path d="M8 60 Q50 54 92 60 L90 84 Q50 94 10 84 Z" fill="#7cc4c0" ${O}/>
    <rect x="26" y="64" width="6" height="9" fill="#d6cfc4" ${T}/><rect x="48" y="64" width="6" height="9" fill="#d6cfc4" ${T}/><rect x="70" y="64" width="6" height="9" fill="#d6cfc4" ${T}/>
    <rect x="8" y="58" width="84" height="6" fill="#ebe5dc" ${O}/>
    <path d="M20 80 q6 -3 12 0 M58 82 q6 -3 12 0" ${N} stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 有田焼 — a white porcelain vase painted in blue, red flowers
  porcelain: `
    <path d="M40 14 H60 V22 Q60 28 66 34 Q80 48 76 70 Q72 88 50 88 Q28 88 24 70 Q20 48 34 34 Q40 28 40 22 Z" fill="${C.white}" ${O}/>
    <path d="M40 24 H60" ${N} stroke="#3f6fb5" stroke-width="3"/>
    <path d="M28 56 q6 -8 12 0 q6 8 12 0 q6 -8 12 0 q6 8 10 2" ${N} stroke="#3f6fb5" stroke-width="3" stroke-linecap="round"/>
    <path d="M30 74 Q50 82 70 74" ${N} stroke="#3f6fb5" stroke-width="2.6"/>
    <g fill="${C.red}"><circle cx="40" cy="44" r="3"/><circle cx="58" cy="42" r="3"/><circle cx="50" cy="66" r="3"/></g>`,
  // 平和祈念像 — the seated figure, one arm up to the sky, one out level (drawn quietly)
  heiwa: `
    <path d="M20 90 L26 78 H74 L80 90 Z" fill="${C.stone}" ${O}/>
    ${line('M44 50 L18 48', '#6fa393', 5)}
    ${line('M57 48 Q61 34 61 14', '#6fa393', 5)}
    <path d="M32 78 Q34 66 46 66 H62 Q70 66 70 78 Z" fill="#6fa393" ${O}/>
    <path d="M40 72 Q38 56 44 46 H58 Q64 56 62 70 Z" fill="#6fa393" ${O}/>
    <circle cx="51" cy="38" r="7" fill="#6fa393" ${O}/>`,
  // 眼鏡橋 — the stone double arch whose reflection closes into a pair of glasses
  meganebashi: `
    <path d="M8 60 H92 V84 Q50 94 8 84 Z" fill="${C.water}" ${O}/>
    <path d="M20 62 A11 11 0 0 0 42 62 M58 62 A11 11 0 0 0 80 62" ${N} stroke="#b9b1a7" stroke-width="4.4" opacity=".8"/>
    <path d="M8 44 H92 V62 H80 A11 11 0 0 0 58 62 H42 A11 11 0 0 0 20 62 H8 Z" fill="${C.stone}" ${O}/>
    <path d="M14 50 h8 M30 50 h10 M48 50 h8 M62 50 h10 M80 50 h8" ${N} ${T}/>`,
  // 九十九島 — little green islands scattered on the sea
  islands: `
    <path d="M8 50 Q50 40 92 50 L90 82 Q50 94 10 82 Z" fill="${C.sea}" ${O}/>
    ${[[24, 60, 10], [48, 54, 8], [70, 62, 11], [36, 74, 7], [60, 78, 8]].map(([x, y, r]) => `<path d="M${Number(x) - Number(r)} ${y} Q${x} ${Number(y) - Number(r) * 1.4} ${Number(x) + Number(r)} ${y} Q${x} ${Number(y) + 3} ${Number(x) - Number(r)} ${y} Z" fill="${C.green}" ${T}/>`).join('')}
    <path d="M70 52 v-6 M24 51 v-5" ${N} stroke="${C.dgreen}" stroke-width="3" stroke-linecap="round"/>`,
  // 別府 — the 地獄: a red pond and a blue pond under a big cloud of steam
  beppu: `
    <path d="M24 60 Q14 50 22 42 Q22 30 34 32 Q40 20 52 26 Q64 20 70 32 Q84 32 82 44 Q90 54 78 60 Z" fill="${C.white}" ${O}/>
    <ellipse cx="34" cy="74" rx="20" ry="8" fill="#d9483b" ${O}/>
    <ellipse cx="68" cy="80" rx="19" ry="7.5" fill="#6fc3d8" ${O}/>
    <path d="M30 62 q-3 -5 0 -9 M40 62 q-3 -5 0 -9 M66 68 q-3 -5 0 -9" ${N} stroke="#b9b1a7" stroke-width="2.6" stroke-linecap="round"/>`,
  // 由布院 — the twin peaks of 由布岳 over the morning mist and the lake
  yufuin: `
    <path d="M10 70 L34 34 L42 40 L50 26 L66 44 L90 70 Z" fill="#7fa36c" ${O}/>
    ${water(72)}
    <path d="M8 64 Q30 56 50 62 Q70 56 92 64 Q88 72 50 70 Q12 74 8 64 Z" fill="${C.white}" opacity=".92" ${T}/>
    <path d="M70 80 q-3 -5 0 -9 q3 -5 0 -9" ${N} stroke="${C.red}" stroke-width="3.2" stroke-linecap="round"/>`,
  // 高千穂峡 — the gorge's basalt walls, the 真名井 fall and a rowboat on the emerald water
  takachiho: `
    <path d="M8 90 L12 14 H40 L36 90 Z" fill="#8a9a7a" ${O}/>
    <path d="M92 90 L88 20 H62 L66 90 Z" fill="#8a9a7a" ${O}/>
    <path d="M18 20 V86 M26 18 V88 M32 18 V88 M70 24 V88 M78 24 V88 M84 24 V88" ${N} stroke="#6f7f62" stroke-width="2"/>
    <path d="M12 16 q8 -10 16 -4 q8 -6 12 2 M62 22 q8 -10 16 -4 q8 -6 10 2" fill="${C.green}" ${T}/>
    <path d="M36 30 Q46 34 46 44 L48 80 H42 L40 46 Q38 38 34 36 Z" fill="${C.white}" ${T}/>
    <path d="M30 78 H72 V88 Q50 94 30 88 Z" fill="#5fb3a3" ${O}/>
    <path d="M52 78 H68 L65 83 H55 Z" fill="${C.red}" ${T}/>`,
  // 桜島 — the volcano across the water, a plume of ash
  sakurajima: `
    ${water(74)}
    <path d="M10 78 Q30 50 40 44 H58 Q70 50 90 78 Z" fill="#a8867a" ${O}/>
    <path d="M40 44 L44 50 L50 46 L55 51 L58 44" ${N} ${T}/>
    <path d="M50 44 Q40 30 48 22 Q52 10 64 14 Q74 8 78 18 Q86 22 80 30 Q72 36 62 32 Q56 40 50 44 Z" fill="#d8d2cc" ${O}/>`,
  // 種子島宇宙センター — the white rocket on its pad by the sea, the red launch tower
  rocket: `
    ${water(80)}
    <path d="M70 84 V24 M80 84 V24 M70 24 H80 M70 34 L80 44 M80 34 L70 44 M70 54 L80 64 M80 54 L70 64" ${N} stroke="${C.red}" stroke-width="3" stroke-linecap="round"/>
    <path d="M42 80 V36 Q42 22 50 12 Q58 22 58 36 V80 Z" fill="${C.white}" ${O}/>
    <path d="M34 80 V56 Q34 48 38 46 Q42 48 42 56 V80 Z" fill="${C.white}" ${O}/>
    <path d="M58 80 V56 Q58 48 62 46 Q66 48 66 56 V80 Z" fill="${C.white}" ${O}/>
    <path d="M42 44 H58" ${N} stroke="#3f6fb5" stroke-width="3"/>
    <circle cx="50" cy="32" r="3.2" fill="${C.sky}" ${T}/>
    <path d="M42 80 Q50 96 58 80 Z" fill="${C.gold}" ${T}/>`,
  // 屋久島 — 苔むす森: a huge old cedar, moss over its roots
  yakusugi: `
    <path d="M16 40 Q10 26 24 20 Q30 8 46 12 Q56 4 68 12 Q84 12 84 28 Q92 38 82 46 Q70 52 50 48 Q30 52 16 40 Z" fill="#4f8a5b" ${O}/>
    <path d="M38 90 Q36 70 40 58 Q38 50 44 46 H58 Q62 52 60 60 Q66 72 64 90 Z" fill="#9a7358" ${O}/>
    <path d="M46 56 Q44 70 46 84 M54 58 Q56 72 54 86" ${N} stroke="#7a5a44" stroke-width="2.2"/>
    <path d="M20 90 Q28 78 40 84 Q50 76 62 84 Q72 78 82 90 Z" fill="${C.green}" ${O}/>
    <g fill="#b7e0a8"><circle cx="42" cy="64" r="3"/><circle cx="60" cy="70" r="3"/><circle cx="30" cy="86" r="2.4"/></g>`,
};

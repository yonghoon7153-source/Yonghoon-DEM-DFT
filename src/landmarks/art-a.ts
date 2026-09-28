// Landmark stickers, east half (東北 · 関東 · 中部, 東京 included) + the shared kinds (♨ 温泉, 城, 滝, 夜の街).
// Look-alikes drawn from memory in the mascot likenesses' hand (ADR 0011) — not photos, not official art.
import { C, INK, N, O, T, castle, ground, line, torii, water } from './helpers';

const windows = (xs: number[], y: number, w = 4, h = 4, fill: string = C.gold) =>
  xs.map((x) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}"/>`).join('');

export const artA: Record<string, string> = {
  // ♨ a wooden tub of hot water and three red wisps of steam, like the map symbol
  onsen: `
    <path d="M20 66 Q20 88 50 88 Q80 88 80 66 Z" fill="${C.wood}" ${O}/>
    <path d="M32 72 v12 M44 74 v13 M56 74 v13 M68 72 v12" ${N} ${T}/>
    <ellipse cx="50" cy="66" rx="30" ry="9" fill="${C.water}" ${O}/>
    <path d="M36 52 q-7 -8 0 -16 q7 -8 0 -16 M50 54 q-7 -8 0 -16 q7 -8 0 -16 M64 52 q-7 -8 0 -16 q7 -8 0 -16" ${N} stroke="${C.red}" stroke-width="4.6" stroke-linecap="round"/>`,
  // a castle keep with grey tiles (駿府城 and other castles)
  castle: castle(C.white, '#7d8a94'),
  // 鶴ヶ城 — white walls under the red-brown 赤瓦 tiles, gold shachihoko
  tsurugajo: castle(C.white, '#b8513c', { trim: C.gold }),
  // a waterfall between two cliffs into a pool (称名滝)
  waterfall: `
    <path d="M12 88 L20 20 Q30 12 42 18 L44 88 Z" fill="#8f9a86" ${O}/>
    <path d="M88 88 L80 20 Q70 12 58 18 L56 88 Z" fill="#8f9a86" ${O}/>
    <path d="M18 24 q6 -10 14 -6 q6 -8 12 0 M82 24 q-6 -10 -14 -6 q-6 -8 -12 0" fill="${C.green}" ${T}/>
    <path d="M42 18 Q50 14 58 18 L60 80 H40 Z" fill="${C.white}" ${O}/>
    <path d="M46 24 V74 M54 24 V74" stroke="${C.water}" stroke-width="2.6"/>
    ${water(76)}`,
  // 夜の街 — tall buildings with lit windows under a crescent moon (池袋 · 六本木)
  night: `
    <path d="M78 12 a10 10 0 1 0 10 14 a8 8 0 1 1 -10 -14 Z" fill="${C.gold}" ${T}/>
    <path d="M12 88 V52 H26 V38 H40 V88 Z" fill="#5d6b8a" ${O}/>
    <path d="M40 88 V22 H58 V88 Z" fill="#4a5674" ${O}/>
    <path d="M58 88 V44 H72 V56 H88 V88 Z" fill="#5d6b8a" ${O}/>
    ${windows([17, 22, 30, 35], 58)}${windows([17, 30], 68)}${windows([22, 35], 78)}
    ${windows([44, 51], 28)}${windows([44], 40)}${windows([51], 50)}${windows([44, 51], 62)}${windows([44], 74)}
    ${windows([62, 67], 50)}${windows([62, 76, 81], 62)}${windows([67, 81], 74)}`,

  // 東京ディズニーランド — a pastel fairy-tale castle (a castle in general, not the park's own design)
  fairycastle: `
    <rect x="16" y="42" width="14" height="46" fill="#fbe3ec" ${O}/>
    <rect x="70" y="42" width="14" height="46" fill="#fbe3ec" ${O}/>
    <rect x="28" y="52" width="44" height="36" fill="#fbe3ec" ${O}/>
    <rect x="41" y="30" width="18" height="24" fill="#fbe3ec" ${O}/>
    <path d="M13 43 L23 18 L33 43 Z M67 43 L77 18 L87 43 Z" fill="#8fc3ea" ${O}/>
    <path d="M38 31 L50 6 L62 31 Z" fill="#8fc3ea" ${O}/>
    <path d="M50 6 V1 l7 2.4 -7 2.4" fill="${C.pink}" ${T}/>
    <path d="M43 88 V74 Q50 64 57 74 V88 Z" fill="${C.wood}" ${O}/>
    <path d="M21 56 v6 M77 56 v6 M48 38 v6 M52 38 v6 M35 62 v6 M65 62 v6" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
  // 東京ディズニーシー — a big globe over a fountain by the water
  globe: `
    ${water(74)}
    <path d="M40 78 L44 64 H56 L60 78 Z" fill="${C.stone}" ${O}/>
    <circle cx="50" cy="38" r="25" fill="#8fc3ea" ${O}/>
    <path d="M36 26 q7 -7 14 -2 q2 7 -5 9 q-7 0 -9 -7 Z M53 42 q9 -2 11 5 q-2 9 -11 6 q-4 -5 0 -11 Z M30 44 q5 -2 7 3 q-3 5 -7 2 Z" fill="${C.green}" ${T}/>
    <path d="M50 13 Q37 38 50 63 M50 13 Q63 38 50 63 M25 38 H75" ${N} stroke="${C.white}" stroke-width="2" opacity=".85"/>
    <path d="M28 64 q-4 -6 0 -10 M72 64 q4 -6 0 -10" ${N} stroke="${C.water}" stroke-width="3" stroke-linecap="round"/>`,

  // 飛鳥山公園 — a cherry tree in full bloom
  sakura: `
    <path d="M44 90 Q47 74 46 60 L54 60 Q53 74 56 90 Z" fill="#9a7358" ${O}/>
    <path d="M47 66 Q40 60 34 62 M53 68 Q60 60 66 62" ${N} stroke="#9a7358" stroke-width="3" stroke-linecap="round"/>
    <path d="M20 48 Q12 34 26 28 Q28 14 44 16 Q52 6 62 14 Q78 12 78 28 Q90 34 82 48 Q80 60 64 58 Q56 66 46 60 Q32 64 26 56 Q16 56 20 48 Z" fill="${C.pink}" ${O}/>
    <g fill="${C.white}"><circle cx="34" cy="32" r="2.6"/><circle cx="52" cy="24" r="2.6"/><circle cx="66" cy="38" r="2.6"/><circle cx="40" cy="48" r="2.6"/><circle cx="60" cy="52" r="2.2"/><circle cx="28" cy="44" r="2"/></g>
    <g fill="#e5708d"><circle cx="46" cy="36" r="1.8"/><circle cx="72" cy="30" r="1.8"/><circle cx="54" cy="44" r="1.8"/></g>`,
  // 都電荒川線 — a one-car tram, cream and green, under its pantograph
  tram: `
    <path d="M8 88 H92" ${N} ${O}/>
    <path d="M40 38 L50 22 L60 38" ${N} ${T}/><path d="M42 22 h16" ${N} ${O}/>
    <rect x="16" y="38" width="68" height="42" rx="11" fill="#fff4dc" ${O}/>
    <path d="M17 64 H83 V72 H17 Z" fill="${C.teal}"/>
    <rect x="23" y="46" width="12" height="12" rx="2.5" fill="${C.sky}" ${T}/><rect x="39" y="46" width="12" height="12" rx="2.5" fill="${C.sky}" ${T}/><rect x="55" y="46" width="10" height="12" rx="2.5" fill="${C.sky}" ${T}/>
    <rect x="68" y="46" width="10" height="22" rx="2.5" fill="${C.sky}" ${T}/>
    <circle cx="32" cy="82" r="5" fill="${INK}"/><circle cx="68" cy="82" r="5" fill="${INK}"/>
    <circle cx="80" cy="74" r="2.2" fill="${C.gold}"/>`,
  // 浅草寺 — 雷門: dark roof, red posts and the huge red lantern
  kaminarimon: `
    <rect x="22" y="44" width="7" height="44" fill="${C.red}" ${O}/><rect x="71" y="44" width="7" height="44" fill="${C.red}" ${O}/>
    <rect x="20" y="38" width="60" height="8" fill="${C.red}" ${O}/>
    <path d="M10 38 Q16 32 24 30 L32 22 H68 L76 30 Q84 32 90 38 Z" fill="${C.roof}" ${O}/>
    <rect x="39" y="46" width="22" height="5" rx="1.5" fill="${INK}"/>
    <ellipse cx="50" cy="66" rx="17" ry="18" fill="${C.red}" ${O}/>
    <rect x="39" y="82" width="22" height="5" rx="1.5" fill="${INK}"/>
    <path d="M36 60 Q50 57 64 60 M35 70 Q50 73 65 70" ${N} stroke="#b8392f" stroke-width="2"/>
    <path d="M46 59 h8 M45 65 h10 M47 71 h6" stroke="#2f2522" stroke-width="3.2" stroke-linecap="round"/>`,
  // 東京スカイツリー — the slender white tower, two decks and the antenna
  skytree: `
    <path d="M50 30 V6" ${N} ${O}/>
    <path d="M38 90 L47 34 H53 L62 90 Z" fill="${C.steel}" ${O}/>
    <path d="M44 60 L56 70 M56 60 L44 70 M42 76 L58 86 M58 76 L42 86" ${N} ${T}/>
    <rect x="41" y="44" width="18" height="8" rx="2.5" fill="${C.white}" ${O}/>
    <rect x="44" y="30" width="12" height="6" rx="2" fill="${C.white}" ${O}/>
    <path d="M32 90 H68" ${N} ${O}/>`,
  // 表参道 — the zelkova avenue: round trees on both sides of a road
  avenue: `
    <path d="M40 90 L47 38 H53 L60 90 Z" fill="#dcd5cb" ${O}/>
    <path d="M50 44 v6 M50 58 v8 M50 74 v10" stroke="${C.white}" stroke-width="2.6" stroke-linecap="round"/>
    <rect x="21" y="52" width="5" height="36" fill="#9a7358" ${T}/><rect x="74" y="52" width="5" height="36" fill="#9a7358" ${T}/>
    <circle cx="23" cy="44" r="15" fill="${C.green}" ${O}/><circle cx="77" cy="44" r="15" fill="${C.green}" ${O}/>
    <circle cx="36" cy="30" r="9" fill="${C.dgreen}" ${O}/><circle cx="64" cy="30" r="9" fill="${C.dgreen}" ${O}/>`,
  // 東京大学 — 赤門: the red lacquered gate under its tiled roof
  akamon: `
    <rect x="26" y="44" width="48" height="44" fill="#d9483b" ${O}/>
    <rect x="38" y="56" width="24" height="32" fill="#7f2d27" ${O}/>
    <path d="M50 56 V88" ${N} ${T}/>
    <path d="M26 62 H38 M62 62 H74" ${N} ${T}/>
    <path d="M12 46 Q18 40 26 38 L32 30 H68 L74 38 Q82 40 88 46 Z" fill="#6b5a52" ${O}/>
    <path d="M40 30 L44 22 H56 L60 30" fill="#6b5a52" ${O}/>`,
  // 秋葉原 — electric town: tall signs in pink, blue and yellow
  akiba: `
    <rect x="18" y="26" width="46" height="62" fill="#ece6dd" ${O}/>
    <rect x="64" y="44" width="20" height="44" fill="#ddd5ca" ${O}/>
    <rect x="23" y="32" width="9" height="32" rx="2" fill="#f7a6c0" ${T}/>
    <rect x="36" y="32" width="9" height="40" rx="2" fill="#8fc3ea" ${T}/>
    <rect x="49" y="32" width="9" height="28" rx="2" fill="${C.gold}" ${T}/>
    <rect x="68" y="50" width="12" height="9" rx="2" fill="#b7e0a8" ${T}/>
    ${windows([23, 36, 49], 78, 9, 5, C.sky)}${windows([68], 66, 12, 5, C.sky)}
    <path d="M27 40 h1.6 M27 48 h1.6 M40 40 h1.6 M40 50 h1.6 M53 40 h1.6" stroke="${C.white}" stroke-width="3" stroke-linecap="round"/>`,
  // 国会議事堂 — the white building and its stepped central tower
  kokkai: `
    <rect x="10" y="62" width="80" height="24" fill="${C.cream}" ${O}/>
    <rect x="34" y="44" width="32" height="42" fill="${C.cream}" ${O}/>
    <path d="M36 44 L41 30 H59 L64 44 Z" fill="#e7dcc5" ${O}/>
    <path d="M43 30 L50 14 L57 30 Z" fill="#e7dcc5" ${O}/>
    <path d="M16 68 v12 M24 68 v12 M76 68 v12 M84 68 v12 M42 52 v26 M50 52 v26 M58 52 v26" ${N} ${T}/>
    <path d="M8 86 H92" ${N} ${O}/>`,

  // 赤レンガ倉庫 — the long red-brick warehouse with rows of white arched windows
  akarenga: `
    <path d="M8 46 L16 36 H84 L92 46 Z" fill="#8a7d74" ${O}/>
    <rect x="10" y="46" width="80" height="40" fill="${C.brick}" ${O}/>
    <path d="M10 66 H90" ${N} ${T}/>
    ${[17, 31, 45, 59, 73].map((x) => `<path d="M${x} 61 V54 Q${x + 4} 49 ${x + 8} 54 V61 Z" fill="${C.white}" ${T}/><path d="M${x} 81 V74 Q${x + 4} 69 ${x + 8} 74 V81 Z" fill="${C.white}" ${T}/>`).join('')}`,
  // コスモクロック21 — the Ferris wheel with a clock at its hub
  cosmoclock: `
    <path d="M34 90 L50 46 L66 90" ${N} ${O}/><path d="M26 90 H74" ${N} ${O}/>
    <circle cx="50" cy="44" r="34" fill="${C.white}" ${O}/>
    <circle cx="50" cy="44" r="27" ${N} ${T}/>
    <path d="M50 17 V71 M23 44 H77 M31 25 L69 63 M69 25 L31 63" ${N} ${T}/>
    ${[[84, 44, '#f7a6c0'], [74, 68, '#8fc3ea'], [50, 78, C.gold], [26, 68, '#b7e0a8'], [16, 44, '#f7a6c0'], [26, 20, '#8fc3ea'], [50, 10, C.gold], [74, 20, '#b7e0a8']]
      .map(([x, y, c]) => `<circle cx="${x}" cy="${y}" r="5" fill="${c}" ${T}/>`).join('')}
    <circle cx="50" cy="44" r="10" fill="${C.gold}" ${O}/>
    <path d="M50 44 V37 M50 44 L55 47" stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>`,
  // 横浜中華街 — the gate: red posts, green tiled roofs, a gold name board
  chinatown: `
    <rect x="26" y="54" width="8" height="36" fill="${C.red}" ${O}/><rect x="66" y="54" width="8" height="36" fill="${C.red}" ${O}/>
    <path d="M18 50 Q50 44 82 50 L79 56 H21 Z" fill="#3f8f6b" ${O}/>
    <rect x="24" y="38" width="52" height="12" fill="${C.red}" ${O}/>
    <rect x="38" y="40" width="24" height="8" fill="${C.gold}" ${T}/>
    <path d="M12 36 Q20 32 26 30 L32 24 H68 L74 30 Q80 32 88 36 Z" fill="#3f8f6b" ${O}/>
    <path d="M46 20 L50 14 L54 20 Z" fill="${C.gold}" ${T}/>`,
  // 箱根神社 — the red 平和の鳥居 standing in the lake, green hills behind
  hakonetorii: `
    <path d="M8 62 Q18 40 34 46 Q48 30 64 44 Q80 36 92 60 Z" fill="${C.dgreen}" ${O}/>
    ${torii(C.red, 50, 28, 62, 44)}
    ${water(68)}
    <path d="M36 78 v6 M64 78 v6" stroke="${C.red}" stroke-width="3.4" stroke-linecap="round" opacity=".55"/>`,
  // ぽんしゅ館 — a big sake bottle and a janome cup
  sake: `
    <path d="M36 90 V48 Q36 40 42 36 V20 H52 V36 Q58 40 58 48 V90 Z" fill="#8fbfa3" ${O}/>
    <rect x="42" y="14" width="10" height="7" rx="1.5" fill="${C.red}" ${T}/>
    <rect x="39.5" y="54" width="15" height="24" fill="${C.white}" ${T}/>
    <path d="M47 58 v16 M44 62 h6" stroke="${INK}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M60 70 H84 L80 88 H64 Z" fill="${C.white}" ${O}/>
    <ellipse cx="72" cy="70" rx="12" ry="3.4" fill="${C.white}" ${T}/>
    <ellipse cx="72" cy="78" rx="5" ry="2" ${N} stroke="#6fa8dc" stroke-width="2.4"/>`,
  // TOYAMAキラリ — the faceted glass building with wood inside
  kirari: `
    <path d="M12 88 L18 40 L50 28 L82 40 L88 88 Z" fill="#cfe6f2" ${O}/>
    <path d="M18 40 L34 88 M50 28 V88 M82 40 L66 88 M16 62 H84" ${N} ${T}/>
    <path d="M38 88 V70 H62 V88" fill="${C.wood}" ${T}/>
    <path d="M24 50 l6 -3 M64 47 l6 3" stroke="${C.white}" stroke-width="3" stroke-linecap="round"/>`,
  // 雪の大谷 — the road between the tall snow walls, a yellow bus
  yukinootani: `
    <path d="M36 12 H64 L58 62 H42 Z" fill="${C.sky}"/>
    <path d="M10 90 L16 18 Q26 12 38 16 L44 90 Z" fill="${C.white}" ${O}/>
    <path d="M90 90 L84 18 Q74 12 62 16 L56 90 Z" fill="${C.white}" ${O}/>
    <path d="M17 34 q10 3 20 0 M16 50 q11 3 23 0 M16 66 q12 3 24 0 M83 34 q-10 3 -20 0 M84 50 q-11 3 -23 0 M84 66 q-12 3 -24 0" ${N} stroke="#b9d6e8" stroke-width="2.6"/>
    <path d="M44 90 L47 40 H53 L56 90 Z" fill="#9a958f" ${O}/>
    <rect x="42" y="64" width="16" height="15" rx="3" fill="${C.gold}" ${O}/>
    <rect x="44.5" y="67" width="11" height="4.5" rx="1" fill="${C.sky}"/>`,
  // 砺波のチューリップ — three tulips, red, yellow and pink
  tulip: `
    ${ground(76)}
    ${[[30, 46, C.red], [50, 36, C.gold], [70, 46, '#f7a6c0']].map(([x, y, c]) => `
      <path d="M${x} 78 V${Number(y) + 6}" ${N} stroke="${C.dgreen}" stroke-width="3.6" stroke-linecap="round"/>
      <path d="M${x} 72 q-11 -5 -13 -16 q11 2 13 12" fill="${C.green}" ${T}/>
      <path d="M${Number(x) - 9} ${y} Q${Number(x) - 10} ${Number(y) - 18} ${Number(x) - 5} ${Number(y) - 20} L${x} ${Number(y) - 14} L${Number(x) + 5} ${Number(y) - 20} Q${Number(x) + 10} ${Number(y) - 18} ${Number(x) + 9} ${y} Q${x} ${Number(y) + 7} ${Number(x) - 9} ${y} Z" fill="${c}" ${O}/>`).join('')}`,
  // 金沢駅 — 鼓門: two twisted wooden posts like the laces of a tsuzumi drum, the glass dome behind
  tsuzumimon: `
    <path d="M8 62 Q50 14 92 62" fill="#e6f2f8" stroke="#8fb4c8" stroke-width="3"/>
    <path d="M20 28 H80 L76 35 H24 Z" fill="${C.wood}" ${O}/>
    <path d="M28 35 Q20 60 30 88 H42 Q34 60 40 35 Z" fill="#d6a574" ${O}/>
    <path d="M72 35 Q80 60 70 88 H58 Q66 60 60 35 Z" fill="#d6a574" ${O}/>
    <path d="M30 42 L39 50 M28 54 L38 62 M29 66 L38 74 M31 78 L40 85 M70 42 L61 50 M72 54 L62 62 M71 66 L62 74 M69 78 L60 85" ${N} ${T}/>`,
  // 一乗谷朝倉氏遺跡 — the 唐門 gate over the old stone walls
  ruins: `
    <path d="M8 90 V66 H92 V90 Z" fill="${C.stone}" ${O}/>
    <path d="M8 78 H92 M22 66 V78 M40 66 V78 M60 66 V78 M78 66 V78 M14 78 V90 M31 78 V90 M50 78 V90 M69 78 V90 M86 78 V90" ${N} ${T}/>
    <path d="M24 70 q4 -4 8 0 M66 70 q4 -4 8 0" fill="${C.green}" ${T}/>
    <rect x="34" y="42" width="32" height="24" fill="${C.dwood}" ${O}/>
    <rect x="42" y="48" width="16" height="18" fill="${INK}"/>
    <path d="M24 44 Q33 42 37 34 Q50 20 63 34 Q67 42 76 44 Z" fill="${C.roof}" ${O}/>`,
  // 鯖江 — a pair of glasses (9 of 10 Japanese frames come from here)
  glasses: `
    <path d="M17 50 L8 42 M83 50 L92 42" ${N} stroke="#8a5a3a" stroke-width="5" stroke-linecap="round"/>
    <circle cx="31" cy="56" r="16" fill="#dff0f8"/><circle cx="69" cy="56" r="16" fill="#dff0f8"/>
    <circle cx="31" cy="56" r="16" ${N} stroke="${INK}" stroke-width="8"/><circle cx="69" cy="56" r="16" ${N} stroke="${INK}" stroke-width="8"/>
    <circle cx="31" cy="56" r="16" ${N} stroke="#8a5a3a" stroke-width="4.4"/><circle cx="69" cy="56" r="16" ${N} stroke="#8a5a3a" stroke-width="4.4"/>
    ${line('M46 52 Q50 45 54 52', '#8a5a3a', 4.4)}
    <path d="M23 49 q4 -4 9 -4 M61 49 q4 -4 9 -4" ${N} stroke="${C.white}" stroke-width="3" stroke-linecap="round"/>`,
  // 忠霊塔 — the red five-storey pagoda with 富士山 behind and cherry blossoms in front
  churei: `
    <path d="M42 68 L63 32 Q68 27 73 32 L94 64 Z" fill="#7fa7d4" ${O}/>
    <path d="M57 42 L63 32 Q68 27 73 32 L79 42 L73 39 L68 44 L63 39 Z" fill="${C.white}" ${T}/>
    <path d="M30 23 V8" ${N} ${O}/><path d="M27 12 h6 M27 16 h6" ${N} ${T}/>
    <rect x="18" y="80" width="24" height="5" fill="${C.stone}" ${T}/>
    <rect x="22" y="70" width="16" height="10" fill="${C.verm}" ${O}/><path d="M13 71 L20 66 H40 L47 71 Z" fill="${C.roof}" ${O}/>
    <rect x="23.5" y="60" width="13" height="6" fill="${C.verm}" ${O}/><path d="M15 61 L21.5 56 H38.5 L45 61 Z" fill="${C.roof}" ${O}/>
    <rect x="25" y="50" width="10" height="6" fill="${C.verm}" ${O}/><path d="M17 51 L23 46 H37 L43 51 Z" fill="${C.roof}" ${O}/>
    <rect x="26" y="40" width="8" height="6" fill="${C.verm}" ${O}/><path d="M19 41 L24.5 36 H35.5 L41 41 Z" fill="${C.roof}" ${O}/>
    <rect x="27" y="30" width="6" height="6" fill="${C.verm}" ${O}/><path d="M21 31 L26 26 H34 L39 31 Z" fill="${C.roof}" ${O}/>
    <path d="M8 88 Q12 74 24 80 Q32 70 44 80 Q54 72 62 84 Q72 78 84 86 Q86 92 80 92 H14 Q6 92 8 88 Z" fill="${C.pink}" ${O}/>`,
  // 飛騨古川 — the 君の名は。 town: a comet with a split tail over the lake and hills
  comet: `
    <circle cx="50" cy="50" r="40" fill="${C.navy}" ${O}/>
    <g fill="${C.white}"><circle cx="24" cy="30" r="1.6"/><circle cx="40" cy="20" r="1.3"/><circle cx="78" cy="56" r="1.4"/><circle cx="30" cy="48" r="1.2"/><circle cx="58" cy="18" r="1.2"/></g>
    <path d="M66 32 Q44 50 22 76" ${N} stroke="#f7b3c6" stroke-width="5" stroke-linecap="round"/>
    <path d="M64 30 Q42 42 16 56" ${N} stroke="#a9d8ec" stroke-width="4" stroke-linecap="round"/>
    <circle cx="67" cy="30" r="5.5" fill="${C.white}" ${T}/>
    <path d="M12 70 Q28 58 40 66 Q54 56 68 64 Q80 58 88 68 Q86 82 70 88 Q50 94 30 88 Q14 82 12 70 Z" fill="#26304f" ${T}/>
    <path d="M34 80 h10 M56 82 h10" stroke="${C.gold}" stroke-width="2.4" stroke-linecap="round"/>`,
  // 富士山 — the snow-capped cone and a little cloud
  fuji: `
    <path d="M8 84 L40 30 Q50 22 60 30 L92 84 Z" fill="#7fa7d4" ${O}/>
    <path d="M29 48 L40 30 Q50 22 60 30 L71 48 L64 44 L57 50 L50 43 L43 50 L36 44 Z" fill="${C.white}" ${T}/>
    <path d="M14 66 Q16 58 24 60 Q28 52 36 58 Q42 56 42 64 Q42 70 34 70 H20 Q12 70 14 66 Z" fill="${C.white}" ${T}/>
    <circle cx="78" cy="22" r="8" fill="${C.red}" ${T}/>`,
  // 楽器の街 (浜松) — piano keys and a music note
  piano: `
    <rect x="10" y="50" width="80" height="32" rx="4" fill="${C.white}" ${O}/>
    <path d="M21.4 50 V82 M32.8 50 V82 M44.2 50 V82 M55.6 50 V82 M67 50 V82 M78.4 50 V82" ${N} ${T}/>
    ${[18, 29.4, 52.2, 63.6, 75].map((x) => `<rect x="${x}" y="50" width="6.8" height="19" rx="1" fill="${INK}"/>`).join('')}
    <path d="M58 14 V36 M58 14 L76 18 V32" ${N} stroke="${INK}" stroke-width="3.6" stroke-linecap="round"/>
    <ellipse cx="53.5" cy="37" rx="5.5" ry="4.4" fill="${INK}"/><ellipse cx="71.5" cy="33" rx="5.5" ry="4.4" fill="${INK}"/>`,
  // トヨタ自動車 本社 — a friendly little car (no badge)
  car: `
    <path d="M10 68 Q10 57 20 55 L31 40 Q35 34 43 34 H61 Q69 34 73 40 L82 55 Q90 57 90 68 V74 H10 Z" fill="${C.red}" ${O}/>
    <path d="M34 53 L40 42 H49 V53 Z M54 53 V42 H61 Q65 42 67 46 L71 53 Z" fill="${C.sky}" ${T}/>
    <path d="M10 64 H90" ${N} stroke="#b8392f" stroke-width="2.4"/>
    <circle cx="29" cy="74" r="9" fill="${INK}"/><circle cx="29" cy="74" r="3.6" fill="${C.stone}"/>
    <circle cx="71" cy="74" r="9" fill="${INK}"/><circle cx="71" cy="74" r="3.6" fill="${C.stone}"/>
    <circle cx="85" cy="60" r="2.6" fill="${C.gold}"/>`,
};

// Likenesses of the real local mascots — Kinki → Okinawa (ADR 0003). Drawn from memory; not official art.
import { INK, S, THIN, blush, eyes, face, mouth, svg } from './helpers';

export const artB: Record<string, string> = {
  // 三重 とこまる — pearl-white sports cheerer in a blue cap
  tokomaru: svg(`
    <circle cx="50" cy="58" r="27" fill="#fdfdfd" ${S}/>
    <path d="M24 44 Q30 20 50 20 Q70 20 76 44 Z" fill="#3b6fb6" ${S}/>
    <path d="M76 44 h12 q0 6 -6 6 z" fill="#3b6fb6" ${S}/>
    ${face(50, 58, { gap: 10, mouth: 'grin' })}
    <path d="M80 62 v26 M80 62 h16 l-4 6 l4 6 h-16" fill="#e0554b" ${THIN}/>
  `),
  // 滋賀 キャッフィー — the big Biwako catfish
  caffy: svg(`
    <path d="M78 58 q14 -14 12 -26 q-10 6 -14 16 M78 58 q14 14 12 26 q-10 -6 -14 -16" fill="#6f8fb5" ${S}/>
    <ellipse cx="46" cy="58" rx="36" ry="24" fill="#6f8fb5" ${S}/>
    <ellipse cx="46" cy="68" rx="24" ry="11" fill="#f7e08a"/>
    <path d="M14 52 l-12 -8 M14 58 l-12 4 M78 52 l12 -8 M78 58 l12 4" fill="none" ${THIN}/>
    ${eyes(46, 52, { gap: 12, r: 3.8, sclera: 6 })}
    ${mouth(46, 64, 'wide', 22)}
    ${blush(46, 60, 24)}
  `),
  // 滋賀 ひこにゃん — white cat in a red samurai helmet with gold horns
  hikonyan: svg(`
    <path d="M40 30 L30 8 L48 22 Z M60 30 L70 8 L52 22 Z" fill="#f2c94c" ${S}/>
    <circle cx="50" cy="56" r="26" fill="#fff" ${S}/>
    <path d="M24 46 Q28 24 50 24 Q72 24 76 46 Q62 40 50 42 Q38 40 24 46 Z" fill="#c8302e" ${S}/>
    <path d="M34 40 h32" fill="none" stroke="#f2c94c" stroke-width="3"/>
    ${eyes(50, 56, { gap: 9, r: 2.8 })}
    <path d="M47 63 q3 3 6 0" fill="none" ${THIN}/>
    <ellipse cx="50" cy="61" rx="1.8" ry="1.3" fill="#f5a3b3"/>
    ${blush(50, 62, 17)}
    <circle cx="50" cy="84" r="5" fill="#f2c94c" ${THIN}/>
  `),
  // 京都 まゆまろ — white cocoon with Heian eyebrows
  mayumaro: svg(`
    <ellipse cx="50" cy="54" rx="24" ry="36" fill="#fdfdfd" ${S}/>
    <ellipse cx="42" cy="38" rx="3.2" ry="2.4" fill="#2b2b2b"/><ellipse cx="58" cy="38" rx="3.2" ry="2.4" fill="#2b2b2b"/>
    ${eyes(50, 52, { gap: 8, r: 2.2 })}
    ${mouth(50, 60, 'smile', 6)}
    ${blush(50, 58, 14)}
  `),
  // 大阪 もずやん — shrike with a black eye stripe
  mozuyan: svg(`
    <ellipse cx="22" cy="64" rx="9" ry="14" transform="rotate(20 22 64)" fill="#8b5a2b" ${S}/><ellipse cx="78" cy="64" rx="9" ry="14" transform="rotate(-20 78 64)" fill="#8b5a2b" ${S}/>
    <circle cx="50" cy="56" r="28" fill="#d99a5b" ${S}/>
    <ellipse cx="50" cy="70" rx="16" ry="12" fill="#f6ead6"/>
    <path d="M22 50 Q50 44 78 50 L78 56 Q50 50 22 56 Z" fill="#2b2b2b"/>
    ${eyes(50, 53, { gap: 10, r: 2.8, color: '#fff' })}
    <path d="M46 60 L50 66 L54 60 Z" fill="#2b2b2b"/>
    ${blush(50, 62, 18)}
    <path d="M40 86 v6 M44 86 v6 M56 86 v6 M60 86 v6" fill="none" stroke="#8b5a2b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 兵庫 はばタン — yellow phoenix with a red plume
  habatan: svg(`
    <path d="M42 26 q-6 -14 4 -16 M50 22 q0 -14 8 -14 M58 26 q6 -14 -2 -18" fill="none" stroke="#e0554b" stroke-width="5" stroke-linecap="round"/>
    <ellipse cx="22" cy="62" rx="10" ry="16" transform="rotate(20 22 62)" fill="#f7d21b" ${S}/><ellipse cx="78" cy="62" rx="10" ry="16" transform="rotate(-20 78 62)" fill="#f7d21b" ${S}/>
    <circle cx="50" cy="58" r="28" fill="#f7d21b" ${S}/>
    <path d="M44 62 L50 68 L56 62 Z" fill="#f7a63b" ${THIN}/>
    ${eyes(50, 56, { gap: 10, r: 3.4 })}
    ${blush(50, 64, 18)}
    <path d="M40 88 v5 M44 88 v5 M56 88 v5 M60 88 v5" fill="none" stroke="#f7a63b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 奈良 せんとくん — child with deer antlers in a red robe
  sentokun: svg(`
    <path d="M36 32 q-4 -14 -12 -16 M36 32 q-2 -12 2 -18 M64 32 q4 -14 12 -16 M64 32 q2 -12 -2 -18" fill="none" stroke="#8b6b4a" stroke-width="3.2" stroke-linecap="round"/>
    <path d="M28 92 Q30 66 50 66 Q70 66 72 92 Z" fill="#c8302e" ${S}/>
    <path d="M50 66 l-8 26 M50 66 l8 26" fill="none" stroke="#fff" stroke-width="2"/>
    <ellipse cx="26" cy="50" rx="7" ry="4" fill="#f3d5b5" ${S}/><ellipse cx="74" cy="50" rx="7" ry="4" fill="#f3d5b5" ${S}/>
    <circle cx="50" cy="48" r="23" fill="#f3d5b5" ${S}/>
    <path d="M40 30 q10 -6 20 0" fill="none" stroke="#2b2b2b" stroke-width="4" stroke-linecap="round"/>
    ${eyes(50, 48, { gap: 9, r: 3.6 })}
    ${mouth(50, 58, 'smile', 8)}
    ${blush(50, 54, 17)}
  `),
  // 和歌山 きいちゃん — white Kishu dog with a mikan
  kiichan: svg(`
    <path d="M30 40 L34 18 L46 34 Z M70 40 L66 18 L54 34 Z" fill="#fff8f0" ${S}/>
    <circle cx="50" cy="54" r="25" fill="#fff8f0" ${S}/>
    <path d="M30 76 Q50 86 70 76 L70 82 Q50 92 30 82 Z" fill="#e0554b" ${S}/>
    <circle cx="50" cy="84" r="3.2" fill="#f2c94c" ${THIN}/>
    <ellipse cx="50" cy="62" rx="3" ry="2.2" fill="${INK}"/>
    ${eyes(50, 54, { gap: 10, r: 3 })}
    ${mouth(50, 65, 'w', 8)}
    ${blush(50, 60, 18)}
    <circle cx="80" cy="82" r="8" fill="#f7a63b" ${THIN}/><path d="M80 74 q4 -4 6 -2" fill="none" stroke="#7fb36b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 鳥取 トリピー — pear-shaped bird
  toripy: svg(`
    <path d="M52 22 v-8" fill="none" stroke="#7a5230" stroke-width="3" stroke-linecap="round"/>
    <path d="M50 18 C36 18 28 40 26 60 C24 80 36 92 50 92 C64 92 76 80 74 60 C72 40 64 18 50 18 Z" fill="#d9e15a" ${S}/>
    <path d="M26 58 q-8 6 -4 14 q6 -4 8 -8 M74 58 q8 6 4 14 q-6 -4 -8 -8" fill="#d9e15a" ${S}/>
    <path d="M44 48 L50 54 L56 48 Z" fill="#f7a63b" ${THIN}/>
    ${eyes(50, 42, { gap: 9, r: 3.2 })}
    ${blush(50, 50, 17)}
    <path d="M40 92 v5 M44 92 v5 M56 92 v5 M60 92 v5" fill="none" stroke="#f7a63b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 島根 しまねっこ — yellow cat under an Izumo-taisha roof hat
  shimanekko: svg(`
    <path d="M22 40 L30 18 H70 L78 40 Z" fill="#6b4a2b" ${S}/>
    <path d="M18 40 Q50 32 82 40 L80 46 Q50 40 20 46 Z" fill="#f0e2c0" ${S}/>
    <path d="M28 42 q4 2 8 0 q4 2 8 0 q4 2 8 0 q4 2 8 0 q4 2 8 0" fill="none" ${THIN}/>
    <circle cx="50" cy="60" r="24" fill="#f7d21b" ${S}/>
    <path d="M32 76 Q50 86 68 76 L68 82 Q50 92 32 82 Z" fill="#e0554b" ${S}/>
    ${eyes(50, 58, { gap: 9, r: 2.8 })}
    <path d="M47 66 q3 3 6 0" fill="none" ${THIN}/>
    <ellipse cx="50" cy="64" rx="1.8" ry="1.3" fill="#f5a3b3"/>
    ${blush(50, 65, 17)}
  `),
  // 岡山 ももっち — peach-headed Momotaro with kibidango
  momocchi: svg(`
    <path d="M28 92 Q30 68 50 68 Q70 68 72 92 Z" fill="#3b6fb6" ${S}/>
    <path d="M50 68 v24" fill="none" stroke="#fff" stroke-width="2"/>
    <path d="M50 28 C36 20 22 30 24 50 C26 66 38 74 50 72 C62 74 74 66 76 50 C78 30 64 20 50 28 Z" fill="#f7b8c8" ${S}/>
    <path d="M50 30 q0 20 0 42" fill="none" stroke="#e79fb3" stroke-width="2"/>
    <ellipse cx="58" cy="22" rx="8" ry="4" transform="rotate(-25 58 22)" fill="#7fb36b" ${S}/>
    ${eyes(50, 50, { gap: 9, r: 3 })}
    ${mouth(50, 60, 'smile', 8)}
    ${blush(50, 56, 17)}
    <path d="M82 60 v30" fill="none" stroke="#8b6b4a" stroke-width="2.4"/>
    <circle cx="82" cy="64" r="4" fill="#fff" ${THIN}/><circle cx="82" cy="73" r="4" fill="#fff" ${THIN}/><circle cx="82" cy="82" r="4" fill="#fff" ${THIN}/>
  `),
  // 広島 ブンカッキー — blue oyster with a maple leaf and a baton
  bunkakky: svg(`
    <path d="M50 12 l4 8 l8 -4 l-2 9 l9 2 l-6 6 l6 6 l-9 2 l2 9 l-8 -4 l-4 8 l-4 -8 l-8 4 l2 -9 l-9 -2 l6 -6 l-6 -6 l9 -2 l-2 -9 l8 4 z" fill="#e0554b" ${THIN}/>
    <path d="M22 60 C22 40 34 34 50 34 C66 34 78 40 78 60 C78 80 66 92 50 92 C34 92 22 80 22 60 Z" fill="#8fa8c7" ${S}/>
    <path d="M28 50 q22 -8 44 0 M26 62 q24 -8 48 0" fill="none" stroke="#6f8fb5" stroke-width="2" stroke-linecap="round"/>
    ${eyes(50, 58, { gap: 10, r: 3.4, sclera: 5.5 })}
    ${mouth(50, 70, 'smile', 10)}
    ${blush(50, 66, 19)}
    <path d="M78 66 L94 50" fill="none" stroke="#2b2b2b" stroke-width="2.6" stroke-linecap="round"/>
  `),
  // 山口 ちょるる — white, 山-shaped blue hair, square 口 mouth
  choruru: svg(`
    <circle cx="50" cy="58" r="28" fill="#fff" ${S}/>
    <path d="M22 44 L30 20 L40 40 L50 14 L60 40 L70 20 L78 44 Z" fill="#3b6fb6" ${S}/>
    <path d="M30 80 Q50 90 70 80 L70 86 Q50 96 30 86 Z" fill="#f2c94c" ${S}/>
    ${eyes(50, 56, { gap: 10, r: 3 })}
    <rect x="44" y="64" width="12" height="9" rx="1.5" fill="#fff" ${THIN}/>
    ${blush(50, 64, 18)}
  `),
  // 徳島 すだちくん — green sudachi citrus
  sudachikun: svg(`
    <ellipse cx="56" cy="24" rx="8" ry="4" transform="rotate(-25 56 24)" fill="#5fa53a" ${S}/>
    <circle cx="50" cy="58" r="30" fill="#8cc63f" ${S}/>
    <ellipse cx="38" cy="44" rx="6" ry="9" transform="rotate(25 38 44)" fill="#fff" opacity=".45"/>
    ${face(50, 58, { gap: 10, mouth: 'smile' })}
    <path d="M22 66 q-8 2 -6 8 M78 66 q8 2 6 8" fill="none" stroke="#8cc63f" stroke-width="5" stroke-linecap="round"/>
    <rect x="36" y="86" width="9" height="8" rx="4" fill="#8cc63f" ${THIN}/><rect x="55" y="86" width="9" height="8" rx="4" fill="#8cc63f" ${THIN}/>
  `),
  // 香川 親切な青鬼くん — kind blue ogre in tiger-stripe shorts
  aoonikun: svg(`
    <path d="M38 24 L34 8 L46 20 Z M62 24 L66 8 L54 20 Z" fill="#f2c94c" ${S}/>
    <path d="M30 36 Q50 14 70 36 Q60 28 50 30 Q40 28 30 36 Z" fill="#2b2b2b" ${S}/>
    <circle cx="50" cy="52" r="26" fill="#3b6fb6" ${S}/>
    <path d="M32 74 H68 L70 92 H30 Z" fill="#f2c94c" ${S}/>
    <path d="M38 76 v14 M50 76 v14 M62 76 v14" fill="none" stroke="#2b2b2b" stroke-width="3"/>
    ${eyes(50, 52, { gap: 10, r: 3 })}
    ${mouth(50, 62, 'smile', 10)}
    ${blush(50, 58, 18, 4.6, 2.6, '#f7a6b8')}
  `),
  // 愛媛 みきゃん — mikan puppy with a leaf and a heart nose
  mican: svg(`
    <ellipse cx="24" cy="56" rx="7" ry="12" transform="rotate(15 24 56)" fill="#e08a2c" ${S}/><ellipse cx="76" cy="56" rx="7" ry="12" transform="rotate(-15 76 56)" fill="#e08a2c" ${S}/>
    <circle cx="50" cy="56" r="27" fill="#f7a63b" ${S}/>
    <path d="M50 30 q2 -10 10 -10 M50 30 q-2 -10 -10 -10" fill="none" stroke="#7fb36b" stroke-width="6" stroke-linecap="round"/>
    <ellipse cx="50" cy="66" rx="12" ry="9" fill="#fff8f0"/>
    <path d="M50 66 C46 61 42 62 44 66 C46 68 48 69 50 71 C52 69 54 68 56 66 C58 62 54 61 50 66 Z" fill="#e0554b" ${THIN}/>
    ${eyes(50, 55, { gap: 10, r: 3.4 })}
    ${blush(50, 62, 19)}
  `),
  // 愛媛 バリィさん — yellow bird with a castle crown and a towel belly-band
  barysan: svg(`
    <path d="M32 26 V14 h8 v6 h6 v-6 h8 v6 h6 v-6 h8 v12 Z" fill="#e0554b" ${S}/>
    <circle cx="50" cy="58" r="30" fill="#f7d21b" ${S}/>
    <path d="M22 66 h56 v14 h-56 z" fill="#3b6fb6"/>
    <path d="M22 70 h56 M22 76 h56" fill="none" stroke="#fff" stroke-width="2.4"/>
    <path d="M44 56 L50 62 L56 56 Z" fill="#f7a63b" ${THIN}/>
    ${eyes(50, 50, { gap: 10, r: 3 })}
    ${blush(50, 58, 18)}
    <path d="M40 90 v5 M44 90 v5 M56 90 v5 M60 90 v5" fill="none" stroke="#f7a63b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 高知 くろしおくん — blue with a curling white wave crest
  kuroshiokun: svg(`
    <circle cx="50" cy="60" r="28" fill="#3b6fb6" ${S}/>
    <path d="M22 44 Q26 20 50 26 Q60 12 74 22 Q66 26 68 34 Q80 36 78 46 Q64 38 50 42 Q36 38 22 44 Z" fill="#fff" ${S}/>
    ${eyes(50, 60, { gap: 10, r: 3.4, sclera: 5.5 })}
    ${mouth(50, 72, 'smile', 10)}
    ${blush(50, 67, 19)}
  `),
  // 高知 カツオ人間 — a person whose head is a slice of bonito
  katsuoningen: svg(`
    <path d="M26 92 Q28 60 50 60 Q72 60 74 92 Z" fill="#fff" ${S}/>
    <path d="M26 92 h48 v-10 H26 Z" fill="#2b3a55"/>
    <path d="M22 44 C22 22 78 22 78 44 C78 58 62 62 50 62 C38 62 22 58 22 44 Z" fill="#c94a4a" ${S}/>
    <path d="M24 50 Q50 66 76 50 Q64 60 50 60 Q36 60 24 50 Z" fill="#4a5568"/>
    <path d="M32 38 q18 -8 36 0 M36 46 q14 -6 28 0" fill="none" stroke="#f0b7b7" stroke-width="2" stroke-linecap="round"/>
    ${eyes(50, 42, { gap: 9, r: 2.6 })}
    ${mouth(50, 50, 'flat', 8)}
  `),
  // 福岡 エコトン — pink pig wearing a tonkotsu ramen bowl
  ecoton: svg(`
    <path d="M24 44 Q26 16 50 16 Q74 16 76 44 Z" fill="#fff" ${S}/>
    <path d="M28 34 h44 M30 40 h40" fill="none" stroke="#e0554b" stroke-width="2"/>
    <path d="M30 22 q6 6 12 0 q6 6 12 0 q6 6 12 0" fill="none" stroke="#f0d79a" stroke-width="3" stroke-linecap="round"/>
    <circle cx="58" cy="20" r="4" fill="#f2c94c" ${THIN}/>
    <path d="M26 52 l-6 -10 l10 4 M74 52 l6 -10 l-10 4" fill="#f6b8c5" ${S}/>
    <circle cx="50" cy="60" r="26" fill="#f6b8c5" ${S}/>
    <ellipse cx="50" cy="66" rx="9" ry="6" fill="#e98aa0" ${THIN}/>
    <circle cx="47" cy="66" r="1.4" fill="${INK}"/><circle cx="53" cy="66" r="1.4" fill="${INK}"/>
    ${eyes(50, 56, { gap: 11, r: 3 })}
    ${blush(50, 62, 20, 4.4, 2.6, '#f27f9a')}
  `),
  // 佐賀 壺侍 — samurai in an Arita porcelain jar
  tsubozamurai: svg(`
    <path d="M52 22 q-2 -10 6 -12" fill="none" stroke="#2b2b2b" stroke-width="5" stroke-linecap="round"/>
    <circle cx="50" cy="34" r="14" fill="#f7dcc4" ${S}/>
    <path d="M36 30 Q40 18 50 20 Q60 18 64 30 Q56 26 50 28 Q44 26 36 30 Z" fill="#2b2b2b" ${S}/>
    ${eyes(50, 36, { gap: 6, r: 2.2 })}
    ${mouth(50, 42, 'flat', 6)}
    <path d="M36 46 H64 Q78 60 74 82 Q70 94 50 94 Q30 94 26 82 Q22 60 36 46 Z" fill="#eaf4fb" ${S}/>
    <path d="M40 60 q10 -8 20 0 q-10 8 -20 0 z" fill="#3b6fb6" opacity=".85"/>
    <circle cx="36" cy="76" r="3" fill="#3b6fb6"/><circle cx="64" cy="76" r="3" fill="#3b6fb6"/><circle cx="50" cy="84" r="3" fill="#3b6fb6"/>
    <path d="M30 66 q20 6 40 0" fill="none" stroke="#3b6fb6" stroke-width="2"/>
  `),
  // 長崎 がんばくん — orange cheerer with a red headband
  ganbakun: svg(`
    <circle cx="50" cy="58" r="30" fill="#f7a63b" ${S}/>
    <path d="M20 44 Q50 34 80 44 L80 52 Q50 42 20 52 Z" fill="#e0554b" ${S}/>
    <path d="M80 46 l10 -6 l-2 10" fill="#e0554b" ${THIN}/>
    ${eyes(50, 60, { gap: 10, r: 3.6 })}
    ${mouth(50, 70, 'grin', 12)}
    ${blush(50, 67, 20)}
  `),
  // 熊本 くまモン — black bear, white eyes, red cheeks
  kumamon: svg(`
    <circle cx="28" cy="32" r="9" fill="#1a1a1a" ${S}/><circle cx="72" cy="32" r="9" fill="#1a1a1a" ${S}/>
    <path d="M30 92 Q28 66 50 66 Q72 66 70 92 Z" fill="#1a1a1a" ${S}/>
    <ellipse cx="50" cy="50" rx="30" ry="26" fill="#1a1a1a" ${S}/>
    <ellipse cx="40" cy="46" rx="7" ry="8" fill="#fff"/><ellipse cx="60" cy="46" rx="7" ry="8" fill="#fff"/>
    <circle cx="41" cy="45" r="3.6" fill="#1a1a1a"/><circle cx="59" cy="45" r="3.6" fill="#1a1a1a"/>
    <circle cx="42" cy="44" r="1.1" fill="#fff"/><circle cx="60" cy="44" r="1.1" fill="#fff"/>
    <circle cx="28" cy="58" r="6" fill="#e0322b"/><circle cx="72" cy="58" r="6" fill="#e0322b"/>
    <ellipse cx="50" cy="58" rx="4" ry="3" fill="#333"/>
    <path d="M44 64 q6 5 12 0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
  `),
  // 大分 めじろん — green white-eye bird
  mejiron: svg(`
    <ellipse cx="22" cy="62" rx="10" ry="15" transform="rotate(20 22 62)" fill="#5fa53a" ${S}/><ellipse cx="78" cy="62" rx="10" ry="15" transform="rotate(-20 78 62)" fill="#5fa53a" ${S}/>
    <circle cx="50" cy="58" r="28" fill="#7fb36b" ${S}/>
    <ellipse cx="50" cy="72" rx="16" ry="11" fill="#d9e15a"/>
    ${eyes(50, 54, { gap: 10, r: 3, sclera: 5.5 })}
    <path d="M45 62 L50 68 L55 62 Z" fill="#f2c94c" ${THIN}/>
    ${blush(50, 62, 19)}
    <path d="M40 88 v5 M44 88 v5 M56 88 v5 M60 88 v5" fill="none" stroke="#f7a63b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 宮崎 みやざき犬 — three pups in hyuganatsu, phoenix-palm and chicken hats
  miyazakiken: svg(`
    <g>
      <circle cx="24" cy="40" r="9" fill="#f7a63b" ${THIN}/><path d="M24 31 q3 -4 6 -3" fill="none" stroke="#7fb36b" stroke-width="2" stroke-linecap="round"/>
      <circle cx="24" cy="58" r="15" fill="#f6ead6" ${S}/>
      ${eyes(24, 57, { gap: 5, r: 2 })}<ellipse cx="24" cy="63" rx="2" ry="1.4" fill="${INK}"/>
    </g>
    <g>
      <path d="M50 22 l-8 10 M50 22 l0 12 M50 22 l8 10 M50 22 l-14 4 M50 22 l14 4" fill="none" stroke="#5fa53a" stroke-width="3" stroke-linecap="round"/>
      <circle cx="50" cy="52" r="17" fill="#f6ead6" ${S}/>
      ${eyes(50, 51, { gap: 6, r: 2.2 })}<ellipse cx="50" cy="58" rx="2.2" ry="1.6" fill="${INK}"/>
    </g>
    <g>
      <path d="M70 34 q3 -8 6 0 q3 -8 6 0 q3 -8 6 0" fill="#e0554b" ${THIN}/>
      <path d="M62 44 l-6 3 l6 3 z" fill="#f2c94c" ${THIN}/>
      <circle cx="76" cy="58" r="15" fill="#f6ead6" ${S}/>
      ${eyes(76, 57, { gap: 5, r: 2 })}<ellipse cx="76" cy="63" rx="2" ry="1.4" fill="${INK}"/>
    </g>
    ${blush(24, 62, 9, 3, 1.8)}${blush(50, 56, 10, 3, 1.8)}${blush(76, 62, 9, 3, 1.8)}
  `),
  // 鹿児島 ぐりぶー — black pig with a pink snout
  greboo: svg(`
    <path d="M26 46 l-6 -12 l12 4 M74 46 l6 -12 l-12 4" fill="#2b2b2b" ${S}/>
    <circle cx="50" cy="58" r="28" fill="#2b2b2b" ${S}/>
    <ellipse cx="50" cy="66" rx="10" ry="7" fill="#f6b8c5" ${THIN}/>
    <circle cx="46.5" cy="66" r="1.6" fill="${INK}"/><circle cx="53.5" cy="66" r="1.6" fill="${INK}"/>
    ${eyes(50, 54, { gap: 11, r: 3, sclera: 5 })}
    ${blush(50, 62, 21, 4.4, 2.6, '#f27f9a')}
  `),
  // 沖縄 花笠マハエ — girl in a red hanagasa and a yellow bingata dress
  hanagasamahae: svg(`
    <path d="M22 40 Q26 16 50 14 Q74 16 78 40 L70 42 Q50 30 30 42 Z" fill="#e0554b" ${S}/>
    <path d="M22 40 q7 6 14 0 q7 6 14 0 q7 6 14 0 q7 6 14 0" fill="none" stroke="#9fd3f0" stroke-width="4" stroke-linecap="round"/>
    <circle cx="50" cy="52" r="18" fill="#f7dcc4" ${S}/>
    <path d="M32 48 Q34 36 50 36 Q66 36 68 48 Q58 44 50 46 Q42 44 32 48 Z" fill="#2b2b2b"/>
    <circle cx="30" cy="54" r="6" fill="#2b2b2b" ${THIN}/><circle cx="70" cy="54" r="6" fill="#2b2b2b" ${THIN}/>
    <path d="M26 92 Q28 68 50 68 Q72 68 74 92 Z" fill="#f5c800" ${S}/>
    <g><circle cx="40" cy="78" r="2.4" fill="#3b6fb6"/><circle cx="50" cy="84" r="2.4" fill="#e0554b"/><circle cx="60" cy="78" r="2.4" fill="#7fb36b"/><circle cx="46" cy="90" r="2" fill="#f5a3b3"/><circle cx="56" cy="90" r="2" fill="#3b6fb6"/></g>
    ${eyes(50, 52, { gap: 8, r: 2.8 })}
    ${mouth(50, 60, 'smile', 7)}
    ${blush(50, 57, 15)}
  `),
};

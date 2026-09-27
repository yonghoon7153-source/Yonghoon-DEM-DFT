// Likenesses of the real local mascots — Hokkaido → Chubu (ADR 0003). Drawn from memory; not official art.
import { INK, S, THIN, blush, eyes, face, mouth, svg } from './helpers';

export const artA: Record<string, string> = {
  // 北海道 キュンちゃん — a pika wearing an Ezo-deer hood
  kyunchan: svg(`
    <path d="M30 90 Q30 66 50 66 Q70 66 70 90 Z" fill="#f6ead6" ${S}/>
    <path d="M34 30 q-6 -12 -13 -14 M34 30 q-1 -12 4 -16 M66 30 q6 -12 13 -14 M66 30 q1 -12 -4 -16" fill="none" stroke="#8b6b4a" stroke-width="3" stroke-linecap="round"/>
    <path d="M20 62 Q16 24 50 20 Q84 24 80 62 Q66 58 50 60 Q34 58 20 62 Z" fill="#a8734a" ${S}/>
    <ellipse cx="22" cy="46" rx="8" ry="4.5" transform="rotate(-25 22 46)" fill="#a8734a" ${S}/><ellipse cx="78" cy="46" rx="8" ry="4.5" transform="rotate(25 78 46)" fill="#a8734a" ${S}/>
    <ellipse cx="50" cy="52" rx="19" ry="17" fill="#f6ead6" ${S}/>
    <ellipse cx="40" cy="38" rx="4" ry="6" fill="#f6ead6" ${THIN}/><ellipse cx="60" cy="38" rx="4" ry="6" fill="#f6ead6" ${THIN}/>
    ${eyes(50, 52, { gap: 8, r: 3.6 })}
    <ellipse cx="50" cy="58" rx="2" ry="1.4" fill="${INK}"/>
    ${mouth(50, 61, 'w', 6)}
    ${blush(50, 58, 14)}
  `),
  // 青森 いくべぇ — apple-red fairy with a nebuta bib
  ikubee: svg(`
    <path d="M50 26 v-9" fill="none" stroke="#7a5230" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="59" cy="21" rx="9" ry="4.5" transform="rotate(-25 59 21)" fill="#8fc47b" ${S}/>
    <circle cx="50" cy="56" r="30" fill="#e0322b" ${S}/>
    <path d="M30 70 Q50 84 70 70 L72 84 Q50 94 28 84 Z" fill="#3b6fb6" ${S}/>
    <path d="M36 76 q6 -4 12 0 q6 4 12 0" fill="none" stroke="#f2c94c" stroke-width="2.4" stroke-linecap="round"/>
    ${face(50, 54, { gap: 10, mouth: 'grin', blushDy: 6 })}
  `),
  // 岩手 わんこきょうだい（そばっち）— red lacquer wanko bowl with soba on top
  wankokyodai: svg(`
    <path d="M30 34 q6 -10 12 0 q6 10 12 0 q6 -10 12 0" fill="none" stroke="#e9dcb8" stroke-width="4" stroke-linecap="round"/>
    <path d="M22 44 H78 Q76 88 50 90 Q24 88 22 44 Z" fill="#c8302e" ${S}/>
    <ellipse cx="50" cy="44" rx="28" ry="8" fill="#2b2b2b" ${S}/>
    <ellipse cx="50" cy="66" rx="17" ry="14" fill="#f6ead6"/>
    ${face(50, 64, { gap: 8, mouth: 'smile', blushDy: 6 })}
  `),
  // 宮城 むすび丸 — onigiri head under Date Masamune's crescent helmet
  musubimaru: svg(`
    <path d="M28 30 Q50 -4 72 30 Q50 18 28 30 Z" fill="#f2c94c" ${S}/>
    <path d="M50 22 Q56 22 59 28 L84 70 Q87 78 79 80 L21 80 Q13 78 16 70 L41 28 Q44 22 50 22 Z" fill="#fff" ${S}/>
    <path d="M24 34 Q50 24 76 34 L70 42 Q50 34 30 42 Z" fill="#2b2b2b" ${S}/>
    <rect x="36" y="62" width="28" height="18" rx="3" fill="#2b2b2b" ${S}/>
    ${face(50, 50, { gap: 9, mouth: 'smile' })}
  `),
  // 秋田 んだッチ — small namahage robot with a white mane and straw cape
  ndacchi: svg(`
    <path d="M50 14 v-8 M46 8 h8" fill="none" ${S}/>
    <path d="M24 92 L34 60 H66 L76 92 Z" fill="#c9b27a" ${S}/>
    <path d="M40 66 v22 M50 64 v26 M60 66 v22" fill="none" stroke="#a48f5c" stroke-width="2" stroke-linecap="round"/>
    <g fill="#fff" ${S}><circle cx="26" cy="40" r="8"/><circle cx="30" cy="26" r="8"/><circle cx="50" cy="20" r="8"/><circle cx="70" cy="26" r="8"/><circle cx="74" cy="40" r="8"/><circle cx="26" cy="54" r="7"/><circle cx="74" cy="54" r="7"/></g>
    <path d="M40 26 L36 12 L46 22 Z M60 26 L64 12 L54 22 Z" fill="#c9c9c9" ${S}/>
    <circle cx="50" cy="44" r="22" fill="#e0554b" ${S}/>
    <path d="M36 38 l7 3 M64 38 l-7 3" fill="none" ${THIN}/>
    ${eyes(50, 44, { gap: 9, r: 3, sclera: 5 })}
    ${mouth(50, 53, 'grin', 14)}
    <path d="M44 52 l2 4 l2 -4 M52 52 l2 4 l2 -4" fill="#fff" ${THIN}/>
  `),
  // 山形 きてけろくん — yellow, profile shaped like Yamagata, cherries on top
  kitekerokun: svg(`
    <path d="M44 24 q0 -8 6 -12 M56 24 q0 -8 -6 -12" fill="none" stroke="#7a5230" stroke-width="2.2" stroke-linecap="round"/>
    <circle cx="42" cy="24" r="5" fill="#e0322b" ${THIN}/><circle cx="58" cy="24" r="5" fill="#e0322b" ${THIN}/>
    <path d="M50 30 C74 30 82 46 80 62 C78 82 66 90 50 90 C36 90 26 82 26 70 C18 70 14 60 22 56 C26 42 34 30 50 30 Z" fill="#f5c800" ${S}/>
    <path d="M22 56 q-6 6 0 12" fill="none" ${THIN}/>
    ${eyes(52, 54, { gap: 10, r: 3 })}
    ${mouth(52, 66, 'wide', 16)}
    ${blush(52, 60, 18)}
  `),
  // 福島 キビタン — yellow flycatcher with a black cap and wings
  kibitan: svg(`
    <ellipse cx="24" cy="60" rx="10" ry="16" transform="rotate(20 24 60)" fill="#2b2f4a" ${S}/><ellipse cx="76" cy="60" rx="10" ry="16" transform="rotate(-20 76 60)" fill="#2b2f4a" ${S}/>
    <circle cx="50" cy="56" r="28" fill="#f7d21b" ${S}/>
    <path d="M24 48 Q50 18 76 48 Q62 40 50 42 Q38 40 24 48 Z" fill="#2b2f4a" ${S}/>
    <path d="M44 60 L50 66 L56 60 Z" fill="#f7a63b" ${THIN}/>
    ${eyes(50, 54, { gap: 10, r: 3 })}
    ${blush(50, 62, 17)}
    <path d="M40 86 v6 M44 86 v6 M56 86 v6 M60 86 v6" fill="none" stroke="#f7a63b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 茨城 ハッスル黄門 — Mito Kōmon with white beard and a cane
  hassurukomon: svg(`
    <path d="M24 92 Q26 62 50 62 Q74 62 76 92 Z" fill="#6a4e96" ${S}/>
    <path d="M50 62 v30" fill="none" stroke="#f2c94c" stroke-width="3"/>
    <path d="M80 60 v34" fill="none" stroke="#8b6b4a" stroke-width="4" stroke-linecap="round"/>
    <rect x="76" y="70" width="8" height="10" rx="2" fill="#f2c94c" ${THIN}/>
    <circle cx="50" cy="44" r="21" fill="#f7dcc4" ${S}/>
    <path d="M30 40 Q34 22 50 22 Q66 22 70 40 Q60 34 50 36 Q40 34 30 40 Z" fill="#fff" ${S}/>
    <path d="M50 24 q0 -10 8 -12" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
    <path d="M36 34 h8 M56 34 h8" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M36 56 Q50 74 64 56 Q50 66 36 56 Z" fill="#fff" ${S}/>
    <path d="M40 50 q10 4 20 0" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
    ${eyes(50, 44, { gap: 8, r: 2.4 })}
    ${blush(50, 49, 15)}
  `),
  // 茨城 ねば～る君 — natto fairy, tall and sticky
  nebarukun: svg(`
    <path d="M32 92 Q26 40 50 32 Q74 40 68 92 Z" fill="#8b5a2b" ${S}/>
    <path d="M30 34 Q50 20 70 34 L66 40 Q50 32 34 40 Z" fill="#e8d5a3" ${S}/>
    <path d="M34 40 v-4 M42 36 v-4 M50 34 v-4 M58 36 v-4 M66 40 v-4" fill="none" stroke="#c9b27a" stroke-width="1.5"/>
    <ellipse cx="50" cy="58" rx="14" ry="12" fill="#c99b66"/>
    ${eyes(50, 56, { gap: 7, r: 2.6 })}
    ${mouth(50, 64, 'grin', 10)}
    ${blush(50, 61, 13)}
    <path d="M70 60 L92 46 M72 66 L92 58" fill="none" stroke="#8b6b4a" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M60 80 q4 8 0 14 M40 80 q-4 8 0 14" fill="none" stroke="#c9b27a" stroke-width="1.6" stroke-linecap="round"/>
  `),
  // 栃木 とちまるくん — leaf hat, yellow face, strawberry in hand
  tochimarukun: svg(`
    <path d="M28 92 Q28 66 50 66 Q72 66 72 92 Z" fill="#8cc63f" ${S}/>
    <path d="M50 30 C36 12 20 16 22 30 C26 40 40 40 50 30 Z M50 30 C64 12 80 16 78 30 C74 40 60 40 50 30 Z" fill="#5fa53a" ${S}/>
    <path d="M50 32 v-14" fill="none" ${THIN}/>
    <circle cx="50" cy="52" r="20" fill="#f5e05a" ${S}/>
    ${face(50, 51, { gap: 8, mouth: 'smile' })}
    <path d="M76 74 c-6 -6 -12 2 -6 8 c4 4 10 2 6 -8 z" fill="#e0322b" ${THIN}/><path d="M74 72 l4 -4" fill="none" stroke="#5fa53a" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 栃木 さのまる — ramen-bowl hat with noodle bangs, imo-fry katana
  sanomaru: svg(`
    <path d="M22 40 Q22 12 50 12 Q78 12 78 40 Z" fill="#fff" ${S}/>
    <path d="M26 30 h48 M28 36 h44" fill="none" stroke="#e0554b" stroke-width="2"/>
    <path d="M28 40 q6 8 12 0 q6 8 12 0 q6 8 12 0 q4 6 8 0" fill="none" stroke="#f0d79a" stroke-width="4" stroke-linecap="round"/>
    <circle cx="50" cy="54" r="18" fill="#f7dcc4" ${S}/>
    <path d="M28 92 Q30 70 50 70 Q70 70 72 92 Z" fill="#3b6fb6" ${S}/>
    <path d="M50 70 v22" fill="none" stroke="#fff" stroke-width="2"/>
    <path d="M70 76 L90 62" fill="none" stroke="#8b6b4a" stroke-width="4" stroke-linecap="round"/>
    <circle cx="78" cy="70" r="3.4" fill="#f2c94c" ${THIN}/><circle cx="85" cy="65" r="3.4" fill="#f2c94c" ${THIN}/>
    ${face(50, 54, { gap: 8, mouth: 'smile' })}
  `),
  // 群馬 ぐんまちゃん — tan pony with a dark mane and a green neckerchief
  gunmachan: svg(`
    <path d="M28 92 Q28 68 50 68 Q72 68 72 92 Z" fill="#e4c28c" ${S}/>
    <path d="M30 72 Q50 84 70 72 L70 80 Q50 90 30 80 Z" fill="#7fb36b" ${S}/>
    <path d="M30 40 L36 18 L46 34 Z M70 40 L64 18 L54 34 Z" fill="#e4c28c" ${S}/>
    <circle cx="50" cy="50" r="25" fill="#e4c28c" ${S}/>
    <path d="M32 40 Q40 22 52 30 Q60 22 68 38 Q58 32 50 36 Q42 32 32 40 Z" fill="#6b4a2b" ${S}/>
    <ellipse cx="50" cy="60" rx="13" ry="9" fill="#f6ead6"/>
    ${eyes(50, 50, { gap: 10, r: 3.4 })}
    <ellipse cx="46" cy="61" rx="1.6" ry="1.2" fill="${INK}"/><ellipse cx="54" cy="61" rx="1.6" ry="1.2" fill="${INK}"/>
    ${mouth(50, 65, 'smile', 8)}
    ${blush(50, 57, 18)}
  `),
  // 埼玉 コバトン — white dove with a red ribbon
  kobaton: svg(`
    <ellipse cx="24" cy="62" rx="10" ry="15" transform="rotate(25 24 62)" fill="#d8dde3" ${S}/><ellipse cx="76" cy="62" rx="10" ry="15" transform="rotate(-25 76 62)" fill="#d8dde3" ${S}/>
    <circle cx="50" cy="56" r="28" fill="#fdfdfd" ${S}/>
    <path d="M44 60 L50 66 L56 60 Z" fill="#f7a63b" ${THIN}/>
    <path d="M40 74 l10 -6 l10 6 l-10 6 z" fill="#e0554b" ${THIN}/>
    ${eyes(50, 54, { gap: 10, r: 3 })}
    ${blush(50, 62, 17)}
    <path d="M40 86 v6 M44 86 v6 M56 86 v6 M60 86 v6" fill="none" stroke="#f7a63b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 千葉 チーバくん — red, profile shaped like Chiba, big white eyes
  chibakun: svg(`
    <path d="M62 22 L66 6 L74 24 Z" fill="#e0322b" ${S}/>
    <path d="M28 44 C20 30 40 14 62 20 C82 26 84 54 74 70 C68 82 58 90 46 88 C30 86 22 72 24 58 C16 56 14 46 28 44 Z" fill="#e0322b" ${S}/>
    <path d="M22 52 Q30 50 34 56 Q30 62 22 60 Z" fill="#fff0d0" ${THIN}/>
    ${eyes(50, 48, { gap: 9, r: 3.4, sclera: 6 })}
    ${mouth(48, 62, 'wide', 16)}
    ${blush(50, 58, 20)}
    <path d="M38 88 v6 M58 88 v6" fill="none" stroke="#e0322b" stroke-width="5" stroke-linecap="round"/>
  `),
  // 千葉 ふなっしー — yellow pear fairy in blue overalls
  funassyi: svg(`
    <path d="M52 26 v-12" fill="none" stroke="#7a5230" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="62" cy="16" rx="9" ry="4.5" transform="rotate(-25 62 16)" fill="#8fc47b" ${S}/>
    <path d="M50 22 C34 22 26 46 26 64 C26 84 38 94 50 94 C62 94 74 84 74 64 C74 46 66 22 50 22 Z" fill="#f7d21b" ${S}/>
    <path d="M30 66 Q50 74 70 66 L72 90 Q50 96 28 90 Z" fill="#3b6fb6"/>
    <path d="M40 66 v-8 h20 v8" fill="none" stroke="#3b6fb6" stroke-width="5"/>
    ${eyes(50, 48, { gap: 10, r: 4.6 })}
    ${mouth(50, 58, 'grin', 14)}
    ${blush(50, 56, 19)}
  `),
  // 東京 ゆりーと — black-headed gull with a red beak and a sports headband
  yurito: svg(`
    <ellipse cx="22" cy="62" rx="10" ry="16" transform="rotate(25 22 62)" fill="#e6e9ee" ${S}/><ellipse cx="78" cy="62" rx="10" ry="16" transform="rotate(-25 78 62)" fill="#e6e9ee" ${S}/>
    <circle cx="50" cy="56" r="28" fill="#fdfdfd" ${S}/>
    <path d="M24 44 Q50 36 76 44 L76 50 Q50 42 24 50 Z" fill="#3b6fb6" ${S}/>
    <path d="M42 60 L50 68 L58 60 Z" fill="#e0554b" ${THIN}/>
    ${eyes(50, 54, { gap: 10, r: 3 })}
    ${blush(50, 62, 17)}
    <path d="M40 86 v6 M44 86 v6 M56 86 v6 M60 86 v6" fill="none" stroke="#e0554b" stroke-width="2.4" stroke-linecap="round"/>
  `),
  // 神奈川 かながわキンタロウ — Kintaro with a red 金 bib and an axe
  kanagawakintaro: svg(`
    <path d="M20 40 L44 24" fill="none" stroke="#8b6b4a" stroke-width="4" stroke-linecap="round"/>
    <path d="M14 34 l10 -8 l6 8 l-10 8 z" fill="#b8c0c8" ${S}/>
    <circle cx="52" cy="46" r="22" fill="#f7dcc4" ${S}/>
    <path d="M30 44 Q30 20 52 20 Q74 20 74 44 Q64 36 52 38 Q40 36 30 44 Z" fill="#2b2b2b" ${S}/>
    <path d="M30 92 Q32 66 52 66 Q72 66 74 92 Z" fill="#e0554b" ${S}/>
    <text x="52" y="86" font-size="16" font-weight="700" text-anchor="middle" fill="#fff" font-family="serif">金</text>
    ${eyes(52, 48, { gap: 9, r: 3 })}
    ${mouth(52, 56, 'smile', 8)}
    ${blush(52, 54, 16, 5.5, 3.2)}
  `),
  // 新潟 レルヒさん — Major Lerch in uniform with one ski pole
  lerchsan: svg(`
    <path d="M84 30 v62" fill="none" stroke="#8b6b4a" stroke-width="3.5" stroke-linecap="round"/><circle cx="84" cy="80" r="5" fill="none" ${THIN}/>
    <path d="M28 92 Q30 62 50 62 Q70 62 72 92 Z" fill="#6b7a3a" ${S}/>
    <path d="M50 62 v30" fill="none" stroke="#4a5528" stroke-width="2"/>
    <circle cx="44" cy="72" r="1.8" fill="#f2c94c"/><circle cx="44" cy="80" r="1.8" fill="#f2c94c"/>
    <circle cx="50" cy="46" r="20" fill="#f7dcc4" ${S}/>
    <path d="M28 36 Q30 18 50 18 Q70 18 72 36 Z" fill="#6b7a3a" ${S}/>
    <path d="M26 36 h48" fill="none" stroke="#2b2b2b" stroke-width="3.5" stroke-linecap="round"/>
    ${eyes(50, 46, { gap: 8, r: 2.6 })}
    <path d="M38 54 q12 -6 24 0 q-6 6 -12 4 q-6 2 -12 -4 z" fill="#4a3f3a"/>
    ${blush(50, 52, 15)}
  `),
  // 富山 きときと君 — sky-blue with a snowy Tateyama cap
  kitokitokun: svg(`
    <path d="M82 60 q14 -8 10 -22 q-6 8 -12 8" fill="#9fd3f0" ${S}/>
    <circle cx="50" cy="58" r="28" fill="#9fd3f0" ${S}/>
    <path d="M22 50 L36 26 L46 40 L56 22 L66 40 L78 50 Z" fill="#fff" ${S}/>
    ${face(50, 60, { gap: 10, mouth: 'smile' })}
  `),
  // 石川 ひゃくまんさん — daruma-like, red with Kaga patterns, gold face and mustache
  hyakumansan: svg(`
    <path d="M50 14 C76 14 86 42 84 66 C82 84 68 92 50 92 C32 92 18 84 16 66 C14 42 24 14 50 14 Z" fill="#c8302e" ${S}/>
    <g opacity=".9"><circle cx="26" cy="60" r="3" fill="#f2c94c"/><circle cx="74" cy="60" r="3" fill="#3b6fb6"/><circle cx="30" cy="78" r="3" fill="#7fb36b"/><circle cx="70" cy="78" r="3" fill="#f5a3b3"/><circle cx="50" cy="84" r="3" fill="#f2c94c"/><circle cx="22" cy="42" r="2.4" fill="#f5a3b3"/><circle cx="78" cy="42" r="2.4" fill="#7fb36b"/></g>
    <ellipse cx="50" cy="48" rx="22" ry="20" fill="#e8c15a" ${S}/>
    <path d="M36 38 q6 -6 12 0 M52 38 q6 -6 12 0" fill="none" stroke="#2b2b2b" stroke-width="3.5" stroke-linecap="round"/>
    ${eyes(50, 46, { gap: 8, r: 2.6 })}
    <path d="M34 56 q8 -8 16 0 q8 -8 16 0 q-8 6 -16 2 q-8 4 -16 -2 z" fill="#2b2b2b"/>
    ${blush(50, 54, 17, 4, 2.4, '#e0554b')}
  `),
  // 福井 はぴりゅう — friendly teal dinosaur with a yellow belly
  hapiryu: svg(`
    <path d="M74 70 q16 4 14 -12 q-6 8 -12 4" fill="#5cc4a8" ${S}/>
    <path d="M40 30 l6 -12 l6 12 M52 30 l6 -12 l6 12" fill="#f2c94c" ${THIN}/>
    <ellipse cx="50" cy="58" rx="30" ry="30" fill="#5cc4a8" ${S}/>
    <ellipse cx="50" cy="70" rx="16" ry="14" fill="#f7e08a"/>
    ${eyes(50, 52, { gap: 11, r: 3.6 })}
    ${mouth(50, 62, 'grin', 12)}
    ${blush(50, 59, 21)}
    <rect x="34" y="84" width="9" height="9" rx="4" fill="#5cc4a8" ${THIN}/><rect x="57" y="84" width="9" height="9" rx="4" fill="#5cc4a8" ${THIN}/>
  `),
  // 山梨 武田菱丸 — dog in Shingen's white-maned helmet, 武田菱 bib
  takedahishimaru: svg(`
    <path d="M30 36 q-10 12 -8 30 M70 36 q10 12 8 30" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>
    <path d="M30 36 q-10 12 -8 30 M70 36 q10 12 8 30" fill="none" ${THIN}/>
    <circle cx="50" cy="52" r="23" fill="#fff8f0" ${S}/>
    <path d="M27 44 Q30 22 50 22 Q70 22 73 44 Q60 36 50 38 Q40 36 27 44 Z" fill="#2b2b2b" ${S}/>
    <path d="M44 26 l6 -12 l6 12" fill="#f2c94c" ${THIN}/>
    <ellipse cx="50" cy="60" rx="3" ry="2.2" fill="${INK}"/>
    ${eyes(50, 52, { gap: 9, r: 3 })}
    ${mouth(50, 63, 'w', 8)}
    <path d="M32 74 Q50 84 68 74 L70 90 Q50 98 30 90 Z" fill="#e0554b" ${S}/>
    <g fill="#2b2b2b"><path d="M46 78 l4 -4 l4 4 l-4 4 z"/><path d="M54 78 l4 -4 l4 4 l-4 4 z"/><path d="M46 86 l4 -4 l4 4 l-4 4 z"/><path d="M54 86 l4 -4 l4 4 l-4 4 z"/></g>
  `),
  // 長野 アルクマ — white bear in an apple hat
  arukuma: svg(`
    <circle cx="28" cy="40" r="8" fill="#fff8f0" ${S}/><circle cx="72" cy="40" r="8" fill="#fff8f0" ${S}/>
    <circle cx="50" cy="58" r="26" fill="#fff8f0" ${S}/>
    <path d="M50 22 v-8" fill="none" stroke="#7a5230" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="58" cy="16" rx="8" ry="4" transform="rotate(-25 58 16)" fill="#8fc47b" ${S}/>
    <path d="M26 42 Q28 18 50 20 Q72 18 74 42 Q62 34 50 36 Q38 34 26 42 Z" fill="#e0322b" ${S}/>
    <ellipse cx="50" cy="66" rx="11" ry="8" fill="#fbeee4"/>
    ${eyes(50, 56, { gap: 10, r: 3 })}
    <ellipse cx="50" cy="63" rx="3" ry="2.2" fill="${INK}"/>
    ${mouth(50, 68, 'w', 8)}
    ${blush(50, 63, 18)}
  `),
  // 岐阜 ミナモ — water sprite with a droplet head
  minamo: svg(`
    <path d="M50 10 C64 34 72 44 72 58 C72 74 62 86 50 86 C38 86 28 74 28 58 C28 44 36 34 50 10 Z" fill="#8fd0ec" ${S}/>
    <path d="M36 72 q7 -5 14 0 q7 5 14 0" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>
    ${eyes(50, 56, { gap: 9, r: 4.2 })}
    ${mouth(50, 66, 'smile', 8)}
    ${blush(50, 62, 17)}
    <rect x="36" y="84" width="10" height="8" rx="4" fill="#8fd0ec" ${THIN}/><rect x="54" y="84" width="10" height="8" rx="4" fill="#8fd0ec" ${THIN}/>
  `),
  // 静岡 ふじっぴー — Mt. Fuji with a face
  fujippi: svg(`
    <path d="M50 16 L92 88 H8 Z" fill="#3a75c4" ${S}/>
    <path d="M50 16 L70 50 Q64 44 60 52 Q55 42 50 52 Q45 42 40 52 Q36 44 30 50 Z" fill="#fff" ${S}/>
    ${eyes(50, 64, { gap: 10, r: 3.6 })}
    ${mouth(50, 74, 'grin', 12)}
    ${blush(50, 70, 20)}
    <path d="M18 70 q-8 2 -6 8 M82 70 q8 2 6 8" fill="none" stroke="#3a75c4" stroke-width="5" stroke-linecap="round"/>
  `),
  // 愛知 モリゾー＆キッコロ — fuzzy forest spirits, big and small
  morizokiccoro: svg(`
    <path d="M40 22 l6 8 l8 -10 l6 10 l8 -6 l2 12 l10 0 l-6 10 l8 6 l-10 4 l6 10 l-12 -2 l0 12 l-10 -6 l-6 10 l-6 -10 l-10 6 l0 -12 l-12 2 l6 -10 l-10 -4 l8 -6 l-6 -10 l10 0 l2 -12 z" fill="#7fb36b" ${S}/>
    <path d="M44 40 q6 -6 12 0 M60 40 q6 -6 12 0" fill="none" stroke="#2b2b2b" stroke-width="3.5" stroke-linecap="round"/>
    ${eyes(58, 46, { gap: 8, r: 2.6 })}
    <path d="M44 56 q14 -8 28 0 q-6 8 -14 6 q-8 2 -14 -6 z" fill="#fff" ${THIN}/>
    <path d="M14 66 l4 5 l5 -6 l4 6 l5 -3 l1 7 l6 0 l-4 6 l5 4 l-6 2 l3 6 l-7 -1 l0 7 l-6 -4 l-4 6 l-4 -6 l-6 4 l0 -7 l-7 1 l3 -6 l-6 -2 l5 -4 l-4 -6 l6 0 l1 -7 l5 3 z" fill="#c9e67a" ${S}/>
    <path d="M22 66 q-2 -8 4 -10" fill="none" stroke="#5fa53a" stroke-width="2.4" stroke-linecap="round"/>
    ${eyes(22, 80, { gap: 5, r: 2.4 })}
    ${mouth(22, 87, 'smile', 5)}
  `),
};

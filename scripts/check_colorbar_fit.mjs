/* 컬러바 글줄 맞춤 검사 — `fitTextLines` 가 폭을 넘기지 않는가.
 *
 * ★ 왜 있나 (2026-08-31): 컬러바 제목을 정직한 이름으로 고치자마자 PNG 에서 **오른쪽이
 *   잘렸다**.  하필 잘려 나간 것이 `— NOT a contact count` 라는 **경고 문구**였고, 잘린
 *   그림은 여전히 그럴듯해 보인다 = 조용한 실패.  라벨이 정직해질수록 길어지므로 사람
 *   눈에 기댈 수 없다.  ⇒ 폭 초과를 기계가 본다.
 *
 * 실행: node scripts/check_colorbar_fit.mjs
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const src = readFileSync(join(here, '..', 'webapp', 'static', 'js', 'viewer3d.js'), 'utf8');

//  브라우저 전용 모듈이라 통째로 import 하면 죽는다 — 순수 함수 하나만 떼어 낸다.
const m = src.match(/export function fitTextLines\([\s\S]*?\n}\n/);
if (!m) { console.error('FAIL — fitTextLines 를 소스에서 못 찾았다 (이름이 바뀌었나)'); process.exit(1); }
const fitTextLines = new Function(m[0].replace(/^export /, '') + '; return fitTextLines;')();

//  글자폭 스텁 — 실제 Arial 은 아니지만 **선형 근사**로 충분하다 (검사 대상은 맞춤 논리다).
const measure = (t, px) => String(t).length * px * 0.52;

let fails = 0;
const chk = (msg, ok, extra) => {
  console.log((ok ? '  ok   ' : '  FAIL ') + msg + (!ok && extra ? `  [${extra}]` : ''));
  if (!ok) fails++;
};
const W = 470 * 6, BASE = 13 * 6, MIN = 8.5 * 6;
const widest = (r) => Math.max(0, ...r.lines.map(l => measure(l, r.px)));

//  ① 실물 — 이 제목이 바로 잘렸던 것이다.
const REAL = 'Carbon wiring — carbon-point density near AM, arb. units (joint scale) — NOT a contact count';
const r1 = fitTextLines(measure, REAL, W, BASE, MIN, 2);
chk('실물 제목이 폭 안에 든다', widest(r1) <= W, `${widest(r1).toFixed(0)} > ${W}`);
chk('실물 제목이 2줄 이하', r1.lines.length <= 2, `${r1.lines.length}줄`);
chk('실물 제목이 한 글자도 안 잘린다',
    r1.lines.join(' ').replace(/\s+/g, ' ') === REAL.replace(/\s+/g, ' '),
    r1.lines.join(' | '));

//  ② 짧은 제목은 기본 글꼴 그대로 한 줄 (과잉 축소 방지 = 회귀).
const r2 = fitTextLines(measure, '|J| (normalized)', W, BASE, MIN, 2);
chk('짧은 제목은 축소도 줄바꿈도 없다', r2.px === BASE && r2.lines.length === 1,
    `px=${r2.px} lines=${r2.lines.length}`);

//  ③ 부제도 같은 논리로 맞는다.
const SUB = 'weighted point count within r + 0.3 µm of the AM centre; pattern comparison only';
const r3 = fitTextLines(measure, SUB, W, 9.5 * 6, 7 * 6, 2);
chk('부제가 폭 안에 든다', widest(r3) <= W, `${widest(r3).toFixed(0)}`);

//  ④ ★ 음성 — 터무니없이 긴 제목도 **자르지 않는다** (줄이 늘 뿐).
const LONG = Array.from({ length: 40 }, (_, i) => `word${i}`).join(' ');
const r4 = fitTextLines(measure, LONG, W, BASE, MIN, 2);
chk('과길이 제목도 글자를 버리지 않는다',
    r4.lines.join(' ') === LONG, `${r4.lines.length}줄`);

//  ⑤ ★ 음성 — 한 낱말이 혼자 폭을 넘으면?  greedy 가 못 자르므로 그 줄은 넘친다.
//    잘라내는 것보다 넘치는 편이 낫다(내용 보존)는 **의도된 선택**임을 여기 못 박는다.
const HUGE = 'X'.repeat(400);
const r5 = fitTextLines(measure, HUGE, W, BASE, MIN, 2);
chk('한 낱말이 폭을 넘어도 최소 글꼴까지 줄이고 내용을 보존한다',
    r5.px === MIN && r5.lines.join('') === HUGE, `px=${r5.px}`);

//  ⑥ 빈 입력.
chk('빈 제목은 빈 줄 목록', fitTextLines(measure, '', W, BASE, MIN, 2).lines.length === 0);
chk('null 제목도 안 죽는다', fitTextLines(measure, null, W, BASE, MIN, 2).lines.length === 0);

//  ⑦ ★ 실물 소스가 실제로 그 맞춤을 **쓰는가** (함수만 있고 안 부르면 무용).
chk('exportColorbarPNG 가 fitTextLines 를 쓴다',
    /const tFit = fitTextLines\(/.test(src) && /cx\.font = `600 \$\{tFit\.px\}px/.test(src));
chk('제목을 고정폭으로 다시 그리지 않는다', !/cx\.fillText\(sp\.title,/.test(src));
chk('부제도 맞춤 결과로 그린다', !/cx\.fillText\(String\(sp\.sub\),/.test(src));

console.log(`\n${fails} failure(s)`);
process.exit(fails ? 1 : 0);

/* 컬러바 글줄 맞춤 검사 — `fitTextLines` 가 폭을 넘기지 않는가.
 *
 * ★ 왜 있나 (2026-08-31): 컬러바 제목을 정직한 이름으로 고치자마자 PNG 에서 **오른쪽이
 *   잘렸다**.  하필 잘려 나간 것이 `— NOT a contact count` 라는 **경고 문구**였고, 잘린
 *   그림은 여전히 그럴듯해 보인다 = 조용한 실패.  라벨이 정직해질수록 길어지므로 사람
 *   눈에 기댈 수 없다.  ⇒ 폭 초과를 기계가 본다.
 *
 * ★★ 2026-09-02 — **두 번째 텍스트 면이 있었다.**  위 검사는 *제목*만 봤고, 그 사이
 *   **눈금 라벨**이 51개 겹쳐 찍혀 SI 그림이 통째로 읽을 수 없게 나왔다 (실측 export).
 *   `_focusTicks` 의 간격 사다리가 `top > 60 → 20` 에서 멈춰, focusing 이 10³ 급인
 *   전자 필드에서 개수에 상한이 없었다.  제목은 잘 맞았고 검사도 초록이었다.
 *   ⇒ 같은 관심사(**컬러바가 읽히는가**)이므로 파일을 나누지 않고 여기 합친다.
 *   ⚠ 이 부류는 **값이 맞고 읽을 수만 없다** — 숫자를 보는 어떤 검사기도 못 잡는다.
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

//  ⑧ ★★ 2026-08-31 — export 제목이 상을 **틀리게 부르지 않는가**.
//    세는 상은 VGCF · SuperP · **SDCP** · SWCNT 인데 SDCP 는 전도성 **고분자**이지
//    탄소가 아니다.  'Carbon …' 으로 되돌아가면 라벨이 정의와 어긋난다.
//    ⚠ 그림 속 글자는 ban-sweep 도 pptx 스윕도 못 읽는다 — 여기가 유일한 방어선이다.
{
  //  ⚠ 작은따옴표와 **템플릿 리터럴** 둘 다 잡는다 — 제목이 `${…}` 로 바뀌자
  //    작은따옴표만 보던 초판이 하나를 놓쳤고, 아래 '검사가 헛돌지 않는다' 가 그것을 물었다.
  const titles = [...src.matchAll(/title:\s*(?:'([^']*)'|`([^`]*)`)/g)]
                   .map(m => m[1] ?? m[2]);
  const exportTitles = titles.filter(t => /near AM/.test(t));
  chk('export 제목을 찾았다 (검사가 헛돌지 않는다)', exportTitles.length >= 2,
      `found=${exportTitles.length}`);
  chk('★★ export 제목이 상을 Carbon 으로 부르지 않는다 (SDCP 는 고분자다)',
      exportTitles.every(t => !/carbon/i.test(t)),
      exportTitles.filter(t => /carbon/i.test(t)).join(' | '));
  chk('export 제목이 conductive-additive 로 부른다',
      exportTitles.every(t => /conductive-additive/i.test(t)));
  chk('영국식 철자가 export 문구에 없다',
      !/'[^']*\b(centre|colour|behaviour)\b[^']*'/i.test(
        src.match(/cbarSpec = \{[\s\S]{0,600}?\};/)?.[0] || ''));
}

//  ══ 눈금 라벨 — 개수가 묶여 있는가 (2026-09-02) ═══════════════════════
{
  const ci = src.indexOf('const FOCUS_MAX_TICKS');
  const fi = src.indexOf('function _focusTicks');
  if (ci < 0 || fi < 0) {
    chk('★★ _focusTicks / FOCUS_MAX_TICKS 를 소스에서 찾는다', false, '이름이 바뀌었나');
  } else {
    const end = src.indexOf('\n}', fi);
    const body = src.slice(ci, src.indexOf('\n', ci)) + '\n' + src.slice(fi, end + 2);
    const { _focusTicks, FOCUS_MAX_TICKS } =
      new Function(body + '\nreturn { _focusTicks, FOCUS_MAX_TICKS };')();
    const CAP = FOCUS_MAX_TICKS + 2;                 // 0 과 상단 라벨은 언제나 붙는다

    //  ★ 실제로 뭉갠 값 + 자릿수를 가로지르는 표본
    for (const top of [1.5, 5, 11.7, 60, 120, 1190, 3.85e3, 2.8e4, 1e6]) {
      const t = _focusTicks({ focus_top: top });
      chk(`눈금 개수 상한: top=${top}`, t && t.length >= 3 && t.length <= CAP,
          `${t ? t.length : 'null'}개 > ${CAP}`);
    }
    const q = _focusTicks({ focus_top: 3.85e3 });
    chk('눈금 양 끝이 0 과 1', q[0].p === 0 && q[q.length - 1].p === 1);
    chk('눈금 p 가 단조 증가', q.every((x, i) => i === 0 || x.p > q[i - 1].p));
    chk('마지막 눈금이 기준량을 밝힌다 (⟨J⟩)', /⟨J⟩$/.test(q[q.length - 1].label));
    chk('눈금 라벨에 부동소수 찌꺼기가 없다',
        q.every(x => !/\d\.\d{6,}/.test(x.label)), JSON.stringify(q.map(x => x.label)));
    chk('top 이 없거나 비정상이면 눈금을 안 그린다 (fail-closed)',
        _focusTicks({}) === null && _focusTicks(null) === null &&
        [0, -1, NaN, Infinity].every(v => _focusTicks({ focus_top: v }) === null));

    //  ★ 자기 민감도 — 옛 사다리를 되돌리면 이 검사가 빨간불이어야 한다
    const OLD = (top) => {
      const step = top > 60 ? 20 : top > 30 ? 10 : top > 12 ? 5 : top > 6 ? 2 : 1;
      let n = 2;
      for (let v = step; v < top * 0.86; v += step) n++;
      return n;
    };
    chk('★★ 옛 사다리는 top=1190 에서 상한을 넘긴다 = 이 검사가 민감하다',
        OLD(1190) > CAP, `옛 개수 ${OLD(1190)}`);
  }
}

console.log(`\n${fails} failure(s)`);
process.exit(fails ? 1 : 0);

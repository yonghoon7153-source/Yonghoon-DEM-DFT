/* 세미나 화면 회귀 — **JS 를 실제로 돌려** 거부가 화면에 뜨는지 본다.
 *
 *   node webapp/test_seminar_dom.mjs
 *
 * ═══ 왜 이 파일이 있나 (R19 Q1c) ═══
 *
 * `test_seminar_page.py` 는 API 만 보고, 화면은 HTML 을 **문자열로 훑을** 뿐이다.
 * 그래서 `renderDeck()` 의 거부 분기를 통째로 들어내도 그 검사는 초록이다 — 서버는
 * 사유를 주는데 화면은 빈 페이지인 상태가 검사를 통과한다.  거부는 **보여야** 거부다.
 *
 * ⚠ 브라우저를 띄우지 않는다.  템플릿에서 `<script>` 본문을 떼어 최소 DOM·fetch 껍데기
 *   위에서 실행하고, 그 결과 `#smRoot` 에 **무엇이 들어갔는지**를 본다.  껍데기가
 *   진짜 브라우저는 아니므로 CSS·레이아웃은 보지 못한다 — 여기서 보는 것은
 *   *"사유가 DOM 에 도달하는가"* 하나다.
 *
 * ★ 자기 민감도를 스스로 증명한다: `--selftest` 는 거부 분기를 **제거한 사본**으로 한 번
 *   더 돌려, 그때 이 검사가 실제로 빨간불이 되는지 확인한다.  안 되면 이 파일은
 *   아무것도 지키지 않는 것이다.
 */
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const TPL = join(HERE, 'templates', 'seminar.html');

let ok = 0;
const bad = [];
function chk(name, cond) {
  if (cond) { ok++; console.log('  PASS  ' + name); }
  else { bad.push(name); console.log('  FAIL  ' + name); }
}

/** 템플릿에서 `<script>` 본문만. */
function script() {
  const html = readFileSync(TPL, 'utf8');
  const i = html.indexOf('<script>'), j = html.lastIndexOf('</script>');
  if (i < 0 || j < 0) throw new Error('seminar.html 에 <script> 블록이 없다');
  return html.slice(i + '<script>'.length, j);
}

/** 최소 DOM.  innerHTML 은 **문자열로 보관**한다 — 우리가 보려는 것이 그것이다. */
function makeDoc() {
  const els = new Map();
  const mk = (id) => ({
    id, innerHTML: '', textContent: '', hidden: false, value: '', dataset: {},
    tagName: 'DIV', classList: { toggle() {}, add() {}, remove() {} },
    addEventListener(k, f) { (this._on ||= {})[k] = f; },
    querySelectorAll() { return []; },
  });
  const get = (id) => { if (!els.has(id)) els.set(id, mk(id)); return els.get(id); };
  return {
    els,
    document: {
      getElementById: get,
      querySelectorAll: () => [],
      addEventListener() {},
    },
  };
}

/** 스크립트를 한 번 돌리고, 통신이 가라앉은 뒤 `#smRoot` 의 내용을 준다. */
async function render(src, payload) {
  const { els, document } = makeDoc();
  const window = { location: '' };
  const fetch = async (url) => ({
    ok: true,
    headers: { get: () => 'application/json' },
    json: async () => payload,
    _url: url,
  });
  const alert = () => {};
  const fn = new Function('document', 'window', 'fetch', 'alert', 'setTimeout',
                          'clearTimeout', 'console', src);
  fn(document, window, fetch, alert, setTimeout, clearTimeout, console);
  await new Promise((r) => setTimeout(r, 0));   // fetch 프라미스가 풀리게
  await new Promise((r) => setTimeout(r, 0));
  return { root: els.get('smRoot')?.innerHTML ?? '', els };
}

const REFUSAL = {
  ok: false, retracted: true,
  error: '⛔ 이 덱은 2026-08-06 발표 기록이고 안의 SDCP 수치는 철회됐습니다.',
  hint: '이력으로 열람하려면 ?historical=1',
  evidence_ref: 'docs/reviews/claims.json',
  evidence_claim: 'CL-24',
};
const DECK = {
  ok: true, deck: 'x.pptx', n_slides: 2,
  slides: [{ n: 1, title: '첫 장', lead: [], notes: 'n1' },
           { n: 2, title: '둘째 장', lead: [], notes: 'n2' }],
};

async function main() {
  const src = script();

  //  ── ① 거부가 화면에 **도달**하는가 ────────────────────────────────
  const r = await render(src, REFUSAL);
  chk('1) ★★ 거부 사유가 DOM 에 실린다 (빈 페이지 금지)',
      r.root.includes('철회') && r.root.length > 40);
  chk('2) ★★ 다음 행동(hint)도 함께 뜬다', r.root.includes('historical=1'));
  chk('3) ★★ 근거 경로가 화면에 뜬다 — 사유만 있으면 확인할 자리가 없다',
      r.root.includes('claims.json'));
  chk('4) ★★ 근거 항목 번호도 뜬다', r.root.includes('CL-24'));
  chk('5) ★ 거부 상태에서 슬라이드 본문이 새지 않는다',
      !r.root.includes('sm-wrap') && !r.root.includes('sm-nav'));
  chk('6) ★ 거부는 오류 스타일로 표시된다 (안내와 구분)', r.root.includes('sm-err'));

  //  ── ② 정상 경로도 여전히 그린다 (거부만 보면 게이트를 켜 둔 채 썩는다) ──
  const d = await render(src, DECK);
  chk('7) ★★ ok 인 덱은 슬라이드로 그려진다',
      d.root.includes('sm-wrap') && d.root.includes('첫 장'));
  chk('8) ★ 장 이동 막대가 그려진다', d.root.includes('sm-nav'));

  //  ── ③ ★ 이 검사가 **민감한가** — 거부 분기를 들어내면 빨간불이어야 한다 ──
  //     들어내는 방식은 Codex 가 제시한 것과 같다: 분기를 죽여 화면이 조용해지게 한다.
  const gutted = src.replace('if (!deckData.ok) {', 'if (false) {');
  chk('9) ★ 돌연변이가 실제로 적용됐다 (원본과 다르다)', gutted !== src);
  const g = await render(gutted, REFUSAL);
  chk('10) ★★ 분기를 들어내면 사유가 화면에서 사라진다 = 검사 ①이 민감하다',
      !g.root.includes('철회'));

  console.log(`\ntest_seminar_dom: ${ok}/${ok + bad.length} PASS`
              + (bad.length ? '   FAILED: ' + JSON.stringify(bad) : ''));
  process.exit(bad.length ? 1 : 0);
}

main().catch((e) => { console.error('⛔', e); process.exit(2); });

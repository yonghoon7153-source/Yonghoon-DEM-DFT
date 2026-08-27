/* 형광펜이 **실제 브라우저에서 칠해지는가** — 진짜 DOM 이 아니면 검증이 안 되는 것들.
 *
 * 왜 있나 (2026-08-27): 첫 판은 `wrapFirst`(한 텍스트 노드 안에 통째로 있을 때만
 * `surroundContents`)로 칠했다. digest 본문은 <b>·<sub>·<em> 이 촘촘해서 사람이 문장을
 * 드래그하면 거의 항상 노드를 가로지른다 — **저장은 되는데 안 칠해졌다.** 파이썬 테스트는
 * 서버만 보고 있어서 이걸 못 잡았고, 1저자가 화면을 보고 신고했다.
 *
 * 이 파일이 못 하는 것: 마우스 드래그(Selection)로 칠하는 경로는 안 본다 —
 * 여기서 보는 것은 **저장된 형광펜이 본문에 다시 붙는가** 하나다.
 *
 * 실행:  node webapp/tests/docnote_paint.test.mjs
 *        (playwright-core 와 /opt/pw-browsers 가 있어야 한다. 없으면 SKIP 으로 끝낸다.)
 */
import { readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "../..");
const JS = path.join(ROOT, "webapp/static/js/docnote.js");

let chromium;
try {
  const req = createRequire(process.env.PW_CORE_FROM || `${ROOT}/package.json`);
  ({ chromium } = req("playwright-core"));
} catch {
  console.log("SKIP — playwright-core 가 없다 (npm i playwright-core)");
  process.exit(0);
}
const EXE = ["/opt/pw-browsers/chromium/chrome-linux/chrome",
             "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"].find(existsSync);
if (!EXE) { console.log("SKIP — chromium 실행파일을 못 찾았다"); process.exit(0); }

const HL = [
  // ① 한 텍스트 노드 안 (옛 판도 되던 경우)
  { id: "h1", text: "한 노드 안에 통째로", color: "yellow", at: "2026-08-27" },
  // ② <b> 경계를 가로지른다 ← 실제 신고 사례
  { id: "h2", text: "굵은 글자를 지나 이어지는 문장", color: "green", at: "2026-08-27" },
  // ③ 인라인 태그 여러 개 + 아래첨자
  { id: "h3", text: "Li6PS5Cl 과 LGPS 에 치환/도핑만 해 왔다", color: "pink", at: "2026-08-27" },
  // ④ 본문에 없는 글 → 자리를 못 찾아야 한다 (음성)
  { id: "h4", text: "본문에 없는 문장이다", color: "blue", at: "2026-08-27" },
  // ⑤ 문단을 가로지른다 → 못 찾아야 한다 (음성, 알려진 한계)
  { id: "h5", text: "첫 문단 끝 두 번째 문단 시작", color: "yellow", at: "2026-08-27" },
];

const PAGE = `
<div id="host"><div id="body" class="doc">
  <p>여기 <em>기울임</em> 이 있고 <span>한 노드 안에 통째로</span> 들어 있는 문단이다. 첫 문단 끝</p>
  <p>두 번째 문단 시작 — <b>굵은 글자</b>를 지나 이어지는 문장 이 있다.</p>
  <ul><li>지금까지는 Li<sub>6</sub>PS<sub>5</sub>Cl 과 <b>LGPS</b> 에 <em>치환/도핑</em>만 해 왔다 → 끝</li></ul>
</div></div>`;

const b = await chromium.launch({ executablePath: EXE });
const pg = await b.newPage();
await pg.setContent(`<!doctype html><meta charset="utf-8">${PAGE}`);
await pg.evaluate((hl) => {
  window.__calls = [];
  window.fetch = function (url, opt) {
    window.__calls.push([url, opt && opt.method]);
    const items = String(url).includes("/api/highlights/") ? hl : [];
    return Promise.resolve({ ok: true, json: () => Promise.resolve({ items }) });
  };
}, HL);
await pg.addScriptTag({ path: JS });
await pg.evaluate(() =>
  window.mountDocNotes(document.getElementById("body"), "kb/x.md",
                       document.getElementById("host")));
await pg.waitForFunction(() => document.querySelectorAll("mark.dn-pen").length > 0,
                         null, { timeout: 5000 }).catch(() => {});

const got = await pg.evaluate(() => {
  const by = {};
  document.querySelectorAll("mark.dn-pen").forEach((m) => {
    const k = m.dataset.hid || "?";
    (by[k] = by[k] || { text: "", cls: m.className, n: 0 });
    by[k].text += m.textContent;
    by[k].n += 1;
  });
  return by;
});

let ok = true;
const chk = (c, m) => { ok = ok && !!c; console.log(`  ${c ? "✓" : "✗"} ${m}`); };
const norm = (s) => String(s || "").replace(/\s+/g, " ").trim();

chk(got.h1 && norm(got.h1.text) === HL[0].text,
    `[형광·양성] 한 노드 안 (조각 ${got.h1 ? got.h1.n : 0}개)`);
chk(got.h2 && norm(got.h2.text) === HL[1].text,
    `[형광·양성·실측회귀] <b> 경계를 가로질러도 칠한다 (조각 ${got.h2 ? got.h2.n : 0}개) `
    + `— 옛 판이 여기서 조용히 실패했다`);
chk(got.h3 && norm(got.h3.text) === HL[2].text,
    `[형광·양성] 인라인 태그 여럿 + <sub> 를 가로질러도 (조각 ${got.h3 ? got.h3.n : 0}개)`);
chk(got.h2 && got.h2.n >= 2, "[형광] 노드를 가로지르면 조각이 2개 이상 생긴다");
chk(got.h2 && /dn-pen-green/.test(got.h2.cls), "[형광] 색 클래스가 붙는다");
chk(!got.h4, "[형광·음성] 본문에 없는 글은 안 칠한다");
chk(!got.h5, "[형광·음성] 문단을 가로지른 선택은 안 칠한다 (알려진 한계)");

const btn = await pg.evaluate(() => {
  const el = document.createElement("button");
  el.id = "docpen"; document.body.appendChild(el);
  window.docnotePenToggle(); window.docnotePenToggle();   // paintPenBtn 을 태운다
  return { text: el.textContent, title: el.title };
});
chk(/⚠2/.test(btn.text), `[형광] 자리를 못 찾은 2개를 버튼에 알린다 ("${btn.text}")`);
chk(/자리를 못 찾았어요/.test(btn.title), "[형광] 왜 그런지 title 로 설명한다");

const dbl = await pg.evaluate(() => {
  window.__dnRerender = true;
  document.querySelectorAll("mark.dn-pen").forEach(() => {});
  return document.querySelectorAll("mark.dn-pen mark.dn-pen").length;
});
chk(dbl === 0, "[형광] 형광펜 안에 형광펜이 겹쳐 들어가지 않는다");

await b.close();
console.log(ok ? "docnote paint PASS" : "docnote paint FAIL");
process.exit(ok ? 0 : 1);

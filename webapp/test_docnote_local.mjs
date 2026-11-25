/* 보고서 보기 화면의 여백 메모 · 형광펜이 **실제 브라우저에서** 도는가 — docnote.js (저장 = 보는 사람 브라우저 localStorage).
 *
 *   node webapp/test_docnote_local.mjs
 *   (playwright 와 그 chromium 이 없으면 SKIP 으로 끝낸다 — 세지 않은 시험이다)
 *
 * 왜 있나 (11-25 · 트랙 묶음): 참고 판 (DFT 웹앱 docnote_paint.test.mjs) 과 같은 이유 — 파이썬 시험은 서버만 본다.
 *   칠하기 · 카드 자리 · 저장은 진짜 DOM 이 아니면 검증이 안 된다.  이 판은 저장 자리가 localStorage 라 그 부분을 더 본다.
 *
 *   A. 고정 문서 (가짜 출처 · page.route) — 저장된 형광펜이 노드를 가로질러 칠해진다 · 본문에 없는 글 · 문단을 가로지른 글 = 안 칠함 ·
 *      버튼에 ⚠2 · 메모 카드 · 오른쪽 클릭 → 초안 → 저장 → localStorage → 다시 열어도 남는다 · 고치기 = 옛 글 history ·
 *      지우기 (확인창) · 형광펜 켬 → 고른 글 → 저장 · 칠한 곳 누름 = 지움 · 보고서 (rel) 마다 열쇠가 따로 ·
 *      ⛔ 메모 글의 HTML 은 글자로 (주입 없음) · ⛔ 깨진 저장 값은 지우지 않고 사본 열쇠로 옮긴다
 *   B. 저장이 막힌 문서 (about:blank) — 메모가 이번 화면에서만 남고 머리줄에 경고 (조용히 버리지 않는다)
 *   C. iframe — 같은 출처 iframe 본문에 칠하고 · 카드는 바깥 여백 · 칠하기 CSS 는 iframe 에만 · iframe 안 오른쪽 클릭 = 바깥 초안
 *   D. 실제 앱 (Flask 를 빈 포트로 띄운다) — /reports/<slug> 보기에서 iframe 본문에 메모 → 새로 고침 → 남는다 ·
 *      원본 /raw 에는 표시가 없다 (바이트 그대로)
 *   못 보는 것: 진짜 마우스 드래그 (선택은 스크립트로 만든다) · 여러 기기 · 다른 브라우저 (애초에 나누지 않는다).
 */
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const JS = path.join(HERE, "static/js/docnote.js");
const CSS = path.join(HERE, "static/css/style.css");

let chromium;
try {
  ({ chromium } = createRequire(import.meta.url)("playwright"));
} catch {
  console.log("SKIP — playwright 가 없다");
  process.exit(0);
}
let browser;
try {
  browser = await chromium.launch();
} catch (e) {
  console.log("SKIP — chromium 을 못 띄웠다 (" + String(e.message || e).split("\n")[0] + ")");
  process.exit(0);
}

let ok = 0;
const bad = [];
const chk = (c, m) => { if (c) { ok++; console.log("  PASS  " + m); } else { bad.push(m); console.log("  FAIL  " + m); } };
const norm = (s) => String(s || "").replace(/\s+/g, " ").trim();
const KEYN = (rel) => "dem-dnote:v1:notes:" + rel;
const KEYP = (rel) => "dem-dnote:v1:pens:" + rel;

const DOC = `<!doctype html><meta charset="utf-8"><main class="content">
<div class="dn-host" id="host"><div id="col" style="min-width:0">
<span id="pnotebadge"></span> <button id="docpen" onclick="docnotePenToggle()">형광</button>
<div id="body">
  <p id="pa">여기 <em>기울임</em> 이 있고 <span>한 노드 안에 통째로</span> 들어 있는 문단이다. 첫 문단 끝</p>
  <p id="pb">두 번째 문단 시작 — <b>굵은 글자</b>를 지나 이어지는 문장 이 있다.</p>
  <ul><li id="pc">지금까지는 Li<sub>6</sub>PS<sub>5</sub>Cl 과 <b>LGPS</b> 에 <em>치환/도핑</em>만 해 왔다 → 끝</li></ul>
  <p id="pd">오른쪽 클릭으로 메모를 달 문단이다.</p>
  <p id="pe">형광펜으로 칠할 문단이다 — 앞 열 글자.</p>
</div></div></div></main>`;
const PENS = [
  { id: "h1", text: "한 노드 안에 통째로", color: "yellow", at: "2026-11-25" },
  { id: "h2", text: "굵은 글자를 지나 이어지는 문장", color: "green", at: "2026-11-25" },
  { id: "h3", text: "Li6PS5Cl 과 LGPS 에 치환/도핑만 해 왔다", color: "pink", at: "2026-11-25" },
  { id: "h4", text: "본문에 없는 문장이다", color: "blue", at: "2026-11-25" },
  { id: "h5", text: "첫 문단 끝 두 번째 문단 시작", color: "yellow", at: "2026-11-25" },
];
const NOTE = { id: "n1", at: "2026-11-25 09:00", anchor: "한 노드 안에 통째로", text: "첫 메모 — **굵게** 와 <img src=x onerror=window.__xss=1> 글자" };

const ctxA = await browser.newContext({ viewport: { width: 1600, height: 1000 } });   // A 의 페이지들은 같은 문맥 = 같은 localStorage
async function fixturePage(seed) {
  const pg = await ctxA.newPage();
  await pg.route("http://dn.test/**", (route) => route.fulfill({ contentType: "text/html; charset=utf-8", body: DOC }));
  await pg.goto("http://dn.test/report");
  await pg.addStyleTag({ path: CSS });
  await pg.addScriptTag({ path: JS });
  if (seed) await pg.evaluate(seed);
  return pg;
}
const mount = (pg, rel) => pg.evaluate((r) => window.mountDocNotes(document.getElementById("body"), r, document.getElementById("host")), rel);

/* ── A. 고정 문서 ─────────────────────────────────────────────────────── */
const REL = "webapp/static/explain/x.html";
let pg = await fixturePage(null);
await pg.evaluate(({ p, n, kp, kn }) => { localStorage.setItem(kp, JSON.stringify(p)); localStorage.setItem(kn, JSON.stringify([n])); },
                  { p: PENS, n: NOTE, kp: KEYP(REL), kn: KEYN(REL) });
await mount(pg, REL);
const a1 = await pg.evaluate(() => {
  const by = {};
  document.querySelectorAll("mark.dn-pen").forEach((m) => { const k = m.dataset.hid; (by[k] = by[k] || { t: "", n: 0, c: m.className }); by[k].t += m.textContent; by[k].n++; });
  const btn = document.getElementById("docpen");
  return { by, btn: btn.textContent, nested: document.querySelectorAll("mark.dn-pen mark.dn-pen").length,
           card: !!document.querySelector(".dnote-gut .dn-card"), on: document.getElementById("host").classList.contains("dnote-on"),
           cardText: (document.querySelector(".dnote-gut .dn-card .dn-text") || {}).innerHTML || "",
           imgInCard: !!document.querySelector(".dnote-gut .dn-card img"), xss: !!window.__xss,
           badge: document.getElementById("pnotebadge").textContent };
});
chk(a1.by.h1 && norm(a1.by.h1.t) === PENS[0].text, "[형광] 한 텍스트 노드 안 — 칠한다");
chk(a1.by.h2 && norm(a1.by.h2.t) === PENS[1].text && a1.by.h2.n >= 2, `[형광] <b> 경계를 가로질러도 칠한다 (조각 ${a1.by.h2 && a1.by.h2.n})`);
chk(a1.by.h3 && norm(a1.by.h3.t) === PENS[2].text, "[형광] 인라인 태그 여러 개 + 아래첨자");
chk(a1.by.h2 && /dn-pen-green/.test(a1.by.h2.c), "[형광] 색 클래스가 붙는다");
chk(!a1.by.h4 && !a1.by.h5, "[형광·음성] 본문에 없는 글 · 문단을 가로지른 글은 안 칠한다");
chk(/⚠2/.test(a1.btn), `[형광] 자리를 못 찾은 2 개를 버튼에 알린다 (${a1.btn})`);
chk(a1.nested === 0, "[형광] 형광펜 안에 형광펜이 겹치지 않는다");
chk(a1.card && a1.on, "[메모] 저장된 메모가 여백 카드로 · 여백이 열린다");
chk(/<b>굵게<\/b>/.test(a1.cardText), "[메모] **굵게** 는 굵게");
chk(!a1.imgInCard && !a1.xss && /&lt;img/.test(a1.cardText), "[메모·음성] 메모 글의 HTML 은 글자로 (img 원소 없음 · 스크립트 안 돎)");
chk(/메모 1/.test(a1.badge) && !/⚠/.test(a1.badge), `[머리줄] 메모 수 · 경고 없음 (${a1.badge})`);

// 오른쪽 클릭 → 초안 → 저장 → localStorage
const a2 = await pg.evaluate(async ({ kn }) => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const p = document.getElementById("pd");
  p.dispatchEvent(new MouseEvent("contextmenu", { bubbles: true, cancelable: true, clientX: 10, clientY: 10 }));
  await wait(50);
  const dr = document.querySelector(".dnote-gut .dn-draft");
  if (!dr) return { err: "초안 없음" };
  dr.querySelector(".dn-in").value = "둘째 메모";
  dr.querySelector(".dn-save").click();
  await wait(50);
  const saved = JSON.parse(localStorage.getItem(kn) || "[]");
  return { n: saved.length, last: saved[saved.length - 1], cards: document.querySelectorAll(".dnote-gut .dn-card").length };
}, { kn: KEYN(REL) });
chk(!a2.err && a2.n === 2 && a2.last.text === "둘째 메모" && a2.last.anchor.indexOf("오른쪽 클릭으로 메모를 달") === 0,
    `[메모·저장] 오른쪽 클릭 → 초안 → 저장 = localStorage 에 2 건 · 자리 = 그 문단 앞머리 ${a2.err || ""}`);
chk(a2.cards === 2, "[메모] 카드 2 장");
// 고치기 → history
const a3 = await pg.evaluate(async ({ kn }) => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const card = [...document.querySelectorAll(".dnote-gut .dn-card")].find((c) => c.dataset.nid === "n1");
  card.querySelector(".dn-edit").click();
  await wait(30);
  card.querySelector(".dn-in").value = "고친 첫 메모";
  card.querySelector(".dn-save").click();
  await wait(50);
  const n1 = JSON.parse(localStorage.getItem(kn)).find((x) => x.id === "n1");
  return n1;
}, { kn: KEYN(REL) });
chk(a3 && a3.text === "고친 첫 메모" && a3.history && a3.history.length === 1 && a3.history[0].text === NOTE.text && !!a3.edited_at,
    "[고치기] 새 글 저장 · 옛 글은 history 에 (지우지 않는다) · edited_at");
// 새로 열어도 남는다 (같은 출처 · 새 페이지)
const pg2 = await fixturePage(null);
await mount(pg2, REL);
const a4 = await pg2.evaluate(() => ({ cards: document.querySelectorAll(".dnote-gut .dn-card").length,
                                        pens: new Set([...document.querySelectorAll("mark.dn-pen")].map((m) => m.dataset.hid)).size }));
chk(a4.cards === 2 && a4.pens === 3, `[저장] 다른 페이지로 다시 열어도 메모 2 · 칠한 형광 3 이 남는다 (${a4.cards} · ${a4.pens})`);
await mount(pg2, "webapp/static/explain/other.html");
const a5 = await pg2.evaluate(() => document.querySelectorAll(".dnote-gut .dn-card").length + document.querySelectorAll("mark.dn-pen").length);
chk(a5 === 0, "[저장·음성] 다른 보고서 (rel) 에는 이 보고서의 메모 · 형광이 안 붙는다 (열쇠가 따로)");
await pg2.close();
// 지우기 (확인창 수락)
pg.on("dialog", (d) => d.accept());
const a6 = await pg.evaluate(async ({ kn }) => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const card = [...document.querySelectorAll(".dnote-gut .dn-card")].find((c) => c.dataset.nid !== "n1");
  card.querySelector(".dn-del").click();
  await wait(50);
  return JSON.parse(localStorage.getItem(kn)).map((x) => x.id);
}, { kn: KEYN(REL) });
chk(a6.length === 1 && a6[0] === "n1", "[지우기] 확인 뒤 그 메모만 지운다");
// 형광펜 켬 → 고른 글 → mouseup → 저장 · 칠한 곳 누름 = 지움
const a7 = await pg.evaluate(async ({ kp }) => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  window.docnotePenToggle();
  const t = document.getElementById("pe").firstChild;
  const r = document.createRange(); r.setStart(t, 0); r.setEnd(t, 10);
  const s = getSelection(); s.removeAllRanges(); s.addRange(r);
  document.getElementById("pe").dispatchEvent(new MouseEvent("mouseup", { bubbles: true }));
  await wait(50);
  const after = JSON.parse(localStorage.getItem(kp)).length;
  const m = document.querySelector("#pe mark.dn-pen");
  if (m) m.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
  await wait(50);
  const gone = JSON.parse(localStorage.getItem(kp)).length;
  return { after, gone, painted: !!m, on: document.body.classList.contains("dn-pen-on") };
}, { kp: KEYP(REL) });
chk(a7.on && a7.painted && a7.after === PENS.length + 1, `[형광·저장] 켜고 고르면 저장 · 바로 칠한다 (${a7.after})`);
chk(a7.gone === PENS.length, "[형광·지우기] 켠 채 칠한 곳을 누르면 지운다");
await pg.close();

// ⛔ 깨진 저장 값 — 지우지 않고 사본 열쇠로 옮긴 뒤 새로 쓴다
const REL2 = "webapp/static/explain/broken.html";
pg = await fixturePage(null);
await pg.evaluate(({ kn }) => localStorage.setItem(kn, "{not json"), { kn: KEYN(REL2) });
await mount(pg, REL2);
const b0 = await pg.evaluate(() => document.getElementById("pnotebadge").textContent);
const b1 = await pg.evaluate(async ({ kn }) => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  document.getElementById("pd").dispatchEvent(new MouseEvent("contextmenu", { bubbles: true, cancelable: true }));
  await wait(30);
  const dr = document.querySelector(".dnote-gut .dn-draft");
  dr.querySelector(".dn-in").value = "깨진 뒤 새 메모";
  dr.querySelector(".dn-save").click();
  await wait(50);
  const keys = Object.keys(localStorage).filter((k) => k.indexOf(kn + ":bak-") === 0);
  return { now: JSON.parse(localStorage.getItem(kn)).map((x) => x.text), bak: keys.map((k) => localStorage.getItem(k)) };
}, { kn: KEYN(REL2) });
chk(/못 읽었다/.test(b0), `[깨진 값] 머리줄에 '저장된 메모를 못 읽었다' (${b0})`);
chk(b1.bak.length === 1 && b1.bak[0] === "{not json" && b1.now.length === 1 && b1.now[0] === "깨진 뒤 새 메모",
    "[깨진 값·음성] 옛 값을 지우지 않고 사본 열쇠 (…:bak-<시각>) 로 옮긴 뒤 새로 쓴다");
await pg.close();

/* ── B. 저장이 막힌 문서 (about:blank — localStorage 가 막힌다) ──────────────── */
pg = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
await pg.setContent(DOC);
await pg.addStyleTag({ path: CSS });
await pg.addScriptTag({ path: JS });
const blocked = await pg.evaluate(() => { try { localStorage.getItem("x"); return false; } catch (e) { return true; } });
await mount(pg, REL);
const bb = await pg.evaluate(async () => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  document.getElementById("pd").dispatchEvent(new MouseEvent("contextmenu", { bubbles: true, cancelable: true }));
  await wait(30);
  const dr = document.querySelector(".dnote-gut .dn-draft");
  dr.querySelector(".dn-in").value = "막힌 브라우저 메모";
  dr.querySelector(".dn-save").click();
  await wait(50);
  return { cards: document.querySelectorAll(".dnote-gut .dn-card").length, badge: document.getElementById("pnotebadge").textContent,
           warn: document.getElementById("pnotebadge").classList.contains("dn-warn") };
});
chk(blocked, "[막힘] 이 문서에서는 localStorage 가 실제로 막혀 있다 (시험 전제)");
chk(bb.cards === 1 && /저장을 막았다/.test(bb.badge) && bb.warn, `[막힘] 메모는 이번 화면에서만 남고 머리줄에 경고 (${bb.badge})`);
await pg.close();

/* ── C. iframe — 본문은 같은 출처 iframe 안 · 카드는 바깥 ───────────────────── */
const FRAME = `<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;font:16px/1.7 sans-serif}main{padding:2rem}</style></head>
<body><main>${Array.from({ length: 6 }, (_, i) => `<p>채움 문단 ${i + 1} — 자리를 아래로 내린다.</p>`).join("")}
<p id="ta">요약 — <b>LPSCl 은 Li 금속과</b> 닿으면 분해된다 는 문장이 여기 있다.</p>
<p id="tb">iframe 안 오른쪽 클릭으로 메모를 달 문단이다.</p></main></body></html>`;
const OUTER = `<!doctype html><meta charset="utf-8"><main class="content"><div style="height:200px">머리</div>
<span id="pnotebadge"></span><button id="docpen">형광</button>
<div class="dn-host" id="fhost"><div style="min-width:0"><iframe id="fr" src="/report" style="width:100%;height:1200px;border:0;display:block"></iframe></div></div></main>`;
const FREL = "docs/x.html";
pg = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
await pg.route("http://frame.test/**", (route) => route.fulfill({ contentType: "text/html; charset=utf-8",
  body: route.request().url().endsWith("/report") ? FRAME : OUTER }));
await pg.goto("http://frame.test/");
await pg.addStyleTag({ path: CSS });
await pg.addScriptTag({ path: JS });
await pg.waitForFunction(() => { const d = document.getElementById("fr").contentDocument; return !!(d && d.readyState === "complete" && d.getElementById("tb")); });
await pg.evaluate(({ kp, kn }) => {
  localStorage.setItem(kp, JSON.stringify([{ id: "fh1", text: "LPSCl 은 Li 금속과 닿으면 분해된다", color: "yellow", at: "2026-11-25" }]));
  localStorage.setItem(kn, JSON.stringify([{ id: "fn1", at: "2026-11-25 10:00", anchor: "iframe 안 오른쪽 클릭으로 메모를 달 문단이다.", text: "iframe 안 문장 메모" }]));
}, { kp: KEYP(FREL), kn: KEYN(FREL) });
const fr = await pg.evaluate(async (rel) => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const fd = document.getElementById("fr").contentDocument;
  window.mountDocNotes(fd.querySelector("main"), rel, document.getElementById("fhost"));
  await wait(200);
  const pens = [...fd.querySelectorAll("mark.dn-pen")];
  const st = fd.getElementById("dn-body-css");
  fd.getElementById("ta").dispatchEvent(new fd.defaultView.MouseEvent("contextmenu", { bubbles: true, cancelable: true }));
  await wait(50);
  return { penN: pens.length, penText: pens.map((m) => m.textContent).join(""),
           penBg: pens.length ? fd.defaultView.getComputedStyle(pens[0]).backgroundColor : "",
           cssIn: !!st, cssOut: !!document.getElementById("dn-body-css"),
           hl: !!fd.querySelector("mark.dn-hl"), card: !!document.querySelector("#fhost .dn-card"), cardInFrame: !!fd.querySelector(".dn-card"),
           draftOut: !!document.querySelector("#fhost .dn-draft"), draftIn: !!fd.querySelector(".dn-draft") };
}, FREL);
chk(fr.penN >= 2 && norm(fr.penText) === "LPSCl 은 Li 금속과 닿으면 분해된다", `[iframe·형광] iframe 문서 안에 칠한다 — <b> 를 가로질러도 (조각 ${fr.penN})`);
chk(fr.cssIn && !fr.cssOut && /^rgb/.test(fr.penBg) && fr.penBg !== "rgba(0, 0, 0, 0)", `[iframe·CSS] 칠한 곳에 색 (${fr.penBg}) · 옮긴 규칙은 iframe 에만`);
chk(fr.hl && fr.card && !fr.cardInFrame, "[iframe·메모] 메모 자리 표시는 iframe 안 · 카드는 바깥 여백");
chk(fr.draftOut && !fr.draftIn, "[iframe·오른쪽 클릭] iframe 안 문단 오른쪽 클릭 → 바깥 여백에 초안");
await pg.close();

/* ── D. 실제 앱 — /reports/<slug> 보기 ─────────────────────────────────────── */
const PY = `import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'webapp'))
import app as A
import track_pages as T
from werkzeug.serving import make_server
srv = make_server('127.0.0.1', 0, A.app, threaded=True)
print('PORT %d %s %s' % (srv.server_port, T.REPORTS[0]['slug'], T.REPORTS[0]['rel']), flush=True)
srv.serve_forever()`;
const child = spawn("python3", ["-c", PY], { cwd: ROOT, stdio: ["ignore", "pipe", "pipe"] });
//  이 시험이 띄운 자식 프로세스만 멈춘다 — 중간에 검사가 던져도 (아래 try · finally) 또는 node 가 그냥 끝나도 (exit) 남기지 않는다.
const stopChild = () => { try { if (child.exitCode === null && child.signalCode === null) child.kill("SIGTERM"); } catch { /* 이미 끝남 */ } };
process.on("exit", stopChild);
let port = null, slug = null, rrel = null;
await new Promise((res) => {
  const t = setTimeout(res, 60000);
  let buf = "";
  child.stdout.on("data", (b) => { buf += String(b); const m = /PORT (\d+) (\S+) (\S+)\n/.exec(buf); if (m) { [, port, slug, rrel] = m; clearTimeout(t); res(); } });
  child.on("exit", () => { clearTimeout(t); res(); });
});
chk(!!port, `[앱] 웹앱을 빈 포트로 띄웠다 (${port})`);
if (port) try {
  const base = `http://127.0.0.1:${port}`;
  pg = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await pg.goto(`${base}/reports/${slug}`);
  await pg.waitForFunction(() => { const f = document.getElementById("rp-frame"); const d = f && f.contentDocument;
    return !!(d && d.readyState === "complete" && d.querySelector("main")); }, null, { timeout: 15000 });
  await pg.waitForTimeout(500);
  const d1 = await pg.evaluate(async () => {
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    const fd = document.getElementById("rp-frame").contentDocument;
    const p = fd.querySelector("main p");
    if (!p) return { err: "문단 없음" };
    p.dispatchEvent(new fd.defaultView.MouseEvent("contextmenu", { bubbles: true, cancelable: true }));
    await wait(80);
    const dr = document.querySelector("#rp-host .dn-draft");
    if (!dr) return { err: "초안 없음" };
    dr.querySelector(".dn-in").value = "실제 앱 메모";
    dr.querySelector(".dn-save").click();
    await wait(80);
    return { cards: document.querySelectorAll("#rp-host .dn-card").length, badge: document.getElementById("pnotebadge").textContent,
             frameH: document.getElementById("rp-frame").getBoundingClientRect().height };
  });
  chk(!d1.err && d1.cards === 1 && /메모 1/.test(d1.badge), `[앱] 보기 화면 iframe 본문에 메모 → 카드 1 ${d1.err || ""} (${d1.badge})`);
  chk(d1.frameH > 900, `[앱] iframe 높이를 보고서 길이에 맞췄다 (${Math.round(d1.frameH || 0)}px)`);
  await pg.reload();
  await pg.waitForFunction(() => document.querySelectorAll("#rp-host .dn-card").length > 0, null, { timeout: 15000 }).catch(() => {});
  const d2 = await pg.evaluate((rel) => ({ cards: document.querySelectorAll("#rp-host .dn-card").length,
    stored: JSON.parse(localStorage.getItem("dem-dnote:v1:notes:" + rel) || "[]").length }), rrel);
  chk(d2.cards === 1 && d2.stored === 1, "[앱] 새로 고쳐도 메모가 남는다 (이 브라우저 localStorage · 열쇠 = 보고서 파일 경로)");
  const raw = await (await pg.request.get(`${base}/reports/${slug}/raw`)).text();
  chk(raw.indexOf("dn-card") < 0 && raw.indexOf("dn-body-css") < 0 && raw.indexOf("실제 앱 메모") < 0,
      "[앱·음성] 원본 /raw 에는 메모 · 칠하기 표시가 없다 (바이트 그대로)");
  await pg.close();
} catch (e) {
  chk(false, "[앱] 실제 앱 검사 중 예외 — " + String(e.message || e).split("\n")[0]);
} finally {
  stopChild();
}
stopChild();

await ctxA.close();
await browser.close();
console.log(`\n== test_docnote_local: ${ok}/${ok + bad.length} PASS`);
if (bad.length) console.log("   실패: " + bad.join(" · "));
process.exit(bad.length ? 1 : 0);

/* 표 칸이 **한 글자 폭으로 쪼그라들지 않는가** — 진짜 브라우저 배치로만 잴 수 있는 것.
 *
 * 왜 있나 (2026-11-11 · 사용자 스크린샷 *'요렇게 길게 나오는 파일을 수정좀 해봐'*):
 *   /governance 인용 위험 표의 '파일' 칸이 `d / b / / / p / r …` 처럼 한 글자씩 세로로 찍혔다 (46 행 전부).
 *   원인은 `.card .mono{overflow-wrap:anywhere}` (10-28) — 표 칸의 최소 폭 (min-content) 이 글자 하나가 돼서,
 *   옆 칸 글이 길면 자동 배치가 그 칸을 끝까지 줄인다. 서버 시험 (pytest) 은 HTML 만 봐서 이걸 못 잡는다.
 *
 * 무엇을 보나 (페이지마다):
 *   ① 쪼그라든 칸 — 안쪽 폭 (padding 뺀 것) 이 글자 4 개 폭 (4 em) 보다 좁은데 글이 12 자 이상인 td/th
 *   ② (--no-overflow 페이지만) 표가 자기 스크롤 상자보다 넓은가 — 넘치면 오른쪽 글이 잘린다
 *   ⓪ 자체 대조: 옛 꼴 (카드 안 표 · td.mono 긴 경로 · 옆 칸 긴 글) 을 **실제 style.css** 로 그려서
 *      ⓪a anywhere 를 직접 걸면 ①이 잡는지 (못 잡으면 헛것을 잰다) · ⓪b 지금 CSS 그대로면 안 쪼그라드는지 본다.
 *
 * 이 파일이 못 하는 것: 글이 읽기 좋은지는 못 본다 · 접힌 (<details>) 안은 다 펴서 잰다 ·
 *   창 폭 1400 px 하나에서만 잰다 (좁은 화면은 안 본다) · 외부 스크립트 (CDN) 는 막고 잰다.
 *
 * 실행: node webapp/tests/table_layout.test.mjs <이름>=<렌더된 html 경로>[:no-overflow] …
 *       (pytest 의 test_tables_have_no_squeezed_cells 가 렌더해서 넘긴다. 도구가 없으면 SKIP.)
 */
import { readFileSync, existsSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "../..");
const STATIC = path.join(ROOT, "webapp/static");

let chromium;
try {
  const req = createRequire(process.env.PW_CORE_FROM || `${ROOT}/package.json`);
  ({ chromium } = req("playwright-core"));
} catch {
  console.log("SKIP — playwright-core 가 없다 (npm i playwright-core)");
  process.exit(0);
}
const isFile = (p) => { try { return existsSync(p) && statSync(p).isFile(); } catch { return false; } };
const EXE = ["/opt/pw-browsers/chromium/chrome-linux/chrome",
             "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
             "/opt/pw-browsers/chromium"].find(isFile);
if (!EXE) { console.log("SKIP — chromium 실행파일을 못 찾았다"); process.exit(0); }

const pages = process.argv.slice(2).map((a) => {
  const [name, rest] = [a.slice(0, a.indexOf("=")), a.slice(a.indexOf("=") + 1)];
  const noOverflow = rest.endsWith(":no-overflow");
  return { name, file: noOverflow ? rest.slice(0, -":no-overflow".length) : rest, noOverflow };
});
if (!pages.length) { console.log("FAIL — 잴 페이지가 없다"); process.exit(1); }

const MIME = { ".css": "text/css", ".js": "application/javascript", ".svg": "image/svg+xml",
               ".png": "image/png", ".woff2": "font/woff2", ".json": "application/json" };

async function measure(page, html) {
  await page.route("**/*", async (route) => {
    const u = new URL(route.request().url());
    if (u.hostname !== "local.test") return route.abort();          // CDN · 외부는 막는다
    if (u.pathname === "/page") return route.fulfill({ body: html, contentType: "text/html; charset=utf-8" });
    if (u.pathname.startsWith("/static/")) {
      const f = path.join(STATIC, decodeURIComponent(u.pathname.slice("/static/".length)));
      if (f.startsWith(STATIC) && isFile(f))
        return route.fulfill({ body: readFileSync(f), contentType: MIME[path.extname(f)] || "application/octet-stream" });
    }
    return route.fulfill({ status: 404, body: "" });
  });
  await page.goto("http://local.test/page", { waitUntil: "load" });
  await page.unroute("**/*");
  return page.evaluate(() => {
    document.querySelectorAll("details").forEach((d) => { d.open = true; });
    const squeezed = [];
    document.querySelectorAll("td, th").forEach((c) => {
      const t = (c.innerText || "").replace(/\s/g, "");
      const cs = getComputedStyle(c);
      // 안쪽 폭 (padding 뺀 것) 을 글자 크기로 나눈다 — 칸 폭만 보면 padding 24 px 에 가려 놓친다 (자체 음성이 잡았다)
      const inner = c.getBoundingClientRect().width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      const em = inner / parseFloat(cs.fontSize);
      if (c.getBoundingClientRect().width > 0 && em < 4 && t.length >= 12)
        squeezed.push(`${em.toFixed(1)}em "${t.slice(0, 40)}"`);
    });
    const over = [];
    document.querySelectorAll(".card table").forEach((tb) => {
      const par = tb.parentElement;
      if (tb.getBoundingClientRect().width > 0 && tb.scrollWidth > par.clientWidth + 4)
        over.push(`${tb.className || "(no class)"} ${tb.scrollWidth} > ${par.clientWidth}`);
    });
    return { squeezed, over, css: !!getComputedStyle(document.body).getPropertyValue("--border") };
  });
}

const browser = await chromium.launch({ executablePath: EXE });
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
let fail = 0;

// ⓪ 자체 대조 둘 — 옛 꼴 (카드 안 표 · td.mono 긴 경로 · 옆 칸 긴 글) 을 실제 style.css 로 그린다.
//   ⓪a 옛 규칙 (overflow-wrap:anywhere) 을 칸에 직접 걸면 **잡혀야** 한다 — 못 잡으면 검출기가 헛것을 잰다.
//   ⓪b 같은 꼴을 지금 style.css 그대로 그리면 **안 잡혀야** 한다 — `.card td .mono{overflow-wrap:break-word}` 가 하는 일.
//       (그 규칙을 지우면 ⓪b 가 빨갛다 — 2026-11-11 원인 규칙의 되돌림을 직접 막는다.)
const negRow = (style) => `<!doctype html><html><head><meta charset="utf-8">
  <link rel="stylesheet" href="/static/css/style.css"></head><body><main class="content"><div class="card">
  <table class="data-table" style="font-size:.78rem"><tbody><tr>
  <td class="mono" style="font-size:.7rem${style}">db/properties/b2o3_md_arrhenius.json</td>
  <td>${"긴 본문 글 ".repeat(60)}</td><td>${"또 긴 글 ".repeat(60)}</td><td>${"셋째 긴 글 ".repeat(60)}</td>
  </tr></tbody></table></div></main></body></html>`;
const na = await measure(page, negRow(";overflow-wrap:anywhere"));
const nb = await measure(page, negRow(""));
if (!na.css || !nb.css) { console.log("FAIL ⓪ — style.css 가 안 실렸다 (배치를 안 잰다)"); fail++; }
else {
  if (!na.squeezed.length) { console.log("FAIL ⓪a — anywhere 를 건 옛 꼴을 못 잡았다: 이 시험은 헛것을 잰다"); fail++; }
  else console.log(`ok ⓪a 검출기 — 옛 꼴을 잡았다 (${na.squeezed[0]})`);
  if (nb.squeezed.length) { console.log(`FAIL ⓪b — 지금 style.css 에서도 표 칸 mono 가 쪼그라든다: ${nb.squeezed[0]}`); fail++; }
  else console.log("ok ⓪b style.css — 표 칸 mono 가 안 쪼그라든다");
}

for (const p of pages) {
  const r = await measure(page, readFileSync(p.file, "utf-8"));
  if (!r.css) { console.log(`FAIL ${p.name} — style.css 가 안 실렸다`); fail++; continue; }
  if (r.squeezed.length) {
    console.log(`FAIL ${p.name} — 쪼그라든 칸 ${r.squeezed.length}: ${r.squeezed.slice(0, 3).join(" | ")}`); fail++;
  } else console.log(`ok ${p.name} — 쪼그라든 칸 0`);
  if (p.noOverflow) {
    if (r.over.length) { console.log(`FAIL ${p.name} — 카드 밖으로 넘친 표: ${r.over.join(" | ")}`); fail++; }
    else console.log(`ok ${p.name} — 넘친 표 0`);
  }
}
await browser.close();
if (fail) { console.log(`table layout FAIL (${fail})`); process.exit(1); }
console.log("table layout PASS");

// 발표 때 한 장씩 넘기며 읽는 대본 PDF: 슬라이드 1장 = 1페이지 (A4 가로, 장표 그림 + 읽을 문장).
// 사용: NODE_PATH=$(npm root -g) node make_reading_pdf.js <script.json> <장표 PNG 폴더(s-01.png…)> <출력.pdf>
// 장표 PNG는 미리보기 PDF에서 만든다: pdftoppm -r 110 -png 02_발표자료_나물로_미리보기.pdf <폴더>/s
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const [SCRIPT, SLIDES, OUT] = process.argv.slice(2);
if (!SCRIPT || !SLIDES || !OUT) { console.error("사용: node make_reading_pdf.js <script.json> <장표 PNG 폴더> <출력.pdf>"); process.exit(1); }
const FONT = path.join(__dirname, "..", "prototype", "pretendard-subset.woff2");
const LABEL = { 1: "표지", 2: "Problem | 고객의 문제와 필요", 3: "Problem | 판매자의 문제와 필요", 4: "Solution | 서비스", 5: "Solution | AI 기능", 6: "Solution | 시연",
  7: "Business | 시장성", 8: "Business | 차별성", 9: "Business | 수익모델", 10: "Vision | 사업화 계획", 11: "Vision | 성장 가능성", 12: "마무리" };
const CUE = { 6: "▶ 장표의 시연 영상을 클릭해 재생 (약 26초). 영상이 끝나도 마지막 화면을 띄운 채 이어서 읽는다.",
  12: "부록 13·14는 읽지 않는다. 질문이 나오면 근거로 보여 준다." };

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const mmss = (x) => `${Math.floor(x / 60)}:${String(Math.floor(x % 60)).padStart(2, "0")}`;
const data = JSON.parse(fs.readFileSync(SCRIPT, "utf8")).filter((o) => o.sentences.length);
const png = (n) => { const f = fs.readdirSync(SLIDES).filter((x) => /\.png$/.test(x)).sort()[n - 1]; return "file://" + path.resolve(SLIDES, f); };

const pages = data.map((o, i) => {
  const next = data[i + 1];
  return `<section class="page">
  <header><div class="num">${o.n}<small>/${data.length}</small></div>
    <div class="meta"><div class="label">${esc(LABEL[o.n] || o.sec)}</div><div class="title">${esc(o.title)}</div></div>
    <div class="time">${mmss(o.start)} – ${mmss(o.start + o.dur)}<small>약 ${Math.round(o.dur)}초</small></div></header>
  <main><div class="script">${o.sentences.map((s) => `<p>${esc(s)}</p>`).join("")}</div>
    <aside><img src="${png(o.n)}" alt="">${CUE[o.n] ? `<div class="cue">${esc(CUE[o.n])}</div>` : ""}
      <div class="next">${next ? `다음 장 → ${next.n}. ${esc(next.title)}` : "끝"}</div></aside></main>
</section>`;
}).join("\n");

const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
@font-face { font-family: "Pretendard"; src: url("file://${FONT}") format("woff2"); font-weight: 100 900; }
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Pretendard", "WenQuanYi Zen Hei", sans-serif; color: #19221E; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 297mm; height: 210mm; padding: 12mm 14mm 11mm; display: grid; grid-template-rows: auto 1fr; gap: 7mm; page-break-after: always; break-after: page; }
.page:last-child { page-break-after: auto; break-after: auto; }
header { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 6mm; border-bottom: 1.2mm solid #1E4D3A; padding-bottom: 4mm; }
.num { font-size: 30pt; font-weight: 800; color: #1E4D3A; line-height: 1; }
.num small { font-size: 13pt; font-weight: 600; color: #8E9993; margin-left: 1mm; }
.label { font-size: 11pt; font-weight: 700; color: #3F7F5F; }
.title { font-size: 19pt; font-weight: 800; margin-top: 1mm; }
.time { text-align: right; font-size: 13pt; font-weight: 700; color: #1E4D3A; }
.time small { display: block; font-size: 10.5pt; font-weight: 500; color: #5D6963; }
main { display: grid; grid-template-columns: 1fr 98mm; gap: 9mm; min-height: 0; }
.script p { font-size: 17pt; line-height: 1.62; margin: 0 0 3.2mm; word-break: keep-all; }
aside { display: flex; flex-direction: column; gap: 4mm; }
aside img { width: 100%; border: 0.3mm solid #E2E7E3; border-radius: 2mm; }
.cue { font-size: 11.5pt; line-height: 1.5; font-weight: 700; color: #B4622A; background: #FBEFE3; border-radius: 2mm; padding: 3mm 3.5mm; }
.next { margin-top: auto; font-size: 11pt; color: #5D6963; text-align: right; }
</style></head><body>
${pages}
</body></html>`;

(async () => {
  const tmp = path.join(path.dirname(path.resolve(OUT)), ".reading.html");
  fs.writeFileSync(tmp, html);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + tmp, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  // 한 페이지에 들어가지 않는 장표가 있으면 알린다
  const over = await page.$$eval(".page", (els) => els.map((e, i) => [i + 1, e.scrollHeight - e.clientHeight]).filter(([, d]) => d > 1));
  if (over.length) console.warn("페이지 넘침:", JSON.stringify(over));
  await page.pdf({ path: OUT, width: "297mm", height: "210mm", printBackground: true, preferCSSPageSize: true });
  await browser.close();
  fs.unlinkSync(tmp);
  console.log("wrote", OUT, `(${data.length}쪽)`);
})();

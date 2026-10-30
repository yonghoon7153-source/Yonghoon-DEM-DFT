// Codex 리뷰 재현 시나리오 점검: 파서 · 확인 후 반영 · 이스케이프 · 품목별 데침 · 한 품목 안내 · 뒤로 가기
const { chromium } = require("playwright");
const path = require("path"), os = require("os");
const ROOT = path.resolve(__dirname, ".."), PAGE = "file://" + path.join(ROOT, "prototype/nm_prototype.html");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 960 } });
  const errs = []; const R = {};
  page.on("pageerror", e => errs.push("pageerror: " + e.message));
  page.on("console", m => { if (m.type() === "error") errs.push("console: " + m.text()); });
  page.on("dialog", d => { errs.push("dialog fired: " + d.message()); d.dismiss(); });
  await page.goto(PAGE + "#home"); await page.waitForTimeout(1200);
  const ev = (f, a) => page.evaluate(f, a);
  // 1) parser: commas + negation, draft state
  await ev(() => demo.go("merchant")); await page.waitForTimeout(200);
  await page.fill("#chatInput", "참나물 10단 3,500원 손질 불가"); await page.click("#chatSend"); await page.waitForTimeout(1000);
  R.draftCard = await page.$$eval(".mcard", els => els.at(-1).innerText.replace(/\n+/g, " | "));
  // 2) confirm -> applied to store s1
  await page.click(".mcard:last-of-type [data-act=ok]", { strict: false }).catch(async () => { const b = await page.$$("[data-act=ok]"); await b.at(-1).click(); });
  await page.waitForTimeout(300);
  R.afterOk = await page.$$eval(".mcard", els => els.at(-1).innerText.replace(/\n+/g, " | "));
  R.s1Stock = await ev(() => ({ cham: STORES[0].stock.chamnamul, trimOk: STORES[0].trimOk, today: STORES[0].today }));
  await ev(() => { demo.set({ cart: ["chamnamul"], namul: "chamnamul" }); demo.go("stores"); }); await page.waitForTimeout(300);
  R.s1Card = await page.$eval('[data-store="s1"]', el => el.innerText.replace(/\n+/g, " | "));
  await page.click('[data-store="s1"]'); await page.waitForTimeout(300);
  R.checkoutOpts = await page.$$eval("#optSeg button", els => els.map(b => b.innerText.replace(/\n/g, " ") + (b.disabled ? " [off]" : "")));
  // 3) escaping of AI fields
  await ev(() => { demo.go("merchant"); st.chat.push({ who: "bot", t: "00:00", card: "stock", data: stockData({ items: [{ name: "참나물<b>x</b>", qty: "<img src=x onerror=alert(1)>", unit: "<i>단</i>", price: "3500<script>" }] }) }); rMerchant(); });
  await page.waitForTimeout(300);
  R.injectedImgs = await ev(() => document.querySelectorAll("#chatBody img:not(.avatar img)").length);
  R.injectedCard = await page.$$eval(".mcard", els => els.at(-1).innerText.replace(/\n+/g, " | "));
  // 4) item-specific blanch note
  const note = async (k) => { await ev(k => { STORES.splice(0, STORES.length, ...JSON.parse(STORES0)); demo.set({ cart: [k], namul: k, store: "s1", opt: "blanch" }); demo.go("checkout"); }, k); await page.waitForTimeout(250);
    return { opts: await page.$$eval("#optSeg button", els => els.map(b => b.innerText.replace(/\n/g, " ") + (b.disabled ? " [off]" : ""))), note: await page.$eval("#optNote", e => e.textContent) }; };
  R.blanch = { sigeumchi: await note("sigeumchi"), kongnamul: await note("kongnamul"), pyogo: await note("pyogo"), gosari: await note("gosari") };
  // 5) multi-item cart note
  await ev(() => { demo.set({ cart: ["sigeumchi", "chamnamul"], namul: "chamnamul" }); demo.go("stores"); }); await page.waitForTimeout(250);
  R.multiNote = await page.$eval("#sNote", e => (e.hidden ? "[hidden] " : "") + e.textContent);
  // 6) back navigation uses one history
  await ev(() => demo.go("home")); await page.waitForTimeout(150);
  await ev(() => demo.go("dogam")); await page.waitForTimeout(150);
  await ev(() => { st.namul = "sigeumchi"; demo.go("guide"); }); await page.waitForTimeout(150);
  await page.click('[data-view=guide] [data-back]'); await page.waitForTimeout(300);
  const afterBack1 = await ev(() => current);
  await page.click('[data-view=dogam] .icon-btn[data-go=aichef]'); await page.waitForTimeout(200);
  await page.click('[data-view=aichef] [data-back]'); await page.waitForTimeout(300);
  R.back = { afterBack1, afterBack2: await ev(() => current), histLen: await ev(() => history.length) };
  // 7) phone width
  const phone = await browser.newPage({ viewport: { width: 390, height: 844 } });
  phone.on("pageerror", e => errs.push("phone pageerror: " + e.message));
  await phone.goto(PAGE + "#home"); await phone.waitForTimeout(800);
  R.phoneOverflowPx = await phone.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  R.viewportMeta = await phone.evaluate(() => !!document.querySelector('meta[name=viewport]'));
  await phone.screenshot({ path: path.join(os.tmpdir(), "namul_review_phone.png") });
  console.log(JSON.stringify({ errs, ...R }, null, 1));
  await browser.close();
})();

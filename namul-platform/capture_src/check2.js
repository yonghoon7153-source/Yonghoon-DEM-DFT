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
  // 8) 2차 리뷰 반례: 금액 표기 · 음수 · 긴 숫자 · '안 됩니다' · g 단위 · 느슨한 타입
  const parse = async (msg) => ev(m => { const d = localParse(m); return d.items.map(it => `${it.name} ${it.qty}${it.unit || ""} ${it.price === null ? "?" : it.price} trim=${it.trim} issues=${it.issues.join("/") || "-"}`).join(" ; "); }, msg);
  R.round2 = {};
  for (const m of ["참나물 10단 3만5천원", "참나물 10단 -6000원", "참나물 10단 1000000원", "참나물 10단 3500원 손질 안 됩니다", "참나물 200g 3500원", "참나물 10단 3,500원 손질 불가", "참나물 10단 3천5백 손질 안돼요"]) R.round2[m] = await parse(m);
  R.round2.looseTypes = await ev(() => stockData({ items: [{ name: "참나물", qty: true, unit: "단", price: [3500] }, { name: "시금치", qty: "15", unit: "단", price: "3,000" }] }).items.map(it => it.issues.join("/")));
  // g 단위 등록안은 확인해도 재고에 반영되지 않는다
  await ev(() => { STORES.splice(0, STORES.length, ...JSON.parse(STORES0)); st.chat = defaultChat().slice(0, 2); demo.go("merchant"); rMerchant(); });
  await page.fill("#chatInput", "참나물 200g 3500원"); await page.click("#chatSend"); await page.waitForTimeout(1000);
  { const b = await page.$$("[data-act=ok]"); await b.at(-1).click(); } await page.waitForTimeout(300);
  R.round2.gramApplied = await ev(() => STORES[0].stock.chamnamul);
  // 이미 담은 품목을 다시 고르면 그 품목 매장을 보여 준다
  await ev(() => { st = Object.assign(st, { cart: [] }); st.namul = "sigeumchi"; demo.go("guide"); }); await page.waitForTimeout(200);
  await page.click("#gBuy"); await page.waitForTimeout(250);
  await ev(() => { st.namul = "chamnamul"; demo.go("guide"); }); await page.waitForTimeout(200);
  await page.click("#gBuy"); await page.waitForTimeout(250);
  await ev(() => { st.namul = "sigeumchi"; demo.go("guide"); }); await page.waitForTimeout(200);
  await page.click("#gBuy"); await page.waitForTimeout(300);
  R.round2.reselect = await page.$eval("#sListTitle", e => e.textContent) + " | cart=" + (await ev(() => st.cart.join(",")));
  // 9) 받는 방법: 저녁 배달 선택 시 배달비·시간·완료·판매자 카드 반영, 예약 탭
  await ev(() => { STORES.splice(0, STORES.length, ...JSON.parse(STORES0)); st = Object.assign(st, { cart: ["chamnamul"], namul: "chamnamul", store: "s1", opt: "trim", qty: 1, recv: "pickup", orderAccepted: false }); demo.go("checkout"); }); await page.waitForTimeout(250);
  R.delivery = { pickupBtn: await page.$eval("#payBtn", e => e.textContent) };
  await page.click('#recvSeg [data-recv="deliver"]'); await page.waitForTimeout(200);
  R.delivery.deliverBtn = await page.$eval("#payBtn", e => e.textContent);
  R.delivery.timeTitle = await page.$eval("#timeTitle", e => e.textContent);
  R.delivery.sum = await page.$eval("#sumBox", e => e.innerText.replace(/\n+/g, " | "));
  await page.click("#payBtn"); await page.waitForTimeout(300);
  R.delivery.done = await page.$eval("#dTitle", e => e.textContent) + " / " + await page.$eval("#dSub", e => e.textContent);
  await ev(() => { st.chat = null; demo.go("merchant"); }); await page.waitForTimeout(300);
  R.delivery.merchantOrder = await page.$$eval(".mcard", els => els.find(e => e.innerText.includes("새 주문")).innerText.replace(/\n+/g, " | "));
  await ev(() => demo.go("box")); await page.waitForTimeout(250);
  R.preorder = { sets: await page.$$eval("#plans .plan", els => els.length), cta: await page.$eval("#subBtn", e => e.textContent), tab: await page.$eval('[data-tab="box"]', e => e.textContent.trim()) };
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

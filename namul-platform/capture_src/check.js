// 기본 점검: 화면 전환 · AI 셰프 예시 응답 · 판매자 메시지 정리 · 390px 가로 넘침 · 콘솔 오류
const { chromium } = require("playwright");
const path = require("path"), os = require("os");
const ROOT = path.resolve(__dirname, ".."), PAGE = "file://" + path.join(ROOT, "prototype/nm_prototype.html");
(async () => {
  const SHOT = os.tmpdir();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 960 } });
  const errs = [];
  page.on("pageerror", e => errs.push("pageerror: " + e.message));
  page.on("console", m => { if (m.type() === "error") errs.push("console: " + m.text()); });
  await page.goto(PAGE);
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(SHOT, "namul_review_desktop.png") });
  // exercise flows quickly
  for (const v of ["dogam", "aichef", "recipe", "stores", "checkout", "done", "box", "merchant", "home"]) {
    await page.evaluate(v => window.demo.go(v), v); await page.waitForTimeout(150);
  }
  await page.evaluate(() => window.demo.go("aichef")); await page.waitForTimeout(200);
  await page.click("#chefChips button"); await page.waitForTimeout(1300);
  const recs = await page.$$eval(".rec", els => els.length);
  await page.evaluate(() => window.demo.go("merchant")); await page.waitForTimeout(200);
  await page.fill("#chatInput", "취나물 10단 4000 손질 가능, 고사리 5봉 6000"); await page.click("#chatSend"); await page.waitForTimeout(1000);
  const lastCard = await page.$$eval(".mcard", els => els.at(-1).innerText);
  // phone-width layout
  const phone = await browser.newPage({ viewport: { width: 390, height: 844 } });
  phone.on("pageerror", e => errs.push("phone pageerror: " + e.message));
  await phone.goto(PAGE + "#home"); await phone.waitForTimeout(800);
  const overflow = await phone.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  await phone.screenshot({ path: path.join(SHOT, "namul_review_phone.png") });
  console.log(JSON.stringify({ errs, recs, lastCard, phoneOverflowPx: overflow }, null, 1));
  await browser.close();
})();

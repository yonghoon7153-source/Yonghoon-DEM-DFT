const { chromium } = require("playwright");
(async () => {
  const S = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 960 } });
  const errs = [];
  page.on("pageerror", e => errs.push("pageerror: " + e.message));
  page.on("console", m => { if (m.type() === "error") errs.push("console: " + m.text()); });
  await page.goto("file://" + S + "/proto/nm_prototype.html");
  await page.waitForTimeout(1500);
  await page.screenshot({ path: S + "/proto/shots/review_desktop.png" });
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
  await phone.goto("file://" + S + "/proto/nm_prototype.html#home"); await phone.waitForTimeout(800);
  const overflow = await phone.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  await phone.screenshot({ path: S + "/proto/shots/review_phone.png" });
  console.log(JSON.stringify({ errs, recs, lastCard, phoneOverflowPx: overflow }, null, 1));
  await browser.close();
})();

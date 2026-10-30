// 발표용 앱 화면 캡처 (표시 링 없이 깨끗한 화면) → assets/screens/*.png
// 사용: node stills.js   (먼저 prototype/build.py 로 nm_prototype.html 을 만든다)
const { chromium } = require("playwright");
const path = require("path"), os = require("os");
const ROOT = path.resolve(__dirname, ".."), PAGE = "file://" + path.join(ROOT, "prototype/nm_prototype.html");
const URL = PAGE, OUT = path.join(ROOT, "assets/screens") + "/";
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1280, height: 960 }, deviceScaleFactor: 2 });
  await page.goto(URL + "#home"); await sleep(1200);
  await page.addStyleTag({ content: "body,.stage{background:transparent!important} .toast{display:none!important}" });
  const dev = await page.$(".device"); const ev = (f, a) => page.evaluate(f, a);
  const snap = async n => { await sleep(300); await dev.screenshot({ path: OUT + n + ".png", omitBackground: true }); };
  const clock = t => ev(t => { document.getElementById("clock").textContent = t; }, t);
  await ev(() => document.getElementById("resetBtn").click()); await sleep(300);
  await ev(() => demo.go("home")); await snap("home");
  await ev(() => demo.go("aichef")); await sleep(200); await ev(() => demo.askChef("다섯 살 아이랑 먹을 순한 반찬 추천해 줘")); await sleep(1400);
  await ev(() => { document.getElementById("chefBody").scrollTop = 150; }); await snap("aichef");
  await ev(() => { demo.set({ namul: "chamnamul", step: 1 }); demo.go("recipe"); }); await sleep(300);
  await ev(() => { document.querySelector("[data-view=recipe] .v-body").scrollTop = 120; }); await snap("recipe");
  await ev(() => { demo.set({ cart: ["chamnamul"], namul: "chamnamul", store: "s1" }); demo.go("stores"); }); await sleep(300);
  await ev(() => { document.querySelector("[data-view=stores] .v-body").scrollTop = 120; }); await snap("stores");
  await ev(() => { demo.set({ store: "s1", opt: "trim", time: "18:00", qty: 1 }); demo.go("checkout"); }); await sleep(300);
  await ev(() => { document.querySelector("[data-view=checkout] .v-body").scrollTop = 140; }); await snap("checkout");
  await ev(() => demo.go("done")); await snap("done");
  // 판매자: 아침 메시지 → AI 정리안 (확인 전)
  await ev(() => { window.nowT = () => "09:12"; demo.go("merchant"); st.chat = defaultChat().slice(0, 2); rMerchant(); }); await sleep(300);
  await ev(() => demo.merchantSend("참나물 스무단 들어왔어요 한단 3,500원 손질 가능 시금치는 15단 3천원")); await sleep(1300);
  await clock("09:12"); await snap("merchant_draft");
  // 판매자: 입고 추천 · 마감 할인 (예시 데이터)
  await ev(() => { st.chat = [{ who: "day", text: "10월 30일 금요일" }, { who: "bot", t: "08:55", card: "forecast" }, { who: "bot", t: "19:05", card: "discount" }]; rMerchant(); document.getElementById("chatBody").scrollTop = 0; }); await sleep(300);
  await clock("19:06"); await snap("merchant_forecast");
  await ev(() => demo.go("box")); await snap("preorder");
  await ev(() => { demo.set({ namul: "gosari" }); demo.go("guide"); }); await sleep(300); await snap("guide_gosari");
  await b.close(); console.log("stills v4 ok");
})();

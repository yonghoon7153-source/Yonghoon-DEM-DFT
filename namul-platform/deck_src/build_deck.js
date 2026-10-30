// 나물로 발표자료 v4 (제출본): 본문 12장 + 부록 2장. Problem → Solution → Business → Vision.
// 사용: NODE_PATH=<pptxgenjs가 설치된 node_modules> node build_deck.js [출력.pptx]
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const { setTheme } = require("./theme.js");
const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv[2] || path.join(ROOT, "02_발표자료_나물로.pptx");
const SH = path.join(ROOT, "assets/screens"), DEMO = path.join(ROOT, "assets/demo");
const NOTES = JSON.parse(fs.readFileSync(path.join(__dirname, "script.json"), "utf8"));
const note = (n) => NOTES.find((o) => o.n === n).notes;
const b64 = (p) => "data:image/png;base64," + fs.readFileSync(p).toString("base64");
const pngRatio = (p) => { const b = fs.readFileSync(p); return b.readUInt32BE(20) / b.readUInt32BE(16); }; // h/w (IHDR)
const PH = pngRatio(path.join(SH, "home.png"));

const INK = "1F2421", G700 = "4A524D", G500 = "7A837D", G300 = "B9C1BB", G200 = "D9DED9", G100 = "F2F4F2";
const BRAND = "1E4D3A", BRAND2 = "3F7F5F", BRAND3 = "A8C8B4", BRANDL = "E6F0EA", ACC = "B8692B", ACCL = "FBEFE3", MARK = "E07B2E", COVER = "173A2C";
const THEME_COLORS = { dk1: INK, lt1: "FFFFFF", dk2: BRAND, lt2: G100, accent1: BRAND, accent2: BRAND2, accent3: ACC, accent4: G500, accent5: BRAND3, accent6: G200, hlink: BRAND, folHlink: BRAND2 };

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
  pres.theme = { headFontFace: "Malgun Gothic", bodyFontFace: "Malgun Gothic" };
  pres.author = "나물로"; pres.title = "나물로 창업 아이템 발표";
  const C = pres.SchemeColor;

  // ---------- layouts ----------
  pres.defineSlideMaster({ title: "COVER", background: { color: COVER }, objects: [
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.6, y: 1.95, w: 6.0, h: 0.9, fontSize: 40, bold: true, color: C.background1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 2.9, w: 6.2, h: 0.5, fontSize: 17, color: "DCE7E0", margin: 0, valign: "top" }, text: "" } } ] });
  const wordmark = { text: { text: "NAMULLO", options: { x: 7.6, y: 0.22, w: 1.95, h: 0.26, fontSize: 9, bold: true, color: G500, align: "right", charSpacing: 3, margin: 0 } } };
  const footer = (x) => ({ text: { text: "나물로  |  창업 아이템 발표", options: { x, y: 5.22, w: 2.4, h: 0.25, fontSize: 9, color: G500, align: x > 5 ? "right" : "left", margin: 0 } } });
  pres.defineSlideMaster({ title: "CONTENT", background: { color: "FFFFFF" }, objects: [
    { rect: { x: 0.45, y: 1.0, w: 9.1, h: 0.55, fill: { color: G100 }, line: { color: G100, width: 0 } } }, wordmark, footer(6.65),
    { placeholder: { options: { name: "label", type: "body", x: 0.45, y: 0.22, w: 6.5, h: 0.26, fontSize: 11, bold: true, color: C.accent1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.45, y: 0.48, w: 9.1, h: 0.46, fontSize: 22, bold: true, color: C.text1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "msg", type: "body", x: 0.62, y: 1.0, w: 8.8, h: 0.55, fontSize: 13, bold: true, color: C.text1, margin: 0, valign: "middle" }, text: "" } } ],
    slideNumber: { x: 9.15, y: 5.22, w: 0.4, h: 0.25, fontSize: 9, color: G500, align: "right" } });
  pres.defineSlideMaster({ title: "DEMO", background: { color: "FFFFFF" }, objects: [ footer(0.45),
    { placeholder: { options: { name: "label", type: "body", x: 0.45, y: 0.22, w: 6.0, h: 0.26, fontSize: 11, bold: true, color: C.accent1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.45, y: 0.48, w: 6.0, h: 0.46, fontSize: 22, bold: true, color: C.text1, margin: 0, valign: "middle" }, text: "" } } ],
    slideNumber: { x: 6.0, y: 5.22, w: 0.4, h: 0.25, fontSize: 9, color: G500, align: "right" } });
  pres.defineSlideMaster({ title: "CLOSING", background: { color: COVER }, objects: [
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.6, y: 0.95, w: 8.8, h: 0.75, fontSize: 34, bold: true, color: C.background1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 1.72, w: 8.8, h: 0.45, fontSize: 15, color: "DCE7E0", margin: 0, valign: "top" }, text: "" } } ] });

  // ---------- helpers ----------
  const tx = (s, t, o) => s.addText(t, { isTextBox: true, margin: 0, ...o });
  const head = (s, label, title, msg) => { s.addText(label, { placeholder: "label" }); s.addText(title, { placeholder: "title" }); if (msg) s.addText(msg, { placeholder: "msg" }); };
  const foot = (s, t, x = 0.45, w = 6.1) => tx(s, t, { x, y: 5.0, w, h: 0.42, fontSize: 9, color: G500, valign: "bottom", objectName: "source note" });
  const box = (s, x, y, w, h, fill, name, line) => s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: fill }, line: { color: line || fill, width: line ? 0.75 : 0 }, objectName: name });
  const bd = (bottom = true) => [{ type: "none" }, { type: "none" }, bottom ? { type: "solid", pt: 0.75, color: G200 } : { type: "none" }, { type: "none" }];
  function table(s, header, body, o) {
    const rows = [];
    if (header) rows.push(header.map((h, j) => ({ text: h, options: { bold: true, color: "FFFFFF", fill: { color: (o.headFills && o.headFills[j]) || BRAND }, fontSize: o.headSize || o.size || 12, align: (o.headAlign && o.headAlign[j]) || "center", valign: "middle", border: bd(false) } })));
    body.forEach((r, i) => rows.push(r.map((c, j) => {
      const opt = { fontSize: o.size || 12, color: INK, valign: "middle", align: (o.align && o.align[j]) || "left", fill: { color: j === 0 && o.firstCol !== false ? G100 : "FFFFFF" }, bold: j === 0 && o.firstCol !== false, border: bd(true) };
      if (o.hlRow === i) opt.fill = { color: BRANDL };
      return typeof c === "string" ? { text: c, options: opt } : { text: c.t, options: { ...opt, ...c.o } };
    })));
    s.addTable(rows, { x: o.x, y: o.y, w: o.w, colW: o.colW, rowH: o.rowH, margin: o.margin || [0.04, 0.1, 0.04, 0.1], objectName: o.name || "table" });
  }
  const chartBase = () => ({ titleFontFace: "+mn-lt", titleFontSize: 12, titleColor: INK, showTitle: true, showValue: true, dataLabelFontFace: "+mn-lt", dataLabelFontSize: 12, dataLabelColor: INK, dataLabelFormatCode: "General",
    catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 12, catAxisLabelColor: G700, catGridLine: { style: "none" }, valAxisLabelFontFace: "+mn-lt", valAxisLabelFontSize: 10, valAxisLabelColor: G500, valGridLine: { style: "none" }, catAxisLineColor: G300, valAxisHidden: true, showLegend: false });
  const content = (n, sec) => { const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: sec }); s.addNotes(note(n)); return s; };
  const phone = (s, file, x, y, h, alt) => s.addImage({ data: b64(path.join(SH, file + ".png")), x, y, w: h / PH, h, objectName: "screen " + file, altText: "나물로 프로토타입 화면: " + alt });
  const badge = (s, n, x, y, d = 0.3) => { s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: MARK }, line: { color: "FFFFFF", width: 1.5 }, objectName: "badge " + n }); tx(s, String(n), { x, y, w: d, h: d, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle", objectName: "badge text " + n }); };
  const tag = (s, t, x, y, on) => { const w = 0.16 + t.length * 0.115; s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.24, rectRadius: 0.12, fill: { color: on ? BRANDL : G100 }, line: { color: on ? BRANDL : G200, width: 0.75 }, objectName: "status " + t }); tx(s, t, { x, y, w, h: 0.24, fontSize: 9.5, bold: true, color: on ? BRAND : G700, align: "center", valign: "middle", objectName: "status text " + t }); };

  // ================= 1. 표지 =================
  pres.addSection({ title: "표지" });
  { const s = pres.addSlide({ masterName: "COVER", sectionTitle: "표지" });
    tx(s, "NAMULLO", { x: 0.6, y: 0.55, w: 3, h: 0.3, fontSize: 11, bold: true, color: "C7D6CC", charSpacing: 4, objectName: "wordmark" });
    tx(s, "창업 아이템 발표", { x: 0.6, y: 1.5, w: 5.5, h: 0.35, fontSize: 14, color: "A9C2B3", objectName: "kicker" });
    s.addText("나물로", { placeholder: "title" });
    s.addText("레시피로 고르고 전통시장에서 사는 나물 장보기", { placeholder: "body" });
    tx(s, "나물 한 봉지로 지역 상권을 돕는 장보기", { x: 0.6, y: 3.45, w: 6.0, h: 0.32, fontSize: 13, color: "C7D6CC", objectName: "one-liner" });
    let cx = 0.6;
    ["나물 접근성", "지역 상권 상생", "AI 기반", "레시피 연계"].forEach((c, i) => { const w = 0.32 + [...c].reduce((a, ch) => a + (/[가-힣]/.test(ch) ? 0.165 : ch === " " ? 0.06 : 0.1), 0);
      s.addShape(pres.ShapeType.roundRect, { x: cx, y: 3.95, w, h: 0.34, rectRadius: 0.17, fill: { color: "24503D" }, line: { color: BRAND2, width: 0.75 }, objectName: "pillar " + i });
      tx(s, c, { x: cx, y: 3.95, w, h: 0.34, fontSize: 11.5, bold: true, color: "FFFFFF", align: "center", valign: "middle", objectName: "pillar text " + i }); cx += w + 0.12; });
    tx(s, "2026. 11.     ○○학과  ○○○", { x: 0.6, y: 4.8, w: 5, h: 0.3, fontSize: 12, color: "A9C2B3", objectName: "presenter" });
    phone(s, "home", 7.05, 0.38, 4.85, "홈 화면");
    s.addNotes(note(1)); }

  // ================= 2. Problem: 고객 =================
  pres.addSection({ title: "Problem" });
  { const s = content(2, "Problem");
    head(s, "Problem  |  고객의 문제와 필요", "고객 문제", "나물을 먹고 싶어도 장보기·손질·메뉴 고민 때문에 덜 먹는 바쁜 가구(맞벌이·1인 가구)가 주 고객");
    [["01", "시간 부족", "퇴근 후 장보기와 저녁 준비\n시간이 짧음"], ["02", "메뉴 고민", "무엇을 해 먹을지, 아이가\n먹을지 정하기 어려움"],
     ["03", "손질 부담", "나물은 다듬기·데치기 과정이\n번거로움"], ["04", "시장 가기 어려움", "시장 나물을 사고 싶어도\n퇴근 후엔 들를 시간이 없음"]].forEach(([n, h, d], i) => {
      const x = 0.45 + (i % 2) * 2.98, y = 1.72 + Math.floor(i / 2) * 1.62;
      box(s, x, y, 2.86, 1.5, G100, "pain box " + n);
      tx(s, n, { x: x + 0.2, y: y + 0.16, w: 0.6, h: 0.28, fontSize: 12, bold: true, color: G500, objectName: "pain num " + n });
      tx(s, h, { x: x + 0.2, y: y + 0.44, w: 2.5, h: 0.36, fontSize: 15, bold: true, color: INK, objectName: "pain head " + n });
      tx(s, d, { x: x + 0.2, y: y + 0.84, w: 2.55, h: 0.56, fontSize: 12, color: G700, objectName: "pain desc " + n }); });
    box(s, 6.48, 1.72, 3.07, 3.12, BRANDL, "stat panel");
    tx(s, "18세 미만 자녀를 둔 부부 가구\n맞벌이 비율 (2025, 처음 60% 넘음)", { x: 6.68, y: 1.84, w: 2.75, h: 0.44, fontSize: 11, color: G700, objectName: "stat label" });
    tx(s, "60.4%", { x: 6.68, y: 2.28, w: 2.6, h: 0.54, fontSize: 30, bold: true, color: BRAND, objectName: "stat value" });
    s.addShape(pres.ShapeType.line, { x: 6.68, y: 2.9, w: 2.67, h: 0, line: { color: BRAND3, width: 0.75 }, objectName: "stat rule 1" });
    tx(s, "1인 가구 비중\n(2025, 824만 가구로 역대 최대)", { x: 6.68, y: 2.98, w: 2.75, h: 0.44, fontSize: 11, color: G700, objectName: "stat label 2" });
    tx(s, "36.6%", { x: 6.68, y: 3.42, w: 2.6, h: 0.54, fontSize: 30, bold: true, color: BRAND, objectName: "stat value 2" });
    s.addShape(pres.ShapeType.line, { x: 6.68, y: 4.04, w: 2.67, h: 0, line: { color: BRAND3, width: 0.75 }, objectName: "stat rule 2" });
    tx(s, "대구 유아 86명 조사에서도 반찬류를\n꺼리는 경향 (정유미, 2019)", { x: 6.68, y: 4.12, w: 2.75, h: 0.44, fontSize: 10.5, color: INK, objectName: "stat research" });
    foot(s, "자료: 국가데이터처 「2025년 하반기 지역별고용조사」(2026.06 보도)·「2025 인구주택총조사」(2026.07 발표), 정유미(2019) 「유아의 나이에 따른 편식 및 식습관 실태」 한국식생활문화학회지 34(5)"); }

  // ================= 3. Problem: 판매자 =================
  { const s = content(3, "Problem");
    head(s, "Problem  |  판매자의 문제와 필요", "판매자 문제", "온라인 구매 수요는 보도로 확인되나, 점포의 상품 등록·주문 응대 부담은 인터뷰로 확인할 가설임");
    [["1,393곳 · 28.7조 원", "전국 전통시장 수 · 연매출 (2023)", BRAND, 20], ["−9.3%", "산나물 생산액, 전년 대비 (2024)", ACC, 26], ["+196%", "배민 전통시장 장보기 입점 점포 매출,\n1년 증가율 (2026.3 보도)", BRAND, 26]].forEach(([v, d, col, fs], i) => {
      const y = 1.72 + i * 1.06;
      box(s, 0.45, y, 3.35, 0.96, G100, "kpi box " + i);
      tx(s, v, { x: 0.65, y: y + 0.08, w: 3.0, h: 0.46, fontSize: fs, bold: true, color: col, valign: "middle", objectName: "kpi value " + i });
      tx(s, d, { x: 0.65, y: y + 0.52, w: 3.05, h: 0.4, fontSize: 10.5, color: G700, objectName: "kpi desc " + i }); });
    tx(s, "예상되는 문제 (인터뷰로 확인할 가설)", { x: 4.15, y: 1.72, w: 5.4, h: 0.3, fontSize: 12, bold: true, color: BRAND, objectName: "pain title" });
    [["온라인 운영 부담", "상품을 올리고 주문에 응대하는 일이 늘어날 것으로 예상"], ["손질 서비스 홍보", "손질해서 팔면 값을 더 받을 수 있어도 알릴 방법이 부족할 것"], ["제철 재고 부담", "제철에 물량이 몰려 남는 재고가 생길 것으로 예상"]].forEach(([h, d], i) => {
      const y = 2.1 + i * 0.78;
      badge(s, i + 1, 4.15, y + 0.03);
      tx(s, h, { x: 4.6, y, w: 4.95, h: 0.34, fontSize: 14, bold: true, color: INK, valign: "middle", objectName: "seller pain " + i });
      tx(s, d, { x: 4.6, y: y + 0.36, w: 4.95, h: 0.32, fontSize: 12, color: G700, objectName: "seller pain desc " + i });
      if (i < 2) s.addShape(pres.ShapeType.line, { x: 4.6, y: y + 0.72, w: 4.95, h: 0, line: { color: G200, width: 0.75 }, objectName: "pain rule " + i }); });
    box(s, 4.15, 4.38, 5.4, 0.42, BRANDL, "need band");
    tx(s, [{ text: "필요  ", options: { bold: true, color: BRAND } }, { text: "간단한 상품 등록과 손질·예약 주문", options: { color: INK } }], { x: 4.28, y: 4.38, w: 5.2, h: 0.42, fontSize: 11.5, valign: "middle", objectName: "need text" });
    foot(s, "자료: 소상공인시장진흥공단 전통시장 실태조사(2023 기준), 산림청 「2024년 임산물생산조사」(2025.10), 머니투데이(2026.03) / 증가율은 입점 점포 기준 보도 수치"); }

  // ================= 4. Solution: 서비스 개요 =================
  pres.addSection({ title: "Solution" });
  { const s = content(4, "Solution");
    head(s, "Solution  |  서비스", "서비스 개요", "레시피 탐색부터 전통시장 가게 주문, 픽업·저녁 배달까지 한 앱에서 처리하는 O2O 커머스");
    [["01  레시피 탐색", "제철 나물 정보·손질법, 아이 선호 메뉴 추천,\n유튜브 레시피 영상 연동"], ["02  재료 담기", "레시피 재료 가운데 집에 없는 것만 골라\n장바구니에 담기"], ["03  주문 · 받기", "가까운 전통시장 나물 가게 비교, 손질·데침 옵션,\n시장 픽업(무료) 또는 저녁 배달 선택"]].forEach(([h, d], i) => {
      const y = 1.72 + i * 0.86;
      s.addShape(pres.ShapeType.homePlate, { x: 0.45, y, w: 1.85, h: 0.74, fill: { color: i === 2 ? BRAND : BRAND2 }, line: { color: i === 2 ? BRAND : BRAND2, width: 0 }, objectName: "step " + i });
      tx(s, h, { x: 0.6, y, w: 1.6, h: 0.74, fontSize: 13, bold: true, color: "FFFFFF", valign: "middle", objectName: "step text " + i });
      tx(s, d, { x: 2.5, y, w: 4.3, h: 0.74, fontSize: 12, color: INK, valign: "middle", objectName: "step desc " + i });
      if (i < 2) s.addShape(pres.ShapeType.line, { x: 2.5, y: y + 0.8, w: 4.3, h: 0, line: { color: G200, width: 0.75 }, objectName: "step rule " + i }); });
    box(s, 0.45, 4.36, 6.35, 0.56, G100, "subscription band");
    tx(s, [{ text: "+ 시장 가게 주문 내역   ", options: { bold: true, color: BRAND } }, { text: "어느 시장 가게에서 얼마를 샀는지 표시", options: { color: INK } }], { x: 0.6, y: 4.36, w: 6.1, h: 0.56, fontSize: 12, valign: "middle", objectName: "subscription text" });
    phone(s, "home", 7.45, 1.66, 3.3, "홈 화면");
    foot(s, "주: 앱 화면은 웹 프로토타입 (매장·가격·선호도는 예시 데이터)"); }

  // ================= 5. Solution: AI 적용 =================
  { const s = content(5, "Solution");
    head(s, "Solution  |  AI 기능", "AI 적용 기능과 구현 현황", "AI는 고객 추천과 판매자 상품 등록에 먼저 적용하고, 판매자 확인을 거쳐 앱에 반영함");
    const h = 3.3, w = h / PH;
    [["aichef", "레시피 추천 화면"], ["merchant_draft", "판매자 상품 등록안 화면"], ["merchant_forecast", "발주 추천·마감 할인 예시 화면"]].forEach(([f, alt], i) => {
      const x = 0.45 + i * (w + 0.14); phone(s, f, x, 1.66, h, alt); badge(s, i + 1, x - 0.06, 1.6); });
    const caps = [["레시피 추천 (고객)", "시연 구현", true, "아이 나이·보유 재료를 입력하면 근처 시장 가게\n재고로 만들 수 있는 반찬을 추천"],
      ["상품 등록 자동화 (판매자)", "시연 구현", true, "메시지 한 줄을 품목·수량·가격으로 정리,\n판매자가 확인해야 앱에 반영"],
      ["발주량 추천 · 마감 할인", "개발 예정", false, "판매 이력·요일·날씨 기반, 주문 데이터가\n쌓인 뒤 도입"]];
    caps.forEach(([t, st, on, d], i) => {
      const y = 1.7 + i * 1.1, x = 5.55;
      badge(s, i + 1, x, y + 0.02);
      tx(s, t, { x: x + 0.42, y, w: 2.45, h: 0.34, fontSize: 13.5, bold: true, color: INK, valign: "middle", objectName: "cap title " + i });
      tag(s, st, 9.55 - (0.16 + st.length * 0.115), y + 0.05, on);
      tx(s, d, { x: x + 0.42, y: y + 0.38, w: 3.6, h: 0.56, fontSize: 11.5, color: G700, objectName: "cap desc " + i });
      if (i < 2) s.addShape(pres.ShapeType.line, { x: x + 0.42, y: y + 1.0, w: 3.58, h: 0, line: { color: G200, width: 0.75 }, objectName: "cap rule " + i }); });
    foot(s, "주: 시연 화면의 AI 응답·매장·가격·예측 수치는 예시 데이터이며 실제 AI 호출은 검증 전 · AI는 야생 채취 식물의 식용 여부를 판단하지 않음"); }

  // ================= 6. Solution: 시연 =================
  { const s = pres.addSlide({ masterName: "DEMO", sectionTitle: "Solution" }); s.addNotes(note(6));
    head(s, "Solution  |  시연", "프로토타입 시연", null);
    tx(s, "사용 시나리오: 맞벌이 부모의 평일 저녁 장보기", { x: 0.45, y: 1.0, w: 6.0, h: 0.32, fontSize: 13, bold: true, color: G700, objectName: "demo sub" });
    const steps = [["17:00", "레시피 추천 요청", "‘다섯 살 아이랑 먹을 순한 반찬’"], ["17:02", "레시피 확인 · 재료 담기", "참나물 들기름무침 → 참나물 200g 담기"], ["17:03", "시장 가게 선택 · 받는 방법", "600m 새벽시장 가게, 손질 옵션, 18:00 픽업"], ["17:04", "판매자 주문 접수", "판매자 화면에서 주문 확인 후 접수"]];
    s.addShape(pres.ShapeType.line, { x: 0.86, y: 1.62, w: 0, h: 2.3, line: { color: G200, width: 1.5 }, objectName: "timeline" });
    steps.forEach(([t, h, d], i) => { const y = 1.48 + i * 0.72;
      s.addShape(pres.ShapeType.roundRect, { x: 0.45, y: y + 0.04, w: 0.82, h: 0.32, rectRadius: 0.16, fill: { color: i === 3 ? MARK : BRAND }, line: { color: i === 3 ? MARK : BRAND, width: 0 }, objectName: "time pill " + i });
      tx(s, t, { x: 0.45, y: y + 0.04, w: 0.82, h: 0.32, fontSize: 10.5, bold: true, color: "FFFFFF", align: "center", valign: "middle", objectName: "time text " + i });
      tx(s, h, { x: 1.45, y, w: 4.9, h: 0.3, fontSize: 14, bold: true, color: INK, objectName: "demo step " + i });
      tx(s, d, { x: 1.45, y: y + 0.31, w: 4.9, h: 0.28, fontSize: 12, color: G700, objectName: "demo detail " + i }); });
    box(s, 0.45, 4.48, 5.95, 0.46, G100, "demo note band");
    tx(s, [{ text: "시연 범위  ", options: { bold: true, color: BRAND } }, { text: "추천 확인부터 픽업 예약, 판매자 접수까지의 흐름" }], { x: 0.6, y: 4.48, w: 5.7, h: 0.46, fontSize: 12, color: INK, valign: "middle", objectName: "demo result" });
    const vh = 4.78, vw = vh * 414 / 868, vx = 6.95, vy = 0.36;
    s.addMedia({ type: "video", path: path.join(DEMO, "demo_phone.mp4"), x: vx, y: vy, w: vw, h: vh, cover: b64(path.join(DEMO, "demo_poster.png")), objectName: "demo video" });
    tx(s, "슬라이드 쇼에서 재생 · 예시 데이터", { x: vx - 0.45, y: 5.18, w: vw + 0.9, h: 0.25, fontSize: 8.5, color: G500, align: "center", objectName: "demo caption" });
    fs.writeFileSync(path.join(__dirname, "demo_rect.json"), JSON.stringify({ slide: 6, x: vx, y: vy, w: vw, h: vh })); }

  // ================= 7. Business: 시장 =================
  pres.addSection({ title: "Business" });
  { const s = content(7, "Business");
    head(s, "Business  |  시장성", "목표 시장", "전통시장 매출 중 수도권 채소·나물류를 1차 목표 시장으로 설정 (비율은 가정, 공개 통계로 보완)");
    [["전체 시장", "28.7조 원", 3.4, G200, INK], ["목표 시장", "약 1.7조 원", 2.6, BRAND2, "FFFFFF"], ["3년차 목표 거래액", "54억 원", 1.8, BRAND, "FFFFFF"]].forEach(([k, v, w, fill, col], i) => { const y = 1.72 + i * 0.86, cx = 2.15;
      s.addShape(pres.ShapeType.trapezoid, { x: cx - w / 2, y, w, h: 0.8, flipV: true, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: "funnel " + k });
      tx(s, [{ text: k, options: { fontSize: 11, breakLine: true } }, { text: v, options: { fontSize: 16, bold: true } }], { x: cx - w / 2, y, w, h: 0.8, color: col, align: "center", valign: "middle", objectName: "funnel text " + k }); });
    table(s, ["구분", "규모", "산출 근거"], [
      ["전체 시장", { t: "28.7조 원", o: { bold: true, align: "center" } }, "전국 전통시장 1,393곳 연매출\n(2023, 식품 외 업종 포함)"],
      ["목표 시장", { t: "약 1.7조 원", o: { bold: true, align: "center", color: BRAND } }, "28.7조 원 × 수도권 40%\n× 채소·나물 15% (가정)"],
      ["3년차 목표", { t: "54억 원", o: { bold: true, align: "center", color: BRAND } }, "입점 300곳 × 월 100건\n× 1.5만 원 × 12개월"],
    ], { x: 4.1, y: 1.68, w: 5.45, colW: [1.2, 1.25, 3.0], rowH: [0.36, 0.78, 0.78, 0.78], align: ["center", "center", "left"], size: 12 });
    box(s, 0.45, 4.45, 9.1, 0.44, G100, "note band");
    tx(s, "온라인 식품 거래는 전통시장 매출과 겹칠 수 있어 전통시장 매출만 기준으로 잡음", { x: 0.6, y: 4.45, w: 8.9, h: 0.44, fontSize: 11.5, color: INK, valign: "middle", objectName: "market note" });
    foot(s, "자료: 소상공인시장진흥공단 전통시장 실태조사(2023 기준) / 주: 수도권·품목 비율과 3년차 목표는 가정 기반 추정"); }

  // ================= 8. Business: 경쟁 =================
  { const s = content(8, "Business");
    head(s, "Business  |  차별성", "경쟁 현황 및 차별점", "레시피에서 고른 나물을 전통시장 가게에 주문하고, 가게별 주문금액을 보여 줌");
    const px = 0.95, py = 1.75, pw = 4.2, ph = 2.85;
    box(s, px, py + ph / 2, pw / 2, ph / 2, BRANDL, "target quadrant");
    s.addShape(pres.ShapeType.rect, { x: px, y: py, w: pw, h: ph, fill: { type: "none" }, line: { color: G300, width: 0.75 }, objectName: "plot frame" });
    s.addShape(pres.ShapeType.line, { x: px + pw / 2, y: py, w: 0, h: ph, line: { color: G200, width: 0.75 }, objectName: "divider v" });
    s.addShape(pres.ShapeType.line, { x: px, y: py + ph / 2, w: pw, h: 0, line: { color: G200, width: 0.75 }, objectName: "divider h" });
    tx(s, "콘텐츠 중심", { x: px, y: py + ph + 0.06, w: 1.6, h: 0.25, fontSize: 10.5, color: G700, objectName: "x axis left" });
    tx(s, "구매 중심", { x: px + pw - 1.6, y: py + ph + 0.06, w: 1.6, h: 0.25, fontSize: 10.5, color: G700, align: "right", objectName: "x axis right" });
    tx(s, "전국\n대상", { x: 0.42, y: py, w: 0.45, h: 0.48, fontSize: 10.5, color: G700, align: "right", objectName: "y axis top" });
    tx(s, "지역\n기반", { x: 0.42, y: py + ph - 0.48, w: 0.45, h: 0.48, fontSize: 10.5, color: G700, align: "right", objectName: "y axis bottom" });
    const dot = (label, cx, cy, hl = false) => { const d = hl ? 0.2 : 0.13;
      s.addShape(pres.ShapeType.ellipse, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color: hl ? ACC : G500 }, line: { color: hl ? ACC : G500, width: 0 }, objectName: "dot " + label });
      tx(s, label, { x: cx + d / 2 + 0.06, y: cy - 0.15, w: 1.6, h: 0.3, fontSize: hl ? 12 : 10.5, bold: hl, color: hl ? ACC : INK, valign: "middle", objectName: "dot label " + label }); };
    dot("레시피 앱·유튜브", px + 0.3, py + 0.55); dot("쿠팡·컬리", px + 2.95, py + 0.45); dot("어글리어스", px + 2.4, py + 1.0);
    dot("배민 장보기", px + 2.85, py + 1.85); dot("네이버", px + 2.4, py + 2.25); dot("당근", px + 3.15, py + 2.55); dot("나물로", px + 0.7, py + 2.2, true);
    tx(s, "기회 영역", { x: px + 0.12, y: py + ph / 2 + 0.1, w: 1.6, h: 0.26, fontSize: 10.5, bold: true, color: BRAND, objectName: "gap caption" });
    tx(s, "차별점", { x: 5.55, y: 1.72, w: 4.0, h: 0.3, fontSize: 12, bold: true, color: BRAND, objectName: "diff title" });
    [["레시피 연동 주문", "레시피 재료를 시장 가게 재고로 바로 주문"], ["지역 상권 상생", "가게가 등록한 가격과 주문 내역을 확인"], ["손질·데침 옵션", "판매자는 추가 매출, 고객은 조리 시간 단축"]].forEach(([h, d], i) => {
      const y = 2.06 + i * 0.8;
      badge(s, i + 1, 5.55, y + 0.02);
      tx(s, h, { x: 6.0, y, w: 3.55, h: 0.34, fontSize: 14, bold: true, color: INK, valign: "middle", objectName: "diff head " + i });
      tx(s, d, { x: 6.0, y: y + 0.35, w: 3.55, h: 0.46, fontSize: 11.5, color: G700, objectName: "diff desc " + i }); });
    box(s, 5.55, 4.52, 4.0, 0.4, BRANDL, "position band");
    tx(s, "목표: 전통시장 가게의 나물 전문 주문 채널", { x: 5.68, y: 4.52, w: 3.8, h: 0.4, fontSize: 11, bold: true, color: BRAND, valign: "middle", objectName: "position text" });
    foot(s, "주: 포지셔닝은 2026.10 공개 정보 기준 자체 판단 / 가격: 한국소비자단체협의회 2026 추석 조사(서울 90곳), 채소·임산물류는 전통시장이 대형마트보다 26.0% 저렴"); }

  // ================= 9. Business: 수익 모델 =================
  { const s = content(9, "Business");
    head(s, "Business  |  수익모델", "수익 모델", "중개 수수료를 기본 수익원으로 하고 판매자 유료 서비스·제휴 광고로 확대, 배달은 별도 이익 없이 연결");
    const nodes = [["고객", "맞벌이·1인 가구", 0.45, 1.75, G100, INK], ["나물로", "주문 · 배달 연결 · 정산", 4.05, 1.75, BRAND, "FFFFFF"], ["판매자", "전통시장 나물 가게", 7.65, 1.75, G100, INK]];
    nodes.forEach(([t, d, x, y, fill, col]) => { box(s, x, y, 1.9, 0.92, fill, "node " + t, fill === G100 ? G300 : null);
      tx(s, [{ text: t, options: { fontSize: 15, bold: true, breakLine: true } }, { text: d, options: { fontSize: 10.5 } }], { x, y, w: 1.9, h: 0.92, color: col, align: "center", valign: "middle", objectName: "node text " + t }); });
    const arrow = (x1, x2, y, name) => s.addShape(pres.ShapeType.line, { x: Math.min(x1, x2), y, w: Math.abs(x2 - x1), h: 0, line: { color: G500, width: 1.25, endArrowType: x2 > x1 ? "triangle" : undefined, beginArrowType: x2 > x1 ? undefined : "triangle" }, objectName: name });
    const lab = (t, x, y, name) => tx(s, t, { x, y, w: 1.7, h: 0.26, fontSize: 10.5, color: G700, align: "center", objectName: name });
    arrow(2.45, 3.95, 2.0, "pay arrow"); lab("주문 결제 · 배달비", 2.35, 1.7, "pay label");
    arrow(3.95, 2.45, 2.42, "service arrow"); lab("레시피 · 픽업 · 배달", 2.35, 2.47, "service label");
    arrow(6.05, 7.55, 2.0, "order arrow"); lab("주문 전달 · 정산", 5.95, 1.7, "order label");
    arrow(7.55, 6.05, 2.42, "stock arrow"); lab("상품 등록 · 수수료", 5.95, 2.47, "stock label");
    table(s, ["수익원", "과금 방식", "비고"], [
      ["중개 수수료", "상품·손질 금액의 4%", "배달비 제외 / 전통시장 첫 6개월 면제"],
      [{ t: "배달비", o: { color: G700 } }, "시험 요금 3,500원", "매출 목표에서 제외 / 차액은 시험 예산으로 지원"],
      ["판매자 유료 서비스", "월 29,000원 (선택)", "발주 추천 · 상단 노출"],
      ["제휴 광고", "건별 계약", "레시피 크리에이터 · 식품 브랜드"],
    ], { x: 0.45, y: 2.92, w: 9.1, colW: [1.9, 2.0, 5.2], rowH: [0.34, 0.4, 0.4, 0.4, 0.4], align: ["left", "left", "left"], size: 12 });
    foot(s, "주: 요금은 예정안이며 파일럿에서 검증 · 판매자 부담 예시: 월 100건 × 1.5만 원 매장 → 수수료 6만 원 + 유료 서비스 2.9만 원 = 월 8.9만 원 (거래액의 약 6%)"); }

  // ================= 10. Vision: 로드맵 =================
  pres.addSection({ title: "Vision" });
  { const s = content(10, "Vision");
    head(s, "Vision  |  사업화 계획", "사업화 로드맵", "시장 1곳 파일럿으로 실제 구매·재구매를 먼저 검증한 뒤, 정부 지원사업과 투자로 단계적 확장");
    const kpi = (t) => ({ t, o: { bold: true, color: BRAND, fill: { color: BRANDL } } });
    table(s, ["구분", "1단계 파일럿\n2026.12~2027.2", "2단계 정식 출시\n2027", "3단계 확장\n2028~"], [
      ["범위", "전통시장 1곳 · 점포 2~3곳", "입점 매장 30곳", "수도권 120곳 → 300곳"],
      ["주요 과제", "웹 프로토타입\n수동 운영, 배달은 단지 한정", "웹앱 출시 · 결제 연동\n명절·제철 예약 오픈", "앱 출시 · 발주 추천 도입"],
      ["자금", "자기자본 300만 원\n배달 지원 최대 20만 원", "예비창업패키지 등\n정부 지원사업", "시드 투자"],
      [{ t: "목표", o: { fill: { color: BRANDL }, color: BRAND } }, kpi("유료 주문 100건"), kpi("월 주문 2,000건"), kpi("3년차 거래액 54억 원")],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [1.3, 2.6, 2.6, 2.6], rowH: [0.56, 0.38, 0.52, 0.52, 0.38], align: ["center", "left", "left", "left"], size: 12, headFills: [BRAND, ACC, BRAND2, BRAND2] });
    box(s, 0.45, 4.1, 9.1, 0.84, G100, "pilot kpi band");
    tx(s, "파일럿 검증 지표", { x: 0.65, y: 4.14, w: 3, h: 0.26, fontSize: 12, bold: true, color: BRAND, objectName: "pilot kpi title" });
    tx(s, "①  유료 주문 수 · 고객 수      ②  30일 재구매율      ③  손질 옵션 선택률\n④  배달 선택률 · 배달 1건당 실제 비용      ⑤  주문당 운영 시간 · 등록 오류율", { x: 0.65, y: 4.42, w: 8.8, h: 0.48, fontSize: 11.5, color: INK, valign: "middle", objectName: "pilot kpi list" });
    foot(s, "주: 2026년 예비창업패키지는 1단계 2천만 원 지원 후 중간평가로 추가 지원(평균 약 4천만 원) · 2027년 공고 조건 확인 필요"); }

  // ================= 11. Vision: 3년 목표 =================
  { const s = content(11, "Vision");
    head(s, "Vision  |  성장 가능성", "3년 목표 및 확장 계획", "3년차 거래액 54억 원·매출 약 2.6억 원을 목표로, 첫 시장에서 재구매와 운영비를 확인한 뒤 확장");
    s.addChart(pres.ChartType.bar, [{ name: "거래액", labels: ["1년차", "2년차", "3년차"], values: [2.5, 15, 54] }],
      { ...chartBase(), x: 0.35, y: 1.66, w: 4.5, h: 2.35, barDir: "col", barGapWidthPct: 70, chartColors: [BRAND3, BRAND2, BRAND], title: "연도별 목표 거래액 (억 원)", valAxisMinVal: 0, valAxisMaxVal: 62, dataLabelPosition: "outEnd", objectName: "gmv chart" });
    box(s, 0.45, 4.1, 4.4, 0.82, G100, "revenue box");
    tx(s, [{ text: "3년차 매출 목표 약 2.6억 원", options: { bold: true, color: BRAND, breakLine: true } }, { text: "수수료 2.2 + 판매자 서비스 0.4 (억 원), 배달비 제외\n보수 시나리오(매장당 월 약 77건) 약 2.1억 원", options: { color: INK, fontSize: 10.5 } }], { x: 0.6, y: 4.12, w: 4.2, h: 0.78, fontSize: 12, valign: "middle", objectName: "revenue text" });
    tx(s, "확장 계획", { x: 5.2, y: 1.72, w: 4.3, h: 0.3, fontSize: 12, bold: true, color: BRAND, objectName: "expand title" });
    table(s, null, [["확장 조건", "첫 시장의 재구매·운영비 확인"], ["지역 확대", "인접 시장·주거 단지 → 수도권"], ["품목 확대", "나물 → 제철 농산물 전체"]],
      { x: 5.2, y: 2.06, w: 4.35, colW: [1.3, 3.05], rowH: [0.42, 0.42, 0.42], align: ["center", "left"], size: 12 });
    tx(s, "기대 효과", { x: 5.2, y: 3.5, w: 4.3, h: 0.3, fontSize: 12, bold: true, color: BRAND, objectName: "effect title" });
    tx(s, [{ text: "전통시장 신규 고객 · 지역 상권 매출 증가", options: { bullet: true, breakLine: true } }, { text: "제철 재고 폐기 감소", options: { bullet: true, breakLine: true } }, { text: "아이 채소 반찬 섭취 개선", options: { bullet: true } }], { x: 5.2, y: 3.84, w: 4.35, h: 1.06, fontSize: 12, color: INK, paraSpaceAfter: 4, objectName: "effect list" });
    foot(s, "주: 재무 수치는 가정 기반 목표치 · 손익분기 시점은 파일럿 실측 후 재산정 (산식은 부록 1)"); }

  // ================= 12. 마무리 =================
  pres.addSection({ title: "마무리" });
  { const s = pres.addSlide({ masterName: "CLOSING", sectionTitle: "마무리" });
    tx(s, "마무리", { x: 0.6, y: 0.6, w: 3, h: 0.3, fontSize: 12, color: "A9C2B3", objectName: "closing label" });
    s.addText("나물로", { placeholder: "title" });
    s.addText("레시피에서 우리 동네 시장 장보기까지", { placeholder: "body" });
    tx(s, "다음 단계", { x: 0.6, y: 2.55, w: 3, h: 0.3, fontSize: 12, bold: true, color: "A9C2B3", objectName: "next steps label" });
    [["01", "고객 인터뷰", "맞벌이·1인 가구 10명\n프로토타입으로 사용성 확인"], ["02", "파일럿", "2026.12~2027.2, 시장 1곳\n유료 주문 100건 · 배달 비용 확인"], ["03", "팀 · 지원사업", "개발·콘텐츠 파트너 모집\n2027 정부 지원사업 신청"]].forEach(([n, h, d], i) => { const x = 0.6 + i * 2.95;
      box(s, x, 2.9, 2.8, 1.4, "214A39", "step box " + n);
      tx(s, n, { x: x + 0.2, y: 3.0, w: 0.6, h: 0.4, fontSize: 18, bold: true, color: "FFFFFF", objectName: "step num " + n });
      tx(s, h, { x: x + 0.82, y: 3.0, w: 1.9, h: 0.4, fontSize: 14, bold: true, color: "FFFFFF", valign: "middle", objectName: "step head " + n });
      tx(s, d, { x: x + 0.2, y: 3.5, w: 2.55, h: 0.7, fontSize: 11.5, color: "C7D6CC", objectName: "step desc " + n }); });
    tx(s, "감사합니다", { x: 0.6, y: 4.62, w: 4, h: 0.42, fontSize: 18, bold: true, color: "FFFFFF", objectName: "thanks" });
    tx(s, "○○학과  ○○○", { x: 5.9, y: 4.62, w: 3.5, h: 0.42, fontSize: 12, color: "A9C2B3", align: "right", valign: "middle", objectName: "presenter" });
    s.addNotes(note(12)); }

  // ================= 13. 부록 1 =================
  pres.addSection({ title: "부록" });
  { const s = content(13, "부록");
    head(s, "부록", "부록 1. 수치 산출 근거", "모든 재무 수치는 가정 기반 추정치이며, 파일럿 실측 후 갱신함");
    const v = (t, o = {}) => ({ t, o: { align: "right", bold: true, ...o } });
    table(s, ["항목", "산식", "값"], [
      ["목표 시장", "28.7조 원 × 수도권 40% × 채소·나물 15%", v("약 1.7조 원")],
      ["3년차 거래액", "입점 300곳 × 월 100건(일반·명절 예약) × 15,000원 × 12개월", v("54억 원")],
      ["중개 수수료", "54억 원 × 4% (배달비 제외, 면제·할인 전)", v("약 2.2억 원")],
      ["판매자 유료 서비스", "120곳 × 월 29,000원 × 12개월", v("약 0.4억 원")],
      [{ t: "3년차 매출 목표", o: { fill: { color: BRANDL }, color: BRAND } }, { t: "수수료 + 판매자 유료 서비스", o: { fill: { color: BRANDL } } }, v("약 2.6억 원", { color: BRAND, fill: { color: BRANDL } })],
      ["보수 시나리오", "거래액 41.4억 원(매장당 월 약 77건) × 4% + 판매자 서비스", v("약 2.1억 원", { color: G700 })],
      ["지자체·제휴 (확장)", "계약 확보 시 추가하는 확장 시나리오 (미검증, 기본 목표에서 제외)", v("+3.1억 원", { color: G700 })],
      ["주문당 수수료 수입", "15,000원 × 4% (변동비 차감 전, 공헌이익 아님)", v("600원")],
      ["배달비 (시험 요금)", "매출 목표 제외 / 차액 최대 20만 원 지원", v("3,500원/건", { color: G700 })],
      ["LLM 호출비 (3년차)", "월 약 5.8만 건 기준, 캐시 적용 / 미적용", v("월 약 72만~99만 원")],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [2.15, 5.0, 1.95], rowH: [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], align: ["left", "left", "right"], size: 11, headSize: 11, margin: [0.02, 0.1, 0.02, 0.1] });
    foot(s, "주: LLM 호출비는 Claude API 가격표(2026.10, 1달러=1,400원) 기준, 재시도·서버·검수 별도 / 배달대행 요금은 견적으로 확인 (2024.10 일부 업체 5,400~5,800원 인상 예정 보도)"); }

  // ================= 14. 부록 2 =================
  { const s = content(14, "부록");
    head(s, "부록", "부록 2. 참고 자료", "수치는 2026.10 웹 검색 기준 공개 통계·보도이며, 발표 전 원문 확인 권장");
    const L = [["국가데이터처, 맞벌이 가구 현황 2025 하반기 (뉴시스)", "https://www.newsis.com/view/NISX20260618_0003673686"],
      ["국가데이터처, 2025 인구주택총조사 1인 가구 (YTN)", "https://www.ytn.co.kr/_ln/0102_202607281324445082"],
      ["소상공인시장진흥공단, 전통시장 실태조사 2023 (뉴시스)", "https://www.newsis.com/view/NISX20250103_0003020386"],
      ["산림청, 2024년 임산물생산조사 (e-나라지표)", "https://www.index.go.kr/unify/idx-info.do?idxCd=1302"],
      ["머니투데이, 배민 전통시장 장보기 입점 성과 (2026.03.18)", "https://www.mt.co.kr/tech/2026/03/18/2026031714425925652"],
      ["정유미(2019), 유아의 나이에 따른 편식 및 식습관 실태, 한국식생활문화학회지 34(5)", "https://koreascience.or.kr/article/JAKO201931765048406.page"],
      ["식품의약품안전처, 산나물과 독초 구별 안내 (웹진)", "https://www.mfds.go.kr/webzine/201504/pdf/main.pdf"],
      ["중소벤처기업부 공고 제2026-143호, 예비창업패키지 수정공고", "https://hanok.gongju.go.kr/cmm/fms/FileDown.do?atchFileId=FILE_0000127870Uc2bM&fileSn=0"]];
    const R = [["네이버, 스마트플레이스 AI 리뷰 관리 · 톡톡 AI FAQ 발표", "https://navercorp.com/media/pressReleasesDetail?seq=34203"],
      ["쿠팡 · 컬리 · 어글리어스 · 당근 서비스 소개 (2026.10 확인, 자체 정리)", null],
      ["뉴데일리, 배달대행 기본료 인상 예정 보도 (2024.10.07)", "https://biz.newdaily.co.kr/site/data/html/2024/10/07/2024100700114.amp.html"],
      ["바이라인네트워크, 배민스토어 전통시장 합배송 (2024.01)", "https://byline.network/2024/01/30_baeminstore"],
      ["한국소비자단체협의회, 2026 추석 제수용품 조사", "https://www.insight.co.kr/news/572535"],
      ["Anthropic, Claude API 가격표 (2026.10)", "https://platform.claude.com/docs/en/about-claude/pricing"],
      ["아이콘 Fluent Emoji (MIT) · 글꼴 Pretendard (OFL)", "https://github.com/microsoft/fluentui-emoji"]];
    const col = (arr, start, x, h) => { tx(s, h, { x, y: 1.68, w: 4.45, h: 0.3, fontSize: 12, bold: true, color: C.accent1, objectName: "ref head " + h });
      s.addText(arr.map(([t, url], i) => ({ text: t, options: { bullet: { type: "number", numberStartAt: start }, breakLine: i < arr.length - 1, ...(url ? { hyperlink: { url, tooltip: url } } : {}) } })), { x, y: 2.02, w: 4.45, h: 2.95, fontSize: 10.5, color: INK, paraSpaceAfter: 6, lineSpacingMultiple: 1.12, valign: "top", margin: 0, isTextBox: true, objectName: "ref list " + h }); };
    col(L, 1, 0.45, "통계 · 시장 · 연구"); col(R, L.length + 1, 5.1, "경쟁 · 기술 · 자료");
    foot(s, "밑줄 친 항목은 원문 링크 · 전체 목록과 확인 메모는 04_레퍼런스_나물로.md"); }

  await pres.writeFile({ fileName: OUT });
  await setTheme(OUT, "Namullo", THEME_COLORS);
  console.log("wrote", OUT);
})().catch((e) => { console.error(e); process.exit(1); });

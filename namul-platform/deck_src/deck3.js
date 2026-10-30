// 나물로 사업계획 v3 — 기업 보고형 + AI + 앱 화면 + 시연
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { applyTheme } = require("/root/.claude/skills/synced/0ec0020a-de2b-4a83-890d-21ddf8272824_eda503ec-9c2e-4018-bdaa-d17eed9d7a32/pptx/scripts/apply_theme.js");
const OUT = process.argv[2];
const SP = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/a9086aab-2880-555b-a3e5-137ced4672cf/scratchpad";
const SH = SP + "/proto/shots/deck/", REC = SP + "/proto/rec/";
const NOTES = JSON.parse(fs.readFileSync(__dirname + "/script.json", "utf8"));
const note = (n) => NOTES.find((o) => o.n === n).notes;
const b64 = (p) => "data:image/png;base64," + fs.readFileSync(p).toString("base64");
const PH = 1736 / 828; // phone screenshot h/w

const INK = "1F2421", G700 = "4A524D", G500 = "7A837D", G300 = "B9C1BB", G200 = "D9DED9", G100 = "F2F4F2";
const BRAND = "1E4D3A", BRAND2 = "3F7F5F", BRAND3 = "A8C8B4", BRANDL = "E6F0EA", ACC = "B8692B", MARK = "E07B2E", COVER = "173A2C";
const THEME = { name: "Namullo Corporate", headFontFace: "Malgun Gothic", bodyFontFace: "Malgun Gothic",
  colors: { dk1: INK, lt1: "FFFFFF", dk2: BRAND, lt2: G100, accent1: BRAND, accent2: BRAND2, accent3: ACC, accent4: G500, accent5: BRAND3, accent6: G200, hlink: BRAND, folHlink: BRAND2 } };

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.author = "Namullo"; pres.title = "나물로 사업계획";
  const C = pres.SchemeColor;

  // ---------- layouts ----------
  pres.defineSlideMaster({ title: "COVER", background: { color: COVER }, objects: [
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.6, y: 2.05, w: 6.0, h: 0.85, fontSize: 32, bold: true, color: C.background1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 2.95, w: 6.0, h: 0.5, fontSize: 15, color: "DCE7E0", margin: 0, valign: "top" }, text: "" } } ] });
  const wordmark = { text: { text: "NAMULLO", options: { x: 7.6, y: 0.22, w: 1.95, h: 0.26, fontSize: 9, bold: true, color: G500, align: "right", charSpacing: 3, margin: 0 } } };
  pres.defineSlideMaster({ title: "CONTENT", background: { color: "FFFFFF" }, objects: [
    { rect: { x: 0.45, y: 1.0, w: 9.1, h: 0.55, fill: { color: G100 }, line: { color: G100, width: 0 } } }, wordmark,
    { text: { text: "나물로 사업계획", options: { x: 7.0, y: 5.22, w: 2.05, h: 0.25, fontSize: 9, color: G500, align: "right", margin: 0 } } },
    { placeholder: { options: { name: "label", type: "body", x: 0.45, y: 0.22, w: 6.5, h: 0.26, fontSize: 10, bold: true, color: C.accent1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.45, y: 0.48, w: 9.1, h: 0.46, fontSize: 22, bold: true, color: C.text1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "msg", type: "body", x: 0.62, y: 1.0, w: 8.8, h: 0.55, fontSize: 12.5, bold: true, color: C.text1, margin: 0, valign: "middle" }, text: "" } } ],
    slideNumber: { x: 9.15, y: 5.22, w: 0.4, h: 0.25, fontSize: 9, color: G500, align: "right" } });
  pres.defineSlideMaster({ title: "DEMO", background: { color: "FFFFFF" }, objects: [
    { text: { text: "나물로 사업계획", options: { x: 0.45, y: 5.22, w: 2.05, h: 0.25, fontSize: 9, color: G500, margin: 0 } } },
    { placeholder: { options: { name: "label", type: "body", x: 0.45, y: 0.22, w: 6.0, h: 0.26, fontSize: 10, bold: true, color: C.accent1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.45, y: 0.48, w: 6.0, h: 0.46, fontSize: 22, bold: true, color: C.text1, margin: 0, valign: "middle" }, text: "" } } ],
    slideNumber: { x: 6.0, y: 5.22, w: 0.4, h: 0.25, fontSize: 9, color: G500, align: "right" } });
  pres.defineSlideMaster({ title: "PLAIN", background: { color: "FFFFFF" }, objects: [ wordmark,
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.6, y: 0.95, w: 2.6, h: 0.6, fontSize: 28, bold: true, color: C.accent1, margin: 0, valign: "middle" }, text: "" } } ],
    slideNumber: { x: 9.15, y: 5.22, w: 0.4, h: 0.25, fontSize: 9, color: G500, align: "right" } });
  pres.defineSlideMaster({ title: "CLOSING", background: { color: COVER }, objects: [
    { placeholder: { options: { name: "title", type: "title", align: "left", x: 0.6, y: 0.95, w: 8.8, h: 0.7, fontSize: 32, bold: true, color: C.background1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 1.7, w: 8.8, h: 0.45, fontSize: 14, color: "DCE7E0", margin: 0, valign: "top" }, text: "" } } ] });

  // ---------- helpers ----------
  const tx = (s, t, o) => s.addText(t, { isTextBox: true, margin: 0, ...o });
  const head = (s, label, title, msg) => { s.addText(label, { placeholder: "label" }); s.addText(title, { placeholder: "title" }); if (msg) s.addText(msg, { placeholder: "msg" }); };
  const foot = (s, t, x = 0.45, w = 6.45) => tx(s, t, { x, y: 5.04, w, h: 0.38, fontSize: 9, color: G500, valign: "bottom", objectName: "source note" });
  const bd = (bottom = true) => [{ type: "none" }, { type: "none" }, bottom ? { type: "solid", pt: 0.75, color: G200 } : { type: "none" }, { type: "none" }];
  function table(s, header, body, o) {
    const rows = [];
    if (header) rows.push(header.map((h, j) => ({ text: h, options: { bold: true, color: "FFFFFF", fill: { color: (o.headFills && o.headFills[j]) || BRAND }, fontSize: o.headSize || 10.5, align: (o.headAlign && o.headAlign[j]) || "center", valign: "middle", border: bd(false) } })));
    body.forEach((r, i) => rows.push(r.map((c, j) => {
      const opt = { fontSize: o.size || 10.5, color: INK, valign: "middle", align: (o.align && o.align[j]) || "left", fill: { color: j === 0 && o.firstCol !== false ? G100 : "FFFFFF" }, bold: j === 0 && o.firstCol !== false, border: bd(true) };
      if (o.hlRow === i) opt.fill = { color: BRANDL };
      if (o.hlCol === j) { opt.fill = { color: BRANDL }; opt.bold = true; opt.color = BRAND; }
      return typeof c === "string" ? { text: c, options: opt } : { text: c.t, options: { ...opt, ...c.o } };
    })));
    s.addTable(rows, { x: o.x, y: o.y, w: o.w, colW: o.colW, rowH: o.rowH, margin: o.margin || [0.04, 0.08, 0.04, 0.08], objectName: o.name || "table" });
  }
  const chartBase = () => ({ titleFontFace: "+mn-lt", titleFontSize: 10.5, titleColor: INK, showTitle: true, showValue: true, dataLabelFontFace: "+mn-lt", dataLabelFontSize: 10, dataLabelColor: INK, dataLabelFormatCode: "General",
    catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 10, catAxisLabelColor: G700, catGridLine: { style: "none" }, valAxisLabelFontFace: "+mn-lt", valAxisLabelFontSize: 9, valAxisLabelColor: G500, valGridLine: { style: "none" }, catAxisLineColor: G300, valAxisHidden: true, showLegend: false });
  const content = (n, sec) => { const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: sec }); s.addNotes(note(n)); return s; };
  const phone = (s, file, x, y, h, name) => s.addImage({ data: b64(SH + file + ".png"), x, y, w: h / PH, h, objectName: name || file, altText: "나물로 앱 화면: " + (name || file) });
  const badge = (s, n, x, y, d = 0.3) => { s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: MARK }, line: { color: MARK, width: 0 }, objectName: "badge " + n }); tx(s, String(n), { x, y, w: d, h: d, fontSize: 11, bold: true, color: "FFFFFF", align: "center", valign: "middle", objectName: "badge text " + n }); };
  function screenSlide(n, sec, label, title, msg, files, caps, src) {
    const s = content(n, sec); head(s, label, title, msg);
    const h = 3.32, w = h / PH;
    files.forEach((f, i) => phone(s, f, 0.45 + i * (w + 0.16), 1.66, h, f));
    caps.forEach(([t, d, impl], i) => {
      const y = 1.7 + i * 1.08, x = 5.72;
      badge(s, i + 1, x, y + 0.02);
      tx(s, t, { x: x + 0.42, y, w: 3.4, h: 0.32, fontSize: 12.5, bold: true, color: INK, valign: "middle", objectName: "cap title " + (i + 1) });
      tx(s, d, { x: x + 0.42, y: y + 0.33, w: 3.4, h: 0.44, fontSize: 10, color: G700, objectName: "cap desc " + (i + 1) });
      tx(s, [{ text: "구현  ", options: { bold: true, color: BRAND } }, { text: impl, options: { color: G700 } }], { x: x + 0.42, y: y + 0.77, w: 3.4, h: 0.24, fontSize: 9.5, objectName: "cap impl " + (i + 1) });
      if (i < caps.length - 1) s.addShape(pres.ShapeType.line, { x: x + 0.42, y: y + 1.04, w: 3.4, h: 0, line: { color: G200, width: 0.75 }, objectName: "cap rule " + i });
    });
    foot(s, src || "주: 직접 만든 웹앱 프로토타입 화면 (매장·가격·수치는 시연용 예시) · 3D 아이콘 Microsoft Fluent Emoji (MIT)");
    return s;
  }

  // ================= 1. 표지 =================
  pres.addSection({ title: "표지" });
  { const s = pres.addSlide({ masterName: "COVER", sectionTitle: "표지" });
    tx(s, "NAMULLO", { x: 0.6, y: 0.55, w: 3, h: 0.3, fontSize: 11, bold: true, color: "C7D6CC", charSpacing: 4, objectName: "wordmark" });
    tx(s, "2026 창업 아이템 사업계획 발표", { x: 0.6, y: 1.6, w: 5.5, h: 0.35, fontSize: 13, color: "A9C2B3", objectName: "kicker" });
    s.addText("나물로(Namullo) 사업계획", { placeholder: "title" });
    s.addText("AI 나물 큐레이션 × 동네 상권 연결 플랫폼", { placeholder: "body" });
    tx(s, "나물로는 AI가 우리 동네 가게의 오늘 나물을\n레시피와 함께 연결하는 플랫폼입니다.", { x: 0.6, y: 3.55, w: 5.8, h: 0.6, fontSize: 12, color: "C7D6CC", objectName: "one-liner" });
    tx(s, "2026. 11.      발표자  ○○○", { x: 0.6, y: 4.8, w: 5, h: 0.3, fontSize: 11, color: "A9C2B3", objectName: "presenter" });
    phone(s, "cover_home", 7.05, 0.38, 4.85, "cover phone");
    s.addNotes(note(1)); }

  // ================= 2. 목차 =================
  pres.addSection({ title: "목차·요약" });
  { const s = pres.addSlide({ masterName: "PLAIN", sectionTitle: "목차·요약" });
    s.addText("목차", { placeholder: "title" });
    tx(s, "Contents", { x: 0.6, y: 1.55, w: 2.4, h: 0.3, fontSize: 12, color: G500, objectName: "contents en" });
    [["Ⅰ", "추진 배경", "나물 산업의 이해 · 소비자와 공급자의 문제 · 시장 공백 · Why now", "4"],
     ["Ⅱ", "사업 개요", "서비스 구조 · AI 엔진 4종 · 앱 화면 · 서비스 시연", "9"],
     ["Ⅲ", "사업성", "목표 시장 · 경쟁 비교 · 국내외 벤치마킹 · 수익 구조와 AI 비용", "15"],
     ["Ⅳ", "추진 계획", "AI 구현 계획 · 로드맵과 자금 · 재무 목표 · 리스크 · 팀", "19"]].forEach(([r, h, d, p], i) => {
      const y = 0.95 + i * 0.95;
      tx(s, r, { x: 3.6, y, w: 0.6, h: 0.5, fontSize: 22, bold: true, color: C.accent1, valign: "middle", objectName: "toc num " + r });
      tx(s, h, { x: 4.3, y, w: 4.0, h: 0.4, fontSize: 16, bold: true, color: C.text1, valign: "middle", objectName: "toc head " + h });
      tx(s, d, { x: 4.3, y: y + 0.42, w: 4.6, h: 0.3, fontSize: 11, color: G700, objectName: "toc desc " + h });
      tx(s, "p." + p, { x: 8.6, y, w: 0.9, h: 0.4, fontSize: 11, color: G500, align: "right", valign: "middle", objectName: "toc page " + h });
      s.addShape(pres.ShapeType.line, { x: 3.6, y: y + 0.85, w: 5.9, h: 0, line: { color: G200, width: 0.75 }, objectName: "toc rule " + i });
    });
    s.addNotes(note(2)); }

  // ================= 3. 요약 =================
  { const s = content(3, "목차·요약");
    head(s, "요약", "사업 요약", "나물 소비 장벽과 동네 판매처의 온라인 공백을 ‘콘텐츠 + AI → 동네 매장 주문’ 구조로 연결하는 사업임");
    table(s, ["구분", "핵심 내용", "주요 근거 · 목표"], [
      ["Ⅰ. 추진 배경", "소비자: 정보·조리·구매 장벽 / 공급자: 판로 위축·원산지 신뢰·가격 변동\n상인용 온라인·AI 도구 부재", "1인 가구 36.1% · 산나물 생산액 −9.3%\n시금치 한 달 +68% (2026.8)"],
      ["Ⅱ. 사업 개요", "도감 · 레시피 · 동네 매장 주문 · 꾸러미 + AI 엔진 4종\n(AI 셰프 · 레시피 구조화 · AI 상인 비서 · 수요 예측)", "반경 3km 매장 연결\nAI 셰프·상인 비서는 프로토타입에서 동작"],
      ["Ⅲ. 사업성", "SAM 약 1.7조 원 · 경쟁 대비 6개 요소 모두 보유\n구독·B2G·제휴·상인 Pro 중심 수익 (수수료 4%)", "3년차 GMV 54억 원 · 매출 8억 원\nAI 운영비 매출의 약 1%"],
      ["Ⅳ. 추진 계획", "시장 1곳 파일럿(300만 원) → 예비창업패키지 → 수도권 → 전국 · 산지", "파일럿 KPI: 주문 100건 · 재구매 30%"],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [1.35, 4.95, 2.8], rowH: [0.34, 0.72, 0.72, 0.72, 0.6], align: ["center", "left", "left"], size: 10.5 });
    foot(s, "주: SAM·GMV·매출·AI 운영비는 가정 기반 추정치 (산출 근거 p.15, p.18)"); }

  // ================= 4. Ⅰ-1 나물 산업의 이해 =================
  pres.addSection({ title: "Ⅰ. 추진 배경" });
  { const s = content(4, "Ⅰ. 추진 배경");
    head(s, "Ⅰ. 추진 배경", "나물 산업의 이해", "나물은 나는 곳·먹는 법마다 다루는 법이 다르고 안전·원산지·가격 이슈가 커, 정보와 수요 관리가 경쟁력임");
    { const K = (t) => ({ t, o: { align: "center", bold: true, fill: { color: G100 }, rowspan: 3 } }), C2 = (t) => ({ t, o: { align: "center", bold: true } }), L = (t, extra = {}) => ({ t, o: { align: "left", ...extra } });
      table(s, ["기준", "분류", "대표 나물"], [
        [K("나는 곳"), C2("산나물"), L("취나물 · 곰취 · 두릅 · 고사리 · 곤드레 · 산마늘")],
        [C2("들나물"), L("냉이 · 달래 · 씀바귀 · 돌나물 · 쑥")],
        [C2("재배나물"), L("시금치 · 콩나물 · 참나물 · 배추 · 가지")],
        [K("먹는 법"), C2("생채"), L("달래 · 씀바귀 · 돌나물 · 참나물 · 더덕")],
        [C2("숙채"), L("냉이 · 고사리 · 두릅 · 다래순 · 원추리\n독성분 있는 나물은 반드시 데침", { color: ACC, bold: true })],
        [C2("묵나물"), L("고사리 · 취나물 · 고비 · 시래기 (데쳐 말림, 겨울~초봄)")],
      ], { x: 0.45, y: 1.68, w: 4.75, colW: [0.8, 0.85, 3.1], rowH: [0.32, 0.43, 0.43, 0.43, 0.43, 0.5, 0.43], firstCol: false, size: 9.5 }); }
    const issues = [["안전", "원추리↔여로, 곰취↔동의나물, 산마늘↔박새 혼동. 독초 섭취 위해 41건 중 80%가 3~6월"], ["원산지", "2023년 중국산 고사리 56톤이 국산과 섞여 학교 급식에 납품, 적발"], ["가격", "2026년 8월 시금치 소비자물가 한 달 +68.2% (폭염)"]];
    issues.forEach(([h, d], i) => { const y = 1.68 + i * 1.1;
      s.addShape(pres.ShapeType.rect, { x: 5.38, y, w: 2.45, h: 1.0, fill: { color: i === 0 ? "FBEFE3" : G100 }, line: { color: i === 0 ? "FBEFE3" : G100, width: 0 }, objectName: "issue box " + h });
      tx(s, h, { x: 5.52, y: y + 0.08, w: 2.2, h: 0.26, fontSize: 11.5, bold: true, color: i === 0 ? ACC : BRAND, objectName: "issue head " + h });
      tx(s, d, { x: 5.52, y: y + 0.36, w: 2.2, h: 0.6, fontSize: 9.5, color: INK, objectName: "issue desc " + h }); });
    phone(s, "d1_guide_gosari_clean", 8.0, 1.66, 3.3, "in-app safety screen");
    foot(s, "자료: 식약처 안내 보도, 한국소비자원 위해감시(쿠키뉴스 2025.04), 경북매일(2023.05), 국가데이터처·KAMIS(2026.08 보도), 나물 분류 문헌 종합 / 오른쪽: 앱 도감의 안전 정보", 0.45, 7.35); }

  // ================= 5. Ⅰ-2 소비자 =================
  { const s = content(5, "Ⅰ. 추진 배경");
    head(s, "Ⅰ. 추진 배경", "소비자 측면의 나물 소비 장벽", "1인 가구·2030 세대는 늘었으나, 정보·조리·구매 장벽으로 나물의 소량·간편 소비 채널이 부재함");
    table(s, ["구분", "현상", "필요 기능"], [
      ["정보 장벽", "나물 이름·제철·맛·안전하게 먹는 법을 모름", "나물 도감, AI 셰프"],
      ["조리 장벽", "다듬기·데치기·간 맞추기 등 공정이 많고 실패 부담이 큼", "단계별 영상 레시피\n손질·데침 옵션"],
      ["구매 장벽", "온라인몰은 한 단·택배 단위, 시장은 재고 확인이 불가함", "동네 매장 소량 주문\n예약 픽업"],
      [{ t: "(추가) 가족", o: { color: G700 } }, "아이가 먹는 나물·조리법 정보가 흩어져 있음", "아이 선호도 지수\n혼합 요리 추천"],
    ], { x: 0.45, y: 1.68, w: 5.6, colW: [1.1, 2.75, 1.75], rowH: [0.34, 0.7, 0.7, 0.7, 0.7], align: ["center", "left", "left"] });
    tx(s, "1인 가구 비중 (2024)", { x: 6.35, y: 1.68, w: 3.2, h: 0.26, fontSize: 10.5, color: G700, objectName: "kpi label" });
    tx(s, "36.1%", { x: 6.35, y: 1.93, w: 1.6, h: 0.55, fontSize: 30, bold: true, color: C.accent1, objectName: "kpi value" });
    tx(s, "804만 가구·2019년 30% 돌파 후 지속 증가", { x: 6.35, y: 2.48, w: 3.2, h: 0.24, fontSize: 9.5, color: G500, objectName: "kpi sub" });
    s.addChart(pres.ChartType.bar, [{ name: "식생활평가지수", labels: ["성인 평균", "30대", "20대"], values: [58.6, 52.8, 50.3] }], { ...chartBase(), x: 6.2, y: 2.78, w: 3.4, h: 2.15, barDir: "bar", barGapWidthPct: 55, chartColors: [G300, BRAND2, BRAND], title: "식생활평가지수 (100점 만점)", valAxisMinVal: 0, valAxisMaxVal: 70, dataLabelPosition: "outEnd", objectName: "diet score chart" });
    foot(s, "자료: 국가데이터처 「2025 통계로 보는 1인 가구」(2025.12), 질병관리청 국민건강영양조사 2022–2024 식생활평가지수(2026.08 보도)"); }

  // ================= 6. Ⅰ-3 공급자 =================
  { const s = content(6, "Ⅰ. 추진 배경");
    head(s, "Ⅰ. 추진 배경", "공급자 측면의 판로 위축", "산나물 생산·판로는 위축되는 반면, 전통시장·로컬푸드는 규모 대비 온라인 주문 채널이 부족함");
    const num = (t, color = BRAND) => ({ t, o: { bold: true, color, fontSize: 12, align: "center" } });
    table(s, ["구분", "지표", "수치", "시사점"], [
      ["생산", "산나물 생산액 증감 (2024, 전년 대비)", num("−9.3%", ACC), "소비 위축이 생산 감소로 연결"],
      ["유통", "제철 집중에 따른 미판매·폐기 (업계 사례)", num("연 40톤", ACC), "수요 분산·묵나물 가공 필요"],
      ["판매처", "전국 전통시장 수 / 추정 연매출 (2023)", num("1,393개\n28.7조 원"), "대규모 오프라인 판매처 존재"],
      ["판매처", "로컬푸드 직매장 수 (2020)", num("554개"), "산지 직거래 인프라 확대"],
    ], { x: 0.45, y: 1.68, w: 6.0, colW: [0.8, 2.3, 1.15, 1.75], rowH: [0.34, 0.7, 0.7, 0.7, 0.7], align: ["center", "left", "center", "left"] });
    s.addChart(pres.ChartType.bar, [{ name: "직매장 수", labels: ["2013", "2020"], values: [32, 554] }], { ...chartBase(), x: 6.7, y: 1.68, w: 2.85, h: 2.55, barDir: "col", barGapWidthPct: 70, chartColors: [BRAND], title: "로컬푸드 직매장 수 (개)", valAxisMinVal: 0, valAxisMaxVal: 650, dataLabelPosition: "outEnd", objectName: "local food chart" });
    tx(s, "7년간 약 17배 증가\n판매처는 늘었으나 온라인 주문 연결은 제한적", { x: 6.75, y: 4.3, w: 2.8, h: 0.6, fontSize: 9.5, color: G700, objectName: "chart note" });
    foot(s, "자료: 산림청 「2024년 임산물생산조사」(2025.10), 유니콘팩토리(2024.11), 소상공인시장진흥공단 전통시장 실태조사(2023 기준), 농림축산식품부(2021.06 보도)"); }

  // ================= 7. Ⅰ-4 공백 =================
  { const s = content(7, "Ⅰ. 추진 배경");
    head(s, "Ⅰ. 추진 배경", "기존 서비스의 공백", "기존 서비스는 콘텐츠 또는 구매 한쪽에 머물고 상인용 AI 도구도 없어, 수요를 만들어 동네 매장으로 잇는 서비스가 없음");
    const px = 0.95, py = 1.75, pw = 4.3, ph = 2.85;
    s.addShape(pres.ShapeType.rect, { x: px, y: py + ph / 2, w: pw / 2, h: ph / 2, fill: { color: BRANDL }, line: { color: BRANDL, width: 0 }, objectName: "target quadrant" });
    s.addShape(pres.ShapeType.rect, { x: px, y: py, w: pw, h: ph, fill: { type: "none" }, line: { color: G300, width: 0.75 }, objectName: "plot frame" });
    s.addShape(pres.ShapeType.line, { x: px + pw / 2, y: py, w: 0, h: ph, line: { color: G200, width: 0.75 }, objectName: "divider v" });
    s.addShape(pres.ShapeType.line, { x: px, y: py + ph / 2, w: pw, h: 0, line: { color: G200, width: 0.75 }, objectName: "divider h" });
    tx(s, "콘텐츠 중심", { x: px, y: py + ph + 0.06, w: 1.6, h: 0.25, fontSize: 9.5, color: G700, objectName: "x axis left" });
    tx(s, "구매 중심", { x: px + pw - 1.6, y: py + ph + 0.06, w: 1.6, h: 0.25, fontSize: 9.5, color: G700, align: "right", objectName: "x axis right" });
    tx(s, "전국\n배송", { x: 0.45, y: py, w: 0.42, h: 0.45, fontSize: 9.5, color: G700, align: "right", objectName: "y axis top" });
    tx(s, "동네\n상권", { x: 0.45, y: py + ph - 0.45, w: 0.42, h: 0.45, fontSize: 9.5, color: G700, align: "right", objectName: "y axis bottom" });
    const dot = (label, cx, cy, hl = false) => { const d = hl ? 0.2 : 0.13;
      s.addShape(pres.ShapeType.ellipse, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color: hl ? ACC : G500 }, line: { color: hl ? ACC : G500, width: 0 }, objectName: "dot " + label });
      tx(s, label, { x: cx + d / 2 + 0.06, y: cy - 0.15, w: 1.9, h: 0.3, fontSize: hl ? 11 : 9.5, bold: hl, color: hl ? ACC : INK, valign: "middle", objectName: "dot label " + label }); };
    dot("레시피 앱·유튜브", px + 0.35, py + 0.6); dot("쿠팡·컬리", px + 3.15, py + 0.45); dot("어글리어스", px + 2.55, py + 1.05);
    dot("배민·네이버 시장 장보기", px + 2.45, py + 2.05); dot("당근", px + 2.3, py + 2.6); dot("나물로 (+ 상인 AI)", px + 0.55, py + 2.3, true);
    tx(s, [{ text: "공백 영역", options: { bold: true, breakLine: true } }, { text: "수요 창출 → 동네 매장 구매" }], { x: px + 0.12, y: py + ph / 2 + 0.1, w: 2.0, h: 0.45, fontSize: 9, color: BRAND, objectName: "gap caption" });
    table(s, ["유형", "대표 서비스", "한계"], [
      ["전국 온라인몰", "쿠팡·컬리", "한 단·택배 단위, 지역 상권과 무관"],
      ["시장 장보기", "배민·네이버", "구매 대행 중심, ‘왜·어떻게 먹는지’ 없음, 상인용 AI 도구 없음"],
      ["레시피 콘텐츠", "만개의레시피·유튜브", "시청에서 끝나고 구매로 이어지지 않음"],
      ["채소 구독", "어글리어스", "전국 택배, 동네 매장·소량 손질 불가"],
    ], { x: 5.65, y: 1.68, w: 3.9, colW: [1.05, 1.1, 1.75], rowH: [0.34, 0.72, 0.8, 0.72, 0.72], align: ["center", "left", "left"], size: 10 });
    foot(s, "자료: 각 사 서비스 소개 및 언론 보도 종합 (2026.10 기준) / 주: 포지셔닝은 자체 판단"); }

  // ================= 8. Ⅰ-5 Why now =================
  { const s = content(8, "Ⅰ. 추진 배경");
    head(s, "Ⅰ. 추진 배경", "왜 지금인가 (Why now)", "AI 비용이 메시지 1건에 수 원 수준으로 내려왔고 시장 디지털화가 검증된 지금, 동네 상인용 AI 도구의 공백을 채울 시점임");
    const cols = [["AI 비용 하락", "약 6원", "상인 메시지 1건 → 재고 데이터\n(Claude Opus 5.5 기준, 경량 모델은 1원 미만)"], ["수요 구조 변화", "36.1%", "1인 가구 비중 (2024)\n온라인 식품 거래 40조 원 돌파"], ["시장 디지털화 검증", "+196%", "배민 입점 전통시장 점포\n1년 매출 증가 (2026.3 보도)"], ["대형 플랫폼의 AI 전환", "컬리·오아시스", "AI 인수 · AI 쇼핑 비서\n동네 상인에겐 아직 없음"]];
    cols.forEach(([h, v, d], i) => { const x = 0.45 + i * 2.3;
      s.addShape(pres.ShapeType.rect, { x, y: 1.75, w: 2.15, h: 2.55, fill: { color: i === 0 ? BRANDL : G100 }, line: { color: i === 0 ? BRANDL : G100, width: 0 }, objectName: "why box " + i });
      tx(s, String(i + 1).padStart(2, "0"), { x: x + 0.18, y: 1.88, w: 0.6, h: 0.3, fontSize: 11, bold: true, color: G500, objectName: "why num " + i });
      tx(s, h, { x: x + 0.18, y: 2.18, w: 1.85, h: 0.32, fontSize: 12.5, bold: true, color: INK, objectName: "why head " + i });
      tx(s, v, { x: x + 0.18, y: 2.58, w: 1.9, h: 0.6, fontSize: v.length > 5 ? 20 : 28, bold: true, color: i === 0 ? ACC : BRAND, valign: "middle", objectName: "why value " + i });
      tx(s, d, { x: x + 0.18, y: 3.3, w: 1.9, h: 0.85, fontSize: 9.5, color: G700, objectName: "why desc " + i }); });
    s.addShape(pres.ShapeType.rect, { x: 0.45, y: 4.45, w: 9.1, h: 0.48, fill: { color: BRAND }, line: { color: BRAND, width: 0 }, objectName: "why band" });
    tx(s, "소규모 팀도 AI로 상인용 도구를 만들고 운영할 수 있는 비용 구조가 처음 갖춰졌다", { x: 0.65, y: 4.45, w: 8.7, h: 0.48, fontSize: 12, bold: true, color: "FFFFFF", valign: "middle", objectName: "why band text" });
    foot(s, "자료: Anthropic 가격표(2026.10, 1달러=1,400원 가정, p.18), 국가데이터처(2025.12), 머니투데이(2026.03), 뉴데일리(2025.07)·뉴스웨이(2026.06) 보도"); }

  // ================= 9. Ⅱ-1 서비스 구조 =================
  pres.addSection({ title: "Ⅱ. 사업 개요" });
  { const s = content(9, "Ⅱ. 사업 개요");
    head(s, "Ⅱ. 사업 개요", "서비스 구조", "정보 탐색부터 동네 매장 구매까지 3단계를 하나의 흐름으로 잇고, 단계마다 AI가 붙어 선택과 운영을 돕는 구조임");
    [["01  알고", "나물 도감"], ["02  고르고", "레시피 허브"], ["03  산다", "동네 매장 주문"]].forEach(([a, b], i) => { const x = 1.75 + i * 2.6;
      s.addShape(pres.ShapeType.homePlate, { x, y: 1.68, w: 2.55, h: 0.5, fill: { color: i === 2 ? BRAND : BRAND2 }, line: { color: i === 2 ? BRAND : BRAND2, width: 0 }, objectName: "step " + a });
      tx(s, [{ text: a + "  ", options: { bold: true } }, { text: "· " + b }], { x: x + 0.15, y: 1.68, w: 2.2, h: 0.5, fontSize: 12, color: "FFFFFF", valign: "middle", objectName: "step text " + a }); });
    const ai = (t) => ({ t, o: { bold: true, color: BRAND, fill: { color: BRANDL } } });
    table(s, null, [
      ["제공 기능", "나물 60여 종 분류·제철·데침 시간\n‘꼭 데쳐 먹는 나물’ 안전 표시\n아이 선호도 지수", "나물별 영상 레시피 큐레이션\n다듬기 → 데치기 → 무치기 구간 이동\n영상 아래 ‘재료 담기’", "반경 3km 시장·직매장·반찬가게\n생나물 / 손질 / 데침 옵션\n예약 픽업 · 근거리 배달"],
      [{ t: "AI 엔진", o: { color: BRAND, fill: { color: BRANDL } } }, ai("AI 셰프 (질문·사진 → 추천)"), ai("레시피 자동 구조화"), ai("AI 상인 비서 · 수요 예측")],
      ["해결 과제", { t: "정보 장벽", o: { bold: true, color: BRAND, align: "center" } }, { t: "조리 장벽", o: { bold: true, color: BRAND, align: "center" } }, { t: "구매 장벽", o: { bold: true, color: BRAND, align: "center" } }],
    ], { x: 0.45, y: 2.28, w: 9.1, colW: [1.3, 2.6, 2.6, 2.6], rowH: [1.0, 0.42, 0.42], align: ["center", "left", "left", "left"], size: 10.5 });
    s.addShape(pres.ShapeType.rect, { x: 0.45, y: 4.38, w: 9.1, h: 0.55, fill: { color: G100 }, line: { color: G100, width: 0 }, objectName: "subscription band" });
    tx(s, [{ text: "＋ 제철 나물 꾸러미 구독", options: { bold: true, color: BRAND } }, { text: "     주 1회 제철 3종 + 양념 + 레시피 카드 · 대보름 9나물 · 봄 산나물 한정판  →  재구매 고정", options: { color: INK } }], { x: 0.65, y: 4.38, w: 8.8, h: 0.55, fontSize: 10.5, valign: "middle", objectName: "subscription text" });
    foot(s, "주: 나물 분류·안전 표시는 식약처 안내와 나물 문헌 기반 (부록 · 도메인 리서치 문서)"); }

  // ================= 10. Ⅱ-2 AI 엔진 =================
  { const s = content(10, "Ⅱ. 사업 개요");
    head(s, "Ⅱ. 사업 개요", "AI 엔진 4종", "AI 엔진 4종이 소비자의 선택과 상인의 운영을 동시에 돕고, 거래 데이터가 쌓일수록 정확해지는 구조임");
    const side = (x, title, lines, name) => { s.addShape(pres.ShapeType.rect, { x, y: 1.75, w: 1.6, h: 2.5, fill: { color: G100 }, line: { color: G200, width: 0.75 }, objectName: name });
      tx(s, title, { x: x + 0.12, y: 1.85, w: 1.4, h: 0.3, fontSize: 12, bold: true, color: INK, align: "center", objectName: name + " title" });
      tx(s, lines.map((l, i) => ({ text: l, options: { breakLine: i < lines.length - 1 } })), { x: x + 0.12, y: 2.25, w: 1.4, h: 1.9, fontSize: 9.5, color: G700, align: "center", paraSpaceAfter: 6, objectName: name + " lines" }); };
    side(0.45, "소비자", ["질문 한 줄", "냉장고 사진", "주문 · 픽업", "‘우리 아이\n먹었어요’"], "consumer box");
    side(7.95, "동네 매장 · 상인", ["카톡 한 줄 재고", "주문 접수", "입고량 결정", "마감 할인"], "merchant box");
    const eng = [["① AI 셰프", "소비자", "질문·사진 → 오늘 동네 재고로 반찬 추천 · 레시피 · 담기"], ["② 레시피 자동 구조화", "콘텐츠", "크리에이터 영상 설명·챕터 → 재료·단계·시간 데이터"], ["③ AI 상인 비서", "상인", "말하듯 쓴 한 줄·음성 → 재고·가격·손질 등록, 홍보글"], ["④ 수요 예측 · 마감 할인", "운영", "판매 이력·요일·날씨 → 내일 입고량, 잔여 재고 할인 제안"]];
    eng.forEach(([t, who, d], i) => { const x = 2.3 + (i % 2) * 2.75, y = 1.75 + Math.floor(i / 2) * 1.3;
      s.addShape(pres.ShapeType.rect, { x, y, w: 2.6, h: 1.18, fill: { color: "FFFFFF" }, line: { color: BRAND2, width: 1 }, objectName: "engine " + i });
      tx(s, t, { x: x + 0.12, y: y + 0.1, w: 1.9, h: 0.3, fontSize: 11.5, bold: true, color: BRAND, objectName: "engine title " + i });
      tx(s, who, { x: x + 1.85, y: y + 0.12, w: 0.65, h: 0.24, fontSize: 9, bold: true, color: G500, align: "right", objectName: "engine who " + i });
      tx(s, d, { x: x + 0.12, y: y + 0.45, w: 2.38, h: 0.65, fontSize: 9.5, color: INK, objectName: "engine desc " + i }); });
    const arrow = (x, y, w, name, rev = false) => s.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color: G500, width: 1.25, endArrowType: rev ? undefined : "triangle", beginArrowType: rev ? "triangle" : undefined }, objectName: name });
    arrow(2.07, 2.34, 0.2, "arrow consumer to chef");
    arrow(7.67, 2.34, 0.26, "arrow merchant to assistant", true);
    arrow(7.67, 3.64, 0.26, "arrow forecast to merchant");
    s.addShape(pres.ShapeType.rect, { x: 2.3, y: 4.38, w: 5.35, h: 0.55, fill: { color: BRAND }, line: { color: BRAND, width: 0 }, objectName: "flywheel band" });
    tx(s, "데이터 플라이휠   주문·재고·피드백 → 정확도 ↑ → 폐기·품절 ↓ → 참여 ↑", { x: 2.45, y: 4.38, w: 5.1, h: 0.55, fontSize: 10, bold: true, color: "FFFFFF", valign: "middle", objectName: "flywheel text" });
    foot(s, "주: ①·③은 프로토타입에서 Claude로 실제 동작, ②·④는 0~1단계에 구현 / AI는 야생 채취 식물의 식용 여부를 판단하지 않음"); }

  // ================= 11~13. 앱 화면 =================
  screenSlide(11, "Ⅱ. 사업 개요", "Ⅱ. 사업 개요", "앱 화면 ① 알고 · 고르고", "질문 한 줄로 오늘 동네 재고에 맞는 반찬을 고르고, 레시피 장면을 보며 필요한 재료만 바로 담음",
    ["a1_home", "a2_aichef", "a3_recipe"],
    [["홈 · AI 셰프 진입", "이달의 제철 · 아이 선호 TOP3, 질문 한 줄로 AI 셰프 시작", "웹앱 + 매장 재고 데이터"],
     ["AI 셰프 추천", "오늘 동네 재고 안에서 반찬 2~3개, 아이 가구는 혼합 요리를 먼저", "Claude (텍스트 · 사진 입력)"],
     ["레시피 · 재료 담기", "영상 구간으로 이동, 집에 있는 재료는 체크하고 필요한 것만 담기", "영상 공식 임베드 + AI 구조화"]]);
  screenSlide(12, "Ⅱ. 사업 개요", "Ⅱ. 사업 개요", "앱 화면 ② 동네에서 산다", "반경 3km 매장의 오늘 재고와 가격을 비교하고, 손질 옵션과 픽업 시간을 골라 1분 안에 예약함",
    ["b1_stores", "b2_checkout", "b3_done"],
    [["동네 매장 지도", "시장 가게 · 직매장 · 반찬가게의 오늘 재고 · 가격 · 입고 시각", "지도 + 상인 재고 데이터"],
     ["손질 옵션 · 픽업 시간", "생나물 / 손질 +500원 / 데침 +800원, 마감된 시간은 자동 비활성", "매장별 옵션 · 픽업 슬롯"],
     ["예약 완료", "픽업 번호 · QR, 다음 날 ‘우리 아이 먹었어요’ 피드백 요청", "PG 결제 + 알림톡"]]);
  screenSlide(13, "Ⅱ. 사업 개요", "Ⅱ. 사업 개요", "앱 화면 ③ AI 상인 비서 · 안전 정보", "사장님은 카톡 한 줄로 재고를 올리고 입고 추천·마감 할인을 받으며, 소비자는 안전하게 먹는 법을 함께 봄",
    ["c1_merchant_stock", "c2_merchant_discount", "d1_guide_gosari"],
    [["AI 재고 등록", "말하듯 쓴 한 줄 → 품목 · 수량 · 가격 · 손질 정리, 사장님 확인 후 게시", "Claude 정보 추출 + 확인 단계"],
     ["입고 추천 · 마감 할인", "판매 이력 · 요일 · 날씨로 내일 입고량, 19시 이후 잔여 재고 할인 제안", "시계열 예측 → 머신러닝"],
     ["도감 안전 정보", "꼭 데쳐 먹는 나물 · 원산지 확인 안내, 야생 채취 식물 판별은 하지 않음", "식약처 안내 기반 도감 데이터"]]);

  // ================= 14. 시연 =================
  { const s = pres.addSlide({ masterName: "DEMO", sectionTitle: "Ⅱ. 사업 개요" }); s.addNotes(note(14));
    head(s, "Ⅱ. 사업 개요", "서비스 시연", null);
    tx(s, "맞벌이 부모의 평일 저녁 — 실제 웹앱 화면 녹화", { x: 0.45, y: 1.0, w: 6.0, h: 0.32, fontSize: 12.5, bold: true, color: G700, objectName: "demo sub" });
    const steps = [["17:00", "AI 셰프에게 질문", "‘다섯 살 아이랑 먹을 순한 반찬’"], ["17:01", "추천 3가지", "오늘 동네 재고 기반 · 아이 선호도 표시"], ["17:02", "레시피 · 재료 담기", "데치기 구간으로 이동 → 참나물 담기"], ["17:02", "동네 매장 선택", "600m 초록나물상회 · 오늘 09:12 입고"], ["17:03", "손질 · 18:00 픽업 예약", "4,000원 · 픽업 번호 N-2381"], ["17:03", "사장님 대화방에 주문 도착", "한 번에 접수 · 17:40까지 손질"]];
    s.addShape(pres.ShapeType.line, { x: 0.83, y: 1.55, w: 0, h: 2.6, line: { color: G200, width: 1.5 }, objectName: "timeline" });
    steps.forEach(([t, h, d], i) => { const y = 1.42 + i * 0.52;
      s.addShape(pres.ShapeType.roundRect, { x: 0.45, y: y + 0.04, w: 0.76, h: 0.3, rectRadius: 0.15, fill: { color: i === 5 ? MARK : BRAND }, line: { color: i === 5 ? MARK : BRAND, width: 0 }, objectName: "time pill " + i });
      tx(s, t, { x: 0.45, y: y + 0.04, w: 0.76, h: 0.3, fontSize: 9.5, bold: true, color: "FFFFFF", align: "center", valign: "middle", objectName: "time text " + i });
      tx(s, h, { x: 1.38, y: y, w: 4.9, h: 0.26, fontSize: 12, bold: true, color: INK, objectName: "demo step " + i });
      tx(s, d, { x: 1.38, y: y + 0.26, w: 4.9, h: 0.24, fontSize: 10, color: G700, objectName: "demo detail " + i }); });
    s.addShape(pres.ShapeType.rect, { x: 0.45, y: 4.58, w: 5.95, h: 0.42, fill: { color: G100 }, line: { color: G100, width: 0 }, objectName: "demo note band" });
    tx(s, [{ text: "결과  ", options: { bold: true, color: BRAND } }, { text: "메뉴 결정부터 예약까지 약 1분 · 매장은 주문 수신과 손질만으로 추가 매출" }], { x: 0.6, y: 4.58, w: 5.7, h: 0.42, fontSize: 10.5, color: INK, valign: "middle", objectName: "demo result" });
    const vh = 4.78, vw = vh * 414 / 868, vx = 6.95, vy = 0.36;
    s.addMedia({ type: "video", path: REC + "demo_phone.mp4", x: vx, y: vy, w: vw, h: vh, cover: b64(REC + "demo_poster.png"), objectName: "demo video" });
    tx(s, "영상: 슬라이드 쇼에서 재생 · AI 응답은 시연용 예시", { x: vx - 0.4, y: 5.18, w: vw + 0.8, h: 0.25, fontSize: 8.5, color: G500, align: "center", objectName: "demo caption" });
    fs.writeFileSync(__dirname + "/demo_rect.json", JSON.stringify({ x: vx, y: vy, w: vw, h: vh })); }

  // ================= 15. Ⅲ-1 시장 =================
  pres.addSection({ title: "Ⅲ. 사업성" });
  { const s = content(15, "Ⅲ. 사업성");
    head(s, "Ⅲ. 사업성", "목표 시장 규모", "먹거리 거래 시장 68.7조 원 중 수도권 채소·나물류 약 1.7조 원을 1차 목표 시장(SAM)으로 설정함");
    [["TAM", "68.7조 원", 3.4, G200, INK], ["SAM", "약 1.7조 원", 2.6, BRAND2, "FFFFFF"], ["SOM (3년차)", "54억 원", 1.8, BRAND, "FFFFFF"]].forEach(([k, v, w, fill, col], i) => { const y = 1.72 + i * 0.88, cx = 2.2;
      s.addShape(pres.ShapeType.trapezoid, { x: cx - w / 2, y, w, h: 0.8, flipV: true, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: "funnel " + k });
      tx(s, [{ text: k, options: { fontSize: 10.5, breakLine: true } }, { text: v, options: { fontSize: 15, bold: true } }], { x: cx - w / 2, y, w, h: 0.8, color: col, align: "center", valign: "middle", objectName: "funnel text " + k }); });
    table(s, ["구분", "정의", "규모", "산출 근거"], [
      ["TAM", "국내 먹거리 거래 시장\n(온라인 식품 + 전통시장)", { t: "68.7조 원", o: { bold: true, align: "center" } }, "온라인 식품 40조 원(2024) + 전통시장 28.7조 원(2023), 단순 합산"],
      ["SAM", "수도권 전통시장·로컬푸드의 채소·나물류", { t: "약 1.7조 원", o: { bold: true, align: "center", color: BRAND } }, "28.7조 원 × 수도권 40% × 채소·나물 15% (가정)"],
      ["SOM", "3년차 나물로 거래액 (GMV)", { t: "54억 원", o: { bold: true, align: "center", color: BRAND } }, "매장 300곳 × 월 100건 × 15,000원 × 12개월"],
    ], { x: 4.15, y: 1.68, w: 5.4, colW: [0.62, 1.5, 0.98, 2.3], rowH: [0.34, 0.78, 0.78, 0.78], align: ["center", "left", "center", "left"], size: 10 });
    tx(s, [{ text: "성장 요인   ", options: { bold: true, color: BRAND } }, { text: "①  1인 가구 증가 (36.1%)      ②  온라인 장보기 일상화      ③  지자체·정부의 전통시장 디지털 전환 정책" }], { x: 0.45, y: 4.42, w: 9.1, h: 0.42, fontSize: 10, color: INK, valign: "middle", fill: { color: G100 }, margin: [0, 0, 0, 0.15], objectName: "growth drivers" });
    foot(s, "자료: 통계청 온라인쇼핑동향 보도(2024), 소상공인시장진흥공단(2023 기준) / 주: SAM·SOM은 가정 기반 추정"); }

  // ================= 16. Ⅲ-2 경쟁 =================
  { const s = content(16, "Ⅲ. 사업성");
    head(s, "Ⅲ. 사업성", "경쟁 서비스 비교", "나물 특화·레시피 연동·동네 매장·손질 옵션·구독·상인 AI 도구 6개 요소를 모두 갖춘 서비스는 나물로가 유일함");
    const hb = (v) => ({ t: v, o: { align: "center", fontSize: 14, color: v === "●" ? BRAND : v === "◐" ? BRAND2 : G300 } });
    const rows = [["나물 특화 큐레이션 (제철·안전)", "○", "○", "◐", "○", "●"], ["레시피 → 즉시 구매 연결", "◐", "○", "◐", "○", "●"], ["동네 상권 (전통시장·로컬푸드) 연결", "○", "●", "○", "○", "●"], ["소량·손질·데침 옵션", "◐", "◐", "–", "◐", "●"], ["제철 꾸러미 구독", "◐", "○", "○", "●", "●"], ["상인용 AI 운영 도구 (재고·예측)", "◐", "○", "○", "○", "●"]].map((r) => [r[0], ...r.slice(1).map(hb)]);
    table(s, ["비교 항목", "쿠팡·컬리", "배민·네이버\n시장 장보기", "레시피 앱\n·유튜브", "어글리어스", "나물로"], rows, { x: 0.45, y: 1.68, w: 9.1, colW: [3.0, 1.15, 1.3, 1.2, 1.15, 1.3], rowH: [0.5, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35], align: ["left", "center", "center", "center", "center", "center"], hlCol: 5, size: 10.5, headFills: [BRAND, BRAND, BRAND, BRAND, BRAND, ACC] });
    tx(s, "●  충족     ◐  일부 충족     ○  미흡   (쿠팡·컬리의 ◐는 자체 물류용 예측)", { x: 3.55, y: 4.33, w: 6.0, h: 0.22, fontSize: 9, color: G500, align: "right", objectName: "legend" });
    [["데이터", "도감·아이 선호도·판매 데이터 누적"], ["관계", "상인의 카톡 등록 습관·손질 서비스"], ["공공 신뢰", "지자체 전통시장 디지털화 사업"]].forEach(([h, d], i) => { const x = 0.45 + i * 3.07;
      s.addShape(pres.ShapeType.rect, { x, y: 4.62, w: 2.96, h: 0.36, fill: { color: G100 }, line: { color: G100, width: 0 }, objectName: "moat " + h });
      tx(s, [{ text: h + "  ", options: { bold: true, color: BRAND } }, { text: d }], { x: x + 0.12, y: 4.62, w: 2.78, h: 0.36, fontSize: 9.5, color: INK, valign: "middle", objectName: "moat text " + h }); });
    foot(s, "주: 2026.10 기준 각 서비스 공개 정보에 근거한 자체 평가 · 아래 띠는 진입 장벽 요소"); }

  // ================= 17. Ⅲ-3 벤치마킹 =================
  { const s = content(17, "Ⅲ. 사업성");
    head(s, "Ⅲ. 사업성", "국내외 벤치마킹", "동네 시장 온라인화·채소 구독·AI 수요 예측·AI 레시피 쇼핑이 각각 검증되었으며, 나물로는 이를 나물 품목에서 통합함");
    table(s, ["구분", "서비스", "사업 모델", "핵심 성과 (보도 기준)", "나물로 적용"], [
      ["국내", "배민 전통시장 장보기", "전통시장 점포 입점, 2시간 배송, 수수료 0%", "입점 점포 매출 1년 +196%", "시장 상인 온라인 수요"],
      ["국내", "어글리어스", "못난이 농산물 정기배송", "누적 293만 kg 구출 · 투자 38억 원", "채소 구독 지불의사"],
      ["국내", "당근", "동네 기반 커뮤니티 · 로컬 광고", "MAU 2,000만+ · 비즈프로필 265만", "동네 단위 연결"],
      [{ t: "AI", o: { color: ACC } }, "Afresh (미국)", "신선식품 발주 AI", "폐기 최대 25% 감소 주장 · 2026.4 3,400만 달러 투자", "AI 입고 추천"],
      [{ t: "AI", o: { color: ACC } }, "컬리 ‘데멍이’", "데이터 기반 수요 예측", "신선식품 폐기율 1% 미만 주장", "예측 → 폐기 감소"],
      [{ t: "AI", o: { color: ACC } }, "Instacart Ask", "ChatGPT 기반 레시피·식단 검색", "레시피 질문 → 장보기 연결 (2023)", "AI 셰프"],
      ["유럽", "Too Good To Go", "매장 잉여 식품 할인 앱", "2025년 1.56억 끼 구출", "마감 할인"],
      ["일본", "타베쵸쿠", "생산자 직거래 마켓", "생산자 1.15만 명 · 이용자 130만 명", "3단계 산지 직거래"],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [0.55, 1.65, 2.4, 2.6, 1.9], rowH: [0.3, 0.36, 0.36, 0.36, 0.4, 0.36, 0.36, 0.36, 0.36], align: ["center", "left", "left", "left", "left"], size: 9.5, margin: [0.03, 0.07, 0.03, 0.07] });
    foot(s, "자료: 머니투데이(2026.03), 한국경제(2025.02), 당근 실적 보도, Afresh(2026.04), 뉴데일리(2025.07), Supermarket News(2023), TGTG·vivid garden(2026) / 회사 발표 수치 포함"); }

  // ================= 18. Ⅲ-4 수익 · AI 비용 =================
  { const s = content(18, "Ⅲ. 사업성");
    head(s, "Ⅲ. 사업성", "수익 구조 및 AI 비용", "구독·지자체 사업·제휴·상인 Pro가 주 수익원이며, AI 운영비는 주문당 약 24원으로 매출의 약 1% 수준임");
    s.addChart(pres.ChartType.bar, [{ name: "3년차 매출", labels: ["상인 Pro (AI 비서·노출)", "크리에이터·브랜드 제휴", "주문 중개 수수료 4%", "지자체·데이터 사업", "제철 꾸러미 구독"], values: [0.4, 1.2, 1.7, 1.9, 2.8] }],
      { ...chartBase(), x: 0.35, y: 1.68, w: 4.45, h: 3.0, barDir: "bar", barGapWidthPct: 45, chartColors: [ACC, BRAND3, G500, BRAND3, BRAND], title: "3년차 수익원별 매출 (억 원, 합계 8.0)", valAxisMinVal: 0, valAxisMaxVal: 3.5, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", objectName: "revenue mix chart" });
    tx(s, "상인 Pro 월 29,000원: 입고 추천 · 마감 할인 · 홍보글 · 상단 노출", { x: 0.45, y: 4.68, w: 4.35, h: 0.28, fontSize: 9.5, color: G700, objectName: "pro note" });
    tx(s, "AI 운영 비용 (3년차, Claude Opus 5.5 기준)", { x: 5.05, y: 1.68, w: 4.5, h: 0.28, fontSize: 10.5, bold: true, color: INK, objectName: "ai cost head" });
    table(s, ["작업", "1건", "월 건수", "월 비용"], [
      ["상인 메시지 → 재고", "약 6원", "27,000", "약 17만 원"],
      ["AI 셰프 (텍스트)", "약 23원", "16,000", "약 37만 원"],
      ["사진 인식", "약 25원", "3,000", "약 7.5만 원"],
      ["홍보글 · 예측 설명 · 레시피 정리", "8~39원", "11,700", "약 10.6만 원"],
      [{ t: "합계", o: { bold: true } }, "", "", { t: "약 72만 원", o: { bold: true, color: BRAND } }],
    ], { x: 5.05, y: 2.0, w: 4.5, colW: [1.95, 0.75, 0.85, 0.95], rowH: [0.3, 0.34, 0.34, 0.34, 0.4, 0.34], align: ["left", "right", "right", "right"], size: 9.5, headSize: 9.5 });
    s.addShape(pres.ShapeType.rect, { x: 5.05, y: 4.22, w: 4.5, h: 0.72, fill: { color: BRANDL }, line: { color: BRANDL, width: 0 }, objectName: "unit band" });
    tx(s, [{ text: "주문당 AI 비용 약 24원", options: { bold: true, color: BRAND, breakLine: true } }, { text: "주문당 공헌이익 약 600원 · 대량 작업에 경량 모델을 쓰면 월 약 20만 원", options: { color: INK } }], { x: 5.2, y: 4.22, w: 4.3, h: 0.72, fontSize: 10, valign: "middle", objectName: "unit text" });
    foot(s, "주: 가격 Opus 5.5 입력 $4 · 출력 $20 / Haiku 5.5 $0.10 · $0.50 (100만 토큰당), 배치 50% 할인, 1달러=1,400원, 토큰 수는 추정"); }

  // ================= 19. Ⅳ-1 AI 구현 계획 =================
  pres.addSection({ title: "Ⅳ. 추진 계획" });
  { const s = content(19, "Ⅳ. 추진 계획");
    head(s, "Ⅳ. 추진 계획", "AI 구현 계획", "AI는 지금 쓸 수 있는 도구로 사람 확인 단계를 둔 채 시작하고, 데이터가 쌓이는 만큼 자동화 범위를 넓힘");
    table(s, ["AI 엔진", "0단계 (지금 · 0~3개월)", "1단계 (4~12개월)", "2단계 (2년차~)"], [
      ["① AI 셰프", "프로토타입 링크로 고객 10명 인터뷰, 추천 품질 기록", "웹앱 정식 기능, 사진 입력", "가족 프로필 개인화"],
      ["② 레시피 구조화", "크리에이터 동의 영상 50편, AI 정리 + 사람 검수", "배치 처리로 200편", "크리에이터 셀프 등록"],
      ["③ AI 상인 비서", "운영자가 카톡 메시지를 AI로 정리 → 사장님 확인 → 시트", "카톡 채널 챗봇 자동화, 음성 메모", "상인 Pro 유료화"],
      ["④ 수요 예측", "주문·폐기 매일 기록, 요일·날씨 이동평균", "매장별 머신러닝 모델, 마감 할인 제안", "지역 수요 리포트 (B2G)"],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [1.5, 2.75, 2.55, 2.3], rowH: [0.34, 0.6, 0.6, 0.6, 0.6], align: ["left", "left", "left", "left"], size: 10, headFills: [BRAND, ACC, BRAND2, BRAND2] });
    s.addShape(pres.ShapeType.rect, { x: 0.45, y: 4.5, w: 9.1, h: 0.46, fill: { color: G100 }, line: { color: G100, width: 0 }, objectName: "ai principles band" });
    tx(s, [{ text: "AI 원칙  ", options: { bold: true, color: BRAND } }, { text: "사람 확인 후 게시 · 야생 식물 식용 판별 금지 · 효능 표현 금지 · 아이 정보 최소 수집 · 사진 비저장 · ‘AI 정리’ 표시" }], { x: 0.6, y: 4.5, w: 8.85, h: 0.46, fontSize: 10, color: INK, valign: "middle", objectName: "ai principles" });
    foot(s, "주: 도구 = Claude API, 구글시트, 파이썬(pandas·머신러닝), 카카오톡 채널 / 개발은 AI 코딩 도구 활용 (이번 프로토타입도 같은 방식으로 제작)"); }

  // ================= 20. Ⅳ-2 로드맵 · 자금 =================
  { const s = content(20, "Ⅳ. 추진 계획");
    head(s, "Ⅳ. 추진 계획", "단계별 로드맵 및 자금 계획", "시장 1곳 파일럿으로 수요를 검증한 뒤 지원사업·시드 투자로 확장하며, 예비창업패키지는 개발·마케팅 중심으로 집행함");
    const kpi = (t) => ({ t, o: { bold: true, color: BRAND, fill: { color: BRANDL } } });
    table(s, ["구분", "0단계 검증\n0–3개월", "1단계 MVP\n4–12개월", "2단계 확장\n2년차", "3단계 전국화\n3년차~"], [
      ["제휴 매장", "시장 1곳 · 점포 2~3곳", "30곳", "수도권 120곳", "전국 300곳 + 산지"],
      ["서비스", "수동 운영 + AI 도구, 도감 30종", "웹앱 · 챗봇 · 레시피 200편", "네이티브 앱 · 구독 3종", "제철 농산물 · 해외"],
      ["자금", "자기자본 300만 원", "예비창업패키지 · 농식품 벤처육성", "시드 3~5억 원", "시리즈 A 검토"],
      [{ t: "목표 KPI", o: { fill: { color: BRANDL }, color: BRAND } }, kpi("주문 100건 · 재구매 30%"), kpi("월 주문 2,000 · 구독 200"), kpi("월 주문 1만 · 구독 1,500"), kpi("GMV 54억 원 · 흑자")],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [1.3, 1.95, 1.95, 1.95, 1.95], rowH: [0.5, 0.36, 0.46, 0.46, 0.4], align: ["center", "left", "left", "left", "left"], size: 9.5, headFills: [BRAND, ACC, BRAND2, BRAND2, BRAND2] });
    s.addChart(pres.ChartType.bar, [
      { name: "개발 (웹앱·챗봇)", labels: ["7천만 원"], values: [40] }, { name: "마케팅·크리에이터", labels: ["7천만 원"], values: [25] }, { name: "파일럿 운영·포장재", labels: ["7천만 원"], values: [15] }, { name: "AI API·서버", labels: ["7천만 원"], values: [10] }, { name: "법무·인증·기타", labels: ["7천만 원"], values: [10] },
    ], { ...chartBase(), x: 0.35, y: 4.17, w: 9.3, h: 0.85, barDir: "bar", barGrouping: "percentStacked", chartColors: [BRAND, BRAND2, BRAND3, ACC, G300], showTitle: false, dataLabelPosition: "ctr", dataLabelFontSize: 9, dataLabelColor: "FFFFFF", dataLabelFormatCode: "0\"%\"", catAxisHidden: true, showLegend: true, legendPos: "r", legendFontSize: 8.5, legendFontFace: "+mn-lt", legendColor: G700, objectName: "funds chart" });
    tx(s, "예비창업패키지 7천만 원 사용 계획", { x: 0.45, y: 4.0, w: 4, h: 0.22, fontSize: 9.5, bold: true, color: INK, objectName: "funds title" });
    foot(s, "주: 지원사업 규모는 2026년 공고 기준 참고치, 2027년 공고 시 조건 재확인 / 사용 비율은 계획(가정)"); }

  // ================= 21. Ⅳ-3 재무 · 확장 =================
  { const s = content(21, "Ⅳ. 추진 계획");
    head(s, "Ⅳ. 추진 계획", "재무 목표 및 확장 전략", "3년차 GMV 54억 원·매출 8억 원·영업이익 1.5억 원 달성 후, 품목·산지·해외로 확장함");
    s.addChart(pres.ChartType.bar, [{ name: "거래액(GMV)", labels: ["1년차", "2년차", "3년차"], values: [2.5, 15, 54] }, { name: "매출", labels: ["1년차", "2년차", "3년차"], values: [0.6, 3, 8] }],
      { ...chartBase(), x: 0.35, y: 1.68, w: 4.6, h: 2.2, barDir: "col", barGrouping: "clustered", barGapWidthPct: 60, chartColors: [BRAND, BRAND3], title: "거래액(GMV) · 매출 목표 (억 원)", valAxisMinVal: 0, valAxisMaxVal: 62, dataLabelPosition: "outEnd", showLegend: true, legendPos: "r", legendFontSize: 9, legendFontFace: "+mn-lt", legendColor: G700, objectName: "financial chart" });
    const pl = (t, color) => ({ t, o: { align: "center", bold: true, color } });
    table(s, ["(억 원)", "1년차", "2년차", "3년차"], [["매출", pl("0.6", INK), pl("3.0", INK), pl("8.0", INK)], ["비용 (AI 포함)", pl("1.2", INK), pl("3.5", INK), pl("6.5", INK)], ["영업손익", pl("−0.6", ACC), pl("−0.5", ACC), pl("+1.5", BRAND)]],
      { x: 0.45, y: 3.95, w: 4.4, colW: [1.25, 1.05, 1.05, 1.05], rowH: [0.26, 0.24, 0.24, 0.24], align: ["center", "center", "center", "center"], size: 9.5, headSize: 9.5 });
    table(s, ["확장 방향", "내용"], [
      ["품목 확장", "나물 → 제철 농산물 전반으로 품목 확대\n(동네 큐레이션 커머스)"],
      ["산지 연결", "산채 농가 → 동네 매장 → 소비자 직거래\n고부가 품목(산마늘 · 곰취)부터"],
      ["해외 진출", "‘Namul’ 브랜드 건조 나물 밀키트 + 레시피\n(국내 산나물 업체 일본 · 미국 진출 사례)"],
      ["사회적 가치", "전통시장 젊은 고객 유입, 산나물 폐기 감소\n2030 · 아동 채소 섭취 개선"],
    ], { x: 5.2, y: 1.68, w: 4.35, colW: [1.1, 3.25], rowH: [0.32, 0.66, 0.66, 0.66, 0.66], align: ["center", "left"], size: 10 });
    foot(s, "주: 재무 수치는 가정 기반 목표치 / 자료: 순천대 산채 소득 연구, 유니콘팩토리(2024.11), 문체부 영문 기사 ‘namul nation’"); }

  // ================= 22. Ⅳ-4 리스크 =================
  { const s = content(22, "Ⅳ. 추진 계획");
    head(s, "Ⅳ. 추진 계획", "리스크 및 대응 방안", "상인 참여·대형 플랫폼 경쟁에 더해 AI 오류·식품 안전·원산지 신뢰를 핵심 리스크로 보고, 사람 확인과 표시 의무로 대응함");
    const lv = (t) => ({ t, o: { align: "center", bold: true, color: t === "높음" ? ACC : t === "중간" ? G700 : G500 } });
    table(s, ["리스크", "영향도", "대응 방안"], [
      ["상인 참여 저조 (디지털 피로)", lv("높음"), "카톡 한 줄 등록 · 현장 온보딩 · 첫 6개월 수수료 0%, 주문을 먼저 확보한 뒤 상인 확대"],
      ["대형 플랫폼 경쟁 (배민 수수료 0%)", lv("높음"), "콘텐츠 · 구독 · 상인 AI 도구로 차별화, 병행 입점 허용 (독점 요구 없음)"],
      ["AI 오류 (파싱 · 추천)", lv("중간"), "사장님 확인 후 게시, 단가 · 수량 범위 검증, ‘AI 정리’ 표시"],
      ["식품 안전", lv("중간"), "꼭 데쳐 먹는 나물 표시, 야생 채취 식물 판별 금지, 손질 · 데침은 당일 픽업"],
      ["원산지 신뢰", lv("중간"), "매장별 원산지 표시 의무화, 직매장 · 산지 연계, 원산지 위반 매장 즉시 제외"],
      ["계절성 · 가격 변동", lv("중간"), "묵나물 · 사계절 나물, 구독 가격 고정, AI 입고 추천으로 재고 조절"],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [2.6, 0.85, 5.65], rowH: [0.32, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47], align: ["left", "center", "left"], size: 10 });
    foot(s, "주: 영향도는 사업 초기(0~1단계) 기준 자체 평가"); }

  // ================= 23. Ⅳ-5 팀 =================
  { const s = content(23, "Ⅳ. 추진 계획");
    head(s, "Ⅳ. 추진 계획", "팀 구성", "대표가 데이터·AI와 현장 제휴를 맡고, 개발·콘텐츠 인력과 상인·영양·식품안전 자문으로 실행력을 보완함");
    table(s, ["역할", "담당", "역량 · 근거", "확보 계획"], [
      [{ t: "대표 ○○○", o: { color: BRAND } }, "수요 예측 · 데이터 · AI 설계, 상인 제휴 현장 운영", "공학 연구실 시뮬레이션 · 데이터 분석(파이썬) 경험\nAI 코딩 도구로 프로토타입 직접 제작", { t: "확보", o: { bold: true, color: BRAND } }],
      ["개발 1명", "웹앱 · 결제 · 지도 · 챗봇", "공동창업 또는 파트타임, AI 코딩 도구 활용", "1단계 착수 전"],
      ["콘텐츠 1명", "도감 · 레시피 촬영, 크리에이터 제휴", "요리 · 영상 경험 (파트타임)", "0단계 중"],
      ["자문", "상인회 · 창업지원단 · 영양사 · 식품안전", "현장 · 아동 식단 · 원산지/표시 규정", "0단계 중"],
    ], { x: 0.45, y: 1.68, w: 9.1, colW: [1.35, 2.75, 3.6, 1.4], rowH: [0.34, 0.7, 0.5, 0.5, 0.5], align: ["center", "left", "left", "center"], size: 10 });
    s.addShape(pres.ShapeType.rect, { x: 0.45, y: 4.52, w: 9.1, h: 0.44, fill: { color: BRANDL }, line: { color: BRANDL, width: 0 }, objectName: "team band" });
    tx(s, [{ text: "일하는 방식  ", options: { bold: true, color: BRAND } }, { text: "작은 팀 + AI 도구: 개발 · 콘텐츠 · 고객 응대 초안을 AI로 처리해 고정비를 낮춘다" }], { x: 0.6, y: 4.52, w: 8.85, h: 0.44, fontSize: 10, color: INK, valign: "middle", objectName: "team band text" });
    foot(s, "주: 시드 단계 투자자는 팀 슬라이드를 가장 오래 본다 (DocSend 2024) · 이름과 경력은 발표자 정보로 채울 것"); }

  // ================= 24. 맺음 =================
  pres.addSection({ title: "맺음" });
  { const s = pres.addSlide({ masterName: "CLOSING", sectionTitle: "맺음" });
    tx(s, "맺음말", { x: 0.6, y: 0.6, w: 3, h: 0.3, fontSize: 12, color: "A9C2B3", objectName: "closing label" });
    s.addText("오늘 나물, 동네에서.", { placeholder: "title" });
    s.addText("콘텐츠와 AI가 수요를 만들고, 동네 가게가 공급하고, 데이터가 쌓이는 구조", { placeholder: "body" });
    tx(s, "Next Steps", { x: 0.6, y: 2.6, w: 3, h: 0.3, fontSize: 11, bold: true, color: "A9C2B3", objectName: "next steps label" });
    [["01", "파일럿 착수", "2026.12 ~ 2027.2\n캠퍼스 인근 시장 1곳 · 점포 2~3곳"], ["02", "AI 검증", "AI 셰프 추천 품질 · 상인 메시지 정리\n오류율 기록, 이동평균 예측 시작"], ["03", "지원사업 · 팀", "2027 예비창업패키지 공고 대응\n개발 · 콘텐츠 팀원 확보"]].forEach(([n, h, d], i) => { const x = 0.6 + i * 2.95;
      s.addShape(pres.ShapeType.rect, { x, y: 2.95, w: 2.8, h: 1.35, fill: { color: "214A39" }, line: { color: "214A39", width: 0 }, objectName: "step box " + n });
      tx(s, n, { x: x + 0.2, y: 3.05, w: 0.6, h: 0.4, fontSize: 18, bold: true, color: "FFFFFF", objectName: "step num " + n });
      tx(s, h, { x: x + 0.85, y: 3.05, w: 1.85, h: 0.4, fontSize: 13, bold: true, color: "FFFFFF", valign: "middle", objectName: "step head " + n });
      tx(s, d, { x: x + 0.2, y: 3.55, w: 2.5, h: 0.65, fontSize: 10, color: "C7D6CC", objectName: "step desc " + n }); });
    tx(s, "감사합니다", { x: 0.6, y: 4.65, w: 4, h: 0.4, fontSize: 16, bold: true, color: "FFFFFF", objectName: "thanks" });
    tx(s, "질의응답", { x: 5.9, y: 4.65, w: 3.5, h: 0.4, fontSize: 12, color: "A9C2B3", align: "right", valign: "middle", objectName: "qa" });
    s.addNotes(note(24)); }

  // ================= 25. 부록 =================
  pres.addSection({ title: "부록" });
  { const s = content(25, "부록");
    head(s, "부록", "참고 자료", "본 자료의 수치는 2026.10.29~30 웹 검색 기준 공개 통계·보도를 인용함 (발표 전 원문 확인 권장)");
    const L = ["국가데이터처 「2025 통계로 보는 1인 가구」 (2025.12)", "질병관리청 국민건강영양조사 2022–2024 (뉴시스 2026.08)", "산림청 「2024년 임산물생산조사」 (쿠키뉴스 2025.10)", "소상공인시장진흥공단 전통시장 실태조사 (2025.01 보도)", "농림축산식품부 로컬푸드 직매장 현황 (2021.06)", "식약처 산나물·독초 안전 안내, 한국소비자원 위해 집계", "경북매일, 중국산 고사리 급식 납품 적발 (2023.05)", "국가데이터처·KAMIS 시금치 가격 (2026.08 보도)", "KREI 산채 소비자 의향 연구 · 나물 조리 과학 논문", "예비창업패키지 · 농식품 벤처육성 · AI 바우처 공고 (2026)"];
    const R = ["머니투데이, 배민 전통시장 입점 성과 (2026.03)", "한국경제, 어글리어스 (2025.02) · 원티드 기업정보", "당근 2025 실적 보도 · 모바일인덱스 (2025.10)", "Afresh 투자 발표 (2026.04) · Grocery Dive", "뉴데일리, 컬리 데멍이 폐기율 (2025.07)", "Supermarket News, Ask Instacart (2023)", "Too Good To Go 2025 성과 · vivid garden 타베쵸쿠 (2026.04)", "Sequoia · YC · DocSend 피치덱 가이드", "Anthropic Claude API 가격표 (2026.10)", "이미지: Microsoft Fluent Emoji (MIT) · 글꼴: Pretendard (OFL)"];
    const col = (arr, start, x, h) => { tx(s, h, { x, y: 1.66, w: 4.45, h: 0.28, fontSize: 11, bold: true, color: C.accent1, objectName: "ref head " + h });
      s.addText(arr.map((t, i) => ({ text: t, options: { bullet: { type: "number", numberStartAt: start }, breakLine: i < arr.length - 1 } })), { x, y: 1.98, w: 4.45, h: 3.0, fontSize: 9.5, color: INK, paraSpaceAfter: 3, valign: "top", margin: 0, isTextBox: true, objectName: "ref list " + h }); };
    col(L, 1, 0.45, "통계 · 시장 · 나물 도메인"); col(R, 11, 5.1, "벤치마크 · AI · 피칭 · 출처");
    foot(s, "전체 링크: 04 레퍼런스 · 06 피치덱 레퍼런스 · 07 나물 도메인 리서치 문서"); }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})().catch((e) => { console.error(e); process.exit(1); });

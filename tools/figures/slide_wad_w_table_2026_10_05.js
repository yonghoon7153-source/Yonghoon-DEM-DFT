#!/usr/bin/env node
/*
 * slide_wad_w_table_2026_10_05.js — 점착(W_ad) 트랙에서 지금까지 나온 W 값 정리 PPT 두 장 (QE · UMA)
 * 사용자 요청 2026-10-05: "지금 까지 나온 W 값 종류 관련해서 표로 작성해줘 ppt sheet로 (UMA, QE 구분해서)"
 *
 *   NODE_PATH=<pptxgenjs 가 깔린 node_modules> node tools/figures/slide_wad_w_table_2026_10_05.js <out.pptx>
 *   node tools/figures/slide_wad_w_table_2026_10_05.js --selftest     # 양성 + 음성 (pptxgenjs 불필요)
 *
 * 숫자는 이 파일에 없다 — 결과 기록 다섯 개(db/properties/wad_*_result_*.json)에서 경로로 읽는다.
 * 게이트 상태(통과·FAIL·경보)도 기록 문자열에서 확인하고, 기대와 다르면 **만들지 않는다** (fail-closed).
 *
 * 이 도구가 못 하는 것
 *   · 값을 판정하지 않는다 — 기록의 헤드라인·라벨을 옮긴다. 라벨 문구는 기록의 허용 문장을 줄인 것이다.
 *   · ⛔ 산출 pptx 를 레포·webapp 에 올리지 않는다 (점착 W 는 화면에 안 싣는다 — 대피 세션 운영 규칙).
 *     기본 출력은 세션 scratchpad 다. 이 생성기만 레포에 둔다 (숫자 없음).
 *   · 진행 중(P1b)·대기(V5) 계산의 값은 없다 — '값 없음' 으로 적는다 (0 으로 그리지 않는다).
 *   · 문헌값은 WAD-CC 의 DEM 시나리오 칸(실험 0.37 ± 0.01 · Wang 2015)에만 결과 기록 문장 그대로 둔다.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const P = (f) => path.join(ROOT, "db", "properties", f);
const SRC = {
  cc: P("wad_cc_graphite_result_2026_09_30.json"),
  v2: P("wad_aprime_pilot_result_v2_2026_09_26.json"),
  v4: P("wad_aprime_pilot_result_v4_2026_09_28.json"),
  sese: P("wad_sese_4L_result_2026_09_25.json"),
  uma: P("wad_se_pairs_uma_result_2026_10_01.json"),
  pipe: path.join(ROOT, "db", "pipelines", "adhesion_pipeline.json"),
};

class Refuse extends Error {}
const need = (c, msg) => { if (!c) throw new Refuse(msg); };
function dig(d, keys, what) {
  let cur = d;
  for (const k of keys) {
    need(cur !== null && typeof cur === "object" && k in cur, `${what}: 경로 ${keys.join(" › ")} 가 없다`);
    cur = cur[k];
  }
  return cur;
}
const num = (v, what) => { need(typeof v === "number" && isFinite(v), `${what}: 숫자가 아니다 (${v})`); return v; };
const f3 = (v) => (v < 0 ? "−" : "") + Math.abs(v).toFixed(3);
const f2 = (v) => (v < 0 ? "−" : "") + Math.abs(v).toFixed(2);
const rng = (a, b, f = f3) => (f(a) === f(b) ? f(a) : (a < 0 || b < 0) ? `${f(a)} ~ ${f(b)}` : `${f(a)}–${f(b)}`);

function load(src = SRC) {
  const J = {};
  for (const [k, f] of Object.entries(src)) J[k] = JSON.parse(fs.readFileSync(f, "utf8"));

  // ── QE ① WAD-CC (C|C 흑연)
  const s33 = dig(J.cc, ["정보량_판정_아님_카드5", "S33_비정합"], "WAD-CC");
  const cc = {
    w: num(s33["W_inc_2성"], "WAD-CC W_inc"),
    aa: num(s33["괄호"][0], "WAD-CC AA"), ab: num(s33["괄호"][1], "WAD-CC AB"),
    atm: num(dig(J.cc, ["D3_3체_ATM_열", "W_inc_S33_plus_ATM"], "WAD-CC"), "WAD-CC +ATM"),
  };
  need(String(dig(J.cc, ["게이트_사전등록_카드4", "라벨"], "WAD-CC")).includes("게이트 전부 통과"), "WAD-CC: 게이트 라벨이 '전부 통과' 가 아니다");
  const scen = dig(J.cc, ["1저자_결정_2026_09_30"], "WAD-CC");
  need(String(scen["DEM_입력값"]).includes("둘 다 시나리오"), "WAD-CC: DEM 입력 결정이 '둘 다 시나리오' 가 아니다");
  const mExp = String(scen["시나리오_실험"]).match(/^([0-9.]+) ± ([0-9.]+) J\/m²/);
  need(mExp, "WAD-CC: 실험 시나리오 문장을 못 읽었다");
  cc.exp = `${mExp[1]} ± ${mExp[2]}`;

  // ── QE ② V2 Ag(111)|그래핀
  const atm2 = dig(J.v2, ["D3_3체_ATM_열_2026_09_27"], "V2");
  const g3 = dig(J.v2, ["G3_top_fcc"], "V2");
  need(String(g3["판정"]).includes("G3 FAIL"), "V2: G3 판정이 FAIL 이 아니다");
  need(String(dig(J.v2, ["G4_top_fcc", "판정"], "V2")).includes("미검증"), "V2: G4 가 '미검증' 이 아니다");
  const reg = dig(J.v2, ["표_registry_4"], "V2");
  const wpbe = Object.values(reg).map((r) => num(r["W_PBE_J_m2"], "V2 W_PBE"));
  const uW = Object.values(reg).map((r) => num(r.UMA["W_UMA_J_m2"], "V2 UMA"));
  const uD = Object.values(reg).map((r) => num(r.UMA["W_UMA_plus_QE_D3_J_m2"], "V2 UMA+D3"));
  const uDel = Object.values(reg).map((r) => num(r.UMA["Delta_J_m2"], "V2 UMA Δ"));
  const v2 = {
    w8: num(atm2["8A"]["W_2체"], "V2 8A"), w10: num(atm2["10A_ii"]["W_2체"], "V2 10A"),
    a8: num(atm2["8A"]["W_2체+ATM"], "V2 8A+ATM"), a10: num(atm2["10A_ii"]["W_2체+ATM"], "V2 10A+ATM"),
    dg3: num(g3["(ii)_직접_8→10"]["dW_J_m2"], "V2 G3 ii"),
    pbe: Math.max(...wpbe), pbeMin: Math.min(...wpbe),
    uma: [Math.min(...uW), Math.max(...uW)], umaD3: [Math.min(...uD), Math.max(...uD)],
    umaDel: [Math.min(...uDel), Math.max(...uDel)],
  };

  // ── QE ③ V4 SE + 벤젠 (조각)
  const v4 = {
    e: num(dig(J.v4, ["값", "dE_frag_F_eV"], "V4"), "V4 ΔE"),
    ea: num(dig(J.v4, ["ATM_3체_별도_열", "dE_frag_2body_plus_ATM_eV"], "V4"), "V4 +ATM"),
    g3ii: num(dig(J.v4, ["G3_끝점_조각", "ii_직접_8→10", "d_dE_frag_meV"], "V4"), "V4 G3 ii"),
  };
  need(dig(J.v4, ["G3_끝점_조각", "상태"], "V4") === "FAIL", "V4: G3 상태가 FAIL 이 아니다");
  need(J.v4.status === "proposed", "V4: 결과 기록 상태가 proposed 가 아니다 (표 문구를 고쳐야 한다)");

  // ── QE ④ SE|SE 4층 (대조 계산)
  const W = dig(J.sese, ["W_J_m2"], "SE|SE");
  const sese = {
    cleave: num(W["W_cleave_relaxed_PBE"], "SE|SE cleave"),
    cleaveB: num(dig(J.sese, ["⛔_정정_회신BX_2026_09_25", "Codex_독립_재계산", "W′_B′기준"], "SE|SE"), "SE|SE B′"),
    sep: num(W["W_sep_unrelaxed_PBE"], "SE|SE sep"), sepD3: num(W["W_sep_unrelaxed_PBE_D3BJ_2body"], "SE|SE sep D3"),
  };
  need(String(dig(J.sese, ["경보_v2", "결과"], "SE|SE")).includes("발화"), "SE|SE: 경보 v2 가 '발화' 가 아니다");
  need(J.sese.citable === false, "SE|SE: citable 이 false 가 아니다");

  // ── 진행 중: P1b (점착 원장 state_text 의 |ΔW| 만)
  const p1b = (J.pipe.systems || []).find((x) => x.id === "P1b");
  need(p1b, "점착 원장에 P1b 가 없다");
  const mdw = String(p1b.state_text).match(/\|ΔW\| ([0-9.]+e-?[0-9]+) J\/m²/);
  need(mdw, "P1b: 기계 대조 |ΔW| 를 못 읽었다");
  need(!/\bW\s+0\.\d{3}/.test(String(p1b.state_text)), "P1b: state_text 에 W 값이 다시 들어왔다 (화면 규율)");
  const st2 = String(p1b.state_text).match(/2단계 SCF \*\*(\d+)\/(\d+)\*\*/);
  const p1 = { dw: mdw[1], st2: st2 ? `${st2[1]}/${st2[2]}` : null };

  // ── UMA: SE 쌍 예측 (P1 · P2 × 종결)
  const H = dig(J.uma, ["★_헤드라인_카드5", "값"], "UMA");
  const order = ["P1_s_outer", "P1_li_outer", "P2_s_outer", "P2_li_outer"];
  const uma = order.map((k) => {
    const r = H[k]; need(r, `UMA: ${k} 가 없다`);
    return {
      key: k, name: r["계면·종결"],
      w: num(r["W_sep_2체_10A_J_m2"], k), lo: num(r["registry_범위_J_m2"][0], k), hi: num(r["registry_범위_J_m2"][1], k),
      atm: num(r["ATM_열_J_m2"], k), w12: num(r["정보_12A_2체_J_m2"], k), wa: num(r["민감도_2체_더하기_ATM_J_m2"], k),
    };
  });
  const g = dig(J.uma, ["게이트_카드4"], "UMA");
  need(/8\/8 PASS/.test(g["G1_이완"]) && /8\/8 PASS/.test(g["G2_구조"]), "UMA: G1·G2 가 8/8 PASS 가 아니다");
  need(/PASS/.test(g["G3_끝점"]["P1_s_outer_A"]) && /PASS/.test(g["G3_끝점"]["P2_s_outer_A"]), "UMA: G3 대표 PASS 가 아니다");
  need(/대기/.test(g["G5_V5"]), "UMA: G5 가 '대기' 가 아니다 (표 문구를 고쳐야 한다)");
  need(String(dig(J.uma, ["라벨_카드1a", "항상"], "UMA")).includes("미검증 UMA+D3 예측"), "UMA: 항상 라벨이 바뀌었다");
  return { cc, v2, v4, sese, p1, uma };
}

// ──────────────────────────────────────────────── 슬라이드
const INK = "1F2937", MUT = "6B7280", LINE = "D1D5DB";
const QE = "0F766E", QE_T = "E6F4F1";        // teal — DFT (QE)
const UM = "B45309", UM_T = "FDF3E7";        // amber — 예측 (UMA)
const FONT = "Malgun Gothic";

function build(D, out) {
  const pptxgen = require("pptxgenjs");
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";                 // 13.33 × 7.5 in
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  pres.title = "W_ad 값 정리 — QE · UMA";
  pres.defineSlideMaster({
    title: "SHEET",
    background: { color: "FFFFFF" },
    objects: [
      { text: { text: "Hanyang · LPSCl 점착(W_ad) 트랙 · 2026-10-05 · 숫자 = 결과 기록에서만", options: { x: 0.5, y: 7.08, w: 9.5, h: 0.28, fontSize: 9, color: MUT, fontFace: FONT, margin: 0 } } },
    ],
    slideNumber: { x: 12.4, y: 7.08, w: 0.45, h: 0.28, fontSize: 9, color: MUT, fontFace: FONT },
  });

  const hdr = (t, fill) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: fill }, fontSize: 12, valign: "middle", fontFace: FONT } });
  const cell = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 12, color: INK, valign: "middle", fontFace: FONT }, o) });
  const strong = (t, color) => ({ text: t, options: { bold: true, color: color || INK } });
  const br = (t, o = {}) => ({ text: t, options: Object.assign({ breakLine: true }, o) });

  function title(slide, t, sub, badge, col, tint) {
    slide.addText(t, { x: 0.5, y: 0.32, w: 9.9, h: 0.62, fontSize: 30, bold: true, color: INK, fontFace: FONT, margin: 0, isTextBox: true, objectName: "title" });
    slide.addText(sub, { x: 0.5, y: 1.0, w: 10.2, h: 0.5, fontSize: 13, color: MUT, fontFace: FONT, margin: 0, valign: "top", isTextBox: true, objectName: "subtitle" });
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.85, y: 0.36, w: 1.98, h: 0.62, rectRadius: 0.12, fill: { color: tint }, line: { color: col, width: 1.25 }, objectName: "badge" });
    slide.addText(badge, { x: 10.85, y: 0.36, w: 1.98, h: 0.62, fontSize: 15, bold: true, color: col, align: "center", valign: "middle", fontFace: FONT, margin: 0, isTextBox: true, objectName: "badge-text" });
  }

  // ── ① QE
  {
    const s = pres.addSlide({ masterName: "SHEET" });
    title(s, "W 값 정리 ① — QE (DFT · PBE+D3(BJ))",
      "QE 고정기하 분리일 W_sep = [E(far) − E(bound)] / A · 헤드라인 = D3 2체 · ATM 3체는 따로",
      "QE · DFT", QE, QE_T);
    const { cc, v2, v4, sese, p1 } = D;
    const rows = [
      [hdr("계면 · 모형", QE), hdr("W 헤드라인 (J/m²)", QE), hdr("+ATM 3체", QE), hdr("게이트 · 라벨", QE), hdr("DEM 전달", QE)],
      [cell([br("C | C 흑연 기저면 (WAD-CC)", { bold: true }), br("덴카·VGCF 세 쌍 공통"), { text: "09-30 · V100 53 잡" }]),
        cell([br(f3(cc.w), { bold: true, color: QE }), { text: `[AA ${f3(cc.aa)} · AB ${f3(cc.ab)}]` }]),
        cell(f3(cc.atm)),
        cell([br("전부 통과"), br("(흑연 대조 · 끝점 · 수치 · 두께)"), { text: "2체 조건부 · 이상 기저면" }]),
        cell([br("✅ 회신 8 · 두 시나리오"), br(`DFT ${f3(cc.w)}`), { text: `실험 ${cc.exp} †` }])],
      [cell([br("Ag(111) | 그래핀 1장 (V2)", { bold: true }), br("A′ 파일럿 · Ag–C 접촉"), { text: "09-26 · V100 28 잡" }]),
        cell([{ text: f3(v2.w8), options: { bold: true, color: QE } }, br(" (끝점 8 Å)"), { text: `${f3(v2.w10)} (끝점 10 Å)` }]),
        cell([br(`${f3(v2.a8)} (8 Å)`), { text: `${f3(v2.a10)} (10 Å)` }]),
        cell([br(`G3 FAIL (8→10 Å +${v2.dg3.toFixed(3)})`), br("G4 k 축 미검증"), { text: `PBE 단독 ${rng(v2.pbeMin, v2.pbe)} (결합 = 분산항)` }]),
        cell([br("✅ 회신 5 · 라벨 동반"), { text: "8 Å 값 + 10 Å 병기" }])],
      [cell([br("SE 위 벤젠 조각 1개 (V4)", { bold: true }), br("A′ 파일럿 · 조각 모델"), { text: "09-28 · gabia 9 잡" }]),
        cell([br(`ΔE_frag ${f2(v4.e)} eV/조각`, { bold: true, color: QE }), { text: "⛔ J/m² 로 바꾸지 않는다" }]),
        cell(`${f2(v4.ea)} eV/조각`),
        cell([br(`G3 FAIL (8→10 Å +${v4.g3ii.toFixed(1)} meV)`), { text: "G4 k·smearing PASS · ecut 미검증" }]),
        cell([br("참고 인계 (회신 7 초안)"), br("기록 proposed"), { text: "J/m² 기준선 아님" }])],
      [cell([br("LPSCl | LPSCl (SE|SE 4층)", { bold: true }), br("방법 점검용 대조 계산"), { text: "09-25 · V100 5 잡" }]),
        cell([{ text: `W_cleave ${f3(sese.cleave)}`, options: { bold: true, color: QE } }, br(` · ${f3(sese.cleaveB)}*`), br(`무이완 PBE ${f3(sese.sep)}`), { text: `무이완 PBE+D3 ${f3(sese.sepD3)}` }]),
        cell("— (미계산)", { color: MUT }),
        cell([br("경보 v2 발화 — 합격선 아님"), br("운영 구간 0.3–0.7 아래"), { text: "일부 = 기준 벌크 셀 모양" }]),
        cell([br("⛔ DEM 금지", { bold: true, color: "B91C1C" }), { text: "파라미터·서열로 안 씀" }])],
    ];
    s.addTable(rows, { x: 0.5, y: 1.55, w: 12.33, colW: [2.85, 2.55, 1.35, 3.05, 2.53], rowH: [0.42, 0.78, 0.78, 0.78, 0.78],
      border: { type: "solid", pt: 0.75, color: LINE }, margin: [0.05, 0.08, 0.05, 0.08], autoPage: false, objectName: "qe-table" });
    // 진행 · 대기 — 아직 W 없음 (표 밖 상자)
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 5.58, w: 12.33, h: 0.74, rectRadius: 0.08, fill: { color: "F3F4F6" }, line: { color: LINE, width: 0.75 }, objectName: "pending-box" });
    s.addText([
      { text: "진행 · 대기 — 아직 W 없음", options: { bold: true, color: INK, breakLine: true } },
      { text: `P1b Ag(111) | 흑연 3층 (kgy) — 기계 대조 G1 PASS (kgy–V100 |ΔW| ${p1.dw} J/m²)${p1.st2 ? ` · 2단계 ${p1.st2}` : ""}   ·   V5 LPSCl | Ag 작은 모델 (VASP 외주) — 09-30 발송 · 반송 대기 (UMA 예측 검증 G5 용)` },
    ], { x: 0.66, y: 5.61, w: 12.0, h: 0.68, fontSize: 12, color: INK, fontFace: FONT, margin: 0, valign: "middle", isTextBox: true, objectName: "pending-text" });
    s.addText([
      { text: `* ${f3(sese.cleaveB)} = 기준 벌크를 epitaxial 셀(a·b 고정 · c 자유)로 바꾼 W_cleave (회신 BX 재계산) · ${f3(sese.cleave)} = 입방 기준.   † 실험 = Wang 2015 흑연 박리 (비정합 직접 측정).`, options: { breakLine: true } },
      { text: "출처: wad_cc_graphite_result_2026_09_30 · wad_aprime_pilot_result_v2_2026_09_26 · …_v4_2026_09_28 · wad_sese_4L_result_2026_09_25 · 점착 원장 (db/properties · db/pipelines)." },
    ], { x: 0.5, y: 6.43, w: 12.33, h: 0.55, fontSize: 10, color: MUT, fontFace: FONT, margin: 0, valign: "top", isTextBox: true, objectName: "qe-notes" });
  }

  // ── ② UMA
  {
    const s = pres.addSlide({ masterName: "SHEET" });
    title(s, "W 값 정리 ② — UMA (예측 · UMA+D3)",
      "UMA-s-1p1 이완 + D3(BJ) 2체 · 끝점 10 Å · 10-01 gabia · 게이트 G1 8/8 · G2 8/8 · G3 2/2 PASS",
      "UMA · 예측", UM, UM_T);
    const rows = [[hdr("계면 · 종결", UM), hdr("W 헤드라인 (J/m²)", UM), hdr("registry A–B", UM), hdr("+ATM (민감도)", UM), hdr("12 Å (정보)", UM)]];
    for (const r of D.uma) {
      const [iface, term] = r.name.split(" · ");
      rows.push([
        cell([strong(iface.replace("|", " | ")), { text: `  ${term} 종결` }]),
        cell([strong(f3(r.w), UM)]),
        cell(`[${f3(r.lo)}, ${f3(r.hi)}]`),
        cell(`${f3(r.wa)}  (ATM ${f3(r.atm)})`),
        cell(f3(r.w12), { color: MUT }),
      ]);
    }
    const v2 = D.v2;
    rows.push([
      cell([strong("방법 대조"), { text: " — Ag(111) | 그래핀 (V2 기하)" }], { fill: { color: "F3F4F6" } }),
      cell([br("UMA 단독"), { text: rng(v2.uma[0], v2.uma[1]) }], { fill: { color: "F3F4F6" } }),
      cell([br("UMA+QE-D3"), { text: rng(v2.umaD3[0], v2.umaD3[1]) }], { fill: { color: "F3F4F6" } }),
      cell([br(`PBE+D3 ${f3(v2.w8)} 보다`), { text: `${rng(v2.umaDel[0], v2.umaDel[1])} 낮다` }], { fill: { color: "F3F4F6" } }),
      cell("G5 대상 아님", { fill: { color: "F3F4F6" }, color: MUT }),
    ]);
    s.addTable(rows, { x: 0.5, y: 1.55, w: 12.33, colW: [4.35, 1.9, 1.95, 2.55, 1.58], rowH: [0.42, 0.5, 0.5, 0.5, 0.5, 0.5],
      border: { type: "solid", pt: 0.75, color: LINE }, margin: [0.05, 0.08, 0.05, 0.08], autoPage: false, objectName: "uma-table" });
    // 라벨 상자 — 결과 기록 카드 1a 네 문장의 요지 (떼지 않는다)
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 4.72, w: 12.33, h: 1.3, rectRadius: 0.08, fill: { color: UM_T }, line: { color: UM, width: 0.75 }, objectName: "label-box" });
    s.addText([
      { text: "라벨 — 값과 같이 다닌다 (카드 1a)", options: { bold: true, color: UM, breakLine: true } },
      { text: "미검증 UMA+D3 예측이다 — DEM 에서는 민감도 시나리오로만 · registry 범위는 신뢰구간·물리적 상하한이 아니다", options: { bullet: true, breakLine: true } },
      { text: "SE 쌍(UMA)과 C–C · Ag–C(QE DFT)의 비는 방법이 섞인 비다 · LPSCl | 흑연은 DFT 로 확인할 경로가 없다", options: { bullet: true, breakLine: true } },
      { text: "종결 둘을 평균하지 않는다 (종결 비율은 DEM 몫) · ATM 을 헤드라인에 더해 '더 정확한 값' 으로 쓰지 않는다", options: { bullet: true } },
    ], { x: 0.68, y: 4.8, w: 12.0, h: 1.15, fontSize: 12, color: INK, fontFace: FONT, margin: 0, valign: "top", paraSpaceAfter: 3, isTextBox: true, objectName: "label-text" });
    s.addText([
      { text: "상태: DEM 회신 9 초안 (사용자 검토 · 발송 대기) · G5 = V5 VASP 외주(은 쪽 작은 모델) 반송 뒤 · 흑연 쪽은 ATM 이 2체의 18–26 % (은 10–14 %).", options: { breakLine: true } },
      { text: "출처: wad_se_pairs_uma_result_2026_10_01 (헤드라인 카드 5) · wad_aprime_pilot_result_v2_2026_09_26 (V2 의 UMA 대조 열)." },
    ], { x: 0.5, y: 6.38, w: 12.33, h: 0.55, fontSize: 10, color: MUT, fontFace: FONT, margin: 0, valign: "top", isTextBox: true, objectName: "uma-notes" });
  }
  return pres.writeFile({ fileName: out });
}

// ──────────────────────────────────────────────── 시험
function selftest() {
  const bad = [];
  const chk = (c, m) => { if (!c) bad.push(m); };
  const dies = (fn, frag) => {
    try { fn(); bad.push(`죽어야 하는데 살았다: ${frag}`); }
    catch (e) { if (!(e instanceof Refuse) || !e.message.includes(frag)) bad.push(`다른 이유로 죽었다: ${e.message} (기대 ${frag})`); }
  };
  const D = load();
  chk(D.uma.length === 4, "UMA 행이 넷이 아니다");
  chk(D.cc.w > 0 && D.cc.aa <= D.cc.w && D.cc.w <= D.cc.ab, "WAD-CC 헤드라인이 [AA, AB] 밖");
  chk(D.uma.every((r) => r.lo <= r.w && r.w <= r.hi + 1e-12), "UMA 헤드라인이 registry 범위 밖");
  chk(D.uma.every((r) => Math.abs(r.w + r.atm - r.wa) < 2e-3), "UMA: 2체+ATM 이 헤드라인+ATM 과 안 맞는다");
  chk(Math.abs(D.cc.atm - D.cc.w) > 0.01, "WAD-CC ATM 열이 헤드라인과 같다 — 다른 칸을 읽었다");
  chk(/^0\.\d+ ± 0\.\d+$/.test(D.cc.exp), "실험 시나리오 형식");
  chk(D.p1.dw === "1.0e-7", `P1b |ΔW| ${D.p1.dw}`);
  // 음성 — 기록 사본을 하나씩 망가뜨린다
  const os = require("os");
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "wadppt-"));
  const mut = (key, fn) => {
    const j = JSON.parse(fs.readFileSync(SRC[key], "utf8")); fn(j);
    const f = path.join(tmp, `${key}.json`); fs.writeFileSync(f, JSON.stringify(j));
    return Object.assign({}, SRC, { [key]: f });
  };
  dies(() => load(mut("cc", (j) => { j["게이트_사전등록_카드4"]["라벨"] = "G3 FAIL"; })), "전부 통과");
  dies(() => load(mut("v2", (j) => { j["G3_top_fcc"]["판정"] = "PASS"; })), "G3 판정");
  dies(() => load(mut("v4", (j) => { j.status = "ratified"; })), "proposed");
  dies(() => load(mut("sese", (j) => { j["경보_v2"]["결과"] = "정상"; })), "발화");
  dies(() => load(mut("uma", (j) => { j["게이트_카드4"]["G5_V5"] = "PASS"; })), "G5");
  dies(() => load(mut("uma", (j) => { delete j["★_헤드라인_카드5"]["값"]["P2_li_outer"]; })), "P2_li_outer");
  dies(() => load(mut("uma", (j) => { j["★_헤드라인_카드5"]["값"]["P1_s_outer"]["W_sep_2체_10A_J_m2"] = "0.89"; })), "숫자가 아니다");
  dies(() => load(mut("pipe", (j) => { const p = j.systems.find((x) => x.id === "P1b"); p.state_text += " · CTRL W 0.1234567"; })), "화면 규율");
  dies(() => load(mut("cc", (j) => { j["1저자_결정_2026_09_30"]["DEM_입력값"] = "(a) DFT 만"; })), "둘 다 시나리오");
  if (bad.length) { console.log("SELFTEST FAIL"); bad.forEach((b) => console.log("  ✗", b)); return 1; }
  console.log("SELFTEST PASS — 양성 7 · 음성 9");
  return 0;
}

if (require.main === module) {
  const a = process.argv.slice(2);
  if (a.includes("--selftest")) process.exit(selftest());
  const out = a[0];
  if (!out) { console.error("usage: node slide_wad_w_table_2026_10_05.js <out.pptx> | --selftest"); process.exit(2); }
  const D = load();
  build(D, out).then((f) => console.log("PPTX", f)).catch((e) => { console.error(e); process.exit(1); });
}
module.exports = { load, build, Refuse };

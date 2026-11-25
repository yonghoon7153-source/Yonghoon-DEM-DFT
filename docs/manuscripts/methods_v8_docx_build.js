const {Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
       WidthType, ShadingType, AlignmentType, BorderStyle} = require("docx");
const fs = require("fs");

const W = 9000;                       // A4 - 여백
const INK = "1F2937", MUT = "6B7280", RED = "B91C1C", BLU = "1D4ED8";

const P = (t, o = {}) => new Paragraph({
  spacing: {after: o.after === undefined ? 120 : o.after, line: 276},
  alignment: o.align, indent: o.indent,
  border: o.rule ? {bottom: {style: BorderStyle.SINGLE, size: 6, color: "D1D5DB"}} : undefined,
  children: (Array.isArray(t) ? t : [t]).map(x =>
    typeof x === "string"
      ? new TextRun({text: x, size: o.size || 20, color: o.color || INK,
                     bold: o.bold, italics: o.italics, font: o.font})
      : x)});
const R  = (t, o = {}) => new TextRun({text: t, size: o.size || 20, color: o.color || INK,
                                       bold: o.bold, italics: o.italics, font: o.font});
const H1 = t => new Paragraph({heading: HeadingLevel.HEADING_1, spacing: {before: 320, after: 160},
                               children: [new TextRun({text: t, size: 28, bold: true, color: INK})]});
const H2 = t => new Paragraph({heading: HeadingLevel.HEADING_2, spacing: {before: 240, after: 120},
                               children: [new TextRun({text: t, size: 23, bold: true, color: INK})]});
// 영문 붙여넣기 블록 — 좌측 굵은 선 + 들여쓰기로 "이건 원고에 들어가는 글" 임을 표시
const EN = t => new Paragraph({
  spacing: {after: 140, line: 300}, indent: {left: 340},
  border: {left: {style: BorderStyle.SINGLE, size: 14, color: BLU, space: 12}},
  children: [new TextRun({text: t, size: 20, color: INK})]});
const BL = t => new Paragraph({bullet: {level: 0}, spacing: {after: 80, line: 276},
  children: [new TextRun({text: t, size: 20, color: INK})]});

const cell = (t, o = {}) => new TableCell({
  width: {size: o.w, type: WidthType.DXA},
  shading: o.fill ? {type: ShadingType.CLEAR, fill: o.fill, color: "auto"} : undefined,
  margins: {top: 70, bottom: 70, left: 110, right: 110},
  children: (Array.isArray(t) ? t : [t]).map(s => new Paragraph({
    spacing: {after: 0, line: 260}, alignment: o.align,
    children: [new TextRun({text: s, size: 18, bold: o.bold,
                            color: o.color || INK, italics: o.italics})]}))});
const table = (cols, rows) => new Table({
  columnWidths: cols, width: {size: cols.reduce((a, b) => a + b, 0), type: WidthType.DXA},
  rows: rows.map((r, i) => new TableRow({
    tableHeader: i === 0,
    children: r.map((c, j) => cell(c === null ? "" : c,
      {w: cols[j], fill: i === 0 ? "EEF2FF" : undefined, bold: i === 0,
       align: j > 0 && i > 0 ? AlignmentType.LEFT : undefined}))}))});

const kids = [];
const add = (...x) => kids.push(...x);

// ══════════════════════════════════════════════════════ 표지
add(new Paragraph({spacing: {after: 60},
  children: [R("Methods (simulation + DFT) — revision v8", {size: 34, bold: true})]}));
add(P("DFT · DEM 두 축을 한 문서로 — 공저자 검토용 교체안, 2026-08-30", {color: MUT, size: 20, rule: true}));
add(P([R("PROVISIONAL — NOT FOR SUBMISSION", {bold: true, color: RED, size: 22})], {after: 60}));
add(P("이 문서는 투고용 최종본이 아니라 " +
      "① 지금 확정된 문장을 그대로 붙여넣을 수 있게 정리하고 " +
      "② 아직 값이 없는 칸을 공란으로 드러내기 위한 것입니다. " +
      "공란은 값이 작아서 생략한 것이 아니라 아직 재지 않았다는 뜻입니다.", {color: MUT}));

add(H1("0. 공란이 어디인가 — 먼저 볼 것"));
add(P("본문·표·캡션에서 값이 비어 있는 자리는 아래 넷뿐입니다. 나머지는 전부 확정문입니다."));
add(table([2100, 3100, 1500, 2300], [
  ["자리", "무엇이 없나", "누가 채우나", "언제"],
  ["Figure 2e · 본문 34", "SDCP vs PTFE 흡착에너지 대비 [ A ]", "DFT 계산", "제출 후 약 4일"],
  ["Table S1", "없음 — 파라미터는 전부 확정", "—", "지금"],
  ["Table S3 σ_ion", "이온 전도도 시뮬 값", "DEM 트랙(별도 브랜치)", "미정"],
  ["Table S3 Areal capacity", "비용량 (mAh g⁻¹)", "공저자 회신", "회신 즉시"]]));
add(P("⚠ Figure 2e 의 공란 [ A ] 는 문장 안의 숫자 한 자리입니다. 그 값이 오면 " +
      "다른 문장은 하나도 바꾸지 않고 그 자리만 채우면 됩니다 — §5 에 들어갈 문장을 " +
      "미리 적어 두었습니다.", {color: MUT}));

// ══════════════════════════════════════════════════════ 1
add(H1("1. v6 대비 무엇이 바뀌나 (DFT 축)"));
add(table([2600, 3000, 3400], [
  ["항목", "v6", "v8"],
  ["계산 코드", "Quantum ESPRESSO 로 서술", "VASP (PAW) — 인용할 값이 이 트랙의 산출입니다"],
  ["기하", "서술 없음", "UMA 이완 기하 위의 단일점 — DFT 최소점이 아님을 명시"],
  ["자기 상태", "\"반강자성 (net 0), Ni 1.02 μB\"", "시작 배치를 선언하고, 실현된 모멘트를 기록하는 방식으로 서술"],
  ["기준계 대칭성", "서술 없음", "복합체·슬랩·기체가 모두 같은 스핀 구속 정책 — 이것이 v6 세대 값을 보류시킨 원인"],
  ["분산 보정", "\"Grimme D3\"", "D3 zero damping 으로 명시 (D3-BJ 아님)"],
  ["기전 문장", "술포네이트가 표면과 상호작용한다", "삭제 — 계산이 그 기전을 보이지 않습니다 (§6)"]]));

// ══════════════════════════════════════════════════════ 2
add(H1("2. Methods — DFT · 설명형 (Full)"));
add(P("지면이 허용되면 이쪽을 씁니다. 영문 그대로 붙여넣으면 됩니다.", {color: MUT}));
add(EN("DFT calculations. Spin-polarised DFT calculations were performed with VASP using " +
  "projector augmented-wave potentials and the Perdew–Burke–Ernzerhof functional, with " +
  "Grimme's D3 dispersion correction in the zero-damping form and a rotationally invariant " +
  "Dudarev +U correction of U − J = 6.2 eV applied to the Ni 3d states. The plane-wave " +
  "cut-off was 520 eV with an electronic convergence threshold of 1 × 10⁻⁶ eV, Gaussian " +
  "smearing of 0.05 eV, aspherical gradient corrections within the PAW spheres, and " +
  "real-space projection disabled."));
add(EN("The NCM811 surface was represented by a LiNiO₂(104) slab (1 × 4, four layers, " +
  "192 atoms, 18.27 × 11.51 Å in plane) with more than 15 Å of vacuum, a Γ-centred " +
  "3 × 4 × 1 k-mesh, and a dipole correction along the surface normal. SDCP was represented " +
  "by its sulfonate-functionalised EDOT repeat unit (C₁₁H₁₆O₆S₂) and PTFE by a C₁₀F₂₂ " +
  "segment; gas-phase references were computed in cubic boxes with 20 and 24 Å of padding, " +
  "the reference energy changing by 0.3 meV between them."));
add(EN("Adsorption configurations were pre-screened over seven surface sites and 48 molecular " +
  "orientations with the UMA-s-1p1 machine-learned interatomic potential, relaxing the " +
  "adsorbate together with the outermost 15 % of the slab. The DFT energies reported here " +
  "are static single points on those machine-learned geometries and are not DFT local " +
  "minima; identical fixed geometries and an identical computational protocol were used for " +
  "every species, so that the comparison is made at matched geometry rather than at matched " +
  "relaxation."));
add(EN("The magnetic state of the slab was declared rather than optimised. Each calculation " +
  "started from a collinear antiferromagnetic configuration of the 48 Ni sites (24 up, " +
  "24 down, ±1 μB initial moments) with the total moment left unconstrained in the " +
  "complexes, the clean slab and the gas-phase references alike, so that no species was " +
  "constrained relative to another. The realised site-projected moments were recorded for " +
  "every calculation, and energies were differenced only between calculations that realised " +
  "the same magnetic configuration."));
add(EN("Adsorption energies were obtained as   E_ads = E_slab+adsorbate − E_slab − E_adsorbate.   (1)"));
add(EN("Limitations. These are vacuum, 0 K, single-molecule quantities evaluated on fixed, " +
  "machine-learned geometries. They are not adhesion energies, interfacial resistances or " +
  "coverage-dependent quantities, and the two adsorbates are molecular segments rather than " +
  "polymers — a real polymer chain contacts the surface at many points simultaneously. " +
  "Total energies are code- and pseudopotential-specific and are meaningful only as internal " +
  "differences within this study. The spectroscopic evidence indicates that the " +
  "as-synthesised SDCP is self-doped, whereas the adsorption model is the neutral repeat " +
  "unit; the spin distribution of the doped state is moreover chain-length dependent."));

// ══════════════════════════════════════════════════════ 3
add(H1("3. Methods — DFT · 압축형 (Compact)"));
add(P("같은 사실을 담되 문장 수만 줄인 판입니다. 한정어는 하나도 빼지 않았습니다 — " +
      "압축은 문장을 줄이는 것이지 유보를 빼는 것이 아닙니다.", {color: MUT}));
add(EN("DFT calculations. Spin-polarised DFT calculations were performed with VASP (PAW, PBE) " +
  "using Grimme D3 dispersion in the zero-damping form, a Dudarev +U correction of " +
  "U − J = 6.2 eV on the Ni 3d states, a 520 eV cut-off, 1 × 10⁻⁶ eV convergence, 0.05 eV " +
  "Gaussian smearing and real-space projection disabled. The NCM811 surface was modelled as " +
  "a LiNiO₂(104) slab (1 × 4, four layers, 192 atoms, 18.27 × 11.51 Å in plane) with more " +
  "than 15 Å of vacuum, a Γ-centred 3 × 4 × 1 mesh and a dipole correction along the surface " +
  "normal; SDCP was represented by its sulfonate-functionalised EDOT repeat unit " +
  "(C₁₁H₁₆O₆S₂) and PTFE by a C₁₀F₂₂ segment, with gas-phase references in 20 and 24 Å boxes " +
  "(0.3 meV apart)."));
add(EN("Adsorption geometries were pre-screened over seven sites and 48 orientations with the " +
  "UMA-s-1p1 machine-learned potential; the reported DFT energies are static single points " +
  "on those geometries and are not DFT minima, the same fixed geometry and protocol being " +
  "used for every species. The slab magnetic state was declared rather than optimised " +
  "(collinear antiferromagnetic, 24 ↑ / 24 ↓ Ni, ±1 μB initial moments, total moment " +
  "unconstrained for complexes, clean slab and gas references alike); realised moments were " +
  "recorded and energies differenced only between calculations that realised the same " +
  "configuration. Adsorption energies follow E_ads = E_slab+adsorbate − E_slab − E_adsorbate."));
add(EN("These are vacuum, 0 K, single-molecule quantities on fixed machine-learned geometries — " +
  "not adhesion energies, interfacial resistances or coverage-dependent quantities — and the " +
  "adsorbates are molecular segments rather than polymers. Total energies are code- and " +
  "pseudopotential-specific and meaningful only as internal differences. The as-synthesised " +
  "SDCP is self-doped by the spectroscopic evidence, whereas the adsorption model is the " +
  "neutral repeat unit."));

// ══════════════════════════════════════════════════════ 4
add(H1("4. Table S1 — 전면 교체 (값은 배포 입력파일 실물)"));
add(P("아래 값은 실제로 배포되는 계산 입력에서 그대로 읽은 것입니다. 공란 없음.", {color: MUT}));
add(table([1700, 3500, 3800], [
  ["Category", "Parameter", "Value"],
  ["Method", "Code / functional", "VASP (PAW); PBE"],
  ["", "Dispersion", "Grimme D3, zero damping"],
  ["", "Hubbard correction", "Dudarev, U − J = 6.2 eV on Ni 3d"],
  ["", "Plane-wave cut-off", "520 eV"],
  ["", "Electronic convergence", "1 × 10⁻⁶ eV"],
  ["", "Smearing (Gaussian)", "0.05 eV"],
  ["", "Real-space projection", "off"],
  ["", "k-point mesh (slab / molecule)", "3 × 4 × 1 / Γ"],
  ["Surface model", "Slab", "LiNiO₂(104), 1 × 4, four layers, 192 atoms (Li₄₈Ni₄₈O₉₆)"],
  ["", "Cell (in-plane)", "18.27 × 11.51 Å"],
  ["", "Adsorbate–image separation", "> 15 Å"],
  ["", "Dipole correction", "along surface normal"],
  ["Magnetic state", "Starting configuration", "collinear AFM, 24 ↑ / 24 ↓ Ni, ±1 μB"],
  ["", "Total-moment constraint", "none — for complexes, slab and gas references alike"],
  ["", "Reported", "realised site-projected moments per calculation"],
  ["Geometry", "Source", "UMA-s-1p1 relaxation, outer 15 % of slab free"],
  ["", "DFT treatment", "static single point — not a DFT minimum"],
  ["Adsorbate", "SDCP repeat unit (neutral)", "C₁₁H₁₆O₆S₂"],
  ["", "PTFE segment", "C₁₀F₂₂"],
  ["", "Gas-phase box padding", "20 and 24 Å (ΔE = 0.3 meV)"],
  ["Search", "Potential; sites / orientations", "UMA-s-1p1; 7 / 48"],
  ["Adsorption energy", "Definition", "Equation (1)"]]));
add(P("표에서 빼면 안 되는 세 줄입니다 — 심사에서 반드시 확인하는 항목입니다: " +
      "기하가 DFT 최소점이 아니라는 것 · 자기 상태가 선언이라는 것 · " +
      "기준계와 복합체가 같은 구속 정책을 쓴다는 것.", {color: MUT}));

// ══════════════════════════════════════════════════════ 5
add(H1("5. 본문 34 (DFT 문단) — 교체안"));
add(P("아래를 그대로 넣고, 대괄호 한 자리만 나중에 채웁니다.", {color: MUT}));
add(EN("Density functional theory calculations were used to compare how the two binder " +
  "chemistries interact with the active material surface (Figure 2e), with the computational " +
  "model and parameters given in Figure S3 and Table S1. Representative segments of SDCP and " +
  "of PTFE were placed on a LiNiO₂(104) surface, the adsorption geometry of each being " +
  "selected by a machine-learned potential over seven surface sites and 48 orientations and " +
  "then evaluated by DFT at fixed geometry, so that both species are compared under an " +
  "identical protocol."));
add(new Paragraph({spacing: {after: 140, line: 300}, indent: {left: 340},
  border: {left: {style: BorderStyle.SINGLE, size: 14, color: RED, space: 12}},
  children: [R("[ A ]  ", {bold: true, color: RED}),
             R("Across the four pre-registered poses of each segment, the lowest adsorption " +
               "energy of the SDCP repeat unit was ", {italics: true}),
             R("[ ___ ] eV", {bold: true, color: RED}),
             R(" lower than that of the C₁₀F₂₂ segment.", {italics: true})]}));
add(EN("The calculations describe an isolated repeat unit on a clean, vacuum-terminated surface " +
  "at 0 K and are therefore a statement about local chemical affinity rather than about " +
  "adhesion of the processed electrode."));

add(H2("삭제해야 하는 문장"));
add(P([R("v6 원문: ", {color: MUT}),
       R("\"The stronger interaction expected for SDCP originates from its polar sulfonate " +
         "moieties, which can interact more effectively with exposed surface sites of NCM811 " +
         "than non-polar PTFE.\"", {italics: true})]));
add(P([R("→ 삭제합니다. ", {bold: true, color: RED}),
       R("계산이 그 기전을 보이지 않습니다. 평가된 기하에서 분자와 표면의 실제 최근접 접촉은 " +
         "탄화수소 C–H 와 표면 O/Ni 사이 2.44 Å 이고, 종전에 근거로 쓰던 술포네이트 O–Li 근접은 " +
         "재측정에서 4.9–5.4 Å 로 나왔습니다. 술포네이트의 역할은 별도 근거(분광·분산)로 " +
         "말해야 하며, 흡착 계산이 그것을 뒷받침하지 않습니다.")]));
add(P([R("자리표시자도 함께 삭제: ", {color: MUT}),
       R("\"Additional text related to DFT.\"", {italics: true})]));

// ══════════════════════════════════════════════════════ 6
add(H1("6. 캡션 — 교체안"));
add(table([1900, 7100], [
  ["위치", "교체안 (영문)"],
  ["Figure 2(e)", "Adsorption of representative SDCP and PTFE segments on a LiNiO₂(104) surface, evaluated by DFT at machine-learned geometries."],
  ["Figure S3", "Computational models used for the DFT calculations: the LiNiO₂(104) slab, the SDCP repeat unit (C₁₁H₁₆O₆S₂) and the C₁₀F₂₂ segment, with the adsorption geometry of each species."],
  ["Figure 4(a)", "DEM-packed and MPM-compacted electronic conduction networks of the SBE and DBE."],
  ["Figure 4(b)", "Effective electronic conductivities of the SBE and DBE under the two binder conventions, each averaged over the eight prescribed grid-origin phases."]]));
add(P("v6 의 \"(e) DFT.\" 와 \"Figure S3. DFT\" 는 자리표시자입니다.", {color: MUT}));

// ══════════════════════════════════════════════════════ 7
add(H1("7. 무엇을 주장할 수 있고 무엇은 못 하나"));
add(P("계산이 끝난 뒤에도 아래 구분은 그대로입니다. 미리 정해 둡니다.", {color: MUT}));
add(table([4700, 1500, 2800], [
  ["원고에 쓰려는 문장", "가능", "이유"],
  ["SDCP 조각이 PTFE 조각보다 표면에 더 세게 붙는다", "가능", "사전등록한 비교량이며 두 조각이 같은 프로토콜입니다"],
  ["흡착에너지 절대값 (−0.X eV)", "조건부", "\"기계학습 기하 위의 단일점\" 을 반드시 함께 적을 때만"],
  ["SDCP 가 Li 자리를 선호한다", "불가", "자리 간 차이가 판정 해상도(30 meV) 아래입니다"],
  ["술포네이트가 표면에 앵커링한다", "불가", "실제 최근접 접촉이 C–H 이고 기전 근거가 없습니다"],
  ["자가도핑 상태의 흡착", "불가", "이번 계산은 중성 반복단위만 다룹니다"],
  ["전역 최소 자세 / \"항상\"", "불가", "자세를 전수로 보지 않았습니다"]]));

// ══════════════════════════════════════════════════════ 8
add(H1("8. DEM 축 (Table S2 · S3 · Figure 4)"));
add(P("이 부분은 별도 트랙에서 관리되며, v7 문서의 서술이 그대로 유효합니다. " +
      "이 문서에서는 공란 상태만 적어 둡니다.", {color: MUT}));
add(table([3000, 2200, 3800], [
  ["행", "상태", "비고"],
  ["σ_ele (두 규약)", "확정", "본문과 Table S3 에 실을 수 있습니다"],
  ["구조 지표 5행", "확정", "절대값이 v6 과 다릅니다 — 규약을 함께 적어야 합니다"],
  ["σ_ion", "공란", "값이 나왔으나 입력 규약 문제로 사용할 수 없습니다"],
  ["Areal capacity", "공란", "비용량(mAh g⁻¹) 회신이 필요합니다"],
  ["Figure 4(b)", "확정", "두 규약 병기로 재작도되었습니다"]]));

// ══════════════════════════════════════════════════════ 9
add(H1("9. 일정"));
add(table([3400, 2400, 3200], [
  ["단계", "소요", "비고"],
  ["계산 제출 준비", "진행 중", "입력 42건 · 검증 절차 정리 중"],
  ["계산 실행", "약 3–4일", "동시 실행 10건 이상이면 3일, 8건이면 4일에 가깝습니다"],
  ["결과 회수 · 판독", "1일", "그 뒤 [ A ] 한 자리를 채우면 §5 가 완성됩니다"]]));
add(P("⚠ 이 문서의 다른 모든 문장은 계산 결과와 무관하게 지금 확정입니다. " +
      "기다리는 것은 §5 의 대괄호 한 자리뿐입니다.", {bold: true}));

const doc = new Document({
  styles: {default: {document: {run: {font: "Malgun Gothic", size: 20, color: INK}}}},
  sections: [{properties: {page: {margin: {top: 1300, right: 1440, bottom: 1300, left: 1440}}},
              children: kids}]});
Packer.toBuffer(doc).then(b => {fs.writeFileSync("Methods_simulation_v8_for_coauthors.docx", b);
                               console.log("written", b.length, "bytes");});

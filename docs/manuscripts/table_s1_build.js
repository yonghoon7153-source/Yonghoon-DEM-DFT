// table_s1_build.js — Table S1 (흡착에너지 DFT 파라미터) docx 생성
//   node table_s1_build.js            → Table_S1_DFT_parameters.docx
//
// ⚠ 2026-09-08 수정 3건 (원본 대비)
//   ① 제목을 좁혔다 — 논문에 DFT 가 둘(QE 슬랩 + ORCA 분자)인데 이 표는 슬랩·흡착만 담는다.
//   ② **Adsorbate 행에서 자가도핑형을 뺐다.** db/properties/sdcp_doped_closed_2026_08_28.json
//      (상태 active)이 자가도핑 단량체의 표면 흡착 수치 전부를 닫았다. 표에 두 형태를 나란히
//      두면 마감된 결과를 암묵적으로 주장하게 된다. 부수 효과로 C₁₁H₁₇O₆S₂(H 가 늘어난 표기)
//      오류도 함께 사라진다.
//   ③ 각주로 분자 계산을 Supplementary Note 2 로 넘긴다.
//
// ⛔ 이 스크립트가 못 하는 것: 값의 물리적 검증. 표기와 범위만 다룬다.
//    ⏳ 확인 필요 — Ref. 번호(본문은 [49,50], 표는 48/49) · 슬랩 조성식 Li₄₈Ni₄₈O₉₆.
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, ShadingType, BorderStyle } = require("docx");
const fs = require("fs");

const W = 9360;
const COL = [1450, 2500, 3050, 860, 1500];
const HDR = "D9E2F3";

function cell(text, { bold = false, shade = null, width, size = 17 } = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: shade, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({
      spacing: { before: 0, after: 0 },
      children: [new TextRun({ text, bold, size, font: "Times New Roman" })],
    })],
  });
}

// row(category, parameter, value, unit, source) — category 는 그룹 첫 행에만 적는다
const row = (c, pm, v, u, s, opt = {}) =>
  new TableRow({ children: [c, pm, v, u, s].map((t, i) => cell(t, { ...opt, width: COL[i] })) });

const p = (text, o = {}) => new Paragraph({
  spacing: { before: o.before ?? 0, after: o.after ?? 110, line: 280 },
  children: [new TextRun({ text, size: o.size ?? 18, bold: o.bold, font: "Times New Roman" })],
});

const rows = [
  row("Category", "Parameter", "Value", "Unit", "Source", { bold: true, shade: HDR }),

  row("Method", "Code / functional", "Quantum ESPRESSO; PBE", "–", "Ref. 48, S1"),
  row("", "Dispersion / Hubbard U (Ni 3d)", "Grimme D3; 6.2 eV", "–", "Ref. S2, 49"),
  row("", "Cut-off (wavefunction / charge density)", "60 / 480", "Ry", "–"),
  row("", "Smearing (Gaussian)", "0.05", "eV", "–"),
  row("", "Convergence (SCF / force)", "1 × 10⁻⁶ Ry / 1 × 10⁻³ Ry bohr⁻¹", "–", "–"),
  row("", "k-point mesh (slab / check / molecule)", "2 × 3 × 1 / 3 × 4 × 1 / Γ", "–", "Γ-centered"),

  row("Surface model", "Slab", "LiNiO₂(104), 1 × 4, four layers, 192 atoms (Li₄₈Ni₄₈O₉₆)", "–", "–"),
  row("", "Cell (in-plane × height)", "18.27 × 11.51 × 30.26", "Å", "–"),
  row("", "Adsorbate–image separation", "> 15", "Å", "–"),
  row("", "Constrained atoms", "144 (z ≤ 17.40 Å)", "–", "–"),
  row("", "Magnetic configuration", "Antiferromagnetic (net 0); Ni 1.02 μB", "–", "–"),
  row("", "Dipole correction", "Along surface normal", "–", "–"),

  // ⚠ 자가도핑형은 여기 없다 (마감 범위) — 분자 계산 쪽에만 등장한다
  row("Adsorbate", "SDCP repeat unit (neutral)", "C₁₁H₁₆O₆S₂", "–", "–"),
  row("", "PTFE segment", "C₁₀F₂₂", "–", "–"),
  row("", "Gas-phase reference box padding", "20 and 24", "Å", "–"),

  row("Configuration search", "Potential; sites / orientations; force",
      "UMA-s-1p1; 7 / 48; 0.05 eV Å⁻¹", "–", "Ref. S3"),
  row("Adsorption energy", "Definition", "Equation (1)", "eV", "–"),
];

const doc = new Document({
  styles: { default: { document: { run: { font: "Times New Roman", size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
                          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children: [
      p("Table S1. Parameters used for the adsorption-energy DFT calculations.",
        { bold: true, size: 19, after: 180 }),

      new Table({
        width: { size: W, type: WidthType.DXA },
        columnWidths: COL,
        borders: {
          top:    { style: BorderStyle.SINGLE, size: 6, color: "808080" },
          bottom: { style: BorderStyle.SINGLE, size: 6, color: "808080" },
          left:   { style: BorderStyle.NONE },
          right:  { style: BorderStyle.NONE },
          insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "BFBFBF" },
          insideVertical:   { style: BorderStyle.NONE },
        },
        rows,
      }),

      p("", { after: 140 }),
      p("Parameters for the molecular (oligomer) calculations are given in Supplementary Note 2.",
        { size: 16, after: 160 }),
    ],
  }],
});

const OUT = process.env.TABLE_S1_OUT || "Table_S1_DFT_parameters.docx";
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(OUT, b); console.log(`wrote ${OUT}`); });

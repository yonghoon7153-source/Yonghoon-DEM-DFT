// sdcp_dft_methods_build.js — SDCP 원고 v5 의 DFT 부분만 Word 로 뽑는다.
//   ① 본문 Experimental section 삽입문단  *Computational details*:
//   ② SI  Table S1. Parameters used for the DFT calculations
// 형식은 `Methodology 참고자료.docx` 기준 (Times New Roman · 이탤릭 lead-in + 콜론 ·
// 표 Category|Parameter|Value|Unit|Source · SI 인용은 Ref. S 계열).
// 수치 출처: sdcp_wave1_2026_08_12 번들 (MANIFEST.json · INCAR · KPOINTS · POSCAR 실측).
// 근거·인용 제약: docs/manuscripts/sdcp_dft_methods_draft_2026_08_23.md
//
// Table S1 각주 a (단일점·k 범위) 는 2026-08-23 사용자 결정으로 **뺐다** — 내부 보관:
//   kb/syntheses/sdcp_eads_revision_defense_2026_08_23.md (리비전 회신 문구 포함)
// 이 스크립트가 못 하는 것: E_ads 수치를 채우지 않는다 (wave1 미회수).
//   Table S1 은 '조건' 표이고 결과값 표가 아니다.
//
//   NODE_PATH=<docx 설치 경로> SDCP_DFT_OUT=<폴더> node docs/manuscripts/sdcp_dft_methods_build.js
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, ShadingType, BorderStyle, PageBreak, PositionalTab,
        PositionalTabAlignment, PositionalTabLeader, PositionalTabRelativeTo } = require("docx");
const fs = require("fs");
const path = require("path");

const W = 9360;                                  // Letter 여백 안에 맞는 표 전체 폭 (DXA)
const COL = [1500, 2760, 3200, 800, 1100];       // 합 = W
const HDR = "D9E2F3";
const FONT = "Times New Roman";

// 미니 리치텍스트: *이탤릭* · ~아래첨자~ · ^위첨자^
function runs(text, { bold = false, size = 18 } = {}) {
  const out = [];
  const re = /(\*[^*]+\*|~[^~]+~|\^[^^]+\^)/g;
  let last = 0, m;
  const push = (t, o) => { if (t) out.push(new TextRun({ text: t, bold, size, font: FONT, ...o })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index));
    const tok = m[0], inner = tok.slice(1, -1);
    if (tok[0] === "*") push(inner, { italics: true });
    else if (tok[0] === "~") push(inner, { subScript: true });
    else push(inner, { superScript: true });
    last = re.lastIndex;
  }
  push(text.slice(last));
  return out;
}

// 별행 수식 + 오른쪽 끝 번호 — 원고의 (1)·(2) 와 같은 모양
function eq(text, num, o = {}) {
  return new Paragraph({
    spacing: { before: o.before ?? 160, after: o.after ?? 160, line: 300 },
    indent: { left: 720 },
    children: [
      ...runs(text, { size: o.size ?? 20 }),
      new TextRun({ children: [new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.NONE,
      })] }),
      ...runs("(" + num + ")", { size: o.size ?? 20 }),
    ],
  });
}

const p = (text, o = {}) => new Paragraph({
  spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 300 },
  alignment: o.alignment,
  children: runs(text, { bold: o.bold, size: o.size ?? 20 }),
});

function cell(text, { bold = false, shade = null, width, size = 18 } = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: shade, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: runs(text, { bold, size }) })],
  });
}
const row = (cells, opt = {}) =>
  new TableRow({ children: cells.map((t, i) => cell(t, { ...opt, width: COL[i] })) });

// ── 본문 삽입 문단 ────────────────────────────────────────────────────────
const METHODS = [
  "*Computational details*: Spin-polarised density functional theory (DFT) calculations were ",
  "performed with Quantum ESPRESSO [ref] using the Perdew–Burke–Ernzerhof functional, Grimme D3 ",
  "dispersion, and a Hubbard correction of *U* = 6.2 eV on the Ni 3*d* states. Wave functions ",
  "and the charge density were expanded to 60 and 480 Ry, respectively, with Gaussian smearing ",
  "of 0.05 eV and a self-consistency threshold of 1 × 10^−6^ Ry. The NCM811 surface was modelled ",
  "as an antiferromagnetic LiNiO~2~(104) slab (1 × 4, four layers, 192 atoms, 18.27 × 11.51 Å in ",
  "plane) with more than 15 Å of vacuum, sampled with a Γ-centred 2 × 3 × 1 mesh and a dipole ",
  "correction along the surface normal. SDCP was represented by its sulfonate-functionalised ",
  "EDOT repeat unit (C~11~H~16~O~6~S~2~; the self-doped form C~11~H~15~O~6~S~2~ was obtained by ",
  "removing the sulfonate proton) and PTFE by a C~10~F~22~ segment. Adsorption configurations ",
  "were pre-screened over seven surface sites and 48 molecular orientations with a ",
  "machine-learned interatomic potential [ref], and the lowest-energy configuration of each ",
  "species on the surface Li and Ni sites was evaluated by DFT. Gas-phase references were ",
  "relaxed at the Γ point in the same cell until residual forces fell below 1 × 10^−3^ Ry ",
  "bohr^−1^, with the box padding increased from 20 to 24 Å to confirm convergence. Adsorption ",
  "energies were obtained as",
].join("");

// 원고 본문은 DEM 절에서 (1)·(2) 를 이미 쓴다 → DFT 수식은 **(3)**.
const EQ_NUM = "3";
const EQ = "*E*~ads~ = *E*(slab+molecule) − *E*(slab) − *E*(molecule)";
const EQ_WHERE =
  "where *E*(slab+molecule), *E*(slab), and *E*(molecule) are the total energies of the "
  + "adsorbed complex, the clean slab, and the isolated molecule, respectively, all computed "
  + "with identical settings and the same antiferromagnetic configuration.";

// ── 그림 캡션 (현재 원고에 'DFT' 한 단어만 있는 자리) ────────────────────
const CAPTIONS = [
  ["Figure 2e", "Calculated adsorption energies of the SDCP repeat unit and a PTFE segment "
    + "on the LiNiO~2~(104) surface. ⟨values to be inserted⟩"],
  ["Figure S3", "Computational models used for the DFT calculations: the LiNiO~2~(104) slab "
    + "and the adsorbed SDCP (neutral and self-doped) and PTFE segments."],
];

// ── Table S1 ─────────────────────────────────────────────────────────────
const ROWS = [
  ["Method", "Code / functional", "Quantum ESPRESSO; PBE", "-", "Ref. S1, S2"],
  ["", "Dispersion / Hubbard *U* (Ni 3*d*)", "Grimme D3; 6.2 eV", "-", "Ref. S3, S4"],
  ["", "Cutoff (wavefunction / charge density)", "60 / 480", "Ry", "-"],
  ["", "Smearing (Gaussian)", "0.05", "eV", "-"],
  ["", "Convergence (SCF / force)",
   "1 × 10^−6^ Ry / 1 × 10^−3^ Ry bohr^−1^", "-", "-"],
  ["", "*k*-point mesh (slab / check / molecule)",
   "2 × 3 × 1 / 3 × 4 × 1 / Γ", "-", "Γ-centred"],
  ["Surface model", "Slab",
   "LiNiO~2~(104), 1 × 4, four layers, 192 atoms (Li~48~Ni~48~O~96~)", "-", "-"],
  ["", "Cell (in-plane × height)", "18.27 × 11.51 × 30.26", "Å", "-"],
  ["", "Adsorbate–image separation", "> 15", "Å", "-"],
  ["", "Constrained atoms", "144 (*z* ≤ 17.40 Å)", "-", "-"],
  ["", "Magnetic configuration", "Antiferromagnetic (net 0); Ni 1.02 μ~B~", "-", "Ref. S5"],
  ["", "Dipole correction", "Along surface normal", "-", "-"],
  ["Adsorbate", "SDCP repeat unit (neutral / self-doped)",
   "C~11~H~16~O~6~S~2~ / C~11~H~15~O~6~S~2~", "-", "-"],
  ["", "PTFE segment", "C~10~F~22~", "-", "-"],
  ["", "Gas-phase reference box padding", "20 and 24", "Å", "-"],
  ["Configuration search", "Potential; sites / orientations; force",
   "UMA-s-1p1; 7 / 48; 0.05 eV Å^−1^", "-", "Ref. S6"],
  ["Adsorption energy", "Definition", "Equation (3)", "eV", "-"],
];

const REFS = [
  "[S1] P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, "
  + "G. L. Chiarotti, M. Cococcioni, I. Dabo, A. Dal Corso, S. de Gironcoli, S. Fabris, G. Fratesi, "
  + "R. Gebauer, U. Gerstmann, C. Gougoussis, A. Kokalj, M. Lazzeri, L. Martin-Samos, N. Marzari, "
  + "F. Mauri, R. Mazzarello, S. Paolini, A. Pasquarello, L. Paulatto, C. Sbraccia, S. Scandolo, "
  + "G. Sclauzero, A. P. Seitsonen, A. Smogunov, P. Umari, R. M. Wentzcovitch, QUANTUM ESPRESSO: "
  + "a modular and open-source software project for quantum simulations of materials, "
  + "J. Phys.: Condens. Matter 21 (2009) 395502.",
  "[S2] J. P. Perdew, K. Burke, M. Ernzerhof, Generalized gradient approximation made simple, "
  + "Phys. Rev. Lett. 77 (1996) 3865–3868.",
  "[S3] S. Grimme, J. Antony, S. Ehrlich, H. Krieg, A consistent and accurate ab initio "
  + "parametrization of density functional dispersion correction (DFT-D) for the 94 elements "
  + "H-Pu, J. Chem. Phys. 132 (2010) 154104.",
  "[S4] ── TO BE SUPPLIED: source for U(Ni 3d) = 6.2 eV in LiNiO2.",
  "[S5] ── TO BE SUPPLIED: source for the antiferromagnetic ordering of LiNiO2.",
  "[S6] B. M. Wood, M. Dzamba, X. Fu, M. Gao, M. Shuaibi, L. Barroso-Luque, K. Abdelmaqsoud, "
  + "V. Gharakhanyan, J. R. Kitchin, D. S. Levine, K. Michel, A. Sriram, T. S. Cohen, A. Das, "
  + "S. J. Sahoo, A. Rizvi, Z. W. Ulissi, C. L. Zitnick, UMA: A family of universal models for "
  + "atoms, Adv. Neural Inf. Process. Syst. 38 (2025) 143528–143564.",
];

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
                          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children: [
      p("Manuscript — Experimental section", { bold: true, size: 22, after: 60 }),
      p("Insert after the “Discrete element method” paragraph, replacing the "
        + "placeholder “Computational details: DFT”. Equations (1) and (2) are already used by "
        + "the discrete-element section, so the adsorption-energy expression is numbered (3).",
        { size: 17, after: 200 }),
      p(METHODS, { after: 0, line: 360 }),
      eq(EQ, EQ_NUM),
      p(EQ_WHERE, { after: 200, line: 360 }),

      new Paragraph({ children: [new PageBreak()] }),

      p("Supporting Information", { bold: true, size: 22, after: 200 }),
      p("**Table S1.** Parameters used for the DFT calculations.".replace(/\*\*/g, ""),
        { bold: true, size: 19, after: 160 }),

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
        rows: [
          row(["Category", "Parameter", "Value", "Unit", "Source"], { bold: true, shade: HDR }),
          ...ROWS.map((r) => row(r)),
        ],
      }),

      p("", { after: 120 }),
      p("Figure captions (DFT panels)", { bold: true, size: 18, after: 80 }),
      ...CAPTIONS.flatMap(([k, v]) => [p(k + ". " + v, { size: 17, after: 60 })]),
      p("", { after: 140 }),

      p("References", { bold: true, size: 18, after: 80 }),
      ...REFS.map((r) => p(r, { size: 16, after: 40 })),
    ],
  }],
});

const out = path.join(process.env.SDCP_DFT_OUT || ".", "SDCP_DFT_methods_TableS1.docx");
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(out, b); console.log("wrote " + out); });

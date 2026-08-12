const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, ShadingType, BorderStyle } = require("docx");
const fs = require("fs");

const W = 9360;                        // total table width (DXA), fits Letter margins
const COL = [2280, 3540, 3540];
const HDR = "D9E2F3";

function cell(text, { bold = false, shade = null, width, span = 1, size = 18 } = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    columnSpan: span,
    shading: shade ? { type: ShadingType.CLEAR, fill: shade, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({
      spacing: { before: 0, after: 0 },
      children: [new TextRun({ text, bold, size, font: "Times New Roman" })],
    })],
  });
}

// row(label, a, b)  -> three cells;  row(label, shared) -> value spans both system columns
function row(label, a, b, opt = {}) {
  const cells = [cell(label, { ...opt, width: COL[0] })];
  if (b === undefined) cells.push(cell(a, { ...opt, width: COL[1] + COL[2], span: 2 }));
  else cells.push(cell(a, { ...opt, width: COL[1] }), cell(b, { ...opt, width: COL[2] }));
  return new TableRow({ children: cells });
}

const p = (text, o = {}) => new Paragraph({
  spacing: { before: o.before ?? 0, after: o.after ?? 110, line: 280 },
  children: [new TextRun({ text, size: o.size ?? 18, bold: o.bold, font: "Times New Roman" })],
});

const rows = [
  row("Parameter", "Li₃N(001)", "LiC₆(0001)", { bold: true, shade: HDR }),

  row("Code / functional", "Quantum ESPRESSO 7.4.1 (pw.x); PBE"),
  row("Pseudopotentials", "Li, N: ultrasoft", "Li: ultrasoft; C: PAW"),
  row("Cutoff (wavefunction / charge density)", "60 / 480 Ry"),
  row("k-point mesh", "2 × 2 × 1 (Γ-centred)"),
  row("Smearing", "Marzari–Vanderbilt, 0.01 Ry"),
  row("Convergence (SCF / force)", "1 × 10⁻⁶ Ry / 1 × 10⁻³ Ry bohr⁻¹"),

  row("Slab model",
      "α-Li₃N, 3 × 3; four Li₂N and three Li planes, Li₂N (N-exposed) termination; 135 atoms + 1 Li adatom",
      "Stage-1 LiC₆, √3 × √3 R30°, 2 × 2 × 2; graphene-terminated; 108 atoms + 1 Li adatom"),
  row("Cell / vacuum",
      "a = b = 10.95 Å, c = 28.545 Å, γ = 120°; 15.7 Å vacuum",
      "15 Å vacuum"),
  row("Fixed atoms", "Bottom two Li₂N/Li bilayers", "Bottom 50 % of the slab"),

  row("Migration path",
      "Constrained relaxation: adatom lateral (x, y) coordinates fixed; its height and all unconstrained atoms relaxed independently",
      "CI-NEB with the UMA-oc20 machine-learned potential (7 images, IDPP initial path, 0.05 eV Å⁻¹), then DFT single-point energies on those geometries"),
  row("Barrier definition",
      "E(saddle-region configuration) − E(relaxed adsorption minimum)",
      "E(highest-energy image) − E(initial adsorption minimum)"),
];

const doc = new Document({
  styles: { default: { document: { run: { font: "Times New Roman", size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
                          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children: [
      p("Table S2. Computational parameters for the DFT calculations of Li-adatom migration on the Li₃N(001) and LiC₆(0001) surfaces.",
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
      p("Both surfaces use identical electronic-structure settings, so the two barriers are directly comparable. On Li₃N(001) the pronounced adsorbate-induced relaxation of the soft ionic surface destabilised elastic-band calculations, so the barrier was evaluated from two independently converged constrained relaxations instead.",
        { after: 110 }),
      p("The LiC₆(0001) energies are DFT single points on machine-learned-potential geometries; because such potentials smooth the transition state, the LiC₆ barrier — and hence the barrier ratio quoted in the main text — is a conservative lower bound."),
    ],
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-12bc-5a75-994e-7718d79c71ba/scratchpad/Table_S2_DFT_parameters.docx", b);
  console.log("wrote Table_S2_DFT_parameters.docx");
});

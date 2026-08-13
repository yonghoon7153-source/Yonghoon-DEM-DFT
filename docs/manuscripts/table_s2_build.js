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

  row("Code / functional", "Quantum ESPRESSO 7.4.1 (pw.x) [1]; PBE [2]"),
  row("Pseudopotentials", "Li, N: ultrasoft", "Li: ultrasoft; C: PAW"),
  row("Cutoff (wavefunction / charge density)", "60 / 480 Ry"),
  row("k-point mesh", "2 × 2 × 1 (Γ-centred)"),
  row("Smearing", "Marzari–Vanderbilt, 0.01 Ry [3]"),
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
      "CI-NEB [4] with the UMA-oc20 machine-learned potential [6] (7 images, IDPP initial path [5], 0.05 eV Å⁻¹) as implemented in ASE [7], then DFT single-point energies on those geometries"),
  row("Barrier definition",
      "E(saddle-region configuration) − E(relaxed adsorption minimum)",
      "E(highest-energy image) − E(initial adsorption minimum)"),
  row("Migration barrier", "0.118 eV", "0.290 eV", { bold: true }),
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
      p("The LiC₆(0001) energies are DFT single points on machine-learned-potential geometries; because such potentials smooth the transition state, the LiC₆ barrier — and hence the barrier ratio quoted in the main text — is a conservative lower bound. The Li₃N(001) value of 0.118 eV agrees with the 0.133 eV reported for the same surface in ref. [8].",
        { after: 160 }),

      p("References", { bold: true, size: 18, after: 80 }),
      p("[1] P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, A. Dal Corso, S. de Gironcoli, S. Fabris, G. Fratesi, R. Gebauer, U. Gerstmann, C. Gougoussis, A. Kokalj, M. Lazzeri, L. Martin-Samos, N. Marzari, F. Mauri, R. Mazzarello, S. Paolini, A. Pasquarello, L. Paulatto, C. Sbraccia, S. Scandolo, G. Sclauzero, A. P. Seitsonen, A. Smogunov, P. Umari, R. M. Wentzcovitch, QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials, J. Phys.: Condens. Matter 21 (2009) 395502. https://doi.org/10.1088/0953-8984/21/39/395502.", { size: 16, after: 40 }),
      p("[2] J. P. Perdew, K. Burke, M. Ernzerhof, Generalized gradient approximation made simple, Phys. Rev. Lett. 77 (1996) 3865–3868. https://doi.org/10.1103/PhysRevLett.77.3865.", { size: 16, after: 40 }),
      p("[3] N. Marzari, D. Vanderbilt, A. De Vita, M. C. Payne, Thermal contraction and disordering of the Al(110) surface, Phys. Rev. Lett. 82 (1999) 3296–3299. https://doi.org/10.1103/PhysRevLett.82.3296.", { size: 16, after: 40 }),
      p("[4] G. Henkelman, B. P. Uberuaga, H. Jónsson, A climbing image nudged elastic band method for finding saddle points and minimum energy paths, J. Chem. Phys. 113 (2000) 9901–9904. https://doi.org/10.1063/1.1329672.", { size: 16, after: 40 }),
      p("[5] S. Smidstrup, A. Pedersen, K. Stokbro, H. Jónsson, Improved initial guess for minimum energy path calculations, J. Chem. Phys. 140 (2014) 214106. https://doi.org/10.1063/1.4878664.", { size: 16, after: 40 }),
      p("[6] B. M. Wood, M. Dzamba, X. Fu, M. Gao, M. Shuaibi, L. Barroso-Luque, K. Abdelmaqsoud, V. Gharakhanyan, J. R. Kitchin, D. S. Levine, K. Michel, A. Sriram, T. S. Cohen, A. Das, S. J. Sahoo, A. Rizvi, Z. W. Ulissi, C. L. Zitnick, UMA: A family of universal models for atoms, Adv. Neural Inf. Process. Syst. 38 (2025) 143528–143564. https://doi.org/10.52202/085713-4310.", { size: 16, after: 40 }),
      p("[7] A. H. Larsen, J. J. Mortensen, J. Blomqvist, I. E. Castelli, R. Christensen, M. Dułak, J. Friis, M. N. Groves, B. Hammer, C. Hargus, E. D. Hermes, P. C. Jennings, P. B. Jensen, J. Kermode, J. R. Kitchin, E. L. Kolsbjerg, J. Kubal, K. Kaasbjerg, S. Lysgaard, J. B. Maronsson, T. Maxson, T. Olsen, L. Pastewka, A. Peterson, C. Rostgaard, J. Schiøtz, O. Schütt, M. Strange, K. S. Thygesen, T. Vegge, L. Vilhelmsen, M. Walter, Z. Zeng, K. W. Jacobsen, The atomic simulation environment—a Python library for working with atoms, J. Phys.: Condens. Matter 29 (2017) 273002. https://doi.org/10.1088/1361-648X/aa680e.", { size: 16, after: 40 }),
      p("[8] M. S. Kim, Z. Zhang, J. Wang, S. T. Oyakhire, S. C. Kim, Z. Yu, Y. Chen, D. T. Boyle, Y. Ye, Z. Huang, W. Zhang, R. Xu, P. Sayavong, S. F. Bent, J. Qin, Z. Bao, Y. Cui, Revealing the multifunctions of Li3N in the suspension electrolyte for lithium metal batteries, ACS Nano 17 (2023) 3168–3180. https://doi.org/10.1021/acsnano.2c12470. (= ref. [54] of the main text)", { size: 16, after: 40 }),
    ],
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-12bc-5a75-994e-7718d79c71ba/scratchpad/Table_S2_DFT_parameters.docx", b);
  console.log("wrote Table_S2_DFT_parameters.docx");
});

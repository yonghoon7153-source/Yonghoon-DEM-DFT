const d = require('docx');
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, AlignmentType, HeadingLevel, ShadingType, BorderStyle,
        TabStopType, TabStopPosition } = d;

const FONT = 'Times New Roman';
const SZ = 21;            // 10.5 pt
const W = 9000;

// ---- inline run helpers -------------------------------------------------
const t  = (s, o={}) => new TextRun({ text: s, font: FONT, size: SZ, ...o });
const i  = (s) => t(s, { italics: true });
const b  = (s) => t(s, { bold: true });
const sup= (s) => t(s, { superScript: true });
const sub= (s) => t(s, { subScript: true });

// parse a mini-markup string into runs:  *ital*  ^sup^  _sub_  **bold**
function runs(str) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|\^[^^]+\^|_[^_]+_)/g;
  let last = 0, m;
  while ((m = re.exec(str)) !== null) {
    if (m.index > last) out.push(t(str.slice(last, m.index)));
    const tok = m[0];
    if (tok.startsWith('**')) out.push(b(tok.slice(2, -2)));
    else if (tok.startsWith('*')) out.push(i(tok.slice(1, -1)));
    else if (tok.startsWith('^')) out.push(sup(tok.slice(1, -1)));
    else out.push(sub(tok.slice(1, -1)));
    last = re.lastIndex;
  }
  if (last < str.length) out.push(t(str.slice(last)));
  return out;
}

const P = (str, o={}) => new Paragraph({
  children: runs(str),
  spacing: { after: 120, line: 300 },
  alignment: AlignmentType.JUSTIFIED, ...o });

// run-in bold heading + body in ONE paragraph (reference-doc style)
const RunIn = (head, body) => new Paragraph({
  children: [ b(head), t(' '), ...runs(body) ],
  spacing: { after: 160, line: 300 },
  alignment: AlignmentType.JUSTIFIED });

const Eq = (eq, num) => new Paragraph({
  children: [ ...runs(eq), t('\t'), t('(' + num + ')') ],
  tabStops: [ { type: TabStopType.RIGHT, position: TabStopPosition.MAX } ],
  spacing: { before: 120, after: 120 },
  alignment: AlignmentType.LEFT,
  indent: { left: 2200 } });

const H = (s, lvl=HeadingLevel.HEADING_1) => new Paragraph({
  children: [ new TextRun({ text: s, font: FONT, size: 24, bold: true }) ],
  heading: lvl, spacing: { before: 300, after: 160 } });

const Cap = (str) => new Paragraph({
  children: runs(str), spacing: { before: 240, after: 100 },
  alignment: AlignmentType.LEFT });

const Note = (str) => new Paragraph({
  children: runs(str).map(r => r),
  spacing: { after: 60 }, indent: { left: 200 },
  alignment: AlignmentType.JUSTIFIED });

// ---- table helpers ------------------------------------------------------
function cell(str, wid, o={}) {
  return new TableCell({
    width: { size: wid, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    columnSpan: o.span,
    shading: o.head ? { type: ShadingType.CLEAR, fill: 'EFEFEF' } : undefined,
    children: [ new Paragraph({
      children: (o.head ? runs(str).map(r => r) : runs(str)),
      alignment: o.center ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing: { after: 0, line: 260 } }) ] });
}
function headCell(str, wid) {
  return new TableCell({
    width: { size: wid, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    shading: { type: ShadingType.CLEAR, fill: 'EFEFEF' },
    children: [ new Paragraph({ children: [ b(str) ],
      alignment: AlignmentType.CENTER, spacing: { after: 0 } }) ] });
}
function mkTable(widths, header, rows, centerFrom=2) {
  const trs = [ new TableRow({ tableHeader: true,
    children: header.map((h, k) => headCell(h, widths[k])) }) ];
  for (const r of rows) {
    const cs = [];
    for (let k = 0; k < r.length; k++) {
      let c = r[k];
      if (typeof c === 'string' && c.startsWith('SPAN:')) {
        cs.push(cell(c.slice(5), widths[k] + widths[k+1],
                     { center: true, span: 2 }));
        k++;  continue;
      }
      cs.push(cell(c, widths[k], { center: k >= centerFrom }));
    }
    trs.push(new TableRow({ children: cs }));
  }
  return new Table({ columnWidths: widths, width: { size: W, type: WidthType.DXA }, rows: trs });
}

// =========================================================================
const body = [];

body.push(new Paragraph({ children: [ new TextRun({
  text: 'DEM / microstructure-modelling sections — revised draft v1',
  font: FONT, size: 28, bold: true }) ], spacing: { after: 80 } }));
body.push(new Paragraph({ children: [ new TextRun({
  text: 'Prepared for merging into Manuscript v5.1 and Supporting Information v5.1. '
      + 'Formatted after "Methodology 참고자료". Open items are listed in Section D.',
  font: FONT, size: 19, italics: true, color: '555555' }) ], spacing: { after: 240 } }));

// ---------------- A. Manuscript -----------------------------------------
body.push(H('A.  Manuscript — 4. Experimental Section'));
body.push(new Paragraph({ children: [ new TextRun({
  text: 'Replaces the single “Discrete element method:” paragraph.',
  font: FONT, size: 19, italics: true, color: '555555' }) ], spacing: { after: 160 } }));

body.push(RunIn('Microstructure reconstruction:',
  'Three-dimensional SBE and DBE microstructures were reconstructed in two stages. '
+ 'Rigid-sphere packing was computed by the discrete element method (DEM) in LIGGGHTS,^[33]^ '
+ 'using 1,271 NCM811 spheres (*r* = 2.5 μm) and 146,420 LPSCl spheres (*r* = 0.5 μm) sized '
+ 'after the experimental powders, mixed at 70:27 by weight in a 50 × 50 μm^2^ domain and '
+ 'compacted under displacement control to 300 MPa. Because rigid-sphere contacts cannot '
+ 'reproduce the plastic flattening, particle rearrangement and grain-boundary sliding that '
+ 'densify sulfide powders, the contact Young’s modulus of LPSCl was softened from the '
+ 'dense-material value of 24 GPa^[34]^ to 1.35 GPa, which reproduces the ~10 % porosity and '
+ '11–12 % contact overlap reported for cold-pressed LPSCl at 300 MPa.^[9]^ Plastic deformation '
+ 'of the electrolyte was then resolved on the fixed DEM skeleton by a GPU-accelerated material '
+ 'point method (MPM)^[35]^ with von Mises plasticity (*E* = 1.53 GPa, *ν* = 0.49, yield strength '
+ '0.30 GPa); the high Poisson’s ratio confines the softening to shear, retaining a dense-solid '
+ 'bulk modulus (*K* = 25.5 GPa) while lowering the shear modulus to *μ* = 0.51 GPa. The two '
+ 'models were calibrated independently against the same experimental porosity rather than '
+ 'against each other. VGCF fibres, PTFE fibrils and SDCP particles were then seeded into the '
+ 'pore space at the experimental weight fractions. All inputs are listed in Table S2. The '
+ 'binder-free NCM811–LPSCl composite compacts to 68.0 μm at 9.8 % porosity, and the SBE and DBE '
+ 'both reach 72.48 μm, at porosities of 7.87 % and 7.39 %, respectively.'));

body.push(RunIn('Effective transport simulations:',
  'Each microstructure was rasterized onto a cubic grid with a voxel edge of 0.15 μm, and the '
+ 'electronic and ionic networks were solved on the same grid. Adjacent conducting voxels were '
+ 'coupled through harmonic-mean conductances and the potential field was obtained from'));
body.push(Eq('∇·(*σ*∇*φ*) = 0', 1));
body.push(P('where *σ* is the local conductivity assigned to each voxel and *φ* is the electric '
+ 'potential. A potential difference was imposed between the separator and current-collector '
+ 'faces of the domain, the remaining boundaries were treated as insulating, and the effective '
+ 'conductivity was obtained from the resulting total current. NCM811, VGCF and SDCP formed the '
+ 'electronic network and LPSCl and SDCP the ionic network, with PTFE insulating in both; the '
+ 'phase conductivities are listed in Table S2. VGCF was assigned a diameter-preserving '
+ 'conductivity so that the axial conductance of a fibre resolved as a one-voxel-wide tube '
+ 'matches that of the 0.15 μm fibre. Because a rasterized conductivity depends on the position '
+ 'of the microstructure relative to the grid, each electrode was solved eight times over a full '
+ 'factorial of half-voxel origin shifts along the three axes; the SBE and DBE were solved on the '
+ 'same set of origins, and conductivity ratios are reported as the paired mean with its standard '
+ 'error. The Joule dissipation of a phase was evaluated as'));
body.push(Eq('*P* = Σ *g*_k_ (Δ*φ*_k_)^2^', 2));
body.push(P('where *g*_k_ and Δ*φ*_k_ are the conductance of and the potential difference across '
+ 'the *k*-th voxel-to-voxel connection and the summation runs over all connections belonging to '
+ 'the phase. Since the electronic conductivity of SDCP has not been measured directly, a '
+ 'representative value of 250 S cm^−1^ was adopted.'));

// ---------------- B. SI tables ------------------------------------------
body.push(H('B.  Supporting Information — tables'));

body.push(Cap('**Table S2.** Material parameters used for the microstructure and transport simulations.'));
{
  const w = [1450, 3150, 1650, 950, 1800];
  const rows = [
   ['Simulation domain','Lateral dimensions','50 × 50','μm^2^','–'],
   ['','Compaction pressure','300','MPa','Experimental value'],
   ['','Voxel edge length','0.15','μm','–'],
   ['NCM811','Particle radius','2.5','μm','Experimental value'],
   ['','Young’s modulus','140','GPa','Ref. [36]'],
   ['','Electronic conductivity','1.0 × 10^−2^','S cm^−1^','Effective value ^a^'],
   ['LPSCl','Particle radius','0.5','μm','Experimental value'],
   ['','Young’s modulus (dense)','24','GPa','Ref. [34]'],
   ['','Young’s modulus (DEM contact)','1.35','GPa','Calibrated ^b^'],
   ['','Young’s modulus (MPM continuum)','1.53','GPa','Calibrated ^b^'],
   ['','Poisson’s ratio (MPM continuum)','0.49','–','Calibrated ^b^'],
   ['','Yield strength','0.30','GPa','Calibrated ^b^'],
   ['','Ionic conductivity (grain interior)','3.0 × 10^−3^','S cm^−1^','Ref. [37]'],
   ['VGCF','Fibre diameter','0.15','μm','Experimental value'],
   ['','Young’s modulus','10','GPa','Assumed'],
   ['','Electronic conductivity (compressed powder)','1.0 × 10^2^','S cm^−1^','Supplier data ^c^'],
   ['','Electronic conductivity (voxel, diameter-preserving)','78.5','S cm^−1^','Calculated value ^c^'],
   ['PTFE','Young’s modulus','0.30','GPa','Assumed ^d^'],
   ['','Electronic / ionic conductivity','0','S cm^−1^','Assumed (insulating)'],
   ['SDCP','Particle diameter','0.30','μm','This work (Figure S5)'],
   ['','Young’s modulus','23.6','GPa','This work (Figure 2g) ^d^'],
   ['','Electronic conductivity','250','S cm^−1^','Assumed'],
   ['','Ionic conductivity','1.0 × 10^−3^','S cm^−1^','Assumed ^e^'],
  ];
  body.push(mkTable(w, ['Category','Parameter','Value','Unit','Source'], rows, 2));
}
body.push(new Paragraph({ children: [], spacing: { after: 80 } }));
body.push(Note('^a^ Effective conductivity of the active-material network, calibrated against the measured electrode response; not the intrinsic conductivity of NCM811.'));
body.push(Note('^b^ Effective mechanical inputs calibrated to reproduce the measured porosity of cold-pressed LPSCl at 300 MPa; not dense-material properties.'));
body.push(Note('^c^ The voxel representation fuses touching fibres and therefore carries no explicit fibre–fibre contact resistance, so the contact-inclusive compressed-powder value (0.012 Ω cm ≈ 83 S cm^−1^) is used rather than the intrinsic single-fibre value (10^−4^ Ω cm ≈ 10^4^ S cm^−1^). At a 0.15 μm voxel a 0.15 μm fibre is resolved as a one-voxel-wide tube, and the assigned conductivity is rescaled to 78.5 S cm^−1^ so that the axial conductance is preserved.'));
body.push(Note('^d^ Values used in the compaction simulations, corresponding to an earlier analysis of the AFM modulus maps.'));
body.push(Note('^e^ SDCP is not an ionic insulator: the LPSCl–SDCP pellet retains 80 % of the ionic conductivity of pristine LPSCl, whereas the LPSCl–PTFE pellet retains 27 % (Figure 2h). A representative value was assigned pending direct measurement.'));

body.push(Cap('**Table S3.** Structural and transport parameters obtained from the simulations.'));
{
  const w = [1400, 3400, 1500, 1500, 1200];
  const rows = [
   ['Structure','Thickness','72.48','72.48','μm'],
   ['','Porosity','7.87','7.39','%'],
   ['','Areal capacity','3.11','3.07','mAh cm^−2^'],
   ['','LPSCl coverage of NCM811','86.7','86.7','%'],
   ['','VGCF coverage of NCM811','13.0','15.4','%'],
   ['','Median conductive-additive contacts per NCM811 particle','433','517','–'],
   ['','Electronic connectivity','100','100','%'],
   ['Transport','Effective electronic conductivity','7.27 × 10^−2^','8.16 × 10^−2^','S cm^−1^'],
   ['','Effective ionic conductivity','5.69 × 10^−4^','5.64 × 10^−4^','S cm^−1^'],
   ['','DBE / SBE electronic conductivity ratio ^a^','SPAN:1.1232 ± 0.0011','','–'],
   ['','DBE / SBE ionic conductivity ratio ^a,b^','SPAN:0.99272 ± 0.00003','','–'],
  ];
  body.push(mkTable(w, ['Category','Parameter','SBE','DBE','Unit'], rows, 2));
}
body.push(new Paragraph({ children: [], spacing: { after: 80 } }));
body.push(Note('^a^ Mean over eight grid-origin arms; the uncertainty is the paired standard error. All eight solves converged.'));
body.push(Note('^b^ PTFE is not resolved on the conduction grid, so the ionic network contains no PTFE blocking. The ionic difference between the two electrodes therefore reflects only the electrolyte volume displaced by SDCP and not the difference in ion blocking between the two binders reported in Figure 2h. This value is provisional.'));

// ---------------- C. References -----------------------------------------
body.push(H('C.  References to be merged into the main list'));
body.push(P('Numbering continues from [32] in Manuscript v5.1; the arbitrary [100]/[102]/[107]/[109]/[110] labels are removed.'));
[
 '[33]\tC. Kloss, C. Goniva, A. Hager, S. Amberger, S. Pirker, *Prog. Comput. Fluid Dyn.* **2012**, *12*, 140.',
 '[34]\tA. Sakuda, A. Hayashi, M. Tatsumisago, *Sci. Rep.* **2013**, *3*, 2261.',
 '[35]\tY. Hu, Y. Fang, Z. Ge, Z. Qu, Y. Zhu, A. Pradhana, C. Jiang, *ACM Trans. Graph.* **2018**, *37*, 150.',
 '[36]\tH. Wang, et al., *J. Power Sources* **2020**, *470*, 228413.',
 '[37]\tM. Cronau, M. Szabo, C. König, T. B. Wassermann, B. Roling, *ACS Energy Lett.* **2021**, *6*, 3072.',
 '[9]\t(already cited) T. Minnmann et al., *Adv. Energy Mater.* **2022**, *12*, 2201425.',
].forEach(r => body.push(new Paragraph({ children: runs(r), spacing: { after: 60 },
  indent: { left: 500, hanging: 500 } })));


// ---------------- D. Notes to co-authors --------------------------------
body.push(H('D.  Notes to co-authors  (delete before submission)'));
const NOTE = (n, str) => body.push(new Paragraph({
  children: [ b(n + '  ') , ...runs(str) ],
  spacing: { after: 120, line: 290 }, alignment: AlignmentType.JUSTIFIED,
  indent: { left: 400, hanging: 400 } }));

NOTE('D1.', '**Removed — "a resolution validated against measured ionic conductivities."** '
+ 'The 0.4 μm grid used in v5.1 is not converged: re-solving the same electrodes at finer voxels '
+ 'changes the electronic conductivity ratio and reverses the sign of the ionic one. The '
+ 'agreement with a measured ionic conductivity held at one grid only and cannot be described '
+ 'as a validation. The sentence is deleted and the production grid (0.15 μm) is simply stated.');

NOTE('D2.', '**All transport numbers replaced.** The v5.1 values (electronic 1.98 → 3.00 S cm^−1^, '
+ 'ionic 2.03 → 2.15 × 10^−4^ S cm^−1^) come from the 0.4 μm grid with SDCP drawn as one voxel '
+ 'per particle, which over-represents its volume roughly four-fold. The values above are from '
+ 'the production convention (0.15 μm voxel, SDCP drawn as a true-diameter sphere, eight '
+ 'grid-origin arms). The electronic gain is +12.3 % and the ionic change is −0.7 %; both figures '
+ 'may be refined and should be treated as provisional.');

NOTE('D3.', '**Table S2 — mechanical inputs vs. the AFM figures (needs a decision).** The '
+ 'microstructures were compacted with PTFE 0.30 GPa and SDCP 23.6 GPa, but Figure 2g and '
+ 'Figures S6–S7 now report 1.8 GPa and 9.0 GPa. A methods table must list what was actually run, '
+ 'so the older values appear above with footnote d. The clean fix is to re-compact one electrode '
+ 'pair at 1.8 / 9.0 GPa and confirm the conductivity ratio moves by less than the ±0.7 % spread '
+ 'of the eight arms; the table can then quote the AFM values throughout.');

NOTE('D4.', '**Table S3 — structural descriptors carried over.** Thickness, porosity, areal '
+ 'capacity, coverages, contact counts and connectivity are unchanged from v5.1 and were '
+ 'extracted from the earlier 0.4 μm rasterization. The coverage and contact-count rows in '
+ 'particular depend on voxel size and should be re-extracted at 0.15 μm before submission. '
+ 'Porosity should also be reported on a single convention (sphere-volume basis) across the paper.');

NOTE('D5.', '**Terminology unified to "Young’s modulus (*E*)".** v5.1 mixes "elastic modulus" '
+ '(AFM, Table S2, Figure S6–S7 captions) with "Young’s modulus" (DEM text). The AFM section and '
+ 'the Figure S6/S7 captions should be changed to match, or the DEM section changed back — but '
+ 'one term only.');

NOTE('D6.', '**Bulk modulus comparison corrected.** v5.1 placed *K* = 25.5 GPa next to the '
+ '"dense-material 24 GPa", but 24 GPa is a Young’s modulus, not a bulk modulus. The revised text '
+ 'states *K* = 25.5 GPa without that comparison. If an anchor is wanted, use the calculated bulk '
+ 'modulus of LPSCl (26.2 GPa, this work) rather than 24 GPa.');

NOTE('D7.', '**Shear-softening factor removed.** v5.1 said the shear modulus "falls 18-fold"; the '
+ 'factor is 15.8 when referred to the calculated shear modulus of dense LPSCl. The revised text '
+ 'quotes the value (0.51 GPa) instead of a fold-change. The 18-fold figure remains correct for '
+ 'the DEM contact Young’s modulus (24 → 1.35 GPa).');

NOTE('D8.', '**Cross-model agreement claim removed.** v5.1 stated that the two models "agree on '
+ 'composite porosity and thickness to within one percentage point". That gap is a bookkeeping '
+ 'difference between the two porosity conventions, not independent agreement, so it is not '
+ 'evidence of validity. The statement that the models were calibrated independently is kept.');

NOTE('D9.', '**σ_SDCP_ sensitivity sweep moved out of Methods.** The paragraph reporting the '
+ 'five-point sweep and the dissipation-share anti-correlation is a result, not a method, and its '
+ 'numbers are from the superseded grid. Methods now states only the value adopted. If the sweep '
+ 'is wanted in the SI it must be re-run at the production convention.');

NOTE('D10.', '**Mechanism sentence needs rewriting wherever it appears in the Results.** The v5.1 '
+ 'reading — SDCP acting as a high-conductivity bridge that relieves series bottlenecks — is not '
+ 'supported by the current simulations: SDCP carries about 1 % of the electronic current, and '
+ 'suppressing its conductivity advantage removes only 6 % of the gain. Suggested replacement: '
+ '*"SDCP raises the electronic conductivity mainly by converting electronically insulating volume '
+ '— electrolyte and pore — into conducting volume, which reroutes current around bottlenecks in '
+ 'the existing carbon network, rather than by carrying a proportional share of the current itself."*');

NOTE('D12.', '**The ionic result is provisional — do not present it as a finding yet.** The value '
+ 'itself is reproducible (eight arms, all converged, ±0.003 % paired), but two things are open. '
+ '(i) It has never been checked against voxel size. The electronic ratio was tested at three grids '
+ 'and kept moving, and the ionic ratio reversed sign across the coarse grids used earlier; a '
+ 'refinement test cannot simply be run here, because the electrolyte fill degrades below 0.15 μm '
+ '(about 5 % of electrolyte cells unfilled at 0.15 μm, 18 % at 0.125 μm, 42 % at 0.10 μm), which '
+ 'makes the ionic solve unusable on finer grids. (ii) More importantly, PTFE is not stamped onto '
+ 'the conduction grid at all in the production setting, so the model cannot express the effect '
+ 'Figure 2h reports — that PTFE suppresses the ionic conductivity of LPSCl to 27 % while SDCP '
+ 'suppresses it only to 80 %. With PTFE invisible, the SBE and DBE differ ionically only in that '
+ 'the DBE has SDCP occupying volume that would otherwise be electrolyte or pore, which is a small '
+ 'penalty by construction. The direct test is to repeat the eight-arm run with PTFE stamped as a '
+ 'blocking phase; on the electronic side that change lowered the SBE by 25 % and the DBE by 13 % '
+ '(the SBE carries twice the PTFE) and raised the ratio from 1.126 to 1.309, so the same asymmetry '
+ 'is expected to move the ionic ratio upward. Until that run exists, either omit the ionic row or '
+ 'state it as a volume-occupancy effect only.');

NOTE('D11.', '**References.** Methods now carries five citations only: LIGGGHTS, MPM, the dense '
+ 'LPSCl modulus, the NCM modulus and the electrolyte grain conductivity. Every quantitative '
+ 'input that is not calibrated or measured in this work has a source in Table S2.');

fs.writeFileSync('/dev/null','');
const doc = new Document({ sections: [ { properties: { page: { margin:
  { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children: body } ] });
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(process.argv[2], buf);
  console.log('wrote', process.argv[2], buf.length, 'bytes');
});

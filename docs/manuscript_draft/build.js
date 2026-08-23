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
  'Each microstructure was rasterized onto a cubic grid with a voxel edge of 0.15 μm. Adjacent '
+ 'conducting voxels were coupled through harmonic-mean conductances, and the potential field was '
+ 'obtained from'));
body.push(Eq('∇·(*σ*∇*φ*) = 0', 1));
body.push(P('where *σ* is the local conductivity of each voxel and *φ* the electric potential. A '
+ 'potential difference was applied between the separator and current-collector faces with the '
+ 'remaining boundaries insulating, and the effective conductivity was taken from the total current. '
+ 'NCM811, VGCF and SDCP carried the electronic network and LPSCl and SDCP the ionic network; PTFE '
+ 'was not resolved on the conduction grid. Phase conductivities are listed in Table S2, in which '
+ 'the VGCF value is rescaled so that a fibre resolved as a one-voxel-wide tube retains its axial '
+ 'conductance. Each electrode was solved at eight half-voxel grid-origin shifts (2 × 2 × 2), the '
+ 'SBE and DBE sharing the same origins, and conductivity ratios are reported as the paired mean '
+ 'with its standard error.'));

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
   ['','Young’s modulus (DEM contact)','1.35','GPa','Calibrated'],
   ['','Young’s modulus (MPM continuum)','1.53','GPa','Calibrated'],
   ['','Poisson’s ratio (MPM continuum)','0.49','–','Calibrated'],
   ['','Yield strength','0.30','GPa','Calibrated'],
   ['','Ionic conductivity (grain interior)','3.0 × 10^−3^','S cm^−1^','Ref. [37]'],
   ['VGCF','Fibre diameter','0.15','μm','Experimental value'],
   ['','Young’s modulus','10','GPa','Assumed'],
   ['','Electronic conductivity (compressed powder)','1.0 × 10^2^','S cm^−1^','Supplier data ^b^'],
   ['','Electronic conductivity (voxel, diameter-preserving)','78.5','S cm^−1^','Calculated value ^b^'],
   ['PTFE','Young’s modulus','0.30','GPa','Assumed ^c^'],
   ['','Electronic / ionic conductivity','0','S cm^−1^','Assumed (insulating)'],
   ['SDCP','Particle diameter','0.30','μm','This work (Figure S5)'],
   ['','Young’s modulus','23.6','GPa','This work (Figure 2g) ^c^'],
   ['','Electronic conductivity','250','S cm^−1^','Assumed'],
   ['','Ionic conductivity','—','S cm^−1^','Not yet calibrated ^d^'],
  ];
  body.push(mkTable(w, ['Category','Parameter','Value','Unit','Source'], rows, 2));
}
body.push(new Paragraph({ children: [], spacing: { after: 80 } }));
body.push(Note('^a^ Effective network value calibrated against the measured electrode response, not the intrinsic conductivity of NCM811.'));
body.push(Note('^b^ The voxel representation fuses touching fibres and therefore carries no explicit fibre–fibre contact resistance, so the contact-inclusive compressed-powder value is used rather than the intrinsic single-fibre value (≈ 10^4^ S cm^−1^). At a 0.15 μm voxel the fibre is one voxel wide, and the conductivity is rescaled by the circle-in-square area ratio (π/4) so that the axial conductance is preserved.'));
body.push(Note('^c^ Values used in the compaction simulations, corresponding to an earlier analysis of the AFM modulus maps.'));
body.push(Note('^d^ Provisional. Figure 2h is consistent with SDCP acting as an inert filler on the ionic network, and this value has not yet been calibrated against that measurement.'));

body.push(Cap('**Table S3.** Structural and transport parameters obtained from the simulations.'));
{
  const w = [1400, 3400, 1500, 1500, 1200];
  const rows = [
   ['Structure','Thickness','72.48','72.48','μm'],
   ['','Porosity','7.87','7.39','%'],
   ['','Areal capacity','3.11','3.07','mAh cm^−2^'],
   ['','LPSCl coverage of NCM811 ^b^','—','—','%'],
   ['','VGCF coverage of NCM811 ^b^','—','—','%'],
   ['','Median conductive-additive contacts per NCM811 particle ^b^','—','—','–'],
   ['','Electronic connectivity ^b^','—','—','%'],
   ['Transport','Effective electronic conductivity','7.27 × 10^−2^','8.16 × 10^−2^','S cm^−1^'],
   ['','Effective ionic conductivity ^c^','—','—','S cm^−1^'],
   ['','DBE / SBE electronic conductivity ratio ^a^','SPAN:1.1232 ± 0.0011','','–'],
   ['','DBE / SBE ionic conductivity ratio ^c^','SPAN:—','','–'],
  ];
  body.push(mkTable(w, ['Category','Parameter','SBE','DBE','Unit'], rows, 2));
}
body.push(new Paragraph({ children: [], spacing: { after: 80 } }));
body.push(Note('^a^ Mean over eight grid-origin arms; the uncertainty is the paired standard error. All eight solves converged.'));
body.push(Note('^b^ Not reported. These descriptors were extracted at the earlier 0.4 μm rasterization and are being re-extracted at the production voxel size.'));
body.push(Note('^c^ Not reported. PTFE is not resolved on the conduction grid, so the ionic network contains no PTFE blocking, and the ionic conductivity of SDCP has not been calibrated against Figure 2h; the model therefore does not yet represent the quantity being compared.'));

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
body.push(H('D.  공저자용 메모  (투고 전 삭제)'));
const NOTE = (n, str) => body.push(new Paragraph({
  children: [ b(n + '  ') , ...runs(str) ],
  spacing: { after: 120, line: 290 }, alignment: AlignmentType.JUSTIFIED,
  indent: { left: 400, hanging: 400 } }));

NOTE('D1.', '**삭제 — "a resolution validated against measured ionic conductivities."** v5.1 의 '
+ '0.4 μm 격자는 수렴하지 않았다.  같은 전극을 더 고운 격자에서 다시 풀면 전자 전도도 비가 '
+ '계속 움직이고 이온 비는 부호가 뒤집힌다.  측정 이온전도도와의 일치는 **그 한 격자에서만** '
+ '성립했으므로 검증이라고 부를 수 없다.  문장을 지우고 생산 격자(0.15 μm)만 적었다.');

NOTE('D2.', '**수송 수치 전면 교체 (잠정).** v5.1 의 값(전자 1.98 → 3.00 S cm^−1^, 이온 '
+ '2.03 → 2.15 × 10^−4^ S cm^−1^)은 0.4 μm 격자에서 SDCP 를 입자당 복셀 하나로 찍은 것이고, '
+ '그러면 SDCP 부피가 참값의 약 네 배가 된다.  위 표의 값은 생산 규약(0.15 μm 복셀 · SDCP 를 '
+ '참 직경 구로 · 격자 원점 8팔)에서 나온 것이다.  전자 이득은 +12.3 % 이며, 이 값도 아직 '
+ '격자 수렴이 확인되지 않았으므로 잠정으로 다룬다.');

NOTE('D3.', '**Table S2 — 기계 물성이 AFM 그림과 어긋난다 (결정 필요).** 미세구조는 PTFE '
+ '0.30 GPa · SDCP 23.6 GPa 로 압밀했는데 Figure 2g 와 Figure S6–S7 은 1.8 GPa 와 9.0 GPa 를 '
+ '보고한다.  방법론 표는 **실제로 돌린 값**을 적어야 하므로 옛 값에 각주 c 를 달아 두었다.  '
+ '깨끗한 해법은 전극 한 쌍을 1.8 / 9.0 GPa 로 다시 압밀해 전도도 비가 8팔 산포(±0.7 %) 안에서 '
+ '움직이는지 확인하는 것이고, 그러면 표에 AFM 값을 그대로 쓸 수 있다.');

NOTE('D4.', '**Table S3 — 구조 항목은 v5.1 에서 그대로 가져왔다.** 두께 · porosity · 면적용량 · '
+ 'coverage · 접촉수 · 연결률은 옛 0.4 μm 래스터에서 뽑은 값이다.  특히 coverage 와 접촉수는 '
+ '복셀 크기에 직접 의존하므로 **표에서 비워 두었다**(각주 b) — 0.15 μm 에서 다시 뽑아 채울 것.  두께 · porosity · 면적용량은 래스터가 아니라 압밀 결과라 그대로 두었고, porosity 는 논문 전체에서 한 가지 규약(구 부피 기준)으로 통일해 보고할 것.');

NOTE('D5.', '**용어를 "Young’s modulus (*E*)" 로 통일했다.** v5.1 은 "elastic modulus"(AFM · '
+ 'Table S2 · Figure S6–S7 캡션)와 "Young’s modulus"(DEM 본문)를 섞어 쓴다.  AFM 절과 '
+ 'Figure S6/S7 캡션을 맞추거나 DEM 쪽을 되돌리거나 — **한 가지만** 쓰면 된다.');

NOTE('D6.', '**체적탄성률 비교 삭제.** v5.1 은 *K* = 25.5 GPa 를 "dense-material 24 GPa" 옆에 '
+ '놓았는데, 24 GPa 는 체적탄성률이 아니라 **영률**이다.  수정본은 *K* = 25.5 GPa 만 적는다.  '
+ '앵커가 필요하면 24 GPa 가 아니라 계산된 LPSCl 체적탄성률(26.2 GPa, this work)을 쓸 것.');

NOTE('D7.', '**전단 연화 배수 삭제.** v5.1 은 전단탄성률이 "18-fold" 떨어진다고 적었으나, 계산된 '
+ '치밀 LPSCl 전단탄성률 기준으로는 15.8 배다.  수정본은 배수 대신 값(0.51 GPa)을 적는다.  '
+ '18 배는 **DEM 접촉 영률**(24 → 1.35 GPa)에 대해서는 그대로 맞다.');

NOTE('D8.', '**두 모델이 "1 %p 안에서 일치" 주장 삭제.** 그 차이는 두 porosity 규약 사이의 '
+ '부기 차이이지 독립적인 일치가 아니므로 타당성의 근거가 되지 않는다.  두 모델을 서로가 아니라 '
+ '같은 실험값에 각각 보정했다는 문장은 남겼다.');

NOTE('D9.', '**σ_SDCP_ 민감도 스윕과 Joule 식을 Methods 에서 뺐다.** 5점 스윕과 소산-분담 논증은 '
+ '방법이 아니라 **결과**이고, 그 수치는 폐기된 격자의 것이다.  그 문단이 빠지면서 Joule 소산을 '
+ '쓰는 곳이 논문에 하나도 남지 않으므로(Figure 4b 는 전도도만 보여준다) 두 번째 식과 기호 정의도 '
+ '함께 삭제하고 남은 식을 (1) 로 번호를 매겼다.  채택한 SDCP 전도도는 이제 Table S2 에만 있다.');

NOTE('D10.', '**기전 문장은 Results 쪽에서 다시 써야 한다.** v5.1 의 서술 — SDCP 가 고전도 '
+ '브리지로서 직렬 병목을 해소한다 — 은 지금 시뮬레이션이 지지하지 않는다.  SDCP 가 나르는 전자 '
+ '전류는 약 1 % 이고, SDCP 의 전도도 우위를 없애도 이득은 6 % 만 줄어든다.  교체안: '
+ '*"SDCP raises the electronic conductivity mainly by converting electronically insulating volume — '
+ 'electrolyte and pore — into conducting volume, which reroutes current around bottlenecks in the '
+ 'existing carbon network, rather than by carrying a proportional share of the current itself."*');

NOTE('D11.', '**레퍼런스.** Methods 는 이제 인용 5개만 쓴다 — LIGGGHTS · MPM · 치밀 LPSCl 영률 · '
+ 'NCM 영률 · 전해질 grain 이온전도도.  이 논문에서 보정하거나 측정한 것이 아닌 **모든 정량 입력**은 '
+ 'Table S2 의 Source 열에 출처가 있다.  임의로 붙였던 [100]/[102]/[107]/[109]/[110] 은 없앴다.');

NOTE('D12.', '**이온 결과는 아직 결과로 내세우지 않는다.** 값 자체는 재현된다(8팔 전부 수렴, '
+ '쌍대응 ±0.003 %).  그러나 두 가지가 열려 있다.  (i) 복셀 크기에 대해 한 번도 확인한 적이 없고, '
+ '**확인할 수도 없다** — 0.15 μm 아래에서 전해질 충전이 무너진다(미충전 셀이 0.15 μm 에서 약 5 %, '
+ '0.125 μm 에서 18 %, 0.10 μm 에서 42 %) → 이온 솔브가 그 격자에서 못 쓰게 된다.  (ii) 더 중요한 것 — '
+ '생산 설정에서 PTFE 가 전도 격자에 **아예 스탬프되지 않는다**.  그래서 Figure 2h 가 보고하는 효과, '
+ '즉 PTFE 는 LPSCl 이온전도도를 27 % 로 죽이고 SDCP 는 80 % 로만 죽인다는 것을 모델이 표현할 수 '
+ '없다.  PTFE 가 보이지 않으면 SBE 와 DBE 의 이온적 차이는 "DBE 에만 SDCP 가 있어 전해질·기공 부피를 '
+ '점유한다" 하나로 줄어들고, 그것은 구성상 작은 손해일 수밖에 없다.  ⇒ **표의 이온 행을 전부 비웠다** (각주 c).  D13 의 보정을 마친 뒤 채운다.');

NOTE('D13.', '**Figure 2h 로 이온 상 전도도를 보정할 수 있다 — 다음 우선순위 (신규).** Figure 2h 는 '
+ '9:1 wt 펠릿을 재는데, 이것이 곧 **이 논문 자신의 상-수준 보정 데이터**다.  리포 밀도 규약'
+ '(LPSCl 2.00 · PTFE 2.20 · SDCP 1.30 g cm^−3^)으로 부피분율을 내고 불활성 충전재 희석'
+ '(Bruggeman, (1 − *φ*)^1.5^)과 비교하면:');
body.push(mkTable([1900, 1500, 2100, 1600, 1900],
  ['Binder','vol %','Dilution-only prediction','Measured','Measured / prediction'],
  [ ['PTFE (9:1)','9.17','3.09 mS cm^−1^','0.97 mS cm^−1^','**0.31**'],
    ['SDCP (9:1)','14.60','2.82 mS cm^−1^','2.86 mS cm^−1^','**1.02**'] ], 1));
body.push(new Paragraph({ children: [], spacing: { after: 80 } }));
NOTE('', '⇒ **SDCP 는 이온망에서 사실상 불활성 충전재로 거동한다** — 부피 희석만으로 실측이 1.5 % '
+ '안에서 설명된다 (Maxwell–Garnett 로 교차확인: 절연 가정 2.84 vs 실측 2.86; σ_i_ = 1.0 mS cm^−1^ '
+ '가정은 3.10 으로 벗어난다).  ρ_SDCP_ 가 proxy 값(1.3)이라 1.1–1.7 g cm^−3^ 로 흔들어 봐도 비는 '
+ '1.06–0.96 로 결론이 바뀌지 않는다.  반대로 **PTFE 는 희석으로 설명되는 것의 3.2 배를 더 깎는다** — '
+ '부피 점유가 아니라 표면 피복/피브릴 웹의 차단 효과다.');
NOTE('', '⇒ 지금 모델은 이 두 가지를 **모두** 놓치고 있다: σ_ion_(SDCP) 를 1.0 mS cm^−1^ 로 두어 '
+ '실측보다 후하게 잡았고, PTFE 는 아예 안 그린다.  두 오차가 **같은 방향으로** 작용해 이온 비를 '
+ 'DBE 에 불리하게 민다.  ⚠ 다만 부피만 보면 DBE 쪽 바인더가 오히려 많다 (2.03 vs 1.51 vol% of '
+ 'solid — SDCP 가 PTFE 보다 가벼워서다).  즉 DBE 의 이온 이득은 부피가 아니라 **PTFE 차단의 비대칭'
+ '**(SBE 1 wt% vs DBE 0.5 wt%)에서만 나올 수 있고, 그것이 지금 모델에 없는 항이다.');
NOTE('', '⇒ **제안하는 보정 (frame[4] — 모델끼리가 아니라 실험에 맞춘다)**: 9:1 LPSCl+바인더 펠릿을 '
+ '같은 복셀 파이프라인으로 만들고, ⓐ σ_ion_(SDCP) 와 ⓑ PTFE 의 차단 표현(스탬프 + 표면층)을 '
+ 'Figure 2h 의 0.97 / 2.86 mS cm^−1^ 를 재현하도록 맞춘다.  그렇게 얻은 상 전도도를 전극에 넣어 '
+ '8팔을 다시 돌리면 이온 축이 **이 논문 자신의 측정에 앵커된** 결과가 된다.  작은 RVE 라 비용도 낮다.');

fs.writeFileSync('/dev/null','');
const doc = new Document({ sections: [ { properties: { page: { margin:
  { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children: body } ] });
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(process.argv[2], buf);
  console.log('wrote', process.argv[2], buf.length, 'bytes');
});

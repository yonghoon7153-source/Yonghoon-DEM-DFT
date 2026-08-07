// Research Seminar 2026-08 — Hanyang BML 템플릿 스타일 덱 생성기
// 대본: docs/seminar_20260806_script.md · 용어: docs/seminar_20260806_glossary.md
const pptxgen = require('pptxgenjs');
const p = new pptxgen();
p.layout = 'LAYOUT_16x9';            // 10 x 5.625 in
p.author = 'Yonghoon An';
p.title  = 'Particle-Resolved Simulation of All-Solid-State Cathodes';

const NAVY = '1F4E79', BLUE = '2E74B5', RED = 'C00000', GRAY = '808080',
      DARK = '262626', HDRFILL = 'DCE6F1', LIGHT = 'F2F2F2';
const TFONT = 'Arial', BFONT = 'Calibri';
let pageNo = 0;

/** 템플릿 공통 뼈대: 파란 볼드 제목 + 가로줄 + 우상단 인용 + 하단 로고/페이지 */
function frame(title, ref) {
  const s = p.addSlide();
  pageNo += 1;
  s.addText(title, { x: 0.42, y: 0.20, w: 8.2, h: 0.55, fontFace: TFONT, fontSize: 24,
                     bold: true, color: NAVY, valign: 'middle', margin: 0 });
  s.addShape(p.ShapeType.line, { x: 0.42, y: 0.80, w: 9.16, h: 0,
                                 line: { color: '404040', width: 1 } });
  if (ref) s.addText(ref, { x: 5.0, y: 0.84, w: 4.58, h: 0.22, fontFace: BFONT, fontSize: 8,
                            italic: true, color: GRAY, align: 'right', margin: 0 });
  s.addText('Battery Materials Lab.', { x: 0.42, y: 5.25, w: 3.0, h: 0.25, fontFace: BFONT,
                                        fontSize: 9, color: 'A6A6A6', margin: 0 });
  s.addText(String(pageNo), { x: 9.0, y: 5.25, w: 0.58, h: 0.25, fontFace: BFONT,
                              fontSize: 9, color: 'A6A6A6', align: 'right', margin: 0 });
  return s;
}

/** ■ 대불릿 + · 소불릿 (템플릿 2단 구조) */
function bullets(s, items, opt) {
  const o = Object.assign({ x: 0.55, y: 1.00, w: 8.9, h: 1.4, size: 13 }, opt || {});
  const runs = [];
  items.forEach((it, i) => {
    const last = i === items.length - 1;
    if (it.h) {
      runs.push({ text: '■  ', options: { color: RED, fontSize: o.size + 1, bold: true } });
      runs.push({ text: it.h, options: { color: DARK, fontSize: o.size + 1, bold: true,
                                         breakLine: !last } });
    } else {
      runs.push({ text: '     ·   ', options: { color: GRAY, fontSize: o.size } });
      (it.parts || [{ t: it.t }]).forEach(pt => runs.push({
        text: pt.t, options: { color: pt.c || DARK, fontSize: o.size, bold: !!pt.b }
      }));
      if (!last) runs[runs.length - 1].options.breakLine = true;
    }
  });
  s.addText(runs, Object.assign({ fontFace: BFONT, valign: 'top', margin: 0,
                                  paraSpaceAfter: 5, lineSpacing: 18 },
                                { x: o.x, y: o.y, w: o.w, h: o.h }));
}

/** 표 (템플릿 헤더 채움색) */
function table(s, rows, opt) {
  const o = Object.assign({ x: 0.6, y: 2.4, w: 8.8, fs: 11 }, opt || {});
  const body = rows.map((r, i) => r.map(c => {
    const txt = typeof c === 'object' ? c.t : c;
    const bold = typeof c === 'object' ? !!c.b : (i === 0);
    const col  = typeof c === 'object' && c.c ? c.c : (i === 0 ? NAVY : DARK);
    return { text: String(txt),
             options: { bold: i === 0 || bold, color: col, fontSize: o.fs,
                        fill: i === 0 ? HDRFILL : (i % 2 ? 'FFFFFF' : LIGHT),
                        align: i === 0 ? 'center' : (typeof c === 'object' && c.a) || 'left' } };
  }));
  s.addTable(body, { x: o.x, y: o.y, w: o.w, colW: o.colW, fontFace: BFONT,
                     border: { type: 'solid', color: 'BFBFBF', pt: 0.5 },
                     rowH: o.rowH || 0.26, valign: 'middle', margin: 3 });
}

/** 결론 캡션 ("그래서 뭐?") */
function takeaway(s, txt, y) {
  s.addShape(p.ShapeType.roundRect, { x: 0.55, y: y || 4.62, w: 8.9, h: 0.52,
    fill: { color: 'EAF1F8' }, line: { color: BLUE, width: 0.75 }, rectRadius: 0.06 });
  s.addText(txt, { x: 0.72, y: y || 4.62, w: 8.56, h: 0.52, fontFace: BFONT, fontSize: 11.5,
                   color: NAVY, bold: true, valign: 'middle', margin: 0 });
}

/** 그림 자리 (실제 그림을 넣기 전 표시) */
function figbox(s, x, y, w, h, label) {
  s.addShape(p.ShapeType.rect, { x, y, w, h, fill: { color: 'FAFAFA' },
                                 line: { color: 'BFBFBF', width: 0.75, dashType: 'dash' } });
  s.addText('[Fig] ' + label, { x: x + 0.08, y, w: w - 0.16, h, fontFace: BFONT, fontSize: 9.5,
                                color: GRAY, align: 'center', valign: 'middle', margin: 0 });
}

/* ═══════════════════ 1. Title ═══════════════════ */
{
  const s = p.addSlide();
  s.addText('August 2026', { x: 6.6, y: 0.28, w: 3.0, h: 0.3, fontFace: BFONT, fontSize: 11,
                             color: DARK, align: 'right', margin: 0 });
  s.addText('Research Seminar', { x: 0.7, y: 1.05, w: 8.6, h: 0.55, fontFace: TFONT,
                                  fontSize: 30, bold: true, color: NAVY, margin: 0 });
  s.addText('Particle-Resolved Simulation of All-Solid-State Cathodes:\nFrom Powder Packing to Cycle Life',
            { x: 0.72, y: 1.68, w: 8.6, h: 0.8, fontFace: BFONT, fontSize: 17, color: DARK,
              lineSpacing: 26, margin: 0 });
  s.addText('Yonghoon An', { x: 0.72, y: 2.72, w: 6.0, h: 0.35, fontFace: BFONT, fontSize: 15,
                             color: DARK, margin: 0 });
  s.addText('Division of Materials Science & Engineering, Hanyang University\n(E-mail : yonghoon71@hanyang.ac.kr)',
            { x: 0.72, y: 3.15, w: 7.0, h: 0.6, fontFace: BFONT, fontSize: 11.5, color: '404040',
              lineSpacing: 17, margin: 0 });
  s.addShape(p.ShapeType.line, { x: 0.72, y: 4.15, w: 3.2, h: 0, line: { color: NAVY, width: 2 } });
  s.addText('HANYANG UNIVERSITY  ·  Battery Materials Lab.',
            { x: 0.72, y: 4.35, w: 6.0, h: 0.3, fontFace: BFONT, fontSize: 10.5, bold: true,
              color: NAVY, margin: 0 });
  s.addNotes('직전 발표(2026-04)는 DEM + DFT 에서 끝났습니다. 오늘은 그 뒤 4개월에 붙은 것 — '
    + '소성 압밀, 3D 전도, 전기화학, 사이클 열화, ML — 을 결과 중심으로 보고합니다.');
}

/* ═══════════════════ 2. Intro — microstructure decides ═══════════════════ */
{
  const s = frame('Introduction', 'J. Electrochem. Soc. 168 (2021) 040537 · Sci. Rep. 3 (2013) 2261');
  bullets(s, [
    { h: 'In an all-solid-state cathode, performance is decided by microstructure' },
    { parts: [{ t: 'In a liquid cell the electrolyte ' }, { t: 'soaks every particle', c: BLUE, b: true },
              { t: '. In a solid cell, Li' }, { t: '+' }, { t: ' passes only where powders were ' },
              { t: 'pressed into contact', c: RED, b: true }, { t: '.' }] },
    { parts: [{ t: 'Cathode = active material (AM, NCM811) + solid electrolyte (SE, Li' },
              { t: '6' }, { t: 'PS' }, { t: '5' }, { t: 'Cl) powders, cold-pressed at ' },
              { t: '300 MPa', b: true }, { t: '.' }] },
    { parts: [{ t: '⇒ What decides performance is ' }, { t: 'not the chemical formula but the microstructure',
              c: BLUE, b: true }, { t: ' — porosity, where particles touch, and how ions/electrons flow through those contacts.' }] },
  ], { h: 1.25 });
  figbox(s, 0.6, 2.40, 4.25, 2.05, 'liquid cell (fully wetted) vs solid cell (contact points only)\n★ 이 덱에서 가장 중요한 그림 — 새로 그려야 함');
  figbox(s, 5.15, 2.40, 4.25, 2.05, 'cold-pressed composite cathode\ncross-section (SEM)');
  takeaway(s, 'Same composition, different pressing → different performance.  To see "how", we must look inside.');
  s.addNotes('여기서 청중이 잡아야 할 것 하나: 고체에서는 눌러 붙인 자리만 이온이 지나간다. '
    + '그래서 미세구조가 전부입니다.');
}

/* ═══════════════════ 3. Intro — experiments cannot see ═══════════════════ */
{
  const s = frame('Introduction', 'Minnmann et al., J. Electrochem. Soc. 168 (2021) 040537');
  bullets(s, [
    { h: 'Experiments cannot see inside — so we rebuild the electrode in a computer' },
  ], { h: 0.35 });
  table(s, [
    ['Experiment', 'What it gives', 'What it CANNOT give'],
    ['SEM / EDS', 'shape of one cut cross-section', '3-D connectivity; where current actually flows'],
    ['EIS (impedance)', 'one number for total cell resistance', 'which contact that resistance comes from'],
    ['Charge–discharge', 'the sum of capacity and polarization', 'which particles are left out, and why'],
  ], { y: 1.42, w: 8.9, colW: [1.9, 3.0, 4.0], rowH: 0.42, fs: 11 });
  bullets(s, [
    { parts: [{ t: 'Input = ' }, { t: 'design numbers', b: true },
              { t: ' (composition · particle size · pressure · thickness · additive wt%).' }] },
    { parts: [{ t: 'Output = what experiments cannot give: ' },
              { t: 'contact network · conduction paths · reaction distribution · stress field · cycle degradation',
                c: BLUE, b: true }, { t: '.' }] },
    { parts: [{ t: 'This talk reports ' }, { t: 'what that pipeline found', b: true },
              { t: ' — it is not a tool introduction.' }] },
  ], { y: 3.35, h: 1.15 });
  s.addNotes('EIS 는 저항을 하나의 숫자로 줍니다. 그 숫자가 어느 접촉에서 왔는지는 못 줍니다. '
    + '그걸 나누는 게 이 파이프라인이 하는 일입니다.');
}

/* ═══════════════════ 4. Intro — DEM vs MPM ═══════════════════ */
{
  const s = frame('Introduction', 'Cundall & Strack, Géotechnique 29 (1979) 47 · Sulsky et al., CMAME 118 (1994) 179');
  bullets(s, [
    { h: 'Two simulation methods, because compaction is two things at once' },
  ], { h: 0.35 });
  table(s, [
    ['', 'What happens physically', 'Method', 'One-line definition'],
    ['①', 'particles roll and settle\n(rearrangement · stacking · contact)', 'DEM\n(discrete element)',
     'treat each particle as a rigid sphere;\nsolve Newton’s equations'],
    ['②', 'particles are squashed\n(plastic deformation · void filling)', 'MPM\n(material point)',
     'treat the material as a continuum;\nsolve the deformation'],
  ], { y: 1.42, w: 8.9, colW: [0.5, 2.9, 1.7, 3.8], rowH: 0.62, fs: 11 });
  bullets(s, [
    { parts: [{ t: 'What DEM cannot do: ' }, { t: 'the sphere never deforms', c: RED, b: true },
              { t: '  →  no shape change.' }] },
    { parts: [{ t: 'What MPM cannot do: ' }, { t: 'a continuum has no "particles"', c: RED, b: true },
              { t: '  →  cannot express "they touched at a point".' }] },
    { parts: [{ t: '⇒ ' }, { t: 'Both are required. Either one alone is half the physics.', c: BLUE, b: true }] },
  ], { y: 3.45, h: 1.05 });
  s.addNotes('DEM 과 MPM 을 처음 듣는 분을 위한 슬라이드입니다. '
    + '핵심은 "둘 중 뭐가 낫냐"가 아니라 "둘이 서로 다른 절반을 담당한다"입니다.');
}

/* ═══════════════════ 5. Intro — the rule ═══════════════════ */
{
  const s = frame('Introduction', 'Minnmann et al., JES 168 (2021) 040537 (calibration anchor)');
  bullets(s, [
    { h: 'The rule that makes it science: never fit one model to the other' },
    { parts: [{ t: 'Fitting A to B and then reporting "A and B agree" is ' },
              { t: 'circular reasoning', c: RED, b: true }, { t: '.' }] },
    { parts: [{ t: 'Instead each model is calibrated ' }, { t: 'only to experiment', c: BLUE, b: true },
              { t: ', then compared on the quantities they share.' }] },
  ], { h: 0.95 });
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 2.05, w: 4.25, h: 1.05,
    fill: { color: 'FDEBEB' }, line: { color: RED, width: 1 }, rectRadius: 0.06 });
  s.addText([{ text: '✗  Cross-fitting\n', options: { bold: true, color: RED, fontSize: 13 } },
             { text: 'DEM ⇄ MPM tuned to each other\n→ agreement proves nothing',
               options: { color: DARK, fontSize: 11 } }],
            { x: 0.75, y: 2.05, w: 3.95, h: 1.05, fontFace: BFONT, valign: 'middle',
              lineSpacing: 16, margin: 0 });
  s.addShape(p.ShapeType.roundRect, { x: 5.15, y: 2.05, w: 4.25, h: 1.05,
    fill: { color: 'EAF7EE' }, line: { color: '2E7D32', width: 1 }, rectRadius: 0.06 });
  s.addText([{ text: '✓  Independent calibration\n', options: { bold: true, color: '2E7D32', fontSize: 13 } },
             { text: 'each → experiment, then compare\nagreement = cross-validation',
               options: { color: DARK, fontSize: 11 } }],
            { x: 5.30, y: 2.05, w: 3.95, h: 1.05, fontFace: BFONT, valign: 'middle',
              lineSpacing: 16, margin: 0 });
  bullets(s, [
    { parts: [{ t: 'There is exactly ' }, { t: 'ONE calibration point', c: BLUE, b: true },
              { t: ': porosity of pure SE pressed at 300 MPa ≈ 10 % (measured).' }] },
    { parts: [{ t: 'Everything after that is a ' }, { t: 'prediction', b: true },
              { t: ' — composite porosity, thickness, coverage, Heckel yield pressure, absolute σ.' }] },
    { parts: [{ t: 'Agreement = cross-validation.  ' },
              { t: 'Disagreement = a quantified model limit — information, not failure.', c: BLUE, b: true }] },
  ], { y: 3.30, h: 1.15 });
  s.addNotes('질문 1순위가 "결국 실험에 맞춘 거 아니냐"입니다. 답: 보정점은 딱 하나이고, '
    + '그 뒤는 전부 예측입니다. 그리고 두 모델은 서로를 절대 안 맞춥니다.');
}

/* ═══════════════════ 6. Intro — scope ═══════════════════ */
{
  const s = frame('Introduction', null);
  bullets(s, [
    { h: 'Scope: one cathode layer resolved; the rest are exact boundary conditions' },
  ], { h: 0.35 });
  table(s, [
    ['Region', 'How it is treated'],
    ['Cathode composite', 'RESOLVED — every particle, every voxel (9 phases: AM_S · AM_P · SE · VGCF · SuperP · SDCP · SWCNT · PTFE · pore)'],
    ['Separator', 'boundary condition (surface supplying Li⁺)'],
    ['Current collector', 'one series resistance (bare-Al 46 · C-SUS 30 Ω·cm²)'],
    ['Li metal anode', 'reference electrode only → vs-Li half-cell convention'],
  ], { y: 1.42, w: 8.9, colW: [2.1, 6.8], rowH: 0.40, fs: 11 });
  bullets(s, [
    { parts: [{ t: '★ Why this is not an approximation: ' },
              { t: 'in a liquid cell you must solve concentration polarization in the electrolyte. ' },
              { t: 'In a single-ion conductor (t⁺ ≈ 1) the anions do not move at all', c: BLUE, b: true },
              { t: ' — that term does not exist. It is not omitted; it is absent.' }] },
    { parts: [{ t: 'Pipeline: ' }, { t: 'packing (DEM) → compaction (MPM) → transport (voxel network) → electrochemistry → degradation', b: true }] },
  ], { y: 3.55, h: 0.95 });
  s.addNotes('"반쪽셀인데 왜?"라는 질문에 대한 선제 답입니다. 단일이온 전도체에서는 '
    + '농도 분극 항이 물리적으로 존재하지 않습니다.');
}

/* ═══════════════════ 7. R1 — two models agree ═══════════════════ */
{
  const s = frame('Results and discussion', 'Minnmann et al., JES 168 (2021) 040537');
  bullets(s, [
    { h: 'Two models that never saw each other agree within 1.1 %p — that gap IS the error bar' },
    { parts: [{ t: 'DEM (rigid spheres, E_eff 1.35 GPa) and MPM (continuum J2, E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa) were each calibrated ' },
              { t: 'only to the same single experiment', c: BLUE, b: true }, { t: '.' }] },
  ], { h: 0.75 });
  table(s, [
    ['', 'MPM', 'DEM (LIGGGHTS)', 'Δ'],
    ['Porosity', '15.93 %', '15.6 %', '+0.33 %p'],
    ['Thickness', '29.95 µm', '30.28 µm', '−0.33 µm'],
    ['Coverage AM_P / AM_S', '49.6 / 48.2 %', '48.3 / 51.8 %', '± 2 %p'],
  ], { x: 0.6, y: 2.00, w: 5.0, colW: [1.85, 1.05, 1.35, 0.75], rowH: 0.30, fs: 10.5 });
  s.addShape(p.ShapeType.roundRect, { x: 5.85, y: 2.00, w: 3.55, h: 1.50,
    fill: { color: 'EAF1F8' }, line: { color: BLUE, width: 0.75 }, rectRadius: 0.06 });
  s.addText([{ text: 'Grid convergence\n', options: { bold: true, color: NAVY, fontSize: 12 } },
             { text: '384 → 512:  porosity 16.7 → 16.80 %\njamming position wall_z 0.616 at BOTH\n',
               options: { color: DARK, fontSize: 10.5 } },
             { text: '⇒ the remaining gap is a converged constitutive\ndifference, not a numerical artifact',
               options: { color: NAVY, fontSize: 10.5, italic: true } }],
            { x: 6.0, y: 2.00, w: 3.25, h: 1.50, fontFace: BFONT, valign: 'middle',
              lineSpacing: 15, margin: 0 });
  figbox(s, 0.6, 3.62, 4.4, 0.90, 'MPM x–z section (AM + SE + void)');
  figbox(s, 5.15, 3.62, 4.25, 0.90, 'porosity vs grid (384 / 512)');
  takeaway(s, 'To "how much do you trust this simulation?" we can answer with a number: ± 1 %p.', 4.62);
  s.addNotes('이 슬라이드가 이 발표의 신뢰 기반입니다. 서로 본 적 없는 두 모델이 만났고, '
    + '격자를 조여도 안 변합니다.');
}

/* ═══════════════════ 8. R2 — who owns the packing dip ═══════════════════ */
{
  const s = frame('Results and discussion', 'Furnas, Ind. Eng. Chem. 23 (1931) · experiment: this lab');
  bullets(s, [
    { h: 'Which model owns which observable — proven by a material sweep, not assumed' },
    { parts: [{ t: 'Bimodal packing dip = mixing large and small particles has a ' },
              { t: 'porosity minimum', c: BLUE, b: true },
              { t: ' (small particles fill the gaps between large ones).  DEM reproduces it — and matches experiment.' }] },
  ], { h: 0.78 });
  s.addChart(p.ChartType.line, [
    { name: 'DEM  (SE D1)',  labels: ['S only', '3:7', '5:5', '7:3', 'P only'], values: [18.9, 15.8, 15.0, 14.3, 16.2] },
    { name: 'DEM  (SE D3)',  labels: ['S only', '3:7', '5:5', '7:3', 'P only'], values: [20.9, 17.2, 15.9, 14.4, 16.2] },
    { name: 'Experiment',    labels: ['S only', '3:7', '5:5', '7:3', 'P only'], values: [23.9, 21.3, 20.3, 19.8, 25.4] },
  ], { x: 0.55, y: 1.95, w: 4.55, h: 2.55, showTitle: true, title: 'Porosity vs large:small AM ratio (AM:SE = 80:20)',
       titleFontSize: 11, titleColor: NAVY, chartColors: [NAVY, BLUE, RED],
       lineSize: 2, lineDataSymbolSize: 6, showLegend: true, legendPos: 'b', legendFontSize: 9,
       catAxisLabelColor: '595959', valAxisLabelColor: '595959', catAxisLabelFontSize: 9,
       valAxisLabelFontSize: 9, valAxisTitle: 'Porosity (%)', showValAxisTitle: true,
       valAxisTitleFontSize: 9, valGridLine: { color: 'E0E0E0', size: 0.5 },
       catGridLine: { style: 'none' } });
  bullets(s, [
    { parts: [{ t: 'MPM gives a ' }, { t: 'monotonic curve', c: RED, b: true },
              { t: ' (AM 60→95 wt%: 11.7 → 24.5 %) — no dip at all.' }] },
    { parts: [{ t: '★ Swept the whole SE material space: soft → monotonic and denser; rigid (E = 24 GPa) → a shallow, mislocated dip but ' },
              { t: '2–3× too porous', c: RED, b: true }, { t: ' (32–48 % vs DEM ~16 %).' }] },
    { parts: [{ t: '⇒ ' }, { t: 'No SE material setting reproduces both the dip shape and the absolute value.', c: BLUE, b: true }] },
    { parts: [{ t: 'The dip lives in the ' }, { t: 'initial rigid-sphere packing geometry', b: true },
              { t: '. A continuum cannot have it, regardless of material.' }] },
  ], { x: 5.25, y: 1.95, w: 4.25, h: 2.55, size: 11 });
  takeaway(s, 'Capability division is a measured conclusion, not an assumption: DEM owns packing, MPM owns plastic shape.', 4.62);
  s.addNotes('"MPM 에 dip 이 없으면 MPM 이 틀린 것 아니냐"는 질문이 옵니다. '
    + '답: 표현 범위 밖이라는 뜻입니다. 연속체에는 "공"이 없습니다.');
}

/* ═══════════════════ 9. R3 — transport network ═══════════════════ */
{
  const s = frame('Results and discussion', 'Bazzoun et al., J. Power Sources 661 (2026) 238682 · Holm, Electric Contacts (1967)');
  bullets(s, [
    { h: 'Transport: a resistor network on voxels — validated by an independent paper' },
    { parts: [{ t: 'Microstructure → ' }, { t: '0.4 µm voxels', b: true },
              { t: ' (2.5 voxels across an SE particle); neighbouring same-phase voxels become resistors; solve ∇·(σ∇φ) = 0.' }] },
    { parts: [{ t: 'Each contact neck carries a ' }, { t: 'constriction resistance', c: BLUE, b: true },
              { t: '  R = 1/(2σ·r_c)  (Holm 1967); plastic contact area from Tabor.' }] },
    { parts: [{ t: 'Three conductivities at once — ' }, { t: 'ionic (SE) · electronic (AM + carbon) · thermal (three parallel paths)', b: true }] },
    { parts: [{ t: 'Coverage of AM by SE, verified against a ' }, { t: 'model-independent geometric ground truth', c: BLUE, b: true },
              { t: ': direct contact 16 % / including plastic spreading 52 %.' }] },
  ], { h: 1.85 });
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 3.02, w: 8.8, h: 1.42,
    fill: { color: 'EAF1F8' }, line: { color: BLUE, width: 1 }, rectRadius: 0.06 });
  s.addText([{ text: '★  External validation — the strongest evidence we have\n',
               options: { bold: true, color: NAVY, fontSize: 12.5 } },
             { text: 'Bazzoun 2026 applied the ', options: { color: DARK, fontSize: 11 } },
             { text: 'same material (LPSCl + NCM811), the same DEM code, and the same resistor-network method',
               options: { color: NAVY, fontSize: 11, bold: true } },
             { text: ', and validated it against ', options: { color: DARK, fontSize: 11 } },
             { text: 'measured EIS and COMSOL FEM', options: { color: NAVY, fontSize: 11, bold: true } },
             { text: ':  network ≈ FEM ≈ experiment, and 32–98× faster.\n', options: { color: DARK, fontSize: 11 } },
             { text: '⇒ our methodology was validated by someone else, not by us.',
               options: { color: NAVY, fontSize: 11, italic: true } }],
            { x: 0.78, y: 3.02, w: 8.44, h: 1.42, fontFace: BFONT, valign: 'middle',
              lineSpacing: 16, margin: 0 });
  s.addNotes('COMSOL 로 하면 되지 않냐는 질문의 답이 여기 있습니다. '
    + '저항망 ≈ FEM ≈ 실험이 남의 논문으로 입증됐고, 우리는 32-98배 빠릅니다.');
}

/* ═══════════════════ 10. R4 — closed-form laws ═══════════════════ */
{
  const s = frame('Results and discussion', 'Bruggeman, Ann. Phys. 416 (1935) · Holm (1967) · Trevisanello, AEM 11 (2021) 2003400');
  bullets(s, [
    { h: 'Closed-form transport laws — and the data independently picks the textbook exponents' },
  ], { h: 0.35 });
  s.addShape(p.ShapeType.rect, { x: 0.6, y: 1.32, w: 8.8, h: 0.78, fill: { color: 'F7F7F7' },
                                 line: { color: 'D0D0D0', width: 0.75 } });
  s.addText([{ text: 'σ_ion  =  σ_grain · Cronau(r_SE) · (ε_eff)^½ · CN² · coverage^½ · f_p³ · C(τ)',
               options: { fontFace: 'Consolas', fontSize: 11, color: NAVY, bold: true, breakLine: true } },
             { text: 'σ_e    =  (σ_S·NCM_S)^(1−p) (σ_P·NCM_P)^p · ε_AM⁴ · √A · (T/d)^β · …',
               options: { fontFace: 'Consolas', fontSize: 11, color: NAVY, bold: true } }],
            { x: 0.78, y: 1.32, w: 8.44, h: 0.78, valign: 'middle', lineSpacing: 17, margin: 0 });
  table(s, [
    ['Exponent', 'Locked value', 'Source', 'Corpus result'],
    ['ε_AM^a  (backbone)', 'a = 4', 'Stauffer–Bruggeman', 'picks exactly 4 out of {2 … 8}'],
    ['√A  (constriction)', '0.5', 'Holm 1967', 'picks exactly 0.5 (symmetric loss)'],
    ['NCM(r)^β  (grain size)', 'β = 1.5', 'Trevisanello 2021', 'picks 1.5'],
    ['(p(1−p))^a  (bimodal)', 'a = 1', 'symmetric mixing', 'within noise'],
  ], { y: 2.28, w: 8.8, colW: [2.2, 1.3, 2.1, 3.2], rowH: 0.29, fs: 10.5 });
  bullets(s, [
    { parts: [{ t: 'LOOCV  σ_ion ' }, { t: '0.975', c: BLUE, b: true }, { t: ' (5 free parameters) · σ_e ' },
              { t: '0.953', c: BLUE, b: true },
              { t: '   — LOOCV = hide one case, learn from the rest, predict it; memorising cannot score.' }] },
    { parts: [{ t: '★ The exponents were ' }, { t: 'taken from the literature and held fixed', b: true },
              { t: ' — the scan below costs ' }, { t: 'zero degrees of freedom', c: BLUE, b: true },
              { t: ', so this is validation, not fitting.' }] },
  ], { y: 3.90, h: 0.72, size: 11 });
  s.addNotes('여기서 강조할 것: 5개 지수를 우리가 맞춘 게 아니라 문헌에서 가져와 고정했고, '
    + '코퍼스가 그 값을 독립적으로 골라냈다는 것입니다.');
}

/* ═══════════════════ 11. R5 — thermal has no scaling law ═══════════════════ */
{
  const s = frame('Results and discussion', 'Bruggeman, Ann. Phys. 416 (1935) 636');
  bullets(s, [
    { h: 'Thermal transport has NO scaling law — and that is the result' },
    { parts: [{ t: 'σ_ion rides one backbone (SE) and σ_e rides one backbone (AM).  Heat instead travels ' },
              { t: 'three paths at once', c: RED, b: true }, { t: ' — AM-AM, AM-SE, SE-SE.' }] },
  ], { h: 0.72 });
  s.addChart(p.ChartType.bar, [
    { name: 'LOOCV', labels: ['A. pure power law', 'B. Bruggeman EMT', 'C. Ridge (14 features)'],
      values: [0.59, 0.0, 0.90] },
  ], { x: 0.55, y: 1.90, w: 4.55, h: 2.35, barDir: 'bar', showTitle: true,
       title: 'Which functional form can represent κ?', titleFontSize: 11, titleColor: NAVY,
       chartColors: [BLUE], showValue: true, dataLabelPosition: 'outEnd', dataLabelFontSize: 10,
       dataLabelColor: DARK, showLegend: false, catAxisLabelColor: '595959',
       valAxisLabelColor: '595959', catAxisLabelFontSize: 9.5, valAxisLabelFontSize: 9,
       valAxisMaxVal: 1.0, valAxisMinVal: 0, valGridLine: { color: 'E0E0E0', size: 0.5 },
       catGridLine: { style: 'none' } });
  bullets(s, [
    { parts: [{ t: 'B (effective-medium theory) gives a ' }, { t: 'negative baseline R²', c: RED, b: true },
              { t: ' (−0.15 … −1.53) — shown as 0 in the chart.' }] },
    { parts: [{ t: 'The ' }, { t: '0.3 LOOCV gap between A and C', c: BLUE, b: true },
              { t: ' is the quantitative proof that composite thermal transport is not a single-backbone scaling law.' }] },
    { parts: [{ t: 'Every lever was exhausted — α sweep, cross terms, greedy over all 246 features, target transforms: ' },
              { t: 'max +0.017 = noise', b: true }, { t: '.' }] },
    { parts: [{ t: '⇒ Ridge is the ' }, { t: 'irreducible representation', c: BLUE, b: true },
              { t: ' at this corpus size — a finding about the physics, not a modelling preference.' }] },
  ], { x: 5.25, y: 1.90, w: 4.25, h: 2.4, size: 11 });
  s.addNotes('"왜 열만 회귀냐, 일관성이 없다"는 질문이 옵니다. 답: 그게 결과입니다. '
    + '단일 골격이 아니라서 원리적으로 스케일링이 안 됩니다.');
}

/* ═══════════════════ 12. R6 — SDCP decomposition ═══════════════════ */
{
  const s = frame('Results and discussion', 'Bard & Faulkner, Electrochemical Methods (2001) — Butler–Volmer');
  bullets(s, [
    { h: 'Why a mixed-conducting additive helps — decomposed for the first time' },
    { parts: [{ t: 'Same skeleton, same property table, same boundary conditions; only the additive differs (3.18 mAh/cm², 72.5 µm).' }] },
    { parts: [{ t: 'σ_e ' }, { t: '+52.0 %', c: BLUE, b: true }, { t: '  ·  σ_ion ' },
              { t: '+5.6 %', c: BLUE, b: true }, { t: '  ·  reaction interface area ' },
              { t: '+18 %', c: BLUE, b: true },
              { t: '   →  total polarization at 1C:  46 → 41 mV.' }] },
  ], { h: 1.0 });
  s.addChart(p.ChartType.bar, [
    { name: 'contribution to the 4.7 mV gap',
      labels: ['reaction area +18%', 'ionic σ +5.6%', 'electronic σ +52%'],
      values: [3.6, 1.0, 0.002] },
  ], { x: 0.55, y: 2.12, w: 4.7, h: 2.30, barDir: 'bar', showTitle: true,
       title: 'Decomposition of the 4.7 mV polarization gap (mV)', titleFontSize: 11,
       titleColor: NAVY, chartColors: [NAVY], showValue: true, dataLabelPosition: 'outEnd',
       dataLabelFontSize: 10, dataLabelColor: DARK, showLegend: false,
       catAxisLabelColor: '595959', valAxisLabelColor: '595959', catAxisLabelFontSize: 9.5,
       valAxisLabelFontSize: 9, valGridLine: { color: 'E0E0E0', size: 0.5 },
       catGridLine: { style: 'none' } });
  bullets(s, [
    { parts: [{ t: 'reaction area  →  ' }, { t: '3.6 mV (78 %)', c: BLUE, b: true }] },
    { parts: [{ t: 'ionic σ  →  1.0 mV (22 %)' }] },
    { parts: [{ t: 'electronic σ  →  ' }, { t: '0.002 mV (≈ 0 %)', c: RED, b: true }] },
    { parts: [{ t: '★ At low rate the voltage gap is governed by ' },
              { t: 'reaction area, not by σ_e', c: BLUE, b: true },
              { t: ' — σ_e is already 10⁴× better than σ_ion, so it is not the bottleneck.' }] },
    { parts: [{ t: 'σ_e matters where the current is large: ' }, { t: 'high rate and thick electrodes', b: true }, { t: '.' }] },
    { parts: [{ t: 'This split is ' }, { t: 'impossible experimentally', c: RED, b: true },
              { t: ' — EIS and the discharge curve give only the sum.' }] },
  ], { x: 5.40, y: 2.12, w: 4.1, h: 2.35, size: 10.5 });
  s.addNotes('"σ_e 를 52% 올렸는데 0.002 mV 라고?"라는 질문이 반드시 옵니다. '
    + '답: 직렬 저항에서는 작은 쪽이 지배합니다. 전자망은 이미 병목이 아닙니다.');
}

/* ═══════════════════ 13. R7 — series-resistance relief ═══════════════════ */
{
  const s = frame('Results and discussion', 'σ_SDCP value is ASSUMED — swept, not asserted');
  bullets(s, [
    { h: 'The additive relieves series resistance — it does not carry the current' },
    { parts: [{ t: 'Swept the additive conductivity 15 → 1500 S/cm with the ' },
              { t: 'microstructure and ionic network held fixed', b: true }, { t: '.' }] },
  ], { h: 0.72 });
  s.addChart(p.ChartType.line, [
    { name: 'σ_e gain vs SBE (%)', labels: ['15', '50', '150', '250', '1500'],
      values: [0.8, 25.8, 45.5, 52.0, 63.4] },
    { name: 'SDCP dissipation share (%)', labels: ['15', '50', '150', '250', '1500'],
      values: [19.6, 16.3, 10.0, 7.3, 1.7] },
  ], { x: 0.55, y: 1.90, w: 4.85, h: 2.55, showTitle: true,
       title: 'Gain rises while the additive’s share of dissipation falls',
       titleFontSize: 10.5, titleColor: NAVY, chartColors: [NAVY, RED], lineSize: 2.5,
       lineDataSymbolSize: 7, showLegend: true, legendPos: 'b', legendFontSize: 9,
       catAxisTitle: 'assumed σ_SDCP (S/cm)', showCatAxisTitle: true, catAxisTitleFontSize: 9,
       catAxisLabelColor: '595959', valAxisLabelColor: '595959', catAxisLabelFontSize: 9,
       valAxisLabelFontSize: 9, valGridLine: { color: 'E0E0E0', size: 0.5 },
       catGridLine: { style: 'none' } });
  bullets(s, [
    { parts: [{ t: '★ The gain grows (+0.8 → +63.4 %) while the additive’s ' },
              { t: 'share of dissipation falls (19.6 → 1.7 %)', c: RED, b: true }, { t: '.' }] },
    { parts: [{ t: 'A phase that ' }, { t: 'carried' }, { t: ' the current would show a ' },
              { t: 'rising', b: true }, { t: ' share.  The inversion is the signature of a phase that ' },
              { t: 'relieves a series resistance', c: BLUE, b: true }, { t: '.' }] },
    { parts: [{ t: '⇒ Practical consequence: ' },
              { t: 'the conclusion does not depend on knowing σ_SDCP', c: BLUE, b: true },
              { t: '.  Even at the worst value (15 S/cm) the additive costs nothing (+0.8 %).' }] },
    { parts: [{ t: 'Ionic conductivity and reaction area are unchanged across the sweep — the effect is isolated to the electronic channel.' }] },
  ], { x: 5.55, y: 1.90, w: 3.95, h: 2.55, size: 10.5 });
  takeaway(s, 'We claim HOW the additive helps — a mechanism — not HOW MUCH.  The mechanism survives the whole sweep.', 4.62);
  s.addNotes('σ_SDCP 250 은 측정값이 아니라 assumed 입니다. 그래서 값 하나로 결론을 내지 않고 '
    + '5점을 스윕했고, 결론 두 가지가 모두 값에 안 걸립니다.');
}

/* ═══════════════════ 14. R8 — what we do not know ═══════════════════ */
{
  const s = frame('Results and discussion', 'Bucci et al., J. Mater. Chem. A (2017) · Yun et al., Energy Storage Mater. (2023)');
  bullets(s, [
    { h: 'What we do NOT know yet — two limits, quantified' },
  ], { h: 0.35 });
  s.addText([{ text: '(a)  Cycle degradation is dominated by chemistry — contact loss is a lower bound of ~2 %',
               options: { bold: true, color: NAVY, fontSize: 12 } }],
            { x: 0.6, y: 1.22, w: 8.8, h: 0.26, fontFace: BFONT, margin: 0 });
  table(s, [
    ['Piece', 'Physics', 'Share of fade', 'Anchor'],
    ['contact–mechanical', 'shrinkage → contact opening (CZM)', '~2 % (lower bound)', 'mono 1.05× vs bimodal 1.51×'],
    ['chemical CEI', 'diffusion-limited √N growth', '~98 %', 'Yun 2023 (this lab) R_ct 2.87× @100 cyc'],
    ['OTHER', 'skeleton rearrangement · SE decomposition · Li side', 'dominant in coated cells', 'awaiting experiment'],
  ], { x: 0.6, y: 1.54, w: 8.8, colW: [1.75, 3.0, 1.65, 2.4], rowH: 0.30, fs: 10 });
  bullets(s, [
    { parts: [{ t: 'The ' }, { t: 'magnitude is anchored to an experimental endpoint', b: true },
              { t: '; the ' }, { t: 'shape (√N) is labelled ASSUMED', c: RED, b: true },
              { t: ' — one endpoint cannot distinguish √N from linear.  A tool decides it once ≥ 4 experimental points exist.' }] },
  ], { x: 0.55, y: 2.82, w: 8.9, h: 0.42, size: 10.5 });
  figbox(s, 0.6, 3.32, 8.8, 1.18,
         'contact-mechanical ~2 % vs chemical CEI ~98 % — three-way split of the fade');
  takeaway(s, 'The magnitude is anchored to experiment; the shape stays labelled ASSUMED until four cycle points exist.', 4.62);
  s.addNotes('열화의 98 % 가 화학이라는 것이 결론입니다. 접촉 2 % 는 반드시 "하한"이라고 '
    + '말해야 합니다 — OTHER 가 모델 밖에 있습니다.');
}

/* ═══════ 15. R9 — a rejected assumption, traced to its cause ═══════ */
{
  const s = frame('Results and discussion', 'this work, Aug 2026 — rejection → mechanism → descriptor → grid check');
  bullets(s, [
    { h: 'A rejected assumption, traced to its cause — and then to a one-number fix' },
    { parts: [{ t: 'We indexed the SE stress response by ' }, { t: 'phi = V_SE /(A*h - V_AM)', b: true },
              { t: ' ("how full is the SE\u2019s own space") and assumed one curve would serve every electrode.  Measured at matched loading rate, ' },
              { t: 'it does not: 2.96 - 3.83x at the same phi', c: RED, b: true }, { t: '.' }] },
  ], { h: 0.80 });
  s.addChart(p.ChartType.line, [
    { name: 'sigma at phi = 0.72', labels: ['501', '620', '745', '916', '1458'],
      values: [0.7001, 0.5457, 0.4921, 0.4671, 0.3743] },
  ], { x: 0.55, y: 1.95, w: 4.3, h: 2.50, showTitle: true,
       title: 'One geometric descriptor collapses the composition effect',
       titleFontSize: 10.5, titleColor: NAVY, chartColors: [NAVY],
       lineSize: 2.5, lineDataSymbolSize: 8, showLegend: false, showValue: true,
       dataLabelPosition: 't', dataLabelFontSize: 9, dataLabelColor: DARK,
       catAxisTitle: 'channel width  d_h = V_free / S_AM   (nm)', showCatAxisTitle: true,
       catAxisTitleFontSize: 9, valAxisTitle: 'sigma (GPa)', showValAxisTitle: true,
       valAxisTitleFontSize: 9, catAxisLabelColor: '595959', valAxisLabelColor: '595959',
       catAxisLabelFontSize: 9, valAxisLabelFontSize: 9,
       valGridLine: { color: 'E0E0E0', size: 0.5 }, catGridLine: { style: 'none' } });
  bullets(s, [
    { parts: [{ t: '1. ' }, { t: 'Mechanism', c: BLUE, b: true },
              { t: ' — von Mises caps only the shape-changing stress, ' },
              { t: 'not the pressure', c: RED, b: true },
              { t: '.  One bed stops at 0.278 GPa (below the 0.30 yield) = still flowing into voids; the other reaches ' },
              { t: '1.012 GPa (3.4x yield)', c: RED, b: true },
              { t: ' = pressurised, unable to reach the remaining voids.' }] },
    { parts: [{ t: '2. ' }, { t: 'The cause is composition, not thickness', c: BLUE, b: true },
              { t: ' — five beds matched to +/-1.4 % in thickness, only the particle-size ratio varied, give ' },
              { t: '1.87x', b: true }, { t: ', ' }, { t: 'perfectly monotonic', b: true },
              { t: ' in that ratio (by chance about 7e-5).' }] },
    { parts: [{ t: '3. ' }, { t: 'The fix', c: BLUE, b: true },
              { t: ' — index by channel width instead:  ' },
              { t: 'sigma proportional to d_h^-0.54,  R2 = 0.935', b: true },
              { t: '.  A new electrode then needs only its d_h, not a new five-point curve.' }] },
    { parts: [{ t: '4. ' }, { t: 'Not a grid artefact', c: BLUE, b: true },
              { t: ' — refining the grid ' }, { t: 'strengthens', b: true },
              { t: ' the effect (+5-10 %): an unresolved constriction simply vanishes and lets material through.  So -0.54 is a ' },
              { t: 'lower bound', b: true }, { t: ' on the magnitude.' }] },
  ], { x: 5.00, y: 1.95, w: 4.5, h: 2.55, size: 10 });
  takeaway(s, 'A rejected assumption became a mechanism, a descriptor, and a convergence check — that is a result.', 4.62);
  s.addNotes('Q: "전이가 기각됐으면 지금까지 결과가 다 틀린 것 아니냐" — 아닙니다. 기각된 것은 '
    + '곡선을 다른 전극에 옮기는 것이고, 각 전극에서 직접 계산한 값은 무관합니다. '
    + '4번은 제 사전 예상이 부호부터 틀렸던 경우입니다 — 미해상이면 뻣뻣해질 줄 알았는데 '
    + '실제로는 협착이 격자에서 사라져 오히려 무릅니다. 그래서 정밀화가 효과를 키웁니다.');
}

/* ═══════════════════ 15. Future plan ═══════════════════ */
{
  const s = frame('Future plan', null);
  bullets(s, [{ h: 'Closing the last verification loop, then scaling to design' }], { h: 0.32 });
  s.addText([{ text: '①  Ready to run (code complete)', options: { bold: true, color: NAVY, fontSize: 12 } }],
            { x: 0.6, y: 1.18, w: 4.3, h: 0.24, fontFace: BFONT, margin: 0 });
  table(s, [
    ['Item', 'Needs', 'Gives'],
    ['PyBaMM matched-condition parity', 'one GPU day', 'defensible → bullet-proof'],
    ['σ(φ, d_h) exponent at finer grid', 'n_grid 288 (~4 h)', 'converged value (now bounded: |slope| ≥ 0.54)'],
    ['COMSOL hybrid export', 'bridge geometry', 'share results in COMSOL users’ language'],
  ], { x: 0.6, y: 1.46, w: 4.35, colW: [1.85, 1.05, 1.45], rowH: 0.36, fs: 9.5 });
  s.addText([{ text: '②  Awaiting anchors — we do not pretend to know',
               options: { bold: true, color: NAVY, fontSize: 12 } }],
            { x: 5.15, y: 1.18, w: 4.3, h: 0.24, fontFace: BFONT, margin: 0 });
  bullets(s, [
    { parts: [{ t: 'LPSCl decomposition activation energy — ' },
              { t: 'confirmed absent from the literature', c: RED, b: true },
              { t: ' ⇒ we do NOT multiply heat into degradation by Arrhenius.' }] },
    { parts: [{ t: 'CEI √N shape confirmation (≥ 4 experimental points)' }] },
    { parts: [{ t: 'measured σ_e of the additive · binding energy from DFT · i₀ split for single- vs poly-crystal' }] },
  ], { x: 5.10, y: 1.46, w: 4.4, h: 1.30, size: 10.5 });
  s.addText([{ text: '③  Machine learning — the differentiator is physics-derived features',
               options: { bold: true, color: NAVY, fontSize: 12 } }],
            { x: 0.6, y: 3.00, w: 8.8, h: 0.24, fontFace: BFONT, margin: 0 });
  bullets(s, [
    { parts: [{ t: 'Now: design → σ triad ' }, { t: 'surrogate', b: true },
              { t: ' (LOOCV 0.975 / 0.953 / 0.90) — seconds instead of hours.' }] },
    { parts: [{ t: 'Next: ' }, { t: 'cycle-life surrogate', c: BLUE, b: true },
              { t: ' = 13 design + ' }, { t: '15 physics features', b: true },
              { t: ' (σ triad · coverage · CN · τ · current focusing · reaction area) + cycle → R_int(N), retention.' }] },
    { parts: [{ t: 'Then: ' }, { t: 'closed design loop', c: BLUE, b: true },
              { t: ' (symbolic regression + Bayesian optimisation → recommend the next composition to make).' }] },
    { parts: [{ t: 'Materials side: ' }, { t: 'MLIP', b: true },
              { t: ' (MACE / UMA) to resolve LPSCl disorder and produce DFT anchors — continuing from the April talk.' }] },
  ], { x: 0.55, y: 3.28, w: 8.9, h: 1.25, size: 10.5 });
  takeaway(s, 'Experiments say "this composition is better".  This pipeline says why, at which contact, and by how much.', 4.68);
  s.addNotes('마지막 문장이 이 발표의 결론입니다.');
}

/* ═══════════════════ Appendix ═══════════════════ */
{
  const s = p.addSlide();
  s.addShape(p.ShapeType.rect, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: NAVY } });
  s.addText('Appendix', { x: 0.7, y: 2.35, w: 8.6, h: 0.7, fontFace: TFONT, fontSize: 34,
                          bold: true, color: 'FFFFFF', align: 'center', margin: 0 });
  s.addText('A. technical backup   ·   B. glossary & symbol conventions   ·   C. anticipated questions',
            { x: 0.7, y: 3.10, w: 8.6, h: 0.35, fontFace: BFONT, fontSize: 13, color: 'CADCFC',
              align: 'center', margin: 0 });
}
{
  const s = frame('Appendix A · Material parameters live on three levels',
                  'Sakuda et al., Sci. Rep. 3 (2013) 2261 · Cronau et al., ACS Energy Lett. 6 (2021) 3072');
  bullets(s, [
    { h: 'The 18× softening is a proxy for missing mechanisms — never claimed as a material property' },
  ], { h: 0.35 });
  table(s, [
    ['Level', 'Value', 'What it means'],
    ['Real bulk LPSCl', 'E = 24 GPa', 'measured single-crystal / dense-pellet modulus (literature)'],
    ['DEM effective', 'E_eff = 1.35 GPa', 'lumps rearrangement + grain-boundary sliding + micro-fracture that rigid spheres cannot do'],
    ['MPM champion', 'E = 1.53 GPa, ν = 0.49\n(K = 25.5, µ = 0.51 GPa)', 'softening confined to SHEAR — bulk stiffness stays at the dense-solid value'],
  ], { y: 1.42, w: 8.8, colW: [1.7, 2.1, 5.0], rowH: 0.52, fs: 10.5 });
  bullets(s, [
    { parts: [{ t: 'Why it is not a free fit — ' }, { t: 'three independent routes demand the same value', c: BLUE, b: true }, { t: ':' }] },
    { parts: [{ t: '① pure-SE contact overlap 11–12 % is reproduced (Cronau)  ② an entirely different code and physics (MPM continuum) independently requires the same 18×  ③ experimental porosity.' }] },
    { parts: [{ t: 'Heckel compaction: R² 0.965 · yield pressure P_y = 138 MPa · σ_y,eff 46 MPa — ' },
              { t: '6.5× softer than the single crystal', b: true }, { t: ', which quantifies the granular softening.' }] },
  ], { y: 3.55, h: 1.0, size: 10.5 });
}
{
  const s = frame('Appendix B · Glossary — terms as used in the field', 'full list with references: docs/seminar_20260806_glossary.md');
  table(s, [
    ['Term', 'In one line', 'Reference'],
    ['DEM (discrete element method)', 'each particle is a rigid sphere; solve Newton', 'Cundall & Strack 1979'],
    ['MPM (material point method)', 'continuum, carried on material points', 'Sulsky et al. 1994'],
    ['Constriction resistance', 'extra resistance of a narrow contact neck  R = 1/(2σa)', 'Holm 1967 · Maxwell 1873'],
    ['Plastic contact area', 'A = F/H — larger than the elastic Hertz area', 'Tabor 1948'],
    ['Percolation', 'is there a connected path end to end?', 'Stauffer & Aharony'],
    ['Tortuosity τ', 'how far ions detour;  σ_eff = σ_bulk·ε/τ  (linear convention)', '⚠ state the convention'],
    ['Coordination number CN', 'how many neighbours a particle touches', 'packing standard'],
    ['Coverage', 'fraction of AM surface covered by SE', 'Hertz 16 % / Tabor 52 %'],
    ['Overpotential η', 'the extra voltage needed to drive the reaction', 'Bard & Faulkner'],
    ['CEI', 'resistive interphase that grows every cycle', 'Yun et al. 2023'],
  ], { y: 1.18, w: 8.8, colW: [2.4, 4.3, 2.1], rowH: 0.29, fs: 10 });
  s.addText([{ text: '⚠  Symbol collisions to state explicitly:  ', options: { bold: true, color: RED, fontSize: 10.5 } },
             { text: 'φ = potential (V) vs volume fraction — use ε for fractions  ·  σ = conductivity vs stress — always give units  ·  τ convention (linear vs squared) differs between papers',
               options: { color: DARK, fontSize: 10.5 } }],
            { x: 0.6, y: 4.42, w: 8.8, h: 0.55, fontFace: BFONT, valign: 'top', lineSpacing: 14, margin: 0 });
}
{
  const s = frame('Appendix C · Anticipated questions', 'full set (40 Q&A): docs/seminar_20260806_script.md');
  table(s, [
    ['Question', 'First sentence of the answer'],
    ['Isn’t this just fitted to experiment?', 'There is exactly one calibration point; everything after it is a prediction — and the two models never see each other.'],
    ['Isn’t the 18× softening a free fit?', 'If it were free, three independent routes would not demand the same value.'],
    ['σ_e up 52 % but only 0.002 mV?', 'Yes — in a series resistance the smaller one dominates, and σ_e was already 10⁴× better.'],
    ['Where does σ_SDCP = 250 S/cm come from?', 'It is assumed, not measured — which is why we swept 15–1500 and claim only the mechanism.'],
    ['If the transfer was rejected, is everything wrong?', 'No — what was rejected is moving one curve to another bed; quantities computed per bed are unaffected.'],
    ['Why not just use COMSOL?', 'For σ and microstructure fields we can replace it — and an independent paper proved that; for liquid systems and full cells we cannot.'],
    ['How does this help an experimentalist?', 'It decomposes why something works, points at what to fix, and screens candidates before they are made.'],
    ['What is your weakest link?', 'Three: the external numerical parity run, the measured additive conductivity, and the experimental confirmation of the √N shape.'],
  ], { y: 1.18, w: 8.8, colW: [3.0, 5.8], rowH: 0.40, fs: 9.5 });
}

const out = process.argv[2] || 'seminar_20260806.pptx';
p.writeFile({ fileName: out }).then(() => console.log('wrote ' + out));

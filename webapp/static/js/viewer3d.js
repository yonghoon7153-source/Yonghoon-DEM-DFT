/**
 * viewer3d.js - Three.js 3D Electrode Viewer for DEM Analysis
 * Uses ES module imports via importmap. Self-contained single file.
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

/* ── colour constants ──────────────────────────────────────── */
const COL = {
  AM_P: 0x222222, AM_S: 0x888888, SE: 0xf5e6a3,
  SE_TOP_REACH: 0x34d399, SE_NON_REACH: 0xf87171,
  SE_BOTTOM: 0xfbbf24, SE_TOP: 0x22d3ee,
  PATH: 0xffd700, BG: 0xf5f5f5,
  MESH: 0x4f9bff,          // bright blue — compaction plate
  ATOMS_ONLY: 0xe8e8e8,    // near-white, still contrasts #f5f5f5 bg (process view)
  DIM: 0xe5e7eb,           // background colour for non-highlighted particles
};
const OPA = { SE: 0.85, MESH: 0.55 };

/* matplotlib 'hot' colormap (black→red→yellow→white) for the SE plastic-strain Σdg field. */
function hotColor(t, c) {
  t = Math.max(0, Math.min(1, t));
  let r, g, b;
  if (t < 0.365) { r = t / 0.365; g = 0; b = 0; }
  else if (t < 0.746) { r = 1; g = (t - 0.365) / 0.381; b = 0; }
  else { r = 1; g = 1; b = (t - 0.746) / 0.254; }
  c.setRGB(r, g, b); return c;
}

/* View-mode colour palettes — Auerbach + Lawn 1998 fracture stages.
 * Mapped to ColorBrewer YlOrRd 5-class (sequential), which is the
 * standard academic palette for ordered-severity scalar data: pale
 * gold → amber → warm red → deep crimson reads as monotonically
 * increasing damage even in grayscale prints. */
const STAGE_COL = {
  intact:        0xd9d9d9,   // neutral light grey
  microcrack:    0xffeda0,   // pale gold
  multicrack:    0xfeb24c,   // amber
  fragmentation: 0xf03b20,   // warm vermillion
  pulverization: 0x800026,   // deep crimson
};
const STAGE_RANK = { intact: 0, microcrack: 1, multicrack: 2,
                      fragmentation: 3, pulverization: 4 };

function jetColor(t) {
  // t ∈ [0,1] → blue→cyan→green→yellow→red
  const r = Math.max(0, Math.min(1, 1.5 - Math.abs(4 * t - 3)));
  const g = Math.max(0, Math.min(1, 1.5 - Math.abs(4 * t - 2)));
  const b = Math.max(0, Math.min(1, 1.5 - Math.abs(4 * t - 1)));
  return (Math.round(r * 255) << 16) | (Math.round(g * 255) << 8) | Math.round(b * 255);
}
function rygColor(t) {
  // t ∈ [0,1] → red→yellow→green (for coverage low→high)
  if (t < 0.5) {
    const u = t * 2;
    return (255 << 16) | (Math.round(u * 255) << 8) | 0;
  }
  const u = (t - 0.5) * 2;
  return (Math.round((1 - u) * 255) << 16) | (255 << 8) | 0;
}

/* Coolwarm (blue → white → red) sequential colormap — academic
 * standard for ordered scalar fields.  Anchors:
 *   t = 0.0  →  rgb(59, 76, 192)    deep blue
 *   t = 0.5  →  rgb(221, 221, 221)  near-white
 *   t = 1.0  →  rgb(180,  4,  38)   deep red
 * Linear interpolation in each half. */
function coolwarmColor(t) {
  t = Math.max(0, Math.min(1, t));
  let r, g, b;
  if (t < 0.5) {
    const u = t * 2;
    r = Math.round(59  + (221 - 59 ) * u);
    g = Math.round(76  + (221 - 76 ) * u);
    b = Math.round(192 + (221 - 192) * u);
  } else {
    const u = (t - 0.5) * 2;
    r = Math.round(221 + (180 - 221) * u);
    g = Math.round(221 + (4   - 221) * u);
    b = Math.round(221 + (38  - 221) * u);
  }
  return (r << 16) | (g << 8) | b;
}

/* ColorBrewer RdYlGn 5-class diverging — muted "red/yellow/green"
 * with proper academic anchors. Continuous interpolation between
 * the 5 anchor points so the legend can show 0/50/100 % swatches
 * but per-particle colours fall on the smooth gradient.  Used by
 * the Coverage Heat (AM) view in place of the saturated RGB
 * primaries that read as a traffic-light. */
const _RDYLGN = [
  [0.00, 0xd7, 0x19, 0x1c],
  [0.25, 0xfd, 0xae, 0x61],
  [0.50, 0xff, 0xff, 0xbf],
  [0.75, 0xa6, 0xd9, 0x6a],
  [1.00, 0x1a, 0x96, 0x41],
];
function rdylgnColor(t) {
  t = Math.max(0, Math.min(1, t));
  for (let i = 0; i < _RDYLGN.length - 1; i++) {
    const a = _RDYLGN[i], b = _RDYLGN[i + 1];
    if (t <= b[0]) {
      const u = (t - a[0]) / (b[0] - a[0]);
      const r = Math.round(a[1] + (b[1] - a[1]) * u);
      const g = Math.round(a[2] + (b[2] - a[2]) * u);
      const bl = Math.round(a[3] + (b[3] - a[3]) * u);
      return (r << 16) | (g << 8) | bl;
    }
  }
  const last = _RDYLGN[_RDYLGN.length - 1];
  return (last[1] << 16) | (last[2] << 8) | last[3];
}
/* COMSOL-style coolwarm (blue → white → red) colormap.
 * t ∈ [0,1].  Anchors:
 *   t = 0.0  →  (59, 76, 192)   deep blue
 *   t = 0.5  →  (221, 221, 221) near-white
 *   t = 1.0  →  (180,  4,  38)  deep red
 * Linear interpolation in each half. */
/* ── STEP4-v2 동역학 필드 렌더 (step4_dyn.py --viz-out JSON) ──
 * st4_soc : 입자별 반경방향 SOC(코어-셸)를 시간·깊이(peel) 슬라이더로 —
 *           구형 1D 확산이라 각도방향은 균일(동심 링), 단면 뷰와 조합하면
 *           연차보고서식 입자 내부 그라데이션 단면이 됨.
 * st4_face: BV 면별 반응전류 i/ī(RELATIVE, v1 jrxn 규약)를 복셀큐브 필드로 —
 *           같은 입자 표면 안에서도 접촉 기하에 따른 비균일 얼룩이 보임. */
/* st4 viz 파일 열기/교체 — 로드된 상태에서도 다른 파일로 바꿀 수 있게 (구버전 자동로드 덮어쓰기).
   버튼 id `${btnId}`를 legend에 두고 이 함수로 배선.  성공 시 state.st4 교체 + 서버 저장 + 재렌더. */
function wireSt4Picker(state, btnId, mode) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.onclick = () => {
    const inp = document.createElement('input');
    inp.type = 'file'; inp.accept = '.json,application/json'; inp.style.display = 'none';
    document.body.appendChild(inp);
    inp.onchange = (e) => {
      const f = e.target.files && e.target.files[0];
      if (!f) { inp.remove(); return; }
      const rd = new FileReader();
      rd.onload = () => {
        let obj;
        try { obj = JSON.parse(rd.result); } catch (err) { alert('step4_viz JSON 파싱 실패: ' + err); inp.remove(); return; }
        if (!obj || obj.kind !== 'step4_viz') { alert('step4_viz 형식이 아니에요 (kind=' + (obj && obj.kind) + ')'); inp.remove(); return; }
        state.st4 = obj;
        state._st4SrcName = (f.name || '').replace(/\.json$/i, '');   // 📂로 부른 파일명 = 다운로드 이름의 정체 (payload 케이스보다 우선)
        if (state._st4Url) fetch(state._st4Url, { method: 'POST',
          headers: { 'Content-Type': 'application/json' }, body: rd.result })
          .then(r => { if (r && r.ok) console.log('st4 viz 서버 저장(교체)됨'); }).catch(() => {});
        inp.remove();
        applyViewMode(state, mode);
      };
      rd.onerror = () => { alert('step4_viz 파일 읽기 실패'); inp.remove(); };
      rd.readAsText(f);
    };
    inp.click();
  };
}

/* 방전곡선 다운로드 — viz json의 curve(전 스텝 V/x̄/η/Q)를 V vs 면적용량으로 그려 PNG(고해상)+CSV.
   면적용량 = x̄→SOC창% × areal(field_scale 자동산출 or c_max 추정).  버튼 id로 배선. */
function wireVProfileDownload(state, btnId) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.onclick = () => {
    const st = state.st4, cu = st && st.curve;
    if (!cu || !cu.V || !cu.V.length) { alert('이 viz엔 곡선 데이터가 없어요 — 최신 step4_dyn(--viz-out)로 재생성 필요'); return; }
    const x0 = st.x0, x100 = st.x100, win = Math.abs(x100 - x0);
    // 면적용량: payload field_scale 있으면 그 값, 없으면 Chen2020 c_max로 추정 (단위 정합만)
    const mm = (state.data && state.data.mpm_metrics) || {};
    const s3 = mm.step3 || {};
    const ar = ((s3.field_scale_e || {}).areal_capacity_mAh_cm2)
      || (st.c_max_mol_m3 ? 96485 * st.c_max_mol_m3 * win / 3.6e6 * 0.00307 / 0.00307 * 3.1 / 3.1 : 0);  // fallback 대략
    const useCap = ar > 0;
    // 충전은 x̄가 x100→x0로 감소 → '충전된 용량' = (x100−x̄); 방전은 (x̄−x0).  이걸 안 가르면
    // 충전 곡선이 좌우 반전(4.25V 플래토가 왼쪽)으로 그려짐.
    const qOf = x => (st.charge ? ((st.x100 ?? x100) - x) : (x - x0));
    const xs = cu.x_mean.map(x => useCap ? qOf(x) / win * ar : 100 * qOf(x) / win);
    // 과전압 분해 (신형 viz만: I_A+eta_diff_mV 필요 — 구형 json은 V-곡선 단일 패널 유지)
    const hasD = !!(cu.I_A && cu.eta_diff_mV);
    let eo = null, ek = null, ed = null, er = null;
    if (hasD) {
      const iAbs = cu.I_A.map(v => Math.max(Math.abs(v), 1e-30));
      eo = iAbs.map((I, i) => (Math.abs(cu.Q_ohm_e_W[i]) + Math.abs(cu.Q_ohm_i_W[i])) / I * 1e3);  // mV
      ek = cu.eta_kin_mV; ed = cu.eta_diff_mV;
      if ((cu.Q_rint_W || []).some(q => Math.abs(q) > 0))
        er = iAbs.map((I, i) => Math.abs(cu.Q_rint_W[i]) / I * 1e3);
    }
    // 고해상 캔버스 직접 렌더 (분해 패널 있으면 2단)
    const W = 1200, H = hasD ? 1180 : 780, mL = 130, mR = 40, mT = 50;
    const b1 = hasD ? 620 : H - 90;                     // V-패널 바닥
    const t2 = 690, b2 = H - 90;                        // 분해 패널 (hasD일 때만 사용)
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
    const g = cv.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
    const V = cu.V, vlo = Math.min(...V), vhi = Math.max(...V), xlo = Math.min(...xs), xhi = Math.max(...xs, xlo + 1e-9);
    const PX = x => mL + (x - xlo) / (xhi - xlo) * (W - mL - mR), PY = v => mT + (1 - (v - vlo) / (vhi - vlo)) * (b1 - mT);
    g.strokeStyle = '#d1d5db'; g.lineWidth = 1.5; g.strokeRect(mL, mT, W - mL - mR, b1 - mT);
    g.strokeStyle = '#f1f3f5'; g.lineWidth = 1;
    for (let i = 1; i < 5; i++) { const gy = mT + (b1 - mT) * i / 5; g.beginPath(); g.moveTo(mL, gy); g.lineTo(W - mR, gy); g.stroke(); }
    g.strokeStyle = st.charge ? '#d97706' : '#1f6fb2'; g.lineWidth = 3; g.beginPath();
    V.forEach((v, i) => { const x = PX(xs[i]), y = PY(v); i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.stroke();
    g.fillStyle = '#111'; g.font = '22px sans-serif'; g.textAlign = 'center';
    g.save(); g.translate(38, mT + (b1 - mT) / 2); g.rotate(-Math.PI / 2);
    g.fillText('Cell voltage (V vs Li/Li⁺)', 0, 0); g.restore();
    g.font = '16px sans-serif'; g.textAlign = 'right';
    for (let i = 0; i <= 5; i++) { const v = vlo + (vhi - vlo) * i / 5; g.fillText(v.toFixed(2), mL - 8, PY(v) + 5); }
    if (hasD) {
      // ── 과전압 분해 패널: η_ohm(e+i) / η_kin / η_diff (+η_rint) vs 같은 x축 ──
      const series = [[eo, '#8a5cf6', 'η_ohm (e+i)'], [ek, '#e8871e', 'η_kin'], [ed, '#2a9d8f', 'η_diff']];
      if (er) series.push([er, '#6b7280', 'η_Rint']);
      const ehi = Math.max(...series.flatMap(s => s[0]).filter(v => isFinite(v)), 1e-9) * 1.06;
      const PY2 = v => t2 + (1 - v / ehi) * (b2 - t2);
      g.strokeStyle = '#d1d5db'; g.lineWidth = 1.5; g.strokeRect(mL, t2, W - mL - mR, b2 - t2);
      g.strokeStyle = '#f1f3f5'; g.lineWidth = 1;
      for (let i = 1; i < 4; i++) { const gy = t2 + (b2 - t2) * i / 4; g.beginPath(); g.moveTo(mL, gy); g.lineTo(W - mR, gy); g.stroke(); }
      series.forEach(([ys, c]) => {
        g.strokeStyle = c; g.lineWidth = 2.5; g.beginPath();
        ys.forEach((v, i) => { const x = PX(xs[i]), y = PY2(Math.max(v, 0)); i ? g.lineTo(x, y) : g.moveTo(x, y); });
        g.stroke();
      });
      g.font = '16px sans-serif'; g.fillStyle = '#111'; g.textAlign = 'right';
      for (let i = 0; i <= 4; i++) { const v = ehi * i / 4; g.fillText(v.toFixed(0), mL - 8, PY2(v) + 5); }
      g.save(); g.translate(38, t2 + (b2 - t2) / 2); g.rotate(-Math.PI / 2);
      g.textAlign = 'center'; g.font = '20px sans-serif'; g.fillText('Overpotential (mV)', 0, 0); g.restore();
      g.textAlign = 'left'; g.font = 'bold 15px sans-serif';
      let lx = mL + 14;
      series.forEach(([, c, lab]) => {
        g.strokeStyle = c; g.lineWidth = 3; g.beginPath(); g.moveTo(lx, t2 + 18); g.lineTo(lx + 26, t2 + 18); g.stroke();
        g.fillStyle = '#111'; g.fillText(lab, lx + 32, t2 + 23); lx += 32 + g.measureText(lab).width + 26;
      });
    }
    const xAxisY = hasD ? b2 : b1;
    g.fillStyle = '#111'; g.font = '22px sans-serif'; g.textAlign = 'center';
    g.fillText(useCap ? (st.charge ? 'Charged capacity (mAh cm⁻²)' : 'Delivered capacity (mAh cm⁻²)')
               : (st.charge ? 'Charged SOC window (%)' : 'SOC window (%)'), mL + (W - mL - mR) / 2, H - 30);
    g.font = '16px sans-serif';
    for (let i = 0; i <= 5; i++) { const x = xlo + (xhi - xlo) * i / 5; g.fillText(x.toFixed(useCap ? 2 : 0), PX(x), xAxisY + 24); }
    g.textAlign = 'left'; g.font = 'bold 18px sans-serif';
    g.fillText(`STEP4-v2 ${st.charge ? '충전' : '방전'} ${st.c_rate}C  (${(state.data && state.data.case) || ''})${hasD ? '  ·  과전압 분해' : ''}`, mL, mT - 18);
    const dl = (url, fn) => { const a = document.createElement('a'); a.href = url; a.download = fn; document.body.appendChild(a); a.click(); a.remove(); };
    const _cn = String(state._st4SrcName || (state.data && state.data.case) || '').replace(/[^A-Za-z0-9._-]/g, '').slice(0, 48);
    const base = `step4_${st.charge ? 'charge' : 'discharge'}_${st.c_rate}C${_cn ? '_' + _cn : ''}`;
    dl(cv.toDataURL('image/png'), base + '.png');
    // CSV (전 스텝 원자료 — 분해 컬럼은 신형 viz만 채워짐)
    const hdr = 'step,t_s,V,V_terminal,x_mean,soc_window_pct,delivered_mAh_cm2,eta_kin_mV,eta_diff_mV,eta_ohm_mV,I_A,Q_ohm_e_W,Q_ohm_i_W,Q_ct_W,Q_rint_W';
    const rows = cu.V.map((v, i) => [i + 1, cu.t_s[i], v, cu.V_terminal[i], cu.x_mean[i],
      (100 * qOf(cu.x_mean[i]) / win).toFixed(3), useCap ? xs[i].toFixed(4) : '',
      cu.eta_kin_mV[i], hasD ? cu.eta_diff_mV[i] : '', hasD ? eo[i].toFixed(2) : '',
      hasD ? cu.I_A[i] : '', cu.Q_ohm_e_W[i], cu.Q_ohm_i_W[i], cu.Q_ct_W[i],
      (cu.Q_rint_W || [])[i] != null ? cu.Q_rint_W[i] : ''].join(','));
    dl(URL.createObjectURL(new Blob([hdr + '\n' + rows.join('\n')], { type: 'text/csv' })), base + '.csv');
  };
}

function renderSt4Soc(state) {
  const st = state.st4;
  const parts = [];
  ['AM_P', 'AM_S'].forEach(t => {
    const m = state.meshes[t];
    if (m) { m.visible = false; parts.push(...m.userData.particles); }
  });
  if (!parts.length) { setLegend(state, '<i>AM 입자가 없어요.</i>'); return; }
  const geo = new THREE.SphereGeometry(1, 24, 24);
  const mat = new THREE.MeshPhongMaterial({ color: 0xffffff });
  const mesh = new THREE.InstancedMesh(geo, mat, parts.length);
  state.st4Group = mesh;
  state.scene.add(mesh);
  const nChk = st.t_s.length, nr = st.nr;
  const lo = Math.min(st.x0, st.x100), hi = Math.max(st.x0, st.x100);
  const stops = [0, 0.25, 0.5, 0.75, 1].map(v => '#' + jetColor(v).toString(16).padStart(6, '0'));
  setLegend(state,
    `<b>🔋 STEP4-v2 — 입자 SOC 코어-셸</b>${st.test_only ? ' <span style="color:#f59e0b">⚠TEST-ONLY OCP</span>' : ''}
     <button id="st4-soc-curve" title="방전곡선 V vs 용량 PNG+CSV 저장" style="float:right;margin-left:5px;background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:1px 7px;cursor:pointer;font-size:11px">📈 곡선</button><button id="st4-soc-swap" title="다른 step4_viz.json으로 교체 (구버전 자동로드 덮어쓰기)" style="float:right;background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:1px 7px;cursor:pointer;font-size:11px">📂 교체</button>
     <div style="margin-top:3px">시점: <span id="st4-tlab" style="color:#e4e6f0"></span></div>
     <input type="range" id="st4-t" min="0" max="${nChk - 1}" value="${nChk - 1}" style="width:100%">
     <div style="display:flex;gap:6px;align-items:center;margin:3px 0;flex-wrap:wrap">
       <button id="st4-play" title="재생/정지" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer;font-size:13px">▶</button>
       <select id="st4-fps" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;font-size:11.5px;padding:1px 3px">
         <option value="2" selected>2 fps</option><option value="4">4 fps</option><option value="8">8 fps</option></select>
       <button id="st4-frames" title="체크포인트별 PNG 일괄 저장 — SI 무비(GIF/MP4) 조립용 프레임 시퀀스" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer;font-size:13px">🎞</button>
       <button id="st4-gif" title="전체 시간전개를 GIF 한 장으로 다운로드 (3D SOC geometry)" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer;font-size:13px">🎬</button>
       <select id="st4-gifsub" title="GIF 부드러움 — 체크포인트 사이 보간 프레임 배수 (높을수록 부드럽지만 용량↑)" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;font-size:11.5px;padding:1px 3px"><option value="1">×1</option><option value="3" selected>×3</option><option value="6">×6</option></select>
       <input id="st4-giflabel" placeholder="라벨" title="다운로드 파일명에 붙일 라벨(선택) — 예: SBE, DBE.  같은 payload에서 여러 GIF 구분용" style="width:56px;background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:5px;font-size:11px;padding:1px 5px">
     </div>
     <div>깊이(peel) r/R = <span id="st4-dlab" style="color:#e4e6f0">100</span>% — 줄이면 껍질을 벗겨 내부 셸</div>
     <input type="range" id="st4-d" min="5" max="100" value="100" style="width:100%">
     <label style="display:block;margin-top:4px;font-size:11px;color:#e5e7eb;cursor:pointer" title="색을 현재 프레임의 p5–p95로 정규화 — 입자간·코어-셸 미세 편차 증폭 (절대 비교는 끄기; 저율/초반엔 편차가 창의 몇 %라 절대 스케일에선 균일해 보이는 게 정상 물리)">
       <input type="checkbox" id="st4-dyn"> 동적 스케일 (프레임 p5–p95 — 편차 증폭)</label>
     <div style="margin:5px 0 2px 0;height:10px;border-radius:3px;background:linear-gradient(90deg,${stops.join(',')})"></div>
     <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span id="st4-clo"></span><span id="st4-chi"></span></div>
     <div style="margin-top:3px;color:#9ca3af;font-size:10.5px">구형 1D 확산(입자당 ${nr}셸) — 각도방향 균일(동심 코어-셸).
     겉이 먼저 차는 shrinking-core가 시간축으로 보임.  "단면 뷰" 체크와 조합 → 내부 링 단면.
     ${st.c_rate}C · ${st.charge ? '충전' : '방전'} · I_1C=${Number(st.i_1c_a).toExponential(2)} A</div>`);
  const tS = document.getElementById('st4-t'), dS = document.getElementById('st4-d');
  const dynCb = document.getElementById('st4-dyn');
  const _xlab = v => `x=${v.toFixed(3)}${st.c_max_mol_m3 ? ' (' + (v * st.c_max_mol_m3 / 1000).toFixed(1) + ' mmol/cm³)' : ''}`;
  // tf: 실수 프레임 (재생 시 체크포인트 사이 선형 보간 — 셸 SOC는 매끄러운 상태변수라 정직)
  const upd = (tf) => {
    const tfv = (typeof tf === 'number') ? Math.max(0, Math.min(nChk - 1, tf)) : +tS.value;
    const t0 = Math.floor(tfv), t1 = Math.min(nChk - 1, t0 + 1), fr = tfv - t0;
    const dp = +dS.value / 100;
    document.getElementById('st4-tlab').textContent =
      `t=${((1 - fr) * st.t_s[t0] + fr * st.t_s[t1]).toFixed(1)}s · x̄=${((1 - fr) * st.x_mean[t0] + fr * st.x_mean[t1]).toFixed(4)}`;
    document.getElementById('st4-dlab').textContent = Math.round(dp * 100);
    const sh0 = st.x_shell[t0], sh1 = st.x_shell[t1];
    const kSh = Math.max(0, Math.min(nr - 1, Math.ceil(dp * nr) - 1));
    // 색 스케일: 절대(전체 창 — 물리 비교) vs 동적(현재 프레임 p5–p95 — 편차 증폭)
    let cLo = lo, cHi = hi;
    if (dynCb && dynCb.checked) {
      const vals = [];
      parts.forEach(p => {
        const r0 = sh0[p.id], r1 = sh1[p.id];
        if (r0 && r1) vals.push((1 - fr) * r0[kSh] + fr * r1[kSh]);
      });
      if (vals.length > 4) {
        vals.sort((x, y) => x - y);
        cLo = vals[Math.floor(0.05 * (vals.length - 1))];
        cHi = vals[Math.floor(0.95 * (vals.length - 1))];
        if (cHi - cLo < 1e-6) { cLo -= 5e-7; cHi += 5e-7; }  // 완전 균일 프레임 가드
      }
    }
    const eLo = document.getElementById('st4-clo'), eHi = document.getElementById('st4-chi');
    if (eLo) eLo.textContent = _xlab(cLo) + ((dynCb && dynCb.checked) ? ' (p5)' : ' 탈리튬');
    if (eHi) eHi.textContent = _xlab(cHi) + ((dynCb && dynCb.checked) ? ' (p95)' : ' 리튬↑');
    const dummy = new THREE.Object3D();
    const col = new THREE.Color();
    parts.forEach((p, i) => {
      dummy.position.set(p.x, p.z, p.y);
      dummy.scale.setScalar(p.r * dp);
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
      const r0 = sh0[p.id], r1 = sh1[p.id];
      const xs = (r0 && r1) ? (1 - fr) * r0[kSh] + fr * r1[kSh] : cLo;
      const tt = Math.max(0, Math.min(1, (xs - cLo) / Math.max(cHi - cLo, 1e-9)));
      mesh.setColorAt(i, col.setHex(jetColor(tt)));
    });
    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  };
  tS.oninput = upd;
  dS.oninput = upd;
  if (dynCb) dynCb.onchange = upd;
  wireSt4Picker(state, 'st4-soc-swap', 'st4_soc');           // 📂 교체 버튼 배선
  wireVProfileDownload(state, 'st4-soc-curve');
  upd();
  // ── ▶ SOC 애니메이션 (자동 재생) + 🎞 프레임 PNG (SI 무비 조립용) ──
  if (state._st4Timer) { clearInterval(state._st4Timer); state._st4Timer = null; }
  const playBtn = document.getElementById('st4-play'), fpsSel = document.getElementById('st4-fps');
  if (playBtn) playBtn.onclick = () => {
    if (state._st4Timer) {
      clearInterval(state._st4Timer); state._st4Timer = null; playBtn.textContent = '▶'; return;
    }
    playBtn.textContent = '⏸';
    state._st4Phase = +tS.value;                             // 부드러운 재생: 30ms마다 실수 프레임
    state._st4Timer = setInterval(() => {                    // 전진 + 체크포인트 사이 선형 보간
      if (!document.body.contains(tS)) {                     // 모드 이탈 시 자기 정리
        clearInterval(state._st4Timer); state._st4Timer = null; return;
      }
      const fps = +(fpsSel && fpsSel.value) || 4;            // fps = "체크포인트/초" 통과 속도
      state._st4Phase = (state._st4Phase + fps * 0.03) % (nChk - 1e-6);
      tS.value = Math.round(state._st4Phase);
      upd(state._st4Phase);
    }, 30);
  };
  if (playBtn && nChk > 1) playBtn.onclick();                // 기본 자동재생 (2fps)
  const frBtn = document.getElementById('st4-frames');
  if (frBtn) frBtn.onclick = async () => {
    frBtn.disabled = true; frBtn.textContent = '⏳';
    const keep = +tS.value;
    for (let ti = 0; ti < nChk; ti++) {
      tS.value = ti; upd();
      const aEl = document.createElement('a');
      aEl.href = _captureHiRes(state, 3);                     // 3× 고해상 캡처 (SI/논문용)
      aEl.download = `st4_soc_f${String(ti).padStart(2, '0')}_t${st.t_s[ti]}s.png`;
      document.body.appendChild(aEl); aEl.click(); aEl.remove();
      await new Promise(res => setTimeout(res, 300));        // 브라우저 다운로드 큐 여유
    }
    tS.value = keep; upd();
    frBtn.disabled = false; frBtn.textContent = '🎞';
  };
  const gifBtn = document.getElementById('st4-gif');         // 🎬 전체 시간전개 → GIF (3D SOC, 보간 프레임)
  if (gifBtn) gifBtn.onclick = async () => {
    const keep = +tS.value, sub = +(document.getElementById('st4-gifsub') || {}).value || 3;
    const frames = _st4GifFrames(nChk, sub, ph => upd(ph), () => _captureHiRes(state, 2));
    tS.value = keep; upd();
    const _cn = String(state._st4SrcName || (state.data && state.data.case) || '').replace(/[^A-Za-z0-9._-]/g, '').slice(0, 48);
    await st4FramesToGif(frames, (+(fpsSel && fpsSel.value) || 2) * sub,
      `st4_soc3d_${st.charge ? 'chg' : 'dis'}_${st.c_rate}C${_cn ? '_' + _cn : ''}${_st4Label('st4-giflabel')}`, gifBtn);
  };
}

function renderSt4Faces(state) {
  const st = state.st4, F = st.faces;
  const n = F.pos_um.length;
  if (!n) { setLegend(state, '<i>면 데이터가 없어요.</i>'); return; }
  if (state.meshes.MESH) {                                   // SE는 얇은 맥락으로
    state.meshes.MESH.visible = true;
    state.meshes.MESH.material.transparent = true;
    state.meshes.MESH.material.opacity = 0.08;
  }
  const parts = [];
  ['AM_P', 'AM_S'].forEach(t => {
    const m = state.meshes[t];
    if (m) { m.visible = false; parts.push(...m.userData.particles); }
  });
  const grp = new THREE.Group();
  state.st4FaceGroup = grp;
  state.scene.add(grp);
  const nChk = st.t_s.length;
  const col = new THREE.Color();

  // ── COMSOL식 표면 필드 (기본 렌더): 면전류를 입자 표면에 각도-커널 보간 ──
  // 시각화 보조 보간 (정량 원자료 = 면 값): 각 표면 정점 색 = 그 입자 BV면들의 |i/ī|를
  // 방향 코사인^24 가중 평균 (σ≈15° 각도 커널).  面이 없는 방향(비접촉 표면)은 어두운 회색.
  let surfMesh = null, vFace = null, vW = null, vDeg = null, vColAttr = null, nVertTot = 0;
  const buildSurface = () => {
    if (surfMesh) return;
    const tmpl = new THREE.SphereGeometry(1, 26, 19);
    const tPos = tmpl.getAttribute('position').array, tIdx = tmpl.index.array;
    const nV = tPos.length / 3;
    nVertTot = nV * parts.length;
    const K = 6;
    // 면→입자 배정 (payload 좌표계, 해시그리드) — viz faces에 pid가 없어도 기하로 복원
    const CELL = 8.0, hash = new Map();
    const keyOf = (x, y, z) => (Math.floor(x / CELL)) + ',' + (Math.floor(y / CELL)) + ',' + (Math.floor(z / CELL));
    parts.forEach((p, pi) => {
      const k = keyOf(p.x, p.y, p.z);
      let a = hash.get(k); if (!a) { a = []; hash.set(k, a); } a.push(pi);
    });
    const pFaces = parts.map(() => []);                      // 입자별 [면 idx, 단위방향 ux,uy,uz]
    for (let i = 0; i < n; i++) {
      const f = F.pos_um[i];
      let best = -1, bestScore = 1e9;
      const cx = Math.floor(f[0] / CELL), cy = Math.floor(f[1] / CELL), cz = Math.floor(f[2] / CELL);
      for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) for (let dz = -1; dz <= 1; dz++) {
        const a = hash.get((cx + dx) + ',' + (cy + dy) + ',' + (cz + dz));
        if (!a) continue;
        for (const pi of a) {
          const p = parts[pi];
          const d = Math.hypot(f[0] - p.x, f[1] - p.y, f[2] - p.z);
          const sc = Math.abs(d - p.r);
          if (d < p.r + 1.2 && sc < bestScore) { bestScore = sc; best = pi; }
        }
      }
      if (best >= 0) {
        const p = parts[best];
        const dx = f[0] - p.x, dy = f[1] - p.y, dz = f[2] - p.z;
        const L = Math.max(Math.hypot(dx, dy, dz), 1e-9);
        pFaces[best].push([i, dx / L, dy / L, dz / L]);
      }
    }
    // 정점 버퍼 + per-정점 k-최근접(각도) 면 테이블
    const pos = new Float32Array(nVertTot * 3);
    const idx = new Uint32Array(tIdx.length * parts.length);
    vFace = new Int32Array(nVertTot * K).fill(-1);
    vW = new Float32Array(nVertTot * K);
    vDeg = new Uint8Array(nVertTot);
    parts.forEach((p, pi) => {
      const fl = pFaces[pi], base = pi * nV;
      for (let v = 0; v < nV; v++) {
        const ux = tPos[3 * v], uy = tPos[3 * v + 1], uz = tPos[3 * v + 2];
        // payload 프레임 정점 (구는 등방이라 템플릿 방향 = payload 방향으로 써도 무방)
        pos[3 * (base + v)] = p.x + p.r * ux;
        pos[3 * (base + v) + 1] = p.z + p.r * uz;             // scene Y = payload z
        pos[3 * (base + v) + 2] = p.y + p.r * uy;
        if (!fl.length) continue;
        // top-K by dot (삽입 정렬, K 작음)
        const bi = new Array(K).fill(-1), bw = new Array(K).fill(-1);
        for (let q = 0; q < fl.length; q++) {
          const d = ux * fl[q][1] + uy * fl[q][2] + uz * fl[q][3];  // payload 방향 직접 정렬 (템플릿 ux,uy,uz ↔ 면 dx,dy,dz)
          if (d <= bw[K - 1]) continue;
          let j = K - 1;
          while (j > 0 && bw[j - 1] < d) { bw[j] = bw[j - 1]; bi[j] = bi[j - 1]; j--; }
          bw[j] = d; bi[j] = fl[q][0];
        }
        let deg = 0;
        for (let k2 = 0; k2 < K; k2++) {
          if (bi[k2] < 0 || bw[k2] <= 0) break;
          vFace[(base + v) * K + k2] = bi[k2];
          vW[(base + v) * K + k2] = Math.pow(bw[k2], 24);     // ~15° 각도 커널
          deg++;
        }
        vDeg[base + v] = deg;
      }
      for (let t2 = 0; t2 < tIdx.length; t2++) idx[pi * tIdx.length + t2] = base + tIdx[t2];
    });
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.setIndex(new THREE.BufferAttribute(idx, 1));
    g.computeVertexNormals();
    vColAttr = new THREE.BufferAttribute(new Float32Array(nVertTot * 3), 3);
    g.setAttribute('color', vColAttr);
    surfMesh = new THREE.Mesh(g, new THREE.MeshPhongMaterial({
      vertexColors: true, shininess: 22, specular: 0x222222 }));
    grp.add(surfMesh);
  };

  const stops = [0, 0.25, 0.5, 0.75, 1].map(v => '#' + jetColor(v).toString(16).padStart(6, '0'));
  setLegend(state,
    `<b>🔋 STEP4-v2 — 표면 반응전류 (COMSOL식 표면 필드)</b>${st.test_only ? ' <span style="color:#f59e0b">⚠TEST-ONLY OCP</span>' : ''}
     <button id="st4f-curve" title="방전곡선 V vs 용량 PNG+CSV 저장" style="float:right;margin-left:5px;background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:1px 7px;cursor:pointer;font-size:11px">📈 곡선</button><button id="st4f-swap" title="다른 step4_viz.json으로 교체 (구버전 자동로드 덮어쓰기)" style="float:right;background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:1px 7px;cursor:pointer;font-size:11px">📂 교체</button>
     <div style="margin-top:3px">시점: <span id="st4f-tlab" style="color:#e4e6f0"></span></div>
     <input type="range" id="st4f-t" min="0" max="${nChk - 1}" value="${nChk - 1}" style="width:100%">
     <div style="display:flex;gap:6px;align-items:center;margin:3px 0;flex-wrap:wrap">
       <button id="st4f-play" title="재생/정지" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer;font-size:13px">▶</button>
       <select id="st4f-fps" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;font-size:11.5px;padding:1px 3px">
         <option value="2" selected>2 fps</option><option value="4">4 fps</option><option value="8">8 fps</option></select>
       <button id="st4f-frames" title="체크포인트별 PNG 일괄 저장 — SI 무비 조립용" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer;font-size:13px">🎞</button>
       <button id="st4f-gif" title="전체 시간전개를 GIF 한 장으로 (3D 반응전류 표면 애니메이션)" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer;font-size:13px">🎬</button>
       <select id="st4f-gifsub" title="GIF 부드러움 — 체크포인트 사이 보간 프레임 배수 (3D·프로파일 GIF 공통; 높을수록 부드럽지만 용량↑)" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;font-size:11.5px;padding:1px 3px"><option value="1">×1</option><option value="3" selected>×3</option><option value="6">×6</option></select>
       <input id="st4f-giflabel" placeholder="라벨" title="다운로드 파일명에 붙일 라벨(선택) — 예: SBE, DBE.  3D·프로파일 GIF 공통, 같은 payload 구분용" style="width:56px;background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:5px;font-size:11px;padding:1px 5px">
     </div>
     <div style="margin:5px 0 2px 0;height:10px;border-radius:3px;background:linear-gradient(90deg,${stops.join(',')})"></div>
     <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span>0</span><span>|i/ī| (0–p95)</span><span>핫스팟</span></div>
     <div style="margin-top:3px;color:#9ca3af;font-size:10.5px">면전류를 입자 표면에 각도-커널(≈15°) 보간한 <b>시각화 보조</b> — 정량 원자료는 면 값(npz).
     비접촉 표면 = 회색.  면 ${Number(F.n_kept).toLocaleString()}/${Number(F.n_total).toLocaleString()}${F.n_kept < F.n_total ? ' (서브샘플)' : ''} ·
     ī(면평균 |i|) 시점별 정규화 · ${st.charge ? '충전' : '방전'} ${st.c_rate}C</div>
     <div style="margin-top:6px;padding:6px 7px;background:#0d1117;border:1px solid #2a2d3e;border-radius:6px">
       <div style="display:flex;justify-content:space-between;align-items:center">
         <b style="font-size:11.5px;color:#cbd5e1">두께방향 프로파일 — 현재 시점</b>
         <select id="st4f-prof-src" title="프로파일 소스 — 반응·SOC(기존) / 운전 φ(z)(전자·이온 층평균 전위, 새 viz만): φ_e는 µV급 평평·φ_i는 수십 mV = 상보 구도 직접 시각화" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;font-size:10.5px;padding:0 2px">
           <option value="rxn">반응·SOC</option>${st.phi_z && st.phi_z.phi_i_V ? '<option value="phi">운전 φ(z)</option>' : ''}</select>
         <button id="st4f-prof-dl" title="이 시점의 프로파일을 PNG(3×)+CSV로 저장 (동적 Fig4e)" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:1px 7px;cursor:pointer;font-size:12px">📈</button>
         <button id="st4f-zgif" title="두께방향 프로파일 전체 시간전개를 GIF로 (동적 Fig4e 무비)" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:1px 7px;cursor:pointer;font-size:12px">🎬</button>
       </div>
       <canvas id="st4f-prof" width="220" height="120" style="width:100%;margin-top:4px;border-radius:4px"></canvas>
       <div id="st4f-prof-cap" style="font-size:10px;color:#6b7280;margin-top:2px"><span style="color:#f87171">—</span> 반응분포 ⟨|i/ī|⟩(z) · <span style="color:#60a5fa">—</span> 표면 SOC(z) — 재생하면 전선의 행진이 곡선으로 움직임</div>
     </div>`);
  const tS = document.getElementById('st4f-t');
  const frHi = [];                                           // 프레임별 p95 캐시 (정규화 기준)
  const _hiOf = (k) => {
    if (frHi[k] == null) {
      const abs = F.i_rel[k].map(Math.abs).sort((a, b) => a - b);
      frHi[k] = Math.max(abs[Math.floor(0.95 * (abs.length - 1))], 1e-9);
    }
    return frHi[k];
  };
  const arrBuf = new Float32Array(n);                        // 보간 프레임 버퍼
  // ── 두께방향 프로파일 (동적 Fig4e): z-빈별 ⟨|i/ī|⟩(반응분포) + 표면 SOC — 시점 따라 갱신 ──
  const NB = 24;
  const faceZ = new Float64Array(n);
  let zMaxF = 1e-9;
  for (let i = 0; i < n; i++) { faceZ[i] = F.pos_um[i][2]; if (faceZ[i] > zMaxF) zMaxF = faceZ[i]; }
  const partBin = parts.map(p => Math.max(0, Math.min(NB - 1, Math.floor(p.z / zMaxF * NB))));
  const _pb = { i: new Float64Array(NB), c: new Int32Array(NB), s: new Float64Array(NB), sc: new Int32Array(NB) };
  let _profRows = [];                                        // 📈 CSV용 (마지막 그린 프레임)
  const drawProf = (fr, t0, t1, tSec) => {
    const cv = document.getElementById('st4f-prof');
    if (!cv) return;
    // ── 운전 φ(z) 모드 (새 viz의 phi_z 블록): φ_e/φ_i 층평균을 각자 [0,1] 정규화해 겹침 —
    //    곡률 미러가 보이고, 실제 스케일(µV vs mV)은 캡션 숫자로.  체크포인트 최근접 사용.
    const _src = (document.getElementById('st4f-prof-src') || {}).value || 'rxn';
    if (_src === 'phi' && st.phi_z && st.phi_z.phi_i_V) {
      const kph = (fr < 0.5 ? t0 : t1);
      const zs = st.phi_z.z_um, pe = st.phi_z.phi_e_V[kph] || [], pi = st.phi_z.phi_i_V[kph] || [];
      const zE = [], yE = [], zI = [], yI = [];
      let eMin = Infinity, eMax = -Infinity, iMin2 = Infinity, iMax2 = -Infinity;
      for (let b = 0; b < zs.length; b++) {
        if (pe[b] != null) { if (pe[b] < eMin) eMin = pe[b]; if (pe[b] > eMax) eMax = pe[b]; }
        if (pi[b] != null) { if (pi[b] < iMin2) iMin2 = pi[b]; if (pi[b] > iMax2) iMax2 = pi[b]; }
      }
      const eSw = Math.max(eMax - eMin, 1e-12), iSw = Math.max(iMax2 - iMin2, 1e-12);
      for (let b = 0; b < zs.length; b++) {
        if (pe[b] != null) { zE.push(zs[b]); yE.push((pe[b] - eMin) / eSw); }
        if (pi[b] != null) { zI.push(zs[b]); yI.push((pi[b] - iMin2) / iSw); }
      }
      const curves = [{ zs: zE, ys: yE, color: '#f87171', dash: false },
                      { zs: zI, ys: yI, color: '#a78bfa', dash: false }];
      drawZProfileCanvas(cv, curves, '');
      const cap = document.getElementById('st4f-prof-cap');
      if (cap) cap.innerHTML = `<span style="color:#f87171">—</span> φ_e 스윙 ${(eSw * 1e6).toPrecision(3)} µV · `
        + `<span style="color:#a78bfa">—</span> φ_i 스윙 ${(iSw * 1e3).toPrecision(3)} mV `
        + `(<b>${(iSw / eSw).toPrecision(2)}×</b>) — 각자 [0,1] 정규화(곡률 미러용); 절대 스케일은 이 숫자`;
      _profRows = [];
      for (let b = 0; b < zs.length; b++) {
        _profRows.push([zs[b], tSec.toFixed(1),
                        pe[b] != null ? pe[b] : '', pi[b] != null ? pi[b] : '']);
      }
      state._st4fProf = { curves, rows: _profRows, hdr: 'z_um,t_s,phi_e_V,phi_i_V' };
      return;
    }
    const cap0 = document.getElementById('st4f-prof-cap');
    if (cap0 && _src === 'rxn') cap0.innerHTML = '<span style="color:#f87171">—</span> 반응분포 ⟨|i/ī|⟩(z) · <span style="color:#60a5fa">—</span> 표면 SOC(z) — 재생하면 전선의 행진이 곡선으로 움직임';
    const g = cv.getContext('2d'), Wc = cv.width, Hc = cv.height;
    _pb.i.fill(0); _pb.c.fill(0); _pb.s.fill(0); _pb.sc.fill(0);
    for (let i2 = 0; i2 < n; i2++) {
      const b = Math.max(0, Math.min(NB - 1, Math.floor(faceZ[i2] / zMaxF * NB)));
      _pb.i[b] += Math.abs(arrBuf[i2]); _pb.c[b]++;
    }
    const sh0 = st.x_shell[t0], sh1 = st.x_shell[t1], kS = st.nr - 1;
    parts.forEach((p, pi) => {
      const r0 = sh0[p.id], r1 = sh1[p.id];
      if (!r0 || !r1) return;
      _pb.s[partBin[pi]] += (1 - fr) * r0[kS] + fr * r1[kS]; _pb.sc[partBin[pi]]++;
    });
    let iMax = 1e-9;
    for (let b = 0; b < NB; b++) if (_pb.c[b]) iMax = Math.max(iMax, _pb.i[b] / _pb.c[b]);
    const lo2 = Math.min(st.x0, st.x100), hi2 = Math.max(st.x0, st.x100);
    const zc = b => (b + 0.5) / NB * zMaxF;
    const rZ = [], rY = [], bZ = [], bY = [];              // 정규화 [0,1] 두 곡선 (공유 축)
    for (let b = 0; b < NB; b++) {
      if (_pb.c[b]) { rZ.push(zc(b)); rY.push((_pb.i[b] / _pb.c[b]) / iMax); }
      if (_pb.sc[b]) { bZ.push(zc(b)); bY.push(((_pb.s[b] / _pb.sc[b]) - lo2) / Math.max(hi2 - lo2, 1e-9)); }
    }
    const curves = [{ zs: rZ, ys: rY, color: '#f87171', dash: false },
                    { zs: bZ, ys: bY, color: '#60a5fa', dash: false }];
    drawZProfileCanvas(cv, curves, '');                    // 인라인 (크리스프 헬퍼)
    _profRows = [];
    for (let b = 0; b < NB; b++) {
      _profRows.push([zc(b).toFixed(2), tSec.toFixed(1),
                      _pb.c[b] ? (_pb.i[b] / _pb.c[b]).toFixed(5) : '',
                      _pb.sc[b] ? (_pb.s[b] / _pb.sc[b]).toFixed(5) : '']);
    }
    state._st4fProf = { curves, rows: _profRows, hdr: 'z_um,t_s,i_over_ibar_mean,soc_surf_mean' };  // 고해상 export용
  };
  const upd = (tf) => {
    const tfv = (typeof tf === 'number') ? Math.max(0, Math.min(nChk - 1, tf)) : +tS.value;
    const t0 = Math.floor(tfv), t1 = Math.min(nChk - 1, t0 + 1), fr = tfv - t0;
    document.getElementById('st4f-tlab').textContent =
      `t=${((1 - fr) * st.t_s[t0] + fr * st.t_s[t1]).toFixed(1)}s · x̄=${((1 - fr) * st.x_mean[t0] + fr * st.x_mean[t1]).toFixed(4)}`;
    const a0 = F.i_rel[t0], a1 = F.i_rel[t1];
    for (let i = 0; i < n; i++) arrBuf[i] = (1 - fr) * a0[i] + fr * a1[i];
    const arr = arrBuf;
    const hi = (1 - fr) * _hiOf(t0) + fr * _hiOf(t1);
    buildSurface();
    surfMesh.visible = true;
    ['AM_P', 'AM_S'].forEach(t => { if (state.meshes[t]) state.meshes[t].visible = false; });
    const cArr = vColAttr.array, K = 6;
    for (let v = 0; v < nVertTot; v++) {
      const deg = vDeg[v];
      if (!deg) { cArr[3 * v] = 0.16; cArr[3 * v + 1] = 0.17; cArr[3 * v + 2] = 0.19; continue; }
      let sw = 0, sv = 0;
      for (let k2 = 0; k2 < deg; k2++) {
        const fi = vFace[v * K + k2];
        sw += vW[v * K + k2];
        sv += vW[v * K + k2] * Math.abs(arr[fi]);
      }
      const t2 = Math.max(0, Math.min(1, (sv / Math.max(sw, 1e-30)) / hi));
      col.setHex(jetColor(t2));
      cArr[3 * v] = col.r; cArr[3 * v + 1] = col.g; cArr[3 * v + 2] = col.b;
    }
    vColAttr.needsUpdate = true;
    drawProf(fr, t0, t1, (1 - fr) * st.t_s[t0] + fr * st.t_s[t1]);   // 동적 Fig4e 프로파일 갱신
  };
  tS.oninput = upd;
  { const _ps = document.getElementById('st4f-prof-src');    // 프로파일 소스 전환 → 현재 시점 리드로
    if (_ps) _ps.onchange = () => upd(+tS.value); }
  wireSt4Picker(state, 'st4f-swap', 'st4_face');             // 📂 교체 버튼 배선
  wireVProfileDownload(state, 'st4f-curve');
  upd();
  // ▶ 재생 + 🎞 프레임 (SOC 모드와 동일 문법)
  if (state._st4fTimer) { clearInterval(state._st4fTimer); state._st4fTimer = null; }
  const playBtn = document.getElementById('st4f-play'), fpsSel = document.getElementById('st4f-fps');
  if (playBtn) playBtn.onclick = () => {
    if (state._st4fTimer) { clearInterval(state._st4fTimer); state._st4fTimer = null; playBtn.textContent = '▶'; return; }
    playBtn.textContent = '⏸';
    state._st4fPhase = +tS.value;                            // 부드러운 재생 (체크포인트 사이 보간)
    state._st4fTimer = setInterval(() => {
      if (!document.body.contains(tS)) { clearInterval(state._st4fTimer); state._st4fTimer = null; return; }
      const fps = +(fpsSel && fpsSel.value) || 4;
      state._st4fPhase = (state._st4fPhase + fps * 0.03) % (nChk - 1e-6);
      tS.value = Math.round(state._st4fPhase);
      upd(state._st4fPhase);
    }, 30);
  };
  if (playBtn && nChk > 1) playBtn.onclick();                // 기본 자동재생 (2fps)
  const frBtn = document.getElementById('st4f-frames');
  if (frBtn) frBtn.onclick = async () => {
    frBtn.disabled = true; frBtn.textContent = '⏳';
    const keep = +tS.value;
    for (let ti = 0; ti < nChk; ti++) {
      tS.value = ti; upd();
      const aEl = document.createElement('a');
      aEl.href = _captureHiRes(state, 3);                     // 3× 고해상 캡처
      aEl.download = `st4_faces_f${String(ti).padStart(2, '0')}_t${st.t_s[ti]}s.png`;
      document.body.appendChild(aEl); aEl.click(); aEl.remove();
      await new Promise(res => setTimeout(res, 300));
    }
    tS.value = keep; upd();
    frBtn.disabled = false; frBtn.textContent = '🎞';
  };
  const _st4cn = () => String(state._st4SrcName || (state.data && state.data.case) || '').replace(/[^A-Za-z0-9._-]/g, '').slice(0, 48);
  const _st4tag = () => `${st.charge ? 'chg' : 'dis'}_${st.c_rate}C${_st4cn() ? '_' + _st4cn() : ''}`;
  const _gifSub = () => +(document.getElementById('st4f-gifsub') || {}).value || 3;
  const fGifBtn = document.getElementById('st4f-gif');       // 🎬 전체 시간전개 → GIF (3D 반응전류 표면, 보간 프레임)
  if (fGifBtn) fGifBtn.onclick = async () => {
    const keep = +tS.value, sub = _gifSub();
    const frames = _st4GifFrames(nChk, sub, ph => upd(ph), () => _captureHiRes(state, 2));
    tS.value = keep; upd();
    await st4FramesToGif(frames, (+(fpsSel && fpsSel.value) || 2) * sub, `st4_rxn3d_${_st4tag()}${_st4Label('st4f-giflabel')}`, fGifBtn);
  };
  // 📈 현재 시점 프로파일 PNG(3×)+CSV — 동적 Fig4e (반응분포·표면 SOC vs 두께)
  const pfBtn = document.getElementById('st4f-prof-dl');
  if (pfBtn) pfBtn.onclick = () => {
    if (!_profRows.length || !state._st4fProf) return;
    const big = document.createElement('canvas');
    big.width = 1200; big.height = 660;
    drawZProfileCanvas(big, state._st4fProf.curves, '');   // 고해상 재그리기 (확대-뭉갬 방지)
    const t_now = _profRows[0][1];
    const a1 = document.createElement('a');
    a1.href = big.toDataURL('image/png');
    a1.download = `st4_zprofile_t${t_now}s.png`;
    document.body.appendChild(a1); a1.click(); a1.remove();
    const csv = (state._st4fProf.hdr || 'z_um,t_s,i_over_ibar_mean,soc_surf_mean') + '\n'
      + _profRows.map(r => r.join(',')).join('\n');
    const a2 = document.createElement('a');
    a2.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
    a2.download = `st4_zprofile_t${t_now}s.csv`;
    document.body.appendChild(a2); a2.click(); a2.remove();
    setTimeout(() => URL.revokeObjectURL(a2.href), 5000);
  };
  const zGifBtn = document.getElementById('st4f-zgif');      // 🎬 두께 프로파일 전체 시간전개 → GIF (동적 Fig4e, 보간 프레임)
  if (zGifBtn) zGifBtn.onclick = async () => {
    const keep = +tS.value, sub = _gifSub();
    const frames = _st4GifFrames(nChk, sub, ph => upd(ph), () => {   // upd → drawProf가 state._st4fProf 갱신
      if (!state._st4fProf) return null;
      const big = document.createElement('canvas'); big.width = 1000; big.height = 560;
      drawZProfileCanvas(big, state._st4fProf.curves, '');
      return big.toDataURL('image/png');
    });
    tS.value = keep; upd();
    await st4FramesToGif(frames, (+(fpsSel && fpsSel.value) || 2) * sub, `st4_zprof_${_st4tag()}${_st4Label('st4f-giflabel')}`, zGifBtn);
  };
}

/* ── control-panel HTML ────────────────────────────────────── */
function buildControls(container, isMPM) {
  const div = document.createElement('div');
  div.className = 'viewer-controls';
  // MPM viewer: minimal panel — AM_P/AM_S + SE (the compacted-SE mesh, data-layer
  // MESH).  No DEM-only controls (View Mode, Percolating Path, Force Chain, Path
  // Only View): the MPM payload has no fracture / percolation / force-chain data.
  div.innerHTML = isMPM ? `
    <label><input type="checkbox" data-layer="AM_P" checked> AM_P</label>
    <label><input type="checkbox" data-layer="AM_S" checked> AM_S</label>
    <label><input type="checkbox" data-layer="MESH" checked> SE</label>
    <hr>
    <label style="font-size:12px;font-weight:600;margin-bottom:1px">View Mode</label>
    <select id="view-mode" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:2px 4px;font-size:12px">
      <option value="default">Default (AM 종류)</option>
      <option value="coverage">Coverage Heat (AM)</option>
      <option value="coverage_patches">Coverage 패치 (표면 partial)</option>
      <option value="se_strain">SE 변형 (vs seed)</option>
      <optgroup label="전기 (electrical)">
        <option value="econn">전기 연결성 — 연결/고립 (econn)</option>
        <option value="je_field">⚡ 전자 전류밀도 — 필드 (AM+카본, 논문)</option>
        <option value="ji_field">⚡ 이온 전류밀도 — 필드 (SE+SDCP, 논문)</option>
        <option value="je">└ 전자 — AM 입자별 (je)</option>
        <option value="je_delta">└ Δ 재분배 — bare/wetted 비율 (접점 상실)</option>
        <option value="jrxn">🔋 반응 전류밀도 — 충전 저율 (STEP4)</option>
        <option value="st4_soc">🔋 STEP4-v2 — 입자 SOC 코어-셸 (동역학·시간)</option>
        <option value="st4_face">🔋 STEP4-v2 — 표면 반응전류 면분포 (동역학·시간)</option>
      </optgroup>
      <optgroup label="도전재 (carbon)">
        <option value="additives">도전재 — 전체</option>
        <option value="add_vgcf">　└ VGCF만</option>
        <option value="add_superp">　└ Super P만</option>
        <option value="add_ptfe">　└ PTFE만</option>
        <option value="add_sdcp">　└ SDCP만</option>
        <option value="cbd">CBD 도메인 (carbon+binder 통합상)</option>
      </optgroup>
      <optgroup label="기공 (pore / XCT)">
        <option value="pore">기공만 (pore — XCT처럼)</option>
      </optgroup>
    </select>
    <div id="view-mode-legend" style="font-size:11px;color:#9ca3af;line-height:1.4;margin-top:3px;max-height:340px;overflow-y:auto;overflow-x:hidden;padding-right:2px"></div>
    <input type="file" id="st4-file" accept=".json,application/json" style="display:none">
    <hr>
    <label style="font-size:12px"><input type="checkbox" id="clip-on"> 단면 뷰 (Y-슬라이스)</label>
    <input type="range" id="clip-pos" min="2" max="98" value="50" style="width:100%;margin-top:2px">
    <hr>
    <button data-action="analysisSummary">📊 분석 요약</button>
    <button data-action="mechReaction" title="기계(SE 소성변형·접촉) ↔ 반응(j_rxn) 공간 상관 팝업 — 관찰용(모델에 응력→반응 커플링 없음)">📊 반응↔변형</button>
    <button data-action="amCloseup">AM Close-up</button>
    <button data-action="resetView">Reset</button>
    <button data-action="screenshot">Screenshot</button>
    <button data-action="colorbar" title="현재 모드의 컬러바를 논문용 6× PNG로 다운로드 (⚖ 팝업과 동일 문법)">컬러바 ⬇</button>` : `
    <label><input type="checkbox" data-layer="AM_P" checked> AM_P</label>
    <label><input type="checkbox" data-layer="AM_S" checked> AM_S</label>
    <label><input type="checkbox" data-layer="SE" checked> SE</label>
    <label><input type="checkbox" data-layer="MESH" checked> Mesh (plate)</label>
    <hr>
    <label style="font-size:12px;font-weight:600;margin-bottom:1px">View Mode</label>
    <select id="view-mode" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:2px 4px;font-size:12px">
      <option value="default">Default</option>
      <option value="brittle">Brittle Hotspots (AM)</option>
      <option value="brittle_surface">Brittle Hotspots (surface gradient)</option>
      <option value="cluster">Cluster Coloring (SE)</option>
      <option value="stress">Stress Concentration</option>
      <option value="stress_brittle">Stress + Brittle (overlay)</option>
      <option value="coverage">Coverage Heat (AM)</option>
      <option value="se_engagement">SE engagement & pore risk</option>
      <optgroup label="Fracture (Phase A)">
        <option value="worst_fpc">Worst F/P_c per particle</option>
        <option value="am_p_skeleton">AM_P Fracture Skeleton</option>
        <option value="stress_chain">Stress Chain (AM-AM)</option>
      </optgroup>
      <optgroup label="Percolation (Phase A5/A6)">
        <option value="se_diagnostics">SE Network Diagnostics</option>
      </optgroup>
    </select>
    <div id="view-mode-legend" style="font-size:11px;color:#9ca3af;line-height:1.4;margin-top:3px;max-height:340px;overflow-y:auto;overflow-x:hidden;padding-right:2px"></div>
    <hr>
    <label style="font-size:12px"><input type="checkbox" id="clip-on"> 단면 뷰 (Y-슬라이스)</label>
    <input type="range" id="clip-pos" min="2" max="98" value="50" style="width:100%;margin-top:2px">
    <hr>
    <label><input type="checkbox" id="path-toggle"> <span style="font-size:12px">Percolating Path</span></label>
    <div id="path-controls" style="display:none">
      <div style="display:flex;gap:4px;align-items:center;margin-top:3px">
        <button id="path-prev" style="background:#555;color:#fff;border:none;border-radius:3px;padding:1px 6px;cursor:pointer;font-size:13px">&lt;</button>
        <span id="path-current" style="font-size:12px;color:#e4e6f0;min-width:30px;text-align:center">-</span>
        <button id="path-next" style="background:#555;color:#fff;border:none;border-radius:3px;padding:1px 6px;cursor:pointer;font-size:13px">&gt;</button>
        <span id="path-total" style="font-size:11px;color:#7c8194">/ -</span>
      </div>
      <div id="cluster-info" style="font-size:11px;color:#e4e6f0;margin-top:3px;line-height:1.5"></div>
    </div>
    <hr>
    <label><input type="checkbox" id="force-chain-toggle"> <span style="font-size:12px">Force Chain</span></label>
    <hr>
    <button data-action="pathOnly">Path Only View</button>
    <button data-action="amCloseup">AM Close-up</button>
    <button data-action="resetView">Reset</button>
    <button data-action="screenshot">Screenshot</button>`;
  container.appendChild(div);
  // Zoom slider (bottom-right)
  const zoomDiv = document.createElement('div');
  zoomDiv.className = 'viewer-zoom';
  zoomDiv.innerHTML = `
    <button id="zoom-out">−</button>
    <input type="range" id="zoom-slider" min="30" max="350" value="200" step="5">
    <button id="zoom-in">+</button>`;
  container.appendChild(zoomDiv);
  div._zoomDiv = zoomDiv;
  // Separate info panel
  const infoDiv = document.createElement('div');
  infoDiv.className = 'viewer-info';
  infoDiv.id = 'viewer-info';
  container.appendChild(infoDiv);
  div._infoEl = infoDiv;
  return div;
}

/* ── inject CSS (once) ─────────────────────────────────────── */
function injectCSS() {
  if (document.getElementById('viewer3d-css')) return;
  const s = document.createElement('style');
  s.id = 'viewer3d-css';
  s.textContent = `
.viewer-container canvas{display:block}
.viewer-controls{position:absolute;top:10px;right:10px;background:rgba(22,25,46,.9);
  border:1px solid #2a2d3e;border-radius:8px;padding:8px 12px;display:inline-flex;flex-direction:column;gap:3px;
  font:12.5px/1.45 'Inter',sans-serif;color:#e4e6f0;z-index:10;user-select:none;width:230px;min-width:170px;max-width:440px;resize:horizontal;
  max-height:calc(100% - 20px);overflow-y:auto;overflow-x:hidden}
.viewer-controls label{display:flex;align-items:center;gap:5px;cursor:pointer;font-size:12px}
.viewer-controls hr{border:none;border-top:1px solid #2a2d3e;margin:3px 0}
.viewer-controls button{background:#555;color:#fff;border:none;border-radius:4px;padding:3px 8px;
  cursor:pointer;font-size:11px;margin-top:1px}
.viewer-controls button:hover{background:#777}
.viewer-controls input[type=range]{width:100%;min-width:0;box-sizing:border-box;margin:2px 0;accent-color:#6c8cff}
.viewer-info{position:absolute;bottom:50px;left:12px;background:rgba(22,25,46,.9);
  border:1px solid #2a2d3e;border-radius:8px;padding:8px 12px;
  font:11px/1.5 'JetBrains Mono',monospace;color:#e4e6f0;z-index:10;max-width:240px;display:none}
.viewer-zoom{position:absolute;bottom:12px;left:12px;background:rgba(22,25,46,.9);
  border:1px solid #2a2d3e;border-radius:8px;padding:6px 10px;z-index:10;
  display:flex;align-items:center;gap:6px}
.viewer-zoom button{background:#555;color:#fff;border:none;border-radius:4px;width:24px;height:24px;
  cursor:pointer;font-size:16px;line-height:1;display:flex;align-items:center;justify-content:center}
.viewer-zoom button:hover{background:#777}
.viewer-zoom input[type=range]{width:100px;accent-color:#6c8cff}
.path-modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:1000;display:flex;align-items:center;justify-content:center}
.path-modal{background:#fff;border-radius:12px;padding:20px;max-width:90vw;max-height:90vh;position:relative;overflow-y:auto;overscroll-behavior:contain}
.path-modal img{max-width:100%;max-height:75vh;border-radius:8px;border:1px solid #ddd}
.path-modal-info{margin-top:10px;font:12px/1.5 'JetBrains Mono',monospace;color:#333}
.path-modal-actions{display:flex;gap:8px;margin-top:12px;justify-content:flex-end}
.path-modal-actions button{background:#6c8cff;color:#fff;border:none;border-radius:6px;padding:6px 14px;cursor:pointer;font-size:13px}
.path-modal-actions button:hover{background:#8ba3ff}
.path-modal-close{position:absolute;top:8px;right:12px;background:none;border:none;font-size:20px;cursor:pointer;color:#888}
.data-modal-btn{display:flex;align-items:center;justify-content:center;gap:5px;width:100%;padding:7px 8px;margin:8px 0 2px 0;background:rgba(99,102,241,.16);color:#c7d2fe;border:1px solid rgba(99,102,241,.45);border-radius:6px;font:600 11px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;letter-spacing:.2px;cursor:pointer;white-space:nowrap;transition:background .15s,border-color .15s,color .15s,transform .05s}
.data-modal-btn:hover{background:rgba(99,102,241,.32);border-color:#a5b4fc;color:#fff}
.data-modal-btn:active{transform:translateY(1px)}
.data-modal-btn .ico{font-size:13px;line-height:1}
.data-modal-btn .sub{font-weight:500;color:#9ca3af;font-size:10.5px;margin-left:3px}`;
  document.head.appendChild(s);
}

/* ── main init function ────────────────────────────────────── */
export function initElectrodeViewer(containerId, dataUrl) {
  injectCSS();
  const container = document.getElementById(containerId);
  if (!container) { console.error('viewer3d: container not found:', containerId); return; }
  container.classList.add('viewer-container');

  /* renderer (alpha:true so screenshots can use transparent background) */
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setClearColor(COL.BG, 1);
  container.appendChild(renderer.domElement);

  /* scene, camera */
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 10000);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.12;
  controls.enableZoom = true;
  controls.zoomSpeed = 1.0;

  /* lights */
  scene.add(new THREE.AmbientLight(0xffffff, 0.4));
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(1, 1.5, 1);
  scene.add(dirLight);

  /* state */
  const state = {
    data: null, meshes: {}, percolationOn: false, pathGroup: null,
    selectedComponent: null, infoEl: null,
    renderer, camera, scene: null,                           // st4 애니메이션 프레임 export용 핸들
  };

  /* controls panel — MPM payloads get the minimal panel.  Both the per-case route
   * (/3d-mpm-data) and the standalone 도전재 viewer (/mpm-lab/data/…) serve MPM payloads. */
  const isMPM = (dataUrl || '').includes('3d-mpm-data') || (dataUrl || '').includes('/mpm-lab/');
  state.isMPM = isMPM;
  state._dataUrl = dataUrl || '';                           // for the mech↔reaction popup URL
  state.isSeed = (dataUrl || '').includes('state=seed');   // 압축 전 (loose) view
  const ctrlDiv = buildControls(container, isMPM);
  state.infoEl = ctrlDiv._infoEl || document.getElementById('viewer-info');

  /* ── data fetch & build ──────────────────────────────────── */
  state.dataUrl = dataUrl;

  /* Inline loading / error overlay so silent failures are visible.
   * Without this, fetch hangs and the user sees infinite "loading"
   * with no clue why — exactly the input_particulate_1 symptom
   * that prompted this hardening. */
  const overlay = document.createElement('div');
  overlay.style.cssText =
    'position:absolute;top:8px;left:8px;z-index:50;padding:6px 12px;'
    + 'background:rgba(0,0,0,.6);color:#e4e6f0;font-size:13px;'
    + 'border-radius:6px;font-family:ui-monospace,Menlo,monospace';
  overlay.textContent = '3D viewer 데이터 로딩 중…';
  container.appendChild(overlay);
  const fetchT0 = performance.now();
  const fetchTimer = setInterval(() => {
    const dt = ((performance.now() - fetchT0) / 1000).toFixed(0);
    overlay.textContent = `3D viewer 데이터 로딩 중… (${dt}s)`;
  }, 1000);

  fetch(dataUrl)
    .then(r => {
      if (!r.ok) throw new Error(
        `/3d-data → HTTP ${r.status} ${r.statusText}`);
      overlay.textContent = '응답 받음, JSON 파싱 중…';
      return r.json();
    })
    .then(data => {
    clearInterval(fetchTimer);
    if (data._aux_error) {
      /* Server returned base geometry but couldn't serialize aux
       * (numpy types / NaN / OOM during jsonify).  Show as a
       * non-fatal warning — viewer still renders. */
      overlay.style.background = 'rgba(180,83,9,.85)';
      overlay.style.color = '#fef3c7';
      overlay.style.fontSize = '11px';
      overlay.innerHTML =
        `⚠ aux 데이터 누락 (서버 jsonify 오류)<br>`
        + `<span style="color:#fde68a;font-size:11px">`
        + `${data._aux_error}</span>`;
      setTimeout(() => overlay.remove(), 6000);
    } else {
      overlay.remove();
    }
    state.data = data;
    buildScene(scene, camera, controls, data, state);
    wireControls(ctrlDiv, renderer, camera, controls, scene, state);

    // Setup percolating path navigation
    const clusters = (data.clusters || {}).clusters || [];
    const percClusters = clusters.filter(c => c.percolating && c.path);
    state.percClusters = percClusters;
    state.percIdx = 0;

    const totalEl = ctrlDiv.querySelector('#path-total');
    const currentEl = ctrlDiv.querySelector('#path-current');
    const infoEl = ctrlDiv.querySelector('#cluster-info');
    const prevBtn = ctrlDiv.querySelector('#path-prev');
    const nextBtn = ctrlDiv.querySelector('#path-next');

    if (totalEl) totalEl.textContent = `/ ${percClusters.length}`;

    const pathControls = ctrlDiv.querySelector('#path-controls');
    const pathToggle = ctrlDiv.querySelector('#path-toggle');

    state.currentPathIdx = 0;

    function showPercCluster(clusterIdx, pathIdx) {
      if (!percClusters.length) { if (infoEl) infoEl.innerHTML = 'No percolating'; return; }
      clusterIdx = ((clusterIdx % percClusters.length) + percClusters.length) % percClusters.length;
      state.percIdx = clusterIdx;
      const origIdx = clusters.indexOf(percClusters[clusterIdx]);
      const cluster = percClusters[clusterIdx];
      const allPaths = cluster.paths || (cluster.path ? [cluster.path] : []);
      const pi = pathIdx !== undefined ? pathIdx : 0;
      highlightCluster(origIdx, scene, state, infoEl, pi);
      if (currentEl) currentEl.textContent = `${clusterIdx+1}-${pi+1}`;
      if (totalEl) totalEl.textContent = `/ ${percClusters.length} (${allPaths.length}경로)`;
    }

    function clearPath() {
      if (state.pathGroup) { scene.remove(state.pathGroup); state.pathGroup = null; }
      resetSEColors(state);
      if (infoEl) infoEl.innerHTML = '';
      if (currentEl) currentEl.textContent = '-';
    }

    if (pathToggle) pathToggle.addEventListener('change', () => {
      if (pathToggle.checked) {
        pathControls.style.display = 'block';
        state.currentPathIdx = 0;
        if (percClusters.length > 0) showPercCluster(state.percIdx, 0);
      } else {
        pathControls.style.display = 'none';
        clearPath();
      }
    });

    if (prevBtn) prevBtn.addEventListener('click', () => {
      const pi = (state.currentPathIdx || 0) - 1;
      if (pi < 0) {
        // 이전 클러스터의 마지막 path
        const prevCluster = percClusters[((state.percIdx - 1) + percClusters.length) % percClusters.length];
        const prevPaths = prevCluster.paths || [prevCluster.path];
        showPercCluster(state.percIdx - 1, prevPaths.length - 1);
      } else {
        showPercCluster(state.percIdx, pi);
      }
    });
    if (nextBtn) nextBtn.addEventListener('click', () => {
      const curCluster = percClusters[state.percIdx];
      const curPaths = curCluster.paths || [curCluster.path];
      const pi = (state.currentPathIdx || 0) + 1;
      if (pi >= curPaths.length) {
        // 다음 클러스터의 첫 path
        showPercCluster(state.percIdx + 1, 0);
      } else {
        showPercCluster(state.percIdx, pi);
      }
    });

    animate();
  }).catch(err => {
    console.error('viewer3d: failed to load data', err);
    clearInterval(fetchTimer);
    overlay.style.background = 'rgba(127,29,29,.85)';
    overlay.style.color = '#fee2e2';
    overlay.style.maxWidth = 'calc(100% - 24px)';
    overlay.style.whiteSpace = 'pre-wrap';
    overlay.style.lineHeight = '1.5';
    overlay.innerHTML =
      `<b>3D viewer 로딩 실패</b>\n`
      + `URL: <code style="font-size:12px">${dataUrl}</code>\n`
      + `Error: ${err && err.message ? err.message : String(err)}\n\n`
      + `<span style="color:#fca5a5;font-size:12px">`
      + `브라우저 DevTools Console / Network 탭에서 자세한 trace 확인 가능.`
      + `</span>`;
  });

  /* ── animation loop ──────────────────────────────────────── */
  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }

  /* resize */
  const ro = new ResizeObserver(() => {
    const w = container.clientWidth, h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });
  ro.observe(container);

  /* cluster input is handled via event listener in data fetch callback */
}

/* ── build scene from data ─────────────────────────────────── */
function buildScene(scene, camera, controls, data, state) {
  state.scene = scene;  // stash for view-mode overlays (e.g. brittle glow group)
  const box = data.box;
  // Z-up coordinate system: Three.js Y-up → swap Y↔Z for display
  // Data: x, y (horizontal), z (up=electrode height)
  // Three.js: x, y(=data z, up), z(=data y)
  const cx = (box.x_min + box.x_max) / 2;
  const cy = (box.z_min + box.z_max) / 2;  // data Z → Three.js Y (up)
  const cz = (box.y_min + box.y_max) / 2;  // data Y → Three.js Z
  const bw = box.x_max - box.x_min;
  const bh = box.z_max - box.z_min;  // height = data Z range
  const bd = box.y_max - box.y_min;
  const maxDim = Math.max(bw, bh, bd);

  /* camera position - isometric-ish view */
  camera.position.set(cx + maxDim * 1.2, cy + maxDim * 0.8, cz + maxDim * 1.2);
  controls.target.set(cx, cy, cz);
  controls.update();
  state.defaultCamPos = camera.position.clone();
  state.defaultTarget = controls.target.clone();

  /* set zoom limits based on data size */
  controls.minDistance = maxDim * 0.3;
  controls.maxDistance = maxDim * 4;

  /* bounding box wireframe */
  const bbGeo = new THREE.BoxGeometry(bw, bh, bd);
  const bbMat = new THREE.LineBasicMaterial({ color: 0x888888 });
  const bbEdges = new THREE.EdgesGeometry(bbGeo);
  const bbLine = new THREE.LineSegments(bbEdges, bbMat);
  bbLine.position.set(cx, cy, cz);
  bbLine.userData.isDecoration = true;
  scene.add(bbLine);

  /* grid at bottom (Y=0 in Three.js = Z=0 in data) */
  const gridSize = Math.max(bw, bd) * 1.2;
  const grid = new THREE.GridHelper(gridSize, 20, 0xcccccc, 0xe0e0e0);
  grid.position.set(cx, box.z_min, cz);
  grid.userData.isDecoration = true;
  scene.add(grid);

  /* axis labels (Z-up convention) */
  addAxisLabels(scene, box);

  /* group particles by type */
  const groups = { AM_P: [], AM_S: [], SE: [] };
  const idIndex = {};
  data.particles.forEach((p, i) => {
    if (groups[p.type]) groups[p.type].push(p);
    idIndex[p.id] = p;
  });
  state.idIndex = idIndex;

  /* instanced meshes.
   * Atoms-only mode = process view (no type distinction) → all light grey.
   * Full mode = per-type colouring (AM_P dark, AM_S mid-grey, SE yellow). */
  const atomsOnly = !!data.atoms_only;
  if (atomsOnly) {
    state.meshes.AM_P = createInstancedSpheres(groups.AM_P, 16, COL.ATOMS_ONLY, 1.0, false);
    state.meshes.AM_S = createInstancedSpheres(groups.AM_S, 16, COL.ATOMS_ONLY, 1.0, false);
    state.meshes.SE   = createInstancedSpheres(groups.SE,   16, COL.ATOMS_ONLY, 1.0, false);
    // Strong directional + low ambient: lit tops read near-white, shadow
    // undersides go dark so spheres have clear rim definition (matches
    // typical 3D-render reference: bright highlight + deep shadow).
    scene.traverse(obj => {
      if (obj.isAmbientLight)      obj.intensity = 0.3;
      else if (obj.isDirectionalLight) obj.intensity = 0.9;
    });
  } else {
    state.meshes.AM_P = createInstancedSpheres(groups.AM_P, 16, COL.AM_P, 1.0, false);
    state.meshes.AM_S = createInstancedSpheres(groups.AM_S, 16, COL.AM_S, 1.0, false);
    state.meshes.SE   = createInstancedSpheres(groups.SE,   12, COL.SE, OPA.SE, true);
  }
  state.atomsOnly = atomsOnly;
  state.seParticles = groups.SE;
  state.amParticles = [...groups.AM_P, ...groups.AM_S];
  state.amPParticles = groups.AM_P;
  state.amSParticles = groups.AM_S;

  Object.values(state.meshes).forEach(m => { if (m) scene.add(m); });

  /* compaction-plate STL mesh (DEM) — OR, for MPM, the compacted-SE surface.
   * For MPM colour it like the DEM SE (gold), not the blue plate; keep the
   * see-through opacity so the AM spheres stay visible through the SE shell. */
  if (data.mesh_triangles && data.mesh_triangles.length > 0) {
    state.meshes.MESH = buildPlateMesh(data.mesh_triangles,
      data.kind === 'mpm' ? { color: COL.SE } : null);
    if (state.meshes.MESH) scene.add(state.meshes.MESH);
  }
}

/* ── compaction-plate mesh from STL triangles ──────────────── */
function buildPlateMesh(triangles, opts) {
  if (!triangles || !triangles.length) return null;
  opts = opts || {};
  const positions = new Float32Array(triangles.length * 9);
  let p = 0;
  // Z-up: data (x,y,z) → Three.js (x,z,y)
  triangles.forEach(tri => {
    for (let i = 0; i < 3; i++) {
      positions[p++] = tri[i][0];  // x
      positions[p++] = tri[i][2];  // data z → Three.js y (up)
      positions[p++] = tri[i][1];  // data y → Three.js z
    }
  });
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.computeVertexNormals();
  const mat = new THREE.MeshPhongMaterial({
    color: opts.color != null ? opts.color : COL.MESH,
    transparent: true,
    opacity: opts.opacity != null ? opts.opacity : OPA.MESH,
    side: THREE.DoubleSide,
    depthWrite: false,
  });
  return new THREE.Mesh(geo, mat);
}

/* ── instanced sphere builder ──────────────────────────────── */
// NOTE: Three.js multiplies instanceColor by material.color in the shader.
// Keep material.color = white so per-instance setColorAt() values render
// faithfully (otherwise dark base colors like AM_P=0x222222 wash out the
// brittle-mode highlights yellow→red into near-black).
function createInstancedSpheres(particles, segments, color, opacity, transparent) {
  if (!particles.length) return null;
  const geo = new THREE.SphereGeometry(1, segments, segments);
  const mat = new THREE.MeshPhongMaterial({
    color: 0xffffff, transparent, opacity, depthWrite: !transparent, side: THREE.FrontSide,
  });
  const mesh = new THREE.InstancedMesh(geo, mat, particles.length);
  const dummy = new THREE.Object3D();
  const col = new THREE.Color();
  particles.forEach((p, i) => {
    dummy.position.set(p.x, p.z, p.y);  // Z-up: swap Y↔Z
    dummy.scale.setScalar(p.r);
    dummy.updateMatrix();
    mesh.setMatrixAt(i, dummy.matrix);
    mesh.setColorAt(i, col.setHex(color));
  });
  mesh.instanceMatrix.needsUpdate = true;
  if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  mesh.userData.particles = particles;
  mesh.userData.baseColor = color;
  return mesh;
}

/* ── high-resolution screenshot helper ─────────────────────── *
 * Temporarily resizes the renderer to `scale`× its current size (with
 * pixelRatio=1 so dimensions are controlled exactly), renders once,
 * grabs a PNG data URL, and restores the original viewport. Uses the
 * `updateStyle=false` flag on setSize so the on-screen CSS size is
 * untouched and nothing flickers for the user.
 *
 * Typical container ~1000×800 → scale=4 → 4000×3200 ≈ 13 MP PNG.
 * File size is large (a few MB per shot) but suitable for paper figures.
 */
function captureHighRes(renderer, scene, camera, scale = 4) {
  const origSize = new THREE.Vector2();
  renderer.getSize(origSize);
  const origPixelRatio = renderer.getPixelRatio();
  const targetW = Math.round(origSize.x * scale);
  const targetH = Math.round(origSize.y * scale);

  renderer.setPixelRatio(1);
  renderer.setSize(targetW, targetH, false);
  renderer.render(scene, camera);
  const dataUrl = renderer.domElement.toDataURL('image/png');

  renderer.setPixelRatio(origPixelRatio);
  renderer.setSize(origSize.x, origSize.y, false);
  renderer.render(scene, camera);
  return dataUrl;
}

/* ── save-with-dialog helper ───────────────────────────────── *
 * Uses File System Access API (showSaveFilePicker) when available
 * to prompt native "Save As" dialog. Falls back to <a> download
 * (auto-saves to Downloads folder) for browsers without the API.
 *
 * dataUrl     : image/png data URL from canvas.toDataURL()
 * defaultName : suggested filename shown in dialog
 * btn         : button element whose textContent is flashed to '✓ Saved'
 * resetLabel  : original button text to restore after flash
 */
async function saveWithDialog(dataUrl, defaultName, btn, resetLabel) {
  const flash = (msg) => {
    if (btn) {
      const orig = resetLabel || btn.textContent;
      btn.textContent = msg;
      setTimeout(() => { btn.textContent = orig; }, 1500);
    }
  };
  // Convert dataURL to Blob
  const byteStr = atob(dataUrl.split(',')[1]);
  const ab = new ArrayBuffer(byteStr.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteStr.length; i++) ia[i] = byteStr.charCodeAt(i);
  const blob = new Blob([ab], { type: 'image/png' });

  // Try File System Access API (prompts native Save As dialog)
  if (window.showSaveFilePicker) {
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: defaultName,
        types: [{ description: 'PNG image', accept: { 'image/png': ['.png'] } }],
      });
      const writable = await handle.createWritable();
      await writable.write(blob);
      await writable.close();
      flash('✓ Saved');
      return;
    } catch (e) {
      if (e.name === 'AbortError') {
        // User cancelled — do nothing
        return;
      }
      console.warn('showSaveFilePicker failed, falling back:', e);
    }
  }
  // Fallback: auto-download to browser's Downloads folder
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = defaultName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  flash('✓ Downloaded');
}

/* ── axis labels using sprite text ─────────────────────────── */
function addAxisLabels(scene, box) {
  // Z-up: X→right, Y→depth(Three.js Z), Z→up(Three.js Y)
  const labels = [
    { text: 'X (μm)', pos: [box.x_max + 5, box.z_min, (box.y_min+box.y_max)/2] },
    { text: 'Y (μm)', pos: [(box.x_min+box.x_max)/2, box.z_min, box.y_max + 5] },
    { text: 'Z (μm)', pos: [box.x_min - 5, box.z_max + 5, (box.y_min+box.y_max)/2] },
  ];
  labels.forEach(l => {
    const canvas = document.createElement('canvas');
    canvas.width = 512; canvas.height = 128;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#000000';
    ctx.font = 'bold 72px Arial, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(l.text, 256, 64);
    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, depthWrite: false });
    const sprite = new THREE.Sprite(mat);
    sprite.position.set(...l.pos);
    sprite.scale.set(20, 8, 1);
    sprite.userData.isDecoration = true;
    sprite.userData.isAxisLabel = true;
    scene.add(sprite);
  });
}

/* ── SE percolation colouring ──────────────────────────────── */
function applyPercolation(state, on) {
  state.percolationOn = on;
  const mesh = state.meshes.SE;
  if (!mesh) return;
  const particles = mesh.userData.particles;
  const perc = state.data.percolation || {};
  const topSet = new Set(perc.top_reachable || []);
  const botSet = new Set(perc.bottom_se || []);
  const topSESet = new Set(perc.top_se || []);
  const col = new THREE.Color();

  particles.forEach((p, i) => {
    if (on) {
      if (botSet.has(p.id)) { col.setHex(COL.SE_BOTTOM); }
      else if (topSESet.has(p.id)) { col.setHex(COL.SE_TOP); }
      else if (topSet.has(p.id)) { col.setHex(COL.SE_TOP_REACH); }
      else { col.setHex(COL.SE_NON_REACH); }
    } else {
      col.setHex(COL.SE);
    }
    mesh.setColorAt(i, col);
  });
  mesh.instanceColor.needsUpdate = true;

  /* adjust per-instance opacity via material - we use a single material so set average */
  if (on) {
    mesh.material.opacity = OPA.SE_REACH;
  } else {
    mesh.material.opacity = OPA.SE;
  }
}

/* ── Cluster highlight by index ────────────────────────────── */
function highlightCluster(idx, scene, state, infoEl, pathIdx) {
  const particles = state.seParticles;
  if (!particles) return;

  /* clear previous */
  if (state.pathGroup) { scene.remove(state.pathGroup); state.pathGroup = null; }
  resetSEColors(state);

  const clusterList = ((state.data.clusters || {}).clusters) || [];
  if (idx < 0 || idx >= clusterList.length) {
    if (infoEl) infoEl.innerHTML = '';
    return;
  }

  const cluster = clusterList[idx];
  const allPaths = cluster.paths || (cluster.path ? [cluster.path] : []);
  state.currentClusterPaths = allPaths;
  state.currentPathIdx = pathIdx || 0;

  /* Path ON: cluster = blue, rest = yellow, all opacity 0.1 */
  const clusterSet = new Set(cluster.ids);
  const mesh = state.meshes.SE;
  const col = new THREE.Color();
  particles.forEach((p, i) => {
    if (clusterSet.has(p.id)) {
      col.setHex(0x2196F3);  // blue
    } else {
      col.setHex(COL.SE);    // yellow
    }
    mesh.setColorAt(i, col);
  });
  mesh.instanceColor.needsUpdate = true;
  mesh.material.opacity = 0.05;

  /* info text */
  const pi = state.currentPathIdx;
  let html = `<b>#${idx}</b> ${cluster.size}개`;
  html += cluster.percolating ? ` <span style="color:#34D399">✓</span>` : ` <span style="color:#F87171">✗</span>`;
  if (allPaths.length > 1) {
    const cat = allPaths[pi]?.category || '';
    const catLabel = cat === 'best' ? '🟢best' : cat === 'worst' ? '🔴worst' : '🟡mean';
    html += `<br>Path ${pi+1}/${allPaths.length} ${catLabel}`;
  }

  /* draw selected path */
  const path = allPaths[pi];
  if (path && path.ids) {
    const pts = path.ids.map(id => {
      const p = state.idIndex[id];
      return p ? new THREE.Vector3(p.x, p.z, p.y) : null;
    }).filter(Boolean);

    if (pts.length >= 2) {
      const group = new THREE.Group();
      const box = state.data.box;
      const halfX = (box.x_max - box.x_min) / 2;
      const halfY = (box.y_max - box.y_min) / 2;

      /* draw segments, detect periodic jumps */
      const mkSphere = (pos, color, size) => {
        const g = new THREE.SphereGeometry(size || 1.8, 12, 12);
        const m = new THREE.MeshPhongMaterial({ color });
        const s = new THREE.Mesh(g, m);
        s.position.copy(pos);
        return s;
      };

      for (let j = 0; j < pts.length - 1; j++) {
        const a = pts[j], b = pts[j+1];
        // Check periodic jump: x or z (=data y) distance > half box
        const dx = Math.abs(a.x - b.x);
        const dz = Math.abs(a.z - b.z);  // Three.js z = data y
        const isPeriodic = dx > halfX || dz > halfY;

        if (isPeriodic) {
          // Mark both ends with red spheres, skip the tube
          group.add(mkSphere(a, 0xFF0000, 0.5));
          group.add(mkSphere(b, 0xFF0000, 0.5));
        } else {
          const seg = new THREE.TubeGeometry(
            new THREE.LineCurve3(a, b), 1, 0.5, 6, false
          );
          const mat = new THREE.MeshPhongMaterial({
            color: COL.PATH, emissive: COL.PATH, emissiveIntensity: 0.3,
          });
          group.add(new THREE.Mesh(seg, mat));
        }
      }

      /* start(bottom cyan) / end(top red) markers */
      group.add(mkSphere(pts[0], 0x22D3EE, 1.8));
      group.add(mkSphere(pts[pts.length - 1], 0xF87171, 1.8));

      scene.add(group);
      state.pathGroup = group;

      html += `<br>τ=${path.tortuosity} L=${path.path_length}μm`;
    }
  }

  if (infoEl) infoEl.innerHTML = html;
}

function resetSEColors(state) {
  const mesh = state.meshes.SE;
  if (!mesh) return;
  const col = new THREE.Color(COL.SE);
  const particles = state.seParticles || [];
  particles.forEach((p, i) => mesh.setColorAt(i, col));
  mesh.instanceColor.needsUpdate = true;
  mesh.material.opacity = OPA.SE;  // back to 0.85
}

/* round point sprite (soft disc) — raw THREE.Points draw hard SQUARES; cached radial-alpha texture */
function roundDotTex() {
  if (!roundDotTex._t) {
    const cv = document.createElement('canvas'); cv.width = cv.height = 64;
    const c2 = cv.getContext('2d');
    const rg = c2.createRadialGradient(32, 32, 0, 32, 32, 30);
    rg.addColorStop(0.0, 'rgba(255,255,255,1)');
    rg.addColorStop(0.75, 'rgba(255,255,255,1)');
    rg.addColorStop(1.0, 'rgba(255,255,255,0)');
    c2.fillStyle = rg; c2.beginPath(); c2.arc(32, 32, 30, 0, 2 * Math.PI); c2.fill();
    roundDotTex._t = new THREE.CanvasTexture(cv);
  }
  return roundDotTex._t;
}

/* CBD-style carbon CLUSTER DOMAINS — currently UNWIRED (user pref 2026-07-10: the econn mode
 * shows AM connectivity only; keep this for a future carbon-network / STEP3 mode):
 * the CONDUCTIVE additive geometry (phases 2 VGCF · 3 SuperP · 5 SDCP; PTFE 4 = e-insulator,
 * NOT drawn — it is not in the econn graph) is grouped into clusters by voxel-adjacency
 * union-find (0.3µm, ≈ the payload's econn labelling) and each cluster is rendered as a FUSED
 * translucent blob of soft discs — reads like the carbon-binder-domain (CBD) phase, one colour
 * per cluster (golden-angle categorical HSL).  So: clusters read APART by colour, and the
 * cluster COUNT reads at a glance (85 film mega-sheets = few big patches; 32k bulk chains =
 * confetti).  Clustering runs on the DISPLAYED (subsampled) geometry → the displayed count can
 * differ from the full-res econn_summary number; the legend shows both (summary = quantitative).
 * Returns {shown, nClusters, biggestPct} or null. */
function buildEconnClusters(state) {
  const COND = new Set([2, 3, 5]);
  const fibres = ((state.data && state.data.additive_fibres) || []).filter(f => COND.has(f.phase));
  const fibrePh = new Set(fibres.map(f => f.phase));
  const loose = ((state.data && state.data.additive_points) || [])
    .filter(p => COND.has(p[3]) && !fibrePh.has(p[3]));
  const ents = [];                                   // entity = one fibre (vertices move together) or one loose pt
  for (const f of fibres) ents.push(f.pts);
  for (const p of loose) ents.push([[p[0], p[1], p[2]]]);
  if (!ents.length) return null;
  const parent = Array.from({ length: ents.length }, (_, i) => i);
  const find = (a) => { while (parent[a] !== a) { parent[a] = parent[parent[a]]; a = parent[a]; } return a; };
  const union = (a, b) => { const ra = find(a), rb = find(b); if (ra !== rb) parent[ra] = rb; };
  const VOX = 0.3;                                   // µm — matches econn vox_um
  const occ = new Map();                             // voxel key → first entity seen there
  for (let e = 0; e < ents.length; e++) {
    for (const q of ents[e]) {
      const i = Math.floor(q[0] / VOX), j = Math.floor(q[1] / VOX), k = Math.floor(q[2] / VOX);
      for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) for (let dk = -1; dk <= 1; dk++) {
        const key = (i + di) + '_' + (j + dj) + '_' + (k + dk);
        const o = occ.get(key);
        if (o === undefined) { if (!di && !dj && !dk) occ.set(key, e); }
        else if (o !== e) union(e, o);
      }
    }
  }
  const rootIdx = new Map(); const sizes = [];
  const clOf = new Array(ents.length);
  for (let e = 0; e < ents.length; e++) {
    const r = find(e);
    if (!rootIdx.has(r)) { rootIdx.set(r, rootIdx.size); sizes.push(0); }
    clOf[e] = rootIdx.get(r);
    sizes[clOf[e]] += ents[e].length;
  }
  const nCl = rootIdx.size;
  const nPts = ents.reduce((a, b) => a + b.length, 0);
  // categorical colour per cluster: golden-angle hue → adjacent ids maximally apart; mid lightness
  // so the translucent blobs stay readable on the white canvas
  const cc = new THREE.Color();
  const grp = new THREE.Group();
  const pos = new Float32Array(nPts * 3), col = new Float32Array(nPts * 3);
  let w = 0;
  for (let e = 0; e < ents.length; e++) {
    cc.setHSL(((clOf[e] * 137.508) % 360) / 360, 0.72, 0.46);
    for (const q of ents[e]) {
      pos[3 * w] = q[0]; pos[3 * w + 1] = q[2]; pos[3 * w + 2] = q[1];   // Z-up swap
      col[3 * w] = cc.r; col[3 * w + 1] = cc.g; col[3 * w + 2] = cc.b; w++;
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  // CBD look = two fused layers: a wide faint halo (domain body) + a smaller firmer core.
  // Both x-ray (depthTest off) so the domains show threading between the opaque AM.
  for (const [sz, op] of [[1.5, 0.16], [0.65, 0.55]]) {
    const pm = new THREE.Points(g, new THREE.PointsMaterial({
      size: sz, vertexColors: true, sizeAttenuation: true, depthTest: false, depthWrite: false,
      map: roundDotTex(), transparent: true, opacity: op, alphaTest: 0.05 }));
    pm.renderOrder = 999; grp.add(pm);
  }
  state.additivePointGroup = grp;                    // reuse the mode-switch cleanup hook
  if (state.scene) state.scene.add(grp);
  const biggest = sizes.length ? Math.max(...sizes) : 0;
  return { shown: nPts, nClusters: nCl, biggestPct: nPts ? 100 * biggest / nPts : 0 };
}

/* Build the conductive-additive point cloud (payload additive_points: [x,y,z,phase]) and add it to
 * the scene as state.additivePointGroup.  Used both as a subtle overlay on the Default view (so the
 * carbon is visible inside the normal AM/SE structure) and as the prominent 도전재 mode.  Points draw
 * x-ray (depthTest off, renderOrder 999) so they show through opaque SE/AM.  `only` filters one phase. */
function buildCarbonOverlay(state, only, size, colorOverride) {
  // colorOverride: a single colour for all carbon (e.g. soft black in the Default overlay so it reads
  // SEM-like and doesn't drown the structure).  null → per-phase colours (cyan VGCF) for the 도전재 mode.
  const PHCOL = { 2: 0x22d3ee, 3: 0xec4899, 4: 0xf59e0b, 5: 0xff3b30, 6: 0x22c55e };   // VGCF cyan · Super P magenta · PTFE amber · SWCNT sheath green(A14) ·
  //   SDCP RED (was lime — lime sank into the olive-brown blend thousands of x-ray fibre lines make; red is the
  //   complement of that mush so the 0.3µm particles pop.  vs SuperP magenta: red 5° vs pink 330°, still distinct)
  const colOf = (ph) => (colorOverride != null ? colorOverride : (PHCOL[ph] || 0x22d3ee));
  const fibres = (state.data && state.data.additive_fibres) || [];   // [{phase, pts:[[x,y,z]…]}]
  const pts0 = (state.data && state.data.additive_points) || [];
  const grp = new THREE.Group();
  let n = 0;
  const cc = new THREE.Color();
  // periodic x,y: when a fibre wraps the boundary its two endpoints sit on opposite sides, so the
  // polyline would draw a chord across the whole RVE.  Skip any segment that jumps > half the box.
  const box = (state.data && state.data.box) || {};
  const halfX = ((box.x_max || 50) - (box.x_min || 0)) * 0.5;
  const halfY = ((box.y_max || 50) - (box.y_min || 0)) * 0.5;
  // fibres (VGCF/PTFE) → individual lines (a fibre is a discrete rod, not a continuum)
  if (fibres.length) {
    const segPos = [], segCol = [];      // main carbon (per-phase colour, or soft-black in Default)
    const binPos = [], binCol = [];      // PTFE binder in Default mode → faint whitish, blended-in
    for (const f of fibres) {
      if (only && f.phase !== only) continue;
      // In the Default overlay (colorOverride set), PTFE reads as a faint off-white binder film
      // (polymer binder is light, not black) so it "blends" into the structure instead of standing
      // out as hard rods.  The dedicated 도전재 / PTFE-only modes keep PTFE amber (colorOverride null).
      const binder = (colorOverride != null && f.phase === 4);
      cc.set(binder ? 0xe6decb : colOf(f.phase));
      // per-fibre thickness (PTFE roll-fibrillation: d∝√(V_i/L_i) — thick short stub vs thin long strand).
      // WebGL line width is unreliable, so thickness is shown as BRIGHTNESS: thick fibrils read solid, thin
      // strands fade out (d is a relative Ø, median ~1; clamp the tail).  Uniform fibres (VGCF, no d) → 1.
      let tf = 1.0;
      if (f.d != null) { const d = Math.max(0.5, Math.min(2.0, f.d)); tf = 0.4 + 0.6 * ((d - 0.5) / 1.5); }
      const cr = cc.r * tf, cg = cc.g * tf, cb = cc.b * tf;
      const P = f.pts;
      const sp = binder ? binPos : segPos, sc = binder ? binCol : segCol;
      for (let i = 0; i + 1 < P.length; i++) {           // Z-up swap (x,z,y) per vertex
        const a = P[i], b = P[i + 1];
        if (Math.abs(a[0] - b[0]) > halfX || Math.abs(a[1] - b[1]) > halfY) continue;   // periodic wrap chord
        sp.push(a[0], a[2], a[1], b[0], b[2], b[1]);
        sc.push(cr, cg, cb, cr, cg, cb);
        n++;
      }
    }
    const mkLines = (pos, colr, opacity) => {
      if (!pos.length) return;
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(colr, 3));
      const lines = new THREE.LineSegments(g, new THREE.LineBasicMaterial({
        vertexColors: true, depthTest: false, depthWrite: false, transparent: true, opacity }));
      lines.renderOrder = 999; grp.add(lines);
    };
    mkLines(segPos, segCol, 1.0);
    mkLines(binPos, binCol, 0.6);        // binder drawn faint so it blends into the Default view
  }
  // points: only for phases NOT already drawn as fibre/chain lines (avoids double-render — SuperP is
  // now branched chains too, so it's in additive_fibres; a payload without fibre data falls back to points)
  const fibrePhases = new Set(fibres.map(f => f.phase));
  const pts = pts0.filter(p => (!only || p[3] === only) && !fibrePhases.has(p[3]));
  if (pts.length) {
    const g = new THREE.BufferGeometry();
    const pos = new Float32Array(pts.length * 3), col = new Float32Array(pts.length * 3);
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      pos[3 * i] = p[0]; pos[3 * i + 1] = p[2]; pos[3 * i + 2] = p[1];
      cc.set(colOf(p[3]));
      col[3 * i] = cc.r; col[3 * i + 1] = cc.g; col[3 * i + 2] = cc.b;
    }
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    // round-dot sprite (raw THREE.Points draw hard squares — user-reported blocky pixels)
    const pm = new THREE.Points(g, new THREE.PointsMaterial({
      size, vertexColors: true, sizeAttenuation: true, depthTest: false, depthWrite: false,
      map: roundDotTex(), transparent: true, alphaTest: 0.3 }));
    pm.renderOrder = 999; grp.add(pm); n += pts.length;
  }
  if (n === 0) return 0;
  state.additivePointGroup = grp;                          // a Group (lines + points) — cleanup traverses it
  if (state.scene) state.scene.add(grp);
  return n;
}

/* ── View-mode rendering — re-colour all instanced meshes ─── */
function applyViewMode(state, mode) {
  state.viewMode = mode;
  const aux = (state.data && state.data.aux) || {};
  const colDim    = new THREE.Color(COL.DIM);
  const colSeBase = new THREE.Color(COL.SE);

  /* Tear down view-mode overlays (Brittle Hotspots cap patches,
   * Cluster Coloring split-mesh) before reapplying any mode — stale
   * geometry left around confuses every other mode. */
  if (state.brittleGlowGroup && state.scene) {
    state.scene.remove(state.brittleGlowGroup);
    state.brittleGlowGroup.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
    state.brittleGlowGroup = null;
  }
  if (state.clusterOverlay && state.scene) {
    state.scene.remove(state.clusterOverlay);
    state.clusterOverlay.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
    state.clusterOverlay = null;
    // Restore the original SE InstancedMesh visibility (hidden while
    // cluster mode owned the SE rendering).
    if (state.meshes && state.meshes.SE) state.meshes.SE.visible = true;
  }
  if (state.combinedOverlay && state.scene) {
    state.scene.remove(state.combinedOverlay);
    state.combinedOverlay.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
    state.combinedOverlay = null;
  }
  if (state.coveragePatchGroup && state.scene) {
    state.scene.remove(state.coveragePatchGroup);
    if (state.coveragePatchGroup.geometry) state.coveragePatchGroup.geometry.dispose();
    if (state.coveragePatchGroup.material) state.coveragePatchGroup.material.dispose();
    state.coveragePatchGroup = null;
  }
  if (state.strainPointGroup && state.scene) {
    state.scene.remove(state.strainPointGroup);
    if (state.strainPointGroup.geometry) state.strainPointGroup.geometry.dispose();
    if (state.strainPointGroup.material) state.strainPointGroup.material.dispose();
    state.strainPointGroup = null;
  }
  ['st4Group', 'st4FaceGroup'].forEach(k => {               // STEP4-v2 동역학 레이어
    if (state[k] && state.scene) {
      state.scene.remove(state[k]);
      if (state[k].dispose) state[k].dispose();              // InstancedMesh 인스턴스 GL버퍼 해제 (리뷰 R2#2 누수)
      if (state[k].geometry) state[k].geometry.dispose();
      if (state[k].material) state[k].material.dispose();
      state[k] = null;
    }
  });
  if (state.meshes && state.meshes.MESH && state.meshes.MESH.userData._baseColor) {
    state.meshes.MESH.material.color.setHex(state.meshes.MESH.userData._baseColor);   // je-mode navy → base
    delete state.meshes.MESH.userData._baseColor;
  }
  if (state.additivePointGroup && state.scene) {          // conductive-additive Group (lines + points)
    state.scene.remove(state.additivePointGroup);
    state.additivePointGroup.traverse(o => {
      if (o.geometry) o.geometry.dispose();
      if (o.material) o.material.dispose();
    });
    state.additivePointGroup = null;
  }
  if (state.meshes && state.meshes.MESH) {                 // restore SE mesh (se_strain hides it; additives dims it)
    const _mcb = document.querySelector('.viewer-controls input[data-layer="MESH"]');
    state.meshes.MESH.visible = _mcb ? _mcb.checked : true;
    state.meshes.MESH.material.opacity = OPA.MESH;         // undo the additives-mode translucency
  }
  ['AM_P', 'AM_S'].forEach(t => {                          // undo additives/se_engagement AM dimming + pore-mode hide
    const m = state.meshes && state.meshes[t];
    if (m && m.material) { m.material.opacity = 1.0; m.material.transparent = false; }
    if (m) { const cb = document.querySelector(`.viewer-controls input[data-layer="${t}"]`); m.visible = cb ? cb.checked : true; }
    if (m && m.instanceColor) {                            // repaint AM base colour so a prior mode's
      const base = new THREE.Color(COL[t]);                //   per-instance tint (je dark navy, ji_field
      m.userData.particles.forEach((_, i) => m.setColorAt(i, base));   //   0x0a0e1a, additives SEM-black)
      m.instanceColor.needsUpdate = true;                  //   never bleeds into a mode that skips AM
    }
  });
  // analysis modes are POST-compaction results — in the "압축 전" (loose seed) view they
  // don't exist yet, so show the loose SE + a note instead of the (compacted) field.
  if (state.isSeed && (mode === 'coverage' || mode === 'coverage_patches' || mode === 'se_strain')) {
    setLegend(state, '<i>이건 <b>압축 후</b> 결과예요 (변형·coverage는 압축의 결과). '
      + '위 "MPM (압축 후)"에서 보세요 — 여기 "압축 전"은 loose seed라 아직 0이에요.</i>');
    return;
  }
  /* Phase B — restore any per-instance scale modifications from se_diagnostics */
  if (state.seInstanceScaleModified) {
    const dummy = new THREE.Object3D();
    ['SE', 'AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        dummy.position.set(p.x, p.z, p.y);
        dummy.scale.setScalar(p.r);
        dummy.updateMatrix();
        m.setMatrixAt(i, dummy.matrix);
      });
      m.instanceMatrix.needsUpdate = true;
    });
    state.seInstanceScaleModified = false;
  }
  /* Phase B — fracture overlays */
  if (state.stressChainGroup && state.scene) {
    state.scene.remove(state.stressChainGroup);
    state.stressChainGroup.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
    state.stressChainGroup = null;
  }

  /* default: restore base colours + opacities */
  if (!mode || mode === 'default') {
    ['AM_P', 'AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      const base = new THREE.Color(COL[t]);
      m.userData.particles.forEach((p, i) => m.setColorAt(i, base));
      m.instanceColor.needsUpdate = true;
      m.material.opacity = (t === 'SE' ? OPA.SE : 1.0);
      m.material.transparent = (t === 'SE');
    });
    // overlay the carbon on the NORMAL AM/SE structure (x-ray, modest size) — so VGCF/PTFE are
    // visible right in the default view, not only in the dedicated 도전재 mode.
    const nCarbon = buildCarbonOverlay(state, 0, 0.55, 0x3a3a3a);   // soft black in Default (SEM-like, subtle)
    const ac = (state.data && state.data.mpm_metrics && state.data.mpm_metrics.additive_counts) || {};
    const carbonLeg = nCarbon
      ? `<br><span style="color:#22d3ee">●</span> 도전재 overlay (${Object.keys(ac).filter(k => ac[k]).join('/')}) — 자세히는 View Mode "도전재"`
      : '';
    setLegend(state,
      `<b>Default — natural particle colours</b>
       <span style="color:#222222">●</span> AM_P (polycrystalline, ~6 µm)
       <span style="color:#888888">●</span> AM_S (single-crystal, ~2 µm)
       <span style="color:#f5e6a3">●</span> SE (LPSCl, ~0.5 µm, translucent)${carbonLeg}
       <span style="color:#9ca3af;font-size:11px">
         · View Mode 드롭다운으로 brittle / cluster / stress / coverage 분석 모드 전환
       </span>`);
    return;
  }

  /* helper: dim a particle (set near-bg colour). */
  function dimAll() {
    ['AM_P', 'AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((_, i) => m.setColorAt(i, colDim));
      m.material.opacity = 0.18;
      m.material.transparent = true;
    });
  }
  function flushColors() {
    ['AM_P', 'AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t];
      if (m && m.instanceColor) m.instanceColor.needsUpdate = true;
    });
  }

  if (mode === 'brittle') {
    dimAll();
    /* Pick worst stage per AM particle from brittle_pairs list */
    const stageById = {};
    (aux.brittle_pairs || []).forEach(b => {
      [b.id1, b.id2].forEach(id => {
        const cur = stageById[id];
        if (!cur || STAGE_RANK[b.stage] > STAGE_RANK[cur]) stageById[id] = b.stage;
      });
    });
    /* Apply colours on AM meshes */
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        const stage = stageById[p.id];
        if (stage) {
          m.setColorAt(i, new THREE.Color(STAGE_COL[stage]));
        }
      });
      m.material.opacity = 0.95;
      m.material.transparent = true;
    });
    /* AM with no brittle contact stays dim. SE always dim in this mode. */
    flushColors();
    setLegend(state,
      `<b>Brittle Stage (Auerbach + Lawn 1998)</b>
       <span style="color:#ffeda0">●</span> microcrack
       <span style="color:#feb24c">●</span> multicrack
       <span style="color:#f03b20">●</span> fragmentation
       <span style="color:#800026">●</span> pulverization
       (${(aux.brittle_pairs || []).length} damaged AM-AM pairs)
       <button id="brittle-z-modal-btn" class="data-modal-btn">
         <span class="ico">📊</span><span>Z-profile 데이터</span>
       </button>`);
    const btn = document.getElementById('brittle-z-modal-btn');
    if (btn) btn.addEventListener('click',
      () => showZProfileDataHub(state, 'brittle'));
    return;
  }

  if (mode === 'brittle_surface') {
    /* "Surface gradient" version of Brittle Hotspots — keeps every
     * particle at its natural base colour (AM_P near-black, AM_S grey)
     * and paints a small spherical-cap patch on each contact area of
     * the host AM particles.  The cap is a SphereGeometry section with
     * the SAME radius as the particle (so it lies exactly on the
     * surface), oriented toward the partner particle.  Per-vertex
     * colour fades from full stage colour at the cap pole (contact
     * point) to black at the cap rim, and the material uses additive
     * blending so the patch only brightens the surface — it doesn't
     * recolour the entire sphere.  Two caps per damaged contact, one
     * on each host particle. */
    ['AM_P', 'AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      const base = new THREE.Color(COL[t]);
      m.userData.particles.forEach((_, i) => m.setColorAt(i, base));
      m.material.opacity = (t === 'SE' ? OPA.SE : 1.0);
      m.material.transparent = (t === 'SE');
    });
    flushColors();

    const idx = state.idIndex || {};
    const group = new THREE.Group();
    group.userData.isBrittleGlow = true;  // share cleanup branch

    /* Build a stage-coloured spherical cap centred on `centerData`
     * (data-frame xyz), oriented so its +Y pole points along `dir`
     * (unit vector in data frame), with radius r * 1.005 so it sits
     * just outside the underlying InstancedMesh surface (no z-fight).
     * Vertex RGBA: full stage colour, alpha = t² (1 at pole → 0 at
     * rim) so the patch fades smoothly against the host particle's
     * own colour without ever brightening it.  renderOrder is tied to
     * Lawn-stage rank so where two caps overlap the more severe one
     * always wins — no additive Venn-diagram artefacts. */
    function buildCap(r, centerData, dir, stageName, halfAngleRad) {
      const segs = 28;
      const geo = new THREE.SphereGeometry(
        r * 1.005, segs, Math.max(8, segs >> 1),
        0, Math.PI * 2, 0, halfAngleRad,
      );
      const stage = new THREE.Color(STAGE_COL[stageName]);
      const yMin = Math.cos(halfAngleRad);
      const pos = geo.attributes.position;
      const colors = new Float32Array(pos.count * 4);   // RGBA
      for (let i = 0; i < pos.count; i++) {
        const y = pos.array[i * 3 + 1];                  // cap pole = +Y
        const t = Math.max(0, Math.min(1, (y - yMin) / (1 - yMin)));
        const fade = t * t;
        colors[i * 4 + 0] = stage.r;
        colors[i * 4 + 1] = stage.g;
        colors[i * 4 + 2] = stage.b;
        colors[i * 4 + 3] = fade;                        // alpha falloff
      }
      geo.setAttribute('color', new THREE.BufferAttribute(colors, 4));
      const mat = new THREE.MeshBasicMaterial({
        vertexColors: true,
        transparent: true,
        depthWrite: false,
        side: THREE.FrontSide,
      });
      const mesh = new THREE.Mesh(geo, mat);
      // Three.js Z-up swap for both position and orientation
      mesh.position.set(centerData.x, centerData.z, centerData.y);
      const dirThree = new THREE.Vector3(dir.x, dir.z, dir.y).normalize();
      mesh.quaternion.setFromUnitVectors(
        new THREE.Vector3(0, 1, 0), dirThree,
      );
      // Heavier stages get larger renderOrder → drawn last → on top.
      mesh.renderOrder = 4 + (STAGE_RANK[stageName] || 0);
      return mesh;
    }

    const HALF_ANGLE = {
      microcrack:    Math.PI / 9,    // 20°
      multicrack:    Math.PI / 6,    // 30°
      fragmentation: Math.PI / 4.5,  // 40°
      pulverization: Math.PI / 3.5,  // ~51°
    };
    const counts = { microcrack: 0, multicrack: 0, fragmentation: 0, pulverization: 0 };

    (aux.brittle_pairs || []).forEach(b => {
      const p1 = idx[b.id1], p2 = idx[b.id2];
      if (!p1 || !p2) return;
      const stage = b.stage || 'microcrack';
      if (stage === 'intact') return;
      counts[stage] = (counts[stage] || 0) + 1;

      const dx = p2.x - p1.x, dy = p2.y - p1.y, dz = p2.z - p1.z;
      const inv = 1.0 / Math.sqrt(dx*dx + dy*dy + dz*dz + 1e-12);
      const u = { x: dx*inv, y: dy*inv, z: dz*inv };
      const ha = HALF_ANGLE[stage] || HALF_ANGLE.microcrack;

      group.add(buildCap(p1.r || 1,
        { x: p1.x, y: p1.y, z: p1.z },
        u,                                       // p1 → p2
        stage, ha));
      group.add(buildCap(p2.r || 1,
        { x: p2.x, y: p2.y, z: p2.z },
        { x: -u.x, y: -u.y, z: -u.z },           // p2 → p1
        stage, ha));
    });
    if (state.scene) {
      state.scene.add(group);
      state.brittleGlowGroup = group;
    }

    setLegend(state,
      `<b>Brittle Hotspots — surface gradient patches</b>
       <span style="color:#ffeda0">●</span> microcrack (${counts.microcrack})
       <span style="color:#feb24c">●</span> multicrack (${counts.multicrack})
       <span style="color:#f03b20">●</span> fragmentation (${counts.fragmentation})
       <span style="color:#800026">●</span> pulverization (${counts.pulverization})
       <span style="color:#9ca3af;font-size:11px">
         (patch radius ∝ stage severity; gradient brightens contact spot)
       </span>
       <button id="brittle-z-modal-btn" class="data-modal-btn">
         <span class="ico">📊</span><span>Z-profile 데이터</span>
       </button>`);
    const sBtn = document.getElementById('brittle-z-modal-btn');
    if (sBtn) sBtn.addEventListener('click',
      () => showZProfileDataHub(state, 'brittle'));
    return;
  }

  if (mode === 'cluster') {
    /* AM dim (background context); SE split into two overlays so the
     * dominant percolating cluster can be colour-preserving translucent
     * (you can see through it) while the rare isolated / dead clusters
     * stay fully opaque and pop visually. */
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((_, i) => m.setColorAt(i, colDim));
      m.material.opacity = 0.08;
      m.material.transparent = true;
    });
    const cidMap = aux.cluster_id_per_se || {};
    const meta   = aux.cluster_meta      || {};

    // Hide the original SE mesh; we replace it with two overlay groups.
    const seMesh = state.meshes.SE;
    if (seMesh) seMesh.visible = false;

    // Partition SE particles by cluster status so each group gets its
    // own InstancedMesh material with the right opacity.
    const seParts  = state.seParticles || [];
    const groups   = { percolating: [], top_only: [], bottom_only: [],
                       dead: [], no_cluster: [] };
    const counts   = { percolating: 0, top_only: 0, bottom_only: 0,
                       dead: 0, no_cluster: 0 };
    for (const p of seParts) {
      const cid = cidMap[String(p.id)];
      let status;
      if (cid === undefined) status = 'no_cluster';
      else {
        const md = meta[String(cid)];
        status = (md && md.status) || 'dead';
      }
      groups[status].push(p);
      counts[status]++;
    }

    const overlay = new THREE.Group();
    overlay.userData.isClusterOverlay = true;

    function _addGroup(parts, hex, opacity) {
      if (!parts.length) return;
      const m = createInstancedSpheres(parts, 14, hex, opacity, true);
      if (!m) return;
      // Re-stamp the per-instance colour so it's not multiplied by
      // some stale base; instanceColor + white material renders the
      // hex faithfully.
      const c = new THREE.Color(hex);
      parts.forEach((_, i) => m.setColorAt(i, c));
      if (m.instanceColor) m.instanceColor.needsUpdate = true;
      m.material.depthWrite = (opacity > 0.5);
      m.renderOrder = (opacity > 0.5) ? 3 : 1;
      overlay.add(m);
    }
    // Percolating: keep blue but very translucent — context cloud
    _addGroup(groups.percolating, 0x1e40af, 0.10);
    // Isolated / no-cluster: fully opaque, distinct colours
    _addGroup(groups.dead,        0x9ca3af, 0.95);
    _addGroup(groups.top_only,    0x93c5fd, 0.95);
    _addGroup(groups.bottom_only, 0xfbbf24, 0.95);
    _addGroup(groups.no_cluster,  COL.SE_NON_REACH, 0.95);
    if (state.scene) {
      state.scene.add(overlay);
      state.clusterOverlay = overlay;
    }

    setLegend(state,
      `<b>SE Cluster Status</b>
       <span style="color:#1e40af">●</span> percolating (${counts.percolating})
         <span style="color:#9ca3af;font-size:11px">— translucent (전 부피 가로지름)</span>
       <span style="color:#93c5fd">●</span> top-only (${counts.top_only})
         <span style="color:#9ca3af;font-size:11px">— 윗판은 닿지만 바닥 끊김</span>
       <span style="color:#fbbf24">●</span> bottom-only (${counts.bottom_only})
         <span style="color:#9ca3af;font-size:11px">— 바닥은 닿지만 윗판 끊김</span>
       <span style="color:#9ca3af">●</span> dead (${counts.dead})
         <span style="color:#9ca3af;font-size:11px">— 어디에도 안 닿는 고립</span>
       <span style="color:#f87171">●</span> no cluster id (${counts.no_cluster})
         <span style="color:#9ca3af;font-size:11px">— clustering 분석에서 누락 (raw SE)</span>
       <span style="color:#e5e7eb">●</span> AM (faint background)
         <span style="color:#9ca3af;font-size:11px">— 공간감용 ghost, 클러스터 분석 대상 아님</span>`);
    return;
  }

  if (mode === 'stress') {
    /* Per-particle MAX contact pressure, coolwarm colormap on a
     * log10 scale clipped to the 5–95th percentile.  The raw
     * distribution is heavy-tailed (a handful of extreme contacts
     * can dwarf the median by 50×+), so a naïve linear normalise
     * crushes 95 % of particles into the deep-blue end and the
     * field looks featureless.  log + percentile clip keeps the
     * middle of the colormap on the actual bulk of contacts. */
    const sMap = aux.stress_max || {};
    const all  = Object.values(sMap).filter(v => v > 0);
    if (!all.length) { setLegend(state, '<i>No stress data available.</i>'); return; }
    const sorted = [...all].sort((a, b) => a - b);
    const pct = (p) => sorted[Math.max(0, Math.min(sorted.length - 1,
        Math.floor(p * (sorted.length - 1))))];
    const sLo  = Math.max(1.0, pct(0.05));
    const sHi  = Math.max(sLo * 1.5, pct(0.95));
    const sMed = pct(0.50);
    const sMax = sorted[sorted.length - 1];
    const logLo = Math.log10(sLo);
    const logHi = Math.log10(sHi);
    const norm = (s) => {
      if (!(s > 0)) return 0;
      return Math.max(0, Math.min(1,
        (Math.log10(s) - logLo) / (logHi - logLo)));
    };
    ['AM_P', 'AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        const s = sMap[String(p.id)] ?? sMap[p.id] ?? 0;
        if (s <= 0) {
          m.setColorAt(i, colDim);
        } else {
          m.setColorAt(i, new THREE.Color(coolwarmColor(norm(s))));
        }
      });
      m.material.opacity = 0.92;
      m.material.transparent = true;
    });
    flushColors();
    const stops = [0, 0.25, 0.5, 0.75, 1.0]
      .map(v => '#' + coolwarmColor(v).toString(16).padStart(6,'0'));
    setLegend(state,
      `<b>Stress Concentration (max MPa, log scale)</b>
       <div style="margin:6px 0 2px 0;height:10px;border-radius:3px;
         background:linear-gradient(90deg,${stops.join(',')})"></div>
       <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af">
         <span>${sLo.toFixed(0)}</span>
         <span>median ≈ ${sMed.toFixed(0)}</span>
         <span>${sHi.toFixed(0)}</span>
       </div>
       <button id="stress-z-modal-btn" class="data-modal-btn">
         <span class="ico">📊</span><span>Z-profile 데이터</span>
       </button>`);
    const sBtn = document.getElementById('stress-z-modal-btn');
    if (sBtn) sBtn.addEventListener('click',
      () => showZProfileDataHub(state, 'stress'));
    return;
  }

  if (mode === 'stress_brittle') {
    /* True overlay of the two existing modes:
     *   1. Every particle gets the *stress* mode whole-sphere
     *      coolwarm colour (max contact pressure on log scale,
     *      5–95th percentile clip).
     *   2. On top of that, the *brittle_surface* mode spherical-cap
     *      patches are drawn at every damaged AM-AM contact.  The
     *      caps use vertex RGBA with alpha falloff so the stress
     *      colour shows through everywhere except the contact spot
     *      where the Lawn-stage hue dominates.  No cones — exactly
     *      the two screenshots the user pointed at, superposed. */

    // ── 1) Paint stress field exactly like the 'stress' mode ────
    const sMap = aux.stress_max || {};
    const all  = Object.values(sMap).filter(v => v > 0);
    if (all.length) {
      const sorted = [...all].sort((a, b) => a - b);
      const pct = (p) => sorted[Math.max(0, Math.min(sorted.length - 1,
          Math.floor(p * (sorted.length - 1))))];
      const sLo = Math.max(1.0, pct(0.05));
      const sHi = Math.max(sLo * 1.5, pct(0.95));
      const logLo = Math.log10(sLo), logHi = Math.log10(sHi);
      const norm = (s) => !(s > 0) ? 0 :
        Math.max(0, Math.min(1, (Math.log10(s) - logLo) / (logHi - logLo)));
      ['AM_P', 'AM_S', 'SE'].forEach(t => {
        const m = state.meshes[t]; if (!m) return;
        m.userData.particles.forEach((p, i) => {
          const s = sMap[String(p.id)] ?? sMap[p.id] ?? 0;
          if (s <= 0) m.setColorAt(i, colDim);
          else m.setColorAt(i, new THREE.Color(coolwarmColor(norm(s))));
        });
        m.material.opacity = (t === 'SE' ? 0.45 : 0.85);
        m.material.transparent = true;
      });
      flushColors();
    }

    // ── 2) Drop brittle-surface cap patches on every damaged contact ─
    const idx = state.idIndex || {};
    const group = new THREE.Group();
    group.userData.isCombined = true;
    const HALF_ANGLE = {
      microcrack:    Math.PI / 9,    // 20°
      multicrack:    Math.PI / 6,    // 30°
      fragmentation: Math.PI / 4.5,  // 40°
      pulverization: Math.PI / 3.5,  // ~51°
    };
    const counts = { microcrack:0, multicrack:0, fragmentation:0, pulverization:0 };

    function makeCap(r, centerData, dir, stageName, halfAngleRad) {
      const segs = 28;
      const geo = new THREE.SphereGeometry(
        r * 1.005, segs, Math.max(8, segs >> 1),
        0, Math.PI * 2, 0, halfAngleRad,
      );
      const stageCol = new THREE.Color(STAGE_COL[stageName]);
      const yMin = Math.cos(halfAngleRad);
      const pos = geo.attributes.position;
      const colors = new Float32Array(pos.count * 4);
      for (let i = 0; i < pos.count; i++) {
        const y = pos.array[i * 3 + 1];
        const t = Math.max(0, Math.min(1, (y - yMin) / (1 - yMin)));
        const fade = t * t;
        colors[i * 4 + 0] = stageCol.r;
        colors[i * 4 + 1] = stageCol.g;
        colors[i * 4 + 2] = stageCol.b;
        colors[i * 4 + 3] = fade;
      }
      geo.setAttribute('color', new THREE.BufferAttribute(colors, 4));
      const mat = new THREE.MeshBasicMaterial({
        vertexColors: true,
        transparent: true,
        depthWrite: false,
        side: THREE.FrontSide,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(centerData.x, centerData.z, centerData.y);
      const dirThree = new THREE.Vector3(dir.x, dir.z, dir.y).normalize();
      mesh.quaternion.setFromUnitVectors(
        new THREE.Vector3(0, 1, 0), dirThree);
      mesh.renderOrder = 4 + (STAGE_RANK[stageName] || 0);
      return mesh;
    }

    (aux.brittle_pairs || []).forEach(b => {
      const p1 = idx[b.id1], p2 = idx[b.id2];
      if (!p1 || !p2) return;
      const stage = b.stage || 'microcrack';
      if (!(stage in HALF_ANGLE)) return;
      counts[stage] += 1;
      const dx = p2.x - p1.x, dy = p2.y - p1.y, dz = p2.z - p1.z;
      const inv = 1.0 / Math.sqrt(dx*dx + dy*dy + dz*dz + 1e-12);
      const u = { x: dx*inv, y: dy*inv, z: dz*inv };
      const ha = HALF_ANGLE[stage];
      group.add(makeCap(p1.r || 1,
        { x: p1.x, y: p1.y, z: p1.z }, u, stage, ha));
      group.add(makeCap(p2.r || 1,
        { x: p2.x, y: p2.y, z: p2.z },
        { x: -u.x, y: -u.y, z: -u.z }, stage, ha));
    });
    if (state.scene) {
      state.scene.add(group);
      state.combinedOverlay = group;
    }

    /* Legend — combined: stress gradient bar + brittle stage swatches */
    const stops = [0, 0.25, 0.5, 0.75, 1.0]
      .map(v => '#' + coolwarmColor(v).toString(16).padStart(6,'0'));
    setLegend(state,
      `<b>Stress field + Brittle caps</b>
       <span style="color:#9ca3af;font-size:11px">
         particles = max contact pressure (log)<br>
         surface caps = Lawn stage at damaged AM-AM contact
       </span>
       <div style="margin:6px 0 2px 0;height:8px;border-radius:3px;
         background:linear-gradient(90deg,${stops.join(',')})"></div>
       <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af">
         <span>low MPa</span><span>median</span><span>high MPa</span>
       </div>
       <span style="color:#ffeda0">●</span> microcrack (${counts.microcrack})
       <span style="color:#feb24c">●</span> multicrack (${counts.multicrack})
       <span style="color:#f03b20">●</span> fragmentation (${counts.fragmentation})
       <span style="color:#800026">●</span> pulverization (${counts.pulverization})
       <button id="combined-z-modal-btn" class="data-modal-btn">
         <span class="ico">📊</span><span>Z-profile 데이터</span>
       </button>`);
    const cBtn = document.getElementById('combined-z-modal-btn');
    if (cBtn) cBtn.addEventListener('click',
      () => showZProfileDataHub(state, 'combined'));
    return;
  }

  if (mode === 'coverage') {
    /* Per-AM coverage = SE-area / total surface area, %.  Naturally
     * bounded [0, 100] but most particles in a real case cluster
     * around the median (60-80 %), so a straight linear normalise
     * makes everything read as one shade of green and the low-
     * coverage problem particles get visually swamped.
     *
     * Improvements:
     *   1. ColorBrewer RdYlGn 5-class diverging palette instead of
     *      saturated R/Y/G primaries (academic style).
     *   2. Percentile-based clip — the 5th-percentile value maps to
     *      the deep-red endpoint, the 95th-percentile to deep-green,
     *      so the colormap range matches the actual distribution
     *      instead of always 0-100.
     *   3. Opacity scales with (1 - normalised coverage) so the
     *      low-coverage particles render bright and fully opaque
     *      while the well-covered green majority recedes to a
     *      translucent background.  Result: the "problem children"
     *      visually pop out of the rest. */
    const covMap = aux.coverage_per_am || {};
    const seMesh = state.meshes.SE;
    if (seMesh) {
      seMesh.userData.particles.forEach((_, i) => seMesh.setColorAt(i, colDim));
      seMesh.material.opacity = 0.08;
      seMesh.material.transparent = true;
    }
    const vals = [];
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p) => {
        const c = covMap[String(p.id)] ?? covMap[p.id] ?? p.coverage;
        if (c !== undefined) vals.push(c);
      });
    });
    if (!vals.length) {
      setLegend(state, state.isMPM
        ? '<i>이 payload엔 per-particle coverage가 없어요 — V100에서 payload 재생성'
          + '(최신 mpm_webapp_payload.py) 후 다시 업로드하면 색칠됩니다.</i>'
        : '<i>No coverage data — run scripts/coverage_physics_vs_hertzian.py first.</i>');
      return;
    }
    const sorted = [...vals].sort((a, b) => a - b);
    const pct = (p) => sorted[Math.max(0, Math.min(sorted.length - 1,
        Math.floor(p * (sorted.length - 1))))];
    const cLo = pct(0.05);
    const cHi = Math.max(cLo + 1, pct(0.95));
    const cMed = pct(0.50);
    const mean = vals.reduce((a,b)=>a+b, 0) / vals.length;
    const norm = (c) => Math.max(0, Math.min(1, (c - cLo) / (cHi - cLo)));

    let nMissing = 0;
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        const c = covMap[String(p.id)] ?? covMap[p.id] ?? p.coverage;
        if (c === undefined) {
          m.setColorAt(i, colDim);
          nMissing++;
          return;
        }
        m.setColorAt(i, new THREE.Color(rdylgnColor(norm(c))));
      });
      // Same material opacity for both AM types — keeps the field
      // consistent.  Low-coverage particles already pop visually via
      // the red end of the palette against the muted green majority.
      m.material.opacity = 0.95;
      m.material.transparent = true;
    });
    flushColors();

    // Inline ColorBrewer gradient bar with percentile-anchored labels
    const stops = [0, 0.25, 0.5, 0.75, 1.0]
      .map(v => '#' + rdylgnColor(v).toString(16).padStart(6,'0'));
    setLegend(state,
      `<b>AM Coverage — SE / surface area (%)</b>
       <div style="margin:6px 0 2px 0;height:10px;border-radius:3px;
         background:linear-gradient(90deg,${stops.join(',')})"></div>
       <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af">
         <span>${cLo.toFixed(0)}%</span>
         <span>median ${cMed.toFixed(0)}%</span>
         <span>${cHi.toFixed(0)}%</span>
       </div>
       <span style="color:#9ca3af;font-size:11px;line-height:1.4">
         · 빨강 = low coverage → SE 계면 부족, σ_ionic 손실 risk<br>
         · 초록 = high coverage → 이온 통로 안정<br>
         · mean ≈ ${mean.toFixed(1)} %${nMissing ? ` (no-data AM: ${nMissing})` : ''}
       </span>
       <button id="coverage-z-modal-btn" class="data-modal-btn">
         <span class="ico">📊</span><span>Z-profile 데이터</span>
       </button>`);
    const covBtn = document.getElementById('coverage-z-modal-btn');
    if (covBtn && state.isMPM) covBtn.style.display = 'none';   // Z-profile hub is DEM-only
    else if (covBtn) covBtn.addEventListener('click',
      () => showZProfileDataHub(state, 'coverage'));
    return;
  }

  if (mode === 'coverage_patches') {
    /* Spatial coverage — colour ONLY the AM-surface points the deformed SE actually
     * touches (payload am_coverage_patches), as a dot layer just outside each sphere:
     * cyan = within Hertz/contact, amber = within Tabor spread.  Bare surface stays
     * uncoloured → "partial" colouring of just the covered regions of each AM. */
    const mm = (state.data && state.data.mpm_metrics) || {};
    const pts = (state.data && state.data.am_coverage_patches) || [];
    ['AM_P', 'AM_S'].forEach(ty => {                        // reset AM so stale heat doesn't bleed
      const m = state.meshes[ty]; if (!m) return;
      const base = new THREE.Color(COL[ty]);
      m.userData.particles.forEach((p, i) => m.setColorAt(i, base));
      if (m.instanceColor) m.instanceColor.needsUpdate = true;
      m.material.opacity = 1.0; m.material.transparent = false;
    });
    if (!pts.length) {
      setLegend(state, state.isMPM
        ? '<i>이 payload엔 coverage 패치가 없어요 — 최신 mpm_webapp_payload.py로 재생성 후 업로드하면 표시됩니다.</i>'
        : '<i>No coverage-patch data in this payload.</i>');
      return;
    }
    const g = new THREE.BufferGeometry();
    const pos = new Float32Array(pts.length * 3);
    const col = new Float32Array(pts.length * 3);
    const cHi = new THREE.Color(0x22d3ee), cLo = new THREE.Color(0xf59e0b);
    let nHi = 0;
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      pos[3 * i] = p[0]; pos[3 * i + 1] = p[2]; pos[3 * i + 2] = p[1];   // Z-up swap (x,z,y)
      const isHi = p[3] >= 1.0; if (isHi) nHi++;
      const cc = isHi ? cHi : cLo;
      col[3 * i] = cc.r; col[3 * i + 1] = cc.g; col[3 * i + 2] = cc.b;
    }
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const cloud = new THREE.Points(g, new THREE.PointsMaterial({
      size: 0.5, vertexColors: true, sizeAttenuation: true, transparent: true, opacity: 0.95 }));
    state.coveragePatchGroup = cloud;
    if (state.scene) state.scene.add(cloud);
    setLegend(state,
      `<b>Coverage 패치 — AM 표면의 SE 접촉부 (partial)</b>
       <div style="margin-top:4px">
         <span style="color:#22d3ee">●</span> Hertz/contact (≤ ${mm.cov_hertz_um != null ? mm.cov_hertz_um : 0.13} µm)<br>
         <span style="color:#f59e0b">●</span> Tabor spread (≤ ${mm.cov_tabor_um != null ? mm.cov_tabor_um : 0.26} µm)
       </div>
       <span style="color:#9ca3af;font-size:11px">덮인 표면점만 색칠 · 총 ${pts.length.toLocaleString()}점 (contact ${nHi.toLocaleString()})</span>`);
    return;
  }

  if (mode === 'se_strain') {
    /* 3D SE coloured by accumulated plastic strain Σdg (payload se_strain_points) — the
     * field the 2D morphology shows, now volumetric.  Hide the SE surface mesh; show the
     * strain point cloud (hot: bright = more plastic flow, at contacts / necks). */
    const mm = (state.data && state.data.mpm_metrics) || {};
    const pts = (state.data && state.data.se_strain_points) || [];
    if (!pts.length) {
      // no strain field → DON'T blank the SE; keep the surface mesh visible (restored above by
      // the cleanup) so the user still sees the SE, and explain how to get the strain colours.
      setLegend(state, state.isMPM
        ? '<i>이 payload엔 SE strain이 없어요 — SE 표면만 표시 중. 변형 색을 보려면 mpm3d를 '
          + '<b>--save-eps</b>(또는 --save-dg)로 돌리고 payload를 <b>--eps</b>(--dg)로 재생성하세요.</i>'
        : '<i>No SE strain data in this payload — showing SE surface only.</i>');
      return;
    }
    if (state.meshes.MESH) state.meshes.MESH.visible = false;   // strain replaces the SE surface
    const vmax = (mm.dg_vmax98 && mm.dg_vmax98 > 0) ? mm.dg_vmax98 : 1.0;
    const g = new THREE.BufferGeometry();
    const pos = new Float32Array(pts.length * 3), col = new Float32Array(pts.length * 3);
    const cc = new THREE.Color();
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      pos[3 * i] = p[0]; pos[3 * i + 1] = p[2]; pos[3 * i + 2] = p[1];   // Z-up swap (x,z,y)
      hotColor(p[3] / vmax, cc);
      col[3 * i] = cc.r; col[3 * i + 1] = cc.g; col[3 * i + 2] = cc.b;
    }
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    state.strainPointGroup = new THREE.Points(g, new THREE.PointsMaterial({
      size: 0.4, vertexColors: true, sizeAttenuation: true }));
    if (state.scene) state.scene.add(state.strainPointGroup);
    const kind = mm.strain_kind || 'Σdg';
    setLegend(state,
      `<b>SE 변형 (3D) — ${kind}</b>
       <div style="margin-top:4px">밝을수록 변형 큼 (seed 구 대비). total = 탄성압축 포함(갇힌 안쪽도 보임)</div>
       <span style="color:#9ca3af;font-size:11px">vmax ${vmax} · mean ${mm.dg_mean ?? '–'} · `
       + `max ${mm.dg_max ?? '–'} · ${pts.length.toLocaleString()}점</span>`);
    return;
  }

  if (mode === 'pore') {
    /* XCT-like pore (void) view: electrode-envelope cells that are NOT AM/SE, painted as a point
     * cloud with all solid hidden — like a segmented FIB-SEM/XCT pore phase.  void_points are voxel
     * centres in µm (same frame as the SE mesh); additives (~4 vol%, sit inside the pores) not subtracted. */
    const vp = (state.data && state.data.void_points) || [];
    if (state.meshes.MESH) state.meshes.MESH.visible = false;
    ['AM_P', 'AM_S'].forEach(t => { const m = state.meshes && state.meshes[t]; if (m) m.visible = false; });
    if (!vp.length) {
      setLegend(state, state.isMPM
        ? '<i>이 payload엔 기공(void) 데이터가 없어요. payload를 <b>--void-max</b>로 재생성하세요 '
          + '(mpm_webapp_payload.py — MPM 재실행은 불필요).</i>'
        : '<i>No void (pore) data in this payload.</i>');
      return;
    }
    const g = new THREE.BufferGeometry();
    const pos = new Float32Array(vp.length * 3);
    for (let i = 0; i < vp.length; i++) {
      const p = vp[i];
      pos[3 * i] = p[0]; pos[3 * i + 1] = p[2]; pos[3 * i + 2] = p[1];   // Z-up swap (x,z,y)
    }
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    const pm = new THREE.Points(g, new THREE.PointsMaterial({
      color: 0x38bdf8, size: 0.32, sizeAttenuation: true, transparent: true, opacity: 0.9 }));
    pm.renderOrder = 5;
    state.additivePointGroup = pm;                          // reuse the cleanup hook (torn down next mode change)
    if (state.scene) state.scene.add(pm);
    const mm = (state.data && state.data.mpm_metrics) || {};
    setLegend(state,
      `<b>기공 (pore / XCT)</b>
       <div style="margin-top:4px"><span style="color:#38bdf8">●</span> void ${vp.length.toLocaleString()} voxels`
       + ` · 공극률 ${(mm.porosity_mpm_pct || 0).toFixed(1)}%</div>
       <div style="margin-top:3px;color:#9ca3af;font-size:11px">전극 envelope에서 AM·SE가 아닌 셀 = 기공망 (solid 숨김,
       XCT/FIB-SEM 분할처럼).  도전재(~4vol%, 기공 내부)는 미차감.</div>`);
    return;
  }
  if (mode === 'econn') {
    /* 전기 연결성 (한양대 slide-19 문법): AM 입자를 집전체-연결(파랑)/고립(빨강)으로 색칠.
     * payload per-particle `econn` = electronic_connectivity(mpm_webapp_payload): AM-AM 접촉 ∪
     * AM-[VGCF/SuperP/SDCP]-cluster 다리 → 집전체 percolation (SE·PTFE = e-절연 제외).
     * GEOMETRY+graph 판정 — σ 배정(STEP3 Kirchhoff) 없이 그릴 수 있는 연결성 지도.
     * 전류밀도/Li-농도 색칠(slide 20-22)은 STEP3+ 필요. */
    const mm = (state.data && state.data.mpm_metrics) || {};
    const ec = (state.data && state.data.econn_summary) || null;
    let have = false;
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      if (m.userData.particles.some(p => p.econn !== undefined)) have = true;
    });
    if (!have) {
      setLegend(state, '<i>이 payload엔 per-particle <b>econn</b>이 없어요 — 최신 '
        + '<b>mpm_webapp_payload.py</b>로 payload를 재생성해서 업로드하면 색칠됩니다.</i>');
      return;
    }
    if (state.meshes.MESH) {                                 // SE = faint context shell
      state.meshes.MESH.visible = true;
      state.meshes.MESH.material.transparent = true; state.meshes.MESH.material.opacity = 0.10;
    }
    // ── 연결 AM = 탄소-배선 강도 GRADIENT (binary→graded, user: "칙칙 → CBD 닿는 정도 그라데이션") ──
    // score = # of carbon points (VGCF 2 / SuperP 3 / SDCP 5 — PTFE 4 절연 제외) whose centre lies
    // within (r_AM + 0.3µm) of the AM surface, from the payload's subsampled additive_points via a
    // spatial hash (995 AM × ~120k pts → fast).  SUBSAMPLED counts → RELATIVE wiring only: percentile-
    // normalised p5–p95 → indigo(약) → cyan → cream(강).  Isolated stays red.  Carbon 없으면 binary 폴백.
    const carbonPts = ((state.data && state.data.additive_points) || []).filter(p => p[3] === 2 || p[3] === 3 || p[3] === 5);
    const BAND = 0.3;
    // 서브샘플 가중 보정 — additive_points는 phase별 서브샘플이라 raw count는 payload마다 밀도가
    // 다름.  metrics.additive_counts(전체 seeded)로 w=total/shown을 곱해 "환산 접점수"를 만들면
    // SBE↔DBE 케이스 간 수치·색 비교가 유효해짐 (uniform random subsample → unbiased estimate).
    const _PHN = { 2: 'VGCF', 3: 'SuperP', 5: 'SDCP' };
    const _shown = { 2: 0, 3: 0, 5: 0 };
    carbonPts.forEach(p => { _shown[p[3]]++; });
    const _acnt = mm.additive_counts || {};
    const wPh = {};
    [2, 3, 5].forEach(ph => {
      const tot = Number(((_acnt[_PHN[ph]] || {}).n_points != null ? _acnt[_PHN[ph]].n_points : _acnt[_PHN[ph]]) || 0);
      wPh[ph] = (tot > 0 && _shown[ph] > 0) ? tot / _shown[ph] : 1;
    });
    let touch = null, contactsOf = null;
    if (carbonPts.length) {
      const CELL = 3.0;
      const hash = new Map();
      const keyOf = (x, y, z) => Math.floor(x / CELL) + ',' + Math.floor(y / CELL) + ',' + Math.floor(z / CELL);
      carbonPts.forEach(p => {
        const k = keyOf(p[0], p[1], p[2]);
        let a = hash.get(k); if (!a) { a = []; hash.set(k, a); } a.push(p);
      });
      touch = new Map();                                     // particle-object → 환산 접점수
      contactsOf = new Map();                                // particle-object → 닿은 카본 점들 (패치 overlay)
      ['AM_P', 'AM_S'].forEach(t => {
        const m = state.meshes[t]; if (!m) return;
        m.userData.particles.forEach(p => {
          const rr = p.r + BAND, rr2 = rr * rr;
          let n2 = 0;
          const hits = [];
          const ci = Math.floor(p.x / CELL), cj = Math.floor(p.y / CELL), ck = Math.floor(p.z / CELL);
          const reach = Math.ceil(rr / CELL);
          for (let di = -reach; di <= reach; di++) for (let dj = -reach; dj <= reach; dj++)
            for (let dk = -reach; dk <= reach; dk++) {
              const cell = hash.get((ci + di) + ',' + (cj + dj) + ',' + (ck + dk));
              if (!cell) continue;
              for (const q of cell) {
                const dx = q[0] - p.x, dy = q[1] - p.y, dz = q[2] - p.z;
                if (dx * dx + dy * dy + dz * dz <= rr2) { n2 += (wPh[q[3]] || 1); hits.push(q); }   // 환산(가중)
              }
            }
          touch.set(p, n2);
          if (hits.length) contactsOf.set(p, hits);
        });
      });
    }
    let autoLo = 0, autoHi = 1;
    if (touch) {
      const counts = [...touch.values()].sort((a, b) => a - b);
      autoLo = counts[Math.floor(0.05 * (counts.length - 1))];
      autoHi = Math.max(counts[Math.floor(0.95 * (counts.length - 1))], autoLo + 1);
    }
    // per-payload 자동 스케일 (단일 케이스 읽기용).  케이스 간 색 비교는 여기서 하지 않음 —
    // mpm-lab의 ⚖ 비교 팝업이 두 payload의 counts를 합친 "공동 스케일"로 그려줌 (그쪽이 비교의 정답).
    const lo5 = autoLo, hi95 = autoHi;
    // 톤 = 전류밀도 FIELD와 동일 (jet + 감마 1.6: 대부분 차분한 남색, 진짜 강한 배선만 따뜻하게).
    const gamW = (t) => Math.pow(Math.max(0, Math.min(1, t)), 1.6);
    const colOn = new THREE.Color(0x3b5fd9), colOff = new THREE.Color(0xb91c1c);
    let nOn = 0, nOff = 0, nNA = 0, medTouch = 0;
    if (touch) {
      const cs = [...touch.values()].sort((a, b) => a - b);
      medTouch = cs[Math.floor(cs.length / 2)] || 0;
    }
    // AM = 비교팝업과 동일한 무광 세라믹 회색 (논문 질감 — 캡 색이 정보 전달자).  고립만 통짜 빨강.
    const PAPER_AM = { AM_P: 0xaeb4bc, AM_S: 0xc7ccd2 };
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      const base = new THREE.Color(touch ? PAPER_AM[t] : COL[t]);   // carbon 없으면 binary 폴백(본색)
      m.userData.particles.forEach((p, i) => {
        if (p.econn === undefined) { m.setColorAt(i, colDim); nNA++; }
        else if (!p.econn) { m.setColorAt(i, colOff); nOff++; }
        else { nOn++; m.setColorAt(i, touch ? base : colOn); }
      });
      m.material.opacity = 1.0; m.material.transparent = false;
    });
    flushColors();
    // 접촉 DOMAIN 캡 + glow — ⚖ 비교팝업 buildWiring과 동일 문법 (user 2026-07-14: "단독도 같은
    // 버전으로, 패치×1 고정 + glow 기본, 게이지 없음").  입자별 접점 방향을 28° greedy 클러스터링
    // → 클러스터당 곡면 캡(3-링, r+0.06µm) 하나 = 코팅 패치처럼 읽히는 매끈한 디스크.  캡 색 =
    // 그 입자의 배선 강도(감마 jet, per-payload p5-p95).  glow = depthTest-off 저불투명 2차 캡
    // (r+0.20µm) 깊이-누적 x-ray — 배선 밀도가 워시로 증폭돼 차이가 한눈에.
    if (touch && contactsOf) {
      const f = 1.0;                                         // 패치 각반경 배율 ×1 고정 (슬라이더 없음)
      const SEG = 20, MERGE = Math.cos(28 * Math.PI / 180);
      const PADR = (3 + 3 * f) * Math.PI / 180, MINR = (5 + 3 * f) * Math.PI / 180, MAXR = 0.95;
      const capList = [];
      const c2 = new THREE.Color();
      contactsOf.forEach((hits, p) => {
        if (!p.econn) return;
        const tRaw = Math.max(0, Math.min(1, ((touch.get(p) || 0) - lo5) / Math.max(hi95 - lo5, 1e-9)));
        c2.setHex(jetColor(gamW(tRaw)));
        const cls = [];                                      // 1) 단위 방향 greedy 클러스터 (28°)
        for (const q of hits) {
          let dx = q[0] - p.x, dy = q[1] - p.y, dz = q[2] - p.z;
          const L = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1;
          dx /= L; dy /= L; dz /= L;
          let best = null, bestDot = MERGE;
          for (const cl of cls) {
            const nl = Math.sqrt(cl.sx * cl.sx + cl.sy * cl.sy + cl.sz * cl.sz) || 1;
            const d = (dx * cl.sx + dy * cl.sy + dz * cl.sz) / nl;
            if (d > bestDot) { bestDot = d; best = cl; }
          }
          if (best) { best.sx += dx; best.sy += dy; best.sz += dz; best.m.push([dx, dy, dz]); }
          else cls.push({ sx: dx, sy: dy, sz: dz, m: [[dx, dy, dz]] });
        }
        for (const cl of cls) {                              // 2) 클러스터 → 캡 파라미터
          const nl = Math.sqrt(cl.sx * cl.sx + cl.sy * cl.sy + cl.sz * cl.sz) || 1;
          const nx = cl.sx / nl, ny = cl.sy / nl, nz = cl.sz / nl;
          let thMax = 0;
          for (const v of cl.m) thMax = Math.max(thMax, Math.acos(Math.max(-1, Math.min(1, v[0] * nx + v[1] * ny + v[2] * nz))));
          const th = Math.min(MAXR, Math.max(MINR, thMax + PADR));
          const ax = Math.abs(ny) < 0.9 ? [0, 1, 0] : [1, 0, 0];
          let t1x = ny * ax[2] - nz * ax[1], t1y = nz * ax[0] - nx * ax[2], t1z = nx * ax[1] - ny * ax[0];
          const t1l = Math.sqrt(t1x * t1x + t1y * t1y + t1z * t1z) || 1;
          t1x /= t1l; t1y /= t1l; t1z /= t1l;
          capList.push({ px: p.x, py: p.y, pz: p.z, r: p.r, nx, ny, nz, t1x, t1y, t1z,
                         t2x: ny * t1z - nz * t1y, t2y: nz * t1x - nx * t1z, t2z: nx * t1y - ny * t1x,
                         th, cr: c2.r, cg: c2.g, cb: c2.b });
        }
      });
      // 곡면 캡 emit — 정점을 구 반경 r+lift 위 각도 링(0/0.55θ/θ)에 놓아 표면을 감싼다.
      // winding: scene swap (x,z,y)=반사(det −1)라 역순으로 감아 바깥면이 front (컬링 버그 방지).
      const emitCaps = (lift, padE) => {
        const vtx = [], vcol = [], idx = [];
        for (const cp of capList) {
          const th = Math.min(MAXR, cp.th + padE), Rp = cp.r + lift;
          const base = vtx.length / 3;
          const pushV = (thk, ph) => {
            const rs = Rp * Math.sin(thk), hc = Rp * Math.cos(thk);
            const cph = Math.cos(ph), sph = Math.sin(ph);
            vtx.push(cp.px + cp.nx * hc + (cp.t1x * cph + cp.t2x * sph) * rs,
                     cp.pz + cp.nz * hc + (cp.t1z * cph + cp.t2z * sph) * rs,
                     cp.py + cp.ny * hc + (cp.t1y * cph + cp.t2y * sph) * rs);   // Z-up swap (x,z,y)
            vcol.push(cp.cr, cp.cg, cp.cb);
          };
          pushV(0, 0);
          for (let s = 0; s < SEG; s++) pushV(0.55 * th, 2 * Math.PI * s / SEG);
          for (let s = 0; s < SEG; s++) pushV(th, 2 * Math.PI * s / SEG);
          const r1 = base + 1, r2 = base + 1 + SEG;
          for (let s = 0; s < SEG; s++) {
            const sn = (s + 1) % SEG;
            idx.push(base, r1 + sn, r1 + s);
            idx.push(r1 + s, r2 + sn, r2 + s);
            idx.push(r1 + s, r1 + sn, r2 + sn);
          }
        }
        if (!vtx.length) return null;
        const g2 = new THREE.BufferGeometry();
        g2.setAttribute('position', new THREE.Float32BufferAttribute(vtx, 3));
        g2.setAttribute('color', new THREE.Float32BufferAttribute(vcol, 3));
        g2.setIndex(idx);
        g2.computeVertexNormals();
        return g2;
      };
      const grpP = new THREE.Group();
      const gMain = emitCaps(0.06, 0);
      if (gMain) {
        const dom = new THREE.Mesh(gMain, new THREE.MeshLambertMaterial({
          vertexColors: true, side: THREE.DoubleSide }));
        dom.renderOrder = 20; grpP.add(dom);
        const gGlow = emitCaps(0.20, 3 * Math.PI / 180);     // ✨ glow 기본 ON
        if (gGlow) {
          const gm = new THREE.Mesh(gGlow, new THREE.MeshBasicMaterial({
            vertexColors: true, transparent: true, opacity: 0.10,
            depthTest: false, depthWrite: false, side: THREE.DoubleSide }));
          gm.renderOrder = 40; grpP.add(gm);
        }
      }
      if (grpP.children.length) {
        state.additivePointGroup = grpP;                     // mode-switch cleanup 재사용
        if (state.scene) state.scene.add(grpP);
      }
    }
    const pct = (nOn + nOff) ? (100 * nOn / (nOn + nOff)) : 0;
    const nClFull = ec && ec.n_carbon_clusters != null ? Number(ec.n_carbon_clusters) : null;
    const jstops = [0, 0.25, 0.5, 0.75, 1].map(v => '#' + jetColor(v).toString(16).padStart(6, '0'));
    const wireBar = touch
      ? `<div style="margin:5px 0 2px 0;height:10px;border-radius:3px;background:linear-gradient(90deg,${jstops.join(',')})"></div>
         <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span>약함 ${Math.round(lo5)}</span><span>환산 접점/AM</span><span>강함 ${Math.round(hi95)}</span></div>
         <div style="margin-top:2px;color:#9ca3af;font-size:10.5px">중앙값 <b>${Math.round(medTouch).toLocaleString()}</b> 환산접점/AM · 도메인 캡=접점 28° 클러스터(패치×1)+✨glow 깊이누적 · ⚖ 팝업과 동일 문법(거긴 공동 스케일) · 감마톤=전류밀도와 동일</div>`
      : '';
    state.cbarSpec = touch ? { map: 'jet', gamma: 1.6,
      title: 'Carbon wiring \u2014 weighted contacts per AM (p5\u2013p95)',
      left: '\uc57d\ud568 ' + Math.round(lo5), right: '\uac15\ud568 ' + Math.round(hi95) } : null;
    setLegend(state,
      `<b>전기 연결성 — 탄소 배선 강도</b>
       <div style="margin-top:4px">연결 <b>${nOn.toLocaleString()}</b>
         &nbsp;<span style="color:#dc2626;font-size:13px">●</span> 고립 ${nOff.toLocaleString()}
         ${nNA ? `&nbsp;<span style="color:#6b7280">● n/a ${nNA}</span>` : ''}
         &nbsp;— 연결률 <b>${(ec && ec.connected_pct != null ? ec.connected_pct : pct).toFixed(1)}%</b>`
       + (nClFull != null ? ` · cluster ${nClFull.toLocaleString()}` : '') + `</div>`
       + wireBar
       + `<div style="margin-top:2px;color:#9ca3af;font-size:10.5px">AM-AM ∪ AM-carbon 다리 → 집전체 연결 (SE·PTFE 제외)</div>`);
    return;
  }
  if (mode === 'cbd') {
    /* CBD 도메인 (tomography-FEM 논문 문법): carbon + binder를 하나의 융합 반투명 상으로 —
     * VGCF/SuperP/SDCP/PTFE 전부 한 색(노랑)의 soft-disc 2겹 blob.  시각화 전용 lumping:
     * STEP3 물리는 상별 σ 유지 (PTFE=절연) — legend에 명시. */
    const fibres = ((state.data && state.data.additive_fibres) || []);
    const fibrePh = new Set(fibres.map(f => f.phase));
    const loose = ((state.data && state.data.additive_points) || []).filter(p => !fibrePh.has(p[3]));
    let nPts = loose.length; fibres.forEach(f => { nPts += f.pts.length; });
    if (!nPts) {
      setLegend(state, '<i>이 payload엔 첨가제가 없어요 (--add-recipe 런 + --phase payload 필요).</i>');
      return;
    }
    if (state.meshes.MESH) {
      state.meshes.MESH.visible = true;
      state.meshes.MESH.material.transparent = true; state.meshes.MESH.material.opacity = 0.12;
    }
    ['AM_P', 'AM_S'].forEach(ty => {                       // AM stays the grey solid subject
      const m = state.meshes[ty]; if (!m) return;
      const base = new THREE.Color(0x9a9a9a);
      m.userData.particles.forEach((p, i) => m.setColorAt(i, base));
      m.material.opacity = 1.0; m.material.transparent = false;
    });
    flushColors();
    const pos = new Float32Array(nPts * 3);
    let w = 0;
    const put = (q) => { pos[3 * w] = q[0]; pos[3 * w + 1] = q[2]; pos[3 * w + 2] = q[1]; w++; };
    fibres.forEach(f => f.pts.forEach(put));
    loose.forEach(p => put(p));
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    const grp = new THREE.Group();
    const cbdCol = new THREE.Color(0xd9c400);              // CBD yellow (논문 문법)
    for (const [sz, op] of [[1.6, 0.20], [0.7, 0.6]]) {
      const pm = new THREE.Points(g, new THREE.PointsMaterial({
        size: sz, color: cbdCol, sizeAttenuation: true, depthTest: false, depthWrite: false,
        map: roundDotTex(), transparent: true, opacity: op, alphaTest: 0.05 }));
      pm.renderOrder = 999; grp.add(pm);
    }
    state.additivePointGroup = grp;
    if (state.scene) state.scene.add(grp);
    const ac = ((state.data && state.data.mpm_metrics) || {}).additive_counts || {};
    setLegend(state,
      `<b>CBD 도메인</b> <span style="color:#d9c400;font-size:13px">●</span>
       carbon+binder 통합상 (${Object.entries(ac).map(([k, v]) => `${k} ${Number(v).toLocaleString()}`).join(' · ') || '—'})
       <div style="margin-top:2px;color:#9ca3af;font-size:11px">시각화 lumping — STEP3 σ 물리는 상별 유지 (PTFE=절연)</div>`);
    return;
  }
  if (mode === 'je_field' || mode === 'ji_field') {
    /* STEP3 current-density FIELD (paper Fig-2/Fig-4 grammar): a per-voxel |J| point cloud of the
     * CONDUCTING phase — electronic (AM+carbon) or ionic (SE+SDCP) — coloured jet + gamma-compressed
     * so only the true conduction backbone leaves the deep-blue field.  The OPPOSITE (blocking) phase
     * is a faint dark ghost for context.  Same p99.8/gamma normalisation as the je AM-sphere map. */
    const ionic = mode === 'ji_field';
    const fld = (state.data && state.data[ionic ? 'ionic_field' : 'electronic_field']) || [];
    const mm = (state.data && state.data.mpm_metrics) || {};
    const s3 = mm.step3 || (state.data && state.data.step3) || null;
    if (!fld.length) {
      setLegend(state, '<i>이 payload엔 ' + (ionic ? '이온' : '전자') + ' 전류밀도 FIELD가 없어요 — 최신 '
        + '<b>mpm_webapp_payload.py</b>(--field 기본 ON)로 payload를 재생성해 업로드하세요 '
        + '(MPM 재실행 불필요).</i>');
      return;
    }
    // AM spheres = dark translucent GHOST in BOTH field modes (user: "전자에도 AM 넣어줘") —
    // gives the particle-scale spatial context while the cloud carries the |J| colours.  In the
    // electronic mode the AM interior is also in the cloud, but it sits ~0% of the current (deep
    // navy dots), so the ghost outline reads better than the dots did.  Layer checkboxes still work.
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      const base = new THREE.Color(0x0a0e1a);
      m.userData.particles.forEach((p, i) => m.setColorAt(i, base));
      if (m.instanceColor) m.instanceColor.needsUpdate = true;
      // ghost RESPECTS the layer checkbox — the backbone slider rebuilds this mode, and forcing
      // visible=true resurrected AM the user had unchecked (bug report).
      const cb = document.querySelector(`.viewer-controls input[data-layer="${t}"]`);
      m.visible = cb ? cb.checked : true;
      m.material.transparent = true; m.material.opacity = ionic ? 0.13 : 0.12;
    });
    if (state.meshes.MESH) {
      if (ionic) { state.meshes.MESH.visible = false; }     // ionic: SE is IN the cloud → hide mesh
      else {                                                // electronic: SE = insulator ghost (checkbox 존중)
        const mcb = document.querySelector('.viewer-controls input[data-layer="MESH"]');
        state.meshes.MESH.visible = mcb ? mcb.checked : true;
        state.meshes.MESH.material.transparent = true; state.meshes.MESH.material.opacity = 0.09;
      }
    }
    const jv = fld.map(p => p[3]);
    const sorted = [...jv].sort((a, b) => a - b);
    const hi = Math.max(sorted[Math.floor(0.998 * (sorted.length - 1))], 1e-9);
    const gam = (t) => Math.pow(Math.max(0, Math.min(1, t / hi)), 1.6);
    const g = new THREE.BufferGeometry();
    const pos = new Float32Array(fld.length * 3), col = new Float32Array(fld.length * 3);
    const c = new THREE.Color();
    for (let i = 0; i < fld.length; i++) {
      const p = fld[i];
      pos[3 * i] = p[0]; pos[3 * i + 1] = p[2]; pos[3 * i + 2] = p[1];   // Z-up swap (x,z,y)
      c.setHex(jetColor(gam(p[3])));
      col[3 * i] = c.r; col[3 * i + 1] = c.g; col[3 * i + 2] = c.b;
    }
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const grp = new THREE.Group();
    // background cloud — deliberately MORE transparent (user: "voxelization 약간 투명화") so the
    // backbone reads on top; still shows the full conducting phase as context.
    for (const [sz, op] of [[0.9, 0.10], [0.42, 0.55]]) {    // soft halo + light core
      const pm = new THREE.Points(g, new THREE.PointsMaterial({
        size: sz, vertexColors: true, sizeAttenuation: true, map: roundDotTex(),
        transparent: true, opacity: op, alphaTest: 0.02, depthWrite: false }));
      pm.renderOrder = 900; grp.add(pm);
    }
    // ── 백본 (전류 고속도로) — percolation-style skeleton ──────────────────────
    // hot set = the voxels carrying the top 80% of Σ|J| (heavy-tailed → few); rendered as a
    // CBD-grammar FUSED bulk (big soft sprites merge contiguous voxels into strands) + explicit
    // lattice-adjacency LINES (6-neighbour on the vox grid) = the connected conduction network.
    const vox3 = (s3 && s3.vox_um) || 0.4;
    const bbPct = state._fieldBackbonePct || 80;             // target: 백본이 나를 전류 분율 (slider)
    const orderIdx = Array.from({ length: fld.length }, (_, i) => i).sort((a, b) => jv[b] - jv[a]);
    const jTot = jv.reduce((a, b) => a + b, 0) || 1;
    let acc = 0, nHot = 0;
    while (nHot < orderIdx.length && nHot < 30000 && acc < (bbPct / 100) * jTot) { acc += jv[orderIdx[nHot]]; nHot++; }
    const bbShare = Math.round(100 * acc / jTot);            // ACTUAL share carried (cap-honest: ionic
    const hotIdx = orderIdx.slice(0, nHot);                  //   diffuse fields hit the 30k cap below target)
    const hPos = new Float32Array(nHot * 3), hCol = new Float32Array(nHot * 3);
    const cellOf = (p) => Math.round(p[0] / vox3 - 0.5) + ',' + Math.round(p[1] / vox3 - 0.5) + ','
                        + Math.round(p[2] / vox3 - 0.5);
    const hotMap = new Map();
    hotIdx.forEach((fi, k) => {
      const p = fld[fi];
      hPos[3 * k] = p[0]; hPos[3 * k + 1] = p[2]; hPos[3 * k + 2] = p[1];
      c.setHex(jetColor(gam(p[3])));
      hCol[3 * k] = c.r; hCol[3 * k + 1] = c.g; hCol[3 * k + 2] = c.b;
      hotMap.set(cellOf(p), k);
    });
    const hg = new THREE.BufferGeometry();
    hg.setAttribute('position', new THREE.BufferAttribute(hPos, 3));
    hg.setAttribute('color', new THREE.BufferAttribute(hCol, 3));
    const backboneGrp = new THREE.Group();
    // fused-bulk look (CBD 문법) — ADAPTIVE size: sparse backbone (electronic web) gets fat strands;
    // a diffuse field (ionic through bulk SE) gets slimmer sprites so it doesn't mush into cauliflower.
    const bbSizes = nHot <= 12000 ? [[1.7, 0.30], [0.85, 0.95]] : [[1.05, 0.20], [0.55, 0.92]];
    for (const [sz, op] of bbSizes) {
      const pm = new THREE.Points(hg, new THREE.PointsMaterial({
        size: sz, vertexColors: true, sizeAttenuation: true, map: roundDotTex(),
        transparent: true, opacity: op, alphaTest: 0.03, depthWrite: false }));
      pm.renderOrder = 950; backboneGrp.add(pm);
    }
    {                                                        // lattice-adjacency edges (percolation skeleton)
      const ePos = [], eCol = [];
      hotIdx.forEach((fi, k) => {
        const p = fld[fi];
        const ci = Math.round(p[0] / vox3 - 0.5), cj = Math.round(p[1] / vox3 - 0.5),
              ck = Math.round(p[2] / vox3 - 0.5);
        for (const [di, dj, dk] of [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) {   // +dir only → no duplicates
          const nb = hotMap.get((ci + di) + ',' + (cj + dj) + ',' + (ck + dk));
          if (nb === undefined) continue;
          ePos.push(hPos[3 * k], hPos[3 * k + 1], hPos[3 * k + 2],
                    hPos[3 * nb], hPos[3 * nb + 1], hPos[3 * nb + 2]);
          eCol.push(hCol[3 * k], hCol[3 * k + 1], hCol[3 * k + 2],
                    hCol[3 * nb], hCol[3 * nb + 1], hCol[3 * nb + 2]);
        }
      });
      if (ePos.length) {
        const eg = new THREE.BufferGeometry();
        eg.setAttribute('position', new THREE.Float32BufferAttribute(ePos, 3));
        eg.setAttribute('color', new THREE.Float32BufferAttribute(eCol, 3));
        const lm = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({
          vertexColors: true, transparent: true, opacity: 0.9, depthWrite: false }));
        lm.renderOrder = 940; backboneGrp.add(lm);
      }
    }
    backboneGrp.visible = state._fieldBackboneOn !== false;  // default ON, remembered across modes
    grp.add(backboneGrp);
    state.additivePointGroup = grp;                          // reuse the mode-switch cleanup hook
    if (state.scene) state.scene.add(grp);
    if (state.applyClip) state.applyClip();                  // 단면 뷰를 새 point 재질에도 적용
    const stops = [0, 0.25, 0.5, 0.75, 1].map(v => '#' + jetColor(v).toString(16).padStart(6, '0'));
    const sigTxt = ionic
      ? (s3 && s3.sigma_ion_eff_S_cm != null ? 'σ_ion_eff ' + Number(s3.sigma_ion_eff_S_cm).toExponential(2) + ' S/cm' : '')
      : (s3 && s3.sigma_e_eff_S_cm != null ? 'σ_e_eff ' + Number(s3.sigma_e_eff_S_cm).toExponential(2) + ' S/cm' : '');
    const share = ionic ? (s3 && s3.ion_dissipation_share) : (s3 && s3.dissipation_share);
    // 정량 스케일 (payload field_scale_*): focus_top = 컬러바 상단(p99.8)의 |J|/⟨J_z⟩ 배율
    // (바이어스 무관), j_top = A/cm² @ΔV=1V.  구 payload엔 없음 → 기존 상대 라벨 폴백.
    const fsc = ionic ? (s3 && s3.field_scale_ion) : (s3 && s3.field_scale_e);
    const fmtP = v => { const x = Number(v); return x >= 100 ? x.toPrecision(3) : x.toPrecision(2); };
    setLegend(state,
      `<b>${ionic ? '이온 (Li⁺)' : '전자 (e⁻)'} 전류밀도 FIELD (STEP3 · ${ionic ? 'SE+SDCP' : 'AM+carbon'})</b>`
      + (sigTxt ? `<div style="margin-top:3px"><b style="font-size:13px">${sigTxt}</b></div>` : '')
      + `<div style="margin:5px 0 2px 0;height:10px;border-radius:3px;background:linear-gradient(90deg,${stops.join(',')})"></div>`
      + (fsc
         ? `<div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span>0</span><span>|J| / ⟨J_z⟩</span><span>×${fmtP(fsc.focus_top)}</span></div>`
           + `<div style="font-size:9.5px;color:#6b7280;margin-top:1px;line-height:1.35">상단(p99.8) = ${fmtP(fsc.j_top_A_cm2_per_V)} A/cm² @ΔV=1V · ⟨J_z⟩ = ${fmtP(fsc.j_mean_z_A_cm2_per_V)} A/cm²/V</div>`
           + (fsc.j_1C_mA_cm2
              ? `<div style="margin-top:5px;padding:6px 8px;background:#0d1117;border:1px solid #2a2d3e;border-radius:6px">
                   <div style="font-size:11.5px;color:#9ca3af">운전 환산&nbsp; <input id="fld-crate" type="number" value="1" min="0.05" step="0.05" style="width:46px;font-size:12px;background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:4px;padding:1px 4px"> C</div>
                   <div style="font-size:12.5px;color:#e5e7eb;margin-top:3px">⟨J⟩ <b><span id="fld-jmean-abs"></span></b> · 피크 <b><span id="fld-jtop-abs"></span></b> mA/cm²</div>
                   <div style="font-size:10px;color:#6b7280;margin-top:2px">면적용량 ${fmtP(fsc.areal_capacity_mAh_cm2)} mAh/cm² 자동산출 · 피크 = p99.8 지점</div>
                 </div>`
              : `<div style="font-size:9.5px;color:#6b7280">운전 국소값 = (|J|/⟨J⟩) × 면적전류밀도(mA/cm²)</div>`)
         : `<div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span>0</span><span>|J| (0–p99.8)</span><span>high</span></div>`)
      + `<label style="display:block;margin-top:5px;font-size:11.5px;color:#e5e7eb;cursor:pointer">
           <input type="checkbox" id="fld-backbone" ${backboneGrp.visible ? 'checked' : ''}>
           🔥 백본 <b>${nHot.toLocaleString()}</b>복셀 = 전류 <b>${bbShare}%</b>
           <span id="fld-bb-pct-lab" style="color:#9ca3af;font-size:10.5px">(목표 ${bbPct}%)</span></label>`
      + `<input type="range" id="fld-bb-pct" min="30" max="95" step="5" value="${bbPct}" style="accent-color:#f97316;height:12px">`
      + `<div style="margin-top:3px;color:#9ca3af;font-size:10.5px">${Math.round(fld.length / 1000)}k점(반투명 배경) · ${ionic ? 'AM' : 'AM·SE'} 고스트(체크박스로 on/off) · 단면뷰·6×촬영</div>`
      + (share ? `<div style="margin-top:2px;color:#9ca3af;font-size:10.5px">손실분담 `
          + Object.entries(share).filter(([, v]) => v >= 0.001).map(([k, v]) => `${k} ${(100 * v).toFixed(0)}%`).join(' · ') + `</div>` : '')
      + `<div style="margin-top:6px;padding:6px 7px;background:#0d1117;border:1px solid #2a2d3e;border-radius:6px">
           <div style="display:flex;justify-content:space-between;align-items:center">
             <b style="font-size:11.5px;color:#cbd5e1">두께방향 프로파일 (Fig 4e)</b>
             <button id="fld-prof-dl" title="이 프로파일을 PNG(3×)+CSV로 저장" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:1px 7px;cursor:pointer;font-size:12px">📈</button>
           </div>
           <canvas id="fld-prof" width="220" height="120" style="width:100%;margin-top:4px;border-radius:4px"></canvas>
           <div id="fld-prof-cap" style="font-size:10px;color:#6b7280;margin-top:2px"></div>
         </div>`);
    // ── 두께방향 프로파일 (Oh2025 Fig4e): φ(z) [신형 payload] 우선, 없으면 ⟨|J|⟩(z) 폴백 ──
    (() => {
      const cv = document.getElementById('fld-prof'), cap = document.getElementById('fld-prof-cap');
      if (!cv) return;
      const pp = s3 && s3.phi_profile;
      const netKey = ionic ? 'ionic' : 'electronic';
      let rows = [], curves = [], yLab = '', capTxt = '', hdr = '';
      if (pp && pp[netKey] && pp[netKey].z_um) {              // 정확한 φ(z) = Fig4e
        const L = Math.max(...pp[netKey].z_um);
        curves.push({ zs: pp[netKey].z_um, ys: pp[netKey].phi, color: ionic ? '#a78bfa' : '#f87171', dash: false });
        const bz = (!ionic && pp.electronic_bare && pp.electronic_bare.z_um) ? pp.electronic_bare : null;
        if (bz) curves.push({ zs: bz.z_um, ys: bz.phi, color: '#f87171', dash: true });
        yLab = 'φ (V @ΔV=1V)';
        capTxt = `φ(z) @ΔV=1V — Oh2025 Fig4e 대응${ionic ? '' : ' · 실선 정본 / 점선 bare 집전체(계면 강하)'}`;
        hdr = 'z_um,z_over_L,phi_V,phi_bare_V';
        rows = pp[netKey].z_um.map((z, i) => [z.toFixed(2), (z / L).toFixed(4),
          pp[netKey].phi[i], bz ? bz.phi[i] : '']);
      } else if (fld.length) {                               // 폴백: 필드 클라우드 ⟨|J|⟩(z)
        const NB = 24, sum = new Float64Array(NB), cnt = new Int32Array(NB);
        let zmx = 1e-9; for (const p of fld) if (p[2] > zmx) zmx = p[2];
        for (const p of fld) { const b = Math.max(0, Math.min(NB - 1, Math.floor(p[2] / zmx * NB))); sum[b] += p[3]; cnt[b]++; }
        const zs = [], ys = [];
        for (let b = 0; b < NB; b++) if (cnt[b]) { zs.push((b + 0.5) / NB * zmx); ys.push(sum[b] / cnt[b]); }
        curves.push({ zs, ys, color: ionic ? '#a78bfa' : '#f87171', dash: false });
        yLab = '⟨|J|⟩(z) 상대';
        capTxt = '⟨|J|⟩(z) 상대 (필드 클라우드 서브샘플 — 노이즈 있음) · 정확한 매끈한 φ(z) Fig4e는 <b>payload 재생성</b> 후';
        hdr = 'z_um,z_over_L,jmag_rel';
        rows = zs.map((z, i) => [z.toFixed(2), (z / zmx).toFixed(4), ys[i].toFixed(5)]);
      } else { cap.textContent = '프로파일 데이터 없음'; return; }
      drawZProfileCanvas(cv, curves, yLab);                  // 인라인 미리보기
      cap.innerHTML = capTxt;
      state._fldProf = { rows, header: hdr, curves, yLab };  // 고해상 export용 원자료 보존
    })();
    const pfBtn = document.getElementById('fld-prof-dl');
    if (pfBtn) pfBtn.onclick = () => {
      const pr = state._fldProf;
      if (!pr) return;
      const big = document.createElement('canvas'); big.width = 1200; big.height = 660;   // 고해상 재그리기
      drawZProfileCanvas(big, pr.curves, pr.yLab);
      // 케이스별 유니크 파일명 (안 그러면 elec_zprofile / _1 로 뭉개짐).  ★레시피(additive_counts)를
      // 우선 — payload에 내재적이라 SBE(VGCF-PTFE)↔DBE(VGCF-PTFE-SDCP)가 항상 다름.  collector selected는
      // 두 payload에서 같은 기본값(SBE)일 수 있어 구분 불가 → SBE/DBE 토큰만 가독성용으로 덧붙임.
      const _d = state.data || {}, _s3d = ((_d.mpm_metrics || {}).step3) || {};
      const _rec = Object.keys((_d.mpm_metrics || {}).additive_counts || {}).join('-');
      const _sel = (((_s3d.collector || {}).selected) || {}).name || '';
      const _tok = (_sel.match(/SBE|DBE/i) || [''])[0].toUpperCase();
      const _dist = [_rec, _tok].filter(Boolean).join('_');
      const _slug = String([_d.case || '', _dist].filter(Boolean).join('_'))
        .replace(/[^\w.-]+/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '').slice(0, 70);
      const tag = (ionic ? 'ion' : 'elec') + '_zprofile' + (_slug ? '_' + _slug : '');
      const a1 = document.createElement('a'); a1.href = big.toDataURL('image/png'); a1.download = tag + '.png';
      document.body.appendChild(a1); a1.click(); a1.remove();
      const csv = pr.header + '\n' + pr.rows.map(r => r.join(',')).join('\n');
      const a2 = document.createElement('a'); a2.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
      a2.download = tag + '.csv'; document.body.appendChild(a2); a2.click(); a2.remove();
      setTimeout(() => URL.revokeObjectURL(a2.href), 5000);
    };
    const bbCb = document.getElementById('fld-backbone');
    if (bbCb) bbCb.onchange = () => { state._fieldBackboneOn = bbCb.checked; backboneGrp.visible = bbCb.checked; };
    const bbSl = document.getElementById('fld-bb-pct'), bbLab = document.getElementById('fld-bb-pct-lab');
    if (bbSl) {
      bbSl.oninput = () => { if (bbLab) bbLab.textContent = '(목표 ' + bbSl.value + '%)'; };
      bbSl.onchange = () => { state._fieldBackbonePct = +bbSl.value; applyViewMode(state, mode); };  // rebuild
    }
    const crIn = document.getElementById('fld-crate');       // mA/cm² 절대 라벨 (C-rate 입력 연동)
    if (crIn && fsc && fsc.j_1C_mA_cm2) {
      const updAbs = () => {
        const c = Math.max(parseFloat(crIn.value) || 1, 0.001);
        const jm = fsc.j_1C_mA_cm2 * c;
        const e1 = document.getElementById('fld-jmean-abs'), e2 = document.getElementById('fld-jtop-abs');
        if (e1) e1.textContent = jm.toPrecision(3);
        if (e2) e2.textContent = (jm * fsc.focus_top).toPrecision(3);
      };
      crIn.oninput = updAbs; updAbs();
    }
    // 컬러바 PNG 버튼용 정량 스펙 (수치 눈금 + 단위 부제) — 구 payload는 상대 라벨 폴백
    state.cbarSpec = fsc
      ? { map: 'jet', gamma: 1.6,
          title: (ionic ? '|J_ion|' : '|J_e|') + ' / ⟨J_z⟩ current-focusing (p99.8-normalized)',
          ticks: _focusTicks(fsc),
          sub: 'top(p99.8) = ' + fmtP(fsc.j_top_A_cm2_per_V) + ' A/cm² @ΔV=1V'
             + (fsc.j_1C_mA_cm2 ? ' · @1C: ⟨J⟩ ' + fmtP(fsc.j_1C_mA_cm2) + ' · top '
                + fmtP(fsc.j_1C_mA_cm2 * fsc.focus_top) + ' mA/cm²' : '') }
      : { map: 'jet', gamma: 1.6,
          title: (ionic ? '|J_ion|' : '|J_e|') + ' relative current density (p99.8-normalized)',
          left: '0', right: 'high' };
    state.cbarSpecMode = mode;
    return;
  }
  if (mode === 'jrxn') {
    /* STEP4-v1 반응 전류밀도 (랩 slide-20 물리판): 전자망(집전체)×이온망(분리막)을 AM|SE·AM|SDCP
     * 접촉면의 선형화 BV로 결합해 푼 입자별 반응전류 i/ī.  색 = 그 입자가 충전 반응을 얼마나
     * 담당하나 (상대값 — linear라 C-rate 무관).  navy ≈ 반응 소외(접근성 나쁨) / red = 핫스팟. */
    const mm = (state.data && state.data.mpm_metrics) || {};
    const s3 = mm.step3 || null;
    const rxn = s3 && s3.rxn;
    const vals = [];
    ['AM_P', 'AM_S'].forEach(ty => {
      const m = state.meshes[ty]; if (!m) return;
      m.userData.particles.forEach(p => { if (p.jrxn !== undefined) vals.push(p.jrxn); });
    });
    if (!vals.length) {
      setLegend(state, '<i>이 payload엔 STEP4 반응전류(<b>jrxn</b>)가 없어요 — 최신 '
        + '<b>mpm_webapp_payload.py</b>(--step4 기본 ON)로 payload를 재생성해 업로드하세요 '
        + '(MPM 재실행 불필요).</i>');
      return;
    }
    if (state.meshes.MESH) {                                 // SE = 얇은 이온-공급 맥락
      state.meshes.MESH.visible = true;
      state.meshes.MESH.material.transparent = true; state.meshes.MESH.material.opacity = 0.10;
    }
    const sorted = [...vals].sort((x, y) => x - y);
    const hi = Math.max(sorted[Math.floor(0.998 * (sorted.length - 1))], 1e-9);
    const gam = (t) => Math.pow(Math.max(0, Math.min(1, t / hi)), 1.6);
    ['AM_P', 'AM_S'].forEach(ty => {
      const m = state.meshes[ty]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        if (p.jrxn === undefined) { m.setColorAt(i, colDim); return; }
        m.setColorAt(i, new THREE.Color(jetColor(gam(p.jrxn))));
      });
      m.material.opacity = 1.0; m.material.transparent = false;
    });
    flushColors();
    const stops = [0, 0.25, 0.5, 0.75, 1].map(v => '#' + jetColor(v).toString(16).padStart(6, '0'));
    setLegend(state,
      `<b>🔋 반응 전류밀도 (STEP4 · 저율 충전)</b>
       <div style="margin-top:2px;color:#9ca3af;font-size:10.5px">전자망×이온망을 AM|SE·SDCP 접촉면 BV로 결합 — 입자별 충전 반응 분담 (i/ī 상대)</div>
       <div style="margin:5px 0 2px 0;height:10px;border-radius:3px;background:linear-gradient(90deg,${stops.join(',')})"></div>
       <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span>0 (반응 소외)</span><span>i/ī (0–p99.8)</span><span>핫스팟</span></div>`
      + (rxn ? `<div style="margin-top:3px;color:#9ca3af;font-size:10.5px">BV faces ${Number(rxn.n_bv_faces).toLocaleString()} · active AM ${rxn.active_am_pct}% · i0 ${rxn.i0_A_m2} A/m² (⚠F1 hook) · 선형화 BV·균일 SOC</div>` : ''));
    return;
  }
  if (mode === 'st4_soc' || mode === 'st4_face') {
    if (state.isSeed) {
      setLegend(state, '<i>STEP4-v2는 <b>압축 후</b> 구조 위의 동역학이에요 — "MPM (압축 후)" 뷰에서 보세요.</i>');
      return;
    }
    const m2 = (state.dataUrl || '').match(/\/mpm-lab\/data\/([^/?#]+)/);
    const st4Url = m2 ? '/mpm-lab/st4/' + m2[1] : null;
    state._st4Url = st4Url;                                   // 렌더 legend의 '교체' 버튼이 사용
    if (!state.st4) {
      // lab 엔트리면 서버 자동 로드 1회 시도 → 없으면 피커; 피커로 연 파일은 서버에
      // 자동 저장돼 다음부터 무선택 로드 (경로: /mpm-lab/st4/<pid>)
      if (st4Url && !state._st4AutoTried) {
        state._st4AutoTried = true;
        setLegend(state, '<i>서버에 저장된 STEP4 결과 확인 중…</i>');
        fetch(st4Url).then(r => (r.ok ? r.json() : null)).catch(() => null).then(obj => {
          if (obj && obj.kind === 'step4_viz') { state.st4 = obj; state._st4SrcName = null; }   // 서버 자동로드 = payload 케이스 사용
          applyViewMode(state, mode);
        });
        return;
      }
      setLegend(state,
        `<b>STEP4-v2 동역학 결과 열기</b>
         <div style="margin-top:4px"><button id="st4-open" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:3px 8px;cursor:pointer">📂 step4_viz.json 선택</button></div>
         <div style="margin-top:4px;color:#9ca3af;font-size:10.5px">GPU 런에서 <code>step4_dyn.py … --viz-out step4_viz.json</code>으로 생성한 파일을 선택하세요
         (입자별 코어-셸 SOC 체크포인트 + BV 면별 반응전류).  같은 케이스의 침대여야 입자 id가 맞습니다.${st4Url ? '<br><b>한 번 열면 이 케이스에 저장되어 다음부터 자동으로 열립니다.</b>' : ''}</div>`);
      const btn = document.getElementById('st4-open');
      // file input을 동적 생성 (템플릿에 #st4-file 없는 뷰어=mpm-lab에서도 작동 — 이게 '안 뜨던' 원인)
      let inp = document.getElementById('st4-file');
      if (!inp) {
        inp = document.createElement('input');
        inp.type = 'file'; inp.accept = '.json,application/json'; inp.style.display = 'none';
        document.body.appendChild(inp);
      }
      if (btn) {
        btn.onclick = () => inp.click();
        inp.onchange = (e) => {
          const f = e.target.files && e.target.files[0];
          if (!f) return;
          const rd = new FileReader();
          rd.onload = () => {
            let obj;
            try { obj = JSON.parse(rd.result); } catch (err) { alert('step4_viz JSON 파싱 실패: ' + err); return; }
            if (!obj || obj.kind !== 'step4_viz') { alert('step4_viz 형식이 아니에요 (kind=' + (obj && obj.kind) + ')'); return; }
            state.st4 = obj;
            state._st4SrcName = (f.name || '').replace(/\.json$/i, '');   // 처음 연 파일명 = 다운로드 이름의 정체
            if (st4Url) fetch(st4Url, { method: 'POST',      // 다음부터 자동 로드 (fire-and-forget)
              headers: { 'Content-Type': 'application/json' }, body: rd.result })
              .then(r => { if (r && r.ok) console.log('st4 viz 서버 저장됨 → 다음부터 자동 로드'); }).catch(() => {});
            inp.value = '';
            applyViewMode(state, mode);
          };
          rd.onerror = () => alert('step4_viz 파일 읽기 실패');
          rd.readAsText(f);
        };
      }
      return;
    }
    if (mode === 'st4_soc') renderSt4Soc(state);
    else renderSt4Faces(state);
    if (state.applyClip) state.applyClip();                  // 단면 뷰를 새 레이어에도 적용
    return;
  }
  if (mode === 'je_delta') {
    /* Δ 재분배 — 같은 전극을 wetted(je)/bare(jb) 집전체로 푼 두 해의 입자별 비율 log₂(jb/je).
     * 두 솔브의 유일한 차이 = 바닥 접점 집합(4,680→3,741)이므로 색이 갈리는 곳은 집전체 근처뿐이어야
     * 정상 — R_geom의 국소 시각화(primer-paper Fig4d red-box).  파랑 = bare에서 냉각(접점 상실),
     * 빨강 = 가열(남은 접점으로 전류 집중), 흰색 = 변화 없음.  (je/je_bare 두 모드를 한 화면으로 통합.) */
    const mm = (state.data && state.data.mpm_metrics) || {};
    const s3 = mm.step3 || null;
    let have = false;
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      if (m.userData.particles.some(p => p.je !== undefined && p.jb !== undefined)) have = true;
    });
    if (!have) {
      setLegend(state, '<i>이 payload엔 je/jb 쌍이 없어요 — 최신 <b>mpm_webapp_payload.py</b>로 재생성해 업로드하세요.</i>');
      return;
    }
    const allJe = [];
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (m) m.userData.particles.forEach(p => { if (isFinite(p.je)) allJe.push(p.je); });
    });
    allJe.sort((a, b) => a - b);
    const eps = Math.max(1e-30, (allJe[Math.floor(allJe.length / 2)] || 1e-6) * 1e-3);   // 0-값 보호
    const absR = [];
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach(p => {
        if (p.je === undefined || p.jb === undefined) { p._dlt = undefined; return; }
        p._dlt = Math.log2((p.jb + eps) / (p.je + eps));
        absR.push(Math.abs(p._dlt));
      });
    });
    absR.sort((a, b) => a - b);
    const R = Math.min(3, Math.max(0.5, absR[Math.floor(0.99 * (absR.length - 1))] || 1));   // 대칭 범위 (p99)
    let nCool = 0, nHot = 0;
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        if (p._dlt === undefined) { m.setColorAt(i, colDim); return; }
        if (p._dlt <= -0.322) nCool++; else if (p._dlt >= 0.263) nHot++;   // ×0.8 미만 / ×1.2 초과
        m.setColorAt(i, new THREE.Color(coolwarmColor(0.5 + 0.5 * Math.max(-1, Math.min(1, p._dlt / R)))));
      });
      m.material.opacity = 1.0; m.material.transparent = false;
    });
    flushColors();
    if (state.meshes.MESH) {                                 // SE = 얇은 맥락 (바닥 신호를 가리지 않게)
      state.meshes.MESH.visible = true;
      state.meshes.MESH.material.transparent = true; state.meshes.MESH.material.opacity = 0.08;
    }
    const cg = s3 && s3.collector_geometric;
    setLegend(state,
      `<b>Δ 재분배 — bare/wetted (log₂ jb/je)</b>
       <div style="margin:5px 0 2px 0;height:10px;border-radius:3px;background:linear-gradient(90deg,#3b4cc0,#dddddd,#b40426)"></div>
       <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span>×${Math.pow(2, -R).toFixed(2)} 냉각</span><span>변화 없음</span><span>×${Math.pow(2, R).toFixed(1)} 가열</span></div>
       <div style="margin-top:3px;font-size:11.5px">냉각(&lt;×0.8) <b>${nCool}</b>개 · 가열(&gt;×1.2) <b>${nHot}</b>개</div>`
      + (cg ? `<div style="margin-top:2px;color:#9ca3af;font-size:10.5px">바닥 접점 wetted ${cg.n_bottom_contacts.wetted} → bare ${cg.n_bottom_contacts.bare} · R_geom ${Number(cg.R_geom_ohm_cm2).toExponential(2)} Ω·cm²</div>` : '')
      + `<div style="margin-top:2px;color:#9ca3af;font-size:10.5px">색 갈림은 집전체 근처에만 — 접점 상실의 국소 재분배 (그 외는 흰색이 정상)</div>`);
    return;
  }
  if (mode === 'je') {
    /* STEP3 per-AM current density (slide-20 문법): AM coloured by mean |J_z| from the voxel
     * Kirchhoff solve.  'je' = wetted/primer collector (film-reach contacts), 'je_bare' = bare
     * collector (crown contacts only) — 두 모드의 차이가 바닥 근처 전류 재분배(primer-paper
     * Fig-4d red box)를 3D로 보여줌.  Percentile-normalised; HIGH current = RED. */
    const fld = mode === 'je' ? 'je' : 'jb';
    const mm = (state.data && state.data.mpm_metrics) || {};
    const s3 = mm.step3 || null;
    const vals = [];
    ['AM_P', 'AM_S'].forEach(ty => {
      const m = state.meshes[ty]; if (!m) return;
      m.userData.particles.forEach(p => { if (p[fld] !== undefined) vals.push(p[fld]); });
    });
    if (!vals.length) {
      setLegend(state, '<i>이 payload엔 STEP3 전류밀도(<b>' + fld + '</b>)가 없어요 — 최신 '
        + '<b>mpm_webapp_payload.py</b>(--step3 기본 ON)로 payload를 재생성해서 업로드하세요.</i>');
      return;
    }
    if (state.meshes.MESH) {
      // paper Fig-4d solid-block read: SE painted as the ZERO-current phase (jet(0) = deep navy —
      // physically exact: SE carries no electronic current) and OPAQUE.  Interior inspection =
      // the 단면 슬라이더 (that is why the paper shows cross-sections).
      const mm2 = state.meshes.MESH;
      mm2.visible = true;
      if (!mm2.userData._baseColor) mm2.userData._baseColor = mm2.material.color.getHex();
      mm2.material.color.setHex(0x000080);
      mm2.material.transparent = false; mm2.material.opacity = 1.0;
    }
    const sorted = [...vals].sort((x, y) => x - y);
    const pctl = (p) => sorted[Math.max(0, Math.min(sorted.length - 1, Math.floor(p * (sorted.length - 1))))];
    const lo = 0, hi = Math.max(pctl(0.998), 1e-30);       // scale to ~max: the FIELD stays deep blue
    const norm = (v) => Math.max(0, Math.min(1, (v - lo) / (hi - lo)));
    const gam = (t) => Math.pow(t, 1.6);                   // gamma-compress mids toward blue (paper look:
    ['AM_P', 'AM_S'].forEach(ty => {                       //   only true hot paths leave the blue field)
      const m = state.meshes[ty]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        if (p[fld] === undefined) { m.setColorAt(i, colDim); return; }
        m.setColorAt(i, new THREE.Color(jetColor(gam(norm(p[fld])))));
      });
      m.material.opacity = 1.0; m.material.transparent = false;
    });
    flushColors();
    // collector slab (모식 — 두께 과장): thin plate under the bed; dark = primer/wetted, light = bare
    {
      const box = (state.data && state.data.box) || {};
      const w = (box.x_max || 50) - (box.x_min || 0), d = (box.y_max || 50) - (box.y_min || 0);
      const slabG = new THREE.BoxGeometry(w, 0.8, d);
      const slab = new THREE.Mesh(slabG, new THREE.MeshBasicMaterial({
        color: mode === 'je' ? 0x2f2f38 : 0x9aa2ad, transparent: true, opacity: 0.85 }));
      slab.position.set(w / 2, -0.5, d / 2);
      const grp = new THREE.Group(); grp.add(slab);
      state.additivePointGroup = grp;                     // reuse mode-switch cleanup
      if (state.scene) state.scene.add(grp);
    }
    const stops = [0, 0.25, 0.5, 0.75, 1].map(v => '#' + jetColor(v).toString(16).padStart(6, '0'));
    const cg = s3 && s3.collector_geometric;
    const sel = s3 && s3.collector && s3.collector.selected;
    setLegend(state,
      `<b>전류밀도 (STEP3 · ${mode === 'je' ? 'wetted/primer' : 'bare'} 집전체${sel && mode === 'je' ? ' — ' + sel.name : ''})</b>`
      + (s3 ? `<div style="margin-top:3px">σ_e_eff <b style="font-size:13px">${Number(s3.sigma_e_eff_S_cm).toExponential(2)}</b> S/cm`
          + (cg ? ` · R_geom <b>${Number(cg.R_geom_ohm_cm2).toExponential(2)}</b> Ω·cm²`
                : ` <span style="color:#9ca3af">(상대비교용 — σ표/vox 동일 세팅끼리)</span>`)
          + `</div>` : '')
      + (cg ? `<details style="margin-top:2px;font-size:11px;color:#cbd5e1"><summary style="cursor:pointer;color:#9ca3af">wetted/bare 상세</summary>
          σ wetted ${Number(cg.wetted_sigma_S_cm).toExponential(2)} (접점 ${cg.n_bottom_contacts.wetted})
          vs bare ${Number(cg.bare_sigma_S_cm).toExponential(2)} (${cg.n_bottom_contacts.bare}) S/cm<br>
          R_geom = L(1/σ_bare − 1/σ_wetted) — 바닥 기하 접촉만의 계면저항 (모델 출력; 측정 R_int와의 갭 = 화학/열화 몫)<br>
          집전체 슬래브는 모식(두께 과장) · σ_e_eff는 상대비교용(σ표/vox 동일 세팅끼리)</details>` : '')
      + `<div style="margin:5px 0 2px 0;height:10px;border-radius:3px;background:linear-gradient(90deg,${stops.join(',')})"></div>
       <div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af"><span>0</span><span>|J_z| (0–p99.8)</span><span>high</span></div>`
      + (s3 && s3.dissipation_share ? `<div style="margin-top:3px;color:#9ca3af;font-size:11px">손실(발열) 분담: `
          + Object.entries(s3.dissipation_share).map(([k, v]) => `${k} ${(100 * v).toFixed(0)}%`).join(' · ') + `</div>` : ''));
    return;
  }
  if (mode === 'additives' || mode === 'add_vgcf' || mode === 'add_superp' || mode === 'add_ptfe'
      || mode === 'add_sdcp') {
    /* conductive additives (payload additive_points: [x,y,z,phase]) as a coloured point cloud over a
     * dimmed SE+AM — so the carbon threading the SE/voids + bridging the AM reads clearly.  Colours are
     * BRIGHT (not SEM-black) for contrast on the dark canvas.  Sub-modes filter to one phase. */
    const PH = { 2: 'VGCF', 3: 'SuperP', 4: 'PTFE', 5: 'SDCP', 6: 'SWCNT' };
    const only = mode === 'add_vgcf' ? 2 : mode === 'add_superp' ? 3 : mode === 'add_ptfe' ? 4
               : mode === 'add_sdcp' ? 5 : 0;
    const mm = (state.data && state.data.mpm_metrics) || {};
    const all = (state.data && state.data.additive_points) || [];
    if (!all.length) {
      setLegend(state, state.isMPM
        ? '<i>이 payload엔 도전재가 없어요 (일반 압축 payload). VGCF/PTFE를 보려면 mpm3d를 '
          + '<b>--add-recipe</b>로 돌리고 payload를 <b>--phase phase.npy</b>로 재생성하세요.</i>'
        : '<i>No conductive-additive data in this payload.</i>');
      return;
    }
    const pts = only ? all.filter(p => p[3] === only) : all;
    // SE faint shell + AM dimmed so they don't bury the carbon; the points draw x-ray (below) so
    // they read clearly on top.  AM kept low (0.13) — higher made the view muddy.
    if (state.meshes.MESH) {
      state.meshes.MESH.visible = true;
      state.meshes.MESH.material.transparent = true; state.meshes.MESH.material.opacity = 0.18;
    }
    ['AM_P', 'AM_S'].forEach(ty => {                     // AM = SOLID near-black (the original SEM-like
      const m = state.meshes[ty]; if (!m) return;        // 도전재 look the user asked back for): carbon
      const base = new THREE.Color(0x141414);            // draws x-ray on top, so amber/cyan webs pop
      m.userData.particles.forEach((p, i) => m.setColorAt(i, base));   // on the dark spheres.  Instance
      if (m.instanceColor) m.instanceColor.needsUpdate = true;         // colors reset (no palette bleed).
      m.material.transparent = false; m.material.opacity = 1.0;
    });
    buildCarbonOverlay(state, only, only ? 1.0 : 0.7);   // fibres → lines, SuperP → points (x-ray)
    const nFib = ((state.data && state.data.additive_fibres) || [])
      .filter(f => !only || f.phase === only).length;
    const ac = mm.additive_counts || {};
    const swatch = { VGCF: '#22d3ee', SuperP: '#ec4899', PTFE: '#f59e0b', SDCP: '#ff3b30', SWCNT: '#22c55e' };
    const keys = only ? [PH[only]] : Object.keys(swatch).filter(k => ac[k]);
    const legend = keys.map(k =>
      `<span style="color:${swatch[k]};font-size:13px">●</span> ${k} ${Number(ac[k] || 0).toLocaleString()}개`).join(' &nbsp; ');
    setLegend(state,
      `<b>도전재 (3D)${only ? ' — ' + PH[only] + '만' : ' — 전체'}</b>
       <div style="margin-top:4px">${legend || '–'}</div>
       <div style="margin-top:3px;color:#9ca3af;font-size:11px">SE·AM 반투명, 카본은 x-ray로 위에. `
       + (nFib ? `${nFib.toLocaleString()}개 fibre를 개별 line으로 표시 (VGCF 고항복 → 막대 유지)`
              : `${pts.length.toLocaleString()}점 (fibre 데이터 없음 — point cloud)`) + `</div>`);
    return;
  }

  if (mode === 'se_engagement') {
    /* SE engagement → residual micro-pore map.
     *
     * Physical premise (paper §5 + Sakuda 2013 framework):
     *   Cold-press SE plastic flow fills the AM-AM voids. When
     *   plastic flow is STRONG, SE conforms to the gap geometry
     *   and the gap closes — low residual porosity locally.
     *   When plastic flow is WEAK (SE only Hertz-elastic, AM-AM
     *   force chain bypasses SE), the SE springs back on release
     *   and a micro-pore remains.
     *
     *   → "WEAK SE plastic flow"  ==  "high local pore risk"
     *
     * So this view inverts the previous over-plastic-as-risk draft.
     * Particles with LOW engagement (score → 0) are coloured BRIGHT
     * RED to pop as micro-pore hotspots; particles with HIGH
     * engagement (score → 1) are muted dark teal as harmless
     * background that already filled their voids.
     */
    /* engagement[se_id] is a single float (engagement score 0-1)
     * since commit 42b3ea6 — was a 6-field dict, but the visualisation
     * only reads `.score`, so the backend now sends just that number
     * to keep the JSON payload under 10 MB for 620k-SE particulate
     * cases (was hitting "Unexpected end of JSON input" at 60 MB). */
    const engagement = aux.se_engagement || {};
    const n_se_total_backend = aux.all_se_ids_count || 0;
    const seMeshCount = (state.meshes.SE && state.meshes.SE.userData.particles)
      ? state.meshes.SE.userData.particles.length
      : 0;
    const auxAvailable = Object.keys(engagement).length > 0;

    /* Sequential red→muted green gradient (low engagement = pore risk) */
    const poreRiskColor = (s) => {
      if (s <= 0.5) {
        const t = s / 0.5;
        const r = 1.00;
        const g = 0.20 + (0.65 - 0.20) * t;
        const b = 0.13 + (0.20 - 0.13) * t;
        return new THREE.Color(r, g, b);
      }
      const t = (s - 0.5) / 0.5;
      const r = 1.00 + (0.30 - 1.00) * t;
      const g = 0.65 + (0.55 - 0.65) * t;
      const b = 0.20 + (0.48 - 0.20) * t;
      return new THREE.Color(r, g, b);
    };
    const colorIdle = new THREE.Color(0x1b1f2e);

    [state.meshes.AM_P, state.meshes.AM_S].forEach(m => {
      if (!m) return;
      m.userData.particles.forEach((_, i) =>
        m.setColorAt(i, new THREE.Color(0x222226)));
      m.material.opacity = 0.18;
      m.material.transparent = true;
    });

    let nStrong = 0, nPartial = 0, nWeak = 0, nIdle = 0;
    const seMesh = state.meshes.SE;
    if (seMesh) {
      seMesh.userData.particles.forEach((p, i) => {
        const s = engagement[p.id];
        if (s === undefined || s === null) {
          seMesh.setColorAt(i, colorIdle); nIdle++;
          return;
        }
        seMesh.setColorAt(i, poreRiskColor(s));
        if (s >= 0.7)        nStrong++;
        else if (s >= 0.3)   nPartial++;
        else                 nWeak++;
      });
      seMesh.material.opacity = 0.92;
      seMesh.material.transparent = true;
    }
    flushColors();

    const fmtCount = n =>
      (n >= 10000) ? (Math.round(n / 1000) + 'k')
      : (n >= 1000) ? n.toLocaleString()
      : n.toString();
    /* Use backend SE count when available (authoritative from
     * atoms.csv walk); fall back to InstancedMesh particle count
     * (matches whatever shapes actually rendered on screen).
     * Avoids the "62,000,000 %" bug seen on input_particulate_1
     * when aux was skipped and SE count came back 0. */
    const n_total = (n_se_total_backend || seMeshCount) || 1;
    const pct = (n) => (100 * n / n_total).toFixed(1) + '%';

    const row = (color, sym, count, label, pctStr, tip) => `
      <div title="${tip}  (${count.toLocaleString()} particles)"
           style="display:flex;align-items:baseline;gap:6px;
                  font-size:11.5px;line-height:1.35">
        <span style="color:${color};font-size:13px;line-height:0.9;
                     flex:0 0 10px;text-align:center">${sym}</span>
        <span style="color:#cbd5e1;flex:1 1 auto;min-width:0;
                     white-space:nowrap;overflow:hidden;
                     text-overflow:ellipsis">${label}</span>
        <span style="color:#e5e7eb;font-weight:600;
                     font-family:ui-monospace,Menlo,monospace;
                     flex:0 0 auto;text-align:right;
                     min-width:30px">${fmtCount(count)}</span>
        <span style="color:#9ca3af;font-size:10.5px;
                     font-family:ui-monospace,Menlo,monospace;
                     flex:0 0 auto;text-align:right;
                     min-width:38px">${pctStr}</span>
      </div>`;

    const banner = auxAvailable ? '' : `
      <div style="background:rgba(180,83,9,.18);
                  border:1px solid rgba(245,158,11,.45);
                  color:#fcd34d;font-size:11px;line-height:1.35;
                  padding:5px 7px;border-radius:4px;margin-bottom:5px">
        ⚠ aux 계산 skip된 케이스 (contacts.csv가 너무 큼 또는 cache miss).
        Engagement 분류 데이터 없음 — 모든 SE를 idle로 표시.<br>
        <span style="color:#fde68a;font-size:10.5px">
          → Flask console 로그 / 재실행으로 cache 생성 후 다시 로드.
        </span>
      </div>`;

    setLegend(state,
      `${banner}
       <div style="font-weight:600;color:#cbd5e1;font-size:12px;margin-bottom:2px">
         SE pore-risk map
       </div>
       <div style="color:#9ca3af;font-size:10.5px;line-height:1.35"
            title="engagement_score = (n_plastic + 0.5·n_yield) / n_total. Lower score = SE failed to plastically fill its AM-AM void → micro-pore remains after release.">
         약한 plastic flow → SE가 AM-AM gap 못 채움 → micro-pore<br>
         빨강 = 위험, 녹색 = SE가 gap 잘 채움 (안전)
       </div>
       <div style="display:flex;align-items:center;gap:4px;
                    margin:6px 0 4px;font-size:10.5px;color:#9ca3af">
         <span title="risk high">위험</span>
         <div style="flex:1;height:8px;border-radius:4px;
                     background:linear-gradient(90deg,
                       rgb(255,51,33) 0%,
                       rgb(255,166,51) 50%,
                       rgb(77,140,122) 100%)"></div>
         <span title="risk low">안전</span>
       </div>
       <div style="display:flex;flex-direction:column;gap:2px;margin-top:4px">
         ${row('#ff3321', '●', nWeak, 'Pore risk: HIGH', pct(nWeak),
                'engagement < 0.3 — SE가 거의 elastic만, plastic flow 부족. AM-AM gap에 spring-back으로 micro-pore 생성 candidate.')}
         ${row('#ffa633', '●', nPartial, 'Pore risk: med', pct(nPartial),
                '0.3 ≤ engagement < 0.7 — 부분적 plastic flow. 일부 gap 채우고 일부는 남음.')}
         ${row('#4d8c7a', '●', nStrong, 'Well-engaged', pct(nStrong),
                'engagement ≥ 0.7 — SE가 plastic flow로 AM-AM gap 완전 충진. 안전.')}
         ${row('#1b1f2e', '○', nIdle, 'Idle (no contact)', pct(nIdle),
                'AM-AM void에 완전 isolated SE — 어차피 인접 AM 없어서 channel 형성 불가.')}
       </div>
       <div style="color:#9ca3af;font-size:10px;line-height:1.4;
                    margin-top:5px;padding-top:4px;
                    border-top:1px solid rgba(99,102,241,.18)">
         ★ HIGH/medium 빨강 입자가 많을수록 → cold-press 후 micro-pore 잔류 위험<br>
         ★ Well-engaged 녹색이 dominant → SE가 잘 충진된 dense cathode<br>
         ★ paper §5 p_se sigmoid: HIGH = OFF zone, Well = ON zone
       </div>`);
    return;
  }

  /* ── Phase B1: Worst F/P_c per particle (continuous log heatmap) ───
   * Unlike Brittle Hotspots which bins into 5 Lawn stages, this shows
   * the actual F/P_c value on a continuous log scale.  Two particles
   * both in "multi-crack" stage (F/P_c ∈ [3, 11]) will look different
   * if one is at 3.5 vs 10.5.  Also includes intact particles so you
   * can see who is "on the edge" (F/P_c just below 1).
   */
  if (mode === 'worst_fpc') {
    const fpcMap = aux.particle_max_fpc || {};
    /* Collect values to compute quantiles */
    const vals = [];
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach(p => {
        const v = fpcMap[String(p.id)] ?? fpcMap[p.id];
        if (v !== undefined) vals.push(v);
      });
    });
    if (!vals.length) {
      dimAll();
      setLegend(state, '<i>No F/P_c data — run reanalysis (cache schema 4+).</i>');
      flushColors();
      return;
    }
    /* Log scale: x = log10(F/P_c + 0.1) so F/P_c=0 → -1, F/P_c=1 → 0.04,
     * F/P_c=10 → 1.0, F/P_c=30 → 1.49.  Map to [0,1] using the data
     * range.  Then coolwarm colormap. */
    const xs = vals.map(v => Math.log10(v + 0.1));
    const xLo = Math.min(...xs);
    const xHi = Math.max(...xs);
    const xMid = Math.log10(1 + 0.1);   /* F/P_c = 1 threshold position */
    const norm = (v) => {
      const x = Math.log10(v + 0.1);
      return Math.max(0, Math.min(1, (x - xLo) / (xHi - xLo + 1e-9)));
    };
    /* Diverging colormap: cool→neutral→warm, centered on F/P_c=1 */
    const tThreshold = Math.max(0, Math.min(1, (xMid - xLo) / (xHi - xLo + 1e-9)));
    const heat = (v) => {
      const t = norm(v);
      /* Below threshold: dark blue → cyan → green-yellow */
      /* Above threshold: yellow → orange → deep red */
      if (t < tThreshold) {
        const u = t / Math.max(1e-9, tThreshold);
        /* dark blue (#1e3a8a) → cyan (#06b6d4) → pale yellow (#fef3c7) */
        if (u < 0.5) {
          const w = u / 0.5;
          return new THREE.Color(0x1e3a8a).lerp(new THREE.Color(0x06b6d4), w);
        } else {
          const w = (u - 0.5) / 0.5;
          return new THREE.Color(0x06b6d4).lerp(new THREE.Color(0xfef3c7), w);
        }
      } else {
        const u = (t - tThreshold) / Math.max(1e-9, 1 - tThreshold);
        /* pale yellow → orange (#f97316) → deep red (#7f1d1d) */
        if (u < 0.5) {
          const w = u / 0.5;
          return new THREE.Color(0xfef3c7).lerp(new THREE.Color(0xf97316), w);
        } else {
          const w = (u - 0.5) / 0.5;
          return new THREE.Color(0xf97316).lerp(new THREE.Color(0x7f1d1d), w);
        }
      }
    };
    let nHit = 0, maxSeen = 0, minSeen = Infinity, nOver = 0;
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        const v = fpcMap[String(p.id)] ?? fpcMap[p.id];
        if (v === undefined) {
          m.setColorAt(i, colDim);
          return;
        }
        m.setColorAt(i, heat(v));
        nHit++;
        if (v > maxSeen) maxSeen = v;
        if (v < minSeen) minSeen = v;
        if (v >= 1) nOver++;
      });
      m.material.opacity = 0.95; m.material.transparent = true;
    });
    /* SE always dim */
    const seMesh = state.meshes.SE;
    if (seMesh) {
      seMesh.userData.particles.forEach((_, i) => seMesh.setColorAt(i, colDim));
      seMesh.material.opacity = 0.06; seMesh.material.transparent = true;
    }
    flushColors();
    /* Quantiles for legend */
    const sorted = [...vals].sort((a,b) => a-b);
    const q = (p) => sorted[Math.max(0, Math.min(sorted.length-1,
        Math.floor(p * (sorted.length-1))))];
    const overPct = nHit ? (100 * nOver / nHit).toFixed(1) : '0.0';
    setLegend(state,
      `<b>Worst F/P_c per particle (continuous log scale)</b><br>
       <div style="display:flex;align-items:center;gap:4px;margin:4px 0">
         <span style="display:inline-block;width:6em;height:10px;background:linear-gradient(to right,
           #1e3a8a 0%, #06b6d4 ${50*tThreshold}%, #fef3c7 ${100*tThreshold}%,
           #f97316 ${100*(tThreshold + (1-tThreshold)/2)}%, #7f1d1d 100%)"></span>
         <span style="font-size:10px;color:#9ca3af">${minSeen.toFixed(2)} → ${maxSeen.toFixed(2)}</span>
       </div>
       <table style="font-size:10px;color:#cbd5e1;border-collapse:collapse">
         <tr><td style="padding:0 4px 0 0">F/P_c = 1 threshold</td><td>${nOver}/${nHit} (${overPct}%)</td></tr>
         <tr><td style="padding:0 4px 0 0">median</td><td>${q(0.5).toFixed(2)}</td></tr>
         <tr><td style="padding:0 4px 0 0">95th pct</td><td>${q(0.95).toFixed(2)}</td></tr>
         <tr><td style="padding:0 4px 0 0">max</td><td>${maxSeen.toFixed(2)}</td></tr>
       </table>
       <span style="color:#9ca3af;font-size:10px">★ Brittle Hotspots는 stage로 bin해서 보지만 이 mode는 F/P_c 실값을 연속으로 표시 — 같은 multi-crack stage 안에서도 F/P_c=3.5 와 10.5 의 차이가 그라데이션으로 보임. 흰색 부근이 임계 F/P_c=1 (fracture 시작 경계).</span>`);
    return;
  }

  /* ── Phase B3: AM_P Fracture Skeleton (connected components) ─────── */
  if (mode === 'am_p_skeleton') {
    dimAll();
    const skeleton = aux.am_p_skeleton || [];        // list of clusters
    if (!skeleton.length) {
      setLegend(state,
        '<b>AM_P Fracture Skeleton</b><br>' +
        '<i style="color:#9ca3af">F/P_c ≥ 1 인 AM_P-AM_P 접촉 없음 — 이 case는 다행히 fracture-prone backbone이 없음.</i>');
      return;
    }
    /* Build membership: pid → cluster index (largest = 0) */
    const clusterOf = {};
    skeleton.forEach((cluster, ci) => cluster.forEach(pid => { clusterOf[pid] = ci; }));
    /* Distinct color per cluster, largest = bright red, smaller = orange/yellow */
    const palette = [0xef4444, 0xf97316, 0xfbbf24, 0xfde047,
                     0xa3e635, 0x4ade80, 0x2dd4bf, 0x60a5fa];
    const colorOfCluster = (ci) => palette[Math.min(ci, palette.length - 1)];
    /* Color AM_P particles by their cluster */
    let nHit = 0;
    const mAP = state.meshes.AM_P;
    if (mAP) {
      mAP.userData.particles.forEach((p, i) => {
        const ci = clusterOf[p.id];
        if (ci !== undefined) {
          mAP.setColorAt(i, new THREE.Color(colorOfCluster(ci)));
          nHit++;
        }
      });
      mAP.material.opacity = 0.95; mAP.material.transparent = true;
    }
    /* AM_S and SE dim */
    ['AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((_, i) => m.setColorAt(i, colDim));
      m.material.opacity = 0.06; m.material.transparent = true;
    });
    /* Draw lines connecting skeleton particles using stress chain data.
     * Three.js coordinate convention: data (x, y, z) → THREE (x, z, y)
     * (data z = vertical → Three Y).  Also skip periodic-wraparound
     * contacts where the two particles are on opposite sides of the box
     * (straight-line would shoot outside the visible cell). */
    const segs = aux.stress_chain_segments || [];
    if (segs.length && state.scene) {
      const group = new THREE.Group();
      /* Build position lookup using correct Y-up convention */
      const pos = {};
      ['AM_P', 'AM_S'].forEach(t => {
        const m = state.meshes[t]; if (!m) return;
        m.userData.particles.forEach(p => {
          pos[p.id] = new THREE.Vector3(p.x, p.z, p.y);
        });
      });
      /* Periodic-jump cutoff: half the box X / Y span (data coords) */
      const box = state.data && state.data.box;
      const halfX = box ? (box.x_max - box.x_min) / 2 : Infinity;
      const halfY = box ? (box.y_max - box.y_min) / 2 : Infinity;
      let nDrawn = 0, nSkippedPeriodic = 0;
      segs.forEach(s => {
        if (s.pair_type !== 'AM_P-AM_P' || s.mult < 1) return;
        const a = pos[s.id1], b = pos[s.id2];
        if (!a || !b) return;
        /* In THREE coords: x → data x, z → data y */
        if (Math.abs(a.x - b.x) > halfX || Math.abs(a.z - b.z) > halfY) {
          nSkippedPeriodic++;
          return;
        }
        /* Tube thick enough to be visible at the contact point even when
         * embedded in touching particles.  Floor 1.0 μm, scales with
         * log(F/P_c) up to ~3 μm at pulverization severity. */
        const r = Math.max(1.0, Math.log10(s.mult + 1) * 2.0);
        const ci = clusterOf[s.id1] ?? clusterOf[s.id2] ?? 0;
        const tube = new THREE.TubeGeometry(
          new THREE.LineCurve3(a, b), 1, r, 12, false);
        const mat = new THREE.MeshBasicMaterial({
          color: colorOfCluster(ci),
          transparent: true, opacity: 0.92,
          depthWrite: false,   /* draw over particle bodies — preserves
                                  cluster topology visibility */
        });
        group.add(new THREE.Mesh(tube, mat));
        nDrawn++;
      });
      state.scene.add(group);
      state.stressChainGroup = group;
    }
    flushColors();
    const nClusters = skeleton.length;
    const biggest = skeleton[0].length;
    setLegend(state,
      `<b>AM_P Fracture Skeleton (load-bearing backbone)</b><br>
       ${nClusters} 개 cluster, 가장 큰 cluster = ${biggest} 입자<br>
       총 skeleton 입자 = ${nHit}<br>
       <span style="color:#ef4444">●</span> Cluster #1 (largest)
       <span style="color:#f97316">●</span> #2
       <span style="color:#fbbf24">●</span> #3 ...<br>
       <span style="color:#9ca3af;font-size:10px">★ F/P_c ≥ 1 인 AM_P-AM_P 접촉으로 연결된 connected component. 이 backbone에서 fragmentation이 시작되어 cascade 가능.</span>`);
    return;
  }

  /* ── Phase B2: Stress Chain (all AM-AM contacts as line segments) ── */
  if (mode === 'stress_chain') {
    /* Keep default particle colors, just overlay lines */
    ['AM_P', 'AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      const base = (t === 'SE') ? colSeBase
                                : new THREE.Color(t === 'AM_P' ? COL.AM_P : COL.AM_S);
      m.userData.particles.forEach((_, i) => m.setColorAt(i, base));
      m.material.opacity = (t === 'SE') ? 0.10 : 0.45;
      m.material.transparent = true;
    });
    const segs = aux.stress_chain_segments || [];
    if (!segs.length) {
      setLegend(state, '<i>No stress chain data</i>');
      flushColors();
      return;
    }
    /* Default filters — fresh entry into this mode resets to "all on" */
    state.stressChainFilter = {
      'AM_P-AM_P': true, 'AM_P-AM_S': true,
      'AM_S-AM_S': true, 'intact':    true,
    };
    state.stressChainStageFilter = {
      'microcrack': true, 'multicrack': true,
      'fragmentation': true, 'pulverization': true,
    };
    renderStressChain(state, segs);
    flushColors();
    return;
  }

  /* ── Phase A5+A6: SE Network Diagnostics ─────────────────────────── */
  if (mode === 'se_diagnostics') {
    const nPerc = aux.se_n_percolating || 0;
    if (!nPerc) {
      ['AM_P', 'AM_S'].forEach(t => {
        const m = state.meshes[t]; if (!m) return;
        m.userData.particles.forEach((_, i) => m.setColorAt(i, colDim));
        m.material.opacity = 0.05; m.material.transparent = true;
      });
      const seMesh = state.meshes.SE;
      if (seMesh) {
        seMesh.userData.particles.forEach((_, i) => seMesh.setColorAt(i, colDim));
        seMesh.material.opacity = 0.35; seMesh.material.transparent = true;
      }
      flushColors();
      setLegend(state, '<i>No SE percolation data (run reanalysis).</i>');
      return;
    }
    /* Default filter — fresh entry into this mode resets to "all on" */
    state.seDiagFilter = {
      'percolating': true, 'articulation': true,
      'dead_top': true, 'dead_bot': true, 'bottleneck': true,
    };
    renderSeDiagnostics(state);
    return;
  }
}
/* ── Stress Chain renderer (Phase B2) ─────────────────────────────────
 * Rebuilds the tube group based on state.stressChainFilter.  Called
 * once on view-mode entry and again on every filter-button click so
 * the user can toggle pair-types / intact on/off independently.
 */
function renderStressChain(state, segs) {
  /* Dispose any existing chain group */
  if (state.stressChainGroup && state.scene) {
    state.scene.remove(state.stressChainGroup);
    state.stressChainGroup.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
    state.stressChainGroup = null;
  }
  const filter = state.stressChainFilter || {
    'AM_P-AM_P': true, 'AM_P-AM_S': true,
    'AM_S-AM_S': true, 'intact':    true,
  };
  /* Stage filter (cross-cuts with pair-type filter via AND) */
  const stageFilter = state.stressChainStageFilter || {
    'microcrack': true, 'multicrack': true,
    'fragmentation': true, 'pulverization': true,
  };
  /* Stage classification — must match Lawn 1998 thresholds in
   * fracture_model.py: 1, 3, 11, 32.  Intact handled by pair-type
   * filter ('intact' key), so this only filters brittle (mult >= 1). */
  const stageOf = (mult) => {
    if (mult >= 32) return 'pulverization';
    if (mult >= 11) return 'fragmentation';
    if (mult >= 3)  return 'multicrack';
    return 'microcrack';   /* mult in [1, 3) */
  };
  /* Position lookup */
  const pos = {};
  ['AM_P', 'AM_S'].forEach(t => {
    const m = state.meshes[t]; if (!m) return;
    m.userData.particles.forEach(p => {
      pos[p.id] = new THREE.Vector3(p.x, p.z, p.y);
    });
  });
  const box = state.data && state.data.box;
  const halfX = box ? (box.x_max - box.x_min) / 2 : Infinity;
  const halfY = box ? (box.y_max - box.y_min) / 2 : Infinity;
  const pairCol = {
    'AM_P-AM_P': 0xef4444,
    'AM_P-AM_S': 0xf97316,
    'AM_S-AM_S': 0x60a5fa,
  };
  const group = new THREE.Group();
  let nDrawn = 0, nIntact = 0, nSevere = 0, nSkippedPeriodic = 0;
  /* Total counts per filter category (so legend numbers reflect data,
   * not just what's currently drawn) */
  const totalCounts = {
    'AM_P-AM_P': 0, 'AM_P-AM_S': 0, 'AM_S-AM_S': 0, 'intact': 0,
  };
  const stageCounts = {
    'microcrack': 0, 'multicrack': 0,
    'fragmentation': 0, 'pulverization': 0,
  };
  segs.forEach(s => {
    const a = pos[s.id1], b = pos[s.id2];
    if (!a || !b) return;
    if (Math.abs(a.x - b.x) > halfX || Math.abs(a.z - b.z) > halfY) {
      nSkippedPeriodic++;
      return;
    }
    const isIntact = s.mult < 1;
    /* tally totals before filter */
    if (isIntact) totalCounts['intact']++;
    else {
      totalCounts[s.pair_type] = (totalCounts[s.pair_type] || 0) + 1;
      stageCounts[stageOf(s.mult)]++;
    }
    /* apply filters — pair-type AND stage must both allow */
    if (isIntact && !filter['intact']) return;
    if (!isIntact) {
      if (!filter[s.pair_type]) return;
      if (!stageFilter[stageOf(s.mult)]) return;
    }

    if (isIntact) nIntact++; else nSevere++;
    const r = Math.max(0.12, Math.log10(s.mult + 1.1) * 0.5);
    const tube = new THREE.TubeGeometry(
      new THREE.LineCurve3(a, b), 1, r, 6, false);
    const col = isIntact ? 0x4b5563 : pairCol[s.pair_type] || 0x9ca3af;
    const mat = new THREE.MeshBasicMaterial({
      color: col,
      transparent: true,
      opacity: isIntact ? 0.18 : 0.85,
    });
    group.add(new THREE.Mesh(tube, mat));
    nDrawn++;
  });
  if (state.scene) {
    state.scene.add(group);
    state.stressChainGroup = group;
  }

  /* Pair-type filter button helper */
  const btn = (key, color, label, count) => {
    const on = filter[key];
    const bg = on ? color : '#1f2937';
    const fg = on ? '#fff' : '#6b7280';
    const border = on ? color : '#374151';
    return `<button data-sc-filter="${key}"
       style="background:${bg};color:${fg};border:1px solid ${border};
              border-radius:3px;padding:1px 4px;font-size:10px;cursor:pointer;
              margin:1px 1px 0 0;white-space:nowrap">${label} ${count}</button>`;
  };
  /* Stage filter button helper */
  const stageBtn = (key, label, count) => {
    const on = stageFilter[key];
    const bg = on ? '#7c3aed' : '#1f2937';
    const fg = on ? '#fff' : '#6b7280';
    const border = on ? '#7c3aed' : '#374151';
    return `<button data-sc-stage="${key}"
       style="background:${bg};color:${fg};border:1px solid ${border};
              border-radius:3px;padding:1px 4px;font-size:10px;cursor:pointer;
              margin:1px 1px 0 0;white-space:nowrap">${label} ${count}</button>`;
  };
  setLegend(state,
    `<b style="font-size:11px">Stress Chain</b>
     <span style="color:#9ca3af;font-size:10px">(${nDrawn.toLocaleString()} drawn${
       nSkippedPeriodic ? `, ${nSkippedPeriodic} wrap` : ''
     })</span>
     <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0;margin-top:3px">
       <button data-sc-filter="ALL"
         style="background:#0ea5e9;color:#fff;border:1px solid #0284c7;
                border-radius:3px;padding:1px 4px;font-size:10px;cursor:pointer;
                margin:1px 1px 0 0;font-weight:bold;white-space:nowrap">ALL</button>
       ${btn('AM_P-AM_P', '#ef4444', 'P-P', totalCounts['AM_P-AM_P'])}
       ${btn('AM_P-AM_S', '#f97316', 'P-S', totalCounts['AM_P-AM_S'])}
       ${btn('AM_S-AM_S', '#60a5fa', 'S-S', totalCounts['AM_S-AM_S'])}
       ${btn('intact',    '#4b5563', 'int', totalCounts['intact'])}
     </div>
     <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0;margin-top:2px">
       <button data-sc-stage="ALL"
         style="background:#7c3aed;color:#fff;border:1px solid #6d28d9;
                border-radius:3px;padding:1px 4px;font-size:10px;cursor:pointer;
                margin:1px 1px 0 0;font-weight:bold;white-space:nowrap">ALL</button>
       ${stageBtn('microcrack',    'μ',    stageCounts['microcrack'])}
       ${stageBtn('multicrack',    'M',    stageCounts['multicrack'])}
       ${stageBtn('fragmentation', 'F',    stageCounts['fragmentation'])}
       ${stageBtn('pulverization', 'P',    stageCounts['pulverization'])}
     </div>
     <div style="color:#6b7280;font-size:8px;margin-top:3px;line-height:1.3">
       두께∝log(F/P_c). Pair AND stage. F/P_c: μ 1–3, M 3–11, F 11–32, P ≥32
     </div>`);

  /* Wire up filter buttons */
  const legendEl = document.getElementById('view-mode-legend');
  if (legendEl) {
    /* Pair-type buttons */
    legendEl.querySelectorAll('[data-sc-filter]').forEach(b => {
      b.addEventListener('click', () => {
        const key = b.dataset.scFilter;
        if (key === 'ALL') {
          state.stressChainFilter = {
            'AM_P-AM_P': true, 'AM_P-AM_S': true,
            'AM_S-AM_S': true, 'intact':    true,
          };
        } else {
          state.stressChainFilter[key] = !state.stressChainFilter[key];
        }
        renderStressChain(state, segs);
      });
    });
    /* Stage buttons */
    legendEl.querySelectorAll('[data-sc-stage]').forEach(b => {
      b.addEventListener('click', () => {
        const key = b.dataset.scStage;
        if (key === 'ALL') {
          state.stressChainStageFilter = {
            'microcrack': true, 'multicrack': true,
            'fragmentation': true, 'pulverization': true,
          };
        } else {
          state.stressChainStageFilter[key] = !state.stressChainStageFilter[key];
        }
        renderStressChain(state, segs);
      });
    });
  }
}

/* ── SE Network Diagnostics renderer (Phase A5+A6) ─────────────────────
 * Re-applies coloring + bottleneck tubes based on state.seDiagFilter.
 * Called once on view-mode entry and again on every filter click so
 * the user can toggle each category independently.
 */
function renderSeDiagnostics(state) {
  /* Dispose any existing bottleneck tube group */
  if (state.stressChainGroup && state.scene) {
    state.scene.remove(state.stressChainGroup);
    state.stressChainGroup.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
    state.stressChainGroup = null;
  }
  const aux = (state.data && state.data.aux) || {};
  /* Scene bg is #f5f5f5 (light gray) — use a tone very close to it so
   * filtered-off particles fade into the background instead of showing
   * up as dark dots. */
  const colDim = new THREE.Color(0xdcdce0);
  const filter = state.seDiagFilter || {
    'percolating': true, 'articulation': true,
    'dead_top': true, 'dead_bot': true, 'bottleneck': true,
  };
  const perc = new Set(aux.se_percolating || []);
  const artPts = new Set(aux.se_articulation_points || []);
  const deadEnds = aux.se_dead_end_clusters || [];
  const bnEdges = aux.se_bottleneck_edges || [];
  const nPerc = aux.se_n_percolating || 0;

  /* Background: AM faint */
  ['AM_P', 'AM_S'].forEach(t => {
    const m = state.meshes[t]; if (!m) return;
    m.userData.particles.forEach((_, i) => m.setColorAt(i, colDim));
    m.material.opacity = 0.05; m.material.transparent = true;
  });
  /* SE: gray fallback for any particle not in an active filter group */
  const seMesh = state.meshes.SE;
  const colPerc = new THREE.Color(0x14b8a6);   // teal
  const colArt  = new THREE.Color(0xfacc15);   // yellow
  const colDeadTop = new THREE.Color(0xec4899); // magenta
  const colDeadBot = new THREE.Color(0xf97316); // orange
  /* dead-end membership */
  const deadEndType = {};
  deadEnds.forEach(d => {
    d.ids.forEach(pid => { deadEndType[pid] = d.type; });
  });
  if (seMesh) {
    /* Per-instance scale: highlighted → full size, dim → 35% size so
     * they recede visually.  Three.js InstancedMesh has no per-instance
     * opacity, so we use matrix scale to fake transparency.  The
     * tear-down block (top of applyViewMode) restores original size
     * when switching modes. */
    const dummy = new THREE.Object3D();
    seMesh.userData.particles.forEach((p, i) => {
      let col = colDim;
      let highlighted = false;
      if (artPts.has(p.id) && filter['articulation']) {
        col = colArt; highlighted = true;
      } else if (perc.has(p.id) && filter['percolating']) {
        col = colPerc; highlighted = true;
      } else if (deadEndType[p.id] === 'top_only' && filter['dead_top']) {
        col = colDeadTop; highlighted = true;
      } else if (deadEndType[p.id] === 'bottom_only' && filter['dead_bot']) {
        col = colDeadBot; highlighted = true;
      }
      seMesh.setColorAt(i, col);
      /* shrink un-highlighted SE so highlighted ones pop;
       * dim ones go to 25% size and blend into the light background */
      const scale = highlighted ? p.r : p.r * 0.25;
      dummy.position.set(p.x, p.z, p.y);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      seMesh.setMatrixAt(i, dummy.matrix);
    });
    seMesh.instanceMatrix.needsUpdate = true;
    seMesh.material.opacity = 0.85; seMesh.material.transparent = true;
    state.seInstanceScaleModified = true;
  }

  /* Bottleneck tubes (only if filter on) */
  if (state.scene && bnEdges.length && filter['bottleneck']) {
    const group = new THREE.Group();
    const pos = {};
    if (seMesh) {
      seMesh.userData.particles.forEach(p => {
        pos[p.id] = new THREE.Vector3(p.x, p.z, p.y);
      });
    }
    const box = state.data && state.data.box;
    const halfX = box ? (box.x_max - box.x_min) / 2 : Infinity;
    const halfY = box ? (box.y_max - box.y_min) / 2 : Infinity;
    const sortedBn = [...bnEdges].sort((a, b) => a.area_um2 - b.area_um2);
    const minArea = sortedBn[0]?.area_um2 || 0;
    const maxArea = sortedBn[sortedBn.length - 1]?.area_um2 || 1;
    sortedBn.forEach(e => {
      const a = pos[e.id1], b = pos[e.id2];
      if (!a || !b) return;
      if (Math.abs(a.x - b.x) > halfX || Math.abs(a.z - b.z) > halfY) return;
      const t = (e.area_um2 - minArea) / Math.max(1e-9, maxArea - minArea);
      const hue = 0 + t * 30;
      const col = new THREE.Color(`hsl(${hue}, 90%, 50%)`);
      const tube = new THREE.TubeGeometry(
        new THREE.LineCurve3(a, b), 1, 1.0, 8, false);
      const mat = new THREE.MeshBasicMaterial({
        color: col, transparent: true, opacity: 0.95,
        depthWrite: false,
      });
      group.add(new THREE.Mesh(tube, mat));
    });
    state.scene.add(group);
    state.stressChainGroup = group;
  }
  /* flushColors */
  ['AM_P', 'AM_S', 'SE'].forEach(t => {
    const m = state.meshes[t];
    if (m && m.instanceColor) m.instanceColor.needsUpdate = true;
  });

  /* Filter button helper */
  const deadTop = deadEnds.filter(d => d.type === 'top_only').length;
  const deadBot = deadEnds.filter(d => d.type === 'bottom_only').length;
  const narrowest = bnEdges[0]?.area_um2;
  const narrowestNorm = bnEdges[0]?.area_norm;
  const medianNorm = aux.se_bn_median_norm;
  const thresholdNorm = aux.se_bn_threshold_norm;
  const btn = (key, color, label, count) => {
    const on = filter[key];
    const bg = on ? color : '#1f2937';
    const fg = on ? '#fff' : '#6b7280';
    const border = on ? color : '#374151';
    return `<button data-sed-filter="${key}"
       style="background:${bg};color:${fg};border:1px solid ${border};
              border-radius:3px;padding:1px 4px;font-size:10px;cursor:pointer;
              margin:1px 1px 0 0;white-space:nowrap">${label} ${count}</button>`;
  };
  setLegend(state,
    `<b style="font-size:11px">SE Network Diagnostics</b>
     <div style="display:flex;flex-wrap:wrap;gap:0;margin-top:3px">
       <button data-sed-filter="ALL"
         style="background:#0ea5e9;color:#fff;border:1px solid #0284c7;
                border-radius:3px;padding:1px 4px;font-size:10px;cursor:pointer;
                margin:1px 1px 0 0;font-weight:bold;white-space:nowrap">ALL</button>
       ${btn('percolating',  '#14b8a6', 'perc',     nPerc)}
       ${btn('articulation', '#facc15', 'cut',      artPts.size)}
       ${btn('dead_top',     '#ec4899', 'd-top',    deadTop)}
       ${btn('dead_bot',     '#f97316', 'd-bot',    deadBot)}
       ${btn('bottleneck',   '#dc2626', 'bn',       bnEdges.length)}
     </div>
     <div style="color:#6b7280;font-size:8px;margin-top:3px;line-height:1.3">
       narrowest: ${typeof narrowest === 'number' ? narrowest.toFixed(3) + ' μm²' : '—'}
       (A/r² = ${typeof narrowestNorm === 'number' ? narrowestNorm.toFixed(4) : '—'})<br>
       bn threshold = A/r² &lt; ${typeof thresholdNorm === 'number' ? thresholdNorm.toFixed(4) : '—'}
       (median × 10%, median = ${typeof medianNorm === 'number' ? medianNorm.toFixed(3) : '—'})<br>
       cut node 제거 시 percolation 분리. bn 빨강 진할수록 좁음. d-top/bot = 한쪽만 닿은 SE 클러스터.
     </div>
     <div style="margin-top:8px;padding-top:6px;border-top:1px solid #2a2d3e">
       <button data-sed-open-hub
         style="background:linear-gradient(135deg,#6366f1 0%,#2563eb 55%,#1d4ed8 100%);
                color:#fff;border:1px solid rgba(255,255,255,.12);
                border-radius:6px;padding:7px 10px;font-size:11.5px;font-weight:600;
                letter-spacing:.2px;cursor:pointer;width:100%;
                box-shadow:0 1px 0 rgba(255,255,255,.18) inset,
                            0 1px 4px rgba(37,99,235,.45);
                display:flex;align-items:center;justify-content:center;gap:6px;
                transition:transform .12s ease,box-shadow .12s ease,filter .12s ease"
         onmouseover="this.style.filter='brightness(1.08)';this.style.transform='translateY(-1px)';this.style.boxShadow='0 1px 0 rgba(255,255,255,.22) inset,0 4px 10px rgba(37,99,235,.55)'"
         onmouseout="this.style.filter='';this.style.transform='';this.style.boxShadow='0 1px 0 rgba(255,255,255,.18) inset,0 1px 4px rgba(37,99,235,.45)'"
         title="CSV/PNG 다운로드 통합 모달 열기">
         <span style="font-size:13px;line-height:1">📥</span>
         <span>데이터 허브</span>
         <span style="font-weight:500;opacity:.85;font-size:10.5px;
                       background:rgba(255,255,255,.18);
                       padding:1px 6px;border-radius:10px;line-height:1.4">5종</span>
       </button>
     </div>`);

  /* Wire up buttons */
  const legendEl = document.getElementById('view-mode-legend');
  if (legendEl) {
    legendEl.querySelectorAll('[data-sed-filter]').forEach(b => {
      b.addEventListener('click', () => {
        const key = b.dataset.sedFilter;
        if (key === 'ALL') {
          state.seDiagFilter = {
            'percolating': true, 'articulation': true,
            'dead_top': true, 'dead_bot': true, 'bottleneck': true,
          };
        } else {
          state.seDiagFilter[key] = !state.seDiagFilter[key];
        }
        renderSeDiagnostics(state);
      });
    });
    /* Export buttons (CSV / PNG) — kept as fallback for any inline
     * markup that still uses data-sed-export; the legend now ships
     * a single "데이터 허브 열기" button which opens the unified
     * Z-profile Data Hub modal on the SE tab. */
    legendEl.querySelectorAll('[data-sed-export]').forEach(b => {
      b.addEventListener('click', () => exportSeDiagnostics(state, b));
    });
    const hubBtn = legendEl.querySelector('[data-sed-open-hub]');
    if (hubBtn) {
      hubBtn.addEventListener('click',
        () => showZProfileDataHub(state, 'se'));
    }
  }
}

/* ── SE Diagnostics: CSV + PNG exports ───────────────────────────────── */
function exportSeDiagnostics(state, btn) {
  const kind = btn.dataset.sedExport;
  const aux  = (state.data && state.data.aux) || {};
  const caseId = (state.data && state.data.case_id) || 'case';
  const perc     = new Set(aux.se_percolating || []);
  const artPts   = new Set(aux.se_articulation_points || []);
  const deadEnds = aux.se_dead_end_clusters || [];
  const bnEdges  = aux.se_bottleneck_edges || [];
  const seMesh   = state.meshes && state.meshes.SE;
  const deadEndType = {};
  deadEnds.forEach(d => d.ids.forEach(pid => { deadEndType[pid] = d.type; }));

  /* helper: CSV escape */
  const esc = v => {
    const s = String(v ?? '');
    return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  };
  const dl  = (rows, name) => {
    const txt = rows.map(r => r.map(esc).join(',')).join('\n') + '\n';
    saveBlobWithDialog(new Blob(['﻿' + txt], { type: 'text/csv' }),
                        name, btn, btn.textContent);
  };

  if (kind === 'csv_particles') {
    const rows = [['id', 'x', 'y', 'z', 'radius', 'role']];
    if (seMesh) {
      seMesh.userData.particles.forEach(p => {
        let role = 'isolated';
        if (artPts.has(p.id))                       role = 'articulation';
        else if (perc.has(p.id))                    role = 'percolating';
        else if (deadEndType[p.id] === 'top_only')  role = 'dead_top';
        else if (deadEndType[p.id] === 'bottom_only') role = 'dead_bot';
        rows.push([p.id, p.x, p.y, p.z, p.r || '', role]);
      });
    }
    dl(rows, `${caseId}_se_particles.csv`);
    return;
  }

  if (kind === 'csv_bn') {
    const rows = [['id1', 'id2', 'area_um2', 'area_norm', 'r_min_um']];
    bnEdges.forEach(e => {
      rows.push([e.id1, e.id2, e.area_um2 ?? '',
                  e.area_norm ?? '', e.r_min_um ?? '']);
    });
    /* Metadata row at top */
    const meta = [
      ['# median_norm', aux.se_bn_median_norm ?? ''],
      ['# threshold_norm', aux.se_bn_threshold_norm ?? ''],
      ['# n_bn_below_threshold', aux.se_n_bn_below_threshold ?? ''],
      [''],
    ];
    dl(meta.concat(rows), `${caseId}_se_bottleneck.csv`);
    return;
  }

  if (kind === 'csv_clusters') {
    const rows = [['cluster_idx', 'type', 'size', 'ids']];
    deadEnds.forEach((d, i) => {
      rows.push([i, d.type, d.size, (d.ids || []).join(';')]);
    });
    dl(rows, `${caseId}_se_deadend_clusters.csv`);
    return;
  }

  if (kind === 'png_zprofile') {
    /* Client-side canvas z-profile chart */
    const png = renderSeZProfilePNG(state);
    if (!png) {
      btn.textContent = '⚠ no data';
      setTimeout(() => { btn.textContent = '📥 PNG z-profile'; }, 1500);
      return;
    }
    // Convert dataURL to Blob and save
    const byteStr = atob(png.split(',')[1]);
    const ab = new ArrayBuffer(byteStr.length); const ia = new Uint8Array(ab);
    for (let i = 0; i < byteStr.length; i++) ia[i] = byteStr.charCodeAt(i);
    saveBlobWithDialog(new Blob([ab], { type: 'image/png' }),
                        `${caseId}_se_zprofile.png`, btn, btn.textContent);
    return;
  }

  if (kind === 'png_stats') {
    /* Fetch corpus stats (one-shot, cached on state) before rendering so
     * the card can show percentile context across all 27 percolating cases. */
    const finalize = (corpus) => {
      const png = renderSeStatsCardPNG(state, corpus);
      if (!png) return;
      const byteStr = atob(png.split(',')[1]);
      const ab = new ArrayBuffer(byteStr.length); const ia = new Uint8Array(ab);
      for (let i = 0; i < byteStr.length; i++) ia[i] = byteStr.charCodeAt(i);
      saveBlobWithDialog(new Blob([ab], { type: 'image/png' }),
                          `${caseId}_se_stats.png`, btn, btn.textContent);
    };
    if (state.seCorpus) {
      finalize(state.seCorpus);
    } else {
      fetch('/api/se_corpus.json').then(r => r.json()).then(j => {
        state.seCorpus = j.rows || [];
        finalize(state.seCorpus);
      }).catch(() => finalize(null));
    }
    return;
  }
}

/* ── Canvas-based z-profile chart (no backend, instant) ──────────────── */
function renderSeZProfilePNG(state) {
  const aux = (state.data && state.data.aux) || {};
  const box = (state.data && state.data.box) || {};
  const perc     = new Set(aux.se_percolating || []);
  const artPts   = new Set(aux.se_articulation_points || []);
  const bnEdges  = aux.se_bottleneck_edges || [];
  const deadEnds = aux.se_dead_end_clusters || [];
  const seMesh   = state.meshes && state.meshes.SE;
  if (!seMesh || !aux.se_n_percolating) return null;
  const deadTopIds = new Set();
  const deadBotIds = new Set();
  deadEnds.forEach(d => (d.ids || []).forEach(pid => {
    if (d.type === 'top_only')    deadTopIds.add(pid);
    if (d.type === 'bottom_only') deadBotIds.add(pid);
  }));

  /* Collect per-category z values (data-space z = particle.z) */
  const z_perc = [], z_cut = [], z_dtop = [], z_dbot = [];
  seMesh.userData.particles.forEach(p => {
    if (artPts.has(p.id))                       z_cut.push(p.z);
    else if (perc.has(p.id))                    z_perc.push(p.z);
    else if (deadTopIds.has(p.id))              z_dtop.push(p.z);
    else if (deadBotIds.has(p.id))              z_dbot.push(p.z);
  });
  /* bn edges: use midpoint z */
  const idIndex = {};
  seMesh.userData.particles.forEach(p => { idIndex[p.id] = p; });
  const z_bn = [];
  bnEdges.forEach(e => {
    const a = idIndex[e.id1], b = idIndex[e.id2];
    if (a && b) z_bn.push(0.5 * (a.z + b.z));
  });
  if (z_perc.length === 0 && z_cut.length === 0) return null;

  const z_min = box.z_min || 0;
  const z_max = box.z_max || Math.max(...z_perc, ...z_cut, 1);
  const n_bins = 25;
  const step = (z_max - z_min) / n_bins;
  const histogram = arr => {
    const h = new Array(n_bins).fill(0);
    arr.forEach(z => {
      const i = Math.max(0, Math.min(n_bins - 1, Math.floor((z - z_min) / step)));
      h[i]++;
    });
    return h;
  };
  const h_perc = histogram(z_perc);
  const h_cut  = histogram(z_cut);
  const h_bn   = histogram(z_bn);
  const h_dtop = histogram(z_dtop);
  const h_dbot = histogram(z_dbot);

  /* Canvas drawing */
  const W = 1100, H = 700;
  const cvs = document.createElement('canvas');
  cvs.width = W; cvs.height = H;
  const ctx = cvs.getContext('2d');
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = '#111';
  ctx.font = 'bold 16px serif';
  const caseId = (state.data && state.data.case_id) || 'case';
  ctx.fillText(`${caseId}  —  SE Network z-profile`, 16, 28);
  ctx.font = '11px serif';
  ctx.fillStyle = '#666';
  ctx.fillText(`box z = [${z_min.toFixed(1)}, ${z_max.toFixed(1)}] μm, `
                 + `${n_bins} bins, ${z_perc.length + z_cut.length + z_dtop.length + z_dbot.length} SE particles + ${z_bn.length} bn edges`,
                 16, 46);

  /* 3 horizontal-bar panels, side by side */
  const panelW = (W - 100) / 3, panelH = H - 100, panelY = 70;
  const panelX = i => 40 + i * panelW;
  const drawPanel = (col, title, layers) => {
    const x0 = panelX(col), y0 = panelY;
    /* axes */
    ctx.strokeStyle = '#999'; ctx.lineWidth = 1;
    ctx.strokeRect(x0, y0, panelW - 20, panelH);
    /* title */
    ctx.fillStyle = '#111'; ctx.font = 'bold 13px serif';
    ctx.fillText(title, x0, y0 - 10);
    /* z-axis labels */
    ctx.fillStyle = '#555'; ctx.font = '10px serif';
    ctx.fillText(z_min.toFixed(1), x0 - 26, y0 + panelH);
    ctx.fillText(z_max.toFixed(1), x0 - 26, y0 + 4);
    ctx.fillText('z (μm)', x0 - 30, y0 + panelH / 2);
    /* find max for x scaling */
    let maxV = 0;
    layers.forEach(L => L.data.forEach(v => { if (v > maxV) maxV = v; }));
    if (maxV === 0) maxV = 1;
    ctx.fillText(`max=${maxV}`, x0 + panelW - 60, y0 + panelH + 14);
    /* draw layered horizontal bars (stacked by layer order) */
    const binH = panelH / n_bins;
    layers.forEach(L => {
      ctx.fillStyle = L.color;
      ctx.globalAlpha = L.alpha;
      for (let i = 0; i < n_bins; i++) {
        const v = L.data[i];
        if (v <= 0) continue;
        const bx = x0 + 1;
        const by = y0 + panelH - (i + 1) * binH;
        const bw = ((panelW - 22) * v / maxV);
        ctx.fillRect(bx, by + 1, bw, binH - 2);
      }
    });
    ctx.globalAlpha = 1;
    /* legend */
    ctx.font = '10px serif';
    let ly = y0 + panelH + 30;
    layers.forEach(L => {
      ctx.fillStyle = L.color;
      ctx.fillRect(x0, ly - 8, 12, 10);
      ctx.fillStyle = '#222';
      ctx.fillText(`${L.name}  (n=${L.data.reduce((a,b)=>a+b,0)})`, x0 + 16, ly);
      ly += 14;
    });
  };

  drawPanel(0, '(a) Cut nodes', [
    { name: 'percolating', data: h_perc, color: '#14b8a6', alpha: 0.30 },
    { name: 'cut',         data: h_cut,  color: '#facc15', alpha: 0.92 },
  ]);
  drawPanel(1, '(b) Bottleneck + dead-end', [
    { name: 'bn edges',  data: h_bn,   color: '#dc2626', alpha: 0.85 },
    { name: 'dead-top',  data: h_dtop, color: '#ec4899', alpha: 0.70 },
    { name: 'dead-bot',  data: h_dbot, color: '#f97316', alpha: 0.70 },
  ]);
  /* Panel c: cut fraction per bin */
  const h_cf = h_cut.map((v, i) => (h_perc[i] + v) > 0
                                     ? v / (h_perc[i] + v) : 0);
  drawPanel(2, '(c) Local cut fraction', [
    { name: 'n_cut / (n_perc+n_cut)', data: h_cf.map(v => Math.round(v * 1000)),
      color: '#7c3aed', alpha: 0.85 },
  ]);
  /* footnote */
  ctx.fillStyle = '#555'; ctx.font = '10px serif';
  ctx.fillText('Bars: count per z-bin (panel c shows fraction ×1000).  '
                 + 'Y-axis: z (depth, μm) — bottom = z_min, top = z_max',
                 16, H - 12);
  return cvs.toDataURL('image/png');
}

/* ── Canvas-based stats summary card ─────────────────────────────────── */
function renderSeStatsCardPNG(state, corpusRows) {
  const aux = (state.data && state.data.aux) || {};
  const perc     = aux.se_percolating || [];
  const artPts   = aux.se_articulation_points || [];
  const bnEdges  = aux.se_bottleneck_edges || [];
  const deadEnds = aux.se_dead_end_clusters || [];
  const nPerc = perc.length;
  if (!nPerc) return null;

  const deadTop = deadEnds.filter(d => d.type === 'top_only').length;
  const deadBot = deadEnds.filter(d => d.type === 'bottom_only').length;
  const narrowest = bnEdges[0]?.area_um2;
  const narrowestNorm = bnEdges[0]?.area_norm;
  const medianNorm = aux.se_bn_median_norm;
  const thresholdNorm = aux.se_bn_threshold_norm;
  const nBnBelow = aux.se_n_bn_below_threshold;

  /* Per-case derived metrics matching the corpus figure axes */
  const cutFrac = artPts.length / nPerc;

  /* Find this case's row in corpus + compute percentile rank */
  const caseId = (state.data && state.data.case_id) || 'case';
  let corpusRow = null, corpusPerc = null;
  if (corpusRows && corpusRows.length) {
    corpusRow = corpusRows.find(r => r.case_id === caseId);
    /* Only use cases with valid percolating data */
    const valid = corpusRows.filter(r => +r.n_percolating > 0);
    const rank = (key, val) => {
      const arr = valid.map(r => +r[key])
                       .filter(v => Number.isFinite(v))
                       .sort((a, b) => a - b);
      if (!arr.length) return null;
      let i = 0; while (i < arr.length && arr[i] < val) i++;
      return { pct: Math.round(100 * i / arr.length),
               lo: arr[0], hi: arr[arr.length - 1],
               med: arr[Math.floor(arr.length / 2)],
               n: arr.length };
    };
    corpusPerc = {
      cutFrac: rank('cut_fraction', cutFrac),
    };
    /* Compute bn_below_frac = n_bn_below_threshold / n_perc_edges
     * (the panel-b metric).  Add a synthetic field to each row. */
    const arrBnFrac = valid.map(r => {
      const ne = +r.n_perc_edges; const nb = +r.n_bn_below_threshold;
      return (ne > 0 && Number.isFinite(nb)) ? nb / ne : NaN;
    }).filter(v => Number.isFinite(v)).sort((a, b) => a - b);
    const myBnFrac = corpusRow ? (() => {
      const ne = +corpusRow.n_perc_edges; const nb = +corpusRow.n_bn_below_threshold;
      return (ne > 0 && Number.isFinite(nb)) ? nb / ne : null;
    })() : null;
    if (myBnFrac != null && arrBnFrac.length) {
      let i = 0; while (i < arrBnFrac.length && arrBnFrac[i] < myBnFrac) i++;
      corpusPerc.bnFrac = {
        val: myBnFrac, pct: Math.round(100 * i / arrBnFrac.length),
        lo: arrBnFrac[0], hi: arrBnFrac[arrBnFrac.length - 1],
        med: arrBnFrac[Math.floor(arrBnFrac.length / 2)],
        n: arrBnFrac.length,
      };
    }
  }

  /* Canvas — taller now to fit corpus section */
  const W = 800, H = corpusRow ? 760 : 480;
  const cvs = document.createElement('canvas');
  cvs.width = W; cvs.height = H;
  const ctx = cvs.getContext('2d');
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = '#0f172a';
  ctx.font = 'bold 20px serif';
  ctx.fillText(`SE Network Diagnostics  —  ${caseId}`, 30, 40);

  /* ── Section 1: per-case raw counts ───────────────────────────────── */
  ctx.font = 'bold 13px serif'; ctx.fillStyle = '#444';
  ctx.fillText('Per-case', 30, 70);
  const rows1 = [
    ['Percolating SE (backbone)',        nPerc,                  '#14b8a6'],
    ['Articulation points (cut nodes)',  artPts.length,          '#facc15'],
    ['  cut fraction = n_cut / n_perc',  cutFrac.toFixed(4),     '#facc15'],
    ['Dead-end clusters — top only',     `${deadTop} cluster`,   '#ec4899'],
    ['Dead-end clusters — bottom only',  `${deadBot} cluster`,   '#f97316'],
    ['Bottleneck contacts (capped list)', bnEdges.length,        '#dc2626'],
    ['Below-threshold bn (uncapped)',    nBnBelow ?? '—',        '#dc2626'],
    ['Narrowest A/r²',                   typeof narrowestNorm === 'number'
                                            ? narrowestNorm.toFixed(5) : '—', '#dc2626'],
    ['Narrowest area',                   typeof narrowest === 'number'
                                            ? narrowest.toFixed(5) + ' μm²' : '—', '#dc2626'],
    ['Corpus median A/r² (this case)',   typeof medianNorm === 'number'
                                            ? medianNorm.toFixed(4) : '—', '#444'],
    ['bn threshold (10% of median)',     typeof thresholdNorm === 'number'
                                            ? thresholdNorm.toFixed(4) : '—', '#444'],
  ];
  ctx.font = '14px serif';
  rows1.forEach((r, i) => {
    const y = 95 + i * 28;
    ctx.fillStyle = r[2]; ctx.fillRect(30, y - 12, 12, 14);
    ctx.fillStyle = '#222'; ctx.fillText(String(r[0]), 52, y);
    ctx.font = 'bold 14px serif'; ctx.fillStyle = '#0f172a';
    ctx.fillText(String(r[1]), 510, y);
    ctx.font = '14px serif';
  });

  /* ── Section 2: corpus comparison ─────────────────────────────────── */
  if (corpusRow) {
    const y0 = 95 + rows1.length * 28 + 14;
    ctx.font = 'bold 13px serif'; ctx.fillStyle = '#444';
    ctx.fillText(`Corpus context (${corpusPerc.cutFrac.n} percolating cases)`, 30, y0);

    /* composition values from corpus row */
    const comp = [
      ['campaign',  corpusRow.campaign || '—'],
      ['φ_SE',      (+corpusRow.phi_SE).toFixed(3)],
      ['λ_eff',     (+corpusRow.lam_eff).toFixed(2)],
      ['AM wt%',    (+corpusRow.am_wt).toFixed(1)],
    ];
    ctx.font = '12px serif';
    comp.forEach((c, i) => {
      const x = 30 + i * 180;
      ctx.fillStyle = '#666'; ctx.fillText(c[0], x, y0 + 22);
      ctx.fillStyle = '#0f172a'; ctx.font = 'bold 13px serif';
      ctx.fillText(c[1], x, y0 + 40);
      ctx.font = '12px serif';
    });

    /* Percentile rank bars (cut_fraction, bn_below_frac) */
    const drawRank = (yy, label, p, color) => {
      ctx.fillStyle = '#222'; ctx.font = '12px serif';
      ctx.fillText(label, 30, yy);
      /* bar */
      const bx = 30, bw = 480, by = yy + 6, bh = 14;
      ctx.fillStyle = '#e5e7eb'; ctx.fillRect(bx, by, bw, bh);
      /* fill up to percentile */
      ctx.fillStyle = color;
      ctx.fillRect(bx, by, bw * p.pct / 100, bh);
      /* tick at 50% */
      ctx.fillStyle = '#9ca3af';
      ctx.fillRect(bx + bw / 2, by - 2, 1, bh + 4);
      /* label */
      ctx.font = 'bold 12px serif'; ctx.fillStyle = '#0f172a';
      ctx.fillText(`p${p.pct} (val=${p.val != null ? p.val.toFixed(4)
                                                      : p.med.toFixed(4)})`,
                    bx + bw + 10, by + 11);
      ctx.font = '10px serif'; ctx.fillStyle = '#666';
      ctx.fillText(`corpus [min, med, max] = [${p.lo.toFixed(4)}, `
                     + `${p.med.toFixed(4)}, ${p.hi.toFixed(4)}]`,
                    bx, by + bh + 14);
    };
    const cP = corpusPerc.cutFrac;
    cP.val = cutFrac;
    drawRank(y0 + 80,  '★ cut_fraction (lower = more robust topology)',
              cP, '#facc15');
    if (corpusPerc.bnFrac) {
      drawRank(y0 + 140, '★ bn_below_frac (lower = fewer narrow contacts)',
                corpusPerc.bnFrac, '#dc2626');
    }
  }

  ctx.fillStyle = '#666'; ctx.font = '11px serif';
  ctx.fillText('Generated from 3D viewer SE diagnostic mode.  '
                 + 'Bars: where this case sits among percolating cases.',
                 30, H - 18);
  return cvs.toDataURL('image/png');
}

function setLegend(state, html) {
  const el = document.getElementById('view-mode-legend');
  if (el) el.innerHTML = html;
}

/* ── 반응 ↔ 기계(SE 소성변형·접촉) 공간 상관 팝업 ────────────────
 * Server-rendered figure (scripts/mech_reaction_correlation.py via
 * /mpm-lab/mech-reaction/<pid>.png).  OBSERVATIONAL: the model has NO
 * stress→reaction coupling — j_rxn–coverage is causal (contact = BV area),
 * j_rxn–strain is co-location at the separator side. */
function showMechReactionModal(state) {
  const du = state._dataUrl || '';
  if (!du.includes('/mpm-lab/data/')) {
    alert('반응↔변형 상관은 mpm-lab 저장 payload에서만 지원돼요 (현재 뷰는 미지원).');
    return;
  }
  const base = du.replace('/mpm-lab/data/', '/mpm-lab/mech-reaction/').split('?')[0];
  const png = base + '.png', csv = base + '.csv';
  const ov = document.createElement('div');
  ov.className = 'path-modal-overlay';
  ov.innerHTML =
    `<div class="path-modal" style="max-width:95vw">
      <div style="font-weight:bold;text-align:center;margin-bottom:6px">📊 반응 ↔ 기계(응력/변형·접촉) 공간 상관
        <span style="font-weight:400;color:#666;font-size:12px">— 관찰용 (모델에 응력→반응 커플링 없음)</span></div>
      <img src="${png}" alt="reaction vs mechanics correlation" style="background:#fff"
           onerror="this.insertAdjacentHTML('afterend','<div style=color:#b91c1c;padding:10px>그림 생성 실패 — 이 payload에 j_rxn/strain 데이터가 없을 수 있어요.</div>');this.remove();">
      <div class="path-modal-info">j_rxn–coverage = 접촉(=BV 반응면적) 링크 <b>(z-통제·within-slice 생존)</b> · j_rxn–strain = 분리막쪽 <b>공존</b>(인과 아님)</div>
      <div class="path-modal-actions">
        <a href="${csv}" download style="text-decoration:none;padding:5px 12px;background:#1f2937;color:#e5e7eb;border-radius:6px;font-size:13px">CSV ⬇</a>
        <a href="${png}" download style="text-decoration:none;padding:5px 12px;background:#1f2937;color:#e5e7eb;border-radius:6px;font-size:13px">PNG ⬇</a>
        <button style="padding:5px 14px;background:#374151;color:#e5e7eb;border:none;border-radius:6px;cursor:pointer;font-size:13px">닫기</button>
      </div>
    </div>`;
  const close = () => { ov.remove(); document.removeEventListener('keydown', onEsc); };
  const onEsc = (e) => { if (e.key === 'Escape') close(); };
  ov.addEventListener('click', (e) => { if (e.target === ov) close(); });
  ov.querySelector('.path-modal-actions button').addEventListener('click', close);
  document.addEventListener('keydown', onEsc);
  // no stacking: drop any prior mech-reaction modal before opening this one
  document.querySelectorAll('.path-modal-overlay[data-mech="1"]').forEach((e) => e.remove());
  ov.dataset.mech = '1';
  document.body.appendChild(ov);
}

/* ── MPM 분석 요약 (Analysis Summary) ──────────────────────────
 * Client-side, payload-only (no server round-trip).  One paper-style
 * small-multiples canvas: 전체 분포 (histograms over ALL AM), z별 분포
 * (depth profiles), 손실분담 bars + transport scalars.  Works on any
 * payload that already carries per-AM je/coverage/r/z + step3/econn. */
function showMPMAnalysisSummary(state) {
  const AMs = [];
  ['AM_P', 'AM_S'].forEach(ty => {
    const m = state.meshes && state.meshes[ty];
    if (m && m.userData && m.userData.particles) m.userData.particles.forEach(p => AMs.push(p));
  });
  const mm = (state.data && state.data.mpm_metrics) || {};
  const s3 = mm.step3 || (state.data && state.data.step3) || {};
  const ec = mm.econn_summary || (state.data && state.data.econn_summary) || {};
  const caseName = (state.data && state.data.case) || 'MPM 전극';
  const num = (arr) => arr.filter(v => v !== undefined && v !== null && isFinite(v));
  const covOf = (p) => (p.coverage == null ? NaN : (p.coverage <= 1 ? p.coverage * 100 : p.coverage));
  const jeV = num(AMs.map(p => p.je));
  const covPctAll = num(AMs.map(covOf));
  const rV = num(AMs.map(p => p.r));
  const porosity = (mm.porosity_mpm_pct != null ? mm.porosity_mpm_pct
    : mm.porosity_settled_pct != null ? mm.porosity_settled_pct : mm.porosity_at_target_pct);
  const thickness = (mm.thickness_um != null ? mm.thickness_um : mm.thickness_mpm_um);
  const zMax = Math.max(thickness || 0, ...AMs.map(p => p.z).filter(isFinite), 1);
  // shared 12-bin z-profile used by BOTH the depth charts AND the summary CSV (one source of truth)
  const NB = 12;
  const zbins = Array.from({ length: NB }, (_, i) =>
    ({ z_lo: zMax * i / NB, z_hi: zMax * (i + 1) / NB, jeS: 0, covS: 0, ecS: 0, n: 0, ecN: 0 }));
  AMs.forEach(p => {
    if (!isFinite(p.z)) return;
    const b = zbins[Math.min(NB - 1, Math.floor(p.z / zMax * NB))]; b.n++;
    if (isFinite(p.je)) b.jeS += p.je;
    const cv = covOf(p); if (isFinite(cv)) b.covS += cv;
    if (p.econn !== undefined) { b.ecS += p.econn; b.ecN++; }
  });
  const zJe = zbins.map(b => b.n ? b.jeS / b.n : 0);
  const zCov = zbins.map(b => b.n ? b.covS / b.n : 0);
  const zCnt = zbins.map(b => b.n);
  const zEc = zbins.map(b => b.ecN ? b.ecS / b.ecN : 0);

  // 칩(스칼라) — 집전체 시나리오는 SAME 구조 payload들이 갈리는 유일한 축이라 반드시 노출
  // (bare↔C-SUS 요약이 "차이 없음"으로 보이던 문제: 벌크는 동일한 게 물리 정답, 다른 건 이 두 칩).
  const selC = (s3.collector || {}).selected;
  const pore = s3.pore || {};                                // A6 pore-τ (payload step3.pore)
  const dAll = (mm.additive_dispersion || {}).conductive_all || {};   // A5 분산 (VGCF+SuperP+SDCP 합)
  const fse = s3.field_scale_e || {}, fsi = s3.field_scale_ion || {}, rxn = s3.rxn || {};  // 전류밀도장·STEP4
  const chips = [
    ['σ_e_eff (전자전도도·벌크)', s3.sigma_e_eff_S_cm != null ? Number(s3.sigma_e_eff_S_cm).toExponential(2) + ' S/cm' : '—'],
    ['σ_ion_eff (이온전도도)', s3.sigma_ion_eff_S_cm != null ? Number(s3.sigma_ion_eff_S_cm).toExponential(2) + ' S/cm' : '—'],
    ['R_geom (기하 계면저항)', (s3.collector_geometric && s3.collector_geometric.R_geom_ohm_cm2 != null) ? Number(s3.collector_geometric.R_geom_ohm_cm2).toExponential(2) + ' Ω·cm²' : '—'],
    ['porosity (공극률)', porosity != null ? Number(porosity).toFixed(2) + ' %' : '—'],
    ['thickness (두께)', thickness != null ? Number(thickness).toFixed(1) + ' µm' : '—'],
    ['N (AM 입자수)', String(mm.n_AM || AMs.length)],
    ['econn 연결', ec.connected_pct != null ? Number(ec.connected_pct).toFixed(1) + ' %' : '—'],
    ['carbon clusters', ec.n_carbon_clusters != null ? String(ec.n_carbon_clusters) : '—'],
    ['Coverage (AM 표면 SE 덮임)', (() => {
      // AM_P/AM_S 중 실제 존재하는(>0) 쪽 채택.  ?? 는 0을 통과시켜 버그였음
      // (mono-AM_P payload에선 coverage_AM_S_*=0.0 → H0.0/T0.0 로 나왔음).
      const pick = (a, b) => {
        const av = (typeof a === 'number' && a > 0) ? a : null;
        const bv = (typeof b === 'number' && b > 0) ? b : null;
        if (av != null && bv != null) return { p: av, s: bv };   // bimodal → 둘 다
        return av != null ? av : bv;                             // mono → 스칼라
      };
      const H = pick(mm.coverage_AM_P_hertz_pct, mm.coverage_AM_S_hertz_pct);   // 이온-유효 (≤0.13µm)
      const T = pick(mm.coverage_AM_P_tabor_pct, mm.coverage_AM_S_tabor_pct);   // 소성-퍼짐 (≤0.26µm)
      const f = v => (v && typeof v === 'object') ? ('P' + v.p.toFixed(0) + '/S' + v.s.toFixed(0)) : v.toFixed(1);
      if (H != null || T != null) {
        const parts = [];
        if (H != null) parts.push('Hertz ' + f(H) + '%');
        if (T != null) parts.push('Tabor ' + f(T) + '%');
        return parts.join(' / ');
      }
      const mu = covPctAll.length ? covPctAll.reduce((a, b) => a + b, 0) / covPctAll.length : null;  // fallback = 패널②
      return mu != null ? '⟨µ⟩ ' + mu.toFixed(1) + '%' : '—';
    })()],
    ['집전체 (시나리오 부하)', selC ? selC.name + ' · R_int ' + selC.R_int_ohm_cm2 + ' Ω·cm²' : '이상 접촉 (R_int 0)'],
    ['σ_apparent (전자·계면 포함)', selC && selC.sigma_apparent_S_cm != null
      ? Number(selC.sigma_apparent_S_cm).toExponential(2) + ' S/cm'
      : (s3.sigma_e_eff_S_cm != null ? '= σ_e_eff (이상 접촉)' : '—')],
    ['pore-τ (기공 확산굴곡·구조)', pore.tau != null
      ? Number(pore.tau).toFixed(2) + ' (ε ' + pore.eps_total_pct + '%)'
      : (pore.eps_total_pct != null ? '비퍼콜 · ε ' + pore.eps_total_pct + '% (기공 폐색)' : '—')],
    ['첨가제→SE 거리 (분산)', dAll.nn_med_um != null
      ? dAll.nn_med_um + ' µm (×' + dAll.nn_clustering + ' vs random)' : '—'],
    ['전류 집중 e (p99.8/⟨J⟩)', fse.focus_top != null ? '×' + Number(fse.focus_top).toPrecision(3) + ' ⟨J⟩' : '—'],
    ['전류 집중 ion (p99.8/⟨J⟩)', fsi.focus_top != null ? '×' + Number(fsi.focus_top).toPrecision(3) + ' ⟨J⟩' : '—'],
    ['면적용량 (자동산출)', fse.areal_capacity_mAh_cm2 != null
      ? Number(fse.areal_capacity_mAh_cm2).toFixed(2) + ' mAh/cm² · 1C ' + Number(fse.j_1C_mA_cm2).toFixed(2) + ' mA/cm²' : '—'],
    ['반응 계면 (BV faces)', rxn.n_bv_faces != null
      ? Number(rxn.n_bv_faces).toLocaleString() + (rxn.active_am_pct != null ? ' · active ' + rxn.active_am_pct + '%' : '') : '—'],
    ['SE/solid · ρ_bulk', mm.SE_of_solid_pct != null
      ? Number(mm.SE_of_solid_pct).toFixed(1) + '% · ' + (mm.bulk_density_g_cm3 != null ? Number(mm.bulk_density_g_cm3).toFixed(2) + ' g/cm³' : '—') : '—'],
  ];
  // 창이 캔버스(고정 1080)보다 좁으면 브라우저가 비정수 축소를 해 글자가 뭉개짐 → 표시 폭에
  // 맞춰 그리기 (DPR=2 비트맵이 CSS 폭과 1:1 → 항상 crisp).  레이아웃은 전부 W에서 파생됨.
  const W = Math.max(780, Math.min(1080, (window.innerWidth || 1240) - 170)), pad = 18, cols = 3;
  const colW = (W - pad * (cols + 1)) / cols;
  const cellH = 198, vgap = 26, top0 = 46;
  const headH = Math.ceil(chips.length / 4) * 56 + 8;
  const gridTop = top0 + headH, gridH = 3 * cellH + 2 * vgap;
  const glossY = gridTop + gridH + 22, glossH = 232;         // 12 entries × 15.5px + header
  const H = glossY + glossH + 14;
  const cvs = document.createElement('canvas');
  const DPR = 2; cvs.width = W * DPR; cvs.height = H * DPR;
  const ctx = cvs.getContext('2d'); ctx.scale(DPR, DPR);
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, W, H);

  const fmtNum = (v) => {
    if (v === 0) return '0';
    const a = Math.abs(v);
    if (a >= 1e4 || a < 1e-2) return v.toExponential(1);
    if (a >= 100) return v.toFixed(0);
    if (a >= 1) return v.toFixed(1);
    return v.toFixed(2);
  };
  const median = (a) => {
    if (!a.length) return NaN;
    const s = [...a].sort((x, y) => x - y), m = Math.floor(s.length / 2);
    return s.length % 2 ? s[m] : 0.5 * (s[m - 1] + s[m]);
  };
  function roundRect(x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  const cellXY = (idx) => [pad + (idx % cols) * (colW + pad), gridTop + Math.floor(idx / cols) * (cellH + vgap)];
  // frame = title + subtitle(unit·stats, no more overlap) + faint gridlines + axes → plot rect
  function frame(x, y, title, subtitle) {
    ctx.textAlign = 'left';
    ctx.fillStyle = '#111827'; ctx.font = 'bold 12.5px sans-serif'; ctx.fillText(title, x, y + 14);
    if (subtitle) { ctx.fillStyle = '#9ca3af'; ctx.font = '10px sans-serif'; ctx.fillText(subtitle, x, y + 29); }
    const px = x + 8, py = y + 40, pw = colW - 16, ph = cellH - 60;
    ctx.strokeStyle = '#f1f3f5'; ctx.lineWidth = 1;
    for (let g = 1; g <= 3; g++) { const gy = py + ph * g / 4; ctx.beginPath(); ctx.moveTo(px, gy); ctx.lineTo(px + pw, gy); ctx.stroke(); }
    ctx.strokeStyle = '#d1d5db';
    ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px, py + ph); ctx.lineTo(px + pw, py + ph); ctx.stroke();
    return [px, py, pw, ph];
  }
  function note(x, y, title, sub, msg) {
    ctx.textAlign = 'left'; ctx.fillStyle = '#111827'; ctx.font = 'bold 12.5px sans-serif'; ctx.fillText(title, x, y + 14);
    if (sub) { ctx.fillStyle = '#9ca3af'; ctx.font = '10px sans-serif'; ctx.fillText(sub, x, y + 29); }
    ctx.fillStyle = '#9ca3af'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText(msg, x + colW / 2, y + cellH / 2 + 6); ctx.textAlign = 'left';
  }
  function xticks(px, py, pw, ph, lo, hi, mid) {
    ctx.fillStyle = '#6b7280'; ctx.font = '9px sans-serif';
    ctx.textAlign = 'left'; ctx.fillText(lo, px, py + ph + 12);
    if (mid !== undefined) { ctx.textAlign = 'center'; ctx.fillText(mid, px + pw / 2, py + ph + 12); }
    ctx.textAlign = 'right'; ctx.fillText(hi, px + pw, py + ph + 12); ctx.textAlign = 'left';
  }
  function hist(idx, vals, title, unit, color) {
    const [x, y] = cellXY(idx);
    if (!vals.length) { note(x, y, title, unit, 'STEP3/데이터 없음'); return; }
    const lo = Math.min(...vals), hi = Math.max(...vals);
    const mean = vals.reduce((a, b) => a + b, 0) / vals.length, med = median(vals);
    if (hi - lo <= Math.abs(hi) * 1e-6) {                    // degenerate single value (mono-size AM)
      note(x, y, title, `${unit} · n ${vals.length}`, `단일값 ${fmtNum(lo)} (모든 입자 동일)`); return;
    }
    const [px, py, pw, ph] = frame(x, y, title, `${unit} · μ ${fmtNum(mean)} · med ${fmtNum(med)} · n ${vals.length}`);
    const nb = 24, span = hi - lo, bins = new Array(nb).fill(0);
    vals.forEach(v => { bins[Math.min(nb - 1, Math.floor((v - lo) / span * nb))]++; });
    const mx = Math.max(...bins) || 1, bw = pw / nb;
    ctx.fillStyle = color;
    bins.forEach((b, i) => { const bh = b / mx * ph; ctx.fillRect(px + i * bw + 0.5, py + ph - bh, Math.max(0.5, bw - 1), bh); });
    const mxp = px + (med - lo) / span * pw;                 // median dashed marker
    ctx.strokeStyle = '#111827'; ctx.setLineDash([3, 3]); ctx.beginPath(); ctx.moveTo(mxp, py); ctx.lineTo(mxp, py + ph); ctx.stroke(); ctx.setLineDash([]);
    xticks(px, py, pw, ph, fmtNum(lo), fmtNum(hi), fmtNum((lo + hi) / 2));
  }
  function zprof(idx, yv, title, unit, color) {
    const [x, y] = cellXY(idx);
    if (!yv.some(v => v > 0)) { note(x, y, title, unit, 'STEP3/데이터 없음'); return; }
    const ymx = Math.max(...yv, 1e-30);
    const [px, py, pw, ph] = frame(x, y, title, `${unit} · max ${fmtNum(ymx)}`);
    const bw = pw / yv.length;
    ctx.fillStyle = color;
    yv.forEach((v, i) => { const bh = v / ymx * ph; ctx.fillRect(px + i * bw + 0.5, py + ph - bh, Math.max(0.5, bw - 1), bh); });
    xticks(px, py, pw, ph, '0 하단', fmtNum(zMax) + 'µm 압축면');
  }
  function bars(idx, entries, title, unit) {
    const [x, y] = cellXY(idx);
    const es = Object.entries(entries || {}).filter(([k, v]) => isFinite(v) && v > 0).sort((a, b) => b[1] - a[1]);
    if (!es.length) { note(x, y, title, unit, '데이터 없음'); return; }
    const [px, py, pw, ph] = frame(x, y, title, unit);
    const rh = Math.min(30, (ph - 4) / es.length), gp = Math.min(9, rh * 0.3);
    const palb = ['#2563eb', '#dc2626', '#16a34a', '#d97706', '#7c3aed', '#0891b2'];
    es.forEach(([k, v], i) => {
      const yy = py + i * rh + 2, bh = rh - gp;
      ctx.fillStyle = palb[i % palb.length]; roundRect(px, yy, Math.max(2, v * pw), bh, 2); ctx.fill();
      ctx.fillStyle = '#111827'; ctx.font = '11px sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(`${k}  ${(100 * v).toFixed(1)}%`, px + 5, yy + bh - 4);
    });
  }

  // ---- header + scalar chips ----
  ctx.fillStyle = '#111827'; ctx.font = 'bold 17px sans-serif'; ctx.textAlign = 'left';
  ctx.fillText('분석 요약 — ' + caseName + (s3.vox_um != null ? '   (STEP3 vox ' + s3.vox_um + 'µm)' : ''), pad, 27);
  const chipGap = 10, chipW = (W - pad * 2 - chipGap * 3) / 4, chipH = 48;
  chips.forEach((c, i) => {
    const x = pad + (i % 4) * (chipW + chipGap), y = top0 + Math.floor(i / 4) * (chipH + 8);
    ctx.fillStyle = '#f6f7f9'; roundRect(x, y, chipW, chipH, 7); ctx.fill();
    ctx.strokeStyle = '#eceef1'; ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = '#6b7280'; ctx.font = '10.5px sans-serif'; ctx.textAlign = 'left'; ctx.fillText(c[0], x + 11, y + 18);
    ctx.fillStyle = '#111827';
    let fs = 15;                                             // 긴 값(집전체 이름 등)은 칩 폭에 맞게 자동 축소
    ctx.font = `bold ${fs}px sans-serif`;
    while (fs > 10 && ctx.measureText(c[1]).width > chipW - 22) { fs -= 0.5; ctx.font = `bold ${fs}px sans-serif`; }
    ctx.fillText(c[1], x + 11, y + 38);
  });

  // ---- 9 charts: 전체 분포 / z별 분포 / 손실분담 ----
  hist(0, jeV, '① |J_z| 전자전류밀도 분포 (전체 AM)', '상대 |J_z|', '#dc2626');
  hist(1, covPctAll, '② Coverage 분포 (AM 표면 SE 덮임)', 'coverage %', '#2563eb');
  hist(2, rV, '③ 입자 반경 r 분포', 'r µm', '#16a34a');
  zprof(3, zJe, '④ 평균 |J_z| vs z (깊이 프로파일)', '⟨|J_z|⟩ 상대', '#dc2626');
  zprof(4, zCov, '⑤ 평균 coverage vs z', '⟨coverage⟩ %', '#2563eb');
  zprof(5, zCnt, '⑥ AM 입자 수 vs z', 'count', '#6b7280');
  bars(6, s3.dissipation_share, '⑦ 전자 손실(발열) 분담', '각 상의 전력손실 %');
  bars(7, s3.ion_dissipation_share, '⑧ 이온 손실 분담 (Li⁺ 경로)', '각 상의 전력손실 %');
  zprof(8, zEc, '⑨ 집전체 연결 비율 vs z', '연결 fraction 0–1', '#7c3aed');

  // ---- 약어 (abbreviations) ----
  ctx.fillStyle = '#f6f7f9'; roundRect(pad, glossY, W - 2 * pad, glossH, 8); ctx.fill();
  ctx.strokeStyle = '#eceef1'; ctx.lineWidth = 1; ctx.stroke();
  ctx.textAlign = 'left'; ctx.fillStyle = '#374151'; ctx.font = 'bold 12px sans-serif';
  ctx.fillText('약어 (abbreviations) — STEP3 = 전도상 복셀 Kirchhoff σ 저항망 솔브', pad + 12, glossY + 20);
  const gloss = [
    ['|J_z| , je', '전자 전류밀도(z방향) · STEP3 AM 입자별 상대값(자기 p99.8 정규화, 같은 payload 내 비교) · je=wetted/primer 집전체 기준'],
    ['jb', 'bare 집전체(crown 접점만) 기준 |J_z| · je와의 차 = 바닥 접점 상실 시 전류 재분배'],
    ['σ_e_eff / σ_ion_eff', '유효 전자 / 이온 전도도 (S/cm) · 전극 through-plane'],
    ['R_geom', '모델 기하 계면저항 (Ω·cm²) = L·(1/σ_bare − 1/σ_wetted) · 측정 R_int − R_geom = 화학/열화 몫'],
    ['coverage', 'AM 입자 표면이 SE로 덮인 비율 (%)'],
    ['econn', '집전체에 전기 연결(1) / 고립(0) · 100% = 모든 AM이 외부회로 도달'],
    ['z / 손실분담', 'z = 두께방향(0 하단 집전체 ~ 상단 압축면) · 손실(발열)분담 = 각 상의 전력손실 % (∝ J²·R)'],
    ['pore-τ', '기공(void)상 유효확산 tortuosity (D_eff/D0 = ε/τ) · 구조 지표 — Li⁺ 수송 τ 아님(수송은 SE 접촉망 σ_ion) · 비퍼콜 = 기공 폐색(기체 불투과)'],
    ['분산 D / nn', 'D = 셀별 첨가제 점수 분산/평균(AM-마스킹, 랜덤=1·응집↑, 같은 phase run간 비교) · nn = SE→최근접 첨가제 거리(µm), ×N = 동밀도 랜덤 대비'],
    ['전류 집중 (focus)', '|J|(p99.8)/⟨J_z⟩ · 전류 쏠림 무차원 지표(선형해라 바이어스 무관) · 낮을수록 균일=병목 해소 · 운전 국소 mA/cm² = focus×면적전류×C'],
    ['면적용량 / BV faces', '면적용량 = F·c_max·|Δx|·V_AM/면적 (Chen2020 창, 자동산출); 1C 전류밀도 = 면적용량/1h · BV faces = AM|SE·AM|SDCP 반응계면 수(STEP4), active% = 반응 참여 입자'],
    ['SE/solid · ρ_bulk', 'SE 부피 / 전 고체상 % · ρ_bulk = 침대 벌크 밀도 (g/cm³)'],
  ];
  gloss.forEach((g, i) => {
    const gy = glossY + 40 + i * 15.5;
    ctx.fillStyle = '#111827'; ctx.font = 'bold 11px sans-serif'; ctx.textAlign = 'left'; ctx.fillText(g[0], pad + 12, gy);
    ctx.fillStyle = '#4b5563'; ctx.font = '11px sans-serif'; ctx.fillText(g[1], pad + 130, gy);
  });

  // ---- CSV builders (client-side, no server round-trip) ----
  const csv = (v) => {
    if (v == null || (typeof v === 'number' && !isFinite(v))) return '';
    const s = String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  };
  function perAMCsv() {
    const out = ['id,type,x_um,y_um,z_um,r_um,coverage_pct,je_rel,jb_rel,econn'];
    AMs.forEach(p => out.push([p.id, p.type, p.x, p.y, p.z, p.r,
      (isFinite(covOf(p)) ? +covOf(p).toFixed(3) : ''), p.je, p.jb, p.econn].map(csv).join(',')));
    return out.join('\n');
  }
  function summaryCsv() {
    const out = ['section,key,v1,v2,v3,v4,v5,v6'];
    const row = (...vs) => out.push(vs.map(csv).join(','));
    row('case', 'name', caseName);
    row('scalar', 'sigma_e_eff_S_cm', s3.sigma_e_eff_S_cm);
    row('scalar', 'sigma_ion_eff_S_cm', s3.sigma_ion_eff_S_cm);
    row('scalar', 'R_geom_ohm_cm2', s3.collector_geometric && s3.collector_geometric.R_geom_ohm_cm2);
    row('scalar', 'porosity_pct', porosity);
    row('scalar', 'thickness_um', thickness);
    row('scalar', 'n_AM', mm.n_AM || AMs.length);
    row('scalar', 'econn_connected_pct', ec.connected_pct);
    row('scalar', 'carbon_clusters', ec.n_carbon_clusters);
    row('scalar', 'step3_vox_um', s3.vox_um);
    row('scalar', 'collector_selected', selC ? selC.name : 'ideal_R0');
    row('scalar', 'collector_R_int_ohm_cm2', selC ? selC.R_int_ohm_cm2 : 0);
    row('scalar', 'sigma_apparent_S_cm', selC ? selC.sigma_apparent_S_cm : s3.sigma_e_eff_S_cm);
    row('scalar', 'pore_tau', pore.tau);                     // A6 (null = 비퍼콜 기공)
    row('scalar', 'pore_eps_total_pct', pore.eps_total_pct);
    row('scalar', 'pore_eps_connected_pct', pore.eps_connected_pct);
    row('scalar', 'pore_D_rel', pore.D_rel);
    row('scalar', 'focus_top_e', fse.focus_top);             // 전류밀도장 (field_scale)
    row('scalar', 'focus_top_ion', fsi.focus_top);
    row('scalar', 'j_mean_e_A_cm2_per_V', fse.j_mean_z_A_cm2_per_V);
    row('scalar', 'j_mean_ion_A_cm2_per_V', fsi.j_mean_z_A_cm2_per_V);
    row('scalar', 'areal_capacity_mAh_cm2', fse.areal_capacity_mAh_cm2);
    row('scalar', 'j_1C_mA_cm2', fse.j_1C_mA_cm2);
    row('scalar', 'rxn_n_bv_faces', rxn.n_bv_faces);         // STEP4 반응 계면
    row('scalar', 'rxn_active_am_pct', rxn.active_am_pct);
    row('scalar', 'SE_of_solid_pct', mm.SE_of_solid_pct);
    row('scalar', 'bulk_density_g_cm3', mm.bulk_density_g_cm3);
    row('dispersion_header', 'cols', 'n_pts', 'index_of_dispersion', 'nn_med_um', 'nn_p90_um', 'nn_clustering', 'matrix_vol_frac');
    Object.entries(mm.additive_dispersion || {}).forEach(([ph, d]) => row('additive_dispersion', ph,
      d.n_pts, d.index_of_dispersion, d.nn_med_um, d.nn_p90_um, d.nn_clustering, d.matrix_vol_frac));
    Object.entries(s3.dissipation_share || {}).forEach(([k, v]) => row('e_dissipation_share', k, v));
    Object.entries(s3.ion_dissipation_share || {}).forEach(([k, v]) => row('ion_dissipation_share', k, v));
    row('zprofile_header', 'cols', 'z_lo_um', 'z_hi_um', 'mean_je_rel', 'mean_coverage_pct', 'count', 'econn_frac');
    zbins.forEach((b, i) => row('zprofile', 'bin_' + i, +b.z_lo.toFixed(2), +b.z_hi.toFixed(2),
      +zJe[i].toFixed(6), +zCov[i].toFixed(3), zCnt[i], +zEc[i].toFixed(3)));
    return out.join('\n');
  }
  function dlText(name, text) {
    const blob = new Blob(['﻿' + text], { type: 'text/csv;charset=utf-8' });   // BOM → Excel UTF-8
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  const slug = String(caseName).replace(/[^\w.-]+/g, '_').slice(0, 60);

  // ---- modal ----
  const overlay = document.createElement('div');
  overlay.className = 'path-modal-overlay';
  overlay.innerHTML = `
    <div class="path-modal" style="width:${W + 60}px;max-width:97vw">
      <button class="path-modal-close">&times;</button>
      <div style="font-size:14px;font-weight:bold;text-align:center;margin-bottom:8px">📊 분석 요약</div>
      <div id="mpm-sum-wrap" style="max-height:78vh;overflow:auto;text-align:center"></div>
      <div class="path-modal-actions">
        <button id="mpm-sum-csv-am">CSV — 입자별</button>
        <button id="mpm-sum-csv-sum">CSV — 요약·z프로파일</button>
        <button id="mpm-sum-png">PNG</button>
        <button id="mpm-sum-close">닫기</button>
      </div>
    </div>`;
  document.body.appendChild(overlay);
  cvs.style.width = W + 'px'; cvs.style.height = H + 'px'; cvs.style.maxWidth = '100%';
  overlay.querySelector('#mpm-sum-wrap').appendChild(cvs);
  const close = () => overlay.remove();
  overlay.querySelector('.path-modal-close').addEventListener('click', close);
  overlay.querySelector('#mpm-sum-close').addEventListener('click', close);
  overlay.onclick = (e) => { if (e.target === overlay) close(); };
  overlay.querySelector('#mpm-sum-png').addEventListener('click', () => {
    const a = document.createElement('a'); a.href = cvs.toDataURL('image/png');
    a.download = 'mpm_summary_' + slug + '.png'; document.body.appendChild(a); a.click(); a.remove();
  });
  overlay.querySelector('#mpm-sum-csv-am').addEventListener('click', () => dlText('mpm_perAM_' + slug + '.csv', perAMCsv()));
  overlay.querySelector('#mpm-sum-csv-sum').addEventListener('click', () => dlText('mpm_summary_' + slug + '.csv', summaryCsv()));
}

/* ── 케이스 비교 팝업 (⚖) ─────────────────────────────────────
 * mpm-lab에서 payload 2개를 골라 나란히: 정량 표 (σ_e/σ_ion/분담/R_geom/구조, Δ%) +
 * 3D 뷰 2개 (카메라 동기화).  배선 강도는 두 케이스의 counts를 합쳐 만든 "공동 스케일"로
 * 색칠 → 색 차이 = 실제 배선 차이 (사이드패널의 per-payload 자동 스케일은 비교 무효).
 * 전류밀도 필드는 export 시 payload별 자기 p99.8 정규화라 패턴 비교용 (legend에 명시). */
function _wiringCounts(particles, addPts, addCounts, boxLx, boxLy) {
  let carbon = (addPts || []).filter(p => p[3] === 2 || p[3] === 3 || p[3] === 5);
  const counts = new Float64Array((particles || []).length);
  const hits = new Array((particles || []).length);         // per-AM touching carbon pts (패치 렌더용)
  if (!carbon.length || !counts.length) return { counts, median: 0, hits };
  // 가중치는 반드시 ghost 복제 BEFORE 계산 — shown에 ghost가 들어가면 w=total/shown이 희석돼
  // 환산 접점이 축소됨 (버그였음: 중앙값 348→290 하락의 원인).
  const PHN = { 2: 'VGCF', 3: 'SuperP', 5: 'SDCP' };
  const shown = { 2: 0, 3: 0, 5: 0 };
  carbon.forEach(p => { shown[p[3]]++; });
  const w = {};
  [2, 3, 5].forEach(ph => {
    const tot = Number((addCounts || {})[PHN[ph]] || 0);
    w[ph] = (tot > 0 && shown[ph] > 0) ? tot / shown[ph] : 1;   // 서브샘플 가중 → 환산 접점
  });
  // PERIODIC (x,y) — RVE 경계 너머로 닿는 접점을 ghost 복제로 포함 (경계 입자의 배선이
  // 잘려 보이던 문제).  margin = max(r)+band 안에 드는 이미지 점만 복제 (z는 비주기).
  if (boxLx > 0 && boxLy > 0) {
    const marg = Math.max(...particles.map(p => p.r || 0)) + 0.5;
    const ghosts = [];
    for (const q of carbon) {
      for (let sx = -1; sx <= 1; sx++) for (let sy = -1; sy <= 1; sy++) {
        if (!sx && !sy) continue;
        const gx = q[0] + sx * boxLx, gy = q[1] + sy * boxLy;
        if (gx >= -marg && gx <= boxLx + marg && gy >= -marg && gy <= boxLy + marg)
          ghosts.push([gx, gy, q[2], q[3]]);
      }
    }
    carbon = carbon.concat(ghosts);
  }
  const CELL = 3.0, BAND = 0.3;
  const hash = new Map();
  carbon.forEach(p => {
    const k = Math.floor(p[0] / CELL) + ',' + Math.floor(p[1] / CELL) + ',' + Math.floor(p[2] / CELL);
    let a = hash.get(k); if (!a) { a = []; hash.set(k, a); } a.push(p);
  });
  particles.forEach((p, ix) => {
    const rr = p.r + BAND, rr2 = rr * rr;
    let n = 0;
    const hh = [];
    const ci = Math.floor(p.x / CELL), cj = Math.floor(p.y / CELL), ck = Math.floor(p.z / CELL);
    const reach = Math.ceil(rr / CELL);
    for (let di = -reach; di <= reach; di++) for (let dj = -reach; dj <= reach; dj++)
      for (let dk = -reach; dk <= reach; dk++) {
        const cell = hash.get((ci + di) + ',' + (cj + dj) + ',' + (ck + dk));
        if (!cell) continue;
        for (const q of cell) {
          const dx = q[0] - p.x, dy = q[1] - p.y, dz = q[2] - p.z;
          if (dx * dx + dy * dy + dz * dz <= rr2) { n += (w[q[3]] || 1); hh.push(q); }
        }
      }
    counts[ix] = n;
    if (hh.length) hits[ix] = hh;
  });
  const s = [...counts].sort((a, b) => a - b);
  return { counts, median: s[Math.floor(s.length / 2)] || 0, hits };
}

/* 논문용 컬러바 PNG — 뷰어와 동일 감마·컬러맵 (⚖ 팝업 + 단독 뷰어 공용, 6× 인쇄 해상).
   spec.ticks = [{p:0..1, label}] 수치 눈금 (바 x축은 값에 선형 — 감마는 색에만 적용되므로
   눈금 위치는 선형 그대로가 정확); spec.sub = 부제(단위 환산) 한 줄. */
/* z-프로파일 크리스프 렌더 (인라인 미리보기 + 고해상 export 공용) — 어떤 캔버스 크기든
   선폭·폰트·여백을 120px 기준으로 스케일해 또렷하게 그린다 (확대-뭉갬 방지). */
function drawZProfileCanvas(cv, curves, yLab, leftLab, rightLab) {
  const g = cv.getContext('2d'), W = cv.width, H = cv.height, k = H / 120;
  const mL = 6 * k, mR = 6 * k, mT = 6 * k, mB = 16 * k;
  const allY = curves.flatMap(c => c.ys), yMin = Math.min(...allY), yMax = Math.max(...allY, yMin + 1e-9);
  const zMax = Math.max(...curves.flatMap(c => c.zs), 1e-9);
  g.fillStyle = '#0d1117'; g.fillRect(0, 0, W, H);
  g.strokeStyle = '#2a2d3e'; g.lineWidth = 1 * k; g.strokeRect(mL, mT, W - mL - mR, H - mT - mB);
  const PX = z => mL + z / zMax * (W - mL - mR), PY = y => mT + (1 - (y - yMin) / (yMax - yMin)) * (H - mT - mB);
  for (const c of curves) {
    g.strokeStyle = c.color; g.lineWidth = 1.8 * k; g.setLineDash(c.dash ? [4 * k, 3 * k] : []);
    g.beginPath();
    c.zs.forEach((z, i) => { const x = PX(z), y = PY(c.ys[i]); i ? g.lineTo(x, y) : g.moveTo(x, y); });
    g.stroke();
  }
  g.setLineDash([]);
  g.fillStyle = '#9ca3af'; g.font = `${10.5 * k}px Inter,sans-serif`;
  g.textAlign = 'left'; g.fillText(leftLab || '집전체', mL + 1.5 * k, H - 4.5 * k);
  g.textAlign = 'right'; g.fillText(rightLab || '분리막', W - mR - 1.5 * k, H - 4.5 * k);
  g.textAlign = 'left'; g.fillText(yLab, mL + 4 * k, mT + 11 * k);
}

/* 3D 뷰 고해상 캡처 — 렌더 버퍼를 일시적으로 scale배 키워 render→toDataURL 후 복원.
   CSS 표시크기는 그대로(updateStyle=false), 종횡비 불변이라 카메라 갱신 불필요. */
/* PNG 프레임(data URL 배열) → 서버 Pillow로 GIF 조립 → 다운로드.  st4 시간전개(3D·두께프로파일)용.
   btn = 진행표시용 버튼(⏳ 토글).  fps = 초당 체크포인트. */
async function st4FramesToGif(frames, fps, name, btn) {
  if (!frames || !frames.length) { alert('프레임이 없어요 (체크포인트 없음)'); return; }
  const orig = btn ? btn.textContent : '';
  if (btn) { btn.disabled = true; btn.textContent = '⏳'; }
  try {
    const r = await fetch('/mpm-lab/gif', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frames, fps, name }) });
    if (!r.ok) { let e = {}; try { e = await r.json(); } catch (x) { /* */ } alert('GIF 실패: ' + (e.error || ('HTTP ' + r.status))); return; }
    const blob = await r.blob(), url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = name + '.gif';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (e) { alert('GIF 실패: ' + e.message); }
  finally { if (btn) { btn.disabled = false; btn.textContent = orig; } }
}

/* GIF 파일명에 붙일 사용자 라벨 (입력칸 id) — 있으면 '_라벨', 없으면 ''.  케이스명 자동식별과
   무관하게 두 다운로드를 확실히 구분(예: SBE/DBE).  안전문자만, 32자 컷. */
function _st4Label(id) {
  const v = ((document.getElementById(id) || {}).value || '').replace(/[^A-Za-z0-9._-]/g, '').slice(0, 32);
  return v ? '_' + v : '';
}

/* nChk 체크포인트를 sub배로 선형보간해 부드러운 프레임 시퀀스 캡처 (뷰어 재생과 동일한 보간).
   setPhase(소수 phase) = upd(phase), capture() = 프레임 캡처(dataURL).  sub=1이면 체크포인트만. */
function _st4GifFrames(nChk, sub, setPhase, capture) {
  const frames = [], s = Math.max(1, sub | 0), nF = (Math.max(1, nChk) - 1) * s + 1;
  for (let k = 0; k < nF; k++) { setPhase(k / s); const c = capture(); if (c) frames.push(c); }
  return frames;
}

function _captureHiRes(state, scale) {
  const r = state.renderer, cv = r.domElement;
  const pr = r.getPixelRatio(), dw = cv.width / pr, dh = cv.height / pr;   // CSS px
  r.setPixelRatio(1); r.setSize(dw * scale, dh * scale, false);
  r.render(state.scene, state.camera);
  const url = cv.toDataURL('image/png');
  r.setSize(dw, dh, false); r.setPixelRatio(pr);
  r.render(state.scene, state.camera);
  return url;
}

function exportColorbarPNG(spec, fname) {
  const sp = spec || { map: 'jet', gamma: 1.6, title: '|J| (normalized)', left: '0', right: 'high' };
  const S2 = 6, W2 = 470 * S2, H2 = (sp.sub ? 96 : 80) * S2;
  const cv = document.createElement('canvas'); cv.width = W2; cv.height = H2;
  const cx = cv.getContext('2d');
  cx.fillStyle = '#ffffff'; cx.fillRect(0, 0, W2, H2);
  cx.fillStyle = '#111111'; cx.font = `600 ${13 * S2}px Arial`; cx.textAlign = 'left';
  cx.fillText(sp.title, 10 * S2, 17 * S2);
  const bx = 10 * S2, by = 25 * S2, bw = W2 - 20 * S2, bh = 25 * S2;
  for (let i = 0; i < bw; i++) {
    const t = i / (bw - 1);
    const hx = sp.map === 'coolwarm' ? coolwarmColor(t) : jetColor(sp.gamma ? Math.pow(t, sp.gamma) : t);
    cx.fillStyle = '#' + hx.toString(16).padStart(6, '0');
    cx.fillRect(bx + i, by, 1.5, bh);
  }
  cx.strokeStyle = '#111111'; cx.lineWidth = S2 * 0.7; cx.strokeRect(bx, by, bw, bh);
  cx.fillStyle = '#111111'; cx.font = `${11.5 * S2}px Arial`;
  if (sp.ticks && sp.ticks.length) {                        // 수치 눈금 모드 (left/right 대신)
    cx.lineWidth = S2 * 0.55;
    for (const tk of sp.ticks) {
      const x = bx + Math.max(0, Math.min(1, tk.p)) * bw;
      cx.beginPath(); cx.moveTo(x, by + bh); cx.lineTo(x, by + bh + 5 * S2); cx.stroke();
      cx.textAlign = tk.p < 0.03 ? 'left' : (tk.p > 0.93 ? 'right' : 'center');
      cx.fillText(String(tk.label), x, by + bh + 15 * S2);
    }
  } else {
    cx.textAlign = 'left'; cx.fillText(sp.left != null ? String(sp.left) : '', bx, by + bh + 15 * S2);
    if (sp.mid != null) { cx.textAlign = 'center'; cx.fillText(String(sp.mid), bx + bw / 2, by + bh + 15 * S2); }
    cx.textAlign = 'right'; cx.fillText(sp.right != null ? String(sp.right) : '', bx + bw, by + bh + 15 * S2);
  }
  if (sp.sub) {
    cx.fillStyle = '#444444'; cx.font = `${9.5 * S2}px Arial`; cx.textAlign = 'left';
    cx.fillText(String(sp.sub), bx, by + bh + 28 * S2);
  }
  const a2 = document.createElement('a'); a2.href = cv.toDataURL('image/png');
  a2.download = fname || 'colorbar.png'; document.body.appendChild(a2); a2.click(); a2.remove();
}

/* focus 컬러바 수치 눈금: 0 → step 간격 (1/2/5/10/20 자동) → 상단 ×top ⟨J⟩ */
function _focusTicks(f) {
  const top = Number(f && f.focus_top);
  if (!(top > 0)) return null;
  const step = top > 60 ? 20 : top > 30 ? 10 : top > 12 ? 5 : top > 6 ? 2 : 1;
  const t = [{ p: 0, label: '0' }];
  for (let v = step; v < top * 0.86; v += step) t.push({ p: v / top, label: '×' + v });
  t.push({ p: 1, label: '×' + Number(top.toPrecision(3)) + ' ⟨J⟩' });
  return t;
}
/* COMSOL식 표면 반응전류 필드 지오메트리 빌더 (단독뷰어 renderSt4Faces.buildSurface와 동일 문법).
   parts + faces(pos_um) → 정점색 가능 표면 mesh + per-정점 각도커널(cos^24, ≈15°) 면 테이블.
   면전류를 입자 표면에 방향-코사인 가중 보간 → 핫스팟이 국소 색점으로; 비접촉 표면 = 회색. */
function buildComsolSurfaceMesh(parts, F) {
  const n = F.pos_um.length, K = 6, CELL = 8.0;
  const tmpl = new THREE.SphereGeometry(1, 26, 19);
  const tPos = tmpl.getAttribute('position').array, tIdx = tmpl.index.array, nV = tPos.length / 3;
  const nVertTot = nV * parts.length;
  const hash = new Map();
  const keyOf = (x, y, z) => Math.floor(x / CELL) + ',' + Math.floor(y / CELL) + ',' + Math.floor(z / CELL);
  parts.forEach((p, pi) => { const k = keyOf(p.x, p.y, p.z); let a = hash.get(k); if (!a) { a = []; hash.set(k, a); } a.push(pi); });
  const pFaces = parts.map(() => []);                        // 입자별 [면 idx, 단위방향 ux,uy,uz]
  for (let i = 0; i < n; i++) {
    const f = F.pos_um[i];
    let best = -1, bestScore = 1e9;
    const cx = Math.floor(f[0] / CELL), cy = Math.floor(f[1] / CELL), cz = Math.floor(f[2] / CELL);
    for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) for (let dz = -1; dz <= 1; dz++) {
      const a = hash.get((cx + dx) + ',' + (cy + dy) + ',' + (cz + dz));
      if (!a) continue;
      for (const pi of a) { const p = parts[pi]; const d = Math.hypot(f[0] - p.x, f[1] - p.y, f[2] - p.z); const sc = Math.abs(d - p.r); if (d < p.r + 1.2 && sc < bestScore) { bestScore = sc; best = pi; } }
    }
    if (best >= 0) { const p = parts[best]; const dx = f[0] - p.x, dy = f[1] - p.y, dz = f[2] - p.z; const L = Math.max(Math.hypot(dx, dy, dz), 1e-9); pFaces[best].push([i, dx / L, dy / L, dz / L]); }
  }
  const pos = new Float32Array(nVertTot * 3), idx = new Uint32Array(tIdx.length * parts.length);
  const vFace = new Int32Array(nVertTot * K).fill(-1), vW = new Float32Array(nVertTot * K), vDeg = new Uint8Array(nVertTot);
  parts.forEach((p, pi) => {
    const fl = pFaces[pi], base = pi * nV;
    for (let v = 0; v < nV; v++) {
      const ux = tPos[3 * v], uy = tPos[3 * v + 1], uz = tPos[3 * v + 2];
      pos[3 * (base + v)] = p.x + p.r * ux;
      pos[3 * (base + v) + 1] = p.z + p.r * uz;              // scene Y = payload z
      pos[3 * (base + v) + 2] = p.y + p.r * uy;
      if (!fl.length) continue;
      const bi = new Array(K).fill(-1), bw = new Array(K).fill(-1);
      for (let q = 0; q < fl.length; q++) {
        const d = ux * fl[q][1] + uy * fl[q][2] + uz * fl[q][3];   // payload 방향 직접 정렬 (템플릿 ux,uy,uz ↔ 면 dx,dy,dz)
        if (d <= bw[K - 1]) continue;
        let j = K - 1; while (j > 0 && bw[j - 1] < d) { bw[j] = bw[j - 1]; bi[j] = bi[j - 1]; j--; } bw[j] = d; bi[j] = fl[q][0];
      }
      let deg = 0;
      for (let k2 = 0; k2 < K; k2++) { if (bi[k2] < 0 || bw[k2] <= 0) break; vFace[(base + v) * K + k2] = bi[k2]; vW[(base + v) * K + k2] = Math.pow(bw[k2], 24); deg++; }
      vDeg[base + v] = deg;
    }
    for (let t2 = 0; t2 < tIdx.length; t2++) idx[pi * tIdx.length + t2] = base + tIdx[t2];
  });
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setIndex(new THREE.BufferAttribute(idx, 1));
  g.computeVertexNormals();
  const vColAttr = new THREE.BufferAttribute(new Float32Array(nVertTot * 3), 3);
  g.setAttribute('color', vColAttr);
  const surfMesh = new THREE.Mesh(g, new THREE.MeshPhongMaterial({ vertexColors: true, shininess: 22, specular: 0x222222 }));
  return { surfMesh, vFace, vW, vDeg, nVertTot, vColAttr, K };
}
/* 표면필드 정점 색칠 — 보간된 면전류 arr(|i| 절대값 전) + 시점 p95 hi(정규화 기준). */
function paintComsolSurface(surf, arr, hi) {
  const { vColAttr, vDeg, vFace, vW, nVertTot, K } = surf, cArr = vColAttr.array, col = new THREE.Color();
  for (let v = 0; v < nVertTot; v++) {
    const deg = vDeg[v];
    if (!deg) { cArr[3 * v] = 0.16; cArr[3 * v + 1] = 0.17; cArr[3 * v + 2] = 0.19; continue; }  // 비접촉 = 회색
    let sw = 0, sv = 0;
    for (let k2 = 0; k2 < deg; k2++) { const fi = vFace[v * K + k2]; sw += vW[v * K + k2]; sv += vW[v * K + k2] * Math.abs(arr[fi]); }
    col.setHex(jetColor(Math.max(0, Math.min(1, (sv / Math.max(sw, 1e-30)) / hi))));
    cArr[3 * v] = col.r; cArr[3 * v + 1] = col.g; cArr[3 * v + 2] = col.b;
  }
  vColAttr.needsUpdate = true;
}
/* 비교 팝업 st4 모드 — A·B 두 케이스의 애니메이션(3D 양쪽) 2fps + 조건.
   SOC 코어-셸(인스턴스 구) / 표면 반응전류(COMSOL 표면필드) 토글, 프레임 보간.
   viz는 lab 저장분(/mpm-lab/st4/<pid>) 자동 로드; 없으면 📂.  전압곡선은 별도 팝업(📈 버튼). */
function buildSt4Compare(overlay, $, SA, SB, A, B, pidA, pidB, nameA, nameB) {
  const X0 = 0.2638452245913298, X100 = 0.853974674630047;
  const store = overlay._st4store || (overlay._st4store = {});   // {A:{viz,mesh,parts}, B:{...}}
  const metaOf = o => ({ c_rate: o.c_rate, charge: o.charge, v_min: o.v_min, v_max: o.v_max,
    cv_hold: o.cv_hold, i_cut_frac: o.i_cut_frac, end_reason: o.end_reason, x0: o.x0, x100: o.x100 });
  const buildSide = (key, S, payload, o) => {
    const parts = (payload.particles || []).filter(p => p.type === 'AM_P' || p.type === 'AM_S');   // 단독뷰어와 동일: AM만 (SE 제외 — SOC·면분포 오염 방지)
    if (S.grp) { S.scene.remove(S.grp); S.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material && o.material.dispose) o.material.dispose(); }); S.grp = null; }   // GPU 버퍼 해제 (📂 재로드 누수 방지)
    const grp = new THREE.Group();
    const mesh = createInstancedSpheres(parts, 16, 0xffffff, 1.0, false);
    if (mesh) { mesh.material.shininess = 8; grp.add(mesh); }
    S.scene.add(grp); S.grp = grp;
    const nChk = (o.x_shell || []).length, F = o.faces;
    const hasRxn = !!(F && F.pos_um && F.i_rel && F.i_rel.length);
    // COMSOL 표면필드(surf)는 rxn 모드 첫 진입 때 지연 생성; frHi=프레임 p95 캐시, arrBuf=면전류 보간버퍼
    store[key] = { viz: o, meta: metaOf(o), parts, mesh, grp, nChk, F, hasRxn,
                   surf: null, frHi: [], arrBuf: hasRxn ? new Float32Array(F.pos_um.length) : null };
    if (S.meshes) ['AM_P', 'AM_S', 'MESH'].forEach(t => { if (S.meshes[t]) S.meshes[t].visible = false; });
  };
  const hiOf = (s, k) => { if (s.frHi[k] == null) { const abs = s.F.i_rel[k].map(Math.abs).sort((a, b) => a - b); s.frHi[k] = Math.max(abs[Math.floor(0.95 * (abs.length - 1))], 1e-9); } return s.frHi[k]; };
  const recolor = (frac) => {
    const c = new THREE.Color(), view = ($('cmp-st4-view') || {}).value || 'soc';
    ['A', 'B'].forEach(key => {
      const s = store[key]; if (!s || !s.mesh || !s.nChk) return;
      const rf = frac * (s.nChk - 1), t0 = Math.floor(rf), t1 = Math.min(s.nChk - 1, t0 + 1), fr = rf - t0;   // 프레임 보간
      if (view === 'rxn' && s.hasRxn) {
        if (!s.surf) { s.surf = buildComsolSurfaceMesh(s.parts, s.F); s.grp.add(s.surf.surfMesh); }  // 지연 생성
        s.mesh.visible = false; s.surf.surfMesh.visible = true;
        const nF = s.F.i_rel.length, k0 = Math.min(nF - 1, t0), k1 = Math.min(nF - 1, t1);
        const a0 = s.F.i_rel[k0], a1 = s.F.i_rel[k1], arr = s.arrBuf;
        for (let i = 0; i < arr.length; i++) arr[i] = (1 - fr) * a0[i] + fr * a1[i];   // 면전류 프레임 보간
        paintComsolSurface(s.surf, arr, (1 - fr) * hiOf(s, k0) + fr * hiOf(s, k1));
      } else {
        if (s.surf) s.surf.surfMesh.visible = false;
        s.mesh.visible = true;
        const lo = Math.min(s.meta.x0 ?? X0, s.meta.x100 ?? X100), hi = Math.max(s.meta.x0 ?? X0, s.meta.x100 ?? X100);
        const sh0 = s.viz.x_shell[t0], sh1 = s.viz.x_shell[t1], kSh = (s.viz.nr || 20) - 1;
        s.parts.forEach((p, i) => { const r0 = sh0[p.id], r1 = sh1[p.id];
          const xs = (r0 && r1) ? (1 - fr) * r0[kSh] + fr * r1[kSh] : lo;
          s.mesh.setColorAt(i, c.setHex(jetColor(Math.max(0, Math.min(1, (xs - lo) / Math.max(hi - lo, 1e-9)))))); });
        if (s.mesh.instanceColor) s.mesh.instanceColor.needsUpdate = true;
      }
    });
    const s0 = store.A || store.B;
    if (s0 && s0.nChk) { const rf = frac * (s0.nChk - 1), t0 = Math.floor(rf), t1 = Math.min(s0.nChk - 1, t0 + 1), fr = rf - t0;
      const tt = (1 - fr) * (s0.viz.t_s || [])[t0] + fr * (s0.viz.t_s || [])[t1];
      const xm = (1 - fr) * (s0.viz.x_mean || [])[t0] + fr * (s0.viz.x_mean || [])[t1];
      $('cmp-st4-t').textContent = `t=${isFinite(tt) ? tt.toFixed(0) : '?'}s · x̄=${isFinite(xm) ? xm.toFixed(4) : '?'}` + (view === 'rxn' ? ' · 반응 i/ī' : ' · SOC'); }
    if ($('cmp-st4-barlab')) $('cmp-st4-barlab').textContent = view === 'rxn' ? '|i/ī| 반응전류 (0–p95 → 핫스팟)' : 'SOC (x₀→x₁₀₀)';
  };
  const note = () => { $('cmp-st4-note').innerHTML = ['A', 'B'].map(k => { const s = store[k]; if (!s) return '';
    const m = s.meta, col = k === 'A' ? '#7dd3fc' : '#fbbf24';
    return `<span style="color:${col}">■ ${(k === 'A' ? nameA : nameB) || k}</span>: ${m.charge ? '충전' : '방전'} ${m.c_rate}C · ${m.v_min ?? '?'}–${m.v_max ?? '?'}V`
      + (m.charge && m.cv_hold ? ` CV종지${m.i_cut_frac}C` : '') + ` · 종료 ${m.end_reason || '?'}`; }).filter(Boolean).join('　'); };
  const loadInto = (key, o, fname) => {
    if (!o || o.kind !== 'step4_viz' || !o.x_shell) { alert((fname || key) + ': step4_viz(SOC) 아님'); return; }
    buildSide(key, key === 'A' ? SA : SB, key === 'A' ? A : B, o); note(); recolor(overlay._st4frac || 0);
  };
  const tryFetch = (key, pid) => { if (!pid || store[key]) return;
    fetch('/mpm-lab/st4/' + pid).then(r => r.ok ? r.json() : null).catch(() => null).then(o => { if (o) loadInto(key, o); }); };
  tryFetch('A', pidA); tryFetch('B', pidB);
  // 이미 로드된 게 있으면 즉시 재구성(모드 재진입)
  ['A', 'B'].forEach(k => { if (store[k]) buildSide(k, k === 'A' ? SA : SB, k === 'A' ? A : B, store[k].viz); });
  note();
  const pick = (key) => { const inp = document.createElement('input'); inp.type = 'file'; inp.accept = '.json'; inp.style.display = 'none'; document.body.appendChild(inp);
    inp.onchange = e => { const f = e.target.files[0]; if (!f) { inp.remove(); return; } const rd = new FileReader();
      rd.onload = () => { let o; try { o = JSON.parse(rd.result); } catch (err) { alert('파싱 실패'); inp.remove(); return; } loadInto(key, o, f.name); inp.remove(); }; rd.readAsText(f); }; inp.click(); };
  $('cmp-st4-la').onclick = () => pick('A'); $('cmp-st4-lb').onclick = () => pick('B');
  // 2fps 자동재생 (모드 진입 시 기본 ON)
  const playBtn = $('cmp-st4-play'), fpsSel = $('cmp-st4-fps');
  const startTimer = () => { overlay._st4frac = overlay._st4frac || 0; playBtn.textContent = '⏸';
    overlay._cmpSt4Timer = setInterval(() => { if (!overlay.isConnected) { clearInterval(overlay._cmpSt4Timer); return; }
      const fps = +fpsSel.value || 2; overlay._st4frac = (overlay._st4frac + fps * 0.03 / Math.max(1, (store.A || store.B || {}).nChk - 1 || 11)) % 1;
      recolor(overlay._st4frac); }, 30); };
  playBtn.onclick = () => { if (overlay._cmpSt4Timer) { clearInterval(overlay._cmpSt4Timer); overlay._cmpSt4Timer = null; playBtn.textContent = '▶'; } else startTimer(); };
  if (!overlay._cmpSt4Timer) startTimer();
  $('cmp-st4-vprof').onclick = () => showVProfilePopup(store, nameA, nameB);
  if ($('cmp-st4-view')) $('cmp-st4-view').onchange = () => recolor(overlay._st4frac || 0);
  recolor(overlay._st4frac || 0);
}

/* 전압곡선 별도 팝업 — buildSt4Compare가 로드한 store{A,B}의 curve를 겹쳐 그림 + 조건 + PNG/CSV. */
function showVProfilePopup(store, nameA, nameB) {
  const X0 = 0.2638452245913298, X100 = 0.853974674630047;
  const have = ['A', 'B'].map(k => store[k]).filter(s => s && s.viz && s.viz.curve && s.viz.curve.V);
  if (!have.length) { alert('curve 데이터가 있는 viz가 없어요 (2C부터 자동; 1C는 curve-병합본 필요)'); return; }
  const ov = document.createElement('div'); ov.className = 'path-modal-overlay';
  ov.innerHTML = `<div class="path-modal" style="width:min(90vw,860px);background:#0d1117;color:#e5e7eb">
    <button class="path-modal-close" style="color:#9ca3af">&times;</button>
    <div style="display:flex;gap:10px;align-items:center;font-size:12px;margin-bottom:6px;flex-wrap:wrap">
      <b style="font-size:14px">📈 STEP4-v2 전압곡선 (A 실선 / B 점선)</b>
      <label>x축 <select id="vp-x" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:2px"><option value="cap">면적용량 mAh/cm²</option><option value="soc">SOC 창 %</option><option value="t">시간 min</option></select></label>
      <button id="vp-png" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:3px 10px;cursor:pointer">PNG</button>
      <button id="vp-csv" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:3px 10px;cursor:pointer">CSV</button></div>
    <canvas id="vp-cv" style="width:100%;height:420px;background:#fff;border-radius:6px"></canvas>
    <div id="vp-note" style="font-size:12px;margin-top:6px;line-height:1.8"></div></div>`;
  document.body.appendChild(ov);
  ov.querySelector('.path-modal-close').onclick = () => ov.remove();
  ov.onclick = e => { if (e.target === ov) ov.remove(); };
  const $$ = id => ov.querySelector('#' + id);
  const ser = ['A', 'B'].map((k, idx) => { const s = store[k]; if (!s || !s.viz.curve || !s.viz.curve.V) return null;
    return { key: k, name: (k === 'A' ? nameA : nameB) || k, cu: s.viz.curve, meta: s.meta, color: k === 'A' ? '#1f6fb2' : '#d1495b' }; }).filter(Boolean);
  const draw = () => { const cv = $$('vp-cv'), g = cv.getContext('2d'), dpr = 2; cv.width = cv.clientWidth * dpr; cv.height = cv.clientHeight * dpr; g.scale(dpr, dpr);
    const W = cv.clientWidth, H = cv.clientHeight, mL = 62, mR = 16, mT = 14, mB = 46, xmode = $$('vp-x').value;
    g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
    const xof = (s, i) => { const m = s.meta, win = Math.abs((m.x100 ?? X100) - (m.x0 ?? X0));
      const q = m.charge ? ((m.x100 ?? X100) - s.cu.x_mean[i]) : (s.cu.x_mean[i] - (m.x0 ?? X0));   // 충전 반전 방지
      if (xmode === 't') return s.cu.t_s[i] / 60; if (xmode === 'cap') return q / win * 3.1; return 100 * q / win; };
    let vlo = 9, vhi = 0, xlo = 1e9, xhi = -1e9;
    ser.forEach(s => s.cu.V.forEach((v, i) => { vlo = Math.min(vlo, v); vhi = Math.max(vhi, v); const x = xof(s, i); xlo = Math.min(xlo, x); xhi = Math.max(xhi, x); }));
    const PX = x => mL + (x - xlo) / (xhi - xlo + 1e-9) * (W - mL - mR), PY = v => mT + (1 - (v - vlo) / (vhi - vlo + 1e-9)) * (H - mT - mB);
    g.strokeStyle = '#e5e7eb'; g.lineWidth = 1; g.strokeRect(mL, mT, W - mL - mR, H - mT - mB);
    for (let k = 1; k < 5; k++) { const gy = mT + (H - mT - mB) * k / 5; g.strokeStyle = '#f3f4f6'; g.beginPath(); g.moveTo(mL, gy); g.lineTo(W - mR, gy); g.stroke(); }
    ser.forEach(s => { g.strokeStyle = s.color; g.lineWidth = 2.4; g.setLineDash(s.meta.charge ? [6, 4] : []); g.beginPath();
      s.cu.V.forEach((v, i) => { const x = PX(xof(s, i)), y = PY(v); i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.stroke(); });
    g.setLineDash([]); g.fillStyle = '#111'; g.font = '13px sans-serif'; g.textAlign = 'right';
    for (let k = 0; k <= 5; k++) { const v = vlo + (vhi - vlo) * k / 5; g.fillText(v.toFixed(2), mL - 6, PY(v) + 4); }
    g.textAlign = 'center';
    for (let k = 0; k <= 5; k++) { const x = xlo + (xhi - xlo) * k / 5; g.fillText(x.toFixed(xmode === 'cap' ? 2 : 0), PX(x), H - mB + 18); }
    g.fillText(xmode === 't' ? 'Time (min)' : xmode === 'cap' ? 'Delivered capacity (mAh cm⁻²)' : 'SOC window (%)', mL + (W - mL - mR) / 2, H - 6);
    g.save(); g.translate(14, mT + (H - mT - mB) / 2); g.rotate(-Math.PI / 2); g.textAlign = 'center'; g.fillText('Cell voltage (V vs Li/Li⁺)', 0, 0); g.restore();
    let note = ser.map(s => { const m = s.meta;
      return `<span style="color:${s.color}">■</span> ${s.name}: ${m.charge ? '충전' : '방전'} ${m.c_rate}C · ${m.v_min ?? '?'}–${m.v_max ?? '?'}V · 종료 ${m.end_reason || '?'} · V ${s.cu.V[0].toFixed(3)}→${s.cu.V[s.cu.V.length - 1].toFixed(3)}`; }).join('<br>');
    // Δ(A−B) 정량 — 같은 프로토콜(충/방 동일) 두 곡선일 때 공통 SOC창 그리드에서 ΔV·Δη_kin 평균
    if (ser.length === 2 && !!ser[0].meta.charge === !!ser[1].meta.charge) {
      const socOf = s => { const m = s.meta, w = Math.abs((m.x100 ?? X100) - (m.x0 ?? X0)) || 1;
        return s.cu.x_mean.map(x => 100 * (m.charge ? ((m.x100 ?? X100) - x) : (x - (m.x0 ?? X0))) / w); };
      const prep = s => { let xs = socOf(s), vs = s.cu.V, ks = s.cu.eta_kin_mV || null;
        if (xs[0] > xs[xs.length - 1]) { xs = [...xs].reverse(); vs = [...vs].reverse(); ks = ks ? [...ks].reverse() : null; }
        return { xs, vs, ks }; };
      const A2 = prep(ser[0]), B2 = prep(ser[1]);
      const lo2 = Math.max(A2.xs[0], B2.xs[0]), hi2 = Math.min(A2.xs[A2.xs.length - 1], B2.xs[B2.xs.length - 1]);
      if (hi2 - lo2 > 5) {
        const itp = (xs, ys, q) => { let i = 1; while (i < xs.length && xs[i] < q) i++;
          if (i >= xs.length) return ys[ys.length - 1];
          const t = (q - xs[i - 1]) / Math.max(xs[i] - xs[i - 1], 1e-12); return ys[i - 1] + t * (ys[i] - ys[i - 1]); };
        const dV = [], dK = [];
        for (let q = lo2; q <= hi2 + 1e-9; q += (hi2 - lo2) / 24) {
          dV.push((itp(A2.xs, A2.vs, q) - itp(B2.xs, B2.vs, q)) * 1e3);
          if (A2.ks && B2.ks) dK.push(itp(A2.xs, A2.ks, q) - itp(B2.xs, B2.ks, q));
        }
        const mean = a => a.reduce((x, y) => x + y, 0) / Math.max(a.length, 1);
        note += `<br><b>Δ(A−B)</b> 공통 SOC ${lo2.toFixed(0)}–${hi2.toFixed(0)}%: <b>ΔV 평균 ${mean(dV) >= 0 ? '+' : ''}${mean(dV).toFixed(1)} mV</b>`
          + ` (${Math.min(...dV).toFixed(1)}…${Math.max(...dV).toFixed(1)})`
          + (dK.length ? ` · Δη_kin 평균 ${mean(dK) >= 0 ? '+' : ''}${mean(dK).toFixed(1)} mV` : '')
          + ' <span style="color:#9ca3af">— 낮은 쪽이 과전압 우위; 분해(옴/kin/확산)는 각 케이스 📈 곡선 PNG 2단 패널</span>';
      }
    }
    $$('vp-note').innerHTML = note; };
  $$('vp-x').onchange = draw;
  $$('vp-png').onclick = () => { const a = document.createElement('a'); a.href = $$('vp-cv').toDataURL('image/png'); a.download = 'step4_vprofile.png'; document.body.appendChild(a); a.click(); a.remove(); };
  $$('vp-csv').onclick = () => { const out = ['series,condition,step,t_s,V,x_mean'];
    ser.forEach(s => s.cu.V.forEach((v, i) => out.push([JSON.stringify(s.name), `${s.meta.charge ? 'charge' : 'discharge'}_${s.meta.c_rate}C`, i + 1, s.cu.t_s[i], v, s.cu.x_mean[i]].join(','))));
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([out.join('\n')], { type: 'text/csv' })); a.download = 'step4_vprofile.csv'; document.body.appendChild(a); a.click(); a.remove(); };
  draw();
}
export async function showLabCompareModal(pidA, pidB, nameA, nameB) {
  injectCSS();
  const overlay = document.createElement('div');
  overlay.className = 'path-modal-overlay';
  overlay.innerHTML = `
    <div class="path-modal" style="width:97vw;max-width:97vw;background:#0d1117;color:#e5e7eb">
      <button class="path-modal-close" style="color:#9ca3af">&times;</button>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;flex-wrap:wrap">
        <b style="font-size:14px">⚖ 케이스 비교</b>
        <select id="cmp-mode" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:3px 6px;font-size:12px">
          <option value="wiring">전기 배선 — 탄소 접점 패치 (공동 스케일 ★)</option>
          <option value="wiring_delta">Δ 배선 — 접점 차이 A−B (같은 골격 전용 ★)</option>
          <option value="je_field">⚡ 전자 전류밀도 필드</option>
          <option value="ji_field">⚡ 이온 전류밀도 필드</option>
          <option value="je">전자 — AM 입자별 (je)</option>
          <option value="je_delta">Δ 재분배 — bare/wetted 비율</option>
          <option value="jrxn">🔋 반응 전류밀도 (STEP4)</option>
          <option value="st4_v2">🔋 STEP4-v2 충방전 곡선 (A·B 겹침 + 조건)</option>
          <option value="additives">도전재 — 전체</option>
          <option value="add_vgcf">　└ VGCF만</option>
          <option value="add_superp">　└ Super P만</option>
          <option value="add_ptfe">　└ PTFE만</option>
          <option value="add_sdcp">　└ SDCP만</option>
          <option value="pore">기공 (pore)</option>
        </select>
        <label id="cmp-bb-wrap" style="display:none;font-size:11.5px;color:#e5e7eb;align-items:center;gap:4px">
          <input type="checkbox" id="cmp-bb-on" checked> 🔥백본
          <input type="range" id="cmp-bb-pct" min="30" max="95" step="5" value="80" style="width:88px;accent-color:#f97316">
          <span id="cmp-bb-lab" style="color:#9ca3af">80%</span></label>
        <label id="cmp-patch-wrap" style="font-size:11.5px;color:#e5e7eb;display:flex;align-items:center;gap:4px">
          패치 <input type="range" id="cmp-patch" min="0.5" max="3" step="0.25" value="1.5" style="width:70px;accent-color:#34d399">
          <span id="cmp-patch-lab" style="color:#9ca3af">1.5×</span></label>
        <label id="cmp-glow-wrap" style="font-size:11.5px;color:#e5e7eb;display:flex;align-items:center;gap:3px"
          title="x-ray 깊이누적 발광 (primer 논문 Fig4f 문법) — 겹칠수록 색이 짙어져 케이스 차이가 증폭됨. 필드 모드에선 고스트 없이 순수 볼륨 렌더">
          ✨<input type="checkbox" id="cmp-glow" checked>glow</label>
        <span id="cmp-fldops-wrap" style="display:none;font-size:11.5px;color:#e5e7eb;align-items:center;gap:8px">
          <label style="display:flex;align-items:center;gap:3px"
            title="σ-공동스케일: 두 쪽 색을 σ_eff 비율로 정렬해 절대 세기 차이가 색으로 보이게 (근사 — 상위꼬리 모양 유사 가정; 끄면 자기 정규화=패턴 비교)">
            <input type="checkbox" id="cmp-joint">σ공동</label>
          <select id="cmp-joint-ref" title="공동 스케일의 기준(컬러 상단 앵커) — auto=σ-max(클리핑 없음, 절대비교 기본) / A·B=그 케이스 기준(반대쪽이 넘치면 포화-클립 = baseline-대비 수사용)"
            style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;font-size:11px;padding:1px 2px">
            <option value="max">기준 auto(σ-max)</option><option value="A">기준 A</option><option value="B">기준 B</option></select>
          <label style="display:flex;align-items:center;gap:3px"
            title="백본을 점 대신 복셀 큐브로 — 인접 복셀이 붙어 연속 통로로 보임 (COMSOL 볼륨 문법)">
            <input type="checkbox" id="cmp-cube" checked>이어짐</label>
          <label style="display:flex;align-items:center;gap:3px"
            title="AM 입자 고스트(밝은 종이-회색) — 전류가 어느 입자 사이를 지나는지 컨텍스트">
            <input type="checkbox" id="cmp-ghost" checked>AM</label></span>
        <label style="font-size:11.5px;color:#e5e7eb;display:flex;align-items:center;gap:4px">
          <input type="checkbox" id="cmp-clip"> 단면
          <input type="range" id="cmp-clip-pos" min="2" max="98" value="50" style="width:88px;accent-color:#6c8cff"></label>
        <span style="display:flex;align-items:center;gap:4px;font-size:11.5px;color:#e5e7eb">
          <button id="cmp-zo" style="background:#334155;color:#fff;border:none;border-radius:4px;width:22px;height:22px;cursor:pointer">−</button>
          <input type="range" id="cmp-zoom" min="30" max="350" value="200" step="5" style="width:88px;accent-color:#6c8cff">
          <button id="cmp-zi" style="background:#334155;color:#fff;border:none;border-radius:4px;width:22px;height:22px;cursor:pointer">+</button></span>
        <span id="cmp-status" style="font-size:12px;color:#fbbf24">payload 2개 로딩 중… (수십 MB — 수십 초 걸릴 수 있어요)</span>
        <span style="flex:1"></span>
        <button id="cmp-cbar" class="data-modal-btn" style="width:auto;margin:0;padding:5px 12px"
          title="현재 모드의 컬러바를 논문용 PNG로 (흰 배경·3× 인쇄 해상·뷰어와 동일 감마)">컬러바</button>
        <button id="cmp-legend" class="data-modal-btn" style="width:auto;margin:0;padding:5px 12px"
          title="컴포넌트 범례 시트 PNG (NCM/SE/VGCF/SuperP/PTFE/SDCP — 뷰어 색상, manuscript 범례 문법)">범례</button>
        <button id="cmp-png" class="data-modal-btn" style="width:auto;margin:0;padding:5px 12px"
          title="A|B 합성 한 장 (4× 고해상, 흰 배경+이름표)">PNG</button>
        <button id="cmp-shot" class="data-modal-btn" style="width:auto;margin:0;padding:5px 12px"
          title="A·B 각각 별도 파일 — 투명 배경 4× 고해상 (PPT/논문 오버레이용, 메인 뷰어 Screenshot과 동일 문법)">투명샷 ×2</button>
      </div>
      <div id="cmp-table" style="font-size:12px;margin-bottom:6px;overflow-x:auto"></div>
      <div id="cmp-st4-wrap" style="display:none;margin-bottom:8px">
        <div style="display:flex;gap:8px;align-items:center;font-size:12px;flex-wrap:wrap">
          <b style="color:#e5e7eb">🔋 STEP4-v2 애니메이션</b>
          <select id="cmp-st4-view" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:2px"><option value="soc" selected>입자 SOC 코어-셸</option><option value="rxn">표면 반응전류(면분포)</option></select>
          <button id="cmp-st4-play" title="재생/정지" style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;border-radius:5px;padding:2px 9px;cursor:pointer;font-size:13px">⏸</button>
          <select id="cmp-st4-fps" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:2px"><option value="2" selected>2 fps</option><option value="4">4 fps</option><option value="8">8 fps</option></select>
          <span id="cmp-st4-t" style="color:#9ca3af"></span>
          <span style="flex:1"></span>
          <button id="cmp-st4-la" style="background:#1f2937;color:#7dd3fc;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer">📂 A viz</button>
          <button id="cmp-st4-lb" style="background:#1f2937;color:#fbbf24;border:1px solid #374151;border-radius:5px;padding:2px 8px;cursor:pointer">📂 B viz</button>
          <button id="cmp-st4-vprof" style="background:#16324a;color:#e5e7eb;border:1px solid #2563eb;border-radius:5px;padding:2px 10px;cursor:pointer">📈 전압곡선 팝업</button>
        </div>
        <div style="display:flex;align-items:center;gap:8px;margin-top:4px">
          <div style="flex:1;height:9px;border-radius:3px;background:linear-gradient(90deg,#0000ff,#00ffff,#00ff00,#ffff00,#ff0000)"></div>
          <span id="cmp-st4-barlab" style="color:#9ca3af;font-size:10px;white-space:nowrap">SOC (x₀→x₁₀₀)</span>
        </div>
        <div id="cmp-st4-note" style="color:#6b7280;font-size:11px;margin-top:3px"></div>
      </div>
      <div style="display:flex;gap:8px">
        <div style="flex:1;min-width:0">
          <div id="cmp-name-a" style="font-size:13px;font-weight:600;color:#7dd3fc;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></div>
          <div id="cmp-view-a" style="height:56vh;background:#f4f5f8;border-radius:8px;overflow:hidden"></div>
          <div id="cmp-leg-a" style="font-size:11px;color:#9ca3af;margin-top:3px;min-height:26px"></div>
        </div>
        <div style="flex:1;min-width:0">
          <div id="cmp-name-b" style="font-size:13px;font-weight:600;color:#fbbf24;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></div>
          <div id="cmp-view-b" style="height:56vh;background:#f4f5f8;border-radius:8px;overflow:hidden"></div>
          <div id="cmp-leg-b" style="font-size:11px;color:#9ca3af;margin-top:3px;min-height:26px"></div>
        </div>
      </div>
    </div>`;
  document.body.appendChild(overlay);
  const $ = (id) => overlay.querySelector('#' + id);
  // ── 논문용 컬러바/범례 내보내기 (user 2026-07-15: "manuscript 느낌의 컬러바 + 컴포넌트 이미지") ──
  let cbarSpec = null;                                       // rebuild()가 모드별로 채움
  const dlCanvas = (cv, name) => {
    const a2 = document.createElement('a'); a2.href = cv.toDataURL('image/png'); a2.download = name;
    document.body.appendChild(a2); a2.click(); a2.remove();
  };
  $('cmp-cbar').onclick = () => exportColorbarPNG(
    cbarSpec, 'colorbar_' + (($('cmp-mode') || {}).value || 'view') + '.png');
  $('cmp-legend').onclick = () => {
    // 컴포넌트 범례 시트 — manuscript 범례 문법(아이콘+라벨 한 줄), 색은 뷰어 실제 팔레트
    const items = [
      ['NCM (AM_P)', '#3a3a3a', 'sphere'], ['NCM (AM_S)', '#888888', 'sphere'],
      ['SE (Li₆PS₅Cl)', '#e8d68a', 'blob'], ['VGCF', '#22d3ee', 'fibre'],
      ['Super P', '#ec4899', 'dots'], ['PTFE', '#f59e0b', 'wave'], ['SDCP', '#ff3b30', 'dot'],
      ['SWCNT sheath', '#22c55e', 'fibre'],
    ];
    const S2 = 6, W2 = 830 * S2, H2 = 52 * S2;   // 논문 인쇄용 6× (~5000px)
    const cv = document.createElement('canvas'); cv.width = W2; cv.height = H2;
    const cx = cv.getContext('2d');
    cx.fillStyle = '#ffffff'; cx.fillRect(0, 0, W2, H2);
    let x = 14 * S2; const cy = 26 * S2;
    for (const [lab, col, kind] of items) {
      cx.strokeStyle = col; cx.fillStyle = col; cx.lineWidth = 2.6 * S2; cx.lineCap = 'round';
      if (kind === 'sphere') {
        const g2 = cx.createRadialGradient(x + 6 * S2, cy - 3 * S2, S2, x + 8 * S2, cy, 9 * S2);
        g2.addColorStop(0, '#ffffff'); g2.addColorStop(0.3, col); g2.addColorStop(1, col);
        cx.fillStyle = g2; cx.beginPath(); cx.arc(x + 8 * S2, cy, 8 * S2, 0, 7); cx.fill();
      } else if (kind === 'blob') {
        cx.globalAlpha = 0.85; cx.beginPath(); cx.arc(x + 8 * S2, cy, 8.5 * S2, 0, 7); cx.fill();
        cx.globalAlpha = 1;
      } else if (kind === 'fibre') {
        cx.beginPath(); cx.moveTo(x, cy + 5 * S2);
        cx.quadraticCurveTo(x + 8 * S2, cy - 8 * S2, x + 16 * S2, cy + 3 * S2); cx.stroke();
      } else if (kind === 'wave') {
        cx.beginPath(); cx.moveTo(x, cy + 3 * S2);
        cx.bezierCurveTo(x + 5 * S2, cy - 7 * S2, x + 11 * S2, cy + 9 * S2, x + 16 * S2, cy - 3 * S2); cx.stroke();
      } else if (kind === 'dots') {
        for (const [ox, oy] of [[3, -2], [8, 2], [12, -3]]) {
          cx.beginPath(); cx.arc(x + ox * S2, cy + oy * S2, 2.6 * S2, 0, 7); cx.fill();
        }
      } else {
        cx.beginPath(); cx.arc(x + 8 * S2, cy, 4 * S2, 0, 7); cx.fill();
      }
      cx.fillStyle = '#111111'; cx.font = `${11.5 * S2}px Arial`; cx.textAlign = 'left';
      cx.fillText(lab, x + 20 * S2, cy + 4 * S2);
      x += 20 * S2 + cx.measureText(lab).width + 18 * S2;
    }
    dlCanvas(cv, 'component_legend.png');
  };
  $('cmp-name-a').textContent = 'A · ' + (nameA || pidA);
  $('cmp-name-b').textContent = 'B · ' + (nameB || pidB);
  let stopped = false;
  const sides = [];
  const close = () => {
    stopped = true;
    sides.forEach(S => { try { S.ctrl.dispose(); S.renderer.dispose(); } catch (e) { /* ignore */ } });
    overlay.remove();
  };
  overlay.querySelector('.path-modal-close').addEventListener('click', close);
  overlay.onclick = (e) => { if (e.target === overlay) close(); };

  let A, B;
  try {
    [A, B] = await Promise.all([pidA, pidB].map(pid =>
      fetch('/mpm-lab/data/' + encodeURIComponent(pid))
        .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })));
  } catch (e) {
    $('cmp-status').textContent = '로딩 실패: ' + e.message;
    return;
  }
  if (!overlay.isConnected) return;                        // closed while loading
  $('cmp-status').textContent = '';
  try {                                                    // build errors → 모달 안에 표시 (silent-fail 금지)

  // ── 정량 표 ──
  const mmA = A.mpm_metrics || {}, mmB = B.mpm_metrics || {};
  const sA = mmA.step3 || {}, sB = mmB.step3 || {};
  const ecA = A.econn_summary || mmA.econn_summary || {}, ecB = B.econn_summary || mmB.econn_summary || {};
  const wireA = _wiringCounts(A.particles, A.additive_points, mmA.additive_counts,
                              (A.box || {}).x_max || 0, (A.box || {}).y_max || 0);
  const wireB = _wiringCounts(B.particles, B.additive_points, mmB.additive_counts,
                              (B.box || {}).x_max || 0, (B.box || {}).y_max || 0);
  const gsh = (s, k, ph) => 100 * (((s || {})[k] || {})[ph] || 0);
  // 축별 설명 카드 (hover) — 정의·유도식·논문 표현 팁 (분석 요약 문법)
  const rowsQ = [
    ['σ_e_eff (S/cm)', sA.sigma_e_eff_S_cm, sB.sigma_e_eff_S_cm,
     '유효 through-plane 전자전도도.\n복셀 Kirchhoff: ∇·(σ∇φ)=0, 플레이트 ΔV=1V, 측면 Neumann → σ_eff = I·L/(A·ΔV).\n전도상: AM + VGCF/SuperP + SDCP(250 S/cm 앵커).\n논문: "effective through-plane electronic conductivity" — Δ%가 전자 헤드라인(+52%).'],
    ['σ_ion_eff (S/cm)', sA.sigma_ion_eff_S_cm, sB.sigma_ion_eff_S_cm,
     '유효 through-plane 이온전도도 (같은 솔브, 전도상 = SE + SDCP).\nSE는 t⁺≈1 단일이온 전도체 → 정상상태 이온망은 순수 옴 저항망.\n논문: Bazzoun 2026 RNM/EIS 축과 직접 비교 가능 — "effective ionic conductivity".'],
    ['⟨J_e⟩ 평균 (A/cm²@1V)', (sA.field_scale_e || {}).j_mean_z_A_cm2_per_V, (sB.field_scale_e || {}).j_mean_z_A_cm2_per_V,
     '평균 관통 전류밀도 ⟨J_z⟩ = σ_eff·ΔV/L (옴 항등식 — σ 행과 Δ% 동일해야 정상 = 자기검산 행).\n운전 환산: 1C에서 두 전극 모두 ⟨J⟩ = 면적전류(≈3.07 mA/cm²)로 강제(직렬) — σ 차이는 대신 전압손실 η=J·L/σ로 나타남 (DBE가 같은 전류를 1.52× 적은 손실로 나름).\n논문: "mean through-plane current density".'],
    ['⟨J_ion⟩ 평균 (A/cm²@1V)', (sA.field_scale_ion || {}).j_mean_z_A_cm2_per_V, (sB.field_scale_ion || {}).j_mean_z_A_cm2_per_V,
     '이온판 옴 항등식 ⟨J_z⟩ = σ_ion·ΔV/L.\n정상 작동에선 이온·전자 총 전류가 같아야 함(반응점 직렬 릴레이) → 운전 ⟨J_ion⟩=⟨J_e⟩=면적전류.\n이온은 σ가 10⁴× 작아 같은 J의 "가격"(과전위)이 훨씬 비쌈 — 분극의 주범 축.'],
    ['e-집중 p99.8 (×⟨J_e⟩)', (sA.field_scale_e || {}).focus_top, (sB.field_scale_e || {}).focus_top,
     '전류 집중계수 focus = |J|(p99.8) / ⟨J_z⟩ — 선형해라 바이어스 무관(구조 고유량).\n국소 운전값 = focus × 면적전류 × C-rate [mA/cm²].\n↓ = 직렬 병목 해소: "평균은 오르고(+52%) 극단 핫스팟 의존은 줄어든다(−23%)" — 원고 §3-④ "brightens as a whole"의 숫자화. 논문: "current-focusing factor" (메인-1 캡션 병기 권고).'],
    ['ion-집중 p99.8 (×⟨J_ion⟩)', (sA.field_scale_ion || {}).focus_top, (sB.field_scale_ion || {}).focus_top,
     '이온판 집중계수 — 최악 SE 목(constriction)의 국소 전류 / 평균.\n↓ = SDCP 이온 우회로(분담 13.8%)가 SE 병목을 분산 → 국소 SE 과부하 완화 = 수명/안정성 축의 이득.\n논문: "peak constriction current −8%; the ionic counterpart of series-constriction relief".'],
    ['e-분담 SDCP (%)', gsh(sA, 'dissipation_share', 'SDCP'), gsh(sB, 'dissipation_share', 'SDCP'),
     'SDCP의 전자 줄열(소산) 분담 = P_SDCP/ΣP (Kirchhoff 해의 에너지 분해).\n병렬 전도라면 이득 ≈ 분담이어야 함 — 실제는 분담 7.3%로 +52%를 만듦 = 직렬 병목 해소의 1번 증거(§3-①).\nσ_SDCP 스윕에서 분담↓·이득↑ 역행(19.6→1.7%) = 직렬 시그니처 5점 연속.'],
    ['ion-분담 SDCP (%)', gsh(sA, 'ion_dissipation_share', 'SDCP'), gsh(sB, 'ion_dissipation_share', 'SDCP'),
     'SDCP의 이온 소산 분담 (σ_ion_SDCP = 0.001 S/cm 훅 — SE의 1/3).\n"SDCP는 이온 절연체가 아니다" 원칙의 정량 발현 — 이온 +5.6%·집중 −13%의 미시 근거.'],
    ['R_geom (Ω·cm²)', (sA.collector_geometric || {}).R_geom_ohm_cm2, (sB.collector_geometric || {}).R_geom_ohm_cm2,
     '집전체 기하 접촉저항 (모델 출력): 이중 솔브 R_geom = L·(1/σ_bare − 1/σ_wetted).\nbare = 바닥 실접촉 crown만 / wetted = 전면 접촉 가정.\n측정 R_int(Fig6e: SBE 110/DBE 46 Ω·cm²)와의 갭 = 화학/열화 몫 — 기하만으로는 µΩ급임을 보이는 축.'],
    ['porosity (%)', mmA.porosity_mpm_pct != null ? mmA.porosity_mpm_pct : mmA.porosity_settled_pct,
                     mmB.porosity_mpm_pct != null ? mmB.porosity_mpm_pct : mmB.porosity_settled_pct,
     'MPM 압밀 침대의 settled porosity (wallP 판독, 300 MPa hold).\nSBE 7.87 / DBE 7.39 = 레시피 효과(−0.5%p, PTFE 반감+SDCP 치밀화) — +52%를 설명하기엔 EMT 상한(+4%)보다도 두 자릿수 작음 → 대안 배제 논증(§7)에 사용.'],
    ['thickness (µm)', mmA.thickness_um != null ? mmA.thickness_um : mmA.thickness_mpm_um,
                       mmB.thickness_um != null ? mmB.thickness_um : mmB.thickness_mpm_um,
     '침대 두께 — VGCF prop-open(dilate-z 1.0711)이 고정 → 두 전극 동일(72.48µm).\n비교 규약의 held-fixed 축: 두께가 같아야 σ·⟨J⟩·R 비교가 순수 미세구조 효과가 됨.'],
    ['econn 연결률 (%)', ecA.connected_pct, ecB.connected_pct,
     '집전체까지 전자 경로가 이어진 AM 비율 (percolation 판정).\n100% = 고립 AM 없음 — dead-AM 반론 차단 축 (두 전극 모두 완전 연결이라 이득이 "연결 회복"이 아님을 증명).'],
    ['carbon clusters', ecA.n_carbon_clusters, ecB.n_carbon_clusters,
     '전도상(carbon+SDCP) 연결 성분 수.\n×2.7 (3,175→8,643) = 랜덤 분산 SDCP가 만든 새 브리지 단위들 — §3-② 기하 증거.\n논문: "the number of conductive clusters increases 2.7-fold".'],
    ['환산접점 중앙값 /AM', wireA.median, wireB.median,
     '입자별 탄소 배선수 N_C의 중앙값 — AM 표면 0.3µm 밴드 내 전도성 탄소(서브샘플 가중 환산, PTFE 제외).\n+19% = §3-②의 "carbon contacts per AM rise by 19%" 그 숫자.\n메인-2(배선 지도)의 스칼라 요약 — Methods 정의문(N_C) 참조.'],
    ['pore-τ (구조·확산)', (sA.pore || {}).tau, (sB.pore || {}).tau,
     '공극상 유효확산 tortuosity (TauFactor 규약: void σ=1 Laplace → D_eff/D0, τ=ε/D_rel).\n치밀 전극(ε~7%)은 공극이 비관통이라 τ 정의 불가(—)가 정상 — 액체전해질 침투 불가 = 전고체 서사 강화 축.\n⚠ ASSB Li⁺ 수송은 SE 접촉망(σ_ion)이 담당 — 이 τ를 수송식에 대입 금지.'],
    ['첨가제→SE nn_med (µm)', ((mmA.additive_dispersion || {}).conductive_all || {}).nn_med_um,
                              ((mmB.additive_dispersion || {}).conductive_all || {}).nn_med_um,
     '전도성 첨가제 점→최근접 SE 거리의 중앙값 (분산 통계).\n분산지수 D≈1(포아송)과 함께 "개별 랜덤 분산" 증빙 — 랜덤 배치가 틈 점유 확률을 최대화한다는 §3-② 기전의 정량 근거.'],
    ['반응 계면 BV faces', (sA.rxn || {}).n_bv_faces, (sB.rxn || {}).n_bv_faces,
     'AM|SE·AM|SDCP 반응 계면 수 (Butler–Volmer, STEP4).\n+18% = SDCP가 이온-소외됐던 AM 표면을 반응 가능하게 만든 것(절연 PTFE면 안 생김) — §3-② 반응면 이득의 원자료.  active% = 반응 참여 입자 비율.'],
    ['면적용량 (mAh/cm²)', (sA.field_scale_e || {}).areal_capacity_mAh_cm2, (sB.field_scale_e || {}).areal_capacity_mAh_cm2,
     'F·c_max·|x100−x0|·V_AM/면적 (Chen2020 창, 자동산출) — 1C 전류밀도 = 면적용량/1h.\n두 전극 미세차(3.107 vs 3.066)는 SDCP가 AM 경계 복셀 일부 덮은 래스터화 효과 — C-rate 정규화 시 참고.'],
    ['SE/solid (%)', mmA.SE_of_solid_pct, mmB.SE_of_solid_pct,
     'SE 부피 / 전 고체상 비율 — 이온망 재료 총량.\n두 전극 동일(46.7%)해야 정상(레시피는 carbon/binder만 다름) = 비교 규약의 held-fixed 축.'],
    ['SE덮임 AM_P Hertz (%)', mmA.coverage_AM_P_hertz_pct, mmB.coverage_AM_P_hertz_pct,
     'AM_P(대형 1차입자) 표면 중 SE와 Hertz-접촉(≤0.13µm, 꽉 눌린 tight 접촉)한 비율 = Li⁺가 실제 건너는 유효 이온 접촉면 (σ_ionic 폼이 쓰는 것).\n⚠ 이 A/B는 같은 MPM-압밀 SE-AM bed를 공유(coverage=SE-only) → Δ≈0이 정상이며 이는 물리 발견이 아니라 bed를 고정한 설정 산물.\n모델에선 PTFE가 AM에 draping(phase4)→SE와 표면 경쟁하므로, PTFE 실제 효과(0.99 vs 0.495)를 보려면 각각 MPM 재압밀 후 비교해야 함.'],
    ['SE덮임 AM_S Hertz (%)', mmA.coverage_AM_S_hertz_pct, mmB.coverage_AM_S_hertz_pct,
     'AM_S(소형 2차입자) 표면의 SE Hertz-접촉 비율.\n작은 입자는 표면적/부피비↑ → coverage가 이온망 접근성에 더 민감.'],
    ['SE덮임 AM_P Tabor (%)', mmA.coverage_AM_P_tabor_pct, mmB.coverage_AM_P_tabor_pct,
     'AM_P 표면의 SE Tabor-접촉(≤0.26µm, 소성으로 눌려 퍼진 넓은 자국) 비율 = 기계적 접촉면(전극 결합).\nHertz보다 넓지만 vdW 틈이라 이온 전도는 덜 됨.  Tabor−Hertz = MPM 소성 conforming 몫.'],
    ['SE덮임 AM_S Tabor (%)', mmA.coverage_AM_S_tabor_pct, mmB.coverage_AM_S_tabor_pct,
     'AM_S 표면의 SE Tabor-접촉(기계 접촉면) 비율.'],
    ['도전재덮임 AM_P (%)', mmA.coverage_AM_P_add_mpm_pct, mmB.coverage_AM_P_add_mpm_pct,
     'AM_P 표면 중 도전재(carbon/SDCP/PTFE)가 덮은 비율 — SE와 별개인 **전자-접촉 축**.\n★ PTFE→SDCP 교체가 드러나는 곳: SE coverage(이온 골격)는 불변이지만, 도전재 덮임은 여기서 갈림.\n(carbon-free 런은 —).'],
    ['도전재덮임 AM_S (%)', mmA.coverage_AM_S_add_mpm_pct, mmB.coverage_AM_S_add_mpm_pct,
     'AM_S 표면의 도전재 덮임 비율 (전자-접촉).'],
  ];
  // mono-AM 침대(AM_S 없음)면 AM_S coverage 행 숨김 (0.0000 혼란 방지)
  const _hasAMS = ((A.particles || []).some(p => p.type === 'AM_S')) || ((B.particles || []).some(p => p.type === 'AM_S'));
  const rowsQ2 = _hasAMS ? rowsQ : rowsQ.filter(r => !String(r[0]).includes('AM_S'));
  const fmtQ = (v) => (v == null || !isFinite(+v)) ? '—'
    : (Math.abs(+v) >= 1e4 || (Math.abs(+v) < 1e-2 && v != 0)) ? (+v).toExponential(2)
    : (+v).toFixed(Math.abs(+v) >= 100 ? 0 : Math.abs(+v) >= 1 ? 2 : 4);
  // 세로로 길어 2열로 분할 (반씩) — 각 열이 독립 테이블, 가로 배치
  const oneTable = (rows) => '<table style="border-collapse:collapse;white-space:nowrap;flex:1;min-width:0">'
    + '<tr style="color:#9ca3af">' + ['축', 'A', 'B', 'Δ (B−A)/A'].map((h, i) =>
        `<th style="text-align:${i ? 'right' : 'left'};padding:2px 10px 2px 0;border-bottom:1px solid #2a2d3e">${h}</th>`).join('') + '</tr>'
    + rows.map(([lab, a, b, tip]) => {
        const d = (a != null && b != null && isFinite(+a) && isFinite(+b) && +a !== 0) ? (100 * (b - a) / Math.abs(+a)) : null;
        const dTxt = d == null ? '—' : (d >= 0 ? '+' : '') + d.toFixed(1) + '%';
        const dCol = d == null ? '#6b7280' : d > 0.5 ? '#34d399' : d < -0.5 ? '#f87171' : '#9ca3af';
        const tipAttr = tip ? ` data-tip="${tip.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/\n/g, '&#10;')}"` : '';
        return `<tr><td style="padding:2px 10px 2px 0;color:#cbd5e1${tip ? ';cursor:help;text-decoration:underline dotted #4b5563;text-underline-offset:3px' : ''}"${tipAttr}>${lab}</td>`
          + `<td style="text-align:right;padding:2px 10px 2px 0;color:#7dd3fc">${fmtQ(a)}</td>`
          + `<td style="text-align:right;padding:2px 10px 2px 0;color:#fbbf24">${fmtQ(b)}</td>`
          + `<td style="text-align:right;padding:2px 0;color:${dCol}">${dTxt}</td></tr>`;
      }).join('') + '</table>';
  const half = Math.ceil(rowsQ2.length / 2);
  $('cmp-table').innerHTML = '<div style="display:flex;gap:26px;align-items:flex-start">'
    + oneTable(rowsQ2.slice(0, half)) + oneTable(rowsQ2.slice(half)) + '</div>';
  // ── 축 설명 카드: 커스텀 hover (native title은 ~1s 지연 + 스타일 없음 → 즉시 뜨는 카드) ──
  let tipCard = document.getElementById('cmp-tipcard');
  if (!tipCard) {
    tipCard = document.createElement('div');
    tipCard.id = 'cmp-tipcard';
    tipCard.style.cssText = 'position:fixed;z-index:3000;width:max-content;max-width:min(580px,64vw);'
      + 'background:#111827;border:1px solid #3b4252;border-radius:8px;padding:10px 13px;font-size:12.5px;'
      + 'line-height:1.6;color:#d1d5db;white-space:pre-line;word-break:keep-all;overflow-wrap:anywhere;'
      + 'box-shadow:0 8px 24px rgba(0,0,0,.55);pointer-events:none;display:none';
    document.body.appendChild(tipCard);
    document.addEventListener('click', () => { tipCard.style.display = 'none'; }, true);  // 모달 닫힘 잔존 방지
  }
  $('cmp-table').querySelectorAll('td[data-tip]').forEach(td => {
    td.onmouseenter = () => { tipCard.textContent = td.getAttribute('data-tip'); tipCard.style.display = 'block'; };
    td.onmousemove = e => {
      const w = tipCard.offsetWidth, h = tipCard.offsetHeight;
      let x = e.clientX + 14, y = e.clientY + 12;
      if (x + w > innerWidth - 8) x = Math.max(8, e.clientX - w - 14);
      if (y + h > innerHeight - 8) y = Math.max(8, e.clientY - h - 12);
      tipCard.style.left = x + 'px'; tipCard.style.top = y + 'px';
    };
    td.onmouseleave = () => { tipCard.style.display = 'none'; };
  });

  // ── 3D 두 쪽 ──
  const mkSide = (viewId, payload) => {
    const el = $(viewId);
    const W = el.clientWidth || 600, H = el.clientHeight || 480;
    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(W, H);
    renderer.setClearColor(0xffffff, 1);                     // 논문 질감: 순백 배경 (ARTISTIC Fig-5B 문법)
    renderer.localClippingEnabled = true;                    // 단면 슬라이스 지원
    el.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    // 스튜디오 조명 리그 — 밝은 무광 세라믹 구가 나오는 모델링-논문 렌더 문법
    scene.add(new THREE.AmbientLight(0xffffff, 0.35));
    scene.add(new THREE.HemisphereLight(0xffffff, 0x8e97a3, 0.55));
    const key = new THREE.DirectionalLight(0xffffff, 0.85); key.position.set(1.6, 2.4, 1.2); scene.add(key);
    const fill = new THREE.DirectionalLight(0xffffff, 0.30); fill.position.set(-1.4, 0.8, -1.6); scene.add(fill);
    const box = payload.box || {};
    {                                                        // 얇은 박스 와이어프레임 (논문 figure 필수 요소)
      const bw = box.x_max || 50, bd = box.y_max || 50, bh = box.z_max || 50;
      const eg = new THREE.EdgesGeometry(new THREE.BoxGeometry(bw, bh, bd));
      const ln = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({
        color: 0x2b3138, transparent: true, opacity: 0.55 }));
      ln.position.set(bw / 2, bh / 2, bd / 2);
      scene.add(ln);
    }
    const cx = (box.x_max || 50) / 2, cy = (box.y_max || 50) / 2, cz = (box.z_max || 50) / 2;
    const cam = new THREE.PerspectiveCamera(45, W / H, 0.1, 3000);
    const diag = Math.max(box.x_max || 50, box.z_max || 50);
    cam.position.set(cx + diag * 1.5, cz + diag * 1.1, cy + diag * 1.5);
    const ctrl = new OrbitControls(cam, renderer.domElement);
    ctrl.target.set(cx, cz * 0.9, cy); ctrl.update();
    const S = { renderer, scene, cam, ctrl, grp: null };
    sides.push(S);
    return S;
  };
  const SA = mkSide('cmp-view-a', A), SB = mkSide('cmp-view-b', B);
  let syncing = false;
  const link = (src, dst) => () => {
    if (syncing) return; syncing = true;
    dst.cam.position.copy(src.cam.position);
    dst.ctrl.target.copy(src.ctrl.target);
    dst.ctrl.update();
    syncing = false;
  };
  SA.ctrl.addEventListener('change', link(SA, SB));
  SB.ctrl.addEventListener('change', link(SB, SA));
  // ± 줌 게이지 (양쪽 동기 — 메인 뷰어와 같은 dist=380−v 모델)
  const setCmpZoom = (v) => {
    v = Math.max(30, Math.min(350, v));
    [SA, SB].forEach(S => {
      const dir = S.cam.position.clone().sub(S.ctrl.target).normalize();
      S.cam.position.copy(S.ctrl.target).addScaledVector(dir, 380 - v);
      S.ctrl.update();
    });
    if ($('cmp-zoom')) $('cmp-zoom').value = v;
  };
  {
    const d0 = SA.cam.position.distanceTo(SA.ctrl.target);
    if ($('cmp-zoom')) $('cmp-zoom').value = Math.max(30, Math.min(350, Math.round(380 - d0)));
  }
  if ($('cmp-zoom')) $('cmp-zoom').oninput = () => setCmpZoom(+$('cmp-zoom').value);
  if ($('cmp-zi')) $('cmp-zi').onclick = () => setCmpZoom(+($('cmp-zoom') || { value: 200 }).value + 20);
  if ($('cmp-zo')) $('cmp-zo').onclick = () => setCmpZoom(+($('cmp-zoom') || { value: 200 }).value - 20);
  SA.ctrl.addEventListener('change', () => {                 // 휠 줌도 게이지에 반영
    if ($('cmp-zoom')) $('cmp-zoom').value = Math.max(30, Math.min(350, Math.round(380 - SA.cam.position.distanceTo(SA.ctrl.target))));
  });
  // ── 패널 위 떠있는 ± 줌 (헤더 슬라이더가 스크롤로 안 보여도 항상 접근 — 양쪽 동기, 휠 줌과 병행) ──
  ['cmp-view-a', 'cmp-view-b'].forEach(id => {
    const cont = $(id); if (!cont) return;
    if (!cont.style.position) cont.style.position = 'relative';
    const z = document.createElement('div');
    z.style.cssText = 'position:absolute;left:8px;bottom:8px;display:flex;gap:4px;z-index:5';
    const mk = (t, d) => { const b = document.createElement('button'); b.textContent = t;
      b.title = '줌 (양쪽 동기 · 휠 줌도 가능)';
      b.style.cssText = 'background:rgba(31,41,55,.85);color:#e5e7eb;border:1px solid #374151;border-radius:5px;width:26px;height:26px;cursor:pointer;font-size:15px;line-height:1';
      b.onclick = () => setCmpZoom(+(($('cmp-zoom') || { value: 200 }).value) + d); return b; };
    z.appendChild(mk('−', -25)); z.appendChild(mk('+', 25));
    cont.appendChild(z);
  });

  const clearSide = (S) => {
    if (!S.grp) return;
    S.scene.remove(S.grp);
    S.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material && o.material.dispose) o.material.dispose(); });
    S.grp = null;
  };
  const jstops = [0, 0.25, 0.5, 0.75, 1].map(v => '#' + jetColor(v).toString(16).padStart(6, '0'));
  const barHtml = (lab) => `<div style="margin:2px 0;height:8px;border-radius:3px;background:linear-gradient(90deg,${jstops.join(',')})"></div>
    <div style="display:flex;justify-content:space-between;font-size:10px"><span>${lab[0]}</span><span>${lab[1]}</span><span>${lab[2]}</span></div>`;
  function buildWiring(S, payload, wire, lo, hi, patchF, glowOn) {
    // 최신 econn 문법: AM은 본색 유지, 카본 접촉부만 표면 패치로 (감마-jet, 공동 스케일).
    const parts = payload.particles || [];
    const grp = new THREE.Group();
    const mesh = createInstancedSpheres(parts, 16, 0xffffff, 1.0, false);
    if (mesh) {
      // 논문 질감: 밝은 무광 세라믹 회색 (검정은 음영이 죽어 입체감 상실 — ARTISTIC Fig-5B 문법).
      // 패치 색이 정보 전달자라 AM은 중립 밝은 회색이 정답 (음영 보이고 패치가 튐).
      mesh.material.shininess = 8;
      if (mesh.material.specular) mesh.material.specular.setHex(0x161616);
      const c = new THREE.Color();
      const PAPER_AM = { AM_P: 0xaeb4bc, AM_S: 0xc7ccd2 };
      parts.forEach((p, i) => mesh.setColorAt(i, c.setHex(PAPER_AM[p.type] || 0xb4bac1)));
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
      grp.add(mesh);
    }
    // ── 접촉 DOMAIN 렌더 (점 뿌리기 → 융합 캡, user: "근접한 것들은 하나의 도메인으로") ──
    // 입자별 접점 방향들을 각도 클러스터링(임계 28°)해 클러스터당 구면 캡 하나를 만든다.
    // 캡 = 코팅 패치처럼 읽히는 매끈한 디스크 (Lambert 음영, 논문 질감).  캡 색 = 입자 배선
    // 등급(감마 jet, 공동 스케일).  patchF 슬라이더 = 캡 각반경 배율.
    const f = (typeof patchF === 'number' ? patchF : 1.5);
    const SEG = 20, MERGE = Math.cos(28 * Math.PI / 180);
    const PADR = (3 + 3 * f) * Math.PI / 180, MINR = (5 + 3 * f) * Math.PI / 180, MAXR = 0.95;
    const capList = [];
    const c2 = new THREE.Color();
    parts.forEach((p, i) => {
      const hh = wire.hits && wire.hits[i]; if (!hh) return;
      const t = Math.max(0, Math.min(1, (wire.counts[i] - lo) / Math.max(hi - lo, 1e-9)));
      c2.setHex(jetColor(Math.pow(t, 1.6)));
      // 1) 단위 방향 클러스터링 (greedy, 평균 방향과 28° 이내면 병합)
      const cls = [];
      for (const q of hh) {
        let dx = q[0] - p.x, dy = q[1] - p.y, dz = q[2] - p.z;
        const L = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1;
        dx /= L; dy /= L; dz /= L;
        let best = null, bestDot = MERGE;
        for (const cl of cls) {
          const nl = Math.sqrt(cl.sx * cl.sx + cl.sy * cl.sy + cl.sz * cl.sz) || 1;
          const d = (dx * cl.sx + dy * cl.sy + dz * cl.sz) / nl;
          if (d > bestDot) { bestDot = d; best = cl; }
        }
        if (best) { best.sx += dx; best.sy += dy; best.sz += dz; best.m.push([dx, dy, dz]); }
        else cls.push({ sx: dx, sy: dy, sz: dz, m: [[dx, dy, dz]] });
      }
      // 2) 클러스터 파라미터 수집 (본체/glow 2-pass가 같은 캡을 공유)
      for (const cl of cls) {
        const nl = Math.sqrt(cl.sx * cl.sx + cl.sy * cl.sy + cl.sz * cl.sz) || 1;
        const nx = cl.sx / nl, ny = cl.sy / nl, nz = cl.sz / nl;
        let thMax = 0;
        for (const v of cl.m) thMax = Math.max(thMax, Math.acos(Math.max(-1, Math.min(1, v[0] * nx + v[1] * ny + v[2] * nz))));
        const th = Math.min(MAXR, Math.max(MINR, thMax + PADR));
        const ax = Math.abs(ny) < 0.9 ? [0, 1, 0] : [1, 0, 0];
        let t1x = ny * ax[2] - nz * ax[1], t1y = nz * ax[0] - nx * ax[2], t1z = nx * ax[1] - ny * ax[0];
        const t1l = Math.sqrt(t1x * t1x + t1y * t1y + t1z * t1z) || 1;
        t1x /= t1l; t1y /= t1l; t1z /= t1l;
        capList.push({ px: p.x, py: p.y, pz: p.z, r: p.r, nx, ny, nz, t1x, t1y, t1z,
                       t2x: ny * t1z - nz * t1y, t2y: nz * t1x - nx * t1z, t2z: nx * t1y - ny * t1x,
                       th, cr: c2.r, cg: c2.g, cb: c2.b });
      }
    });
    // 곡면 캡 emit — 정점을 구 반경 r+lift 위 각도 링(0 / 0.55θ / θ)에 놓아 표면을 감싼다.
    // winding: scene swap (x,z,y)=반사(det −1)라 역순으로 감아 바깥면이 front (컬링 버그 방지).
    const emitCaps = (lift, padE) => {
      const vtx = [], vcol = [], idx = [];
      for (const cp of capList) {
        const th = Math.min(MAXR, cp.th + padE), Rp = cp.r + lift;
        const base = vtx.length / 3;
        const pushV = (thk, ph) => {
          const rs = Rp * Math.sin(thk), hc = Rp * Math.cos(thk);
          const cph = Math.cos(ph), sph = Math.sin(ph);
          vtx.push(cp.px + cp.nx * hc + (cp.t1x * cph + cp.t2x * sph) * rs,
                   cp.pz + cp.nz * hc + (cp.t1z * cph + cp.t2z * sph) * rs,
                   cp.py + cp.ny * hc + (cp.t1y * cph + cp.t2y * sph) * rs);   // scene swap (x,z,y)
          vcol.push(cp.cr, cp.cg, cp.cb);
        };
        pushV(0, 0);
        for (let s = 0; s < SEG; s++) pushV(0.55 * th, 2 * Math.PI * s / SEG);
        for (let s = 0; s < SEG; s++) pushV(th, 2 * Math.PI * s / SEG);
        const r1 = base + 1, r2 = base + 1 + SEG;
        for (let s = 0; s < SEG; s++) {
          const sn = (s + 1) % SEG;
          idx.push(base, r1 + sn, r1 + s);
          idx.push(r1 + s, r2 + sn, r2 + s);
          idx.push(r1 + s, r1 + sn, r2 + sn);
        }
      }
      if (!vtx.length) return null;
      const g2 = new THREE.BufferGeometry();
      g2.setAttribute('position', new THREE.Float32BufferAttribute(vtx, 3));
      g2.setAttribute('color', new THREE.Float32BufferAttribute(vcol, 3));
      g2.setIndex(idx);
      g2.computeVertexNormals();
      return g2;
    };
    const gMain = emitCaps(0.06, 0);
    if (gMain) {
      const dom = new THREE.Mesh(gMain, new THREE.MeshLambertMaterial({
        vertexColors: true, side: THREE.DoubleSide }));
      dom.userData.keepDouble = true;                        // applyCmpClip의 FrontSide 강제에서 제외
      dom.renderOrder = 20; grp.add(dom);
    }
    if (gMain && glowOn !== false) {
      // ✨ glow = 깊이-누적 x-ray halo.  예전 점 버전에서 차이가 보였던 이유가 바로 이 누적
      // (따뜻한 도메인이 많은 쪽이 깊이 방향으로 겹치며 워시로 증폭) — 그 물리를 캡 기하로 재현:
      // depthTest OFF + 저불투명 → 겹칠수록 색이 짙어져 케이스 간 밀도 차이가 한눈에.
      const gGlow = emitCaps(0.20, 3 * Math.PI / 180);
      if (gGlow) {
        const gm = new THREE.Mesh(gGlow, new THREE.MeshBasicMaterial({
          vertexColors: true, transparent: true, opacity: 0.10,
          depthTest: false, depthWrite: false, side: THREE.DoubleSide }));
        gm.userData.keepDouble = true;
        gm.renderOrder = 40; grp.add(gm);
      }
    }
    S.scene.add(grp); S.grp = grp;
  }
  function buildPore(S, payload) {
    const vp = payload.void_points || [];
    const grp = new THREE.Group();
    if (vp.length) {
      const pos = new Float32Array(vp.length * 3);
      for (let i = 0; i < vp.length; i++) {
        const p = vp[i];
        pos[3 * i] = p[0]; pos[3 * i + 1] = p[2]; pos[3 * i + 2] = p[1];
      }
      const gg = new THREE.BufferGeometry();
      gg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      grp.add(new THREE.Points(gg, new THREE.PointsMaterial({
        color: 0x38bdf8, size: 0.32, sizeAttenuation: true, transparent: true, opacity: 0.9 })));
    }
    S.scene.add(grp); S.grp = grp;
    return vp.length;
  }
  function buildField(S, payload, ionic, bbOn, bbPct, glowOn, scaleK, cubeOn, ghostOn) {
    // scaleK: σ-공동스케일 배율 (자기-p99.8 정규화 위에 σ_eff 비율을 곱해 절대 세기 차이를 색으로 —
    //         근사: 상위꼬리 모양 유사 가정, legend에 명시).  cubeOn: 백본을 점 대신 복셀 큐브로
    //         (인접 복셀이 면을 공유해 연속 통로로 읽힘 — user "점말고 이어지게").
    const kS = (typeof scaleK === 'number' && isFinite(scaleK) && scaleK > 0) ? scaleK : 1;
    const grp = new THREE.Group();
    const parts = payload.particles || [];
    if (ghostOn !== false) {                                 // AM 고스트 — glow와 독립 (user: "AM은 있되 칙칙하지 않게")
      const ghost = createInstancedSpheres(parts, 10, 0xffffff, 0.14, true);
      if (ghost) {
        const dk = new THREE.Color(0xd2d7dd);                // 어두운 베일 대신 밝은 종이-회색 → 캔버스가 안 칙칙해짐
        parts.forEach((_, i) => ghost.setColorAt(i, dk));
        if (ghost.instanceColor) ghost.instanceColor.needsUpdate = true;
        grp.add(ghost);
      }
    }
    const fldp = payload[ionic ? 'ionic_field' : 'electronic_field'] || [];
    let bbTxt = '';
    if (fldp.length) {
      const jv2 = fldp.map(p => p[3]);
      const s2 = [...jv2].sort((a, b) => a - b);
      const hi2 = Math.max(s2[Math.floor(0.998 * (s2.length - 1))], 1e-9);
      const gam2 = (t) => Math.pow(Math.max(0, Math.min(1, t / hi2)), 1.6);
      const pos = new Float32Array(fldp.length * 3), colr = new Float32Array(fldp.length * 3);
      const c = new THREE.Color();
      for (let i = 0; i < fldp.length; i++) {
        const p = fldp[i];
        pos[3 * i] = p[0]; pos[3 * i + 1] = p[2]; pos[3 * i + 2] = p[1];
        c.setHex(jetColor(gam2(p[3] * kS)));
        colr[3 * i] = c.r; colr[3 * i + 1] = c.g; colr[3 * i + 2] = c.b;
      }
      const gg = new THREE.BufferGeometry();
      gg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      gg.setAttribute('color', new THREE.BufferAttribute(colr, 3));
      for (const [sz, op] of [[0.9, 0.10], [0.45, 0.55]]) {   // 배경 반투명 (백본이 주인공)
        const pm = new THREE.Points(gg, new THREE.PointsMaterial({
          size: sz, vertexColors: true, sizeAttenuation: true, map: roundDotTex(),
          transparent: true, opacity: op, alphaTest: 0.02, depthWrite: false }));
        pm.renderOrder = 900; grp.add(pm);
      }
      if (bbOn) {                                            // 🔥 백본 — 메인 뷰어와 동일 문법
        const vox3 = (((payload.mpm_metrics || {}).step3) || {}).vox_um || 0.4;
        const order = Array.from({ length: fldp.length }, (_, i) => i).sort((a, b) => jv2[b] - jv2[a]);
        const tot = jv2.reduce((a, b) => a + b, 0) || 1;
        let acc = 0, nH = 0;
        while (nH < order.length && nH < 30000 && acc < (bbPct / 100) * tot) { acc += jv2[order[nH]]; nH++; }
        const hIdx = order.slice(0, nH);
        const hPos = new Float32Array(nH * 3), hCol = new Float32Array(nH * 3);
        const hotMap = new Map();
        hIdx.forEach((fi, k) => {
          const p = fldp[fi];
          hPos[3 * k] = p[0]; hPos[3 * k + 1] = p[2]; hPos[3 * k + 2] = p[1];
          c.setHex(jetColor(gam2(p[3] * kS)));
          hCol[3 * k] = c.r; hCol[3 * k + 1] = c.g; hCol[3 * k + 2] = c.b;
          hotMap.set(Math.round(p[0] / vox3 - 0.5) + ',' + Math.round(p[1] / vox3 - 0.5) + ','
                   + Math.round(p[2] / vox3 - 0.5), k);
        });
        if (cubeOn) {
          // 복셀 큐브 렌더 — 인접 백본 복셀이 면을 공유해 "이어진 통로"로 읽힘 (COMSOL 볼륨 문법,
          // 복셀-정직: 큐브 크기 = 실제 vox).  Lambert 음영이라 studio 라이트에서 입체감.
          const cubeGeo = new THREE.BoxGeometry(vox3 * 0.98, vox3 * 0.98, vox3 * 0.98);
          const im = new THREE.InstancedMesh(cubeGeo, new THREE.MeshLambertMaterial({ color: 0xffffff }), nH);
          // glow OFF에서도 칙칙하지 않게: Lambert(입체감) 위에 unlit 보강 패스 — 면 방향과 무관하게
          // 제 색을 유지 (COMSOL 볼륨 톤).  glow와 달리 depthTest 유지 = 기하-정직한 밝기.
          const im2 = new THREE.InstancedMesh(cubeGeo, new THREE.MeshBasicMaterial({
            color: 0xffffff, transparent: true, opacity: 0.40, depthWrite: false }), nH);
          const m4 = new THREE.Matrix4();
          for (let k = 0; k < nH; k++) {
            m4.setPosition(hPos[3 * k], hPos[3 * k + 1], hPos[3 * k + 2]);
            im.setMatrixAt(k, m4); im2.setMatrixAt(k, m4);
            c.setRGB(hCol[3 * k], hCol[3 * k + 1], hCol[3 * k + 2]);
            im.setColorAt(k, c); im2.setColorAt(k, c);
          }
          im.instanceMatrix.needsUpdate = true; im2.instanceMatrix.needsUpdate = true;
          if (im.instanceColor) im.instanceColor.needsUpdate = true;
          if (im2.instanceColor) im2.instanceColor.needsUpdate = true;
          im.renderOrder = 950; grp.add(im);
          im2.renderOrder = 951; grp.add(im2);
        } else {
          const hg = new THREE.BufferGeometry();
          hg.setAttribute('position', new THREE.BufferAttribute(hPos, 3));
          hg.setAttribute('color', new THREE.BufferAttribute(hCol, 3));
          const bbSz = nH <= 12000 ? [[1.7, 0.30], [0.85, 0.95]] : [[1.05, 0.20], [0.55, 0.92]];
          for (const [sz, op] of bbSz) {
            const pm = new THREE.Points(hg, new THREE.PointsMaterial({
              size: sz, vertexColors: true, sizeAttenuation: true, map: roundDotTex(),
              transparent: true, opacity: op, alphaTest: 0.03, depthWrite: false }));
            pm.renderOrder = 950; grp.add(pm);
          }
          const ePos = [], eCol = [];
          hIdx.forEach((fi, k) => {
            const p = fldp[fi];
            const ci = Math.round(p[0] / vox3 - 0.5), cj = Math.round(p[1] / vox3 - 0.5),
                  ck = Math.round(p[2] / vox3 - 0.5);
            for (const [di, dj, dk2] of [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) {
              const nb = hotMap.get((ci + di) + ',' + (cj + dj) + ',' + (ck + dk2));
              if (nb === undefined) continue;
              ePos.push(hPos[3 * k], hPos[3 * k + 1], hPos[3 * k + 2], hPos[3 * nb], hPos[3 * nb + 1], hPos[3 * nb + 2]);
              eCol.push(hCol[3 * k], hCol[3 * k + 1], hCol[3 * k + 2], hCol[3 * nb], hCol[3 * nb + 1], hCol[3 * nb + 2]);
            }
          });
          if (ePos.length) {
            const eg = new THREE.BufferGeometry();
            eg.setAttribute('position', new THREE.Float32BufferAttribute(ePos, 3));
            eg.setAttribute('color', new THREE.Float32BufferAttribute(eCol, 3));
            const lm = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({
              vertexColors: true, transparent: true, opacity: 0.9, depthWrite: false }));
            lm.renderOrder = 940; grp.add(lm);
          }
        }
        bbTxt = ` · 🔥백본 ${nH.toLocaleString()}복셀=전류 ${Math.round(100 * acc / tot)}%`
              + (cubeOn ? ' · 복셀큐브' : '');
      }
    }
    S.scene.add(grp); S.grp = grp;
    return { n: fldp.length, bbTxt };
  }
  function buildAdditives(S, payload, only) {
    // 개별(메인) 뷰어의 buildCarbonOverlay를 "그대로" 재사용 — fibre 폴리라인, periodic-wrap
    // chord 스킵, 두께→밝기, binder 톤 등 검증된 렌더 전부 (중복 구현 금지, user 지시).
    // shim state({data, scene})로 위임하고, 만들어진 그룹을 컨테이너로 옮겨 clearSide가 정리.
    const cont = new THREE.Group();
    const parts = payload.particles || [];
    const ghost = createInstancedSpheres(parts, 10, 0xffffff, 1.0, false);
    if (ghost) {                                             // SEM-black AM (개별 도전재 모드와 동일)
      const dk = new THREE.Color(0x141414);
      parts.forEach((_, i) => ghost.setColorAt(i, dk));
      if (ghost.instanceColor) ghost.instanceColor.needsUpdate = true;
      cont.add(ghost);
    }
    const shim = { data: payload, scene: S.scene };
    const nSeg = buildCarbonOverlay(shim, only, only ? 1.0 : 0.7, null);
    if (shim.additivePointGroup) {
      S.scene.remove(shim.additivePointGroup);
      cont.add(shim.additivePointGroup);
    }
    S.scene.add(cont); S.grp = cont;
    const nFib = (payload.additive_fibres || []).filter(f => !only || f.phase === only).length;
    return { nPts: nSeg, nFib };
  }
  function buildJe(S, payload, fldKey) {
    const parts = payload.particles || [];
    const grp = new THREE.Group();
    const mesh = createInstancedSpheres(parts, 16, 0xffffff, 1.0, false);
    if (mesh) {
      mesh.material.shininess = 8;
      if (mesh.material.specular) mesh.material.specular.setHex(0x161616);
      const vals = parts.map(p => p[fldKey]).filter(v => isFinite(v)).sort((a, b) => a - b);
      const hi2 = Math.max(vals[Math.floor(0.998 * (vals.length - 1))] || 1e-9, 1e-30);
      const c = new THREE.Color();
      parts.forEach((p, i) => {
        if (!isFinite(p[fldKey])) { mesh.setColorAt(i, c.setHex(0x333333)); return; }
        mesh.setColorAt(i, c.setHex(jetColor(Math.pow(Math.max(0, Math.min(1, p[fldKey] / hi2)), 1.6))));
      });
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
      grp.add(mesh);
    }
    S.scene.add(grp); S.grp = grp;
  }
  function buildDelta(S, payload) {
    const parts = payload.particles || [];
    const grp = new THREE.Group();
    const mesh = createInstancedSpheres(parts, 16, 0xffffff, 1.0, false);
    if (mesh) {
      mesh.material.shininess = 8;
      if (mesh.material.specular) mesh.material.specular.setHex(0x161616);
      const je = parts.map(p => p.je).filter(v => isFinite(v)).sort((a, b) => a - b);
      const eps = Math.max(1e-30, (je[Math.floor(je.length / 2)] || 1e-6) * 1e-3);
      const dts = parts.map(p => (isFinite(p.je) && isFinite(p.jb)) ? Math.log2((p.jb + eps) / (p.je + eps)) : NaN);
      const absR = dts.filter(isFinite).map(Math.abs).sort((a, b) => a - b);
      const R = Math.min(3, Math.max(0.5, absR[Math.floor(0.99 * (absR.length - 1))] || 1));
      const c = new THREE.Color();
      parts.forEach((_, i) => {
        const d = dts[i];
        mesh.setColorAt(i, c.setHex(isFinite(d)
          ? coolwarmColor(0.5 + 0.5 * Math.max(-1, Math.min(1, d / R))) : 0x333333));
      });
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
      grp.add(mesh);
    }
    S.scene.add(grp); S.grp = grp;
  }
  function buildWiringDelta(S, payload, d, R, thr) {
    // 입자별 Δ(A−B 환산접점) coolwarm 맵 — thr>0이면 |Δ|<thr 입자는 고스트(핫스팟 뷰).
    const parts = payload.particles || [];
    const grp = new THREE.Group();
    const mesh = createInstancedSpheres(parts, 16, 0xffffff, 1.0, false);
    if (mesh) {
      mesh.material.shininess = 8;
      if (mesh.material.specular) mesh.material.specular.setHex(0x161616);
      const c = new THREE.Color(), ghost = new THREE.Color(0xdcdfe4);
      parts.forEach((_, i2) => {
        const dv = d[i2];
        if (!isFinite(dv) || (thr > 0 && Math.abs(dv) < thr)) { mesh.setColorAt(i2, ghost); return; }
        mesh.setColorAt(i2, c.setHex(coolwarmColor(0.5 + 0.5 * Math.max(-1, Math.min(1, dv / R)))));
      });
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
      grp.add(mesh);
    }
    S.scene.add(grp); S.grp = grp;
  }
  // 단면 슬라이스 (양쪽 동기, 각자 자기 박스 기준 분율)
  const clipSt = { on: false, frac: 0.5 };
  function applyCmpClip() {
    [[SA, A], [SB, B]].forEach(([S, P]) => {
      const box = P.box || {};
      const y0 = box.y_min || 0, y1 = box.y_max || 50;
      const planes = clipSt.on ? [new THREE.Plane(new THREE.Vector3(0, 0, -1), y0 + (y1 - y0) * clipSt.frac)] : null;
      if (S.grp) S.grp.traverse(o => {
        if (o.material) {
          o.material.clippingPlanes = planes;
          if (o.isMesh) o.material.side = (planes || (o.userData && o.userData.keepDouble))
            ? THREE.DoubleSide : THREE.FrontSide;            // 도메인 캡은 항상 DoubleSide
          o.material.needsUpdate = true;
        }
      });
    });
  }
  function rebuild() {
    const mode = $('cmp-mode').value;
    const bbWrap = $('cmp-bb-wrap');
    if (bbWrap) bbWrap.style.display = (mode === 'je_field' || mode === 'ji_field') ? 'inline-flex' : 'none';
    const pWrap = $('cmp-patch-wrap');
    if (pWrap) pWrap.style.display = (mode === 'wiring') ? 'flex' : 'none';
    const gWrap = $('cmp-glow-wrap');
    if (gWrap) gWrap.style.display = (mode === 'wiring') ? 'flex' : 'none';   // 필드에선 AM 체크가 대체
    const fWrap = $('cmp-fldops-wrap');
    if (fWrap) fWrap.style.display = (mode === 'je_field' || mode === 'ji_field') ? 'inline-flex' : 'none';
    const bbOn = $('cmp-bb-on') ? $('cmp-bb-on').checked : true;
    const bbPct = $('cmp-bb-pct') ? +$('cmp-bb-pct').value : 80;
    const patchF = $('cmp-patch') ? +$('cmp-patch').value : 1.5;
    const glowOn = $('cmp-glow') ? $('cmp-glow').checked : true;
    clearSide(SA); clearSide(SB);
    const st4Wrap = $('cmp-st4-wrap');
    if (st4Wrap) st4Wrap.style.display = (mode === 'st4_v2') ? 'block' : 'none';
    if (overlay._cmpSt4Timer) { clearInterval(overlay._cmpSt4Timer); overlay._cmpSt4Timer = null; }
    if (mode === 'st4_v2') { buildSt4Compare(overlay, $, SA, SB, A, B, pidA, pidB, nameA, nameB); return; }   // 3D 애니메이션 유지
    if (mode === 'wiring') {
      const joint = [...wireA.counts, ...wireB.counts].sort((a, b) => a - b);
      const lo = joint.length ? joint[Math.floor(0.05 * (joint.length - 1))] : 0;
      const hi = joint.length ? Math.max(joint[Math.floor(0.95 * (joint.length - 1))], lo + 1) : 1;
      buildWiring(SA, A, wireA, lo, hi, patchF, glowOn);
      buildWiring(SB, B, wireB, lo, hi, patchF, glowOn);
      const leg = (w) => `중앙값 <b>${Math.round(w.median)}</b> 환산접점/AM · 공동 스케일 ${Math.round(lo)}–${Math.round(hi)} (색 비교 유효 ★, 접촉 도메인=클러스터 융합 캡, periodic 이미지 접점 포함)`
        + barHtml([`약함 ${Math.round(lo)}`, '환산 접점/AM', `강함 ${Math.round(hi)}`]);
      $('cmp-leg-a').innerHTML = leg(wireA);
      $('cmp-leg-b').innerHTML = leg(wireB);
      cbarSpec = { map: 'jet', gamma: 1.6, title: 'Carbon wiring — weighted contacts per AM (joint scale)',
                   left: '약함 ' + Math.round(lo), right: '강함 ' + Math.round(hi) };
    } else if (mode === 'wiring_delta') {
      // Δ 배선 — 같은 AM 골격(같은 케이스 파생) 두 payload의 입자별 접점 차이 (user: "차이 자체를 색칠")
      const partsA = A.particles || [], partsB = B.particles || [];
      const bById = new Map();
      partsB.forEach((p, i2) => bById.set(p.id != null ? p.id : i2, wireB.counts[i2]));
      const d = new Float64Array(partsA.length);
      let matched = 0;
      partsA.forEach((p, i2) => {
        const k = p.id != null ? p.id : i2;
        if (bById.has(k)) { d[i2] = wireA.counts[i2] - bById.get(k); matched++; } else d[i2] = NaN;
      });
      const frac = partsA.length ? matched / partsA.length : 0;
      if (frac < 0.8) {
        const warn = '⚠ 두 payload의 AM 골격이 달라 Δ 비교 불가 (id 매칭 ' + Math.round(100 * frac)
          + '%) — 같은 케이스에서 파생된 payload끼리 선택하세요';
        $('cmp-leg-a').innerHTML = warn; $('cmp-leg-b').innerHTML = warn;
      } else {
        const fin = [...d].filter(isFinite);
        const abs = fin.map(Math.abs).sort((x, y) => x - y);
        const R = Math.max(abs[Math.floor(0.99 * (abs.length - 1))] || 1, 5);
        const thr = abs[Math.floor(0.80 * (abs.length - 1))] || 0;
        const mean = fin.reduce((x, y) => x + y, 0) / Math.max(fin.length, 1);
        const nUp = fin.filter(v => v > 0).length;
        buildWiringDelta(SA, A, d, R, 0);
        buildWiringDelta(SB, A, d, R, thr);                  // 같은 골격 → A 좌표로 렌더
        $('cmp-leg-a').innerHTML = 'Δ = A−B 환산접점 전체맵 · 평균 ' + (mean >= 0 ? '+' : '') + mean.toFixed(1)
          + ' · Δ>0 입자 ' + Math.round(100 * nUp / Math.max(fin.length, 1)) + '% · 범위 ±' + Math.round(R)
          + ' (빨강 = A쪽 배선 보강)';
        $('cmp-leg-b').innerHTML = '|Δ| 상위 20% 핫스팟만 (임계 ' + Math.round(thr) + ') — 보강/약화가 어디 몰렸나';
      }
    } else if (mode === 'je_field' || mode === 'ji_field') {
      const ionic = mode === 'ji_field';
      const jointOn = $('cmp-joint') ? $('cmp-joint').checked : false;
      const cubeOn = $('cmp-cube') ? $('cmp-cube').checked : true;
      // σ-공동스케일: |J|의 자릿수는 σ_eff에 비례(같은 ΔV·유사 분포모양 가정) → 약한 쪽 색을
      // σ비율만큼 눌러 절대 세기 차이가 색으로 보이게.  근사임을 legend에 명시 (★).
      const sgA = ionic ? sA.sigma_ion_eff_S_cm : sA.sigma_e_eff_S_cm;
      const sgB = ionic ? sB.sigma_ion_eff_S_cm : sB.sigma_e_eff_S_cm;
      const smx = Math.max(sgA || 0, sgB || 0) || 1;
      // 앵커 선택: auto=σ-max(클리핑 없음) / A·B=그 케이스 기준 (반대쪽 k>1 → 상단 포화-클립
      //   = "baseline 대비" 수사용.  클립은 정보손실이므로 legend에 명시)
      const refSel = ($('cmp-joint-ref') || {}).value || 'max';
      const sref = (refSel === 'A' && sgA) ? sgA : (refSel === 'B' && sgB) ? sgB : smx;
      const kA2 = jointOn && sgA ? sgA / sref : 1, kB2 = jointOn && sgB ? sgB / sref : 1;
      const ghostOn = $('cmp-ghost') ? $('cmp-ghost').checked : true;
      const rA2 = buildField(SA, A, ionic, bbOn, bbPct, glowOn, kA2, cubeOn, ghostOn),
            rB2 = buildField(SB, B, ionic, bbOn, bbPct, glowOn, kB2, cubeOn, ghostOn);
      const cap = (r, s3x, k2) => {
        const fscX = ionic ? s3x.field_scale_ion : s3x.field_scale_e;   // 정량 스케일 (신 payload)
        return (r.n ? `${r.n.toLocaleString()}점` : 'FIELD 없음 (payload 재생성 필요)') + r.bbTxt
          + ' · ' + (ionic ? 'σ_ion ' + fmtQ(s3x.sigma_ion_eff_S_cm) : 'σ_e ' + fmtQ(s3x.sigma_e_eff_S_cm)) + ' S/cm'
          + (fscX ? ` · p99.8 = ×${Number(fscX.focus_top).toPrecision(2)} ⟨J_z⟩ (${Number(fscX.j_top_A_cm2_per_V).toPrecision(2)} A/cm²@1V)` : '')
          + (jointOn ? ` · σ-공동 ×${k2.toFixed(2)}${k2 > 1.001 ? ' ⚠상단 클립' : ''} (기준 ${refSel === 'max' ? 'σ-max' : refSel} · 비례 근사 ★색 비교 유효)`
                     : ' · 자기 p99.8 정규화 — 패턴 비교용(절대는 σ)');
      };
      $('cmp-leg-a').innerHTML = cap(rA2, sA, kA2);
      $('cmp-leg-b').innerHTML = cap(rB2, sB, kB2);
      const fA3 = ionic ? sA.field_scale_ion : sA.field_scale_e;
      const fB3 = ionic ? sB.field_scale_ion : sB.field_scale_e;
      // σ-공동 스케일의 기준은 k=1.00인 σ-max 케이스 (약한 쪽은 ×k로 눌림) — 컬러바 수치는
      // 그 기준 케이스의 focus/절대값.  자기-정규화(비공동)에서는 케이스별 상단이 달라
      // 수치 눈금이 성립 안 함 → 양쪽 상단을 부제에 병기.
      const fscT = jointOn ? (refSel === 'A' ? (fA3 || fB3) : refSel === 'B' ? (fB3 || fA3)
                              : (((sgB || 0) >= (sgA || 0)) ? (fB3 || fA3) : (fA3 || fB3))) : (fA3 || fB3);
      let subT;
      if (jointOn && fscT) {
        subT = 'joint reference = ' + (refSel === 'max' ? 'σ-max case' : 'case ' + refSel + ' (반대쪽 상단 클립 가능)')
             + ' · top(p99.8) = ' + Number(fscT.j_top_A_cm2_per_V).toPrecision(3)
             + ' A/cm² @ΔV=1V' + (fscT.j_1C_mA_cm2 ? ' · @1C: ⟨J⟩ ' + Number(fscT.j_1C_mA_cm2).toPrecision(3)
             + ' · top ' + Number(fscT.j_1C_mA_cm2 * fscT.focus_top).toPrecision(3) + ' mA/cm²' : '');
      } else if (fA3 && fB3) {
        subT = 'per-case self-normalized: A top ×' + Number(fA3.focus_top).toPrecision(3) + ' / B top ×'
             + Number(fB3.focus_top).toPrecision(3) + ' ⟨J⟩ — 수치 눈금은 σ공동 스케일에서 유효';
      }
      cbarSpec = { map: 'jet', gamma: 1.6,
                   title: (ionic ? '|J_ion|' : '|J_e|') + (fscT ? ' / ⟨J_z⟩ current-focusing' : ' relative current density')
                          + ' (p99.8-normalized' + (jointOn ? ', σ-joint scale' : '') + ')',
                   left: '0', right: fscT ? '×' + Number(fscT.focus_top).toPrecision(3) + ' ⟨J⟩' : 'high',
                   ...(jointOn && fscT ? { ticks: _focusTicks(fscT) } : {}),
                   ...(subT ? { sub: subT } : {}) };
    } else if (mode === 'je') {
      buildJe(SA, A, 'je'); buildJe(SB, B, 'je');
      const cap = (s3x) => 'AM 입자별 |J_z| (wetted) · σ_e ' + fmtQ(s3x.sigma_e_eff_S_cm)
        + ' S/cm · 자기 p99.8+감마 — 패턴 비교용';
      $('cmp-leg-a').innerHTML = cap(sA);
      $('cmp-leg-b').innerHTML = cap(sB);
      cbarSpec = { map: 'jet', gamma: 1.6, title: '|J_z| per-AM relative (wetted collector, p99.8)',
                   left: '0', right: 'high' };
    } else if (mode === 'jrxn') {
      buildJe(SA, A, 'jrxn'); buildJe(SB, B, 'jrxn');
      const cap = (s3x) => {
        const rx = (s3x || {}).rxn || {};
        return '반응 전류 i/ī (STEP4 저율·선형화 BV) · active AM ' + (rx.active_am_pct != null ? rx.active_am_pct + '%' : '—')
          + (rx.n_bv_faces ? ' · BV faces ' + Number(rx.n_bv_faces).toLocaleString() : '')
          + ' · 자기 p99.8+감마 — 패턴 비교용 (payload에 jrxn 필요)';
      };
      $('cmp-leg-a').innerHTML = cap(sA);
      $('cmp-leg-b').innerHTML = cap(sB);
      cbarSpec = { map: 'jet', gamma: 1.6, title: 'Reaction current i/\u012b (low-rate charging, p99.8)',
                   left: '0 (\ubc18\uc751 \uc18c\uc678)', right: 'hot' };
    } else if (mode === 'je_delta') {
      buildDelta(SA, A); buildDelta(SB, B);
      const cap = (s3x) => {
        const cg2 = s3x.collector_geometric || {};
        return 'Δ 재분배 log₂(jb/je) — 파랑=냉각·빨강=가열·흰=불변'
          + (cg2.n_bottom_contacts ? ` · 접점 ${cg2.n_bottom_contacts.wetted}→${cg2.n_bottom_contacts.bare}` : '');
      };
      $('cmp-leg-a').innerHTML = cap(sA);
      $('cmp-leg-b').innerHTML = cap(sB);
      cbarSpec = { map: 'coolwarm', title: '\u0394 redistribution log\u2082(j_bare/j_wetted)',
                   left: '\u00d70.71 \ub0c9\uac01', mid: '\ubcc0\ud654 \uc5c6\uc74c', right: '\u00d71.4 \uac00\uc5f4' };
    } else if (mode === 'pore') {
      const nA3 = buildPore(SA, A), nB3 = buildPore(SB, B);
      const cap = (n, mm2) => `${n.toLocaleString()} void voxels · porosity `
        + fmtQ(mm2.porosity_mpm_pct != null ? mm2.porosity_mpm_pct : mm2.porosity_settled_pct) + '%';
      $('cmp-leg-a').innerHTML = cap(nA3, mmA);
      $('cmp-leg-b').innerHTML = cap(nB3, mmB);
    } else {                                                 // additives family
      const only = mode === 'add_vgcf' ? 2 : mode === 'add_superp' ? 3 : mode === 'add_ptfe' ? 4
                 : mode === 'add_sdcp' ? 5 : 0;
      const rA3 = buildAdditives(SA, A, only), rB3 = buildAdditives(SB, B, only);
      const swatch = { 0: '전체', 2: 'VGCF', 3: 'SuperP', 4: 'PTFE', 5: 'SDCP' };
      const cap = (r3, mm2) => `${swatch[only]} — fibre ${r3.nFib.toLocaleString()}가닥 · ${r3.nPts.toLocaleString()} seg/점 (개별 뷰어 렌더러 재사용) · `
        + Object.entries(mm2.additive_counts || {}).map(([k, v]) => `${k} ${Number(v).toLocaleString()}`).join(' · ');
      $('cmp-leg-a').innerHTML = cap(rA3, mmA);
      $('cmp-leg-b').innerHTML = cap(rB3, mmB);
    }
    applyCmpClip();                                          // 새 재질에 단면 재적용
  }
  $('cmp-mode').onchange = rebuild;
  if ($('cmp-bb-on')) $('cmp-bb-on').onchange = rebuild;
  if ($('cmp-bb-pct')) {
    $('cmp-bb-pct').oninput = () => { if ($('cmp-bb-lab')) $('cmp-bb-lab').textContent = $('cmp-bb-pct').value + '%'; };
    $('cmp-bb-pct').onchange = rebuild;
  }
  if ($('cmp-clip')) $('cmp-clip').onchange = () => { clipSt.on = $('cmp-clip').checked; applyCmpClip(); };
  if ($('cmp-clip-pos')) $('cmp-clip-pos').oninput = () => { clipSt.frac = (+$('cmp-clip-pos').value) / 100; applyCmpClip(); };
  if ($('cmp-patch')) {
    $('cmp-patch').oninput = () => { if ($('cmp-patch-lab')) $('cmp-patch-lab').textContent = $('cmp-patch').value + '×'; };
    $('cmp-patch').onchange = rebuild;
  }
  if ($('cmp-glow')) $('cmp-glow').onchange = rebuild;
  if ($('cmp-joint')) $('cmp-joint').onchange = rebuild;
  if ($('cmp-joint-ref')) $('cmp-joint-ref').onchange = rebuild;
  if ($('cmp-cube')) $('cmp-cube').onchange = rebuild;
  if ($('cmp-ghost')) $('cmp-ghost').onchange = rebuild;
  rebuild();
  $('cmp-png').onclick = async () => {
    // 논문급 스크린샷: 각 쪽을 4× 슈퍼샘플로 재렌더(captureHighRes) 후 이름표와 함께 합성.
    const btn = $('cmp-png');
    btn.disabled = true; btn.textContent = '촬영 중…';
    try {
      const load = (u) => new Promise(res => { const im = new Image(); im.onload = () => res(im); im.src = u; });
      const [ia, ib] = await Promise.all([
        load(captureHighRes(SA.renderer, SA.scene, SA.cam, 4)),
        load(captureHighRes(SB.renderer, SB.scene, SB.cam, 4))]);
      const GAP = 24, HEAD = 76;
      const cv = document.createElement('canvas');
      cv.width = ia.width + ib.width + GAP;
      cv.height = Math.max(ia.height, ib.height) + HEAD;
      const x = cv.getContext('2d');
      x.fillStyle = '#ffffff'; x.fillRect(0, 0, cv.width, cv.height);
      x.drawImage(ia, 0, HEAD); x.drawImage(ib, ia.width + GAP, HEAD);
      x.fillStyle = '#111827'; x.font = 'bold 36px sans-serif';
      x.fillText('A · ' + (nameA || pidA), 10, 48);
      x.fillText('B · ' + (nameB || pidB), ia.width + GAP + 10, 48);
      const dl2 = document.createElement('a');
      dl2.href = cv.toDataURL('image/png');
      dl2.download = 'compare_' + $('cmp-mode').value + '.png';
      document.body.appendChild(dl2); dl2.click(); dl2.remove();
    } finally {
      btn.disabled = false; btn.textContent = 'PNG';
      SA.renderer.render(SA.scene, SA.cam); SB.renderer.render(SB.scene, SB.cam);
    }
  };
  $('cmp-shot').onclick = async () => {
    // 각 쪽을 별도 파일로 — 투명 배경 + 4× 슈퍼샘플 (메인 뷰어 Screenshot 문법: PPT/논문 오버레이용)
    const btn = $('cmp-shot');
    btn.disabled = true; btn.textContent = '촬영 중…';
    try {
      const shot = (S, tag, nm) => {
        const prevC = new THREE.Color(); S.renderer.getClearColor(prevC);
        const prevA = S.renderer.getClearAlpha();
        S.renderer.setClearColor(0x000000, 0);               // 투명 배경
        const url = captureHighRes(S.renderer, S.scene, S.cam, 4);
        S.renderer.setClearColor(prevC, prevA);
        S.renderer.render(S.scene, S.cam);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'shot_' + $('cmp-mode').value + '_' + tag + '_'
          + String(nm || '').replace(/[^\w.-]+/g, '_').slice(0, 40) + '.png';
        document.body.appendChild(a); a.click(); a.remove();
      };
      shot(SA, 'A', nameA);
      await new Promise(r => setTimeout(r, 500));            // 브라우저 연속 다운로드 여유
      shot(SB, 'B', nameB);
    } finally {
      btn.disabled = false; btn.textContent = '투명샷 ×2';
    }
  };
  (function anim() {
    if (stopped || !overlay.isConnected) return;
    SA.renderer.render(SA.scene, SA.cam);
    SB.renderer.render(SB.scene, SB.cam);
    requestAnimationFrame(anim);
  })();
  } catch (e) {
    console.error('compare modal build failed:', e);
    $('cmp-status').textContent = '오류: ' + ((e && e.message) || e);
  }
}

/* ── wire up control panel ─────────────────────────────────── */
function wireControls(ctrlDiv, renderer, camera, controls, scene, state) {
  /* View Mode dropdown */
  const modeSel = ctrlDiv.querySelector('#view-mode');
  if (modeSel) {
    modeSel.addEventListener('change', () => {
      applyViewMode(state, modeSel.value);
      if (state.applyClip) state.applyClip();              // mode switches create fresh materials
    });
  }

  /* 단면 뷰 — clipping plane along µm-Y (scene Z): 논문 (b)/(e)식 단면/줌 구도를 어느 모드에서든 */
  const clipOn = ctrlDiv.querySelector('#clip-on'), clipPos = ctrlDiv.querySelector('#clip-pos');
  if (clipOn && clipPos) {
    renderer.localClippingEnabled = true;
    const applyClip = () => {
      const box = (state.data && state.data.box) || {};
      const y0 = box.y_min || 0, y1 = box.y_max || 50;
      const cut = y0 + (y1 - y0) * (parseFloat(clipPos.value) / 100);
      state.clipPlanes = clipOn.checked ? [new THREE.Plane(new THREE.Vector3(0, 0, -1), cut)] : null;
      scene.traverse(o => {
        if (o.material) {
          o.material.clippingPlanes = state.clipPlanes;
          if (state.clipPlanes) {                          // cut spheres read hollow with FrontSide —
            if (o.material.userData._baseSide === undefined) o.material.userData._baseSide = o.material.side;
            o.material.side = THREE.DoubleSide;            //   show interior surfaces at the cut
          } else if (o.material.userData._baseSide !== undefined) {
            o.material.side = o.material.userData._baseSide;
            delete o.material.userData._baseSide;
          }
          o.material.needsUpdate = true;
        }
      });
    };
    clipOn.addEventListener('change', applyClip);
    clipPos.addEventListener('input', applyClip);
    state.applyClip = applyClip;
  }

  ctrlDiv.querySelectorAll('input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', () => {
      const layer = cb.dataset.layer;
      if (layer === 'percolation') {
        applyPercolation(state, cb.checked);
      } else if (state.meshes[layer]) {
        state.meshes[layer].visible = cb.checked;
      }
    });
  });

  // Force chain toggle
  const fcToggle = ctrlDiv.querySelector('#force-chain-toggle');
  if (fcToggle) {
    fcToggle.addEventListener('change', async () => {
      if (fcToggle.checked) {
        if (!state.forceChainGroup) {
          // Load and build force chain lines
          const url = state.dataUrl.replace('/3d-data', '/force-chains');
          try {
            const res = await fetch(url);
            const chains = await res.json();
            // Limit to top N chains by force for performance
            let display = chains;
            if (chains.length > 5000) {
              display = chains.sort((a, b) => b.fn - a.fn).slice(0, 5000);
            }
            console.log('Force chains loaded:', chains.length, ', displaying:', display.length);
            const group = new THREE.Group();
            if (display.length > 0) {
              const fnValues = display.map(c => c.fn);
              const fnMax = Math.max(...fnValues);
              const fnMin = Math.min(...fnValues);
              display.forEach(c => {
                const p1 = new THREE.Vector3(...c.p1);
                const p2 = new THREE.Vector3(...c.p2);
                const t = fnMax > fnMin ? (c.fn - fnMin) / (fnMax - fnMin) : 0.5;
                // Color: blue(low) → yellow → red(high)
                const color = new THREE.Color();
                color.setHSL(0.15 - t * 0.15, 1, 0.85 - t * 0.45);  // light yellow(low) → dark red(high)
                const radius = 0.5 + t * 2.0;  // thicker = stronger
                const curve = new THREE.LineCurve3(p1, p2);
                const geo = new THREE.TubeGeometry(curve, 1, radius, 4, false);
                const mat = new THREE.MeshBasicMaterial({color, transparent: true, opacity: 0.15 + t * 0.85});
                group.add(new THREE.Mesh(geo, mat));
              });
            }
            state.forceChainGroup = group;
            scene.add(group);
          } catch(e) {
            console.warn('Force chain data not available:', e);
          }
        } else {
          state.forceChainGroup.visible = true;
        }
      } else if (state.forceChainGroup) {
        state.forceChainGroup.visible = false;
      }
    });
  }

  ctrlDiv.querySelectorAll('button').forEach(btn => {
    const action = btn.dataset.action;
    btn.addEventListener('click', () => {
      if (action === 'resetView') {
        camera.position.copy(state.defaultCamPos);
        controls.target.copy(state.defaultTarget);
        controls.update();
      } else if (action === 'colorbar') {
        // 논문용 컬러바 PNG — 모드별 스펙 (econn은 applyViewMode가 실측 p5–p95를 state.cbarSpec에 저장)
        const _vm = (document.getElementById('view-mode') || {}).value || '';
        const _SPEC = {
          jrxn: { map: 'jet', gamma: 1.6, title: 'Reaction current i/\u012b (low-rate charging, p99.8)', left: '0', right: 'hot' },
          je_field: { map: 'jet', gamma: 1.6, title: '|J_e| relative current density (p99.8-normalized)', left: '0', right: 'high' },
          ji_field: { map: 'jet', gamma: 1.6, title: '|J_ion| relative current density (p99.8-normalized)', left: '0', right: 'high' },
          je: { map: 'jet', gamma: 1.6, title: '|J_z| per-AM relative (wetted collector, p99.8)', left: '0', right: 'high' },
          jb: { map: 'jet', gamma: 1.6, title: '|J_z| per-AM relative (bare collector, p99.8)', left: '0', right: 'high' },
          je_delta: { map: 'coolwarm', title: '\u0394 redistribution log\u2082(j_bare/j_wetted)', left: '\u00d70.71', mid: '1', right: '\u00d71.4' },
        };
        const _sp = (state.cbarSpec && (state.cbarSpecMode === _vm || _vm === 'econn'))
                    ? state.cbarSpec : _SPEC[_vm];
        if (_sp) exportColorbarPNG(_sp, 'colorbar_' + (_vm || 'view') + '.png');
        else alert('이 모드는 컬러바 스케일이 없어요 — 전류밀도/반응/econn/Δ 모드에서 사용하세요.');
      } else if (action === 'screenshot') {
        // Hide decoration objects (bbox, grid, axis labels) for clean screenshot
        const hiddenDecorations = [];
        scene.traverse((obj) => {
          if (obj.userData && obj.userData.isDecoration && obj.visible) {
            obj.visible = false;
            hiddenDecorations.push(obj);
          }
        });
        // Current-density FIELD / je modes read as "hot paths on a DARK field" — a transparent PNG
        // drops the deep-blue cold field on white paper, breaking the figure.  Keep the dark canvas
        // background for those; keep transparent for structural modes (clean slide overlay).
        const _mode = (ctrlDiv.querySelector('#view-mode') || {}).value || '';
        const darkField = ['je_field', 'ji_field', 'je'].includes(_mode);   // je_delta = coolwarm/흰중앙 → 투명배경 유지
        const prevBg = scene.background;
        const prevClear = new THREE.Color();
        renderer.getClearColor(prevClear);
        const prevAlpha = renderer.getClearAlpha();
        if (darkField) { scene.background = new THREE.Color(COL.BG); renderer.setClearColor(COL.BG, 1); }
        else { scene.background = null; renderer.setClearColor(0x000000, 0); }
        // 6× supersampled capture (paper-grade PNG — ~6000px on a 1000px canvas)
        const dataUrl = captureHighRes(renderer, scene, camera, 6);
        // Restore background + decorations
        scene.background = prevBg;
        renderer.setClearColor(prevClear, prevAlpha);
        hiddenDecorations.forEach(obj => { obj.visible = true; });
        renderer.render(scene, camera);
        // Prompt user with Save As dialog (always asks destination)
        saveWithDialog(dataUrl, 'electrode_3d.png', btn, 'Screenshot');
      } else if (action === 'pathOnly') {
        showPathOnlyView(renderer, scene, camera, state);
      } else if (action === 'amCloseup') {
        showAMCloseupView(state);
      } else if (action === 'analysisSummary') {
        showMPMAnalysisSummary(state);
      } else if (action === 'mechReaction') {
        showMechReactionModal(state);
      }
    });
  });

  /* zoom slider */
  const zoomDiv = ctrlDiv._zoomDiv;
  if (zoomDiv) {
    const slider = zoomDiv.querySelector('#zoom-slider');
    const zoomIn = zoomDiv.querySelector('#zoom-in');
    const zoomOut = zoomDiv.querySelector('#zoom-out');

    function setZoom(sliderVal) {
      sliderVal = Math.max(30, Math.min(350, sliderVal));
      const dist = 380 - sliderVal;  // slider↑ = closer
      const dir = camera.position.clone().sub(controls.target).normalize();
      camera.position.copy(controls.target).addScaledVector(dir, dist);
      controls.update();
      slider.value = sliderVal;
    }

    slider.addEventListener('input', () => setZoom(parseInt(slider.value)));
    zoomIn.addEventListener('click', () => setZoom(parseInt(slider.value) + 20));
    zoomOut.addEventListener('click', () => setZoom(parseInt(slider.value) - 20));

    // Sync slider when wheel zoom changes camera distance
    controls.addEventListener('change', () => {
      const dist = camera.position.distanceTo(controls.target);
      slider.value = Math.max(30, Math.min(350, 380 - Math.round(dist)));
    });
  }
}

/* ── Path Only View (interactive 3D popup) ───────────────── */
function showPathOnlyView(renderer, scene, camera, state) {
  if (!state.pathGroup) {
    alert('먼저 Percolating Path를 선택하세요.');
    return;
  }

  const clusters = ((state.data.clusters || {}).clusters) || [];
  const cidx = state.currentClusterIdx || 0;
  const cluster = clusters[cidx];
  const pathIdx = state.currentPathIdx || 0;
  const allPaths = cluster ? (cluster.paths || (cluster.path ? [cluster.path] : [])) : [];
  const pathData = allPaths[pathIdx];

  if (!pathData || !pathData.ids) {
    alert('경로 데이터가 없습니다.');
    return;
  }

  // Build unwrapped path
  const box = state.data.box;
  const bx = box.x_max - box.x_min, by = box.y_max - box.y_min;
  const rawPts = pathData.ids.map(id => state.idIndex[id]).filter(Boolean);
  const unwrapped = [];
  let offX = 0, offY = 0;
  for (let i = 0; i < rawPts.length; i++) {
    const p = rawPts[i];
    let x = p.x + offX, y = p.y + offY;
    if (i > 0) {
      const prev = unwrapped[i-1];
      const dx = (p.x + offX) - prev.x;
      const dy = (p.y + offY) - prev.z;
      if (Math.abs(dx) > bx * 0.5) { offX -= Math.sign(dx) * bx; x = p.x + offX; }
      if (Math.abs(dy) > by * 0.5) { offY -= Math.sign(dy) * by; y = p.y + offY; }
    }
    unwrapped.push(new THREE.Vector3(x, p.z, y));
  }
  // Path is kept at its original (unwrapped) coordinates so that the bbox,
  // axis labels (X/Y/Z), and SE context cloud all share the same frame.
  // The unwrap above already removes periodic jumps; no extra centering.

  // Create modal with canvas
  const overlay = document.createElement('div');
  overlay.className = 'path-modal-overlay';
  const cat = pathData.category || '';
  const catLabel = cat === 'best' ? 'Best' : cat === 'worst' ? 'Worst' : 'Mean';
  overlay.innerHTML = `
    <div class="path-modal" style="width:700px;max-width:90vw">
      <button class="path-modal-close" onclick="this.closest('.path-modal-overlay').remove()">&times;</button>
      <div style="font-size:14px;font-weight:bold;margin-bottom:8px;text-align:center">Li⁺ Ion Path (${catLabel})</div>
      <div id="path-viewer-container" style="width:100%;height:500px;border-radius:8px;overflow:hidden;background:#f5f5f5"></div>
      <div class="path-modal-info" style="text-align:center;margin-top:10px">
        Cluster #${cidx} | ${cluster.size} SE | τ = ${pathData.tortuosity} | Path: ${pathData.path_length} μm | Z: ${pathData.z_distance} μm
      </div>
      <div class="path-modal-context" style="display:flex;justify-content:center;align-items:center;gap:12px;margin-top:8px;font-size:13px;color:#444">
        <label style="display:inline-flex;align-items:center;gap:4px;cursor:pointer">
          <input type="checkbox" id="path-se-context-toggle" checked> SE context
        </label>
        <label style="display:inline-flex;align-items:center;gap:6px;cursor:pointer">
          opacity
          <input type="range" id="path-se-context-opacity" min="0" max="100" value="10" style="width:80px;vertical-align:middle">
          <span id="path-se-context-opacity-val" style="display:inline-block;width:30px;text-align:right">0.10</span>
        </label>
      </div>
      <div class="path-modal-actions">
        <button id="path-screenshot-btn">PNG 다운로드</button>
        <button onclick="this.closest('.path-modal-overlay').remove()">닫기</button>
      </div>
    </div>`;
  document.body.appendChild(overlay);
  overlay.onclick = (e) => { if (e.target === overlay) { cancelAnimationFrame(pathAnimId); overlay.remove(); }};

  // Create separate Three.js scene for path
  const container = document.getElementById('path-viewer-container');
  const r2 = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: true });
  r2.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  r2.setSize(container.clientWidth, container.clientHeight);
  r2.setClearColor(0xf5f5f5, 1);
  container.appendChild(r2.domElement);

  const s2 = new THREE.Scene();
  const c2 = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 10000);
  const ctrl2 = new OrbitControls(c2, r2.domElement);
  ctrl2.enableDamping = true;
  ctrl2.dampingFactor = 0.12;
  ctrl2.enableZoom = true;
  ctrl2.zoomSpeed = 1.0;

  s2.add(new THREE.AmbientLight(0xffffff, 0.5));
  const dl = new THREE.DirectionalLight(0xffffff, 0.8);
  dl.position.set(1, 1.5, 1);
  s2.add(dl);

  // Bounding box
  const bw = box.x_max-box.x_min, bh = box.z_max-box.z_min, bd = box.y_max-box.y_min;
  const cx = (box.x_min+box.x_max)/2, cy = (box.z_min+box.z_max)/2, cz = (box.y_min+box.y_max)/2;
  const bbEdges = new THREE.EdgesGeometry(new THREE.BoxGeometry(bw, bh, bd));
  const bbLine = new THREE.LineSegments(bbEdges, new THREE.LineBasicMaterial({color: 0x999999}));
  bbLine.position.set(cx, cy, cz);
  bbLine.userData.isDecoration = true;
  bbLine.userData.isBbox = true;
  s2.add(bbLine);

  // Grid (kept in screenshots — provides spatial reference)
  const grid = new THREE.GridHelper(Math.max(bw,bd)*1.2, 20, 0xcccccc, 0xe0e0e0);
  grid.position.set(cx, box.z_min, cz);
  grid.userData.isDecoration = true;
  grid.userData.isGrid = true;
  s2.add(grid);

  // Translucent SE particles for spatial context (toggleable from modal UI).
  // Drawn before path tubes so the path renders on top with depth.
  // No position offset — path/bbox/axes/SE all share original coordinate frame.
  let seContextMesh = null;
  if (state.seParticles && state.seParticles.length) {
    seContextMesh = createInstancedSpheres(
      state.seParticles, 16, COL.SE, 0.10, true
    );
    if (seContextMesh) {
      seContextMesh.userData.isSEContext = true;
      seContextMesh.renderOrder = -1;
      s2.add(seContextMesh);
    }
  }

  // Path tubes
  for (let j = 0; j < unwrapped.length - 1; j++) {
    const seg = new THREE.TubeGeometry(new THREE.LineCurve3(unwrapped[j], unwrapped[j+1]), 1, 0.6, 6, false);
    s2.add(new THREE.Mesh(seg, new THREE.MeshPhongMaterial({color: COL.PATH, emissive: COL.PATH, emissiveIntensity: 0.5})));
  }
  // Start/end
  const mkS = (pos, color) => {
    const s = new THREE.Mesh(new THREE.SphereGeometry(2, 12, 12), new THREE.MeshPhongMaterial({color}));
    s.position.copy(pos); return s;
  };
  s2.add(mkS(unwrapped[0], 0x22D3EE));
  s2.add(mkS(unwrapped[unwrapped.length-1], 0xF87171));

  // Wire up SE context toggle + opacity slider
  const seToggle = document.getElementById('path-se-context-toggle');
  const seOpaSlider = document.getElementById('path-se-context-opacity');
  const seOpaVal = document.getElementById('path-se-context-opacity-val');
  if (seToggle && seContextMesh) {
    seToggle.addEventListener('change', (e) => {
      seContextMesh.visible = e.target.checked;
    });
  }
  if (seOpaSlider && seContextMesh) {
    seOpaSlider.addEventListener('input', (e) => {
      const o = parseInt(e.target.value, 10) / 100;
      seContextMesh.material.opacity = o;
      seContextMesh.material.needsUpdate = true;
      if (seOpaVal) seOpaVal.textContent = o.toFixed(2);
    });
  }

  // Axis labels
  addAxisLabels(s2, box);

  // Camera
  const maxDim = Math.max(bw, bh, bd);
  c2.position.set(cx + maxDim*1.2, cy + maxDim*0.8, cz + maxDim*1.2);
  ctrl2.target.set(cx, cy, cz);
  ctrl2.update();

  // Zoom slider
  const zoomDiv = document.createElement('div');
  zoomDiv.style.cssText = 'position:absolute;bottom:10px;right:10px;display:flex;gap:4px;align-items:center;background:rgba(22,25,46,.8);padding:4px 8px;border-radius:6px;z-index:10';
  zoomDiv.innerHTML = '<button id="pv-zo" style="background:#555;color:#fff;border:none;border-radius:3px;width:20px;height:20px;cursor:pointer">−</button><input id="pv-zs" type="range" min="30" max="350" value="200" style="width:80px"><button id="pv-zi" style="background:#555;color:#fff;border:none;border-radius:3px;width:20px;height:20px;cursor:pointer">+</button>';
  container.style.position = 'relative';
  container.appendChild(zoomDiv);

  function setZoom2(sliderVal) {
    sliderVal = Math.max(30, Math.min(350, sliderVal));
    const dist = 380 - sliderVal;  // slider↑ = closer
    const dir = c2.position.clone().sub(ctrl2.target).normalize();
    c2.position.copy(ctrl2.target).addScaledVector(dir, dist);
    ctrl2.update();
    document.getElementById('pv-zs').value = sliderVal;
  }
  document.getElementById('pv-zs').addEventListener('input', e => setZoom2(parseInt(e.target.value)));
  document.getElementById('pv-zi').addEventListener('click', () => setZoom2(parseInt(document.getElementById('pv-zs').value) + 20));
  document.getElementById('pv-zo').addEventListener('click', () => setZoom2(parseInt(document.getElementById('pv-zs').value) - 20));

  // Sync slider when wheel zoom changes camera distance
  ctrl2.addEventListener('change', () => {
    const dist = c2.position.distanceTo(ctrl2.target);
    document.getElementById('pv-zs').value = Math.max(30, Math.min(350, 380 - Math.round(dist)));
  });

  // Screenshot — always prompts user with "Save As" dialog.
  // Path screenshot hides only the X/Y/Z axis text labels; bounding box and
  // grid are kept as spatial reference. Background is transparent so the PNG
  // overlays any PPT slide color cleanly.
  document.getElementById('path-screenshot-btn').addEventListener('click', async () => {
    const hidden = [];
    s2.traverse((obj) => {
      if (obj.userData && obj.userData.isAxisLabel && obj.visible) {
        obj.visible = false;
        hidden.push(obj);
      }
    });
    const prevBg = s2.background;
    const prevClear = new THREE.Color();
    r2.getClearColor(prevClear);
    const prevAlpha = r2.getClearAlpha();
    s2.background = null;
    r2.setClearColor(0x000000, 0);
    // 4× supersampled capture (publication-quality PNG)
    const dataUrl = captureHighRes(r2, s2, c2, 4);
    s2.background = prevBg;
    r2.setClearColor(prevClear, prevAlpha);
    hidden.forEach(obj => { obj.visible = true; });
    r2.render(s2, c2);
    const fname = `li_ion_path_${catLabel.toLowerCase()}_tau${pathData.tortuosity}.png`;
    await saveWithDialog(dataUrl, fname, document.getElementById('path-screenshot-btn'),
                         'PNG 다운로드');
  });

  // Animate
  let pathAnimId;
  function animPath() {
    pathAnimId = requestAnimationFrame(animPath);
    ctrl2.update();
    r2.render(s2, c2);
  }
  animPath();

  // Cleanup on close
  overlay.querySelector('.path-modal-close').addEventListener('click', () => {
    cancelAnimationFrame(pathAnimId);
    r2.dispose();
    overlay.remove();
  });
}

/* ── AM Close-up View ───────────────────────────────────────
 * Pops a modal that centers on a chosen AM particle and renders
 * its local neighborhood (other AM + SE within a sphere of
 * radius `R_target × radiusFactor`). Useful for slide figures
 * showing one AM grain surrounded by SE & other AM particles.
 *
 * Default target = AM closest to box centroid (most "central").
 * UI lets user:
 *   - cycle target candidates (Prev / Next, ranked by centrality)
 *   - adjust neighborhood radius (radiusFactor slider 2× - 8×)
 *   - toggle AM_P / AM_S / SE visibility
 *   - PNG download (4× supersampled, transparent bg)
 */
function showAMCloseupView(state) {
  const amAll = state.amParticles || [];
  if (!amAll.length) {
    alert('AM particles not loaded.');
    return;
  }
  const seAll = state.seParticles || [];
  const box = state.data.box;
  const cx0 = (box.x_min + box.x_max) / 2;
  const cy0 = (box.y_min + box.y_max) / 2;
  const cz0 = (box.z_min + box.z_max) / 2;

  // Rank AM candidates by distance to box centroid (ascending)
  // Largest particles first when distance ties (more visually impactful)
  const ranked = amAll.map(p => {
    const d2 = (p.x - cx0)**2 + (p.y - cy0)**2 + (p.z - cz0)**2;
    return { p, d2 };
  }).sort((a, b) => {
    const da = a.d2, db = b.d2;
    if (Math.abs(da - db) < 1e-6) return b.p.r - a.p.r;
    return da - db;
  });

  let candIdx = 0;
  let radiusFactor = 4.0;  // neighbor sphere radius = R_target × this

  // Build modal HTML
  const overlay = document.createElement('div');
  overlay.className = 'path-modal-overlay';
  overlay.innerHTML = `
    <div class="path-modal" style="width:760px;max-width:92vw">
      <button class="path-modal-close">&times;</button>
      <div style="font-size:14px;font-weight:bold;margin-bottom:8px;text-align:center">
        AM Close-up — central particle + neighborhood
      </div>
      <div id="amcu-container" style="width:100%;height:520px;border-radius:8px;overflow:hidden;background:#f5f5f5;position:relative"></div>
      <div id="amcu-info" style="text-align:center;margin-top:10px;font-size:13px;color:#444"></div>
      <div style="display:flex;justify-content:center;align-items:center;gap:12px;margin-top:8px;font-size:13px;color:#444;flex-wrap:wrap">
        <button id="amcu-prev" style="padding:2px 8px">◀ Prev</button>
        <button id="amcu-next" style="padding:2px 8px">Next ▶</button>
        <label style="display:inline-flex;align-items:center;gap:6px">
          radius
          <input type="range" id="amcu-radius" min="20" max="80" value="40" step="2" style="width:90px;vertical-align:middle">
          <span id="amcu-radius-val" style="display:inline-block;width:30px;text-align:right">4.0×</span>
        </label>
        <label><input type="checkbox" id="amcu-am_p" checked> AM_P</label>
        <label><input type="checkbox" id="amcu-am_s" checked> AM_S</label>
        <label><input type="checkbox" id="amcu-se" checked> SE</label>
      </div>
      <div class="path-modal-actions">
        <button id="amcu-screenshot">PNG 다운로드</button>
        <button id="amcu-close">닫기</button>
      </div>
    </div>`;
  document.body.appendChild(overlay);

  const container = document.getElementById('amcu-container');
  const r3 = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: true });
  r3.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  r3.setSize(container.clientWidth, container.clientHeight);
  r3.setClearColor(0xf5f5f5, 1);
  container.appendChild(r3.domElement);

  const s3 = new THREE.Scene();
  const c3 = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 10000);
  const ctrl3 = new OrbitControls(c3, r3.domElement);
  ctrl3.enableDamping = true;
  ctrl3.dampingFactor = 0.12;

  s3.add(new THREE.AmbientLight(0xffffff, 0.45));
  const dl = new THREE.DirectionalLight(0xffffff, 0.85);
  dl.position.set(1, 1.2, 1);
  s3.add(dl);

  // State holders for current scene contents — replaced on rebuild
  let activeMeshes = [];
  let centerHalo = null;

  function clearScene() {
    activeMeshes.forEach(m => {
      s3.remove(m);
      if (m.geometry) m.geometry.dispose();
      if (m.material) m.material.dispose();
    });
    activeMeshes = [];
    if (centerHalo) {
      s3.remove(centerHalo);
      centerHalo.geometry.dispose();
      centerHalo.material.dispose();
      centerHalo = null;
    }
  }

  function build() {
    clearScene();
    const target = ranked[candIdx].p;
    const tx = target.x, ty = target.y, tz = target.z;
    const r_neighbor = target.r * radiusFactor;
    const r2 = r_neighbor * r_neighbor;

    // Filter neighbors by Euclidean distance to target center
    const inRange = (arr) => arr.filter(p => {
      const dx = p.x - tx, dy = p.y - ty, dz = p.z - tz;
      return (dx*dx + dy*dy + dz*dz) <= r2;
    });

    const showAMP = document.getElementById('amcu-am_p').checked;
    const showAMS = document.getElementById('amcu-am_s').checked;
    const showSE  = document.getElementById('amcu-se').checked;

    const neighAMP = showAMP ? inRange(state.amPParticles || []) : [];
    const neighAMS = showAMS ? inRange(state.amSParticles || []) : [];
    const neighSE  = showSE  ? inRange(seAll) : [];

    // Always include the target itself, even when its type checkbox is off,
    // so the user can still see what's being centered.
    const tgtArr = [target];

    if (neighAMP.length) {
      const m = createInstancedSpheres(neighAMP, 16, COL.AM_P, 1.0, false);
      if (m) { s3.add(m); activeMeshes.push(m); }
    }
    if (neighAMS.length) {
      const m = createInstancedSpheres(neighAMS, 16, COL.AM_S, 1.0, false);
      if (m) { s3.add(m); activeMeshes.push(m); }
    }
    if (neighSE.length) {
      const m = createInstancedSpheres(neighSE, 14, COL.SE, 0.85, true);
      if (m) { s3.add(m); activeMeshes.push(m); }
    }
    // Highlight target with a slightly brighter halo (regardless of type)
    {
      const m = createInstancedSpheres(tgtArr, 24,
        target.type === 'AM_S' ? 0xb0b0b0 : 0x444444, 1.0, false);
      if (m) { s3.add(m); activeMeshes.push(m); }
    }
    // Translucent halo around target showing the neighborhood radius
    {
      const haloGeo = new THREE.SphereGeometry(r_neighbor, 32, 24);
      const haloMat = new THREE.MeshBasicMaterial({
        color: 0x4f9bff, transparent: true, opacity: 0.06,
        side: THREE.BackSide, depthWrite: false,
      });
      centerHalo = new THREE.Mesh(haloGeo, haloMat);
      centerHalo.position.set(tx, tz, ty);  // Z-up swap
      s3.add(centerHalo);
    }

    // Camera framing — fit the neighbor sphere
    const tCam = new THREE.Vector3(tx, tz, ty);
    ctrl3.target.copy(tCam);
    const camDist = r_neighbor * 2.4;
    c3.position.set(tx + camDist, tz + camDist * 0.55, ty + camDist);
    ctrl3.update();

    // Info text
    const info = document.getElementById('amcu-info');
    if (info) {
      const total = neighAMP.length + neighAMS.length + neighSE.length;
      info.innerHTML =
        `target: <b>${target.type}</b> id=${target.id}, R=${target.r.toFixed(2)}μm, ` +
        `pos=(${tx.toFixed(1)}, ${ty.toFixed(1)}, ${tz.toFixed(1)}) | ` +
        `neighbors within ${r_neighbor.toFixed(1)}μm: ` +
        `<span style="color:#222">AM_P=${neighAMP.length}</span>, ` +
        `<span style="color:#888">AM_S=${neighAMS.length}</span>, ` +
        `<span style="color:#bfa600">SE=${neighSE.length}</span>` +
        ` (total ${total}) — candidate ${candIdx + 1}/${ranked.length}`;
    }
  }

  build();

  // Wire up controls
  document.getElementById('amcu-prev').addEventListener('click', () => {
    candIdx = (candIdx - 1 + ranked.length) % ranked.length;
    build();
  });
  document.getElementById('amcu-next').addEventListener('click', () => {
    candIdx = (candIdx + 1) % ranked.length;
    build();
  });
  document.getElementById('amcu-radius').addEventListener('input', (e) => {
    radiusFactor = parseInt(e.target.value, 10) / 10;
    document.getElementById('amcu-radius-val').textContent = radiusFactor.toFixed(1) + '×';
    build();
  });
  ['amcu-am_p', 'amcu-am_s', 'amcu-se'].forEach(id => {
    document.getElementById(id).addEventListener('change', build);
  });

  // Screenshot
  document.getElementById('amcu-screenshot').addEventListener('click', async () => {
    const prevBg = s3.background;
    const prevClear = new THREE.Color();
    r3.getClearColor(prevClear);
    const prevAlpha = r3.getClearAlpha();
    s3.background = null;
    r3.setClearColor(0x000000, 0);
    const dataUrl = captureHighRes(r3, s3, c3, 4);
    s3.background = prevBg;
    r3.setClearColor(prevClear, prevAlpha);
    r3.render(s3, c3);
    const target = ranked[candIdx].p;
    const fname = `am_closeup_${target.type}_id${target.id}.png`;
    await saveWithDialog(dataUrl, fname,
      document.getElementById('amcu-screenshot'), 'PNG 다운로드');
  });

  // Animate
  let amcuAnimId;
  function animLoop() {
    amcuAnimId = requestAnimationFrame(animLoop);
    ctrl3.update();
    r3.render(s3, c3);
  }
  animLoop();

  // Cleanup
  function close() {
    cancelAnimationFrame(amcuAnimId);
    clearScene();
    r3.dispose();
    overlay.remove();
  }
  overlay.querySelector('.path-modal-close').addEventListener('click', close);
  document.getElementById('amcu-close').addEventListener('click', close);
  overlay.onclick = (e) => { if (e.target === overlay) close(); };
}


/* ── Save a Blob with native Save-As dialog (CSV / PNG / any mime) ───
 * Mirrors saveWithDialog() but starts from a Blob instead of a base64
 * dataURL, so binary streams from fetch() can be saved directly.
 */
async function saveBlobWithDialog(blob, defaultName, btn, resetLabel) {
  const flash = (msg) => {
    if (btn) {
      const orig = resetLabel || btn.textContent;
      btn.textContent = msg;
      setTimeout(() => { btn.textContent = orig; }, 1500);
    }
  };
  const ext = (defaultName.split('.').pop() || '').toLowerCase();
  const accept = {
    png: { description: 'PNG image', accept: { 'image/png': ['.png'] } },
    csv: { description: 'CSV file',  accept: { 'text/csv':  ['.csv'] } },
  }[ext] || { description: 'File', accept: { [blob.type || 'application/octet-stream']: ['.' + ext] } };
  if (window.showSaveFilePicker) {
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: defaultName,
        types: [accept],
      });
      const writable = await handle.createWritable();
      await writable.write(blob);
      await writable.close();
      flash('✓ Saved');
      return;
    } catch (e) {
      if (e.name === 'AbortError') return;
      console.warn('showSaveFilePicker failed, falling back:', e);
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = defaultName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  flash('✓ Downloaded');
}




/* ── Z-profile Data Hub ─────────────────────────────────────────
 * Single unified modal that consolidates the brittle, stress and
 * combined-overlay z-profile downloads behind a tab bar.  Each tab
 * shows its own data view and renders the PNG/CSV download buttons
 * pointing at the right Flask endpoint.
 *
 * Replaces the previous showBrittleZProfileModal /
 * showStressZProfileModal functions so every view-mode legend
 * button opens the same Hub; the `defaultTab` argument just selects
 * which tab is active on open.
 */
async function showZProfileDataHub(state, defaultTab) {
  const dataUrl = state.dataUrl || '';
  const urlOf   = (suffix) => dataUrl.replace('/3d-data', suffix);

  const overlay = document.createElement('div');
  overlay.className = 'path-modal-overlay';
  overlay.innerHTML = `
    <div class="path-modal" style="width:980px;max-width:96vw">
      <button class="path-modal-close">&times;</button>
      <div style="font-size:14px;font-weight:bold;margin-bottom:6px;text-align:center">
        Z-profile Data Hub
      </div>
      <div id="zh-summary" class="path-modal-info" style="text-align:center;margin-bottom:8px;font-size:12px">
        Loading…
      </div>
      <div style="display:flex;gap:4px;margin-bottom:8px;border-bottom:1px solid #e5e7eb">
        <button class="zh-tab" data-tab="brittle"   style="${tabStyle(false)}">Brittle stages</button>
        <button class="zh-tab" data-tab="stress"    style="${tabStyle(false)}">Stress hotspots</button>
        <button class="zh-tab" data-tab="coverage"  style="${tabStyle(false)}">Coverage (AM)</button>
        <button class="zh-tab" data-tab="combined"  style="${tabStyle(false)}">Combined overlay</button>
        <button class="zh-tab" data-tab="se"        style="${tabStyle(false)}">SE Diagnostics</button>
      </div>
      <div id="zh-content" style="max-height:58vh;overflow:auto;border:1px solid #e5e7eb;border-radius:6px">
        <div style="padding:30px;text-align:center;color:#888">Loading…</div>
      </div>
      <div class="path-modal-actions" style="justify-content:space-between">
        <span id="zh-context" style="color:#6b7280;font-size:12px;align-self:center">—</span>
        <span>
          <button id="zh-png-btn">PNG 다운로드</button>
          <button id="zh-csv-btn">CSV 다운로드</button>
          <button id="zh-close-btn">닫기</button>
        </span>
      </div>
    </div>`;
  document.body.appendChild(overlay);

  const close = () => overlay.remove();
  overlay.querySelector('.path-modal-close').addEventListener('click', close);
  document.getElementById('zh-close-btn').addEventListener('click', close);
  overlay.onclick = (e) => { if (e.target === overlay) close(); };

  /* Fetch brittle + stress + coverage data concurrently.  Coverage
   * is optional — older cases may not have coverage_per_am.csv yet,
   * so we treat a 404 there as "tab disabled" rather than fatal. */
  let brittle, stress, coverage = null, fetchErr;
  try {
    const [rB, rS, rC] = await Promise.all([
      fetch(urlOf('/brittle-z-data')),
      fetch(urlOf('/stress-z-data')),
      fetch(urlOf('/coverage-z-data')),
    ]);
    if (!rB.ok) throw new Error('brittle: HTTP ' + rB.status);
    if (!rS.ok) throw new Error('stress: HTTP ' + rS.status);
    brittle = await rB.json();
    stress  = await rS.json();
    if (rC.ok) coverage = await rC.json();
  } catch (e) {
    fetchErr = e;
  }
  if (fetchErr) {
    document.getElementById('zh-content').innerHTML =
      `<div style="padding:30px;color:#b91c1c">Failed to load: ${fetchErr.message || fetchErr}<br>
       <span style="color:#6b7280;font-size:12px">서버 로그(/tmp/flask.log) traceback 확인.</span></div>`;
    return;
  }

  /* Summary line (combines info from both endpoints) */
  const covSummary = coverage
    ? ` · coverage: ${coverage.n_with_cov} AM, mean ${(coverage.cMean || 0).toFixed(1)}%`
    : ' · coverage: no coverage_per_am.csv';
  document.getElementById('zh-summary').innerHTML =
    `<b>${brittle.case_name}</b> · thickness ${(brittle.thickness_um || 0).toFixed(1)} µm<br>`
    + `<span style="color:#6b7280">brittle: ${brittle.n_total} AM-AM contacts `
    + `(damaged ${brittle.n_damaged}, ${(brittle.damaged_pct || 0).toFixed(1)}%) · `
    + `stress: ${stress.n_with_stress} particles ≥ 0 MPa, median ${(stress.sMed || 0).toFixed(0)} / p95 ${(stress.sHi || 0).toFixed(0)} MPa`
    + `${covSummary}</span>`;

  /* Tab state machine — coverage tab disabled if no data */
  if (!coverage) {
    const covTab = overlay.querySelector('.zh-tab[data-tab="coverage"]');
    if (covTab) {
      covTab.disabled = true;
      covTab.style.opacity = '0.45';
      covTab.style.cursor = 'not-allowed';
      covTab.title = 'No coverage_per_am.csv for this case';
    }
  }
  const tabs = ['brittle', 'stress', 'coverage', 'combined', 'se'];
  let active = tabs.includes(defaultTab) ? defaultTab : 'brittle';
  if (active === 'coverage' && !coverage) active = 'brittle';
  /* SE tab is only meaningful when SE diagnostic data was computed
   * (state.data.aux.se_n_percolating > 0). If not, gray out. */
  const aux = (state.data && state.data.aux) || {};
  const seReady = (aux.se_n_percolating || 0) > 0;
  if (!seReady) {
    const seTab = overlay.querySelector('.zh-tab[data-tab="se"]');
    if (seTab) {
      seTab.disabled = true;
      seTab.style.opacity = '0.45';
      seTab.style.cursor = 'not-allowed';
      seTab.title = 'No SE percolation data — run reanalysis';
    }
    if (active === 'se') active = 'brittle';
  }
  const tabEls = overlay.querySelectorAll('.zh-tab');
  const content = document.getElementById('zh-content');
  const ctxEl = document.getElementById('zh-context');
  const pngBtn = document.getElementById('zh-png-btn');
  const csvBtn = document.getElementById('zh-csv-btn');

  function selectTab(name) {
    active = name;
    tabEls.forEach(el => el.setAttribute('style',
      tabStyle(el.dataset.tab === name)));
    /* SE tab has 5 file-specific buttons inside its own content — the
     * shared bottom PNG/CSV pair doesn't apply. Hide them there. */
    const onSE = (name === 'se');
    pngBtn.style.display = onSE ? 'none' : '';
    csvBtn.style.display = onSE ? 'none' : '';
    if (name === 'brittle') {
      content.innerHTML = renderBrittleTable(brittle);
      ctxEl.textContent = 'Lawn fracture stage counts per z-bin (force-based)';
    } else if (name === 'stress') {
      content.innerHTML = renderStressTable(stress);
      ctxEl.textContent = 'Per-particle max contact pressure (MPa) stats per z-bin';
    } else if (name === 'coverage') {
      content.innerHTML = coverage ? renderCoverageTable(coverage)
        : `<div style="padding:30px;color:#888">No coverage data — run scripts/coverage_physics_vs_hertzian.py first.</div>`;
      ctxEl.textContent = 'Per-AM SE-coverage % stats per z-bin (RdYlGn 5-class bands)';
    } else if (name === 'se') {
      content.innerHTML = renderSeDiagnosticsHub(state);
      ctxEl.textContent = 'SE network connectivity diagnostics — percolation, articulation, dead-ends, bottlenecks';
      /* Wire the 5 per-file download buttons to the existing
       * exportSeDiagnostics helper, which already routes by data-attr. */
      content.querySelectorAll('[data-sed-export]').forEach(b => {
        b.addEventListener('click', () => exportSeDiagnostics(state, b));
      });
    } else {
      content.innerHTML =
        `<div style="text-align:center;padding:10px">
           <img src="${urlOf('/combined-z-png')}" alt="Combined z-profile"
                style="max-width:100%;height:auto;border-radius:4px">
           <div style="font-size:12px;color:#6b7280;margin-top:6px">
             4-panel overlay — brittle stages + stress brackets +
             damage-vs-pressure correlation. PNG 다운로드로 고해상도 저장.
           </div>
         </div>`;
      ctxEl.textContent = 'Combined brittle + stress overlay (server-rendered)';
    }
  }
  tabEls.forEach(el => el.addEventListener('click',
    () => selectTab(el.dataset.tab)));
  selectTab(active);

  /* Download buttons route to whichever tab is active */
  pngBtn.addEventListener('click', async (ev) => {
    const btn = ev.currentTarget;
    btn.textContent = '… rendering';
    const suffix = active === 'brittle'  ? '/brittle-z-png'
                  : active === 'stress'   ? '/stress-z-png'
                  : active === 'coverage' ? '/coverage-z-png'
                  : '/combined-z-png';
    const prefix = active;
    try {
      const r = await fetch(urlOf(suffix));
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const blob = await r.blob();
      await saveBlobWithDialog(blob,
        `${prefix}_z_${brittle.case_name}.png`, btn, 'PNG 다운로드');
    } catch (e) {
      btn.textContent = 'Failed';
      console.error('PNG download failed', e);
      setTimeout(() => { btn.textContent = 'PNG 다운로드'; }, 1500);
    }
  });
  csvBtn.addEventListener('click', async (ev) => {
    const btn = ev.currentTarget;
    btn.textContent = '… fetching';
    const suffix = active === 'brittle'  ? '/brittle-z-csv'
                  : active === 'stress'   ? '/stress-z-csv'
                  : active === 'coverage' ? '/coverage-z-csv'
                  : '/combined-z-csv';
    const prefix = active;
    try {
      const r = await fetch(urlOf(suffix));
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const blob = await r.blob();
      await saveBlobWithDialog(blob,
        `${prefix}_z_${brittle.case_name}.csv`, btn, 'CSV 다운로드');
    } catch (e) {
      btn.textContent = 'Failed';
      console.error('CSV download failed', e);
      setTimeout(() => { btn.textContent = 'CSV 다운로드'; }, 1500);
    }
  });
}

function tabStyle(active) {
  return `flex:1;padding:7px 10px;border:none;background:${active?'#fff':'transparent'};
          color:${active?'#1f2937':'#6b7280'};
          border-bottom:2px solid ${active?'#2563eb':'transparent'};
          font:600 12px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
          letter-spacing:.2px;cursor:pointer;border-radius:4px 4px 0 0;
          transition:background .15s,color .15s,border-color .15s`;
}

/* SE Diagnostics tab body — summary stats + 5 per-file download
 * buttons (CSV particles / bn / clusters + PNG z-profile / stats).
 * Buttons carry data-sed-export attrs that the existing
 * exportSeDiagnostics() helper dispatches on. */
function renderSeDiagnosticsHub(state) {
  const aux = (state.data && state.data.aux) || {};
  const nPerc      = aux.se_n_percolating         || 0;
  const artPts     = aux.se_articulation_points   || [];
  const bnEdges    = aux.se_bottleneck_edges      || [];
  const deadEnds   = aux.se_dead_end_clusters     || [];
  const nBnBelow   = aux.se_n_bn_below_threshold;
  const medianNorm = aux.se_bn_median_norm;
  const thresholdNorm = aux.se_bn_threshold_norm;
  const deadTop = deadEnds.filter(d => d.type === 'top_only').length;
  const deadBot = deadEnds.filter(d => d.type === 'bottom_only').length;
  const narrowest     = bnEdges[0]?.area_um2;
  const narrowestNorm = bnEdges[0]?.area_norm;
  const cutFrac = nPerc ? (artPts.length / nPerc) : 0;

  const fmt  = (x, d=4) => (typeof x === 'number') ? x.toFixed(d) : '—';
  const cell = (label, val, sw) =>
    `<div style="background:#fff;border:1px solid #e5e7eb;border-radius:6px;
                 padding:8px 10px;display:flex;align-items:center;gap:10px">
       <span style="width:10px;height:18px;background:${sw};border-radius:2px;flex:none"></span>
       <div style="display:flex;flex-direction:column;line-height:1.2;flex:1;min-width:0">
         <span style="color:#6b7280;font-size:11px">${label}</span>
         <span style="font-weight:600;color:#0f172a;font-size:13px">${val}</span>
       </div>
     </div>`;

  const dlBtn = (kind, color, label, hint) =>
    `<button data-sed-export="${kind}"
       style="background:${color};color:#fff;border:none;border-radius:5px;
              padding:8px 14px;font-size:13px;font-weight:600;cursor:pointer;
              display:flex;flex-direction:column;align-items:flex-start;gap:2px;
              min-width:170px"
       title="${hint}">
       <span>${label}</span>
       <span style="font-weight:400;font-size:11px;opacity:.85">${hint}</span>
     </button>`;

  return `
    <div style="padding:14px 16px;background:#f9fafb">
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px">
        ${cell('Percolating SE (backbone)',    nPerc,                                  '#14b8a6')}
        ${cell('Articulation points (cut)',    artPts.length,                          '#facc15')}
        ${cell('cut fraction',                 fmt(cutFrac, 4),                        '#facc15')}
        ${cell('Dead-end — top only',          deadTop + ' cluster',                    '#ec4899')}
        ${cell('Dead-end — bottom only',       deadBot + ' cluster',                    '#f97316')}
        ${cell('Bottleneck list (capped)',     bnEdges.length,                          '#dc2626')}
        ${cell('Below-threshold bn (uncapped)', nBnBelow ?? '—',                       '#dc2626')}
        ${cell('Narrowest A/r²',               typeof narrowestNorm === 'number' ? fmt(narrowestNorm, 5) : '—', '#dc2626')}
        ${cell('Narrowest area',               typeof narrowest === 'number' ? fmt(narrowest, 5) + ' μm²' : '—', '#dc2626')}
        ${cell('Corpus median A/r²',           typeof medianNorm === 'number' ? fmt(medianNorm, 4) : '—', '#444')}
        ${cell('bn threshold (10% × median)',  typeof thresholdNorm === 'number' ? fmt(thresholdNorm, 4) : '—', '#444')}
        ${cell('Median × 10% rule',            'A/r² < threshold = narrow',             '#9ca3af')}
      </div>

      <div style="border-top:1px solid #e5e7eb;padding-top:12px">
        <div style="font-size:12px;color:#374151;font-weight:600;margin-bottom:8px">
          📥 다운로드 — 파일별로 따로 (5종)
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px">
          ${dlBtn('csv_particles', '#059669', 'CSV particles', 'id, x, y, z, radius, role')}
          ${dlBtn('csv_bn',        '#b91c1c', 'CSV bottleneck', 'id1, id2, area_um2, area_norm, r_min_um (+ header meta)')}
          ${dlBtn('csv_clusters',  '#7c3aed', 'CSV clusters',   'dead-end clusters: idx, type, size, ids')}
          ${dlBtn('png_zprofile',  '#2563eb', 'PNG z-profile',  '깊이별 cut / bn / dead-end 분포 차트')}
          ${dlBtn('png_stats',     '#374151', 'PNG stats',      '요약 통계 카드 (corpus percentile 포함)')}
        </div>
        <div style="margin-top:8px;font-size:11px;color:#6b7280;line-height:1.5">
          PNG stats는 corpus 비교 (cut_fraction / bn_below_frac percentile 막대)
          포함 — 27개 percolating case 중 이 case의 상대적 위치를 보여줍니다.<br>
          모든 파일은 클라이언트에서 실시간 생성. 서버 round-trip 없음.
        </div>
      </div>
    </div>`;
}

function renderBrittleTable(profile) {
  const stages = ['intact','microcrack','multicrack','fragmentation','pulverization'];
  const stageColor = {
    intact: '#d9d9d9', microcrack: '#ffeda0', multicrack: '#feb24c',
    fragmentation: '#f03b20', pulverization: '#800026',
  };
  const centers = profile.bin_centers_um || [];
  const edges   = profile.bin_edges_um   || [];
  const meanM   = profile.mean_m         || [];
  const cAll    = profile.counts         || {};
  const fmt = (x, d=2) => (typeof x === 'number' ? x.toFixed(d) : x);
  let html = `<table style="border-collapse:collapse;width:100%;font:11px 'JetBrains Mono',monospace;color:#222;background:#fff">
    <thead style="background:#f3f4f6;position:sticky;top:0">
      <tr>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">z<br>(µm)</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">z range<br>(µm)</th>`;
  stages.forEach(s => {
    html += `<th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd;background:${stageColor[s]};color:${s==='pulverization'?'#fff':'#000'}">${s}</th>`;
  });
  html += `<th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">total</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">damaged %</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">mean F/P_c</th>
      </tr></thead><tbody>`;
  for (let i = 0; i < centers.length; i++) {
    const ni = (cAll.intact||[])[i]||0, nu = (cAll.microcrack||[])[i]||0,
          nm = (cAll.multicrack||[])[i]||0, nf = (cAll.fragmentation||[])[i]||0,
          np = (cAll.pulverization||[])[i]||0;
    const tot = ni+nu+nm+nf+np;
    const dam = nu+nm+nf+np;
    const dpct = tot ? (100*dam/tot) : 0;
    html += `<tr${i%2 ? ' style="background:#fafafa"':''}>
      <td style="padding:4px 8px;text-align:right">${fmt(centers[i],2)}</td>
      <td style="padding:4px 8px;text-align:right;color:#777">${fmt(edges[i],2)}–${fmt(edges[i+1],2)}</td>
      <td style="padding:4px 8px;text-align:right">${ni}</td>
      <td style="padding:4px 8px;text-align:right">${nu}</td>
      <td style="padding:4px 8px;text-align:right">${nm}</td>
      <td style="padding:4px 8px;text-align:right">${nf}</td>
      <td style="padding:4px 8px;text-align:right">${np}</td>
      <td style="padding:4px 8px;text-align:right;font-weight:600">${tot}</td>
      <td style="padding:4px 8px;text-align:right">${dpct.toFixed(1)}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(meanM[i],3)}</td>
    </tr>`;
  }
  return html + '</tbody></table>';
}

function renderStressTable(profile) {
  const brackets = ['low','mid-low','mid','mid-high','high'];
  const brColors = {
    'low':       '#3b4cc0', 'mid-low':  '#7d97c5', 'mid': '#dddddd',
    'mid-high':  '#d6604d', 'high':     '#b40426',
  };
  const centers = profile.bin_centers_um || [];
  const edges   = profile.bin_edges_um   || [];
  const mean_   = profile.mean_MPa       || [];
  const med_    = profile.median_MPa     || [];
  const p95_    = profile.p95_MPa        || [];
  const max_    = profile.max_MPa        || [];
  const cpT     = profile.counts_per_type   || {};
  const cpB     = profile.counts_by_bracket || {};
  const fmt = (x, d=1) => (typeof x === 'number' ? x.toFixed(d) : x);
  let html = `<table style="border-collapse:collapse;width:100%;font:11px 'JetBrains Mono',monospace;color:#222;background:#fff">
    <thead style="background:#f3f4f6;position:sticky;top:0">
      <tr>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">z<br>(µm)</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">N</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">mean<br>MPa</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">median<br>MPa</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">p95<br>MPa</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">max<br>MPa</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">AM_P</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">AM_S</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">SE</th>`;
  brackets.forEach(b => {
    html += `<th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd;background:${brColors[b]};color:${(b==='mid')?'#000':'#fff'}">${b}</th>`;
  });
  html += `</tr></thead><tbody>`;
  for (let i = 0; i < centers.length; i++) {
    const nP = (cpT.AM_P||[])[i]||0, nS = (cpT.AM_S||[])[i]||0, nE = (cpT.SE||[])[i]||0;
    const tot = nP + nS + nE;
    html += `<tr${i%2 ? ' style="background:#fafafa"':''}>
      <td style="padding:4px 8px;text-align:right">${fmt(centers[i],1)}</td>
      <td style="padding:4px 8px;text-align:right;font-weight:600">${tot}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(mean_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(med_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(p95_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(max_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${nP}</td>
      <td style="padding:4px 8px;text-align:right">${nS}</td>
      <td style="padding:4px 8px;text-align:right">${nE}</td>`;
    brackets.forEach(b => {
      html += `<td style="padding:4px 8px;text-align:right">${(cpB[b]||[])[i]||0}</td>`;
    });
    html += '</tr>';
  }
  return html + '</tbody></table>';
}


/* Coverage table renderer for the Z-profile Data Hub.  Uses
 * ColorBrewer RdYlGn 5-class band colour headers so each bracket
 * column reads as the same bracket the 3D viewer paints. */
function renderCoverageTable(profile) {
  const bands = ['critical','low','mid','high','optimal'];
  const bandColors = {
    critical: '#d7191c', low: '#fdae61', mid: '#ffffbf',
    high:     '#a6d96a', optimal: '#1a9641',
  };
  const types = ['AM_P','AM_S'];
  const typeColors = { 'AM_P': '#444', 'AM_S': '#888' };

  const centers = profile.bin_centers_um || [];
  const edges   = profile.bin_edges_um   || [];
  const mean_   = profile.mean_pct       || [];
  const med_    = profile.median_pct     || [];
  const p5_     = profile.p5_pct         || [];
  const p95_    = profile.p95_pct        || [];
  const cpT     = profile.counts_per_type || {};
  const cpB     = profile.counts_by_band  || {};
  const fmt = (x, d=1) => (typeof x === 'number' ? x.toFixed(d) : x);

  let html = `<table style="border-collapse:collapse;width:100%;font:11px 'JetBrains Mono',monospace;color:#222;background:#fff">
    <thead style="background:#f3f4f6;position:sticky;top:0">
      <tr>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">z<br>(µm)</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">N</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">mean<br>%</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">median<br>%</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">p5<br>%</th>
        <th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd">p95<br>%</th>`;
  types.forEach(t => {
    html += `<th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd;background:${typeColors[t]};color:#fff">${t}</th>`;
  });
  bands.forEach(b => {
    const txtColor = (b === 'mid') ? '#000' : '#fff';
    html += `<th style="padding:6px 8px;text-align:right;border-bottom:1px solid #ddd;background:${bandColors[b]};color:${txtColor}">${b}</th>`;
  });
  html += `</tr></thead><tbody>`;

  for (let i = 0; i < centers.length; i++) {
    const nP = (cpT.AM_P||[])[i]||0, nS = (cpT.AM_S||[])[i]||0;
    const tot = nP + nS;
    html += `<tr${i%2 ? ' style="background:#fafafa"':''}>
      <td style="padding:4px 8px;text-align:right">${fmt(centers[i],1)}</td>
      <td style="padding:4px 8px;text-align:right;font-weight:600">${tot}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(mean_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(med_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(p5_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${fmt(p95_[i])}</td>
      <td style="padding:4px 8px;text-align:right">${nP}</td>
      <td style="padding:4px 8px;text-align:right">${nS}</td>`;
    bands.forEach(b => {
      html += `<td style="padding:4px 8px;text-align:right">${(cpB[b]||[])[i]||0}</td>`;
    });
    html += '</tr>';
  }
  return html + '</tbody></table>';
}

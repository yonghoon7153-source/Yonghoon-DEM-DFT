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
/* ── control-panel HTML ────────────────────────────────────── */
function buildControls(container) {
  const div = document.createElement('div');
  div.className = 'viewer-controls';
  div.innerHTML = `
    <label><input type="checkbox" data-layer="AM_P" checked> AM_P</label>
    <label><input type="checkbox" data-layer="AM_S" checked> AM_S</label>
    <label><input type="checkbox" data-layer="SE" checked> SE</label>
    <label><input type="checkbox" data-layer="MESH" checked> Mesh (plate)</label>
    <hr>
    <label style="font-size:11px;font-weight:600;margin-bottom:1px">View Mode</label>
    <select id="view-mode" style="background:#16192e;color:#e4e6f0;border:1px solid #2a2d3e;border-radius:4px;padding:2px 4px;font-size:11px">
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
    <div id="view-mode-legend" style="font-size:10px;color:#9ca3af;line-height:1.4;margin-top:3px;max-height:340px;overflow-y:auto;overflow-x:hidden;padding-right:2px"></div>
    <hr>
    <label><input type="checkbox" id="path-toggle"> <span style="font-size:11px">Percolating Path</span></label>
    <div id="path-controls" style="display:none">
      <div style="display:flex;gap:4px;align-items:center;margin-top:3px">
        <button id="path-prev" style="background:#555;color:#fff;border:none;border-radius:3px;padding:1px 6px;cursor:pointer;font-size:12px">&lt;</button>
        <span id="path-current" style="font-size:11px;color:#e4e6f0;min-width:30px;text-align:center">-</span>
        <button id="path-next" style="background:#555;color:#fff;border:none;border-radius:3px;padding:1px 6px;cursor:pointer;font-size:12px">&gt;</button>
        <span id="path-total" style="font-size:10px;color:#7c8194">/ -</span>
      </div>
      <div id="cluster-info" style="font-size:10px;color:#e4e6f0;margin-top:3px;line-height:1.5"></div>
    </div>
    <hr>
    <label><input type="checkbox" id="force-chain-toggle"> <span style="font-size:11px">Force Chain</span></label>
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
  font:12px/1.4 'Inter',sans-serif;color:#e4e6f0;z-index:10;user-select:none;width:140px}
.viewer-controls label{display:flex;align-items:center;gap:5px;cursor:pointer;font-size:11px}
.viewer-controls hr{border:none;border-top:1px solid #2a2d3e;margin:3px 0}
.viewer-controls button{background:#555;color:#fff;border:none;border-radius:4px;padding:3px 8px;
  cursor:pointer;font-size:10px;margin-top:1px}
.viewer-controls button:hover{background:#777}
.viewer-info{position:absolute;bottom:50px;left:12px;background:rgba(22,25,46,.9);
  border:1px solid #2a2d3e;border-radius:8px;padding:8px 12px;
  font:11px/1.5 'JetBrains Mono',monospace;color:#e4e6f0;z-index:10;max-width:240px;display:none}
.viewer-zoom{position:absolute;bottom:12px;right:12px;background:rgba(22,25,46,.9);
  border:1px solid #2a2d3e;border-radius:8px;padding:6px 10px;z-index:10;
  display:flex;align-items:center;gap:6px}
.viewer-zoom button{background:#555;color:#fff;border:none;border-radius:4px;width:24px;height:24px;
  cursor:pointer;font-size:16px;line-height:1;display:flex;align-items:center;justify-content:center}
.viewer-zoom button:hover{background:#777}
.viewer-zoom input[type=range]{width:100px;accent-color:#6c8cff}
.path-modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:1000;display:flex;align-items:center;justify-content:center}
.path-modal{background:#fff;border-radius:12px;padding:20px;max-width:90vw;max-height:90vh;position:relative}
.path-modal img{max-width:100%;max-height:75vh;border-radius:8px;border:1px solid #ddd}
.path-modal-info{margin-top:10px;font:12px/1.5 'JetBrains Mono',monospace;color:#333}
.path-modal-actions{display:flex;gap:8px;margin-top:12px;justify-content:flex-end}
.path-modal-actions button{background:#6c8cff;color:#fff;border:none;border-radius:6px;padding:6px 14px;cursor:pointer;font-size:12px}
.path-modal-actions button:hover{background:#8ba3ff}
.path-modal-close{position:absolute;top:8px;right:12px;background:none;border:none;font-size:20px;cursor:pointer;color:#888}
.data-modal-btn{display:flex;align-items:center;justify-content:center;gap:5px;width:100%;padding:7px 8px;margin:8px 0 2px 0;background:rgba(99,102,241,.16);color:#c7d2fe;border:1px solid rgba(99,102,241,.45);border-radius:6px;font:600 11px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;letter-spacing:.2px;cursor:pointer;white-space:nowrap;transition:background .15s,border-color .15s,color .15s,transform .05s}
.data-modal-btn:hover{background:rgba(99,102,241,.32);border-color:#a5b4fc;color:#fff}
.data-modal-btn:active{transform:translateY(1px)}
.data-modal-btn .ico{font-size:13px;line-height:1}
.data-modal-btn .sub{font-weight:500;color:#9ca3af;font-size:9.5px;margin-left:3px}`;
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
  };

  /* controls panel */
  const ctrlDiv = buildControls(container);
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
    + 'background:rgba(0,0,0,.6);color:#e4e6f0;font-size:12px;'
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
        + `<span style="color:#fde68a;font-size:10px">`
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
      + `URL: <code style="font-size:11px">${dataUrl}</code>\n`
      + `Error: ${err && err.message ? err.message : String(err)}\n\n`
      + `<span style="color:#fca5a5;font-size:11px">`
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

  /* compaction-plate STL mesh (optional) */
  if (data.mesh_triangles && data.mesh_triangles.length > 0) {
    state.meshes.MESH = buildPlateMesh(data.mesh_triangles);
    if (state.meshes.MESH) scene.add(state.meshes.MESH);
  }
}

/* ── compaction-plate mesh from STL triangles ──────────────── */
function buildPlateMesh(triangles) {
  if (!triangles || !triangles.length) return null;
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
    color: COL.MESH,
    transparent: true,
    opacity: OPA.MESH,
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

/* Generic blob saver — accepts any Blob (CSV, PNG, etc.).  Picks MIME
 * label based on blob.type to drive the OS Save-As dialog filter. */
async function saveBlobWithDialog(blob, defaultName, btn, resetLabel) {
  const flash = (msg) => {
    if (btn) {
      const orig = resetLabel || btn.textContent;
      btn.textContent = msg;
      setTimeout(() => { btn.textContent = orig; }, 1500);
    }
  };
  const mime = blob.type || 'application/octet-stream';
  const ext = defaultName.split('.').pop().toLowerCase();
  const descMap = {
    csv:  { description: 'CSV file',  accept: { 'text/csv':         ['.csv']  } },
    png:  { description: 'PNG image', accept: { 'image/png':        ['.png']  } },
    json: { description: 'JSON file', accept: { 'application/json': ['.json'] } },
  };
  if (window.showSaveFilePicker) {
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: defaultName,
        types: [descMap[ext] || { description: 'File',
                                    accept: { [mime]: ['.' + ext] } }],
      });
      const writable = await handle.createWritable();
      await writable.write(blob);
      await writable.close();
      flash('✓ Saved');
      return;
    } catch (e) {
      if (e.name === 'AbortError') return;
      console.warn('saveBlobWithDialog fallback:', e);
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = defaultName;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
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
    setLegend(state,
      `<b>Default — natural particle colours</b>
       <span style="color:#222222">●</span> AM_P (polycrystalline, ~6 µm)
       <span style="color:#888888">●</span> AM_S (single-crystal, ~2 µm)
       <span style="color:#f5e6a3">●</span> SE (LPSCl, ~0.5 µm, translucent)
       <span style="color:#9ca3af;font-size:10px">
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
       <span style="color:#9ca3af;font-size:10px">
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
         <span style="color:#9ca3af;font-size:10px">— translucent (전 부피 가로지름)</span>
       <span style="color:#93c5fd">●</span> top-only (${counts.top_only})
         <span style="color:#9ca3af;font-size:10px">— 윗판은 닿지만 바닥 끊김</span>
       <span style="color:#fbbf24">●</span> bottom-only (${counts.bottom_only})
         <span style="color:#9ca3af;font-size:10px">— 바닥은 닿지만 윗판 끊김</span>
       <span style="color:#9ca3af">●</span> dead (${counts.dead})
         <span style="color:#9ca3af;font-size:10px">— 어디에도 안 닿는 고립</span>
       <span style="color:#f87171">●</span> no cluster id (${counts.no_cluster})
         <span style="color:#9ca3af;font-size:10px">— clustering 분석에서 누락 (raw SE)</span>
       <span style="color:#e5e7eb">●</span> AM (faint background)
         <span style="color:#9ca3af;font-size:10px">— 공간감용 ghost, 클러스터 분석 대상 아님</span>`);
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
       <div style="display:flex;justify-content:space-between;font-size:9px;color:#9ca3af">
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
       <span style="color:#9ca3af;font-size:10px">
         particles = max contact pressure (log)<br>
         surface caps = Lawn stage at damaged AM-AM contact
       </span>
       <div style="margin:6px 0 2px 0;height:8px;border-radius:3px;
         background:linear-gradient(90deg,${stops.join(',')})"></div>
       <div style="display:flex;justify-content:space-between;font-size:9px;color:#9ca3af">
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
        const c = covMap[String(p.id)] ?? covMap[p.id];
        if (c !== undefined) vals.push(c);
      });
    });
    if (!vals.length) {
      setLegend(state, '<i>No coverage data — run scripts/coverage_physics_vs_hertzian.py first.</i>');
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
        const c = covMap[String(p.id)] ?? covMap[p.id];
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
       <div style="display:flex;justify-content:space-between;font-size:9px;color:#9ca3af">
         <span>${cLo.toFixed(0)}%</span>
         <span>median ${cMed.toFixed(0)}%</span>
         <span>${cHi.toFixed(0)}%</span>
       </div>
       <span style="color:#9ca3af;font-size:10px;line-height:1.4">
         · 빨강 = low coverage → SE 계면 부족, σ_ionic 손실 risk<br>
         · 초록 = high coverage → 이온 통로 안정<br>
         · mean ≈ ${mean.toFixed(1)} %${nMissing ? ` (no-data AM: ${nMissing})` : ''}
       </span>
       <button id="coverage-z-modal-btn" class="data-modal-btn">
         <span class="ico">📊</span><span>Z-profile 데이터</span>
       </button>`);
    const covBtn = document.getElementById('coverage-z-modal-btn');
    if (covBtn) covBtn.addEventListener('click',
      () => showZProfileDataHub(state, 'coverage'));
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
                  font-size:10.5px;line-height:1.35">
        <span style="color:${color};font-size:12px;line-height:0.9;
                     flex:0 0 10px;text-align:center">${sym}</span>
        <span style="color:#cbd5e1;flex:1 1 auto;min-width:0;
                     white-space:nowrap;overflow:hidden;
                     text-overflow:ellipsis">${label}</span>
        <span style="color:#e5e7eb;font-weight:600;
                     font-family:ui-monospace,Menlo,monospace;
                     flex:0 0 auto;text-align:right;
                     min-width:30px">${fmtCount(count)}</span>
        <span style="color:#9ca3af;font-size:9.5px;
                     font-family:ui-monospace,Menlo,monospace;
                     flex:0 0 auto;text-align:right;
                     min-width:38px">${pctStr}</span>
      </div>`;

    const banner = auxAvailable ? '' : `
      <div style="background:rgba(180,83,9,.18);
                  border:1px solid rgba(245,158,11,.45);
                  color:#fcd34d;font-size:10px;line-height:1.35;
                  padding:5px 7px;border-radius:4px;margin-bottom:5px">
        ⚠ aux 계산 skip된 케이스 (contacts.csv가 너무 큼 또는 cache miss).
        Engagement 분류 데이터 없음 — 모든 SE를 idle로 표시.<br>
        <span style="color:#fde68a;font-size:9.5px">
          → Flask console 로그 / 재실행으로 cache 생성 후 다시 로드.
        </span>
      </div>`;

    setLegend(state,
      `${banner}
       <div style="font-weight:600;color:#cbd5e1;font-size:11px;margin-bottom:2px">
         SE pore-risk map
       </div>
       <div style="color:#9ca3af;font-size:9.5px;line-height:1.35"
            title="engagement_score = (n_plastic + 0.5·n_yield) / n_total. Lower score = SE failed to plastically fill its AM-AM void → micro-pore remains after release.">
         약한 plastic flow → SE가 AM-AM gap 못 채움 → micro-pore<br>
         빨강 = 위험, 녹색 = SE가 gap 잘 채움 (안전)
       </div>
       <div style="display:flex;align-items:center;gap:4px;
                    margin:6px 0 4px;font-size:9.5px;color:#9ca3af">
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
       <div style="color:#9ca3af;font-size:9px;line-height:1.4;
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
         <span style="font-size:9px;color:#9ca3af">${minSeen.toFixed(2)} → ${maxSeen.toFixed(2)}</span>
       </div>
       <table style="font-size:9px;color:#cbd5e1;border-collapse:collapse">
         <tr><td style="padding:0 4px 0 0">F/P_c = 1 threshold</td><td>${nOver}/${nHit} (${overPct}%)</td></tr>
         <tr><td style="padding:0 4px 0 0">median</td><td>${q(0.5).toFixed(2)}</td></tr>
         <tr><td style="padding:0 4px 0 0">95th pct</td><td>${q(0.95).toFixed(2)}</td></tr>
         <tr><td style="padding:0 4px 0 0">max</td><td>${maxSeen.toFixed(2)}</td></tr>
       </table>
       <span style="color:#9ca3af;font-size:9px">★ Brittle Hotspots는 stage로 bin해서 보지만 이 mode는 F/P_c 실값을 연속으로 표시 — 같은 multi-crack stage 안에서도 F/P_c=3.5 와 10.5 의 차이가 그라데이션으로 보임. 흰색 부근이 임계 F/P_c=1 (fracture 시작 경계).</span>`);
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
       <span style="color:#9ca3af;font-size:9px">★ F/P_c ≥ 1 인 AM_P-AM_P 접촉으로 연결된 connected component. 이 backbone에서 fragmentation이 시작되어 cascade 가능.</span>`);
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
              border-radius:3px;padding:1px 4px;font-size:9px;cursor:pointer;
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
              border-radius:3px;padding:1px 4px;font-size:9px;cursor:pointer;
              margin:1px 1px 0 0;white-space:nowrap">${label} ${count}</button>`;
  };
  setLegend(state,
    `<b style="font-size:10px">Stress Chain</b>
     <span style="color:#9ca3af;font-size:9px">(${nDrawn.toLocaleString()} drawn${
       nSkippedPeriodic ? `, ${nSkippedPeriodic} wrap` : ''
     })</span>
     <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0;margin-top:3px">
       <button data-sc-filter="ALL"
         style="background:#0ea5e9;color:#fff;border:1px solid #0284c7;
                border-radius:3px;padding:1px 4px;font-size:9px;cursor:pointer;
                margin:1px 1px 0 0;font-weight:bold;white-space:nowrap">ALL</button>
       ${btn('AM_P-AM_P', '#ef4444', 'P-P', totalCounts['AM_P-AM_P'])}
       ${btn('AM_P-AM_S', '#f97316', 'P-S', totalCounts['AM_P-AM_S'])}
       ${btn('AM_S-AM_S', '#60a5fa', 'S-S', totalCounts['AM_S-AM_S'])}
       ${btn('intact',    '#4b5563', 'int', totalCounts['intact'])}
     </div>
     <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0;margin-top:2px">
       <button data-sc-stage="ALL"
         style="background:#7c3aed;color:#fff;border:1px solid #6d28d9;
                border-radius:3px;padding:1px 4px;font-size:9px;cursor:pointer;
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
              border-radius:3px;padding:1px 4px;font-size:9px;cursor:pointer;
              margin:1px 1px 0 0;white-space:nowrap">${label} ${count}</button>`;
  };
  setLegend(state,
    `<b style="font-size:10px">SE Network Diagnostics</b>
     <div style="display:flex;flex-wrap:wrap;gap:0;margin-top:3px">
       <button data-sed-filter="ALL"
         style="background:#0ea5e9;color:#fff;border:1px solid #0284c7;
                border-radius:3px;padding:1px 4px;font-size:9px;cursor:pointer;
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
     <div style="margin-top:5px;padding-top:4px;border-top:1px solid #2a2d3e;
                  display:flex;flex-wrap:wrap;gap:0">
       <button data-sed-export="csv_particles"
         style="background:#0a4f2e;color:#8cffb2;border:1px solid #0a4f2e;
                border-radius:3px;padding:1px 5px;font-size:9px;cursor:pointer;
                margin:1px 1px 0 0;white-space:nowrap"
         title="모든 SE 입자: id, x, y, z, role">📥 CSV particles</button>
       <button data-sed-export="csv_bn"
         style="background:#5a1d1d;color:#ffb8b8;border:1px solid #5a1d1d;
                border-radius:3px;padding:1px 5px;font-size:9px;cursor:pointer;
                margin:1px 1px 0 0;white-space:nowrap"
         title="Bottleneck contacts: id1, id2, area_um2, area_norm, r_min_um">📥 CSV bn</button>
       <button data-sed-export="csv_clusters"
         style="background:#4a2d6f;color:#d8c2ff;border:1px solid #4a2d6f;
                border-radius:3px;padding:1px 5px;font-size:9px;cursor:pointer;
                margin:1px 1px 0 0;white-space:nowrap"
         title="Dead-end clusters: idx, type, size, ids">📥 CSV clusters</button>
       <button data-sed-export="png_zprofile"
         style="background:#1d3a5f;color:#a8d2ff;border:1px solid #1d3a5f;
                border-radius:3px;padding:1px 5px;font-size:9px;cursor:pointer;
                margin:1px 1px 0 0;white-space:nowrap"
         title="Depth (z) profile of cut / bn / dead-end as PNG">📥 PNG z-profile</button>
       <button data-sed-export="png_stats"
         style="background:#3a3a3a;color:#d8d8d8;border:1px solid #3a3a3a;
                border-radius:3px;padding:1px 5px;font-size:9px;cursor:pointer;
                margin:1px 1px 0 0;white-space:nowrap"
         title="Summary stats card as PNG">📥 PNG stats</button>
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
    /* Export buttons (CSV / PNG) */
    legendEl.querySelectorAll('[data-sed-export]').forEach(b => {
      b.addEventListener('click', () => exportSeDiagnostics(state, b));
    });
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
    const png = renderSeStatsCardPNG(state);
    if (!png) return;
    const byteStr = atob(png.split(',')[1]);
    const ab = new ArrayBuffer(byteStr.length); const ia = new Uint8Array(ab);
    for (let i = 0; i < byteStr.length; i++) ia[i] = byteStr.charCodeAt(i);
    saveBlobWithDialog(new Blob([ab], { type: 'image/png' }),
                        `${caseId}_se_stats.png`, btn, btn.textContent);
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
function renderSeStatsCardPNG(state) {
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

  const W = 700, H = 480;
  const cvs = document.createElement('canvas');
  cvs.width = W; cvs.height = H;
  const ctx = cvs.getContext('2d');
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, W, H);

  const caseId = (state.data && state.data.case_id) || 'case';
  ctx.fillStyle = '#0f172a';
  ctx.font = 'bold 20px serif';
  ctx.fillText(`SE Network Diagnostics  —  ${caseId}`, 30, 40);

  const rows = [
    ['Percolating SE (backbone)',        nPerc,                  '#14b8a6'],
    ['Articulation points (cut nodes)',  artPts.length,          '#facc15'],
    ['  cut fraction = n_cut / n_perc',  (artPts.length / nPerc).toFixed(4), '#facc15'],
    ['Dead-end clusters — top only',     `${deadTop} cluster`,   '#ec4899'],
    ['Dead-end clusters — bottom only',  `${deadBot} cluster`,   '#f97316'],
    ['Bottleneck contacts (capped list)', bnEdges.length,        '#dc2626'],
    ['Below-threshold bn (uncapped)',    nBnBelow ?? '—',        '#dc2626'],
    ['Narrowest A/r²',                   typeof narrowestNorm === 'number'
                                            ? narrowestNorm.toFixed(5) : '—', '#dc2626'],
    ['Narrowest area',                   typeof narrowest === 'number'
                                            ? narrowest.toFixed(5) + ' μm²' : '—', '#dc2626'],
    ['Corpus median A/r²',               typeof medianNorm === 'number'
                                            ? medianNorm.toFixed(4) : '—', '#444'],
    ['Threshold (10% of median)',        typeof thresholdNorm === 'number'
                                            ? thresholdNorm.toFixed(4) : '—', '#444'],
  ];
  ctx.font = '14px serif';
  rows.forEach((r, i) => {
    const y = 90 + i * 30;
    /* color swatch */
    ctx.fillStyle = r[2]; ctx.fillRect(30, y - 12, 12, 14);
    ctx.fillStyle = '#222';
    ctx.fillText(String(r[0]), 52, y);
    ctx.font = 'bold 14px serif';
    ctx.fillStyle = '#0f172a';
    ctx.fillText(String(r[1]), 460, y);
    ctx.font = '14px serif';
  });
  ctx.fillStyle = '#666'; ctx.font = '11px serif';
  ctx.fillText('Generated from 3D viewer SE diagnostic mode.  '
                 + 'cut + bn = percolation risk descriptors.',
                 30, H - 18);
  return cvs.toDataURL('image/png');
}

function setLegend(state, html) {
  const el = document.getElementById('view-mode-legend');
  if (el) el.innerHTML = html;
}

/* ── wire up control panel ─────────────────────────────────── */
function wireControls(ctrlDiv, renderer, camera, controls, scene, state) {
  /* View Mode dropdown */
  const modeSel = ctrlDiv.querySelector('#view-mode');
  if (modeSel) {
    modeSel.addEventListener('change', () => {
      applyViewMode(state, modeSel.value);
    });
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
      } else if (action === 'screenshot') {
        // Hide decoration objects (bbox, grid, axis labels) for clean screenshot
        const hiddenDecorations = [];
        scene.traverse((obj) => {
          if (obj.userData && obj.userData.isDecoration && obj.visible) {
            obj.visible = false;
            hiddenDecorations.push(obj);
          }
        });
        // Use transparent background so PNG overlays cleanly on any PPT slide color
        const prevBg = scene.background;
        const prevClear = new THREE.Color();
        renderer.getClearColor(prevClear);
        const prevAlpha = renderer.getClearAlpha();
        scene.background = null;
        renderer.setClearColor(0x000000, 0);
        // 4× supersampled capture (publication-quality PNG)
        const dataUrl = captureHighRes(renderer, scene, camera, 4);
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
      <div class="path-modal-context" style="display:flex;justify-content:center;align-items:center;gap:12px;margin-top:8px;font-size:12px;color:#444">
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
      <div id="amcu-info" style="text-align:center;margin-top:10px;font-size:12px;color:#444"></div>
      <div style="display:flex;justify-content:center;align-items:center;gap:12px;margin-top:8px;font-size:12px;color:#444;flex-wrap:wrap">
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
      <div id="zh-summary" class="path-modal-info" style="text-align:center;margin-bottom:8px;font-size:11px">
        Loading…
      </div>
      <div style="display:flex;gap:4px;margin-bottom:8px;border-bottom:1px solid #e5e7eb">
        <button class="zh-tab" data-tab="brittle"   style="${tabStyle(false)}">Brittle stages</button>
        <button class="zh-tab" data-tab="stress"    style="${tabStyle(false)}">Stress hotspots</button>
        <button class="zh-tab" data-tab="coverage"  style="${tabStyle(false)}">Coverage (AM)</button>
        <button class="zh-tab" data-tab="combined"  style="${tabStyle(false)}">Combined overlay</button>
      </div>
      <div id="zh-content" style="max-height:58vh;overflow:auto;border:1px solid #e5e7eb;border-radius:6px">
        <div style="padding:30px;text-align:center;color:#888">Loading…</div>
      </div>
      <div class="path-modal-actions" style="justify-content:space-between">
        <span id="zh-context" style="color:#6b7280;font-size:11px;align-self:center">—</span>
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
       <span style="color:#6b7280;font-size:11px">서버 로그(/tmp/flask.log) traceback 확인.</span></div>`;
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
  const tabs = ['brittle', 'stress', 'coverage', 'combined'];
  let active = tabs.includes(defaultTab) ? defaultTab : 'brittle';
  if (active === 'coverage' && !coverage) active = 'brittle';
  const tabEls = overlay.querySelectorAll('.zh-tab');
  const content = document.getElementById('zh-content');
  const ctxEl = document.getElementById('zh-context');
  const pngBtn = document.getElementById('zh-png-btn');
  const csvBtn = document.getElementById('zh-csv-btn');

  function selectTab(name) {
    active = name;
    tabEls.forEach(el => el.setAttribute('style',
      tabStyle(el.dataset.tab === name)));
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
    } else {
      content.innerHTML =
        `<div style="text-align:center;padding:10px">
           <img src="${urlOf('/combined-z-png')}" alt="Combined z-profile"
                style="max-width:100%;height:auto;border-radius:4px">
           <div style="font-size:11px;color:#6b7280;margin-top:6px">
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

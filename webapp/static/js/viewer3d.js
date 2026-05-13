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

/* View-mode colour palettes — Auerbach + Lawn 1998 fracture stages */
const STAGE_COL = {
  intact:        0xcccccc,
  microcrack:    0xfde047,   // yellow
  multicrack:    0xfb923c,   // orange
  fragmentation: 0xef4444,   // red
  pulverization: 0x7f1d1d,   // dark red
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
      <option value="cluster">Cluster Coloring (SE)</option>
      <option value="stress">Stress Concentration</option>
      <option value="coverage">Coverage Heat (AM)</option>
      <option value="se_brittle">Fracture-prone SE</option>
    </select>
    <div id="view-mode-legend" style="font-size:10px;color:#9ca3af;line-height:1.4;margin-top:3px"></div>
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
.path-modal-close{position:absolute;top:8px;right:12px;background:none;border:none;font-size:20px;cursor:pointer;color:#888}`;
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
  fetch(dataUrl).then(r => r.json()).then(data => {
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
    setLegend(state, '');
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
    const csvUrl = (state.dataUrl || '').replace('/3d-data', '/brittle-z-csv');
    setLegend(state,
      `<b>Brittle Stage (Auerbach + Lawn 1998)</b>
       <span style="color:#fde047">●</span> microcrack
       <span style="color:#fb923c">●</span> multicrack
       <span style="color:#ef4444">●</span> fragmentation
       <span style="color:#7f1d1d">●</span> pulverization
       (${(aux.brittle_pairs || []).length} damaged AM-AM pairs)
       <a href="${csvUrl}" download
          style="display:inline-block;margin-top:4px;padding:2px 8px;background:#2563eb;color:#fff;border-radius:4px;font-size:11px;text-decoration:none;font-weight:600">
         Z-profile CSV ↓
       </a>`);
    return;
  }

  if (mode === 'cluster') {
    /* AM dim, SE coloured by cluster status */
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((_, i) => m.setColorAt(i, colDim));
      m.material.opacity = 0.10;
      m.material.transparent = true;
    });
    const cidMap   = aux.cluster_id_per_se || {};
    const meta     = aux.cluster_meta      || {};
    const seMesh   = state.meshes.SE;
    if (seMesh) {
      seMesh.userData.particles.forEach((p, i) => {
        const cid = cidMap[String(p.id)];
        if (cid === undefined) {
          seMesh.setColorAt(i, new THREE.Color(COL.SE_NON_REACH));
          return;
        }
        const md = meta[String(cid)];
        const c  = (md && md.color) ? new THREE.Color(md.color) : colSeBase;
        seMesh.setColorAt(i, c);
      });
      seMesh.material.opacity = 0.92;
      seMesh.material.transparent = true;
    }
    flushColors();
    /* Legend: cluster status counts */
    const counts = { percolating: 0, top_only: 0, bottom_only: 0, dead: 0 };
    Object.values(meta).forEach(md => { if (counts[md.status] !== undefined)
                                          counts[md.status] += md.size || 1; });
    setLegend(state,
      `<b>SE Cluster Status</b>
       <span style="color:#1e40af">●</span> percolating (${counts.percolating})
       <span style="color:#93c5fd">●</span> top-only (${counts.top_only})
       <span style="color:#fbbf24">●</span> bottom-only (${counts.bottom_only})
       <span style="color:#9ca3af">●</span> dead (${counts.dead})`);
    return;
  }

  if (mode === 'stress') {
    /* All particles coloured jet by max contact stress (MPa) */
    const sMap = aux.stress_max || {};
    const all  = Object.values(sMap).filter(v => v > 0);
    if (!all.length) { setLegend(state, '<i>No stress data available.</i>'); return; }
    const sMax = Math.max(...all), sMin = Math.min(...all);
    const span = (sMax - sMin) || 1;
    ['AM_P', 'AM_S', 'SE'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        const s = sMap[String(p.id)] ?? sMap[p.id] ?? 0;
        if (s <= 0) {
          m.setColorAt(i, colDim);
        } else {
          const tnorm = Math.max(0, Math.min(1, (s - sMin) / span));
          m.setColorAt(i, new THREE.Color(jetColor(tnorm)));
        }
      });
      m.material.opacity = 0.85;
      m.material.transparent = true;
    });
    flushColors();
    setLegend(state,
      `<b>Max Contact Pressure (MPa)</b>
       <span style="color:#0000ff">■</span> ${sMin.toFixed(0)}
       <span style="color:#00ff00">■</span> ${((sMax+sMin)/2).toFixed(0)}
       <span style="color:#ff0000">■</span> ${sMax.toFixed(0)}`);
    return;
  }

  if (mode === 'coverage') {
    /* AM coloured red→green by coverage %, SE dim */
    const covMap = aux.coverage_per_am || {};
    const seMesh = state.meshes.SE;
    if (seMesh) {
      seMesh.userData.particles.forEach((_, i) => seMesh.setColorAt(i, colDim));
      seMesh.material.opacity = 0.10;
      seMesh.material.transparent = true;
    }
    ['AM_P', 'AM_S'].forEach(t => {
      const m = state.meshes[t]; if (!m) return;
      m.userData.particles.forEach((p, i) => {
        const c = covMap[String(p.id)] ?? covMap[p.id];
        if (c === undefined) {
          m.setColorAt(i, colDim);
          return;
        }
        const tnorm = Math.max(0, Math.min(1, c / 100));
        m.setColorAt(i, new THREE.Color(rygColor(tnorm)));
      });
      m.material.opacity = 0.92;
      m.material.transparent = true;
    });
    flushColors();
    setLegend(state,
      `<b>AM Coverage (% SE / surface)</b>
       <span style="color:#ff0000">■</span> 0%
       <span style="color:#ffff00">■</span> 50%
       <span style="color:#00ff00">■</span> 100%`);
    return;
  }

  if (mode === 'se_brittle') {
    /* Highlight SE-SE pairs with high δ/R (sub-Auerbach but yielding) */
    dimAll();
    const stressIds = new Set();
    const plasticIds = new Set();
    (aux.se_stress_pairs || []).forEach(b => {
      [b.id1, b.id2].forEach(id => {
        stressIds.add(id);
        if (b.plastic) plasticIds.add(id);
      });
    });
    const seMesh = state.meshes.SE;
    if (seMesh) {
      seMesh.userData.particles.forEach((p, i) => {
        if (plasticIds.has(p.id)) {
          seMesh.setColorAt(i, new THREE.Color(0xef4444));   // red — Tabor plastic
        } else if (stressIds.has(p.id)) {
          seMesh.setColorAt(i, new THREE.Color(0xfde047));   // yellow — yield onset
        }
      });
      seMesh.material.opacity = 0.95;
      seMesh.material.transparent = true;
    }
    flushColors();
    setLegend(state,
      `<b>SE-SE Stress (Tabor regime)</b>
       <span style="color:#fde047">●</span> δ/R > 0.0011 (yield)
       <span style="color:#ef4444">●</span> δ/R > 0.0078 (fully plastic)
       (${(aux.se_stress_pairs || []).length} stressed SE-SE pairs)`);
    return;
  }
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

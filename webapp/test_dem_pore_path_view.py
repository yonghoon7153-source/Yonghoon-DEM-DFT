#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 3D 뷰어 — 기공 (빈 공간 · 격자 추정) 보기 + "Path Only View" 가 화면의 경로를 연다 (2026-10-07).

1저자 요청 (*"3D webapp 업데이트 해야되는 부분 있음 추가해봐"*) — 다음 날 아침 보고 슬라이드용 3D 그림 두 가지.

  python3 webapp/test_dem_pore_path_view.py      # 종료코드 0 = PASS

[P] Path Only View — 옛 판은 `showPathOnlyView` 가 `state.currentClusterIdx` 를 읽는데 **아무도 그 값을 쓰지 않아** 늘 0 번
    클러스터를 열었다 (화면에서 2 번 클러스터의 경로를 골라도 팝업은 0 번 클러스터 · 같은 번호의 다른 경로).
    → `highlightCluster` 가 고른 클러스터 번호를 기록한다.  시험 = 그 두 함수를 viewer3d.js 에서 **그대로** 잘라 node 에서 돌리고,
      팝업 정보 줄 (Cluster # · τ) 과 팝업이 그린 관 (tube) 의 끝점이 화면에서 고른 경로와 같은지 본다.
      대조 (0 번 클러스터를 고른 경우) 는 옛 판도 통과한다 = 껍데기가 아무것도 못 보는 것이 아니다.
[D] DEM 기공 보기 (View Mode "기공 (빈 공간 · 격자 추정)" · value `dem_pore`) — 칸 중심이 어느 구에도 안 들면 빈 칸.
    순수 함수 `computeVoidVoxels` 를 잘라 node 에서 돌린다:
      빈 상자 = 1 · 구 하나 = 1 − V_구/V_상자 (격자 오차 한도가 칸이 작아질수록 줄어든다) · 꽉 찬 단순 입방 격자 = 0 (x·y 주기 —
      주기를 끄면 0 이 아니다 = 판별력 대조) · 판 · 바닥에서 잘림 · 주기 상 (면 · 모서리) · 무작위 침대에서 모든 칸이 전수 대조와 같다 ·
      real_14 실침대 (33,289 입자) = 웹앱 정확 union 과 **같은 계산** (`scripts/lhs_union_webapp.coverage` · 무작위 점 · KD 트리)
      과 맞고 (주기를 끄면 안 맞는다) 브라우저급 시간 안에 끝난다.
    판 z (메시 · 없으면 입자 윗면 = 판 아님 표지) · 격자 크기 선택 · 범례 문구 ("격자 추정 · 표시용 — 보고 porosity 는 표의 값" ·
    격자 빈 칸 비율 · 격자 크기) · 그리기 (InstancedMesh 칸 수 = 빈 칸 수 · three 축 순서 · 단면 뷰 다시 적용 · 입자 흐리게 ·
    되돌리기 · PNG 에서 빠지는 장식이 아님) 도 같은 방식으로 돌린다.
    ★ 단면 뷰 (Y-슬라이스) — 반투명 칸이 시선마다 ~20 겹 쌓여 단면도 통째로 덮였다 (headless 미리보기에서 확인) → 단면이 켜지면
      그 자리 칸 n 층만 불투명 (기공 단면 · XCT 슬라이스처럼) · 입자는 단면에서 불투명 (3 상 단면) · 끄면 모든 칸 반투명 0.08.
      단면 위치 막대를 따라가고, 단면이 꺼진 채 막대 · 불투명도를 움직여도 수십만 칸을 다시 짓지 않는다 (D17–D17h).
⚠ node 가 없으면 건너뛰지 않고 FAIL 한다 (돌지 않는 검사는 없는 것과 같다 — 규칙 K).
"""
import gzip
import json
import math
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
REAL14 = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')

sys.path.insert(0, HERE)
from test_closed_param_labels import js_fn, js_const, run_node   # noqa: E402  (렌더된 JS 를 잘라 node 로 — 같은 도구)

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


def fns(src, names):
    """함수 소스 묶음 · 못 찾은 이름 목록 (옛 판에는 없는 함수가 있다 — 예외 대신 FAIL 로 적는다)."""
    out, miss = [], []
    for n in names:
        try:
            out.append(js_fn(src, n))
        except (ValueError, AssertionError):
            miss.append(n)
    return '\n'.join(out), miss


def consts(src, names):
    out, miss = [], []
    for n in names:
        try:
            out.append(js_const(src, n))
        except (ValueError, AssertionError):
            miss.append(n)
    return '\n'.join(out), miss


# ══════════════════════════════════════════════════════════════════════════════
#  [P] Path Only View — 화면에서 고른 경로를 연다
# ══════════════════════════════════════════════════════════════════════════════
P_SHIM = r"""
'use strict';
const LOG = { alerts: [], overlay: null, scenes: [] };
class V3 { constructor(x = 0, y = 0, z = 0) { this.x = x; this.y = y; this.z = z; }
  set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }
  copy(v) { this.x = v.x; this.y = v.y; this.z = v.z; return this; }
  clone() { return new V3(this.x, this.y, this.z); }
  sub(v) { this.x -= v.x; this.y -= v.y; this.z -= v.z; return this; }
  normalize() { const l = Math.hypot(this.x, this.y, this.z) || 1; this.x /= l; this.y /= l; this.z /= l; return this; }
  addScaledVector(v, s) { this.x += v.x * s; this.y += v.y * s; this.z += v.z * s; return this; }
  distanceTo(v) { return Math.hypot(this.x - v.x, this.y - v.y, this.z - v.z); } }
class Obj3 { constructor() { this.position = new V3(); this.userData = {}; this.children = []; this.visible = true; }
  add(c) { this.children.push(c); return this; } remove(c) { this.children = this.children.filter(x => x !== c); }
  traverse(f) { f(this); this.children.forEach(c => (c.traverse ? c.traverse(f) : f(c))); } }
class Mesh3 extends Obj3 { constructor(g, m) { super(); this.geometry = g; this.material = m; } }
const THREE = {
  Vector3: V3, Vector2: class { constructor() { this.x = 0; this.y = 0; } },
  Color: class { constructor(v) { this.v = v; } setHex(h) { this.v = h; return this; } },
  Object3D: Obj3, Group: class extends Obj3 {},
  Scene: class extends Obj3 { constructor() { super(); LOG.scenes.push(this); } },
  Mesh: Mesh3, LineSegments: Mesh3, GridHelper: class extends Obj3 {}, AmbientLight: class extends Obj3 {},
  DirectionalLight: class extends Obj3 {}, PerspectiveCamera: class extends Obj3 {},
  SphereGeometry: class {}, BoxGeometry: class {}, EdgesGeometry: class {},
  MeshPhongMaterial: class { constructor(o) { Object.assign(this, o || {}); } },
  LineBasicMaterial: class { constructor(o) { Object.assign(this, o || {}); } },
  LineCurve3: class { constructor(a, b) { this.v1 = a; this.v2 = b; } },
  TubeGeometry: class { constructor(c) { this.curve = c; } },
  WebGLRenderer: class { constructor() { this.domElement = mkEl('canvas'); }
    setPixelRatio() {} setSize() {} setClearColor() {} getClearColor(c) { return c; } getClearAlpha() { return 1; }
    render() {} dispose() {} },
  DoubleSide: 2, FrontSide: 0,
};
class OrbitControls { constructor() { this.target = new V3(); } update() {} addEventListener() {} }
function mkEl(tag) {
  return { tag, style: {}, value: '10', checked: true, textContent: '', innerHTML: '', className: '', children: [],
    clientWidth: 700, clientHeight: 500, onclick: null,
    appendChild(c) { this.children.push(c); return c; }, addEventListener() {}, remove() { this.removed = true; },
    querySelector() { return mkEl('q'); } };
}
const ELS = {};
const document = { body: { appendChild(o) { LOG.overlay = o; } }, createElement: mkEl,
                   getElementById(id) { return ELS[id] || (ELS[id] = mkEl(id)); } };
const window = { devicePixelRatio: 1 };
function requestAnimationFrame() { return 1; }
function cancelAnimationFrame() {}
function alert(m) { LOG.alerts.push(String(m)); }
function addAxisLabels() {}
function createInstancedSpheres(ps) { const m = new Obj3(); m.material = { opacity: 0.1 }; m.userData.particles = ps; return m; }
function tubesOf(root) {
  const out = [];
  root.traverse(o => { if (o.geometry && o.geometry.curve) { const c = o.geometry.curve;
    out.push([[c.v1.x, c.v1.y, c.v1.z], [c.v2.x, c.v2.y, c.v2.z]]); } });
  return out;
}
"""

P_RUN = r"""
const P = [], idIndex = {};
function se(id, x, y, z) { const p = { id, type: 'SE', x, y, z, r: 0.5 }; P.push(p); idIndex[id] = p; return p; }
//  세 클러스터 — 0 번 · 2 번은 관통 (경로 둘) · 1 번은 비관통.  좌표 = µm (x, y, z) · 주기 점프 없음
se(1, 5, 5, 0.5); se(2, 5.5, 5, 4); se(3, 6, 5, 9.5); se(4, 4, 5, 3); se(5, 4.5, 6, 6);
se(6, 1, 1, 5); se(7, 1.5, 1, 5.5);
se(8, 15, 15, 0.5); se(9, 15, 15.5, 5); se(10, 15, 16, 9.5); se(11, 16, 15, 3); se(12, 16.5, 16, 7);
const mkPath = (ids, tau, cat) => ({ ids, tortuosity: tau, path_length: +(9 * tau).toFixed(1), z_distance: 9, category: cat });
const clusters = [
  { ids: [1, 2, 3, 4, 5], size: 5, percolating: true, paths: [mkPath([1, 2, 3], 1.11, 'best'), mkPath([1, 4, 5, 3], 1.22, 'mean')] },
  { ids: [6, 7], size: 2, percolating: false, path: null },
  { ids: [8, 9, 10, 11, 12], size: 5, percolating: true, paths: [mkPath([8, 9, 10], 1.55, 'best'), mkPath([8, 11, 12, 10], 1.77, 'worst')] },
];
clusters.forEach(c => { if (c.paths) c.path = c.paths[0]; });
const box = { x_min: 0, x_max: 20, y_min: 0, y_max: 20, z_min: 0, z_max: 10 };
function seMesh() { return { setColorAt() {}, instanceColor: { needsUpdate: false }, material: { opacity: 0.85 }, userData: {} }; }
function mkState() { return { data: { box, clusters: { clusters } }, idIndex, seParticles: P, meshes: { SE: seMesh() }, pathGroup: null }; }
function run(ci, pi) {
  LOG.alerts = []; LOG.overlay = null;
  const scene = new THREE.Scene(), state = mkState();
  let err = null, mainTubes = [], modalTubes = [];
  try {
    highlightCluster(ci, scene, state, mkEl('info'), pi);
    mainTubes = state.pathGroup ? tubesOf(state.pathGroup) : [];
    const n0 = LOG.scenes.length;
    showPathOnlyView({}, scene, {}, state);
    if (LOG.scenes.length > n0) modalTubes = tubesOf(LOG.scenes[LOG.scenes.length - 1]);
  } catch (e) { err = String(e && e.stack || e); }
  return { err, info: LOG.overlay ? LOG.overlay.innerHTML : null, alerts: LOG.alerts.slice(), mainTubes, modalTubes };
}
const OUT = { c2p1: run(2, 1), c2p0: run(2, 0), c0p1: run(0, 1), c0p0: run(0, 0) };
//  경로를 끈 뒤 (clearPath = pathGroup null) · 범위 밖 클러스터 → 팝업은 거절해야 한다 (옛 선택을 열지 않는다)
{ LOG.alerts = []; LOG.overlay = null; const scene = new THREE.Scene(), state = mkState();
  highlightCluster(2, scene, state, mkEl('i'), 1); state.pathGroup = null;
  showPathOnlyView({}, scene, {}, state); OUT.off = { alerts: LOG.alerts.slice(), opened: !!LOG.overlay }; }
{ LOG.alerts = []; LOG.overlay = null; const scene = new THREE.Scene(), state = mkState();
  highlightCluster(2, scene, state, mkEl('i'), 1); const g = state.pathGroup;
  highlightCluster(9, scene, state, mkEl('i'), 0); state.pathGroup = g;          // 범위 밖 선택 뒤 남은 그룹이 있어도
  showPathOnlyView({}, scene, {}, state);
  OUT.bad = { alerts: LOG.alerts.slice(), opened: !!LOG.overlay, cur: state.currentClusterIdx === undefined ? '(undefined)' : state.currentClusterIdx }; }
console.log(JSON.stringify(OUT));
"""


def p_expected_tubes(ids, coords):
    pts = [coords[i] for i in ids]
    return [[[a[0], a[2], a[1]], [b[0], b[2], b[1]]] for a, b in zip(pts, pts[1:])]     # µm (x, y, z) → three (x, z, y)


def section_path(js):
    print('[P] Path Only View — 화면에서 고른 경로를 연다')
    if not shutil.which('node'):
        chk('P0 node 필요 (경로 함수를 실제로 돌린다)', False, 'node 미설치')
        return
    src, miss = fns(js, ('highlightCluster', 'resetSEColors', 'showPathOnlyView'))
    cs, miss_c = consts(js, ('COL', 'OPA'))
    if not chk('P0 viewer3d.js 에서 highlightCluster · resetSEColors · showPathOnlyView · COL · OPA 를 잘라 냈다',
               not miss and not miss_c, f'없음 {miss + miss_c}'):
        return
    res = run_node(P_SHIM + cs + '\n' + src + '\n' + P_RUN)
    if not chk('P0b node 실행', res is not None):
        return
    coords = {1: (5, 5, 0.5), 2: (5.5, 5, 4), 3: (6, 5, 9.5), 4: (4, 5, 3), 5: (4.5, 6, 6),
              8: (15, 15, 0.5), 9: (15, 15.5, 5), 10: (15, 16, 9.5), 11: (16, 15, 3), 12: (16.5, 16, 7)}
    want = {'c2p1': (2, 1.77, [8, 11, 12, 10]), 'c2p0': (2, 1.55, [8, 9, 10]),
            'c0p1': (0, 1.22, [1, 4, 5, 3]), 'c0p0': (0, 1.11, [1, 2, 3])}
    labels = {'c2p1': 'P1 화면에서 2 번 클러스터의 2 번째 경로', 'c2p0': 'P2 화면에서 2 번 클러스터의 1 번째 경로',
              'c0p1': 'P3 (대조 · 옛 판도 통과) 0 번 클러스터의 2 번째 경로', 'c0p0': 'P4 (대조) 0 번 클러스터의 1 번째 경로'}
    for k, (ci, tau, ids) in want.items():
        d = res[k]
        info = d['info'] or ''
        mi = re.search(r'class="path-modal-info"[^>]*>(.*?)</div>', info, re.S)
        info1 = re.sub(r'\s+', ' ', mi.group(1) if mi else info)[:200]
        tubes = p_expected_tubes(ids, coords)
        chk(f"{labels[k]} → 팝업 정보 줄 = Cluster #{ci} · τ = {tau}",
            d['err'] is None and not d['alerts'] and f'Cluster #{ci} |' in info and f'τ = {tau} |' in info,
            f"err {d['err']} · alerts {d['alerts']} · info {info1!r}")
        chk(f"{labels[k]} → 팝업이 그린 관 = 그 경로의 SE 중심 ({len(ids)} 개 · 화면의 금색 관과 같다)",
            d['modalTubes'] == tubes and d['mainTubes'] == tubes, f"modal {d['modalTubes']} · main {d['mainTubes']}")
    note = res['c2p1']['info'] or ''
    chk('P5 팝업에 τ 의 정의 한 줄 — 이 경로의 기하 τ (SE 중심 잇는 길이 ÷ 양 끝 z 거리) · 수송 tortuosity 아님 · '
        'tortuosity_SE_wall 과 다른 정의 (보고 그림 캡션 오기 방지 · τ 명명 규약)',
        '수송 tortuosity 아님' in note and 'tortuosity_SE_wall' in note and '양 끝 z 거리' in note, re.sub(r'\s+', ' ', note)[-260:])
    chk('P6 경로를 끈 뒤 (pathGroup 없음) 팝업은 열리지 않고 안내만 한다',
        res['off']['alerts'] and not res['off']['opened'], repr(res['off']))
    chk('P7 범위 밖 클러스터를 고르면 선택이 지워진다 — 남은 그룹이 있어도 옛 선택 (2 번) 을 열지 않는다',
        res['bad']['cur'] is None and res['bad']['alerts'] and not res['bad']['opened'], repr(res['bad']))


# ══════════════════════════════════════════════════════════════════════════════
#  [D] DEM 기공 보기 — 순수 함수 · 범례 · 그리기
# ══════════════════════════════════════════════════════════════════════════════
D_RUN = r"""
const OUT = {};
const box = { x_min: 0, x_max: 10, y_min: 0, y_max: 10, z_min: 0, z_max: 10 };
const vf = (ps, nx, o) => computeVoidVoxels(ps, box, 10, nx, o).voidFraction;
{ const r = computeVoidVoxels([], box, 10, 20);
  OUT.empty = { vf: r.voidFraction, nVoid: r.nVoid, nTotal: r.nTotal, nC: r.centres.length, dims: [r.nx, r.ny, r.nz], h: [r.hx, r.hy, r.hz] }; }
OUT.single = [10, 20, 40, 80].map(nx => ({ nx, vf: vf([{ x: 5, y: 5, z: 5, r: 3 }], nx) }));
{ const a = 2, lat = [];
  for (let x = 0; x < 10; x += a) for (let y = 0; y < 10; y += a) for (let z = 0; z <= 10; z += a) lat.push({ x, y, z, r: 0.9 * a });
  OUT.packed = { per: vf(lat, 40), nonper: vf(lat, 40, { periodicXY: false }), n: lat.length }; }
OUT.clip = { half: vf([{ x: 5, y: 5, z: 10, r: 3 }], 80), above: vf([{ x: 5, y: 5, z: 13.5, r: 3 }], 40),
             below: vf([{ x: 5, y: 5, z: -3.5, r: 3 }], 40), floorHalf: vf([{ x: 5, y: 5, z: 0, r: 3 }], 80) };
OUT.wrap = { centre: vf([{ x: 5, y: 5, z: 5, r: 3 }], 80), face: vf([{ x: 0, y: 5, z: 5, r: 3 }], 80),
             corner: vf([{ x: 0, y: 0, z: 5, r: 3 }], 80), faceNP: vf([{ x: 0, y: 5, z: 5, r: 3 }], 80, { periodicXY: false }),
             atL: vf([{ x: 10, y: 5, z: 5, r: 3 }], 80), neg: vf([{ x: -0.000001, y: 5, z: 5, r: 3 }], 80) };
OUT.zeroR = vf([{ x: 5, y: 5, z: 5, r: 0 }, { x: NaN, y: 5, z: 5, r: 2 }], 20);
//  무작위 침대 — 모든 칸을 전수 (최소 영상 거리 · 모든 구) 로 다시 판정해 같은지 본다
{ let s = 12345; const rnd = () => (s = (s * 1103515245 + 12345) % 2147483648) / 2147483648;
  const ps = []; for (let i = 0; i < 40; i++) ps.push({ x: rnd() * 10, y: rnd() * 10, z: -1 + rnd() * 12, r: 0.4 + 2.2 * rnd() });
  const nx = 24, r = computeVoidVoxels(ps, box, 10, nx);
  const isVoid = new Set();
  for (let q = 0; q < r.nVoid; q++) isVoid.add(Math.round((r.centres[3 * q] - r.x0) / r.hx - 0.5) + ',' + Math.round((r.centres[3 * q + 1] - r.y0) / r.hy - 0.5)
                                               + ',' + Math.round((r.centres[3 * q + 2] - r.z0) / r.hz - 0.5));
  let bad = 0, nVoidBF = 0, outside = 0;
  for (let q = 0; q < r.nVoid; q++) { const x = r.centres[3 * q], y = r.centres[3 * q + 1], z = r.centres[3 * q + 2];
    if (x < 0 || x > 10 || y < 0 || y > 10 || z < 0 || z > 10) outside++; }
  for (let k = 0; k < r.nz; k++) for (let j = 0; j < r.ny; j++) for (let i = 0; i < r.nx; i++) {
    const x = r.x0 + (i + 0.5) * r.hx, y = r.y0 + (j + 0.5) * r.hy, z = r.z0 + (k + 0.5) * r.hz;
    let solid = false;
    for (const p of ps) { let dx = x - p.x, dy = y - p.y; dx -= 10 * Math.round(dx / 10); dy -= 10 * Math.round(dy / 10);
      const dz = z - p.z; if (dx * dx + dy * dy + dz * dz < p.r * p.r) { solid = true; break; } }
    if (!solid) nVoidBF++;
    if (solid === isVoid.has(i + ',' + j + ',' + k)) bad++;
  }
  OUT.brute = { bad, nVoid: r.nVoid, nVoidBF, nTotal: r.nTotal, outside, dims: [r.nx, r.ny, r.nz] }; }
//  큰 구 (2r + h ≥ L — 최소 영상 가지) · 원점이 0 이 아닌 상자 (x −5…5 · y 2…12) — 같은 전수 대조
{ let s = 777; const rnd = () => (s = (s * 1103515245 + 12345) % 2147483648) / 2147483648;
  const bx = { x_min: -5, x_max: 5, y_min: 2, y_max: 12 };
  const ps = []; for (let i = 0; i < 6; i++) ps.push({ x: -5 + rnd() * 10, y: 2 + rnd() * 10, z: rnd() * 10, r: i < 3 ? 4.6 + 2.4 * rnd() : 0.5 + rnd() });
  const r = computeVoidVoxels(ps, bx, 10, 20);
  const isVoid = new Set();
  for (let q = 0; q < r.nVoid; q++) isVoid.add(Math.round((r.centres[3 * q] - r.x0) / r.hx - 0.5) + ',' + Math.round((r.centres[3 * q + 1] - r.y0) / r.hy - 0.5)
                                               + ',' + Math.round((r.centres[3 * q + 2] - r.z0) / r.hz - 0.5));
  let bad = 0, nBig = ps.filter(p => 2 * p.r + r.hx >= 10).length;
  for (let k = 0; k < r.nz; k++) for (let j = 0; j < r.ny; j++) for (let i = 0; i < r.nx; i++) {
    const x = r.x0 + (i + 0.5) * r.hx, y = r.y0 + (j + 0.5) * r.hy, z = r.z0 + (k + 0.5) * r.hz;
    let solid = false;
    for (const p of ps) { let dx = x - p.x, dy = y - p.y; dx -= 10 * Math.round(dx / 10); dy -= 10 * Math.round(dy / 10);
      const dz = z - p.z; if (dx * dx + dy * dy + dz * dz < p.r * p.r) { solid = true; break; } }
    if (solid === isVoid.has(i + ',' + j + ',' + k)) bad++;
  }
  OUT.bruteBig = { bad, nBig, nVoid: r.nVoid, nTotal: r.nTotal, x0: r.x0, y0: r.y0 }; }
//  격자 크기 선택 (칸 수 목표) · 판 z
OUT.presets = Object.keys(DEM_PORE_PRESETS).map(k => { const nx = demPoreGridNx({ x_min: 0, x_max: 50, y_min: 0, y_max: 50 }, 30.2845, k);
  const h = 50 / nx; return [k, nx, Math.round(50 / h) * Math.round(50 / h) * Math.round(30.2845 / h), DEM_PORE_PRESETS[k].target]; });
OUT.top = { mesh: demPoreDomainTop(DTOP.mesh), none: demPoreDomainTop(DTOP.none), empty: demPoreDomainTop(DTOP.empty),
            low: demPoreDomainTop(DTOP.low) };
//  범례 문구
{ const res = { nx: 100, ny: 100, nz: 61, hx: 0.5, hy: 0.5, hz: 30.2845 / 61, nTotal: 610000, nVoid: 104432, voidFraction: 104432 / 610000, periodicXY: true };
  OUT.leg = { mesh: demPoreLegendHTML(res, { zTop: 30.2845, source: 'mesh' }, { preset: 'normal', ms: 87 }),
              top: demPoreLegendHTML(res, { zTop: 31.336, source: 'particle_top' }, { preset: 'normal', ms: 87 }) };
  OUT.status = { full: demPoreStatusHTML(res, { section: false, shown: 104432, stride: 1, opacity: 0.08 }),
                 cap: demPoreStatusHTML(res, { section: false, shown: 52216, stride: 2, opacity: 0.08 }),
                 sec: demPoreStatusHTML(res, { section: true, cut: 25, layers: 1, shown: 1234, stride: 1 }) }; }
console.log(JSON.stringify(OUT));
"""

# 그리기 — 아주 작은 THREE 껍데기로 renderDemPore · _teardownDemPore 를 그대로 돌린다
R_SHIM = r"""
'use strict';
const LEG = [];
function setLegend(state, html) { LEG.push(html); }
const THREE = {
  Color: class { constructor(v) { this.v = v; } setHex(h) { this.v = h; return this; } },
  BoxGeometry: class { constructor(a, b, c) { this.dims = [a, b, c]; } dispose() { this.disposed = true; } },
  MeshLambertMaterial: class { constructor(o) { Object.assign(this, o || {}); this.userData = {}; } dispose() { this.disposed = true; } },
  MeshPhongMaterial: class { constructor(o) { Object.assign(this, o || {}); this.userData = {}; } dispose() { this.disposed = true; } },
  InstancedMesh: class { constructor(g, m, n) { this.geometry = g; this.material = m; this.count = n; this.isInstancedMesh = true;
    this.instanceMatrix = { array: new Float32Array(16 * n), needsUpdate: false }; this.userData = {}; this.visible = true; }
    dispose() { this.disposed = true; } },
  FrontSide: 0, DoubleSide: 2,
};
THREE.MeshBasicMaterial = THREE.MeshLambertMaterial;
const ELS = {};
//  요소 껍데기 — 붙은 듣개 (listener) 를 적어 두고 시험이 직접 불러 사건을 흉내 낸다
const document = { getElementById(id) { return ELS[id] || (ELS[id] = { id, value: '', checked: true, textContent: '', innerHTML: '', style: {}, ls: [],
                     addEventListener(type, fn) { this.ls.push([type, fn]); } }); },
                   querySelector() { return null; } };
function fire(id, type) { (ELS[id] ? ELS[id].ls : []).filter(l => l[0] === type).forEach(l => l[1]({ type })); }
function nListen(id, type) { return (ELS[id] ? ELS[id].ls : []).filter(l => l[0] === type).length; }
"""

R_RUN = r"""
function pm(name, ps, opa, tr) {
  return { name, visible: true, userData: { particles: ps, baseColor: 0x123456 }, setColorAt() {}, instanceColor: { needsUpdate: false },
           material: { opacity: opa, transparent: tr, depthWrite: !tr, userData: {}, needsUpdate: false } };
}
const ps = [{ id: 1, type: 'AM_P', x: 5, y: 5, z: 5, r: 3 }, { id: 2, type: 'SE', x: 1, y: 8, z: 2, r: 1 }];
const scene = { children: [], add(o) { this.children.push(o); }, remove(o) { this.children = this.children.filter(c => c !== o); } };
let clipCalls = 0;
const plate = [[[0, 0, 8], [10, 10, 8], [10, 0, 8]], [[0, 0, 8], [0, 10, 8], [10, 10, 8]]];
const state = { scene, data: { particles: ps, box: { x_min: 0, x_max: 10, y_min: 0, y_max: 12, z_min: 0, z_max: 8 }, mesh_triangles: plate },
                meshes: { AM_P: pm('AM_P', [ps[0]], 1, false), AM_S: null, SE: pm('SE', [ps[1]], 0.85, true),
                          MESH: { visible: true, material: { opacity: 0.55 } } },
                applyClip() { clipCalls++; } };
const OUT = { err: null };
try {
  renderDemPore(state);
  const vm = scene.children.filter(o => o.isInstancedMesh);
  const m = vm[0] || null;
  const res = computeVoidVoxels(ps, state.data.box, 8, demPoreGridNx(state.data.box, 8, 'normal'));
  let tx = [Infinity, -Infinity], ty = [Infinity, -Infinity], tz = [Infinity, -Infinity], firstEq = null;
  if (m) { const a = m.instanceMatrix.array;
    for (let q = 0; q < m.count; q++) { const o = 16 * q;
      tx = [Math.min(tx[0], a[o + 12]), Math.max(tx[1], a[o + 12])]; ty = [Math.min(ty[0], a[o + 13]), Math.max(ty[1], a[o + 13])];
      tz = [Math.min(tz[0], a[o + 14]), Math.max(tz[1], a[o + 14])]; }
    firstEq = [a[12], a[13], a[14], a[0], a[5], a[10], a[15]].map(v => +v.toFixed(5)).join(',') ===
              [res.centres[0], res.centres[2], res.centres[1], 1, 1, 1, 1].map(v => +v.toFixed(5)).join(','); }
  OUT.render = { nMesh: vm.length, count: m ? m.count : null, nVoid: res.nVoid, dims: m ? m.geometry.dims : null, h: [res.hx, res.hz, res.hy],
                 tx, ty, tz, firstEq, needsUpdate: m ? m.instanceMatrix.needsUpdate : null, deco: m ? !!m.userData.isDecoration : null,
                 frustumCulled: m ? m.frustumCulled : null, clipCalls, legend: LEG[LEG.length - 1] || '',
                 matOpa: m ? m.material.opacity : null, matDepthWrite: m ? m.material.depthWrite : null,
                 am: Object.assign({}, state.meshes.AM_P.material, { userData: undefined }), se: Object.assign({}, state.meshes.SE.material, { userData: undefined }),
                 plate: state.meshes.MESH.visible, groupIsMesh: state.demPoreGroup === m };
  //  같은 격자를 다시 그리면 다시 계산하지 않는다 (캐시) · 그룹은 하나
  renderDemPore(state);
  OUT.again = { nMesh: scene.children.filter(o => o.isInstancedMesh).length, oldDisposed: !!(m && m.geometry.disposed) };
  //  단면 뷰 — Y-슬라이스 판 (scene 법선 −Z · constant = data y) 이 있으면 그 자리 칸 n 층만 불투명 (기공 단면)
  state.viewMode = 'dem_pore';
  const meshNow = () => scene.children.filter(o => o.isInstancedMesh);
  const tzRange = (mm) => { let lo = Infinity, hi = -Infinity; const a = mm.instanceMatrix.array;
    for (let q = 0; q < mm.count; q++) { lo = Math.min(lo, a[16 * q + 14]); hi = Math.max(hi, a[16 * q + 14]); } return [lo, hi]; };
  //  기대값 (구현과 다른 식으로): 판 바로 아래 점 (cut − 10⁻⁷h) 을 품은 층과 그 아래 L − 1 층 · 층 번호 = floor((y − y0)/h)
  const layerOf = y => Math.floor((y - res.y0) / res.hy);
  const inWin = (cut, L) => { const kc = Math.min(res.ny - 1, Math.max(0, layerOf(cut - 1e-7 * res.hy))), k0 = kc - (L - 1); let n = 0;
    for (let q = 0; q < res.nVoid; q++) { const j = layerOf(res.centres[3 * q + 1]); if (j >= k0 && j <= kc) n++; }
    return [n, res.y0 + k0 * res.hy, res.y0 + (kc + 1) * res.hy]; };
  const c0 = clipCalls;
  state.clipPlanes = [{ constant: 6.0, normal: { x: 0, y: 0, z: -1 } }];
  fire('clip-on', 'change');
  { const mm = meshNow(), [n1, lo1, hi1] = inWin(6.0, 1);
    OUT.sec1 = { nMesh: mm.length, count: mm[0] ? mm[0].count : null, want: n1, lo: lo1, hi: hi1, tz: mm[0] ? tzRange(mm[0]) : null,
                 opa: mm[0] ? mm[0].material.opacity : null, tr: mm[0] ? mm[0].material.transparent : null,
                 dw: mm[0] ? mm[0].material.depthWrite : null, clip: clipCalls - c0, status: (ELS['dem-pore-status'] || {}).innerHTML || '',
                 am: Object.assign({}, state.meshes.AM_P.material, { userData: undefined }), se: Object.assign({}, state.meshes.SE.material, { userData: undefined }),
                 popUi: [(ELS['dem-pore-pop'] || {}).value, (ELS['dem-pore-pop-val'] || {}).textContent] }; }
  ELS['dem-pore-slab'].value = '3'; fire('dem-pore-slab', 'input');
  { const mm = meshNow(), [n3, lo3, hi3] = inWin(6.0, 3);
    OUT.sec3 = { count: mm[0] ? mm[0].count : null, want: n3, lo: lo3, hi: hi3, tz: mm[0] ? tzRange(mm[0]) : null }; }
  state.clipPlanes[0].constant = 9.0; fire('clip-pos', 'input');
  { const mm = meshNow(), [n9, lo9, hi9] = inWin(9.0, 3);
    OUT.secMove = { count: mm[0] ? mm[0].count : null, want: n9, lo: lo9, hi: hi9, tz: mm[0] ? tzRange(mm[0]) : null }; }
  //  단면이 칸 면에 정확히 걸리면 (기본 50 % · ny 짝수면 흔하다) — 그 아래 층 (판 쪽에 온전히 남는 층) 의 빈 칸.
  //  칸 번호로 센다: j = round((y − y0)/h − ½) (Float32 중심의 반올림에 흔들리지 않게).  옛 판은 실수 창이라 0 칸이 됐다 (real_14 미리보기)
  ELS['dem-pore-slab'].value = '1'; fire('dem-pore-slab', 'input');
  OUT.faceCut = [2, 3, 4, 5].map(div => {
    const K = Math.floor(res.ny / div), cut = res.y0 + K * res.hy;     // 칸 면 (float64 산술 그대로 — 페이지의 cut 도 이렇게 나온다)
    state.clipPlanes = [{ constant: cut, normal: { x: 0, y: 0, z: -1 } }]; fire('clip-pos', 'input');
    let want = 0;
    for (let q = 0; q < res.nVoid; q++) if (layerOf(res.centres[3 * q + 1]) === K - 1) want++;
    const mm = meshNow();
    return { K, cut, count: mm[0] ? mm[0].count : null, want };
  });
  state.clipPlanes = null; fire('clip-on', 'change');
  { const mm = meshNow();
    OUT.back = { nMesh: mm.length, count: mm[0] ? mm[0].count : null, nVoid: res.nVoid, tr: mm[0] ? mm[0].material.transparent : null,
                 opa: mm[0] ? mm[0].material.opacity : null, status: (ELS['dem-pore-status'] || {}).innerHTML || '',
                 am: Object.assign({}, state.meshes.AM_P.material, { userData: undefined }),
                 popUi: [(ELS['dem-pore-pop'] || {}).value, (ELS['dem-pore-pop-val'] || {}).textContent] }; }
  //  단면 뷰가 꺼진 채 단면 위치 막대를 끌거나 기공 불투명도를 바꿔도 모든 칸 묶음 (수십만 칸) 을 다시 짓지 않는다 — 재질만 바꾼다
  { const g0 = meshNow()[0];
    fire('clip-pos', 'input');
    const g1 = meshNow()[0];
    ELS['dem-pore-op'].value = '20'; fire('dem-pore-op', 'input');
    const g2 = meshNow()[0];
    OUT.noRebuild = { sameAfterClipPos: g0 === g1, sameAfterOp: g1 === g2, opa: g2 ? g2.material.opacity : null,
                      status: (ELS['dem-pore-status'] || {}).innerHTML || '' };
    ELS['dem-pore-op'].value = '8'; fire('dem-pore-op', 'input'); }
  OUT.listen = { clipOn: nListen('clip-on', 'change'), clipPos: nListen('clip-pos', 'input') };
  //  다른 모드에서는 단면 사건이 기공 칸을 만들지 않는다
  state.viewMode = 'default'; _teardownDemPore(state, true);
  state.clipPlanes = [{ constant: 6.0, normal: { x: 0, y: 0, z: -1 } }]; fire('clip-on', 'change');
  OUT.otherMode = { nMesh: meshNow().length };
  state.viewMode = 'dem_pore'; state.clipPlanes = null;
  _teardownDemPore(state);
  OUT.teardown = { nMesh: scene.children.filter(o => o.isInstancedMesh).length, group: state.demPoreGroup,
                   am: Object.assign({}, state.meshes.AM_P.material, { userData: undefined }), se: Object.assign({}, state.meshes.SE.material, { userData: undefined }) };
} catch (e) { OUT.err = String(e && e.stack || e); }
console.log(JSON.stringify(OUT));
"""


def stl_payload_tris(path, scale=1000):
    """웹앱 /3d-data 와 같은 모양 — mesh_info 삼각형 (sim) × scale · 소수 셋째 자리 (app.py serve_3d_data)."""
    tris, cur = [], []
    with open(path, encoding='utf-8') as fh:
        for ln in fh:
            t = ln.split()
            if t and t[0] == 'vertex':
                cur.append([round(float(t[1]) * scale, 3), round(float(t[2]) * scale, 3), round(float(t[3]) * scale, 3)])
                if len(cur) == 3:
                    tris.append(cur)
                    cur = []
    return tris


def load_real14():
    """real_14 기준 덤프 (docs/data/real14_reference_20260928) → 웹앱 입자 (µm · 상 이름) · 판 z (STL)."""
    tmap = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    with gzip.open(os.path.join(REAL14, 'atom_2060000.liggghts.gz'), 'rt') as fh:
        lines = fh.read().splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith('ITEM: ATOMS'))
    cols = lines[i].split()[2:]
    ci = {c: cols.index(c) for c in ('id', 'type', 'x', 'y', 'z', 'radius')}
    bx = [float(v) for v in lines[next(k for k, ln in enumerate(lines) if ln.startswith('ITEM: BOX BOUNDS')) + 1].split()[:2]]
    parts = []
    for ln in lines[i + 1:]:
        v = ln.split()
        if len(v) < len(cols):
            continue
        parts.append({'id': int(v[ci['id']]), 'type': tmap[int(v[ci['type']])],
                      'x': round(float(v[ci['x']]) * 1000, 2), 'y': round(float(v[ci['y']]) * 1000, 2),
                      'z': round(float(v[ci['z']]) * 1000, 2), 'r': round(float(v[ci['radius']]) * 1000, 2)})
    tris = stl_payload_tris(os.path.join(REAL14, 'mesh_2060000.stl'))
    return parts, tris, bx


def mc_union_void(parts, lx, ly, plate_z, n=1_000_000, seed=20261007):
    """웹앱 정확 union 과 같은 계산 — scripts/lhs_union_webapp.coverage (무작위 점 · 반경별 KD 트리 · x·y 주기)."""
    import numpy as np
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import lhs_union_webapp as LU
    X = np.array([[p['x'], p['y'], p['z']] for p in parts], dtype=float)
    R = np.array([p['r'] for p in parts], dtype=float)
    isSE = np.array([p['type'] == 'SE' for p in parts])
    rng = np.random.default_rng(seed)
    Q = np.column_stack([rng.uniform(0, lx, n), rng.uniform(0, ly, n), rng.uniform(0, plate_z, n)])
    cs, ca = LU.coverage(X, R, isSE, 0.0, lx, 0.0, ly, Q)
    v = float(np.mean(~(cs | ca)))
    return v, math.sqrt(v * (1 - v) / n)


REAL_RUN = r"""
const OUT = {};
const box = { x_min: 0, x_max: LX, y_min: 0, y_max: LY, z_min: 0 };
const dom = demPoreDomainTop({ particles: PARTS, mesh_triangles: TRIS });
OUT.dom = dom;
for (const [k, o] of [['normal', {}], ['fine', {}], ['normal_np', { periodicXY: false }]]) {
  const preset = k.split('_')[0];
  const nx = demPoreGridNx(box, dom.zTop, preset);
  const t0 = performance.now();
  const r = computeVoidVoxels(PARTS, box, dom.zTop, nx, o);
  OUT[k] = { ms: performance.now() - t0, vf: r.voidFraction, dims: [r.nx, r.ny, r.nz], h: r.hx, nVoid: r.nVoid };
}
console.log(JSON.stringify(OUT));
"""


def section_pore(js):
    print('[D] DEM 기공 보기 (View Mode "기공 (빈 공간 · 격자 추정)")')
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    sels = re.findall(r'<select id="view-mode".*?</select>', bc, re.S)
    dem_sel = sels[-1] if len(sels) == 2 else ''
    opt = re.search(r'<option value="dem_pore">([^<]*)</option>', dem_sel)
    chk('D0 DEM 조작판 View Mode 에 "기공 (빈 공간 · 격자 추정)" (value dem_pore) 이 있다',
        opt is not None and '기공' in opt.group(1) and '격자 추정' in opt.group(1), f'select {len(sels)} 개 · {opt and opt.group(0)}')
    chk('D0b MPM 조작판에는 없다 (DEM 전용 · MPM 은 옛 "기공만 (pore — XCT처럼)" 그대로)',
        len(sels) == 2 and 'dem_pore' not in sels[0] and '<option value="pore">' in sels[0])
    try:
        av = js_fn(js, 'applyViewMode')
    except (ValueError, AssertionError):
        av = ''
    i_def = av.find("if (!mode || mode === 'default')")
    i_td = av.find('_teardownDemPore(state)')
    chk('D0c 모드를 바꾸면 기공 칸을 걷는다 (applyViewMode 앞머리 · default 분기보다 먼저 _teardownDemPore)',
        0 <= i_td < i_def, f'teardown @{i_td} · default @{i_def}')
    chk("D0d applyViewMode 의 dem_pore 분기가 renderDemPore 를 부른다",
        re.search(r"if \(mode === 'dem_pore'\) \{\s*renderDemPore\(state\);\s*return;\s*\}", av) is not None)

    if not shutil.which('node'):
        chk('D1 node 필요 (기공 함수를 실제로 돌린다)', False, 'node 미설치')
        return
    src, miss = fns(js, ('computeVoidVoxels', 'demPoreDomainTop', 'demPoreGridNx', 'demPoreLegendHTML', 'demPoreStatusHTML'))
    cs, miss_c = consts(js, ('DEM_PORE_PRESETS',))
    m_misc = re.findall(r'^const DEM_PORE_(?:COL|MAX_INSTANCES) = [^;]+;', js, re.M)     # 범례 · 그리기가 쓰는 낱 상수 둘
    if not chk('D1 viewer3d.js 에서 computeVoidVoxels · demPoreDomainTop · demPoreGridNx · demPoreLegendHTML · demPoreStatusHTML · '
               'DEM_PORE_PRESETS · DEM_PORE_COL · DEM_PORE_MAX_INSTANCES 를 잘라 냈다',
               not miss and not miss_c and len(m_misc) == 2, f'없음 {miss + miss_c} · 상수 {m_misc}'):
        return
    cs = cs + '\n' + '\n'.join(m_misc)
    plate = [[[0, 0, 30.2845], [50, 50, 30.2845], [50, 0, 30.2845]], [[0, 0, 30.2845], [0, 50, 30.2845], [50, 50, 30.2845]]]
    pts = [{'x': 10, 'y': 10, 'z': 5, 'r': 2}, {'x': 20, 'y': 20, 'z': 30.836, 'r': 0.5}]
    dtop = {'mesh': {'particles': pts, 'mesh_triangles': plate}, 'none': {'particles': pts},
            'empty': {'particles': pts, 'mesh_triangles': []},
            'low': {'particles': pts, 'mesh_triangles': [[[0, 0, -1], [1, 0, -1], [0, 1, -1]]]}}
    res = run_node('"use strict";\n' + cs + '\n' + src + '\nconst DTOP = ' + json.dumps(dtop) + ';\n' + D_RUN)
    if not chk('D1b node 실행', res is not None):
        return

    e = res['empty']
    chk('D2 빈 상자 = 빈 칸 비율 정확히 1 · 빈 칸 중심 = 모든 칸', e['vf'] == 1 and e['nVoid'] == e['nTotal'] == 20 * 20 * 20
        and e['nC'] == 3 * e['nTotal'] and e['dims'] == [20, 20, 20], repr(e))
    V, S, Vb = 4 / 3 * math.pi * 27, 4 * math.pi * 9, 1000.0
    exact = 1 - V / Vb
    tol = {nx: math.sqrt(3) * (10 / nx) * S / Vb for nx in (10, 20, 40, 80)}     # 표면에서 칸 반대각선 (√3/2 h) 안 칸만 틀릴 수 있다
    errs = {d['nx']: abs(d['vf'] - exact) for d in res['single']}
    chk('D3 구 하나 (r 3 · 상자 10³) = 1 − V_구/V_상자 — 각 격자에서 오차 ≤ √3·h·S/V_상자 (칸이 작을수록 한도가 준다)',
        all(errs[nx] <= tol[nx] for nx in tol), f'정확 {exact:.5f} · 오차 {errs} · 한도 {tol}')
    chk('D3b 가장 고운 격자 (h 0.125) 오차 < 0.5 %p — 표시용으로 충분',
        errs[80] < 0.005, f'{errs[80]:.5f}')
    pk = res['packed']
    chk('D4 꽉 찬 단순 입방 격자 (간격 2 · r 1.8 > √3) = 빈 칸 0 (x·y 주기 상 포함)', pk['per'] == 0, repr(pk))
    chk('D4b 대조 — 주기를 끄면 같은 격자가 0 이 아니다 (상자 가장자리 칸이 비는 것 = 주기 상이 실제로 쓰인다)', pk['nonper'] > 0.01, repr(pk))
    half = 1 - (V / 2) / Vb
    c = res['clip']
    chk('D5 판에서 잘림 — 중심이 판 (z 10) 에 있는 구는 아래 반만 고체 (1 − ½V/V_상자)', abs(c['half'] - half) <= tol[80], repr(c))
    chk('D5b 전체가 판 위 · 전체가 바닥 아래인 구는 고체 0 (빈 칸 비율 정확히 1)', c['above'] == 1 and c['below'] == 1, repr(c))
    chk('D5c 바닥에서 잘림 — 중심이 바닥 (z 0) 인 구는 위 반만', abs(c['floorHalf'] - half) <= tol[80], repr(c))
    w = res['wrap']
    chk('D6 주기 상 — 면 (x 0) · 모서리 (x 0, y 0) · x = L · x < 0 에 걸친 구도 온전한 구 하나와 같은 고체 (상자 가운데 구와 같다)',
        all(abs(w[k] - w['centre']) <= 2e-3 for k in ('face', 'corner', 'atL', 'neg')) and abs(w['centre'] - exact) <= tol[80], repr(w))
    chk('D6b 대조 — 주기를 끄면 면에 걸친 구는 반만 남는다', abs(w['faceNP'] - half) <= tol[80], repr(w))
    chk('D6c 반경 0 · NaN 좌표 입자는 건너뛴다 (빈 칸 비율 1)', res['zeroR'] == 1, repr(res['zeroR']))
    b = res['brute']
    chk(f"D7 무작위 침대 (구 40 · 판 위 · 바닥 아래로 삐져나감 · 주기) — 칸 {b['nTotal']:,} 개 전부 전수 판정과 같다 · 빈 칸 중심은 영역 안",
        b['bad'] == 0 and b['nVoid'] == b['nVoidBF'] and b['outside'] == 0 and 0 < b['nVoid'] < b['nTotal'], repr(b))
    bb = res['bruteBig']
    chk(f"D7b 상자만 한 구 ({bb['nBig']} 개 · 2r + h ≥ L = 최소 영상 가지) · 원점이 0 이 아닌 상자 — 칸 {bb['nTotal']:,} 개 전부 전수 판정과 같다",
        bb['bad'] == 0 and bb['nBig'] >= 2 and 0 < bb['nVoid'] < bb['nTotal'] and bb['x0'] == -5 and bb['y0'] == 2, repr(bb))
    pr = {k: (nx, n, tgt) for k, nx, n, tgt in res['presets']}
    chk('D8 격자 선택 셋 (거침 · 보통 · 고움) — 칸 수가 목표의 ±25 % 안 · 거침 < 보통 < 고움',
        set(pr) == {'coarse', 'normal', 'fine'} and all(0.75 <= n / tgt <= 1.25 for _, n, tgt in pr.values())
        and pr['coarse'][0] < pr['normal'][0] < pr['fine'][0], repr(res['presets']))
    t = res['top']
    chk('D9 판 z = 판 메시 (웹앱 mesh_triangles) 꼭짓점 z — 30.2845 µm · 출처 mesh',
        t['mesh']['source'] == 'mesh' and abs(t['mesh']['zTop'] - 30.2845) < 1e-9, repr(t['mesh']))
    chk('D9b 판 메시 없음 · 빈 메시 · 바닥 아래 메시 → 입자 윗면 최댓값 (max z + r = 31.336) · 출처 particle_top (판 아님)',
        all(t[k]['source'] == 'particle_top' and abs(t[k]['zTop'] - 31.336) < 1e-9 for k in ('none', 'empty', 'low')), repr(t))
    lg = res['leg']
    plain = {k: re.sub(r'<[^>]+>', '', v) for k, v in lg.items()}
    chk('D10 범례 = "격자 추정 · 표시용 — 보고 porosity 는 표의 값" (보고 값처럼 보이지 않게)',
        all('격자 추정 · 표시용 — 보고 porosity 는 표의 값' in v for v in plain.values()), plain['mesh'][:200])
    chk('D10b 범례에 격자 빈 칸 비율 (17.1 %) · 격자 크기 (100×100×61 · 칸 0.50 µm) · 빈 칸 수',
        '17.1 %' in plain['mesh'] and '100×100×61' in plain['mesh'] and '0.50 µm' in plain['mesh'] and '104,432' in plain['mesh'],
        plain['mesh'][:400])
    chk('D10c 범례에 영역 — 판 메시면 "판 메시" · 아니면 "판 메시 없음 … 입자 윗면 (판 위치 아님)"',
        '판 메시' in plain['mesh'] and '판 메시 없음' not in plain['mesh']
        and '판 메시 없음' in plain['top'] and '입자 윗면' in plain['top'] and '판 위치 아님' in plain['top'], plain['top'][:400])
    chk('D10d 범례에 정의 — 겹친 부피 한 번 (합집합) · 표의 ε_sphere (구 부피 합) 와 다른 양 · x·y 주기',
        '합집합' in plain['mesh'] and 'ε_sphere' in plain['mesh'] and '주기' in plain['mesh'], plain['mesh'])
    st = {k: re.sub(r'<[^>]+>', '', v) for k, v in res['status'].items()}
    chk('D10e 표시 줄 — 표시 상한으로 솎으면 그렇게 말한다 (2 칸마다 1 개) · 안 솎으면 말하지 않는다',
        '2 칸마다 1 개' in st['cap'] and '칸마다' not in st['full'] and '104,432' in st['full'], repr(st))
    chk('D10f 범례에 격자 선택 · 기공 불투명도 · 입자 불투명도 · 단면 판 두께 조작 · 표시 줄 (id dem-pore-grid · op · pop · slab · status)',
        all(f'id="{i}"' in lg['mesh'] for i in ('dem-pore-grid', 'dem-pore-op', 'dem-pore-pop', 'dem-pore-slab', 'dem-pore-status')),
        lg['mesh'][-700:])
    chk('D10g 표시 줄 (단면) — 단면 y = 25.00 µm · 칸 1 층 · 불투명 · 1,234 칸',
        all(w in st['sec'] for w in ('단면', 'y = 25.00 µm', '1 층', '불투명', '1,234')), st['sec'])
    chk('D10h 범례가 단면 동작을 말한다 — 단면 뷰 (Y-슬라이스) 를 켜면 그 자리 칸 층만 불투명 (기공 단면) · 끄면 모든 빈 칸 반투명',
        '단면 뷰 (Y-슬라이스)' in plain['mesh'] and '불투명' in plain['mesh'] and '반투명' in plain['mesh'], plain['mesh'][-500:])

    # ── 그리기 (THREE 껍데기) ──
    src_r, miss_r = fns(js, ('computeVoidVoxels', 'demPoreDomainTop', 'demPoreGridNx', 'demPoreLegendHTML', 'demPoreStatusHTML',
                             'renderDemPore', '_demPoreBuildMesh', '_demPoreCutY', '_teardownDemPore', '_demPoreFade',
                             '_demPoreWireControls'))
    cs_r, miss_rc = consts(js, ('DEM_PORE_PRESETS', 'COL'))
    m_misc = re.findall(r'^const DEM_PORE_(?:COL|MAX_INSTANCES) = [^;]+;', js, re.M)
    if not chk('D11 그리기 함수 (renderDemPore · _demPoreBuildMesh · _demPoreCutY · _teardownDemPore · _demPoreFade · '
               '_demPoreWireControls) 를 잘라 냈다',
               not miss_r and not miss_rc and len(m_misc) == 2, f'없음 {miss_r + miss_rc} · 상수 {m_misc}'):
        return
    rr = run_node(R_SHIM + cs_r + '\n' + '\n'.join(m_misc) + '\n' + src_r + '\n' + R_RUN)
    if not chk('D11b node 실행 (renderDemPore)', rr is not None and rr.get('err') is None, repr(rr and rr.get('err'))[:600]):
        return
    g = rr['render']
    chk(f"D12 빈 칸마다 InstancedMesh 칸 하나 ({g['count']:,} = 빈 칸 {g['nVoid']:,}) · 장면에 하나 · state.demPoreGroup",
        g['nMesh'] == 1 and g['count'] == g['nVoid'] > 0 and g['groupIsMesh'], repr({k: g[k] for k in ('nMesh', 'count', 'nVoid', 'groupIsMesh')}))
    chk('D12b 칸 크기 = 격자 칸 (three 축: x · data z · data y) · 위치 = 빈 칸 중심 (three 축 순서 x, z, y · 행렬 단위 크기)',
        g['dims'] is not None and all(abs(a - b) < 1e-9 for a, b in zip(g['dims'], g['h'])) and g['firstEq'] is True
        and g['needsUpdate'] is True, repr({k: g[k] for k in ('dims', 'h', 'firstEq', 'needsUpdate')}))
    chk('D12c 위치가 영역 안 — three x ∈ [0, 10] · three y (= data z) ∈ [0, 판 8] · three z (= data y) ∈ [0, 12]',
        0 <= g['tx'][0] and g['tx'][1] <= 10 and 0 <= g['ty'][0] and g['ty'][1] <= 8 and 0 <= g['tz'][0] and g['tz'][1] <= 12
        and g['tz'][1] > 10, repr({k: g[k] for k in ('tx', 'ty', 'tz')}))
    chk('D12d 단면 뷰 (Y-슬라이스) 를 칸이 생긴 뒤 다시 적용한다 (state.applyClip) · PNG 에서 빠지는 장식이 아니다 · 시야 밖 잘림 끔',
        g['clipCalls'] >= 1 and g['deco'] is False and g['frustumCulled'] is False, repr({k: g[k] for k in ('clipCalls', 'deco', 'frustumCulled')}))
    chk('D12e 입자 흐리게 (반투명 · 깊이 쓰기 끔 = 뒤의 기공이 보인다) · 판 메시 숨김',
        g['am']['opacity'] < 1 and g['am']['transparent'] is True and g['am']['depthWrite'] is False
        and g['se']['opacity'] < 0.85 and g['se']['depthWrite'] is False and g['plate'] is False, repr({k: g[k] for k in ('am', 'se', 'plate')}))
    chk('D12f 범례가 같은 문구로 붙는다 (격자 추정 · 표시용)', '격자 추정 · 표시용 — 보고 porosity 는 표의 값' in re.sub(r'<[^>]+>', '', g['legend']))
    chk('D12g 단면 뷰 꺼짐 = 모든 빈 칸 반투명 안개 (기본 불투명도 0.08 · 깊이 쓰기 끔 — 칸 ~20 겹이 겹쳐도 다 덮지 않게)',
        g['matOpa'] == 0.08 and g['matDepthWrite'] is False, repr({k: g[k] for k in ('matOpa', 'matDepthWrite')}))
    a2 = rr['again']
    chk('D13 다시 그려도 칸 묶음은 하나 (옛 묶음은 버리고 GPU 자원 해제)', a2['nMesh'] == 1 and a2['oldDisposed'] is True, repr(a2))
    s1, s3, sm, bk = rr['sec1'], rr['sec3'], rr['secMove'], rr['back']
    eps = 1e-6
    chk(f"D17 단면 뷰 켬 (y = 6) = 판을 품은 칸 1 층만 ({s1['count']:,} 칸 = 그 층의 빈 칸 {s1['want']:,}) · 위치가 그 층 안",
        s1['nMesh'] == 1 and s1['count'] == s1['want'] > 0 and s1['tz'] is not None
        and s1['lo'] - eps <= s1['tz'][0] and s1['tz'][1] < s1['hi'] + eps, repr(s1))
    chk('D17b 단면 칸은 불투명 (불투명도 1 · 깊이 쓰기) = 기공 단면이 또렷하다 · 새 칸에 단면 판을 다시 건다 (applyClip) · 표시 줄이 단면을 말한다',
        s1['opa'] == 1 and s1['tr'] is False and s1['dw'] is True and s1['clip'] >= 1 and '단면' in s1['status'], repr(s1))
    chk(f"D17c 판 두께 3 층 = 판을 품은 층과 그 아래 2 층의 빈 칸 ({s3['count']:,} = {s3['want']:,} > 1 층 {s1['count']:,})",
        s3['count'] == s3['want'] > s1['count'] and s3['tz'] is not None
        and s3['lo'] - eps <= s3['tz'][0] and s3['tz'][1] < s3['hi'] + eps, repr(s3))
    chk(f"D17d 단면 위치를 옮기면 (y = 9) 칸 층이 따라간다 ({sm['count']:,} = {sm['want']:,})",
        sm['count'] == sm['want'] > 0 and sm['tz'] is not None
        and sm['lo'] - eps <= sm['tz'][0] and sm['tz'][1] < sm['hi'] + eps, repr(sm))
    fc = rr['faceCut']
    chk('D17i 단면이 칸 면에 정확히 걸려도 (ny/2 · /3 · /4 · /5 번째 면) 그 아래 층의 빈 칸을 그린다 — 0 칸이 되지 않는다 '
        '(real_14 미리보기에서 기본 50 % 단면이 0 칸이던 결함)',
        all(d['count'] == d['want'] > 0 for d in fc), repr(fc))
    chk('D17e 단면 뷰 끔 = 다시 모든 빈 칸 반투명', bk['nMesh'] == 1 and bk['count'] == bk['nVoid'] and bk['tr'] is True
        and bk['opa'] == 0.08 and '단면' not in bk['status'], repr(bk))
    chk('D17g 입자 불투명도는 보기마다 따로 — 단면 = 불투명 1 (AM · SE · 깊이 쓰기 = 3 상 단면) · 3D 안개 = 0.15 (다시 흐리게) · 조작 막대가 따라간다',
        (s1['am']['opacity'], s1['am']['transparent'], s1['am']['depthWrite']) == (1, False, True)
        and (s1['se']['opacity'], s1['se']['depthWrite']) == (1, True) and s1['popUi'] == ['100', '1.00']
        and (bk['am']['opacity'], bk['am']['transparent'], bk['am']['depthWrite']) == (0.15, True, False) and bk['popUi'] == ['15', '0.15'],
        repr({'sec': (s1['am'], s1['se'], s1['popUi']), 'back': (bk['am'], bk['popUi'])}))
    nr = rr['noRebuild']
    chk('D17h 단면 뷰 꺼짐에서 단면 위치 막대 · 기공 불투명도를 움직여도 모든 칸 묶음을 다시 짓지 않는다 (재질만 · 표시 줄 0.20)',
        nr['sameAfterClipPos'] is True and nr['sameAfterOp'] is True and nr['opa'] == 0.2 and '0.20' in nr['status'], repr(nr))
    chk('D17f 단면 사건 듣개는 한 번만 붙는다 (두 번 그려도 clip-on change 1 · clip-pos input 1) · 다른 모드에서는 기공 칸을 만들지 않는다',
        rr['listen'] == {'clipOn': 1, 'clipPos': 1} and rr['otherMode']['nMesh'] == 0,
        repr({'listen': rr['listen'], 'other': rr['otherMode']}))
    td = rr['teardown']
    chk('D13b 걷기 = 칸 묶음 제거 · 입자 재질 되돌림 (불투명도 · 투명 · 깊이 쓰기 = 처음 값)',
        td['nMesh'] == 0 and td['group'] is None
        and (td['am']['opacity'], td['am']['transparent'], td['am']['depthWrite']) == (1, False, True)
        and (td['se']['opacity'], td['se']['transparent'], td['se']['depthWrite']) == (0.85, True, False), repr(td))

    # ── real_14 실침대 ──
    if not os.path.isdir(REAL14):
        chk('D14 real_14 기준 덤프 (docs/data/real14_reference_20260928)', False, '없음')
        return
    parts, tris, bx = load_real14()
    lx = bx[1] - bx[0]
    n_ty = {t: sum(1 for p in parts if p['type'] == t) for t in ('AM_P', 'AM_S', 'SE')}
    chk('D14 real_14 = 33,289 입자 (AM_P 36 · AM_S 421 · SE 32,832) · 상자 50 µm', len(parts) == 33289
        and n_ty == {'AM_P': 36, 'AM_S': 421, 'SE': 32832} and abs(lx * 1000 - 50) < 1e-9, repr(n_ty))
    rres = run_node('"use strict";\n' + cs + '\n' + src + '\nconst PARTS = ' + json.dumps(parts) + ';\nconst TRIS = ' + json.dumps(tris)
                    + f';\nconst LX = {lx * 1000!r}, LY = {lx * 1000!r};\n' + REAL_RUN)
    if not chk('D14b node 실행 (real_14)', rres is not None):
        return
    dom = rres['dom']
    chk('D14c 판 z = STL 30.2845 µm (웹앱 payload 소수 셋째 자리 · 출처 mesh)', dom['source'] == 'mesh'
        and abs(dom['zTop'] - 30.2845) <= 1e-3, repr(dom))
    try:
        mc, se = mc_union_void(parts, 50.0, 50.0, dom['zTop'])
    except Exception as ex:              # scipy 없음 등 — 건너뛰지 않고 FAIL
        chk('D15 기준 = 웹앱 정확 union 계산 (lhs_union_webapp.coverage · scipy)', False, repr(ex))
        return
    nm, fi, npr = rres['normal'], rres['fine'], rres['normal_np']
    print(f"    real_14: MC 정확 union {100 * mc:.3f} ± {100 * se:.3f} % · 격자 보통 {100 * nm['vf']:.3f} % ({nm['dims']} · h {nm['h']:.3f} µm · "
          f"{nm['ms']:.0f} ms) · 고움 {100 * fi['vf']:.3f} % ({fi['dims']} · h {fi['h']:.3f} µm · {fi['ms']:.0f} ms) · 주기 끔 {100 * npr['vf']:.3f} %")
    chk('D15 real_14 보통 격자 빈 칸 비율 = 웹앱 정확 union (무작위 점 10⁶ · KD 트리) ± 0.5 %p',
        abs(nm['vf'] - mc) <= 0.005, f"격자 {nm['vf']:.5f} · MC {mc:.5f} ± {se:.5f}")
    chk('D15b real_14 고움 격자 = 정확 union ± 0.3 %p',
        abs(fi['vf'] - mc) <= 0.003, f"격자 {fi['vf']:.5f} · MC {mc:.5f}")
    chk('D15c 대조 — 주기 상을 빼면 정확 union 에서 1 %p 넘게 벗어난다 (위 일치가 주기 처리 덕이라는 판별력)',
        npr['vf'] - mc > 0.01, f"주기 끔 {npr['vf']:.5f} · MC {mc:.5f}")
    chk('D16 브라우저급 시간 — 보통 < 3 s · 고움 < 8 s (node · 33,289 입자)', nm['ms'] < 3000 and fi['ms'] < 8000,
        f"보통 {nm['ms']:.0f} ms · 고움 {fi['ms']:.0f} ms")


def main():
    js = open(VIEWER_JS, encoding='utf-8').read()
    section_path(js)
    section_pore(js)
    print()
    print(f'{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())

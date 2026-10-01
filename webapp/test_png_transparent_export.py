#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""투명 배경 PNG 내보내기 회귀 — 슬라이드에 붙일 그림 (2026-10-01 요청).

  python3 webapp/test_png_transparent_export.py      # 종료코드 0 = PASS

두 화면의 그림 내보내기는 **둘 다 브라우저 안에서** 만들어진다 (서버 PNG 경로 없음 — mixer_bed.py 는 JSON 만 준다):

  [M] /mixer "침대 보기" — ⬇ 고화질 PNG = 2D 캔버스 (`paint2d`) 또는 WebGL 복사 (`grab3d`) + 캡션 띠 (`withCaption`).
      옛 판은 배경을 늘 #fbfbf8 (그림) · #ffffff (캡션 띠) 로 칠했다 — 투명 선택이 없었다.
      → ☐ "투명 배경 PNG" (#bedPngClear · **기본 꺼짐** = 옛 출력 그대로).  켜면 그 PNG 한 장만 배경 알파 0 ·
        캡션 두 줄 (런 · step · 시간 · 보기 / 보기 전용 표지) 은 어두운 글자 그대로.  화면 · GIF 는 배경 그대로.
  [V] 케이스 페이지 "3D 전극 구조" (DEM 3D · MPM 압축 전 · MPM 압축 후 — 셋 다 viewer3d.js `initElectrodeViewer`).
      Screenshot 은 옛 판부터 구조 모드에서 투명이고, 전류밀도 장 모드 (je_field · ji_field · je) 만 뷰어 배경색이었다
      (7a6a43c93 — 차가운 장이 흰 종이에서 깨지지 않게).  → ☑ "투명 배경 PNG" (#shot-transparent) 가 그 모드별 기본값을
        **보여 주고** (모드를 바꾸면 그 모드의 기본값으로) 바꿀 수 있게 한다 — 장 모드도 투명 = opt-in · 기본값 불변.

★ 기능 시험은 페이지의 **그 함수들을 그대로** 잘라 node 에서 돌린다 (브라우저 없음 — test_seminar_dom.mjs 와 같은 원칙).
  캔버스는 껍데기다: 두 점 (왼쪽 위 = 그림 · 왼쪽 아래 = 캡션 띠) 의 알파만 따라가며 칠하기 (fillRect) · 지우기
  (clearRect) · 복사 (drawImage) 를 그대로 합성한다.  ★ 기본 (꺼짐) 출력이 **불투명**으로 나오는 것이 같은 껍데기의
  판별력 대조다 — 껍데기가 아무것도 못 보면 그쪽이 빨개진다.
⚠ node 가 없으면 기능 시험을 건너뛰지 않고 FAIL 한다 (돌지 않는 검사는 없는 것과 같다 — 규칙 K).
"""
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
SINGLE_HTML = os.path.join(HERE, 'templates', 'single.html')

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


# ══════════════════════════════════════════════════════════════════════════════
#  [M] /mixer 침대 보기
# ══════════════════════════════════════════════════════════════════════════════
#  두 점 캔버스 껍데기 — 크기를 바꾸면 비워진다 (브라우저와 같다) · toBlob 은 마지막 출력 캔버스를 잡아 둔다
CANVAS_SHIM = r"""
'use strict';
function alphaOf(s) {
  if (typeof s !== 'string') return 1;
  const t = s.replace(/\s+/g, '').toLowerCase();
  if (t === 'transparent') return 0;
  const m = t.match(/^rgba\(([^)]*)\)$/);
  return m ? +m[1].split(',')[3] : 1;
}
const over = (a, b) => a + b * (1 - a);
const hit = (p, x, y, w, h) => p.x >= x && p.x < x + w && p.y >= y && p.y < y + h;
class Ctx {
  constructor(cv) { this.cv = cv; this.fillStyle = '#000000'; this.strokeStyle = '#000000'; this.globalAlpha = 1; this.font = ''; this.lineWidth = 1; }
  fillRect(x, y, w, h) {
    const a = alphaOf(this.fillStyle) * this.globalAlpha;
    this.cv.ops.push(['fillRect', this.fillStyle, x, y, w, h, x <= 0 && y <= 0 && x + w >= this.cv.width && y + h >= this.cv.height]);
    for (const p of this.cv.probes()) if (hit(p, x, y, w, h)) p.a = over(a, p.a);
  }
  clearRect(x, y, w, h) { this.cv.ops.push(['clearRect', null, x, y, w, h]); for (const p of this.cv.probes()) if (hit(p, x, y, w, h)) p.a = 0; }
  drawImage(src, dx, dy, dw, dh) {
    const w = dw === undefined ? src.width : dw, h = dh === undefined ? src.height : dh;
    this.cv.ops.push(['drawImage', null, dx, dy, w, h]);
    for (const p of this.cv.probes()) if (hit(p, dx, dy, w, h)) p.a = over(src.alphaAt(p.x - dx, p.y - dy) * this.globalAlpha, p.a);
  }
  fillText(t) { this.cv.ops.push(['fillText', this.fillStyle, String(t)]); }
  fill() { this.cv.ops.push(['fill', this.fillStyle]); }
  beginPath() {} moveTo() {} lineTo() {} arc() {} stroke() {}
  getImageData(x, y, w, h) { return { data: new Uint8ClampedArray(w * h * 4) }; }
}
let LAST_OUT = null;
class Canvas {
  constructor() { this._w = 300; this._h = 150; this.ops = []; this._ctx = null; this._reset(); }
  _reset() { this.tl = { x: 0, y: 0, a: 0 }; this.bl = { x: 0, y: Math.max(0, this._h - 1), a: 0 }; }
  probes() { return [this.tl, this.bl]; }
  get width() { return this._w; } set width(v) { this._w = v; this._reset(); }
  get height() { return this._h; } set height(v) { this._h = v; this._reset(); }
  alphaAt(x, y) { return y < this._h / 2 ? this.tl.a : this.bl.a; }
  getContext() { return this._ctx || (this._ctx = new Ctx(this)); }
  toBlob(cb) { LAST_OUT = this; cb({ size: 4321 }); }
}
const document = { createElement: () => new Canvas() };
const window = { devicePixelRatio: 1 };
const THREE = { Vector2: class { constructor() { this.x = 0; this.y = 0; } },
                Color: class { constructor(v) { this.v = v === undefined ? 0 : v; } } };
//  WebGL 캔버스 껍데기 — render 가 배경 (scene.background 가 있으면 불투명 · 없으면 지우기 알파) 으로 통째로 칠한다
function mkGL(clearAlpha) {
  const cv = new Canvas(); cv.width = 800; cv.height = 576;
  return { pr: 1, w: 800, h: 576, cc: 0x000000, ca: clearAlpha, domElement: cv, renders: [],
    getPixelRatio() { return this.pr; },
    setPixelRatio(p) { this.pr = p; cv.width = Math.round(this.w * p); cv.height = Math.round(this.h * p); },
    getSize(v) { v.x = this.w; v.y = this.h; return v; },
    getClearColor(c) { c.v = this.cc; return c; }, getClearAlpha() { return this.ca; },
    setClearColor(c, a = 1) { this.cc = (c && typeof c === 'object') ? c.v : c; this.ca = a; },
    setClearAlpha(a) { this.ca = a; },
    render(scene) { const a = scene.background ? 1 : this.ca; cv.tl.a = a; cv.bl.a = a; this.renders.push({ ca: this.ca, bg: !!scene.background, pr: this.pr }); } };
}
const nf = new Intl.NumberFormat('ko-KR');
const EL = { bedPngScale: { value: '2' }, bedPngClear: { checked: false }, bedExportMsg: { textContent: '', className: '' } };
const $ = (id) => EL[id] || null;
let VIEW = 'proj';
function view() { return VIEW; }
const DL = [];
function download(b, name) { DL.push(name); }
function exmsg(t) { EL.bedExportMsg.textContent = t || ''; }
const S = { data: null, hidden: {}, xr: [-0.0026, 0.0026], three: null };
const META = { root: 0, run: 'LC_s67867967', step: 1001, time_s: 1.001, rev: 1.6, phase: 'rotation', view: 'proj', selection: null,
  types_present: { '1': { name: 'AM_P', color: '#5b5b5b', n_shown: 1, n_total: 1 }, '3': { name: 'SE', color: '#c9b88a', n_shown: 2, n_total: 2 } },
  drum: { R: 0.0131, x_min: -0.0026, x_max: 0.0026 }, bounds: { x: [-0.001, 0.001], y: [-0.004, 0.004], z: [-0.011, -0.006] }, r_max: 0.0007 };
"""

MIXER_RUN = r"""
function setData(v) {
  const sel = v === 'slab' ? { rule: 'x0 - t/2 <= x <= x0 + t/2', x0: 0, t: 0.001 } : null;
  S.data = { meta: Object.assign({}, META, { view: v, selection: sel }), n: 3,
             x: new Float32Array([0, 0.0003, -0.0004]), y: new Float32Array([0.002, -0.003, 0.001]),
             z: new Float32Array([-0.008, -0.010, -0.009]), r: new Float32Array([0.0007, 0.0001, 0.0001]), t: new Uint8Array([1, 3, 3]) };
}
const OUT = {};
for (const v of ['proj', 'slab', '3d']) for (const clear of [false, true]) for (const glA of (v === '3d' ? [0, 1] : [0])) {
  VIEW = v; setData(v); EL.bedPngClear.checked = clear; DL.length = 0; LAST_OUT = null; EL.bedExportMsg.textContent = '';
  const gl = mkGL(glA);
  S.three = v === '3d' ? { THREE: THREE, renderer: gl, scene: { background: null }, cam: {} } : null;
  let err = null;
  try { exportPng(); } catch (e) { err = String(e && e.stack || e); }
  const o = LAST_OUT;
  OUT[v + '|' + clear + '|' + glA] = {
    err: err, file: DL[0] || null, msg: EL.bedExportMsg.textContent, caption: captionText(),
    tl: o ? o.tl.a : null, bl: o ? o.bl.a : null,
    outFills: o ? o.ops.filter(q => q[0] === 'fillRect' && q[6]).map(q => q[1]) : null,
    texts: o ? o.ops.filter(q => q[0] === 'fillText').map(q => [q[1], q[2]]) : null,
    gl: v === '3d' ? { ca: gl.ca, cc: gl.cc, pr: gl.pr, renders: gl.renders } : null };
}
//  화면 (draw2d → paint2d 인자 둘) · GIF 프레임 (captureFrame) 은 체크박스와 무관하게 배경 그대로여야 한다
VIEW = 'proj'; setData('proj'); EL.bedPngClear.checked = true; S.three = null;
const scr = document.createElement('canvas'); paint2d(scr, 800);
let fr = null, frErr = null; try { fr = captureFrame(640); } catch (e) { frErr = String(e); }
OUT.screen = { tl: scr.tl.a, bl: scr.bl.a };
OUT.gifFrame = { tl: fr ? fr.tl.a : null, bl: fr ? fr.bl.a : null, err: frErr };
console.log(JSON.stringify(OUT));
"""


def section_mixer(html):
    print('[M] /mixer 침대 보기 — ⬇ 고화질 PNG')
    row = re.search(r'<div class="bed-row bed-tools">((?:(?!</div>).)*?id="bedPng"(?:(?!</div>).)*)</div>', html, re.S)
    rtxt = row.group(1) if row else ''
    tag = re.search(r'<input[^>]*id="bedPngClear"[^>]*>', rtxt)
    chk('M1 PNG 버튼과 같은 줄에 ☐ "투명 배경 PNG" (#bedPngClear · checkbox)',
        bool(tag) and 'type="checkbox"' in tag.group(0) and '투명 배경 PNG' in rtxt, rtxt.strip()[:200])
    chk('M1b 기본 꺼짐 (checked 속성 없음 = 옛 출력 그대로)', bool(tag) and 'checked' not in tag.group(0))
    chk('M1c 반복 체크박스와 같은 꼴 (<label …><input type="checkbox" …> 글</label>)',
        bool(re.search(r'<label[^>]*><input type="checkbox" id="bedPngClear"[^>]*>\s*투명 배경 PNG</label>', rtxt)))

    if not shutil.which('node'):
        chk('M2 node 필요 (내보내기 함수를 실제로 돌린다)', False, 'node 미설치')
        return
    src, miss = fns(html, ('typeOrder', 'mm', 'paint2d', 'captionText', 'withCaption', 'grab3d', 'exportPng', 'captureFrame'))
    if not chk('M2 페이지에서 내보내기 함수를 잘라 냈다', not miss, f'없음 {miss}'):
        return
    res = run_node(CANVAS_SHIM + '\n' + src + '\n' + MIXER_RUN)
    if not chk('M2b node 실행', res is not None):
        return
    for v in ('proj', 'slab', '3d'):
        d = res[f'{v}|false|0']
        chk(f'M3 [{v}] 기본 (꺼짐) = 불투명 — 그림 · 캡션 띠 알파 1 (옛 출력 그대로 · 껍데기 판별력 대조)',
            d['err'] is None and d['tl'] == 1 and d['bl'] == 1, f"tl {d['tl']} · bl {d['bl']} · {d['err']}")
        chk(f'M3b [{v}] 기본 파일 이름 그대로 (mixer_<런>_step<step>_<보기>.png)',
            d['file'] == f'mixer_LC_s67867967_step1001_{v}.png', str(d['file']))
        chk(f'M3c [{v}] 기본 = 캡션 띠를 #ffffff 로 칠한다 (옛 판과 같은 칠)', d['outFills'] == ['#ffffff'], repr(d['outFills']))
        t = res[f'{v}|true|0']
        chk(f'M4 [{v}] ☑ 투명 = 그림 · 캡션 띠 알파 0', t['err'] is None and t['tl'] == 0 and t['bl'] == 0,
            f"tl {t['tl']} · bl {t['bl']} · {t['err']}")
        chk(f'M4b [{v}] ☑ 투명 = 출력 캔버스를 통째로 칠하는 불투명 칠이 없다', t['outFills'] == [], repr(t['outFills']))
        tx = dict((s, c) for c, s in (t['texts'] or []))
        chk(f'M4c [{v}] ☑ 투명 = 캡션 두 줄 (런 · step · 보기 / 보기 전용 표지) 을 어두운 글자로 그대로 쓴다',
            bool(t['caption']) and t['caption'].startswith('LC_s67867967 · step') and tx.get(t['caption']) == '#222'
            and any(s.startswith('보기 전용 — 판정은 3D 칸 M 으로만') and c == '#8a5a00' for s, c in tx.items()),
            repr(t['texts'])[:240])
        chk(f'M4d [{v}] ☑ 투명 = 파일 이름에 _transparent (기본 이름과 구분)',
            t['file'] == f'mixer_LC_s67867967_step1001_{v}_transparent.png', str(t['file']))
    g = res['3d|true|1']
    snap = [r for r in (g['gl'] or {}).get('renders', []) if r['pr'] != 1]
    chk('M5 [3d] ☑ 투명 = 렌더러가 불투명 지우기 (알파 1) 로 바뀌어 있어도 그 한 장은 알파 0 으로 지운다',
        g['err'] is None and g['tl'] == 0 and g['bl'] == 0 and bool(snap) and all(r['ca'] == 0 and not r['bg'] for r in snap),
        f"tl {g['tl']} · snap {snap} · {g['err']}")
    chk('M5b [3d] 찍은 뒤 렌더러 지우기 색 · 알파 · 픽셀 비율 복구 (화면 그대로)',
        g['gl'] is not None and g['gl']['ca'] == 1 and g['gl']['cc'] == 0 and g['gl']['pr'] == 1, repr(g['gl'])[:200])
    g0 = res['3d|false|1']
    chk('M5c [3d] 기본 (꺼짐) 은 렌더러 지우기 알파를 건드리지 않는다 (옛 판과 같은 렌더)',
        g0['gl'] is not None and all(r['ca'] == 1 for r in g0['gl']['renders']) and g0['gl']['ca'] == 1, repr(g0['gl'])[:200])
    chk('M6 화면 그림 (paint2d 인자 둘) 은 배경 그대로 #fbfbf8 (체크박스 무관)',
        res['screen']['tl'] == 1, repr(res['screen']))
    chk('M6b GIF 프레임 (captureFrame) 은 배경 그대로 — 체크박스를 켜도 불투명 (GIF 는 알파 없음)',
        res['gifFrame']['err'] is None and res['gifFrame']['tl'] == 1 and res['gifFrame']['bl'] == 1, repr(res['gifFrame']))


# ══════════════════════════════════════════════════════════════════════════════
#  [V] 케이스 페이지 3D 전극 구조 (viewer3d.js)
# ══════════════════════════════════════════════════════════════════════════════
V_SHIM = r"""
'use strict';
const THREE = { Color: class { constructor(v) { this.v = v === undefined ? 0 : v; } },
                Vector2: class { constructor() { this.x = 0; this.y = 0; } } };
function mkR(cc, ca) {
  const cv = { width: 1000, height: 800, a: null, toDataURL() { return 'data:image/png;alpha=' + this.a; } };
  return { cc: cc, ca: ca, pr: 2, w: 500, h: 400, domElement: cv, renders: [],
    getClearColor(c) { c.v = this.cc; return c; }, getClearAlpha() { return this.ca; },
    setClearColor(c, a = 1) { this.cc = (c && typeof c === 'object') ? c.v : c; this.ca = a; },
    getPixelRatio() { return this.pr; }, setPixelRatio(p) { this.pr = p; },
    getSize(v) { v.x = this.w; v.y = this.h; return v; }, setSize(w, h) { this.w = w; this.h = h; },
    render(scene) { cv.a = scene.background ? 1 : this.ca;
      this.renders.push({ ca: this.ca, bg: scene.background ? scene.background.v : null, w: this.w,
                          deco: scene.objs.filter(o => o.userData.isDecoration && o.visible).length }); } };
}
function mkScene() {
  const objs = [{ userData: { isDecoration: true }, visible: true }, { userData: { isDecoration: true }, visible: false },
                { userData: {}, visible: true }];
  return { background: null, objs: objs, traverse(f) { objs.forEach(f); } };
}
"""

V_RUN = r"""
const OUT = { defaults: MODES.map(m => [m, shotTransparentDefault(m)]), bg: COL.BG };
for (const tr of [true, false]) {
  const r = mkR(COL.BG, 1), s = mkScene();
  let url = null, err = null;
  try { url = captureScreenshotPNG(r, s, {}, tr); } catch (e) { err = String(e && e.stack || e); }
  const snap = r.renders.filter(x => x.w === 3000);
  OUT[String(tr)] = { url: url, err: err, snap: snap,
    after: { cc: r.cc, ca: r.ca, pr: r.pr, w: r.w, h: r.h, bg: s.background, vis: s.objs.map(o => o.visible) } };
}
console.log(JSON.stringify(OUT));
"""

OPAQUE_MODES = {'je_field', 'ji_field', 'je'}          # 7a6a43c93 의 darkField 목록 (je_bare 는 그 뒤 빠졌다) — 옛 기본값


def section_viewer():
    print('[V] 케이스 페이지 "3D 전극 구조" — Screenshot')
    sh = open(SINGLE_HTML, encoding='utf-8').read()
    tabs = re.findall(r'onclick="load3DViewer\(\'([a-z-]+)\'\)"', sh)
    chk('V0 탭 셋 (DEM 3D · MPM 압축 전 · MPM 압축 후) 이 한 로더 → viewer3d.js initElectrodeViewer (같은 Screenshot)',
        {'dem', 'mpm-seed', 'mpm'} <= set(tabs) and "mod.initElectrodeViewer('viewer-container', urls[mode])" in sh, repr(tabs))

    js = open(VIEWER_JS, encoding='utf-8').read()
    shots = [m.start() for m in re.finditer(r'<button data-action="screenshot">Screenshot</button>', js)]
    near = [js[i:i + 700] for i in shots]
    lab = [re.search(r'<label[^>]*><input type="checkbox" id="shot-transparent"([^>]*)>\s*투명 배경 PNG</label>', t) for t in near]
    chk('V1 두 조작판 (MPM · DEM) 모두 Screenshot 바로 옆에 ☑ "투명 배경 PNG" (#shot-transparent)',
        len(shots) == 2 and all(lab), f'Screenshot {len(shots)} · 체크박스 {[bool(x) for x in lab]}')
    chk('V1b 처음 상태 = 켜짐 (처음 모드 Default 는 구조 모드 = 옛 판도 투명)',
        all(x and 'checked' in x.group(1) for x in lab))

    try:
        wc = js_fn(js, 'wireControls')
    except (ValueError, AssertionError):
        wc = ''
    i_sh = wc.find("action === 'screenshot'")
    shot_br = wc[i_sh:wc.find("} else if (action ===", i_sh)] if i_sh >= 0 else ''      # Screenshot 분기 하나
    chk('V2 Screenshot 이 체크박스 상태로 배경을 정한다 (captureScreenshotPNG(…, #shot-transparent.checked))',
        "querySelector('#shot-transparent')" in wc
        and re.search(r'captureScreenshotPNG\(renderer, scene, camera, [^;]*\.checked', shot_br) is not None,
        shot_br[:200])
    chk('V2b 파일 이름 · 저장 대화상자 그대로 (electrode_3d.png · saveWithDialog)',
        "saveWithDialog(dataUrl, 'electrode_3d.png', btn, 'Screenshot')" in shot_br)
    chk('V2c 모드를 바꾸면 체크박스가 그 모드의 기본값으로 (= 보이는 상태가 찍힐 배경)',
        re.search(r"modeSel\.addEventListener\('change',\s*syncShotBg\)", wc) is not None
        and re.search(r'shotCb\.checked\s*=\s*shotTransparentDefault\(', wc) is not None)

    if not shutil.which('node'):
        chk('V3 node 필요 (캡처 함수를 실제로 돌린다)', False, 'node 미설치')
        return
    src, miss = fns(js, ('shotTransparentDefault', 'captureHighRes', 'captureScreenshotPNG'))
    m_op = re.search(r'const SHOT_OPAQUE_MODES = \[[^\]]*\];', js)
    if not chk('V3 viewer3d.js 에서 캡처 함수 · 모드 목록을 잘라 냈다', not miss and m_op is not None,
               f'없음 {miss + ([] if m_op else ["SHOT_OPAQUE_MODES"])}'):
        return
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    modes = sorted(set(re.findall(r'<option value="([^"]+)"', ''.join(re.findall(r'<select id="view-mode".*?</select>', bc, re.S)))))
    script = (V_SHIM + js_const(js, 'COL') + '\n' + m_op.group(0) + '\n' + src + '\n'
              + 'const MODES = ' + json.dumps(modes) + ';\n' + V_RUN)
    res = run_node(script)
    if not chk('V3b node 실행', res is not None):
        return
    bad = [(m, t) for m, t in res['defaults'] if t != (m not in OPAQUE_MODES)]
    chk(f'V4 모드별 기본값 = 옛 동작 그대로 (조작판 모드 {len(modes)} 개 — 투명 · 장 모드 je_field · ji_field · je 만 뷰어 배경)',
        len(modes) >= 20 and OPAQUE_MODES <= set(modes) and not bad, repr(bad)[:200])
    t = res['true']
    chk('V5 ☑ 투명 = 6× 캡처 렌더가 지우기 알파 0 · scene.background 없음 · 장식 숨김 → PNG 알파 0',
        t['err'] is None and len(t['snap']) == 1 and t['snap'][0]['ca'] == 0 and t['snap'][0]['bg'] is None
        and t['snap'][0]['deco'] == 0 and str(t['url']).endswith('alpha=0'), repr(t)[:240])
    f = res['false']
    chk('V6 ☐ 꺼짐 = 뷰어 배경색 (COL.BG) 불투명 (옛 장 모드 분기와 같다)',
        f['err'] is None and len(f['snap']) == 1 and f['snap'][0]['ca'] == 1 and f['snap'][0]['bg'] == res['bg']
        and str(f['url']).endswith('alpha=1'), repr(f)[:240])
    for k, d in (('투명', t), ('꺼짐', f)):
        a = d['after']
        chk(f'V7 [{k}] 찍은 뒤 복구 — 지우기 색 · 알파 · 픽셀 비율 · 크기 · 배경 · 장식 (화면 그대로)',
            a == {'cc': res['bg'], 'ca': 1, 'pr': 2, 'w': 500, 'h': 400, 'bg': None, 'vis': [True, False, True]}, repr(a))


def main():
    tmp = tempfile.mkdtemp(prefix='png_clear_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab'),
                     ('WEBAPP_MIXER_RUNS', 'mixer_runs')):
            os.environ[k] = os.path.join(tmp, v)
        os.makedirs(os.environ['WEBAPP_MIXER_RUNS'])
        sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        import app as A
        r = A.app.test_client().get('/mixer')
        chk('M0 /mixer 200', r.status_code == 200, str(r.status_code))
        section_mixer(r.get_data(as_text=True))
        section_viewer()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    print(f'{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())

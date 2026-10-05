#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 "침대 보기" 탭 (/mixer · /api/mixer/*) 회귀 — 경로 거부 · 맹검 잠금 · 덤프 읽기 · 단면 선택.

  python3 webapp/test_mixer_bed_view.py

★ 반례를 먼저 적었다 (1저자 비준 2026-09-30 — *"시험: 경로 거부, 덤프 읽기, 단면 선택을 반례부터"*).
★ 실제 런 폴더를 건드리지 않는다 — 임시 루트에 가짜 런을 만들고 `WEBAPP_MIXER_RUNS` 로 가리킨다.
"""
import base64
import json
import os
import shutil
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


COLS = 'id type x y z vx vy vz fx fy fz radius'
#  (id, type, x, y, z, r) — x 는 단면 경계 반례를 담는다 (±0.001 = 경계 · 0.0010000001 = 바로 밖)
ROWS = [(1, 1, 0.0, 0.004, -0.006, 0.0009),
        (2, 1, 0.0010000001, -0.003, -0.007, 0.0009),
        (3, 1, -0.002, 0.001, -0.008, 0.0009),
        (4, 2, 0.001, 0.002, -0.009, 0.0003),
        (5, 2, -0.001, -0.002, -0.010, 0.0003),
        (6, 3, 0.0009999999, 0.0, -0.011, 0.0001),
        (7, 3, -0.0010000001, 0.0005, -0.0105, 0.0001),
        (8, 3, 0.0024, -0.0005, -0.0095, 0.0001)]
DT, PERIOD, SCALE = 1e-3, 0.5, 0.0262
ROT0 = 1 + 100 + 100                                   # run 1 · run 100 · run 100 → 회전 시작 step


#  ⑰d GIF 색 — 페이지의 인코더 (lzwBlocks … gifEnd) 를 **그대로 잘라** node 로 돌리고 Pillow (독립 디코더) 로 푼다.
#  반례 (1저자 09-30 밤 *"gif 하면 흑백으로 나온다"*): 층상 런은 첫 프레임 (정착 ①) 에 SE 가 없다 — 회색 AM 둘 (#5b5b5b · #8f8f8f) 뿐.
#  옛 인코더는 팔레트를 첫 프레임에서만 뽑아 뒤 프레임의 SE 베이지 (#c9b88a) 를 가장 가까운 회색으로 칠했다.
GIF_HARNESS = r"""
const fs = require('fs'), W = 48, H = 32;
function frame(withSE) {
  const f = new Uint8ClampedArray(W * H * 4);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const s = 0.5 + 0.5 * y / (H - 1);                                  // 3D 음영처럼 밝기 사다리
    let c = [251, 251, 248];                                            // 배경 #fbfbf8
    if (x < 16) c = [0x5b, 0x5b, 0x5b].map(v => Math.round(v * s));    // AM_P
    else if (x < 32) c = [0x8f, 0x8f, 0x8f].map(v => Math.round(v * s)); // AM_S
    else if (withSE) c = [0xc9, 0xb8, 0x8a].map(v => Math.round(v * s)); // SE (둘째 프레임에만)
    const p = 4 * (y * W + x); f[p] = c[0]; f[p + 1] = c[1]; f[p + 2] = c[2]; f[p + 3] = 255;
  }
  return f;
}
const f0 = frame(false), f1 = frame(true), g = gifBegin(f0, W, H);
gifAdd(g, f0, 10); gifAdd(g, f1, 10);
const parts = gifEnd(g), out = Buffer.alloc(parts.reduce((a, c) => a + c.length, 0));
let o = 0; for (const c of parts) { Buffer.from(c.buffer, c.byteOffset, c.length).copy(out, o); o += c.length; }
fs.writeFileSync(process.argv[2], out);
"""


def gif_encoder_src(html):
    """페이지에서 GIF 인코더 부분 (function lzwBlocks( … function gifEnd( 가 있는 줄 끝) 을 그대로 잘라 낸다.  못 찾으면 None."""
    a = html.find('  function lzwBlocks(')
    b = html.find('function gifEnd(', a if a >= 0 else 0)
    if a < 0 or b < 0:
        return None
    e = html.find('\n', b)
    return html[a:e if e >= 0 else len(html)]


def gif_color_check(html, tmp):
    """→ (None = node 없음) 또는 (ok, 설명).  둘째 프레임의 SE 칸이 베이지로 풀리고 (±8) · 두 프레임의 회색이 그대로인가."""
    import subprocess
    node = shutil.which('node')
    if node is None:
        return None
    src = gif_encoder_src(html)
    if src is None:
        return False, '인코더 (lzwBlocks … gifEnd) 를 페이지에서 못 찾았다'
    js, gif = os.path.join(tmp, 'gif_harness.js'), os.path.join(tmp, 'gif_out.gif')
    with open(js, 'w', encoding='utf-8') as fh:
        fh.write(src + '\n' + GIF_HARNESS)
    r = subprocess.run([node, js, gif], capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not os.path.isfile(gif):
        return False, f'node 실패 rc {r.returncode}: {r.stderr[-300:]}'
    from PIL import Image
    im = Image.open(gif)
    n = getattr(im, 'n_frames', 1)
    im.seek(0)
    a0 = np.asarray(im.convert('RGB'), dtype=int)
    im.seek(1)
    a1 = np.asarray(im.convert('RGB'), dtype=int)
    se = a1[:, 32:]                                                     # 둘째 프레임 SE 칸
    want = np.array([0xc9, 0xb8, 0x8a])
    top = np.abs(se[-1] - want).max()                                   # 맨 아래 줄 = 밝기 1.0 = 상 색 그대로
    hue = float((se[..., 0] - se[..., 2]).mean())                       # 베이지는 R − B ≈ 63 (회색이면 0)
    gray_ok = all(np.abs(a[:, :16][-1] - 0x5b).max() <= 8 and np.abs(a[:, 16:32][-1] - 0x8f).max() <= 8 for a in (a0, a1))
    ok = n == 2 and top <= 8 and hue > 40 and gray_ok
    return ok, (f'프레임 {n} · SE 맨 아래 줄 최대 편차 {top} (≤ 8) · SE 평균 R−B {hue:.1f} (> 40) · 회색 둘 보존 {gray_ok} · '
                f'SE 픽셀 예 {tuple(int(v) for v in se[-1, 0])}')


#  ⑰e 투명 배경 GIF (1저자 10-02 *"투명배경 gif 버전도"*) — 같은 인코더를 clear=true 로 돌린다.
#  배경 (알파 0) = 프레임마다 투명 색 하나 (index 0) · 처분 방식 2 (배경으로 되돌림) — 1 이면 앞 프레임 그림이 투명 자리에 남는다 (잔상).
GIF_HARNESS_CLEAR = r"""
const fs = require('fs'), W = 48, H = 32;
function frame(left) {
  const f = new Uint8ClampedArray(W * H * 4);                         // 알파 0 = 투명 배경
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const on = left ? x < 16 : x >= 32, p = 4 * (y * W + x);
    if (on) { f[p] = 0xc9; f[p + 1] = 0xb8; f[p + 2] = 0x8a; f[p + 3] = 255; }   // SE 베이지 덩어리 (프레임마다 자리가 바뀐다)
  }
  return f;
}
const f0 = frame(true), f1 = frame(false), g = gifBegin(f0, W, H, true);
gifAdd(g, f0, 10, true); gifAdd(g, f1, 10, true);
const parts = gifEnd(g), out = Buffer.alloc(parts.reduce((a, c) => a + c.length, 0));
let o = 0; for (const c of parts) { Buffer.from(c.buffer, c.byteOffset, c.length).copy(out, o); o += c.length; }
fs.writeFileSync(process.argv[2], out);
"""


def gif_clear_check(html, tmp):
    """→ (None = node 없음) 또는 (ok, 설명).  투명 GIF 두 프레임: 배경은 알파 0 · 덩어리는 불투명 베이지 · 둘째 프레임에 첫 덩어리 잔상 없음."""
    import subprocess
    node = shutil.which('node')
    if node is None:
        return None
    src = gif_encoder_src(html)
    if src is None:
        return False, '인코더 (lzwBlocks … gifEnd) 를 페이지에서 못 찾았다'
    js, gif = os.path.join(tmp, 'gif_clear.js'), os.path.join(tmp, 'gif_clear.gif')
    with open(js, 'w', encoding='utf-8') as fh:
        fh.write(src + '\n' + GIF_HARNESS_CLEAR)
    r = subprocess.run([node, js, gif], capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not os.path.isfile(gif):
        return False, f'node 실패 rc {r.returncode}: {r.stderr[-300:]}'
    from PIL import Image
    im = Image.open(gif)
    n = getattr(im, 'n_frames', 1)
    im.seek(0)
    a0 = np.asarray(im.convert('RGBA'), dtype=int)
    tr0 = im.info.get('transparency')
    im.seek(1)
    a1 = np.asarray(im.convert('RGBA'), dtype=int)
    want = np.array([0xc9, 0xb8, 0x8a])
    obj0 = a0[:, :16]; obj1 = a1[:, 32:]
    ok_obj = (obj0[..., 3] == 255).all() and (obj1[..., 3] == 255).all() and np.abs(obj0[..., :3] - want).max() <= 8 \
        and np.abs(obj1[..., :3] - want).max() <= 8
    bg0 = int(a0[:, 16:][..., 3].max()); bg1 = int(a1[:, :32][..., 3].max())     # 둘째 프레임의 왼쪽 = 첫 덩어리 자리 (잔상이면 알파 > 0)
    ok = n == 2 and tr0 is not None and ok_obj and bg0 == 0 and bg1 == 0
    return ok, f'프레임 {n} · 투명 색 {tr0} · 덩어리 불투명 · 베이지 {bool(ok_obj)} · 배경 알파 최대 {bg0} / 둘째 프레임 첫 자리 {bg1} (둘 다 0)'


#  ⑰f GIF 캡션 — 런 (샘플) 이름 없이 (1저자 10-02 *"무슨 샘플인지 이름은 빼서"*) · PNG 캡션은 그대로 (런 이름 포함)
CAPTION_HARNESS = r"""
const S = { data: { meta: { run: 'LC_s32452843', step: 317331, time_s: 0.224, rev: null, phase: 'fill', view: '3d', types_present: {}, selection: null } }, hidden: {} };
const nf = new Intl.NumberFormat('ko-KR'); function mm(v) { return (v * 1e3).toFixed(2) + ' mm'; }
process.stdout.write(JSON.stringify({ png: captionText(), gif: captionText(false) }));
"""


def caption_check(html, tmp):
    import subprocess, json as _json
    node = shutil.which('node')
    if node is None:
        return None
    a = html.find('  function captionText(')
    b = html.find('\n  }\n', a) if a >= 0 else -1
    if a < 0 or b < 0:
        return False, 'captionText 를 페이지에서 못 찾았다'
    js = os.path.join(tmp, 'caption.js')
    with open(js, 'w', encoding='utf-8') as fh:
        fh.write(html[a:b + 4] + '\n' + CAPTION_HARNESS)
    r = subprocess.run([node, js], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return False, f'node 실패 rc {r.returncode}: {r.stderr[-300:]}'
    o = _json.loads(r.stdout)
    ok = 'LC_s32452843' in o['png'] and 'LC_s32452843' not in o['gif'] and o['gif'].startswith('step ')
    return ok, f"PNG 캡션 '{o['png'][:40]}…' · GIF 캡션 '{o['gif'][:40]}…'"


#  ⑰i 3D PNG 잘림 (1저자 10-02 *"png 딸때 잘려서 나온다"*) — 기본 시점에서 드럼이 화면 높이의 93–99 % 라 시점을 기울이면 테가 틀 밖으로
#     나가고 PNG 는 그 틀을 그대로 찍었다 (헤드리스 재현: 위 · 아래 가장자리 닿음).  ⇒ 내보낼 때 드럼 윤곽 (두 테) 을 화면 px 로 투영해
#     틀에 걸리면 그만큼 틀을 넓힌다 (시점 · 배율은 화면 그대로) · 크게 당긴 시점 (1.6 배 넘게 넓혀야 함) · 카메라 뒤 점은 화면 그대로.
#     exportPad (순수 함수) 를 페이지에서 그대로 잘라 node 로 돌린다.
PAD_HARNESS = r"""
const W = 1000, H = 720;
process.stdout.write(JSON.stringify({
  inside: exportPad([[200, 100], [800, 620]], W, H),
  cut: exportPad([[100, 5], [900, 760]], W, H),
  zoom: exportPad([[-1500, -900], [2500, 1700]], W, H),
  behind: exportPad(null, W, H),
}));
"""


def pad_check(html, tmp):
    """→ (None = node 없음) 또는 (ok, 설명).  여백 m = 3 % · max(W, H) = 30 px."""
    import subprocess, json as _json
    node = shutil.which('node')
    if node is None:
        return None
    a = html.find('  function exportPad(')
    b = html.find('\n  }\n', a) if a >= 0 else -1
    if a < 0 or b < 0:
        return False, 'exportPad 를 페이지에서 못 찾았다'
    js = os.path.join(tmp, 'pad.js')
    with open(js, 'w', encoding='utf-8') as fh:
        fh.write(html[a:b + 4] + '\n' + PAD_HARNESS)
    r = subprocess.run([node, js], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return False, f'node 실패 rc {r.returncode}: {r.stderr[-300:]}'
    o = _json.loads(r.stdout)
    zero = lambda d: all(d.get(k) == 0 for k in 'lrtb')
    ok = (o['inside']['fit'] is False and zero(o['inside'])
          and o['cut']['fit'] is True and (o['cut']['l'], o['cut']['r'], o['cut']['t'], o['cut']['b']) == (0, 0, 25, 70)
          and o['zoom']['fit'] is False and o['zoom']['why'] == 'zoom' and zero(o['zoom'])
          and o['behind']['fit'] is False and o['behind']['why'] == 'behind' and zero(o['behind']))
    return ok, (f"틀 안 = 그대로 {zero(o['inside'])} · 위 5 px · 아래 40 px 넘침 → 여백 위 {o['cut'].get('t')} 아래 {o['cut'].get('b')} (기대 25 · 70) · "
                f"크게 당김 = {o['zoom'].get('why')} · 카메라 뒤 = {o['behind'].get('why')}")


def frame_txt(step, rows=ROWS, n_hdr=None, step_hdr=None):
    L = ['ITEM: TIMESTEP', str(step if step_hdr is None else step_hdr), 'ITEM: NUMBER OF ATOMS',
         str(len(rows) if n_hdr is None else n_hdr), 'ITEM: BOX BOUNDS mm mm mm', '-0.02 0.02', '-0.02 0.02',
         '-0.02 0.02', 'ITEM: ATOMS ' + COLS]
    for (i, t, x, y, z, r) in rows:
        L.append(f'{i} {t} {x!r} {y!r} {z!r} 0 0 0 0 0 0 {r!r}')
    return '\n'.join(L) + '\n'


DECK = f"""timestep        {DT:g}
fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant 4750 radius constant 0.0009
fix pt2 all particletemplate/sphere 11887 atom_type 2 density constant 4750 radius constant 0.0003
fix pt3 all particletemplate/sphere 13901 atom_type 3 density constant 1900 radius constant 0.0001
fix Drum  all mesh/surface file Drum.stl  type 4 scale {SCALE:g}
fix Front all mesh/surface file Front.stl type 4 scale {SCALE:g}
run 1
dump dmp all custom 100 post/mix_*.liggghts id type x y z vx vy vz fx fy fz radius
run 100
unfix ins
run 100
write_restart restart/settled.bin
fix mvD all move/mesh mesh Drum  rotate origin 0 0 0 axis 1. 0. 0. period {PERIOD:g}
fix mvF all move/mesh mesh Front rotate origin 0 0 0 axis 1. 0. 0. period {PERIOD:g}
run 1000
"""


def stl_txt(n=12, r=0.5, hx=0.1):
    """반경 r · x ∈ [−hx, hx] 의 n 각 원통 옆면 (ASCII STL — 튜토리얼 Drum.stl 과 같은 모양)."""
    th = np.linspace(0, 2 * np.pi, n + 1)
    L = ['solid t']
    for k in range(n):
        a, b = th[k], th[k + 1]
        ca, sa, cb, sb = (float(v) for v in (np.cos(a), np.sin(a), np.cos(b), np.sin(b)))   # np.float64 repr 금지
        p = [(-hx, r * ca, r * sa), (hx, r * ca, r * sa), (hx, r * cb, r * sb), (-hx, r * cb, r * sb)]
        for tri in ((p[0], p[1], p[2]), (p[0], p[2], p[3])):
            L += ['facet normal 0 0 0', 'outer loop'] + [f'vertex {v[0]!r} {v[1]!r} {v[2]!r}' for v in tri] \
                + ['endloop', 'endfacet']
    return '\n'.join(L + ['endsolid t']) + '\n'


def mkrun(root, name, steps=(1, 201, 1001), deck=True, drum=True, frames=None, r_container=None):
    d = os.path.join(root, name)
    os.makedirs(os.path.join(d, 'post'))
    if r_container is not None:                           # gen_all.sh 가 런 옆에 적는 드럼 반경 (m)
        open(os.path.join(d, 'r_container'), 'w').write(f'{r_container:.6f}\n')
    if deck:
        open(os.path.join(d, 'in.mixer'), 'w').write(DECK)
    if drum:
        open(os.path.join(d, 'Drum.stl'), 'w').write(stl_txt())
    for s in steps:
        open(os.path.join(d, 'post', f'mix_{s}.liggghts'), 'w').write(frame_txt(s))
    for fn, txt in (frames or {}).items():
        open(os.path.join(d, 'post', fn), 'w').write(txt)
    return d


def snapshot(root):
    out = []
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            p = os.path.join(dp, f)
            st = os.lstat(p)
            out.append((os.path.relpath(p, root), st.st_size, st.st_mtime_ns))
        dn.sort()
    return sorted(out)


def b64f(s):
    return np.frombuffer(base64.b64decode(s), dtype='<f4')


def main():
    tmp = tempfile.mkdtemp(prefix='mxbed_')
    root_a = os.path.join(tmp, 'runsA')
    root_b = os.path.join(tmp, 'runsB')
    outside = os.path.join(tmp, 'outside')
    os.makedirs(root_a); os.makedirs(root_b); os.makedirs(os.path.join(outside, 'post'))
    open(os.path.join(outside, 'post', 'mix_1.liggghts'), 'w').write(frame_txt(1))
    open(os.path.join(outside, 'secret.liggghts'), 'w').write(frame_txt(5))
    L0 = mkrun(root_a, 'L0_s32452843', frames={'notes.txt': 'x', 'mix_abc.liggghts': 'x', 'mix_7.dump': 'x'},
               r_container=0.5 * SCALE)
    mkrun(root_a, 'LB3_s15', steps=(1,), r_container=0.5 * SCALE * 1.01)                  # 1 % 어긋난 기록
    for nm in ('LH_s32452843', 'LC_ref_r2_s32452843', 'E0_ref_dthalf_s32452843', 'npprobe20_E0_ref_s32452843',
               'LC_s32452843_old', 'LH_ref_r2_s32452843', 'LHx30_ref_r2_s32452843', 'LH_ref_s32452843',
               'LH_ref_r2_s15485863', 'LHx10_ref_r2_s49979687', 'LU212_ref_r2_s32452843', 'LU637_ref_r2_s32452843'):
        mkrun(root_a, nm)
    for nm in ('bad name', '.hidden', 'L0_s1-copy'):
        mkrun(root_a, nm)
    mkrun(root_a, 'LA_s11', steps=(1,), frames={
        'mix_2.liggghts': frame_txt(2, n_hdr=9),                                            # 머리 원자 수 ≠ 행 수
        'mix_3.liggghts': frame_txt(3, rows=[(1, 1, float('nan'), 0.0, 0.0, 0.001)]),      # 비유한 좌표
        'mix_4.liggghts': frame_txt(4, step_hdr=999)})                                       # 머리 step ≠ 파일명
    mkrun(root_a, 'LB1_s12', deck=False, drum=False)                                         # 덱 · 드럼 없음
    mkrun(root_a, 'LB2_s13', drum=False)                                                     # 드럼만 없음
    os.symlink(outside, os.path.join(root_a, 'LB3_s14'))                                     # 런 디렉터리 탈출
    os.symlink(os.path.join(outside, 'secret.liggghts'), os.path.join(L0, 'post', 'mix_5.liggghts'))  # 프레임 탈출
    mkrun(root_b, 'LC_s67867967', steps=(1,))
    os.environ['WEBAPP_MIXER_RUNS'] = os.pathsep.join([root_a, root_b, os.path.join(tmp, 'nope')])

    import app as webapp
    import mixer_bed
    c = webapp.app.test_client()

    # ── ① 페이지 ──
    r = c.get('/mixer')
    html = r.get_data(as_text=True)
    chk('① /mixer 200 · 탭 둘 (개발 이력 · 침대 보기)', r.status_code == 200 and '개발 이력' in html and '침대 보기' in html)
    chk('①b 표지 "보기 전용 — 판정은 3D 칸 M 으로만" 이 화면에 있다', '보기 전용 — 판정은 3D 칸 M 으로만' in html)
    chk('①c 개발 이력 카드는 그대로 뜬다 (회귀)', 'mx-timeline' in html and 'mx-toggle' in html)

    before = snapshot(tmp)

    # ── ② 목록 ──
    j = c.get('/api/mixer/runs').get_json()
    runs = {(x['root'], x['run']): x for x in j['runs']}
    chk('② 목록 ok · 루트 셋 (없는 루트는 exists False)',
        j['ok'] and [x['exists'] for x in j['roots']] == [True, True, False])
    l0 = runs.get((0, 'L0_s32452843'), {})
    chk('②b 층상 캠페인 L0 는 열림 · 프레임은 **숫자순** [1, 201, 1001] (사전순이면 1001 이 201 앞)',
        l0.get('allowed') is True and l0.get('steps') == [1, 201, 1001])
    chk('②c 이름 규약 밖 파일 (notes.txt · mix_abc · mix_7.dump) · 탈출 링크 (mix_5) 는 프레임이 아니다',
        l0.get('n_frames') == 3)
    chk('②d 두 번째 루트의 런도 잡힌다', runs.get((1, 'LC_s67867967'), {}).get('allowed') is True)

    # ── ③ 맹검 잠금 ──
    #  10-04 (1저자 *"믹서 lh 도 웹앱에서 gif 등으로 볼 수 있게"*): DEV seed 1 의 2 바퀴 런은 M 열람 기록이 있어 열린다 —
    #  정지된 09-28 LH (M · 겹침 미열람) · 후행 8 바퀴 (`LH_ref_s32452843`) · holdout 시드 · 다른 개발 시드 · 기록 없는 E0 는 그대로 잠금.
    #  10-05 — 개발 탐색 dev-u 의 LU212 · LU637 (등록 §12 · M 열람 전) 도 잠금 (⑭e 가 정책 쪽을 본다).
    locked = ('LH_s32452843', 'E0_ref_dthalf_s32452843', 'npprobe20_E0_ref_s32452843', 'LC_s32452843_old',
              'LH_ref_s32452843', 'LH_ref_r2_s15485863', 'LHx10_ref_r2_s49979687', 'LU212_ref_r2_s32452843', 'LU637_ref_r2_s32452843')
    chk('③ 고-Bo · 강성 축 · NP 프로브 · 패턴 밖 이름은 잠긴다 (프레임 목록도 안 준다)',
        all(runs.get((0, n), {}).get('allowed') is False and not runs[(0, n)].get('steps') for n in locked))
    chk('③b 잠긴 런에는 사유 문자열이 있다 (맹검)', all('맹검' in runs.get((0, n), {}).get('reason', '') for n in locked))
    rr = c.get('/api/mixer/frame?root=0&run=LH_s32452843&step=1&view=3d')
    chk('③c 잠긴 런의 프레임 요청은 403', rr.status_code == 403 and rr.get_json().get('ok') is False)
    dev = {'LC_ref_r2_s32452843': 'mixer_highbo_devrot_prelim_20261002', 'LH_ref_r2_s32452843': 'mixer_highbo_devrot_prelim_20261002',
           'LHx30_ref_r2_s32452843': 'mixer_highbo_devbo_prelim_20261003'}
    chk('③d DEV seed 1 의 2 바퀴 런 (M 열람 기록 있음) 은 열린다 · 근거 = 그 열람 기록 폴더 + "판정 미사용" 표지',
        all(runs.get((0, n), {}).get('allowed') is True and runs[(0, n)].get('steps') == [1, 201, 1001]
            and rec in runs[(0, n)].get('basis', '') and '판정 미사용' in runs[(0, n)].get('basis', '')
            for n, rec in dev.items()))
    rd = c.get('/api/mixer/frame?root=0&run=LHx30_ref_r2_s32452843&step=201&view=3d')
    chk('③e 열린 DEV 런 (점착 ×30) 의 프레임 요청은 200 (GIF · PNG 재료)',
        rd.status_code == 200 and rd.get_json().get('ok') is True and rd.get_json().get('n_total') == len(ROWS))

    # ── ④ 이름 규약 밖 디렉터리 ──
    chk('④ 규약 밖 디렉터리 (공백 · 점 · 하이픈) 는 목록에 없다',
        not any(n in ('bad name', '.hidden', 'L0_s1-copy') for (_, n) in runs))

    # ── ⑤ 경로 거부 ──
    bad = [('0', '../L0_s32452843', '1'), ('0', 'L0_s32452843/..', '1'), ('0', '/etc', '1'), ('0', '..', '1'),
           ('0', '', '1'), ('0', 'L0_s32452843%2F..', '1'), ('0', 'L0_s32452843\x00', '1'),
           ('-1', 'L0_s32452843', '1'), ('9', 'L0_s32452843', '1'), ('x', 'L0_s32452843', '1'),
           ('', 'L0_s32452843', '1'), ('0', 'L0_s32452843', '1e3'), ('0', 'L0_s32452843', '-1'),
           ('0', 'L0_s32452843', '../1'), ('0', 'L0_s32452843', ''), ('2', 'L0_s32452843', '1')]
    codes = []
    for (ro, ru, st) in bad:
        resp = c.get('/api/mixer/frame', query_string={'root': ro, 'run': ru, 'step': st, 'view': '3d'})
        codes.append((resp.status_code, (resp.get_json() or {}).get('ok')))
    chk('⑤ 경로 탈출 · 형식 밖 입력 16 종 전부 거부 (4xx · ok False)',
        all(400 <= s < 500 and o is False for s, o in codes))
    resp = c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=999&view=3d')
    chk('⑤b 목록에 없는 step 은 404', resp.status_code == 404)

    # ── ⑥ 심볼릭 링크 탈출 ──
    chk('⑥ 루트 밖을 가리키는 런 링크 (LB3_s14) 는 목록에 없다', (0, 'LB3_s14') not in runs)
    s6 = [c.get(f'/api/mixer/frame?root=0&run={ru}&step={st}&view=3d').status_code
          for ru, st in (('LB3_s14', 1), ('L0_s32452843', 5))]
    chk('⑥b 링크로 루트 밖 파일을 읽지 않는다 (런 링크 · 프레임 링크 둘 다 4xx)', all(400 <= s < 500 for s in s6))

    # ── ⑦ 덤프 읽기 ──
    fj = c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=1001&view=3d').get_json()
    D = {k: b64f(fj['data'][k]) for k in ('x', 'y', 'z', 'r')}
    T = np.frombuffer(base64.b64decode(fj['data']['type']), dtype=np.uint8)
    want = np.array(ROWS, dtype=float)
    chk('⑦ 3D: 행 수 · 좌표 · 반경 · 타입이 덤프와 같다 (float32 반올림 안)',
        fj['n_total'] == len(ROWS) and fj['n_shown'] == len(ROWS)
        and np.allclose(D['x'], want[:, 2], rtol=0, atol=1e-9) and np.allclose(D['y'], want[:, 3], atol=1e-9)
        and np.allclose(D['z'], want[:, 4], atol=1e-9) and np.allclose(D['r'], want[:, 5], atol=1e-9)
        and T.tolist() == [int(t) for t in want[:, 1]])
    import viz_mixer_bed
    pal = {viz_mixer_bed.TYPE_LAB[k]: viz_mixer_bed.TYPE_COL[k] for k in viz_mixer_bed.TYPE_COL}
    tp = fj['types_present']
    chk('⑦b 상 이름은 덱의 템플릿 시드에서 (AM_P · AM_S · SE) · 색은 viz_mixer_bed 팔레트 그대로 · 개수',
        {k: (v['name'], v['color'], v['n_total']) for k, v in tp.items()}
        == {'1': ('AM_P', pal['AM_P'], 3), '2': ('AM_S', pal['AM_S'], 2), '3': ('SE', pal['SE'], 3)})

    # ── ⑧ 깨진 프레임은 그리지 않는다 ──
    e2 = c.get('/api/mixer/frame?root=0&run=LA_s11&step=2&view=3d')
    e3 = c.get('/api/mixer/frame?root=0&run=LA_s11&step=3&view=3d')
    e4 = c.get('/api/mixer/frame?root=0&run=LA_s11&step=4&view=3d')
    chk('⑧ 머리 원자 수 ≠ 행 수 → 422 + 검사기 문장',
        e2.status_code == 422 and any('원자 수' in p for p in e2.get_json().get('problems', [])))
    chk('⑧b 비유한 좌표 → 422', e3.status_code == 422 and any('비유한' in p for p in e3.get_json().get('problems', [])))
    chk('⑧c 머리 step ≠ 파일명 step → 422', e4.status_code == 422)

    # ── ⑨ 단면 선택 ──
    sj = c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=1001&view=slab&x0=0&t=0.002').get_json()
    ids_in = sorted(int(i) for (i, _, x, *_r) in ROWS if -0.001 <= x <= 0.001)
    xs = b64f(sj['data']['x'])
    chk('⑨ 단면 = 중심이 x₀ ± t/2 **닫힌 구간** 안 (경계 ±0.001 포함 · 0.0010000001 제외 · 0.0009999999 포함)',
        sj['ok'] and sj['n_shown'] == len(ids_in) == 4 and sj['n_total'] == len(ROWS)
        and np.all(np.abs(xs) <= 0.0010000001))
    sj2 = c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=1001&view=slab&x0=0.0015&t=0.002').get_json()
    chk('⑨b x₀ 를 옮기면 조각이 옮겨 간다 (0.0005 ≤ x ≤ 0.0025 → 4 개)', sj2['n_shown'] == 4)
    tp9 = sj['types_present']
    chk('⑨c 상별 n_shown 합 = n_shown · n_total 은 프레임 전체',
        sum(v['n_shown'] for v in tp9.values()) == sj['n_shown'] and sum(v['n_total'] for v in tp9.values()) == 8)
    badq = ['x0=0&t=0', 'x0=0&t=-1', 'x0=0&t=nan', 'x0=0&t=inf', 'x0=nan&t=0.001', 'x0=abc&t=0.001',
            'x0=0', 't=0.001', 'x0=1e999&t=0.001']
    s9 = [c.get(f'/api/mixer/frame?root=0&run=L0_s32452843&step=1001&view=slab&{q}').status_code for q in badq]
    chk('⑨d 단면 인자 반례 9 종 (0 · 음수 · nan · inf · 수 아님 · 빠짐 · 넘침) 전부 400', all(s == 400 for s in s9))
    chk('⑨e 모르는 view 는 400', c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=1001&view=m').status_code == 400)

    # ── ⑩ 투영 ──
    pj = c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=1001&view=proj').get_json()
    chk('⑩ 투영은 전 입자 (n_shown = n_total)', pj['ok'] and pj['n_shown'] == pj['n_total'] == len(ROWS))

    # ── ⑫ 덱 정보 (표시용) ──
    dk = l0.get('deck') or {}
    drum = dk.get('drum') or {}
    chk('⑫ 드럼 = Drum.stl 꼭짓점 × scale (R = 0.5·S · x ∈ ±0.1·S)',
        abs(drum.get('R', 0) - 0.5 * SCALE) < 1e-12 and abs(drum.get('x_min', 0) + 0.1 * SCALE) < 1e-12
        and abs(drum.get('x_max', 0) - 0.1 * SCALE) < 1e-12)
    chk('⑫b dt · 주기 · 회전 시작 step (run 합) 을 덱 문자열에서',
        dk.get('dt') == DT and dk.get('period') == PERIOD and dk.get('rot_start_step') == ROT0)
    f1 = c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=1&view=proj').get_json()
    chk('⑫c 바퀴 = (step − 회전 시작)·dt/주기 — 1001 → 1.6 · 회전 전 (step 1) 은 None + 정착 구간',
        abs((fj.get('rev') or 0) - (1001 - ROT0) * DT / PERIOD) < 1e-12 and fj.get('phase') == 'rotation'
        and f1.get('rev') is None and f1.get('phase') == 'fill')
    b2 = runs.get((0, 'LB2_s13'), {})
    fb2 = c.get('/api/mixer/frame?root=0&run=LB2_s13&step=1&view=3d')
    chk('⑫d Drum.stl 없음 → 드럼 None + 사유 (짐작하지 않는다) · 프레임은 그대로 뜬다',
        b2.get('allowed') is True and (b2.get('deck') or {}).get('drum', 0) is None
        and any('Drum.stl' in n for n in (b2.get('deck') or {}).get('notes', [])) and fb2.status_code == 200)

    chk('⑫e 런 옆 r_container (생성기 기록) 는 드럼 반경과 대조만 한다 — 같으면 사유 없음',
        abs((drum.get('r_container') or 0) - float(f'{0.5 * SCALE:.6f}')) < 1e-12
        and not any('r_container' in n for n in dk.get('notes', [])))
    b5 = runs.get((0, 'LB3_s15'), {})
    chk('⑫f r_container 가 Drum.stl 반경과 0.1 % 넘게 다르면 사유를 적는다 (그림은 STL 기준 그대로)',
        any('r_container' in n for n in (b5.get('deck') or {}).get('notes', []))
        and abs(((b5.get('deck') or {}).get('drum') or {}).get('R', 0) - 0.5 * SCALE) < 1e-12)

    # ── ⑬ 상 이름 못 읽음 ──
    fb1 = c.get('/api/mixer/frame?root=0&run=LB1_s12&step=1&view=3d').get_json()
    chk('⑬ 덱 없음 → 상 이름은 "type N" + types_named False (짐작하지 않는다)',
        fb1.get('ok') and fb1.get('types_named') is False
        and (fb1.get('types_present') or {}).get('1', {}).get('name') == 'type 1'
        and fb1.get('rev') is None)

    # ── ⑭ 정책 파일 ──
    pol = mixer_bed.load_policy()
    chk('⑭ 선적 정책: 항목마다 basis · since · 패턴 컴파일', pol['ok'] and pol['allow']
        and all(a['basis'].strip() and a['since'].strip() for a in pol['allow']))
    names_ok = ['E0_s32452843', 'L0_s32452843', 'LA_s49979687', 'LB1_s32452843', 'LB3_s32452843', 'LC_s67867967',
                #  DEV seed 1 · 2 바퀴 · M 열람 (dev-rot 10-02 · dev-bo 10-03) + 두 판독의 공통 기준 E0
                'LC_ref_r2_s32452843', 'LH_ref_r2_s32452843', 'LHx10_ref_r2_s32452843', 'LHx30_ref_r2_s32452843',
                'E0_ref_s32452843']
    names_lock = ['LH_s32452843', 'LH_s49979687', 'LH_s67867967',          # 09-28 정지 LH (M · 겹침 미열람 · 재발사 맹검)
                  'LC_ref_s32452843', 'LH_ref_s32452843', 'LC_ref2_s32452843', 'LH_ref2_s32452843',   # 후행 8 바퀴 (r₁ · t₁ 등록)
                  'LH_ref_dt2_s32452843', 'E0_ref2_s32452843', 'E0_ref_dthalf_s32452843',            # 기록 반입 없는 DEV E0
                  'E0_ref_s49979687', 'E0_ref_s67867967',
                  'E0_ref_s15485863', 'LC_ref_s15485863', 'LH_ref_s86028121', 'LH_soft_s104395301',   # 확인 (holdout) 블록
                  'LH_ref_r2_s15485863', 'LHx10_ref_r2_s49979687', 'LHx10_ref_s32452843',
                  'xLHx10_ref_r2_s32452843', 'LHx10_ref_r2_s32452843_b', 'LHx100_ref_r2_s32452843',
                  'E0_soft_s1', 'LB4_s1', 'LC_s1x', 'npprobe5_E0_ref_s32452843', 'L0_s32452843_r2', 'xLC_s1']
    chk('⑭b 선적 정책: 층상 캠페인 · M 열람된 DEV seed 1 런만 열림 · 나머지는 잠김 (fullmatch — 앞뒤 덧붙임도 잠김)',
        all(mixer_bed.classify(n, pol)[0] for n in names_ok)
        and not any(mixer_bed.classify(n, pol)[0] for n in names_lock))
    import re as _re
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cited = [(a['pattern'], _re.findall(r'docs/[A-Za-z0-9_./-]+[A-Za-z0-9_/]', a['basis'])) for a in pol['allow']]
    chk('⑭d 선적 정책: 항목마다 근거 basis 가 리포 안의 기록 경로를 하나 이상 적고, 그 경로가 실제로 있다',
        all(paths and all(os.path.exists(os.path.join(repo, q)) for q in paths) for _, paths in cited))
    pdir = tempfile.mkdtemp(prefix='mxpol_')                   # 런 루트 밖 (⑪ 스냅숏과 섞지 않는다)
    broken = {'json': '{', 'empty_basis': json.dumps({'schema': 'mixer_view_policy/1', 'allow': [
        {'pattern': '.*', 'basis': ' ', 'since': '2026-09-30'}]}),
        'bad_re': json.dumps({'schema': 'mixer_view_policy/1', 'allow': [
            {'pattern': '(', 'basis': 'x', 'since': '2026-09-30'}]}),
        'schema': json.dumps({'schema': 'other/9', 'allow': []})}
    fc = []
    for k, txt in broken.items():
        p = os.path.join(pdir, k + '.json'); open(p, 'w').write(txt)
        pp = mixer_bed.load_policy(p)
        fc.append(pp['ok'] is False and not mixer_bed.classify('L0_s32452843', pp)[0])
    chk('⑭c 정책 파일이 깨지면 (JSON · 빈 basis · 정규식 · schema) 전부 잠긴다 (fail-closed)', all(fc))
    #  ⑭e (2026-10-05 · 개발 탐색 dev-u · 강성 축 사전등록 §12) — LU212 · LU637 런은 **M 열람 기록 없이** 열리지 않는다.  정책의 어느 항목이 dev-u 셀
    #     이름을 열면 그 항목의 basis 가 리포 안의 dev-u 열람 기록 폴더 (docs/data/mixer_highbo_devu_prelim_…) 를 적고 그 폴더가 있어야 한다.
    #     ★ 반례를 먼저 확인했다 — 옛 시험은 dev-rot 항목의 패턴을 `(LC_ref_r2|LH_ref_r2|E0_ref|LU212_ref_r2|LU637_ref_r2)_s32452843` 로 넓힌 정책
    #       (근거는 dev-rot 기록 그대로) 을 54/54 로 통과시켰다 — LU 런이 열람 기록 없이 화면에 열린다.
    lu_names = ['LU212_ref_r2_s32452843', 'LU637_ref_r2_s32452843', 'LU212_ref_r8_s15485863', 'LU637_soft_r2_s32452843', 'LU212_ref_s32452843']

    def lu_open_without_record(pol_):
        bad_ = []
        for n_ in lu_names:
            for a_ in pol_['allow']:
                if a_['_rx'].fullmatch(n_) and not [q for q in _re.findall(r'docs/data/mixer_highbo_devu_prelim_[A-Za-z0-9_]+', a_['basis'])
                                                    if os.path.isdir(os.path.join(repo, q))]:
                    bad_.append(n_)
        return bad_
    raw_pol = json.load(open(mixer_bed.POLICY_PATH, encoding='utf-8'))
    wide = []
    for k_, pat_ in (('in_devrot', r'(LC_ref_r2|LH_ref_r2|E0_ref|LU212_ref_r2|LU637_ref_r2)_s32452843'), ('generic', r'L[A-Za-z0-9]+_ref_r2_s32452843')):
        w_ = json.loads(json.dumps(raw_pol))
        w_['allow'][1]['pattern'] = pat_
        p = os.path.join(pdir, f'wide_{k_}.json'); open(p, 'w').write(json.dumps(w_, ensure_ascii=False))
        wide.append(mixer_bed.load_policy(p))
    chk('⑭e ★ dev-u (LU212 · LU637) 런은 M 열람 기록 없이 열리지 않는다 — 선적 정책에서 잠김 (분류 · 목록 ③) · 열린다면 그 항목 basis 가 리포 안의 dev-u 열람 '
        '기록 폴더를 적어야 한다 / 반례 둘 (dev-rot 항목에 LU 를 끼움 · L* 일반 패턴 — 근거 = dev-rot 기록) 은 "기록 없는 열림" 으로 잡힌다',
        not any(mixer_bed.classify(n_, pol)[0] for n_ in lu_names) and lu_open_without_record(pol) == []
        and all(w_['ok'] and lu_open_without_record(w_) for w_ in wide))

    # ── ⑮ 크기 상한 · 캐시 ──
    old = mixer_bed.MAX_FRAME_BYTES
    mixer_bed.MAX_FRAME_BYTES = 100
    mixer_bed.clear_cache()
    big = c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=201&view=3d')
    mixer_bed.MAX_FRAME_BYTES = old
    chk('⑮ 크기 상한을 넘는 프레임은 읽지 않는다 (413)', big.status_code == 413)
    calls = []
    orig = mixer_bed._parse_frame
    mixer_bed._parse_frame = lambda p: calls.append(p) or orig(p)
    try:
        mixer_bed.clear_cache()
        c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=201&view=3d')
        c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=201&view=slab&x0=0&t=0.001')
        n_first = len(calls)
        pth = os.path.join(L0, 'post', 'mix_201.liggghts')
        st = os.stat(pth)
        os.utime(pth, ns=(st.st_atime_ns, st.st_mtime_ns + 10**9))
        c.get('/api/mixer/frame?root=0&run=L0_s32452843&step=201&view=3d')
        os.utime(pth, ns=(st.st_atime_ns, st.st_mtime_ns))
    finally:
        mixer_bed._parse_frame = orig
    chk('⑮b 같은 프레임은 한 번만 읽는다 · 파일이 바뀌면 (mtime) 다시 읽는다', n_first == 1 and len(calls) == 2)

    # ── ⑪ 쓰기 없음 ──
    chk('⑪ 보기 전용: 런 폴더에 아무것도 쓰지 않는다 (파일 · 크기 · mtime 불변)', snapshot(tmp) == before)

    # ── ⑯ 화면 스크립트 ──
    chk('⑯ 침대 보기 스크립트에 innerHTML 보간이 없다 (런 이름은 textContent)',
        'bedRuns' in html and not any('${' in ln for ln in html.splitlines() if 'innerHTML' in ln))
    chk('⑯b 화면이 겹침 · 혼합 지표를 계산한다는 문구가 없다 (보기 전용 표지와 함께 "계산하지 않는다")',
        '계산하지 않는다' in html)

    # ── ⑰ 재생 · 고화질 PNG · GIF (1저자 요청 09-30 밤) — 화면 쪽 계약만 (동작은 브라우저 시험) ──
    chk('⑰ 자동 재생 · 고화질 PNG · GIF 버튼이 있다',
        all(f'id="{i}"' in html for i in ('bedPlay', 'bedSpeed', 'bedLoop', 'bedPng', 'bedPngScale', 'bedGif', 'bedGifStride', 'bedGifRange')))
    chk('⑰b GIF 인코더는 페이지 안에 있다 (외부 GIF 라이브러리 · 워커 없음) · 내보낸 그림에 보기 전용 표지를 붙인다',
        'function gifBegin(' in html and 'function gifAdd(' in html and 'function lzwBlocks(' in html and 'gif.js' not in html
        and 'new Worker' not in html and 'idx.length > 1000' in html and '150 장 이하' not in html
        and '보기 전용 — 판정은 3D 칸 M 으로만 · 원 = 실제 반경' in html)
    chk('⑰c 3D: 메시를 프레임 사이에 재사용하고 (InstancedMesh.dispose 로 GPU 버퍼를 푼다) · WebGL 컨텍스트가 끊기면 복구 / 재생성한다',
        'mesh.count = cnt' in html and 'o.dispose()' in html and 'webglcontextlost' in html and 'webglcontextrestored' in html
        and 'function rebuild3(' in html)
    gc = gif_color_check(html, pdir)
    if gc is None:
        print('  —     ⑰d GIF 색 시험 건너뜀 (node 없음 · CI 에서 돈다)')
    else:
        chk(f'⑰d GIF: 첫 프레임에 없던 상 색 (층상 런의 SE) 도 뒤 프레임에서 그 색으로 나온다 — 팔레트를 첫 프레임에서만 뽑지 않는다 '
            f'(1저자 09-30 밤 "gif 하면 흑백") · {gc[1]}', gc[0])
    # ── ⑰e–g 투명 배경 GIF · GIF 캡션에 런 이름 없음 (1저자 10-02) ──
    gt = gif_clear_check(html, pdir)
    if gt is None:
        print('  —     ⑰e 투명 GIF 시험 건너뜀 (node 없음 · CI 에서 돈다)')
    else:
        chk(f'⑰e 투명 배경 GIF: 배경 = 투명 색 · 덩어리 불투명 그대로 · 앞 프레임 잔상 없음 (처분 2) · {gt[1]}', gt[0])
    cc = caption_check(html, pdir)
    if cc is None:
        print('  —     ⑰f GIF 캡션 시험 건너뜀 (node 없음 · CI 에서 돈다)')
    else:
        chk(f'⑰f GIF 캡션에는 런 (샘플) 이름이 없고 PNG 캡션에는 그대로 있다 · {cc[1]}', cc[0])
    chk('⑰h ☑ 드럼 면 채우기 (#bedDrumFill · 기본 켜짐) — 3D 드럼을 실물처럼 (원통 벽 · 뒤 뚜껑 · 앞 테) 그리고 끄면 옛 선 그림 · '
        '토글은 메시를 다시 만들고 (선 · 면 메시 모두 GPU 에서 푼다) 카메라는 그대로',
        'id="bedDrumFill" checked' in html and 'function drumSolid(' in html and 'function drumLines(' in html
        and "($('bedDrumFill') || {}).checked ? drumSolid(THREE, j.drum) : drumLines(THREE, j.drum)" in html
        and 'else if (o.isMesh) { o.geometry.dispose(); o.material.dispose(); }' in html
        and "$('bedDrumFill').addEventListener('change'" in html
        and 'THREE.BackSide' in html[html.find('function drumSolid('):html.find('function render3d(')]
        and 'THREE.FrontSide' in html[html.find('function drumSolid('):html.find('function render3d(')]
        and 'back.rotation.y = Math.PI / 2' in html and 'front.rotation.y = -Math.PI / 2' in html)
    #   ⑰h 의 BackSide · 안쪽 향한 뚜껑 둘 = 어느 시점에서도 가까운 쪽 벽 · 뚜껑은 그리지 않는다 (잘라 본 그림) — 양면 벽이면 돌렸을 때 입자가 가려졌다 (10-02 시각 확인)
    chk('⑰g ☑ 투명 배경 GIF (#bedGifClear) 가 있고 GIF 내보내기가 그 값을 프레임 · 인코더에 넘긴다',
        'id="bedGifClear"' in html and "$('bedGifClear')" in html and 'captureFrame(G, clear)' in html
        and 'gifBegin(rgba, w, h, clear)' in html and 'gifAdd(gif, rgba, delay, clear)' in html)
    # ── ⑰i 3D PNG · GIF 잘림 (1저자 10-02) — 드럼이 틀에 걸리면 내보낼 때 틀을 넓힌다 · drawing buffer 는 키우지 않고 타일로 그린다 ──
    pc = pad_check(html, pdir)
    if pc is None:
        print('  —     ⑰i 여백 계산 시험 건너뜀 (node 없음 · CI 에서 돈다)')
    else:
        chk(f'⑰i 내보내기 여백 (exportPad): 드럼 윤곽이 틀 가장자리 3 % 안 · 밖이면 그만큼 틀을 넓히고 · 틀 안 · 크게 당긴 시점 · 카메라 뒤 점은 화면 그대로 · {pc[1]}', pc[0])
    sl = lambda a, b: html[html.find(a):html.find(b)] if html.find(a) >= 0 and html.find(b) > html.find(a) else ''
    rt, g3 = sl('function render3Tiles(', 'function grab3d('), sl('function grab3d(', 'function exportPng(')
    chk('⑰i-b 3D 내보내기: PNG 는 drumPad3 (드럼 두 테 투영 → exportPad) 로 틀을 정하고 render3Tiles 로 그린다 — 카메라 setViewOffset 타일 · '
        '끝나면 clearViewOffset · 화면 캔버스 (drawing buffer) 를 키우지 않는다 (setPixelRatio 없음) · GIF 는 여백을 한 번만 정해 모든 프레임에 같은 틀',
        'function drumPad3(' in html and 'setViewOffset(' in rt and 'cam.clearViewOffset()' in rt
        and 'drumPad3(' in g3 and 'render3Tiles(' in g3 and 'setPixelRatio' not in g3 and 'setPixelRatio' not in rt
        and 'render3Tiles(' in sl('function captureFrame(', 'function exportGif(')
        and 'drumPad3(' in sl('function exportGif(', '// ── 자동 재생'))
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(pdir, ignore_errors=True)
    print(f'\ntest_mixer_bed_view: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 1 if _fail else 0


if __name__ == '__main__':
    raise SystemExit(main())

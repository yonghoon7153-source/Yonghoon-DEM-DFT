#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""전류 흐름 3D 보기 (DEM 뷰어 'net_current') 회귀 — 1저자 요청 *"전류가 보이게"* (보고 슬라이드 그림).

웹앱 망 단계는 간선별 전류를 디스크에 남기지 않는다 (`--dump-raw-dir` 를 넘기지 않는다 · 망 단계 · 봉인 · 게시 계약은 그대로 둔다).
그래서 케이스마다 **한 번** `scripts/network_current.py dump <결과 폴더>` 를 돌려 같은 풀이의 간선 전류를 `network_raw_dump/` 에 남기고,
뷰어가 `/network-current` 로 상위 N 간선을 받아 굵기 · 색 (log |I|) 으로 그린다.

  ① 덤프 ↔ 비덤프 비트 동일 — `network_conductivity.py` CLI 를 같은 입력으로 두 번 (`--dump-raw-dir` 없이 · 있게) → 네 JSON 바이트 동일
     (덤프는 출력만 더한다).  real14 기준 침대 실측 (10-06 · 62 s · 네 JSON 동일 · 원 덤프 96 MB) — `NETCUR_REAL14=1` 이면 이 시험도 real14 로 돈다.
  ② 한 번 실행 도구 — 웹앱이 쓴 argv (도장 `network_provenance.json`) 그대로 · **옆 폴더**에서 풀고 (게시 파일 무변경) · 덤프 폴더 이름이
     망 산출물 glob (`network_raw_*`) 에 들어 다음 망 재계산이 옛 세대와 함께 치운다 · 게시 JSON 대조 (같음 · 다름) · 입력 해시 불일치 거부 ·
     도장 없으면 argv 를 지어내지 않는다.
  ③ 경로 `/results/<id>/network-current` · `/archive/results/<folder>/network-current` — 덤프 없음 = 404 + 만드는 명령 · 상위 N (|I| 내림차순) ·
     I_전체 = 해의 G · z-단면 전류 보존 · Tellegen (Σ I²R = I_전체) · 방향 (전위 강하) · 위치 = 3d-data 입자 · 주기 경계 표지 · 0 전류 간선 제외 ·
     채널 · 모드 · 잘못된 인자 400 · 게시 σ 대조 · 세대 대조.
  ④ 뷰어 (node 로 함수를 잘라 실행) — DEM 드롭다운 · 주기 경계 함수 (서버 표지와 같은 답) · URL (실 · 보관 · 질의문) · 범례 문구 · 컬러바 눈금 ·
     모드 전환 정리 · 늦은 응답 무시.

  python3 webapp/test_network_current_view.py        # 종료코드 0 = PASS
"""
import copy
import fnmatch
import gzip
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
NC = os.path.join(SCRIPTS, 'network_conductivity.py')
TOOL = os.path.join(SCRIPTS, 'network_current.py')
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
CHECK_ALL = os.path.join(SCRIPTS, 'check_all.sh')
TYPE_MAP = '1:AM_P,3:SE'
NET_FOUR = ('network_conductivity.json', 'network_conductivity_hertzian.json',
            'network_conductivity_physics.json', 'network_conductivity_dual.json')
DUMP = 'network_raw_dump'

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


# ══════════════════════════════════════════════════════════════════════════════
#  합성 침대 — SE 단순입방 4×4×8 (x · y 주기 경계 접촉 + 층을 건너는 대각 wrap 접촉) + AM 기둥 셋 (가로 연결 · x wrap 하나)
#  sim 단위 = mm (scale 1000 → µm) · 접촉 면적 · 힘은 난수 (간선 전류가 서로 다르게 — 순서 · log 눈금 시험)
# ══════════════════════════════════════════════════════════════════════════════
def bed(seed=11):
    rnd = random.Random(seed)
    r, a, n, nz = 0.0005, 0.00098, 4, 8
    box = n * a
    atoms, cons, idx, k = {}, [], {}, 0
    for iz in range(nz):
        for iy in range(n):
            for ix in range(n):
                k += 1
                idx[(ix, iy, iz)] = 100 + k
                atoms[100 + k] = dict(type=3, x=(ix + 0.5) * a, y=(iy + 0.5) * a, z=r + iz * a, radius=r)

    def con(i, j, f=1.0):
        d = 2 * r - a
        cons.append(dict(id1=i, id2=j, fz=rnd.uniform(2e-5, 8e-5), area=math.pi * (r / 2) * d * f * rnd.uniform(0.3, 3.0), delta=d))
    for iz in range(nz):
        for iy in range(n):
            for ix in range(n):
                i = idx[(ix, iy, iz)]
                con(i, idx[((ix + 1) % n, iy, iz)])               # x 이웃 (ix = n-1 → 주기 경계)
                con(i, idx[(ix, (iy + 1) % n, iz)])               # y 이웃 (주기 경계)
                if iz + 1 < nz:
                    con(i, idx[(ix, iy, iz + 1)])
    for iz in range(1, nz - 2):                                    # 층을 건너는 대각 wrap (수직 전류를 실어 나른다 — 단면 몫 시험)
        for iy in (0, 2):
            con(idx[(n - 1, iy, iz)], idx[(0, iy, iz + 1)], f=0.7)
    plate = r + (nz - 1) * a + r
    ram, s = 0.0006, 0.0011
    for c, (x, y) in enumerate(((0.0007, 0.0020), (0.0020, 0.0020), (0.0033, 0.0020))):
        for kz in range(7):
            aid = 1000 + 10 * c + kz
            atoms[aid] = dict(type=1, x=x, y=y, z=ram + kz * s, radius=ram)
            if kz:
                d = 2 * ram - s
                cons.append(dict(id1=aid - 1, id2=aid, fz=rnd.uniform(1e-4, 4e-4),
                                 area=math.pi * (ram / 2) * d * rnd.uniform(0.5, 2.0), delta=d))
    for (i, j) in ((1003, 1013), (1013, 1023), (1004, 1024)):      # 1004 ↔ 1024 = x 주기 경계 (가로)
        cons.append(dict(id1=i, id2=j, fz=2e-4, area=math.pi * (ram / 2) * 5e-5, delta=5e-5))
    return atoms, cons, plate, box


def write_inputs(d, case=None):
    A, C, plate, box = case or bed()
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'atoms.csv'), 'w') as f:
        f.write('id,type,x,y,z,radius\n')
        for i, at in sorted(A.items()):
            f.write(f'{i},{at["type"]},{at["x"]!r},{at["y"]!r},{at["z"]!r},{at["radius"]!r}\n')
    with open(os.path.join(d, 'contacts.csv'), 'w') as f:
        f.write('id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta\n')
        for c in C:
            f.write(f'{c["id1"]},{c["id2"]},0,0,{c["fz"]!r},0,0,0,{c["area"]!r},{c["delta"]!r}\n')
    with open(os.path.join(d, 'mesh_info.json'), 'w') as f:
        json.dump({'plate_z': plate}, f)
    with open(os.path.join(d, 'input_params.json'), 'w') as f:
        json.dump({'box_x': box, 'box_y': box}, f)


def run_cli(inp, out, dump=None, type_map=TYPE_MAP, scale='1000'):
    """웹앱 망 단계와 같은 argv (`app._network_and_stage_e`) — -o 폴더에 mesh_info · input_params 사본을 둔다 (CLI 가 거기서 읽는다)."""
    os.makedirs(out, exist_ok=True)
    for n in ('mesh_info.json', 'input_params.json'):
        if os.path.exists(os.path.join(inp, n)) and os.path.abspath(inp) != os.path.abspath(out):
            shutil.copy2(os.path.join(inp, n), os.path.join(out, n))
    cmd = [sys.executable, NC, os.path.join(inp, 'atoms.csv'), os.path.join(inp, 'contacts.csv'), '-o', out,
           '-t', type_map, '-s', str(scale), '--contact-mode', 'both']
    if dump:
        cmd += ['--dump-raw-dir', dump]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    return r.returncode, r.stdout + r.stderr


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def tree(d, skip=DUMP):
    out = {}
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x != skip]
        for fn in files:
            p = os.path.join(root, fn)
            out[os.path.relpath(p, d)] = sha(p)
    return out


def run_tool(*args):
    r = subprocess.run([sys.executable, TOOL] + [str(a) for a in args], capture_output=True, text=True, timeout=1800)
    return r.returncode, r.stdout + r.stderr


def dump_file(raw, stem):
    """덤프 폴더의 그 파일 — 도구 판 (.csv.gz) 또는 CLI 원 판 (.csv)."""
    for ext in ('.csv.gz', '.csv'):
        if os.path.exists(os.path.join(raw, stem + ext)):
            return os.path.join(raw, stem + ext)
    return os.path.join(raw, stem + '.csv.gz')


def read_csv_rows(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt', encoding='utf-8') as f:
        lines = f.read().splitlines()
    hdr = lines[0].split(',')
    return [dict(zip(hdr, ln.split(','))) for ln in lines[1:] if ln]


# ══════════════════════════════════════════════════════════════════════════════
#  ① 덤프 ↔ 비덤프 비트 동일
# ══════════════════════════════════════════════════════════════════════════════
def section_bit_identity(tmp):
    print('[①] --dump-raw-dir 가 망 결과를 바꾸지 않는다 (네 JSON 바이트 동일)')
    inp = os.path.join(tmp, 'bit_inp')
    write_inputs(inp)
    ra, oa = run_cli(inp, os.path.join(tmp, 'bit_A'))
    rb, ob = run_cli(inp, os.path.join(tmp, 'bit_B'), dump=os.path.join(tmp, 'bit_dump'))
    chk(f'①a CLI 두 번 다 rc 0 (덤프 없이 {ra} · 덤프 {rb})', ra == 0 and rb == 0, (oa + ob)[-400:])
    for n in NET_FOUR:
        pa, pb = os.path.join(tmp, 'bit_A', n), os.path.join(tmp, 'bit_B', n)
        chk(f'①b {n} 바이트 동일 (덤프 없음 ↔ 있음)', os.path.exists(pa) and os.path.exists(pb) and sha(pa) == sha(pb))
    dumped = sorted(os.listdir(os.path.join(tmp, 'bit_dump'))) if os.path.isdir(os.path.join(tmp, 'bit_dump')) else []
    want = {f'{k}_{m}_{c}{e}' for k, e in (('edges', '.csv'), ('nodes', '.csv'), ('solution', '.json'))
            for m in ('hertzian', 'physics') for c in ('ionic', 'electronic', 'thermal')}
    chk(f'①c 덤프 = 모드 2 × 채널 3 × (edges · nodes · solution) 18 파일 ({len(dumped)})', set(dumped) == want, repr(dumped)[:200])
    chk('①d 덤프 없는 실행은 덤프 파일을 만들지 않는다 (bit_A 에 edges_* 없음)',
        not any(x.startswith(('edges_', 'nodes_', 'solution_')) for x in os.listdir(os.path.join(tmp, 'bit_A'))))
    try:
        sol = json.load(open(os.path.join(tmp, 'bit_dump', 'solution_hertzian_ionic.json')))
        pub = json.load(open(os.path.join(tmp, 'bit_B', 'network_conductivity_hertzian.json')))
        chk(f'①e 덤프 해의 σ/σ₀ 를 8 자리로 반올림하면 게시 sigma_full 과 같다 ({pub.get("sigma_full")})',
            round(sol['sigma_ratio'], 8) == pub.get('sigma_full'))
    except (OSError, ValueError, KeyError) as e:
        chk('①e 덤프 해 ↔ 게시 sigma_full', False, repr(e))
    if os.environ.get('NETCUR_REAL14') == '1':
        section_bit_identity_real14(tmp)
    else:
        print('  —  real14 판 (NETCUR_REAL14=1 일 때만 · 약 2 분) 건너뜀 — 10-06 실측: 네 JSON 동일 · 62 s · 원 덤프 96 MB')


def section_bit_identity_real14(tmp):
    src = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
    raw = os.path.join(tmp, 'r14_src')
    os.makedirs(raw)
    for n in ('atom_2060000.liggghts', 'contact_2060000.liggghts'):
        with gzip.open(os.path.join(src, n + '.gz'), 'rb') as fi, open(os.path.join(raw, n), 'wb') as fo:
            shutil.copyfileobj(fi, fo)
    for n in ('mesh_2060000.stl', 'input_real_14.liggghts'):
        shutil.copy2(os.path.join(src, n), raw)
    case = os.path.join(tmp, 'r14_case')
    rp = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'parse_liggghts.py')]
                        + [os.path.join(raw, n) for n in ('atom_2060000.liggghts', 'contact_2060000.liggghts',
                                                           'mesh_2060000.stl', 'input_real_14.liggghts')] + ['-o', case],
                        capture_output=True, text=True)
    chk('①r real14 덤프 해석 (parse_liggghts)', rp.returncode == 0, rp.stderr[-300:])
    ra, _ = run_cli(case, os.path.join(tmp, 'r14_A'), type_map='1:AM_P,2:AM_S,3:SE')
    rb, _ = run_cli(case, os.path.join(tmp, 'r14_B'), dump=os.path.join(tmp, 'r14_dump'), type_map='1:AM_P,2:AM_S,3:SE')
    same = [n for n in NET_FOUR if sha(os.path.join(tmp, 'r14_A', n)) == sha(os.path.join(tmp, 'r14_B', n))] if ra == rb == 0 else []
    chk(f'①r real14 — 네 JSON 바이트 동일 ({len(same)}/4)', len(same) == 4)


# ══════════════════════════════════════════════════════════════════════════════
#  ② 한 번 실행 도구 (scripts/network_current.py dump)
# ══════════════════════════════════════════════════════════════════════════════
def publish_case(rd, run_id='20261007T000000-netcur01'):
    """웹앱 망 단계가 게시한 상태를 흉내 낸다 — 같은 CLI 를 -o 결과 폴더로 · 도장 (argv · 입력 해시) · full_metrics 의 망 세대."""
    write_inputs(rd)
    rc, out = run_cli(rd, rd)
    if rc:
        raise RuntimeError(out[-600:])
    import pipeline_service as ps
    inputs = {n: ps.file_digest(os.path.join(rd, n)) for n in ('atoms.csv', 'contacts.csv')}
    ps.stamp_network_provenance(rd, run_id, inputs, 'success', argv={'type_map': TYPE_MAP, 'scale': '1000', 'contact_mode': 'both'})
    with open(os.path.join(rd, 'full_metrics.json'), 'w') as f:
        json.dump({'network_run_id': run_id, 'porosity': 20.0}, f)
    return run_id


def section_tool(tmp):
    print('[②] 한 번 실행 도구 — scripts/network_current.py dump <결과 폴더>')
    import pipeline_service as ps
    rd = os.path.join(tmp, 'pub')
    rid = publish_case(rd)
    before = tree(rd)
    rc, out = run_tool('dump', rd)
    chk(f'②a 도구 rc 0', rc == 0, out[-600:])
    dd = os.path.join(rd, DUMP)
    man = {}
    try:
        man = json.load(open(os.path.join(dd, 'manifest.json')))
    except (OSError, ValueError):
        pass
    chk('②b 덤프 폴더 + manifest.json', os.path.isdir(dd) and bool(man))
    chk('②c 게시 파일 무변경 (덤프 폴더 밖 전 파일 해시 같음 · 새 파일 없음)', tree(rd) == before,
        repr(sorted(set(tree(rd)) ^ set(before)))[:200])
    chk(f'②d 덤프 폴더 이름이 망 산출물 glob 에 든다 (다음 망 재계산이 옛 세대와 함께 치운다) — {ps.NETWORK_ARTIFACT_GLOBS}',
        any(fnmatch.fnmatch(DUMP, g) for g in ps.NETWORK_ARTIFACT_GLOBS))
    chk(f'②e manifest argv = 도장 argv · 출처 = 도장 ({man.get("argv")} · {man.get("argv_source")})',
        man.get('argv') == {'type_map': TYPE_MAP, 'scale': '1000', 'contact_mode': 'both'}
        and man.get('argv_source') == 'network_provenance.json')
    chk(f'②f manifest 망 세대 = 도장 run id ({man.get("network_run_id")})', man.get('network_run_id') == rid)
    pm = man.get('published_match') or {}
    chk(f'②g 게시 JSON 대조 = identical (같은 코드 · 같은 입력 · 같은 argv) — {pm.get("status")}', pm.get('status') == 'identical')
    files = sorted((man.get('files') or {}).keys())
    want = {f'{k}_{m}_{c}' for k in ('edges', 'nodes') for m in ('hertzian', 'physics') for c in ('ionic', 'electronic')}
    chk(f'②h 덤프 = 이온 · 전자 × Hertz · Physics (edges · nodes = .csv.gz · solution .json) · 열 채널 없음 ({len(files)})',
        {f.split('.')[0] for f in files if f.startswith(('edges_', 'nodes_'))} == want
        and all(f.endswith('.csv.gz') for f in files if f.startswith(('edges_', 'nodes_')))
        and not any('thermal' in f for f in files)
        and all(os.path.exists(os.path.join(dd, f)) and sha(os.path.join(dd, f)) == man['files'][f]['sha256'] for f in files))
    cmdline = ' '.join(man.get('cmd') or [])
    chk('②i manifest 의 명령 = 웹앱 망 단계 argv + --dump-raw-dir (옆 폴더 -o · --contact-mode both)',
        'network_conductivity.py' in cmdline and '--dump-raw-dir' in cmdline and '--contact-mode both' in cmdline
        and f'-t {TYPE_MAP}' in cmdline and '-s 1000' in cmdline and f'-o {rd} ' not in cmdline + ' ', cmdline[:300])
    chk('②j 도구 출력에 실제로 돌린 명령 (network_conductivity.py … --dump-raw-dir) 이 찍힌다',
        'network_conductivity.py' in out and '--dump-raw-dir' in out)
    # 같은 원천 — 덤프 edges 의 |I| 가 다시 푼 해 (raw) 와 같다: solution G_eff 와 단면 보존으로 아래 ③ 에서 본다.

    # 다음 망 재계산 (stash) 이 덤프를 옛 세대와 함께 옮긴다 — 실 함수 (`stash_network`) 로 확인 (사본 폴더)
    rd_s = os.path.join(tmp, 'pub_stash')
    shutil.copytree(rd, rd_s)
    st = ps.stash_network(rd_s, case_id='t')
    chk('②k 망 재계산 stash 가 덤프 폴더를 옛 세대와 함께 옮긴다 (재계산 성공 = 버림 · 실패 = 되돌림)',
        st is not None and os.path.isdir(os.path.join(st, DUMP)) and not os.path.exists(os.path.join(rd_s, DUMP)))

    # 입력이 도장과 다르면 거부 — 덤프를 만들지 않는다
    rd2 = os.path.join(tmp, 'pub_input_changed')
    shutil.copytree(rd, rd2)
    shutil.rmtree(os.path.join(rd2, DUMP))
    with open(os.path.join(rd2, 'contacts.csv')) as f:
        rows = f.read().splitlines()
    rows[1] = rows[1].rsplit(',', 1)[0] + ',' + repr(float(rows[1].rsplit(',', 1)[1]) * 1.5)
    with open(os.path.join(rd2, 'contacts.csv'), 'w') as f:
        f.write('\n'.join(rows) + '\n')
    rc2, out2 = run_tool('dump', rd2)
    chk('②l 입력 (contacts.csv) 해시 ≠ 도장 → 거부 (rc ≠ 0 · 덤프 없음 · 사유 = 입력)',
        rc2 != 0 and not os.path.exists(os.path.join(rd2, DUMP)) and 'contacts.csv' in out2, out2[-300:])

    # 게시 JSON 이 다시 푼 해와 다르면 기록한다 (거부 아님 — 코드 세대 차이일 수 있다 · 뷰어가 경고)
    rd3 = os.path.join(tmp, 'pub_differs')
    shutil.copytree(rd, rd3)
    shutil.rmtree(os.path.join(rd3, DUMP))
    p = os.path.join(rd3, 'network_conductivity_hertzian.json')
    d = json.load(open(p))
    d['sigma_full'] = d['sigma_full'] * 1.01
    with open(p, 'w') as f:
        json.dump(d, f, indent=2)
    rc3, out3 = run_tool('dump', rd3)
    m3 = {}
    try:
        m3 = json.load(open(os.path.join(rd3, DUMP, 'manifest.json')))
    except (OSError, ValueError):
        pass
    pm3 = m3.get('published_match') or {}
    chk(f'②m 게시 JSON ≠ 다시 푼 해 → 기록 (status differs · 파일 이름) · 덤프는 만든다 (rc {rc3})',
        rc3 == 0 and pm3.get('status') == 'differs'
        and (pm3.get('files') or {}).get('network_conductivity_hertzian.json', {}).get('status') == 'differs', repr(pm3)[:300])

    # 도장이 없으면 argv 를 지어내지 않는다 — 명시 인자로만
    rd4 = os.path.join(tmp, 'pub_noprov')
    shutil.copytree(rd, rd4)
    shutil.rmtree(os.path.join(rd4, DUMP))
    os.remove(os.path.join(rd4, 'network_provenance.json'))
    os.remove(os.path.join(rd4, 'full_metrics.json'))
    rc4, out4 = run_tool('dump', rd4)
    chk('②n 도장 없음 + argv 인자 없음 → 거부 (웹앱이 쓴 type_map · scale 을 짐작하지 않는다)',
        rc4 != 0 and not os.path.exists(os.path.join(rd4, DUMP)), out4[-300:])
    rc5, out5 = run_tool('dump', rd4, '--type-map', TYPE_MAP, '--scale', '1000')
    m5 = {}
    try:
        m5 = json.load(open(os.path.join(rd4, DUMP, 'manifest.json')))
    except (OSError, ValueError):
        pass
    chk(f'②o 도장 없음 + --type-map · --scale → 만든다 · argv 출처 = cli (rc {rc5} · {m5.get("argv_source")})',
        rc5 == 0 and m5.get('argv_source') == 'cli', out5[-300:])
    try:
        import network_current as _ncur
        st4, b4 = _ncur.current_payload(rd4, 'ionic', 'hertzian', 5, 1000)
        g4 = b4.get('generation') or {}
    except Exception as e:                                       # noqa: BLE001 — 옛 코드 (모듈 없음)
        st4, g4 = None, {'err': repr(e)}
    chk(f'②p 도장 없는 케이스의 덤프 → 세대 대조 = 미확인 (match None · 사유) — 참이라고 하지 않는다 ({st4} · {g4})',
        st4 == 200 and g4.get('match') is None and '미확인' in str(g4.get('note')))
    return rd, rid


# ══════════════════════════════════════════════════════════════════════════════
#  ③ 경로
# ══════════════════════════════════════════════════════════════════════════════
def section_routes(tmp, pub_rd, rid):
    print('[③] /results/<id>/network-current · /archive/results/<folder>/network-current')
    import app as A
    c = A.app.test_client()
    up, rs, ar = A.app.config['UPLOAD_FOLDER'], A.app.config['RESULTS_FOLDER'], A.app.config['ARCHIVE_FOLDER']

    def make(cid, src=pub_rd, with_dump=True):
        os.makedirs(os.path.join(up, cid), exist_ok=True)
        with open(os.path.join(up, cid, 'meta.json'), 'w') as f:
            json.dump({'name': cid, 'status': 'done', 'type_map': TYPE_MAP, 'scale': 1000, 'mode': 'standard'}, f)
        dst = os.path.join(rs, cid)
        shutil.copytree(src, dst)
        if not with_dump and os.path.isdir(os.path.join(dst, DUMP)):
            shutil.rmtree(os.path.join(dst, DUMP))
        return dst

    def get(url):
        r = c.get(url)
        return r.status_code, (r.get_json(silent=True) or {})

    rd_none = make('261007_000001_nodump', with_dump=False)
    s, j = get('/results/261007_000001_nodump/network-current')
    chk(f'③a 덤프 없음 → 404 · error no_dump ({s} · {j.get("error")})', s == 404 and j.get('error') == 'no_dump' and j.get('ok') is False)
    chk('③b 404 본문에 만드는 명령 (scripts/network_current.py dump <이 케이스 결과 폴더>)',
        'scripts/network_current.py dump' in str(j.get('how_to')) and os.path.realpath(rd_none) in str(j.get('how_to')), repr(j)[:300])
    import shlex
    chk('③b2 그 명령 = 웹앱 프로세스의 파이썬 + 이 리포 도구의 절대 경로 (어디서 붙여 넣어도 같은 환경)',
        str(j.get('how_to')).startswith(shlex.quote(sys.executable) + ' ' + shlex.quote(TOOL) + ' dump '), str(j.get('how_to'))[:200])

    cid = '261007_000002_dump'
    rd = make(cid)
    raw = os.path.join(rd, DUMP)
    sol = json.load(open(os.path.join(raw, 'solution_hertzian_ionic.json')))
    erows = read_csv_rows(dump_file(raw, 'edges_hertzian_ionic'))
    nrows = {int(r['id']): r for r in read_csv_rows(dump_file(raw, 'nodes_hertzian_ionic'))}
    I_tot = sol['G_eff']
    nz = [abs(float(r['I'])) for r in erows if abs(float(r['I'])) > 1e-12 * I_tot]

    s, j = get(f'/results/{cid}/network-current?channel=ionic&mode=hertzian&top=5')
    E = j.get('edges') or []
    chk(f'③c 이온 · Hertz · top 5 → 200 · 간선 5 ({s} · {len(E)})', s == 200 and j.get('ok') is True and len(E) == 5)
    sh = [e.get('s') for e in E]
    chk('③d |I|/I_전체 내림차순 · 첫 간선 = 해의 최대 |I|', sh == sorted(sh, reverse=True) and bool(sh)
        and abs(sh[0] - max(nz) / I_tot) < 1e-12)
    chk(f'③e I_전체 = 덤프 해의 G (ΔV = 1) ({j.get("I_total")} · {I_tot})', j.get('I_total') == I_tot)
    chk(f'③f 채널 · 모드 · 관통 간선 수 (echo · {j.get("channel")} · {j.get("mode")} · {j.get("n_perc_edges")} = {len(erows)})',
        j.get('channel') == 'ionic' and j.get('mode') == 'hertzian' and j.get('n_perc_edges') == len(erows))
    zc = j.get('zcut') or {}
    chk(f'③g z-단면 전류 보존 (전 간선 Σ 위로 흐르는 전류 = I_전체 · 최대 편차 {zc.get("identity_max_dev")})',
        isinstance(zc.get('identity_max_dev'), float) and zc['identity_max_dev'] < 1e-9 and zc.get('planes', 0) >= 8)
    chk(f'③h Tellegen Σ I²R = I_전체 (상대 {j.get("power_identity_rel")})',
        isinstance(j.get('power_identity_rel'), float) and j['power_identity_rel'] < 1e-9)
    ok_dir = all(e['va'] >= e['vb'] for e in E)
    chk('③i 방향 — a = 위쪽 전위 (V_a ≥ V_b · 전류는 a → b)', ok_dir and bool(E))
    ok_pos = True
    for e in E:
        for key, idk in (('a', 'ia'), ('b', 'ib')):
            nr = nrows[e[idk]]
            want = [float(nr['x']) * 1000, float(nr['y']) * 1000, float(nr['z']) * 1000]
            ok_pos &= all(abs(u - v) < 1e-6 for u, v in zip(e[key], want))
            ok_pos &= abs(e['r' + key] - float(nr['radius']) * 1000) < 1e-6
    chk('③j 위치 · 반경 = 덤프 노드 × scale (µm · 뷰어 좌표)', ok_pos and bool(E))
    d3 = c.get(f'/results/{cid}/3d-data').get_json(silent=True) or {}
    P = {p['id']: p for p in (d3.get('particles') or [])}
    chk('③k 위치가 3d-data 의 그 입자와 같다 (반올림 0.01 µm 안)',
        bool(P) and bool(E) and all(all(abs(P[e[idk]][ax] - e[key][k]) <= 0.006 for k, ax in enumerate('xyz'))
                        for e in E for key, idk in (('a', 'ia'), ('b', 'ib'))))

    s, j = get(f'/results/{cid}/network-current?channel=ionic&mode=hertzian&top=100000')
    E = j.get('edges') or []
    zc = j.get('zcut') or {}
    chk(f'③l top 상한 → 0 전류가 아닌 간선 전부 ({len(E)} = {len(nz)}) · 0 전류 간선 (띠 안) {j.get("n_zero_current")} 개 제외',
        s == 200 and len(E) == len(nz) and j.get('n_zero_current') == len(erows) - len(nz) and j.get('n_zero_current', 0) > 0)
    chk(f'③m 전부면 단면 몫 = 1 · 소산 몫 = 1 (평균 {zc.get("share_mean")} · {j.get("power_share")})',
        abs((zc.get('share_mean') or 0) - 1) < 1e-9 and abs((zc.get('share_min') or 0) - 1) < 1e-9
        and abs((j.get('power_share') or 0) - 1) < 1e-9)
    nw = sum(1 for e in E if e.get('w'))
    chk(f'③n 주기 경계를 넘는 간선 표지 (w) {nw} = n_wrap_returned {j.get("n_wrap_returned")} · 대각 wrap 이 있어 그린 몫 < 1 '
        f'({zc.get("drawn_share_mean")})', nw > 0 and nw == j.get('n_wrap_returned')
        and 0 < (zc.get('drawn_share_mean') or 0) < 1 - 1e-6)
    box = j.get('box') or {}
    chk(f'③o 상자 = input_params × scale ({box})', abs(box.get('x', 0) - 3.92) < 1e-9 and abs(box.get('y', 0) - 3.92) < 1e-9)
    payload_all = j

    s, j = get(f'/results/{cid}/network-current?channel=electronic')
    chk(f'③p 전자 (AM–AM) · 기본 top · Hertz → 200 · AM 반경 0.6 µm ({s} · {len(j.get("edges") or [])})',
        s == 200 and j.get('channel') == 'electronic' and j.get('mode') == 'hertzian' and j.get('top') == 5000
        and len(j.get('edges') or []) > 0 and all(abs(e['ra'] - 0.6) < 1e-9 for e in j['edges']))
    s, j = get(f'/results/{cid}/network-current?channel=ionic&mode=physics&top=3')
    chk(f'③q Physics (민감도) 모드도 같은 덤프에서 ({s} · {j.get("mode")})', s == 200 and j.get('mode') == 'physics' and len(j.get('edges') or []) == 3)
    for q, why in (('channel=thermal', '열 채널은 이 보기 범위 밖'), ('mode=bogus', '모드'), ('top=abc', 'top 정수 아님')):
        s, j = get(f'/results/{cid}/network-current?{q}')
        chk(f'③r {q} → 400 ({why} · {s} · {j.get("error")})', s == 400 and j.get('ok') is False)

    s, j = get(f'/results/{cid}/network-current')
    sc = j.get('sigma_check') or {}
    chk(f'③s 게시 σ 대조 — 같은 해 (match · {sc.get("published")} · {sc.get("dump")})', sc.get('match') is True)
    gen = j.get('generation') or {}
    chk(f'③t 세대 대조 — 덤프 run id = 활성 도장 run id ({gen.get("dump_network_run_id")} · {gen.get("active_network_run_id")})',
        gen.get('match') is True and gen.get('dump_network_run_id') == rid and not gen.get('problem'))

    cid_t = '261007_000003_tamper'
    rdt = make(cid_t)
    p = os.path.join(rdt, 'network_conductivity_hertzian.json')
    d = json.load(open(p))
    d['sigma_full'] = round(d['sigma_full'] * 1.02, 8)
    with open(p, 'w') as f:
        json.dump(d, f)
    s, j = get(f'/results/{cid_t}/network-current')
    chk('③u 게시 σ 가 덤프 해와 다르면 match False (그림 = 다른 해)', s == 200 and (j.get('sigma_check') or {}).get('match') is False)
    cid_g = '261007_000004_regen'
    rdg = make(cid_g)
    import pipeline_service as ps
    ps.stamp_network_provenance(rdg, '20261008T000000-newgen', {}, 'success', argv={'type_map': TYPE_MAP, 'scale': '1000', 'contact_mode': 'both'})
    with open(os.path.join(rdg, 'full_metrics.json'), 'w') as f:
        json.dump({'network_run_id': '20261008T000000-newgen'}, f)
    s, j = get(f'/results/{cid_g}/network-current')
    chk('③v 활성 망 세대가 덤프 세대와 다르면 generation.match False', s == 200 and (j.get('generation') or {}).get('match') is False)

    folder = '보관/케이스 a'
    tgt = os.path.join(ar, folder)
    shutil.copytree(rd, tgt)
    shutil.copy2(os.path.join(up, cid, 'meta.json'), os.path.join(tgt, 'meta.json'))
    from urllib.parse import quote
    s, j = get('/archive/results/' + quote(folder) + '/network-current?channel=ionic&mode=hertzian&top=100000')
    chk(f'③w 보관 경로도 같은 자료 ({s} · 간선 {len(j.get("edges") or [])})', s == 200 and j.get('edges') == payload_all.get('edges'))
    s, j = get('/archive/results/../../etc/network-current')
    chk(f'③x 보관 경로 탈출 거부 ({s})', s == 404)
    return payload_all


# ══════════════════════════════════════════════════════════════════════════════
#  ④ 뷰어 (node)
# ══════════════════════════════════════════════════════════════════════════════
JS_NAMES = ('netCurrentUrl', 'netCurrentWrap', 'netCurrentLogRange', 'netCurrentT', 'netCurrentPct', 'netCurrentTicks',
            'netCurrentColorbarSpec', 'netCurrentControlsHtml', 'netCurrentLegendHtml', 'netCurrentErrorHtml', 'jeEscH', 'jetColor')


def section_viewer(payload_all):
    print('[④] 뷰어 — DEM 드롭다운 · 함수 (node)')
    js = open(VIEWER_JS, encoding='utf-8').read()
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    sels = re.findall(r'<select id="view-mode".*?</select>', bc, re.S)
    chk('④a 조작판 두 개 (MPM · DEM) 의 View Mode', len(sels) == 2, str(len(sels)))
    mpm_sel, dem_sel = (sels + ['', ''])[:2]
    m = re.search(r'<option value="net_current">([^<]*)</option>', dem_sel)
    chk(f'④b DEM 드롭다운에 net_current ("전류 흐름") · MPM 드롭다운엔 없음 ({m.group(1) if m else None})',
        m is not None and '전류 흐름' in m.group(1) and 'net_current' not in mpm_sel)
    try:
        avm = js_fn(js, 'applyViewMode')
    except (ValueError, AssertionError):
        avm = ''
    chk('④c 모드를 바꿀 때마다 전류 그림을 치운다 (applyViewMode 머리에서 netCurrentTeardown(state))',
        re.search(r'netCurrentTeardown\(state\);', avm[:6000]) is not None)
    chk("④d applyViewMode 가 'net_current' 를 applyNetCurrentMode 로 보낸다",
        re.search(r"mode === 'net_current'\)\s*\{\s*applyNetCurrentMode\(state\);\s*return;", avm) is not None)
    try:
        anm = js_fn(js, 'applyNetCurrentMode')
        rnc = js_fn(js, 'renderNetCurrent')
        ntd = js_fn(js, 'netCurrentTeardown')
    except (ValueError, AssertionError):
        anm = rnc = ntd = ''
    chk('④e 늦은 응답 무시 — 토큰 · 지금 모드를 보고 그린다 (옛 옵션 · 다른 모드 위에 그리지 않는다)',
        "state.viewMode !== 'net_current'" in anm and '_netCurToken' in anm and '_netCurToken' in ntd)
    chk('④f 그리기 = 주기 경계 간선 생략 (netCurrentWrap) · 단면 뷰 다시 적용 (applyClip) · 범례 갱신',
        'netCurrentWrap(' in rnc and 'applyClip' in rnc and 'netCurrentLegendHtml(' in rnc)
    chk('④g 범례의 컬러바 ⬇ = 논문용 컬러바 PNG (exportColorbarPNG · netCurrentColorbarSpec)',
        'exportColorbarPNG(netCurrentColorbarSpec(' in js)
    try:
        import network_current as _ncur
        td = _ncur.TOP_DEFAULT
    except Exception:                                            # noqa: BLE001 — 옛 코드 (모듈 없음)
        td = None
    m_def = re.search(r"_netCurOpt = \{ channel: 'ionic', mode: 'hertzian', top: (\d+)", anm)
    chk(f'④g2 뷰어 기본 top = 경로 기본 TOP_DEFAULT ({m_def.group(1) if m_def else None} · {td})',
        m_def is not None and td is not None and int(m_def.group(1)) == td)
    if not (payload_all and payload_all.get('edges')):
        chk('④h–④y node 시험 — 경로 자료 (③) 가 없어 건너뜀', False)
        return

    parts, miss = [], []
    for n in JS_NAMES:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    for n in ('NETCUR_CHANNELS', 'NETCUR_MODES'):
        try:
            parts.append(js_const(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    m_tops = re.search(r'const NETCUR_TOPS = \[[^\]]*\];', js)
    if not chk(f'④h viewer3d.js 에서 함수 · 상수를 잘라 냈다 (없음 {miss})', not miss and m_tops is not None):
        return
    pay = copy.deepcopy(payload_all)
    pay5 = dict(pay, edges=pay['edges'][:5], top=5, n_returned=5)
    script = '\n'.join(parts) + '\n' + m_tops.group(0) + '\n' + r"""
const PAY = __PAY__, PAY5 = __PAY5__;
const out = {};
out.url = [
  netCurrentUrl('/results/abc/3d-data', {channel: 'ionic', mode: 'hertzian', top: 2000}),
  netCurrentUrl('/archive/results/보관/케이스 a/3d-data', {channel: 'electronic', mode: 'physics', top: 500}),
  netCurrentUrl('/results/abc/3d-data?x=1', {channel: 'ionic', mode: 'hertzian', top: 7}),
];
const hx = PAY.box.x / 2, hy = PAY.box.y / 2;
out.wrapJs = PAY.edges.map(e => netCurrentWrap(e.a, e.b, hx, hy));
out.wrapSrv = PAY.edges.map(e => !!e.w);
out.wrapFix = [netCurrentWrap([0, 0, 0], [3, 0, 0], 2, 2), netCurrentWrap([0, 0, 0], [1.9, 1.9, 5], 2, 2),
               netCurrentWrap([0, 0, 0], [0, -2.5, 0], 2, 2), netCurrentWrap([0, 0, 0], [0, 0, 99], 2, 2)];
out.range = netCurrentLogRange(PAY.edges);
out.rangeZero = netCurrentLogRange([{s: 0}, {s: 0.01}, {s: 0.1}]);
out.rangeNone = netCurrentLogRange([{s: 0}]);
out.t = [netCurrentT(0.01, -2, -1), netCurrentT(0.1, -2, -1), netCurrentT(10 ** -1.5, -2, -1), netCurrentT(1e-5, -2, -1), netCurrentT(5, -2, -1)];
out.pct = [netCurrentPct(0.196), netCurrentPct(0.01), netCurrentPct(0.0031), netCurrentPct(1), netCurrentPct(0.00047)];
out.ticksDec = netCurrentTicks(-4, -1);
out.ticksNarrow = netCurrentTicks(Math.log10(0.0031), Math.log10(0.0143));
out.ticksCrowd = netCurrentTicks(Math.log10(0.00157), Math.log10(0.0143));
out.spec = netCurrentColorbarSpec(PAY5, {channel: 'ionic', mode: 'hertzian', top: 5}, -2.5, -1);
const st = {nDrawn: 4, nWrapSkipped: 1, lo: -2.5, hi: -1};
out.leg = netCurrentLegendHtml(PAY5, {channel: 'ionic', mode: 'hertzian', top: 5, arrows: false}, st);
const bad = JSON.parse(JSON.stringify(PAY5));
bad.sigma_check.match = false; bad.generation.match = false; bad.generation.dump_network_run_id = '<b>x</b>';
out.legBad = netCurrentLegendHtml(bad, {channel: 'ionic', mode: 'hertzian', top: 5}, st);
const gp = JSON.parse(JSON.stringify(PAY5));
gp.generation = {match: false, dump_network_run_id: 'r1', active_network_run_id: 'r1', problem: 'full_metrics 세대 &lt;x&gt; ≠ 도장'};
out.legGenProblem = netCurrentLegendHtml(gp, {channel: 'ionic', mode: 'hertzian', top: 5}, st);
const gn = JSON.parse(JSON.stringify(PAY5));
gn.generation = {match: null, dump_network_run_id: null, active_network_run_id: null, problem: '', note: '도장 없는 케이스로 만든 덤프 — 덤프 세대 미확인'};
out.legGenUnknown = netCurrentLegendHtml(gn, {channel: 'ionic', mode: 'hertzian', top: 5}, st);
const ph = JSON.parse(JSON.stringify(PAY5)); ph.mode = 'physics'; ph.channel = 'electronic';
out.legPh = netCurrentLegendHtml(ph, {channel: 'electronic', mode: 'physics', top: 5}, {nDrawn: 5, nWrapSkipped: 0, lo: -2, hi: -1});
out.err = netCurrentErrorHtml({error: 'no_dump', message: 'm<script>', how_to: 'python3 scripts/network_current.py dump /r/x'});
out.tops = NETCUR_TOPS;
console.log(JSON.stringify(out));
""".replace('__PAY__', json.dumps(pay, ensure_ascii=False)).replace('__PAY5__', json.dumps(pay5, ensure_ascii=False))
    res = run_node(script)
    if not chk('④i node 실행', res is not None):
        return
    chk('④j URL — 실 · 보관 경로 /3d-data → /network-current · 질의문은 버리고 채널 · 모드 · top', res['url'] == [
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=2000',
        '/archive/results/보관/케이스 a/network-current?channel=electronic&mode=physics&top=500',
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=7'], repr(res['url']))
    chk(f'④k 주기 경계 함수 = 서버 표지 (간선 {len(res["wrapJs"])} 개 전부 같은 답 · wrap {sum(res["wrapSrv"])})',
        res['wrapJs'] == res['wrapSrv'] and sum(res['wrapSrv']) > 0)
    chk(f'④l 주기 경계 고정 예 (x 반폭 초과 · 대각 안 · y 반폭 초과 · z 는 무관) {res["wrapFix"]}', res['wrapFix'] == [True, False, True, False])
    lo, hi = res['range'] or (None, None)
    ss = [e['s'] for e in payload_all['edges']]
    chk(f'④m log 범위 = 그 간선들의 log10 (최소 · 최대) ({lo} · {hi})',
        lo is not None and abs(lo - math.log10(min(ss))) < 1e-12 and abs(hi - math.log10(max(ss))) < 1e-12)
    chk(f'④n log 범위는 0 전류를 버린다 · 0 만 있으면 null ({res["rangeZero"]} · {res["rangeNone"]})',
        res['rangeZero'] is not None and abs(res['rangeZero'][0] + 2) < 1e-12 and abs(res['rangeZero'][1] + 1) < 1e-12
        and res['rangeNone'] is None)
    chk(f'④o 색 · 굵기 축 t = log 정규화 · [0, 1] 로 자른다 {res["t"]}',
        [round(x, 9) for x in res['t']] == [0.0, 1.0, 0.5, 0.0, 1.0])
    chk(f'④p 백분율 표기 (0 꼬리 없음) {res["pct"]}', res['pct'] == ['19.6 %', '1 %', '0.31 %', '100 %', '0.047 %'])
    td = res['ticksDec']
    chk(f'④q 눈금 — 10 배 간격 · 끝 포함 · 0..1 · 라벨 % ({[t["label"] for t in td]})',
        [t['label'] for t in td] == ['0.01 %', '0.1 %', '1 %', '10 %'] and all(0 <= t['p'] <= 1 for t in td)
        and abs(td[0]['p']) < 1e-12 and abs(td[-1]['p'] - 1) < 1e-12)
    tn = res['ticksNarrow']
    chk(f'④r 좁은 범위 (한 자릿수 안) 도 끝 두 개 + 안쪽 1 · 2 · 5 눈금 ({[t["label"] for t in tn]})',
        len(tn) >= 3 and tn[0]['label'] == '0.31 %' and tn[-1]['label'] == '1.4 %' and '1 %' in [t['label'] for t in tn]
        and all(0 <= t['p'] <= 1 for t in tn))
    tc = res['ticksCrowd']
    ps_ = [t['p'] for t in tc]
    chk(f'④r2 끝 라벨과 겹치는 안쪽 눈금은 뺀다 (real14 상위 10000 범위 0.16–1.4 % — 옛 판은 0.2 % 가 0.16 % 에 붙었다) '
        f'({[t["label"] for t in tc]})',
        '0.2 %' not in [t['label'] for t in tc] and all(b - a >= 0.12 - 1e-12 for a, b in zip(ps_, ps_[1:])))
    sp = res['spec'] or {}
    chk('④s 컬러바 스펙 = jet · 감마 없음 (튜브 색과 같은 사상) · 영문 제목 (채널 · Hertz FULL · 1 V probe) · 눈금',
        sp.get('map') == 'jet' and not sp.get('gamma') and 'Hertz FULL' in sp.get('title', '') and '1 V probe' in sp.get('title', '')
        and 'ionic' in sp.get('title', '') and len(sp.get('ticks') or []) >= 2, repr(sp)[:300])
    leg = res['leg']
    pct5 = res['pct']  # noqa: F841
    chk('④t 범례 — 채널 (이온 · SE–SE) · Hertz FULL · "1 V 프로브 해 · 상위 5 간선 = 전체 전류의 x %" · 모델 접촉망 풀이 표지',
        '이온' in leg and 'SE–SE' in leg and 'Hertz FULL' in leg
        and re.search(r'1 V 프로브 해 · 상위 5 간선 = 전체 전류의 [0-9.]+ %', leg) is not None
        and '접촉망 풀이' in leg and '측정 전류' in leg, leg[:400])
    chk('④u 범례 — 주기 경계 생략 수 · 소산 몫 · 검산 · 게시 σ 같은 해 · 컬러바 · 화살표 · 조작 (채널 · top · 모드)',
        '주기 경계' in leg and '1 간선' in leg and '소산' in leg and '검산' in leg and '게시 σ 와 같은 해' in leg
        and 'id="netcur-cbar"' in leg and 'id="netcur-arrows"' in leg
        and 'id="netcur-channel"' in leg and 'id="netcur-top"' in leg and 'id="netcur-mode"' in leg)
    lb = res['legBad']
    chk('④v 게시 σ 다름 · 세대 다름 → ⚠ 두 줄 · 서버 문자열은 이스케이프', '⚠ 게시 σ 와 다른 해' in lb and '⚠ 덤프 세대' in lb
        and '<b>x</b>' not in lb and '&lt;b&gt;x&lt;/b&gt;' in lb)
    lg = res['legGenProblem']
    chk('④v2 세대 id 는 같고 활성 세대가 무효 → "활성 망 세대 무효 — 사유" (≠ 줄을 지어내지 않는다)',
        '⚠ 활성 망 세대 무효' in lg and '⚠ 덤프 세대' not in lg and '&amp;lt;x&amp;gt;' in lg)
    lu = res['legGenUnknown']
    chk('④v3 세대 미확인 (도장 없는 케이스) → ⚠ 미확인 줄 (같은 해라고 말하지 않는다)',
        '⚠ 도장 없는 케이스로 만든 덤프 — 덤프 세대 미확인' in lu and '⚠ 활성 망 세대 무효' not in lu)
    lp = res['legPh']
    chk('④w Physics 모드 = 민감도 표지 · 전자 = AM–AM', '민감도' in lp and 'AM–AM' in lp and 'Physics FULL' in lp)
    er = res['err']
    chk('④x 덤프 없음 범례 = 만드는 명령 (code) · 서버 문자열 이스케이프 · 다시 불러오기 버튼 (같은 모드를 다시 골라도 change 가 안 난다)',
        'scripts/network_current.py dump /r/x' in er and '<script>' not in er and 'id="netcur-retry"' in er)
    try:
        wl = js_fn(js, 'netCurrentWireLegend')
    except (ValueError, AssertionError):
        wl = ''
    chk("④x2 다시 불러오기 = applyNetCurrentMode (오류는 캐시하지 않는다 — 다시 fetch)",
        re.search(r"on\('netcur-retry', 'click', \(\) => applyNetCurrentMode\(state\)\)", wl) is not None
        and 'cache[url] = res.body' in anm and anm.index('netCurrentErrorHtml') < anm.index('cache[url] = res.body'))
    chk(f'④y top 고르기 {res["tops"]}', res['tops'] == [500, 1000, 2000, 5000, 10000, 20000])


def section_registration():
    print('[⑤] check_all 배선')
    s = open(CHECK_ALL, encoding='utf-8').read()
    chk('⑤a scripts/check_all.sh 가 이 시험을 돈다', 'webapp/test_network_current_view.py' in s)


def main():
    tmp = tempfile.mkdtemp(prefix='netcur_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
            os.makedirs(os.environ[k], exist_ok=True)
        sys.path.insert(0, SCRIPTS)
        section_bit_identity(tmp)
        pub = rid = None
        try:
            pub, rid = section_tool(tmp)
        except Exception as e:                                   # noqa: BLE001 — 옛 코드 (도구 없음) 에서도 나머지를 돈다
            chk('② 도구 절 실행', False, f'{type(e).__name__}: {e}')
        if not pub or not os.path.isdir(os.path.join(pub, DUMP)):
            # 도구가 없거나 실패했다 → 같은 CLI 의 원 덤프 (--dump-raw-dir · .csv · manifest 없음) 로 경로 절을 돈다 (옛 코드에서도 경로 결함을 하나씩 본다)
            pub = os.path.join(tmp, 'pub_fallback')
            rid = publish_case(pub)
            run_cli(pub, os.path.join(tmp, 'pub_fallback_side'), dump=os.path.join(pub, DUMP))
        payload = {}
        try:
            payload = section_routes(tmp, pub, rid)
        except Exception as e:                                   # noqa: BLE001
            chk('③ 경로 절 실행', False, f'{type(e).__name__}: {e}')
        section_viewer(payload)
        section_registration()
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

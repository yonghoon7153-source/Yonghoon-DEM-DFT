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
     ★ 10-07 (1저자 결정 · 웹앱 묶음 #17) — 색 · 굵기 = 접촉 전류 밀도 j (A cm⁻²) · 컬러바 @1V + @1C · 옛 몫 (|I|/I_전체 %) 표시 없음.
       전류 밀도 자체 (단위 · 손 계산 · @1C 환산) 는 webapp/test_net_current_density.py.
  ⑥ 고르기 (10-08 · 1저자 Q1 · Q2 권고대로) — 전류 몫 50 · 80 · 95 % (독립 재계산과 같은 개수 · 가장 적은 개수) · 전부 · 압축 꼴 (값 · 순서 그대로 ·
     절반 이하 크기) · 정수 고르기 = 옛 키 + selection · 잘못된 이름 400 · 단면 없는 해 = 경로 기본 + 사유 · 경로 · CLI.
  ④c 뷰어 고르기 칸 (개수 · 그 케이스보다 작은 상위 N 만) · 압축 꼴 풀기 · 색 위쪽 (최대 · p99 · p95 · 범례 = 숫자 셋 · '≥' · ▲ 없음) · 가볍게 그리기 ·
     받은 자료 기억 4 개 · 기본 = 전류 50 %.

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
JS_NAMES = ('netCurrentUrl', 'netCurrentWrap', 'netCurrentLogRange', 'netCurrentT', 'netCurrentPct', 'netCurrentFmtJ', 'netCurrentTicks',
            'netCurrentFrame', 'netCurrentColorbarSpec', 'netCurrentControlsHtml', 'netCurrentTopOptions', 'netCurrentLegendHtml',
            'netCurrentErrorHtml', 'jeEscH', 'jetColor')
NETCUR_CONST_NAMES = ('NETCUR_TOPS', 'NETCUR_WIDTHS', 'NETCUR_SHARES', 'NETCUR_CAPS')   # 조작판이 쓰는 한 줄 상수 (10-08 고르기 · 위쪽 더함)


def netcur_consts(js, names=NETCUR_CONST_NAMES):
    """viewer3d.js 의 전류 흐름 한 줄 상수 — 있는 것만 (옛 코드엔 없는 것도 있다)."""
    return [m.group(0) for m in (re.search(r'const ' + n + r' = [^;]*;', js) for n in names) if m]


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
        td = getattr(_ncur, 'VIEWER_DEFAULT', None)
    except Exception:                                            # noqa: BLE001 — 옛 코드 (모듈 없음)
        td = None
    #  10-08 1저자 Q2 *"권고대로"* — 뷰어 기본 = 전류 50 % (서버 VIEWER_DEFAULT).  옛 판은 경로 기본 TOP_DEFAULT (5000) 와 대조했다.
    m_def = re.search(r"_netCurOpt = \{ channel: 'ionic', mode: 'hertzian', top: '([^']+)'", anm)
    chk(f'④g2 뷰어 기본 top = 서버 VIEWER_DEFAULT (전류 50 %) ({m_def.group(1) if m_def else None} · {td})',
        m_def is not None and td is not None and m_def.group(1) == td)
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
    m_tops = re.search(r'const NETCUR_TOPS = \[[^\]]*\];', js)          # 나머지 한 줄 상수 (굵기 · 전류 몫 · 위쪽) = netcur_consts
    if not chk(f'④h viewer3d.js 에서 함수 · 상수를 잘라 냈다 (없음 {miss})', not miss and m_tops is not None):
        return
    pay = copy.deepcopy(payload_all)
    pay5 = dict(pay, edges=pay['edges'][:5], top=5, n_returned=5)
    script = '\n'.join(parts + netcur_consts(js)) + '\n' + r"""
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
out.rangeZero = netCurrentLogRange([{j: 0}, {j: 0.01}, {j: 0.1}]);
out.rangeNone = netCurrentLogRange([{j: 0}]);
out.t = [netCurrentT(0.01, -2, -1), netCurrentT(0.1, -2, -1), netCurrentT(10 ** -1.5, -2, -1), netCurrentT(1e-5, -2, -1), netCurrentT(5, -2, -1)];
out.pct = [netCurrentPct(0.196), netCurrentPct(0.01), netCurrentPct(0.0031), netCurrentPct(1), netCurrentPct(0.00047)];
out.ticksDec = netCurrentTicks(-4, -1, netCurrentPct);
out.ticksNarrow = netCurrentTicks(Math.log10(0.0031), Math.log10(0.0143), netCurrentPct);
out.ticksCrowd = netCurrentTicks(Math.log10(0.00157), Math.log10(0.0143), netCurrentPct);
out.spec = netCurrentColorbarSpec(PAY5, {channel: 'ionic', mode: 'hertzian', top: 5}, -2.5, -1, '1V');
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
    ss = [e['j'] for e in payload_all['edges'] if e.get('j')]
    chk(f'④m log 범위 = 그 간선들의 log10 j — 접촉 전류 밀도 (최소 · 최대) ({lo} · {hi})',
        lo is not None and bool(ss) and abs(lo - math.log10(min(ss))) < 1e-12 and abs(hi - math.log10(max(ss))) < 1e-12)
    chk(f'④n log 범위는 j = 0 을 버린다 · 0 만 있으면 null ({res["rangeZero"]} · {res["rangeNone"]})',
        res['rangeZero'] is not None and abs(res['rangeZero'][0] + 2) < 1e-12 and abs(res['rangeZero'][1] + 1) < 1e-12
        and res['rangeNone'] is None)
    chk(f'④o 색 · 굵기 축 t = log 정규화 · [0, 1] 로 자른다 {res["t"]}',
        [round(x, 9) for x in res['t']] == [0.0, 1.0, 0.5, 0.0, 1.0])
    chk(f'④p 백분율 표기 (0 꼬리 없음) {res["pct"]}', res['pct'] == ['19.6 %', '1 %', '0.31 %', '100 %', '0.047 %'])
    td = res['ticksDec']
    chk(f'④q 눈금 배치 — 10 배 간격 · 끝 포함 · 0..1 · 라벨 함수를 넘긴다 (여기 % = netCurrentPct) ({[t["label"] for t in td]})',
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
    chk('④s 컬러바 스펙 = jet · 감마 없음 (튜브 색과 같은 사상) · 영문 제목 (접촉 전류 밀도 A cm⁻² · 채널 · Hertz FULL · @1V probe) · 눈금',
        sp.get('map') == 'jet' and not sp.get('gamma') and 'Hertz FULL' in sp.get('title', '') and '@1V probe' in sp.get('title', '')
        and 'Contact current density' in sp.get('title', '') and 'ionic' in sp.get('title', '') and len(sp.get('ticks') or []) >= 2,
        repr(sp)[:300])
    leg = res['leg']
    chk('④t 범례 — 채널 (이온 · SE–SE) · Hertz FULL · 접촉 전류 밀도 (A cm⁻² · @1V · @1C) · 상위 5 접촉 · 옛 몫 문구 없음 · 모델 접촉망 풀이 표지',
        '이온' in leg and 'SE–SE' in leg and 'Hertz FULL' in leg and '접촉 전류 밀도' in leg and 'A cm⁻²' in leg
        and '@1V' in leg and '@1C' in leg and '상위 5' in leg and '전체 전류의' not in leg
        and '접촉망 풀이' in leg and '측정 전류' in leg, leg[:400])
    chk('④u 범례 — 주기 경계 생략 수 · 소산 몫 · 검산 · 게시 σ 같은 해 · 컬러바 둘 (@1V · @1C) · 화살표 · 조작 (채널 · top · 모드)',
        '주기 경계' in leg and '1 접촉' in leg and '소산' in leg and '검산' in leg and '게시 σ 와 같은 해' in leg
        and 'id="netcur-cbar-1v"' in leg and 'id="netcur-cbar-1c"' in leg and 'id="netcur-arrows"' in leg
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


def section_viewer_width():
    """④z 관 굵기 — 1저자 10-08 *"이거 크기 좀더 얇게 가능한가?"* (전자 AM–AM 상위 20000 · 관이 굵어 망이 뭉쳐 보인다).
    반경 = 굵기 배율 × (0.10 + 0.40 t) × 망 입자 반경 중앙값 — 배율 1 = 옛 그림 그대로 (rMin 0.10 · rMax 0.50 r_ref) · 고르기 ×1 · ×0.5 · ×0.25 · ×0.1 ·
    잘못된 배율 (0 · 음수 · NaN · 없음) = 1 · 바꾸면 다시 받지 않고 다시 그린다 (같은 자료) · 화살표도 같은 반경을 따른다."""
    print('[④z] 뷰어 — 관 굵기 고르기 (node)')
    js = open(VIEWER_JS, encoding='utf-8').read()
    parts, miss = [], []
    for n in ('netCurrentRadius', 'netCurrentControlsHtml', 'netCurrentTopOptions'):
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    m_w = re.search(r'const NETCUR_WIDTHS = \[[^\]]*\];', js)
    m_tops = re.search(r'const NETCUR_TOPS = \[[^\]]*\];', js)
    if not chk(f'④z1 viewer3d.js 에 netCurrentRadius · NETCUR_WIDTHS (없음 {miss} · 상수 {m_w is not None})',
               not miss and m_w is not None and m_tops is not None):
        return
    script = '\n'.join(parts + netcur_consts(js)) + '\n' + r"""
const out = {};
out.widths = NETCUR_WIDTHS;
out.r1 = [netCurrentRadius(0, 2, 1), netCurrentRadius(1, 2, 1), netCurrentRadius(0.5, 2, 1)];
out.rq = [netCurrentRadius(0, 2, 0.25), netCurrentRadius(1, 2, 0.25)];
out.rBad = [netCurrentRadius(1, 2, 0), netCurrentRadius(1, 2, -1), netCurrentRadius(1, 2, NaN), netCurrentRadius(1, 2, undefined),
            netCurrentRadius(1, 2, 'x')];
out.ctl = netCurrentControlsHtml({channel: 'electronic', mode: 'physics', top: 20000, width: 0.25});
out.ctlDef = netCurrentControlsHtml({channel: 'ionic', mode: 'hertzian', top: 5000});
console.log(JSON.stringify(out));
"""
    res = run_node(script)
    if not chk('④z2 node 실행', res is not None):
        return
    chk(f'④z3 굵기 고르기 = ×1 · ×0.5 · ×0.25 · ×0.1 ({res["widths"]})', res['widths'] == [1, 0.5, 0.25, 0.1])
    chk(f'④z4 배율 1 = 옛 그림 그대로 (t 0 → 0.10 r_ref · t 1 → 0.50 r_ref · t 0.5 → 0.30 r_ref) {res["r1"]}',
        [round(x, 12) for x in res['r1']] == [0.2, 1.0, 0.6])
    chk(f'④z5 배율 0.25 = 반경 4 분의 1 {res["rq"]}', [round(x, 12) for x in res['rq']] == [0.05, 0.25])
    chk(f'④z6 잘못된 배율 (0 · 음수 · NaN · 없음 · 문자) = 1 {res["rBad"]}', [round(x, 12) for x in res['rBad']] == [1.0] * 5)
    ctl = res['ctl']
    chk('④z7 조작판에 굵기 고르기 (id netcur-width) · 고른 값 표시 (×0.25 selected) · 기본 = ×1',
        'id="netcur-width"' in ctl and re.search(r'<option value="0\.25" selected>[^<]*0\.25', ctl) is not None
        and re.search(r'<option value="1" selected>', res['ctlDef']) is not None, ctl[:300])
    try:
        rnc = js_fn(js, 'renderNetCurrent')
        wl = js_fn(js, 'netCurrentWireLegend')
        anm = js_fn(js, 'applyNetCurrentMode')
    except (ValueError, AssertionError):
        rnc = wl = anm = ''
    chk('④z8 그리기 = netCurrentRadius(t, rRef, opt.width) (관 · 화살표 같은 반경)',
        re.search(r'netCurrentRadius\(\s*t\s*,\s*rRef\s*,\s*opt\.width\s*\)', rnc) is not None
        and 'rMin + (rMax - rMin) * t' not in rnc)
    chk('④z9 굵기를 바꾸면 다시 받지 않고 다시 그린다 (renderNetCurrent · 같은 자료)',
        re.search(r"on\('netcur-width', 'change', ev => \{ opt\.width = \+ev\.target\.value; if \(pay\) renderNetCurrent\(state, pay\); \}\)",
                  wl) is not None)
    chk("④z10 기본 옵션에 width: 1 (top = 숫자 또는 전류 몫 이름 · 10-08 위쪽 cap: 'max' 더함)",
        re.search(r"_netCurOpt = \{ channel: 'ionic', mode: 'hertzian', top: (?:\d+|'share\d+'), arrows: false, width: 1, scale: 'log', "
                  r"cap: 'max' \}", anm) is not None)


def section_viewer_scale():
    """④s 선형 눈금 — 1저자 10-08 *"우리 전류밀도 값들 두개 로그스케일 말고 그냥 스케일로 그림 표현되게 하고 범례도 이등분 되게"*.
    고르기 log (기본 · 옛 그림 그대로) · 선형 — 선형이면 색 · 굵기 t = (j − 최소) / (최대 − 최소) · 컬러바 눈금 셋 = 최소 · (최소 + 최대) / 2 · 최대
    (@1C 는 × I_1C / I_1V) · 범례가 '선형' 과 가운데 값을 적는다."""
    print('[④s] 뷰어 — 선형 눈금 · 이등분 범례 (node)')
    js = open(VIEWER_JS, encoding='utf-8').read()
    names = ('netCurrentRange', 'netCurrentTv', 'netCurrentLogRange', 'netCurrentT', 'netCurrentFmtJ', 'netCurrentTicks', 'netCurrentFrame',
             'netCurrentColorbarSpec', 'netCurrentControlsHtml', 'netCurrentTopOptions', 'netCurrentLegendHtml', 'netCurrentPct', 'jeEscH',
             'jetColor')
    parts, miss = [], []
    for n in names:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    for n in ('NETCUR_CHANNELS', 'NETCUR_MODES'):
        try:
            parts.append(js_const(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    consts = netcur_consts(js)
    if not chk(f'④s1 viewer3d.js 에 netCurrentRange · netCurrentTv (없음 {miss})',
               not miss and any('NETCUR_TOPS' in c for c in consts) and any('NETCUR_WIDTHS' in c for c in consts)):
        return
    script = '\n'.join(parts + consts) + '\n' + r"""
const E = [{j: 1}, {j: 2}, {j: 5}, {j: 0}];
const PAY = {channel: 'ionic', mode: 'hertzian', n_returned: 3, n_perc_edges: 3, edges: E, power_share: 0.5, power_identity_rel: 0,
             density: {c1: {status: 'ok', factor: 10, Q_areal_mAh_cm2: 3}}, zcut: null, sigma_check: {}, generation: {match: true}};
const out = {};
out.rLin = netCurrentRange(E, 'linear'); out.rLog = netCurrentRange(E, 'log'); out.rLog0 = netCurrentLogRange(E);
out.tLin = [netCurrentTv(3, 1, 5, 'linear'), netCurrentTv(0.5, 1, 5, 'linear'), netCurrentTv(9, 1, 5, 'linear'), netCurrentTv(0, 1, 5, 'linear'),
            netCurrentTv(2, 2, 2, 'linear')];
out.tLog = [netCurrentTv(10, 0, 2, 'log'), netCurrentT(10, 0, 2)];
const lin = {channel: 'ionic', mode: 'hertzian', top: 3, scale: 'linear'}, lg = {channel: 'ionic', mode: 'hertzian', top: 3};
out.sLin = netCurrentColorbarSpec(PAY, lin, 1, 5, '1V'); out.sLin1C = netCurrentColorbarSpec(PAY, lin, 1, 5, '1C');
out.sLog = netCurrentColorbarSpec(PAY, lg, 0, Math.log10(5), '1V');
out.legLin = netCurrentLegendHtml(PAY, lin, {nDrawn: 3, nWrapSkipped: 0, lo: 1, hi: 5, scale: 'linear'});
out.legLog = netCurrentLegendHtml(PAY, lg, {nDrawn: 3, nWrapSkipped: 0, lo: 0, hi: Math.log10(5)});
out.ctlLin = netCurrentControlsHtml(lin); out.ctlDef = netCurrentControlsHtml(lg);
out.fj = [netCurrentFmtJ(1), netCurrentFmtJ(3), netCurrentFmtJ(5), netCurrentFmtJ(10), netCurrentFmtJ(30), netCurrentFmtJ(50)];
console.log(JSON.stringify(out));
"""
    res = run_node(script)
    if not chk('④s2 node 실행', res is not None):
        return
    chk(f'④s3 범위 — 선형 = j [최소, 최대] (0 은 버림) {res["rLin"]} · log = netCurrentLogRange 그대로',
        res['rLin'] == [1, 5] and res['rLog'] == res['rLog0'])
    chk(f'④s4 선형 t = (j − 최소) / (최대 − 최소) · 자름 · 0 → 0 · 한 점 → 1 {res["tLin"]} · log 는 netCurrentT 그대로',
        [round(x, 12) for x in res['tLin']] == [0.5, 0.0, 1.0, 0.0, 1.0] and res['tLog'][0] == res['tLog'][1])
    t1 = [(round(t['p'], 12), t['label']) for t in res['sLin']['ticks']]
    t2 = [t['label'] for t in res['sLin1C']['ticks']]
    fj = res['fj']
    chk(f'④s5 컬러바 선형 = 눈금 셋 (최소 · 가운데 · 최대) {t1} · @1C × 10 {t2}',
        t1 == [(0.0, fj[0]), (0.5, fj[1]), (1.0, fj[2])] and t2 == [fj[3], fj[4], fj[5]])
    chk('④s6 컬러바 글 — 선형 = "Linear colour scale" · log 는 "Log colour scale" 그대로',
        'Linear colour scale' in res['sLin']['sub'] and 'Log colour scale' not in res['sLin']['sub'] and 'Log colour scale' in res['sLog']['sub'])
    ll, lg_ = res['legLin'], res['legLog']
    chk('④s7 범례 — 선형 = "선형" · 1 … 5 A cm⁻² · 가운데 3 · log 는 "(log₁₀)" 그대로',
        '선형' in ll and '1 … 5 A cm⁻²' in ll and '가운데 3' in ll and '(log₁₀)' in lg_ and '선형 눈금' not in lg_.split('netcur-scale')[0], ll[:300])
    chk('④s8 조작판에 눈금 고르기 (id netcur-scale) · 선형 고르면 selected · 기본 = log',
        'id="netcur-scale"' in res['ctlLin'] and re.search(r'<option value="linear" selected>', res['ctlLin']) is not None
        and re.search(r'<option value="log" selected>', res['ctlDef']) is not None)
    try:
        rnc = js_fn(js, 'renderNetCurrent')
        wl = js_fn(js, 'netCurrentWireLegend')
    except (ValueError, AssertionError):
        rnc = wl = ''
    chk('④s9 그리기 = netCurrentRange(edges, sc) · netCurrentTv(e.j, lo, hi, sc) · st.scale 기록',
        'netCurrentRange(edges, sc)' in rnc and 'netCurrentTv(e.j, lo, hi, sc)' in rnc and 'scale: sc' in rnc)
    chk('④s10 눈금을 바꾸면 다시 받지 않고 다시 그린다',
        re.search(r"on\('netcur-scale', 'change', ev => \{ opt\.scale = ev\.target\.value; if \(pay\) renderNetCurrent\(state, pay\); \}\)", wl) is not None)


# ══════════════════════════════════════════════════════════════════════════════
#  ⑥ 고르기 — 전류 몫 (50 · 80 · 95 %) · 전부 · 압축 꼴.  1저자 10-08 *"애초에 상위 20000 으로만 한 이유 · 좀더 모델 최적화로 숫자
#     조절해주면 안되나?"* → Q1 · Q2 *"권고대로"* (기본 = 전류 50 %).  20000 은 근거 기록 없는 상한이었다 — real14 전자 645 접촉이면
#     1000 … 20000 이 같은 그림 · ps45 이온 35–44 만 접촉이면 5 % 만.  ⇒ 숫자를 그 케이스의 전류 분포가 정한다 (|I| 큰 순으로 세어
#     높이 32 단면 평균 전류 몫이 처음 X 에 닿는 개수).  정수 고르기 = 옛 자료 그대로 (키 selection 하나만 더함).  이름 고르기 = 압축 꼴
#     (입자 표 한 번 + 접촉 = 입자 번호 둘 + j · 값 그대로).  webapp/app.py (194 봉인) 는 고치지 않는다 — top 문자열을 그대로 넘긴다.
# ══════════════════════════════════════════════════════════════════════════════
OLD_KEYS = {'ok', 'channel', 'mode', 'top', 'scale', 'n_perc_edges', 'n_perc_nodes', 'n_returned', 'n_zero_current',
            'n_missing_position', 'n_wrap_returned', 'I_total', 'I_total_source', 'share_max', 'share_min', 'zcut', 'power_share',
            'power_identity_rel', 'sum_abs_share', 'box', 'sigma_check', 'generation', 'dump', 'probe', 'density', 'edges'}
EDGE_VIEW_KEYS = ('a', 'b', 'ra', 'rb', 'ia', 'ib', 'j')           # 뷰어가 쓰는 칸 (압축 꼴이 싣는 것)


def ref_share_ladder(raw, mode='hertzian', channel='ionic', planes=32):
    """독립 재계산 (순수 파이썬 · 덤프 CSV) — 0 아닌 전류 간선을 |I| 큰 순 (동률 id1 · id2) 으로 세며, 간선마다 단면 평균 순 흐름 / I_전체
    를 누적한다.  단면 = 전극 띠 (전류가 흐르는 V = 1 · V = 0 노드) 사이 평면 32 개 (경로 정의 그대로).  → (누적 목록 · I_전체 · 0 아닌 수)."""
    t = f'{mode}_{channel}'
    sol = json.load(open(os.path.join(raw, f'solution_{t}.json')))
    I_tot = float(sol['G_eff'])
    nodes = {int(r['id']): r for r in read_csv_rows(dump_file(raw, f'nodes_{t}'))}
    E = []
    for r in read_csv_rows(dump_file(raw, f'edges_{t}')):
        a, b = int(r['id1']), int(r['id2'])
        if a in nodes and b in nodes:
            E.append((a, b, float(r['I'])))
    inc = {}
    for a, b, I in E:
        inc[a] = inc.get(a, 0.0) + abs(I)
        inc[b] = inc.get(b, 0.0) + abs(I)
    act = {k for k, v in inc.items() if v > 1e-12 * I_tot}
    nzE = sorted((e for e in E if abs(e[2]) > 1e-12 * I_tot), key=lambda e: (-abs(e[2]), e[0], e[1]))
    zb = [float(nodes[k]['z']) for k in act if float(nodes[k]['V']) == 1.0]
    zt = [float(nodes[k]['z']) for k in act if float(nodes[k]['V']) == 0.0]
    if not zb or not zt or min(zt) <= max(zb):
        return None, I_tot, len(nzE)
    z_lo, z_hi = max(zb), min(zt)
    P = [z_lo + (k + 0.5) * (z_hi - z_lo) / planes for k in range(planes)]
    ladder, cum = [], 0.0
    for a, b, I in nzE:
        z1, z2 = float(nodes[a]['z']), float(nodes[b]['z'])
        cum += sum((I if z1 <= p < z2 else 0.0) - (I if z2 <= p < z1 else 0.0) for p in P) / planes
        ladder.append(cum / I_tot)
    return ladder, I_tot, len(nzE)


def ref_n(ladder, x, n_all):
    """누적이 처음 x 에 닿는 개수 (끝까지 못 닿으면 전부)."""
    for i, v in enumerate(ladder):
        if v >= x:
            return i + 1
    return n_all


def decode_compact(b):
    """압축 꼴 (packing nodes_v1) → 간선 dict 목록 (뷰어 칸) — 뷰어 netCurrentDecode 와 같은 규칙 (시험의 독립 판)."""
    nd, ec = b.get('nodes') or {}, b.get('edges_c') or {}
    out = []
    for ka, kb, jv in zip(ec.get('a') or [], ec.get('b') or [], ec.get('j') or []):
        out.append({'a': [nd['x'][ka], nd['y'][ka], nd['z'][ka]], 'b': [nd['x'][kb], nd['y'][kb], nd['z'][kb]],
                    'ra': nd['r'][ka], 'rb': nd['r'][kb], 'ia': nd['id'][ka], 'ib': nd['id'][kb], 'j': jv})
    return out


def section_selection(tmp, pub_rd):
    print('[⑥] 고르기 — 전류 몫 · 전부 · 압축 꼴 (상위 20000 상한 대신 모델이 정한 숫자 · 1저자 10-08)')
    import network_current as _ncur
    raw = os.path.join(pub_rd, DUMP)
    ladder, I_tot, n_nz = ref_share_ladder(raw)
    if not chk(f'⑥a 독립 재계산 — 단면이 있고 0 아닌 전류 간선이 있다 ({n_nz})', ladder is not None and n_nz > 10):
        return {}
    chk(f'⑥b 상수 — 전류 몫 고르기 {getattr(_ncur, "SHARE_CHOICES", None)} · 뷰어 기본 {getattr(_ncur, "VIEWER_DEFAULT", None)} '
        f'(1저자 Q2 = 전류 50 %) · 경로 기본 (top 없음) 은 그대로 5000', getattr(_ncur, 'SHARE_CHOICES', None) == (50, 80, 95)
        and getattr(_ncur, 'VIEWER_DEFAULT', None) == 'share50' and _ncur.TOP_DEFAULT == 5000)

    def pay(top, rd=pub_rd, channel='ionic'):
        try:
            return _ncur.current_payload(rd, channel, 'hertzian', top, 1000)
        except Exception as e:                                   # noqa: BLE001 — 옛 코드 (int('share50') ValueError 밖으로)
            return None, {'exc': repr(e)}
    got = {}
    for p in (50, 80, 95):
        x = p / 100.0
        st, b = pay(f'share{p}')
        sel = b.get('selection') or {}
        n = sel.get('n')
        lo_n, hi_n = ref_n(ladder, x - 1e-9, n_nz), ref_n(ladder, x + 1e-9, n_nz)
        got[p] = (st, b, n)
        chk(f'⑥c share{p} → 200 · 고르기 = 전류 몫 {p} % · 개수 {n} = 독립 재계산 [{lo_n}, {hi_n}] · 돌려준 수 · top = 그 개수',
            st == 200 and sel.get('kind') == 'share' and sel.get('share_pct') == p and isinstance(n, int)
            and lo_n <= n <= hi_n and b.get('n_returned') == n and b.get('top') == n, repr(sel)[:300] + repr(b.get('exc'))[:200])
        zc = b.get('zcut') or {}
        st_m, b_m = pay(n - 1) if isinstance(n, int) and n > 1 else (None, {})
        zc_m = b_m.get('zcut') or {}
        chk(f'⑥d share{p} = 가장 적은 개수 — 단면 몫 평균 {zc.get("share_mean")} ≥ {x} · 하나 덜면 (상위 {None if n is None else n - 1}) '
            f'{zc_m.get("share_mean")} < {x}',
            isinstance(zc.get('share_mean'), float) and zc['share_mean'] >= x - 1e-9
            and (n == 1 or (isinstance(zc_m.get('share_mean'), float) and zc_m['share_mean'] < x + 1e-9)))
    ns = [got[p][2] for p in (50, 80, 95)]
    chk(f'⑥e 50 ≤ 80 ≤ 95 % ≤ 전부 ({ns} · 0 아닌 전류 {n_nz})', all(isinstance(v, int) for v in ns) and ns[0] <= ns[1] <= ns[2] <= n_nz)
    sel50 = (got[50][1].get('selection') or {})
    chk(f'⑥f 고르기 정보 — 세 몫의 개수 (share_n) · 0 아닌 전류 접촉 수 (n_nonzero) ({sel50.get("share_n")} · {sel50.get("n_nonzero")})',
        sel50.get('share_n') == {'50': ns[0], '80': ns[1], '95': ns[2]} and sel50.get('n_nonzero') == n_nz)
    st_a, b_a = pay('all')
    sel_a = b_a.get('selection') or {}
    zc_a = b_a.get('zcut') or {}
    chk(f'⑥g all → 0 아닌 전류 접촉 전부 ({b_a.get("n_returned")} = {n_nz}) · 단면 몫 = 1 · 소산 몫 = 1',
        st_a == 200 and sel_a.get('kind') == 'all' and b_a.get('n_returned') == n_nz and sel_a.get('n') == n_nz
        and abs((zc_a.get('share_mean') or 0) - 1) < 1e-9 and abs((b_a.get('power_share') or 0) - 1) < 1e-9)
    b80 = got[80][1]
    chk('⑥h 이름 고르기 = 압축 꼴 (packing nodes_v1 · 입자 표 nodes · 접촉 edges_c · edges 없음)',
        b80.get('packing') == 'nodes_v1' and 'edges' not in b80 and isinstance(b80.get('nodes'), dict)
        and isinstance(b80.get('edges_c'), dict) and b_a.get('packing') == 'nodes_v1' and 'edges' not in b_a)
    n80 = ns[1]
    st_i, b_i = pay(n80 if isinstance(n80, int) else 5)
    sel_i = b_i.get('selection') or {}
    chk(f'⑥i 정수 고르기 = 옛 꼴 그대로 (edges 목록 · 키 = 옛 키 + selection 하나 · 고르기 = 개수 · 꼴 edges) — 더한 키 '
        f'{sorted(set(b_i) - OLD_KEYS)} · 빠진 키 {sorted(OLD_KEYS - set(b_i))}',
        st_i == 200 and set(b_i) == OLD_KEYS | {'selection'} and sel_i.get('kind') == 'count' and sel_i.get('packing') == 'edges'
        and isinstance(b_i.get('edges'), list) and 'packing' not in b_i)
    chk(f'⑥j 정수 고르기에도 세 몫의 개수 · 0 아닌 수 (뷰어가 고르기 칸에 개수를 적는다) ({sel_i.get("share_n")})',
        sel_i.get('share_n') == {'50': ns[0], '80': ns[1], '95': ns[2]} and sel_i.get('n_nonzero') == n_nz)
    dec = decode_compact(b80)
    old = [{k: e.get(k) for k in EDGE_VIEW_KEYS} for e in (b_i.get('edges') or [])]
    chk(f'⑥k 압축 꼴을 풀면 같은 개수 정수 고르기의 간선과 값 · 순서 그대로 (위치 · 반경 · 번호 · j 정확히 같음 · {len(dec)} 개)',
        bool(dec) and dec == old, (repr(dec[:1]) + ' vs ' + repr(old[:1]))[:400])
    same = all(b80.get(k) == b_i.get(k) for k in ('zcut', 'power_share', 'share_max', 'share_min', 'sum_abs_share', 'n_wrap_returned',
                                                  'n_returned', 'top', 'density', 'I_total', 'n_perc_edges', 'n_zero_current'))
    chk('⑥l 요약 값도 같다 (단면 몫 · 소산 몫 · 몫 최대 · 최소 · 주기 경계 수 · 전류 밀도 묶음 · I_전체)', same)
    st_big, b_big = pay(100000)                                  # 옛 상한 20000 → 이 침대에서는 전부 (옛 꼴)
    nb = max(1, len(b_big.get('edges') or []))
    by_old = len(json.dumps(b_big.get('edges'), separators=(',', ':'))) / nb
    by_new = len(json.dumps({'nodes': b_a.get('nodes'), 'edges_c': b_a.get('edges_c')}, separators=(',', ':'))) / max(1, b_a.get('n_returned') or 1)
    chk(f'⑥m 압축 꼴이 가볍다 — 접촉당 {by_new:.0f} B ↔ 옛 꼴 {by_old:.0f} B (절반 이하 · 같은 간선 수)',
        b_a.get('packing') == 'nodes_v1' and bool((b_a.get('nodes') or {}).get('id')) and len((b_a.get('edges_c') or {}).get('a') or []) == nb
        and 0 < by_new <= 0.5 * by_old)
    for tok in ('share0', 'share100', 'share', 'shareabc', 'share5.5', 'al', 'ALL'):
        st_b, b_b = pay(tok)
        chk(f'⑥n top={tok} → 400 (잘못된 고르기 · {st_b} · {b_b.get("error")})', st_b == 400 and b_b.get('error') == 'bad_top')
    # 전극 띠 노드가 없어 단면을 못 정하는 해 — 전류 몫 잣대가 없다 → 경로 기본 (상위 5000) 으로 그리고 사유를 적는다
    rd_nz = os.path.join(tmp, 'pub_nozcut')
    shutil.copytree(pub_rd, rd_nz)
    nf = dump_file(os.path.join(rd_nz, DUMP), 'nodes_hertzian_ionic')
    rows = read_csv_rows(nf)
    hdr = list(rows[0].keys())
    with gzip.open(nf, 'wt', encoding='utf-8') if nf.endswith('.gz') else open(nf, 'w') as f:
        f.write(','.join(hdr) + '\n')
        for r in rows:
            if float(r['V']) == 1.0:
                r['V'] = '0.999999'
            f.write(','.join(r[h] for h in hdr) + '\n')
    st_f, b_f = pay('share50', rd=rd_nz)
    sel_f = b_f.get('selection') or {}
    chk(f'⑥o 단면을 못 정하는 해 → share50 은 경로 기본 (상위 {_ncur.TOP_DEFAULT}) 으로 · 사유 (fallback) · 세 몫 개수 없음 '
        f'({st_f} · {sel_f.get("kind")} · {sel_f.get("fallback")})',
        st_f == 200 and b_f.get('zcut') is None and sel_f.get('kind') == 'count' and sel_f.get('requested') == 'share50'
        and bool(sel_f.get('fallback')) and sel_f.get('share_n') is None and b_f.get('n_returned') == min(_ncur.TOP_DEFAULT, n_nz))
    # 경로 — app.py 는 top 문자열을 그대로 넘긴다 (194 봉인 파일 · 고치지 않는다)
    import app as A
    c = A.app.test_client()
    up, rs = A.app.config['UPLOAD_FOLDER'], A.app.config['RESULTS_FOLDER']
    cid = '261008_000001_select'
    os.makedirs(os.path.join(up, cid), exist_ok=True)
    with open(os.path.join(up, cid, 'meta.json'), 'w') as f:
        json.dump({'name': cid, 'status': 'done', 'type_map': TYPE_MAP, 'scale': 1000, 'mode': 'standard'}, f)
    shutil.copytree(pub_rd, os.path.join(rs, cid))
    r = c.get(f'/results/{cid}/network-current?channel=ionic&mode=hertzian&top=share50')
    jr = r.get_json(silent=True) or {}
    chk(f'⑥p 경로 ?top=share50 → 200 · 고르기 전류 50 % · 같은 개수 ({r.status_code} · {(jr.get("selection") or {}).get("n")} = {ns[0]})',
        r.status_code == 200 and (jr.get('selection') or {}).get('kind') == 'share' and (jr.get('selection') or {}).get('n') == ns[0])
    app_src = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    chk("⑥q webapp/app.py 무변경 꼴 — top 문자열을 그대로 넘긴다 (top=request.args.get('top'))",
        "top=request.args.get('top')" in app_src)
    rc, out = run_tool('show', pub_rd, '--top', 'share80')
    chk(f'⑥r CLI show --top share80 → rc 0 · 고르기 줄 (전류 80 % · 개수 {n80})', rc == 0 and '전류 80 %' in out and str(n80) in out, out[-400:])
    return {'share80': b80, 'int80': b_i, 'all': b_a, 'n': dict(zip(('50', '80', '95'), ns)), 'n_nz': n_nz}


def section_viewer_select(sel):
    """④c 뷰어 — 고르기 칸 (전류 몫 · 상위 N · 전부 · 개수 표시) · 압축 꼴 풀기 · 색 위쪽 (최대 · p99 · p95) · 큰 N 가볍게 그리기 · 기억 4 개.
    1저자 10-08 Q1 · Q2 권고대로 + 이미 비준된 위쪽 고르기 (범례 = 숫자 셋 · '≥ X' · ▲ 없음 · 백분위는 방법 메모에만)."""
    print('[④c] 뷰어 — 고르기 · 압축 꼴 · 색 위쪽 · 가볍게 그리기 (node)')
    js = open(VIEWER_JS, encoding='utf-8').read()
    if not chk('④c0 서버 고르기 자료 (⑥) 가 있다', bool(sel and sel.get('share80') and sel.get('int80'))):
        return
    names = ('netCurrentDecode', 'netCurrentUrl', 'netCurrentTopOptions', 'netCurrentControlsHtml', 'netCurrentCap', 'netCurrentQuantile',
             'netCurrentCapTag', 'netCurrentCacheTrim', 'netCurrentLegendHtml', 'netCurrentColorbarSpec', 'netCurrentRange', 'netCurrentLogRange',
             'netCurrentTicks', 'netCurrentFrame', 'netCurrentFmtJ', 'netCurrentPct', 'jeEscH', 'jetColor')
    parts, miss = [], []
    for n in names:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    for n in ('NETCUR_CHANNELS', 'NETCUR_MODES'):
        try:
            parts.append(js_const(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    consts = {}
    for n in ('NETCUR_TOPS', 'NETCUR_WIDTHS', 'NETCUR_SHARES', 'NETCUR_CAPS', 'NETCUR_CACHE_MAX', 'NETCUR_LOD_N'):
        m = re.search(r'const ' + n + r' = [^;]*;', js)
        if m:
            consts[n] = m.group(0)
        else:
            miss.append(n)
    if not chk(f'④c1 viewer3d.js 에서 함수 · 상수를 잘라 냈다 (없음 {miss})', not miss):
        return
    n = sel['n']
    script = '\n'.join(parts + list(consts.values())) + r"""
const C = __C__, D = __D__, AL = __AL__;
const out = {};
const pick = e => [e.a, e.b, e.ra, e.rb, e.ia, e.ib, e.j];
const dc = netCurrentDecode(JSON.parse(JSON.stringify(C)));
out.dec = dc.edges.map(pick); out.dict = D.edges.map(pick);
out.decGone = !('edges_c' in dc) && !('nodes' in dc);
const dd = netCurrentDecode(JSON.parse(JSON.stringify(D)));
out.decIdem = dd.edges.length === D.edges.length && JSON.stringify(dd.edges) === JSON.stringify(D.edges);
out.url = ['share50', 'share80', 'share95', 'all', 2000, 'abc', 'share100'].map(t =>
  netCurrentUrl('/results/abc/3d-data', {channel: 'ionic', mode: 'hertzian', top: t}));
const opt = {channel: 'ionic', mode: 'hertzian', top: 'share50', width: 1, scale: 'log', cap: 'max'};
out.optPay = netCurrentTopOptions(opt, dc);
out.optNoPay = netCurrentTopOptions(opt);
const small = {selection: {kind: 'count', n_nonzero: 645, share_n: {'50': 40, '80': 200, '95': 400}}};
out.optSmall = netCurrentTopOptions(Object.assign({}, opt, {top: 20000}), small);
out.ctlPay = netCurrentControlsHtml(opt, dc);
out.ctlNoPay = netCurrentControlsHtml(opt);
out.ctlCap = netCurrentControlsHtml(Object.assign({}, opt, {cap: 'p95'}), dc);
const al = netCurrentDecode(JSON.parse(JSON.stringify(AL)));
const st = {nDrawn: 3, nWrapSkipped: 0, lo: -1, hi: 0, scale: 'log'};
out.legShare = netCurrentLegendHtml(dc, opt, st);
out.legAll = netCurrentLegendHtml(al, Object.assign({}, opt, {top: 'all'}), st);
out.legCount = netCurrentLegendHtml(dd, Object.assign({}, opt, {top: dd.n_returned}), st);
const fb = JSON.parse(JSON.stringify(dd));
fb.selection = {kind: 'count', requested: 'share50', fallback: '단면 없음 <b>x</b>', n: dd.n_returned, packing: 'edges'};
out.legFallback = netCurrentLegendHtml(fb, opt, st);
const E = [{j: 1}, {j: 2}, {j: 3}, {j: 4}, {j: 100}, {j: 0}, {j: null}];
out.cap = [netCurrentCap([1, 100], E, 'linear', 'max'), netCurrentCap([1, 100], E, 'linear', 'p99'), netCurrentCap([1, 100], E, 'linear', 'p95'),
           netCurrentCap([0, 2], E, 'log', 'p99'), netCurrentCap([1, 100], E, 'linear', 'bogus'), netCurrentCap(null, E, 'linear', 'p99'),
           netCurrentCap([1, 100], E, 'linear', undefined)];
out.q = [netCurrentQuantile([1, 2, 3, 4, 100], 0.99), netCurrentQuantile([5], 0.95), netCurrentQuantile([1, 3], 0.5)];
out.tag = [netCurrentCapTag({cap: 'p99'}), netCurrentCapTag({cap: 'p95'}), netCurrentCapTag({cap: 'max'}), netCurrentCapTag({}), netCurrentCapTag(null)];
const PJ = JSON.parse(JSON.stringify(dd));
const lin99 = Object.assign({}, opt, {scale: 'linear', cap: 'p99'});
out.legCap = netCurrentLegendHtml(PJ, lin99, {nDrawn: 3, nWrapSkipped: 0, lo: 1, hi: 96.16, scale: 'linear'});
out.legNoCap = netCurrentLegendHtml(PJ, Object.assign({}, lin99, {cap: 'max'}), {nDrawn: 3, nWrapSkipped: 0, lo: 1, hi: 100, scale: 'linear'});
out.specCap = netCurrentColorbarSpec(PJ, lin99, 1, 96.16, '1V');
out.specLogCap = netCurrentColorbarSpec(PJ, Object.assign({}, opt, {cap: 'p95'}), 0, Math.log10(80.8), '1V');
out.specMax = netCurrentColorbarSpec(PJ, Object.assign({}, lin99, {cap: 'max'}), 1, 100, '1V');
out.specShare = netCurrentColorbarSpec(dc, opt, -1, 0, '1V');
out.specAll = netCurrentColorbarSpec(al, Object.assign({}, opt, {top: 'all'}), -1, 0, '1V');
out.fj = [netCurrentFmtJ(1), netCurrentFmtJ(0.5 * (1 + 96.16)), netCurrentFmtJ(96.16)];
const cache = {};
['u1', 'u2', 'u3', 'u4', 'u5'].forEach(u => { cache[u] = {}; netCurrentCacheTrim(cache, u); });
out.cache = Object.keys(cache);
cache.u2 = {x: 1}; netCurrentCacheTrim(cache, 'u2');
out.cacheKeep = Object.keys(cache);
out.consts = {shares: NETCUR_SHARES, caps: NETCUR_CAPS.map(c => c[0]), cacheMax: NETCUR_CACHE_MAX, lod: NETCUR_LOD_N, tops: NETCUR_TOPS};
console.log(JSON.stringify(out));
""".replace('__C__', json.dumps(sel['share80'], ensure_ascii=False)).replace('__D__', json.dumps(sel['int80'], ensure_ascii=False)) \
        .replace('__AL__', json.dumps(sel['all'], ensure_ascii=False))
    res = run_node(script)
    if not chk('④c2 node 실행', res is not None):
        return
    cs = res['consts']
    chk(f'④c3 상수 — 전류 몫 {cs["shares"]} · 위쪽 {cs["caps"]} · 기억 {cs["cacheMax"]} · 가볍게 그리기 문턱 {cs["lod"]} · 상위 N 목록 그대로',
        cs['shares'] == [50, 80, 95] and cs['caps'] == ['max', 'p99', 'p95'] and cs['cacheMax'] == 4 and cs['lod'] == 20000
        and cs['tops'] == [500, 1000, 2000, 5000, 10000, 20000])
    chk(f'④c4 압축 꼴 풀기 = 같은 개수 정수 고르기의 간선 (위치 · 반경 · 번호 · j · 순서 정확히 같음 · {len(res["dec"])} 개) · 푼 뒤 압축 칸은 지운다',
        bool(res['dec']) and res['dec'] == res['dict'] and res['decGone'])
    chk('④c5 옛 꼴 (edges) 은 풀기가 손대지 않는다 (같은 객체 그대로)', res['decIdem'])
    chk(f'④c6 URL — 이름 고르기는 그대로 (share50 · share80 · share95 · all) · 정수는 옛 그대로 · 잘못된 것 = 5000 {res["url"]}', res['url'] == [
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=share50',
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=share80',
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=share95',
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=all',
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=2000',
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=5000',
        '/results/abc/network-current?channel=ionic&mode=hertzian&top=5000'])
    nz = sel['n_nz']
    want = [['share50', f'전류 50 % ({n["50"]} 개)'], ['share80', f'전류 80 % ({n["80"]} 개)'], ['share95', f'전류 95 % ({n["95"]} 개)']] \
        + [[t, f'상위 {t}'] for t in (500, 1000, 2000, 5000, 10000, 20000) if t < nz] + [['all', f'전부 ({nz} 개)']]
    chk(f'④c7 고르기 칸 (자료 있음) = 전류 50 · 80 · 95 % (개수) · 그 케이스 접촉 수보다 작은 상위 N 만 · 전부 (개수) {res["optPay"]}',
        res['optPay'] == want, repr(want))
    chk(f'④c8 자료 없을 때 (오류 범례) = 개수 없이 · 상위 N 전부 · 전부 {res["optNoPay"]}', res['optNoPay'] == (
        [['share50', '전류 50 %'], ['share80', '전류 80 %'], ['share95', '전류 95 %']]
        + [[t, f'상위 {t}'] for t in (500, 1000, 2000, 5000, 10000, 20000)] + [['all', '전부']]))
    chk(f'④c9 접촉 645 침대 — 상위 500 만 남고 전부 (645 개) · 지금 고른 상위 20000 은 지워지지 않고 보인다 {res["optSmall"]}', res['optSmall'] == [
        ['share50', '전류 50 % (40 개)'], ['share80', '전류 80 % (200 개)'], ['share95', '전류 95 % (400 개)'], [500, '상위 500'],
        ['all', '전부 (645 개)'], [20000, '상위 20000']])
    cp = res['ctlPay']
    chk('④c10 조작판 — 고르기 (id netcur-top) 기본 = 전류 50 % selected · 개수 표시 · 위쪽 고르기 (id netcur-cap) 기본 = 최대',
        'id="netcur-top"' in cp and re.search(r'<option value="share50" selected>전류 50 % \(\d+ 개\)</option>', cp) is not None
        and 'id="netcur-cap"' in cp and re.search(r'<option value="max" selected>', cp) is not None
        and re.search(r'<option value="p95" selected>', res['ctlCap']) is not None
        and re.search(r'<option value="share50" selected>전류 50 %</option>', res['ctlNoPay']) is not None, cp[:500])
    ls, la, lc, lf = res['legShare'], res['legAll'], res['legCount'], res['legFallback']
    def sel_line(h):                                             # 범례의 고르기 줄 (굵은 '색 · 굵기 = …') — 조작판 칸 글자는 빼고 본다
        m = re.search(r'<b>색 · 굵기 = [^<]*</b>', h)
        return m.group(0) if m else ''
    lsl, lal, lcl = sel_line(ls), sel_line(la), sel_line(lc)
    chk(f'④c11 범례 고르기 줄 — 전류 80 % 를 나르는 상위 {n["80"]} 접촉 · 전부 {nz} 개 · 정수 = 옛 문구 (상위 N 접촉 · |I| 큰 순) '
        f'[{lsl} / {lal} / {lcl}]',
        f'전류 80 % 를 나르는 상위 {n["80"]} 접촉' in lsl and '|I|' in lsl and f'전류가 흐르는 접촉 전부 ({nz} 개)' in lal
        and f'상위 {n["80"]} 접촉 (|I| 큰 순)' in lcl and '전류 80 %' not in lcl)
    chk('④c12 단면을 못 정한 해 → 범례 ⚠ 사유 (서버 문자열 이스케이프) · 상위 N 문구', '⚠' in lf and '단면 없음' in lf and '<b>x</b>' not in lf
        and '&lt;b&gt;x&lt;/b&gt;' in lf and '상위 ' in lf)
    cap = res['cap']
    chk(f'④c13 색 위쪽 — 최대 = 그대로 · p99 · p95 = 고른 접촉 j (0 · 없음 제외) 의 백분위 (선형 보간 · numpy 기본과 같은 정의) · log = log₁₀ · '
        f'잘못된 값 · 없음 = 그대로 {cap}',
        cap[0] == [1, 100] and abs(cap[1][1] - 96.16) < 1e-9 and cap[1][0] == 1 and abs(cap[2][1] - 80.8) < 1e-9
        and abs(cap[3][1] - math.log10(96.16)) < 1e-12 and cap[3][0] == 0 and cap[4] == [1, 100] and cap[5] is None and cap[6] == [1, 100])
    chk(f'④c14 백분위 함수 {res["q"]}', abs(res['q'][0] - 96.16) < 1e-9 and res['q'][1] == 5 and res['q'][2] == 2)
    chk(f'④c15 컬러바 파일 이름 꼬리 — p99 → _p99 · p95 → _p95 · 최대 · 없음 → 꼬리 없음 {res["tag"]}', res['tag'] == ['_p99', '_p95', '', '', ''])
    lcap, lno = res['legCap'], res['legNoCap']
    fj = res['fj']
    chk(f'④c16 범례 숫자 = 평범한 숫자 셋 ({fj[0]} … {fj[2]} · 가운데 {fj[1]}) · "≥" · ▲ 없음 · 위쪽 고른 것은 회색 방법 메모 (99 % 값)',
        f'{fj[0]} … {fj[2]} A cm⁻²' in lcap and f'가운데 {fj[1]}' in lcap and '≥' not in lcap and '▲' not in lcap
        and '99 % 값' in lcap and '99 % 값' not in lno and '≥' not in lno, lcap[:500])
    sc_, sl_, sm_ = res['specCap'], res['specLogCap'], res['specMax']
    chk(f'④c17 컬러바 PNG 눈금 = 숫자 셋 그대로 ({[t["label"] for t in sc_["ticks"]]}) · "≥" · ▲ 없음 · 위쪽 고르기는 아래 작은 글 (방법) 에만 '
        f'(99th · 95th percentile) · 최대면 그 글 없음',
        [t['label'] for t in sc_['ticks']] == fj and not any(('≥' in t['label'] or '▲' in t['label']) for t in sc_['ticks'] + sl_['ticks'])
        and '99th percentile' in sc_['sub'] and '95th percentile' in sl_['sub'] and 'percentile' not in sm_['sub']
        and '≥' not in sc_['title'] + sc_['sub'] and '▲' not in sc_['title'] + sc_['sub'], repr(sc_)[:400])
    chk('④c18 컬러바 제목 — 전류 몫 = "top N contacts (80 % of the current)" · 전부 = "all N current-carrying contacts"',
        f'top {n["80"]} contacts (80 % of the current)' in res['specShare']['title']
        and f'all {nz} current-carrying contacts' in res['specAll']['title'], res['specShare']['title'] + ' / ' + res['specAll']['title'])
    chk(f'④c19 받은 자료 기억 = 최근 4 개 (전부 자료가 쌓여 메모리를 잡지 않게) · 다시 쓴 것은 맨 뒤로 (지우지 않는다) {res["cache"]} · '
        f'{res["cacheKeep"]}', res['cache'] == ['u2', 'u3', 'u4', 'u5'] and res['cacheKeep'] == ['u3', 'u4', 'u5', 'u2'])
    try:
        rnc = js_fn(js, 'renderNetCurrent')
        wl = js_fn(js, 'netCurrentWireLegend')
        anm = js_fn(js, 'applyNetCurrentMode')
    except (ValueError, AssertionError):
        rnc = wl = anm = ''
    chk('④c20 그리기 = 위쪽을 고른 범위 (netCurrentCap(netCurrentRange(edges, sc), edges, sc, opt.cap)) · 접촉이 많으면 (> NETCUR_LOD_N) 6 각 · '
        '뚜껑 없는 관 (삼각형 4 배 적게) · 아니면 옛 12 각 그대로',
        'netCurrentCap(netCurrentRange(edges, sc), edges, sc, opt.cap)' in rnc and 'draw.length > NETCUR_LOD_N' in rnc
        and 'new THREE.CylinderGeometry(1, 1, 1, 6, 1, true)' in rnc and 'new THREE.CylinderGeometry(1, 1, 1, 12, 1, false)' in rnc)
    chk('④c21 받기 = 압축 꼴을 풀고 (netCurrentDecode) 기억 (cache[url]) 뒤 4 개로 자른다 (netCurrentCacheTrim) — 오류 범례가 먼저',
        'netCurrentDecode(res.body)' in anm and 'netCurrentCacheTrim(cache, url)' in anm
        and anm.index('netCurrentErrorHtml') < anm.index('netCurrentDecode(res.body)') < anm.index('cache[url] = res.body')
        < anm.index('netCurrentCacheTrim(cache, url)'))
    chk('④c22 고르기 바꾸기 — 숫자는 숫자로 · 이름 (share · all) 은 그대로 · 위쪽을 바꾸면 다시 받지 않고 다시 그린다',
        re.search(r"on\('netcur-top', 'change', ev => \{ const v = ev\.target\.value; opt\.top = /\^\\d\+\$/\.test\(v\) \? \+v : v; "
                  r"applyNetCurrentMode\(state\); \}\)", wl) is not None
        and re.search(r"on\('netcur-cap', 'change', ev => \{ opt\.cap = ev\.target\.value; if \(pay\) renderNetCurrent\(state, pay\); \}\)", wl)
        is not None)
    chk("④c23 컬러바 단추 둘의 파일 이름 = … + netCurrentCapTag(opt) + '.png' (위쪽을 고른 그림이 최대 그림을 덮어쓰지 않게)",
        wl.count("netCurrentCapTag(opt) + '.png'") == 2)
    chk("④c24 기본 옵션 = 전류 50 % (1저자 Q2) · 위쪽 최대 — { channel: 'ionic', mode: 'hertzian', top: 'share50', arrows: false, width: 1, "
        "scale: 'log', cap: 'max' }",
        "_netCurOpt = { channel: 'ionic', mode: 'hertzian', top: 'share50', arrows: false, width: 1, scale: 'log', cap: 'max' }" in anm)


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
        section_viewer_width()
        section_viewer_scale()
        sel = {}
        try:
            sel = section_selection(tmp, pub)
        except Exception as e:                                   # noqa: BLE001 — 옛 코드 (고르기 없음) 에서도 나머지를 돈다
            chk('⑥ 고르기 절 실행', False, f'{type(e).__name__}: {e}')
        section_viewer_select(sel)
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

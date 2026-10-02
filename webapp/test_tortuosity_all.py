#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""기하 τ 전체판 회귀 — 바닥 띠 관통 SE **전부** → 위쪽 띠 SE 까지 각자의 최단 경로 (1저자 10-02 · J20-l 코드 → 웹앱 같은 묶음).

  python3 webapp/test_tortuosity_all.py      # 종료코드 0 = PASS

  옛 τ_Dij (`calc_tortuosity`) 는 바닥 SE 와 위쪽 SE 를 **무작위로 짝지은 최대 200 쌍**의 최단 경로 ÷ 두 입자 z 차다.
  전체판 (`calc_tortuosity_all`) 은 표본 없이 바닥 띠의 관통 SE 마다 **경로가 가장 짧은 위쪽 띠 SE** 까지의 길이 ÷ 두 입자 z 차
  (다중 출발 Dijkstra 한 번 · 간선 길이 = calc_percolation 의 'distance' = x,y 주기 최소상 중심 거리 · 길이만 = 기하).

  [A] 핵심 함수 — A1 곧은 사슬 = 1 · A2 옆 우회 빗 (해석해 · 표본판보다 작거나 같다) · A3 무작위 침대 = 짝별 전수 대조 (oracle) ·
      A4 관통 없음 = None · A5 주기 경계를 넘는 사슬 · A6 Δz ≤ 0 은 빼고 센다 · A7 SE 없음
  [B] 파이프라인 — 웹앱과 같은 CLI (analyze_contacts_bimodal.py) 가 full_metrics.json 에 tortuosity_all_* 를 쓴다
  [C] 웹앱 — 케이스 표 τ 비교 블록에 'τ_Dij,all' 행 (τ_Dij 바로 아래) · 정렬 목록 · 영문 라벨 ↔ 역맵 · 툴팁 · τ_Dij 툴팁에 '200 쌍 무작위 짝'
"""
import json
import math
import os
import random
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)

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


def close(a, b, tol=1e-12):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


import networkx as nx  # noqa: E402
import dem_analysis_core as dac  # noqa: E402

SE = {3}
R = 0.002


def bed(atoms_list, pairs):
    atoms = {i: {'type': 3, 'x': x, 'y': y, 'z': z, 'radius': R} for i, x, y, z in atoms_list}
    contacts = [{'id1': a, 'id2': b} for a, b in pairs]
    return atoms, contacts


def run_all(atoms, contacts, plate_z, box=(0.05, 0.05), **kw):
    perc = dac.calc_percolation(atoms, contacts, SE, plate_z, box_x=box[0], box_y=box[1])
    fn = getattr(dac, 'calc_tortuosity_all', None)
    if fn is None:
        return perc, None
    return perc, fn(atoms, perc, box_x=box[0], box_y=box[1], **kw)


print('[A] 핵심 함수 calc_tortuosity_all')
chk('A0 함수가 있다', hasattr(dac, 'calc_tortuosity_all'))

# A1 — 곧은 사슬 셋 (x 0.01 · 0.02 · 0.03 · z 2 → 28.6 µm) → 전부 τ = 1 · n = 3
al, pr = [], []
for c, cx in enumerate((0.01, 0.02, 0.03)):
    ids = [100 * (c + 1) + k for k in range(8)]
    al += [(i, cx, 0.01, R + 0.0038 * k) for k, i in enumerate(ids)]
    pr += list(zip(ids[:-1], ids[1:]))
_, r1 = run_all(*bed(al, pr), plate_z=0.03)
chk('A1 곧은 사슬 셋 → mean = median = 1 · n = n_sources = 3 · std 0',
    r1 is not None and close(r1.get('mean'), 1.0) and close(r1.get('median'), 1.0) and r1.get('n') == 3
    and r1.get('n_sources') == 3 and close(r1.get('std'), 0.0), repr(r1))

# A2 — 옆 우회 빗: 바닥 줄 B0..B4 (서로 닿음) · 기둥 하나 (B0 위) · 위 줄 T0..T4.  바닥 B_k 의 최단 = k·s (옆) + H (위) → τ_k = (k·s + H) / H
s, H, zb = 0.0038, 0.0038 * 6, R
bot = [(10 + k, 0.005 + s * k, 0.01, zb) for k in range(5)]
col = [(20 + m, 0.005, 0.01, zb + 0.0038 * m) for m in range(1, 6)]
topz = zb + H
top = [(30 + k, 0.005 + s * k, 0.01, topz) for k in range(5)]
pr2 = [(10 + k, 11 + k) for k in range(4)] + [(10, 21)] + [(20 + m, 21 + m) for m in range(1, 5)] + [(25, 30)] \
    + [(30 + k, 31 + k) for k in range(4)]
a2, c2 = bed(bot + col + top, pr2)
p2, r2 = run_all(a2, c2, plate_z=topz + R, detail=True)
exp2 = {10 + k: (k * s + H) / H for k in range(5)}
per2 = (r2 or {}).get('per_source') or {}
chk('A2 옆 우회 빗 — 바닥 다섯 각자의 τ = (k·s + H)/H (해석해) · 닿는 위쪽 = 기둥 꼭대기 T0',
    r2 is not None and len(per2) == 5
    and all(close(per2[i]['tau'], e, 1e-9) and per2[i]['target'] == 30 for i, e in exp2.items()),
    repr({i: (round(v['tau'], 6), v['target']) for i, v in per2.items()}))
chk('A2b mean = 해석 평균', r2 is not None and close(r2.get('mean'), sum(exp2.values()) / 5, 1e-9), repr(r2 and r2.get('mean')))
ts2 = dac.calc_tortuosity(a2, p2, box_x=0.05, box_y=0.05)
chk('A2c 표본판 (무작위 짝 · 위쪽 짝이 옆으로 멀다) 보다 작거나 같다 — 이 빗에서는 strict',
    r2 is not None and ts2.get('mean') is not None and r2['mean'] < ts2['mean'], f"all {r2 and r2.get('mean')} · 표본 {ts2.get('mean')}")

# A3 — 무작위 침대 → 짝별 전수 대조 (oracle): 바닥 관통 SE 마다 min_t L(s,t) · 동률이면 번호가 작은 t · τ = L / (z_t − z_s)
rng = random.Random(7)
found = None
for seed in range(40):
    rng.seed(seed)
    pts = [(1000 + i, rng.uniform(0, 0.02), rng.uniform(0, 0.02), rng.uniform(R, 0.03 - R)) for i in range(260)]
    atoms3 = {i: {'type': 3, 'x': x, 'y': y, 'z': z, 'radius': R} for i, x, y, z in pts}
    ids3 = sorted(atoms3)
    c3 = []
    for ii, a in enumerate(ids3):
        for b in ids3[ii + 1:]:
            if dac._periodic_dist(atoms3[a], atoms3[b], 0.02, 0.02) < 2 * R * 1.55:
                c3.append({'id1': a, 'id2': b})
    p3, r3 = run_all(atoms3, c3, plate_z=0.03, box=(0.02, 0.02), detail=True)
    srcs = sorted(p3['bottom_se'] & p3.get('percolating_se', set()))
    if len(srcs) >= 6 and r3 is not None:
        found = (atoms3, p3, r3, srcs)
        break
chk('A3a 관통하는 무작위 침대를 만들었다 (바닥 관통 SE ≥ 6)', found is not None)
if found:
    atoms3, p3, r3, srcs = found
    G3 = p3['graph']
    tops = sorted(p3['top_se'] & p3['percolating_se'])
    bad = []
    for sid in srcs:
        lens = nx.single_source_dijkstra_path_length(G3, sid, weight='distance')
        best = min(((lens[t], t) for t in tops if t in lens), default=None)
        got = r3['per_source'].get(sid)
        if best is None or got is None:
            bad.append((sid, 'missing'))
            continue
        L, t = best
        dz = atoms3[t]['z'] - atoms3[sid]['z']
        if not (close(got['length'], L, 1e-12) and got['target'] == t and close(got['tau'], L / dz, 1e-12)):
            bad.append((sid, got, L, t))
    chk(f'A3 전수 대조 — 바닥 관통 SE {len(srcs)} 개 각자 = 짝별 최단 경로 중 최소 (길이 · 닿는 위쪽 · τ)', not bad, repr(bad[:3]))
    chk('A3b n_sources = 바닥 관통 SE 수 · n + n_dz_nonpos = n_sources',
        r3['n_sources'] == len(srcs) and r3['n'] + r3['n_dz_nonpos'] == len(srcs), repr(r3))

# A4 — 관통 없음 (사슬이 위 띠에 못 닿는다) → None · n 0
al4 = [(i, 0.01, 0.01, R + 0.0038 * i) for i in range(4)] + [(50 + i, 0.03, 0.01, 0.03 - R - 0.0038 * i) for i in range(4)]
pr4 = [(i, i + 1) for i in range(3)] + [(50 + i, 51 + i) for i in range(3)]
_, r4 = run_all(*bed(al4, pr4), plate_z=0.03)
chk('A4 관통 없음 → mean None · n 0 · n_sources 0', r4 is not None and r4.get('mean') is None and r4.get('n') == 0
    and r4.get('n_sources') == 0, repr(r4))

# A5 — x 주기 경계를 넘나드는 지그재그 사슬 (x 0.0495 ↔ 0.0005 · 상자 0.05) → 걸음 = √(0.001² + dz²)
dzs = 0.0036
al5 = [(i, 0.0495 if i % 2 == 0 else 0.0005, 0.01, R + dzs * i) for i in range(8)]
al5 += [(60 + i, 0.02 + 0.0045 * (i % 2), 0.01, R + dzs * i) for i in range(8)]       # 둘째 사슬 (띠 ≥ 3 개 유지)
al5 += [(80 + i, 0.035, 0.01, R + dzs * i) for i in range(8)]
pr5 = [(i, i + 1) for i in range(7)] + [(60 + i, 61 + i) for i in range(7)] + [(80 + i, 81 + i) for i in range(7)]
_, r5 = run_all(*bed(al5, pr5), plate_z=R + dzs * 7 + R, detail=True)
exp5 = math.sqrt(0.001 ** 2 + dzs ** 2) / dzs
chk('A5 주기 경계를 넘는 사슬 — 걸음마다 최소상 √(0.001² + dz²) · τ = 그 비',
    r5 is not None and close((r5.get('per_source') or {}).get(0, {}).get('tau'), exp5, 1e-9),
    repr(r5 and (r5.get('per_source') or {}).get(0)))

# A6 — 바닥 · 위 띠가 겹치는 얇은 침대 (plate_z 6 µm · 띠 = 자기 반지름 2 배) → Δz ≤ 0 출발점은 빼고 센다
al6 = [(i, 0.005 + 0.0038 * i, 0.01, 0.003) for i in range(4)]
pr6 = [(i, i + 1) for i in range(3)]
_, r6 = run_all(*bed(al6, pr6), plate_z=0.006)
chk('A6 띠가 겹친 출발점 (Δz = 0) 은 τ 에서 빼고 n_dz_nonpos 로 센다 · mean None',
    r6 is not None and r6.get('n_dz_nonpos') == 4 and r6.get('n') == 0 and r6.get('mean') is None, repr(r6))

# A7 — SE 없음
_, r7 = run_all({1: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': 0.01, 'radius': 0.003}}, [], plate_z=0.03)
chk('A7 SE 없음 → mean None · n 0 (예외 없음)', r7 is not None and r7.get('mean') is None and r7.get('n') == 0, repr(r7))

print('[B] 파이프라인 (웹앱과 같은 CLI)')
import test_closed_param_values as tcv  # noqa: E402

tmp = tempfile.mkdtemp(prefix='tau_all_')
try:
    bA = tcv.make_bed(os.path.join(tmp, 'A'))
    prA, mA = tcv.run_bed(bA)
    chk('B0 침대 A — analyze_contacts_bimodal.py rc 0 · full_metrics.json', prA.returncode == 0 and bool(mA),
        (prA.stderr or prA.stdout or '')[-400:])
    chk('B1 full_metrics.json 에 tortuosity_all_mean = 1 (곧은 SE 사슬 셋) · _n = 3 · _n_sources = 3',
        close(mA.get('tortuosity_all_mean'), 1.0) and mA.get('tortuosity_all_n') == 3 and mA.get('tortuosity_all_n_sources') == 3,
        repr({k: v for k, v in mA.items() if k.startswith('tortuosity')}))
    chk('B2 _median · _std · _recommended 키도 있다',
        all(k in mA for k in ('tortuosity_all_median', 'tortuosity_all_std', 'tortuosity_all_recommended')))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print('[C] 웹앱')
import app as A  # noqa: E402

LBL_ALL = 'τ_Dij,all (Dijkstra 전체, 기하만)'
LBL_DIJ = 'τ_Dij (Dijkstra, 기하만)'
tmp = tempfile.mkdtemp(prefix='tau_all_web_')
try:
    rd = os.path.join(tmp, 'results', 'tcase')
    os.makedirs(rd)
    with open(os.path.join(rd, 'network_summary.csv'), 'w', encoding='utf-8') as f:
        f.write('지표,값\n── 구조 ──,\nPorosity(%),15.63\n')
    met = {'porosity': 15.63, 'thickness_um': 30.28, 'phi_se': 0.25,
           'sigma_full_mScm': 0.15, 'sigma_bulk_net_mScm': 0.6,
           'tortuosity_mean': 1.25, 'tortuosity_all_mean': 1.1234, 'tortuosity_all_n': 321}
    with open(os.path.join(rd, 'full_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(met, f)
    cd = os.path.join(tmp, 'uploads', 'tcase')
    os.makedirs(cd)
    with open(os.path.join(cd, 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump({'name': 'tcase', 'mode': 'bimodal', 'scale': 1000}, f)
    tables, _m, _ip = A._load_case_tables(rd, {'id': 'tcase', 'name': 'tcase'})
    rows = tables['network_summary']['data']
    labels = [str(r[0]).strip() for r in rows]

    def _idx(lbl):                       # 표는 원 라벨을 영문 라벨 (_PAPER_LABEL_MAP) 로 바꿔 낸다 — 둘 중 하나
        for cand in (lbl, A._PAPER_LABEL_MAP.get(lbl, lbl)):
            if cand in labels:
                return labels.index(cand)
        return -1
    i_dij, i_all = _idx(LBL_DIJ), _idx(LBL_ALL)
    chk('C1 τ 비교 블록에 τ_Dij,all 행 · τ_Dij 바로 아래', i_dij >= 0 and i_all == i_dij + 1, repr(labels[-10:]))
    if i_all >= 0:
        chk('C2 값 = tortuosity_all_mean 반올림 2 자리', any(str(v).strip() == '1.12' for v in rows[i_all][1:]), repr(rows[i_all]))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

src = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
order_blk = src[src.index('_CANONICAL_ROW_ORDER = ['):]
order_blk = order_blk[:order_blk.index(']')]
chk('C3 정렬 목록 (_CANONICAL_ROW_ORDER) 에 τ_Dij 다음 τ_Dij,all',
    LBL_ALL in order_blk and order_blk.index(LBL_ALL) > order_blk.index(LBL_DIJ))
eng = A._PAPER_LABEL_MAP.get(LBL_ALL)
chk('C4 영문 라벨 (_PAPER_LABEL_MAP) 이 있다 · 표본 아님 (every bottom SE) 을 말한다',
    bool(eng) and 'every bottom SE' in eng, repr(eng))
html = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
chk('C5 역맵 (PAPER_TO_ORIG) 이 영문 라벨 → 원 라벨', bool(eng) and f"'{eng}': '{LBL_ALL}'" in html)
k = html.find(f"'{LBL_ALL}': {{")
tip = html[k:k + 1600] if k >= 0 else ''
chk('C6 툴팁 — 식 (최단 경로 ÷ z 차) · 바닥 관통 SE 전부 · 표본판과의 차이',
    k >= 0 and 'Δz' in tip and '전부' in tip and '200' in tip, tip[:200])
k2 = html.find(f"'{LBL_DIJ}': {{")
tip2 = html[k2:k2 + 900] if k2 >= 0 else ''
chk('C7 τ_Dij 툴팁 = 무작위 짝 최대 200 쌍 (표본) 이라고 적는다', '200' in tip2 and '무작위' in tip2, tip2[:200])

print('[D] 기존 케이스 채우기 — scripts/tau_all_backfill.py (파이프라인 재실행 없이 · 같은 입력 · 표본판 재계산 일치 때만 기록)')
import subprocess  # noqa: E402

BF = os.path.join(SCRIPTS, 'tau_all_backfill.py')
chk('D0 도구가 있다', os.path.exists(BF))
tmp = tempfile.mkdtemp(prefix='tau_all_bf_')
try:
    bA = tcv.make_bed(os.path.join(tmp, 'A'))
    prA, mA = tcv.run_bed(bA)
    out = bA['out']
    for fn in ('atoms.csv', 'contacts.csv'):                        # 웹앱은 분석 입력을 results 폴더에 복사해 둔다
        shutil.copy2(os.path.join(bA['dir'], fn), os.path.join(out, fn))
    fm = os.path.join(out, 'full_metrics.json')
    orig_all = {k: v for k, v in mA.items() if k.startswith('tortuosity_all_')}
    old = {k: v for k, v in mA.items() if not k.startswith('tortuosity_all_')}   # 옛 케이스 흉내 — 새 키 없음
    with open(fm, 'w', encoding='utf-8') as f:
        json.dump(old, f)

    def bf(*extra):
        return subprocess.run([sys.executable, BF, '--results', out, '--type-map', bA['tmap'], '--scale', '1000',
                               '--tsv', os.path.join(tmp, 'tau.tsv')] + list(extra), capture_output=True, text=True, timeout=600)
    p1 = bf()
    tsv = open(os.path.join(tmp, 'tau.tsv'), encoding='utf-8').read() if os.path.exists(os.path.join(tmp, 'tau.tsv')) else ''
    chk('D1 읽기만 — rc 0 · 표에 τ_all = 1 · 표본판 재계산 = 저장값 (match) · 파일은 그대로',
        p1.returncode == 0 and 'match' in tsv and '\t1.0' in tsv
        and json.load(open(fm, encoding='utf-8')) == old, (p1.stderr or p1.stdout)[-400:] + ' | ' + tsv[:300])
    p2 = bf('--write')
    new = json.load(open(fm, encoding='utf-8'))
    got_all = {k: v for k, v in new.items() if k.startswith('tortuosity_all_') and k != 'tortuosity_all_provenance'}
    chk('D2 --write — 새 키 = 파이프라인 값과 같다 · 다른 키는 그대로 · 출처 기록 · 원본 사본',
        p2.returncode == 0 and got_all == orig_all
        and {k: v for k, v in new.items() if not k.startswith('tortuosity_all_')} == old
        and (new.get('tortuosity_all_provenance') or {}).get('sampled_recheck') == 'match'
        and os.path.exists(fm + '.pre_tau_all'), f'{got_all} vs {orig_all} · {(p2.stderr or p2.stdout)[-300:]}')
    bad = dict(old, tortuosity_mean=1.5)                             # 저장값이 재계산과 다르다 = 입력이 다르다
    with open(fm, 'w', encoding='utf-8') as f:
        json.dump(bad, f)
    p3 = bf('--write')
    chk('D3 표본판 재계산이 저장값과 다르면 --write 거부 (rc ≠ 0 · 파일 그대로)',
        p3.returncode != 0 and json.load(open(fm, encoding='utf-8')) == bad, (p3.stderr or p3.stdout)[-300:])
    # D4 — 웹앱 폴더 + 케이스 이름으로 찾기 (uploads/<id>/meta.json 의 name · type_map · scale → results/<id>)
    root = os.path.join(tmp, 'webapp')
    os.makedirs(os.path.join(root, 'uploads', 'cid1'))
    shutil.copytree(out, os.path.join(root, 'results', 'cid1'))
    with open(os.path.join(root, 'results', 'cid1', 'full_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(old, f)
    with open(os.path.join(root, 'uploads', 'cid1', 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump({'name': 'input_bedA', 'mode': 'bimodal', 'type_map': bA['tmap'], 'scale': 1000}, f)
    p4 = subprocess.run([sys.executable, BF, '--webapp-root', root, '--name', 'input_bedA',
                         '--tsv', os.path.join(tmp, 'tau4.tsv')], capture_output=True, text=True, timeout=600)
    t4 = open(os.path.join(tmp, 'tau4.tsv'), encoding='utf-8').read() if os.path.exists(os.path.join(tmp, 'tau4.tsv')) else ''
    chk('D4 --webapp-root · --name 으로 케이스를 찾는다 (meta.json 의 type_map · scale)',
        p4.returncode == 0 and 'input_bedA' in t4 and 'match' in t4, (p4.stderr or p4.stdout)[-300:])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print('[E] 웹앱 그룹 표 · 보고서 · 파라미터 목록에 τ_Dij,all')
lines = src.splitlines()
hits = [i for i, ln in enumerate(lines)
        if ln.strip() in ("('Tortuosity', 'tortuosity_mean'),", "('Tortuosity', '', 'tortuosity_mean', 'SE 네트워크'),")]
chk('E0 τ_Dij 목록 셋 (그룹 표 · 파라미터 목록 · 보고서 표) 을 찾았다', len(hits) == 3, repr(hits))
for i in hits:
    chk(f'E {i + 1} 행 다음 줄 = tortuosity_all_mean', i + 1 < len(lines) and 'tortuosity_all_mean' in lines[i + 1],
        lines[i + 1][:120] if i + 1 < len(lines) else '')

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
sys.exit(1 if _fail else 0)

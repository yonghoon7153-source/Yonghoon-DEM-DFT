#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S0 단계 1 메모리 고침 — 옛 판 (커밋 3b12fbe2d 의 carbon_junction.py) ↔ 새 판 (작업 트리) 측정 (합성 침대 · 2026-11-06).

측정마다 새 자식 프로세스 (`--child`) — 최대 RSS (ru_maxrss · 그 프로세스) · 시간 · 상태를 잰다.  옛 판은 주소 공간 상한 (RLIMIT_AS ·
기본 6 GB) 안에서만 돌린다 (이 기계 15 GB 보호 · 상한에 걸리면 'MemoryError' 또는 신호로 기록).  옛 판의 후보 수는 부모가
`cKDTree.count_neighbors` 로 **저장 없이 정확히** 센다 (옛 반지름 2·max(선분 반 길이) + D).
측정 둘 — ① carbon_junction `_distinct_instances` + `_self_pairs` (옛 = 3b12fbe2d) ② S0 `fiber_sphere_instances` 를 SDCP 밀도 구 (DBE 킷
0.64 /µm³ · 반지름 0.15 · tol 0.05) 로 (옛 = ca_s0_census.py 39104710a · 단계 2 위험의 합성 실측).

  python3 docs/reviews/rint2_s0_mem_fix_20261106/tools/mem_measure.py [--out FILE.json] [--cap-gb 6]

값 (σ · census) 은 쓰지 않는다 — 기하 후보 수 · instance 수 · 메모리 · 시간만.
"""
import argparse
import importlib.util
import json
import os
import resource
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SCRIPTS = os.path.join(ROOT, 'scripts')
REF = '3b12fbe2d'
REF_S0 = '39104710a'
D, T = 0.2, 0.15            # 생산 꼴 (r_f 0.075 · tol_ff 0.05)
RHO_SDCP = 116532 / (50.0082 * 50.0082 * 72.534)    # DBE 킷 SDCP 점 / 상자 (재압밀 기록 README · 주기 50.0082 µm · 두께 72.534 µm)
FS_CASES = (3, 4)           # fiber_sphere 측정 침대 = CASES 의 D · E (실침대 밀도 · 긴 선분 있음 · 없음)

#  (이름, seed, 걸음 섬유 수, 점 수, 점 간격, 상자, 긴 두 점 섬유 수, 긴 섬유 길이, 방향 지속, 옛 판도 돌릴지)
CASES = (
    ('A 2k (PEQ C 꼴)', 29, 90, 24, 0.06, 2.5, 2, 2.0, 0.3, True),
    ('B 7k (PMEM 꼴)', 5, 120, 60, 0.06, 8.0, 4, 6.0, 0.3, True),
    ('C 7k 긴 선분 없음 (대조)', 5, 120, 60, 0.06, 8.0, 0, 0.0, 0.3, True),
    ('D 37k 실침대 밀도 (9.07 /µm³ · 간격 0.1 · 긴 선분 8 µm 4 개)', 41, 930, 40, 0.1, 16.0, 4, 8.0, 0.1, False),
    ('E 37k 실침대 밀도 · 긴 선분 없음', 41, 930, 40, 0.1, 16.0, 0, 0.0, 0.1, False),
)


def walk(np, seed, nf, npts, step, box, n_long, long_len, persist):
    rng = np.random.default_rng(seed)
    polys = []
    for _ in range(nf):
        p = rng.uniform(0.3, box - 0.3, 3)
        d = rng.normal(size=3)
        d /= np.linalg.norm(d)
        pts = [p.copy()]
        for _ in range(npts - 1):
            d = d + persist * rng.normal(size=3)
            d /= np.linalg.norm(d)
            p = p + step * d
            pts.append(p.copy())
        polys.append(np.asarray(pts))
    for _ in range(n_long):
        p = rng.uniform(0.3, box - 0.3, 3)
        d = rng.normal(size=3)
        d /= np.linalg.norm(d)
        polys.append(np.asarray([p, p + long_len * d]))
    return polys


def segs_of(np, CJ, polys):
    P, PH, F, K = [], [], [], []
    for x, pts in enumerate(polys):
        P.append(pts); PH.append(np.full(len(pts), 2)); F.append(np.full(len(pts), 10 + 10 * x)); K.append(np.ones(len(pts), int))
    P = np.vstack(P); PH = np.concatenate(PH).astype(np.int64); F = np.concatenate(F).astype(np.int64)
    K = np.concatenate(K).astype(np.int64)
    rej = []
    paths = CJ._paths_of(P, PH, F, K, 2, rej, 'VGCF')
    ok = CJ._canonical_paths([(f, r, kp) for f, r, kp in paths if kp], P, rej, 'VGCF')
    return CJ._segments_of(ok, P, 2.0)[0]


def load_ref():
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{REF}:scripts/carbon_junction.py'], capture_output=True, check=True).stdout
    d = tempfile.mkdtemp(prefix='cjref_mem_')
    p = os.path.join(d, 'carbon_junction_ref_mem.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('carbon_junction_ref_mem', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_ref_s0():
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{REF_S0}:scripts/ca_s0_census.py'], capture_output=True, check=True).stdout
    d = tempfile.mkdtemp(prefix='s0ref_mem_')
    p = os.path.join(d, 'ca_s0_census_ref_mem.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('ca_s0_census_ref_mem', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def child_fs(mode, idx, cap_gb):
    """S0 fiber_sphere_instances — SDCP 밀도 구 (실침대 SBE/DBE 상자 기준 0.64 /µm³ · 반지름 0.15 · tol 0.05) · 옛 (39104710a) ↔ 새."""
    if cap_gb > 0:
        cap = int(cap_gb * (1 << 30))
        resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    sys.path.insert(0, SCRIPTS)
    import numpy as np
    import ca_s0_census as S0
    import carbon_junction as CJ
    M = load_ref_s0() if mode == 'old' else S0
    nm, seed, nf, npts, step, box, nl, ll, per, _ = CASES[idx]
    rng = np.random.default_rng(seed + 100)
    polys = walk(np, seed, nf, npts, step, box, nl, ll, per)
    paths = [(10 + 10 * x, S0.pieces_of(q, 2.0)) for x, q in enumerate(polys)]
    n_sd = int(round(RHO_SDCP * box ** 3))
    C = rng.uniform(0.0, box, (n_sd, 3))
    rss0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t0 = time.time()
    rec = {'case': nm, 'mode': f'fiber_sphere_{mode}', 'n_spheres': n_sd, 'cap_gb': cap_gb}
    try:
        r = M.fiber_sphere_instances(paths, C, np.full(n_sd, 0.15), 0.075, 0.05)
        rec.update(status='ok', n_pairs=int(r['n_pairs']), n_instances=int(r['n_instances']))
    except MemoryError as e:
        rec.update(status=f'MemoryError (주소 공간 상한 {cap_gb} GB) {str(e)[:80]}')
    rec['elapsed_s'] = round(time.time() - t0, 3)
    rec['maxrss_before_kb'] = int(rss0)
    rec['maxrss_kb'] = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if mode == 'new':
        rec['pair_search'] = dict(CJ._PAIR_SEARCH_LAST.get('s0_fiber_sphere', {}))
    print('RESULT ' + json.dumps(rec, ensure_ascii=False))


def child(mode, idx, cap_gb):
    if mode.startswith('fs_'):
        return child_fs(mode[3:], idx, cap_gb)
    if cap_gb > 0:
        cap = int(cap_gb * (1 << 30))
        resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    sys.path.insert(0, SCRIPTS)
    import numpy as np
    import carbon_junction as CJ
    M = load_ref() if mode == 'old' else CJ
    nm, seed, nf, npts, step, box, nl, ll, per, _ = CASES[idx]
    segs = segs_of(np, CJ, walk(np, seed, nf, npts, step, box, nl, ll, per))
    rss0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t0 = time.time()
    rec = {'case': nm, 'mode': mode, 'n_segments': int(len(segs['P0'])), 'cap_gb': cap_gb}
    try:
        inst = M._distinct_instances(segs, D, T)
        t1 = time.time()
        sp = M._self_pairs(segs, D, None)
        rec.update(status='ok', n_instances=int(len(inst['fi'])), n_self_pairs=int(len(sp['i'])),
                   t_distinct_s=round(t1 - t0, 3), t_self_s=round(time.time() - t1, 3))
    except MemoryError as e:
        rec.update(status=f'MemoryError (주소 공간 상한 {cap_gb} GB) {str(e)[:80]}')
    rec['elapsed_s'] = round(time.time() - t0, 3)
    rec['maxrss_before_kb'] = int(rss0)
    rec['maxrss_kb'] = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if mode == 'new':
        rec['pair_search'] = {k: dict(v) for k, v in CJ._PAIR_SEARCH_LAST.items()}
    print('RESULT ' + json.dumps(rec, ensure_ascii=False))


def old_count(idx):
    sys.path.insert(0, SCRIPTS)
    import numpy as np
    from scipy.spatial import cKDTree
    import carbon_junction as CJ
    nm, seed, nf, npts, step, box, nl, ll, per, _ = CASES[idx]
    segs = segs_of(np, CJ, walk(np, seed, nf, npts, step, box, nl, ll, per))
    P0, P1 = segs['P0'], segs['P1']
    half = 0.5 * np.linalg.norm(P1 - P0, axis=1)
    rad = 2.0 * float(half.max()) + D
    t = cKDTree(0.5 * (P0 + P1))
    n = len(P0)
    return {'n_segments': int(n), 'old_radius_um': rad, 'old_candidates': (int(t.count_neighbors(t, rad)) - n) // 2,
            'max_seg_len_um': float(2.0 * half.max()), 'mean_seg_len_um': float(2.0 * half.mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--child', nargs=3, metavar=('MODE', 'IDX', 'CAP_GB'))
    ap.add_argument('--out', default='')
    ap.add_argument('--cap-gb', type=float, default=6.0)
    a = ap.parse_args()
    if a.child:
        child(a.child[0], int(a.child[1]), float(a.child[2]))
        return 0
    rows = []
    for idx, c in enumerate(CASES):
        oc = old_count(idx)
        row = {'case': c[0], **oc}
        for mode in (('old', 'new') if c[-1] else ('new',)):
            cap = a.cap_gb if mode == 'old' else 0.0
            p = subprocess.run([sys.executable, os.path.abspath(__file__), '--child', mode, str(idx), str(cap)],
                               capture_output=True, text=True)
            res = None
            for line in p.stdout.splitlines():
                if line.startswith('RESULT '):
                    res = json.loads(line[7:])
            row[mode] = res if res is not None else {'status': f'자식 rc {p.returncode} (신호 = 음수) · 결과 줄 없음',
                                                    'stderr_tail': p.stderr[-300:]}
        rows.append(row)
        n = row.get('new') or {}
        o = row.get('old') or {}
        ps = (n.get('pair_search') or {}).get('distinct') or {}
        print(f"{c[0]}: 선분 {oc['n_segments']} · 최대 선분 {oc['max_seg_len_um']:.3f} µm · 옛 반지름 {oc['old_radius_um']:.3f} → 옛 후보 "
              f"{oc['old_candidates']} · 새 반지름 {ps.get('radius_um')} → 새 후보 {ps.get('n_candidates')} · 새 RSS "
              f"{n.get('maxrss_kb')} kB ({n.get('elapsed_s')} s · {n.get('status')}) · 옛 RSS {o.get('maxrss_kb')} kB "
              f"({o.get('elapsed_s')} s · {o.get('status')})", flush=True)
    fs_rows = []
    for idx in FS_CASES:
        row = {'case': CASES[idx][0]}
        for mode in ('old', 'new'):
            cap = a.cap_gb if mode == 'old' else 0.0
            p = subprocess.run([sys.executable, os.path.abspath(__file__), '--child', f'fs_{mode}', str(idx), str(cap)],
                               capture_output=True, text=True)
            res = None
            for line in p.stdout.splitlines():
                if line.startswith('RESULT '):
                    res = json.loads(line[7:])
            row[mode] = res if res is not None else {'status': f'자식 rc {p.returncode} (신호 = 음수) · 결과 줄 없음',
                                                    'stderr_tail': p.stderr[-300:]}
        fs_rows.append(row)
        n, o = row['new'] or {}, row['old'] or {}
        print(f"fiber_sphere (SDCP 밀도 구 {n.get('n_spheres')}) {row['case']}: 새 RSS {n.get('maxrss_kb')} kB ({n.get('elapsed_s')} s · "
              f"{n.get('status')} · 쌍 {n.get('n_pairs')} · 후보 {(n.get('pair_search') or {}).get('n_candidates')}) · 옛 RSS "
              f"{o.get('maxrss_kb')} kB ({o.get('elapsed_s')} s · {o.get('status')} · 쌍 {o.get('n_pairs')})", flush=True)
    import numpy, scipy
    meta = {'python': sys.version.split()[0], 'numpy': numpy.__version__, 'scipy': scipy.__version__, 'ref_commit': REF,
            'ref_commit_s0': REF_S0, 'D_um': D, 'T_um': T, 'cap_gb_old': a.cap_gb}
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            json.dump({'meta': meta, 'rows': rows, 'fiber_sphere_rows': fs_rows}, fh, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())

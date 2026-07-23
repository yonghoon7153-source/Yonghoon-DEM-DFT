#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 초기압밀 취성 파괴 → per-AM 심각도 CSV (mpm3d_compaction --fracture-scaffold 입력).

frame[5]: DEM Auerbach 분류가 '어디서' 균열이 개시하는지(WHERE)를 계산하고, 이 CSV로
MPM 스캐폴드에 넘겨주면 MPM이 그 형태적 결과(SE가 열린 균열공간으로 흘러듦)를 그린다.

입력: 한 케이스의 atoms.csv + contacts.csv + meta.json(scale, type_map) + am_scaffold CSV.
동작: AM–AM 접촉을 fracture_model.fracture_classify_force_sim 로 분류(SE 접촉은 제외 —
      SE 소성은 Tabor 담당) → per-AM 최악단계 + max(F/P_c) → am_scaffold 각 행을 위치로
      최근접 AM 원자에 매칭(cKDTree) → 심각도 부착.
출력: am_scaffold 와 **행-정렬** 동일 CSV + 두 열 추가: worst_stage_rank(0 intact..4 pulv), f_over_pc.
      → mpm3d_compaction.py --fracture-scaffold 가 행-정렬로 읽어 fragmentation+ AM에 crack-void.

예:
  python scripts/dem_fracture_scaffold.py --case-dir webapp/results/<cid> \
      --am-scaffold docs/data/real14_am_scaffold.csv --out real14_fracture.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fracture_model import STAGE_RANK                       # intact0..pulverization4
from viewer3d_data import aggregate_particle_metrics        # per-AM worst_stage / max F/Pc


def _stream_contacts(path):
    with open(path, newline='') as fh:
        for row in csv.DictReader(fh):
            out = {}
            for k, v in row.items():
                try:
                    out[k] = float(v)
                except (TypeError, ValueError):
                    out[k] = v
            yield out


def _load_atoms(path):
    atoms_by_id = {}
    with open(path, newline='') as fh:
        for r in csv.DictReader(fh):
            try:
                aid = int(float(r['id']))
                atoms_by_id[aid] = {'type': int(float(r['type'])),
                                    'radius': float(r.get('radius', r.get('r', 0.0)) or 0.0),
                                    'x': float(r['x']), 'y': float(r['y']), 'z': float(r['z'])}
            except (KeyError, TypeError, ValueError):
                continue
    return atoms_by_id


def build_fracture_scaffold(atoms_csv, contacts_csv, meta_json, am_scaffold_csv):
    """→ (scaffold_rows[np.ndarray N×M], rank[N], fpc[N], stats dict).  행-정렬 보장."""
    meta = json.loads(open(meta_json).read()) if os.path.exists(meta_json) else {}
    scale = float(meta.get('scale', 1000))
    tmstr = meta.get('type_map', '1:AM_P,2:AM_S')
    type_map = {}
    for item in str(tmstr).split(','):
        if ':' in item:
            k, v = item.split(':', 1); type_map[int(k)] = v.strip()

    atoms_by_id = _load_atoms(atoms_csv)
    agg = aggregate_particle_metrics(_stream_contacts(contacts_csv), atoms_by_id, type_map, scale=scale)
    worst = agg.get('particle_worst_stage', {}) or {}
    maxf = agg.get('particle_max_fpc', {}) or {}

    # AM 원자만 KDTree (SE 제외) — 위치 매칭.  am_scaffold 는 AM만 있음.
    am_ids = [aid for aid, a in atoms_by_id.items()
              if str(type_map.get(a['type'], '')).upper().startswith('AM')]
    if not am_ids:                                           # type_map 이 AM 라벨 아니면(예 1:AM_S,2:SE) 폴백
        am_ids = list(atoms_by_id.keys())
    am_xyz = np.array([[atoms_by_id[i]['x'], atoms_by_id[i]['y'], atoms_by_id[i]['z']] for i in am_ids])

    scaf = np.atleast_2d(np.loadtxt(am_scaffold_csv, delimiter=','))
    sc_xyz = scaf[:, 1:4]                                    # type,x,y,z,r
    try:
        from scipy.spatial import cKDTree
        _, idx = cKDTree(am_xyz).query(sc_xyz, k=1)
    except ImportError:                                      # scipy 없으면 brute-force (작은 N)
        idx = np.array([int(np.argmin(((am_xyz - p) ** 2).sum(1))) for p in sc_xyz])
    d = np.linalg.norm(am_xyz[idx] - sc_xyz, axis=1)

    rank = np.zeros(len(scaf), dtype=int)
    fpc = np.zeros(len(scaf), dtype=float)
    for k, j in enumerate(idx):
        aid = am_ids[int(j)]
        rank[k] = STAGE_RANK.get(worst.get(aid, 'intact'), 0)
        fpc[k] = float(maxf.get(aid, 0.0))
    r_med = float(np.median(scaf[:, 4])) if scaf.shape[1] > 4 and len(scaf) else 0.0
    stats = {'n_scaffold': len(scaf), 'n_am_atoms': len(am_ids),
             'match_dist_med': float(np.median(d)) if len(d) else 0.0,
             'match_dist_max': float(d.max()) if len(d) else 0.0,
             'r_med': r_med,
             'n_micro': int((rank == 1).sum()), 'n_multi': int((rank == 2).sum()),
             'n_frag': int((rank == 3).sum()), 'n_pulv': int((rank >= 4).sum())}
    return scaf, rank, fpc, stats


def write_fracture_scaffold(out_path, scaf, rank, fpc, src_header=''):
    with open(out_path, 'w', newline='') as fh:
        fh.write(f'# {src_header}worst_stage_rank(0 intact..4 pulv), f_over_pc appended '
                 f'(dem_fracture_scaffold.py) — mpm3d --fracture-scaffold 행-정렬 입력\n')
        w = csv.writer(fh)
        for i in range(len(scaf)):
            row = [f'{v:.6f}' for v in scaf[i]] + [int(rank[i]), f'{fpc[i]:.4f}']
            w.writerow(row)


def main(argv=None):
    ap = argparse.ArgumentParser(description='DEM 취성 파괴 → per-AM crack 심각도 CSV (MPM crack-void 입력)')
    ap.add_argument('--case-dir', default='', help='케이스 폴더 (results/<cid>: atoms.csv/contacts.csv/meta.json)')
    ap.add_argument('--atoms', default='', help='atoms.csv (case-dir 대신 직접 지정)')
    ap.add_argument('--contacts', default='', help='contacts.csv')
    ap.add_argument('--meta', default='', help='meta.json (scale, type_map)')
    ap.add_argument('--am-scaffold', required=True, help='am_scaffold CSV (type,x,y,z,r) — 출력이 이것과 행-정렬')
    ap.add_argument('--out', required=True, help='출력 fracture-scaffold CSV')
    a = ap.parse_args(argv)
    cd = a.case_dir
    atoms = a.atoms or os.path.join(cd, 'atoms.csv')
    contacts = a.contacts or os.path.join(cd, 'contacts.csv')
    meta = a.meta or os.path.join(cd, 'meta.json')
    for p in (atoms, contacts):
        if not os.path.exists(p):
            raise SystemExit(f'없음: {p} (--case-dir 또는 --atoms/--contacts 확인)')
    scaf, rank, fpc, st = build_fracture_scaffold(atoms, contacts, meta, a.am_scaffold)
    # ★M2(리뷰): 위치-매칭 거리 게이트 — 다른 전극/프레임 CSV면 KDTree가 무관 입자에 심각도를 붙여도
    #   조용히 그럴싸한 값을 냄.  최대 매칭거리가 AM 반경의 상당 부분을 넘으면 = 다른 전극 → 중단.
    if st['r_med'] > 0 and st['match_dist_max'] > 0.5 * st['r_med']:
        raise SystemExit(f"[fracture] 위치-매칭 최대거리 {st['match_dist_max']:.3g} > 0.5×AM반경중앙값 "
                         f"{st['r_med']:.3g} — atoms.csv와 am_scaffold가 다른 전극/프레임일 가능성.  "
                         "같은 케이스의 atoms/contacts + 그 케이스로 만든 am_scaffold를 쓰세요.")
    if st['r_med'] > 0 and st['match_dist_max'] > 0.1 * st['r_med']:
        print(f"  ⚠ 매칭거리 최대 {st['match_dist_max']:.3g} (AM반경중앙 {st['r_med']:.3g}의 "
              f"{100*st['match_dist_max']/st['r_med']:.0f}%) — 정렬 재확인 권장.")
    write_fracture_scaffold(a.out, scaf, rank, fpc)
    print(f'✓ {a.out}  ({st["n_scaffold"]} AM 행-정렬; 위치매칭 중앙거리 {st["match_dist_med"]:.2g} '
          f'최대 {st["match_dist_max"]:.2g})')
    print(f'  심각도: micro {st["n_micro"]} · multi {st["n_multi"]} · '
          f'frag {st["n_frag"]} · pulv {st["n_pulv"]}  '
          f"(mpm3d --fracture-scaffold {a.out} --fracture-min-stage fragmentation)")
    if st['n_frag'] + st['n_pulv'] == 0:
        print('  ⚠ fragmentation+ 없음 → MPM crack-void는 near-null (DEM 취성은 수송 f_intact에만 반영).')
    return 0


# ─────────────────────────── self-test ───────────────────────────
def _selftest():
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as td:
        # 합성 케이스: 2 AM (id1,2) + 1 SE(id3).  큰 힘의 AM–AM 접촉 → fragmentation/pulv 유도.
        atoms = os.path.join(td, 'atoms.csv'); contacts = os.path.join(td, 'contacts.csv')
        meta = os.path.join(td, 'meta.json'); scaf = os.path.join(td, 'scaf.csv'); out = os.path.join(td, 'out.csv')
        with open(atoms, 'w') as f:
            f.write('id,type,radius,x,y,z\n1,1,0.006,0.02,0.02,0.01\n2,1,0.006,0.032,0.02,0.01\n3,2,0.0005,0.05,0.05,0.02\n')
        # AM_P-AM_P 접촉에 매우 큰 힘 → pulverization (F/P_c ≫ 32).  aggregate는 fn·contact_area 읽음.
        # r_min=0.006·fn=50(sim,/scale) → F_real 0.05N, P_c≈1.45e-3N (K_IC_AMP=0.3e6) → F/P_c≈35 = pulv.
        with open(contacts, 'w') as f:
            f.write('id1,id2,fn,contact_area,delta\n1,2,50,1e-6,1e-5\n')
        with open(meta, 'w') as f:
            f.write('{"scale":1000,"type_map":"1:AM_P,2:AM_S"}')
        with open(scaf, 'w') as f:                          # am_scaffold: 두 AM (원자 위치와 동일)
            f.write('# type,x,y,z,r\n1,0.02,0.02,0.01,0.006\n1,0.032,0.02,0.01,0.006\n')
        s, rank, fpc, st = build_fracture_scaffold(atoms, contacts, meta, scaf)
        if len(s) != 2: fails.append(f'행수 {len(s)}!=2')
        if st['match_dist_max'] > 1e-6: fails.append(f'위치매칭 거리 {st["match_dist_max"]} 큼')
        # 큰 힘 → 두 AM 모두 심각(rank≥3) 이어야 (SE 접촉은 없음)
        if not (rank >= 3).any(): fails.append(f'심각 단계 미검출 (rank={rank.tolist()}, fpc={fpc.tolist()})')
        write_fracture_scaffold(out, s, rank, fpc)
        r2 = np.atleast_2d(np.loadtxt(out, delimiter=','))
        if r2.shape[1] != s.shape[1] + 2: fails.append(f'출력 열수 {r2.shape[1]} != {s.shape[1]}+2')
        if not np.allclose(r2[:, -2], rank): fails.append('rank 왕복 불일치')
    print('selftest OK' if not fails else 'selftest FAIL: ' + '; '.join(fails))
    return 1 if fails else 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        raise SystemExit(_selftest())
    raise SystemExit(main())

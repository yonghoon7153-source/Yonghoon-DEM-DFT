#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T2b — 응력과 같은 step 네 단계의 porosity = **exact union** (1저자 10-12 *"exact union으로 해야지"* · LHS 배포와 같은 양).

단계 = 체크포인트 step (1저자 10-12 *"3D porosity를 저때로 맞추면 좋을듯"*):
  400,000 (Initial · 판 닿기 전) · 1,650,000 (47.1 MPa) · 3,100,000 (296.2 MPa) · 3,220,000 (이완 · 165.3 MPa).
입력 (읽기만):
  세 체크포인트 = 1저자 WSL 스냅숏 (`make_snap_decks.py` · run 0) 의 파서 출력 `<snap-root>/ps73_snap_<S>/ana/atoms.csv` · `mesh_info.json`
  3,220,000 = ibb 묶음 atom 덤프 (common.atom_path · t2_porosity 와 같은 입력)
계산 = t2_porosity.py 와 같은 함수 · 같은 MC (4e6 점 · seed crc32('ps_7_3_r45')) · 상자 50 × 50 µm · 높이 = 판 높이.
  ε_union = scripts/dem_analysis_core.calc_porosity_union_exact  ← 보고 값 (CSV 는 이것만)
  ε_sphere = scripts/dem_analysis_core.calc_porosity              ← JSON 기록만 (그림 · CSV 에 안 씀)
검사: 스냅숏 판 높이 (mesh_info) = curve/plate.csv · 원자 수 = thermo (160,420 · 이완 160,417) · id 중복 없음 · 3,220,000 union = t2 기록 (16.4941) 재현.

  cd OUT && python3 -I -B code/t2b_union_ckpt.py --snap-root <폴더>
"""
import argparse
import csv
import json
import math
import sys
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

MC_N = 4_000_000
SEED = zlib.crc32(C.CASE.encode())
ODIR = C.OUT / 'aligned_ckpt'
STAGES = [
    ('initial', 'Initial (before plate contact)', 400000, 'snap'),
    ('p50', '47 MPa (compression)', 1650000, 'snap'),
    ('p300', '296 MPa (just before stop)', 3100000, 'snap'),
    ('relaxed', 'After relaxation', 3220000, 'dump'),
]
#: 원자 수 = 그 step thermo 줄 — 이완 시작 (3,125,000 → 3,130,000) 에 바닥 SE 3 개가 사라졌다 (README §4 · aux_missing_atoms.json)
N_ATOMS = {400000: 160420, 1650000: 160420, 3100000: 160420, 3220000: 160417}


def pressure_table():
    out = {}
    with open(C.CURVE_DIR / 'curve' / 'pressure.csv', newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if r['pressure_mpa'] not in ('', None):
                out[int(r['step'])] = float(r['pressure_mpa'])
    return out


def read_snap_atoms(root, step):
    ana = Path(root) / f'ps73_snap_{step}' / 'ana'
    atoms = {}
    with open(ana / 'atoms.csv', newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            i = int(float(r['id']))
            if i in atoms:
                raise SystemExit(f'⛔ {step}: id 중복 {i}')
            atoms[i] = {'x': float(r['x']), 'y': float(r['y']), 'z': float(r['z']),
                        'radius': float(r['radius']), 'type': int(float(r['type']))}
    mi = json.loads((ana / 'mesh_info.json').read_text(encoding='utf-8'))
    return atoms, float(mi['plate_z']), {'atoms_csv_sha256': C.sha256(ana / 'atoms.csv'),
                                         'mesh_info_sha256': C.sha256(ana / 'mesh_info.json'), 'mesh_source': mi.get('source')}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--snap-root', required=True)
    a = ap.parse_args(argv)
    import dem_analysis_core as WEB
    ODIR.mkdir(parents=True, exist_ok=True)
    plate, press = C.plate_table(), pressure_table()
    rows = []
    for key, label, step, src in STAGES:
        if src == 'snap':
            atoms, pz, inp = read_snap_atoms(a.snap_root, step)
            if pz != plate[step][0]:
                raise SystemExit(f'⛔ {step}: 스냅숏 판 높이 {pz} ≠ plate.csv {plate[step][0]}')
        else:
            atoms, _A, info = C.read_atoms(step)
            pz = plate[step][0]
            inp = {'atom_dump_sha256': C.sha256(C.atom_path(step))}
        if len(atoms) != N_ATOMS[step]:
            raise SystemExit(f'⛔ {step}: 원자 {len(atoms)} ≠ {N_ATOMS[step]}')
        t0 = time.time()
        un = WEB.calc_porosity_union_exact(atoms, pz, box_xy=0.05, box_y=0.05, mc_n=MC_N, seed=SEED)
        if un['union_exact_status'] != 'OK':
            raise SystemExit(f'⛔ union 상태 {un["union_exact_status"]} @ {step}')
        eps_s = float(WEB.calc_porosity(atoms, pz, box_xy=0.05, box_y=0.05))
        rec = {'stage_key': key, 'stage': label, 'step': step, 'time_ms': step * C.STEP_MS, 'plate_pressure_MPa': press.get(step),
               'plate_um': pz * C.SCALE, 'eps_union_pct': un['porosity_union_exact_pct'], 'union_mc_std_pct': un['porosity_union_exact_se_pct'],
               'eps_sphere_pct_RECORD_ONLY': eps_s, 'union_mc_n': un['union_exact_mc_n'], 'union_mc_seed': un['union_exact_mc_seed'],
               'input': {'source': src, **inp}, 'seconds': round(time.time() - t0, 1)}
        print(f'  {key:8s} {step:>8d}  판 {rec["plate_um"]:.3f} µm  {rec["plate_pressure_MPa"]} MPa  ε_union {rec["eps_union_pct"]:.4f} ± '
              f'{rec["union_mc_std_pct"]:.4f} %  (ε_sphere {eps_s:.4f} · 기록만)  {rec["seconds"]} s', flush=True)
        rows.append(rec)
    ref = 16.4941
    r3220 = rows[-1]['eps_union_pct']
    if abs(r3220 - ref) > 5e-5:
        raise SystemExit(f'⛔ 3,220,000 union {r3220:.6f} ≠ t2 기록 {ref} (같은 입력 · 같은 시드)')
    head = ['Simulation time', 'Porosity (exact union)', 'Union MC std', 'Plate pressure', 'Plate height', 'Step', 'Stage']
    units = ['ms', '%', '%', 'MPa', 'µm', '', '']
    comm = ['step × 1e-3', '1 − V_union/(A·H) · MC 4e6 points · seed crc32(ps_7_3_r45) — same quantity as LHS porosity_union_exact_pct',
            'binomial 1σ (yErr of B)', 'curve/pressure.csv', 'H = plate mesh', '', '']
    C.write_origin_csv(ODIR / 'ps73_ckpt_porosity_exact_union_origin.csv', head, units,
                       [(f'{r["time_ms"]:.3f}', f'{r["eps_union_pct"]:.4f}', f'{r["union_mc_std_pct"]:.4f}',
                         f'{r["plate_pressure_MPa"]:.2f}', f'{r["plate_um"]:.3f}', r['step'], r['stage']) for r in rows], comm)
    C.write_json(ODIR / 'ps73_ckpt_porosity.json', {'tool': 't2b_union_ckpt', 'reported_quantity': 'eps_union_pct (exact union)',
                                                     'mc_n': MC_N, 'seed': SEED, 'check_3220000_vs_t2': {'got': r3220, 'ref': ref}, 'rows': rows})
    print(f'쓴 파일 {ODIR.name}/ps73_ckpt_porosity_exact_union_origin.csv · ps73_ckpt_porosity.json')


if __name__ == '__main__':
    main()

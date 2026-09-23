#!/usr/bin/env python3
"""수확기 porosity ↔ 웹앱 porosity — **같은 덤프**에서 두 코드의 함수를 그대로 불러 맞댄다 (LHS-10 · 판단 J8).

왜: 수확기 (`lhs_descriptor_harvest.volumes_and_phi`) 는 분모 높이를 덤프 `BOX BOUNDS` 바닥에서 잰다
    (H = plate_z − box_lo_z).  웹앱 (`dem_analysis_core.calc_porosity`) 은 벽 z = 0 에서 잰다 (V_box = L² · plate_z).
    LHS 덱은 상자를 벽보다 10 µm 아래서 시작해 둘이 갈린다.  이 도구는 수식을 옮겨 적지 않고 **두 코드의 함수를
    호출**한다 — 바닥 말고 다른 차이 (plate_z 출처 · 반경 · 원자 수) 가 있어도 잔차로 드러난다.
    (웹앱 φ_SE 를 내는 `calc_effective_conductivity` 는 τ 가 없으면 None 이다 — `DESC-01` — 그래서 porosity 로 맞댄다.
    φ 는 porosity 와 같은 분모를 쓰므로 바닥 판정은 porosity 하나로 충분하다.)

덤으로 **플래튼 − 고체 윗면** (`plate_gap`) 을 잰다 — 수확기가 원자 step 보다 이른 메시를 쓰면 (`latest_le`)
플래튼이 아직 높을 때의 위치라 이 틈이 커진다 (LHS-11).  같은 step 메시면 틈은 작아야 한다.

판정 (케이스마다):
    FLOOR_ONLY — ε_web == 100·(1 − (1 − ε_harv/100)·H_harv/H_web) (|잔차| < 1e-9 %p): 차이가 **바닥 하나로 전부** 설명된다
    SAME       — 두 값이 같다 (상자 바닥 = 벽)
    OTHER      — 바닥으로 설명 안 되는 잔차가 있다 → 다른 차이를 찾아야 한다

사용:
    python3 scripts/lhs_phi_crosscheck.py --cohort <봉인 코호트 TSV> [--root-from A --root-to B] [--case lhs00_000 …] --out x.tsv
    python3 scripts/lhs_phi_crosscheck.py --selftest
"""
import argparse
import csv
import os
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lhs_descriptor_harvest as HV          # noqa: E402
import lhs_harvest_batch as HB               # noqa: E402
import dem_analysis_core as WEB              # noqa: E402

TOL = 1e-9


def compare(atom_path, plate_z, n_types):
    atoms, lo, hi, _bc = HV.read_atom_dump(atom_path)
    labels, _tmap = HV.phase_labels(atoms['type'], n_types)
    h = HV.volumes_and_phi(atoms, labels, lo, hi, plate_z)
    lx, ly = float(hi[0] - lo[0]), float(hi[1] - lo[1])
    web_atoms = {k: {'radius': float(r)} for k, r in enumerate(atoms['radius'])}
    eps_w = float(WEB.calc_porosity(web_atoms, plate_z, box_xy=lx))
    eps_h = float(h['porosity_sphere_pct_RECORD_ONLY'])
    h_h, h_w = float(h['H_sim']), float(plate_z)
    pred = 100.0 * (1.0 - (1.0 - eps_h / 100.0) * h_h / h_w)
    resid = eps_w - pred
    if abs(eps_w - eps_h) < TOL:
        verdict = 'SAME'
    elif abs(resid) < TOL:
        verdict = 'FLOOR_ONLY'
    else:
        verdict = 'OTHER'
    solid_top = float((atoms['z'] + atoms['radius']).max())
    solid_bot = float((atoms['z'] - atoms['radius']).min())
    return dict(plate_z=h_w, box_lo_z=float(lo[2]), floor_gap=h_h - h_w, lx=lx, ly=ly,
                solid_top=solid_top, solid_bot=solid_bot, plate_gap=h_w - solid_top,
                square=abs(lx - ly) < 1e-12, eps_harvest=eps_h, eps_webapp=eps_w,
                phi_scale=h_w / h_h if h_h else None, resid=resid, verdict=verdict)


def run_cohort(args):
    rows = HB.read_cohort(Path(args.cohort))
    want = set(args.case)
    out = []
    for row in rows:
        if want and row['case'] not in want:
            continue
        atom = HB.remap(row['atom_file'], args.root_from, args.root_to)
        rec = {'case': row['case']}
        mesh, how, note = HB.pick_mesh(atom)
        if not atom.is_file() or mesh is None:
            rec.update(verdict='MISSING', note=f'atom {atom.is_file()} · mesh {how} {note}')
            out.append(rec)
            continue
        try:
            rec.update(compare(str(atom), HV.plate_z_from_stl(str(mesh)), int(row['n_types'])))
            rec['mesh_pick'] = how
        except Exception as e:                                  # noqa: BLE001
            rec.update(verdict='ERROR', note=f'{type(e).__name__}: {e}'[:160])
        out.append(rec)
    keys = ['case', 'verdict', 'plate_z', 'box_lo_z', 'floor_gap', 'solid_top', 'solid_bot', 'plate_gap',
            'lx', 'ly', 'square', 'eps_harvest',
            'eps_webapp', 'phi_scale', 'resid', 'mesh_pick', 'note']
    with open(args.out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=keys, delimiter='\t', extrasaction='ignore')
        w.writeheader()
        for r in out:
            w.writerow(r)
    ok = [r for r in out if r['verdict'] in ('SAME', 'FLOOR_ONLY', 'OTHER')]
    cnt = {v: sum(r['verdict'] == v for r in out) for v in ('SAME', 'FLOOR_ONLY', 'OTHER', 'MISSING', 'ERROR')}
    print(f'케이스 {len(out)} · ' + ' · '.join(f'{k} {v}' for k, v in cnt.items()))
    if ok:
        gaps = sorted(r['floor_gap'] for r in ok)
        print(f'바닥 틈 (H_harv − H_web, sim 단위): min {gaps[0]:.6g} · max {gaps[-1]:.6g}')
        print(f'porosity 중앙 — 수확기 {st.median(r["eps_harvest"] for r in ok):.2f} % · '
              f'웹앱 {st.median(r["eps_webapp"] for r in ok):.2f} %')
        print(f'φ 배율 (웹앱/수확기) min {min(r["phi_scale"] for r in ok):.4f} · max {max(r["phi_scale"] for r in ok):.4f}')
        print(f'최대 |잔차| {max(abs(r["resid"]) for r in ok):.3e} %p · 정사각 아님 {sum(not r["square"] for r in ok)} 건')
        for how in sorted({r.get('mesh_pick') for r in ok}):
            g = sorted(r['plate_gap'] for r in ok if r.get('mesh_pick') == how)
            print(f'플래튼 − 고체 윗면 ({how}, n={len(g)}): min {g[0]:.6g} · 중앙 {st.median(g):.6g} · max {g[-1]:.6g}')
    print(f'→ {args.out}')
    return 0 if not cnt['OTHER'] and not cnt['ERROR'] else 1


def selftest():
    import tempfile
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        print(('  ✓ ' if cond else '  ✗ ') + name)
        ok, fail = ok + bool(cond), fail + (not cond)

    print('lhs_phi_crosscheck — 자기검사')
    rows = [(1, 2.0, 2.0, 1.0, 0.5, 1), (2, 5.0, 5.0, 2.0, 0.5, 2), (3, 8.0, 3.0, 3.0, 0.5, 3)]
    with tempfile.TemporaryDirectory() as tmp:
        # ① LHS 덱 모양: 상자 바닥 −1, 벽 0, 플래튼 5 ⇒ 차이는 바닥 하나로 전부 설명된다
        a1 = HV._atom_file(tmp, rows, name='atom_a.liggghts', lo=(0.0, 0.0, -1.0), hi=(10.0, 10.0, 20.0))
        r1 = compare(a1, 5.0, 3)
        chk('상자 바닥이 벽 아래면 FLOOR_ONLY (LHS-10 재현)', r1['verdict'] == 'FLOOR_ONLY')
        chk('바닥 틈 = 1.0 (상자 −1 ↔ 벽 0)', abs(r1['floor_gap'] - 1.0) < 1e-12)
        chk('수확기 porosity 가 웹앱보다 크다 (분모가 부푼다)', r1['eps_harvest'] > r1['eps_webapp'])
        chk('φ 배율 = H_web / H_harv = 5/6', abs(r1['phi_scale'] - 5.0 / 6.0) < 1e-12)
        chk('플래튼 − 고체 윗면 = 5 − 3.5 = 1.5 (가장 높은 알 z 3 + r 0.5)', abs(r1['plate_gap'] - 1.5) < 1e-12)
        # ② 음성 대조: 상자 바닥 = 벽 ⇒ 두 코드가 같은 값
        a2 = HV._atom_file(tmp, rows, name='atom_b.liggghts', lo=(0.0, 0.0, 0.0), hi=(10.0, 10.0, 20.0))
        chk('음성 대조: 상자 바닥 = 벽이면 SAME', compare(a2, 5.0, 3)['verdict'] == 'SAME')
    print(f'\nselftest: {ok} 통과 / {fail} 실패')
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='수확기 ↔ 웹앱 porosity 교차검사 (LHS-10)')
    ap.add_argument('--cohort', default=str(HB.COHORT))
    ap.add_argument('--case', action='append', default=[])
    ap.add_argument('--root-from', default='')
    ap.add_argument('--root-to', default='')
    ap.add_argument('--out', default='lhs_phi_crosscheck.tsv')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    return run_cohort(a)


if __name__ == '__main__':
    sys.exit(main())

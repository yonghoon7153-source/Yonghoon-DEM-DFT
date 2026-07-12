#!/usr/bin/env python3
"""uma_md_interface.py — SDCP/LiNiO2 계면 UMA MD (300 K): 수소결합·양성자 이동 이벤트 추적.

정적 스크린(클린면 6배향 + 수산화면 6배치)이 양방향 모두 수소결합 0을 판정했다.
남은 질문: 열운동(300 K)이 켜지면 과도적(transient) 수소결합/이동이 나타나는가?

  python3 uma_md_interface.py --xyz complex_sulfdown_r90.xyz --out md_sulfdown_r90 \
      [--n_slab 96 --n_ads 9 --T 300 --dt 1.0 --ps 5 --device cuda]

추적(10스텝마다): 산성 O-H 길이 / 산성H→표면O(격자+수산기) 최단 / 표면OH의 H→분자O 최단.
끝나면 수소결합 점유율(%)과 TRANSFER 이벤트(산성 O-H > 1.3 A) 목록 출력.
주의: UMA는 전하분리를 못 다루므로 TRANSFER는 후보일 뿐 — 반드시 DFT 재검.
슬랩 원자(--n_slab)는 동결, 수산기 패치와 분자는 자유. GPU 잔여 ~5 GB에 공존 가능.
"""
import argparse
import os
import numpy as np

from ase.io import read, write
from ase.constraints import FixAtoms
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase import units
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator


def find_acid_global(atoms):
    """복합체 전체에서 설포네이트 S/O/산성H를 mic 거리로 탐지 (슬랩엔 S가 없어 유일함이 보장).
    스크린의 수산기 패치가 6~9원자로 가변이라 고정 슬라이스는 어긋난다 — 전역 탐지가 정답."""
    sym = atoms.get_chemical_symbols()
    allO = [i for i, s in enumerate(sym) if s == "O"]
    allH = [i for i, s in enumerate(sym) if s == "H"]
    sS = None
    for i, s in enumerate(sym):
        if s != "S":
            continue
        d = atoms.get_distances(i, allO, mic=True)
        if sum(1 for x in d if x < 1.8) >= 3:
            sS = i
            break
    assert sS is not None, "sulfonate S not found"
    dSO = atoms.get_distances(sS, allO, mic=True)
    sO = [allO[k] for k, x in enumerate(dSO) if x < 1.8]
    for o in sO:
        d = atoms.get_distances(o, allH, mic=True)
        for k, x in enumerate(d):
            if x < 1.15:
                return o, allH[k], sO
    raise SystemExit("acidic H not found — doped xyz를 넣었나? 중성 복합체를 사용할 것")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True, help="정적 스크린이 저장한 complex_*.xyz")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n_slab", type=int, default=96, help="동결할 슬랩 원자 수 (앞쪽 인덱스)")
    ap.add_argument("--n_mol", type=int, default=35, help="분자 원자 수 (중성 v7c = 35; 뒤쪽 인덱스)")
    ap.add_argument("--T", type=float, default=300.0)
    ap.add_argument("--dt", type=float, default=1.0, help="fs (H 있으므로 1 fs 권장)")
    ap.add_argument("--ps", type=float, default=5.0)
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device=a.device),
                              task_name="oc20")
    atoms = read(a.xyz)
    sym = atoms.get_chemical_symbols()
    mol_start = len(atoms) - a.n_mol                       # 분자 = 마지막 n_mol 원자
    n_ads = mol_start - a.n_slab                           # 수산기 패치 크기는 자동 산출 (6~9 가변)
    assert n_ads >= 0, f"n_slab({a.n_slab})+n_mol({a.n_mol}) > 전체 원자수 {len(atoms)}"
    atoms.set_constraint(FixAtoms(indices=list(range(a.n_slab))))
    atoms.calc = calc
    print(f"atoms {len(atoms)} = slab {a.n_slab} + ads {n_ads} + mol {a.n_mol}", flush=True)

    iO, iH, sO = find_acid_global(atoms)
    molO = [i for i in range(mol_start, len(atoms)) if sym[i] == "O"]
    ztop = atoms.positions[:a.n_slab, 2].max()
    surfO = [i for i in range(a.n_slab) if sym[i] == "O"
             and atoms.positions[i, 2] > ztop - 1.4]
    adsO = [i for i in range(a.n_slab, mol_start) if sym[i] == "O"]
    adsH = [i for i in range(a.n_slab, mol_start) if sym[i] == "H"]
    accO = surfO + adsO                                    # 산성 H의 억셉터 후보

    MaxwellBoltzmannDistribution(atoms, temperature_K=a.T)
    dyn = Langevin(atoms, a.dt * units.fs, temperature_K=a.T, friction=0.02)

    nsteps = int(a.ps * 1000 / a.dt)
    trackf = open(os.path.join(a.out, "md_track.csv"), "w")
    trackf.write("t_fs,T_K,acid_OH_A,acidH_to_surfO_A,surfH_to_molO_A\n")
    stats = {"hb_acid": 0, "hb_rev": 0, "n": 0}
    transfers = []

    def snap():
        t = dyn.get_number_of_steps() * a.dt
        doh = float(atoms.get_distance(iH, iO, mic=True))
        d1 = float(min(atoms.get_distances(iH, accO, mic=True)))
        d2 = min((float(min(atoms.get_distances(h, molO, mic=True))) for h in adsH),
                 default=9.9)
        Tk = atoms.get_temperature()
        trackf.write(f"{t:.0f},{Tk:.0f},{doh:.3f},{d1:.2f},{d2:.2f}\n")
        stats["n"] += 1
        if d1 <= 2.2:
            stats["hb_acid"] += 1
        if d2 <= 2.2:
            stats["hb_rev"] += 1
        if doh > 1.30:
            transfers.append((t, doh, d1))
        if stats["n"] % 25 == 0:
            print(f"  t={t:6.0f} fs  T={Tk:3.0f} K  O-H {doh:.3f}  "
                  f"acidH..surfO {d1:.2f}  surfH..molO {d2:.2f}", flush=True)
            trackf.flush()

    def dump():
        write(os.path.join(a.out, "traj.xyz"), atoms, append=True)

    dyn.attach(snap, interval=10)
    dyn.attach(dump, interval=50)
    print(f"MD start: {nsteps} steps × {a.dt} fs = {a.ps} ps @ {a.T} K  ({a.xyz})", flush=True)
    dyn.run(nsteps)
    trackf.close()

    n = max(stats["n"], 1)
    print("\n=== MD 요약 ===")
    print(f"수소결합 점유율: 산성H→표면O {100*stats['hb_acid']/n:.1f}% | "
          f"표면OH→분자O {100*stats['hb_rev']/n:.1f}%  (기준 2.2 A, {n} 샘플)")
    if transfers:
        t0, doh, d1 = transfers[0]
        print(f"⚠ TRANSFER 이벤트 {len(transfers)}건 — 첫 발생 t={t0:.0f} fs (O-H {doh:.2f} A). "
              f"UMA는 전하분리 불가 → 해당 스냅샷 DFT 재검 필수")
    else:
        print("양성자 이동 이벤트 없음 (O-H ≤ 1.3 A 유지)")
    print(f"saved: {a.out}/md_track.csv, traj.xyz")


if __name__ == "__main__":
    main()

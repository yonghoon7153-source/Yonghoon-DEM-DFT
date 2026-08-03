#!/usr/bin/env python3
"""make_slab_relax.py — 깨끗한 LiNiO2(104) 슬랩의 **표면 이완** QE 입력을 만든다.

왜 필요한가
  build_linio2_slab.py 가 내는 슬랩은 **이상적 벌크 절단면**이라 표면 Ni/O 가 아직 벌크
  자리에 있다. (104) 표면 이완만으로 표면당 0.3-1.0 eV 급이라, 이걸 안 풀고 E_bind 절대값을
  쓰면 흡착에너지에 표면 이완 몫이 섞인다.
  ⚠ E_bind = E(복합체) - E(슬랩) - E(분자) 에서 **슬랩 기준도 같은 자유도로 이완**해야
    상쇄된다. 복합체만 이완하고 슬랩 기준을 안 이완하면 그 차이가 통째로 E_bind 에 남는다.

⚠⚠ **1x1 (48원자)로 이완하고 나중에 1x4 로 복제한다.** 192원자 DFT+U relax 는 이 자원에서
  6-15일이라 불가능하다. 깨끗한 표면의 이완은 재구성이 없으면 1x1 주기를 보존하므로,
  1x1 을 이완해 복제한 것과 1x4 를 직접 이완한 것이 **같다**. (재구성이 일어나면 다르지만,
  그건 이완 후 1x4 단일점으로 힘을 재보면 바로 드러난다 — 아래 3단계.)

  1단계  python3 tools/sdcp/make_slab_relax.py --out <dir>      # 1x1 48원자 relax 입력
  2단계  (gabia 에서 relax 실행)
  3단계  python3 tools/sdcp/make_slab_relax.py --harvest <dir>  # 이완좌표 -> 1x4 192원자

AFM: R-3m LiNiO2 는 면내(G-type) 반강자성이다. 기존 파이프라인의 판정
     (`phaseB_v7c_dft_binding.py` afm_inplane)과 같은 규약 — z-밴드 안에서 전역 교대.
"""
import argparse
import os
import sys

import numpy as np
from ase.io import read, write

ECUTWFC, ECUTRHO = 60.0, 480.0
DEGAUSS = 0.03
CONV_THR = 1.0e-6
MIX_BETA, MIX_NDIM = 0.03, 20
U_NI = 6.2
PSEUDOS = {
    'Li':  ('6.940',  'li_pbe_v1.4.uspp.F.UPF'),
    'Ni1': ('58.690', 'ni_pbe_v1.4.uspp.F.UPF'),
    'Ni2': ('58.690', 'ni_pbe_v1.4.uspp.F.UPF'),
    'O':   ('15.999', 'O.pbe-n-kjpaw_psl.0.1.UPF'),
}
ORDER = ['Li', 'Ni1', 'Ni2', 'O']


def zbands(at, tol=0.5):
    """(104) 면 단위로 z 를 묶는다 → [(z평균, [원자인덱스])]."""
    z = at.positions[:, 2]
    order = np.argsort(z)
    g = [[order[0]]]
    for k in order[1:]:
        if z[k] - z[g[-1][-1]] > tol:
            g.append([])
        g[-1].append(k)
    return [(float(z[q].mean()), q) for q in g]


def afm_labels(at):
    """면내 G-type: 각 z-밴드 안에서 (x,y) 정렬 후 전역 교대."""
    lab = list(at.get_chemical_symbols())
    flip = 0
    for _, idx in zbands(at):
        ni = [i for i in idx if lab[i] == 'Ni']
        ni.sort(key=lambda i: (round(at.positions[i, 0], 3), round(at.positions[i, 1], 3)))
        for i in ni:
            lab[i] = 'Ni1' if flip % 2 == 0 else 'Ni2'
            flip += 1
    return lab


def write_relax(path, at, lab, fixed, kpts, prefix):
    n1, n2 = lab.count('Ni1'), lab.count('Ni2')
    if n1 != n2:
        sys.exit(f"⛔ AFM 이 불균형이다 (Ni1 {n1} / Ni2 {n2}) — 총 자화가 0 이 안 된다")
    present = [s for s in ORDER if s in lab]
    L = ["&CONTROL", "    calculation     = 'relax'", f"    prefix          = '{prefix}'",
         "    outdir          = './tmp'", "    pseudo_dir      = '/data/work/pseudo'",
         "    tprnfor         = .true.", "    tstress         = .false.",
         "    disk_io         = 'low'", "    nstep           = 80",
         "    forc_conv_thr   = 1.0d-3", "    etot_conv_thr   = 1.0d-4", "/",
         "&SYSTEM", "    ibrav           = 0", f"    nat             = {len(at)}",
         f"    ntyp            = {len(present)}",
         f"    ecutwfc         = {ECUTWFC}", f"    ecutrho         = {ECUTRHO}",
         "    occupations     = 'smearing'", "    smearing        = 'mv'",
         f"    degauss         = {DEGAUSS}",
         "    nspin           = 2", "    nosym           = .true.",
         # ⚠ **분산 보정 (2026-08-03 리뷰 지적).** repo 전체에 vdw_corr 가 한 줄도 없었다.
         #   맨 슬랩엔 영향이 작지만, 흡착 단계와 **같은 범함수를 써야** E_bind 가 성립하므로
         #   여기서부터 켠다.
         "    vdw_corr        = 'grimme-d3'"]
    for k, sp in enumerate(present, 1):
        if sp == 'Ni1':
            L.append(f"    starting_magnetization({k}) = +0.300")
        elif sp == 'Ni2':
            L.append(f"    starting_magnetization({k}) = -0.300")
        elif sp == 'Li':
            L.append(f"    starting_magnetization({k}) = 0.0")
    L += ["/", "&ELECTRONS", f"    conv_thr        = {CONV_THR}",
          f"    mixing_beta     = {MIX_BETA}", "    mixing_mode     = 'local-TF'",
          f"    mixing_ndim     = {MIX_NDIM}", "    electron_maxstep = 300",
          "    diagonalization = 'david'", "    diago_david_ndim = 2", "/",
          "&IONS", "    ion_dynamics    = 'bfgs'", "/", "",
          "ATOMIC_SPECIES"]
    for sp in present:
        m, pp = PSEUDOS[sp]
        L.append(f"  {sp:<3s} {m:>8s}  {pp}")
    L += ["", "HUBBARD ortho-atomic", f"U Ni1-3d {U_NI}", f"U Ni2-3d {U_NI}", "",
          "CELL_PARAMETERS angstrom"]
    for v in at.cell.array:
        L.append(f"  {v[0]:18.12f} {v[1]:18.12f} {v[2]:18.12f}")
    L += ["", "ATOMIC_POSITIONS angstrom"]
    for i, (s, p) in enumerate(zip(lab, at.positions)):
        # ⚠ 고정 원자는 if_pos 0 0 0. 슬랩 기준과 복합체가 **같은 원자를 고정**해야
        #   E_bind 에서 고정 조건이 상쇄된다.
        f = "  0 0 0" if i in fixed else "  1 1 1"
        L.append(f"  {s:<3s} {p[0]:18.12f} {p[1]:18.12f} {p[2]:18.12f}{f}")
    L += ["", "K_POINTS automatic", f"  {kpts}", ""]
    open(path, "w").write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slab", default="db/structures/linio2_104_sym_1x4L4.vasp",
                    help="게이트를 통과한 1x4 슬랩 (여기서 1x1 을 잘라 쓴다)")
    ap.add_argument("--out", help="relax 입력을 쓸 디렉터리")
    ap.add_argument("--harvest", help="relax 가 끝난 디렉터리 — 이완좌표를 1x4 로 복제")
    ap.add_argument("--kpts", default="4 6 1 0 0 0", help="1x1 셀 기준 (18.27 x 2.88 A)")
    a = ap.parse_args()

    if a.harvest:
        rel = read(os.path.join(a.harvest, "relax.out"), format="espresso-out", index=-1)
        big = rel.repeat((1, 4, 1)); big.set_pbc(True)
        write("db/structures/linio2_104_sym_1x4L4_relaxed.vasp", big, format="vasp", direct=False)
        write("db/structures/linio2_104_sym_1x4L4_relaxed.xyz", big)
        d = np.abs(rel.positions - read(os.path.join(a.harvest, "start.vasp")).positions)
        print(f"✓ 이완 완료 — 최대 원자 변위 {d.max():.3f} A")
        print("  → db/structures/linio2_104_sym_1x4L4_relaxed.{vasp,xyz} (192원자)")
        print("  ⚠ 다음: 이 1x4 로 단일점을 돌려 **최대 잔여력 < 0.05 eV/A** 인지 확인할 것.")
        print("     크면 1x1 주기를 깨는 재구성이 있다는 뜻이고, 그때는 1x4 를 직접 이완해야 한다.")
        return

    if not a.out:
        sys.exit("--out 또는 --harvest 가 필요하다")
    os.makedirs(a.out, exist_ok=True)
    big = read(a.slab)
    # 1x4 → 1x1 로 되돌린다 (b 축 1/4)
    cell = big.cell.array.copy(); cell[1] /= 4.0
    keep = [i for i, f in enumerate(big.get_scaled_positions()) if f[1] < 0.25 - 1e-6]
    small = big[keep]; small.set_cell(cell, scale_atoms=False); small.set_pbc(True)
    if len(small) * 4 != len(big):
        sys.exit(f"⛔ 1x1 추출 실패: {len(small)} x 4 != {len(big)}")

    bands = zbands(small)
    if len(bands) != 4:
        sys.exit(f"⛔ (104) 면이 4장이 아니다 ({len(bands)}장)")
    # 아래 2장 고정, 위 2장 자유 (리뷰 권고)
    fixed = set(bands[0][1]) | set(bands[1][1])
    lab = afm_labels(small)
    write_relax(os.path.join(a.out, "relax.in"), small, lab, fixed, a.kpts, "lno_relax")
    write(os.path.join(a.out, "start.vasp"), small, format="vasp", direct=False)
    print(f"✓ {a.out}/relax.in  ({len(small)}원자, 고정 {len(fixed)} / 자유 {len(small)-len(fixed)})")
    print(f"   셀 {np.linalg.norm(cell[0]):.3f} x {np.linalg.norm(cell[1]):.3f} x "
          f"{np.linalg.norm(cell[2]):.3f} A · k {a.kpts}")
    print(f"   AFM Ni1 {lab.count('Ni1')} / Ni2 {lab.count('Ni2')} · U {U_NI} · vdw grimme-d3")
    print(f"   면 z: {[round(b[0],2) for b in bands]}  (아래 2장 고정)")


if __name__ == "__main__":
    main()

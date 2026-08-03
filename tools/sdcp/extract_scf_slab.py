#!/usr/bin/env python3
"""extract_scf_slab.py — pull the clean DFT-relaxed LiNiO2(104) slab out of a QE
input (scf_u62.in = linio2_104_optB) into an ASE-readable xyz, and record its
exact Ni1/Ni2 AFM sublattice so Phase-B can inherit it by index (no matching).

Why: reference/slab_relaxed.xyz (UMA-re-relaxed) reconstructed -- its upper Ni
layers collapsed and one Ni ejected. scf_u62.in still holds the clean 6x4-layer
DFT slab; use THAT as the substrate. Writes:
  <out>/slab_clean.xyz   species Ni (Ni1/Ni2 merged for ASE/UMA), DFT geometry
  <out>/slab_afm.json    {"nat":.., "Ni1":[idx..], "Ni2":[idx..]} for Phase-B
and prints a z-layer check (should be evenly-spaced bands of 4).

  python3 extract_scf_slab.py \
      --scf /data/work/runs/sdcp_linio2_binding/reference_dft_v2/scf_u62.in \
      --out /data/work/runs/sdcp_linio2_binding/slab_clean
"""
import argparse
import json
import os
import re
import numpy as np
from ase import Atoms
from ase.io import write


def parse_qe(scf):
    with open(scf) as f:
        L = f.readlines()
    cell = None
    for i, ln in enumerate(L):
        if ln.strip().upper().startswith('CELL_PARAMETERS'):
            cell = np.array([[float(x) for x in L[i + k].split()[:3]] for k in (1, 2, 3)])
            break
    for i, ln in enumerate(L):
        u = ln.strip().upper()
        if u.startswith('ATOMIC_POSITIONS'):
            crystal = 'CRYSTAL' in u
            sym, pos = [], []
            j = i + 1
            while j < len(L):
                s = L[j].split()
                if len(s) < 4 or not re.match(r'^[A-Za-z]', s[0]):
                    break
                p = np.array([float(s[1]), float(s[2]), float(s[3])])
                if crystal:
                    p = p @ cell
                sym.append(s[0]); pos.append(p)
                j += 1
            return sym, np.array(pos), cell
    raise SystemExit("no ATOMIC_POSITIONS")


def zbands(z, tol=0.8):
    order = np.argsort(z); b = 0; band = np.zeros(len(z), int)
    for k in range(1, len(order)):
        if z[order[k]] - z[order[k - 1]] > tol:
            b += 1
        band[order[k]] = b
    return band


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scf", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    sym, pos, cell = parse_qe(a.scf)
    # QE label -> element (Ni1/Ni2 -> Ni); keep AFM map by index
    elem = ['Ni' if s.startswith('Ni') else s for s in sym]
    ni1 = [i for i, s in enumerate(sym) if s == 'Ni1']
    ni2 = [i for i, s in enumerate(sym) if s == 'Ni2']
    atoms = Atoms(symbols=elem, positions=pos, cell=cell, pbc=True)

    write(os.path.join(a.out, "slab_clean.xyz"), atoms)
    with open(os.path.join(a.out, "slab_afm.json"), "w") as f:
        json.dump({"nat": len(sym), "Ni1": ni1, "Ni2": ni2, "source": a.scf}, f, indent=0)

    # ---- clean-layer verification ----
    ni_idx = [i for i, s in enumerate(elem) if s == 'Ni']
    z = pos[ni_idx, 2]
    ni1set, ni2set = set(ni1), set(ni2)
    band = zbands(z)
    nb = int(band.max()) + 1
    print(f"nat={len(sym)}  Ni={len(ni_idx)} (Ni1 {len(ni1)}/Ni2 {len(ni2)})")
    print(f"Ni z-layers: {nb} bands")
    clean = True
    for b in range(nb):
        members = [ni_idx[k] for k in range(len(ni_idx)) if band[k] == b]
        zc = z[band == b].mean(); n = len(members)
        n1 = sum(1 for g in members if g in ni1set)
        print(f"  band {b}: z={zc:6.2f}  n={n}  (Ni1 {n1}/Ni2 {n - n1})")
        if n != 4:
            clean = False
    # ⚠⚠⚠ **이 판정은 폐기됐다 (2026-08-03).** "밴드당 Ni 4개"는 깨진 슬랩의 밀도(1/3)에
    #   맞춰진 값이라 판정이 정확히 뒤집혀 있었다 — 실측:
    #     정상 (104) 1x2 슬랩 (밴드당 Ni 6) -> "NOT cleanly layered" 로 **탈락**
    #     깨진 원본     (밴드당 Ni 4)      -> "CLEAN layered slab" 로 **통과**
    #   z-밴드 개수는 대리 지표다. 물리 불변량은 결합길이·배위수·종단이고, 그건
    #   tools/sdcp/build_linio2_slab.py 의 gate() 가 본다. 여기서는 판정하지 않는다.
    print("verdict: (판정 없음 — 이 검사는 폐기. build_linio2_slab.py 의 gate() 를 쓸 것)")
    print(f"  z-밴드 {nb}개 · 밴드당 Ni {'4개씩' if clean else '4개가 아님'} "
          "— 이 숫자만으로는 아무것도 판정하지 못한다")
    print(f"wrote {a.out}/slab_clean.xyz + slab_afm.json")


if __name__ == "__main__":
    main()

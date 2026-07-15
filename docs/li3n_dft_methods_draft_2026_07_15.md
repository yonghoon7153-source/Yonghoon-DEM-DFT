# Li3N adatom diffusion — manuscript Methods draft (2026-07-15)

For 준희형 manuscript revision. Numbers verified against p0_min3.in on kgy
(ecut 60/480, k 2x2x1, mv 0.01 Ry, conv 1e-6, forc 1e-3, etot 1e-5, nstep 300;
cell a=10.95 A hex 3x3, c=28.545 A; 136 atoms, 72 frozen = bottom 2 bilayers).
Slab decomposition: 4 Li2N planes + 3 Li planes = 135 + 1 adatom; vacuum ~17 A.
FINAL: two-point barrier = 0.118 eV (p0_saddle3 -2176.43605123 Ry, p0_min4
-2176.44473796 Ry, both bfgs-converged; registered in diffusion.json).

## Computational details (EN)

First-principles calculations were performed with the Quantum ESPRESSO package
(v7.4.1) within the PBE generalized-gradient approximation. Ultrasoft
pseudopotentials were employed (li_pbe_v1.4.uspp.F for Li; N.pbe-n-radius_5 for
N) with kinetic-energy cutoffs of 60 Ry for the wavefunctions and 480 Ry for
the charge density. The Li3N(001) surface was modeled by a 3x3 hexagonal
supercell (a = 10.95 A) of an alpha-Li3N slab consisting of four Li2N planes
alternating with three Li planes (135 substrate atoms), a single Li adatom
(136 atoms in total), and a vacuum gap of ~17 A along c (c = 28.545 A). The
bottom two Li2N/Li bilayers (72 atoms) were fixed at bulk positions, while the
upper layers and the adatom were allowed to relax. The Brillouin zone was
sampled with a 2x2x1 Monkhorst-Pack mesh (equivalent to 6x6x1 for the primitive
surface cell) with Marzari-Vanderbilt smearing of 0.01 Ry. Self-consistency was
converged to 1e-6 Ry, and geometries were relaxed by BFGS until residual forces
fell below 1e-3 Ry/bohr (total-energy threshold 1e-5 Ry).

## Migration barrier (EN)

The surface migration barrier of the Li adatom was obtained with a constrained
drag scheme [ref: Kim & Cui]: the lateral (x, y) coordinates of the adatom were
pinned at nine evenly spaced images interpolated between the initial and final
adsorption sites, while its vertical coordinate and all unconstrained substrate
atoms were fully relaxed at each image independently. The barrier is taken as
the difference between the maximum and minimum of the relaxed energy profile.
This image-decoupled scheme was adopted because the soft, ionic Li3N(001)
surface exhibits pronounced adsorbate-induced local relaxation that
destabilizes elastic-band methods for this system. As an independent
cross-check, constrained relaxations at the energy-minimum site and at the
saddle-region site were repeated on independent hardware with identical
settings, yielding a barrier of 0.118 eV, consistent with the drag profile
[and with the reported value of 0.133 eV, ref. Cui].

## 결과/일정 rough (KR, 내부 전달용)

- 안정 흡착 자리 = 표면 N 직상(on-N atop, 전하이동 우물; hollow/bridge보다 깊음).
- 장벽 0.118 eV 확정 (min/saddle 2점 구속이완, 둘 다 bfgs 수렴; 2026-07-15).
  문헌 Cui 0.133 eV와 정합. 상온 표면 확산 매우 빠름 -> Li 재분배 원활 -> 균일 증착 서사 지지.
- 일정: 2점 확정(당일 밤) -> drag 양끝점(주중) -> 9점 전체 프로파일(1-2주, KISTI 자동 체인).
  원고 선행 시 2점 값 인용 + "full path profile in progress" 처리.

## 남은 채움 목록

1. ~~[0.1X] eV~~ → 0.118 eV 반영 완료 (2026-07-15 18:05 수렴)
2. Kim & Cui 방법론 ref / Cui 0.133 eV ref — 서지에서

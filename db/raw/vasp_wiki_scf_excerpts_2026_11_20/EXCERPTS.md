# VASP wiki — SCF 수렴 관련 발췌 (사용자 캡처 2026-11-20)

출처: 사용자가 vasp.at 위키 페이지를 캡처해 보냈다 (이 세션의 웹 읽기 도구가 vasp.at 에 닿지 못했다 · 환경 허용 뒤에도 ENOTFOUND).
아래는 캡처에서 읽은 문장이다 — 원문 그대로 옮기되 캡처 해상도 때문에 못 읽은 곳은 […] 로 둔다. 은 e70 far 재시도 (개정 5) 근거용.
⚠ 위키는 최신 VASP (6.x) 기준이다 — 업체 빌드는 VASP 5.4.4 라 6.x 전용 태그 (예: ISEARCH) 는 쓸 수 없을 수 있다 (판 확인 필요).

## ALGO (https://vasp.at/wiki/ALGO · 2026-06-23 수정판 캡처)
- Normal (default) · blocked Davidson · IALGO 38 · self-consistency cycle — "Robust default, recommended for most calculations."
- Conjugate / All · blocked Davidson + all-band conjugate gradient · 58 · direct optimization — "Simultaneous update of all orbitals. The two values are synonymous. Recommended together with the improved line-search algorithm (ISEARCH = 1). Appropriate choice for magnetic systems and systems where ALGO = Normal failed."
- Damped · blocked Davidson + damped molecular dynamics · 53 · direct optimization — "Damped velocity-friction dynamics for the orbitals. Robustness and time-to-solution strongly depend on setting TIME appropriately."
- Recommendations (캡처에서 읽은 요지): "Elongated geometries, systems including vacuum, slabs, surfaces: prefer the mixing (self-consistency-cycle) algorithms (Normal or Fast). These systems are prone to charge sloshing, which can be reduced by fine tuning the mixing tags (AMIX, BMIX, …), see Troubleshooting electronic convergence. For fast convergence of the self-consistency cycle, LMAXMIX must be set appropriately […]"
- OSZICAR 열: "dE: change of the total energy with respect to the previous step. d eps: change of the band-structure energy (sum of one-electron eigenvalues) due to the orbital optimization in this step."
- Tip (요지): 전 에너지를 스텝에 대해 그리면 지수적으로 줄어야 한다 · rms(c) 가 크면 전자밀도가 아직 바뀌거나 출렁인다 (charge sloshing).

## Electrostatic corrections (https://vasp.at/wiki/Electrostatic_corrections · 2026-08-11 수정판)
- Surfaces: "To correct the potential for the spurious interactions between the dipoles, additionally set LDIPOL=.TRUE. This can, however, slow convergence. Optionally, DIPOL may be set to define the center of the slab."
- "The following options may be used to improve convergence for this case. 1. Pre-converging the orbitals without the LDIPOL tag 2. The center of charge should be set in the INCAR file (DIPOL= center of mass) whenever many calculations with, say, different surface terminations are compared, or if the default algorithm fails to determine the centre of the slab/molecules. 3. Ensure that the cell is sufficiently large to determine the dipole moment with sufficient accuracy (see DIPOL). If the cell is too small, the charge might slosh into the vacuum, causing very slow convergence. Often, convergence improves with the vacuum width."

## LDIPOL (https://vasp.at/wiki/LDIPOL · 2026-08-11 수정판)
- "The disadvantage is that the convergence to the electronic ground state might slow down considerably, i.e., more electronic iterations might be required to obtain the required precision."
- Important: "Dipole corrections can lead to slow convergence, since charge often needs to be moved from one side of a slab to the other. The convergence rate often improves by setting AMIN to a smaller value, for instance AMIN = 0.01, since this dampens charge sloshing (charge moving back and forth from one to the other side of the slab in consecutive steps). Sometimes, it might also be necessary to increase the number of electronic steps using NELM and to tighten the energy convergence EDIFF = 1E-6. An unconverged dipole correction can lead to erroneous forces."

## TIME (https://vasp.at/wiki/TIME)
- "Default: TIME = 0.4 · TIME controls the time step for IALGO=5X and for the initial (steepest descent) phase of IALGO=4X."

## AMIN (https://vasp.at/wiki/AMIN)
- "Default: AMIN = min(0.1, AMIX, AMIX_MAG) · AMIN specifies the minimal mixing parameter in Kerker's initial approximation to the charge-dielectric function used in the Broyden/Pulay mixing scheme (IMIX=4, INIMIX=1)." · Kerker: max(A G²/(G²+B²), A_min) · A = AMIX · B = BMIX · A_min = AMIN.

## MAXMIX (https://vasp.at/wiki/MAXMIX)
- "Default: MAXMIX = -45 · MAXMIX specifies the maximum number of steps stored in the Broyden mixer (IMIX=4)."
- "MAXMIX<0: The mixer is reset after each ionic step or if the number of electronic steps exceeds |MAXMIX| (this is the default …)."
- "MAXMIX>0: The charge density mixer is only reset if the storage capabilities are exceeded. The reset is done "smoothly" by removing the five oldest vectors from the iteration history. … Especially for relaxations that start from a good ionic starting guess and for systems with a strong charge sloshing behavior the speedup can be significant. … The optimal setting for MAXMIX is usually around three times the number of electronic steps required in the first iteration. Too large values for MAXMIX might cause the code to crash (because linear dependencies between input vectors might develop). Too small values for MAXMIX can slow your convergence significantly. For instance, if you need 50 self-consistency cycles, and set MAXMIX to 20, you force the mixer to remove iteration history continuously, which can cause divergence and at least a slow down of the convergence."
- "In general, whenever the column RMS(c) in the OSZICAR files shows a sudden increase in the norm of the charge density residual vector, try to remove the tag MAXMIX from the INCAR file." · "Mind: MAXMIX is only available in VASP.4.4 and newer versions …"
- ⚠ 우리 읽기: 기본 MAXMIX = −45 이면 전자 스텝이 45 를 넘을 때 믹서가 리셋된다 — 우리 실패 잡은 200–300 스텝이었다 (리셋이 반복됐을 수 있다 · 확인 필요).
  → ⛔ 정정 (같은 날 · a4 OUTCAR 실측): 리셋이 아니었다 — a4 ⓐ · ⓑ 둘 다 Broyden 이력이 44 에서 막혀 5 스텝마다 오래된 벡터를 버리는 미끄러지는 창이었다 (고유값 개수 44 → 40 → … → 44 → 40). 결론 (이력을 계속 버렸다 = 위키의 '너무 작은 MAXMIX') 은 같다 · 개정 5 새_진단.

## IMIX (https://vasp.at/wiki/IMIX)
- "IMIX=1: Kerker mixing … If BMIX is very small, e.g., BMIX=0.0001, a straight mixing is obtained." · "Mind: BMIX=0 might cause floating-point exceptions on some platforms."
- "IMIX=4: Broyden's 2nd method and Pulay-mixing method (default) … AMIN=0.4 usually yields good convergence. AMIX strongly depends on the system, for instance, it should be small, e.g., AMIX= 0.02, for metals."
- IMIX=2 (Tchebycheff): "To determine the optimal parameters for μ and AMIX, first converge to the ground state with the Pulay mixer (IMIX=4). Then, search for the eigenvalues of the charge-dielectric matrix in the OUTCAR file at the last occurrence of 'eigenvalues of (default mixing * dielectric matrix)'."

## EDIFF (https://vasp.at/wiki/EDIFF · 2025-10-24 수정판)
- "The relaxation of the electronic degrees of freedom stops if the total (free) energy change and the band-structure-energy change ('change of eigenvalues') between two steps are both smaller than EDIFF (in eV)."
- "… for large systems with many atoms and/or when using METAGGA functionals, attaining an energy convergence of 1E-8 or even 1E-7 might be difficult. So, overall EDIFF= 1E-6 is likely the best compromise."

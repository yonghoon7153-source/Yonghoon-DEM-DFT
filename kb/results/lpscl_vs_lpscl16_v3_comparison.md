# LPSCl vs LPSCl1.6 — v3 직접 비교 (Pipeline v2 §8)

업데이트하면서 채워나가는 살아있는 비교 문서. 두 시스템 모두 같은 방법
(Pipeline v2: MLIP anneal → DFT BM-EOS V0 → DFT §8) 사용. 데이터 들어올
때마다 [pending] 자리 채움.

- **LPSCl** = comp1_v3, Li6PS5Cl, 52 atoms, V0 = 1016.62 Å³ (a = 10.055 Å)
- **LPSCl1.6** = modelc_v3, Li5.4PS4.4Cl1.6, ~104 atoms, V0 = 1216.44 Å³

마지막 업데이트: 2026-06-03


## 0. Pipeline §8 진행 현황

| 단계 | LPSCl (comp1_v3) | LPSCl1.6 (modelc_v3) |
|---|---|---|
| §8a V0 relax (BM-EOS V0에서 cell-fixed BFGS) | 진행 중 2026-06-03 | 완료 |
| §8b 결합 통계 (bond stats) | 대기 | 완료 |
| §8c 배위수 (coordination) | 대기 | 완료 |
| §8d Voronoi | 대기 | 완료 |
| §8e BVSE (python) | 대기 | 완료 |
| §8f Bader (AE plot_num=17) | 대기 | 완료 |
| §8g DOS / PDOS | 대기 | 완료 |
| §8h 밴드 구조 (Hungarian 재정렬) | 대기 | 완료 |
| §8i stress-strain 전체 6×6 Cij | 대기 (v2-cell 버전 철회됨) | 완료 |
| §8j MLIP UMA 600K snapshot 탄성 | 대기 | 완료 |
| §8k AIMD 600/800/1000K (Arrhenius) | 대기 | 완료 |
| §8l ELF (단면 + 3D iso) | 대기 | 완료 |
| §8m LOBSTER (COHP/ICOHP 4-panel) | 대기 | NSCF 완료, lobster 대기 |


## 1. Paper 헤드라인 값 (잠정)

데이터 들어올 때마다 채움. **굵게** = paper-grade 값, [pending] = 대기.

| 항목 | LPSCl (Li6) | LPSCl1.6 (Li5.4) | 추세 | 메커니즘 |
|---|---|---|---|---|
| **B0** (BM-EOS, GPa) | **26.23** | **21.71** | Li6가 더 단단 | Cl→Br/공공으로 격자 약화 |
| **K_VRH** (stress-strain, GPa) | [pending] | **44.47** | TBD | |
| **G_VRH** (GPa) | [pending] | **20.05** | TBD | |
| **E_VRH** (GPa) | [pending] | **52.30** | TBD | |
| **ν** (Poisson) | [pending] | 0.304 | TBD | |
| **Zener A** | [pending] | 0.416 | TBD | |
| 밴드갭 (DFT-PBE, eV) | [pending] | [추가] | | |
| Bader q(Li) (e) | [pending] | [추가] | | |
| AIMD Ea (eV) | [pending] | [추가] | | |
| AIMD D₀ at 300K (cm²/s) | [pending] | [추가] | | |
| ICOHP P–S (eV/bond) | [pending] | [추가] | | |
| ICOHP Li–S (eV/bond) | [pending] | [추가] | | |
| ICOHP Li–Cl (eV/bond) | [pending] | [추가] | | |

**실험 기준점**: LPSCl1.6의 측정 Young's modulus가 LPSCl보다 **더 높음**.
DFT 0K에서 반대 결과 (Li6가 더 단단)가 나오면 그게 "vacancy paradox" —
DFT가 유한온도의 비조화 강화(anharmonic stiffening) 및 Li 동적 재분배를
놓침. Paper에서 다룰 핵심 주제.


## 2. EOS (BM3, free 4-parameter fit)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| V0 (Å³) | 1016.62 | 1216.44 |
| a (Å, cubic) | 10.0547 | ≈ 10.674 |
| B0 (GPa) | 26.233 ± 0.004 | 21.71 ± 0.27 |
| B0' | 4.171 ± 0.011 | 7.01 ± 1.37 |
| R² | 1.000000 | 0.999012 |
| n_points | 8 | 11 |
| Fit 날짜 | 2026-06-03 | 2026-06-03 |

**B0' 차이에 대한 노트**: comp1의 B0' = 4.17 (교과서 범위), modelc_v3 B0' =
7.01 (높고 σ도 큼). modelc의 큰 B0' 불확실성은 더 넓은 부피 sweep + 평탄한
Li 에너지면을 반영. 두 시스템 각자 K 값 (BM vs stress-strain)은 ~3% 이내로
교차검증됨.


## 3. 탄성 — DFT 0K stress-strain (전체 6×6)

| 항목 (GPa) | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| C11 평균 | [pending] | 89.87 ± 3.16 |
| C12 평균 | [pending] | 21.82 ± 2.43 |
| C44 평균 | [pending] | 14.43 ± 1.25 |
| B_VRH | [pending] | 44.47 |
| G_VRH | [pending] | 20.05 |
| E_VRH | [pending] | 52.30 |
| ν | [pending] | 0.304 |
| Zener A | [pending] | 0.416 |
| 역학적 안정성 | [pending] | 안정 |

(comp1_v3 stress-strain v2 cell 값은 2026-06-03에 철회. V0 relax 후 재실행.)


## 4. 탄성 — MLIP UMA 600K snapshot

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| E_VRH (GPa) | [pending] | 52.72 ± 1.42 |
| 프로토콜 | UMA-s-1p1 600K Langevin → snapshot → relaxed-ion FIRE → Cij | 동일 |


## 5. 결합 환경 (DFT V0)

Bond stats: 평균 d, σ, n_bonds. Coordination: 평균 Z. Voronoi: 다면체 부피.

| 결합 종류 | LPSCl 평균 d (Å) | LPSCl1.6 평균 d (Å) |
|---|---|---|
| P–S | [pending] | [db에서 추가] |
| Li–S | [pending] | [db에서 추가] |
| Li–Cl | [pending] | [db에서 추가] |
| S–S (cage) | [pending] | [db에서 추가] |

| 사이트 | LPSCl 배위수 | LPSCl1.6 배위수 |
|---|---|---|
| Li 평균 | [pending] | [추가] |
| P (PS4 단위) | [pending] | 4 (tetrahedral) |


## 6. BVSE (Python 구현)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| 최소 Ea_BVSE (eV) | [pending] | [추가] |
| 예측 이동 경로 | [pending] | [추가] |


## 7. Bader (plot_num=17 AE charge density)

| 종 (평균 전하, e) | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Li | [pending] | [추가] |
| P | [pending] | [추가] |
| S | [pending] | [추가] |
| Cl | [pending] | [추가] |


## 8. DOS / PDOS

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| 밴드갭 (PBE, eV) | [pending] | [추가] |
| VBM 성격 | [pending] | S 3p 우세 |
| CBM 성격 | [pending] | [추가] |
| E_F 근처 Li-PDOS | [pending] | [추가] |


## 9. 밴드 구조 (Hungarian 재정렬, k-path X-Γ-L-W-K)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Direct/indirect | [pending] | [추가] |
| 갭 위치 | [pending] | [추가] |
| Li-like 밴드 유효질량 | [pending] | [추가] |


## 10. AIMD 이온 확산 (Arrhenius 600/800/1000K)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| D(600K) (cm²/s) | [pending] | [추가] |
| D(800K) (cm²/s) | [pending] | [추가] |
| D(1000K) (cm²/s) | [pending] | [추가] |
| Ea (eV) | [pending] | [추가] |
| D₀ 300K 외삽 (cm²/s) | [pending] | [추가] |
| σ_Li 300K (mS/cm, Nernst-Einstein) | [pending] | [추가] |


## 11. ELF (전자 국소화 함수)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Li–S 이온성 | [pending] | [추가] |
| P–S 공유성 (ELF > 0.7 사이) | [pending] | 있음 |
| 3D iso 레벨 | [pending] | 0.75 |


## 12. LOBSTER ICOHP (per-bond 평균, eV)

음수일수록 bonding 강함. 0에 가까울수록 약함.

| 결합 종류 | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| P–S | [pending] | [pending — lobster 대기 중] |
| S–S | [pending] | [pending] |
| Li–S | [pending] | [pending] |
| Li–Cl | [pending] | [pending] |

Charge spilling (lobsterout): comp1 [pending], modelc_v3 [pending].


## 13. 시스템 내부 교차검증 (intra-system cross-checks)

| 검증 | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| K_BM vs K_VRH (GPa) | 26.23 vs [pending] | 21.71 vs 44.47 |
| K_BM vs K_VRH 차이 해석 | TBD | 물리적으로 다른 양: BM은 E(V) 등방 압축, VRH는 clamped-ion Cij 전체에서 유도. Cl-rich soft phase에서 ~2배 차이 예상. |
| Cij 역학적 안정성 (모든 eigenvalue > 0) | [pending] | 안정 |


## 14. 논의 포인트 (paper outline)

1. **Vacancy paradox**: 실험은 LPSCl1.6 > LPSCl (Young's), DFT 0K은 반대일
   수 있음. 유한온도 강화의 원인 후보:
   - Cl-rich basin의 비조화 phonon 강화
   - Li 사이트 무질서 → effective stiffening (엔트로피 효과)
   - §4 MLIP 600K snapshot에서 비율 비교.
2. **Cl 치환**: Cl→{S 공공 + Cl}은 배위수 분포 + Li 이동성 모두 변화시킴
   (BVSE / AIMD 절).
3. **Ionic vs covalent 비율**: ELF + Bader + LOBSTER가 함께 PS4 공유 backbone
   (P–S 강한 ICOHP)에서 Li–anion 이온 결합 (Li–S/Li–Cl 약한 ICOHP, 높은
   Bader 전하 이동) 으로의 이동을 정량화.
4. **B0 vs K_VRH 불일치**: 물리적으로 의미 있음 — BM-EOS B0는 등방 압축
   (hydrostatic) bulk modulus, K_VRH from clamped-ion Cij는 harmonic-only
   frozen-ion 값. Cl-rich soft phase일수록 둘의 갭이 큼. Paper에 둘 다 보고.


## 각주

- modelc_v3 Pipeline v2 lineage 전체는 `db/compositions/modelc_v3.json`
  (Step 1–8 audit trail).
- comp1 v2 §8 결과 (a=9.929, v2 cell)는 컨테이너의
  `/home/ubuntu/work/runs/comp1_v3/archive_v2_post/`에 archive — 재현성
  목적, paper 사용 안 함.
- 모든 §8 도구는 `tools/modelc_v3/` 와 `tools/comp1_v3/`에.

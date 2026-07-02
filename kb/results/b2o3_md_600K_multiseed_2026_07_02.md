# B₂O₃ MD 이온전도도 — 600K 다중시드 error bar (Ea = 0.21 ± 0.03 eV)

**날짜** 2026-07-02 · **계기** 단일-seed Ea가 0.223↔0.172로 51 meV 흔들리던 문제(leave-one-out으로 600K 점이 주범임을 규명) → 600K를 다중시드 재현
**데이터** `db/properties/b2o3_600K_reseed_errorbar.csv`, `b2o3_md_arrhenius.json`(multiseed_600K_errorbar) · **그림** `docs/figures/cascade/b2o3_600K_reseed_errorbar.png`

> **한 줄.** 600K를 3-seed(s2/s3/s4, 각 200 ps, 2–50 ps 창) 재현하니 **D₆₀₀ = 1.04 ± 0.25 ×10⁻⁵ cm²/s (24% 스프레드)**. 이 하나의 노이지한 점이 Arrhenius 기울기를 지배 → **Ea = 0.206 (+0.038/−0.030) ≈ 0.21 ± 0.03 eV**. 어제의 "0.223 vs 0.172" 는 실제 차이가 아니라 **순전히 600K seed 변동**이었음(leave-one-out 예측과 정확히 일치).

---

## 1. 방법
- 표준 파이프라인(UMA-s-1p1 omat, Langevin NVT, D = MSD/6t, 창 2–50 ps, 3점 Arrhenius 600/800/1000 K, Nernst–Einstein).
- **600K만** seed 3개(s2·s3·s4, 각 200 ps prod) 재현 → D₆₀₀ 분포 확보. 고온(800/1000 K)은 deck-검증된 단일-seed anchor(3.009 / 5.067 ×10⁻⁵) 유지.
- (아직 800/1000은 단일-seed → 2차 불확실성; 그러나 leave-one-out이 600K를 지배 노이즈로 지목했으므로 우선 600K를 정량.)

## 2. 결과
| seed | D₆₀₀ (×10⁻⁵) | Ea (eV) | σ₃₀₀ (mS/cm) |
|---|---|---|---|
| s2 | 0.798 | 0.243 | 11.3 |
| s4 | 1.021 | 0.209 | 27.1 |
| s3 | 1.304 | 0.175 | 64.8 |
| **평균** | **1.04 ± 0.25** | **0.206 (+0.038/−0.030)** | 29 (범위 11–65) |

- **D₆₀₀ 24% 스프레드** — 600K는 확산이 느려 200 ps에서도 통계오차가 큼(hop 수 적음). 이게 Ea·σ의 지배 노이즈.
- **σ₃₀₀이 seed에 따라 11–65 mS/cm로 6배** 요동 → **단일-seed 절대 σ는 보고 불가.** Ea±오차 + b2o3/modelc 비율만 인용.

## 3. 함의 (논문값)
- **Ea = 0.21 ± 0.03 eV** 를 논문값으로. precise한 0.223이 아님(그건 error bar 안의 한 점).
- 어제의 51 meV 흔들림 = 600K seed 변동으로 **완전 설명** → error bar의 필요성 정량 증명.
- b2o3 vs modelc **동일 Ea**(둘 다 ~0.21–0.22, 오차 내) 결론은 유지 — 이득은 여전히 prefactor(D₀)-driven.
- **정직한 한계**: 800/1000 K도 단일-seed(2차 불확실성). 완전한 오차엔 그것도 재현 필요하나, 600K가 지배 노이즈였음이 확인됨.

## 4. ε∞(유전율) 상태 — 두 경로 모두 KISTI서 막힘 (별개 이슈)
- **ph.x DFPT epsil**: KISTI qe-cpu 빌드에서 hang(384-rep setup 후 멈춤, trans=.false. 무시). GPU 빌드엔 ph.x 없음.
- **epsilon.x (nscf→ε(ω))**: nscf(GPU)는 완주했으나 epsilon.x가 **`USPP are not implemented`** 로 stop — **epsilon.x는 NC pseudo만 지원**하는데 b2o3는 USPP+PAW.
- → ε∞ 경로 옵션: (a) **NC(ONCV) pseudo로 SCF/nscf 재계산 후 epsilon.x**, (b) **ph.x epsil을 kgy 서버 QE-CPU 빌드에서**(USPP 지원, 빌드 다르니 hang 안 할 수도), (c) **lelfield 유한장**(pw.x, USPP 가능). ε∞은 secondary라 보류 가능.

## 참고
- `db/properties/b2o3_600K_reseed_errorbar.csv`, `b2o3_md_arrhenius.json`(FINAL_for_paper.Ea_eV_PAPER + multiseed_600K_errorbar)
- 그림 `docs/figures/cascade/b2o3_600K_reseed_errorbar.png`
- MD 원본: gabia `runs/b2o3_600_reseed/s{2,3,4}/ensemble_results.json` (D_per_T[0]) / `.../T600/msd.json` (D_Li_cm2_s)
- 관련: `kb/methodology/md_conductivity_protocol.md`, `b2o3_vs_modelc_md.json`

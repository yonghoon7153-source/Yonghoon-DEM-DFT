# MD 이온전도도 추출 프로토콜 (논문용 — 고정 설정)

**날짜** 2026-06-30 · **목적** σ(T)·Ea·D0를 **계 간 일관·deck 검증**되게 뽑는 단일 파이프라인을 못박는다. fitting이라 설정에 값이 ±10–20% 흔들리므로 **아래 설정을 전 계에 동일 적용**한다.

> **한 줄.** `msd_origin` **window (2,50) ps · 3-pt Arrhenius(600/800/1000 K) · Nernst-Einstein(Haven=1)`. 이 설정으로 **modelc가 발표 슬라이드를 소수점까지 재현**(Ea 0.2235, σ300 13.94 = 슬라이드 14) → 검증된 기준.

---

## 1. MD (생성)
| 항목 | 값 |
|---|---|
| MLIP | **UMA-s-1p1**, `task_name="omat"` (FAIRChemCalculator) |
| 적분기 | **Langevin NVT** (ASE) |
| timestep | **2 fs** |
| friction | 0.01–0.02 /fs (스크립트 기본) |
| equilib | **5 ps** (버림) |
| production | **≥ 50 ps** (window 상한 50 ps를 덮어야 함) |
| 온도 | **600 / 800 / 1000 K** (well-converged 확산영역) |
| 저장 간격 | save_fs (MSD 해상도 충분하게) |
| 도구 | `tools/modelc_v3/disorder_ensemble_diffusion.py` |

- **production 길이 주의**: modelc/comp1는 100 ps, b2o3는 ~50 ps로 돌렸음. (2,50) window는 50 ps까지만 쓰므로 **현재 비교는 일관**. 다만 **최고 엄밀성**을 원하면 b2o3도 100 ps로 재실행해 동일 길이로 맞추는 게 베스트(아래 §5).

## 2. D 추출 (MSD → D)
| 항목 | 값 |
|---|---|
| 관계식 | **MSD(Li) = 6 D t** (3D), cell-correct unwrap (fractional) |
| **fit window** | **(2, 50) ps** ← `msd_origin.py` 기본. **전 계 동일 고정** |
| 도구 | `tools/ionic/msd_origin.py` (`--fit_window 2 50`) |

- ⚠️ **window가 결과를 가른다**: modelc 800 K가 (5,40)에선 1.71e-5, (2,50)에선 2.05e-5. **(5,40)은 쓰지 말 것**(modelc Ea를 0.226으로 부풀려 b2o3 Ea 우위를 가짜로 만들었음). **(2,50)이 deck 검증값.**

## 3. Arrhenius
- **3-pt 선형회귀** `ln D = ln D0 − (Ea/kB)(1/T)` on 600/800/1000 K.
- 저온(400/500 K)은 **별도 보조**(곡률 점검). 잡음 크고 deck도 3-pt이므로 **논문 메인은 3-pt**. 5-pt로 갈 거면 저온 MSD도 **(2,50)로 재추출**해 섞어야 함(현재 저온 D는 (5,40)).

## 4. σ (Nernst-Einstein)
- `σ = n q² D(T) / (kB T)`, **Haven ratio = 1**.
- `n_Li` = 해당 **이완 구조의 Li 수 / 셀부피**: modelc 2.2197e22 (27/1216.38 ų), b2o3 2.3806e22 (58/2436.33 ų).
- **절대 σ는 UMA가 3–5× 과대**(LPSCl family) → **Ea·상대비로 인용**, 절대값은 상한.

---

## 5. 검증 + 최종값 (이 설정으로)
| 계 | D600/800/1000 (e-6, e-5, e-5) | Ea (eV) | D0 (e-4) | **σ300** | **σ273** | 검증 |
|---|---|---|---|---|---|---|
| **modelc (LPSCl1.6)** | 7.90 / 2.05 / 4.55 | **0.2235** | 5.75 | **13.94** | 6.52 | **= 슬라이드 14 ✅** |
| **b2o3-doped** | 9.17 / 3.01 / 5.07 | **0.2234** | 7.11 | **18.51** | 8.65 | — |
| comp1 (LPSCl)* | 3.09 / 1.03 / 2.20 | 0.2532 | 4.11 | 3.35 | — | deck 검증값 인용 |

\*comp1은 `msd_comp1_modelc.csv`의 comp1 컬럼이 deck과 **다른 trajectory**라 재현 안 됨 → **deck 검증값을 그대로** 사용.

**결론(정직)**: **b2o3와 modelc는 Ea가 동일(0.223 eV, ΔEa 0 meV).** b2o3의 σ ~1.33× 우위는 **전적으로 D0(1.24×)** = 캐리어/시도빈도에서 옴(장벽 감소 아님). LPSCl→LPSCl1.6의 D0 메커니즘(Cl-vacancy)과 같은 결, B2O3가 D0를 추가로 올림.

**최고 엄밀성 옵션(논문 최종 전 권장)**: ① b2o3 high-T를 **100 ps**로 재실행(길이 parity) ② 저온 400/500도 **(2,50)** 재추출해 5-pt 일관 ③ 가능하면 **multi-seed 평균**으로 ±오차 막대(현 단일 trajectory는 ~15% 잡음).

## 참고
- 데이터: `db/properties/md_conductivity_FINAL_2026_06_30.csv`, `b2o3_vs_modelc_md.json`, `b2o3_md_arrhenius.json`
- 그림: `docs/figures/cascade/md_conductivity_FINAL.png` (평행선 = 같은 Ea, b2o3 위로 = 높은 D0)
- 검증 기준: `kb/results/ionic_conductivity_synthesis_comp1_modelc.md` (deck 슬라이드 값)
- 도구: `tools/ionic/msd_origin.py`, `tools/modelc_v3/disorder_ensemble_diffusion.py`

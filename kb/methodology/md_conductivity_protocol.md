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

### 1.1 실행 결정 (2026-06-30) — 고온 유지·저온만 신규
- **고온 600/800/1000 유지**: modelc = **deck 검증값**(100 ps, (2,50) → 슬라이드 정확재현), b2o3 = **커밋된 FINAL**(49 ps, (2,50) → Ea 0.223). **재실행 안 함**.
- **저온 400/500만 통일 설정으로 신규**: 양쪽 다 `--prod_ps 100 --save_fs 100 --fit_window_ps 2 50`. modelc는 deck 100 ps와 합쳐 **완전 일관 5pt**. b2o3는 고온 49 ps vs 저온 100 ps **약한 prod 불일치** → **3pt(메인)엔 무영향, 저온/5pt는 곡률 점검용 보조**. publication-grade 5pt 필요 시 b2o3 고온만 100 ps 재실행.
- (이전 (5,40)/단일-GPU 동시 저온 run은 취소; (2,50) 불일치라 폐기.)

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

---

## 6. D₀ 인자별 분해 (jump 통계) — **재실행 후 본격 진행**

> **왜.** b2o3의 σ 우위(1.33×)는 **Ea 동일·D₀ 주도(1.24×)**. D₀가 어느 인자에서 오는지(자리 z↑ vs 캐리어 c_v↑ vs 엔트로피 ΔS↑ vs 시도빈도 ν₀)를 **trajectory jump 통계로 정량 귀속**한다.

**분해식** (홉핑 random-walk):
$$D = \tfrac{1}{6}a^2\Gamma,\quad \Gamma=z\,\nu_0\,c_v\,f\,e^{\Delta S/k}e^{-E_a/kT}\ \Rightarrow\ D_0=\tfrac{1}{6}a^2 z\,\nu_0 c_v f\,e^{\Delta S/k}$$

| 인자 | 측정법 (trajectory) | 도구 |
|---|---|---|
| 홉 거리 a | inter-cage hop 거리 히스토그램 평균 | aimd_jump_stats |
| 홉률 Γ(T) | flicker-robust inter-cage hop 수 / 시간 | aimd_jump_stats |
| 캐리어 분율 c_v | (≥1회 홉한 Li)/(전체 Li) | aimd_jump_stats |
| 체류시간 τ | 전체시간 / mobile-Li당 홉 수 = 1/Γ_per-Li | aimd_jump_stats |
| **유효 시도빈도 ν₀,eff** | **Γ(T)=ν₀,eff·exp(−Ea/kT) Arrhenius 절편** | aimd_jump_stats(다온도) |
| 상관계수 f | f = D_MSD / [⅙ a²Γ] | (D_MSD ÷ jump-D) |
| 자리/연결성 z | inter-cage 48h-48h "window" 거리(율속), Li-per-cage | cage_jump_descriptors |

### 6.1 정적 기하 (지금 가능, trajectory 불필요)
```bash
python3 tools/ionic/cage_jump_descriptors.py \
  b2o3=db/structures/b2o3_relaxV0.xyz \
  modelc=db/structures/modelc_V0_k663.xyz \
  --out db/properties/cage_jump_b2o3_vs_modelc.csv
```
→ **율속 inter-cage window 거리**(짧을수록 z↑·연결성↑), **Li-per-cage(c_v 분포)**, **cage Cl-fraction/S-cage Li(무질서)**. b2o3가 window↓·Li분산↑이면 "자리↑·캐리어↑" 가설 정적 확증(BVSE 2× 채널과 정합).

### 6.2 동역학 (재실행 MD **trajectory 저장 필요**)
⚠️ **현재 `disorder_ensemble_diffusion.py`는 msd.json만 저장(위치 없음).** jump 통계엔 **프레임 좌표(extended-xyz)** 필요 →
- 옵션 A: 재실행 시 각 T의 frames를 `traj.xyz`로 덤프하도록 `run_md`에 1줄 추가(`write(cdir/f"T{int(T)}"/"traj.xyz", frames)`), 또는
- 옵션 B: 대표 온도(예 600 K)만 `tools/ionic/aimd_mlip.py`로 별도 trajectory MD.
```bash
python3 tools/ionic/aimd_jump_stats.py \
  --traj /data/work/b2o3md/b2o3_unified/d0.00_cfg0/T600/traj.xyz \
  --label b2o3_600 --out_dir /data/work/jump/b2o3_600 \
  --hop_smooth_ps 2.0 --hop_min_dist 2.5 --jump_lag_ps 2.0
# modelc도 동일 (검증 deck trajectory 또는 동설정 재실행)
```
→ Γ·c_v·a·τ → **D₀ = ⅙ a² z ν₀ c_v f e^{ΔS/k} 인자별 b2o3/modelc 비**. soft 포논(ν₀↓)에도 D₀↑면 **z·c_v·ΔS가 ν₀ 감소를 압도**함을 정량 확인.

### 6.3 가설 (검증 대상)
b2o3 D₀ 1.24× = **자리↑(BVSE 2× 채널·inter-cage window↓) + 무질서/엔트로피↑(4d Cl 25%·free-S²⁻) + 캐리어 분포↑**, **ν₀에서 오는 것 아님**(soft 격자는 Ea를 도울 뿐). Meyer-Neldel 보상도 아님(Ea 동일). → jump 통계가 어느 항이 주효인지 못박음.

## 참고
- 데이터: `db/properties/md_conductivity_FINAL_2026_06_30.csv`, `b2o3_vs_modelc_md.json`, `b2o3_md_arrhenius.json`
- 그림: `docs/figures/cascade/md_conductivity_FINAL.png` (평행선 = 같은 Ea, b2o3 위로 = 높은 D0)
- 검증 기준: `kb/results/ionic_conductivity_synthesis_comp1_modelc.md` (deck 슬라이드 값)
- 도구: `tools/ionic/msd_origin.py`, `tools/modelc_v3/disorder_ensemble_diffusion.py`

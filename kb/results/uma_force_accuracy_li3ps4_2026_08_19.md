---
title: UMA-s-1p1(omat) 힘 정확도 — Li₃PS₄ DFT 라벨 벤치 (외부 데이터, DFT 0회)
date: 2026-08-19
updated: 2026-08-19
tags: [mlip, uma, forces, li3ps4, benchmark, petmad, neb, msd]
status: 측정완료
confidence: medium
verificationStatus: verified
verifiedAt: 2026-08-19
verifiedBy: kgy 실측 (tools/mlip/bench_against_dft.py, test 243 / train 1940) → db/properties/mlip_bench_li3ps4_uma.json
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: single-source
---

# UMA-s-1p1(omat) 힘 정확도 — Li₃PS₄ DFT 라벨 벤치

> **한 줄**: 우리 정본 MLIP 이 **학습한 적 없는** 황화물 데이터에서 **힘 MAE 30.0 meV/Å**,
> 같은 test set 에 대해 그 데이터로 **1940개 학습한 전용 모델(35.6)보다 정확하다.**
> ⇒ **"UMA sulfide PES softening"** 이라는 알리바이의 근거가 사라진다.
> ⚠ 다만 이 벤치는 **응력·장벽을 안 잰다** — NEB 0.528 vs MD 0.253 격차 자체는 못 닫는다.

## 0. 왜 쟀나

2026-08-19 하루 종일 같은 논쟁이 되풀이됐다 — 전부 **참값이 없어서** 생긴 것이다:
- cascade 부피축이 뒤집힌 게 UMA 편향인가 미수렴인가 (→ 미수렴이었다)
- NEB 0.528 eV 가 UMA 탓인가 단일 경로 탓인가 (→ 이 카드가 절반을 답한다)
- preflight 이 **"UMA sulfide PES softening"** 을 알리바이로 썼다 (→ 근거 없음)

PET-MAD 논문(EPFL COSMO, *Nat. Commun.* 2025, 16, 10653)이 **Li₃PS₄ DFT 라벨 데이터셋**을
공개했다 ⇒ **우리가 DFT 를 한 판도 안 돌리고** 황화물에서 오차를 잴 수 있다.

## 1. 설정

| 항목 | 값 |
|---|---|
| 모델 | **UMA-s-1p1, task `omat`** (우리 정본) |
| 데이터 | PET-MAD 배포 `Li3PS4/` — train **1940** / test **243** 구조, 16–64 원자, α/β/γ 3상 |
| 라벨 | energy + forces, **PBEsol** (QE 7.2+SIRIUS, SSSP v1.2-eff, 110/1320 Ry, non-magnetic) |
| 도구 | `tools/mlip/bench_against_dft.py` (2026-08-19 신설) |
| 실행 | kgy (RTX3090, uma env) · test 84 s / train 667 s |
| 산출 | `db/properties/mlip_bench_li3ps4_uma.json` |

**참조 보정**: 두 DFT 설정의 절대 총에너지는 **원소별 상수만큼** 어긋나므로
`E_MLIP − E_DFT ≈ Σ_el n_el·e_el` 를 **train 에서 적합해 test 에 적용**한다.
적합값 **Li +0.0931 · P +0.0310 · S +0.1242 eV/atom**, R² 0.620.

## 2. 결과

| 지표 | 값 |
|---|---|
| **힘 MAE** | **0.0300 eV/Å** (RMSE 0.0446, 최악 0.477) |
|  ├ Li | **0.0132** (RMSE 0.0187, n=8064) |
|  ├ P | 0.0368 (RMSE 0.0546, n=2688) |
|  └ S | 0.0409 (RMSE 0.0545, n=10752) |
| 에너지 (보정 후) MAE | 0.0135 eV/atom (RMSE 0.0185, 중앙 0.0086, 최악 0.0553) |
| **상대에너지 RRMSE** | **2.4 %** (RMSE 0.688 eV) |
| 실패 구조 | **0 / 243** |

### 2-1. 같은 test set 공표값과의 위치

| 모델 | 힘 MAE (meV/Å) | 학습 |
|---|---|---|
| PET-MAD 기저 | 63.9 | 범용 (MAD 9.6만) |
| PET-MAD LoRA (N=1940) | 39.2 | **이 데이터로 파인튜닝** |
| bespoke (N=1940) | 35.6 | **이 데이터로 from-scratch** |
| **UMA-s-1p1/omat (우리)** | **30.0** | **이 데이터 학습 안 함** |

⇒ **범용 모델이 전용 모델을 이겼다.** 그것도 **참조 범함수가 다른데도**(UMA=OMat24/PBE 계열 ↔ 라벨=PBEsol).

## 3. 이 결과가 닫는 것 / 못 닫는 것

**닫는다**
- ⛔ **"UMA 가 황화물에서 PES 를 무르게 본다"** — 적어도 Li₃PS₄ **힘**에서는 근거가 없다.
  preflight 이 이 문구를 알리바이로 쓰던 것을 **철회해야 한다.**
- **Li 힘이 특히 정확하다**(13.2 meV/Å, 전체의 44 %). Li 이동이 우리가 재는 전부이므로
  MD/NEB 입력으로서의 건전성이 이 축에서 확인된다.

**못 닫는다 (도구 자신이 docstring 에 적어 둔 한계)**
- **응력을 안 잰다** — 이 데이터셋에 stress 라벨이 없다.
  ⇒ **cascade 부피 편향(+32.7 %) 은 이 벤치로 무죄가 되지 않는다.** 별건이다.
- **장벽을 안 잰다** — 힘이 맞아도 NEB 장벽이 맞는다는 보장이 없다.
  오히려 그게 안 된다는 것이 문헌의 요지다 (Zhang npj 2026: MACE-MP-0 이 힘 0.16 eV/Å 인데도
  **CI-NEB 전이상태 상대에너지 RRMSE 22.8 %**).
  ⇒ **NEB 0.528 vs MD 0.253 (109 %) 격차의 남은 후보는 경로 선택**이다.
- **데이터셋의 DFT 설정을 검증하지 않는다.** 그쪽이 틀리면 이 값도 틀린다.

## 4. 반론 / 약한 곳 (지우지 말 것)

1. **참조보정 R² 0.620** — 원소별 선형 모형이 ΔE 분산의 **62 %만** 설명한다.
   즉 에너지 오차는 **참조 offset 만이 아니다**. 보정 후 13.5 meV/atom 이 정직한 수치다.
   ⚠ 단 **자기적합(낙관치)이 13.49 로 train-적합 13.45 와 사실상 같다** ⇒ 잔차는
   **적합 부족이 아니라 진짜 모델 오차**다. 이 점은 결과를 강화한다.
2. **최악 힘 0.477 eV/Å = 평균의 16배.** Kauwe 2021 §2.5 의 교훈("평균 RMSE 가 낮아도
   목표 물성이 틀릴 수 있다")이 그대로 적용된다. 꼬리를 평균으로 덮지 말 것.
3. **범함수 교차**(PBE 계열 모델 ↔ PBEsol 라벨). 힘은 offset 에 둔감하지만 무감하지 않다.
   ⇒ **UMA 가 실제 PBE 라벨에서는 더 좋을 수도, 더 나쁠 수도 있다** — 미측정.
4. **공표값의 분할을 우리가 직접 확인하지 않았다.** PET-MAD 63.9 / bespoke 35.6 이
   **이 test.xyz 243구조 위의 값인지**는 배포 parity 데이터로 재계산한 에이전트 보고에 의존한다.
   ⇒ **원고에 넣기 전에 반드시 직접 확인할 것.** (지금은 `figure-read`급 신뢰도)
5. **조성이 Li₃PS₄ 다** — 우리 계는 Li₆PS₅Cl(+Cl, +O, +B). **Cl 이 없다.**
   PET-MAD MAD-bench 1562 구조에도 Li+P+S 동시 구조가 0개였다(에이전트 실측).
   ⇒ **아르지로다이트·Cl 무질서로의 전이는 이 벤치가 보증하지 않는다.**

## 5. 다음 (이 카드가 여는 것)

- **[싸다]** UMA 보존성 점검 — 원자 하나 ±1e-3 Å 로 `(E(+δ)−E(−δ))/2δ` vs `−F`.
  PET-MAD `Fig. S5`(비보존 모델만 기하최적화 9–11 % 미수렴) · `Fig. S16/S17`(종별 온도 분리, MSD 과대)와 직결.
- **[싸다]** 기존 궤적에서 **비-Li 골격(P·S·Cl) MSD** 를 600/800/1000 K 에서 확인.
  Zhang npj 2026 이 MACE-MP-0 의 LGPS 골격이 1050–1500 K 에서 **인위적으로 녹는** 것을 잡고
  샘플링을 1050 K 로 낮췄다 — **우리 1000 K 앵커가 그 선 바로 아래**다.
- **[중간]** 같은 벤치를 **Cl 포함 계**에서 반복하려면 우리가 DFT 라벨을 만들어야 한다
  (PET-MAD 데이터에 Cl-thiophosphate 가 없다).

## 6. 출처

- 데이터: PET-MAD 배포 `datasets/Li3PS4.zip` → kgy `~/work/data/petmad_li3ps4/`
- digest: `litdb/papers/petmad2026_lightweight_universal_interatomic_potential_mad.md`
- 교차: `litdb/papers/zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill.md` (RRMSE 22.8 %)
- 도구: `tools/mlip/bench_against_dft.py` (`--selftest` 23건, 음성 경로 포함)
- 값: `db/properties/mlip_bench_li3ps4_uma.json`
- 미결: `kb/open_items.md` #R

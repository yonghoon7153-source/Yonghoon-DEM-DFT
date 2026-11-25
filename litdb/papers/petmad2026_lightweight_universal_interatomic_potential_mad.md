<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. 이 논문은 [외부·methods·범용 MLIP] — 재료비교가 아니라 **도구 판정용** -->
# PET-MAD as a lightweight universal interatomic potential for advanced materials modeling — Mazitov, Bigi et al. (Nature Communications 2025)

> slug `petmad2026_lightweight_universal_interatomic_potential_mad` · DOI `10.1038/s41467-025-65662-7` · type `MLIP (universal) + DFT reference + MD/PIMD` · PDF `34b02e87-63.…pdf` + `c90694f1-63._Sup_….pdf` · digested `2026-08-19` · status ✅ · 태그 **[외부·methods·도구판정]**
> **저자**: Arslan Mazitov¹²*, Filippo Bigi¹² (공동1저자), Matthias Kellner, Paolo Pegolo, Davide Tisi, Guillaume Fraux, Sergey Pozdnyakov, Philip Loche, **Michele Ceriotti***  (EPFL COSMO — Laboratory of Computational Science and Modeling) · Nat. Commun. **16**, 10653 (2025) · Received 2025-04-04 / Accepted 2025-10-17 · arXiv:2503.14118

> elements: Li, P, S, Cl, Ga, As, Co, Cr, Fe, Mn, Ni, H, C, N, O, Ba, Ti, Be, Te, Br
> methods: DFT, MLIP, MD, MSD, phonon

> ⚠ **slug 의 `2026` 은 우리 반입 번호(63번) 관례일 뿐, 실제 출판은 2025 년**이다. 인용할 땐 **Nat. Commun. 2025, 16, 10653**.

---

## 0. 이 digest 를 읽는 법

이 논문은 **재료 논문이 아니라 도구 논문**이다. 우리가 여기서 얻을 것은 Li₆PS₅Cl 의 물성값이 아니라
**"범용 MLIP 를 그냥 써도 되나 / 얼마나 손봐야 하나 / 얼마나 빠른가"** 에 대한 정량 근거다.
따라서 §9(Li₃PS₄)와 §15(우리 시야)가 본체이고, 나머지는 그 판정을 떠받치는 재료다.

우리에게 결정적인 두 가지:
1. **Li₃PS₄(황화물 SE)가 여섯 사례 중 하나**다 — 우리 계와 가장 가깝고, 원수치(σ vs T)가 통째로 공개돼 있다.
2. **UMA(fairchem/OMat24)는 이 논문의 비교군에 없다.** 우리가 쓰는 모델이 빠진 벤치마크라는 사실을 계속 기억해야 한다(§7).

> 🔎 이 digest 의 수치 중 **"[배포자료]" 표시는 논문 본문이 아니라 Materials Cloud 부속자료를 내가 직접 읽어 뽑은 값**이다.
> 논문 본문 수치와 어긋나는 곳이 여러 군데 있고, 그건 §17 에 따로 모았다. 섞어 쓰지 말 것.

## 1. 한 줄 요약

**9.6 만 구조·2.8 M 파라미터짜리 "가벼운" 범용 potential 이, 10⁶–10⁷ 구조로 학습한 대형 모델들과 대등한 정확도를 내고, 그중 Li₃PS₄ 이온전도도는 전용(bespoke) 모델 대비 σ 비 0.88–0.98 · Ea 차 0.03 eV 안에서 재현한다** — 즉 **황화물 SE 의 이온수송에서는 범용 모델을 그냥 써도 전용 모델과 구분이 안 될 만큼 가깝다**. 대신 그 대가는 (a) 자기 데이터셋(MAD)에서만 압도적이고, (b) 참조 DFT 가 **PBEsol** 로 고정돼 있으며, (c) 융점·상전이 같은 자유에너지 양에서는 수십 K 씩 어긋난다는 것.

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 문제 | 범용 MLIP 들이 **안정 구조에 편향**돼 있고(대개 MP 이완 궤적 학습), **참조 DFT 설정이 서로 달라** 모델 오차와 참조 오차를 분리할 수 없다 |
| 처방 | ① 화학·구조 다양성을 **인위적으로** 밀어올린 데이터셋(MAD) ② **전 원소 동일 DFT 설정**(내부 일관성) ③ 10 만 미만으로 크기를 묶어 학습을 대중화 |
| 모델 | **PET**(Point Edge Transformer) — 회전 등변성을 **강제하지 않고** data augmentation 으로 배우는 transformer GNN |
| 검증 축 | (i) 공개 벤치마크 7종 대비 정확도 (ii) 속도·메모리 (iii) **여섯 개 고난도 시뮬레이션**(각각 기존에 전용 MLIP 로 수행된 적 있는 문제) |
| 여섯 사례 | **Li₃PS₄(이온전도) ← 우리 계** · GaAs(융점) · CoCrFeMnNi HEA(표면편석) · 액체 물(핵양자효과) · succinic acid(NMR 화학적 차폐) · BaTiO₃(유전응답·상전이) |
| 비교 대상(정확도) | MACE-MP-0-L · MatterSim-5M · Orb-v2 · SevenNet-l3i5 — **UMA 없음** |
| 배포 | 코드 `github.com/lab-cosmo/pet-mad`(BSD-3) · 데이터 Materials Cloud `10.24435/materialscloud:fe-1p` · 모델 v1.0.2(논문 재현용)/v1.1.0(dev) |

## 3. 핵심 수치 총정리

| 항목 | 값 | 비고 |
|---|---|---|
| MAD 데이터셋 크기 | **95,595 구조 / 85 원소**(Z 1–86, At 제외) | 8개 하위집합 합이 정확히 95,595 (검산 ✓, §4) |
| 모델 파라미터 | **2.8 M** | MACE-MP-0-L 15.8 M · MatterSim-5M 4.6 M · Orb-v2 25 M · SevenNet-l3i5 **1.17 M** |
| 학습 데이터 비 | 95,595 vs 1.58 M / 17 M / 32.1 M / 1.58 M | **1–3 자릿수 적음** |
| cutoff | **4.5 Å** | GNN 2층 × transformer 2층, d_PET 256, head 8 |
| 학습 비용 | 8× **H100**, 1500 epoch, **약 40 시간** | batch 24/GPU, Adam LR 1e-4 |
| PET-MAD 정확도 (MAD test) | **15.1 meV/atom ∣ 72.3 meV/Å** | train 7.3∣43.2, val 14.7∣72.2 |
| Matbench(WBM) E_hull MAE | **41 meV/atom**(일관 참조) / **138**(비일관 참조) | 참조 DFT 자체 불일치가 **120 meV/atom** |
| 속도 (H100, Al 8k atoms) | **≈15 µs/atom·step** | MACE-MP-0-M ≈87 · SevenNet-0 ≈62 · MatterSim-1M ≈47 (figure-read ≈, `Fig. 3`) |
| 비보존력(NC) 가속 | **약 2×** (직접 힘 head) / MTS(8스텝) **1.8×** | ⚠ 에너지 보존 깨짐 — §11 |
| **Li₃PS₄ MAE** | PET-MAD **4.9∣63.9** · bespoke **1.2∣35.6** · fine-tuned **1.3∣36.0** | 본문 값(validation). [배포자료] test 값은 §9.4 |
| **Li₃PS₄ σ (β, 600 K)** | PET-MAD **1.007** · bespoke **1.151** · LoRA **1.047** S/cm | [배포자료] `fig4/*_beta_sigma_T.data` |
| **Li₃PS₄ Ea (β, 475–900 K)** | PET-MAD **0.323** · bespoke **0.356** · LoRA **0.363** · Gigli(ref 39) **0.317** eV | ⚠ **논문에 없는 값 — 내가 배포 원수치로 직접 회귀**(§9.3) |
| GaAs 융점 | bespoke **1169±4** · LoRA **1169±3** · PET-MAD **1111±72** K | 실험 1511 K (PBEsol 자체 한계) |
| BTO T–C 전이 오차 | **< 30 K** | ε_r 곡선은 약 25 K 이동 |
| LoRA 설정 | **rank 8, scaling 0.5** | 전 사례 공통 |

## 4. MAD 데이터셋 — "universal" 을 어떻게 정의했나 ★

### 4.1 구성 (Supplementary Table 1, `Table S1`)

| 하위집합 | 만든 법 | 구조 수 |
|---|---|---|
| MC3D | Materials Cloud 3D 벌크 결정 **그대로** 재계산 | 33,596 |
| MC3D-rattled | 각 원자 좌표에 **공유반경의 20 %** 표준편차 가우시안 노이즈 | 30,044 |
| MC3D-random | MC3D 구조의 **원소를 85종에서 무작위 재배정** + 공유반경 기반 부피 등방 조정 | 2,800 |
| MC3D-surface | 무작위 저지수면(최대 Miller 3) 절단 슬랩 | 5,589 |
| MC3D-cluster | 무작위 결정에서 **원자 2–8개짜리 구형 환경**을 오려냄 | 9,071 |
| MC2D | Materials Cloud 2D 결정 | 2,676 |
| SHIFTML-molcrys | CSD 유래 분자결정(이완 + 열교란) | 8,578 |
| SHIFTML-molfrags | 중성 분자 조각 | 3,241 |
| **합** |  | **95,595** ✓ |

핵심 철학 3줄:
1. **유기 + 무기 + 전 차원(0D/2D/3D/표면)** 을 한 데이터셋에 — "mindless benchmark"(Korth–Grimme) 아이디어를 고체·표면으로 이식.
2. **일부러 망가뜨린 구조**(rattled / 조성 무작위)를 넣는다 — 범용 모델이 실제로 쓰이는 곳은 안정 구조가 아니라 **MD 가 지나가는 뒤틀린 배열**이기 때문.
3. **10 만 구조 미만으로 묶는다** — 학습 접근성. (그리고 이게 `Fig. 1` 의 데이터효율 주장의 근거가 된다.)

필터링: 힘이 **100 eV/Å**(MC3D-rattled/random) 또는 **10 eV/Å**(그 외)를 넘는 이상치 제거. SCF 수렴률은 대부분 **>95 %**, 단 **MC3D-random 은 ~55 %** 만 수렴(조성 무작위라 당연).

### 4.2 참조 DFT (내부 일관성이 이 논문의 진짜 주장)

- **코드**: Quantum ESPRESSO **v7.2** + **SIRIUS v7.5.2** + **AiiDA v2.6.3** (워크플로/프로버넌스)
- **범함수**: **PBEsol**, **전 계산 non-magnetic**(스핀 상태 모호성 회피) — vdW 보정 **없음**
- **pseudo**: **SSSP v1.2 (efficiency)**
- **cutoff**: **ecutwfc 110 Ry / ecutrho 1320 Ry** — 85 원소 중 **가장 빡센 값을 전부에 일괄 적용**
  (⚠ SI §5 는 같은 값을 **1360 Ry** 로 적는다 — 본문/SI 불일치, §17)
- **smearing**: Marzari–Vanderbilt–DeVita–Payne cold smearing, spread **0.01 Ry**
- **k-mesh**: Γ-centered, **해상도 0.125 Å⁻¹**; 비주기 방향은 Γ 만 + **진공 25 Å** + Coulomb 절단(2D: Sohier–Calandra–Mauri, 0D: Martyna–Tuckerman)
- **에너지 기준선**: 고립원자 에너지 기반 조성 baseline 을 빼고 학습

**왜 구조마다 cutoff 를 맞추지 않고 전부 최대값으로 갔나** — `Fig. S3` 이 답이다. 원소별 권장 SSSP 설정과 MAD 설정으로 계산한 **고립원자 에너지 차이가 원소에 따라 10–100 meV/atom** 에 달한다. 구조마다 수렴도가 다르면 한 원자의 에너지 기여가 **cutoff 반경 안의 이웃이 아니라 셀 전체 조성에 의존**하게 되고, 그건 **물리적으로 말이 안 되고 학습 불가능**하다. → 비용을 감수하고 불일치를 아예 없앤다.

> 🔑 **우리에게 그대로 꽂히는 교훈**: 우리 db 도 comp1/modelc/b2o3/LPSOCl 을 **같은 ecut·k-mesh·pseudo** 로 돌아야 조성 간 차이가 물리다. 이 논문은 그 규율을 "왜"까지 정량화해 준다(원소당 10–100 meV/atom).

## 5. PET 아키텍처 & 학습 ★

- **구조**: 방향성 결합(i→j)마다 토큰 f^l_ij 를 두고, 각 원자 i 에서 **이웃에서 들어온 메시지 집합을 transformer 에 통째로 넣어** 나가는 메시지를 만든다(sequence-to-sequence, permutation-covariant). 각 f^l_ij 에 feed-forward 를 태워 결합·층 전체를 합산 → 에너지.
- **회전 등변성을 강제하지 않는다.** 대신 data augmentation 으로 배운다. 이론적 표현력은 높다(단일 층도 universal approximator, 사실상 무한 body-order).
- **하이퍼파라미터 탐색**(`Fig. S1`): R_cut [4.0, 4.5, 5.0, 5.5] × N_GNN [1–4] × N_trans [1–4] × d_PET [64, 128, 256] × N_heads [4, 8] 격자 탐색 → **Pareto 최적 = 4.5/2/2/256/8**. y축 = validation 에너지 MAE, x축 = **원자당 추론시간(GH200, batch 1)** — 즉 정확도만이 아니라 **MD 에서의 속도**를 명시적으로 최적화 축에 넣었다.
- **학습**: PyTorch + **metatrain**, 8× H100, batch 24/GPU, **1500 epoch, ~40 h**, Adam LR 1e-4, 250 epoch 마다 LR 반감, loss = 에너지·힘 RMSE(에너지 가중 **0.1**).
- **추가 head 2개**:
  - **직접(비보존) 힘/응력 head** — backprop 없이 힘을 바로 예측 → **2–3× 가속**. ⚠ 에너지 보존 위반(§11).
  - **LLPR 불확실도** — 마지막 층 특징의 공분산으로 사후 불확실도, 추가비용 거의 0. 여기서 **128 멤버 shallow ensemble** 을 뽑아 임의의 후처리에 전파(§12).

[배포자료] `inputs/PET-MAD/options-*.yaml` 은 이 서술과 **부분적으로 다르다**:
- `options-nc-pretrain.yaml` = **1단계: 비보존(nc) 힘·응력만으로 from-scratch 사전학습** (2000 epoch, **cosine** scheduler, batch 24, energy weight 0.1)
- `options-c-finetune.yaml` = **2단계: 보존(c) 힘·응력을 추가해 `finetune: method: "full"` 로 전체 미세조정** (1500 epoch, batch 16, energy weight 0.5)
- 즉 **배포된 yaml 은 "LoRA 로 계를 파인튜닝하는 설정"이 아니라 PET-MAD 자기 자신의 2단계 학습 레시피**다. 계별 LoRA 설정 파일은 배포에 **없다**(§17).

## 6. "lightweight" 의 근거 — 속도·메모리 실측 ★ (`Fig. 3`, `Fig. S5`)

**측정 조건**: 단일 **NVIDIA H100**. 각 모델은 LAMMPS 인터페이스(가능하면 **Kokkos**)를, 없으면 ASE 를 쓴다. 비교군은 **정확도 표보다 가벼운 변종**(MACE-MP-0 **M**, MatterSim **1M**, SevenNet-**0**, Orb-v2)을 써서 PET-MAD 에게 불리하게 잡았다 — 이 점은 논문이 명시한다(honest).

| 계 (≈8–9×10³ atoms) | PET-MAD | PET-MAD (NC) | Orb-v2 (NC) | MACE-MP-0-M | SevenNet-0 | MatterSim-1M |
|---|---|---|---|---|---|---|
| Water | ≈37 | ≈13 | ≈16 | ≈130 | **OOM** (~2.3k 에서, 직전 ≈90) | ≈110 |
| Diamond | ≈54 | ≈22 | ≈14 | ≈200 | **OOM** (~2k, 직전 ≈135) | ≈320 |
| Aluminium | ≈15 | ≈8 | ≈15 | ≈87 | **OOM** (~4k, 직전 ≈62) | ≈47 |

*(단위 µs/atom·step, **figure-read ≈** — fig3 원수치는 배포자료에 포함되지 않았다. 크롭본은 Al 패널이 잘려 배포 PNG `figures/png/timings.png` 를 대신 봤다.)*

읽는 법:
- **보존력 기준으로 PET-MAD 가 전부 이긴다** (Al 에서 MACE 대비 **5.8×**, MatterSim 대비 **3.1×**, SevenNet 대비 **4.1×**).
- **비보존 head 를 켜면 Orb-v2(비보존)와 동급**이 된다.
- **"메모리 효율" 주장의 증거는 OOM 십자표뿐**이다 — 메모리 사용량 곡선은 없다. PET-MAD·Orb·MatterSim 은 ~10⁴ 원자까지 갔고 MACE·SevenNet 은 2–4×10³ 에서 죽었다는 정성 사실이 전부(§19).
- ⭐ **작은 계에서는 전부 수렴한다**: x축 왼쪽 끝(30–60 원자)에서 모든 모델이 **200–400 µs/atom** 근처에 몰린다. 이건 계산이 아니라 **GPU 커널 런치 오버헤드**가 지배한다는 뜻 — §15 에서 우리 52 원자 셀 문제로 이어진다.

**기하최적화 벤치**(`Fig. S5`): BeO/BeTe/LiBr 각 1000회, 위치·격자에 σ=0.1 Å 무작위 변위 후 **ASE LBFGS, fmax 0.05 eV/Å, 최대 100 스텝**.
- PET-MAD 이완시간 중앙값 ≈75(BeO)/45(BeTe)/35(LiBr) ms/atom — **보존 모델 중 가장 빠르고 분포도 가장 좁다**(figure-read ≈).
- **미완료 실행 수**: PET-MAD·MACE·SevenNet·MatterSim ≈0, **Orb-v2 만 BeO ~112회(11 %)·LiBr ~94회(9 %)** 실패. 논문 표현: "비보존 Orb-v2 는 일관되게 빠르지만 **덜 안정**하고, 변위의 최대 10 %에서 수렴 실패한 유일한 모델".

## 7. MAD-bench / 공개 벤치마크 결과 ★ (`Table 1`, `Fig. 1`, `Fig. 2`)

### 7.1 데이터효율 프론티어 (`Fig. 1`)
x = 학습셋 크기(10⁵–2×10⁸), y = Matbench Discovery(WBM) E_hull MAE. PET-MAD 는 **9.6×10⁴ 구조에서 0.041 eV/atom** — MACE-MP-0-L·SevenNet-l3i5(1.58 M 구조, 0.04–0.045)와 **같은 높이**를 **16배 적은 데이터**로 찍는다. 회색 점 무리 위로 Pareto 선이 확실히 내려간다.
비교 지점: eSEN-30M-**OAM**(≈10⁸ 구조, 30 M 파라미터) 0.018 · MatterSim-5M 0.025 · Orb-v2 0.031 · M3GNet 0.075 · MEGNet 0.16 (figure-read ≈).

⚠ **PET-MAD 의 0.041 은 "자기 설정으로 다시 계산한 참조" 대비**이고, 나머지 모든 점은 **원래 WBM 참조** 대비다. 논문도 이걸 알고 있어 **Matbench Discovery 리더보드에 등재하지 않았다**(SI §4). 즉 **`Fig. 1` 의 세로 위치 비교는 엄밀히 같은 자 위의 비교가 아니다**(§19).

### 7.2 공개 데이터셋 7종 (`Table 1`, 단위 meV/atom ∣ meV/Å)

| Dataset | PET-MAD | MACE-MP-0-L | MatterSim-5M | Orb-v2 | SevenNet-l3i5 |
|---|---|---|---|---|---|
| **MAD** | **17.6 ∣ 65.1** | 81.6 ∣ 181.5 | 47.3 ∣ 133.7 | 52.9 ∣ 96.2 | 82.1 ∣ 173.5 |
| MPtrj | 22.3 ∣ 77.9 | 15.1 ∣ 50.8 | 21.3 ∣ 61.4 | **5.6 ∣ 21.9** | 9.8 ∣ 25.5 |
| Matbench | **31.3** ∣ — | 58.5 ∣ — | 38.2 ∣ — | 37.9 ∣ — | 47.5 ∣ — |
| Alexandria | 49.0 ∣ 66.8 | 65.4 ∣ 79.5 | 21.2 ∣ 39.9 | **13.2 ∣ 10.5** | 47.6 ∣ 70.3 |
| OC2020 (S2EF) | **18.3** ∣ 114.5 | 82.4 ∣ 169.6 | 31.5 ∣ 119.2 | 19.8 ∣ **99.3** | 45.7 ∣ 162.7 |
| SPICE | **3.7 ∣ 59.5** | 10.6 ∣ 166.8 | 21.3 ∣ 145.6 | 59.0 ∣ 140.8 | 11.3 ∣ 139.1 |
| MD22 | **1.9 ∣ 65.6** | 9.4 ∣ 182.9 | 28.6 ∣ 160.4 | 174.3 ∣ 220.7 | 11.1 ∣ 146.2 |

- **이기는 곳**: 자기 데이터셋(MAD), 분자(SPICE·MD22 압도), 촉매 표면(OC2020 — MAD 에 흡착분자 배열이 **없는데도**), 일관참조 Matbench.
- **지는 곳**: **MPtrj·Alexandria** — Orb-v2 가 이 둘을 학습에 썼으니 당연. SevenNet 도 MPtrj 에서 앞선다.
- 벤치 부분집합 크기(SI §3): MAD 360(하위집합당 50) · MPtrj 136 · Matbench 555 · Alexandria 200 · OC2020 78 · SPICE 99 · MD22 134. **전부 수백 개 규모의 표본**이라 소수점 자릿수 신뢰는 제한적이다.

### 7.3 MAD 하위집합별 (`Fig. 2` — 레이더 차트)
직접 봤을 때: 검정(PET-MAD) 다각형이 **MC3D-rattled·MC3D-random·MC3D-cluster·MC3D-surface·SHIFTML-molcrys/molfrags 에서 다른 모든 선보다 확실히 안쪽**(log 축으로 1–1.5 decade). 반대로 **MC3D·MC2D(안정 무기결정)에서는 격차가 사라지고 Orb-v2 가 근소하게 안쪽**. 본문 서술("왜곡 부분집합에서 다른 모델 오차가 최대 50배")과 그림이 일치한다.
⚠ 레이더라 눈금 읽기가 어렵다 — **숫자는 `Table 1` 과 본문만 인용**하고 그림은 순위 판정용으로만 썼다. 크롭본은 세 번째 패널(회전 불일치)이 잘렸다.

### 7.4 회전 대칭 깨짐 (등변성을 강제하지 않은 대가)
Lebedev–Laikov 9차 격자로 회전시켜 예측 표준편차를 잰다. 본문: "대부분 예측오차보다 **1–2 자릿수 작고**, MC3D-random·MC3D-cluster 를 뺀 전 부분집합에서 **1 meV/atom 미만**". Orb-v2 는 훨씬 크고 때때로 실제 오차와 맞먹는다.
[배포자료] `mad-bench-PET-MAD-predictions.xyz`(1562 구조)에 구조별 `energy_rot_discrepancy`/`forces_rot_discrepancy` 가 들어 있다. 내가 계산한 **중앙값 0.0057, 최대 0.124**(본문 서술과 단위를 맞추면 meV/atom) — 모델 자체 MAE 15–20 meV/atom 대비 **3 자릿수 작다**. 실용상 무시 가능.

### 7.5 ⚠ **UMA 는 비교에 없다**
- 본문·SI·`Table 1`·`Fig. 2`·`Fig. 3` 어디에도 **UMA / fairchem / OMat24 학습 모델이 이름으로 등장하지 않는다.**
- `Fig. 1` 의 **회색 점** 중 하나일 수는 있으나 라벨이 없다. 이름 붙은 것 중 OMat24 계열은 **eSEN-30M-OAM**(0.018 eV/atom @ ~10⁸ 구조) 하나뿐 — UMA 와 **학습데이터 혈통은 같지만 다른 모델**이다.
- ⇒ **우리 UMA-s-1p1(omat)의 상대 위치는 이 논문으로 판정 불가.** 굳이 말하면 "PET-MAD 는 OMat24 혈통 모델보다 Matbench 상 2.3배 부정확하지만 학습데이터는 1000배 적다" 정도가 최대이고, 그마저 §7.1 의 참조 불일치 때문에 조심해야 한다.
- 그리고 **MAD-bench 1562 구조 안에 Li+P+S 를 동시에 가진 구조가 0개**다(내가 직접 셈: Li 253 · S 793 · P 515 · Cl 453 원자는 있으나 **thiophosphate 조합은 없음**). **황화물 SE 에 대한 근거는 §9 의 Li₃PS₄ 사례 하나뿐**이다.

## 8. LoRA vs bespoke vs full fine-tune ★

세 가지 전략이 나온다.

| 전략 | 정의 | 비용 | 기저(MAD) 성능 |
|---|---|---|---|
| **PET-Bespoke** | 계별 데이터로 **처음부터** PET 학습 | 데이터 많이 필요 · 학습 오래 | 없음(범용성 0) |
| **PET-MAD-LoRA** | 기저 가중치 **동결**, attention 블록마다 저랭크 행렬 2개 추가 (**rank 8, scale 0.5**) | 가장 쌈 | 부분 보존 |
| **full fine-tune** | 전 파라미터 미세조정 | 중간 | 파국적 망각 |

논문 결론(Methods "Fine-tuning"): **저데이터 영역에서는 파인튜닝이 항상 from-scratch 보다 낫고**, 큰 데이터셋에서는 전용 모델이 앞설 수 있으나 **이 논문의 BaTiO₃·succinic acid·Li₃PS₄·HEA 에서는 그렇지 않았다**. 권고: "특정 응용을 위해 PET-MAD 를 파인튜닝한다면 **LoRA 를 써라**".

⚠ 그런데 **"파국적 망각 완화" 주장은 SI Table 3(`Table S3`)이 절반쯤 반박한다**:

| LoRA 모델 | MAD test 에너지 MAE (meV/at.) | 힘 MAE (meV/Å) | 기저 대비 |
|---|---|---|---|
| (기저 PET-MAD) | **15.1** | **72.3** | — |
| BTO | 44.4 | 140.8 | **2.9× / 1.9×** |
| GaAs | 78.8 | 134.5 | 5.2× / 1.9× |
| HEA25S | 91.1 | 228.9 | 6.0× / 3.2× |
| **LPS (Li₃PS₄)** | **129.4** | **215.1** | **8.6× / 3.0×** |
| Succinic acid | 144.4 | 191.1 | 9.6× / 2.6× |
| Water | 284.8 | 288.3 | **18.9× / 4.0×** |

→ **LoRA 를 걸고 나면 범용성은 사실상 소실된다**(에너지 3–19배 악화). "varying degree of accuracy 를 유지한다"는 문장은 맞지만, **"파인튜닝한 모델을 committee 의 범용 멤버로 계속 쓸 수 있다"는 뜻은 아니다.** 우리 계획에 직접 영향(§15).

## 9. ⭐ Li₃PS₄ — 우리 계 (별도 절)

### 9.1 무엇을 했나
- 대상: **α, β, γ-Li₃PS₄** 세 상 (γ = 저온 비-초이온상, β = 중간, α = 고온 초이온상).
- 관측량: **이온전도도 σ(T)** — **Green–Kubo 선형응답**으로. 전하 flux **J_q = (e/Ω)Σ q_i v_i**, q_i 는 **공칭 산화수**(Li +1, P +5, S −2). σ = (Ω/3k_BT)∫₀^∞ ⟨J_q(t)·J_q(0)⟩ dt.
- 참조/데이터 출처: **Gigli, Tisi, Grasselli, Ceriotti, *Chem. Mater.* 36, 1482 (2024)** — "Mechanism of charge transport in lithium thiophosphate"(ref 39). 시스템 전용 데이터셋도 여기서 왔다.
- 비교 모델 3종: **PET-MAD(그대로)** / **PET-Bespoke(LPS 데이터로 from scratch)** / **PET-MAD-LoRA(rank 8)**.

### 9.2 MD 조건 — **[배포자료] 원본 LAMMPS 입력 직독** ★

`inputs/Li3PS4/{alpha,beta,gamma}-768atoms/Temp*/0.input-lammpsNPT.lammps` **48개 파일 전부**를 파싱했다.

| 항목 | 논문 본문(Methods) | **[배포자료] 실제 입력 파일** |
|---|---|---|
| 셀 | quasi-cubic **768 원자**, α/β/γ | ✔ 같음 (`alpha_align_732.data`, `beta_align_732.data`, `gamma_LPS_4x4x3.input`) |
| 앙상블 | **NPT**, 등방 **p = 0 atm** | ✔ `fix 1 all npt/kk temp T T $(100*dt) iso 0.0 0.0 $(1000*dt)` → **T_damp 0.2 ps · P_damp 2 ps** |
| 온도 | "450–900 K" | **475–900 K, 16점** (475–800 을 25 K 간격 + 850 + 900). γ 는 675/750/800 이 `u*` 폴더로 분리 |
| **timestep** | **1 fs** | ⚠ **2 fs** (`timestep 0.002`, units metal) |
| **길이** | 열화 200 ps + 전류수집 **4 ns** | ⚠ **총 3 ns** (`run 1500000` × 2 fs), 단일 run |
| 모델 | (본문엔 3종) | **48개 전부 `finetuningLoRA_response/2/model.pt`** — 즉 **배포된 입력은 LoRA 재실행분(referee response)** 한 벌뿐 |
| 시드 | 명시 없음 | `velocity all create T <seed>` — **α·β 전부 956748, γ 전부 555748** → **온도당 단일 궤적, 시드 반복 없음** |
| 질량중심 | "고정" | `mom yes rot yes` (생성 시 선/각운동량 제거) |
| flux 샘플링 | — | `fix printvel ... 10` → **20 fs 마다 종별 속도합**(= J_q 입력). dump 도 10 스텝 |
| 실행 | — | Slurm 1 노드 **GPU 1장**, LAMMPS-Kokkos + `pair_style metatensor/kk`, 23:50 h walltime |
| 누락 | — | ⚠ **γ 의 `input-structures/` 폴더가 배포본에 없다** (α·β 는 있음) → γ 재현 불가 |

**우리 프로토콜과의 대비**(중요):

| | PET-MAD (Li₃PS₄) | **우리 (LPSCl 계열)** |
|---|---|---|
| 셀 | **768 원자** | **52 원자**(comp2 기준) |
| 길이 | 3–4 ns / 온도 | **200 ps** / 온도 (+ 5 ps 열화) |
| 온도점 | **16점** | **3점**(600/800/1000 K) |
| 앙상블 | **NPT** (p=0) | **NVT Langevin**(friction 0.02) |
| σ 추정자 | **Green–Kubo 전하 flux** (교차상관 포함 = Haven 비 자동 반영) | **Nernst–Einstein, Haven=1** (교차상관 무시) + MSD 2–50 ps |
| 오차막대 | 온도마다 **3–7 %** (GK 블록 통계) | 단일궤적엔 없음; modelc 3-seed 만 |

→ 이 표가 **"우리는 σ 절대값을 인용하지 않는다"는 규율이 왜 옳은지**를 외부 근거로 보여준다. 그들은 **셀 15배·시간 15–20배·추정자도 더 완전**하고 그래서 ±5 % 를 붙일 수 있다.

### 9.3 결과 — **[배포자료] σ(T) 원수치 (figure-read 아님, exact)** ★

`data/figures_data/fig4/{PETMAD,PET,LoRA,Gigli}_{alpha,beta,gamma}_sigma_T.data` (열: T[K], σ[S/cm], σ_err[S/cm])

**β-phase** (우리 관심상 — 상온 LPS 의 실용상):

| T [K] | PET-MAD | PET-Bespoke | PET-MAD-LoRA | Gigli(ref 39) |
|---|---|---|---|---|
| 475 | 0.1662 ± 0.0102 | 0.1349 ± 0.0175 | 0.1098 ± 0.0066 | 0.1910 ± 0.0148 |
| 500 | 0.2711 ± 0.0172 | 0.2030 ± 0.0310 | 0.2110 ± 0.0113 | 0.2956 ± 0.0193 |
| 525 | 0.4625 ± 0.0300 | 0.3076 ± 0.0175 | 0.3455 ± 0.0210 | 0.4655 ± 0.0320 |
| 550 | 0.5439 ± 0.0450 | 0.5776 ± 0.0590 | 0.5223 ± 0.0260 | 0.6638 ± 0.0430 |
| 575 | 0.8359 ± 0.0580 | 0.7316 ± 0.0790 | 0.7066 ± 0.0380 | 0.8328 ± 0.0490 |
| **600** | **1.007 ± 0.050** | **1.151 ± 0.068** | **1.047 ± 0.052** | **1.226 ± 0.070** |
| 650 | 1.449 ± 0.084 | 1.583 ± 0.076 | 1.673 ± 0.083 | 1.731 ± 0.130 |
| 700 | 2.018 ± 0.084 | 2.094 ± 0.110 | 2.226 ± 0.095 | 2.274 ± 0.110 |
| 800 | 3.427 ± 0.180 | 3.193 ± 0.140 | 3.397 ± 0.140 | 3.166 ± 0.150 |
| 900 | 3.748 ± 0.170 | 3.837 ± 0.190 | 3.926 ± 0.150 | 3.661 ± 0.210 |

**α-phase**: 475 K 에서 이미 1.07–1.38 S/cm, 900 K 4.0–4.8 — **거의 평평**(초이온).
**γ-phase**: 475 K 에서 (0.79–1.47)×10⁻³ 로 시작해 **600 → 625 K 사이에서 한 자릿수 점프**(0.10–0.36 → 0.91–1.57), 그 뒤 α/β 와 같은 고전도 가지에 합류.

**모델 간 σ 비 (전 온도, 중앙값 / 범위)** — 내가 계산:

| phase | PET-MAD / bespoke | LoRA / bespoke | **Gigli(ref 39) / bespoke** |
|---|---|---|---|
| α | **0.88** (0.80–0.94) | 0.96 (0.84–1.05) | 0.96 (0.81–1.11) |
| β | **0.96** (0.82–1.50) | 0.99 (0.81–1.12) | 1.06 (0.94–1.51) |
| γ | **0.98** (0.58–1.87) | 0.90 (0.66–1.09) | 0.95 (0.36–1.11) |

🔑 **핵심 판독**: **"범용 PET-MAD vs 전용 bespoke" 의 차이가, "전용 bespoke vs 또 다른 전용 모델(Gigli 2024 의 원래 NN)" 의 차이보다 크지 않다.** γ 의 넓은 범위는 전부 전이 구간(600–625 K)에서 나온다.

**Ea (아레니우스)** — ⚠ **논문에 없다. 배포 원수치에 내가 직접 ln(σT) vs 1/k_BT 회귀를 돌린 값**:

| 구간 | Gigli(ref 39) | PET-Bespoke | PET-MAD-LoRA | **PET-MAD** |
|---|---|---|---|---|
| α, 475–900 K | 0.157 (r²0.983) | 0.165 (0.991) | 0.156 (0.992) | **0.168** (0.993) |
| β, 475–900 K | 0.317 (0.982) | 0.356 (0.975) | 0.363 (0.974) | **0.323** (0.984) |
| γ, 650–900 K (고전도 가지) | 0.216 (0.963) | 0.209 (0.989) | 0.198 (0.967) | **0.245** (0.985) |
| γ, 475–600 K (저전도 가지) | 1.068 (0.940) | 1.025 (0.954) | 1.048 (0.963) | **1.101** (0.959) |

🔑 **범용 대 전용의 Ea 계통오차 = 0.012 eV(α) / 0.033 eV(β) / 0.036 eV(γ-고온).**
우리 modelc 3-seed 시드산포가 **±0.032 eV**, comp2 가 **±0.033 eV** 다 — **범용 모델을 쓰는 대가가 우리 시드 잡음과 같은 크기**다.

### 9.4 학습곡선 — 몇 개의 DFT 구조가 필요한가 ★ (`Fig. S9`)

[배포자료] `data/datasets/Li3PS4/{train,val,test}.xyz` 를 직접 셌다:
- **train 1940 / val 243 / test 243 = 총 2426 구조**, 전부 **화학량론 Li₃PS₄**
- 크기 분포: **16 원자 384개 · 32 원자 2007개 · 64 원자 35개** → **대부분이 32 원자짜리 작은 셀**

[배포자료] `figures_data/figs9/mae_{energy,forces}.txt` — **test MAE vs 학습셋 크기** (배포 parity 데이터로 역산해 자릿수까지 일치 확인 ✓):

| N_train | LoRA E∣F | Bespoke E∣F | **full-FT** E∣F | PET-MAD(기저) |
|---|---|---|---|---|
| **97** | **2.56 ∣ 50.9** | 2.99 ∣ 70.4 | 2.33 ∣ 48.6 | 4.90 ∣ 63.9 |
| 194 | 2.15 ∣ 48.0 | 2.45 ∣ 55.9 | 2.00 ∣ 45.1 | ↑ |
| **388** | 2.10 ∣ **45.3** | 1.97 ∣ **46.9** | 1.64 ∣ 42.8 | ↑ |
| 776 | 1.86 ∣ 43.2 | 1.52 ∣ 39.0 | 1.45 ∣ 37.4 | ↑ |
| 1164 | 1.74 ∣ 43.2 | 1.78 ∣ 37.8 | 1.47 ∣ 36.5 | ↑ |
| 1552 | 1.63 ∣ 39.2 | 2.75 ∣ 36.4 | 0.93 ∣ 30.0 | ↑ |
| **1940** | 1.42 ∣ 39.2 | **1.16 ∣ 35.6** | **0.86 ∣ 29.0** | ↑ |

🔑 세 줄 요약:
1. **DFT 구조 ~100개만으로 LoRA 가 기저 PET-MAD 를 넘고**(힘 50.9 < 63.9), **from-scratch 전용 모델도 이긴다**(50.9 < 70.4).
2. **교차점은 N ≈ 400**. 그 위로는 bespoke 가 힘에서 앞선다.
3. **full fine-tune 이 전 구간에서 최고**(N=1940 에서 29.0 meV/Å). ⚠ 그런데 **`Fig. S9` 에는 이 곡선이 그려져 있지 않다** — SI §11.2 본문은 "완전 파인튜닝(초록)이 ~20 % 낫다"고 쓰는데 **그림엔 초록 선이 없다**(§17). 배포 노트북 `figs9.ipynb` 를 열어 보니 fullFT 열을 **읽기만 하고 plot 하지 않는다**.

### 9.5 이 사례의 논문 결론
> "세 상 모두에서 PET-MAD 는 bespoke·fine-tuned 모델과 훌륭히 일치하며, 더 큰 validation 오차에도 불구하고 **정량적 정확도**를 보인다. γ 상에서만 고전도 상으로의 **전이 온도를 약간 과대평가**한다. 이 차이를 빼면 PS₄ 사면체 회전에 따른 σ 거동 변화까지 포착한다."

**그림을 실제로 보고 확인한 것**(`Fig. 4`): 세로축 log σ (10⁻³–~4 S/cm), 가로축 **1000/T (1.1–2.1 K⁻¹)** — 위쪽에 T 눈금 병기. 3패널(α/β/γ)에 각 상의 768원자 셀 스냅샷 인셋.
- **범례는 3개뿐**(PET-MAD ■ 검정 / PET-Bespoke ● 파랑 / PET-MAD-LoRA ▲ 주황). **ref 39(Gigli) 곡선은 그려져 있지 않다** — 배포 노트북 `fig4.ipynb` 도 Gigli 파일을 `loadtxt` 만 하고 plot 하지 않는다. 즉 **"ref 39 와 정량적으로 일치한다"는 문장은 주장만 있고 그림에 증거가 없다.** (내가 배포 원수치로 확인한 결과 그 주장 자체는 **참**이다 — §9.3 표 마지막 열.)
- γ 패널의 실제 모양은 "**전이온도 과대평가**"보다 "**전이가 뭉개졌다**"에 가깝다: 600 K 에서 PET-MAD 0.364 는 bespoke 0.194 의 **1.9배로 높고**, 625 K 에서 0.910 은 bespoke 1.573 의 **0.58배로 낮다**. 즉 **저온 가지는 과대, 급점프는 한 온도격자(25 K) 늦다.** 본문 서술은 후자만 말한다(§19).

## 10. 나머지 다섯 사례 (요약 — 우리에겐 방법 참고용)

| 사례 | 셋업 | PET-MAD ∣ bespoke ∣ LoRA (E meV/at.∣F meV/Å) | 결론 |
|---|---|---|---|
| **GaAs 융점** (`Fig. 5`) | interface pinning, **1152 원자 17×17×90 Å**, 1 ns, **dt 4 fs**, 950–1200 K/50 K, LAMMPS+PLUMED, Steinhardt Q4 CV | 14.4∣74.1 ∣ 0.7∣29.0 ∣ 1.3∣45.3 | **1111±72 vs 1169±4 K**. UQ(128 멤버 재가중)가 그 격차를 정확히 감싼다. 실험 1511 K 는 **PBEsol 자체 한계** |
| **HEA 표면편석** (`Fig. 6`) | fcc(111) **7×7×11 = 539 원자**, REMD/MC **16 replica**, 200 ps, NPT dt 2 fs, log T 500–1200 K, Γ_a @800 K | 25.8∣175.1 ∣ 14.6∣138.3 ∣ 9.4∣124.8 | 사전학습·파인튜닝 모델이 거의 동일한 Ni-농축 편석 패턴. **bespoke 가 오히려 과적합**(HEA25S 3만 중 ~2000 만 재계산) |
| **액체 물 NQE** (`Fig. 7`) | **128 분자(384 원자)**, PIMD, 298 K/1 atm, i-PI 3.1 + LAMMPS | (본문 수치 없음; 데이터셋 1228 구조) | g(r)·C_V 가 bespoke 와 일치. 단 **GGA 답게 물의 융점을 과대평가**해 298 K 가 과냉각 액체처럼 나온다 |
| **succinic acid ¹H NMR** (`Fig. 8`) | MD/PIMD **dt 0.5 fs, 250 ps, NPT 1 bar/300 K, 32 beads**, SOAP 선형 shielding 모델 | 12.5∣106.1 ∣ 3.1∣86.0 ∣ 2.0∣64.5 | 세 potential 의 shielding 분포가 거의 겹침. 양자요동이 ¹H 분포를 크게 아래로 이동·확장 |
| **BaTiO₃ 유전응답** (`Fig. 9`) | **320 원자(4×4×4)**, flexible-cell MD 40–400 K, Nosé–Hoover 압력 + SVR 온도, λ-SOAP 쌍극자 모델 | 12.67∣27.96 ∣ 0.23∣9.41 ∣ 0.12∣3.92 | 상전이 T 최대 불일치 **<30 K**, ε_r 곡선 약 25 K 이동. **오차가 50배 큰데도 전이를 맞힌다** |

> 🔑 **여섯 사례 공통 패턴**: **PET-MAD 의 raw MAE 는 bespoke 보다 5–50배 나쁜데, 관측량(σ, g(r), Γ_a, shielding 분포, ε_r)은 거의 같다.** 유일하게 무너지는 곳이 **자유에너지 차이로 정의되는 양**(융점, 전이온도)이다. 우리 식으로 옮기면: **수송·구조 관측량은 범용으로 충분하고, 상안정성·전이는 아니다.**

## 11. 비보존력(non-conservative) 경고 — SI §12 ★ (`Fig. S16`, `Fig. S17`)

PET-MAD 는 backprop 없이 힘을 직접 뱉는 head 를 함께 학습했다(≈2× 가속). SI 가 그 대가를 **BMIM-Cl 이온성 액체 500 K** 로 실측한다.

- **NVE (dt 0.5 fs, velocity Verlet)**: 보존력은 초기 온도 근처에서 정상 요동. **직접 힘은 운동에너지가 지수적으로 폭주**해 분자가 해리된다. **MTS(8스텝마다 보존력으로 보정)는 보존력과 동일한 안정 궤적**.
- **NVT + 공격적 전역 thermostat(SVR, τ_L = 10 fs)**: 전체 온도는 500 K 근처로 잡히지만, **종별 온도가 갈라진다 — Cl 이 2000 K 이상**, H 등이 그만큼 아래. 즉 **thermostat 이 병을 감추기만 한다.**
- **관측량 파괴**(`Fig. S17`, 직접 봄): g_ClCl(r) 에서 **직접 힘만 r ≈ 3.1 Å 에 가짜 Cl–Cl 이합체 봉우리**를 만들고 1.8 Å 부터 밀도가 새어 나온다. MSD_Cl 은 **보존력 8 ns 에 4.2 Å², 직접 힘은 200 ps 만에 축을 벗어남**(= 확산 자릿수 과대). MTS 는 보존력과 통계오차 안에서 일치(3.6 Å²).

> 🔑 **우리에게 직결**: MLIP-MD 로 **D 와 Ea 를 재는 우리 작업에서, 힘이 보존장이 아니면 D 가 계통적으로 부풀 수 있다**(§15-③).

## 12. 불확실도 정량화 — LLPR / shallow ensemble ★

- **LLPR**(last-layer prediction rigidity): σ_i² = α f_iᵀ (FᵀF + ε²I)⁻¹ f_i. 마지막 층 특징 f 의 학습셋 공분산만 있으면 되고 **추가비용 거의 0**.
- 여기서 **마지막 층 가중치를 N=128 세트 샘플**해 **shallow ensemble** 을 만든다 → 임의의 복잡한 워크플로에 오차 전파 가능(앙상블 멤버 수에 비례하는 비용이 **없다**).
- 검증(`Fig. S6`): MAD test 의 예측 불확실도 vs 실제 구조별 오차 parity — 8개 부분집합 전부에서 기대분포를 거의 정확히 따른다. **단, "학습 도메인 안에서"** 라고 논문이 명시.
- 활용 예: GaAs 융점(`Fig. 5`, 128 멤버 재가중 → 1111 **±72** K), 포논 밴드 앙상블(`Fig. S7`, BeO 광학모드가 물러진 것이 UQ 분산 증가로 드러남).

## 13. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | Pareto: 학습셋 크기 vs Matbench(WBM) E_hull MAE. PET-MAD 9.6e4 구조 / 0.041 eV·at⁻¹ (일관참조) · 0.138(비일관). 색 = 파라미터 수 | 데이터효율 논거의 원본. ⚠ **UMA 이름 없음**, PET-MAD 만 다른 참조로 평가 — 세로 비교 조심 |
| 2 | MAD 8개 부분집합별 E/F MAE **레이더**(5모델) + 회전 불일치 패널 | PET-MAD 의 우위가 **왜곡·분자 부분집합**에 집중돼 있음을 확인. 안정 무기결정에선 무승부 |
| 3 | 원자수 32–10⁴ 에서 MD 처리량(µs/atom, H100), water/diamond/Al 3패널, 적색 × = OOM | ⭐ **왼쪽 끝이 평평** = 소형 셀은 런치 오버헤드 지배 → **우리 52원자 셀은 GPU 를 놀리고 있다**(§15) |
| **4** | **α/β/γ-Li₃PS₄ σ(T) 아레니우스**(1000/T 1.1–2.1), PET-MAD/bespoke/LoRA 3종 | ⭐ **우리 계 유일 근거.** 범용≈전용 판정의 원본. 원수치는 배포자료에 exact 로 존재(§9.3) |
| 5 | GaAs Δμ(solid−liquid) vs T + **128 LLPR 앙상블 멤버(회색 실선)** | UQ 전파의 표본 예. bespoke 선이 앙상블 띠 안에 들어옴 = UQ 가 정직 |
| 6 | CoCrFeMnNi (111) Gibbs 표면과잉 Γ_a (800 K, REMD/MC) | 표면편석 워크플로 참고. bespoke 과적합 사례 |
| 7 | 액체 물 g_OO/g_OH + C_V vs bead 수 (PIMD 298 K) | 핵양자효과까지 범용으로 되는지의 근거. GGA 융점 과대 캐비앳 |
| 8 | α-succinic acid ¹H 화학적 차폐 분포 (MD vs PIMD) | 관측량-수준 일치 사례 |
| 9 | BaTiO₃ ε_r(T) + 상 분류 CV 지형 인셋 | 상전이 온도 <30 K 오차 = "자유에너지 양은 어렵다"의 반례성 사례 |
| S1 | 하이퍼파라미터 Pareto (정확도 vs **원자당 추론시간**) | 속도를 최적화 축에 넣은 설계 — 우리가 모델 고를 때 같은 관점 |
| S3 | 원소별 고립원자 에너지: MAD 설정 vs SSSP 권장 설정 차이 (10⁻³–10² meV) | ⭐ **"조성마다 cutoff 바꾸면 안 된다"의 정량 근거** — 우리 db 일관성 규율의 외부 앵커 |
| S4 | 9개 원소 이합체 곡선 (H,C,O,Na,Ga,Ti,Si,**Cl**,Ne) DFT vs PET-MAD | 단거리 반발이 학습으로 제대로 들어갔는지 — MLIP 신뢰성 점검 관례 |
| **S5** | 1000회 LBFGS 기하최적화 시간분포 + **미완료 실행 수**(주황) | ⭐ **우리 UMA fmax 0.05 미수렴 사건과 같은 축.** 비보존 Orb-v2 만 9–11 % 실패 |
| S6 | LLPR / shallow-ensemble 불확실도 vs 실제오차 parity (8 부분집합) | UQ 신뢰도 근거 |
| S7 | BeO/BeTe/LiBr 포논 밴드: DFT vs PET-MAD LLPR 앙상블 | 포논에도 UQ 를 붙이는 법. BeO 광학모드 연화 = 범용 MLIP 공통병 |
| S8 | PET-MAD 학습곡선(데이터 20→100 %) | 60 % 넘으면 train 오차가 되레 증가 = 과적합 불가능한 다양성 |
| **S9** | **Li₃PS₄ 학습곡선** (bespoke vs LoRA vs 기저 PET-MAD) | ⭐ **"우리가 DFT 몇 개 찍어야 하나"의 직답: ~100 개부터 이득, ~400 에서 교차** |
| S10–S15 | GaAs / HEA / water / succinic / BTO 학습곡선 + shielding parity | 계별 파인튜닝 데이터요구량 사례집 |
| **S16** | BMIM-Cl NVE·NVT 운동온도 궤적 (보존 vs 직접 vs MTS) | ⭐ **직접힘의 파국** — Cl 이 2000 K 로 갈라짐. 우리 D/Ea 신뢰성 점검 논거 |
| **S17** | 같은 계 g_ClCl(r) + MSD_Cl (보존/직접/MTS) | ⭐ **직접힘이 확산을 자릿수로 부풀린다** — 우리 MLIP-MD 에 대한 직접 경고 |
| Table 1 | 7개 공개 데이터셋 × 5모델 E∣F MAE | 정확도 위치의 원본 표 |
| Table S1 | MAD 8개 부분집합 정의·구조 수 | 데이터셋 구성 원본 |
| **Table S3** | LoRA 파인튜닝 후 **MAD 기저 성능** | ⭐ **파국적 망각이 실제로 얼마나 일어나는지**(3–19배) — LoRA 를 committee 멤버로 못 쓰는 이유 |

**내가 실제로 이미지로 본 그림 (8장)**: `Fig. 1`, `Fig. 2`, `Fig. 3`(+배포 PNG 로 Al 패널 보완), `Fig. 4`, `Fig. 5`, `Fig. S5`, `Fig. S9`, `Fig. S17`.
**안 본 그림 (18장)**: `Fig. 6`–`Fig. 9`, `Fig. S4`, `S6`, `S7`, `S8`, `S10`–`S16`, 표 3장(`Table 1`·`Table S1`·`Table S3` 는 PDF 텍스트로 읽음 — 표는 이미지보다 텍스트가 정확).

## 14. Post-processing ★

| 무엇 | 도구 | 수치화 방식 |
|---|---|---|
| **이온전도도 σ** | LAMMPS(27 Jun 2024, Kokkos 4.3.1) + `pair_style metatensor/kk`; **Green–Kubo** | 종별 속도합을 20 fs 마다 기록 → J_q(t) → 자기상관 적분. 온도마다 오차막대(3–7 %) |
| **융점** | LAMMPS + **PLUMED**, interface pinning, Steinhardt **Q4** CV | 구속력 평균 ∝ Δμ → Δμ(T)=0 근찾기 |
| **표면편석** | REMD/MC(원자 교환), 16 replica | **Gibbs 표면과잉** Γ_a = (N_a − N_a^B·N/N^B)/S, 벌크영역 = 슬랩 중심 10 Å |
| **핵양자효과** | **i-PI 3.1** (LAMMPS backend), PIMD, 32 beads(succinic)/가변(water) | C_V 는 Yamamoto scaled-coordinate virial 추정자 |
| **NMR shielding** | GIPAW 참조 + **SOAP(featomic) 선형 대리모델** | ¹H σ_iso test RMSE **0.17 ppm** (원 kernel 모델 0.16) |
| **유전응답** | **λ-SOAP 등변 선형 쌍극자 모델** + MD 공분산 | ε_r,αβ = δ_αβ + cov(M_α,M_β)/(ε₀Ωk_BT); 상은 **Gaussian mixture 로 CV 공간 clustering**, Δμ^{kk'} = −k_BT ln(ΣP_k/ΣP_k') |
| **포논** | phono3py / phononDB(PBEsol) 참조 | LLPR 앙상블을 밴드에 전파(`Fig. S7`) |
| **불확실도** | LLPR + 128멤버 shallow ensemble | 궤적 재가중(thermodynamic reweighting)으로 관측량에 전파 |
| **시각화/탐색** | chemiscope + PET-MAD featurizer(sketch-map) | 마지막층 특징으로 데이터셋 2D/3D 지도 |

## 15. ⭐⭐ 우리 시야 — 판정

> 배경(2026-08-19 우리 실측): UMA-s-1p1(omat) 사용. DFT 이완 구조는 잘 유지(modelC +0.92 %, b2o3 −0.00 %). 그런데 **이상화 대칭 canonical Li₆PS₅Cl 에서 fmax 0.05 로 미수렴 → 27.478 Å³/atom (진짜 최소 20.415)**, cascade 부피축이 이것 때문에 뒤집혔다. NEB inter-cage 단일경로 0.528 eV vs MD Ea 0.253 vs 실험 0.2–0.35.

### ① PET-MAD 를 UMA 의 **대안**으로 쓸 만한가 → **아니오(교체는 부적절), 예(추가는 유익)**

**교체하지 말아야 하는 이유 3개:**
1. **근거가 없다.** MAD-bench 1562 구조에 **Li+P+S 동시 함유 구조 0개**, 아르지로다이트·Li–P–S–Cl 계 근거는 **논문 전체에 0**. 우리에게 있는 유일한 증거는 Li₃PS₄(무-Cl, 화학량론) 한 계다.
2. **참조 범함수가 다르다.** PET-MAD = **PBEsol**(QE/SSSP, non-magnetic, vdW 없음). 우리 DFT 정본 = **PBE**(QE/USPP, ecut 60/480). UMA-omat = OMat24(VASP PBE 계열). **세 축이 서로 다르다.** 우리 규율("문헌 수치는 소환값, 방법 명시 없이 이식 금지")을 그대로 적용하면, PET-MAD 로 뽑은 부피·에너지를 우리 PBE 표에 넣을 수 없다.
3. **우리 db 의 연속성**. comp1/modelc/b2o3/LPSOCl 의 D·Ea 가 전부 UMA 로 잡혀 있다. 엔진을 갈면 **전 계열 재계산**이고, 그건 "새 수치"가 아니라 "새 축"이다.

**그럼에도 도입 가치가 큰 이유 3개:**
1. **속도**: `Fig. 3` 기준 PET-MAD 는 MACE-MP-0-M 대비 3–6×, 파라미터는 2.8 M. **A6000 48 GB·RTX3090 24 GB 어느 쪽에도 부담이 아니다**(2.8 M 파라미터면 가중치가 ~11 MB). VRAM 은 전혀 문제가 아니고, gabia 의 제약은 **pw.x 와 동시 실행 금지**(CLAUDE.md) 쪽이다.
2. **built-in UQ**: `calculate_uncertainty=True` 한 줄로 LLPR 불확실도가 나온다. **"이 배열이 학습분포 밖인가"를 모델 하나로** 물어볼 수 있다. UMA 에는 우리가 아는 한 이런 게 없어서 §②의 committee 를 짜고 있었다.
3. **성질이 다른 학습 데이터**: MAD 는 **rattled·조성 무작위·나노클러스터·표면**이 전체의 절반 가까이다. 우리가 다루는 **무질서 아르지로다이트·SEI 계면·비정질**은 MP-이완궤적 계열(MPtrj/OMat24)의 사각지대인데, MAD 는 정확히 그쪽을 겨냥해 만들어졌다.

**판정**: 🟡 **"UMA 대체" 가 아니라 "UMA 옆에 두는 두 번째 눈"**. 우리 정본 축(D·Ea·부피)은 UMA 로 유지하고, PET-MAD 는 **검증·탐지·파인튜닝 실험용**으로 별도 env 에 깐다.

### ② committee 파트너로 쓰는 게 나은가 → **예. 그리고 지금 있는 3개보다 낫다**

`tools/ionic/mlip_committee.py` 가 이미 `uma / mace / sevennet` 를 지원한다. 여기에 PET-MAD 를 **네 번째 엔진으로 추가하는 것이 가장 값싸고 가장 정보량이 크다**.

**왜 PET-MAD 가 최적 파트너인가** — 우리 도구 docstring 이 이미 지적했듯 "MACE-MP-0·SevenNet-0 은 **둘 다 MPtrj**, UMA 는 OMat24" 라서 **셋이 서로 상관돼 있다**. 상관된 멤버로 짠 committee 는 **불일치를 계통적으로 과소평가**한다. PET-MAD 는
- 학습 데이터가 **완전히 다르고**(MAD 9.6만, 왜곡 편중),
- 참조 범함수도 **다르며**(PBEsol vs PBE 계열),
- 아키텍처도 다르다(비등변 transformer vs 등변 GNN).
→ **가장 탈상관된 멤버**. extrapolation 탐지기로서는 이게 정확히 원하는 성질이다.

**구체 처방 (코드 수정은 하지 않았다 — 처방만):**
```
① 별도 conda env (⚠ UMA env 에 절대 넣지 말 것 — §④)
     conda create -n petmad && conda activate petmad
     conda install -c metatensor -c conda-forge pet-mad
② tools/ionic/mlip_committee.py 의 get_calc() 에 분기 1개 추가 (새 파일 금지 — 기존 도구 확장)
     if engine == "petmad":
         from pet_mad.calculator import PETMADCalculator
         return PETMADCalculator(version="1.0.2", device=device)   # 논문 재현 버전 고정
   그리고 argparse 의 choices 에 "petmad" 추가. 그게 전부다 — predict 는 이미 엔진별
   env 에서 따로 돌려 npz 로 떨구는 구조라 나머지는 손댈 게 없다.
③ 기준선 재교정 필수: --baseline 없이 평형 벌크 표본으로 먼저 "교정 모드"를 돌려
   새 기준선 json 을 만든다. PBEsol×PBE 혼합이라 **불일치 바닥값이 올라간다** —
   기존 uma/mace/sevennet 기준선을 그대로 쓰면 전부 "외삽"으로 오판한다.
④ 에너지는 쓰지 않는다. 범함수가 다르면 절대에너지·조성 baseline 이 다르므로
   **force RMS 불일치만** 본다 — 다행히 mlip_committee.frame_disagreement() 가 이미 힘만 쓴다.
```
⚠ **§8 의 경고**: LoRA 파인튜닝한 PET-MAD 는 MAD 기저 성능이 **3–19배** 나빠진다(`Table S3`, LPS 는 8.6×/3.0×). 그러니 **committee 멤버로는 반드시 기저 PET-MAD(v1.0.2)를 쓰고, 파인튜닝본을 멤버로 넣지 않는다.**

### ③ ⭐ 그림에서 나온 **뜻밖의 소득 2개** (우리 현안에 바로 걸린다)

**(a) `Fig. S5` — 우리 fmax 0.05 미수렴 사건에 이름이 붙는다.**
1000회 LBFGS(fmax 0.05, 최대 100 스텝)에서 **비보존(직접힘) 모델만 9–11 % 수렴 실패**했고 나머지 넷은 0 이다. 힘이 어떤 에너지의 gradient 가 아니면 **line search 가 일관되지 않아 optimizer 가 맴돈다** — 정확히 우리가 canonical Li₆PS₅Cl 에서 본 증상이다.
> ⚠ **UMA-s-1p1 이 직접힘(비보존) 모델인지 나는 이 논문으로 확인할 수 없다.** 이 논문에 UMA 는 없다. 그러니 이건 **가설**이고, 확인은 30초짜리다:
> **유한차분 검사** — 원자 하나를 ±δ(예 1e-3 Å) 움직여 `(E(+δ)−E(−δ))/2δ` 와 `-F` 를 비교한다. 수치오차(≲1e-3 eV/Å) 이상으로 갈리면 비보존이다.
> 결과가 "비보존"이면 우리 처방은 명확하다: (i) 이완은 **fmax 를 느슨하게 잡고 마지막에 DFT 로 마감**, (ii) 또는 **MTS 방식**(N 스텝마다 보존 기준으로 보정) — 이 논문이 1.8× 가속을 유지하며 아티팩트를 없앤 방법.

**(b) `Fig. S16`/`Fig. S17` — 우리 D·Ea 에 대한 정직한 의심 한 줄.**
직접힘 MD 는 **전역 thermostat 아래서도 종별 온도가 갈라지고**(Cl 2000 K↑), **MSD 가 자릿수로 부푼다**. 만약 UMA 가 비보존이라면 우리 **D(600 K) 3.09e-6 / 7.90e-6 cm²/s 와 Ea 0.253/0.224 eV** 가 같은 방향(D 과대, Ea 과소)으로 편향돼 있을 수 있다. **NEB 0.528 eV 와 MD 0.253 eV 의 큰 격차 중 일부**가 여기서 올 가능성이 있다(전부는 아니다 — NEB 단일경로 vs MD 다경로/협동운동이 원래 큰 몫).
> 다행히 **우리 프로토콜이 그들보다 방어적이다**: 우리는 **Langevin(per-atom, friction 0.02)** 을 쓰는데, 이건 SVR 같은 전역 thermostat 과 달리 **각 원자에 개별적으로 등분배를 강제**한다 → 종별 온도 분리를 억제한다. 다만 **억제하는 것이지 없애는 게 아니다**(thermostat 이 비보존 일을 계속 상쇄하며 동역학을 바꾼다).
> **비용 0에 가까운 점검 2개**: ① 같은 셀로 **NVE 20 ps** 를 돌려 총에너지 drift 를 본다. ② 기존 NVT 궤적에서 **Li/P/S/Cl 별 운동온도**를 따로 평균낸다. 갈리면 그 자체가 결론이다.

**(c) `Fig. 3` 왼쪽 끝 — 우리 52 원자 셀은 GPU 를 놀리고 있다.**
30–60 원자 구간에서 모든 모델이 200–400 µs/atom 으로 수렴한다 = **원자당 비용이 아니라 스텝당 고정 오버헤드**가 지배한다. 우리 comp2 셀은 52 원자다. **2×2×2 로 키워 416 원자로 가면 통계는 8배인데 벽시계는 2–3배**밖에 안 늘 가능성이 크다(그림상 400 원자대는 아직 평탄부에 못 미침). 그러면 **200 ps 단일궤적의 잡음 문제(우리가 400/500 K 를 버려야 했던 이유)** 를 계산비 거의 그대로 두고 완화할 수 있다.
> ⚠ 이건 **PET-MAD 를 도입하든 안 하든 유효한 처방**이고, 엔진 무관이다. 다만 우리 UMA 는 **ASE 경유**라 Python 오버헤드가 더 크므로 이득은 그림보다 클 수도, 작을 수도 있다 — **실측 1회**(52 vs 416 원자, 1000 스텝 타이밍)로 끝난다.

### ④ LoRA 파인튜닝을 우리 LPSCl 에 적용하면 — 비용 견적

**필요한 DFT 구조 수**: `Fig. S9`+배포자료가 직답한다. **~100개면 기저를 이기고, ~200개면 from-scratch 를 확실히 이기고, ~400개면 bespoke 와 교차**한다. Li₃PS₄ 데이터셋의 구조는 **16–64 원자(대부분 32)** — 우리 52 원자 아르지로다이트 셀과 같은 체급이다.

**시간 견적 (우리 자원 기준)**:
| 단계 | 내용 | 견적 |
|---|---|---|
| 스냅샷 추출 | 기존 UMA-MD 궤적(600/800/1000 K)에서 200–400 프레임 층화추출 | 분 단위, 이미 있는 자산 |
| DFT 라벨 | QE SCF **200–400회**, 52 원자 | 우리 설정(60/480 Ry)이면 GPU 1장에 구조당 수 분 → **하루 안** |
| ⚠ MAD 정합 라벨 | PBEsol + SSSP-eff + **110/1320 Ry** 로 맞추면 평면파 수 ~2.5배 → SCF 비용 **3–6배** | **2–4일** |
| LoRA 학습 | metatrain, rank 8/scale 0.5, 단일 GPU | **시간 단위**(2.8 M 파라미터 중 저랭크 행렬만 학습) |

**⚠ 여기서 갈림길이 하나 있다 — 라벨을 어느 설정으로 찍나.**
- **(A) 우리 PBE/USPP/60 Ry 로 찍는다**: 싸다. 하지만 PBEsol 기저 위에 PBE 라벨을 얹는 것이라 **이 논문이 SI §4–5 에서 통째로 경고한 "참조 불일치"** 를 우리가 스스로 만드는 셈(그들 실측: WBM 에서 baseline 차 **120 meV/atom**, 원소별 고립원자 차 10–100 meV/atom). 다만 **힘은 에너지 offset 에 둔감**하고 MD 를 굴리는 건 힘이므로, **σ·Ea 용도로는 (A)로도 실용상 괜찮을 가능성이 높다**. ⛔ 대신 **그 모델로 뽑은 에너지/부피/hull 은 우리 PBE 표에 절대 못 넣는다.**
- **(B) MAD 설정으로 다시 찍는다**: 비싸지만 정직하고, 논문의 6개 사례가 전부 이 방식(**"MAD DFT 설정으로 재계산"**)이다.
→ **권고: 목적이 수송(σ·Ea)이면 (A) 로 시작하되 라벨 설정을 digest·db 에 명시**, 목적이 에너지/안정성이면 **(B) 아니면 하지 말 것**.

### ⑤ zhang2026(MACE 파인튜닝 ~200 config + NEP 증류)과 어느 쪽이 우리에게 싼가

두 논문이 **놀랍도록 같은 숫자에 수렴**한다: **필요한 ab initio 구조 = O(10²)**.

| 축 | **PET-MAD + LoRA** (이 논문) | **MACE-FT + NEP 증류** (zhang2026, 61번) |
|---|---|---|
| 기저 모델 | PET-MAD (PBEsol / MAD 9.6만) | MACE-MP-0 (PBE+U / MPtrj 158만) |
| 필요한 DFT 수 | **~100–400** (Li₃PS₄ 실측) | **~200 configurations** (LGPS/LATP/LYC) |
| 단계 수 | **1단계** (LoRA) | **2단계** (파인튜닝 → NEP 증류) |
| 최종 MD 속도 | GNN 그대로 (H100 Al 기준 15 µs/atom) | **NEP** — 대규모 MD 용 경량 potential |
| 우리 계와의 거리 | Li₃PS₄ **황화물 SE 직접 실증** | LGPS(황화물)·LATP·LYC — **황화물 SE 직접 실증** |
| 우리 엔진과의 관계 | 새 엔진 추가 | 새 엔진 추가 (MACE 는 committee 에 이미 있음) |
| 기저 모델 그대로의 성능 | Li₃PS₄ σ 가 이미 bespoke 의 0.88–0.98 | **MACE-MP-0 는 그대로론 부족** (이동장벽 관련 상대 RMSE ~22.8 %) |

**판정**: 🟢 **지금 우리 규모(52–416 원자, 200 ps)에서는 PET-MAD LoRA 가 싸다.**
이유는 단순하다 — **zhang2026 의 2단계(NEP 증류)는 "대규모·장시간 MD 속도"를 사는 단계인데, 우리는 §③(c) 에서 봤듯 지금 처리량이 아니라 오버헤드에 묶여 있다.** 증류로 살 이득이 없다. 반대로 **10⁴–10⁵ 원자 / µs 스케일**(예: 다결정 GB, 슬랩 계면 장시간)로 갈 계획이 생기면 그때는 zhang2026 쪽이 유일한 답이 된다.
한 가지 zhang2026 이 이기는 축: **MACE-MP-0 는 우리 committee 에 이미 들어 있어서**(mlip_committee.py) 환경이 이미 있다. PET-MAD 는 env 를 새로 만들어야 한다.

### ⑥ 설치 가능성 판정 — **별도 env 필수**

```
[의존성 실물 확인]
  pet-mad 1.4.3 (repo bf3fba9) → dependencies = metatrain==2025.10  ← **하드 == 핀**
                                  + huggingface_hub, hf_xet, packaging, platformdirs, tqdm, scipy>=1.15
  논문 재현용 requirements.txt  → metatensor-torch==0.6.3 / metatensor-operations==0.3.0 /
                                  metatensor-core==0.1.11 / pet-neighbors-convert
  python >= 3.10
```
- 🔴 **gabia 의 fairchem/UMA env 에 절대 넣지 말 것.** `metatrain==2025.10` 은 하드 핀이고, 그게 metatensor-torch 스택과 **특정 torch 버전**을 끌고 온다. fairchem 도 torch 를 핀한다 → **UMA env 가 깨질 실질 위험**. 우리 정본 D·Ea 축이 전부 그 env 에 걸려 있으니, 이건 감수할 위험이 아니다.
- 🟢 **권장**: repo README 대로 **Miniforge 기반 별도 conda env**. (README 가 Anaconda 채널은 의존성 해석이 어긋난다고 명시적으로 경고한다.) LAMMPS 연동까지 하려면 conda 설치가 사실상 필수.
- **VRAM**: 2.8 M 파라미터 — A6000 48 GB·RTX3090 24 GB 어느 쪽도 여유. 실제 제약은 **CLAUDE.md 의 "pw.x 와 UMA 동시 실행 금지"** 와 같은 성격: **PET-MAD 도 GPU 를 잡으므로 nvidia-smi 확인 후 실행**.
- **LAMMPS-metatomic 빌드**: 논문 실행은 커스텀 lammps-kokkos 빌드였다. **우리 규모에선 필요 없다 — ASE calculator 로 충분**하고, committee 용도(§②)는 ASE 만 쓴다.
- **모델 버전 고정**: `version="latest"` 는 시간이 가면 바뀐다. 논문 재현·우리 기록 재현성을 위해 **`version="1.0.2"` 로 못 박는다**(README: v1.0.2 = 논문 재현용 stable, v1.1.0 = dev·분자계 성능 저하로 프로덕션 비권장).
- **보너스**: 같은 패키지에 **PET-MAD-DOS**(`PETMADDOSCalculator.calculate_bandgap/ calculate_dos/ calculate_efermi`)가 들어 있다. 우리 밴드갭 축과 겹치지만 ⛔ **정본에 못 쓴다** — 별도 논문(arXiv 2508.17418)이고, 학습 참조가 **PBEsol** 이라 우리 PBE fixed-occ nscf 정본(2.066/2.099/1.9671/2.2309 eV)과 **자가 다르다**. 스크리닝 1차 필터로는 흥미로울 수 있다.

## 16. 우리 DFT/MLIP 기준 대비 (comp1 / modelc) → `../our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 이유 — **진짜 차이 vs 방법 인공물** |
|---|---|---|---|
| MLIP 엔진 | PET-MAD 2.8 M (PBEsol/MAD) | **UMA-s-1p1 (omat)** | **다른 축.** 이 논문에 UMA 없음 → 상대 정확도 **판정 불가** |
| 참조 범함수 | **PBEsol**, non-magnetic, vdW 없음 | **PBE** (QE/USPP, 60/480 Ry) | ⚠ **방법 차이** — 수치 이식 금지. 힘 기반 관측량(σ·Ea)은 상대적으로 둔감 |
| 대상 조성 | Li₃PS₄ (무-Cl, 화학량론) | Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆ / +B₂O₃ / LPSOCl | **화학이 다르다.** Cl·무질서·공공 화학이 이 논문엔 없음 |
| σ 추정자 | **Green–Kubo 전하 flux**(교차상관 포함) | **Nernst–Einstein Haven=1**(교차상관 무시) | **진짜 방법 차이.** σ 절대값 비교 자체가 성립 안 함 |
| MD 셀·시간 | 768 원자 · 3–4 ns · 16 온도점 | 52 원자 · 200 ps · 3 온도점 | **진짜 차이(통계 품질).** 그들이 ±5 % 오차막대를 붙일 수 있는 이유 |
| Ea (β-Li₃PS₄) | **0.323**(PET-MAD) / 0.356(bespoke) / 0.317(ref 39) eV | comp1 **0.253** · modelc **0.224** (단일궤적) · modelc 3-seed 0.197±0.032 · comp2 0.275±0.033 | **조성이 다르니 값 비교 금지.** 가져올 것은 값이 아니라 **"범용−전용 계통차 = 0.012–0.036 eV"** 라는 스케일 |
| **모델선택 계통오차** | **σ 비 0.88–0.98 · Ea 차 ≤0.036 eV** | 우리 시드산포 **±0.032–0.033 eV**, 철회한 단일시드 σ 비 1.33× | 🔑 **우리 잡음과 같은 크기.** "단일시드 1.33× 철회"(SEMIFINAL 2026-07-09) 판단이 외부 근거로 지지된다 |
| 이완 수렴 | LBFGS fmax **0.05**, 100 스텝; 비보존 모델만 9–11 % 실패(`Fig. S5`) | **UMA fmax 0.05 미수렴** → 27.478 vs 20.415 Å³/atom | 🔑 **같은 증상의 문헌 선례.** 단 UMA 보존성 여부는 **우리가 확인해야 함**(§15-③a) |
| MD 힘 보존성 | 직접힘 → **MSD 자릿수 과대**, 종별 온도 분리(`Fig. S16`, `Fig. S17`) | 우리 D·Ea 는 전부 UMA-MD | ⚠ **잠재적 계통편향** — NVE drift + 종별 T 점검 필요(§15-③b) |
| 밴드갭 | 논문 본문 없음. (패키지의 PET-MAD-DOS 는 별도 논문·PBEsol) | comp1 2.066 / modelc 2.099 / b2o3 1.9671 / LPSOCl 2.2309 eV (PBE fixed-occ nscf) | **비교 불가.** 우리 규율(DOS-threshold 금지, PBE 과소평가) 유지 |
| ESW / 산화 onset | **없음** | 2.256 V (S²⁻-limited, GG set) | 이 논문은 전기화학 창을 다루지 않는다 |
| 기계 (E/B/G) | 없음(포논만 `Fig. S7`) | E_VRH 22.06/27.66 GPa, B₀ 26.23/21.71 GPa | 비교항 없음 |

## 17. ⭐ 검산 기록 — **내가 실제로 확인한 것 / 어긋난 것**

**자기정합 확인 (✓ 통과)**
1. `Table S1` 8개 부분집합 합 = 33,596+30,044+2,800+5,589+9,071+2,676+8,578+3,241 = **95,595** ✓ 본문 값과 일치.
2. Li₃PS₄ 배포 parity 데이터(243 test 구조)에서 MAE 재계산 → **PET-MAD 4.903∣63.90**, **bespoke 1.165∣35.57** — 본문의 "4.9∣63.9", "1.2∣35.6" 과 **자릿수까지 일치** ✓
3. 배포 `mae_forces.txt` 의 N=1940 값이 parity 재계산과 일치 ✓
4. 학습셋 크기 1940 = 배포 `train.xyz` 구조 수 ✓ (val 243 / test 243)

**어긋난 것 (⚠ 인용 전 확인 필요)**
| # | 무엇 | 본문 | SI / 배포자료 |
|---|---|---|---|
| 1 | 전하밀도 cutoff | **1320 Ry** (Methods) | **1360 Ry** (SI §5) |
| 2 | Li₃PS₄ MD **timestep** | **1 fs** (Methods) | **2 fs** (배포 LAMMPS 입력 48/48) |
| 3 | Li₃PS₄ MD **길이** | 열화 200 ps + 수집 **4 ns** | **총 3 ns 단일 run**(1.5 M × 2 fs) |
| 4 | Li₃PS₄ 온도범위 | "450–900 K" | **475–900 K** (최저점 475) |
| 5 | Li₃PS₄ LoRA MAE | **1.3 ∣ 36.0** (validation) | 배포 test 값 **1.42 ∣ 39.23** (~9 % 차) — PET-MAD·bespoke 는 일치하는데 LoRA 만 다름 |
| 6 | `Fig. S9` 곡선 수 | SI §11.2 본문 "**세 시나리오**(from-scratch·LoRA·**완전 파인튜닝**)" | 그림엔 **두 곡선뿐**. 배포 `figs9.ipynb` 가 fullFT 열을 읽고 **plot 하지 않음** |
| 7 | "ref 39 와 정량적으로 일치" | 본문 주장 | `Fig. 4` 에 **ref 39 곡선 없음**; `fig4.ipynb` 가 Gigli 파일을 `loadtxt` 만 하고 미사용. (주장 자체는 배포 원수치로 확인하면 **참**) |
| 8 | HEA 파인튜닝 구조 수 | "**2000** randomly chosen" (1000+500+200+200+100) | SI §11.4 "only contains **1975** structures" |
| 9 | 학습 스케줄러 | "250 epoch 마다 LR **반감**", 1500 epoch, batch 24 | 배포 yaml = **cosine** scheduler; 1단계 2000 epoch(batch 24) + 2단계 1500 epoch(batch 16) |
| 10 | 배포 yaml 의 성격 | (본문은 LoRA 를 계별 파인튜닝으로 서술) | `options-c-finetune.yaml` 은 `finetune: method: "full"` — **PET-MAD 자체의 2단계 학습**이지 계별 LoRA 설정이 아님. **계별 LoRA yaml 은 배포에 없음** |
| 11 | γ-Li₃PS₄ 재현성 | — | **`gamma-768atoms/input-structures/` 폴더 자체가 배포본에 없음** (α·β 는 있음) → γ MD 재현 불가 |
| 12 | 오타 | — | SI §4 "MAE drops from 138 meV/atom to **41 eV/atom**" (meV 오타) |

**시드/오차막대 감사**
- Li₃PS₄ MD 는 **온도당 단일 시드**(α·β 956748, γ 555748 고정). σ 오차막대는 **시드 반복이 아니라 단일 궤적의 GK 블록 통계**다. → **`Fig. 4` 의 오차막대는 통계오차이지 재현성 오차가 아니다.**
- GaAs 융점의 ±는 **LLPR 앙상블(모델 epistemic)** 이지 MD 시드가 아니다.
- BTO ε_r 만 "4개 독립 MD 의 표준편차"로 진짜 시드 오차막대를 붙였다.

## 18. 인용 가능 문장 (deck / 원고용)

- "범용 MLIP 를 황화물 고체전해질에 그대로 적용해도, 전용 모델 대비 이온전도도 비 0.88–0.98·활성화에너지 차 0.036 eV 이내였다 [Mazitov, Nat. Commun. 2025, 16, 10653]."
- "같은 계에서 **전용 모델 두 개 사이의 차이**가 **범용 대 전용의 차이**만큼 컸다 — 즉 모델 선택의 계통오차가 전용화 여부보다 크지 않다 (배포 원수치 기반 자체 검증)."
- "MLIP 를 계에 맞추는 데 필요한 ab initio 구조는 **O(10²)** 이다 — LoRA 는 ~100 구조에서 이미 범용 기저와 from-scratch 전용 모델을 둘 다 앞선다 [Mazitov 2025 Fig. S9; 같은 결론이 MACE 파인튜닝에서도 ~200 configuration]."
- "참조 DFT 설정의 불일치만으로 에너지 기준선이 **120 meV/atom** 어긋날 수 있다 — 이는 모델 자체 오차보다 크다. 따라서 조성 간 비교는 동일 설정에서만 유효하다 [Mazitov 2025 SI §4–5]."
- "직접(비보존) 힘 예측은 2배 빠르지만, 전역 thermostat 아래서도 종별 운동온도가 갈라지고 확산계수를 자릿수로 과대평가한다 [Mazitov 2025 SI §12]."
- ⛔ **쓰면 안 되는 문장**: "PET-MAD 가 UMA 보다 (부)정확하다" — **이 논문에 UMA 는 없다.**

## 19. 주의 / 한계 (비판)

1. **자기 데이터셋으로 자기 모델을 평가한다.** `Table 1` 의 MAD 행에서 PET-MAD 가 4–5배 앞서는 것은 **정의상 그럴 수밖에 없다**(다른 모델에겐 완전한 out-of-domain). 논문도 "not too surprising" 이라 쓰지만, **초록의 "competitive with state-of-the-art" 인상은 이 행이 상당 부분 떠받친다**. 공정한 축은 MPtrj·Alexandria(거기선 진다)와 SPICE·MD22(거기선 이긴다)다.
2. **`Fig. 1` 의 세로 비교는 같은 자 위가 아니다.** PET-MAD 만 **자기 설정으로 재계산한 참조**에 맞춰 0.041 을 얻고, 나머지는 원 WBM 참조로 평가된다. 저자들이 리더보드 등재를 스스로 포기했을 만큼 이 문제를 알고 있는데, **그림은 여전히 한 평면에 같이 그린다**. 비일관 참조 값 0.138 을 흐린 라벨로 병기한 건 정직하지만, 눈에는 0.041 이 먼저 들어온다.
3. **속도 비교의 비대칭.** 정확도는 **가장 큰** 변종(MACE-MP-0-**L**, MatterSim-**5M**)으로, 속도는 **가벼운** 변종(MACE-MP-0-**M**, MatterSim-**1M**, SevenNet-**0**)으로 비교한다. 논문이 명시하니 은폐는 아니지만, **"정확하면서 빠르다"는 한 문장은 두 개의 다른 비교에서 온 것**이다.
4. **"메모리 효율" 주장의 증거가 약하다.** 메모리 곡선이 없고 OOM 십자표뿐이다.
5. **파국적 망각 완화 주장 대 `Table S3`.** LoRA 후 MAD 성능이 **3–19배** 나빠진다. "완화한다"는 맞지만 "유지한다"는 아니다. Water LoRA 는 284.8 meV/atom — 기저의 **19배**.
6. **UMA/fairchem 계열 부재.** 2025년 시점 가장 널리 쓰이는 범용 모델군 중 하나가 비교에 없다. eSEN-30M-OAM 이 `Fig. 1` 에 있으니 데이터 접근이 문제는 아니었다.
7. **시드 반복이 사실상 없다.** Li₃PS₄ 48개 MD 가 상당 온도당 단일 시드다. 우리 규율(멀티시드 판정)로 보면 **`Fig. 4` 의 모델 간 미세 차이는 시드 잡음과 분리되지 않았다.** (다행히 우리가 쓰려는 결론 — "차이가 작다" — 은 이 한계에 강건하다.)
8. **γ 상 서술이 그림과 미묘하게 다르다.** 본문은 "전이온도를 약간 과대평가"라 하지만 원수치는 **저온 가지 과대 + 급점프 1격자 지연**이다(600 K 1.9배 높음). "과대평가"만 읽으면 저온 쪽 방향을 반대로 안다.
9. **PBEsol 고정의 대가를 논문이 인정한다.** 물 융점 과대, BTO/GaAs 전이·융점이 실험과 크게 어긋남(1111 vs 실험 1511 K). **"실험과 맞는가"는 이 논문의 축이 아니다** — 전부 "DFT 참조와 맞는가"다. 우리가 실험(Ea 0.2–0.35 eV)과 대조할 때 이 논문을 근거로 쓸 수 없다.
10. **배포자료와 본문 불일치 12건**(§17). 특히 **MD timestep·길이**가 다르다는 건, `Fig. 4` 를 재현하려는 사람이 본문만 보고는 못 한다는 뜻이다. γ 입력구조 누락까지 겹치면 **γ 패널은 현재 배포본으로 재현 불가**.
11. **우리 계에 대한 근거 부재.** Cl·무질서·공공·계면이 전혀 없다. Li₃PS₄ 결과가 Li₆PS₅Cl 로 전이된다는 보장은 이 논문 안에 **없다**.

## 20. 기법 용어 미니사전

- **PET (Point Edge Transformer)**: 원자쌍(방향성 결합)을 토큰으로 삼아, 각 원자의 이웃 토큰 집합에 transformer 를 태워 메시지를 갱신하는 GNN. 회전 등변성을 수학적으로 강제하지 않고 **data augmentation 으로 배운다**(→ §7.4 의 회전 불일치 지표로 감시).
- **conservative vs non-conservative force**: 보존력 = 예측 에너지의 −∇(autograd). 비보존력 = 별도 head 로 힘을 **직접** 회귀. 후자가 2–3배 빠르지만 어떤 에너지의 gradient 도 아니어서 **NVE 에서 에너지가 표류**하고 optimizer/thermostat 이 병든다.
- **MTS (multiple time stepping)**: 대부분 스텝은 싼 힘(직접), N 스텝마다 비싼 힘(보존)으로 보정. 여기선 M=8 로 **1.8× 가속을 유지하면서 아티팩트 제거**.
- **LoRA (Low-Rank Adaptation)**: 기저 가중치를 **동결**하고 각 attention 블록에 저랭크 행렬 두 개(rank r)만 더해 학습. 학습 파라미터가 극소라 저데이터에서 강하고, 원 모델 능력을 부분 보존.
- **LLPR (last-layer prediction rigidity)**: 마지막 층 특징의 학습셋 공분산으로 사후 불확실도를 계산. **σ² = α fᵀ(FᵀF+ε²I)⁻¹f**. 추가비용 ~0.
- **shallow ensemble**: 마지막 층 가중치만 여러 벌 샘플해 만든 앙상블(여기선 128). 전체 모델 앙상블과 달리 **비용이 멤버 수에 비례하지 않는다**.
- **Green–Kubo σ**: 전하 flux 자기상관의 시간적분으로 전도도를 얻는 선형응답 공식. **NE(Haven=1)와 달리 이온 간 교차상관(Haven 비)을 자동 포함**한다.
- **interface pinning**: 고-액 공존 셀에 질서변수(Steinhardt Q4) 구속을 걸고, 평균 구속력으로 **Δμ(액−고)** 를 재어 Δμ=0 에서 융점을 찾는 법.
- **REMD/MC**: replica-exchange MD + 원자 종 교환 Monte-Carlo. 확산이 느린 합금에서 **조성 자유도까지 평형화**시키기 위한 조합.
- **Gibbs 표면과잉 Γ_a**: (슬랩의 원소 a 수 − 벌크 비율로 기대되는 수)/표면적. **벌크층 두께 선택에 무관**하게 표면 친화도를 재는 지표.
- **PIMD / bead**: 양자 핵을 P 개의 고전 복제(bead)를 스프링으로 이은 고리로 사상. P→∞ 에서 정확, P=1 이면 고전 MD.
- **SSSP (Standard Solid-State Pseudopotentials)**: 원소별로 검증된 pseudo 라이브러리(efficiency/precision 세트). 원소마다 권장 cutoff 가 다르다 — 이 논문은 그걸 **일부러 무시하고 최대값 일괄 적용**했다(§4.2).
- **rotational discrepancy**: 같은 구조를 여러 각도로 회전시켜 예측값 표준편차를 잰 것. 비등변 모델의 대칭 깨짐 크기.

## 21. INDEX / comparison 넣을 항목 (⚠ **파일 충돌 회피 — 여기에만 적어 둔다**)

> 다른 에이전트 2개가 `INDEX.md` · `comparison_vs_ours.md` · `comparison_vs_ours_DEM.md` 를 동시에 만지고 있어 **이 digest 는 그 세 파일을 건드리지 않았다.** 아래를 그대로 옮겨 붙이면 된다.

**(a) `litdb/INDEX.md` — "✅ Digest 완료" 표에 추가할 행**

```
| `papers/petmad2026_lightweight_universal_interatomic_potential_mad.md` | **[외부·methods·도구판정]** Mazitov/Bigi(공동1)/Kellner/Pegolo/Tisi/Fraux/Pozdnyakov/Loche/**Ceriotti** (EPFL COSMO), "**PET-MAD as a lightweight universal interatomic potential for advanced materials modeling**" (**Nat. Commun. 2025, 16, 10653**, DOI 10.1038/s41467-025-65662-7; 본문 14 pp · Fig 9 · Table 1 · SI 20 pp · Fig S1–S17 · Table S1–S3) — **9.6만 구조·2.8 M 파라미터 범용 MLIP**. MAD 데이터셋(8 부분집합, 85 원소, **일부러 왜곡시킨 rattled/조성무작위 절반**) + **전 원소 동일 DFT**(QE 7.2+SIRIUS, **PBEsol**, SSSP v1.2-eff, **110/1320 Ry**, non-magnetic, k 0.125 Å⁻¹). **⭐ 여섯 사례 중 하나가 Li₃PS₄(황화물 SE)** — 768원자 NPT MD, Green–Kubo σ, α/β/γ 16 온도점: **범용 PET-MAD σ/bespoke = 0.88–0.98**, **Ea 차 ≤0.036 eV**(배포 원수치로 우리가 회귀). **LoRA 는 DFT ~100 구조에서 이미 기저·from-scratch 를 둘 다 이기고 ~400 에서 bespoke 와 교차**(`Fig. S9`). 속도 H100 Al 8k atoms **≈15 µs/atom·step**(MACE-MP-0-M 87 · MatterSim-1M 47 · SevenNet-0 62, figure-read). **비보존(직접힘) head 2× 가속의 대가**: NVE 폭주·종별 온도 분리(Cl>2000 K)·**MSD 자릿수 과대**(`Fig. S16`/`Fig. S17`), 기하최적화 9–11 % 미수렴(`Fig. S5`). ⚠ **UMA/fairchem 이 비교군에 없음** · MAD-bench 1562 구조에 **Li+P+S 동시 구조 0개** · Cl·무질서·아르지로다이트 근거 0 · **LoRA 후 MAD 기저 성능 3–19배 악화**(`Table S3`) · 배포자료↔본문 불일치 12건(MD dt 1 vs 2 fs, 길이 4 ns vs 3 ns, γ 입력구조 누락 등) | **도구 판정 — 재료비교 0.** ①**UMA 대체 아님, committee 4번째 멤버로 최적**(MPtrj 계열 3종과 달리 데이터·범함수·아키텍처가 전부 탈상관) ②`tools/ionic/mlip_committee.py` `get_calc()` 에 분기 1줄 + 별도 conda env(metatrain==2025.10 하드핀 → **UMA env 오염 금지**) ③**우리 fmax 0.05 미수렴·D 과대 의심에 문헌 선례** → UMA 보존성 유한차분 점검 처방 ④**52원자 셀은 GPU 오버헤드 지배 구간**(`Fig. 3` 좌단) → 416원자 승격 검토 ⑤범용−전용 계통차(0.012–0.036 eV)가 **우리 시드산포(±0.032)와 동급** = "단일시드 1.33× 철회" 판단의 외부 지지 |
```

**(b) `litdb/comparison_vs_ours.md` — 축별 추가 항목**

- **A(이온전도) 축**:
  - `petmad2026…` — **Li₃PS₄ β상 Ea 0.323(PET-MAD) / 0.356(bespoke) / 0.317(Gigli 2024) eV**(⚠ 배포 원수치로 우리가 회귀, 논문 미보고). 우리 comp1 0.253 / modelc 0.224 와 **조성이 달라 값 비교 금지**. 가져오는 것은 **"모델 선택 계통차 ≤0.036 eV"** 라는 스케일뿐 — 우리 시드산포 ±0.032 eV 와 동급.
  - **σ 추정자 차이 명시**: 그들 **Green–Kubo 전하 flux**(교차상관 포함) vs 우리 **NE Haven=1**. 셀 768 vs 52 원자, 3–4 ns vs 200 ps, 16 vs 3 온도점. → **σ 절대값 인용 금지 규율의 외부 근거**.
  - **처방**: 우리 MD 셀을 52 → 416 원자로 올리는 비용 실측(`Fig. 3` 좌단이 오버헤드 지배 구간임을 시사).
- **D(전자구조) 축**: 해당 없음(이 논문은 밴드갭·DOS 를 다루지 않는다). 패키지의 **PET-MAD-DOS 는 별도 논문·PBEsol** 이라 우리 PBE fixed-occ nscf 정본(2.066/2.099/1.9671/2.2309 eV)과 **섞지 않는다**.
- **B(산화안정 4축)**: 해당 없음(ESW·grand-potential 없음).
- **C(기계)**: 해당 없음(탄성 없음; 포논은 BeO/BeTe/LiBr 만).
- **방법론(축 밖)**: **참조 DFT 불일치만으로 에너지 기준선 120 meV/atom 이동**(SI §4) + **원소별 고립원자 10–100 meV/atom**(`Fig. S3`) → **우리 db 조성 간 비교는 동일 ecut/k-mesh/pseudo 에서만 유효**하다는 규율의 정량 앵커.
</content>
</invoke>

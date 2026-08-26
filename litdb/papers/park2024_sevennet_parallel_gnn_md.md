# Scalable Parallel Algorithm for Graph Neural Network Interatomic Potentials in Molecular Dynamics Simulations — Park (J. Chem. Theory Comput. 2024)

> slug `park2024_sevennet_parallel_gnn_md` · DOI `10.1021/acs.jctc.4c00190` · type `methods (병렬 알고리즘 + MLIP 구현 + 검증 MD)` · PDF `litdb/inbox/71. Park2024_SevenNet_Parallel_GNN_MD.pdf` (+ SI 5 pp) · digested `2026-08-26` · status ✅
> **저자**: Yutack Park, Jaesun Kim, Seungwoo Hwang, **Seungwu Han\*** (서울대 재료공학부 + 신소재공동연구소; Han 은 KIAS 겸직) — *J. Chem. Theory Comput.* **20**, 4857–4868 · 접수 2024-02-14 / 수정 2024-05-21 / 채택 2024-05-21 / 게재 2024-05-30 · 본문 **12 pp** · SI **5 pp** · Fig **6개**(본문) + **2개**(SI) · Table **0개** · refs **58**
> elements: Si, O, N
> methods: MLIP, MD, AIMD, DFT
> 🎤 **관련 발표**: `talks/lee2026_skku_mlip_materials_design.md` §7a (슬 22) · §99-3 A1 · §99-4 A1 · ⛔ 그 talk 은 citable=no — **이 논문이 정본이고, 덱/구술과 어긋나면 이 논문이 이긴다**

---

## 0. 이 digest 를 읽는 법 — ⚠ 먼저 읽을 것

**이건 물성 논문이 아니라 시스템/알고리즘 논문이다.** 배터리·Li·황화물·argyrodite 가 **한 글자도**
안 나온다. 벤치마크 계는 **α-quartz SiO₂**(타이밍 전용)와 **비정질 Si₃N₄**(검증 전용) 둘뿐이다.
σ·Ea·ESW·탄성·band gap 이 **0건**이라 `comparison_vs_ours.md` 의 **물성 4축(A/B/C/D)에 안 들어간다**
(→ **§J-7 `🔧 방법 원전`** 블록에만).

**핵심 기여 한 줄**: 메시지패싱 GNN 포텐셜을 **공간분할(spatial decomposition)** 로 병렬화하는
방법을 만들고, 그것을 **LAMMPS 에 붙인 패키지 SevenNet** 으로 구현했다. 부산물로 범용 사전학습
모델 **SevenNet-0** 을 공개했다.

**우리가 이걸 읽는 이유는 두 개다.**

> ### 🔴 ① T1b 대조군 — 결론부터: **이 논문은 T1b 를 판정하지 못한다.**
>
> SevenNet 은 **NequIP 기반 등변(equivariant) GNN** = **우리 UMA(eSEN 기반 등변 GNN)와 같은 계열**이다.
> 그래서 *"PES softening 이 GNN 계열 공통 성질인가, 모델·훈련셋 문제인가"* 를 가르는 대조군으로
> 받았다. 그런데 **이 논문은 PES softening 을 재는 실험을 하나도 안 했다**:
> **에너지 보존(NVE) 검사 0 · 장시간 드리프트 0 · 고온 스냅샷의 MLIP↔DFT 에너지/힘 재평가 0 ·
> 포논 0 · 탄성 0 · 융점 0 · 장벽/전이상태 0.** 유일한 MLIP↔DFT 정량 대조는 **결정 test set MAE**
> (= 평형 근처)이고, 고온 쪽 검증은 **비정질 구조 지표**(g(r)·g(θ)·배위수) **하나뿐**이다.
> ⇒ **"이 논문이 softening 을 반증했다/입증했다" 로 쓰면 안 된다.** ⚠ Shapeev γ 판독에서
> *"UMA 에는 γ 정의가 없다"* 로 근거를 넘어간 전례가 있다 — 같은 실수를 여기서 반복하지 않는다.
>
> **다만 정황은 하나 얻었고, 그 방향이 덱과 반대다** (→ §13 에서 자세히):
> SevenNet-0 은 **결정 구조만으로 학습**했는데도(저자 명시: *"Disordered phases like liquid or
> amorphous are not present in the training set"*) **5000 K 초가열 → 3000 K → 급랭** 을 거쳐
> 11.2만 원자 비정질 Si₃N₄ 를 만들었고 배위수·g(r)·g(θ) 가 DFT 참조와 맞았다.
> 우리 UMA 의 훈련셋 **OMat24 는 AIMD·Rattled 부분집합을 포함**한다
> (`papers/uma2026_family_of_universal_models_for_atoms.md` — UMA 논문이 *"OMat24 를 AIMD/Rattled 로
> 분리"* 하는 개선안을 적고 있고, `Table 11` 의 **OMat24 Force RMS = 2.83 eV/Å** 자체가
> 평형 구조만으로는 나올 수 없는 값이다) — 즉 **비평형 방향으로 UMA 쪽이 더 넓다.**
> 덱 슬 8 의 *"평형 근처 훈련점에 치우쳐 고에너지에서 물러진다"* 기구가 참이라면,
> **더 좁게 학습한 SevenNet-0 이 먼저 무너졌어야 한다.**

> ### 🔧 ② 우리 T3(Li‖LPSCl 대형 반응 MD) 의 **비용 산정 원본**
> 이 논문은 등변 GNN 의 **원자·시간당 실제 처리량**을 A100 단위로 준다:
> **≈1.58×10⁶ atom·ps/day per A100** (SevenNet-0 급 5층 모델, 우리 산술 · §14).
> 우리 T3-small(≈7,000 원자 × 20 ns)로 환산하면 **≈89 A100-day** — 이게 왜 이상욱 랩이
> 20 ns·50 ns 계면 MD 를 **GNN 이 아니라 MTP** 로 돌렸는지의 **비용 쪽 답**이다 (Q-T2 의 절반).

---

## 1. 한 줄 요약

메시지패싱 GNN 포텐셜은 수용영역이 `r_c × (층 수)` 로 넓어져 공간분할 병렬화가 어려운데,
**통신 반경을 원래 `r_c` 로 묶고 대신 층마다 forward/reverse 통신을 반복**하는 방식으로 이 문제를
풀었다. NequIP 아키텍처 위에 구현한 **SevenNet**(LAMMPS 연동)은 32-GPU 에서 **weak scaling 80 %↑**,
strong scaling 은 **GPU 가 충분히 채워질 때만** 이상적에 가깝다(12,960 원자 32-GPU 에서 최대 15.3×).
사전학습 모델 **SevenNet-0**(M3GNet 데이터셋, 결정만)으로 **112,000 원자 비정질 Si₃N₄ melt–quench** 를
실증했다.

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | Y. Park, J. Kim, S. Hwang, **S. Han\*** (서울대 MSE + RIAM; Han = KIAS 겸직) |
| 저널/년 | *J. Chem. Theory Comput.* **20**, 4857–4868 (2024) |
| DOI | `10.1021/acs.jctc.4c00190` |
| 대상 계 | **α-quartz SiO₂**(성능 벤치마크) · **비정질 Si₃N₄**(응용 실증) · SevenNet-0 은 MP 기반 **89 원소** |
| 연구유형 | 순수 계산 (알고리즘 + 구현 + MD). **실험 0건** |
| 코드·데이터 | 패키지 `https://github.com/MDIL-SNU/SevenNet` · 벤치마크 스크립트/결과 `10.6084/m9.figshare.25573938.v2` |
| 지원 | 삼성종합기술원 Global Research Cluster (벤치마크 = **삼성 SSC-21** 클러스터) · Si₃N₄ MD 는 **KISTI** (KSC-2023-CRE-0337) · 학습은 **KIAS CAC** |
| 이름 | **Seven**Net = **S**calable **E**qui**V**ariance-**E**nabled **N**eural **NET**work |

## 3. 핵심 수치 — 물성이 아니라 **정확도 + 성능**

### 3a. 정확도 (§5.1)

| 모델 | E MAE | F MAE | Stress MAE | 대상 |
|---|---|---|---|---|
| **SevenNet-0** | **25 meV/atom** | **0.070 eV/Å** | **0.68 GPa** | **M3GNet 데이터셋 test set** (전체의 5 %, materials 단위 분할) |
| M3GNet (ref 25 보고값, 저자가 인용) | 35 meV/atom | 0.072 eV/Å | **0.41 GPa** | 같은 데이터셋 |

- ⇒ SevenNet-0 이 **E·F 는 낫고 응력은 나쁘다**(0.68 vs 0.41 GPa). 저자는 *"has shown improvements in
  energy and force accuracies"* 라고만 쓰고 **응력이 1.7배 나쁜 것은 언급하지 않는다** (→ §10).
- ⚠ **SiO₂ 벤치마크용 20개 포텐셜의 정확도는 논문에 없다.** 전부 **타이밍 전용**으로 학습했고
  MAE·RMSE 를 한 줄도 보고하지 않는다 → **n/a**.
- ⚠ 이 test set 은 **MP 결정 구조의 이완 스냅샷**이다 = **평형 근처**. 고에너지·비평형 오차는 미측정.

### 3b. 성능 (§4, §5.2, SI)

| 항목 | 값 | 조건 |
|---|---|---|
| **Weak scaling (scaled-size)** | 32 GPU 에서 **0.67–0.83**(2층) ~ **0.79–0.84**(5층) | **4,608 원자/GPU**, 32 GPU = 147,456 원자, α-quartz SiO₂ |
| 〃 2 GPU | 0.83–0.98 (2층) / 0.95–1.0 (5층) | 〃 |
| **Strong scaling (fixed-size)** | 32 GPU 에서 speed-up **최대 15.3×**(이상 32×) | **12,960 원자** 고정 |
| 〃 최악 | 4 채널·2층은 **4 GPU 이상에서 이득 없음** (speed-up 2.4× 포화) | 〃 (figure-read `Fig. 5a`) |
| **SevenNet vs NequIP (단일 GPU)** | **1.99 vs 1.12 timesteps/s** (≈**1.8×**) | 32채널·4층·l_max 3·r_c 4.0 Å, α-quartz SiO₂ **4,608 원자**, A100 80GB @ **KISTI Neuron** |
| **Si₃N₄ melt–quench 실제 비용** | **112,000 원자 · 60 ps · 12.7 h · 8×A100** = *"0.1 ns/day with 0.1 million atoms"* | 저자 표현 그대로 |
| 〃 약스케일링 검증 | 14,000 원자(1/8) 단일 A100 **12.5 h** ⇒ **8 GPU 병렬효율 0.98** | 같은 프로토콜 |
| **SevenNet-0 vs MACE-MP-0** (`Fig. S2`) | SevenNet-0 448 원자/GPU: 1→8 GPU 에서 `figure-read ≈` **1.54 → 1.21** M-timesteps/day (효율 **≈0.79**) · MACE 다중GPU 는 **≈0.10 으로 평탄**, 단일GPU 를 **≈3,500–4,000 원자 이상**에서만 추월 | ⚠ **계·모델·출처가 다른 비교** (MACE 값은 ref 32 문헌값, 고엔트로피 합금 500 원자/GPU) |

**★ 우리가 뽑아낸 dt-무관 처리량** (우리 산술 · §14):
`112,000 원자 × 113 ps/day ÷ 8 GPU` = **1.58×10⁶ atom·ps/day per A100**
(교차검증: 14,000 원자 × 115 ps/day = 1.61×10⁶ — 0.98 효율과 일치 ✓)

---

## 4. 계산 방법 ★

### 4a. 아키텍처 — NequIP 대비 **무엇을 바꿨나**

| 항목 | SevenNet-0 | 근거 |
|---|---|---|
| 기반 | **NequIP**(Batzner 2022, ref 15) — E(3)-등변 GNN. *"SevenNet retains the NequIP architecture"* | §3.2 |
| 하이퍼파라미터 출처 | *"in line with **GNoME**"*(ref 24 = Merchant 2023) | §5.1 |
| **메시지패싱 층 수 T** | **5 interaction blocks** | §5.1 |
| **노드 feature 차원** | **128 scalars (l=0) · 64 vectors (l=1) · 32 tensors (l=2)** ⇒ **l_max = 2** | §5.1 |
| **cutoff r_c** | **5 Å** | §5.1 |
| 반경 기저 | **8개 radial Bessel** × 구면조화(l ≤ 2) 의 텐서곱 = convolutional filter | §5.1 |
| 정규화 | 모인 메시지 합을 **훈련셋에서 계산한 r_c 내 평균 이웃수**로 나눔 | §5.1 |
| **파라미터 수** | **0.84 M** (GNoME 은 **16.24 M**) | §5.1 |
| 구현 | PyTorch + **e3nn** 라이브러리(등변성 보장) + **TorchScript** JIT. 층마다 별도 TorchScript 파일 | §3.2 |
| MD 연동 | **LAMMPS** pair style. LAMMPS 통신 루틴을 그대로 씀 | §3.2 |
| 정밀도 | **single precision** (벤치마크) | §4 |

**★ NequIP 에서 실제로 손댄 것 2가지** (§5.1):
1. **self-connection 층의 텐서곱을 제거**했다. `Fig. 2b` 의 `⊗` 자리에 원소별(element-specific)
   파라미터가 몰려 있었는데, 이것을 **노드 feature 에 직접 거는 선형층**으로 교체 →
   *"a reduction in validation error and an increase in training error, which suggest a mitigation of overfitting"*.
   ⚠ **수치는 없다** — validation/training loss 값도 곡선도 안 나온다 (→ §10).
2. **마지막 interaction block 의 중복 텐서곱 경로 제거** — 스칼라 출력을 내는 경로만 남김.
⇒ 이 둘로 **16.24 M → 0.84 M** (19배 축소). ⚠ 어느 쪽이 얼마씩 줄였는지는 미분해.

**★ 병렬화의 핵심 제약 = 수용영역** (§1, `Fig. 1b`):
> *"GNN-IPs require a broader region for communication, **reaching up to r_c multiplied by the number
> of message-passing steps**."*

- SevenNet-0 은 **T=5, r_c=5 Å ⇒ 유효 수용영역 25 Å**.
- 단순 해법("통신 반경을 T·r_c 로 키운다")은 저자가 명시적으로 기각한다:
  *"simply expanding the communication radius would lead to a rapid increase in **redundant computations**,
  as neighboring processors possess a substantial **common subgraph**."*
- **이 논문의 해법**: 통신 반경을 **원래 r_c 로 묶고**, 대신 층마다 통신을 **반복**한다.

### 4b. 병렬 알고리즘 (§3.1, `Fig. 3`)

한 MD 스텝의 통신 스케줄 (T = 층 수):

| 순서 | 무엇을 주고받나 | 횟수 | 그림 |
|---|---|---|---|
| forward | ghost atom 의 **r, Z** | 1 | `Fig. 3c` |
| forward | 갱신된 **노드 feature h** | **T−1** | `Fig. 3d` |
| — | (전역 pooling 으로 E) | — | `Fig. 3a` |
| reverse | **∇_h E** (에너지 기울기) | **T−1** | `Fig. 3e` |
| reverse | **부분 힘 F** | 1 | `Fig. 3f` |

- **첫 interaction block 에는 통신이 없다** — ghost atom 의 `h^(1)` 은 `Z` 의 embedding 이라
  이미 forward 1단계에서 확보됐기 때문 (`Fig. 2a` 에서 첫 블록만 회색인 이유).
- **힘 계산이 더 까다롭다**: 엣지 힘 `F_vw = Σ_{t=1..T} (∂E/∂e_vw^(t))(∂e_vw^(t)/∂r_vw)` (eq 5),
  원자 힘 `F_v = Σ_{w∈N(v)} (F_vw − F_wv)` (eq 6). `F_wv` 에서 w 가 ghost 면
  **역방향 통신으로 되받아야** 한다 → `Fig. 3f`.
  `∂E/∂h_v^(T)` 는 통신이 필요 없고(마지막 층 뒤 E_v 는 h_v^(T+1) 에만 의존),
  `t = T−1 … 1` 로 **연쇄율(eq 8)** 을 역으로 내려오며 ghost 항을 매번 되받는다.
- ⇒ **통신 데이터 크기 ∝ 채널 수**, **통신 빈도 ∝ 층 수**. 논문의 20모델 스캔이 정확히 이 두 축이다.
- 검증: *"We validated our implementation by ensuring **identical energies and atomic forces across the
  serial and parallel runs**."* ⚠ 이건 **병렬 일관성 검사**지 물리 검증이 아니다.

### 4c. 훈련 데이터 ★★ (우리 UMA 와 갈리는 지점)

| | SevenNet-0 (이 논문) | SiO₂ 벤치마크 20모델 |
|---|---|---|
| 데이터 | **M3GNet 데이터셋** (ref 25 = Chen & Ong, *Nat. Comput. Sci.* 2022, 2, 718). *"includes **three relaxation steps** of crystal structures obtained from the **Materials Project**, covering **89 elements**"* | **자체 생성 DFT MD 스냅샷** |
| 분할 | **90 / 5 / 5** (train/val/test), **materials 단위** | **9 : 1** (train/val), 무작위 셔플 |
| 규모 | 명시 없음 (**n/a**) | 72 SiO₂ 단위(=216 원자) 궤적에서 **40 fs 마다 샘플 → 1,600 구조** |
| 성격 | **결정만.** 저자 명시: *"SevenNet-0 is **exclusively trained on crystal structures**, including polymorphs of Si₃N₄. **Disordered phases like liquid or amorphous are not present in the training set.**"* | **melt–quench–annealing 과정 + 300 K α-quartz 진동** = 고온·비평형 포함 |
| DFT | 명시 없음 (M3GNet 데이터셋 승계 · **n/a**) | **VASP**, **PBE**, 스냅샷 재계산 **450 eV**, **Γ 점만** |

**★ MPtrj·OMat24·sAlex 는 이 논문에 **전혀 안 나온다.** SevenNet-0 = **M3GNet 데이터셋** 하나다.
⇒ 우리 UMA(OMat24)와 **훈련셋이 다르다** — T1b 대조에서 **교란변수 1개 증가** (→ §13).

### 4d. 학습 설정 (§5.1)

- **다중 GPU 학습**, **4×A100**, batch **16**, **Adam**, lr **0.004**, validation loss 가 **50 epoch** 개선
  없으면 lr **×0.5**. 총 **493 epoch**.
- 원자 에너지는 **원소 참조에너지(ref 25)로 shift**, **원자당 에너지 표준편차로 scale**.
- 손실 (eq 9): `Γ = (1/M)Σ L_Huber(Ê_i/N_i, E_i/N_i, δ) + (μ_f/3MΣN_i)ΣΣΣ L_Huber(F̂, F, δ)
  + (μ_s/6M)ΣΣ L_Huber(Ŝ, S, δ)`, **μ_f = 1.0**, **μ_s = 0.01**, **Huber δ = 0.01**.
  Huber 를 쓴 이유: *"to reduce the impact of outliers in the M3GNet data set"* — 절대오차가 δ 를 넘으면
  MSE 에서 MAE 로 넘어간다.
  > ⚠ **이 δ 선택 자체가 T1b 와 얽힌다** — Huber 는 **큰 오차의 기울기를 잘라낸다.**
  > 고에너지·비평형 구조가 outlier 로 들어오면 그 항의 학습 압력이 **의도적으로 약해진다**.
  > ⛔ 단 **논문은 이 연결을 말하지 않는다** — 우리 관찰이다.

### 4e. MD 설정

| | SiO₂ 벤치마크 | Si₃N₄ 실증 |
|---|---|---|
| 엔진 | **LAMMPS 23Jun2022-Update4**, CUDA-aware **OpenMPI 4.1.2**, LibTorch(PyTorch **1.12.0**), nvcc **CUDA 11.6.2**, gcc **9.4.0** | 동일 계열 |
| 앙상블 | **NVT, 300 K, Nosé–Hoover** | 초가열·급랭 (아래) |
| **Δt** | **명시 없음 (n/a)** ⚠ | **명시 없음 (n/a)** ⚠ |
| 부하 분산 | **`fix balance` 10 MD 스텝마다** 동적 재분할 | 동일 |
| 측정 | 210 스텝 실행, **마지막 100 스텝의 벽시계** | — |
| 하드웨어 | **HPE Apollo 6500 Gen10**, 노드당 **8× A100 80GB + NVLink**, 노드간 **InfiniBand HDR200**, GPU 1장당 CPU **1코어** = MPI rank 1 | 8× A100 80GB |

**Si₃N₄ melt–quench 프로토콜** (§5.2) — 우리 비정질/계면 작업에 그대로 이식 가능:
1. **112 원자**를 밀도 **3.10 g/cm³** 큐빅 셀에 무작위 배치 → **5000 K 5 ps 초가열**
2. 그 셀을 **10×10×10 복제** → **112,000 원자** (한 변 **10.6 nm**)
3. **5000 K 10 ps** 초가열 → **3000 K 20 ps** 평형 → **2000 K 까지 −33 K/ps 급랭**
4. 2000 K 에서 원자 운동이 무시할 만하다고 보고 **0 K 좌표 최적화** → 최종 비정질 구조
- 총 MD ≈ 60 ps, 12.7 h, 8 GPU.
- ⚠ **2000 K 에서 멈춘 뒤 0 K 최적화**로 건너뛴다 — 2000 K→300 K 구간을 MD 로 지나가지 않는다.
  저자 근거: *"atomic motions are negligible at 2000 K"*. ⛔ 이건 **주장이지 측정이 아니다**(→ §10).

### 4f. 무질서 처리
**해당 없음** — SQS·enumerate·점유 decorate 가 필요한 계가 없다. 무질서는 **melt–quench MD 로 생성**한다.
(우리 argyrodite 4a/4c 무질서 문제와는 성격이 다르다.)

---

## 5. Figure set ★ — **8장 전부 크로핑 후 실제로 봤다**

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a | 메시지패싱 1스텝 도해 — 노드 feature `h_v^(t)` 가 이웃에서 모은 메시지로 `h_v^(t+1)` 로 갱신 | GNN 이 "왜 컷오프보다 멀리 본다"는지의 그림 원본 |
| 1b | **수용영역 확장** — t=1(주황) → t=2(파랑) → t=3(초록), 점선원이 층마다 한 겹씩 커진다 | **`유효 반경 = T × r_c`** 의 시각 정본. SevenNet-0 은 5×5 Å = **25 Å**. 우리 슬랩 두께 설계의 하한 근거 |
| 2a | 단순화한 NequIP 흐름 — Embedding → Interaction block ×3 → Output block → E. 파랑=forward, 주황=reverse(힘) | **첫 블록만 회색 = 통신 없음.** 통신을 어디에 끼우는지가 한눈에 |
| 2b | Interaction block 내부 — `⊗`(self-connection) → Self-interaction → **Forward comm.** → Convolution → Self-interaction → `⊕` → Non-linearity, 그리고 **Reverse comm.** 대칭 | 저자가 손댄 자리가 **왼쪽 `⊗`** 다. 그 자리에 원소별 파라미터가 몰려 있었고 선형층으로 교체 → 19배 축소 |
| 3a–f | 공간분할 워크플로 전체 — (a) 스텝 흐름, (b) 셀, (c) r·Z forward, (d) h forward, (e) ∇_hE reverse, (f) F reverse. ghost atom 은 점선원 | **통신 스케줄 정본.** forward h ×(T−1), reverse ∇_hE ×(T−1), reverse F ×1 |
| 4a–d | **약스케일링(weak)** 병렬효율 vs GPU 수(1→32), 4패널 = 2/3/4/5층, 각 5곡선 = 4/8/16/32/64 채널. y 0.6–1.0, 점선 = ideal 1.0 | 32 GPU 에서 `figure-read ≈` 2층 **0.67–0.83** · 5층 **0.79–0.84**. **8→16 GPU 에서 꺾인다**(노드당 8 GPU → 노드간 통신 시작). ⚠ 32 GPU 에서 **64채널이 오히려 최저**인 패널이 둘(b: 0.738 / d: 0.81) = 본문 서술과 어긋남 |
| 5a–d | **강스케일링(strong)** speed-up vs GPU 수, 12,960 원자 고정. y 로그축 1–32, 점선 = ideal | 32 GPU 32채널 `figure-read ≈` **2층 9.6 · 3층 14.1 · 4층 15.3 · 5층 15.3**. ⚠ 본문의 "13.1–15.4" 중 **13.1 은 64채널·2층 점**이다(→ §10). 4채널·2층은 **4 GPU 에서 포화** |
| 6a | 비정질 Si₃N₄ 112,000 원자, 한 변 **10.6 nm** (Si 노랑 / N 파랑) | 등변 GNN 으로 **10 nm 급 비정질**이 실제로 만들어진다는 실물 |
| 6b | **g(r)** Si–N(초록)/Si–Si(파랑)/N–N(빨강), 0–6 Å. 실선 = SevenNet-0, 빈 원 = DFT 참조(ref 52) | Si–N 첫 피크 **≈1.75 Å**. ⚠ **피크 높이가 다르다**: 실선 `figure-read ≈`**11.2** vs 원 ≈**8.7** — MLIP 쪽이 **더 뾰족**(over-structuring). 위치는 일치 |
| 6c | **g(θ)** Si–N–Si(파랑)/N–Si–N(빨강), 60–180° | N–Si–N 주피크 ≈109°(실선 ≈185 vs 원 ≈205 — MLIP 이 **낮다**), Si–N–Si ≈118°(실선 ≈155 vs 원 ≈128 — MLIP 이 **높다**). **90° 어깨**(square-planar) 는 양쪽 다 재현 |
| S1 | **단일 GPU 이용률** — x=원자 수(288–15,500), y=**원자수×steps/s**, 4층 모델의 채널별 곡선. 위쪽 축에 fixed-size test 의 GPU별 원자 수 표시 | **채널이 적을수록 포화에 더 많은 원자가 필요하고, 절대 처리량은 더 높다.** `figure-read ≈` 포화값 4ch **35k** · 8ch **19.5k** · 16ch **10k** · 32ch **5.3k** · 64ch **3.5k** atom·steps/s. 64ch 곡선은 **≈9,000 원자에서 끊긴다**(메모리) |
| S2 | **SevenNet-0 vs MACE-MP-0** 약스케일링, x=원자 수 500–4000, y=M-timesteps/day | SevenNet-0(448 원자/GPU) `figure-read ≈` **1.54 → 1.21**(1→8 GPU, 효율 **0.79**). MACE 단일GPU 는 1/N 로 떨어지고, MACE 다중GPU 는 **0.10 평탄** → **≈3,500–4,000 원자 넘어야** 다중GPU 가 이득. ⚠ 계·출처가 다른 비교 |

**⚠ 본 그림 vs 안 본 그림**: **8/8 전부 크로핑해서 봤다.** 표는 이 논문에 **없다**(`Table` 0개).

---

## 6. Post-processing ★

| 무엇 | 어떻게 | 도구 |
|---|---|---|
| **부분 동경분포함수 g(r)** | Si–N / Si–Si / N–N, 0–6 Å. **단일 112,000-원자 구조**에서 계산 | 명시 없음 (**n/a**) |
| **각분포함수 g(θ)** | Si–N–Si / N–Si–N. 90° 어깨 = square-planar 지표 | 명시 없음 (**n/a**) |
| **배위수** | Si **4-fold**, N **3-fold** 유지 확인 | 명시 없음 (**n/a**) |
| **병렬효율** | weak: `t(1)/t(n)` · strong: speed-up `t(1)/t(n)` | LAMMPS 벽시계 (마지막 100/210 스텝) |
| **GPU 이용률** | `원자수 × steps/s` 를 원자 수에 대해 → **평탄역 = full utilization**, 저원자 구간 = *"ballistic region"* | `Fig. S1` |
| **정확도** | E/F/S **MAE** (test set) | — |
| ⛔ **없는 것** | NEB · Bader · COHP · DOS · ELF · 포논 · 탄성 · **에너지 보존/드리프트** · **MLIP↔DFT 고온 스냅샷 재평가** | — |

**DFT 참조의 출처**: 비정질 Si₃N₄ 의 g(r)·g(θ) 원 데이터는 **ref 52** (Kang, Lee, Lee, Kim, Han,
*Phys. Rev. Appl.* **10**, 064052, 2018 — **같은 그룹**)에서 가져왔고, **112 원자짜리 40개 구조의 평균**이다.
⇒ **비교의 양쪽이 다르다**: 112,000-원자 **단일** 구조 vs 112-원자 **40개 앙상블 평균** (→ §10).

---

## 7. 우리 대비 (`our_dft_baseline.md` · UMA 설정)

**⛔ 물성 4축 비교가 불가능하다** — 이 논문에 σ·Ea·ESW·탄성·gap 이 0건. 대신 **엔진 축**으로 비교한다.

| 항목 | **[Park24] SevenNet-0** | **우리 UMA-s-1p1 (omat)** | 판정 |
|---|---|---|---|
| 계열 | **등변 GNN** (NequIP 기반) | **등변 GNN** (eSEN 기반, MoLE) | ✅ **같은 계열** — T1b 대조가 성립하는 이유 |
| **cutoff r_c** | **5 Å** | **6 Å** | ⚠ 우리가 조금 넓다 |
| **층 수 T** | **5** | **n/a** (우리 UMA digest 에 층 수 기록 없음) | 🔴 **대조 불가** — 확인 필요 |
| 유효 수용영역 | **25 Å** (= 5 × 5 Å) | **> 6 Å** 이나 정확한 값 미상 | 🔴 우리 쪽 미확정 |
| **l_max** | **2** (128 scalar / 64 vector / 32 tensor) | 구면조화 기반 eSCN — 차수 미기록 | 🔴 미확정 |
| 파라미터 | **0.84 M** | **150 M total / 6 M active** (UMA-S) | 🔴 **자릿수가 다르다** — 비용·표현력 비교 금지 |
| **훈련셋** | **M3GNet 데이터셋** = MP **결정 이완 3스텝**, 89원소. **액체·비정질 없음(저자 명시)** | **OMat24** 1.008억 구조·89원소·평균 19원자, **AIMD·Rattled 부분집합 포함** | 🔴🔴 **다르다. 그리고 비평형 방향으로 우리가 더 넓다** ← T1b 의 핵심 |
| 참조 DFT | **n/a** (M3GNet 데이터셋 승계). SiO₂ 훈련셋만 VASP/PBE/450 eV/Γ | VASP/PAW **PBE** (OMat24 설정) | ⚠ 둘 다 PBE 계열로 보이나 **SevenNet-0 쪽은 논문에 명시 없음** |
| **F MAE (평형 근처)** | **0.070 eV/Å** (MP 결정 test set) | **n/a** — 우리는 held-out 힘 MAE 를 **안 재 봤다** | 🔴 **우리 쪽 공백** (T1 이 필요한 이유) |
| E MAE | **25 meV/atom** | **n/a** | 🔴 우리 공백 |
| MD 엔진 | **LAMMPS** pair style (다중 GPU) | **ASE** Langevin NVT (단일 GPU) | 🔴 **우리는 다중 GPU 경로가 없다** (→ §14) |
| 앙상블/열욕 | Nosé–Hoover NVT | **Langevin NVT** (friction 0.02) | ⚠ 열욕이 다르다 — 확산계수 비교 시 주의 |
| Δt | **n/a** | **2 fs** (우리 규약) | — |
| 정밀도 | **single** | n/a | ⚠ single 정밀도는 장시간 드리프트에 불리 |
| **에너지 보존 검증** | ⛔ **없음** | ⛔ **없음** | 🔴 **둘 다 공백** — 우리만의 흠이 아니다 |

**⚠ 방법 의존성 경고**: 위 표에서 **"우리가 더 넓다/좁다" 로 성능을 추론하면 안 된다.**
훈련셋 크기·아키텍처·손실함수·정밀도가 전부 다르고, 두 모델을 **같은 계에서 같은 지표로 잰 적이 한 번도 없다.**
지금 말할 수 있는 최대치는 **"같은 계열이고, 훈련셋의 비평형 포함 범위가 다르다"** 까지다.

---

## 8. 적용 인사이트

① **T3 비용 산정이 처음으로 숫자가 됐다** (→ §14). 등변 GNN 5층 기준 **1.58×10⁶ atom·ps/day per A100**.
   우리 T3-small(7,000원자 × 20 ns) ≈ **89 A100-day**. 이걸 알면 **T3 를 어떤 자원에 올릴지**가 결정된다.

② **수용영역 = T × r_c 를 슬랩 설계에 넣어야 한다.** 5층·5 Å 모델은 **25 Å 를 본다**.
   우리가 슬랩을 5 nm 이하로 자르면 **모든 원자가 양쪽 표면을 동시에 느낀다.**
   ⛔ 단 우리 UMA 의 T 를 아직 모른다 — **먼저 확인할 것**(§7 의 🔴 3줄).

③ **melt–quench 프로토콜을 그대로 베낄 수 있다** (§4e): 소형 셀 초가열 → 복제 → 재초가열 →
   평형 → 정률 급랭 → 0 K 최적화. 우리 비정질 SEI·b2o3 유리상 작업의 표준 레시피가 된다.

④ **GPU 이용률 규칙**(`Fig. S1`, `Fig. S2`): **원자/GPU 가 적으면 GPU 를 늘려도 손해다.**
   448 원자/GPU 에서 8-GPU 효율 **0.79**, 14,000 원자/GPU 에서 **0.98**.
   ⇒ 우리 T3-small(7,000원자)은 **A100 1장에 통째로 올리는 게 맞다**(원자/GPU 최대화).

⑤ **정확도 눈금이 하나 늘었다**: 같은 GNN 계열의 **base 모델이 평형 근처에서 F MAE 0.070 eV/Å**.
   덱 슬 14 의 MTP 벌크 LPSCl **0.073 eV/Å** 과 **같은 자릿수**다 (→ §13 의 talk 정정).

⑥ **오픈소스 경로**: MIT 라이선스 · LAMMPS 다중 GPU · fine-tuning 인터페이스.
   우리가 UMA 로 못 하는 것(다중 GPU MD, fine-tune)을 **할 수 있는 대안 엔진**이 이것이다.

### 🔍 **확보 실패 — 안 본 것** (정직하게 기록)
- **figshare `benchmark_sevennet.gz` (10.6084/m9.figshare.25573938.v2)** — 프록시가 `figshare.com` ·
  `api.figshare.com` 을 **403 으로 차단**. **원시 타이밍 데이터 미확보.**
  ⇒ `Fig. 4`·`Fig. 5`·`Fig. S1` 의 값은 **전부 figure-read** 이고, 저자 원본 수치는 우리에게 없다.
- **`mdil-snu.github.io` 문서 사이트도 차단** — 체크포인트별(`SevenNet-0__22May2024` /
  `__11Jul2024` / `MF-0` / `l3i5`) **정확도 표 미확보**.
- ⚠ **repo 는 이 논문 이후로 많이 나아갔다** (multi-fidelity 학습 · 망각방지 fine-tune(experience
  replay + EWC) · CUDA D3 분산 · 후속 모델 SevenNet-MF-ompa / Omni / Nano).
  **repo 기능을 이 논문 결과로 적으면 안 된다** — 이 digest 의 모든 수치는 **2024 논문 본문 + SI** 한정.

---

## 9. 인용 가능 문장

- "메시지패싱 GNN 포텐셜의 유효 수용영역은 컷오프 반경 × 메시지패싱 층 수까지 넓어지며,
  이것이 공간분할 병렬화를 어렵게 만든다 [Park 2024, JCTC 20, 4857]."
- "SevenNet 은 통신 반경을 원래 컷오프로 유지한 채 층마다 forward/reverse 통신을 반복하는 방식으로,
  32-GPU 약스케일링에서 80 % 이상의 병렬효율을 얻었다 (4,608 원자/GPU) [Park 2024]."
- "강스케일링 이득은 GPU 당 원자 수가 충분할 때만 얻어지며, 12,960 원자를 32 GPU 로 나누면
  이상적 32배 대비 절반 수준(최대 15배)에 그친다 [Park 2024]."
- "결정 구조만으로 학습한 범용 GNN 포텐셜(SevenNet-0)이 5000 K 초가열–급랭을 거쳐 만든
  비정질 Si₃N₄ 의 배위수·g(r)·g(θ) 를 DFT 참조와 부합하게 재현했다 [Park 2024]."
- "SevenNet-0 의 시험셋 정확도는 에너지 25 meV/atom, 힘 0.070 eV/Å, 응력 0.68 GPa 이다 [Park 2024]."

**⛔ 이 논문에서 인용하면 안 되는 것**
1. **"SevenNet 이 MACE 보다 빠르다"** — `Fig. S2` 는 **다른 계**(SevenNet=비정질 Si₃N₄ 448원자/GPU vs
   MACE=고엔트로피 합금 500원자/GPU)에 **다른 출처**(MACE 는 ref 32 문헌값)를 겹쳐 그린 그림이다.
   같은 하드웨어·같은 계에서 잰 것이 아니다.
2. **"SevenNet 이 NequIP 보다 2배 빠르다"를 일반화** — SI 의 조건은 32채널·4층·l_max 3·r_c 4.0 Å·
   4,608원자·SiO₂ 단일 A100 이고, **LAMMPS 버전마저 다르다**(23Jun2022-U4 vs 29Sep2021-U2).
3. **"SevenNet-0 이 M3GNet 보다 정확하다"를 통째로** — **응력은 1.7배 나쁘다**(0.68 vs 0.41 GPa).
4. **"GNN 이 비평형에서 잘 작동함이 검증됐다"** — 검증된 것은 **구조 지표 하나**(g(r)·g(θ)·배위수)이고,
   **에너지·힘·안정성은 고온 영역에서 한 번도 재지 않았다.**
5. **80 % 병렬효율을 무조건적으로** — **4,608 원자/GPU 조건**이다. 448 원자/GPU 에서는 **0.79**로 떨어진다.

---

## 10. 주의 / 한계 — 비판적으로

### 10-1. 🔴 **본문 수치와 그림이 어긋나는 곳이 하나 있다** (우리가 픽셀 실측)

본문 §4.2: *"a model configured with **32 channels** and between 2 and 5 message-passing layers registers
performance gains ranging from **13.1 to 15.4** when using 32 GPUs."*

`Fig. 5` 를 축 눈금 픽셀 보정(선형 y축, 1–32)해서 32 GPU 지점의 **32채널 ◆ 마커**를 읽으면:

| 층 수 | 32채널 ◆ (우리 실측) | 본문 범위 |
|---|---|---|
| 2 (`Fig. 5a`) | **≈9.6** | (13.1 이어야) |
| 3 (`Fig. 5b`) | ≈14.1 | ✅ 범위 안 |
| 4 (`Fig. 5c`) | ≈15.3 | ✅ |
| 5 (`Fig. 5d`) | ≈15.3 | ✅ (본문 15.4) |

- **13.1 은 `Fig. 5a` 의 최상단 마커 = ▼ 64채널** 값과 정확히 일치한다(우리 실측 **13.11**).
  마커 모양을 확대해 **▼(64ch) 가 위, ◆(32ch) 가 아래**임을 확인했다.
- 보정 신뢰도: 같은 보정으로 본문의 **15.4** 를 **15.29** 로 재현(오차 0.7 %) → **9.6 이 13.1 일 수 없다.**
- **결론**: 본문의 하한 13.1 은 **32채널이 아니라 64채널 곡선**을 읽은 것으로 보인다.
  ⇒ **2층·32채널의 실제 강스케일링은 32 GPU 에서 9.6× (이상의 30 %)** 로, 본문 인상보다 나쁘다.
  ⚠ 논문의 결론(*"halved speedup even for the best-performed model"*)은 **그대로 유효**하다.

### 10-2. `Fig. 4` 의 채널 추세가 32 GPU 에서 뒤집힌다
본문: *"we observe a slight increase in parallel efficiency with the addition of more channels or
message-passing layers."* 그런데 32 GPU 지점에서:
- `Fig. 4b`(3층): **64채널이 최저 (≈0.738)**, 16채널이 최고(≈0.83)
- `Fig. 4d`(5층): **64채널이 최저 (≈0.81)**
- `Fig. 4a`(2층): 64채널(≈0.81)이 32채널(≈0.825)에 **역전당함**
⇒ "채널이 많을수록 효율이 좋다"는 **8 GPU 까지의 추세**이고, **최대 GPU 수에서는 깨진다.** 본문 미언급.

### 10-3. `Fig. 6` 의 "agree well" 은 **위치**에 대한 말이지 **진폭**에 대한 말이 아니다
- Si–N 첫 피크: SevenNet `figure-read ≈`**11.2** vs DFT ≈**8.7** → **MLIP 이 ~29 % 더 뾰족**.
- N–Si–N g(θ) 주피크: MLIP ≈185 vs DFT ≈205 (**MLIP 이 낮다**);
  Si–N–Si: MLIP ≈155 vs DFT ≈128 (**MLIP 이 높다**) — **방향이 반대**라 단순한 스케일 차이가 아니다.
- ⚠ **다만 비교의 양쪽이 다르다**: 112,000원자 **단일** 구조 vs 112원자 **40개 평균**(ref 52).
  앙상블 평균은 피크를 넓히고 낮추므로 **Si–N 진폭 차의 상당 부분은 통계 탓일 수 있다.**
  ⇒ **이것으로 "MLIP 이 과경직/과연화" 를 판정하면 안 된다.** 오차막대·시드가 **양쪽 다 없다.**

### 10-4. 검증축이 **구조 하나**다 (T1b 에 직결)
- **에너지 보존·드리프트 검사 없음**(NVE 실행 자체가 없다 — 전부 NVT).
- **고온 스냅샷을 DFT 로 재평가하지 않았다** — 5000 K·3000 K 구조에서 MLIP 이 얼마나 틀렸는지 **모른다**.
- **포논·탄성·융점·장벽 없음.**
- `2000 K 에서 0 K 로 건너뛴` 근거(*"atomic motions are negligible at 2000 K"*)는 **주장이고 측정이 아니다**.
  Si₃N₄ 융점이 ~2170 K 급인 것을 생각하면 2000 K 는 **아직 상당히 뜨겁다.**
- **한 개 조성·한 개 시드**. 비정질 구조 1개로 g(r)/g(θ) 를 뽑았다.

### 10-5. 아키텍처 개선의 근거 수치가 없다
*"a reduction in validation error and an increase in training error"* — **얼마나?** 값도 곡선도 없다.
19배 파라미터 축소가 **정확도에 얼마를 대가로 냈는지** 이 논문으로는 알 수 없다.
(GNoME 16.24 M 모델과 같은 test set 에서 직접 비교한 표가 없다.)

### 10-6. SiO₂ 20모델의 정확도가 **전혀 없다**
타이밍만 재고 MAE 를 안 보고했다. ⇒ *"채널·층을 늘리면 효율이 좋아진다"* 는 결론은
**정확도를 통제하지 않은 상태**에서의 말이다. 실무에서는 "같은 정확도를 어느 설정이 더 싸게 내나"가
질문인데, 이 논문은 그 질문에 답하지 않는다.

### 10-7. Δt 가 명시되지 않았다
SiO₂ 벤치마크에도, Si₃N₄ melt–quench 에도 **시간 간격이 없다.** 그래서 `timesteps/s` ↔ `ps/day` 환산에
가정이 들어간다. **우리는 dt-무관 지표(atom·ps/day)로만 인용한다** (§14).

### 10-8. ★★ **우리 계로의 이식 한계 — 벤치마크가 무엇이고 황화물과 무엇이 다른가**

| 축 | 이 논문 벤치마크 (SiO₂ · Si₃N₄) | 우리 계 (Li₆PS₅Cl 계열) | 왜 문제인가 |
|---|---|---|---|
| **결합 성격** | **공유결합 네트워크**. Si–N/Si–O 는 방향성이 강하고 배위수가 고정 | **이온성 골격 + 초이온 Li 부격자**. Li 는 사이트 사이를 뛴다 | 공유 네트워크에서 "붕괴"는 **배위수 이상**으로 즉시 보인다. 이온성 골격의 **creep** 은 배위수로 안 보인다 — 우리 b2o3 판정 지표(log-log MSD 기울기 **β ≥ 0.60**)가 이 논문에 **없다** |
| **관측량** | 정적 구조(g(r)·g(θ)·배위수) | **동역학**(D, Ea, 골격 β) | 구조가 맞아도 동역학이 틀릴 수 있다. 이 논문은 **D 를 한 번도 재지 않았다** |
| **장거리 정전기** | SiO₂·Si₃N₄ — 부분전하는 있으나 이동 이온 없음 | **Li⁺ 이동 + S²⁻/Cl⁻ 분극** | r_c 5 Å 단거리 모델(명시적 Ewald 없음)이 이온 수송을 얼마나 잡는지 **이 논문은 답하지 않는다** |
| **혼합 음이온·무질서** | 2원소 계, 무질서는 melt 로 생성 | **S/Cl 4a·4c 자리무질서**가 물성을 지배 | 자리무질서 앙상블 문제는 이 논문에 **없다** |
| **목표 시간창** | **60 ps** (melt–quench) | **20–50 ns** (계면 SEI) | **2–3 자릿수 차이.** 이 논문이 "장시간 안정성"을 못 말하는 이유이기도 하다 |
| **온도** | 5000 / 3000 / 2000 / 300 K | **600–1000 K**(우리 아레니우스) · **350 K**(계면) | 겹치는 구간이 거의 없다 |

⇒ **한 줄**: 이 논문은 **"등변 GNN 을 대형·병렬로 굴리는 법"** 의 정본이지,
**"등변 GNN 이 이온성 황화물의 동역학을 옳게 준다"** 의 근거가 아니다. 후자는 **여전히 우리 T1/T1b 몫**이다.

---

## 11. 절 단위 정독 — 논문이 실제로 하는 말

### §1 서론 — 문제 정의
- MD 의 힘 계산: DFT 는 `O(N³)`. MLIP 은 컷오프 `r_c` 로 국소성을 가정해 `O(N)`.
- GNN-IP 는 손으로 만든 descriptor(거리·각·이면각) 없이 원자 그래프에서 특징을 **학습**한다.
  메시지패싱으로 **`r_c` 너머의 다체 상호작용·중거리 질서**를 담는다.
- GNN-IP 는 노드 feature 의 수학적 성질로 두 갈래: **불변(invariant)** vs **등변(equivariant)**.
  NequIP 은 구면조화 표현을 쓰고 회전 시 **Wigner D-행렬**로 선형변환된다 → 데이터 효율·정확도.
- **문제**: 공간분할 병렬화. 엄격히 국소인 MLIP 은 경계에서 `r_c` 만 주고받으면 되는데,
  GNN-IP 는 **`r_c` × 층 수**까지 필요하다. 통신 반경을 그대로 키우면 **이웃 프로세서 간 공통
  부분그래프가 커져 중복 계산이 폭증**한다.
- **선행**: MACE 를 원래 공간분할로 병렬화해 **32,000원자 고엔트로피 합금을 64 GPU** 로 돌린 사례(ref 28).
  그러나 *"employing multiple GPUs incurred significant additional costs, becoming favorable only for
  very large systems."* ← 이 논문이 이기려는 지점.

### §2 GNN-IP 일반형
- 임베딩층이 원자번호로 `h^(1)` 초기화. `r_c` 안의 두 원자를 엣지로 잇고, 변위벡터를 엣지 feature `e_vw` 로.
- `E = Σ_i E_i` (eq 1), `F_i = −∇_i E` (eq 2).
  **에너지를 원자별 합으로 쓰는 것이 선형 확장성의 열쇠**이고, **공간분할이 성립하는 전제**다.
- 메시지패싱 (eq 3, 4): `m_v^(t+1) = Σ_{w∈N(v)} M_t(h_v, h_w, e_vw)`, `h_v^(t+1) = U_t(h_v, m_v)`.
- §2.2: NequIP 을 토대로 삼은 이유 = *"demonstrated to be both data-efficient and accurate."*

### §3 병렬화 — 이 논문의 본체
- §3.1 공간분할: 셀을 부분영역으로 나눠 프로세서에 배정. 경계 밖 원자는 **ghost atom** 으로 복제.
- forward: `r, Z` → 부분영역 그래프 구성 → 첫 메시지패싱(통신 불필요) → 이후 `h` 를 **(T−1)회** 교환.
- reverse: eq 5–8 의 연쇄율을 따라 `∇_h E` 를 **(T−1)회**, 마지막에 부분 힘 `F` 를 1회 교환.
- §3.2 구현: PyTorch + e3nn + **TorchScript**. **층 1개 = TorchScript 파일 1개**로 재구성해
  LAMMPS 통신 루틴을 사이에 끼웠다. LAMMPS 통신 루틴은 *"proven their robustness across a broad
  spectrum of large-scale simulations"* → **확장성 한계를 따로 걱정하지 않는다**는 논리.
- 단일 GPU 속도: **SevenNet 1.99 vs NequIP 1.12 timesteps/s** (≈1.8×) — 마지막 interaction block 의
  중복 텐서곱 경로 제거 덕.
- ASE 도 지원, fine-tuning 인터페이스 제공.

### §4 벤치마크
- 축 2개: **채널 수**(통신 **데이터 크기**) × **층 수**(통신 **빈도**) → 5×4 = **20 모델**.
  공통: **l_max = 3**, **r_c = 4.0 Å**. (⚠ SevenNet-0 의 l_max 2 / r_c 5 Å 와 **다르다**)
- §4.1 약스케일링: **4,608 원자/GPU 고정**, 32 GPU = **147,456 원자**.
  - 층이 적을수록(통신 빈도 낮음) 오히려 효율이 **나쁘다** → 저자 설명: 층·채널이 늘면
    **직렬 계산시간 `t(1)` 과 병렬 계산시간 `t(n)` 이 같이 커져 통신비용의 상대적 비중이 준다**.
  - **8 → 16 GPU 에서 급락** — 노드당 8 GPU 이므로 **여기서 노드간 통신이 시작**된다.
    16 → 32 에서는 더 나빠지지 않는다 ⇒ *"the impact of internode communication does not worsen"*.
  - 단서: *"these benchmarks were conducted on a **homogeneous SiO₂ bulk** system, which facilitates a
    uniform distribution of atoms across subdomains."* **불균질계·GPU 수 증가 시 동기화 비용이 커질 수 있다.**
- §4.2 강스케일링: **12,960 원자 고정**(A100 80GB 메모리를 32채널·4층에서 거의 채우는 수).
  - **64채널 × 3–5층 조합은 단일 GPU 측정 불가**(메모리) → `Fig. 5b–d` 에서 빠져 있다.
  - 포화 원인은 **GPU 이용률**: GPU 당 원자가 줄면 일을 나눠도 계산시간이 안 준다 (`Fig. S1`).
  - Allegro(ref 34)의 강스케일링 벤치마크에서도 같은 관찰.

### §5 범용 모델
- §5.1 SevenNet-0 학습 (→ §4c·§4d).
- §5.2 대형 melt–quench (→ §4e).
  - 대상 선정 이유: **비정질 Si₃N₄ 는 플래시 메모리의 charge-trap 층**(ref 56, 57).
  - 통상은 **작은 비정질 모델 여러 개를 평균**내는데(ref 52–54), 저자는 *"conducting large-scale
    amorphous simulations is crucial to study systems in actual devices"* 라고 주장.
  - 결과: **Si 4배위 · N 3배위 유지**, g(r)·g(θ) 가 DFT 참조와 부합, **90° 어깨(square-planar) 재현**.
  - ★ 저자 자신의 총평(그대로): *"SevenNet-0 is exclusively trained on crystal structures … Disordered
    phases like liquid or amorphous are not present in the training set. However, SevenNet-0 reproduces
    key structural features of amorphous Si₃N₄ … This demonstrates the **generalization capability** …
    Such **emergent capability** is a result of training on a large data set with diverse chemistry."*
  - **메모리 한계 명시**: *"it is not feasible to run a simulation with 112,000 atoms on a single A100 GPU.
    Consequently, employing multi-GPU MD simulations is indispensable for large-scale simulations."*

### §6 논의 — 일반성과 한계
- 이 병렬화는 **두체(two-body) 메시지 함수**를 쓰는 모든 GNN-IP 에 적용된다:
  **SchNet · PhysNet · PaiNN · NequIP · MACE**. (SchNet·PhysNet 을 뺀 나머지는 전부 **등변**.)
- **DimeNet · ALIGNN · CHGNet · M3GNet** 은 eq 3 의 두체 형태에서 벗어난다(각·삼중항 feature, 보조 line graph).
  그래도 **컷오프로 국소성이 보장**되므로 엣지 feature·기울기를 forward/reverse 통신에 넣으면 같은 방식으로
  병렬화 가능하다고 본다.
- **미래 과제로 명시**: *"The parallel efficiency in **more heterogeneous systems such as surfaces and
  interfaces** will be assessed in future studies."* ← **우리 T3 가 정확히 그 미검증 영역이다.**

### §7 결론
- 통신을 추가한 공간분할로 NequIP 계열을 병렬화. 약스케일링은 층·채널에 **무관하게** 잘 되고,
  강스케일링은 **GPU 이용률 부족**으로 제한된다. SevenNet-0 공개 + 대형 비정질 실증.

---

## 12. 기술 용어 미니사전 (이 논문을 읽는 데 필요한 만큼)

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **메시지패싱(message passing)** | 그래프의 각 노드가 이웃에서 정보를 모아 자기 상태를 갱신하는 것을 여러 번 반복 | eq 3–4. `T` 번 반복하면 `T` 홉 떨어진 원자 정보까지 들어온다 |
| **수용영역(receptive field)** | 한 원자의 에너지가 실제로 의존하는 공간 범위 | **`T × r_c`**. `Fig. 1b` 가 이걸 그린다 |
| **등변(equivariant) vs 불변(invariant)** | 회전시켰을 때 feature 가 **같이 회전**하면 등변, **안 변하면** 불변 | NequIP·SevenNet·UMA·MACE = **등변**. SchNet = 불변 |
| **구면조화 / l_max** | 방향 정보를 각운동량 차수 `l` 로 전개. `l=0` 스칼라, `l=1` 벡터, `l=2` 텐서 | SevenNet-0: 128 scalar / 64 vector / 32 tensor ⇒ **l_max = 2** |
| **채널(channel)** | 각 `l` 마다 몇 개의 독립 feature 를 둘지 | 통신 **데이터 크기**를 직접 결정 |
| **텐서곱(tensor product)** | 두 등변 feature 를 합쳐 새 등변 feature 를 만드는 연산(Clebsch–Gordan) | 등변 GNN 비용의 대부분. SevenNet 은 **중복 경로를 잘라** 가속 |
| **e3nn** | E(3) 등변 연산 라이브러리 | 등변성을 코드 수준에서 보장 |
| **TorchScript** | PyTorch 의 JIT 컴파일러. 파이썬 없이 C++ 에서 모델 실행 | LAMMPS(C++) 안에서 신경망을 돌리는 통로 |
| **공간분할(spatial decomposition)** | 셀을 공간적으로 쪼개 프로세서에 나눠 주는 병렬화. LAMMPS 의 기본 | 이 논문의 무대 |
| **ghost atom** | 이웃 프로세서 소유지만 내 계산에 필요해서 복제해 온 원자 | `Fig. 3c` 의 점선원 |
| **약스케일링(weak/scaled-size)** | **GPU 당 일을 고정**하고 GPU 를 늘림. 효율 = `t(1)/t(n)` | 큰 계를 다룰 수 있느냐 |
| **강스케일링(strong/fixed-size)** | **전체 일을 고정**하고 GPU 를 늘림. speed-up = `t(1)/t(n)` | 같은 계를 더 빨리 돌릴 수 있느냐 |
| **Huber loss** | 오차가 작으면 MSE, 크면 MAE 로 넘어가는 손실 | `δ = 0.01`. **이상치의 영향을 줄이려고** 씀 |
| **`fix balance`** | LAMMPS 의 동적 부하 재분할 | 10 스텝마다 부분영역 경계 조정 |
| **ballistic region** | GPU 가 덜 채워져 원자를 늘려도 시간이 거의 안 느는 구간 | `Fig. S1` 의 저원자 상승부 |

---

## 13. ★★ T1b 판정 — **이 논문이 말한 것과 말하지 않은 것**

### 13-1. 이 논문이 **말하지 않은 것** (⛔ 이걸 우리가 채워 넣으면 안 된다)

**본문 12 pp + SI 5 pp 전문 텍스트 전수 검색** (pymupdf, 대소문자 무시):

| 검색어 | 본문 | SI | | 검색어 | 본문 | SI |
|---|---:|---:|---|---|---:|---:|
| `soften` | **0** | **0** | | `phonon` | **0** | **0** |
| `energy conservation` / `conserv` | **0** | **0** | | `elastic` | **0** | **0** |
| `drift` | **0** | **0** | | `msd` | **0** | **0** |
| **`NVE`** (단어) | **0** | **0** | | `arrhenius` | **0** | **0** |
| `microcanonical` | **0** | **0** | | `melting point` | **0** | **0** |
| `extrapolat` / `uncertain` | **0** | **0** | | `diffusion` | **1** ← ref 51 제목 안 | **0** |
| `active learn` | **0** | **0** | | `MPtrj` / `OMat` / `sAlex` | **0** | **0** |

⚠ `nve` 부분문자열은 본문에서 9회 잡히는데 전부 **unveil · conventional · investigating · inversion ·
Conversely · convergence** 안이다 — **NVE 앙상블은 한 번도 안 나온다.**

- **PES softening 이라는 말도, 개념도 나오지 않는다.**
- **에너지 보존/드리프트를 재지 않았다.** NVE 실행이 없다(전부 NVT).
- **고온 스냅샷의 MLIP↔DFT 오차를 재지 않았다.** 정확도는 오직 **MP 결정 test set**(평형 근처).
- **fine-tuning 전후 비교가 없다.** 덱 슬 8 의 주장(*"fine-tuning 으로 되돌린다"*)에 대해
  이 논문은 **아무 데이터도 주지 않는다** (fine-tuning **인터페이스가 있다**고만 적는다).
- **동역학 물성(D, Ea)을 재지 않았다.** MSD 도 아레니우스도 없다.
⇒ **"이 논문이 softening 을 반증했다" 는 문장은 쓸 수 없다.**

### 13-2. 이 논문이 **실제로 준 것** — 정황 3개

**① 결정만 학습한 등변 GNN 이 5000 K melt–quench 를 구조적으로 통과했다.**
- 훈련셋에 액체·비정질이 **없다**(저자 명시). 그런데 5000 K → 3000 K → 급랭에서
  Si 4배위·N 3배위가 유지되고 g(r)·g(θ) 가 DFT 참조와 부합했다.
- **방향**: 덱 슬 8 의 기구(*평형 근처 훈련점 편중 → 고에너지 PES 연화*)가 **결정적이라면**,
  훈련셋이 **더 좁은** SevenNet-0 이 먼저 무너졌어야 한다. 안 무너졌다.
- ⚠ **그러나 관측량이 다르다.** 비정질 생성에서 "연화"는 **보이지 않는 종류의 실패**다 —
  목표 상태가 이미 무질서이기 때문이다. 우리 b2o3 판정은 **결정 골격이 안 움직여야 하는데
  움직인다**(β ≥ 0.60)는 것이고, 이건 이 논문의 실험으로 **원리적으로 검출 불가능**하다.

**② 훈련셋의 비평형 포함 범위가 우리 쪽이 더 넓다.**

| | SevenNet-0 | 우리 UMA-s-1p1 (omat) |
|---|---|---|
| 훈련셋 | **M3GNet 데이터셋** — MP 결정 **이완 3스텝**. 액체·비정질 **없음**(저자 명시) | **OMat24** — 1.008억 구조, 89원소, 평균 19원자, **AIMD·Rattled 부분집합 포함** |
| 훈련셋 힘의 세기 | **n/a** (이 논문에 없음) | **Force RMS 2.83 eV/Å** (UMA `Table 11`) — 평형 구조만으로는 안 나오는 값 |
⇒ *"평형 근처 훈련점 편중"* 이라는 진단은 **SevenNet-0 에 더 잘 들어맞는다.**
⛔ **그런데 이것으로 "우리 UMA 는 안전하다" 를 말할 수 없다** — 데이터에 있다는 것과
잘 학습됐다는 것은 다르고, 우리 UMA digest 자체가 **diatomic 스캔에서 1.5–6 Å 구간의 가짜 혹**을
기록해 뒀다(= 2차 배위권 거리). **훈련 범위와 PES 품질은 별개 축이다.**

**③ 정확도 눈금 — 덱 표에 빠져 있던 base 행을 채운다.**

| 출처 | 엔진 | E MAE | **F MAE** | 대상 |
|---|---|---|---|---|
| 덱 슬 14 (citable=no) | MTP (자체학습, 벌크) | 2.88 meV/atom | **0.073 eV/Å** | Li₆PS₅Cl 벌크 |
| 덱 슬 17 (citable=no) | MTP (계면) | Li 11 / LPSCl 5 | 0.083 / **0.111** | Li‖LPSCl 계면 |
| **[Park24] §5.1 (정본)** | **SevenNet-0 (base, GNN)** | **25 meV/atom** | **0.070 eV/Å** | **MP 결정 89원소 test set** |
| 덱 슬 22 (citable=no) | SevenNet (fine-tuned) | 8.8 meV/atom | **0.57 eV/Å** | LPSCl + H₂O 가수분해 |

🔑 **읽는 법**: **평형 근처에서는 GNN(0.070)과 MTP(0.073)가 같은 자릿수다.**
0.57 eV/Å 은 **아키텍처 탓이 아니라 계 탓**일 가능성이 커진다(반응·H₂O·비평형).
⛔ 단 **네 행의 계·훈련셋·측정 프로토콜이 전부 다르다** — 이건 **우열 판정이 아니라 자릿수 감각**이다.
그래도 *"GNN 계열은 원래 힘을 거칠게 본다"* 라는 읽기는 **이 표로는 지지되지 않는다.**

### 13-3. 🔴 **T1b 최종 판정**

> **이 논문으로 T1b 는 닫히지 않는다. 그러나 "GNN 계열이라서 물러진다" 는 읽기는 약해졌다.**
>
> - 판정에 필요한 실험(에너지 보존·고온 재평가·동역학)이 **하나도 없다**.
> - 얻은 것은 **반대 방향의 정황 2개**(더 좁게 학습한 같은 계열 모델이 5000 K 를 통과 ·
>   평형 근처 힘 정확도가 MTP 와 동급)와, **관측량이 다르다는 경고 1개**.
> - ⇒ **T1b 는 여전히 우리가 직접 돌려야 한다**: b2o3 셀을 **vdW 보정 DFT**(optB88-vdW / PBE-D3)로
>   재이완해 S···S 접촉거리·B₀ 를 PBE 값(24.48 GPa)과 비교하는 원래 계획이 **그대로 유효**하다.
> - **추가로 얻은 값싼 검사 하나**: 이 논문이 안 한 것 중 우리가 **하루면 하는 것** —
>   b2o3 700 K 궤적의 스냅샷 몇 개를 **UMA 로 단일점 재평가 vs 우리 DFT** 로 힘 MAE 를 재는 것.
>   합격선 눈금은 §13-2 ③ 표가 준다: **≲0.1 eV/Å 이면 MTP 급, ≳0.5 면 반응계 fine-tune 급**.
>   이건 **T1(외삽 대리지표)의 실행 가능한 최소판**이다.

---

## 14. ★ T3 실현가능성 산정 — **우리 산술** (논문의 주장이 아님)

**출발 수치(전부 논문 본문)**: 112,000 원자 · 60 ps · 12.7 h · 8× A100 80GB
(교차검증: 14,000 원자 · 60 ps · 12.5 h · 1× A100, 병렬효율 0.98)

```
60 ps / 12.7 h            = 113 ps/day
113 ps/day × 112,000 atom = 1.27e7 atom·ps/day  (8 GPU)
                          ÷ 8  = 1.58e6 atom·ps/day  per A100
교차검증: 115 ps/day × 14,000 = 1.61e6 atom·ps/day  (1 GPU) ✓
```

| 대상 | 규모 | 필요량 | **단일 A100** | 8× A100 (효율 가정) |
|---|---|---|---|---|
| **T3-small** (kim2026 소형) | 7,000 원자 × **20 ns** | 1.4×10⁸ atom·ps | **≈89 일** | 875 원자/GPU = **저이용** → 효율 ~0.8 ⇒ **≈14 일** |
| **T3-large** (kim2026 대형) | ⚠ 원자수 미상. 16,000 가정 × **50 ns** | 8×10⁸ atom·ps | ≈506 일 | 2,000 원자/GPU ⇒ **≈70 일** |
| 참고: 논문 자신의 실증 | 112,000 원자 × 0.06 ns | 6.7×10⁶ atom·ps | (메모리 불가) | **12.7 시간** |

**★ 이 표에서 읽어야 할 것 3가지**
1. **T3-small 은 단일 A100 에서 3개월이다.** 우리 gabia(A6000 1장)·kgy(RTX3090)로는 **수개월 이상** —
   ⛔ 현실적으로 불가. **KISTI 다중 GPU 할당이 필요**하다.
2. **그런데 GPU 를 늘려도 8배는 안 나온다.** 7,000 원자를 8장에 쪼개면 **875 원자/GPU** 로,
   `Fig. S1` 의 **ballistic region**(저이용)에 들어간다. `Fig. S2` 가 448 원자/GPU 에서 **0.79** 를 보인다.
   ⇒ **원자/GPU 를 최대화하는 쪽이 이득**. 계를 키우는 것(대형 모델)이 오히려 병렬효율에 유리하다.
3. **이상욱 랩이 왜 MTP 를 썼는지의 답이 여기 있다.** 그들은 7,000원자 20 ns 와 대형 50 ns 를
   **둘 다** 돌렸다. GNN 으로 하면 **89 + 506 = 약 600 A100-day** 다.
   ⇒ **Q-T2("A1 의 이유가 속도인가 PES 품질인가")의 속도 쪽 근거가 정량으로 확보됐다.**
   ⛔ 단 **PES 품질 쪽은 이 논문이 답하지 않는다** — Q-T2 는 **절반만** 닫힌다.

**⚠ 이 산정의 한계**
- **SevenNet-0(5층·l_max 2·r_c 5 Å·0.84 M 파라미터) 기준**이다. **UMA-S 는 150 M/6 M active** 로
  **자릿수가 다르다** — 우리 UMA 의 실제 처리량은 **직접 재야 한다**(이건 하루면 된다).
- **LAMMPS + 다중 GPU 경로**를 전제한다. **우리 UMA 는 ASE 단일 GPU** 다 —
  🔴 **UMA 에 LAMMPS 다중 GPU 경로가 있는지 이 논문은 말하지 않는다**(UMA 는 2025+ 모델).
  없다면 위 8-GPU 열은 **우리에게 아직 존재하지 않는 선택지**다.
- 계가 **불균질**(Li 금속 ‖ LPSCl 계면)하면 저자 자신이 *"synchronization costs could become more
  substantial"* 이라고 경고한다. 위 효율 가정은 **균질 벌크 기준**이라 **낙관적**이다.

---

## 15. 우리 기록에 남길 것

1. **`comparison_vs_ours.md` §J-7** 에 `[Park24]` 블록 추가 (물성 4축 **금지**).
2. **`talks/…lee2026…` §99-10 표 5행 완료 처리** + §99-3 정확도 표에 **base 행 추가 정정**.
3. **`kb/open_items.md` T1b** — *"대조군을 받았고, 판정은 안 났다. 정황은 반대 방향"* 으로 갱신.
4. **미해결로 남는 것**:
   - 🔴 **우리 UMA 의 층 수 T** — 확인해야 유효 수용영역을 계산할 수 있다.
   - 🔴 **UMA 의 LAMMPS/다중 GPU 경로 유무** — T3 계획의 전제.
   - 🔴 **figshare 원시 타이밍 데이터** — 프록시 차단으로 미확보.
   - 🔴 SevenNet-0 의 **참조 DFT 설정**(M3GNet 데이터셋 승계) — 이 논문에 명시 없음.

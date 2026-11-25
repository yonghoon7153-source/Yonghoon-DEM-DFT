<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md.
     2026-10-27 작성 — 병렬 9 편 중 1 편 (INDEX · comparison 반영은 메인 세션이 합친다).
     그림 9 장 전부 실독 + Table 2 크롭 확인 + 무번호 graphical abstract 쪽 렌더 확인.
     크롭 정정: Fig. 6 · 7 · 9 아래 ≈14 pt 잘림 → 재렌더 · 표 5 장 쪽 이음 수동 크롭 (figures.json recrop / manual_crop 사유). -->

# Universal Machine Learning Force Fields for Materials Simulation: From Model Construction to Complex-System Applications — Wang, Yi, Hu & Zhao (*Physica Scripta* 2026, Accepted Manuscript)

> slug `wang2026_umlff_review_softening_forgetting_longrange` · DOI `10.1088/1402-4896/aeb836` · type `리뷰 (MLIP 방법론) + 자체 frozen-checkpoint 힘 대조 2 건 (Li₆PS₅Cl AIMD · BaTiO₃) — 새 DFT 0 · 새 MD 0` · PDF `d17ba3fc-15._Universal_machine_learning_force_fields_for_materials_simulation_From_model_construction_to_complex-system_applications.pdf` (업로드 · 38 pp = IOP 표지 1 + 원고 37 pp) · digested `2026-10-27` · status ✅ · 태그 **[외부·리뷰·methods]**
> elements: Li, P, S, Cl, Ba, Ti, O, La, Zr
> methods: DFT, AIMD, MD, MLIP, phonon, elastic

> **저자**: **Guoyang Wang**¹, Jing Yi¹, Yuanmao Hu², **Shuai Zhao**¹\* — ¹School of Physics and Renewable Energy, **Chongqing University of Technology** (충칭이공대) · ²Interdisciplinary Graduate School of Engineering Sciences, **Kyushu University** (규슈대). 교신 zhaoshuai@cqut.edu.cn
> ***Phys. Scr.* (IOP) 2026, in press** · 원고번호 PHYSSCR-154972.**R1** (1 차 수정본 수락) · © 2026 IOP · **12 개월 엠바고 뒤 CC BY-NC-ND 4.0** (지금은 재배포 불가 — litdb 크롭은 내부 열람용) · 연구비 Chongqing Municipal Education Commission KJQN202401108 · refs **80** · Fig **9** · Table **5** · Box **2** · 무번호 graphical abstract 1
> ⚠ **이름 겹침 주의**: litdb 의 `wang2026_domain_oriented_universal_machine_learning_potential` (**Feng** Wang, 샤먼대 · *Nat. Commun.*) 은 **다른 논문**이다. 이 리뷰가 그 편을 ref 54 로 인용해 `Fig. 7a–c` 에 그림을 빌려 왔다 (§5.9).
>
> **계보 (이 리뷰가 세운 줄기)**: AGNI (2017 · 단원소 6 종) → Behler–Parrinello · GAP · MTP · SNAP (시스템 전용) → **M3GNet** (주기율표 규모 GNN) → **CHGNet** (자기모멘트 보조학습) → **MACE-MP-0** (등변 + ACE) → SevenNet · MatterSim · ORB (병렬 MD · 온도압력 범위 · 추론속도) → 최근 **UMA** (MoLE) · eSEN · Orb-v3 · DPA3 · SevenNet-Omni/Nano · GRACE · NEP89. 우리 엔진 (UMA-s-1p1) 은 이 줄기 끝에 **이름만** 나온다 (§5.6).
>
> 🎤 **관련 발표**: **해당 없음** — `talks/*` 인입 대기열에 이 논문은 없다 (메인 세션 확인 2026-10-27). 단 `talks/lee2026_skku_mlip_materials_design.md` **§12 의 10 번 항목**이 *"덱에도 이 talk 에도 softening 을 잰 수치가 없다"* 고 적은 빈칸에, 이 리뷰 `Table 2` 의 **SevenNet-0 on Li₆PS₅Cl 투영 기울기**가 첫 외부 수치를 준다 (§7c-2). 방향은 이 digest → talk 참조뿐이고 talk 파일은 고치지 않았다 (talk 은 citable=no).
>
> **본 digest 에서 실제로 본 그림 (2026-10-27)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. 7` `Fig. 8` `Fig. 9` — **9 장 전부** + `Table 2` 크롭 (쪽 이음 확인용) + 무번호 graphical abstract (쪽 렌더).
> 안 본 것: `Table 1` `Table 3` `Table 4` `Table 5` 의 크롭 이미지 — 값은 전부 PDF 텍스트 층에서 옮겼다 (표는 텍스트가 정확).
> 표기: 그림에서만 읽은 값 **`figure-read ≈`** · 그림 안에 인쇄된 숫자 **(그림 인쇄값)** · 원전 수치를 리뷰가 옮긴 것 **(리뷰 재인용)** · 표 값으로 내가 계산한 것 **(우리 산수)**.
> 🔧 **크롭 정정 (figures.json 에 사유)**: 추출기가 `Fig. 6` · `Fig. 7` · `Fig. 9` 의 아래 ≈14 pt (= x 축 눈금 · 축 제목) 를 잘랐다 → 이미지 사각형 끝까지 다시 렌더. 표는 도구가 1 · 3 만 잡았는데 (쪽 전체 렌더 · `Table 3` 은 본문 문장을 캡션으로 오인) **`Table 2` (Li₆PS₅Cl — 이 리뷰에서 우리에게 제일 중요한 표) 를 놓쳤다** (캡션 줄이 본문 단락과 같은 텍스트 블록에 들어 있음) → 표 5 장 모두 쪽 이음 수동 크롭.

---

## 0. 이 digest 를 읽는 법

이 논문은 **리뷰**다 — 새 DFT · 새 MD 는 없다. 그런데 우리에게 값이 있는 부분은 리뷰가 *정리한* 것보다
**리뷰 저자들이 직접 돌린 표 두 장** (`Table 2` · `Table 3`) 이다: 다섯 사전학습 체크포인트를 **미세조정 · 이완 · MD 없이**
공개 DFT 라벨 위에서 단일점 힘으로 잰 것. 그중 `Table 2` 의 계가 **Li₆PS₅Cl AIMD 프레임 999 개**다.

그리고 그 표가 쓰는 softening 지표 —
**원점 통과 힘 투영 기울기 Σ(F_DFT·F_pred) / Σ|F_DFT|²** — 는 **우리 도구의 식과 글자 그대로 같다**
(`tools/mlip/bench_against_dft.py::_softening_slope` · `tools/ionic/mlip_committee.py` 343 행 — 힘 성분을 펴서 (ravel) 원점 통과 최소제곱).
MAE 도 같은 정의 (Cartesian 성분) 다. ⇒ **이 리뷰의 표와 우리 기록은 '같은 자' 로 잰 숫자**다. 다만 **시험셋이 다르다** (§7b).

⚠ 오독 방지 두 가지:

1. **UMA 는 리뷰의 자체 대조 (`Table 2` · `Table 3`) 에도, 결함 벤치 (`Fig. 9`) 에도, graphical abstract 에도 없다.** UMA 가 나오는 곳은
   §3.2 본문 두 문장 (MoLE · UMA-M 총 1.4 B / 활성 ~50 M 파라미터 · 총/활성 구분의 예) 과 `Table 4` 두 줄 (GRACE 원논문 값 재인용) 뿐이다.
   `Table 2` 에서 우리 엔진에 가장 가까운 것은 **Orb-v3 (conservative inf OMat)** — **같은 OMat24 코퍼스 · 같은 보존력 (conservative)**
   이지만 **아키텍처가 다르다**. ⇒ *"리뷰가 UMA 를 검증했다"* 고 읽으면 안 된다.
2. **수치 대부분은 리뷰 재인용이다.** 리뷰가 직접 만든 수치는 `Table 2` · `Table 3` 뿐이고, 나머지 (`Table 1` · `Table 4` · `Table 5`,
   reEWC 의 MPE/MAPE, 전해질 · LLZO · BaTiO₃ 응용값) 는 원전 확인 전이다.

이 리뷰의 뼈대 = **신뢰성 병목 셋** — 우리 관행 셋과 1:1 로 맞물린다 (§7):

| 리뷰의 병목 | 우리 쪽 대응 (기록) |
|---|---|
| ① **PES softening** — 평형 근처에 치우친 사전학습 데이터 | 힘 투영 기울기 실측 (Li₃PS₄ 벤치 · a-Li₄PS₄Cl 소셀 원소별 기울기) |
| ② **catastrophic forgetting** — 하류 미세조정 | **미세조정 안 함** (UMA-s-1p1 동결 사용) — 도입하면 보존 시험이 필요 |
| ③ **장거리 정전기 · 분산 · 분극 결손** — 국소 cutoff | 점착은 UMA + 외부 D3(BJ) 가산 · 계면 반응 해석은 구조 서술까지만 |

---

## 1. 한 줄 요약

범용 MLFF (이 리뷰의 약어 **uMLFF** — 우리가 쓰는 uMLIP 와 같은 말) 가 시스템 전용 퍼텐셜에서 파운데이션 모델로 넘어온 흐름을
**데이터 → 벤치마크 → 미세조정 → 아키텍처 → 물리 사전지식 → 응용** 순으로 정리하고, 신뢰성의 세 병목 (softening · forgetting · 장거리) 을
축으로 삼은 리뷰다. 결론은 한 문장 — ***"universality describes model scope, whereas validation breadth describes how extensively that scope has been tested"*** —
**신뢰성은 과제마다 그 관측량으로 따로 세워야 한다.** 자체 대조가 그 말을 숫자로 보였다: 같은 다섯 체크포인트의 힘 MAE 가
**Li₆PS₅Cl (PBE) 에서는 6.6 배 벌어지고 (0.0316–0.2075 eV/Å, 투영 기울기 0.63–0.99)**, **BaTiO₃ (PBEsol) 에서는 1.6 배에 그치며
기울기가 전부 1 보다 크다 (1.03–1.08)** — *"the Li₆PS₅Cl high-force attenuation is not a general result."*

---

## 2. 메타 / 동기 / 구성

| 항목 | 내용 |
|---|---|
| 유형 | 리뷰 (MLIP 방법론) + **자체 frozen-checkpoint 힘 대조 2 건** (`Table 2` Li₆PS₅Cl · `Table 3` BaTiO₃) |
| 출처 상태 | IOP *Physica Scripta* **Accepted Manuscript** (VoR 전) · 인용은 DOI `10.1088/1402-4896/aeb836` · 권 · 쪽 미부여 |
| 정의 (Introduction) | **universality** = 퍼텐셜이 덮는 화학 · 구조 범위 (원소 · 조성 · 배위 다양성) · **foundation-model status** = 대규모 사전학습 + 하류 적응성 · **validation breadth** 와 **deployability** 는 universality 의 정의 기준이 아니라 **별도 차원** |
| 동기 | 범용화가 화학 공간을 넓히면서 새 문제 셋: ① 평형 근처 위주 사전학습 → 표면 · 결함 · 이동경로 · 강왜곡 배치가 덜 묶임 (*PES softening*) ② 미세조정 시 망각 ③ 국소 cutoff → 장거리 정전기 · 분산 · 분극 결손 (전해질 · 강유전체 · 전극–전해질 계면) |
| 리뷰의 태도 | *"should not be understood merely as a linear expansion of data size and model-parameter number"* — 데이터 분포 · 아키텍처 · 물리 제약 · 미세조정 · 평가체계의 **결합 진화** |
| 우리와의 관계 | 우리 엔진 (UMA-s-1p1 omat) 의 **사용 지침을 재는 외부 자** · 물성값 0 → **물성 4 축 금지** · comparison J 축 (🔧 방법 원전) 전용 |

**절 구성 (PDF 쪽 — 원고 쪽 = PDF − 1)**

| 절 | PDF 쪽 | 핵심 | 그림 · 표 |
|---|---|---|---|
| Abstract | 3 | 세 병목 · 응용 · 전망 | graphical abstract (무번호 · 'uMLFFs Ecosystem' A–F 여섯 경로) |
| Introduction | 4–5 | 정의 · 계보 · 세 병목 | `Fig. 1` (p.6) |
| §2.1 데이터 구축 | 6–9 | AGNI 4 단계 → 능동 PES 탐색 (MP-ALOE) · **참조 수준과 라벨 충실도** | `Fig. 2` `Fig. 3` |
| §2.2 벤치마크 | 9–13 | Matbench Discovery · CHIPS-FF · **자체 frozen 대조** | `Table 1` `Table 2` `Table 3` |
| §2.3 PES softening | 13–15 | 진단 · 데이터 범위 · 과제 수준 귀결 | `Fig. 4` |
| §3.1 망각 인지 미세조정 | 15–16 | reEWC (SevenNet-0 → Li₆PS₅Cl) | `Fig. 5` |
| §3.2 아키텍처 계보 | 16–21 | GNN · 등변 · Orb · ACE/GRACE · NEP · UMA · 선택 순서 | Box 1 · `Table 4` |
| §3.3 장거리 · 전하평형 · 분극 · 외부장 | 21–23 | Latent Ewald · FIREANN · PQEq · 4G-HDNNP | `Fig. 6` |
| §3.4 자성 | 23 | 위치만 받는 퍼텐셜의 한계 | — |
| §4.1 전지 전해질 | 23–25 | 액체 전해질 (domain-oriented) · c-LLZO · Li₃PS₄/Li | `Fig. 7` |
| §4.2 상전이 · 포논 | 25–28 | BaTiO₃ · 포논 벤치 | `Fig. 8` `Table 5` |
| §4.3 결함 · 표면 · 열수송 | 28–29 | CHIPS-FF · GRACE 결함 · 표면 · 열전도 | `Fig. 9` |
| §5 과제 · 전망 / §6 결론 | 29–32 | 설계 차원 넷 · 미래 과제 i–vi | Box 2 |
| References | 32–38 | 80 편 | — |

---

## 3. 핵심 수치 총정리 ★

### 3a. ★★ 자체 대조 ① — Li₆PS₅Cl AIMD 고정 배치 힘 (`Table 2`, 자체)

조건: 52 원자 Li₆PS₅Cl · Cl 이 음이온 4c 자리 절반 · **PBE AIMD 600 · 1000 K** (Kim et al. 2026 의 Zenodo 배포 궤적) ·
온도별 500 프레임 (첫 프레임 공유) → **999 고유 배치 · 51,948 원자–프레임 쌍** · 고힘 부분집합 = |F_DFT| 상위 10 % (**5,195 쌍 · |F_DFT| ≥ 1.763082 eV/Å**) ·
MAE = Cartesian 성분 (eV/Å) · 기울기 = 원점 통과 투영 · [ ] = 95 % 블록 부트스트랩 CI.

| 체크포인트 | MAE 600 K | MAE 1000 K | **MAE pooled** [CI] | 고힘 MAE [CI] | **기울기 pooled** [CI] | **기울기 고힘** [CI] |
|---|---|---|---|---|---|---|
| **Orb-v3** (conservative inf OMat) | 0.029370 | 0.033726 | **0.031557** [0.031409, 0.031709] | 0.0378 [0.0373–0.0384] | **0.9810** [0.9804–0.9815] | **0.9926** [0.9919–0.9933] |
| MatterSim-v1.0.0-1M | 0.062979 | 0.078059 | **0.070544** [0.070058, 0.071010] | 0.1111 [0.1092–0.1130] | **0.9871** [0.9858–0.9883] | **0.9983** [0.9963–1.0003] ← CI 가 1 포함 |
| SevenNet-0 | 0.094395 | 0.112481 | **0.103519** [0.102984, 0.104202] | 0.1970 [0.1947–0.1994] | **0.8438** [0.8417–0.8459] | **0.8740** [0.8707–0.8772] |
| MACE-MP-0 medium | 0.115625 | 0.136738 | **0.126277** [0.125535, 0.127149] | 0.3103 [0.3051–0.3154] | **0.7791** [0.7767–0.7815] | **0.7625** [0.7583–0.7666] |
| CHGNet 0.3.0 | 0.191733 | 0.222995 | **0.207538** [0.206856, 0.208728] | 0.4298 [0.4254–0.4342] | **0.6269** [0.6236–0.6302] | **0.6759** [0.6709–0.6811] |

**(우리 산수) 이 표에서 더 읽히는 것**
- **모델 간 폭**: pooled MAE 최악/최선 = CHGNet/Orb = **6.6 배** (MatterSim 2.2 · SevenNet 3.3 · MACE 4.0 배).
- **고힘/pooled MAE 비**: Orb **1.20** · MatterSim 1.57 · SevenNet 1.90 · CHGNet 2.07 · MACE **2.46** — MPtrj 계열일수록 꼬리가 무겁다.
- **1000 K/600 K MAE 비**: 1.15–1.24 (전 모델) — 온도로 순위는 안 바뀐다 (본문: *"the same model ordering at 600 and 1000 K. Every model had a higher MAE at 1000 K"*).
- ⭐ **고힘 기울기가 pooled 보다 1 에 *가깝다* — 다섯 중 넷** (Orb 0.981→0.993 · MatterSim 0.987→0.998 · SevenNet 0.844→0.874 · CHGNet 0.627→0.676; **MACE 만 0.779→0.763 로 반대**).
  ⇒ 이 데이터에서는 감쇠가 **고힘 꼬리에 몰려 있지 않다** — *"고에너지 · 비평형 배치에서 무른다"* 는 §2.3 의 서사를 이 표가 그대로 지지하지는 않는다. 리뷰는 이 점을 말하지 않는다 (§10-④).
- ⭐ **기울기 ≈ 1 ≠ 정확**: MatterSim 은 기울기 0.987 로 Orb 와 같은 무리인데 MAE 는 2.2 배다 — 기울기는 *계통 감쇠*만 재고 *산포*는 안 잰다. 둘을 같이 봐야 한다 (§12-②).

### 3b. 자체 대조 ② — BaTiO₃ PET-MAD test split (`Table 3`, 자체)

조건: **146 주기 40 원자 배치 (5,840 쌍) · PBEsol 참조** (Mazitov et al., Materials Cloud Archive 2025.145) · 상위 10 % = 584 쌍 (|F_DFT| ≥ 1.010988 eV/Å) · 기울기는 **전 쌍** · [ ] = 배치 단위 부트스트랩 (모델 간 같은 추첨).

| 체크포인트 | MAE | RMSE | 상위 10 % MAE | 기울기 (전 쌍) |
|---|---|---|---|---|
| Orb-v3 | **0.033909** [0.0294–0.0389] | 0.063805 [0.0532–0.0746] | 0.097077 [0.0787–0.1145] | **1.0805** [1.0673–1.0896] |
| MatterSim-1M | 0.039935 [0.0352–0.0450] | 0.073222 [0.0638–0.0830] | 0.101753 [0.0838–0.1180] | **1.0813** [1.0680–1.0896] |
| SevenNet-0 | 0.039086 [0.0344–0.0440] | 0.073738 [0.0640–0.0840] | 0.100260 [0.0834–0.1165] | **1.0651** [1.0484–1.0756] |
| MACE-MP-0 medium | 0.049723 [0.0436–0.0563] | 0.098110 [0.0845–0.1125] | 0.126974 [0.1019–0.1509] | **1.0774** [1.0499–1.0948] |
| CHGNet 0.3.0 | **0.054900** [0.0489–0.0612] | 0.093831 [0.0824–0.1059] | 0.121180 [0.1024–0.1373] | **1.0262** [0.9961–1.0459] ← CI 가 1 포함 |

- SevenNet-0 ≈ MatterSim (0.039086 vs 0.039935) — *"the paired 95% interval for their difference included zero."*
- (우리 산수) 최악/최선 = **1.6 배** (Li₆PS₅Cl 6.6 배의 1/4). 다섯 전부 **기울기 > 1 = 과대예측**.
- 리뷰의 단서 (그대로): *"The Li₆PS₅Cl and BaTiO₃ tests use different reference functionals (PBE and PBEsol) and different configurations; changes in error between them cannot be attributed to material identity alone."*
- ⚠ **내 가설 (리뷰에 없음)**: PBE 로 학습한 체크포인트를 PBEsol 평형 (더 작은 부피) 근처 배치에 대면 계통적으로 큰 힘이 나올 수 있다 — 그러면 BaTiO₃ 의 기울기 > 1 은 *재료*가 아니라 *범함수 불일치*의 서명일 수 있다. 우리 Li₃PS₄ 벤치 (PET-MAD **PBEsol** 라벨 · UMA omat 는 PBE) 에도 같은 혼입이 있다 (§7a-4) — 그 벤치를 기울기와 함께 다시 내면 이 가설을 우리 데이터로 시험할 수 있다 (§12-②).

### 3c. 망각 인지 미세조정 — Kim et al. 2026 reEWC (리뷰 재인용, `Fig. 5`)

| 항목 | 값 |
|---|---|
| 기저 / 표적 | **SevenNet-0** → **Li₆PS₅Cl** |
| 비교 전략 | naive · layer freezing · low LR · experience replay · EWC · **reEWC** (= replay + EWC) |
| 적응셋 | **1,000 배치 · 100 ps MD @ 600 · 1000 K** · 학습:검증 9:1 |
| replay / 보존 감시 | MPtrj 무작위 10 % (replay) · MPtrj 10 % 표본 = **sMPtrj** (보존) |
| E/F 시험 | **126 argyrodite 조성** + **9 비-argyrodite Li SE** |
| D 비교 | **45 argyrodite** + 9 기타 @ **800 · 1000 · 1200 K** · 점마다 **독립 MD 초기화 5 개** 평균 ± 표준편차 |
| **D 오차 (MPE / MAPE)** | argyrodite: **reEWC −5 % / 11 %** vs **사전학습 SevenNet-0 24 % / 26 %** · 비-argyrodite: **reEWC 0 % / 17 %** vs 사전학습 **18 % / 33 %** · **naive 는 비-argyrodite 9 계에서 50 % / 57 %** |
| 그 밖 | naive 는 표적 손실을 낮추되 sMPtrj 손실을 올리고 **탄성상수 · 포논 예측을 바꿨다** · 순차 · 동시 3 표적 시험 = *"initial evidence"* |

⚠ MPE 의 부호 규약 (예측 − 기준 인가) 이 리뷰에 없다 — 통상 규약이면 **사전학습 SevenNet-0 가 argyrodite D 를 ~24 % 과대** = softening (장벽 과소 → D 과대) 방향과 일치. 원전 확인 전에는 부호를 인용하지 않는다.

### 3d. Matbench Discovery 부분표 (`Table 1`, Ref. 36 리뷰 재인용 · WBM · MAE/RMSE eV/atom)

| 모델 | F1 | DAF | Precision | MAE | RMSE | 라벨 |
|---|---|---|---|---|---|---|
| eqV2 S DeNS | **0.815** | 5.042 | 0.771 | 0.036 | 0.085 | EFS |
| ORB MPtrj | 0.765 | 4.702 | 0.719 | 0.045 | 0.091 | EFS |
| SevenNet | 0.724 | 4.252 | 0.650 | 0.048 | 0.092 | EFS |
| MACE | 0.669 | 3.777 | 0.577 | 0.057 | 0.101 | EFS |
| CHGNet | 0.613 | 3.361 | 0.514 | 0.063 | 0.103 | EFSM |
| M3GNet | 0.569 | 2.882 | 0.441 | 0.075 | 0.118 | EFS |
| ALIGNN | 0.567 | 3.206 | 0.490 | 0.093 | 0.154 | Energy |
| MEGNet | 0.510 | 2.959 | 0.452 | **0.130** | 0.206 | Energy |
| CGCNN | 0.507 | 2.855 | 0.436 | **0.138** | 0.233 | Energy |
| Dummy | 0.185 | 1.000 | 0.154 | **0.124** | 0.184 | — |

- (우리 산수) **MEGNet · CGCNN 의 MAE (0.130 · 0.138) 가 평균값 Dummy (0.124) 보다 나쁜데 F1 은 2.7 배** — *"low formation-energy prediction error does not ensure strong stability classification"* 의 가장 짧은 증거.
- ⚠ 이 표는 **옛 스냅숏**이다. `Table 4` (다른 출처) 와 섞지 않는다 — 'MACE' 0.669 vs 'MACE-MPA-0' 0.852, 'ORB MPtrj' 0.765 vs 'ORB-v3' 0.906 은 **다른 체크포인트 · 다른 시점**이다.

### 3e. 최근 체크포인트 — F1 · κSRME · 속도 (`Table 4`, Ref. 49 = GRACE 원논문 리뷰 재인용)

속도 = **μs atom⁻¹ step⁻¹**, **1024 원자 W-bcc · NVIDIA A100 80 GB 한 장**, ASE / LAMMPS 구분.

| 모델 | 그룹 | F1 | κSRME | t_ASE | t_LAMMPS |
|---|---|---|---|---|---|
| UMA-M-1.1 | MatBench-compatible | **0.930** | 0.195 | 2981 | — |
| eSEN-30M-OAM | 〃 | 0.925 | 0.170 | 1897 | — |
| eqV2-M | 〃 | 0.917 | **1.771** | — | — |
| **UMA-S-1.1** | 〃 | **0.916** | **0.203** | **401** | — |
| ORB-v3 | 〃 | 0.906 | 0.210 | 197 | — |
| SevenNet-MF-OMPA | 〃 | 0.901 | 0.317 | 651 | — |
| GRACE-2L-OAM-L | 〃 | 0.890 | **0.168** | 91 | 51 |
| DPA-3.1-3M-FT | 〃 | 0.884 | 0.469 | 227 | — |
| GRACE-2L-OAM-M | 〃 | 0.881 | 0.200 | 71 | 31 |
| GRACE-2L-OAM | 〃 | 0.880 | 0.294 | 64 | 23 |
| MatterSim-v1 | 〃 | 0.862 | 0.574 | 198 | — |
| MACE-MPA-0 | 〃 | 0.852 | 0.412 | 198 | — |
| GRACE-1L-OAM | 〃 | 0.824 | 0.516 | 51 | 10 |
| GRACE-1L-OAM-L | 〃 | 0.815 | 0.377 | 54 | 13 |
| GRACE-2L-OMAT-L | OMat24-only | — | 0.186 | 91 | 51 |
| GRACE-2L-OMAT-M | 〃 | — | 0.217 | 71 | 31 |
| MACE-OMAT-0 | 〃 | — | 0.245 | 202 | — |
| GRACE-2L-OMAT | 〃 | — | 0.288 | 64 | 23 |
| GRACE-1L-OMAT-L | 〃 | — | 0.383 | 54 | 13 |
| GRACE-1L-OMAT | 〃 | — | 0.398 | 51 | 10 |

- F1 = Matbench Discovery 안정 분류 (높을수록 좋음) · κSRME = **103 개 이원계 열전도도**의 대칭 상대 평균오차 (낮을수록 좋음 — F1 과 다른 과제) · 빈칸은 0 이 아니다 (각주 원문 *"missing entries are not zero"*).
- (우리 산수) **UMA-S-1.1 401 μs × 1024 원자 = 0.41 s/step ≈ 2.4 step/s**. UMA 원논문 표 1 은 **1k 원자 16 step/s** (H100 · TF-32 · torch.compile · MoLE 사전병합 · 그래프 생성 제외 — `uma2026` digest §3.1) ⇒ **같은 모델의 속도가 프로토콜에 따라 ≈ 6.6 배** 갈린다 (UMA-M: 0.33 vs 3 step/s ≈ 9 배). 리뷰 각주가 정확히 이 경고다: *"Checkpoint, training reference level and test protocol should accompany transfer of these values to another task."*
- UMA-M-1.1 F1 0.930 ↔ `uma2026` digest 의 UMA-M 0.929 — 출처가 다른 같은 값 (0.001 차).
- ⚠ **`Table 4` 의 'ORB-v3' 는 'MatBench-compatible' 줄**이다 — `Table 2` 의 **Orb-v3 (conservative inf OMat)** 과 같은 체크포인트라는 보장이 없다 (`Fig. 9` 는 `ORBv3-cons-inf-mpa` 와 `-omat` 을 따로 그린다). 리뷰는 이 구분을 하지 않는다.
- ⚠ 'UMA-S-1.1' 이 **어느 task 로** 잰 값인지 표에 없다 — 우리 `omat` task 값으로 읽지 않는다.

### 3f. 포논 — 동역학 안정성 혼동행렬 (`Table 5`, Ref. 63 = Loew 2025 리뷰 재인용) + 파라미터 수

PBE 기준 **8189 stable / 1769 unstable**. TS + FU = 100 (PBE-stable) · TU + FS = 100 (PBE-unstable).

| 모델 | TS % | FU % | TU % | FS % | 경향 (리뷰 표기) |
|---|---|---|---|---|---|
| M3GNet | 87 | 13 | 73 | 27 | Relatively balanced |
| CHGNet | 77 | 23 | 73 | 27 | Moderate stable recall |
| MACE-MP-0 | 95 | 5 | 73 | 27 | High stable recall |
| SevenNet-0 | 81 | 19 | 80 | 20 | Balanced classification |
| MatterSim-v1 | 95 | 5 | 75 | 25 | High stable recall |
| ORB | **15** | **85** | 92 | 8 | Over-predicts instability |
| eqV2-M | **7** | **93** | 94 | 6 | Strongly over-predicts instability |
| **PBEsol** (다른 DFT) | 97 | 3 | 76 | **24** | Reference comparison |

- (우리 산수) **PBEsol 조차 PBE-불안정의 24 % 를 안정으로 판정**한다 — 모델의 FS 20–27 % 는 *범함수끼리의 불일치 바닥*과 같은 크기다. 모델 비교의 바닥선으로 읽는다.
- ⚠ 'ORB' 의 판 (版) 이 리뷰에 없다 (원전 시점상 Orb-v3 이전일 가능성) — `Table 2` 의 Orb-v3 conservative 와 **동일시 금지**.
- 파라미터 수 (같은 포논 벤치 출처, 리뷰 재인용): M3GNet **0.23 M** · CHGNet 0.41 M · SevenNet-0 0.84 M · MatterSim-v1 4.5 M · MACE-MP-0 4.69 M · ORB 25.2 M · eqV2-M **86 M** · (별도) UMA-M 총 **1.4 B / 활성 ~50 M**.
  리뷰: *"Trainable parameter count helps characterize capacity but is not a proxy for either predictive accuracy or wall-clock speed."*

### 3g. 데이터셋 (리뷰 재인용)

| 데이터 | 규모 · 참조 | 리뷰가 강조한 점 |
|---|---|---|
| AGNI (Huan 2017) | 단원소 6 종 (Al · Cu · Ti · W · Si · C) · 300 · 600 K 벌크 DFT-MD | 벌크 힘 정확도가 표면 · 점결함 · 전이상태 · 강압축을 보증하지 않는다 (AGNI 방식 자체가 아니라 *그 학습셋의 범위* 문제) |
| MPtrj | MP 이완 궤적 · MACE-MP-0 = 89 원소 | 평형 근처 위주 |
| **OMat24** | **> 1.1 억** DFT 계산 + 사전학습 모델 | (UMA omat · Orb-v3 OMat 의 코퍼스) |
| MatPES | 주로 **300 K MD** | — |
| **MP-ALOE** | **~100 만 r2SCAN** 프레임 · 원형구조 원소치환 + 위원회 질의 능동학습 + 대표 축소 | 힘 크기 · 압력의 **주변분포**가 MatPES 보다 넓다 — 그러나 *"do not by themselves establish improved coverage of specific configuration classes such as defects, surfaces, or transition states"* |

### 3h. 응용 사례 수치 (리뷰 재인용)

| 계 | 수치 | 리뷰가 단 단서 |
|---|---|---|
| **액체 전해질** (Wang 2026 domain-oriented, DeepMD) | 용매 2,300+ · 염 ~20 · 동시학습 91 회 · **PBE-D3** · ~160,000 배치 · 19 원소 · 300–800 K · 1–100 bar · RMSE **~0.005 eV/atom · 0.16 eV/Å** · 5 ps 궤적 13,000+ 끝점 DFT 재검 · σ = NE (~10 ns) | *"these errors alone do not determine transport accuracy"* · NE 는 **이온–이온 교차상관 미포함** · 배위수명은 *"useful microscopic descriptor"* 이지 유일한 인과가 아님 |
| **c-LLZO** (Gao 2025 polarizable) | Ea **AIMD 0.258 ± 0.017 · 모델 0.261 ± 0.006 · 장거리 뺀 모델 0.263 ± 0.006 eV** (그림 인쇄값) · ns MD · 800–1800 K MSD | *"Similar activation energies in (d) alone do not isolate a long-range contribution"* · 확산 통계 · 장벽은 독립 검증 필요 (He 2018 인용) |
| **Li₃PS₄/Li** 반응 MD (Gao 2025) | **13,760 원자** · 계면 재배열 + 유효전하 변화 | 산화환원 경로 · 2 차상 · 부동태 · 공간전하 귀속은 *경계조건 명시 + 독립 상 · 전자구조 검증* 필요 |
| **Li₃YCl₆ · Li₆PS₅Cl** (Du 2025) | 에너지 · 힘 · 포논 · 탄성상수 · Li 확산으로 사전학습 퍼텐셜 평가 — **리뷰에 숫자 없음** | *"one diffusion curve cannot validate disorder, lattice response and transport across electrolytes"* |
| **BaTiO₃** (Gao 2025) | R–O–T–C 순서 재현 · 전이온도 **≈145 · 205 · 285 K** (실험보다 낮음) | 순서 재현 ≠ 전이온도 정량 일치 |
| **BaTiO₃ 등** (Eggestad 2026 on-the-fly) | 상 순서는 정성 재현 · 전이온도는 XC 의존 · **PBEsol 이 LDA · r2SCAN 보다 견고** | 라벨 충실도의 실례 |
| **LaMnO₃ · SrRuO₃** (Jansen 2023, DFT+U MLFF) | U 선택이 LaMnO₃ 구조전이를 바꿈 | *"fitting the labels more closely cannot by itself remove errors in the reference PES"* |
| **NEP89** | 89 원소 · 비교 대상 파운데이션 모델보다 처리량 **10³–10⁴ 배** · 백만 원자 시연 | *"source-specific results, not a hardware-matched ranking"* |
| 벌크모듈러스 (Gao 2025, `Fig. 6c–e`) | Reuss R² 0.93 · MAE **13.54 GPa** / Voigt 0.94 · **12.98** / VRH 0.94 · **13.08 GPa** (그림 인쇄값) | — |

- **장벽 홉 수 검산** (CLAUDE.md · `D-2026-09-27-barrier-hop-count` · c-LLZO Ea ≈ 0.26 eV · ν₀ = 10¹³ s⁻¹ **가정**): Γ(800 K) ≈ 2.3×10¹¹ s⁻¹ → 평균 대기 ≈ 4.4 ps · 1 ns 창이면 N ≈ 230 · Γ(300 K) ≈ 4×10⁸ s⁻¹ → 평균 대기 ≈ 2.4 ns. ⇒ 800–1800 K · ns MD 에서 수백–수천 홉 — `Fig. 7e` 의 800 K MSD 가 ≈ 10–20 ps 뒤 기울기 1 에 붙는 것 (figure-read ≈) 과 차수가 맞는다. 확산계수 · 전도도 검산이 아니다.

### 3i. 물성 4 축 (A 이온전도 · B 산화 · C 기계 · D 전자구조)

| 물성 | 값 | 비고 |
|---|---|---|
| 이온전도도 σ (우리 계) | **n/a** | 액체 전해질 σ · c-LLZO D 는 남의 계 · 리뷰 재인용 |
| 활성화E Ea (우리 계) | **n/a** | c-LLZO 0.26 eV 는 남의 계 |
| 산화 onset / ESW | **n/a** | 리뷰에 ESW 없음 |
| 기계 (E/B/G, C_ij) | **n/a** | 벌크모듈러스 MAE ~13 GPa 는 데이터셋 평균 (남의 계) |
| 전자구조 (gap) | **n/a** | — |

⇒ ⛔ **물성 4 축 진입 금지 (값 0 건)** · comparison **J 축 🔧 방법 원전** 전용.

---

## 4. 계산 방법 ★ (리뷰 자체 대조 + 인용 연구 설정)

### 4a. 리뷰 자체 대조 — 두 표 (Li₆PS₅Cl · BaTiO₃) 의 설정
- **code / version**: 다섯 체크포인트 이름만 — Orb-v3 (conservative inf OMat) · MatterSim-v1.0.0-1M · SevenNet-0 · MACE-MP-0 medium · CHGNet 0.3.0. **패키지 판 · 정밀도 (float32/64) · 장치 · 이웃목록 설정은 미기재 (n/a)**.
- **절차**: *"The same downloaded checkpoint weight files were reused across both test sets, without material-specific fine-tuning, geometry relaxation, or model-driven molecular dynamics."* — 고정 기하 단일점 힘만.
- **참조 (functional)**: Li₆PS₅Cl = **PBE** (AIMD, Kim et al. 2026, Zenodo `10.5281/zenodo.15686940`) · BaTiO₃ = **PBEsol** (PET-MAD test split, Materials Cloud `10.24435/materialscloud:fe-1p`). 참조 DFT 의 k · ecut · PP · vdW 는 리뷰에 없다 (**n/a — 원전 확인 필요**).
- **supercell / nat**: Li₆PS₅Cl **52 원자** (단위정 1 개) · BaTiO₃ **40 원자** × 146.
- **무질서 처리**: Li₆PS₅Cl 은 **단일 배치** — *"Cl occupied half of the anion 4c sites, and S occupied the remaining 4c sites"* (= 4a/4c 50 % 자리교환 한 배치). SQS · 열거 없음.
- **AIMD**: 600 · 1000 K · 온도별 500 프레임 · 첫 프레임 공유. 앙상블 · 열욕 · dt · 총 길이는 리뷰에 없음 (reEWC 절의 *"1,000 configurations from 100-ps MD at 600 and 1000 K"* 가 같은 자료일 가능성 — **확정 못 함**).
- **통계**: Li₆PS₅Cl = **10,000 회 온도층화 순환 이동블록 부트스트랩 (12 프레임 블록 · seed 20260927)**, 고힘 컷오프 고정 · BaTiO₃ = **배치 단위 10,000 회 percentile 부트스트랩 (모델 간 같은 추첨 = 짝 비교 · seed 20260927)**.
- **스스로 단 한계 (원문)**: 사전학습 데이터와의 겹침 **미검증** · CI 는 *"do not cover pretraining overlap, reference-functional differences, or untested properties"* · *"individual model predictions and analysis scripts are not included with this manuscript."*
- **DFT+U · vdW · MLIP 학습**: 해당 없음 (학습 0).

### 4b. 인용 연구 설정 (리뷰 재인용)
- **reEWC (Kim 2026)**: §3c 표.
- **domain-oriented 전해질 (Wang 2026)**: DeepMD-kit · 동시학습 91 회 · PBE-D3 · §3h.
- **polarizable long-range (Gao 2025)**: 에너지 = 단거리 비정전 + **PQEq 정전 (전역 결합 전하 + core–shell 분극)** + **DFT-D3 분산 (따로)** · 전기음성도 · 경도 관련 *모델 파라미터*와 배치마다 푸는 *전하 자유도*를 구분.
- **포논 벤치 (Loew 2025)**: ~10,000 ab initio 포논 · PBE 참조.
- **softening (Deng 2025)**: M3GNet · CHGNet · MACE-MP-0 · 표면 · 결함 · 혼합에너지 · 이동장벽 · 포논 · WBM 1000 화합물 기울기.
- **결함 벤치 (Lysogorskiy 2026 GRACE)**: 13 BCC + 13 FCC 금속 · PBE 참조 · SIA · 빈자리 형성에너지.

---

## 5. 절별 상세 — 논증 흐름 전체

### 5.1 Introduction — 정의와 세 병목 (`Fig. 1`)
- 제일원리 (DFT · AIMD) 는 수천 원자 · 수백 ps 를 넘기 어렵고, 고전 퍼텐셜은 함수형에 전이성이 묶인다. MLFF 는 *"first-principles accuracy within well-covered configuration spaces"* 를 겨냥한다.
- 초기 MLFF (AGNI · BPNN · GAP · MTP · SNAP) 는 **one-system-one-model** — 새 계마다 재샘플 · 재학습.
- 대규모 DB + GNN + 등변 표현학습 + HPC 로 범용 · 파운데이션 MLFF 가 등장. 리뷰는 **universality (범위)** · **foundation status (사전학습 + 적응)** · **validation breadth** · **deployability** 를 **서로 다른 축**으로 둔다 — 이것이 이 리뷰 전체의 문법이다.
- 계보: M3GNet (3 체 GNN · 주기율표 규모) → CHGNet (자기모멘트 보조) → MACE-MP-0 (등변 MP + ACE · 고체 · 액체 · 계면 · 분자 · 반응계 전이) → SevenNet (대규모 병렬 MD) · MatterSim (온도 · 압력 범위) · ORB (확장 가능 추론).
- 세 병목: ① **PES softening** — *"Energy or force underprediction has been observed for particular models and test sets, but its extent and origin must be assessed for each model and application"* ② **catastrophic forgetting** ③ **장거리** (전해질 · 강유전체 · 전극–전해질 계면).

### 5.2 §2.1 데이터 구축 — 수동 수집에서 능동 PES 탐색으로 (`Fig. 2`, `Fig. 3`)
- AGNI 4 단계 (`Fig. 2`): ① DFT 참조 배치 · 힘 ② **방향 분해 지문** (평행이동 · 동종원자 치환 불변 · 회전은 회전된 참조로 학습) ③ 클러스터링 · 힘 구간화 · 능동학습으로 **작고 중복 없는 대표 학습셋** ④ 커널 릿지 회귀 → 힘장. 이 워크플로가 이후 uMLFF 의 방법적 바탕.
- 한계 단서: AGNI 단원소 모델은 300 · 600 K 벌크 DFT-MD 에서 뽑았으므로 **표면 · 점결함 · 이동 전이상태 · 강압축**의 정확도는 그 시험으로 안 선다 (단 Al 의 점결함 확산 · 표면 adatom 연구는 따로 있었다 — *"this limitation concerns the scope of the specific training sets ... rather than the AGNI approach as a whole"*).
- 전환: *"passive collection of relaxation trajectories"* → *"active PES exploration"*. 대표 MP-ALOE (`Fig. 3`). 결합 패러다임 = **범용 DB + 대규모 사전학습 + 능동학습 보충 + 하류 미세조정**. *"the universality of MLFFs depends on the coverage of elements, structures, temperature and pressure conditions, and off-equilibrium states, not merely on model size."*
- ★ **참조 수준과 라벨 충실도** (이 절의 핵심 단락): *"A learned potential approximates the potential-energy surface specified by its training labels, so the exchange-correlation approximation and calculation settings are part of its applicability domain."* PBE (널리 쓰임) · PBEsol (조밀 고체 평형) · r2SCAN (별도 meta-GGA) — 우열은 물성 의존. 상관 물질은 U · 자기배열 · 국소전자 처리가 참조를 바꾼다. 혼성 · 분산보정은 *"none supplies a universally exact reference"*. ⇒ ***"Labels from different functionals should therefore be identified separately."*** 한 모델로 합치려면 **에너지 기준 정렬 + 명시적 multifidelity 설계** 필요, *"rather than unqualified pooling"*. 실례: 강유전체 전이온도의 XC 의존 (PBEsol 견고) · LaMnO₃ 의 U 의존. *"the reference functional and its parameters, magnetic state and target observable must be recorded together with force errors."*

### 5.3 §2.2 표준 벤치마크 + 자체 대조 (`Table 1`, `Table 2`, `Table 3`)
- 전통 평가 (무작위 분할 + MAE / RMSE / R²) 는 소재 발견 가치를 다 못 잡는다 — 안정 경계 근처 오차가 위양성 · 위음성을 만든다.
- **Matbench Discovery**: WBM (원소 치환 생성) 을 **전향적 시험셋**으로, 회귀가 아니라 **convex hull 거리 기반 안정 분류** (precision · recall · F1 · **DAF**) 로 바꿨다. 결론 *"low formation-energy prediction error does not ensure strong stability classification"* · E · F · S 로 이완하는 범용 퍼텐셜이 에너지 전용 모델을 이긴다.
- **CHIPS-FF**: 탄성상수 · 포논 · 결함 · 표면 · 계면 · 비정질로 평가 확장 — *"shifting the focus from fitting DFT labels to reliably predicting essential material properties."*
- 다층 평가 목록: E · F · S 회귀 · 구조 이완 · 열역학/동역학 안정 · 포논 · 결함 · 표면 · 실사용 계산 효율. *"universality describes model scope, whereas validation breadth describes how extensively that scope has been tested."*
- ★ **자체 frozen 대조** (§3a · §3b · §4a): 다섯 체크포인트를 두 시험셋에. 결론 두 줄 — ① Li₆PS₅Cl 에서 MPtrj 계열 셋 (SevenNet-0 · MACE-MP-0 · CHGNet) 은 **기울기 0.63–0.87 = 감쇠**, OMat24 로 학습한 Orb-v3 와 자체 능동학습 (넓은 온도 · 압력) 데이터의 MatterSim 은 **≈ 1** ② BaTiO₃ 에선 전부 **> 1** ⇒ *"the Li₆PS₅Cl high-force attenuation is not a general result across these test configurations."* 그리고 바로 단서: *"These static-force results do not establish accuracy for structural relaxation, ferroelectric transitions, phonons, diffusion, long-time model-driven dynamics, or other systems."*

### 5.4 §2.3 PES softening — 진단 · 데이터 범위 · 과제 귀결 (`Fig. 4`)
- *"PES softening is a reported manifestation of this coverage gap, but its force-based diagnostic does not identify a unique cause."*
- Deng et al.: M3GNet · CHGNet · MACE-MP-0 가 표면 · 결함 · 혼합에너지 · 이동장벽 · 포논 시험에서 **에너지 · 힘 과소예측**.
- ★ 진단의 한계 (리뷰가 두 번 강조): ***"A force-regression slope below one diagnoses aggregate force underprediction; it is not a direct measurement of the Hessian or PES curvature."*** 평형 근처 학습은 *그럴듯한* 원인이고 아키텍처 · 라벨 충실도 · 외삽도 기여할 수 있다.
- 하류 귀결: **장벽 과소 → D 과대** · 포논 · 표면 · 결함 · 혼합에너지 오차 → 안정성 · 속도론 분석으로 전파.
- 처방: 비평형 DFT 배치로 표적 보정 · 미세조정 — 단 *"its effectiveness should be established on independent post-tuning tests of the relevant barriers, pathways, or properties rather than inferred from the training fit alone."* ⇒ 데이터 구축 때 **비평형 · 고힘 · 고에너지 배치를 의도적으로 샘플링**.

### 5.5 §3.1 망각 인지 미세조정 (`Fig. 5`)
- 고체전해질 이온확산 · 계면반응 · 복잡 상전이에는 소량 표적 데이터로 미세조정이 *"often necessary"*. naive 는 표적 오차를 줄이지만 사전학습 분포 성능을 깎는다 = **catastrophic forgetting**.
- Kim et al.: SevenNet-0 → Li₆PS₅Cl 에서 naive · layer freezing · low LR · replay · **EWC** (Fisher 정보행렬로 파라미터 중요도를 재서 중요 파라미터의 큰 이탈을 벌점) · **reEWC** (replay + EWC) 비교 → reEWC 가 적응–보존 균형이 제일 좋았다. 수치는 §3c.
- 리뷰의 단서: 순차 · 동시 3 표적은 *"initial evidence for multi-step and multi-target learning; longer task sequences and broader chemistries still require validation."*

### 5.6 §3.2 아키텍처 계보와 정확도–효율 교환 (Box 1, `Table 4`)
- **GNN 경로**: M3GNet (3 체) · CHGNet (자기모멘트 보조) · MatterSim (능동학습으로 T · P 범위) — 선대: 메시지 패싱 · SchNet · CGCNN · MEGNet. *"good average errors on energies and forces do not guarantee reliable predictions for high-energy configurations, phonons, defects, or long-time MD simulations."*
- **등변 · 고차 다체 경로**: MACE-MP-0 (등변 MP + ACE) · SevenNet (대규모 MD 병렬 · LAMMPS 배포) · eqV2 (고차 등변 Transformer).
- **Orb**: 빠른 추론 설계 공간 — Orb-v3 는 **등변성 · 그래프 희소성 · 힘 보존성**이 다른 변형을 낸다 ⇒ *"The particular Orb checkpoint therefore matters"* · **직접힘 (direct-force) 모델은 포논 · 열수송 전에 에너지–힘 일관성 시험을 따로**.
- **ACE/GRACE**: 체계적 다체 기저 · GRACE 는 그래프/트리 기저로 확장하고 **총에너지 미분으로 힘** → 일관성이 구조적으로 보장.
- **NEP (NEP89)**: 종 의존 국소 기술자 + 작은 원자 신경망 · 에너지 미분 힘 · 89 원소 · GPUMD 배포 · 처리량 10³–10⁴ 배 (원전 비교 한정).
- **최근 파운데이션**: ***UMA*** = 분자 · 재료 · 촉매 데이터 결합 + **mixture-of-linear-experts** · 중형 **총 1.4 B / 활성 ~50 M** · **eSEN** = 매끈한 에너지 보존 시뮬레이션 (안정성 · 열수송 · 포논 시험) · **Orb-v3** = 지연 · 메모리 · 등변성 · 힘 구성의 귀결 탐구 · **DPA3** = 선그래프 메시지 패싱 + 데이터셋 인코딩 (다중 도메인) · **SevenNet-Omni** = 학습 도메인 간 전이 · **SevenNet-Nano** = 교사 모델 증류. *"Their reported gains are tied to their respective datasets and protocols and should be checked at the checkpoint and task level."*
- ★ **모델 선택 순서**: ***"specify the observable, then the required model behavior, and finally a relevant test."*** 백만 원자 MD → 처리량 · 안정 궤적 / 포논 · 열수송 → 검증된 PES 미분 + (직접힘이면) 에너지–힘 일관성 / 반응 · 대전 계면 → 학습 범위 + 전하상태 · 경계조건 처리 검증.
- Yu et al. (M3GNet-DIRECT · CHGNet · MACE-MP-0 · ALIGNN-FF): MACE-MP-0 이 형성에너지 · 포논 오차 최저, CHGNet · M3GNet-DIRECT 는 이완 격자에서 양호 — 학습 데이터 · 참조가 달라 *아키텍처 효과를 분리 못 함*.
- Box 1 (정성 비교): M3GNet/CHGNet = 고처리 이완 · 스크리닝 · 기준선 (OOD 결함 · 표면 · 포논 주의) · MACE-MP-0/SevenNet/eqV2 = 표적 오차 · 미분 검증 · Orb/Orb-v3 = *"Select the actual checkpoint and test force conservativeness, energy-force consistency and task errors before derivative-sensitive use"* · GRACE = 사전 스크리닝 → 고정확 재확인의 다층 워크플로 · Latent Ewald/FIREANN/PQEq = 전해질 · 강유전체 · 계면 전하 재분배 · domain-oriented = 설계 도메인 밖 전이성 별도 평가 · NEP89 = 고처리 MD, 표적 화학 검증.

### 5.7 §3.3 장거리 상호작용 · 전하평형 · 분극 · 외부장 (`Fig. 6`)
- 다층 메시지 패싱이 수용 영역을 넓혀도 cutoff 너머의 전역 상호작용은 못 그린다 → **물리 사전지식의 명시적 결합**.
- **Latent Ewald** (Cheng 2025): 국소 기술자에서 숨은 장거리 변수를 배워 역공간 합으로 상호작용.
- **FIREANN**: 외부 전기장 방향 · 세기에 반응하는 임베딩 · 장 의존 총에너지 → 장 미분으로 응답량. ★ 미묘한 단서: *"force-only labels determine the field-dependent energy only up to an arbitrary field-dependent constant; derivatives of this constant also affect dipole and polarizability"* ⇒ 힘 라벨만으로는 응답 예측이 안 선다 — 게이지 · 가지 일관 응답 제약 필요.
- **PQEq 분극 장거리 파운데이션 (Gao 2025)**: 단거리 비정전 + PQEq 정전 + DFT-D3 분산 (따로) · LiFePO₄ · c-LLZO · BaTiO₃ · Li₃PS₄/Li 응용은 *"feasibility"* 를 세울 뿐 — ***"the separate contribution of the long-range module remains to be determined by matched ablation tests."***
- **전하 이동 ≠ 분극 ≠ 고정전하**: 4 세대 HDNNP (Ko 2021) = 환경 의존 전기음성도 + 전역 전하평형. *"Such partial charges are model variables rather than a direct measurement of electron flow"* ⇒ 전극 · 반응 계면 검증은 부과한 전하 · 경계조건 · 참조 전하상태 범위 · *재분배와 실제 산화환원을 가르는 관측량*을 포함해야.

### 5.8 §3.4 자성 — 위치만 받는 퍼텐셜의 한계
- 스핀분극 DFT 라벨은 자기질서 · 전자구조 방법에 의존하는데 *"a position-only potential generally assigns a single energy to each atomic geometry."* CHGNet 의 자기모멘트 보조학습은 스핀 방향을 독립 입력으로 만들지 않는다. 자기 MTP 는 bcc Fe 에서 원자 · 공선 스핀 자유도를 같이 모델링.
- 강자성 · 반강자성 · 상자성 전이 · 국소모멘트 변화 · 스핀–격자 동역학은 *자기상태 인지 데이터 + 에너지 · 힘 · 자기관측량 각각의 검증* 필요. 권하는 시험 = 고정 기하에서 자기배열 간 DFT 에너지차 비교 + 각 상태 안에서 변위 뒤 국소모멘트 · 힘 확인. 공선 bcc Fe 시연은 비공선 · 유한온도 스핀 무질서의 예측 정확도를 세우지 않는다.

### 5.9 §4.1 전지 전해질 — 용매화 동역학에서 계면 반응까지 (`Fig. 7`)
- 응용을 세 검증 요구로 묶는다: **긴 동역학 샘플링** (전지 · 고체전해질) · **PES 미분 민감 물성** (강유전 전이 · 포논 · 열수송) · **저배위 · 왜곡 환경으로의 전이** (결함 · 표면 · 계면).
- 액체 전해질 (Wang 2026): §3h. `Fig. 7a–c` = 배위수명 ↔ 수송. *"These correlations indicate that coordination dynamics provide a useful microscopic descriptor of transport behavior, although conductivity also depends on viscosity, carrier concentration and electrolyte composition."* — 짝 digest `wang2026_domain_oriented…` 가 이 원전을 전문 판독했다 (리뷰 재인용 수치 2,300 · 91 · 160,000 · 13,000 · 0.005 eV/atom · 0.16 eV/Å 가 그 digest §3 과 일치함을 대조했다).
- c-LLZO (Gao 2025): ns MD · 대형 셀 · 시험 온도에서 D · Arrhenius 경향 재현 (`Fig. 7d,e`). 확산 통계 · 장벽은 독립 검증 (He 2018) 필요 · Ea 가 같다는 것만으로 장거리 몫을 분리 못 함.
- **Du 2025**: Li₃YCl₆ · Li₆PS₅Cl 에서 사전학습 퍼텐셜을 에너지 · 힘 · 포논 · 탄성 · Li 확산으로 평가 — *"one diffusion curve cannot validate disorder, lattice response and transport across electrolytes."* (리뷰는 숫자를 옮기지 않았다.)
- **Li 금속/황화물 계면**: 재구성이 전하 재분배와 수송을 결합 (Cheng 2017 QM 반응동역학 인용) · Gao 의 13,760 원자 Li₃PS₄/Li 반응 MD 는 *구조 · 유효전하 재조직*까지만 지지한다.

### 5.10 §4.2 상전이와 포논 — PES 고차 물성 시험 (`Fig. 8`, `Table 5`)
- 강유전 전이 = 집단 변위 + 국소 쌍극자 → 자유에너지차 · 장거리 정전 · 분극에 민감. BaTiO₃ (Gao): R–O–T–C 순서 재현, 전이온도 ≈145 · 205 · 285 K (실험보다 낮음) — 순서 재현 ≠ 정량.
- 같은 순서를 **다른 길로도** 재현: Chen (MACE-MP-0 를 BaTiO₃ DB 로 미세조정 · 4 상 + 포논 비교) · Eggestad (on-the-fly · XC 의존) ⇒ *"because they are different protocols, they cannot alone isolate a long-range module as the cause of success."*
- **포논** = PES 2 차 미분 시험. Loew: ~10,000 ab initio 포논 · 최대 진동수 · 진동 엔트로피 · 헬름홀츠 자유에너지 · 열용량 · 포논 DOS · 평균 음속 → *"models that excel in energy and force prediction can still yield substantial errors in phonon and dynamical stability predictions."*
- ★ **두 오차 기구를 분리하라**: ① 부정확하지만 **보존적인** 퍼텐셜 → 틀린 Hessian ② **직접힘** 모델 → 추가로 *비적분성 · 에너지–힘 불일치* (Bigi 2025). 혼동행렬은 분류 결과일 뿐 어느 기구인지 말하지 않는다. MACE-MP-0 · MatterSim-v1 은 PBE-안정을 안정으로 잘 판정 · ORB · eqV2-M 은 PBE-안정을 불안정으로 자주 판정.

### 5.11 §4.3 결함 · 표면 · 열수송 (`Fig. 9`)
- 결함 · 표면 = 저배위 · 강왜곡 환경 → 흔한 학습 분포 밖일 수 있다 · 열수송 = 진동 동역학 + 비조화 힘.
- CHIPS-FF (탄성 · 포논 · 결함 형성 · 표면 · 계면 · 비정질) · GRACE 등의 열수송 · 포논 · 탄성 = 미분 정확도 · 수치 안정 · 다체 응답을 찌른다.
- `Fig. 9` = 단원소 SIA · 빈자리 형성에너지 — *"direct evidence for static point-defect formation energies in that benchmark set, but it does not by itself establish performance for migration barriers, surfaces, grain boundaries, amorphous structures, or thermal transport."*
- 표면: Focassio — MACE · CHGNet · M3GNet 의 **즉시사용 (out-of-the-box) 표면에너지 한계** → 표면 특화 샘플링 · 열수송: Póta — Wigner 열전도 워크플로에서 언제 미세조정이 필요한지. ⇒ *"each observable requires its own reference and protocol."*

### 5.12 §5 과제 · 전망 (Box 2) · §6 결론
Box 2 의 설계 차원 넷 (현 한계 → 미래 우선순위):

| 차원 | 현 한계 | 우선순위 |
|---|---|---|
| 배치 범위 · 참조 충실도 | 큰 데이터도 가용 DFT 수준 · 평형 근처에 치우칠 수 있다 — 범위와 라벨 충실도는 따로 평가 | 표적 비평형 샘플링 + 참조 수준 감사 + 조건부 multifidelity |
| 화학 범위 · 도메인 적응 | 넓은 화학 범위 ≠ 전문 도메인의 과제 정확도 | 적용 영역 보고 · **zero-shot / 미세조정 / domain-oriented 를 같은 검증 규약으로 비교** |
| 국소 효율 · 비국소 물리 | 국소 cutoff 가 정전 · 분극 · 전하평형을 빠뜨릴 수 있다 | 필요한 곳에 비국소 물리 · 전역 결합 전하 응답 보존 · 관련 응답 관측량 + 통제 비교로 기여 검증 |
| 벤치 지표 · 응용 신뢰성 | 전역 · 리더보드 지표가 장시간 MD 안정 · 포논 · 결함 · 계면을 예측 못 함 | 과제 지향 벤치 + **보정된 불확실도** + **갱신 뒤 재검증** |

미래 과제 i–vi: **i)** 라벨 · multifidelity — 다른 전자구조 수준의 데이터를 *"should not simply be pooled as if they defined an identical PES"* (에너지 기준 일관 · fidelity 조건화 / 겹침 / 델타학습 + 독립 고충실 과제 검증) · **ii)** 단일계 미세조정 → 다계 연속학습 (갱신마다 보존 측정 · 참조 설정 변화는 multifidelity 로) · **iii)** 장거리 물리 ↔ 비용 (증류 · 다중스케일 · 적응형 비국소 활성화도 전역 정전 일관 · 매끄러움 · 에너지 보존 유지) · **iv)** 공정 벤치 · UQ · 폐루프 — 위원회 · 앙상블 · 예측분산은 *"should be calibrated against known prediction errors before they are used to trigger relabeling or local fine-tuning, and they should be revalidated after model updates"* · **v)** 해석가능성 — 모델 유래 특징을 독립 섭동시험 · 고수준 계산 · 실험 없이 물리 기구로 취급하지 말 것 · **vi)** 툴체인 통합 — 참조 수준 · 적용 경계 · 검증 절차 · 불확실도를 명시 기록.
결론: *"reliability remains task dependent and is jointly influenced by configurational coverage, label fidelity, model architecture, physical treatment, and application-specific validation."*

---

## 6. 논지 종합 — 세 병목과 처방

| 병목 | 원인 (리뷰의 서술) | 진단 | 처방 | 리뷰 자신의 단서 |
|---|---|---|---|---|
| ① PES softening | 평형 근처 위주 사전학습 → 비평형 · 고에너지 배치가 덜 묶임 (*plausible contributor*) | 힘 회귀/투영 **기울기 < 1** (`Fig. 4b,c`, `Table 2`) | 비평형 · 고힘 배치 의도 샘플링 · 표적 보정/미세조정 | 기울기 ≠ Hessian · 원인 유일하지 않음 · BaTiO₃ 에선 반대 (`Table 3`) · *독립 사후 시험*으로만 효과 인정 |
| ② catastrophic forgetting | naive 미세조정이 사전학습 분포를 잊음 | 사전학습 표본 (sMPtrj) 손실 · 탄성 · 포논 변화 · 비표적 D 오차 (`Fig. 5`) | replay · EWC · **reEWC** | 순차 · 다표적은 *초기 증거* |
| ③ 장거리 결손 | 국소 cutoff · 메시지 패싱 수용영역 한계 | 이량체 원거리 꼬리 · 장 응답 · 벌크모듈러스 (`Fig. 6`) | Latent Ewald · FIREANN · PQEq (+D3 따로) · 4G-HDNNP | 장거리 모듈의 *별도 기여*는 짝지은 ablation 으로만 · 힘 라벨만으론 장 응답 불확정 |

공통 문법: **"표의 숫자 하나가 다른 과제를 보증하지 않는다"** — *does not by itself establish* · *cannot alone* · *not a direct measurement* 계열 단서가 본문에 15 회 안팎 나온다 (R1 수정본이라 심사 대응으로 보인다).

---

## 7. 우리 UMA 관행 대조 ★★ (MLIP-MD 규율 · `db/properties/` · 결정 원장 기준)

> 우리 쪽 설정 (CLAUDE.md MLIP-MD 줄): **UMA-s-1p1, task `omat`** · Langevin NVT · dt 2 fs · friction 0.02 · 평형 5 ps / 생산 200 ps · **MSD 창 2–50 ps 고정** · 아레니우스 600/800/1000 K · σ = NE (Haven = 1) — **절대값 인용 금지 · 비율도 다중시드 판정만** · Ea 도 계 간 상대차만 (1저자 인용정책 2026-09-18). **UMA 는 Li₃N 에 사용 금지** (2026-06 결정론적 편향 판정 · `kb/projects/mlip_next_campaigns_2026_07.md`).

### 7a. 항목별 대조

| # | 리뷰의 지침 (절) | 우리 관행 (기록) | 판정 · 이유 |
|---|---|---|---|
| 1 | **관측량 → 필요 거동 → 관련 시험** 순으로 고른다 (§3.2) | UMA-s-1p1 omat = LPSCl MD 표준 — 근거 = 정적 힘 대조 2 건 + committee. 관측량 (σ · D · Ea) 은 상대차 · 다중시드로만 | **순서는 맞다.** 단 '관련 시험'이 **정적 힘에 머문다** — LPSCl 에 대한 UMA-MD ↔ DFT-AIMD 확산 대조는 우리 기록에서 **못 찾았다** (`kb/results` · `db/properties` 에서 UMA 와 AIMD 를 함께 담은 파일을 훑음: 'AIMD' 라벨이 실은 UMA MLIP-MD 라는 정정 줄 (`kb/results/ionic_conductivity_synthesis_comp1_modelc.md` 등) 과 b₂o₃ 의 'AIMD 는 범위 밖' 판정 (`b2o3_md_arrhenius.json`) 만 있었다) |
| 2 | softening 진단 = **원점 통과 투영 기울기**, pooled + **상위 10 %** (§2.2, `Table 2`) | **같은 식** (`bench_against_dft.py::_softening_slope` · `mlip_committee.py` L343) · **원소별 분해**까지 낸다 · **상위 10 % 부분집합 기울기는 안 낸다** · Li₃PS₄ 벤치 (08-19) 기록에는 기울기 자체가 없다 | 식 일치 ✓ · 우리가 한 칸 더 (원소별), 리뷰가 한 칸 더 (고힘 부분집합) — 고힘 칸은 기존 출력으로 공짜 (§12-②) |
| 3 | CI = 프레임 상관을 고려한 **블록 부트스트랩** (§2.2) | 소셀 대조 = **10 프레임 · 단일 시드 · CI 없음** (원장 허용 서술이 그 단서를 박는다) | 10 프레임은 블록 부트스트랩이 성립하지 않는 규모 — **단서 문구로 대신한 것은 정직한 선택**. 999 프레임급 외부 데이터면 CI 를 낼 수 있다 (§12-①) |
| 4 | **참조 범함수를 힘 오차와 같이 기록** · 다른 범함수 시험의 차이를 재료 탓으로 못 돌림 (§2.1, `Table 3` 단서) | Li₃PS₄ 벤치 = **PET-MAD PBEsol 라벨** vs UMA omat (**PBE**) · a-Li₄PS₄Cl 소셀 = **QE/PBE (USPP/PSL)** vs OMat24 PBE (PAW) → 절대에너지 비교 안 함 · 힘 · 상대에너지만 (`lpscl_smallcell_uma_qe_force_estimand_2026_09_16.json` §3) | 소셀은 일치 ✓ · **Li₃PS₄ 30.0 meV/Å 에는 PBEsol ↔ PBE 차가 섞여 있다** — comparison J-1 은 'PBEsol 라벨' 을 적었지만 그 *효과* (기울기 > 1 쪽 편향 가능 · §3b 가설) 는 단서 목록에 없다 |
| 5 | 정적 힘 결과는 이완 · 전이 · 포논 · 확산 · 장시간 MD 를 보증 안 함 (`Table 3` 뒤 단서) | J-1 단서 ① (응력 안 잼) ② (장벽 안 잼) · σ 절대값 금지 · Ea 상대차만 · '소셀 검증 조성' 표지의 영구 단서 (`D-2026-09-18-lpscl-smallcell-production-scope`) | **일치 ✓ — 우리가 더 엄격** (인용정책이 숫자를 막는다; 리뷰는 문장 단서뿐) |
| 6 | 미세조정은 **망각 인지** (replay · EWC · reEWC) + 갱신 뒤 재검증 (§3.1, Box 2) | **미세조정 안 함** (동결 UMA) | 해당 없음. ⚠ 도입하면 우리 UMA 는 LPSCl 밖 (Li₂S · Li₃PS₄ · B₂O₃ · Nd · 점착 계면) 에도 쓰이므로 **'좁은 표적 하나'가 아니다** → `tompa2026` 의 'naive 가 최선' 조건에 안 맞고 이 리뷰의 reEWC 쪽 조건에 가깝다 (§12-③) |
| 7 | **장거리 정전 · 분산 · 분극** — 국소 cutoff 가 빠뜨릴 수 있고, 모듈 기여는 짝지은 ablation 으로만 (§3.3) | UMA = 국소 메시지 패싱 (우리 소셀 카드가 적은 문헌 cutoff 6.0 Å) · omat 라벨에 D3 없음 → **점착 W 는 UMA + 외부 D3(BJ) 가산**, D3 항은 QE 출력 (같은 끝점) 으로 정의 (`D-2026-09-26-wad-aprime-amend-1-d3-from-qe`) · 헤드라인 2 체 · ATM 따로 (`D-2026-09-23-wad-d3-twobody-atm-separate`) · 벌크 MD 는 D3 없이 | **가산형 분산 = 리뷰가 PQEq 틀에서 설명한 '분산은 따로' 설계와 같은 분리 ✓.** 벌크 LPSCl 확산에서 장거리 결손의 몫은 **미측정** — 리뷰 재인용 c-LLZO 사례는 장거리 유무 Ea 차 0.002 eV (그림 인쇄값) 로 작았지만 *다른 계*다 |
| 8 | 전극 · 반응 계면: 전하상태 · 경계조건 명시 · 재분배 ≠ 산화환원 (§3.3, §4.1) | 계면에서 UMA 는 점착 · 자리 판독 위주 · Li‖LPSCl 반응 해석은 문헌 (`lai2025` HAML · `kim2026_li_argyrodite…` MTP) | 같은 방향 ✓ — UMA 로 계면 *반응 기구*를 귀속하지 않는다 |
| 9 | 자성: 위치만 받는 퍼텐셜은 기하당 에너지 하나 · 상관 물질은 U · 자기배열 · 국소전자 처리가 참조를 바꾼다 (§2.1, §3.4) | Nd 자리 UMA 판독 (`ndo_site_uma_rietveld_readout_2026_10_15.json`, CEI 트랙) | ⚠ 그 기록에서 **OMat24 의 Nd 라벨 처리 (4f · PAW 선택 · 자기상태) 를 적은 줄을 못 찾았다** (키 전수 · '4f' · 'PAW' · 'OMat24' · 'magnet' 0 회) — 확인 거리 (§12-⑥) |
| 10 | 속도 · 파라미터 수는 체크포인트 · 하드웨어 · 프로토콜에 묶인다 · 툴체인은 참조 수준을 명시 기록 (§3.2, `Table 4` 각주, §5 vi) | 캠페인마다 fairchem 판을 적는다 (기록에 2.19.0 · 2.21.0 · 2.22.0 이 보인다) · li2s 카드는 turbo/default 모드를 추측하지 않고 읽는다 · 옛 kb 문서의 'AIMD' 가 UMA-MD 였다는 라벨 정정 줄 | 일치 ✓ — `Table 4` 의 UMA t_ASE 를 우리 GPU 시간 견적에 쓰지 않는다 · 라벨 정정은 리뷰 vi 의 '참조 수준 명시 기록'과 같은 문제를 이미 겪은 흔적 |
| 11 | 화학 범위 ≠ 과제 정확도 (Box 2) | **Li₃N 에 UMA 금지** · LPSCl 계열은 검증 표준 | 같은 원리 ✓ — UMA 원논문 부록 G 가 1.1 의 omat 를 결합영역 밖 비물리적이라 적은 것과 함께 (`uma2026` §11) |
| 12 | UQ 는 알려진 오차로 보정한 뒤 재라벨 트리거로 · 갱신 뒤 재검증 (§5 iv) | committee (`mlip_committee.py`) | 우리 committee 가 '알려진 오차에 보정' 단계를 갖는지는 **이 digest 에서 확인하지 않았다** — UQ 축 정본은 `carrete2023` · `kurniawan2025` · `grasselli2025` digest |

### 7b. 숫자를 나란히 놓을 때 — **같은 식 · 다른 시험셋 (순위 아님)**

| 출처 | 모델 | 시험셋 · 참조 | 성분 MAE | RMSE | 투영 기울기 |
|---|---|---|---|---|---|
| **우리** `mlip_bench_li3ps4_uma.json` | UMA-s-1p1 omat | PET-MAD Li₃PS₄ test 243 구조 · **PBEsol** · 16–64 원자 | **0.02997 eV/Å** (Li 0.01319 · P 0.0368 · S 0.04085) | 0.04458 | 기록 없음 |
| **우리** `lpscl_smallcell_gb3_result_2026_09_18.json` | UMA-s-1p1 omat | a-Li₄PS₄Cl **120 원자** · **QE/PBE** · 10 프레임 (융체 3 · 담금질 경로 4 · 300 K 유리 3) · 단일 시드 | — | **0.0390 eV/Å** | **전체 0.9836** · S 0.9785 · P 0.9766 · Cl 1.0104 · Li 1.0149 |
| 리뷰 `Table 2` | Orb-v3 cons-inf-**OMat** | Li₆PS₅Cl 52 원자 AIMD 600 · 1000 K · **PBE** · 999 배치 | **0.031557** | — | 0.9810 (고힘 0.9926) |
| 리뷰 `Table 2` | MatterSim-1M | 〃 | 0.070544 | — | 0.9871 (0.9983) |
| 리뷰 `Table 2` | SevenNet-0 | 〃 | 0.103519 | — | **0.8438** (0.8740) |
| 리뷰 `Table 2` | MACE-MP-0 medium | 〃 | 0.126277 | — | 0.7791 (0.7625) |
| 리뷰 `Table 2` | CHGNet 0.3.0 | 〃 | 0.207538 | — | 0.6269 (0.6759) |

- 우리 소셀 원장의 허용 서술 그대로 (`lpscl_smallcell_closed_2026_09_18.json` §2 — li2s 트랙 · 외부 1저자 비준 09-18 · 인용범위 확정 09-19):
  ① *"UMA 는 a-Li₄PS₄Cl **120 원자** 비정질 셀에서, 지정 QE/PBE 참조 대비 힘 RMSE **0.0390 eV/Å** · 상대 에너지 MAE **0.55 meV/atom** 이다 (단일 시드 · 10 프레임)."*
  ③ *"오차는 균일하지 않다 — S·P(PS₄ 골격)의 RMSE 가 Cl·Li 보다 약 5 배 크고, softening 기울기의 **부호가 갈린다**(S 0.9785 · P 0.9766 무름 / Cl 1.0104 · Li 1.0149 단단)."* — ⛔ 보고이지 게이트가 아니다 · ⛔ 다른 조성 · 다른 DFT 설정으로 이식 금지.
- **읽는 법**: 우리 UMA 의 전체 기울기 (0.9836) 는 리뷰 `Table 2` 의 **비평형 데이터 학습 무리 (OMat24 의 Orb-v3 0.981 · 자체 능동학습의 MatterSim 0.987)** 에 놓이고 MPtrj 계열 (0.63–0.84) 과는 떨어져 있다 — **두 독립 지표가 같은 방향** (비평형 배치를 많이 본 보존력 모델은 이 황화물 국소환경에서 계통 감쇠가 작다). ⛔ 그러나 **계 · 참조 · 온도 · 크기가 다 다르다** → *"UMA 가 Orb-v3 와 같다/낫다"* 는 이 표로 못 말한다. 리뷰 자신이 Li₆PS₅Cl ↔ BaTiO₃ 사이에서도 같은 경고를 했다.
- MAE 와 RMSE 를 섞지 않는다 (우리 소셀 = RMSE · 리뷰 = 성분 MAE).

### 7c. 우리 원장의 빈칸을 이 리뷰가 채우는 곳
1. **comparison J-1 단서 ③ — *"Cl 이 없다 … 아르지로다이트 · Cl 무질서로의 전이를 이 벤치가 보증하지 않는다"***: 리뷰 `Table 2` 의 시험셋 (Kim 2026 Zenodo, Li₆PS₅Cl · 4a/4c 50 % 교환 한 배치 · PBE AIMD) 이 **바로 그 빈칸의 공개 데이터**다. 리뷰는 UMA 를 안 돌렸다 → 우리가 같은 999 배치에 UMA 를 대면 **같은 식 · 같은 시험셋**으로 리뷰 표 안에 우리 엔진을 놓을 수 있다 (§12-①).
2. **`talks/lee2026_skku…` §12 의 10 번 — *"softening 을 잰 수치가 없다"* · *"'평형 근처 편중' 진단이 결정적이라면 더 좁게 학습한 쪽이 먼저 무너졌어야 한다"***: 사전학습 SevenNet-0 (MPtrj — 더 좁은 학습) 의 Li₆PS₅Cl 투영 기울기 **0.8438 (고힘 0.8740)** vs 비평형 데이터 학습 무리 (Orb-v3 · MatterSim) ≈ 0.98–0.99 — **힘 기울기로는 '좁게 학습한 쪽이 더 무르다'** 는 첫 외부 수치다 (리뷰 자체 계산). 단 그 talk 의 관찰 (초가열–급랭 통과) 은 *구조적 붕괴* 라는 다른 지표이고, 그 talk 의 엔진은 *미세조정된* SevenNet 이다 — 이 값으로 talk 의 주장을 검증하지는 못한다. 참고로 `park2024_sevennet_parallel_gnn_md` 의 SevenNet-0 시험셋 힘 MAE 0.070 eV/Å (MP 결정 test) 대비 이 Li₆PS₅Cl AIMD 에선 0.1035 (정의 대조 전 · 약 1.5 배).
3. **"UMA sulfide PES softening" 알리바이 철회 (`kb/results/uma_force_accuracy_li3ps4_2026_08_19.md`)**: 리뷰 `Table 2` 는 Li₆PS₅Cl 에서 softening 이 **MPtrj 학습 체크포인트**의 이야기라는 정황을 준다 — 우리 철회 판정과 같은 방향의 외부 정황 (UMA 자체 증거는 아니다).

---

## 8. Post-processing ★

- **무엇**: 성분 MAE · RMSE · 상위 10 % |F_DFT| 부분집합 MAE · **원점 통과 힘 투영 기울기** Σ(F_DFT·F_pred)/Σ|F_DFT|² · 95 % CI (블록 부트스트랩 / 배치 부트스트랩, 짝 추첨) · Matbench F1 · DAF · precision · κSRME · SRME · ΔE (MAE) · 혼동행렬 (TS/FU/TU/FS) · 바이올린 분포 · NE σ · 배위수명 · MSD (log–log, 기울기 1 안내선) · Arrhenius Ea ± 오차.
- **도구**: 리뷰 자체 대조의 스크립트 · 예측값은 **미공개** · 데이터 출처만 명시 (Zenodo · Materials Cloud). 인용 연구의 도구: DeepMD-kit (Wang) · ASE / LAMMPS (속도) · GPUMD (NEP).
- **수치화 · 플롯 · 기록**: 표는 소수 6 자리 + CI 괄호 (`Table 2` 는 600 K · 1000 K · pooled 를 한 칸에 겹쳐 적어 읽기 어렵다) · 그림은 `Fig. 1` (자작 개념도) 을 빼고 전부 원전에서 'Adapted from' · `Fig. 9` 아래 범위 단서 상자는 리뷰 문체와 같아 리뷰가 덧붙인 것으로 보인다 (추정).
- **우리가 가져올 기록 양식**: ① 기울기를 **pooled + 상위 10 %** 둘로 ② CI 를 **프레임 상관 블록**으로 ③ **참조 범함수 · 시험셋 출처 · 사전학습 겹침 여부 (검증/미검증)** 를 표 캡션에 같이.

---

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나 · 실제로 본 것) | 우리 활용 |
|---|---|---|
| 1 | 리뷰 구성도 — ① Dataset Construction → ② Model Construction → ③ Training and Fine-Tuning → ④ Evaluation and Benchmarking → ⑤ Physics Enhancement → ⑥ Applications (Batteries/Electrolytes · Interfacial Reactions · Ferroelectrics Phase Transitions) | 리뷰 지도. ④ 칸이 'Regression errors (E/F/σ) · Stability classification (F1/DAF) · Phonons/defects/surfaces/thermal transport' (여기 σ 는 응력) 인데 **'diffusion' 칸이 없다** — 우리가 제일 많이 쓰는 관측량이 평가 목록에 없다 |
| 2 | AGNI 4 단계 (Huan 2017 각색) — Step 1 DFT Calculations → Step 2 Fingerprinting → Step 3 Clustering & Sampling → Step 4 Machine Learning → FORCE FIELD | 개념도 · 수치 없음 |
| 3 | MP-ALOE vs MatPES 주변분포 (Kuner 2025) — (a) 응집에너지: MatPES 봉우리 figure-read ≈ 0.30 @ ≈ −4 eV/atom, MP-ALOE 는 ≈ 0.23 으로 넓고 덜 음수 쪽 · (b) 힘 크기 0–5 eV/Å: MP-ALOE 가 < 0.3 eV/Å 와 꼬리에 더 · (c) 압력: 둘 다 0 GPa 봉우리, MP-ALOE 만 −50…+90 GPa 날개 (밀도 figure-read ≈ 0.003–0.005) | 압력 날개 = 응력 학습 범위. 우리 cascade 부피 편향 · 셀 정책 문제 (J-1 단서 ①) 는 **응력** 축이라 이런 분포가 직접 관련 — 단 리뷰 캡션대로 1 차원 분포는 특정 배치군 포함을 증명하지 않는다 |
| 4 | (a) DFT PES vs uMLFF PES 개념도 — 노랑 = 평형 근처 학습점 · 빨강 = 비평형/고에너지 후보 · 'possible softening' · 'targeted sampling' (*illustrative*) · (b) mp-973966 고에너지 상태 힘 대각 산점도, 축 −6…6 eV/Å — 기울기 / MAE / cMAE (그림 인쇄값) **M3GNet 0.820 / 0.220 / 0.184 · CHGNet 0.851 / 0.190 / 0.162 · MACE-MP-0 0.871 / 0.174 / 0.154** · (c) WBM 1000 화합물 기울기 바이올린 (0–2): 1 아래 비율 **93.0 · 98.1 · 96.5 %** (위 7.0 · 1.9 · 3.5 %), 분포 중심 figure-read ≈ 0.75–0.85 | **softening 진단의 원형** — 우리 기울기와 같은 계열 지표. cMAE (기울기 보정 뒤 MAE) 가 MAE 의 ≈ 84–89 % — 감쇠를 고쳐도 오차 대부분은 남는다 (우리 산수). ⚠ (b) y 축 제목에 ')' 가 하나 더 붙은 조판 흠 |
| 5 | reEWC (Kim 2026) — (a) 총손실 vs epoch (0–400) — 캡션 정의: 총손실 = E RMSE (eV/atom) + F RMSE (eV/Å) + 0.01 × S RMSE (kbar) 의 **숫자 합** (단위가 섞인 a.u.): sMPtrj (실선) 400 epoch figure-read ≈ **Vanilla 1.20 · Layer freezing 1.00 · Lower LR 0.99 · EWC 0.87 · Replay 0.68 · reEWC 0.58** (SevenNet-0 기준 ≈ 0.57) · FT 셋 (점선) ≈ 0.32 → 0.05–0.17 (layer freezing 이 제일 높게 ≈ 0.16) · (b) SevenNet-0 로부터 파라미터 MAD: 400 epoch ≈ **Vanilla 0.108 · Replay 0.105 · reEWC 0.056 · Lower LR 0.042 · EWC 0.034 · Layer freezing ≈ 0.001** · (c) 손실 보존비 vs 섭동 크기 (10⁻⁵…10⁰): 무작위는 10⁻² 에서 ≈ 0.93 · 10⁻¹ 에서 ≈ 0.25 · 10⁰ 에서 ≈ 0 / **FIM 인지**는 10⁻¹ 까지 1.0 · 10⁰ 에서 ≈ 0.77 | ⭐ **그림에서만 보이는 것**: 파라미터를 *얼마나* 움직였나 (MAD) 와 *얼마나 잊었나*가 비례하지 않는다 — Replay 는 Vanilla 만큼 움직이고도 덜 잊고, Layer freezing 은 거의 안 움직이고도 많이 잊는다 ⇒ **'어느 파라미터'가 '얼마나'보다 중요** ((c) 와 같은 말). 우리가 UMA 를 미세조정할 날의 설계 근거 |
| 6 | PQEq 분극 장거리 모델 (Gao 2025) — (a) Na–Na · Na–Cl 이량체 상호작용 에너지 vs 거리 (1.8–5.5 Å): Na–Cl 우물 figure-read ≈ DFT −4.15 eV @ 2.4 Å / 장거리 모델 −3.7 / 장거리 뺀 모델 −2.5 · Na–Na ≈ −0.7 / −0.4 / −0.5 eV · 삽입도 (3.5–12.5 Å): Na–Cl 꼬리가 12 Å 에서도 0 에 안 닿는다 · (b) 물 분자 전기장 응답 (±0.41 V/Å): DFT ≈ −4.8 meV · 모델 ≈ −6.0 meV · QEq ≈ 0 (평탄) · (c–e) 벌크모듈러스 예측 vs 참조 (0–450 GPa): R² 0.93 / 0.94 / 0.94 · MAE **13.54 / 12.98 / 13.08 GPa** (그림 인쇄값, Reuss / Voigt / VRH) | 장거리 결손의 생김새 (원거리 이온쌍 꼬리). ⚠ 장거리 모델도 우물 깊이를 ≈ 0.4 eV, 장 응답을 ≈ 25 % 틀린다 (figure-read) — 리뷰는 크기를 말하지 않는다. **벌크모듈러스 MAE ~13 GPa 는 데이터셋 평균** — 연한 황화물은 상대오차가 훨씬 클 수 있다 ⇒ 우리 탄성은 DFT 로 (`uma2026` 의 '탄성은 UMA 로 재지 않는다' 판정과 같은 결론) · ⚠ 범례 *'Our model'* 은 Gao 의 모델이다 (리뷰 저자 것 아님) |
| 7 | (a) LiFSI/FAN: τ(Li⁺–FAN) figure-read ≈ 3 → 23 ps · τ(Li⁺–FSI⁻) ≈ 9 → 71 ps (10³/T 3.0 → 4.9) · σ_exp ≈ 44 → 12 · **σ_MLMD ≈ 62 → 6 mS cm⁻¹** · (b) σ vs 배위가중 평균수명 τ̄ (0–1000 ps), 4 전해질 · 빠른 교환 / 전이 / 리간드 유지 음영 · (c) 약용매화 → 강용매화 개념도 · (d) c-LLZO D vs 1000/T (0.4–2.0 K⁻¹): AIMD · 장거리 모델 · 장거리 뺀 모델 — Ea **0.258 ± 0.017 / 0.261 ± 0.006 / 0.263 ± 0.006 eV** (그림 인쇄값), 모델 두 선이 AIMD 보다 위 (figure-read ≈ 1.2–1.5 배) · (e) 모델 MSD vs τ (log–log, 10⁰–10³ ps), 800–1800 K, 기울기 1 안내선 — 800 K 는 ≈ 10–20 ps 뒤 기울기 1 (figure-read ≈) | ⭐ **(a) 의 계통 추세** — σ_MLMD/σ_exp 가 ≈ 1.4 (333 K) → ≈ 0.5 (≈ 202 K): MLMD 의 온도 의존이 실험보다 가파르다 (= 겉보기 Ea 과대). 리뷰는 *"compared with experiment"* 라고만 쓴다 → **우리 σ 절대값 비인용 규율의 근거 하나 더** (`wang2026_domain…` §10-7 은 다른 전해질 (LiPF₆/EC-EMC) 에서 반대 방향 교차를 기록했다 — 원전 그림 5a 로 이 LiFSI/FAN 교차를 재확인할 것). (d) = Ea 는 맞고 D 는 평행이동 — `alghamdi2026` 의 'D₀ 쪽 오차' 와 같은 꼴 (부호 · 계는 다름). (e) = 우리 MSD 창 (2–50 ps) 을 log–log 기울기로 검산하는 양식 |
| 8 | 포논 오차 바이올린 (Loew 2025) — (a) Δ최대진동수 [K] (−400…250): M3GNet · CHGNet · MACE-MP-0 · SevenNet-0 중심이 음수 (figure-read ≈ −70 · −60 · −30 · −20 K = 무름), MatterSim-v1 ≈ 0 으로 가장 좁음, ORB · eqV2-M 은 넓고 크게 음수, PBEsol ≈ +20 K · (b) Δ엔트로피 · (c) Δ자유에너지 · (d) Δ열용량 · (e) ΔDOS · (f) Δ평균음속 — 전 패널에서 ORB · eqV2-M 이 가장 넓다 | ⭐ **softening 의 포논판**: MPtrj 계열 넷의 Δ최대진동수가 한쪽 (음수) 으로 쏠림 = `Fig. 4` 의 힘 기울기 < 1 과 같은 방향. 직접힘 모델 (ORB · eqV2-M) 의 폭 = 에너지–힘 불일치 기구 (§5.10). 우리 UMA-S 는 **보존적** (`uma2026` §3.1) |
| 9 | 단원소 점결함 벤치 (GRACE 원논문) — (a) SIA: E_SIA-SRME 최선 GRACE-2L-OAM-L ≈ 0.08 … 최악 MatterSim ≈ 0.31 · ΔE_SIA ≈ 0.23–0.72 eV · (b) 빈자리: SRME 최선 SevenNet-MF-ompa ≈ 0.14 … 최악 MatterSim ≈ 0.49 · ΔE_vac ≈ 0.09–0.34 eV (figure-read ≈) · 빨강 = GRACE · 그림 아래 범위 단서 상자 (13 BCC + 13 FCC 금속 · PBE) — **UMA 없음** | ⭐ **그림에서만 보이는 것 둘**: ① 같은 계열에서 **-omat (OMat24 단독) 판이 -ompa / -oam 판보다 빈자리 SRME 가 나쁘다** (SevenNet-MF 0.24 vs 0.14 · ORBv3 0.39 vs 0.22 · MACE 0.31 vs 0.21 · GRACE-2L 0.23 vs 0.195, figure-read ≈ — 단 SIA 에서는 이 패턴이 일관되지 않고, OMat 단독인 eSEN-30M-OMat 은 ΔE_vac 가 오히려 최저 ≈ 0.09 eV) ② **ORBv3-cons-inf-omat 은 여기서 뒤에서 둘째**인데 `Table 2` (Li₆PS₅Cl 힘) 에서는 **1 등** — 과제가 바뀌면 순위가 뒤집힌다. 원인 (OMat24 라벨 설정 ↔ 벤치 PBE 참조 불일치? 데이터 분포?) 은 리뷰에 없다 — **우리 omat task 에 대한 직접 증거는 아니다** (UMA 부재) |
| Table 1 | Matbench Discovery 부분표 (Ref. 36) — §3d | 옛 스냅숏 · 'MAE 낮음 ≠ 분류 좋음' 예시 |
| Table 2 | ★★ **Li₆PS₅Cl AIMD 고정 배치 힘 — 다섯 체크포인트 (자체)** — §3a | **우리 기울기 식과 동일** · J-1 단서 ③ 의 빈칸을 채울 공개 시험셋 · UMA 없음 |
| Table 3 | BaTiO₃ PET-MAD test split 힘 (자체) — §3b | 범함수 불일치 혼입 경고의 실례 (우리 Li₃PS₄ 벤치도 PET-MAD PBEsol) |
| Table 4 | F1 · κSRME · 속도 (GRACE 원논문) — §3e | UMA-S-1.1 F1 0.916 · κSRME 0.203 · 401 μs/atom/step — **우리 처리량 견적에 쓰지 않는다** |
| Table 5 | 동역학 안정성 혼동행렬 (Loew 2025) — §3f | PBEsol ↔ PBE 불일치 바닥선 · 직접힘 모델의 불안정 과대예측 |

---

## 10. 비판 — 이 리뷰의 약한 곳 ★

① **자체 대조에 UMA · eSEN · GRACE · SevenNet-MF · MACE-MPA 가 없다.** OMat24 학습 대표가 Orb-v3 하나뿐 (MatterSim 은 자체 능동학습 데이터) 이라, `Table 2` 의 '감쇠 대 비감쇠' 대비는 사실상 **MPtrj 학습 (옛) 대 대규모 비평형 데이터 학습 (새)** 의 대비이기도 하다 — 리뷰는 이 교란 (학습 코퍼스) 을 이름 붙이지 않고 '체크포인트 의존' 으로만 말한다.
② **재현 불가 요소** — 예측값 · 스크립트 미첨부 (본문 명시) · 패키지 판 · 정밀도 · 장치 · 이웃목록 설정 미기재 · 사전학습 겹침 미검증 (본문 명시). 데이터 출처는 공개라 *다시 잴* 수는 있다.
③ **Li₆PS₅Cl 시험셋이 좁다** — 52 원자 한 셀 · 음이온 배치 하나 (4a/4c 50 % 교환) · 두 온도 · 같은 첫 프레임에서 나온 연속 AIMD 프레임 (그래서 블록 부트스트랩을 썼다). 실온 · 결함 · 표면 · 계면 없음. CI 가 좁은 것 (예: Orb pooled MAE ±0.00015) 은 *표본 오차*가 작다는 뜻이지 일반화 폭이 아니다 — 리뷰도 그렇게 단서를 달았다.
④ **표가 서사를 다 지지하지 않는다** — 다섯 중 넷에서 **고힘 기울기가 pooled 보다 1 에 가깝다** (§3a). *"평형 근처 학습 → 고에너지 배치에서 무름"* 이라는 §2.3 의 그림 (`Fig. 4a`) 과 이 데이터의 모양은 다르다. 리뷰는 이 점을 짚지 않는다.
⑤ **BaTiO₃ 의 기울기 > 1 해석이 열려 있다** — PBE 학습 체크포인트 × PBEsol 라벨의 범함수 불일치가 그 자체로 > 1 을 만들 수 있다 (§3b 가설 — 리뷰에 없음). 그러면 *"Li₆PS₅Cl attenuation is not a general result"* 의 일부는 재료가 아니라 참조 탓이다. 리뷰는 '재료 탓으로 단정 못 함' 까지만 말한다.
⑥ **두 리더보드 스냅숏을 화해시키지 않는다** — `Table 1` (옛 · 'MACE' 0.669 · 'ORB MPtrj' 0.765) 과 `Table 4` (새 · 'MACE-MPA-0' 0.852 · 'ORB-v3' 0.906) 를 같은 리뷰에 싣고 판 · 시점 차이를 설명하지 않는다. `Table 4` 의 ORB-v3 (MatBench-compatible 줄) 와 `Table 2` 의 Orb-v3 OMat 도 같은 체크포인트라는 보장이 없다.
⑦ **원전 자기 벤치의 틀이 그대로 들어왔다** — `Table 4` 와 `Fig. 9` 는 GRACE 원논문 값이고 (빨강 강조 · LAMMPS 시간은 GRACE 만), 리뷰는 *"source-study benchmark"* 라고 적긴 했다. UMA 의 t_ASE (우리 산수 ≈ 2.4 step/s) 와 UMA 원논문의 16 step/s 사이의 ≈ 6.6 배 차는 언급이 없다.
⑧ **빌린 그림의 범례** — `Fig. 6` · `Fig. 7d` 의 *"Our model"* 은 Gao et al. 의 모델이다. 리뷰 안에서는 오해를 부른다.
⑨ **`Fig. 7a` 의 계통 추세 무언급** — σ_MLMD 의 온도 의존이 실험보다 가파르다 (≈ 1.4 → 0.5 배, figure-read ≈). 수송 주장에서 제일 중요한 부분인데 본문은 *"compared with experiment"* 한 마디다.
⑩ **응력 · 부피 · EOS 를 자체 시험에서 안 다룬다** — 평가 목록에는 *"energy, force and stress regression errors"* 가 있지만 자체 대조는 힘뿐이다. NPT MD · 셀 이완 (우리 cascade 부피 편향의 축) 에 대해선 이 리뷰가 줄 근거가 없다. 장시간 MD 안정성 (NVE 표류 · dt · 열욕) 도 '중요하다' 는 말뿐 지표가 없다. `Fig. 1` 의 평가 칸에 '확산' 이 없는 것도 같은 결손이다.
⑪ **가장 가까운 SE 벤치를 한 문장으로 넘겼다** — Du 2025 (Li₃YCl₆ · Li₆PS₅Cl · 에너지 · 힘 · 포논 · 탄성 · 확산) 의 숫자가 하나도 없다.
⑫ **reEWC 증거는 한 그룹 · 한 아키텍처** — Kim 2026 은 SevenNet 계보 (같은 저자군: Park · Hwang · Han — ref 16 과 ref 20 대조) 이고 SevenNet-0 에서만 시험했다. MoLE (UMA) 같은 다른 구조로의 일반성은 미검증. MPE 부호 규약도 리뷰에 없다.
⑬ **수치 문턱이 없다** — 'task-specific validation' 을 수십 번 요구하지만 *얼마면 충분한가* (기울기 · MAE · 시험셋 크기) 는 한 번도 주지 않는다. Box 2 는 일반론이다. 우리 사전등록 문턱 관행 (예: 소셀 카드 F_RMSE ≤ 0.15 eV/Å · 상대 E MAE ≤ 15 meV/atom) 과 비교하면 **처방이 아니라 체크리스트**다.
⑭ (형식) R1 수정본이라 단서 문구가 매우 많다 — 읽기엔 정직하지만 인용할 '주장' 이 적다. 인용은 §13 의 원문 문장 단위로.

> **그림 ↔ 본문 대조 결과**: **본문과 어긋난 그림은 없었다** (캡션 · 범례 · 본문 수치 일치 확인 — `Table 2` 본문 범위 0.031557–0.207538 · 고힘 0.0378–0.4298 · 고힘 기울기 다섯 값 · `Fig. 7` 패널 기호 · `Fig. 4c` 비율 표기 모두 일치). 대신 **본문이 말하지 않는 것이 그림 · 표에 있었다** — ④ (고힘 기울기 방향 · 표) · ⑨ (`Fig. 7a` 추세) · `Fig. 9` 의 -omat 패턴과 Orb-v3 순위 반전 · `Fig. 5b` 의 MAD–망각 비례 깨짐 · `Fig. 6a,b` 의 장거리 모델 자체 오차 크기 · `Fig. 1` 평가 칸의 '확산' 부재.

---

## 11. 우리 원장 매핑 (요약표)

| 리뷰 항목 | 우리 원장 · 도구 · 결정 |
|---|---|
| 투영 기울기 지표 | `tools/mlip/bench_against_dft.py::_softening_slope` · `tools/ionic/mlip_committee.py` (L343, 원소별) |
| 우리 UMA 힘 실측 (정적 · 외부 라벨) | `db/properties/mlip_bench_li3ps4_uma.json` · `kb/results/uma_force_accuracy_li3ps4_2026_08_19.md` · comparison **J-1** |
| 우리 UMA 소셀 대조 (QE/PBE) | `db/properties/lpscl_smallcell_gb3_result_2026_09_18.json` · `lpscl_smallcell_closed_2026_09_18.json` (허용 서술 ①③) · `D-2026-09-16-lpscl-smallcell-uma-qe-force` · `D-2026-09-18-lpscl-smallcell-production-scope` |
| UMA ↔ PBE 압력–부피 모델 검증 (li2s · 잠정) | `db/properties/lpscl_smallcell_glass_model_check_estimand_2026_10_19.json` · `D-2026-10-19-lpscl-smallcell-glass-model-check` (**proposed**) — 리뷰의 '과제 수준 검증' 을 *부피*로 하는 우리 사례 (값은 이 digest 에 옮기지 않는다) |
| 분산 가산 (UMA + D3) | `D-2026-09-23-wad-d3-twobody-atm-separate` · `D-2026-09-26-wad-aprime-amend-1-d3-from-qe` · `D-2026-10-01-wad-se-pairs-uma-card` |
| 수송 인용 규율 | CLAUDE.md MLIP-MD 줄 · 1저자 인용정책 2026-09-18 · `D-2026-09-27-barrier-hop-count` |
| 화학별 금지 | UMA × Li₃N 금지 (2026-06 · `kb/projects/mlip_next_campaigns_2026_07.md`) |
| 엔진 사양 | `papers/uma2026_family_of_universal_models_for_atoms.md` (보존력 · 부록 G · 속도 조건) |

---

## 12. 적용 인사이트 ★

① ⭐⭐ **같은 자 · 같은 시험셋으로 UMA 를 리뷰 `Table 2` 안에 놓을 수 있다 (제안 · 사용자 결정).** Kim 2026 Zenodo 의 Li₆PS₅Cl AIMD 999 배치에 UMA-s-1p1 omat 를 단일점으로 대고 `bench_against_dft.py` 로 성분 MAE · pooled/고힘 기울기 · 원소별 분해를 내면, **DFT 0 회 · GPU 단일점 1 천 회 규모**로 comparison J-1 단서 ③ (Cl · 아르지로다이트 음이온 무질서 부재) 을 닫는 첫 외부 수치가 된다. ⚠ 던지기 전에 **보고량 카드** (CLAUDE.md 계산 규율): 참조 DFT 설정 (원전 확인) · 52 원자 셀 (통상 a ≈ 9.8–9.9 Å · 리뷰 미기재) 이 우리 소셀 카드의 하드 기준 (L/2 > cutoff 6 Å) 에 못 미친다는 점 → '같은 주기 셀 대조' 로만 읽는다 · 사전학습 겹침 미검증 단서 · 결과 전 문턱.
② ⭐ **우리 벤치 출력에 '상위 10 % |F_DFT| 기울기 · MAE' 칸을 더하고, 기울기와 MAE 를 늘 같이 보고한다.** 기존 배열에서 공짜다. MatterSim 사례 (기울기 0.987 · MAE 2.2 배) 가 '기울기 ≈ 1 = 정확' 이 아님을 보인다. 덤으로 **Li₃PS₄ 벤치를 기울기와 함께 다시 내면** §3b 의 범함수 불일치 가설 (PBE 모델 × PBEsol 라벨 → > 1) 을 우리 데이터로 바로 시험한다. ⚠ 도구 수정이면 CLAUDE.md 코드 규율대로 selftest (음성 포함) + 과거 마감 재현 (소셀 0.9836 이 그대로 나오는지).
③ **미세조정을 도입할 날의 설계 조건** — 우리 UMA 는 LPSCl 밖 (Li₂S · Li₃PS₄ · B₂O₃ · Nd · 점착 계면) 에도 쓰이니 '좁은 표적 하나' 가 아니다 ⇒ `tompa2026` (좁은 표적이면 naive 최선) 보다 이 리뷰의 reEWC 쪽 조건에 가깝다 · 카드에 **보존 시험** (사전학습 분포 표본 손실 · 탄성/포논 · 비표적 계 D) 을 결과 전 문턱과 함께 넣는다. `Fig. 5b` 가 보여 주듯 '파라미터 이동량' 은 보존의 지표가 못 된다.
④ **속도 · 파라미터 수는 프로토콜에 묶어서만 쓴다** — `Table 4` 의 UMA-S t_ASE (≈ 2.4 step/s 환산) 와 UMA 원논문 16 step/s 는 6.6 배 다르다. 우리 GPU 견적은 우리 기계 실측으로.
⑤ **계면 서술의 상한** — 리뷰의 *"partial charges are model variables rather than a direct measurement of electron flow"* · *"Assigning redox pathways … would require specified boundary conditions and independent phase or electronic-structure validation"* 은 우리 Li‖LPSCl · CEI 계면 UMA 결과를 **구조 서술**에서 멈추게 하는 외부 근거로 쓸 수 있다.
⑥ **Nd 자리 UMA 판독의 라벨 감사 (확인 거리 · CEI 트랙 · 사용자 결정)** — 리뷰 §2.1 · §3.4 의 '상관 물질 · 국소전자 처리 · 자기상태가 참조를 바꾼다' 에 해당한다. OMat24 의 Nd 라벨 처리를 확인하고 그 기록에 한 줄 남기는 것을 권한다 (지금 기록에서 못 찾음 — §7a-9).
⑦ **원고 문장 근거** — 우리가 'UMA 소셀 검증 조성' 표지를 쓸 때 *universality ≠ validation breadth* 를 이 리뷰 문장으로 외부 인용할 수 있다 (§13).

---

## 13. 인용 가능 문장 (영문 · 원문 그대로 또는 근거 명시 초안)

- (원문) *"In this review, universality refers to the chemical and structural scope covered by a potential, including elemental, compositional, and configurational diversity, whereas foundation-model status emphasizes large-scale pretraining and adaptability to downstream tasks. Validation breadth and computational deployability are treated as separate dimensions rather than criteria defining universality."*
- (원문) *"Accordingly, universality describes model scope, whereas validation breadth describes how extensively that scope has been tested."*
- (원문) *"A force-regression slope below one diagnoses aggregate force underprediction; it is not a direct measurement of the Hessian or PES curvature."*
- (원문) *"These static-force results do not establish accuracy for structural relaxation, ferroelectric transitions, phonons, diffusion, long-time model-driven dynamics, or other systems."*
- (원문) *"A learned potential approximates the potential-energy surface specified by its training labels, so the exchange-correlation approximation and calculation settings are part of its applicability domain."*
- (원문) *"A useful selection order is to specify the observable, then the required model behavior, and finally a relevant test."*
- (우리 원고용 초안) *"Following the frozen-checkpoint protocol of Wang et al. (Phys. Scr. 2026), we report the zero-intercept force-projection slope, Σ(F_DFT·F_pred)/Σ|F_DFT|², together with the force error against our own DFT reference."* — ⚠ 우리 값은 원장 허용 서술 (§7b) 만.
- ⛔ 쓰면 안 되는 문장: *"Wang et al. benchmarked UMA on Li₆PS₅Cl"* (UMA 없음) · *"Orb-v3 and UMA show the same softening slope"* (다른 시험셋) · `Table 4` 속도로 우리 처리량 서술.

---

## 14. 주의 / 한계 (인용 규율)

- **Accepted Manuscript** — VoR 에서 쪽 · 표 번호가 바뀔 수 있다. 인용은 DOI 로 · 숫자는 VoR 가 나오면 재대조.
- **엠바고** — 12 개월 동안 재배포 불가 (CC BY-NC-ND 4.0 은 그 뒤). litdb 크롭은 내부 열람용 — 발표 덱 · 외부 공유에 그림을 쓰지 않는다.
- **리뷰 재인용 수치** (§3c–§3h) 는 원전 확인 전 — 원고에는 원전으로 인용.
- **`Table 2` · `Table 3` 은 자체 계산이지만 미공개 스크립트** — 우리 값과 같은 표에 놓을 때는 '같은 식 · 다른 시험셋' 단서를 필수로 (§7b).
- **물성 4 축 금지** — 이 편에서 우리 계 (comp1 · modelc · +B₂O₃ · LPSOCl) 로 옮길 값은 0 이다.
- figure-read 값은 300 dpi 크롭 해상도 안에서 한 눈금 단위로 읽었다.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 (한 단계씩) |
|---|---|
| **uMLFF / uMLIP** | 범용 기계학습 힘장 — 주기율표 대부분의 원소 · 구조를 한 모델로. 이 리뷰는 MLFF, 우리는 MLIP 라고 부른다 |
| **foundation model** | 대규모 사전학습 + 하류 과제에 적응 (미세조정) 하는 모델. universality (범위) 와 다른 축 |
| **PES softening** | 모델 PES 가 DFT 보다 '무른' 것 — 힘 · 곡률 · 장벽을 계통적으로 작게 냄. 결과: 장벽 과소 → D 과대 · 포논 진동수 과소 |
| **투영 기울기** | Σ(F_DFT·F_pred)/Σ\|F_DFT\|² — 예측 힘을 참조 힘 방향에 투영한 원점 통과 회귀 기울기. 1 보다 작으면 계통 감쇠. **산포 (MAE) 는 따로** 재야 한다. Hessian (곡률) 의 직접 측정이 아니다 |
| **cMAE** | 힘을 선형 재스케일 (기울기 보정) 한 뒤의 MAE — 계통 감쇠를 빼고 남은 무작위 오차 (`Fig. 4b`) |
| **고힘 부분집합** | \|F_DFT\| 상위 10 % 원자–프레임 쌍. 꼬리의 감쇠를 따로 본다 |
| **블록 부트스트랩** | 연속 MD 프레임은 서로 상관 → 프레임 하나씩이 아니라 **연속 블록** (여기선 12 프레임) 으로 재표집해 CI 를 낸다. 순환 (circular) = 끝과 처음을 이어 블록을 만든다 · 온도층화 = 온도별로 따로 뽑는다 |
| **catastrophic forgetting** | 새 데이터로 미세조정하면 옛 분포에서 성능이 무너지는 현상 |
| **EWC** | Elastic Weight Consolidation — Fisher 정보행렬로 '옛 과제에 중요한 파라미터' 를 재서 그 이탈에 벌점 |
| **FIM** | Fisher Information Matrix — 파라미터를 흔들 때 손실이 얼마나 민감한가의 척도 |
| **experience replay** | 미세조정 중 옛 데이터 (여기선 MPtrj 10 %) 를 섞어 다시 보여 줌 |
| **reEWC** | replay + EWC 결합 (Kim 2026) |
| **MAD (파라미터)** | 미세조정 모델 파라미터가 기저 모델에서 평균 얼마나 떨어졌나 (`Fig. 5b`) — 망각과 비례하지 않는다 |
| **Matbench Discovery · WBM** | 원소 치환으로 만든 미지 구조 (WBM) 의 hull 안정 여부를 맞히는 전향적 벤치 |
| **F1 · DAF** | F1 = precision 과 recall 의 조화평균 · DAF = precision ÷ 시험셋의 안정 비율 (무작위보다 몇 배 잘 고르나) |
| **κSRME / SRME** | 대칭 상대 평균오차 — κSRME 는 열전도도 (103 이원계), E_SIA / E_vac-SRME 는 결함 형성에너지 |
| **conservative vs direct force** | 보존력 = 에너지를 미분해 얻은 힘 (에너지 보존 · 일관). 직접힘 = 힘을 따로 예측 (빠르지만 비적분 가능 → 포논 · 열수송 · NVE 에서 문제). UMA-S/M 은 보존, UMA-L 은 직접 (`uma2026`) |
| **MoLE · 활성 파라미터** | Mixture of Linear Experts — 총 파라미터는 크지만 구조마다 섞인 일부만 계산에 쓰인다 (UMA-M 1.4 B / ~50 M) |
| **multifidelity · delta learning** | 다른 정확도 (PBE · r2SCAN …) 라벨을 한 모델에 — 단순 합치기 대신 fidelity 를 조건으로 주거나 차이 (Δ) 만 학습 |
| **Latent Ewald** | 국소 기술자에서 숨은 '전하 같은' 변수를 배워 Ewald 역공간 합으로 장거리 상호작용 |
| **PQEq · core–shell** | 분극 가능 전하평형 — 배치마다 전역 결합 전하를 풀고, 껍질 변위로 분극을 표현 |
| **FIREANN** | 외부 전기장에 반응하는 임베딩을 가진 신경망 퍼텐셜 |
| **4G-HDNNP** | 4 세대 고차원 신경망 퍼텐셜 — 환경 의존 전기음성도 + 전역 전하평형으로 비국소 전하 이동 |
| **NE (Nernst–Einstein) · 교차상관** | 자기확산계수로 σ 를 환산 — 이온–이온 상관 (교차항) 을 빼므로 Haven 비 = 1 가정. 우리도 같은 가정이라 σ 절대값을 인용하지 않는다 |
| **배위수명 τ** | Li⁺ 와 특정 리간드의 배위가 유지되는 평균 시간 — 짧을수록 빠른 교환 |
| **혼동행렬 TS/FU/TU/FS** | PBE 안정을 안정 (TS) / 불안정 (FU) 으로, PBE 불안정을 불안정 (TU) / 안정 (FS) 으로 판정한 비율 |

---

## 16. 짝 digest · 후속 확보 후보

**짝 digest (겹치는 곳 — 그 파일들은 고치지 않았다)**
- `uma2026_family_of_universal_models_for_atoms` — 우리 엔진 사양서. 이 리뷰가 UMA 에 대해 말한 것 (MoLE · 1.4 B / ~50 M · `Table 4` 값) 은 전부 거기 더 자세히 있다. 속도 조건 차 (§3e) 는 여기서만 짚었다.
- `petmad2026_lightweight_universal_interatomic_potential_mad` — 리뷰 `Table 3` 의 BaTiO₃ 시험셋 출처 (PET-MAD 배포) = 우리 Li₃PS₄ 벤치의 출처와 같은 배포. 비보존력 경고 (그 digest §11) 는 `Table 5` · `Fig. 8` 의 ORB · eqV2-M 과 같은 줄기 (Bigi 2025 = 이 리뷰 ref 74).
- `wang2026_domain_oriented_universal_machine_learning_potential` — `Fig. 7a–c` 의 원전 (ref 54). 리뷰의 재인용 수치가 그 digest 와 일치함을 대조했다. `Fig. 7a` (LiFSI/FAN) 의 σ 교차 (§9) 는 그 digest 에 적혀 있지 않다 — 원전 그림 5a 로 재확인할 것.
- `talks/lee2026_skku_mlip_materials_design` — §12 의 10 번 'softening 수치 없음' 빈칸 ↔ 이 리뷰 `Table 2` 의 SevenNet-0 기울기 (§7c-2). talk 은 citable=no · 방향은 이쪽 → talk 참조뿐.
- 미세조정 축: `tompa2026_finetuning_mlip_foundation_strategies` (같은 Li₆PS₅Cl 표적 · '좁은 표적이면 naive 최선 · 넓게 쓸 거면 replay' — 이 리뷰 reEWC 와 **조건으로 갈라 읽으면 모순 아님**) · `liu2026_finetuning_umlip_tutorial` · `alghamdi2026_finetuning_strategies_li_diffusion_mace` (D 오차가 D₀ 에 실린다 ↔ `Fig. 7d`) · `zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill` (평균이 좋아도 장벽은 틀린다).
- 선정 · 지도: `chang2026_performance_based_mlip_selection_sse` (argyrodite 직접 벤치 · UMA 없음 · 그 digest 의 ref 52/53 짝 = 학습 범함수가 σ 를 크게 가른다 → 이 리뷰 §2.1 '라벨 충실도' 의 argyrodite 실례 · ref 52 = 이 리뷰 ref 77 과 같은 JACS 2025 편) · `phuthi2026_mlip_ssb_perspective` (원소별 softening 은 우리 쪽이 더 세분) · `makino2026_mlip_battery_materials_review` (Du 2025 를 추천 목록 5 번으로) · `dutra2025_atomistic_modelling_ml_se_review` · `park2024_sevennet_parallel_gnn_md` (SevenNet 원전 = ref 16).
- UQ: `carrete2023_deep_ensembles_vs_committees` · `kurniawan2025_comparative_ensemble_uq_nnip` · `grasselli2025_uncertainty_era_ml_atomistic` (리뷰 §5 iv 의 '보정된 UQ').
- 계면 반응 MD: `lai2025_haml_li_metal_lpscl_interface_doping_seFO` · `kim2026_li_argyrodite_sei_reactive_md` (리뷰의 Li₃PS₄/Li 13,760 원자 사례와 같은 질문의 다른 방법).

**후속 확보 후보 (litdb 에 digest 없음 · 우선순위)**
1. **Kim J. et al., *npj Comput. Mater.* 12, 26 (2026)** — reEWC · SevenNet-0 → Li₆PS₅Cl · 126 argyrodite · D 비교 + **Zenodo `10.5281/zenodo.15686940`** (리뷰 `Table 2` 시험셋 = §12-① 의 재료).
2. **Du H. et al., *ACS Mater. Lett.* 7, 3403 (2025)** — Li₃YCl₆ · Li₆PS₅Cl 에서 사전학습 uMLIP 평가 (`makino2026` 도 추천).
3. **Deng B. et al., *npj Comput. Mater.* 11, 9 (2025)** — softening 원전 (`Fig. 4`).
4. **Gao R. et al., *Nat. Commun.* 16, 10484 (2025)** — PQEq 분극 장거리 파운데이션 · Li₃PS₄/Li 13,760 원자 · c-LLZO.
5. **Loew A. et al., *npj Comput. Mater.* 11, 178 (2025)** — 포논 벤치 (`Fig. 8`, `Table 5`).
6. Bigi F. et al., PMLR 267 (2025) — 비보존력 · Lysogorskiy Y. et al., *npj Comput. Mater.* 12, 114 (2026) — GRACE (`Table 4`, `Fig. 9`) · Kim J. et al., *JACS* 147, 1042 (2025) — multifidelity.

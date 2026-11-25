# An AI-Ready Fine-Tuning Framework for Accurate Machine-Learning Interatomic Potentials in Solid–Solid Battery Interfaces — Liu et al. (arXiv 2026, **preprint**)

> slug `liu2026_ai_ready_finetuning_solid_solid_interfaces` · arXiv **2601.17847v1** [cond-mat.mtrl-sci], **25 Jan 2026** · DOI `n/a (preprint)` · type `MLIP (fine-tuning 방법론) + 실험 보조(EIS/AFM/XRD)` · PDF `a9f742ec-94._An_AIready_finetuning_framework…pdf` · digested `2026-09-09` · status ✅
> elements: Li, Na, Sb, S, P, Cl, B, O, C, F, Ga, La, Zr, Ta, Nb
> methods: DFT, MLIP, MD, elastic

> **저자 (표지 그대로 · 공동1저자 3인)**: **Xiaoqing Liu**†‡, **Xinyu Yu**¶§, **Yangshuai Wang**∥ (이상 equal contribution), Zhe-Tao Sun¶§, Zedong Luo‡, Kehan Zeng‡, **Teng Zhao\***⊥‡#, **Shou-Hang Bo\***¶@, **Zhenli Xu\***†
> † SJTU 수학과 MOE-LSC/CMA-Shanghai · ‡ SJTU–충칭 인공지능연구원 · ¶ SJTU Future Battery Research Center · § SJTU Global College · ∥ **NUS 수학과** · ⊥ SJTU 자연과학연구원 · # SOG AI-Technology Co. Ltd. · @ SJTU 화학화공
> 교신: `zhaoteng_sjtu@sjtu.edu.cn` · `shouhang.bo@sjtu.edu.cn` · `xuzl@sjtu.edu.cn`

---

## 0. ⚠ 이 digest 를 읽기 전에 — 세 가지 경고

### 0-1. **동료심사 안 됐다**
arXiv v1 (2026-01-25) 이고 저널 게재 표시가 없다. 본문 21 pp 중 **참고문헌이 8 pp** 다.
⇒ 이 편의 수치·주장은 **peer review 를 통과하지 않았다**. 우리 원고에서 인용할 때
"preprint" 를 명시하거나, 게재본이 나올 때까지 **방법론 참조로만** 쓴다.

### 0-2. **SI 를 우리는 못 봤다** — 그런데 우리가 제일 알고 싶은 게 거기 있다
본문이 SI 로 미룬 것: **S.1 FIRE 프레임 상세 · S.2 데이터셋 생성 · S.3 MD 상세 · S.4 실험**.
우리에게 온 PDF 21 pp 는 **본문 + 참고문헌뿐이고 SI 가 없다**(네트워크 차단으로 arXiv 원본도 못 받았다).
⇒ ★★ **1저자가 물은 "계면 구조를 어떻게 만드나"(격자 정합·변형률·표면 종단·배향·분리거리)는
본문에 단 한 줄도 없다.** 전문 검색 결과: `strain` 0 · `lattice` 0 · `termination` 0 · `slab` 0 ·
`vacuum` 0 · `supercell` 0 · `mismatch` **1회(서론의 동기 문장뿐)**.
**이 편은 그 답을 주지 않는다.** 아래 §7-1 에 항목별로 적었다.

### 0-3. 형제편과의 분담 — **중복 서술 금지**
같은 그룹의 튜토리얼 편 **`liu2026_finetuning_umlip_tutorial`** (*J. Appl. Phys.*, 48 pp) 이
동시에 digest 되고 있다. **fine-tuning 일반론**(왜 파인튜닝인가 · 어느 층을 얼거나 푸나 ·
catastrophic forgetting · 하이퍼파라미터 · 파운데이션 모델 개관)은 **그쪽이 정본**이다.
이 digest 는 **이 편에만 있는 것**만 깊게 판다:

| 이 편에만 있는 것 | 튜토리얼 편으로 넘김 |
|---|---|
| **FIRE = replay + PCA/K-means 표본추출**의 구체 레시피 | fine-tuning 이 무엇인가 · 전이학습 일반론 |
| **6개 배터리 고체-고체 계에서의 실측 RMSE 표** (Fig. 2) | MACE 아키텍처 설명 |
| **데이터 크기 스캔**(100→4000 프레임) + **시간비용** (Fig. 3) | 학습률·에폭·손실함수 일반 지침 |
| **σ·E·ν 실험 대조 + MD 시간 스케일링** (Fig. 4) | 파운데이션 모델 목록·벤치마크 |

---

## 1. 한 줄 요약

**MACE-MP-0 를 배터리 고체-고체 계면 6종에 파인튜닝하는 레시피(FIRE = Fine-tuning with
Integrated Replay and Efficiency)** 를 제안한다. 두 부품이 전부다 — ① **replay**(에폭마다
사전학습 데이터를 부분표집해 task 데이터와 같이 먹여 catastrophic forgetting 억제) +
② **효율 표본추출**(20–50 구조로 만든 pre-fine-tuned 모델 → MD 로 ~20,000 구조 생성 →
SOAP 서술자 → PCA → K-means 로 대표 구조만 추림). 결과는 **에너지 RMSE < 1 meV/atom,
힘 RMSE ~20 meV/Å** 로, 기존 보고 대비 한 자릿수 개선을 **기존 데이터의 10 %** 로 달성.
🔴 **그러나 검증은 전부 *벌크* 물성이다 — 계면 물성(접착일·계면저항·계면 Li 이동)은 한 건도 없다.**

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 문제 | 고체-고체 계면은 (a) 결함·전위로 **구조 다양성**이 크고, (b) 이종 화학결합이라 **화학공간 일반화**가 필요하고, (c) 전기-화학-역학 다물리 결합이라 단일 스케일로 못 푼다 |
| 갭 | from-scratch MLIP = 데이터 폭식 · U-MLIP(MACE-MP-0, CHGNet, EquiformerV2, MatterSim, DPA) = 범용성 대가로 **특정 계에서 정확도 하락** |
| 제안 | **task-specific fine-tuning + replay + 표본추출 자동화** |
| 백본 | **MACE-MP-0** (ref 17, Batatia 2023) — *"FIRE 는 개념상 일반적이고 다른 U-MLIP 에도 적용 가능"* 이라고만 씀 |
| 실험 층 | EIS(Nyquist + 등가회로) · **AFM 나노역학 맵**(Young's modulus) · XRD (Fig. S3) — SJTU Bo 그룹 자체 측정 |
| 자금 | NNSFC 12426304 / 12325113 / 22222204 / 22393902, STCSM 23JC1402300 외 |
| 이해상충 | 없음 선언. ⚠ 단 저자 1인(T. Zhao)이 **SOG AI-Technology Co. Ltd.** 소속 — "AI-ready" 프레이밍의 배경 |

---

## 3. 무엇을 계산했나 — **6개 계** (★ 1저자 질문 6)

| # | 계 | 저자의 분류 | 두 상이 진짜 붙어 있나 (Fig. 2A figure-read) | **우리 계와의 거리** |
|---|---|---|---|---|
| 1 | **Na / Na₃SbS₄** | 전극-전해질 | ✅ **결정-결정 급준 계면**. 위=Na 금속 정방격자, 아래=Na₃SbS₄ | ✖ Na 계 (우리는 Li) |
| 2 | **LiCl / GaF₃** | (전기)화학적 무질서 SE | ✅ 결정-결정 층상 | ✖ 우리 계 아님 |
| 3 | **Li₂CO₃ / LiF** | 음극 SEI | ⚠ **비정질/무질서 혼합** — 급준 면이 안 보인다 | △ SEI 화학 |
| 4 | **Li₃PS₄ / Li₃B₁₁O₁₈** | 복합양극 **코팅** | ⚠ **비정질-비정질** (원전 ref 45 = Wang/Aykol/Mueller *"amorphous–amorphous interfaces"*) | ⭕ **황화물 SE ‖ 붕산염 코팅 — 우리 B₂O₃ 축과 화학이 겹친다** |
| 5 | **Li / Li₆PS₅Cl** | 전극-전해질 | ⚠ 무질서. Li 금속 영역 + 성긴 SE 영역 | ⭕⭕ **우리 comp1 그 자체 + Li 금속 계면** |
| 6 | **Li₇La₃Zr₂₋ₓMₓO₁₂ (M=Ta,Nb)** | (전기)화학적 무질서 SE | ❌ **계면이 아니다** — 도핑된 가넷 **벌크** 한 상 | ✖ 산화물 SE |

🔴 **첫 번째 비판**: 초록은 *"Across six solid-solid battery interface systems"* 라고 쓰는데,
**저자 자신의 분류에서 2개(#2 LiCl/GaF₃, #6 LLZTO)는 "disordered solid electrolyte"** 이고,
#6 은 Fig. 2A 에서 봐도 **두 번째 상이 없다**. 실질 고체-고체 계면은 **4개**다.
⇒ *"6종 계면에서 검증됐다"* 를 그대로 인용하면 안 된다.

🔴 **두 번째 비판**: **우리 계(#5 Li/Li₆PS₅Cl)와 황화물 코팅(#4)이 하필 6종 중 성능이 제일 나쁘다.**
Fig. 2C 참조 — 아래 §5-2.

---

## 4. FIRE 가 정확히 무엇인가 — 세 부품 (Fig. 1)

Fig. 1 은 도식 3장이다. 실제로 보고 정리한다.

### 4-A. 파인튜닝 패러다임 (Fig. 1A)
위쪽 = from-scratch: 전체 데이터 → 파운데이션 모델 → 전 층 학습.
아래쪽 = fine-tuning: **학습된 가중치를 가진 층을 이식**(그림에 가위 아이콘)하고,
**앞쪽 = "Frozen non-trainable layers" / 뒤쪽 = "Task-specific trainable layers"** 로 나눈다.
⇒ **부분동결(partial freezing)** 이다. ⚠ 어느 층을 몇 개 얼렸는지 본문에 없다(SI S.2).

### 4-B. Replay-augmented continual fine-tuning (Fig. 1B) — **이 편의 핵심 신규성**
- 가로축이 **Epoch 1 → 2 → … → N**.
- **위에서 내려오는 파란 점선 = "Sub-sample"** — 매 에폭 **사전학습 데이터셋(MPtrj 등)에서 부분표집**.
- **아래에서 올라오는 주황 점선 = "Mini-batch"** — **task-specific data stream D₁, D₂, …, D_N**.
- 둘을 **같은 에폭에 섞어 먹인다** → catastrophic forgetting 억제 + 과적합 억제.

> 📌 **왜 이게 필요한가 (개념 한 단계)**: 파운데이션 모델은 수백만 구조에서 배운 "일반 감각"을
> 가지고 있다. 좁은 계면 데이터 4,000장만 계속 먹이면 그 일반 감각을 **잊는다**
> (catastrophic forgetting). MD 를 돌리다 보면 학습 분포 밖 배치가 반드시 나오는데, 잊어버린
> 모델은 거기서 폭주한다. Replay 는 매 에폭 원래 데이터를 조금씩 다시 보여줘서 그 감각을
> 붙잡아 둔다. 저자들이 *"stable and accurate MD"* 를 강조하는 이유가 이것이다.
> ⚠ **replay 비율(사전학습 : task 비)은 본문에 없다** — 이 방법의 유일한 핵심 하이퍼파라미터인데.

### 4-C. 효율 표본추출 (Fig. 1C) — **AI-ready 의 실체** (★ 1저자 질문 4)
그림의 화살표를 그대로 옮기면:
```
Foundation model  --[20-50 samples]-->  Pre-fine-tuned model  --[Run MD]-->  MD trajectories
                                                                                   |
                                                                              [Sampling]
                                                                                   v
Refined dataset  <--[Sampling]--  PCA + K-Means  <--  ~20,000 configurations
```
- **① 종잣값**: **perturbed configuration 20–50개**로 pre-fine-tuned 모델을 먼저 만든다.
  (왜? 생짜 U-MLIP 으로 MD 를 돌리면 복잡한 계면에서 궤적이 터진다 → *"significantly improves
  the stability and reliability of MD simulations"*.)
- **② 후보 풀**: 그 모델로 MD → **~20,000 구조**.
- **③ 압축**: **SOAP 서술자**(ref 40 Bartók 2013, DScribe ref 41) → **PCA** → **K-means 클러스터링**
  → 대표 구조만 뽑아 **refined dataset**.
- **④ 이름의 정체**: *"providing an **AI-ready dataset** for model fine-tuning"* 이라 쓰고
  **ref 42 (Feng 2023, 로봇 AI-Chemist multi-modal AI-ready database)** 를 단다.
  ⇒ **"AI-ready" 는 이 논문이 정의한 규격이 아니다.** 데이터 표준·스키마·API·라이선스 같은
  것은 **하나도 없다**. *"모델에 바로 먹일 수 있게 정제된 데이터셋"* 이라는 **수사(修辭)**에 가깝다.
  🔴 **우리가 이식할 "형식"은 없다. 이식할 수 있는 것은 파이프라인 순서뿐이다.**

### 4-D. **능동학습은 쓰지 않는다** (★ 1저자 질문 2)
전문 검색: `active learn` 1회 · `uncertain` 1회 — 둘 다 **결론의 미래과제 문장 한 곳**이다:
> *"In future work, **uncertainty-aware active learning protocols can be integrated with the FIRE**…"*

⇒ **FIRE 는 능동학습이 아니다.** one-shot 다양성 표본추출(K-means)이고, 불확실도·외삽등급·
위원회를 **전혀 쓰지 않는다**. 이건 `grasselli2025_uncertainty_era_ml_atomistic` 가 지적한
*"벤치마크가 불확실도를 거의 안 본다"* 의 교과서 사례다.

---

## 5. 결과 — 그림별 상세

### 5-1. Fig. 1 — 위 §4 에서 다 풀었다 (도식, 수치 없음)

### 5-2. Fig. 2 — 정확도 벤치마크 ★★ (**이 편의 알맹이**)

**Fig. 2A**: 6계의 원자배치 스냅샷 (위 §3 표에 판독 결과 정리).
**Fig. 2B**: 계마다 **F_MACE vs F_DFT 패리티 플롯**. 범례는 **Train(파란 원) / Valid(분홍 사각)** 둘뿐.
- 축 범위(figure-read): Na/Na₃SbS₄ ±10 · LiCl/GaF₃ ±6 · Li₂CO₃/LiF ±20 · Li₃PS₄/Li₃B₁₁O₁₈ ±20 ·
  **Li/Li₆PS₅Cl ±10** · LLZTO ±40 eV/Å.
- **figure-read**: 6장 중 **Li/Li₆PS₅Cl 패널의 산포가 눈에 띄게 크다**(다른 패널은 대각선에
  거의 붙어 있는데 이 패널만 분홍 사각이 양옆으로 벌어진다). 아래 RMSE 43 meV/Å 과 일치한다.
- 🔴 **독립 테스트셋이 없다.** Train / Valid 뿐이고, Valid 는 **같은 MD 궤적을 K-means 로 나눈 것**이다
  (SI 미확인이라 단정은 못 하지만 본문에 hold-out 선언이 없다). **같은 궤적에서 쪼갠 valid 는
  상관된 표본**이라 RMSE 를 낙관적으로 만든다.

**Fig. 2C**: 막대에 **숫자가 인쇄돼 있어 그대로 옮긴다** (figure-read 아님, 인쇄값):

| 계 | **E RMSE (meV/atom)** FIRE / Vanilla / Reference | **F RMSE (meV/Å)** FIRE / Vanilla / Reference |
|---|---|---|
| Na/Na₃SbS₄ | **0.34** / 0.71 / 15.66 | **18.56** / 23.23 / 61.92 |
| LiCl/GaF₃ | **0.10** / 0.12 / 1.00 | **18.28** / 22.41 / 70.00 |
| Li₂CO₃/LiF | **0.19** / 0.65 / 0.74 | **13.47** / 26.88 / 50.00 |
| **Li₃PS₄/Li₃B₁₁O₁₈** | **1.04** / 1.71 / 21.23 | **54.18** / 74.82 / 216.35 |
| **Li/Li₆PS₅Cl** | **0.86** / 1.29 / 5.45 | **43.02** / 55.47 / 93.90 |
| LLZTO (Zr₂₋ₓM₍ₓ₎) | **0.11** / 0.18 / 2.04 | **8.50** / 15.65 / 107.00 |

> `Vanilla` = replay 없는 순수 파인튜닝 · `Reference` = 문헌 기존 보고(ref 44,47,49–54; 상세는 Table S2)

🔴 **초록의 두 숫자가 자기 그림과 안 맞는다 — 이게 이 편의 가장 큰 과장이다.**
- 초록: *"root-mean-square errors in energy **below 1 meV/atom**"* → **Li₃PS₄/Li₃B₁₁O₁₈ = 1.04** (초과)
- 초록: *"in force **near 20 meV/Å**"* → **43.02 와 54.18** 이 있다. "near 20" 은 6계 중 **3계**뿐
  (18.56 / 18.28 / 13.47). 나머지는 **2–3배**다.
- ⚠ **그 두 낙제 계가 하필 황화물 두 계**, 즉 **우리 화학**이다.
  ⇒ ⛔ **"FIRE 를 쓰면 LPSCl 계면에서 20 meV/Å 을 얻는다" 는 인용 금지.**
     LPSCl 계면의 실제 보고값은 **43 meV/Å** 이다.

✅ **그래도 replay 는 진짜로 듣는다** — Vanilla 대비 FIRE 가 **6계 전부에서** 개선:
에너지 1.2–3.4배, 힘 1.2–2.0배. 이건 통제된 A/B(같은 데이터·같은 백본)라 신뢰할 만하다.
**이 편에서 가장 방어 가능한 결론은 "replay 가 있으면 없는 것보다 낫다" 다.**

### 5-3. Fig. 3 — 데이터 효율 ★★ (★ 1저자 질문 2·비용)

**Fig. 3A (Na/Na₃SbS₄ PCA)** — 회색 = ~20,000 전체 풀, 보라 = 선택된 n 프레임.
n = 500 / 1000 / 2000 / 4000. 축 −50…100 (PC1) × −75…100 (PC2), **V자 매니폴드**.
figure-read: **n=500 에서도 보라 점이 V 자 양쪽 끝까지 퍼져 있다** — K-means 다양성 선택이
의도대로 작동. 늘릴수록 밀도만 채워진다.

**Fig. 3B (LLZTO PCA)** — **클러스터가 3개**(왼쪽 초승달 + 중앙 큰 덩어리 + 우하단 덩어리).
figure-read 🔴: **n=500 에서 왼쪽 초승달이 거의 비어 있다.** n=2000 이 돼서야 채워진다.
⇒ **K-means 다양성 선택이 "덩어리 하나를 통째로 놓치는" 실패를 한다.** 캡션은
*"broader structural coverage with increasing dataset size"* 로 긍정적으로만 쓰는데,
같은 그림이 **작은 n 에서 특정 상(相)이 통째로 빠질 수 있다**는 것도 보여준다.
우리가 이 방법을 쓰면 **클러스터별 최소 할당(stratified) 을 강제해야 한다.**

**Fig. 3C (Na/Na₃SbS₄) / 3D (LLZTO)** — 각 3패널: E RMSE · F RMSE · 시간비용 vs 데이터 크기.
4개 곡선: **FIRE(빨강 ●) / Random(파랑 ■) / Scratch(노랑 △) / Vanilla(초록 ▽)**.

**Fig. 3C, Na/Na₃SbS₄ (figure-read ≈)**

| n (frames) | ~100 | ~200 | ~400 | 500 | 1000 | 2000 | 4000 |
|---|---|---|---|---|---|---|---|
| E RMSE FIRE | **0.86** | 0.30 | 0.17 | 0.16 | 0.16 | 0.17 | 0.14 |
| E RMSE Random | **0.42** | 0.24 | 0.26 | 0.18 | 0.19 | 0.155 | 0.145 |
| E RMSE Scratch | 1.93 | 1.05 | — | 0.85 | 0.63 | 0.27 | 0.23 |
| E RMSE Vanilla | — | — | ~0.9 | 0.30 | 0.25 | 0.22 | 0.19 |
| F RMSE FIRE | ~17 | — | — | 11 | 10 | 8.5 | 8 |
| F RMSE Random | ~19 | — | — | 11.5 | 10.5 | 9 | 8 |

🔴 **본문이 자기 그림과 어긋난다 (2건)**:
1. 본문: *"the FIRE yields the lowest RMSEs for both energy and force **across all data sizes**"*
   → **틀렸다.** n≈100 에서 **FIRE 0.86 > Random 0.42** 로 FIRE 가 **2배 나쁘다**.
   n≈2000 에서도 Random(0.155) < FIRE(0.17).
2. 본문: *"significantly outperforms … **random sampling**"*
   → Na/Na₃SbS₄ 에서는 **n ≥ 500 부터 FIRE ≈ Random**(4000 에서 0.14 vs 0.145, 힘은 8 vs 8 로 동일).
   **다양성 표본추출의 이득이 데이터가 늘면 사라진다.**

**Fig. 3D, LLZTO (figure-read ≈)** — 여기서는 FIRE 가 **깨끗이 이긴다**:

| n | ~100 | 500 | 1000 | 2000 | 4000 |
|---|---|---|---|---|---|
| E RMSE FIRE | 1.35 | 0.85 | 0.30 | 0.30 | **0.20** |
| E RMSE Random | 1.6 | 1.05 | 0.75 | 0.75 | 0.60 |
| E RMSE Vanilla | 1.7 | 0.75 | 0.70 | 0.65 | 0.60 |
| E RMSE Scratch | 8.7 | 5.9 | 4.75 | 3.3 | 2.2 |
| F RMSE FIRE | 33 | 21 | 20 | 19 | **16** |
| F RMSE Random | 46 | 35 | 35 | 30 | 25 |
| F RMSE Vanilla | 43 | 29 | 26 | 24 | 21 |
| F RMSE Scratch | 71 | 57 | 59 | 55 | 53 |

⇒ **정직한 결론: FIRE 표본추출의 이득은 계 의존적이다.** 구성공간이 단순한(V자 한 덩어리)
Na/Na₃SbS₄ 는 무작위로도 충분하고, **다상·다클러스터인 LLZTO 에서만 3배 이긴다.**
**우리 계(무질서 아르지로다이트 + 계면)는 후자 쪽**일 가능성이 높다 — 그게 이 편을 우리가
읽을 이유다. 단 **그 근거는 이 편의 LPSCl 계가 아니라 LLZTO 계에서 나왔다**는 걸 밝혀야 한다.

**Fig. 3C/D 오른쪽 — 시간비용 (log y, min)** ★ 1저자 질문 "비용"

| | n≈100 | 1000 | 2000 | 4000 |
|---|---|---|---|---|
| Fine-tuning (Na/Na₃SbS₄) | ~20 min | ~180 | ~600 | **~800 min (≈13 h)** |
| Sampling (Na/Na₃SbS₄) | ~0.15 | ~0.7 | ~1.5 | **~3 min** |
| Fine-tuning (LLZTO) | ~45 min | ~500 | ~800 | **~1100 min (≈18 h)** |
| Sampling (LLZTO) | ~0.1 | ~0.5 | ~1.0 | **~2 min** |

✅ **표본추출은 파인튜닝 비용의 0.3–0.4 % 다.** 저자 주장(*"sampling contributing only a minor
overhead"*) 은 그림이 뒷받침한다. **PCA+K-means 를 안 쓸 이유가 없다** — 공짜다.
🔴 **그런데 정작 제일 비싼 것이 표에 없다: DFT 라벨링 비용.** 4,000 프레임을 VASP 로 라벨하는
비용(수백 원자 계 × 4,000 SCF)은 파인튜닝 13 h 보다 **훨씬** 크다. **하드웨어(GPU 종류·개수)도
본문에 없다** (`GPU` 0회 · `A100` 0회). ⇒ 이 시간축은 **우리 예산 산정에 쓸 수 없다**.

### 5-4. Fig. 4 — 물성 검증 ★★★ (★ 1저자 질문 3 의 답이 여기 있다)

**Fig. 4A** (3행 × 3열): 왼쪽 = 최적화 구조, 가운데 = MSD, 오른쪽 = **실험 EIS Nyquist + 등가회로**.

| 계 | D (인쇄값) | σ_MLIP-MD | σ_EIS (실험) | MSD 창 (figure-read) | 편차 |
|---|---|---|---|---|---|
| **T-Na₃SbS₄** | 1.74×10⁻¹¹ m²/s | 0.14 mS/cm | **0.13** | **100–500 ps** | +8 % |
| **LLZTO** | 5.24×10⁻¹² m²/s | 0.24 mS/cm | **0.31** | **50–200 ps** | −23 % |
| **LPSCl** | 4.29×10⁻¹¹ m²/s | 0.75 mS/cm | **0.89** | **50–200 ps** | −16 % |

등가회로(3계 공통, 그림 인셋): `R1 – (R2‖CPE1) – (R3‖CPE2) – W1` (Warburg 종단).
Nyquist 축: Na₃SbS₄ 0–2200 Ω · LLZTO 0–8000 Ω · LPSCl 0–1200 Ω.

**검산 (우리가 직접 했다)**: LLZTO 패널에서 적합선이 t=50 ps 에 1.72×10⁻²⁰ m², t=200 ps 에
2.18×10⁻²⁰ m² → 기울기 3.07×10⁻¹¹ m²/s → **D = 기울기/6 = 5.1×10⁻¹² m²/s**, 인쇄값 5.24×10⁻¹² 과
**일치**. LPSCl 도 같은 방식으로 4.4×10⁻¹¹ ≈ 인쇄값 4.29×10⁻¹¹. ⇒ **MSD→D 사슬은 자기정합적이다.**

🔴 **그런데 D→σ 사슬은 맞지 않는다.** LPSCl 을 Nernst–Einstein(Haven=1, 300 K, a=9.86 Å,
24 Li/cell → n=2.5×10²² cm⁻³)으로 넣으면 **σ ≈ 67 mS/cm** 가 나온다 — 인쇄된 **0.75 mS/cm 의 89배**.
LLZTO 는 32배, Na₃SbS₄ 는 124배 어긋난다(계마다 배수가 다르다).
가장 그럴듯한 설명은 **MSD 를 고온에서 돌리고 σ 는 RT 로 아레니우스 외삽했다**는 것이다 —
실제로 **Fig. 4 캡션은 *"at relevant temperatures"*, 본문은 *"room-temperature MSD curves"* 로
서로 어긋난다.** **MD 온도가 본문 어디에도 없다.** 저자가 언급한 *"Haven-ratio correction"*
(ref 58–60)의 **값도 없다** — 참고로 우리 계열의 실측 H_R 은 **0.235–0.315**(adeli2019)라
방향이 반대(σ 를 **키운다**)여서 이 격차를 설명하지 못한다.
⇒ ⛔ **이 D 값들을 우리 표로 옮기지 마라.** 온도가 미상이라 우리 600 K 값과 비교 불가.

**figure-read (LPSCl MSD 패널)**: 적합 직선이 **약 160 ps 이후 실제 MSD(청록) 위로 벗어난다**
— 꼬리가 평평해지는데 직선은 계속 올라간다. 즉 **적합 창 안에서 MSD 가 선형이 아니다**.
그리고 **Fig. 4 전체에 오차막대가 하나도 없다 = 계당 궤적 1개**로 보인다.
(우리 규율: `modelc` 3-seed 600 K 에서 Ea 0.197±0.032 eV — **±16 % 산포**. 단일 궤적 σ 는
그만큼의 미표시 불확도를 안는다.)

**Fig. 4B — 기계적 물성** (막대 2개, figure-read ≈)

| 계 | E_FIRE (GPa) | E_실험(AFM) | 편차 | ν_FIRE | ν_Reference | 출처(ν) |
|---|---|---|---|---|---|---|
| T-Na₃SbS₄ | ≈ **31** | ≈ 28 | +11 % | 0.27 | 0.31 | ref 55 (⚠ **학회 포스터**) |
| LLZTO | ≈ **156** | ≈ 127 | **+23 %** | 0.26 | 0.26 | ref 56 (Yu 2016 *Chem. Mater.*) |
| **LPSCl** | ≈ **26** | ≈ 40 | **−35 %** | 0.34 | 0.37 | ref 3 (Chen 2024 *ACS Energy Lett.*) |

- 본문은 *"capture mechanical response with relatively high accuracy"* 라 쓰는데,
  **세 계 중 두 계가 20 % 이상 어긋나고 우리 계(LPSCl)가 −35 % 로 제일 나쁘다.**
- ⚠ **비교의 축이 서로 다르다**: E 는 **AFM 나노역학 맵의 공간평균**(로컬 접촉 강성 →
  Hertz/DMT 모델 의존, 다결정 펠릿의 기공·입계 포함)이고, ν 는 **"first-principle
  calculations"**(=문헌 계산값) 이다. **실험 E ↔ 계산 E** 는 같은 양이 아니다.
- ⚠ ν 의 Na₃SbS₄ 기준값이 **peer-reviewed 논문이 아니라 학회 포스터(ref 55)** 다.
  게다가 그 포스터 제목은 *"resistive switching memory devices for Neuromorphic Computing"*
  — 배터리 문맥이 아니다. **약한 앵커다.**

**Fig. 4C — MD 시간 스케일링** (log x = 원자수, y = s/step, y축 파단 있음)
- **MACE-MD**: 16 원자 ≈ 1.3 s/step → **3456 원자 ≈ 1.4 s/step** (사실상 평평)
- **VASP-MD**: 16 원자 ≈ 1.0 s/step → 576 원자 ≈ **195 s/step**, 그 이상은 메모리 한계
- **figure-read 🔴 16 원자에서는 VASP 가 MACE 보다 빠르다**(1.0 vs 1.3). 교차점은 대략 30–60 원자.
- 🔴 **1.3 s/step 은 MLIP 치고 느리다.** 2 fs × 100,000 step(200 ps) = **36 시간/궤적**.
  평평한 것은 "확장성이 좋다"가 아니라 **오버헤드가 지배한다**는 뜻이다(16 원자와 3456 원자가
  같은 시간). 하드웨어 미기재라 우리 UMA 처리량과 직접 비교 못 한다.

---

## 6. DFT / 계산 방법 ★ — **본문에 있는 게 거의 없다**

| 항목 | 본문 기재 | 비고 |
|---|---|---|
| **DFT 코드** | ⚠ **VASP** (단 1회, Fig. 4C 의 *"VASP-based MD"* 문맥) | 라벨 생성도 VASP 로 추정되나 **명시 없음** |
| functional (PBE/SCAN…) | ❌ **없음** (`PBE` 0회) | SI S.2 |
| pseudo / PAW | ❌ 없음 | SI S.2 |
| k-points / ecut / supercell / nat | ❌ **전부 없음** | SI S.2 |
| DFT+U | ❌ 없음 | 산화물 계(LLZTO)에 필요할 수 있는데 언급 없음 |
| **AIMD** | ❌ 생산 AIMD 없음. VASP-MD 는 **시간 벤치마크 전용** | |
| **MLIP 백본** | **MACE-MP-0** (ref 17) | ⚠ 버전(small/medium/large)·체크포인트 미기재 |
| **MLIP 학습** | replay 비율 ❌ · 동결 층수 ❌ · 학습률 ❌ · 에폭 수 ❌ · 손실 가중치 ❌ | **전부 SI S.2** |
| **MLIP-MD** | 앙상블 ❌ · 온도 ❌ · dt ❌ · thermostat ❌ · 시드 수 ❌ | 창 길이만 그림에서 읽힘(200/500 ps) |
| **무질서 처리** (SQS/enumerate/단일배열) | ❌ **없음** — LLZTO Ta/Nb 치환과 아르지로다이트 S/Cl 무질서를 **어떻게 배열했는지 안 적었다** | 우리 관심축 정면 |
| **계면 구조 생성** | ❌ **완전 부재** (§7-1) | SI S.1/S.2 |
| 표본추출 | SOAP(ref 40,41) + PCA + K-means | 하이퍼(σ, r_cut, n_max, l_max, PC 수, k) **전부 없음** |
| 데이터 크기 | pre-fine-tune **20–50** perturbed · 후보 풀 **~20,000** · 최종 **최대 4,000 프레임** | Fig. 3 |
| 실험 | EIS(등가회로 R–RCPE–RCPE–W) · **AFM 나노역학 맵**(공간평균 E) · XRD(Fig. S3) | S.4 |

> 📌 **판정**: **이 편은 재현 가능한 방법 기술이 아니다.** 본문만으로는 아무도 FIRE 를 다시
> 못 만든다. SI 를 받기 전에는 **"이런 순서로 하더라" 이상을 인용하면 안 된다.**

---

## 7. ★★ 1저자 질문에 항목별로 답한다

### 7-1. **계면 구조를 어떻게 만드나** — 🔴 **이 논문은 답하지 않는다**

우리 B2 가 막힌 자리와 **정확히 같은 항목들**을 하나씩 대조한다:

| 우리 B2 가 선언해야 하는 것 | 이 논문의 기재 | 판정 |
|---|---|---|
| **격자 정합 알고리즘** (어떤 초격자로 두 상을 맞추나) | ❌ **없음** (`lattice` 0회) | 🔴 못 배운다 |
| **변형률**(누구를 얼마나 늘리나 · 한쪽 vs 양쪽 배분) | ❌ **없음** (`strain` 0회). 서론에 *"interface mismatch"* 라는 **동기 문장 1회**뿐 | 🔴 못 배운다 |
| **표면 종단**(어느 면·어느 원자층으로 자르나) | ❌ **없음** (`termination` 0 · `slab` 0) | 🔴 못 배운다 |
| **상대 배향**(면내 회전/평행이동 표본 수) | ❌ **없음** | 🔴 못 배운다 |
| **분리거리 gap** | ❌ **없음** (`vacuum` 0) | 🔴 못 배운다 |
| **표본 수 / 시드** | ❌ **없음** (Fig. 4 에 오차막대 0) | 🔴 못 배운다 |
| **셀 크기 / 원자수** | ⚠ **간접**: Fig. 4C 에서 MACE-MD 를 **3456 원자**까지, VASP-MD 는 **576–600 원자**가 한계 | 🟠 상한만 |
| **비정질 계면을 다루나** | ⚠ **간접**: Fig. 2A 3·4번 패널이 비정질-비정질, 원전 ref 45 = Wang/Aykol/Mueller 비정질 계면 논문 | 🟠 **원전이 더 유용** |

⇒ **★ 결론: 이 편의 계면 구조 표본 규약을 우리 B2 보고량 정의에 "그대로 쓸 수 있는" 항목은
0 개다.** 이 편은 *"계면 구조가 다양해서 표본추출이 어렵다"* 를 **문제로 제기하고**,
그 해법을 **"MD 로 20,000개 뽑아 K-means 로 추려라"** 로 답한다. 즉 **"초기 계면을 어떻게
짓나"가 아니라 "이미 지어진 계면에서 학습 프레임을 어떻게 고르나"** 를 푼 논문이다.
**우리 B2 의 🔴 미정의는 전자(前者)의 문제**이므로 **이 편으로는 닫히지 않는다.**

🔵 **다만 우리 B2 에 쓸 수 있는 것이 딱 하나 있다** — **"admissible state 를 하나 고르지 말고
분포를 학습 데이터로 삼는다"** 는 발상 전환. 우리 B2 의 병은 *"난수·xy 이동·비정질 표면이라
상태가 여럿인데 고르는 규칙이 없다"* 인데, 이 편의 태도는 **고르지 않고 다 넣는다**이다.
⇒ B2 를 **스칼라 W_ad 하나**로 정의하지 말고 **`W_ad` 의 표본 분포**로 정의하고
집계 규칙(중앙값/최소/평균 ± 표본수)을 **미리 선언**하면 회신 BJ 의 판정 기준을 만족한다.
(이건 이 논문의 주장이 아니라 **우리 해석**이다.)

### 7-2. **fine-tune 데이터를 계면에서 어떻게 뽑나 / 벌크 모델이 왜 실패하나 / 몇 점 필요한가**

- **왜 실패하나**: 저자들은 *"broad generality of U-MLIPs often comes at the cost of reduced
  accuracy for task-specific materials"* 라고만 쓴다. **계면 특유의 실패 모드(전하이동·이종결합·
  공간전하)를 물리적으로 진단하지 않는다.** 정량 근거는 Fig. 2C 의 `Reference` 막대뿐이고,
  그것도 **U-MLIP zero-shot 이 아니라 문헌의 다른(대개 전용) MLIP** 값이다.
  🔴 ⇒ **"MACE-MP-0 zero-shot 이 계면에서 얼마나 틀리나" 를 이 논문은 재지 않았다.**
  우리가 제일 알고 싶은 그 숫자(=UMA 를 그냥 믿어도 되나)의 **MACE 판**조차 없다.
- **몇 점 필요한가** ✅ **여기는 답이 있다**:
  - **종잣값 20–50 개** perturbed 구조 (pre-fine-tuned 모델용)
  - **후보 풀 ~20,000** (MD 로 생성, DFT 라벨 불필요)
  - **최종 학습셋 ~500–4,000 프레임**. Fig. 3 에서 **수렴 지점은 계 의존**:
    Na/Na₃SbS₄ 는 **~500 프레임**에서 이미 포화, LLZTO 는 **1000–2000** 필요.
  - **⇒ 실무 수치: DFT 라벨 500–2,000점 + 종잣값 20–50점.**
- **능동학습**: ❌ 안 쓴다 (§4-D). 미래과제로 남겼다.

### 7-3. ★★ **무엇을 검증하나 — 계면 물성까지 가나?** 🔴 **안 간다**

전문 검색: **`work of adhesion` 0회 · `adhesion` 0회 · `interfacial resistance` 0회 ·
계면 Li 이동/계면 전도도 0회 · 계면 반응/분해 0회.**

Fig. 4 의 검증 3계 = **T-Na₃SbS₄ · LLZTO · LPSCl** — **셋 다 단일상 벌크다.**
계면 6종으로 **학습**해 놓고, **검증은 벌크 3종에서** 한다.

| 검증 층위 | 이 논문 | 판정 |
|---|---|---|
| 힘·에너지 RMSE (계면 구조에서) | ✅ 함 (Fig. 2) | 유일하게 계면에서 한 검증 |
| **계면 접착일 W_ad** | ❌ | 🔴 없음 |
| **계면 저항 / 계면 Li 이동** | ❌ | 🔴 없음 |
| **계면 반응·분해산물** | ❌ | 🔴 없음 |
| 벌크 σ (EIS 대조) | ✅ 함 (Fig. 4A) | **벌크** |
| 벌크 E, ν | ✅ 함 (Fig. 4B) | **벌크** |
| **DFT 대비 정확도를 계면에서 따로 보고하나** | ❌ **아니다.** 계마다 하나의 RMSE 만 낸다 — **계면 영역과 벌크 영역을 분리한 오차 보고가 없다** | 🔴 **핵심 결함** |

🔴 **이것이 이 편의 가장 심각한 논리 구멍이다.** 계면 슬랩의 RMSE 는 **원자 대부분이 벌크**라
벌크 정확도에 지배된다. **계면 근방 원자만 따로 뽑은 힘 오차**를 보고하지 않으면,
"계면에서 정확하다" 는 **증명되지 않는다.** 초록의 *"accurate MLIPs in solid–solid battery
interfaces"* 는 **현재 데이터로 뒷받침되지 않는다.**
⇒ **우리가 계면 MLIP 을 하면 반드시 넣어야 할 항목**: `RMSE(계면층) / RMSE(벌크층)` 분리 보고.

### 7-4. **"AI-ready" 가 무슨 뜻인가 — 우리가 이식할 형식인가**
§4-C 참조. **형식(스키마·API·메타데이터·라이선스)은 없다.** ref 42 를 인용한 수사다.
이식 가능한 것은 **파이프라인 순서**뿐이고, 그건 코드 100줄이면 우리도 짠다:
`perturb(20–50) → 짧은 fine-tune → MD → SOAP → PCA → K-means(k=N) → 대표 N개 DFT 라벨 → replay fine-tune`.
🔵 우리 `tools/` 에 붙일 자리: `tools/ionic/` 의 MLIP 계열 + `dscribe`(SOAP) 의존성 1개 추가.

### 7-5. ★ **어느 파운데이션 모델을 쓰나 — UMA 가 있나?** ❌ **없다**
- **백본은 MACE-MP-0 하나**다. 사사(Acknowledgement)도 MACE GitHub 커뮤니티에 한다.
- 서론 열거: MACE-MP-0(17) · CHGNet(18) · EquiformerV2(19) · MatterSim(20) · DPA(21) ·
  Orb(22) · GPTFF(23) · SevenNet(24) · GNoME(25) · Allegro-FM(26).
- **전문 검색: `UMA` 0회** (유일한 "uma" 는 참고문헌 저자명 *Ne**uma**nn*) · **`fairchem` 0회** ·
  **`OMat` 0회** · **`eSEN` 0회**.
- ⇒ ⛔ **"이 논문이 UMA 를 검증했다" 는 인용 금지.** UMA 계열은 이 편의 시야에 없다.
  (EquiformerV2 가 인용되지만 이는 FAIR 의 **이전** 아키텍처이고, UMA 체크포인트가 아니다.)

### 7-6. **어느 계면인가 — 우리 계와 얼마나 겹치나**
§3 표. **직접 겹침 2건**: #5 `Li ‖ Li₆PS₅Cl`(= 우리 comp1 + Li 금속 음극 계면),
#4 `Li₃PS₄ ‖ Li₃B₁₁O₁₈`(= 황화물 SE ‖ **붕산염 코팅** — 우리 B₂O₃ 축과 화학이 같은 줄).
**겹치지 않음**: 우리의 주축인 **황화물 SE ‖ 산화물 양극(NCM/LiNiO₂)** 계면은
**이 논문에 없다.** ⇒ **우리 Stage 11 의 그 계면은 이 편으로 커버되지 않는다.**

### 7-7. **저자가 스스로 적은 한계**
놀랍게도 **한계 절이 없다.** 결론에서 미래과제 한 문장(*"uncertainty-aware active learning …
long-timescale and multiscale simulations"*)이 전부다. 🔴 **자기비판 0.** preprint 라는 점과
함께 감안해야 한다.

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | FIRE 3부품 도식 — (A) frozen/trainable 층 분할, (B) **replay**(에폭마다 사전학습 데이터 sub-sample + task mini-batch), (C) 표본추출 파이프라인(20–50 perturbed → pre-fine-tuned → MD → ~20,000 → SOAP+PCA+K-means → refined) | **파이프라인 순서를 그대로 이식**. ⚠ replay 비율·동결 층수 미기재라 그림만으로는 재현 불가 |
| 2 | (A) 6계 스냅샷 (B) 힘 패리티(Train/Valid) (C) **E·F RMSE 막대 = FIRE/Vanilla/Reference** | **§5-2 표가 이 편의 알맹이.** 우리 계(LPSCl) 실제 값 = **0.86 meV/atom · 43.02 meV/Å** — 초록의 "20 meV/Å" 이 아니다 |
| 2C | 초록 주장과 자기 그림의 불일치 | ⛔ **"<1 meV/atom, ~20 meV/Å" 를 황화물 계면에 적용 금지** |
| 3 | (A,B) PCA 커버리지 n=500→4000 (C,D) RMSE·시간 vs 데이터 크기, FIRE/Random/Scratch/Vanilla | **필요 라벨 수 산정 근거**: 500–2000 프레임. **표본추출 비용 = 파인튜닝의 0.3–0.4 %** |
| 3B | LLZTO PCA 에서 n=500 이 **왼쪽 클러스터를 통째로 놓친다**(figure-read) | 우리가 쓰면 **클러스터별 최소 할당(stratified)** 강제 |
| 3C | n≈100 에서 **FIRE > Random**(더 나쁨), n≥2000 에서 FIRE ≈ Random | 본문의 *"across all data sizes"* 반증. **다양성 표본추출 이득은 계 의존** |
| 4 | (A) 구조·MSD·EIS Nyquist (B) E·ν 대 실험 (C) MACE-MD vs VASP-MD 벽시계 | 🔴 **검증이 전부 벌크다.** 계면 물성 0건 |
| 4A | LPSCl: D=4.29×10⁻¹¹ m²/s · σ_MD 0.75 vs σ_EIS 0.89 mS/cm · MSD 창 50–200 ps · 오차막대 없음 | ⛔ **MD 온도 미기재 + D↔σ 불일치(89배) → D 값 이식 금지.** 창(50–200 ps)은 우리 2–50 ps 와 다름 |
| 4B | E: Na₃SbS₄ 31/28 · LLZTO 156/127 · **LPSCl 26/40 GPa** (FIRE/실험) · ν 0.27/0.31, 0.26/0.26, 0.34/0.37 | **LPSCl −35 % 가 최악.** 단 실험 E 는 **AFM 공간평균**이라 우리 DFT C_ij 와 축이 다름 |
| 4C | MACE-MD 1.3→1.4 s/step (16→3456 atoms) · VASP-MD 1.0→195 s/step (16→576) | 규모 상한 근거. ⚠ **16 원자에선 VASP 가 더 빠르다** · 하드웨어 미기재 |
| S1 | 손실 곡선 (미열람 — SI 없음) | — |
| S2 | 기존 문헌 정확도 표 (미열람) | `Reference` 막대의 출처. **받으면 최우선 확인** |
| Table S2 | 문헌 MLIP 정확도 (미열람) | 위와 동일 |
| S3 | XRD 시료 특성 (미열람) | — |

---

## 9. Post-processing ★

- **정확도**: 에너지/힘 **RMSE**, 힘 **패리티 플롯**(Train/Valid). ⚠ hold-out 테스트셋 선언 없음.
- **구성공간 진단**: **SOAP**(DScribe) → **PCA 2차원 투영** → **K-means** 클러스터링.
  - 기록 방식: PC1–PC2 산점도에 **전체 풀(회색) 위에 선택 표본(색)** 을 겹쳐 그린다.
    → **우리도 이 그림은 바로 만들 수 있다** (표본 대표성을 눈으로 보이는 유일한 그림).
- **수송**: MSD → 선형적합 → **D = slope/6** → **Nernst–Einstein + Haven 보정** → σ.
  ⚠ 창(50–200 / 100–500 ps), 온도, H_R 값 **전부 미기재**.
- **역학**: Young's modulus, Poisson's ratio (계산 방법 미기재 — 변형-응력? 탄성행렬? 불명).
- **실험 대조**: EIS **등가회로 피팅**(`R1–(R2‖CPE1)–(R3‖CPE2)–W1`) · **AFM 나노역학 맵의 공간평균**.
- **성능**: MD **s/step vs 원자수** 로그-로그 (MACE vs VASP).

> 🔵 **우리가 바로 차용할 것 2개**: ① **SOAP+PCA 커버리지 그림**(학습셋 대표성 시각화)
> ② **s/step vs 원자수** 벤치마크 그림(우리 UMA vs QE 로 다시 그리면 규모 상한을 방어할 수 있다).

---

## 10. 🔴 비판 — 이 논문의 약한 자리

1. **"6종 계면"이 과장.** 6종 중 LLZTO 는 계면이 아니라 도핑 벌크이고, LiCl/GaF₃ 도 저자 자신이
   "disordered SE" 로 분류한다. **실질 계면 4종.**
2. **초록 수치가 자기 그림과 모순.** `<1 meV/atom` → 1.04 존재. `~20 meV/Å` → 43.02, 54.18 존재.
   **하필 황화물 두 계**가 낙제.
3. **"across all data sizes" 가 Fig. 3C 로 반증됨.** n≈100 에서 FIRE 가 Random 보다 2배 나쁘다.
4. **계면 물성 검증 0건.** 학습은 계면, 검증은 벌크. **계면층/벌크층 분리 RMSE 도 없다**
   ⇒ *"계면에서 정확하다"* 가 증명되지 않았다.
5. **재현 불가.** functional·k-mesh·ecut·supercell·replay 비율·동결 층수·MD 온도·앙상블·
   시드 수 — **본문에 하나도 없다.** SI 없이는 아무것도 못 한다.
6. **MD 온도 미기재 + 캡션/본문 모순** (*"at relevant temperatures"* vs *"room-temperature"*),
   그리고 **인쇄된 D 와 인쇄된 σ 가 Nernst–Einstein 으로 30–120배 어긋난다**(우리 검산).
7. **오차막대 0.** Fig. 4 전부 단일 궤적으로 보인다. 우리 3-seed 규율(±16 %)에 비추면
   σ·E 의 "일치"는 산포 안에 있을 수도 있고 아닐 수도 있다 — **판정 불가**.
8. **기준값의 품질 편차.** ν 의 Na₃SbS₄ 앵커가 **뉴로모픽 메모리 학회 포스터**(ref 55)다.
9. **비교의 축이 섞였다.** E 는 실험(AFM 공간평균), ν 는 문헌 계산 — 같은 막대 그림에
   "Experiment" / "Reference" 로 라벨만 바꿔 나란히 둔다.
10. **자기 한계 절이 없다.** preprint + 자기비판 0.
11. **능동학습·불확실도 부재.** `grasselli2025` 가 지적한 *"벤치마크가 불확실도를 안 본다"* 의 사례.
12. **`Reference` 막대의 정체가 불투명.** 문헌 6편(44,47,49–54)에서 뽑았다는데 **RMSE 와 MAE 를
    섞었다고 본문이 자인**한다(*"(RMSE or MAE)"*). **다른 지표를 같은 막대에 그렸다.**

---

## 11. 우리 DFT/MLIP 대비 (comp1 / modelc) → `../our_dft_baseline.md`

⚠ **아래는 전부 "소환값(문헌) vs 우리 값" 대조이고, 우리 db 로 옮기는 표가 아니다.**

| 항목 | 이 논문 (LPSCl 계) | 우리 (comp1 = Li₆PS₅Cl) | 판정 — 진짜 차이인가 방법 차이인가 |
|---|---|---|---|
| **MLIP 백본** | MACE-MP-0 (fine-tuned) | **UMA-s-1p1 (omat), zero-shot** | 🔵 **다른 축.** 이 편은 파인튜닝, 우리는 무조정. **직접 비교 불가** |
| **σ (RT)** | MD 0.75 / EIS 0.89 mS/cm | ⛔ **절대 σ 인용 금지** (규율) | ⛔ 비교 자체를 안 한다 |
| **D** | 4.29×10⁻¹¹ m²/s (온도 미상) | 3.09×10⁻⁶ cm²/s **@600 K** | 🔴 **비교 불가** — 저쪽 온도 미기재 |
| **MSD 창** | **50–200 ps** (LPSCl) | **2–50 ps 고정** (우리 규약) | 🟠 **방법 차이.** 창이 다르면 D 가 다르다. 우리 창이 더 짧은 대신 자유절편 |
| **시드** | 오차막대 없음 = 1궤적 추정 | 600 K **3-seed**, Ea 0.197±0.032 eV | ✅ **우리가 더 엄격** |
| **Young's modulus** | FIRE ≈ 26 GPa / AFM 실험 ≈ 40 | **E_VRH 22.06 GPa** (DFT relaxed-ion) | 🟠 **우리 DFT 와 저쪽 MLIP 이 26 vs 22 로 가깝다.** 그런데 저쪽 "실험" 40 은 둘 다와 멀다 → **AFM 공간평균이 다른 양을 잰다**(기공·입계·접촉모델). ⇒ **방법 차이가 지배** |
| **ν (푸아송비)** | FIRE 0.34 / ref 0.37 | n/a (우리 C_ij 에서 유도 가능하나 미등록) | — |
| **계면 W_ad** | ❌ **없음** | γ_SE(comp1) **1.211 J/m²**, `Wad` v2 1.107±0.027 J/m² | 🔴 **대조군이 없다.** 이 편은 계면 물성을 안 잰다 |
| **NCM 계면** | ❌ 없음 (Li 금속 · 붕산염 코팅만) | Stage 11 `run_cathode_interface.py` (LiNiO₂) | 🔴 **겹치지 않는다** |
| **무질서 처리** | ❌ 미기재 | SQS/enumerate 미선언 (우리도 약점) | ⚪ **양쪽 다 부실** — 이 편을 근거로 우리를 정당화할 수 없다 |
| **불확실도** | 없음 | `force_contrast` M=3 (UMA/MACE/SevenNet) | ✅ **우리가 더 앞선다** |

---

## 12. ★ 우리 좌표 — 계면 축(B1·B2·Stage 11)에 이 편을 어디에 놓나

### 12-1. 우리 계면 자산과 결함 (2026-09-09 현재)
| 자산 | 상태 |
|---|---|
| `tools/doping/run_cathode_interface.py` (Stage 11) | **273 배치에서 0회 실행** |
| UMA melt-quench 비정질 표면 파이프라인 | `adhesion_v2_3000K_melt` (5 seeds) 등 존재 |
| `db/properties/adhesion.json` | γ_SE(comp1) **1.211 J/m²** · Wad v2 comp1 **1.107 ± 0.027** / comp2 1.046 ± 0.074 |
| 실측 앵커 | `lee2026_mechanical_halogen_argyrodite_drycoating` **AFM-FS W_ad = 194 / 180 / 316 / 298±11 / 249 aJ** (5조성) ⚠ 그 논문의 **계산층은 우리 digest 가 "약함" 등급** → **실험층만** 앵커 |

**우리 결함 (비준 카드 §6 + Codex BJ)**
- `run_cathode_interface.py:105,110,113` — `MaxwellBoltzmannDistribution` · `Langevin`(×2) 이
  **rng 미지정** ⇒ `Wad_std` **재현 불가**
- 표면·조성·면적·변형률·배치 분포·분리 기준 **미선언** (`adhesion.json` 에 strain 0.2 / 1.1 / 3.3 %
  가 흩어져 있고 어느 규칙으로 골랐는지 없음)
- `run_cathode_interface.py:50–51` — **`build_ncm_1L`: LiNiO₂ R-3m (a=2.878, c=14.19) 를 "NCM" 이라
  부른다. Co·Mn 이 없다.** ⇒ **별도 카드 필요**
- Codex BJ 판정: **B2 = 🔴 미정의** (*"admissible state 다수 + 선택·집계 규칙 없음"*)

### 12-2. **이 편의 계면 구조 표본 규약을 B2 에 그대로 쓸 수 있나** — 항목별 답
| B2 가 선언해야 할 것 | 이 편에서 가져올 수 있나 |
|---|---|
| 격자 정합 알고리즘 | ❌ **없다** |
| 변형률 배분 규칙 (우리: SE 를 NCM 에 맞춰 강제 변형 — 한쪽 몰빵) | ❌ **없다** |
| 표면 종단 | ❌ **없다** |
| 상대 배향 표본 수 (우리: xy 시프트 5 seeds) | ❌ **없다** (저쪽도 오차막대 없음 = 표본 1) |
| 분리거리 (우리: `GAP = 2.5 Å` 고정) | ❌ **없다** |
| **난수 고정** | ❌ **없다** (저쪽도 시드 미기재 — **우리와 같은 병**) |
| **셀 크기 상한** | 🟠 **간접**: MLIP 3456 원자 OK / DFT 576–600 원자 한계 |
| **상태를 고르지 말고 분포로 다루는 태도** | 🔵 **이것 하나** — §7-1 참조 |

⇒ **★ 결론: B2 는 이 편으로 안 닫힌다.** 계면 구조 표본 규약은 **우리가 처음부터 써야 한다.**
이 편이 주는 것은 **"표본을 하나로 줄이지 말고 분포째 다뤄라"** 는 방향뿐이다.

🔵 **B2 를 정의하려면 우리가 지금 당장 할 수 있는 것 (이 편과 무관하게 우리 자산으로)**
1. `run_cathode_interface.py:105,110,113` 에 **`rng` 인자 명시** → `Wad_std` 재현성 확보 (GPU 0)
2. **`LiNiO₂ ≠ NCM` 카드** 를 `kb/` 에 박고 파일·필드 이름을 `lno` 로 바꾸거나 주석 고정
3. **B2 를 스칼라가 아니라 분포로 재정의**: `X_B2(M) = median{W_ad} ± MAD, n=k seeds`,
   집계 규칙·시드 수·strain 배분·gap·종단을 **결과 보기 전에** 선언
4. 표면 종단·strain 배분은 **`choi2025_mlip_cu_taxn_interfacial_adhesion`** 쪽을 먼저 보는 게 낫다
   (그 편은 계면 접착을 MLIP 으로 직접 잰다 — **이 편은 안 잰다**)

### 12-3. **계면 fine-tune 이 우리에게 필요한가 — UMA 를 그냥 믿어도 되나**
🔴 **이 논문은 답하지 않는다.**
- 이 편은 **MACE-MP-0** 만 다루고 **UMA 를 한 번도 언급하지 않는다** (§7-5).
- 게다가 **U-MLIP zero-shot 의 계면 오차 자체를 재지 않았다** — `Reference` 막대는
  문헌의 **다른 전용 MLIP** 값이지 MACE-MP-0 무조정 값이 아니다.
- ⇒ ⛔ *"이 논문이 파인튜닝 없이는 계면에서 못 쓴다고 했다"* 는 **인용 불가**.
  이 논문이 보인 것은 **"파인튜닝하면 문헌 값보다 낫다"** 뿐이다.

🔵 **그래도 방향 신호는 있다** — 6계 중 **황화물 두 계가 파인튜닝 후에도 제일 나쁘다**
(43 / 54 meV/Å). **황화물 계면이 이 종류 모델에 어려운 화학**이라는 약한 증거다.
우리 계에 대해서는 **직접 재는 수밖에 없다**: `force_contrast`(UMA/MACE/SevenNet M=3) 를
**계면 구조에서** 돌려 세 모델 산포를 보는 것이 **GPU 0 에 가장 가까운 진단**이다.
(⚠ 이건 `grasselli2025` 판정대로 **epistemic uncertainty 가 아니라 오설정 대조**다.)

### 12-4. **비용** — 계면 라벨 몇 점, GPU 몇 시간
| 항목 | 이 논문 (소환값) | 우리 이식 시 |
|---|---|---|
| 종잣값 (perturbed) | **20–50 구조** | 계면 1종당 20–50 SCF |
| 후보 풀 (MD, 라벨 불필요) | **~20,000 구조** | MLIP-MD 로 생성 — 싸다 |
| **최종 DFT 라벨** | **500–4,000 프레임** (계 복잡도 의존; 단순계 500 포화, 다상계 1000–2000) | 🔴 **여기가 진짜 비용**. 계면 슬랩 300–600 원자 × 1,000점 SCF = **우리 자원으론 큰 캠페인** |
| 표본추출 (PCA/K-means) | **2–3 min** (파인튜닝의 0.3–0.4 %) | 사실상 공짜 |
| 파인튜닝 | **13–18 h** (n=4000; **하드웨어 미기재**) | GPU 1장 기준 비슷한 자릿수로 추정 (⚠ 근거 약함) |
| **DFT 라벨링 시간** | ❌ **논문에 없다** | 🔴 **이 편으로는 예산 산정 불가** |

⇒ **★ 정직한 결론: 이 편은 "GPU 몇 시간" 을 답해 주지 않는다.** 하드웨어도, 라벨링 비용도
없다. 답하는 것은 **"DFT 라벨 500–2,000점이면 수렴한다"** 는 **라벨 개수**뿐이고,
그것도 **계면이 아니라 이 편의 6계 기준**이다.

### 12-5. 🎤 talk 역링크
`litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 **인입 대기열 6건**을 확인했다 —
**이 논문은 그 표에 없다** (대기열은 MTP/SevenNet/GNoME/argyrodite hydrolysis 계열).
⇒ **역링크 대상 없음.** 다만 그 talk 의 MLIP 축과 주제가 인접하므로, 향후 대기열에 넣을 때
이 digest 를 정본으로 걸면 된다.

---

## 13. 인용 가능 문장 (deck / 원고용) — **preprint 표기 필수**

- "Liu et al. (arXiv 2601.17847, **preprint**) show that replay-augmented continual fine-tuning of
  MACE-MP-0 lowers energy/force RMSE against plain fine-tuning in all six battery solid–solid
  systems they studied (e.g. 1.29 → 0.86 meV/atom and 55.5 → 43.0 meV/Å for Li/Li₆PS₅Cl)."
- "Diversity-based selection (SOAP → PCA → K-means) costs only ~0.3–0.4 % of the fine-tuning
  wall time, so the sampling step is essentially free."
- "Fine-tuned MLIP-MD keeps a near-constant wall time per step from 16 to 3456 atoms, whereas
  first-principles MD scales cubically and is limited to ~600 atoms by memory."
- ⛔ **쓰면 안 되는 문장**: *"FIRE achieves force RMSE ~20 meV/Å at sulfide interfaces"*
  (실제 43–54) · *"validated on six solid–solid interfaces"* (실질 4) ·
  *"validated interfacial properties"* (계면 물성 검증 0건) ·
  *"UMA fine-tuning"* (UMA 를 안 씀).

---

## 14. 기법 용어 미니사전

- **U-MLIP (universal MLIP)**: 수십만~수백만 개 결정 구조(Materials Project 등)로 미리 학습한
  범용 원자간 퍼텐셜. 임의 조성에 바로 쓸 수 있는 대신, 특정 계에서는 전용 모델보다 부정확.
- **Fine-tuning**: 사전학습 모델의 가중치를 출발점으로, **작은 task 데이터로 이어 학습**하는 것.
  이 편은 앞 층을 얼리고(frozen) 뒤 층만 학습(Fig. 1A).
- **Catastrophic forgetting**: 새 데이터만 계속 학습하면 이전에 배운 것을 잃는 현상.
  좁은 계면 데이터만 먹인 모델이 MD 중 분포 밖 배치에서 폭주하는 이유.
- **Replay**: 그 망각을 막으려고 **사전학습 데이터를 매 에폭 조금씩 다시 섞어 먹이는** 기법.
  ← **이 편의 유일한 알고리즘적 신규성**.
- **SOAP (Smooth Overlap of Atomic Positions)**: 원자 하나 주변의 이웃 배치를 회전불변 벡터로
  바꾸는 서술자. "이 두 구조가 얼마나 비슷한가" 를 숫자로 만든다. 구현은 **DScribe**.
- **PCA + K-means 표본추출**: SOAP 벡터를 2–수십 차원으로 줄이고(PCA), k 덩어리로 나눠(K-means)
  **덩어리마다 대표를 뽑는다** → 비슷한 구조 중복 라벨링을 피한다.
- **Pre-fine-tuned model**: 20–50개 구조로 **아주 짧게** 파인튜닝한 임시 모델. 목적은 정확도가
  아니라 **MD 가 안 터지게 하는 것**.
- **RMSE (energy, meV/atom / force, meV/Å)**: MLIP 정확도의 표준 두 지표. ⚠ **MAE 와 섞으면 안 된다**
  (이 편의 `Reference` 막대가 그 죄를 자인한다).
- **Nernst–Einstein + Haven ratio**: MSD 에서 얻은 tracer 확산계수 D\* 를 전도도 σ 로 바꾸는 식.
  H_R = D\*/D_σ. **H_R = 1 을 가정하면 이온 간 상관운동을 무시**하는 것 — 우리 계열 실측은
  0.235–0.315 (adeli2019).
- **AFM 나노역학 맵**: 팁을 격자점마다 눌러 힘-거리 곡선을 얻고 접촉모델로 국소 탄성률을 뽑는 것.
  **공간평균 E** 는 기공·입계를 포함하므로 **단결정 DFT C_ij 와 같은 양이 아니다**.
- **등가회로 `R–(R‖CPE)–(R‖CPE)–W`**: 임피던스 스펙트럼을 벌크/입계/전하이동 + Warburg 확산으로
  나누는 표준 회로. 반원 2개 + 꼬리.

---

## 15. ⚠ **못 한 것 / 확인 못 한 것** (필수 절)

1. **SI (S.1–S.4) 를 못 봤다.** 우리에게 온 PDF 는 본문 21 pp 뿐. 네트워크가 막혀 arXiv 원본도
   못 받았다. ⇒ **계면 구조 생성 · DFT 설정 · replay 비율 · MD 온도/앙상블 · Table S2(문헌 비교) ·
   Fig. S1–S3 을 전부 확인 못 했다.** 위 §6·§7-1 의 "❌ 없음" 은 **"본문에 없음"** 이지
   "논문 전체에 없음" 이 아니다. **SI 를 구하면 §6·§7-1 을 다시 써야 한다.**
2. **본 그림 / 안 본 그림**: 크로핑된 **4장 전부 실제로 열람**(Fig. 1·2·3·4) + Fig. 4B·4A(LLZTO/LPSCl
   MSD)·Fig. 3C-left 를 **고해상도로 재크로핑해 확대 판독**. **SI 그림(S1–S3)·Table S1–S2 는
   파일 자체가 없어 미열람.**
3. **형제편(`liu2026_finetuning_umlip_tutorial`)을 아직 못 읽었다.** 동시 진행 중이라
   `litdb/papers/` 에 없다. **저자 겹침·주장 겹침·모순 여부를 대조하지 못했다.**
   특히 **replay 비율·동결 층수** 같은 빠진 하이퍼파라미터가 튜토리얼 편에 있을 수 있다.
4. **`Reference` 막대의 출처 6편(ref 44,47,49–54)을 원문 대조하지 않았다.** 그 값이 어떤 조건
   (계 크기·functional·테스트셋)에서 나온 것인지 모른다 ⇒ **"한 자릿수 개선" 주장을 독립 검증 못 함.**
5. **D↔σ 30–120배 불일치는 우리 검산이다.** 격자상수·이온수를 우리가 문헌값으로 넣었고
   (LPSCl a=9.86 Å/24 Li, LLZTO a=12.95 Å/52 Li, T-Na₃SbS₄ V≈373 Å³/6 Na),
   저자가 쓴 Haven 비·온도를 모른다. ⇒ **"저자가 틀렸다" 가 아니라 "본문 정보로는 재현 불가" 로만 읽어야 한다.**
6. **Fig. 3C/3D 의 수치는 눈금 판독(figure-read ≈)** 이다. Fig. 2C 만 막대에 숫자가 인쇄돼 있어
   정확값이다. **Fig. 4B 의 E·ν 도 전부 figure-read.**
7. **하드웨어·라벨링 비용을 확인 못 했다** — 논문에 없다. ⇒ 우리 GPU 예산으로 환산 불가.
8. **저널 게재 여부를 확인 못 했다** (네트워크 차단). arXiv v1 기준으로만 판단했다.

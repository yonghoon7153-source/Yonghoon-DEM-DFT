# 외부 자료 — OMat24 보충자료 (**우리 UMA 의 훈련 데이터**)

> 출처: Barroso-Luque 외, *"The Open Materials 2024 (OMat24) inorganic materials dataset and models"*,
> ***Nat. Comput. Sci.*** (2026) `10.1038/s43588-026-00996-w` · arXiv **2410.12771** ·
> 보충자료 MOESM1(SI 16 pp) / MOESM3 / MOESM4 / MOESM5 / MOESM6 · 입수 2026-08-26
> **본문 PDF 미확보** — SI 와 보충 데이터만 있다.

## ⚠ 권리
Nature 계열 보충자료다. **내부 분석 전용.** 재배포 금지, 수치를 우리 결과로 제시 금지.
인용은 논문으로 한다.

## 파일

| 파일 | 무엇 | 크기 |
|---|---|---|
| `phonon_softening.csv` | **2차(포논) softening** — 모델×데이터셋 9쌍 × ~10,000 구조 | 99,418행 |
| `energy_force_softening.csv` | **0차(에너지)·1차(힘) softening** — 10쌍 × 979 구조 (**high-energy WBM set**) | 9,790행 |
| `omat-element-hist.csv` | 원소별 구조 수 (Z=0–118) | 89종 등장 |
| `matbench_discovery_leaderboard_MOESM5.csv` | **20모델 공통 눈금** — F1·DAF·MAE·RMSE·R²·**κ_SRME** 등 21지표 | 22행 |
| `formation_energy_corrections_MOESM4.csv` | MP vs OMat 생성에너지 보정 대조 (424 조성) | 424행 |

⛔ 안 가져온 것: `fig_1b.json.gz` (31 MB, Fig 1b 원자료) · `fairchem_core 1.10.0` 소스.

---

## 🔬 우리가 읽은 것 (2026-08-26) — **T1b 의 전제가 바뀐다**

### ① softening 은 실재하고, **측정돼 있고, 정의가 3차수다**

SI §E 원문:

> *"**Zeroth order (energy), first order (forces) and second order (phonon)** systematic softening
> distribution shifts between MPTrj, OAM (OMat24 + MP/sAlex finetuning) and MPA (MP/sAlex) trained models"*
> — 평가는 **high energy WBM set**(에너지·힘)과 **recalculated MDR phonon dataset**(포논).

즉 이상욱 랩 덱 슬 8 의 `DFT PES ──softening──▶ uMLIP PES` 는 **개념도가 아니라
이 분야가 이미 정량화해 둔 현상**이다. 우리 T1b 질문의 절반은 이미 답이 있었다.

### ② ★★ **원인은 아키텍처가 아니라 데이터셋이다** — 저자들의 결론

> *"Improvements across all degrees of softening are consistently observed in **five distinct
> architectures**, indicating that the effect is **largely architecture-independent** and
> **primarily attributable to the diversity of the OMat24 dataset**."*

우리 실측 재집계가 그 문장을 그대로 재현한다 (중앙값):

| 모델 | 훈련셋 | 힘 softening | 에너지 softening | 포논 softening |
|---|---|---|---|---|
| **sevenn** | MPtrj | 0.9248 | −0.0299 | 0.9888 |
| **sevenn** | **OAM** | **0.9809** | **−0.0045** | **0.9917** |
| **grace** | MPtrj | 0.8978 | −0.0598 | 0.9862 |
| **grace** | **OAM** | **0.9621** | **−0.0107** | **0.9932** |
| **eSEN** | MPtrj | 0.9920 | −0.0018 | 0.9846 |
| **eSEN** | **OAM** | **0.9965** | **−0.0010** | 0.9768 |
| **mace** | MPtrj | 0.8957 | −0.0366 | 0.9760 |
| **mace** | **mpa** | **0.9789** | **−0.0099** | 0.9860 |
| **eqV2 S** | MPtrj | 0.9685 | −0.1316 | — |
| **eqV2 S** | **OAM** | **1.0015** | **−0.0043** | — |

**힘·에너지는 5/5 아키텍처 전부에서 OMat24 계열 훈련이 개선한다.** eqV2 는 에너지 softening 이
**−0.1316 → −0.0043 (31배)** 로 가장 극적이다.

### ③ 🔑 **그래서 덱의 논증을 우리 UMA 에 적용하면 방향이 반대다**

덱 슬 8 의 함의는 *"uMLIP 은 평형 근처에 치우쳐 PES 가 무르다"* 이고, 그 대응이 fine-tuning 이다.
그런데 이 데이터가 말하는 것은 **"무르게 만드는 것은 좁은 훈련셋(MPtrj)이고, OMat24 가 그 해독제"** 다.

**우리 UMA-s-1p1(omat) 의 `omat` 이 바로 그 OMat24 다.**
⇒ *"우리는 uMLIP 을 써서 PES 가 무르다"* 는 논증은 **우리 설정에 대해서는 성립하지 않는다.**

⚠ **단 그대로 옮기면 안 되는 이유 셋**
1. **UMA-S 는 이 표의 어느 행도 아니다.** OAM = `OMat24 + MP/sAlex finetuning` 인데,
   UMA-S 는 OMat24 를 **여러 데이터셋과 함께 멀티태스크**로 학습한다(OC20·OMol25·OPoly26 등).
   같은 계열이지만 같은 모델이 아니다.
2. **평가 계가 우리 계가 아니다.** high-energy WBM · MDR phonon 은 일반 무기결정이고
   **황화물 초이온 전도체가 아니며 700 K MD 도 아니다.**
3. **크기가 안 맞는다.** 여기 softening 은 **1–10 %** 규모다. 우리 b2o3 는 골격이
   **rigid → β ≥ 0.60 (확산)** 으로 **질적으로** 바뀐다. 몇 %의 PES 연화가 그 전이를
   만든다고 보기 어렵다 ⇒ **b2o3 를 "조성 고유"로 본 우리 판정이 오히려 강화된다.**

### ④ ⚠ 이상치 1건 — 설명하지 말고 기록만

`eqv2 · OAM` 포논 중앙값 **0.2565**(99.7 %가 <1)로 다른 8쌍(0.976–0.993)과 자릿수가 다르다.
그런데 같은 `eqV2 S · OAM` 의 **힘** softening 은 **1.0015 로 전체 최고**다. 서로 안 맞는다.
모델 변종 표기(`eqv2` vs `eqV2 S`)가 다르니 **다른 모델일 가능성**이 크지만 확인 못 했다.
**본문 PDF 를 받기 전에는 이 행을 인용하지 않는다.**

### ⑤ 우리 계 원소의 커버리지 — 충분하다

총 **326,304,488** (원소별 구조 수 합) · **89종** 등장.

| 원소 | 구조 수 | 전체 대비 | 순위 |
|---|---:|---:|---:|
| **O** | 6,893,229 | 2.11 % | **1위** |
| **Li** | 5,879,591 | 1.80 % | 9위 |
| **P** | 4,908,329 | 1.50 % | 25위 |
| **Cl** | 4,757,487 | 1.46 % | 26위 |
| **S** | 4,737,594 | 1.45 % | 27위 |
| **Y** | 4,667,722 | 1.43 % | 30위 |
| **Sn** | 4,119,909 | 1.26 % | 37위 |
| **Na** | 3,878,101 | 1.19 % | 42위 |
| **Nd** | 3,511,213 | 1.08 % | 52위 |
| **B** | 2,286,232 | 0.70 % | **72위** ⚠ |

🔑 **B 가 89종 중 72위로 눈에 띄게 적다.** 우리 b2o3 축이 바로 B 다.
⛔ **이것을 "그래서 b2o3 가 틀렸다"의 근거로 쓰면 안 된다** — 원소 등장 횟수는
**그 원소가 든 구조가 몇 개냐**이지 **B–S 결합이 얼마나 표집됐느냐**가 아니다.
Li₃N 편향 전례처럼 **화학 환경 수준**에서 봐야 하는데 이 히스토그램으로는 못 본다.
다만 **T1b 를 왜 해야 하는지의 정황**으로는 값어치가 있다.

### ⑥ 🆕 **공통 눈금이 생겼다** — `matbench_discovery_leaderboard_MOESM5.csv`

20모델 × 21지표 (F1 · DAF · Precision/Recall · MAE · RMSE · R² · **κ_SRME** · missing_preds …).
`SevenNet-MF-ompa` · `SevenNet-l3i5` · `MACE-MP-0` · `MACE-MPA-0` · `CHGNet` · `M3GNet` · `GNoME` ·
`eqV2` · `eSEN` · `GRACE` · `ORB` · `MatterSim` · `DPA-3.1` 등이 **같은 자로** 재어져 있다.
⇒ 우리가 별도로 요청했던 *"Matbench Discovery 리더보드"* 가 사실상 여기 들어왔다.
⚠ **UMA 는 이 표에 없다** — 우리 모델의 자리는 여전히 비어 있다.

---

## 🔴 우리 기록에 반영해야 할 것 (에이전트 종료 후)

1. **`kb/open_items.md` T1b** — *"PBE 계열이 황화물 골격을 무르게 보는가"* 의 **전제를 다시 써야 한다.**
   softening 은 **functional 이 아니라 훈련셋 다양성**의 문제로 측정돼 있고, 우리 훈련셋이 그 해독제 쪽이다.
   T1b 의 vdW-DFT 검사(=참조 이론 축)는 **여전히 유효**하지만, "uMLIP 이라서 무르다" 가지는 약해진다.
2. **`litdb/papers/uma2026_…`** — OMat24 표 한 줄 옆에 **softening 개선 수치**를 붙인다.
3. **`litdb/talks/lee2026_skku…` §99-4 A1**(*"uMLIP PES 가 고에너지에서 물러진다"*) —
   **덱이 맞다. 다만 원인이 아키텍처가 아니라 훈련셋**이라는 외부 정량자료가 생겼다고 병기.
4. **위시리스트** — OMat24 **본문 PDF** 는 여전히 필요하다(④ 이상치 · softening 정의식 · UMA 와의 관계).

# 📥 병합 대기 — `imbalzano2021_committee_uq_md_thermodynamic_averages`
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09, litdb-curator. **동시 4편 작업 중이라 `INDEX.md`·`comparison_vs_ours.md` 를 직접 안 건드렸다.**
> 아래 3덩이를 사용자가 병합한다. digest 원본: `litdb/papers/imbalzano2021_committee_uq_md_thermodynamic_averages.md`
> 그림: `litdb/figures/imbalzano2021_committee_uq_md_thermodynamic_averages/` (fig_1…fig_9, 9장)
>
> ⚠ **서지 미확인**: PDF 에 저널·DOI·arXiv 도장이 **하나도 없다** (pdfTeX, 2020-11-10 생성, 16 pp preprint).
> 슬러그의 `2021` 은 사용자 지정이고 PDF 가 확인해 주지 않는다. **표지 대조 전에는 서지 인용 금지.**
> 병합할 때 이 단서를 INDEX 행에 남겨 두는 것을 권한다.

---

## ① `INDEX.md` — 행 1줄

넣을 자리: **MLIP/방법론 절** (`uma2026…` · `petmad2026…` · `shapeev2016…` · `park2024…` 과 같은 표).

| slug | 논문 | 축 · 우리 쪽 결론 |
|---|---|---|
| `papers/imbalzano2021_committee_uq_md_thermodynamic_averages.md` | **[외부·methods·🔧 방법 원전 · ★MLIP 불확실도 축 3편 중 우리한테 제일 중요한 편]** G. Imbalzano, Y. Zhuang, V. Kapil, K. Rossi, E. A. Engel, **F. Grasselli\***, **M. Ceriotti\*** (**EPFL COSMO** + 샤먼대 + 케임브리지), "**Uncertainty estimation by committee models for molecular dynamics and thermodynamic averages**" — ⚠ **PDF 에 저널·DOI·arXiv 없음**(pdfTeX 2020-11-10, preprint 16 pp · §I–VI + Appendix A · Fig 1–9 · **Table 0개** · refs 82). **보정된 committee 산포를 MD 궤적 위 평균까지 전파하는 식을 세운 방법론 논문.** 구성: 전체 훈련셋을 **복원 없이 부분표집**해 M 모델 독립학습(⚠ 실제로는 계마다 달라 삼펩타이드는 *"가중치 초기화 + 90/10 CV 분할만 다름"* = 사실상 시드 앙상블) → **로그우도로 전역 스칼라 α 교정**(`Eq. 5`; M 유한 편향보정판 `Eq. 6`) → **재척도 `Eq. 7`**. ★★ **대표식**: 궤적 하나(V̄)만 돌리고 멤버별 에너지를 저장해 **on-the-fly 재가중**(`Eq. 22`, 원리적으로 정확)하되, 오차가 `Var[β(V^(i)−V̄)]` 에 **지수적**이고 그 분산이 **계 크기에 비례**해 커지므로 **누율전개 근사(CEA)로 선형화**(`Eq. 24`: `⟨a⟩_{V^(i)} ≈ ⟨a⟩_V̄ − β⟨a(V^(i)−V̄)⟩_V̄`) ⇒ **`σ̃² ≈ σ_a²(관측량모델) + σ_V²(퍼텐셜모델)`** (`Eq. 26–28`), `σ_V ≈ β·std_i[Cov(a, V^(i)−V̄)]`. **소환 수치**: α **2.1**(물 M=4, 편향판 3.75) · **4.08**(산/페놀 M=5, 원논문 5.8) · **1.0**(삼펩타이드) · T_m **290±5 K** · Δs_m 0.16±0.01 meV/K/mol · Δh_m 46±3 meV/mol · 탈양성자화 **20 (+5/−2) kJ/mol**(비대칭) · σ_b 7×10⁻³ meV/atom(⚠ 단위 의심). **M 규율**: `E[1/ς²]=(M−1)/(M−3)` ⇒ **M≥4 하드 하한**(M=3 발산), M=4 편향판은 α 를 **65 % 과대**(`Fig. 9` figure-read 4.6 vs 2.77), 비선형 조합 전파 시 **M≥6 권고**. 시연 4계: Phe-Gly-Phe REMD(weighted baseline) · 물 g(r)·융점 · 산/페놀 자유에너지 · 액체 Ga 유한온도 DOS. 엔진 i-PI + LAMMPS/n2p2 | **⛔ 물성값 0 · Li/황화물 0 → A–D 물성 4축 금지, `J-7 🔧 방법 원전` 에만.** ① 🔴 **우리 D 에 이 논문을 인용할 수 없다** — 전문에 `diffusion`·`transport`·`MSD`·`Green–Kubo`·`time-correlation`·`conductivity` **각 0회**(grep). 전파하는 것은 **정적 배위평균뿐**이고, 재가중은 배열의 볼츠만 확률만 고치지 **시간상관을 복원하지 못한다** ⇒ **원리적 확장 불가** ② ★ **축 판정**: 우리 blocker 2축 중 **모델축의 정적 부분만** 덮고 **시드축 0 · 동역학축 0**. ⇒ 지금 우리 D 오차막대는 **"통계 오차막대"이지 총 불확실도가 아니다** — 이름을 그렇게 쓴다 ③ ★ **M≥4 하한이 우리를 친다**: 이종 committee **M=3**(UMA/MACE/SevenNet) · modelc Ea **3시드**. PET-MAD 4번째 투입은 "권장"이 아니라 **하한 도달**(3점 SD 의 상대오차는 `1/√(2(M−1))` = **50 %**, 내 계산) ④ ★ **raw 산포는 좁다**(α=2.1·4.08 **>1**) ⇒ 우리 불일치는 **하한으로만** 말할 수 있고 *"불일치가 작았으니 안전"* 은 **이 논문이 지지하지 않는다** (`b2o3_committee_2026_09_07.json` 허용선과 정확히 양립) ⑤ ★ **비선형 유도량 처방**: 멤버별로 끝까지 계산 후 산포 — `Fig. 6` T_m(적합의 근=비) · `Fig. 7` 대칭 Δp→`−kT log`→**비대칭 구간**. 우리 Arrhenius Ea·D_rel 에 절차만 이식 가능 ⑥ ⚠ **이종 committee 에 이 통계 적용 금지** — 가정 (i) 같은 y_ref (ii) 교환가능 (iii) 가우시안 이 **셋 다 깨진다**(OMat24 vs MPtrj 훈련셋 계통차 · MACE/SevenNet 이 둘 다 MPtrj 라 상관 · 참조라벨 없어 α 불가) ⑦ ⚠ **저자 자신의 단서 2개가 세다**: *"committee σ 는 총오차가 아니다 — 유한크기·참조에너지 오차가 comparable"*(§III B 2) · 융점은 *"수렴값이 아니다"*(유한크기) ⑧ 🔴 **내가 찾은 흠**: `Fig. 6` 의 ±5 K 에 **통계오차가 안 들어갔다**(점 산포가 눈에 보이는데 모델산포만 씀 — 우리 Q7 판정과 같은 계열의 문제) · 전파된 폭의 **커버리지 검증이 논문 전체에 없다**(`Fig. 1` 은 **평균**만 검증) |

---

## ② `comparison_vs_ours.md` — 참고키 표에 1행 추가

넣을 자리: **J 절 머리의 참고키 표** (`[Shapeev16]` · `[Park24]` 아래).

```
| **[Imbalzano21]** 🔧 | `imbalzano2021_committee_uq_md_thermodynamic_averages` — **committee UQ → 열역학 평균 전파 원전** (EPFL COSMO, ⚠ **PDF 에 저널·DOI 없음**). ⚠ **물성값 0 · 물/펩타이드/페놀/Ga 전용** → 아래 **J-7** 에만 등장, A–D 축 금지. 🔴 **동역학량(D·수송) 0회 — 우리 D 인용 금지** |
```

---

## ③ `comparison_vs_ours.md` §J-7 — 새 소절 (블록 통째로 붙여넣기)

```markdown
**[Imbalzano21] `imbalzano2021_committee_uq_md_thermodynamic_averages` — committee 불확실도를 궤적 평균까지 전파하는 통계 원전**
(EPFL COSMO, Grasselli & Ceriotti 교신 · ⚠ **PDF 에 저널·DOI·arXiv 없음**, pdfTeX 2020-11-10 preprint ·
계: 물·삼펩타이드·메탄술폰산/페놀·액체 Ga — **Li·황화물·아르지로다이트 0건, 물성값 0건**)

> ★ **왜 이 편이 MLIP 불확실도 축 3편 중 제일 중요한가**: 다른 UQ 논문이 **힘·에너지 오차**에서 멈추는데
> 이 편은 그걸 **궤적 평균까지 전파**한다. 우리 D 는 MSD 기울기 = 궤적 평균이라 겉보기 구조가 같다.
> **그런데 겉보기만 같다** — 아래 표 마지막 두 행이 그 이유다.

| 항목 | [Imbalzano21] | 우리 (UMA-s-1p1 단일 모델) | 판정 |
|---|---|---|---|
| committee 구성 | 전체 훈련셋을 **복원 없이 부분표집** → M 모델 독립학습 (⚠ 실제로는 계마다 다름: Ga DOS 는 300/394 부분표집, 삼펩타이드는 **초기화 시드 + 90/10 CV 분할만**) | **단일 파운데이션 모델. committee 자체가 없다** | 🔴 **σ_V·α·재가중 전부 실행 불가** |
| committee 크기 M | 4(펩타이드·물·Ga PM) · 5(산/페놀) · **64**(Ga DOS OM) · 16(부록 α 분석) | 이종 3종(UMA/MACE-MP-0/SevenNet-0) = **M=3** · 시드 3 | 🔴 **`E[1/ς²]=(M−1)/(M−3)` 이 M=3 에서 발산 ⇒ 우리는 하한 미달** |
| 최소 M | **4 하드 하한**, 비선형 전파 시 **6 권고** (Appendix A) | — | ⇒ **PET-MAD/UMA-1.2 4번째 투입은 "권장" 이 아니라 "하한 도달"** (§J-5 처방의 정량 근거) |
| 교정 α | 로그우도 최대화. **α = 2.1**(물) · **4.08**(산/페놀) · 1.0(펩타이드). **전부 ≥1 ⇒ raw 산포는 참오차를 2–4배 과소추정** | **α 를 잴 수 없다** — 참조 DFT 검증셋도, UMA 훈련분포(OMat24)도 우리에게 없다 | ⚠ **우리 committee 불일치는 "하한" 으로만 말한다.** *"불일치가 작았으니 안전하다"* 는 결론을 **이 논문이 지지하지 않는다** (`b2o3_committee_2026_09_07.json` 허용선과 정확히 양립) |
| 전파 방식 | `Eq. 22` 재가중(정확) → 계 크기에 **지수적**으로 통계효율 붕괴 ⇒ **`Eq. 24` CEA 선형화** | — | ⭕ **개념만 이식.** CEA 는 `⟨a⟩_{V^(i)} ≈ ⟨a⟩_V̄ − β⟨a(V^(i)−V̄)⟩_V̄` — **선형화이지 재가중이 아니다** |
| 분산 분해 | **`σ̃² ≈ σ_a² + σ_V²`** — 관측량모델(OM) + 퍼텐셜모델(PM). `σ_V ≈ β·std_i[Cov(a, V^(i)−V̄)]` | 우리 D 에는 **σ_a 항이 없다**(D 는 학습된 관측량이 아니라 궤적의 범함수) ⇒ 모델 불확실도는 **전부 σ_V 형** | 🔴 **그런데 그게 정확히 못 재는 항이다** |
| 비교 대상 | `Fig. 8` 액체 Ga DOS 에서 σ_a 가 σ_V 를 지배 (figure-read: 원자가띠에서 σ_V ≈ σ_a 의 1/3–1/2) — 그래도 저자는 *"σ_V is sizeable"* | — | ⇒ **관측량 모델을 아무리 잘 학습해도 퍼텐셜 쪽 항이 남는다**. 우리는 그 항만 있는데 못 잰다 |
| **관측량 종류** | **정적 배위평균뿐** — g(r) · Δμ/T_m · 자유에너지 프로파일 · 유한온도 DOS | **D = MSD 기울기 (동역학량)** | 🔴🔴 **여기서 갈라진다.** 전문 grep: `diffusion`·`transport`·`MSD`·`mean square`·`Green–Kubo`·`time-correlation`·`conductivity`·`viscosity` **전부 0회**. "correlation function" 6회는 전부 **radial** |
| **동역학 확장 가능성** | 논의 없음 | — | 🔴 **원리적으로 불가.** 재가중은 *"어떤 배열을 얼마나 자주 보나"* 를 고치지 *"그 배열에서 다음 순간 어디로 가나"* 를 못 고친다. `V` 를 바꾸면 힘이 바뀌어 **궤적 자체가 갈라진다** ⇒ ⛔ *"Imbalzano 를 따라 D 에 committee 불확실도를 붙였다"* 는 문장 **금지** |
| 시드/궤적 통계 축 | ⛔ **형식화 없음.** 정성 언급 3회뿐 (*"comparable"* · *"larger than the statistical error"* · *"somewhat scattered"*) | modelc Ea 3시드 **0.197±0.032 eV** · 단일시드 1.33× 철회(SEMIFINAL 2026-07-09) | ⇒ **우리 시드축을 이 논문이 도와주지 않는다.** 우리 규율이 이 논문보다 이 축에서 **앞서 있다** |
| 비선형 유도량 | `Fig. 6` T_m = 선형적합의 **근**(=계수의 비) → **멤버별 적합 → 멤버별 T_m^(i) → 산포**. `Fig. 7` 대칭 Δp → `−kT log` → **비대칭 구간** | 우리 Ea = Arrhenius **로그 기울기**, D_rel = **비** | ⭕ **절차만 이식**: 멤버별로 끝까지 계산 후 산포. ⚠ **M=1 이라 모델축에선 실행 불가**, 시드축 짝짓기는 **정당화되지 않는다**(다른 계·다른 궤적. 시드번호가 같은 것은 난수열이 같을 뿐 물리적 상관이 아니다) |
| 온도 의존 | `Eq. 28` 에 **β = 1/k_BT 가 앞에 붙는다** — 같은 공분산이면 고온일수록 σ_V 가 작다 | 600/800/1000 K | ⚠ 우리 온도가 이 방향으로는 유리하다. 단 **공분산 자체가 고온에서 커질 수 있어 순효과는 미정** (내 관찰, 논문 미논의) |

**🔴 이 축에서 제일 중요한 두 줄**

1. **우리 D 오차막대의 이름이 틀렸다.** 이 논문이 형식화한 분해(`σ_a` + `σ_V` vs 통계)로 재면,
   우리가 지금 낼 수 있는 것은 **통계(시드/블록) 오차막대**이고 **모델 불확실도가 아니다**.
   ⇒ `db/properties/` 와 원고 캡션의 *"uncertainty"* 를 **`seed/statistical spread`** 로 명시한다
   (우리 **Q7** 판정 — *"창 4개의 max−min 은 불확도가 아니다"* — 과 같은 계열의 정정).
2. **이 논문의 통계를 우리 이종 committee 에 이식하면 안 된다.** 가정 셋이 다 깨진다:
   (i) **같은 `y_ref`** — OMat24 vs MPtrj 로 훈련셋·DFT 설정이 달라 세 모델의 target 이 같은 함수가 아니다.
   (ii) **교환가능** — MACE-MP-0 과 SevenNet-0 이 **둘 다 MPtrj** 라 상관, 실질 표본은 3이 아니라 ≈2 클러스터
        (§J-5 가 이미 지적한 것과 같은 얘기).
   (iii) **가우시안** — 참조라벨이 없어 검증 불가.
   ⇒ 남는 것은 **순서적 신호**(이 배열이 다른 배열보다 합의 밖이다)뿐이고, 그게 정확히
   `tools/ionic/mlip_committee.py analyze` 가 하는 일이다. **이 논문은 그 도구를 정당화해 주지 않는다** —
   오히려 M=3 · 상관 · 비교환성을 **전부 지적하는 쪽**이다.
   ⭕ 다만 **한 가지는 우리 편**: α 논리가 *"committee 산포는 절대오차가 아니라 교정이 필요한 대리지표"* 라고
   말하므로, 문턱을 **상대적으로만** 쓰고 기준선을 **별도 표본**에서 잡는 우리 방식이 이 논문 정신과 맞다.

**⚠ 우리 도구 표기 정정 (2026-09-09, 코드 재독)**
`tools/ionic/mlip_committee.py` 의 **`force_contrast` 는 이종 committee 가 아니다.**
`cmd_force_contrast`/`contrast_from_forces` 는 **한 엔진(기본 UMA)의 예측을 파일 안 DFT 라벨과 비교**해
골격 힘오차를 내고 그것을 **test 계 / control 계의 비 R** 로 만든다
(카드 `db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json`).
**이종 3종 committee 는 `sample` → `predict --engine {uma,mace,sevennet}` → `analyze` 경로**이고,
[Imbalzano21] 과 대응하는 것은 **`analyze`** 쪽이다. 위 표는 `analyze` 기준으로 읽는다.

**🔧 우리 산술 (논문 주장 아님)**
- 편향 배율 `√[(M−1)/(M−3)]`: M=4 **1.73** · 5 1.41 · 6 **1.29** · 8 1.18 · 16 1.07.
- M 표본 SD 의 상대오차 `1/√(2(M−1))`: M=3 **50 %** · 4 40.8 % · 6 31.6 %.
  ⇒ **3점으로 낸 ± 는 그 자신이 ±50 % 다.**
- `Fig. 9` 자체검산: figure-read M=16 무편향 α ≈ 2.77 을 참값으로 `Eq. A1` 에 넣으면
  M=4 편향판 4.88 (그림 4.6), 역변환 무편향 2.61 (그림 2.62) — **식과 눈금 판독이 자기일관적**.
```

---

## ④ 병합 시 확인할 것

- **talk 역링크 불필요**: `litdb/talks/lee2026_skku_mlip_materials_design.md` 의 인입 대기열 6건에
  **이 논문은 없다** (그 큐는 MTP/SevenNet/GNoME/Kim/Shin/Luo 계열). 확인함.
- **`properties/`**: 해당 물성 파일 없음 (물성값 0건).
- **`db/` 미수정** (지시대로).
- **git 미커밋** (지시대로).
- 그림 9장 중 **`fig_7.png` 은 내가 수동 복구**했다 — `extract_figures.py` 의 기하검증이
  벡터 draw op 부족(`img0/draw5`)으로 오탈락시켰다. `figures.json` 의 `f7` 항목에 `note` 로 남겨 뒀다.
  ⇒ 도구 개선 후보: **matplotlib 벡터 라인플롯이 draw op 5개로 잡히는 경우**가 있다.

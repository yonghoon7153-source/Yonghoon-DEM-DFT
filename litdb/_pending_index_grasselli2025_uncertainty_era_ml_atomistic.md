# ⏸ 병합 대기 — `grasselli2025_uncertainty_era_ml_atomistic`
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09 · litdb-curator 4개 동시 실행으로 **`INDEX.md`·`comparison_vs_ours.md` 직접 수정 금지**를
> 받아, 넣어야 할 내용을 여기 적어 둔다. 충돌이 풀리면 **아래 두 블록을 그대로 옮기고 이 파일을 지운다.**
>
> ⛔ 이 논문은 **물성값 0건**이다 → **A/B/C/D 물성 4축 표에 넣지 않는다.**
> `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만 둔다 (shapeev2016 · park2024 선례).

---

## ① `INDEX.md` 에 추가할 행

| `papers/grasselli2025_uncertainty_era_ml_atomistic.md` | **[외부·methods·★MLIP 불확실도 축 지도(map) 편]** **F. Grasselli\*** (Modena e Reggio Emilia + CNR NANO S3), **S. Chong** (EPFL COSMO), **V. Kapil** (Cambridge + UCL), **S. Bonfanti** (Milano + NOMATEN), **K. Rossi\*** (TU Delft), "**Uncertainty in the era of machine learning for atomistic modeling**" (***Digital Discovery* 2025, 4, 2654–2675**, DOI `10.1039/d5dd00102a` · CC-BY 4.0 · 접수 2025-03-11 / 채택 2025-06-05; 본문 22 pp · **SI 없음** · Fig **8개** · **Table 0개** · refs **156** · Appendix A/B/C) — **Perspective. 계산 0회·신규 데이터 0건**(저자 선언: *"no primary research results, software or code … no new data were generated or analysed"*). 배터리·황화물·아르지로다이트 **0회**, σ·Ea·ESW·gap·탄성 **0건**. **핵심 기여** = 선형회귀·GPR·NN(Laplace)·**마지막층**·MoE·D-optimality·MIG 가 전부 **하나의 마할라노비스 형태 `σ²_★ = α² f_★ᵀ G f_★`(식 1)** 로 귀착됨을 유도. **★★ 우리에게 값진 판정 4개**: ①**캘리브레이션 편향보정 식 (27) 은 `M ≥ 4` 를 요구**(`(M−3)/(M−1)` 가 M=3 에서 0 → `α² = −1/3 < 0`; 부호전환점 `M=2+√3≈3.73` 은 우리 산술) ⇒ **우리 `force_contrast` M=3 은 단위 있는 오차막대를 원리적으로 못 붙인다** — "절대 σ 인용 금지" 규율의 식(式) 근거 ②**§2.8 = 관측량 전파 절**. 힘·에너지 → **차이량**(상관 덕에 절대값보다 훨씬 작다) → **정적/열역학 평균(RDF·⟨E⟩)은 Imbalzano reweighting 식 (31) 로 궤적 1개 + 사후 재가중**까지 간다. 🔴 **그러나 시간의존 상관함수 = 스펙트럼·수송계수는 "rigorous theory 부재"로 저자들이 열린 문제로 남긴다** — **우리 보고량 `D_rel`(확산계수 비) 이 정확히 그 자리**이고, 현재 유일한 길이 저자들이 *"time-consuming, brute-force"* 라 부른 **멀티궤적**(= 우리 3-seed) ③**§4.1 단일 파운데이션 모델 UQ 처방 = 마지막층 Laplace(식 14) 하나뿐**(ref 142 Mazitov et al. arXiv 2503.14118, *"almost no additional computational load"*) + *"**커뮤니티 벤치마크가 불확실도와 그 전파를 거의 안 본다**"* ⇒ **"UMA 가 Matbench 에서 좋다"에서 우리 D_rel 신뢰도를 유도 금지** ④**§2.9 오설정**: 앙상블 멤버 **전원이 같은 틀린 예측에 합의**할 수 있고 **전역 캘리브레이션으로 못 고친다** — 우리 봉인 `mlip_applicability`(*"점수와 검증이 같은 퍼텐셜이라 함께 틀리면 상관은 오히려 좋아진다"*)와 **글자 그대로 같은 논증**. **★ UMA 언급**: §2.3.2 가 **Wood et al. (ref 40) = UMA 논문**을 **mixture-of-experts** 사례로 인용하고 MoE 전파식 `σ²_★=Σ_k p_k²σ²,⁽ᵏ⁾_★`(식 25)을 준다 — ⚠ **그 식은 전문가별 독립 데이터셋·`G⁽ᵏ⁾`·`α⁽ᵏ⁾` 와 Zeni 식 거리/밀도 라우팅(식 22–23)을 전제**하고, **UMA 라우팅이 그 구조인지 이 리뷰는 답하지 않는다** ⇒ ⛔ **식 (25) 를 "UMA 의 UQ 공식"으로 인용 금지**. **불확실도 4겹 분류**: ①epistemic(멤버 퍼짐) ②aleatoric(MV 모델 출력; ⚠ **DFT 라벨처럼 잡음 없는 관측에선 전부 "모델 편향"**, Heid ref 34 ⇒ **우리 계엔 이 칸이 없다**) ③**오설정**(§2.9) ④**표집/통계**(§2.8 *"the statistical one due to a poor sampling"*). ⇒ **우리 축 매핑**: 3-seed = ④ **깨끗이 일치** · `force_contrast`(UMA-OMat24 / MACE-MP-0-MPtrj / SevenNet-0-MPtrj) = ①이 **아니다** — §2.2 는 멤버가 *"equivalent models"*(같은 데이터 부분표집 또는 **훈련 시드**)여야 한다고 못 박으므로, 우리 것은 실질 **③ 오설정 대조 + §3.2 계열 위원회 OOD 프록시**. ⚠ **우리 "시드"는 MD 초기속도 시드이고 §2.2 의 훈련 시드가 아니다** (UMA 는 고정 체크포인트라 훈련시드 축이 원리적으로 없다). **캘리브레이션 권고 절차**(§2.4): 식(26)→작으면 **식(27)** → **log–log parity plot 의 선형성부터**(α² 는 log–log 에서 **강체 평행이동**이라 미캘리브레이션이어도 선형이어야 하고, **선형성이 나쁘면 전역 α² 로 못 고침 = 국소 α²(x) 필요 신호**) → **ENCE**(식 28) → **Pernot 층화로 consistency(예측σ 조건부) vs adaptivity(입력특징 조건부) 분리** → ⛔ **miscalibration area(CDF 면적)는 권하지 않음**(더 높은 모멘트를 섞어 봄). **전이성 3분류**(`Fig. 5`): Phase / Temperature(**고온→저온 일반화는 잘 되는 편** ⇒ 우리 600–1000 K 에 유리) / Compositional(**화학량비 + 새 원소; 후자는 "맞춤 기법 없이는 상당히 어렵다"** ⇒ 도판트 30종 캠페인의 정직한 한계 문장). **★ `Fig. 4` figure-read 소득**(캡션에 없는 것): 아래줄 **도넛(고리) 분포에서 convex hull 이 빈 중앙까지 in-distribution 으로 오판** — 밀도 기준은 그 구멍을 잡는다 ⇒ **비볼록 조성공간에서 "껍질 안이니 안전" 금지**. **`Fig. 8` figure-read**: 잠재특징 **센터링 여부만으로 `σ_★/α` 3.03 → 3.95 (~30 %)** (Appendix C 는 이를 **미해결로 남김**) ⇒ 우리가 LL-UQ 를 구현하면 센터링 여부 기록 필수. **`Fig. 2`**: `d^E`가 같아도 `d^M_A 3.18` vs `d^M_B 9.95`(3.13배). **저자 미해결 14건**(§6-5 표): 최상위가 **#4 시간의존 관측량 전파 이론 부재**(=우리 D_rel) · **#9 벤치마크가 불확실도를 안 본다** · **#6 전이성 표준정의 부재** · **#10 미세조정이 UQ 추정기에 주는 영향 미지**. **🔴 우리 지적 3건**: ①**§2.7 첨자 오식** — *"Kellner and Ceriotti**41**"* 인데 ref 41=**Musil et al.**, Kellner–Ceriotti 는 **ref 37** ②**§2.6 Tran 귀속 어긋남 의심** — 본문 첨자 51(=Tran & Ulissi *Nat. Catal.* 2018, 금속간화합물 AL)인데 서술은 *MLST* 2020 **ref 46**(Tran, Neiswanger, Yoon, Zhang, Xing, Ulissi = UQ 비교 논문)에 맞는다 ⚠**원 논문 2편 미확인, 단정 안 함** ③**NTK 방어가 현대 아키텍처를 커버 못 한다** — §2.1.3 은 DeePMD(3층×240)·Behler–Parrinello(2층×40) 각주로 *"깊이보다 넓다"* 를 방어하는데, **§4.1 이 다루는 파운데이션 모델(MACE·UMA)은 깊은 등변 메시지패싱 GNN** 이고 그 다리가 본문에 없다 ⇒ **우리가 LL 근사를 UMA 에 쓰려면 타당성을 스스로 검증해야 한다**. **⚠ 인용 편중**: 핵심 자리(refs 11·14·15·37·41·88·142)가 **EPFL COSMO/Ceriotti 계열** — *"의도적으로 제한된 대표 연구"* 선언은 있으나 **"필드의 합의"로 읽으면 안 된다**. **⚠ 정량 비교 0건** — 어느 UQ 가 낫다는 **저자 자신의 수치가 없다** ⇒ ⛔ *"이 리뷰가 방법 A 가 낫다고 했다"* 식 인용 전부 오용. **🔧 talk 교차소득**: §3.5.2 가 **γ 문턱의 "original paper" 로 Podryabinkin & Shapeev 2017**(*CMS* 140, 171, ref 108)을 지목 — `talks/lee2026_skku…` §99-10 3b′ 의 재귀속과 **같은 방향**(⚠ 리뷰 경유). 단 **비선형 일반화 귀속은 갈린다**: 이 리뷰 = **Gubaev 2018 *JCP* 148, 241727**(ref 113) vs 우리 `tools/ionic/mlip_committee.py` = **Gubaev 2019 *CMS* 156, 148** — **다른 두 논문**, 원문 미확인이라 도구 귀속 안 바꿈. **⛔ 물성 4축 편입 금지** → `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만. **그림 8/8 전부 실제 열람**(`Fig. 4` 는 자동 캡션앵커가 놓쳐 **수동 크로핑** — figures.json 에 `note` 표시). | **방법론(UQ 이론)·MLIP 불확실도 축 지도편** — 물성값 0, 계 비특정 |

---

## ② `comparison_vs_ours.md` §J-7 `🔧 방법 원전` 에 추가할 블록

**[Gra25UQ] `grasselli2025_uncertainty_era_ml_atomistic` — 불확실도 어휘·판정선의 정의 원본**
(⛔ 물성값 0건. A–D 4축 행 금지. 아래는 **정의**와 **우리 위치 판정**뿐이다.)

| 항목 | [Gra25UQ] 가 정의하는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **불확실도 4겹** | ①epistemic ②aleatoric ③**오설정**(§2.9) ④**표집/통계**(§2.8) | 축 2개(모델 / 시드·궤적) | 🔵 **재라벨 필요** — 아래 두 행 |
| **시드·궤적 축** | ④ *"the statistical one due to a poor sampling (i.e. too short trajectories)"* (§2.8) | 600 K **3-seed**, MSD 2–50 ps, `Ea 0.197±0.032 eV` | ✅ **깨끗이 일치.** 이름표 그대로 채택 |
| **모델 축 (`force_contrast`)** | §2.2 앙상블은 멤버가 **"equivalent models"**(같은 데이터 부분표집 / **훈련 시드**·MC dropout)여야 한다 | UMA(OMat24) · MACE-MP-0(MPtrj) · SevenNet-0(MPtrj) = **아키텍처도 훈련셋도 다름**, **M=3** | 🔴 **①epistemic 이 아니다.** 실질 **③오설정 대조 + §3.2 위원회 OOD 프록시** ⇒ ⛔ *"epistemic uncertainty"* 로 부르지 말 것 |
| **캘리브레이션 하한** | 식 (27) 편향보정 ⇒ **최소 M = 4** (`(M−3)/(M−1)`=0 at M=3 → `α²=−1/3<0`) | **M = 3** | 🔴 **단위 있는 σ 원리적 불가.** 우리 "절대 σ 인용 금지"의 **식 근거 확보**(종전엔 경험 관례) |
| **aleatoric 칸** | 잡음 없는 관측(=DFT 라벨)에서는 모든 편차가 **모델 편향** (Heid ref 34) | DFT 라벨 = 결정론적 | ✅ **우리 계엔 ② 칸이 없다.** `Fig. 3a` 빨간 상자 해당 없음 |
| **"시드"의 의미** | §2.2 의 시드 = **훈련 시드**(앙상블 멤버 생성) | 우리 시드 = **MD 초기속도 시드** | ⚠ **다른 것.** 섞어 쓰면 §2.2 와 §2.8 이 뒤엉킨다. UMA 는 고정 체크포인트라 **훈련시드 축이 원리적으로 없다** |
| **관측량 전파 도달점** | 힘/E → **차이량**(상관 덕에 작음) → **정적·열역학 평균**(식 31 reweighting, 궤적 1개) | — | ✅ **정적 지표(RDF·배위수·⟨E⟩)에는 지금 당장 위원회 오차막대 가능** |
| **수송계수 전파** | 🔴 *"rigorous theory"* **부재**. 현재는 **멀티궤적 brute-force 뿐** | `D_rel` = 확산계수 비 = **수송계수** | 🔴 **우리 3-seed 가 문헌이 아는 전부.** 뒤처진 게 아니라 **분야 한계**. 단 그것은 ④만 재고 **①은 시드를 늘려도 안 채워진다** |
| **`D_rel` 이 비(ratio)인 것** | §2.8(c): ML 오차는 가까운 배치에 **고도로 상관** ⇒ **차이의 불확실도 ≪ 절대값** | 설계/host 를 **같은 모델**로 | ✅ **설계 정당화.** ⚠ 저자 논증 대상은 **에너지 차이**이고 수송계수 비가 아니다 — **유추임을 밝히고 인용** |
| **단일 uMLIP UQ 처방** | **마지막층 Laplace, 식 (14)**, 추론 부담 거의 0 (§4.1, ref 142) | 없음 | 🔵 **다음 계산 1순위.** 라벨 검증셋 후보 = `db/properties/mlip_bench_li3ps4_uma.json` (PET-MAD Li₃PS₄ 243구조 PBEsol) ⚠ **Cl 부재 = "critical subdomain underrepresented"** |
| **UMA = MoE 분류** | §2.3.2 가 **ref 40 (Wood et al., UMA)** 을 MoE 사례로 인용, 식 (25) 제공 | UMA-s-1p1 | ⛔ **식 (25) 를 UMA 에 적용 금지** — 식은 전문가별 독립 데이터셋·`G⁽ᵏ⁾`·`α⁽ᵏ⁾` + Zeni 라우팅 전제. **UMA 라우팅 구조를 이 리뷰가 확인해 주지 않는다** |
| **오설정 = 우리 봉인 논증** | 앙상블 전원이 같은 틀린 예측에 합의 → **인위적으로 낮은 σ**, **전역 캘리브레이션으로 불가** | 봉인 `mlip_applicability`: *"점수와 검증이 같은 퍼텐셜이라 함께 틀리면 상관은 오히려 좋아진다"* | ✅ **독립 도달 확인.** 우리 논증이 문헌 표준과 동일 |
| **전이성 3분류** | Phase / Temperature(**고온→저온 일반화 양호**) / Compositional(**새 원소 외삽은 맞춤기법 없이 어렵다**) | 상(결정↔무질서) · 600–1000 K · 도판트 30종 | ⚠ **세 갈래 동시**. 세 번째가 저자들이 어렵다고 한 그것 ⇒ 봉인의 *"UMA 내부 순위로만"* 이 옳다 |
| **OOD 판정법** | ⛔ convex hull(고차원 붕괴 + **비볼록 구멍 오판**, `Fig. 4`) / ✅ **적응 k-NN 밀도(식 32)+TwoNN 내재차원** · GMM NLL · 하우스도르프 | 없음 | 🔵 후보 — cascade 조성공간이 비볼록일 위험 |
| **γ(외삽등급) 원전** | §3.5.2: *"original paper by **Podryabinkin and Shapeev**"* (ref 108, *CMS* 140, 171, 2017) | `talks/lee2026_skku…` §99-10 3b′ 의 재귀속 후보 | ✅ **같은 방향의 외부 증언** ⚠ **리뷰 경유** — 1차 근거 아님 |
| **γ 비선형 일반화 귀속** | **Gubaev 2018, *JCP* 148, 241727** (ref 113) | `tools/ionic/mlip_committee.py` = **Gubaev 2019, *CMS* 156, 148** | ⚠ **서로 다른 논문.** 원문 미확인 ⇒ **도구 귀속 안 바꾼다** |

**⛔ [Gra25UQ] 에서 인용하면 안 되는 것**
1. 리뷰가 요약한 **2차 수치** 전부 — 전이성 관행 문턱(**10 meV/atom · 100 meV/Å**), γ 문턱(**≲1 / ≫1**),
   앙상블 통상 크기(**5–10**), Kellner–Ceriotti 물의 **N·√N**, DeePMD **3층×240**. 전부 `[리뷰경유]`.
   → 원 논문 확인 전 **우리 표의 1차 근거 금지**.
2. *"이 리뷰가 방법 A 가 B 보다 낫다고 했다"* — **저자 자신의 정량 비교가 0건**이다.
3. `Fig. 6`·`Fig. 7` 의 축 값(eV/atom 등) — **합성 데이터로 판단**(확인은 못 함).
4. **이 논문으로 "우리 UMA 결과가 신뢰할 만하다"를 주장** — 이 논문은 재는 법을 말하지 우리 점수를
   말하지 않는다. **오히려 우리가 ①을 안 재고 있다는 것을 드러낸다.**

---

## ③ 병합자에게 남기는 메모

- **PDF 를 `litdb/inbox/` 로 옮기지 못했다** (쓰기 범위 제한). 원본:
  `/root/.claude/uploads/82ea256b-12bc-5a75-994e-7718d79c71ba/295b265a-81._Uncertainty_in_the_era_of_machine_learning_for_atomistic_modeling.pdf`
  → 나중에 그림 재추출을 하려면 이 파일을 `litdb/inbox/` 에 넣고 `pdf_map.tsv` 에 등록해야 한다.
  (`litdb/figures/_sources.json` 에는 업로드 경로 기준으로 이미 색인됐다.)
- **`litdb/talks/lee2026_skku_mlip_materials_design.md` 는 건드리지 않았다.** 이 논문은 그 talk 의
  §99-10 인입 대기열 6건에 **들어 있지 않다** ⇒ 양방향 링크 의무 없음. 다만 위 §J-7 마지막 두 행
  (γ 원전 / 비선형 귀속)은 그 talk §99-10 3b′ 와 **내용상 연결**되므로, 병합자가 원하면
  talk 쪽에 *"외부 증언: [Gra25UQ] §3.5.2 (리뷰 경유)"* 한 줄을 달아도 좋다. **필수는 아니다.**
- `db/` 는 손대지 않았다. 위 표의 🔵 항목(마지막층 Laplace 등)은 **제안일 뿐 등록된 결정이 아니다** —
  실행하려면 `kb/templates/estimand_card.md` (보고량 카드)부터.

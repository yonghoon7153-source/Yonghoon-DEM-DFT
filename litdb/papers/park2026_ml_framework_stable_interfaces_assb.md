<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-22 신규 작성. 1저자 지정 읽기축:
       🔴 이 digest 의 존재 이유는 **선행연구 판정**이다. `wu2026_ml_driven_electrolyte_interface_design_review`
          §12a/§J-20 이 이 논문을 *"우리 최근접 선행연구 후보 1순위"* 로 지목하고
          **"원문 확인 전까지 '선행 없음' 이라고 쓰지 마라"** 라고 못박아 뒀다. 그 확인이 이 파일이다.
       ⇒ 본체는 §0b(예측 검증) · §7(우리 §B/§D/§2b/§E 와의 대조) · §10(비판) · §13(우리가 여전히 주장할 수 있는 것).
       ⇒ litdb 에 이미 있는 계보(Richards16·Xiao19·Aykol16·Nolan18)는 반복 서술하지 않고 §2c 지도 한 줄로 처리.
     크로핑 11장(그림 9 + 표 2) + 도구가 오탐으로 버린 Fig 2·4·7 을 페이지 직접 렌더로 회수 →
     **본문 그림 6장 전부 + SI 그림 3장 = 9장을 실제로 봤다**. 목록은 §0c. -->

# Machine-Learning Framework for Designing Stable Interfaces in All-Solid-State Lithium-Ion Batteries — Park, Jang et al. (*Advanced Science* **2026**, 0:e76305)

> slug `park2026_ml_framework_stable_interfaces_assb` · DOI `10.1002/advs.76305` · type `DB-thermo + ML (자체 DFT 0 · 자체 실험 0 — MP 총에너지를 pymatgen 상도로 소비)` · PDF `litdb/inbox/125. AdvSci_2026_Park_ML_framework_stable_interfaces_ASSLIB_MAIN.pdf` (본문 **13 pp** · Fig 1–7 · Table 0 · refs **79**) + `125. Sup) …_SI.pdf` (SI 10 pp · Fig S1–S5 · Table S1–S2 · refs 6) · digested `2026-09-22` · status ✅ · 태그 **[외부·🔴최근접 선행연구]**

> elements: Li, P, S, Cl, Br, O, N, F, B, Si, Al, Mg, Ca, Zn, Ga, Zr, Hf, Sc, Y, La, Gd, Dy, Ho, Er, Lu, Tm, Ni, Co, Mn, Fe, Ge, Be, Ba, Sr, Bi, W, Sb, In
> methods: DFT

> ⚠ **`methods: DFT` 의 뜻** — 저자들은 **DFT 를 한 번도 직접 돌리지 않는다.** Materials Project 의
> DFT 총에너지를 pymatgen 으로 불러 상도(phase diagram)를 풀 뿐이다. 태그 어휘에 "hull/phase-diagram" 이
> 없어 `DFT` 로 둔다. **ESW·NEB·AIMD·MLIP·COHP 는 하나도 없다** — 저자 스스로 ESW 를 *"향후 과제"* 로 적었다(§5.6).
> ⛔ **이 파일의 수치는 전부 소환값이다.** `db/properties/*` 에 이식 금지.
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md`
> 하나뿐이고 **이 논문은 그 대기열(#1–#9, MTP/SevenNet/SKKU 계열)에 없다** ⇒ 역링크 작업 없음.

> **저자**: **Sehyeok Park**^a†, **Myeongcho Jang**^{a,b†} (†공동1저자), **Hun-Gi Jung**^{a,c,d}, **Kyung Yoon Chung**^{a,c}, **Seungho Yu\***^{a,c} —
> ^a **KIST 에너지저장연구센터**(서울 성북구 화랑로 14길 5) · ^b **고려대 기계공학부** · ^c **UST KIST School 에너지·환경기술** · ^d **성균관대 에너지과학 + KIST-SKKU 탄소중립연구센터**.
> 교신 `shyu@kist.re.kr`. 투고 2026-04-12 / 수정 2026-05-22 / 수락 2026-06-13 · OA CC BY.
> 과제: KIST 기관고유(26E0321, 26E0323) · NRF(RS-2024-00404414, RS-2025-23523434) · NST(GTL24012-000).
>
> 🔴 **전원 국내 기관이다 (KIST 주도).** 경쟁 관계가 지리적·제도적으로 직접적이다.
> 🔴 **이 논문은 단발이 아니라 시리즈의 3편째다** — 같은 교신(Yu)의 앞선 두 편을 self-cite 한다:
> ref 28 **Kim·Jang·Yu**, *"Rational Materials Design for Stable Interfaces in All-Solid-State **Potassium**-Ion Batteries"*, *J. Mater. Chem. A* **13**, 39013 (2025);
> ref 29 **Jang·Kwon·Jeon·Kim·Yu**, *"Interfacial Stability and Design Strategies for **Halide** Solid Electrolytes in High-Voltage All-Solid-State **Sodium**-Ion Batteries"*, *Small Methods* **10**, 02179 (2026).
> ⇒ **K-ion → Na-ion 할라이드 → Li-ion 황화물 코팅** 순으로 같은 hull 반응에너지 기계를 계(system)만 바꿔 돌리고 있다.
> **다음 편이 "도펀트" 또는 "전압 축" 일 위험을 전제하고 우리 일정을 잡아야 한다** (§13-3).

---

## 0a. 이 digest 를 읽는 법 — 판정이 먼저다

이 논문의 제목은 우리가 하는 일과 **이름이 같다**(*ML Framework for Designing **Stable Interfaces** in ASSB*).
그래서 이 digest 는 요약문이 아니라 **판정문**으로 쓴다. 결론을 먼저 박아 둔다:

> **🟢 판정: 우리 §B(전압 축 grand-potential 계면 반응성)·§D(Nd 기전)·§2b(보호율 닫힌 식)·§E(dual compatibility 의 정면 충돌) 중
> 어느 것도 이 논문이 선점하지 않았다. 단, §B 의 *닫힌계 하위층*은 정확히 같은 양이고, "란타나이드 + 폴리음이온 + O 가
> 저반응성 계면상" 이라는 *조성 수준의 관찰*은 이 논문에 이미 있다.**
>
> 갈리는 지점은 세 개이고, 셋 다 **원문에서 문장으로 확인했다**:
> 1. **전압 축이 없다.** 이 논문의 `E_reaction` 은 **닫힌계**(Richards 2016 식) 다. `grand potential`·`applied potential`·
>    `μ_Li`·`state of charge` 는 본문·SI 전체에 **0 회**다. 우리 §B 의 2.5–4.5 V 6점 축이 여기엔 없다.
> 2. **in-situ 가 없다.** `in situ`/`in-situ`/`ex situ` 가 본문·SI 전체에 **0 회**다. 처방은 전부
>    *"precursor-based synthesis, wet-chemical coating, or thin-film deposition"* — **밖에서 바르는 층**이다.
> 3. **정량 모델이 없다.** `coverage`(물리적 의미) · `passivat*` · `scaling law` · `closed-form` 이 **0 회**다.
>    산출물은 **후보 목록과 순위**이지 닫힌 식이 아니다.
>
> ⚠ **확인하지 못한 범위**: 데이터 가용성 문장이 *"supplementary material 에 있다"* 라고만 하고
> **후보 전체 목록(809 종 · 확장 521 종)의 기계판독 파일이 SI 에 없다.** SI 는 그림 5 + 표 2 뿐이다.
> ⇒ **"그 809 종 안에 Nd 화합물이 없다"** 는 우리가 확인할 수 없다. 확인한 것은 **확장 M-pool 에 Nd 가 없다**는 것뿐(§4d).

---

## 0b. 🔴 예측 검증 — 우리 리뷰 digest 가 원문 없이 적어 둔 3+2 가지

`wu2026_ml_driven_electrolyte_interface_design_review` §12a·§J-20 이 원문 미확보 상태에서 적어 둔 내용을
원문과 하나씩 대조한다. **이 표가 이 digest 의 핵심이다.**

| # | 리뷰가 적어 둔 것 | 원문 확인 | 판정 |
|---|---|---|---|
| ① | **809 Li 화합물 × 10 산화물 양극 × 7 황화물 전해질** | Methods: *"Only entries with E_hull = 0 meV/atom were retained … yielding **809** compounds"* · 양극 **10** 종 · SSE **7** 종 (`Fig. 1a` 가 7×10 행렬) | ✅ **글자 그대로 정확** |
| ② | **비지도 군집으로 저반응성 설계영역 정의** | HDBSCAN 으로 noise 제거 → **k-medoids k=4** (Ward·spectral·GMM·Leiden 과 벤치마크, `Fig. S2`) → 군집 지문(`Fig. S3`) → **Cluster 3**(310 종, O–P 중심)을 설계영역으로 채택 | ✅ **정확** |
| ③ | **Park 에는 피복률 법칙이 없다** | `coverage`·`passivat*`·`scaling law`·`closed-form`·`analytic` 전수 검색 **0 회**. 산출은 순위 목록 + `⟨E_reaction⟩_OC`/`⟨E_reaction⟩_SSE` 두 스칼라뿐 | ✅ **정확 — 닫힌 식 없음** |
| ④ | **갈리는 지점 = ex-situ 코팅 선택 vs in-situ 도펀트 보호상** | `in situ`/`in-situ`/`ex situ` **0 회**. 처방은 *"precursor-based synthesis, wet-chemical coating, or thin-film deposition … either as coating phases or as interfacial layers on representative oxide cathode particles"* = **전부 ex-situ 증착** | ✅ **정확, 그리고 더 강하다** — 저자들이 in-situ 를 *배제*한 게 아니라 **개념 자체를 꺼내지 않는다** |
| ⑤ | *(리뷰에 없던 것)* **"Li 함량이 산화한계를 정한다" 형 축** | `Li fraction`·`Li content`·`Li-rich`·`Li-poor`·`Li/P` 전수 검색 **0 회**. 서술자는 MAGPIE 조성통계이고 상위 10 개에 Li 관련 항이 **없다**(`Fig. 4b`) | ✅ **없다** — Xiao 2019 형 Li-분율 축을 계면으로 확장하지 **않았다** |

**⇒ 리뷰 digest 가 원문 없이 적은 4 가지가 4/4 맞았다.** 그 판정을 이제 원문 근거로 승격한다.

---

## 0c. 본 digest 에서 **실제로 본 그림 / 안 본 그림**

> **본 것 (9장)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 7` `Fig. S2` `Fig. S4` `Fig. S5` — **본문 그림 6장 전부 + SI 그림 3장**.
> ⚠ `Fig. 2` `Fig. 4` `Fig. 7` 은 `extract_figures.py` 가 *"그래픽 없음"·"영역 없음"* 으로 **오탐 배제**했다
> (벡터 드로잉 12만 개짜리 페이지인데 기하검증이 실패). **페이지 3·5·7 을 직접 렌더해 회수했다.**
> `Fig. 7` 은 이 논문의 헤드라인 결과라 놓쳤으면 digest 가 성립하지 않았다.
>
> **안 본 것**: `Fig. 6` 은 봤고(아래), `Fig. S1` `Fig. S3` 은 **이미지로는 안 봤다** —
> 두 장 다 수치가 PDF 텍스트 층에 전부 들어 있어 텍스트로 옮겼다(§3f, §5.2). `Table S1` `Table S2` 는 표라서 텍스트로 읽었다.
> 정정: `Fig. 6` 도 봤다(크로핑본). ⇒ **본문 6/6 · SI 3/5 · 표 0/2(텍스트로 대체)**.
>
> **그림에서만 읽은 값은 `figure-read ≈` 로 표시**했다.
> 🟢 **`Fig. 1a`·`Fig. 7` 의 셀 숫자는 figure-read 가 아니다** — 히트맵 셀에 숫자가 **활자로 인쇄**돼 있고,
> PDF 텍스트 층 덤프와 **자리·값이 모두 일치**함을 교차확인했다. 그래서 정확한 인용값으로 쓴다.
>
> **본문 서술과 어긋난 것**: 있다. 3 건이고 §10 에 적었다
> (`Fig. S2` 의 RSD 주장 · `Fig. 4a` R² 의 성격 · `Fig. S4` 의 gap 정의 불일치).

---

## 1. 한 줄 요약

**황화물 SE ↔ 산화물 양극 계면은 코팅 없이는 열역학적으로 못 쓴다(70 쌍 평균 −332 meV/atom)** 는 것을 다시 못박고,
**MP 의 상안정(E_hull = 0) Li 화합물 809 종**에 대해 그 계면 반응에너지 벡터를 전부 계산한 뒤
**비지도 군집으로 "저반응성 조성 지문"(O 중심 + B/P/Si 폴리음이온 + 고정원자가 금속)** 을 뽑고,
그 지문 안에서 **전하중성 Li–M–O / Li–M–A–O 를 521 종 새로 생성**해 **XGB+HGBR 대리모형**으로 순위를 매긴 논문이다.
**새로 발견한 물리는 없다** — 기여는 *"DB 에 없는 조성까지 같은 열역학 잣대로 줄 세우는 파이프라인"* 이다.

---

## 2a. 메타

| 항목 | 값 |
|---|---|
| 저자 | S. Park†, M. Jang†, H.-G. Jung, K. Y. Chung, **S. Yu\*** (KIST / 고려대 / UST / SKKU) |
| 저널/년 | *Advanced Science* **2026**, 0:e76305 (OA) |
| DOI | `10.1002/advs.76305` |
| 대상 계 | **황화물 SE 7 종** × **산화물·올리빈 양극 10 종** × **코팅 후보 809 (학습) + 521 (생성)** |
| 연구유형 | **DB 열역학 스크리닝 + 지도/비지도 ML.** 자체 DFT 0 · 자체 실험 0 · 실험 검증 0 |
| 자체 계산량 | pymatgen 상도 풀이 (809+521) × 17 쌍 ≈ **2.2 만 회** + ML 학습 |

## 2b. 이 논문이 실제로 묻는 질문

> *"코팅 후보를 고르고 싶은데 DB 에 든 상안정 Li 화합물이 809 종뿐이다.
> **DB 밖으로, 그러나 통제된 방식으로** 후보를 늘릴 수 있는가?"*

답: **군집이 정한 조성 지문 안에서만 생성**하고(신규성 추구가 아니라 *guided exploration*),
생성물은 **전구체 분해 hull** 로 proxy label 을 붙여 같은 잣대에 올린다.

⚠ **이 질문은 "어떤 물질이 왜 안정한가" 가 아니다.** 저자들도 그렇게 못박는다 —
*"these descriptors should be interpreted as composition level proxies rather than deterministic design rules"* ·
*"A dedicated causal attribution of individual descriptors remains beyond the scope of this work."*

## 2c. litdb 계보 안에서의 자리 (반복 서술 안 함)

| 계보 | 이 논문과의 관계 |
|---|---|
| `richards2016_interface_stability_pseudobinary` (**우리 방법 원전**) | **인용한다(ref 51) · 확장하지 않는다 · 대체하지 않는다.** 식 (1)–(3) 이 Richards 의 pseudo-binary 를 **문자 그대로 재기술**한 것이다. **차이는 Richards 가 가진 개방계(Li·O 열린 축) 확장을 이 논문이 쓰지 않는 것**이다 — §4b |
| `xiao2019_cathode_coating_screening` | 인용한다(ref 50). **같은 코팅 스크리닝 문제·같은 잣대.** 차이 = Xiao 는 만충/반충 두 상태 + Li-분율 해석, Park 은 만충 단일 상태 + ML 확장 |
| `aykol2016_ht_cathode_coating_design` / `aykol2014_cathode_coating_thermodynamics` | 인용한다(ref 13). 이미 그 digest 가 다룬다 |
| `nolan2018_computation_accelerated_design_review` | ref 19 로 인용(Nolan 2021 ES M 쪽). 어휘집 역할은 그 digest 가 다룬다 |
| `wu2026_ml_driven_electrolyte_interface_design_review` | **이 논문을 ref 139 로 인용하는 리뷰다.** 그 digest 의 §12a·§J-20 이 이 판정의 출발점 |
| `honrao2021_interpretable_ml_sse_anode_coatings` · `sendek2017_ml_screening_12k_conductors` · `jain2026_ml_pipelines_solid_state_electrolyte_design` | **ML 방법 층위는 이미 그 digest 들이 다룬다.** 이 논문의 신규성은 방법이 아니라 *"열역학 라벨로 조성공간을 확장"* 이라는 조합 |
| `cha2024_dualcompatible_halide_ncm_lpscl_interface` | **dual compatibility 개념의 선례.** Park `Fig. 2b` 가 그 길항을 809 종 통계로 보여준다 — §5.2 |
| `liang2026_interface_bottleneck_solid_state_batteries` · `miao2023_role_of_interfaces_solid_state_batteries` · `tu2026_diffusion_descriptor_ml_li_sse_interface` | 겹치는 대목 없음(운동학·수송 축) |

---

## 3. 핵심 수치 총정리 ★ (전부 소환값)

### 3a. 데이터셋 규모

| 항목 | 값 |
|---|---|
| 코팅 후보 (학습) | **809** 종 — MP 의 Li 함유 화합물 중 **E_hull = 0 meV/atom 만** |
| 산화물·올리빈 양극 | **10** 종 |
| 황화물 SSE | **7** 종 |
| 반응성 벡터 차원 | **17** (= 10 + 7) |
| 저반응성 기준 | **E_reaction ≥ −50 meV/atom** |
| 기준 통과 | **53 / 809 = 6.6 %** |
| 군집 | HDBSCAN noise 제거 후 **k-medoids k = 4** |
| Cluster 3 (설계영역) | **310** 종 |
| 생성 조성 | **521** = Li–M–O **144** + Li–M–A–O **377** |
| 적용가능영역 | core(≤p90) **94.6 %** · boundary(≤p95) **97.9 %** · 극단 외삽 **0** |

### 3b. 🔴 `Fig. 1a` — 코팅 없는 SE↔양극 반응에너지 전수 (meV/atom, 인쇄값)

> **행 = SSE, 열 = 양극. 값이 음수일수록 분해 구동력이 크다.**
> 🟢 이 표는 셀에 활자로 인쇄된 값이고 PDF 텍스트 층과 교차확인했다 — figure-read 아님.

| SSE \ 양극 | LiFe₀.₅Mn₀.₅PO₄ | LiFePO₄ | LiMn₂O₄ | LiNi₀.₅Mn₁.₅O₄ | NMC111 | NMC622 | NMC811 | LiNi₀.₈Mn₀.₂O₂ | NCA(811) | NMC955 |
|---|---|---|---|---|---|---|---|---|---|---|
| Li₃PS₄ | −86 | −132 | −350 | −386 | −380 | −434 | −479 | −452 | −488 | −503 |
| Li₇P₃S₁₁ | −83 | −128 | −383 | −427 | −418 | −475 | **−523** | −495 | −529 | **−548** |
| Li₁₀GeP₂S₁₂ | −94 | −136 | −271 | −304 | −302 | −357 | −406 | −377 | −418 | −433 |
| Li₁₀SiP₂S₁₂ | −108 | −152 | −327 | −361 | −356 | −408 | −454 | −427 | −463 | −477 |
| **Li₆PS₅Cl** | −100 | −142 | **−263** | −289 | −289 | −333 | −377 | −352 | −388 | −401 |
| **Li₆PS₅Br** | −100 | −142 | −263 | −289 | −289 | −333 | −377 | −352 | −388 | −401 |
| **"Li₅.₅PS₅Cl₁.₅"** ⚠ | −94 | −135 | −277 | −302 | −301 | −345 | −390 | −364 | −402 | −415 |

**전체 70 셀 평균 = −331.8 ≈ −332 meV/atom** (본문의 *"averaging ≈ −332 meV/atom"* 를 재계산으로 확인 — 저자는 어느 모집단인지 안 밝혔는데 **70 셀 전체**가 맞다).

**🔑 여기서 우리가 뽑아야 할 것 3 가지:**

**(1) 아지로다이트가 황화물 중 가장 덜 반응한다.** 8 종 산화물 양극(올리빈 2 제외) 평균:

| SSE | 8 산화물 양극 평균 (meV/atom) | 순위 |
|---|---|---|
| **Li₆PS₅Cl = Li₆PS₅Br** | **−336.5** | **1위 (가장 온건)** |
| "Li₅.₅PS₅Cl₁.₅" | −349.5 | 2위 |
| Li₁₀GeP₂S₁₂ | −358.5 | 3위 |
| Li₁₀SiP₂S₁₂ | −409.1 | 4위 |
| Li₃PS₄ | −434.0 | 5위 |
| **Li₇P₃S₁₁** | **−474.8** | **7위 (최악)** |

⇒ **우리가 아지로다이트를 고른 것이 이 잣대에서 최선의 선택이었다는 외부 근거**다.
Li₇P₃S₁₁(P₂S₇ 함유)이 최악인 것도 P–S 결합 산화 논리와 맞는다.

**(2) 🔴🔴 Li₆PS₅Cl 과 Li₆PS₅Br 이 10 열 전부에서 비트 단위로 같다.** 10/10 셀이 완전 동일하다.
우연이 아니다 — 이 잣대는 **할로겐 정체(Cl vs Br)를 원리적으로 분해하지 못한다.**
(가장 그럴듯한 기전: LiX 가 양쪽 다 hull 상이고, 식 (3)의 자체분해 차감에서 할로겐 항이 정확히 상쇄된다.)
⇒ **우리 축 A(Cl-rich 가 빠르다)·축 B(Cl 의 산화 거동)를 이 잣대로는 물을 수 없다.** 우리 전압 축이 그래서 필요하다.

**(3) 🔴🔴 Cl 을 더 넣으면 이 잣대에서는 *더 나빠진다*.** Li₆PS₅Cl → "Li₅.₅PS₅Cl₁.₅":

| 양극 | Δ(Cl-rich − Cl) meV/atom |
|---|---|
| LiFe₀.₅Mn₀.₅PO₄ | **+6** (좋아짐) |
| LiFePO₄ | **+7** (좋아짐) |
| LiMn₂O₄ | −14 |
| LiNi₀.₅Mn₁.₅O₄ | −13 |
| NMC111 | −12 |
| NMC622 | −12 |
| NMC811 | −13 |
| LiNi₀.₈Mn₀.₂O₂ | −12 |
| NCA | −14 |
| NMC955 | −14 |
| **8 산화물 평균** | **−13.0 (나빠짐)** |

⇒ **축을 명명하지 않고 "Cl-rich 가 산화에 강하다" 고 쓰면 이 표에 반박당한다.**
이 표가 말하는 것은 **축 B③(닫힌계 양극 접촉 구동력)** 이고, 거기서 Cl-rich 는 **13 meV/atom 불리**하다.
(⚠ 단 Li 도 5.5 로 줄어 있어 **Cl 증가와 Li 감소가 교락**돼 있다 — §10-6.)

⚠⚠ **조성식 오기**: 논문은 본문 Methods·`Fig. 1a`·`Fig. 7` 전부에서 **`Li₅.₅PS₅Cl₁.₅`** 라고 쓴다.
이 식은 **전하중성이 안 맞는다** (양 10.5+ vs 음 11.5−). 의도한 것은 거의 확실히 **Li₅.₅PS₄.₅Cl₁.₅** 다
(= 우리 `modelc` 계열). **어느 MP entry 를 실제로 썼는지 SI 에 없어 확인 불가** ⇒ 이 행의 수치는
**"Cl-rich 아지로다이트 계열" 로만 인용하고 우리 modelc 와 1:1 대응시키지 않는다.**

### 3c. `Fig. 7` — 코팅을 넣었을 때 (헤드라인 결과, meV/atom, 인쇄값)

**요약 통계 (본문 명시)**: 코팅–양극 평균 **≈ −8** (범위 **−51 ~ 0**) · 코팅–SSE 평균 **≈ −17** (범위 **−105 ~ 0**).
⇒ **−332 → −8 / −17.** 이것이 논문의 판매 문장이다.

🔑 **범위의 양 끝(−51, −105)이 둘 다 같은 물질 `Li₂Zr₂O₅` 에서 나온다** (저자는 이 사실을 안 적는다).

**학습셋 코팅 10 종** (SSE 열 = Li₃PS₄ / Li₇P₃S₁₁ / Li₁₀GeP₂S₁₂ / Li₁₀SiP₂S₁₂ / Li₆PS₅Cl / Li₆PS₅Br / "Li₅.₅PS₅Cl₁.₅"):

| 코팅 | 양극 10 열 | SSE 7 열 |
|---|---|---|
| **Li₃PO₄** | 0,0,0,0,0,0,0,0,0,0 | 0, 0, −0, **−6**, 0, 0, 0 |
| Li₃B₇O₁₂ | −4,0,−2,0,−17,−17,−19,−20,−20,−22 | −0,−1,0,−0,−1,−0,−1 |
| LiBO₂ | −17,−17,0,0,−3,0,0,0,0,0 | −18,−25,−17,−19,−17,−17,−17 |
| LiAlO₂ | −19,−21,0,0,0,0,0,0,0,0 | −22,−27,−20,−25,−20,−20,−20 |
| LiAl₅O₈ | −7,−8,0,−20,−22,−24,−25,−25,−27 | −3,−14,−3,−15,−3,−3,−3 |
| Li₂BeSiO₄ | −6,−7,0,0,0,0,0,0,0,0 | 0,−18,−0,−2,0,0,0 |
| LiAlSiO₄ | 0,0,0,0,−7,−8,−9,−10,−11,−11 | 0,−5,−0,0,−2,0,−3 |
| Li₂Al(BO₂)₅ | −2,0,−0,0,−15,−16,−18,−19,−19,−21 | 0,0,−3,−0,−0,−0,0 |
| LiMgPO₄ | 0,0,−4,0,−21,−24,−26,−27,−27,−28 | 0,0,−2,−16,−11,−11,−6 |
| Li₂MgSiO₄ | −22,−23,−3,0,0,0,0,0,0,0 | −24,−34,−20,−25,−20,−20,−20 |

**확장 후보 — MP 수록 5 종**:

| 코팅 | 양극 10 열 | SSE 7 열 |
|---|---|---|
| **Li₂Hf₂O₅** | −0,0,0,0,0,0,−41,−38,−17,−13 | −62,−68,−56,−61,−55,−55,−55 |
| **Li₂Zr₂O₅** ⚠ | 0,0,0,0,0,0,−51,−48,−27,−23 | **−88,−105,−72,−85,−70,−70,−80** |
| LiAl(SiO₃)₂ | −15,−17,−19,−20,−18,−21,0,0,−2,0 | 0,−4,−0,0,−1,0,−1 |
| LiAlB₂O₅ | −15,−16,−19,−20,−18,−19,−3,−5,0,0 | −2,−8,−2,−6,−2,−2,−2 |
| LiCaPO₄ | 0,0,0,0,0,0,0,0,0,0 | −12,−15,−20,−33,−27,−27,−20 |

**확장 후보 — MP 미수록 5 종** (`Fig. 7` 회색 이탤릭, proxy label):

| 코팅 | 양극 10 열 | SSE 7 열 |
|---|---|---|
| LiAl₃O₅ | −11,−12,−14,−15,−13,−15,−7,−6,0,0 | −5,−12,−5,−12,−5,−5,−5 |
| Li₂Hf₃O₇ | −0,0,0,0,0,0,−34,−32,−14,−11 | −48,−53,−45,−48,−44,−44,−44 |
| **Li₆Zr(PO₅)₂** | 0,0,0,0,0,0,0,0,0,0 | −16,−17,−14,−14,−14,−14,−19 |
| Li₂Hf(BO₃)₂ | −3,0,0,0,0,0,−14,−14,0,0 | −14,−21,−13,−14,−13,−13,−13 |
| Li₃AlSi₂O₇ | −5,−6,−8,−8,−7,−9,−15,−14,0,0 | −10,−21,−9,−11,−11,−9,−11 |

**참조 행 (코팅 없음)**:
- LiFePO₄ vs 7 SSE: −132, −128, −136, −152, −142, −142, −135
- NMC955 vs 7 SSE: −503, −548, −433, −477, −401, −401, −415
- Li₆PS₅Cl vs 10 양극 / Li₁₀GeP₂S₁₂ vs 10 양극: `Fig. 1a` 와 동일

**🔑 우리가 뽑을 것:**
- **Li₃PO₄ 가 사실상 완벽하다** (양극 10/10 = 0, SSE 최악 −6). 이 잣대에서 **인산염이 챔피언**이다.
- **Zr·Hf 산화물은 양극엔 온건, 황화물 SE 엔 최악** (Li₂Zr₂O₅ −70~−105, Li₂Hf₂O₅ −55~−68, Li₂Hf₃O₇ −44~−53).
  ⇒ **우리 repo 의 `choi2026_bzox_dry_zro2x_nmc_shell_coating`(ZrO₂ₓ 건식 쉘 코팅) 축과 직접 연결된다** — §12-4.
- **Li₆Zr(PO₅)₂** (= Li₆ZrP₂O₁₀, MP 미수록): 양극 10/10 = 0 이면서 SSE −14~−19 로, Zr 을 인산염에 넣으면
  Zr 산화물의 황화물 독성이 **−70~−105 → −14~−19 로 사라진다.** ⇒ **"폴리음이온이 금속의 독성을 가린다"**
  의 정량 사례. 우리 §D(인산염 경로)와 **같은 방향의 물리**이되 **Li 를 안 쓰는 경로라는 요점은 없다**.

### 3d. `Fig. 4`·`Fig. S4` — ML 성능 (🔴 여기서 논문이 제일 약하다)

| 항목 | 값 | 출처 |
|---|---|---|
| 모델 비교 | ET · RF · HGBR · XGB · LGBM · CAT · ENet **7 종** | Methods |
| 분할 | 학습 80 % / 홀드아웃 20 %, **1 회 분할** · 5-fold CV · 탐색예산 **54 configs/모델** | Methods |
| 선택 목적함수 | `Penalized Score = MAE_CV + max(0, MAE_CV − MAE_train)` | 식 (4) |
| 최종 | **XGB 0.44 + HGBR 0.56** (OOF MAE 최소 그리드 탐색) | 본문 |
| **Total MAE** | XGB ≈ **31.1** · LGBM ≈ 31.8 · HGBR ≈ **31.9** · CAT ≈ 32.2 · ET ≈ 34.3 · RF ≈ 35.9 · ENet ≈ 44.5 | `Fig. S4` **figure-read ≈** |
| **Error Gap** | XGB ≈ **26.5** · LGBM ≈ 27.7 · HGBR ≈ **25.8** · CAT ≈ 26.7 · ET ≈ 18.4 · RF ≈ 16.0 · ENet ≈ **6.1** | `Fig. S4` **figure-read ≈** |
| 패리티 R² | **0.9805** | `Fig. 4a` — ⚠ **in-sample** (저자 명시: *"retrained on the full labeled dataset (consistency check)"*) |

🔴🔴 **이 세 줄을 나란히 놓으면 논문의 판매 문장이 무너진다:**
- 의사결정 문턱은 **−50 meV/atom** 인데
- 최량 모델의 **MAE ≈ 31 meV/atom** (문턱 크기의 **62 %**)
- 그리고 **일반화 격차 ≈ 26 meV/atom** ⇒ 학습 MAE 는 ≈ 5. **과적합이 크다.**
- **R² = 0.9805 는 일반화 지표가 아니다.** 저자도 *consistency check* 라고 쓴다. 인용하면 안 된다.

**`Fig. 4b` 치환 중요도 (OOF MAE 증가, meV/atom, figure-read ≈)**:

| 순위 | 서술자 | ΔMAE |
|---|---|---|
| **1** | **Max Group (Period.)** | **≈ 32** ← 압도적 |
| 2 | Mean Electronegativity | ≈ 11 |
| 3 | Mean SpaceGroupNumber | ≈ 7 |
| 4 | Mean GS Band Gap | ≈ 6.5 |
| 5 | Electronegativity MAD | ≈ 6.5 |
| 6 | GS Volume per Atom (max−min) | ≈ 4 |
| 7 | Mean Covalent Radius | ≈ 2.5 |
| 8 | Mean Ionic Character | ≈ 2 |
| 9 | p-Valence Electron MAD | ≈ 2 |
| 10 | d-Valence Electron Fraction | ≈ 2 |

🔴 **1위가 2위의 약 3 배다.** `Max Group` = 구성원소 중 최대 주기율표 족번호 =
**사실상 음이온 정체 지시자**(O·S = 16, N·P = 15, F·Cl = 17). ⇒ 이 "해석가능 ML" 은
실질적으로 **"산화물·플루오라이드는 온건, 질화물·안티몬화물은 아니다"** 라는 한 줄짜리 규칙이고,
그건 §5.2 군집 결과를 다시 말한 것이다. §10-3.

### 3e. `Table S1` — 군집 대표 조성 (SI, 텍스트로 읽음)

| 조성 | 군집 | ⟨E⟩_OC | ⟨E⟩_SSE | 주요 모티프 |
|---|---|---|---|---|
| Li₅BiO₅ | 1 | −46.9 | **−330.7** | O-rich Bi 산화물 |
| LiLa(WO₄)₂ | 1 | −48.4 | **−310.9** | O-rich 텅스텐산염 폴리음이온 |
| "LSiNO" | 2 | **−249.3** | −39.3 | Li–Si 옥시나이트라이드 (O–N) |
| LiAl(CN₂)₂ | 2 | **−262.3** | −20.2 | 시안아미드 (C–N) 골격 |
| LiInP₂O₇ | 3 | −53.2 | −114.1 | 인산염 (O–P) |
| **Li₂ZrO₃** | 3 | −21.5 | **−111.7** | Zr 산화물 |
| Li₂CaSiO₄ | 3 | −13.4 | −97.1 | 규산염 (O–Si) |
| LiBaSb | 4 | −390.4 | −303.4 | 안티몬화물 / Zintl |
| Li₃BN₂ | 4 | −355.6 | −311.4 | 질화물 (B–N) |

🔑 **Cluster 1 은 산화물 양극엔 −47 로 온건한데 황화물 SE 엔 −311~−331 로 최악**이다.
**"양극에 좋은 것이 전해질에 좋지 않다"** 가 여기서 숫자로 보인다 — §5.2, §7-E.
🔑 **Li₂ZrO₃ 이 Cluster 3 대표인데 ⟨E⟩_SSE = −111.7** ⇒ Zr 산화물 코팅의 황화물 독성은 학습셋에서도 이미 보인다.

### 3f. `Fig. S1` — 상위 20 후보 (SI 텍스트 층에서 회수, 이미지 미독)

Li₃AlF₆ · **LiTmSiO₄** · LiAl₂H₆BrO₆ · LiH₂BrO · Sr₂LiB₁₀H₃O₁₉ · Li₂Si₂O₅ · Li₂MgSiO₄ · LiAl₅O₈ ·
LiMgPO₄ · LiAlO₂ · LiBO₂ · LiYF₄ · Li₄Al₃Si₃ClO₁₂ · Li₃B₇O₁₂ · BaLi(B₃O₅)₃ · Li₃B₅(HO₅)₂ ·
Li₂Al(BO₂)₅ · LiAlSiO₄ · Li₂BeSiO₄ · **Li₃PO₄**

🔴 **`LiTmSiO₄` (Tm = 툴륨, 란타나이드)가 상위 20 안에 이미 있다.** §7-D 에서 다시 다룬다.
⚠ 수소 함유 상(LiAl₂H₆BrO₆, LiH₂BrO, Li₃B₅(HO₅)₂, Sr₂LiB₁₀H₃O₁₉)이 4 종 있는데 **전지 코팅으로는 비현실적**이다
— E_hull = 0 필터만 걸어서 수화물·수산화물이 그대로 통과했다. §10-5.

### 3g. `Table S2` — Li 이온전도도 (SI, 문헌 소환의 소환 ⛔ 이중 인용)

| 계열 | 대표 | 보고 대역 | 출처 |
|---|---|---|---|
| Li–P–O 인산염 | Li₃PO₄ | 10⁻⁶ ~ 10⁻⁸ S/cm | SI ref [1] |
| Li–Nb–O | LiNbO₃ (비정질) | 10⁻⁵ ~ 10⁻⁶ S/cm | SI ref [2] |
| Li–Si–O 규산염 | Li₂SiO₃, Li₄SiO₄ | 10⁻⁶ ~ 10⁻⁸ S/cm | SI ref [3] |
| Li–B–O 붕산염 | Li₃BO₃ | 2×10⁻⁶ S/cm | SI ref [4] |
| Li–M–O 산화물 | LiAlO₂ **5.6×10⁻⁸** · Li₄Ti₅O₁₂ **10⁻¹³** · Li₂ZrO₃ **10⁻¹²** | — | SI ref [5,6] |

⛔ **이 표는 이 논문이 계산한 것이 아니다.** 저자 자신이 *"should not be interpreted as quantitative
conductivity assignments to individual expanded compositions"* 라고 못박는다. **우리 원장에 넣지 않는다.**
🔑 다만 **Li₂ZrO₃ 10⁻¹² S/cm** 는 §3c 의 "Zr 산화물은 황화물 SE 에 −70~−105" 와 합쳐 **Zr 코팅 이중 감점**을 만든다.

---

## 4. 방법 — 우리가 같은 축을 재현할 때 필요한 조건 전부 ★

### 4a. 계산 환경

- **code**: 없음. **자체 DFT 0 회.**
- **총에너지 원천**: **Materials Project** (ref 47–49) — pymatgen `MPRester` 경유. **MP 스냅샷 날짜·버전 미기재** ⚠
- **functional / pseudo / k-points / ecut / supercell / DFT+U**: **전부 해당 없음** (MP 기본값 승계, 명시 없음)
- **AIMD / MLIP / NEB / COHP / DOS / ELF / Bader**: **전부 없음**
- **무질서 처리**: **없다.** 조성을 MP entry 로 받을 뿐 배열 무질서를 다루지 않는다.
  ⇒ 아지로다이트의 S²⁻/Cl⁻ 자리무질서가 이 논문에는 **존재하지 않는다**.

### 4b. 🔴 안정성 지표의 정확한 정의 (선행연구 판정의 핵심)

접촉쌍 A·B, 몰분율 x ∈ (0,1):

```
(1)  E_bin(x)      = x·E_A + (1−x)·E_B                         ← 기계적 혼합 에너지
(2)  ΔE_D(x)       = E_eq(C_bin(x)) − E_bin(x)                 ← 미보정 분해 구동력
                     E_eq = 그 조성에서 상도 위 최소에너지 상집합
(3)  E_reaction(x) = ΔE_D(x) − x·ΔE_D(A) − (1−x)·ΔE_D(B)       ← 자체분해 차감
```
**보고값 = `min_x E_reaction(x)`**, 원자당 정규화(meV/atom). 부호 규약: **더 음수 = 분해 구동력 더 큼.**

| 규약 항목 | Park | **우리 §B** | 같은가 |
|---|---|---|---|
| 기본 식 | Richards 2016 pseudo-binary | 동일 | ✅ **같다** |
| 도구 | pymatgen (`InterfaceReactions` 계열) | pymatgen | ✅ **같다** |
| hull 에너지 사용 | 사용 (E_eq = hull 최소) | `use_hull_energy=True` | ✅ **같다** |
| 자체분해 차감 | 식 (3) 으로 차감 | 차감 | ✅ **같다** |
| **개방계 / 전압** | **없음 (닫힌계)** | **`GrandPotentialInterfacialReactivity`, 2.5–4.5 V 6 점** | ❌ **다르다 — 결정적** |
| `include_no_mixing_energy` | 언급 없음 | `True` | ❓ 확인 불가 |
| x 축 보고 | **최솟값 1 개만** | **전 kink 저장 (곡선 전체)** | ❌ **다르다** |
| 양극 상태 | **만충 1 상태만** | 전압으로 μ_Li 를 훑음 | ❌ 다르다 (⚠ Xiao 2019 는 만충/반충 2 상태) |
| 후보 필터 | **E_hull = 0 만** | (조성 지정) | — |
| 문턱 | −50 meV/atom | (문턱 없음, 곡선 비교) | — |

> 🔴 **"같은 도구·같은 식·다른 열역학적 앙상블"** 이 한 줄이 이 판정의 전부다.
> Park 의 `E_reaction` 은 **닫힌계**에서 두 고체를 붙였을 때의 구동력이다.
> 우리 §B 는 **Li 저장소에 열린 계**에서 **전압의 함수로** 같은 것을 본다.
> 저자 자신이 경계를 그어 준다 — *"This contact-reaction metric is **distinct from** the intrinsic
> electrochemical stability window of an isolated electrolyte or coating phase."*

### 4c. ML — 어디에 들어가나 (대리모형 / 회귀 / 생성?)

**답: 대리모형(surrogate regression)이다. hull 계산을 *대체하지 않고*, *DB 밖 조성으로 확장*하는 데 쓴다.**

```
809 MP 상안정 Li 화합물
   └─ pymatgen hull 로 17 차원 E_reaction 벡터 계산  ← ML 아님, 정공법
        ├─[비지도]─ HDBSCAN(noise 제거) → k-medoids(k=4) → 군집 지문(원소 출현율·음이온쌍 공출현율)
        │              └─ Cluster 3(310 종, O–P 중심) = **설계영역**
        ├─[생성]──  그 영역 안에서 Li–M–O(144) / Li–M–A–O(377) 무작위 화학량론 + 전하중성 필터
        │              └─ ⚠ **생성모형 아님.** 규칙 기반 열거 + 무작위 표집
        └─[지도]──  matminer/MAGPIE 조성 서술자 → XGB+HGBR 앙상블
                       └─ 521 신조성의 **평균 E_reaction 예측 → 순위**
                            └─ 검증: MP 미수록분은 **전구체 hull proxy label** 로 대조 (`Fig. 6`)
```

- **ML 이 대체하는 것**: 없다. **가속하는 것**: DB 에 없어 hull 을 못 푸는 조성의 *사전 순위 매기기*.
- ⚠ **역설**: MP 미수록 조성에도 결국 **전구체 분해 hull 을 풀어 proxy label 을 만든다** (`Fig. 6` 의 x 축).
  즉 **열역학 계산을 실제로 다 돌린다.** 그러면 ML 은 무엇을 절약하나? 저자는 답하지 않는다. §10-4.

### 4d. 🔴 확장 조성공간의 정확한 정의 (Nd 판정의 근거)

- **대상 공간 2 개**: 삼원 **Li–M–O** · 사원 **Li–M–A–O**
- **A (폴리음이온 형성 원소)**: **B, P, Si** — 3 종
- **M pool (15 종, 원문 그대로)**: **Mg, Ca, Al, Zn, Ga, Zr, Hf, Sc, Y, La, Gd, Dy, Ho, Er, Lu**
  - 선정 논리: *"cations with limited oxidation-state variability and strong oxide-forming tendencies,
    thereby reducing redox-driven interfacial reaction pathways"*
  - 🔴 **란타나이드 6 종(La, Gd, Dy, Ho, Er, Lu)이 들어 있다.** **Nd 는 없다.**
    Ce·Pr·Nd·Sm·Eu·Tb·Tm·Yb 도 없다 — **La 와 Gd 이후 무거운 쪽만 골랐다.**
    (Nd 는 Ce–Pr–Nd 초기 란타나이드라 4f 원자가 변동 위험이 상대적으로 크다는 판단으로 보이나, **논문은 이유를 안 적는다**.)
- **화학량론**: 원소분율·총원자수에 사전 경계를 두고 **무작위 표집**. 경계값은 **미기재** ⚠ (재현 불가)
- **전하중성**: 명목 산화수로 강제, 실패 시 폐기
- **선택적 필터**: MP 수록 여부

### 4e. 비지도 학습

- HDBSCAN (ref 68) 으로 저밀도 outlier = noise 제거 → **이후 분할에서 제외**
- 남은 점에 Ward · spectral · GMM · Leiden · **k-medoids** 비교 (`Fig. S2`)
- 선택 기준: (i) **silhouette** (ii) **cluster-size RSD (σ/μ)**
- 채택: **k-medoids, k = 4**
- 군집 입력 = **반응성 프로파일 벡터(17 차)** — *"rather than by crystal-structure information"*
- PCA 는 **시각화 전용** (저자 명시)
- 지문 = 원소 출현율 + 음이온쌍 공출현율

### 4f. 지도 학습

- 서술자: **matminer** (ref 66) + **MAGPIE** preset (ref 67) — 조성 통계(평균·범위·분산)
  + 원소수 · 이상혼합엔트로피 · 음이온 원자분율 · 폴리음이온(B/P/Si) 분율 · 전이금속 지시자 · 전하균형 일관성
  - ⚠ **구조 서술자 0** (의도적 — 가상 조성은 구조를 모르므로)
- 타깃: **17 쌍 전체 평균 E_reaction** (스칼라 1 개)
- 하위선택용 보조: `⟨E_reaction⟩_OC`, `⟨E_reaction⟩_SSE` **각각 문턱 적용**
- 중요도: 5-fold OOF 치환 중요도, 치환 **10 회 반복**

### 4g. 적용가능영역(applicability domain) 분석 — `Fig. S5`

- 정의: 809 참조셋으로 z-표준화한 서술자 공간에서 **최근접 5 개까지의 평균 유클리드 거리**
- 문턱: 참조셋 **LOO** 거리 분포의 **p90 / p95 / p99**
- 결과: core(≤p90) **94.6 %** · boundary(≤p95) **97.9 %** · **극단 외삽 영역 0**
- 🔴 **p95 초과 꼬리에 "일부 란타나이드 함유 조성" 이 들어 있다** (SI Note 명시)
- **figure-read ≈ (Fig. S5a)**: 문턱선 p90 ≈ **7.8** · p95 ≈ **9.6** · p99 ≈ **13.8** (scaled Euclidean).
  분포 중앙값 — 참조 ≈ **4.9** · **LMO ≈ 5.4** · LMAO ≈ **4.0**.
  ⇒ 🔴 **Li–M–O(144 종) 가 참조셋보다 오히려 더 멀다** (중앙값이 위로 이동). §10-7.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 §2.1 코팅 없는 계면은 열역학적으로 불가 (`Fig. 1`)

`Fig. 1a` 를 보면 **두 개의 뚜렷한 영역**으로 갈린다.
- **올리빈 인산염**(LiFePO₄, LiFe₀.₅Mn₀.₅PO₄): **−80 ~ −152 meV/atom** (본문은 *"−80 to −150"*).
  저자 해석: *"comparatively stable polyanion frameworks"* — **P 가 이미 O 와 결합해 있어 S↔O 교환의 구동력이 작다**.
- **스피넬 + 층상 R̄3m 산화물**: **−263 ~ −548 meV/atom** (본문은 *"−260 to −550"*).

본문의 판정: **양극 화학이 지배 변수**이고, 전해질 축(티오포스페이트 vs LGPS vs 아지로다이트)의 차이는
**양극이 만드는 대비보다 작다.** ✅ `Fig. 1a` 실독과 일치한다 — 열 방향 스팬(−100 → −548, 448)이
행 방향 스팬(−263 → −383 at LiMn₂O₄, 120)보다 훨씬 크다.

⚠ **그러나 "작다" 가 "무시할 만하다" 는 아니다**: NMC811 열에서 Li₆PS₅Cl(−377) vs Li₇P₃S₁₁(−523) 은
**146 meV/atom** 차이고, 이건 코팅이 만드는 개선폭(−332 → −8/−17)과 같은 자릿수다.
**전해질 선택만으로도 얻을 것이 있다** — 저자는 이 함의를 안 쫓는다.

`Fig. 1b` (**실독**): x = Mean E_reaction(Cathode), y = Mean E_reaction(Electrolyte), 둘 다 −600 ~ +100 meV/atom.
**빨간 점선이 양축 −50 에 그어져 있다.** 809 점의 분포가 **L 자**다 —
(i) x ≈ 0~−100 에 붙어 y 가 −600 까지 떨어지는 **수직 띠**,
(ii) y ≈ 0 에 붙어 x 가 −600 까지 떨어지는 **수평 띠**,
(iii) 둘 다 ≥ −50 인 **우상단 모서리는 성기다** → 여기가 **53 종 (6.6 %)**.

🔑 **이 L 자가 이 논문에서 가장 물리적으로 값어치 있는 그림이다** (저자는 그냥 *"highly skewed"* 라고만 쓴다).
L 자는 **한쪽에 좋은 것이 다른 쪽에 나쁘다**는 **길항**의 기하학적 표현이고,
우리 **§E dual compatibility** 가 말하는 바로 그것이다. §7-E.

### 5.2 §2.2 군집과 조성 지문 (`Fig. 2`, `Fig. 3`, `Fig. S2`, `Fig. S3`)

**`Fig. 2a` (실독)**: PC1 −10~5, PC2 −10~5. 회색 = HDBSCAN noise. 4 색 군집.
Cluster 4(보라)는 왼쪽에 분리돼 있고, Cluster 2(하늘)는 위쪽, **Cluster 1(분홍)과 Cluster 3(주황)은 오른쪽에서
맞닿아 있으며 경계가 곧은 직선이다.**
⚠ **직선 경계 = k-medoids 가 강제한 Voronoi 분할의 흔적**이지 밀도 간극이 아니다. §10-2.

**`Fig. 2b` (실독)** — 이 논문의 두 번째로 중요한 그림. y = −500 ~ 0 meV/atom, x = 양극 10 + SSE 7 (세로선으로 분리).
**figure-read ≈**:

| 군집 | 양극 쪽 거동 | SSE 쪽 거동 | 성격 |
|---|---|---|---|
| **Cluster 3** (주황▲) | ≈ **−20 → −70** (가장 평탄·온건) | ≈ **−95 ~ −100** (완만한 하락) | **타협점 = 설계영역** |
| **Cluster 1** (빨강●) | ≈ −50 → −25 → −75 (온건) | ≈ **−350 으로 급락** | 산화물엔 착하고 **황화물엔 적대적** |
| **Cluster 2** (하늘■) | ≈ −85 → **−355 로 급락** | ≈ **−40 으로 급상승** | **거울상** — 황화물엔 착하고 산화물엔 적대적 |
| **Cluster 4** (보라◆) | ≈ −245 → −470 | ≈ −300 ~ −370 | 전 구간 최악 |

🔑🔑 **Cluster 1 과 Cluster 2 가 정확히 서로의 거울상이다.** 이것이 `Fig. 1b` L 자의 군집 수준 재현이고,
**"양극 친화 ↔ 전해질 친화" 가 구조적으로 길항한다**는 809 종 통계 근거다.
Cluster 3 이 "설계영역" 인 이유는 **어느 쪽에서도 최고가 아니지만 양쪽에서 나쁘지 않아서**다.

**군집 지문 (`Fig. S3`, SI 텍스트에서 수치 회수 — 이미지 미독)**

원소 출현율 (좌 패널):

| 군집 | 특징 원소 | 값 |
|---|---|---|
| Cluster 1 | **O 0.96** · Sb 0.08 · Te 0.10 · Mn 0.09 · Fe 0.09 · W 0.08 | 극단적 O-rich |
| Cluster 2 | **S 0.46** · N 0.19 · Se 0.19 · P 0.18 · H 0.16 | 혼합 음이온 |
| **Cluster 3** | **O 0.80** · **P 0.30** · F 0.18 · B 0.14 · Si 0.11 · H 0.10 | **O + 폴리음이온** |
| Cluster 4 | **N 0.76** · Sr 0.17 · H 0.13 · Si 0.11 | 질화물 |

음이온쌍 공출현율 (우 패널):

| 군집 | 주요 쌍 |
|---|---|
| Cluster 1 | **O–Sb 0.08** · O–Se 0.06 · O–S 0.04 |
| Cluster 2 | **O–P 0.07** · P–S 0.04 · P–Se 0.04 · B–S 0.04 · S–Sb 0.03 |
| **Cluster 3** | **O–P 0.30** · **B–O 0.13** · **O–Si 0.10** · O–F 0.05 |
| Cluster 4 | **N–Si 0.11** · N–O 0.05 · B–N 0.04 |

**`Fig. 3` (실독)** — Cluster 3 만의 음이온 조합 UpSet plot.
좌측 막대 = 개별 음이온 보유 화합물 수 (Counts 0–200), 상단 막대 = 상위 10 개 **조합**의 교집합 수 (0–80).
읽은 것: **O 단독**이 가장 크고, 그 다음이 **O+P**, **B+O**, **O+Si**, 그리고 F·N·S 를 낀 조합이 꼬리에 있다.
⇒ *"beyond O-only compositions, the most frequent anion intersections include **A–O** combinations where **A = B, P, or Si**"*
⇒ 이것이 **Li–M–A–O (A = B, P, Si)** 확장 공간의 근거다. **지문 → 생성규칙**의 연결은 이 그림 하나로 이뤄진다.

**`Fig. S2` (실독)** — ⚠ **여기서 본문 주장과 어긋난다.**
x = 군집수 k (2~10), y = Cluster Imbalance RSD (0.84~1.04), 색 = silhouette (0.4~0.9).
**점이 방법당 딱 하나씩, 총 5 개뿐이다** (k-sweep 이 아니다):

| 방법 | k | RSD (figure-read ≈) | silhouette (색, figure-read ≈) |
|---|---|---|---|
| Ward | 2 | **1.013** | ≈ 0.55–0.60 (청록) |
| Spectral | 2 | **0.990** | ≈ 0.55–0.60 (청록) |
| **k-medoids** ★ | **4** | **0.987** | ≈ **0.85+ (노랑, 최고)** |
| GMM | 9 | **1.024** | ≈ 0.42–0.45 (남색, 최저) |
| Leiden | 10 | **0.859 (최저=최선)** | ≈ 0.65 (초록) |

🔴 **본문은 k-medoids 가 *"strong separation without severe size imbalance"* 라고 쓰지만,
그림에서 k-medoids 의 RSD ≈ 0.987 은 Ward(1.013)·Spectral(0.990)과 사실상 같고 **Leiden(0.859)보다 나쁘다.**
RSD ≈ 1 은 **군집 크기의 표준편차가 평균과 같다**는 뜻으로, 그 자체가 **심한 불균형**이다
(실제로 Cluster 3 혼자 310 종). ⇒ **RSD 기준은 아무것도 가르지 못했고, 선택은 silhouette 단독으로 이뤄졌다.** §10-2.

### 5.3 §2.3 대리모형 (`Fig. 4`, `Fig. S4`)

수치는 §3d. 서사는:
- XGB = **정확도 리더**, HGBR = **안정성 리더**(중앙값 이하 MAE 중 gap 최소) → 0.44/0.56 가중 앙상블
- 저자의 물리적 근거: XGB 는 *"high-order, nonlinear interactions and threshold-like dependencies"* 를 잘 잡고,
  HGBR 은 *"feature binning and constrained split search act as an implicit regularizer"*
- ⚠ 그런데 `Fig. S4` 실독에서 **XGB gap 26.5 vs HGBR gap 25.8 = 0.7 차이**다.
  이 정도로 *"the most stable choice"* 를 선언하는 것은 과하다. §10-3.

### 5.4 §2.4 후보 생성과 확장 (`Fig. 5`, `Fig. 6`, `Fig. S5`)

**`Fig. 5` (실독)** — 순수 도식. 6 단 흐름:
`Coating-Candidate Set Construction` → {`Oxygen only (Li-M-O)`, `Oxygen polyanion (Li-M-A-O)`} →
`M selection: Redox-inactive, Fixed-valence metal` → `Stoichiometry sampling` → `Charge-neutrality check` →
`Optional filtering (e.g., Materials Project coverage)` → `Output candidate set`.
🔑 **`M selection` 이 "Redox-inactive, Fixed-valence" 로 못박혀 있다** — 이 한 칸이 우리와의 차별을 만든다. §7-D.

**`Fig. 6` (실독)** — 확장셋 예측 대 proxy label 패리티.
(a) **Li–M–O**: 양축 −150 ~ 0 meV/atom. 점 ≈ 144. 주황(MP 수록) ≈ 10 개, 나머지 파랑(MP 미수록).
산포가 **넓다** — true ≈ −100 에서 predicted 가 **−70 ~ −130** 에 퍼진다 (**figure-read ≈ ±30**).
(b) **Li–M–A–O**: 양축 ≈ −120 ~ 0. 점 ≈ 377. (a)보다 조밀하지만 여전히 **figure-read ≈ ±25–30**.
🔴 (b)에서 **true ≈ −60 ~ −90 구간의 점 다발이 패리티선 *위*(predicted ≈ −40 ~ −55)에 몰려 있다**
= **낙관 편향**. 스크리닝 필터에서 이 방향은 **위양성**을 만든다 — 실제보다 안정하다고 말한다. §10-4.

⚠ **`Fig. 6` 의 "True" 축은 진짜가 아니다.** MP 미수록 조성에는 목표상 에너지가 없으므로
**전구체 hull 분해 assemblage** 의 반응에너지를 proxy 로 쓴다. 저자도 명시:
*"These proxy labels should be interpreted as composition level thermodynamic consistency checks
rather than exact reaction energies of synthesized target phases."*
⇒ **`Fig. 6` 은 "ML vs 현실" 이 아니라 "ML vs 또 하나의 조성기반 열역학 추정" 이다.**

**`Fig. S5` (실독)** — §4g. 핵심 관찰은 **Li–M–O 가 참조셋보다 더 멀다**는 것 (§10-7).

### 5.5 §2.4 말미 — 코팅 효과 총정리 (`Fig. 7`)

수치는 §3c. 서사: **−332 → 코팅–양극 −8 / 코팅–SSE −17.**
저자 표현: *"transforming highly reactive cathode–SSE pairings into substantially less reactive coating-mediated contacts."*

⚠ **이 비교는 사과 대 오렌지에 가깝다**: 분모(−332)는 **70 쌍 전수 평균**이고,
분자(−8/−17)는 **저자가 골라 보여준 20 종 코팅**의 평균이다. 20 종은 `⟨E⟩_OC`·`⟨E⟩_SSE`
**양쪽 문턱을 통과하도록 선별된 것**이다 — 즉 **선택 후 평균**이다. §10-1.

### 5.6 🔴 저자들이 **스스로 못 한다고 적은 것** (positioning 에 직접 쓴다)

원문 두 문단을 그대로 옮긴다. **이 목록이 우리가 메우는 칸의 지도다.**

> *"it does not by itself capture several factors that can critically influence practical coating behavior,
> including **reaction kinetics**, **interfacial microstructure**, **coating thickness and conformity**,
> **adhesion**, **space-charge-layer formation**, **strain and volume-change effects**, and
> **Li-ion transport across the coating layer**."*

> *"Future work will need to bridge the gap … by factoring in **finite-temperature stability**, **metastability**,
> reaction kinetics, space-charge effects, strain/volume changes, interfacial transport, and ion-transport properties."*

> *"**Although Li-ion conductivity was not explicitly evaluated in the present framework** …"*

> 🔴🔴 그리고 결정적으로:
> *"**Additional computational checks, such as electrochemical stability-window and Li-ion migration analyses,
> could further support candidate down-selection before experimental testing.**"*

⇒ **저자들이 ESW(우리 축 B①)와 Li 이동(우리 축 A)을 "앞으로 해야 할 일" 로 명시했다.**
우리는 그 둘을 이미 갖고 있다. **이 문장은 우리 원고 introduction 의 gap 문장으로 직접 쓸 수 있다.**

또한 저자 자인:
- *"these values serve as **comparative indices of stability** rather than precise forecasts of reaction products,
  interfacial morphologies, or transport behavior"* — **산물 정체 예측을 스스로 부인한다** (우리 §D 의 영역)
- *"ML predictions … are interpreted as **ranking and prioritization scores** … rather than as precise
  quantitative estimates of absolute reaction energies"*
- *"The ML framework should be viewed as a **thermodynamically grounded first-pass filter**"*
- *"top-ranked compositions … should be regarded as **thermodynamically prioritized targets** …
  **rather than final synthesis-ready coating materials**"*
- *"A dedicated **causal attribution** of individual descriptors remains **beyond the scope**"*
- **실험 검증 0** — 합성·XRD·XPS·EIS·셀 시험 **전무**

---

## 6. Post-processing ★

- **무엇**: pymatgen **phase diagram / convex hull** → pseudo-binary `E_reaction(x)` → **min over x**
  · `E_hull` 필터 · **전구체 분해 hull proxy label** (MP 미수록 조성)
- **도구**: **pymatgen** (ref 47–49) · **matminer** (ref 66) + MAGPIE (ref 67) ·
  **scikit-learn**(HGBR, ENet, ET, RF, spectral, GMM, PCA, permutation importance) ·
  **XGBoost**(ref 42) · **LightGBM**(ref 76) · **CatBoost**(ref 77,78) · **HDBSCAN**(ref 68) ·
  **Leiden**(ref 73) · **PAM/k-medoids**(ref 40,41)
- **수치화·플롯·기록**: 히트맵(`Fig. 1a`, `Fig. 7`, `Fig. S1`, `Fig. S3`) — **셀에 값을 활자로 인쇄**(좋은 관행,
  우리가 배울 점) · 산점(`Fig. 1b`, `Fig. 4a`, `Fig. 6`) · 오차막대 선(`Fig. 2b`, 95 % CI) ·
  UpSet plot(`Fig. 3`) · 박스+스트립(`Fig. S5a`)
- ⛔ **결과 데이터는 기계판독 형태로 공개되지 않았다.** Data Availability = *"available in the supplementary
  material"* 인데 SI 에 표 2 개뿐이다. **809 종·521 종 목록과 그 값이 없다** ⇒ **재현 불가.** §10-8.

---

## 7. 🔴🔴 우리 연구와의 대조 — 선점 판정 ★★

> 우리 축 정의는 `../our_dft_baseline.md` 와 `comparison_vs_ours.md` §B 4축을 따른다.
> **문헌 수치는 소환값이므로 우리 절대값과 같은 표에 놓지 않는다** — 축과 규약만 맞춘다.

### 7a. 항목별 판정표

| 우리 주장 | 이 논문에 있나 | 근거 (원문) | 판정 |
|---|---|---|---|
| **§B 전압 축 계면 반응성** — `GrandPotentialInterfacialReactivity`, 2.5–4.5 V **6 점**, 전 kink 저장 | **❌ 없다** | `grand`·`applied potential`·`μ_Li`·`state of charge`·`voltage-dependent` **0 회**. 식 (1)–(3) 은 닫힌계. 저자 자인: *"distinct from the intrinsic electrochemical stability window"* | 🟢 **선점 아님** |
| **§B 닫힌계 하위층** — `InterfacialReactivity(use_hull_energy=True)` 최솟값 | **⚠ 있다 — 정확히 같은 양** | 식 (1)–(3) = Richards 2016 재기술, 같은 도구 | 🟠 **같은 층. 단 이건 [Richards16]·[Xiao19] 가 이미 원전이라 Park 의 선점이 아니다** |
| **§B 6 조성 × 4 양극 × 6 전압 전 kink** | **❌ 없다** | `kink` 0 회. 보고는 **min 1 개**. 양극 만충 1 상태 | 🟢 **선점 아님** |
| **§D 기전 — Nd 는 *Li 를 안 쓰는* 인산염 경로를 연다 (NdPO₄ Li/P=0)** | **❌ 없다** | `Li/P`·`Li content`·`Li fraction` **0 회**. 서술자 상위 10 에 Li 항 없음. **Nd 가 M-pool 에 없다** | 🟢 **선점 아님** |
| **§D — Li/P ≈ 1.67 부호 반전** | **❌ 없다** | 닫힌 식·부호반전·문턱 개념 전무 | 🟢 **선점 아님** |
| **§2b 보호율 `min(1, k·x/(1−x))`, 맞춘 매개변수 0** | **❌ 없다** | `coverage`·`passivat*`·`scaling law`·`closed-form`·`analytic` **0 회**. 산출은 순위 목록 | 🟢 **선점 아님** |
| **§C Nd 효과와 O 효과의 가법성 (잔차 +0.0005)** | **❌ 없다** | 도펀트 조합·교호작용 분석 없음 | 🟢 **선점 아님** |
| **§E dual compatibility — CEI 산물이 전해질 쪽과도 지내야 한다** | **🟠 개념은 있다, 충돌 서사는 없다** | `⟨E⟩_OC` / `⟨E⟩_SSE` 양쪽 문턱 + `Fig. 1b` L 자 + `Fig. 2b` Cluster 1↔2 거울상 | 🟠 **아래 7b** |
| **in-situ 도펀트 보호상** | **❌ 없다 — 개념 부재** | `in situ`/`ex situ` **0 회**. 처방 전부 증착 | 🟢 **선점 아님, 그리고 이게 우리 축이다** |
| **란타나이드 + 인산염이 계면 안정상** | **🟠 조성 수준으로는 있다** | M-pool 에 La·Gd·Dy·Ho·Er·Lu · 학습셋 상위 20 에 **LiTmSiO₄** | 🟠 **아래 7d — 정직하게 인정해야 한다** |
| **황화물 SE 도핑** | **❌ 없다** | SE 7 종은 고정된 비교군일 뿐. 도핑 0 회 | 🟢 **선점 아님** |

### 7b. §E dual compatibility — 가장 가까운 대목, 정확히 갈라 쓴다

**그들이 한 것**: `⟨E_reaction⟩_OC` 와 `⟨E_reaction⟩_SSE` 를 **따로 평균 내고 양쪽 모두에 문턱**을 걸었다.
*"prioritized candidates that remain low-reactivity against both sets **to avoid compositions that are
favorable only on one side**."* 그리고 `Fig. 2b` 가 Cluster 1(산화물 친화·황화물 적대) ↔
Cluster 2(그 거울상)로 **길항을 809 종 통계로 보여준다.**

**그들이 안 한 것** — 세 가지, 전부 우리 자리다:
1. **길항을 전압의 함수로 보지 않았다.** 그들의 길항은 조성 공간의 정적 구조다.
   우리 §E 는 **V_ox 를 올리면 전해질 적합성이 떨어지는** 동적 충돌이다. **전압 축이 없으면 이 충돌은 볼 수 없다.**
2. **CEI 산물을 다루지 않았다.** 그들은 **코팅 물질 자체**의 양쪽 상성을 본다.
   우리 §E 는 **반응해서 생긴 산물**이 전해질 쪽과도 지내야 한다는 2차 조건이다.
   저자 자인이 이 칸을 비워 준다 — *"rather than precise forecasts of **reaction products**"*.
3. **길항의 이유를 묻지 않았다.** *"trade-off"* 라고 관찰만 하고 기전을 안 쫓는다.

⇒ **원고 문장**: *"Interfacial screening has recognized that a coating must be compatible with both contacting
phases [Park 2026]. What has not been addressed is that this dual requirement **tightens with applied potential**,
and that it applies not only to the coating phase itself but to the **products it forms**."*

### 7c. 🔴 §B 축 B③ — 우리 값과 같은 잣대에 놓을 수 있는 유일한 지점

우리 `comparison_vs_ours.md` §B③ 은 이미 `comp1|LiCoO₂ = −0.3227 eV/atom` (= **−322.7 meV/atom**) 을
`InterfacialReactivity(use_hull_energy=True)`, MP2026 으로 갖고 있고 [Xiao19] Table S2 의 **−339** 와
16 meV/atom 차로 맞춰 뒀다. Park 은 **LiCoO₂ 를 안 쓴다**(양극 10 종에 LCO 없음).
그래도 겹치는 3 쌍이 있고, **같은 잣대인데 값이 크게 갈린다**:

| 쌍 (Li₆PS₅Cl 기준) | [Xiao19] Table S2 (만충) | **[Park26] `Fig. 1a`** | 차이 |
|---|---|---|---|
| \| NCM(111) | **−330** | **−289** | 41 |
| \| LiMn₂O₄ | **−421** | **−263** | 🔴 **158** |
| \| LiFePO₄ | **−101** | **−142** | 41 |
| \| LiCoO₂ | −339 | *(없음)* | — |
| *(참고) 우리 comp1\|LiCoO₂* | — | — | **−322.7** |

🔴🔴 **LiMn₂O₄ 에서 158 meV/atom 이 갈린다.** 같은 식·같은 도구인데 **코팅 효과 개선폭(−332→−8)의 절반**이다.
원인 후보: MP hull 세대 차 · LiMn₂O₄ entry(다형·자성 상태) 선택 차 · 음이온 보정 세대 차.
**둘 중 누가 맞는지는 이 자료로 판정할 수 없다.**

⇒ **이것이 우리에게 주는 가장 실용적인 교훈**:
**이 잣대의 절대값은 연구 간 이식이 불가능하다.** 우리 §B③ 이 [Xiao19] 와 16 meV/atom 맞은 것은
**운이 좋았던 것이지 일반적 재현성이 아니다.** ⇒ 우리 원고에서 **문헌 반응에너지와 우리 값을 나란히 쓸 때는
반드시 "같은 hull 스냅샷에서 재계산" 을 하거나, **비교를 순위·부호로만** 한다.
(⚠ 이건 우리 데이터 규율 *"문헌 수치는 소환값 — 방법 명시 없이 이식 금지"* 의 정량적 근거가 된다. §11.)

### 7d. 🟠 정직하게 인정할 것 — 란타나이드 + 폴리음이온

**우리가 "새롭다" 고 말하면 안 되는 것**이 하나 있다:

- Park 의 **M-pool 에 란타나이드 6 종(La, Gd, Dy, Ho, Er, Lu)** 이 들어 있고,
  근거는 *"limited oxidation-state variability and strong oxide-forming tendencies"* — **우리가 Nd 를 고른 논리와 같다.**
- 학습셋 **상위 20 후보에 `LiTmSiO₄`(란타나이드 규산염)** 가 이미 있다 (`Fig. S1`).
- `Table S1` 의 Cluster 1 대표에 **`LiLa(WO₄)₂`** 가 있다.

⇒ **"란타나이드 + O + 폴리음이온이 계면 저반응성 영역에 속한다" 는 조성 수준의 관찰은 이미 발표돼 있다.**
우리 원고에서 그것을 발견으로 쓰면 **Xiao 2019 형 사고**가 난다.

**그러나 다음 4 가지는 여전히 우리 것이다** — 그리고 이건 원문 근거로 확인했다:
1. **Nd 가 그들 pool 에 없다** (La·Gd·Dy·Ho·Er·Lu 만). Nd 특유의 결과는 미보고.
2. **란타나이드 조성이 하필 그들 대리모형의 신뢰도 최저 구간이다** — SI Note:
   p95 초과 꼬리가 *"includes some lanthanide-containing compositions"*. 그리고
   **`Fig. 7` 의 전시 후보 10 종에 란타나이드가 하나도 없다** (전부 Al·Zr·Hf·Mg·Ca·Be·B·Si 계).
   ⇒ **그들 파이프라인은 란타나이드를 열거는 했지만 결론으로 내지 못했다.**
3. **코팅(ex-situ) 이지 도펀트(in-situ) 가 아니다.**
4. **기전이 없다.** Li/P 축·Li 소비 여부·보호율 — 전부 없다.

### 7e. 우리 규율 점검 (자기검열)

- **band gap**: 이 논문에 밴드갭 계산 없음. `Mean GS Band Gap` 은 **구성원소 단체의 GS 밴드갭 통계**(MAGPIE)이지
  화합물 갭이 아니다. **우리 축 D 와 무관** — 혼동 금지.
- **ESW onset S-limited (축 ①)**: 이 논문에 ESW 없음. 비교 불가.
- **"Cl-rich 산화안정" 은 축을 명명해야 한다**: 🔴 **이 논문이 그 규율의 실증 사례를 준다** —
  축 B③(닫힌계 양극 접촉)에서 **Cl-rich 는 13 meV/atom 불리**하다 (§3b-(3)).
  축을 안 대고 말하면 이 표에 정면으로 반박당한다.

---

## 8. 🔴 판정 요약 — 세 문장

1. **우리 §B 의 전압 축(grand-potential, 2.5–4.5 V, 전 kink)은 선점되지 않았다.**
   이 논문은 **닫힌계 최솟값 1 개**만 본다. 개방계·전압 개념이 본문·SI 전체에 **0 회**다.
2. **우리 §D 기전과 §2b 보호율 닫힌 식은 선점되지 않았다.**
   Li 함량 축·산물 정체 기전·정량 보호 모델이 전부 없고, 저자들이 산물 예측을 **스스로 부인**한다.
3. **단, "hull 반응에너지로 계면 상성을 대량 스캔한다" 는 방법 층위는 확실히 겹치고,
   "란타나이드+폴리음이온이 저반응성" 은 조성 수준으로 이미 발표돼 있다.**
   ⇒ 우리 novelty 는 **방법이 아니라 ① 전압 축 ② in-situ 도펀트 ③ 정량 보호율** 세 다리에 서야 한다.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 7 SSE × 10 양극 코팅 없는 E_reaction 히트맵 (셀에 값 인쇄) | 🔴 **아지로다이트가 황화물 중 최선(−336.5), Li₇P₃S₁₁ 최악(−474.8)** · **Li₆PS₅Cl = Li₆PS₅Br 이 10/10 비트동일 → 이 잣대는 할로겐을 못 가른다** · **Cl-rich 는 산화물 양극에 13 meV/atom 불리** (축 B③) |
| 1b | 809 후보의 ⟨E⟩_cathode vs ⟨E⟩_electrolyte 산점, −50 문턱 2 선 | 🔴 **L 자 = dual compatibility 길항의 809 종 기하학.** 우리 §E 의 외부 통계 근거. 우상단 53/809 = 6.6 % |
| 2a | 반응성 프로파일의 PCA 2D 투영, HDBSCAN noise + k-medoids 4 군집 | Cluster 1·3 경계가 **직선** = 강제 분할 흔적. PCA 는 시각화 전용이라는 저자 명시 |
| 2b | 군집별 양극 10 + SSE 7 평균 E_reaction (95 % CI) | 🔴 **Cluster 1 ↔ Cluster 2 가 서로의 거울상** — 양극 친화와 전해질 친화가 구조적으로 길항. Cluster 3 = 타협점 |
| 3 | Cluster 3 음이온 조합 UpSet plot | **O 단독 > O+P > B+O > O+Si** ⇒ Li–M–A–O (A = B,P,Si) 생성규칙의 유일한 근거 |
| 4a | XGB+HGBR 앙상블 패리티, R² = 0.9805 | ⛔ **in-sample. 일반화 지표 아님 — 인용 금지.** 저자도 *consistency check* 라 명시 |
| 4b | OOF 치환 중요도 상위 10 | 🔴 **`Max Group` 이 2 위의 3 배(≈32 vs ≈11)** = 사실상 음이온 정체 1 변수 모형. "해석가능" 주장의 실체 |
| 5 | 후보 생성 워크플로 도식 | **`M selection: Redox-inactive, Fixed-valence metal`** 칸이 우리와의 분기점 — 이 규칙이 Nd 같은 가변원자가 도펀트를 원천 배제한다 |
| 6a,b | 확장셋 (a) Li–M–O 144 · (b) Li–M–A–O 377 예측 vs proxy label | 산포 **figure-read ≈ ±25–30 meV/atom**. (b) 중간 구간에 **낙관 편향** = 위양성 방향. "True" 축도 proxy임에 주의 |
| 7 | 코팅 20 종 × (양극 10 + SSE 7) 히트맵 + 코팅 없는 참조 4 행 | 🔴 **헤드라인**: −332 → 코팅–양극 −8 / 코팅–SSE −17. **Li₃PO₄ 가 챔피언(양극 10/10 = 0)** · **Zr·Hf 산화물은 황화물 SE 에 −44~−105 (우리 ZrO₂ₓ 코팅 축과 직결)** · **Li₆Zr(PO₅)₂ 가 그 독성을 −14~−19 로 지운다** |
| S1 | 상위 20 후보 × 17 쌍 히트맵 | **LiTmSiO₄(란타나이드 규산염)가 상위 20 에 이미 있다** — §7d. 수소 함유 상 4 종도 통과(§10-5) |
| S2 | 군집 방법 벤치마크 (k vs RSD, 색 = silhouette) | 🔴 **방법당 점 1 개뿐(k-sweep 아님)** · **RSD ≈ 0.99 는 심한 불균형인데 "without severe imbalance" 라고 씀** · Leiden 이 RSD 로는 더 낫다 |
| S3 | 군집 지문 (원소 출현율 / 음이온쌍 공출현율) | Cluster 3 = **O 0.80 · P 0.30 · O–P 공출현 0.30 · B–O 0.13 · O–Si 0.10** — 설계영역의 정의 그 자체 |
| S4 | 모델 선택 지도 (Total MAE vs Error Gap) | 🔴 **최량 MAE ≈ 31 meV/atom 인데 판정 문턱이 −50** · **gap ≈ 26 = 큰 과적합** · XGB vs HGBR gap 차 0.7 로 "가장 안정" 선언 |
| S5 | 적용가능영역 (k-NN 거리 분포 + 정렬 스펙트럼) | 🔴 **Li–M–O 중앙값(≈5.4)이 참조셋(≈4.9)보다 높다** = 더 외삽적인데 본문은 뭉뚱그림 · p95 초과 꼬리에 **란타나이드** |
| Table S1 | 군집별 대표 조성 + ⟨E⟩_OC/⟨E⟩_SSE | **Cluster 1 은 양극 −47 / SSE −311~−331** = 길항의 개별 사례 · **Li₂ZrO₃ ⟨E⟩_SSE = −111.7** |
| Table S2 | 계열별 문헌 Li 전도도 | ⛔ **이중 인용. 우리 원장 금지.** Li₂ZrO₃ 10⁻¹² S/cm 는 Zr 코팅 이중 감점 근거로만 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

**10-1. 헤드라인 비교(−332 → −8/−17)가 선택 후 평균이다.**
분모는 70 쌍 **전수** 평균, 분자는 **양쪽 문턱을 통과하도록 고른 20 종**의 평균이다.
공정한 비교는 "809 종 전체의 코팅 후 평균" 이어야 하는데 그건 `Fig. 1b` 에서 보듯 훨씬 나쁘다
(**53/809 = 6.6 % 만 문턱 통과**). 개선폭 자체는 실재하지만 **40 배(−332/−8)라는 인상은 부풀려져 있다.**

**10-2. 군집 선택 근거가 그림과 어긋난다 (`Fig. S2` 실독).**
본문은 k-medoids 가 *"strong separation **without severe size imbalance**"* 라고 쓰는데,
그림에서 k-medoids RSD ≈ **0.987** 은 Ward(1.013)·Spectral(0.990)과 사실상 동일하고 **Leiden(0.859)보다 나쁘다**.
RSD ≈ 1 자체가 심한 불균형이다(Cluster 3 혼자 310 종). ⇒ **RSD 기준은 실제로는 아무것도 가르지 못했고,
선택은 silhouette 단독이다.** 게다가 **방법당 k 가 하나씩만 찍혀 있어** k-medoids 의 k=4 가
다른 방법의 다른 k 와 공정 비교됐는지 알 수 없다. 추가로 **HDBSCAN 이 저밀도 점을 먼저 지운 뒤 silhouette 을
재므로 silhouette 이 구조적으로 부풀려진다.**

**10-3. "해석가능 ML" 이 사실상 1 변수 모형이다 (`Fig. 4b` 실독).**
`Max Group (Period.)` 하나가 ΔMAE ≈ 32 로 2 위(≈11)의 **3 배**다. 이 서술자는
**최대 족번호 = 음이온 정체 지시자**(O·S 16, N·P 15, F·Cl 17)에 불과하다.
⇒ 학습된 규칙은 **"산화물·플루오라이드는 온건, 질화물·안티몬화물은 아니다"** 한 줄이고,
그건 §2.2 군집이 이미 말한 것이다. **모형이 군집을 재학습했을 뿐 새 정보를 주지 않는다.**
3 위 `Mean SpaceGroupNumber` 는 **구성원소 단체의 공간군 번호 평균** — 물리량이 아니라 **임의의 정수 라벨**이다.
그게 상위에 오른다는 것은 모형이 **원소 정체의 프록시를 외우고 있다**는 신호다.
또한 XGB(gap 26.5) vs HGBR(gap 25.8) 의 **0.7 차이**로 *"the most stable choice"* 를 선언한 것은 과하다.

**10-4. 정확도가 판정 문턱을 감당하지 못한다 (`Fig. S4` 실독).**
판정 문턱 **−50 meV/atom**, 최량 모형 **MAE ≈ 31 meV/atom** (문턱의 62 %), **일반화 격차 ≈ 26**.
⇒ 문턱 근처 후보의 통과/탈락은 **사실상 동전 던지기**다.
`Fig. 6b` 에서 중간 구간이 **패리티선 위(낙관 편향)** 로 몰리는 것은 **위양성** 방향이라 더 나쁘다.
그리고 홀드아웃이 **단일 분할 1 회**라 20 % 테스트 성능에 오차막대가 없다.
⚠ **정의 불일치**: 본문은 gap = `MAE_CV − MAE_train`, `Fig. S4` 캡션은 *"absolute difference between
training and test MAE"* — **두 다른 양이다.** 어느 쪽이 그림의 y 축인지 알 수 없다.

**10-5. `E_hull = 0` 단일 필터가 비현실적 후보를 통과시킨다.**
`Fig. S1` 상위 20 에 **LiAl₂H₆BrO₆ · LiH₂BrO · Li₃B₅(HO₅)₂ · Sr₂LiB₁₀H₃O₁₉** — **수소 함유 상 4 종**이 있다.
전지 코팅으로 쓸 수 없는 수화물·수산화물이다. 열역학 문턱만 걸고 **화학적 타당성 필터가 없다.**
(확장셋에는 M-pool 제약이 있지만 학습셋에는 없다 — 그런데 **학습셋이 ML 의 라벨을 만든다.**)

**10-6. Cl-rich 아지로다이트 행이 교락돼 있고 조성식이 틀렸다.**
`Li₅.₅PS₅Cl₁.₅` 는 **전하중성이 안 맞는다**(양 10.5+ vs 음 11.5−). 의도는 거의 확실히 `Li₅.₅PS₄.₅Cl₁.₅` 다.
**어느 MP entry 를 썼는지 SI 에 없다.** 또한 Li₆PS₅Cl → 그 조성은 **Cl 증가와 Li 감소가 동시에 일어나** 교락된다
— §3b-(3) 의 −13 meV/atom 을 "Cl 효과" 로만 읽으면 안 된다.
게다가 **Li₆PS₅Cl = Li₆PS₅Br 이 10/10 비트동일**한 것을 저자는 **언급조차 하지 않는다** —
7 행 중 2 행이 완전 중복이면 *"할로겐 치환 효과를 담았다"* 는 Methods 의 서술이 사실상 공허하다.

**10-7. 적용가능영역 주장이 하위집합에서 깨진다 (`Fig. S5` 실독).**
본문은 *"94.6 % within the core reference domain"* 을 521 종 전체로 말하지만,
`Fig. S5a` 에서 **Li–M–O(144 종)의 중앙값(≈5.4)이 참조셋 중앙값(≈4.9)보다 높다.**
즉 **Li–M–O 가 Li–M–A–O 보다 훨씬 외삽적**인데 본문은 뭉뚱그린다.
그리고 실제로 `Fig. 6a`(Li–M–O)의 산포가 `Fig. 6b`(Li–M–A–O)보다 뚜렷이 넓다 — **저자가 이 상관을 안 짚는다.**

**10-8. 재현 불가.** MP 스냅샷 버전·날짜 미기재 · 화학량론 표집 경계 미기재 · 난수 시드 미기재 ·
**809 종 / 521 종 목록과 계산값의 기계판독 파일 없음** (Data Availability 는 SI 를 가리키는데 SI 엔 표 2 개뿐).
⇒ §7c 의 [Xiao19] 대비 **158 meV/atom 불일치**를 추적할 방법이 없다.

**10-9. 열역학만으로 코팅을 고르는 것의 근본 한계 — 저자도 인정한다.**
반응속도 · 계면 미세구조 · 코팅 두께/균일도 · 접착 · 공간전하층 · 변형/부피변화 · **코팅을 가로지르는 Li 수송**
전부 없다. 특히 **Li 전도도를 안 봤는데** `Fig. 7` 챔피언들이 Li₃PO₄(10⁻⁶~10⁻⁸) · LiAlO₂(5.6×10⁻⁸) ·
Li₂ZrO₃(10⁻¹²) 로 **절연체에 가깝다**(`Table S2`). *"충분히 얇으면 된다"* 는 변론은 있지만
**두께–저항 트레이드오프를 정량화하지 않았다.**

**10-10. 실험 검증 0.** 합성·구조분석·전기화학 시험이 하나도 없다. 검증은 전부 내부적이다
(패리티 · 적용가능영역 · proxy label). 예측된 신조성 중 **실제로 만들어진 것은 0 종**이다.

---

## 11. 우리 원장 매핑

| 우리 원장 | 이 논문이 주는 것 | 처리 |
|---|---|---|
| `comparison_vs_ours.md` **§B③** (cathode 계면) | Li₆PS₅Cl 행 전수 + Cl-rich 델타 + [Xiao19] 와의 158 meV/atom 불일치 | ✅ **§B③ 에 행 추가** (소환값 표기) |
| `comparison_vs_ours.md` **§J** (ML 방법) | 대리모형 MAE 31 vs 문턱 50 · Max Group 단독 지배 · in-sample R² 함정 | ✅ **§J-16 신설** |
| `db/properties/*` | **없음** — 이식 금지 | ⛔ |
| `our_dft_baseline.md` | 변경 없음 (우리 값에 영향 없음) | — |
| `kb/` 규율 | *"문헌 수치는 소환값"* 의 **정량적 근거**(같은 식·같은 도구에서 158 meV/atom 갈림) | ✅ §7c 에 기록 |

---

## 12. 적용 인사이트 ★

**12-1. 🔴 우리 §B 의 "전압 축" 을 novelty 의 1 번 다리로 승격한다.**
지금까지 우리는 전압 축을 *"더 자세히 본다"* 정도로 다뤘다. 이 논문이 확인해 준 것은
**최근접 선행연구가 그 축을 아예 안 가졌다**는 것이고, 저자들이 그것을 **미래 과제로 명시**했다는 것이다
(*"electrochemical stability-window … could further support candidate down-selection"*).
⇒ intro 의 gap 문장을 **이 인용으로 직접 만든다.**

**12-2. 🔴 `Fig. 1a` 의 아지로다이트 순위를 우리 물질 선택의 외부 근거로 쓴다.**
Li₆PS₅Cl 이 **7 종 황화물 중 산화물 양극에 가장 온건**(−336.5, 최악 Li₇P₃S₁₁ −474.8)하다는 것은
우리가 아지로다이트를 고른 것에 대한 **독립 3자 근거**다. (⚠ 소환값 · 순위로만 인용)

**12-3. 🔴 우리 §B③ 값을 문헌과 나란히 쓸 때의 규율을 강화한다.**
같은 식·같은 도구인데 LiMn₂O₄ 에서 **158 meV/atom** 이 갈린다(§7c).
⇒ **앞으로 문헌 반응에너지와 우리 값을 같은 표에 놓을 때는 (a) 같은 hull 스냅샷 재계산 또는
(b) 순위·부호만 비교** 둘 중 하나를 반드시 쓴다. 절대값 병기는 금지에 준한다.

**12-4. ZrO₂ₓ 코팅 축(`choi2026_bzox_dry_zro2x_nmc_shell_coating`)에 열역학 경고를 붙인다.**
이 논문은 Zr·Hf 산화물이 **양극엔 온건하지만 황화물 SE 에 −44~−105 meV/atom** 임을 보인다
(Li₂Zr₂O₅ −70~−105 · Li₂ZrO₃ ⟨E⟩_SSE −111.7 · Li₂Hf₂O₅ −55~−68).
여기에 `Table S2` 의 **Li₂ZrO₃ ≈ 10⁻¹² S/cm** 를 겹치면 **Zr 코팅은 전해질 쪽 반응성 + 절연성 이중 감점**이다.
⇒ 그 digest 에 교차링크할 가치가 있다. 🔑 그리고 **Li₆Zr(PO₅)₂ 가 그 독성을 −14~−19 로 지운다** —
**"인산염화가 금속산화물의 황화물 독성을 가린다"** 는 우리 §D 와 같은 방향의 외부 사례다(기전은 없다).

**12-5. `Fig. 1b` L 자를 우리 §E 그림의 문법으로 빌린다.**
⟨E⟩_cathode vs ⟨E⟩_electrolyte 산점 + 양축 문턱선은 dual compatibility 를 보여주는 **가장 경제적인 표현**이다.
우리는 여기에 **전압 축을 색이나 궤적으로 얹으면** 그들이 못 한 것을 한 장으로 보여줄 수 있다
(점이 전압에 따라 우상단에서 좌하단으로 이동하는 그림).

**12-6. ML 대리모형을 우리 cascade 에 넣는다면 이 논문이 반면교사다.**
판정 문턱보다 큰 MAE 로 순위를 매기면 안 된다(§10-4). 우리 `kb/templates/estimand_card.md` 의
*"던지기 전에 보고량 정의"* 규율로 말하면, **이 논문은 보고량(min_x E_reaction)은 잘 정의했는데
판정 게이트(−50)와 측정 불확도(31)의 관계를 정의하지 않았다.** 우리는 그걸 먼저 박는다.

---

## 13. 🔴 우리가 여전히 주장할 수 있는 것 (원고에 그대로 옮길 문장 단위)

> ⚠ 아래는 **이 논문 원문을 읽고 확인한 범위**에서만 방어된다. 확인 못 한 범위는 §0a 에 적었다.

**13-1. 전압 축 (가장 강함)**
> *"Prior high-throughput interfacial screening for ASSLIBs evaluates the closed-system pseudo-binary reaction
> energy at a single, fully lithiated state [Park 2026; Richards 2016]. We evaluate the same quantity in the
> grand-potential ensemble across 2.5–4.5 V and retain the full reaction-energy profile rather than its minimum,
> which resolves the potential dependence that a single closed-system minimum cannot express."*
> — 근거: `grand`·`applied potential`·`μ_Li`·`kink` 가 Park 본문·SI 에 **0 회**.

**13-2. in-situ 도펀트 보호상 (개념 자체가 그들에게 없다)**
> *"Existing ML-guided interface design frames the problem as **selecting an externally deposited coating**
> [Park 2026], where the metal pool is restricted by construction to **redox-inactive, fixed-valence** cations.
> We instead ask whether a dopant inside the electrolyte can generate the protective phase **in situ** at the
> interface — a mode that is outside the candidate-construction rules of that framework."*
> — 근거: `Fig. 5` 의 `M selection: Redox-inactive, Fixed-valence metal` 칸 + `in situ` **0 회**.

**13-3. 정량 보호율 (닫힌 식이 없다)**
> *"Thermodynamic interface screening yields **ranked candidate lists** [Park 2026]. It does not yield a
> closed-form relation between dopant content and the degree of protection. We report one with **no fitted
> parameter**, in which the coefficient is fixed by the P/Nd ratio of the phosphate selected by the hull."*
> — 근거: `coverage`·`passivat*`·`scaling law`·`closed-form`·`analytic` **0 회**.

**13-4. 기전 — Li 를 안 쓰는 인산염 경로**
> *"Composition-level screening identifies phosphate and oxide-polyanion families as low-reactivity
> [Park 2026], but explicitly declines to forecast reaction products. The distinction that matters for an
> electrolyte-side dopant is **whether the protective phosphate consumes Li from the electrolyte**; that axis
> (Li/P) does not appear in composition-descriptor screening."*
> — 근거: 저자 자인 *"rather than precise forecasts of reaction products"* + `Li/P`·`Li content` **0 회**.

**13-5. dual compatibility 의 동적 판**
> §7b 의 문장 그대로.

**13-6. ⛔ 쓰면 안 되는 문장 (선점됐다)**
- ❌ *"란타나이드 + 폴리음이온 산화물이 계면 저반응성 영역이라는 것을 우리가 처음 보였다"*
  → **틀렸다.** Park 의 M-pool(La·Gd·Dy·Ho·Er·Lu) + `Fig. S1` 의 `LiTmSiO₄` + `Table S1` 의 `LiLa(WO₄)₂`.
  ✅ 대신: *"란타나이드 계열이 저반응성 영역에 속한다는 것은 조성 수준에서 알려져 있었으나 [Park 2026],
  그 계열은 그 연구의 대리모형에서 **적용가능영역 p95 를 넘는 최저신뢰 구간**에 있었고 최종 후보에 오르지 못했다."*
- ❌ *"hull 반응에너지로 계면 상성을 대량 스캔하는 것이 우리 방법의 새로움이다"*
  → **틀렸다.** [Richards16]·[Xiao19]·[Aykol16]·[Park26] 계보다. **novelty 는 축과 대상에 있지 방법에 없다.**
- ❌ *"Cl-rich 아지로다이트가 산화 안정성이 좋다"* (축 없이)
  → 이 논문의 축 B③ 표가 **반대 방향(−13 meV/atom)** 이다. 축을 반드시 명명한다.

---

## 14. 인용 가능 문장 (영문 초안)

- *"Across ten oxide cathodes and seven sulfide electrolytes, the mutual interfacial reaction energy averages
  ≈ −332 meV/atom, i.e. bare oxide–sulfide contacts are thermodynamically unusable without a buffer layer."*
  (Park 2026, `Fig. 1a`; 70-cell mean, 우리가 재계산으로 확인)
- *"Only 53 of 809 hull-stable Li-containing compounds satisfy a −50 meV/atom low-reactivity criterion against
  both the cathode and the electrolyte set (6.6 %)."* (Park 2026, `Fig. 1b`)
- *"Among sulfide electrolytes, argyrodites show the weakest driving force against oxide cathodes
  (Li₆PS₅Cl, mean −336.5 meV/atom over eight oxide cathodes), while Li₇P₃S₁₁ shows the strongest
  (−474.8 meV/atom)."* (Park 2026, `Fig. 1a` 로부터 우리가 계산 — ⚠ 소환값, 순위로만)
- *"Li₆PS₅Cl and Li₆PS₅Br give **numerically identical** reaction energies against all ten cathodes in this
  metric, indicating that the closed-system contact-reaction energy does not resolve halide identity."*
  (Park 2026, `Fig. 1a`; 저자는 이 사실을 논평하지 않는다)
- *"The authors themselves identify electrochemical stability-window and Li-ion migration analyses as checks
  that 'could further support candidate down-selection' — neither is performed."* (Park 2026, §2.4 말미)

⛔ **인용 금지**: `R² = 0.9805` (in-sample) · `Table S2` 전도도 (이중 인용) · Cl-rich 델타를 "Cl 효과" 단독으로 (Li 교락).

---

## 15. 추가로 구해야 할 논문

1. **Kim, Jang, Yu**, *"Rational Materials Design for Stable Interfaces in All-Solid-State **Potassium**-Ion
   Batteries"*, *J. Mater. Chem. A* **13**, 39013 (2025), DOI `10.1039/D5TA07134H` — 🔴 **같은 그룹 시리즈 1편.
   이 그룹의 규약(전압 축을 쓰는지)이 거기 있을 수 있다.**
2. **Jang, Kwon, Jeon, Kim, Yu**, *"Interfacial Stability and Design Strategies for **Halide** Solid Electrolytes
   in High-Voltage All-Solid-State **Sodium**-Ion Batteries"*, *Small Methods* **10**, 02179 (2026),
   DOI `10.1002/smtd.202502179` — 🔴 **시리즈 2편. 제목에 "High-Voltage" 가 있다 → 전압 축을 쓸 가능성이 있다.
   이것이 확인되면 §13-1 의 강도가 달라진다. 최우선.**
3. **Nolan, Liu, Mo**, *"Solid-State Chemistries Stable With High-Energy Cathodes"*, *ACS Energy Lett.* **4**,
   2444 (2019) (Park ref 53) — 우리 §B 계보에 아직 digest 가 없다.
4. **Fitzhugh, Chen, Wang, Ye, Li**, *"Solid–Electrolyte-Interphase Design in Constrained Ensemble"*,
   *EES* **14**, 4574 (2021) (Park ref 25) — **"constrained ensemble"** = 기계적 구속을 넣은 계면 열역학.
   우리 §B 의 구속 축과 직접 관련.
5. **Jung, Sun, Kim, Shin, Min**, *"Scalable AI-Accelerated Design of Dual-Doped LGPS Electrolytes"*,
   *eTransportation* **28**, 100570 (2026) (Park ref 37) — ✅ **확보·판정 완료 (2026-09-22)**
   → `papers/jung2026_scalable_ai_dual_doped_lgps.md` · **판정 🟡 인접(선점 아님)**.
   계(LGPS ≠ 아지로다이트)·도펀트공간(**Nd·란타나이드 0종**)·"dual-doped" 의 뜻(자리쌍 조합론 +
   Li 가감 전하보정)이 갈려 **우리 Nd/O 서사는 선점되지 않았다**. 단 *"ML 대리모형 → DFT ECW →
   AIMD σ"* **프레임**과 *"S 자리 최적 도펀트는 Cl·O"* **결론**은 선점됐다 →
   `comparison_vs_ours.md` **§J-30**.
6. **Lee, Noh, Seong, Lee, Park**, *"Suppressing Unfavorable Interfacial Reactions Using Polyanionic Oxides
   as Efficient Buffer Layers: Low-Cost Li₃PO₄ Coatings"*, *ACS AMI* **15**, 12998 (2023) (Park ref 46) —
   `Fig. 7` 챔피언 Li₃PO₄ 의 실험 판.

---

## 16. 기법 용어 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **pseudo-binary reaction energy** | 두 상을 몰분율 x 로 섞었을 때 상도 최소에너지와 기계적 혼합의 차 | 식 (1)–(3). **닫힌계** |
| **E_hull** (energy above hull) | 볼록껍질 위 거리. 0 = 열역학적 안정상 | 후보 필터: **= 0 만** |
| **grand potential** | Li 저장소에 열린 계의 퍼텐셜 Φ = E − n_Li μ_Li. 전압 축이 여기서 나온다 | **없음** ← 우리와의 결정적 차이 |
| **HDBSCAN** | 밀도 기반 군집. 저밀도 점을 noise 로 라벨 | **noise 제거 전용** (군집 정의엔 안 씀) |
| **k-medoids (PAM)** | 군집 대표를 실제 데이터점(medoid)으로 잡는 분할. 이상치에 강함 | **k = 4 채택** |
| **silhouette score** | 군집 내 응집 vs 군집 간 분리. 높을수록 좋음 (−1~1) | 선택 기준 (i) |
| **RSD (σ/μ)** | 군집 크기의 상대표준편차. 낮을수록 균형 | 선택 기준 (ii) — **실제로는 안 갈랐다** §10-2 |
| **MAGPIE** | 원소 물성(전기음성도·반지름·원자가전자…)을 조성 가중 통계(평균·범위·분산)로 만드는 표준 서술자 세트 | matminer 경유 |
| **Max Group (Period.)** | 구성원소 중 **최대 주기율표 족번호**. 사실상 음이온 정체 지시자 | 🔴 중요도 압도적 1 위 §10-3 |
| **Mean GS Band Gap** | 구성원소 **단체(elemental form)** 의 바닥상태 밴드갭 평균 | ⚠ **화합물 갭이 아니다** — 우리 축 D 와 무관 |
| **XGB / HGBR** | 그래디언트 부스팅 트리 두 구현(XGBoost / sklearn HistGradientBoosting) | 0.44 / 0.56 앙상블 |
| **OOF (out-of-fold)** | CV 에서 각 fold 의 검증 예측만 모은 것. 누수 없는 앙상블 가중 최적화에 씀 | 가중치·중요도 산출 |
| **permutation importance** | 특징을 무작위로 섞었을 때 오차 증가량. **인과가 아니라 예측 기여** | 저자도 인과 아님을 명시 |
| **applicability domain** | 모형이 믿을 만한 서술자 공간 영역. 보통 참조셋까지의 거리로 정의 | 5-NN 평균거리 + LOO p90/95/99 |
| **proxy label** | 참값 대신 쓰는 대체 라벨 | MP 미수록 조성 = **전구체 hull assemblage 반응에너지** |
| **UpSet plot** | 집합 교집합을 막대+점행렬로 보여주는 벤다이어그램 대체 | `Fig. 3` (Cluster 3 음이온 조합) |

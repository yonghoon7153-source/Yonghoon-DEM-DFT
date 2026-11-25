# Hard and soft electrons and holes — Mulks (Chem, Cell Press, 2024)

> slug `mulks2024_hard_soft_electrons_holes` · DOI `10.1016/j.chempr.2024.06.013` · type `theory/DFT (분자, 주기계 아님)` · PDF `1572305d-53._Hard_and_soft_electrons_and_holes.pdf` (+SI `c7ffc0a4`.xlsx, `c247bf09`.pdf, `8eb8cb54`.pdf) · digested `2026-08-05` · **재검증 `2026-08-06`**(Table 1 산술 전수 대조 → 오타 4건 + 머리글 오류 확정, §14b) · status ✅
> **저자**: **Florian F. Mulks** — *단독 저자* (Institute of Organic Chemistry, RWTH Aachen University, Landoltweg 1, 52074 Aachen, Germany; lead contact `ff@mulks.ac`). Chem **10**, 2724–2744 (September 12, 2024). Received Jan 6 2024 / Revised Mar 31 2024 / Accepted Jun 12 2024 / Published (online) Jul 8 2024. Open Access CC BY 4.0. 데이터셋 ioChem-BD `10.19061/iochem-bd-6-328`.
> ⚠ **인용 표기 주의**: "Mulks **et al.**" 이 아니라 **"Mulks"** — 저자 1명이다 (fan2026 리뷰 §3.1 ref [80] 표기 정정 대상).


> elements: Cl F H Li O S
> methods: bader, bandgap, bvse, cohp, dft, dos, elf, esw, functional, kpoint, md, mlip, neb, pdos, pseudo

---

## 0. 이 digest를 읽는 법 — 왜 지금 이 논문인가

이 논문은 **황화물 고체전해질 논문이 아니다. 배터리 논문도 아니다.** 유기·유기금속 분자의
**regioselectivity(어느 자리에서 반응하나)** 를 예측하는 **개념 화학(conceptual DFT) 논문**이다.

우리가 이걸 읽는 이유는 하나다 — 1저자가 심사 중인 리뷰 원고
`fan2026_sulfide_assb_stability_review_ECERD2600097` 가 **§3.1 (공기/수분 안정성)** 에서
이 논문을 **ref [80]** 으로 끌어와

> "The Hard-Soft-Electron-Hole theory proposed by Mulks et al. extends the HSAB concept to
> multi-electron systems [80]."

라고 쓴다. 우리 리뷰어 노트 `kb/reviews/ECERD2600097_review_notes.md` 의 **A5** 항목이
"이게 정당한 인용인가, name-drop 인가"를 판정하라고 걸어 뒀다. **§1.5 에 그 답이 있다.**

---

## 1. 한 줄 요약

전자 **하나**를 더/덜 넣었을 때와 전자 **한 쌍**을 더/덜 넣었을 때 전자밀도가 *다르게* 재배치된다는
사실을 이용해, 분자 안에서 **"딱딱한(hard) 자리"와 "무른(soft) 자리"를 하나의 부호 있는 양으로 동시에
집어내는** 기술자(EHR / EHI)를 정의하고, HSAB·Fukui 함수가 틀리는 30여 개 ambident 분자에서
실험 regioselectivity 를 사후 재현한다. **정의식과 계산 레시피는 명확하지만, 정량 예측 모델은 아직 아니다**
(저자 본인이 "정량 관계 확립엔 추가 연구 필요"라고 명시).

## 1.5 ★ 리뷰어 A5 에 대한 직답 (이 digest 의 존재 이유)

### ① HSEH 가 황화물 SE(또는 무기 고체)에 적용된 선례가 이 논문 안에 있나?
**없다. 0건.** 근거를 전수로 적는다.

| 점검 항목 | 이 논문의 실제 내용 |
|---|---|
| 계산 대상 | **전부 이산 분자/이온/유기금속 착체** — 분자 1–30 (Fig. 4, Fig. 6–9). 주기계(periodic) **0개** |
| 코드 | **ORCA 5.0.4** (가우시안 기저 분자 코드) + xTB 6.4.0 + autodE 1.3.0 + RDKit. 평면파·k-point·PAW **전무** |
| 경계조건 | **기체상(gas phase), 용매 모델 없음**(DMSO 1건만 CPCM 감도 테스트) |
| 표면/계면 | **없음**. 흡착·표면·슬랩·GB 계산 0건 |
| 황화물 | **없음**. S 를 포함한 종은 **DMSO(1)**·**thiocyanate SCN⁻(2)**·티올 첨가 논의뿐 — 전부 분자 |
| Li | **1건뿐**: 분자 **17** = (E)-pent-3-en-2-one 의 **Li⁺ 배위 착체**(리튬 엔올레이트 모형). 고체 Li 화합물 아님 |
| 고체와 가장 가까운 것 | 분자 **27** (potassium zincate). 본문: *"A simplification of the structure **in the solid state** was utilized"* — **결정 구조를 잘라 분자 단량체로 축소**해 계산. 즉 고체를 *피해서* 계산한 사례 |
| "재료과학" 언급 | benzo[a]pyrene **18** 을 *"Semiconductor"* 라 부르는 Fig. 6 불릿 한 줄. 계산 자체는 고립 분자 |
| 전기화학 접점 | Fig. 6 의 **Pt 전극 SET(1전자 산화)** 경로 — 단, 용액 중 *분자* 의 전기화학 |

**단, 문헌 자체엔 주기계 확장 도구가 있다** (이 논문이 *인용만* 하고 쓰지 않은 것):
- ref **[29]** Cerón, Gomez, Calatayud, Cárdenas, *J. Phys. Chem. A* **124**, 2826 (2020),
  "**Computing the Fukui Function in Solid-State Chemistry: Application to Alkaline Earth Oxides
  Bulk and Surfaces**" ← 주기계 Fukui 함수 선례
- ref **[51]** Yang & Parr, *PNAS* **82**, 6723 (1985), "Hardness, softness, and the fukui function
  in the electronic theory of **metals and catalysis**"

→ **판정**: HSEH 의 *1차 도구인 Fukui 함수* 는 고체에 적용된 전례가 있으나,
**HSEH(EHR/EHI) 자체가 무기 고체·황화물에 적용된 선례는 이 논문 안에 없고, 이 논문이 그런 주장을 하지도 않는다.**
리뷰가 §3.1 가수분해 문맥에 끌어온 것은 **유비(analogy)/개념 수입**이다.

### ② HSAB 대비 무엇을 새로 설명·예측하나? 정량 기준이 있나?

**(a) 새로 설명하는 것 — 명확히 있다.** HSAB 는 *종(species) 단위 전역 분류*(hard acid / soft base)여서
**한 분자 안 어느 자리인지**를 말하지 못한다. Fukui 함수(FF)는 자리 분해는 되지만 **soft/orbital-control
쪽만** 잡고 **local hardness 는 정의가 모호**하다(본문: *"Local hardness is less straightforward to define.
The hardest sites, by definition, are electronically unresponsive"*). HSEH 는 **하나의 부호 있는 양으로
hard 자리와 soft 자리를 동시에** 집어낸다.
그리고 **HSAB·FF 가 틀리는 케이스를 뒤집는다** — 대표 4건:

| 분자 | HSAB / FF 예측 | HSEH(EHI) 예측 | 실험 |
|---|---|---|---|
| **SCN⁻ (2)** | S = soft 자리 (FF f⁻ S 654 > N 265) | **S 가 hard** (EHI **+78**), N 이 soft (−46) | hard 카보양이온·soft 할로알칸 **둘 다 S 에서** 반응; HSCN 도 S–H |
| **CN⁻ (3)** | C = soft (f⁻ C 642 > N 358) | **C 가 hard** (+114), N 이 soft (−114) | hard 카보양이온이 **C 에서** 반응; HCN 도 C–H |
| **isoquinoline (8)** | FMO·FF 모두 **C3 → C4** 예측 (틀림) | **C5 가 soft 최우선**(−28), C3 가 가장 hard(+24) | 니트로화 **C5 90 % / C8 10 %** |
| **isoquinolinium (8H⁺)** | — | **C8 이 가장 hard 반응 자리**(+26) | 강산(H₂SO₄/HNO₃) 조건의 C8 생성물 설명 |

**(b) 정량 기준(descriptor) — 정의식은 있다.** 세 가지 단일점 계산만으로 계산 가능:

- **전자경도 응답 EHR** (실공간 장, Eq. 5A/5B):
  - 친전자체: `f^(2,+)(r) = ρ_{N+2}(r) − 2ρ_{N+1}(r) + ρ_N(r)`
  - 친핵체: `f^(2,−)(r) = ρ_N(r) − 2ρ_{N−1}(r) + ρ_{N−2}(r)`
  - **부호 규약: 양 = hard(lone-pair 형), 음 = soft(radical 형)**. `∫f^(2,±)(r)dr = 0`
- **전자경도 지수 EHI** (원자별 스칼라, Eq. 6A/6B — 원자전하 `q_k` 만 있으면 됨):
  - 친전자체: `f_k^(2,+) = q_k(N+2) − 2q_k(N+1) + q_k(N)`
  - 친핵체: `f_k^(2,−) = q_k(N) − 2q_k(N−1) + q_k(N−2)`
  - `Σ_k f_k^(2,±) = 0`. 논문 전체가 **10⁻³ e** 단위로 보고
- 계산 절차(Fig. 2 / Fig. S1): ① N-전자 기하 최적화 → ② **같은 기하에서** N, N±1, N±2 세 단일점
  → ③ 밀도 뺄셈(Eq. 5) 후 총밀도에 투영해 시각화 + ④ Hirshfeld 전하로 EHI 계산.
  Data S1(xlsx)이 **빈 계산 템플릿**(Nucleophile/Electrophile 시트, 셀 수식 `f=-(D-C)`, `f2=-(E-D)`,
  `f^(2)=f2-f`, SUM/MAX/MIN 정합성 검사 포함)으로 배포된다.

**(c) 그러나 "정량 예측 모델"은 아니다 — 이게 핵심 유보.** 본문 원문:
> *"Larger values imply pronounced reactivity differences, whereas smaller values suggest minor
> selectivity differences… **Further studies are needed to establish quantitative relationships.**"*

즉 **부호·순위(ranking) 기술자**이지, 선택성 %·ΔΔG‡ 로 환산되는 보정된 예측자가 아니다.
논문에 **상관 플롯·회귀·오차지표가 하나도 없다.** 전부 사례별 사후 합리화(post-hoc rationalization).
저자 스스로 pyridine 5 에서 *"differences as small as 10⁻³ e cannot be considered meaningful"* 라고
자기 해상도 한계를 긋는다.

**(d) 수학적 신규성도 제한적** — 본문이 직접 인정한다:
> *"This approach is **identical to evaluating the dual descriptor** f^(2)(r) of an N ± 1 system
> at the N electron system's geometry."*

**dual descriptor 자체는 기존 conceptual-DFT 양**(refs 53–57, Morell/Grand/Toro-Labbé).
신규성은 **(i) 해석**("전자 하나 = radical-like = soft" / "전자 쌍 = lone-pair-like = hard" 로 *전자·홀의
경도* 라 부르기), **(ii) 표준 프로토콜·튜토리얼·스프레드시트 배포**, **(iii) 30여 사례의 폭** 이다.

### → A5 판정 (리뷰어로서 어떻게 쓸 것인가)
**"name-drop 이라 삭제하라"는 과하다. 하지만 "그대로 두라"도 아니다.** 세 가지로 갈라 쓴다.

1. **인용 자체는 사실관계상 정확** — "HSAB 를 다전자계로 확장했다"는 문장은 **[80] 의 내용과 맞다.**
   그러므로 *허위 인용* 지적은 성립하지 않는다.
2. **하지만 §3.1 문맥(황화물 격자의 가수분해)에는 근거가 없다.** [80] 은 무기 고체·주기계·표면
   계산을 **하나도** 하지 않는다. 만약 원고가 (우리 digest 의 §5.2 요약처럼) "전자·홀 거동으로
   **황화물 격자의 전자구조 진화**를 설명한다"는 취지까지 나아간다면 **그 부분은 [80] 이 지지하지 않는다.**
3. **요구할 것 한 문장**: "HSEH 가 이 리뷰에서 무엇을 새로 설명/예측하는가"를 명시하고,
   **무기 고체 적용 선례가 없음(분자 반응 regioselectivity 한정)** 을 밝히거나,
   쓰려면 **계산 가능한 양(EHR/EHI)** 을 지목해 "P–S 결합의 어느 원자가 hard/soft 자리인가"를
   구체적으로 말하게 할 것. 덧붙여 **"Mulks et al." → "Mulks"** (단독 저자) 표기 정정.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | Florian F. Mulks (단독) — RWTH Aachen, Institute of Organic Chemistry |
| 저널/년 | **Chem** (Cell Press) **10**, 2724–2744, 2024 |
| DOI | 10.1016/j.chempr.2024.06.013 (Open Access CC BY 4.0) |
| 조성/대상 | 유기·유기금속 **분자 30종** (황화물 SE 무관) |
| 연구유형 | 순수 이론/계산 (conceptual DFT). **실험 0건**, 실험은 전부 문헌 소환 |
| 데이터 | ioChem-BD DOI 10.19061/iochem-bd-6-328; Data S1 = 계산용 xlsx 템플릿; Video S1 = 튜토리얼 영상 |
| 지원 | Fonds der Chemischen Industrie Liebig Fellowship (Li 210/01), AvH Feodor Lynen Return Fellowship, RWTH 계산자원 rwth0928/rwth1236 |
| 이해상충 | 저자가 **Chem 의 "Next-Generation" Advisory Board** 소속 (본인 명시) |
| 편집도구 | DeepL + Word 사용 명시 |
| 로컬 파일 | **inbox #53 · 사용자 분류 폴더 `DFT`**. 본문 22 pp + SI 60 pp. **SI 원본 = `inbox/53. Sup2) …pdf`(60 pp, 깨끗한 SI 단독본 — 그림 51장 중 41장의 추출 source)**. 업로드된 `53. Sup3) …pdf`(82 pp)는 **본문+SI 이어붙인 중복본**(§14-12·§14c-A) — 그림 추출에 넣지 말 것. SI 평문 = `inbox/_53si3_text.txt` |
| 검증 이력 | 1차 digest 2026-08-05 · **2차** Table 1 산술 전수 대조 2026-08-06(§14b, 오타 4건) · **3차** SI 실물 기계 검산 2026-08-06(§14c, Table S3 오류 4건·Table S6 재현 실패·라벨 오류 6건) · **4차** SI-2 재투입 중복 판정 2026-08-06(§14d, 60/60쪽 완전 일치 — 신규 내용 0건) |

## 3. 핵심 물성 (수치) — **이 논문엔 없다**

| 물성 | 값 | 비고 |
|---|---|---|
| 이온전도도 σ | **n/a** | 측정·계산 없음 |
| 활성화E Ea | **n/a** | 없음 |
| 산화 onset / ESW | **n/a** | 없음 |
| 기계적 (E/B/G, C_ij) | **n/a** | 없음 |
| 전자구조 (gap, VBM/CBM) | **n/a** | **밴드갭 개념 자체가 없음**(분자 HOMO–LUMO 정성 언급만) |
| 이 논문이 내놓는 유일한 수치 | **FI(f^±), f^(±2), EHI(f^(2,±))**, 단위 **10⁻³ e** | Table 1(본문) + Tables S7–S33(SI, 원자 전수) |

> ⚠ **소환값 규율**: 아래 모든 숫자는 **DSD-BLYP-D3BJ/def2-QZVPP//PBEh-3c, 기체상, Hirshfeld 전하**
> 조건의 값이다. 우리 db(comp1/modelc)의 어떤 값과도 **같은 표에 넣지 않는다** — 물리량 종류가 아예 다르다.

## 4. DFT/계산 방법 ★

- **code / version**: **ORCA 5.0.4** (단일점·최적화·Hessian) · **xTB 6.4.0** (GFN2-xTB, conformer 사전 최적화) ·
  **autodE 1.3.0** (파이프라인·ZPE/자유에너지 보정·TS 탐색 템플릿) · **RDKit 2022.03.4** (ETKDGv3 로 SMILES→conformer) ·
  **ChemCraft b688bt_win64** (밀도 대수 연산·시각화)
- **functional + vdW**:
  - **기하 최적화**: **PBEh-3c** (triple-corrected composite) / **def2-mSVP**, RIJCOSX + def2/J
  - **단일점(전하·밀도)**: **DSD-BLYP** (double-hybrid, spin-component-scaled) + **D3BJ** / **def2-QZVPP**,
    보조기저 def2/J + def2-QZVPP/C, `TightSCF keepdens`
  - 예외: **enfumafungin 24** 만 **def2-TZVPP** (크기 때문, Fig. 7 캡션 명시)
- **pseudo / PAW**: **해당 없음** — 전자 all-electron 가우시안 기저(분자 코드)
- **k-points / ecut / supercell / nat**: **해당 없음(주기계 아님)**. 밀도 cube 는 **각 축 80 grid interval**
- **DFT+U**: 없음
- **AIMD / MLIP**: 없음. 동역학 계산 전무
- **무질서 처리**: **해당 없음**. 대신 **conformer 샘플링** — SMILES→ETKDGv3→GFN2-xTB 최적화→
  autodE 기본 설정으로 저에너지 conformer 선별→PBEh-3c 재최적화→Hessian 으로 local minimum 확인
- **용매**: **없음(기체상)**. 감도 테스트로 DMSO **1** 만 CPCM(DMSO) 1회 (Table S6)
- **원자전하 분할**: **Hirshfeld**(주). 비교용 **Mulliken** (Tables S4–S5)
- **특이사항**: FI/EHI 정규화 — FI 합 = 1, EHI 합 = 0 (Data S1 의 SUM 행이 이 정합성을 검사)

### 4b. ★ 방법 의존성 — SI 가 스스로 폭로한 것 (우리에게 가장 중요한 절)
저자가 감도 테스트를 성실히 넣어 뒀다. **전부 cyanide 3 (CN⁻) 한 분자 기준.**

| 축 | 조건 | f^(2,−) (C / N) | DSD-BLYP 대비 상대차 |
|---|---|---|---|
| **기저 (Table S1)** | 6-31G* AutoAux | −0.09876 / +0.09876 | **+13.2 %** |
| | def2-SVP | −0.11506 / +0.11506 | −1.1 % |
| | def2-TZVP(P) | −0.11672 / +0.11672 | −2.6 % |
| | **def2-QZVPP (기준)** | **−0.11380 / +0.11382** | 0 |
| **범함수 (Table S2)** | HF-D3BJ | −0.08913 / +0.08914 | **+21.7 %** |
| | **PBE-D3BJ** | −0.06696 / +0.06698 | **+41.2 %** ← |
| | B3LYP-D3BJ | −0.07539 / +0.07541 | **+33.8 %** |
| | **DSD-BLYP-D3BJ (기준)** | −0.11380 / +0.11382 | 0 |

- **🔑 PBE 는 EHI 크기를 4할 넘게 깎는다.** 단 **부호(soft/hard 배정)는 4개 범함수 모두 동일**
  (C 음/soft, N 양/hard). → **"순위·부호는 견고, 절대값은 범함수 자유도"**.
  이건 우리 밴드갭 규율("PBE 과소, wide-gap 수준으로만 비교")과 **완전히 같은 형태의 경고**다.
- **전하 분할 스킴 (Tables S4–S5)**: DMSO **1** 은 Hirshfeld↔Mulliken 정량 차이만.
  그러나 **pyridine 5 에서는 배정이 바뀐다** — Hirshfeld 는 **N(−4.4)** 을 가장 soft 로 뽑는데,
  Mulliken 은 **C2(−0.02386)** 를 뽑고 N(−0.01045)은 2위로 밀린다. SI 본문:
  *"in borderline cases, the qualitative conclusion drawn from EHR considerations can be impacted by
  the charge localisation scheme."* 저자는 Mulliken 이 기저 의존이 심하고 **비물리적 음의 전자수**를
  낼 수 있다며 Hirshfeld 를 권고하되 *"also Hirshfeld charges can fail"* 이라고 붙인다.
- **구조 선택 (Table S3, 1e vs 2e shift)**: N±2 를 중성 기하에서 계산해도 되나?
  acetone **14′**·pentenone **16′** 의 **radical anion 구조**에서 다시 계산 → **응답 진폭은 크게 달라지지만
  EHI 로 정렬한 친전자 자리 *순서는 안 바뀐다*** → "중성 바닥상태 기하에서 평가하라"로 결론.
  🔴 **단 Table S3 자체에 오류 4건**(Δ 열 3행·f⁺² 1칸)이 있고, 인쇄된 표만 읽으면 16′ 에서 순서가 깨져 보인다 —
  SI 원표로 고쳐 계산하면 **결론은 살아난다**. 인용은 Tables S23/S25/S32/S33 에서 직접 계산 (§14c-B).
- **용매 (Table S6)**: DMSO 1 을 CPCM(DMSO)로. EHI 가 >10⁻² e 인 원자는 상대차 작음
  (**논문 인쇄값 O +7.9 %, S +2.1 %**). 그러나 EHI 가 6×10⁻³ e 수준인 양성자 2개는 **상대차 >1(100 % 초과)**.
  → *"care should be taken, particularly in cases of weak EHR"*.
  🔴 **인쇄값은 Table S7(유일하게 공개된 기체상 Hirshfeld)로 재현되지 않는다** — 실제로는 **O +17 %, S +4 %**
  로 약 2배다(§14c-C). 인용할 땐 두 값을 병기한다. 정성 결론은 그대로.
- **EHR 은 전하분할 무관** — 실공간 장이라 분할 스킴이 필요 없다. **EHI(축약값)만** 분할 의존.

## 5. Concept — 개념 전개 (본문 Introduction ~ Concept)

### 5.1 문제 설정 (Fig. 1)
ambident(양쪽성) 반응체에서 **어느 자리가 반응하나**는 화학의 중심 문제인데(단계 경제성·효율·안전),
믿을 만한 단일 예측자가 없다. 기존 도구의 실패를 Fig. 1 이 한 판에 늘어놓는다:
- **kinetic vs thermodynamic**(정확·고비용·비직관) — 전이상태를 다 계산해야 함
- **hard vs soft (HSAB)** — *local hardness 정의가 빈약*, 복잡한 국재화 필요, "trivial case 넘어가면 이해 곤란"
- **orbital vs charge (Klopman–Salem)** — HOMO 는 모호, MESP 는 **가용 오비탈을 반영 못 함**
- **FMO** — 고리화첨가엔 성공, **ambident philicity 서술 실패**
- **Fukui 함수** — soft/orbital-control 만 잡고, **lone pair 또는 radical 쪽으로 원치 않는 편향**
- 배경 근거: **Mayr 의 대규모 실험 데이터가 HSAB 예측과 거의 안 맞는다**(ref 1)

### 5.2 기존 정의 (Eq. 1–3)
- FF: `f⁺(r) = (∂ρ/∂N)⁺ ≅ ρ_{N+1} − ρ_N` (친전자, 전자 받는 자리) / `f⁻(r) ≅ ρ_N − ρ_{N−1}` (친핵, 주는 자리)
- FI(축약): `f_k⁺ ≅ q_k(N+1) − q_k(N)` / `f_k⁻ ≅ q_k(N) − q_k(N−1)`, 합 정규화
- dual descriptor: `f^(2)(r) = f⁺(r) − f⁻(r)` — 친전자·친핵 영역 동시 판정 (≈ 2차 도함수 = hyper-hardness)

### 5.3 핵심 물리 논거 (이 논문의 심장)
> **SOMO(홑전자)는 soft 자리에서 안정화되고(전자상관 강화·저전기음성도·mesomeric 안정화;
> captodative 효과), 고립전자쌍(lone pair)은 hard 중심에서 더 국재화되어 안정화된다.**

엔올레이트 [O⁻–CH=CH₂ ↔ O=CH–C⁻H₂] 예시로 설명: O 는 C 보다 전기음성도가 커서
점유 오비탈 준위가 낮고 원자반경이 작다 → HOMO–LUMO 간격 ↑ = **더 hard** → 고립전자쌍이 O 에
국재화되면 더 낮은 에너지에 더 많은 전자를 몰아넣을 수 있어 안정.
따라서 **오비탈 점유수를 두 번 바꾸면 비슷하지만 *동일하지 않은* 밀도 변화**가 생긴다 — 그 차이가 신호다.
(**전자 경도/무름 ≠ 화학적 경도/무름**임을 저자가 명시적으로 구분한다. 두 개념은 자주 같이 가지만
일치하지 않는 경우가 여럿 나온다.)

### 5.4 정의 (Eq. 4–6) → **§1.5(b)** 에 정리한 식들
Eq. 4A/4B 가 `f^{±2}` (두 번째 전자 이동의 밀도 차), Eq. 5A/5B 가 EHR, Eq. 6A/6B 가 EHI.
FMO 근사(f⁺≅ρ_LUMO, f⁻≅ρ_HOMO)가 정확하다면 `f^{±2}` 와 `f^±` 가 같아야 하지만,
**오비탈 완화(orbital relaxation)** 때문에 다르다 — 그 차이가 곧 EHR 이다.
> **방향 규약(본문 §"The FFs/FIs for nucleophiles point toward the harder part…")**:
> 친핵체에서 FF/FI 는 **hard 쪽**을 가리키고, 친전자체에서는 **soft 쪽**을 가리킨다.
> EHR/EHI **양수 = frontier 오비탈의 hard 부분, 음수 = soft 부분**.

## 6. 결과 — 분자별 상세 (Table 1 전수, 단위 10⁻³ e)

> ⚠ **Table 1 읽는 법**: 앞 블록(1–8H⁺)은 **친핵체 규약** `f⁻ / f⁻² / f^(2,−)`,
> 뒤 블록(7 재등장, 9–17)은 **친전자체 규약** `f⁺ / f⁺² / f^(2,+)` 이다 (표 중간에 헤더가 바뀐다 — 놓치기 쉽다).
> 🔴 **단, 이어짐 페이지(p.2732, 분자 12–17)는 머리글이 `f⁻…`로 잘못 인쇄돼 있다** — 데이터는 친전자체 규약이다 (§14b-14).
> 🔴 **아래 4개 값은 본문 Table 1 의 오타다**(SI 대조 확정, §14b-13): **1** H@C1/C2 의 `63`→**53** ·
> **9** (E)-H@C1 의 `192`→**105** · **10** C1 의 `43`→**54** · **11** C2 의 EHI `+3`→**−3**.
> 아래 본문 서술은 논문 인쇄본을 그대로 옮긴 것이므로, **수치를 인용할 땐 SI Tables S7–S33 을 1차 출처로** 쓴다.

### 6.1 친핵체 (nucleophiles) — 분자 1–8

**DMSO 1** — O 397 / 199 / **+199** · S 227 / 326 / **−100** · H@C1/C2 43 / 63 / −10
FF/FI 는 S–O π결합의 **hard 쪽(O)** 을 가리킨다(보통 soft 반응성 지표로 쓰이는데도).
FF 로 본 가장 hard 한 자리는 양성자들. 그런데 **두 번째 전자를 빼면 S 에 훨씬 크게 국재**된다
→ S 에 강한 음의 EHR(soft), O 에 강한 양의 EHR(hard).
실험: 메틸 할라이드와 반응 시 **kinetic control = O-메틸화, thermodynamic control = S-메틸화**.
methyl *p*-bromobenzenesulfonate, 50 °C → **O-알킬화 94 %**; 더 soft 한 **methyl iodide → O-알킬화 7 %**(=S 93 %).
🔑 이 한 쌍이 **"음의 EHR = soft 응답, 양의 EHR = hard 응답"** 부호 규약의 실험적 정박점.

**Thiocyanate SCN⁻ 2** — S 654 / 575 / **+78** · N 265 / 311 / **−46** → §1.5(a) 표 참조.
**Cyanide CN⁻ 3** — N 358 / 472 / **−114** · C 642 / 528 / **+114** → 동상.
이 둘은 *"HSAB 기반 처리의 실패 사례"* 로 유명한 음이온이고, **EHI 가 HSAB·FF 의 배정을 정반대로 뒤집어
실험과 맞춘다.** 이 논문에서 가장 깨끗한 승리.

**PMDTA 4** (N,N,N′,N″,N″-pentamethyldiethylenetriamine) — N1 −9 / 175 / **−184** · N2 287 / −130 / **+417** ·
N3 6 / 176 / **−170**
말단 N 두 개가 **동시에 soft** 로 잡히고(−184, −170), 중앙 N2 는 FI(287)가 뽑고 EHI 가 **가장 hard(+417)** 로 확증.
비대칭 conformer 가 최안정 구조였음에도 soft/hard 분리가 흐트러지지 않았다(견고성 논거).
**⚠ Table 1 의 "4 | C4 | 43 | 47 | −3.7" 행은 pyridine 5 의 C4 행과 완전히 동일하며,
SI Table S10(PMDTA 전수)에는 그런 값을 갖는 원자가 없다 → 표 복제 오류로 판단** (§10 참조).

**Pyridine 5** — N 60 / 64 / **−4.4** · C2/6 149 / 148 / **+1.0** · C3/5 150 / 154 / **−4.0** · C4 43 / 47 / **−3.7**
HOMO 는 C2·C3·C5·C6 의 π. 실제 친전자 반응(양성자화·메틸화)은 **N 중심**인데
**FMO 도 FF 도 재현 못 한다.** EHR 은 π계를 **거의 상쇄**시키고(그림상 균일한 초록),
축약값은 N 이 가장 soft 이나 **차이가 10⁻³ e 수준이라 의미 없다**고 저자가 스스로 못 박는다.
→ **비-FMO 지배 반응엔 절차 확립 전까지 쓰지 말라**는 자기 제한. (우리에게 중요 — §7 참조)

**Phenolate 6** — O 274 / 147 / **+128** · C1 42 / 83 / **−41** · C2/6 104 / 119 / **−15** · C4 138 / 182 / **−44**
FF: O-공격 강선호 → C4. EHR: **C4 가 soft 로 약간 유리**, O 는 명확히 **hard**.
실험(Fig. 1 상단): TNB(1,3,5-trinitrobenzene)와 −40 °C 에서 **O-attack**(kinetic), 20 °C 에서 **C-attack**.
1,3,5-트리니트로벤젠은 조건에 따라 양쪽 다 되는 경계 사례로 소개된다.
**Phenol 6H⁺** — C3/5 65 / 55 / **+9** · C4 148 / 193 / **−45**: C4 가 뚜렷한 soft, C3/5 는 약한 hard.
알코올(OH)은 *"unreactive with a very weak soft response"*. 페놀은 보통 **C4**(드물게 C2/6)에서 반응하고,
**C3/5 관능화는 template 보조 합성**으로만 달성됨. 탈불소화 시약은 OH 배위·탈양성자화로 시작.

**Nitrobenzene 7** (친핵체 규약) — C1 142 / −90 / **+232** · C2/6 61 / 193 / **−132** · C3/5 83 / 188 / **−104** ·
C4 142 / −90 / **+232**
전자 결핍이라 친전자체 반응성 낮음. ortho(C2/6)가 meta(C3/5)보다 **약간 더 soft**, C1·C4 는 동일한 hard 응답.
산성 니트로화에서 **ortho/meta/para ≈ 1 : 9 : 0**. 가역 ortho 반응 또는 니트로기 입체장애가
실험적 meta 선호를 설명할 수 있다.
**7H⁺** — C1 117 / −64 / **+181** · C2/6 37 / 245 / **−208** · C3/5 94 / 179 / **−85** · C4 161 / −110 / **+271**
→ 양성자화하면 C2/6 가 가장 soft, C4 가 가장 hard.
**7 을 친전자체로 볼 때**(뒤 블록, `f⁺` 규약) — N 141 / 46 / **−95** · O1/2 198 / 91 / **−106** ·
C1 19 / 88 / **+70** · C2/6 51 / 75 / **+24** · C3/5 40 / 61 / **+21** · C4 84 / 140 / **+55**:
**니트로 O 가 soft 자리**로 잡히고 이는 **니트로기 환원**과 정합. C1·C4 는 hard.
부틸 그리냐르 반응은 **ortho : para = 2 : 1** 혼합물 — C1 첨가가 가역이면 높은 ortho 분율이 설명됨.

**Isoquinoline 8 / 8H⁺** — §1.5(a) 표. 8: N 53 / 65 / −12 · C3 113 / 90 / **+24** · C4 101 / 97 / +5 ·
C5 93 / 121 / **−28**. 8H⁺: C3 102 / 123 / −21 · C4 54 / 82 / −29 · **C8 134 / 108 / +26**.
FMO/FF 는 C3→C4 를 뽑아 **틀리고**, EHR 은 **C5 를 명확히** 뽑는다. 두 4급 탄소가 가장 hard.

### 6.2 친전자체 (electrophiles) — 분자 9–17

**1-buten-3-ium 9** (알릴 양이온) — C1 241 / 256 / **+15** · C3 228 / 199 / **−29** · (E)-H@C1 87 / 192 / +18 ·
(Z)-H@C1 70 / 80 / +10 → FI 는 C1 을 soft 로 보나 **EHI 는 C1 이 hard, C3 가 soft**.
**1-chlorobut-2-ene 10** — C1 56 / 43 / −2 · C2 141 / −91 / **−232** · C3 165 / −119 / **−284** · C4 40 / 133 / **+92**
*n*-BuMgBr → **C1 선택성 90 %**; 더 soft 한 *n*-butylcopper → 목표 자리 **21 %**, 나머지 **79 %가 알릴 C3**.
EHR: **C3 에서 강한 soft 응답**(알릴 치환), **C4 양성자가 hard**(→ HCl 제거로 다이엔 가능).
FF 는 쓸 만한 반응 자리를 하나도 못 찾는다(염화물을 soft, 양성자를 hard 로 제시).
**Chlorobutane 11** — C1 44 / 29 / −15 · C2 30 / 27 / +3 · C3 58 / 29 / **−28** · C4 43 / 90 / **+48**
포화계 **비-FMO(σ*) 치환은 두 모델 모두 서술 실패.** LUMO 가 C1·C4 의 **C–C σ-반결합**성(Fig. S8).
**Oxaisoindolium 12** — C2 18 / 17 / −1 · C6a 31 / 70 / **+38** · C10b 136 / 100 / **−36**
kinetic 조건에서 C10b 예상이었으나 가수분해 시 **C2 공격만** 관측(알코올분해도 C2 에서 에테르).
두 지수 모두 **C10b 를 soft 반응 자리로 정확히** 지목. EHI 는 C6a 가 더 hard.
C2 의 C–O 절단은 **늦은 전이상태(late TS)** 라 반응물 전자구조로는 서술이 안 된다 — 11 과 같은 부류.
**Diiminium pyridine adduct 13** (2+, 강한 Lewis 산) — N@Py 66 / 6 / **−60** · C2/6 108 / 78 / **−30** ·
C4 144 / 133 / **−11** · C1′ 10 / 81 / **+70** · H@NMe 13 / 20 / +7
FI 는 pyridine 의 C4·C2/C6 를 soft 산 자리로 잡고 EHI 가 확증. 실험은 **hydride·phosphine 이 C4 에** 첨가.
EHI 는 **kinetic soft 자리 = C2/C6**, FI 는 C4 선호. 두 번째(열역학적) 자리 = **diiminium 탄소 C1′**,
**EHI 가 정확히 hard 최댓값(+70)** 으로 지목(FI 는 양성자를 hard 로 봐서 실험과 무관).
피리딘 치환 시 **플루오라이드가 C1′ 에** 첨가. 4-dimethylaminopyridine 은 경계 사례 —
**C4 즉시 반응 → 수 시간에 걸쳐 addition/elimination 으로 diiminium 탄소 치환**.
**Acetone 14** — O 245 / −123 / **−369** · C1/3 54 / 123 / **+69** · C2 237 / −153 / **−390** ·
H@C1/3 68 / 172 / **+103**
FF: 카보닐 O 가 C2 보다 근소 우세. **FI 최저값과 EHI 최저값이 서로 다른 양성자를 hard 로 지목** →
**hard 염기(수산화물)와는 탈양성자화→엔올레이트→알돌**, soft 탄소친핵체(그리냐르)와는 **카보닐 첨가**.
**Methyl 3-oxobutanoate 15** — O=C3 240 / −153 / **−392** · C3 236 / −180 / **−416** · H@C1′ 15 / 137 / **+122**
FF 는 카보닐 O 다음 C 를 soft 로, **EHI 는 카보닐 C 를 soft 반응 자리로 정확히** 결정.
둘 다 메틸 치환기 양성자를 hard 로 봄. 실제로는 **두 카보닐 사이 가장 산성인 위치**에서 탈양성자화.
**(E)-pent-3-en-2-one 16** (Michael 수용체) — O 163 / 17 / **−146** · C1 37 / 79 / **+42** ·
C2 145 / −1 / **−146** · C4 156 / 35 / **−121** · H@C5 43 / 123 / **+79**
FF 는 O 와 카보닐 C2 를 거의 동일하게 봄. **가장 hard 이자 EHR 이 선호하는 위치 = C5 양성자**
(탈양성자화 시 공액 엔올레이트 생성). EHI 최강 soft = 카보닐 C(−146), O 도 거의 동일값.
lithium trimethylsilylacetylide 를 카보닐에 첨가 → 알코올 **96 % 수율**.
티올레이트 첨가는 보통 **C4**(EHI −121, 약간 덜 반응성인 soft 자리)에서 일어남.
C1(카보닐) 티올 첨가의 hemithioacetal 은 불안정 → **kinetic 중간체**, C4 생성물이 열역학 선호.
**(E)-pent-3-en-2-one lithium complex 17** — O 117 / −110 / **−226** · **Li 110 / 1.316 / 1.206** ·
C2 179 / −96 / **−275** · C4 148 / −50 / **−197** · C5 33 / −6 / −39 · H@C5 39 / −5 / −44
O 를 Li⁺ 가 배위. 두 지수 모두 **C2 를 soft 반응 자리**로 지지. FI 최저는 C5(그 다음 부착 양성자).
FI 기준 C4 가 두 번째 soft(**O 를 앞지름**), EHI 기준으로는 **C2 > O > C4** 순.
**EHI 는 Li 를 더 hard 한 반응 자리로 제시** → 추가 리간드 배위 가능성을 지지.
Gilman 쿠프레이트(R₂LiCu)의 1,4-선택성에서 **Li 가 Cu-결합 알킬에 배위**하는 그림과 정합.
> **⚠ 이 행은 두 가지 이유로 조심해서 읽어야 한다** (§10):
> (i) **단위 불일치** — Table 1 은 "10⁻³ e" 단위인데 Li 의 `1.316 / 1.206` 은 SI Table S26 의
> **e 단위 원값**(1.31592 / 1.20600 e) 이다. 10⁻³ e 로는 1316 / 1206 이어야 한다.
> (ii) **물리적 정체** — SI Table S26 의 Hirshfeld 전하 열은 `N`(=착이온, 총전하 +1) →
> `N+1`(중성 라디칼) → `N+2`(음이온)이고, **Li 전하가 +0.7046 → +0.5947 → −0.7212** 로 간다.
> 즉 **두 번째 넣은 전자가 사실상 통째로 Li 에 들어간다(Li⁺ + e⁻ → Li⁰)**. 확산함수 없는
> def2-QZVPP 로 음이온을 다루는 것은 알려진 위험(비결합 전자) — 이 EHI 는 "화학적 hard 자리"라기보다
> **금속 중심 환원**을 보고 있을 가능성이 크다. 우리가 Li 화학에 이 논문을 끌어 쓸 때 **가장 조심할 지점**.

## 7. Case studies (본문 3건)

### 7.1 Case 1 — 넓게 비편재된 계: benzo[a]pyrene 18 (Fig. 6)
PAH 는 성간화학부터 **반도체 재료**까지 걸치고, 석탄타르·담배연기·구운 고기에 편재하며
대개 발암성이다. 18 의 대사체가 DNA·RNA·단백질에 공유결합한다.
- **EHR: C7 이 soft, C6 가 hard.**
- **soft 경로(효소·O₂)**: monooxygenase 로 **C7/C8 에폭시화 → 19** → epoxide hydrolase/monooxygenase
  → **20**(diol epoxide, 가장 강력한 발암 대사체) → DNA 부가체 **21**.
  코발트 단편 (C₅Me₅)Co(I) 도 **C7–C10 π계에 배위**.
- **hard 경로(SET)**: **Pt 전극에서 1전자 산화 → 라디칼 양이온 18•⁺** (스핀밀도 **ρ_α = 0.26**)
  → RH 와 반응해 **22** → **23**. 전기화학적 산화·화학 산화제·광산화 관측과 정합.
- 저자 결론: **HSEH 로 PAH 의 (생)화학을 폭넓게 이해할 수 있다.**
> 🔑 **우리 관점의 핵심 문장**: *"전극에서의 1전자 이동(SET) = **hard 전자** 채널,
> 효소·O₂ 의 2전자 화학 = **soft 전자** 채널"* — 이 논문 전체에서 **전기화학과 가장 가까운 진술**이다.

### 7.2 Case 2 — 복잡 천연물 전합성: enfumafungin 24 → ibrexafungerp 26 (Fig. 7)
24 는 내생균이 만드는 트리테르페노이드, **20년 만에 승인된 첫 신규 계열 항진균제** 26 의 출발물질.
산 매개 환원(TFA, Et₃SiH, toluene)으로 **하이드록시 하나만 선택 제거** → 25 → 26.
24 는 O 를 **10개** 갖고 그중 **5개가 OH** 로 양성자를 두고 경쟁한다.
- 두 hemiketal 이성질체를 각각 계산해 지수를 **평균**.
- **C=C 이중결합이 이용 가능한 자리 중 가장 hard**(HOMO 가 거기 대부분 국재) → 1전자 산화는 이 위치가 지배.
  라디칼 양이온 **24•⁺ 스핀밀도 0.33(bridgehead) / 0.44(CH)**.
- **음의 EHI 들이 반응성 OH 기들을 지목**.
- 저자 태도가 정직하다: *"The HSEH principle is able to assist in such challenging retrosynthesis
  scenarios **but does not replace a specialist's judgment**."* — 지수는 **"가능한 반응 자리 목록"**
  을 주는 출발점이지 답이 아니라고 명시. 3차 카보양이온 안정화 같은 **하류 과정(downstream)** 을
  같이 고려해야 예측이 정련된다(첫 전하 도입 후엔 알켄이 hard 로 재배정됨).

### 7.3 Case 3 — 유기금속 (Fig. 8, Fig. 9)
**(a) potassium zincate 27** `(toluene)K(µ-N(SiMe₃)₂)₂ZnCH₂Ph`
diphenylmethane 과 반응 시 **아연에 결합한 톨릴 리간드가 양성자를 받아** 톨릴이 diphenylmethyl 로 치환(→29).
**EHR 의 hard 부분이 이 반응성을 정확히 재현.** soft 응답은 **hexamethyldisilazane 의 N 중심**을 가리키며
이는 금속 아미드가 아미드 염기로 작동하는 성질과 일치. → **더 soft 한 금속 중심이면 톨릴징크 단위를
유지한 채 disilazane 만 전달할 수 있을 것**이라는 예측을 내놓는다.
**⚠ 모델링**: *"A simplification of the structure **in the solid state** was utilized."*
고체상에서 벤질 리간드는 반복 단위의 K 에 **π-배위로 다리**를 놓는데, 이를 **K 에 π-배위한 단좌 톨루엔
리간드를 갖는 이금속 단량체**로 단순화했다. → **고체를 계산한 게 아니라 고체 구조를 잘라 분자로 만든 것.**

**(b) chloroimidazopyrazine 30** (Fig. 9)
금속염·조건에 따라 regioselectivity 가 넓게 갈리는 기질.
- **TMP₂Zn·2MgCl₂·2LiCl (hard acceptor)** → **C4 탈양성자화** — 모델의 **가장 hard 한 acceptor 자리**와 정합.
- **TMPMgCl·LiCl** → **C6 마그네슘화**(열역학적 탈양성자화 생성물). 이 자리는 *"only marginally softer"*.
- **RZnCl·MgCl·LiCl + [Pd] (soft donor)** → 교차 커플링으로 **염화물이 아릴로 치환** —
  30 의 **염화물과 결합 탄소의 soft donor 성**과 정합.
- **hard Li 양이온 배위** → 이후 Mg 중심 반응 → **C1 치환체 36**.
- **EHI 가 C9 를 30 의 가장 hard 한 친핵 자리로** 찾고, 3D 표현은 **질소 lone pair 가 아니라 π계를 통한
  배위**를 시사 → *"방향족 질소의 FMO 고려는 조심해서 다루라"*(pyridine 교훈 재확인).
🔑 **이 사례가 "reagent 의 경도를 바꿔 regioselectivity 를 스위치한다"는 HSEH 의 가장 실용적 시연.**

## 8. 결론 (저자 자신의 범위 선언)
- 홑전자와 전자쌍은 **다르게 행동**: 전자 하나는 **mesomeric donor/acceptor 를 가진 soft 자리**,
  전자쌍은 **hard 자리·mesomeric acceptor** 를 선호.
- 지수는 **직관으로도 추정 가능**하고, **저비용 계산**으로 얻을 수 있다.
- **적용 범위 명시**: *"With its foundations in the FMO of the starting materials, the model is best
  suited for describing **frontier orbital-dominated reactions with early transition states**.
  Cases with **non-FMO reactivity, leading to low responses or late transition states, should be
  treated carefully.**"*

## 9. Figure set ★
> **본 그림 / 안 본 그림 구분** — 크로핑 51장(본문 fig 9 + SI fig 8 + 표 34).
> **크로핑 PNG 로 직접 본 것 6장**: `Fig. 1`, `Fig. 3`, `Fig. 5`, `Fig. 6`, `Fig. 7`, `Fig. 8`, `Fig. 9`(7장).
> **PDF 페이지 렌더로 본 것**: `Fig. 2`, `Fig. 4`, `Fig. S1`~`Fig. S8`(전 페이지를 읽으며 봄, 저해상).
> **표(tab_*.png)는 이미지로 안 봄** — PDF 텍스트/SI 원문에서 직접 수치를 뽑았다(더 정확).
> 그림에서만 읽은 값은 `figure-read ≈` 로 표시.
> **★ 2026-08-06 추가로 본 것**: `Table 1`(tab_1.png) · `Table S7` · `Table S18` · `Table S19` · `Table S20`
> — 산술이 안 맞는 4개 행을 SI 원자 전수표와 대조하려고 **의도적으로 표 이미지를 봤다**(§14b).
> 이 경우엔 이미지가 유일한 대조 수단이었다(해당 SI 표의 텍스트 추출본이 이 세션에 없었음).

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | ambident 반응성 예측법 6종 비교 대장정(HSAB·Klopman–Salem·FMO·FF·kinetic-vs-thermo)과 각각의 실패 사유 → 본 논문 위치. 하단에 **phenolate 를 예로 EHR 을 "lone pair delta − radical delta"** 로 조립하는 도식 + **양=hard / 음=soft** 부호 규약 | **개념 슬라이드 원본으로 최적** — "왜 HSAB 만으로 부족한가"를 한 장으로 설명. 우리 리뷰 코멘트 첨부 자료로 쓸 수 있음 |
| 2 | 계산 흐름도: 기하 최적화 → N, N±1, N±2 단일점 → 밀도 뺄셈(Eq. 5) → 총밀도에 투영 / EHI 계산(Eq. 6) | **재현 레시피 그 자체.** 우리가 이식을 검토한다면 이 4단계가 이식 대상 |
| 3 | phenolate 로 네 밀도 비교: ρ_HOMO(Fukui) vs f⁻(Yang–Parr) vs f⁻²(본 논문) vs f^(2,−)(EHR) | **"HOMO ≠ Fukui ≠ EHR"** 을 눈으로 보여줌. 우리 PDOS(=HOMO 유사)로 반응 자리를 말할 때의 한계 경고 |
| 4 | 조사한 ambident 분자 17종 갤러리 (친핵체 1–8, 친전자체 9–17) | **적용 대상이 전부 유기 분자**임을 한 장으로 증명 — A5 판정의 시각 증거 |
| 5 | DMSO 1 · PMDTA 4 · pyridine 5(친핵) + diiminium adduct 13(친전자)의 f^± / f^{±2} / f^(2,±) 등고면(위)과 총밀도 투영(아래), 원자별 지수 표기 | 부호 규약 정박점. **pyridine 패널이 거의 균일한 초록 = π 상쇄 = "신호 없음"** 을 실제로 보여줌 (figure-read: pyridine EHI −4.4 / −4.0 / −3.7 / +1.0) |
| 6 | benzo[a]pyrene 18: EHR 투영(등고 ρ=0.004, 투영 ρ=0.02, ±1×10⁻³) + **soft 경로(효소 O₂ 에폭시화 → DNA 부가체)** vs **hard 경로(Pt 전극 SET → 18•⁺, ρ_α=0.26)** | **전기화학과 가장 가까운 그림.** "전극에서의 1전자 산화 = hard 채널" 프레이밍. figure-read EHI ≈ **+22 / +13 / −12 / −24** (×10⁻³ e) — SI Table S27 의 MAX +0.02162 / MIN −0.02371 과 일치 |
| 7 | enfumafungin 24 EHR(등고 0.004, 투영 0.02, ±1×10⁻³, 두 hemiacetal 평균, def2-TZVPP) + ibrexafungerp 26 합성 경로 | 거대 분자(원자 70+)에도 돌아간다는 스케일 증거. figure-read EHI ≈ **171 / 129 / −17 / −31 / −40 / −21 / −8** |
| 8 | potassium zincate 27 EHR(등고 0.005, 투영 0.01, ±1×10⁻³) + diphenylmethane 과의 반응(soft acceptor vs hard acceptor 분기) | **"고체 구조를 분자로 단순화"** 를 명시한 유일한 사례 — 무기 고체 미적용의 결정적 증거. figure-read EHI ≈ **+70 / +64 / +23 / −38 / −60** |
| 9 | chloroimidazopyrazine 30 을 **산으로 볼 때 f^(2,+)** 와 **염기로 볼 때 f^(2,−)** 두 패널(등고 0.002, 투영 0.01, ±5×10⁻⁴) + 시약 경도에 따라 갈리는 4갈래 경로 | **reagent 경도로 regioselectivity 를 스위치**하는 최선의 시연. figure-read: acid 패널 ≈ +23/+23/+22/+21/+12/−26/−42, base 패널 ≈ +27/+22/+14/−3/−14/−37/−42 |
| S1 | Fig. 2 와 동일한 흐름도(SI 튜토리얼판) | — |
| S2,S3 | `orca_plot` 대화형 메뉴 스크린샷 — density plot 선택, **grid 80×80×80**, Gaussian cube 출력 설정 | 이식 시 그대로 따라할 수 있는 조작 순서 |
| S4,S5,S6 | ChemCraft 에서 cube 뺄셈(`Multiple cubes operations`), EHR 등고면, 총밀도에 EHR 매핑 스크린샷 | 시각화 파이프라인(우리 VESTA/cube 관례와 대응) |
| S7 | EHI 계산용 스프레드시트 예시(=Data S1) | 축약지수 계산이 **엑셀 한 장**이라는 것 |
| S8 | chlorobutane 11 의 LUMO — C1·C4 의 **C–C σ-반결합** 성격 | **비-FMO(σ*) 반응에서 왜 실패하는지**의 물증 |
| Table 1 | 조사 분자 전체의 FI·f^{±2}·EHI (10⁻³ e). 앞=친핵 규약, 뒤=친전자 규약 | 이 논문의 유일한 수치 자산. **규약 전환·단위 불일치·복제행 주의**(§10) |
| Table S1 | 기저 의존(cyanide 3): 6-31G* 13 %, def2-SVP −1.1 %, def2-TZVP −2.6 % (vs def2-QZVPP) | 기저는 비교적 관대 |
| Table S2 | **범함수 의존(cyanide 3): HF +22 %, PBE +41 %, B3LYP +34 %** (vs DSD-BLYP) | **🔑 우리 PBE 캠페인에 직접 걸리는 숫자.** 부호는 불변, 크기는 4할 |
| Table S3 | 1전자 vs 2전자 이동 구조(14′, 16′) — 진폭은 크게 변하나 **EHI 순서 불변** | 기하 선택 규칙(중성 바닥상태에서 평가). 🔴 **표에 오류 4건** — Δ 열 3행(14′ O·16′ O 는 부호 반대, 16′ C2), 14′ C1/C3 의 `f⁺²=0.010`(참값 0.095), 16′ H@C5 행 열 혼합. **인용은 S23/S25/S32/S33 재계산으로** (§14c-B) |
| Table S4,S5 | Mulliken 전하판(DMSO 1, pyridine 5) | **pyridine 에서 Hirshfeld↔Mulliken 이 "가장 soft 원자"를 바꾼다** |
| Table S6 | CPCM(DMSO) 용매 효과 — 인쇄값 O +7.9 %, S +2.1 %, 약한 EHI 양성자는 >100 % | 용매 도입 시 **강한 자리만 신뢰**. 🔴 인쇄값이 Table S7 로 재현 안 됨 — 기체상 대비 실제는 **O +17 % / S +4 %** (§14c-C). 캡션 "Mulliken"·"last row" 도 오기 |
| Table S7–S33 | 27개 분자의 원자 전수 Hirshfeld 전하 + FI + f^{±2} + EHI, 번호 매긴 구조 그림 포함 | 재현·검증용 원자료. **단 원자번호는 파일 순번**(본문 IUPAC 번호와 대응표 없음) |

## 10. Post-processing ★
- **무엇**: (i) **Fukui function / Fukui index** (Yang–Parr), (ii) **dual descriptor** 의 재해석판인
  **EHR(실공간 장) / EHI(축약 스칼라)**, (iii) **Hirshfeld 전하 분할**(대조군 Mulliken),
  (iv) **밀도 cube 대수**(뺄셈 2회) + **총밀도 표면 매핑**, (v) 라디칼 양이온 **스핀밀도**(ρ_α 0.26, 0.33/0.44),
  (vi) **Hessian(진동해석)** 으로 극소점 확인, (vii) ZPE·자유에너지 보정(autodE).
  **NEB·Bader·COHP·DOS·ELF·BVSE·grand-potential 전부 없음.**
- **도구**: ORCA 5.0.4(`!SP DSD-BLYP D3BJ def2-QZVPP … TightSCF keepdens`, `Print[P_Hirshfeld]=1`) →
  `orca_plot JOB.gbw -i` 또는 입력 내 `%plots dim1/2/3 80, Format Gaussian_Cube, ElDens(...)` →
  **ChemCraft** 의 *Multiple cubes operations → Perform operation on two cubes(subtract)* 2회 →
  등고면 + 총밀도 투영. 축약지수는 **Excel(Data S1)**.
- **수치화·플롯·기록 방식**: 지수는 전부 **10⁻³ e**. 그림엔 **등고 isovalue** 와 **투영 색범위**를
  캡션에 명시(예 Fig. 9: contour ρ=0.002, projection ρ=0.01, range ±5×10⁻⁴).
  **색 규약: 빨강 = 양(hard), 파랑 = 음(soft)**; 투영 표면은 red→green→blue.
  화학적으로 등가인 핵은 **평균값**으로 보고(Table 1 각주).
- **재현성 지원**: SI 에 **단계별 튜토리얼 + Video S1 + 입력파일 전문 + 빈 계산 스프레드시트**,
  데이터셋은 **ioChem-BD**. — 이 부분은 모범적이다.

## 11. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

> ⚠ **먼저 못 박는다**: 이 논문엔 **σ·Ea·ESW·C_ij·band gap 이 하나도 없다.**
> 따라서 **우리 4축 물성표에 수치 행으로 들어갈 것이 0개**다. 아래는 **방법·개념 대조표**이며
> `comparison_vs_ours.md` 에도 **framework note** 형태로만 넣는다(수치 비교 금지).

| 항목 | Mulks 2024 | 우리 (comp1/modelc) | 대응 / 왜 다른가 |
|---|---|---|---|
| 계 | **고립 분자·이온**(기체상) | **주기 결정** Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆ (52원자급 셀) | ✗ **범주가 다름.** 경계조건·전하 처리·전자 국재화 물리가 전부 다름 |
| 코드 | ORCA 5.0.4 (가우시안 기저) | Quantum ESPRESSO (평면파·PAW) | ✗ 직접 이식 불가. cube 출력·시각화 관례만 공통 |
| 범함수 | **DSD-BLYP-D3BJ**(double hybrid) | **PBE** | ⚠ **논문 자기 시험에서 PBE 는 EHI 를 41 % 축소**(부호 보존). 우리가 EHI 를 재보려면 **순위만** 쓸 수 있음 — 우리 밴드갭 규율과 동형 |
| 전하 분할 | **Hirshfeld** | **Bader** | ⚠ 세 번째 분할 스킴. 논문 SI 가 이미 Hirshfeld↔Mulliken 에서 **가장 soft 원자가 바뀐 사례**(pyridine)를 보고 → Bader 이식은 **자체 검증 필수** |
| "어느 자리가 반응하나" | **f⁻(r)** = ρ_N − ρ_{N−1} (전자수 미분) | **site-resolved PDOS**(VBM 근처 어느 S 인가) + **ICOHP**(어느 결합) + **ELF** | ◐ **개념적으로 같은 질문, 다른 관측량.** 우리 PDOS 는 *고정 N* 의 오비탈 성분, FF 는 *N 변화*의 응답 — Fig. 3 이 바로 "HOMO ≠ Fukui" 를 보여준다 |
| "hard 자리" | **EHR/EHI**(2차 응답, 부호로 판정) | **대응물 없음** — 우리 파이프라인엔 2차 전자수 미분이 없다 | ✗ 이식하려면 **하전 슈퍼셀 N±1, N±2** 가 필요 → jellium 배경·Makov–Payne/FNV 유한크기 보정·polaron 국재화 문제. **공짜가 아님** |
| Li 화학 | 분자 **17** 의 Li⁺ 배위 1건. `f⁺²(Li)=1.316 e` = **두 번째 전자가 Li 에 통째로** | 우리 Li 는 **격자 이온**(BVSE·MLIP-MD·grand-potential 로 다룸) | ✗ **비교 금지.** 논문의 Li 수치는 분자 음이온 상태(확산함수 없는 기저)의 산물 — 우리 Li⁺ 수송/환원과 물리가 다름 |
| S 화학 | DMSO(S–O π)·SCN⁻ 2건, 전부 **분자** | 우리 축① = **자유 S²⁻ 3p 가 VBM 을 pin → 산화 onset 2.256 V** ([Banik] 외부 정답지) | ◐ 개념 평행선만. "S 가 soft base 라 산화가 쉽다"는 **HSAB 서사와 우리 PDOS/COHP 결과가 같은 방향**이지만, 이 논문은 그 계산을 **하지 않았다** |
| 가수분해(P–S 절단 → H₂S) | **다루지 않음.** 가장 가까운 것도 티올/알코올의 분자 첨가 | 우리도 **직접 계산한 적 없음**(과장 금지) — 관련 자산은 ESW·interface_reactivity·XPS anchor | ✗ **양쪽 다 빈칸.** 리뷰 §3.1 이 이 논문으로 가수분해를 설명한다고 쓰면 그건 **양쪽 문헌 어디에도 없는 다리** |
| 계면 산화/환원 | **Fig. 6 의 Pt 전극 SET 1건**(용액 중 분자) | grand-potential ESW(2e⁻ 단계, 닫힌 고체 hull) + PDOS/COHP | ◐ **프레이밍만 이식 가능**: "1전자(SET/전극) ≠ 2전자(화학) 는 다른 자리를 고른다". 우리 ESW 는 정의상 **2e⁻·열역학**이라 이 구분을 못 본다 |
| 무질서 | 없음(conformer 샘플링) | 4a/4c S/Cl 무질서 · disorder ensemble | ✗ 대응 없음 |
| 적용 조건 | **FMO 지배·early TS** 반응에 한정(저자 명시). late TS·σ* 는 실패 자인 | 우리 관심 반응(가수분해·계면 분해)은 **late TS + 표면 + 양성자 이동** | ⚠ **이게 결정적**: 우리가 원하는 반응들이 정확히 저자가 "안 된다"고 한 부류에 들어간다 |

### 11b. 그래서 우리 관측량(PDOS/ICOHP/ELF/Bader)에 대응되나? — 정직한 판정
- **f⁻(r) ↔ site-PDOS(VBM 근처)**: ◐ **부분 대응.** 둘 다 "첫 전자/홀이 어디서 나가나"를 본다.
  단 FF 는 **완화(relaxation) 포함**, PDOS 는 **비완화 오비탈 성분** — Fig. 3 이 그 차이를 그림으로 보여준다.
  우리가 "VBM = 자유 S²⁻ 3p 96–97 %" 라고 말할 때, 그것은 **f⁻ 가 아니라 ρ_HOMO 쪽**에 해당한다.
- **EHR/EHI ↔ 우리 것 중 무엇?**: **없다.** 우리 파이프라인에 2차 전자수 응답이 없다.
  가장 가까운 사고는 "1차 산화 산물이 2차 산화에서 어디로 가나"인데, 그건 우리가 **grand-potential
  계단(2.256 → 2.385 → 3.326 V)** 으로 이미 *열역학적으로* 보는 것이고, EHR 은 **반응물 전자구조만으로**
  같은 질문에 답하려는 시도다. **다른 접근, 같은 질문.**
- **ICOHP ↔ HSEH**: ✗ 대응 없음. ICOHP 는 결합의 공유성/세기(고정 N), EHI 는 원자의 응답성.
  다만 리뷰 A3(분극률 vs 극성) 논점에서 **"분극률 = 전자구름의 응답성"** 이라는 어휘가
  EHR 의 언어와 같은 계열이라는 점은 지적할 만하다.
- **Bader ↔ Hirshfeld**: ✗ 직접 대체 불가. 논문 SI 가 분할 스킴 민감성을 이미 보였다.

## 12. 적용 인사이트 (우리 연구에 어떻게)
1. **리뷰어 코멘트 A5 를 "정밀 지적"으로 격상.** 삭제 요구가 아니라
   **(a) 저자 표기 정정(Mulks, 단독)**, **(b) "무기 고체 적용 선례 없음" 명시 요구**,
   **(c) "이 리뷰에서 HSEH 가 무엇을 새로 설명하는가" 한 문장 요구** — 세 갈래로 쓴다.
   근거는 이 digest §1.5 (전수 점검표 + 저자 자신의 적용범위 선언).
2. **"1전자 ≠ 2전자" 프레이밍은 우리 산화 서사에 실제로 쓸 수 있다.**
   우리 축① 는 grand-potential(=2e⁻·열역학) 로 onset 2.256 V(S²⁻-limited)를 준다.
   그런데 실제 계면에서 첫 사건은 **1전자 이동(홀 주입)** 이다. Mulks 의 Fig. 6 이
   "SET(hard) vs 2전자 화학(soft)이 다른 자리를 고른다"는 것을 분자에서 보였다면,
   우리는 **"첫 홀이 앉는 자리(site-PDOS/⟨3p⟩ centroid) ≠ 열역학 분해가 지목하는 상"**
   이라는 이미 가진 관찰을 같은 언어로 말할 수 있다. **단 인용은 "개념 유비"로만.**
3. **범함수·전하분할 민감성 표를 우리 규율의 외부 판례로 재사용.**
   Table S2 의 **PBE +41 %(부호 불변)** 는 [Spencer22] 의 밴드갭 판례와 나란히 놓을 수 있는
   "전자구조 기술자는 순위·부호만 인용" 근거다. 우리 `comparison_vs_ours.md` §D 방법론 주석에 추가.
4. **이식을 검토한다면 비용 견적부터**: EHR/EHI 를 우리 셀에 얹으려면 (i) 하전 슈퍼셀 N±1/N±2,
   (ii) 유한크기 보정, (iii) polaron 국재화 통제, (iv) Bader 기반 축약지수 자체검증 — **네 겹의 신규 작업**.
   현 캠페인 우선순위에서 **투자 대비 회수 낮음**으로 판단. 개념 인용에 그치는 것을 권한다.
5. **가수분해에 이 틀을 쓰겠다는 서사는 (우리도) 쓰지 않는다.** 저자가 late TS·비-FMO 를
   명시적으로 제외했고, 우리도 가수분해를 계산한 적이 없다. **양쪽 빈칸을 유비로 메우지 않는다.**

## 13. 인용 가능 문장 (deck/원고/리뷰 회신용)
- "Mulks (Chem 2024) defines the electronic hardness response/index (EHR/EHI) as a second finite
  difference of the electron density (or of atomic charges) with respect to electron number,
  evaluated at fixed geometry from three single-point calculations; positive values mark
  lone-pair-like ('hard') sites and negative values radical-like ('soft') sites."
- "The framework is demonstrated exclusively on discrete molecules and organometallic complexes in
  the gas phase; **no periodic-solid, surface, or sulfide-electrolyte application is reported**."
- "The author states that quantitative structure–selectivity relationships **remain to be
  established**, and that the model is best suited to frontier-orbital-dominated reactions with
  early transition states."
- (우리 규율용) "In the paper's own benchmark, replacing the double-hybrid reference by PBE changes
  the condensed index magnitude by ~41 % while preserving its sign — a reminder that electronic
  descriptors from semi-local DFT support rankings, not absolute values."

## 14. 주의/한계 (over-claim 방지 + 논문 자체의 흠)

**우리 쪽 규율**
- 이 논문의 어떤 수치도 **우리 db 절대값과 같은 표에 넣지 않는다.** 물리량 종류가 다르다.
- "HSEH 로 황화물 가수분해를 설명할 수 있다"는 문장을 **우리가 먼저 쓰지 않는다.** 근거가 없다.
- 우리 밴드갭·BVSE·MLIP 규율 그대로. 이 논문은 그 축들에 **아무 입력도 주지 않는다.**

**논문 자체의 약점 (리뷰어 시각)**
1. **정량 검증 부재** — 상관 플롯·회귀·오차지표·hold-out 예측이 **0건**. 전부 사후 합리화이고,
   실험과 안 맞는 사례(pyridine, chlorobutane 11, oxaisoindolium 12 의 late-TS 자리)는
   *"further investigation is needed"* 로 처리된다. **예측력 주장은 아직 검증되지 않았다.**
2. **선택 편향 가능성** — 30여 사례가 "HSEH 가 잘 맞는 사례"로 뽑혔는지 통제할 방법이 없다.
   실패 사례를 숨기지 않은 점은 정직하나, **분모(시도한 전체 사례 수)** 가 제시되지 않는다.
3. **해상도 자기모순** — pyridine 에서 "10⁻³ e 차이는 무의미"라고 해놓고,
   Table 1 은 여러 분자에서 **±1~±10 ×10⁻³ e** 수준 차이로 순위를 논한다(예 9: +15 vs −29,
   12: −1 vs +38 vs −36). 어디까지가 신호인지 **정량 기준이 없다.**
4. **Table 1 복제 오류** — 분자 **4(PMDTA)** 의 `C4 | 43 | 47 | −3.7` 행은
   분자 **5(pyridine)** 의 C4 행과 **완전히 동일**하고, SI Table S10(PMDTA 원자 전수)에
   그런 값을 갖는 원자가 **없다**. 표 복제 오류로 보인다.
5. **Table 1 단위 불일치** — 표 제목은 "in 10⁻³ e" 인데 분자 **17** 의 Li 행 `1.316 / 1.206` 은
   SI Table S26 의 **e 단위 원값**(1.31592 / 1.20600 e). 같은 행 안에서 `110`(=10⁻³ e)과 섞였다.
6. **Fig. 5 캡션 오기** — 캡션은 *"Diiminium pyridine adduct **15**"* 라 쓰지만
   패널 라벨과 Table 1 은 **13** 이고, 15 는 methyl 3-oxobutanoate 다.
   또 캡션은 *"The given numbers are electronic hardness indices"* 라 하지만
   `f⁻`·`f⁻²` 열 아래 숫자는 EHI 가 아니라 **FI·f^{±2}** 이다.
7. **SI 원자번호 ↔ 본문 위치번호 대응표 없음** — SI Tables S7–S33 은 **파일 원자 순번**을 쓰고
   본문은 **IUPAC 위치번호**(C6, C7, C10b …)를 쓴다. 번호 매긴 구조 그림이 있긴 하나,
   benzo[a]pyrene 처럼 큰 계에서는 독자가 본문 주장(예 "soft at C7, hard at C6")을
   SI 수치로 **검증하기 어렵다**. (figure-read 로 확인한 것은 Fig. 6 의 4개 라벨 +22/+13/−12/−24 가
   Table S27 의 최대/최소값과 일치한다는 사실까지다.)
8. **분자 17 의 Li EHI 는 화학적 해석 이전에 방법론 문제** — N+2 상태가 확산함수 없는
   def2-QZVPP 음이온이고, 전자가 사실상 Li 로 들어간다(§6.2). 이 값을 "Li 가 hard 반응 자리"
   근거로 쓰는 것은 **약하다**.
9. **용매 없음** — 논의된 반응(알킬화·니트로화·그리냐르·Michael 첨가)은 전부 용액상인데
   지수는 기체상 값이다. 저자가 한계를 밝히고 CPCM 감도만 1건 제시.
10. **범함수 의존 41 %** (Table S2) — 부호는 살아남지만, "값이 크면 선택성 차이가 크다"는
    저자의 반정량 주장은 **범함수 선택에 그만큼 흔들린다.**
11. **저자 1인 + 저널 자문위원** — 단독 저술이고 저자가 *Chem* 의 Next-Generation Advisory Board
    소속임을 스스로 공시. 사실 자체는 문제가 아니나, **독립 재현·외부 검증이 아직 없다**는 점과 함께 읽을 것.
12. **파일 중복 안내** — 업로드된 SI-3(82 pp)는 **본문(22 pp) + SI-2(60 pp)를 이어붙인 파일**로
    고유 내용이 없다. 그림 추출 시 SI-3 를 넣으면 S 번호가 오염된다(본문 Fig. 1 이 Fig. S1 로 잡힘) —
    **본문 + SI-2 만으로 추출**했다.

### 14b. ★ 2차 검증 (2026-08-06) — Table 1 산술 전수 대조로 새로 찾은 것

> **방법**: Table 1 의 80개 행 전부에 대해 `EHI == f^{±2} − f^±`(친전자) / `f^± − f^{±2}`(친핵)를
> 스크립트로 검산하고, 어긋난 행만 **SI 원자 전수표(Tables S7/S18/S19/S20)의 크로핑 PNG** 로 대조했다.
> 결과: **어긋난 4행이 모두 본문 Table 1 의 오타로 확정**됐다(SI 값이 정답, EHI 열은 SI 와 일치).

13. 🔴 **Table 1 의 `f^{±2}` 열 오타 3건 + EHI 부호 오타 1건** — SI 대조로 확정:

| 분자 | 원자 | Table 1 (본문) | **SI 정답** | SI 출처 |
|---|---|---|---|---|
| **1** DMSO | H@C1/C2 | 43 / **63** / −10 | 43 / **53** / −10 | Table S7 `Avg Hs` 행 (0.04280 / 0.05273 / −0.00994) |
| **9** | (E)-H@C1 | 87 / **192** / +18 | 87 / **105** / +18 | Table S18 원자 6 (0.08672 / 0.10510 / 0.01838) |
| **10** | C1 | 56 / **43** / −2 | 56 / **54** / −2 | Table S19 원자 4 (0.05591 / 0.05382 / −0.00209) |
| **11** | C2 | 30 / 27 / **+3** | 30 / 27 / **−3** | Table S20 원자 3 (0.02997 / 0.02670 / **−0.00327**) |

   - 앞의 3건은 **중간 열만 틀렸고 EHI 는 맞다** → soft/hard 배정에는 영향 없음.
   - **네 번째(11 C2)는 부호가 뒤집혀 있다** — 표만 보면 C2 가 hard 로 읽히지만 SI 값은 soft 다.
     다행히 본문에서 C2 를 언급하는 문장은 EHI 가 아니라 **FF** 기준이라(*"The FF … suggests C2 as
     the hardest site"*) **본문 주장은 무너지지 않는다.** 하지만 표를 그대로 인용하면 틀린다.
   - ⚠ **인용 규율**: 이 논문의 수치를 쓸 때는 **Table 1 이 아니라 SI Tables S7–S33 을 1차 출처로** 삼는다.

14. 🔴 **Table 1 이어짐(p.2732)의 열 머리글이 틀렸다.** 인쇄된 머리글은 `f⁻ / f⁻² / f^(2,−)`(친핵체 규약)인데,
    거기 실린 **분자 12–17 의 26개 행 전부**가 실제로는 **친전자체 규약 `f^(2,+) = f^{+2} − f⁺`** 를 따른다
    (검산: 친전자체 규약 **26/26 일치**, 머리글 규약 **26/26 불일치**).
    예 — **14** 아세톤 O: `245 / −123` 이면 머리글대로는 **+368** 이어야 하는데 표는 **−369**.
    Fig. 5 의 **13** 패널이 `f⁺(r) / f^{+2}(r) / f^(2,+)(r)` 로 라벨된 것이 방증.
    → §6 의 "뒤 블록은 친전자체 규약" 안내는 **논문이 인쇄한 머리글과 반대**임을 알고 읽어야 한다.

15. ⚠ **본문 자기참조 문장 1건** (Fig. 9 논의):
    *"Note that magnesiation occurred at **C6** with TMPMgCl·LiCl, which is the thermodynamic
    deprotonation product. This site is only marginally softer than **C6**."*
    — **C6 를 C6 와 비교**한다. 문맥상 뒤쪽은 (hard acceptor 로 탈양성자화되는) **C4** 여야 한다.
    편집 단계 오기로 보이나, "두 자리의 경도 차가 근소하다"는 이 문장이 **시약 스위칭 서사의 핵심 근거**라
    그냥 넘길 수 없다.

16. ✅ **§14-7(SI↔본문 번호 대응표 없음)을 일부 해소** — 검증 과정에서 확인한 대응:
    **분자 10·11 은 본문 IUPAC 번호가 SI 파일 원자 순번과 정확히 역순**이다
    (예 **11**: 본문 C1 = SI 원자 4 = C–Cl 탄소, 본문 C4 = SI 원자 1 = 말단 메틸).
    **9** 는 본문 C1/C3 = SI 원자 1/3 로 순서가 같다. **1**(DMSO)의 `H@C1/C2` 는 개별 원자가 아니라
    SI 의 **`Avg Hs`(양성자 6개 평균)** 행이다 — Table 1 각주의 "화학적 등가 핵은 평균"이 여기 해당한다.

> 🛠 **운영 노트 (재현 시 반드시)**: 이 PDF 는 **마이너스 기호를 `\x02` 글리프**로 넣어 두었다.
> PyMuPDF `get_text()` 등 평문 추출을 그대로 쓰면 **표의 음수 부호가 전부 사라져** `−100` 이 `100` 으로
> 읽힌다(= soft/hard 배정이 통째로 뒤집힘). 추출 후 **`.replace('\x02','−')`** 를 반드시 적용할 것.
> `litdb/inbox/_53_text.txt` 는 이 치환을 적용해 다시 만들어 뒀다.

### 14c. ★ 3차 검증 (2026-08-06) — SI 실물(SI-3 82 pp) 독립 재검증

> **계기**: 사용자가 `53. Sup3) …pdf` 를 재투입(사용자 분류 폴더 `DFT`). §14-12 의 "중복 파일" 판정을
> 실물로 확정하고, 그 김에 **SI 표 전체를 기계 검산**했다.
> **방법**: `.replace('\x02','−')` 적용 후 pp.1–22 를 기존 `_53_text.txt` 와 정규화 대조;
> Tables S1–S6 의 rel 열과 Table S3 의 Δ 열을 SI 원표(S7–S33)로 전수 재계산;
> 열 정렬은 `tab_S3/S6/S25.png` **크로핑 이미지로 직접 확인**(평문 추출 열 어긋남 배제).

**A. 파일 판정 — §14-12 확정, 단 지금은 SI 의 유일한 로컬 사본**
- pp.**1–22** = 본문. 공백 정규화 후 기존 `_53_text.txt` 와 **문자 단위 완전 일치**(양쪽 77,331자).
- pp.**23–82** = SI(내부 쪽번호 1–59 + 표지). 22 + 60 = 82 ✓. **고유 내용 0건.**
- ⚠ 그러나 원래 업로드분(본문 PDF·SI-2 PDF)은 로컬에서 사라졌고 **SI 실물은 지금 이 파일뿐**이다.
  → SI 평문을 `litdb/inbox/_53si3_text.txt` 로 보존(부호 치환 적용). 그림은 이미 51장 추출돼 있어 재추출 불필요.
  ⚠ `litdb/inbox/` 는 .gitignore 대상이라 **이 텍스트도 로컬 전용**이다(`_53_text.txt` 와 동일 관례) —
  repo 로 넘어오는 SI 근거는 `litdb/figures/<slug>/tab_S*.png` 34장과 이 digest 본문뿐이다.
  → 재추출 사고 방지로 `litdb/pdf_map.tsv` 에 가드 1줄 추가(§아래 D-도구 노트).

**B. Table S3(1e vs 2e 이동) — 오류 4건. 결론은 살지만 표는 틀렸다**
Δ 열의 규약은 **Δ = f^(2,+)(중성 기하) − f^(2,+)(라디칼음이온 기하)** 이다 — 7개 행 중 **4행이 이 규약을
소수 3자리까지 정확히** 만족(14′ C1/C3 · 14′ C2 · 16′ C1 · 16′ C4)하므로 규약은 확정이다. 나머지가 깨진다:

| 행 | 인쇄 Δ | SI 원표 재계산 | 판정 |
|---|---|---|---|
| **14′ O** | **+0.030** | **−0.123** (S23 −0.36863 / S32 −0.24563) | 부호 반대 |
| **16′ O** | **+0.099** | **−0.089** (S25 −0.14576 / S33 −0.05634) | 부호 반대 |
| **16′ C2** | **−0.089** | **−0.075** (S25 −0.14607 / S33 −0.07059) | 위 O 행 참값이 내려옴 |

추가로 **행 자체가 모순인 칸 2개** (항등식 `f^(2,+) = f^{+2} − f^{+}` 위반, 나머지 7행은 전부 만족):
- **14′ C1/C3 의 `f^{+2} = 0.010`** → S32 참값 **0.095**(0.09459/0.09452 평균). 같은 행의 f⁺·f^(2,+) 는 맞다.
- **16′ H@C5 행은 열이 섞였다** — f⁺ 0.044 / f⁺² 0.089 는 메틸 3-H **평균**인데,
  f^(2,+) 로 인쇄된 **−0.003 은 S33 13H 단일 원자값**이다. 평균 규약대로면 **+0.048**.

**🔑 그래서 SI 의 "the order … does not change" 주장은?**
- **인쇄된 표만 읽으면 깨진다**: 16′ 에서 H@C5 가 hard(+79)→soft(−3)로 부호 반전 → C1(+1)과 순서가 뒤바뀐다.
  하필 본문이 **16 에서 미는 논거가 정확히 "가장 hard 한 자리 = C5 양성자 → 탈양성자화 → 공액 엔올레이트"** 다.
- **정정값(+0.048)을 쓰면 순서가 그대로다**: C2(−71) < O(−56) < C4(−37) < C1(+1) < H@C5(+48),
  중성 C2(−146) ≈ O(−146) < C4(−121) < C1(+42) < H@C5(+79) 와 동일 순서.
- → **저자 결론은 유지된다. 틀린 것은 표다.** 이 절을 인용할 땐 **Table S3 이 아니라
  Tables S23/S25/S32/S33 에서 직접 계산**한다. (§14b-13 의 Table 1 오타 4건과 **같은 종류의 흠이 SI 에도 있다**.)

**C. Table S6(용매) — rel 열이 Table S7 로 재현되지 않는다. 실제 용매 민감도는 서술의 약 2배**

| 원자 | 기체상 f^(2,−) (S7) | CPCM f^(2,−) (S6) | 재계산 상대차 | **인쇄·본문값** |
|---|---|---|---|---|
| O | +0.19888 | +0.23281 | **+17.1 %** (기체 분모) / +14.6 % (CPCM 분모) | **+8 %** |
| S | −0.09984 | −0.10405 | **+4.2 %** / +4.0 % | **+2 %** |

- 대조군으로 **Tables S1·S2 의 rel 열은 규약 `Δ = ref − X, rel = Δ/ref` 로 5행 전부 소수 6자리까지 재현**된다
  (6-31G\* 0.132162 vs 인쇄 0.132161 등). 즉 **S6 만 다른 기준**을 썼고, 그 기준 run 은 SI 에 없다
  (CPCM 재최적화 기하에서의 무-CPCM 단일점일 가능성 — 그렇다면 오류는 아니나 **미공개**).
- **📌 우리 인용 규율 (§4b 표 수정)**: "O +7.9 %, S +2.1 %" 는 **논문 인쇄값**이라고 명시하고,
  *유일하게 표로 공개된 기체상 값(Table S7) 대비로는 **O +17 % / S +4 %*** 라고 병기한다.
  정성 결론(강한 자리는 견고 · EHI 6×10⁻³ e 수준 양성자는 100 % 넘게 흔들림)은 그대로 유효하다.

**D. 라벨·번호 오류 (신규 6건)**
1. **Table S4** — 캡션 "Atomic **Mulliken** charges … DMSO 1" ↔ 표 안 머리글 "**Hirshfeld** charges (e)".
   데이터는 Mulliken 이 맞다(O −0.61896 ≠ Table S7 Hirshfeld O −0.42946) → **머리글이 오기**.
2. **Table S6** — 캡션 "Atomic **Mulliken** charges" ↔ 머리글 "**Hirshfeld** charges (e)" → 이번엔 **캡션이 오기**
   (연구 표준·본문 서술 모두 Hirshfeld). 게다가 캡션 *"The last **row** gives the relative difference"*
   → 실제로는 마지막 **열**이다.
3. **Table S30** — 캡션 *"…reactivity indices of **enfumafungine 27** (toluene)K(−N(SiMe₃)₂)₂ZnCH₂Ph 27"*.
   유기금속 표에 "enfumafungine" 이 복붙됐다.
4. **같은 분자에 번호가 셋** — 본문 Fig. 7 캡션 "enfumafungin **24**" / SI 목차 "Enfumafungine **25**" /
   SI Tables S28·S29 캡션 "enfumafungine **23**". (zincate **27** · chloroimidazopyrazine **30** 은 본문↔SI 일치.)
   → §14-7 의 "번호 대응표 부재"는 원자번호뿐 아니라 **분자번호에도** 해당한다.
5. **SI 본문 오기 2건** — p.S16 *"no selection of the nitrogen in **2** can be observed with the Mulliken charge"*:
   논의 대상은 **pyridine 5** 다(**2** 는 thiocyanate). p.S18 *"conclusions drawn from **HSER** considerations"*:
   EHR/HSEH 오기.
6. **SI 목차 첫 줄에 Word 필드 오류가 그대로 인쇄** — *"Hard and Soft Electrons and Holes … **Error! Bookmark
   not defined.**"* (§2 "편집도구 Word 명시"와 함께 읽으면 교정 공정이 얕았다는 정황.)

**E. ✅ 확증된 것 (반증 아님)**
- **§4b 의 방법 의존성 수치는 전부 실물과 일치** — 기저 13.2 %(6-31G\*), 범함수 **PBE 41.2 % · HF 21.7 % ·
  B3LYP 33.8 %**, 그리고 **부호는 4개 범함수 모두 불변**(C 음/soft, N 양/hard). 우리가 이 논문을 쓰는
  **가장 중요한 이유(= "semi-local DFT 전자기술자는 순위·부호만" 판례)는 그대로 선다.**
- **Table S5 Mulliken↔Hirshfeld 배정 반전(pyridine N→C2)** 실물 확인 — Mulliken f^(2,−): C2 −0.02386 < N −0.01045.
- **분자 17 의 Li `f^{+2}=1.31592` / `f^{(2,+)}=1.20600` e** 실물 확인, Li 전하 **+0.7046 → +0.5947 → −0.7212**
  (§6.2·§14-8 의 "두 번째 전자가 통째로 Li 로" 판정 유지).
- **Table 1 각주의 "등가 핵 평균" 규약이 H 행 전반에 적용됨을 수치로 확증**(§14b-16 의 DMSO 사례 확장):
  acetone **14** `H@C1/3` 68/172/**+103** = S23 의 H 6개 산술평균 0.06833/0.17181/**+0.10348**;
  pentenone **16** `H@C5` 43/123/**+79** = S25 의 **H7·H8·H9**(tab_S25.png 구조 그림으로 원자 배정 확인)
  평균 0.04332/0.12281/**+0.07949**. → **Table 1 의 H 행을 SI 로 검증할 땐 반드시 평균을 취한다.**

**🛠 도구 노트 — 파싱 함정 2개 (자동 전사 시)**
- **2차 Fukui 열 머리글이 두 표기로 섞여 있다**: `f⁻²/f⁺²` = S1,S2,S4,S6,S7–S12,S16,S18,S21–S26,S33 /
  `f⁻⁻/f⁺⁺` = S5,S13,S14,S15,S17,S19,S20,S27–S32.
- **S3·S19·S20 은 "Hirshfeld charges (e) / Indices" 머리 블록 자체가 없다** → 열 폭이 달라진다.

### 14d. 4차 — SI-2 재투입 (2026-08-06): **중복 확정, 신규 내용 0건**

> **계기**: 사용자가 `litdb/inbox/53. Sup2) Hard and soft electrons and holes.pdf`(60 pp)를
> "논문 에이전트로 처리" 요청(사용자 분류 폴더 `DFT`). **새 논문이 아니라 이 digest 의 SI 다.**

- **판정: 중복.** 60쪽 전부를 기존 `_53si3_text.txt`(SI-3 에서 뜬 SI 60쪽)와 공백 정규화 후 대조 →
  **60/60쪽 문자 단위 완전 일치, 차이 0쪽**. 고유 내용 없음 → digest 본문 수정 사항 없음.
- **이미 반영돼 있었다**: `figures/mulks2024_hard_soft_electrons_holes/figures.json` 의 `sources` 에
  `c247bf09-53._Sup2_…pdf` 가 있고, 크로핑 **51장 중 41장**(`fig_S1`–`S8` + `tab_S1`–`S33`)이
  **바로 이 파일에서 잘린 것**이다. 즉 1차 digest 때 쓴 SI 원본이 이름만 바꿔 다시 들어온 것.
- **달라진 것 하나** — §14c-A 는 "SI 실물은 SI-3(82 pp) 뿐"이라고 적었으나, 이제
  **본문 오염이 없는 깨끗한 SI 단독본(SI-2, 60 pp)이 로컬에 있다.** 재추출이 필요해지면
  SI-3 가 아니라 **이 파일**을 쓴다(§14-12 의 S 번호 오염 문제가 원천적으로 없음).
- **🔴 재추출 주의** — 지금 `inbox/` 에는 **SI-2 만 있고 본문 PDF 는 없다.**
  이 상태로 `extract_figures.py --slug mulks2024_hard_soft_electrons_holes --clean` 을 돌리면
  본문 크롭 10장(`fig_1`–`9`, `tab_1`)이 **지워지고 SI 41장만 남는다.** 본문 PDF 를 같이 넣거나
  `--clean` 없이 돌릴 것. (`--inbox --skip-done` 은 이미 done 으로 걸러지므로 안전 — 실측 확인.)

## 15. 기법 용어 미니사전
- **HSAB (Hard-Soft Acid-Base)**: Pearson(1963). 작고 전하밀도 높고 잘 안 분극되는 파트너(hard)끼리,
  크고 분극 잘 되는 파트너(soft)끼리 잘 결합한다는 경험칙. **종 단위 전역 분류**라 자리 분해가 안 됨.
- **ambident (양쪽성) 반응체**: 한 분자 안에 반응 가능한 자리가 둘 이상이라 regioselectivity 가
  조건에 따라 갈리는 화합물(예 SCN⁻: S 냐 N 이냐, phenolate: O 냐 C 냐).
- **regioselectivity**: 어느 자리에서 반응이 일어나는가.
- **FMO (Frontier Molecular Orbital)**: 반응성이 HOMO/LUMO 로 결정된다는 단순화(Fukui).
- **Fukui function f^±(r)**: 전자수 N 에 대한 전자밀도의 1차 도함수(유한차분). "가장 무른 자리" 표지.
- **Fukui index (FI)**: FF 를 원자별 전하 차이로 축약한 스칼라. 합 = 1 로 정규화.
- **dual descriptor f^(2)(r) = f⁺ − f⁻**: 친전자/친핵 영역을 동시에 판정. ≈ 밀도의 2차 전자수 미분(hyper-hardness).
- **EHR (electronic hardness response)**: 이 논문의 실공간 장. `f^(2,±)(r)`. **양 = hard, 음 = soft**.
- **EHI (electronic hardness index)**: EHR 의 원자별 축약 스칼라. 합 = 0.
- **orbital relaxation (오비탈 완화)**: 전하를 바꾸면 남은 전자들이 재배치되는 효과.
  FF 가 ρ_HOMO 와 다른 이유이자 EHR 신호의 기원.
- **SOMO / captodative**: 홑점유 분자 오비탈 / donor·acceptor 치환기가 **동시에** 라디칼을 안정화하는 효과.
- **SET (single-electron transfer)**: 1전자 이동. 이 논문에선 Pt 전극 산화 = **hard 채널**로 분류.
- **Hirshfeld charge**: 전자밀도를 자유원자 밀도 비율(stockholder)로 나눠 얻는 원자전하.
  Mulliken 보다 기저 의존이 작아 이 논문의 표준.
- **PBEh-3c / DSD-BLYP-D3BJ**: 각각 저비용 복합 hybrid 기하 최적화 방법 /
  spin-component-scaled double-hybrid(MP2 상관 혼합) 단일점 방법. D3BJ = Grimme 분산 보정(Becke–Johnson 감쇠).
- **RIJCOSX**: Coulomb 은 RI-J 근사, HF 교환은 chain-of-spheres(COSX) 수치적분으로 가속.
- **autodE / xTB(GFN2) / ETKDGv3**: 반응경로 자동화 파이프라인 / 반경험적 tight-binding /
  RDKit 의 거리기하 기반 conformer 생성 알고리즘.
- **CPCM**: conductor-like polarizable continuum model — 연속체 용매 모델.

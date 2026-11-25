<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md.
     2026-09-27 초판 · 1저자 요청 "새로 들어온 논문들인데 dft 위주로 논문 에이전트 해줘".
     ① 본문 37 pp + SI 11 pp 전문을 PyMuPDF 텍스트로 전수 판독 (이 기계엔 pdftoppm 이 없어 Read 의 PDF 렌더가 안 된다).
     ② 그림 크롭 18장 + 표 3장 = 21장 중 **8장을 실제로 봤다** (아래 목록). 도구가 놓친 4장(Fig. 12·13·15·17)은 손으로 잘라
        figures.json 에 `manual_crop` 사유와 함께 넣었다 — 그중 13·15 가 이 리뷰의 ML 그림 핵심이다.
     ③ "✎" = 논문이 말하지 않은 것을 우리가 판단·유도한 것. "figure-read ≈" = 그림에서만 읽은 값. -->

# Accelerating Electrolyte Discovery for Sodium-Ion Battery Through Property-Based Frameworks and Artificial Intelligence — Gao et al. (*Electrochem. Energy Rev.* **9**, 23 (2026))

> slug `gao2026_sib_electrolyte_ai_review` · DOI `10.1007/s41918-026-00296-x` · type `리뷰 (자체 계산 0 · 자체 실험 0 — 전량 2차 인용 · Na-ion 전해질 개관 + AI 절 ≈4 pp)` · PDF `litdb/inbox/0927-2. ElectrochemEnergyRev_2026_Gao_SIB_electrolyte_property_framework_AI_review_MAIN.pdf` (37 pp = 본문 ≈27 pp + 참고문헌 232개 ≈10 pp · sha256 `b09ecd2935cbbc67…`) + `litdb/inbox/0927-2. Sup) ElectrochemEnergyRev_2026_Gao_SIB_electrolyte_AI_review_SI.pdf` (11 pp · **`Table S1` 하나뿐** · sha256 `a4444c8ffa0bf602…`) · digested `2026-09-27` · status ✅ · 태그 **[외부 · Na 계 · 리뷰]**

> elements: Na, Zr, Si, P, O, Al, S
> methods: DFT, AIMD, MD, MLIP, BVSE, phonon, ESW

> **저자**: **Li Ting Gao**¹² · Hossein Mashhadimoslem¹ · Yi He¹ · Weinan Zhao¹ · Qiran Lu¹ · **Sushanta K. Mitra\***³⁴ · **Zhan-Sheng Guo\***² · **Aiping Yu\***¹
> (¹ Univ. Waterloo 화공·WIN · ² 上海大学 SIAMM 역학공학 · ³ Waterloo 기계(Micro & Nano-Scale Transport Lab) · ⁴ Chulalongkorn Univ. ISE)
> 접수 2026-03-23 · 수정 2026-05-19 · 수락 2026-07-23 · © Shanghai University & Periodicals Agency · NSFC 12172206(Gao)·12572202(Guo) + CSC
> ⚠ **사사에 명시**: *"use of OpenAI's ChatGPT to assist with optimizing figures and to provide minor language editing, paraphrasing, and proofreading"* (p.28).
> 🎤 **관련 발표: 없음** — `talks/*.md` 인입 대기열(유일한 대기열 = `talks/lee2026_skku_mlip_materials_design.md` §99-10)에 이 논문은 없다 (2026-09-27 확인).

> **본 digest 에서 실제로 본 그림 (2026-09-27)**: `Fig. 2` `Fig. 3`(+ 레이더 부분 600 dpi 확대) `Fig. 10` `Fig. 13` `Fig. 14` `Fig. 15` `Fig. 16` `Fig. 18` — **8장**.
> 안 본 것: `Fig. 1`(탄소배출) · `Fig. 4`(GPE 제조) · `Fig. 5`(SPE 수송 모식) · `Fig. 6`(NASICON UHS 소결) · `Fig. 7`(β/β″-alumina 구조) · `Fig. 8`(NASICON 연표) · `Fig. 9`(양극 균열 STEM·MRI) · `Fig. 11`(SEI NMR) · `Fig. 12`(PRC 막) · `Fig. 17`(비용·LCA·ELET) — **10장, 전부 실험·개관 그림이라 DFT 요청 축에서 뺐다**. 표 `Table 1` `Table 2` `Table S1` 은 이미지로 안 보고 **PDF 텍스트로 전사**했다.
> **본문 서술과 어긋난 그림: 5장** (`Fig. 3` · `Fig. 13a` · `Fig. 13b` · `Fig. 15a` · `Fig. 15b`) **+ 부분 1장** (`Fig. 14` — 본문의 t/η 를 t 단독으로 축약) — §5·§10. 미독 `Fig. 9` 는 캡션 텍스트만으로 출처 불일치가 보인다(§10-⑱).

---

## 0. 이 digest 를 읽는 법 — "DFT 위주로" 라는 요청에 대한 정직한 답

**이 리뷰에는 자체 DFT 가 한 줄도 없다.** 1저자가 기대했을 계산 항목 — HOMO/LUMO 표 · 산화·환원 전위 계산 · Na⁺ 결합에너지 · 용매화 구조·RDF · ESP · AIMD 조건 — 은 **거의 전부 없다**. 본문 전수 문자열 검색(하이픈 줄바꿈 복원 후) 결과:

| 찾은 것 | 본문 등장 | 비고 |
|---|---|---|
| `DFT` | **8회** | 전부 남의 연구 소개 (흡착에너지 1문장 · ML 후보 검증 3문장 · 그림 캡션) |
| `AIMD` · `ab initio` MD | 2 · 1 | Kim 2023 검증 · Bekaert 2023 비교 대상 |
| `HOMO` · `LUMO` (약어) | **0 · 0** | 풀어 쓴 *"lowest unoccupied molecular orbital"* **1회** (p.15, 정성 문장 — §4b) |
| 범함수·기저·PP·용매모델(PCM/SMD)·k-점·cut-off | **0** | 방법 파라미터 0줄 |
| `convex hull` · grand potential · NEB · Bader · COHP | **0** | |
| universal MLIP (`UMA`·`MACE`·`CHGNet`·`M3GNet`·`SevenNet`) | **0** | NNP-MD 1편·ML force field 1편 소개뿐 |
| `sulfide` / 황화물 조성 | 9 / **`Na₃PS₄` 1회** | `Na₃SbS₄`·`Na₁₁Sn₂PS₁₂`·Na-argyrodite **0회**. ISE 절은 NASICON·β-alumina 만 다룬다 |
| `NASICON` | 20 | 이 리뷰의 실질 주인공 |

AI 절(§4, p.20–24)은 본문 ≈27 pp 중 **≈4 pp**다. 제목·초록이 약속한 *"property-based frameworks and AI"* 에 비해 얇다. 그래서 이 digest 의 "DFT 위주" 는 세 가지로 채웠다:

1. **이 리뷰가 소개한 계산·ML 연구의 수치 전부** (§3-A·§3-B) — 전부 **2차 인용**이고 원전 번호를 달았다.
2. **이 리뷰가 계산 개념을 잘못·느슨하게 쓴 곳** (§4b LUMO 문장, §7-① ESW 주장, §10) — 우리 ESW·gap 규율과 정면으로 부딪히는 대목이라 가치가 있다.
3. **"property-based framework" 와 "AI 가 DFT 를 대체/보완" 의 실체** (§5-4·§5-5).

> ⚠⚠ **전위 기준이 셋이다.** 이 리뷰의 창(ESW)은 **vs Na⁺/Na**, Na 금속·흑연 전위는 **vs SHE**, 우리 ESW(2.256 V 산화 onset)는 **vs Li⁺/Li** 다.
> 이 리뷰의 어떤 전압도 우리 값 옆에 놓지 않는다 (`li2026_na_sulfide_halide_interface_review` §4b 가 같은 판정을 이미 적어 뒀다 — 고체 전해질의 μ 기준에서는 SHE 경유 단순 환산이 성립하지 않는다).

---

## 1. 한 줄 요약

Na-ion 전해질(GPE·SPE·무기 SE·하이브리드) 연구가 파편화돼 있다는 진단 아래, **이온전도·전기화학 안정성·기계 강건성·계면 호환성(+ 지속가능성·비용)** 을 축으로 삼는 *성능 중심·기전 지향* 틀과 **ML/AI 를 "보조가 아닌 핵심 동력"** 으로 놓는 로드맵을 제시한 **개관 리뷰** — 그러나 그 틀은 **조작적 정의(순서·문턱·계산법)가 없는 개념도(`Fig. 2`)** 이고, 계산 내용은 전부 2차 인용이며, **부류별 물성 범위·ESW 주장·그림 서술에 자기모순과 오인용이 많다** (§10 에 21건).

---

## 2. 메타 / 동기 / 구성

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| L. T. Gao 외 7 (Waterloo · 上海大学) | *Electrochem. Energy Rev.* 9:23 (2026) | 10.1007/s41918-026-00296-x | NASICON(`Na₃Zr₂Si₂PO₁₂` 계), β/β″-alumina, PEO·PVDF-HFP 계 고분자, (`Na₃PS₄` 1회) | 리뷰 (계산 0 · 실험 0) |

**동기 (p.3–4)**: ① 기존 리뷰는 전해질 부류별·단일 지표(전도도, 계면 개질) 최적화에 치우쳐 **덴드라이트·계면 열화·기계 불안정을 따로 다룬다** ② 저자들이 **62편의 기존 리뷰**(`Table S1`)를 분류해 보니 그렇다 ③ ML·고처리량 계산이 **기존 리뷰 틀에 체계적으로 들어가지 않았다**.

**구성과 쪽 비중** (본문 p.1–28):

| 절 | 쪽 | 내용 | 계산 관련 |
|---|---|---|---|
| 1 Introduction | 1–4 | 탄소배출 `Fig. 1` · SIB 동기 · 선행 리뷰 `Table 1` · 틀 `Fig. 2` | 없음 (DFT·MD·MC 는 *"비싸고 실험 맥락이 없다"* 한 문장) |
| 2 Electrolyte Classification | 4–14 | GPE(2.1) · SPE(2.2) · ISE(2.3: NASICON·β-alumina) · 하이브리드(2.4) · 비교 `Fig. 3` | 없음 |
| 3 Crack, Dendrite, Interface | 14–19 | 균열(3.1) · Na 덴드라이트(3.2, `Table 2`) · 계면(3.3) | **DFT 흡착에너지 1문장 · LUMO 1문장** (§4b) |
| **4 AI for Electrolyte Discovery** | **20–24** | 4.1 AI-관련 물성 · 4.2.1 조성 기반 · 4.2.2 구조 인지 · 4.2.3 비정질·계면 · 4.2.4 폐루프 | **이 리뷰의 계산 내용 전부** |
| 5 Sustainability and Cost | 24–27 | 비용 동등성 · LCA · ELET 표준화 `Fig. 17` | 없음 |
| 6 Challenges and Outlook | 27–28 | 전도도·계면·덴드라이트 · AI 난제 `Fig. 18` | GNN·PINN·UQ 한 단락 |

---

## 3. 핵심 수치 총정리 ★

> **전부 2차 인용이다.** "원전" 열의 번호는 이 리뷰의 참고문헌 번호. ⛔ **이 리뷰의 인용 번호는 틀린 곳이 여럿 확인됐다**(§10-⑮) — 번호만 믿고 원전을 달지 말 것.

### 3-A. DFT/원자단위 계산 수치 (리뷰 전체에서 이게 전부다)

| 양 | 값 | 계 | 원전 (이 리뷰가 적은 것) | 방법 정보 |
|---|---|---|---|---|
| Li 흡착(결합)에너지 | **> ~1 eV** | Li / 탄소계 기판 | [158] Uthaisar 2009 *JAP*(zigzag 그래핀 나노리본) · [159] Valencia 2006 *JPCB*(흑연) | **n/a** — 범함수·기준상태(원자 vs 금속)·피복률 미기재 |
| Na 흡착에너지 | **~0.51 eV** | Na 단원자 / 흑연 | [160] Rytkönen 2004 *PRB* 69, 205404 | **n/a** |
| Na 표준전위 | −2.714 V (p.2) · −2.71 V (p.16) **vs SHE** | Na/Na⁺ | [5]·[162]·[163] | 실험 상수 |
| Na 이론용량 | 1 165 mAh g⁻¹ | Na 금속 | [5]·[6] | — |
| "흑연 음극 작동전위" | **~2.84 V vs SHE** | *"conventional SIBs … graphite"* | [164] Meister (dual-ion 셀 논문) | ⛔ **값·부호·계 모두 의심** (§10-⑤) |
| 배위에너지 ML 정확도 | 본문 **"better than 0.02 eV"** ↔ `Fig. 15a` **CV error figure-read ≈ 0.127–0.13 eV**(MLR·LASSO·ES-LiR 최선점), 기술자 조합 분포 ≈0.13–0.24 eV | 알칼리 이온–용매 분자 | [212] Ishikawa 2019 *PCCP* 21, 26399 | GPR 은 그림에 없다 · ⛔ **본문과 그림이 ~6배 다르다** (§10-⑧) |
| 활성화에너지 | 0.20 eV | Fe 도핑 α-Al₂O₃ + 30 vol% TZ-3Y → Na-β″-alumina | [129] Ghadbeigi | **실험** |

### 3-B. ML/스크리닝 수치 (§4.2 — 리뷰의 실질 계산 내용)

| 연구 (원전) | 계·데이터 | 모델·기술자 | 지표 | 후속 검증 | 리뷰가 안 적은 것 |
|---|---|---|---|---|---|
| **Kim 2023** [206] *ACS AMI* 15, 41417 | NASICON **3 573 구조** | 조성 기술자(Na 함량·이온반경·전기음성도) → **LightGBM + XGBoost 앙상블 분류기** · 문턱 σ > 10⁻⁴ S cm⁻¹ | **accuracy 84.2 %** | **DFT + AIMD** → `Na₃YTaSi₂PO₁₂` · `Na₃HfZrSi₂PO₁₂` · `Na₃LaTaSi₂PO₁₂` · `Na₃ScTaSi₂PO₁₂` "열역학 안정·고전도" | 레이블 출처 · 클래스 균형 · 분할 · DFT 안정성 기준(E_hull?) · AIMD T·시간 |
| **Zhang 2024** [207] *ChemSusChem* 17, e202301284 | **실험** 211 레코드 / NASICON 160종 / **24 특징**(합성조건·구조·전자) | RF vs NN 회귀 · 전역 민감도 + **Sobol** | **R² 0.82** | — | 분할 단위(같은 물질의 여러 레코드가 train·test 양쪽?) |
| **Zhang 2024** [205] *J. Energy Storage* 75, 109714 | antiperovskite **106 시료** (Li·Na-rich) | 분류(SVC·kNN·RF·DT·LR·LDA) + **symbolic regression** | `Fig. 13b` figure-read: 분류 문턱 **1×10⁻⁶ S cm⁻¹** · 중요 특징 `Ea` `M_b` `M_x` `η` `V_c` `CS` `t` · 회귀식 *"t×g_x/(V_c/CS) ~ log σ"* · 새 기술자 **t/η** | — | 성능 지표 수치 없음 |
| **Wu & Sun 2022** [208] *ACS Mater. Lett.* 4, 175 | **> 4 000 위상 물질** (Na-ion **양극** 스크리닝) | **GPR** + 결정트리 → Na 확산장벽 지도 | 중요 특징: 양이온 반경·전기음성도 | — | 장벽의 원천(NEB? BV?) |
| **Pereznieto 2023** [209] *Mater. Lett.* 349, 134848 | 실험 전해질 **160종 · σ–T 5 619점** · **Magpie 145 기술자** | 다중 회귀기 → **RF 최선** | **R² 0.97** | ICSD Na 화합물 **~25 000** 스크리닝 → `NaPb₃` · `Na₂MoO₄` · `NaMoF₆` · `Na₃BiO₃` → **"phonon-DOS DFT 로 확인"** | **분할 단위** (§7-② · §10-⑫) · 전자절연 필터 (§10-⑬) |
| **Katcho 2019** [210] *J. Appl. Cryst.* 52, 148 | Li·Na 화합물 **> 2 500** | **고처리량 bond-valence(BV) 에너지 지형** + 그래프 퍼콜레이션 + Voronoi → 회귀 | 핵심 예측인자: **전역 확산 병목 · 양이온 배위수 · 이동이온 부피분율** | — | 지표 수치 |
| **Park 2024** [12] *npj Comput. Mater.* 10, 226 | Na 화합물 **12 670** · **구조 기술자 180** | 비지도 — **계층적 밀도기반 군집** + 결정트리 | **구조족 12개**(NASICON·thiophosphate 등) — 열린 채널·약한 Na–음이온 상호작용 ↔ 고전도 | 결정트리가 *"DFT 입력 없이"* 조성만으로 선별 | — |
| **Bekaert 2023** [211] *JPCC* 127, 8503 | **`Na₃PS₄`/Na 금속 계면** | **NNP-MD**(DFT 데이터로 학습) | **수백 ps** — *"AIMD 보다 자릿수 길다"* | 순차 분해 **PS₄ → PS₃ → PS₂ → PS** · SEI 동역학적 안정화 | 학습셋·온도·셀 크기 |
| **Luo 2024** [19] *JMCA* 12, 33518 | **NaPSO 유리** | ML force field | O 도핑이 구조 유연성↑ → 자유부피↓ 에도 D↑ → 실험의 **비단조 σ** 설명 | — | — |
| **Rezaei 2024** [13] *ACS AMI* 16, 32169 | Na-triflate **water-in-salt** | 리뷰 표현 *"ML-informed polarizable force fields"* (✎ 원전 제목은 *"first-principles-based molecular dynamics"*) | 수송 양호 · SEI 불안정 경고 | — | — |
| Jagad 2024 [33] *JES* 171, 060516 | 고체고분자·액체 전해질 1D/3D 수송 | GPR + 물리 연속체 모델 | — | — | — |
| Halilu 2024 [213] *JPS* 614, 235016 | 고체 공융(DES) 전해질 | Tikhonov 정규화 + k-fold CV 로 DRT 분해 | 수소결합 vs Na⁺ 확산 기여 분리 | — | — |
| Parejiya 2024 [214] *JOM* 76, 1088 | NASICON 분리막+양극 전셀 설계 | 리뷰 표현 *"ML-guided interface compatibility"* | — | — | ⛔ `Fig. 15b` 에 ML 요소 없음 (§10-⑨) |

### 3-C. §4.1 "AI-관련 물성" — 부류별 범위 (⚠ 같은 리뷰 안에서 서로 어긋난다)

| 물성 | GPE | SPE | ISE | 출처(쪽) |
|---|---|---|---|---|
| σ (RT) — §4.1 | > 1 mS cm⁻¹ | **< 0.01 mS cm⁻¹** | **0.1–1 mS cm⁻¹** | p.20 [61–63]·[194,195]·[49] |
| σ (RT) — §2.2 | — | **10⁻³–10⁻¹ mS cm⁻¹** | — | p.8 |
| σ — §2.3 NASICON 실례 | — | — | **4.64 · 4.92 · 3.2 mS cm⁻¹** (도핑) | p.11 [98]–[100] |
| σ — `Fig. 3` 표 | 10⁻³–10⁻² S cm⁻¹ (*"moderate"*) | **10⁻⁵–10⁻³ S cm⁻¹** (*"low"*) | **10⁻³–10⁻² S cm⁻¹** (*"high"*) | p.6 — ISE 가 §4.1 보다 **10배**, SPE 가 §4.1 보다 **100배** 높고, GPE 와 ISE 가 같은 범위인데 라벨만 다르다 |
| ESW (vs Na⁺/Na) | **~4.0 V** | **> 4.0 V, ~5.0 V 근접** | **> 4.5 V** (*"sulfide and NASICON-type ceramics"*) | p.20 [196,197] · [199–201] · **[198,199]** — ⛔ ISE 근거 둘 다 **Li 계 논문** (§7-① · §10-③) |
| 기계 | 낮은 전단탄성률 | 중간 강성 | 높은 탄성률 | p.20 [202]·[203]·[43] — 수치 0 |

### 3-D. 실험 수치 (배경 — 우리 4축과 무관, 전사만)

- **GPE** (p.7–8): 나노셀룰로오스 **2.32** mS cm⁻¹ [73] · spirocyclic biphosphate 공중합 **3.26** [74] · HPMC **3.3** [75] · adiponitrile+EC **4.6** [77] · methyl phosphonate 삼원공중합 **5.13** mS cm⁻¹, 250 °C 까지 열안정 [79] · 가교 인산계 −20~70 °C [78] · PU+폴리도파민 t_Na⁺ **0.70** [71].
- **SPE** (p.8): PEO-NaPF₆ **85.8 %/200 cyc @2 C** (Na‖NVP@C) [85].
- **NASICON** (p.11): Sc³⁺/Ge⁴⁺ **4.64** [98] · Sc³⁺/Si⁴⁺ **4.92** [99] · Mg²⁺ **3.2** @25 °C [100] · Yb³⁺/Sc³⁺ **1.62** [101] · Cu²⁺ 계면저항 **19 Ω cm²** · 도금/박리 **1 450 h** [102] · 이중상 **2.7** [108] · 냉간소결 **< 400 °C** [112] · Hf 계 **1.07** mS cm⁻¹ [114] · `Na₃.₄Zr₁.₈Cu₀.₂Si₂PO₁₂` **660 cyc @5 C, 86.5 %** · Mg 도핑 60 °C·0.1 mA cm⁻²·~300 Wh kg⁻¹(인용 없음).
- **β/β″-alumina** (p.11–12): Na-β = Na₂O·11Al₂O₃(육방) · Na-β″ = Na₂O·5Al₂O₃(능면체, c 축 ≈1.5배, 전도층 2개) · β″ RT **~2 mS cm⁻¹** [120] · ~1 500 °C 에서 분해 [121] · MnO₂ 1.0 wt% / Ta₂O₅ 0.3 wt% → **1.0×10² / 1.1×10² mS cm⁻¹ @350 °C** [124] · YSZ 굽힘강도 **260 MPa** [125,126] · Mn/Ni *"fracture toughness … **296 MPa**"* @1.5 wt% [127] (⛔ 단위 오류 §10-⑱) · TiO₂ **3×10² mS cm⁻¹ @300 °C** [127] · Cs₂O > 3 wt% 역효과 [128] · 밀도 97 %·입자 0.8 µm [129].
- **하이브리드** (p.13): > **50 000 cyc** [132] · 산화안정 > **4.8 V** [133] · CATL 2세대 SIB > 200 Wh kg⁻¹ (2027 목표, 신문기사 [134]).
- **`Table 2` 핵생성 과전압**: Na — Cu **~27** · Al **~45** · NSCNT **~9** mV [154] · Al(100) **25** / 상용 Al **46** mV [155]; Li — Cu(카보네이트) **~40** · Ni(10 µA cm⁻²) **~30** · Au **~0** [156] · Ag NP **~25** mV [157].
- **SEI** (p.17): NaDFOB 유래 SEI = Na₂CO₃·NaOH·NaBF₄·Na₄B₂O₅·NaF [173–175] · **~50 사이클**에 보호 최적 [170].
- **비용** (p.24–25): LFP 대비 비용 동등성 **2030년대 이전 불가** [220].

---

## 4. DFT/계산 방법 ★ — 1저자 요청 체크리스트에 대한 답

### 4a. 체크리스트 (리뷰 자체 · 인용 연구 모두)

| 요청 항목 | 이 리뷰 | 판정 |
|---|---|---|
| 코드 (Gaussian/ORCA/VASP/QE/CP2K…) | **n/a** — 코드 이름 0회 | 리뷰에 없음 |
| 범함수 (+분산보정) | **n/a** | 리뷰에 없음 — [158]–[160] 흡착에너지조차 범함수가 안 붙어 있다 |
| 기저 / PP | **n/a** | 리뷰에 없음 |
| **용매 모델** (PCM/SMD/명시적) | **n/a** — 액체·GPE 를 다루면서도 용매화 계산은 0. `solvation` 5회는 전부 실험 서술 | 리뷰에 없음 |
| **산화·환원 전위 계산 방식** (열역학 사이클 · 기준 환산 상수 · HOMO/LUMO 근사 vs ΔG) | **계산 0.** 유일한 관련 문장 = LUMO 정성 문장 1개(§4b). ESW 수치는 **부류별 실험 범위**이고 측정법(LSV/CV 스캔속도·컷오프 전류)도 없다 | ⛔ **HOMO/LUMO 인지 ΔG 인지 구분할 재료가 없다** — 구분이 없는 것 자체가 약점 (§7-①) |
| **결합에너지 정의** (BSSE 보정) | "binding/adsorption energy" 2회(Li >~1 eV · Na 0.51 eV) — **기준상태·BSSE·피복률 미기재** | 정의 없음. ✎ 주기 슬랩 흡착이라 BSSE 는 대개 해당 없지만(평면파), **원자 기준인지 금속 기준인지**가 추론의 성패를 가른다 (§10-⑥) |
| MD/AIMD (힘장·앙상블·T·시간) | Kim 2023 "AIMD 검증"(조건 0) · Bekaert NNP-MD "수백 ps"(조건 0) · Luo MLFF(조건 0) · Rezaei 편광 FF(조건 0) | 조건 전부 n/a |
| **데이터셋 크기·출처** | ✅ **있다** — 3 573 / 211(160종) / 106 / > 4 000 / 5 619(160종) / ~25 000(ICSD) / > 2 500 / 12 670 (§3-B) | 이 리뷰에서 유일하게 정량적인 계산 정보 |
| **ML 모델·기술자** | ✅ 있다 (§3-B) | 모델명·기술자 목록은 충실 |
| **검증 방식 (분할·지표)** | 지표만(84.2 % · R² 0.82 · R² 0.97 · "< 0.02 eV") — **분할 규약·클래스 균형·불확실도 0** | ⛔ 지표 비교 불가 (§7-② · §10-⑫) |
| 무질서 처리 (SQS 등) | **n/a** | 리뷰에 없음 |

**결론**: 이 리뷰를 **계산 방법의 근거로 인용할 수 있는 곳은 없다.** 방법을 알려면 §16 의 원전을 확보해야 한다.

### 4b. 유일한 "궤도 에너지" 문장 — LUMO 와 ESW 를 섞는 법 (★ 우리 규율과 정면으로 겹친다)

> p.15: *"In conventional liquid electrolytes (`Fig. 10a`), dendrites typically grow in a directional manner because the **lowest unoccupied molecular orbital of the electrolyte lies below the redox potential of Na**, thereby driving continuous electrolyte reduction until a stable SEI forms [5]."*

세 가지가 섞여 있다:
1. **에너지와 전위의 부호 혼동** — LUMO 는 에너지(eV, 위가 +)이고 "redox potential" 은 전위(V, 에너지 눈금에서는 −eE)다. 교과서적 서술은 *"음극의 전기화학 퍼텐셜(페르미 준위 μ_A)이 전해질 LUMO 보다 **위에** 있으면 전해질이 환원된다"* 이다. "LUMO 가 Na 전위보다 **아래**" 는 눈금을 안 밝히면 참·거짓이 정해지지 않는다.
2. **인과 오류** — 전해질 환원은 **SEI 형성**을 설명하지 **방향성 덴드라이트 성장**을 설명하지 않는다 (✎).
3. **HOMO/LUMO ≠ 전기화학 창** — litdb `nolan2018_computation_accelerated_design_review` §9-② 가 이미 원문으로 박아 둔 정의: *"The electrochemical window is the gap between the reduction and oxidation potentials based on the Gibbs free energy difference of the reactants and products, and is different from the band gap or the gap between the levels of HOMO and LUMO … the gap between HOMO and LUMO is an **upper bound** of the electrochemical window."* (Nolan 2018 p.2022, 원전 Peljo & Girault 2018 *EES* *"The HOMO–LUMO misconception"*).

⇒ 이 리뷰는 궤도 근사와 ΔG 근사를 **구분하지 않는다** — 수치가 없으니 틀렸다고도 맞았다고도 할 수 없고, **이 문장을 우리 원고의 근거로 쓰면 안 된다**는 것만 확실하다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5-1. §2 전해질 분류 + `Fig. 3` (✅ 실독)

`Fig. 3` 은 위쪽 **비교표**(Key performance · Advantages · Disadvantages · Applicable scenarios)와 아래쪽 **7축 레이더**(1 = Very poor … 5 = Excellent)다. 캡션·본문이 설명 없이 가리키기만 하고 **점수의 출처가 없다**. 실독 결과 **표와 레이더와 본문이 서로 어긋난다**:

| 축 | 레이더 figure-read ≈ (±0.3) | 같은 그림의 표 / 본문 | 판정 |
|---|---|---|---|
| Ionic conductivity | ISE ≈4.6 > **SPE ≈3.0 > GPE ≈2.7** | 표: GPE *moderate* 10⁻³–10⁻² · SPE *low* 10⁻⁵–10⁻³ S cm⁻¹ · 본문: GPE > 1, SPE < 0.01 mS cm⁻¹ | 🔴 **SPE 점이 GPE 점 바깥** — 순서 역전 |
| Electrochemical stability | ISE ≈4.3 > GPE ≈3.6 > **SPE ≈2.8** | 표: SPE *"high electrochemical stability"* · 본문: SPE > 4.0→~5.0 V ≥ GPE ~4.0 V | 🔴 SPE 가 최하위 |
| Mechanical strength | ISE ≈4.7 · SPE ≈ GPE ≈2.9 (점 겹침) | 본문: SPE *moderate stiffness* > GPE *low shear modulus* | 🟠 구분 없음 |
| Interface contact | GPE ≈4.2 > **ISE ≈3.8** > SPE ≈2.8 | 표: ISE 단점 *"Poor interface contact"* | 🔴 ISE 가 "Good" 수준 |
| Safety | **GPE ≈3.8** > SPE ≈ ISE ≈3.0 | 본문: GPE 는 가연성 용매 위험 · 표: SPE·ISE 가 *"High-safety solid-state batteries"* | 🔴 GPE 가 최고 |
| Processability | SPE ≈4.9 > GPE ≈4.3 > ISE ≈2.9 | 본문과 정합 | ✅ |
| Cost effectiveness | 반경 SPE ≈3.7 > ISE ≈2.8 > GPE ≈2.4 | 축 라벨 *"(Lower is better)"* ↔ 범례 5 = Excellent · 표: ISE *"High cost"* | 🔴 **해석 불능** (라벨과 척도가 반대) |

표 자체에도 **SPE 단점에 "Brittle"** 이 있다 — 취성은 본문이 ISE 의 한계로 드는 성질이다. ⇒ `Fig. 3` 은 **정성적 인상의 요약으로도 쓰면 안 된다.**

2.3 절 ISE 는 **NASICON(도핑·소결)과 β/β″-alumina(상 안정화·도핑)** 두 가지만 다룬다. 황화물 Na SE 는 *"sulfide-based electrolytes"* 한 번 호명되고 끝난다.

### 5-2. §3 균열·덴드라이트·계면 + `Fig. 10` (✅ 실독)

- **3.1 균열**: 양극 입계 균열(`Fig. 9` Zn 석출 안정화 [141]), MRI 로 Na 덴드라이트 가시화 [142], 코팅·구배·도핑(Li/Ti [145], W [146])·중공 입자, FEC 첨가제. 전부 실험 서술.
- **3.2 덴드라이트**: 네 형태(선형·분지·파편·분산) [151,152]; Na⁺ 는 **입계·공극·결함 등 고에너지 자리에 모이고 국소 전자누설이 환원을 돕는다** [153]. → `Fig. 10b` 에 실제로 *"Na agglomeration penetrates along electrolyte grain boundaries"* · *"The interconnection of the originally isolated Na deposits → results in short circuit"* · **"Dendrite growth affects mechanical properties and bandgaps of electrolyte grain boundaries"** 가 인쇄돼 있다 (Darjazi 2024 [9] 재수록). ✎ 이 **입계 밴드갭 감소 → 내부 전자누설** 서사는 우리 축 D(전자구조)가 벌크 갭만 보고 입계는 안 본다는 한계와 같은 곳을 가리킨다 (§7-D 보조).
  - **DFT 문장** (p.15–16): Li 는 탄소계 기판에 > ~1 eV 로 강하게 흡착 [158,159], Na 단원자/흑연은 ~0.51 eV [160] → *"Na has a lower thermodynamic driving force for anisotropic whisker-type dendritic growth"* → Na 는 이끼형·판상, Li 는 바늘형 휘스커. ⛔ 추론의 비약 (§10-⑥).
  - `Table 2` 와 본문: *"Au·Ag 같은 친리튬 기판에서 Li 핵생성 과전압이 0 에 가깝다"* ↔ 표의 Ag NP **~25 mV** (§10-⑰).
  - 저자 자기 인용: Gao & Guo 2024 [161] **phase-field** 로 Na 덴드라이트 형태(전류밀도·이방성 강도·Na⁺ 소모) — 저자 그룹의 유일한 모델링 이력이다(DFT 아님).
- **3.3 계면**: SEI 는 정적 막이 아니라 동적 층(내층 무기 NaF·borate / 외층 유기), ~50 사이클 최적 [170], 전략 3갈래(전해질 공학 · 계면 재구성 · 전극 구조). *"dual-domain molecular-locking"* [193] 은 액체 전해질 사례.

### 5-3. §4.1 "AI-relevant properties" — 물성 중심 재분류

리뷰의 핵심 제안: 전해질을 화학(GPE/SPE/ISE)이 아니라 **AI 가 학습할 물성**으로 재배치하자. 세 축 — **이온전도도 · 전기화학 안정창 · 기계 강건성** — 과 부류별 범위(§3-C). §5 끝에서 **지속가능성·비용을 "다섯 번째 물성 공간"** 으로 추가하고(*"complementing conductivity, stability, interfacial compatibility, and mechanical robustness"*), 계면 호환성은 네 번째로 암묵 편입된다.

### 5-4. "property-based framework" 가 **실제로 무엇인가** (1저자 질문)

`Fig. 2` (✅ 실독): 가운데 *"Na⁺ AI assisted solid-state electrolyte"* 배터리, 둘레에 **5개 노드** — **AI-guided design · Interphase engineering · Safety · Sustainability · Performance** — 와 노드 사이 양방향 화살표(*"AI optimizes interphase / Interphase data refines AI"* · *"Performance feedback trains AI"* · *"High performance reduces safety risk / Safety constraints guide performance optimization"* · *"Sustainable materials improve performance"* …), 바깥 고리 6칸(*"Faster discovery, lower cost"* · *"Stable interface, longer life"* · *"Inherent safety, reduced risk"* · *"Resource efficient, low environmental impact"* · *"High conductivity, strong structure"* · *"High ionic conductivity, high energy density"*).

| 스크리닝 틀이라면 있어야 할 것 | 이 리뷰 |
|---|---|
| 어떤 물성을 | ✅ 5개 (σ · ESW · 기계 · 계면 · 지속가능/비용) |
| 어떤 계산으로 내나 | ❌ **없다** — 물성별 계산법(σ ← MD/BVSE, ESW ← hull/grand-potential, 기계 ← C_ij, 계면 ← 반응에너지) 대응표가 없다 |
| 어떤 순서로 거르나 | ❌ **없다** — `Fig. 2` 는 순환 관계도지 깔때기가 아니다 |
| 문턱은 | ❌ 틀 차원의 문턱 0. 인용 연구 두 곳에만 있다: σ > 10⁻⁴ S cm⁻¹ (Kim 2023) · 1×10⁻⁶ S cm⁻¹ (antiperovskite, `Fig. 13b`) |
| 물성 간 상충의 처리(파레토·가중) | ❌ "상호의존" 이라는 말만 |

⇒ ✎ **"property-based framework" = 물성 5개로 문헌을 재분류하는 개념도**다. 계산 워크플로가 아니다. 워크플로에 가장 가까운 그림은 `Fig. 14`(조성 기반 ML 파이프라인)와 `Fig. 16`(폐루프)인데, 둘 다 틀의 물성 5개와 연결돼 있지 않다.

### 5-5. §4.2 AI 가 DFT 를 **대체**하는 곳과 **보완**하는 곳 (1저자 질문)

| 역할 | 사례 (이 리뷰가 적은 대로) | ✎ 우리 판단 |
|---|---|---|
| **대체 — 계산 자체를 건너뜀** | Park [12] 결정트리가 *"without explicit DFT input"* 조성만으로 초이온체 선별 · Zhang [205] t/η 로 *"without full structural modelling"* · Ishikawa [212] *"circumventing costly quantum mechanical simulations"*(배위에너지 회귀) | 1차 선별용. 정확도 주장은 §10-⑧ 처럼 검증 불가 |
| **대체 — 더 긴 시간척도** | Bekaert [211] NNP-MD *"hundreds of picoseconds … orders of magnitude longer than AIMD"* · Luo [19] MLFF | ✅ 가장 성숙한 역할. 우리 UMA MLIP-MD 가 이 칸이다 |
| **보완 — ML 후보를 DFT/AIMD 로 검증** | Kim [206] → DFT 열역학 안정성 + AIMD 전도 · Pereznieto [209] → **phonon-DOS DFT** · `Fig. 13a` ML → DFT → 실험 · `Fig. 14` Validation 열 = DFT · AIMD · 실험 | ⚠ "phonon DOS 로 고전도 확인" 은 σ 의 확인이 아니다(§10-⑬) |
| **보완 — DFT 가 학습 데이터원** | `Fig. 14` Data sources 에 *"DFT/AIMD Database"* · NNP 는 *"trained on DFT datasets"* | 학습 범함수 편향 상속 문제는 언급 없음 (`oginni2026` §9-④ 참조) |
| **물리 기반 보강** | PINN(Nernst–Planck·Poisson) [229] · GNN 위상 학습 [226–228] · 베이지안·앙상블 UQ [230] (§6) | 한 단락 나열. 적용 사례 0 |

`Fig. 14` (✅ 실독, 저자 자작 — "Adapted" 표기 없음): **Data Sources**(Experimental DB · DFT/AIMD DB · ICSD ~25 000) → **Feature Engineering**(조성: Na 함량·이온반경·전기음성도 / 구조 기술자 / Magpie) → **ML Models**(RF · XGBoost/LightGBM · NN · GP) → **Predictions**(Ionic conductivity · Diffusion barrier · Stability screening) → **Validation**(DFT · AIMD · Experimental confirmation) → **Key Insights** 4줄: *Na stoichiometry: Dominant factor · Sintering conditions: Critical · Electronegativity: Secondary role · **Tolerance factor ↓ : Conductivity ↑***. 🔴 네 줄이 **서로 다른 계의 결과를 한 법칙처럼 합친 것**이다 — 앞 셋은 NASICON 실험 211 레코드(Zhang [207]), 마지막은 antiperovskite 106 시료(Zhang [205])이고, 본문은 **t/η 비**가 log σ 와 음의 상관이라 했는데 그림은 **t 단독**으로 줄였다.

`Fig. 16` (✅ 실독, 저자 자작): Prediction(data-driven models · virtual screening · candidate ranking) → Synthesis(targeted · high-throughput) → Testing(electrochemical · σ · stability/interface · cycling) → Iteration(feedback · retraining · active learning · next-round prediction), 가운데 Database/Model. ✎ **폐루프 안에 DFT/시뮬레이션 노드가 없다** — `Fig. 14` 에서는 검증 단계였던 DFT 가 여기서는 사라졌다.

`Fig. 18` (✅ 실독): Challenges(저전도 · 계면 불안정 · 덴드라이트) → AI & Modeling Strategies(**GNN** 위상학습 · **Physics-informed** Nernst–Planck/Poisson · **Ensemble & Uncertainty** = *"Bayesian Optimization"*) → Future(하이브리드 전해질 · AI–실험 통합 · 오픈 데이터 · 기술경제). ✎ "AI & Modeling" 열에 **MLIP·DFT 가 없다** — 리뷰 본문(§4.2.2)이 가장 구체적으로 보여 준 도구(NNP-MD·MLFF)가 전략도에서 빠졌다. UQ 와 베이지안 최적화를 한 칸에 묶은 것도 개념 혼동이다.

### 5-6. §5 지속가능성·비용, §6 전망

- 비용: SIB 는 LFP 와 비용 동등성을 **2030년대 이전에 달성하기 어렵다** [220]; 레버 = 컷오프 전압↑·비용량↑·전극 두께 최적(`Fig. 17a`, 미독). LCA: 고체 SIB(NASICON)가 자원·독성 영향 최저 [221]. 황화물은 수분 제어가 비용 요인 — 대기 가공 표면분자공학 [224]. ELET 표준화(`Fig. 17c`, 미독 — 캡션은 [222], 본문은 [223] 로 번호가 다르다).
- 전망: 데이터 희소·파편화 · 기술자 선택 · 해석가능성 · 전이성 · **교차검증·실험 벤치마크 부족**(리뷰 자신이 지적한다 — 그런데 §4.2 에서 소개한 연구들의 교차검증 규약은 안 적었다).

---

## 6. 논증 흐름 종합

**주장**: 전해질 성능은 고립된 물성이 아니라 **결합된 구조–물성 관계**로 봐야 하고(p.19), 그 결합을 풀 도구가 **AI** 다(§4). 순서는 ① 부류별 트레이드오프(§2) → ② 실패 기전 3종의 결합(§3) → ③ 물성 중심 재분류(§4.1) → ④ ML 사례(§4.2) → ⑤ 비용·표준(§5).
**약한 고리**: ③→④ 가 끊겨 있다. §4.1 의 물성 축이 §4.2 의 어떤 ML 사례와 연결되는지(예: ESW 를 예측하는 ML 은?) 한 번도 대응시키지 않는다. §4.2 사례는 **거의 전부 σ(또는 확산장벽) 예측**이고, ESW·기계·계면을 ML 로 예측한 사례는 **0건**이다 (Bekaert 계면 분해 MD 가 유일하게 계면 쪽).

---

## 7. 우리 DFT 와의 대조 ★★ (`../our_dft_baseline.md` · 1저자 지정 3축)

> ⛔ **이 리뷰의 수치는 전부 소환값이고 Na 계다. 우리 db 절대값과 한 표에 두지 않는다.** 아래 표는 **방법 대 방법** 비교다. 물성 4축(A–D) 표에는 행을 만들지 않는다 → `comparison_vs_ours.md` §J-49 (🔧 방법 원전 블록 · 참고: 같은 날 §J-48 은 다른 편 `[Li26MnS]` 이다).

### 7-① 산화안정성 / 전위창 — **계산 방식이 무엇이 다른가**

| 항목 | 이 리뷰 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 창의 **정의** | 없음. 부류별 수치(GPE ~4.0 · SPE >4.0→~5.0 · ISE >4.5 V vs Na⁺/Na)만 | **grand-potential 상평형** (`pymatgen get_element_profile`, μ_Li 스캔, 0 K, GG phase set) = **층①(분해 onset)** | 🔴 **다른 양이다.** 리뷰 수치는 ✎ 실험 겉보기 창(LSV/CV — 동역학·부동태를 포함, `[Schw21]` 의 층②·③ 쪽)으로 보이지만 측정법이 안 적혀 있어 어느 층인지도 확정 못 한다 |
| 궤도 근사 사용 | LUMO 정성 문장 1개 (§4b) — 에너지/전위 부호 혼동 | **고유값 갭은 ESW 에 쓰지 않는다** — fixed-occ nscf VBM/CBM 은 축 D(전자구조), ESW 는 ΔG | ✅ 우리 규율("gap ↔ ESW 분리")이 이 리뷰가 빠진 함정을 막는다. 근거 문장 = `nolan2018` §9-② (Peljo & Girault 2018 원전) |
| 무엇이 창을 정하나 | 설명 없음 | 우리 두 무도핑 조성에서 **S²⁻ 가 산화 onset 을 정한다** (2.256 V vs Li⁺/Li · 두 조성 동일) | — |
| **황화물 창** | *"ISEs, including **sulfide** and NASICON-type ceramics, offer wide stability windows (**>4.5 V vs Na⁺/Na**) and high intrinsic redox stability"* [198,199] | 황화물 열역학 창은 **좁다** — 우리 계(Li)에서 onset 이 S 한계 | 🔴 **진짜 긴장 (같은 Na⁺/Na 눈금 안에서)**: litdb `li2026_na_sulfide_halide_interface_review` `Fig. 3a`(원전 Tang 2018 *Chem. Mater.* 30, 163)의 `Na₃PS₄` 열역학 안정띠는 **figure-read ≈ 1.2–2.5 V vs Na⁺/Na** 다. 리뷰의 ">4.5 V" 를 뒷받침하는 인용 [198] Shimizu 2022(5 V 박막 전고체 **Li** 전지)·[199] Nie 2018(**Li** 양극 계면 리뷰)은 **둘 다 Li 계**다 ⇒ 황화물 Na SE 에 대한 근거가 없다 |
| 기준 전극 | vs Na⁺/Na (창) · vs SHE (금속) | vs Li⁺/Li | ⛔ 수치 비교 금지 (§0) |

**판정**: 🔴 **방법 차이가 아니라 정의 부재**다. 이 리뷰의 ESW 문장은 **우리 "S-limited onset" 서사와 반대 방향**이므로, 우리 원고에서 *"황화물은 창이 넓다"* 류 문장의 근거로 **절대 쓰지 않는다.** 반대로 이 리뷰를 인용해야 한다면 *"부류 개관"* 역할까지만.

### 7-② 스크리닝·ML 방법론 — 우리 cascade · UMA · BVSE · research-agent 와

| 항목 | 이 리뷰가 소개하는 것 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **검증 분할 규약** | 지표만(84.2 % · R² 0.82 · **R² 0.97**) — 분할 단위·클래스 균형·UQ 0 | cascade predictor 는 **LODO** 로 평가(`comparison_vs_ours.md` §J-8: 무작위 분할 R² 0.99 대 우리 LODO −0.18 판정) | 🔴 **§J-8 과 같은 질문.** 특히 Pereznieto [209] 의 **5 619 σ–T 점 / 160 물질**은 ✎ 점 단위 무작위 분할이면 같은 물질의 다른 온도점이 train·test 양쪽에 들어가 R² 가 부풀 수 있다 — 리뷰가 분할을 안 적었으므로 **위험 신호로만** 적는다(원전 미확인) |
| **MLIP** | NNP-MD 1편(Bekaert 2023, `Na₃PS₄`/Na) · MLFF 1편(Luo 2024) · **universal MLIP 0회** · MLIP 논문 [17] Bertani & Pedone 2025(`Na₄P₂S₇` 유리 미세조정)·[18] Klarbring & Walsh 2024(W 도핑 `Na₃SbS₄`)는 **서론 일반문장 인용으로만** 등장 | **UMA-s-1p1 (omat) as-is** MLIP-MD, 558 원자, MSD 2–50 ps, 상대차 인용 정책 | ⚠ 이 리뷰는 **우리 UMA 선택의 근거가 못 된다.** Bekaert 의 현대판은 litdb `li2026_mci_vs_sei_na3ps4_na_mlip_md`(ACE-MLIP + r²SCAN 라벨, Persson 2026)다 |
| **BV 지형 기술자** | Katcho 2019 [210]: BV 에너지 지형 + 퍼콜레이션 + Voronoi → ML, 예측인자 = **전역 병목 · 배위수 · 이동이온 부피분율** | softBV BVSE (`tools/comp1_v3/`), 채널 % = above-min ≤ iso | ✅ **같은 계열의 도구.** 우리 채널 % 는 Katcho 의 "이동이온 부피분율/병목" 과 개념이 가깝다 → **ML 기술자로 쓰는 선례** (원전 확보 대상 §16) |
| 후보의 물리 필터 | 없음 — Pereznieto 후보에 `NaPb₃` | cascade 는 분해 산물 밴드갭(전자누설) 축을 따로 둔다 (⚠ 그 통계는 `HZ-cascade-product-gaps-nonground-polymorph` **HOLD** — 수치 인용 금지) | 🔴 ✎ `NaPb₃` 는 Na–Pb **금속간화합물(금속)** 로 알려져 있다 — 전자절연 필터 없이 σ 만 보면 생기는 전형적 함정. 원전이 갭 필터를 걸었는지는 이 리뷰로 확인 불가 |
| "DFT 로 고전도 확인" | phonon-DOS DFT (Pereznieto) · DFT+AIMD (Kim) | σ·Ea 는 **MLIP-MD 상대차로만** · 절대값 인용 금지 | ⚠ phonon DOS 는 동역학 안정성·격자 연성 지표이지 **σ 의 확인이 아니다** |
| research-agent | (해당 없음) — 리뷰의 AI 는 **물성 예측** | research-agent = **문헌** 알림·분류·큐·vault (물성 예측 아님) | ✎ **겹침 거의 없음.** 유일한 접점은 리뷰 §6·`Fig. 18` 의 *"curated open databases"* 요구 — 우리 litdb/db 원장(출처·인용위험 `citation_hazards.json`)은 그 요구의 한 형태지만 **공개 데이터셋은 아니다** |

### 7-③ Na 계 — 우리에게 Na 계산이 있나

- 지시대로 `grep -ril "Na" db/properties | head` 를 돌리면 **605개 파일**이 걸리는데 `Name`·`NaN` 같은 잡음이다. 조성·용어로 좁히면(`sodium|Na3PS4|Na-ion|NaCl|Na2S|"Na"`) 걸리는 것은 **cascade 계열**뿐이고, 내용을 열어 보면 **Na 는 Li-argyrodite(LPSCl) cascade 의 도펀트 후보(`Na2O`·`Na2S`, x = 0.02)로만** 등장한다 — `oxidation_stability_cascade.json` · `cascade_v23_themes.json` · `seminar_table_esw_windows.csv` · `cascade_interface_li.jsonl`.
- ⇒ **Na 호스트 SE(`Na₃PS₄`·NASICON·β-alumina)에 대한 우리 계산은 없다.** 이 리뷰의 어떤 값도 우리와 같은 표에 놓을 대상이 없다.
- Na 계를 더 직접 다루는 litdb digest: `li2026_na_sulfide_halide_interface_review`(Na 황화물·할라이드 계면 리뷰 · grand-potential 그림 있음) · `jang2026_halide_se_interfacial_stability_highv_na`(Na 할라이드 SE 창 두 겹 정의) · `li2026_mci_vs_sei_na3ps4_na_mlip_md`(`Na₃PS₄`/Na MLIP-MD).

### 7-D (보조) 전자구조 — 입계 밴드갭

`Fig. 10b` 문구 *"Dendrite growth affects … bandgaps of electrolyte grain boundaries"* 와 p.15 *"local electron leakage"* [153] 은 **입계에서 갭이 줄어 SE 내부에서 Na 가 석출된다**는 서사다. 우리 갭(2.066/2.099 eV, fixed-occ nscf 고유값)은 **벌크** 값이다 — 이 리뷰는 수치를 주지 않으므로 비교가 아니라 **우리 §H 정직목록의 "입계 전자구조 미계산" 을 상기시키는 문장**으로만 쓴다.

---

## 8. Post-processing ★ (리뷰가 언급하는 것만)

| 무엇 | 어디서 | 도구 | 수치화 방식 |
|---|---|---|---|
| Sobol 전역 민감도 | Zhang [207] | n/a | 특징별 분산 기여 → *"Na 화학량론·소결 변수 지배, 도펀트 전기음성도 2차"* |
| symbolic regression | Zhang [205], `Fig. 13b` | n/a | 기술자 식 생성 → t/η |
| 계층적 밀도기반 군집 + 결정트리 | Park [12] | n/a | 구조족 12개 |
| BV 에너지 지형·그래프 퍼콜레이션·Voronoi | Katcho [210] | n/a | 병목·배위수·부피분율 |
| phonon DOS | Pereznieto [209] | n/a | "고전도 확인" (§10-⑬) |
| 궤적 분해 분석 (total trajectory analysis) | Bekaert [211] | n/a | PS₄→PS₃→PS₂→PS 순차 |
| CV error 히스토그램 | Ishikawa [212], `Fig. 15a` | n/a | 기술자 조합별 교차검증 오차 분포 |
| DRT (Tikhonov + k-fold) | Halilu [213] | n/a | 완화시간 분포 분해 |

도구 이름(pymatgen·VESTA·LOBSTER 등)은 **0회**.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (미독) 전 지구 배출 격차 — SP 2.0/1.5 시나리오, Wei 2020 재수록 | 없음 |
| 2 | ✅ **"property-based framework" 개념도** — 5노드(AI-guided design · Interphase engineering · Safety · Sustainability · Performance) + 양방향 관계 화살표 + 바깥 고리 6칸. 순서·문턱·계산법 **없음** | 틀의 실체 = 재분류 개념도(§5-4). 우리 cascade 깔때기와 **구조가 다르다** — 비교 대상 아님 |
| 3 | ✅ GPE/SPE/ISE 비교표 + 7축 레이더(1–5). 🔴 **레이더가 표·본문과 5축에서 모순**(σ: SPE>GPE · ESW: SPE 최하 · 계면: ISE≈3.8 · 안전: GPE 최고 · 비용축 라벨 반대), 표의 SPE 단점에 "Brittle" | ⛔ 정성 요약으로도 인용 금지 (§5-1 표) |
| 4 | (미독) PSB X 계 GPE 현장 제조 · NVP/Na 셀 기전 [64][65] | 없음 |
| 5 | (미독) SPE 이온수송 모식 [82] · HMOP 합성 [83] | 없음 |
| 6 | (미독) NZSPO UHS 소결 [103] · 세라믹 함량별 σ [104] | 없음 |
| 7 | (미독) β/β″-alumina 결정구조·전도면 [122] | 없음 |
| 8 | (미독) NASICON 개발 연표 [130] | 없음 |
| 9 | (미독) NMZ10 입계균열 STEM [141] · (c–e) 단락 셀 X-ray 단층·SEM 덴드라이트 균열 [142] · (f,g) 균열 기전 모식. ⚠ 캡션 텍스트 기준: 해상도·스케일 단위 `mm`(µm 오기 의심) · © 2024 AAAS ↔ [142] = Rees 2021 *Angew. Chem.* MRI 논문 — 출처 불일치 | 없음 (양극 균열은 DEM 축 소관) |
| 10 | ✅ 덴드라이트 기전 모식 (Darjazi 2024 재수록): (a) 액체 — 불균일 Na 분포 → 분리막 관통 → dead Na, (b) 다결정 고체 — **입계를 따라 Na 응집·필라멘트 연결 → 단락**, 인쇄 문구 *"affects mechanical properties and bandgaps of electrolyte grain boundaries"*. LUMO 관련 에너지도식은 **없다** | 축 D 보조 — 벌크 갭만 보는 우리 한계 상기 (§7-D) |
| 11 | (미독) SEI ²³Na·¹¹B SS-NMR, 유/무기 비율 [170][180] | 없음 |
| 12 | (미독 · ✂ 손 크롭) PRC 골격 동축전기방사·테이프캐스팅, 이온 경로 비교 [183] | 없음 |
| 13a | ✅ (✂ 손 크롭) **ML → DFT → 실험 워크플로** — 그러나 원전 [204] 은 **K-ion 층상산화물 양극의 공기(H₂O) 안정성** 연구: 주기율표 입력 → NN → Fe/Co/Ni/Cu 출력, *"H₂O attack · Machine learning · DFT calculation(DFT-calculated adsorption energies) · Experiment · Air stable materials"* | 🔴 문맥 이탈 — SIB 전해질 워크플로의 예시가 아니다 (§10-⑩) |
| 13b | ✅ (✂ 손 크롭) antiperovskite ML [205]: 분류(SVC·kNN·RF·DT·LR·LDA, 문턱 1×10⁻⁶ S cm⁻¹, 중요특징 Ea·M_b·M_x·η·V_c·CS·t) + symbolic regression(*"t×g_x/(V_c/CS) ~ log σ"*) → **t/η** | 본문은 이 패널이 *"SSE·계면·용매·양극 등 여러 부품"* 을 보여 준다고 서술 — 🔴 실제로는 한 워크플로. 기술자 탐색 방식 자체는 참고 가능 |
| 14 | ✅ 저자 자작 조성 기반 ML 파이프라인 (Data → Features → Models → Predictions → Validation(DFT·AIMD·실험) → Key Insights 4줄) | 🔴 Key Insights 가 이종 계 결과를 합침 · t/η → t 로 축약 (§5-5). 파이프라인 도식은 우리 cascade 설명용 대조 그림으로만 |
| 15a | ✅ (✂ 손 크롭) Ishikawa 2019 [212] CV error 히스토그램 — x `CV error/eV` 0.12–0.24, y `Number of counts` 0–400, 분포 figure-read ≈0.13–0.24 eV(최빈 ≈0.18–0.19), **MLR·LASSO·ES-LiR 최선점 ≈0.127–0.13 eV** | 🔴 본문 *"better than 0.02 eV"* 와 ~6배 차이 · "비정질·계면" 절에 분자 용매 배위에너지를 분류 (§10-⑧) |
| 15b | ✅ (✂ 손 크롭) Parejiya [214]: 활물질(노랑)+NASICON II(청록) 복합양극 ‖ NASICON I 분리막(녹색) + *"Structure-Function Control in NASICON A_xB_y(TO₄)₃ · Combinatorial Chemistry Approach"* 주기율표(A 자리 1·2가 / B 자리 2–5가 / 음이온 자리). 빨강·회색 입자는 범례 없음 | 🔴 본문 *"ML-guided interface compatibility"* — **그림에 ML 요소 없음** |
| 16 | ✅ 저자 자작 AI–실험 폐루프 (Prediction → Synthesis → Testing → Iteration, 가운데 Database/Model) | ✎ 폐루프에 DFT/시뮬레이션 노드 없음 · 정량 내용 0 |
| 17 | (미독 · ✂ 손 크롭) (a) Na-ion 셀 가격 민감도 2030/2040 [220] (b) LCA 고체 SIB·액체 SIB·액체 LIB [221] (c) ELET [222] | 없음 |
| 18 | ✅ 저자 자작 과제 → AI 전략(GNN · PINN · Ensemble/UQ = "Bayesian Optimization") → 미래방향 | ✎ **MLIP·DFT 부재**, UQ ≠ BO 혼동 |
| Table 1 | 선행 리뷰 6범주(SSE · 액체 · 이온액체 · 고분자/복합 · 계면/용매화/첨가제 · 시스템) 의 초점·기여·한계 | 없음 |
| Table 2 | Na·Li 핵생성 과전압 (§3-D) | ⚠ 전해질·전류밀도가 다른 값의 비교 · 본문 "Ag ≈ 0 mV" ↔ 표 ~25 mV |
| Table S1 | 선행 리뷰 **62편** 분류 (고체 32 · 계면/용매화/첨가제 9 · 액체 8 · 고분자/복합 7 · 이온액체 3 · 일반 3) | 🔴 **#25 = #38 중복**(Zhao *EER* 7, 3 (2024)) → 최대 61편 · **AI/ML 리뷰 범주 0개** |

---

## 10. 비판 — 이 리뷰의 약한 곳 ★

**A. 계산·개념**
- ① **제목 대비 계산 비중** — AI 절 ≈4 pp / 본문 ≈27 pp, `DFT` 8회, 자체 계산 0. 제목의 *"property-based frameworks and AI"* 는 서술의 일부일 뿐이다.
- ② **틀이 조작적이지 않다** — `Fig. 2` 는 관계도다. 물성 → 계산법 → 순서 → 문턱이 없고(§5-4), §4.1 물성 축과 §4.2 ML 사례가 대응되지 않는다(§6).
- ③ **ESW 주장** — *"sulfide … >4.5 V vs Na⁺/Na"* 는 양이 정의되지 않았고, 근거 [198,199] 는 Li 계, 열역학 창(`Na₃PS₄` figure-read ≈1.2–2.5 V vs Na⁺/Na, `li2026_na…` `Fig. 3a`)과 모순 (§7-①).
- ④ **LUMO 문장** — 에너지/전위 부호 혼동 + 인과 오류 + HOMO/LUMO ≠ ESW (§4b).
- ⑤ **"conventional SIBs typically employ … graphite … (~2.84 V vs SHE)"** [164] — ✎ SIB 음극의 표준은 hard carbon 이고(리뷰 자신도 p.25 에서 hard carbon 을 SIB 음극으로 적는다 = 자기모순), 흑연은 카보네이트 전해질에서 Na 를 거의 삽입하지 않는다. "+2.84 V vs SHE" 는 음극 전위로 불가능한 값이다(부호 탈락 의심). [164] 는 흑연이 **양극**(음이온 삽입)인 dual-ion 셀 논문이다 → 인용 역할도 불일치.
- ⑥ **흡착에너지 → 덴드라이트 형태 추론의 비약** — Li >~1 eV [158,159] vs Na 0.51 eV [160] 는 기판(zigzag GNR vs 흑연)·연도(2004–2009)·범함수가 다른 세 편이고 기준상태가 안 적혀 있다. ✎ **단원자 흡착에너지(원자 기준)는 도금의 구동력이 아니다** — 도금의 기준은 **금속 벌크**(응집에너지)여야 하고, SE 나 집전체가 아닌 흑연 흡착으로 SE 내 덴드라이트 형태를 논할 수 없다.

**B. 그림–본문 불일치**
- ⑦ **`Fig. 3`** — 레이더가 같은 그림의 표·본문과 5축에서 모순, 비용축 라벨-척도 반대, SPE 에 "Brittle" (§5-1).
- ⑧ **`Fig. 15a`** — 본문 *"accuracies better than 0.02 eV"* ↔ 그림의 최선 CV error figure-read ≈0.13 eV. GPR 은 그림에 없다. 게다가 **분자 용매 배위에너지**를 *"비정질·계면 전해질"* 절에 넣었다.
- ⑨ **`Fig. 15b`** — *"ML-guided"* 라는데 그림은 조합화학 주기율표 모식이다.
- ⑩ **`Fig. 13`** — (a) K-ion 양극 공기안정성 워크플로를 SIB 전해질 예시로, (b) 단일 antiperovskite 워크플로를 *"여러 부품의 ML"* 로 서술.
- ⑪ **`Fig. 14`** — 이종 계 결과의 합성, t/η → t 축약.

**C. ML 보고**
- ⑫ **지표만 있고 규약이 없다** — 분할 단위·클래스 균형·UQ 0. 84.2 % accuracy 는 기저율 없이 해석 불가, R² 0.97(5 619 σ–T 점/160 물질)은 점 단위 분할이면 부풀 수 있다(§7-②). 리뷰 자신이 §6 에서 *"lack of rigorous cross-validation"* 을 난제로 꼽으면서 정작 소개한 연구의 교차검증은 안 적었다.
- ⑬ **후보의 물리 타당성** — ✎ `NaPb₃`(금속간화합물)를 *"highly conductive candidate"* 로 무비판 전재 · *"confirmed by phonon-DOS DFT"* 는 σ 의 확인이 아니다.
- ⑭ **MLIP 공백** — universal MLIP 0회, MLIP 논문 [17][18] 은 서론 일반문장에만. 원자단위 SE 모델링에서 가장 성숙한 AI 도구가 전략도(`Fig. 18`)에서 빠졌다.

**D. 인용·서지 위생**
- ⑮ **인용 번호 오류·역할 불일치** — §3.2 *"Ding et al. [167]"* → Ding 은 **[166]**, *"Wan et al. [168]"* → Wan 은 **[167]**, *"Tian et al. [163]"* → Tian 은 **[168]** (한 칸씩 밀림) · §3.3 *"Li et al. [182]"* → [182] 는 Wen(CoSe₂) · [13] Rezaei(WiSE MD)를 **SSE 불연성·기계강도**(p.2) 와 **덴드라이트 원인**(p.3) 근거로 · [12] Park(비지도 ML)을 *"SSE 관심 증가"* 근거로 · `Fig. 17c` 본문 [223] ↔ 캡션 [222] · 참고문헌 [182]·[194] 저자란에 *"University, W"* · *"University, U"* (서지관리 산물).
- ⑯ **`Table S1` "62편"** — #25 와 #38 이 같은 논문(Zhao *EER* 7, 3 (2024); #38 은 페이지란에 ISSN `2520-8489`) → 최대 61편. 또 표본에 **AI/ML 리뷰 범주가 0개**라 *"AI 가 기존 리뷰에 체계적으로 안 들어갔다"* 는 결론이 표본 구성상 **자명하게** 나온다(✎).
- ⑰ **`Table 2` ↔ 본문** — *"Au·Ag 에서 Li 핵생성 과전압 ≈ 0"* ↔ 표 Ag NP ~25 mV · 전해질·전류밀도가 다른 값을 한 표에서 Na 대 Li 로 비교.
- ⑱ **단위 오류** — *"fracture toughness, reaching **296 MPa**"* [127]: 파괴인성 단위는 MPa·m^½ 이다. 296 MPa 는 강도 단위 → 굽힘강도였을 가능성(✎). 우리 기계 축에 옮길 때 특히 주의. 같은 부류: `Fig. 9` 캡션의 *"X-ray tomography images (**4.66 mm** resolution)"* · SEM *"100 and 10 **mm** scale"* — PDF 원문 글리프도 `mm` 다(µ 글리프 없음 확인). ✎ µm 의 오기로 보인다. 또 `Fig. 9c–e` 캡션은 *"Copyright © 2024, **AAAS**"* 인데 가리키는 [142] 는 Rees 2021 *Angew. Chem.*(Wiley, MRI 논문)이고, 캡션 내용(X-ray 단층·SEM)도 본문 서술(*"MRI … (Fig. 9c-e)"*)과 다르다 — **출처 불일치** (그림 미독 · 캡션·참고문헌 텍스트 기준).
- ⑲ **전도도 범위 자기모순** — ISE 0.1–1 mS cm⁻¹(§4.1) vs NASICON 4.64–4.92(§2.3) vs `Fig. 3` 10⁻³–10⁻² S cm⁻¹; SPE 10⁻³–10⁻¹ mS cm⁻¹(§2.2) vs < 0.01(§4.1) vs `Fig. 3` 10⁻⁵–10⁻³ S cm⁻¹.
- ⑳ **황화물 Na SE 공백** — `Na₃SbS₄`·`Na₁₁Sn₂PS₁₂`·Na-argyrodite 0회. ISE 절은 NASICON·β-alumina 만. 키워드 *"Solid-state electrolytes"* 대비 범위가 좁다.
- ㉑ **ChatGPT 사사** — *"optimizing figures"* 보조를 명시했다. `Fig. 3`·`Fig. 14`·`Fig. 16`·`Fig. 18` 의 모순이 그 과정에서 생겼는지는 **알 수 없다** — 사실로만 적는다.

**판정**: 우리 방법을 **부정하는 대목은 없다**. 오히려 ③④ 는 우리 ESW·gap 규율이 왜 필요한지 보여 주는 **반면교사**다.

---

## 11. 우리 원장 매핑 (요약표)

| 이 리뷰의 대목 | 우리 원장·문서 | 관계 |
|---|---|---|
| ESW >4.5 V (sulfide) · LUMO 문장 | `our_dft_baseline.md` ESW 절 · `comparison_vs_ours.md` §B① · `nolan2018_…` §9-② | 🔴 반대 방향 문장 — 인용 금지, 반면교사 |
| ML 지표(분할 미기재) | `comparison_vs_ours.md` §J-8 (CV 규약 판정) | 같은 질문의 외부 사례 |
| NNP-MD `Na₃PS₄`/Na | `li2026_mci_vs_sei_na3ps4_na_mlip_md` · §J-42 | 현대판이 이미 litdb 에 있다 |
| BV 지형 + ML (Katcho) | `tools/comp1_v3/` BVSE · CLAUDE.md BVSE 규약 | 기술자 선례 — 원전 확보 대상 |
| 입계 밴드갭·전자누설 | `comparison_vs_ours.md` §H | 우리 미계산 항목 상기 |
| Na 계 | `db/properties/` cascade 파일 (Na 는 도펀트로만) | Na 호스트 계산 없음 |
| 방법 원전 블록 | `comparison_vs_ours.md` §J-49 + Reference key `[Gao26SIBRev]` | 신설 |

---

## 12. 적용 인사이트 ★

1. **원고 방어** — *"황화물 전해질은 전기화학 창이 넓다"* 는 문장을 이 리뷰로 받치면 안 된다. 우리 ESW 는 **"층① 열역학 분해 onset (S²⁻ 한계, vs Li⁺/Li)"** 로 **양을 이름 붙여** 인용하고, 겉보기 창은 별개라고 적는 우리 규율이 정확히 이 리뷰의 빈틈을 막는다. (근거 문장은 `nolan2018` §9-②.)
2. **ML 보고 체크리스트의 외부 반례로 쓴다** — ① 분할 단위(점/물질/조성군) ② 클래스 기저율 ③ 전자절연 등 물리 필터 ④ "검증"이 무엇을 확인하는가(phonon DOS ≠ σ). 우리 cascade 문서(§J-8·J-11)를 심사자에게 설명할 때 *"문헌 ML 은 이 네 가지를 흔히 빠뜨린다"* 의 사례.
3. **확보 대상 2편이 우리 도구에 바로 걸린다** — **Katcho 2019** (BV 지형을 ML 기술자로 — 우리 BVSE 채널 % 의 다음 쓰임) · **Bekaert 2023** (NNP-MD 계면 분해의 원조 — `li2026_mci…` 와 짝). 나머지(Kim 2023 NASICON · Pereznieto 2023 · Park 2024 · Ishikawa 2019)는 이 리뷰의 수치를 **원전에서 확인**하려는 용도.

---

## 13. 인용 가능 문장 (영문 초안 — 원전과 함께만)

- *"electrolyte performance in sodium-based systems should be understood through coupled structure–property relationships rather than isolated physicochemical parameters"* (p.19) — 서론 방향 문장. 단독 인용 가능하나 무게가 없다.
- *"key structural features, such as diffusion bottlenecks, channel connectivity, coordination number, and local disorder, consistently emerge as dominant factors controlling ion migration barriers and conductivity"* (p.23) — **Katcho 2019 [210] · Park 2024 [12] 원전을 반드시 같이**.
- *"A fundamental issue is the scarcity and fragmentation of high-quality datasets, which severely constrain predictive reliability and model generalization."* (p.27) — ML 한계 서술. 단독 가능.
- ⛔ 부류별 σ·ESW 범위(§3-C), `Fig. 3`, `Fig. 14` Key Insights, "0.02 eV", "R² 0.97" 은 인용 문장 후보에서 **제외**.

---

## 14. 주의 / 한계 (인용 규율)

- 이 리뷰의 **모든 수치는 2차 인용**이다 — 원전 확인 없이 인용 금지. 특히: ESW ">4.5 V"(sulfide) · 배위에너지 "< 0.02 eV" · R² 0.97 · 흑연 "~2.84 V vs SHE" · "296 MPa fracture toughness".
- **인용 번호를 믿지 말 것** (§10-⑮ — 한 절에서 세 번 밀림).
- **Na 계 → 우리 물성 4축(A–D) 표 진입 금지.** 전위 눈금이 다르다(vs Na⁺/Na · vs SHE ↔ 우리 vs Li⁺/Li).
- 이 digest 의 figure-read 값(`Fig. 3` 레이더 ±0.3 · `Fig. 15a` ≈0.13 eV)은 **저해상도 재수록 래스터**에서 읽었다 — 순서·자릿수만 믿는다.
- 안 본 그림 10장(§머리말)은 이 digest 의 판단 근거가 아니다.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 (이 digest 문맥) |
|---|---|
| **HOMO / LUMO** | 분자의 최고 점유 / 최저 비점유 궤도 **에너지**. 그 간격은 전기화학 창의 **상한**일 뿐 창 자체가 아니다 (Peljo & Girault 2018) |
| **ESW (전기화학 안정창)** | 열역학 정의 = 분해 반응 ΔG 로 정한 환원·산화 한계 (우리 grand-potential, 층①). 실험 겉보기 창 = LSV/CV 의 전류 문턱 — 동역학·부동태 포함 (층②·③) |
| **grand-potential 상평형** | 알칼리 화학퍼텐셜 μ 를 훑으며 평형상을 갱신 → 알칼리 흡수/방출이 0 인 구간 = 안정창. `Na uptake per f.u.` 계단 그림이 이것 |
| **GPE / SPE / ISE** | 겔 고분자 / 고체 고분자 / 무기 고체 전해질 |
| **NASICON** | Na Super Ionic CONductor, `Na₁₊ₓZr₂SiₓP₃₋ₓO₁₂` 계 골격 산화물 |
| **β / β″-alumina** | Al–O 스피넬 블록 사이 Na⁺ 전도면을 가진 층상 산화물 (β″ 가 전도층 2개·c 축 ≈1.5배) |
| **LightGBM / XGBoost** | 그래디언트 부스팅 결정트리 계열 분류·회귀기 |
| **Sobol 분석** | 출력 분산을 입력 특징별 기여로 쪼개는 전역 민감도 지표 |
| **symbolic regression** | 수식 형태 자체를 탐색하는 회귀 (→ t/η 같은 기술자) |
| **Magpie 기술자** | 조성만으로 만드는 원소 통계 특징 세트(평균·편차 등) |
| **GPR** | 가우시안 과정 회귀 — 예측과 불확실도를 같이 낸다 |
| **LASSO / ES-LiR** | L1 정규화 선형회귀 / 전수탐색 선형회귀(기술자 조합을 모두 시험) |
| **CV error** | 교차검증 오차 — `Fig. 15a` 의 x 축 |
| **NNP-MD / MLFF / MLIP** | DFT 데이터로 학습한 신경망·기계학습 원자간 퍼텐셜로 돌리는 MD (우리 UMA 가 이 부류의 범용판) |
| **BV 에너지 지형 / BVSE** | 결합원자가 합의 편차로 이동이온의 퍼텐셜 지형을 근사 — 우리 softBV BVSE 와 같은 계열 |
| **phonon DOS** | 포논 상태밀도 — 동역학 안정성(허수 모드 없음)·격자 연성 지표. σ 를 직접 확인하지 않는다 |
| **tolerance factor t / atomic packing fraction η** | (antiperovskite) 이온반경 기반 구조 안정 지표 / 원자 부피 충전율 |
| **DRT** | 임피던스의 완화시간 분포 분해 |
| **PINN** | 지배방정식(Nernst–Planck·Poisson)을 손실함수에 넣은 신경망 |
| **ELET** | Extremely lean electrolyte testing — 희박 전해질 조건의 표준 사이클 수명 평가 |

---

## 16. 📥 확보 대상 (원전 — 이 리뷰의 수치를 확인하거나 우리 도구에 걸리는 것)

1. **Katcho et al. 2019** *J. Appl. Crystallogr.* 52, 148–157 — BV + ML (우리 BVSE 채널 % 의 기술자 쓰임) · litdb 미보유.
2. **Bekaert et al. 2023** *J. Phys. Chem. C* 127, 8503–8514 — `Na₃PS₄`/Na NNP-MD · litdb 미보유 (`li2026_mci…` 와 짝).
3. **Pereznieto et al. 2023** *Mater. Lett.* 349, 134848 — R² 0.97 의 분할 규약 · `NaPb₃` 갭 필터 여부 확인 (litdb `jain2026_ml_pipelines…` 에 한 줄 언급만).
4. **Kim, Kang, Min 2023** *ACS AMI* 15, 41417 — NASICON 3 573 · 84.2 % 의 레이블·클래스 균형 · DFT/AIMD 조건.
5. **Ishikawa et al. 2019** *PCCP* 21, 26399 — "0.02 eV" vs 그림 0.13 eV 판정.
6. **Park et al. 2024** *npj Comput. Mater.* 10, 226 — Na 12 670 비지도 군집.
7. **Tang et al. 2018** *Chem. Mater.* 30, 163 — `Na₃PS₄` 상평형 원전 (현재 litdb 에는 `li2026_na…` 재수록 그림으로만).
8. (선택) Bertani & Pedone 2025 *JPCC* 129, 12697 (`Na₄P₂S₇` 유리 MLIP 미세조정) · Klarbring & Walsh 2024 *Chem. Mater.* 36, 9406 (W 도핑 `Na₃SbS₄` MLFF) — 이 리뷰가 서론에만 묻어 둔 MLIP 편.

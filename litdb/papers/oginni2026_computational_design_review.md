<!-- digest 표준 양식 (paper-level STANDALONE).
     2026-09-26 초판 (논문 에이전트 · 1저자 = 사용자). 읽기축 = 「일반 계산재료 리뷰가 우리 방법 스택(QE-PBE · UMA MLIP-MD ·
     grand-potential ESW · LOBSTER/BVSE · disorder-ensemble)을 어디에 놓나, 어느 문장을 서론·방법 인용 후보로 쓸 수 있나」.
     ★ 이 리뷰는 argyrodite 를 다루지 않는다 — Li₆PS₅Cl 은 본문에 정확히 **한 번**(§3.6 multi-fidelity 한 문장) 나온다.
     크로핑 그림 7장 **전부 실독**(Fig. 1–7) · 표 5장은 PDF 텍스트로 전사. 그림에서만 읽은 값은 `figure-read ≈`. -->

# Computational design of quantum and functional materials for next generation electronic and energy technologies — Oginni, Ogunsakin, Moshood, Oluwasegun\*, Umukoro & Akanbi (*Next Materials* **13**, 103432 (2026))

> slug `oginni2026_computational_design_review` · DOI `10.1016/j.nxmate.2026.103432` · type `리뷰 (자체 계산 0 · 자체 실험 0 — 전량 2차 인용 · 방법론 개관형)` · PDF `litdb/inbox/0926-1. NextMater_2026_Oginni_Computational_design_quantum_functional_materials_review_MAIN.pdf` (18 pp = 본문 ≈14 pp + refs ≈3.5 pp · **SI 없음** · 그림 **7장** · 표 **5장** · refs **185**) · Received 2026-06-07 · revised 2026-08-26 · accepted 2026-09-02 · online **2026-09-15** · **OA CC BY** · digested `2026-09-26` · status ✅ · 태그 **[외부·리뷰·일반 계산재료·⛔ 물성 4축 아님 · 🔧 서론/방법 인용 후보]**

> elements: Li, Na, P, S, Cl, Zr
> methods: DFT, AIMD, MD, MLIP

> **저자**: Adetoun Adunni Oginni¹ / Oluwakunle Moyofoluwa Ogunsakin² / Monsuru Olanrewaju Moshood³ / **Boluwatife John Oluwasegun**\*⁴ / Emmanuel Ediri Umukoro⁵ / Opeyemi Samson Akanbi⁶ — ¹Univ. of Waterloo 기계·메카트로닉스 · ²Missouri S&T 지구과학공학 · ³Ball State Univ. 수학 · ⁴**LAUTECH(Ladoke Akintola Univ. of Technology, Ogbomoso, Nigeria) 기계공학 — 교신(학생 계정 `bjoluwasegun@student.lautech.edu.ng`)** · ⁵Delta State Univ. 물리 · ⁶LAUTECH 물리. **펀딩 없음**(명시). AI 선언: 문법·교정만. CRediT: Oginni = Investigation·Conceptualization / Oluwasegun = 초고·시각화 / Akanbi = Validation·Supervision.
> 🎤 **관련 발표: 없음** — `litdb/talks/*.md` 인입 대기열(`lee2026_skku_mlip_materials_design.md`)에 이 논문은 **없다**(2026-09-26 grep: Oginni / Oluwasegun / "quantum and functional" **0건**). 역링크 불필요.
> 🖼 **본 digest 에서 실제로 본 그림: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. 7` — 7장 전부.** 표 `Table 1`–`Table 5` 는 이미지가 아니라 PDF 텍스트로 읽었다(관례). 그림에서만 읽은 값은 **`figure-read ≈`**.

---

## 0. 이 digest 를 읽는 법 — 먼저 알아야 할 세 가지

1. **이 편은 우리 계(황화물 argyrodite)를 다루지 않는다.** `Li₆PS₅Cl` 은 본문 전체에서 **한 번**(§3.6, multi-fidelity 학습 예시 한 문장), `argyrodite`·`sulfide` 는 **0회**다. 물성값(σ·Ea·gap·E·ESW)을 이 편에서 가져올 수 있는 것은 **없다** — INDEX 의 **EXTERNAL** 절에 두고, `comparison_vs_ours.md` 에는 **§J-47 방법 원전 블록**으로만 들어간다(물성 4축 A–D 행 **없음**).
2. **값어치는 "서론·방법 절에 인용할 수 있는 일반 문장"** 에 있다 — *DFT(PBE)로 넓게 걸러 필요할 때만 상위 방법* · *MLIP 는 학습 범함수의 편향을 상속한다* · *검증은 힘 오차가 아니라 관측량(σ·D·상전이 T)으로* · *유한크기 효과가 D 와 초이온 전이 T 를 바꾼다* · *ML 은 hull 경계 근처에서 안정/준안정을 잘 못 가른다*. **단 전부 2차 서술**이므로 원고에는 **원전**(Grasselli 2022 · Riebesell 2025 · Kim 2024 arXiv 등)을 붙여야 한다 — §9 에 문장과 원전을 짝지어 뒀다.
3. **참고문헌 위생이 나쁘다.** `Fig. 4` 캡션의 출처 `[103]` 은 종양학 통계 논문이고(GNoME 원전은 `[105]`), MOF 수소저장에 `[157]`(MoS₂ NAMD)을, 데이터셋 편향에 `[182]`(플렉서블 전자 바이오센서 리뷰)를 단다(§10-①). **이 편의 인용번호를 그대로 옮기지 마라** — 원전을 직접 확인한 뒤 인용한다.

---

## 1. 한 줄 요약

전자·에너지 재료용 계산설계 방법을 **DFT → beyond-DFT(TDDFT/GW/BSE) → MD/MC → ML(GNN·MLIP·생성모델·자율실험실) → 양자컴퓨팅(VQE/QPE/하이브리드 임베딩) → 하이브리드(DFT–ML–MD · multi-fidelity · ML–MC)** 순으로 훑고, 그 위에 응용(반도체·2D·스핀트로닉스·플렉서블 / 태양전지·촉매·배터리·전해질) 사례를 얹은 **입문형 지도 리뷰**다. 자체 계산·실험은 0건, 정량 규약(k-점·컷오프·dt·앙상블·MSD 창·불확실도)은 **0줄**. 우리에게 쓸모 있는 것은 (a) 방법 계층·검증·전이성에 관한 **일반 문장 8개**(§9), (b) `Fig. 3a`(Grasselli 2022 재수록)가 주는 **유한크기 점검 압박**, (c) `Li₆PS₅Cl` σ 를 multi-fidelity(PBE+SCAN/r²SCAN) MLIP 로 *"10 % 이내"* 재현했다는 **arXiv 한 줄**(원전 확보 대상)이다.

---

## 2. 메타 / 리뷰가 스스로 그은 범위

| 항목 | 내용 |
|---|---|
| 저널 | *Next Materials* (Elsevier, 2949-8228) **13**, 103432 — OA 신생 저널(2023 창간) |
| 주장하는 차별점 (p.2–3) | *"Unlike previous reviews that commonly examine individual computational approaches or specific material classes, this review evaluates computational materials design as an **integrated, property-driven hierarchy**"* — 정확도·비용·확장성·응용 적합성의 관계 + DFT/beyond-DFT 와 MD·MC·ML·QC 의 결합 + 소자 지향 설계로의 전환 |
| 범위 안 | 양자재료(위상·강상관·저차원·양자정보) + 기능재료(나노·반도체·자성·스마트·바이오·에너지·산화물·MOF·페로브스카이트) 전반의 **계산 방법** |
| 범위 밖 (사실상) | 특정 계 심층 분석 · 방법 파라미터 · 벤치마크 수치 · 실험–계산 정량 대조. **배터리는 응용 §4.2.3 의 두 단락**(Na 양극·Li₂ZrCl₆·NaMOCl₄·NASICON) |
| 자체 계산 / 실험 | **0 / 0** |
| 그림 | 7장 — `Fig. 1`·`Fig. 2` 저자 자작 개념도, `Fig. 3`–`Fig. 7` 전부 **재수록**(refs 91·85·105·158·178·179) |
| 표 | 5장 — 전부 정성 비교표(`Table 2` DFT 범함수 5행 · `Table 3` TDDFT/GW/BSE · `Table 4` QC 4법 · `Table 5` 7법 종합) |
| 구조 | 1 Intro → 2 Overview(2.1 QM · 2.2 FM) → **3 Methods**(3.1 DFT · 3.2 Beyond-DFT · 3.3 MD&MC · 3.4 ML · 3.5 QC · 3.6 Hybrid) → 4 Applications(4.1 Electronic · 4.2 Energy) → 5 Challenges → 6 Conclusion |

**저자 진영**: 계산재료 전문 그룹이 아니다(기계·수학·지구과학·물리 학과 6인, 3대륙). 자체 계산이 없는 이유이자, 서술이 교과서 수준에 머무는 이유다. 공저자 자기인용이 3건(`[7]` 착용형 센서 리뷰 · `[12]` *JPCL* 미니리뷰 · `[29]` 위상 양자컴퓨팅 리뷰) 있다.

---

## 3. 절별 내용 정리 (본문 순서 · 모든 수치 포함)

### 3-1. §1 Introduction — 문제 설정

- 동기: 고효율 태양전지·양자배터리·저전력 스핀트로닉스·차세대 저장장치가 요구하는 물성 공간이 넓어 **시행착오 실험이 못 따라간다** → 계산설계가 "pivotal paradigm".
- DFT 의 한계 3개를 미리 못박는다: **밴드갭 과소평가 · 강상관계 · 장거리 분산/전자상관 기술 부족** → beyond-DFT(TDDFT·GW·BSE)로 넘어가는 서사.
- ML(ANN·GNN·생성모델·MLIP) + 양자컴퓨팅(변분 알고리즘)의 융합을 `Fig. 1` 로 그린다.
- **기존 리뷰와의 차별**: 방법이 따로따로 논의돼 "어느 방법이 언제 적절하고 어떻게 서로 보완하나" 를 판단하기 어렵다는 지적 — 이 리뷰는 그것을 **정확도–비용–확장성–응용 적합성** 축으로 통합하겠다고 한다.

### 3-2. §2 Overview — 양자재료 · 기능재료 카탈로그

- **§2.1 양자재료(QM)**: Goyal et al.`[3]` 정의(양자구속·강상관·위상·대칭이 거시 물성을 결정). 분류 4종 — 위상재료(TI·Weyl/Dirac 반금속·위상초전도체), 강상관(큐프레이트·중페르미온·양자스핀액체), 저차원/양자구속(QD·나노선·그래핀·TMD), 양자정보재료(NV 센터·초전도회로·스핀결함·위상큐빗). 이정표로 **1986 큐프레이트 고온초전도** 발견. `Table 1` 이 4가지 성질(양자구속 / 강상관 / 위상·대칭 / 구동·비평형 동역학)을 개념·기원·현상·응용으로 정리 — 정성표.
- **§2.2 기능재료(FM)**: 외부 자극(전기·자기·온도·압력·빛)에 능동 응답하는 재료. `Fig. 2` 8분류(나노재료·반도체·자성·스마트·바이오·**에너지**·금속산화물·MOF). 각 단락은 카탈로그다 — 그래핀/CNT(전도·열·기계), 산화물 TiO₂/ZnO/NiO/Fe₃O₄(광촉매·광전자·센서·ETL), 할라이드 페로브스카이트(가변 갭·강흡수·긴 확산길이·결함 내성), MOF(기공·표면적 → 가스저장·CO₂ 포집·촉매·센싱), 에너지 저장(Li/Na 이온·연료전지·슈퍼커패시터 — *"높은 이온전도도·구조 안정성·전기화학 성능"* 을 전극·전해질 요구조건으로 한 줄).
- 우리에게 남는 것: **없음**(어휘 확인용). 단 `Fig. 2` 에너지 칸의 세 키워드 *"High energy density · Ion transport · Electrochemical stability"* 가 우리 축 A(이온전도)·B(산화안정)와 이름이 겹친다는 정도.

### 3-3. §3.1 DFT — 범함수 선택이 "정확도–비용–확장성 트레이드오프" 의 핵심

- 이론 기반: Hohenberg–Kohn(밀도 n(r) 3좌표로 환원). *"practical performance depends strongly on the exchange-correlation functional"*.
- **범함수 지도** (`Table 2`, 원문 그대로 전사):

| Approach | Strength | Main limitation | Suitable applications |
|---|---|---|---|
| PBE/GGA | Low cost, scalable | **Band-gap and correlation errors** | Screening, structures, stability |
| DFT+(U) | Better localized (d/f) states | Depends on (U) | Oxides, magnets, batteries |
| Meta-GGA | Improved semilocal accuracy | Higher cost than GGA | Property refinement |
| HSE06 | Improved band gaps | High computational cost | Semiconductors, photovoltaics |
| DFT-D / vdW | Improved dispersion description | **Method-dependent** | 2D materials, interfaces, adsorption |

- 본문 보충: PBE-GGA 는 구조최적화·형성에너지·상안정·결함·흡착·HT 스크리닝에 표준 `[51]`; *"systematic underestimation of semiconductor band gaps and limitations for localized (d/f) electrons and long-range interactions"*; DFT+U 는 전이금속 산화물·자성·**배터리 전극**에 싼 개선 `[52]`; HSE06 은 밴드 가장자리·갭 개선하나 비용 큼 `[53]`; 분산보정은 층상·흡착·분자결정·**계면** `[54]`.
- **DFT 가 내는 서술자 목록**: *"band structures, density of states, formation and defect energies, diffusion barriers, elastic properties, and adsorption energies"* — 구조를 기능에 잇는 것이 스크리닝의 본질이라는 논지. 사례: TiO₂/ZnO/BiVO₄ 광촉매 `[42]`, MXene 이온확산 장벽·흡착 `[58]`, MOF 전기화학 저장 `[46,59]`, 폴리피롤 복합체(DFT+TD-DFT 갭 감소·π 비국재화) `[60]`, 촉매 흡착에너지 + 스케일링 관계 + Sabatier(HER/OER/ORR/CO₂RR) `[61]`.
- **한계 = 확장성**: 계 크기·후보 수에 따라 비용 급증 → HT-DFT + ML(DFT 를 고충실도 학습데이터로) `[62,63]`. DFT 는 바닥상태 방법이므로 준입자·여기상태·전자–정공은 beyond-DFT 로.
- 🔑 **전략 문장**(§9-②): *"an efficient computational strategy uses DFT for broad structural and energetic screening, higher-level DFT approaches for selected candidates, and more computationally demanding excited-state methods only when the target property requires them."*

### 3-4. §3.2 Beyond-DFT — TDDFT · GW · BSE 는 "정확도 사다리" 가 아니라 "다른 물리 문제"

- 핵심 프레이밍: *"Rather than representing interchangeable levels of accuracy, TDDFT, GW, and BSE address different physical problems"* — TDDFT = 시간의존 응답, GW = 준입자 에너지 보정, BSE = 전자–정공(엑시톤).
- **TDDFT**(§3.2.1): 여기에너지·광스펙트럼·전자동역학 `[67,68]`; 비용 대비 유리; 약점 = 장거리 전하이동 여기·이중여기·원뿔교차·일부 코어 여기 `[69,70]`. 최근 **유전 스크리닝 하이브리드 TDDFT** 가 **Si·GaN·LiF** 에서 BSE 급 정확도 + 엑시톤 분산·손실함수 `[72]`.
- **GW**(§3.2.2): KS 고유값 ≠ 준입자 첨가/제거 에너지 → 갭 과소평가의 근원 `[64,73,74]`; 자기에너지 Σ = GW. 잘 수렴된 반도체에서 갭 오차 **"order of tens of meV"**(SOC·상대론 처리 시) `[76]`. 민감도: **출발 전자구조 · 빈 밴드 수렴 · 유전 스크리닝 · k-점 · SOC** `[76,77]`. HT GW-BSE 자동화 시작(pyGWBSE `[64]`). 2D·양자나노구조에서 실험과 우수 일치 `[78,79]`.
- **BSE**(§3.2.3): 엑시톤 결합에너지·흡수 스펙트럼·미세구조 `[66,75,80]`; 저차원·분자·페로브스카이트 광전자재료에 필수 `[77,81,82]`. 비용 최대(GW 위에 얹음); 정적 스크리닝·**Tamm–Dancoff** 근사에 의존 `[80,83]`. 스케일 사례: **qsGW-BSE, ≈2,000 상관전자 · >11,000 기저함수** 발색단 `[84]` — 그래도 HT 부적합.
- `Table 3` 요약: 비용 TDDFT(최저) < GW(높음) < BSE(최고). 적용: TDDFT = 분광·동역학·결함·광학재료 / GW = 반도체·2D·페로브스카이트·양자재료 / BSE = 2D·페로브스카이트·분자·광전자.
- 우리에게: **전부 해당 없음**(우리는 gap 을 정성 "wide-gap" 으로만 쓴다). 다만 §3.1+§3.2 의 *"GW 는 갭이 결정적인 선별 후보에만"* 논리는 **우리가 HSE/GW 를 안 한 이유**를 쓸 때 인용할 수 있다(§7-②).

### 3-5. §3.3 MD & MC — "어떻게 움직이나" vs "어느 배열이 유리한가"

- 역할 분담: MD = 확산·열수송·계면·열화(궤적) / MC = 상안정·배열·편석·결함 분포(배열 표본) `[85,86]`.
- **고전 MD vs AIMD**: 고전 = 확장성·큰 계·긴 시간, 그러나 퍼텐셜 품질 의존·결합 파괴/반응 불가 `[87–89]`; AIMD = 화학 재배열·열활성 구조 거동에 충실, 그러나 **작은 계·짧은 궤적** `[86,90]`.
- 🔑 **유한크기 사례**(`Fig. 3a`, ref `[91]` = Grasselli, *J. Chem. Phys.* **156**, 134705 (2022)): *"MD simulations of superionic conductors showed that **finite-size effects can significantly influence calculated diffusion behavior and transition temperatures**"* — 셀을 키우면 D 가 바뀌고 초이온 전이 T 가 이동한다 → *"importance of carefully selecting simulation dimensions"*.
  - `figure-read ≈` PbF₂·CaF₂·UO₂ 세 형석형 계에서 **N = 12**(초록) 셀은 저온에서 D 가 **큰 셀보다 1–2 자릿수 높게** 남는다(PbF₂, 10³/T = 2.0: N=12 ≈ 10⁻¹ · N=96 ≈ 10⁻² · N=324/768 ≈ 10⁻³ Å² ps⁻¹). 전이 T 표지(점선)가 N 에 따라 이동(PbF₂ ≈ 10³/T 1.05 → 1.17 → 1.25 K⁻¹, 즉 ≈950 → 855 → 800 K). **α-AgI 패널(N = 32–864)은 다섯 크기가 한 선에 겹친다 = 크기효과 없음** — 본문·캡션이 이 대조를 **언급하지 않는다**(§10-②).
- 반응성 MD 로 전해질 열화·배위환경 변화 해석 `[92]`.
- **MC**: 배열공간 표본추출; 합금 정렬·상안정·편석·결함배열·배열 엔트로피; DFT·클러스터 전개·MLIP 와 결합 `[93–96]`. 사례 `Fig. 3b`(ref `[85]` = Menon/Poul/Hickel/Neugebauer/Drautz, arXiv 2607.14795): 명시적 배열 표본추출이 **Au–Cu 정렬–무질서 전이를 ≈810 → 710 K** 로 끌어내려 **실험 683 K** 에 접근. `figure-read ≈` 그림 인쇄값은 **818 K(no swap) → 721 K(MC swap), ΔT = −97 K**; 자유에너지 −4.65 ~ −5.00 eV/atom, 400–1000 K, 곡선 3개(AuCu 실선 / FCC-MD / FCC-MCMD 점선). ML 퍼텐셜 + MC 로 고엔트로피 합금 결함배열 탐색 `[96]`. 한계: **실시간 동역학 없음 · 상전이 근처 임계 감속** `[97]`.
- 🔑 결론 문장(§9-⑦): *"MD and MC should not be viewed as competing methods. MD is preferable when the central question concerns how atoms move… whereas MC is preferable when the question concerns which configurations are thermodynamically favored."*

### 3-6. §3.4 ML — 가속층, 그러나 "학습 도메인 안에서만"

- 데이터 기반: **Materials Project · OQMD · AFLOW** `[14,101]`.
- 알고리즘: 선형·트리·RF·SVM·NN 여전히 유용; **GNN** 이 결정구조 표현에 자연스럽다 `[102–104]`(⚠ `[103]` 은 종양학 통계 논문 — §10-①).
- **GNoME**(`Fig. 4`, 원전 Merchant et al. *Nature* 624, 80 (2023) = `[105]`; ⚠ 캡션은 `[103]`): GNN + 능동학습으로 "millions of candidate crystal structures"; §4.2.1 에서 **≈2.2 million** 안정/hull 근접 구조. 워크플로 = ML 예측 → 계산 필터 → DFT 평가 → 실험 검증의 반복.
  - `figure-read ≈` `Fig. 4b` 안정물질 수: 외부 DB ≈ 2.8–4.8×10⁴(2019–2020) → GNoME ≈ **3.8×10⁵**(2022 말). `Fig. 4d` 안정 예측 정밀도: **원소 3종** 조성에서 MP 학습 ≈ 10 % vs GNoME ≈ 80 %, **원소 6종**에서 MP < 1 % vs GNoME ≈ 50 %. `Fig. 4e` 도메인 밖 MAE: MP 데이터 ≈ 300 → 90 meV/atom(10³–10⁵ 학습점) · GNoME ≈ 70 → **≈30 meV/atom**(10⁷). `Fig. 4c` 예시 6종: K₂BiCl₅ · Li₄MgGe₂S₇ · Mo₅GeB₂ · KV₃Se₃ · Rb₂HfSi₃O₉ · Tm₅Pd₉P₇. ⚠ `Fig. 4a` 상자 "2.2 million stable structures" 와 `Fig. 4b` 막대 ≈3.8×10⁵ 는 **다른 양**(hull 위 vs hull 근접 포함)인데 리뷰는 구분 없이 "2.2 million" 만 쓴다.
  - 경고: *"the advantage of ML is greatest within the chemical domain represented by its training data; prediction errors can increase substantially for unfamiliar compositions, defects, surfaces, or bonding environments."*
- **MLIP**: GAP · Deep Potential 이 DFT 에너지·힘을 근사 → AIMD 보다 큰 계·긴 시간 `[107,108]`(⚠ `[108]` = Kim et al. *Nat. Commun.* 17, 3432 (2026) "Optimizing cross-domain transfer for **universal** MLIPs" 인데 본문은 이를 범용 모델 논의에 쓰지 않는다). 사례: Fe 전위·파괴 `[110]`, 고엔트로피 배열 표본 `[109]`; **전이성이 주된 한계**. *"ML does not simply make calculations faster; it can change the accessible length, time, and configurational scales."*
- **생성·역설계**: VAE·GAN·RL `[107,111,112]`; 능동학습·자율 워크플로. 생성 후보는 열역학 안정성·합성 가능성·분포 밖 거동이 보장되지 않아 **물리 검증 필수**(이 문장이 한 단락 안에 **두 번** 반복 인쇄됨 — 교정 누락).
- **파운데이션 모델** `[113]`(Pyzer-Knapp 2025): 물성예측·합성계획·분자생성으로 확장, 그러나 데이터 가용성·품질·다양성에 제약 — *"small structural or compositional changes can strongly affect material properties"*.
- **자율실험실 A-Lab** `[114]`(Szymanski 2023): **17일 연속 가동, 목표 57종 중 36종 합성**, 실패 후 능동학습으로 합성법 개선.
- 결론: ML 은 **대체가 아니라 보완** — DFT(전자·에너지) / MD(유한온도 동역학) / MC(배열 열역학) 의 가장 비싼 단계를 ML 이 가속.

### 3-7. §3.5 양자컴퓨팅 — "표적 보완재", 일반 가속기 아님

- 강점 영역 = 강상관·다참조 전자계. 현 하드웨어 제약: 잡음·측정 오버헤드·회로 깊이·큐빗 수 `[1,13,115]`.
- `Table 4`: **VQE**(근시일 NISQ 적합; 측정·최적화 오버헤드; 작은 활성공간) / **QPE**(원리상 고정확; 깊은 내결함 회로 필요; 미래) / **하이브리드 임베딩**(강상관 부분공간만 양자처리; 가장 유망) / **Quantum+ML / QSCI**(희소 상관상태; 양자 표본 품질 의존).
- 사례: ADAPT-VQE(회로 깊이·측정 감소) · **folded-spectrum VQE 로 H₂·LiH 여기상태** `[117]` · **DFT+DMFT on IBM 하드웨어, 큐프레이트 Ca₂CuO₂Cl₂, 최대 14 큐빗** `[122,123]` · Hubbard 모델 금속–Mott 전이 재현 · **Fe–S 클러스터 밀리하트리 정확도** `[115,124]`.
- 판정: *"quantum computing has not yet become a general accelerator for materials discovery"*; ML 은 학습 후 수백만 예측을 싸게 내지만 QC 는 **계산 하나에도 큰 자원**.
- 우리에게: **해당 없음.**

### 3-8. §3.6 하이브리드 모델 — ★ 우리 방법 스택과 가장 가까운 절

- **DFT–ML–MD**: DFT 참조 에너지·힘 → MLIP → **10⁴–10⁶ 원자 · ns** 스케일. 사례: 능동학습 MLIP 로 **비정질 Li₃PS₄/Li₃B₁₁O₁₈ 계면**(Wang/Aykol/Mueller 2023 `[139]`) · DFT 학습 퍼텐셜로 **Li₂CO₃ 계 SEI 의 Li 확산 기전** `[138]`.
- **Multi-fidelity DFT–ML** `[140]`(= Kim et al., arXiv 2409.07947, "Data-efficient multi-fidelity training for high-fidelity MLIPs"): 다량 저비용 **PBE** + 소량 고충실 **SCAN / r²SCAN**. 🔑 *"In **Li₆PS₅Cl**, this strategy predicted Li-ion conductivity **within 10 % error**, while an InₓGa₁₋ₓN study reproduced mixing energies with **R² = 0.98** using a high-fidelity dataset only about **10 %** the size of the low-fidelity dataset."* — **이 리뷰가 우리 물질을 호명하는 유일한 문장.** ⚠ "10 % 오차" 의 기준(실험? 고충실도 MD?)을 리뷰는 말하지 않는다 → 원전 확보 전 인용 금지(§10-⑥·§11).
- **사전학습·증류**: 사전학습 **MACE** 를 미세조정 후 더 작은 신경 EOS 퍼텐셜로 **증류, 추가 DFT 수백 개** `[142]`; 능동학습 **GAP for a-Si₃N₄: MAE ≈ 8 meV/atom, MD 3–4 자릿수 가속** `[141]`.
- **DFT–AIMD**: 겔 고분자 전해질 계면 산물 규명 `[145]` · **LiPON** AIMD 로 DFT 이동장벽 ↔ 유한온도 수송 연결 `[144]` · 준고체 전해질 Li⁺ 용매화 `[143]` · **Li–S 계면 전하이동**(황화물 SE + 이온성 액체, DFT+AIMD) `[146]`.
- **ML–MC · ML–클러스터전개**: 희소 클러스터전개가 **학습셋 >50 % 감축 · ≥3× 빠른 표본추출** `[135,137,147]`.
- 🔑 **한계 = 오차 상속·전이성**: *"ML models **inherit biases from the DFT functional used for training** and may become unreliable for defects, interfaces, highly distorted structures, or chemical environments outside the training domain"* `[136,138]`. 능동학습이 대응 `[148,149]`.
- 🔑 **검증 관행**: *"recent studies increasingly **validate hybrid models against downstream observables rather than energy and force errors alone**, including ionic conductivity, phase-transition temperatures, diffusion, and electronic properties"* `[137,140,150]`.

### 3-9. §4.1 응용 — 전자재료

- **4.1.1 스크리닝·전자구조**: HT-DFT 가 구조안정·형성에너지·**탄성**·**포논 안정성**을 1차 필터로 `[151,153]`; ML 로 수천 후보 저비용. 사례: **≈700 종 2D 반도체의 G₀W₀ 급 밴드구조를 ML 로**(스칼라 갭이 아니라 분산 전체) `[154]`. 한계: 데이터 표준화·학습량·화학적 신계 외삽.
- **4.1.2 결함·계면·수송**: 결함 형성에너지·전이준위·재결합·이온 이동장벽이 실용성을 결정 `[156]`; ML 로 **>100 종 미탐색 도펀트–결함 구조**(층상 칼코게나이드·질화물·할라이드) `[156]`. **ML-NAMD of defective MoS₂: 수천 원자·ns** — 결함이 캐리어 포획·재결합을 지배, 경로가 결함농도·캐리어/결함 비에 비선형 `[157]` → *"a favorable band structure does not necessarily translate into efficient carrier transport"*.
- **4.1.3 광학·플렉서블**: `Fig. 5` — DFT + GNN(ALIGNN 임베딩) + **Cauchy 모델** n(λ)=A+B/λ²+C/λ⁴ 로 **>1,000 TMD 단층**의 NIR 굴절률 `[158]`; **Bi₂Te₂Se** 고굴절 후보; 분광 검증. `figure-read ≈` A,B 계수 패리티 **Train RMSE 0.015 / Test RMSE 0.069**; WSe₂ DFT n ≈ 4.2–5.2(400–2000 nm) vs 모델 ≈ 3.8–4.7(700–1100 nm 창) vs 비교모델 GNNOpt ≈ 1.4–3.0(크게 과소). OLED: **160만 분자 가상탐색 → TDDFT >40만 → 합성 EQE 22 %** `[159]`; 투명 OLED 양극: ML+DFT 일함수 오차 **0.20 eV**, 후보 2D 재료 σ **>10⁶ S m⁻¹**, 투과율 **>90 %**, WF **>5 eV** `[160]`.
- **4.1.4 양자·스핀트로닉스**: 자성·SOC·밴드 반전·상관상태가 근사에 민감 → DFT/ML 1차, **하이브리드·GW 로 검증** `[152,161]`; Bi₂Se₃ 밴드 반전; **QMC** 가 MoS₂·CrI₃·VSe₂·그래핀계의 검증 필요성 강조 `[152]`; 양자어닐링/ML/제일원리로 스피넬 산화물 MTJ 장벽 무질서 최적화 `[162]`.

### 3-10. §4.2 응용 — 에너지재료 (★ 우리 축이 걸리는 곳)

- **4.2.1 HT·AI 발견**: GNoME ≈ **2.2 million** hull 근접 구조; **Alexandria** `[163]` · **InvDesFlow-AL** `[164]`. 🔑 **경고**: *"scale does not automatically guarantee predictive reliability. Recent benchmarking has shown that **ML models can struggle to distinguish stable from metastable structures near the convex-hull boundary**"* `[165,166]`(= Riebesell, **Matbench Discovery**, *Nat. Mach. Intell.* 7, 836 (2025)) → ML 은 **스크리닝 가속기**, 물리 검증의 대체 아님.
- **4.2.2 물성 → 기전·소자**: 무연 페로브스카이트 **DFT + SCAPS-1D**(소자 시뮬) `[167–170]`; 이중원자 촉매 CO₂RR 의 ML-DFT `[171–173]`; 광촉매 물분해에 **DFT + NAMD**(정적 밴드 정렬 → 캐리어 분리·재결합) `[174]`. *"computational design increasingly seeks to explain **why** a material performs well."*
- **4.2.3 에너지저장의 동적·다중스케일 설계**: 정적 계산은 부족 — DFT + 전이상태 + AIMD + ML-MD. Na 양극 **양이온 정렬 ↔ Na 이동** `[175,176]`; P2 층상 Mn 산화물 상전이 기전 `[177]`.
  - 🔑 *"The role of dynamic simulations is particularly important for **solid electrolytes, where ionic conductivity depends on collective motion and structural disorder**."*
  - `Fig. 6`(ref `[178]` Guo/Koverga/Selvaraj/Ngo, *ACS Appl. Energy Mater.* 8, 14773 (2025)): **Li₂ZrCl₆ 딥러닝 퍼텐셜** — ordered α / disordered α / β 세 상에서 DP 힘 vs AIMD 힘 패리티. `figure-read ≈` 축 범위 Li ±6 · Zr ±8 · Cl ±24 eV Å⁻¹; 세 상 모두 대각선에 밀착; β-LZC Li 패널 고힘 구간(+3~+5 eV Å⁻¹)에 약한 과대예측 군, disordered α Zr 패널 −6~−8 구간에 산포. **RMSE/MAE 수치는 그림·본문 어디에도 없다** — "정확히 재현" 은 시각 판정이다(§10-③).
  - `Fig. 7`(ref `[179]` Wei/Binci/**Ceder**, *ACS Energy Lett.* 11, 1861 (2026)): **NaMOCl₄ (M = Nb, Ta)** 결정 vs 비정질 Na 확산 아레니우스. `figure-read ≈` (a) c-NNOC: 고온 **0.19 eV** / 중간 **0.42 eV** / 저온 **0.95 eV**, 전이 음영 **550–650 K**, D ≈ 10⁻⁵(800 K) → ≈3×10⁻⁷ cm² s⁻¹(≈475 K); (b) c-NTOC: **0.17 eV** / **1.40 eV**, 전이 **500 K**; (c) 비정질 a-NNOC **0.19 eV** · a-NTOC **0.18 eV**, 300–830 K 에서 **단일 아레니우스**(D ≈ 10⁻⁴ → ≈10⁻⁶ cm² s⁻¹). 본문은 *"structural disorder can facilitate three-dimensional Na-ion diffusion"* 한 줄이고 **Ea 수치는 그림에만** 있다.
  - 치환 설계: **S 치환 NASICON** 이 Na 이동 병목을 넓힘 `[180]`.
  - 슈퍼커패시터·수소저장: MXene 층간 이온성 액체 MD ↔ 미분 커패시턴스 `[181]`; MOF 개방 금속자리 H₂ 흡착·확산 ML 퍼텐셜(⚠ `[157]` 오인용). 결론: *"a material may possess favorable thermodynamic or electronic properties while exhibiting poor transport or unfavorable structural evolution under operating conditions."*

### 3-11. §5 Challenges & Perspectives — 5 테마

| 테마 | 요지 (원문 근거) | 우리 관련 |
|---|---|---|
| **확장성·다중스케일** | DFT/beyond-DFT 비용이 큰·무질서·강상관·계면 풍부 계를 막는다; MLIP 가 **수천 원자·긴 시간** 가속, **GPU 가속 제일원리** 가 계 크기 확장 `[140]`; *"no single method can currently provide accurate and efficient treatment across all relevant length and time scales"* | 우리 UMA-MD(558 원자·200–400 ps)가 정확히 "MLIP 가속 칸" 의 **하단** |
| **데이터 품질·도메인 밖 신뢰성** | 데이터셋의 중복·선택편향·측정 불일치·희귀계 부족 `[182]`; *"increasing dataset size does not necessarily guarantee better extrapolation"*; **UQ · 적용영역 탐지 · 능동학습 · 큐레이션** 필요(⚠ "Recent studies show that conventional evaluation strategies can overestimate out-of-distribution performance" 는 **인용 없음**) | 우리 cascade LODO(§J-8)·UQ 축(§J-18)과 방향 일치 — 근거는 우리 전용편 |
| **설명가능·물리정보 ML** | 블랙박스 정확도 ≠ 기전 통찰 `[183]`; 대칭·보존법칙·물리 제약 내장; 단 물리가정이 틀리면 같이 틀린다 `[184]` | §J-11(SHAP·PFI) 참조 |
| **자율 발견** | 예측–합성–특성–재설계 폐루프; *"greater maturity in identifying synthesizable materials than in establishing long-term functional performance"*; 다목적(안정·효율·내구·비용·독성·제조성)+실험 불확실도 | 해당 없음(우리는 계산 전용) |
| **양자컴퓨팅** | 장기 프론티어; 잡음·큐빗·결맞음·연결성·**barren plateau** `[185]`; *"current evidence does not yet demonstrate predictive quantum simulations of energy materials"* | 해당 없음 |

- 통합 비전: ML(탐색) + 물리모델(제약) + 고충실도 계산(검증) + 실험(피드백)의 폐루프; *"increased computational automation does not come at the expense of physical validity or experimental relevance."*

### 3-12. §6 Conclusion — 요약 재진술(신규 내용 없음)

---

## 4. DFT / 계산 방법 ★ — ⛔ **이 리뷰에는 파라미터가 없다** (전문 검색, 본문 ≈14 pp)

| 항목 | 이 리뷰 | 비고 |
|---|---|---|
| 코드 | **0회** — VASP·Quantum ESPRESSO·CP2K 전문 0(GPAW 는 참고문헌 `[128]` 에만) | 재현 목적 인용 불가 |
| functional | PBE **4회** · HSE06 **3회** · SCAN/r²SCAN **1회** · DFT+U(Hubbard) 1회 — 전부 **정성 서술**(`Table 2`) | 어느 계에 어떤 U 값·어떤 컷오프인지 **0** |
| vdW / 분산 | "dispersion" 6회 · "van der Waals" 2회 — **D2/D3/BJ/TS/MBD 구분 없음**, `Table 2` 에 *"Method-dependent"* 한 마디 | 우리 D3(BJ) 선택의 근거로 **못 쓴다**(방향만) |
| pseudo / PAW | 본문 **0** | — |
| k-points / cutoff | "k-point sampling" **1회**(GW 수렴 인자로) · cutoff **0** · supercell **0** | — |
| DFT+U | 개념 1문장(전이금속 산화물·자성·배터리 전극) | 우리 Nd 는 **frozen-4f** 이지 +U 아님(대조군, `citable:false`) |
| AIMD | 정성: *"small systems and short trajectories"*; **dt · 앙상블 · 열욕 · 시간 길이 전부 0** | Dutra25Rev 는 최소 dt 1–2 fs 를 줬다 — 이 편은 그것도 없다 |
| MLIP | GAP · Deep Potential · **MACE(사전학습 미세조정 1회)** · 증류 · 다중충실도 · 능동학습; **UMA/OMat24 · CHGNet · M3GNet · SevenNet · MACE-MP-0 = 0** | "foundation model" 1회(`[113]`, 재료 일반) |
| **무질서 처리** | **SQS · special quasirandom · enumeration 0회.** 무질서는 (i) MC 배열 표본추출(§3.3) (ii) `Fig. 6` disordered α-Li₂ZrCl₆ 학습 사례 (iii) `Fig. 7` 결정 vs 비정질 로만 등장 | 우리 disorder-ensemble(S/Cl 배열 다중 + 시드)은 이 리뷰 어휘로는 *"explicit configurational sampling"* 에 가장 가깝다 — 단 **볼츠만 가중 여부**를 우리 카드가 선언해야 한다(§7-⑥) |
| 검증·불확실도 | "validation" 어근 15회(전부 정성) · **uncertainty 2회**(§5 한 문장) · **error bar · seed · MSD · Haven · Nernst–Einstein · Arrhenius(1회, `Fig. 7` 캡션) · RDF · Green–Kubo 전부 0** | 우리 MSD 2–50 ps 창·3-시드·NE(Haven=1) 규약의 외부 근거로 **못 쓴다** |
| 후처리 어휘 | *"band structures, density of states, formation and defect energies, diffusion barriers, elastic properties, adsorption energies"* 한 줄(§3.1) · "phonon stability" 1회(§4.1.1) · **COHP · Bader · ELF · BVSE · LOBSTER 0** | 우리 ICOHP·BVSE 는 이 리뷰 지도 밖(Dutra25Rev 와 동일 판정) |

> 🔑 **판정**: 방법 재현·규약 근거 목적으로는 **인용할 것이 없다.** 쓸 수 있는 것은 §9 의 **방향 문장**들이다.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | 저자 자작 개념도 — 중앙 "Computational Materials Design" 을 6 상자(DFT 바닥상태 / Beyond-DFT TDDFT-GW-BSE / Atomistic Simulation MD&MC / Machine learning GNN·ML potentials·active learning / Quantum Computing) 가 원형으로 감싸고, 바깥에 응용 5종(wearable · electronics · photovoltaics · energy storage · fuel cell H₂). ⚠ 그림 안에 **"Exicted States" 오타 + 워드프로세서 맞춤법 밑줄(붉은 물결선)** 이 그대로 인쇄됨 | 서론 슬라이드용 "방법 지형" 참고 이상은 없음. 제작 품질 표지(§10-④) |
| 2 | 기능재료 8분류 원형 인포그래픽(나노재료 · 반도체 Si/GaN/InP/페로브스카이트 · 자성 Fe₃O₄/NiO/CoFe₂O₄ · 스마트 · 바이오 · **에너지(배터리·슈퍼커패시터·연료전지·태양전지 — "High energy density · Ion transport · Electrochemical stability")** · 금속산화물 TiO₂/ZnO/NiO/Fe₃O₄ · MOF) | 어휘 확인용. 에너지 칸 키워드 셋이 우리 축 A·B 이름과 겹친다는 정도 |
| **3a** ★ | **유한크기 효과**(Grasselli 2022 재수록): PbF₂·CaF₂·UO₂·α-AgI 의 D(Å² ps⁻¹, 로그) vs 10³/T. 형석형 3계는 N=12/96/324/768 셀에서 **작은 셀이 저온 D 를 1–2 자릿수 과대** + 초이온 전이 표지(점선)가 N 에 따라 이동(`figure-read ≈` PbF₂ ≈950 → 855 → 800 K). **α-AgI(N=32–864)는 크기 무관하게 한 선** — 캡션은 "fluorite-structure" 라 하지만 AgI 는 형석형이 아니고, 본문은 이 null 결과를 언급하지 않는다 | 🔴 **우리 UMA-MD 558 원자 상자의 D·Ea 에 셀-크기 수렴 기록이 있는가** 를 묻는 그림. 없으면 §H 정직목록 후보(§7-③). 원전 Grasselli 2022 *JCP* 156, 134705 확보 대상 |
| 3b | AuCu 정렬–무질서 전이: 자유에너지(eV/atom) vs T(400–1000 K), 곡선 3개(AuCu / FCC-MD / FCC-MCMD). 명시적 MC 배열 표본추출로 교차점 **818 → 721 K(ΔT = −97 K)**, 실험 683 K. 본문은 "≈810 → 710 K" 로 반올림 | "배열 표본추출이 없으면 전이 T 를 100 K 과대" — 우리 disorder-ensemble 의 **필요성** 을 말하는 외부 사례(계는 합금). 개념 인용만 |
| 4a–e | GNoME(Merchant 2023) 재수록: (a) 구조/조성 파이프라인 → GNN 안정성 → DFT → DB(에너지모델 · **2.2 million** · 퍼텐셜) + 능동학습 루프 (b) 연도별 안정물질 수(외부 DB ≈3–5×10⁴ → GNoME `figure-read ≈` 3.8×10⁵) (c) 예시 6종 구조 (d) 안정예측 정밀도: 원소 3종 MP ≈10 % vs GNoME ≈80 %, 원소 6종 <1 % vs ≈50 % (e) 도메인 밖 MAE 30–300 meV/atom vs 학습셋 10³–10⁷. ⚠ 캡션 출처 `[103]` 오기(정답 `[105]`) | 우리 cascade 의 hull 컷·다중충실도 층(§J-10·J-12) 논의에서 **"규모 ≠ 신뢰성"** 과 **hull 경계 정밀도** 의 문헌 그림. 수치는 GNoME 원전에서 다시 확인 |
| 5a–c | TMD 단층 NIR 굴절률 ML(Klimova 2026): ALIGNN 임베딩 → MLP → Cauchy 계수; 패리티 Train RMSE 0.015 / Test 0.069; (b) WSe₂ (c) WS₂ 의 DFT n ≈4–5 vs 모델 ≈3.7–4.7 vs GNNOpt ≈1.4–3 | ⛔ 우리 축 아님(광학). "사전학습 GNN 임베딩 + 소형 헤드" 구조만 방법 어휘로 |
| **6** ★ | **Li₂ZrCl₆ DP 힘 패리티**(Guo 2025): 3×3 = {ordered α, disordered α, β} × {Li ±6, Zr ±8, Cl ±24 eV Å⁻¹}, DP vs AIMD. 대각선 밀착; 약한 이탈(β-Li 고힘 과대 · disordered-α Zr 음의 고힘 산포). **오차 수치 없음** | 우리 §J-1(UMA 힘 정확도 실측)과 **같은 종류의 그림**. 이 리뷰 자신이 §3.6 에서 *"힘 오차만으로 검증하지 말라"* 고 쓰고는 검증 그림으로 힘 패리티만 실었다 — 우리 원고에서 힘 패리티 그림을 낼 때 **RMSE 수치 + 관측량 검증을 같이** 내야 하는 반면교사 |
| **7a–c** ★ | **NaMOCl₄ 결정 vs 비정질 Na 확산 아레니우스**(Wei/Binci/Ceder 2026): `figure-read ≈` c-NNOC 0.19/0.42/0.95 eV(전이 550–650 K) · c-NTOC 0.17/1.40 eV(전이 500 K) · a-NNOC 0.19 · a-NTOC 0.18 eV 단일 기울기(300–830 K). D ≈10⁻⁴–10⁻⁷ cm² s⁻¹ | 🔑 **"무질서 → 저온 초이온 상태 유지(꺾임 없는 아레니우스)"** 의 문헌 그림. 우리 Cl-rich disorder 서사의 **개념 대응물**(계는 Na 옥시클로라이드 · 값 이식 금지). ⚠ Ea 는 그림에만 있고 본문에 없다 — 인용 시 원전 `[179]` 로 |
| Table 1 | 양자재료 성질 4행(양자구속 / 강상관 / 위상·대칭 / 구동 비평형) 개념·기원·현상·응용 | 없음 |
| Table 2 | DFT 범함수 5행(PBE/GGA · DFT+U · Meta-GGA · HSE06 · DFT-D/vdW) 강점·한계·적용 | **우리 PBE 선택을 "screening, structures, stability" 칸으로 위치짓는 인용 후보**(§9-①). vdW 는 "method-dependent" 뿐 |
| Table 3 | TDDFT/GW/BSE 목표·강점·한계·비용·적용 | 우리 미사용 — "왜 안 했나" 답변용(§7-②) |
| Table 4 | QC 4법(VQE·QPE·하이브리드 임베딩·Quantum+ML/QSCI) | 없음 |
| Table 5 | 7법(DFT·TDDFT·GW·BSE·MD·MC·ML/AI·QC) 목적·정확도·비용·강점·한계·응용·참고 | 슬라이드 1장짜리 "방법 지형표" 원형 — 단 참고열이 부실(§10-①) |

---

## 6. Post-processing ★ — 리뷰가 다루는 것 / 다루지 않는 것

- **다루는 것(이름만)**: 밴드구조 · DOS · 형성/결함 에너지 · **확산 장벽**("transition-state calculations" 로 표현, NEB 라는 이름은 없음) · 탄성 · 흡착에너지 · 포논 안정성(1회) · convex hull(1회, Matbench 문맥) · 아레니우스(그림 캡션 1회) · 스케일링 관계·Sabatier(촉매).
- **다루지 않는 것**: **COHP/ICOHP · Bader · ELF · BVSE · grand-potential/ESW · 상 도표(phase diagram) 계산 · 계면 반응에너지 · MSD 분석 · Haven/NE · Green–Kubo**. 도구명(pymatgen · VESTA · LOBSTER · ASE) **0**.
- **수치화·플롯·기록 관행**: 논의 없음. 그림은 전부 재수록이라 "어떻게 그렸나" 를 리뷰가 말하지 않는다.
- ⇒ 우리 §B(grand-potential onset) · ICOHP · BVSE 는 **이 리뷰 지도 밖**이다. `[Dutra25Rev]`(J-24)와 같은 판정 — *"이 두 리뷰가 안 다룬다"* 까지만 말할 수 있고 *"아무도 안 한다"* 는 아니다.

---

## 7. 우리 기준선 대비 — **수치 비교가 아니라 방법론 지형 대비** (`our_dft_baseline.md` · CLAUDE.md §데이터 규율)

> ⛔ 이 표에는 우리 값도 문헌 값도 **놓지 않는다**. 이 리뷰에 비교할 물성값이 없다.

| # | 항목 | 이 리뷰의 서술 | 우리 캠페인 | 위치 / 차이 / 판정 |
|---|---|---|---|---|
| ① | **범함수 · vdW** | PBE/GGA = *screening, structures, stability*; 갭·상관 오차; HSE06 = 갭 개선·고비용; Meta-GGA = 정제; DFT-D/vdW = 층상·계면·흡착, **"method-dependent"** | **QE · PBE**(`SLA PW PBX PBC`, comp1 gap 실행 `ecutwfc 60 / ecutrho 480 Ry`, `K_POINTS 8 8 2`) · **+D3(BJ) 2체**(W_ad 슬랩, ATM 별도 · `D-2026-09-23-wad-d3-twobody-atm-separate`) · 도펀트 Nd 는 **frozen-4f**(+U 아님) | ✅ **정합** — 우리는 리뷰의 "PBE 칸" 에 정확히 앉는다. 갭은 리뷰가 경고하는 그 과소평가 사례라 **"wide-gap" 정성 인용 규율**과 리뷰 서술이 같은 방향. ⚠ vdW 는 리뷰가 D3/BJ 를 구분 안 하므로 **우리 D3(BJ) 선택 근거는 `[Maurer15MBD]`(§J-43) 로**, 이 리뷰는 "계면엔 분산보정이 적절" 방향 문장만 |
| ② | **Beyond-DFT (TDDFT/GW/BSE)** | 갭·준입자·엑시톤이 **목표 물성일 때만** 선별 후보에 적용; GW 는 출발점·빈밴드·k·SOC 민감·고비용 | **안 함.** 우리 갭은 fixed-occ nscf 고유값 PBE(comp1 2.066 / modelc 2.099 eV)이고 **정성 "wide-gap" 으로만** 인용 | ✅ **정합** — 리뷰 §3.1 말미 문장(§9-②)이 *"우리가 HSE/GW 를 안 한 이유"* 의 외부 표현. 🔴 단 리뷰는 "갭이 결정적이면 GW" 라 한다 — **우리 SEI/전자절연 서사에서 갭이 결정적이라고 주장하는 순간** 이 문장은 우리를 겨눈다. 갭을 정성으로만 쓰는 현 규율을 유지할 것 |
| ③ | **AIMD vs MLIP · 스케일 · 유한크기** | AIMD = 작은 계·짧은 궤적 / MLIP = **10⁴–10⁶ 원자 · ns** / `Fig. 3a`: 셀 크기가 **D 와 전이 T 를 바꾼다** | **UMA-s-1p1(omat) MLIP-MD**, box331 **558 원자**, 600/800/1000 K 3점 아레니우스, 5 ps 평형 + **200 ps**(lpsocl 일부 400 ps), MSD 2–50 ps, 3-시드(600 K) | 🔴 **위치**: `[Dutra25Rev] Fig. 3b`(>10,000 원자·>1 ns)와 같은 판정 — **우리는 리뷰의 "MLIP 스케일 칸" 하단**이다. 🔴 **새 압박**: `Fig. 3a` 는 초이온체에서 N 수렴 없이 D·전이 T 를 말하면 안 된다고 그림으로 보여준다. `our_dft_baseline.md`·CLAUDE.md 에는 **D 의 셀-크기 수렴 기록이 없다** — 있으면 카드를 여기 링크, 없으면 **§H 정직목록에 추가**(우리 인용정책이 상대차만 쓰는 것이 완충이지만, 상대차도 N 에 따라 바뀔 수 있다는 것이 `Fig. 3a` 의 요지다) |
| ④ | **범용/파운데이션 MLIP** | "foundation models" 1회(`[113]`) · 사전학습 **MACE 미세조정+증류** 1회 `[142]` · `[108]`(범용 MLIP 도메인 전이, *Nat. Commun.* 2026)은 참고문헌에만; **UMA·OMat24 0회**; 기본 서사는 여전히 *"DFT 참조데이터로 계 전용 퍼텐셜 학습"* | **사전학습 UMA 를 미세조정 없이 as-is** 사용 | ⚠ **Dutra25Rev(0회)보다 한 칸 최신**이지만 우리 선택의 근거는 못 된다. 근거는 기존 전용편(`liu2026_finetuning_umlip_tutorial` · `tompa2026_…` · `alghamdi2026_…` · `petmad2026_…` · `chang2026_…` · `wang2025_pretrained_…`). 🔴 리뷰의 **"ML 은 학습 범함수의 편향을 상속한다"** 는 UMA(omat = PBE/PBE+U 계열 데이터)에 그대로 걸린다 → 우리 "UMA 는 PBE 편향 상속" 한 줄의 인용 후보(§9-④), 원전은 `[136]` Park 2026 *AEM* / `[138]` |
| ⑤ | **검증 관행** | *"validate … against downstream observables rather than energy and force errors alone (ionic conductivity, phase-transition T, diffusion, electronic properties)"*; 그러나 자기 그림 `Fig. 6` 은 **오차 수치 없는 힘 패리티** | §J-1 UMA 힘 정확도 실측(외부 데이터) + 물성 수준은 **계 간 상대 Ea/D 만**; RDF 0 · VDOS 0 · 상전이 T 0 | ⚠ 문장은 우리 편(§9-⑤)이고 `makino2026`·`chang2026` 과 같은 방향. 🔴 그러나 우리도 리뷰가 요구하는 관측량 검증(σ 실험 대조 · 상전이 T)을 **절대값 정책 때문에 못 한다** — "상대차만 인용" 은 정책이지 검증이 아니다. 이 문장을 인용하면 심사자가 **"그럼 너희는 무엇으로 검증했나"** 를 물을 것을 예상하고 J-1 + 3-시드 + He18 통계를 준비 |
| ⑥ | **무질서 처리** | MC 배열 표본추출(*"which configurations are thermodynamically favored"*) · 클러스터전개 · ML-MC; `Fig. 3b` 배열 표본 없으면 전이 T 100 K 과대; `Fig. 6` disordered 상 학습; `Fig. 7` 비정질 단일 아레니우스. **SQS 0** | **disorder-ensemble**: S/Cl 배열 다중 + 담금질/속도 시드, 배열별 MD → 산포 보고(`disorder_ensemble_diffusion.py`) | ⚠ 어휘상 *"explicit configurational sampling"* 에 가장 가깝다. 🔴 리뷰의 MC 정의는 **열역학 가중**을 전제한다 — 우리 앙상블이 배열을 **균등 가중**하는지 **볼츠만 가중**하는지, 카드(`estimand_card`)에 선언돼 있어야 이 리뷰 어휘로 설명할 수 있다. 선언이 없으면 *"균등 표본의 산포"* 라고 정확히 쓰고 MC 라 부르지 않는다 |
| ⑦ | **ML 발견 · hull 컷** | GNoME 2.2 M · Alexandria · InvDesFlow-AL; **Matbench Discovery**: hull 경계 근처 안정/준안정 판별 실패 → *"ML as a screening accelerator rather than a replacement"* | cascade Stage 00–12(§J-10) · 다중충실도 층(§J-12/13) · hull 컷 | ✅ 방향 정합. 인용 후보 §9-⑥(원전 `[166]` Riebesell 2025 *Nat. Mach. Intell.*). `Fig. 4d`(원소 수 ↑ → 정밀도 ↓)는 우리 다원소 도핑 후보에 그대로 걸리는 경고 |
| ⑧ | **다중충실도 · 우리 물질 호명** | *"In Li₆PS₅Cl, [PBE+SCAN/r²SCAN multi-fidelity MLIP] predicted Li-ion conductivity within 10 % error"* `[140]` | 우리 cascade 다중충실도 층(§J-12·J-13 [Basu26MFB] · `aqib2026_…`)은 **물성 대리모형** 층이고 MLIP 충실도 혼합은 아니다 | 🔑 **우리 물질에서의 MLIP 다중충실도 선례** — 원전(Kim et al. arXiv 2409.07947)을 확보해 (a) "10 %" 의 기준 (b) 셀·온도·MSD 규약 (c) 실험 대조 여부를 확인한 뒤 §J 에 별도 블록. ⛔ 확보 전 인용 금지 |
| ⑨ | **후처리 어휘** | DOS·결함에너지·확산장벽·탄성·흡착 — **COHP/Bader/ELF/BVSE/ESW 0** | ICOHP(LOBSTER) · BVSE · grand-potential ESW · EOS · elastic | Dutra25Rev 와 동일: 우리 결합·채널 관측량은 **일반 리뷰 지도 밖** — 차별화이자 "설명 부담" |
| ⑩ | **불확실도 · 통계** | UQ 한 문장(§5) · 오차막대·시드·MSD 창 0 | 3-시드 600 K(결정계) · 유리 담금질 시드 IQR · MSD 2–50 ps 고정 · NE Haven=1 · 절대값 인용 금지 | ⛔ 근거로 못 쓴다. 정본은 `he2018_…`(§J-29) · `maginn2019_…` · `mccluskey2025_…` · `zaby2026_…` · `carrete2023_…`(§J-18) |

**종합 판정** — 이 리뷰는 우리 방법 스택을 **부정하는 곳이 없고**(모두 "표준 칸" 안), **더 요구하는 곳이 셋**이다: ③ 셀-크기 수렴 근거, ⑤ 관측량 수준 검증, ⑥ 배열 가중 규칙 선언. 셋 다 이미 우리 원장의 §H(못 하는 것)·보고량 카드 규율과 겹친다 — **새 결손이 아니라 기존 결손의 세 번째 외부 지적**이다.

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

1. **서론 첫 단락의 "방법 계층" 문장**은 이 리뷰로 열 수 있다 — *DFT 로 넓게, 상위 방법은 목표 물성이 요구할 때만*(§9-②). 우리가 PBE 에 머물고 갭을 정성으로 쓰는 선택을 **"비용 대비 스크리닝 표준"** 으로 위치짓는 데 딱 맞는 일반 문장이다. 단 방법 절에는 쓰지 않는다(파라미터 근거 0).
2. **`Fig. 3a` 가 준 숙제**: 558 원자 상자에서 D·Ea 의 **N 의존성**을 한 번은 확인하거나(싼 탐침: 같은 조성 2×2×2 vs 3×3×1 짧은 MD 1점 · 상대 Ea 차가 시드 산포 안이면 닫음), 확인하지 않을 거면 **§H 에 "셀-크기 수렴 미시험" 을 명시**한다 — 재개 규칙(문턱 + 발동 시 할 일)을 결과 전에 박는 CLAUDE.md 규율 그대로. 상대차 정책이 완충이라도 `Fig. 3a` 의 N=12 vs 768 은 **기울기(Ea)까지 바뀐다**는 것을 보여준다.
3. **UMA 편향 상속 문장**(§9-④)을 방법 절 한 줄로 — *"UMA(omat) inherits the biases of the PBE-family functionals in its training data"* — 원전 `[136]`·`[138]` + 우리 `wang2025_pretrained_…`(안장점 과소평가) 와 묶는다.
4. **Kim 2024 arXiv 2409.07947 확보** — 우리 물질에서 PBE+r²SCAN 다중충실도로 σ 를 재현했다는 유일한 선례. cascade 다중충실도 층(§J-12/13)의 "층 정의 근거" 로 **MLIP 충실도 축**을 추가할지 판단할 자료다.
5. **`Fig. 7` 패턴 어휘** — "결정 = 꺾인 아레니우스(초이온 전이) / 비정질·무질서 = 단일 기울기" 를 우리 Cl-rich disorder 논의의 **개념 대응물**로만 쓴다(Na 옥시클로라이드 값 이식 금지). 우리 3점(600/800/1000 K) 아레니우스가 **꺾임을 볼 수 없는 설계**라는 점도 같이 적어야 정직하다(400/500 K 는 판정 제외 — 감김·통계 사유).
6. **인용 위생 반면교사**: 이 리뷰의 `[103]`·`[157]`·`[182]` 오인용은 "리뷰의 번호를 그대로 옮기면 틀린다" 의 실증. 우리 원고 레퍼런스는 **로컬 PDF/digest 기준**(CLAUDE.md §원고 작성) — 이 편이 그 규칙의 이유를 보여준다.

---

## 9. 인용 가능 문장 (deck/paper 용 — 원문 그대로 · 짝지은 원전을 함께 인용)

| # | 원문 (p.) | 용도 | ⚠ 같이 붙일 원전 |
|---|---|---|---|
| ① | *"Semilocal functionals, particularly PBE-GGA, are widely used for structural optimization, formation energies, phase stability, defect formation, adsorption, and high-throughput screening because of their relatively low computational cost. However, their systematic underestimation of semiconductor band gaps … restrict their quantitative reliability"* (p.5) | 방법 절 — 우리 PBE 선택 + 갭 정성 인용 규율 | 갭 과소평가는 교과서적 — 원전 없이도 되나 `[76]`/Perdew 계열 원전 병기 권장 |
| ② | *"an efficient computational strategy uses DFT for broad structural and energetic screening, higher-level DFT approaches for selected candidates, and more computationally demanding excited-state methods only when the target property requires them."* (p.5) | 서론 — 왜 PBE 스크리닝인가 | 단독 인용 가능(리뷰 자신의 종합 문장) |
| ③ | *"MD simulations of superionic conductors showed that finite-size effects can significantly influence calculated diffusion behavior and transition temperatures"* (p.6) | 방법/한계 — 셀 크기 | **Grasselli 2022 *J. Chem. Phys.* 156, 134705** (`[91]`) 를 반드시 원전으로 |
| ④ | *"ML models inherit biases from the DFT functional used for training and may become unreliable for defects, interfaces, highly distorted structures, or chemical environments outside the training domain"* (p.10) | 방법 — UMA 편향 상속 · 계면 외삽 경고 | `[136]` Park 2026 *Adv. Energy Mater.* e71046 · `[138]` Li 2025 *Mater. Horiz.* + 우리 `wang2025_pretrained_…` |
| ⑤ | *"recent studies increasingly validate hybrid models against downstream observables rather than energy and force errors alone, including ionic conductivity, phase-transition temperatures, diffusion, and electronic properties"* (p.10) | 검증 절 — 왜 힘 RMSE 로 끝내지 않나 | `[137]` Xie 2024 *JCTC* · `[140]` Kim 2024 arXiv · `[150]` Sauer 2025 arXiv + 우리 `makino2026_…`·`chang2026_…` |
| ⑥ | *"ML models can struggle to distinguish stable from metastable structures near the convex-hull boundary, where small prediction errors can lead to incorrect material selection"* (p.12) | cascade hull 컷 논의 | **Riebesell 2025 *Nat. Mach. Intell.* 7, 836** (`[166]`) |
| ⑦ | *"MD and MC should not be viewed as competing methods. MD is preferable when the central question concerns how atoms move or a process evolves, whereas MC is preferable when the question concerns which configurations are thermodynamically favored."* (p.7) | disorder-ensemble 위치 설명 | 단독 인용 가능(리뷰 종합 문장) |
| ⑧ | *"The role of dynamic simulations is particularly important for solid electrolytes, where ionic conductivity depends on collective motion and structural disorder."* (p.12) | 서론 — 왜 MD 인가 | 단독 가능; 구체 근거는 `[178]`·`[179]` 또는 우리 `[Morgan21Mech]`(§J-33) |
| ⑨ | *"increasing dataset size does not necessarily guarantee better extrapolation to genuinely new materials."* (p.14) | ML 축 — LODO·UQ 정당화 | ⚠ 리뷰가 이 문장 뒤의 "Recent studies show…" 에 **인용을 안 달았다** — Riebesell `[166]` 또는 우리 `[Carrete23UQ]` 로 보강 |
| ⑩ | `Table 2` 행: *"DFT-D/vdW — Improved dispersion description — Method-dependent — 2D materials, interfaces, adsorption"* (p.5) | W_ad 슬랩에 분산보정을 넣는 이유 | 모델 선택(D3(BJ) vs MBD)은 `[Maurer15MBD]`(§J-43) 로 |

⛔ **인용하면 안 되는 것**: `Li₆PS₅Cl` "10 % 이내" (원전 미확보 · 기준 불명) · `Fig. 7` Ea 수치(그림 전용 · Na 계) · `Fig. 6` "정확히 재현"(오차 수치 없음) · GNoME "2.2 million" 을 hull 위 안정 수로 · `Table 5` 참고열 번호 · 이 리뷰의 인용번호 일체(원전 재확인 없이).

---

## 10. 주의 / 한계 / 비판 (over-claim 방지)

① **참고문헌 위생 — 이 편의 가장 큰 결함.** 확인된 오귀속·부적합 인용: `Fig. 4` 캡션 `[103]` = Rashidi et al. *Front. Oncol.* 2023(지도학습 통계 개념) ← GNoME 원전은 `[105]` Merchant 2023 *Nature*; §4.2.3 MOF 수소저장에 `[157]`(Liu/Prezhdo, MoS₂ NAMD *PNAS*); §5 재료 데이터셋 편향에 `[182]`(Su et al. *Biosensors* — 플렉서블 전자 ML 리뷰); §3.3 MC 방법론에 `[95]`("Method 'Monte Carlo' in Healthcare", *World J. Methodol.*); §3.4 ML 알고리즘에 `[102]`(ML 구성방정식 리뷰)·`[103]`(종양학); §2.1 양자재료 예시(그래핀·TMD)에 `[5]`·`[6]`(탄소점 약물전달·도핑 탄소점); `[15]` 위상절연체–양자컴퓨팅이 *"Biol. Med. Sci."*; `[3]` 저널명 누락; 공저자 자기인용 `[7]`·`[12]`·`[29]`. ⇒ **이 리뷰를 경유해 1차 문헌을 인용할 때는 번호가 아니라 제목으로 찾아 원문을 연다.**

② **그림–본문 불일치·누락**: `Fig. 3b` 인쇄값 818 → 721 K vs 본문 "810 → 710 K"(반올림, 무해하지만 인용 시 원전값으로); `Fig. 3a` 캡션 "fluorite-structure" 인데 **α-AgI 패널 포함**, 그리고 AgI 의 **크기효과 없음** 결과를 본문이 다루지 않는다(유한크기 효과가 계 의존이라는 더 유용한 메시지가 빠짐); `Fig. 4a` "2.2 million" vs `Fig. 4b` ≈3.8×10⁵(다른 양)를 구분 없이 사용; `Fig. 7` 의 Ea 수치·전이 T 가 본문에 전혀 없음.

③ **검증 서술의 자기모순**: §3.6 은 *"힘·에너지 오차만으로 검증하지 말라"* 고 쓰고, 그 절 바로 뒤 §4.2.3 의 유일한 "검증" 그림 `Fig. 6` 은 **오차 수치도 없는 힘 패리티**다. 본문의 *"accurately reproducing ab initio atomic forces"* 는 시각 판정이다.

④ **제작 품질**: `Fig. 1` 에 "Exicted States" 오타와 **맞춤법 검사 밑줄(붉은 물결선)** 이 그대로 인쇄됨; §3.4 에 같은 문장("generated candidates still require physics-based validation…")이 **두 번** 인쇄; `[85]` 뒤 문장부호 누락("[85]Fig. 3(b)"). Received → online 이 **100일**(2026-06-07 → 09-15)이고 펀딩 없음.

⑤ **방법 파라미터 0 · 규약 0**(§4). `[Dutra25Rev]` 보다도 얇다(dt 조차 없음). 방법 재현·규약 근거로 인용 불가.

⑥ **`Li₆PS₅Cl` "10 % 이내" 한 줄**은 arXiv 프리프린트(`[140]` 2409.07947)의 2차 요약이고 **비교 기준(실험 σ? 고충실도 MD?)·온도·셀·MSD 규약이 전부 없다.** 우리 물질이라 끌리지만 **원전 확보 전 인용 금지**.

⑦ **2026 기준으로 낡은 곳**: 범용/파운데이션 MLIP(MACE-MP-0 · CHGNet · M3GNet · SevenNet · **UMA/OMat24** · MatterSim · Orb)가 본문에 **하나도 없다**(참고문헌 `[108]` 이 범용 MLIP 논문인데 본문은 GAP/DP 예시로만 소비); MLIP 벤치마크(Matbench Discovery 는 안정성 예측 문맥에만) · UQ 프로토콜 · 유한크기 보정(`[91]` 을 그림으로 실어 두고 보정법은 없음) · Haven/NE · MSD 창 논의 0. QC 절은 "가능성" 서술이 대부분이고 저자들도 *"not yet … predictive quantum simulations of energy materials"* 라 인정한다.

⑧ **"property-driven hierarchy" 라는 차별화 주장**은 실질적으로 `Table 5` 한 장 + TDDFT/GW/BSE 단락의 "다른 물리 문제" 프레이밍이다. 방법 간 **정량 비교**(같은 계에서 PBE vs HSE vs GW 갭, AIMD vs MLIP D)는 하나도 없다. 응용 §4 는 사례 나열이고 사례 간 연결 논리는 "정적 → 동적/소자로 이동 중" 한 줄이다.

⑨ **우리 판정에 대한 함의** — 이 편이 우리 방법을 **부정하는 대목은 없다.** 다만 우리가 이미 §H 에 적어 둔 결손(셀-크기 수렴 · 관측량 검증 · 배열 가중 선언)을 **세 번째 외부 문헌이 다시 짚는 것**이므로, 원고 심사 대비 답변 준비의 우선순위를 올린다.

---

## 11. 확보 대상 (이 digest 가 발굴한 원전 · 우선순위)

1. **Grasselli 2022, *J. Chem. Phys.* 156, 134705** (`[91]`, `Fig. 3a` 원전) — 초이온체 MD 유한크기 효과(D · 열수송 · 열운동). 우리 558 원자 상자의 **셀-크기 수렴 논거/보정법** 원전. ⚠ litdb 에 있는 `grasselli2025_uncertainty_era_ml_atomistic.md` 는 **다른 논문**이다.
2. **Kim et al. 2024, arXiv 2409.07947** (`[140]`) — Data-efficient multi-fidelity MLIP; **Li₆PS₅Cl σ "10 % 이내"** 의 원전. 기준·규약 확인 후 §J 별도 블록 후보.
3. **Riebesell et al. 2025, *Nat. Mach. Intell.* 7, 836** (`[166]`, Matbench Discovery) — hull 경계 ML 판별 실패의 정량 근거(cascade hull 컷 §J-10·J-12 에 직접).
4. **Guo/Koverga/Selvaraj/Ngo 2025, *ACS Appl. Energy Mater.* 8, 14773** (`[178]`, `Fig. 6` 원전) — Li₂ZrCl₆ DP-MD: 무질서 상 학습·검증 절차(우리 `ren2026_li2zrcl6_…` 의 계산 짝).
5. **Wei/Binci/Ceder 2026, *ACS Energy Lett.* 11, 1861** (`[179]`, `Fig. 7` 원전) — 결정 vs 비정질 초이온 기전; Ea 수치의 정본.
6. **Park et al. 2026, *Adv. Energy Mater.* e71046** (`[136]`) — 에너지재료용 MLIP 아키텍처·학습·응용 리뷰(§9-④ 원전).
7. Kim et al. 2026, *Nat. Commun.* 17, 3432 (`[108]`) — 범용 MLIP 도메인 전이 최적화(⚠ litdb 의 `wang2026_domain_oriented_universal_…` 과 **다른 논문**인지 확인).
8. Menon et al. 2026, arXiv 2607.14795 (`[85]`, `Fig. 3b` 원전) — 배열·진동 엔트로피 명시 상도표(disorder-ensemble 의 가중 규칙 참고).

---

## 12. 기법 미니 용어집 (이 편에 나오는 것만)

- **TDDFT** — 시간의존 KS 방정식으로 여기에너지·광응답을 얻는 방법. 선형응답 커널이 XC 근사에 의존; 장거리 전하이동 여기에 약함.
- **GW 근사** — 자기에너지 Σ ≈ iGW (G = 단일입자 그린함수, W = 스크린된 쿨롱). KS 고유값을 준입자 에너지로 보정 → 갭 개선. G₀W₀(1회 보정) / qsGW(준입자 자기일관). 출발점·빈밴드·k·SOC 수렴에 민감.
- **BSE** — 전자–정공 2체 방정식; GW 준입자 위에 엑시톤(결합에너지·흡수 스펙트럼). **Tamm–Dancoff 근사** = 여기/탈여기 결합 무시.
- **VQE / QPE / DMFT 임베딩 / QSCI** — 변분 양자 고유해법(NISQ 용) / 양자 위상 추정(내결함 필요) / 강상관 부분공간만 양자처리 / 양자 표본 기반 선택 CI.
- **GNN · GNoME · AIRSS** — 원자=노드·결합=엣지 그래프 신경망 / DeepMind 의 GNN+능동학습 결정 발견(2.2 M hull 근접) / 무작위 구조 탐색.
- **GAP · Deep Potential · MACE** — 커널(SOAP) 기반 / 심층신경망 기반 / 등변 메시지패싱 기반 MLIP. **증류(distillation)** = 큰 사전학습 모델의 지식을 작은 모델로 옮김. **multi-fidelity** = 저충실(PBE) 다량 + 고충실(SCAN/r²SCAN) 소량 공동 학습.
- **클러스터 전개(cluster expansion)** — 격자 배열 에너지를 클러스터 상관함수의 선형결합으로; MC 와 결합해 정렬–무질서·상도표. 희소화로 학습셋 절감.
- **NAMD(비단열 MD)** — 전자 상태 간 전이를 포함한 MD; 캐리어 포획·재결합 시간.
- **SCAPS-1D** — 태양전지 1D 소자 시뮬레이터(DFT 물성을 입력으로).
- **Cauchy 모델** — n(λ)=A+B/λ²+C/λ⁴ 굴절률 분산식.
- **Sabatier 원리 · 스케일링 관계** — 흡착에너지 중간이 최적 / 중간체 흡착에너지 간 선형관계로 서술자 축소.
- **E_hull · Matbench Discovery** — 볼록껍질 위 에너지(안정성 지표) / ML 안정성 예측 벤치마크.
- **Barren plateau** — 변분 양자회로에서 기울기가 큐빗 수에 지수적으로 소멸하는 문제.
- **A-Lab** — 자율 합성 실험실(로봇 합성 + XRD 자동 해석 + 능동학습).

---

## 🗨️ Q&A 로그
(비어 있음 — 질문이 나오면 여기에 누적)

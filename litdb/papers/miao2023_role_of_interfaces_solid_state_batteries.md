# Role of Interfaces in Solid-State Batteries — Miao / Guan / Ma / Li* / Nan* (Adv. Mater. 2023, 35, 2206402)

> slug `miao2023_role_of_interfaces_solid_state_batteries` · DOI `10.1002/adma.202206402` · type **review (문헌 컴파일 — 자체 계산·실험 0)** · PDF `663eb3cf-56._Role_of_Interfaces_in_SolidState_Batteries.pdf` (21 pp, 본문 15 pp + refs 266) · digested `2026-08-05` · status ✅
> **로컬 원본** = `litdb/inbox/56. Role of Interfaces in Solid-State Batteries.pdf` (**inbox #56 · 사용자 분류 폴더 `DFT`**) — 업로드본과 동일 파일. **재투입 검증 `2026-08-06`**: 21쪽 텍스트 전문 재전사 + 그림 6장(fig_1–fig_6) 재추출·**재열람**. 본문 수치·표 3개·Figure 6장 모두 일치, 신규 사실 없음. 유일한 정정 = **Fig. 2a 반원 귀속**(아래 §7 표) — 고압 곡선에 반원이 있는 게 아니라 **없다**.

> 🔗 **왜 지금 이 논문인가 (두 축)**
> ① **같은 그룹의 3년 전 리뷰다.** 교신저자 **Ce-Wen Nan**(Tsinghua)이 우리가 심사 중인 원고
> `papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md`(ECER-D-26-00097)의 공저자다.
> → **§10 이 digest의 본체**: 2026 원고가 2023 프레임을 무엇을 이어받고·무엇을 새로 넣고·
> **무엇을 빠뜨렸고**·어디서 다르게 설명하는지. 리뷰어 노트 `kb/reviews/ECERD2600097_review_notes.md`의
> **B5·B1·B4·B2**가 이 논문으로 근거를 얻는다.
> ② **우리 T3(Li‖LPSCl 반응 MD) 공백**과 정면으로 닿는다 → §11.3.


> elements: Al B Br C Cl Co F Fe H La Li N Nb O P S Ti Y
> methods: arrhenius, bandgap, bvse, cohp, dft, elastic, esw, functional, md, mlip, pdos

---

## 0. 이 digest를 읽는 법

- **이 논문은 "계면" 한 축으로만 쓴 리뷰다.** 공기·용매·열 안정성은 **아예 없다**(본문 전체에서
  H₂S 0회 · HSAB 0회 · air 2회(스치듯) · 열은 "열처리 접합" 문맥뿐). 대신 **계면을 세 층위로
  분류**하는 좌표계를 세운다 — 그게 이 리뷰의 유일하고 진짜인 기여다.
- **자체 데이터 0.** 모든 수치는 소환값. **DFT·first-principles·band gap·VBM 단어가 본문에 0회**
  (계산은 §6 Outlook 3번 항목에서 "앞으로 필요하다"로만 등장). 즉 이 리뷰는 **비계산 리뷰**다 —
  우리 물성 4축과 숫자로 겨룰 논문이 아니라 **어휘·분류·표 양식**을 가져올 논문이다.
- 실제 인용 가치가 가장 큰 것은 본문이 아니라 **Table 1·2·3**(압력↔셀 성능 / CAM 코팅 / Li‖SE
  버퍼층) — 리뷰가 흩어진 문헌을 한 좌표에 모은 유일한 자리다. (→ 리뷰어 노트 **B5**의 정답지)
- 섹션별 상세 §5, 수치 총정리 §4, 표 3개 §6, 그림 6장 §7, **2023↔2026 대조 §10**, 우리 대비 §11.

## 1. 한 줄 요약

SSB의 성능은 재료가 아니라 **고체–고체 계면**이 결정한다는 명제를, 계면을 **① SE 내부 매립계면
(입계·CSE 필러/폴리머 계면) ② 복합전극 내부 계면(AMP/SE) ③ 전극|SE 분리막·집전체 평면계면**
세 층위로 분해해 정리한 21쪽 리뷰. 각 층위마다 **물리적 접촉 → (전기)화학 안정성 → 기계적
부피변화**의 같은 3박자로 문제를 세우고, 해법을 **코팅·버퍼층·압력·in-situ 중합**으로 대응시킨다.
가장 오래 살아남은 산출물은 **Li/SE 계면 3분류(열역학 안정 / MCI / SEI)**와 **μ_c ↔ HOMO 정렬
도식**이며, 둘 다 2026 원고가 그대로 물려받았다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | Role of Interfaces in Solid-State Batteries |
| 저널 | **Adv. Mater. 2023, 35, 2206402** (Wiley-VCH; article number 2206402, 21 pp) · DOI 10.1002/adma.202206402 |
| 저자 | **Xiang Miao**, Shundong Guan, **Cheng Ma**, **Liangliang Li\***, **Ce-Wen Nan\*** |
| 소속 | State Key Laboratory of New Ceramics and Fine Processing, School of Materials Science and Engineering, **Tsinghua University**, Beijing 100084 · (C. Ma) Hefei National Research Center for Physical Sciences at the Microscale, CAS Key Lab of Materials for Energy Conversion, **USTC**, Hefei |
| 교신 | liliangliang@mail.tsinghua.edu.cn · **cwnan@tsinghua.edu.cn** |
| 날짜 | Received **2022-07-14** / Revised **2022-08-14** / Published online **2023-02-22** (PDF 푸터상 2023 issue 50) |
| Keywords | composite cathodes; grain boundaries; interfaces; lithium anodes; solid electrolytes; solid-state batteries |
| Funding | NSFC **51788104**, **U21A2080** |
| 유형 | **리뷰 (자체 계산/실험 0)** — 본문 15 pp, Figure 6, Table 3, refs **266** |
| 그룹 맥락 | **Nan 교신** = `fan2026_…ECERD2600097`(심사 중, Nan 공저)의 **3년 전 선행 리뷰**. 우리 litdb의 `kim2021_review_oxide_sulfide_se_interfaces`(Rupp)와 같은 "계면 landscape" 계열 |

## 3. 리뷰 구조 지도 + 이 리뷰가 세우는 프레임

```
1  Introduction                         — LIB의 액체–고체 계면 → SSB의 고체–고체 계면 (Fig. 1)
2  Interfaces within Solid Electrolytes   ← ① SE 내부 "매립(buried)" 계면
   2.1 Grain Boundaries in Inorganic SEs  (Fig. 2)   ★ 2026 원고에 대응 절 없음
   2.2 Interfaces within Composite SEs    (Fig. 3)   ★ 2026 원고에 대응 절 없음
3  Interfaces within Composite Electrodes ← ② 복합전극 내부 계면
   3.1 Physical Contact at Interfaces     (Fig. 4a,b · Table 1)
   3.2 Chemical/Electrochemical Stability (Fig. 4c,d · Table 2)
4  Interfaces between Electrodes and SE Separators ← ③ 평면계면
   4.1 Cathode | SE separator             (Fig. 5a–d)
   4.2 Anode | SE separator
       4.2.1 Chemical/Electrochemical Stability  ★ 계면 3분류(안정/MCI/SEI) · Table 3
       4.2.2 Li Dendrite Growth                  (Fig. 5e–g)
5  Interfaces between Current Collectors and Electrodes  ★ 2026 원고에 대응 절 없음
6  Outlook — 5 방향 (Fig. 6)
```

**이 리뷰가 실제로 기여하는 것 = 3개의 분류체계 (수치가 아니라 어휘)**

| # | 분류체계 | 내용 | 어디서 |
|---|---|---|---|
| **F1** | **계면 3층위 (공간적)** | ① SE 내부 매립계면(GB·필러/폴리머) ② 복합전극 내부(AMP/SE) ③ 전극\|SE분리막 + 전극\|집전체 | §2·3·4·5 = 리뷰의 뼈대 |
| **F2** | **Li/SE 계면 3유형 (거동적)** — ★가장 많이 인용됨 | ① **열역학 안정**(새 상 없음; "most desired, but extremely rare") ② **MCI** = mixed electronically & ionically conducting interphase → SE나 음극이 다 소모될 때까지 성장 → "completely unacceptable" ③ **SEI형** = 이온전도·전자절연 → 자기제한 | §4.2.1 |
| **F3** | **μ_c ↔ HOMO 정렬 (에너지)** | 양극 화학퍼텐셜 μ_c가 황화물 HOMO **위** = 안정 / **아래** = 산화 → CEI 필요; CEI(또는 코팅)의 HOMO가 μ_c보다 **아래**여야 계가 안정 | Fig. 4c |

+ 두 개의 **설계 rubric**(체크리스트):
- **CAM 코팅 6조건** (§3.2): 1) 완전 격리 균일성 2) **최소 두께**(전하이동저항↓) 3) 높은 σ_ion
  4) CAM 부피변화 내성 5) 화학·전기화학 안정 6) **단순·확장 가능한 합성**(양산성)
- **음극측 버퍼층 4조건** (§4.2.1, 산화물 대상): 1) **lithiophilicity** 2) SE와 (전기)화학적 불활성
  3) 높은 Li 확산도 + **저두께** 4) 사이클 중 안정

## 4. 수치 총정리 (본문에 실제로 등장하는 정량값 **전부**)

> ⚠ 정직 note: **이 리뷰는 정량 리뷰가 아니다.** 아래가 본문 15쪽에 있는 숫자의 거의 전부이며,
> 대부분이 "어떤 논문이 이런 값을 냈다"는 단발 소환이다. 기계 물성(E·G·K_IC), ESW(무기 SE),
> band gap, 흡착에너지 같은 **재료 고유 물성값은 사실상 0개**다.

### 4.1 전도도·재료 스펙
| 값 | 대상 | 위치 |
|---|---|---|
| σ(RT) ≈10⁻⁷–10⁻⁵ S/cm | 폴리머 SE (PEO계) | §1 |
| σ(RT) ≈10⁻⁴–10⁻² S/cm | 무기 SE 일반 (예: Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃, Li₁₀GeP₂S₁₂), t_Li ≈ 1 | §1 |
| σ(RT) 10⁻⁴–10⁻² S/cm | **냉간가압 100–300 MPa** 만으로 얻어지는 황화물·할라이드 펠릿 총전도도 | §2.1 |
| σ ~10⁻³ S/cm (LLTO 벌크) → 총 10⁻⁵ S/cm | 페로브스카이트: **GB 저항이 2 자릿수를 먹는다** | §2.1 |
| σ_bulk 10⁻³ S/cm ≫ σ_total (LATP) | NASICON: GB 때문에 총전도도 1 자릿수↓ | §2.1 |
| σ_GB ≈ σ_bulk ≈ 10⁻⁴ S/cm | **Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂** — GB가 총전도도를 안 깎는 **예외** | §2.1 |
| **1.03×10⁻³ vs 1.12×10⁻⁴ S/cm** | B(붕소) 도핑 LiTi₂(PO₄)₃ glass-ceramic vs 무도핑 — **GB 유리화**로 ~9배 | §2.1 |
| GB σ **×2–3** | Nb 도핑 LLTO — 캐리어/도펀트 농도↑ → **공간전하 전위↓** | §2.1 |
| GB 두께 **1–2 unit cells** | 고국소 특징 → Cs-corrected STEM 필요 | §2.1 |
| 소결 **>1100 °C** | 산화물 SE 치밀화 (황화물은 냉간가압) | §2.1 |
| EIS 정전용량 배정 기준: bulk ≈10⁻¹¹ / GB ≈10⁻¹⁰–10⁻⁷ / 계면 ≈10⁻⁷–10⁻⁵ F | (지름 1 cm × 두께 1 mm 펠릿 기준) — GB 반원이 안 보이는 LPSCl·LGPS의 R_GB를 등가회로로 분해할 때 | §2.1 |
| SE 분리막 목표 두께 **10–25 µm** | 고에너지밀도 요구 | §2.2 |
| Li 이론용량 **3860 mAh/g**, 전위 **−3.040 V vs SHE** | Li 금속 음극 | §1 |

### 4.2 복합 SE(CSE) — 폴리머 매트릭스
| 값 | 의미 | 위치 |
|---|---|---|
| σ **2 자릿수↑** | PEO/LiClO₄ + Al₂O₃ 또는 TiO₂ 나노입자 | §2.2 |
| σ **~2 자릿수↑** | PEO + 2D 버미큘라이트 시트(음전하 표면) | §2.2 |
| **9.83×10⁻⁴ S/cm**, t_Li⁺ **0.68** | PEG 매트릭스 + LGPS (실란 커플링제로 계면 상용성 개선) | §2.2 |
| **4.6×10⁻⁴ S/cm** | MXene-mSiO₂ 나노시트 + PPO 엘라스토머 매트릭스 CSE | §2.2 |
| **Fig. 3c 표(figure-read)**: E_a(A)→E_a(B) — PEO/LiClO₄ ~1.0→~0.5 eV · PEO/LiTFSI ~0.5–0.6→~0.3–0.4 eV · PAN/LiClO₄ ~0.94→~0.34 eV | 필러 무첨가(A) → 계면층 퍼콜레이션(B)이 **E_a를 절반으로** | Fig. 3c |

### 4.3 복합전극 · 코팅
| 값 | 의미 | 위치 |
|---|---|---|
| 초기 **103 vs 81 mAh/g**, 50 cyc **91.7 %** | (Li₂S)₈(P₂S₅)₂(Ni₃S₂)₁ 복합양극: 냉간가압+**85 °C/500 MPa** 추가가압 vs 냉간가압만 | §3.1 / Table 1 |
| **0.32 MJ/cm³** resilience, σ **0.25 mS/cm**, 300 cyc **95 %**@0.2 C | PPO 엘라스토머 매트릭스 SE + LiFePO₄ | §3.1 |
| 탄성률 **6.8 GPa** | AMP에 코팅한 전자·이온 이중전도 폴리머 | §3.1 |
| **LiNbO₃ ~5 nm** → **203 mAh/g**@0.1 C, **136.8 mAh/g**@5 C | NCM811 + LGPS | §3.2 |
| **20 000 cycles / 71 %** @1.0 mA cm⁻² RT | LiNbO₃-코팅 NCM811 + **Li₆PS₅Cl** — 리뷰 전체 최장수명 | §3.2 / Table 1·2 |
| 결정질 **LLTO ≈6 nm**, σ **0.3 mS/cm** | 단결정 NCM622 코팅 — "계면반응과 **공간전하층**" 동시 대응 | §3.2 |
| 산화한계 **≈5 V** | PEO + LLZO 입자 catholyte; NCM622 셀 70 °C·4.2 V cutoff·**160 mAh/g @C/20** | §3.2 |

### 4.4 전극|분리막 · 음극 계면
| 값 | 의미 | 위치 |
|---|---|---|
| ESW **5.1 V vs Li/Li⁺**, σ **1.02×10⁻⁴ S/cm** | 폴리플루오로알킬 아크릴레이트 버퍼층(in-situ 무용매 전기중합) NCM811\|PEO — **본문 유일의 ESW 수치** | §4.1 |
| **700 cycles**, CE ≈100 % | Li\|poly-DOL\|LiFePO₄ (DOL 개환 in-situ 중합) | §4.1 |
| **193 mAh/g** 초기, CE **>99 %** | NCM811 + PEGMEA–Li₆PS₅Cl 복합전해질 (3D 다공 LPSCl 골격에 in-situ 중합) | §4.1 |
| 50 cyc **95.2 %** | Li–S 셀, 폴리아크릴로니트릴 복합양극 ↔ LLZO 세라믹 분리막을 "glue" 전해질로 접합 | §4.1 |
| 계면저항 **28배↓** | V₂O₅\|LLZO **마이크로파 솔더링**(수 초 내 선택가열·재응고) | §4.1 |
| SEI 두께 **<5 unit cells** | Al-도핑 LLZO ‖ Li — 국소 상전이지만 **전자절연·이온전도** SEI → 저저항 | §4.2.1 |
| 계면 임피던스 **1710 → 1 Ω cm²** | ALD **Al₂O₃ 5–6 nm** on Li₇La₂.₇₅Ca₀.₂₅Zr₁.₇₅Nb₀.₂₅O₁₂ — 리튬화되어 젖음성 확보 | §4.2.2 |
| **G ≈31 GPa (LiPON) vs ≈3.4 GPa (Li)** ≈ 9배 | **Monroe–Newman 기준**(버퍼층 전단탄성률 ≥ Li의 2배)의 실증 — 덴드라이트 관측 안 됨 | §4.2.2 |
| Si 부피팽창 **≈300–400 %** | 완전 리튬화 시 | §4.2.2 |
| 접착강도 **>24 MPa** | 하이드로탈사이트 나노전도체 하이브리드 SE 바인더 ↔ Al 집전체 | §5 |
| CNT 집전체 **2 µm** | TiS₂ 복합양극 위 용액코팅 컨포멀 집전체 | §5 |

## 5. 섹션별 상세 (전 섹션)

### 5.1 §1 Introduction — 문제 설정 (Fig. 1)
- LIB는 액체가 다공 구조 전체에 스며들어 **퍼콜레이션 이온망**을 자동으로 만든다. SE로 바꾸는
  순간 그 자동성이 사라지고 **모든 접촉점이 계면**이 된다 (**Fig. 1a,b**).
- 핵심 시각 논증 = **Fig. 1c,d**: LIB에서는 Li⁺ 이동 퍼텐셜 장벽이 **전극/전해질 두 지점에만**
  솟는데, SSB에서는 **SE 입자 접촉마다 봉우리가 반복**된다 ("The Li⁺ migration potential
  increases at each interface"). — 우리 언어로 옮기면 *퍼콜레이션 경로의 직렬 저항이 입자 수만큼
  곱해진다*.
- SE 3군 위치: 폴리머(유연·저 σ 10⁻⁷–10⁻⁵) / 무기(σ 10⁻⁴–10⁻², t_Li≈1, **비변형성·대기 불안정**)
  / CSE(둘의 절충). SE 내부에도 GB(다결정)·interphase(CSE) 같은 "내부 계면"이 있다는 점을 강조.

### 5.2 §2.1 Grain Boundaries in Inorganic SEs (Fig. 2) — ★ 2026이 통째로 버린 절
- **측정 문제부터 짚는다**: GB 반원이 안 보이는 SE(LPSCl·LGPS)는 등가회로 분해로 R_GB를
  구해야 하고, 그 배정은 **정전용량 범위(bulk 10⁻¹¹ / GB 10⁻¹⁰–10⁻⁷ / 계면 10⁻⁷–10⁻⁵ F)** 라는
  **경험적 가설**에 기댄다 → *"when the GB semicircle is obscure, the corresponding resistances
  reported by different research groups often vary considerably"* (**Fig. 2a**).
- **재료군별로 GB의 의미가 다르다**:
  - **황화물·할라이드**: 변형성이 커서 **100–300 MPa 냉간가압**만으로 결정립이 밀착 → GB가
    Li 이동을 크게 방해하지 않고 별도 반원도 잘 안 생긴다. 압력이 낮으면(예 **50 MPa**) 기공률↑
    → GB 임피던스↑ → 반원이 나타난다. ⚠ 리뷰 자신이 못박는다: ***"there are few reports on the
    effect of GBs in sulfide and halide SEs so far."*** ← **이 문장이 §10③의 핵심 근거**
  - **산화물**: 취성 → 냉간가압 불가 → **>1100 °C 소결** 필요 → 그렇게 만든 GB가 **저항 덩어리**.
    LLTO 벌크 10⁻³ → 총 10⁻⁵ S/cm; LATP도 1자릿수 손실. 예외는 Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂(GB≈벌크≈10⁻⁴).
- **기전 = 공간전하 + 국소 재구성** (**Fig. 2b,c**): 산화물 GB는 벌크보다 Li⁺ 농도가 낮고
  (Fig. 2b의 초록 곡선이 GB에서 급강하) 그 결과 **E_a(GB) > E_a(G)** (Fig. 2c). 원자수준으로는
  Cs-corrected STEM이 LLTO GB 대부분에서 **국소 구조 재구성**을 보였고 — 재구성된 GB는
  페로브스카이트가 아니라 **Ti–O 층**이라 Li가 거의 못 지나간다. 반면 garnet은 재구성이 없고
  EELS로도 벌크와 차이가 없다 → GB 저항도 낮다.
  - 리뷰가 남긴 **열린 질문**: 왜 페로브스카이트만 재구성되나? → *"remains an open question"*,
    가설은 **대칭성**(garnet=cubic이라 인접 결정립 배향차를 흡수 / LLTO=단범위 정렬 정방정).
- **GB 개선 레버 3개**: ① 불순물상 억제(LLZTO에 LiF 도입 → Li₂CO₃ 억제·Li–Al–O 안정) ②
  **비정질화**(SiO₂로 LLTO GB 비정질화 → 이방성 제거; **B로 LiTi₂(PO₄)₃ GB 유리화 → σ
  1.12×10⁻⁴ → 1.03×10⁻³ S/cm, 벌크 저항은 거의 불변**) ③ **도핑으로 공간전하 전위 낮추기**
  (Nb-LLTO GB σ ×2–3).
- 방법론적 한계 자백: SE는 전자빔에 극도로 민감해 원자분해능 관찰이 **페로브스카이트 계열
  하나만** 체계적으로 됐다. 저선량 현미경 개발이 필요.

### 5.3 §2.2 Interfaces within Composite SEs (Fig. 3) — ★ 2026에 대응 절 없음
- **폴리머-매트릭스 CSE**: 무기 필러 표면에 **Lewis 산–염기 상호작용** → 필러 주위에 Stern층 +
  확산(Gouy–Chapman)층 = **공간전하층** (**Fig. 3a**). 두 효과: (i) 폴리머 사슬 결정화를 kinetic하게
  방해 → 세그먼트 운동↑ (ii) Li 염 해리 촉진 → 자유 Li⁺ 농도 n↑. 결과적으로 σ = q·n·µ 에서
  **n과 µ 둘 다** 올린다.
- **필러 함량의 최적점** (**Fig. 3b**, figure-read): σ vs 필러 wt% 곡선이 **최댓값을 지나 꺾인다** —
  A(필러 없음) → B(계면층이 연속 퍼콜레이션) → 그 이상은 **응집**으로 경로 파괴. B에서 E_a가
  A의 절반 수준으로 떨어진다(Fig. 3c 표).
  ⚠ **이게 이 리뷰에 있는 유일한 명시적 trade-off 곡선이다** (→ §10④·B1).
- 필러 형상: 나노입자보다 **나노섬유·나노와이어·2D 시트**(고종횡비)가 더 긴 연속 계면망을 만든다
  (LLTO 섬유 > LLTO 입자; 버미큘라이트 시트 → σ ~2자릿수↑).
- 필러 표면 상태가 결정적: **LLZO 표면의 LiOH·Li₂CO₃**(공기 중 수분·CO₂ 반응)가 있으면
  활성 필러가 오히려 죽는다. 반대로 Stern층이 너무 강하면 SE 입자가 전도에서 **차폐**되어
  불활성 필러처럼 행동.
- 상호작용 설계 사례: 실란 커플링제로 LGPS–PEG 화학결합(**9.83×10⁻⁴ S/cm, t_Li⁺ 0.68**);
  flyash의 산소공공이 TFSI⁻를 고정 → t_Li⁺·ESW 동시 개선; MXene-mSiO₂ 나노시트(−F/−OH)로
  **4.6×10⁻⁴ S/cm** + 기계강도 동시 확보.
- **황화물·할라이드 매트릭스 CSE** (**Fig. 3d,e**): 여기선 폴리머가 **바인더에 불과**하고 무기
  SE 입자망이 3D 연속상이다. 산화물은 이 용도에 부적합 — 비변형성이라 밀착이 안 되고
  **바인더를 더 넣어야 해서 σ가 크게 깎인다**. Fig. 3e = Li₆PS₅Cl + PVDF-co-TrFE CSE의 SEM
  (스케일바 10 µm, figure-read: 입자 경계가 뭉개진 치밀한 파단면).

### 5.4 §3.1 복합전극의 물리적 접촉 (Fig. 4a,b)
- 무기 SE 복합전극(**Fig. 4a**): AMP 주위에 SE 입자가 **확률적으로** 쌓여 퍼콜레이션 이온망을
  만들지만 **느슨한 패킹의 공극**이 확산을 막고 계면저항을 키운다. 사이클 중 AMP 부피변화
  (인터칼레이션형 or 변환형)가 **균열·박리(delamination)** 를 만들고 → 계면 임피던스↑ → 셀 실패.
- 폴리머-매트릭스 복합전극(**Fig. 4b**): 밀착은 쉬우나 탄성이 나빠 팽창–수축 후 **소성변형이
  남아 void**가 생긴다. → 고탄성(resilience 0.32 MJ/cm³) 엘라스토머로 해결한 예.
- **압력의 역할**: 황화물·할라이드는 소성변형으로 냉간가압만으로도 밀착. 85 °C 정도의
  **완만한 승온 가압**을 더하면 치밀화가 더 진행 — 초기용량 **81 → 103 mAh/g**, 50 cyc **91.7 %**.
  Si 음극은 AMP 위에 **컨포멀 Li₆PS₅Cl 층**을 코팅해 복합음극 내 SE 양을 줄이고 에너지밀도↑.
- **Table 1** = 압력↔성능 데이터 15행 (자세히 §6).

### 5.5 §3.2 복합전극의 (전기)화학 안정성 (Fig. 4c,d · Table 2)
- **F3 프레임**(**Fig. 4c**): 3패널 에너지 도식. (좌) μ_c(CAMP) > HOMO(황화물) → 산화 없음, 열역학
  안정. (중) μ_c < HOMO → 산화 → **CEI** 생성; 그 CEI의 HOMO가 μ_c보다 **낮으면 "Stable"**
  (자기제한), **높으면 "Unstable"**(연속 반응). (우) **코팅**의 HOMO가 μ_c보다 낮으면 계 전체 안정.
  → **Fig. 4d**: 표면코팅이 CAMP와 황화물의 직접 접촉을 끊어 "stable, conductive interface" 확보.
  ⚠ 리뷰는 **HOMO/LUMO(분자 용어)** 로 고체 SE의 밴드엣지를 부른다. 우리(그리고 리뷰어 노트
  B2)는 이걸 **VBM/CBM**으로 써야 한다고 본다 → §10④·§14.
- 구체 실패 사례 2개: (i) LiCoO₂의 산화 화학퍼텐셜 > PEO-매트릭스 SE의 anodic 한계 → PEO 분해
  + LCO의 self-oxygen-release → 급속 열화. (ii) **LiCoO₂/Li₂S–P₂S₅ 계면에서 Co·P·S 상호확산**
  → 원치 않는 계면상. **할라이드 SE는 산화물 CAM에 대해 전기화학적으로 안정해 코팅이 불필요
  하지만, 그런 SE는 드물다** → 대부분은 코팅이나 안정 catholyte로 계면을 손봐야 한다.
- **CAM 코팅 6조건 rubric**(§3에 기재; 위 §3 표) + **Table 2** = 코팅 19행 카탈로그.
- 폴리머 catholyte 쪽: **LLZO 입자를 PEO에 넣으면 산화한계가 ≈5 V로 확장** → NCM622 셀
  70 °C/4.2 V cutoff에서 **160 mAh/g @C/20**. PEO 대신 **폴리(프로필렌 카보네이트)** 로 바꾸면
  catholyte 산화 억제로 사이클 개선. ⚠ 다만 **전자전도성 카본이 고전압에서 PEO 분해를 가속**한다.

### 5.6 §4.1 양극 | SE 분리막 계면 (Fig. 5a–d)
- 문제 5개를 한 그림에 번호로 박아둔 것이 **Fig. 5a**: ① 양극/SE 접촉 불량 ② 양극측 부반응
  ③ 음극/SE 접촉 불량 ④ **Li 덴드라이트** ⑤ 음극측 부반응.
- 해법 4갈래:
  - **in-situ 중합** (**Fig. 5b**): DOL 개환중합 poly-DOL(700 cyc, CE≈100 %); **PEGMEA를 3D 다공
    Li₆PS₅Cl 골격 + 양극 사이에 in-situ 중합** → 양극/LPSCl 계면 void 제거, LPSCl 골격이 고속
    이온경로 담당 → NCM811 셀 **193 mAh/g**, CE **>99 %**.
  - **버퍼층** (**Fig. 5c**): 요구조건 = 양쪽에 대한 젖음성·강한 접착·고 σ_ion·화학/전기화학 안정.
    사례 = 폴리플루오로알킬 아크릴레이트 in-situ 전기중합(**ESW 5.1 V**, σ 1.02×10⁻⁴ S/cm,
    "공간전하 효과를 크게 억제"); ex-situ PMA 층으로 PEO를 LiCoO₂ 고전압 산화로부터 보호.
  - **외부 자극** (**Fig. 5d**): 전기열 어닐링(V₂O₅\|LLZO 임피던스 급감), **마이크로파 솔더링**
    (선택가열로 V₂O₅ 표면만 수 초 내 용융·재응고 → 계면저항 **28배↓**).
  - **3D 구조화**: 양극/SE 접촉 면적을 기하학적으로 늘리기.
- ⚠ 산화물 세라믹 분리막의 근본 한계 자백: 강성이 커서 전극 부피변화를 못 버틴다 → 장기
  사이클에서 균열·박리 **불가피**; 고온 공정 때문에 벌크 SSB 제작 자체가 어렵다 → 오히려
  **박막 마이크로배터리**나 **저온 동시소성 다층 세라믹**이 맞는 무대다.

### 5.7 §4.2.1 음극 | SE 계면 — (전기)화학 안정성 ★ F2 분류 (Table 3)
- **F2 3분류**(원문 그대로): ① **thermodynamically stable interface** — SE가 Li에 화학적으로
  불활성, 새 상 없음. *"most desired, but is extremely rare."* ② **MCI** — 이온·전자 둘 다 통해
  음극이 계속 리튬화·환원 진행 → **"SE 또는 음극이 완전히 소모될 때까지 성장이 멈추지 않는다"**
  → *"completely unacceptable for SSB operation."* ③ **SEI형** — 이온은 통하고 전자는 막아
  자기제한; σ_ion만 충분하면 실전 성능이 나온다.
- **Li에 열역학적으로 안정한 것은 이성분 Li 화합물뿐**: **LiF, LiCl, LiBr, Li₂O, Li₂S, LiH, Li₃N**.
  그러나 σ가 너무 낮아 SE로는 못 쓰고 **얇은 보호층**으로만 쓴다. 그 밖 대부분의 무기 SE는
  MCI나 SEI를 만든다 — 원인은 **고원자가 양이온(P⁵⁺, Ge⁴⁺, Ta⁵⁺, Ti⁴⁺, In³⁺)** 이 LLZO·LLTO·
  NASICON·황화물·할라이드에 폭넓게 들어 있기 때문.
- **자기제한(=③)의 실례**: Al-LLZO ‖ Li → 국소 상전이가 나지만 생성층이 **전자절연·이온전도**
  이고 두께가 **5 unit cell 미만** → 저항 문제 없음. **Li₇P₃S₁₁·Li₆PS₅Cl** 도 "benign" — *"none of
  their reduction products is highly electronically conductive"*.
- 폴리머도 안전하지 않다: PEO는 Li와 **C₂H₄ + H₂ 로 분해**되고 Li₂O 함유 계면상 형성 → 임피던스↑.
  PVDF는 잔류 용매–Li 반응에서 나온 라디칼 공격으로 **탈불화(dehydrofluorination)**.
- **버퍼층 전략** (**Fig. 5e**, 3종): (좌) **protective layer**(부반응 차단) (중) **lithiophilic layer**
  (Li⁺ flux 균질화·젖음) (우) **stiff layer**(덴드라이트 물리 차단). 사례: LGPS ‖ Li 사이에
  **Li₅.₅PS₄.₅Cl₁.₅**(Cl-rich argyrodite!)·Ag·LiH₂PO₄·plastic crystal; **Li₃YCl₆ ‖ Li 는 Li₆PS₅Cl 얇은
  층으로 보호** — Li₆PS₅Cl의 계면상은 전자전도가 나빠 자기제한이지만, Li₃YCl₆는 그대로 두면
  혼성전도 계면상이 **계속 자란다**. 산화물은 문제가 달라서 **lithiophilicity**가 관건.
- **in-situ 형성 버퍼층** (Table 3 후반): **LiF/Li₃N-rich** 층이 폴리머·할라이드·황화물 전반에서
  통한다. 폴리머계는 LiNO₃·Li₂S·**Li₂MgCl₄** 첨가로 염 분해를 유도(→ Li⁺ 전도·전자절연 층,
  **CCD 상승**); PVDF의 결합잔류용매(DMF)–Li 라디칼 반응으로 **LiF-rich mosaic** 층; 무기계는
  **F 도핑**(F-doped bromide SE → **LiF/YF_x** 층)이 인위 불화층보다 균질성·밀착에서 우수.

### 5.8 §4.2.2 Li 덴드라이트 (Fig. 5e–g)
- 원인 4갈래: ① **stripping 속도 > Li 자기확산** → 접촉면적 감소 → 국소전류 집중 → hotspot
  ② SE의 **낮은 젖음성** → 애초에 밀착이 안 됨 ③ SE 고유물성 — *"electronic conductivity and
  elastic modulus are two critical factors. If the SE exhibits lower electronic conductivity and
  higher elastic modulus, the dendrites would be more difficult to form and grow."* ④ **압력** —
  **너무 높으면 연성 Li이 SE를 뚫고 크리프해 즉시/조기 단락**.
- **Monroe–Newman 기준을 명시적으로 인용**: 버퍼층의 전단탄성률이 **Li의 최소 2배**여야 한다 →
  LiPON 박막(**G ≈31 GPa**, Li의 ≈3.4 GPa 대비 ~9배)을 스퍼터로 Li 위에 올려 **덴드라이트 미관측**.
- **음극 형태 설계**: 평면 Li은 접촉면적이 작고 덴드라이트가 계면에 **수직**으로 자라 SE를 뚫는다
  → **3D / 수직정렬 음극**(**Fig. 5f**)이 접촉면적을 늘릴 뿐 아니라 **성장 방향을 옆으로 돌린다**
  (lithiophilic microwall로 측면 성장 유도, 3D Li–Ni 복합).
- **대체 음극** (**Fig. 5g**, figure-read: 축에 눈금 숫자 없음 — 순서만 읽을 수 있는 정성 산포도):
  평형전위(V vs Li/Li⁺) vs 비용량. 위에서부터 **Li–In > Li–Sn > Li–Al ≈ Si > Li–Zn > graphite >
  Li–Mg > Li metal(0 V, 최대 용량)**. 합금 음극의 장점 3개 = SE 분해 회피(전위가 높아서)·
  Li 확산계수↑·젖음성↑. **Li₀.₈Al**은 LGPS와 호환이 좋아 LGPS의 환원분해를 막는다.
  **Si**는 SEI가 안정·부동태화라는 장점이 있으나 **≈300–400 % 팽창**으로 분쇄·전극 균열.

### 5.9 §5 집전체 | 전극 계면 ★ 2026에 대응 절 없음
- 상용 LIB에 없는 문제: 황화물 복합양극은 표면이 거칠어 **평활한 Al 포일과 사이에 간극**이 생긴다
  → 접촉면적↓·계면저항↑.
- 해법: **CNT 집전체**(유연·전기적 우수, Al보다 접착 훨씬 강함; 입자 사이 간극을 CNT가 채운다),
  TiS₂ 복합양극 위 **2 µm CNT 컨포멀 층**, 전극 한쪽 면에 전자전도 나노와이어+rGO를 넣은
  **gradient 복합양극**(= 집전체 일체형).
- ⚠ **할라이드 SE의 Al 부식**: **Li₃InCl₆는 Al 금속과 반응해 자신이 분해되고 Al 집전체를 부식시킨다.**
  → Al 집전체에 **탄소 코팅**을 넣어 직접 접촉을 막으면 율속·가역용량·분극·사이클 모두 개선.
- 하이브리드 SE 바인더(하이드로탈사이트 나노전도체 + PVA-g-피롤-2-카복실산 + LiTFSI + 이온액체)
  의 **−OH 수소결합**으로 양극\|Al 접착강도 **>24 MPa**.
- **Li ‖ Cu**: Li 포일은 점착성이 커서 롤투롤 라미네이션이 어렵다 → 실리콘 오일 처리 PET 보조막
  또는 **Cu 위 Li 증착/스퍼터링**.

### 5.10 §6 Outlook — 5방향 (Fig. 6)
1. **Conductive, dynamically stable interfaces** — 저저항 + 장기 내성. ⚠ 자기비판이 날카롭다:
   *"proof-of-concept solid-state cells reported in the literature use a low mass loading of active
   materials and an overly thick layer for the SE separators… their energy densities are not
   competitive."* 로딩을 실전 수준으로 올리면 **복합양극 계면 문제가 더 두드러진다**, 특히
   나노 활물질에서 → **동적 접촉 유지**가 관건.
2. **In situ / operando 특성화** — operando STEM-EELS, in-situ/operando X-ray CT, 중성자 심도
   프로파일링, in-situ MRI. 아직 소수 재료계만 적용됨.
3. **Theoretical calculations** — *"density functional theory-based calculations, ab initio molecular
   dynamics, finite elemental modeling"* 으로 계면 반응·진화 예측, **Li plating/stripping 거동**,
   **공간전하층 효과**, 코팅재 탐색. **고처리량 + 대형 계산 DB** 필요, **멀티스케일 시뮬 + 실험 통합** 필요.
   ← ⭐ 이 한 문단이 이 리뷰의 계산 관련 서술 **전부**다.
4. **Novel battery configurations** — **anode-free**(에너지밀도·안전; 현재 CE·가역성 부족),
   **monolithic** 구성(황화물이 활물질과 전해질을 겸함 → redox 활성점↑ + 양극/SE 계면반응 회피).
5. **Large-scale interface engineering technologies** — 단일 공정 체인이 모든 SSB에 통하지 않는다;
   저비용·확장 가능한 계면 개질 기술이 양산의 관건.

## 6. Table 1·2·3 — 이 리뷰의 진짜 자산

### Table 1 — 압력 ↔ 사이클 성능 (황화물·할라이드 SE, 15행)
열: SE / 음극‖양극 / **양극 제조압 [MPa]** / **시험조건 (T / P [MPa])** / 율속·전류밀도 / 수명(cycle) / 유지율 / Ref.
- **제조압 범위 50–510 MPa**, 시험압 2–150 MPa. 이 표가 곧 "SSB 랩 데이터는 압력 없이 못 읽는다"의 증거.
- ⭐ **압력 직접 대조 행 (ref [40])**: Li₆PS₅Cl, Li–In‖NCA — **50 MPa → 40 cyc "Low"** vs
  **370 MPa → "High"**. (숫자 대신 High/Low로만 적힌 유일한 행)
- ⭐ **공정온도 대조 행 (ref [102])**: (Li₂S)₈(P₂S₅)₂(Ni₃S₂)₁ — 500 MPa **냉간가압 61.5 %** vs
  냉간가압 후 **85 °C·500 MPa 추가가압 91.7 %** (50 cyc).
- 최장수명: **Li₆PS₅Cl(CSE, PVDF-co-TrFE) — 20 000 cyc / 71 %** @1.61 C, 1.0 mA cm⁻², 시험압 100 MPa.
- 할라이드: Li₃InCl₆ 94 %(50 cyc, 80 °C/2 MPa) · Li₃YCl₆ **96.8 %**(200 cyc, 30 °C/70 MPa).

### Table 2 — CAM 코팅 카탈로그 (19행)
열: 양극 / **코팅** / 복합양극 내 SE / 음극 / 시험 T / 전압창 / 율속 / 수명 / 유지율 / Ref.
- **LiNbO₃가 압도적 다수(8행)**. 그 외 Li₂WO₄, Li₂CoTi₃O₈, **LLTO 3종**(Li₀.₃₅La₀.₅Sr₀.₀₅TiO₃,
  Li₀.₅La₀.₅TiO₃, Li₀.₃₅La₀.₅₅TiO₃), **LATP**(±cyclized PAN), Li₂CO₃/LiNbO₃, **TiNb₂O₇**, LiOH,
  NCM811@LiCoO₂, **LiTaO₃**.
- 전압창은 대개 Li–In 기준(2.2–3.6 V ≈ 2.8–4.2 V vs Li/Li⁺). 최고 율속 행: LiNbO₃/LiCoO₂/
  Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃/LTO @100 °C — **18 C / 12 mA cm⁻², 500 cyc, 75 %**.
- ⚠ **코팅 두께는 대부분 열에 없다**(본문에만 5–6 nm 식으로 산발). B4형 결함.

### Table 3 — Li‖SE 버퍼층 카탈로그 (27행) ★ 우리 SEI 축과 가장 가까움
열: SE / **버퍼층** / Li‖Li 셀 조건(전류밀도 & 용량, T) / **지속시간 [h]** / Ref.
- **황화물 SE 행 6개**: LGPS+**Ag**(1000 h) · LGPS+**Li₅.₅PS₄.₅Cl₁.₅**(1800 h) · LGPS+LiH₂PO₄(~950 h)
  · LGPS+plastic crystal(250 h) · Li₃PS₄+Li_xSiS_y(**2000 h**) · Li₇P₃S₁₁+**LiF**(200 h).
- **할라이드 행 2개**: **Li₃YCl₆ + Li₆PS₅Cl (1000 h)** · Li₃YBr₅.₇F₀.₃ + **LiF/YF_x** (1000 h).
- 산화물(LLZO/LLZTO/LATP/LAGP) 12행: Zn–Li–N–O(**5500 h** 최장) · Au · Li-Al 합금(3000 h) · Ge ·
  **Al₂O₃** · ZnO · SnF₂ · **LiF** · **Li₃N** · graphite · Li₃N/Cu · PEO/BN.
- 폴리머 7행: 버퍼가 거의 전부 **LiF 또는 Li₃N(또는 둘 다)** — Li₂MgCl₄/LiF · Li₃N/LiF ·
  Li₃PS₄/Li₂S/LiF(**3475 h**) 등.
- 🔑 **패턴**: 27행 중 **LiF 계열 8행 · Li₃N 계열 4행** — 즉 리뷰가 "이상적 SEI"라 부르는 것의
  실체는 대부분 **wide-gap 이성분 Li 염**이다. 우리 `b2o3_sei_gaps.json`의 서열이 겨루는 대상이
  바로 이 목록이다.
- 🔑 **Cl-rich argyrodite가 "버퍼층"으로 등장한다**(LGPS + Li₅.₅PS₄.₅Cl₁.₅, 1800 h) — 우리
  modelc(Li₅.₄PS₄.₄Cl₁.₆)와 사실상 같은 조성이 **음극 보호막**으로 쓰인 문헌 좌표.

## 7. Figure set ★

> ✅ **6장 전부 실제로 Read 로 봤다** (fig_1 ~ fig_6) — 2026-08-05 최초, **2026-08-06 inbox #56 재투입 때 6장 전부 다시 봄**(그림 파일은 재추출해도 동일). 표 3장(tab_1·tab_2·tab_3.png)은 이미지로 안
> 보고 PDF 텍스트로 전사했다(관례 — 표는 텍스트가 정확). 그림에서만 읽은 값은 **figure-read ≈** 표기.

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| **1a,b** | LIB(액체가 전 셀에 스며 액체–고체 계면) vs SSB 2종(복합전극+SE층 / 복합양극+SE+Li금속). 붉은 원으로 "고체–고체 계면"을 찍어 강조 | 발표 오프닝 — "계면 개수가 폭증한다"의 한 장 |
| **1c,d** | ★ Li⁺ **migration potential** 프로파일: LIB는 전극 양끝 **두 봉우리만**, SSB는 SE 입자 접촉마다 **주기적 봉우리**. 캡션 명시: "The Li⁺ migration potential increases at each interface" | 우리 BVSE 채널·퍼콜레이션 서사의 **정성 만화판** — "직렬 장벽이 입자 수만큼" 프레임 차용 |
| **2a** | Nyquist 도식 3종. **정정(2026-08-06 재열람)**: 왼쪽 붉은 선(**황화물 고압**)은 원점 근처에서 바로 솟는 **거의 수직선 — 반원이 아예 없다**; 두 번째 붉은 선(**황화물 저압**)의 발치에만 **작은 반원 1개**가 붙고 거기에 `R_GB` 화살표가 달려 있다; 파란 선(**산화물**)은 **R_b 반원 + 그보다 큰 R_GB 반원 2개**. 즉 그림이 본문("고압에서는 별도 반원이 생기지 않는다 / 50 MPa 저압이면 반원이 나타난다")과 **정확히 일치**한다. figure-read: **축에 눈금 숫자 없음**(순수 도식) | EIS 해석 규율 — "GB 반원이 안 보이면 R_GB는 등가회로 가정에 의존" 인용. 압력↔GB 반원 유무는 **Table 1의 50 MPa vs 370 MPa 행과 같은 축**이다 |
| **2b,c** | GB에서 **Li⁺ 농도 급감**(b, 초록) → **E_a(GB) ≫ E_a(G)**(c, 주기 퍼텐셜 + GB 봉우리 1개) | 공간전하층의 **표준 교과서 그림**. 우리 T3/GB 논의의 정성 기준선 (⚠ 숫자 0개 — §11.3) |
| **3a** | 폴리머-매트릭스 CSE + 필러 주위 **Lewis 산–염기** + Stern층/확산층 확대도 | CSE 계면 어휘 (우리 축 아님, 배경) |
| **3b,c** | ★ **σ vs 필러 함량 곡선에 최댓값**(A=무필러 → B=퍼콜레이션 → 그 이상 응집으로 감소) + Arrhenius A/B 2선 + **E_a 표**(PEO/LiClO₄ ~1.0→~0.5 eV 등, figure-read) | **이 리뷰의 유일한 명시적 trade-off 그림** — 리뷰어 노트 B1에서 "당신 그룹은 2023에 이런 곡선을 그렸다"의 근거 |
| **3d,e** | 황화물/할라이드-매트릭스 CSE 도식(무기 입자가 연속상, 폴리머는 바인더) + Li₆PS₅Cl+PVDF-co-TrFE SEM(스케일바 10 µm) | 황화물 CSE = 바인더 최소화 논리 |
| **4a,b** | 무기 SE 복합전극(공극 → 사이클 후 **균열 / 박리**) vs 폴리머-매트릭스(팽창–수축 후 **소성변형 → void**) | 우리 DEM/기계 축과 어휘 공유; "같은 실패를 두 매트릭스가 다르게 낸다" |
| **4c** | ★★ **μ_c ↔ HOMO 3패널**: (좌) μ_c > HOMO(황화물) = 안정 / (중) μ_c < HOMO → **CEI**; CEI HOMO < μ_c면 Stable, > μ_c면 **Unstable** / (우) **코팅** HOMO < μ_c = 안정. E_g가 sulfide 밴드 폭으로 그려짐 | **우리 grand-potential ESW의 "정성 사촌"** — 발표에서 두 프레임을 나란히 놓기 좋음. ⚠ HOMO/LUMO 용어 = 고체엔 VBM/CBM (§14) |
| **4d** | 코팅 없는 CAMP/황화물(붉은 분해층이 Li⁺ 통과 차단) → 표면코팅 후 "stable, conductive interface" | 코팅 전략의 한 컷 |
| **5a** | ★ 전극–SE 계면 문제 **①–⑤ 번호 지도**: ①양극접촉불량 ②양극부반응 ③음극접촉불량 ④Li 덴드라이트 ⑤음극부반응 | 리뷰 전체의 문제 번호체계 — 우리 계면 논의 목차로 재사용 가능 |
| **5b,c,d** | 해법: in-situ 중합(b) / 양극-분리막 버퍼층(c) / **외부자극(가열)** 으로 접합(d) | (d)의 마이크로파 솔더링(계면저항 28배↓)은 우리 문헌에 드문 접근 |
| **5e** | ★ 음극측 버퍼 **3종 기능 분류**: protective(부반응 차단) / lithiophilic(균일 Li⁺ flux) / **stiff**(덴드라이트 물리차단) | 우리 SEI 산물 라벨링에 그대로 이식 가능한 3-way 태그 |
| **5f** | 3D 음극(격자형)으로 균일 Li⁺ flux | 기하 해법 축 |
| **5g** | 대체 음극 산포: 평형전위 vs 비용량. figure-read 순서 **Li–In > Li–Sn > Li–Al ≈ Si > Li–Zn > graphite > Li–Mg > Li(0 V)**. ⚠ **축에 눈금 숫자 전혀 없음** — 정성 배치도 | Li–In 기준전위 논의 시 인용(단 수치 인용 불가) |
| **6** | Outlook 5방향 그래픽: 전도성·동적 안정 계면 / in-situ·operando / **이론계산**(원자구조 그림) / anode-free / 대면적 계면공학 → "Interface optimization" 화살표 → SSB | **2026 원고의 §6 미래방향과 1:1 대조표를 만들 근거** (§10②) |
| Table 1 | 압력 ↔ 사이클 성능 15행 (제조압 50–510 MPa, 시험압 2–150 MPa) | **B5 근거 #1** + 우리 기계축(압력) 문헌 좌표 |
| Table 2 | CAM 코팅 19행 (LiNbO₃ 8행 등) | **B5 근거 #2** + [Sundar] 코팅 스크리닝과 대조 |
| Table 3 | Li‖SE 버퍼층 27행 (**LiF 8 · Li₃N 4**; LGPS+**Li₅.₅PS₄.₅Cl₁.₅** 1800 h) | **B5 근거 #3** + 우리 `b2o3_sei_gaps.json` 서열의 비교 대상 |

## 8. DFT/계산 방법 ★

**해당 없음 — 이 리뷰는 자체 계산을 하지 않는다.** 규율상 명시해 둔다:

| 항목 | 내용 |
|---|---|
| code / functional / pseudo / k-points / ecut / supercell | **n/a** (계산 없음) |
| DFT+U / AIMD / MLIP / 무질서 처리 | **n/a** |
| 본문 내 계산 관련 단어 빈도 | `DFT` **0회** · `first-principles` **0회** · `band gap` **0회** · `VBM/CBM` **0회** · `ab initio` **1회**(Outlook) · `simulation` 3회 · `calculation` 6회(대부분 Outlook) |
| 계산이 등장하는 유일한 자리 | §6 Outlook 3) *Theoretical calculations* — DFT / AIMD / **finite element modeling** 이 계면 반응·진화 예측, **Li plating/stripping**, **공간전하층 효과**, 코팅재 탐색에 쓰였다고 **한 문단**으로 소개하고 "고처리량 + 대형 DB + 멀티스케일 + 실험 통합"을 요구 |
| 인용된 계산 문헌(참조번호만) | [88] [249–256] (본문에 결과값 전재 없음) |
| **소환된 유일한 이론 기준** | **Monroe–Newman** — 버퍼층 전단탄성률 ≥ 2×G(Li) (ref [210]) |

> 🔎 **함의**: 우리 물성 4축(σ·ESW·기계·전자구조)의 **어떤 숫자도 이 논문에서 가져올 수 없다.**
> 가져올 것은 **분류·어휘·표 양식·문제 번호체계**뿐이다. `comparison_vs_ours.md`에도 수치 행이
> 아니라 **프레임 행**으로 들어간다.

## 9. Post-processing ★

리뷰가 **다루는(=자기가 하지 않고 소개하는)** 특성화·후처리:

- **EIS / 등가회로 분해** — Nyquist에서 R_b·R_GB·R_interface 배정. 배정 기준은 **정전용량 범위**
  (bulk ≈10⁻¹¹ / GB ≈10⁻¹⁰–10⁻⁷ / 계면 ≈10⁻⁷–10⁻⁵ F, 1 cm ⌀ × 1 mm 펠릿). ⚠ 리뷰가 스스로
  *"largely based on empirical hypotheses"* 라고 못박고, 그래서 그룹 간 R_GB가 크게 다르다고 경고.
  → **이게 이 리뷰에서 가장 방법론적으로 성숙한 한 문단**이다 (B4의 모범).
- **Cs-corrected STEM (HAADF)** — LLTO GB의 국소 재구성(Ti–O 층) 관찰. **전자빔 손상**이
  대상 SE를 사실상 페로브스카이트 하나로 제한한다는 자백 + **저선량 기법 개발 요구**.
- **HRTEM + EELS** — garnet GB가 벌크와 구조·전자상태 차이 없음을 보임.
- **ALD** — Al₂O₃ 5–6 nm를 LLZO계 SE 표면에 (계면저항 1710→1 Ω cm²).
- **마그네트론 스퍼터링** — LiPON 박막(G ≈31 GPa).
- **Outlook에서만 언급**: operando STEM-EELS · in-situ/operando X-ray CT · 중성자 심도
  프로파일링 · in-situ MRI.
- **도구·수치화 방식**: pymatgen/LOBSTER/VESTA류 언급 **없음**. 정량 플롯도 없음(모든 Figure가
  스키매틱; 유일한 실측 이미지는 **Fig. 3e** SEM 한 장).

## 10. ★★ 2023(본 논문) ↔ 2026(ECER-D-26-00097) 대조 — 같은 그룹, 3년 간격

> 두 리뷰의 공통 저자 = **Ce-Wen Nan** (2023 교신 / 2026 공저). 2023 = Tsinghua 단독 주도,
> 2026 = USTB(Fan Li-Zhen) 주도 + Tsinghua(Nan) 참여. **주도권이 옮겨간 상태의 후속작**으로 읽어야
> 정확하다 — 아래 ③의 누락 상당수는 "Nan 그룹이 버렸다"기보다 "USTB 주도로 축이 바뀌었다"에 가깝다.

### ① 2026이 **이어받은** 것 (직계 상속 — 출처 명시 없이)

| 상속 항목 | 2023 (본 논문) | 2026 (ECER-D-26-00097) | 비고 |
|---|---|---|---|
| **F2 계면 3분류** | §4.2.1: 열역학 안정 / **MCI** / SEI형 — 정의·판정·"MCI는 수용 불가"까지 | §3.4: "계면 3유형 = 안정 / MCI / passivated" (Wenzel ref 116 인용) | **어휘·순서·결론이 동일**. 2023은 [8,154]를, 2026은 [116]을 근거로 달았을 뿐 |
| **F3 μ_c ↔ HOMO 정렬** | **Fig. 4c** 3패널 도식 (CEI/코팅 HOMO 조건까지) | §4.1.3 ①: "충전 시 양극 전기화학퍼텐셜이 황화물 **HOMO 아래**로 → 전자 이동 = 산화분해" | **동일 프레임·동일 용어**(HOMO). 2026의 HOMO 용법은 신조어가 아니라 **그룹의 2023년 관례**다 → **B2 지적의 성격이 바뀐다**(오타가 아니라 house convention) |
| **Li에 안정한 것은 이성분 Li 화합물뿐** | §4.2.1: LiF·LiCl·LiBr·Li₂O·Li₂S·LiH·Li₃N — "σ 낮아 보호층으로만" | §5.2.2/5.2.3: 할로겐/F/LiI 도핑 → **in-situ Li-halide/불화물 SEI**; LiF-rich SEI 사다리 | 2026은 같은 명제를 **"그럼 in-situ로 만들자"** 로 전개 = 진짜 진전 |
| **자기제한 SEI = 목표, 전자절연이 조건** | §4.2.1: "SEI가 σ_ion만 충분하면 실전 성능이 나온다" | §5.2.3 이상 SEI 4조건 중 ③ **고유 전자절연** | 조건 목록 형태로 승격 |
| **코팅 rubric(체크리스트) 양식** | §3.2 **6조건** (균일·박막·σ_ion·부피변화 내성·화학안정·**양산성**) | §4.2.2 **4조건** (고전압 안정·σ_ion·**최소 σ_e**·기계 유연) + 두께 정밀제어 | ⚠ 항목이 **바뀌었다** → ③·④ 참조 |
| **압력의 양면성** | §4.2.2: "압력이 너무 높으면 연성 Li이 SE를 크리프 관통해 단락" + Table 1의 제조압/시험압 | §5.1.4: **stack pressure window**(하한=공극, 상한=GB 압출) + 변형기구 지도로 최적압 예측 | 2023의 경험적 관찰 → 2026의 **설계 창** 으로 정식화 = 진짜 진전 |
| **Outlook 항목 → 2026 본문** | ①동적 안정 계면 ③이론계산 ④anode-free·**monolithic** ⑤대면적 공정 | ①→미래방향①(intrinsic stability) ③→**본문 전체의 계산 콘텐츠** ④→§5.2.1 anode-free + §4.2.3 **"cathode homogenization"(=monolithic의 후신)** ⑤→§3.2 dry electrode·§3.5 시트화 | 🔑 **2026 원고는 상당 부분 "2023 outlook의 이행보고서"** 다 |

### ② 2026에만 **새로 들어온** 것

| 신규 축 | 2023에서의 상태 | 우리에게 중요한가 |
|---|---|---|
| **재료 고유 안정성 5축 전체** (공기·용매·열·전기화학·기계) | **사실상 0** — 본문 전체에서 `H₂S` 0회 · `HSAB` 0회 · `bond energy` 0회 · `fracture/toughness` 0회 · `Young` 0회 · `air` 2회(스치듯) · 용매는 "무용매 중합" 문맥 2회 · thermal은 "열 어닐링 접합" 문맥뿐 | ⭐⭐ 2026의 진짜 신규 기여. 우리 free-S/O-doping/B₂O₃ 서사가 꽂히는 칸이 **전부 여기** |
| **정량 ESW / 열역학 창** | **없음**(무기 SE ESW 수치 0개; 유일 ESW는 폴리머 버퍼 5.1 V) | ⭐⭐ 우리 grand-potential 2.256 V가 겨룰 상대는 **2026뿐** |
| **덴드라이트 wedge-opening 기전**(Ning 2023) · SEI 내부 dead-Li 핵생성(MD) | 없음(2023 온라인 게재 시점에 원전이 갓 나옴) | ⭐ §10④ 참조 |
| **서술자 계열**(Th₀/Th′ 열안정 · ionization level 덴드라이트) | 없음 | ⭐⭐ 우리 SEI-gap 지표의 형제 |
| **신규 CAM**(할라이드 Li₁.₃Fe₁.₂Cl₄·FeS₂·S–Se 균질화) | Outlook 4)의 "monolithic" 한 줄이 씨앗 | ○ |
| **anode-free 정량**(Ag 층 두께 진화·A/C 비) | Outlook 4)의 한 문단 | ○ |
| **건식전극 / 용매 공정** | 언급 1회("mixing and dry-coating/pressing") | ○ |
| **계산 콘텐츠 전반**(AIMD 계면·MD SEI·상도·미세구조 연속체) | Outlook 3) 한 문단 요구 | ⭐⭐ |

### ③ 2023에 **있었는데 2026이 빠뜨린** 것 — ⚠ 리비전 코멘트 1순위

| # | 2023에 있던 것 | 2026 상태 | 왜 문제인가 (코멘트 강도) |
|---|---|---|---|
| **③-1** | **§2.1 SE 내부 입계(GB)** — 전 절(2.5쪽), Fig. 2 전체. 게다가 **리뷰 자신이 못박은 공백 선언**: *"there are **few reports on the effect of GBs in sulfide and halide SEs so far**."* | GB가 **덴드라이트 경로(D10/D11)로만** 등장. **이온수송 병목으로서의 GB 절 없음** | ⭐⭐⭐ **가장 강한 코멘트.** "당신 그룹이 2023 Adv. Mater.에서 *황화물·할라이드 GB 연구가 거의 없다*고 지목했다. 3년 뒤 **황화물 전용** 안정성 리뷰라면 그 공백이 채워졌는지 점검하는 것이 자연스럽다." — 우호적이면서 반박 불가 |
| **③-2** | **§5 집전체\|전극 계면** — 특히 **Li₃InCl₆가 Al과 반응해 분해되고 Al을 부식시킨다** + 탄소코팅 해법 | **대응 절 0.** 그런데 2026 §4.2.1은 **"양극측에 고전도 할라이드 SE"** 를 권장 전략으로 제시 | ⭐⭐⭐ **내용상 모순에 가장 가깝다.** 할라이드 catholyte를 권하면서 자기 그룹이 2023에 기록한 **Al 집전체 부식**을 안 쓰면, 실무 독자가 그대로 따라 하다 실패한다. 제목이 *"…to Electrode **Interfaces**"* 인 점에서 범위 누락이기도 함 |
| **③-3** | **Table 1·2·3 = 자체 종합 표 3개**(압력↔성능 15행 / 코팅 19행 / 버퍼층 27행) | **자체 종합 표 사실상 없음**(digest §4 정직 note: "수치가 드문 정성 리뷰", 셀 성능 %가 본문에 거의 없음) | ⭐⭐⭐ **B5의 정답지가 자기 그룹 선행 리뷰에 있다.** "2023 리뷰는 21쪽에 표 3개를 넣었다. 113쪽 원고에 같은 양식의 표 2–3개(σ 비교 / 공기·용매 안정성 비교 / 완화전략↔축)를 넣어 달라." — 재배치만으로 되는 요구 |
| **③-4** | **EIS 등가회로 배정 기준 + 그 한계 자백**(정전용량 범위 3구간, *"largely based on empirical hypotheses"*, 그래서 그룹 간 R_GB가 크게 다르다) | 특성화 방법론 절 없음. §6 미래방향④에서 **"평가 표준화"를 요구**하지만 **구체 recipe는 0** | ⭐⭐ **B4 보강.** "표준화를 요구하려면 2023 리뷰가 EIS에서 했던 것처럼 — 기준값 + 그 기준의 경험적 성격 경고 — 를 한 번은 보여줘야 설득된다." |
| **③-5** | **Monroe–Newman 기준 명시**(G_buffer ≥ 2 G_Li) + 검증 사례(LiPON 31 GPa vs Li 3.4 GPa) | 기계 축은 **E 10–30 GPa · K_IC 0.2–0.4 MPa·m¹ᐟ²** 로 옮겨갔고 Monroe–Newman은 **미등장** | ⭐⭐ ④와 묶어서 코멘트 (아래) |
| **③-6** | **복합 SE(CSE) / 폴리머-매트릭스 전체**(Fig. 3) — Lewis 산–염기, 필러 퍼콜레이션, **σ vs 필러 함량 최적곡선** | 세라믹/폴리머 복합 SE가 §3.5·§5.2.2에 **기계 buffer로만** 잔존 | ⭐ 황화물 전용 리뷰라 범위 축소는 정당. 단 **Fig. 3b의 최적곡선**은 B1(축 상충)의 자기 선례라 아까움 |
| **③-7** | **in-situ 중합 · 외부자극 접합**(전기열 어닐링, **마이크로파 솔더링 28배↓**) · 3D 구조화 | 접촉 개선이 **압력 중심**으로 수렴, 이 세 갈래 없음 | ○ 범위 문제 |
| **③-8** | **저로딩·과두께 셀에 대한 자기비판**(Outlook 1: "그런 셀은 에너지밀도가 경쟁력이 없다") | 면적용량 **>3 mAh/cm²** 목표로 계승 — ✅ 이건 살아남았다 | (누락 아님, 계승 확인) |

### ④ **같은 현상을 다르게 설명하는** 지점

| 현상 | 2023의 설명 | 2026의 설명 | 판정 / 코멘트 |
|---|---|---|---|
| **덴드라이트 성장** | **기계론적·재료물성 중심**: "σ_e가 낮고 **탄성률이 높으면** 덴드라이트가 어렵다" + **Monroe–Newman**(G ≥ 2G_Li) + LiPON 31 GPa 실증. 성장은 계면에서 SE 안으로 **수직 관통** | **파괴역학 중심**: **wedge-opening** — 균열 **후단**에 Li이 주입되며 쐐기로 벌린다(선단응력 모델과 대비). + **SEI 내부**에서 전자침투로 dead-Li 클러스터가 **독립 핵생성**(MD) | ⭐⭐⭐ **가장 뚜렷한 설명 전환.** 원전(Ning, *Nature* 2023)이 2023 리뷰 게재와 거의 동시라 2023이 놓친 건 정당. **문제는 2026이 "그래서 Monroe–Newman 기준은 어떻게 되나"를 말하지 않는 것** — 높은 탄성률 처방이 여전히 유효한지, 파괴인성(K_IC)이 그 자리를 대신하는지 독자가 알 수 없다. → **코멘트**: "wedge-opening 기전과 고전적 전단탄성률 기준(Monroe–Newman)의 관계를 한 문단으로 정리해 달라. 2026은 K_IC를 새 지표로 들여오는데, 두 기준이 대체 관계인지 보완 관계인지가 설계에 직결된다." |
| **공간전하층(SCL)** | **인과적·조작 가능한 변수로 격상**: 산화물 GB의 Li⁺ 결핍 → E_a(GB)↑ (**Fig. 2b,c**), **레버까지 제시**(도핑으로 캐리어 농도↑ → 공간전하 전위↓ → Nb-LLTO GB σ ×2–3). 양극측에서도 "NCM622/LPSCl의 계면반응 **및 공간전하층**"을 실재 문제로 취급 | **격하**: §4.1.3 ③ *"공간전하층이 유일 원인은 아니다 — **조성변화·부산물 축적이 더 직접적**"* | ⭐⭐ **입장이 반대 방향으로 움직였다.** 엄밀히는 위치가 다르다(2023=**GB**, 2026=**양극 계면**)이라 정면충돌은 아니다. 그러나 2026이 GB 절을 통째로 뺀 탓에 **SCL이 유효한 자리(GB)가 원고에서 사라졌고**, 남은 자리(양극)에서만 격하되어 독자는 "SCL은 별거 아니다"로 읽는다. → **코멘트**: "SCL이 지배적인 경우(입계·산화물)와 아닌 경우(황화물/양극 계면)를 구분해 한 문단으로 정리해 달라." · **양쪽 다 SCL을 숫자 없이 다룬다**(두께·전위·Debye 길이 0개) → §11.3 |
| **압력** | **공정 변수**: 냉간가압 100–300 MPa로 밀착, 과압은 Li 크리프 단락. Table 1이 제조압 50–510 MPa·시험압 2–150 MPa를 **데이터로** 깔아둠 | **설계 변수**: stack-pressure **window** + Li 변형기구 지도로 **최적압 예측** | ✅ 정상 진화. 단 ⭐ **2026의 "창"에는 실측 데이터 표가 없고, 그 데이터가 2023 Table 1에 있다** → ③-3 코멘트와 묶으면 강력: "압력 창 개념에 2023 Table 1 양식의 실측 표를 붙이면 창의 위치가 눈에 보인다" |
| **코팅의 요구조건** | 6조건 — **양산성(simple & scalable synthesis)** 포함, **σ_e 조건 없음** | 4조건 — **최소 σ_e** 포함, 양산성 없음 | ⭐ 서로를 보완한다. 2026이 σ_e를 넣은 건 **물리적으로 옳은 개선**(2023의 실질적 결함을 고침), 대신 양산성을 잃었다. → **코멘트(가벼움)**: "두 rubric을 합치면 5–6조건이 된다; 특히 양산성 조건은 §6 미래방향(대면적 공정)과 직결되니 되살릴 만하다" |
| **GB의 이온전도 영향** | **재료군별로 갈린다**: 황화물·할라이드는 **거의 무해**(고변형성+냉간가압), 산화물은 **치명적**(2자릿수) | GB는 **덴드라이트·기계 파괴 경로**로만 등장 | ⭐ 같은 대상에 대한 **관점 전환**(수송 → 파괴). 둘 다 맞지만 2026 독자는 "황화물 GB는 수송에 무해한가?"를 알 수 없다 → ③-1 코멘트에 포함 |
| **in-situ / operando 특성화** | **Outlook 2)** 로 요구 | 여전히 **미래방향 ②** 로 요구 | ⭐⭐ **3년째 같은 요구를 반복.** 그 사이 원고 자신이 operando XCT·operando 압력·cryo-EM 그림을 여러 장 싣는다 → **코멘트**: "2023 리뷰의 outlook 이후 무엇이 달라졌는지 한 문단으로 평가해 달라('what has changed since 2022'). 리뷰의 신뢰도가 크게 오른다." |

### ⑤ 2026 원고 §4·§5 ↔ 2023 절 매핑 (요청 항목)

| 2026 §4 (양극 계면) | 2023 대응 | 상태 |
|---|---|---|
| §4.1.1 화학·전기화학 불안정(S²⁻ 우선 산화 ~2 V) | §3.2 앞부분 + **Fig. 4c** | 프레임 상속, **수치는 2026이 신규** |
| §4.1.2 고전압 O 방출 양방향 결합 | 없음 | **신규** |
| §4.1.3 기전(HOMO·Li 화학퍼텐셜·공간전하) | **Fig. 4c** + §3.2 상호확산 + §3.2의 "공간전하층" 언급 | 상속 + **SCL 평가 역전(④)** |
| §4.1.4 화학-기계 결합 | §3.1 (**Fig. 4a,b** 균열·박리) | 상속, 2026이 응력·operando로 심화 |
| §4.2.1 복합양극 최적화 | §3.1 + **Table 1** | 상속. ⚠ **2026이 표를 안 가져옴** |
| §4.2.2 코팅 | §3.2 + **Table 2** + 6조건 rubric | 상속. ⚠ **표 누락 + rubric 항목 교체** |
| §4.2.3 신규 CAM | Outlook 4) "monolithic" 한 줄 | **씨앗만 상속, 본문은 신규** |

| 2026 §5 (음극 계면) | 2023 대응 | 상태 |
|---|---|---|
| §5.1.1 덴드라이트 핵생성·성장 | §4.2.2 | **설명 전환(④)** |
| §5.1.2 결함×σ_e 시너지 | §4.2.2 "σ_e·탄성률이 두 임계 인자" | 상속 + 정량화 |
| §5.1.3 기계 불일치 | §4.2.2 압력·형태 논의 | 상속 |
| §5.1.4 공극/접촉 진화 | §4.2.2 "stripping이 확산보다 빠르면 접촉면적↓" | **상속(같은 문장의 확장판)** |
| §5.2.1 음극재(흑연/Si/합금/anode-free) | §4.2.2 후반 + **Fig. 5g** + Outlook 4) | 한 문단 → 한 절로 승격 |
| §5.2.2 SE 개질(할로겐/F/LiI) | §4.2.1 in-situ LiF/Li₃N 버퍼 + **Table 3** | 상속. ⚠ **Table 3 누락** |
| §5.2.3 인공 SEI 사다리 | §4.2.1 버퍼층 + **Fig. 5e** 3분류 + **Table 3** | 상속. ⚠ **Fig. 5e의 3-way 기능분류(protective/lithiophilic/stiff)가 2026에 없다** — 2026의 사다리는 재료 계열별이라 기능 축이 흐릿 |

## 11. 우리 DFT/캠페인 대비 → `../our_dft_baseline.md`

> ⚠ **규율**: 이 리뷰에는 우리 4축과 **직접 비교 가능한 계산 수치가 하나도 없다**(§8). 아래 표는
> **수치 대조가 아니라 프레임 대조**다. 문헌 수치(σ·유지율·시간)는 전부 소환값이며 우리 db 절대값과
> 같은 표에 넣지 않는다.

우리 값(참조용): eigenvalue gap comp1 **2.066** / modelc **2.099** / +B₂O₃ **1.967** / LPSOCl **2.231** eV ·
grand-potential 산화 onset **2.256 V**(S²⁻-limited, 두 조성 동일) · 환원 1.242 V / OCV 1.717 V ·
E_VRH 22.06 / **27.66** GPa(relaxed-ion) · BVSE 채널 3.32/4.74/**6.73** % · UMA σ300 b2o3/modelc **동등**(멀티시드).

### 11.1 프레임 대조표

| 리뷰의 칸 | 리뷰 내용 | 우리 결과 | 판정 |
|---|---|---|---|
| **F2 계면 3분류**(안정/MCI/SEI) | 정성 정의만. 판정 기준 = "전자를 통하나" — **측정·계산법 미제시** | `db/properties/b2o3_sei_gaps.json` = 계면 분해산물의 **gap 서열** = "전자를 통하나"의 **정량 판정자**; `interface_reactivity` = 반응 여부 게이트 | **✓✓ 우리가 정량판을 갖고 있다.** 리뷰의 ②/③ 라벨을 우리 산물 목록에 붙일 수 있다 — *wide-gap → ③(passivating), narrow-gap → ②(MCI 위험)* |
| **F3 μ_c ↔ HOMO** (Fig. 4c) | 밴드 정렬 도식, 숫자 0 | **grand-potential ESW**: onset 2.256 V(S²⁻-limited), 단계 2.385(P₂S₇+S)·3.326(SCl) | **✓ 같은 물리, 다른 언어.** 리뷰=단일 준위 만화 / 우리=**상 경계 계단**. 발표에서 나란히 두면 "정성 → 정량" 전환을 한 장으로 보여줄 수 있다. ⚠ HOMO는 분자 용어 — 우리는 VBM으로 쓴다 |
| "Li에 안정한 건 **LiF·LiCl·LiBr·Li₂O·Li₂S·LiH·Li₃N** 뿐" | 목록만 | 우리 SEI json의 wide-gap 산물군과 **정확히 겹친다**(LiCl·Li₂O·LiF…) | **✓ 목록 일치** — 우리 gap 서열이 이 목록에 **순서**를 부여한다 |
| Table 3 27행 중 **LiF 8 · Li₃N 4** | 실험 지속시간(h)으로 줄세움 | 우리는 **gap**으로 줄세움 | **○ 교차검증 후보** — h ↔ gap 상관을 보면 우리 지표의 실험적 정당성이 생긴다 (⚠ 조건이 제각각이라 정량 회귀는 금지, 순위 일치 여부만) |
| **Li₅.₅PS₄.₅Cl₁.₅ 가 LGPS의 음극 버퍼**(1800 h) | 실험 소환 | **modelc = Li₅.₄PS₄.₄Cl₁.₆** — 사실상 같은 조성 | **✓✓ 우리 조성의 새로운 용도 좌표.** 우리는 modelc를 "Cl-rich 고속 SE"로만 봤는데 문헌은 **음극 보호막**으로도 쓴다 → 우리 환원 한계 1.242 V·SEI gap 데이터가 이 용도를 직접 설명할 수 있다 |
| §4.2.2 "**σ_e 낮고 탄성률 높으면** 덴드라이트가 어렵다" + Monroe–Newman(G≥2G_Li) | 정성 + LiPON 31 vs Li 3.4 GPa | 우리 E_VRH **22.06 / 27.66 GPa**(relaxed-ion, PBE) — Li(≈3.4 GPa G)의 여러 배 | **✓ 방향 정합 (⚠ 값 이식 금지)**: 우리 것은 **E**(Young), 리뷰 기준은 **G**(shear)이고 relaxed/clamped·functional 구분이 리뷰엔 없다. "우리 modelc가 Monroe 기준을 만족한다"는 **말하면 안 된다** — G를 따로 뽑고 다결정/GB를 고려해야 성립 |
| §2.1 "황화물·할라이드는 **GB가 이온수송을 크게 막지 않는다**"(100–300 MPa 냉간가압) | 정성 + 산화물과 대비 | 우리 BVSE·UMA-MD는 **전부 단결정 주기셀** — GB 없음 | **✗ 우리 밖.** 리뷰의 이 문장은 우리 단결정 결과를 다결정 실측과 잇는 **정당화 근거**로 쓸 수 있다("황화물은 GB 기여가 작아 단결정 계산이 총전도도의 좋은 대리다") — 단 [Kim24 MTP argyrodite GB] digest와 교차확인 필요 |
| §2.1 GB 두께 **1–2 unit cells** · 공간전하 도식(Fig. 2b,c) | 정성, **숫자 없음**(두께·전위·Debye 길이 전무) | 우리도 **없음** | **✗ 양쪽 공백** → §11.3 |
| 압력↔성능 (Table 1, 50–510 MPa) | 실험 소환값 | 우리 기계축은 0-pressure DFT 탄성 | **✗ 축이 다름** — DEM 트랙(`comparison_vs_ours_DEM.md`)이 받을 내용 |
| band gap · ESW 절대값 | **리뷰에 없음** | comp1 2.066 / modelc 2.099 / B₂O₃ 1.967 / LPSOCl 2.231 eV (PBE) | — 비교 대상 자체가 없음. PBE 과소·무질서 민감 규율 유지 |

### 11.2 계면 분류 ↔ 우리 축의 대응 (요청 항목)

| 리뷰 분류 | 우리 계산축 | 대응 방식 | 갭 |
|---|---|---|---|
| ① **열역학 안정 계면** | **hull 반응성 게이트** (`interface_reactivity`, T9 47종 전수) | 반응에너지 ≈ 0 → ①. 우리 T9에서 **LPSCl vs Li 는 −541.5**(= 격렬한 반응) → LPSCl‖Li 는 ①이 **아니다**. 리뷰도 "①은 extremely rare"라 일치 | 없음 — 잘 맞는다 |
| ② **MCI** vs ③ **SEI(passivating)** | **SEI 산물 gap 서열**(`b2o3_sei_gaps.json`) | 산물의 gap이 크면 ③, 작으면 ② — 리뷰의 정성 이분법에 **연속 좌표**를 준다 | ⚠ 우리 gap은 **PBE 과소평가 + 무질서 민감**. **절대 임계값(예 "3 eV 이상이면 SEI")을 정하면 안 된다** — 같은 방법 내 **순위**로만 쓴다 |
| 산화측(양극) 안정성 | **grand-potential ESW**(축 ①: intrinsic 0-pressure) | 리뷰 F3(μ_c↔HOMO)의 정량판 | ⚠ 리뷰는 **kinetic/열역학 구분을 안 한다**(2026 §3.4는 구분함). 우리 축 명명 규율 유지 — "Cl-rich 산화안정"은 축을 반드시 명시 |
| **공간전하층** | **없음** | — | → §11.3 |
| 기계(덴드라이트 억제) | **elastic C_ij** | 방향만 정합 | ⚠ G vs E, relaxed vs clamped, 다결정/GB 미포함 |

### 11.3 ★ 공간전하층(SCL) — 정량인가 정성인가 (요청 항목)

**답: 완전히 정성이다. 양쪽 리뷰 모두.**

- 2023의 SCL 언급은 **총 5회**뿐이고, 첨부된 숫자는 **하나도 SCL 자체의 양이 아니다**:
  ① Fig. 2b,c 도식(농도 급감 + E_a 봉우리 — **축 눈금 없음**) ② "도핑으로 캐리어 농도↑ →
  공간전하 전위↓" → 결과값은 **GB σ ×2–3**(SCL 두께도, 전위 V도 아님) ③ CSE의 Stern/확산층
  (Fig. 3a) ④ NCM622/LPSCl의 "계면반응 및 공간전하층" 나열 ⑤ 버퍼층이 "공간전하 효과를 억제".
  → **SCL 두께(nm)·공간전하 전위(V)·Debye 길이·유전상수 어느 것도 본문에 없다.**
- 2026은 한 발 더 물러나 *"SCL이 유일 원인은 아니다"* 로 격하 — 역시 숫자 없음.
- **함의**: SCL은 두 리뷰 모두에서 **설명 어휘일 뿐 측정·계산량이 아니다.** 우리가 "공간전하층을
  계산했다"고 말하려면 최소한 계면 슬랩의 **정전위 프로파일 + Li 농도 프로파일**이 필요하고,
  그건 우리가 **아직 안 한** 것이다. 지금 단계에서 SCL을 우리 서사에 넣으면 안 된다.

### 11.4 ★ T3(Li‖LPSCl 반응 MD) 와의 접점 — 새 시뮬레이션 없이 지금 채울 수 있는 칸

`kb/open_items.md` **T3**는 완전 공백이고 비용이 크다(≥20 ns). 그런데 **이 리뷰는 T3가 겨눌
관측량에 "이름"을 붙여 준다** — 우리가 이미 가진 산출물의 재해석만으로 메울 수 있는 칸이 셋이다.

| 칸 | 지금 있는 것 | 후처리로 할 일 (새 계산 0) | 얻는 것 |
|---|---|---|---|
| **(a) SEI 산물의 MCI/passivating 라벨링** | `b2o3_sei_gaps.json` · `anode_interface_b2o3.json` · T9 47종 반응성 | 각 산물 행에 **`interface_type` 열**(②MCI / ③passivating / ①inert) 추가 — 판정은 **gap 서열 + hull 반응성**의 조합. 절대 임계 대신 *"이 방법 내 서열 상위 N개 = passivating 후보"* | 리뷰(2023 §4.2.1 · 2026 §3.4)의 **표준 어휘로 우리 데이터를 말할 수 있게** 된다. 발표·논문에서 즉시 인용 가능 |
| **(b) Table 3 대조표** | 위와 같음 | 리뷰 Table 3의 **버퍼층 재료 27행 중 이성분 Li 염(LiF·Li₃N·Li₂O·LiCl…)** 을 뽑아 우리 gap 서열과 **순위 대조표** 1장 | *"실험이 오래 버틴 버퍼일수록 우리 gap 서열 상위"* 가 성립하면 **우리 지표의 외부 검증**이 된다. ⚠ 조건이 제각각이라 **정량 회귀 금지, 순위 일치 여부만** |
| **(c) T3 관측량 재정의** | T3 프로토콜(잔존 PS₄ 층수 vs 시간) | T3의 성공 판정에 **F2 라벨을 명시적으로 붙인다**: "20 ns에서 계면상 성장이 **멈추면 ③, 계속 자라면 ②**" — 리뷰가 정의한 그대로 | T3가 "MD를 돌렸다"가 아니라 **"문헌 표준 분류의 어느 칸인지 판정했다"** 가 되어 결과의 의미가 명확해진다. 프로토콜 문서만 고치면 되므로 비용 0 |

> ⚠ **당장 못 채우는 칸**: 공간전하층(§11.3) · GB(우리 셀에 GB 없음) · 압력↔성능(축이 DEM 트랙) ·
> Monroe–Newman G 기준(우리는 E만 보유).

## 12. 적용 인사이트

- ① **리비전 코멘트 3개가 이 논문 하나로 근거를 얻는다** — B5(→③-3, 표 3개), B4(→③-4, EIS
  기준+한계 자백), B1(→Fig. 3b 최적곡선 = 그룹 자신의 trade-off 선례). **"같은 그룹의 선행
  리뷰는 이렇게 했다"** 는 형태라 저자가 방어하기 어렵고 기분 상할 여지도 적다.
- ② **B2(HOMO vs VBM)의 성격을 바꿔야 한다.** 2026의 HOMO 용법은 실수가 아니라 **2023
  Fig. 4c에서 확립된 그룹 관례**다. → 지적을 "틀렸다"가 아니라 **"고체를 다루는 절에서는 VBM/CBM
  으로 쓰고, 분자 유래 틀을 쓸 때는 그 사실을 한 번 명시해 달라"** 로 (B3와 같은 화법).
- ③ **우리 SEI-gap 지표의 "말하기 방식"을 바꾼다.** 지금까지는 "gap이 크면 전자를 막는다"였는데,
  이 리뷰의 **F2 3분류(안정/MCI/SEI)** 라는 표준 어휘에 얹으면 *"우리는 MCI/passivating 판정을
  정량화한다"* 가 된다 — 리뷰 두 편이 모두 쓰는 어휘라 수용성이 높다.
- ④ **modelc(Li₅.₄PS₄.₄Cl₁.₆)의 두 번째 얼굴**: Table 3에 **Li₅.₅PS₄.₅Cl₁.₅가 LGPS의 음극 버퍼로
  1800 h** 버틴 행이 있다. 우리 Cl-rich 서사를 "빠른 SE"에서 **"빠르면서 음극에서도 자기제한적"**
  으로 확장할 실마리 — 우리 환원 한계(1.242 V)·SEI gap 데이터가 그 주장의 근거가 된다.
- ⑤ **단결정 계산의 정당화 문장**을 얻었다: 리뷰 §2.1의 *"황화물·할라이드는 GB가 Li 이동을 크게
  막지 않는다(냉간가압 100–300 MPa로 밀착)"* — 우리 BVSE·MLIP-MD가 전부 단결정 주기셀인 것에
  대한 **문헌 방어선**. (단 [Kim24 MTP GB] digest와 교차확인 후 사용)

## 13. 인용 가능 문장 (deck/paper용)

- "Miao et al. (Adv. Mater. 2023, 35, 2206402) classify Li|SE interfaces into three types —
  thermodynamically stable, mixed electronic–ionic conducting interphase (MCI), and
  electronically insulating SEI — and note that the first is *'extremely rare'*; our computed band
  gaps of the interfacial decomposition products turn this qualitative trichotomy into a ranking."
- "The same review states that in sulfide and halide electrolytes the grain boundaries *'do not
  create much hindrance to Li-ion migration'* thanks to cold pressing at 100–300 MPa — which is
  why single-crystal periodic-cell transport calculations remain a reasonable proxy for the total
  conductivity of these materials."
- "Miao et al. frame cathode-side oxidation through the alignment of the cathode chemical
  potential μ_c with the sulfide HOMO (their Fig. 4c); our grand-potential construction replaces
  that single-level cartoon with an explicit staircase of decomposition equilibria (onset 2.256 V,
  S²⁻-limited)."
- (리비전용) "The authors' own earlier review (Miao, Li, Nan, *Adv. Mater.* 2023, 35, 2206402)
  compiled three comparison tables — pressure vs cycling performance, cathode coatings, and
  Li/SE buffer layers — within 21 pages; comparable tables would substantially raise the utility
  of the present 113-page manuscript."

## 14. 주의/한계 (비판적으로)

- **자체 데이터 0 + 계산 0.** DFT·first-principles·band gap·VBM이 본문에 **한 번도** 안 나온다.
  "이 리뷰가 이렇게 계산했다"는 서술은 **불가능**하다. 물성 4축 수치 비교에서 제외.
- **HOMO/LUMO를 고체 SE에 적용** (Fig. 4c, 본문 10회). 고체는 **VBM/CBM**이며 밴드폭·상태밀도가
  있다. 단일 준위 도식은 (i) 무질서로 밴드엣지가 흔들리는 효과 (ii) 부분 산화가 특정 **자리**
  (free S vs PS₄ S)에서 먼저 일어나는 효과를 **원리적으로 표현할 수 없다** — 정확히 우리 site-PDOS
  결과가 채우는 자리.
- **열역학 vs 속도론을 안 가른다.** "μ_c가 HOMO 아래면 산화된다"는 열역학이지만, 실제 셀이
  그 너머에서 도는 이유(kinetic passivation)는 언급되지 않는다. (2026 §3.4는 이걸 제대로 가른다 —
  **후속작이 개선한 지점**)
- **임계 수치에 조건이 없다** — GB 두께 "1–2 unit cells", 냉간가압 "100–300 MPa", LiPON
  "G ≈31 GPa"가 어떤 측정·시편·응력상태에서 나온 값인지 없음. (단 EIS 정전용량 범위만은
  펠릿 치수와 **경험적 성격 경고**를 함께 달았다 — 리뷰 내 유일한 모범)
- **Fig. 5g는 눈금 없는 정성 산포도**다. "Li–In이 Li–Al보다 전위가 높다" 같은 **순서**만 읽어야 하고,
  전위·용량 값을 이 그림에서 읽어 인용하면 안 된다.
- **Table 1의 "Low / High"** 행(ref [40])은 유지율이 숫자가 아니라 형용사다 — 압력 효과의
  방향성 근거로만 쓰고 정량 인용 금지.
- **오래된 소재**: Received 2022-07, Revised 2022-08. 즉 **2022년 중반까지의 문헌**이다.
  wedge-opening(Ning 2023), 고엔트로피 argyrodite, anode-free 정량, 할라이드 CAM은 다 그 뒤다.
  **2023년 논문이라고 2023년 지식으로 읽으면 안 된다.**
- **자기 그룹 편중 여부**: 2023은 오히려 균형적(266 refs, 자기인용 두드러지지 않음). 2026 원고가
  자기 그룹 그림([Liu23]/[Li25])을 Figure로 쓰는 것과 대비된다.
- **우리 그룹(한양대) 문헌 미인용** — 이 계보(Tsinghua–USTB) 특성.

## 15. 후속 추적 참고문헌 (우선순위순)

| 우선 | ref# | 내용 | 왜 |
|---|---|---|---|
| ★★★ | [45,46] | **황화물·할라이드 GB 효과** — 리뷰가 "few reports"라며 붙인 단 2개 | ③-1 코멘트의 실탄. 이 2편이 무엇인지 확인하면 "3년간 몇 편 늘었나"를 말할 수 있다 |
| ★★★ | [232] | **Li₃InCl₆ ↔ Al 집전체 반응·부식** + 탄소코팅 해법 | ③-2 코멘트의 근거. 2026이 할라이드 catholyte를 권하는 것과 정면으로 닿는다 |
| ★★ | [48] | Cs-corrected STEM: LLTO GB의 **Ti–O 층 재구성** | GB 원자구조의 유일한 직접 증거 — 우리 GB 논의의 실측 앵커 |
| ★★ | [210] | **Monroe & Newman** — G_buffer ≥ 2 G_Li | ④ 코멘트(wedge-opening과의 관계)의 원전. `kim2021_review…`(Rupp)에도 등장 |
| ★★ | [82] | LiNbO₃-NCM811 + Li₆PS₅Cl **20 000 cycles / 71 %** (CSE, PVDF-co-TrFE) | Table 1·2에 동시 등장하는 최장수명 셀 — 우리 코팅/CSE 논의의 상한 기준 |
| ★★ | [178] | LGPS ‖ Li 사이 **Li₅.₅PS₄.₅Cl₁.₅ 버퍼 1800 h** | modelc 사촌 조성의 **음극 보호막 용도** 원전 (§12④) |
| ★ | [183] | Li₃YCl₆ ‖ Li 를 **Li₆PS₅Cl** 층으로 보호(1000 h) | "LPSCl 계면상은 전자전도가 나빠 자기제한" 주장의 원전 |
| ★ | [54] | **B 도핑으로 LiTi₂(PO₄)₃ GB 유리화** → σ 1.12×10⁻⁴ → 1.03×10⁻³ S/cm | **B의 계면 역할** 선례 — 우리 B₂O₃ 서사의 (다른 계지만) 사촌 |
| ★ | [58] | Al-LLZO ‖ Li 계면상이 **<5 unit cell 전자절연 SEI** | "자기제한 SEI"의 정량 사례 (두께 명시) |
| ★ | [189] | ALD Al₂O₃ 5–6 nm → 계면저항 **1710 → 1 Ω cm²** | 계면 개질 효과 크기의 감각 |

## 16. 기법 용어 미니사전

- **MCI (mixed electronically and ionically conducting interphase)**: 이온·전자를 **둘 다** 통과시키는
  계면 분해상. 전자가 통하니 SE 환원이 계속 진행되어 **SE나 음극이 소진될 때까지 성장**한다 →
  리뷰 판정 *"completely unacceptable"*. 반대말이 **passivating SEI**(이온만).
- **SEI (solid electrolyte interphase)**: 여기서는 액체계 SEI의 **기능적 유비** — 이온전도·전자절연
  이라 자기제한. σ_ion만 충분하면 실전 성능이 나온다.
- **μ_c (cathode chemical potential)**: 양극 내 전자의 화학퍼텐셜(≈ Fermi 준위). 충전으로 내려간다.
  **μ_c < HOMO(SE)** 가 되면 SE에서 양극으로 전자가 넘어가 = **SE 산화**.
- **CEI (cathode electrolyte interphase)**: 양극측 계면상. 그 **HOMO가 μ_c보다 낮아야** 자기제한.
- **공간전하층 (space-charge layer)**: 두 상의 Li 화학퍼텐셜 차 때문에 계면(또는 GB) 근처에
  생기는 Li 결핍/과잉 층. 2023은 GB 저항의 기전으로 **적극 활용**, 2026은 양극 계면에서 **격하**.
  ⚠ **두 리뷰 모두 두께·전위 숫자가 없다** — 설명 어휘이지 측정량이 아니다(§11.3).
- **GB 반원 (Nyquist)**: 임피던스 반원 중 결정립계 성분. **황화물·LGPS는 잘 안 보여서** 등가회로로
  분해해야 하고, 그 배정은 **정전용량 범위**(bulk 10⁻¹¹ / GB 10⁻¹⁰–10⁻⁷ / 계면 10⁻⁷–10⁻⁵ F)라는
  **경험 규칙**에 기댄다 → 그룹 간 R_GB 편차가 크다.
- **Monroe–Newman 기준**: 덴드라이트 억제를 위해 계면층의 **전단탄성률 G ≥ 2 × G(Li)** 여야 한다는
  선형안정성 이론. 2023이 명시 인용(LiPON 31 GPa vs Li 3.4 GPa), **2026은 미언급**.
- **lithiophilic / lithiophobic**: Li 금속에 대한 젖음성. lithiophilic 층은 접촉면적을 확보해
  국소 전류 집중을 막는다. Fig. 5e의 버퍼 3분류 중 하나.
- **CSE (composite solid electrolyte)**: 폴리머 매트릭스 + 무기 필러(또는 그 반대). **필러 함량에
  최적점**이 있고(Fig. 3b), 개선 기전은 **Lewis 산–염기 상호작용**을 통한 자유 Li⁺ 농도·사슬 운동성 증가.
- **AMP / CAMP**: active material particle / cathode active material particle — 리뷰의 복합전극 표기.
- **monolithic configuration**: 황화물이 **활물질과 전해질을 겸하는** 셀 구성(2023 Outlook 4). 2026의
  *"cathode homogenization"*(단일상에 이온+전자 수송 내장)의 조상 개념.
- **anode-free**: 음극 활물질 없이 집전체 위에 in-situ Li 증착. 2023은 Outlook, 2026은 본문 절.

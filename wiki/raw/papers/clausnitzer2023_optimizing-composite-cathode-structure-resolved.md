---
title: "Clausnitzer, Mücke, Al-Jaljouli et al. 2023 — Optimizing the Composite Cathode Microstructure in All-Solid-State Batteries by Structure-Resolved Simulations (Batteries & Supercaps 6, e202300167)"
source_url: local-upload/02._Optimizing_the_Composite_Cathode_Microstructure_in_AllSolid-State_Batteries_by_Structure-Resolved_Simulations.pdf
source_url_si: local-upload/02._Sup_Optimizing_the_Composite_Cathode_Microstructure_in_AllSolid-State_Batteries_by_Structure-Resolved_Simulations.pdf
pdf_sha256_main: 8f11a26048872dca981f310e72ef6f0c7bbb1cd4617c033192d6406c3e6ea335
pdf_sha256_si: 315eb29a63bf75e6163c07fafe22a739fa21afc0f64c5b70ff41fcd05508ac73
ingested: 2026-09-16
sha256: 166278ef6c73110613c1de8a289765afaef814045da7a4ed38b61c531a8c58f6
---

# 수집 목적

Moritz Clausnitzer (교신, DLR/HIU), Robert Mücke, Fadi Al-Jaljouli, Simon Hein,
Martin Finsterbusch, Timo Danner, Dina Fattakhova-Rohlfing, Olivier Guillon,
Arnulf Latz, **"Optimizing the Composite Cathode Microstructure in All-Solid-State
Batteries by Structure-Resolved Simulations"**, *Batteries & Supercaps* **6** (2023)
e202300167 의 **절별 해체분석** — 본문 16 쪽 + Supporting Information 10 쪽.

**이 위키 `assb` 섹션의 2호 논문이다.** 액체셀 계열(현재 `raw/papers/` 20 편)과
**섞지 않는다** — 음극 축이 다르다.

흡수 이유는 하나다. 1호([[composite-cathode-percolation-utilization]], Bielefeld 2019)가
복합양극의 **기하**만 풀고 **전압축을 한 번도 쓰지 않은** 채 끝났고, 닻
([[assb-contact-loss-vs-lampe]])의 가장 큰 공백이 거기였다. 이 논문은 그 다음 칸이다:

> **★ 전압축이 들어왔다.** 개회로 전위(`U₀ = 4.2 V`), 하한 컷오프(`U_cut = 3.4 V`),
> 방전 곡선(SI Fig. S5, `V` vs `mAh/cm²`), 셀 단위 에너지밀도(`Wh/kg_cell`,
> 식 (9) `∫ i·U dt / (m_An+m_Sep+m_Ca)`) 가 전부 있다. `assb` 섹션에서 **처음**이다.

동시에, 이 논문이 **주지 않는 것**도 분명하다 — 그리고 그것이 이 digest 의 절반이다
(§13 어긋남 원장 14 건, §14 Q1~Q8 표). 없다는 사실도 이 계보의 관측이다.

**표기 규칙** (이 위키 관례 3구분 + 1):
- `[인쇄]` — 논문 본문/식/표/그림 안에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**; `figure-read ≈`)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

> ⛔ **인용 금지.** 이 파일의 숫자는 **사본**이다. 인용 근거는 원문 PDF 이고,
> 우리 연구 수치의 정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md` 다.
> 여기 적힌 수치를 논문·보고서에 옮기려면 원문을 다시 확인한다.
>
> ⚠ **모집단 경고.** 이 논문의 결론은 **LCO(또는 NMC811) / LLZO 2 성분 소결
> 복합양극**, **Li 금속 음극(이상 접촉 가정)**, **도전재·바인더 없음**, **공극은
> 채워지지 않는 빈 공간**, 전극 두께 **50 µm 고정**, 방전 **1 mA/cm² 정전류 1 회**,
> 구조 **1 점당 1 개**(반복 없음) — 이 한 조합에서 나온 것이다. **셀 실험이 0 개**이고
> **사이클링이 0 회**다. 그 밖으로 옮기면 모집단이 다르다.
>
> ⚠ **`[도표]` 경고.** 이 논문은 수치표를 거의 주지 않는다 (숫자표는 Table 1·2·S1·S2·S4
> 의 **입력 파라미터**뿐이고 **결과 수치표는 0 개**). 아래 결과 수치는 대부분
> **그림에서 눈으로 읽은 값**이며 ±5~10 % 오차를 가진다. 모두 `[도표]` 로 표시했다.

- 원본 파일 (로컬 업로드, 저장소에 바이너리를 넣지 않는다):
  - 본문 `02._Optimizing_the_Composite_Cathode_Microstructure_in_AllSolid-State_Batteries_by_Structure-Resolved_Simulations.pdf`
    (16 쪽, PDF sha256 `8f11a26048872dca981f310e72ef6f0c7bbb1cd4617c033192d6406c3e6ea335`).
    PDF 메타데이터 `subject` = `Batteries & Supercaps 2023.6:e202300167`,
    `creationDate` 2023-11-03.
  - SI `02._Sup_...pdf` (10 쪽, PDF sha256
    `315eb29a63bf75e6163c07fafe22a739fa21afc0f64c5b70ff41fcd05508ac73`),
    `creator` = pdftk 2.02, `creationDate` 2023-11-08.
- 크로핑 그림: `raw/figures/clausnitzer2023_optimizing-composite-cathode-structure-resolved/`
  — **24 장** (본문 fig 11 + SI fig 7 + 표 6). **직접 Read 로 본 것은 15 장**:
  Fig. 1·2·3·4·5·6·7·8·9·10·11 (본문 전부) + Fig. S1·S3·S4·S5·S7.
  **안 본 것 3 장**: Fig. S2(시뮬레이션 도메인 모식도 — 캡션으로 충분),
  Fig. S6(면적당 용량 — 본문이 "Fig. 4 와 같은 상관" 이라고 명시),
  그리고 표 6 장(`tab_*.png`)은 **이미지로 읽지 않고 PDF 텍스트로** 읽었다.
- 본문·SI 텍스트는 `pymupdf.get_text()` 로 추출. 이 저널 조판은 **단어를 줄바꿈으로
  쪼개는 경우가 많아**(예: "Small / SE / particles / contribute") 단어 세기는 줄 단위가
  아니라 문자열 검색으로 했다.
- 페이지 참조는 PDF 페이지 1–16 = 논문 (1 of 16)–(16 of 16). SI 는 `SI p1–p10`.

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

| # | 공백 | 왜 문제인가 |
|---|---|---|
| **G1** | ★ **`Norm. capacity` 가 연결성(`Connectivity`)을 포함하는지 안 하는지 원문에 없다.** `[인쇄, p5]` "Before starting the electrochemical simulations, **isolated clusters were removed from the input structure** to improve numerical stability." 그런데 식 (7) `C_grav = C_3.4V/(V_CAM·ρ_CAM)` 의 `V_CAM` 이 **제거 전**인지 **제거 후**인지 적혀 있지 않다. | **우리 물음의 정확히 그 자리다.** 제거 후 부피로 나눴다면 `C_norm` 에는 기하적 접촉 손실(`θ`)이 **안 들어 있고**, 제거 전이면 들어 있다. 두 경우 `Q_apparent = θ·η·Q_material` 의 분해가 달라진다 (§15·§16). 그림만으로는 판별 불가 — 두 해석 모두 Fig. 8a 를 설명한다. |
| **G2** | **오차 막대가 단 한 그림에도 없다.** `standard deviation` 0 회, `error bar` 0 회, `seed` 0 회. `random` 은 **1 회**만 나오고 그것은 구조 실현이 아니라 `[인쇄, p3]` "The identified particles are **randomly assigned to 8 different material IDs**" — GB ID 배정이다. | **파라미터 점당 구조 1 개.** 1호 Bielefeld 2019 이 같은 종류의 모델에서 **거시 파라미터 고정에도 무작위 충전만으로 `θ_AM` 이 ≈30 % ↔ ≈70 % 이봉**이라고 인쇄했는데, 이 논문은 그 폭을 **한 번도 재지 않는다**. Fig. 10·11b 의 "상위 3 개" 차이가 0.94 vs 0.93 vs 0.89 인데, 이 차이가 실현 잡음보다 큰지 알 수 없다. |
| **G3** | **`i_00^CAM = 0.0116 A cm^2.5 mol^-1.5` 를 식 (2) 로 재현할 수 없다.** `[인쇄, p4]` `R_CT = 2600 Ω cm²` (ref 54 Kato 2014) + 식 (2) `i₀ = RT/(zFA·R_CT)`. | `[재현]` `A = 1 cm²` 로 두면 `i₀ = 8.314×298.15/(96485×2600) = 9.88×10⁻⁶ A/cm²`. 그런데 Table S3 의 `i₀ = i_00 c_e^α c_s^α (c_max−c_s)^(1−α)` 에 `c_e = 0.0384`, `c_s = c_0 = 0.027058`, `c_max−c_s = 0.024497` 을 넣으면 `0.0116 × 0.19596 × 0.16449 × 0.15651 = 5.85×10⁻⁵ A/cm²` — **약 5.9 배 크다.** `A` 의 정의(어느 면적인가)와 선형화 기준 농도가 인쇄돼 있지 않아 어느 쪽이 맞는지 못 정한다. |
| **G4** | **NMC811 의 밀도 `ρ_NMC` 가 어디에도 없다.** Table S4 는 `ρ_SE = 5.3`, `ρ_CAM(LCO) = 5.051 g/cm³` 만 준다. | 식 (7)(8)(10) 이 전부 `ρ_CAM` 을 쓴다 → **NMC 의 gravimetric capacity·energy density 를 재현할 수 없다.** `[재현]` 본문 수치(norm. 0.65 ↔ 133 mAh/g)에서 역산하면 `C_theo,grav(NMC) = 204.6 mAh/g` → `ρ_NMC ≈ 4.94 g/cm³`. 인쇄된 적은 없다. |
| **G5** | **전극 두께가 50 µm 하나로 고정**돼 있다 (`250×250×500 voxel`, 100 nm voxel → 크롭 후 25×25×50 µm³). | 그런데 결론이 `[인쇄, p9]` "Simulations allow to derive an optimal electrode composition **and thickness**" 라고 두께를 결과 목록에 넣는다. **두께는 스윕되지 않았다** (§13 불일치 4). |
| **G6** | **전기화학 시뮬레이션은 복셀을 2 배로 키운 격자에서 돈다.** `[인쇄, p3]` "we **increase the voxel size of the cathode microstructures by a factor of 2**". 즉 기하 지표(연결성·굴곡도·활성면적)는 100 nm 격자, 전기화학은 **200 nm 격자**. | 두 결과가 **다른 해상도의 구조**에서 나온 것이다. 격자 수렴 시험이 없다. `d_SE = 0.70 µm` 구조는 200 nm 격자에서 **지름 3.5 복셀**이다 — 그 구조가 Fig. 10 에서 최적으로 뽑힌다. |
| **G7** | **한계 분율 "약 20 vol%" 가 시뮬레이션되지 않은 점에서 나온다.** `[인쇄, p6]` "Our calculations indicate that the limiting material fraction is around 20 vol.% **for both the SE and CAM**." 시뮬레이션된 `SVF_LCO` 는 {33.3, 40, 50, 60, 69.4, 80} 뿐 (+순물질 100). | → SE 쪽 20 vol% 는 `SVF_LCO = 80 %` **한 점**에서 나오고 (Fig. 3a 에는 그 점이 `σ_eff = 0` 이라 **찍히지도 않는다**), **CAM 쪽 20 vol% 는 시뮬레이션된 점이 아예 없다** (최저가 33.3 %). Fig. 3 의 빨간 점선(안내선)의 함수 형태도 캡션·본문 어디에도 없다. |
| **G8** | **GB 저항 `R_GB` 가 본문 안에서 두 값으로 나온다.** `[인쇄, p4]` "The reported GB exchange current density of `i₀^GB = 6.91·10⁻³ A/cm²` results in a corresponding resistance per GB of approximately `R_GB = 3.7 Ω cm²`." `[인쇄, p7]` "`R_GB,3 = 3.6 Ω cm²`" (from `7·10⁻³ A/cm²`). | `[재현]` `RT/(F·6.91e-3) = 3.718`, `RT/(F·7e-3) = 3.670`. 즉 Methods 는 **문헌값 그대로**, Results 는 **반올림한 7e-3** 을 쓴다. 1.3 % 차이라 결론에 영향은 없지만, `R_GB,3` 을 "Ref. [38] 이 보고한 값" 이라고 부르는 문장과 어긋난다. |
| **G9** | **식 (1) 과 Table S3 의 GB Butler–Volmer 지수에 `F` 가 없다.** `[인쇄, 식 1]` `i_GB = i₀^GB [exp(Δφ̃/2RT) − exp(−Δφ̃/2RT)]`, Table S3 는 `∆ϕ_GB/2RT`. | `ϕ`(전위, V)로 읽으면 `ϕ/RT` 는 무차원이 아니다. G8 의 재현이 `R = RT/(F i₀)` 로 맞는 것을 보면 **실제 코드에는 `F` 가 있고 인쇄에서 빠진 것**이다. 본문이 `Δφ̃` 를 "electrochemical potential"(J/mol)이라 부르므로 본문은 구제되지만 **SI 의 `∆ϕ` 표기는 구제되지 않는다.** |
| **G10** | **실험 대조가 다른 재료계다.** Fig. 3 의 experiment 는 Minnmann et al.(ref 22) 의 **NMC622/Li₆PS₅Cl**(황화물) 이고, 논문의 모델은 **LCO/LLZO**(산화물, 소결)다. | 논문 스스로 `[인쇄, p7]` "Systematic conductivity measurements on **LLZO based composite electrodes are lacking** in the literature and additional data is needed for quantitative validation of model predictions." → **이 논문의 재료계에 대한 검증은 0 이다.** `validat*` 2 회 모두 "앞으로 해야 한다" 는 문장 안에 있다. |
| **G11** | **`i₀^NMC = i₀^LCO` 로 두었다.** `[인쇄, p13]` "Note that `i₀^NMC` is also the same as in the previous simulations with LCO. Generally, NMC exhibits **low interfacial stability with LLZO, making it challenging to measure the charge transfer resistance** of pristine interfaces experimentally." | LCO/NMC 비교의 결론("NMC 가 gravimetric 으로 더 낫다")이 **NMC/LLZO 계면이 LCO/LLZO 만큼 좋다는 가정** 위에 서 있다. 그 가정이 틀릴 것이라고 같은 문단이 말한다. |
| **G12** | **방전 1 회, 정전류 1 개(1 mA/cm²) 뿐이다.** 율 스윕 없음. `[인쇄, p5]` 근거는 "This value falls within the range of reported **critical current densities** for garnet-type electrolytes in contact with Li-metal anodes"(ref 60) 이고, `[인쇄]` "At lower current densities, local currents and overpotentials are generally lower, resulting in **reduced sensitivity to microstructural variations**." | `[재현]` 이 셀의 면적당 용량이 ≈1.36 mAh/cm² (§8.6) 이므로 1 mA/cm² 는 **≈0.74 C** 다 — 준평형(pOCV)이 아니라 **중간 율**이다. 논문이 최적 조성이라 부르는 것은 **0.74 C 에서의 최적**이고, 저율 최적은 다를 수 있다고 논문 자신이 위 문장에서 인정한다. ★ 이것이 §16 의 핵심 지렛대다. |
| **G13** | **사이클링·역학이 없다.** `[인쇄, p9]` "it should be noted that pore formation and **contact loss** between individual particles **can also result from mechanical degradation due to volume changes of the CAM during operation**. While our current model **does not incorporate mechanics** … specific changes in the microstructure, such as **pore formation during cycling, are beyond the scope** of our current model." | 1호와 **똑같은 자리에서 멈춘다.** `θ`(=Connectivity)의 **시간 변화는 여전히 아무도 안 줬다.** 이 논문의 `sinter density` 스윕은 "제조가 남긴 정적 공극" 이지 "사이클이 만든 공극" 이 아니다 (§15-3). |
| **G14** | **데이터·코드 공개 없음.** `[인쇄, p15]` "The data … are available from the corresponding author **upon reasonable request**." GeoDict(Math2Market) + BEST(Fraunhofer ITWM/DLR) 모두 상용/내부 코드. | 재현하려면 두 상용 패키지가 필요하다. 미시구조 파일·분할 결과·시뮬레이션 설정이 제공되지 않는다. |

---

## 0. 서지사항 (직접 확인)

`[인쇄]` 1 쪽 헤더/각주 및 15–16 쪽:

| 항목 | 값 |
|---|---|
| 제목 | Optimizing the Composite Cathode Microstructure in All-Solid-State Batteries by Structure-Resolved Simulations |
| 저자 | Moritz Clausnitzer *^[a,b] · Robert Mücke^[c] · Fadi Al-Jaljouli^[c,d] · Simon Hein^[a,b] · Martin Finsterbusch^[c] · Timo Danner^[a,b] · Dina Fattakhova-Rohlfing^[c] · Olivier Guillon^[c,d] · Arnulf Latz^[a,b,e] |
| 소속 | [a] DLR Institute of Engineering Thermodynamics, Stuttgart · [b] Helmholtz Institute Ulm (HIU) · [c] Forschungszentrum Jülich IEK-1 + JARA-Energy · [d] RWTH Aachen, Institute of Mineral Engineering · [e] Ulm University, Institute of Electrochemistry |
| 교신 | moritz.clausnitzer@dlr.de |
| 저널 | *Batteries & Supercaps* **2023**, 6, e202300167 (16 쪽) |
| DOI | 10.1002/batt.202300167 |
| 투고/수정/게재 | Received April 20, 2023 · Revised June 26, 2023 · Accepted July 11, 2023 · Version of record July 25, 2023 |
| 라이선스 | `[인쇄]` Creative Commons Attribution (open access), © 2023 The Authors |
| 키워드 | `[인쇄]` all-solid-state batteries · composite cathode · continuum modeling · LLZO · microstructure-resolved simulation |
| 자금 | BMBF **FestBatt2** (03XP0435A) · BMWK **OptiKeraLyt** (03ETE016C) · US DOE + BMBF **CatSE2** (03XP0510D, 13XP0510A) · 계산자원 bwHPC / DFG INST 40/575-1 FUGG (JUSTUS 2) |
| 이해관계 | `[인쇄]` "There is no conflict of interest to declare." |
| 소프트웨어 | 구조 생성·소결: **GeoDict** (Math2Market GmbH, Kaiserslautern) · 전기화학: **BEST** (Battery and Electrochemistry Simulation Tool, Fraunhofer ITWM + DLR 공동개발, ref 46) |

`[해석]` **1호와 다른 진영이다.** 1호(Bielefeld/Weber/Janek)는 Giessen + VW, 황화물
(NMC/LPS·Li₆PS₅Cl) 축이고, 이쪽은 **DLR/Ulm(Latz 그룹) + Jülich(Guillon/Finsterbusch)**,
**산화물 소결(LLZO) 축**이다. 그리고 이 논문은 1호를 **ref 35·36·63 으로 세 번 인용**한다
— ref 63 이 정확히 우리 1호 (J. Phys. Chem. C 2019, 123, 1626) 다. 즉 **2호가 1호를
명시적으로 딛고 서 있다.** `[인쇄, p2]` "Bielefeld et al. investigated the effect of the
structural properties … **GB effects in the SE are generally expected to be minor in
Li₆PS₅Cl and were, consequently, neglected in this study**" — 1호가 뺀 것을 이 논문이
넣는다는 선언이다.

---

## 1. 초록 — 무엇을 주장하는가

`[인쇄, 초록]` 요지 6 문장:

1. ASSB 는 고에너지·고출력 응용의 enabler 로 여겨지나 여러 제약 때문에 이론 잠재력에
   못 미친다.
2. 문제 하나는 **불충분한 전하 수송 동역학** — "material inherit limitations"(재료
   고유 한계)과 **비최적화 설계** 양쪽에서 온다.
3. 따라서 양극 미시구조의 관련 물성에 대한 이해가 필요하다.
4. 이 논문은 **구조분해 전기화학 3D 시뮬레이션**으로 복합양극의 최적화 여지를 찾는다.
5. 조사 축: **CAM 분율 · 밀도 · 입자 크기 · 활물질 물성**. **특별한 초점은 입계(GB)가
   양극 설계에 미치는 영향**.
6. 결과로 **제조를 위한 목표값(target values)을 예측**하고 개선된 양극 설계를 위한
   최적화 전략을 드러낸다.

`[해석]` **1호의 초록과 달리 이 초록은 계산되지 않은 양을 주장하지 않는다.**
"target values" 는 실제로 본문에 있다 — `[인쇄, p12]` "This indicates an **upper limit of
a tolerable GB resistance between `R_GB,2` and `R_GB,3`**"(즉 0.36–3.6 Ω cm² 사이) 와
`[인쇄, p9]` "the GB resistance must not significantly exceed values measured in dense
pellets". 초록–본문 일치도는 1호보다 **훨씬 좋다.**

다만 `[해석]` 초록의 "**structure-resolved electrochemical 3D-simulations**" 라는 표현이
숨기는 것 하나: **기하 지표와 전기화학이 서로 다른 해상도의 격자에서 계산된다**(G6).

---

## 2. 서론 — 이 논문이 서 있는 자리

`[인쇄, p1–p2]` 논증 순서:

1. **동기**: 재생에너지 전환·전동화 → Li-ion 이 150 $/kWh 에 접근했지만 기술 한계에
   도달 중(ref 4) → ASSB. SE 는 **Li 금속 음극**을 가능하게 해 에너지밀도를 크게 올린다.
2. **SE 분류 4 종**: polymer · sulfide · oxide · halide. 그중 **가넷형 Li₇La₃Zr₂O₁₂
   (LLZO)** 가 **넓은 전기화학 안정 창 · 합리적 이온전도도 · 좋은 열안정성**으로 두드러진다.
3. **그런데 LLZO 의 대가**: `[인쇄]` "the manufacturing of dense pellets typically includes
   a **high-temperature sintering step**, which increases production costs and can cause
   detrimental side reactions and secondary phases in contact with the cathode active
   material (CAM)"(ref 13–17). 그리고 `[인쇄]` "the effect of **grain boundaries is most
   prominent in LLZO** and can reduce the Li-ion conductivity significantly"(ref 18).
4. **복합양극의 요구 충돌**: 에너지밀도를 위해 CAM 을 최대화해야 하는데, 출력밀도를
   위해선 **큰 표면적과 짧은 수송 경로**가 필요하다(ref 17). 이상적으로는 두 물질이
   **각각 퍼콜레이팅 네트워크**를 이룬다.
5. **액체셀과의 결정적 차이**: `[인쇄, p2]` "In a conventional Li-ion battery, **liquid
   electrolyte infiltrates the porous CAM structure, naturally forming the required 3D
   network**. However, in case of an ASSB, SE and CAM particles **must be mixed and
   densified**. Any significant remaining pores … negatively impact battery performance
   by blocking transport pathways and reducing the surface area for charge transfer."
   + `[인쇄]` "composite cathodes in ASSBs feature a **high number of solid-solid
   interfaces** that pose an additional barrier for charge transfer"(ref 19).
6. **열화 언급 (단 한 문단)**: `[인쇄, p2]` "the cathode is **prone to electrochemical and
   mechanical degradation during cell manufacturing and operation**. These can lead to
   the formation of **secondary phases and voids, which impede charge transfer and
   significantly limit cell performance**"(ref 17, 21).
7. **선행 연구 정리**:
   - CAM 분율 ↑ → SE 상 굴곡도 ↑ → 유효 **이온** 전도도 ↓; CAM 분율 ↓ → 유효 **전자**
     전도도 ↓ (ref 22–28).
   - `[인쇄]` "Generally, **SE particles should be smaller than CAM particles** to ensure
     good SE/CAM contact"(ref 24, 29). 작은 SE 입자는 좋은 이온 퍼콜레이션·균질 분포·
     낮은 굴곡도를 준다(ref 22). **그러나 GB 가 전하이동 저항을 올려 유효 전도도를
     낮춘다**(ref 19, 29, 38, 39).
   - CAM 입자 크기는 퍼콜레이션 네트워크 형성과 **CAM 내 평균 확산 길이** 양쪽을 정한다
     (ref 21, 30).
8. **선행 시뮬레이션 3 계보** (이 논문이 자기 자리를 잡는 문단):
   - **Bielefeld et al.**(ref 35, 36) — NMC811/Li₆PS₅Cl. `[인쇄]` GB 효과는
     Li₆PS₅Cl 에서 미미할 것으로 기대되어 **무시됐다**.
   - **Finsterbusch et al.**(ref 31) — LCO/LLZO 의 **FIB-SEM 재구성**을 기반으로 공극과
     양극 두께를 바꿔 본 구조분해 시뮬레이션. `[인쇄]` "The SE was treated as
     **homogeneous phase not resolving individual GBs**."
   - **Neumann et al.**(ref 38, 40, 41) — 2021, **GB 전하이동 저항 모형**을 도입.
     `[인쇄]` "This model allows for **efficient simulation of grain boundary resistances
     without spatially resolving them explicitly**."
9. **공백 선언**: `[인쇄, p2]` "This approach allows **for the first time** to consistently
   consider the effect of **different SE and CAM particle size** in the optimization of
   the composite microstructure."

`[해석]` 서론이 **열화를 원인 목록에 넣지만**(6번), 1호와 똑같이 그것을 **동기로만**
쓰고 모델에 넣지 않는다. 다만 차이가 하나 있다: 1호는 "AM 부피변화 → 접촉 손실" 을
**첫 번째 원인**으로 올렸고, 이 논문은 **제조(소결 밀도)** 를 첫 번째로 올린다.
→ 두 논문이 `θ` 하락의 **서로 다른 원인**(사이클 vs 제조)을 가리키면서, 둘 다 그
**시간 변화는 안 푼다** (§15-3).

---

## 3. METHODS — 시뮬레이션 흐름 (Fig. 1, p3)

**Fig. 1 을 직접 봤다.** `[도표]` 4 칸 흐름도:
- 좌하 **Structure Generation** ("Adjust CAM fraction, density and particle sizes")
- → (Basic Microstructure) → 좌상 **SE Segmentation** ("Assign SE particles to different
  material IDs to define grain boundaries")
- → (Segmented Microstructure) → 우상 **Electrochemical Simulations**
- 좌하 → (Structural Properties) → 우하 **Geometrical Analysis**
- 우상 ↔ 우하 사이에 **빨간 양방향 화살표 "Structure-Performance Correlations"**

`[해석]` ★ 그림이 정직하게 말해 주는 구조적 사실: **기하 분석은 분할(segmentation)
전의 구조에서**, 전기화학은 **분할 후 구조에서** 돈다. 본문도 같은 말을 한다
`[인쇄, p6]` "we calculate geometrical characteristics from the **unsegmented** cathode
structures, while additionally taking into account GBs in the electrochemical simulations."
→ Fig. 2·3·6·7·9(기하)와 Fig. 4·5·8·10·11(전기화학)은 **서로 다른 전처리를 거친 구조**의
결과다. 그리고 G6(복셀 2 배)까지 겹치면 두 축은 **같은 격자의 같은 구조가 아니다.**

---

## 4. METHODS — 미시구조 생성 (p3 + SI p2–p3)

### 4.1 5 단계 절차

`[인쇄, p3]` GeoDict 의 **process-mimetic** 알고리즘(ref 42 = Al-Jaljouli et al.,
*J. Energy Storage* 2023, 68, 107784):

1. CAM + LLZO 입자 혼합물을 **퇴적(piling / sedimentation)**. 목표 CAM 부피분율로 전체
   부피분율을 스케일, 목표 체적평균 지름으로 치수를 균일 스케일. 도메인
   **250×250×650 voxel (25×25×65 µm³)**, **voxel 100 nm**, 최장축(z) 방향으로 채움.
2. **크롭** → 250×250×**500** voxel (25×25×**50** µm³), **중앙 정렬** — `[인쇄]` "to remove
   regions of **lower packing density and deviating CAM solid volume fractions**".
3. `[인쇄]` "In order to prevent **unrealistic shading effects from the piling**, the
   particles were **distributed for uniform spacing**."
4. **기하학적 소결** — GeoDict 의 **Voronoi tessellation** 알고리즘(ref 43)으로 목표
   밀도까지.
5. 최종 CAM 고상 부피분율·밀도를 목표와 대조, 편차가 크면 입력을 조정해 1–4 반복해
   **최대 편차 0.25 %** 를 보장. 이때 **DFSANE**(derivative-free spectral approach for
   solving nonlinear systems, ref 44)을 쓴다.

`[인쇄, p3]` ★ 용어 정의: "**when referring to particle size, we specifically refer to the
mean particle diameter _before_ the geometric sintering process**, which can be interpreted
as the mean particle size of the **powder materials**."

**Fig. S1 을 직접 봤다.** `[도표]` 4 개 직육면체(a 퇴적 후 → b 분산 후 → c 크롭 후 →
d 소결 후), 진회색 CAM · 연회색 LLZO, 각 **10 µm 스케일바**, 우하단 `x/y/z` 축 표시.
(a)(b) 가 (c)(d) 보다 눈에 띄게 **길다**(65 → 50 µm 크롭). (a) 의 **맨 위 층이 성기고
입자 형상(육각기둥·구)이 또렷이 보이는 반면** 아래로 갈수록 조밀 — 크롭이 지우는
"낮은 충전밀도 영역" 이 그림에서 확인된다. (d) 는 (c) 보다 입자 경계가 뭉개지고 덩어리져
있다 — 기하학적 소결의 효과.
`[인쇄, SI p2]` 이 예시는 퇴적 직후 **54 % 이론밀도**, 소결 후 **80 %**, `SVF_LCO = 50 %`,
`d_LCO = 2.00 µm`, `d_LLZO = 1.41 µm`.

### 4.2 Table S1 — 입력 입자 집단 (★ 1호와 가장 크게 다른 자리)

`[인쇄, SI p2, Table S1]` 퇴적 단계에 넣는 입자의 **형상·부피분율·기본 지름/두께**:

| 물질 | 형상 | 상(相) 내 부피분율 | 기본 지름* | 기본 두께 |
|---|---|---:|---:|---:|
| **CAM** (LCO 또는 NMC811) | Hexagonal | 43.9 % | 6.0 µm | 2.0 µm |
| | Hexagonal | 30.3 % | 5.0 µm | 1.5 µm |
| | Hexagonal | 15.2 % | 3.3 µm | 1.0 µm |
| | Sphere | 7.6 % | 3.0 µm | – |
| | Sphere | 3.0 % | 1.5 µm | – |
| **LLZO** | Sphere | 5.9 % | 2.5 µm | – |
| | Sphere | 35.3 % | 1.0 µm | – |
| | Sphere | 58.8 % | 0.5 µm | – |

\* `[인쇄]` "outer diameter of the hexagon or sphere".

`[인쇄, SI p2]` 각 상의 부피분율은 **공통 인자로 곱해** 목표 CAM/LLZO 분율을 맞추고,
지름·두께도 **균일하게 조정**해 목표 체적평균 지름을 맞춘다. `[인쇄]` "It was previously
shown that with these parameters the **experimental microstructure can be well matched**"(ref 1
= Al-Jaljouli 2023). `[인쇄]` "the initial diameters in the article **do not necessarily match
the particle size distribution of the starting powders** in the experiment due to the fact
that the sintering algorithm in GeoDict is **mimicking** the sintered structures, but is **not
reflecting a physical sintering model**."

`[해석]` ★ **이것이 1호와의 가장 큰 모델링 차이다.**

| | 1호 Bielefeld 2019 | 2호 Clausnitzer 2023 |
|---|---|---|
| CAM 형상 | **구 하나, 균일 입도, 겹침 없음** | **육각판 3 종 + 구 2 종 혼합, 5 성분 다분산** |
| SE 형상 | 볼록다면체, **3 µm 고정**, 겹침 허용 | **구 3 종(0.5/1.0/2.5 µm) 다분산**, 소결로 융합 |
| 결합 방식 | 겹침을 AM 에 배정 | **Voronoi 기하 소결**로 목표 밀도까지 성장 |
| 입도분포 | `[인쇄]` "oversimplification" 을 자인하며 **후속 과제로 미룸** | **처음부터 다분산**, 게다가 실험 미시구조에 맞춘 것 |

→ **1호의 닫힌 형태 `p_c = [7.83 ln(d/µm) + 36.67] vol%` 를 이 논문 구조에 그대로
적용할 수 없다.** 1호의 적용 조건("AM 구·균일 입도·겹침 없음")이 여기서 전부 깨진다.

---

## 5. METHODS — SE 분할과 입계 모형 (p3 + SI p4–p5)

### 5.1 분할 (SNOW / watershed)

`[인쇄, p3]` "We segment the electrolyte in the virtual microstructures using a
**marker-based watershed algorithm**(ref 45) to resolve individual grains. The identified
particles are **randomly assigned to 8 different material IDs. Interfaces of different IDs
represent GBs.** Further increasing the ID number did not yield any noticeable changes in
cell performance."

`[인쇄, SI p4]` 구체적으로 **SNOW 알고리즘**(Gostick 2017, ref 2): 거리변환 → σ 가우시안
블러 → 반지름 `R` 구형 구조요소 최대필터로 peak 추출 → 안장점·평탄부 peak 제거 + 너무
가까운 peak 병합 → watershed. `[인쇄]` Gostick 의 기본값 **σ = 0.35, R = 5** 를 기본으로
쓰되 "in some cases, **oversegmentation or loss of information still occurred**. Since the
**number of grain boundaries is a crucial factor** in determining the optimum SE particle
size, the segmentation parameters for the relevant structures (cf. Figure 10) were
**carefully adjusted**."

`[해석]` ⚠ **8 개 ID 무작위 배정의 대가**: 인접한 두 grain 이 같은 ID 를 받을 확률이
**1/8** 이므로 **GB 의 약 12.5 % 가 조용히 사라진다.** 논문은 ID 수를 늘려도 성능이
안 변한다고 적어 이 문제를 다뤘다고 볼 수 있으나, 그 대조 데이터는 인쇄돼 있지 않다.

`[해석]` ⚠ 더 큰 문제: **GB 개수가 결론을 좌우한다고 논문 스스로 말하면서, 그 GB
개수를 정하는 분할 파라미터를 "구조별로 손으로 조정" 했다.** Table S2 가 그 조정값이다.

### 5.2 Table S2 — 분할 파라미터와 결과 입경

`[인쇄, SI p5, Table S2]` 전부 `SVF_LCO = 50 %`, `ρ_S = 93.1 %`, `σ = 0.35`:

| `d^Init_LCO` (µm) | `d^Init_LLZO` (µm) | `R` | `d^seg_LLZO` (µm) |
|---:|---:|---:|---:|
| 2.00 | **0.70** | **2** | 1.09 |
| 0.80 | 1.41 | 4 | 1.55 |
| 2.00 | 1.41 | 4 | **1.76** |
| 3.00 | 1.41 | 4 | 1.75 |
| 3.50 | 1.41 | 4 | 1.75 |
| 8.00 | 1.41 | **2** | **4.56** |
| 2.00 | 3.00 | **8** | 3.13 |
| 2.00 | 3.50 | **8** | 3.18 |

`[해석]` ★ **이 표가 Fig. 10 의 해석을 흔든다.** 두 가지:
1. **`R` 이 구조마다 2·4·8 로 다르다** — `R` 은 peak 검출 반경이고 그것이 grain 개수,
   따라서 **GB 개수**를 정한다. GB 개수가 용량을 정하는 논문에서 **GB 개수를 정하는
   하이퍼파라미터가 구조마다 손으로 바뀌었다.**
2. **`d^Init_LLZO = 1.41 µm` 인데 `d^seg_LLZO = 1.76 µm`** — 즉 "입경" 이라 부르는 축과
   실제 GB 를 만드는 grain 크기가 **25 % 어긋난다**. 더 심한 것은 `d^Init_LCO = 8.00` 행:
   LLZO 입경은 그대로 1.41 µm 인데 `R` 이 2 로 바뀌면서 `d^seg_LLZO` 가 **4.56 µm** 이
   된다 — **같은 LLZO 분말이 3.2 배 다른 grain 으로 분할된다.** Fig. 10 에서 `(d_SE=1.41,
   d_CAM=8.0)` 점의 성능은 그래서 "큰 CAM 입자의 효과" 와 "분할이 만든 큰 grain 의
   효과" 가 **교란**돼 있다. 논문은 이 교란을 논하지 않는다.

**Fig. S3 을 직접 봤다.** `[도표]` 분할 후 SE 입경 분포 4 패널(`d^Init_LCO = 2.00 µm`,
`SVF_LCO = 50 %`, `ρ_S = 93.1 %` 고정), x = Particle diameter (µm), y = Probability:
- (a) `d^Init_LLZO = 0.70` — 0.5–1.5 µm 에 두 막대(0.40, 0.38)로 몰림, 꼬리 ~3 µm
- (b) `1.41` — 1.0–1.5 에 최빈(0.435), **2.5–3.0 에 두 번째 봉우리(0.17)**, 0–4 µm 에 걸침
- (c) `3.00` — 2–2.5 최빈(0.415), **4.5–6 µm 에 넓은 꼬리**, 0–6.5 µm
- (d) `3.50` — 2.5–3 최빈(0.555), 꼬리 ~7 µm

`[해석]` 분포 폭이 **평균의 배 이상**이다. "SE 입경" 이라는 한 숫자로 요약되는 축이
실제로는 **1 옥타브 넘게 퍼진 분포**이고, (b) 는 **명백히 이봉**이다. 논문이 Fig. 10 에서
`d_SE` 를 4 개 점으로 스캔할 때 그 점들은 서로 **분포가 상당히 겹친다.**

### 5.3 GB 전류 모형 (식 1)

> **식 (1)** `i_GB = i₀^GB [ exp(Δφ̃/2RT) − exp(−Δφ̃/2RT) ]`

`[인쇄, p3]` "The current density depends on the **local difference in electrochemical
potential Δφ̃** at the interface between two adjacent grains. The GB resistance is linked to
the exchange current density `i₀^GB` which can be **estimated from electrochemical impedance
spectroscopy (EIS) measurements**"(ref 38 = Neumann et al. 2021).

`[인쇄, Table S3]` 여기에 **공간전하층(space charge layer)** 이 하나 더 붙는다:
`i^GB_DL = C^GB_DL ∂Δϕ_DL/∂t`, 총 `i_SE-SE = i₀^GB + i^GB_DL`.
(Table 1 의 `C^GB_DL = 9.75×10⁻⁹ F/cm²`.)

`[해석]` ⚠ Table S3 의 마지막 줄 `i_SE-SE = i₀^GB + i^GB_DL` 은 **그대로 읽으면 틀렸다** —
BV 전류 `i_GB`(식 1) 가 아니라 교환전류밀도 `i₀^GB` 를 더하고 있다. `i_GB + i^GB_DL` 의
오식으로 보인다 (§13 불일치 9). G9(지수의 `F` 누락)과 같은 종류의 조판 오류다.

---

## 6. METHODS — 전기화학 모형과 파라미터 (p3–p5)

### 6.1 지배방정식 (Table S3)

`[인쇄, SI p6, Table S3]` BEST 의 지배방정식 — Latz & Zausch 이론(ref 47, 48):

```
활물질:   ∂c_AM/∂t = −∇·(−D_AM ∇c_AM)        (질량)
          0 = −∇·i_AM ,  i_AM = −σ_AM ∇Φ_AM   (전하 / 전자 전류)
고체전해질 (t⁺_Li = 1):
          0 = −∇·i_SE ,  i_SE = −κ_SE ∇Φ_SE   (전하 / 이온 전류)
AM|SE 계면:
          i_BV = i₀ [ exp(αF η/RT) − exp(−(1−α)F η/RT) ]
          i₀ = i₀₀ c_e^α c_s^α (c_max_s − c_s)^(1−α)
SE grain 간:  식 (1) + 이중층
```

`[해석]` 중요한 구조적 사실 셋:
1. **SE 상에 농도 방정식이 없다** — `t⁺ = 1` 이므로 염 농도 구배가 없다. 액체셀
   P2D(PyBaMM DFN)와 다른 자리. `[인쇄, p4]` "This implies that Li-ions move **exclusively
   due to migration in the electric field** and **no concentration gradients form in the
   electrolyte phase**."
2. **AM 상에는 확산이 있다** — 입자 내부 확산이 풀린다. 이것이 Fig. 5 의 히스토그램에서
   "입자 중심이 덜 리튬화" 로 나타난다.
3. **역학(mechanics)이 없다.** 응력·부피변화·균열이 방정식에 없다 (G13).

### 6.2 Table 1 — 입력 파라미터 (PDF 텍스트로 읽음, 이미지 아님)

`[인쇄, p4, Table 1]` (`*` = 농도 의존 함수형 파라미터, 표시값은 초기 조건):

| 구분 | 기호 | 값 | 단위 | 설명 | 출처 |
|---|---|---:|---|---|---|
| **Li 금속** | `U^AN_0` | 0 | V | 개회로 전위 | – |
| | `σ^AN_Li` | 1 | S/cm | 전자 전도도 | – |
| | `i^Li_0` | 2.59×10⁻² | A/cm² | 교환전류밀도 | [38] |
| | `α_Li` | 0.5 | – | 대칭 인자 | – |
| **LLZO** | `c^SE_Li` | 0.0384 | mol/cm³ | Li 이온 농도 | [38] |
| | `κ^SE_Li` | **7.69×10⁻⁴** | S/cm | **Li 이온 bulk 전도도** | [38] |
| | `D^SE_Li` | 5.36×10⁻⁹ | cm²/s | Li 이온 확산계수 | [38] |
| | `t⁺_Li` | 1 | – | 수송률 | – |
| | `i^GB_0` | **6.91×10⁻³** | A/cm² | **GB 교환전류밀도** | [38] |
| | `C^GB_DL` | 9.75×10⁻⁹ | F/cm² | GB 이중층 용량 | [38] |
| | `l_sep` | **25** | µm | 분리막 두께 | – |
| **LCO** | `U^CAM_0` * | **4.2** | V | **개회로 전위** | [56] Landstorfer 2011 |
| | `c^CAM,0_Li` | 0.027058 | mol/cm³ | 초기 Li 농도 | [31] |
| | `c^CAM,max_Li` | 0.051555 | mol/cm³ | 최대 Li 농도 | [57] |
| | `σ^CAM_Li` * | 4.47 | S/cm | 전자 전도도 | [58] Molenda 1989 |
| | `D^CAM_Li` * | 8.48×10⁻¹² | cm²/s | Li 확산계수 | [59] Xia 2006 |
| | `i^CAM_00` | 0.0116 | A cm^2.5 / mol^1.5 | 교환전류밀도 인자 | [54] 에서 계산 |
| | `α_Li` | 0.5 | – | 대칭 인자 | [31] |
| **경계** | `i_I` | **1** | mA/cm² | **방전 전류밀도** | – |
| | `U_cut` | **3.4** | V | **하한 컷오프 전압** | – |

`[재현]` 초기 Li 점유율 `x₀ = c^CAM,0/c^CAM,max = 0.027058/0.051555 = **0.5248**` —
Fig. 5 히스토그램의 왼쪽 끝(≈0.52)과 일치한다. 즉 모든 방전 시뮬레이션은
**Li₀.₅₂₅CoO₂ → Li₁CoO₂** 구간이다.

`[재현]` 식 (8) 로 LCO 의 이론 용량:
`C^theo_grav,Ca = (c_max − c₀)·F/ρ_CAM = 0.024497 × 96485 / 5.051 = 467.9 C/g = **129.98 mAh/g**`.
→ 본문의 "LCO 116 mAh/g" 는 **정규화 용량 0.895** 에 해당한다 (`0.895 × 129.98 = 116.3`).
Fig. 11a `[도표]` 의 LCO 최대 정규화 용량 ≈90 % 와 일치한다. **식 (7)(8)–본문–그림이
서로 검증된다.**

### 6.3 Table 2 — NMC811 파라미터

`[인쇄, p13, Table 2]` (`*` = 함수형):

| 기호 | 값 | 단위 | 출처 |
|---|---:|---|---|
| `U^NMC_0` * | 4.2 | V | [36] Bielefeld 2022 |
| `c^NMC,0_Li` | 0.01131 | mol/cm³ | Calc. |
| `c^NMC,max_Li` | 0.04903 | mol/cm³ | Calc. |
| `σ^NMC_Li` * | **8.83×10⁻³** | S/cm | [52] Amin & Chiang 2016 |
| `D^NMC_Li` * | **8.71×10⁻¹³** | cm²/s | [53] Ruess 2020 |
| `i^NMC_00` | 0.0116 | A cm^2.5 / mol^1.5 | [54] 에서 계산 (= LCO 와 **동일**, G11) |

`[재현]` `x₀(NMC) = 0.01131/0.04903 = **0.2307**`. `ρ_NMC` 가 인쇄되지 않아(G4) 이론용량을
직접 못 구한다 — 본문 수치에서 역산하면 `C^theo(NMC) = 133/0.65 = **204.6 mAh/g**`
(그리고 `172/204.6 = 0.841`, Fig. 11a `[도표]` 의 NMC 최대 정규화 용량 ≈85 % 와 일치),
이로부터 `ρ_NMC = 0.03772 × 96485/(204.6 × 3.6) ≈ **4.94 g/cm³**`.

`[해석]` 대조로 읽을 것: **`σ` 는 LCO 가 NMC 의 506 배**(4.47 vs 8.83×10⁻³),
**`D` 는 9.7 배**(8.48e-12 vs 8.71e-13). 그러나 **용량은 NMC 가 1.57 배**
(204.6 vs 130.0 mAh/g). 이 세 비(比)가 §11 의 전체 결론을 만든다.

### 6.4 SE/CAM 계면과 Li 금속

`[인쇄, p4]` 계면 교환전류밀도는 **ref 54 (Kato et al. 2014)** 의 EIS 에서:
`R_CT = **2600 Ω cm²**` → 식 (2) `i₀ = RT/(zFA·R_CT)` 로 선형화.
`[인쇄, p4]` Li 금속은 "**assumed to be in ideal contact with the SE separator**",
파라미터는 ref 38.

`[해석]` ★ 닻의 Q7(dead Li ↔ SEI)에 대한 답이 여기서 끝난다: **음극은 이상적이라고
가정됐다.** 열화도 계면층도 없다. `indium` 0 회, `pressure` 0 회.

### 6.5 시뮬레이션 설정

`[인쇄, p4–p5]` 측면 경계 **주기 경계조건**, 모든 시뮬레이션에서 **정전류 방전
1 mA/cm²**. 근거: `[인쇄]` "This value falls within the range of reported **critical
current densities** for garnet-type electrolytes in contact with Li-metal anodes"(ref 60).
그리고 `[인쇄]` "**At lower current densities, local currents and overpotentials are
generally lower, resulting in reduced sensitivity to microstructural variations.**"
방전은 **3.4 V 에서 정지**.

`[해석]` ★★ **밑줄 친 문장이 이 논문에서 우리에게 가장 값진 인식론적 진술이다.**
논문 스스로 "전류를 낮추면 미시구조 민감도가 줄어든다" 고 적었다. 뒤집으면:
**이 논문이 보고하는 미시구조 효과의 상당 부분은 전류가 만든 것**이고,
**`i → 0` 극한(= pOCV/OCV 적합의 영역)에서는 사라진다.** 이것이 §16 의 분리 시험이다.

---

## 7. 정의 — 기하·전기화학 지표 (p5–p6)

### 7.1 고상 부피분율 (식 3) — ★ 1호와의 좌표 변환

> **식 (3)** `SVF_CAM = V_CAM / (V_CAM + V_SE)`

`[인쇄, p5]` "In this context, `SVF_CAM` gives the ratio of active material volume to the
total solid volume and, thus, **is independent of porosity**."

`[해석]` ★ **1호의 `g^S_AM` 과 정확히 같은 양이다.** 1호는 두 종류를 썼다:
`g^V_AM`(전체 구조 부피 기준, 공극 포함)과 `g^S_AM`(고상만). 2호는 **`g^S` 하나만**
쓰고 이름을 `SVF` 로 바꿨다. 변환은 1호의 식 (9) 그대로:

```
SVF_CAM  ≡  g^S_AM  =  g^V_AM / (1 − φ)  =  g^V_AM / ρ_S
```

여기서 이 논문의 **`ρ_S`(density after sintering) = 1 − φ**(= 고상 부피분율, 이론밀도
대비 %)다. 즉 **두 논문의 조성 축은 변환 없이 비교 가능하고**, 공극률 축만 부호가
뒤집힌 같은 양(`ρ_S = 1 − φ`)이다. 예: `SVF_LCO = 50 %`, `ρ_S = 93.1 %` →
`g^V_CAM = 0.4655` (1호 그림들의 아래 x 축 좌표).

### 7.2 활성 면적

`[인쇄, p5]` "The active area was determined by calculating the **number of neighboring SE
and CAM voxel surfaces** using a **Euclidean distance transform** on the microstructure
data"(ref 61 = Ender et al. 2012). 그림에서 단위는 **`A_act/V_ca` [1/cm]**.

`[해석]` 1호의 **`A_spec,a`**(이온 클러스터 SE ↔ 전자 클러스터 AM 계면적 / 구조 부피,
m²/m³)와 **같은 종류의 양**이지만 **두 가지가 다르다**:
1. 1호는 **퍼콜레이팅 클러스터에 속한** SE·AM 사이만 센다. 2호는 Fig. 9 에서는 그냥
   이웃 복셀면을 센다 (Fig. 7 은 `[인쇄]` "Isolated material clusters were **removed** from
   the structures before computing the active area" 라고 밝힌다 — **두 그림의 정의가
   서로 다르다**, §13 불일치 6).
2. 단위가 `1/cm` vs `m²/m³`. `[재현]` **`1 m²/m³ = 10⁻² 1/cm`**, 즉
   `6000 1/cm = 6.0×10⁵ m²/m³`. → 2호 Fig. 7 의 ≈6150 1/cm ↔ 1호 Fig. 3 의 5 µm·66 vol%
   포화값 ≈6.75×10⁵ m²/m³ = 6750 1/cm. **같은 자릿수다.**

### 7.3 연결성 (식 4) — ★★ 1호의 `θ` 와 같은 양

> **식 (4)** `Connectivity = 1 − n_iso,j / n_tot,j`

`[인쇄, p5]` "**Isolated SE clusters include electrolyte particles that are not connected to
the separator** and do not contribute to the ionic conduction network. Similarly, **isolated
active material particles are not connected to the cathode current collector.** Before
starting the electrochemical simulations, isolated clusters were removed from the input
structure to improve numerical stability."

`[해석]` ★★ **이것이 1호의 이용률 `θ = V_c/V_ν`(식 6) 와 같은 양이다.** 근거 셋:

| | 1호 `θ_ν` | 2호 `Connectivity_j` |
|---|---|---|
| 분모 | 그 성분의 전체 부피 `V_ν` | 그 상의 전체 복셀 수 `n_tot,j` |
| 분자 | **퍼콜레이팅 클러스터**에 속한 부피 `V_c` | 전체 − **격리된** 복셀 `n_tot − n_iso` |
| 전자 쪽 클러스터의 출발 경계 | **집전체** | **집전체**("not connected to the cathode current collector") |
| 이온 쪽 클러스터의 출발 경계 | **분리막** | **분리막**("not connected to the separator") |
| 알고리즘 | Hoshen−Kopelman | (명시 안 함) |

균일 복셀에서 복셀 수 비 = 부피 비이므로 **`Connectivity_CAM ≡ θ_AM`, `Connectivity_SE ≡ θ_SE`**.
→ **두 논문의 숫자를 변환 없이 견줄 수 있다.** (⚠ 단 2호는 클러스터 판정 알고리즘을
밝히지 않고, 격리의 정의가 "경계에 연결 안 됨" 이라는 문장 하나뿐이다.)

### 7.4 유효 전도도·굴곡도 (식 5, 6)

> **식 (5)** `σ_eff,i = l·j / U`  (`U = 1 V` 를 양극 구조 양단에 걸고 Poisson 방정식을 풀어
> SE 망과 CAM 망 각각의 전류밀도 `j` 를 구한다; `l` = 시료 두께)
> **식 (6)** `τ_i = sqrt(σ_i/σ_eff,i) · ε_i`   (ref 62 = Tjaden 2018)

`[해석]` ★ **1호가 한 번도 안 한 계산이 여기 있다.** 1호는 `conductivit*` 18 회,
`S/cm` **0 회**였다 (1호 digest G1). 2호는 **절대값을 SI Fig. S4 에 S/cm 로 찍는다.**
→ 닻의 공백 하나가 채워졌다.

⚠ 식 (6) 의 형태가 통상 정의와 다르다. 일반적으로는 `τ = ε·σ_bulk/σ_eff`
(또는 `τ² = ε σ/σ_eff`). 여기 인쇄된 것은 **`τ = sqrt(σ/σ_eff)·ε`** 다.
`[해석]` `sqrt` 는 `τ²` 정의에서 온 것으로 읽히지만, 그렇다면 `ε` 는 곱이 아니라
**나눗셈**이어야 통상 정의와 맞는다 (`τ = sqrt(ε σ/σ_eff)` 또는 `τ² = ε σ/σ_eff`).
**인쇄대로 읽으면 `ε → 0` 에서 `τ → 0`** 이라는 비물리적 극한이 나온다. 조판 오류로
보이나 확인 불가 (§13 불일치 8).

### 7.5 용량·에너지 (식 7–10)

> **식 (7)** `C_grav = C_3.4V / (V_CAM · ρ_CAM)`
> **식 (8)** `C^theo_grav,Ca = (c^CAM,max_Li − c^CAM,0_Li)·F / ρ_CAM`
> **식 (9)** `E_grav = ∫_{t0}^{tend} i·U dt / (m_An + m_Sep + m_Ca)`
> **식 (10)** `m_An = C^theo_grav,Ca · m_CAM / C^theo_grav,Li`

`[인쇄, p5]` "The normalized capacity `C_norm = C_grav / C^theo_grav,Ca` can be interpreted
as the **average utilization of the CAM in the electrode**."
`[인쇄, p6]` "We assume an **ideal balancing** of negative and positive electrode (n/p = 1)
and **neglect the weight of current collectors and cell housing**."
`[인쇄, SI Table S4]` `C^theo_grav,Li = 3861 mAh/g`, `ρ_SE = 5.3 g/cm³`, `ρ_CAM(LCO) = 5.051 g/cm³`.

`[해석]` ★★ **`C_norm` 이 이 논문에서 "utilization" 으로 불리는 양이고, 그것이 우리가
`LAM_PE` 라 부르는 자리에 정확히 앉는다.** 그런데 **G1** — `V_CAM` 이 격리 클러스터
제거 전인지 후인지 안 적혀 있어 `C_norm` 이 `Connectivity`(= `θ_AM`)를 포함하는지 모른다.
→ **1호의 `θ` 와 2호의 `C_norm` 이 같은 양인지 곱의 관계인지가 확정되지 않는다.** 이것이
이 digest 가 남기는 가장 큰 미해결 좌표다 (§15·§16, 후속 질문 1).

`[해석]` 에너지밀도는 **음극+분리막+양극 질량** 기준이고 분리막이 **25 µm LLZO
(ρ=5.3)** 이므로 **분리막 질량이 지배적으로 크다** — `[재현]` 분리막 면적당 질량
`25e-4 cm × 5.3 g/cm³ = 1.33e-2 g/cm²`; 양극 CAM 질량(`SVF 50 %`, `ρ_S 93.1 %`, 50 µm)
`= 50e-4 × 0.4655 × 5.051 = 1.18e-2 g/cm²`. → **Wh/kg 수치는 "25 µm LLZO 분리막" 가정에
강하게 의존한다.** 논문은 이 민감도를 논하지 않는다.

---

## 8. RESULTS — CAM 분율의 영향 (p6–p9)

### 8.1 Fig. 2 — 연결성과 굴곡도

**Fig. 2 를 직접 봤다.** `[도표]` x = `SVF_LCO / %` ∈ [30, 80], 좌 y = `Connectivity / %`
[0,100], 우 y = `1/Tortuosity` [0,1]. 삼각형 = 연결성(파랑 SE, 빨강 CAM), 원 = 1/굴곡도
(파랑 SE, 빨강 CAM). 그림 안에 `SVF=33 %`·`SVF=80 %` 의 **SE 상 3D 이미지 2 개**가
박혀 있다. 고정: `ρ_S = 93.1 %`, `d_CAM = 2.00 µm`, `d_SE = 1.41 µm`.

`[도표]` 읽은 값 (figure-read ≈):

| `SVF_LCO` (%) | 33.3 | 40 | 50 | 60 | 69.4 | 80 |
|---|---:|---:|---:|---:|---:|---:|
| Connectivity **SE** (%) | ≈99 | ≈100 | ≈100 | ≈100 | **≈95** | **≈16** |
| Connectivity **CAM** (%) | ≈99 | ≈100 | ≈100 | ≈100 | ≈100 | ≈100 |
| 1/τ **SE** | ≈0.745 | ≈0.69 | ≈0.58 | ≈0.45 | ≈0.265 | **≈0.00** |
| 1/τ **CAM** | ≈0.385 | ≈0.495 | ≈0.61 | ≈0.71 | ≈0.785 | ≈0.855 |

`[인쇄, p6]` 본문 서술:
- "At small LCO fractions, the connectivity of the CAM phase decreases. … However,
  **above `SVF_LCO = 33.3 %`, considered as lower limit in this study, the effect is not
  pronounced.** For even smaller CAM fractions, a significant decrease in connectivity and,
  hence, capacity is expected."
- "**Above `SVF_LCO = 70 %`, there is no longer a percolating network for ion transport** and
  the amount of SE particles connected to the separator **reduces to less than 20 %**."
- "CAM particles that are **not connected to the separator are not accessible to Li-ions,
  rendering them electrochemically inactive**."

`[해석]` ★ 마지막 문장이 중요하다 — **"격리" 가 두 방향으로 작동한다.** 1호는 AM 이
집전체에 안 붙으면(전자) 죽는다고만 했는데, 2호는 **SE 가 분리막에 안 붙으면 그에
닿은 CAM 도 죽는다**(이온)고 명시한다. 즉 `θ_AM` 만으로는 부족하고 **`θ_SE` 가 CAM 의
가용성에 직접 들어온다.** 이것이 고 CAM 분율에서 용량이 0 으로 떨어지는 기전이다.

`[해석]` ⚠ **본문–그림 어긋남 1**: "At small LCO fractions, the connectivity of the CAM
phase decreases" 인데 `[도표]` CAM 연결성은 33.3 %에서도 **≈99 %** 로 거의 평평하다.
(뒷문장이 "not pronounced" 로 완화하므로 거짓 진술은 아니지만, **그림은 감소를 보여
주지 않는다.**) `[도표]` Fig. 6b 를 보면 그 감소는 **낮은 소결 밀도에서만** 나타난다
(60 % 밀도, `SVF 33.3 %` → CAM 연결성 ≈84.5 %).

`[해석]` ⚠ **캡션 어긋남 2**: 캡션은 "Influence of the solid volume fraction of LCO on
connectivity and tortuosity of **the electrolyte network**" 인데 그림은 **두 상 모두**를
보여 준다. 그리고 캡션 끝에 "The discharge simulations were conducted at a current density
of 1 mA/cm²" 라고 적혀 있으나 **이 그림에는 방전 시뮬레이션이 전혀 들어 있지 않다**
(순수 기하량). 상투 문구 복사로 보인다.

### 8.2 Fig. 3 — 유효 부분 전도도와 실험 대조

**Fig. 3 을 직접 봤다.** `[도표]` 두 패널 모두 y = `Norm. conductivity / -` (log, 10⁻³–10⁰).
(a) "Ionic", x = `SE fraction / vol%` ∈ [10, 100]. (b) "Electronic", x = `CAM fraction / vol%`.
파란 네모 = Experiment (Minnmann et al. ref 22), 주황 원 = Simulation, 주황 점선 = 안내선.

`[도표]` 읽은 값 (figure-read ≈, 정규화 = bulk 대비):

| (a) 이온 | SE 분율 ≈30.6 | 40 | 50 | 60 | 66.7 | 100 |
|---|---:|---:|---:|---:|---:|---:|
| Simulation | ≈2.0e-2 | ≈7.0e-2 | ≈1.6e-1 | ≈2.6e-1 | ≈3.5e-1 | (1) |
| Experiment (근처 점) | ≈2.0e-3 (25) | ≈2.2e-2 (32) | ≈1.0e-1 (44) | ≈2.3e-1 (60) | – | ≈9e-1 (85) |

| (b) 전자 | CAM 분율 ≈33.3 | 40 | 50 | 60 | 69.4 | 80 |
|---|---:|---:|---:|---:|---:|---:|
| Simulation | ≈4.3e-2 | ≈8.5e-2 | ≈1.7e-1 | ≈2.8e-1 | ≈3.9e-1 | ≈5.3e-1 |
| Experiment (근처 점) | ≈2.6e-3 (26) | ≈3.0e-2 (33) | ≈6.5e-2 (43) | ≈1.4e-1 (56) | ≈1.7e-1 (64) | ≈9e-1 (100) |

`[인쇄, p6–p7]`:
- "we can identify **limiting SE and CAM fractions**, below which the effective conductivity
  **drops to 0** due to a loss of percolation … the limiting material fraction is
  **around 20 vol.% for both the SE and CAM**."
- "The simulations are in **qualitative agreement** with the experiments. However, the
  **simulated conductivities are slightly higher** for both ion and electron transport."
- "The good agreement between the simulations and the experimental data by Minnmann et al.
  indicates a **small GB resistance in Li₆PS₅Cl** electrolyte."
- "**Systematic conductivity measurements on LLZO based composite electrodes are lacking in
  the literature** and additional data is needed for **quantitative validation** of model
  predictions."

`[해석]` ⚠ **어긋남 3 (G7)**: "limiting material fraction ≈ 20 vol% for **both**" 에서
**CAM 쪽은 시뮬레이션된 점이 하나도 없다** — 최저 `SVF_LCO` 가 33.3 % 다. 그림에서
20 vol% 부근의 급락은 **점선(안내선)만** 그린다. 안내선의 함수 형태는 캡션·본문·SI
어디에도 없다. SE 쪽 20 vol% 도 `SVF_LCO = 80 %` **한 점**에서 나오고, 그 점은 `σ_eff = 0`
이라 **로그 축에 찍히지도 않는다.**

`[해석]` ⚠ **어긋남 4**: "simulated conductivities are slightly higher" 인데 `[도표]`
차이는 임계 근방에서 **한 자릿수(≈10 배)** 다 (예: 이온 25–31 vol% 구간에서 2.0e-3 vs
2.0e-2). "slightly" 는 고분율 영역에만 맞는다. 그리고 이 차이를 논문은 "Li₆PS₅Cl 의
GB 저항이 작다는 뜻" 으로 읽는데, **모델이 실험보다 높다는 것은 모델이 어떤 저항을
빠뜨렸다는 뜻**이지 그 반대가 아니다. (논문은 이어서 밀도·형상·접촉저항 차이를
후보로 든다 — 정직한 서술이다.)

`[해석]` ★ 그리고 **대조 실험이 다른 재료계다**(G10): NMC622/**Li₆PS₅Cl** vs 모델의
LCO/**LLZO**. 논문 스스로 LLZO 계 데이터가 없다고 적는다. → **이 논문의 재료계에 대한
정량 검증은 0 이다.**

### 8.3 Fig. 4 — GB 저항 → 정규화 용량·에너지밀도 ★

**Fig. 4 를 직접 봤다.** `[도표]` (a) x = `SVF_LCO / %` [30,80], 좌 y = `Norm. capacity`
[0,1] (원, 주황→진빨강), 우 y = `Norm. conductivity σ_eff` (log 10⁰–10⁻⁴, **파란 네모 점선**).
(b) 같은 x, y = `Energy density / Wh/kg_cell` [0,180].
`[인쇄]` 4 경우: `w/o GBs` · `R_GB,1 = 3.6×10⁻²` · `R_GB,2 = 3.6×10⁻¹` · `R_GB,3 = 3.6 Ω cm²`
(대응 `i₀^GB = 7×10⁻¹, 7×10⁻², 7×10⁻³ A/cm²`).

`[도표]` (a) 정규화 용량 (figure-read ≈):

| `SVF_LCO` (%) | 33.3 | 40 | 50 | 60 | 69.4 | 80 |
|---|---:|---:|---:|---:|---:|---:|
| w/o GBs | ≈0.875 | **≈0.895** | ≈0.888 | ≈0.865 | ≈0.805 | ≈0.02 |
| `R_GB,1` | ≈0.875 | ≈0.89 | ≈0.885 | ≈0.86 | ≈0.595 | ≈0.02 |
| `R_GB,2` | ≈0.87 | ≈0.89 | ≈0.835 | ≈0.49 | ≈0.145 | ≈0.02 |
| `R_GB,3` | **≈0.535** | ≈0.457 | ≈0.248 | ≈0.118 | ≈0.043 | ≈0.01 |

`[도표]` (a) 우축 `σ_eff`(정규화, 이온): w/o GBs ≈0.35 → 0.025 (33.3 → 69.4 %);
`R_GB,1` ≈0.12 → 0.0055; `R_GB,2` ≈0.032 → 8.9e-4; `R_GB,3` ≈0.0066 → 1.1e-4.

`[도표]` (b) 에너지밀도 (Wh/kg_cell):

| `SVF_LCO` (%) | 33.3 | 40 | 50 | 60 | 69.4 | 80 |
|---|---:|---:|---:|---:|---:|---:|
| w/o GBs | ≈90 | ≈113 | ≈140 | ≈165 | **≈173** | ≈5 |
| `R_GB,1` | ≈89 | ≈110 | ≈140 | **≈161** | ≈124 | ≈4 |
| `R_GB,2` | ≈89 | ≈110 | **≈125** | ≈87 | ≈30 | ≈3 |
| `R_GB,3` | ≈52 | **≈53** | ≈37 | ≈20.5 | ≈8.5 | ≈2 |

`[인쇄, p7–p8]`:
- "For the highest GB resistance `R_GB,3`, the effective conductivity is **approximately two
  orders of magnitude smaller** than in the simulation case with perfect inter-particle contact."
- "In case of negligible GB resistance, the maximum normalized capacity is **close to 0.9**
  indicating good utilization of the CAM. The capacity reaches a maximum for a solid volume
  fraction of LCO **around 40 %**."
- "**the maximum capacity shifts towards structures with lower LCO fractions.** … for the GB
  resistance reported in Ref. [38] the virtual structure with **`SVF_LCO = 30 %`** performs
  best … This result demonstrates that **electrode design and process development … cannot
  be done independently**."
- "the **optimal LCO:LLZO ratio shifts towards lower values**, indicating that a reduced
  tortuosity in the SE is necessary to counteract the high GB resistance."

`[해석]` ⚠ **어긋남 5**: "`SVF_LCO = 30 %` performs best" — **30 % 구조는 존재하지 않는다.**
시뮬레이션된 최저는 **33.3 %** 이고 그림에도 33.3 에만 점이 있다. 그리고 그 점이
`R_GB,3` 곡선의 **끝점**이므로 "최적" 이 아니라 **탐색 격자의 경계**다. 진짜 최적은 더
낮은 분율일 수 있고 논문은 그것을 보지 않았다.

`[해석]` ★★ **이 그림이 우리 물음에 주는 것**: 같은 `SVF_LCO = 50 %`, 같은 밀도, 같은
입경, **같은 양의 LCO** 를 두고 GB 저항만 바꾸면 정규화 용량이 **0.888 → 0.248** 로
간다. **재료는 1 g 도 잃지 않았는데 겉보기 용량이 72 % 사라진다.**
→ 닻이 묻는 "접촉 손실" 말고 **세 번째 후보**가 생겼다: **SE 내부 계면 저항**.
그리고 이것은 기하량(`θ`)으로도, 재료량(`Q_material`)으로도 설명되지 않는다 (§16).

### 8.4 Fig. 5 — CAM 이용률의 공간·입자 분포 ★

**Fig. 5 를 직접 봤다.** 고정: `SVF_LCO = 50 %`, `ρ_S = 93.1 %`, `d_CAM = 2.00`,
`d_SE = 1.41 µm`, 1 mA/cm².
`[도표]` (a) 히스토그램: x = `x in Li_xCoO₂` ∈ [0.5, 1], y = `Relative probability` [0, 0.25].
4 색(파랑 w/o GBs · 주황 `R_GB,1` · 노랑 `R_GB,2` · 보라 `R_GB,3`).
- 파랑·주황: **x ≈ 1 에 0.21–0.24 의 큰 막대 하나** + 0.85–1.0 에 완만한 분포. 거의 겹침.
- 노랑(`R_GB,2`): 봉우리가 **0.9–0.98 로 왼쪽 이동**, x=1 막대 없음.
- 보라(`R_GB,3`): **x ≈ 0.52–0.55 에 큰 막대(0.12, 0.10, 0.055…)**, 즉 **초기 농도 그대로**.
  긴 꼬리가 0.6–0.9 를 지나 0.95 부근에 작은 봉우리.

`[도표]` (a) 삽입 그림: x = `Cathode length / µm` [0, 50] (좌 `Sep` ↓, 우 `CC` ↓),
y = `CAM utilization` [0,1]:

| | 분리막(0 µm) | 집전체(50 µm) |
|---|---:|---:|
| w/o GBs | ≈0.95 | ≈0.84 |
| `R_GB,1` | ≈0.95 | ≈0.84 (파랑과 거의 겹침) |
| `R_GB,2` | ≈0.96 | ≈0.71 |
| `R_GB,3` | ≈0.87 | **≈0.02** |

`[도표]` (b) 3D: 위 `w/o GBs` — 전체가 **빨강(x≈1.0)**, 노란 얼룩 약간. 아래 `R_GB,3` —
분리막 쪽 얇은 층만 빨강, 급격한 **초록 띠**를 지나 나머지 대부분이 **파랑(x≈0.5)**.
컬러바 0.5(파랑) – 1.0(빨강).

`[인쇄, p8]`:
- "In the case of negligible GB resistance …, the majority of CAM voxels has a Li content
  **between 0.9 and 0.98**. Voxels close to the separator are almost completely lithiated.
  On the other hand, **voxels in the center of the particles are closer to a Li content of
  0.9 due to slow diffusion in the CAM**."
- "In the `R_GB,3` case, the histogram shows a large portion of voxels **close to the initial
  Li concentration at the end of the discharge** … A large portion of the CAM close to the
  current collector is **effectively not lithiated and does not contribute to the cell
  capacity**."
- "This effectively **reduces the active thickness of the electrode** resulting in higher
  local reaction currents at the CAM-SE interfaces in the region adjacent to the separator.
  The slow Li diffusion in the CAM leads to **Li accumulation on CAM particle surfaces**
  causing a rapid drop in cell voltage at a higher current (cf. Figure S5)."

`[해석]` ★★★ **이 그림이 이 논문에서 우리에게 가장 중요한 하나다.** 이유:

`R_GB,3` 의 CAM 은 **"죽은 것" 이 아니라 "아직 안 간 것"** 이다. 히스토그램에서 그
집단은 `x ≈ 0.52` — **초기값 그대로** 다. 즉:

- **진짜 `LAM_PE`**(재료 손실)라면 그 CAM 은 **애초에 없다** → 히스토그램에 막대 자체가
  없다.
- **기하적 접촉 손실**(1호의 `1 − θ_AM`)이라면 그 CAM 은 **영원히 `x = 0.52`** 다 — 전자든
  이온이든 도달 경로가 끊겨 있으므로 **시간을 줘도 안 변한다.**
- **동역학적 손실**(이 논문의 `R_GB,3`)이면 그 CAM 은 **시간을 주면 채워진다** — 경로는
  이어져 있고 저항이 클 뿐이다.

→ **셋을 가르는 관측이 존재한다: 전류를 낮추거나(율 스윕), 방전을 멈추고 이완시키는 것
(전압 회복).** 세 번째만 이완에서 전압이 회복되고, 두 번째는 회복되지 않으며, 첫 번째는
애초에 용량 축이 줄어 있다. **이것이 닻의 미결 항목에 대한 이 논문의 최대 기여다.**
(전부 `[해석]` — 논문은 이완 시험도 율 스윕도 하지 않았다.)

### 8.5 SI Fig. S4 — 절대 유효 전도도 ★ 그리고 본문과의 충돌

**Fig. S4 를 직접 봤다.** `[도표]` x = `SVF_LCO / %` [30,80], y = `Conductivity / S cm⁻¹`
(log, 10⁻⁶–10⁰ 넘게). 파란 원 = 이온; 주황 ▲ = 전자(`c_Li,min`); 주황 ▼ = 전자(`c_Li,max`).
고정 `ρ_S = 93.1 %`, `d_CAM = 2.00`, `d_SE = 1.41 µm`.

`[도표]` 읽은 값 (figure-read ≈, S/cm):

| `SVF_LCO` (%) | 33.3 | 40 | 50 | 60 | 69.4 | 80 |
|---|---:|---:|---:|---:|---:|---:|
| **이온** `σ_eff` | ≈2.5e-4 | ≈2.0e-4 | ≈1.2e-4 | ≈5.2e-5 | ≈1.4e-5 | (없음 = 0) |
| 전자 @ `c_Li,min` | ≈0.2 | ≈0.4 | ≈0.75 | ≈1.3 | ≈1.8 | ≈2.6 |
| 전자 @ `c_Li,max` | **≈1.6e-5** | ≈3.0e-5 | ≈5.5e-5 | ≈1.0e-4 | ≈1.4e-4 | ≈2.0e-4 |

`[인쇄, p7]` "It's worth noting that while the effective electrical conductivity in the CAM
phase decreases at low CAM fractions, the **bulk conductivity of LCO is higher than the
ionic conductivity in LLZO**. In fact, **Figure S4 highlights that the effective electronic
conductivity at low SOCs is orders of magnitude higher than the effective ionic
conductivity. Therefore, kinetic limitations are mainly due to ion conduction.**"

`[해석]` ⚠⚠ **어긋남 6 — 이 논문에서 가장 무거운 본문–그림 충돌이다.**
`c_Li,max` = 완전 리튬화 = **방전 끝**(= 셀의 낮은 SOC)이다. 그 상태에서 `[도표]`:
- `SVF_LCO = 33.3 %`: 전자 1.6e-5 **<** 이온 2.5e-4 → **전자가 16 배 낮다.**
- `SVF_LCO = 50 %`: 전자 5.5e-5 **<** 이온 1.2e-4 → 전자가 2 배 낮다.
- `SVF_LCO = 69.4 %`: 전자 1.4e-4 **>** 이온 1.4e-5 → 이제 전자가 10 배 높다.

즉 **교차점이 `SVF ≈ 60 %` 부근에 있고, 그 아래에서는 전자 망이 더 약하다.**
"orders of magnitude higher" 는 `c_Li,min`(방전 시작, 높은 SOC)에서만 참이다.
본문이 "at low SOCs" 라 쓴 것이 만약 "CAM 의 Li 함량이 낮을 때"(= 셀 SOC 는 **높을** 때)를
뜻한다면 용어가 뒤집힌 것이고, 통상 의미대로 읽으면 **그림이 문장을 반증한다.**
그리고 이 문장이 떠받치는 결론("kinetic limitations are mainly due to ion conduction")이
**논문의 저 CAM 분율 최적화 권고 전체의 근거**다.
(⚠ 이 판정은 `[도표]` 기반이다. 원 수치표가 없어 확인할 수 없다.)

**Fig. S7 을 직접 봤다** — 위 판정의 물리적 근거. `[도표]` (a) `σ` vs Li 점유율:
LCO 는 x=0.53 에서 ≈4 S/cm → x→1 에서 **≈5e-3 로 급락**(마지막 0.05 구간에서 거의
수직). NMC 는 x=0.23 에서 9e-3, x≈0.32 최대 2e-2 → x→1 에서 **≈1e-6**.
(b) `D_Li`: LCO 8.5e-12 → 1e-12; NMC 0.9e-12 → **x≈0.9 에서 5e-14 로 절벽**.
(c) `σ_eff` vs `SVF_CAM`: NMC 의 `c_Li,max` 값은 **5e-8 – 8e-7 S/cm** — 유효 이온 전도도보다
**2–4 자릿수 낮다**.

`[해석]` → **NMC 에서는 방전 끝의 율 제한이 전자 쪽에서 온다**는 것이 SI 그림에 있다.
본문은 NMC 절에서 이것을 부분적으로 인정한다(`[인쇄, p13]` "NMC has a **low electrical
conductivity, especially at high lithiation states**") 지만, §8.5 의 "kinetic limitations
are mainly due to ion conduction" 이라는 일반 진술은 **철회되지 않는다.**

### 8.6 SI Fig. S5 — ★★ `assb` 섹션 최초의 전압 곡선

**Fig. S5 를 직접 봤다.** `[도표]` x = `Capacity / mAh/cm²` ∈ [0, 1.5], y = `Voltage / V`
∈ [3.4, 4.2]. 4 곡선. 고정 `SVF_LCO = 50 %`, `ρ_S = 93.1 %`, `d_CAM = 2.00`,
`d_SE = 1.41 µm`, 1 mA/cm².

`[도표]` 읽은 값 (figure-read ≈):

| | 시작 전압 (Q=0) | 3.4 V 도달 용량 |
|---|---:|---:|
| `w/o GBs` | ≈4.155 V | **≈1.37 mAh/cm²** |
| `R_GB,1` | ≈4.135 V | ≈1.36 |
| `R_GB,2` | ≈4.085 V | ≈1.31 |
| `R_GB,3` | **≈3.98 V** | **≈0.385** |

`[도표]` 곡선 모양: `w/o GBs`·`R_GB,1` 은 완만히 내려가다 **≈1.05 mAh/cm² 에서 기울기가
꺾이고** 1.3 부근에서 급락. `R_GB,2` 는 처음부터 더 가파르고 같은 꺾임이 ≈1.2 에서.
`R_GB,3` 은 **처음부터 거의 직선으로 급락**해 0.385 에서 컷오프.

`[재현]` 검산: `SVF 50 %`, `ρ_S 93.1 %`, 두께 50 µm → CAM 부피분율 0.4655 →
면적당 CAM 질량 `50e-4 × 0.4655 × 5.051 = 1.176e-2 g/cm²`.
`C_norm = 0.89` → `0.89 × 129.98 mAh/g × 1.176e-2 g/cm² = **1.360 mAh/cm²**`.
**`[도표]` 의 ≈1.37 과 일치한다.** → 식 (7)(8)·Table 1·Table S4·Fig. 4a·Fig. S5 가
**서로 닫힌 고리로 검증된다.** (이 digest 에서 가장 강한 내적 일관성 검사다.)

`[재현]` **C-rate**: 1.36 mAh/cm² 를 1 mA/cm² 로 빼면 **1.36 h ≈ 0.74 C**.
→ `[해석]` 이 논문의 모든 결과는 **≈0.74 C 방전 1 회**의 결과다. pOCV(보통 ≤ C/20)와
**한 자릿수 이상 떨어진 영역**이다.

`[해석]` ★★★ **우리 물음에 대해 이 그림이 말하는 것 셋:**
1. **겉보기 용량이 3.56 배 차이 난다**(1.37 → 0.385) — **재료·기하가 전부 동일한데.**
   → `LAM_PE` 로 해석하면 **72 % 의 가짜 활물질 손실**이다.
2. **곡선이 수평 스케일링이 아니다.** `R_GB,3` 은 시작 전압부터 175 mV 낮고(IR),
   기울기가 다르며, `w/o GBs` 곡선을 용량축으로 눌러 얹어도 겹치지 않는다.
   → `bms-balancing` 의 **아핀 창 매개화 `(a_PE, b_PE)` 로는 이 곡선을 맞출 수 없다.**
   나쁜 소식이 아니라 **좋은 소식**이다: 아핀 잔차가 이 성분을 **드러낸다.**
3. **그러나 이것은 OCV 곡선이 아니다.** 전 곡선이 1 mA/cm² 부하 아래 있다.
   **`assb` 섹션에는 여전히 OCV 곡선이 0 편이다** (§14 Q8).

### 8.7 소결론 (p9, 인쇄된 불릿 3 개)

`[인쇄]`
- "The electrochemical performance at high CAM fractions is limited by the **effective ionic
  conductivity and isolated electrolyte clusters**."
- "To achieve high CAM utilization at high CAM fractions, the **GB resistance must not
  significantly exceed values measured in dense pellets**."
- "Simulations allow to derive an **optimal electrode composition and thickness** depending
  on transport properties and operation conditions."

`[해석]` ⚠ **어긋남 7**: 세 번째 불릿의 "**and thickness**" — **두께는 이 논문에서 한 번도
변하지 않았다** (50 µm 고정, G5). 두께 스윕은 이 그룹의 선행 논문(ref 31 Finsterbusch
2018)에 있는 것이고 이 논문의 결과가 아니다.

---

## 9. RESULTS — 소결 후 밀도의 영향 (p9–p11)

### 9.1 도입부의 열화 문단 (★ 닻과 직결)

`[인쇄, p9]` "The **sinter density** of the composite cathode describes the **residual
porosity in the structure after manufacturing**. In contrast to a conventional Li-ion battery
with liquid electrolyte, **pores cannot be completely filled by the solid electrolyte** in an
ASSB. … **Small voids at the interface between SE and CAM particles reduce the active surface
area and cause constriction effects**(ref 65)."

`[인쇄, p9]` ★ 그리고 곧바로: "However, it should be noted that **pore formation and contact
loss between individual particles can also result from mechanical degradation due to volume
changes of the CAM during operation**(ref 17). While our current model **does not incorporate
mechanics**, our simulation results provide valuable insights into the impact of increasing
porosity in the overall microstructure on cell performance. However, **specific changes in
the microstructure, such as pore formation during cycling, are beyond the scope of our
current model**."

`[해석]` ★★ **이 문단이 닻 질문의 Q1 에 대한 이 논문의 답 전부다.** 논문은
**"공극률 = 접촉 손실의 대리 변수"** 라는 다리를 스스로 놓고, 동시에 그 다리가
**제조 공극이지 사이클 공극이 아니라**고 못 박는다. 즉:

- 이 논문이 주는 것: **`ρ_S` (소결 밀도) 를 낮추면 겉보기 용량·에너지가 어떻게 되는가**
  의 **정량 지도** — 그리고 그 지도는 `[해석]` "사이클이 만든 공극" 에도 **형태적으로는**
  같은 답을 줄 것이다 (공극이 어디서 왔든 기하는 기하다).
- 이 논문이 안 주는 것: **그 공극이 사이클에 따라 어떻게 늘어나는가** — `θ(N)` 의 시간축.
  1호와 **똑같은 자리**에서 멈춘다 (§15-3).

⚠ 그리고 `[해석]` **형태적으로 같다는 보장이 없다**: 소결 밀도를 낮추면 공극이 **전체에
고르게** 생기지만, 사이클 균열은 **CAM/SE 계면에 우선적으로** 생긴다(ref 65 Eckhardt 2022
가 말하는 constriction). 분포가 다르면 같은 `ρ_S` 에서도 `θ`·`A_act`·`τ` 가 다르다.

### 9.2 Fig. 6 — 밀도 → 연결성

**Fig. 6 을 직접 봤다.** `[도표]` (a) SE phase, (b) CAM phase — 막대그래프, x = `Sinter
density / %` ∈ {60, 70, 80, 90}, y = `Connectivity / %`. 3 색(하늘 `SVF 33.3` · 주황 `50.0` ·
보라 `69.4`). (c) `SVF_LCO = 69.4 %` 의 3D 이미지 3 개(소결밀도 70/80/90 %), **파랑 = SE
connected, 빨강 = SE isolated**, 분리막이 왼쪽·집전체가 오른쪽.

`[도표]` 읽은 값 (figure-read ≈, %):

| 소결밀도 | 60 | 70 | 80 | 90 |
|---|---:|---:|---:|---:|
| (a) SE, `SVF 33.3` | ≈100 | ≈100 | ≈100 | ≈100 |
| (a) SE, `SVF 50.0` | ≈96.5 | ≈98.5 | ≈99.5 | ≈99.8 |
| (a) SE, `SVF 69.4` | **≈37** | ≈74.5 | ≈87 | ≈94 |
| (b) CAM, `SVF 33.3` | **≈84.5** | ≈93.5 | ≈96.5 | ≈98.5 |
| (b) CAM, `SVF 50.0` | ≈99 | ≈99.5 | ≈100 | ≈100 |
| (b) CAM, `SVF 69.4` | ≈100 | ≈100 | ≈100 | ≈100 |

`[도표]` (c) 3D: 70 % 에서 빨간(격리) SE 가 **구조 전체에 촘촘히 박혀 있고 오른쪽(집전체)
으로 갈수록 빽빽**, 90 % 에서는 거의 파랑, 표면에 빨간 점 몇 개.

`[인쇄, p9]` "The share of unconnected clusters **increases with increasing distance from the
separator**. Thus, CAM particles close to the current collector are more likely to show
reduced utilization at low densities and high CAM fractions."

`[해석]` ★ **`θ` 가 공간적으로 균일하지 않다** — 이것은 1호에 없던 관측이다. 1호의
`θ_AM` 은 전극 전체에 대한 스칼라 하나였다. 여기서는 `θ_SE(z)` 가 **분리막에서 멀어질수록
떨어진다.** → 우리 forward model 로 옮길 때 `θ` 를 스칼라로 넣으면 **집전체 쪽 손실을
과소평가**한다.

`[해석]` ⚠ **표현 주의**: (a)(b) 의 y 축이 **0 이 아니라 ≈33 % 에서 시작**한다. 눈으로는
차이가 과장돼 보인다. (실제 SE 연결성 37 % → 94 % 는 충분히 큰 차이이므로 결론은
안 바뀐다.)

### 9.3 Fig. 7 — 밀도 → 굴곡도·활성면적

**Fig. 7 을 직접 봤다.** `[도표]` x = `Sinter density / %` ∈ [60, 93.1], 좌 y =
`Tortuosity τ` (**log**, 1–15, **원 + 점선**), 우 y = `A_act/V_Ca / 1/cm` (0–7500,
**삼각형 + 실선**). 3 색(`SVF` 33.3/50.0/69.4).
`[인쇄, 캡션]` "**Isolated material clusters were removed from the structures before computing
the active area.**" (⚠ 캡션이 `ρ_S = 93.1 %` 도 "constant" 라고 적는데, 이 그림의 x 축이
바로 밀도다 — 상투 문구 복사, §13 불일치 10.)

`[도표]` 읽은 값 (figure-read ≈):

| 소결밀도 | 60 | 70 | 80 | 90 | 93.1 |
|---|---:|---:|---:|---:|---:|
| `τ_SE`, `SVF 33.3` | ≈1.45 | ≈1.28 | ≈1.18 | ≈1.11 | ≈1.10 |
| `τ_SE`, `SVF 50.0` | ≈2.55 | ≈1.75 | ≈1.50 | ≈1.35 | ≈1.30 |
| `τ_SE`, `SVF 69.4` | (축 위, >15) | **≈10.8** | ≈6.0 | ≈4.7 | ≈3.4 |
| `A_act/V_Ca`, `SVF 33.3` | ≈1080 | ≈2050 | ≈3350 | ≈4700 | ≈5050 |
| `A_act/V_Ca`, `SVF 50.0` | ≈1150 | ≈2700 | ≈4100 | ≈5750 | **≈6150** |
| `A_act/V_Ca`, `SVF 69.4` | ≈450 | ≈1400 | ≈2950 | ≈4650 | ≈5050 |

`[인쇄, p9–p10]`
- "we observe an **exponential increase of tortuosity with decreasing density**."
- "**Even at the maximum density (93.1 %) the configuration with high CAM fraction shows
  higher tortuosity than compositions with elevated LLZO content and low sinter density.**"
- "The structure with `SVF_LCO = 50 %` shows the **highest active area** since a similar share
  of SE particles is in direct contact with the CAM. We observe **almost linear dependence of
  the surface area on density after sintering**."
- "the **effect of cathode composition on active area is minor compared to the significant
  effect on tortuosity** at low densities."

`[해석]` ✔ 그림이 본문을 지지한다 (`τ(69.4 %, 93.1 %) ≈ 3.4 > τ(50 %, 60 %) ≈ 2.55`).
`[해석]` ⚠ **어긋남 8**: 같은 구조(`SVF 50 %`, `ρ_S 93.1 %`, `d_CAM 2.0`, `d_SE 1.41`)의
활성면적이 **Fig. 7 에서 ≈6150 1/cm, Fig. 9a 에서 ≈5300 1/cm** 로 읽힌다 (둘 다 `[도표]`,
Fig. 9a 는 컬러바 보간이라 오차가 더 크다). Fig. 7 은 격리 클러스터를 **제거하고** 계산했고
Fig. 9 는 그 언급이 없다 — 그런데 제거하면 면적은 **줄어야** 한다. 방향이 반대다.
⚠ 두 값 모두 figure-read 이므로 **판정은 유보**하고, 두 그림의 활성면적 정의가 같은지
확인이 필요하다고만 적는다.

### 9.4 Fig. 8 — 밀도 → 용량·공간분포·에너지 ★

**Fig. 8 을 직접 봤다.** 3×3 패널. 열 = `SVF_LCO` 33.3 / 50.0 / 69.4 %.
- (a) 막대: x = `Sinter density / %` {60,70,80,90,93}, y = `Normalized capacity` [0,1],
  **연한 색 = w/o GBs, 진한 색 = w/ GBs**(`R_GB,3 = 3.6 Ω cm²`).
- (b) 선: x = `Cathode length / µm` [0,50], y = `CAM utilization` [0,1], 5 색 = 밀도
  {60, 70, 80, 90, 93.1 %}, **w/o GBs 경우만**.
- (c) 막대: 같은 x, y = `Energy density / Wh/kg_cell` [0, ~180].

`[도표]` (a) 정규화 용량 (figure-read ≈):

| | 60 | 70 | 80 | 90 | 93 |
|---|---:|---:|---:|---:|---:|
| `SVF 33.3` w/o | ≈0.435 | ≈0.695 | ≈0.81 | ≈0.87 | ≈0.88 |
| `SVF 33.3` w/ | ≈0.025 | ≈0.21 | ≈0.285 | ≈0.465 | **≈0.54** |
| `SVF 50.0` w/o | ≈0.585 | ≈0.75 | ≈0.83 | ≈0.88 | **≈0.89** |
| `SVF 50.0` w/ | ≈0.012 | ≈0.048 | ≈0.14 | ≈0.205 | ≈0.25 |
| `SVF 69.4` w/o | ≈0.008 | ≈0.10 | ≈0.54 | ≈0.775 | ≈0.80 |
| `SVF 69.4` w/ | ≈0.005 | ≈0.005 | ≈0.015 | ≈0.033 | ≈0.042 |

`[도표]` (b) CAM 이용률 프로파일 (분리막 → 집전체):
- `SVF 33.3`: 전 밀도에서 **거의 평평**. 93.1 % ≈0.88 평탄, 60 % ≈0.40→0.53(오히려 약간
  상승, 잡음 큼).
- `SVF 50.0`: 93.1 % ≈0.89 평탄; 60 % ≈0.60 에서 시작해 47 µm 부터 0.40 으로 급락.
- `SVF 69.4`: 93.1 % ≈0.95→0.62 로 완만히 하강; **80 % 는 0.95→0.28**; **70 % 는 5 µm 만에
  0.3 아래로, 20 µm 부터 ≈0**; **60 % 는 1 µm 만에 ≈0.02**.

`[도표]` (c) 에너지밀도 (Wh/kg_cell):

| | 60 | 70 | 80 | 90 | 93 |
|---|---:|---:|---:|---:|---:|
| `SVF 33.3` w/o | ≈38 | ≈66 | ≈81 | ≈90 | ≈93 |
| `SVF 33.3` w/ | ≈1.5 | ≈19 | ≈30.5 | ≈46 | **≈54** |
| `SVF 50.0` w/o | ≈78 | ≈110 | ≈127 | ≈139 | ≈141 |
| `SVF 50.0` w/ | ≈2 | ≈7 | ≈22 | ≈33 | ≈37 |
| `SVF 69.4` w/o | ≈1.5 | ≈19 | ≈109 | ≈166 | **≈174** |
| `SVF 69.4` w/ | ≈1 | ≈1.5 | ≈3 | ≈7 | ≈8.5 |

`[인쇄, p10–p11]`
- "For the scenario with negligible GB resistance, the structure with `SVF_LCO = 50 %`
  provides the **highest capacity for all densities**. This indicates that the **optimal
  cathode composition does not significantly depend on density after sintering**."
- "In electrodes with high CAM content **even a moderate increase in porosity is not
  tolerable** resulting in almost negligible capacity."
- "At low grain boundary resistance, energy density is **maximum for `SVF_LCO = 69.4 %` at
  densities above 90 %**. However, **at 80 % density, cathodes with `SVF_LCO = 50 %` already
  outperform** those with 69.4 %."
- "At high grain boundary resistance, the maximum energy density is observed for the structure
  with **`SVF_LCO = 33.3 %` across all densities**."

`[해석]` ✔ 네 문장 모두 `[도표]` 와 맞는다 (127 vs 109 @80 %; 166/174 vs 139/141 @≥90 %;
54 vs 37 vs 8.5).

`[해석]` ★ **우리에게 중요한 것은 (b) 다.** `SVF 69.4 %` 열에서 밀도 70 % 곡선은
**전극의 90 % 가 이용률 ≈0** 이다. 그 CAM 은 **물질로는 다 있고 전자망에도 붙어 있는데**
(Fig. 6b 에서 CAM 연결성 ≈100 %) **이온이 못 간다.** 겉보기로는 `LAM_PE ≈ 90 %` 다.
→ **`Connectivity_CAM = 100 %` 인데 `C_norm = 0.10`.** 즉 `[해석]`
**`θ_AM` 하나로는 겉보기 용량을 설명할 수 없다**는 것이 이 논문 안에서 반례로 증명된다.
1호의 `Q_apparent = θ_AM · Q_material` 은 **필요조건일 뿐 충분조건이 아니다** (§15-2).

---

## 10. RESULTS — SE·CAM 입자 크기의 영향 (p11–p12)

### 10.1 Fig. 9 — 기하 (활성면적·굴곡도)

**Fig. 9 를 직접 봤다.** `[도표]` 두 패널 모두 x = `Mean particle diameter LLZO / µm`
[0.5, 3.5], y = `Mean particle diameter LCO / µm` [0, 8], 점 8 개, 색 = 값.
(a) 컬러바 `A_act/V_ca / 1/cm` (3000–9000). (b) 컬러바 **`1/Tortuosity`** (0.45–0.65).
고정 `SVF_LCO = 50 %`, `ρ_S = 93.1 %`. **화살표 2 개**(`d_CAM` 수직, `d_SE` 수평)가
최적 방향을 가리킨다.

`[도표]` 8 개 점 읽은 값 (figure-read ≈, 컬러바 보간이라 오차가 크다):

| (`d_SE`, `d_CAM`) µm | (0.7, 2.0) | (1.41, 0.8) | (1.41, 2.0) | (1.41, 3.0) | (1.41, 3.5) | (1.41, 8.0) | (3.0, 2.0) | (3.5, 2.0) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) `A_act/V_ca` (1/cm) | **≈9000** | ≈8800 | ≈5300 | ≈4200 | ≈4100 | ≈2900 | ≈3400 | ≈3300 |
| (b) `1/τ_SE` | ≈0.615 | **≈0.52** | ≈0.585 | ≈0.63 | ≈0.63 | **≈0.645** | ≈0.46 | ≈0.50 |

`[인쇄, p11]`
- "A **maximum contact area** between SE and CAM can be achieved for the combination of
  **small SE and CAM particle diameters**."
- "However, at constant SE particle size, **small CAM particles cause tortuous pathways in
  the SE** due to the higher number of particles and thus, obstacles"(ref 23).
- "**Low tortuosities are realized by small SE particles and moderate or large CAM particle
  size.**"
- "the **particle size ratio `λ = d_CAM/d_SE`** is an important parameter … To achieve short
  ionic pathways and good connectivity, **SE particles must be smaller than CAM particles**
  (ref 24, 35). As λ increases, **channels form between larger CAM particles that can be
  occupied by smaller SE particles**. However, large CAM particles result in **long diffusion
  pathways in the active material**. Additionally, **small SE particles increase the GB
  resistance**."

`[해석]` ✔ 그림이 본문과 맞는다 (활성면적 최대 = 좌하단; 1/τ 최대 = `d_CAM` 큰 쪽).
`[해석]` ⚠ **어긋남 9 (캡션)**: 캡션은 "(b) **Tortuosity** in the SE phase" 라고 쓰는데
컬러바는 **`1/Tortuosity`** 다. 부호를 반대로 읽으면 결론이 뒤집힌다.
`[해석]` ★ 이 그림은 1호의 `p_c(d)` 논지와 **정반대 방향의 축**을 다룬다: 1호는
**작은 AM 입자가 전자 퍼콜레이션에 유리**하다고 했고(무탄소·전자망), 2호는
**작은 CAM 입자가 SE 굴곡도를 나쁘게 한다**(이온망)고 한다. **둘 다 맞고, 최적은 둘의
절충**이다. 1호는 이온망의 대가를 안 쟀고, 2호는 전자망을 LCO 의 높은 `σ` 덕에 거의
무시한다.

### 10.2 Fig. 10 — 입자 크기 → 정규화 용량 (GB 3 경우) ★

**Fig. 10 을 직접 봤다.** `[도표]` 3 패널(`R_GB,1` → `R_GB,2` → `R_GB,3`, 아래 굵은
화살표 "`R_GB ↑`"), 각각 x = `d_LLZO / µm` [0.5,3.5], y = `d_LCO / µm` [0,8], 점 8 개,
**공통 컬러바 = `Normalized capacity` [0,1]**. `[인쇄, 캡션]` "For each simulation case the
**three highest capacities are highlighted with red circles**." 고정 `SVF_LCO = 50 %`,
`ρ_S = 93.1 %`, 1 mA/cm².

`[인쇄, 그림 안 숫자]` 상위 3 개:

| | 1 위 | 2 위 | 3 위 |
|---|---|---|---|
| `R_GB,1` | **0.94** @ (`d_SE` 0.7, `d_CAM` 2.0) | **0.93** @ (1.41, 0.8) | **0.89** @ (1.41, 2.0) |
| `R_GB,2` | **0.82** @ (0.7, 2.0) | **0.81** @ (1.41, 3.0) | **0.79** @ (1.41, 2.0) |
| `R_GB,3` | **0.23** @ (**3.5**, 2.0) | **0.22** @ (1.41, 3.5) | **0.20** @ (1.41, 3.0) |

`[도표]` 나머지 점들: `R_GB,1` 은 전부 주황~노랑(0.8 이상), `R_GB,2` 는 (1.41, 8.0)·(3.0, 2.0)·
(3.5, 2.0) 가 초록(≈0.6), `R_GB,3` 은 **8 개 전부 파랑(≤0.25)**.

`[인쇄, p12]`
- "In case of a **small GB resistance, structures with both small CAM and SE particles
  provide the best** electrochemical performance … the **short diffusion length in the CAM**
  enables high utilization … The increased tortuosity resulting from small CAM particles
  **does not significantly impact cell performance since ion transport is not limiting**."
- "In the `R_GB,2` case maximum capacities are achieved with small SE particles and moderate
  CAM diameters (**`d_SE = 0.8 µm` and `d_CAM = 2.0 µm`**)."
- "In the `R_GB,3` case … the structure with **larger LLZO particles (`d_SE = 3.5 µm`,
  `d_CAM = 2.0 µm`) performs slightly better** … This indicates an **upper limit of a
  tolerable GB resistance between `R_GB,2` and `R_GB,3`** which is a **strict requirement**
  to be met in process development."

`[해석]` ⚠ **어긋남 10**: 본문의 "`d_SE = 0.8 µm`" 인 구조는 **없다.** Table S2 의
`d^Init_LLZO` 는 {0.70, 1.41, 3.00, 3.50} 뿐이고, 0.80 µm 는 **LCO** 쪽 값이다
(`d^Init_LCO = 0.80`). 그림의 `R_GB,2` 1 위는 `(d_SE = 0.7, d_CAM = 2.0)` 이므로
**0.8 은 0.7 의 오기**로 보인다. (혹은 `d_SE`/`d_CAM` 을 맞바꿔 쓴 것.)

`[해석]` ★★ **이 그림의 진짜 메시지는 "최적이 이동한다" 가 아니라 "최적이 사라진다" 다.**
`R_GB,3` 에서 8 개 전부 0.20–0.25 다 — 즉 **입자 크기 최적화의 효과가 `R_GB` 앞에서
무의미해진다.** 그리고 `R_GB,1`(0.94)과 `R_GB,3`(0.23) 사이가 **4.1 배**이므로,
**입자 크기 축(최대 0.94 vs 0.89, 5 %p)보다 GB 저항 축이 압도적으로 크다.**
→ `[해석]` 이 논문이 자기 제목("Optimizing the … Microstructure")이 말하는 것보다
**공정(GB 저항)의 지배력이 더 크다**는 결론을 스스로 내고 있다.

`[해석]` ⚠ **어긋남 11 (캡션)**: 캡션은 "Influence of the grain boundary resistance on the
**gravimetric capacity**" 인데 컬러바와 본문은 **normalized capacity** 다. (값이 0–1 이므로
컬러바가 맞다.) Fig. 11b 캡션도 같은 오류를 반복한다.

`[해석]` ⚠ **G2 재확인**: 최상위 3 개의 차이가 0.94/0.93/0.89 인데 **구조 실현이 점당
1 개**다. 1호가 같은 계열 모델에서 실현 간 `θ` 가 ≈40 %p 벌어진다고 인쇄한 것을 생각하면
**0.94 와 0.89 의 순위를 신뢰할 근거가 이 논문 안에 없다.**

---

## 11. RESULTS — CAM 물성 (LCO vs NMC811) (p12–p14)

### 11.1 Fig. 11a — 조성 스캔에서의 두 물질

**Fig. 11 을 직접 봤다.** `[도표]` (a) x = `SVF_CAM / %` [30, 80], 좌 y = `Norm. capacity / %`
[30,100], 우 y = `Grav. capacity / mAh/g_CAM` [0,200]. 4 계열: LCO 정규화(파란 원·실선),
NMC 정규화(주황 원·실선), LCO 중량(파란 네모·점선), NMC 중량(주황 네모·점선).
고정 `ρ_S = 93.1 %`, `d_CAM = 2.00`, `d_SE = 1.41 µm`, 1 mA/cm², **GB 무시**.

`[도표]` 읽은 값 (figure-read ≈):

| `SVF_CAM` (%) | 33.3 | 40 | 50 | 60 | 69.4 | 80 |
|---|---:|---:|---:|---:|---:|---:|
| Norm. LCO (%) | ≈88 | **≈90** | ≈89.5 | ≈87.5 | ≈80 | ≈2 |
| Norm. NMC (%) | ≈74.5 | ≈82 | **≈85** | ≈83 | ≈73.5 | ≈2 |
| Grav. LCO (mAh/g) | ≈115 | ≈117 | ≈116.5 | ≈114 | ≈104 | ≈3 |
| Grav. NMC (mAh/g) | ≈148 | ≈164 | **≈170** | ≈166 | ≈147 | ≈4 |

`[인쇄, p13]` "For all generated structures, the simulations with LCO show a **better CAM
utilization** due to the superior Li diffusivity and electrical conductivity … However,
despite the low chemical diffusion coefficient and poor electrical conductivity … the
**more relevant gravimetric capacity is still higher for NMC** cathodes. These results
indicate that research on LLZO-based cell designs should **aim at integrating NMC811**."

`[재현]` 본문의 "**172 mAh/g and 116 mAh/g for NMC811 and LCO**" ↔ `[도표]` ≈170 과 ≈116.5.
✔ 일치. 그리고 `116.3 = 0.895 × 129.98` (§6.2) — **내적 일관.**

`[해석]` ⚠ 그림 읽기 함정 하나: NMC 의 정규화 곡선과 중량 곡선이 **거의 겹쳐 보인다.**
이유는 `[재현]` `C^theo(NMC) ≈ 204.6 mAh/g` 이고 우축 최대가 200 mAh/g 이라서 —
정규화 85 % 와 중량 170 mAh/g 이 **같은 높이**에 찍힌다. 우연한 축 스케일이다.

### 11.2 Fig. 11b — NMC 의 입자 크기 지도

`[인쇄, 그림 안 숫자]` 상위 3 개 (`SVF_NMC = 50 %`, `ρ_S = 93.1 %`):

| | 1 위 | 2 위 | 3 위 |
|---|---|---|---|
| `R_GB,1` | **0.90** @ (`d_SE` 1.41, `d_CAM` 0.8) | **0.89** @ (0.7, 2.0) | **0.85** @ (1.41, 2.0) |
| `R_GB,2` | **0.65** @ (0.7, 2.0) | **0.65** @ (1.41, 3.0) | **0.63** @ (1.41, 3.5) |

`[인쇄, p14]` "compared to the simulations with LCO, normalized capacities are significantly
lower, especially for the `R_GB,2` case. The maximum normalized capacity is **around 65 %
which corresponds to a specific capacity of around 133 mAh/g**. Note that the capacity gain
in comparison to the values of LCO (**106 mAh/g**) for the same electrolyte parameters is
significantly lower than in case of negligible GB resistance, where capacities are at
**172 mAh/g and 116 mAh/g** for NMC811 and LCO."

`[재현]` `133/0.65 = 204.6 mAh/g = C^theo(NMC)` ✔ (G4 의 역산 근거).
`[재현]` LCO `R_GB,2` 최고 = 0.82 (Fig. 10) → `0.82 × 129.98 = 106.6 mAh/g` ↔ 본문의
**106 mAh/g** ✔. **Fig. 10 · Fig. 11b · 본문 · Table 1 · 식 (8) 이 서로 닫힌다.**

`[재현]` **GB 저항이 NMC 의 이점을 깎는 정도**:
무시 시 `172/116 = 1.48 배`; `R_GB,2` 에서 `133/106 = 1.25 배`.
→ `[해석]` **NMC 로 바꿔 얻는 이득의 절반 가까이를 GB 저항이 먹는다.**

`[인쇄, p14]` 처방: "reducing the CAM and SE particle size, using **single-crystal NMC**, and
**adding conducting additives**"(ref 17, 71).

`[해석]` ⚠ **어긋남 12**: 마지막 처방("도전재 첨가")은 **이 논문의 모델에 없는 상(相)**
이다 — 2 성분(CAM+SE)+공극 구조에 탄소가 없다. 1호가 탄소를 뺀 이유(황화물 분해)와 달리
이 논문은 **탄소를 뺀 이유를 한 번도 적지 않고**, 결론에서는 그것을 추천한다.

---

## 12. Conclusions and Outlook (p14)

`[인쇄]` 요지:
1. 모델의 특징: 질량·전하 보존식 + **SE 입계 수송 저항 모형**. "By using input geometries
   that feature **realistic morphologies**."
2. `[인쇄]` ★ "**To validate the results of our computational studies, it is important to
   perform corresponding experiments.** As an initial step, **impedance measurements for
   LCO/LLZO composite cathodes** could be conducted to determine the ionic and electronic
   **partial conductivities**, similar to the approach used for thiophosphate electrolyte in
   a previous study(ref 22). Furthermore, more emphasis should be placed on conducting such
   measurements for **different particle sizes and densities**."
3. 결과 요약: **중간 CAM 분율**에서 최대 용량. 낮으면 전자 전도도, 높으면 격리 클러스터와
   굴곡도.
4. 처방: **농도 구배 양극**(분리막 쪽 SE ↑, 집전체 쪽 CAM ↑, ref 72, 73), **GB 저항 저감**,
   **FAST/SPS 등 신공정으로 밀도 ↑**(ref 67).
5. NMC: 에너지밀도 잠재력은 있으나 이온·전자 수송이 도전. **단결정 NMC·도전재**.
6. `[인쇄]` ★ "we believe that **coupling electrochemical and mechanical models is essential**
   for optimizing the composite cathode. This approach takes into account **mechanical stress
   resulting from volume changes of the active material** and could **potentially alter
   optimal cathode designs**."

`[해석]` 6 번이 **닻의 다음 논문을 지정한다.** 저자들 스스로 "역학 결합이 필수" 라고
적었고, 그 역학이 바로 우리가 찾는 **`θ(N)` 의 시간축**이다. `assb` 3 호 후보 1 순위.

`[해석]` 2 번도 중요하다: **자기 재료계(LCO/LLZO)에 대한 부분 전도도 측정이 존재하지
않는다**고 논문이 명시했다. 이것이 1호의 "아무도 공극률을 안 잰다" 와 같은 형식의
**"모두가 빠뜨린 측정" 원장** 항목이다 (§16-6).

---

## 13. 본문 · 그림 · 캡션 어긋남 원장

| # | 자리 | 어긋남 | 무게 |
|---|---|---|---|
| **1** | 본문 p7 ↔ Fig. S4 | "effective electronic conductivity at low SOCs is **orders of magnitude higher** than the effective ionic" — `[도표]` `c_Li,max` 에서 `SVF ≤ 60 %` 는 **전자가 더 낮다**(33.3 %: 1.6e-5 vs 2.5e-4). 이 문장이 "kinetic limitations are mainly due to ion conduction" 을 떠받친다. | **큼** |
| **2** | 본문 p6 ↔ Fig. 3 | "limiting material fraction is around **20 vol.% for both**" — **CAM 쪽에 시뮬레이션된 점이 없다**(최저 33.3 %). 안내선의 함수 형태 미기재. | **큼** |
| **3** | 본문 p8 ↔ Fig. 4a | "the virtual structure with **`SVF_LCO = 30 %`** performs best" — 30 % 구조가 없다. 33.3 % 는 **격자 경계**이지 최적이 아니다. | 중 |
| **4** | 소결론 p9 ↔ 방법 | "Simulations allow to derive an optimal electrode composition **and thickness**" — **두께는 50 µm 고정**, 스윕 0 회. | 중 |
| **5** | 본문 p12 ↔ Table S2/Fig. 10 | "`d_SE = 0.8 µm`" — 그런 SE 구조가 없다(0.70·1.41·3.00·3.50). 0.80 은 **LCO** 쪽 값. | 중 |
| **6** | Fig. 7 캡션 ↔ Fig. 9 | Fig. 7 은 활성면적을 "격리 클러스터 제거 후" 계산, Fig. 9 는 언급 없음 → **두 그림의 활성면적 정의가 같은지 불명.** `[도표]` 로는 같은 구조가 ≈6150 vs ≈5300 1/cm. | 중(유보) |
| **7** | 본문 p7 | "simulated conductivities are **slightly** higher" — 임계 근방에서 **약 10 배**. | 중 |
| **8** | 식 (6) | `τ = sqrt(σ/σ_eff)·ε` — 통상 정의(`τ² = ε σ/σ_eff`)와 `ε` 의 위치가 다르다. 인쇄대로면 `ε→0` 에서 `τ→0`. | 중(조판 의심) |
| **9** | 식 (1) · Table S3 | BV 지수에 **`F` 가 없다**(`Δϕ/2RT`). G8 의 재현은 `F` 가 있어야 맞는다. Table S3 마지막 줄 `i_SE-SE = i₀^GB + i^GB_DL` 은 `i_GB + i^GB_DL` 의 오식으로 보인다. | 중(조판) |
| **10** | Fig. 2 캡션 | "…tortuosity of **the electrolyte network**" 인데 그림은 두 상 모두. 그리고 "The discharge simulations were conducted at 1 mA/cm²" 인데 **이 그림에 방전이 없다**(순수 기하). Fig. 7 캡션도 `ρ_S = 93.1 %` 를 "constant" 라 하는데 x 축이 밀도다. | 작음(상투 문구) |
| **11** | Fig. 10 · 11b 캡션 | "**gravimetric** capacity" ↔ 컬러바·본문 "**normalized** capacity". | 작음 |
| **12** | Fig. 9 캡션 | "(b) **Tortuosity**" ↔ 컬러바 "**1/Tortuosity**". 부호 반대. | 작음 |
| **13** | 본문 p4 ↔ p7 | `R_GB = **3.7** Ω cm²`(Methods, `i₀=6.91e-3`) ↔ `R_GB,3 = **3.6** Ω cm²`(Results, `i₀=7e-3`). "Ref. [38] 이 보고한 값" 이라는 서술과 어긋난다. | 작음 |
| **14** | 결론 p14 | "adding **conducting additives**" 를 처방하는데 모델에 **도전재 상(相)이 없다.** 탄소를 뺀 이유도 한 번도 적히지 않는다. | 작음 |

`[해석]` **1호(어긋남 8 건) 대비 14 건이지만 성격이 다르다.** 1호의 최악은
**"계산된 적 없는 양을 초록이 결과로 말한 것"** 이었다. 2호의 초록은 그런 짓을 하지
않는다 — 대신 **본문 서술이 자기 SI 그림과 충돌**하고(1), **격자 밖을 결론으로
말한다**(2·3·4). 그리고 **조판 오류가 눈에 띄게 많다**(8·9·10·11·12) — 식을 코드로
옮기려면 전부 걸린다.

---

## 14. 닻 질문 Q1–Q8 (`questions/assb-contact-loss-vs-lampe.md` 의 수집 지침)

| # | 물음 | 이 논문의 답 |
|---|---|---|
| **Q1** | 접촉 손실을 어떻게 정량했나 — 단위·측정법·모델 형태 | **부분.** 세 층으로 갈린다. (i) **기하**: `Connectivity = 1 − n_iso/n_tot` (식 4, 무차원) — **1호의 `θ` 와 같은 양**(§7.3). (ii) **제조 공극**: `sinter density ρ_S` (= `1 − φ`) 를 60–93.1 % 로 스윕 → 겉보기 용량 지도(Fig. 8). (iii) **계면 저항**: `R_GB` 0.036–3.6 Ω cm² → 겉보기 용량 0.89 → 0.25. **그러나 "사이클이 만드는 접촉 손실" 은 명시적으로 범위 밖**(G13). |
| **Q2** | 접촉 손실과 LAM 을 가르는 **독립 관측**을 썼나 | **부분, 그러나 약하다.** 자기 실험 **0 개**. 유일한 대조는 Fig. 3 의 Minnmann et al.(ref 22) 유효 부분 전도도인데 **재료계가 다르다**(NMC622/Li₆PS₅Cl vs LCO/LLZO, G10). 논문 스스로 `[인쇄]` "LLZO 기반 복합전극의 계통적 전도도 측정은 문헌에 없다" 고 적는다. → **제안된 독립 관측은 "복합양극 EIS 의 부분 전도도"** 이고 그것이 결론의 첫 제안이다(§12-2). |
| **Q3** | 라벨 출처 층위 — measured / fitted / 가정, 오차 막대 | **전부 computed.** 기하량은 computed-geometric, 용량·에너지는 computed-electrochemical. 재료 파라미터는 **전부 문헌 인용**(Table 1·2). **오차 막대 0 개, 구조 실현 1 개/점, 반복 0 회**(G2). `fit` 0 회. |
| **Q4** | 유일성·식별성을 쟀나 (조건수·근최적 폭·프로파일) | **없다.** 순수 forward. `inverse` 2 회는 전부 "1/tortuosity" 의 inverse. 역문제·조건수·신뢰구간 **0 회**. → **`assb` 2/2 편이 안 쟀다** (액체셀 17/17 과 같은 형식). |
| **Q5** | Li-In 기준 전위 이동을 다뤘나 | **없다.** `indium` **0 회**. 음극은 **Li 금속** 이고 `U^AN_0 = 0 V` 고정, `[인쇄]` "assumed to be in **ideal contact**". |
| **Q6** | 압력을 통제·보고했나 | **없다.** `pressure` **0 회**, `stack` **0 회**. ★ **`assb` 2/2 편이 압력을 0 회 언급했다.** (다만 `sinter density` 와 FAST/SPS 언급이 **제조 압력의 간접 대리**이긴 하다 — 작동 중 스택 압력과는 다른 축.) |
| **Q7** | 무음극이면 dead Li 와 SEI Li 를 갈랐나 | **없다.** 무음극이 아니라 **Li 금속**이고, 그마저 이상 접촉·무열화로 가정. `dead` 0 회. |
| **Q8** | 양극 화학과 OCP 기울기 | **★ 있다 — `assb` 섹션 최초.** **LCO**(`U₀ = 4.2 V` 초기, 농도 의존 함수형, ref 56 Landstorfer 2011) 와 **NMC811**(ref 36 Bielefeld 2022), 컷오프 **3.4 V**, 작동 구간 `x ∈ [0.525, 1]`(LCO) / `[0.231, 1]`(NMC). ⚠ **OCP 곡선 자체는 어느 그림에도 그려져 있지 않다** — 함수 파라미터로만 들어간다. 그리고 Fig. S5 의 전압 곡선은 **1 mA/cm² 부하 곡선이지 OCV 가 아니다.** |

### 채움표 갱신 (닻 페이지에 반영)

| 논문 | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 |
|---|---|---|---|---|---|---|---|---|
| Bielefeld 2019 (1호) | 부분 (`θ`) | **없다** | computed-geometric | **없다** | 없다 | **없다** | 없다 | 부분 |
| **Clausnitzer 2023 (2호)** | **부분** (`Connectivity`+`ρ_S`+`R_GB`) | **부분** (타 재료계 EIS) | computed × 2, **오차막대 0** | **없다** | **없다** | **없다** | **없다** | **있다** (LCO·NMC811, OCP 함수형, 3.4 V 컷오프) |

`[해석]` **이 논문 단독으로는 8 칸 중 ≈2.5 칸.** 2 편 누적 합집합도 **≈2.5/8** 이다
(2호가 1호를 대부분 포함한다). **Q4·Q5·Q6·Q7 은 여전히 0 편** — 특히 **Q6(압력)은 2/2 편이
`pressure` 0 회**이고, **Q4(유일성)는 두 논문 모두 forward 전용**이라 원리적으로 못 채운다.
→ **역문제를 다루는 논문이 `assb` 축에 반드시 한 편 들어와야 한다.**

---

## 15. ★ 1호(Bielefeld 2019)와의 정면 대조

### 15-1. 같은 양인가 — **그렇다, 변환 불필요**

| 개념 | 1호 기호 | 2호 기호 | 변환 |
|---|---|---|---|
| 조성 (고상 기준) | `g^S_AM` | **`SVF_CAM`** | **동일** |
| 조성 (전체 부피 기준) | `g^V_AM` | (안 씀) | `g^V = SVF × ρ_S` |
| 공극 | `φ` (공극률) | **`ρ_S`** (소결 밀도) | `ρ_S = 1 − φ` |
| **이용률 / 연결성** | **`θ = V_c/V_ν`** (식 6) | **`Connectivity = 1 − n_iso/n_tot`** (식 4) | **동일** (§7.3) |
| 활성 계면적 | `A_spec,a` [m²/m³] | `A_act/V_ca` [1/cm] | `1 m²/m³ = 10⁻² 1/cm` |
| 굴곡도 | (없음) | `τ` (식 6) | — |
| 유효 전도도 | **(계산 안 함)** | `σ_eff` [S/cm] (식 5) | — |
| 용량·전압 | **(없음)** | `C_norm`·`C_grav`·`E_grav`·`V(Q)` | — |

`[해석]` → **두 논문의 숫자를 직접 견줄 수 있다.** 예: 1호가 5 µm AM·공극률 20 % 에서
`θ_AM` 이 48–52 vol% 사이에 전이한다고 했고, 2호는 `SVF_LCO = 80 %`(= `g^V ≈ 74.5 %`)
에서 **SE 연결성**이 붕괴한다고 한다 — 서로 **다른 상(相)의 임계**이므로 모순이 아니다.
⚠ 단 §4.2 의 이유로 **1호의 닫힌 형태(식 7·8)는 2호 구조에 적용 불가**다 (입도분포·형상이
전혀 다르다).

### 15-2. ★★ 1호의 `Q_apparent = θ_AM · Q_material` 은 **충분하지 않다**

이 논문이 **반례를 준다** (§9.4):

> `SVF_LCO = 69.4 %`, 소결 밀도 70 %, GB 무시 → `[도표]` **CAM 연결성 ≈100 %**
> (Fig. 6b) 인데 **정규화 용량 ≈0.10** (Fig. 8a).

즉 **모든 CAM 이 집전체에 전기적으로 연결돼 있는데도 90 % 가 안 쓰인다.**
원인은 `θ_AM` 이 아니라 **SE 쪽 굴곡도·격리(`τ_SE ≈ 10.8`, `θ_SE ≈ 74.5 %`)와 전류**다.
→ **최소한 세 항이 곱해진다:**

```
Q_apparent  =  θ_AM(기하)  ·  η(i ; θ_SE, τ_SE, R_GB, D_CAM, σ_CAM)  ·  Q_material
                 ↑ 율 무관                ↑ 율 의존 (i→0 에서 → 1)        ↑ 진짜 LAM_PE
```

(`[해석]` — 이 분해는 우리 것이고 논문의 식이 아니다. 그리고 **G1 때문에 이 논문의
`C_norm` 이 `θ_AM·η` 인지 `η` 만인지 확정할 수 없다.**)

### 15-3. 동역학(`θ` 의 시간 변화)은 **여전히 0 편**

| | 1호 | 2호 |
|---|---|---|
| `θ` 의 사이클 의존 | **없음** (pristine 정적 기하) | **없음** — `[인쇄]` "pore formation during cycling … beyond the scope" |
| 역학 결합 | 없음 | **없음** — `[인쇄]` "our current model does not incorporate mechanics" |
| 사이클 횟수 | 0 | **0** (방전 **1 회**) |

`[해석]` ★ **닻의 "아직 모르는 것 1" 의 두 번째 절반(동역학)은 2 편을 읽고도 비어 있다.**
다만 2호가 **대리 축을 하나 줬다**: `ρ_S` 를 낮추는 것이 "공극이 늘어난 상태" 이므로,
**`ρ_S` 스윕을 시간축으로 가정하면** 열화 궤적의 **후보 경로**가 된다 (Fig. 8 이 그
지도다). ⚠ 단 §9.1 의 이유로 공극의 **분포**가 다를 수 있다.

### 15-4. 무엇이 새로 들어왔나 — 한 줄 요약

| 축 | 1호 | 2호 |
|---|---|---|
| **전압축** | **없음** | **★ 있음** (`U₀ 4.2 V`, `U_cut 3.4 V`, Fig. S5 `V`–`Q` 곡선, `Wh/kg_cell`) |
| **동역학(시간축)** | 없음 | **없음** (방전 1 회, 사이클 0) |
| **시드 산포** | **인쇄됨** (`θ` ≈30↔70 % 이봉; `A_spec` σ ≈±32 %) | **없음** (점당 구조 1 개, 오차 막대 0) |
| 유효 전도도 [S/cm] | 계산 0 회 | **★ 계산함** (Fig. 3·S4) |
| 굴곡도 | 없음 | **★ 있음** |
| 입계(GB) | 무시 | **★ 핵심 축** |
| 입도분포 | 균일(단분산) | **★ 다분산 5+3 성분** |
| 실험 대조 | 정성, 자기 무효화 | 정성, **타 재료계** |
| 도메인 | 80×80×140 µm, 200 nm voxel | 25×25×50 µm, **100 nm** voxel(기하) / **200 nm**(전기화학) |

`[해석]` ★ **시드 산포가 1호 → 2호에서 후퇴했다.** 1호는 "무작위 충전만으로 `θ` 가
≈40 %p 벌어진다" 를 **인쇄했고**, 2호는 그보다 **작은 도메인**(부피비
`25×25×50 / 80×80×140 = 31250/896000 ≈ 1/28.7`)에서 **점당 1 개 구조**로 일한다.
→ `[해석]` **2호의 산포는 1호보다 클 가능성이 높은데 보고되지 않았다.**
Fig. 10 의 0.94 vs 0.89 같은 순위는 이 때문에 **신뢰 근거가 없다.**

---

## 16. 우리 프로젝트에 대한 시사점 (전부 `[해석]`)

### 16-1. ★★ **율(rate) 이 접촉 손실과 동역학 손실을 가르는 축이다**

논문이 인쇄한 두 문장을 붙이면 분리 시험이 나온다:
- `[인쇄, p5]` "At **lower current densities** … resulting in **reduced sensitivity to
  microstructural variations**."
- `[인쇄, p8]` `R_GB,3` 에서 CAM 의 큰 부분이 **초기 Li 농도 그대로** 남는다 (Fig. 5).

→ **세 성분의 율 의존이 다르다:**

| 성분 | `i → 0` 극한 | 이완(전류 차단) 후 전압 |
|---|---|---|
| 진짜 `LAM_PE`(재료 손실) | 그대로 (용량 축이 줄어 있다) | 회복 없음 |
| 기하 접촉 손실 `1 − θ_AM` | **그대로** (경로가 끊겨 있다) | **회복 없음** |
| 동역학 손실 `1 − η` | **0 으로 사라진다** | **회복 있음** |

→ **처방**: ASSB 자료에서 `LAM_PE` 를 적합할 때 **최소 2 개 율**(가능하면 pOCV + 중간율)
에서 같은 파라미터를 적합하고 **율 간 `a_PE` 차이**를 보고한다. 그 차이가 **동역학
성분의 하한**이다. 그러고도 남는 것이 `θ_AM · Q_material` 이고 **그 곱은 여전히
안 갈라진다**(1호의 결론은 유효하다).

이것은 액체셀 축의 [[thermo-kinetic-loss-partition]](ΔE/η)와 **형식이 같고 대상이
다르다** — 거기서는 `η` 가 분극 전압이었고, 여기서는 `η` 가 **겉보기 용량 인자**다.

### 16-2. **아핀 창 매개화가 깨지는 방식이 확인됐다 — 그리고 그것이 진단이 된다**

Fig. S5 의 `R_GB,3` 곡선은 `w/o GBs` 곡선의 **수평 스케일링이 아니다**(시작 전압 −175 mV,
기울기 다름). `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 이 세운 3 파라미터
(`a_PE, b_PE` + 상대극 평탄) 창 모형은 **열역학적 변형만** 표현한다.
→ `[해석]` **동역학 성분은 아핀 모형의 잔차에 남는다.** 이는 나쁜 소식이 아니라
**관측 가능성**이다: 아핀 적합의 **구조적 잔차 패턴**(특히 곡선 끝의 급락)이
동역학 성분의 지표가 될 수 있다. [[halfcell-ocp-shape-invariance]] 가 다루는
"모양 불변" 가정이 ASSB 에서 **어디서 먼저 깨지는가**의 첫 후보.

### 16-3. **`θ` 를 스칼라로 넣으면 안 된다 — 공간 분포가 있다**

Fig. 6c·8b 가 보여 준 것: `θ_SE` 는 **분리막에서 멀어질수록 떨어지고**, CAM 이용률
프로파일은 **집전체 쪽에서 무너진다.** 1호의 `θ_AM` 은 전극 전체 스칼라였다.
→ `[해석]` DEM 산출을 forward model 에 주입할 때 **`θ(z)` 단면 프로파일**을 함께 받아야
한다. 최소한 "평균 + 기울기" 2 개 수.

### 16-4. **우리가 이 논문에 공급할 수 있는 것 — 산포와 식별 가능성**

두 가지가 이 논문에 **명백히 비어 있고 우리가 가진 기계로 바로 채울 수 있다**:

1. **구조 실현 산포** (G2). 1호가 "실현만 바꿔도 `θ` 가 ≈40 %p 벌어진다" 를 인쇄했는데
   2호는 **28.7 배 작은 도메인에서 점당 1 개**로 일한다. → **같은 파라미터로 N 개 실현을
   돌려 `C_norm` 의 폭을 재는 것**이 이 논문의 Fig. 10·11b 순위를 검증/무효화한다.
   비용이 싸고 결과가 결정적이다.
2. **식별 가능성**(Q4). 이 논문은 `(SVF, ρ_S, d_SE, d_CAM, R_GB)` **5 차원 forward map** 을
   갖고 있다. [[near-optimal-set-width-measurement]] 를 그 위에 얹으면
   **"관측된 `C_norm`(또는 `V(Q)`)에서 이 5 개를 되찾을 수 있는가"** 를 바로 잴 수 있다.
   `[도표]` 로 본 바로는 **못 되찾는다** — `R_GB,3` 패널의 8 개 구조가 전부 0.20–0.25 로
   **구별 불가**하고, `R_GB,1` 패널은 0.85–0.94 로 **역시 좁다.** 즉 **입자 크기 축이
   용량 관측에 대해 거의 null 방향**이다. 이것은 [[fitting-degeneracy]] 가 화학 무관하게
   재현되는 **두 번째 자리**다 (첫 번째는 1호의 `A_spec,a` 평탄 봉우리).

### 16-5. **`bms-balancing` 5→3 붕괴와의 접속**

`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 의 실측(평탄 상대극 → `a_NE`·`b_NE`·`γ_Si`
민감도 정확히 0)은 **이 논문의 셋업과 정확히 맞는다** — Li 금속 음극 `U₀ = 0 V` 고정.
→ 남는 3 축(`a_PE`, `b_PE`, + 상대 정렬)에 이 논문이 **네 번째 축 `η(i)`** 를 추가한다.
`[해석]` 즉 ASSB 적합 문제는 **3 파라미터가 아니라 "3 + 율 의존 1"** 이고,
**율을 관측 축으로 쓰면** 그 하나는 **추가 관측으로 분리 가능**하다 (16-1).

### 16-6. **"모두가 안 잰 것" 원장 — `assb` 축 갱신**

[[mode-identifiability-unmeasured-lineage]] 와 같은 형식:

| 안 재는 것 | 지목한 주체 | 편수 |
|---|---|---|
| **공극률** | 1호가 8 편을 지목 | — |
| **LLZO 복합전극의 부분 전도도** | **2호가 스스로 "문헌에 없다"** | — |
| **압력** | **우리가 지목** | `assb` **2/2 편이 0 회** |
| **구조 실현 산포** | **우리가 지목** | 1호는 쟀고 **2호는 안 쟀다** |
| **유일성·식별성** | **우리가 지목** | `assb` **2/2 편이 안 쟀다** |

---

## 17. 후속 논문 후보 (이 논문이 가리키는 것)

| 순위 | 후보 | 왜 |
|---|---|---|
| **1** | **Ren, Danner, Moy, Finsterbusch, … Latz et al.**, *Adv. Energy Mater.* 2022, 2201939 (ref 17) — 이 논문이 **열화·최적화 양쪽에서 가장 많이 인용**하는 리뷰 | `[인쇄]` "the cathode is prone to **electrochemical and mechanical degradation**"·"contact loss … **mechanical degradation due to volume changes**"·"**single-crystal NMC, conducting additives**" 가 전부 ref 17 이다. **`θ(N)` 시간축의 문헌 입구.** |
| **2** | **Neumann, Hamann, Danner, Hein, … Latz**, *ACS Appl. Energy Mater.* 2021, 4, 4786 (ref 38) | **GB 모형의 원전**이자 `R_GB = 3.7 Ω cm²`·LLZO 파라미터 전부의 출처. 우리가 `η(i)` 를 모형화하려면 여기 식이 필요하다. EIS 로 파라미터화했으므로 **measured 라벨의 자리**이기도 하다. |
| **3** | **Minnmann, Quillman, Burkhardt, Richter, Janek**, *J. Electrochem. Soc.* 2021, 168, 040537 (ref 22) | Fig. 3 의 **유일한 실험 대조**. 복합양극의 **이온·전자 부분 전도도를 따로 재는 방법**(Q2 의 실체). 액체셀 계열에 없던 독립 관측 후보. |
| **4** | **Bielefeld, Weber, Rueß, Glavas, Janek**, *J. Electrochem. Soc.* 2022, 169, 020539 (ref 36) | 1호 저자들의 **후속**이며, 이 논문이 **NMC811 의 OCV(`U₀`)를 가져온 곳**. 1호가 전압축을 얻은 논문일 가능성이 높다 — **1호 계보에서 전압축이 언제 들어왔는지** 확인용. |
| **5** | **Al-Jaljouli, Mücke, Kaghazchi, … Guillon**, *J. Energy Storage* 2023, 68, 107784 (ref 42 / SI ref 1) | **구조 생성 알고리즘의 원전**이고, 제목이 "Microstructural parameters governing the **mechanical stress** and conductivity" — **역학이 들어 있는 쪽**. |
| 6 | **Eckhardt, Fuchs, Burkhardt, Klar, Janek, Heiliger**, *ACS AMI* 2022, 14, 42757 (ref 65) | `[인쇄]` "Small voids at the interface … cause **constriction effects**" — 1호가 명시적으로 **배제**한 수축 저항(1호 G8)을 정면으로 다룬 논문. |

---

## 18. 이 digest 가 주장하지 않는 것

- 이 논문이 **열화를 모델링했다고 주장하지 않는다.** 사이클 0 회, 역학 0, 접촉 손실의
  시간 변화 0. `ρ_S` 스윕은 **제조 공극**이다.
- **OCV 곡선이 있다고 주장하지 않는다.** 있는 것은 `U₀`(함수형 파라미터)와
  **1 mA/cm² 부하 방전 곡선**(Fig. S5)이다. `assb` 섹션에 **OCV 곡선은 여전히 0 편**이다.
- `Q_apparent = θ_AM · η · Q_material` 3 항 분해는 **우리 해석**이다 — 논문은 이 식을
  쓰지 않고, **G1 때문에 `C_norm` 이 어느 항까지 포함하는지도 확정되지 않았다.**
- "율을 바꾸면 갈린다" 는 **이 논문이 한 실험이 아니다.** 논문은 **단일 율**로만 돌았고
  (G12), 율 의존은 우리가 논문의 두 문장에서 **추론한 것**이다.
- 이 논문의 수치를 **실측으로 취급하지 않는다.** 셀 실험 0 개, 검증 0 개, 자기 재료계
  (LCO/LLZO) 실험 대조 0 개.
- **`assb` 결론을 액체셀로 옮기지 않는다.** 음극이 Li 금속(이상 접촉)이고 SE 는 단일
  이온 전도체(`t⁺=1`)라 **염 농도 구배가 없다** — 액체셀 P2D 와 방정식 구조부터 다르다.

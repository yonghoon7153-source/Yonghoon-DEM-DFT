---
title: "Neumann, Hamann, Danner, Hein, Becker-Steinberger, Wachsman, Latz 2021 — Effect of the 3D Structure and Grain Boundaries on Lithium Transport in Garnet Solid Electrolytes (ACS Appl. Energy Mater. 4, 4786-4804)"
source_url: local-upload/16._Effect_of_the_3D_structure_and_grain_boundaries_on_lithium_transport_in_garnet_solid_electrolytes.pdf + 16._Sup_Effect_of_the_3D_structure_and_grain_boundaries_on_lithium_transport_in_garnet_solid_electrolytes.pdf (SI)
source_url_note: "본문 19 쪽(그림 12 · 표 1 · 참고문헌 66) + SI 26 쪽(S1-S10, Table S1-S5, Fig. S1-S9). 크로퍼 27 장. Read 9 장(Fig. 4 · 5 · 6 · 7 · 8 · S1 · S4 · S5 + 표 S4 표기 확인), 나머지는 텍스트로. 실험 자료는 ref 30 · ref 9 재사용 — 인용 원전 미열람. 원자료는 커밋하지 않는다."
source_doi: 10.1021/acsaem.1c00362
source_license: "© 2021 American Chemical Society — 오픈액세스 표기 없음"
pdf_sha256: 9919ecef8b07fd25bb288c3d7d285cbc995cdc9065c14bc20bee80b12b495baf
si_sha256: 4de480f31aed9755d0de738c7363493393eeb1ac3c89431c6b5a0a6c19c28215
ingested: 2026-09-23
sha256: 8ed4ca348e9f226a114410a3ef7277a0b8454dd7a1fa462fb7abe9bdb7f08e48
---

# 수집 목적

`assb` 섹션 **54호**. 큐 **55번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **열여섯째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행 ★★★: "**GB 저항 모형 원전 + EIS 로 파라미터화된 measured 라벨**" — 지목 **3 회**: 02호 Clausnitzer 2023 ref 38(GB 전류식 (1) · `i₀^GB` · `σ` · `C^GB_DL` 전부 [38]) · 27호 Sinzig 2024 ref 14(공간전하층 확장의 예) · 53호 Ren 2023 ref [27](P2D 입력 `σ⁰_LLZO` 8 × 10⁻⁴ · `β_GB` 1.39 · `β_tort` 2.31 의 출처로 표기).
⚠ **Neumann 2020 *ACS AMI* 12, 9277(접촉 손실 → 활성 면적 → `R_ct`, 원장 별도 행)과 다른 논문이다** — 같은 제1저자 · 같은 DLR 모델(BEST), 이 편은 황화물 복합양극이 아니라 **LLZO 계열 고체전해질 자체**의 수송.

이 digest 의 1순위 물음: **(1) 벌크 전도도 `σ⁰` · 입계 동역학(`i₀₀^GB` ∝ `k_hop`, 53호 말로 `β_GB`) · 굴곡도(`τ`, 53호 말로 `β_tort`)를 이 편이 서로 갈라서 정했는가 — 무엇으로(3D 구조 계산? 한 EIS 의 두 호? 온도? 입도 시리즈?) (2) 각 값은 측정인가, 적합인가, 가정인가 — 원장의 "measured 라벨" 표현이 맞는가 (3) 이 편의 SE 펠릿 값을 복합양극 모델(02 · 27 · 53호)에 옮길 때 무엇이 조건인가.** 카드의 CAM–SE 접촉 `θ` 와는 다른 물리(SE–SE 입계 · SE 망 굴곡도)이고, 카드에 닿는 것은 **곱 축퇴 처방**과 **라벨 층위(Q3)** 쪽이다.

A. Neumann*, T. R. Hamann, T. Danner, S. Hein, K. Becker-Steinberger, E. Wachsman, A. Latz (7 인, * 교신 1) —
**"Effect of the 3D Structure and Grain Boundaries on Lithium Transport in Garnet Solid Electrolytes"**,
*ACS Appl. Energy Mater.* **2021**, **4**(5), 4786–4804, doi `10.1021/acsaem.1c00362` · 표제 "Article".
`[인쇄]` Received 2021-02-03 · Accepted 2021-04-20 · Published 2021-05-04 · "© 2021 American Chemical Society"(오픈액세스 표기 없음) · "The authors declare no competing financial interest."
소속: **DLR 공학열역학연구소 Stuttgart + HIU Ulm**(Neumann · Danner · Hein · Becker-Steinberger · Latz; Latz 는 Ulm 대 겸) · **UMD**(Hamann · Wachsman — 실험 쪽). 자금: 미·독 공동 "Interfaces and Interphases In Rechargeable Li-metal based Batteries"(DOE `DEEE0008858` + BMBF `03XP0223E`) · 계산 bwHPC JUSTUS.
**계보 겹침**: 02호(Clausnitzer 2023) · 53호(Ren 2023) 와 **같은 DLR · Latz 계열**(Danner · Latz), 53호 공저자 Hamann · Wachsman 도 여기 있다 — **53호의 `[27]` 은 공저자 자기 인용**이다.

본문 PDF **19 쪽**(논문 4786–4804 · 그림 12 · 표 1 · 참고문헌 66 번호) · SI PDF **26 쪽**(S1 구조 생성 · S2 차단 전극 · S3 수송식 · S4 입계 전류 유도 · S5 파라미터화(Fig. S4 · Table S4) · S6 유효 유전율 · S7 입계 저항 스윕(Fig. S5) · S8 ASR(Table S5) · S9 전류 분포 · S10 Bode · 참고문헌 18). sha256 은 frontmatter(본문 `pdf_sha256` · SI `si_sha256`). 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ **이 편은 모델 논문이다.** 1차 측정은 **UMD 쪽의 이미 출판된 자료**(FIB-SEM · 차단 전극 EIS = ref 30 Hamann 2020; 치밀 펠릿 EIS = ref 9 Han 2016)를 **재사용**한다. 이 편에서 새로 잰 스펙트럼 · 새 시편은 지면에 없다(측정 절차는 전부 "Details … in ref 30").

---

# 판정 (먼저)

> ★★★★ **세 인자를 가른 방식은 셋이 다르고, 가른 것은 하나뿐이다.**
>
> | 인자 | 이 편에서의 기호 · 값 | 어떻게 정했나 | 층위 |
> |---|---|---|---|
> | **굴곡도** (53호 `β_tort`) | Table 1 `τ` x/y/z = 1.75/1.68/1.78 (56 %) · 1.45/1.34/1.26 (42 %) · 1.21/1.15/1.20 (25 %) | **FIB-SEM 3D 재구성에서 계산**(GeoDict) — EIS 적합에 안 들어간다. 모델은 복셀 구조 위에서 풀므로 `τ` 는 **입력 파라미터가 아니라 기하가 내장**한다 | **computed-geometric** (단, 이진화 문턱 · 0.5 µm 재척도에 조건부) |
> | **벌크 `σ⁰`** | `σ_Li^SE` = **7.69 × 10⁻⁴** S cm⁻¹ ("within the grains") | `[인쇄]` "We **estimated** … using EIS measurements on highly dense LLCZNO pellets.⁹" — 문헌 범위 "2.4 to 7.69 × 10⁻⁴" 의 **윗끝**. 교정 스펙트럼(Fig. S4)에서 벌크 절편은 **측정 대역 밖**(아래 ②) | **external-input (EIS 유래, 분할 근거 미인쇄)** |
> | **입계** (53호 `β_GB`) | `i₀₀^GB` = **6.91 × 10⁻³** A cm⁻² · `C_DL^GB` = **9.75 × 10⁻⁹** F cm⁻² | `[인쇄]` "we use EIS measurements on dense pellets published in ref 9. These measurements are used to **estimate** the hopping rate `k_hop` and the DL capacity `C_DL^GB` which are in a second step **refined manually** to improve the agreement with the experimental data." 가상 치밀 시편은 재구성이 아니라 **GeoDict 다면체 `d = 15 ± 6 µm` 가정**(SI S5) | **hand-refined on one reused spectrum, over an assumed grain structure** |
>
> **곱 `σ⁰·ε/τ(²)` 의 축퇴는 "`τ` 를 구조로 계산해 한 인자를 떼어낸" 방식으로 푼다 — 그것까지는 풀렸다.** 남는 것은 **합** `R_bulk(σ⁰) + R_GB(i₀₀^GB, N_GB)` 이고, 이 합은 **풀리지 않았다 — 저자가 두 번 인쇄한다**: 본문 `[인쇄]` "Since both degradation mechanisms possess a similar effect on the impedance response, **an exact deconvolution of both contributions via EIS is unfeasible** without additional information on the GB composition." · SI S7 `[인쇄]` "Both the bulk conductivity influence as well as the GB interface resistance are **not fully separable by experimental EIS** without additional knowledge of the structural and compositional changes of bulk and GB during sintering." 합을 가르는 표준 채널 셋이 전부 없다:
> - **① 온도(`Ea`)**: 없다 — `T` = 300 K 하나(Table S4). `activation` · `Arrhenius` 0 회.
> - **② 주파수(벌크 호 ↔ 입계 호)**: 모델 안에는 있고(**`σ⁰` 는 고주파 절편을 옮기고 `i₀₀^GB` 는 안 옮긴다** — SI S7 `[인쇄]` "We do not observe a shift in the bulk polarization contribution along the x-axis"), **측정에는 없다** — `[인쇄]` 25 % 시편 벌크 특성 주파수 `f_C,B` = **1.40 × 10⁷ Hz** ↔ 장비 상한 "**around 1.5 × 10⁷ Hz**" · "we assume that the bulk polarization process is **not fully resolved** in the experiments". `[도표]` 교정 펠릿(Fig. S4) 실험 호는 Re ≈12 Ω cm² 에서 시작하고 모델의 벌크 절편은 ≈28 Ω cm² — **교정 데이터가 벌크 절편을 보지 못한다** ⇒ 교정이 정한 것은 합(≈95 Ω cm²)과 호 모양이고, 그 합의 `σ⁰` 몫은 **입력**이 정했다.
> - **③ 입도 시리즈(입계 수 ↔ 입계당 저항)**: 없다 — 입도가 공극률과 **교락**(`[인쇄]` 56 % `d̄` 3.1 µm ↔ 42 · 25 % 4.59 · 4.62 µm), 교정 치밀 시편의 입도(15 ± 6 µm)는 **가정**이다. 입계 호 크기 ∝ `N_GB/i₀₀^GB` 이므로 `[해석]` **교정이 정한 것은 `i₀₀^GB × d_dense` 한 조합**이고, 이 편은 `d_dense` 를 가정으로 닫았다.
>
> ★★★★ **원장 "EIS 로 파라미터화된 measured 라벨" 판정 — ❌ 두 곳이 틀렸다.** (i) **"measured" 아님**: 표 자신이 말한다 — Table S4 `[인쇄]` 범례는 "taken from the respective reference (superscript [# of REF]), **measured by the authors (superscript [°])**, or calculated (superscript [*])" 셋인데, **[°] 표시는 0 개 · [#REF] 표시도 0 개**이고 `i₀₀^GB` · `C_DL^GB` · `i₀₀^Li`(본문은 "measured by Han et al.") · `D` · `κ` 전부 **[*] "calculated"**, `σ` 는 **표시 없음**. 본문 동사는 "estimated … refined manually". (ii) **"라벨" 아님**: 이것은 열화 모드 라벨이 아니라 **모델 파라미터**이고, 교정 대상은 **남의 논문(Han 2016)에서 가져온 치밀 펠릿 스펙트럼 하나**(시편 수 · 반복 · 오차 0)다. 정확한 이름: **"재사용한 치밀 펠릿 EIS 한 스펙트럼 위에서 손으로 다듬은 입계 동역학 파라미터 — 벌크 몫은 외부 입력, 굴곡도는 구조 계산"**. `[해석]` 02호가 이 값을 "the GB resistance must not significantly exceed values **measured** in dense pellets"(02 p9)로 옮긴 곳에서 "measured" 가 붙었고, 원장이 그 낱말을 이었다.
>
> ★★★ **복합양극 이식 조건 — 53호의 `β_GB` · `β_tort` 는 이 편에 인쇄돼 있지 않다.** 이 편에 멱지수 · Bruggeman 식 · 8 × 10⁻⁴ 은 없다(`Bruggeman` 1 회 = **유전율** 혼합칙, SI S6). `[재현]` Fig. 8 판독에서: **`β_tort` 2.31 = 56 % 시편 한 점의 구조-만 전도도에서 정확히 나온다**(`ln(1.07e-4/7.69e-4)/ln 0.426` = 2.31; 25 % 점 2.54 · 42 % 점 2.23 — 단일 멱법칙이 아니다). **`β_GB` 1.39 는 "치밀 전 모형(2.15 × 10⁻⁴)으로 정규화한" 입계 초과 지수로만 근처에 온다**(점별 25 % 1.36 · 42 % 0.70 · 56 % 1.46 — 역시 단일 멱법칙 아님; 1.39 자체는 재현 못 함). 그렇게 읽으면 **53호가 곱한 `σ⁰` = 8 × 10⁻⁴ 은 치밀-입계 인자(×≈0.28)를 빠뜨린 값**이다 — 이 편은 7.69 × 10⁻⁴ 을 "**within the grains**" 로, 치밀 시편 전 모형을 **2.1 × 10⁻⁴** 로 인쇄하는데, 53호는 8 × 10⁻⁴ 을 "assuming GB contributions **similar to those measured in dense pellets**"(β_GB = 0)로 쓴다. `[재현]` 인자를 살리면 53호 state-of-the-art `σ_Li,eff` 4.7 × 10⁻⁶ → ≈1.3 × 10⁻⁶ S cm⁻¹. 이식 조건 넷(§6): ① `ε` 범위 — 이 편 SE 분율 0.43–0.75(공극 = 공기), 53호는 0.25(CAM 75 vol%)로 **외삽** ② 입계 항은 `τL/d` 에 비례하는데 `d` 가 공극률과 교락된 채 `ε` 의 지수로 흡수됐다 — **입도가 다른 복합체로 안 옮겨진다** ③ `σ⁰` 의 뜻(입자 내부 ↔ 치밀 펠릿 전체)을 맞춰야 한다 ④ 이 편의 다공 시편 불일치(56 % 에서 ≈30 %)는 벌크 저하 · 입계 저하 · 2차상 셋 중 무엇인지 **미분리** — 53호는 이를 "2차상 · 입계" 지수로 한 칸에 모았다(53호 Fig. 9 는 그 칸을 `β_SP` 라 부른다, 53호 D15).
>
> **채움표: ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(CAM 없음 — SE · Li 만) · Q2 없음 · **Q3 층 하나 새로** · **Q4 0/54 — 마흔여섯 번째 성질 "교정 단계에서 합을 입력으로 나누고, 적용 단계에서 같은 합의 비식별을 인쇄했다"** · Q5 해당 없음 · Q6 없음(`MPa` 1 = Li 음극 문헌 400 MPa) · Q7 · Q8 해당 없음. 곱 축퇴 처방 **서른일곱 번째 적용**(§8): 1단계 `C` 채널은 **입계 두께를 정하지 않는다** — `[재현]` 벽돌층 등가 두께 ≈**6.8 µm**(ε_r 75) · 3-a 온도 ❌ · 4단계 진폭 채널은 **모델에만**(Table S5 시나리오 1 ASR 1064 → 655 Ω cm², 0.1 → 10 mA cm⁻²) · 새 줄 "**벌크 특성 주파수 ↔ 측정 대역 상한**".

---

# 0. 원문에 없어서 확인이 필요한 것

1. **`σ⁰` = 7.69 × 10⁻⁴ 을 Han 2016 치밀 펠릿 스펙트럼에서 어떻게 벌크 몫으로 떼었는지** — 지면에 없다("estimated … using EIS measurements"). Fig. S4 에서 벌크 절편은 대역 밖이다. Han 2016(ref 9) 원문 미열람.
2. **"refined manually" 의 전후 값** — 첫 추정 `k_hop` · `C_DL^GB` 와 손 보정 뒤 값의 차이, 목적함수, 무엇에 맞췄는지(호 크기? 정점 주파수?) 0. 불확실성 0.
3. **치밀 시편 입도 15 ± 6 µm 의 근거 SEM** — "Based on the SEM images taken on the dense sample" 뿐, 그림 · 개수 0. 이 값이 `i₀₀^GB` 를 정한다(§4 ③).
4. **워터셰드 분할의 minima imposition 파라미터**(과분할 억제 강도) — SI S1.1 에 방법만, 값 0. 입계 수(`A_Spec,GB`)가 이것에 달렸다(02호 G-절이 같은 도구에서 반경 `R` 로 입도가 ×3.2 움직인 것을 보였다).
5. **Fig. 8 실험점(ref 30)이 어느 호까지를 "전도도" 로 셌는지** — `[재현]` 56 % 실험 첫 호 끝(≈5.4 kΩ cm²)으로 ≈5.9 × 10⁻⁶, 중주파 호까지(≈11 kΩ cm²) 넣으면 ≈2.9 × 10⁻⁶; Fig. 8 점(≈5.2–5.8 × 10⁻⁶)은 전자와 맞는다 — 즉 **"excellent agreement" 는 중주파 호를 뺀 비교**일 가능성(ref 30 미열람).
6. **`f_C,GB` ≈ 7.0 × 10⁶ Hz 의 계산법** — `[재현]` 한 계면 `R·C` 로는 ≈4.4 × 10⁶, 계면당 공간전하층 두 겹 직렬로 보면 ≈8.7 × 10⁶. 어느 쪽인지 미인쇄.
7. **다공 시편의 두께 방향 미러링**이 굴곡도 · 입계 수 통계를 보존하는지 — "Through the repetition process, we preserve the specific porosities, such as grain sizes and electrode tortuosity" 는 주장뿐, 거울면에서 경로가 꺾이는지 검사 0.
8. 실험 쪽 **시편 수 · 반복 · 오차 막대 0**(Fig. 8 회색 점은 ref 30 의 여러 시편 — 개별 정체 미표기).

---

# 1. 서지 · 낱말 지문

**낱말 지문**(NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문 참고문헌 전; SI 는 괄호 — SI 참고문헌 전; 다운로드 바닥글 줄 제외):

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** (SI 0) | **0** (0) | **0** (0) | 0 (0) | 0 (0) | **0** (0) | 0 (0) | 0 (0) | 0 (0) | **0** (0) | **1** (SI 0) |

- NFKC 변경 본문 **296 자**(`ﬁ` 143 · `ﬀ` 115 · `ﬂ` 32 · `ﬃ` 5 · 비분리 하이픈 1) · SI **91 자**(`ϕ` 53 · `˜` 23 · `µ` 12 · `ﬀ` 1 · `Ω` 1 · `²` 1) — **열 변화 0**. 소프트 하이픈 0 · 줄끝 하이픈 본문 27 곳 · SI 19 곳(이어도 열 변화 0).
- ⚠ **SI 는 LaTeX 조판이라 `fi` 합자가 추출에서 글리프째 빠진다**("tted" · "specic" · "modied" · "identied") — `fit*` · `identif*` 는 SI 에서 따로 셌다: **`fit*` SI 5**(분포 적합 3 — "distribution fit" · "Gaussian curve fit" · "adjusted to fit"; 치밀 시편 두께 "was fitted to the experimental pallet size" 1; "fitted curves" 1) · `identif*` SI 1(입계 활성계수를 "can be identified as an additional GB energy barrier").
- `MPa` 1 = **Li 음극 문헌값**("increasing the cell pressure up to 400 MPa during cycling", ref 17 Krauskopf 2019) — 이 편 셀의 압력 0.
- 보조(본문 / SI): **`deconvol*` 1 / 1**(둘 다 "exact deconvolution … unfeasible") · **`unfeasible` 1 / 1** · **`separab*` 0 / 1**("not fully separable by experimental EIS") · **`uniquely` 1 / 0**(2차상 배정 "cannot be uniquely assigned") · **`fit*` 1 / 5**(본문 1 = **남의 논문**의 ECM 적합 "based on a fit of equivalent circuit models" — 자기 교정은 "estimate … refined manually") · `refin*` 1 · `manual*` 1 · `estimat*` 13 / 6 · `assum*` 19 / 17 · `tortuos*` 16 / 3 · `grain bound*` 6 / 4 · `GB`/`GBs` 109 / 62 · `secondary phase` 43 / 7 · `dense` 53 / 5 · `measured` 14 / 1 · `calculated` 5 / 2 · `validat*` 5 / 1 · `qualitativ*` 7 / 0 · `excellent` 2 / 0 · `Bruggeman` 1 / 1(유전율) · `temperature` 5 / 4(실험 온도 시리즈 0) · **`activation` · `Arrhenius` · `error` · `sensitiv*` 의 파라미터 불확실성 용법 0**(`sensitiv*` 2 = "more sensitive to phase impurities" · CCD "sensitive to multiple factors") · `percolat*` 9 / 3(Li 금속 망) · `contact` 22 / 2(Li\|SE · 다공\|치밀 층 접촉) · `cathode` · `composite` **0 / 0**.
- `[해석]` 식별성 낱말 자리를 **"deconvolution … unfeasible"** 이 차지한다 — 이 계보에서 **비식별을 원문 스스로 인쇄한 편**(49호 "not uniquely identifiable" · 53호 "Deconvolution … is challenging" 에 이어). 그러나 `identifiab` 0 · 불확실성 0.

---

# 2. 방법 — 무엇을 재구성했고, 무엇을 풀었고, 무엇을 넣었나

## 2.1 구조 (§2.1, SI S1)

- 시편: LLCZNO(`Li₇La₂.₇₅Ca₀.₂₅Zr₁.₇₅Nb₀.₂₅O₁₂`) 다공층 **셋** — 공극률 56.6 · 42.6 · 25.0 vol%(`[인쇄]` Table 1). 제조 · 측정은 ref 30(Hamann 2020) · SI S1 "For a rigorous and detailed discussion … we refer to Ref. 1, 2".
- FIB-SEM: 면내 **0.05 µm** · 밀링 방향 **0.1 µm**(`[인쇄]` SI S1). 0.1 µm 등방 격자로 맞춰 ≈1000 × 1000 × 210 복셀 → 이진화(회색조 문턱; 2차상은 두 번째 문턱) → 역거리변환 + **minima imposition** + 워터셰드로 입자 분할(SI S1.1) → 2차상 재삽입 → **계산 복셀 0.5 µm 로 재척도**(`[인쇄]` "to reduce the computational cost").
- 분할 결과 인접 입자 쌍마다 입계 계면을 둔다 — `[인쇄]` "Despite the different colors, all grains do have the same physical and chemical properties."
- 입도: 부피 등가 구 직경 `d = (6V/π)^(1/3)`(SI 식 1) 분포에 "지수 감쇠 + 가우스" 를 적합하고 **가우스 중심을 평균 입도로** 쓴다(SI S1.2). `[도표]` Fig. S1: 56 % 는 **≈0.6–1.4 µm 에 가장 많은 입자**(정규화 1.0 에서 잘림) + 가우스 ≈3.25 µm · 25 % 는 가우스 ≈5.0 µm. ⚠ 표 1 은 25 % 를 **4.62 µm** 로 인쇄 — 판독 ≈5.0 과 ≈8 % 차(D14). `[해석]` 평균 입도는 **가장 많은 작은 입자를 "지수 꼬리" 로 빼고** 잡은 값이지만, 시뮬레이션은 분할된 **모든** 입자 사이에 입계를 둔다 — 표의 `d̄` 와 모델이 실제로 보는 입계 밀도는 같은 양이 아니다. 게다가 ≈1 µm 입자는 0.5 µm 재척도에서 **2 복셀 폭**이다.

**Table 1**(`[인쇄]`, SI Table S1 과 같은 값):

| | 56 | 42 | 25 |
|---|---:|---:|---:|
| 공극 vol% | 56.61 | 42.6 | 25.0 |
| LLCZNO vol% | 42.6 | 55.9 | 75.0 |
| 2차상 vol% | 0.77 | 1.7 | 0 |
| `A_Spec,SE` (× 10⁴ cm² cm⁻³) | 2.18 | 0.93 | 0.66 |
| `A_Spec,GB` (× 10⁴ cm² cm⁻³) | 1.37 | 1.08 | 1.35 |
| `τ` x / y / z | 1.75 / 1.68 / 1.78 | 1.45 / 1.34 / 1.26 | 1.21 / 1.15 / 1.20 |
| `d̄` (µm) | 3.1 | 4.59 | 4.62 |

`[인쇄]` "All three samples show an increase in tortuosity with increasing porosity of around 44%." · "we do not observe significant deviations between tortuosity values in the three spatial directions". ⚠ 표의 `τ` 의 **정의**(기하 굴곡도인가, 굴곡도 인자 `τ²` 인가)는 지면에 없다 — `[재현]` §5.1 은 이 편의 구조-만 전도도가 **`σ⁰·ε/τ_x²`** 와 맞음을 보인다(즉 표의 `τ` 는 **기하 굴곡도** 쪽).

## 2.2 모델 (§3, SI S3 · S4)

- 프레임워크: **BEST**(Fraunhofer ITWM 상용) — 복셀 구조 위에서 질량 · 전하 보존을 푸는 미세구조 해상 연속체 모델. EIS 는 Hein 2020(ref 34)의 **계단 여기법**으로 모의. 17 MHz – 1 Hz.
- SE 벌크: `N_SE = −D_SE∇c + j/F` · `j_SE = −σ_SE∇ϕ_SE`(SI Table S3) · `t⁺` = 1 · `D` 는 `σRT/(cF²)` 로 계산. ⚠ `[인쇄]` "In our model, we do not take into account the **polarization of the bulk SE grains**" — **벌크는 순수 옴**(벌크 RC 호 없음) ⇒ 모의 스펙트럼의 고주파 절편 = 벌크 저항.
- **입계 계면**(식 (9), SI 식 (12)–(27)): 전이상태 이론 + 질량작용 → `i_GB = k_hop √(c̃_Gi c̃_Gj) [exp(Δφ̃/2RT) − exp(−Δφ̃/2RT)]`, 대칭 인자 0.5 고정, 농도 인자 상수 ⇒ `i₀₀^GB := k_hop √(c̃c̃)`. 병렬로 **공간전하층 축전** `i_DL = C_DL^GB dΔΦ/dt`(식 (3) 을 입계에 옮김, 식 (10)–(11)). `[인쇄]` "the electrochemical potential of the transition state at the GB is only a function of **temperature**" — 온도 의존을 `γ‡_GB` 에 넣어 두고 **한 온도만** 푼다.
- 2차상: 이온 차단(`i₀` 1 × 10⁻⁸) + 축전(`C_DL^SP` 1 × 10⁻⁶ F cm⁻², "fixed … since the experimental EIS measurements indicate a presumable occurrence in the mid-frequency range").
- Au 차단 전극: `i₀^Au` 1 × 10⁻⁸ · `C_DL^Au` 2.4 × 10⁻⁴ F cm⁻² — `[인쇄]` "**adjusted** … based on the experimental data to reproduce the experimental impedance response at low frequencies".
- Li 금속: `i₀₀^Li` 2.59 × 10⁻² A cm⁻²(`[인쇄]` "measured by Han et al. using EIS on dense LLCZNO samples in a symmetric cell setup") · `κ` 10 × 10⁴ S cm⁻¹.

## 2.3 파라미터 출처 — 표 자신의 표기(Table S4, 쪽 렌더로 확인)

| 파라미터 | 값 | 표 표기 | 본문이 말하는 출처 |
|---|---|---|---|
| `c_Li^SE,0` | 0.0384 mol cm⁻³ | * — ⚠ 설명 "concentration of Li ions in **β-LPS**" | "composition and density … determined in previous studies⁷,⁹" |
| `σ_Li^SE` | 7.69 × 10⁻⁴ S cm⁻¹ | **표시 없음** | "estimated … using EIS … on highly dense LLCZNO pellets⁹" |
| `D_Li^SE` | 5.36 × 10⁻⁹ cm² s⁻¹ | * | `σRT/(cF²)` |
| `i₀₀^GB` | 6.91 × 10⁻³ A cm⁻² | * | Han 2016 치밀 펠릿 EIS 로 추정 + **손 보정** |
| `C_DL^GB` | 9.75 × 10⁻⁹ F cm⁻² | * | 같음 · "in the range reported in the literature for this type of process⁶¹"(Irvine 1990) |
| `i₀₀^Li` | 2.59 × 10⁻² A cm⁻² | * | "measured by Han et al." |
| `i₀₀^Au` · `C_DL^Au` | 1 × 10⁻⁸ · 2.4 × 10⁻⁴ | * | 억제 · "adjusted" |
| `F` | "9.6485 × 10⁵" C mol⁻¹ | — | ⚠ × 10 오기(D2) |
| `R` | "10.973 × 10⁶ m⁻¹ **Rydberg constant**" | — | ⚠ 기체상수 자리에 뤼드베리 상수(D2) |
| `T` | 300 K | — | 한 온도 |

`[인쇄]` 범례: "Values are taken from the respective reference (superscript [# of REF]), **measured by the authors (superscript [°])**, or calculated (superscript [*])." — **[°] 0 개 · [#REF] 0 개.** `[인쇄]` "The parameter set was not modified for the different samples with varying porosity."
`[재현]` `D = σRT/(cF²)` = 7.69e-4 × 8.314 × 300 / (0.0384 × 96485²) = **5.37 × 10⁻⁹** ✓ — 표의 `F` · `R` 오기를 넣으면 7.1 × 10⁻⁵(×1.3 × 10⁴)이므로 **계산은 올바른 상수로 했고 표만 틀렸다.**

---

# 3. 절별 해체

## 3.1 §1 서론 (p1–2, Fig. 1)

- 동기: Li 금속 음극 + LLZO 계 가넷. Li\|SE 계면 저항과 **SE 입계 저항**이 성능 한계; 덴드라이트는 입계를 따라 자란다(내부 기원 = 잔류 전자전도, 외부 기원 = 표면 결함 · 입계 · 불량 적심). 경험적 CCD(critical current density).
- **삼층(trilayer)** 구조: 다공 LLCZNO 두 층(≈70–100 µm) 사이 치밀 층(≈20 µm) — `[인쇄]` 다공층이 "increase the active surface area for electrochemical reactions by a factor of around 40⁷". UMD 가 제안한 구조(ref 7 Hitz 2019 · ref 8 Yang 2018).
- `[인쇄]` "EIS measurements demonstrate that GBs have a significant impact on the transport of lithium ions in the SE microstructure and become even more important in porous 3D networks.⁷,³⁰,³¹" ⚠ ref 8 과 ref 31 은 **같은 논문**(Yang … Hu, PNAS 2018, 115, 3770 — D10).
- Fig. 1 = 작업 흐름 모식(안 봤다).

## 3.2 §2 미세구조 모델 (p3–4, Fig. 2, 3)

§2.1 은 위 §2.1. §2.2 차단 전극 모의: 세 구조를 두께 방향으로 **반복 미러링**해 실험 두께(SI Table S2: 317 · 359 · 218 µm; EIS 면적 0.221 · 0.122 · 0.279 cm²)에 맞추고 면내 100 × 100 복셀로 자른 뒤, 양면에 Au 층 8 복셀. `[인쇄]` "Since we could not fully resolve the evidence for a secondary-phase formation using X-ray diffraction (XRD),³⁰ we do not take them into account in our base model."
§2.3 삼층: 56 % 구조 사용(에너지 밀도 이유), 다공 100 µm × 2 + 치밀 20 µm, 440 × 100 × 100 복셀 = 220 × 50 × 50 µm³. `[인쇄]` 치밀 층은 "a homogeneous layer containing **no grains and GBs**, as indicated by experimental measurements" — ⚠ `[해석]` 교정에 쓴 치밀 펠릿은 입계를 가진 다면체 구조(15 µm)로 모의했는데, 삼층의 치밀 층은 입계 0 — 같은 "치밀 LLCZNO" 에 두 모델.
Fig. 2 · 3 안 봤다(모식 · 구조 렌더).

## 3.3 §3 모의 방법 (p4–6) — §2.2 · §2.3 참조

- §3.3.1 `[인쇄]` "The **most decisive** transport parameter is the ionic conductivity of the SE. We **estimated** the bulk ionic conductivity **within the grains** σ = 7.69 × 10⁻⁴ S/cm using EIS measurements on highly dense LLCZNO pellets.⁹ This is also in line with previous measurements published in the literature, which range from **2.4 to 7.69 × 10⁻⁴** S/cm at room temperature." 2차상 `σ^SP` = 1.0 × 10⁻⁹("can be regarded as isolating").
- §3.3.5 입계: 위 판정 표의 인용문 + `[인쇄]` "Note that we use the **same set of GB parameters** given in Table S4 for all simulations shown in this publication."
- §3.4.2 ASR: 정전류에서 정상 상태를 풀어 ASR 산출. `[인쇄]` "our continuum modeling framework is **not able to model the time-resolved lithium nucleation and film growth** … we need to simulate specific cell configuration, which recreates experimentally observed or expected snapshots."

## 3.4 §4.1 구조 분석 (p6–7, Table 1)

위 §2.1 표. `[인쇄]` 가장 다공한 시편 입도가 "around 32% smaller" → 비표면적 ↑ → 소결 중 표면 열화 ↑ 가능. `[인쇄]` "Even though the samples with 56% and 25% porosities have comparable specific GB surface area, due to longer lithium transport pathways, the highly porous sample is expected to show higher GB contributions".

## 3.5 §4.2 임피던스 (p7–11, Fig. 4–7, SI S5–S7 · S10) — 이 편의 식별성 본체

**§4.2.1 벌크 ↔ 입계 (25 %, 217 µm, Fig. 4).** `[도표]` 모의(주황): 고주파 절편 ≈53 Ω cm²(`[인쇄]` "around 53 Ω cm²") → 호 → ≈295 Ω cm² 에서 Au 차단 수직선. 실험(회색 점선): 10 MHz 에서 Re ≈10 Ω cm² 부근 시작 → 첫 호 정점 ≈125 · 100 kHz 에서 ≈275 부근 골 → 두 번째 과정(10 kHz ≈370) → 1 kHz 이후 상승. 위상각(Fig. 4b): 실험 최소 ≈0.18 rad(≈10⁵ Hz), 모의는 10⁵–10³ Hz 에서 ≈0.
`[인쇄]` "Even within our model framework, **the assignment of processes is challenging**, since minor changes in the material composition significantly change the EIS response. Several impedance studies on LLCZNO materials are published in the literature,⁹,³⁰,⁵⁷ **each of them providing a different interpretation of the data**." · `[인쇄]` "Since the bulk polarization contribution enters as a constant shift along the x-axis in our model, we therefore **cannot account for the superposition of the two polarization contributions** as measured in the experiment." · 결론 `[인쇄]` "we conclude that we have an **overlap between bulk and GB processes** in the frequency regime between 10⁷ and 10⁶ Hz in the experimental data. Thereby, the bulk contribution is smaller in magnitude and **the contribution of the GBs dominates** the impedance." `[해석]` "입계가 지배한다" 는 모델의 분할(입력 `σ⁰` 이 벌크 몫을 정한 뒤 남은 몫)에서 나온 문장이고, 실험 스펙트럼은 두 과정을 **겹쳐서** 보인다고 저자가 바로 앞에 적었다.
유효 유전율(Bruggeman 혼합, SI S6): 25 % → ε_eff = 47(`[재현]` 47.5 ✓) · `f_C,B` = 1.40 × 10⁷ Hz(`[재현]` 1.40 × 10⁷ ✓) · `C_DL` = 9.75 × 10⁻⁹ F cm⁻² · `f_C,GB` ≈ 7.0 × 10⁶ Hz.

**§4.2.2 공극률 (Fig. 5).** `[인쇄]` "the parametrization for all three samples is identical, and therefore, changes in our simulations arise only due to differences in the sample microstructure." `[도표]` 첫 호 끝(모의 ↔ 실험): 25 % ≈295 ↔ ≈290 Ω cm² · 42 % ≈900 ↔ ≈1300 · 56 % ≈3.9 ↔ ≈5.4 kΩ cm²(56 % 실험은 뚜렷한 두 번째 호). `[인쇄]` "our model **underestimates the impedance at high frequencies by almost 30%** for the highly porous samples" — `[재현]` 3.9/5.4 = −28 % ✓. `[인쇄]` "The measurements do not show the same shift [of the high-frequency intercept], which again points at overlapping contributions of bulk and GB processes". `[인쇄]` 입계: "the reduced tortuosity in the 25% sample provides shorter pathways … and consequently **reduces the number of GBs along the path**. In contrast, for the highly porous sample, the **reduced grain size and larger tortuosity** give rise to a higher number of GBs" — 저자 스스로 입도와 굴곡도를 **한 문장에 묶는다**(③ 교락).

**§4.2.3 벌크 전도도 스윕 (Fig. 6, 42 · 56 %).** `σ_bulk` 7.69(범례 "7.67") → 5.0 · 4.0 · 3.0 · 2.0 × 10⁻⁴, 나머지 고정. `[도표]` 벌크를 낮추면 고주파 절편이 오른쪽으로 옮겨지고 호도 커진다. 최적: 42 % → **3.0 × 10⁻⁴**(끝 ≈1240 ↔ 실험 골 ≈1270) · 56 % → **2.0 × 10⁻⁴**(끝 ≈5.45 ↔ 실험 골 ≈5.4 kΩ cm²; 그러나 호 높이 ≈2.0 ↔ 실험 ≈2.4). `[인쇄]` "we see a reduction in bulk conductivity by **60 and 75%**" — `[재현]` 1 − 3.0/7.69 = 61 % · 1 − 2.0/7.69 = 74 % ✓. 그리고 곧바로 판정 표의 "exact deconvolution … unfeasible" 문장.

**SI S7 입계 스윕 (Fig. S5, 42 · 56 %).** `i₀₀^GB` × 0.75 · × 0.50, 나머지 고정. `[도표]` 고주파 절편은 **안 움직이고**(`[인쇄]` "We do not observe a shift in the bulk polarization contribution along the x-axis") 호만 커진다. 최적: 42 % → **× 0.50**(끝 ≈1340 ↔ 실험 골 ≈1270) · 56 % → **× 0.75**(끝 ≈4.85 ↔ ≈5.4; × 0.50 은 ≈6.45 로 넘침). `[인쇄]` "the GB charge transfer resistance **does not increases monotonically** with increasing sample porosity" — 저자는 이를 입계 편석 경로 길이로 설명하지만(`[인쇄]` "would indicate that the lithium segregation into the GB … would be dependent on the specific SE surface area") **검증 0**. ⚠ 본문은 이 스윕을 "The increase in the GB charge transfer resistance by **25%** improves the agreement" 로 옮긴다 — `i₀₀` × 0.75 는 저항 **+33 %**, 42 % 최적 × 0.50 은 **+100 %**(D6).
`[해석]` **두 한-파라미터 스윕이 같은 저주파 끝(첫 호 골)에 닿는다** — 다른 것은 고주파 절편뿐이고 그것은 측정 대역 밖이다. 저자가 인쇄한 "unfeasible" 의 **그림 판**이 Fig. 6 ↔ Fig. S5 겹치기다([[assb-sensitivity-sweep-vs-identifiability]] 처방 2 — "스윕 그림끼리 겹친다").

**§4.2.4 2차상 (Fig. 7, 56 %).** `[인쇄]` "We **assume** that the mid-frequency polarization contribution is related to the formation of a secondary phase" · "the content is as low as **0.77 vol %**, and contributions of measurement artifacts cannot be excluded. Moreover, no additional phases were found in XRD measurements since such small amounts are below the detection limit." 재구성 분포(군집, SE 표면 ≈1.2 % 접촉) → `[도표]` ≈5 × 10³ Hz 에 작은 위상 봉우리, Nyquist 에는 거의 안 보임. 인공 박막(표면 피복 ≈2.2 %) → 두 번째 호 ≈3.6 → ≈5.4 kΩ cm²(`[도표]` 폭 ≈1.8) ↔ 실험 두 번째 호 ≈5.5 → ≈11 kΩ cm²(폭 ≈5.5). `[인쇄]` "Since our simulated distribution is **artificial**, we can only draw **qualitative conclusions**" · "we expect that our model simulations only reproduce qualitative trends observed in the experiments."

## 3.6 §4.3 유효 전도도 (p11, Fig. 8) — 53호가 가져간 곳

`[인쇄]` "we separate the effect of the microstructure and GBs on the conductivity" — **구조만(파랑)** ↔ **구조 + 입계(빨강)**. `[도표]` Fig. 8(반로그, S cm⁻¹):

| 공극 % | 구조만 | 구조 + 입계 | 빨간 띠 아래끝 (`σ_bulk` 낮춤) | 실험점(ref 30, 근처) |
|---|---|---|---|---|
| 0 | ≈7.7e-4 (= `σ⁰`) | **≈2.15e-4** (`[인쇄]` "2.1 × 10⁻⁴") | — | ≈2.45e-4 · ≈3.0e-4 · ≈5.4e-4 |
| 25 | ≈3.7e-4 (`[인쇄]` 3.66e-4, §4.2.1) | ≈7.0e-5 | — | ≈4.0e-5 (18 %) · ≈6.7e-5 (20 %) · ≈4.9e-5 (27 %) |
| 42 | ≈2.1e-4 | ≈3.9e-5 | ≈2.7e-5 | ≈1.5e-5 · ≈6.3e-5 · ≈8.5e-6 · ≈1.6e-5 (41–44 %) |
| 56 | ≈1.07e-4 (`[인쇄]` "1.1 × 10⁻⁴") | ≈8.6e-6 (`[인쇄]`) | ≈6e-6 | ≈1.45e-5 · ≈1.6e-5 (53–54 %) · ≈5.8e-6 (55.5 %) · ≈6.5e-6 (57 %) · ≈5.2e-6 (62 %) |

`[인쇄]` "deviations to the experimental data are still another order of magnitude (∼5.17 × 10⁻⁶ S/cm)" · "the GB resistance provides a significant contribution to the reduction of the ionic conductivity from 2.1 × 10⁻⁴ S/cm down to 8.6 × 10⁻⁶ S/cm when going from the dense to the highly porous sample" · 벌크 저하를 넣으면 "**in excellent agreement** with the experimental data" · "Note that in these calculations, we did not account for the influence of secondary phases".
`[해석]` ⚠ 실험점은 **같은 공극률 근처에서 ×≈7 흩어진다**(41–44 % 에서 ≈8.5 × 10⁻⁶ ↔ ≈6.3 × 10⁻⁵) — "excellent agreement" 의 판정 해상도가 그 산포보다 좁지 않다. 치밀 0 % 에서 모델 전 모형(≈2.15 × 10⁻⁴)은 **실험 세 점 모두의 아래**, 구조만(= `σ⁰`)은 **모두의 위**다.

## 3.7 §4.4 삼층 셀 (p11–16, Fig. 9–12, SI S8 · S9)

56 % 구조, 양쪽 다공층 근집전체 절반을 Li 로 채움 + 남은 공극 표면 Li 피복 0 · 32 · 55 · 73 %(잔류 Li ≈0 · 3 · 6 · 10 vol%; 73 % 에서만 전자 퍼콜레이션). **2차상 · 벌크 저하는 끔**(`[인쇄]` "Degradation of the materials due to lithium evaporation during sintering … is neglected in this study").
ASR(SI Table S5, `[인쇄]`, Ω cm²):

| mA cm⁻² | 0 % | 32 % | 55 % | 73 % |
|---|---:|---:|---:|---:|
| 0.1 | 1064 | 170 | 16 | 6 |
| 0.5 | 1053 | 170 | 15 | 6 |
| 1 | 1026 | 170 | 15 | 6 |
| 5 | 767 | 168 | 15 | 6 |
| 10 | 655 | 164 | 15 | 6 |

`[인쇄]` "In scenario 1, the ASR for all currents **fluctuates around 1100** Ω cm²" — ⚠ 표는 0.1 → 10 mA cm⁻² 에서 **1064 → 655(−38 %)** 로 **단조 감소**한다(요동이 아니다, D19). `[재현]` 시나리오 1 = Li 없는 다공 두 구간 50 µm × 2 를 전 모형 `σ_eff`(8.6 × 10⁻⁶)로 + 치밀 20 µm(입계 0, 7.69 × 10⁻⁴): 2 × 0.005/8.6e-6 + 0.002/7.69e-4 ≈ **1166** Ω cm² ↔ 인쇄 1064(저전류) — ≈10 % 안 ⇒ **이 ASR 은 입계 포함 유효 전도도의 옴 합산**이다. `[해석]` 전류 의존의 출처: 모델의 비선형 원소는 입계 sinh(식 (9))와 Li 계면 BV 둘뿐이고 벌크는 옴 — 시나리오 1 의 −38 % 는 **입계 sinh 가 국소 고전류에서 선형 영역을 벗어난 것**으로 읽힌다(`[재현]` 입계당 선형 저항 `RT/(F·i₀₀^GB)` = **3.74 Ω cm²**, 국소 입계 전류가 `i₀₀^GB` ≈6.9 mA cm⁻² 를 넘으면 비선형; `[인쇄]` 0.5 mA cm⁻² 외부 전류에서도 국소 SE 전류 "up to 9 mA/cm²"). 저자는 이 진폭 의존을 **해석하지 않는다**.
나머지 인쇄: 73 % → ≈7 Ω cm² 는 "also reported in experiments on similar structures⁷" · 치밀 층 몫 "∼3.7−7 Ω cm²" · 전류 핫스팟(시나리오 1: 국소 최대 9 mA cm⁻², SE 의 ≈73 % 가 외부 전류 초과; 시나리오 4: 1.1 %) · 10 mA cm⁻² 에서 계면 전류의 ≈1.5 % 가 CCD 0.9 mA cm⁻² 초과 · 입계 계면 전류 봉우리 ≈2 mA cm⁻²(치밀 층 근처) · **혼합 삼층**(치밀 층 양쪽 7 µm 두께 25 % 층) → 0.5 mA cm⁻² 초과 분율 −30 % · ASR −4.3 Ω cm²(−30 %) · Li 계면 전류 초과 분율 ×4. `[인쇄]` "we believe that the benefits … more than compensate" · "additional experimental studies are needed to test the predicted improvements". Fig. 9–12 · S6 · S7 안 봤다(표 S5 · 본문 수치로).

## 3.8 §5 결론 (p16)

`[인쇄]` "Our simulations indicate that highly porous samples are prone to lithium evaporation, reducing the bulk **and/or** GB conductivity" — 결론도 "and/or" 로 **분리 불가를 유지**한다(49호형 "결론에서 지웠다" 가 아니다). `[인쇄]` "Simulated effective conductivities are in excellent agreement with the experimental data". `[인쇄]` "fundamental questions such as the influence of GB properties and composition on the effective SE conductivity need to be addressed."

---

# 4. 식별성 해부 — 네 양이 무엇에 의해 정해졌나

**① 굴곡도 — 계산, 적합 아님(✅ 떼어냄).** 모델이 복셀 구조 위에서 풀리므로 `τ` 는 파라미터 벡터에 없다. 구조-만 계산(Fig. 8 파랑)이 `σ⁰` 와 기하만의 함수다. 조건: 이진화 문턱(단일 회색조) · 0.5 µm 재척도 · 두께 미러링 — 셋 다 민감도 0. `[재현]` §5.1: 구조-만 전도도 ÷ `σ⁰` ≈ `ε/τ_x²`(56 % 0.139 ↔ 0.139 · 42 % 0.266 ↔ 0.273 · 25 % 0.512 ↔ 0.481) ⇒ 표의 `τ` 는 **기하 굴곡도**, 굴곡도 인자는 `τ²`([[assb-tortuosity-factor-effective-conductivity-split]] 의 이름 충돌 축).

**② 벌크 `σ⁰` — 외부 입력(❌ 데이터가 정하지 않음).** 교정 스펙트럼(Fig. S4, Han 2016, 200 µm · "Porosity 2%")에서 `[도표]` 실험 호는 Re ≈12 Ω cm² 에서 시작하고, 모델 벌크 절편은 ≈28 Ω cm²(`[재현]` 0.02 cm / 7.69e-4 = 26.0 Ω cm²). `[재현]` 치밀 LLCZNO(ε_r 75)의 `f_C,B` = σ/(2πε₀ε_r) ≈ **1.8 × 10⁷ Hz** — 장비 상한 ≈1.5 × 10⁷ 위. ⇒ 교정 데이터에는 **벌크 절편이 없다**; 벌크 몫은 입력 7.69 × 10⁻⁴ 이 정했고, 그 값은 문헌 범위 2.4–7.69 × 10⁻⁴ 의 **윗끝**이다. `[해석]` 윗끝을 고를수록 같은 합에서 입계 몫이 커진다 — "입계가 지배한다" 는 이 선택과 같은 방향이다.

**③ 입계 `i₀₀^GB` — 가정 위의 손 보정(❌ 곱).** 호 크기 ∝ (경로 위 입계 수) / `i₀₀^GB` ∝ `L·τ/(d·i₀₀^GB)`. 교정 시편의 `d` = 15 ± 6 µm 는 **SEM 에서 본 값을 넣은 GeoDict 다면체**(재구성 아님). ⇒ 교정이 정한 것은 `d_dense·i₀₀^GB` 한 조합이고, `d_dense` 가 절반이면 `i₀₀^GB` 도 절반이어야 같은 호가 나온다. 이 값은 그대로 **다공 시편(분할 입도 3.1–4.6 µm) · 삼층 · 02호 복합양극**으로 간다. `[재현]` 입계당 선형 저항 3.74 Ω cm²(02호 G8 "≈3.7" 과 같다).

**④ 입계 `C_DL^GB` — 호 위치 맞춤(❌ 두께를 정하지 않는다).** 1단계 전제("`C` 가 계면 두께 · 면적을 말한다")를 이 값에 걸면: `[재현]` 벽돌층 등가 두께 `δ = ε₀ε_r/C` = 8.854 × 10⁻¹⁴ × 75 / 9.75 × 10⁻⁹ ≈ **6.8 µm** — 입계(53호 인용 TEM ≈1.5 nm)나 공간전하층(nm–수십 nm)보다 **10²–10³ 배** 두껍고, 치밀 입도(15 µm)의 절반이다. 셀상수 1 cm⁻¹ 로 환산한 호 용량 ≈9.75e-9/(1 cm / 15 µm) ≈ **1.5 × 10⁻¹¹ F** — Irvine 1990(ref 61) GB 범위(10⁻¹¹–10⁻⁸ F)의 **바닥**이고 벌크(ε_r 75 → ≈6.6 × 10⁻¹² F)의 **≈2.2 배**뿐이다. ⚠ 원문의 "in the range reported in the literature" 는 **계면당 F cm⁻²** 와 **셀상수 정규화 F** 를 단위 환산 없이 나란히 둔 비교다. `[해석]` 이 `C` 는 입계 호를 벌크 호와 **같은 10⁶–10⁷ Hz 대역**에 두도록 고른 값이고(그래서 저자가 "overlap" 이라 쓴다), 물리적 입계 두께를 주지 않는다 — **C 채널이 막힌 이유가 측정이 아니라 파라미터 선택 쪽에 있다.** nm 급 입계 용량이면 입계 호는 벌크보다 10²–10³ 배 낮은 주파수로 가서 **두 호가 갈렸을 것**이다(`[추론]`, 원문 0).

**⑤ 다공 시편에서 남는 것.** 56 % 에서 ≈30 % 저평가 → 설명 후보 셋: `σ⁰` 저하(Fig. 6) · `i₀₀^GB` 저하(Fig. S5) · 2차상(Fig. 7, "assume"). 셋 다 한-파라미터 스윕이고 **공동 적합 · 상관 · 폭 0**. 저자 판정 "unfeasible without additional information on the GB composition". 입도 · 굴곡도 · 비표면적 · 2차상 분율이 공극률과 **함께** 움직이는 세 시편이라 시리즈도 못 가른다.

**정리(`[해석]`)**: 원장의 물음 "곱 `σ⁰·ε/τ` 형 축퇴를 어떻게 풀었나" 의 답 — **곱은 구조 계산으로 풀었고, 합은 입력과 가정으로 닫았다.** 온도 · 입도 시리즈 · 고주파 대역 확장 중 무엇도 쓰지 않았다.

---

# 5. `[재현]` 계산 모음

1. `D` = 5.37 × 10⁻⁹ cm² s⁻¹(인쇄 5.36) — 올바른 `R` · `F` 로. 표의 `R`(뤼드베리) · `F`(×10)로는 7.1 × 10⁻⁵.
2. Bruggeman 유효 유전율(SI 식 28, ε_SE 75 · 공기 1): 25 % → **47.5**(인쇄 47 ✓) · 42 % → 26.9 · 56 %(ε_SE 0.426) → **13.6** / (0.434, 2차상 포함) → 14.3 ↔ SI S6 인쇄 "**16**"(D8).
3. `f_C,B`: 25 % (3.66e-4, 47) → **1.40 × 10⁷** ✓ · 56 % (SI 7.56e-5, 16) → 8.49 × 10⁶ ↔ 인쇄 8.27 × 10⁶(≈3 %) · 56 % 를 본문 1.1 × 10⁻⁴ 로 하면 1.24 × 10⁷ · 치밀(7.69e-4, 75) → 1.84 × 10⁷.
4. 입계: `RT/(F i₀₀^GB)` = **3.74 Ω cm²** · 한 계면 `f = 1/(2πRC)` = **4.4 × 10⁶ Hz**(C/2 면 8.7 × 10⁶) ↔ 인쇄 7.0 × 10⁶.
5. `C_DL^GB` 벽돌층 등가 두께 **≈6.8 µm**(ε_r 75) · 호 용량 ≈1.5 × 10⁻¹¹ F(셀상수 1 cm⁻¹, 15 µm 간격) ≈ 벌크의 2.2 배.
6. 첫 호 끝 → 전도도: 25 % 0.02175/295 = 7.4 × 10⁻⁵(Fig. 8 ≈7.0 ✓) · 42 % 0.03591/900 = 4.0 × 10⁻⁵ ✓ · 56 % 0.03168/3900 = 8.1 × 10⁻⁶ ✓ · 실험 42 % 1300 → 2.8 × 10⁻⁵ · 56 % 5400 → 5.9 × 10⁻⁶ · 56 % 두 호 합 ≈11 000 → 2.9 × 10⁻⁶.
7. 치밀 교정: 전 모형 끝 ≈95 Ω cm²(`[도표]`) → 0.02/95 = **2.1 × 10⁻⁴** ✓(Fig. 8 치밀 전 모형과 같다).
8. 벌크 저하 비: 61 % · 74 %(인쇄 60 · 75 ✓). `i₀₀` × 0.75 = 저항 +33 %(본문 "25%" ✗).
9. 삼층 시나리오 1 ASR ≈1166 Ω cm²(인쇄 1064 @0.1 mA).
10. **53호 지수 추적**(§6 표).

---

# 6. 53호 `β` 추적과 복합양극 이식 조건

53호 SI 식 (8) `[인쇄]`(53호 digest 에서): `σ_Li,eff = ε_LLZO^β_e · σ⁰_LLZO`, `β_e = β_GB + β_tort`; Table 3 `σ⁰` 8 × 10⁻⁴ · `β_GB` 1.39 · `β_tort` 2.31 — 셋 다 `[27]` = 이 편. 53호 본문 `[인쇄]` "By avoiding secondary phases and **assuming GB contributions similar to those measured in dense pellets[27]** (σ⁰ = 8 × 10⁻⁴ S cm⁻¹, β_GB = 0)".

**이 편의 지면에는** 멱지수 · 8 × 10⁻⁴ · `ε^β` 형 식이 **없다**. `[재현]` Fig. 8 판독값으로 점별 지수(`ε` = LLCZNO vol%):

| 공극 % | `ε` | 구조-만 지수 `ln(σ_str/σ⁰)/ln ε` | 치밀 전 모형 정규화 총지수 `ln(σ_full/σ_full,0)/ln ε` | 차 = 입계 초과 지수 | 비정규화 총지수 `ln(σ_full/σ⁰)/ln ε` |
|---|---|---:|---:|---:|---:|
| 25 | 0.75 | 2.54 | 3.90 | **1.36** | 8.33 |
| 42 | 0.559 | 2.23 | 2.94 | **0.70** | 5.13 |
| 56 | 0.426 | **2.31** | 3.77 | **1.46** | 5.27 |

(인쇄값만으로 56 %: `β_tort` 2.28 · 입계 초과 1.47.)
- `[해석]` **`β_tort` 2.31 = 56 % 시편 한 점.** 세 점이 한 멱법칙에 서지 않는다(2.23–2.54).
- `[해석]` **`β_GB` 1.39 는 치밀 전 모형 정규화에서만 근처(1.36 · 1.46)** — 42 % 점은 0.70 이고, 1.39 를 정확히 주는 조합은 찾지 못했다. 비정규화로 읽으면 입계 지수는 2.9–5.8 이라 1.39 와 멀다.
- 그렇다면 `σ_full(ε) ≈ σ_full,0 · ε^(β_tort + β_GB)` 이고 `σ_full,0` = **2.1 × 10⁻⁴**(치밀, 입계 포함) 이어야 한다. 53호는 **8 × 10⁻⁴**(≈이 편의 입자 내부 값 7.69 × 10⁻⁴)을 곱했다 ⇒ `[재현]` 53호 state-of-the-art `ε` 0.25: 8e-4 × 0.25^3.7 = 4.7 × 10⁻⁶ ↔ 치밀-입계 인자 2.1/7.69 를 살리면 **1.3 × 10⁻⁶**(×0.27). ⚠ 이것은 **우리 재구성**이다 — 53호 SI 는 지수 도출을 적지 않는다.

**복합양극 이식 조건(`[해석]`, 근거는 위 표 + 이 편 인쇄문)**:
1. **`ε` 범위** — 이 편 SE 분율 0.43–0.75(두 번째 상 = 공기). 53호의 복합양극 SE 분율 0.25(CAM 75 vol%)는 **범위 밖 외삽**이고, 두 번째 상이 **CAM**(공소결 계면 · 상호확산 · 소결 이력 다름)이다.
2. **입도** — 입계 항 ∝ `τL/d`. 이 편 세 시편의 `d` 가 공극률과 같이 움직였으므로 `ε` 지수가 `d` 효과를 흡수했다. 복합체의 LLZO 입도(02호는 `d_SE` 를 스윕한다)가 다르면 지수는 옮겨지지 않는다. 02호처럼 **계면당 `i₀₀^GB` 로 옮기면** 이 문제는 피하지만, 그 값 자체가 가정된 치밀 입도(15 µm)에 조건부다(§4 ③).
3. **`σ⁰` 의 뜻** — "입자 내부"(이 편) ↔ "치밀 펠릿 전체"(53호 문장) — ×≈3.7 차.
4. **다공 시편 불일치의 배정** — 이 편은 벌크 · 입계 · 2차상을 **미분리**로 남겼다. 53호는 그 초과분을 `β_GB`("secondary phases and grain boundaries") 한 칸에 넣고 개선 시나리오에서 0 으로 지웠다(53호 Fig. 9 의 `β_SP` 막대). 이 편의 결론 "bulk **and/or** GB" 를 한쪽으로 읽은 것이다.
5. 이 편은 **Li 금속 · 차단 Au** 대칭 구조만 다뤘다 — 양극 활물질 · 산화물 CAM\|LLZO 계면은 0(`cathode` 0 회).

---

# 7. 계보 대조 — 지목 셋이 가져간 것

| 지목 | 가져간 것 | 원문(이 편)에서의 그 값 | 판정 |
|---|---|---|---|
| **02호** Clausnitzer 2023 ref 38 | 식 (1) 입계 BV · `i₀^GB` 6.91e-3 · `C^GB_DL` 9.75e-9 · `κ^SE` 7.69e-4 · `c` 0.0384 · `D` 5.36e-9 · `i₀^Li` 2.59e-2(02 Table 1 전부 "[38]"). 02 p3 "which can be **estimated** from EIS measurements" · 02 p9 "the GB resistance must not significantly exceed values **measured** in dense pellets" | 값은 **일치**. 이 편 표 표기 = 전부 "calculated" · σ 표시 없음 · 본문 "estimated … refined manually" | ✅ 값 · ⚠ "measured" 는 이 편이 쓰지 않은 낱말. ⚠ 02호 식 (1) 의 `F` 누락(02 G9)은 이 편 식 (9) 에서도 `Δφ̃` 가 J/mol 인 "electrochemical potential" 이라 무차원 — 원전은 정합 |
| **27호** Sinzig 2024 ref 14 | "공간전하층 확장의 예" 한 번(27호 digest) | 식 (3) · (10)–(11): 공간전하층을 **분해하지 않고** 평판 축전기 이중층으로 근사(`[인쇄]` "we do not resolve the thickness of the SCL") | ⚠ "확장" 이라기보다 **근사** — SCL 분해 모델은 이 편이 가리키는 ref 33 Braun 2015 · ref 44 Becker-Steinberger 2021 |
| **53호** Ren 2023 [27] | `σ⁰` 8e-4 · `β_GB` 1.39 · `β_tort` 2.31 + "GB resistance and secondary phases in highly porous samples contribute significantly" + "reduce … by more than two orders of magnitude" | 8e-4 · 지수 **0**. "두 자릿수" = 이 편 2.1e-4 → 8.6e-6(×24) 또는 7.69e-4 → 8.6e-6(×89) — 후자면 "two orders" 에 가깝다 | ⚠ **지수는 이 편에 없다 — 파생값**(§6). 문장 요지는 일치 |

---

# 8. 곱 축퇴 처방 — 서른일곱 번째 적용

대상은 카드의 동역학 곱(`A_eff·ε_p/R_s`)이 아니라 **SE 수송의 곱 · 합**(`σ⁰·ε/τ²` + 입계)이다 — 처방의 전 단계를 SE 쪽에 걸어 본다.

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 입계 호 `R`(≈3.74 Ω cm²/계면) · `C_DL^GB` 9.75e-9 — 둘 다 교정 파라미터 | ❌ `C` 가 **두께를 정하지 않는다** — `[재현]` 등가 두께 ≈6.8 µm(§4 ④) |
| **2단계** 면적 대조군 | 공극률 세 시편 — 구조량(`τ` · `A_Spec,SE` · `A_Spec,GB`)을 **계산으로** 공급 | ⚠ 부분 — 입도 · 2차상이 같이 움직인다(교락) |
| **3단계-a** `Ea` | 300 K 하나 | ❌ |
| **3단계-b** `C` 상한 | — | 해당 없음 |
| **4단계** 시간 영역 / 진폭 | 모델 ASR 이 전류에 따라 −38 %(시나리오 1) — 입계 sinh 의 비선형 | ❌(데이터) · 모델에만 |

**곱이 선 자리**: `σ⁰·ε/τ²` 의 곱은 **구조 계산으로 떼어졌다**(✅ — 이 계보에서 수송 곱을 구조로 가른 표본). 남은 것은 `R_bulk(σ⁰)` + `R_GB(d, i₀₀^GB)` 의 **합**, 그리고 그 안의 `d·i₀₀^GB` **곱**.

**⇒ 이 적용이 처방에 더하는 것**:
1. **새 줄 "벌크 특성 주파수 ↔ 측정 대역 상한"** — SE 벌크와 입계(또는 SE 벌크와 계면)의 합을 나누기 전에 `f_C,B = σ/(2πε₀ε_r)` 를 측정 상한과 비교한다. `f_C,B` ≳ 상한이면 **벌크 절편은 관측되지 않고 `σ⁰` 는 추정이 아니라 입력**이다. 이 편: 1.40 × 10⁷ ↔ 1.5 × 10⁷(25 %) · 치밀 `[재현]` 1.84 × 10⁷. 모델 안에서는 절편 이동이 두 파라미터를 가르는데(SI S7 인쇄), 그 채널이 **대역 밖**이다. (49호 "창 규약" 줄의 **위쪽 끝**을 SE 에 적용한 판.)
2. **1단계 `C` 판독의 전제 하나 더** — 교정된 `C` 가 물리적 두께와 10² 배 이상 어긋나면 그 `C` 는 **호 위치 맞춤값**이고 면적 · 두께 서명으로 못 쓴다.
3. **진폭 채널의 SE 판** — 53호 "전류 진폭" 줄(직렬 `R_SP` ↔ `R_CT`)과 같은 구조가 SE 안에 있다: 벌크(옴) ↔ 입계(sinh). 이 편 모델은 그 차를 ASR 표로 보였고(시나리오 1 −38 %) 실험은 소신호 EIS 뿐.

**⚠ 이것이 곱을 푼 것은 아니다** — 구조 계산이 뗀 것은 기하 인자 하나이고, 벌크 ↔ 입계는 원문이 비식별을 인쇄했다. 위 `[재현]` 들은 인쇄값 · 그림 판독 위의 우리 계산이다.

---

# 9. Q1–Q8

- **Q1** 해당 없음 — 양극 없음(Li · Au 대칭). `θ(N)` 0/54. 다공 SE 표면의 **Li 피복**(0–73 %)이 "활성 면적" 역할을 하지만 **그려 넣은 스냅샷**이고(`[인쇄]` "generated based on a visual interpretation of SEM images") 측정 0.
- **Q2** 없음 — 독립 관측 채널 0(재사용 EIS · FIB-SEM). XRD 는 2차상을 못 봤다(`[인쇄]` "below the detection limit").
- **Q3** ★ **층 하나 새로: "재사용 스펙트럼 위 손 보정 · 표 스스로 'calculated'"** — 교정 대상 = 남의 논문(Han 2016)의 치밀 펠릿 한 스펙트럼, 교정 시편 구조 = 가정(15 ± 6 µm 다면체), 교정 방법 = "estimate … refined manually", 표 범례의 "measured by the authors" 칸 0. 이것이 02 · 53호의 입력으로 가면서 "measured" · "similar to those measured in dense pellets" 로 **층위가 올라갔다**(02호 G-절 · 53호 Q3 "계 간 이식" 에 이은 상류).
- **Q4** **0/54 — 마흔여섯 번째 성질 "교정 단계에서 합을 입력으로 나누고, 적용 단계에서 같은 합의 비식별을 인쇄했다"** — 치밀 교정에서는 `σ⁰` 를 문헌 윗끝으로 넣어 합의 분할을 **정했고**, 다공 시편에서는 같은 분할을 "exact deconvolution … unfeasible" 로 **열어 두었다**. 비식별 인쇄는 정직하지만(49호와 달리 결론에서 안 지움 — "and/or"), 교정 단계의 같은 분할에는 적용하지 않았다. 카드의 방향(양극 용량 분할)과 다른 계라 칸은 안 움직인다(누적 0.5 그대로).
- **Q5** 해당 없음 — 3전극 0 · 기준극 0.
- **Q6** 없음 — 셀 압력 0(`MPa` 1 = 문헌 Li 음극 400 MPa).
- **Q7** 해당 없음(Li 금속은 무한 저장소 가정 — `[인쇄]` "the lithium-ion concentration is assumed to be an infinite reservoir").
- **Q8** 해당 없음(OCP 곡선 0 — Li `U₀` = 0).

---

# 10. 채움표 행 (Q1–Q8)

| 논문 | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 |
|---|---|---|---|---|---|---|---|---|
| Neumann · Hamann · Danner · Hein · Becker-Steinberger · Wachsman · Latz 2021 (`assb` 54호 · 큐 55 · LLCZNO SE 자체 · 모델 + 재사용 자료) | 해당 없음(양극 0) | 없음 | **새 층 — 재사용 치밀 펠릿 한 스펙트럼 위 손 보정, 표 "calculated"**; `τ` 는 computed-geometric; `σ⁰` 외부 입력(대역 밖) | **0/54 — 마흔여섯 번째 성질** | 해당 없음 | 없음 | 해당 없음 | 해당 없음 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 11. 어긋남 (실제로 어긋난 것만)

| # | 어긋남 | 무게 |
|---|---|---|
| **D1** | Table S4 `c_Li^SE,0` 설명 "concentration of Li ions in **β-LPS**" — 황화물(Li₃PS₄) 이름, 이 편 SE 는 LLCZNO(황화물 편 Neumann 2020 표에서 옮긴 흔적으로 보임 `[추론]`) | ★ |
| **D2** | Table S4 상수: `F` "9.6485 × 10⁵"(×10) · `R` "m⁻¹ **Rydberg constant** 10.973 × 10⁶" — 기체상수 자리. `[재현]` 계산(`D`)은 올바른 상수로 됨 | ★ |
| **D3** | Table S4 범례의 "measured by the authors [°]" · "[# of REF]" 표시 **0 개**; `i₀₀^Li` 는 본문 "measured by Han et al." 인데 [*]; `σ` 는 표시 없음 | ★★★ (원장 판정 근거) |
| D4 | Fig. 6 범례 `σ_Bulk` "7.67 × 10⁻⁴" ↔ 본문 · 표 7.69 | · |
| D5 | 본문 §4.2.3 · SI S7 "42 and **52**% porosity" · "(b) **52** % porosity" ↔ 그림 · 표 56 % | · |
| **D6** | 본문 "GB charge transfer resistance by **25%**" ↔ SI 스윕 `i₀₀` × 0.75(저항 +33 %) · 42 % 최적 × 0.50(+100 %) | ★ |
| **D7** | 56 % 구조-만 유효 전도도: SI S6 "**7.56 × 10⁻⁵ S/cm²**"(단위도 오기) ↔ 본문 §4.3 "**1.1 × 10⁻⁴**" ↔ `[도표]` Fig. 8 ≈1.07 × 10⁻⁴ | ★ |
| D8 | SI S6 56 % 유효 유전율 "16" ↔ `[재현]` Bruggeman 13.6(0.426) / 14.3(0.434) | · |
| D9 | §4.2.4 "The corresponding parameters are given in Section **3.1**" ↔ 실제 §3.3.4 | · |
| D10 | ref 8 = ref 31(Yang … Hu, PNAS 2018 115, 3770) 중복 | · |
| D11 | SI S7 `A_Spec,SE` "2.18 cm²/cm³" · "0.93 cm²/cm³" — × 10⁴ 누락 | · |
| D12 | 본문 "(∼5.17 × 10⁻⁶ S/cm)" — `[도표]` Fig. 8 56 % 근처 실험점 ≈5.8 × 10⁻⁶(55.5 %) · ≈6.5 × 10⁻⁶(57 %); 5.2 × 10⁻⁶ 근처 점은 ≈**62 %** | ⚠ 판독 |
| D13 | 치밀 교정 시편: 본문 "(≤2% porosity)" · Fig. S4 "Porosity 2%" ↔ SI 본문 "compacted sample (**>99 %**)" | · |
| D14 | 25 % 평균 입도: Table 1 4.62 µm ↔ `[도표]` Fig. S1 가우스 중심 ≈5.0 µm | ⚠ 판독 |
| **D15** | `C_DL^GB` 가 "in the range reported in the literature⁶¹" — Irvine 범위는 셀상수 정규화 F, 이 값은 계면당 F cm⁻²(단위 환산 없는 비교; 환산하면 범위 바닥 · 벌크의 ≈2.2 배) | ★★ |
| D16 | SI S9 "The respective SE current density distribution is given in the main article, **Figure 9**" ↔ 실제 Figure 10 | · |
| D17 | SI S10 "Bode plot … for the **Figure 4 and Figure 6**" ↔ S10.1 공극률(= Fig. 5) · S10.2 2차상(= Fig. 7) | · |
| D18 | 교정 치밀 시편 = 입계 있는 15 µm 다면체 ↔ 삼층 치밀 층 = "no grains and GBs" — 같은 치밀 LLCZNO 에 두 모델 | ★ |
| **D19** | §4.4.1 시나리오 1 ASR "**fluctuates around 1100** Ω cm²" ↔ Table S5 **1064 → 655 단조 감소**(−38 %, 0.1 → 10 mA cm⁻²) | ★★ |
| D20 | `f_C,GB` ≈ 7.0 × 10⁶ Hz ↔ `[재현]` 한 계면 `R·C` 4.4 × 10⁶(계산법 미인쇄) | ⚠ |

---

# 12. 그림 — 무엇을 봤나

크로퍼 **27 장**(본문 그림 12 · 표 1 + SI 그림 9 · 표 5). **Read 9 장**: **Fig. 4 · 5 · 6 · 7 · 8 · S1 · S4 · S5 + 표 S4(표기 확인용)**. 안 본 것: Fig. 1 · 2 · 3(모식 · 구조 렌더) · 9 · 10 · 11 · 12(삼층 — 값은 표 S5 · 본문) · S2 · S3 · S6 · S7 · S8 · S9, 표 1 · S1 · S2 · S3 · S5 는 PDF 텍스트로.
**본문과 어긋난 그림**: Fig. 6 범례 7.67(D4) · Fig. 8 실험점 산포가 "excellent agreement" 보다 넓다(§3.6) · Fig. S1 25 % 중심 ≈5.0 ↔ 표 4.62(D14) · Table S5 단조 감소 ↔ 본문 "fluctuates"(D19, 표). Fig. S4: 실험 호가 모델 벌크 절편(≈28)보다 **낮은 Re(≈12)** 에서 시작 — 벌크 호가 대역 끝에서 잘린 것과 맞는다(저자 서술과 정합).

---

# 13. 참고문헌 중 후속 후보 (66 번호 · SI 18, 서지 기준 — 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Hamann, Zhang, Gong, Godbey, Gritton, McOwen, Hitz, Wachsman 2020** — The Effects of Constriction Factor and Geometric Tortuosity on Li-Ion Transport in Porous Solid-State Li-Ion Electrolytes, *Adv. Funct. Mater.* 30, 1910362 | [30] · SI (1) | ★★★ 이 편 **실험 자료 전부**(FIB-SEM · 차단 EIS · Fig. 8 실험점)의 원전 · 제목이 "협착 인자 ↔ 기하 굴곡도" 분리 — **수송 곱의 실험 쪽 분해** | Q3 · Q4(수송 곱) |
| **Han, Gong, Fu, He, Hitz, Dai, Pearse, Liu, Wang, Rubloff, Mo, Thangadurai, Wachsman, Hu 2016** — Negating interfacial impedance in garnet-based solid-state Li metal batteries, *Nat. Mater.* 16, 572 | [9] · SI (15) | ★★★ `σ⁰` 7.69e-4 · `i₀₀^Li` · 입계 교정 스펙트럼(Fig. S4)의 원전 — **`σ⁰` 벌크 몫을 어떻게 뗐는가** | Q3 |
| Fleig, Maier 1999 — The impedance of ceramics with highly resistive grain boundaries: Validity and limits of the brick layer model, *J. Eur. Ceram. Soc.* 19, 693 | [63] | ★★ 벽돌층 `C` → 입계 두께 해석의 한계 — §4 ④ 의 기준 | 곱(C 채널) |
| Irvine, Sinclair, West 1990 — Electroceramics: Characterization by Impedance Spectroscopy, *Adv. Mater.* 2, 132 | [61] | ★ `C` 범위표의 원전(D15) | 곱(C 채널) |
| Hein, Danner, …, Schmidt, Latz 2020 — Influence of Conductive Additives and Binder on the Impedance of Lithium-Ion Battery Electrodes: Effect of Morphology, *JES* 167, 013546 | [34] | ★ BEST 임피던스 모의(계단 여기) 방법 원전 | 도구 |
| Hitz, McOwen, …, Wachsman 2019 — High-rate lithium cycling in a scalable trilayer Li-garnet-electrolyte architecture, *Mater. Today* 22, 50 | [7] | 삼층 실험 · ASR ≈7 Ω cm² · 10 mA cm⁻² | 칸 밖 |
| Yu, Siegel 2017 — Grain Boundary Contributions to Li-Ion Transport in the Solid Electrolyte LLZO, *Chem. Mater.* 29, 9639 | [28] · SI (13) | 입계 원자 규모 장벽 — `γ‡_GB` 의 이론 입력 후보 | 칸 밖 |
| Braun, Yada, Latz 2015 *JPCC* 119, 22281 · Becker-Steinberger, Schardt, Horstmann, Latz 2021 arXiv:2101.10294 | [33] · [44] | 공간전하층 분해 모델(27호가 가리킨 "확장" 의 실체) | 칸 밖 |
| Neumann, Randau, …, Janek, Latz 2020 *ACS AMI* 12, 9277 | [37] | 이미 원장 행(접촉 → 활성 면적) — D1 표 설명의 출처 추정 | Q1 · 곱 |

**큐 56–59 대조**: 56 Hlushkou 2018 **❌ 인용 0**(같은 *JPS* 396 권의 ref 21 Taylor 2018 은 다른 편) · 57 Bielefeld 2022 ❌ · 58 Bielefeld 2020 ❌ · 59 Asheri 2023 ❌(이 편보다 늦다). **이 편은 큐 56–59 어느 것도 인용하지 않는다.**

---

# 14. 이 digest 가 주장하지 않는 것

- **입계가 지배한다는 결론이 틀렸다고 하지 않는다.** 주장은 **그 분할이 입력 `σ⁰` 가 정한 것이고, 교정 데이터는 그 분할을 보지 못했다**는 것까지다(대역 밖 절편 — 저자 자신의 "not fully resolved").
- **53호의 `β_GB` 1.39 가 틀렸다고 하지 않는다** — 1.39 를 이 편 수치에서 정확히 재현하지 못했고, 근처 값을 주는 유일한 읽기(치밀 전 모형 정규화)에서 `σ⁰` 의 뜻이 어긋난다는 것까지가 우리 계산이다. 53호 SI 는 도출을 적지 않았다.
- **`C_DL^GB` 의 등가 두께 6.8 µm 를 이 편의 주장으로 적지 않는다** — 벽돌층 · ε_r 75 · 15 µm 간격 가정 위의 우리 계산이다. 저자는 이 값을 공간전하층 용량으로 부른다.
- **시나리오 1 ASR 의 전류 의존을 입계 sinh 로 단정하지 않는다** — 모델 식에서 비선형 원소가 둘(입계 · Li 계면)뿐이라는 것과 국소 전류 크기에서 나온 해석이다.
- **Fig. 8 "excellent agreement" 를 반박하지 않는다** — 실험 산포(×≈7)와 호 선택(§0 의 5 번)이 판정 해상도를 정한다는 것까지.
- 원문 인용 원전(Han 2016 · Hamann 2020 등)은 **열람하지 않았다**.

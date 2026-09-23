---
title: "Yanev, Auer, Pertsch, Heubner, Nikolowski, Partsch, Michaelis 2024 — Quantifying Resistive and Diffusive Kinetic Limitations of Thiophosphate Composite Cathodes in All-Solid-State Batteries (J. Electrochem. Soc. 171, 050530)"
source_url: local-upload/28._Quantifying_Resistive_and_Diffusive_Kinetic_Limitations_of_Thiophosphate_Composite_Cathodes_in_All-Solid-State_Batteries.pdf
source_url_note: "11쪽(IOP 표지 1 + 본문 10, 참고문헌 57편). SI 는 업로드에 없다(Table S1·S2, Fig. S1–S8 미열람 — IOP 접근은 프록시 정책상 차단). 크로퍼 7장 전부 직접 봤다, 안 본 그림 0장(+ 식 1–5 300 dpi 렌더 · Fig. 2c/2d 확대). 17호(Yanev 2024 JES 171 020512)와 같은 연구실 — 이 편의 ref 21. PDF 는 커밋하지 않는다."
source_doi: 10.1149/1945-7111/ad47d7
source_license: "CC BY 4.0, (c) 2024 The Author(s). Published on behalf of The Electrochemical Society by IOP Publishing Limited — Open Access"
pdf_sha256: c0fc33c717c166349a1002b2c2d51685789cdd6562e336b358cdfda5e389b1ca
ingested: 2026-09-23
sha256: 7a0836eba5a52829279f51654c1763f4d1b0c630cc9e58e0c56b13986b867f86
---

# 수집 목적

`assb` 섹션 **29호**. 큐 **28번** (28호 = 큐 27 Bizeray 2019, 27호 = 큐 26 Sinzig 2024). 닻은 `questions/assb-contact-loss-vs-lampe.md`.
큐 문서(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3)의 등록 축은 **"★ `η(i)` 항 그 자체 + OCV 곡선 최유력"** 이고, 25~29 낱말 지문 표는 이 편을
`identifiab` **0** · `uniqu` **0** · `sensitiv` — · `Sobol` — · `GITT` **20** · `OCV` **0** 으로 적었다.

⚠ **저자가 17호와 같다.** Yanev · Auer · Pertsch · Heubner · Nikolowski · Partsch · Michaelis (Fraunhofer IKTS Dresden + TU Dresden). 17호(Yanev 2024 *JES* 171, 020512, Li-In 음극 동역학)가
이 편의 **ref 21** 이고, 이 편의 음극 복합체(40 at% Li, 40 wt% SE)는 17호가 3전극으로 검증한 바로 그 조성이다(§9). 방법의 앞선 ASSB 판은 ref 20 (Yanev 2022 *JES* 169, 090519) — 이번 업로드에 없다.

**원문 11 쪽(IOP 표지 1 + 본문 10)을 전수로 다시 셌다.** IOP 조판이고 `ﬁ`(U+FB01) **99 개** · `ﬂ`(U+FB02) **17 개**의 합자를 쓴다. 지문은 **NFKC 정규화 뒤** 센다(27·28호 맹점).

| 낱말 | 추출 그대로 | **NFKC 뒤** | 비고 |
|---|---:|---:|---|
| `identifiab` | 0 | **0** | 합자 맹점과 무관하게 **진짜 0** |
| `identif*` | 1 | 4 | 정규화로 +3 — 전부 일상어("identified as effective ways" · "identification of the kinetic bottleneck" · "identify the performance bottleneck" · "identified as a major goal") |
| `uniqu` | 0 | 0 | |
| `fit*` (낱말 머리) | **0** | **20** | ★ 합자로 0 이 되는 낱말 — 이 편의 방법 절 전체가 "ﬁt" 이다. 28호에 이어 두 번째로 크게 변한 낱말 |
| `dependenc*` | 2 | 2 | ★★ **둘 다 적합 공분산 진단**("All parameter values and their dependencies are additionally shown in Table S2" · "high dependencies close to unity in Table S2") |
| `sensitiv*` | 1 | 1 | 일상어("utilization of sc AM is much more sensitive to changes in the AM ratio") |
| `Sobol` · `Fisher` · `covarian*` · `confidence` · `uncertaint*` · `error bar` · `standard deviation` · `reproducib*` | 0 | 0 | |
| `correlat*` | 3 | 3 | 전부 정성("correlate with n values approaching 1") — 상관계수 수치 0 |
| `GITT` | 20 | 20 | 큐 지문과 같다 |
| `OCV` | 0 | 0 | 큐 지문과 같다. `open circuit` 1(초기 4 h 휴지) · `equilib*` 1(같은 문장) — **OCV 곡선은 지면에 없다** |
| `contact` | 23 | 23 | `contact area` 5 · `contact surface` 6 · `contact loss*` 2 |
| `percolat*` · `utiliz*` | 15 · 14 | 같음 | Q_M 해석의 두 낱말 |
| `crack*` | 11 | 11 | |
| `tortuos*` · `porosit*` | 3 · 4 | 같음 | |
| `pressure` | 5 | 5 | 스택 ca. 50 MPa 2 · BET 상대압 1 · 서술 2 |
| `LAM` · `LLI` (대소문자 구분 낱말) | 0 · 0 | 0 · 0 | ⚠ 대소문자 무시로 세면 `LLI` 18 · `LAM` 5 가 나온다 — "ba**ll**-m**i**lled" 류 오검출. **대소문자 구분 + 낱말 경계로 센다** |
| `degrad*` · `aging` | 4 · 0 | 같음 | 전부 기계적 열화 서술 · 열화 데이터 0 |
| `indium` · `Li-In` · `LiIn` · `0.62` | 2 · 3 · 1 · 0 | 같음 | 기준 전위 **숫자 0.62 는 지면에 없다** — 2.38–3.68 V vs Li⁺/LiIn ↔ 3.00–4.30 V vs Li⁺/Li 의 병기로만 있다(ref 23 Santhosha 2019) |
| `reference electrode` · `three-electrode` | 0 | 0 | 2전극 |

⇒ 큐 지문은 **정규화 전후로 다 맞았다**(`identifiab` 0 · `OCV` 0 · `GITT` 20). 정규화가 바꾼 것은 `fit` 0 → 20 과 `identif*` 1 → 4 이고, **식별성 신호는 낱말 지문이 아니라 `dependenc*` 2 에 있었다** — 지문 표의 열에 없는 낱말이다.
큐 메모의 우려("GITT 로 재면서 'OCV 곡선' 이라 부르지 않을 수 있다")는 **반만 맞다**: GITT 는 SOC 30–70 % 다섯 점의 **확산계수**를 위해서만 쓰였고, 준평형 전위(`ΔE_S`) 값도 곡선도 인쇄되지 않는다.

> ★★★★ **Q1·Q4 판정을 먼저 적는다.**
> 1. **이 편은 용량을 둘로 나눈다 — 정적(`Q_M`, 무한 저율 외삽 용량 = "AM utilization") ↔ 동적(`α`·`n`, 율 의존 감쇠).** 그리고 동적 쪽을 다시 둘로 나눈다 — **저항성(SE 쪽, `n → 1`, `σ_eff`) ↔ 확산성(AM 쪽, `n → 0.5`, GITT `D_Li⁺`)**.
>    카드의 3항 분해로 옮기면 `Q_M` 은 **`θ_el`(전자 비연결) + 기계 손상 + 물질 고유 용량**의 합이고, `α`·`n` 은 **`η(i)`** 다. 그러니까 **"비연결 분율 ↔ 동역학적으로 접근 못 한 용량"은 가른다.**
> 2. **가르는 방식은 측정이 아니라 적합 외삽이고, 그 한계는 저자가 스스로 인쇄했다.** 식 (2) `Q(R) = Q_M / (1 + 2(Rα)ⁿ)` 는 고율 극한에서 `(Q_M/2)(Rα)⁻ⁿ` 가 되어 데이터가 `Q_M·α⁻ⁿ` **한 조합**만 본다(`[재현]` 식 2 대수).
>    `[인쇄]` sc90 은 저율 평탄이 측정 창(0.02 C) 안에 없어 "there is not enough information in the measured data to accurately fit the Q_M and α parameters, which is reflected by their **high dependencies close to unity in Table S2**." — **적합 공분산 진단(OriginPro "dependency")으로 `Q_M` ↔ `α` 비식별을 판정한 명제**다.
> 3. ★★★★ **Q4 — ASSB 계보 첫 반 칸으로 올린다 (0/28 → 0.5, 29호).** 근거가 **논문 명제 + 저자가 돌린 진단**이다(26·28호처럼 우리 `[재현]` 이 아니다).
>    26호 개념 페이지의 세 줄 표로는 **둘째 줄(추정 민감도 — 추정 데이터 위 `J` 의 평행 열)에 수치 진단을 붙인 계보 첫 편**이고, 식별 집합에 **용량 스케일 `Q_M` 이 들어 있다**(28호의 `Q_th` 는 입력으로 빠졌다).
>    **반 칸인 이유 넷**: ① 진단 값은 **SI Table S2** 에 있고 SI 는 업로드에 없다(IOP 접근도 정책상 차단) — 본문 명제만 봤다 ② 국소 공분산 하나, 폭·프로파일·CI 0 ③ 그 축은 **정적 ↔ 동적**이지 카드의 **`LAM_PE` ↔ 접촉**이 아니다(`Q_M` 이 둘을 합친다) ④ ★ **저자가 자기 진단을 해석에 전파하지 않는다** — Fig. 4 는 sc90 의 `Q_M`·`α` 를 표시 없이 그리고(`[도표]` ≈60 mAh g⁻¹ · ≈2.2 h), 논문의 이용률 결론 중 가장 센 것(**"`Q_M` 최대는 sc84, LIB 기준 용량보다 높다"**)은 `[인쇄]` "the low-rate plateau of sc84 is not clearly visible" 인 **바로 그 외삽 영역**에서 나왔다(§5·§10 D7).
> 4. **Q1 — 칸 이동 없음. `θ(N)` 0/29.** 접촉량 둘이 조성마다 수치로 나온다 — `Q_M`(전자 이용률) 14 점 · `φ`(AM 표면의 SE 피복률, `[인쇄]` 53.3 → 18.0 % · 85.2 → 3.1 %) 14 점. 그러나 **둘 다 역산**이다:
>    `Q_M` 은 용량에서, `φ` 는 `φ = √(D_ASSB/D_LIB)` 로 **"진짜 `D` 는 LIB 와 같다 · LIB 피복률 = 100 %"** 두 가정 위에서. 22호의 기준(용량 밖 구조 측정)에 못 미친다. 신품(형성 2 사이클)이라 노화 축도 0.
> 5. **곱 축퇴 처방 열두 번째 적용** — 이 편의 GITT 가 곱 자체다: 식 (3) 에서 `D_app ∝ 1/A²` 이므로 **데이터가 보는 것은 `D·(A_eff/A_BET)²`** 이고, 저자는 **같은 분말의 액체 반쪽전지 `D_LIB` 를 수입해** 한 인자를 고정했다. 처방 첫 줄 **"율 스윕(`i → 0` 포함)"** 의 계보 첫 실적용이기도 하다 — 그리고 그 줄의 **실패 조건**(평탄이 창 밖이면 `θ·Q` 와 `η` 가 한 조합)을 저자 진단이 인쇄했다.

# 판정 한 줄

**카드 물음의 "정적 ↔ 동적" 절반을 적합 외삽으로 가르고, 그 외삽이 언제 실패하는지를 저자의 공분산 진단이 인쇄한 첫 ASSB 편 — 그러나 가장 센 이용률 주장은 진단이 경고한 영역에서 나왔고, "접촉 면적 ↔ 고체 확산" 절반은 측정이 아니라 액체 기준 수입(가정)으로 갈랐다.**
이 편에서 "확산성 한계"(`D_app` ↓)와 "작은 접촉 면적"(`φ` ↓)은 **같은 숫자의 두 이름**이다(`φ ≡ √(D_app/D_LIB)` — 정의상 항등).

---

# 0. 원문에 없어서 확인이 필요한 것 (공백)

- **SI 전체가 없다.** 업로드는 본문 PDF 하나. 본문이 가리키는 **Table S1(조성) · Table S2(적합값과 dependency) · Fig. S1(TLM 스펙트럼·회로) · S2–S4(SEM·입도·전자 전도도) · S5(SE 차단 EIS) · S6(형성 CCCV 곡선) · S7(나머지 적합) · S8(`τ`·`φ` 그림)** 을 못 봤다.
  ⇒ `dependency` **수치 0**, 적합 `Q_M`·`α`·`n` 은 **그림 판독**(Fig. 4)만, 형성 곡선(= 이 편에서 OCV 에 가장 가까운 것) **0**.
- **적합 오차·신뢰구간 0.** Fig. 4 에 오차막대 없음. 셀 **조건당 1 개**로 보인다(반복 서술 0).
- **CA 방전 전위 "3.0 V" 의 기준이 안 적혔다.** 전압창은 2.38–3.68 V vs Li⁺/LiIn(= 3.00–4.30 V vs Li⁺/Li). `[해석]` 3.0 V vs Li⁺/Li(= 2.38 V 셀) 로 읽는 것이 맞다 — 17호 Fig. 4d 의 CA 가 `E_cell` 2.38 V 고정이었다.
- **"nominal capacity of the AM"(C-rate 기준) 값이 없다.** 공칭 면적 용량 2.80 mAh cm⁻² 만 있다.
- **LIB 기준 셀의 전압창·온도·율 범위가 없다.** `Q_LIB` 는 **0.1 C 한 점**(193 · 213 mAh g⁻¹), `D_LIB` 는 GITT 조건 미기재.
- **공극률 측정 0.** 식 (4) 의 `ε` 는 "volume fraction of the catholyte" — 조성에서 온 공칭값으로 보인다(§4-1 `[재현]`).
- **GITT 의 `ΔE_S` · `dE/d√t` 값, 5 SOC 점의 산포 0.** "quasi-constant" 라 평균만 보고.
- **열화 0.** 형성 2 사이클 뒤 한 번의 CA. `LAM`·`LLI`·`aging` 0 회.

---

# 1. 서지·셀 사양

| 항목 | 값 |
|---|---|
| 서지 | S. Yanev, H. Auer, R. Pertsch, C. Heubner, K. Nikolowski, M. Partsch, A. Michaelis, "Quantifying Resistive and Diffusive Kinetic Limitations of Thiophosphate Composite Cathodes in All-Solid-State Batteries", *J. Electrochem. Soc.* **171** (2024) 050530, doi 10.1149/1945-7111/ad47d7 |
| 접수·게재 | 2024-03-19 접수 · 04-29 수정 · 05-16 게재. **Open Access, CC BY 4.0** |
| 소속 | Fraunhofer IKTS Dresden (전원) + TU Dresden (Michaelis) |
| 연구비 | "MaLiFest"(Lower Saxony) · "FB2-Oxid"(BMBF 03XP0434B) |
| 활물질 | NCM811 두 형상 — **gran**(다결정 2차 입자, Targray, `[인쇄]` 평균 10 µm, BET 0.570 m² g⁻¹, 전자 전도도 15.7 mS cm⁻¹) · **sc**(단결정 LiNi0.83Co0.11Mn0.06O2, MSE Supplies, 1차 ca. 1 µm · 응집 ca. 4 µm, BET 0.696, 14.5 mS cm⁻¹) |
| 고체전해질 | Li₆PS₅Cl (NEI) **그대로**(BET 2.25 m² g⁻¹, 3.13 mS cm⁻¹ @30 °C, >20 µm 입자 섞임) · **습식 볼밀 LPSCl-BM**(p-xylene, 200 rpm 4 × 30 min, ≈2 µm, BET 8.36, **1.62 mS cm⁻¹** — 부분 비정질화) |
| 도전재 | VGCF **5 vol% 고정** |
| 조성 | AM **51.0 · 73.2 · 84.0 · 89.5 wt%** × {gran, sc, gran-BM, sc-BM} — BM 은 73–90 만 ⇒ **14 복합체** |
| 음극 | Li-In-SE 복합(40 at% Li, SE 40 wt%, ref 21 = 17호) 80 mg |
| 셀 | ∅10 mm PET 몰드 + SUS 피스톤(Hohsen KP). 분리막 LPSCl 150 mg @500 MPa 1 min → 음극 @500 MPa 1 min → 양극 12.3–21.5 mg @**500 MPa 5 min**. 공칭 **2.80 mAh cm⁻²** 고정 |
| 운전 | **30 °C · 스택 ca. 50 MPa** · 2.38–3.68 V vs Li⁺/LiIn |
| 프로토콜 | 4 h OCV 휴지 → 형성 2 × (0.1 C CCCV 충전, 0.02 C 종료 / CC 방전) → CCCV 충전 → **CA 방전(3.0 V) — 전류가 0.02 C 로 떨어질 때까지** |
| 대칭 셀 | 양극 40 mg × 2 + LPSCl 150 mg 분리막, EIS 1 MHz–10 mHz, 25 mV, **TLM 적합**(RelaxIS, ref 9 Minnmann · 22 Kaiser) → `σ_eff` |
| GITT | 별도 셀. 형성 후 0.033 C 로 SOC 30 % → 4 h 휴지 → **0.04 C 10 min 펄스** → 4 h → +10 % … SOC 30·40·50·60·70 % 다섯 점 평균 |
| LIB 기준 | AM:C65:PVDF 77:11.5:11.5, Al 박, 1 M LiPF₆ EC:DEC, Li 금속, 2032 코인 — `Q_LIB`(0.1 C) · `D_LIB`(GITT) |
| 기타 | FESEM(이온 밀링, Zeiss Crossbeam 550) · BET(5 점, 0.06–0.2) |

---

# 2. 방법 — 식 다섯 (300 dpi 렌더로 확인)

| 식 | `[인쇄]` | 뜻 |
|---|---|---|
| (1) | `R(t) = I(t) / ∫₀ᵗ I(t′)dt′` | CA 과도 전류를 "율" 로 바꾼다. 원출처 Tian 2020 (ref 19) |
| (2) | `Q(R) = Q_M / (1 + 2(Rα)ⁿ)` | **3 파라미터 경험식**. `Q_M` = 무한 저율 용량("maximum capacity which can be discharged at an infinitely low rate") · `α` = 급감 개시("onset rate", 단위 h) · `n` = 감쇠 기울기 |
| (3) | `D = (4/π)(m·V_M/(M·A))² · (ΔE_S/(t_GITT·dE/d√t))²` | Weppner–Huggins 단시간 형(ref 24). **`A` = BET 면적으로 가정** |
| (4) | `τ = (σ₀/σ_eff)·ε` | 굴곡도 **인자**(ref 22 Kaiser). `σ₀` = 순수 SE 벌크, `ε` = catholyte 부피분율 |
| (5) | `φ = √(D_Li⁺ / D_Li⁺^LIB)` | AM 표면의 SE 피복률. **LIB 피복률 = 100 % 로 정규화** |

`[인쇄]` `n` 의 해석: "n values of 0.5 are associated with diffusive kinetic limitations, whereas n values of 1.0 are associated with resistive kinetic limitations" — 근거는 ref 19(Tian 2020)·20(Yanev 2022). **이 편에서 새로 보이지 않는다.**

`[인쇄]` 저항성 = SE 쪽: "Li⁺ transport in the SE can be described as purely electric field-driven migration with no significant macroscopic diffusion … the ionic conductivity is considered the **only** relevant Li⁺ transport descriptor in the SE." 확산성 = AM 쪽: "composites showing diffusively limited kinetics (n ∼0.5) are associated with a diffusive Li⁺ transport bottleneck within the NCM811 particles."
`[인쇄]` 전자 수송은 배제("unlikely that the electron transport can act as a kinetic bottleneck"), SE|AM 계면 분해층은 "constant in all our cells" 로 **가정**.

---

# 3. 결과 — 절별 · 그림별

## 3-1. Fig. 1 — 분말 FESEM (본 그림)
`[도표]` gran: 구형 2차 입자, 몇 개에 균열 · sc: 1–2 µm 판상 결정 + 응집 · LPSCl: 수십 µm 판 조각 + 미세 분말 혼재 · LPSCl-BM: 수 µm 이하로 균질. 캡션·본문과 어긋남 없음. **복합체 단면 SEM 은 없다**(피복률을 영상으로 확인한 그림 0).

## 3-2. Fig. 2 — CA 율 성능 (본 그림, 4 판, x = 공칭 C-rate 로그 0.01–50, y = 0–240 mAh g⁻¹)
`[도표]` 0.02 C 끝값: gran51 ≈194 · gran73 ≈172 · gran84 ≈174 · gran90 ≈147 | sc51 ≈195 · **sc73 ≈211** · sc84 ≈177 · sc90 ≈26 | gran73-BM ≈173 · gran84-BM ≈173 · gran90-BM ≈147 | sc73-BM ≈175 · **sc84-BM ≈205** · sc90-BM ≈132(곡선이 ≈0.027 C 에서 끝남).
`[인쇄]` 서술과 대조:
- "gran … low-rate capacity 51 % > 73 % ≈ 84 % > 90 %" ✓
- "sc84 … (177 mAh g⁻¹) only at the lowest studied rate … The low-rate plateau of sc84 is **not clearly visible**" ✓ — `[도표]` 0.02 C 에서도 기울기가 남아 있다
- "sc90 … yielding only 25 mAh g⁻¹" ✓(≈26) · "gran90 … 2 C close to zero" ✓ · "gran90 provides only 25 mAh g⁻¹ at 1 C" ✓
- "gran90-BM provides **73** mAh g⁻¹ at 1 C" — `[도표]` 확대 판독 **≈80** ⚠ (D2)
- "sc90 … 14 mAh g⁻¹ at 0.1 C" ✓ · "sc90-BM provides 92 mAh g⁻¹ at 0.1 C" ✓
- "sc84-BM shows a significantly higher low-rate capacity than sc73-BM (**175 and 195** mAh g⁻¹ respectively)" — ⚠⚠ **숫자 순서가 이름과 반대**이고(그대로 읽으면 sc84-BM 175 < sc73-BM 195 로 문장과 모순), 그림은 **sc84-BM ≈205 · sc73-BM ≈175** (D1)
- ⚠ **gran51 에도 "평탄" 은 없다** — `[도표]` 0.1 → 0.02 C 에서 ≈180 → ≈194 로 계속 오른다. 모든 곡선이 로그 축 끝까지 기울어 있다.

## 3-3. Fig. 3 — `Q(R)` 적합 예시 (본 그림; 크로퍼가 Fig. 2 까지 한 장에 잡았다)
`[도표]` log–log, `R` 0.001–1000 h⁻¹. gran 네 셀의 데이터(삼각형)는 **`R` ≈0.02–0.03 에서 시작해 ≈1000 h⁻¹ 까지** — 고율 쪽은 **CA 시작 직후 초 단위 구간**이다(`R` → ∞ 는 `t` → 0). 적합 곡선은 `R` 0.001 까지 수평으로 **외삽**되어 그려져 있다.
고율 꼬리는 네 셀 모두 **거의 같은 기울기의 직선**(`n` ≈0.8–1.0).

## 3-4. Fig. 4 — 적합 파라미터 (본 그림, 세 층 `n` / `α`(log) / `Q_M`)
`[도표]` 판독(±0.02 · 로그 반 칸 · ±5 mAh g⁻¹):

| | `n` | `α` / h | `Q_M` / mAh g⁻¹ | 0.02 C 실측 (Fig. 2) |
|---|---:|---:|---:|---:|
| gran51 | 1.00 | 0.05 | ≈185 | ≈194 |
| sc51 | **1.03** | 0.035 | ≈189 | ≈195 |
| gran73 | 0.96 | 0.065 | ≈166 | ≈172 |
| gran73-BM | 0.98 | 0.054 | ≈166 | ≈173 |
| sc73 | 0.90 | 0.057 | ≈207 | ≈211 |
| sc73-BM | 1.00 | 0.039 | ≈170 | ≈175 |
| gran84 | 0.97 | 0.12 | ≈170 | ≈174 |
| gran84-BM | 0.965 | 0.07 | ≈168 | ≈173 |
| **sc84** | 0.565 | 1.4 | **≈236** | **≈177** |
| sc84-BM | 0.84 | 0.12 | ≈208 | ≈205 |
| gran90 | 0.785 | 0.45 (`[인쇄]` 0.45) | ≈159 | ≈147 |
| gran90-BM | 0.86 | 0.14 (`[인쇄]` 0.14) | ≈148 | ≈147 |
| **sc90** | **0.41** | **≈2.2** | **≈60** | ≈26 |
| sc90-BM | 0.615 | 1.35 | ≈179 | ≈132 (0.027 C) |

`[도표]` 읽은 것 셋:
1. ★★★ **sc90 의 `Q_M`·`α` 가 다른 점과 같은 기호로 그려져 있다** — 본문은 "not enough information … to accurately fit the Q_M and α" 라 했다. 그림에는 표시·주석이 없다(D9).
2. ★★★★ **sc84 `Q_M` ≈236 은 실측 최대(0.02 C ≈177)보다 ≈+33 % 위의 외삽값**이고, `[인쇄]` "even exceeding the reference LIB capacity at sc84"(213 대비 ≈111 %) 의 근거다. `[재현]` 판독값으로 식 (2) 를 `R` ≈0.028 에 넣으면 `(Rα)ⁿ` = (0.039)^0.565 ≈0.16 → `Q` ≈236/1.32 ≈179 — **적합은 데이터 끝에서도 `Q_M` 의 76 % 에 있다.** 즉 `Q_M` 은 측정 창 밖으로 **곡선 모양만으로** 뻗은 값이다.
3. ★★ **잘 거동하는 셀에서는 거꾸로 `Q_M` 이 실측 저율 용량보다 낮다** — gran51 ≈185 < 194, sc51 ≈189 < 195, sc73 ≈207 < 211(D6). "무한 저율 최대 용량" 이라는 정의와 반대 방향이다. `[해석]` 식 (2) 의 저율 쪽은 `Q_M` 으로 빨리 수렴하는데 데이터는 로그 축 끝까지 기울어 있어서(§3-2), 적합이 평탄을 **낮게** 잡는다. ⇒ `Q_M` 은 평탄이 보이면 **과소**, 안 보이면 **과대**(sc84) — 두 방향 모두 식 모양이 데이터 모양과 다른 데서 온다.

`n` 의 범위: `[도표]` sc51 **1.03** · sc90 **0.41** — 해석 범위 [0.5, 1] 밖이 둘(D8). 저자는 이 둘을 논의하지 않는다.

## 3-5. `Q_M` 의 해석 — 저자 서술 (본문 p.6)
- `[인쇄]` "The low-rate capacity is therefore an indicator of the **degree of electronically percolated AM**, referred to as AM utilization." — **용량 결손 ≡ 전자 비연결** 을 정의로 인쇄한다(열화 0 이라 진짜 LAM 항이 없다).
- `[인쇄]` 물질 고유 차이는 LIB 기준으로 뗀다: gran 193 · sc 213 mAh g⁻¹ @0.1 C — "reflects intrinsic differences in the AMs which might come from differing production process". ⇒ **`Q_M / Q_LIB` = 이용률** 이라는 구조(카드의 `θ` ↔ 물질 용량 분리의 신품판).
- 두 반대 효과: AM 비 ↑ → 전자 퍼콜레이션 ↑(ref 28 = **1호 Bielefeld 2019**) · AM–AM 경접촉 ↑ → 균열 → `[인쇄]` "Damaged AM particles are likely to detach form the electronic percolation network and remain unutilized"(ref 20). "We believe that mechanical degradation … is the primary reason for the declining capacity trend of the gran AM" — **측정 0, 믿음**.
- `[인쇄]` sc-BM: "sc73-BM and sc84-BM both show lower Q_M than their sc73 and sc84 counterparts … explained by a partial enveloping of AM … by electronically insulating SE shells." ⚠⚠ sc84 쌍은 **실측 0.02 C 용량 순서가 반대**다(sc84 ≈177 < sc84-BM ≈205). 순서를 뒤집는 것은 sc84 의 외삽 `Q_M` 뿐이다(§10 D7).
- `[인쇄]` VGCF: "the electronic percolation network generated the AM particles themselves is still the dominant factor for the utilization, despite using VGCF" — VGCF 없는 대조 셀 0.

## 3-6. Fig. 5 — 모식도 (본 그림)
분리막은 수직 "Li⁺ conduction", 양극 확대창은 SE→AM 경계에서 "Li⁺ diffusion". 데이터 없음. **음극은 회색 판 하나** — 음극 기여는 그림에도 본문에도 없다(§9).

## 3-7. Fig. 6 · Table I — `σ_eff` · `D_Li⁺` · `τ` · `φ` (본 그림 + 표 전사)

`[인쇄]` Table I (sc90 `σ_eff`·`τ` 는 "could not be accurately determined"):

| 셀 | `σ_eff` / S cm⁻¹ | `τ` | `D_Li⁺` / cm² s⁻¹ | `φ` / % |
|---|---:|---:|---:|---:|
| gran51 | 1.18·10⁻³ | 1.5 | 1.76·10⁻¹² | 53.3 |
| gran73 | 3.10·10⁻⁴ | 3.7 | 1.57·10⁻¹² | 50.3 |
| gran84 | 7.09·10⁻⁵ | 10.3 | 1.11·10⁻¹² | 42.3 |
| gran90 | 1.73·10⁻⁵ | 27.6 | 2.00·10⁻¹³ | 18.0 |
| gran73-BM | 3.60·10⁻⁴ | 1.7 | 2.14·10⁻¹² | 58.6 |
| gran84-BM | 8.71·10⁻⁵ | 4.4 | 1.40·10⁻¹² | 47.5 |
| gran90-BM | 2.25·10⁻⁵ | 11.1 | 5.69·10⁻¹³ | 30.2 |
| sc51 | 1.12·10⁻³ | 1.6 | 1.68·10⁻¹² | 85.2 |
| sc73 | 1.29·10⁻⁴ | 8.9 | 1.11·10⁻¹² | 69.3 |
| sc84 | 2.88·10⁻⁵ | 25.4 | 1.12·10⁻¹³ | 22.0 |
| sc90 | — | — | 2.29·10⁻¹⁵ | 3.1 |
| sc73-BM | 2.03·10⁻⁴ | 2.6 | 1.29·10⁻¹² | 70.8 |
| sc84-BM | 4.88·10⁻⁵ | 7.8 | 3.05·10⁻¹³ | 36.3 |
| sc90-BM | 4.60·10⁻⁶ | 54.2 | 1.16·10⁻¹⁴ | 7.1 |

`[인쇄]` `D_LIB` = **6.21·10⁻¹²**(gran) · **2.31·10⁻¹²**(sc) cm² s⁻¹ — 같은 조성인데 **2.7 배**. 저자: "this apparent difference **must be caused by morphological effects**. Even in LIBs, assuming A (Eq. 3) as equal to the BET surface does not accurately describe the effective surface area available for diffusion."
`[도표]` Fig. 6 은 표와 대부분 맞는다. ⚠ **sc84 `D` 는 그림에서 ≈8–8.5·10⁻¹⁴**(10⁻¹³ 격자선 **아래**) — 표 1.12·10⁻¹³ 과 다르다; Fig. 7b 의 sc84 점도 ≈8·10⁻¹⁴ 에 있다(D3). 표의 `φ` 22.0 은 표의 `D` 와 맞으므로(`[재현]`), 그림이 다른 값으로 그려졌다.

## 3-8. Fig. 7 — `α`·`n` 대 `σ_eff`·`D` (본 그림, 네 판)
- (a) `α` vs `σ_eff`: 네 계열이 **따로** 놓인다. `[인쇄]` "diminishing returns … as σ_eff exceeds 10⁻³ S cm⁻¹" — 10⁻³ 위의 점은 51 % 두 개뿐이다.
- (b) `α` vs `D`: 파란 파선 하나 근처에 모인다. `[인쇄]` "The data points can be reasonably described as falling on a **master line**" — 캡션: "The blue lines are a **guide to the eye only**." **회귀·잔차·상관계수 0.**
- (c) `n` vs `σ_eff`: `σ_eff` 가 클수록 `n` → 1. `[인쇄]` "which seems contradictory at first. Therefore, resistive effects alone can not be responsible".
- (d) `n` vs `D`: 파선 위. **맨 아래 점(`D` ≈2.3·10⁻¹⁵, `n` ≈0.41)이 sc90** — 범례 "usc (51–90 %)"(a–c 는 "sc (51–84 %)").
- 범례 표기 "ugran/usc" (그림 4·7) — 본문 이름과 다름(D10, 외형).

## 3-9. 결론 (본문 p.9–10)
`[인쇄]` "the solid-state diffusion of Li⁺ within the AM is often limiting to the overall cathode rate performance … especially … single crystal NCM811 and at high AM ratios (>84 %). The diffusive limitation is associated with a **small AM-SE contact surface**, whereby diffusive transport is only initiated at discrete point contacts." · "roughly an order of magnitude lower than that of comparable reference LIBs" · "Reducing the solid electrolyte particle size is shown to improve the AM-SE contact area".
`[인쇄]` 범위 명제: "The methods and principles used in this work are **generally applicable** for ASSB cathodes."

---

# 4. `[재현]` 우리가 한 계산

## 4-1. 식 (4) 로 `ε` 역산 — 공칭값이고, sc73-BM 행이 안 맞는다
`ε = τ·σ_eff/σ₀` (`σ₀` = 3.13 mS cm⁻¹, BM 은 1.62):

| AM wt% | gran | sc | gran-BM | sc-BM |
|---|---:|---:|---:|---:|
| 51 | 0.565 | 0.573 | — | — |
| 73 | 0.366 | 0.367 | 0.378 | **0.326** |
| 84 | 0.233 | 0.234 | 0.237 | 0.235 |
| 90 | 0.153 | — | 0.154 | 0.154 |

⇒ `ε` 는 **조성마다 하나**(≈0.57 / 0.37 / 0.234 / 0.153)이고 gran·sc·BM 에 공통 — **공칭 catholyte 분율**이다. 공극은 `ε` 가 아니라 `τ` 로 들어간다(저자도 `τ` 를 "geometric and porosity-related effects" 로 부른다 — 서술과 일치).
⚠ **sc73-BM** 만 0.326 — 다른 셋이 0.37 이면 `τ` 는 **≈2.9**(인쇄 2.6) 또는 `σ_eff` **≈2.29·10⁻⁴**(인쇄 2.03·10⁻⁴) 여야 한다. 같은 행의 `φ` 도 안 맞는다(§4-2) ⇒ **이 행에 전사 오류가 둘**(D4).
Table S1 이 없어 공칭 부피분율을 직접 대조하지 못했다(밀도 가정 NCM 4.8 · LPSCl 1.64–1.86 g cm⁻³ 로 51 wt% ≈0.66–0.69 — 역산 0.57 보다 크다; 밀도 가정에 민감해 판정하지 않는다).

## 4-2. 식 (5) — 제곱근이 맞게 쓰였다, 한 행만 빼고
`√(D/D_LIB)` 로 13 행이 인쇄 `φ` 와 ±0.1 %p 안에서 맞는다. ⚠ **sc73-BM**: √(1.29/2.31) = **74.7 %** ↔ 인쇄 70.8 %(= `D` 1.16·10⁻¹² 에 해당). sc51: 본문 p.8 "85.1 %" ↔ 표·p.8 뒤 "85.2 %" ↔ 계산 85.3 %(D5, 반올림 급).

## 4-3. ★★★★ 식 (2) 의 고율 극한 — `Q_M` 과 `α` 는 한 조합이 된다
`R α ≫ 1` 이면 `Q ≈ (Q_M/2)·α⁻ⁿ·R⁻ⁿ`. 로그–로그 직선의 **기울기 = `n`**, **절편 = `log(Q_M α⁻ⁿ / 2)`**. 저율 평탄이 창 안에 없으면 데이터는 `n` 과 `Q_M·α⁻ⁿ` 만 정한다 — `Q_M` 을 올리고 `α` 를 `Q_M^{1/n}` 비례로 올리는 방향이 **null 방향**이다.
⇒ 저자의 "dependency close to unity" 는 이 대수의 수치판이고, **"`n` 만 해석할 수 있다" 는 판정도 이 대수와 정확히 맞다**(`n` 은 기울기라 조합 밖).
★ 카드 물음으로 옮기면(`[해석]`): **용량 스케일(`Q_M` — `θ`·LAM·물질 용량의 합)은 준평형 데이터가 있어야 동역학(`α`)과 갈린다.** 이것은 카드가 OCV 에 거는 전제("무한 저율 용량이 보이면 `η` 가 빠진다")의 **ASSB 실측판 경계**다.

## 4-4. ★★★ `n` 은 CA 초기 과도의 시간 지수다 — "저항 = SE, 확산 = AM" 배정은 식이 아니라 가정이다
식 (1) 에서 `Q(t) ∝ t^m` 이면 `I ∝ t^{m−1}`, `R = I/Q ∝ 1/t` ⇒ `Q ∝ R^{−m}` — **`n` = CA 누적 전하의 시간 지수**.
- 전류 일정(직렬 저항 하나가 정하는 옴 한계) → `m = 1` → **`n = 1`**
- 반무한 확산(Cottrell) → `Q ∝ √t` → **`n = 0.5`**
`[해석]` 그런데 **다공 전극의 이온 전송선(de Levie TLM — 분산 저항 + 계면 저장)** 도 초기에 `Q ∝ √t` 를 준다. 이 편이 `σ_eff` 를 **바로 그 TLM 으로 적합**했다(식 없음, ref 9·22). 따라서 `n → 0.5` 는 **AM 고체 확산**과 **catholyte 의 분산 이온 저항** 둘 다와 양립하고, `n → 1` 은 **분산이 아닌 뭉친 직렬 저항**(분리막 · 음극 · 계면)과 양립한다.
Fig. 7c 의 "contradictory" (`σ_eff` 가 높을수록 `n` → 1) 는 이 읽기에서 모순이 아니다: catholyte 가 잘 통하면 전극이 뭉친 요소처럼 굴어 **직렬 저항이 초기 과도를 정한다**(`n` ≈1); catholyte 가 나쁘면 **전송선의 √t 가 드러난다**(`n` ↓).
⇒ `[해석]` **"확산성 한계 = AM 내부 확산" 은 `n` 에서 나오지 않는다.** 저자는 §2 의 가정("SE 에서는 이동만, 거시 확산 없음")으로 이 대안을 막았다.
⚠ 이것은 우리의 대안 해석이다 — **판별하지 않았다**(CA 원자료 · TLM 파라미터 0).

## 4-5. ★★★ 두 "독립" 측정이 설계 위에서 거의 공선이다
13 셀(sc90 제외)에서 `σ_eff` 와 `D` 의 Spearman **ρ = 0.94**, log–log Pearson **r = 0.85**. 둘 다 AM 비와 함께 내려간다.
⇒ Fig. 7a vs 7b 의 "어느 쪽이 더 잘 모이나" 로 병목을 정하는 논증은 **공선 회귀변수 두 개 중 하나를 고르는 것**이다. 판정 근거(master line)는 눈대중 파선이다.
그리고 `D_app` 는 **`σ_eff` 가 들어간 측정**일 수 있다 — GITT 의 `dE/d√t` 는 복합체 전체의 전위 응답이고, 고 AM 비에서 catholyte 전송선의 √t 응답이 섞인다(§4-4). 저자는 GITT 에 이 보정을 하지 않았다.

## 4-6. ★★★★ GITT 가 재는 것은 `D` 가 아니라 `D·(A_eff/V)²` — 28호의 `τ_d` 묶음이다
식 (3) 에 `A` 가 **제곱**으로 들어가므로, 진짜 활성 면적이 `A_eff = φ·A_BET` 이면 `D_app = D·φ²`. 한편 `(A/V)` 는 확산 길이의 역수(`L = V/A`)라 **데이터가 정하는 것은 `D/L_eff² = 1/τ_d`** — 28호 SPM 묶음 `τ_d = R²/D` 와 같은 자리다.
- `[인쇄]` 저자도 그렇게 말한다: "The knowledge or assumption of A is necessary when quantifying diffusive phenomena." · "the apparent D_Li⁺ differences **must result from the inclusion of the surface area A** in Eq. 3."
- 그들이 `D` 와 면적을 가르는 방법 = **`D_true(ASSB) = D_LIB` 수입** + **LIB 피복률 100 %**. 둘 다 가정이다 — 그리고 두 번째는 `D_LIB` 가 gran/sc 에서 2.7 배 다르다는 **자기 데이터**가 흔든다(LIB 에서도 `A_eff ≠ A_BET`).
- `[재현]` 크기 검산: `L = V/A_BET` 로 gran 0.37 µm(0.570 m² g⁻¹ × 4.8 g cm⁻³ 가정) → `L²/D_LIB` ≈ **215 s ≈ 0.06 h** ↔ gran51 `α` 0.05 h. sc(0.30 µm) `L²/D_sc51` ≈0.15 h ↔ `α` 0.035 h(×4) · sc84 2.2 h ↔ 1.4 h · gran90-BM 0.65 h ↔ 0.14 h(×4.6) · sc90-BM 21 h ↔ 1.35 h(×16). ⇒ **GITT 시간척도와 CA `α` 가 대체로 한 자릿수 안** — Fig. 7b 의 "master line" 은 `[해석]` **시간척도 대 시간척도**이고, `D` 라는 이름은 면적 가정이 붙인 것이다. (NCM 밀도 4.8 은 우리 가정.)
⇒ **입자 크기(면적)와 `D` 를 분리하는가? — 아니다.** 면적은 BET(분말, 신품)로 **입력**하고, 남는 차이는 전부 "피복률" 로 배정한다.

---

# 5. 핵심 물음에 대한 답 — 이 편은 무엇을 가르고, 그것은 측정인가

| 가르는 쌍 | 방법 | 측정인가 | 무엇이 흔드나 |
|---|---|---|---|
| **정적 용량(`Q_M`) ↔ 동역학적 결손(`α`·`n`)** = 카드의 `θ`+LAM ↔ `η` | CA 한 번 + 식 (2) 외삽 | **적합 외삽.** 평탄이 창 안이면 식별 · 창 밖이면 `Q_M·α⁻ⁿ` 한 조합(저자 진단) | ① 평탄이 **어느 셀에도 진짜로는 없다**(Fig. 2) ② `Q_M` 은 평탄이 보이면 과소 · 안 보이면 과대(§3-4) ③ sc84 가 경계에 걸린 채 해석됨 |
| **물질 고유 용량 ↔ 이용률(전자 비연결 + 균열 이탈)** = 카드의 LAM ↔ `θ` 의 **신품판** | 같은 분말의 LIB 반쪽전지 0.1 C 용량 | 외부 **측정**이지만 **기준이 한계가 아니다**: 0.1 C 유한 율 · 창 미기재 · sc84 `Q_M/Q_LIB` ≈111 % | 이용률 > 100 % 가 나오는 기준은 `θ` 의 분모가 못 된다 |
| **전자 비연결(용량) ↔ 이온 접촉 면적(동역학)** — 접촉 손실의 두 종류 | `Q_M` ↔ `φ` | 둘 다 역산. **균열이 두 칸에 동시에 배정**된다("detach from the electronic percolation network" → `Q_M` / "particle delamination and contact loss" → `φ`) | 균열 몫을 가를 관측 0 |
| **저항성(SE 수송) ↔ 확산성(AM 수송)** | `n` + `σ_eff`(TLM) + `D`(GITT) | 셋 다 측정이지만 **배정은 가정**(§4-4) · `σ_eff`–`D` 공선(§4-5) | TLM 전송선의 √t 가 `n` ≈0.5 를 흉내 낼 수 있다 |
| **접촉 면적 ↔ 고체 확산계수** | `φ = √(D_app/D_LIB)` | **순수 가정**(`D_true` 공통 · LIB 100 %) — 저자 자신이 "knowledge or assumption of A is necessary" | `D_LIB` gran/sc 2.7 배 |

⇒ **부모 질문의 답**: 이 편은 "비연결 활물질 분율(정적)" 과 "확산 제한으로 접근 못 한 용량(동적)" 을 **가른다** — 단 **율 외삽 적합으로**, 그리고 **그 적합이 실패하는 조건을 공분산 진단으로 인쇄**했다. 동적 쪽 안에서 "접촉 면적" 과 "고체 확산" 은 **모델 가정으로** 가른다.

---

# 6. 28호(Bizeray) 묶음과 대조 (`[해석]`)

| 28호 SPM | 29호 | 관계 |
|---|---|---|
| `Q_th` (용량 스케일) — **입력**(`β = dU/dQ` 로 흡수) | `Q_M` — **적합**(외삽) | 28호가 뺀 축을 29호는 넣었다 — 그래서 29호는 그 축의 비식별을 **볼 수 있었다** |
| `τ_d = R²/D` — 식별 | GITT `D_app` = `D·(A_eff/V)²` ≡ `1/τ_d` (`L = V/A`) | **같은 묶음.** 28호는 묶음으로 두고, 29호는 BET + `D_LIB` 수입으로 쪼갠다 |
| `τ_k` · `R_ct` (표면 일부 접촉은 여기로 사라짐) | `φ` (표면 피복률) | 28호에서 `R_ct` → `R0` 로 사라지는 **표면 일부 접촉**을 29호는 **확산 묶음의 면적**으로 읽는다 — 같은 물리량이 **다른 묶음**에 배정된다 |
| 입자 통째 비연결 `ε → uε` ≡ LAM (`Q_th`) | `Q_M` 의 "electronically isolated AM clusters" | 같은 자리. 29호는 LIB 기준으로 물질 용량을 떼려 했다(신품) |
| 비식별 조건: `β = 0` · 두 전극 맞바꿈 | 비식별 조건: **저율 평탄이 창 밖** | 둘 다 "여기(excitation)가 그 방향을 안 건드린다" 의 사례 |

---

# 7. Q1~Q8

| # | 이 편 | 칸 |
|---|---|---|
| Q1 정량 | `Q_M`(이용률) 14 점 · `φ`(피복률) 14 점 — 둘 다 **역산**(용량 · `D` 비 + 가정). `contact loss` 2 회는 전부 균열 서술(ref 47 = 23호 Koerver). 단면 영상 0. **`θ(N)` 0/29** | **이동 없음** |
| Q2 독립관측 | LIB 기준(같은 분말) · 대칭 셀 EIS · GITT — 세 채널. 그러나 **LAM ↔ 접촉**을 가르는 관측은 아니다(신품; 기준이 한계로 기능 안 함, sc84 ≈111 %) | **반 칸 검토 후 접음** |
| Q3 라벨층위 | **fitted-extrapolated**(`Q_M`) + **derived-by-reference-ratio**(`φ` = 외부 액체 기준 수입) + fitted(TLM `σ_eff`) · 공칭(`ε`). 오차막대 0 · 조건당 1 셀 · **적합 공분산 진단 있음(SI, 미열람)** | 층 둘 |
| Q4 유일성 | ★ **`Q_M` ↔ `α` dependency ≈1 (sc90) 을 저자가 계산·인쇄** — 둘째 줄의 수치 진단 · 식별 집합에 용량 스케일 포함. 반 칸 이유 넷(판정 상자) | **+0.5 (ASSB 첫)** |
| Q5 Li-In | 2전극, 0.62 V 오프셋 **가정**(ref 23 Santhosha 2019, 숫자는 지면에 없음). 같은 연구실 17호가 **같은 음극 조성**을 3전극으로 검증 — 그러나 검증 창(정상 상태 ≈20 mV)과 이 편이 `n` 을 읽는 창(CA 첫 초~분, 17호 `[인쇄]` 시작 ca. 0.9 V)이 다르다 | **이동 없음** — 열한 번째 형태 |
| Q6 압력 | 제조 500 MPa · 운전 ca. 50 MPa **고정**, 스윕 0 | 이동 없음 |
| Q7 dead Li | 해당 없음(Li-In) | — |
| Q8 화학·OCP | NCM811 두 형상(단결정 첫 대조) · OCP 0(형성 곡선은 SI Fig. S6) | 이동 없음 |

---

# 8. 곱 축퇴 처방 — 열두 번째 적용

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | TLM 적합은 했으나 **`C`·계면 요소 값 0**(Fig. S1 SI) · 인쇄는 `σ_eff` 뿐 | ❌ |
| **2단계** (18호·25호) | + 면적을 아는 대조군 | ★ **SE 입도 쌍(LPSCl 2.25 ↔ BM 8.36 m² g⁻¹, ×3.7) + CAM 형상 쌍(BET 0.570 ↔ 0.696) + 같은 분말 LIB** | ✅ **부분** — `[재현]` BM/비BM `φ` 비 1.02–2.29 < BET 비 3.7: **방향 통과, 크기는 상한 안**(피복률이 SE 면적에 선형일 이유 없음). 25호 "SE 입도 쌍 + BET" 줄의 두 번째 표본 |
| **3단계-a** (19호) | `Ea` | 30 °C 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | `C` 없음 | ❌ |
| **4단계** (20호) | 시간 영역에도 같은 검사 | ★ CA `α`(h) ↔ GITT `L²/D` 시간척도 | ✅ **자릿수 양립**(×1–16, §4-6) — 단 둘이 같은 곱을 보므로 **검사가 아니라 일관성** |

**이 편이 처방에 더하는 것**:
1. ★★★★ **처방 표 첫 줄("율 스윕, `i → 0` 포함 — `η(i)` 를 지워 `θ_AM·Q_material` 만 남긴다")의 계보 첫 실적용이고, 그 줄의 실패 조건이 저자 진단으로 인쇄됐다**: 저율 평탄이 측정 창 안에 없으면 `Q_M`(= `θ·Q`) 과 `α`(= `η` 시간척도)가 **한 조합**이 된다. ⇒ 처방 첫 줄에 **"종료 율이 평탄 안에 있는지 먼저 확인 — 곡선이 로그 축 끝까지 기울어 있으면 외삽 용량을 쓰지 않는다"** 를 붙인다.
2. ★★★ **새 줄 — "외부 액체 기준 수입"**: GITT 곱 `D·A_eff²` 에서 **같은 분말의 액체 반쪽전지 `D_LIB`** 로 한 인자를 고정. 22호의 "LIB 대조(같은 CAM)" 와 같은 부류. ⚠ **기준 자체가 곱을 진다** — `D_LIB` 가 gran/sc 2.7 배(액체가 균열 내면을 적신다, 저자 서술).

---

# 9. Q5 — 같은 연구실의 3전극 검증을 2전극으로 옮겼다 (열한 번째 형태)

- 이 편: 2전극, 기준극 0, `E_CE` 기록 0. 음극 = 17호 조성(40 at% Li, 40 wt% SE), `[인쇄]` "prepared as described elsewhere.²¹".
- 17호(3전극, 같은 음극 복합체): CA 방전 중 `[인쇄]` "E_CE of the Li-In-SE composite cell shows a much lower potential of **ca. 0.9 V at the beginning of discharge** and relaxes rapidly to 0.64 V at 0.2 h" — 17호 digest `[재현]` 그 초기 돌출의 ≈71 % 가 CE–RE 옴.
- `[해석]` 이 편의 `n` 은 **CA 첫 구간**(`R` ≫ 1 h⁻¹, Fig. 3 의 꼬리)의 기울기다 — 17호가 음극·분리막 쪽 **수백 mV 과도**를 본 바로 그 시간대다. 양극 제한이라는 `[인쇄]` "the typical features of cathode limited cells can be seen" 은 곡선 모양에서 온 판단이고, 음극 몫을 뺀 계산은 없다.
- ⇒ **Q5 열한 번째 형태 = "검증 이식 — 같은 연구실이 직전 편에서 3전극으로 검증한 상대극을 2전극 기준으로 재사용하되, 검증된 창(정상 상태)과 해석하는 창(과도 초기)이 다르다."** 21호 "교정 이식" 과 같은 계열.
- 스택 50 MPa · 17호의 운전 압력과 같은지는 이 편에서 확인 안 됨.

---

# 10. ⚠ 어긋남 15 건

| # | 내용 | 근거 |
|---|---|---|
| **D1** | "sc84-BM … significantly higher … than sc73-BM (**175 and 195** respectively)" — 순서가 반대이고 195 ≠ 그림 ≈205 | Fig. 2d `[도표]` sc84-BM ≈205 · sc73-BM ≈175 |
| D2 | gran90-BM @1 C "73 mAh g⁻¹" ↔ 그림 ≈80 | Fig. 2c 확대 |
| **D3** | sc84 `D` 표 1.12·10⁻¹³ ↔ Fig. 6b · 7b ≈8·10⁻¹⁴ | 격자선 아래 |
| **D4** | sc73-BM 행: `φ` 70.8 ↔ √ 계산 74.7 · `τ` 2.6 ↔ `ε` 정합 2.9 — 한 행에 둘 | §4-1 · §4-2 |
| D5 | sc51 `φ` 본문 85.1 ↔ 표·본문 85.2 ↔ 계산 85.3 | 반올림 급 |
| **D6** | `Q_M` = "무한 저율 최대" 인데 gran51 · sc51 · sc73 에서 실측 0.02 C 용량보다 **낮다** | Fig. 4 ↔ 2 `[도표]` |
| **D7** | ★ sc84 `Q_M` ≈236(실측 177, LIB 213)을 "Q_M maximum … even exceeding the reference LIB capacity" 로 해석 — 저자 자신이 "plateau not clearly visible" · "fit quality … lower" 라 한 셀. **sc84 ↔ sc84-BM 의 `Q_M` 순서가 실측 순서와 반대**이고, "insulating SE shells" 설명이 그 순서에 기댄다 | Fig. 2b·2d · 4 |
| D8 | `n` 이 해석 범위 [0.5, 1] 밖: sc51 ≈1.03 · sc90 ≈0.41 — 논의 없음 | Fig. 4 · 7d |
| **D9** | sc90 `Q_M` ≈60 · `α` ≈2.2 h 가 "accurately fit 불가" 선언 뒤에도 Fig. 4 에 무표시로 그려짐 | Fig. 4 |
| D10 | 범례 "ugran/usc/ugran-BM/usc-BM" ↔ 본문 이름; Fig. 7 a–c "sc (51–84 %)" ↔ d "usc (51–90 %)" | 외형 |
| D11 | CA "3.0 V" 기준 미기재(vs Li⁺/Li 로 읽는다) | §0 |
| D12 | BM `σ_eff` 효과: p.7 "significantly higher" ↔ p.9 gran90 쌍 "very similar"(×1.3). 전 쌍 ×1.16–1.69 | Table I |
| D13 | "9.04·10⁻³ **S⁻² cm⁻¹**" — 단위 오기(S cm⁻¹) | p.10 |
| D14 | 이용률 기준 `Q_LIB` 는 **0.1 C 실측**, `Q_M` 은 **무한 저율 외삽** — 다른 양의 비. LIB 창 미기재 | p.6 |
| D15 | "master line" (Fig. 7b) — 회귀 없음, 캡션은 "guide to the eye only" | p.9 ↔ 캡션 |

---

# 11. 그림 — 무엇을 봤나

크로퍼 **7 장 전부 봤다, 안 본 것 0 장**: Fig. 1(SEM) · 2(CA 네 판) · 3(크롭에 Fig. 2 가 겹쳐 들어왔다 — 아래 우측이 Fig. 3) · 4(`n`/`α`/`Q_M`) · 5(모식도) · 6(`σ_eff`·`D`) · 7(네 판).
추가로 본 것: 식 (1)–(5) 300 dpi 렌더(추출 텍스트에서 제곱근·계수 2 가 빠져서) · Fig. 2c/2d 확대(D1·D2).
Table I 은 텍스트 추출로 전사하고 Fig. 6 과 대조했다. **SI 그림 8 장(S1–S8) · 표 2 개(S1·S2)는 못 봤다** — 업로드 없음, IOP 접근 정책상 차단.

---

# 12. 참고문헌 — 후속 후보

| ref | 서지 | 왜 |
|---|---|---|
| 19 | Tian, King, Coelho, Park, Horvath, Nicolosi, O'Dwyer, Coleman, *J. Power Sources* **468** (2020) 228220 | 식 (1)·(2) 와 `n` 해석(0.5 확산 · 1 저항)의 원전 — **§4-4 의 대안(TLM √t)을 원전이 다뤘는지** |
| 20 | Yanev, Auer, Heubner, Höhn, Nikolowski, Partsch, Michaelis, *J. Electrochem. Soc.* **169** (2022) 090519 | 같은 방법의 ASSB 첫 판 · "damaged AM particles … detach" 의 출처 |
| 22 | Kaiser, Spannenberger, Schmitt, Cronau, Kato, Roling, *J. Power Sources* **396** (2018) 175 | 식 (4) `τ` · TLM — 16호(Roling 연구실) 계보 |
| 9 | Minnmann, Quillman, Burkhardt, Richter, Janek, *J. Electrochem. Soc.* **168** (2021) 040537 | TLM 부분 전도도(2호가 인용) |
| 15 | Minnmann et al., *Adv. Energy Mater.* **12** (2022) 2201425 | 단결정 NCM · 도전재 없는 양극 |
| 26 | Ruess, Schweidler, Hemmelmann, **Conforto**, Bielefeld, Weber, Sann, Elm, Janek, *J. Electrochem. Soc.* **167** (2020) 100532 | NCM 균열과 GITT — 액체 ↔ 고체 |
| 28 | Bielefeld, Weber, Janek, *J. Phys. Chem. C* **123** (2019) 1626 | = **1호** (`Q_M` 해석의 전자 비연결 근거로 인용) |
| 47 | Koerver et al., *Chem. Mater.* **29** (2017) 5574 | = **23호** ("particle delamination and contact loss") |
| 21 | Yanev et al., *J. Electrochem. Soc.* **171** (2024) 020512 | = **17호** (음극 조성) |
| 23 | Santhosha, Medenbach, Buchheim, Adelhelm, *Batteries & Supercaps* (2019) | Q5 0.62 V 뿌리(17호 ref 26 과 같은 편) |

`[해석]` 큐와의 접점: **큐 30(ICI 확산계수)** 은 이 편의 GITT `D` 를 대체할 방법이고, **큐 37(Conforto chemo-mechanical NCM)** 은 ref 26 공저자 계열이다. **큐 29(Park, low-mass-loading NMC111, asymmetric kinetics)** 는 같은 "율 한계 분해" 축이다.
Bizeray 2019(28호)는 인용 0 — ASSB 문헌이 식별성 원전을 가리키지 않는다는 기록이 29호에서도 유지된다.

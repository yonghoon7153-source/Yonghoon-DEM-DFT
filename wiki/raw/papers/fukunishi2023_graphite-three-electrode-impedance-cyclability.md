---
title: "Fukunishi, Ikezawa, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2023 — Impedance Analysis and Cyclability Evaluation of Graphite Composite Electrodes with All-Solid-State Three-Electrode Cells (ACS Appl. Energy Mater. 6, 10908-10917)"
source_url: local-upload/5._Impedance_analysis_and_cyclability_evaluation_of_graphite_composite_electrodes_with_all-solid-state_three-electrode_cells.pdf + 5._Sup_Impedance_analysis_and_cyclability_evaluation_of_graphite_composite_electrodes_with_all-solid-state_three-electrode_cells.pdf (SI)
source_url_note: "본문 10 쪽(참고문헌 54, 그림 5 · 표 3) + SI 9 쪽(그림 S1-S8). 크로퍼 16 장(그림 13 · 표 3) 중 그림 9 장을 봤다(Fig. 1 · 2 · 4 · 5 · S2 · S4 · S5 · S7 · S8) — fig_S7 은 아래 띠만 잘려 SI 8 쪽을 따로 렌더해 봄. 판정 수치는 크롭 래스터 화소 판독(Fig. 1b · 4a · 4b · 4d · S7a). 원자료 · PDF 는 커밋하지 않는다. 18호(Fukunishi 2023 JPS 564, NCM523)와 다른 논문 — 같은 연구실의 흑연 음극 판."
source_doi: 10.1021/acsaem.3c01656
source_license: "오픈액세스 표기 없음 (지면 '© 2023 American Chemical Society')"
pdf_sha256: d4be72363488236b3a0cf3a975187d062dd25ea5021ac5a0364d2d39ec390b88
si_sha256: 038b4a91e91a64a9fb54ff7bf13181d06a08167a23c9647eb2e0fe861792d715
ingested: 2026-09-23
sha256: 7d0f9c263cfc300ac383bda544d9c831ec787124e2357a8522bf91261bbcbd4a
---

# 수집 목적

`assb` 섹션 **43호**. 큐 **44번**(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g, 2차 묶음 다섯째 편).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장 지목은 19호(★★★).

⚠ **같은 제1저자의 다른 논문**이다 — 18호(Fukunishi 2023 *J. Power Sources* 564, 232864, NCM523 양극 3전극)와
같은 연구실(Tokyo Tech Arai) · 같은 셀 설계(R-LTO 메시 3전극, 110 MPa) · 같은 해에 나온 **흑연 음극 판**이다.
40호(Ikezawa 2020, R-LTO 원전)의 직계 후속이고, 이 편의 ref 31 = 40호 · ref 32 = 18호다.

이번 흡수의 두 물음:
1. **음극 쪽 열화 분해** — 3전극 EIS 가 흑연 복합전극의 저항을 성분별로 나눠 사이클 열화에 배정했는가,
   용량 손실 배정은 측정인가 해석인가, 곱 축퇴(접촉 ↔ `LAM`)가 **음극에서** 어떻게 나타나는가(지금까지 계보는 양극 중심).
2. **Q5** — R-LTO 1.55 V 를 다시 인용만 하는가, 전위를 새로 검증했는가.

# 판정 (먼저)

> **음극 쪽 열화 배정: 저항 분해는 측정(3전극 EIS + 등가회로 적합, 성분마다 `R` · CPE-T · CPE-P 를 노화 전후로 ± 와 함께 인쇄),
> 용량 손실의 기구 배정은 해석이다.** `[인쇄]` "every peak intensity corresponding to the graphite staging is decreased.
> This means that capacity decrease mainly resulted from the loss of the active material" — **dQ/dV 봉우리 높이 한 관측에서
> `LAM` 을 읽었고**, 같은 문단 뒤에서 임피던스로 `[인쇄]` "the decrease in the electrode−electrolyte interface area" ·
> "the loss of contact area" 를 읽는다. **같은 셀의 같은 열화를 용량 채널은 `LAM`, 임피던스 채널은 면적 · SEI 로 이름
> 붙이고 두 채널의 크기를 대조하지 않는다.**
>
> ★★★★ **대조하면 갈린다(`[재현]`, 우리 계산)**: 0.05 C 용량 비 `[도표]` **≈0.75–0.78** ↔ `R_CT` 호의 면적 서명
> (Table 3 로 `C_eff = (R·Q)^{1/P}/R`) **`C` 비 0.43 ± ≈0.2 ≈ 1/`R` 비 0.47**. 면적 손실이 전부 **입자 통째 고립**이면
> 용량도 ×0.45 여야 한다 ⇒ **면적 손실이 용량 손실보다 크다 — 적어도 일부는 표면 피복(`A_eff`, 37호의 `k` 쌍둥이)이지
> 고립이 아니다.** 반대로 **용량 25 % 가 진짜 `LAM_NE` 인지 고립(`θ`)인지는 이 편의 어떤 채널로도 안 갈린다** —
> 반쪽전지(Li-In 저장소)라 `LLI` 는 WE 용량에 안 보이므로, **음극 판 곱 축퇴는 `LAM_NE` ↔ 접촉 고립 두 항으로 순수하게 남는다.**
> 그리고 **3-a `Ea` 채널은 1단계와 반대로 말한다**: `R_CT` 의 `Ea` 22(1) → 27.5(3) kJ mol⁻¹(저자: "nearly unchanged") —
> 면적만이면 `Ea` 불변이어야 한다. **노화 뒤 세 성분의 `Ea` 가 27.6 · 27 · 27.5 로 한 값에 모인다**(원문 무언급).
>
> **Q2 — 반 칸 검토 후 접음.** 채널은 셋(3전극 EIS R·CPE · `Ea` 노화 전후 · 전극별 dQ/dV)이 같은 셀에 있고 입력은 계보에서
> 가장 완비됐지만, **원전은 채널마다 다른 기구를 배정했을 뿐 가르지 않았다** — 가른 것은 우리 계산이고 두 면적-불변 채널이
> 충돌한다. `capacitan*` **0 회**, CPE 는 Table 3 의 T · P 로만(단위 "F" — P < 1 이면 F s^(P−1)).
>
> **Q5 — +0.5 (열아홉 번째 형태 "공통 모드 표류 판독").** 값은 **또 인용이다**: `[인쇄]` "**Suppose** the R-LTO reference
> electrode shows a redox potential of 1.55 V vs Li/Li⁺ for Li₇Ti₅O₁₂/Li₄Ti₅O₁₂,⁴⁰,⁴¹" — [40] Colbow 1989 · [41] Ohzuku 1995
> (18호와 같은 수입 경로; 40호의 Costard 경로 아님). 검증은 증인 둘 — **작업전극 자신의 흑연 단계 평탄 셋**(GITT 준-OCP
> 0.195 · 0.110 · 0.068 V, 문헌값은 인쇄 안 함 · "roughly consistent")과 **Li-In 0.60 V**([44] = 42호 Santhosha, 그 원전 인쇄값은
> **0.62/0.622**). ★ **새것은 표류 수다**: `[인쇄]` "a small potential shift of ca. **10 mV** (negative direction) seen in **both** the
> graphite and Li−In electrodes, which **could be caused by the change of the R-LTO reference electrode potential**" (333 K 가속
> 열화 뒤). `[도표]` 흑연 dQ/dV 봉우리 리튬화 · 탈리튬화 **둘 다 −13 … −21 mV**, Li-In 평탄 중점 **0.609 → 0.593 V(−16 mV)** —
> 저항 증가라면 두 방향이 반대로 가야 한다 ⇒ **공통 모드 ≈−14 mV**. **R-LTO 가지(40 · 18 · 19호)에서 처음 인쇄된 표류 값**이다.
> **반 칸인 이유**: 배정이 "could" · n = 1 · 시간 축 없음(전후 두 점) · **같은 지면이 SI Fig. S2 의 임피던스 합 일치로
> R-LTO 의 "stability" 를 "proves"** 한다(18호 K–K 와 같은 범주 오류 — 합 일치는 DC 전위를 보지 않는다) · 1.55 V 값 자체는
> 여전히 인용. `leak` · `drift` **0 회** — **누설 직접 측정 0/43.**
>
> **채움표 ≈18.5 → ≈19.0 (Q5 +0.5).** Q1 `θ(N)` **0/43**(식 (4) 가 `[인쇄]` "the total surface area of the active material
> particles, **or** the interface area" 로 `θ ≡ 1` 을 인쇄) · Q4 **0/43 서른다섯 번째 성질** · Q6 이동 없음(운전 압력 0) ·
> Q7 · Q8 해당 없음.

> 표기: `[인쇄]` 본문·SI 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`) · `[재현]` 우리가 지면의 숫자로 계산한 값 ·
> `[해석]` 우리 해석 · `[추론]` 가정을 붙인 추정. **`[해석]` · `[추론]` 표시 없는 문장은 원문이 실제로 말한 것이다.**

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 걸리나 |
|---|---|---|
| **G1** | **셀 개수 · 반복이 없다.** `n =` 0 회. RT 500 사이클과 333 K 50 사이클이 **같은 셀**(`[인쇄]` "using the same cell (after the durability tests at 298 K)") | 가속 열화의 "전" 상태가 이미 RT 500 사이클 뒤다 — 두 열화 조건이 한 이력에 쌓인다 |
| **G2** | **R-LTO 전위를 Li 대비로 재지 않았다** — "Suppose … 1.55 V [40,41]" | 컷오프(−1.55 / −0.55 V vs R-LTO = 0 / 1.00 V vs Li)와 모든 "vs Li/Li⁺" 축이 이 가정 위 |
| **G3** | **흑연 단계 전위의 비교 문헌값을 인쇄하지 않았다** — "roughly consistent with the literature values [42,43]" | 증인의 분해능(몇 mV 까지 맞는가)을 지면에서 계산할 수 없다 |
| **G4** | **"3.0 mg" 가 복합체 질량인지 흑연 질량인지 불명** — `[인쇄]` "graphite composite (3.0 mg, 0.78 cm²)", 조성 20 : 80 wt% | 복합체면 흑연 0.6 mg. C-rate · 전류 · 면적 환산이 ×5 갈린다. `[재현]` §5.4 의 4단계 검사가 **복합체 쪽**을 지지 |
| **G5** | **운전 압력이 없다.** 조립 110 MPa · Li-In 압착 ≈100 MPa, `pressure` **0 회** | 서론이 void · crack 과 "high pressing force" 필요를 인용하면서 열화 셀의 압력은 보고 · 통제 없음 |
| **G6** | **dQ/dV 봉우리 넓이(적분)를 안 냈다** — 높이로 `LAM` 을 읽는다 | 높이는 넓어짐(분극 분포 · 불균일)에도 준다. `[도표]` 봉우리마다 비가 다르다(§4.3) |
| **G7** | **흑연 밀도 · BET 비표면적 미인쇄** — 식 (4) 의 `d` 도 값 없음 | 3단계-b(`C` 물리 상한)를 우리 가정(2.2 g cm⁻³)으로만 건다 |
| **G8** | **입도 스윕(2전극)은 3전극 셀과 다른 흑연**(3전극 Mitsubishi D50 11.2 · 2전극 SEC carbon 5.0/11.2/30.0) | 입도 축 결론(Table 1)과 3전극 임피던스 배정이 같은 분말이 아니다 |
| **G9** | **CPE 를 커패시턴스로 환산하지 않았다** — Table 3 의 T 를 "F" 단위로 인쇄 | 1단계(`R·C`)는 우리가 환산(§5.2) |

# 1. 서지 · 낱말 지문

- Fukunishi · Ikezawa · Okajima · Kitamura · Suzuki · Hirayama · Kanno · Arai, "Impedance Analysis and Cyclability Evaluation of Graphite
  Composite Electrodes with All-Solid-State Three-Electrode Cells", *ACS Appl. Energy Mater.* **2023**, 6, 10908–10917,
  `10.1021/acsaem.3c01656`. 접수 2023-07-04 · 수락 09-27 · 게재 10-16. Tokyo Tech(School of Materials and Chemical Technology +
  All-Solid-State Battery Center). NEDO SOLiD-EV(P18003). SEC carbon 흑연 제공 사례. ACS 조판, 오픈액세스 표기 없음.
- 본문 10 쪽(참고문헌 54) + SI 9 쪽(Fig. S1–S8).

**낱말 지문** (NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문 = 참고문헌 전; 괄호 = SI):

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 2 (0) |

- NFKC 변경: 본문 **0 자** · SI **36 자**(전각 괄호 `（` `）` 18 쌍 — 그림 판 표지) — **열 변화 0**. 소프트 하이픈 0.
  줄끝 하이픈 본문 23 곳(이어도 열 변화 0).
- Q5 보조: `leak` **0** · `drift` **0** · `assum*` 1(과정 (A) 의 피막 가정 — 기준 전위 아님) · **`Suppos*` 1(기준 전위)** ·
  `stab*` 3(SEI 안정 서술 1 · R-LTO "stability" 2) · `1.55` 3(가정 1 · 컷오프 1 · LSV 1; SI 8 은 축 눈금) · `0.60` 2 ·
  `reproducib*` 0 · `prove*` 1("proves the stability").
- 곱 축퇴 보조: `contact` 3(물리 접촉 2 — "contact area" · "loss of contact area"; 1 은 저자 연락처) · `interface area` 2 ·
  `area` 7 · `"loss of the active material"` 1 · `dead` · `isolat*` · `percolat*` **0** · `capacitan*` **0** · `time constant` 0 ·
  `fit*` 4 · `void` 2 · `crack` 2(둘 다 서론 인용) · `pressure` **0** · `SEI` 6 · `error` · `n =` · `uniqu*` · `degenera*` **0**.
- `[해석]` **이 편은 "LAM" 이라는 약어 없이 "loss of the active material" 한 구절로 `LAM_NE` 를 배정한다** —
  약어 열(`LAM` 0)만 보면 배정이 없는 편으로 잘못 읽힌다. 이후 지문 표에 구절 검사를 같이 둔다.

# 2. 셀 · 실험 (`[인쇄]`, 괄호 안 `[재현]`)

| 항목 | 값 |
|---|---|
| WE | 구형 천연흑연(3전극: Mitsubishi D50 11.2 µm) : SE = **20 : 80 wt%**, 막자 15 분 + 볼밀 100 rpm 15 분. **3.0 mg, 0.78 cm²**(G4) |
| SE | **LPSI**(Li₂S–P₂S₅–LiI 유리세라믹, Idemitsu, D50 5.0 µm, 2.6 mS cm⁻¹) — 주. 대조 **LGPS**(자체 합성, 7.1 mS cm⁻¹). 복합체 SE = 분리막 SE |
| RE | **R-LTO 메시**(부분환원 Li₄₊ₓTi₅O₁₂ 를 Ni 망에 도포, SE 없음 — "universal design"), 두 SE 층 **1.0 mm(위, CE 쪽) · 0.6 mm(아래, WE 쪽)** 사이 |
| CE | Li–In: In 박 ∅10 × 0.05 mm + Li 박 ∅5 × 0.1 mm, ≈100 MPa 압착 (`[재현]` 18호와 같은 치수 → x_Li ≈37.7 at%) |
| 조립 | PET 관 ∅10 mm, **110 MPa**, Ar 폴리스티렌 용기 안에서 단자로 측정. 운전 압력 미보고 |
| 전기화학 | VSP-300. C-rate = 372 mAh g⁻¹ 기준. **컷오프 WE −1.55 / −0.55 V vs R-LTO(= 0 / 1.00 V vs Li)**. 조건화 0.05 C × 3 |
| GITT | 0.05 C 10 분 + 휴지 4.0 h |
| EIS | 각 평탄의 OCP 에서 2.0 h 유지 후, 10 mV, **7.0 MHz – 5.0 mHz**, Z-View 적합. 온도 273 · 283 · 293(· 303 · 313) K |
| 열화 | **RT**: 1.0 C × 500 사이클(298 K), 100 사이클마다 0.05 C 곡선 + 만리튬 상태 EIS · **HT(가속)**: 같은 셀로 1.0 C × 50 사이클(333 K), 전후 0.05 C(298 K) + EIS |
| 보조 | Cu 박 WE 3전극 LSV(≈2.0 → 0 V vs Li, 23 µV s⁻¹ — `[재현]` ≈24 h, 첫 0.05 C 충전과 같은 시간) · 입도 3종 2전극 셀(SEC carbon, 컷오프 "0.60 · −0.40 V vs Li–In" — §8 D7) |

# 3. 절별 해체

## 3.1 서론 (p1–2)

흑연의 두 과제 = 첫 리튬화 비가역 + 사이클 열화, 액체계에서는 SEI(<0.80 V 환원 분해). 액체 EIS 문헌이 정리한 속도결정 과정 넷
(전해질 수송 · SEI · 전하이동 · Li 수송)과 **>1 kHz 의 SEI 반원**. 고체계는 고체–고체 접촉이 어렵고 void · crack(ref 24 · 25),
고압 필요(24 · 26), 리튬화 흑연과 SE 의 반응성(27)이 보고됐다. `[인쇄]` 기존 고체계 흑연 EIS 는 **2전극이라** 막 형성 · 사이클
열화 거동이 불명. 목표: LPSI 흑연 복합전극을 3전극으로, **"The impedance components of the graphite electrode are successfully separated
in the solid electrolyte systems for the first time."**

## 3.2 기준극 타당성 — Fig. 1 · S1 · S2 (3.1 절, 제목 "Validly" 오기)

- `[인쇄]` 1.55 V 가정 위에서 흑연 세 평탄 ≈0.20 · 0.10 · 0.06 V 가 문헌([42] Dahn 1991 · [43] Asenbauer 2020)과 "roughly consistent",
  Li-In 평탄 **0.60 V** 가 [44](Santhosha 2019)와 "agrees" ⇒ "the R-LTO reference electrode works appropriately".
- dQ/dP 봉우리(리튬화/탈리튬화): 0.190/0.206 · 0.102/0.119 · 0.065/0.076 V. GITT 준-OCP(Fig. S1b): **0.195 · 0.110 · 0.068 V**.
- 임피던스 분리 검증(Fig. S2 a–c, 273/283/293 K): 흑연 + Li-In 합 ≈ 2전극 셀 임피던스. 273 K 에서 >1 MHz 불일치 → `[인쇄]`
  "possibly due to insufficient conductivity of the reference electrode at low temperatures", 그 대역 제외.
- **안정성**(Fig. S2 d–f, 가속 열화 뒤): 합 일치가 `[인쇄]` "**proves the stability** of the R-LTO reference electrode, as well as the
  previous study.³¹,³²"
- `[도표]` Fig. 1a: 첫 리튬화 ≈300 mAh g⁻¹, 탈리튬화 ≈230 — 이후 사이클 겹침. Fig. 1b: Li-In 네 사이클 완전 평탄,
  화소 판독 **≈0.604 V vs Li(= −0.946 V vs R-LTO)**, 판독 폭 ±3 mV.
- `[도표]` Fig. S2: 신품 293 K 흑연은 ≈35 Ω 에서 시작하는 사선(TLM 형), **Li-In 은 ≈60–150 Ω 반원** — 2전극 셀의 중주파 호는 대부분
  상대극이다. 가속 뒤(f) **Li-In 호가 ≈100–490 Ω 로 커진다**(`[도표]`, ×≈4 폭) — 상대극 열화, 원문 무언급.

## 3.3 첫 리튬화 비가역 — Table 1 · S3 · S4

- 비가역 두 과정: (A) ≳0.3 V · (B) <0.3 V. Cu LSV(Fig. S3a) 에 SE 환원 봉우리 여럿.
- 입도 스윕(2전극, Fig. S4 · Table 1): (A) 4.0 / 13 / 16 · (B) **96 / 52 / 21** · 합 1.0×10² / 65 / 37 mAh g⁻¹(D50 5.0 / 11.2 / 30.0 µm).
  `[인쇄]` (B) 는 "roughly inversely proportional to D50" ⇒ 식 (1)–(4) `S = 6M/(dD)` 로 **계면 반응 = SE 환원 분해**.
  `[재현]` (B)·D = 480 / 582 / 630 — ±14 % 안에서 반비례. ⚠ (A) 는 **D 와 같이 커진다**(4 → 16) — 설명 없음.
- ★ `[인쇄]` "the total surface area of the active material particles, **or** the interface area between the active materials and electrolyte, is
  inversely proportional to D" — **입자 전 표면 = 접촉 면적(`θ ≡ 1`)을 문장으로 놓는다**(18호 식 (4) "completely immersed" 와 같은 수법).

## 3.4 임피던스 성분 배정 — Fig. 2 · 3 · S3b · S5 · S6 · Table 2

회로(Fig. 2c): `L – R_SE – (R_X ∥ CPE_X) – (R_CT ∥ CPE_CT) – W_O`.

| 성분 | 원문 배정 | 근거(`[인쇄]`) | `Ea` 전 / 후 (kJ mol⁻¹) |
|---|---|---|---|
| `R_SE` | WE–RE 사이 SE 층 이온 수송 | 28 Ω ↔ σ · 0.79 cm² · 0.06 cm 로 29 Ω; `Ea` ≈ LPSI 문헌 22 | 22.9(7) / 27.6(3) |
| `R_X` | SE 환원 분해 생성물(Li₂S · Li₃P)의 표면층 | >1 kHz · 전위 무관(Fig. 2d ≈1.5–2 Ω) · 첫 리튬화에서 생김(S5) · Cu LSV 뒤 비슷한 반원(S3b) · LGPS 에서 훨씬 큼(S6) | **53(3)** / 27(3) |
| `R_CT` | 흑연\|SE 전하이동 | 전위 의존(Fig. 2d: 0.58 V 에서 2.77×10¹² Ω — 차단 · 0.195 V ≈10 · 0.068 V ≈21 · 0.005 V ≈39 Ω) · `Ea` ≈20 < 액체 >40("solvation-free") · `CPE_CT-P` "significantly lower than unity, suggesting a reaction distribution" | 22(1) / 27.5(3) |
| `W_O` | 2차 입자 안 Li 수송(상변화 경계 이동) | 저주파 직선 | — |

- `[인쇄]` "For properly evaluating RCT, it is clear from Figure S2 that two-electrode configuration can hardly be applicable and the three-electrode cell setup
  is mandatory."
- `[인쇄]` `R_X` 의 `Ea` 가 가장 높아 "could be an important rate-limiting step at low temperatures".
- `[재현]` `R_SE` = 0.06 / (2.6×10⁻³ × 0.79) = **29.2 Ω** ✓ — ★ **3전극 옴 몫이 기준극 위치로 정해진다는 것을 저자가 직접 계산해 인쇄한
  계보 첫 사례**(40호에서 우리가 세운 줄 — 여기서는 WE–RE 0.6 mm 층 전부가 WE 채널로).
- `[해석]` **`R_CT` 의 신품 `Ea` 22(1) 은 `R_SE` 22.9(7) · LPSI 벌크 문헌 22 와 구별되지 않는다.** 저자는 "용매화 없음" 으로 읽지만
  **복합체 안 SE 이온 경로(TLM 이온 저항)**도 같은 `Ea` 를 준다 — 그리고 `CPE_CT-P` 0.45 는 이상 전송선 45° 의 P = 0.5 와
  같은 자리다. 19호 `[인쇄]` "계면 `Ea` 가 낮은 쪽 SE 벌크 `Ea` 와 같은 정도" 와 같은 모양. 10호 §"EIS 는 대가를 받는다"(전하이동
  ↔ 기공 이온 저항 축퇴)의 **음극 실측 표본**이다.

## 3.5 RT 500 사이클 — Fig. S7

`[인쇄]` "There is no significant change in the Nyquist plot, except for a slight increase in RSE" · 0.05 C 곡선 · dQ/dV 도
"support the good cyclability". ⚠ SI Fig. S7a(1.0 C) 는 크로퍼가 아래 띠만 잘라(fig_S7.png) **쪽 전체를 따로 렌더해 봤다**:
`[도표]` 1.0 C 탈리튬 용량 **≈120 → ≈95 mAh g⁻¹(−≈21 %, 500 사이클)** · 0.05 C 는 ≈225 → ≈220. **저율 용량은 보존, 1 C 용량은 −21 %** —
`[해석]` 율 의존 손실(동역학)이 있는데 Nyquist 는 "변화 없음" 으로 적혔다(D10).

## 3.6 333 K 가속 — Fig. 4 · 5 · S8 · Table 2 · 3

- `[인쇄]` 초기 용량은 RT 보다 크지만 50 사이클에 빠르게 열화(Fig. S8). `[도표]` S8a 1 C·333 K: ≈157 → ≈150 → ≈140 mAh g⁻¹(1 · 30 · 50번째).
- **Fig. 4 (0.05 C · 298 K 전후)**: `[도표]` 흑연 탈리튬 **≈223 → ≈168**, 리튬화 ≈222 → ≈173 mAh g⁻¹ ⇒ **용량 비 ≈0.75–0.78**.
  `[인쇄]` ≈10 mV 음의 이동이 흑연 · Li-In 둘 다 — R-LTO 탓 "could be", "the influence was limited".
- `[인쇄]` dQ/dV: "every peak intensity … is decreased. This means that capacity decrease mainly resulted from the loss of the active material."
- **Table 3 (@293 K)**:

| | 전 | 후 | 비 |
|---|---:|---:|---:|
| `R_SE` / Ω | 29.4(2) | 47.0(2) | ×1.60 |
| `R_X` / Ω | 4.50(7) | 39.9(8) | ×8.87 |
| `CPE_X-T` / "F" | 6.7(4)E-6 | 3.5(6)E-5 | **×5.2(증가)** |
| `CPE_X-P` | 0.74(4) | 0.48(1) | |
| `R_CT` / Ω | 22.8(7) | 48.95(8) | ×2.15 |
| `CPE_CT-T` / "F" | 0.045(6) | 0.020(5) | ×0.44 |
| `CPE_CT-P` | 0.45(4) | 0.72(1) | |

- `[인쇄]` "The RX value significantly increased, whereas RCT and RSE was doubled" · `R_X` 증가 = 고온에서 가속된 SE 분해,
  "the most serious cause of degradation" · `R_CT` 배증 = "the decrease in the electrode−electrolyte interface area (for ionic paths) caused by
  the solid electrolyte decomposition" · "The decrease in the CPE constant (CPEx-T and CPECT-T) also suggests the loss of contact area."
- `[인쇄]` `Ea`: "RSE and RCT were nearly unchanged … whereas the activation energy of RX considerably decreased" ⇒ 계면의 SE 변성(Li₃P 등)이
  계면상의 성질을 바꿨다.
- `[도표]` Fig. 5b 재판독: `R_X` 전 기울기 ≈53.6 · 후 ≈27.7 · `R_SE` 전 ≈22.3 · 후 ≈27.7 · `R_CT` 전 ≈21.5 · 후 ≈24 kJ mol⁻¹ —
  인쇄값과 1–3.5 kJ 안.

## 3.7 결론 (p7)

네 성분 배정(`[인쇄]` "assigned in Sections 3.1 and 3.2" — 실제는 3.3 절, D9) · `R_X` 는 첫 리튬화에서만 자라 초기 비가역의 원인 ·
RT 는 거의 열화 없음 · 333 K 급속 열화의 원인은 `R_X` 증가 = SE 의 환원 분해 · 변성. 입도 · 혼합비 · 혼합법 최적화에 쓰일 것을 기대.

# 4. ★★★★ 음극 쪽 열화 분해 — 측정과 해석의 경계

## 4.1 무엇이 측정인가

| 층 | 무엇 | 층위 |
|---|---|---|
| 전극별 곡선 | 흑연 · Li-In 전위를 R-LTO 대비로 따로(0.05 C, 전후) | **measured**(단 vs Li 는 1.55 V 가정) |
| 성분 저항 | `R_SE` · `R_X` · `R_CT` + CPE T · P, 전후, ± | **fitted**(Z-View, 회로 고정, ± = 적합 표준오차) |
| `Ea` | 성분별 5 온도 Arrhenius, 전후, ± | **fitted of fitted**(회귀 표준오차) |
| 용량 손실 → `LAM` | dQ/dV 봉우리 높이 감소 한 문장 | **해석** |
| `R_CT` → 면적 손실 | `R` 배증 + CPE-T 감소 | **해석**(CPE_X-T 는 반대로 움직였다 — D4) |
| `R_X` → SE 분해 | 첫 리튬화 · LSV · LGPS 대조의 정성 일치 + 가속 후 ×8.9 | **해석**(대조 실험 셋이 신품 쪽에서 받친다) |

## 4.2 ★★★★ 반쪽전지라서 음극 곱 축퇴가 순수해진다 (`[해석]`)

WE 흑연 ↔ CE Li-In(`[재현]` Li 박 0.151 mmol ≈4.0 mAh ↔ 흑연 0.6 mg 이론 0.22 mAh ⇒ 재고 ≈18 배) — **Li 는 CE 가 대 준다.** 그러므로 WE 0.05 C 용량 손실에 `LLI` 는 안 들어가고
남는 것은 **`LAM_NE`(물질 자체) · 고립(`θ`: 전자 · 이온 경로 단절) · 동역학(저율에서 작다)** 셋이다. 0.05 C 에서 `[재현]` 추가 옴 강하
≈1 mV(§5.4) 라 동역학은 무시 가능 ⇒ **용량 비 0.75–0.78 = (1 − `LAM_NE`)·θ 한 곱.** 원전의 "loss of the active material" 은 이 곱에 이름
하나를 붙인 것이다 — **양극 쪽 카드 물음(`LAM_PE` ↔ 접촉)과 같은 구조가 음극에서 그대로 선다.**

## 4.3 dQ/dV 봉우리 높이가 `LAM` 모양이 아니다

순수 `LAM`(같은 흑연이 비례로 사라짐)이면 모든 봉우리가 **같은 비(≈0.76)** 로 준다. `[도표]` Fig. 4d 화소 판독(1 화소 ≈0.74 mV · ≈30 단위):

| 봉우리 | 위치 전 → 후 (V) | 높이 전 → 후 | 비 |
|---|---|---:|---:|
| 탈리튬 stage2→… (≈0.08) | 0.0755 → 0.063 | 3366 → 1798 | **0.53** |
| 탈리튬 (≈0.12) | 0.118 → 0.104 | ≈5800 → 3514 | **≈0.61** |
| 탈리튬 dilute (≈0.21) | 0.207 → 0.186 | 999 → 1028 | **1.03** |
| 리튬화 (≈0.06) | 0.061 → 0.046 | ≈5600 → 3914 | **≈0.70** |
| 리튬화 (≈0.10) | 0.102 → 0.087 | 4979 → 3203 | **0.64** |

⇒ **주 봉우리는 용량 비보다 더 줄고(0.53–0.70), 0.2 V 봉우리는 안 준다(1.03).** `[해석]` 높이 감소의 일부는 **넓어짐**(분극 분포 ·
불균일 — `CPE_CT-P` 가 변했다)이고, 봉우리 모양은 "균일 비례 손실" 을 지지하지 않는다. 원전의 "every peak" 는 0.2 V 봉우리에서
어긋난다(D11). **`LAM` 배정은 높이가 아니라 봉우리 넓이(G6)로 해야 했다.**

## 4.4 ★★★★ 두 채널의 크기 대조 — 면적 손실 > 용량 손실 (`[재현]`, §5.2)

| 채널 | 비(후/전) | 무엇에 비례 |
|---|---:|---|
| 0.05 C 용량 | **0.75–0.78** `[도표]` | 연결된 활물질 = (1 − `LAM_NE`)·(1 − `u`) |
| `R_CT` 호 1/`R` | 0.47 | 면적 × 고유 속도 |
| `R_CT` 호 `C_eff` | **0.43 ± ≈0.2** | 면적(전제 `C ∝ A`) |
| `R_CT` 호 τ | 0.92 | 면적 약분(고유 시상수) |

`[해석]` `C` 비 ≈ 1/`R` 비 · τ 거의 불변 ⇒ `R_CT` 배증은 **면적 서명**(원전 해석과 같은 방향 — 이 점에서 원전은 우리 처방 1단계로 지지된다).
그런데 면적이 ×0.45 인데 용량은 ×0.76 ⇒ 면적 손실의 **대부분은 통째 고립(`u`)이 아니라 연결된 입자의 표면 피복 감소(`φ`, `A_eff`)** 여야 한다:
`(1−u)·φ ≈ 0.45` · `(1−u)(1−LAM) ≈ 0.76` — 식 둘에 미지수 셋. **`u` 와 `LAM_NE` 는 한 곱 안에 남는다** — 이 편의 어떤 채널도 그 둘을 가르지 않는다.

⚠ **이 대조의 전제 셋**: (i) `C_eff ∝ 접촉 면적`(18 · 19호에서 두 번 깨졌다) — 그리고 여기 `C_eff` ≈20–46 mF 는 이중층 상한의 수백–수천 배(§5.3):
이 호의 `C` 가 이중층이 아니라면 "면적 서명" 이라는 읽기 자체가 서지 않는다 · (ii) P 가 0.45 → 0.72 로 바뀌어 두 T 의 차원이 다르다(τ 가 `R·Q` ≈1 근처라
P 에 둔감한 것은 우연한 행운) · (iii) EIS 는 만리튬 상태, 용량은 전 구간.

## 4.5 ★★★ 3-a `Ea` 가 1단계와 반대로 말한다 — 그리고 세 값이 모인다

- 면적만 잃으면 `Ea` 불변(19호 채널). `R_CT` 는 **22(1) → 27.5(3)**(+5.5, 인쇄 ± 로 ≈5σ). 원전 "nearly unchanged" 는 자기 ± 와 맞지 않는다(D5).
- `[재현]` 전지수가 같다면 +5.5 kJ mol⁻¹ 은 293 K 에서 ×9.6 이다 — 관측 `R` ×2.15 ⇒ 전지수가 ×0.22 로 **줄어야**(면적이 **늘어야**) 한다.
  **1단계(면적 ×0.43)와 3-a(면적 ×≈4.5)가 같은 호에서 반대 방향** — 19호 검사 B("`C` 와 `Ea` 가 70 배 충돌")의 **동일 계면 · 동일 셀판**이다.
- ★ **노화 뒤 세 성분의 `Ea` = 27.6(3) · 27(3) · 27.5(3)** — 하나의 값. `[해석]` 가장 단순한 읽기는 **노화 뒤 세 호가 하나의 공통 과정(변성 SE 이온 수송)에
  지배되거나, 적합이 세 호를 가르지 못한다**는 것이다. 어느 쪽이든 노화 후 성분별 배정(`R_X` = "most serious cause")은 이 수렴 위에 있다. 원문 무언급.

## 4.6 원전 결론의 자리

`[해석]` 원전의 "333 K 열화의 원인 = SE 환원 분해(`R_X`)" 는 **저항 쪽 명제**로는 지면이 받친다(첫 리튬화 · LSV · LGPS 대조 + ×8.9). 그러나
**용량 손실 25 % 를 `R_X` 에 잇는 고리는 없다** — 0.05 C 에서 `R_X` 40 Ω 이 만드는 강하는 `[재현]` <0.5 mV 다. 용량은 "LAM" 으로, 저항은
"SE 분해" 로 **따로 배정되고**, 결론 문장("the rapid decrease in capacity at 333 K is due to reductive decomposition and denaturation")에서 **이어진다**.
이것이 서른다섯 번째 성질(§6 Q4)이다.

# 5. `[재현]` 검산

## 5.1 화소 판독 (원본 크롭 래스터)

- **Fig. 4d** 틀 x 1315–1720.5 px = 0–0.30 V, y 681–1086.5 = +6000 … −6000. 봉우리 표는 §4.3. 탈리튬 0.12 V 검은 봉우리는 상단 틀 근처라 판독 상한
  5527 → 그림 겉보기 ≈5800.
- **Fig. 4a**(Li-In) 틀 y 106–483 = 1.00–0.00 V vs Li(1 화소 2.65 mV): 전 두 선 ≈0.610 · 0.605(중점 **0.609**, 폭 ≈5 mV) · 후 ≈0.600 · 0.584(중점
  **0.593**, 폭 **≈17 mV**) ⇒ 중점 **−16 mV** · Li-In 히스테리시스 ×≈3(상대극 분극 증가).
- **Fig. 4b** 틀 x 1331–1694 = 0–300 mAh g⁻¹: 탈리튬 끝 223 → 168 · 리튬화 끝 222 → 173.
- **Fig. 1b** Li-In 평탄 **0.604 V vs Li**(행 247–252, ±3 mV).
- **SI Fig. S7a**(쪽 렌더 130 dpi): 1 C 탈리튬 끝 ≈120.5 → ≈95.1 mAh g⁻¹.

## 5.2 1단계 — CPE → 유효 커패시턴스

`τ = (R·Q)^{1/P}` · `C_eff = τ/R`(Table 3, 293 K):

| 호 | 상태 | τ | `C_eff` | 꼭짓점 1/(2πτ) |
|---|---|---:|---:|---:|
| `R_X` | 전 | 0.78 µs | 0.17 µF | 205 kHz |
| `R_X` | 후 | 1.13 µs | 0.028 µF | 141 kHz |
| `R_CT` | 전 | 1.06 s | **46 mF** | 0.15 Hz |
| `R_CT` | 후 | 0.97 s | **20 mF** | 0.16 Hz |

- `R_CT`: `C` 비 **0.43**, 1/`R` 비 0.47, τ 비 0.92. 오차 전파(T 의 ± 만, `R·Q` ≈1 이라 P 둔감): `C` 비 ±≈0.2 ⇒ 순수 동역학(1.0)은 ≈2.8σ 밖.
- `R_X`: `C` 비 0.16, 1/`R` 0.113, τ ×1.45 — 그러나 전 상태 P ±0.04 가 `ln τ` 에 ±0.76(×2.1)을 준다 ⇒ **`R_X` 의 분해는 이 표로 안 정해진다**.
  (막이면 두께 증가도 면적 감소와 같은 서명 `C ∝ 1/R` 을 준다 — τ = ρε 만 막 성질.)
- 꼭짓점 0.15 Hz ⇒ 원문 "around 0.10 Hz"(3.4 절 둘째 서술)가 맞고 첫 서술 "around 1 Hz" 가 어긋난다(D6).

## 5.3 3단계-b — `C` 물리 상한

`[추론]` 흑연 0.6 mg(G4 복합체 읽기) · 밀도 2.2 g cm⁻³(우리 가정) · D 11.2 µm ⇒ 식 (4) 기하 표면 **1.46 cm²** · 이중층 10–50 µF cm⁻² ⇒ **15–73 µF**.
`R_CT` 호 `C_eff` 20–46 mF 는 그 **≈270–3,200 배**(흑연 3.0 mg 읽기여도 55–630 배). ⇒ **"전하이동" 호의 `C` 가 이중층이 아니다** —
계보에서 네 번째(19호 `P2` · 20호 `R_ct` · 21호 저주파 호에 이어). `[해석]` 후보: 흑연의 화학(삽입) 커패시턴스 — 21호가 In/In₁Li₁ 2상 평탄의
큰 dQ/dE 로 읽은 것과 같은 부류(흑연도 단계 2상 평탄) · 복합체 이온 경로의 분포 요소. 어느 쪽이든 **`C ∝ 접촉 면적` 전제가
이 호에서 설 근거가 없다** — §4.4 의 면적 서명은 그 조건부다.
`R_X` 호 0.17 µF 는 `[추론]` ε_r 10 · 기하 표면 1.46 cm² 면 두께 ≈75 nm 급 층 — 표면막 귀속과 자릿수 양립.

## 5.4 4단계 — DC 히스테리시스 ↔ EIS `ΔR`

EIS 저항 증가 합 `ΔR` = 35.4 + 26.2 + 17.6 = **79 Ω**. 0.05 C 전류 ×2(리튬화 · 탈리튬화 반대 방향):
- 흑연 0.6 mg(복합체 3.0 mg 읽기) → 11.2 µA → **1.8 mV**
- 흑연 3.0 mg 읽기 → 55.8 µA → **8.8 mV**

`[도표]` dQ/dV 봉우리 쌍의 간격 증가 = 리튬화 이동 −15 vs 탈리튬화 −13.5 ⇒ **≈+1.5 mV**(판독 ±1.5). ⇒ **복합체 읽기와 맞고 흑연 3.0 mg 읽기와 안 맞는다** —
G4 의 모호성을 4단계가 푼다(`[추론]`, 판독 한계 근처).

## 5.5 공통 모드 표류

저항 증가는 리튬화 봉우리를 **음**, 탈리튬화를 **양**으로 민다. 관측은 **둘 다 음**(−13 … −21 mV) ⇒ 공통 모드 ≈**−14 mV**(흑연 쌍 평균) · Li-In 중점 **−16 mV** —
두 증인이 같은 방향 · 같은 크기 ⇒ 인쇄 "ca. 10 mV … both" 와 판독 한계 안에서 맞다. SI Fig. S8c(333 K 사이클 중) 봉우리도 1 → 50번째로 **리튬화 · 탈리튬화 둘 다
왼쪽으로 진행**(`[도표]` ≈−5 mV) — 표류가 가속 사이클 **동안** 쌓였다는 정성 증거. ⚠ Li-In 쪽 공통 모드는 Li-In 자신의 조성 변화와도 겹칠 수 있다(반쪽전지 비가역
Li 소모 — `[재현]` 재고 대비 소모는 작아 평탄 안이 유력).

## 5.6 R-LTO 절대값 — 증인 값을 원전으로 바꾸면

Li-In 판독 −0.946 V vs R-LTO 에 42호 원전 **0.622 V** 를 넣으면 R-LTO ≈ **1.568 V**(인쇄 증인 0.60 이면 1.546). ⇒ 40호 1.5745 · 41호 ≈1.575 에 이은
**세 번째 ≈1.57** — `[해석]` 계보가 쓰는 1.55 V 와 In 가지 원전 사이에 ≈20 mV 가 반복해서 남는다. ⚠ SE(LPSI ↔ LGPS ↔ LPSCl) · 셀 · 조성 다름, 판정 아님.
그리고 이 편이 [44] 에서 가져온 "0.60 V" 는 그 원전이 인쇄한 0.62/0.622 가 아니다(D13).

## 5.7 기타

- LSV 시간 2.0 V / 23 µV s⁻¹ = **24.2 h** — 원문 "almost the same as … first charge step at 0.05C"(공칭 20 h) ✓.
- `R_X` 이력: Fig. 2d(조건화 뒤, ≈298 K 추정) ≈1.5–2 Ω ↔ Table 3 "전"(RT 500 사이클 뒤, 293 K) 4.50 Ω. 온도로 `[재현]` ×1.44(`Ea` 53) → ≈2.6 Ω —
  남는 ×≈1.7 은 RT 사이클 중 `R_X` 증가로 읽힌다(원문 "no significant change except RSE" 와 긴장, 상태 · 측정 조건이 달라 판정 아님).

# 6. 우리 축 (Q1–Q8)

| Q | 판정 |
|---|---|
| **Q1** 정량 | **없다 — `θ(N)` 0/43.** 식 (4) 의 `[인쇄]` "total surface area … **or** the interface area" = `θ ≡ 1` 인쇄. 접촉 손실은 CPE-T 해석 한 문장(그중 하나는 반대 방향, D4). 입도 축은 **비가역 용량의 면적 비례**(첫 리튬화)이지 접촉 분율이 아니다 |
| **Q2** 독립관측 | **반 칸 검토 후 접음.** 채널 셋(3전극 EIS R · T · P 전후 ± · `Ea` 전후 · 전극별 dQ/dV)이 한 셀에 있고 1단계 입력은 계보 최완비. 그러나 원전은 **채널별로 다른 기구를 배정**했을 뿐 가르지 않았다. 가른 것은 우리 계산(§4.4)이고 두 면적-불변 채널이 충돌한다(§4.5) |
| **Q3** 라벨 층위 | 층 하나 — **"완전한 CPE 삼중(R · T · P) ± 가 노화 전후 둘 다"**(18호는 전 상태 P 만 · `C` 에 ± 없음). ± 는 적합 표준오차뿐, n = 1, 전후가 같은 셀의 누적 이력(RT 500 → HT 50). 표 온도 "@293 K" ↔ 본문 298 K(D1) |
| **Q4** 유일성 | **0/43 — 서른다섯 번째 성질 "채널별 명명 — 같은 셀의 같은 열화를 용량 채널은 `LAM`, 임피던스 채널은 면적 · SEI 로 나눠 부르고, 두 채널의 크기를 대조하지 않았다"**. 그리고 노화 뒤 세 `Ea` 의 수렴(27.6 · 27 · 27.5)을 "불변" 두 개와 "감소" 하나로 읽었다. `identifiab` · `uniqu*` · `uncertaint` · `degenera*` · `error` 0 |
| **Q5** Li-In / 기준극 | **+0.5 — 열아홉 번째 형태 "공통 모드 표류 판독"**: 두 평탄 증인(작업전극 흑연 · 상대극 Li-In)이 **같이** 음으로 ≈10 mV(인쇄) · `[도표]` ≈−14 / −16 mV 움직인 것을 기준극 표류로 읽었다 — R-LTO 가지 첫 표류 값, 첫 가속 열화 뒤 값. **반 칸**: "could" · n = 1 · 두 시점 · 같은 지면이 합 일치로 "proves the stability" · 1.55 V 는 "Suppose" + [40,41] 인용. 증인 하나는 새 종류(**작업전극 자신의 단계 평탄 셋**, 문헌값 미인쇄). 부호 오기 D7 = 계보 세 번째 컷오프 부호 오기(40호 D1 · 41호 D2) |
| **Q6** 압력 | 이동 없음 — 조립 110 · Li-In 압착 ≈100 MPa, 운전 압력 0, `pressure` 0 회. void · crack 은 서론 인용뿐 |
| **Q7** dead Li | 해당 없음 — 흑연(0 V 컷오프는 1.55 V 가정 위; `[재현]` R-LTO 가 1.568 이면 실제 컷오프 ≈+18 mV) |
| **Q8** 화학 · OCP | 해당 없음(양극 없음). 칸 밖: **ASSB 안 흑연 준-OCP**(GITT, 0.195 · 0.110 · 0.068 V) — 단계 평탄이라 음극 판 `(X1, X3)` 형 평탄 축퇴의 재료 |

# 7. ★★★ 곱 축퇴 처방 — 스물여섯 번째 적용 (음극 첫 적용)

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | Table 3 — `R` · T · P 전후 ± (두 호) | ✅ **완비(계보 첫 — 전후 모두 P 와 ±)**. `R_CT`: `C` ×0.43 ± 0.2 ≈ 1/`R` ×0.47, τ ×0.92 ⇒ 면적 서명 · `R_X`: P 오차로 미정 |
| **2단계** 면적 대조군 | 입도 3 종 — 2전극 · 다른 공급처 · 첫 리튬화 비가역만(EIS 0) | ⚠ 면적 비례를 **비가역 용량**에서 보인다((B)·D ±14 %) — `R·C` 대조군은 아님 |
| **3단계-a** `Ea` | 5 온도 × 전후 × 세 성분 | ✅ 입력 완비(40호가 바란 "노화 셀 한 쌍") — ❌ **결과가 1단계와 충돌**: `R_CT` `Ea` +5.5 kJ mol⁻¹, 세 성분이 27.5 로 수렴 |
| **3단계-b** `C` 물리 상한 | `C_eff` | ❌ `R_CT` 호 20–46 mF = 이중층 상한 ×270–3,200 — "전하이동" 이 **네 번째로** 상한을 넘는다 · `R_X` 0.17 µF 는 막 자릿수 |
| **4단계** 시간 영역 | 0.05 C dQ/dV 봉우리 간격 ↔ EIS `ΔR` | ✅ 복합체 질량 읽기에서 1.8 ↔ ≈1.5 mV (흑연 3.0 mg 읽기면 ❌) |

**⇒ 처방에 더하는 것**:
1. **새 줄 "면적 서명 ↔ 저율 용량 비 대조 — 반쪽전지 음극에서"**: 1단계가 면적 서명을 주면 그 비를 **같은 셀 저율 용량 비**와 댄다.
   면적 비 < 용량 비 ⇒ 면적 손실의 일부는 연결된 입자의 피복(`A_eff` — 37호 `k` 쌍둥이)이지 통째 고립이 아니다. 반쪽전지(Li 저장소)는 `LLI` 를
   지워 용량 채널을 `(1−LAM)(1−u)` 한 곱으로 만든다 — **음극 판 곱은 순수하게 남는다**.
2. **1단계와 3-a 가 같은 호 · 같은 셀에서 반대로 말할 수 있다** — 19호(다른 계면)에 이어 **동일 계면 · 노화 전후** 첫 충돌. 두 채널 다 "면적-불변 조합" 이라는
   같은 이름을 갖지만 전제가 다르다(`C ∝ A` ↔ 전지수 = 면적). 3-b 가 먼저 실패하면(이 호) 1단계 쪽 전제가 약하다.
3. **노화 뒤 `Ea` 수렴은 경고등**: 여러 호의 `Ea` 가 한 값으로 모이면 성분별 배정 전에 **적합이 호를 가르는가**(근최적 폭)를 먼저 본다.

⚠ **이것이 곱을 푼 것은 아니다.** n = 1 · 같은 셀 누적 이력 · `C ∝ A` 전제가 3-b 에서 약함 · 용량은 그림 판독 · 봉우리 넓이 없음.
기여는 **음극 판 곱의 형태(반쪽전지에서 `LAM_NE` ↔ 고립 두 항)** 와 **두 채널 크기 대조의 첫 표본**, 그리고 **1단계 ↔ 3-a 의 동일 계면 충돌**이다.

# 8. 어긋남 (실제로 어긋난 것만)

| # | 어디 | 무엇 |
|---|---|---|
| **D1** | Table 3 ↔ 3.5 절 · Fig. 5 | 표 "@293 K" ↔ 본문 "impedance measured at 298 K" |
| D2 | 3.3 절 ↔ Table 3 · 2.2 절 | `R_SE` "28 Ω" ↔ 29.4(2) Ω · 면적 0.79 ↔ 0.78 cm² |
| **D3** | 3.5 절 ↔ Table 3 | "RCT and RSE was doubled" ↔ `R_SE` ×1.60 |
| **D4** | 3.5 절 ↔ Table 3 | "**decrease** in the CPE constant (CPEx-T and CPECT-T)" ↔ `CPE_X-T` 6.7E-6 → 3.5E-5(**×5.2 증가**) — 접촉 면적 손실 논거의 절반이 자기 표와 반대 |
| **D5** | 3.5 절 ↔ Table 2 | `R_SE` · `R_CT` `Ea` "nearly unchanged" ↔ +4.7(±0.8) · +5.5(±1.0) kJ mol⁻¹, 자기 ± 로 ≈5–6σ; 세 값이 27–27.6 으로 수렴(무언급) |
| D6 | 3.3 절 두 곳 | `R_CT` "at around 1 Hz" ↔ "at around 0.10 Hz" — `[재현]` 꼭짓점 0.15 Hz |
| **D7** | 2.3 절 ↔ SI Fig. S4 | 2전극 컷오프 "0.60 and −0.40 V vs the Li−In"(= 0 · 1.00 V vs Li) ↔ S4 축은 흑연 − Li-In(0 V vs Li = 바닥 ≈−0.58 쪽) ⇒ −0.60 · +0.40 이어야 — **계보 세 번째 부호 오기**(40호 D1 · 41호 D2) |
| D8 | 2.1 절 · Table 1 ↔ 3.2 절 · SI S4 | D50 11.2 ↔ "11.0 µm"(NG-10); 입도 시료(SEC carbon)와 3전극 시료(Mitsubishi)가 다른 분말(G8) |
| D9 | 결론 | "assigned in Sections 3.1 and 3.2" ↔ 배정은 3.3 절 |
| **D10** | 3.4 절 · 초록 ↔ SI Fig. S7a | RT "few changes … in the charge−discharge profile" ↔ `[도표]` 1 C 용량 ≈120 → ≈95(−21 %) |
| **D11** | 3.5 절 ↔ Fig. 4d | "every peak intensity … is decreased" ↔ `[도표]` 0.21 V 탈리튬 봉우리 ×1.03 |
| D12 | 3.5 절 ↔ Fig. 4 캡션 | 본문 "Figure 4(a,b) … graphite working and Li−In counter" ↔ 캡션 · 그림 (a) Li-In · (b) 흑연 |
| **D13** | 3.1 절 ↔ ref 44(42호) | Li-In "0.60 V … agrees with the literature value⁴⁴" ↔ Santhosha 인쇄 0.62 / 그림 0.622 |
| D14 | 참고문헌 | ref 32 쪽 "No. 2328644" ↔ 232864(18호) · ref 25 에 Angew. 2022 e202201249(ref 23 의 번호)가 붙어 있다 |
| D15 | 3.3 절 · SI S2 | 안정성 "proves" ↔ 같은 지면 3.5 절 "could be caused by the change of the R-LTO reference electrode potential" — 한 편 안의 긴장 |

# 9. 그림 — 무엇을 봤나

크로퍼 16 장(본문 그림 5 · SI 그림 8 · 표 3). **그림 13 장 중 9 장 봤다**: Fig. 1 · 2 · 4 · 5 · S2 · S4 · S5 · S7 · S8.
화소 판독: Fig. 1b · 4a · 4b · 4d · S7a. ⚠ **fig_S7.png 는 아래 띠(1890 × 392)만 잘렸다** — SI 8 쪽을 130 dpi 로 따로 렌더해 봤다(저장소에 넣지 않음).
**안 본 것**: Fig. 3(신품 Arrhenius — Fig. 5b 가 같은 "전" 점을 담는다) · S1(GITT — 값은 본문 인쇄) · S3(LSV) · S6(LGPS). 표 3 장은 PDF 텍스트로.
**본문과 어긋난 그림**: Fig. 4d(D11) · Fig. 4 순서(D12) · S4(D7) · S7a(D10). Fig. 2d 는 `R_CT` 0.58 V 값을 2.770×10¹² Ω 로 축 꺾어 인쇄(차단 전극 — 본문과 맞음).

# 10. 참고문헌 중 후속 후보 (54 번 중 — 미열람, 서지는 지면 그대로)

| 서지 | ref | 왜 |
|---|---|---|
| Kuratani · Sakuda · Takeuchi · Kobayashi 2020 *ACS Appl. Energy Mater.* 3, 5472 | 24 | 황화물 ASSB 흑연 용량 열화의 **void 형성 기구** — 음극 판 `θ(N)` 후보 |
| Otoyama · Sakuda · Hayashi · Tatsumisago 2018 *Solid State Ionics* 323, 123 | 25 | 흑연 복합음극 **광학 현미경 operando** — 음극 접촉 관찰 |
| Lee · … · Ahn 2022 *ACS Appl. Energy Mater.* 5, 5227 | 26 | 탄소계 복합음극 **crack healing by stack pressure** — Q6 음극 판 · 압력 되돌림 처방 |
| Höltschi · … · Novák 2020 *J. Electrochem. Soc.* 167, 110558 | 27 | 리튬화 흑연 ↔ 황화물 반응성 — `R_X` 화학의 독립 근거 |
| Yu · … · Fukutsuka 2022 *Electrochemistry* 90, 037003 | 30 | 흑연판 \| Li₂S–P₂S₅ 계면 이동 동역학(3전극, 액체 결합) — `R_CT` `Ea` 대조 |
| Colbow · Dahn · Haering 1989 *J. Power Sources* 26, 397 · Ohzuku · Ueda · Yamamoto 1995 *J. Electrochem. Soc.* 142, 1431 | 40 · 41 | 1.55 V 의 18호 · 43호 수입 경로(액체 · 1989/1995) |

큐 45–59 인용 **0**(Oh 2022 *Angew.*(ref 23)는 큐 53 Oh…Choi 2025 *AEM* 과 다른 편).

# 11. 이 digest 가 주장하지 않는 것

- **"`R_CT` 배증은 면적 손실이다" 라고 주장하지 않는다.** 1단계는 면적 서명을 주지만 3-b 가 그 호의 `C` 를 이중층으로 보기 어렵게 만들고, 3-a 가 반대 방향을 준다.
  주장은 **"원전의 면적 해석이 1단계로는 지지되고 3-a 와는 충돌한다"** 까지다.
- **"용량 손실은 `LAM_NE` 가 아니다" 라고 주장하지 않는다.** 주장은 dQ/dV **높이**가 균일 비례 모양이 아니고, 용량 채널이 `LAM_NE` 와 고립을 한 곱으로만 본다는 것까지다.
- **공통 모드 −14 mV 를 기준극 표류로 확정하지 않는다** — 원문도 "could" 다. Li-In 조성 변화 · 흑연 쪽 평형 이동이 같은 방향으로 겹칠 수 있다(작다고 추정할 뿐).
- **R-LTO ≈1.568 V 를 측정값으로 쓰지 않는다** — 다른 SE · 다른 셀의 원전 값을 넣은 산술이다.
- `[도표]` 값(용량 · 봉우리 · Li-In 중점)은 크롭 래스터 판독이다 — 판독 폭을 각 줄에 적었다. **우리 연구 수치(artifact · `RESULTS*.md`)와 비교하지 않았다.**

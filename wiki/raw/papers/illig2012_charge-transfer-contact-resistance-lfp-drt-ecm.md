---
title: "Illig, Ender, Chrobak, Schmidt, Klotz, Ivers-Tiffée 2012 — Separation of Charge Transfer and Contact Resistance in LiFePO4-Cathodes by Impedance Modeling (J. Electrochem. Soc. 159, A952)"
source_url: local-upload/13._Separation_of_Charge_Transfer_and_Contact_Resistance_in_LiFePO4-Cathodes_by_Impedance_Modeling.pdf
source_url_note: "PDF 10 쪽(IOP 표지 1 + 본문 A952-A960, 참고문헌 29 편), SI 없음. ⚠ 액체셀(LFP | LiPF6 EC:EMC | Li). 크로퍼가 9 장을 잡고 벡터 그림 7 장(Fig. 6 · 7 · 11 · 12 · 13 · 14 · 16)을 놓쳐 400 dpi 수동 크롭 + Table I · II 크롭; 자동 fig_10 은 아래 절반만 — fig_10_manual_p6 이 전체. 크롭 Read 8 장(Fig. 9 · 10 · 12 · 13 · 14 · 15 · 16 · Table I). 원자료는 커밋하지 않는다."
source_doi: 10.1149/2.030207jes
source_license: "© 2012 The Electrochemical Society. All rights reserved (open access 표기 없음)"
pdf_sha256: 4b05f7d8bbe0b6fc613ab67473c3659a34ca3b2fddcfe36f05e0144d3cf2f1a8
ingested: 2026-09-23
sha256: 57f8e4bf4ad5a9597b518ee8a8e0bbb4ee433367703687ffe057c2778ae6820e
---

# 수집 목적

`assb` 섹션 **51호**. 큐 **52번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **열셋째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행: "'전하이동과 **접촉저항**의 분리' — 곱 축퇴(`θ`↔`j₀`)를 가르는 방법의 액체셀 원형". 지목 3 회 — 18호 ref [29](저자를 "Chroal" 로 오기) · 11호 ref [9] · 47호 ref [35].
⚠ **액체셀이다** (LiFePO₄ \| 1 M LiPF₆ EC:EMC \| Li 금속). ASSB 칸은 원칙적으로 도구 칸(28 · 31 · 47 · 49호 선례).
이 digest 의 1순위 물음: **"접촉 저항" 과 "전하이동" 을 무엇으로 갈랐나 — 조작 · 주파수 대역 · 온도(`Ea`) · 커패시턴스 중 어느 것이고, 가른 근거가 측정인가 가정인가. 그리고 이 "접촉" 이 카드의 접촉(CAM\|SE 이온 접촉, `θ`)과 같은 물리인가.**

J. Illig, M. Ender, T. Chrobak, J. P. Schmidt, D. Klotz, **E. Ivers-Tiffée**(마지막 저자) —
**"Separation of Charge Transfer and Contact Resistance in LiFePO₄-Cathodes by Impedance Modeling"**,
*J. Electrochem. Soc.* **159** (7) A952–A960 (**2012**), doi `10.1149/2.030207jes`.
`[인쇄]` 투고 2012-02-22 · 수정본 2012-03-26 · 게재 2012-07-17 · "This was Paper 1061 presented at the Las Vegas, Nevada, Meeting of the Society, October 10-15, 2010." · "© 2012 The Electrochemical Society. All rights reserved."
소속: IWE, Karlsruhe Institute of Technology(전원) + DFG CFN(Ivers-Tiffée). 교신 `joerg.illig@kit.edu`. 자금: BMBF KoLiWIn(03SF0343H) · "Elektrochemie für Elektromobilität – Verbund Süd"(03KP801). 사사: 양극 테이프 캐스팅 Henning Lorrmann(Fraunhofer ISC).

PDF **10 쪽** = IOP 표지 1 + 본문 A952–A960 9 쪽(참고문헌 29 편). SI 없음. sha256 은 frontmatter `pdf_sha256`. 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 눈으로 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ 이 조판의 추출 텍스트는 본문 단위 기호 **Ω 를 떨어뜨린다**("ASR = 178 cm2") — 쪽 렌더로 "Ωcm²" 확인. 그림 · 표는 벡터라 크로퍼가 7 장을 "영역 없음" 으로 놓쳤고 400 dpi 로 수동 크롭했다(§12).

---

# 판정 (먼저)

> ★★★★ **이 편의 "접촉 저항" 은 양극층 \| Al 집전체 계면의 저항이다 — 카드의 접촉(CAM\|SE 이온 접촉, `θ`)과 다른 물리이고, 곱 `A·j₀`(또는 `θ·j₀`)는 건드리지 않는다.** 가른 것은 **직렬로 놓인 두 호(P1C ↔ P2C)의 이름**이고, 한 호 안의 곱이 아니다.
>
> **(a) "접촉" 의 정체.** `[인쇄]` 초록 "(iii) contact resistance (cathode/current collector)" · Table II "Contact resistance cathode/current collector" · Fig. 15 캡션 "contact area cathode /current collector: red". 낱말 `contact` 20 회(줄끝 하이픈 이음) 중 **CAM–전해질 · CAM–탄소 · 입자–입자 접촉은 0** — 예외는 초록 · 결론의 "contact area between cathode/electrolyte and cathode/current collector" 두 곳(전해질 접근 면적에 같은 낱말을 쓴 것). `electronic` 2 회는 서론(LFP 전도도)과 `R0` 정의뿐 — **P2C 를 "전자" 접촉이라 부른 문장은 없다.** `[해석]` 액체셀에서 이온 경로는 집전체를 지나지 않으므로 이 계면을 지나는 전류는 **전자 전류**다 — 물리는 전자 접촉(Al \| 탄소 · LFP 층).
>
> **(b) 무엇으로 갈랐나 — 네 채널, 그리고 각각의 층위.**
>
> | 채널 | 이 편이 쓴 것 | 층위 |
> |---|---|---|
> | **주파수 대역** | DRT(전처리: < 0.1 Hz 에 GFLW + C₀ 적합 → 빼기) 로 봉우리 셋: P1(≈3 Hz) · P2(250 Hz) · P3(1 kHz) at 20 °C | **측정** — 단 정규화 λ 미인쇄("special methods" refs 14 · 21 · 22), 전처리 모형 선택은 "best fit" |
> | **전극 배정** | LFP\|LFP · Li\|Li 대칭셀 DRT 를 반쪽전지와 대조 → P1 · P3 = 양극, P2 = Li | **측정**(대조) — 저자가 재현성 한계를 인쇄("reproducibility … is limited") |
> | **온도(`Ea`)** | 0 · 10 · 20 · 23 · 30 °C, SOC 100 %, 한 셀 — P1C **0.45 eV** · P2C **0.06 eV** | **측정** — ± 0, 셀 1 |
> | **SOC** | 100 → 10 % at 0 °C — P1C 는 ≈×270(7 → 1900 Ω cm², T 와 함께), P2C 는 "generally not SOC dependant" | **측정** |
> | **물리 이름** | P1C = 전하이동: `[인쇄]` "as a transfer process is **always temperature activated**, this clearly points at P1C" · P2C = 접촉: **소거**("the dominant P2C originates from another cathodic process") + T · SOC 무관 + 문헌(Gaberscek 2008, ref 11) | **가정 · 논증** — 측정이 아니다 |
> | **조작(캘린더링)** | 한 쌍(미압연 ↔ 압연): P2C `R` ↓ · 주파수 ↑, P1C `R` ↑ · 주파수 ↓ — "respond readily" | **측정, 방향만** — 크기 0, 셀 1 쌍, 한 조작이 네 원인(두께 20 → 10 µm · 공극률 64.7 → 41.5 % · 전해질 접근 면적 · 집전체 접촉 면적)을 동시에 움직임(저자 스스로 (i) · (ii) 로 나열) |
> | **커패시턴스** | `[인쇄]` 식 (9) `τ_nC = R_nC·C_nC` **한 줄** — `C` · `Q` · CPE 지수 `n` **전수 미인쇄** | **없다** — 처방 1단계 · 3-b 입력을 지면이 주지 않는다 |
>
> ⇒ **가른 근거의 핵심은 온도 채널(`Ea` 0.45 ↔ 0.06 eV)과 SOC 채널이고, 이름은 "전하이동은 늘 열활성" 이라는 가정 + 소거 + 문헌이 붙였다.** 캘린더링은 **이름을 확인하려는 조작**인데 단일 원인 조작이 아니고 크기를 대지 않았다.
>
> **(c) ★★★ 처방 1단계를 지면 수치로 걸면 (`[재현]`, 이상 RC 근사).** Table I 에서 `C = 1/(2πf·R)`: P2C ≈**0.9–1.2 µF cm⁻²** · P1C ≈**2.8–3.5 mF cm⁻²**(기하 면적당, 30 · 0 °C 양끝) — **두 호의 `C` 가 ≈3,000 배 다르고 각 호 안에서는 온도에 거의 불변**(P2C ×0.74 · P1C ×1.23 on 30 → 0 °C). 대역 분리의 실체는 `R` 이 아니라 **`C` 의 세 자릿수 차**다 — 처방의 "C 크기" 채널이 이 편에서 가장 강한 판별자인데 **저자는 쓰지 않았다**.
> ⚠ 이 짝맞춤은 Table I 의 주파수 열 순서를 **뒤집어** 읽어야 선다(D1) — 인쇄 순서 그대로면 P1C 의 `C` 가 30 → 0 °C 에 ×0.012(80 배)로 움직인다.
>
> **(d) ★★★ 캘린더링 쌍의 1단계 (`[도표]` 봉우리 위치만).** Fig. 16b: P1C ≈1 → ≈0.28 Hz(τ ×≈3.5) · P2C ≈1.3 kHz → ≈8 kHz(τ ×≈1/6) · Li 음극 P1A ≈40 → ≈100 Hz(음극도 바뀜, 저자 인정). **두 양극 호 모두 τ 가 움직였다** — 같은 계면 `C`(`C ∝ 그 계면 면적`) 전제에서 면적 서명(τ 보존)이 **아니다**. `R` 비는 DRT 높이 정규화가 Table I 과 맞지 않아(D9) 읽지 않았다.
> `[해석]` 단 **P2C 의 `C` 는 도식상 접촉의 여집합에 있다** — Fig. 15 에서 P2C 의 CPE 가지는 집전체의 **녹색(전해질 접면)** 쪽, 저항 가지는 **빨간(접촉)** 쪽에 그려졌다(원문 문장 없음, `[도표]` 도식). 이 모형이면 접촉 면적 ↑ ⇒ `R` ↓ **그리고** `C` ↓ ⇒ τ 가 크게 ↓ — 관측 방향과 맞는다. 즉 **전자 접촉 호에서는 "C ∝ 접촉 면적" 전제가 뒤집힌다**(C 는 비접촉 면적을 본다). P1C 의 τ ×3.5 증가는 "전해질 접근 면적 감소"(저자 설명)의 순수 면적 서명과 맞지 않는다 — `j₀` · 공극 이온 저항(얇고 치밀해진 층) · 탄소 이중층 몫 중 무엇인지 지면으로 못 가른다.
>
> **(e) ASSB 이식.** **방법의 형태**(DRT 전처리 → 대칭셀 배정 → 온도 · SOC 지도 → 단일 원인 조작)는 옮겨진다. **P2C 의 정체 판별자(`Ea` ≈ 0)는 옮겨지지 않는다**: 18호(Fukunishi 2023, 이 편을 [29] 로 인용)의 **ASSB Al\|복합체 전자 계면 호 R2 는 `Ea` 41–70 kJ mol⁻¹**(18호 Table 1 네 칸 — 70 ± 20 · 41 ± 8 · 60 ± 10 · 43 ± 6; `[인쇄]` "ca. 4 kJ mol⁻¹" 인 액체 문헌 대비, LiNbO₃ 탓으로 추정)이고 같은 셀의 전하이동 호 R3 는 49–63 — **두 호의 `Ea` 범위가 겹친다**. 이 편 P2C 0.06 eV = `[재현]` **5.8 kJ mol⁻¹** · P1C 0.45 eV = 43.4. 액체의 "온도 무관 = 접촉" 규칙을 ASSB 에 그대로 걸면 18호 R2 는 **전하이동과 구별되지 않는다**. 그리고 **CAM\|SE 이온 접촉(`θ`)의 제약 저항은 SE 이온 전도의 활성화를 그대로 지므로**(`[해석]`) 온도 무관 서명을 가질 이유가 없다 — **이 편의 판별자는 전자 접촉 ↔ 이온 과정의 판별자이지 `θ` ↔ `j₀` 의 판별자가 아니다.**
>
> **Q4**: `identifiab*` · `uniqu*` · `ambigu*` · `uncertaint*` · `error` · `standard deviation` · `regulari[sz]*` · `λ` **전수 0**. 대신 비유일성의 **자리**가 둘 인쇄됐다 — (i) 0 °C 에서 P2 · P3 사이 넷째 과정 "neglected in this study because it is not separable from P3" · "The CNLS fit becomes **unstable** when including this additional loss process[es] … and is therefore neglected. Furthermore, this process overlaps with P2C" (ii) Li\|Li 저주파 작은 봉우리들이 "either subtracted with the capacitive diffusion branch Pdiff,c or remain in the pre-processed spectrum. Hence, these clearly visible peaks influence either the obtained values for solid state diffusion or P3." — **빠진 몫이 흘러가는 이웃이 바로 결론의 주인공 P2C(=P3)** 다. 그리고 결론은 "a physically motivated ECM is established **without any a priori settings**". ⇒ **마흔세 번째 성질 "불안정한 적합을 요소 제거로 안정시키고, 제거된 몫이 흘러갈 곳(주인공 호)을 스스로 인쇄한 뒤 '선험 설정 없음' 으로 닫았다"**.
>
> **11 · 18 · 47호가 가져간 것**: 18호 = DRT 참고문헌만([28][29]) — 이 편의 판별 채널(`Ea`)은 18호가 **자기 데이터로 이미 쟀고**, 그 값은 이 편과 **반대 부호의 결론**(ASSB 전자 계면은 열활성). 11호 = "slightly above 10³ Hz … solid-solid contact impedance of LiFePO₄/Al" 대역 이식([19,20] 문장 — 이 편은 11호 목록의 [9]) — 이 편 자신이 P2C 주파수를 **캘린더링으로 ×≈6, 반쪽 ↔ 대칭셀로 ×≈2–3** 움직여 보인다 ⇒ **대역은 그 셀의 R·C 이지 정체가 아니다.** 47호 = LFP 등가회로 R–(R‖CPE)–W("단순화") — `[해석]` 이 편 지도에서 **R‖CPE 하나는 P1C + P2C 를 합친 것**이고, 47호 EIS 온도(10 °C)에서 이 편 LFP 는 P2C(≈150 Ω cm²)가 P1C(≈25)보다 크다(`[도표]` Fig. 12) — 47호의 "LFP `R_CT` 불변" 은 이 편 지도에서는 **접촉 몫이 지배하는 합**일 수 있다(전극이 달라 판정 아님).

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **RQ 요소의 `Q`(또는 `C`) · 지수 `n` 전수 미인쇄.** 식 (2) `Z_RQ = R/(1+(jωτ)ⁿ)` 는 인쇄, 값은 `R`(ASR) · `F_R` 뿐 | 처방 1단계(R·C) · 3-b(C 상한)의 입력이 없다 — §5.2 의 `C` 는 이상 RC 근사의 재현값 |
| G2 | **DRT 정규화 파라미터(λ) · 알고리즘 미인쇄.** "ill-posed and requires special methods" + refs 14 · 21 · 22(Schichlein · Tikhonov · Weese) | 18호 G10 과 같은 구조 — 봉우리 개수(넷째 과정 포함 여부)가 λ 에 달린다 |
| G3 | **셀 수 · 반복 · 산포 0.** 온도 · SOC 지도는 한 셀로 보이고(명시 없음), 캘린더링은 미압연 1 · 압연 1 | `Ea` · ASR 에 ± 없음. "178 ± 50" 은 통계가 아니라 범위(§5.3) |
| G4 | **캘린더링 쌍의 크기 미인쇄** — "decreases … shifts" 방향만 | 1단계를 걸 `R` 비가 없다. DRT 높이는 정규화가 Table I 과 안 맞는다(D9) |
| G5 | **전극 로딩 · 활물질 질량 · BET 미인쇄.** 두께 20 → 10 µm, 공극률 64.7 → 41.5 %(FIB/SEM; 앞 값은 ref 29 Ender 2011) 만 | `[재현]` 고체 부피 7.06 → 5.85 µm(×0.83, §5.4) — 같은 시트를 압연한 것인지 다른 조각인지 불명. 3-b 의 거칠기 인자 계산 불가 |
| G6 | **"전해질 접근 면적 감소 · 집전체 접촉 면적 증가" 는 측정이 아니다** — FIB/SEM 은 공극률만 인쇄 | 캘린더링 확인 논증의 두 전제가 둘 다 도식(Fig. 15) |
| G7 | **P2C 의 온도 무관을 설명하는 물리 모형 없음** — Gaberscek 2008(ref 11) 에 기댄다 | 전자 접촉의 `Ea` ≈ 0 은 가정이 아니라 관측이지만, 그것이 "접촉" 이라는 이름의 근거가 되는 사슬은 문헌 |
| G8 | **Li 음극 조건 · 셀 치구 · 압착 미인쇄**(Freudenberg FS2019 분리막, 면적 2.54 cm²) | 대칭셀 ↔ 반쪽전지 주파수 차(P2C 1 ↔ 2 kHz)를 "reproducibility" 로 돌렸다 |
| G9 | **Pdiff,C 의 `Ea` 는 "calculated" 라 적고 값 미인쇄**(Table I 빈 칸) | §5.1 `[재현]` 양끝 ≈0.38 eV |
| G10 | **원자료 공개 문장 없음** | 재적합 불가 |

---

# 1. 서지 · 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문은 참고문헌 전까지(그림 안 벡터 글자 포함). 줄끝 하이픈은 이은 판을 병기.

| `identifiab` | `uncertaint` | `confidence interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | **0** |

- NFKC 변경: 본문 **166 자**(`ﬁ` 72 · `²` 61 · `´` 15 · `ﬂ` 8 · `¨` 7 · `…` 3) — **열 변화 0**. 소프트 하이픈 0. 줄끝 하이픈 **97 곳** — 이으면 `contact` 18 → 20 · `contact resistance` 12 → 14 · `capacit*` 20 → 21 · `solid state diffusion` 13 → 14 · `symmetric*` 16 → 17 · `porosit*` 5 → 6 · `prov*` 4 → 3 — **열 변화 0**.
- ⚠ 추출이 본문의 **Ω 를 떨어뜨린다**("ASR = 7 cm2 … 1900 cm2") — 렌더로 Ωcm² 확인.
- 보조(이은 판): `contact` 20(전부 양극 \| 집전체 — 초록 · 결론의 "contact area between cathode/electrolyte" 2 곳은 전해질 접근 면적) · `contact area` 6 · `current collector` 12 · `charge transfer` 19 · `activation energ*` 13 · **`capacit*` 21 — 전부 확산 가지 · 삽입 용량 · 이론 용량, RQ 요소의 커패시턴스 0** · `double layer` **0** · `electronic` 2(P2C 무관) · `carbon` 8 · `calender*` 8 · `surface area` 3 · `pressure` **0** · `fit*` 22 · `residual*` 9 · `Kramers` 4 · `ill-posed` 1 · `regulari[sz]*` · `Tikhonov`(본문) · `λ` **0** · `unambiguous*` 2 · `ambigu*` 0 · `unstable` 1 · `neglect*` 2 · `reproducib*` 2 · `assum*` 2(둘 다 문헌 서술 — "charge transfer resistance is **assumed** as dominant loss process in LiFePO4 cathodes") · `a priori` 2 · `prov*` 3("aims at proving" · "thus proving" ×2) · `SEI` 10 · `aging` 2(Li 음극) · `degrad*` 0 · `error` · `standard deviation` · `uniqu*` 0 · `Gaberscek` 1.
- `[해석]` **이 편의 가정은 `assum*` 이 아니라 "always"("a transfer process is always temperature activated")에 들어 있다** — 21호 "calculated based on" · 43호 "Suppose" · 45호 "therefore exhibited" · 48호 `expect*` 와 같은 부류. 그리고 **"proving" 이 방향만 본 한 쌍 비교에 붙었다**.

---

# 2. 셀 · 실험 (`[인쇄]`)

| 항목 | 값 |
|---|---|
| 양극 | LiFePO₄(탄소 코팅, Süd-Chemie) : 카본블랙 : PVDF = **70 : 24 : 6** wt%, NMP 슬러리, 닥터 블레이드 → Al 박, 80 °C 2 h 진공 → 타발 → 120 °C 3 h |
| 두께 · 공극률 | 미압연 **20 µm · 64.7 %**(ref 29) → 압연 **10 µm · 41.5 %**(FIB/SEM) |
| 음극 | Li 금속 박 0.38 mm(Sigma Aldrich) |
| 분리막 · 전해질 | Freudenberg FS2019 · 1 M LiPF₆ EC:EMC 1:1 (ref 17 은 LiClO₄) |
| 구성 | LFP\|Li 반쪽전지 · LFP\|LFP · Li\|Li 대칭셀, 활성 면적 **2.54 cm²** |
| 전처리 | 조립 뒤 충방전 10 사이클 |
| EIS | Solartron 1400E + Scribner Multistat, **10 mV** 개방회로, **1 MHz – 10 mHz**; Kramers–Kronig 잔차 < 1 % 인 **10 mHz – 100 kHz** 만 평가 |
| 온도 | 0 · 10 · 20 · 23 · 30 °C (Weiss WK1 180) |
| SOC | 100 → 10 % 단계 감소(방전 전류 적분) |
| 적합 | CNLS(Matlab), 시작값은 DRT; 파라미터 의존 평가에서는 **전체 주파수 범위**에 완전 모형 적합 |

---

# 3. 절별 해체

## 3.1 서론 (p. A952)

LFP 의 약점은 이온 · 전자 전도도. `[인쇄]` 성능 제한 과정의 해석이 문헌에서 "not consistent, varying from charge transfer resistance at cathode/electrolyte to contact resistance at cathode/current collector" (refs 3 · 11 · 12) — **이 편의 물음 자체가 "그 큰 호가 전하이동이냐 집전체 접촉이냐" 다.** 방법 논지: ECM 을 과정의 수 · 정체를 모른 채 정하지 말고 DRT 로 먼저 식별(SOFC 에서 온 방법, refs 13–16).

## 3.2 DRT · 전처리 (p. A953–A954, Fig. 1–3)

- 식 (3) `Z = R0 + R_pol ∫ g(τ)/(1+jωτ) dτ` · 식 (4) 유한 RC 합 — 역문제는 "ill-posed" (refs 14 · 21 · 22).
- 리튬 셀은 저주파에서 순수 용량성이라 실축으로 안 닫힌다 → DRT 경계조건 위반. 처리: **(1) < 0.1 Hz 에 확산 모형 적합 (2) 빼기 (3) 나머지를 DRT.**
- 확산 모형: Levi & Aurbach(ref 23)의 **GFLW + 직렬 C₀**(식 5). GFSW 가 "more appropriate" 이지만 "best fit results were obtained" 로 GFLW 선택. `[인쇄]` 지수 `P_GFLW` 0.35–0.5 — "indicating a limited representation of the occurring diffusion process" · "an **empiric homogenized description**".
- 파라미터 의존 평가에서는 완전 모형을 **전체 주파수에** 적합("to exclude an influence of the previous frequency selection").

## 3.3 반쪽전지 · 온도 (p. A954–A955, Fig. 4–9a)

- 온도 ↓ ⇒ 총 분극 · 옴 저항 ↑(Fig. 4). K–K 잔차 < 1 %(Fig. 5).
- 전처리 없이 DRT 는 "not meaningful"(Fig. 6).
- 20 °C · SOC 100: 봉우리 **P1 3 Hz(작음) · P2 250 Hz · P3 1000 Hz(비슷한 크기)**(Fig. 7).
- 온도 지도(Fig. 9a): P1 · P2 는 강하게 온도 의존(저온 → 저주파 · 큰 R), **P3 는 "no distinctive temperature dependency, but a rather large resistance"**. 0 °C 에서 P2 · P3 사이에 **넷째 과정** — "neglected in this study because it is not separable from P3 and plays a minor role".
- `[도표]` Fig. 9a: 0 °C 에서 P1A 봉우리 ≈25 Hz · 높이 ≈370, P2C ≈1–1.5 kHz · ≈85; 30 °C 에서 P1A 는 ≈300–500 Hz 로 이동해 P2C 와 이웃.

## 3.4 대칭셀로 전극 배정 (p. A956, Fig. 8–9b · c)

- LFP\|LFP: 두 과정 — 옛 P1(0.8–10 Hz, 온도 의존) · 옛 P3(**"remains at 2 kHz"**, 거의 온도 무관). 저온에서 P1 이 쌍봉으로 갈라짐 — "Possibly … a small electrical asymmetry of both electrodes".
- Li\|Li: P2 가 주 과정(강한 온도 의존) + "significantly less pronounced low frequency peaks" — 반쪽전지에서 양극 확산과 겹쳐 "a separation impossible" → 확산 또는 P3 에 흡수.
- ⇒ `[인쇄]` "enable to assign … P1 and P3 **unambiguously** to the cathode and P2 to the anode" → 이름 **P1C(옛 P1) · P2C(옛 P3) · P1A(옛 P2)**.
- `[인쇄]` 단서: 구성마다 특성 주파수 · 온도 의존이 조금씩 다름 — "a clear indication that the **reproducibility of our experimental cell setups is limited**"; Li 금속이 전해질을 소모해 양극 쪽 손실에 영향 가능.
- `[도표]` Fig. 9b 대칭셀 P3=P2C ≈3 kHz(본문 "2 kHz") · 반쪽전지 Fig. 9a P2C ≈1–1.5 kHz.
- `[해석]` 대칭셀은 같은 전극 둘의 직렬이라 한 전극 과정이면 `R` ×2 · `C` ×½ · **τ 불변**이어야 한다. P2C τ 가 반쪽 ↔ 대칭에서 ×≈2–3 다른 것은 "재현성" 이 **이 호의 주파수 자체를 셀마다 움직인다**는 뜻 — 대역을 정체로 쓰는 이식(11호)에 직접 걸린다.

## 3.5 등가회로 (p. A956, Fig. 10–11)

`L0 – R0 – RQ2C – RQ1A – RQ1C – (Z_GFLW – C0)` **전부 직렬**. P1A = "a combination of SEI-diffusion and charge transfer at the surface"(ref 25). `R0` = "ohmic contribution of electronic and ionic charge transport phenomena in all cell components".
`[도표]` Fig. 10(0 °C, SOC 100): 꼭짓점 표지 **P2C 1 kHz · P1A 30 Hz · P1C 0.9 Hz** · 10 mHz 끝 · 모의 양극 호 P2C ≈0 → ≈190 Ω cm²(R0 포함), P1C ≈680 → ≈740.
잔차(Fig. 11): < 100 Hz 에서 매우 작고 그 위에서 계통 편차 — Li 과정의 불완전 모형 탓; `[인쇄]` "The CNLS fit becomes unstable when including this additional loss processes into the model and is therefore neglected. Furthermore, this process overlaps with P2C … and cannot be separated for high temperatures. **Without modeling that process the residuals remain below 1 %**".

## 3.6 온도 · 활성화 에너지 (p. A957, Fig. 12, Table I)

| 과정 | 요소 | `F_R` [Hz] (표 머리 "T = 30 … 0 °C") | ASR [Ω cm²] (30 … 0 °C) | `E_act` [eV] |
|---|---|---|---|---|
| R0 | R | – | 7 … 12 | 0.14 |
| P1A | RQ | **30 … 500** (D1) | 25 … 486 | 0.72 |
| Pdiff,C | Z_FLW + C0 | 2·10⁻³ … 4.4·10⁻⁴ | 219 … 1089 | (빈 칸, D2) |
| P1C | RQ | **0.8 … 8** (D1) | 7 … 57 | 0.45 |
| P2C | RQ | 1000 | 131 … 178 | 0.06 |

- ASR 는 전극 면적 2.54 cm² 기준.
- R0 0.14 eV ↔ 문헌 LiPF₆ EC/DEC 0.11 · EC/DMC 0.155 eV(ref 26) → 전해질 이온 전도.
- P1A 0.72 eV ↔ Zaban 의 SEI 확산 0.3–0.83 eV(ref 25) → "cumulated temperature dependency of a composite SEI layer".
- ★ **배정 논증 전문**: "According to literature, charge transfer resistance is **assumed** as dominant loss process in LiFePO4 cathodes. Hence, either P1C or P2C is attributed to the charge transfer … However, as a transfer process is **always temperature activated**, this clearly points at P1C, whereas the dominant P2C originates from another cathodic process. It is not possible to address this question to literature as, to our knowledge, the impedance response of the LiFePO4-cathode was never separated before into several losses."
- `[도표]` Fig. 12: 다섯 계열 모두 5 점 · 직선 적합. P1C 점들이 선 주위로 흩어짐(20 °C 점 ≈20 이 선 ≈15 위 · 10 °C 점 ≈24 가 선 ≈28 아래). P2C ≈135 → ≈175 거의 평탄. 10 °C 에서 P2C ≈150 · P1C ≈24 · P1A ≈200.

## 3.7 SOC (p. A957, Fig. 13)

- P1C 는 SOC ↓ 에 커짐 — "charge transfer is facilitated when few lithium-ions are present in the host lattice – hence, for high SOC" → 전하이동 배정의 "supplementary indication". 저 SOC 에서 P1C 와 확산이 함께 저주파로 밀려 **측정 범위를 벗어난다** — 10 % 에서 스펙트럼이 실축으로 안 닫혀 전처리 · DRT 가 "less adequate".
- P1A 도 SOC 의존 — 덴드라이트 위 증착 가설("Probably") + Li 전극 무순환 노화.
- P2C: "generally not SOC dependant" — 70 % 아래에서 Li 쪽 작은 인공물과 합쳐 봉우리 모양이 변함.
- `[도표]` Fig. 13b(0 °C): P2C 봉우리 높이 ≈80(100 %) → ≈130(10 %) — Table II 로는 0 °C SOC 100 → 10 에서 178 → 225(`[재현]` ×1.26).
- ⚠ Fig. 13b 축 이름 "g(f) /Ωcm²" — 다른 DRT 그림은 "Ωcm²s"(D9).

## 3.8 T × SOC 지도 (p. A958, Fig. 14, Table II)

| 과정 | 30 °C · SOC 100 | 20 °C · SOC 50 | 0 °C · SOC 10 | 이름 |
|---|---:|---:|---:|---|
| Pdiff,C | 219 | 781 | 1308 | Solid state diffusion |
| P1C | 7 | 196 | 1900 | Charge transfer cathode/electrolyte |
| P2C | 131 | 180 | 225 | Contact resistance cathode/current collector |

- `[인쇄]` P2C "almost independent of temperature and SOC. The rather constant value of **ASR = 178 Ωcm² ± 50 Ωcm²** strongly supports this polarization mechanism as being caused by the contact resistance between cathode and current collector (Fig. 15) as Gaberscek et al. proposed in Ref. 11."
- P1C 7 → 1900 "more than two orders of magnitude" → "further piece of evidence" 로 전하이동.
- Pdiff,C: 온도에 민감(SOC 50: 287–1287), SOC 에 덜 민감(20 °C: 393–909).
- `[인쇄]` 서열: 확산이 "major loss process in almost any case", 고 SOC 에서 다음이 **접촉 저항**, 저 T · 저 SOC 에서 전하이동이 양극 임피던스의 주 몫.

## 3.9 캘린더링 (p. A958–A959, Fig. 15–16)

- 설계 문장: 압연은 (i) "decreased in thickness, open porosity and electrolyte accessible surface area, which **should** change the charge transfer resistance, P1C" (ii) "increased in contact area cathode/current collector, which **should** influence the contact resistance, P2C".
- 측정: FIB/SEM 공극률 64.7 → 41.5 % · 두께 20 → 10 µm. **면적 두 개는 도식(Fig. 15)뿐.**
- 결과(Fig. 16, 0 °C · SOC 100): "P2C decreases, whereas the process shifts toward a higher relaxation frequency. By contrast, P1C increases … and it decreases in relaxation frequency. The shift in frequency for each process PnC follows equation (9): `τ_nC = R_nC·C_nC`" → "thus **proving** the suitability of our novel approach as well as the applicability of our proposed equivalent circuit model".
- `[인쇄]` 단서: Li 전극 임피던스도 두 셀 사이에 다름 — "the reproducibility of our lithium-metal electrode is always limited and influences the LiFePO4 evaluation".
- `[도표]` Fig. 16a: 첫 호 끝 최소점 Z′ ≈780(미압연) → ≈560 Ω cm²(압연) — R0 + P2C + P1A 합(음극 포함). Fig. 16b 봉우리 위치: **P1C ≈1 → ≈0.28 Hz · P2C ≈1.3 kHz → ≈8 kHz · P1A ≈40 → ≈100 Hz**; 채운 봉우리(압연) P1C 높이 ≈160 ↔ 빗금(미압연) ≈50, P2C 빗금 ≈90 ↔ 채움 ≈12.

## 3.10 결론 (p. A959)

"cathode and anode polarization processes with close time constants are separated individually and a physically motivated ECM is established **without any a priori settings** for the electrochemical system" · 세 양극 손실(확산 · 전하이동 · 집전체 접촉) · 캘린더링에 두 저항이 "respond readily in size and relaxation frequency, thus proving the applicability".

---

# 4. ★ 무엇으로 갈랐나 — 판정 표 (카드 처방의 언어로)

| 처방 채널 | 이 편 | 가른 것 | 판정 |
|---|---|---|---|
| 대역(DRT) | ✅ 봉우리 분리 | **직렬 호 둘**(1 kHz ↔ 1–8 Hz) | 측정 · λ 미인쇄 · 넷째 과정 제거 |
| 대칭셀 | ✅ | 전극 배정 | 측정 · 셀 간 τ 차 ×2–3 |
| 3-a `Ea` | ✅ **핵심 채널** | 열활성(0.45) ↔ 비활성(0.06) | 측정(한 셀, ± 0) — 이름은 "always temperature activated" 가정 |
| SOC | ✅ | Li 함량 의존 ↔ 무관 | 측정 |
| 2단계 조작 | ⚠ 캘린더링 한 쌍 | 방향만 | 네 원인 동시 · 크기 0 · 음극도 변함 |
| 1단계 R·C | ❌ 지면 0 (식 9 한 줄) | — | `[재현]` Table I 로 `C` 3 자릿수 분리 · 캘린더링 τ 이동(§5) |
| 3-b C 상한 | ❌ 지면 0 | — | `[재현]` P2C ≈1 µF cm⁻² · P1C ≈3 mF cm⁻²(§5.2) |
| 4단계 시간 영역 | ❌ | — | — |
| **곱 `A·j₀`(한 호 안)** | **❌ 대상 아님** | — | P1C 의 면적 ↔ `j₀` 는 캘린더링 설명(면적)과 SOC 설명(`j₀`)이 **서로 다른 인자에 배정**됐을 뿐 갈리지 않음 |

---

# 5. `[재현]` 검산

## 5.1 `Ea` 양끝 두 점 (Table I)

`Δ(1/T) = 1/273.15 − 1/303.15 = 3.630 × 10⁻⁴ K⁻¹`, `Ea = k_B·ln(R₀°C/R₃₀°C)/Δ(1/T)`:
P2C ln(178/131) → **0.073 eV** (인쇄 0.06) · P1C ln(57/7) → **0.50** (0.45) · P1A ln(486/25) → **0.70** (0.72) · R0 ln(12/7) → **0.13** (0.14) · **Pdiff,C ln(1089/219) → 0.38 eV (인쇄 없음, D2)**.
인쇄값과 ≤0.05 eV — 5 점 적합과 두 점의 차. kJ mol⁻¹ 환산: 0.06 eV = **5.8** · 0.45 = **43.4** · 0.72 = **69.5**.

## 5.2 ★ Table I 에서 `C` (이상 RC, `C = 1/(2π F_R R)`)

| 과정 | 30 °C | 0 °C | 비(0/30) |
|---|---:|---:|---:|
| P2C (F 1000 Hz) | R 131 → **1.2 µF cm⁻²** | R 178 → **0.89 µF cm⁻²** | ×0.74 |
| P1C (F 8 · 0.8 Hz, D1 뒤집음) | R 7, 8 Hz → **2.8 mF cm⁻²** | R 57, 0.8 Hz → **3.5 mF cm⁻²** | ×1.23 |
| P1C (인쇄 순서 그대로) | R 7, 0.8 Hz → 28 mF cm⁻² | R 57, 8 Hz → 0.35 mF cm⁻² | ×0.012 |

- 뒤집은 판이 Fig. 9 · 본문("shift to lower frequencies … for decreasing temperatures")과 맞고, **`C` 가 온도에 거의 불변**이라는 RC 물리와도 맞는다 ⇒ D1 은 인쇄 순서 오류로 판정.
- **두 호의 `C` 비 ≈2,300–3,900.** `[해석]` 3-b: P1C ≈3 mF cm⁻²(기하 면적당)는 탄소 24 wt% 다공 전극의 이중층(거칠기 수백)과 양립 — 단 **그 `C` 의 대부분은 카본블랙 표면일 수 있어** `C ∝ LFP|전해질 면적` 전제가 이 전극에서 약하다(BET · 로딩 미인쇄, G5). P2C ≈1 µF cm⁻² 는 평판 이중층(≈10–50 µF cm⁻²)보다 작다 — 비접촉 집전체 면의 일부 또는 직렬 결합과 양립, 상한 위반 없음.
- ⚠ RQ 의 `n` 미인쇄 — 위 `C` 는 꼭짓점 주파수에서의 유효값.

## 5.3 "178 ± 50"

Table II 의 P2C 131 · 180 · 225 ⇒ 중간값 (131+225)/2 = **178** · 반폭 **47**. `[재현]` **± 50 은 표 범위의 반폭이지 통계가 아니다.** 178 은 동시에 Table I 의 0 °C · SOC 100 값.

## 5.4 공극률 · 두께 질량수지

고체 부피 / 면적: (1 − 0.647) × 20 µm = **7.06 µm** ↔ (1 − 0.415) × 10 µm = **5.85 µm** ⇒ **×0.83**. 같은 시트의 압연이면 1.00 이어야 한다 — 두께가 둥근 값이거나(인쇄 "from 20 μm to 10 μm") 다른 조각 · 다른 로딩. ASR 은 기하 면적 기준이라 로딩 차 17 % 가 두 셀 비교에 그대로 들어간다.

## 5.5 캘린더링 τ (`[도표]` 봉우리 위치)

P1C τ ×≈3.5(1 → 0.28 Hz) · P2C τ ×≈0.16(1.3 → 8 kHz) · P1A τ ×≈0.4(40 → 100 Hz). 판독 오차 ≈±0.1 decade.
- **같은 계면 `C` 전제**(C ∝ 그 계면 면적)에서 면적 서명 = τ 보존 → **두 양극 호 모두 면적 서명 아님.**
- **여집합 `C` 전제**(P2C: 저항은 접촉 면적 `A_c`, `C` 는 비접촉 면적 `A_g − A_c`) — `R ∝ 1/A_c`, `C ∝ (A_g − A_c)` ⇒ 접촉 증가가 τ 를 **두 인자로** 줄인다 — 관측(×0.16)과 방향 일치. Fig. 15 도식이 이 배치다(CPE → 녹색 집전체 면).
- `R` 비는 읽지 않는다 — §5.6.

## 5.6 DRT 높이 ↔ Table I (정규화 검사)

0 °C · SOC 100 에서 Fig. 9a 높이 P1A ≈370 · P2C ≈85(비 4.4) ↔ Table I 486 · 178(비 2.7). 로그 축 밀도로 읽으면(높이 ∝ R/폭) 폭 차가 ×1.6 를 설명해야 하고, 선형 Hz 밀도로 읽으면(R ∝ 높이 × f) P2C/P1A ≈14 로 **Table 과 반대 서열**. 20 °C Fig. 7b P2 ≈75 · P3 ≈80 ↔ 52 · 155(비 3.0). ⇒ **축 "g(f) / Ωcm²s" 의 정규화를 지면으로 복원할 수 없다** — DRT 높이에서 `R` 비를 읽지 않았다.

---

# 6. ★★★ 전자 접촉 vs 이온 접촉 — ASSB 로 무엇이 옮겨지나

| | 이 편 P2C | 카드의 접촉 손실(`θ`) | 18호 R2 (ASSB) |
|---|---|---|---|
| 계면 | 양극층 \| Al 집전체 | CAM \| SE | Al \| 복합체 |
| 전하 운반자 | 전자 | Li⁺ | 전자 |
| `Ea` | **0.06 eV (5.8 kJ mol⁻¹)** | `[해석]` SE 제약 전도 → SE 이온 전도의 `Ea` 를 짐 | **41–70 kJ mol⁻¹** (18호 digest Table 1, LiNbO₃ 추정 · 같은 셀 R3 49–63 과 겹침) |
| `C` 의 자리 | `[도표]` 도식상 **여집합**(비접촉 집전체 면) | 같은 계면(접촉 면의 이중층) — 처방 1단계 전제 | 미상 |
| 처방 1단계 서명 | 접촉 ↑ ⇒ τ ↓(두 인자) | 접촉 ↓ ⇒ τ 보존(`R`↑ · `C`↓) | — |

`[해석]` 세 결론:
1. **이 편은 곱 `θ·j₀` 를 가르는 방법의 원형이 아니다** — 원장 행 문구("곱 축퇴(`θ`↔`j₀`)를 가르는 방법의 액체셀 원형")는 제목에서 온 기대이고, 지면이 가른 것은 **직렬 두 호의 이름**(분배)이다. 곱 앞 단계(45 · 48호 줄)의 표본이다.
2. **옮겨지는 것은 채널의 조합**(대역 + 대칭셀 + `Ea` + SOC + 조작)이고, **옮겨지지 않는 것은 판별값**(`Ea` ≈ 0 = 접촉). ASSB 에서 전자 접촉 호는 열활성일 수 있고(18호), 이온 접촉은 원리적으로 열활성이다.
3. **처방 1단계의 전제는 계면 종류에 따라 부호가 바뀐다** — 전자 접촉 호의 `C` 는 여집합을 보므로 "τ 보존 = 면적" 규칙을 그대로 쓰면 면적 변화를 면적이 아니라고 판정한다. ASSB 에서 한 호에 1단계를 걸기 전에 **그 호의 `C` 가 저항과 같은 계면에 있는지**를 먼저 적는다.

---

# 7. 11 · 18 · 47호가 가져간 것 — 원전 조건 대조

| 편 | 가져간 것 | 원전 조건 | 판정 |
|---|---|---|---|
| **18호** Fukunishi 2023 (ref [29], "Chroal" 오기) | DRT 방법 참고문헌([28] Schichlein 과 함께) | — | 이 편의 **판별 채널 `Ea`** 는 18호가 자기 셀에서 이미 쟀다: R2(Al\|복합체, Al 대칭셀로 검증) 41–70 kJ mol⁻¹(R3 전하이동 49–63 과 겹침) ↔ 액체 문헌 "ca. 4" [37,38] — 18호가 비교한 액체 값은 이 편 5.8 과 같은 자릿수(그 [37,38] 이 어느 편인지는 18호 digest 에 없음). **원전의 "접촉 = 온도 무관" 은 18호 ASSB 에서 서지 않는다** — 18호는 LiNbO₃ 로 설명 |
| **11호** Yu 2024 (목록 [9]; 대역 문장은 [19,20]) | "slightly above 10³ Hz … solid-solid contact impedance of LiFePO₄/Al and nano-Si/Cu current-collectors" → ASSB P3 = CAM–SE 기계 접촉 | 이 편 P2C: 반쪽 1 kHz · 대칭 2 kHz(`[도표]` ≈3) · 압연 ≈8 kHz; 정체 근거 = `Ea` · SOC 무관 | ⚠ **대역만 옮겼고 정체의 근거(온도)는 두고 왔다** — 11호는 RT 고정(11호 digest). 원전 안에서 대역이 셀 · 조작마다 ×2–6 움직인다. 그리고 원전의 접촉은 **집전체 전자 접촉**이지 CAM\|SE 가 아니다. [19] = Schmidt 2011 *JPS* 196, 5342(이 편 ref 19, 같은 IWE — 이 편은 연도를 "(2010)" 으로 인쇄) |
| **47호** Solchenbach 2016 (ref [35]) | LFP 등가회로 R–(R‖CPE)–W("단순화") · Li 금속 호 배정 | 이 편 LFP: 양극 RQ **둘**(P1C · P2C) + 확산; Li: RQ **하나**(P1A = "SEI-diffusion **and** charge transfer" 합, 30–500 Hz, 0.72 eV) + 분리 불가한 저주파 작은 봉우리 | `[해석]` 단순화가 **이 편이 가른 두 호를 다시 합쳤다**. 10 °C 에서 이 편 LFP 는 P2C ≈150 > P1C ≈25(Fig. 12) — 47호 "LFP `R_CT` 불변" 은 원전 지도에서 접촉 지배 합과 양립(다른 전극이라 판정 아님). Li 는 47호가 두 호(1.3 kHz "SEI" · 1 Hz "charge transfer", ref 36 Mogi)로 나눔 — 원전은 한 호에 둘을 합쳤고 저주파 봉우리는 이름을 안 붙임 |

---

# 8. 곱 축퇴 처방 — 서른네 번째 적용 (⚠ 액체셀, 도구 칸)

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 지면 `C` 0 · 식 (9) 한 줄 · `[재현]` Table I → P2C ≈1 µF · P1C ≈3 mF cm⁻² · 캘린더링 τ `[도표]` | ⚠ **부분** — 두 호 분리는 `C` 3 자릿수로 강하게 선다. 캘린더링 쌍은 두 호 모두 τ 이동 → 같은 계면 전제로 면적 서명 아님, **여집합 전제(P2C 도식)로는 접촉 증가와 양립** |
| **2단계** 면적 대조군 | 캘린더링 한 쌍 — 두께 · 공극률 · 두 면적 동시, 음극도 변함, 고체량 ×0.83 | ⚠ 단일 원인 조작 아님 |
| **3단계-a** `Ea` | ✅ 다섯 과정 모두(5 점) | ✅ **이 편의 주 판별자** — 단 판별값(≈0 = 접촉)이 ASSB 로 안 옮겨진다(18호 R2) |
| **3단계-b** `C` 상한 | `[재현]` 위 값 | ✅ 둘 다 통과(P1C 는 탄소 면적 몫이 큼 — 전제 약함) |
| **4단계** 시간 영역 | 없음 | ❌ |

**새 줄 후보**: "**`C` 의 자리 — 저항과 같은 계면인가, 여집합인가(전자 접촉 호) · 그리고 `Ea` 판별값은 계 고유**". 1단계 전 그 호의 `C` 가 어디 있는지(같은 계면 이중층 ↔ 비접촉 면)를 적고, 3-a 로 정체를 붙일 때는 판별 문턱을 **같은 계의 대조**(18호식 Al 대칭셀)로 잰다.

⚠ **이것이 곱을 푼 것은 아니다**: 액체 · 전자 접촉 · 셀 1 · `C` 는 이상 RC 재현 · 캘린더링 τ 는 도표 판독. 기여는 **분배(직렬 호 이름) 단계의 채널 목록**과 **1단계 전제의 부호가 계면 종류에 달렸다**는 것.

---

# 9. Q2 · Q4 · Q5

- **Q2** — **해당 없음(액체) · 도구 칸.** 신품 · 열화 0 · `LAM_PE` ↔ 접촉 대상 아님. 방법(대역 · 대칭셀 · `Ea` · SOC · 조작)은 이식 가능한 형태.
- **Q4** — **0/51, 마흔세 번째 성질** "불안정한 적합을 요소 제거로 안정시키고, 제거된 몫이 흘러갈 곳(주인공 호 P2C)을 스스로 인쇄한 뒤 '선험 설정 없음' 으로 닫았다". 식별성 낱말 전수 0. "unambiguously" 2 회 중 1 회는 일반론("not always identified unambiguously"), 1 회는 대칭셀 배정.
- **Q5** — 해당 없음: 기준극 0, 대칭셀은 **AC 전극 배정**에만(50호 "대칭셀 반 빼기" 와 달리 빼지 않는다) — DC 영점이 결과에 들어가지 않는다.

---

# 10. 채움표 행 (Q1–Q8)

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **없다 — `θ(N)` 0/51.** 액체 · 접촉 = 양극층 \| 집전체(전자) | **해당 없음(액체) — 도구 칸.** 직렬 두 호의 이름을 대역 + 대칭셀 + `Ea`(0.45 ↔ 0.06 eV) + SOC 로 가르고 캘린더링 한 쌍으로 방향 확인 | **DRT-seeded CNLS ECM, 물리 이름은 소거 + 가정("always temperature activated") + 문헌** · ± 0 · 셀 1 · "± 50" 은 범위 | **0/51 — 마흔세 번째 성질** | 해당 없음 — 기준극 0, 대칭셀 AC 배정 | 없다 — `pressure` · `MPa` 0(압연 압력 미인쇄) | 해당 없음(Li 금속 덴드라이트 가설 "Probably") | 해당 없음(액체 LFP) — OCP 0 |

---

# 11. 어긋남 (실제로 어긋난 것만)

| # | 지면 A | 지면 B | 종류 |
|---|---|---|---|
| **D1** | Table I `F_R` "T = 30 … 0 °C": P1A 30 … 500 · P1C 0.8 … 8 | Fig. 9 · 본문: 저온 → 저주파 | **표 열 순서 오류** — `[재현]` 인쇄 순서면 P1C `C` 가 ×80 움직임(§5.2) |
| **D2** | "The activation energy of the solid state diffusion … is calculated" · Fig. 12 "all showing Arrhenius behavior" | Table I `E_act` 빈 칸 | 값 미인쇄 — `[재현]` ≈0.38 eV |
| D3 | P2C "178 Ωcm² ± 50" | Table II 131–225 | ± = 범위 반폭(§5.3) |
| **D4** | 공극률 64.7 → 41.5 % · 두께 20 → 10 µm | 고체 부피 7.06 → 5.85 µm | `[재현]` ×0.83 — 같은 시트면 1 |
| D5 | 대칭셀 P3 "remains at 2 kHz" | 반쪽전지 1000 Hz · `[도표]` 대칭 ≈3 kHz | 같은 전극 과정이면 τ 동일해야 — 저자 "reproducibility" |
| **D6** | 초록 · 결론 "modified in porosity, thickness and **contact area** between cathode/electrolyte and cathode/current collector" | 측정은 공극률 · 두께뿐 | 면적은 도식 |
| **D7** | 결론 "without any a priori settings" | GFLW 선택("best fit") · 넷째 과정 제거 · λ 미인쇄 | 방법 서술 과장 |
| D8 | Fig. 3 캡션 "an appropriate diffusion model22" | 본문 Levi et al. = ref 23; ref 22 = Weese(DRT) | 인용 번호 |
| **D9** | DRT 축 "g(f) / Ωcm²s"(Fig. 7 · 9 · 16) · "g(f) /Ωcm²"(Fig. 13) | Table I ASR 비와 높이 비 불일치(§5.6) | 정규화 복원 불가 |
| D10 | 캘린더링 "P1C increases" · "P2C decreases" = 양극 변화 | P1A(음극)도 ≈40 → ≈100 Hz · 높이 변화 | 대조 쌍이 양극만 바뀐 쌍이 아님(저자 인정) |
| D11 | ref 19 Schmidt … *J. Power Sources* 196(12), 5342 "(2010)" | 11호 digest 같은 편 "(2011)" | 연도 한쪽 오기(판정 안 함) |

---

# 12. 그림 — 무엇을 봤나

크로퍼가 9 장(Fig. 1–5 · 8–10 · 15)을 자동으로 잡고 **7 장을 "영역 없음" 으로 놓쳤다**(Fig. 6 · 7 · 11 · 12 · 13 · 14 · 16 — 전부 벡터). 400 dpi 로 수동 크롭 + Table I · II 도 크롭(`*_manual_p*.png`). ⚠ 자동 `fig_10.png` 는 **아래쪽 절반만** 잘렸다 — 전체는 `fig_10_manual_p6.png`.

**본 것 (크롭 Read, 8 장)**: Fig. 16(캘린더링 — 봉우리 위치 판독) · Fig. 12(Arrhenius — 10 °C 값 판독) · Fig. 9(대칭셀 배정 — 주파수 판독) · Fig. 14(T×SOC 지도) · Fig. 13(SOC) · Fig. 10(ECM, 수동 크롭 전체) · Fig. 15(도식 — 700 dpi 확대로 P2C CPE 위치 확인) · Table I(Ω · 순서 확인).
**쪽 미리보기(70 dpi)로만 본 것**: p5 의 Fig. 5 · 6 · 7 · 8 · p9 의 Table II(값은 추출 텍스트와 대조).
**안 본 것**: Fig. 1 · 2 · 3 · 4 · 11(크롭은 있음).
본문과 어긋난 그림: **Table I 주파수 열 ↔ Fig. 9**(D1) · Fig. 9b 대칭 P2C ≈3 kHz ↔ 본문 2 kHz(D5, 근사 범위) · Fig. 13 축 단위(D9).

---

# 13. 참고문헌 중 후속 후보 (29 편, 서지 기준 — 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Gaberscek, Moskon, Erjavec, Dominko, Jamnik 2008 *Electrochem. Solid-State Lett.* 11, A170** | 11 | ★★★ **"집전체 접촉 저항" 배정의 원전** — P2C 이름이 이 편에서는 문헌 사슬이다. `C` 의 자리(여집합)를 모형으로 적었는지 | Q2 · 곱 축퇴(1단계 전제) |
| Schmidt, Chrobak, Ender, Illig, Klotz, Ivers-Tiffée *J. Power Sources* 196(12), 5342 | 19 | 11호 [19] — 대역 문장의 직접 출처 | Q2 |
| Illig, Chrobak, Ender, Schmidt, Klotz, Ivers-Tiffée 2010 *ECS Trans.* 28(30), 3 | 17 | 같은 방법의 선행(LiClO₄) — 셀 간 재현성 비교 | Q4 |
| Levi & Aurbach 1997 *J. Phys. Chem. B* 101, 4630 | 23 | 전처리 확산 모형(GFLW + C) — 빼기가 P1C 에 새는 경로 | Q4 |
| Schichlein … Ivers-Tiffée 2002 *J. Appl. Electrochem.* 32, 875 | 14 | DRT 계산법(18호 [28] 과 같은 편) | Q4 |
| Zaban, Zinigrad, Aurbach 1996 *J. Phys. Chem.* 100, 3089 | 25 | Li SEI 다층 `Ea` 0.3–0.83 eV — 47호 Li 호 배정과 대조 | Q7 인접 |

큐 53–59 인용: **0**(전부 2012 이후 — 시간상 불가).

---

# 14. 이 digest 가 주장하지 않는 것

- **P2C 가 집전체 접촉이 아니라고 하지 않는다** — 온도 · SOC 무관 · 캘린더링 방향 · 도식의 여집합 `C` 와 모두 양립한다. 주장은 이름이 **측정이 아니라 소거 + 가정 + 문헌**으로 붙었다는 것까지다.
- **§5.2 의 `C` 를 인용값으로 쓰지 않는다** — 이상 RC · `n` 미인쇄 · 표 순서 뒤집음(D1) 위의 재현이다.
- **캘린더링 τ 판정은 봉우리 위치 판독(±0.1 decade)과 셀 1 쌍 위다.** `R` 비는 읽지 않았다.
- **18호 R2 와의 대조는 18호 digest 의 값**이다 — 18호 원문은 이 세션에서 다시 열지 않았다.
- 47호의 "LFP 불변" 이 접촉 지배라고 **판정하지 않는다** — 전극 · 셀이 다르다.
- 연구 수치의 정본은 `degradation-degeneracy/` artifact + `docs/RESULTS*.md` 이고, 이 digest 는 그것을 복사하지 않는다.

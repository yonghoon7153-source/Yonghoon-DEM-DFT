---
title: "Barai, Uddin, Widanage, McGordon, Jennings 2018 — A study of the influence of measurement timescale on internal resistance characterisation methodologies for lithium-ion cells (Sci. Rep. 8, 21)"
source_url: local-upload/11._A_study_of_the_influence_of_measurement_timescale_on_internal_resistance_characterisation_methodologies_for_lithium-ion_cells.pdf
source_url_note: "PDF 13 쪽(본문 약 11 쪽 + 참고문헌 37). SI 없음. 크로퍼 7 장(Fig. 1-7) 전부 봤다, 화소 판독 Fig. 5a · 5b · 6a · 7b(원본 래스터 추출), 300 dpi 렌더 확인 p. 7. Table 1 · 2 는 PDF 텍스트. 원자료 · PDF 는 커밋하지 않는다. ⚠ 액체셀(상용 20 Ah LFP/흑연 파우치) — 도구 칸. 20호(Chang 2020) ref [24] 가 R0/R_ct/R_p 3성분 분해의 근거로 지목."
source_doi: 10.1038/s41598-017-18424-5
source_license: "CC BY 4.0 (Scientific Reports, 오픈액세스) — (c) The Author(s) 2017"
pdf_sha256: fbe2c1bec8d2717a477bb7b1343066e7cb6995e110d255566e8dda2382269bf7
ingested: 2026-09-23
sha256: 561aebc6c5fa15afd3dab99d1875cb178685bec09d9c6a27888f9d5149227db1
---

# 수집 목적

`assb` 섹션 **49호**. 큐 **50번**(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g, 2차 묶음 열한째 편).
닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q2(저항 성분 분리) · Q4(유일성)**. 원장 행 메모:
"`R₀`/`R_ct`/`R_p` **작도법 원전**. 제목이 *measurement timescale* — 20호(Chang 2020)에서 '분해가 적합조차 아니다 — 작도다' 가 나온 자리".
지목 1 회: 20호 ref [24](Waag 2013 = ref [25] 와 함께, 3성분 분해의 근거).

> ⚠ **액체셀이다.** 상용 20 Ah LiFePO₄/흑연 파우치, 50 % SoC · 25 °C 한 상태, 열화 0 · 기준극 0 · 압력 0.
> 28 · 31 · 47호 선례대로 **도구 칸**이다 — ASSB 칸은 원칙적으로 움직이지 않는다.
> 이 편이 카드에 주는 것은 **"시간 창을 고르면 저항 값이 바뀐다" 는 명제의 원전 형태**, 그리고 그 명제가
> 저항 성분 **식별**에 대해 무엇을 말하고 무엇을 말하지 않는지다.

> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`, 원본 래스터 화소 판독) ·
> `[재현]` 우리가 지면의 숫자로 계산한 값 · `[해석]` 우리 해석.
> **`[해석]` 표시 없는 문장은 원문이 실제로 말한 것이다.** 원문 영어 인용의 오탈자는 그대로 옮기고 (sic) 로 표시한다.

---

# 원문에 없어서 확인이 필요한 것 (공백 먼저)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **셀 개수 미인쇄.** `[인쇄]` "20 Ah pouch cells" · "All the tests as outlined below were performed on each cell" — 몇 개인지 · 값이 셀 평균인지 한 셀인지 0 | 모든 "±" 의 뜻이 정해지지 않는다(G2) |
| **G2** | **"±" 의 출처 미인쇄.** Table 1 · 2 · Fig. 7a 의 ± 가 반복 산포인지 · 셀 간 산포인지 · 분해능인지 0. `[재현]` Table 2 의 ± 는 **열마다 상수**(1 C 0.05 · 2 C 0.03 · 5 C 0.02 · 15 C 0.01–0.02 mΩ)이고 1 C · 2 C 는 **≈1 mV ÷ 전류**(20 A → 0.05 · 40 A → 0.025)와 맞는다 | `[해석]` 전압 양자화에서 나온 분해능일 가능성 — 그러면 셀 간 산포는 **0 보고**다. 가설이고 확인 불가 |
| **G3** | **시간 ↔ 주파수 대응 규약의 유도 0.** 쓰인 규약은 `[인쇄]` "251 Hz (i.e., a timescale of 4ms)" · "a 2 sec square wave has highest harmonic contribution from 0.5 Hz" ⇒ **t = 1/f** 한 가지. 다른 규약(예: τ = 1/(2πf))과의 비교 0 | 논문의 핵심 주장("timescales match → align")의 분해능이 이 규약 선택에 걸린다(판정 (3) · R8) |
| **G4** | **EIS 에서 `Re Z` 와 `\|Z\|` 를 섞는 규칙 미인쇄.** `R₀` · `R₀+R_CT` 는 Nyquist(실수부)에서, 0.1 · 0.01 Hz 총저항 · 10 · 0.5 · 1 Hz 비교값은 Bode(크기)에서 읽는다 | 위상이 작은 0.1–100 Hz 에서는 차이가 ≤2 % 이나 **0.01 Hz 에서는 ≈11 %**(R6, D4) |
| **G5** | **다중사인 ECM 의 시상수 τ₁ · τ₂ 미인쇄**(`R` 셋과 ± 만). 설계 신호의 전류 진폭 · 주파수 격자 · 주기 길이 수치 0 | 처방 1단계(`R·C`)와 3-b(`C` 상한)가 막힌다. "RCT = 1.10" 이 어느 대역의 과정인지 확인 불가(판정 (3)) |
| **G6** | **전극 면적 · 활물질 질량 · BET 미인쇄**(상용 셀) | 면적당 저항 · `C` 가 없어 3-b 판정 불가 |
| **G7** | **펄스 사이 · 시험 사이 상태 복귀 확인 0.** 1 h 휴지(단일 펄스 방전 → 충전) · 30 min 휴지(다중 펄스) 뒤 OCV · SoC 기록 0 | Table 2 의 진폭 의존(최대 ×1.46)에서 **순서 효과 · 발열 누적**을 뗄 수 없다 |
| **G8** | **(iii) 구간의 시작 시점 기호가 인쇄에서 빠졌다** — "occurring at timescales 5 seconds34"(300 dpi 렌더로 확인, 관계 기호 없음) | `>` 인지 `≥` 인지 `~` 인지 모른다. 표 1 의 "5 s = RO + RCT + %RP" 와 합치면 `[해석]` "≥ 5 s" 쪽 |

---

# 판정 (먼저)

## (1) 창 의존성의 성격 — **총량은 "같은 양의 다른 창", 성분 이름은 "창 경계에 붙인 규약"**

**원문의 명제는 앞쪽이다.** `[인쇄]` 초록 "the computed resistance is strongly dependent on the timescales of the technique employed and that when timescales match, the resistances derived via different techniques align" ·
p. 2 "The value of resistance measured will thus depend on the remaining degree of freedom: the measurement duration (timescale) of the measurement" ·
결론 "it is not the non-linearity of the lithium-ion battery, as suggested in other studies, rather the timescale associated with the technique itself that influences measured internal resistance".
증거는 Fig. 7b 한 장이다 — 5 C 펄스 `ΔV/ΔI(t)` 여섯 점 · 1 kHz 측정기 한 점 · 다중사인 두 점을 **EIS 곡선 위(가로축 = t = 1/f)** 에 얹었다.
`[재현]` 5 C 펄스 ↔ 같은 "시간" 의 EIS: 0.1 s 1.33 ↔ 10 Hz 1.41(−6 %) · 1 s 1.61 ↔ 1 Hz 1.62(−1 %) · 2 s 1.71 ↔ 0.5 Hz 1.69(+1 %) · 10 s 2.12 / 2.00 ↔ 0.1 Hz 1.91(+11 / +5 %).
⇒ **총저항 `R(t)` 는 한 응답 함수를 다른 창에서 읽은 것**이라는 명제가 이 셀 · 이 진폭에서 ±11 % 안에서 선다.

**그러나 `R₀` · `R_CT` · `R_p` 는 그 함수의 "양" 이 아니라 창 경계의 차이다.** 원문 스스로 셋 모두를 규약으로 인쇄한다:

| 성분 | 원문이 붙인 경계 | 원문 자신의 판정 |
|---|---|---|
| `R₀` | DC: 0.1 s(장비 10 Hz 한계) · EIS: Im Z = 0 교차(251 Hz = 4 ms) · 다중사인: ECM 직렬 R | `[인쇄]` "physically more meaningful to use the voltage drop after 4ms" · 다중사인 값은 "cannot be labelled as a pure Ohmic resistance" |
| `R_CT` | DC: 0.1 → 2 s · EIS: 4 ms → −Im 극소(2 Hz = 0.5 s) · 다중사인: 첫 RC | `[인쇄]` "a comparison of RCT values measured from pulse power test and EIS test in not meaningful" (sic) |
| `R_p` | DC: 2 → 10 s(표 1 은 18 s 까지도 같은 이름) · EIS: 2 Hz → **0.1 Hz 또는 0.01 Hz** · 다중사인: 둘째 RC | `[인쇄]` "Estimating polarisation resistance using EIS results is not well-defined" · "Rp isn't identified from a Nyquist plot, instead it is pre-defined" |

`[재현]` 같은 이름이 방법마다 **×2.0(`R₀` 0.82–1.62) · ×2.9(`R_CT` 0.38–1.10) · ×13(`R_p` 0.11–1.39)** 흩어진다(Fig. 7a).
EIS `R_p` 는 경계를 0.1 → 0.01 Hz 로 옮기면 **0.36 → 1.39 mΩ(×3.9)** 가 된다 — 같은 셀 · 같은 스펙트럼.
⇒ **`[해석]` 판정: 총량은 같은 양의 다른 창이고, 성분은 다른 양이 아니라 "양이 아닌 것"(창 차분)이다.** 성분 값은 데이터가 아니라 **경계 선택**이 정하고, 원문은 그 경계를 `R₀` 에만 물리로 고정하려 했다(Im Z = 0) — `R_p` 는 "pre-defined" 로 남겼다.

## (2) 원문이 "어느 창이 옳다" 를 인쇄했나 — **`R₀` 에만, 그리고 그 기준도 설정 의존이다**

- `[인쇄]` 결론 "It is not possible to categorise a single best or correct technique; this will usually depend on the application and the availability of the test equipment" — **방법 선택은 용도 문제**로 둔다.
- `[인쇄]` **`R₀` 만은 옳은 창을 적었다**: "Since EIS results of this battery suggests that R0 corresponds to the 251 Hz (4mS) frequency response; it is therefore physically more meaningful to use the voltage drop after 4ms". 그리고 DC `R₀`(0.1 s) 과대를 "limitations of the battery test equipment" 로 돌린다 — `[재현]` 1.315 / 0.92 = **+43 %**, 그 값은 **EIS |Z|(10 Hz) 1.41** 과 −7 % 로 맞는다.
- ⚠ `[해석]` 그 "옳은 창" 의 기준(Im Z = 0 교차)은 **인덕턴스가 정하는 점**이다. 원문도 1 kHz 가 유도성 · 용량성 어느 쪽에 드는지가 "highly dependent on the battery sample" · "experimental setup (e.g. cable assembly)" 이라 적는다 — 교차점도 같은 이유로 이동한다. `R₀` 의 창은 **물리량이 아니라 셀 + 배선의 성질**로 고정됐다.
- **`R_CT` · `R_p` 의 옳은 창은 인쇄되지 않았다.** `R_CT` 의 EIS 끝점(−Im 극소)은 스펙트럼 모양의 점이고, `R_p` 는 "pre-defined".

## (3) 식별 관점 — **비식별을 두 곳에 인쇄하고, 결론에서 지웠다**

원문에는 비유일성 문장이 **두 종류** 있다.

1. **적합(ECM)의 비유일성** — `[인쇄]` "Although the ECM parameters are not uniquely identifiable, the series connected resistance and the resistance of the 1st and 2nd RC branches of the ECM are typically attributed to Ro, RCT and Rp" · "despite the good fit between model and experimental data, the parameters do not reflect the physical meanings attributed to them (due to unique identifiability)" (sic — 뜻은 비유일성) ·
   "An inherent problem with parameter identification is the uniqueness of the solution, which gives rise to ambiguities between identified model parameters (in the simplest case Ro and RCT) and their actual physical values. This ambiguity is further enhanced when higher order equivalent circuit models utilized … Given this ambiguity, the effectiveness of phenomenological models is judged solely on closeness of fit."
2. **작도(창 분할)의 비분리** — `[인쇄]` p. 3 "there in an inability to completely separate the different resistance components" (sic) · Fig. 3 캡션 "The overlap between (ii) and (iii) is indicative of the inability, within this technique, of precisely discerning each contribution" · p. 7 "Although Ro, RCT and Rp are not completely separated, at their respective timescales they are expected to be the dominant contribution" · p. 10 "Nevertheless, here, we follow the usual prescription of calculating Ro, RCT and Rp with DC methods8".

**그런데 결론은 둘 다 지운다**: `[인쇄]` "EIS can accurately provide separation and identification of all the individual resistance components, Ro, RCT and Rp." — 같은 지면의 "not well-defined" · "pre-defined" 와 정면으로 어긋난다(D5).
**그리고 창 의존성 자체를 식별 불가의 증거로 다루지 않았다** — "timescale matching" 이라는 **일관성**(총량이 한 곡선에 모인다)으로 풀었다. 일관성은 성분의 식별이 아니다(31호 "방법 간 일치 ≠ 인자 식별" 과 같은 범주).

`[해석]` **이 편이 식별 쪽으로 가장 멀리 간 자리는 다중사인 절이다.** 다중사인 ECM 의 직렬 R(`R₀`) 1.62 mΩ 은 **EIS |Z|(1 Hz) 1.62 와 같은 값**이고, 원문은 그 이유를 "employs a maximum frequency of 1 Hz" 로 적는다. 즉 **적합된 직렬 저항 = 여기 대역의 위쪽 끝에서의 임피던스** — 대역보다 빠른 과정은 전부 직렬 R 에 흡수된다. DC `R₀`(0.1 s) = |Z|(10 Hz) 도 같은 구조다(샘플링 10 Hz 가 대역 끝). ⇒ **파라미터 값을 정하는 것은 물리가 아니라 관측 대역의 끝**이다. 이것은 원문 명제를 한 걸음 넘는 우리 일반화다.
같은 구조로, 다중사인의 "RCT = 1.10 mΩ" 은 `[재현]` 1 Hz 에서 이미 |Z| ≈ `R₀` 이므로 **두 RC 가 모두 1 Hz 보다 느린 과정**이다 — EIS 의 `R_CT` 대역(2–251 Hz)과 **겹치지 않는 대역에 같은 이름**이 붙었다.

## (4) ★★★ 20호 대조 — **20호가 가져간 것은 "모양 규칙" 이고, 원전의 "시간 규약" 은 두고 왔다**

| 항목 | 원전(Barai 2018, 이 편) | 20호(Chang 2020, ref [24]) |
|---|---|---|
| 셀 | 상용 20 Ah LFP/흑연 파우치, **액체** | 벌크형 ASSB TiS₂ \| Li₂S–P₂S₅ \| Li₄.₄Si, ⌀14 mm 펠릿 |
| 전류 | **5 C(명목 100 A)**, 진폭 스윕 1 · 2 · 5 · 15 C | **200 µA ≈ C/72**(`[인쇄]` 고율 펄스는 "not adequate for ASSBs") |
| 상태 | **50 % SoC · 25 °C · 4 h 휴지 뒤** | 정전류 구간의 시작(직전 휴지 20 min — 20호 digest 프로토콜 표), `[해석]` 반대 방향 구간 끝의 상태 · 온도 0회 |
| `R₀` 창 | 0.1 s(장비 10 Hz) — 원문이 스스로 "4 ms 가 옳다" | "순간 강하"(샘플 간격 미인쇄) |
| `R_CT` 창 | **0.1 → 2 s**(고정 시점) | 이어지는 **비선형** 구간 — `[도표]`(20호) ≈0.8–1.2 h |
| `R_p` 창 | **2 → 10 s**(고정 시점) | 그 뒤 **~1 h 선형** 구간 |
| 경계 규칙 | `[인쇄]` "The RCT and Rp values are calculated using the 2 sec and 10 sec data points" = **시점 규약** · Fig. 1 모식도에만 선형 외삽 작도(점선, 본문 서술 0) | **선형 외삽 작도**(20호 Fig. 4 주황 직선) — 시작점 규칙 미인쇄(20호 G4) |
| 분리 가능성 서술 | "inability to completely separate" · Fig. 3 캡션 "overlap … inability" | 서술 0, 값은 5 Ω 단위로 Table 1 에 |
| 적합 여부 | **적합 아님**(DC 는 시점 읽기, EIS 는 Nyquist 판독) | 적합 아님 |

- `[해석]` **20호 판정 "분해가 적합조차 아니다 — 작도다" 는 원전에서도 선다.** 원전의 DC 분해도 적합이 아니고, 원전은 한 걸음 더 나가 **분리 불가를 인쇄**했다. 다른 점은 원전의 경계가 **시점**(0.1 · 2 · 10 s)이라 재현 가능한 규약이고, 20호의 경계는 **모양**(비선형 → 선형 전환)이라 규칙 없이는 재현이 안 된다는 것이다.
- `[해석]` **20호가 가져간 것은 원전 텍스트의 모양 서술**("(ii) the voltage drop within the first few seconds … (iii) the shallow, linear (or close to linear) voltage drop") **에서 시간 척도("first few seconds")를 뺀 것**이다. 원전 자신의 명제("resistance … governed by the measurement timescale")에 따르면 창을 바꾸면 내용이 바뀐다 — 20호의 `R_CT` 창은 원전의 **≈1.4–2.2 × 10³ 배**(2 s ↔ ≈0.8–1.2 h)이고 전류는 **1/360** 이다.
- `[재현]` 원전 규약(t = 1/f)으로 20호의 1 h 창을 옮기면 **≈0.28 mHz** — 원전 EIS 의 최저 주파수(10 mHz)보다 36 배 아래이고, 원전이 "low frequency diffusion dominated region" 이라 부른 쪽이다. `[해석]` **20호 곱 축퇴 처방 3-b 의 실패(`C = τ/R` 가 이중층 상한의 10²–10³ 배)는 원전의 틀이 예측하는 결과다** — 그 창에는 전하이동이 아니라 확산 · 화학 용량이 산다.
- `[해석]` **20호의 "접촉 저항 362 Ω"(= `R₀` 810 − SE 벌크 448)에 새 조건이 붙는다.** 원전이 보인 대로 "순간" `R₀` 는 **샘플링 대역 끝보다 빠른 모든 과정의 합**이다(0.1 s → |Z|(10 Hz), `R_CT` 일부 포함 — 원문 "the DC resistance calculated from pulse power tests will contain kinetic contributions (a portion of RCT)"). 20호 샘플 간격이 인쇄되지 않았으므로 **362 Ω 에 계면 전하이동 호가 섞였는지 지면으로 판정할 수 없다** — 20호 digest 가 이미 제기한 "이름표가 데이터에 의해 요구되지 않는다" 에 대역 쪽 이유가 하나 더 붙는다.
- **20호 G4("`R_CT`/`R_p` 경계를 어디서 긋는가의 규칙")의 답**: 원전의 규칙은 **"2 s · 10 s 데이터 점"** 이고, 그 근거는 `[인쇄]` "(ii) … from circa. instantaneous up to 2–5 seconds and (iii) … occurring at timescales 5 seconds" 한 문장(G8) — **이 셀(고출력 박막 LFP)의 관찰**이다. ASSB 로 옮길 규칙이 아니다.

## (5) 계보 — 31호 · 34호와의 자리

- **31호(Chien 2023, ICI)**: `R_ICI`(1–5 s 차단) ≈ EIS `R0+R1+R2` 합 — **시간 영역 총량 = 주파수 영역 합**이라는 같은 형태의 일치를 이 편이 5 년 먼저 5 방법에 걸쳐 인쇄했다. 두 편 모두 **총량의 일관성**이지 성분의 식별이 아니다.
- **34호(Liang 2026, 능동 펄스 BMS)**: 34호는 대역 이름표 셋(옴 >10³ Hz · 계면 10⁰–10³ Hz · 확산 <10⁻¹ Hz)만 두고, 인용 ref 21 제목이 "10 Hz sampling rate" 였다. **이 편은 10 Hz 샘플링의 대가를 같은 셀에서 잰 원전 표본이다** — `[인쇄]` "a typical battery cycler has an upper limit of 10 Hz for measurement resolution" · `[재현]` `R₀` +43 %. `[해석]` 34호가 "사전이 채운다" 고 적은 5 Hz 위 대역은, 이 편에서는 **직렬 R 로 흡수**된다 — 재구성이 없으면 사전 대신 흡수가 일어난다.

---

# 서지

| 항목 | 값 |
|---|---|
| 서지 | Anup Barai, Kotub Uddin, W. D. Widanage, Andrew McGordon, Paul Jennings, *Scientific Reports* (2018) **8**:21, `10.1038/s41598-017-18424-5` |
| 소속 | WMG, University of Warwick (전원) |
| 일정 | 접수 2017-06-28 · 게재확정 2017-12-12 · (PDF 표기 "Published: xx xx xxxx", © 2017) |
| 지원 | Innovate UK(WMG HVM Catapult, Jaguar Land Rover · TATA Motors 협력) · EPSRC EP/M507143/1, EP/N001745/1 |
| 라이선스 | CC BY 4.0 (오픈액세스) |
| 분량 | 13 쪽(본문 ≈11 쪽 + 참고문헌 37) · 그림 7 · 표 2 · SI 없음 |
| 경쟁 이익 | "no competing interests" |

# 셀 · 방법 (전부 `[인쇄]`)

- 셀: 상용 **20 Ah 파우치, 흑연(LiC₆) 음극 / LiFePO₄ 양극**. 충전 상한 3.6 V(10 s 펄스 3.8 V) · 방전 하한 2.0 V(10 s 펄스 1.6 V) · 제조사 최대 **15 C 순간**.
- 상태 조정: 2.0 V 까지 방전(= 0 % SoC) → 4 h 휴지 → CC-CV 1 C, 3.6 V, C/20 컷 → 4 h 휴지 → 1 C 30 min 방전(= 50 % SoC) → 4 h 휴지. 장비 Bitrode MCV 16-100-5 · 챔버 Weiss Gallenkamp Votsch VC3 4060. **25 °C**.
- 방법 다섯:
  1. **단일 펄스**: 5 C × 18 s 방전 → 1 h 휴지 → 5 C × 18 s 충전. 18 s 는 "one of the longest pulse durations outlined in current standards"(ISO 12405-2).
  2. **다중 진폭 펄스**(IEC 62660-1): 10 s, 1 · 2 · 5 · 최대 C(= 15 C), 펄스 사이 30 min 휴지.
  3. **전류 전환**: 5 C 방전 → 5 C 충전(각 5 s) · −1 C → −5 C · 1 C → 5 C.
  4. **1 kHz 측정기**: Hioki BT3563.
  5. **EIS**: Solartron Modulab 2100A + 2 A 부스터, 정전류, **10 mHz – 100 kHz**, RMS **0.2 · 0.5 · 0.8 · 1.0 · 1.4 A**.
  6. **다중사인**(Widanage 2016): 10 s 최대 충·방전 C-rate 를 덮는 펄스-다중사인 5 주기 → LPM 비모수 임피던스 + σ → **2차 ECM** 적합.
- DC 저항 = ΔV/ΔI. `R₀` = 0.1 s 점("the battery cycler … has a maximum resolution of 0.1 sec").

---

# 결과 — 절별 해체

## §1 이론 — DC (Fig. 1)

`[인쇄]` 전압 강하의 세 몫: (i) 순간 = `R₀`("all electronic resistances and the bulk electrolyte ionic resistance") · (ii) "within the first few seconds" = 이중층 + `R_CT` · (iii) "shallow, linear (or close to linear)" = `R_p`("ionic diffusion in the solid phase … usually considered to be the rate determining step").
다중 진폭: 저항 = V–I 직선의 기울기, "As long as the change in SoC is negligible and the battery does not enter into a regime of diffusion limitation".
하강 · 전환 모서리 `R₀`: 원리상 같아야 하나 하강 모서리에서는 전극 표면이 분극돼 있어 "small voltage differences".
`[도표]` **Fig. 1** 은 전류 계단(`ΔI`, `Δt_p`)과 전압 응답(빨강)을 그리고 `R₀`(수직 강하) · `R_CT`(곡선) · `R_p`(직선)를 표시한다. **검은 점선이 선형 구간을 펄스 시작점까지 외삽**하고, `ΔV₂`(= `R_CT` 몫) 화살표는 `R₀` 강하 뒤 수준에서 **그 외삽 절편 수준까지**다 — **20호 Fig. 4 주황 직선과 같은 작도**가 원전에는 **모식도로만** 있고 본문은 이 작도를 서술하지 않는다.

## §2 이론 — AC · EIS (Fig. 2)

`[인쇄]` 식 (1)–(6) 페이저 정의. Nyquist 에서 Im Z = 0 교차 = "typically correlated with the pure Ohmic resistance R0" · −Im 국소 극소의 Re − `R₀` = `R_CT` · "The real part of Z(ω) at min{−Im(Z(ω))}, in theory therefore, should correspond to the total resistance measured from other methods e.g. pulse power test."
`[도표]` **Fig. 2a** 모식 Nyquist: 가로축 구간 셋에 **`R₀` · `R_CT` · `R_D`** — 저주파 구간 이름이 본문(`R_p`)과 다르다(D8). **Fig. 2b** m차 ECM(`U` – `R₀` – m 개 `R_i‖C_i`).
1 kHz: 대용량(예 40 Ah 파우치)은 유도성 쪽, 소용량(예 3 Ah 18650)은 교차 근처라 "reliable and repeatable".

## §3 이론 — 다중사인

`[인쇄]` 식 (7) `V = Z·I + E`(E = 측정 오차 **또는 비선형 응답**) → LPM 으로 `Ẑ(ω_k)` 와 σ → 식 (8) 2차 ECM. "In this manuscript, a second order model is considered … as this has been shown to capture cell behaviour most accurately21."

## §4 DC 결과 — 단일 펄스 (Fig. 3 · Table 1)

`[인쇄]` Table 1 (5 C):

| 펄스 길이 (s) | 방전 (mΩ) | % | 충전 (mΩ) | % | 분해 |
|---|---:|---:|---:|---:|---|
| 0.1 | 1.31 ± 0.02 | — | 1.32 | — | RO + %RCT |
| 2 | 1.72 ± 0.02 | 31 | 1.70 | 29 | RO + RCT |
| 5 | 1.92 ± 0.02 | 46 | 1.85 | 41 | RO + RCT + %RP |
| 10 | 2.12 ± 0.02 | 62 | 2.00 | 52 | RO + RCT + RP |
| 18 | 2.38 ± 0.02 | 82 | 2.13 | 62 | RO + RCT + RP |

⚠ **10 s 와 18 s 가 같은 분해 이름("RO + RCT + RP")인데 값이 +12 %(방전) · +7 %(충전) 다르다** — `R_p` 는 이 창에서 포화하지 않는다. 이름은 고정, 값은 창.
`[도표]` **Fig. 3a · b**: 전류 ≈ −97 / +97 A(명목 100 A), 방전 전압 ≈3.300 → ≈3.070 V(18 s). `[재현]` 0.230 V / 97 A ≈ **2.37 mΩ** ↔ 인쇄 2.38 ✓. **Fig. 3c · d**: `R(t)` 곡선 1.31 → ≈2.38(방전) · 1.32 → ≈2.13(충전), 구간 막대 (i) t = 0 선 · (ii) ≈0–5 s · (iii) ≈3–18 s — **(ii) 와 (iii) 막대가 겹친다**. 후반 직선 적합이 그려져 있고 그림 안 인쇄 **R² = 0.9951(방전) · 0.982(충전)**.
`[인쇄]` 방전 > 충전 해석: "On discharging a cell, Lithium is transferred from a high energy state in the anode to a low energy configuration in the cathode, hence, the resistance values for discharging are higher".

## §5 DC 결과 — 진폭 (Table 2)

`[인쇄]` Table 2 (캡션 "discharge pulses" 이나 충전 행 포함 — D1):

| 길이 (s) | 1 C | 2 C | 5 C | 15 C |
|---|---:|---:|---:|---:|
| 방전 0.1 | 1.35 ± 0.05 | 1.37 ± 0.03 | 1.31 ± 0.02 | 1.30 ± 0.01 |
| 방전 2 | 1.76 | 1.81 | 1.72 | 1.66 |
| 방전 5 | 2.07 | 2.12 | 1.92 | 1.84 |
| 방전 10 | **2.49** | 2.49 | 2.12 | **2.05** |
| 충전 0.1 | 1.35 ± 0.05 | 1.35 ± 0.03 | 1.32 ± 0.02 | 1.30 ± 0.02 |
| 충전 2 | 1.76 | 1.76 | 1.70 | 1.51 |
| 충전 5 | 2.02 | 1.99 | 1.85 | 1.59 |
| 충전 10 | **2.33** | 2.23 | 2.00 | **1.70** |

(± 는 열마다 같아 첫 행에만 옮겼다.)
`[인쇄]` 0.1 s 값은 진폭에 거의 무관(SD 0.05 mΩ) · 2–10 s 는 진폭 의존("the difference between resistance measured with a 2 second and 10 sec pulse is 0.73 mΩ using a 1 C discharge pulse, while it is 0.39 mΩ using a 15 C") · 원인은 "various electrochemical processes that are activated … and the heat generation" · `[재현]` 발열 "0.5 Wh (1800 Joules) in just 10 seconds when 300 A (15 C) … through a 2mΩ" = 300² × 0.002 × 10 = **1800 J ✓** · SoC 변화 1 C 10 s **0.28 % ✓** · 15 C 10 s **4.2 % ✓**(`[재현]` 4.17 %). "Within the Butler-Volmer framework, these peaks may be associated with the temperature-overpotential duality."
`[인쇄]` LFP 평탄(70–40 % SoC) 때문에 4.2 % SoC 변화는 "little impact" · "For battery technologies with steeper OCV curves, such as LiNiCoAlO2 and LiNiMnCoO2 however, the effect is expected to be more pronounced."
★ `[재현]` **진폭 축의 크기가 시간 축과 같다**: 10 s 창에서 진폭만 바꾼 범위 1.70–2.49 = **×1.46**(방전 1 → 15 C −18 % · 충전 −27 %) ↔ 5 C 방전에서 창만 바꾼 범위(0.1 → 10 s) 1.31–2.12 = **×1.62**. EIS 0.1 Hz(1.91)와 대면 1 C 방전 **+30 %** · 15 C 충전 **−11 %** — "timescales match → align" 은 **5 C 에서만** 보였다(D6).

하강 · 전환 모서리: `[인쇄]` 하강 모서리 `R₀` 방전 1.30 / 1.35 / 1.35 / 1.40 · 충전 1.40 / 1.40 / 1.40 / 1.56 mΩ(1 · 2 · 5 · 15 C). "On average, the values for discharge are less than 0.1 mΩ higher than those shown in Table 2." `[재현]` 방전 평균 1.35 ↔ 1.33(+0.02) ✓ · 충전 평균 1.44 ↔ 1.33(**+0.11**, 문장은 방전만 말한다).
`[도표]` **Fig. 4d**(그림 안 인쇄 표): 전환 `R₀` **Dis-Ch 1.34 · Dis-Dis 1.39 · Ch-Ch 1.37 mΩ**. **Fig. 4a–c** 전류 계단 t = 2 s · 7 s · 12 s, 1 C ≈ ±20 A · 5 C ≈ ±97 A.

## §6 AC 결과 (Fig. 5)

`[인쇄]` 1 kHz 측정기 **0.82 mΩ**, 유도성 영역. EIS 진폭 0.2–1.4 A: "no identifiable differences … as expected" · 0.2 A 만 잡음 · "resistance measured using EIS is not dependent on current amplitude" · "if a higher current like 1 C was used for the EIS test, it would have an effect on results" · C/20(1 A) 채택.
`[인쇄]` Nyquist: `R₀` = **0.92 mΩ @ 251 Hz(4 ms)** · 국소 극소 **1.55 mΩ @ 2 Hz** ⇒ `R_CT` **0.63** · `R_p` 는 "not well-defined" → **0.1 Hz 0.36 · 0.01 Hz 1.39 mΩ**. EIS @1 kHz 0.79(p. 9).
`[도표]` 원본 래스터(1000 × 1153) 화소 판독:
- **Fig. 5a** Nyquist 끝점(0.01 Hz 쪽) **Re ≈2.62 · −Im ≈1.35 mΩ** ⇒ `[재현]` |Z| ≈2.95 · 위상 ≈−27°. 1 kHz 표지 점 Re ≈0.80(인쇄 0.79 ✓) · −Im ≈−0.84. 인셋: 교차 Re ≈0.93 · 호 꼭짓점 ≈(1.25, 0.19) · 극소 ≈(1.55, 0.15). 다섯 진폭 겹침.
- **Fig. 5b** Bode(그림 축 0.01 – 10⁴ Hz — 측정 상한 100 kHz 는 그리지 않았다): |Z| **0.01 Hz ≈2.95 · 0.1 Hz ≈1.91 · 1 Hz ≈1.61 · 10 Hz ≈1.40 · 최소 ≈0.86 @ ≈500–650 Hz · 1 kHz ≈1.0 · 10 kHz ≈6.9**. 위상 **0.01 Hz ≈−27° · 0.1 Hz ≈−12° · 1 Hz ≈−6° · 10–100 Hz ≈−7…−9° · 251 Hz ≈0° · 1 kHz ≈+40° · 10 kHz ≈+80°**.
- ⇒ `[재현]` 0.1–100 Hz 는 **위상 ≤≈12° · |Z| 기울기 ≈15–19 %/decade**(10 → 1 Hz +15 % · 1 → 0.1 Hz +19 %)의 거의 평탄한 스펙트럼이다(R8 의 근거).

## §7 다중사인 결과 (Fig. 6)

`[인쇄]` 2차 ECM: `R₀` **1.618 ± 0.003** · `R₁`("RCT") **1.10 ± 0.07** · `R₂`("Rp") **0.109 ± 0.005 mΩ** · "Although the ECM parameters are not uniquely identifiable" · `R₀` 과대의 두 이유 "i) the fact that most of the power in the driving current signal belongs to harmonics lower than 1 Hz, and/or ii) … the parameters do not reflect the physical meanings attributed to them (due to unique identifiability)" (sic).
`[도표]` **Fig. 6** 가로축 **선형 0–1 Hz**, 점 간격 ≈0.033 Hz, **첫 점 ≈0.017 Hz**(인쇄 "0.01 Hz minimum frequency" — D10). 첫 점 크기 **≈−54.08 dB ⇒ `[재현]` ≈1.98 mΩ** · 1 Hz 쪽 ≈−55.7 dB ⇒ ≈1.63 mΩ · 위상 첫 점 ≈−12.6°, 1 Hz 쪽 ≈−1.5 … −2.5°.
★ `[재현]` **다중사인 "총저항" 2.83 mΩ(= `R₀+R₁+R₂`) 은 ECM 의 ω → 0 극한이고, 여기된 최저 주파수(≈0.017 Hz)의 측정 크기는 ≈1.98 mΩ 이다** — Fig. 7b 가 100 s 에 찍은 2.83 은 **데이터 밖 외삽**이다.
★ `[재현]` **같은 주파수에서 대진폭(다중사인) ↔ 소진폭(EIS)이 어긋난다**: ≈0.017 Hz 1.98 ↔ EIS ≈2.6(**−24 %**) · 0.1 Hz 부근 ≈1.70 ↔ 1.91(**−11 %**) · 1 Hz 1.63 ↔ 1.61(≈0). `[해석]` 느린 대역에서 진폭이 값을 바꾼다 — Table 2 의 고율 저하와 같은 방향. **"비선형이 아니라 시간 척도" 라는 결론(D6)에 원문 자신의 두 그림이 반대 증거를 준다.**

## §8 비교 (Fig. 7)

`[도표]` **Fig. 7a**(그림 안 인쇄 표):

| | `R₀` 시간 (s) | `R₀` | `R_CT` | `R_p` | `R_total` |
|---|---|---:|---:|---|---|
| 5 C 방전 | 0.1 | 1.31 | 0.41 | 0.40 (0.1 Hz) | 2.12 ± 0.02 |
| 5 C 충전 | 0.1 | 1.32 | 0.38 | 0.30 (0.1 Hz) | 2.00 ± 0.02 |
| 1 kHz | <0.001 | 0.82 | – | – | 0.82 ± 0.04 |
| EIS | <0.001 | 0.92 | 0.63 | 0.36 (0.1 Hz) · 1.39 (0.01 Hz) | 1.91 ± 0.01 · 2.94 ± 0.01 |
| 다중사인 | ~1 | 1.62 | 1.10 | 0.11 | 2.83 ± 0.07 |

(DC `R_p` 칸에 "(0.1 Hz)" — 10 s 펄스를 0.1 Hz 로 표기했다. EIS `R₀` 시간 "<0.001" ↔ 본문 4 ms — D3.)
**Fig. 7b**: 가로축 "Timescale (s)" 로그 10⁻⁴–10³, EIS 곡선 + 펄스(방전 □ · 충전 ◆) 0.1 · 1 · 2 · 5 · 10 s + 1 kHz(●, 0.001 s) + 다중사인(✕, 1 s · 100 s).
`[도표]` 곡선은 10⁻⁴ s ≈6.9 → 최소 ≈0.88 @ ≈0.002 s → 0.1 s ≈1.4 → 100 s ≈2.9 — **Bode |Z| 와 같은 곡선**(Re 아님). ⇒ 1 kHz 측정기 점(0.82)이 곡선(≈1.0–1.1)보다 **아래에** 찍혀 있다 — 측정기 값은 본문이 Re(0.79)와 맞췄는데 그림은 |Z| 위에 얹었다(D12).
`[인쇄]` 비교 문장: 10 Hz EIS 1.41 ↔ DC 1.33 · 0.5 Hz 1.69 ↔ 2 s "1.71 ± 0.01"(표 1 은 1.72 ± 0.02 · 1.70 — D2) · 0.1 Hz 1.91 ↔ 10 s 2.12 / 2.00("expected to be slightly higher than EIS results" — 이유: 지속 DC 의 추가 삽입 · 탈리, AC 는 "lithium saturation" 회피) · 1 Hz 1.62 ↔ 다중사인 `R₀` 1.62 ↔ 1 s 펄스 1.61 · 0.01 Hz ↔ 다중사인 총 2.83("close").

## §9 적용 · 결론

`[인쇄]` ECM 식별의 모호성 문단(판정 (3)-1) · 다중사인이 "better represent actual battery usage" → 시스템 모델용 · 1 kHz 는 "not much value" · 장기 열화 특성화에는 EIS "may be a more appropriate method … conclusions can be derived for the contribution of SEI to degradation" · "it may be advantageous therefore, to perform a reliable EIS test only".
결론: "for the first time it has been shown that it is not the non-linearity …" · "the discrepancy in measuring pure Ohmic resistance … originates from the limitation of the test equipment" · "For the first time, it is demonstrated that the resistance measured with different techniques can be estimated from an EIS test result" · "EIS can accurately provide separation and identification of all the individual resistance components".

---

# `[재현]` 장부

| # | 계산 | 결과 | 판정 |
|---|---|---|---|
| R1 | Fig. 3a ΔV / I (18 s 방전) | 0.230 V / ≈97 A = 2.37 ↔ 2.38 mΩ | ✅ |
| R2 | Table 1 차분 → Fig. 7a 성분 | `R_CT` 1.72−1.31 = 0.41 · 1.70−1.32 = 0.38 · `R_p` 2.12−1.72 = 0.40 · 2.00−1.70 = 0.30 | ✅ (성분 = 창 차분) |
| R3 | EIS `R_p` = 총 − 1.55 | 1.91−1.55 = 0.36 · 2.94−1.55 = 1.39 | ✅ 산술 · ⚠ 섞인 양(R6) |
| R4 | 발열 · SoC | 1800 J ✓ · 0.28 % ✓ · 4.17 % ✓ | ✅ |
| R5 | DC `R₀` 과대 | 1.315 / 0.92 = **+43 %** · 1.33 ↔ \|Z\|(10 Hz) 1.41 −6 % | ✅ 원문 해석과 양립 |
| R6 | EIS 0.01 Hz: Re ↔ \|Z\| | Nyquist 끝점 Re ≈2.62 · \|Z\| ≈2.95 ⇒ 표의 2.94 = **\|Z\|**. Re 로 하면 총 ≈2.62 · `R_p` ≈1.07 | ⚠ 같은 표 안에서 `R₀` · `R_CT` 는 Re, 0.01 Hz 총은 \|Z\| (D4) |
| R7 | 5 C 펄스 ↔ EIS(t = 1/f) | −6 / −1 / +1 / +11(방) · +5(충) % | ✅ ±11 % |
| R8 | 같은 비교를 **t = 1/(2πf)** 로 | 0.1 s 1.33 ↔ \|Z\|(1.59 Hz) ≈1.57(−15 %) · 2 s 1.71 ↔ \|Z\|(0.08 Hz) ≈1.97(−13 %) · 10 s 2.12 / 2.00 ↔ \|Z\|(0.016 Hz) ≈2.6(−18 / −23 %) | ⚠ 규약을 0.8 decade 옮기면 일치가 −13 … −23 % 로 벌어진다 — **일치의 시간 분해능 ≈1 decade** |
| R9 | 진폭 축 ↔ 시간 축 | 10 s 창 진폭 범위 ×1.46 ↔ 5 C 창 범위 ×1.62 · 1 C 방전 +30 % · 15 C 충전 −11 % vs EIS 0.1 Hz | ⚠ 결론(비선형 아님)과 긴장 (D6) |
| R10 | 다중사인 총 ↔ 측정 | ECM ω→0 2.83 ↔ 최저 여기(≈0.017 Hz) 측정 ≈1.98 | ⚠ 외삽 |
| R11 | 대진폭 ↔ 소진폭 같은 f | 0.017 Hz −24 % · 0.1 Hz −11 % · 1 Hz ≈0 | ⚠ 느린 대역 진폭 의존 |
| R12 | 성분 이름의 방법 간 퍼짐 | `R₀` ×2.0 · `R_CT` ×2.9 · `R_p` ×13 (EIS 경계만 ×3.9) | 성분 = 경계 선택 |
| R13 | EIS ↔ DC 경계 위치(t = 1/f) | `R₀`: 4 ms ↔ 0.1 s(×25) · `R_CT`/`R_p`: 2 Hz(= 0.5 s) ↔ 2 s(×4) | ⚠ 같은 논문 안에서 두 방법의 경계가 다른 시간에 있다 — 성분 칸은 비교 대상이 아니다(원문도 `R_CT` 에 대해 인정) |
| R14 | ± 의 크기 | 1 mV ÷ I: 20 A 0.05 · 40 A 0.025 · 100 A 0.01 · 300 A 0.003 ↔ 인쇄 0.05 · 0.03 · 0.02 · 0.01–0.02 | `[해석]` 저율 두 열은 양자화와 일치(G2) |
| R15 | 20호 창 ↔ 원전 창 | `R_CT` 2 s ↔ ≈0.8–1.2 h = ×1.4–2.2 × 10³ · 전류 5 C ↔ C/72 = ×360 · 1 h ↔ 0.28 mHz(원전 EIS 하한 10 mHz 의 1/36) | 판정 (4) |

---

# 곱 축퇴 처방 — 서른두 번째 적용 (⚠ 액체, 도구 칸)

카드의 곱(`A_eff·ε_p/R_s`)은 대상이 없다(액체 · 상용 셀 · 열화 0). 처방의 **4단계(시간 ↔ 주파수)** 가 이 편의 본체이고, 나머지는 입력이 없다.

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C`(또는 τ) | EIS 적합 0(Nyquist 판독만) · 다중사인 τ₁ · τ₂ 미인쇄(G5) | ❌ |
| **2단계** 면적 대조군 | 셀 한 종 · 면적 축 0 | ❌ |
| **3단계-a** `Ea` | 25 °C 한 점(온도는 발열 서술뿐) | ❌ |
| **3단계-b** `C` 상한 | DC `R_CT` 0.41 mΩ · τ ≲ 2 s ⇒ `[재현]` 셀 단위 `C` ≲ 5 × 10³ F — 전극 면적 · 질량 · BET 미인쇄(G6) | ⚠ 판정 불가 |
| **4단계** 시간 ↔ 주파수 | ★ 편 전체 — Fig. 7b | ✅ **총량에서 ±11 %(5 C, t = 1/f)** · 성분에서는 원문이 "not meaningful" · 분해능 ≈1 decade(R8) · 진폭 의존(R9 · R11) |

⇒ 이 적용이 처방에 더하는 것 — **새 줄 "창 규약"**: 시간 영역 성분(4단계 · 20호 번역 · 34호 온보드)을 쓸 때 값 옆에 (i) **대역 위쪽 끝**(샘플 간격 · 여기 최고 주파수 — 직렬 `R` 이 그보다 빠른 모든 것을 흡수) (ii) **시간 ↔ 주파수 대응 규약**(1/f · 1/2πf)과 그 대역의 **|Z| 기울기**(일치 판정의 분해능) (iii) **전류 진폭**(같은 창에서 ×1.46) (iv) ECM 총량이면 **최저 여기 주파수 밖 외삽인지**를 적는다.

---

# 칸별 요약 (채움표 행)

| 칸 | 판정 |
|---|---|
| **Q1 정량** | **없다 — `θ(N)` 0/49.** 액체 · `contact` 0 회 |
| **Q2 독립관측** | **해당 없음(액체) — 도구 칸.** 5 방법이 **총량**에서 한 곡선에 모인다(시간 ↔ 주파수 일관성, 31호 형태의 원전) — 성분 분리는 원문이 "inability" · "not well-defined" · "pre-defined" 로 스스로 사양. `[해석]` 저항 성분 **식별**에 대한 이 편의 뜻: 창 이름표(`R₀`/`R_CT`/`R_p`)는 식별된 양이 아니다 — 식별하려면 스펙트럼 수준의 배정(R·C · 시상수)이 필요하다 |
| **Q3 라벨층위** | 층 둘 — **window-differenced reads under a declared convention**(성분 = 고정 시점 · 주파수에서 읽은 값의 차, 규약 t = 1/f 는 한 문장 근거) · **unstated-origin ±, column-constant**(± 가 열마다 상수, 저율 두 열은 1 mV 양자화와 일치 — 셀 수 미인쇄) |
| **Q4 유일성** | **0/49(ASSB 0 — 도구 칸) — 마흔한 번째 성질 "비식별을 두 곳에 인쇄하고 결론에서 지웠다"**: 적합의 비유일성(`[인쇄]` "not uniquely identifiable" · "ambiguities … Ro and RCT" · "judged solely on closeness of fit")과 작도의 비분리(`[인쇄]` "inability to completely separate" · "usual prescription" · `R_p` "pre-defined")를 본문에 적고, 결론은 "EIS can accurately provide separation and identification of all the individual resistance components". 창 의존성은 식별 불가의 증거가 아니라 **시간 척도 정렬의 일관성**으로 처리. 폭 · 조건수 · CI 0. `identifiab` 3(파라미터 뜻 2) · `uniqu*` 4 · `ambigu*` 3. 누적 0.5 그대로 |
| **Q5 Li-In** | **해당 없음** — 2전극 상용 파우치, 기준극 0 |
| **Q6 압력** | **없다** — `pressure` · `MPa` 0 회 |
| **Q7 dead Li** | **해당 없음** |
| **Q8 화학·OCP** | **해당 없음(액체 LFP/흑연)** — `[인쇄]` 평탄 70–40 % SoC 에서 4.2 % SoC 변화 "little impact", 가파른 OCV(NCA · NMC)에서는 "more pronounced" — OCP 수치 0 |

**채움표 이동: ≈20.0 → ≈20.0 (새 칸 0).**

---

# 어긋남 (D)

| # | 자리 | 내용 |
|---|---|---|
| D1 | Table 2 캡션 · 본문 | 캡션 "different amplitude discharge pulses" ↔ 충전 행 포함 · 본문 "five charge-discharge pulses of varying amplitudes" ↔ 표 4 율(1 · 2 · 5 · 15 C) · 방법 "1 C, 2 C, 5 C and maximum C" |
| D2 | p. 10 ↔ Table 1 | 2 s `R₀+R_CT` "1.71 ± 0.01" ↔ 표 1.72 ± 0.02(방전) · 1.70(충전) — 두 값의 평균으로 보이나 ± 출처 불명 |
| D3 | Fig. 7a ↔ 본문 | EIS `R₀` 시간 "<0.001 s" ↔ 본문 251 Hz = 4 ms |
| **D4** | Fig. 7a EIS 행 · §6 | `R₀`(0.92) · `R₀+R_CT`(1.55) = Re Z(Nyquist) ↔ 0.01 Hz 총 2.94 = \|Z\|(Bode) — `[재현]` Re ≈2.62. EIS `R_p`(0.01 Hz) 1.39 는 두 양의 차 |
| **D5** | 결론 ↔ §6 · §8 | "EIS can accurately provide separation and identification of all the individual resistance components, Ro, RCT and Rp" ↔ "Estimating polarisation resistance using EIS results is not well-defined" · "Rp … is pre-defined" |
| **D6** | 결론 ↔ Table 2 · Fig. 6 | "not the non-linearity … rather the timescale" ↔ 같은 창 10 s 에서 진폭만으로 ×1.46(원문은 BV · 발열로 해석) · 대진폭 다중사인 ↔ 소진폭 EIS 가 0.017 Hz 에서 −24 % |
| D7 | §6 "resistance measured using EIS is not dependent on current amplitude" | 시험 범위 0.2–1.4 A RMS(≤0.07 C) ↔ DC 펄스 20–300 A — 소신호 범위 안의 진술이다(원문도 "if a higher current like 1 C was used … it would have an effect"). 결론의 "비선형이 아니다" 를 받치지 않는다 |
| D8 | Fig. 2a ↔ 본문 | 저주파 구간 이름 `R_D` ↔ 본문 `R_p` |
| D9 | p. 7 | "occurring at timescales 5 seconds" — 관계 기호 누락(G8, 렌더 확인) |
| D10 | Fig. 6 ↔ p. 11 | "multisine signal with 0.01 Hz minimum frequency" ↔ `[도표]` 첫 점 ≈0.017 Hz |
| D11 | 하강 모서리 문장 | "the values for discharge are less than 0.1 mΩ higher" — 방전 +0.02 ✓, 충전은 `[재현]` +0.11(문장 밖) |
| D12 | Fig. 7b | 1 kHz 측정기 점(0.82, Re 기준 — 본문 대조값 0.79)이 \|Z\| 곡선(≈1.0–1.1) 위에 얹혀 곡선 아래로 보인다 |
| D13 | p. 8 | 다중사인 `R₀` 과대 이유 (ii) "(due to unique identifiability)" — 뜻은 비유일성(sic) |
| D14 | p. 3 · p. 10 | "there in an inability" · "in not meaningful" (sic, 조판 오탈자) · "Section 2.1" / "Sec. 2.1." ↔ 번호 없는 절 |
| D15 | 평균 `R₀` 두 값 | p. 8 "1.33 mΩ with standard deviation of 0.04" ↔ p. 10 "1.315 mΩ" — 모집단이 다르다(전 DC 방법 ↔ 5 C 두 값) |

---

# 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계(앞) · 본문(참고문헌 전). SI 없음.
NFKC 변경 본문 **404 자**(U+2009 얇은 공백 298 · NBSP 34 · U+2002 9 · U+2003 5 · `ϕ` 15 · `Ω`(U+2126 옴 기호) 43) — **열 변화 0**. 소프트 하이픈 0. **줄끝 하이픈 45 곳** — 이으면 `charge transfer` 7 → 8("trans-fer") · `amplitude` 17 → 18 · `polari[sz]*` 8 → 9, **열 변화 0**.

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **3** | **1** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- `identifiab` 3 = 파라미터 뜻 **2**("not uniquely identifiable" · "due to unique identifiability") + 무관 1("no identifiable differences" — EIS 진폭). `uncertaint` 1 = 열량계 방법의 "large uncertainty"(재인용).
- 보조: `timescale` **20** · `window` **0** · `uniqu*` 4 · `ambigu*` 3 · `pre-defined` 3(`R_p` 1) · `well-defined` 1("not") · `non-?linear*` 3 · `nonlinearity` 2 · `extrapolat*` 0 · `Kramers` 0 · `Warburg` 0 · `capacitan*` 3 · `double layer` 4 · `time constant` 1 · `error` 4(식 7 · 최소제곱) · `standard deviation` 3 · `repeat*` 3 · `reproducib*` 0 · `n =` 0 · `fit*` 10 · `ECM` 14 · `harmonic` 3 · `resolution` 3 · `10 Hz` 5 · `inductive` 8 · `Nyquist` 11 · `Bode` 3 · `EIS` 55 · `pulse` 114 · `Ohmic` 25 · `temperature` 12 · `heat` 9 · `contact` 0 · `pressure` 0 · `SEI` 3 · `degrad*` 3 · `ag(e)ing` 4 · `assum*` 1(고율 펄스가 사용을 모사한다는 가정).
- `[해석]` **`window` 0 · `timescale` 20** — 이 편은 창을 "시간 척도" 로 부르고, 창의 **경계**(어디서 끊는가)는 낱말이 아니라 표의 행 머리(0.1 · 2 · 10 s)와 "pre-defined" 로 나타난다. 경계 선택을 낱말 지문으로 잡으려면 `pre-?defined` · `prescription` · `data point` 를 같이 센다.

---

# 그림 — 본 것 / 안 본 것

크로퍼 7 장(`wiki/raw/figures/barai2018_measurement-timescale-internal-resistance-methods/`, Fig. 1–7) — **7 장 다 봤다, 안 본 것 0 장.** Table 1 · 2 는 PDF 텍스트(크로퍼가 영역 없음으로 제외).
화소 판독(원본 래스터 추출): **Fig. 5a**(Nyquist 끝점 · 1 kHz 점) · **Fig. 5b**(Bode 여섯 주파수의 |Z| · 위상) · **Fig. 6a**(첫 점 dB · 주파수) · **Fig. 7b**(곡선 최소 · 0.001 s 값). 300 dpi 렌더 확인: p. 7 "timescales 5 seconds"(기호 누락).
**본문 서술과 어긋난 그림**: Fig. 6(최저 주파수 ≈0.017 ↔ "0.01 Hz") · Fig. 7b(1 kHz 점이 |Z| 곡선 아래 — Re/|Z| 혼용) · Fig. 7a(EIS `R₀` 시간 <0.001 ↔ 4 ms) · Fig. 2a(`R_D` ↔ `R_p`). Fig. 1 은 본문이 서술하지 않은 **선형 외삽 작도**를 그린다(20호 Fig. 4 의 모양).

---

# 계보에서의 자리

- **20호 ref [24]** — 3성분 분해의 근거로 인용됐다. 원전은 분해를 **분리 불가라고 인쇄한 채 "usual prescription"(ref 8 Waag 2013)으로 따른** 편이다 — **작도의 원전은 이 편이 아니라 Waag 2013 쪽**이고(20호도 [25] 로 함께 인용), 이 편은 그 규약을 시간 척도로 **해석**한 편이다.
- **31호**(ICI ↔ EIS 합) · **34호**(10 Hz · 대역 이름표)와 같은 축 — 이 편이 **가장 이르고(2018) 가장 직접적인 수치**(10 Hz 의 +43 %)를 준다.
- 큐 51–59 인용 **0**(2018 액체 편이라 당연). ref 목록 37 편 중 ASSB 0.

---

# 후속 (서지 기준, 미열람)

| 서지 | ref | 왜 |
|---|---|---|
| **Waag, Käbitz, Sauer 2013, *Applied Energy* 102, 885–897** | 8 | "usual prescription of calculating Ro, RCT and Rp with DC methods" 의 출처 — **작도 규약의 실제 원전**, 20호 [25] 와 같은 편(두 번째 지목) · 진폭 비선형 해석(이 편이 반박한 쪽) |
| Schweiger et al. 2010, *Sensors* 10, 5604 | 22 | 교차 방법 비교의 선행 — "AC impedance … cannot be directly compared to that from pulse power test" |
| Widanage et al. 2016, *J. Power Sources* 324, 61–69 (Part 2) · 70–78 (Part 1) | 21 · 20 | 다중사인 · LPM · 2차 ECM 선택 근거 — 대역 끝이 직렬 R 을 정하는 구조의 원설계 |
| Barai et al. 2015, *J. Power Sources* 280, 74–80 | 18 | 이완 시간이 EIS 에 미치는 영향 — 4 h 휴지의 근거(20호는 20 min) |
| Smith & Wang 2006, *J. Power Sources* 161, 628–639 | 28 | 펄스의 고체 확산 한계 — `R_p` 창의 물리 |

---

# 이 digest 가 주장하지 않는 것

- **"t = 1/f 규약이 틀렸다" 고 주장하지 않는다.** R8 은 다른 규약이면 일치가 −13 … −23 % 로 벌어진다는 **그림 판독 위의 대조**이고, 주장은 "이 셀의 평탄한 스펙트럼에서 일치 판정의 시간 분해능은 ≈1 decade" 까지다.
- **"결론(비선형이 아니다)이 틀렸다" 고 단정하지 않는다.** 진폭 의존(×1.46)을 원문은 발열 · BV 로 해석했고, 발열은 비선형이라기보다 상태 변화다. 주장은 **"시간 척도만으로 값이 정해진다" 가 5 C 한 진폭에서 보였고, 같은 지면의 다른 진폭 · 다중사인은 그렇지 않다**는 것까지다.
- **다중사인 ≈1.98 mΩ(0.017 Hz)을 측정값으로 인용하지 않는다** — dB 축 화소 판독(±≈0.02 dB ≈ ±0.5 %)이고 주파수 격자는 점 간격에서 추정했다.
- **± 가 양자화라고 단정하지 않는다**(R14 는 두 열의 일치 · 가설).
- **20호의 결론(음극이 용량 손실 원인)을 이 편으로 흔들지 않는다** — 흔드는 것은 20호 `R_CT` · "접촉 저항" 의 **이름표**와 경계 규칙뿐이다.
- **이 편의 수치를 ASSB 로 옮기지 않는다** — 액체 · 상용 파우치 · 한 상태. 옮기는 것은 **"창 끝이 값을 정한다" 는 구조**와 **보고 규약**이다.
- 우리 연구 수치의 정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md` — 여기서 비교하지 않는다.

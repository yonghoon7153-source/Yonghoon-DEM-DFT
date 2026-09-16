---
title: "Shi, Zhang, Tu, Wang, Scott, Ceder 2020 — Characterization of mechanical degradation in an all-solid-state battery cathode (J. Mater. Chem. A 8, 17399)"
source_url: local-upload/04._Sup_Characterization_of_mechanical_degradation_in_an_all-solid-state_battery_cathode.pdf
source_url_si: local-upload/04._Characterization_of_mechanical_degradation_in_an_all-solid-state_battery_cathode.pdf
source_url_note: "업로드 파일명이 서로 바뀌어 있다 — 파일명에 Sup_ 이 붙은 쪽(6쪽)이 본문이고 안 붙은 쪽(7쪽)이 ESI 다. 아래 해시는 내용 기준"
source_doi: 10.1039/d0ta06985j
pdf_sha256_main: 102f2791a98bc1cb67335f2496701018640cea9c3380990d8762b4f81e103fbe
pdf_sha256_si: bbe3568e1825566da687facc39d034955e9ceacd37a1f8cead8bdb6501507011
ingested: 2026-09-16
sha256: 37324b24d8de02453b2d0a08a5068ce9abd9ba27a695825b66100d14fd49c2bd
---

# 수집 목적

Tan Shi‡, Ya-Qian Zhang‡, Qingsong Tu, Yuhao Wang, M. C. Scott (교신),
Gerbrand Ceder (교신), **"Characterization of mechanical degradation in an
all-solid-state battery cathode"**, *Journal of Materials Chemistry A* **8**
(2020) 17399–17404, doi `10.1039/d0ta06985j` (Communication, Received 17 July
2020 / Accepted 11 August 2020 / Published 20 August 2020, CC-BY-NC 3.0) 의
**절별 해체분석** — 본문 PDF 6 쪽 + ESI(Supporting Information) 7 쪽.

**이 위키 `assb` 섹션의 4호 논문이다.** 액체셀 계열과 **섞지 않는다** — 음극 축이
다르다. 닻은 `questions/assb-contact-loss-vs-lampe.md`.

> ⚠ **업로드 파일명이 서로 바뀌어 있었다.** 파일명에 `Sup_` 이 붙은 쪽
> (`3759fa18-…_Sup_…pdf`, 6 쪽)이 **본문**이고, 붙지 않은 쪽
> (`49134dd6-…pdf`, 7 쪽)이 **ESI** 다. 첫 쪽을 열면 즉시 갈린다 — ESI 1 쪽이
> "Supporting Information" 표제, 본문 1 쪽이 저널 헤더(`Cite this: J. Mater.
> Chem. A, 2020, 8, 17399`)다. 아래 `pdf_sha256_main` / `pdf_sha256_si` 는
> **내용 기준**으로 붙였다 (파일명 기준이 아니다).

**★ 이 논문이 이 계보에서 하는 일**: `assb` 1·2·3 호가 **전부 시뮬레이션**이었고
Q2(독립 관측)가 **3/3 편 연속 0** 이었다. **4호에서 그 칸이 깨진다** — 처음부터
끝까지 실험이고, 시뮬레이션이 한 줄도 없다. 그리고 **Q6(압력)도 같이 깨진다**:
`assb` 3/3 편이 `pressure` 0 회였는데 이 논문은 압력을 **제작 변수 · 사이클
경계조건 · 개입 변수** 셋으로 쓴다.

---

# 0. 이 digest 를 쓰기 전에 실제로 본 것

크로핑 6 장 중 **6 장 전부**를 Read 했다
(`wiki/raw/figures/shi2020_mechanical-degradation-assb-cathode/`):

| 파일 | 무엇 | 봤나 | 왜 |
|---|---|---|---|
| `fig_1.png` | Fig. 1 전기화학 + EIS | ✅ | 이 논문 수치의 본체. **본문에 없는 수를 여럿 준다** |
| `fig_2.png` | Fig. 2 FIB-SEM 워크플로 | ✅ | 해상도·척도 확인 |
| `fig_3.png` | Fig. 3 3D 재구성 3 시점 | ✅ | **`θ(N)` 시간축의 실물** — void vol% 3 개 |
| `fig_4.png` | Fig. 4 단면 SEM + 접촉 손실 라벨 | ✅ | 10.4 % 의 근거 그림 |
| `fig_S1.png` | Fig. S1 별도 셀의 사이클 + **V–Q 곡선** | ✅ | **이 계보 최초의 사이클별 실측 전압곡선** |
| `fig_S2.png` | Fig. S2 회색도 히스토그램 | ✅ | 10.4 % 가 딛고 선 분할의 신뢰성 |

**추출되지 않은 것 하나**: ESI **Fig. S3**(Weka 분할 워크플로, ESI 7 쪽 중 6 쪽).
캡션이 PDF 안에서 `Fi` / `gure S3.` 로 줄이 끊겨 있어 캡션 탐지에 걸리지 않았다.
내용은 텍스트로만 확인했다 — 분할 방법 그림이고 **정확도 수치가 없다**(§11 D11).
**이 digest 에 Fig. S3 을 본 것처럼 쓴 문장은 없다.**

표기 규약 (이 위키 관례):
- `[인쇄]` = 원문 본문/캡션에 **문자로 적힌 것**
- `[도표]` / `figure-read ≈` = **내가 그림을 보고 읽은 값** (원문에 숫자가 없다)
- `[재현]` = 원문 값들로 내가 **계산**한 것
- `[해석]` = **우리 해석** — 원문의 주장이 아니다

---

# 1. 원문에 없어서 확인이 필요한 것 (공백 먼저)

이 절을 머리에 둔다. 아래 것들은 **논문이 안 준 것**이고, 없다는 사실 자체가
이 계보의 관측이다.

1. **토모그래피 3 개 셀의 전기화학 상태가 없다.** "before cycling / after 10
   cycles / after 50 cycles" 세 셀을 뜯었다고만 하고, **그 셀들의 방전 용량 곡선을
   한 번도 보여 주지 않는다.** Fig. 1(a) 는 **또 다른 셀**(재가압을 받은 셀)이고
   Fig. S1 은 **세 번째 셀**이다. → **접촉 손실 라벨(10.4 %)과 용량 관측이 같은
   셀에서 오지 않았다.** 그런데 논문 스스로 `[인쇄]` "the sudden drop in capacity
   could be found earlier or later" 라고 셀 간 산포를 인정한다.
2. **오차 막대가 단 한 그림에도 없다.** 본문·ESI 전체에서
   `error bar` 0 회 · `standard deviation` 0 회 · `uncertain*` 0 회 ·
   `replicate` 0 회. 조건당 구조 **1 개**, 셀 **1 개**. (`assb` **4/4 편 연속**이다 —
   1호만 실현 간 폭을 쟀다.)
3. **분할(segmentation) 정확도 수치가 없다.** ESI 가 Fig. S3 을 `[인쇄]` "showing
   the accuracy of different phase identification" 이라 부르지만 **혼동행렬·검증셋·
   정확도 %·분할 문턱 민감도가 전부 없다.** void 부피 9.50 %와 접촉 손실 10.4 %는
   전부 이 분할기 출력이다.
4. **면내 화소 크기(해상도 바닥)가 없다.** 슬라이스 두께 50 nm 와 `[인쇄]`
   "sub-100 nm spatial resolution" 만 있다. → 나노 규모 디본딩 틈은 보이지 않는다.
   논문이 스스로 인정한다: `[인쇄]` "in the early cycles, only very small
   microfractures occur, **undetectable by the tomography**".
   **따라서 9.50 vol% 와 10.4 % 는 바닥이 정해지지 않은 하한이다.**
5. **면적 분율 → 용량 분율 변환 모형이 없다.** 10.4 % 의 표면이 막혔을 때 겉보기
   용량이 얼마나 주는지 논문은 **모형도 계산도 하지 않는다.** 오히려 `[인쇄]` Fig.
   4(f) 로 "한쪽에 몰려 있어서 더 나쁘다" 고 **비선형**을 시사하고 끝낸다.
6. **압력 스윕이 없다.** 사이클 중 압력은 `~2 MPa` **한 점**이고, 재가압도
   `300 MPa` **한 점**이다. 압력–용량 회복 곡선이 없다.
7. **재가압 후 장기 거동이 없다.** Fig. 1(a) figure-read 로 사이클 ≈56 까지만 있고
   (재가압 후 5–6 사이클), 회복분이 얼마나 유지되는지 모른다.
8. **EIS 등가회로 적합의 신뢰구간·유일성이 없다.** `R_bulk`–(`R_HF`‖`Q_HF`)–
   (`R_MF`‖`Q_MF`)–(`R_LF`‖`Q_LF`)–`Q_T` 5 요소 적합인데 파라미터 표가 없고
   CPE 지수·용량도 없다. 그리고 논문 스스로 시간상수가 겹친다고 적는다(§12 Q4).
9. **음극(In) 형태학 관찰이 없다.** EIS 에서 가장 크게 자란 것이 음극 쪽으로
   귀속되는 LF 인데(§5) 음극은 한 번도 뜯지 않았다 — `[인쇄]` "requires further
   study of the anode morphology".
10. **`θ`·퍼콜레이션·굴곡도·공극률·OCV 라는 단어가 0 회다.**
    본문+ESI 전체에서 `percolat*` 0 · `tortuos*` 0 · `porosity` 0 ·
    `OCV` 0 · `open-circuit` 0 · `utilization` **1**(그것도 "cathode utilization 이
    나빠질 수 있다" 는 지나가는 언급). → **1·2호의 좌표계와 말이 통하지 않는다.**
    변환은 우리가 해야 한다 (§13).
11. **In 기준 전위의 안정성 논의가 없다.** `1.4–3.7 V vs In ≡ 2–4.3 V vs Li/Li⁺`
    라는 **고정 오프셋 0.6 V** 를 쓰고 그 가정을 검토하지 않는다 (§12 Q5).

---

# 2. 한 문장 요약과, 논문이 실제로 물은 것

> **물음**: 전고체전지 복합양극에서 사이클 중 생기는 **기계적 접촉 손실**이 실제로
> 용량 감쇠에 유의미한 기여를 하는가, 그리고 그것을 **3D 로 직접 보고 정량할 수**
> 있는가.
>
> **답(논문의 주장)**: 그렇다. FIB-SEM 토모그래피로 50 사이클 뒤 **void 9.50 vol%**
> 와 **양극 표면적의 10.4 % 접촉 손실**을 직접 보았고, **300 MPa 재가압으로 용량이
> 회복**되므로 기계적 열화가 원인임이 확인된다. 그리고 그 열화는 **점진적이지 않고
> 후기 사이클에 몰려서** 일어난다.

`[해석]` **우리에게 중요한 것은 이 답이 아니라, 답을 만든 세 관측이 우리 축퇴
질문에 대해 서로 다른 방향을 가리킨다는 점이다** (§13·§14).

---

# 3. 셀·재료·프로토콜 (본문 + ESI Experimental Methods)

전부 `[인쇄]`. **압력 값은 ESI 에만 있다** (본문은 300 MPa 재가압만 적는다).

| 항목 | 값 | 출처 |
|---|---|---|
| 양극 활물질 (CAM) | **LiNi₀.₅Mn₀.₃Co₀.₂O₂ (NMC532)**, `D_CAM ≈ 12 µm`, MSE Supplies | 본문 + ESI |
| 코팅 | **Li₂O–ZrO₂ (LZO) 6–8 nm**, Samsung Research Japan, Ito et al. 절차 (ref 18/ESI ref 1) | 본문 + ESI |
| 고체전해질 (SE) | **비정질 75Li₂S–25P₂S₅ (LPS)**. Li₂S(99.98 %)+P₂S₅(99 %) 볼밀 200 min (SPEX 8000M, 50 mL ZrO₂ jar) | ESI |
| 복합양극용 미세 LPS | 헵탄+디부틸에테르 습식 볼밀 **40 h** (Retsch PM200) | ESI |
| 도전재 | **CNF (carbon nanofiber)**, Samsung Research Japan | ESI |
| 복합양극 조성 | **NMC : LPS : CNF = 60 : 35 : 5 wt%** (ESI: NMC 60 mg + LPS 35 mg + CNF 5 wt%) | 본문 + ESI |
| 음극 | **In 금속** (지름 8 mm) | 본문 + ESI |
| 셀 | 자작 가압셀, PEEK 실린더 **내경 8 mm**, 스테인리스 로드 2 개 = 집전체 | ESI |
| 분리막층 | LPS **35 mg** | ESI |
| 양극 로딩 | 복합양극 **~5 mg** | ESI |
| **제작 압력** | SE 층 **~100 MPa** → 복합양극 **~300 MPa** → In 부착 **~100 MPa** | ESI |
| **★ 사이클 중 스택 압력** | **~2 MPa (스프링)** | **ESI 만** |
| 분위기 | Ar 글로브박스 (H₂O < 0.1 ppm, O₂ < 0.1 ppm), Ar jar 밀봉 | ESI |
| 전압창 | **1.4–3.7 V vs In ≡ 2–4.3 V vs Li/Li⁺** (본문) / ESI 는 **"2–3.7 V vs In"** ⚠ 모순 (§11 D1) | — |
| 프로토콜 | **CCCV 충전** (3.7 V 에서 **5 h 유지**, ESI) + CC 방전 | 본문 + ESI |
| 전류밀도 | **0.05 mA cm⁻²** | 본문 + ESI |
| 사이클러 | Bio-Logic VMP300 | ESI |
| EIS | **7 MHz – 10 mHz, 10 mV 진폭**, **방전 끝**에서 측정 | ESI |
| FIB-SEM | FEI Helios G4 dual-beam, Ga⁺, Slice and View, **슬라이스 두께 50 nm**, 시료 52° 경사 | 본문 + ESI |
| 분할 | 수동 라벨 → **Trainable Weka Segmentation (ImageJ)** 4상(NMC/LPS/carbon/void) → 전 스택 | ESI |
| 재구성·가시화 | **Dragonfly** | ESI |

`[해석]` **율의 좌표**: 0.05 mA cm⁻² · 양극 ~5 mg 중 NMC 60 wt% ≈ 3 mg · 면적
π(0.4 cm)² ≈ 0.503 cm² → 전류 ≈ 0.025 mA, 비전류 ≈ **8.4 mA g⁻¹(NMC)**.
첫 방전 용량 129 mAh g⁻¹ 대비 `[재현]` **≈ C/15**. → **저율이다.**
2호(≈0.74 C)·3호(0.25–5 C)보다 한 자릿수 낮다. 우리 3항 분해의 `η(i)` 항이
**작아야 하는 구간**이다 — 이 점이 §13 에서 결정적이다.
⚠ 이 계산은 "~5 mg" 이라는 물결표 값 위에 서 있다. 논문은 활물질 질량을
정확히 주지 않는다.

---

# 4. 결과 ①: 용량 곡선과 300 MPa 재가압 (본문 p17400, Fig. 1(a))

## 4.1 `[인쇄]` 로 적힌 것

- 첫 사이클 방전 용량 **129 mAh g⁻¹**.
- 이후 **26 사이클** 동안 **102 mAh g⁻¹** 로 완만히 감소 → `[인쇄]` "a loss rate of
  approximately **1 mA h g⁻¹ per cycle**" (Fig. 1(a) 의 노란 띠).
- **30~40 사이클 사이에 급락**, `[인쇄]` "with the cell capacity ending at **less
  than 20 mA h g⁻¹**".
- `[인쇄]` "Similar cycling behavior was consistently observed in other cells,
  although the sudden drop in capacity could be **found earlier or later**."
- **50 사이클 후 300 MPa 재가압** → 방전 용량이 **80 mAh g⁻¹ 로 회복**.
  `[인쇄]` "This result **unambiguously confirms** that mechanical degradation
  significantly contributes to capacity loss during SSB cycling."
- `[인쇄]` 80 mAh g⁻¹ 는 "an average capacity decay rate of 1 mA h g⁻¹ per cycle,
  which is **consistent with the initial decay rate** for the first 25 cycles."
- `[인쇄]` 결론: **두 개의 구별되는 열화 모드** — (i) 일정한 속도의 점진적 감쇠
  (화학적일 수 있다), (ii) 몇 사이클에 걸친 급속 감쇠 (기계적).

## 4.2 `[도표]` figure-read (Fig. 1(a)) — 본문에 없는 것

| 좌표 | figure-read |
|---|---|
| 사이클 1 | ≈130 mAh g⁻¹ |
| 사이클 ~26 | ≈102 |
| 급락 시작 | 사이클 **≈28** |
| 바닥 도달 | 사이클 **≈45**, **≈2 mAh g⁻¹** |
| 사이클 46–50 | **≈2 mAh g⁻¹ 유지** |
| 사이클 51 (재가압 직후) | **≈80** |
| 사이클 ~56 (마지막 점) | **≈64** |

★ **본문의 "less than 20 mA h g⁻¹" 는 참이지만 실제는 그 1/10 이다** (§11 D3).
`[재현]` 잔존율 = 2/129 ≈ **1.6 %** → **겉보기 용량 손실 ≈98 %.**

★ `[재현]` **재가압으로 되돌아온 몫**: (80 − 2)/129 = **60.5 %p**.
즉 **초기 용량의 약 61 %가 "물질이 없어서" 가 아니라 "닿지 않아서" 없던 것**이다.
`[해석]` 이것이 이 논문이 우리 닻 질문에 주는 **가장 큰 한 수**다 — §13.

★ `[도표]` 재가압 후 5–6 사이클 만에 80 → **≈64** 로 떨어진다 (`[재현]` 약
3 mAh g⁻¹/cycle, 초기 감쇠율의 **3 배**). **논문은 이 재감쇠를 언급하지 않는다.**

---

# 5. 결과 ②: EIS (본문 p17400, Fig. 1(b)(c)(d))

## 5.1 `[인쇄]`

- 스펙트럼이 **고·중·저 주파 3 개 반원**으로 구성된다. 등가회로로 적합.
- 첫 50 사이클 동안 **모든 주파수 영역의 저항이 증가**. **재가압(51 사이클) 후 모두
  유의하게 감소.**
- `[인쇄]` "This general trend suggests that mechanical degradation is **not limited
  to the cathode/solid electrolyte interface** but may also occur at other
  interfaces such as the **anode/solid electrolyte interface** and solid
  electrolyte grain boundaries."
- ★ `[인쇄]` "it is **not possible to precisely assign a single frequency region to
  the cathode/solid electrolyte interface** because of the **overlapping time
  constants** of different transport processes" — 다만 선행 연구(ref 7)를 들어
  **중주파(MF)가 양극/SE 계면에 가장 민감**하다고 본다.
- `R_MF`: **954 Ω → 1241 Ω** (첫 10 사이클, **+30 %**) → **3283 Ω** (50 사이클,
  **+244 %**) → 재가압 후 **2755 Ω**.
- `[인쇄]` 재가압 후에도 `R_MF` 가 초기보다 훨씬 크다 → "other factors, such as
  **chemical degradation** at the interfaces, also play a role … or **not all
  contact can be restored**".
- `[인쇄]` LZO 가 NMC 충전 전압에서 완전히 보호하지 못한다(ref 27)는 최근 인식 →
  "the observed capacity fade can be **partially attributed to the instability of
  the LZO coating**".

## 5.2 `[도표]` figure-read (Fig. 1(c)) — ★ 본문에 없는, 가장 무거운 수

Fig. 1(c) 는 `HF`(주황 ×) · `MF`(파랑 ○) · `LF`(빨강 △) 를 사이클
**1, 5, 10, 20, 50, 51** 여섯 점에 찍는다 (y 축은 4 kΩ / 38 kΩ 에서 끊긴 파단축).
등가회로 인셋: `R_bulk` – (`R_HF`‖`Q_HF`) – (`R_MF`‖`Q_MF`) – (`R_LF`‖`Q_LF`) – `Q_T`.

| 사이클 | `R_HF` | `R_MF` | **`R_LF`** |
|---|---:|---:|---:|
| 1 | ≈0.8 kΩ | ≈0.95 kΩ (인쇄 954 Ω ✅) | ≈0.7 kΩ |
| 5 | ≈0.9 | ≈0.9 | ≈0.8 |
| 10 | ≈1.4 | ≈1.24 (인쇄 1241 Ω ✅) | ≈1.1 |
| 20 | ≈2.0 | ≈1.9 | ≈1.85 |
| **50** | **≈4.7** | **≈3.3** (인쇄 3283 Ω ✅) | **≈110** |
| **51 (재가압)** | **≈2.9** | **≈2.75** (인쇄 2755 Ω ✅) | **≈39** |

> **읽기 신뢰도**: `R_MF` 세 점이 인쇄값 954/1241/3283/2755 Ω 와 **모두 맞는다**.
> 같은 축척에서 읽은 `HF`·`LF` 도 같은 신뢰도로 본다.

★★ `[재현]` 이 표에서 나오는 세 가지, **전부 본문에 없다**:

1. **50 사이클에서 셀 저항을 지배하는 것은 LF 다.**
   `R_HF + R_MF + R_LF ≈ 4.7 + 3.3 + 110 ≈ 118 kΩ` → **LF 가 93 %.**
   양극에 귀속되는 MF 는 **2.8 %**. **LF 가 MF 의 ≈33 배.**
2. **재가압이 되돌린 것도 주로 LF 다.**
   회복률 = (50사이클 − 51사이클)/(50사이클 − 1사이클):
   - `R_LF`: (110−39)/(110−0.7) = **≈65 %**
   - `R_HF`: (4.7−2.9)/(4.7−0.8) = **≈46 %**
   - `R_MF`: (3283−2755)/(3283−954) = **≈22.7 %**  ← 인쇄값으로 계산
3. ★ **용량 회복률(≈61 %p)과 가장 잘 맞는 것은 양극 MF(23 %)가 아니라 음극 LF(65 %)다.**

`[해석]` → **논문의 인과 서사(초록·결론: 양극 접촉 손실이 급락의 원인)와 자기 Fig.
1(c) 가 어긋난다.** 본문은 §5.1 의 한 문장에서 이를 인정하고도 **초록과 결론에서는
양극으로 돌린다** (§11 D8). 우리에게 이것은 단순한 흠이 아니라 **Q5·Q7 축의 경고**다:
**In 음극은 "평탄해서 안전한 기준극" 이 아니라, 이 셀에서 가장 크게 변한 계면이다.**

## 5.3 `[도표]` Nyquist (Fig. 1(b)(d))

- (b) 전체 뷰: `Re(Z)` 0–30 kΩ. 1 cyc(빨강)가 원점 근처 작은 호, 20 cyc(파랑),
  50 cyc(주황), 51 cyc(검정, 재가압)가 차례로 커진다. **50 cyc 곡선이 27 kΩ 까지
  올라가는 긴 확산 꼬리**를 보이고, 51 cyc(재가압)는 그보다 **안쪽**에 있다.
- (d) 확대 뷰(0–8 kΩ): 반원 경계에 **50 kHz**, **6 Hz** 가 점선으로 표시된다.
  `[해석]` → HF/MF 경계 ≈50 kHz, MF/LF 경계 ≈6 Hz.
  **원문 본문·캡션 어디에도 이 두 수가 글로 없다** — 그림에만 있다.

---

# 6. 방법: FIB-SEM 토모그래피 (본문 p17401, Fig. 2)

`[인쇄]` 세 개의 SSB 셀 — **cycling 전 · 10 사이클 후 · 50 사이클 후** — 을 **방전
상태에서** 꺼내 측정. 셀을 52° 기울이고 복합양극 단면을 이온빔에 수직으로 둔다.
이온빔으로 관심 영역 주위에 trench 를 판 뒤, **50 nm** 씩 깎고 매번 **BSE(후방산란
전자) 이미지**를 찍는다. **수백 회** 반복 → 정렬·크롭 → 2D 스택 → 4상 분할 → 3D.

`[인쇄]` Fig. 2 캡션: "the final 3D volumes were slightly different for the three
samples but were **all 60 × 40 × 30 µm³**". ⚠ **Fig. 3 의 실제 라벨과 어긋난다**
(§11 D4).

`[도표]` Fig. 2 에서 읽은 것:
- (b) trench 사진 2 장, **스케일바 30 µm**, "Milling direction" 화살표,
  **"Platinum protective layer"** 가 표면에 얹혀 있다 (본문에 언급 없음).
- (c) 2D 스택, **스케일바 10 µm**, `x–y–z` 축 표시.
- (d) 4상 분할 범례 — **NMC 보라 · LPS 노랑 · CNF 회색 · Void 빨강.**
  ⚠ 본문 p17401 은 `[인쇄]` "the NMC cathode (**blue**), LPS solid electrolyte
  (yellow), carbon (**black**), and void (red)" 라고 쓴다. Fig. 2(d) 범례의
  CNF 는 **회색**, NMC 는 **보라/남색**이다 — 색 서술이 느슨하다 (약한 어긋남).
- (e) 3D 재구성 1 개.
- ⚠ **면내 화소 크기가 어디에도 없다** (§1-4).

---

# 7. 결과 ③: void 의 발달 — **이 계보 최초의 `θ(N)` 시간축** (본문 p17401, Fig. 3)

## 7.1 `[인쇄]` + `[도표]` 결합

Fig. 3 은 3 행(시점) × 3 열(전 성분 / NMC 만 / void 만) 이고, **각 행 아래에
전체 부피와 void 부피분율이 라벨로 찍혀 있다**:

| 시점 | `[도표]` 재구성 부피 | `[도표]` void | `[인쇄]` 본문의 서술 |
|---|---|---:|---|
| **before cycling** | **57 × 33 × 29 µm³** | **2.87 vol%** | "voids only account for **less than 3 %**" ✅ |
| **after 10 cycles** | **66 × 41 × 31 µm³** | **3.23 vol%** | "increased by **less than 0.5 %**" ✅ (`[재현]` +0.36 %p) |
| **after 50 cycles** | **64 × 38 × 36 µm³** | **9.50 vol%** | "**more than three times** that in the pristine" ✅ (`[재현]` ×3.31) |

`[재현]` 부피: 54,549 / 83,886 / 87,552 µm³ → **pristine 이 50-사이클의 0.62 배**.
⚠ Fig. 2 캡션의 "all 60 × 40 × 30 µm³ (=72,000)" 와 맞는 것이 **하나도 없다**
(§11 D4). 그리고 **기준선(pristine)이 가장 작은 표본**이다.

★★ `[해석]` **이것이 `assb` 1·2·3 호가 한 편도 주지 않은 "시간축" 이다.**
1호는 pristine 정적 기하만, 2호는 방전 1 회, 3호는 방전 1 회 + 충전 1 회였다.
여기는 **사이클 0 / 10 / 50 의 3 점**이고, 그 축 위에서 기하량이 움직인다.
⚠ 단 **3 점이고, 각 점이 다른 셀이며, 반복이 없다.**

## 7.2 `[인쇄]` void 의 성격 변화

- pristine: void 는 SE 부피 전체에 퍼져 있으나 **작고 고립**돼 있다.
  기원은 `[인쇄]` **cold-pressing 중 SE 입자의 큰 변형** → 입자 경계의 작은 공극.
- 10 사이클: 형태 변화 없음. `[인쇄]` "the mechanical degradation … is **minimal or
  is not at the scale where it is visible or influences performance**."
- 50 사이클: `[인쇄]` void 가 **연결되어 양극 입자 근처에 10 µm 규모의 flake 모양
  균열**을 만든다.

`[도표]` Fig. 3 오른쪽 열(void 만)에서 눈으로 보이는 것: 0·10 사이클은 **먼지 같은
붉은 점 구름**, 50 사이클은 **거의 연속인 붉은 덩어리**다. 중간 열(NMC 만)에서는
50 사이클 쪽 입자 표면이 눈에 띄게 거칠어지고 입자 사이가 벌어져 보인다.
`[해석]` **10 → 50 은 양적 변화(2.87→9.50)가 아니라 위상 변화(고립 → 연결)다.**
논문도 같은 말을 하지만 **연결도를 수치로 재지 않는다** — 퍼콜레이션 분석 없음
(`percolat*` 0 회).

## 7.3 `[인쇄]` 단면 SEM (Fig. 4(a)–(c))

- (a) before, (b) 10 cycles: **작은 고립 공극만**.
- (c) 50 cycles: **양극 입자 옆에 큰 균열**(빨간 화살표 3 개).
- `[인쇄]` "This location suggests that the **repeated volume change of cathode
  particles** during cycling is likely the **main driving force** for the void
  formation."

`[도표]` Fig. 4 figure-read: **스케일바 10 µm** (a)(b)(c)(d) 공통. (a) 에도 이미
어두운 void 영역이 몇 개 보인다(2.87 vol% 와 일관). (c) 의 균열은 **NMC 입자
표면을 따라** 난 검은 띠이고, **NMC 입자 내부를 가로지르지 않는다**.

---

# 8. 결과 ④: 접촉 손실의 정량 — **10.4 %** (본문 p17402, Fig. 4(d)(e)(f))

## 8.1 정의 — `[인쇄]`

> "we divided the cathode surface into **cathode surface in contact with voids
> (contact loss)** and **cathode surface in contact with other components such as
> other cathode, solid electrolyte, or carbon (with contact)**, based on the
> segmentation shown in Fig. 3."

즉:

```
접촉 손실 =  A(NMC ∩ void) / A(NMC 전체 표면)        [무차원, 면적 분율]
```

- `[인쇄]` **"The estimated contact loss area is 10.4 % of the total cathode
  surface area."** — 50 사이클 시료에 대해서만. (0·10 사이클 값은 **없다.**)
- `[인쇄]` "Contact loss was observed at **most of the cathode particle surfaces**,
  demonstrating the severity of the mechanical problems."

⚠ `[해석]` **분자가 "void 와 닿은 면적" 이지 "이온 경로가 끊긴 면적" 이 아니다.**
분모에는 **NMC–NMC 접촉**도 "with contact" 로 들어간다 — 그런데 NMC–NMC 접촉은
Li⁺ 경로가 아니다. → **이 정의는 접촉 손실을 과소평가하는 쪽으로 치우친다.**
논문은 이 점을 언급하지 않는다.

## 8.2 `[도표]` figure-read

- **Fig. 4(d)**: Fig. 4(c) 의 같은 슬라이스 위에 NMC 표면 윤곽을 **청록색**으로
  그리고, void 와 접한 구간만 **주황/빨강**으로 덧칠했다. 눈으로 보면 주황 구간은
  전체 윤곽의 **소수 지분**이고, **특정 입자의 특정 변에 몰려 있다** (한 입자
  주위를 둘러싸지 않는다). **10.4 % 라는 전역값과 시각적으로 모순되지 않는다.**
  ⚠ 캡션은 "(d) NMC surfaces (**blue**) … highlighted in **red**" 라 하지만 실제
  윤곽은 **청록(cyan)**, 강조는 **주황**에 가깝다 (약한 어긋남).
- **Fig. 4(e)**: 3D 전체. 파란 실선 그물(접촉 유지 표면) 위에 **주황 패치**가
  흩뿌려져 있다. 캡션 `[인쇄]` 박스 크기 **64 × 38 × 36 µm³** — **Fig. 3 의
  50-사이클 부피와 정확히 같다** ✅ (일관성 확인).
- **Fig. 4(f)**: 단일 NMC 입자(회색) + 주변 void(빨강), 박스 **18 × 20 × 18 µm³**.
  ★ **눈으로 보면 붉은 영역이 보이는 입자 표면의 대략 절반 가까이를 덮는다** —
  전역 10.4 % 와 **인상이 크게 다르다.** 논문은 `[인쇄]` "a single NMC particle …
  were **isolated** from the larger volume" 이라고만 하고 **선택 기준을 밝히지
  않는다.** 대표 입자인지 극단 입자인지 알 수 없다 (§11 D13).
- `[인쇄]` "The voids are **much more concentrated on the right side** of the NMC
  particle" — `[도표]` 렌더에서 붉은 영역은 **위·앞·왼쪽에도 넓게** 있어 "한쪽" 이
  그림에서 자명하지 않다. 시점 문제일 수 있다 (§11 D14, 약한 항목).

## 8.3 `[인쇄]` 왜 "한쪽에 몰리는가" 와 그 귀결

- 몰리는 이유: "the presence of voids on **one side** of the particle is
  **sufficient to release the strain**".
- ★ 귀결: "This **concentration** of the decohered area … may **aggravate** its
  effect on capacity loss as now **all the Li ions going in and out of the area
  under the contact loss have a much larger distance to travel**".
  균일하게 흩어져 있었다면 `[인쇄]` "diffusion gradients parallel to the surface …
  would **rapidly fade out** in the cathode particle."

★★ `[해석]` **이 문단이 우리 3항 분해에 직접 들어오는 문장이다.**
논문 자신이 **"같은 면적 손실이라도 분포에 따라 용량 영향이 다르다"** 고 말한다.
즉 **면적 분율 → 용량 분율 사상이 비선형이고 분포 의존**이다.
→ `Q_apparent = θ_AM · η(i) · Q_material` 에서 **`θ` 를 스칼라로 쓰면 안 된다**는
2호의 결론(공간 `z` 의존)에 **입자 표면 상의 방향 의존**이 하나 더 붙는다.
그리고 논문은 그 사상을 **모형화하지 않는다** (§1-5).

---

# 9. 논의 (본문 p17402–17403)

`[인쇄]` 로 적힌 것들:

1. **주장**: "The FIB-SEM tomography and electrochemical testing results together
   strongly suggest that the **severe mechanical degradation is the main cause of
   the rapid capacity fade** … particularly in later cycles."
2. **한계 인정 ①(음극)**: "the observed cathode/solid electrolyte delamination is
   likely **only part** of the overall mechanical degradation… Contact loss during
   cycling is **also likely to occur at the anode side**. The **low-frequency
   region** … often attributed to the **anode/solid electrolyte interface**, sees a
   **significant increase** during cycling and **decreases after pressing**."
3. **한계 인정 ②(입자 균열)**: "although significant **cathode particle cracking is
   not observed** in the current study (Fig. 4(d)), it has often been observed in
   **liquid cells**, and could occur in SSBs with **longer cycling and larger depth
   of charge and discharge**."
4. **개선 경로 4 개** (`[인쇄]` "none of which is likely to be very easy"):
   - **양극 형태**: 입자 크기를 줄이면 표면 변위가 줄어 계면 응력이 준다.
     ⚠ 단 "reducing the cathode particle size could **negatively affect the cathode
     utilization and energy density**" (ref 26 = Shi et al. *AEM* 2020, 10, 1902881).
   - **양극 화학/구조**: 부피 변화가 작은 "**zero-strain**" 재료 탐색.
     `[인쇄]` 층상 양극의 사이클 부피 변화는 **최대 8 %** (ref 19, 20).
   - **전해질 물성**: 산화물계(더 단단함)에서는 `[인쇄]` "the **rapid development of
     cracks in the first few cycles**" 가 보고됐다 (ref 25). 폴리머 복합 전해질은
     더 큰 변형을 수용한다 (ref 32–34). → **탄성이 높은 SE 개발**.
   - **외부 압력**: "applying a **large external pressure (stack pressure)** during
     cycling could **in principle** reduce the contact loss … but such a large stack
     pressure **may not be practical for large format cells**."
5. **미해결로 남긴 것**: `[인쇄]` "the reason why the mechanical degradation and
   associated capacity fade **accelerates in the later cycles remains unclear**."
   두 가설:
   - (a) **화학 열화가 기계 열화와 공모**한다 — 계면 반응층이 자라 기계적 접착을
     약화시키거나 잔류응력을 더한다.
   - (b) **초기의 아주 작은 미세균열**이 토모그래피로 **검출되지 않다가** 나중에
     합체해 큰 디코히전으로 간다 ("not uncommon for **ductile fracture**").

`[해석]` ★ **(b) 는 논문이 스스로 자기 측정의 검출 한계를 인정한 문장이다.**
그런데 같은 논문의 §7.2 는 10 사이클에서 `[인쇄]` "mechanical degradation … is
**minimal**" 이라고 **단정**한다. 두 문장은 같이 설 수 없다 — (b) 가 맞으면
10 사이클의 "minimal" 은 **"안 보였다"** 이지 **"작았다"** 가 아니다 (§11 D12).

---

# 10. 결론 (본문 p17403) — `[인쇄]` 전문 요지

- 50 사이클 후 복합양극에 **큰 void 부피(9.50 %)**.
- void 는 주로 **양극 입자 표면 근처**에 분포 → **10 % 이상의 접촉 면적 손실**.
- `[인쇄]` "The observed rapid capacity drop in later cycles is **attributed to this
  mechanical contact loss**."
- ★ `[인쇄]` "Our results also suggest, **somewhat surprisingly**, that mechanical
  degradation **does not progress gradually** starting from the first cycle.
  Instead, the majority of the void formation and contact loss **likely occurs at
  later cycles and over a short period**."

`[해석]` 마지막 항이 우리에게 가장 쓸모 있다: **접촉 손실의 시간 프로파일이
단조 완만이 아니라 계단(문턱)이다.** 열화 모드 추정에서 `θ(N)` 을 부드러운
함수로 매개화하면 **이 구조를 원리적으로 못 맞춘다.**

---

# 11. ⚠ 어긋남 원장 (본문 ↔ 그림 ↔ 초록 ↔ ESI)

`assb` 1호 8 건 · 2호 14 건 · 3호 18 건에 이어 **4호 18 건**.
**무거운 것(결론을 떠받치는 문장이 자기 그림/자기 데이터와 충돌)은 D8·D9·D10·D12.**

| # | 무게 | 내용 |
|---|:--:|---|
| **D1** | 중 | **전압창이 본문과 ESI 에서 다르다.** 본문 `[인쇄]` "cycled between **1.4** and 3.7 V vs. In (between 2 and 4.3 V vs. Li/Li⁺)" ↔ ESI `[인쇄]` "the cycling voltage window was **2–3.7 V vs. In**". `[도표]` Fig. S1(b)(c) 의 방전 종점이 **≈1.4 V** 이므로 **본문이 맞고 ESI 가 틀렸다.** (ESI 가 vs-Li 하한 2.0 을 vs-In 칸에 옮겨 적은 것으로 보인다.) |
| **D2** | 중 | **패널 지시가 뒤바뀌었다.** 본문 `[인쇄]` "Fig. 1(b) and (c) present the EIS measurements … summarized in Fig. **1(d)**" ↔ Fig. 1 캡션과 실제 그림은 **(b),(d) = Nyquist, (c) = 저항 요약**. **본문이 (c)/(d) 를 바꿔 썼다.** |
| **D3** | 중 | **급락 후 값이 10 배 부풀려 서술됐다.** 본문 `[인쇄]` "ending at **less than 20 mA h g⁻¹**" ↔ `[도표]` Fig. 1(a) 사이클 46–50 은 **≈2 mAh g⁻¹**. 참이지만 실제의 10 배 여유를 둔 표현이고, 이 차이가 D9 의 정량 대조를 흐린다. |
| **D4** | 중 | **재구성 부피가 "slightly different" 가 아니다.** Fig. 2 캡션 `[인쇄]` "were **all 60 × 40 × 30 µm³**" ↔ `[도표]` Fig. 3 라벨 **57×33×29 / 66×41×31 / 64×38×36**. `[재현]` 54,549 / 83,886 / 87,552 µm³ — **pristine 이 50-사이클의 0.62 배**이고 캡션 값(72,000)과 맞는 것이 하나도 없다. **기준선 표본이 가장 작다.** |
| **D5** | 경 | 캡션 `[인쇄]` "Fig. 1 … (b) and (d) EIS measurement after **1, 20, 50, and 51** cycles" ↔ `[도표]` Fig. 1(c) 에는 **1, 5, 10, 20, 50, 51** 여섯 점이 있다. 캡션의 목록이 (b)/(d) 전용인데 (c) 설명과 한 문장에 붙어 있어 오해를 부른다 (본문의 "first 10 cycles" 서술은 (c) 의 10 사이클 점에 근거해 성립한다). |
| **D6** | 경 | 본문 `[인쇄]` "significant cathode particle cracking is not observed … (**Fig. 4(d)**)" — Fig. 4(d) 는 **접촉 손실 라벨링 패널**이다. 입자 균열 유무는 (a)–(c) 의 원 BSE 에서 판정해야 한다. 패널 지시 오류. |
| **D7** | 경 | 감쇠 구간 서술이 세 번 다르다: `[인쇄]` "over the next **26** cycles" / "the first **25** cycles" / 노란 띠는 `[도표]` **사이클 1–28** 을 덮는다. |
| **D8** | **★상** | **초록·결론의 인과가 자기 Fig. 1(c) 와 충돌한다.** 초록 `[인쇄]` "mechanical contact loss between the solid conductor and cathode … **plays a significant role** in the observed capacity fade", 결론 `[인쇄]` "The observed rapid capacity drop … is **attributed to this mechanical contact loss**" ↔ `[도표]` Fig. 1(c) 50 사이클에서 **`R_LF` ≈110 kΩ 가 전체 저항의 ≈93 %** 이고 양극에 귀속되는 `R_MF` 는 **≈3.3 kΩ (2.8 %)** — **33 배 차이**. 본문은 한 문단(§9-2)에서 음극 기여를 인정하고도 초록·결론은 양극으로 돌린다. ★ **2·3호와 같은 형태다.** |
| **D9** | **★상** | **두 핵심 수를 나란히 놓고 한 번도 비교하지 않는다.** 접촉 손실 **면적 10.4 %** ↔ 재가압으로 되돌아온 용량 `[재현]` **≈60.5 %p** (2 → 80 mAh g⁻¹, 129 기준). **비 ≈ 5.8 배.** "10 % 접촉이 끊겨서 60 % 용량이 날아갔다" 는 주장이 되려면 **면적→용량 증폭 기구**가 필요한데 논문은 §8.3 의 정성 논의만 하고 계산하지 않는다. |
| **D10** | **★상** | **라벨과 관측이 서로 다른 셀에서 온다.** 토모그래피 3 셀의 **용량이 한 번도 보고되지 않는다.** Fig. 1(a) 는 재가압 셀, Fig. S1 은 또 다른 셀. 그런데 `[인쇄]` "the sudden drop … could be found **earlier or later**" 로 **셀 간 산포를 스스로 인정**한다. → "50 사이클 시료의 10.4 %" 와 "50 사이클에 ≈2 mAh g⁻¹" 를 같은 문장에 쓸 근거가 논문 안에 없다. |
| **D11** | 중 | **분할 정확도가 수치로 없다.** ESI `[인쇄]` Fig. S3(b) 를 "showing the **accuracy** of different phase identification" 이라 부르지만 혼동행렬·검증셋·정확도 %가 없다. 그리고 `[도표]` **Fig. S2(a) 에서 CNF 와 LPS 의 회색도 분포가 크게 겹치고, void 의 꼬리가 CNF 영역까지 들어간다.** ESI 스스로 `[인쇄]` "image segmentation using grayscale value only … lead **some incorrect phase identification** … especially within the **boundaries** of different components due to the **edge effect**" 라고 적는다 — **접촉 손실은 정확히 그 "경계" 에서 재는 양이다.** |
| **D12** | **★상** | **검출 한계가 두 문장 사이에서 뒤집힌다.** §7.2 `[인쇄]` 10 사이클에서 "the mechanical degradation … is **minimal** or is not at the scale where it is visible" ↔ §9-5(b) `[인쇄]` "in the early cycles, only **very small microfractures** occur, **undetectable by the tomography**". 후자가 맞으면 **"작았다" 가 아니라 "안 보였다"** 이고, 그러면 **"열화가 후기에 몰린다" 는 결론(§10 의 'somewhat surprisingly')의 근거가 사라진다.** 논문은 둘을 화해시키지 않는다. |
| **D13** | 중 | **Fig. 4(f) 단일 입자의 선택 기준이 없다.** `[인쇄]` "a single NMC particle … were isolated" 뿐. `[도표]` 그 입자는 보이는 표면의 **절반 가까이가 붉다** — 전역 10.4 % 와 인상이 어긋난다. 대표/극단 여부를 알 수 없다. |
| **D14** | 경 | `[인쇄]` "voids are much more concentrated on the **right side**" ↔ `[도표]` Fig. 4(f) 에서 붉은 영역은 위·앞·왼쪽에도 넓다. 렌더 시점 문제일 수 있으나 그림만으로는 "한쪽" 이 확인되지 않는다. |
| **D15** | 경 | 색 서술이 그림 범례와 다르다. 본문 `[인쇄]` "carbon (**black**)" ↔ Fig. 2(d) 범례 **CNF = 회색**. Fig. 4(d) 캡션 "NMC surfaces (**blue**) … highlighted in **red**" ↔ `[도표]` 실제는 **청록 윤곽 + 주황 강조**. |
| **D16** | 경 | **압력 이력이 전부 ESI 에만 있다.** 본문은 제작 압력(100/300/100 MPa)도, **사이클 중 스택 압력 ~2 MPa** 도 언급하지 않는다. 초록의 "large external pressure" 가 **300 MPa** 라는 것은 Fig. 1 캡션에서야 드러난다. 역학이 주제인 논문에서 **상태변수를 본문 밖에 둔 것**이다. |
| **D17** | 경 | **재가압 후 재감쇠를 언급하지 않는다.** `[도표]` Fig. 1(a) 는 51→≈56 사이클에서 80 → **≈64** (`[재현]` ≈3 mAh g⁻¹/cycle, 초기 감쇠율의 3 배). 본문·결론 모두 침묵. |
| **D18** | 경 | 단위 오식 2 건: 본문 `[인쇄]` "a rate of 0.05 mA **cm2**" (cm⁻²), Fig. 3·4 캡션의 `mm³`/`mm` 는 PDF 텍스트 추출상 µ 가 소실된 것이고 `[도표]` 그림에는 **µm** 로 찍혀 있다 (이건 추출 아티팩트 — 원문 결함 아님). |

---

# 12. ★ Q1~Q8 (닻 `questions/assb-contact-loss-vs-lampe.md` 의 수집 지침)

## Q1 — 접촉 손실을 어떻게 정량했나 (단위·측정법·모델 형태)

★★ **있다. 그리고 `assb` 계보에서 처음으로 `θ` 와 같은 종류의 무차원 분율이다.**
두 개의 양을 준다:

| 양 | 정의 | 단위 | 값 | 시점 |
|---|---|---|---|---|
| **void 부피분율** | void 복셀 / 재구성 전체 부피 | 무차원 vol% | **2.87 / 3.23 / 9.50** | **0 / 10 / 50 사이클** |
| **접촉 손실 면적분율** | `A(NMC ∩ void) / A(NMC 전체)` | 무차원 % | **10.4** | **50 사이클만** |

측정법: **FIB-SEM 직렬절삭 토모그래피(50 nm 슬라이스) + Weka ML 4상 분할**.
모델 형태: **없다** — 이 양을 용량으로 옮기는 식이 논문에 없다.

⚠ **1호의 `θ` 와 같은 양이 아니다.** 변환이 안 되는 이유:

| | **1호·2호 (`θ` / Connectivity)** | **4호 (Shi 2020)** |
|---|---|---|
| 차원 | **부피** 분율 (퍼콜레이팅 클러스터에 속한 AM 부피 / AM 전체 부피) | **면적** 분율 (void 와 닿은 NMC 표면 / NMC 전체 표면) |
| 판정 | **Hoshen–Kopelman 퍼콜레이션** — 집전체/분리막까지 **경로가 이어지는가** | **국소 인접** — 이 픽셀이 void 에 닿았는가. **경로 판정 없음** (`percolat*` 0 회) |
| 분모 | AM 전체 부피 | NMC 전체 **표면적** — **NMC–NMC 접촉도 "with contact" 로 센다** (Li⁺ 경로가 아닌데) |
| 시간축 | 없음 (정적) | **있다 (0/10/50 사이클)** — void 쪽만 |

`[해석]` **면적 → 부피 변환에는 "표면의 몇 %가 막히면 입자의 몇 %가 못 쓰이나" 라는
모형이 필요하고, 그 모형이 논문에 없다.** 그리고 논문 자신이 §8.3 에서 그 사상이
**분포 의존(비선형)** 이라고 말한다. → **3호(응력, GPa)처럼 "차원이 달라 변환 불가"
는 아니지만, "같은 무차원인데 사상이 미정" 이다.** 이것이 4호의 자리다.

## Q2 — ★★ 접촉 손실과 LAM 을 가르는 독립 관측을 썼나

**★★ 있다. `assb` 3/3 편 연속 0 이던 칸이 4호에서 깨진다.**
그것도 **세 겹**이고, 그중 하나는 이 계보 최초의 **개입(intervention)** 이다:

| # | 관측 | 무엇을 재나 | 층위 |
|---|---|---|---|
| (a) | **FIB-SEM 토모그래피** (3 셀 × 1 구조, 0/10/50 사이클) | 기하 — void vol%, 접촉 손실 면적% | **measured (ex situ) → ML 분할** |
| (b) | **EIS** (7 MHz–10 mHz, 사이클 1/5/10/20/50/51) | 계면 저항 3 성분 | **measured → 등가회로 fitted** |
| (c) | ★ **300 MPa 재가압 개입** (50 사이클 후) | **가역/비가역 분할** | **measured (직접)** |

★★ **(c) 가 이 계보 최초로 "접촉 손실만 되돌리는 조작" 이다.**
논리: **진짜 활물질 손실(rock-salt 화, 구조 붕괴)은 압력으로 돌아오지 않는다.
닿지 않던 활물질은 돌아온다.** 따라서

```
압력으로 회복된 용량 ≤ (그 시점 접촉 손실의 용량 등가)
```

가 **하한이 아니라 상한**을 준다 (완전 회복이 아닐 수 있으므로 등호는 안 선다).
`[재현]` 이 셀에서: **≈60.5 %p 가 압력으로 돌아왔다** → 사이클 50 시점의
겉보기 용량 손실 ≈98 % 중 **최소 60 %p 가 `LAM_PE` 가 아니다.**

⚠ **세 겹 모두에 붙는 경고**: (a)는 (b)(c)와 **다른 셀**이다(D10). (b)의 시간상수는
논문 스스로 겹친다고 적는다. (c)의 회복은 `[도표]` **음극 쪽 LF 저항**에서 가장
크게 나타난다(§5.2) — **양극 전용 조작이 아니다.**

## Q3 — 라벨 출처 층위 · 오차 막대

**세 층이 섞여 있다**:
- **measured (전기화학)**: 용량·전압곡선. 오차 막대 없음, 셀 1 개(+ESI 1 개).
- **measured → ML 분할 (기하)**: void %·접촉 손실 %. **★ 새 층위다** —
  3호의 "**fitted 문턱**"(타 화학 실험 분포에 적합한 12 % 소성전단)과도 다르고,
  1·2호의 "computed-geometric"(순수 시뮬레이션)과도 다르다.
  여기는 **실측 영상**이되 **학습된 분류기가 문턱 역할**을 하고 그 정확도가 없다.
  → 이 위키 표기로 **`measured-but-ML-thresholded`**.
- **fitted (EIS 등가회로)**: `R_HF/R_MF/R_LF`. 파라미터 표·신뢰구간 없음.

**오차 막대: 0 개.** `error bar` · `standard deviation` · `uncertain*` · `replicate`
· `seed` **전부 0 회** (본문+ESI). → **`assb` 4/4 편 연속.** 1호만 실현 간 폭을 쟀다.

## Q4 — 유일성·식별성을 쟀나

**없다. `assb` 4/4 편 0.**
★ **그러나 4호는 "안 쟀다" 가 아니라 "축퇴를 인쇄로 인정하고 그대로 썼다" 는
새로운 형태다**:

> `[인쇄]` "it is **not possible to precisely assign a single frequency region to
> the cathode/solid electrolyte interface** because of the **overlapping time
> constants** of different transport processes"

그러고도 `R_MF` 를 **양극/SE 계면의 대리**로 쓰고 그 수(954 → 3283 → 2755 Ω)를
서사의 기둥으로 삼는다. `identifiab*` 0 회 · 조건수 0 · 프로파일 0 ·
등가회로 대안 모형 비교 0.

`[해석]` **이것은 우리 질문의 EIS 판이다** — 3 개 RC 의 시간상수가 겹칠 때
`R_MF` 를 점추정으로 보고할 수 있는가. 액체셀 계열에서 우리가 "LAM 분할은 폭과 함께
보고해야 한다" 고 한 것과 **정확히 같은 형식의 요구**가 여기에 걸린다.

## Q5 — Li-In 기준 전위 이동을 다뤘나

**부분 — 그리고 채워지면서 동시에 문제로 드러난 칸이다.**

- ★ **이 계보 최초로 In 금속 음극이 실제로 쓰였다** (1호 없음 · 2호 Li 금속 이상접촉 ·
  3호 음극 모델링 자체 없음).
- `[인쇄]` "cycled between **1.4 and 3.7 V vs. In (between 2 and 4.3 V vs. Li/Li⁺**)"
  → `[재현]` **고정 오프셋 0.6 V 를 암묵 가정**한다 (In/LiIn 2상 공존 평탄역).
- **그 가정의 타당성·이동 가능성을 한 번도 논의하지 않는다.** `indium` 0 회
  (`In metal` 만 3 회), In 음극의 조성·과잉 In 량·2상 영역 이탈 여부 **전부 없다**.
- ⚠ **그런데 같은 논문의 EIS 에서 가장 크게 자란 것이 음극 쪽 LF 다**
  (`[도표]` ≈0.7 → ≈110 kΩ, **≈157 배**). → **기준극이 크게 변하는데 기준 전위는
  불변으로 놓는다.**

`[해석]` 닻의 미결 항목 2("Li-In 기준 전위가 얼마나 안정한가")에 대해
4호가 주는 것은 **답이 아니라 경고**다: 실험 논문이 그 축을 **가정으로 지우고
있다**는 실물 사례. 완전지 OCV 를 양극 곡선으로 읽는 우리 계획이 딛는 바로 그 가정이다.

## Q6 — ★★ 압력을 통제·보고했나

**★★ 있다. `assb` 3/3 편이 `pressure` 0 회였던 칸이 4호에서 깨진다.**
그리고 **세 가지 역할로** 쓴다:

| 역할 | 값 | 어디에 |
|---|---|---|
| **제작 변수** | SE 층 ~100 MPa → 복합양극 **~300 MPa** → In 부착 ~100 MPa | **ESI 만** |
| **사이클 중 경계조건 (스택 압력)** | **~2 MPa, 스프링** | **ESI 만** |
| ★ **개입 변수** | 50 사이클 후 **300 MPa 재가압** | 본문 + Fig. 1 캡션 |

낱말 빈도: 본문 `pressur*` **9** · `MPa` 3, ESI `pressur*` **5** · `MPa` 5.
`[인쇄]` 개선 경로에서 스택 압력을 정면으로 다룬다: "could **in principle** reduce
the contact loss … but such a large stack pressure **may not be practical for large
format cells**."

⚠ **한계**: **압력 스윕이 없다.** 사이클 압력 1 점(2 MPa), 재가압 1 점(300 MPa).
압력–회복 곡선도, 재가압 반복도, 다른 압력에서의 대조군도 없다.
`[해석]` **2 MPa 는 낮은 편이다** — 이 셀의 급락이 저압 조건의 산물일 가능성을
논문이 검토하지 않는다 (닻의 후속 후보 Shin 2023 이 겨냥하는 축이 바로 이것).

## Q7 — 무음극이면 dead Li 와 SEI Li 를 갈랐나

**없다 — 해당 없음 + 공백.** 음극이 **In 금속**이라 dead Li/SEI Li 축이 성립하지
않는다. 그러나 **음극 형태학을 한 번도 보지 않았다**: `[인쇄]` "requires further
study of the **anode morphology**". `assb` **4/4 편 0.**

## Q8 — 양극 화학과 OCP 기울기

**★★ 있다. 그리고 이 계보 최초의 "실측 · 사이클별" 전압곡선이다.**
(3호의 OCV 는 **액체 반쪽전지 GITT**(타 논문)에서 온 입력 곡선이었다.)

- **화학**: **NMC532** (LiNi₀.₅Mn₀.₃Co₀.₂O₂), `D ≈ 12 µm`, **LZO 6–8 nm 코팅** /
  **비정질 LPS (75Li₂S–25P₂S₅)** / CNF, **60:35:5 wt%**, 음극 **In**.
- **OCP 기울기**: `[도표]` Fig. S1(b)(c) 의 방전 곡선은 **전 구간 기울기가 있다** —
  평탄역 없음. `[해석]` → LFP 형 `(X1, X3)` 축퇴는 여기서 **오지 않는다**
  (닻 미결 항목 5 의 "NMC 면 기울기가 있다" 쪽).
- ⚠ **엄밀히 OCV 가 아니다**: CC 방전 곡선(0.05 mA cm⁻², ≈C/15)이고 GITT·이완이
  없다. `OCV`·`open-circuit` 0 회.

### `[도표]` Fig. S1(b) — 사이클 5 / 25 / 34 (별도 셀)

| | 방전 용량 | **방전 시작 전압(Q≈0)** | 충전 시작 전압(Q≈0) |
|---|---:|---:|---:|
| 사이클 **5** | ≈122 mAh g⁻¹ | **≈3.65 V** | ≈3.10 V |
| 사이클 **25** | ≈112 | **≈3.50 V** | ≈3.20 V |
| 사이클 **34** | ≈102 | **≈3.35 V** | ≈3.30 V |

★ `[해석]` **용량 축이 줄어드는 동시에 전압 축이 내려간다.**
`[재현]` 29 사이클에 방전 시작점 **≈−300 mV**, 충전 시작점 **≈+200 mV**
(= 이력 확대 ≈500 mV). **이것은 아핀 용량축 스케일링(`a_PE`)이 아니다** —
2호 Fig. S5(입계 저항만 바꿔도 시작 전압 −175 mV)에서 본 것과 **같은 형태가
실측에서 재현됐다.**

### `[도표]` Fig. S1(c) — 급락을 관통하는 사이클 34/37/38/39/40

| 사이클 | 방전 용량 | 방전 시작 전압 |
|---|---:|---:|
| 34 | ≈103 | ≈3.35 V |
| 37 | ≈99 | ≈3.45 V |
| 38 | ≈91 | ≈3.45 V |
| 39 | ≈83 | ≈3.50 V |
| **40** | **≈43** | **≈2.98 V** |

★★ `[도표]` **사이클 40 에서 방전 시작 전압이 한 번에 ≈500 mV 떨어지고 용량이
반으로 준다.** 34→39 는 오히려 시작 전압이 조금 올라간다(≈3.35→3.50) —
**단조가 아니다.** 논문은 이 비단조성을 언급하지 않는다.

### ★★ `[도표]` Fig. S1(c) 인셋 — **전압 비단조 진동**

확대 상자(≈3.3–3.75 V, 충전 곡선 상부)에서 **사이클 38(회색)·39(빨강)의 충전
전압이 위아래로 흔들린다** — 단조 상승이 아니라 **톱니**다. ESI 캡션 `[인쇄]`:

> "the voltage curve becomes **unstable** during these cycles, **jumping up and
> down** instead of smoothly increasing or decreasing … This unstable voltage
> behavior can be explained by the **intermittent Li transport to and from the
> contracting/expanding cathode particles**."

★★ `[해석]` **이것이 접촉 손실의 "전압 서명" 후보다.** 곡선 모양(용량축·전압축)이
아니라 **곡선의 국소 비단조성**이 관측량이다. OCP 적합에서는 **잔차의 고주파 성분**
으로 나타나고, 보통은 노이즈로 버려진다. 액체셀에서는 이런 서명이 없다 —
전해질이 항상 젖어 있기 때문. → **`assb` 전용 판별 feature 후보.**
⚠ 단 **크기가 수치로 보고되지 않았고**(figure-read 로 대략 ±50–100 mV 대역),
이 셀 하나의 5 사이클 구간에서만 보였다.

### `[도표]` Fig. S1(a) — 두 번째 셀의 붕괴 양상

130 → ≈100 (사이클 37) → **사이클 39→40 에 한 번에 ≈84 → ≈43** → 이후 완만히
≈27 (사이클 53). ⚠ **Fig. 1(a) 셀(≈2 까지 바닥)과 시간 구조가 다르다** —
한쪽은 **계단 하나 뒤 안정**, 다른 쪽은 **바닥까지 붕괴**.
논문은 `[인쇄]` "earlier or later" 로만 처리한다 (§11 D10).

## Q1~Q8 요약 (4호 행)

| Q | 4호 판정 |
|---|---|
| Q1 | **있다(무차원 분율)** — void 2.87/3.23/**9.50 vol%** (0/10/50 사이클) + 접촉 손실 **면적 10.4 %**. ⚠ `θ` 와 **차원이 같지 않다**(면적 vs 부피) + **퍼콜레이션 판정 없음** + 면적→용량 사상 **없음** |
| Q2 | **★★ 있다 — 3/3 편 연속 0 을 깬다.** FIB-SEM 토모 + EIS + **300 MPa 재가압 개입** |
| Q3 | **measured-but-ML-thresholded** (새 층위) + fitted(EIS). **오차막대 0 · 조건당 셀 1 · 분할 정확도 0** |
| Q4 | **없다 (4/4 편 0).** ★ 단 **시간상수 겹침을 인쇄로 인정하고도 `R_MF` 를 점추정으로 쓴다** |
| Q5 | **부분 — 계보 최초 In 음극.** 오프셋 **0.6 V 고정 가정**, 안정성 논의 0. ⚠ 그런데 **LF(음극) 저항이 ≈157 배** 자란다 |
| Q6 | **★★ 있다 — 3/3 편 0 을 깬다.** 제작 100/300/100 MPa · **사이클 ~2 MPa 스프링** · **재가압 300 MPa**. ⚠ 스윕 없음, 전부 ESI |
| Q7 | **없다 (4/4 편 0)** — In 음극이라 해당 없음. 음극 형태학 미관찰 |
| Q8 | **★★ 있다 — 계보 최초 실측 사이클별 V–Q.** NMC532+LZO/LPS/CNF, 전 구간 기울기, 방전 시작 전압 29 사이클에 **−300 mV**, 사이클 40 에 **−500 mV 계단**, **충전 전압 비단조 진동** |

---

# 13. ★ 우리 계보에 붙는 것 — 3항 분해와의 정면 대조

닻이 세운 좌표: `Q_apparent = θ_AM · η(i) · Q_material`.
4호의 수들을 그 위에 얹으면 **처음으로 세 항이 동시에 관측된다.** 그리고
**셋이 서로 맞지 않는다.**

## 13.1 세 관측이 주는 세 개의 숫자

| 항 | 4호가 주는 관측 | 값 (사이클 50) |
|---|---|---|
| `θ_AM` 쪽 (기하) | 접촉 손실 **면적** 분율 | **10.4 %** |
| `η(i)` 쪽 (동역학) | `R_MF` 증가 | 954 → **3283 Ω** (+244 %) |
| `Q_material` 쪽 (재료) | — | **재지 않았다** (XRD·rock-salt 분석 없음) |
| **겉보기** | 용량 잔존 | `[도표]` **≈2/129 ≈ 1.6 %** |
| **가역분** | 300 MPa 재가압 회복 | `[재현]` **+60.5 %p** |

## 13.2 ★ 가장 무거운 한 줄: **10.4 % 가 60 %p 를 설명해야 한다**

`[해석]` 접촉 손실이 **곱셈 인자**라면 `θ_AM` 이 0.896 이 되고 용량은 **10 %** 만
줄어야 한다. 실제로 압력으로 돌아온 몫은 **60 %p** 다. **≈6 배 어긋난다.**
가능한 설명 셋 (논문은 **아무 것도 검증하지 않는다**):

1. **면적 ≠ 부피.** 표면의 10.4 % 가 막혀도 그 입자 **전체**가 못 쓰일 수 있다
   (한쪽에 몰리면 확산 거리가 급증 — §8.3 이 정확히 이 말을 한다).
   → **`θ` 는 면적에 대해 선형이 아니다. 문턱 함수에 가깝다.**
2. **관측이 다른 셀에서 왔다** (D10). 토모그래피 셀의 실제 용량 손실이 60 %p 가
   아니었을 수 있다.
3. **회복분이 양극이 아니다.** `[도표]` 회복은 **LF(음극)에서 65 %**, MF(양극)에서
   **23 %** 다 (§5.2). → 60 %p 중 상당 부분이 **음극 접촉 회복**일 수 있다.

★★ **셋 중 어느 것이 맞든 결론은 하나다: "접촉 손실 면적분율" 을 그대로
`θ_AM` 자리에 넣으면 안 된다.** 우리가 DEM 산출을 라벨로 쓰려는 계획에
**직접 걸리는 제약**이다 — DEM 이 주는 것도 대개 **접촉 수/면적**이지 퍼콜레이션
부피분율이 아니다.

## 13.3 `η(i)` 항이 이 논문에서 작아야 한다는 것

`[재현]` 율 ≈ **C/15** (§3). 2호의 결론(`i→0` 에서 `η→1`)과 3호의 율 스윕
(0.25 C 에서 전 크기 ≈0.95–0.99)을 그대로 적용하면, **이 셀의 `η` 는 1 에 가까워야
한다.** 그런데 겉보기 용량이 98 % 날아갔다.

`[해석]` → **저율에서도 살아남는 손실**이므로 `η(i)` 로 설명되지 않는다.
남는 것은 `θ_AM` 과 `Q_material` 이고, **압력으로 60 %p 가 돌아왔으므로 그중
최소 60 %p 는 `θ_AM` 쪽이다.** ★ **이것이 2호의 "율 스윕 분리 시험" 을 실험에서
간접 검증한 첫 사례다** — 율을 낮췄더니 동역학 성분이 아니라 **기하 성분만
남았다.** ⚠ 단 이 논문은 율 스윕을 하지 않았으므로 **직접 증명이 아니다.**

## 13.4 압력이 **새로운 분리 연산자**다

`[해석]` 닻의 미결 항목 1 은 "접촉 손실을 모델에 어떤 형태로 넣나" 였고
1호가 **형태**(곱), 2호가 **셋째 항**, 3호가 **구동력**을 줬다.
4호가 주는 것은 **연산자**다:

```
Q(i, P_high) − Q(i, P_low)   =   기하 접촉 손실의 (상한) 용량 등가
Q(i, P_high)                 →   θ_AM ≈ 1 로 되돌린 상태의 용량
```

율 스윕이 `η` 를 지우듯, **압력 재인가가 `θ_AM` 을 (부분적으로) 되돌린다.**
둘을 합치면 세 항이 **원리적으로** 분리된다:

| 조작 | 지우는 항 | 출처 |
|---|---|---|
| `i → 0` (저율) | **`η(i) → 1`** | 2호(추론) · 3호(율 스윕 20 곡선) |
| **`P ↑` (재가압)** | **`θ_AM → ~1`** | **4호 (본 논문)** |
| 둘 다 하고 남는 것 | **`Q_material`** = 진짜 `LAM_PE` | — |

★★ **이것이 4호가 이 위키에 넣는 가장 큰 한 수다.** 그리고 이 조작은
**OCV 적합이 못 하는 일을 실험이 해 준다** — 닻 질문("OCV 적합이 가를 수 있는가")의
답이 "못 가른다" 여도, **압력 축을 붙이면 가를 수 있다**는 경로가 열린다.

⚠ **이 연산자에 붙는 4 개의 경고** (전부 4호 자신이 준다):
1. **완전 회복이 아니다** — `R_MF` 는 23 % 만 돌아왔다. → 상한이지 등호가 아니다.
2. **양극 전용이 아니다** — 회복의 대부분이 LF(음극)다. 셀 수준 조작이다.
3. **비가역 부작용이 있을 수 있다** — 300 MPa 는 셀을 다시 누르는 것이고,
   `[도표]` 재가압 후 감쇠율이 3 배로 빨라진다(D17).
4. **압력–회복 곡선이 없다** — 1 점뿐이라 "얼마나 눌러야 얼마나 돌아오나" 를 모른다.

## 13.5 `θ(N)` 의 모양: 부드럽지 않다

★ `[인쇄]` 결론: "mechanical degradation **does not progress gradually** … the
majority of the void formation and contact loss **likely occurs at later cycles and
over a short period**."
`[도표]` 뒷받침: void 2.87 → 3.23 (10 사이클, +0.36) → 9.50 (50 사이클, +6.27).
용량: 완만 → 사이클 ≈28–45 에 붕괴.

`[해석]` → **`θ_AM(N)` 을 부드러운 감소 함수(지수·멱)로 매개화하면 이 구조를
원리적으로 못 맞춘다.** 문턱/계단 형태가 필요하다.
⚠ **그리고 그 결론 자체가 D12 에 걸려 있다** — 논문이 뒤에서 "초기 미세균열은
토모그래피로 검출 불가" 라고 적으므로, "후기에 몰린다" 는 **관측의 성질일 수 있다.**
→ **우리가 이 논문에 싸게 공급할 수 있는 것**: 같은 자료에 **검출 한계를 넣은
전방 모형**을 세워 "계단" 이 실재인지 검출 아티팩트인지 가르기.

## 13.6 우리가 이 논문에 공급할 수 있는 것 (식별 가능성 경계)

1. **`R_MF` 의 근최적 폭.** 논문이 스스로 시간상수가 겹친다고 적었다. 3 개 RC
   등가회로에서 `R_MF` 의 **프로파일 우도/근최적 집합 폭**을 재면 954 → 3283 Ω 의
   **244 % 증가가 유의한지** 판정할 수 있다. 우리 폭 측정기
   (`concepts/near-optimal-set-width-measurement.md`)는 화학 무관하다.
2. **셀 간 폭.** 논문이 셀 3 개 + 2 개(Fig. 1a, S1a)를 쓰고도 산포를 안 쟀다.
   급락 사이클이 셀마다 다르다는 것은 **`θ(N)` 이 확률변수**라는 뜻이다.
3. **면적 → 용량 사상.** 10.4 % ↔ 60 %p 의 6 배 간극을 메울 모형이 없다.
   DEM/입자 스케일 확산 모형이 정확히 그 자리다.
4. **검출 한계를 넣은 전방 모형** (§13.5).

---

# 14. 이 digest 가 주장하지 않는 것 (모집단 경고)

- **이 수치들을 인용 근거로 쓰지 않는다.** 정본은 원문 PDF 다. 이 문서의 값은
  **사본**이고 `[도표]`·`[재현]`·`[해석]` 은 원문에 없다.
- **모집단**: **NMC532(LZO 6–8 nm 코팅, D≈12 µm) + 비정질 LPS(75Li₂S–25P₂S₅) +
  CNF, 60:35:5 wt% · In 금속 음극 · 8 mm 펠릿 · 제작 300 MPa · 사이클 스택 압력
  ~2 MPa · 1.4–3.7 V vs In · CCCV, 0.05 mA cm⁻² (`[재현]` ≈C/15) · 50 사이클 ·
  셀 1 개(전기화학) + 3 개(토모그래피) · 반복 0.**
  다른 화학·다른 압력·다른 율로 옮길 근거가 논문 안에 없다.
- **"10.4 % 접촉 손실이 60 %p 용량 손실을 일으킨다" 고 논문이 말하지 않는다.**
  두 수를 비교한 것은 **우리다**(§13.2). 논문은 정성적으로만 잇는다.
- **`θ_AM` 을 쟀다고 주장하지 않는다.** 4호는 **면적 분율**을 쟀고
  퍼콜레이션 판정을 하지 않았다 (`percolat*` 0 회).
- **압력 재인가가 `θ_AM` 을 1 로 되돌린다고 주장하지 않는다.** 부분 회복이고,
  회복의 대부분이 **음극 쪽**일 수 있다 (§5.2).
- **저율이므로 `η ≈ 1` 이라는 것은 우리 추론**이다 (2·3호의 결과를 이 셀에
  적용한 것). 이 논문은 **율 스윕을 하지 않았다.**
- **급락의 원인이 양극이라고 확인되지 않았다.** 자기 EIS 에서 가장 크게 자란 것은
  음극 쪽 LF 다 (§11 D8).
- **Fig. S3 을 보지 않았다** (크로핑 실패, §0). Weka 분할 워크플로 그림이고
  본문 텍스트로만 확인했다.

---

# 15. 좌표 색인 (다시 찾을 때)

| 찾는 것 | 어디 |
|---|---|
| 129 / 102 / 80 mAh g⁻¹, 1 mAh g⁻¹/cycle, 300 MPa 재가압 | 본문 p17400 ¶3–4 · Fig. 1(a) |
| `R_MF` 954 / 1241 / 3283 / 2755 Ω | 본문 p17400 ¶6 |
| `R_LF` ≈110 → ≈39 kΩ | **Fig. 1(c) 그림에만** (`[도표]`) |
| 50 kHz · 6 Hz 반원 경계 | **Fig. 1(d) 그림에만** (`[도표]`) |
| void 2.87 / 3.23 / 9.50 vol% | **Fig. 3 라벨** (본문은 "<3 %", "<0.5 %", "9.50 %") |
| 재구성 부피 57×33×29 / 66×41×31 / 64×38×36 µm³ | **Fig. 3 라벨** |
| **접촉 손실 10.4 %** | 본문 p17402 ¶1 |
| 접촉 손실 정의 | 본문 p17402 ¶1 (Fig. 4(d)(e)) |
| 단일 입자 한쪽 편중 + 확산거리 논증 | 본문 p17402 ¶2 · Fig. 4(f) |
| 시간상수 겹침 인정 | 본문 p17400 ¶6 |
| 음극 delamination 인정 | 본문 p17402 하단 |
| "후기에 몰린다" 결론 | 본문 p17403 Conclusions |
| "초기 미세균열 검출 불가" | 본문 p17403 ¶2 |
| 압력 100/300/100 MPa, **스프링 2 MPa** | **ESI p2 Cell fabrication** |
| EIS 조건 7 MHz–10 mHz, 10 mV, 방전 끝 | ESI p3 |
| FIB 50 nm 슬라이스, Weka, Dragonfly | ESI p3 |
| **사이클별 V–Q 곡선 (5/25/34, 34–40)** | **ESI Fig. S1(b)(c)** |
| **충전 전압 비단조 진동** | **ESI Fig. S1(c) 인셋** + ESI p4 캡션 |
| 회색도 히스토그램 (CNF↔LPS 겹침) | ESI Fig. S2 |
| 분할 정확도 주장(수치 없음) | ESI p6 Fig. S3 캡션 (**미열람**) |

# 16. 후속 후보

1. **Koerver et al., *Chem. Mater.* 2017, 29, 5574** (이 논문 ref 8; `assb`
   1·2·3호도 전부 인용) — 접촉 손실의 실험 원전. **여전히 1 순위**: 4호가
   `θ(N)` 을 3 점 줬지만 **용량과 같은 셀에서** 주지 못했다.
2. **Koerver et al., *Energy Environ. Sci.* 2018, 11, 2142** (ref 24) —
   ASSB 화학역학 종설 + **스택 압력**. Q6 을 스윕으로 채울 후보.
3. **Neumann, Danner, … Latz, *ACS AMI* 2020, 12, 9277** (ref 23) —
   2호 계보(Latz 그룹)의 ASSB 복합양극 수송 모형. **4호의 실측 기하를 2호의
   전방 모형에 꽂는 다리.**
4. **Zhang, … Scott, Ceder, *Adv. Energy Mater.* 2020, 1903778** (ref 27) —
   같은 저자들의 **LZO 코팅 불안정성** 논문. 4호가 `[인쇄]` 로 "용량 감쇠의 일부는
   LZO 불안정성" 이라 적으면서 정량하지 않은 몫이 거기 있다.
5. **Shi et al., *Adv. Energy Mater.* 2020, 10, 1902881** (ref 26) — 같은 저자의
   **양극 입자 크기 ↔ 이용률** 논문. §9-4 의 "입자 크기를 줄이면 이용률이 나빠진다"
   의 근거이고, **`θ` 와 입도의 관계**라 1호와 직접 붙는다.

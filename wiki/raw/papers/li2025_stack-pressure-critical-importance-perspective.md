---
title: "Li Q., Liu H., Ye Y., Li K.J., Wu F., Li L., Chen R. 2025 — The critical importance of stack pressure in batteries (Nat. Energy 10, 1064–1073)"
source_url: local-upload/21._The_critical_importance_of_stack_pressure_in_batteries.pdf + 21._Sup_The_critical_importance_of_stack_pressure_in_batteries.xlsx
source_url_note: "본문 PDF 10 쪽(pp. 1064–1073, Perspective, 그림 6 · 식 3 · 참고문헌 52) + Source Data xlsx 1 개(시트 Figure 5 = 내용은 Fig. 1b 원자료 29 점 · 시트 References = 출처 27 편 — Fig. 5 원자료는 없음). 그림 자동 크롭 6 장 + 수동 크롭 3 장(Fig. 2 · 5 · 6 — 자동 크롭이 패널 · 제목 줄을 잘라냄), 본 그림 전부. 3차 묶음 파일 21 (2차 묶음 큐 번호와 별개)."
source_doi: 10.1038/s41560-025-01820-x
source_license: "© Springer Nature Limited 2025 (exclusive rights) — 오픈액세스 표기 없음"
pdf_sha256: e203387f7784468dc958a70ec79098559956615e78e7655549a4e331b258f07c
si_sha256: 1559e0f10ab083c1f4f24986f0a27b80218bf0cabf64d7538b864f0af9333ec3
ingested: 2026-09-28
sha256: 31c88f5fa4fabb169614e61b1de4942045e8a631cbd191403b9e10c9000c12e5
---

# 수집 목적

`assb` 섹션 **59호** — **3차 묶음 파일 21**(3차 묶음의 첫 편). 3차 묶음의 파일 번호 21–33 은 2차 묶음 "큐 N" 번호
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d, 큐 1–59)와 **별개**다 — 이 편은 "큐 21" 이 아니다.
닻은 `questions/assb-contact-loss-vs-lampe.md`.

들어온 경로: 13호(Zheng 2026 *Energy*)가 스택 압력을 `[인쇄]` "perhaps most critically for system integration" 이라 부르며
단 인용 **[23]** 이 이 편이다. 13호 digest 후속 후보 1 순위 · 카드 Status Log(13호 항)에 **"Q6 요구 창의 정본 후보 (8호 Xu 2024 ·
12호 Tian/Shao 와 삼각 대조)"** 로 올라 있었고, 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1)에는
"★ Li Q. 외 2025 — *Nat. Energy* · Zhang 외 2025 — *Nat. Commun.* | 지목 13호 | 1 회 | Q6 | 무외압 Si 음극 — 저압 축" 한 줄로
파일 22 와 짝지어 있다.

이 digest 의 일 (지시):

1. **Q6 판정** — 카드가 적은 실측 **"압력 요구치 ≈1–5 MPa 가 종설 셋에서 원전 셋으로 독립 수렴"** 을 이 편이 지지 / 반박 / 무관 중 어느 쪽인지.
2. **13호 귀속 검사** — 13호가 [23] 에 매단 명제가 원문에 있는가.
3. Q1–Q8 · 채움표 59호 행 · 곱 축퇴 처방 마흔두 번째 적용.
4. **Source Data (xlsx)** — 시트 · 열 · 행과 어느 그림의 원자료인지. 원자료로 그림 판독을 교차 확인(`[도표]` 보다 원자료가 우선).
5. 2차 묶음 뒤 보류 결정 **(가)(나)(다)(아)(자)(차)(타)** 중 이 편이 근거를 주는 것을 **표시만** 한다 — 결정은 하지 않는다.

> ⚠ **형식 — Perspective 10 쪽(pp. 1064–1073), 1차 측정 0.** 그림 6 장 = 모식도 셋(Fig. 2 · 4 · 6) · 문헌 집계 둘(Fig. 1b · 5a,b) ·
> 재수록 하나(Fig. 3 — ref 21 · 32) · 개념 곡선 하나(Fig. 5c). 식 3 개(식 (1) 유속 부등식 · 식 (2)(3) 균일도 지표).
> 따라서 이 digest 의 `[인쇄]` 는 10 · 12 · 13 · 33호와 같은 뜻 — **"이 지면에 이렇게 적혀 있다"** 이지 "실측됐다" 가 아니다.
> **이 편의 요약 문장은 채움표 칸을 올리지 않는다** — 칸을 움직일 수 있는 것은 1차 원전으로 거슬러 확인된 명제뿐이다.
>
> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`) · `[데이터]` Source Data xlsx 의 셀 값과 그것으로 센 수 ·
> `[재현]` 우리가 지면 · 원자료의 숫자로 계산 · 대조한 값 · `[해석]` 우리 해석. `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **카드 실측 "≈1–5 MPa 가 종설 셋에서 원전 셋으로 독립 수렴"** | ❌ **반박 — "정본 후보" 가 그 띠를 인쇄하지 않는다** | `[인쇄]` 실용 요구치 **"<0.1 MPa"**(p.1071, 인용 0) · SSB 실험실 필요치 "several to hundreds of MPa"(p.1064) · "at least 20 MPa"(p.1066, [12][13]) · "above 10 MPa … limit practical viability"(p.1066, [16]). 1–5 MPa 를 **요구치로** 적은 문장 0 — 5 MPa 는 인용 프로토콜 "25 MPa … before reducing to 5 MPa for cycling"[36] 한 번이고, 이 편의 지도에서 0.1–수 MPa 는 **액체 LMB** 대역이다. ⇒ 계보 인쇄 요구치 띠 0.4–5 → **0.1–5 MPa**(폭 ×12.5 → ×50), 확인된 원전 **0 그대로** |
| **13호 귀속** (13호가 [23] 에 매단 것) | ✅ **선다 — 어휘 수준** | 13호 `[인쇄]` "mechanical requirement for stack pressure … [23] … creep, fatigue, and fracture" ↔ 이 편: 압력 요구(Fig. 1) · "lithium creep" · "mechanical fatigue in the SSE" · "fracture into multiple segments" · 집전체 "rupture" — 셋 다 있다. 13호의 `<5 MPa` 는 [35]·[45] 에 달렸고 [23] 이 아니므로 **13호 오귀속 아님**. 정정 대상은 **우리 13호 digest 대조표**가 [23] 을 요구치 원전 줄에 같이 적은 것 |
| **Q6 칸** | **이동 없음 — 층 넷** | ① 요구치 일곱 번째 인쇄 `<0.1 MPa`(원전 0) ② 제조(~100–500 MPa) ↔ 운전 **명시 분리** ③ 문헌 운전 압력 **원자료 첫 수록**(xlsx 29 점 — 그림 점과 어긋남) ④ CSP 개념 곡선(수치 0 · 이력 0) |
| **Q1 칸** | **없다 — `θ(N)` 0/59** | 양극 쪽은 "detachment of active materials from the SSE" 한 문단 + Fig. 2d 모식(수치 0). 그 문단의 핵심 명제 "Stack pressure minimizes this effect" 는 **인용 0**(앞 문장 [17] = 23호 Koerver 2017, 운전 압력 고정 편) |
| **Q4** | **0/59 — 쉰한 번째 성질** | `[인쇄]` "challenging to decouple the stack pressure effect independently" 를 적고, 처방한 벤치마크는 **CE 한 스칼라의 최대**(CSP) — 분해 대상 0 |
| **CSP "empirical model"** | **개념도 — 수치 0 · 적합 0 · 짝 자료 미공개** | "Based on our statistical analysis" 의 통계는 CE · 압력의 **주변 분포**(Fig. 5a · 5b 상자그림)뿐, CE–P 짝 그림 0, Fig. 5c 두 축 눈금 0, "validation" 인용 [44] 모델 편 · [45] Na 계 |
| **Source Data xlsx** | **Fig. 1b 원자료 — Fig. 5 원자료가 아니다** | 시트 2 개('Figure 5' · 'References'). 'Figure 5' 시트의 머리 셀이 **"Figure. 1b"**, 값 29 개 = Fig. 1b 세 범주. 캡션이 가리키는 "Source Data Fig. 5"(CE 통계)는 받은 파일에 없다. ⚠ **그림 점이 원자료와 다르다**(D1) |
| **곱 축퇴 처방 마흔두 번째** | **적용 불가 — 대상 없음** · 대신 52호 줄이 압력 벤치마크의 선행 검사 | 1차 데이터 0 · 곱이 설 모델 0. CSP 측정법(오름 압력 + CE 최대)은 CE 결손을 Li 재고 · 양극 접근 · 누설로 나누지 않는다 |
| **보류 (가)(나)(다)(아)(자)(차)(타)** | **근거 0 — 결정 안 함** | 일곱 항 모두 이 편의 내용과 닿지 않는다(§"보류 결정") |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | The critical importance of stack pressure in batteries |
| 저자 (7) | **Qianya Li**, **Hao Liu** (공동 1저자 — `[인쇄]` "These authors contributed equally"), **Yusheng Ye\***, Karen Jiayi Li, Feng Wu, **Li Li\***, **Renjie Chen\*** |
| 소속 | Beijing Institute of Technology — Beijing Key Laboratory of Environmental Science and Engineering, School of Materials Science and Engineering · BIT Zhuhai · BIT Advanced Technology Research Institute (Jinan) |
| 서지 | *Nature Energy* **10**, 1064–1073 (2025 년 9 월호) · doi `10.1038/s41560-025-01820-x` · **Perspective** · © Springer Nature Limited 2025 (exclusive rights, 오픈액세스 표기 없음) |
| 일정 | 접수 2024-05-19 · 승인 2025-06-06 · 온라인 2025-08-13 — `[재현]` 접수 → 승인 **383 일**, 승인 → 온라인 68 일 |
| 심사 | `[인쇄]` "Nature Energy thanks Hyun-Wook Lee and the other, anonymous, reviewer for their contribution to the peer review of this work." |
| 자금 | NSFC 92472112 · 52302212 · Beijing NSF L242005 · Taishan Scholars Program tsqn202408319 |
| 기여 | `[인쇄]` "Y.Y. conceived of the project. Y.Y., Q.L. and H.L. analysed the statistical data and wrote the manuscript. K.J.L. helped with the literature studies." |
| COI | `[인쇄]` "The authors declare no competing interests." |
| 분량 | 본문 pp. 1064–1071(그림 6 · 식 3) + 참고문헌 **52 편** pp. 1071–1072 + 후기 p. 1073 = PDF 10 쪽 |
| 보충 | Source Data xlsx 1 개(§"Source Data") — `[인쇄]` "The online version contains supplementary material available at https://doi.org/10.1038/s41560-025-01820-x." |
| PDF sha256 | `e203387f7784468dc958a70ec79098559956615e78e7655549a4e331b258f07c` (8,025,449 B) |
| xlsx sha256 | `1559e0f10ab083c1f4f24986f0a27b80218bf0cabf64d7538b864f0af9333ec3` (14,675 B) |
| 서지 대조 | 호출자가 웹으로 확인한 "Li Q., Liu H., Ye Y., … *Nature Energy* 10, 1064–1073 (2025)" 와 **일치**. 문서 종류는 PDF 머리의 "Perspective" |
| `[해석]` 자기 인용 | ref 12 (Li, Q. et al. *Angew. Chem. Int. Ed.* 2024 — 제1저자 성·이니셜 일치, 같은 사람인지는 PDF 로 미확인) · ref 32 (Huang, W. et al. *Nat. Commun.* 2022 — 본문이 `[인쇄]` "**we** established … (ref. 32)" 라 적으므로 저자 겹침이 있는 편이다; 인쇄 저자 목록은 "et al." 뿐이라 누구인지는 확인 불가) |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **실용 요구치 "<0.1 MPa" 의 출처 0** — `[인쇄]` "driven by practical considerations (typically requiring a pressure of <0.1 MPa)". 같은 단락의 유일한 인용 [52] 는 저압 전략 목록에 붙는다 | 계보 **일곱 번째** 요구치 인쇄값이 또 출처 없이 나온다(§"Q6") |
| G2 | **CSP 의 값이 하나도 없다** — CSP_L · CSP_S1 · CSP_S2 수치 0, Fig. 5c 두 축 눈금 0, "Based on our statistical analysis" 의 분석 절차 0 | "empirical model" 이 적합도 수치도 아닌 모양 하나다 |
| G3 | **Fig. 5 원자료 미수령** — 캡션 `[인쇄]` "summarized in Source Data Fig. 5". 받은 xlsx 는 시트명만 'Figure 5' 이고 내용은 Fig. 1b(§"Source Data") | 본문 `[인쇄]` "we have listed the battery Coulombic efficiency along with the stack pressure" 의 **짝**을 확인할 길이 없다 |
| G4 | **CE 의 정의 0** — Li‖Cu 반쪽 CE 인지 완전지 CE 인지, 몇 번째 사이클 · 평균인지 · 전류 · 적재 · 온도 — `[인쇄]` "measured Coulombic efficiencies in batteries" 뿐 | CE 를 압력의 함수로 읽는 벤치마크의 **종속 변수가 정의되지 않았다** |
| G5 | **"Stack pressure minimizes this effect (detachment)" 의 근거 0** — 인용 번호 없음(앞 문장 [17] 은 운전 압력 고정 편, D7) | 우리 [[assb-pressure-reapplication-separation-test]] 의 전제(`P↑` → 접촉 되돌림)와 같은 명제인데 원전이 없다 — 33호 G4 와 같은 형태 |
| G6 | **SSE 피로의 하중 형태 근거** — `[인쇄]` "fluctuations in stack pressure at the MPa level can induce mechanical fatigue in the SSE"[39] 인데 [39] = 5호 Doux 2020 digest 에 그 명제가 없다(D6) | 위 벽 "피로" 형태(13호)의 원천이 이 편에서도 비어 있다 |
| G7 | 균일도 지표 식 (3)의 `n` · `P̄` 정의 0 · 문턱 `σ² < 3 %` 출처 0(D8) | 지표를 옮겨 쓸 수 없다 |
| G8 | dP/dQ 도금 문턱의 **검출 성능 0** — `[인쇄]` "high-precision indicator" 에 오검출 · 누락률 · 지연 수치 0 | 관측 채널로 쓰기 전 필요한 값 |
| G9 | EV 한 대 "approximately 8,000 SSBs" 출처 0 | 규모 논증의 입력 |
| G10 | Fig. 1b **점 ↔ 원자료 행 대응표 0**(D1) | 그림 판독과 원자료가 어긋나도 어느 점이 어느 편인지 모른다 |
| G11 | `LLI` · `LAM` · `degradation mode` · `OCV` · `EIS` · `SOH` **전부 0** — 전기화학 축은 CE 하나(`capacit*` 4 · `impedance` 1 · `resistance` 2) | 이 편의 체계에서 용량 손실은 분해의 대상이 아니다(Q4) |
| G12 | 압력 **이력**(가압 ↔ 감압 분기) 0 — `hysteres*` · `histor*` 0 | CSP 측정법(오름 스윕)의 "최소 압력" 은 분기에 따라 다를 수 있다(5호 이력) |

# 그림 — 자동 크롭 6 장 + 수동 크롭 3 장, 실제로 본 것: **전부** (Fig. 1–6 + 수동 2 · 5 · 6)

폴더 `raw/figures/li2025_stack-pressure-critical-importance-perspective/`. ⚠ 자동 크롭 셋이 불완전해 수동 크롭을 더했다(`figures.json` 의
`manual: true` 세 행): **Fig. 2** 는 bbox 가 x1 355 pt 에서 잘려 패널 d · e 가 빠짐 → `fig_2_manual_p3.png` · **Fig. 5** 는 x1 333 pt 에서
잘려 패널 c(CSP 곡선)가 빠짐 → `fig_5_manual_p7.png` · **Fig. 6** 은 y0 70 pt 에서 시작해 패널 제목 줄이 빠짐 → `fig_6_manual_p8.png`.
Fig. 1 · 3 · 4 는 머리 쪽 패널 문자(a · b)만 빠지고 내용은 온전하다.

## `[도표]` Fig. 1 — 코인셀 등가 압력 비유 + 문헌 압력 범위 (봤다 · 화소 판독 + 원자료 대조) — ⚠ **그림 점이 원자료와 다르다**

- **a**: 닭(LIB) · 개(액체 LMB) · 코끼리(고체 LMB)가 코인셀 위에 서 있는 비유 — 수치 0. 아래에 세 셀 단면(Al/Cu 집전체 · 양극 · 분리막 · 음극 /
  Li metal anode / SSE).
- **b**: 세로 로그축 0.01–1,000 MPa · 가로 범주 넷(LIBs · Liquid-state LMBs · Solid-state LMBs · Future batteries). 점 라벨 "0.01 MPa" ·
  "0.35 MPa" · "1.1 MPa" · "1.2 MPa" · "20 MPa" · "250 MPa". 실선 추세가 고체 LMB 에서 꺾여 **점선이 별표 "Future target — Low or zero
  pressure"** 로 떨어진다. `[도표]` 별표 중심 ≈0.03 MPa.
- 판독 방법: 큰 눈금 6 개(1,000 → 0.01)의 위치를 눈금 라벨 중심과 대조(차 ≤1.5 px)해 확인하고, 작은 눈금으로 구간별 로그 보간했다.
  점 29 개를 색 분할(회 7 · 황 9 · 청 13)로 찾았다 — **원자료의 개수와 같다.** ⚠ 10 배 구간 길이가 140 · 155 · 159 · 161 · 154 px 로 고르지
  않다 — 축 자체가 다시 그려진 것이라 판독 불확실은 ≈±10 %.

| 범주 | `[데이터]` xlsx (n · 범위 · 중앙값) | `[도표]` 그림 점 (n · 정렬한 값) | 판정 |
|---|---|---|---|
| LIBs | 7 · 0.01–0.1 · 0.05 MPa (0.01 · 0.042 · 0.05 · 0.05 · 0.075 · 0.08 · 0.1) | 7 · ≈0.012 · 0.036 · 0.044 · 0.049 · 0.056 · 0.063 · 0.099 | 끝점 ✓ · 가운데 값이 원자료보다 **최대 ≈25 % 낮다** |
| Liquid-state LMBs | 9 · **0.69–1.4** · 1.1 MPa | 9 · ≈**0.34** · 0.46 · 0.65 · 0.66 · 1.01 · 1.15 · 1.50 · 1.87 · **2.51** | ❌ **범위가 원자료 ×2.0 → 그림 ×7.5** — 원자료에 없는 <0.69 점 4 개 · >1.4 점 2 개 |
| Solid-state LMBs | 13 · 5–400 · 45 MPa | 13 · ≈5.6 · 8.7 · 12.7 · 15.0 · 16.9 · 25.2 · 30.0 · 51.3 · 51.9 · 89.9 · 123 · 193 · 365 | ⚠ 순위 짝으로 가운데가 **−25 … −33 %** (20 → ≈15 · 25 → ≈17 · 34 → ≈25 · 45 → ≈30 · 70 → ≈51 · 75 → ≈52 · 250 → ≈193) |

- 캡션 `[인쇄]` "All data points are included in the Source Data Fig. 1." ⇒ **D1**: 그림의 점은 원자료의 점이 아니다(특히 액체 LMB).
  점의 가로 위치는 범주 안 흩뿌림이라 의미가 없고, 점 ↔ 원자료 행 대응표도 없다(G10). **수치는 원자료로 옮긴다.**
- 라벨 "0.35 MPa" 는 ≈0.1 MPa 점 옆에 붙어 있지만 원자료 LIB 최댓값은 0.1 — 0.35 는 본문 "<50 psi (<0.35 MPa)" 의 상한이다(D13).
- `[해석]` 이 편의 지도에서 **0.1–수 MPa 는 액체 LMB 대역**이다(`[인쇄]` "Moderate stack pressures of 0.1 to a few MPa in liquid-state LMBs") —
  우리 계보가 "SSB 산업 요구치" 로 모은 ≈1–5 MPa 띠가 여기서는 액체 셀의 자리다.

## `[도표]` Fig. 2 — void 억제 모식 (봤다 · 자동 크롭 a–c + 수동 크롭 a–e)

- **a**: 위아래 "Load cell" 사이 고체 LMB(양극 복합체 · SSE · Li 금속), 표시 1–4 가 b–e 로 이어진다. 수치 0.
- **b** "Lithium filament voids": 무압 — 긴 필라멘트, 두께 변화 `ΔH` ↔ 가압 — 조밀, `Δh`. 캡션 `[인쇄]` "ΔH > Δh".
- **c** "Grain boundary voids": 무압 — SE 입자 사이로 Li 침투 ↔ 가압 — `P` 를 `P_vertical` · `P_horizontal` 로 분해. `[재현]` 두 성분 화살표의
  벡터 합이 `P` 화살표와 맞고 두 성분은 거의 직교한다(화면 좌표 판독) — 그림 정합.
- **d** "SSE/active material voids": 무압 — 활물질 입자 셋이 **입자 전체를 두른 점선 void** 안에 떠 있고 Li 수송 화살표에 금지 표시 ↔ 가압 —
  셋이 서로 붙은 채 SE 에 묻힌다. `[해석]` 그려진 것은 **통째 고립(`θ` · `ε_p` 자리)의 압력 복원**이지 표면 피복(`φ` · `A_eff` 자리)이 아니다 —
  37호 틀로 `LAM_PE` 와 같은 자리의 그림. 수치 0 · 인용 0(G5).
- **e** "Interfacial voids": 무압 — Li⁺ migration 화살표가 void 사이 접촉 지점으로 몰리고 Li 는 Diffusion 만 ↔ 가압 — "Creep + Diffusion" 이 void
  (점선 = 원래 경계)를 채우고 migration 이 고르다. 식 (1) 의 그림판.

## `[도표]` Fig. 3 — 전기화학-기계 관계 (봤다 · 화소 판독) — ⚠ **패널 a ↔ b 경계가 같은 (P, i) 쌍에서 어긋난다**

재수록: a · b ← ref 21 (Yan et al. 2022 *AEM*, Wiley) · c ← ref 32 (Huang et al. 2022 *Nat. Commun.*, CC BY 4.0).

- **a**: 가로 스택 압력 2–14 MPa · 세로 전류밀도 0.5–3.5 mA cm⁻², 붉은 "Transition" 곡선 위 = "Void formation", 아래 = "No void".
  `[도표]` 경계 `i_c(P)` ≈0.80(2) · 최소 ≈0.68(3.5) · 0.86(6) · 1.13(8) · 1.33(9) · 1.58(10) · 2.40(12) · 2.94(13) · 3.5(14 MPa, 그림 끝) mA cm⁻².
  **저압 쪽이 비단조**(2 → 3.5 MPa 에서 내려간다) — 본문 설명 0.
- **b**: 아래 가로 = 압력 2–14 MPa, **위 가로 = 전류밀도 0.5–3.5 mA cm⁻²** — 눈금이 같은 위치(2 ↔ 0.5, 6 ↔ 1.5, 10 ↔ 2.5, 14 ↔ 3.5)라
  `[재현]` `P = 2 + 4(i − 0.5)` 인 한 경로다. 세로 log 유속 10⁻³–10⁻¹ µmol cm⁻² s⁻¹. `[도표]` `J_creep`(붉은 직선 — 반로그에서 직선이니 압력에
  지수) ≈0.0040(2 MPa) → ≈0.074(14 MPa) · `J_migration`(검은 곡선) ≈0.0049 → ≈0.035 · `J_diffusion`(점선) ≈0.0024 일정.
  `[재현]` `J_migration` 은 `i/F` 와 맞는다(0.5 mA cm⁻² → 0.0052 · 3.5 → 0.036 µmol cm⁻² s⁻¹). 교차 `J_creep = J_migration` ≈9 MPa ↔ ≈2.25 mA cm⁻²;
  식 (1) 경계(`J_creep + J_diffusion = J_migration`)는 ≈8.0–8.5 MPa ↔ ≈2.0–2.1 mA cm⁻².
- ⚠ **D5**: 같은 경로에서 a 의 경계 전류는 8–9 MPa 에서 ≈1.1–1.3 mA cm⁻² — b 의 경계(≈2.0–2.25)의 ≈0.6 배. 거꾸로 b 의 경로를 a 에 올리면
  경계에 닿는 곳은 **14 MPa** 다(8–9 MPa 가 아니라). 두 패널이 같은 원전(ref 21)에서 왔는데 같은 (P, i) 쌍에 다른 판정을 준다 —
  원전을 열람하지 않아 원전에서도 그런지는 모른다.
- **c**: `dP/|dQ|` (MPa mAh⁻¹) 대 시간 0–66 h, 배경색 = C-rate(청 저율 ↔ 적 고율, ≈36–52 h 가 고율). 붉은 점선 "Li-plating threshold"
  `[도표]` ≈+0.005 MPa mAh⁻¹ — `[인쇄]` "defined by the maximum of dP/dQ at 0.2 C". 고율 구간에서 봉우리 ≈+0.010–0.013 · 골 ≈−0.04.
  검출 성능 수치 0(G8). 세로축 라벨 "dP/|dQ|" ↔ 캡션 · 본문 "dP/dQ"(D12). LIB(흑연) 자료다 — ASSB 아님.

## `[도표]` Fig. 4 — 과압 실패 모식 (봤다) — ⚠ d · e 에 균열선이 없다

- a(액체 LMB) · b(고체 LMB) 단면에 표시 1–11 → c 집전체 변형 · 파단 · d/e "Electrode crack" · f/g "Material pulverization" ·
  h/i "Lithium deformation" · j "Dendrite growth"(분리막) · k "Dendrite across SSE" · l "Separator pores closure" · m "SSE fatigue-induced crack".
- d · e 를 확대해 봤다: 입자가 눌려 **비구형으로 변형**된 모습뿐, 균열선 0(D11). f/g 는 입자 파쇄가 그려져 있다.
- m: SE 입자 사이 흰 틈 — 캡션 `[인쇄]` "The SSE crack phenomenon with continued pressure **fluctuation** induces mechanical fatigue".

## `[도표]` Fig. 5 — CE · 압력 통계 + CSP 곡선 (봤다 · 자동 크롭은 a · b 만, 수동 크롭으로 c) — **짝 없는 주변 분포 둘과 눈금 없는 곡선 하나**

- **a** 왼쪽: 7 화학(Li · Na · K · Zn · Mg · Ca · Al)의 CE 상자그림 90–100 %, 청 = 압력 정보 있음 · 회 = 없음.
  `[도표]` Li 상자 ≈98.0–99.8 % · 중앙 ≈99.0 % · 아래 수염 ≈95.4 %(화소 판독, 2 %당 93 px). 오른쪽 확대 98.0–100.0 %: Li 점은 전부 짙은 청,
  Na 는 대부분 회색 + 연청 둘.
- **b** 왼쪽: 압력 0–500 MPa(≈260–350 MPa 사이 축 끊김). Li · Na 에 상자, K 1 점 ≈2 · Zn 2 점 ≈0 · Mg 2 점 ≈25 · ≈100 MPa, Ca · Al 0.
  `[도표]` Li 상자 ≈1.3–34 MPa · 위 수염 ≈75 MPa · 이상점 ≈450 MPa 까지 · **중앙선 식별 불가**(아래 모서리와 겹친 것으로 보인다).
  Na 상자 ≈3.4–20 · 중앙 ≈10 · 위 수염 ≈29 MPa. 오른쪽 확대 0–10 MPa: Li 점 다수가 ≈0–3.2 MPa, 4–5 · 6 · 7 MPa 에 무리, 10 MPa 선에 잘린 점들.
- **c** "Relationship between Coulombic efficiency and stack pressure in liquid- and solid-state LMBs" — **두 축 눈금 0**.
  액체 LMB(청): L1 급상승 → CSP_L → L2 평탄(청 음영 = 최적) → L3(점선 하강). 고체 LMB(주황): S0 바닥 → CSP_S1 → S1 상승 → CSP_S2 →
  S2 평탄(주황 음영 = 최적) → S3(점선 하강). 두 평탄의 높이는 거의 같다.
- `[해석]` Fig. 5 에는 **CE 와 압력을 한 점에 짝지은 그림이 없다.** 본문은 `[인쇄]` "In lithium-based batteries, we have listed the battery
  Coulombic efficiency along with the stack pressure" 라 적지만 짝은 원자료(Source Data Fig. 5)에만 있고, 그 원자료는 받은 파일에 없다(G3).
  그리고 Li 범주는 LIB · 액체 LMB · 고체 LMB 를 **한 상자에 합친다** — 5c 의 두 곡선(액체 ↔ 고체)을 5a · 5b 에서 뗄 수 없다.

## `[도표]` Fig. 6 — 향후 방향 (봤다 · 자동 크롭은 제목 줄 누락, 수동 크롭으로)

- **a** "Stack pressure benchmark": "How much pressure?" + 0–50 MPa 게이지(바늘 여럿) + 과녁 "Standardizaton process"(오타, D12) —
  Device · Electrolyte · System · Size · Temperature · …… → "Exact value".
- **b** "Stack pressure diagnosis": Pressure sensor + Battery monitoring + Dynamic regulation; Pressure → Signal → Signal + Threshold(문턱을 넘는 스파이크).
- **c** "Spatial homogeneity control": "Maintain constant"(스프링 지그) · "Uniform distribution"(층별 압력 지도); Stack pressure 대 cycle time —
  **Now = 큰 진동(청 점선) · Future = 평평(적 실선).**
- **d** "Stack pressure optimization": 게이지 ≈50 → ≈0 MPa; 삼각형 — Electrochemical properties(Bad → Good) · Stack pressure(High → Low) ·
  Interface contact(Loose → Tight), "Current solid-state LMBs"(Bad · Loose 모서리) · "Current liquid-state LMBs"(High · Tight 모서리) → "Future"(Good · Low).
- `[해석]` **제어 방향**: 이 편은 압력을 **일정하게 두고**(c "Maintain constant") 압력 **신호로 운전을 조절**한다 — `[인쇄]` "Battery operation
  can therefore be dynamically regulated adaptively from the feedback of stack pressure". 13호의 "율↑ → P↑, 휴지 · 노화 → P↓"(압력 = 조작 변수)와
  **반대 방향**이다(§"Q6").

# Source Data (xlsx) — 시트 · 열 · 행

- 파일 14,675 B · sha256 `1559e0f1…` · Microsoft Excel(AppVersion 16.0300) · `docProps/core.xml` 작성자 "LH" · 최종 수정자 "Hao Liu"(공동 1저자) ·
  **최종 수정 2025-07-20**(승인 뒤 · 온라인 전) · 숨은 시트 0 · 수식 0 · 셀 주석 0 · 이름 정의 0 · 차트 · 이미지 0.
- **시트 1 'Figure 5'** (A1:H17, 병합 7) — ⚠ **A1 머리 셀 "Figure. 1b"**. 2 행 범주(A–B LIBs · C–D Liquid-state LMBs · E–F Solid-state LMBs),
  3 행 "X · Y", 4 행 "Stack pressure (MPa)", 값은 5–17 행: LIB **7** · 액체 LMB **9** · 고체 LMB **13** = **29 값**. X 열은 범주 이름 병합뿐.
- **시트 2 'References'** (A1:S15, 병합 9) — 범주별 표(Number · Stack pressure (MPa) · Title · Reference): LIB **6 편**(7 값 — Cannarella 2014
  *JPS* 245 가 0.1 · 0.05 두 값) · 액체 LMB **8 편**(9 값 — Zhu 2021 이 1.1 · 1.4 두 값) · 고체 LMB **13 편**(13 값). **출처 27 편.**
- ⇒ **이 파일은 Fig. 1b 의 원자료다.** Fig. 5 캡션이 가리키는 "Source Data Fig. 5"(CE · 압력 통계)는 이 파일에 없다. 출판사 쪽 Source Data 가
  그림별 두 파일(Fig. 1 · Fig. 5)인지, 받은 것이 어느 쪽 이름으로 올라간 것인지는 이 파일만으로 판정할 수 없다(D2).

| 범주 | `[데이터]` 값 (MPa) · 출처 (시트 'References' 서지 그대로 요약) |
|---|---|
| LIBs | 0.1 · 0.05 Cannarella & Arnold 2014 *JPS* 245 · 0.05 Cannarella & Arnold 2014 *JPS* 269 · 0.042 Hahn … Birke 2021 *J. Energy Storage* 40 · 0.01 Spingler 2021 *JES* 168 · 0.075 Aufschläger … Jossen 2024 *J. Energy Storage* 76 · 0.08 Müller 2019 *JES* 166 (Si/C \| NMC811) |
| Liquid-state LMBs | 1.1 Yin 2018 *Nano Energy* 50 (= 본문 ref 3) · 1.2 Louli 2019 *JES* 166 (무음극) · 0.85 Zhang C. 2019 *JES* 166 (= 본문 ref 42) · 1.2 Weber 2019 *Nat. Energy* 4 (무음극 파우치) · 1.0 Harrison 2021 *iScience* 24 · 1.1 · 1.4 Zhu 2021 *Acta Phys. Chim. Sin.* 39 · 0.69 Kasse 2022 *ACS AEM* 5 · 1.2 Kim … Sun 2023 *ACS Energy Lett.* 8 |
| Solid-state LMBs | 20 Zhang X. 2023 *CRPS* 4 ("high-throughput **simulations**") · 25 Doux 2020 *JMCA* 8 (5호 *AEM* 와 다른 편) · 10 Yuan 2021 *Nano Energy* 86 · 5 Hänsel & Kundu 2021 *Adv. Mater. Interfaces* 8 · 250 Ye & Li 2021 *Nature* 593 · 400 Tu … Ceder 2020 *CRPS* 1 · **143** Koerver 2018 *EES* 11 · 98 Cronau 2023 *Adv. Mater. Interfaces* 10 · 13 Wang Y. 2022 *Adv. Mater.* 35 (무음극) · 70 Jung 2019 *AEM* 10 (Ni-rich 양극) · 75 Yamamoto … Takahashi 2020 *JPS* 473 · 34 Sung 2023 *Adv. Mater.* 35 · 45 Hänsel … Kundu 2021 *Chem. Mater.* 33 (Li-In/Sn 음극) |

- `[데이터]` 요약: LIB 0.01–0.1(중앙 0.05) · 액체 LMB 0.69–1.4(중앙 1.1) · 고체 LMB 5–400(중앙 45) MPa. 고체 13 값 중 **≥50 MPa 6** ·
  **≤5 MPa 1**(Hänsel & Kundu 2021, 5 MPa) · 1–2 MPa 대 **0**.
- `[해석]` 출처의 성격(제목 기준): 고체 범주 13 편 중 제목에 Li 금속 · 무음극 · 덴드라이트 · 도금이 드러나는 것 7, 드러나지 않는 것 6(Zhang X. 2023
  시뮬 · Doux 2020 *JMCA* · Koerver 2018 *EES* · Jung 2019 Ni-rich 양극 · Yamamoto 2020 · Hänsel 2021 Li-In/Sn 음극) ⇒ "Solid-state LMBs" 범주는
  사실상 **SSB 전반**이다. 제목에 **시뮬레이션**이 명시된 행 1(Zhang X. 2023, 20 MPa) — 캡션의 "pressure values applied" 에 모델 입력값이
  섞였다. 나머지 행의 성격은 원문 미열람.
- `[재현]` 본문 참고문헌 52 편과 겹치는 출처는 **2 편**(Yin 2018 = ref 3 · Zhang C. 2019 = ref 42) — 나머지 25 편은 원자료에만 있다.
- ⚠ **Koerver 2018 *EES* 의 값이 편마다 다르다** — 이 원자료 **143 MPa** ↔ 33호 Table 1 운전 **70 MPa**(제조 445; 33호 digest). 원전 미열람 —
  같은 원전의 다른 셀 · 다른 단계일 수 있다(D9).

# 절별 해체

## 초록 · 서론 (pp. 1064–1066)

- 초록 `[인쇄]`: "The wide variation in stack pressure levels in batteries has perplexed researchers seeking to determine an optimal value …
  we … advocate for considering a **critical stack pressure empirical model** as a means to determine the optimal stack pressure. We begin by
  analysing the broad range of stack pressures, which span multiple orders of magnitude. We then categorize their effects into **four distinct
  stages** … Future research on stack pressure should focus on areas such as **benchmarking, diagnosis, spatial distribution and minimization**."
  `[해석]` "네 단계" 는 Fig. 5c 의 S0–S3 로 읽힌다(액체 LMB 는 L1–L3 셋).
- 동기 — CE: `[인쇄]` "Pursuing batteries that approach **100% Coulombic efficiency** is a major target" · "elevating the stack pressure alone can
  significantly enhance the Coulombic efficiency, increasing it **from 60 to 90%** and prolonging the cycle life by **more than six times**3,4"
  (ref 3 Yin 2018 · ref 4 Gireaud 2006 — 둘 다 **액체** Li 금속) · "current high-Coulombic-efficiency (>99%) battery designs are often achieved
  under varying stack pressures5".
- 범위: `[인쇄]` "Low stack pressures of **<50 psi (<0.35 MPa)** in LIBs are adequate … Moderate stack pressures of **0.1 to a few MPa** in liquid-state
  LMBs could help to suppress dendrite growth … much higher stack pressures, ranging from **several to hundreds of MPa** in solid-state LMBs, are
  necessary to prevent layer delamination, severe volume expansion and interfacial contact issues (Fig. 1b)." `[재현]` 50 psi = 0.345 MPa ✓.
- ★ **제조 ↔ 운전 분리** `[인쇄]`: "although **fabrication pressures** for solid-state electrolyte (SSE) pelletizing are usually high (**~100–500 MPa**),
  this Perspective specifically focuses on **operating stack pressures**2" (ref 2 = Hu 2024 *Nat. Rev. Mater.*).
- 규모: `[인쇄]` "in a future electric vehicle powered by approximately **8,000 SSBs**, the implementation of a pressurization system poses a major
  challenge" (인용 0, G9) · "Battery materials suffer from **mechanical fatigue** under excessive stack pressure".
- ★ **분리 불가의 인쇄** `[인쇄]`: "Besides, the qualitative and quantitative relationships between stack pressure and electrochemical behaviour are
  ambiguous. Currently, it is **challenging to decouple the stack pressure effect independently**, partially due to the electrochemomechanical
  relationship of stack pressure."
- 주장 예고 `[인쇄]`: "Our analysis indicates that electrochemical performance peaks are achieved within a specific stack pressure range. We therefore
  propose a critical stack pressure (CSP) empirical model as a benchmark for standardizing battery evaluation. We emphasize that the major contribution
  of stack pressure is in mitigating void formation during the initial stage. Moreover, we identify a threshold at which the beneficial effects of
  stack pressure are maximized, beyond which parasitic effects begin to dominate."
- 서론 오타: `[인쇄]` "operating conditions (such as current density, **temperate** and stack pressure)" — `temperature` 는 본문 0 회(D12).

## Suppression of voids (pp. 1066–1067) — ★ 축 Q1 · Q6

- `[인쇄]` "Void formation is one of the main culprits of battery degradation and failure, frequently arising from material volume changes, crack
  propagation or irregular lithium plating/stripping. Stack pressure can mitigate the formation of voids, including in lithium filaments, grain
  boundaries, SSE/active materials and interfaces, during cycling (Fig. 2a)."
- Li 필라멘트: Monroe–Newman `[인쇄]` "when the shear modulus of the SSE or polymer separator exceeds twice that of lithium metal (**G_Li = 4.2 GPa**)" ·
  AFM 캔틸레버 국소 **≈13 MPa**[10] · 액체 LMB **0.35 MPa** 에서 이론 밀도 **99.49 %** Li[11] · `[인쇄]` "In contrast, SSBs typically require **at least
  20 MPa** to regulate deposited lithium porosity and reduce the formation of inactive lithium12,13" (ref 12 = 자기 종설로 보임).
- 입계: `[인쇄]` "Stack pressure can facilitate lithium dendrite growth across SSEs along the grain boundary … even at very low current densities" ·
  "High stack pressures **above 10 MPa** are generally considered necessary to achieve sufficient suppression, yet such high values **limit practical
  viability**16" (ref 16 = Albertus 2021 *ACS Energy Lett.*) · 대안 = 측면 가압 · 단결정 SSE.
- ★ **양극 복합체 — 이 편에서 카드 물음에 가장 가까운 문단** `[인쇄]`: "Another contributor to void formation is the **detachment of active materials
  from the SSE** in electrodes. Detachment commonly arises from factors such as mechanical stress, thermal expansion/contraction, chemical reactions or
  structural shifts within the battery system, creating gaps and **cutting off the lithium transport pathway**17. **Stack pressure minimizes this effect,
  thereby preventing disengagement** between the SSE and active materials in electrodes (Fig. 2d). Therefore, the application of an appropriate stack
  pressure is crucial to maintain battery stability and longevity, by averting the occurrence of detachment-related issues." — 수치 0 · 둘째 문장
  인용 0(G5 · D7). `[해석]` "cutting off the lithium transport pathway" 는 입자 통째 고립의 말이고 Fig. 2d 도 그렇게 그렸다 — 용량 쪽으로는
  `LAM_PE` 와 같은 자리다. 이 편은 그것이 `LAM` 과 어떻게 갈리는지 묻지 않는다.
- 계면 void(음극): 식 (1) `[인쇄]` "J_creep + J_diffusion > J_migration"[21] — "This causes vacancies to transport away from the interface, thus
  replenishing voids at the interface."

## Electrochemomechanical relationship of stack pressure (pp. 1067–1068) — 축 Q2 · Q7

- `[인쇄]` "Currently, many insights into this rely heavily on **simulations**, due to the lack of definitive experimental data." ·
  "Stack pressure can mirror electrochemical behaviour as it changes periodically with the electrochemical process23. This phenomenon offers a
  preliminary basis for **differentiating between normal and harmful states**, including interfacial evolution24, short circuiting25 and gas evolution26."
  (ref 23 = Zhang W. … Janek 2017 *JMCA* 5, 9929 — 이번 묶음 파일 24.)
- 압력–전류 기준 둘: Fig. 3a/b(ref 21, 창 = 크리프 · 확산 · 이동 경쟁) · `[인쇄]` "Zhang and co-workers27 further proposed a threshold condition based on
  the Bond equation (stack pressure (P)/current density (I) **> 25 MPa cm⁻² mA⁻¹**) to assess the mechanical stability at the **SSE/cathode interface**."
  ⚠ 단위 부호(D4). `[재현]` 이 기준을 그대로 받으면 1 mA cm⁻² 에 25 MPa · 13호 그리드 5 mA cm⁻² 에 **125 MPa** · 이 편 실용 목표 0.1 MPa 에서
  허용 전류 **0.004 mA cm⁻²** — 이 편은 두 명제를 조정하지 않는다(D4).
- `[인쇄]` "in the stripping process the critical current density is theoretically positively correlated with increasing stack pressure, whereas in the
  plating process a negative correlation is observed29,30."
- ★ **Q7 — 압력 기저선의 합** `[인쇄]`: "Compounding the complexity, the accumulation of **residual solid electrolyte interphase and isolated lithium**
  would gradually increase the **baseline stack pressure**, but this non-routine variation **cannot be accurately correlated with specific electrochemical
  reactions**31."
- ★ **dP/dQ 도금 문턱(LIB)** `[인쇄]`: "we established a relationship between lithium plating and lithium intercalation by defining a specific threshold
  based on the change in stack pressure per unit charge (dP/dQ) in LIBs, as shown in Fig. 3c (ref. 32) … once lithium deposits on the graphite surface,
  it further **re-intercalates** into bulk graphite particles. This re-intercalation enhances battery capacity while concurrently decreasing battery stack
  pressure, leading to an **asynchrony** in reaching the peak stack pressure and charge capacity. Elucidating these behaviours remains **system specific**".

## Excessive stack pressure (p. 1068) — 축 Q6 위 벽

- `[인쇄]` "Stack pressure is a double-edged sword, with an optimal range … When the stress from stack pressure surpasses the **yield strength**, battery
  materials become unable to withstand such immense stress, leading to plastic deformation or even structural damage."
- 집전체 `[인쇄]` "lower deformability (**∼2%**) compared with that of the separator (**70–150%**)"[33] · 전극 균열 · 분쇄[34] · Li 크리프 · 소성변형으로
  "lithium being forced out through gaps"[35] · 분리막 · SSE 기공을 건너는 덴드라이트 → 단락[36].
- 액체: `[인쇄]` "excessive pressure may lead to the **closure of separator pores**, hindering ion transport and elevating impedance"[37].
- ★ **고체 — 피로의 하중 형태** `[인쇄]`: "In solid-state cases, **fluctuations in stack pressure at the MPa level** can induce **mechanical fatigue** in the SSE,
  leading to crack formation as the material attempts to relieve internal stress (Fig. 4m)39. Over time, the SSE may **fracture into multiple segments**,
  impeding Li⁺ ion migration and creating voids conducive to the growth of lithium filaments." — ref 39 = **5호 Doux 2020 *AEM***(D6).
- `[인쇄]` "Between these extremes lies a critical range where the benefits of stack pressure are maximized".

## CSP (pp. 1068–1070) — ★ 이 편의 제안

- 근거 문장 `[인쇄]`: "Although many strategies have shown increased Coulombic efficiency in various battery systems, their correlation with stack pressure
  remains unknown due to the **lack of stack pressure recording**. It has been found that the interfacial resistance decreases to a certain extent and
  remains stable with increasing stack pressure, and other factors have similar variation trends with pressure40,41. This indicates that stack pressure
  does not exhibit a linear correlation with Coulombic efficiency, where there **might** exist a threshold instead42."
- 통계 `[인쇄]`: "We summarize the statistics of Coulombic efficiency (Fig. 5a) and stack pressure (Fig. 5b) … In lithium-based batteries, we have listed the
  battery Coulombic efficiency along with the stack pressure. However, for other batteries, most lack stack pressure information".
- 모형 `[인쇄]`: "**Based on our statistical analysis**, we propose a CSP empirical model, as depicted in Fig. 5c, that illustrates the general relationship
  between Coulombic efficiency and stack pressure in liquid- and solid-state LMBs." 단계: L1(void 제거 시작, CE 상승) → CSP_L(최대) → L2(평탄 —
  `[인쇄]` "further elimination of voids by increasing stack pressure is debatable") → L3(실패). 고체: `[인쇄]` "an additional stage (stage S0) with the
  requirement for considerably higher initial stack pressure (termed CSPS1) to initiate battery operation" → S1 "keeps establishing better interfacial
  contact" → CSP_S2 → S2 → S3. "The spectrum of this stage in solid-state LMBs is much broader".
- 검증 `[인쇄]`: "Although current research offers **limited examples of CSP empirical model validation**, several studies have demonstrated promising
  trends44,45." — ref 44 = Naik … Mukherjee 2024 *AEM*(제목 "Interrogating the role of stack pressure in transport–reaction interaction in the
  solid-state battery **cathode**"), ref 45 = Spencer Jolly 2019(**Na**/Na β″-alumina). `[해석]` Li LMB 의 CE–P 측정이 아니다(D3).
- ★ **측정법** `[인쇄]`: "By **continuously measuring the Coulombic efficiency** values of batteries while **gradually increasing the stack pressure**, the
  **minimum stack pressure that yields the highest Coulombic efficiency** can be identified as the CSP empirical model for a given battery system. In
  addition to fixed stack pressure, dynamic stack pressures (such as **25 MPa SSE/Li interfacial formation pressure before reducing to 5 MPa for
  cycling**)36 and multiple-step protocols can also be derived from the CSP empirical model."
- `[인쇄]` "determining the CSP for each type of battery requires systematic studies because this value is **system specific**."

## Stack pressure spatial distribution (p. 1070)

- `[인쇄]` "The distribution of stack pressure is spatially inhomogeneous across the cell, influenced by factors such as surface roughness, non-uniform
  lithium deposition/dissolution, **dead lithium accumulation** and the pressurization device." · 이상적 장치 = "conformal, **constant**, spatially uniform and
  self-adaptive" — 공압 · 에어백 · 실리콘 폼 · 압축 스프링[36,38,48] · 유체 등방 홀더[49] · 3D 미세패턴 SSE[50].

## Future directions (pp. 1070–1071)

- 네 과제: benchmark · diagnosis · spatial homogeneity · optimization (Fig. 6).
- 진단 `[인쇄]`: "In LIBs, dP/dQ can serve as a **high-precision indicator** for monitoring real-time health status. Battery operation can therefore be
  dynamically regulated adaptively from the feedback of stack pressure".
- 균일도 `[인쇄]`: "Stack pressure is a dynamic quantity that varies temporally and spatially." 식 (2)(3) + "A σ² value of **<3%** indicates greater
  uniformity." (§"균일도 지표")
- ★ **요구치** `[인쇄]`: "The emerging trend towards reducing or eliminating stack pressure is driven by practical considerations (**typically requiring a
  pressure of <0.1 MPa**). Stack pressures up to hundreds of MPa, as seen in many current studies, are impractical due to technical challenges, high
  manufacturing costs and safety hazards … Future studies should focus on elucidating the relationship between stack pressure and various **failure
  modes**." — 저압 수단 넷(유동 · 변형 계면 · 전극 구조 · 응력 관리 · 고탄성 유연 부품)에 [52] Pan 2024 *Nat. Commun.*(무외압 μ-Si SSB).

## Conclusion (p. 1071)

- 새 명제 0. `[인쇄]` "incorporating the CSP model as a design descriptor is imperative" · "considering the material tolerance to stack pressure is important".

# 어휘 집계 — NFKC 정규화 후, 대소문자 구분, 낱말 경계 (본문 · 캡션 | 참고문헌 | 그림 안 글자 — 글꼴로 분리)

**정규화 전후 차이**: 본문 글꼴에서 NFKC 가 바꾼 문자 **19 자**(가는 공백 U+2009 18 · `µ` 1), 그림 · 참고문헌 쪽 20 자(합자 `ﬀ` 6 — Fig. 5 축
"Coulombic eﬀiciency" · Fig. 2 "Diﬀusion" — 가는 공백 13 · `″` 1). 열 값은 정규화 뒤 기준.

| 지문 열 | 본문 · 캡션 | 참고문헌 | 그림 글자 | 메모 |
|---|---:|---:|---:|---|
| `identifiab` | **0** | 0 | 0 | `identif*` 2 = "we identify a threshold" · "can be identified as the CSP" — 식별성 뜻 0 |
| `uncertaint` | **1** | 0 | 0 | "These uncertainties surrounding stack pressure" — 일반어 |
| `confidence interval` | 0 | 0 | 0 | |
| `Bayes` | 0 | 0 | 0 | |
| `posterior` | 0 | 0 | 0 | |
| `calibrat` | 0 | 0 | 0 | |
| `LLI` | 0 | 0 | 0 | |
| `LAM` | 0 | 0 | 0 | |
| `degradation mode` | 0 | 0 | 0 | `failure modes` 1(향후 과제 문장) |
| `contact loss` | **0** | 0 | 0 | 양극 문단은 "detachment" · "disengagement" 로 적혀 지문에 안 잡힌다 |
| `MPa` | **15** | 0 | 19 | 요구치 인쇄는 `<0.1` 한 번 |

추가 열(본문 · 캡션): `pressure(s)` 188 · `stack pressure(s)` 150 · `operating` 4 · `fabrication` 1 · `Coulombic efficienc*` 19 · `CSP*` 20 · `empirical` 11 ·
`void(s)` 23 · `contact(s)` 11 · `interfac*` 25 · `detach*/disengag*` 3 · `fatigue` 3 · `creep` 6 · `crack*` 6 · `fractur*` 2 · `fluctuat*` 2 · `constant` 1 ·
`dynamic*` 4 · `dP/dQ` 5 · `threshold(s)` 7 · `optimal` 9 · `benchmark*` 8 · `uniform*` 9 · `statistic*` 3 · `model*` 12 · `validat*` 1 · `simulat*` 1 ·
`decoupl*` 1 · `distinguish*/differentiat*` 2 · `capacit*` 4 · `impedance` 1 · `resistance` 2 · `degradation` 4 · `cathode(s)` 3 · `active material(s)` 4 ·
`isolated` 1 · `inactive` 1 · `dead lithium` 1 · `SEI/solid electrolyte interphase` 1 · `sensor(s)` 1 · `current densit*` 7 · `LMB(s)` 27 · `SSE(s)` 22 ·
`LIB(s)` 6 · `SSB(s)` 4 · **0 인 것**: `EIS` · `OCV` · `hysteres*/histor*` · `indium/In-Li` · `reference electrode` · `error(s)` · `temperature`(오타 `temperate` 1) ·
`load cell`(그림 글자 2).

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/59** | `contact loss` 0 · 양극 쪽 "detachment" 한 문단(수치 0) — 핵심 명제 "Stack pressure minimizes this effect" **인용 0**, 앞 문장 [17] = 23호 Koerver 2017(운전 64/70 MPa 고정 · `[인쇄]` "no additional solid electrolytes can fill the emerging voids", 23호 digest). Fig. 2d = 통째 고립의 압력 복원 모식(`[해석]` `ε_p` 자리 그림). CSP 단계 S1 의 "better interfacial contact" 는 CE 로만 말한다 |
| **Q2** 독립 관측 | **없다 — 1차 측정 0** · 층 하나: **압력 = 진단 채널 처방** | `[인쇄]` "a preliminary basis for differentiating between normal and harmful states" · "In LIBs, dP/dQ can serve as a high-precision indicator" — 모드를 **가르는** 용도 0 · 검출 성능 0(G8) · ASSB 양극 예 0 |
| **Q3** 라벨 층위 | 칸 없음 · **층 하나: "literature-aggregate, unpaired + concept curve"** | Fig. 1b = 문헌 압력 29 점(원자료 있음, 그림 점과 불일치 — D1) · Fig. 5a/b = CE · 압력 **주변 분포**(짝 미공개, 원자료 미수령 — G3) · Fig. 5c = 눈금 없는 곡선인데 이름이 "empirical model". 오차 · 불확실성 0 |
| **Q4** 유일성·식별성 | **0/59 — 쉰한 번째 성질 "압력 효과를 '독립적으로 떼기 어렵다' 고 인쇄하고, 처방한 벤치마크는 CE 한 스칼라의 최대다"** | `[인쇄]` "challenging to decouple the stack pressure effect independently" · 측정법 `[인쇄]` "the minimum stack pressure that yields the highest Coulombic efficiency". `identifiab` 0 · `hysteres*/histor*` 0 — 오름 분기 하나(5호 이력 무시) |
| **Q5** Li-In 기준 | **해당 없음** | `indium` · In-Li 0 · 기준극 0 (원자료 출처 제목 하나에 "Li-In/Sn anodes" — 음극) |
| **Q6** 압력 | **칸 이동 없음 — 층 넷** | ① 요구치 **일곱 번째 인쇄 `<0.1 MPa`**(인용 0) → 인쇄 띠 0.1–5 MPa · 원전 0 · **"≈1–5 MPa 독립 수렴" 반박** ② 제조 ↔ 운전 **명시 분리**(`[인쇄]` "~100–500 MPa … specifically focuses on operating stack pressures") — 33호에 이은 두 번째 종설 층 분리 ③ **문헌 운전 압력 원자료**(xlsx 29 점 · 27 편, 계보 첫 수록; 그림 점은 어긋남) ④ **CSP 개념 곡선** — 아래 벽(S0/S1) · 평탄(S2) · 위 벽(S3)을 CE 한 곡선으로, 수치 0 · 이력 0. + 위 벽 피로의 하중 = **요동**(`[인쇄]` "fluctuations … at the MPa level", [39] = 5호 — 5호 digest 에 그 명제 없음) ↔ 13호 "high, constant" |
| **Q7** dead Li | **칸 이동 없음 — 층 하나** | `[인쇄]` "accumulation of residual solid electrolyte interphase and isolated lithium would gradually increase the baseline stack pressure, but this non-routine variation cannot be accurately correlated with specific electrochemical reactions"[31] — **압력 기저선 = SEI + 고립 Li 의 합, 분리 불가를 저자가 인쇄**(원전 Kim 2020 *JPS* 미열람) · "≥20 MPa … reduce the formation of inactive lithium"[12,13] |
| **Q8** 화학·OCP | **없음** | 양극 화학 0 · OCP · OCV 0. 전기화학 축은 CE 하나 |

# ★ Q6 — 요구치 계보 일곱 번째 인쇄값, 그리고 "≈1–5 MPa 독립 수렴" 판정

카드(13호 Status Log 항)가 적은 실측: **"압력 요구치 ≈1–5 MPa 가 종설 셋에서 원전 셋으로 독립 수렴"** — 종설 셋 = 8 · 12 · 13호, 원전 셋 =
Xu 2024(8호) · Tian/Shao(12호) · 13호의 인용([23] · [35] · [45] — 13호 digest 대조표 표기). 이 편이 그 [23] 이다.

| 편 | 요구치 | 근거 층위 | 원전 |
|---|---|---|---|
| 8호 Li 2026 | < ≈1 MPa | 재인용 | Xu 2024 (확인 편 0) |
| 12호 Kouhestani 2022 | 0.4–1 MPa | 재인용 (모델 최적) | Tian & Qi 2017 / Shao 2022 (미확정) |
| 13호 Zheng 2026 | < 5 MPa | 1 차 주장 | [35] Li Menglin *AFM* 2025 · [45] Zhang *Nat. Commun.* 2025 (미열람 — [45] 는 이번 묶음 파일 22) |
| 25호 Zhou 2025 | ≤ 5 MPa | 인용 없음 | — |
| 33호 Zhang 2025 | < 2 / ≤ 2 MPa | 인용 없음 ("To our knowledge") | — |
| 39호 Sakka 2022 | 1 MPa ("upper limit … practically") | 인용 | Wang · Kazyak · Dasgupta · Sakamoto *Joule* 2021 (미열람) |
| **59호 Li Q. 2025 (이 편 = 13호 [23])** | **< 0.1 MPa** ("practical considerations") | **인용 없음** | — |

**판정: ❌ 반박 — 무관이 아니다.** 같은 물음(실용 운전 압력 요구치)에 **다른 자릿수**로 답한다.

1. **이 편은 1–5 MPa 를 요구치로 인쇄하지 않는다.** 요구치는 `<0.1 MPa`(인용 0), SSB 실험실 필요치는 "several to hundreds of MPa" · "at least 20 MPa" ·
   "above 10 MPa". 5 MPa 가 나오는 곳은 인용 프로토콜 "25 MPa … before reducing to 5 MPa for cycling"[36] 한 번이다. 그리고 `[인쇄]` "0.1 to a few MPa"
   는 이 편 지도에서 **액체 LMB** 대역이다(Fig. 1b 원자료 0.69–1.4 MPa).
2. **"정본 후보" 는 원전이 아니다.** 이 편 자체가 Perspective 이고 요구치에 인용이 없다 — 원전 층이 아니라 **일곱 번째 종설 층 인쇄값**이다.
3. ⇒ 계보는 **일곱 편 · 여섯 값(0.1 · 0.4–1 · ≈1 · 1 · 2 · 5) · 확인된 원전 0**. 인쇄 띠가 0.4–5 MPa(×12.5)에서 **0.1–5 MPa(×50)** 로 넓어진다 —
   "자릿수 수렴" 은 ≈1.7 자릿수 산포가 된다. "원전 셋" 중 지금까지 **열어 본 유일한 다리([23])가 띠 밖**이고, 나머지(Xu 2024 · Tian/Shao · [35] · [45])는
   미열람이다.
4. 13호 쪽 정정: 13호는 `<5 MPa` 에 [35] · [45] 를 달았고 [23] 을 달지 않았다 — **13호의 오귀속이 아니다.** [23] 을 요구치 원전 줄에 같이 적은 것은
   **우리 13호 digest 대조표**(`raw/`, 불변)다. 이 판정은 카드 · 개념 페이지에 정정 표시로 남긴다.
5. `[해석]` 이 편의 요구치 `<0.1 MPa` 는 자기 원자료의 **LIB 범주(0.01–0.1 MPa)** 와 겹친다 — "실용" 을 **LIB 모듈 수준 압력**으로 정의한 것으로 읽힌다.
   Fig. 1b 의 별표도 `[도표]` ≈0.03 MPa 에 있다.

# 귀속 검사 — 13호가 [23] 에 매단 것

| 13호 `[인쇄]` (13호 digest) | 이 편 | 판정 |
|---|---|---|
| "perhaps most critically for system integration … **mechanical requirement for stack pressure** … [23]" | Fig. 1 · `[인쇄]` "much higher stack pressures, ranging from several to hundreds of MPa in solid-state LMBs, are necessary" · "the implementation of a pressurization system poses a major challenge" | ✅ |
| "new points of mechanical failure, such as **creep, fatigue, and fracture**" | "Excessive stack pressure exacerbates lithium **creep**" · "mechanical **fatigue** in the SSE" · "the SSE may **fracture** into multiple segments" · 집전체 "rupture" | ✅ 셋 다 |
| (13호 §5, 인용 번호 확인 안 됨) "**high, constant** stack pressure can induce … fatigue-driven micro-crack initiation" | 이 편의 피로는 **요동**의 산물 — `[인쇄]` "**fluctuations** in stack pressure at the MPa level can induce mechanical fatigue" · Fig. 4m 캡션 "continued pressure fluctuation" | ⚠ **하중 형태가 반대** — 13호의 이 문장을 [23] 에 거슬러 올릴 수 없다 |
| (13호 §4, 인용 0) 능동 응력 관리 — "apply higher pressure during high-rate cycling … reduce pressure during extended rest periods or as the cell ages" | 이 편은 압력을 **일정하게**("Maintain constant", Fig. 6c "Now 진동 → Future 평평") 두고 압력 **신호로 운전을 조절**("Battery operation can therefore be dynamically regulated adaptively from the feedback of stack pressure") | `[해석]` **제어 방향이 반대** — 이 편의 기구(요동 → 피로)를 받으면 13호의 변조 정책은 피로의 구동 하중을 **늘린다** |

# 인용 대조 — 우리 위키에 원전이 있는 것

| 이 편 명제 | 인용 | 우리 위키 원전 | 판정 |
|---|---|---|---|
| "fluctuations in stack pressure at the MPa level can induce mechanical fatigue in the SSE, leading to crack formation … (Fig. 4m)" | [39] Doux 2020 *AEM* = **5호** | 5호 digest: 압력 스윕 1–75 MPa · 75 MPa 에서 도금 전 단락 + `[인쇄]` "severe cracking of the electrolyte" · 로드셀 계측. `fatigue` · `fluctuat` 명제 **없음**(digest 기준) | ⚠ **확인 안 됨** — 5호가 인쇄한 균열은 **정압 고압**의 것이다. 요동 → 피로는 5호 digest 에 없다(원문 PDF 미보유라 전수 검색 못 함) — D6 |
| "Detachment … creating gaps and **cutting off the lithium transport pathway**" | [17] Koerver 2017 *Chem. Mater.* = **23호** | 23호: 첫 충전 NCM 수축 → "spherical gap" · `[인쇄]` "no additional solid electrolytes can fill the emerging voids" · 운전 64/70 MPa 고정 · 압력 스윕 0 | ✅ 첫 문장 선다 · ❌ 다음 문장 "**Stack pressure minimizes this effect**" 는 23호에 없고 **인용 번호도 없다** — 33호 D1/G4("continuous application of external pressure … reactivation", 인용 0)와 **같은 형태의 두 번째 표본**(D7) |
| 원자료 고체 #7 Koerver 2018 *EES* = **143 MPa** | (본문 인용 아님) | 33호 Table 1: 제조 445 · 운전 **70** MPa (33호 digest) | ⚠ **값 불일치** — 원전 미열람, 다른 셀일 수 있다(D9) |
| 원자료 고체 #2 Doux 2020 *JMCA* 8 = 25 MPa | (본문 인용 아님) | 5호는 Doux 2020 *AEM*(다른 편) | 대조 대상 아님 |

# ★ CSP 벤치마크를 카드의 틀로 — CE 는 무엇을 합치나 (`[해석]`)

CE = Q_dis / Q_ch (사이클당). Li 금속 음극(과잉 Li) 셀에서 CE < 1 을 만드는 것은 적어도 넷이고, 우리 위키에 **ASSB 실측 근거가 셋** 있다:

| CE 결손의 출처 | 카드의 몫 | 우리 위키 근거 |
|---|---|---|
| Li 재고 손실(SEI · 고립 Li) | `LLI` | — (이 편 `[인쇄]` "SEI and isolated lithium … baseline stack pressure" 는 둘을 합친다) |
| 충전 중 고립된 양극 입자(재리튬화 불가) | `θ`(접촉) — 그 사이클 CE 에 한 번 찍히고 이후 용량 손실로 남는다 | 23호 "contact loss should only occur during the initial charge" |
| 누설 · 연성 단락(충전량만 부푼다) | 어느 몫도 아님 | **41호** Nam 2018: 얇은 SE 에서 CE 99.0 → 80–89 % 가 누설 · **52호** Oh 2025: 3 MPa 누적 결손 ≈ Li 재고의 ≈2 배 |
| 상대극 기준 전위 이동(Li-In) | 어느 몫도 아님 | **17호** Yanev 2024: CE 비에 두 이동의 차가 들어간다 |

⇒ **"CE 최대의 최소 압력" 은 이 넷 중 무엇이 압력에 반응했는지 말하지 않는다.** S0 → S1 의 CE 상승이 접촉 복원이 아니라 누설 억제일 수 있고,
S3 의 하강은 이 편 스스로 단락(Fig. 4j · k)을 든다 — 곡선의 양 끝이 **접촉이 아닌 기구**로 설명될 수 있다. 곡선 모양은 카드의 세 몫을 가르지 않는다.

- **측정법은 [[assb-pressure-reapplication-separation-test]] 의 오름 분기 판**이다. 그 페이지의 설계 조건과 대조: D1 사이클 해상 압력 계측(언급 0) ·
  D2 기준셀 이중차분(0) · D3 압력만 바꾸기(원리상 ✓) · D4 제조 ↔ 운전 분리(✓ 인쇄) · **D5 채널별 신고(❌ — CE 하나)**. 그리고 5호 이력
  (처녀 5 MPa 110 Ω ↔ 25 MPa 를 찍고 내려온 5 MPa 50 Ω) 아래서 "최소 압력" 은 **가압 분기와 감압 분기에서 다르다** — 측정법은 가압 분기만 정의한다.
- **원자료 층**: Fig. 5 의 CE 는 적재 · 전류 · 온도 · 셀 형식이 다른 문헌값이고 정규화 0 — 52호에서 조건 간 CE 차 ×≈7 이 면적당 결손으로는 ×≈1.8 이었다.

# 압력 균일도 지표 — 식 (2)(3) 재현 (`[재현]`)

`[인쇄]` 식 (2) `ΔP_norm(x, y) = (P(x, y) − P̄) / (P_max(x, y) − P_min(x, y))` · 식 (3) `σ² = (1/n) Σ_{i,j=1}^{n} (ΔP_norm(x_i, y_j) − overline{ΔP_norm(x, y)})²` ·
"x and y are the row and column of the sensor matrix" · "A σ² value of <3% indicates greater uniformity."

성질 셋(대수): ① **척도 불변** — `P = P̄ + ε·f(x, y)` 면 `ΔP_norm` 이 `ε` 와 무관하다(편차를 ×1000 해도 `σ²` 같음, 수치 확인) ② `P̄` 가 같은 격자의
평균이면 `ΔP_norm` 의 평균은 **정확히 0** — 식 (3) 의 윗줄 항은 0 이다 ③ `1/n` 과 이중합(`i, j = 1…n`)이 겹쳐 `n × n` 격자면 `σ²` 가 점 평균 분산의 `n` 배다
— 어느 쪽인지 정의 없음(G7).

10 × 10 격자 수치 예 (우리 계산):

| 압력 지도 | `σ²` (점 평균 `1/N Σ`) | `σ²` (인쇄 그대로 `1/n Σ_{i,j}`, n = 10) | `<3 %` 판정(점 평균) |
|---|---:|---:|---|
| 한 점만 +0.001 MPa (나머지 5 MPa) | 0.99 % | 9.9 % | "균일" |
| 한 점만 **+10 MPa** | **0.99 %** | 9.9 % | **"균일" — 위와 같다** |
| 절반만 +0.001 MPa | 25 % | 250 % | "불균일" |
| 선형 기울기 5.0 → 5.5 MPa | 10.2 % | 102 % | "불균일" |
| 균일 난수 ±1 MPa | ≈8.5 % | — | "불균일" |
| 정규 잡음 (σ 0.1 MPa) 10 × 10 | ≈4.0 % | — | "불균일" |
| 같은 잡음 32 × 32 | ≈2.4 % | — | **"균일"**(센서 수만 바뀜) |
| 같은 잡음 100 × 100 | ≈1.7 % | — | "균일" |

⇒ `[해석]` 이 지표는 불균일의 **크기**를 보지 않고 분포의 **모양**과 **센서 수**를 본다. 이 편이 `[인쇄]` "worse pressure uniformity conditions make them
susceptible to triggering local side reactions, including dendrite growth, overcharging and thermal runaway" 로 경고한 **국소 핫스팟**을 가장 "균일" 로
판정한다. 우리 쪽(D1 압력 계측 · 합성 truth 압력 입력)에서 이 지표를 쓰지 않는다.

# 곱 축퇴 처방 — 마흔두 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]`)

**적용 불가 — 대상 없음.** 1차 데이터 0, 곱이 설 모델 0(식 (1)은 음극 계면 유속 부등식, 식 (2)(3)은 균일도 지표). 32 · 33호처럼 "대상 없음" 도 한 번으로 센다.

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| 1단계 (16호) | `R` 과 `C` 를 같이 | `EIS` 0 · `impedance` 1(액체 분리막 기공 폐쇄) | ❌ |
| 2단계 (18 · 25호) | 면적을 아는 대조군 | Fig. 2d 모식만(수치 0) | ❌ |
| 3단계-a/b (19호) | `Ea` · `C` 상한 | `temperature` 0(오타 `temperate` 1) | ❌ |
| 4단계 (20호) | 시간 영역 동일 검사 | 0 | ❌ |
| 52호 줄 | 누적 충–방 결손 ↔ Li 재고 상한 | **CSP 가 CE 를 벤치마크 축으로 쓴다 — 이 검사 없이** | ⚠ 선행 검사 누락 |

★ `[해석]` **이 편이 처방에 주는 것은 단계가 아니라 경고 하나다**: 압력 축의 벤치마크 · 분리 시험이 **CE 한 스칼라**로 정의되면, 곱을 가르기 전 단계에서
52호 줄(CE 결손 ↔ Li 재고 상한)과 D5(채널별 신고)가 먼저다 — CE 최대는 접촉 복원 · 누설 억제 · Li 재고 보존을 한 비로 합친다. 처방 표에 경고 행으로 남긴다.

# 보류 결정 (가)(나)(다)(아)(자)(차)(타) — 이 편이 주는 근거 (결정 안 함)

원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 의 항목과 대조. **결정은 사용자 몫이고, 이 편은 어느 항목에도 근거를 주지 않는다.**

| # | 결정 | 이 편 | 근거 |
|---|---|---|---|
| 가 | 29호 Q4 +0.5 유지 | 무관 | 적합 · 공분산 · 율 외삽 0 |
| 나 | 38호 Q2 +0.5 유지 | 무관 | 사이클 해상 활성 질량 · 두 채널 0 |
| 다 | 28호 Bizeray 를 ASSB Q4 분모에 | 무관 | 식별성 방법 0 |
| 아 | 35호 합성 쌍 → Roman 특징 30 개 재계산 | 무관 | ML · 특징 0 |
| 자 | 31호 ICI zenodo `R/k` 면적 소거 검사 | 무관 | ICI · 확산 0 |
| 차 | 23호 PyBaMM 면적 노브 / `j₀` 노브 분리 forward | 수치 근거 0 | `[해석]` 정성 메모 하나: 이 편이 23호를 인용한 Fig. 2d 모식은 **통째 고립**(점선 void 가 입자 전체를 두름)이라 면적 노브도 `j₀` 노브도 아닌 `ε_p` 쪽 그림이다 — 두 노브 사이 선택의 근거가 아니다 |
| 타 | Navidi 2024 digest 재점검 | 무관 | — |

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것, 그리고 인용 · 원자료

| # | 등급 | 내용 |
|---|---|---|
| **D1** | ★★★ | **Fig. 1b 점 ≠ 원자료** — 캡션 "All data points are included in the Source Data Fig. 1" 인데 액체 LMB 점 `[도표]` ≈0.34–2.5 MPa ↔ `[데이터]` 0.69–1.4 MPa(범위 ×7.5 ↔ ×2.0), 고체 LMB 가운데 순위 −25 … −33 %, LIB 가운데 ≤−25 %. 점 개수(7 · 9 · 13)는 맞는다 |
| **D2** | ★★★ | **Source Data 파일 이름표** — 시트명 'Figure 5' ↔ 머리 셀 "Figure. 1b" · 내용 = Fig. 1b. Fig. 5 원자료(캡션 "Source Data Fig. 5")는 받은 파일에 없다 |
| **D3** | ★★★ | **CSP "empirical model" 의 경험 근거** — "Based on our statistical analysis" ↔ Fig. 5 는 CE · 압력 **주변 분포**뿐(짝 그림 0) · Li 범주가 액체/고체 미분리 · Fig. 5c 눈금 0 · "validation" 인용 [44] = 양극 압력 **모델** 편(Naik 2024) · [45] = **Na**/β″-alumina(Spencer Jolly 2019) — Li LMB 의 CE–P 측정이 아니다 |
| **D4** | ★★ | **인용 기준 `P/I > 25 MPa cm⁻² mA⁻¹`**(SSE/양극 계면, [27]) — 단위 부호 오류(P/I 는 MPa cm² mA⁻¹). `[재현]` 기준을 받으면 이 편 실용 목표 0.1 MPa 의 허용 전류 **0.004 mA cm⁻²** · 13호 그리드 5 mA cm⁻² 에 **125 MPa** — 이 편은 두 명제를 조정하지 않는다 |
| **D5** | ★★ | **Fig. 3a ↔ 3b 경계** — 같은 (P, i) 경로에서 b 의 경계 ≈8–9 MPa ↔ ≈2.0–2.25 mA cm⁻², a 의 경계는 같은 압력에서 ≈1.1–1.3 mA cm⁻², 경로 위 a 의 경계는 14 MPa. 두 패널 모두 ref 21 재수록 — 원전 미열람 |
| **D6** | ★★ | **5호 귀속** — "fluctuations … at the MPa level … mechanical fatigue in the SSE"[39] ↔ 5호 digest 의 균열은 75 MPa 정압 "severe cracking", `fatigue` · `fluctuat` 명제 없음(digest 기준) |
| **D7** | ★★ | **"Stack pressure minimizes this effect" 인용 0** — 앞 문장 [17] = 23호 Koerver 2017(운전 압력 고정 · "no additional solid electrolytes can fill the emerging voids"). 33호 D1/G4 와 같은 형태 |
| **D8** | ★★ | **균일도 지표 식 (2)(3)** — 범위 정규화로 척도 불변 · 평균항 ≡ 0 · `1/n` + 이중합 모호 · `<3 %` 출처 0. `[재현]` 한 점 +10 MPa 가 "균일"(0.99 %), 센서 수만 늘려도 판정이 뒤집힌다 |
| **D9** | ★ | **Koerver 2018 *EES* 운전 압력** — 이 편 원자료 143 MPa ↔ 33호 Table 1 70 MPa(원전 미열람) |
| **D10** | ★ | **"0.1 to a few MPa in liquid-state LMBs"** ↔ 원자료 최소 0.69 MPa · **"several to hundreds of MPa"**(고체) ↔ 원자료 5–400 ✓ — 본문 범위가 원자료보다 넓게 적힌 쪽은 액체 LMB 아래 끝 |
| **D11** | ⚠ | Fig. 4d · e 제목 "Electrode crack" ↔ 그림은 입자 변형만, 균열선 0 |
| **D12** | ⚠ | 오타 · 표기: 서론 "temperate"(temperature) · Fig. 6a "Standardizaton" · Fig. 3c 세로축 "dP/\|dQ\|" ↔ 캡션 · 본문 "dP/dQ" |
| **D13** | ⚠ | Fig. 1b 라벨 "0.35 MPa" 가 ≈0.1 MPa 점 옆 — 원자료 LIB 최댓값 0.1, 0.35 는 본문 "<50 psi" 상한 |
| **D14** | ⚠ | Fig. 5 캡션 "The lack of statistical data on stack pressure for potassium-, zinc-, magnesium-, calcium- and aluminium-based batteries" ↔ 5b 에 K 1 · Zn 2 · Mg 2 점 `[도표]` — "lack" 이 "적다" 의 뜻이면 정합 |

`[해석]` D1 · D2 · D3 은 한 방향이다 — **이 편의 "통계" 는 다시 그린 그림 위에 서 있고, 그 그림이 원자료와 맞지 않으며, 벤치마크 곡선의 원자료는 공개된
파일에 없다.** 수치는 원자료(Fig. 1b 29 점)만 옮긴다.

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. ★★★ **Q6 — "정본 후보" 가 탈락하고 수렴 명제가 반박된다.** 인쇄 요구치 띠 **0.1–5 MPa(×50) · 원전 0**. 이식판(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md`)의
   운전 압력 입력은 **가정**으로 표시해야 한다 — 값의 근거가 되는 원전이 아직 한 편도 없다.
2. ★★★ **CE 스칼라 벤치마크는 카드의 몫들을 합친다** — 압력 최적을 CE 최대로 정의하는 순간 `LLI` · `θ` · 누설(41 · 52호) · 기준 전위(17호)가 한 비가 되고,
   오름 스윕은 이력(5호)을 지운다. 압력 되돌림 분리 시험의 D5(채널별 신고)가 왜 필요한지 보여 주는 **반례형 처방**이다.
3. ★★ **문헌 운전 압력 원자료 29 점**(LIB 0.01–0.1 · 액체 LMB 0.69–1.4 · 고체 LMB 5–400 MPa, 중앙 0.05 · 1.1 · 45) — 범위 확인용. 그림 점은 쓰지 않는다(D1),
   시뮬 편 포함(제목 기준 1).
4. ★★ **위 벽 "피로" 의 하중 형태가 계보 안에서 갈린다** — 59호 "요동"(5호 인용, 확인 안 됨) ↔ 13호 "high, constant"; 제어 처방도 반대(59호 일정 유지 · 신호로 운전 조절 ↔
   13호 율 · 휴지에 따라 압력 변조). [[assb-stack-pressure-operating-window]] 의 두 번째 위 벽은 **하중 형태 미정**으로 둔다.
5. ★ **압력 = 관측 채널** — dP/dQ 도금 문턱(LIB 흑연, ref 32)과 "SEI + 고립 Li → 기저 압력"(ref 31). 주 프로젝트(액체 LLI/LAM) 쪽으로는 Mohtat 2019 셀 팽창과 같은
   **관측 추가** 부류다([[constrained-crb-identifiability]]) — 단 음극 도금 검출용이고 검출 성능 수치 0, 기저선은 SEI 와 고립 Li 를 가르지 않는다(Q7).
6. ★ 균일도 지표 식 (2)(3)은 쓰지 않는다(`[재현]` §"균일도 지표").

# 후속 후보 (원전 우선)

본문 참고문헌 52 편 + 원자료 출처 27 편(겹침 2)에서 우리 축(Q1 · Q6 · Q7 · 관측 추가)에 닿는 것만. **모드 분해 · 식별성 · 기준극을 제목에 단 원전 0.**

| 서지 | ref | 왜 | 축 | 우선 |
|---|---|---|---|---|
| **Zhang W. et al. 2017 *J. Mater. Chem. A* 5, 9929** (저자 전체는 33호 digest 기준: Zhang · Schröder · Arlt · Manke · Koerver · Pinedo · Weber · Sann · Zeier · Janek) | [23] | 원장 ★★★ 지목 3 회(22 · 23 · 33) → **4 회째**. "Stack pressure can mirror electrochemical behaviour" 의 근거 — **이번 묶음 파일 24**(대기) | Q1 · Q6 | ★★★ |
| **Chen M., Xiao, Dong, Fan, Zhang X. 2023 *Acta Mech. Solida Sin.* 36, 65** | [27] | 이 편에서 **양극(SSE/cathode) 계면**에 붙은 유일한 정량 기준 `P/I > 25` — 단위(D4)와 모델 가정 확인 | Q6 · Q1 | ★★★ |
| **Naik, Jangid, Vishnugopi, Dasgupta, Mukherjee 2024 *Adv. Energy Mater.* 15, 2403360** | [44] | "stack pressure in transport–reaction interaction in the solid-state battery **cathode**" — CSP "validation" 인용, 양극 압력 모델(원장의 Naik 2022 *ACS AMI* 와 다른 편) | Q6 · Q1 | ★★ |
| **Yamamoto, Terauchi, Sakuda, Kato, Takahashi 2020 *J. Power Sources* 473, 228595** | 원자료 고체 #11 (75 MPa) | "volume variations under **different compressive pressures** on the performance and microstructure of ASSBs" — 압력 × 미세구조 후보 | Q6 · Q1 | ★★ |
| Feng, Yang, Qi 2022 *J. Electrochem. Soc.* 169, 090526 | [43] | "The **critical stack pressure** to alter void generation at Li/SE interfaces during stripping" — CSP 이름의 원형 후보(음극) | Q6 | ★★ |
| Yan H. et al. 2022 *Adv. Energy Mater.* 12, 2102283 | [21] | Fig. 3a · b 원전 — D5 판정 | Q6(음극) | ★★ |
| Kim S. et al. 2020 *J. Power Sources* 463, 228180 | [31] | 기저 압력 = SEI + 고립 Li "cannot be accurately correlated" 의 원전 — 차분 역학 분석 | Q7 · 관측 추가 | ★★ |
| Huang W. et al. 2022 *Nat. Commun.* 13, 7091 | [32] | dP/dQ 도금 문턱 원전(LIB) — 검출 성능 확인. 주 프로젝트 관측 추가 후보 | 주 프로젝트 · Q2 | ★★ |
| Ham S.-Y. et al. 2023 *Energy Storage Mater.* 55, 455 | [36] | "25 → 5 MPa" 동적 압력 프로토콜 · 완전지 CCD — 형성 ↔ 운전 분기 | Q6 | ★★ |
| Lee C. et al. 2021 *ACS Energy Lett.* 6, 3261 · Lee C. et al. 2024 *Energy Storage Mater.* 66, 103196 | [24] · [48] | 압력 측정으로 Li–SE 계면 진화 · 압력 조절의 전기화학-기계 | Q6 · Q2 | ★ |
| Chen Y.-T. et al. 2023 *Adv. Energy Mater.* 14, 2304327 | [49] | 균일 · 정확한 압력 제어 장치 — D1 계측 | Q6 | ★ |
| Liu X. et al. 2021 *Adv. Energy Mater.* 11, 2003583 | [34] | 미세구조별 Ni-rich 양극의 전기화학-기계 파괴(ASSB) | Q1 | ★ |
| Koerver et al. 2018 *Energy Environ. Sci.* 11, 2142 | 원자료 고체 #7 (143 MPa) | 원장 ★★★ 지목 2 회 — 운전 압력 값 불일치(D9) | Q6 · Q8 | ★ (기존) |
| Pan H. et al. 2024 *Nat. Commun.* 15, 2263 | [52] | 무외압 μ-Si SSB — **파일 22(Zhang 2025 *Nat. Commun.* 16, 1013)와 다른 편**. 이 편은 Zhang 2025 를 인용하지 않는다 | Q6 | ★ |
| Hu X. et al. 2024 *Nat. Rev. Mater.* 9, 305 | [2] | 외압–전기화학 결합 종설 — "제조 ~100–500 MPa" 의 인용처 | Q6 | ★ |
| Albertus et al. 2021 *ACS Energy Lett.* 6, 1399 | [16] | "above 10 MPa … limit practical viability" — 13호 참고문헌에도 "Albertus" 가 있다(13호 digest, 같은 편인지 미확인) | Q6 | ★ |

# 이 digest 가 주장하지 않는 것

- **실용 압력 요구치가 0.1 MPa 라고 하지 않는다** — 일곱 인쇄값 중 하나이고 인용이 없다. 주장은 "계보의 인쇄 띠가 0.1–5 MPa 이고 확인된 원전이 0" 까지.
- **CSP 모양이 틀렸다고 하지 않는다** — 곡선은 개념이다. 주장은 "그 곡선의 종속 변수(CE)가 카드의 몫들을 합치고, 이 편이 보인 통계는 짝을 주지 않는다" 까지.
- **5호가 피로를 말하지 않았다고 단정하지 않는다** — 5호 digest 기준이고 원문 PDF 는 이 세션에 없다.
- **Fig. 3a · 3b 의 불일치를 원전의 오류라고 하지 않는다** — 이 지면에서의 불일치까지다(재수록 과정일 수 있다).
- **Fig. 1b 점 판독값을 원자료 대신 쓰지 않는다** — 화소 판독은 불일치를 보이는 데만 썼다(축 자체가 고르지 않다).
- **Koerver 2018 *EES* 의 운전 압력이 143 인지 70 인지 판정하지 않는다.**

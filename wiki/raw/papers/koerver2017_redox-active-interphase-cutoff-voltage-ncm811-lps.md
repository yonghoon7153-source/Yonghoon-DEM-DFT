---
title: "Koerver R., Walther F., Aygün I., Sann J., Dietrich C., Zeier W.G., Janek J. 2017 — Redox-active cathode interphases in solid-state batteries (J. Mater. Chem. A 5, 22750–22760)"
source_url: local-upload/26._Redox-active_cathode_interphases_in_solid-state_batteries.pdf + 26._Sup_Redox-active_cathode_interphases_in_solid-state_batteries.pdf
source_url_note: "본문 PDF 11 쪽(RSC Paper · 그림 8 · 식 0 · 참고문헌 51 · 초록 그래픽 PDF 에 없음) + ESI PDF 6 쪽(그림 S1–S7 · 표 S8 은 텍스트 층). 그림 자동 크롭 14 장(본문 7 · ESI 7) + 수동 1(Fig. 7 — 8 쪽 캡션 블록이 줄바꿈으로 시작해 자동 추출이 놓쳤다) — 15 항목 전부 봤고, 수치는 PDF 원본 래스터(ESI 는 SMask 가 있어 200 dpi 렌더)에서 축 눈금 적합으로 픽셀 판독했다. 3차 묶음 파일 26 (2차 묶음 큐 번호와 별개 — 큐 22 = 23호 Koerver Chem. Mater. 는 다른 논문). 22호 ref 12 · 42호 ref 2a · 17호 ref 8 의 원전이고 23호([11]) · 62호([21]) · 63호([7]) 를 인용한다. 추출 텍스트에서 µ · 음수 부호 · 위첨자 · fi/fl 합자 소실 — 단위와 부호는 렌더링으로 확인. 원자료는 커밋하지 않는다."
source_doi: 10.1039/c7ta07641j
source_license: "© The Royal Society of Chemistry 2017 — 구독 논문(Paper) · CC 표시 없음. 이 digest 는 인용 · 요약 · 재현 계산만 담는다"
pdf_sha256: e43294fd1217f54b5960a9bd339e147496529607e53db4cdafdba7b3ec19c9c0
si_sha256: 13882b887f9d30a12e8afc9cac12656a42d506963d316866f571d84cd0016fb3
ingested: 2026-09-28
sha256: 99c347aef96a0b979092c88b557741ba3693dc7404a228d1e010941beb523c15
---
# 수집 목적

`assb` 섹션 **64호** — **3차 묶음 파일 26**(3차 묶음 여섯째 편). 3차 묶음의 파일 번호는 2차 묶음 "큐 N" 번호(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d, 큐 1–59)와
**별개**다 — 이 편은 "큐 26" 이 아니다. ⚠ **2차 큐 22 = Koerver 2017 *Chem. Mater.* 29, 5574 = 23호는 다른 논문**이다(같은 제1저자 · 같은 셀 설계 · 이 편의 [11]). 닻은 `questions/assb-contact-loss-vs-lampe.md`.

들어온 경로: 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1) "★★ **Koerver·Walther·Aygün·…·Janek 2017** — *J. Mater. Chem. A* 5, 22750−22760 | 지목 22 · 42 | **2** | Q2 |
산화 계면층 — 곱 축퇴의 **`j₀` 쪽** 원전 (큐 22 Koerver *Chem. Mater.* 와 **다른 논문**)". 지목한 digest 가 이 편에 매단 명제(각 digest 에서 `22750` · `Koerver` 로 grep 해 읽음 — 22 · 42 · 17호의 원문 PDF 는 이 세션에 없다):

| 지목 | 인용 번호 | 매단 명제 (digest 자리) |
|---|---|---|
| **22호** Strauss 2018 | ref 12 | ① 본문(:129–130) `[인쇄]` 무탄소 이유 — 탄소 첨가제가 "cause severe degradation of sulfidic SEs upon cycling" (refs 10–12) ② 후속 표(:574) "★★ 5 — **탄소 첨가제·산화 계면층 — 계면층(j₀) 쪽 원전** \| Q2" |
| **42호** Santhosha 2019 | ref 2a | 후속 표(:374) "원장에 이미 있음(22호) — **서론 인용만** \| Q1" — 명제 전사 0 |
| (지목 수 밖) **17호** Yanev 2024 (Li-In) | ref 8 | 관련 절(:911–912) "17호는 그것을 **interphase formation** 으로만 인용한다(접촉 손실 아님)" |
| (지목 수 밖) **23호** Koerver 2017 *Chem. Mater.* | — | (:559) "이 편이 **가리키지 않는 것**: Koerver 2017 *JMCA* 5, 22750 (같은 해 후속 — 시점상 불가)" — 역방향으로 **이 편 [11] = 23호**(본문 21 회) |

**59–63호의 결과를 이어받는다.** 63호(Zhang 2017 *ACS AMI* — 이 편 [7], 본문 12 회)는 같은 연구망 In | LGPS | LCO 셀에서 EIS 배정("kinetic hindrance" 는 In 쪽 · 중주파 호 = 양극/SE)이
기준극 없는 **배정**임을, 그리고 SOC 축 1단계(`R`·`C` 로 면적형 ↔ 저항형)를 기록했다. 62호(이 편 [21])는 운전 중 압력(≈61.8 MPa 기저)을 기록했다. 이 편은 **양극 계면층(산화 분해층)이
redox-active 하다**는 원전이고, 셀은 **23호와 같은 설계**(NCM811 : β-Li₃PS₄ 70 : 30 · 12 mg · In 박 ∅6 mm · 445 MPa 제조 · ≈70 MPa 운전)다.

이 digest 의 일 (지시):

1. **인용 귀속 검증** — 지목 둘(22 · 42호) + 지목 밖 둘(17 · 23호) + 원장 행이 이 편에 매단 명제를 원문이 실제로 주는가.
2. **(a)** 계면층의 **화학 동정**과 **양**(두께 · 전하 · 저항)이 측정인가 추정인가 · 어떤 셀(양극 · SE · 음극 · 면적 · 적재 · 가압 · 운전 압력)에서인가.
3. **(b)** 계면층이 **용량(전하)을 낸다/먹는다**는 주장 — 그 크기, 카드의 `LLI` · `LAM` 귀속과 CE 해석에 무엇을 바꾸나.
4. **(c)** 곱 축퇴(`j₀` · 접촉 면적) — 계면 저항 성장이 어느 쪽인지 가를 측정(SOC · 사이클 해상 EIS, `R` 과 `C` 동시)이 있나, 63호의 1단계 분류를 이 편 자료에 걸 수 있나.
5. **(d)** 개념 `assb-interphase-vs-contact-loss-attribution` 의 처방에 들어오는 것 · **(e)** Q1(`θ(N)`) · Q5(Li-In 기준).
6. Q1–Q8 · 채움표 64호 행 · 곱 축퇴 처방 마흔일곱 번째 적용 · 보류 (가)(나)(다)(아)(자)(차)(타) 표시(결정 안 함).

> ⚠ **형식 — *J. Mater. Chem. A* Paper 11 쪽(그림 8 · 식 0 · 표 0 · 참고문헌 51) + ESI 6 쪽(그림 S1–S7 · 표 S8 텍스트). 1차 측정 있음** — 정전류 25 사이클(상한 컷오프 넷 × 셀 2) · 충·방전마다 EIS(R · SI 에 C) ·
> 25 번째 뒤 24 h 휴지 EIS · XPS 깊이 프로파일(25 번째 방전 뒤, 집전체 쪽 복합체 면) · in situ XPS(탄소 C65 : β-Li₃PS₄ 복합체, ±10 V). **컷오프당 셀 2 "representative" · 오차 막대 0 · CPE → C 환산식 0.**
> 그림은 전부 래스터 — `[도표]` 값은 PDF 원본 이미지(본문 300 dpi · SI 200 dpi 렌더)에서 축 눈금 픽셀에 선형(S7 은 로그) 적합한 뒤 마커 · 선을 읽었다(§"픽셀 판독").
> 추출 텍스트 층은 µ · 음수 부호 · 위첨자 · "fi"/"fl" 합자를 잃는다(예: "214 mA cm2" = 렌더 "214 µA cm⁻²", "switched to 10 V" = 렌더 "−10 V") — 단위 · 부호는 렌더로 확인했다.
>
> 표기: `[인쇄]` 본문 · 캡션 · SI 명시(그림 안 인쇄 표지 포함) · `[도표]` 그림에서만 읽은 값(`figure-read ≈`) · `[재현]` 지면의 숫자로 우리가 계산 · 대조한 값 · `[해석]` 우리 해석.
> `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **(a) 계면층의 화학 · 양 — 측정인가** | ✅ **화학은 측정 · 양은 거의 없다** | 화학: XPS S 2p 세 성분(PS₄³⁻ 161.4 · P–[S]n–P 162.7 · S⁰ 163.5 eV) + in situ 에서 Li₂S(159.8) — `[인쇄]` 표 S8 표면 at%(4.0 V 66/17/17 · 4.3 V 70/17/13 · 4.6 V 66/20/14 · 5.0 V 42/32/26). **두께 = 식각 시간(6 · 10 · 18 · 32 분)뿐** — `[인쇄]` "the exact determination of the probed depth is experimentally not possible" · "nanometer scale". **전하 0 · 저항 = EIS 한 호(위치 미분리)**. 측정 위치는 **복합체의 집전체 쪽 면 한 곳**(X-선 200 µm) · 컷오프당 셀 1(25 번째 방전 뒤) |
| 셀 | 23호와 같은 설계 | NCM811(BASF, 무코팅) : β-Li₃PS₄ 70 : 30 wt(47 : 53 vol) **12 mg** · `[인쇄]` 10.7 mg cm⁻² · 2.14 mAh cm⁻² (`[재현]` ∅10 mm = 0.785 cm²) · 무탄소 · 분리막 β-Li₃PS₄ 60 mg ≈400 µm · **In 박 0.125 mm ∅6 mm(무 Li)** · 제조 35 kN ≈445 MPa · 운전 **"approximately 70 MPa"** · 0.1 C = 214 µA cm⁻² · 25 °C · 상한 3.4 / 3.7 / 4.0 / 4.4 V vs In(= 4.0 / 4.3 / 4.6 / 5.0 V vs Li) · 하한 2.00 V vs In · **컷오프당 셀 2** |
| **(b) 계면층이 전하를 낸다/먹는다** | ⚠ **정성 한 문장 — 수량 0** | `[인쇄]` "In the end, every redox reaction of the electrolyte in the electrode will add up to the total capacity obtained for each cycle" · Fig. 8 도식(2 Li₃PS₄ → Li₄P₂S₈ + 2 Li⁺ + 2 e⁻ …). `[재현]` 상한: 양극 복합체의 SE 3.6 mg 전부 1 e⁻/PS₄ = **0.54 mAh = 64 mAh g⁻¹_NCM**. in situ(탄소 복합체, 외압 0) `[도표]`+`[재현]` 산화 ≈0.55 mAh(+10 V 3 h) · 환원 ≈0.52 mAh(−10 V, ≈0.1 h 안) — **환원이 무 Li In 에 산화 단계가 넣은 Li(≈0.55 mAh)에서 끊긴다**(상대극 재고 한계와 가역성이 안 갈린다) |
| (b) 카드 귀속 · CE | **덧셈 항 + `LLI` 아닌 CE 결손** | `[해석]` 산화환원 계면층 전하는 겉보기 양극 용량에 곱이 아니라 **덧셈**으로 들어간다(`Q_app = θ·η·Q_mat + Q_SE,rev`) — OCV 적합의 `a_PE` 가 흡수할 수 있다. SE 산화는 Li⁺ 를 SE 에서 음극으로 옮긴다 ⇒ CE 결손의 일부는 **NCM Li 손실이 아니다** |
| **(c) 곱 축퇴 `j₀` ↔ 면적 — 입력** | ★ **있다 — 양극 호 `R`·`C` 를 사이클 축(25) × 충/방 × 컷오프 넷으로 인쇄**(Fig. 4 + S7) | 우리 위키에서 양극 호의 `R`·`C` 를 사이클마다 인쇄한 첫 편으로 읽힌다(카드 63호 행 "사이클 축 R·C 0" · 18호는 두 상태 · 43호는 음극). **원전은 `C` 를 해석 0** — 가르는 것은 우리다 |
| (c) 우리 판독 (전제 `C ∝ 면적`) | **노화분 = 저항형 · 가역 SOC 분 = 컷오프에 따라 갈림 · 4.0 V 호는 정체 불명** | `[도표]`+`[재현]` 사이클 축: 4.6 V `R` ×4.5–4.9 · `C` ×1.04 · 5.0 V `R` ×4.9–5.5 · `C` ×1.9–2.0(**오른다**) ⇒ **저항형**(면적 손실이면 `C` ×0.2) / SOC 축(충 ÷ 방): 4.6 V `R` ×1.50 · `C` ×0.73–0.83 · τ ×1.10–1.24(**면적형 쪽**) · 5.0 V `R` ×2.3–2.5 · `C` ×0.95–0.98 · τ ×2.2–2.4(**저항형**) · 4.0 V `R` ×0.20 · `C` ×0.64–0.70(부호 반대, 둘 다 아님) / **4.0 V "양극 호" 의 `C` 0.1–0.85 mF = 다른 셀의 ×250–700 = 음극 호 자릿수** |
| (c) 63호 1단계 분류 적용 | ✅ 걸린다 — SOC 축은 **두 점**(충 · 방)뿐, 대신 **사이클 축**이 붙는다 | 63호(SOC 10 점, 한 충전)와 달리 이 편은 같은 SOC 두 점을 25 번 준다 ⇒ **노화분과 가역분을 같은 호에서 따로** 분류할 수 있다 — 23호(상태축) · 63호(SOC 축 뒤 절반)와 같은 방향(노화분 저항형) |
| **(d) 개념 처방** | 넷이 들어온다 | ① 1단계 **사이클 축** ② **호 정체 검사**(같은 이름의 호의 `C` 자릿수) ③ **위치**(원전 XPS 는 분해를 **집전체 쪽**에 둔다 — 집전체 \| SE 는 Li⁺ 차단 계면이라 `θ` 도 `A·j₀` 도 아닌 자리; 전자 경로면 51호 줄) ④ **EIS 휴지 시간**(25 번째 24 h 휴지 뒤 양극 호 `[도표]` ×1.3–1.9) |
| **(e) Q1** | **없다 — `θ(N)` 0/64** | `contact` 6 회 — 셀 관련 둘은 자기 인용([11] 23호 · [21] 62호) · 접촉 측정 0. 층 하나(우리 판독): 4.6 V 가역 SOC 분의 면적형 서명 — "충전 수축 → 가역 접촉 호흡" 과 양립 |
| **(e) Q5** | **층 하나 — 스물일곱 번째 형태** | `[인쇄]` "The In/InLix-anode delivers a constant potential (0.6 V vs. Li/Li+)25" — **[25] = Zaghib 1999**(23호가 **LTO 1.55 V** 에 단 편 · 3차 묶음 파일 32) · 음극 쪽 SE 안정의 실험 근거 [22][39] 는 **Li₄Ti₅O₁₂** 음극 · LF 배정의 대칭셀 근거 [7] = 63호 S14(**무 Li In**) · 전압 그림은 전부 "vs Li" 환산 축. `[재현]` 무 Li In ∅6 mm 첫 충전 끝 14–22 · 첫 방전 끝 7.5–9.9 at% Li(42호 창 안) · In 면 0.59 mA cm⁻²(조건 (6) ×6). 기준극 0 |
| **22호 ref 12 "탄소 → severe degradation upon cycling"** | ⚠ **부분** | 이 편 셀은 무탄소이고 `[인쇄]` "conductive carbon is known to promote side reactions.29,30" 로 **스스로 2차 인용**한다. 탄소 증거는 in situ XPS(탄소 : SE 25 : 75 · 외압 0 · ±10 V 3 h — 무전류 혼합만으로 "small amounts of oxidized species") — **탄소 첨가 셀의 사이클 0** |
| **22호 후속 표 · 원장 "계면층(j₀) 쪽 원전"** | ⚠ **절반** | "산화 계면층의 원전" ✅(화학 · SOC 의존 · 컷오프 의존). "`j₀` 쪽" 은 ⚠ — 원전 낱말에 `j₀` · 면적 · 곱 0, **원전의 위치 판정은 집전체 쪽**(CAM 쪽은 "minor but steady"), 노화분 저항형은 **SI `C` 의 우리 판독** |
| **42호 ref 2a** | **판정 불가** | 42호 digest 에 명제 전사 0 · Santhosha 원문 PDF 이 세션에 없음 |
| (밖) **17호 ref 8 "interphase formation"** | ✅ | XPS 깊이 · in situ 모두 계면층 형성 |
| **Q4** | **0/64 — 쉰여섯 번째 성질** | "같은 이름의 호(`R_cathode/SE`)를 컷오프 넷에 걸쳐 비교하면서 그 정전용량이 ×250–700 다른 것을 묻지 않고, 부호가 컷오프로 뒤집히는 SOC 의존을 한 기구(계면층 산화환원)로 읽었다" |
| **곱 축퇴 처방 마흔일곱 번째** | ★★ **부분 적용 — 1단계 사이클 축 통과(4.6 · 5.0 V 노화분 저항형) · SOC 축은 컷오프마다 갈림 · 3단계-b 4.0 V 탈락 · 4단계 대용 판정 불가** | 아래 §곱 축퇴 |
| **보류 (가)(나)(다)(아)(자)(차)(타)** | **근거 0 — 결정 안 함** | (차)에 정성 메모 하나(§보류) |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | Redox-active cathode interphases in solid-state batteries |
| 저자 (7) | **Raimund Koerver**ᵃᵇ, Felix Walther, Isabel Aygün, Joachim Sann, Christian Dietrich, **Wolfgang G. Zeier**\*, **Jürgen Janek**\* (전원 ᵃᵇ) |
| 소속 | ᵃ Institute of Physical Chemistry, Justus-Liebig-University Giessen · ᵇ Center for Materials Research (LaMa), JLU Giessen |
| 서지 | *J. Mater. Chem. A* **5**, 22750–22760 (2017) · doi `10.1039/c7ta07641j` · Paper · © The Royal Society of Chemistry 2017 — **구독 논문(CC 표시 없음, 첫 쪽 "Licence and permissions")**; 이 digest 는 인용 · 요약 · 재현 계산만 담는다 |
| 일정 | 접수 2017-08-30 · 승인 2017-10-05 · 게재 2017-10-05 — `[재현]` 접수 → 승인 **36 일**. 23호(2017-06 게재)의 넉 달 뒤. PDF 메타: title 동일 · author "Raimund Koerver" · 생성 2017-11-02 · 수정 2026-03-17(재저장). ESI 메타: author "Wenbo Zhang"(63 · 62호 제1저자) · 생성 2017-08-30(= 접수일) · 수정 2017-10-05(= 승인일) |
| 자금 · COI | `[인쇄]` BASF SE (International Network for Electrochemistry and Batteries) · R. K. — Kekulé scholarship (Funds of the Chemical Industry) · "The authors declare no competing financial interests." · 초록 그림에 Dr Bjoern Luerben 감사 |
| 분량 | 본문 PDF 11 쪽(1,843,424 B) — 그림 **8** · 식 0 · 표 0 · 참고문헌 **51** · 초록 그래픽은 PDF 에 없음(1 쪽 래스터는 RSC 로고) |
| ESI | PDF 6 쪽(1,010,396 B) — 그림 **S1–S7** · 표 **S8**(텍스트 층 있음) · 참고문헌 0 |
| sha256 | 본문 PDF `e43294fd1217f54b5960a9bd339e147496529607e53db4cdafdba7b3ec19c9c0` · ESI PDF `13882b887f9d30a12e8afc9cac12656a42d506963d316866f571d84cd0016fb3` — 호출자 명시값과 **일치** |
| 서지 대조 | 호출자 "Koerver R., Walther F., Aygün I., Sann J., Dietrich C., Zeier W.G., Janek J." — PDF 첫 쪽 · ESI 첫 쪽 일치 |
| `[해석]` 자기 인용 | 51 편 중 Janek 이 저자인 편: [1] Janek & Zeier 2016 · [7] Zhang W. 2017(= 63호) · [11] Koerver 2017(= 23호) · [18] Wenzel 2016 *Chem. Mater.* · [21] Zhang W. 2017(= 62호) · [28] Wenzel 2016 *SSI* · [30] Zhang W. 2017 *ACS AMI* 9, 35888 · [33] Dietrich 2016 · [46] Wenzel 2017 · [49] Dietrich 2017 — **10 편** |
| ⚠ 동명 주의 | **23호 Koerver 2017 *Chem. Mater.* 29, 5574**(= 이 편 [11] · 2차 큐 22) — 같은 제1저자 · 같은 셀 설계 · **다른 논문**. 3차 묶음 파일 22 = 60호 Zhang 2025 와도 무관 |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | ★★★ **셀 산포 0** — `[인쇄]` "Two cells per chosen cut-off voltage were investigated, and the data shown here are representative of all collected data" · 어느 셀인지 · 둘째 셀 값 · 오차 막대 · 적합 ± 0 | 컷오프 사이 차이(특히 4.3 ↔ 4.6 V)가 셀 간 산포보다 큰지 모른다 |
| G2 | ★★★ **CPE → C 환산식 · α 0** — S7 은 `C` 만 준다. 방법 · 식 · CPE 지수 인쇄 0 | 우리 1단계 판독(§(c))이 환산식에 걸린다. 63호는 SI 에 환산식을 인쇄했다 — 이 편은 안 했다 |
| G3 | ★★★ **계면층의 양 0** — 두께는 식각 시간(6 · 10 · 18 · 32 분)뿐, 식각 속도 · nm 환산 0(`[인쇄]` "not possible"); 계면층의 **전하 0**; 저항은 EIS 한 호(위치 미분리) | 카드 (b) 의 크기를 이 편에서 얻을 수 없다 — 상한만 `[재현]` |
| G4 | ★★★ **위치 분리 0** — XPS 는 복합체의 **집전체 쪽 면** 한 점(200 µm, 식각 분화구 2 × 2 mm²) · 분리막 쪽 · 단면 0. EIS 는 집전체 \| SE 와 CAM \| SE 를 한 호(`R_cathode/SE`)로 합친다 | "j₀ 쪽" 인가 "집전체 층" 인가가 이 편 안에서 안 갈린다(§(c)) |
| G5 | ★★ **깊이 프로파일의 대조 시편 0** — 미사이클 복합체 · 무전류 복합체의 식각 프로파일 없음. Ar⁺ 식각 자체의 손상 대조 0 | 40 분 평탄(`[도표]` PS₄ ≈86–89 %)이 "minor but steady decomposition" 인지 식각 · 혼합 인공물인지 — 23호 `[인쇄]` 신품 ≈96 % 와 대조하면 ≈7–11 %p |
| G6 | ★★ **운전 압력** — `[인쇄]` "a reduced pressure of approximately 70 MPa was applied" — 장치 · 유지 방식(정하중/정변위) · 측정 0. 셀 케이스 "manufactured in our workshop" | 23호의 "5 kN (64 MPa)" ↔ "≈70 MPa"(23호 D3)와 같은 계열의 한 값 |
| G7 | ★★ **In 음극 재고 · 조성** — 순수 In 박(무 Li) · `[인쇄]` "approx. capacity = 7.7 mA h cm⁻²"(23호 D17 과 같은 값 — `[재현]` In → LiIn 21.3 mAh cm⁻² 의 36 %, 기준 불명) · ∅6 mm = 양극 면적의 0.36 배 | Q5 조건 (5)(6) · 17호 함정 |
| G8 | ★★ **in situ XPS 의 전하 · 조건** — 전류 적분 · 전하량 인쇄 0, 측정 스폿(`[도표]` S2b 집전체 가장자리에서 중심까지 ≈0.3 mm) · 측정 전 **Ar 식각 4 분** · 외압 0 · 탄소 복합체(NCM 0) · ±10 V | 전지 양극과 다른 계 — "battery cathode 에서 redox-active" 로 옮기는 다리가 없다(§(b)) |
| G9 | ★★ **EIS 휴지 0** — `[인쇄]` "measured directly after the respective charge and discharge" + 25 번째 뒤 24 h 휴지 한 번. Fig. 3(24 h 뒤) 양극 호가 Fig. 4(직후) 25 번째 값보다 `[도표]` ×1.3–1.9 — 설명 0 | 충/방 차(SOC 의존)와 이완 · 시간 의존이 섞일 수 있다 |
| G10 | ★ **저주파 호(음극 배정)의 추이 0** — Fig. 3d 에서 가장 큰 호(`[도표]` Re 3.0 → 5.6 kΩ, 0.1 Hz 에서 열림)인데 사이클 추이 · 값 인쇄 0; S7 캡션 `C_anode/SE` "~0.3 mF" 한 줄 | "only this thin interphase is responsible for a significant overvoltage"(본문)의 반례 후보(D9) |
| G11 | ★ **NCM 쪽 측정 0** — "> 4.3 V 산소 방출 · 비가역 구조 변화" 는 인용[34,35] 뿐, XRD · 단면 0 | 4.6 · 5.0 V 감쇠의 `LAM_PE` 몫이 이 편에서 0 |
| G12 | ★ **5.0 V "둘째 방전 평탄" 의 전하 · 전위 인쇄 0** | 계면층 전하(덧셈 항)의 유일한 전압 서명 후보인데 크기 0 |
| G13 | ★ **탄소 첨가 셀 0** | 22호 ref 12 명제("upon cycling")를 이 편이 셀로 주지 않는다 |

# 그림 — 자동 14 + 수동 1, 실제로 본 것: 15 / 안 본 것: 0 — 수치는 원본 래스터에서 픽셀로 읽었다

폴더 `raw/figures/koerver2017_redox-active-interphase-cutoff-voltage-ncm811-lps/`(`figures.json` 15 항목). 수동 1: **Fig. 7**(`fig_7_manual_p8.png` — 8 쪽 캡션 블록이 "Fig. 7" 뒤 줄바꿈으로
시작해 자동 추출이 캡션으로 잡지 못했다; 래스터 1314 × 792 의 bbox + 여백 2 pt). 초록 그래픽은 PDF 에 없다(1 쪽 래스터 335 × 226 = RSC 로고, 봤다).
**봤다(15)**: Fig. 1–8 · S1–S7. 표 S8 은 ESI 텍스트 층으로 읽었다. 수치 판독은 크롭 PNG 가 아니라 **PDF 안의 원본 이미지**(Fig. 1 1420 × 735 · Fig. 2 769 × 1000 · Fig. 3 769 × 1115 · Fig. 4 1420 × 600 ·
Fig. 6 1420 × 873 · Fig. 7 1314 × 792; ESI 는 SMask 가 있어 200 dpi 페이지 렌더 — S5 732 × 490 · S7 1154 × 478)에서 했다 — 축 눈금 픽셀에 선형(S7 은 log₁₀) 적합 → 마커 가장자리 · 중심 · 선.
판독 오차 ≈±0.5 mAh g⁻¹(Fig. 2a) · ±0.005 V(2b) · ±0.3 Ω(Fig. 4a · b) · ±1.3 Ω(4c) · ±8 Ω(4d) · S7 ±1 화소 = ±2.4 %(b–d) · ±1.8 %(a).

## `[도표]` Fig. 1 — 컷오프 넷의 충방전 곡선 (봤다)

- 네 패널(a 4.0 · b 4.3 · c 4.6 · d 5.0 V) · 세로축 **"Potential / V vs. Li/Li⁺" 2.5–5.0**(In 기준 값에 0.6 V 를 더한 환산 축 — 원 측정 축은 그림 어디에도 없다) · 가로 0–225 mAh g⁻¹ · 굵은 선 = 첫 사이클 · 가는 선 = 2 · 5 · 10 · 15 · 20 · 25 번째("25th – 2nd" 화살표, 오른쪽 → 왼쪽).
- ⚠ 방전 끝 `[도표]` **≈2.57–2.62 V**(여덟 곡선씩) ↔ 캡션 `[인쇄]` "cycled between **2.7 V** (lower boundary)" ↔ 방법 "discharged … to 2.00 V"(vs In = 2.6 V vs Li) — **그림은 방법과 맞고 캡션이 어긋난다**(D1).
- 첫 충전 끝 `[인쇄]` 121 · 176 · 186 · 200 mAh g⁻¹(본문). (d) 후반 방전 곡선 앞부분 ≈3.5–3.6 V 에 짧은 어깨 — `[인쇄]` "additional plateau in the discharge curve"(크기 인쇄 0, G12). 후반 충전 곡선은 시작 전위가 사이클마다 오른다(5.0 V 25 번째 ≈4.2–4.3 V 에서 시작).

## `[도표]` Fig. 2 — (a) 방전 용량 · (b) 평균 충전 전압, 25 사이클 (봤다)

- (a) 세로 0–140 mAh g⁻¹ · 가로 사이클 1–25 · 네 계열 열린 사각형 · 왼쪽 상자 "first cycle formation". 값은 §픽셀 판독 ①.
  ⚠ 본문 `[인쇄]` "the cell charged to 4.0 V offers a reversible capacity of only **74** mA h g⁻¹"(둘째 사이클) ↔ `[도표]` 둘째 **83.9** · 25 번째 75.4 — **74 는 25 번째 값에 가깝다**(D2).
  본문 "(Fig. 1a–c)"(4.3–5.0 V 셀) ↔ 해당 패널은 1b–d(D13).
- (b) 세로 3.8–4.6 V vs Li⁺/Li · **가로 0–24**(a 는 1–25 — D14) · 열린 원. 4.0 V 3.815 → 3.86 · 4.3 V 3.91 → 4.02 · 4.6 V ≈3.94 → 4.225 · 5.0 V 3.985 → 4.59 V(§①).
  `[인쇄]` 캡션 "The overvoltage increases during the first battery cycles and increases with higher cut-off voltages" — `[해석]` 평균 충전 전압은 **과전압 + 용량 감쇠로 좁아진 창의 이동**의 합이다(고정 상한에서 창이 줄면 평균이 오른다) — 순수 과전압 척도가 아니다(§곱 축퇴 4단계).

## `[도표]` Fig. 3 — 25 사이클 + 24 h 휴지 뒤 방전 상태 Nyquist (봤다)

- (a) 4.0 · (b) 4.3 · (c) 4.6 · (d) 5.0 V · 열린 원 = 측정 · 실선 = (RQ)(RQ)(RQ)(RQ) 적합 · 회색 반원 = `R_SE/Cathode` · 주파수 표지 **3 MHz · 2 kHz · 1 Hz**(회색 점).
- 고주파: 모든 셀이 Re ≈380–420 · −Im ≈130–150 Ω 에서 시작해 ≈500 Ω 로 내려온다(`[인쇄]` `R_bulk` "approximately 450 ohms").
- `[도표]` 회색 호 폭: (b) **≈100 Ω**(527 → 628) · (c) **≈740 Ω**(648 → 1387) · (d) **≈2.3 kΩ**(731 → 3032) · (a) 마커에 가려 판독 불가(작은 호). ⚠ 같은 셀의 Fig. 4 25 번째 방전(직후) 값 79 · 384 · 1417 Ω 보다 **×1.3 · ×1.9 · ×1.6**(D17 · G9).
- ★ (d) **저주파 호가 가장 크다** — `[도표]` Re ≈3.0 kΩ 의 골에서 시작해 0.1 Hz 끝점 Re ≈5.6 kΩ 까지 닫히지 않는다(꼭대기 −Im ≈1.5 kΩ, Re ≈5.3–5.5 kΩ) — 폭 **≥2.5 kΩ**. 음극(In/SE) 배정 호다. (c) 는 ≈1.39 → ≈1.6 kΩ 의 작은 꼬리. 본문은 이 호의 크기를 논의하지 않는다(G10 · D9).
- ⚠ 모든 패널에서 **1 Hz 표지 뒤로 자료가 이어진다** — 방법 "7 MHz to 1 Hz" 와 어긋난다(S6 는 0.1 Hz 까지, D6).

## `[도표]` Fig. 4 — `R_cathode/SE` × 사이클, 충전(채움) · 방전(열림) (봤다) — ★ 이 편의 핵심 그림

- (a) 4.0 V 세로 0–120 Ω · "formation" 상자(1–2 사이클) · (b) 4.3 V 0–100 · (c) 4.6 V 0–600 · (d) 5.0 V 0–3500 Ω. 값은 §픽셀 판독 ②.
- 본문 정합: "decreases from 105 Ω to 58 Ω"(4.0 V 방전) ↔ `[도표]` 105.8 → 58.7 ✓ · "the discharged state has a higher resistance than the charged state"(4.0 V) ✓(×5) · 4.3 V "rather small but well reproducible" ✓(10 사이클 뒤 차 ≤ ±3 Ω) ·
  4.6 · 5.0 V "always higher" after charging ✓.
- 캡션 `[인쇄]` "The difference in the interfacial resistance between the charged and discharged states during cycling suggests a partially reversible redox process that limits ion conduction at the interface."
- `[해석]` **SOC 차의 부호가 컷오프로 뒤집힌다**: 4.0 V 방전 > 충전(×5) ↔ 4.3 V ≈ 같음 ↔ 4.6 V 충전 > 방전(×1.5) ↔ 5.0 V 충전 > 방전(×2.3–2.5). 본문은 넷을 한 기구(계면층 산화환원)로 읽는다(§(c) · Q4).

## `[도표]` Fig. 5 — S 2p 폭포 그림 × 식각 시간 (봤다)

- 네 패널 · 표지 surface · 2 · 4 · 6 · 8 · 10 · 12 · 14 · (끊김) · 40 min(캡션은 "0 to 16 minutes" — 14 뒤 표지 없는 선 1–2 개) · 세 성분 띠: 파랑 P–S⁻⋯Li⁺ 161.4 · 초록 P–[S]n–P 162.7 · 빨강 −S⁰− 163.5 eV(각 2p₃/₂ · 2p₁/₂ 쌍).
- 표면 분해 예시: 5.0 V 에서 빨강(S⁰) 면적이 초록보다 커 보인다 — 표 S8 의 5.0 V 두 열과 방향이 반대(D4). 40 분 스펙트럼은 넷이 거의 같은 모양.

## `[도표]` Fig. 6 — S 조성(at%) × 식각 시간 (봤다)

- 네 패널 · 회색 띠 "current collector"(x −5–0) · "CC-SEI" 표지 · 사각형 PS₄ · 원 P–[S]n–P · 세모 S⁰ · 점선 **6 · 10 · 18 · 32 min**(인쇄 표지 = "계면층 두께" 의 식각 시간 등가). 값은 §⑥.
- `[도표]` 0 분: 4.0 V 66.8 / ≈16.7 / ≈16.7 · 4.3 V 70.0 / 17.6 / 12.5 · 4.6 V 66.0 / 20.5 / 13.9 · **5.0 V 42.5 / 25.9(원) / 31.9(세모)** — 표 S8(42 / **32** / **26**)과 5.0 V 두 성분이 **뒤바뀐다**(D4). 40 분 평탄 PS₄ ≈86–89 · P–[S]n–P ≈9–11 · S⁰ ≈2–5 %.
- 캡션 `[인쇄]` "the thickness of the cathode electrolyte interphase region (at the current collector) is only estimated" · "decomposition at the CC as well as the cathode–electrolyte interphase depends on the upper cut-off voltage". 명칭 "CC-SEI"(양극 쪽에 SEI — D15).

## `[도표]` Fig. 7 — in situ XPS(탄소 C65 : β-Li₃PS₄ 25 : 75) · 전류/전압 (수동 크롭, 봤다)

- (a) 산화: E **+10 V**(빨강) · I(파랑, mA) ≈1.25 → `[도표]` 0.29(0.5 h) · 0.16(1 h) · 0.08(2 h) · 0.05 mA(3 h) · 가로축 **단위 표지 없음**(본문 "3 h"). (b) 환원: E **−10 V** · I ≈−1.8 mA 에서 **−8.0 mA(t ≈0.075 h ≈4.5 분)** 까지 커진 뒤 ≈0.12 h 에 ≈−0.7, 0.2 h 에 ≈0 · 가로 0–0.2 h + 끊김 2.8–3.0 h.
- (c) 준비 상태: 파랑 PS₄ 주 · 초록 · 빨강 작음 · **노랑 Li₂S 작은 봉우리가 이미 있다** ↔ 본문 "Li2S (159.8 eV), which is found in the polarized samples (Fig. 7e)"(D16). (d) 산화 뒤 "shoulder increases"(빨강 · 초록 커짐). (e) 환원 뒤 "shoulder decreases again" · "new shoulder"(노랑 Li₂S ≈160 eV).
- `[재현]` 전류 적분(§⑦): **산화 ≈0.55 mAh · 환원 ≈0.52 mAh**(비 ≈0.95). 본문은 전하를 적지 않는다(G8).

## `[도표]` Fig. 8 — Li₃PS₄ 산화환원 도식 (봤다)

- 가운데 2 PS₄³⁻(파랑) ↔ 위 P₂S₈⁴⁻(S–S 다리, −2 e⁻) → 불균화 → P₂S₇⁴⁻ + S⁰ ↔(±2 e⁻) → 아래 P₂S₆²⁻(모서리 공유) + 2 S⁰(−4 e⁻) · 왼쪽 "Reduced Compound" P₂S₆⁴⁻ **+ S²⁻**(+2 e⁻). 아래 이름표 Li₄P₂S₆ · Li₃PS₄ · Li₄P₂S₈ · Li₄P₂S₇ · Li₂P₂S₆.
- ⚠ `[재현]` 환원 가지: 2 PS₄³⁻ + 2 e⁻ → P₂S₆⁴⁻ + **2** S²⁻ 이어야 S(8 = 6 + 2) · 전하(−8)가 맞는다 — 그림은 S²⁻ **하나**(D18). 본문 "further reduction of Li3PS4 to Li4P2S6 … under Li2S subtraction" 과는 2 Li₂S 로 정합.
- 캡션 `[인쇄]` "Lithium ions are transferred to the counter electrode and elemental sulfur is accumulated at the positive electrode" — ★ 산화 전하가 Li⁺ 를 **음극으로** 보낸다는 도식 자신의 문장(§(b)).

## `[도표]` ESI Fig. S1–S7 · 표 S8 (전부 봤다 · 표는 텍스트)

- **S1** 추출 펠릿 사진(검은 복합체 면 · 흰 테두리 SE) — 크기 · 방향 표지 0. **S2** (a) in situ XPS 시료대: "Steel current collector"(양극 쪽 클램프) · "Composite cathode" · "Indium foil" · "Pt wire" · 노랑 × 측정점 · (b) SXI "FOV: 1000.0 µm" · 200 µm 막대 ·
  점선 = 집전체(CC) 가장자리 · 노랑 원 = 측정 스폿(`[도표]` 지름 ≈200 µm = X-선 빔 · 중심이 가장자리에서 ≈0.3 mm — 200 µm 막대 151 화소로 환산) · 날짜 "8/13/2017". **S3** 측정 모식(metal clamp (CC) · carbon/SE · solid electrolyte · indium foil · adhesive pad · Pt wire (CC)) — **가압 장치 없음**.
- **S4** 신품 β-Li₃PS₄ S 2p: 두 성분(파랑 + 작은 초록) — `[인쇄]` "Two species are needed to provide a sufficient fit" · **정량 0**(23호는 ≈96 at% PS₄ 를 인쇄).
- **S5** CE × 사이클(세로 끊김 50–60 ↔ 94–100 %): `[도표]` 첫 사이클 표지 "4.0 V" 초록 **58.5 %** · "4.3 V" 보라 **52.2 %** · "4.6 V" 자홍 57.5 % · "5.0 V" 주황 63.2 % ↔ 본문 · Fig. 1–2(`[재현]` 4.0 V 52.0 · 4.3 V 58.2 %) — **4.0 ↔ 4.3 V 가 뒤바뀐다**(D3).
  이후: 4.0 V 94.8(2) → 99.2(15) → 98.4 %(25) · 4.3 V 95.9 → ≈99.0 → 98.7 · 4.6 V 96.5 → 98.6 → 98.2 · 5.0 V 93.9 → 95.5–98.4 흩어짐 → 96.1. 캡션 "Cells cycled to 4.0 and 4.3 V are cycled stable above 98 %"(4.0 V 는 5 사이클까지 <98 %).
- **S6** Bode: (a) 위상 — 4.0 · 4.3 V 는 10¹–10⁵ Hz 에서 **−2 … −4°** 로 평탄(양극 호가 거의 안 보인다) · 4.6 V 최소 ≈−20°(≈3 × 10² Hz) · 5.0 V ≈−33°(≈1.5 × 10² Hz) + 저주파 ≈−17°(≈0.3 Hz) · 가로 **10⁻¹–10⁷ Hz**(자료 0.1 Hz 부터 — D6);
  (b)(c) |Z| — 0.1 Hz 에서 4.0 V ≈720 · 4.3 V ≈780 · 4.6 V ≈1.6 k · 5.0 V ≈5.7 kΩ; (d) 회로 `R_SE,bulk` · `R_SE,gb` · `R_SE/Cathode` · `R_SE/Anode` 네 (RQ). 캡션 전류 "213 µA/cm²"(본문 214 — D14).
- **S7** `C_cathode/SE` × 사이클(로그 세로): ⚠ **(a) 4.0 V 축 10⁻⁵–10⁻² F ↔ (b)–(d) 10⁻⁸–10⁻⁴ F** — 같은 높이의 패널에 세 자릿수 다른 값(D10). `[도표]` 4.0 V 0.1–0.85 mF · 4.3 V 9.8 µF(1 사이클 방전) → ≈1 µF · 4.6 V 0.4–1.1 µF · 5.0 V 0.22 · 0.49 → 0.95 µF.
  ⚠ (d) 5.0 V **충전(채움) 점은 1 사이클뿐** — 2–25 는 방전 원 아래에 1–2 화소 비켜 가려져 있다(원 아래 가장자리가 두껍다 — §③). 캡션 `[인쇄]` "CSE,bulk ~ 0.05 nF, CSE,grain ~ 0.1 µF and Canode/SE ~ 0.3 mF".
- **표 S8**(텍스트 층) — 집전체 쪽 표면(0 분) at%: `x(P-S-Li)` / `x(P-[S]n-P)` / `x(S0)` = 4.0 V **66 / 17 / 17** · 4.3 V **70 / 17 / 13** · 4.6 V **66 / 20 / 14** · 5.0 V **42 / 32 / 26**. ⚠ 4.6 V 가 4.0 V 와 같다 — 본문 "more severe decomposition at higher voltages (4.6 V and 5.0 V)" 의 4.6 V 쪽은 **표면 조성으로는 서지 않고 깊이(18 분)로만** 선다(D5).

# 픽셀 판독 (`[도표]` 전부 — 원본 래스터 · 축 눈금 적합)

**① Fig. 2 — 방전 용량 (mAh g⁻¹) · 평균 충전 전압 (V vs Li)**

| 사이클 | 4.0 V | 4.3 V | 4.6 V | 5.0 V |
|---|---:|---:|---:|---:|
| 1 | 62.9 | 102.6 | 107.2 | 126.7 |
| 2 | **83.9** | ≈129–130(겹침) | 129.6 | ≈129–130(겹침) |
| 3 | 85.1 | 127.1 | 122.4 | 117.5 |
| 5 | 85.7 | 121.7 | 115.0 | 106.9 |
| 10 | 84.3 | 112.1 | 102.6 | 94.5 |
| 15 | 81.4 | 107.5 | 90.9 | 77.4 |
| 20 | — | 103.4 | 80.6 | 62.6 |
| 25 | **75.4** | 98.5 | 71.6 | 49.3 |
| 25 / 2 | 90 % | 76 % | 55 % | 38 % |
| 첫 CE `[재현]`(인쇄 첫 충전 ÷ 첫 방전 판독) | 52.0 % | 58.3 % | 57.6 % | 63.4 % |
| 평균 충전 전압 1 → 25 (Fig. 2b) | 3.815 → 3.86 (+0.045) | 3.91 → 4.02 (+0.11) | ≈3.94 → 4.225 (+0.29) | 3.985 → 4.59 (+0.605) |

첫 CE 재현은 본문(52 · 58 · 58 · 63 %)과 ≤0.5 %p 로 맞는다. 둘째 방전 − 첫 방전: 4.0 V **+21.0** · 4.3 V ≈+27 · 4.6 V +22.4 · 5.0 V ≈+3 mAh g⁻¹(첫 사이클 결손 58 · 73 · 79 · 73 의 ≈36 · 37 · 28 · 4 %).

**② Fig. 4 — `R_cathode/SE` (Ω), 충전 / 방전** (열린 사각형은 위 · 아래 가장자리의 중점)

| 사이클 | 4.0 V 충 / 방 | 4.3 V 충 / 방 | 4.6 V 충 / 방 | 5.0 V 충 / 방 |
|---|---|---|---|---|
| 1 | 31.0 / **105.8** | 29.2 / 34.3 | 47.1 / 69.9 | 241.9 / ≈172 |
| 2 | 24.4 / **58.7** | 51.9 / 37.7 | 87.3 / 99.4 | 593.8 / 288.3 |
| 3 | 15.2 / 55.2 | 55.4 / 41.0 | 118.2 / 84.7 | 825.7 / 388.8 |
| 5 | 12.7 / 55.0 | 62.9 / 49.8 | 155.7 / 115.5 | 1204.6 / 535.8 |
| 7 | 11.4 / 53.0 | 61.3 / 58.4 | 205.3 / 146.0 | 1483.0 / 628.6 |
| 10 | 10.6 / 52.4 | 67.2 / ≈65.0 | 288.4 / 191.9 | 1800.1 / 729.1 |
| 15 | 12.0 / 52.9 | (겹침) | 401.1 / 261.7 | 2306.5 / 883.7 |
| 20 | 11.1 / 54.9 | 70.2 / 77.2 | 493.6 / 326.0 | 2766.6 / 1123.5 |
| 25 | 10.6 / 56.3 | ≈81(24) / 79.1 | **576.0 / 383.7** | **3246.1 / 1417.3** |

**③ ESI Fig. S7 — `C_cathode/SE`, 충전 / 방전** (4.0 V 는 **mF**, 나머지 µF · 열린 원은 위 · 아래 가장자리 중점 · log 축)

| 사이클 | 4.0 V (mF) | 4.3 V (µF) | 4.6 V (µF) | 5.0 V (µF) |
|---|---|---|---|---|
| 1 | 0.096 / 0.269 | 1.06 / **9.8** | ≈0.58 / 0.58 | 0.22 / 0.57 |
| 2 | 0.259 / 0.379 | 0.61 / 2.04 | 0.96 / 0.43 | ≈0.47* / 0.485 |
| 3 | 0.269 / 0.382 | 0.60 / 1.85 | 0.87 / 1.05 | ≈0.49* / 0.51 |
| 7 | 0.300 / ≈0.40 | 0.76 / 1.01 | 0.85 / ≈1.10 | ≈0.57* / 0.58 |
| 10 | 0.264 / 0.411 | 0.78 / 0.95 | 0.815 / 1.114 | ≈0.625* / 0.640 |
| 15 | 0.212 / ≈0.40 | ≈0.9 / ≈1.1 | 0.825 / 1.087 | ≈0.74* / 0.758 |
| 20 | 0.264 / 0.375 | ≈0.9 / ≈1.1 | 0.876 / 1.10 | ≈0.83* / 0.855 |
| 25 | ≈0.42 / ≈0.39 (23–25 사이클 충전 스파이크 0.85 · 0.57) | (충전 가림) / 1.09 | 0.897 / 1.087 | ≈0.91* / 0.952 |

\* 5.0 V 충전 원은 방전 원 아래로 1–2 화소 비켜 가려져 있어 아래 가장자리로 역산(`C_ch ≈ 0.95–0.98 × C_dis`). 1 사이클 충전 원만 떨어져 보인다.

**④ 파생 — `R·C`(τ) 와 비** (`[재현]`, 전제 없이 산술)

| | 사이클 축(노화분) | SOC 축(충 ÷ 방, 같은 사이클) |
|---|---|---|
| 4.0 V | 방전 3 → 25: `R` ×1.02 · `C` ×1.03 (평탄) · 1 → 2(formation) `R` ×0.555 · `C` ×1.41 · τ ×0.78 | 10 · 20 사이클: `R` ×0.20 · `C` ×0.64–0.70 · τ ×0.13 — τ = 2.8 ms(충) · 21.5 ms(방) ⇒ **7–57 Hz**(본문이 음극에 둔 "10–1 Hz" 대역) |
| 4.3 V | 방전 3 → 7: `R` ×1.42 · `C` ×0.55 · τ ×0.78 / 7 → 25: `R` ×1.35 · `C` ×1.08 · τ ×1.46 | 10 사이클: `R` ×1.03 · `C` ×0.81 · τ ×0.84 |
| 4.6 V | 방전 3 → 25: `R` ×4.53 · `C` ×1.035 · τ ×4.7 / 충전 3 → 25: `R` ×4.87 · `C` ×1.04 · τ ×5.1 | 10 · 15 · 20 · 25: `R` ×1.50 · 1.53 · 1.51 · 1.50 / `C` ×0.73 · 0.76 · 0.80 · 0.83 / **τ ×1.10 · 1.16 · 1.21 · 1.24** |
| 5.0 V | 방전 2 → 25: `R` ×4.92 · `C` ×1.96 · τ ×9.6 / 충전 2 → 25: `R` ×5.47 · `C` ≈×1.9 | 10 · 25: `R` ×2.47 · 2.29 / `C` ≈×0.976 · 0.953 / **τ ×2.41 · 2.18** |

면적형 기준(전제 `C ∝ 면적`, `C` 가 `R` 과 같은 계면): τ 보존 · `C` = 1/`R` 비 — 4.6 V SOC 축의 요구 `C` ×0.67 · 5.0 V ×0.40–0.44 · 4.0 V ×5.0.

**⑤ Fig. 3 — 24 h 휴지 뒤(25 사이클, 방전 상태) 회색 `R_SE/Cathode`** — (b) ≈100 Ω · (c) ≈740 Ω · (d) ≈2.3 kΩ ↔ Fig. 4 25 번째 방전(직후) 79.1 · 383.7 · 1417 Ω ⇒ **×1.27 · ×1.93 · ×1.62**. (d) 저주파 호 Re ≈3.0 → ≥5.6 kΩ(0.1 Hz 에서 열림).

**⑥ Fig. 6 — 0 분 · 40 분 at%** — 표는 Fig. 6 절. 0 분 값은 표 S8 과 4.0 · 4.3 · 4.6 V 에서 ≤1 %p · 5.0 V 는 두 성분이 뒤바뀐 채 ≤0.1 %p.

**⑦ Fig. 7 — 전류 적분** — (a) 파랑 곡선 391 열 추적(0.035–3.02 h) 적분 0.51 mAh + 0 → 0.035 h(≈1.25 → 0.92 mA) ≈0.04 ⇒ **Q_ox ≈0.55 mAh(≈2.0 C)**. (b) 0.017–0.2 h 적분 0.51 + 꼬리 ≤0.01 ⇒ **Q_red ≈0.52 mAh**. 봉우리 −8.03 mA @ 0.075 h(본문 "8.0 mA" ✓) · 시작 −2.1 mA @ 0.02 h.

**⑧ Fig. 1 — 방전 끝 전위** — 네 패널 가장 낮은 곡선 끝 **2.57–2.62 V vs Li**(0.6 V 환산 하한 2.6 V 와 일치, 캡션 2.7 V 와 불일치).

# 절별 해체

## 초록 · 서론 (pp. 22750–22751)

- `[인쇄]` 초록: "we charge solid-state batteries to different cut-off potentials and find the formation of a **redox-active resistive layer in the solid electrolyte, which impedes the conductivity depending on the state-of-charge** of the battery. Using electrochemical impedance spectroscopy as well as depth profiling with X-ray photoelectron spectroscopy we find a **thick passivation layer at the current collector** and decomposition products within the cathode composite. In addition, an in situ electrochemical experiment during X-ray photoelectron spectroscopy shows that the solid electrolyte is redox active at the cathode/solid electrolyte interface in solid-state batteries."
  ⚠ 초록 "**thick** passivation layer" ↔ 본문 "the formed interphase is estimated to have a thickness on the **nanometer scale**" · "This **thin**, but highly resistive, interphase"(D7). ⚠ in situ 실험은 **탄소** 복합체 · 외압 0 · ±10 V 다 — "at the cathode/solid electrolyte interface in solid-state batteries" 는 옮김이다(§(b)).
- `[인쇄]` 서론의 접촉 문장: "it was previously shown that chemo-mechanical volume changes lead to pressure changes or even local contact loss in solid-state batteries.11,21" — [11] 23호 · [21] 62호(62호 digest: 접촉 손실은 **무가압 셀의 추론**).
- `[인쇄]` 가설의 출처: "recent work by Tatsumisago and co-workers on interfacial reactions in the cathode composite suggests a redox activity of the Li3PS4 electrolyte. Similar observations were made by Auvergniot et al. in studying the redox activity of Li6PS5Cl.22,23" · "Han et al. … single material battery".24
- `[인쇄]` 목표 문단: "Surprisingly, the bulk cathode remains unchanged in terms of the chemical composition, and the electrolyte oxidation takes place **predominantly in close proximity to the current collector (CC)**" · "The potential drop at the interface between the current collector and the solid electrolyte induces severe oxidation of the thiophosphate, leading to a less conducting interphase" · "not only the CAM particles have to be coated, but also the interface between the SE and the current collector itself needs to be engineered".

## 실험 (pp. 22751–22752)

- **셀**: "Li–In\|β-Li3PS4\|NCM-811+β-Li3PS4" · NCM-811(BASF) 250 °C 진공 건조 · β-Li₃PS₄(BASF) `[인쇄]` **1.5 × 10⁻⁴ S cm⁻¹** · In 박 "0.125 mm thickness, approx. capacity = 7.7 mA h cm⁻², with a diameter of 6 mm" ·
  `[인쇄]` "The In/InLix-anode delivers a constant potential (0.6 V vs. Li/Li+)25 and also prevents decomposition and side reactions, unlike lithium metal" · "SSB cells were assembled following the previously described procedure.7,11" ·
  분리막 60 mg ≈400 µm · 복합체 12 mg(70 : 30 wt, 47 : 53 vol) "corresponding to an area mass loading of 10.7 mg cm⁻² and an area specific charge of 2.14 mA h cm⁻²" ·
  `[인쇄]` "**This ratio was previously found to provide optimal battery performance for the used material combination and for this fabrication process** … 7,11"(D11) · "No conductive additives were added as NCM delivers sufficiently high electronic conductivity and as conductive carbon is known to promote side reactions.29,30" ·
  "compressed uniaxially at 35 kN … approximately 445 MPa. During electrochemical experiments, a reduced pressure of approximately 70 MPa was applied. Two cells per chosen cut-off voltage".
  `[재현]` 10.7 mg cm⁻² × 0.2 Ah g⁻¹ = 2.14 mAh cm⁻² ✓ · 8.4 mg ÷ 10.7 = **0.785 cm²(∅10.0 mm)** · 35 kN ÷ 0.785 cm² = 446 MPa ✓ · 70 MPa × 0.785 cm² = **5.5 kN**.
- **전기화학**: SP300 · 0.1 C 충전 → 컷오프 · 0.1 C 방전 → 2.00 V · `[인쇄]` "The current density was calculated based on the theoretical capacity of 200 mA h g⁻¹ … and was 214 µA cm⁻²" · 충 · 방전마다 EIS "at the OCV in a frequency range from 7 MHz to 1 Hz applying a 10 mV signal amplitude" · RelaxIS 적합 · "assigned … as previously reported.7,11,31,32" · 25 °C.
  `[재현]` 8.4 mg × 200 mAh g⁻¹ × 0.1 = **0.168 mA** ÷ 0.785 = 214 µA cm⁻² ✓ · In 면(∅6 mm = 0.283 cm²) **0.594 mA cm⁻²**.
- **XPS 깊이**: 25 사이클 방전 뒤 분해 · "fragments of the cathode were measured with a depth profile by argon etching" · PHI5000 VersaProbe II · Al Kα · X-선 200 µm · Ar⁺ 0.5 kV · 분화구 2 × 2 mm² · 통과 에너지 23.5 eV · "All measurements were conducted in one batch".
- **in situ XPS**: SE 100 mg 손 압착 · 윗면에 "20 mg of a composite cathode of 25 wt% carbon and 75 wt% of the sulfide electrolyte" · 아랫면 In ∅6 mm · 탄소 패드 고정 · In 은 Pt 선 · 탄소 쪽은 스테인리스 클램프 · `[인쇄]` "**no external pressure was applied during this experiment**" · SP200 ·
  "SXI was used to select a spot for XPS analysis in close proximity to the top side current collector. Prior to the measurements, the sample was argon etched for 4 min" · "+10 V for a period of 3 hours … switched to −10 V (discharge) for the same period" ·
  "The voltages were selected based on the maximum potential range provided by the potentiometer, in order to induce as much redox changes as possible" · OCV: 처음 **0.61 V** · 산화 뒤 **2.11 V** · 환원 뒤 **0.20 V**.

## 결과 1 — 전지 성능 (pp. 22752–22754) · Fig. 1 · 2 · S5

- `[인쇄]` "The cut-off voltage-dependent capacities in the first charging cycle reach 121 mA h g⁻¹ (4.0 V), 176 mA h g⁻¹ (4.3 V), 186 mA h g⁻¹ (4.6 V) and 200 mA h g⁻¹ (5.0 V)" · "When charged to 4.3 V and 4.6 V, the cells show similar efficiencies of η1 = 58%, with 5.0 V it is slightly higher with η1 = 63%, however, charging to 4.0 V results in a significantly lower first cycle efficiency η1 of 52%" ·
  "In the second cycle cells charged to 4.3–5.0 V … almost identical at approximately 127 mA h g⁻¹. In contrast, the cell charged to 4.0 V offers a reversible capacity of only 74 mA h g⁻¹"(D2) · "The cells charged to voltages above 4.3 V exhibit a strong capacity fading from the third cycle on".
- `[인쇄]` 첫 사이클의 배정: "Our previously described findings on the effect of chemo-mechanical contact loss of the active materials combined with interphase formation **explain** the low first cycle efficiencies for NCM materials … 11" — `[해석]` 23호 원전은 "combination" 을 인쇄하고 **나누지 않았다**(23호 손실 예산 ≳85 % 미배정) — 이 편은 그것을 "explain" 으로 옮긴다.
- `[인쇄]` 고전위 감쇠: "Beyond 4.3 V vs. Li+/Li, NCM materials release oxygen and undergo irreversible structural changes which are represented by enhanced capacity fading.34,35 This adds up to the irreversible oxidative decomposition of the solid electrolyte at the cathode interface" — **두 기구(`LAM_PE` 형 · 계면층) 병치 · 가르는 측정 0**(G11).
- `[인쇄]` "The cell that is charged repeatedly to 5.0 V develops an additional plateau in the discharge curve … we attribute this second discharge plateau to advanced battery degradation."

## 결과 2 — EIS (pp. 22753–22755) · Fig. 3 · 4 · S6 · S7

- `[인쇄]` "Directly after the electrochemical cycling, the recorded spectra showed **scattered data in the low frequency region** (assigned to the indium/SE interface).7,11 Kramers–Kronig tests show that the recorded values exhibit sufficient correlation between Z(Re) and Z(Im) **in the mid-frequency region**" — KK 는 MF 만.
- `[인쇄]` 회로 · 배정: "a reasonable fit consists of four (RQ) elements, in which two (RQ) elements contribute to the mid-frequency process.7,11" · "in accordance with a previously suggested model by Tatsumisago and coworkers as well as by Zhang et al.7,36" · HF = `R_bulk` "approximately 450 ohms" · MF = `R_SE,gb` + `R_cathode/SE` ·
  "The low frequency region is widely accepted to refer to transfer related processes at the interface of the negative electrode (Ranode/SE), in this case the In/LiInx anode, which is **experimentally supported by EIS measurements of symmetric In,LiInx/SE/In,LiInx cells conducted by Oh et al.6,7,37**"(D12 — [7] = 63호 S14 는 **무 Li In** 대칭셀).
- `[인쇄]` 기구: "With progressive decomposition, side products accumulate at the electrochemically active interface. These decomposition products exhibit poor ionic conductivities, which severely hinder the transfer of lithium ions and result in an increased overpotential.14"
- `[인쇄]` SOC 의존: "The reversible behavior of the cathode resistance for all cells suggests redox reactions, which reversibly decrease and increase the resistance across the formed interphase, depending on the SOC. At higher charging voltages, the cathode resistance increases significantly; simultaneously the fraction of the reversible redox process increases as well" ·
  "This reversible resistance, which is particularly large for cells charged to 5.0 V, appears to be responsible for the observed second discharge plateau".
- `[인쇄]` 4.0 V formation: "a beneficial resistance drop during the first cycle … from 105 Ω to 58 Ω and remains constant during further cycles. This interface formation correlates well with the higher discharge capacity in the second cycle of all the NCM-811 batteries" · "As the oxidative SE decomposition is thought to increase the resistance in the charged state, this compensation can be explained by these two counteracting processes".
  `[해석]` 4.0 V 의 **방전 > 충전**(×5) 순서를 설명하는 문장은 없다 — "formation" 은 1→2 사이클의 감소를 설명할 뿐이다. 대안 둘(§(c)): NCM 자체 `R_ct` 의 SOC 의존(고리튬 쪽에서 큼 — 이 편 논의 0) · 호 정체(4.0 V 의 `C` 가 음극 호 자릿수).
- `[인쇄]` 크기: "Rcathode/SE reaches values well above the bulk resistance of the separator".

## 결과 3 — XPS 깊이 프로파일 (pp. 22755–22757) · Fig. 5 · 6 · 표 S8

- `[인쇄]` 전제: "As the electrical potential will exhibit a major drop at the CC/SE interface, the effect of the cut-off voltage needs to be evaluated.38 Furthermore, this potential drop should be spatially extended to the boundary between the CAM particles and the solid electrolyte, as long as the CAM particles are electronically connected to the CC." ·
  "only the cathode side is investigated because theoretical calculations suggest that the SE is electrochemically stable at the anode interface within the applied voltage window.15,16 The stability on the anode side was experimentally shown for **Li4Ti5O12** by interfacial analysis performed by Auvergniot et al. and Wu et al.22,39"(D19).
- `[인쇄]` 배정 모델: 161.4 eV PS₄³⁻ · 162.7 eV P–[S]n–P("as in the P2S7⁴⁻ unit (n = 1) or P–S–S–P type structures (n = 2)") · 163.5 eV "S–S bonds as present in S8" · "The oxidation of Li3PS4 may therefore be described as the polymerization (or oligomerization) of the SE anion species.38,40"
- `[인쇄]` 결과: "For 4.0 V and 4.3 V, the spectrum of the cathode surface is more or less identical" · "the fraction of decomposition products **never reaches zero**, irrespective of depth. In other words, while the majority of decomposition products are found at the CC,41 even far from the CC we find evidence for reaction of the SE at the CAM (NCM-811) interface" ·
  "At etching times of 40 minutes all spectra look identical, which indicates that the bulk SE is rather intact and undergoes only a minor but steady decomposition at the SE/CAM interface" ·
  "The thickness of the decomposition layer at the CC as well as around the CAM particles increases with the increasing upper voltage limit and likely with the cycle number as suggested by our previous work.11" ·
  "Judging from the experimental depth resolution of the XPS, the formed interphase is estimated to have a thickness on the nanometer scale. However, the exact determination of the probed depth is experimentally not possible as the etching spot develops a very smooth crater."
  `[해석]` "around the CAM particles" 는 따로 재지 않았다 — 측정은 집전체 쪽 면의 한 분화구다. 23호는 "no steady decomposition" 도 인쇄했다(23호 A2 · D12) — 이 편은 23호의 두 문장 중 다른 쪽("most formed after first charge" 는 아래)을 한 문단씩 인용한다.
- `[인쇄]` 저항 배정: "**The interphase formed at the CC on the other hand has therefore a significant contribution to the cell resistance.** This thin, but highly resistive, interphase correlates well with the observed potential drop at the electrode interface. As recently shown, the major part of the interphase is developed during the very first charge.11 These XPS data support the assumption that the developed interphase severely decreases the ionic conduction and that **only this thin interphase is responsible for a significant overvoltage during cycling**."
  `[해석]` ★ 집전체 \| SE 는 **Li⁺ 차단 계면**이다 — 양극 반응의 이온 전류는 SE → CAM 으로 흐르고 집전체로 들어가지 않는다. 그 면의 저항층이 셀 저항에 "significant" 하려면 **전자 경로**(CAM \| 집전체 접촉)를 덮거나 집전체 근처 CAM \| SE 에 걸려야 하는데, 이 편은 그 경로를 가르지 않는다(EIS 는 한 호, XPS 는 조성).
  전자 경로라면 51호 Illig(집전체 \| 전극층 전자 접촉 호)의 자리다.
- `[인쇄]` 처방: "Whereas in liquid phase systems, the interface at the current collector is passivated by reactions of the conductive salt,41,43 this concept is not possible for SSBs. A different approach could be the use of a **mixed conductor** in the composite cathode to reduce the area that is affected by the potential drop".

## 결과 4 — in situ XPS · 반응 도식 (pp. 22757–22758) · Fig. 7 · 8 · S2–S4

- `[인쇄]` "Without the application of a current or a potential, mechanical dispersion of the SE with conductive carbon leads to small amounts of oxidized species (compare with ESI Fig. S4)" · "Upon electrochemical oxidation, the shoulder towards higher binding energies increases significantly, indicating the degradation of β-Li3PS4" ·
  "When reversing the current by the application of a negative potential, the shoulder towards higher binding energies decreases again. As already seen in EIS measurements, the oxidative decomposition is not fully reversible. The additional formation of Li2S may explain the remnant interfacial resistance."
- `[인쇄]` 전지로의 다리: "Within the uncertainty of the experimental data, **no binding states matching Li2S were found in the post-mortem analysis of battery cathodes** in the interphase at any time. This indicates that the reducing conditions during cycling are not as harsh as the ones chosen in the XPS in situ electrochemistry experiment." ·
  "In battery cycling, instead of Li2S … the cell resistance is likely to increase due to the formation of highly resistive Li4P2S6 … However, in this XPS experiment, Li4P2S6 was not distinguishable from Li3PS4 … the P 2P signal was not evaluated in detail."
- `[인쇄]` 전류: "During oxidation, the current is initially at approximately 1.2 mA and declines constantly over the 3 hour period … upon reversing the current by application of −10 V, a very sharp reducing current is observed. The current increases within the first few minutes, reaches a maximum at 8.0 mA and then rapidly drops off. The increasing current with constant applied potential translates to an increase in conductivity. This may indicate that the highly resistive reaction products formed during oxidation are converted during reduction to a less resistive species."
  `[해석]` ★ 무 Li In 상대극에서 환원 단계가 넘길 수 있는 Li 는 **산화 단계가 In 에 넣은 만큼**이다 — `[재현]` 적분 산화 ≈0.55 · 환원 ≈0.52 mAh(§⑦)이고 전류가 그 근처에서 무너진다. "급감" 은 산화 생성물 소진과 **상대극 재고 소진** 둘 다와 양립한다(Q5 · 17호 함정).
- `[인쇄]` 도식 · 전하: "Upon oxidation two or more Li3PS4 units are interconnected in a kind of polymerization reaction" · "possible structures developed in two-electron oxidation steps … Li4P2S8 or … Li4P2S7. Via Li2S subtraction from Li4P2S7, the edge-sharing species Li2P2S6 can form in an overall four-electron oxidation" ·
  "In practice, one can expect a large variety of intermediate species … In the end, **every redox reaction of the electrolyte in the electrode will add up to the total capacity obtained for each cycle**. However, the less reversible the redox reactions are the more detrimental the influence of the low conductivity products will be for the battery performance."

## 결론 (pp. 22758–22759)

- `[인쇄]` "Above charging voltages of 4.3 V a significant interfacial resistance evolves that severely impacts the battery performance. Electrochemical impedance spectroscopy shows that the cathode interfacial resistance is partially dependent on the state-of-charge of the battery, corroborating the idea of a redox-active CEI layer.22–24 The redox activity of the formed interlayer has further been verified by applying in situ XPS during electrochemical polarization. Furthermore, depth profiling of the forming interphase reveals that most degradation occurs at the current collector and that the cut-off voltage and the associated potential drop determine the thickness of the degradation layer." ·
  "this work highlights the necessity of appropriate particle coatings as well as the need to design and passivate the current collector".

## 참고문헌 51 편 — 우리 축에 닿는 것

[6] Kato … Kanno 2016 *Nat. Energy* 1, 16030(5 V 둘째 평탄 · LF 근거 중 하나) · **[7] = 63호**(12 회) · **[11] = 23호**(21 회) · [12] Kerman … Chen 2017 *JES* 164, A1731 · [14] Richards 2016 *Chem. Mater.* 28, 266(42호 ref 9) · [15] [16] Zhu, He, Mo 2015 *JMCA* · *ACS AMI* ·
[18] Wenzel … Janek 2016 *Chem. Mater.* 28, 2400(42호 후속 · 62호 [10] · 63호 [20]) · **[21] = 62호**(1 회) · **[22] Auvergniot … Dedryvère 2017 *SSI* 300, 78**(원장 ★ · 23호) · **[23] Hakari … Tatsumisago 2017 *Chem. Mater.* 29, 4768**(7 회 — "redox-active" 가설의 원전) ·
[24] Han … Wang 2015 *Adv. Mater.* 27, 3473 · **[25] Zaghib, Simoneau, Armand, Gauthier 1999 *JPS* 81–82, 300**(In 0.6 V 의 인용 — 23호에서는 LTO 1.55 V) · [29] Ito … Tatsumisago 2017 *JMCA* 5, 10658 · **[30] Zhang W. … Janek 2017 *ACS AMI* 9(41), 35888**(탄소 — 48호 ref 19) ·
[31] Sakuda 2009 *JES* 156, A27 · [32] Ohta 2007 *Electrochem. Commun.* 9, 1486(10호 ref 89 · 63호 [27]) · [33] Dietrich … Zeier 2016 *Chem. Mater.* 28, 8764(Li₄P₂S₆) · [34] Luo … Bruce 2016 *Nat. Chem.* 8, 684 · [35] Li … Dahn 2015 *JES* 162 · [36] Sakuda 2010 *Chem. Mater.* 22, 949(63호 [26]) ·
**[37] Oh, Hirayama, Kwon, Suzuki, Kanno 2016 *Chem. Mater.* 28, 2634**(대칭 In,LiInₓ 셀 EIS) · [38] Sumita, Tanaka, Ohno 2017 *JPCC* 121, 9698 · [39] Wu, El Kazzi, Villevieille 2017 *J. Electroceram.* · [40] Sumita … Ohno 2016 *JPCC* 120, 13332 · [41] Myung, Hitoshi, Sun 2011 *J. Mater. Chem.* 21, 9891 ·
**[42] Stegmaier, Voss, Reuter, Luntz 2017 *Chem. Mater.* 29, 4330**(집전체 전위 강하 계산) · [44] Sang, Haasch, Gewirth, Nuzzo 2017 *Chem. Mater.* 29, 3029 · [49] Dietrich … Zeier 2017 *Inorg. Chem.* 56, 6681.
`[해석]` [41](액체셀 집전체 논문)이 "the majority of decomposition products are found at the CC" 에 붙어 있다 — 이 편 자신의 관측에 남의 액체 문헌을 단 자리(제목 미인쇄라 내용 미확인).

# 어휘 집계 — NFKC · 줄 끝 하이픈 복원, 대소문자 무시 · 약어(EIS · OCV · SEI · CEI · LLI · LAM)는 단어 경계 (본문 · 캡션 | 참고문헌 | ESI 텍스트 층)

| 지문 열 | 본문 | 참고문헌 | ESI | 메모 |
|---|---:|---:|---:|---|
| `identifiab` · `standard deviation` · `±` · `error` | **0** | 0 | 0 | `uncertaint` 1("Within the uncertainty of the experimental data") |
| `LLI` · `LAM`(단어) | **0** | 0 | 0 | |
| `OCV` · `impedance` · `EIS` · `interfacial resistance` | 6 · 14 · 7 · 11 | 0 · 0 · 0 · 0 | 1 · 0 · 0 · 0 | |
| `capacitance` | **1** | 0 | 2 | 본문 1 = ESI 목록 한 줄 — `C` 를 본문이 해석 0 |
| `capacity` | 15 | 0 | 0 | "add up to the total capacity" 1 |
| `contact` · `contact loss` | 6 · 2 | 0 | 1 · 0 | 접촉 손실 둘 다 자기 인용([11] · [11,21]) |
| `pressure` · `MPa` | 5 · **2** | 0 | 0 | 445 · 70 |
| `redox` · `reversib` | 26 · 17 | 0 | 1 · 0 | |
| `current collector` · `potential drop` · `mixed conductor` | 15 · 7 · 1 | 0 | 3 · 0 · 0 | |
| `interphase` · `CEI` · `SEI` · `passivat` | 23 · 3 · 2 · 4 | 0 | 1 · 0 · 0 · 0 | 양극 쪽을 "SEI" 로도 부른다(D15) |
| `decompos` · `oxid` · `reduc` · `Li2S` | 29 · 32 · 16 · 11 | 0 | 0 | |
| `thickness` · `nanometer` · `etch` | 7 · 1 · 16 | 0 | 0 | 두께는 식각 시간 |
| `carbon` | 13 | 0 | 1 | 전지 셀은 무탄소 |
| `symmetric` · `reference electrode` · `three-electrode` | 1 · **0** · **0** | 0 | 0 | 대칭셀 1 = Oh et al. 인용 |
| `exchange current` · `contact area` · `tortuos` · `void` · `crack` | **0** | 0 | 0 | |
| `representative` · `reproduc` · `optimal` | 6 · 1 · 1 | 0 | 0 | "optimal" 1 = 70 : 30(D11) |
| `0.6 V` · `In/InLi` · `indium` · `Li4Ti5O12` | 2 · 3 · 6 · 1 | 0 | 0 · 0 · 1 · 0 | |

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/64** | `contact` 6 회 중 측정 0 · 접촉 손실 2 회 모두 자기 인용. ★ 층 하나(`[해석]`): 4.6 V 가역 SOC 분이 면적형(τ 비 1.10–1.24)으로 읽힌다 — "충전 수축 → 가역 접촉 호흡"(23호 기구)과 양립; 전제 위 · 셀 1 · 측정 아님 |
| **Q2** 독립 관측 | **부분 — ★ 양극 호 `R`·`C` 사이클 축 · 가르는 것은 우리 판독** | EIS 네 (RQ) × 25 사이클 × 충/방 × 컷오프 넷(Fig. 4 + S7) · 24 h 휴지 한 점(Fig. 3 · S6) · XPS 깊이(집전체 쪽 면) · in situ XPS(탄소) — `[도표]`+`[재현]` 노화분 저항형(4.6 · 5.0 V) · 가역분 4.6 V 면적형 / 5.0 V 저항형 · 4.0 V 호 정체 불명. 원전은 `R` 만 해석 · `C` 해석 0 |
| **Q3** 라벨 층위 | **fitted-ECM(± 0 · KK 는 MF 만) + assigned(Sakuda 2010 · 63호 · Oh 2016) + XPS at%(표면 한 점, 표 S8) + 식각 분(nm 0)** | n = 2/컷오프 "representative" · 오차 막대 0 · CPE → C 환산 0 · EIS 휴지 0("directly after") ↔ 24 h 뒤 `R` ×1.3–1.9 · 표 S8 ↔ Fig. 6d 두 열 뒤바뀜(D4) · S5 첫 CE 두 색 뒤바뀜(D3) |
| **Q4** 유일성·식별성 | **0/64 — 쉰여섯 번째 성질** "같은 이름의 호를 컷오프 넷에 걸쳐 비교하면서 그 정전용량이 ×250–700 다른 것을 묻지 않고, 부호가 컷오프로 뒤집히는 SOC 의존을 한 기구(계면층 산화환원)로 읽었다 — 대안(가역 접촉 호흡 · CAM 고유 `R_ct(SOC)` · 호 혼동) 언급 0" | `identifiab` · `uncertaint`(해석 쪽) · `±` 0. 네 (RQ) 중 MF 에 두 개를 겹쳐 둔 적합(`R_SE,gb` + `R_cathode/SE`)에서 4.0 · 4.3 V 는 위상이 ≤4°(S6a) — 두 요소의 분할이 자료에서 거의 정해지지 않는 조건이다 |
| **Q5** Li-In 기준 | **층 하나 — 스물일곱 번째 형태 "영점 0.6 V 의 인용이 LTO 논문을, 음극 쪽 안정의 실험 근거가 LTO 음극을 가리킨다 — 전압 그림은 전부 'vs Li' 환산 축"** | `[인쇄]` "(0.6 V vs. Li/Li+)25" — [25] Zaghib 1999(23호 ref 44 = LTO 1.55 V · 3차 묶음 파일 32) · [22][39] LTO · LF 배정 대칭셀 근거 [7] = 63호 S14(무 Li In, 차단 거동). `[재현]` 무 Li In(25.8 mg = 225 µmol): 첫 충전 끝 **14.4 · 19.7 · 20.6 · 21.8 at%** · 첫 방전 끝(결손이 In 에 남는다는 가정) **7.5 · 9.3 · 9.9 · 9.3 at%** — 42호 창(≈1–47 at%) 안. In 면 0.594 mA cm⁻²(조건 (6) ≲0.1 의 ×6). in situ 환원 전하가 In 재고(≈0.55 mAh = 8.4 at%)에서 끊긴다. 기준극 0 · 전위 측정 0 |
| **Q6** 압력 | **칸 이동 없음 — 층 셋** | ① 제조 35 kN ≈445 MPa · 운전 "approximately 70 MPa"(장치 · 유지 · 측정 0 — 23호 64/70 MPa 와 같은 계열, `[재현]` 5.5 kN) ② **in situ XPS 는 외압 0**(클램프만) — 산화환원 증명이 무가압 · 다른 전극 ③ 압력 스윕 0 |
| **Q7** dead Li · Li 재고 | **해당 없음(In) · 층 하나** | SE 산화 전하는 Li⁺ 를 SE 에서 음극으로 옮긴다(Fig. 8 캡션 "Lithium ions are transferred to the counter electrode") ⇒ CE 결손의 일부는 NCM 의 Li 손실이 아니라 SE 전하 · 무 Li In 이라 CE 는 `LLI` 게이지가 아니다(52 · 60호 줄) · 수량 0 |
| **Q8** 화학·OCP | **층 하나** | NCM811(BASF, 무코팅) · 컷오프 넷 · 첫 충전 121 / 176 / 186 / 200 · 25 번째 방전 `[도표]` 75 / 99 / 72 / 49 mAh g⁻¹ · "> 4.3 V 산소 방출" 인용[34,35] · 5.0 V 둘째 방전 평탄 · OCV 곡선 0 · 전압은 전부 +0.6 V 환산 축 |

# ★ (a) 계면층의 화학 동정과 양 — 측정인가 추정인가

| 항목 | 이 편 | 층위 |
|---|---|---|
| 화학 동정 | S 2p 세 성분(+ in situ Li₂S) · 도식(Fig. 8)의 후보 화합물 Li₄P₂S₈ · Li₄P₂S₇ · Li₂P₂S₆ · Li₄P₂S₆ | ✅ **측정(XPS)** + 후보 화합물은 **가설**(`[인쇄]` "reasonable reaction scheme" · Li₄P₂S₆ 는 "not distinguishable") · P 2p 미평가 |
| 조성(at%) | 표 S8 — 집전체 쪽 **표면(0 분)** 한 점씩 · 5.0 V 만 PS₄ 42 %(나머지 66–70 %) | ✅ 측정 · 셀 1(25 번째 방전 뒤) · 5.0 V 두 열 그림과 뒤바뀜(D4) |
| 두께 | 식각 시간 6 · 10 · 18 · 32 분(Fig. 6 점선) — "nanometer scale" | ❌ **nm 환산 0** — 식각 속도 인쇄 0, 분화구가 "very smooth" 라 깊이 측정 불가라고 스스로 적는다 |
| 위치 | "predominantly in close proximity to the current collector" · CAM 쪽 "minor but steady" | ⚠ **집전체 쪽 면 한 분화구**의 깊이 방향 — 분리막 쪽 · 단면 0. "around the CAM particles" 는 따로 재지 않음 |
| 전하 | "add up to the total capacity" | ❌ **수량 0** — §(b) 의 상한은 우리 계산 |
| 저항 | `R_cathode/SE`(Fig. 4) — 4.6 V 25 사이클 576 / 384 Ω · 5.0 V 3246 / 1417 Ω(`[도표]`) | ⚠ **적합값 · 위치 배정**(집전체 층 + CAM 계면층 + 1 번째 입계 호를 MF 에서 둘로 나눈 적합) — ± 0 |
| `[재현]` 두께 ↔ `C` | 기하 면적 평판 유전층이라면 `d = ε₀ε_r A / C` — 0.785 cm² · `C` 0.5–1.1 µF · ε_r 10 ⇒ **≈6–14 nm**(ε_r 5–30 이면 ≈3–40 nm) | `[해석]` "nanometer scale" 과 같은 자릿수 — 그러나 같은 `C` 를 CAM 실면적(12–18 cm², 23호 `[재현]`)에 두면 부분 접촉 · 수백 nm 층과도 양립 ⇒ **`C` 는 위치를 정하지 못한다** |

⇒ **이 편은 계면층의 "무엇" 은 쟀고 "얼마나" 는 식각 분 · 적합 저항까지만 준다.** 셀은 23호와 같은 설계(NCM811 : β-LPS 70 : 30 · 0.785 cm² · 10.7 mg cm⁻² · In ∅6 mm 무 Li · 445 / ≈70 MPa · 25 °C)이고, 산화환원의 직접 증거(in situ)는 **다른 계**(탄소 : SE · 외압 0 · ±10 V)다.

# ★ (b) 계면층이 전하를 낸다/먹는다 — 크기 · 귀속 · CE

**원전이 준 것** — `[인쇄]` 한 문장("every redox reaction of the electrolyte in the electrode will add up to the total capacity obtained for each cycle")과 도식(Fig. 8: 2 PS₄³⁻ → P₂S₈⁴⁻ + 2 e⁻ … 4 e⁻ 까지 · 캡션 "Lithium ions are transferred to the counter electrode"). **크기 0.**

**우리가 붙일 수 있는 크기** (`[재현]`, 가정 명시):

| 경로 | 크기 | 가정 |
|---|---|---|
| 양극 복합체 SE 전부 산화 — 상한 | 3.6 mg Li₃PS₄(180.0 g mol⁻¹) = 20.0 µmol ⇒ 1 e⁻/PS₄ **0.54 mAh = 64 mAh g⁻¹_NCM** · 2 e⁻/PS₄ 1.07 mAh = 128 mAh g⁻¹ | 복합체 SE 전부 · 분리막 제외 · 도식의 전자 수 |
| 40 분 평탄의 "산화 몫" 을 복합체 전체에 적용 | 23호 신품 ≈96 % ↔ 이 편 ≈86–89 % ⇒ ≈7–11 %p × 64 ⇒ **≈4–7 mAh g⁻¹_NCM** | ⚠ 강한 가정 — 집전체 쪽 면 한 점 · 식각 손상 대조 0(G5) · 신품 기준이 다른 편 · S 원자 분율 ↔ 산화된 PS₄ 단위 분율을 1 : 1 로 둠 |
| in situ(탄소 복합체) | Q_ox ≈0.55 mAh = 복합체 SE 15 mg(83.3 µmol)의 1 e⁻ 산화 2.23 mAh 의 **≈25 %** · Q_red ≈0.52 mAh | 전 셀 전류(용량성 · 음극 반응 포함) · ±10 V · 스폿과 무관 |

- ★★★ **환원 전하는 상대극 재고에서 끊긴다.** 무 Li In 은 산화 단계에서 ≈0.55 mAh(20.5 µmol Li → In 225 µmol 의 8.4 at%)를 받았고, 환원 단계는 그만큼 돌려줄 수 있다 — `[재현]` Q_red/Q_ox ≈0.95 · 전류가 ≈0.1 h 에 무너진다.
  원문의 "partially reversible" 과 "conversion to a less resistive species" 는 이 **재고 한계와 구분되지 않는 설계**에서 나왔다(17호 함정의 in situ 판).
- ★★ **카드 귀속에 바꾸는 것 둘** (`[해석]`):
  ① **덧셈 항** — 산화환원 계면층의 가역 전하는 겉보기 양극 용량에 **곱이 아니라 덧셈**으로 들어간다: `Q_app = θ·η(i)·Q_mat + Q_SE,rev` — 3항 분해([[assb-apparent-capacity-decomposition]]) 밖의 항이다. 평탄 상대극 셀의 OCV 적합은 이 전하를 NCM 곡선의 스케일(`a_PE`)이나 모양으로 흡수할 수 있고, 계면층이 자랄수록 **겉보기 `LAM_PE` 를 줄여 보이게** 한다(방향만, 크기 0). 5.0 V 둘째 방전 평탄이 그 전압 서명 후보다(G12).
  ② **CE 결손 ≠ `LLI`** — SE 산화 전하는 충전 용량에만 들어가고 Li⁺ 를 음극(In)에 쌓는다 ⇒ 무 Li In 셀의 CE 결손은 NCM Li 손실 · 접촉 고립 · SE 전하의 합이다(52 · 60호 줄). 23호 손실 예산의 "계면층 패러데이 몫 ≈4 %" 는 SE 1 % 기준이었다 — 이 편의 상한(64 mAh g⁻¹)은 그 몫이 **원리적으로는 첫 사이클 결손(58–79 mAh g⁻¹)과 같은 자릿수까지** 갈 수 있다는 것까지만 말한다(측정 0).
- ⚠ **첫 방전 결손의 일부는 둘째 사이클에 돌아온다** — `[도표]` 둘째 − 첫 방전 +21(4.0 V) · ≈+27(4.3) · +22(4.6) · ≈+3 mAh g⁻¹(5.0 V), 4.0 V 에서 방전 상태 `R` 105.8 → 58.7 Ω 과 동행(`[인쇄]` "formation") ⇒ 첫 사이클 결손의 **≈28–37 % 는 `η` 형(되돌아옴)** 이다(4.0–4.6 V). 5.0 V 는 되돌아옴이 0 에 가깝다.

# ★ (c) 곱 축퇴 `j₀` ↔ 면적 — 이 편의 `R`·`C` 로 가를 수 있나

**입력이 있다.** Fig. 4(`R`) + S7(`C`) = 같은 호의 `R` 과 `C` 를 **25 사이클 × 충/방 × 컷오프 넷**으로. 원전은 `C` 를 한 문장도 해석하지 않는다(`capacitance` 본문 1 회 = ESI 목록). 아래는 **우리 판독**이고 전제는 16 · 23 · 63호와 같다(`C ∝ 접촉 면적`, `C` 가 `R` 과 같은 계면).

| 축 · 컷오프 | `R` | `C` | τ | 서명 | 원전 서술 |
|---|---|---|---|---|---|
| **사이클 축** 4.6 V (3 → 25) | 방 ×4.53 · 충 ×4.87 | ×1.04 · ×1.04 | ×4.7 · ×5.1 | **저항형** | "more severe decomposition … side products accumulate" |
| **사이클 축** 5.0 V (2 → 25) | 방 ×4.92 · 충 ×5.47 | ×1.96 · ≈×1.9 | ×9.6 · ≈×10 | **저항형(`C` 가 오른다)** | 같음 |
| 사이클 축 4.3 V | 3 → 7: ×1.42 / 7 → 25: ×1.35 | ×0.55 / ×1.08 | ×0.78 / ×1.46 | 앞: `C` 가 면적 예측(×0.70)보다 빨리 준다 / 뒤: 저항형 | "small increase with progressive cycling" |
| 사이클 축 4.0 V (3 → 25) | ×1.02 | ×1.03 | 보존 | 평탄 | "rather stable" |
| **SOC 축** 4.6 V (충 ÷ 방, 10–25) | ×1.50–1.53 | ×0.73–0.83 | **×1.10–1.24** | **면적형 쪽**(요구 ×0.67 · 저항형이면 ×1.0) | "redox reactions, which reversibly decrease and increase the resistance" |
| **SOC 축** 5.0 V (10 · 25) | ×2.47 · ×2.29 | ≈×0.98 · ×0.95 | ×2.4 · ×2.2 | **저항형** | 같음 |
| SOC 축 4.3 V (10) | ×1.03 | ×0.81 | ×0.84 | 차 작음 | "rather small but well reproducible" |
| SOC 축 4.0 V (10 · 20) | **×0.20** | ×0.64–0.70 | ×0.13 | 부호 반대 — 면적형이면 `C` ×5 | "the discharged state has a higher resistance" — 기구 서술 0 |

⇒ `[해석]` **세 층으로 갈린다.**
1. ★★★ **노화분(사이클 축)은 저항형**이다 — 4.6 · 5.0 V 에서 `R` 이 ×4.5–5.5 오를 때 `C` 는 그대로거나 오른다. 전제 위에서 **접촉 면적 손실이 아니다** — 23호(상태축 · 두 셀 다섯 구간 화학형) · 63호(SOC 축 뒤 절반 저항형)와 **같은 연구실 · 세 축 · 같은 방향**이다. 원장의 "`j₀` 쪽" 은 이 판독으로 **노화분에 한해** 선다 — 단 아래 위치 문제로 "`j₀`(CAM \| SE)" 인지 "집전체 쪽 직렬 층" 인지는 안 갈린다.
2. ★★ **가역분(SOC 축)은 컷오프마다 다르다** — 5.0 V 는 저항형(원문의 "redox-active interphase" 와 양립), **4.6 V 는 면적형 쪽**(τ 가 ±10–24 % 안에서 보존) — NCM811 의 충전 수축으로 접촉이 줄었다 방전에 돌아오는 **가역 접촉 호흡**과 양립한다(23호 기구의 가역판). 4.0 V 는 방향이 반대라 둘 다 아니다 — 후보는 NCM 자체 `R_ct` 의 SOC 의존(원문 논의 0)과 아래 호 정체 문제.
   ⇒ **원문의 "for all cells suggests redox reactions" 는 원문 자신의 SI 로 5.0 V 에서만 선다.**
3. ⚠⚠ **4.0 V 의 "양극 호" 는 다른 과정이다** — `C` 0.1–0.85 mF 는 4.3–5.0 V 셀(0.4–1.1 µF)의 **×250–700** · S7 캡션의 `C_anode/SE` "~0.3 mF" 와 같은 자릿수 · τ ⇒ 7–57 Hz(원문이 음극에 둔 "10–1 Hz" 대역). S6a 에서 4.0 · 4.3 V 의 중주파 위상은 −2 … −4° 로 호가 거의 없다.
   ⇒ 4.0 V 의 "formation"(105.8 → 58.7 Ω)과 방전 > 충전 순서가 **양극 계면층의 것이라는 근거가 이 편 SI 에서 약해진다**(호 혼동 가능). S7 이 (a) 만 다른 축(10⁻⁵–10⁻² F)에 그려 이 차이가 눈에 안 띈다(D10).

**63호 1단계 분류의 적용** — 63호는 한 충전 안 10 점(SOC 축)으로 "2상 평탄 면적형 · 고전위 저항형" 을 갈랐다. 이 편은 SOC 두 점(충 · 방)뿐이지만 **같은 두 점을 25 번** 준다 ⇒ 63호가 못 한 **노화분 ↔ 가역분 분리**가 된다. 두 편을 합치면 `[해석]`: 고전위 쪽 저항 성장(63호 뒤 절반 · 이 편 노화분)은 저항형으로 일관되고, 면적형은 **가역 구간**(63호 앞 절반 · 이 편 4.6 V SOC 분)에만 나타난다.

**⚠ 이 판독이 곱을 푼 것은 아니다.** ① `C` 는 CPE 환산값이고 환산식 · α 가 인쇄되지 않았다(G2) — α 가 SOC · 사이클에 따라 움직이면 `C` 비가 흔들린다. ② 전제 `C ∝ 면적` 은 18 · 19호에서 깨졌고 23호에서 한 호만 양성 대조됐다. ③ **위치**: 원전 XPS 는 분해의 주 위치를 집전체 쪽에 두고 EIS 는 그것과 CAM 계면층을 한 호로 합친다 — 집전체 \| 복합체 쪽 층이 전자 경로에 걸린 것이라면 `C` 가 저항과 **다른 면(여집합)** 에 있을 수 있어(51호 줄) 1단계 규칙 자체가 뒤집힌다. ④ 셀 1(컷오프당 2 중 "representative") · 로그 축 픽셀 판독(±1 화소 = ±2.4 %). ⑤ 완전 고립 입자는 호에서 빠진다(판정 밖).

# ★ (d) 개념 `assb-interphase-vs-contact-loss-attribution` 의 처방에 들어오는 것

| 처방 | 이 편이 주는 것 |
|---|---|
| 1. `R`·`C` 를 상태축 위 연속으로 | ★ **세 번째 표본 · 첫 사이클 축**(23호 상태축 · 63호 SOC 축에 이어) — 노화분 저항형 · 가역분 컷오프 의존. 조건: CPE α 인쇄(이 편 0) |
| (새) **호 정체 검사** | 같은 이름의 호를 셀 · 조건 사이에서 비교하기 전에 `C` 자릿수를 본다 — 4.0 V 의 ×250–700(§(c) 3) |
| (새) **위치** | 깊이 XPS(집전체 쪽 면)가 "계면층 = CAM \| SE" 전제를 흔든다 — 분해가 집전체 쪽에 몰리면 `R_cathode` 의 성장은 `j₀`(CAM) · 면적(`θ`) 어느 쪽도 아닌 **직렬 · 전자 접촉 항**일 수 있다. 분리막 쪽 면 · 단면 XPS 와 쌍으로 |
| (새) **SOC 의존의 세 기구** | 계면층 산화환원(저항형) · 가역 접촉 호흡(면적형) · CAM 고유 `R_ct(SOC)`(부호가 SOC 쪽에 따라) — **`C` 가 가른다**(5.0 V · 4.6 V · 4.0 V 가 각각 다른 칸) |
| (새) **휴지 시간** | EIS 직후 ↔ 24 h 휴지 뒤 `R` ×1.3–1.9(`[도표]`) — `R(N)` 을 노화 축으로 쓰려면 SOC 와 휴지를 고정 |
| 5. 코팅 유무 쌍 | 이 편 0(무코팅 NCM) — `[인쇄]` 처방("particle coatings" + "passivate the current collector")만 |

# ★ (e) 카드 Q1 · Q5 에 들어오는 것

## Q1 — `θ(N)`: 없다

접촉을 잰 관측 0. `[해석]` 층 하나 — 4.6 V 의 가역 SOC 분이 면적형으로 읽히면(전제 위), **첫 충전에 한 번 생기고 마는 접촉 손실**(23호 A3 "contact loss should only occur during the initial charge")이 아니라 **매 사이클 되풀이되는 가역 접촉 변화**가 있다는 뜻이다 — `θ` 가 사이클 안에서 SOC 의 함수(`θ(N, SOC)`)일 수 있다. 합성 truth 에 새 요구 후보(카드).

## Q5 — 스물일곱 번째 형태

- **① 영점의 인용이 다른 재료를 가리킨다.** `[인쇄]` "The In/InLix-anode delivers a constant potential (0.6 V vs. Li/Li+)25" — [25] **Zaghib 1999**(23호가 ref 44 로 **LTO 1.55 V** 에 단 편; 제목 미인쇄, 3차 묶음 파일 32 에서 확인). 같은 연구실의 23호는 0.6 V 에 Jung 2015 리뷰(ref 16)를 달았다.
- **② 음극 쪽 SE 안정의 실험 근거가 LTO 다.** `[인쇄]` "theoretical calculations suggest that the SE is electrochemically stable at the anode interface … 15,16 The stability on the anode side was experimentally shown for Li4Ti5O12 … 22,39" — 셀은 In(0.6 V) 이고 인용 실험은 LTO(1.55 V)다. 같은 편 서론은 "quite narrow (thermodynamic) stability windows" 를 적는다(D19).
  `[해석]` In \| SE 쪽 SE 환원이 있으면 그것은 **진짜 `LLI`** 이고, 이 편은 그 가능성을 설계상 보지 않는다(음극 쪽 XPS 0).
- **③ LF 배정의 대칭셀 근거 중 하나가 63호다.** `[인쇄]` "experimentally supported by EIS measurements of symmetric In,LiInx/SE/In,LiInx cells conducted by Oh et al.6,7,37" — [7] = 63호, 그 대칭셀(S14)은 **무 Li In**(차단 거동, ≈1 Hz 호 없음 · 63호 본문 인용 0). 남은 근거는 [37] Oh 2016(미열람) · [6] Kato 2016.
- **④ 무 Li 조립 · 작은 상대극.** `[재현]` In ∅6 mm(양극의 0.36 배) · 첫 충전 끝 14.4–21.8 at% · 첫 방전 끝 7.5–9.9 at%(첫 사이클 결손이 전부 In 에 남는다는 가정) — 42호 평탄 창 안. In 면 전류 0.594 mA cm⁻²(조건 (6) ×6). ⇒ 조건 (1) 은 서고 (6) 은 깨진다.
- **⑤ in situ 판 17호 함정.** 환원 전하(≈0.52 mAh)가 산화 단계가 무 Li In 에 넣은 Li(≈0.55 mAh)에서 끊긴다 — 상대극 재고가 "가역성" 측정을 덮는다.
- **⑥ 전압 그림은 전부 "vs Li" 환산 축**이다(Fig. 1 · 2b) — 원 측정 축(vs In) 그림 0. 하한 2.00 V vs In 은 그림에서 ≈2.6 V 로 보이는데 캡션은 2.7 V(D1).
- ⇒ 계보: … → 공칭 조성 계산(62호) · 창 이탈을 동역학 장애로 명명(63호, 2017-05) · 가정을 명시하고 깨지는 곳을 이름표로 덮음(23호, 2017-06) · **영점과 음극 안정의 인용이 LTO 를 가리킨다(64호, 2017-10)**. 칸 이동 없음(Q5): 전위 측정 0 · 기준극 0.

# 귀속 검사 — 지목 둘 · 지목 밖 둘 · 원장 행이 이 편에 매단 것

| 인용처 | 매단 명제 | 이 편 | 판정 |
|---|---|---|---|
| **22호** ref 12(본문 :129–130, refs 10–12) | 탄소 첨가제가 "cause severe degradation of sulfidic SEs upon cycling" | 전지 셀은 무탄소 · `[인쇄]` "conductive carbon is known to promote side reactions.29,30"(2차 인용) · 탄소 증거는 in situ XPS(C65 : SE · 외압 0 · ±10 V 3 h — 무전류 혼합만으로 "small amounts of oxidized species", +10 V 에서 산화 어깨) | ⚠ **부분** — "탄소 + SE → 산화" 는 in situ 로 서고, "upon cycling" 의 셀 증거는 [29] Ito 2017 · [30] Zhang W. 2017 *ACS AMI* 9, 35888 로 위임 |
| **22호** ref 12(후속 표 :574) | "탄소 첨가제·산화 계면층 — 계면층(j₀) 쪽 원전" | 산화 계면층의 화학 · SOC 의존 · 컷오프 의존 ✅ · 위치 = 집전체 쪽(CAM 쪽 "minor") · `j₀` · 면적 · 곱 낱말 0 · SI `R`·`C` → 우리 판독 노화분 저항형 | ⚠ **절반** — "산화 계면층 원전" ✅ · "`j₀` 쪽" 은 우리 판독이고 노화분에 한함, 위치(집전체 ↔ CAM) 미분리 |
| **42호** ref 2a(:374) | 서론 인용(명제 전사 0) | — | **판정 불가** |
| (밖) **17호** ref 8(:911) | "interphase formation" 으로만 인용(접촉 손실 아님) | XPS 깊이 · in situ — 계면층 형성 | ✅ |
| (밖) **23호** | 인용 0(시점) — **역인용: 이 편 [11] = 23호, 본문 21 회** | 23호의 "combination" 을 "explain" 으로(결과 1) · 23호의 "most formed after first charge"(✅ 인쇄 일치) 와 "likely with the cycle number"(23호는 "no steady decomposition" 도 인쇄 — 23호 D12 의 두 문장을 한쪽씩) · 셀 설계 · XPS 모델 · 산화 관측 | 기록 — 23호가 **가르지 않은 것**을 이 편이 "shown" 으로 받는다 |
| 원장 §1 행 | "산화 계면층 — 곱 축퇴의 `j₀` 쪽 원전" | 위 두 줄 | ⚠ — 정정 제안(wiki 밖): "산화 계면층의 화학 · SOC 의존 · 컷오프 의존 원전 · 원전의 위치 판정은 **집전체 쪽** · `j₀` 쪽은 SI `R`·`C` 의 우리 판독(노화분 저항형 · 가역분 컷오프 의존)" |

# 인용 대조 — 우리 위키 · 원장에 원전 · 관련 digest 가 있는 것

| 이 편 인용 | 우리 호 · 원장 | 이 편이 적은 것 | 대조 |
|---|---|---|---|
| **[7] Zhang W. … Janek 2017 *ACS AMI* 9, 17835** | **63호** | 12 회 — 셀 절차 · "optimal … for the used material combination" · EIS 배정 · "interfacial resistance … increase during the charging process" · LF 대칭셀 근거 | 충전 중 증가 ✅(63호 Fig. 5 R_MF ×2.07) · **"optimal … used material combination" ❌**(63호는 LCO : LGPS · "optimal" 0) · **대칭셀 ❌**(63호 S14 는 무 Li In) |
| **[11] Koerver … Janek 2017 *Chem. Mater.* 29, 5574** | **23호** | 21 회 — 절차 · XPS 모델 · "contact loss … combined with interphase formation explain" · "major part … during the very first charge" · "likely with the cycle number" | 셀 · XPS ✅ · "explain" ⚠(23호는 나누지 않았다) · 두 시간 문장은 23호 내부 충돌(D12)의 양쪽 |
| **[21] Zhang W. … Janek 2017 *JMCA* 5, 9929** | **62호** | "pressure changes or even local contact loss" | 압력 ✅ · 접촉 손실 ⚠(62호: 무가압 셀의 추론) |
| [22] Auvergniot 2017 *SSI* 300, 78 | 원장 ★(23호) | Li₆PS₅Cl 산화환원 · LTO 음극 쪽 안정 | **지목 +1** |
| [25] Zaghib 1999 *JPS* 81–82, 300 | 원장 ★★(23호 — LTO 1.55 V) · 3차 묶음 파일 32 | **In 0.6 V** | 같은 편이 두 연구에서 두 재료의 영점에 달린다 — 파일 32 에서 확인 |
| [18] Wenzel 2016 *Chem. Mater.* 28, 2400 | 42호 후속 · 62호 [10] · 63호 [20] | XPS PS₄ 봉우리 · Li 금속 반응 | — |
| [32] Ohta 2007 · [36] Sakuda 2010 | 10호 ref 89 · 63호 [27] · [26] | EIS 배정 · 코팅 | 같은 편 |
| [14] Richards 2016 *Chem. Mater.* 28, 266 | 42호 ref 9 | 안정 창 | — |
| [30] Zhang W. … Janek 2017 *ACS AMI* 9, 35888 | 48호 ref 19("NMC 초기 경사 = SE 분해(탄소 촉진)") · 원장 0 | 탄소 부반응 | **신규 후보** — 22호 "탄소" 명제의 1차 후보 |

⚠ 이 편(2017-10)은 22호(2018) · 42호(2019) · 17호(2024)를 인용할 수 없다 — 시점. 23호 · 62호 · 63호는 모두 이 편 **앞**(2017-05 – 06)이다.

# 곱 축퇴 처방 — 마흔일곱 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]`)

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | Fig. 4 + S7 — **사이클 축 25 × 충/방 × 컷오프 넷** | ✅ **사이클 축 통과** — 4.6 · 5.0 V 노화분 저항형 · SOC 축 4.6 V 면적형 쪽 · 5.0 V 저항형 |
| **2단계** (18 · 25호) | + 면적을 아는 대조군 | 컷오프 넷 = 전위(화학) 조작 — 면적 대조 아님 · 코팅 쌍 0 | ❌ |
| **3단계-a** (19호) | `Ea` | 25 °C | ❌ |
| **3단계-b** (19 · 20호) | `C` 상한 | 4.3–5.0 V: 0.4–1.1 µF ÷ 0.785 cm² = 0.5–1.4 µF cm⁻²(기하) · CAM 실면적 12–18 cm²(23호 `[재현]`)당 ≈0.02–0.09 µF cm⁻² — 이중층 이하 ✓ · **4.0 V: 0.1–0.85 mF = 실면적당 5–70 µF cm⁻² — 이중층 자릿수 · 음극 호 자릿수** ✗ | ⚠ 4.3–5.0 V 통과 · **4.0 V 탈락(호 정체)** |
| **4단계** (20호) | 시간 영역 동일 검사 | 대용: 평균 충전 전압(Fig. 2b) 증가 ↔ `I·ΔR_ch`(0.168 mA) — 5.0 V +0.605 ↔ +0.505 V(≈83 %) · 4.6 V +0.29 ↔ +0.089(≈31 %) · 4.3 V +0.11 ↔ +0.009 · 4.0 V +0.045 ↔ −0.003 | ⚠ **판정 불가** — 평균 충전 전압은 과전압 + 창 압축 + 다른 호(5.0 V 저주파 ≥2.5 kΩ)의 합 |
| 52호 줄 | 누적 결손 ↔ Li 재고 | 무 Li In — 재고 = 양극이 준 것 + **SE 산화가 준 것** | ⚠ SE 전하가 결손에 섞인다(§(b)) — 검사력 0 |
| (새) 호 정체 | 같은 이름의 호 · 같은 자릿수의 `C` | 4.0 V ×250–700 | ❌ 4.0 V · ⚠ 4.3 V 1 사이클(9.8 µF) |

⇒ **부분 적용 — 1단계를 사이클 축에 건 첫 표본.** 기록 이유 셋: (i) 원장이 이 편을 "`j₀` 쪽 원전" 으로 올린 명제는 원전 문장이 아니라 **SI 의 `R`·`C` 를 우리가 읽을 때** 서고, 그것도 **노화분**에 한한다 (ii) 가역 SOC 분은 컷오프마다 다른 칸(4.6 V 면적형 · 5.0 V 저항형)이라 "redox-active interphase" 한 이름이 두 기구를 덮는다 (iii) **같은 이름의 호가 셀마다 같은 과정인지**(4.0 V `C` ×250–700)를 1단계 앞에 검사해야 한다 — 처방 표 새 줄 후보.

# 보류 결정 (가)(나)(다)(아)(자)(차)(타) — 이 편이 주는 근거 (결정 안 함)

원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 와 대조. **결정은 사용자 몫이다.**

| # | 결정 | 이 편 | 근거 |
|---|---|---|---|
| 가 | 29호 Q4 +0.5 유지 | 무관 | 적합 · 식별성 진단 0 |
| 나 | 38호 Q2 +0.5 유지 | 무관 | 활성 질량 채널 0 |
| 다 | 28호 Bizeray 를 ASSB Q4 분모에 | 무관 | 식별성 방법 0 |
| 아 | 35호 합성 쌍 → Roman 특징 재계산 | 무관 | ML 0 |
| 자 | 31호 ICI zenodo `R/k` 면적 소거 | 무관 | 펄스 · 차단 0 |
| 차 | 23호 PyBaMM 면적 노브 / `j₀` 노브 분리 | **정성 메모 하나** | 23호와 같은 셀 설계에서 노화분은 저항형 · 가역 SOC 분은 컷오프에 따라 면적형(4.6 V) ↔ 저항형(5.0 V) — 두 노브 외에 **SOC 의존 가역 항**과 **집전체 쪽 직렬 항**이 관측에 섞인다는 메모; 결정 재료 아님 |
| 타 | Navidi 2024 digest 재점검 | 무관 | — |

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 어디 | 판정 |
|---|---|---|---|
| **D1** | ★★ 하한 전위 — Fig. 1 캡션 "cycled between **2.7 V** (lower boundary)" ↔ 방법 "discharged … to 2.00 V"(vs In = 2.6 V vs Li) ↔ `[도표]` 곡선 끝 2.57–2.62 V | Fig. 1 캡션 ↔ p. 22751 | 캡션 오기로 읽힌다 |
| **D2** | ★★★ 4.0 V 둘째 사이클 가역 용량 "only **74** mA h g⁻¹" ↔ `[도표]` Fig. 2a 둘째 **83.9** · 25 번째 75.4 | p. 22752 ↔ Fig. 2a | 본문이 25 번째 값을 옮긴 것으로 읽힌다 |
| **D3** | ★★ ESI S5 첫 사이클 CE — "4.0 V" 초록 58.5 % · "4.3 V" 보라 52.2 % ↔ 본문 4.0 V 52 % · 4.3 V 58 % ↔ `[재현]` Fig. 1–2 52.0 · 58.3 % | S5 ↔ p. 22752 · Fig. 2 | S5 첫 점 두 색(또는 표지)이 뒤바뀜 |
| **D4** | ★★ 표 S8 5.0 V `x(P-[S]n-P)` 32 · `x(S0)` 26 ↔ Fig. 6d 0 분 세모(S⁰) ≈31.9 · 원(P–[S]n–P) ≈25.9 · Fig. 5d 분해도 S⁰ 쪽이 크다 | 표 S8 ↔ Fig. 5d · 6d | 표 쪽 두 열 뒤바뀜으로 읽힌다 |
| **D5** | ★★ "the SE undergoes a more severe decomposition at higher voltages (**4.6 V** and 5.0 V)" ↔ 표 S8 표면 4.6 V 66/20/14 ≈ 4.0 V 66/17/17 | p. 22757 ↔ 표 S8 | 4.6 V 는 깊이(18 분)로만 선다 |
| **D6** | ★★ EIS 범위 "from 7 MHz to 1 Hz"(방법) ↔ S6 자료 0.1 Hz 부터 · Fig. 3 모든 패널에서 1 Hz 표지 뒤 자료 | p. 22751 ↔ Fig. 3 · S6 | 24 h 휴지 측정만 넓혔을 가능성 — 서술 0 |
| **D7** | ★★ 초록 "a **thick** passivation layer at the current collector" ↔ 본문 "thickness on the **nanometer scale**" · "This **thin**, but highly resistive, interphase" | 초록 ↔ p. 22756 | |
| **D8** | ★ "The obtained spectra in combination with the current profile for each step are shown in **Fig. 5**" ↔ Fig. 7 | p. 22757 | 그림 번호 오기 |
| **D9** | ★★★ "**only this thin interphase is responsible for a significant overvoltage**" ↔ Fig. 3d 저주파(음극 배정) 호 `[도표]` ≥2.5 kΩ ≥ 양극 호 ≈2.3 kΩ · Fig. 2b 평균 전압 증가의 `I·ΔR_cathode` 몫 4.6 V ≈31 % · 4.3 V ≈8 % | p. 22756 ↔ Fig. 2b · 3d | 셀 전압의 다른 항을 재지 않은 결론 |
| **D10** | ★★ S7 (a) 세로축 10⁻⁵–10⁻² F ↔ (b)–(d) 10⁻⁸–10⁻⁴ F — 같은 높이 패널에 ×250–700 다른 값 · 본문 · 캡션 언급 0 | S7 | 4.0 V "양극 호" 정체 문제를 가린다 |
| **D11** | ★★ "This ratio was previously found to provide **optimal** battery performance **for the used material combination** … 7,11" ↔ [7] 63호 = LCO : LGPS · "optimal" 0 · [11] 23호 조성 시험 0 | p. 22751 ↔ 63 · 23호 | 인용이 명제보다 약하다 — 7:3 계보의 평서문화 |
| **D12** | ★★ LF 배정 "experimentally supported by EIS measurements of symmetric In,LiInx/SE/In,LiInx cells … 6,7,37" ↔ [7] 63호 S14 = 무 Li In 대칭셀(차단 거동, 본문 인용 0) | p. 22754 ↔ 63호 | [37] Oh 2016 미열람 |
| **D13** | ★ "In the second cycle cells charged to 4.3–5.0 V (**Fig. 1a–c**)" ↔ 해당 셀은 Fig. 1b–d | p. 22752 | |
| **D14** | ★ Fig. 2 캡션 "214 µA cm⁻², which corresponds to 0.1C **for the cell charged to 4.3 V**" ↔ 방법 "based on the theoretical capacity of 200 mA h g⁻¹" · S6 캡션 "213 µA/cm²" · Fig. 2b 가로축 0–24 ↔ 2a 1–25 | Fig. 2 ↔ p. 22751 · S6 | |
| **D15** | ★ 명칭 — 양극 쪽을 "SEI formation"(p. 22752) · "SEI forming reaction"(p. 22757) · "CC-SEI"(Fig. 6) 로도 부른다 ↔ "CEI" | 본문 · Fig. 6 | |
| **D16** | ★ Fig. 7c 준비 상태에 이미 노랑 Li₂S 성분 ↔ 본문 "Li2S … which is found in the polarized samples (Fig. 7e)" | Fig. 7 ↔ p. 22757 | |
| **D17** | ★★ Fig. 3(25 사이클 + 24 h 휴지) 회색 `R_SE/Cathode` ≈100 · 740 · 2300 Ω ↔ Fig. 4 25 번째 방전(직후) 79 · 384 · 1417 Ω(×1.3–1.9) — 서술 0 | Fig. 3 ↔ Fig. 4 | 휴지 중 성장 또는 다른 셀(G1 · G9) |
| **D18** | ★ Fig. 8 환원 가지 "P₂S₆⁴⁻ + **S²⁻**" — S · 전하 균형은 2 S²⁻ | Fig. 8 | 도식 오기 |
| **D19** | ★★ "the SE is electrochemically stable at the anode interface within the applied voltage window.15,16 … experimentally shown for **Li4Ti5O12**" ↔ 셀은 In(0.6 V) · 서론 "quite narrow (thermodynamic) stability windows" | p. 22755 ↔ p. 22750 | 인용 실험의 음극이 다르다 |
| 교차 | ★ 23호 D17 "approx. capacity = 7.7 mAh cm⁻²"(기준 불명) 을 그대로 반복 · [25] Zaghib 1999 가 23호에서는 LTO, 이 편에서는 In 영점 | 23호 ↔ 64호 | 같은 연구실 넉 달 차 |

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. ★★★ **양극 호 `R`·`C` 의 사이클 축 판독 — 노화분은 저항형**(4.6 V `R` ×4.5–4.9 · `C` ×1.04 · 5.0 V `R` ×4.9–5.5 · `C` ×1.9). 23호(상태축) · 63호(SOC 축) · 64호(사이클 축) — 같은 연구실 세 축이 같은 방향이다. 원장 "`j₀` 쪽 원전" 은 **이 판독으로 노화분에 한해** 선다.
2. ★★★ **가역 SOC 분은 한 기구가 아니다** — 4.6 V 면적형 쪽(τ ×1.10–1.24) · 5.0 V 저항형(τ ×2.2–2.4) · 4.0 V 부호 반대. 원문의 "redox-active interphase for all cells" 는 원문 SI 로 5.0 V 에서만 선다. RPT 의 EIS 는 같은 SOC · 같은 휴지에서만 노화 축이다.
3. ★★★ **위치 — 원전은 분해를 집전체 쪽에 둔다.** 집전체 \| SE 는 Li⁺ 차단 계면이라 그 층이 셀 저항에 크게 들어가려면 전자 경로에 걸려야 한다 — 그러면 `θ` 도 `A·j₀` 도 아닌 직렬 · 전자 접촉 항(51호 줄)이고 1단계 규칙의 전제(`C` 와 `R` 이 같은 면)가 흔들린다.
4. ★★ **호 정체 검사가 1단계보다 먼저다** — 4.0 V "양극 호" 의 `C` 는 다른 셀의 ×250–700(음극 호 자릿수) · τ 는 음극 대역 — 이 셀의 "formation" 과 방전 > 충전 순서는 양극 것이라는 근거가 약하다.
5. ★★ **산화환원 계면층은 덧셈 항 + `LLI` 아닌 CE 결손** — 상한 64 mAh g⁻¹_NCM(1 e⁻/PS₄, 복합체 SE 전부). OCV 적합의 `a_PE` 가 흡수할 수 있다. in situ 의 "가역성" 은 무 Li In 재고 한계(≈0.55 mAh)와 안 갈린다.
6. ★ **첫 사이클 결손의 ≈28–37 % 는 둘째 사이클에 돌아오는 `η` 형**(4.0–4.6 V) — 첫 사이클 손실을 한 칸(`LLI` 또는 `LAM`)에 두면 과대다.
7. ★ **인용 계보 셋** — 70 : 30 "optimal for the used material combination"(원전은 LCO : LGPS · "optimal" 0) · In 0.6 V 의 인용이 LTO 논문 · LF 대칭셀 근거가 무 Li In.

# 후속 후보 (원전 우선)

참고문헌 51 편 중 우리 축(Q2 · Q5 · Q7)에 닿는 것만. **셀 열화 식별성 원전 0.**

| 서지 | ref | 왜 | 축 | 우선 |
|---|---|---|---|---|
| **Hakari, Deguchi, Mitsuhara, Ohta, Saito, Orikasa, Uchimoto, Kowada, Hayashi, Tatsumisago 2017 *Chem. Mater.* 29, 4768–4774** | [23] | "redox-active interphase" 가설의 원전 — `[인쇄]` 이 편 "Tatsumisago and coworkers previously attributed the interfacial redox chemistry to a partially reversible formation and dissociation of S–S bonds using ex situ XPS measurements on charged and discharged cathodes" · 이 편이 "confirm" 한 대상 · 원장 0 | Q2 · Q7 | ★★★ |
| **Oh, Hirayama, Kwon, Suzuki, Kanno 2016 *Chem. Mater.* 28, 2634–2640** | [37] | LF = In/SE 배정의 **운전 조성(In,LiInₓ) 대칭셀** 근거 — 63호 G3 의 빈칸("운전 조성 대칭셀 0")을 채울 후보 · 원장 0 | Q5 · Q2 | ★★★ |
| **Zhang W., Leichtweiss, Culver, Koerver, Das, Weber, Zeier, Janek 2017 *ACS Appl. Mater. Interfaces* 9(41), 35888–35896** | [30] | 이 편이 "탄소 → 부반응" 을 위임한 원전(같은 연구실) · 22호 refs 10–12 명제의 1차 후보 · 48호 ref 19 · 원장 0 | Q2 | ★★★ |
| **Stegmaier, Voss, Reuter, Luntz 2017 *Chem. Mater.* 29, 4330–4340** | [42] | 집전체 계면 전위 강하 계산 — 이 편 위치 판정("necessarily the highest at the CC interface")의 물리 근거 · 원장 0 | Q2 | ★★ |
| Auvergniot, Cassel, Foix, Viallet, Seznec, Dedryvère 2017 *SSI* 300, 78–85 | [22] | 원장 ★(23호) — **지목 +1** · Li₆PS₅Cl 산화환원 · LTO 음극 쪽 안정 | Q2 · Q5 | ★★(기존) |
| Zaghib, Simoneau, Armand, Gauthier 1999 *JPS* 81–82, 300–305 | [25] | 원장 ★★(23호, LTO 1.55 V) — 이 편은 **In 0.6 V** 의 근거로 인용 · **3차 묶음 파일 32** 에서 In 전위가 실제로 있는지 확인 | Q5 | ★★(기존) |
| Sang, Haasch, Gewirth, Nuzzo 2017 *Chem. Mater.* 29, 3029–3037 | [44] | 음극 계면의 LPS/LGPS 부분 가역 산화환원(PS₄ ↔ P₂S₆ + Li₂S) — In \| SE 쪽 SE 환원(진짜 `LLI`) 후보 | Q5 · Q7 | ★★ |
| Ito, Yamakawa, Hayashi, Tatsumisago 2017 *JMCA* 5, 10658–10668 | [29] | 탄소 부반응의 다른 원전 | Q2 | ★ |
| Kato, Hori, Saito, Suzuki, Hirayama, Mitsui, Yonemura, Iba, Kanno 2016 *Nat. Energy* 1, 16030 | [6] | 5 V 둘째 방전 평탄의 선례 · LF 근거 중 하나 | Q2 · Q5 | ★ |
| Sumita, Tanaka, Ohno 2017 *JPCC* 121, 9698 · Sumita, Tanaka, Ikeda, Ohno 2016 *JPCC* 120, 13332 | [38] · [40] | 전위 강하 · 음이온 중합(계산) | Q2 | ☆ |
| Han, Gao, Zhu, Gaskell, Wang 2015 *Adv. Mater.* 27, 3473 | [24] | SE 단일 재료 전지 — SE 산화환원 **용량**의 선례 | Q7 | ☆ |

# 이 digest 가 주장하지 않는 것

- **4.6 V 가역분이 접촉 호흡이라고 단정하지 않는다** — τ 비 1.10–1.24 는 전제 `C ∝ 면적` · CPE 환산(식 · α 미인쇄) · 셀 1 · 로그 축 픽셀 판독(±2.4 %) 위의 분류다. 계면층 산화환원이 `C` 를 바꾸는 경로(층 유전율 · 두께의 SOC 의존)도 배제하지 않았다.
- **노화분 저항형을 "`j₀` 가 줄었다" 로 옮기지 않는다** — 원전 자신이 분해를 집전체 쪽에 두고, EIS 한 호가 집전체 층 · CAM 계면층 · (MF 에 겹친) 입계 호의 분할에 걸려 있다. 주장은 "전제 위에서 접촉 면적 손실이 아니다" 까지다.
- **4.0 V "양극 호" 가 음극 호라고 단정하지 않는다** — `C` 자릿수 · τ 대역이 음극 쪽과 같다는 것까지다(두 요소를 적합이 섞었을 가능성).
- **집전체 층이 셀 저항에 기여하지 않는다고 하지 않는다** — Li⁺ 차단 계면이라는 물리에서 **경로를 묻는** 것까지다(전자 경로에 걸리면 기여할 수 있다).
- **in situ 전류 적분(≈0.55 / 0.52 mAh)을 SE 산화환원 전하로 쓰지 않는다** — 탄소 복합체 · ±10 V · 셀 전체 전류(용량성 · 음극 반응 포함)이고, 스폿 XPS 와 전하가 같은 부피를 보지 않는다.
- **상한 64 mAh g⁻¹ 을 계면층 용량으로 쓰지 않는다** — 복합체 SE 전부가 1 e⁻ 산화된다는 극한이다. "≈4–7 mAh g⁻¹" 은 한 분화구의 40 분 평탄을 전체에 편 강한 가정이다.
- **표 S8 · S5 의 뒤바뀜을 오기로 확정하지 않는다** — 그림 · 본문과 어긋난다는 것까지다(표 쪽이 맞고 그림이 틀렸을 가능성은 남는다).
- **Fig. 3 ↔ Fig. 4 의 ×1.3–1.9 를 휴지 중 성장으로 단정하지 않는다** — 다른 셀("representative")일 가능성이 있다.
- **[25] Zaghib 1999 에 In 전위가 없다고 하지 않는다** — 23호가 같은 편을 LTO 1.55 V 에 달았다는 것과 제목이 이 PDF 에 없다는 것까지다(파일 32 에서 확인).
- **픽셀 판독값을 인쇄값처럼 쓰지 않는다** — 원본 래스터 · 축 적합 위의 값이고 판독 오차가 있다(§그림 머리).

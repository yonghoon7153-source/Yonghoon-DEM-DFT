---
title: "Zhang W., Schröder D., Arlt T., Manke I., Koerver R., Pinedo R., Weber D.A., Sann J., Zeier W.G., Janek J. 2017 — (Electro)chemical expansion during cycling: monitoring the pressure changes in operating solid-state lithium batteries (J. Mater. Chem. A 5, 9929–9936)"
source_url: local-upload/24._Electro_chemical_expansion_during_cycling_monitoring_the_pressure_changes_in_operating_solid-state_lithium_batteries.pdf + 24._Sup_Electro_chemical_expansion_during_cycling_monitoring_the_pressure_changes_in_operating_solid-state_lithium_batteries.pdf
source_url_note: "본문 PDF 8 쪽(J. Mater. Chem. A PAPER · 그림 5 · 표 0 · 참고문헌 40) + ESI PDF 12 쪽(그림 S1–S7 · 부피 계산 3 · 참고문헌 11). 그림 자동 크롭 12 장(본문 5 · ESI 7) · 수동 크롭 0 — 12 장 전부 봤고, 수치는 PDF 안의 원본 래스터에서 축 눈금 적합으로 픽셀 판독했다. 본문 텍스트 층은 µ 를 m 으로 싣는다 — 단위는 렌더로 대조. 3차 묶음 파일 24 (2차 묶음 큐 번호와 별개). 22호 ref 18 · 23호 ref 40 · 33호 [89] · 59호 ref 23 의 원전."
source_doi: 10.1039/c7ta02730c
source_license: "© The Royal Society of Chemistry 2017 — 첫 쪽 'Licence and permissions'(RSC 라이선스 링크) · 오픈액세스 · CC 표시 없음. 이 digest 는 인용 · 요약 · 재현 계산만 담는다"
pdf_sha256: f449a273795f7bfbff0a70a9bcbd4853a87d7bb6945a06a48e6fd9e7e4c82ccd
si_sha256: e882761a29dd787da3504c659c3dcc68ad6c7ef3326cdb59267ea811ab2506ae
ingested: 2026-09-28
sha256: 0e1fd2869495b7f2a1488d3607ea8b4107830e926eecdaf4a210f792d38258a8
---
# 수집 목적

`assb` 섹션 **62호** — **3차 묶음 파일 24**(3차 묶음 넷째 편). 3차 묶음의 파일 번호 21–33 은 2차 묶음 "큐 N" 번호
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d, 큐 1–59)와 **별개**다 — 이 편은 "큐 24" 가 아니다. 닻은 `questions/assb-contact-loss-vs-lampe.md`.

들어온 경로: 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1) "★★★ **Zhang·Schröder·Arlt·…·Janek 2017** — *J. Mater. Chem. A* 5, 9929−9936 | 지목 22 · 23 · 33 · 59 | **4** | Q1·Q6 |
22호 셀 장치의 원전(양극 면적 미기재) + **충전 중 부피 수축 → 접촉 감소**를 압력으로 감시한 근거 — Q1 의 기구 쪽 입력". 네 지목이 이 편에 매단 명제(각 digest 에서 grep 해 읽음):

| 지목 | 인용 번호 | 매단 명제 |
|---|---|---|
| **22호** Strauss 2018 (digest :81 · :148 · :524 · :571) | ref 18 + SI ref 2 | (i) `[인쇄]` "setup described elsewhere" — 22호 **G5 양극 면적/지름 미기재**(22호 `[재현]` 0.66–0.80 cm²) (ii) `[인쇄]` "note that the **volume contraction during charging** leads to a reduced electrical contact between the CAM particles and the SE" (refs 9, 18) |
| **23호** Koerver 2017 (digest :553) | ref 40 | 본문 2 회: 서론 범위 인용 · "LiCoO₂ undergoes an overall expansion of the unit cell" |
| **33호** Zhang 2025 저압 종설 (digest :138 · :227 · :383) | [89] | Fig.(F) 재수록 — X-CT pristine ↔ charged 단면 곡률 `R₁` → `R₂` + 평면 원판 2 장 · `[인쇄]` "the pressure also induced noticeable cracks at the edges of the electrolyte, causing **contact loss**" · "if the battery is not subjected to external pressure during cycling, electrode expansion could prevent tight contact … ultimately leading to battery failure" |
| **59호** Li Q. 2025 (digest :268) | ref 23 | `[인쇄]` "Stack pressure can **mirror electrochemical behaviour** as it changes periodically with the electrochemical process23" |
| (6호 Lee 2020 — **카드 Status Log 기록만**) | ref 46 | 카드 6호 항: "4 순위 Zhang et al. 2017 (`JMCA` 5, 9929 — 6호 ref 46, **운전 중 압력 변화 실측**; G12(정압인가 정변위인가)의 답이 여기 있을 수 있다)". ⚠ 6호 digest 본문에는 ref 46 전사가 없고 6호 원문은 이 세션에 없다 — 원장 지목 목록에도 없다 |

**59–61호의 결과를 이어받는다.** 59호는 "운전 압력 요구치 ≈1–5 MPa 독립 수렴" 을 반박했고(원전 0), 60호는 13호 `<5 MPa` 의 [45] 다리가 "5" 를 주지 않음과
정변위 지그 첫 충전 **+1.51 MPa** 를, 61호(Masias 2019)는 Li 항복 0.73–0.81 MPa · creep `n` 6.56 · 계보 띠가 Li 눈금으로 여러 영역을 가로지름을 기록했다.
이 편은 **셀 안 압력 변화를 운전 중 실측한 원전**(2017-05 게재 — 60호 S14 · 33호 재수록 압력 진동들보다 앞선다)이다.

이 digest 의 일 (지시):

1. **인용 귀속 검증** — 네 지목(+ 카드의 6호 기록)이 이 편에 매단 명제를 원문이 실제로 주는가.
2. **(a)** 압력 변화의 크기 · 부호 · 사이클 추이(충전/방전별)가 인쇄돼 있는가, 어떤 셀(양극 · SE · 음극 · 면적 · 적재 · 초기 압력 · 지그 강성)에서인가.
3. **(b)** "부피 수축 → 접촉 감소" 가 **측정**인가 압력 신호에서 **추론**인가 — 카드 Q1(`θ(N)`)에 무엇이 들어오는가.
4. **(c)** 60호 S14(정변위 첫 충전 +1.51 MPa) · 61호(Li 항복/creep)와 같은 눈금에서 비교 가능한가.
5. **(d)** 22호 셀 장치의 원전으로서 22호가 비워 둔 값(양극 면적)을 주는가.
6. Q1–Q8 · 채움표 62호 행 · 곱 축퇴 처방 마흔다섯 번째 적용 · 보류 (가)(나)(다)(아)(자)(차)(타) 표시(결정 안 함).

> ⚠ **형식 — *J. Mater. Chem. A* PAPER 8 쪽(그림 5 · 표 0 · 참고문헌 40) + ESI 12 쪽(그림 S1–S7 · 부피 계산 3 · 참고문헌 11). 1차 측정 있음** — in situ 압력(In 음극 셀 ·
> LTO 음극 셀) · 딜라토미터(무가압 셀) · ex situ X-CT(실험실 · 싱크로트론) · in situ XRD · EIS(첫 충전). **셀 수는 어디에도 없다(조건당 1 로 읽힌다) · 오차 막대 0 · `±` 0.**
> 이 편의 그림은 **전부 래스터**다 — `[도표]` 값은 PDF 에서 원본 이미지를 꺼내 축 눈금 픽셀에 선형 적합한 뒤 마커 · 선 중심을 읽었다(§"픽셀 판독").
>
> 표기: `[인쇄]` 본문 · 캡션 · ESI 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`) · `[재현]` 지면의 숫자로 우리가 계산 · 대조한 값 · `[해석]` 우리 해석.
> `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **(a) 압력 변화의 크기 · 부호** | ★★★ **충전 ↑ · 방전 ↓ — 두 전극 모두 충전에 팽창** · 본문 값은 **하나**(1.25 MPa, 기저선 보정) · **운전 기저 ≈61.8 MPa 는 ESI 그림 축에만** | `[인쇄]` "During the initial charge, the pressure change is as high as 1.25 MPa, reflecting the volume expansion of both the LiCoO2 in the cathode during delithiation and the In/InLi composite at the anode upon lithiation". 본문 `MPa` **1 회**(이 문장) · `stack pressure` **0 회**. `[도표]` S7 원시 곡선 **61.83 → 62.90 MPa**(첫 충전 +1.07) — 운전 스택 압력이 본문 어디에도 없다 |
| **(a′) 사이클 추이가 용량을 따라가는가** | ⚠⚠ **아니다 — 압력/용량 비가 사이클마다 커진다** | `[도표]` Fig. 1b 진폭 **1.267 → 1.152 MPa(−9 %)** ↔ 용량 **116.7 → 93.2 mAh g⁻¹(−20 %)** ⇒ `[재현]` 진폭/용량 **1.086 → 1.236 MPa per 100 mAh g⁻¹(+14 %)**. `[도표]` S7 **원시** 충전 상승은 0.1C 에서 **+1.07 · +1.11 · +1.12 · +1.13 → +1.08 · +1.10 MPa** — 용량이 20 % 빠지는 동안 평탄하다. Fig. 1b 의 "진폭 감소" 는 기저선 규약의 몫(첫 충전 ≈0.20 MPa)과 같은 크기다 |
| **(a″) 셀 사양** | ✅ 대부분 인쇄 · ❌ 초기 압력 · 지그 강성 · 면적(직접) | In 박 125 µm × ∅8 mm ‖ LGPS 80 mg(∅10 mm Macor 실린더) ‖ LNTO(1 wt%)-LCO : LGPS 70 : 30, 12 mg(LCO 8.4 mg) · 조립 3.5 t / 1.5 t · 16 h 휴지 · 146 / 366 µA cm⁻²(C/10 · C/4) · 2.0–3.6 V vs In/InLi · 25 °C · "hot-press setup … hydraulic pressing device and an electronic pressure gauge"(장치는 [28] 에 위임). `[재현]` 면적 0.785 cm² · 10.7 mg LCO cm⁻² · 첫 충전 ≈1.25 mAh cm⁻² |
| **(b) "부피 수축 → 접촉 감소"** | ❌ **이 셀에서는 충전 = 팽창** · 접촉 손실은 **추론**(측정 0) | `contract` **1 회** — LCO 가 **방전(리튬화)** 에 수축해 압력이 내려간다는 문장뿐. 접촉 손실(`contact` 본문 10 회 중 셀 관련 9)은 (i) 용량 ↔ 압력 진폭의 상관(Fig. 1b 캡션) (ii) **외압 없는** 펠릿의 휨 · SE 가장자리 균열(X-CT, **다른 펠릿 둘 · 각 1** · 첫 충전 1 회) (iii) 무가압 딜라토미터 셀의 낮은 용량에서 **추론**한다 — 접촉 면적 · 공극 · 임피던스 사이클 시계열 0 |
| **(c) 60호 S14 · 61호와 같은 눈금인가** | ⚠ **아니다** — 크기는 같은 자릿수(≈1–1.5 MPa)지만 기저 · 구속 · 음극 · 온도가 다르다 | 기저 ≈61.8 ↔ 0.8 MPa(**×77**) · hot-press 유압 ↔ 정변위 지그 · In ↔ Si 계 음극 · 25 ↔ 45 °C. `[재현]` 면적 용량당 ΔP ≈**1.0**(보정) · ≈**0.86**(원시) ↔ 60호 ≈**0.52** MPa per mAh cm⁻². `[재현]` 관측 ΔP 를 셀 적층의 탄성만으로 내려면 유효 길이 **≈22–36 mm**(인쇄 SE 탄성률 18–25 GPa · ESI 1/3 규칙 두께) — 셀 적층은 두께 인쇄 0 이나 `[해석]` 밀도를 낮게 잡아도 ≲1.3 mm ⇒ **ΔP 는 지그 순응(또는 공극 압밀)이 정한다**(강성 인쇄 0). 61호: 이 셀의 기저 ≈61.8 MPa 는 Li 항복의 **≈80×** — 그러나 음극은 In 이라 Li 눈금 밖 |
| **(d) 22호 셀 장치의 원전** | ⚠ **부분** | `[인쇄]` "**10 mm** diameter cylinder composed of Macor™" · In "**diameter of 8 mm**" → `[재현]` 0.785 cm² — 22호 역산 0.66–0.80 cm² 안이고 C/10 = 146 µA cm⁻² 가 0.785 cm² 로 **정확히 재현**(8.4 mg × 137 mAh g⁻¹). ⚠ 장치는 다시 **[28] Busche 2016** 에 위임 · EIS 는 "standard SSB setup"(→ [27] "submitted") · ESI 계산은 "**cell area of 1.103 cm²**"(∅11.85 mm) · 조립 3.5/1.5 t(`[재현]` 437/187 MPa) ↔ 22호 375/125 MPa · 운전 압력 본문 0 ↔ 22호 55 MPa |
| **22호 ref 18 귀속** | (i) ⚠ 부분 · (ii) ❌ | (i) 위 (d). (ii) 이 편의 양극(LCO)은 충전에 **팽창**하고 "수축 → 접촉" 문장은 0 — NCM 은 결론에 `[인쇄]` "volume changes of nearly 6%"[31] 로만(방향 0). "충전 수축" 은 22호의 다른 다리 ref 9(= 23호 Koerver)의 명제다 |
| **23호 ref 40 귀속** | ✅ (⚠ 수치는 재인용) | `[인쇄]` "the layered structure of LiCoO2 shows an expansion of the unit cell upon deintercalation.30 … resulting in a 2% volume expansion along the c-axis … as shown by Dahn and coworkers" + ESI in situ XRD (003) 저각 이동 · 분열(정성, `[도표]` x = 1 → 0.743 까지). "2 %" 는 [30] Reimers & Dahn 1992 의 값 |
| **33호 [89] 귀속** | ✅ 그림 · ⚠ 문장 | `R₁` · `R₂` 는 원 Fig. 5a 에 있다(주황 곡선 · **수치 0**). 균열 ✅ `[인쇄]` "At the edge of the charged pellet, several cracks can be seen". "causing contact loss" 는 원문에서 **추론** — `[인쇄]` "Consequently, without any pressure confinement of the SSB, the contact between electrode particles and interfaces **cannot be maintained** … **Eventually this can lead to** a loss of grain contact". 대상은 **외압 없는** 펠릿 · 충전 1 회 · 다른 펠릿과의 비교 |
| **59호 ref 23 귀속** | ✅ (⚠ 기저선을 뺀 그림에서) | `[인쇄]` "The pressure change follow the cell potential during charge and discharge process, and the change is almost linearly with the amount of charge transferred" · 초록 "a highly reproducible cycle of pressure changes". ⚠ "mirror" 는 기저선을 뺀 Fig. 1 의 성질 — 원시 곡선(S7)은 110 h 에 **−1.2 MPa** 표류(한 사이클 진폭과 같은 크기). 59호의 다음 문장("differentiating between normal and harmful states")은 refs 24–26 의 것 |
| **6호 ref 46(카드 기록)** | ⚠ G12 에는 답하지 않는다 | 이 편은 **Giessen hot-press** 의 셀이 충전에 압력을 올린다는 것(= 정하중 제어가 아님)까지 — 6호(SAIT) 지그의 정압/정변위 여부와 무관 |
| **원장 행 서술** | ⚠ 절반 · ❌ 절반 | "22호 셀 장치의 원전(양극 면적 미기재)" ⚠ · "**충전 중 부피 수축** → 접촉 감소를 **압력으로 감시**" ❌ — 압력이 본 것은 충전 **팽창**이고(음극 몫 `[재현]` ≈90–95 %), 접촉은 압력으로 감시되지 않았다 |
| **Q1** | **없다 — `θ(N)` 0/62** | 사이클 시계열은 압력 진폭 11 점(In) · 11 점(LTO) · 용량 · 원시 압력(S7) · 높이(S6, 무가압) — 접촉량 0 |
| **Q2** | **부분 — 채널 다섯, 가르는 용도 0** · ★ LTO 대조 = **압력 채널의 전극 분해** | in situ 압력 · 딜라토미터 · X-CT(실험실 6.25 µm · 싱크로트론 2.15 µm) · in situ XRD · EIS. `[재현]` 음극 교체로 압력 신호의 음극 몫 **≈90–95 %**(진폭 ×18.9 · 용량당 ×14.7 · ESI 두께 계산 ×10.6) — 양극 `LAM_PE` ↔ 접촉 손실 분해 0 |
| **Q4** | **0/62 — 쉰네 번째 성질** | "압력 진폭 감소를 용량 감쇠와 '잘 상관' 한다 적고 접촉 손실의 지표로 읽지만, 진폭은 전달 전하에 선형이라 따라가는 것이 구성상이고 · 진폭 감소의 크기는 기저선 규약 몫과 같으며 · 같은 지면에 감쇠 원인 넷을 나열하고 가르지 않는다" |
| **곱 축퇴 처방 마흔다섯 번째** | **적용 불가 — 1단계 입력 없음** · ★ 기록: **압력 채널에도 곱이 있다** | `ΔP = k_eff · Δh` · `Δh ∝ (순환 활성 부피) · Δx` — 강성 `k_eff(N)` 과 활성 분율이 한 곱(`[해석]`). `[재현]` 비 +14 % 는 활성 분율이 아니라 `k_eff` 쪽이 움직였다는 것과 양립(이 편의 압밀 서사) — 처방 표에 경고 행 |
| **보류 (가)(나)(다)(아)(자)(차)(타)** | **근거 0 — 결정 안 함** | 일곱 항 모두 이 편의 내용과 닿지 않는다 |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | (Electro)chemical expansion during cycling: monitoring the pressure changes in operating solid-state lithium batteries† |
| 저자 (10) | **Wenbo Zhang**ᵃ, Daniel Schröderᵃ, Tobias Arltᵇ, Ingo Mankeᵇ, Raimund Koerverᵃ, Ricardo Pinedoᵃ, Dominik A. Weberᵃ, Joachim Sannᵃ, **Wolfgang G. Zeier**ᵃ\*, **Jürgen Janek**ᵃ\* |
| 소속 | ᵃ Physikalisch-Chemisches Institut, Justus-Liebig-Universität Giessen · ᵇ Helmholtz-Zentrum Berlin für Materialien und Energie |
| 서지 | *J. Mater. Chem. A* **5**, 9929–9936 (2017) · doi `10.1039/c7ta02730c` · PAPER · 첫 쪽 "Published on 05 May 2017" · "Licence and permissions"(rsc.org/rsc-licence 링크) — **오픈액세스 · CC 표시 없음**(이 digest 는 인용 · 요약 · 재현 계산만 담는다) |
| 일정 | 접수 2017-03-29 · 승인 2017-05-05 · 게재 2017-05-05 — `[재현]` 접수 → 승인 **37 일**. PDF 메타: title · author("Wenbo Zhang") · subject(DOI) 일치 · creator/producer Aspose · 생성 2017-05-20 · 수정 2026-03-17(재저장) |
| 자금 | `[인쇄]` HGP-E · BASF International Scientific Network for Electrochemistry and Batteries |
| COI | 문구 없음 |
| 기여 | `[인쇄]` 구상 W.Z. · J.J. · W.G.Z. · 압력 · 토모그래피 셀 설계/조립 W.Z. · D.S. · **"The data for Li4Ti5O12 was provided by R. K."**(Koerver = 23호 제1저자) · 토모그래피 D.S. · T.A. · W.Z. · I.M. · in situ XRD R.P. · 논의 D.A.W. · J.S. · 감독 J.J. · W.G.Z. |
| 분량 | 본문 pp. 9929–9936 = PDF 8 쪽(2,062,755 B) — 그림 5 · 표 0 · 식 0 · 참고문헌 **40** |
| ESI | PDF 12 쪽(21,563,294 B) — 6 절(① EIS · 장기 사이클 ② in situ XRD ③ 전극 부피 팽창 추정 ④ 토모그래피 부가 정보 ⑤ 딜라토미터 ⑥ 압력 기저선) · 그림 **S1–S7** · 참고문헌 11. 메타: title "Microsoft Word - Supporting_Information.docx" · 생성 **2017-03-29(접수일)** · 수정 **2017-05-05(승인일)** |
| sha256 | 본문 PDF `f449a273795f7bfbff0a70a9bcbd4853a87d7bb6945a06a48e6fd9e7e4c82ccd` · ESI PDF `e882761a29dd787da3504c659c3dcc68ad6c7ef3326cdb59267ea811ab2506ae` — 호출자 명시값과 **일치** |
| 서지 대조 | 호출자가 준 "Zhang W., Schröder D., Arlt T., Manke I., Koerver R., Pinedo R., Weber D.A., Sann J., Zeier W.G., Janek J. — *J. Mater. Chem. A* 5, 9929–9936 (2017)" 와 **일치**. DOI 는 첫 쪽 · 메타에서 읽었다 |
| ⚠ 텍스트 층 | 본문 PDF 의 텍스트 층은 **µ 를 "m" 으로** 싣고(예: 렌더 "125 µm" → 텍스트 "125 mm" · "~1 µm" → "1 mm") **fi · fl · ft 합자를 사용자 영역 문자**(U+E103 · U+E104 · U+E09D)로 싣는다 — 이 digest 의 단위는 전부 **렌더한 쪽 이미지로 대조**했고, 어휘 집계는 합자를 복원해 셌다 |
| `[해석]` 자기 인용 | 40 편 중 Janek 이 저자인 편: [1] Zeier & Janek 2016 · [9] [10] Wenzel 2016 · [21] Weber 2016 · [25] [26] Schröder 2016 · [27] Zhang W. 2016 "submitted" · [28] Busche 2016 · [31] Kondrakov 2017 · [39] Haetge 2011 — **10 편**(+ [24] Schröder · Arlt · Krewer · Manke 2014 는 이 편 공저자 셋) |
| ⚠ 동명 주의 | 60호 Zhang Z. 2025 · 33호 Zhang 2025 종설과 무관. [27] "W. Zhang, D. A. Weber, H. Weigand, T. Arlt, I. Manke, D. Schröder, W. G. Zeier and J. Janek, 2016, submitted"(= ESI ref 1) — 원장 ★★★★ **Zhang 2017 *ACS AMI* 9, 17835**(저자 11 명)와 같은 편일 가능성(8 명이 부분집합) — **미확인** |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | ★★★ **운전 스택 압력이 본문에 없다.** `[인쇄]` "homemade apparatus (referred to as hot-press setup) combined with a hydraulic pressing device and an electronic pressure gauge at the bottom of the setup. Detailed information on the apparatus is provided in a previous publication from our group.28" — 예압 설정값 · 조절 방식(정하중/정변위) · 지그 강성 · 게이지 분해능 · 온도 제어 0. 절대값은 **S7 세로축(`[도표]` ≈60.6–62.9 MPa)** 에만. 본문의 구속 서술은 "solid-state cells with a **fixed volume**" 한 구절 | ΔP 의 크기는 지그 강성의 함수다(§(c) `[재현]`). 기저 ≈62 MPa 위의 1.25 MPa 를 저압(60호 0.8 MPa 기저) 셀로 옮길 근거가 없다 |
| G2 | ★★★ **기저선의 정의 0** — `[인쇄]` "The absolute pressure change is shown after subtracting the baseline" · S7 "An inclined baseline indicates the consolidation of SE". 기저선이 무엇에 맞춘 곡선인지 0 — `[도표]` S7 의 빨간 선은 **방전 말 골을 잇는 꺾은선**(골과 ≤0.02 MPa) | Fig. 1a 의 방전 말 ΔP = 0 은 **구성상**이다. 사이클당 비가역 압력 변화(원시 −0.30 → −0.12 MPa/사이클)와 보정 진폭의 감소분이 이 규약에 걸려 있다 |
| G3 | ★★★ **접촉 측정 0** — 접촉 면적 · 공극 · 균열 정량 · 임피던스의 사이클 시계열 0. EIS 는 **첫 충전**뿐이고 "standard SSB setup"(다른 장치, ESI ref 1) | 이 편의 접촉 명제는 전부 추론이다(§(b)) |
| G4 | ★★ **셀 수 · 반복 0** — `n =` 0 회 · `±` 0 회. 토모그래피 pristine ↔ charged 는 `[인쇄]` "**two identical SSB pellets**" — 같은 시편의 전후가 아니다 | 공극률 5.45 → 2.58 % 는 두 펠릿의 차이다 |
| G5 | ★★ **LTO 셀의 장치 · 조건** — `[인쇄]` "the cell was fabricated in an air-tight cell casing designed by our group27 and tested in a cabinet maintained at 25 °C". 같은 hot-press 로 쟀는지 · 예압 · 기저선 처리 · LTO 복합 음극 적재 · N/P 0. 본문 스스로 "**both setups**" | Fig. 4 "direct comparison" 의 ×20 은 **장치 차이를 포함**할 수 있다 |
| G6 | ★★ **ESI 계산 셀의 정체** — `[인쇄]` "14 mg LiCoO2" · "89 mg In foil … 774.5 µmol" · "a capacity of 1.53 mAh" · "cell area of 1.103 cm²" ↔ 본문 압력 셀(LCO 8.4 mg · In 125 µm × ∅8 mm · ∅10 mm). `[재현]` 1.53 mAh ÷ 8.4 mg = **182 mAh g⁻¹ > 이론 137** | ESI 의 두께 추정(1.56 µm · 0.163 µm · Li 2.2 µm)이 어느 셀의 값인지 0 |
| G7 | ★★ **예상 압력 0** — ESI 설명은 "the estimation of maximum pressure build-up" 을 약속하지만 ESI 는 `[인쇄]` "it is not possible to fully gauge the expected pressure build up … all estimates of pressure build-up are theoretical upper limits" 로 끝나고 **압력 수치 0** | 본문 "the observed pressure increase is lower than expected for the fully dense single crystalline SSB" 의 "expected" 에 수치가 없다 |
| G8 | ★ **딜라토미터의 하중 · 첫 구간** — "non-pressurized" 이지만 ECD-3-nano 의 측정 하중 0. S6 첫 ≈6.5 h 는 `[도표]` 전압이 창(2.7–3.6 V) 밖 — 휴지로 읽힌다(정의 0) | 그 구간의 높이 −2.6 µm 가 "setup relaxation 배제" 논증(D13)에 걸린다 |
| G9 | ★ **토모그래피 셀의 양극 적재 · In 두께 · 충전 용량 0** | ESI 부피(음극 1.89 → 5.93 mm³ 등)를 해석할 재료가 없다(D9) |
| G10 | ★ **Fig. 1b 의 "capacity"(충전/방전) · "pressure amplitude"(정점 − 기저선? 정점 − 직전 골?) 정의 0** | 비(§(a′))의 분자 · 분모 규약 |
| G11 | ★ **In 음극의 기계 물성 · 압력 셀의 무전류 대조 0** — 기저선 표류(원시 −1.2 MPa/110 h)의 후보(SE 압밀 · In creep · 장치 이완 · 온도)를 가를 대조는 딜라토미터 셀의 **사후 유지** 하나뿐 | 저자는 압밀 하나로 배정한다 |
| G12 | ★ **XRD 범위 · 격자상수 0** — in situ XRD 는 `[도표]` x = 1 → **0.743** 까지(충전 18 h, C/33) · a · c 수치 0. "2 %" 는 [30] 재인용 | 양극 팽창의 크기는 이 편에서 재지 않았다 |

# 그림 — 자동 크롭 12 장(본문 5 · ESI 7), 실제로 본 것: 12 / 안 본 것: 0 — 수치는 원본 래스터에서 픽셀로 읽었다

폴더 `raw/figures/zhang2017_in-situ-pressure-electrochemical-expansion-assb/`(`figures.json` 12 항목 · 수동 크롭 0 — 캡션 기준 자동 추출이 12 장을 모두 잡았다).
**봤다(12)**: Fig. 1 · 2 · 3 · 4 · 5 · S1 · S2 · S3 · S4 · S5 · S6 · S7. 그 밖에 단위 판정을 위해 본문 pp. 9930–9932 의 문장 영역과 S6 첫 구간을 따로 렌더해 봤다(그림 아님).
수치 판독은 크롭 PNG 가 아니라 **PDF 안의 원본 이미지**(Fig. 1 888×1116 · Fig. 3 888×1157 · Fig. 4 710×474 · S3 3471×2282 · S6 3163×1932 · S7 2429×2224 px)에서 했다 — 축 눈금 픽셀에
선형 적합 → 마커 연결 성분 중심 · 선 중심. 판독 오차 ≈±0.3 mAh g⁻¹ · ±0.003 MPa(Fig. 1b) · ±0.001 MPa(Fig. 3b) · ±0.01 MPa(S7, 선 두께 ≈0.013 MPa) · ±0.05 µm(S6).

## `[도표]` Fig. 1 — In ‖ LGPS ‖ LCO 셀의 전압 · ΔP(a) · 용량 · 압력 진폭(b) (봤다) — ★ 이 편의 중심 그림

- (a) 왼쪽 축 셀 전압 2.0–3.6 V(파랑) · 오른쪽 축 **"Δ Pressure / MPa" 0.0–3.0**(빨강) · 시간 0–≈105 h · 띠 0.1 C(0–≈60 h) · 0.25 C(≈60–84 h) · 0.1 C(≈84 h–). ΔP 는 **삼각파** —
  충전 중 선형 상승 · 방전 중 선형 하강 · **매 방전 말 0.0 으로 복귀**. 정점 `[도표]` **1.270(8.2 h) · 1.235 · 1.222 · 1.222** | 1.090 · 1.090 · 1.083 · 1.055 · 1.048 | **1.159(90.7 h)**
  (선 윗변 판독 — 선 두께만큼 ≈+0.01). 점선이 정점들을 잇는다(0.1 C 블록 · 0.25 C 블록 · 0.1 C 블록 각각).
- (b) 용량(파랑 ■, 60–120 mAh g⁻¹) · 압력 진폭(빨강 ●, **0.95–1.4 MPa** — 오른쪽 축이 0 에서 시작하지 않는다) × 사이클 1–11. 값은 §"픽셀 판독" 표.
- 본문 정합: `[인쇄]` "the pressure change is as high as 1.25 MPa" ↔ `[도표]` 1.267 ✓ · "At a higher C-rate less capacity is obtained and leads to a lower pressure change" ✓.
- ⚠ **(b) 의 두 축 범위가 감소를 크게 보이게 한다** — 용량 축 60–120(×2) · 진폭 축 0.95–1.4(×1.47) 위에서 두 점선이 나란히 내려가지만, 비율로는 용량 −20 % ↔ 진폭 −9 % 다(`[재현]` §(a′)).
- ⚠ **방전 말 0 은 구성상**(S7 · D1) — (a) 는 기저선을 뺀 그림이다.

## `[도표]` Fig. 2 — In(정방) → InLi(입방) 격자 모식 (봤다)

- 왼쪽 "Pure indium Tetragonal phase" **a = 3.298 Å · c = 5.063 Å** — 화살표 "More"(a · b 방향) · "Less"(c 방향). 오른쪽 "InLi cubic phase" **a = 6.792 Å**, 안에 정방 부분 격자
  (밑변 **4.803 Å** · c = 6.792 Å) · "Equal Expansion". 수치 판독 0(인쇄된 치수뿐).
- `[재현]` In 격자 3.298² × 5.063 = **55.07 Å³** ✓(인쇄 55.069) · 4.803 = 6.792/√2 ✓ · **그린 InLi 부분 격자 4.803² × 6.792 = 156.66 Å³ ↔ 인쇄 "113.23 Å³"**(D3) ·
  입방 격자 a³/8(In 8 개)로 In 원자당 몰부피 **23.59 cm³ mol⁻¹ ✓(인쇄 23.597)** · 그린 In 격자(원자 2)로 **16.58 ↔ 인쇄 15.71 cm³ mol⁻¹**(5.5 %).

## `[도표]` Fig. 3 — LTO ‖ LGPS ‖ LCO 셀 (봤다) — 음극 교체 대조

- (a) 셀 전압 1.0–3.0 V · **"Δ Pressure / MPa" 0.00–0.24** · 시간 0–≈82 h. ΔP 는 **잡음이 큰 삼각파**(`[도표]` 폭 ≈±0.005 MPa) — 0.1 C 정점 ≈0.065–0.068 · 0.25 C ≈0.03–0.04 MPa.
- (b) 용량 0–110 · 진폭 **0.00–0.10 MPa** × 사이클 1–11. 값은 §"픽셀 판독" 표.
- 본문 정합: `[인쇄]` "a 20 times smaller pressure change is observed" ↔ `[재현]` 1.267 / 0.0669 = **18.9** ✓ · 캡션 "decreases to 60% of the previous values" ↔ `[재현]` 0.25 C 평균 0.0412 / 0.1 C 평균 0.0655 = **63 %** ✓.
- ⚠ 캡션 "**as was also observed when using In anode**" ↔ Fig. 1b `[재현]` In 셀 0.25 C/0.1 C 진폭 = 1.083 / 1.205 = **0.90**(D10) — 방향만 같다.
- ⚠ **0.1 C 에서 LTO 셀 진폭은 11 사이클 내내 평탄**(0.0669 → 0.0669) — 용량은 90.6 → 82.2(−9 %). 잡음 폭(3 사이클 0.061) 안이지만 "진폭 ↔ 용량 상관" 은 이 셀에서 율 전환에만 선다.

## `[도표]` Fig. 4 — 두 셀의 둘째 충전 Δp vs 용량 (봤다)

- 세로 **"Δp / MPa"** — **축이 끊겨 있다**(아래 0.00–≈0.06 · 위 ≈0.1–1.2). 가로 "Capacity / mAh g⁻¹ (LiCoO2)" **0–90**. 캡션 `[인쇄]` "The curves have been smoothed and are extracted from the second charge process".
- `[도표]` In(짙은 파랑): 0 에서 ≈0.04 → **88 mAh g⁻¹ 에서 ≈1.06 MPa**, 직선 — 기울기 **≈0.0115 MPa per mAh g⁻¹**(Fig. 1b 2 사이클 비 0.0114 와 일치). LTO(하늘색): ≈0.007 → 88 에서 **≈0.065**,
  ≈10–25 mAh g⁻¹ 에 ≈0.013 의 평탄 계단 · 기울기 ≈0.00066. `[재현]` 기울기 비 **≈17**.
- ⚠ 가로축이 **90 에서 잘린다** — In 셀 둘째 충전은 `[도표]` 107.9 mAh g⁻¹(Fig. 1b). 평활 방법 0. 두 셀은 다른 케이스에서 쟀다(G5 — 본문 "both setups").

## `[도표]` Fig. 5 — X-CT: (a) 실험실 · (b) 싱크로트론 (봤다) — 33호 재수록 원본

- (a) 윗줄 펠릿 렌더 셋 + 보는 면(보라). 가운데 렌더 옆에 적층 "LCO / SE / In". **pristine** 줄(회색 배경): 왼쪽 세로 단면(0.5 mm 막대, 직사각형 · 입자 질감) · 가운데 전체 단면 —
  아래 밝은 띠(In) 위에 **주황 곡선 `R₁`**(약한 휨) · 오른쪽 평면 원판(1 mm 막대, 흰 반점 다수). **charged** 줄: 왼쪽 단면이 **사다리꼴 · 위쪽에 어두운 균열망** · 가운데 단면 **`R₂`**(더 휜
  곡선) · 오른쪽 원판 더 균일한 회색 · 가장자리 작은 결손. **`R₁` · `R₂` 에 수치 0**(곡률 반경 · 처짐 0).
- (b) 3D 재구성(0.7 mm 막대) — 왼쪽 반원 **charged**(균일한 녹황 · 반점 거의 0) · 오른쪽 **pristine**("low density" 검은 반점 · "SE" · "high density" 파란 반점) · 색 막대 "material density".
- 캡션 `[인쇄]` "Bright areas … refer to a high attenuation … i.e. heavy elements or higher material density" · "The charged pellet is subjected to a strong bending force during charging" · "Cracking of the SE can be observed at the edges of the charged cell".
- ⚠ 본문 "the more uniform distribution of **pores (light areas** in the tomography images of the solid electrolyte, right column of Fig. 5a)" ↔ 캡션 "Bright areas … **higher material density**"(D6) — 오른쪽 원판의 흰 반점은 캡션대로면 고밀도 상이다.
- ⚠ 캡션 "after the 1st charge at a current density corresponding to **0.1C**" ↔ 실험 "19.1 µA cm⁻², corresponding to a C-rate of **0.03C**"(D7). pristine 과 charged 는 **서로 다른 펠릿**(G4).

## `[도표]` Fig. S1 — 첫 충전 전후 Nyquist (봤다)

- "Nyquist plot of a SSB (In/LGPS/LNTO-LCO)": ● 조립 직후(빨강) — 고주파 절편 **≈21 Ω** 에서 스파이크 · ● "after 1% of charge (not yet reach the plateau)"(주황) ≈19 Ω · ● "fully charged to 3.6 V"(파랑)
  ≈15.5–16 Ω + 두 반원(인셋 0–200 Ω: 파랑이 ≈100 Ω 안에서 닫힘). 점선 반원 셋은 원점 → 각 절편의 **작도**(측정점 아님) · 화살표 "charge".
- 본문 `[인쇄]` "a spike starting from 21 Ohm" · "A shift of Re(Z) to 19 Ohm" · "to 16 Ohm" ✓ · "The decrease in the resistance with the charge process indicates the microstructural consolidation (densification) of the SE."
- ⚠ **측정 장치는 "our standard SSB setup"(ESI ref 1)** — 압력 셀이 아니다. `[해석]` 고주파 절편 −24 % 를 SE 압밀 하나로 배정하고 다른 기여(복합양극 경로 · 접촉)를 가르는 대조는 없다.

## `[도표]` Fig. S2 — 첫 충전 중 EIS 10 점 (봤다)

- 세로로 **어긋나 쌓은** Nyquist 10 개(각 곡선 ≈6 Ω 씩 위로) · 라벨 3.305 V(3.296 V) → 3.599 V(3.578 V) — 괄호 값은 30 분 휴지 뒤 값으로 읽힌다(정의 0). 주파수 표지 1.84 MHz · 500 Hz · 15 Hz · 0.1 Hz ·
  고주파 시작 ≈15 Ω · 두 봉우리(500 Hz · 15 Hz). 캡션 `[인쇄]` "The two semicircles were observed only when the cell potential reached the plateau of LiCoO2, i.e. 3.3 V vs. In/InLi … the total value was maintained below 100 Ohm".
- ⚠ 방법 절 "7 MHz to 10 mHz" ↔ 그림 표지 1.84 MHz–0.1 Hz(표시 범위). 사이클 축 EIS 0.

## `[도표]` Fig. S3 — "model SSB" 100 사이클 (봤다)

- 용량(파랑, 0–200) · CE(초록, 86–100 %) × 0–100 사이클. `[도표]` 용량 **135.2(1) → 125.0(2) → 116.7(10) → 114.7(20) → 113.2(50) → 106.1(100) mAh g⁻¹** · CE **91.0(1) · 98.3(2) · 98.5(3) · 98.7(4) · 99.0(5) · 99.4(10) · ≈99.6 %(20–100)**.
- 캡션 `[인쇄]` "80% of its initial capacity could be maintained after 100 cycles at 0.1 C" ↔ `[재현]` 106.1 / 135.2 = **78.5 %** ✓(반올림) · "the Coulombic efficiency was maintained **above 99% from the 2nd cycle on**" ↔ `[도표]` 2 사이클 98.3 % · 99 % 도달 ≈5 사이클(D12).
- ⚠ **압력 셀과 다른 셀이다** — 압력 셀 첫 사이클 116.7 · 11 사이클 −20 %(Fig. 1b) ↔ 이 셀 135.2 · 10 사이클 −14 %. 본문 "stable electrochemical performance (see the ESI)" 의 근거는 이 셀이다.

## `[도표]` Fig. S4 — in situ XRD (봤다)

- 위: 1 h → 18 h 회절 무늬 폭포(2θ 10–70°) · 인셋 전압–시간 — `[도표]` **1.0 V 에서 시작해 ≈4 h 에 ≈3.0 V, ≈6 h 부터 ≈3.3 V 평탄**(C/33 로 ≈6 h = 명목 용량의 ≈18 % 가 평탄 전에 흐른다 — 설명 0).
- 아래 왼쪽 (003) 18.2–19.0°: Li₁CoO₂(≈18.73°) → Li₀.₉₂₄ → Li₀.₈₄₉ → Li₀.₇₇₃ → **Li₀.₇₄₃CoO₂** — 봉우리가 저각으로 밀리고 ≈18.5° 에 새 봉우리(분열). 아래 오른쪽 (104) 43.5–46.5°: 파란 띠(≈44.85°)에 새 반사 · 분홍 띠(≈45.1°).
- ⚠ **x = 1 → 0.743 까지**(완전 충전 x ≈0.5 의 절반) · 격자상수 수치 0 · XRD 셀 = 토모그래피 방식 조립(등방 4000 bar · 외압 0).

## `[도표]` Fig. S5 — 공극 분할 시각화 (봤다)

- pristine(위) · charged(아래) SE 영역만(1.0 mm 막대). pristine: 어두운 반점(= void, 캡션 "dark gray") 산재. charged: 반점이 적고 **가장자리 테두리가 어두운 반점 띠**. `[도표]` charged 원판이 가로로 ≈5 % 넓다.
- 캡션 `[인쇄]` "Porosity decreases approximately by 50% from for the pristine pellet to the charged pellet, whereas pores below the spatial resolution of 6.25 µm are not accounted for".
- `[해석]` charged 가장자리의 어두운 띠(Fig. 5a 의 가장자리 균열 자리)를 공극 계산에서 어떻게 다뤘는지 0 — 문턱 분할이면 void 로 셀 자리다.

## `[도표]` Fig. S6 — 무가압 셀 딜라토미터 (봤다) — ⚠ **캡션의 "setup relaxation 배제" 와 첫 구간이 어긋난다**

- 전압 2.7–3.6 V(파랑) · **"Height / µm" −6 → −23**(빨강) · 0–100 h · 주황/분홍 띠 둘(기울어진 기저의 장식 띠). 값은 §"픽셀 판독" 표.
- `[도표]` **첫 ≈6.5 h 는 전압이 창 밖**(첫 충전 전 휴지로 읽힌다) — 높이 **−6.05 → −8.63 µm**. 첫 충전(6.5–13 h) 중에도 **−8.63 → −9.74**(내려간다) · 첫 방전 −2.72 µm. 충전 중 상승은
  2 사이클 **+0.13** → 9–11 사이클 **+0.58–0.59 µm** · 방전 중 하강 −2.28 → **−1.09 µm** · 사이클 순감소 −3.83 → **−0.50 µm**(마지막까지 남는다). 사이클 끝(≈95–98 h) 평탄 −21.70.
- 캡션 `[인쇄]` "The height-change curve (red) follows well the charge-discharge curve (blue) from the third cycle on … no height change could be observed once the galvanostatic cycling stops, which excludes the
  relaxation of setup components leading to the inclined baseline" ↔ 첫 휴지 구간 −2.6 µm(D13) · 본문 "within the first few cycles" ↔ 11 사이클 끝까지 −0.5 µm/사이클(D14).

## `[도표]` Fig. S7 — 압력 셀의 **원시** 압력(기저선 제거 전) (봤다) — ★★★ **운전 기저 ≈61.8 MPa 는 이 그림에만 있다**

- 세로 **"Pressure / MPa" 60.5–65** · 가로 0–110 h · 검정 "measured curve" · 빨강 "baseline". 원시 곡선 **61.83 MPa 에서 시작**, 첫 정점 **62.90** · 방전 말 골 61.53 → 60.68 · 끝 ≈60.63 MPa.
  빨간 기저선 61.75(0 h) → 60.58 MPa(110 h) — **골을 잇는다**(골과 ≤0.02 MPa). 값은 §"픽셀 판독" 표.
- 캡션 `[인쇄]` "the pressure change curve of the In/SE/LiCoO2 without subtracting the baseline. An inclined baseline indicates the consolidation of SE due to the pressure generated by the volume expansion of electrode materials during cycling."
- ⚠ 캡션은 "pressure change curve" 라 부르지만 축은 **절대 압력**이다(D20). 본문 Fig. 1 은 이 곡선에서 기저선을 뺀 것.

# 픽셀 판독 (`[도표]` 전부 — 원본 래스터 · 축 눈금 선형 적합)

**Fig. 1b · Fig. 3b** — 마커 중심. 비 = 진폭 ÷ 용량(MPa per 100 mAh g⁻¹, `[재현]`).

| 사이클 | 율 | In 셀 용량 | In 셀 진폭 (MPa) | In 비 | LTO 셀 용량 | LTO 셀 진폭 (MPa) | LTO 비 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.1 C | 116.7 | 1.267 | 1.086 | 90.6 | 0.0669 | 0.074 |
| 2 | 0.1 C | 107.9 | 1.227 | 1.137 | 87.7 | 0.0670 | 0.076 |
| 3 | 0.1 C | 102.2 | 1.218 | 1.192 | 86.0 | 0.0610 | 0.071 |
| 4 | 0.1 C | 100.9 | 1.205 | 1.194 | 84.8 | 0.0669 | 0.079 |
| 5 | 0.25 C | 88.6 | 1.083 | 1.222 | 63.9 | 0.0480 | 0.075 |
| 6 | 0.25 C | 86.9 | 1.087 | 1.251 | 52.8 | 0.0391 | 0.074 |
| 7 | 0.25 C | 85.7 | 1.077 | 1.257 | 49.3 | 0.0410 | 0.083 |
| 8 | 0.25 C | 84.4 | 1.053 | 1.248 | 47.8 | 0.0380 | 0.080 |
| 9 | 0.25 C | 83.3 | 1.041 | 1.250 | 47.3 | 0.0401 | 0.085 |
| 10 | 0.1 C | 94.0 | 1.154 | 1.228 | 81.9 | 0.0660 | 0.081 |
| 11 | 0.1 C | 93.2 | 1.152 | 1.236 | 82.2 | 0.0669 | 0.082 |

`[재현]` In 셀: 용량 1 → 11 **−20.1 %** · 진폭 **−9.1 %** · 비 **+13.8 %**(0.1 C 끼리 1 → 4: 용량 −13.5 % · 진폭 −4.9 %). LTO 셀: 용량 −9.3 % · 진폭 **0 %** · 비 +10 %(잡음 폭 안).
In ÷ LTO: 진폭 ×18.9(1 사이클) · 비 ×14.7 ⇒ 같은 강성이라면 압력 신호의 **양극 몫 ≈5–7 %**. ESI 두께 계산(In 1.56 µm · LCO 0.163 µm)은 양극 몫 **9.5 %** 를 예측한다.

**Fig. S7** — 선 중심. 원시 상승/하강 = 직전 골(또는 시작)에서 정점까지 / 정점에서 다음 골까지.

| 반사이클 | 시각 (h) | 원시 압력 (MPa) | 원시 변화 (MPa) | 빨간 기저선 (MPa) | 정점 − 기저선 |
|---|---:|---:|---:|---:|---:|
| 시작 | 0.1 | 61.83 | — | 61.75 | — |
| 충전 1 | 7.6 | 62.90 | **+1.07** | 61.63 | 1.275 |
| 방전 1 | 15.1 | 61.53 | −1.37 | 61.50 | — |
| 충전 2 · 3 · 4 | 22.5 · 37.1 · 51.6 | 62.64 · 62.44 · 62.28 | **+1.11 · +1.12 · +1.13** | 61.41 · 61.22 · 61.06 | 1.235 · 1.227 · 1.222 |
| 방전 2 · 3 · 4 | 29.9 · 44.3 · 58.7 | 61.33 · 61.14 · 61.00 | −1.31 · −1.30 · −1.27 | | |
| 충전 5–9 (0.25 C) | 61.3–80.7 | 62.05 → 61.84 | +1.05 · +1.04 · +1.04 · +1.01 · +1.00 | 60.96 → 60.79 | 1.093 → 1.052 |
| 방전 5–9 | 63.7–83.1 | 60.96 → 60.80 | −1.09 · −1.09 · −1.07 · −1.05 · −1.04 | | |
| 충전 10 · 방전 10 · 충전 11 | 89.7 · 96.5 · 103.3 | 61.88 · 60.68 · 61.78 | **+1.08** · −1.20 · **+1.10** | 60.72 · — · 60.62 | 1.164 · — · 1.161 |
| 끝 | 109.9 | 60.63 | | 60.58 | |

`[재현]` 원시 110 h 표류 **−1.20 MPa**(61.83 → 60.63) — 한 사이클 진폭과 같은 크기. 골 사이 시간당 하강 **≈0.02 → 0.014 → 0.013 → 0.010 → 0.008(0.25 C 5 사이클 묶음) → 0.009 MPa h⁻¹** —
율을 올려 사이클이 2.5× 잦아진 구간에서도 **시간당** 하강이 이어서 줄어든다. 사이클당으로는 0.1 C −0.30 → −0.14 · 0.25 C −0.03–0.05 · 0.1 C −0.12 MPa.
정점 − 기저선 값은 Fig. 1b 진폭과 **≤0.01 MPa** 로 맞는다(선 두께 몫) — Fig. 1b 의 진폭 = 원시 상승 + 그 충전 동안의 기저선 하강.

**Fig. S6** — 높이(µm), 선 중심.

| 구간 | 시각 (h) | 높이 | 변화 |
|---|---:|---:|---:|
| 시작 → 첫 충전 전(전압 창 밖) | 0.1 → 6.5 | −6.05 → −8.63 | **−2.58** |
| 충전 1 · 방전 1 | → 13.0 · → 18.0 | −9.74 · −12.46 | −1.11 · −2.72 |
| 충전 2 · 방전 2 | → 22.7 · → 27.7 | −12.33 · −14.61 | +0.13 · −2.28 |
| 충전 3–6 | | | +0.29 · +0.36 · +0.45 · +0.51 |
| 방전 3–6 | | | −1.96 · −1.74 · −1.59 · −1.43 |
| 충전 7–11 | | | +0.56 · +0.58 · +0.59 · +0.59 · +0.58 |
| 방전 7–10 | | | −1.32 · −1.25 · −1.18 · −1.09 |
| 사이클 끝 유지 | 95.5 → 98 | −21.70 | 0 |

`[재현]` 논문 ESI 방식(1/3 수직 · ΔVm 7.887 cm³ mol⁻¹ · 0.87 Li/In)으로 10 번째 충전(6.48 mAh g⁻¹ × 10.5 mg)의 예상 두께 증가는 **≈0.10–0.12 µm**(∅10 · ∅9 mm) — 전부 수직으로 몰아도
≈0.29–0.36 µm · LCO 몫 ≈0.01 µm. 관측 상승 ≈0.58–0.59 µm 는 ⅓ 추정의 **≈5–6 배** · 전부 수직 추정의 **≈1.6–2 배**다. 논문은 높이의 크기를 계산과 대조하지 않는다.

# 절별 해체

## 초록 · 서론 (pp. 9929–9930)

- `[인쇄]` "Interestingly, the mechanical effects during operation of SSBs, and their correlation to the electrochemical performance, have rarely been investigated." · 고체에서는 "rigid mechanical coupling
  between the active phases and the solid electrolyte will lead to more complex non-local strain effects than in the common liquid electrolyte-based lithium-ion batteries".
- `[인쇄]` "The continuous volume changes of both the anode and the cathode during lithiation/delithiation are responsible for a **highly reproducible cycle of pressure changes** during the operation of the
  solid-state battery cell. **Bending and cracking** of the solid-state battery cells are observed with X-ray tomography and provide evidence for the critical role of the macroscopic strain generated during
  cycling. Furthermore, these pressure and dilatometry measurements as well as X-ray tomography underline the importance of **external confinement and pressure control** for SSBs."
- `[인쇄]` 서론의 접촉 문장(재인용): "the chemical expansion of working electrodes during lithiation/delithiation may lead to severe microstructural changes, **loss of contact** and poor utilization of the
  active material, as recently shown for Sn–Li alloys.19 During lithiation, the volume expansion becomes so noticeable that **appreciable external pressure is required** to retain the SSB performance.19"
- `[인쇄]` 황화물 SE "extremely low Young's moduli (**18–25 GPa**) and good compressibility, enable cold pressing.20" ↔ 산화물(가닛) "high Young's moduli up to 150 GPa.22".
- `[인쇄]` 목표: "the direct observation of the volume expansion and resulting pressure build-up … by in situ monitoring the pressure changes and dilatometric height variations" · "cell breathing" ·
  zero-strain Li₄Ti₅O₁₂ 대조 · X-CT 로 "the deformation of a non-pressurized battery pellet".

## 실험 (pp. 9930–9931)

- **모델 셀** `[인쇄]`: "A In/Li10GeP2S12/LiCoO2 architecture was chosen as a model cell for all tests in this study due to its stable electrochemical performance (see the ESI†).27 Instead of lithium, indium metal
  was used as the anode in order to avoid any possible side reactions with the thiophosphate solid electrolyte (SE).10" · LCO 표면 LiNb₀.₅Ta₀.₅O₃ 1 wt% 코팅[27].
- **압력 셀**: hot-press setup(유압 + 바닥의 전자 압력 게이지, [28]) · LGPS **80 mg** 을 **∅10 mm Macor™ 실린더**에서 손 압착 → 복합양극 **12 mg**(LCO : LGPS = 70 : 30 wt) 을 "**3.5 tons**" 로
  단축 압착 → 반대편에 In 박 **125 µm · ∅8 mm** 를 "**1.5 tons**" 로 · 양쪽 스테인리스 봉 집전 · **16 h 휴지**("to allow for the relaxation of the plastic components").
  `[재현]` ∅10 mm 면적 0.785 cm² 로 3.5 t → **437 MPa** · 1.5 t → **187 MPa**(In ∅8 mm 면적이면 293 MPa).
- **LTO 셀** `[인쇄]`: "Due to the minor pressure change … and its sensitivity to changes in temperature, the cell was fabricated in an **air-tight cell casing** designed by our group27 and tested in a cabinet
  maintained at 25 °C" · 복합 음극 LTO : SE : C65 = 30 : 60 : 10 wt% · "The cell assembly process is the same as described above".
- **전기화학**: 2.0–3.6 V vs In/InLi(In 셀) · 1.0–2.7 V vs Li₄Ti₅O₁₂/Li₇Ti₅O₁₂(LTO 셀) · LCO 이론 **137 mAh g⁻¹**("based on Li0.5CoO2 as the fully charged state") · **146 · 366 µA cm⁻² = C/10 · C/4** ·
  SP150. `[재현]` 8.4 mg × 137 = 1.151 mAh → C/10 ÷ 0.785 cm² = **146.5 µA cm⁻²** ✓ · C/4 = **366.3** ✓ — **면적 0.785 cm²(∅10 mm)가 정확히 재현된다**. 적재 **10.7 mg LCO cm⁻²** · 이론 1.47 mAh cm⁻².
  `[재현]` 0.62 V 오프셋(본문 [33])이면 2.0–3.6 V vs In/InLi = 2.62–4.22 V vs Li/Li⁺ — 논문은 환산하지 않는다.
- **EIS**: SP300 · "after charging the cells to 3.6 V vs. In/InLi at 0.1C, followed by a resting period of 30 min" · 10 mV · 7 MHz–10 mHz · 10 점/decade.
- **X-CT**: 토모그래피 셀은 "fabricated differently" — SE · 복합체 손 압착 → ∅10 mm 펠릿 한쪽에 In 박막 ∅8 mm → "**isostatically pressed with 4000 bar for 30 min**"(`[재현]` 400 MPa) → 19.1 µA cm⁻²
  "corresponding to a C-rate of 0.03C" 로 3.6 V 까지 충전 · 파우치 밀봉 · **외압 0**. 실험실: 80 kV · 125 µA · 1200 투영 · Hamamatsu 2316 × 2316 · 재구성 화소 **6.25 µm**. 싱크로트론: HZB BAMline(BESSY II) ·
  15 keV · PCO 4000 · 2200 투영 · 화소 **2.15 µm** · Fiji.
- **딜라토미터**: 복합체 15 mg(LCO 10.5 mg) · "A thicker SE membrane (**~1 µm**)"(인쇄 그대로 — D16) 등방 압착 ∅10 mm · In ∅9 mm · EL-Cell **ECD-3-nano** · 28 µA cm⁻² · 2.0–3.6 V.

## 결과 1 — 금속(In) 음극 셀의 압력 (pp. 9931–9932) · Fig. 1 · 2

- `[인쇄]` "The absolute pressure change is shown after subtracting the baseline. (The baseline can be found in the ESI, Fig. S7;† before cycling, a 16 hours' rest time was applied …) The pressure change follow the
  cell potential during charge and discharge process, and the change is **almost linearly with the amount of charge transferred**. During the initial charge, the pressure change is as high as **1.25 MPa**".
- 두 과정: **① LCO** — `[인쇄]` "Coulomb repulsion drives the lattice apart, resulting in a **2% volume expansion along the c-axis** of the unit cell as shown by Dahn and coworkers.30 **Upon lithiation, the induced
  volume contraction again leads to a decrease in pressure.**" — 이 편에서 `contract` 가 나오는 **유일한** 문장(방전 쪽). **② In** — InLi₁₋ₓ(−0.35 < x < 0.13) · In 과 평형인 조성 ≈InLi₀.₈₇[32] ·
  "the Coulometric titration curve of In–Li shows a flat plateau at **0.62 V vs. Li/Li+** in the In-rich region.33 In the case studied here, the anode was kept within this In-rich region (see ESI†) and the volume
  change of the In anode thus depends **linearly on the Li content**" · "roughly doubles the volume (i.e. adds about **42 vol%** per formula unit; see ESI†)" · 정방 → 입방 이방 팽창 — `[인쇄]` "This
  anisotropic volume expansion **may lead to** additional local strain and possible cracking as well as **contact losses at the anode interface**." · "113.23 Å³ … ∼2 times larger than … (55.069 Å³)" ·
  "15.71 → 23.597 cm³ mol⁻¹ … a volume expansion of **105.6%**"(D2 · D3).
- `[인쇄]` 다른 음극: 흑연 C₆Li **10 %** 팽창[35] · Li 금속 "should increase the anode thickness linearly, by approximately **2.2 µm**, with the here employed charge flow"(D5).
- ★ `[인쇄]` 진폭 감소와 감쇠: "Fig. 1a shows that the amplitude of the pressure change … decreases with increasing cycle number. This behavior **corresponds well with the observed capacity fade** of the SSB cells
  (Fig. 1b). The capacity fade corresponds to a partial irreversibility of the lithium intercalation/deintercalation of **both electrodes**. There are many possible reasons … (i) the increasing resistance at the
  **indium/SE interface** at the end of any discharge curve increases the overvoltage …27 (ii) There may be **cracking of the cathode particles as well as of the coating layer** generated by volume expansion,27 …
  (iii) The limited electrochemical window and chemical instability of SEs on the cathode side, may result in **decomposition reactions** at high voltages (e.g. 3.6 V vs. In/InLi) … side products … will accumulate
  at the grain boundaries and influence the mechanical properties of the interfaces, leading to the observed variations in the amplitude of pressure change." — **원인 셋을 나열하고 가르지 않는다; 접촉 손실은
  이 목록에 없다**(Fig. 1b 캡션에는 있다 — D15).
- `[인쇄]` 율: "At higher C-rates, less LiCoO2 is electrochemically activated,27 resulting in less Li+ being transferred into the anode … less expansion occurs and a lower pressure increase is observed. Thus, the
  pressure response of the SSB strongly depends on the amount of Li+ transferred through the cathode material, as well as the speed of the intercalation process."

## 결과 2 — 무변형 음극(LTO) 셀 (pp. 9932–9933) · Fig. 3 · 4

- `[인쇄]` "the data above show that volume expansions of the electrodes lead to a **severe deterioration of the cycling performance**. However, the data above is convoluted by the fact that both the anode and the
  cathode expand during the charging process." — `[해석]` 앞 문장은 상관(Fig. 1b)에서 인과를 적는다.
- `[인쇄]` LTO "only up to **0.2% volume expansion**"[37–39] → "any occurring pressure changes … is associated with the cathode material" · "a **20 times smaller** pressure change is observed … the observed pressure
  increase is **solely due to the expansion of the cathode active material**" · 0.25 C 에서 "less active material is electrochemically addressed,27 and therefore less expansion" · "A direct comparison of the
  pressure change for **both setups** … is shown in Fig. 4."

## 결과 3 — 변형이 미세구조에 미치는 것 (pp. 9933–9934) · Fig. 5 · 딜라토미터(S6)

- `[인쇄]` "In light of the volume expansion of the electrode materials and the subsequent pressure build-up in solid-state cells with a **fixed volume**, we expect that severe strain is generated during cycling" ·
  "we investigated the effect of cycling SSB cells that were **free of uniaxial pressure** … **two identical SSB pellets** … a pristine pellet and … a charged pellet after the 1st charge, in which **no external
  pressure** was applied".
- `[인쇄]` "Significant **bending** … after the 1st charge … The SSB bends towards the cathode side due to the dominant volume expansion of indium … At the edge of the charged pellet, several **cracks** can be seen …
  **Consequently, without any pressure confinement** of the SSB, the contact between electrode particles and interfaces **cannot be maintained** due to the volume expansion during cycling. **Eventually this can lead
  to** a loss of grain contact, and detrimental effects on the electrical (and ionic) connectivity after repetitive cycling will be observed. **This loss of connectivity gives rise to capacity losses and an increase
  in the overpotential, as seen in the present study (Fig. 1).**" — `[해석]` Fig. 1 셀은 **≈62 MPa 구속 셀**(S7)이다 — 무가압 펠릿의 추론을 가압 셀의 감쇠로 옮긴다(D15).
- `[인쇄]` 압밀: "the increasing pressure during charging appears to lead to the **densification** of the SE, as suggested by the more uniform distribution of pores (light areas …)" · 싱크로트론 "the estimated
  porosity is reduced relative to the pristine cell. This observation **may explain** the asymmetric shape of the pressure profile in ESI Fig. S7. After each cycle the pressure is always lower than that at the
  beginning of charge, implying that the entire cell becomes denser upon cycling" · "the volume expansion during charging leads to a concurrent densification and pressure build-up, which is why the observed pressure
  increase is **lower than expected** for the fully dense single crystalline SSB (Fig. 1)."
- `[인쇄]` 딜라토미터(무가압): "only **11.4 mA h g⁻¹** of charge capacity in the first charge and low first cycle coulombic efficiency of **77.2%** … only **6.48 mA h g⁻¹** at the 10th charge … Therefore, **without external
  pressure, intimate contact between the cell components cannot be maintained**" · "a continuous height-change … from the third cycle on. The height of the whole cell increases upon charging, while it decreases during
  discharging" · 공극률 "**5.5% before cycling and 2.6% after cycling**"(< 6.25 µm 제외) · "the consolidation of the SE in the non-pressurized SSB was more significant and required more cycles to equilibrate … Therefore,
  external confinement is of paramount importance in preventing cell bending and **maintaining cathode/SE contact**." — `[해석]` 양극 쪽 관측(양극 부피 0.94 → 0.94 mm³, ESI)은 이 결론을 지지하는 자료가 아니다.
  `[재현]` 이용률 11.4 / 137 = **8 %**(가압 셀 116.7 / 137 = 85 %) — 그러나 두 셀은 압력 말고도 SE 두께 · In 지름 · 전류(28 ↔ 146 µA cm⁻²) · 장치가 다르다.

## 결론 (pp. 9934–9935)

- `[인쇄]` "we demonstrate **quantitatively for the first time** that significant pressure and height changes occur during galvanostatic cycling in SSB cells. Changing from a metal anode to a zero-strain anode
  reveals that the mechanical properties … are **closely related to the resultant electrochemical performance**." — `[해석]` 두 셀의 전기화학 비교는 Fig. 1b ↔ 3b 뿐(0.1 C 11 사이클 −20 % ↔ −9 %, 0.25 C 용량은
  LTO 셀이 더 나쁘다)이고 음극 동역학 · 케이스가 같이 바뀌었다.
- `[인쇄]` "Bending and cracking, generated at the edge of the charged **non-pressurized** SSB … revealing the importance of external confinement which suppresses the effects of the pressure variations, in order to
  maintain the contact required for ionic and electrical conductivity between particles" · "LiNi1−x−yCoxMnyO2 and LiFePO4 exhibit volume changes of **nearly 6% and 6.8%**, respectively.31,40" · "the search for
  stress-free cathode materials is very important and incomplete."

## ESI (12 쪽)

- **① EIS · 장기 사이클** — S1 · S2(첫 충전, "standard SSB setup") · S3(100 사이클 · "80%") — §그림.
- **② in situ XRD** — `[인쇄]` "home-made sample holder … fabricated and charged in the same manner as for the tomography analysis … recorded every 1 h" · "The gradual splitting of the (003) reflection and the steady
  decrease of the (003) Bragg angle indicate an increase in c-axis length, as already reported by Dahn" · "the volume expansion of LiCoO2 upon delithiation contributes to the pressure changes observed."
- **③ 부피 팽창 추정** `[인쇄]`: "In the first charge, a capacity of **1.53 mAh** was achieved" → n(Li) = **5.7×10⁻⁵ mol** · "**89 mg** In foil used as anode, which equals to 774.5 µmol, corresponding to a nominal
  composition of the lithiated In anode of **InLi0.0736**" · "The constant potential of the two-phase anode is maintained throughout the entire battery cycling, as In is in equilibrium with indium-rich InLi0.87" ·
  InLi₀.₈₇ **65.5 µmol** · "about **8 %** of the In metal is lithiated" · "we can assume that **one third** of the total volume expansion contributes to the volume expansion in the vertical direction, which is **35.2 %**" ·
  ΔV = (23.597 − 15.71) × 65.5×10⁻⁶ = **516.6×10⁻⁶ cm³** → ⅓ = 172×10⁻⁶ cm³ → "Considering the **cell area of 1.103 cm²**, the vertical displacement … **1.56 µm**" · Li 금속이면 **2.2 µm**(12.97 cm³ mol⁻¹) ·
  LTO ≈0.2 % · 흑연 10 % · LCO "**14 mg** … 2.76×10⁻³ cm³ (… 5.07 g/cm³) … 2 % … 5.52×10⁻⁵ … one third … 1.84×10⁻⁵ cm³ … **0.163 µm**" · "it is not possible to fully gauge the expected pressure build up …
  all estimates of pressure build-up are theoretical upper limits." `[재현]` 5.708×10⁻⁵ mol ✓ · 65.6 µmol ✓ · 8.47 % ✓ · x = 0.0737 ✓ · 516.8×10⁻⁶ ✓ · 1.564 µm ✓ · Li 6.71 → ⅓ **2.24 µm**(✓ — ⅓ 을 곱한 값) ·
  LCO **0.167 µm**(인쇄 0.163, 2.4 %).
- **④ X-CT 부가** `[인쇄]`: SE 공극률(void ÷ 전체 SE 부피) **5.45 % → 2.58 %**(< 6.25 µm 제외) · 부피: pristine 양극 **0.94** · SE **21.32** · 음극 **1.89 mm³** / charged 양극 **0.94** · SE **24.85** · 음극 **5.93 mm³**(D9) ·
  S5. ⚠ 이 절은 토모그래피를 "**Figure 6 a)**"(S5 캡션 "**Fig 4 a)**")로 부른다 — 본문은 Fig. 5a(D11).
- **⑤ 딜라토미터** — S6. `[인쇄]` "An inclined baseline of the height-change curve indicates the consolidation of the SE caused by the pressure generated by the lattice expansion of electrode material."
- **⑥ 압력 기저선** — S7. `[인쇄]` "Similarly, an inclined baseline is observed in the SSB In/SE/LiCoO2 used for the pressure monitoring … The corresponding plot after the subtraction of baseline is shown in Figure 1."

## 참고문헌 40 편 — 우리 축에 닿는 것

[10] Wenzel … Zeier, Janek 2016 *Chem. Mater.* 28, 2400(LGPS 는 Li 금속에 불안정 · In 음극 선택 근거) · [19] Whiteley … Lee 2015 *JES* 162, 711(Sn–Li 합금 — 접촉 손실 · 외압 필요) ·
[20] Sakuda, Hayashi, Tatsumisago 2013 *Sci. Rep.* 3, 2261(황화물 SE 탄성률 18–25 GPa) · [27] Zhang W. … Janek 2016 "submitted"(모델 셀 · 코팅 · EIS · 율 이용률) · **[28] Busche … Janek 2016 *Chem. Mater.* 28, 6152
(hot-press 장치)** · [30] Reimers & Dahn 1992 *JES* 139, 2091(LCO c 축) · **[31] Kondrakov … Janek 2017 *J. Phys. Chem. C* 121, 3286(NCM "nearly 6%")** · [32] Alexander … Calvert 1976 *Can. J. Chem.* 54, 1052(InLi₀.₈₇) ·
**[33] Takada, Aotani, Iwamoto, Kondo 1996 *Solid State Ionics*(0.62 V 평탄 — 인쇄 권 "2738")** · [35] Qi … Timmons 2010 *JES* 157, A558(흑연 10 %) · [36] Zhang W.J. 2011 *JPS* 196, 13(Li 몰부피) ·
[37] Ohzuku 1995 · [38] Wagemaker 2006 · [39] Haetge 2011(LTO 무변형) · [40] Padhi 1997(LFP 6.8 %).

# 어휘 집계 — NFKC 정규화 · 합자 복원 후, 대소문자 무시 (본문 · 캡션 | 참고문헌 | ESI)

| 지문 열 | 본문 | 참고문헌 | ESI | 메모 |
|---|---:|---:|---:|---|
| `identifiab` · `uncertaint` · `error` · `standard deviation` · `±` | **0** | 0 | 0 | 셀 수(`n =`) 0 · 오차 막대 0 |
| `LLI` · `LAM` · `OCV` | **0** | 0 | 0 | `degradation` 1 · `capacity` 14 · `fade/fading` 4 |
| `EIS` · `impedance` · `overpotential/overvoltage` | 1 · 2 · 4 | 0 | 8 · 4 · 0 | EIS 는 첫 충전(ESI)뿐 |
| `contact` | **10** | 0 | 0 | 셀 관련 9 — 전부 추론 · 재인용 · 결론(§(b) 표) · 1 은 "contact with ambient air" |
| `contact loss` · `loss of (grain) contact` | 4 | 0 | 0 | Fig. 1b 캡션 · p. 9932(음극 계면, "may lead to") · 서론(재인용) · p. 9933 |
| `pressure` | **76** | 0 | 12 | |
| `stack pressure` | **0** | 0 | 0 | |
| `external pressure` · `non-pressurized` · `confinement` | 6 · 7 · 5 | 0 | 0 · 3 · 1 | |
| `MPa` | **1** | 0 | 0 | "1.25 MPa" 하나 — 운전 압력 값 0(S7 축에만) |
| `bar` · `ton(s)` | 1 · 2 | 0 | 0 | 조립 가압(4000 bar · 3.5 / 1.5 tons) |
| `fixed volume` · `hot-press` · `gauge` · `load cell` · `stiff` | 1 · 1 · 1 · **0** · 1 | 0 | 0 · 0 · 1 · 0 · 0 | `stiff` 1 = 가닛 SE("mechanically stiff") — 지그 강성 0 |
| `expan` · `contract` · `compress` | 43 · **1** · 8 | 0 | 23 · 0 · 0 | `contract` 1 = LCO 방전 수축 |
| `breathing` · `dilatomet` · `tomograph` | 3 · 9 · 24 | 0 | 0 · 4 · 5 | |
| `baseline` · `consolidat` · `densif` | 4 · 3 · 4 | 0 | 9 · 6 · 1 | |
| `crack` · `bend` · `pore/porosity` · `void` | 6 · 6 · 8 · 0 | 0 · 2 · 0 · 0 | 0 · 0 · 9 · 2 | 참고문헌 `bend` 2 = 저자명 Bender |
| `creep` · `yield` · `fatigue` · `dendrit` | **0** | 0 | 0 | 61호의 눈금 어휘는 이 편에 없다 |
| `indium` · `Li4Ti5O12` · `zero-strain` · `Li metal` | 15 · 18 · 4 · 6 | 0 | 7 · 2 · 0 · 3 | |
| `strain` · `stress` · `correlat` · `temperature` · `reproducib` | 25 · 3 · 3 · 2 · 1 | 0 | 0 | |

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/62** | 사이클 시계열: 압력 진폭 11 점(In · LTO) · 용량 · 원시 압력 110 h(S7) · 높이(S6, 무가압) — 접촉량 0. 셀 관련 `contact` 9 개는 전부 재인용 · 추정("may lead to") · 무가압 셀에서의 추론 · 결론(§(b)) |
| **Q2** 독립 관측 | **부분 — 채널 다섯, 가르는 용도 0** | ① in situ 압력(hot-press · In 셀 / air-tight casing · LTO 셀) ② 딜라토미터(무가압) ③ X-CT 실험실 6.25 µm · 싱크로트론 2.15 µm(무가압 두 펠릿) ④ in situ XRD(x 1 → 0.743) ⑤ EIS(첫 충전, 다른 장치). ★ 음극 교체(LTO)는 **압력 채널의 전극 분해** — `[재현]` 음극 몫 ≈90–95 %. ⚠ 채널들이 **다섯 개의 다른 셀**(압력 · EIS/S3 · CT · XRD · 딜라토)에 흩어져 있어 서로 대질되지 않는다. 양극 `LAM_PE` ↔ 접촉 손실을 가르는 관측 0 |
| **Q3** 라벨 층위 | **measured-mechanical(in situ, 기저선 보정본) + literature-derived(2 % · Vm) + calculated(⅓ 규칙)** — 오차 0 · 셀 수 0 | 원시 ↔ 보정이 추이의 방향을 바꾼다(원시 충전 상승 평탄 ↔ 보정 진폭 −9 %). 공극률은 두 펠릿 · 문턱 분할 · 6.25 µm 해상 한계 위 |
| **Q4** 유일성·식별성 | **0/62 — 쉰네 번째 성질** "압력 진폭 감소를 용량 감쇠와 '잘 상관' 한다고 적고 접촉 손실의 지표로 읽지만, 진폭은 전달 전하에 선형이라 따라가는 것이 구성상이고 · 진폭 감소의 크기는 기저선 규약 몫과 같으며 · 같은 지면에 감쇠 원인 넷(In 계면 · 입자/코팅 균열 · SE 분해 · 접촉 손실)을 나열하고 가르지 않는다" | `identifiab` · `uncertaint` · `error` · `±` 0 |
| **Q5** Li-In 기준 | **층 하나 — "공칭 조성으로 창 안임을 계산한다"(전위 측정 0)** | `[인쇄]` "flat plateau at 0.62 V vs. Li/Li+ in the In-rich region"[33] Takada 1996 · InLi₀.₈₇ 평형[32] · ESI "The constant potential of the two-phase anode is maintained throughout the entire battery cycling" · 공칭 InLi₀.₀₇₃₆(ESI 셀). `[재현]` 압력 셀: In 125 µm × ∅8 mm = **400 µmol**(인쇄 Vm 15.71 · ESI 의 89 mg ↔ 774.5 µmol 로 M 114.9) · 첫 충전 0.98 mAh → **InLi₀.₀₉₁ ≈8.4 at% Li** — 42호가 잰 평탄 창(≈1–47 at%) 안. 기준극 0 |
| **Q6** 압력 | **칸 이동 없음 — 층 다섯** | ① **운전 중 압력 변화의 계보 첫 1차 측정(2017)** — 그러나 **운전 압력 값은 본문 0**(S7 축 ≈60.6–62.9 MPa) ② **요구치 · 문턱 인쇄 0** — "external confinement is of paramount importance"(값 0) ⇒ 요구치 띠 0.1–5 MPa · 확인된 원전 0 **그대로** ③ 제조 압력은 힘 · bar(3.5 t · 1.5 t · 4000 bar) — 운전과의 분리 명시 0 ④ 무가압 대조는 **다른 셀**(딜라토 · CT) — 압력만 바꾼 대조 0 ⑤ **기저선 규약 · 지그 강성이 ΔP 의 크기와 추이를 정한다** |
| **Q7** dead Li · Li 재고 | **해당 없음**(In 음극 · 무 Li 조립) · 층 하나(`[해석]`) | 방전 말 In 에 남은 Li 는 잔류 팽창 → 방전 말 압력을 **올려야** 하는데 원시 골은 −0.30 → −0.12 MPa/사이클로 **내려간다** — 표류가 덮고 기저선 제거가 둘 다 지운다. Li 금속 두께 "2.2 µm" 는 ⅓ 규칙(평면 석출이면 `[재현]` 6.7–9.4 µm) |
| **Q8** 화학·OCP | **층 하나** | LCO(LiNb₀.₅Ta₀.₅O₃ 1 wt%) · 137 mAh g⁻¹ = Li₀.₅CoO₂ · 2.0–3.6 V vs In/InLi · LCO 평탄 3.3 V vs In/InLi(S2 캡션) · in situ XRD 1차 상전이(정성) · OCP 곡선 0 · dQ/dV 0 · NCM "nearly 6%" · LFP 6.8 %(재인용, 방향 0) |

# ★ (a) 압력 변화의 크기 · 부호 · 추이 — 어떤 셀에서인가

## (a-1) 셀 사양 — 네 가지 셀이 한 논문에 섞여 있다

| 항목 | **In 압력 셀**(Fig. 1 · 4 · S7) | **LTO 압력 셀**(Fig. 3 · 4) | **딜라토미터 셀**(S6) | **CT · XRD 펠릿**(Fig. 5 · S4 · S5) |
|---|---|---|---|---|
| 양극 | LNTO(1 wt%)-LCO : LGPS = 70 : 30, **12 mg**(LCO 8.4 mg) | "rest of the battery composition unchanged" | 15 mg(LCO 10.5 mg) | 적재 0 |
| SE | LGPS **80 mg**, ∅10 mm Macor 실린더, 손 압착 | (같음으로 읽힌다) | "~1 µm"(인쇄 — D16) 등방 압착 ∅10 mm | 손 압착 ∅10 mm |
| 음극 | In 박 **125 µm × ∅8 mm**(`[재현]` 400 µmol · 45.9 mg) | LTO : SE : C65 = 30 : 60 : 10 wt%(적재 0) | In ∅9 mm(두께 0) | In 박막 ∅8 mm(두께 0) |
| 조립 가압 | 양극 **3.5 t** · In **1.5 t**(`[재현]` ∅10 mm 로 437 · 187 MPa) | "same as described above" | 등방 | **등방 4000 bar 30 min**(400 MPa) |
| 면적 | `[재현]` **0.785 cm²**(C/10 = 146 µA cm⁻² 재현) · 적재 10.7 mg LCO cm⁻² | | | |
| 운전 구속 | hot-press(유압 + 바닥 전자 게이지) · **기저 ≈61.8 MPa**(`[도표]` S7 — 본문 0) · "fixed volume" | **air-tight cell casing · 25 °C 캐비닛** · 기저 0 | 무가압(ECD-3-nano) | **외압 0**(파우치) |
| 휴지 | 16 h("relaxation of the plastic components") | | (첫 ≈6.5 h 로 읽힘) | |
| 전류 | 146 · 366 µA cm⁻²(0.1 · 0.25 C) | 같음 | 28 µA cm⁻² | 19.1 µA cm⁻²(0.03 C) |
| 창 · 온도 | 2.0–3.6 V vs In/InLi · 25 °C(캡션) | 1.0–2.7 V vs LTO · 25 °C | 2.0–3.6 V · 0 | → 3.6 V · 0 |
| 사이클 | 11(0.1 C 4 · 0.25 C 5 · 0.1 C 2) | 11 | 11 충전 · 10 방전 | 첫 충전 1(XRD 는 18 h 까지) |
| 셀 수 | 1(명시 0) | 1 | 1 | pristine 1 · charged 1 |

`[해석]` 원장이 묻는 "초기 압력 · 지그 강성" 은 **In 압력 셀에서 초기 압력만 그림으로 있고(≈61.8 MPa), 강성은 없다**. LTO 셀은 둘 다 없다.

## (a-2) 크기 · 부호 — 본문 값 하나, 나머지는 그림

- **부호**: `[인쇄]` "The pressure increases almost linearly during charging, and decreases during discharging … the SSB experiences volume expansion during charging, and compression during the discharge"(Fig. 1 캡션) —
  LCO(c 축, 탈리튬 팽창)와 In(→ InLi, 리튬화 팽창)이 **둘 다 충전에 팽창**한다. LTO 셀도 충전 ↑(LCO 만).
- **크기**:

| | 원시(S7 `[도표]`) | 기저선 보정(본문 `[인쇄]` · Fig. 1b `[도표]`) |
|---|---|---|
| 기저(절대) | **61.83 MPa**(시작) → 60.63(110 h) | 제거 |
| 첫 충전 | **+1.07 MPa** | **1.25**(인쇄) · 1.267 |
| 0.1 C 충전 2–4 | +1.11 · +1.12 · +1.13 | 1.227 · 1.218 · 1.205 |
| 0.25 C 충전 5–9 | +1.05 → +1.00 | 1.083 → 1.041 |
| 0.1 C 충전 10–11 | +1.08 · +1.10 | 1.154 · 1.152 |
| 방전 하강 | −1.37 → −1.27(0.1 C) · −1.09 → −1.04(0.25 C) · −1.20 | 0 으로 복귀(구성상) |
| LTO 셀 | (원시 0) | ≈0.067(0.1 C) · ≈0.041(0.25 C) — 평탄 |

## (a-3) ★★★ 추이 — 압력/용량 비가 움직인다

- `[재현]` 기저선 보정 진폭/용량 **1.086 → 1.236 MPa per 100 mAh g⁻¹(+14 %)**(§픽셀 판독) · 원시 충전 상승/용량 **0.92 → 1.18(+29 %)** — 0.1 C 끼리 비교해도 같은 방향.
- `[재현]` Fig. 1b 진폭 = 원시 상승 + 충전 동안의 기저선 하강 — 첫 충전의 기저선 몫 ≈**0.20 MPa**, 넷째 ≈0.08 ⇒ **0.1 C 1 → 4 사이클의 진폭 감소(1.267 → 1.205, −0.06)는 기저선 몫의 감소(−0.12)보다 작다**. 원시 상승은
  같은 구간에 **+0.06** 이다.
- `[해석]` 비가 커지는 원인 후보 셋 — (i) **셀이 굳는다**(압밀로 공극이 줄어 같은 팽창에 더 큰 압력 — 이 편 자신의 서사) (ii) **초기 용량에 Δx 없는 전하가 섞였다**(부반응 · SE 분해 — 초기에 크다) (iii) 기저선 규약.
  지면은 셋을 가를 자료를 주지 않는다. 어느 쪽이든 **압력 진폭은 용량의 비례 대리가 아니다**.
- LTO 셀: 용량 −9 % 동안 진폭 **0 %**(0.0669 → 0.0669; 잡음 폭 ≈±0.005). 율 전환에서만 진폭 ↔ 용량(63 % ↔ 60 %)이 같이 움직인다.
- `[재현]` 음극 교체로 본 전극 몫: In ÷ LTO 진폭 ×18.9 · 비 ×14.7 · Fig. 4 기울기 ≈×17 ⇒ 양극 몫 ≈5–7 %(같은 강성 가정); ESI 두께 계산은 9.5 % ⇒ **압력 신호의 ≈90–95 % 는 음극(In)** 이다. ⚠ 두 셀의 케이스가 다르다(G5).

# ★ (b) "부피 수축 → 접촉 감소" — 측정인가 추론인가

**수축은 이 셀의 충전에 없다.** `contract` 는 본문 1 회 — `[인쇄]` "Upon lithiation, the induced volume contraction again leads to a decrease in pressure"(LCO, **방전**). 충전 수축(NCM)은 이 편의 셀이 아니고,
결론의 NCM 문장은 `[인쇄]` "volume changes of nearly 6%"[31] 로 **방향이 없다**.

**접촉 손실의 근거 — `contact` 본문 10 회를 전부 분류:**

| # | 자리 | 원문 | 층위 |
|---|---|---|---|
| 1 | 서론 p. 9930 | "severe microstructural changes, loss of contact and poor utilization of the active material, as recently shown for Sn–Li alloys.19" | 재인용([19] Whiteley 2015) |
| 2 | X-CT 방법 | "To avoid contact with ambient air" | 무관 |
| 3 | **Fig. 1b 캡션** | "indicative of irreversible processes at the electrode/electrolyte interfaces and **particle contact loss** due to the 'breathing' of the SSB" | **추론** — 용량 ↔ 압력 진폭 상관에서(§(a-3): 비례 아님) |
| 4 | p. 9932 | "This anisotropic volume expansion **may lead to** additional local strain and possible cracking as well as contact losses at the anode interface" | 추정 — In 이방 팽창(음극) |
| 5–7 | p. 9933 | "without any pressure confinement … the contact … **cannot be maintained** … Eventually this **can lead to** a loss of grain contact … trying to maintain particle contact" | **추론** — **무가압** 펠릿(첫 충전 1 회)의 휨 · 가장자리 균열 영상에서 |
| 8 | p. 9934 | "without external pressure, intimate contact between the cell components cannot be maintained, resulting in poor charge–discharge performance" | **추론** — 무가압 딜라토미터 셀의 낮은 용량(11.4 mAh g⁻¹)에서 |
| 9 | p. 9934 | "external confinement is of paramount importance in preventing cell bending and **maintaining cathode/SE contact**" | 결론 — 양극 쪽 관측 0(ESI 양극 부피 0.94 → 0.94 mm³) |
| 10 | 결론 p. 9935 | "in order to maintain the contact required for ionic and electrical conductivity between particles" | 결론 |

⇒ **측정 0 · 추론 셋 · 재인용 하나 · 결론 둘.** 추론의 두 줄기(X-CT · 딜라토)는 **무가압** 셀이고, 그 결론을 `[인쇄]` "This loss of connectivity gives rise to capacity losses and an increase in the overpotential,
as seen in the present study (**Fig. 1**)" 로 **≈62 MPa 구속 셀**의 감쇠에 붙인다(D15). 같은 지면 p. 9932 의 감쇠 원인 목록(In 계면 · 입자/코팅 균열 · SE 분해)에는 접촉 손실이 없다.

**카드 Q1(`θ(N)`)에 들어오는 것: 없다.** 사이클 축의 시계열은 압력 진폭(In · LTO) · 원시 압력 · 용량 · 높이(무가압)뿐이다. `[해석]` 그중 압력 진폭은 (ㄱ)의 이유로 입자 고립과 `LAM_PE` 를 같은
서명으로 본다 — **접촉 손실 시계열의 후보조차 아니다**.

# ★ (c) 60호 S14 · 61호와 같은 눈금에서 비교할 수 있는가

| 항목 | **62호(이 편) In 셀** | **60호 S14** | **61호** |
|---|---|---|---|
| 셀 | In ‖ LGPS ‖ LCO(LNTO) | Li₂₁Si₅/Si–Li₂₁Si₅ ‖ Li₆PS₅Cl ‖ Li₃InCl₆ ‖ LCO | 셀 0(벌크 Li) |
| 기저 | **≈61.8 MPa**(S7 `[도표]`, 본문 0) | 예압 **0.8 MPa**(인쇄 "minimum pressure load") | — |
| 구속 | hot-press 유압 + 게이지("fixed volume") | 정변위(두께 제한) · 사양 0 | 벌크 시편 정하중 |
| 온도 · 환경 | 25 °C | 45 °C · 공기 < 10 % RH | 실온 ≈26 °C |
| 첫 충전 ΔP | **+1.25**(인쇄, 보정) · **+1.07**(원시) | **+1.51**(인쇄) | — |
| 면적 용량 | `[재현]` 1.25 mAh cm⁻²(116.7 × 8.4 mg / 0.785) | `[재현]` ≈2.9(0.28 mA cm⁻² × ≈10.5 h — 60호 digest 판독) | — |
| ΔP / 면적 용량 | ≈**1.0**(보정) · ≈0.86(원시) MPa per mAh cm⁻² | ≈**0.52** | — |
| 사이클 추이 | 보정 진폭 −9 %/11 · 원시 상승 평탄 · 원시 기저 −1.2 MPa | ≈1.2 → 1.05(4 사이클) · 방전 말 기저 복귀 | — |
| 기저 ÷ Li 항복(0.73–0.81, 61호) | **≈76–85×** | ≈1× | 1 |

- `[재현]` **ΔP 는 셀이 아니라 구속계가 정한다** — 압력 셀의 두께 증가를 ESI 방식(⅓ 규칙)으로 내면 In 1.41 + LCO 0.12 = **≈1.53 µm**(0.785 cm²). 이 변위를 셀 적층의 탄성만으로 받으면
  ΔP ≈ E · Δh / L; 인쇄된 황화물 SE 탄성률 18–25 GPa 로 관측 ΔP 1.07–1.27 MPa 를 내는 유효 길이는 **L ≈22–36 mm**. 셀 적층(두께 인쇄 0)은 `[해석]` 밀도를 1 g cm⁻³ 로 낮게 잡아도 ≲1.3 mm ⇒
  변위의 **≥94 %** 는 셀 탄성 밖(지그 · 유압 기둥 · 게이지 순응, 또는 공극 압밀 · In 소성 흐름 — In 박 ∅8 mm 가 다이 ∅10 mm 보다 작아 옆으로 흐를 자리가 있다; In 물성은 이 편에 0)에서 흡수된다.
  전부 수직으로 몰면(Δh ≈4.6 µm) L 은 ≈65–110 mm 로 더 길어진다.
- ⇒ `[해석]` **두 편의 "≈1–1.5 MPa" 는 같은 자릿수의 우연이지 같은 눈금이 아니다** — ΔP 는 (지그 강성) × (음극 팽창) 의 곱이고, 60호와 이 편은 곱의 두 인자가 다 다르다(Si 계 ↔ In · 0.8 ↔ 61.8 MPa 기저 ·
  사양 0 ↔ 사양 0). 면적 용량당 ΔP 가 ×1.9 다른 것을 음극 화학으로도 강성으로도 배정할 수 없다.
- **61호 눈금**: 이 셀의 음극은 In 이라 Li 눈금(항복 · creep `n` 6.56)은 직접 적용되지 않는다. 걸리는 곳은 둘 — (i) 이 편의 가정 "Li 금속 음극이면 ≈2.2 µm" 는 ⅓ 규칙을 평면 석출에 곱한 값이다
  (`[재현]` 6.7 µm @ 1.103 cm² · 9.4 µm @ 0.785 cm²) (ii) 이 셀의 기저 ≈61.8 MPa 는 61호 눈금으로 σ/G ≈2.2×10⁻² — power-law breakdown 영역(> 2.83 MPa)의 한가운데다. `[해석]` 같은 지그에 Li 금속을 넣으면
  압력 호흡은 Li 흐름(초–분 척도)으로 풀려 이 편의 In 셀 삼각파와 같은 모양일 이유가 없다. 원시 기저의 **감쇠형 표류**(0.02 → 0.009 MPa h⁻¹)는 61호 압축 시험의 시간 의존 변형(속도가 시간에 따라 준다)과
  **모양이 닮았을 뿐** 재료가 다르다.

# ★ (d) 22호 셀 장치의 원전으로서 — 22호 G5 에 무엇을 주는가

| 항목 | 22호 Strauss 2018(digest) | 이 편 압력 셀 | 이 편 다른 셀 · 23호 |
|---|---|---|---|
| 양극 다이 | **미기재(G5)** · `[재현]` 0.66–0.80 cm²(∅9.2–10.1 mm) | `[인쇄]` **∅10 mm Macor 실린더** → `[재현]` 0.785 cm² · C/10 · C/4 전류밀도 정확히 재현 | CT · 딜라토 ∅10 mm 펠릿 · **23호 `[재현]` ∅10 mm · 8.4 mg AM(12 mg × 70 %)** |
| In | 100 µm · ∅8 mm · 125 MPa | 125 µm · ∅8 mm · 1.5 t(`[재현]` 187 MPa) | CT ∅8 · 딜라토 ∅9 · 23호 ∅6 mm |
| SE | 60 mg · ≈125 MPa → ≈400 µm | LGPS 80 mg 손 압착 | |
| 양극 부착 | 10–12 mg · 375 MPa · 1.9 mAh cm⁻² | 12 mg · 3.5 t(`[재현]` 437 MPa) · 이론 1.47 mAh cm⁻² | 23호 35 kN ≈445 MPa |
| 운전 압력 | 55 MPa | **본문 0** · `[도표]` S7 ≈61.8 MPa | 23호 ≈70 / 64 MPa |
| 장치 원전 | "setup described elsewhere" → ref 18(이 편) | "hot-press setup" → **[28] Busche 2016** · EIS "standard SSB setup" → **[27]**(submitted) | |
| ⚠ | | ESI 계산 "**cell area of 1.103 cm²**"(∅11.85 mm) — 22호 역산 범위 밖 | |

⇒ **⚠ 부분.** 이 편은 **다이 지름(∅10 mm)** 을 인쇄하고, 그 면적이 전류밀도 · C-율로 정확히 재현된다 — 22호 역산 범위 안이고 같은 연구망 23호의 역산(∅10 mm · 8.4 mg)과도 같다. 그러나
(i) **장치는 다시 [28] · [27] 로 위임**된다 — 22호의 "setup described elsewhere" 가 가리킨 원전은 이 편에서 한 번 더 넘어간다 (ii) 조립 가압(437/187 ↔ 375/125 MPa) · In 두께(125 ↔ 100 µm) · 운전 압력
(≈62 ↔ 55 MPa)이 다르다 — 22호 셀이 이 셀과 같은 다이를 썼다는 것은 22호의 한 줄에만 걸려 있다 (iii) ESI 는 다른 면적(1.103 cm²)을 쓴다. `[해석]` 22호 G5 에는 **"0.785 cm²(같은 연구망의 인쇄 지름 ∅10 mm —
조건부)"** 를 적을 수 있다 — 확정값은 아니다.

# 귀속 검사 — 22 · 23 · 33 · 59호(+ 카드의 6호 기록)가 이 편에 매단 것

| 인용처 | 매단 명제 | 이 편 | 판정 |
|---|---|---|---|
| 22호 ref 18(22호 digest :81) | 셀 장치 — "setup described elsewhere"(양극 면적/지름) | ∅10 mm Macor · In ∅8 mm 인쇄 · `[재현]` 0.785 cm² 재현; 장치 → [28] · EIS → [27] · ESI 1.103 cm² | ⚠ **부분** — 지름은 주고 장치는 다시 위임 |
| 22호 refs 9, 18(22호 digest :148 · :524) | "**volume contraction during charging** leads to a reduced electrical contact between the CAM particles and the SE" | 양극 LCO 는 **충전 팽창** · `contract` 1 회 = 방전 · NCM 은 "nearly 6%"(방향 0) · 접촉 손실은 무가압 셀의 추론 | ❌ **ref 18 다리** — "충전 수축" 은 ref 9(= 23호 Koerver 2017, NCM811)의 명제 |
| 23호 ref 40(서론 범위 인용) | 23호 digest 에 전사 0 | — | 판정 불가 |
| 23호 ref 40 | "LiCoO₂ undergoes an overall expansion of the unit cell" | `[인쇄]` "shows an expansion of the unit cell upon deintercalation" · "2% volume expansion along the c-axis"[30] · ESI XRD 정성 | ✅ — 수치는 [30] Reimers & Dahn 재인용 |
| 33호 [89] Fig.(F)(33호 digest :138) | X-CT pristine ↔ charged 단면 곡률 `R₁` → `R₂` + 평면 CT 원판 2 장 | 원 Fig. 5a 에 `R₁` · `R₂`(주황 곡선) · 원판 2 — **수치 0** | ✅ |
| 33호 [89](33호 digest :138) | "the pressure also induced noticeable cracks at the edges of the electrolyte, causing **contact loss**" | 균열 ✅ "At the edge of the charged pellet, several cracks" · "causing contact loss" = 원문 **추론** · 셀은 **외압 0** 펠릿(여기 "pressure" 는 내부 응력) · 충전 1 회 | ⚠ 관측 ✅ · 인과 ⚠ |
| 33호 [89](33호 digest :227) | "if the battery is not subjected to external pressure during cycling, electrode expansion could prevent tight contact … ultimately leading to battery failure" | "without any pressure confinement … the contact … cannot be maintained due to the volume expansion during cycling" · 서론 "in order to prevent long-term mechanical failure" | ✅ 의역 — 단 "cycling" 은 충전 1 회 영상 · "failure" 는 전망 |
| 33호 digest :138 분류 | "음극/SE 쪽 명제" | 휨 = In 팽창 · 균열 = SE 가장자리 ✅ — 단 이 편 결론은 "maintaining **cathode**/SE contact" 로 넓힌다(양극 관측 0) | ✅ 분류 · ⚠ 원문의 확장 |
| 33호 digest :383 | "33호의 서술(X-CT 휨)과 원장 서술(압력 감시)이 다른 측면" | 둘 다 이 편에 있다 — 단 X-CT(외압 0 펠릿)와 압력(≈62 MPa 구속 셀)은 **다른 셀** | ✅ 해소 |
| 59호 ref 23(59호 digest :268) | "Stack pressure can mirror electrochemical behaviour as it changes periodically with the electrochemical process" | "The pressure change follow the cell potential … almost linearly with the amount of charge transferred" · "highly reproducible cycle of pressure changes" | ✅ — 기저선을 뺀 그림에서(원시 −1.2 MPa/110 h). 59호 다음 문장(진단)은 refs 24–26 |
| 6호 ref 46(카드 Status Log 6호 항) | "운전 중 압력 변화 실측; G12(정압/정변위)의 답이 여기 있을 수 있다" | 실측 ✅ · 이 편의 hot-press 셀은 충전에 압력이 **오른다**(= 정하중 제어가 아니다) — 6호(SAIT) 지그와 무관 | ✅ 실측 · ❌ G12 |
| 원장 §1 행 | "22호 셀 장치의 원전(양극 면적 미기재) + **충전 중 부피 수축 → 접촉 감소**를 **압력으로 감시**한 근거" | 위 전부 | ⚠ 앞 절반 · ❌ 뒤 절반 — 정정 필요(wiki 밖) |

# 인용 대조 — 우리 위키 · 원장에 원전 · 관련 digest 가 있는 것

| 이 편 인용 | 우리 호 · 원장 | 이 편이 적은 것 | 대조 |
|---|---|---|---|
| [27] Zhang W., Weber, Weigand, Arlt, Manke, Schröder, Zeier, Janek 2016 "submitted"(= ESI [1]) | 원장 ★★★★ **Zhang 2017 *ACS AMI* 9, 17835**(지목 22 · 23 · 24 · 39 · 41 · 42 = 6) — 같은 편 가능성 | 모델 셀 안정성 · 코팅 · "less LiCoO2 is electrochemically activated" at higher C-rates · In/SE 계면 저항 · 입자/코팅 균열 · "standard SSB setup" · EIS 배정 | 미확인 — 같은 편이면 지목 7 |
| **[28] Busche … Janek 2016 *Chem. Mater.* 28, 6152** | 원장 **0** | hot-press 장치("Detailed information on the apparatus") | **신규** — G1(강성 · 조절 방식)의 확인처 |
| **[31] Kondrakov … Janek 2017 *J. Phys. Chem. C* 121, 3286** | 원장 ★★★(지목 23, 1) · 23호 G1("부피 변화 % 가 없다") | NCM "volume changes of nearly 6%" | 23호 G1 의 빈칸에 **같은 연구망 편이 ≈6 % 를 인쇄** — 방향 · 조성 0 · **지목 2** |
| **[33] Takada, Aotani, Iwamoto, Kondo 1996 *SSI*** | 원장 ★★★(지목 20 · 42, 2) · 42호 digest [18] "86–88, 877" | "flat plateau at 0.62 V vs. Li/Li+ in the In-rich region" | 이 편 인쇄 권 "2738"(D21) · **지목 3** |
| [19] Whiteley, Kim, Kang, Cho, Oh, Lee 2015 *JES* 162, 711 | 원장 0 | Sn–Li: "loss of contact … appreciable external pressure is required" | 신규 — 이 편 서론 접촉 문장의 원전 |
| [20] Sakuda, Hayashi, Tatsumisago 2013 *Sci. Rep.* 3, 2261 | 원장 1 회 언급 | 황화물 SE 탄성률 18–25 GPa | §(c) 유효 길이 계산의 입력 |
| [30] Reimers & Dahn 1992 *JES* 139, 2091 | 0 | LCO c 축 · "2 %" | 신규(★) |
| [10] Wenzel … Janek 2016 *Chem. Mater.* 28, 2400 | 42호 후속 목록 | LGPS 는 Li 금속에 불안정 → In 음극 | |
| (이 편 이후) Koerver 2018 *EES* | 원장 ★★★ · 33호 [58] 재수록 "LCO/NCM 양극 ≈0.05–0.07 MPa" | LTO 압력 자료 제공자 "R. K." | `[해석]` 33호 재수록 양극 ΔP 와 이 편 LTO 셀 ≈0.067 MPa 가 같은 자릿수 — 같은 측정 계열일 가능성(미확인) |

⚠ 이 편(2017-05)은 22호(2018) · 23호(2017-06) · 33 · 59 · 60 · 61호를 인용할 수 없다 — 시점. 23호 Koerver 2017 과는 저자 Koerver 가 겹치고 LTO 자료를 공유한다.

# ★ 카드의 틀로 — 이 편이 우리 3 항 분해에 들어가는 자리 (`[해석]`)

## (ㄱ) 압력 채널의 관측 연산자 — `P(t) = P_base(t) + k_eff(N) · [Δh_an(q) + Δh_ca(q)]`

이 편의 지면을 한 식으로 적으면 위와 같다. `Δh_e ∝ (그 전극에서 실제로 Δx 를 겪은 활성 부피) · Δx_e`.
- **음극 지배** — In 셀에서 `Δh_an` 이 ≈90–95 %(LTO 교체로 잰 것 · 같은 `k_eff` 가정). Li-In · 합금 · Si 음극 셀의 압력 신호는 **대부분 음극 채널**이다.
- **강성 곱** — `k_eff(N)` 는 셀 밖(지그 · 유압 · 게이지) + 셀 안(공극 압밀 · 소성 흐름)의 순응. 인쇄 0 · 사이클마다 변할 수 있다(이 편의 압밀 서사가 곧 그 말이다).
- **표류** — `P_base(t)` 원시 −1.2 MPa/110 h. 이 편은 방전 말 골을 잇는 선으로 뺐다.

⇒ 카드 물음(양극 `LAM_PE` ↔ 접촉 손실)으로: 양극 몫 `Δh_ca` 는 활성 LCO 중 Δx 를 겪은 부피에 비례한다. 전자/이온 고립(`θ`)으로 빠진 입자와 구조 열화(`LAM_PE`)로 빠진 입자는 **둘 다 Δx 를 멈춘다** ⇒
압력 진폭은 `θ·ε_p` 곱을 **용량과 같은 방식**으로 본다. 압력이 용량과 다르게 보는 것은 (i) **Δx 없는 전하**(부반응 · 누설 — 용량에는 들어가고 압력에는 안 들어간다)와 (ii) **`k_eff` 변화**뿐이고, 이 편에서는
(ii) 가 (i) 를 가린다(비 +14 %).

## (ㄴ) 압력 채널은 관측 하나와 미지수 하나를 같이 더한다

ΔP/Q 를 움직이는 원인은 `k_eff(N)` · 부반응 몫 · 전극 몫 셋이다. `k_eff` 를 따로 재지 않으면(예: 사이클 사이 작은 하중 계단으로 셀 순응을 잰다 — 제안) 압력 채널의 **순 식별 이득은 0** 이다.
곱 축퇴 처방 표에 경고 행으로 붙인다.

## (ㄷ) 기저선은 버릴 값이 아니다 — 재고 손실과 압밀이 같은 자리에 있다

59호는 LMB 에서 기저 압력 **상승**을 `[인쇄]` "residual solid electrolyte interphase and isolated lithium" 의 누적으로 적었다(분리 불가 인쇄). 이 편의 In 셀에서 방전 말 In 에 남은 Li(재고 손실의 한 몫)는
잔류 팽창이라 기저를 **올려야** 한다 — 원시 기저는 사이클당 −0.30 → −0.12 MPa 로 **내려간다**. 압밀 · 이완 표류가 그 몫을 덮고, 기저선 제거는 **둘을 한꺼번에 지운다**. 압력으로 재고 손실을 보려면
무전류 유지로 표류를 먼저 재야 한다 — 압력 되돌림 시험 D1 에 붙일 조건 후보(결정은 사용자 몫).

## (ㄹ) 합성 truth · 이식판의 "운전 압력" 표기에 두 항을 더한다

60호 새 제약 1(경계조건 표기) · 61호 새 제약 1(Li 눈금 영역)에 이 편이 두 항을 더한다: **기저(절대) 압력**과 **기저선 규약**. "ΔP 1.25 MPa" 는 기저 ≈62 MPa · 방전 말 골 기저선 위의 값이고
원시로는 +1.07 이다. 이 셋 없이 옮긴 ΔP 는 값이 아니다.

# 곱 축퇴 처방 — 마흔다섯 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]`)

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | EIS 는 첫 충전뿐 · 다른 장치(S1 · S2) — 사이클 축 0 · `C` 추출 0 | ❌ |
| **2단계** (18 · 25호) | + 면적을 아는 대조군 | LTO 음극 교체 = **압력 채널의 전극 분해**(면적 대조 아님) | ❌ |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | 온도 1 점(25 °C) | ❌ |
| **4단계** (20호) | 시간 영역 동일 검사 | 압력–시간(원시 · 보정) 11 사이클 — 전기화학 시간 영역 아님 | ❌ |
| 52호 줄 | 누적 결손 ↔ Li 재고 | 무 Li In 조립 → 재고 = 양극. 압력 셀 CE 0 · S3 셀(다른 셀) CE 91.0 → ≈99.6 % | ⚠ 입력 부분 |

⇒ **적용 불가 — 1단계 입력 없음.** 32 · 33 · 59 · 60 · 61호처럼 한 번으로 센다. 기록 이유: **압력(두께) 채널에도 곱이 있다** — `ΔP = k_eff · Δh`, `Δh ∝ (θ·ε_p·V)·Δx`. 이 편의 비 +14 % 는
활성 분율이 아니라 `k_eff` 가 움직였다는 것과 양립한다(이 편의 압밀 서사). 처방 표에 경고 행: **"압력 · 두께 진폭을 활성 분율(`θ·ε_p`)의 대리로 쓸 때 — `k_eff(N)` · 기저선 규약 · 음극 몫이 먼저"**.

# 보류 결정 (가)(나)(다)(아)(자)(차)(타) — 이 편이 주는 근거 (결정 안 함)

원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 와 대조. **결정은 사용자 몫이고, 이 편은 어느 항목에도 근거를 주지 않는다.**

| # | 결정 | 이 편 | 근거 |
|---|---|---|---|
| 가 | 29호 Q4 +0.5 유지 | 무관 | 적합 · 정적/동적 축 0 |
| 나 | 38호 Q2 +0.5 유지 | 무관 | 활성 질량 · 채널 결합 0 |
| 다 | 28호 Bizeray 를 ASSB Q4 분모에 | 무관 | 식별성 방법 0 |
| 아 | 35호 합성 쌍 → Roman 특징 재계산 | 무관 | ML 0 |
| 자 | 31호 ICI zenodo `R/k` 면적 소거 | 무관 | 펄스 · 차단 0 |
| 차 | 23호 PyBaMM 면적 노브 / `j₀` 노브 분리 | 무관 | 모델 0 — 23호와 LTO 자료를 공유하나 면적 · `j₀` 에 닿는 값 0 |
| 타 | Navidi 2024 digest 재점검 | 무관 | — |

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 어디 | 판정 |
|---|---|---|---|
| **D1** | ★★★ **"The absolute pressure change is shown after subtracting the baseline"** ↔ S7: 기저선은 방전 말 골을 잇는 선(`[도표]` ≤0.02 MPa) — Fig. 1a 의 방전 말 0 은 구성상 · 값은 "absolute" 가 아니라 기저선 상대값 · 원시 첫 충전 상승 +1.07 ↔ 보정 1.267 | p. 9931 ↔ S7 | 규약 미정의(G2) |
| **D2** | ★★★ **In → InLi 부피 팽창 세 값** — "roughly doubles the volume (i.e. adds about **42 vol%** per formula unit)"(p. 9931) ↔ "**105.6%**"(p. 9932 · Fig. 2 캡션 · ESI) ↔ `[재현]` 인쇄 몰부피 15.71 → 23.597 = **+50.2 %**. ESI 두께 계산은 +50.2 %(ΔVm 7.887)를 쓰고 "35.2 %"(= 105.6/3)는 105.6 을 쓴다 | p. 9931 ↔ p. 9932 ↔ ESI | 두께 추정(1.56 µm)은 +50 % 쪽 |
| **D3** | ★★ **"113.23 Å³"** ↔ `[재현]` Fig. 2 치수 4.803² × 6.792 = **156.66 Å³** · 인쇄 Vm 로 In 원자 둘이면 78.4 · 넷이면 156.7 — 어느 쪽으로도 113.23 이 안 나온다. Fig. 2 의 In 격자(3.298 · 5.063)는 원자당 16.58 ↔ 인쇄 15.71 cm³ mol⁻¹ | p. 9932 ↔ Fig. 2 | 계산 경로 불명 |
| **D4** | ★★★ **ESI 계산 셀 ↔ 본문 압력 셀** — "14 mg LiCoO2" · "89 mg In"(774.5 µmol) · "1.53 mAh" · "cell area of 1.103 cm²" ↔ 복합체 12 mg(LCO 8.4 mg → 이론 1.15 mAh) · In 125 µm × ∅8 mm(`[재현]` 400 µmol) · ∅10 mm(0.785 cm²). `[재현]` 1.53 mAh ÷ 8.4 mg = 182 mAh g⁻¹ > 137 | ESI ③ ↔ pp. 9930–9931 | 다른 셀의 계산(G6) |
| **D5** | ★★ **Li 두께 "2.2 µm"** — 본문 "should increase the anode thickness **linearly**" ↔ ESI 값은 ⅓(등방 다결정 가정)을 곱한 것: `[재현]` 5.7×10⁻⁵ mol × 12.97 / 1.103 = 6.71 µm → ÷3 = 2.24 µm. 평면 석출이면 6.7(1.103 cm²) · 9.4 µm(0.785 cm²) | p. 9932 ↔ ESI ③ | ⅓ 규칙의 오적용 |
| **D6** | ★★ **기공 = "light areas"** — "the more uniform distribution of pores (**light areas** in the tomography images …)" ↔ Fig. 5 캡션 "**Bright areas** … refer to a high attenuation … i.e. heavy elements or **higher material density**" · Fig. 5b "low density" = 검정 · S5 void = 어두운 회색 | p. 9933 ↔ Fig. 5 캡션 · S5 | 본문 오기로 읽힌다 |
| **D7** | ★★ Fig. 5 캡션 "at a current density corresponding to **0.1C**" ↔ 실험 "19.1 µA cm⁻², corresponding to a C-rate of **0.03C**" ↔ S4 "**C/33**" | Fig. 5 ↔ p. 9930 ↔ S4 | 캡션 오기로 읽힌다 |
| **D8** | ★★ 공극률 "**5.5% before cycling and 2.6% after cycling**" ↔ ESI "5.45% for the **pristine pellet** and a porosity of 2.58% for the **charged pellet**" · "two identical SSB pellets" — 같은 시편의 전후가 아니고, 사이클이 아니라 첫 충전 1 회 | p. 9934 ↔ ESI ④ · p. 9933 | 서술이 실험보다 강하다 |
| **D9** | ★★ **ESI 부피** — SE 21.32 → **24.85 mm³(+16.6 %**; `[재현]` 고체 SE 20.16 → 24.21 mm³ **+20 %**) · 음극 1.89 → **5.93 mm³(×3.1)** · 양극 0.94 → 0.94 — "densification" 서술과 SE 부피의 방향이 반대 · 논문 두께 계산(8 % 리튬화)과 음극 자릿수 불일치 · 본문 논의 0 | ESI ④ | 두 펠릿 차이 · 분할의 몫(G9) |
| **D10** | ★★ Fig. 3 캡션 "decreases to 60% … **as was also observed when using In anode**" ↔ `[재현]` In 셀 0.25 C/0.1 C 진폭 1.083 / 1.205 = **0.90** | Fig. 3 ↔ Fig. 1b | 방향만 같다 |
| **D11** | ★ ESI 가 토모그래피를 "**Figure 6 a)**"(ESI p. 8) · "**Fig 4 a)**"(S5 캡션)로 부른다 ↔ 본문 Fig. 5a | ESI ↔ 본문 | 판 번호 잔재 |
| **D12** | ★ S3 캡션 "the Coulombic efficiency was maintained **above 99% from the 2nd cycle on**" ↔ `[도표]` 2 사이클 **98.3 %** · 99 % 도달 ≈5 사이클 | S3 | 캡션이 그림보다 강하다 |
| **D13** | ★★ S6 캡션 "**no height change** could be observed once the galvanostatic cycling stops, which **excludes the relaxation of setup components** leading to the inclined baseline" ↔ `[도표]` 첫 ≈6.5 h(전압 창 밖 — 첫 충전 전으로 읽힘) 높이 **−6.05 → −8.63 µm** · 사후 유지(≈95–98 h)만 평탄 | S6 | 배제 논증이 한쪽 끝만 본다 |
| **D14** | ★ 딜라토미터 "the decreased baseline of the height-change curve **within the first few cycles**" · "required more cycles to equilibrate" ↔ `[도표]` 11 사이클 끝까지 순감소(마지막 −0.50 µm/사이클) — 평형 도달 0 | p. 9934 ↔ S6 | |
| **D15** | ★★★ **Fig. 1 감쇠의 배정이 세 번 다르다** — p. 9932 원인 목록 (i) In/SE 계면 저항 (ii) 양극 입자 · 코팅 균열 (iii) SE 분해(접촉 손실 없음) ↔ Fig. 1b 캡션 "interfaces and **particle contact loss** due to the 'breathing'" ↔ p. 9933 "This loss of connectivity gives rise to capacity losses … **as seen in the present study (Fig. 1)**" — 무가압 펠릿의 추론을 ≈62 MPa 구속 셀의 감쇠에 옮긴다 | p. 9932 ↔ Fig. 1 ↔ p. 9933 | 배정 미결 |
| **D16** | ★ "A thicker SE membrane (**~1 µm**)"(렌더로 확인한 인쇄 단위) — 압착 펠릿으로 불가능 · "thicker" 와도 모순 | p. 9931 | mm 의 오기로 읽힌다 |
| **D17** | ★ ESI 설명(본문 p. 9929 각주) "the **estimation of maximum pressure build-up**" ↔ ESI 에 압력 추정 수치 0("it is not possible to fully gauge the expected pressure build up") | p. 9929 ↔ ESI ③ | 약속된 계산 부재(G7) |
| **D18** | ★ "a 2% **volume** expansion **along the c-axis**" — 부피와 축 길이의 혼용; ESI 는 "2 % volume expansion" 으로 계산 | p. 9931 ↔ ESI ③ | 표현 |
| **D19** | ★ LCO 두께 "**0.163 µm**" ↔ `[재현]` 1.84×10⁻⁵ cm³ ÷ 1.103 cm² = **0.167 µm**(2.4 %) | ESI ③ | 반올림 · 면적 |
| **D20** | ★ S7 캡션 "the **pressure change** curve" ↔ 세로축 "Pressure / MPa" **60.5–65** 절대값 | S7 | 표현 |
| **D21** | ★ 참고문헌 서지 이상 — [3] "*Isr. J. Chem.*, 2015, **742**, 1–15" · [5] "*Nat. Mater.*, 2016, **1**, 1–9" · [23] "*Adv. Energy Mater.*, 2016, **1196**, 1–11" · [33] "*Solid State Ionics*, 1996, **2738**, 877–882"(42호 digest [18]: 86–88) · [27] "2016, submitted" | 참고문헌 | 원전 추적 때 권 · 쪽을 다시 확인 |
| **D22** | ★ "only up to 0.2% volume expansion **during lithium**" | p. 9932 | 낱말 누락(lithiation) |

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. ★★★ **이 편의 압력은 충전 팽창을 본다** — 양극 LCO + 음극 In, 신호의 ≈90–95 % 가 음극(`[재현]` LTO 교체). "**충전 중 부피 수축 → 접촉 감소**" 는 이 편의 명제가 아니다(22호 ref 18 다리 ❌ · 원장 행 정정 — wiki 밖).
2. ★★★ **운전 기저 ≈61.8 MPa 는 ESI 그림 축에만 있다** — 본문 `MPa` 1 회(1.25). 1.25 MPa 는 기저선 보정값이고 원시 첫 충전 상승은 +1.07. 60호 S14(0.8 MPa 기저 · +1.51)와 같은 자릿수여도 **같은 눈금이 아니다** —
   `[재현]` ΔP 를 셀 탄성으로 내려면 유효 길이 ≈22–36 mm ⇒ 지그 순응이 ΔP 를 정한다(강성 인쇄 0).
3. ★★★ **압력 진폭은 용량을 비례로 따라가지 않는다** — 보정 비 +14 % · 원시 충전 상승 평탄(용량 −20 % 동안) · LTO 셀 진폭 평탄(용량 −9 %). "correlates well" 은 방향 · 율 전환까지이고 사이클 감쇠의 원인 배정(접촉 손실)에 쓸 근거가 아니다.
4. ★★ **접촉 손실은 무가압 셀의 추론이고, 그것을 ≈62 MPa 구속 셀의 감쇠로 옮긴다**(D15). `θ(N)` 0/62. 33호 [89] 의 관측(휨 · 가장자리 균열)은 서고 인과("causing contact loss")는 원문에서도 추론이다.
5. ★★ **22호 G5** — ∅10 mm(0.785 cm²)를 조건부로 줄 수 있다(같은 연구망 23호 역산과 같다). 장치 원전은 [28] Busche 2016(원장 0 — 등록 필요, wiki 밖).
6. ★★ **23호 G1 의 빈칸** — "NCM volume changes of nearly 6%"([31] Kondrakov 2017 *JPCC* 121, 3286 — 원장 ★★★ **지목 2** 회째) · 방향 0.
7. ★ **Q5 형태** — "공칭 조성으로 창 안임을 계산"(`[재현]` 압력 셀 ≈8.4 at% Li — 42호 창 ≈1–47 at% 안) · Takada 1996 **지목 3** 회째.
8. ★ `[해석]` **압력 채널의 곱** — `ΔP = k_eff · Δh` · 기저선이 재고 손실과 압밀을 같이 지운다 · 관측 하나를 더하면 미지수(`k_eff`)도 하나 는다 → 처방 표 경고 행 · 새 개념 [[assb-operando-pressure-signal-attribution]].

# 후속 후보 (원전 우선)

참고문헌 40 편 중 우리 축(Q1 · Q2 · Q5 · Q6)에 닿는 것만. **셀 열화 · 식별성 원전 0.**

| 서지 | ref | 왜 | 축 | 우선 |
|---|---|---|---|---|
| **Busche, Weber, Schneider, Dietrich, Wenzel, Leichtweiss, Schröder, Zhang, Weigand, Walter, Sedlmaier, Houtarde, Nazar, Janek 2016 *Chem. Mater.* 28, 6152** | [28] | **hot-press 장치의 원전** — 예압 · 조절 방식(정하중/정변위) · 강성 · 게이지가 여기 있을 수 있다(G1). 원장 0 → 등록 요청 | Q6 | ★★★ |
| **Zhang W. … Janek 2016 "submitted"**(= 원장 ★★★★ Zhang 2017 *ACS AMI* 9, 17835 로 추정) | [27] · ESI [1] | "standard SSB setup" · EIS 배정 · 장기 사이클(S3) · 율 이용률 — 22 · 23호 방법 원전과 같은 편인지 확인 | Q1 · Q2 | ★★★★(기존, 지목 +1 후보) |
| **Kondrakov … Janek 2017 *J. Phys. Chem. C* 121, 3286** | [31] | NCM "nearly 6%" · 23호 G1 · 방향(수축/팽창) · 조성 | Q1 · Q8 | ★★★(기존, 지목 2) |
| **Takada, Aotani, Iwamoto, Kondo 1996 *Solid State Ionics* 86–88, 877**(권 · 쪽은 원장 · 42호 기준 — 이 편 인쇄 "2738, 877–882") | [33] | 0.62 V In-rich 평탄 — ASSB 쪽 뿌리 후보 | Q5 | ★★★(기존, 지목 3) |
| **Koerver 2018 *EES*** | (이 편 이후; 33호 [58]) | LTO 압력 자료 제공자 R. K. 의 후속 — 33호 재수록 양극 ΔP ≈0.05–0.07 MPa 가 이 편 LTO 셀과 같은 계열인지 · 기저 · 기저선 규약 | Q1 · Q6 | ★★★(기존, 재지목) |
| **Whiteley, Kim, Kang, Cho, Oh, Lee 2015 *JES* 162, 711** | [19] | Sn–Li 합금 "loss of contact … appreciable external pressure is required" — 이 편 서론 접촉 문장의 원전 | Q1 · Q6 | ★★ |
| Han 2021 *Joule* · Ji 2022 *ESM* | (이 편 이후; 33호 [90] · [88]) | 기저 20 · 45 MPa 위 압력 진동 — "기저는 본문에 없다" 형태가 이 편과 같은지 | Q6 | ★★(기존) |
| Reimers & Dahn 1992 *JES* 139, 2091 | [30] | LCO c 축 · "2 %" 의 원전 | Q8 | ★ |
| Alexander … Calvert 1976 *Can. J. Chem.* 54, 1052 | [32] | InLi₀.₈₇ · −0.35 < x < 0.13 | Q5 | ★ |
| Sakuda, Hayashi, Tatsumisago 2013 *Sci. Rep.* 3, 2261 | [20] | 황화물 SE 탄성률 18–25 GPa — §(c) 입력 | Q6 | ☆ |

# 이 digest 가 주장하지 않는 것

- **접촉 손실이 없었다고 하지 않는다** — 이 편이 재지 않았고, 압력 진폭은 그것을 볼 수 있는 채널이 아니라는 것(우리 대수 (ㄱ))까지다.
- **Fig. 1b 의 진폭 감소가 전부 기저선 규약의 산물이라고 하지 않는다** — 원시 충전 상승이 0.1 C 에서 평탄하고, 보정 진폭의 감소가 기저선 몫과 같은 크기라는 것까지다(S7 픽셀 판독 위).
- **기저선 표류가 SE 압밀이 아니라고 하지 않는다** — 후보(압밀 · In 흐름 · 장치 이완 · 온도)를 가를 대조가 없다는 것까지다. 시간당 표류가 율과 무관하게 줄어든다는 것은 그림 판독 위의 관찰이다.
- **"지그 순응이 ΔP 를 정한다" 를 측정으로 주장하지 않는다** — 인쇄 SE 탄성률(18–25 GPa) · ESI ⅓ 규칙 두께 · 밀도를 낮게 잡은 셀 두께 상한 위의 `[재현]` 이다. 강성 실측 0.
- **22호 셀의 면적이 0.785 cm² 라고 확정하지 않는다** — 같은 연구망의 인쇄 지름이 22호 역산과 맞는다는 것까지.
- **ESI 계산 셀이 어느 셀인지 안다고 하지 않는다** — 본문 압력 셀과 맞지 않는다는 것까지.
- **[27] = Zhang 2017 *ACS AMI* 9, 17835 라고 단정하지 않는다** — 저자 목록이 부분집합이라는 것까지.
- **6호 ref 46 = 이 편이라는 것은 카드 Status Log 기록 기준이다** — 6호 digest 본문 전사 0 · 6호 원문 미열람.
- **33호 재수록 양극 ΔP(Koerver 2018)와 이 편 LTO 자료가 같은 측정이라고 하지 않는다** — 같은 자릿수 · 같은 제공자라는 것까지.
- **픽셀 판독값을 인쇄값처럼 쓰지 않는다** — 원본 래스터 · 선형 축 적합 위의 값이고 판독 오차가 있다(§그림 머리).

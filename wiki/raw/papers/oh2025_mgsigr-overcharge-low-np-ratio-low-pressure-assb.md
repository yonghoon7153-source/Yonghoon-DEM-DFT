---
title: "Oh, Kwon, Choi, Lee, Sohn, Lee, Lee, Kim, Bae, Choi 2025 — All-Solid-State Batteries with Extremely Low N/P Ratio Operating at Low Stack Pressure (Adv. Energy Mater. 15, 2404817)"
source_url: local-upload/14._All_Solid_State_Batteries_With_Extremely_Low_NP_Ratio_Operating_at_Low_Stack_Pressure.pdf + 14._Sup_All_Solid_State_Batteries_With_Extremely_Low_NP_Ratio_Operating_at_Low_Stack_Pressure.pdf (SI)
source_url_note: "본문 10 쪽(참고문헌 25 항목) + SI 28 쪽(Word 판, 그림 S1-S25 · 표 S1-S2 는 이미지). 크로퍼 34 장(본문 7 + SI 25 + 표 2) 중 14 장 Read(Fig. 1-6 · S11 · S15 · S17 · S19 · S23 · S25 · 표 S1 · S2), 화소 판독 Fig. 4D · 6D. 14호(Oh 2025 Angew.)와 같은 연구실. 원자료는 커밋하지 않는다."
source_doi: 10.1002/aenm.202404817
source_license: "© 2024 Wiley-VCH GmbH (오픈액세스 표기 없음)"
pdf_sha256: 309e25f56e80e0ada422dec4d59f00667a0061f2bccd5efe2ce76ac1fcf63302
si_sha256: 40337c89ca3fb2a028f7787f6217db65c36b90fe2f4d3f0e8cbef08006cd27e4
ingested: 2026-09-23
sha256: 71398603ec371f75ed9448ed04afe813f1a05ebc78a9692b2370ca7ca28b219c
---

# 수집 목적

`assb` 섹션 **52호**. 큐 **53번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **열넷째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행 ★★★: "저압 실셀 — 14호(Maxwell Protocol)와 **같은 연구실**. 13호 후속 4순위 → 14호에서 1순위 승격", 축 Q6 · Q3 · Q4. 지목 2 회 — 13호 Zheng 2026 ref [34] · 14호 Oh 2025 *Angew.* ref [10].
이 digest 의 1순위 물음: **(1) 운전 스택 압력은 얼마이고 제조 압력과 갈렸나, 압력별 비교가 있나, 저압에서 무엇이 열화를 지배한다고 쓰나 — 측정인가 해석인가. (2) N/P < 1 셀에서 어느 전극이 용량의 끝을 내고, 용량 손실을 `LLI` · `LAM` · 접촉 중 어디에 배정했나. 쿨롱 효율을 `LLI` 대리로 쓰나(41호: 연성 단락 누설 오염).**

J. Oh, D. Kwon(공동 1저자), S. H. Choi, N. Lee, Y. Sohn, T. Lee, T. Lee, J. Y. Kim, K. Y. Bae, **J. W. Choi**(교신) —
**"All-Solid-State Batteries with Extremely Low N/P Ratio Operating at Low Stack Pressure"**,
*Adv. Energy Mater.* **2025**, **15**(16), 2404817, doi `10.1002/aenm.202404817`.
`[인쇄]` Received 2024-10-16 · Revised 2024-11-23 · Published online 2024-12-15 · "© 2024 Wiley-VCH GmbH" (오픈액세스 표기 없음).
소속: 서울대 화학생물공학부 · **HMG-SNU JBRC**(Oh · N. Lee · Sohn · T. Lee · Choi) · KETI(S. H. Choi) · **현대자동차 Advanced Battery Development Team**(J. Y. Kim · K. Y. Bae). 자금: NRF · KIMM · SNF Sinergia · 서울대 연구소 · "This work was also supported by Hyundai Motor Company". `[인쇄]` "The authors declare no conflict of interest." 데이터: "available from the corresponding author upon reasonable request".
**14호(Oh · Kim · Kim · An · Kwon · Choi 2025 *Angew.*)와 제1저자 · 교신저자 · 공동 1저자(Kwon)가 겹친다 — 같은 연구실의 앞선 편.**

본문 PDF **10 쪽**(본문 9 + 참고문헌 25 항목) · SI PDF **28 쪽**(Word 판, 그림 S1–S25 · 표 S1–S2 — 표 둘은 **이미지**라 텍스트로 안 뽑힌다, 렌더로 읽음). sha256 은 frontmatter(본문 `pdf_sha256` · SI `si_sha256`). 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> Fig. 4D · 6D 의 쿨롱 효율 · 용량은 **화소 판독**(축 틀 좌표로 보정, 마커 중심 = 테두리 위·아래 가장자리 평균 또는 윗가장자리 + 반지름 12.5 px)이다 — 판독 오차는 CE ±≈1 %p, 용량 ±≈2 mAh g⁻¹. 검증: 6D 용량 1 → 75 사이클 판독 비 0.652 ↔ `[인쇄]` 64.7 %.

---

# 판정 (먼저)

> ★★★★ **Q6 — 운전 압력은 명시되고(스프링 20 · 3 MPa, 파우치 볼트 3 MPa) 제조 압력과 갈린다(150 · 380 · WIP 450 MPa). 그러나 압력 비교는 없다: 20 ↔ 3 MPa 두 점이 양극 적재(20 ↔ 6 mg cm⁻²) · N/P(0.15 ↔ 0.66)와 함께 바뀌고, 반쪽전지의 압력은 인쇄되지 않았다.** 저자가 저압 열화의 지배 인자로 지목한 것은 **음극 계면(Li 도금 위치 · 친리튬성 · 공극)** 이고, 그 근거는 **3 MPa 고정에서 음극 셋(SiGr · Li 10 µm · MgSiGr)을 바꾼 비교**다 — 압력을 바꾼 측정이 아니다. MgSiGr 3 MPa 셀 자신의 감쇠(75 사이클 64.7 %)는 마지막 문단의 해석 한 줄("volume changes during overcharging, especially under low stack pressure")뿐이고 **양극 쪽 관측은 0**(양극 EIS · 영상 · 사후 분석 전수 0).
>
> **(a) 압력 값.** `[인쇄]` "The stack pressure was set at either 20 or 3 MPa using a spring with a specific spring constant" · 파우치 "pressurized at 3 MPa … by tightening bolts and nuts at the four substrate corners with a torque of 3.5 Nm". **스프링 상수 · 압축 변위 · 로드셀 0**, 토크 → 압력 변환 근거 0. `[재현]` 표준 체결식(`F = T/(K·d)`, K ≈ 0.2)으로 M6–M10 볼트 넷이면 체결력 ≈7–12 kN — 파우치 전극 면적 4 cm² 기준 **≈17–29 MPa**; 3 MPa 가 되려면 기준 면적이 PEEK 판 전체이거나 따로 교정했어야 한다(볼트 규격 · 판 면적 미인쇄 — 우리 계산, 칸 밖).
> **(b) 33호 요구치 띠(0.4–5 MPa) 안의 1차 운전값을 준다** — 실온 25 °C · 완전지 · 75 사이클 · 3 MPa, 펠릿 셀과 파우치 둘. 단 33호 인쇄 산업 요구치 "< 2 MPa" 위이고, 25호(Zhou 2025)가 이미 2 MPa 완전지 100 사이클을 줬다 — **띠의 아래 끝을 새로 내리지 않는다.**
> **(c) 제목의 두 조건은 한 셀에서 만나지 않는다.** "extremely low N/P" 0.15 는 **20 MPa** 에서만, **3 MPa** 셀은 N/P 0.66(펠릿) · 0.6(파우치)이다(D1).
>
> ★★★★ **용량 제한 전극 · 손실 배정 — 둘 다 지면에 없다.** 2전극만, 기준극 0 · dV/dQ 0 · 반쪽전지 분해 0(완전지 기준). `LLI` · `LAM` · `degradation mode` 전수 0 회. 용량 손실에 붙은 이름은 **"short circuit / soft short"**(실패)와 반쪽전지 EIS 의 **`R_SEI`**(SiGr 만)뿐이다. `[해석]` 충전 끝은 양극이 낸다 — 도금 구간의 음극은 `[도표]` −15 … −22 mV vs Li 로 거의 평탄해 4.2 V 는 양극 전위로 읽힌다. **방전 끝(2.5 V)을 어느 전극이 내는지는 정할 재료가 없다** — 음극이 끝을 내면(도금 Li 소진 → SiGr 탈리튬 전위 상승) Li 재고 손실이 곧 용량 손실이고, 양극이 끝을 내면 음극에 남은 Li 가 `LLI` 를 가린다. 우리 α · β 전제(41호 요구 "어느 전극이 끝을 내는가")는 이 편에서 **판정 불가**다.
>
> ★★★★ **쿨롱 효율은 이 편에서 `LLI` 대리가 아니다 — 지면 자신의 수치로 깨진다** (`[재현]`, 우리 계산이라 칸 밖):
> - **20 MPa**: `[인쇄]` "average CE of 99.2 % for the 75 cycles" ↔ "capacity retention of 83.7 %". CE 결손을 Li 손실로 읽으면 `[재현]` ∏CE ≈ 0.992⁷⁵ ≈ **0.55**, 누적 충–방 결손 ≈**95 mAh g⁻¹** ↔ 관측 용량 손실 ≈27(`[도표]` 170 → 143) — **≈3.5 배**.
> - **3 MPa**: CE 는 **본문에 한 번도 인쇄되지 않는다.** `[도표]` Fig. 6D 초록 속빈 원 — 1–12 사이클 **≈85–89 %**, 13–40 ≈91–94 %, 75 사이클 ≈96.5 %. `[재현]` 누적 충–방 결손 ≈**575 mAh g⁻¹** — **NCM811 이론 Li 재고(≈275 mAh g⁻¹)의 ≈2 배**인데 용량은 64.7 % 남는다. ⇒ **결손의 대부분은 사이클 재고에서 빠진 Li 가 아니다** — 누설 전자(연성 단락 — 저자 자신이 S17 에 병렬 `r_SS` 로 그린 경로 · 부반응) 또는 SE 분해가 재고를 보충하는 경로(그 자체가 부반응). 어느 쪽이든 **CE 결손 ≠ `LLI`**. 41호 "세 번째 오염 — 연성 단락 누설" 의 **실셀 크기 판**이다.
> - `[재현]` **면적당**으로 바꾸면 결손은 ≈0.025(20 MPa) ↔ ≈0.046 mAh cm⁻² 사이클⁻¹(3 MPa) — **×≈1.8**. CE 로 보면 ×≈7 의 차이 중 대부분은 **양극 적재 20 ↔ 6 mg cm⁻² 의 정규화**다(적재 = NCM 질량 가정, 조성 질량이면 둘 다 ×0.68 — 비 불변).
>
> **Q1 · Q7.** `θ(N)` **0/52** — 양극 접촉은 재지 않았다. 접촉 관측은 **음극 \| SE 계면 XRM 한 쌍**(반쪽전지 · 첫 과충전–방전 1 회 뒤 · 압력 미인쇄)이고 `[인쇄]` "substantial contact loss along the interface" · "interface porosity was much lower" — **수치 · 분할 문턱 · 시야 대표성 0**, `[도표]` 두 기공 지도가 **둘 다 넓게** 칠해져 "much lower" 는 그림으로 크기를 확인할 수 없다(D4). Q7: 무음극형(Li 도금이 용량의 85 % · 34 %)인데 **dead Li ↔ SEI Li 를 가르지 않는다** — `dead` 0 · 적정 0 · Li 재고 수지 0; SEI 는 SiGr 반쪽전지 Nyquist 의 "extra semi-circle" 이름뿐.
>
> **채움표: 새 칸 0** (≈20.0 그대로). Q6 반 칸 검토 후 접음(운전값 명시 + 교락 — 25호 요인 설계 · 39호 5 점과 다르다) · Q4 0/52 **마흔네 번째 성질** · Q3 층 하나 · 곱 축퇴 처방 **서른다섯 번째 적용**(적용 불가 — 양극 채널 0; 새 줄 "누적 충–방 결손 ↔ Li 재고 상한").

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 없는 것 | 왜 필요한가 |
|---|---|---|
| G1 | **반쪽전지의 스택 압력** — Fig. 1–3 · 5 · S5 · S11–S20 전부 | XRM "contact loss" 영상(Fig. 5)과 in situ EIS 의 압력 조건. 원문 "set at either 20 or 3 MPa" 가 반쪽전지에도 걸리는지 모른다 |
| G2 | **스프링 상수 · 압축 변위 · 사이클 중 압력 계측** | "Precise control" 의 근거. Li 도금 두께 변화(20 MPa 셀 `[재현]` 사이클당 ≈15 µm)가 스프링 힘을 얼마나 바꾸는지 |
| G3 | **파우치 토크 → 3 MPa 변환**(볼트 규격 · 판 면적 · 교정) | 판정 (a) `[재현]` — 표준 식으로는 전극 면적 기준 17–29 MPa |
| G4 | **완전지 N/P 의 계산 기준**(음극 용량을 0.1C 825 · 1 mA cm⁻² 277 중 무엇으로, "SiGr 0.8 mg" 이 Si+Gr 인지 LPSCl 포함인지, 양극 적재가 NCM 인지 조성물인지) | D2 — 인쇄 적재로는 0.15 와 0.66 을 한 SiGr 용량으로 재현 못 한다 |
| G5 | **저압 셀(3 MPa)의 CE 수치** · 파우치의 CE · 용량 유지율 | 판정 ★ — 그림에만 있다 |
| G6 | **방전 끝을 내는 전극** — 3전극 · dV/dQ · 방전 끝 반쪽 전위 | α · β 전제 |
| G7 | **조건당 셀 수 · 오차 막대** | `n =` · `error bar` · `standard deviation` · `reproduc*` 전수 0 |
| G8 | **XRM 분할 문턱 · 공극률 수치 · 시야 크기 대 셀 면적** | Fig. 5 "much lower" 의 크기 |
| G9 | **EIS 적합 값 표**(EC-Lab "deconvoluted") — 본문 `R_B` 두 값(23.6 → 15.7 Ω)과 S19 그림뿐, 면적 정규화 0 | 반쪽 `R_CT`/`C` 판정 |
| G10 | **과충전 중 SiGr 추가 리튬화와 Li 도금의 분할** | S11B `[도표]` 0.01 V 에서 용량이 ≈270 → ≈640 mAh g⁻¹ 계속 들어간다 — "modified N/P" 는 0 V 교차 표지이지 저장 분할이 아니다 |

---

# 1. 서지 · 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문은 참고문헌 전까지(Wiley 내려받기 바닥글 줄 제외). SI 는 괄호. 줄끝 하이픈은 이은 판을 병기.

| `identifiab` | `uncertaint` | `confidence interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | **0** (0) | **0** (0) | **0** (0) | 0 (0) | **1** (0) | **13** (SI 2) |

- NFKC 변경: 본문 **124 자**(`ﬁ` 86 · `ﬀ` 24 · `ﬂ` 7 · `ﬃ` 4 · `Ω` 옴 기호 1 · 수학 이탤릭 `𝜇` 2) · SI 1 자(`µ`) — **열 변화 0**. 소프트 하이픈 0. 줄끝 하이픈 본문 132 곳 · SI 1 곳 — 이으면 `pressure` 25 → 26 · `stack pressure` 23 → 24 · `overcharg*` 27 → 32 · `capacit*` 30 → 32 · `por(e|osity)` 5 → 6 — **열 변화 0**.
- `MPa` 13 = **운전 3 MPa ×7**(초록 · 본문 3 · Fig. 6 캡션 · 파우치 방법 "pressurized at 3 MPa" · "20 or 3 MPa" 1) + **제조 6**(380 ×4 · SE 150 · WIP 450). "20 MPa" 는 문장에 "20 or 3" 한 번 + Fig. 4D 래스터 라벨. SI 2 = 3 MPa(S24 · S25 캡션).
- `contact loss` 1 = **음극 \| SE 계면**(Fig. 5B "substantial contact loss along the interface"). `contact` 7 — 초록 "mitigating the poor contact" · 서론 "interparticle contact" · 음극 Li–SE "contact area" · "direct contact between the plated Li and the SE" · Fig. 5 · "smooth contact between the MgSiGr anode and SE" · 결론 "intimate inter-particle contact"(바인더 제언). **양극 접촉 0.**
- 보조(이은 판, 본문 / SI): `N/P` 41 / 11 · `overcharg*` 32 / 6 · `short*` 16 / 9 · `soft short` 2 / 2 · `Coulombic` 2 / 0 · `CE`/`CEs` 4 / 3 · **`retention` 1**(20 MPa 83.7 % 한 번 — 3 MPa 64.7 % 는 "maintained 64.7 % of the original capacity") · `SEI` 2 / 0 · `void` 3 / 0 · `crack` 4 / 0 · `pore`/`porosity` 6 / 0 · `spring` 4 / 1 · `torque` 1 / 0 · `cathode` 6 / 0(전부 조성 · 조립 · 적재) · `degrad*` 2 / 0 · `loss` 1 / 0 · `utiliz*` 3 · `limit*` 4 · `noise` 1 · `deconvolut*` 1 · `equivalent circuit` 0 / 1 · **`dead` · `isolat*` · `reservoir` · `inventory` · `titrat*` · `leak*` · `fit*` 0 / 0** · `reference electrode` · `three-electrode` 0 · `indium`/`In` 금속 0 · `Li metal` 14 / 0 · `anode-less` 5 · `anode-free` 0 · `n =` · `error bar` · `standard deviation` · `reproduc*` **0 / 0**.
- `[해석]` **이 편은 CE 를 "가역성" 의 증거로 쓰고(`[인쇄]` "superior CEs and cycle lives" · "impressive average CE of 99.2 %"), Li 재고 · 누설의 낱말은 0 이다** — CE 가 무엇을 세는지 묻지 않았다.

---

# 2. 셀 · 실험 (`[인쇄]`)

**재료.** Mg 200 nm 스퍼터 → SUS316L-H 박(Wellcos). SiGr = Si 나노입자(NanoAmor, D50 40 nm) : 인조흑연 **1 : 6 wt** 건식 혼합 → LPSCl(NEI) 과 **7 : 3 wt** 막자사발. **SiGr 적재 0.8 mg cm⁻²**. MgSiGr = SiGr 복합 분말을 Mg 코팅 SUS 에 올림, SiGr 는 코팅 없는 SUS. 양극(펠릿) = LiNbO₃ 코팅 NCM811(Wellcos, 입경 `[인쇄]` 5 µm — S21) : LPSCl : VGCF **68 : 30 : 2** 건식 · 적재 **20 mg cm⁻²(고압 평가) · 6 mg cm⁻²(저압 평가)**.

**셀.** 반쪽전지: LPSCl 150 mg · ∅13 mm · **150 MPa** 냉간 → (Mg)SiGr 을 아래에 두고 **380 MPa** → Li 박을 위에. 완전지: 양극 + (Mg)SiGr 을 SE 양면 → **380 MPa**. Li 금속 완전지: 양극 380 MPa 뒤 반대면에 **Li 10 µm**. 운전 **20 또는 3 MPa**(스프링, S23 도식 "Depth control" · "Specific spring constant" · "Torque"). 전부 Ar 글러브박스.
**파우치 20 × 20 mm².** 양극 슬러리 NCM : LPSCl : VGCF : NdBR = 70 : 26 : 1.5 : 2.5(부틸 뷰티레이트, Al 박, 100 °C 15 h) · MgSiGr 층 = SiGr : LPSCl 1 : 1 + NdBR 3 wt%, **10 µm**, SiGr 0.8 mg cm⁻² · SE 시트 100 µm(PET 이형). 진공 밀봉 → **WIP 450 MPa · 75 °C · 15 min**(ISA-W50-6000) → PEEK 판 사이 **3 MPa**(모서리 볼트 넷, 3.5 N·m).
**측정.** 전부 **25 °C**. 반쪽전지: "time-cutoff discharge within 0–0.1 V or 0–1.5 V (vs Li/Li⁺)"(WBCS 3000). 완전지 2.5–4.2 V · 충전 CC-CV · 방전 CC. 율: 방전 0.1C 고정 · 충전 0.1/0.3/0.5/1C. CV 0–1.5 V · 0.1 mV s⁻¹. EIS 1 MHz–0.01 Hz(VSP), "deconvoluted using EC-Lab". FE-SEM(JSM-7800F) · FIB(Helios 650) · XRD · **XRM Xradia 620 Versa**(80 kV · 125 µA · 10 W · 노출 4 h · Dragonfly).
**N/P 정의.** 식 (1) **"Modified N/P ratio = Capacity delivered by the SiGr / Total capacity"** — 반쪽전지용, "to explicitly characterize the overcharging phenomenon"; "the modified N/P ratio depends largely on the current density". **완전지 N/P 의 식은 인쇄되지 않았다**(서론의 일반 정의 "ratio of the capacity of the negative electrode to that of the positive electrode" 뿐). 1C = 3.6 mA cm⁻²(Fig. 4 캡션).

---

# 3. 절별 해체

## 3.1 초록 · 서론 (p. 1–2)

`[인쇄]` 문제 설정: ASSB 는 "impractically high stack pressure" 를 요구하고, 특히 N/P 가 작은 고에너지 셀에서 "uneven lithium (Li) stripping induces the formation of interfacial voids". 해법: SiGr 얇은 층 **밑에** 친리튬 Mg 막 → 과충전 때 과잉 Li 가 SiGr 아래에 도금 → "stable cycling even at room temperature and at a low stack pressure of 3 MPa" · "reducing the N/P ratio to less than one". "By mitigating the poor contact that is characteristic of ASSBs with a low stack pressure" — **접촉 개선은 초록의 주장이고 측정은 음극 계면 XRM 한 쌍뿐**(§3.9).
서론: LIB 의 N/P 1.05–1.2 [11] · "N/P ratios lower than these can lead to unwanted Li metal precipitation" · 무음극 = N/P 0 · "At low N/P ratios, Li deposition becomes more inhomogeneous" [13] · "Li-SE interface … creates significant void spaces after stripping, which makes it difficult to self-heal under low stack pressure conditions" [16]. 에너지 밀도 이득은 SI 표 S1 · S2 의 **이론 계산**(§5.6).

## 3.2 Mg 막 · 반쪽전지 · N/P 정의 (p. 2, Fig. S3–S11)

Mg ≈200 nm 균일(S3 · S4, 보지 않음) · SUS 반쪽전지에서 `[인쇄]` "the Mg-coated SUS sample … maintaining over 250 cycles of Li plating-stripping without any failure" ↔ 맨 SUS "rapid short-circuiting"(S5, 보지 않음). SiGr 최대 용량 `[인쇄]` **825 mAh g⁻¹ @0.1C(0.05 mA cm⁻²)** ↔ **277 @1 mA cm⁻²** — "the actual capacity contributed by the SiGr at practical current densities is significantly lower".
`[도표]` S11: 0.1C 리튬화 ≈830 · 탈리튬화 ≈695(`[재현]` 첫 효율 ≈84 %). 1 mA cm⁻²: 0.01 V 도달 ≈270 mAh g⁻¹, **그 뒤 0.01 V 부근 수평선이 ≈640 까지 이어지고** 탈리튬화 ≈440 — `[해석]` 전압 유지(CV) 구간으로 보인다(절차 미인쇄). ⇒ "277" 은 **전압 교차 용량**이고 SiGr 가 1 mA cm⁻² 에서 받을 수 있는 양이 아니다 — 과충전 중 SiGr 는 계속 리튬화될 수 있다(G10).

## 3.3 과충전 전압 (p. 2–3, Fig. 1, S12)

`[인쇄]` SiGr 을 0 V 까지 충전 뒤 과잉 Li 도금, 박리 컷오프 0.1 V("to focus solely on the stability of the Li metal plating process"). "For the plain SiGr anode, Li precipitation occurred after charging to 0.22 mAh cm⁻²" = 식 (1)의 분자 → **modified N/P 0.22 @1 mA cm⁻² · 1 mAh cm⁻²**. MgSiGr: 개시점 부근 완만한 기울기 = "Li−Mg alloying" · "Mg effectively participates in the initial Li nucleation".
`[도표]` Fig. 1A · B: SiGr 0 V 교차 ≈0.22 · 도금 개시 ≈0.25 mAh cm⁻²(구간 "Li nucleation"). MgSiGr 0 V 교차 ≈0.225 · "Li-Mg alloying" ≈0.225 → ≈0.35 · 도금 개시 ≈0.35. 도금 전압: SiGr 2 · 3 사이클 ≈−19 · ≈−22 mV("Li⁰ overpotential" 증가) ↔ MgSiGr ≈−19 · ≈−14 mV("Overpotential recovery"). Fig. 1C: SiGr **<20 h 단락** ↔ MgSiGr **>500 h**(`[인쇄]` "in excess of 500 h").
`[재현]` Mg 200 nm = 1.43 µmol cm⁻²(밀도 1.74) · "Li-Mg alloying" 구간 ≈0.125 mAh cm⁻² = 4.7 µmol Li ⇒ Li/Mg ≈3.3(≈77 at% Li) — bcc Li–Mg 고용체의 Li 풍부 쪽과 양립(`[해석]`), 단 같은 구간에 SiGr 리튬화가 섞여 분할 불가.
⚠ `[해석]` 인셋의 mV 차(≈3–8 mV)는 **2전극 합**이다 — 상대극 Li 박의 박리 과전압(압력 미인쇄)이 같은 전압에 들어간다. "overpotential recovery" 를 MgSiGr 전극에 귀속한 근거는 형태 비교뿐.

## 3.4 SEM-EDS (p. 3–4, Fig. 2, S8, S14)

`[인쇄]` 3.5 mAh cm⁻² 과충전(modified N/P 0.06): SiGr = "Li deposition inside the composite anode was irregular and sparse … pronounced Li dendritic growth" ↔ MgSiGr = "clearly distinguishable intermediate layer" + 그 아래 Li. "the deposition of Li beneath this layer not only decreases the contact area between Li and the SE to reduce the formation of the solid-electrolyte interphase (SEI) … but also contributes to enhancing the stability of the anode-SE interface. This interfacial stability is crucial for reliable operation at low stack pressure" — **SEI 감소는 기하 추론, SEI 정량 0**.
`[도표]` Fig. 2B 단면: Si-Gr / Li-Mg(≈2–4 µm) / Li / SUS 층상, Mg EDS 가 중간층에. Li 층 두께 ≈9 µm(5 µm 눈금 판독) ↔ `[재현]` 도금 ≈3.3 mAh cm⁻² 의 치밀 Li ≈16 µm(4.85 µm per mAh cm⁻²) — FIB 한 시야라 국소 · 다공 · SiGr 추가 흡수 중 무엇인지 모른다(칸 밖).

## 3.5 반쪽전지 CE · EIS (p. 4–5, Fig. 3, S13, S15–S17)

`[인쇄]` 3.5 mAh cm⁻² 첫 사이클 ICE **MgSiGr 90.3 % ↔ SiGr 85.2 %**("attributed to the stability of the underlying Li deposition") — `[도표]` Fig. 3A 박리 끝 ≈3.16 · ≈2.98 mAh cm⁻² → `[재현]` 90.3 · 85.1 % ✓. Fig. 3B: MgSiGr 1 mAh cm⁻² 250 사이클 · 3.5 mAh cm⁻² 100 사이클 CE ≈99–100 %, SiGr 는 ≈10 사이클 안에 흩어짐(`[도표]` 첫 점 ≈50 %, >100 % 점 하나).
S15: modified N/P 0.05 · 0.11 · 0.33 · 0.44(SiGr 적재 가변) — `[도표]` MgSiGr CE 평탄 ≈99.7 · ≈99.6 · ≈99.1 · ≈98.0 %(N/P 가 클수록 **낮다**), SiGr 는 전부 ≤20 사이클에 흩어짐. `[인쇄]` "the MgSiGr anodes performed more stably even at lower N/P ratios, a finding we attributed to the 0.1 V stripping voltage cutoff … only Li metal undergoes repeated plating and stripping". ⚠ 시험 길이가 160 · 60 · 37 · 30 사이클로 달라 "안정" 비교가 같은 창이 아니다.
**EIS**: `[인쇄]` "The x-intercept of the plot represents the bulk electrolyte resistance (RB), whereas the semi-circle corresponds to the charge transfer resistance (RCT)" · 연성 단락 셀은 "additional parallel resistance associated with this short circuit (rSS) is taken into account due to the substantial electronic conduction through it, which reduces RB and RCT accordingly" [23]. SiGr: "RB suddenly decreased from 23.6 to 15.7 Ω after 7 cycles, which indicated the onset of the short circuit" + 고주파 새 반원 = `R_SEI` "resulted from uncontrollable side reactions between the overcharged Li metal and the SE". MgSiGr: "consistently maintained RB without the appearance of new semi-circles over 50 cycles".
`[도표]` S17: 정상 · 연성 · 경성 단락의 도식 + 회로 — 연성 = `r_B`–(`r_CT`‖C) 전체에 `r_SS` 병렬, 겉보기 `R_B` · `R_CT` 가 준다. Fig. 3D MgSiGr Nyquist 에는 **반원 자체가 뚜렷하지 않다**(1st → 50th 곡선 모양 유지, `R_B` ≈24–25 Ω 판독). Ω 는 셀 절대값(∅13 mm, 면적 정규화 0).

## 3.6 in situ EIS 첫 충전 (p. 5, Fig. S18–S19)

`[인쇄]` 0.1 mAh cm⁻² 간격 EIS(**modified N/P 0.32** — Fig. 1 의 같은 전류 · 용량 0.22 와 다르다, D9). SiGr: "RB declined during the early charging stage of SiGr lithiation … in reflection of the growth of Li filaments through the SE even prior to overcharging" ↔ MgSiGr: "RB decreased to below its initial value during overcharge … indicating that the Mg film enhances the tolerance against a short circuit, particularly during the early pre-charge stage".
`[도표]` S19: SiGr `R_B` 19.2 → 18.2 → ≈17.8 Ω(세 점째부터 평탄) · MgSiGr 18.0 → 19.0 → 18.6 → 18.1 → 17.3 → 16.9 Ω. **두 음극 모두 ≈1–1.3 Ω(≈6–7 %) 줄고**, 차이는 언제 줄었는가(SiGr 단계 ↔ 도금 단계)뿐. `R_CT` 는 둘 다 ≈4.5–5.3 → ≈1 Ω.
⚠ `[해석]` 저자 자신의 S17 틀에서 `R_B` 감소 = 병렬 전자 경로 — MgSiGr 의 "초기값 아래로" 감소도 같은 틀로는 **도금 단계의 연성 단락 개시와 양립**한다. "tolerance" 는 시점 차이를 읽은 것이고, SE 치밀화 · SiGr 리튬화에 따른 전자 전도 변화 같은 대안은 논의 0. 셀 1 개씩(D3).

## 3.7 박리 컷오프 1.5 V (p. 5, Fig. S20 — 보지 않음)

`[인쇄]` SiGr 까지 매 사이클 탈리튬 — "the plain SiGr anode was short-circuited after only two cycles" ↔ MgSiGr "significantly improved the cyclability".

## 3.8 완전지 · 20 MPa (p. 5, Fig. 4)

`[인쇄]` "extremely low N/P ratio of 0.15" · 0.1C 형성: MgSiGr **185 mAh g⁻¹ · ICE 92.4 %** ↔ SiGr 176 · 87.7 % · MgSiGr "stable operation up to the 75th cycle with capacity retention of 83.7 %" ↔ SiGr "short circuit after just 16 cycles" · "**impressive average CE of 99.2 % for the 75 cycles**" · 율 181.2 / 166.5 / 160.1 / 156.1 mAh g⁻¹(0.1 / 0.3 / 0.5 / 1C 충전, 0.1C 방전).
`[도표]` Fig. 4D 라벨: "Cathode areal capacity: 3.6 mAh cm⁻² · N/P ratio: 0.15 · 0.2C (dis)charge cycles · 25 ℃, 20 MPa". MgSiGr 0.2C 방전 1 → 75 사이클 ≈170 → ≈143(`[재현]` 0.84 ✓). SiGr ≈162 → ≈116(14 사이클, 점이 끝남). Fig. 4C SiGr 16 번째 충전은 ≈3.9 V 에서 멈추지 않는다(무한 충전). **CE 축**: MgSiGr 1 사이클 `[도표]` ≈94 %, 2 사이클부터 마커가 100 % 틀에 **잘려** 중심을 못 읽는다(가시 윗가장자리 ≈99.6 %, 추정 중심 ≈99.3–99.5 %) — 인쇄 99.2 % 와 모순 없음, 그림으로는 99.2 ↔ 99.8 을 가를 분해능이 없다. SiGr CE ≈95–97 %.

## 3.9 XRM (p. 5–6, Fig. 5, S22)

`[인쇄]` "Following the first overcharge–discharge cycle during half-cell operation with a modified N/P ratio of 0.22" — SiGr: "cracks were initiated at the interface … propagation of these cracks through the SE" · "An internal pore mapping image revealed substantial contact loss along the interface" · "irregular morphologies" ↔ MgSiGr: "significantly smoother interface … prevented crack formation" · "the interface porosity was much lower compared to that of SiGr" · "uniform, flat appearance". "the smooth contact … aligns with one of the critical goals of this study, namely to enable operation under low stack pressure conditions".
`[도표]` Fig. 5: 시야 ≈0.3–0.4 mm(50 µm 눈금). A 는 균열 경로 표시("Crack initiation" · "Propagation"). **B · E 기공 지도는 둘 다 넓은 녹색 판** — E 가 조금 성기고 작아 보이나 크기 차를 그림으로 정할 수 없다. C 는 균열선이 보이고 F 는 균일. ⇒ **"substantial contact loss" 와 "much lower" 는 형용사**다 — 공극률 수 · 분할 문턱 · 반복 0, 반쪽전지 압력 미인쇄, 1 사이클 한 시점(`θ(N)` 아님).

## 3.10 저압 3 MPa (p. 6, Fig. 6A–D, S23–S24)

`[인쇄]` "The full-cell assessment was subsequently conducted at low stack pressure (3 MPa)" · 비교군에 **Li 금속 10 µm**("thickness identical to that of the MgSiGr anode (10 μm)", "to directly evaluate the impact of the Li plating position (top vs bottom)") · SiGr: "An abnormal capacity increase and considerable noise … indicating the onset of soft short circuits" [25] → 21 사이클 무한 충전(S24) · Li 금속: "early short-circuiting behavior at the 15th cycle due to the growth of Li dendrites" · MgSiGr: "stable voltage profiles for both the 1st and 15th cycles" · "maintained 64.7 % of the original capacity after 75 cycles under the challenging conditions of low stack pressure, room temperature, and a low N/P ratio of **0.66**".
`[도표]` Fig. 6D 라벨 "N/P ratio: 0.66 · 0.2C · 25 ℃, 3 MPa". 0.2C 첫 방전: **MgSiGr ≈115 · Li 금속 ≈140 · SiGr ≈70 mAh g⁻¹**. MgSiGr 75 사이클 ≈75. Li 금속 ≈140 → ≈105(≈13 사이클) 뒤 점 끝. SiGr ≈70 → ≈105(17 사이클, **증가**) → ≈90. **CE(속빈 원)**: MgSiGr ≈85–89 %(1–12) → ≈91–94 %(13–40) → ≈95–96.5 %(41–75) · Li 금속 ≈82–86 % · SiGr ≈62 → ≈75–90 % 흩어짐. Fig. 6C: MgSiGr 1 사이클 충전 ≈135 · 방전 ≈113(`[재현]` ≈84 %), 15 사이클 ≈120 · ≈111(≈92 %); 1 사이클 방전 곡선이 크게 기울어 3.5 V 아래에서 절반을 낸다.
⚠ 본문은 3 MPa 셀의 **CE 를 한 번도 적지 않고**, MgSiGr 첫 용량이 **같은 압력 · 같은 양극의 Li 10 µm 보다 ≈25 mAh g⁻¹(≈18 %) 낮은 것**도 적지 않는다(D10). SiGr 의 "abnormal capacity increase" 는 **방전** 용량의 증가다 — 연성 단락이 방전 용량을 늘리는 기구는 설명되지 않았고(`[해석]` 초기 분극 · 활성화와도 양립), 근거 [25] 는 액체 LIB 내부 단락 논문이다.

## 3.11 파우치 (p. 6–7, Fig. 6E, S25)

`[인쇄]` "N/P ratio of 0.6" · SiGr 파우치는 "short-circuiting during the first formation cycle at 0.1C, showing infinite charging" · MgSiGr "well-defined charge and discharge profiles" · "the transition from the SiGr charging stage to the Li plating stage (overcharging) proceeded smoothly" · "When cycled at 0.5C, the MgSiGr pouch-cell sustained short-circuit-free cycling for 75 cycles to demonstrate decent cyclability". **유지율 수치 0**.
`[도표]` Fig. 6E: 0.5C ≈113 → ≈51 mAh g⁻¹(`[재현]` ≈45 %). S25A 0.1C 형성 MgSiGr 충전 ≈210 · 방전 ≈163(`[재현]` ≈78 %) · SiGr 충전이 300 넘어 계속. S25B 0.5C 1 사이클 충전 ≈125 · 방전 ≈113, 10 사이클 방전 ≈87. 사진 속 파우치 라벨 "HMG-SNU Joint Battery Research Center" · HYUNDAI MOTOR GROUP 로고.

## 3.12 Fig. 7 · 결론 (p. 7, Fig. 7 — 보지 않음)

`[인쇄]` "the interfacial stability, the most critical factor for the cyclability of ASSBs operating at low stack pressure, highly depends on the lithiation kinetics of the anode, which, in turn, is largely determined by its lithiophilicity and geometrical features such as the pore volume" · "Low N/P ratio conditions enhance battery energy density but compromise long-term durability due to volume changes during overcharging, especially under low stack pressure. Potential improvements may involve the implementation of advanced elastic binders to maintain intimate inter-particle contact". 결론: "This anode design allows successful operation at remarkably low N/P ratios at room temperature and at low stack pressure".
`[해석]` "most critical factor" 는 **3 MPa 고정 음극 교체**로 받쳐진 명제이고, 저압 감쇠(MgSiGr 64.7 %)의 원인 문장("volume changes … especially under low stack pressure")은 **측정 0 의 해석**이다 — 부피 변화 · 압력 이력 · 양극 계면 어느 것도 재지 않았다.

## 3.13 SI 표 S1 · S2 — 이론 에너지 밀도 (렌더로 읽음)

| | SiGr 셀 | MgSiGr 과충전 셀 |
|---|---:|---:|
| SE 두께 | 30 µm | 30 µm |
| 음극 집전체 · 활물질 | 10 · 60 µm | 10 · 28 µm |
| N/P | 1.1 | 0.5 |
| in situ Li 도금 | — | 7.5 µm |
| 양극 집전체 · 활물질 | 10 · 60 µm | 10 · 60 µm |
| 셀 두께 | 170 µm | 138 (도금 포함 145.5) µm |
| 방전 전압 · 용량 · 면적 | 3.75 V · 30 mAh · 10 cm² | 같음 |
| 부피 에너지 밀도 | **662 Wh L⁻¹** | **815**(도금 포함 **773**) |

`[재현]` 112.5 mWh / (0.170 · 0.138 · 0.1455 cm³) = 662 · 815 · 773 ✓ · 도금 1.5 mAh cm⁻² × 4.85 µm = 7.3 ≈ 7.5 ✓ · 활물질 60/1.1 × 0.5 = 27.3 ≈ 28 ✓. ⚠ **이론표의 셀은 시험 셀이 아니다** — SE 30 µm(시험 펠릿 150 mg ∅13 mm 는 `[재현]` ≈0.7–0.8 mm(Li₆PS₅Cl 이론 밀도 1.64 g cm⁻³ 의 85–100 %), 파우치 시트 100 µm) · N/P 0.5(시험 0.15 · 0.66 · 0.6) · 두 셀 같은 용량 30 mAh(= 실측 용량 차 · 압력 비용 무시).

---

# 4. ★ Q6 판정 표 — 압력

| 구분 | 값 | 층위 |
|---|---|---|
| 제조 | SE 150 MPa · 셀 380 MPa(펠릿) · WIP 450 MPa 75 °C 15 min(파우치) | `[인쇄]` |
| 운전 — 펠릿 완전지 | **20 MPa**(N/P 0.15 · 양극 20 mg cm⁻² · 3.6 mAh cm⁻²) · **3 MPa**(N/P 0.66 · 6 mg cm⁻²) | `[인쇄]` 스프링 — 상수 · 변위 · 계측 0 |
| 운전 — 파우치 | **3 MPa**(N/P 0.6) · 볼트 넷 3.5 N·m | `[인쇄]` · 변환 0 · `[재현]` 표준 식이면 전극 면적 기준 17–29 MPa(G3) |
| 운전 — 반쪽전지 | **미인쇄** | G1 |
| 압력 비교 | **없다** — 두 점이 적재 ×3.3 · N/P ×4.4 · 음극 Li 몫(0.85 ↔ 0.34)과 같이 바뀐다 | — |
| 압력 이력 | 380 MPa 제조 → 운전으로 내린 절차 미기재(하강 분기, 25호와 같은 모양) | — |
| 저압 지배 기구(저자) | 음극 계면 안정성 = 친리튬성 + 기공 — **3 MPa 고정 음극 교체 비교** | 측정(음극 교체) + 해석(일반화) |
| 저압 감쇠 원인(MgSiGr) | "volume changes during overcharging, especially under low stack pressure" | **해석 한 줄, 측정 0** |
| 양극 쪽 | 0 — 양극 EIS · 영상 · 반쪽 분해 · 사후 분석 전수 0 | — |

`[재현]` **교락의 방향**: 20 → 3 MPa 에서 0.2C 첫 방전 ≈170 → ≈115 mAh g⁻¹(**−32 %**)인데 양극은 20 → 6 mg cm⁻² 로 **얇아졌다**(보통 비용량이 느는 쪽). `[해석]` 압력 + N/P 변화의 초기 비용은 −32 % 이상일 수 있다 — 25호(30 → 2 MPa, 두 미세구조 공통 −26.5 ↔ −30.7 mAh g⁻¹)와 **방향이 같다**. 그러나 두 조건의 음극 Li 몫(85 ↔ 34 %)이 다르고, 같은 3 MPa 에서 Li 10 µm 이 ≈140 을 내므로 비용의 일부는 **MgSiGr 음극 자체**다(D10) — 압력 몫을 떼어낼 수 없다.

---

# 5. `[재현]` 검산

## 5.1 20 MPa — 평균 CE ↔ 유지율

| | 값 | 근거 |
|---|---:|---|
| 평균 CE | 99.2 % | `[인쇄]` |
| ∏CE(75) | 0.992⁷⁵ ≈ **0.547** | 계산 |
| 유지율 | 83.7 % | `[인쇄]` |
| 유지율이 함의하는 사이클당 효율 | 0.837^(1/74) ≈ **99.76 %** | 계산 |
| 누적 충–방 결손 | Σ Q_dis (1/CE − 1) ≈ 11,740 × 0.00806 ≈ **95 mAh g⁻¹** | `[도표]` 방전 170 → 143 선형 |
| 관측 용량 손실 | ≈27 mAh g⁻¹ | `[도표]` |
| 형성 때 음극에 남은 Li(저장소 상한) | 충전 ≈200 − 방전 185 ≈ **15** | `[도표]` Fig. 4A · `[인쇄]` 185 |

⇒ 결손 95 가 전부 Li 손실이면 용량 손실 27 + 저장소 15 = 42 를 넘는 **≈50 mAh g⁻¹(결손의 ≈55 %)는 재고 손실로 설명되지 않는다.** 1 사이클(≈94 %)을 빼도(나머지 평균 ≈99.27 %) 결론 같음.

## 5.2 ★ 3 MPa — 누적 결손 ↔ Li 재고

화소 판독(§ 표기): 방전 용량 75 점(≈114.5 → ≈74.7, `[재현]` 비 0.652 ↔ `[인쇄]` 64.7 %) · CE 75 점(1–12 ≈85–89 %, 평균 ≈93.1 %).
- 누적 충–방 결손 Σ Q_dis (1/CE − 1) ≈ **575 mAh g⁻¹**(CE 판독 ±1 %p → ±≈80).
- ∏CE ≈ **0.005**.
- 비교: NCM811 이론 용량(= 양극이 처음 가진 Li 전부) ≈**275 mAh g⁻¹** · 관측 손실 ≈40 · 형성 뒤 첫 사이클 결손(≈22)만으로도 두 사이클이면 저장소 상한을 넘는다.

⇒ **결손은 양극 Li 재고의 ≈2 배** — 사이클 재고에서 빠진 Li 로는 불가능하다. 남는 해석(`[해석]`, 지면 밖): (i) **누설 전자** — 충전(특히 CV) 중 연성 단락(S17 `r_SS`) · 셔틀성 부반응이 Li 이동 없이 전하를 흘린다; (ii) **SE 분해가 Li 를 보충** — 양극 쪽 LPSCl 산화가 Li⁺ 를 내고 음극에 도금되면 재고가 채워지지만 그 자체가 부반응 전하다. 어느 쪽이든 **CE 결손 ≠ `LLI`**. 셀 1 개 · 그림 판독 위의 계산이다.

## 5.3 면적당 결손 — 적재 정규화

| | 사이클당 결손 | × 적재 | 면적당 |
|---|---:|---:|---:|
| 20 MPa | 95 / 75 ≈ 1.27 mAh g⁻¹ | 20 mg cm⁻² | **≈0.025 mAh cm⁻²** |
| 3 MPa | 575 / 75 ≈ 7.7 mAh g⁻¹ | 6 mg cm⁻² | **≈0.046 mAh cm⁻²** |

적재를 NCM 질량으로 읽음(1C 3.6 mA cm⁻² / 20 mg = 180 mAh g⁻¹ 기준과 양립). 조성 질량이면 둘 다 ×0.68 — 비 ×≈1.8 불변. 두 조건 모두 0.2C(충전 ≈5 h + CV). ⇒ **누설의 면적 속도는 ≈2 배 차**이고, CE 차(1 − CE: ≈0.8 ↔ ≈7 %)의 대부분은 분모(양극 용량 ×≈3.3 차)다. `[해석]` "저압이 CE 를 떨어뜨렸다" 로 읽으면 적재 정규화를 빠뜨린 것이다.

## 5.4 완전지 N/P

| 셀 | 양극 면적 용량 | N/P `[인쇄]` | 함의 N | ÷ SiGr 0.8 mg cm⁻² |
|---|---:|---:|---:|---:|
| 20 MPa | 3.6 mAh cm⁻²(`[인쇄]`) | 0.15 | 0.54 | **675 mAh g⁻¹** |
| 3 MPa | 6 mg × 180 = 1.08(`[재현]` 가정) | 0.66 | 0.71 | **≈890 mAh g⁻¹**(> 0.1C 최대 825) |

⇒ **인쇄된 적재 · 용량으로는 두 N/P 를 한 SiGr 용량으로 재현 못 한다**(D2). 3 MPa 셀의 음극 적재가 달랐거나(미인쇄) 기준이 다르다. 반쪽전지의 modified N/P 는 재현된다: 0.22 = 0.22 / 1.0 · 0.06 ≈ 0.22 / 3.5 = 0.063 · 0.22 mAh cm⁻² / 0.8 mg = 275 mAh g⁻¹ ≈ `[인쇄]` 277 ✓.

## 5.5 파우치 토크

3 MPa × 4 cm² = **1.2 kN**(볼트당 0.3 kN). `F = T/(K·d)`, K ≈ 0.2: M6 → 2.9 kN · M8 → 2.2 kN · M10 → 1.75 kN(볼트당) ⇒ 합 7–12 kN = 전극 면적 기준 **17–29 MPa**. 판 면적(미인쇄)이 ≈25–40 cm² 면 3 MPa 가 판 평균일 수 있다 — 어느 기준인지 원문이 말하지 않는다. PEEK 크리프에 따른 이완도 논의 0.

## 5.6 에너지 밀도 표 — §3.13 ✓

---

# 6. 용량 제한 전극 · 손실 배정 (α · β 전제)

- **충전 끝**: `[해석]` 양극. 도금 구간의 음극은 Li 금속(`[도표]` 반쪽 −15 … −22 mV)이라 완전지 전압 ≈ 양극 전위 + 과전압. N/P 0.15 이면 충전 용량의 ≈85 % 가 이 구간이다 — **이 구간의 2전극 곡선은 사실상 양극 반쪽 곡선**이고, 음극 OCP 는 기울기가 없다.
- **방전 끝(2.5 V)**: **미정**. 도금 Li 가 먼저 빠지고 SiGr 탈리튬(0.1–1.5 V vs Li, S11)이 마지막이다. 음극이 끝을 내면 방전 용량 = 순환 가능 Li → `LLI` 가 그대로 용량 손실. 양극이 끝을 내면(양극 재리튬화 한계) 음극에 남은 Li 가 저장소가 되어 `LLI` 를 가린다 — 그 모드에서는 **Li 를 잃어도 CE 가 1 에 가깝다**(양극이 준 만큼 받는다). 어느 모드인지 가를 3전극 · dV/dQ · 방전 끝 반쪽 전위가 없다.
- `[해석]` **평탄한 음극(Li 금속)은 OCV 적합의 `LLI` 슬리피지 서명을 지운다** — 액체셀 흑연처럼 음극 계단이 양극 곡선에 대해 미끄러지는 모양이 없고, `LLI` 는 끝점 이동으로만 나타난다. 그 끝점을 누가 내는지가 정해지지 않으면 `LLI` ↔ `LAM_PE` 는 같은 "용량 축 절단" 으로 보인다 — 45 · 48호 선례(2전극에서 음극 몫이 양극 용량 손실처럼 보이는 경로)의 **무음극형 판**.
- **배정**: 이 편은 용량 손실을 `LLI` · `LAM` · 접촉 어디에도 배정하지 않는다. 실패는 "short circuit"(전압 잡음 · 무한 충전 · `R_B` 급감)로, 반쪽 SiGr 의 새 고주파 반원은 `R_SEI` 로 이름 붙였다. **CE 는 "가역성" 의 증거로 쓰였다**(ICE 90.3 ↔ 85.2 %, "impressive average CE of 99.2 %") — 암묵적 `LLI` 대리다. §5.2 가 그 대리가 저압 셀에서 성립하지 않음을 보인다.

---

# 7. 계보 대조 — 13 · 14호가 이 편에 매단 것, 그리고 압력 계보

| 편 | 무엇을 매달았나 | 판정 |
|---|---|---|
| **14호** Oh 2025 *Angew.* ref [10] | `[인쇄]` "potential to support high-energy electrode materials such as Li metal anodes.[7–10]" | ✅ **선다(느슨하게)** — 이 편은 Li 금속 박이 아니라 SiGr 아래 **과충전 Li 도금**이다 |
| **13호** Zheng 2026 ref [34] | `[인쇄]` "substantial volume expansion (~280 %) … can be engineered against within composite electrodes through pre-lithiation, robust binders, and controlled porosity [34]" | ⚠ **약한 판** — 이 편은 선리튬화 · 바인더 · 기공 제어 **어느 것도 시연하지 않는다**. 접점은 결론의 제언("advanced elastic binders")과 "geometrical features such as the pore volume" 한 구절뿐 |
| 13호 digest 후속표 "저압 운전의 실셀 데이터" | 이것은 **우리 digest 의 이유 칸**이지 13호의 인용 문장이 아니다 | ✅ 이유는 선다 — 3 MPa 펠릿 · 파우치 실셀 데이터가 있다 |
| **14호 D12**("void 2 배 셀이 유지율 더 높음" — void ≠ 용량) | — | `[해석]` **양립, 한 걸음 더**: 이 편에서 음극 계면 공극 · 균열은 용량 감쇠가 아니라 **단락(전압 잡음 · 무한 충전 · 방전 용량 "증가")** 으로 나타난다. void 가 용량에 보이면 **반대 부호**로 보일 수 있다 — 누설이 충전 용량을 늘린다 |
| **13호 SOH 이분법**(true AM loss ↔ usable capacity) | — | 이 편은 둘 다 재지 않는다 |
| **14호 세 번째 축(void)** | — | 음극 void 는 여기서 **단락 · 누설 축**과 한 몸이다 — SOH 를 셋으로 둔다면 누설(CE 결손 − Li 손실)이 넷째 후보(`[해석]`) |
| **25호** Zhou 2025(운전 30 · 10 · 2 MPa × 미세구조) | — | 이 편은 요인 설계가 아니다. 방향(저압 초기 비용)은 같다(§4) |
| **33호** Zhang 2025 종설 띠 0.4–5 MPa · 산업 "< 2 MPa" | — | 3 MPa 1차 운전값 — 띠 안, 산업 요구치 위 |
| **39호** Sakka 2022(제조 압력 5 점) | — | 제조 ↔ 운전 축이 이 편에서도 갈린다(380 ↔ 3/20) |
| **41호** Nam 2018(CE → `LLI` 세 번째 오염 "연성 단락 누설" · 첫 사이클 끝을 양극이 낸다) | — | ★ 이 편이 **크기**를 준다(§5.2) — 그리고 끝 전극은 이 편에서 판정 불가 |

---

# 8. 곱 축퇴 처방 — 서른다섯 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| 1단계 `R`·`C` 짝 | 반쪽전지 `R_B` · `R_CT` 만(음극), `C` 미인쇄, 양극 0 | ❌ |
| 2단계 면적 대조군 | 음극 교체(SiGr ↔ MgSiGr ↔ Li) — 음극 쪽 | ❌(양극 곱 대상 아님) |
| 3-a `Ea` | 25 °C 한 온도 | ❌ |
| 3-b `C` 상한 | 없음 | ❌ |
| 4단계 시간 영역 | 없음 | ❌ |

**곱이 선 자리**: 양극 곱(`A_eff·ε_p/R_s`)은 입력이 없다. 대신 **그 앞 단계**에 구멍이 있다 — 2전극 용량 손실을 `LAM_PE` · 접촉(`θ`) · `LLI` 로 나누기 **전에** CE 결손이 Li 재고 손실인지부터 검사해야 하는데, 이 편에서는 그 검사가 실패한다(§5.2).
**처방에 더하는 것 — 새 줄 "누적 충–방 결손 ↔ Li 재고 상한 · 관측 용량 손실 대조"**: (1) Σ(Q_ch − Q_dis) 를 양극 이론 Li 재고 · 형성 때 남은 저장소 · 관측 용량 손실과 대조한다 — 결손이 재고를 넘으면 초과분은 누설이다; (2) 조건 간 CE 비교는 **면적당 결손**으로 바꿔 적재 정규화를 뺀다; (3) 끝 전극 모드(양극 끝이면 `LLI` 가 CE 에 안 보인다)를 먼저 정한다. 44호 "Li 재고 수지(한 사이클, 방전 > 충전)" 의 다중 사이클 · 반대 부호 판.
**⚠ 이것이 곱을 푼 것은 아니다** — 양극 채널 0 · 셀 1 · 그림 판독.

---

# 9. Q1 · Q2 · Q4 · Q5 · Q7

- **Q1**: `θ(N)` **0/52**. 접촉 = 음극 \| SE XRM(1 시점 · 정성).
- **Q2**: 없다 — 양극 독립 관측 0. 음극 쪽 관측(SEM-EDS · XRM · 반쪽 EIS)은 `LAM_PE` ↔ 접촉과 무관.
- **Q4**: **0/52 — 마흔네 번째 성질 "가역성의 지표(CE)를 인쇄한 조건에서만 인쇄했다"** — 20 MPa 평균 CE 99.2 % 는 본문에, 3 MPa CE(≈85–97 %)는 그림에만. 같은 지면의 유지율과 대조 0(20 MPa 도 ∏CE 0.55 ↔ 0.837). 식별성 낱말 전수 0.
- **Q5**: 해당 없음 — In 0. 반쪽전지 "vs Li/Li⁺" 의 영점은 **상대극 Li 박**(압력 미인쇄)이고 그 박리 과전압이 도금 전압 mV 판독에 들어간다(§3.3).
- **Q7**: 없다 — dead Li ↔ SEI Li 미분리(`dead` · 적정 · 재고 수지 0). 무음극형 셀의 CE 는 여기서 둘 중 어느 것의 추정자도 아니다(§5.2).
- **Q8**: NCM811(LiNbO₃) · OCP 0.

---

# 10. 채움표 행 (Q1–Q8)

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **없다 — `θ(N)` 0/52.** 접촉 관측은 음극 \| SE XRM 한 쌍(반쪽 · 1 사이클 뒤 · 압력 미인쇄) — "substantial contact loss" · "much lower" 는 형용사, 수치 0 | **없다(양극).** 음극 교체 비교 · SEM-EDS · XRM · 반쪽 EIS 는 음극 계면 | **measured-2electrode + imaging-qualitative + ECM(EC-Lab, 값 두 개)** · 실패 라벨 = 전압 잡음 · 무한 충전 · `R_B` 급감(`r_SS` 병렬 도식) · ± 0 · 조건당 셀 1 · **3 MPa CE 는 그림에만** | **0/52 — 마흔네 번째 성질** | 해당 없음 — Li 박 상대극 영점 | **운전 20 · 3 MPa(스프링) · 파우치 3 MPa(토크 3.5 N·m, 변환 0) · 제조 150/380/450 명시 · 반쪽 압력 미인쇄 · 두 압력이 적재 · N/P 와 교락 — 반 칸 검토 후 접음** | 없다 — 무음극형인데 dead ↔ SEI 0, CE 결손은 재고를 넘는다(`[재현]`) | NCM811 · OCP 0 |

---

# 11. 어긋남 (실제로 어긋난 것만)

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | 제목 "Extremely Low N/P Ratio **Operating at** Low Stack Pressure" ↔ N/P 0.15 는 **20 MPa** 에서만, 3 MPa 는 0.66 · 0.6 | `[인쇄]` Fig. 4 · 6 캡션 |
| **D2** | 완전지 N/P 0.15 · 0.66 을 인쇄 적재(SiGr 0.8 mg · 양극 20 / 6 mg)로 한 SiGr 용량으로 재현 불가(675 ↔ ≈890 mAh g⁻¹, 후자는 0.1C 최대 825 초과) | §5.4 |
| **D3** | MgSiGr `R_B` 가 "초기값 아래로" 준 것을 "tolerance against a short circuit" 로 읽음 ↔ 같은 SI S17 틀에서 `R_B` 감소 = 병렬 전자 경로 · 두 음극 모두 ≈−1 Ω | §3.6 · `[도표]` S19 |
| **D4** | "interface porosity was much lower" ↔ `[도표]` 두 기공 지도가 둘 다 넓게 칠해짐, 수치 0 | Fig. 5B · E |
| **D5** | ★ 3 MPa MgSiGr CE ≈85–97 %(`[도표]`) — 본문 무언급 · "stable" · 누적 결손 ≈575 mAh g⁻¹ > 양극 Li 재고 ≈275 | §5.2 |
| **D6** | 20 MPa "impressive average CE of 99.2 %" ↔ 유지율 83.7 %(∏CE 0.55 · 결손 ≈95 ↔ 손실 ≈27) — 대조 0 | §5.1 |
| **D7** | 13호 [34] "pre-lithiation, robust binders, and controlled porosity" ↔ 이 편은 셋 다 시연 0 | §7 |
| **D8** | "Precise control of the stack pressure" ↔ 스프링 상수 · 변위 · 계측 0 · 파우치 토크 → 3 MPa 변환 0(`[재현]` 표준 식 17–29 MPa @4 cm²) | §5.5 |
| **D9** | S18 in situ EIS 셀 modified N/P **0.32** ↔ 같은 1 mA cm⁻² · 1 mAh cm⁻² 의 Fig. 1 은 **0.22** | `[인쇄]` 캡션 |
| **D10** | 3 MPa 첫 0.2C 방전 MgSiGr ≈115 < Li 10 µm ≈140 mAh g⁻¹(같은 양극 · 압력) — 무언급, "stable voltage profiles" | `[도표]` Fig. 6D |
| **D11** | "277 mAh g⁻¹ … the utilization of the SiGr at this current density was limited" ↔ `[도표]` S11B 0.01 V 에서 ≈640 까지 계속 · 탈리튬 ≈440 | §3.2 |
| **D12** | 파우치 "decent cyclability" ↔ `[도표]` 75 사이클 ≈45 %(0.5C), 수치 미인쇄 | §3.11 |
| D13 | SiGr 3 MPa "abnormal capacity increase" = **방전** 용량 증가(≈70 → ≈105)를 연성 단락으로 — 기구 설명 0, 근거 [25] 액체 LIB | §3.10 |
| D14 | Fig. 2B Li 층 `[도표]` ≈9 µm ↔ 도금 3.3 mAh cm⁻² 치밀 Li ≈16 µm(국소 FIB) | §3.4 |

---

# 12. 그림 — 무엇을 봤나

크로퍼(`wiki/tools/extract_figures.py`)가 본문 7 + SI 25 = 32 장 + SI 표 2 장(이미지) = **34 장**을 잡았다. **Read 로 본 것 14 장**: Fig. 1 · 2 · 3 · 4 · 5 · 6 · S11 · S15 · S17 · S19 · S23 · S25 · 표 S1 · 표 S2. **화소 판독**: Fig. 4D(CE 마커가 100 % 틀에 잘려 판독 한계 — §3.8) · Fig. 6D(용량 · CE 75 점, §5.2).
**안 본 것 20 장**: Fig. 7(도식) · S1(도식) · S2(에너지 밀도 막대 — 표 S1 · S2 로 대신) · S3 · S4(Mg 막 SEM) · S5(SUS 반쪽 CE) · S6 · S7(SiGr SEM · XRD) · S8(MgSiGr 단면) · S9 · S10(LPSCl 전도도 · XRD · Raman) · S12(CV) · S13(전압–시간) · S14(51 사이클 뒤 단면) · S16(등가회로) · S18(in situ Nyquist) · S20(1.5 V 컷오프) · S21(NCM SEM) · S22(XRM x–z) · S24(무한 충전) — 캡션 · 본문 인용으로만 다뤘다.
본문과 그림이 어긋난 곳: D3(S19) · D4(Fig. 5) · D5 · D10(Fig. 6D) · D11(S11B) · D12(Fig. 6E) · D14(Fig. 2B).

---

# 13. 참고문헌 중 후속 후보 (25 항목, 서지 기준 — 미열람)

1. ★★ **[12b] Oh, Chung, Jung, Kim, Lee, Nam, Lee, Kim, Choi, *Energy Storage Mater.* 2024, 71, 103606** · **[12c] Oh, Choi, Kim, …, Bae, Son, Choi, *Adv. Energy Mater.* 2023, 13, 2301508** — "requirement for high operating temperatures and pressures" 의 근거로 붙은 **같은 연구실의 앞선 압력 편 둘**(Q6).
2. ★★ **[23] Menkin, Fritzke, Larner, de Leeuw, Choi, Gunnarsdóttir, Grey, *Faraday Discuss.* 2024, 248, 277** — 연성 단락 병렬 `r_SS` 틀의 근거(CE 누설 해석의 원전 후보, Q7 · 41호 오염 경로).
3. ★ **[16a] Chen … Li, *ACS Appl. Energy Mater.* 2021, 4, 4879** · **[16b] Yan … Chen, *Adv. Energy Mater.* 2022, 12, 2102283** — "void spaces after stripping … difficult to self-heal under low stack pressure" 의 근거(Q6 아래 벽 · 음극).
4. ★ **[9b] Lee, Choi, Im, …, Choi, *Adv. Mater.* 2022, 34, 2203580** · **[9c] Oh, Choi, Chang, …, Choi, *ACS Energy Lett.* 2022, 7, 1374** — 같은 연구실 무음극 편(Q7).
5. [13a] Kim, Lee, Han, Kim, Yoo, *J. Power Sources* 2024, 601, 234301 — "At low N/P ratios, Li deposition becomes more inhomogeneous".
6. [24] Shearing … Harris, *J. Electrochem. Soc.* 2012, 159, A1023 — XRM 방법 인용.
7. [25] Huang … Sauer, Ouyang, *Int. J. Energy Res.* 2021, 45, 15797 — "soft short circuits" 판정 근거(액체 LIB).
큐 54–59(Ren 2023 · Neumann 2021 · Hlushkou 2018 · Bielefeld 2022 · Bielefeld 2020 · Asheri 2023) **인용 0**.

---

# 14. 이 digest 가 주장하지 않는 것

- **MgSiGr 설계가 효과 없다고 하지 않는다.** 같은 압력 · 같은 양극에서 SiGr · Li 10 µm 이 15–21 사이클에 단락하고 MgSiGr 이 75 사이클을 간 것은 지면의 측정이다(조건당 셀 1).
- **3 MPa 셀에 연성 단락이 있었다고 단정하지 않는다.** §5.2 는 "CE 결손이 사이클 Li 손실이 아니다" 까지이고, 누설 전자 · SE 분해 보충 중 어느 것인지는 지면으로 못 가른다.
- **압력이 CE 를 떨어뜨렸다고도, 안 떨어뜨렸다고도 하지 않는다.** 적재 · N/P 가 같이 바뀌었고, 면적당 결손 ×≈1.8 은 적재 = NCM 질량 가정 위의 계산이다.
- **파우치 압력이 3 MPa 가 아니라고 하지 않는다.** 토크 계산은 볼트 규격 · 판 면적 · 마찰 계수를 가정한 것이다 — 변환 근거가 없다는 것까지다.
- **그림 판독값을 인용하지 않는다.** CE ±1 %p · 용량 ±2 mAh g⁻¹, 셀 1 개. 수치의 정본은 원문이다.

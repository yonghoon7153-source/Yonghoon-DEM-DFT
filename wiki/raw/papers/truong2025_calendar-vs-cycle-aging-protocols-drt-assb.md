---
title: "Truong T.K., Whang G., Huang J., Sandoval S.E., Zeier W.G. 2025 — Probing solid-state battery aging: evaluating calendar vs. cycle aging protocols via time-resolved electrochemical impedance spectroscopy (J. Mater. Chem. A 13, 17261–17270)"
source_url: local-upload/1._Probing_solid-state_battery_aging_evaluating_calendar_vs._cycle_aging_protocols_via_time-resolved_electrochemical_impedance_spectroscopy.pdf
source_url_si: local-upload/1._Sup2_Probing_solid-state_battery_aging_evaluating_calendar_vs._cycle_aging_protocols_via_time-resolved_electrochemical_impedance_spectroscopy.pdf
source_url_note: "본문 PDF 10 쪽(J. Mater. Chem. A 2025, 13, 17261–17270 · 기사 유형 띠 'REVIEW' — 내용은 1차 실험 · 그림 7 · 표 0 · 번호 식 1 · 참고문헌 37) 1,560,581 B + ESI PDF 12 쪽(그림 S1–S14 · 표 0 · 참고문헌 4) 5,612,169 B + 보충 데이터 ZIP '1._Sup1_Probing_solid-state_battery_aging_evaluating_calendar_vs._cycle_aging_protocols_via_time-resolved_electrochemical_impedance_spectroscopy.zip'(바깥 7,671,637 B · sha256 = data_sha256 · 항목 1 = 무압축 data.zip 7,671,479 B · data.zip sha256 ba108aba62c471311dfa5ce62b44acedbb4f90502754a47405f0f34fef559143 · 안쪽 1,273 항목 = 폴더 47 + 파일 1,226 · 본문 그림 1–7 · 컷오프 3.7 · 3.9 · 4.1 V 만 · SI 그림 자료 0 · 원자료는 커밋하지 않음 — 구조 · sha256 · 재현에 쓴 파일 이름과 결과만) · 업로드 파일 이름의 접두(업로드 식별자)는 뺐다 · 2026-10-02 사용자 공급 · 파일명 번호 1 · 원장 지목 0 · 그림 21 항목(자동 21 — 전부 봄 · 화소 판독 S4) · 저장소 DOI 10.17879/14908422666 미열람"
source_doi: 10.1039/D5TA01083G
source_license: "CC BY 4.0(p. 1 띠 'Licensed under CC-BY 4.0' · 쪽 바닥 © The Royal Society of Chemistry 2025) — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기 · 화소 판독은 판독용 · 커밋 안 함)"
pdf_sha256: 585bba0d4fcddc6015b36d847b689efbc04204643ad6e70faec4c2fdd5aacee2
si_sha256: d0b39576974b0586b1d47c7ec1171772f95f8db94117c38e036e4a56c125971b
data_sha256: 0f792d1164ec71c48764028e66f71263d9f99a278eb7d1937febede6415e796e
ingested: 2026-10-02
sha256: 7a5925bdaf3e3e2454cd8a966a5b7d82f1dac3766c4f4cc0393c93466dbe4162
---
# 수집 목적

`assb` 섹션 **90호** — **2026-10-02 사용자 공급 · 업로드 파일명 번호 "1" · 원장 지목 0**. 사용자 말: "이건 assb 관련한거야. assb로 잘 분류해서 부탁할게용". 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) · 위키 전체에서 `Truong` · `D5TA01083G` · `calendar vs` grep 0(호출자 실측) — **원장 밖에서 온 새 편**이다(3차 묶음 파일 21–50 = 59–89호는 끝났다).
뮌스터대 무기 · 분석화학연구소 + FZ Jülich IMD-4(Helmholtz-Institut Münster) Zeier 연구실의 *J. Mater. Chem. A* 논문으로, **In/InLi | Li₆PS₅Cl | NCM83 : Li₆PS₅Cl(7 : 3) 반쪽전지**에 상한 전위 다섯(3.7 · 3.8 · 3.9 · 4.0 · 4.1 V vs In/InLi)을 두고 두 "가속 노화" — **(1) 48 h 정전위 유지(calendar · float) · (2) 약 48 h 의 1C 사이클(cycle)** — 를 같은 형성(0.1C × 3) · RPT(0.1C × 3) 사이에 끼워, **용량 손실 · ΔV(50 % SoC) · dQ/dV · 시간분해 EIS → DRT(hybrid-drt)** 로 비교한 편이다. 결론은 "calendar 쪽이 훨씬 나빠지고, calendar 에서는 양극–전해질 계면 저항(P_C), cycle 에서는 음극(In/InLi)–전해질 계면(P_A)이 지배 · 영향" 이고, 정전위 유지를 **빠른 선별(screening) 프로토콜**로 권한다.
닻은 `questions/assb-contact-loss-vs-lampe.md`(양극 판 — Q1 · Q2 · Q4 · Q5 · Q7 이 직접 걸린다).

들어온 경로: 사용자 직접 공급(본문 PDF · 보충 ZIP(원자료) · ESI PDF). 지목 digest **0**(위 grep). **이 편이 우리 digest 셋을 인용한다** — [11] Huo D. 외 2025 *JPS* 627, 235830(= 우리 `assb` **9호**) · [27] Koerver R. 외 2017 *Chem. Mater.* 29, 5574(= **23호**) · [33] Yu C.-Y. 외 2024 *JPS* 597, 234116(= **11호** — 가장 가까운 선행).

이 digest 의 일 (지시):

1. **(a) "calendar aging" 의 실체** — 개회로 보관인가 정전위 유지인가 · 유지 전위 · 시간 · 온도 · RPT · cycle 조건 표 · 두 프로토콜을 무엇으로 맞췄나(벽시계 · RPT · 통과 전하 · 상한 체류) — 데이터 ZIP 으로 상한 체류 시간 재현.
2. **(b) 전위 기준** — In/InLi ↔ Li⁺/Li 환산(42호 값 · 조건) · 64호 컷오프 시험과 같은 축.
3. **(c) DRT 귀속의 근거** — 양극 · 음극 계면 봉우리를 무엇으로 갈랐나 · λ · 소프트웨어 · 주파수 · 봉우리 수 · "cycle 은 음극" 이 직접 증거인가.
4. **(d) 용량 손실의 분해** — dQ/dV · ΔV–Q_loss 가 무엇을 재나 · Q1 · Q7 · 채움표 칸.
5. **(e) 데이터 재현** — ZIP 으로 핵심 수치 2–4 개 · 폴더 수 · 그림 대응 · 빠진 그림.
6. **(f) Q4 · Q5 · Q6 · Q8** — 식별성 어휘 전수 · Li-In 기준 · 운전 압력(명목 ↔ 계측) · 기타.
7. **(g) 우리 위키와의 관계** — Yu 2024 대조 · Huo 2025 인용의 쓰임 · 정전위 유지 노화가 합성 truth · 모형에 요구하는 것.
8. **(h) SI** — 12 쪽 전부 · 그림 · 표 목록 · 본문 참조 대조.
9. **(i) 후속 후보** — 우리 축의 원전만 · 지목 수는 각 digest 후속 절 grep 값.

> ⚠ **형식 — *J. Mater. Chem. A* 2025, 13, 17261–17270 · p. 1 띠에 기사 유형 `[인쇄]` "REVIEW"(쪽 머리 "Review") — 그러나 내용은 1차 실험 편이다(`[해석]` — 서론 · 결과와 논의 · 결론 · 실험은 ESI; D10).** 오픈액세스 `[인쇄]` "Published on 13 May 2025 · Licensed under CC-BY 4.0"(creativecommons.org/licenses/by/4.0/ 링크).
> 본문 PDF 10 쪽 — p. 1 제목 · 저자 · 초록 · 서론 시작 · 소속 · ESI 각주 · 일정 · pp. 2–9 서론 · 결과와 논의(소절 제목 없음) · 결론 · 데이터 가용성 · COI · 사사 · pp. 9–10 참고문헌 **37** · 그림 **7** · 표 **0** · 번호 식 **1**(Q_loss) · **저자 기여 절 0**.
> ESI PDF 12 쪽 — p. 1 표지(제목 · 저자 · 소속 · 교신 이메일) · pp. 2–4 실험(SE 합성 · 복합 양극 · 셀 조립 · 전기화학 · DRT · 노화 절차) · pp. 4–12 그림 **S1–S14** · p. 12 참고문헌 **4** · 표 **0** · 번호 식 **1**(DRT 적분식).
> 보충 ZIP — 바깥 `…Sup1….zip`(7,671,637 B) 안에 무압축 `data.zip`(7,671,479 B) 하나 · 그 안에 **1,273 항목(폴더 47 · 파일 1,226)** — `data/Figure 1 …` ~ `data/Figure 7 …` **본문 그림 1–7 만**(SI 그림 0 · 3.8 · 4.0 V 0 — §보충 자료).
> 표기: `[인쇄]` 본문 · 캡션 · ESI 명시 · `[도표]` 그림에서만 읽은 값(판독 폭 병기 · 화소 판독은 `[도표·화소]`) · `[데이터]` 보충 ZIP 의 원자료 값(판독 아님) · `[재현]` 우리가 지면 · 자료의 숫자로 계산 · 대조한 값(외부 상수 · 가정은 `[재현·외부 값]` · `[재현·가정]`) · `[해석]` 우리 해석. `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.
> 층위를 가른다 — **측정**(이 편 셀 열: 컷오프 다섯 × 프로토콜 둘 · 25 ℃ · 조건당 셀 수 인쇄 0) · **인용**(분해 개시 전위 3.58–3.7 V vs In/InLi[5,13,15] · τ 대역 귀속[31,33,34] · 정전위 유지의 한계[7]) · **모형** 0(DRT 역변환은 방법 — 물리 모형 아님).

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **(a) "calendar aging" 의 실체** | **개회로 보관이 아니다 — 상한 전위 정전위 유지(float) 48 h 이다.** `[인쇄]` "A potentiostatic hold (also known as float test or voltage hold) protocol[3,6] was employed as a qualitative accelerated tool for calendar aging tests" · ESI "charged up to a cut-off with a constant current (CC) mode at 0.1C, followed by a constant voltage mode for 48 h before being discharged by another CC mode at 0.1C" | 두 프로토콜은 **명목 시간 "48 h" 와 같은 형성 · RPT 틀**로만 맞춰졌다 — `[데이터]` 상한 ±1.5 mV 체류 **calendar 48.00 h ↔ cycle 0.00–0.01 h** · 상한 50 mV 안 48.0–48.2 ↔ **0.9–2.5 h** · 3.58 V 이상 48.7–49.3 ↔ **6.4–17.8 h** · 통과 전하 **≈300(calendar · `[데이터]`+`[도표]`) ↔ ≈9,000–10,150 mAh g⁻¹(cycle · `[데이터]`)** · 최대 탈리튬 깊이 ≈158–169(`[도표]` S12) ↔ ≈92–104 mAh g⁻¹(`[재현·가정]`) — "calendar 가 훨씬 나쁘다" 는 **"같은 명목 시간 · 25 ℃ · 같은 컷오프 숫자"** 조건에서만 선다(같은 컷오프 숫자가 같은 충전 깊이 · 같은 고전위 체류가 아니다) |
| (a') 시간 축 | ⚠ **그림 1 · 2 · S1 · 자료의 시간 축은 휴지 · EIS 를 뺀 시간이다** | `[데이터]` 방전 끝 2.0 V 뒤 이완형 전위 상승이 **같은 시각 값**으로 기록 · 1C 구간 CC 시간 47.73 · 50.04 · 50.76 h(3.7 · 3.9 · 4.1 V) · 정전위 구간은 정확히 48.00 h · `[인쇄]` 30 분 OCV 휴지(1C 구간은 두 사이클마다) · `[재현]` 38–40 회 × 30 분 ≈19–20 h 가 축 밖 — 캡션 미표기(D8) |
| **(b) 전위 기준** | **In/InLi 기준(인쇄) · Li⁺/Li 환산을 지면이 +0.62 V 로 인쇄(출처 0)** — 3.7 · 3.8 · 3.9 · 4.0 · 4.1 V vs In/InLi = 4.32 · 4.42 · 4.52 · 4.62 · 4.72 V vs Li⁺/Li · 형성 · RPT 창 2.0–3.7 V(= 2.62–4.32) | `[재현]` In 50 mg + Li 1.2 mg = **28.42 at% Li ✅** · 양극 이론 1.40 mAh 전부 받아도 34.1 at% — **42호 평탄 창(≈1–47 at%) 안 · 이완 OCV ≈0.622–0.625 V(1–40 at% 띠)** — 단 42호 값은 **액체 3전극 · 실온 · 0.5 h 이완 · 전기화학 리튬화 박**의 값이다(이 편은 고체 · 압착 박) · 조립 방향 `[인쇄]` "In foil was in contact with the solid electrolyte while the Li foil was in contact with the current collector" = 21호 **InLi-(In) 형**(원천 역할 미검사) · 64호 같은 축: 64호 3.4 · 3.7 · 4.0 · 4.4 V vs In(무 Li In · +0.6) = 4.0 · 4.3 · 4.6 · 5.0 V vs Li → 이 편 띠 4.32–4.72 는 64호 **4.3 ↔ 4.6 V 사이 + 그 위** |
| **(c) DRT 귀속의 근거** | **가정 의존 — 문헌 τ 대역[31,33,34] + 봉우리 연속성(2D DRT)뿐 · 대칭셀 · 3전극 · 온도 · 정전용량 대조 0.** calendar 의 "양극 계면 지배" 는 **연속성 + 우리 `[재현]` C_eff 평탄으로 지지(조건부 성립)** · cycle 의 "음극 계면 영향" 은 **불성립에 가깝다(직접 증거 0 · 기준선 문제)** | `[데이터]` 3.9 · 4.1 V 유지 48 h 의 지배 봉우리가 **τ = 0.19 · 0.54 s — 지면이 P_A 에 준 창(10⁻¹–1 s) 안**으로 이동(1 h 5.4 · 17 ms) — 이름은 연속성으로 유지 · `[재현]` 그 봉우리 C_eff = τ/R **1.6–2.5 µF 로 평탄(R ×4–27)** ↔ cycle P_A C_eff **≈1.5–3.3 mF**(이중층 ≈10 µF cm⁻² 의 ×190–520 — 23 · 84호처럼 "전하 이동" 이름표가 C 상한을 못 넘는다) · cycle 의 시간분해 EIS 는 **1C 방전 끝(상태 표류)** · 그림 6 의 "before aging" 은 **한 셀 스펙트럼(= 그림 4)을 여섯 셀 공통 기준으로** — 자기 셀 기준(S4 `[도표·화소]`)이면 cycle 셀 저주파 Re 는 **−40 · −30 · −4 Ω(줄었다)** |
| (c') DRT 방법 | **hybrid-drt(계층 베이즈 MAP · "without manual parameter tuning") · 7 MHz–50 mHz · 10 mV rms · K–K 통과 인쇄 · τ 기저 측정 창 ±1 자릿수 확장 · λ · 사전 · 초모수 인쇄 0** | `[데이터]` τ 격자 284 점(2.1×10⁻¹¹–3.4×10³ s · ≈20 점/자릿수) · 전형 DRT(그림 4)에서 **측정 하한(τ_max 3.18 s) 밖 몫 257 Ω / 970 Ω(26 %)** — P_D(τ ≈10.5 s)는 창 밖 · "다섯 봉우리" 중 P_C2 는 국소 극대가 아니라 어깨 |
| **(d) 용량 손실의 분해** | **가르지 않는다 — ΔV(50 % SoC)와 Q_loss 는 같은 0.1C 곡선에서 뽑은 두 수의 동행이다.** dQ/dV 봉우리 세기 ↓ 를 "loss of lithium inventory in the CAM"[23] 으로 읽는다(검사 0) | `[재현·가정]` ΔV 증가를 균일 분극 이동으로 놓으면 calendar 손실의 **≈1/8–1/3**(1.5 · 7.3 · 13.4 % ↔ 12.0 · 31.0 · 41.8 %)만 설명 — 나머지는 열역학(LAM_PE · CAM Li 갇힘)이든 SOC 의존 동역학이든 이 편 자료로 못 가른다 · Q7: In/InLi 공칭 Li 재고 **×3.31**(4.63 ↔ 1.40 mAh `[재현]`) — 접근 가능하면 LLI 는 용량에 안 보이고, InLi-(In) 조립이라 접근성은 미검사 → **판정 불가** · Q1: `θ(N)` 0/90 |
| **(e) 데이터 재현** | **부분 일치 — 그리고 자료 무결성 문제 둘** | ✅ 1C 전류 = 200 mA g⁻¹(그림 7 Q ÷ 그림 2 시간 199.6–200.6) · ΔV 표 여섯 값 · 2D DRT 색 막대 최댓값 여섯(543 Ω · 27.9 kΩ · 347 kΩ · 64.5 · 73.7 · 134.6 Ω) · 28.42 at% · 1.783 mAh cm⁻² · ❌ **그림 2 "4.1 V calendar" 자료의 RPT 구간 = "3.9 V calendar" RPT 구간의 시간 이동 복사(9,794 연속 표본 · 전위 · 시간 증분 동일 · Δt 0.8732 h — D1)** · ❌ **Q_loss 기준선**: 그림 2 ↔ 3 이 닫히는 두 cycle 셀에서 인쇄 9.80 · 9.29 % 는 **첫 형성 방전 기준**(9.69 · 9.32 %)으로만 재현 — 지면 정의(마지막 = 3번째 형성)면 **2.99 · 2.83 %**(D2) · ⚠ 그림 2 ↔ 3 폐합은 여섯 셀 중 셋(3.9 calendar 2 % 비례 · 3.9 · 4.1 cycle 0.1–0.3 %) |
| (e') ZIP 구조 | **본문 그림 1–7 만 · 세 컷오프(3.7 · 3.9 · 4.1 V)만 · SI 그림 0** | 폴더 ↔ 그림: 그림 1(= 3.9 V 두 셀의 세 구간) · 2(여섯 셀) · 3(a–d 32 + e · f 표 2) · 4(3) · 5(261) · 6(16) · 7(900) = 1,226 파일 · 3.8 · 4.0 V 값은 그림 3e · f 표 두 줄뿐 · 저장소 DOI 10.17879/14908422666 은 **열람하지 않았다**(네트워크 대조 0 — 같은 자료인지 미확정) |
| **(f) Q4 · Q5 · Q6 · Q8** | **Q4 0/90 — 여든두 번째 성질** · Q5 **서른네 번째 형태**(조성 · 조립 방향 · 환산 인쇄 · 출처 0) · Q6 **SI 에만**: "a torque of 10 Nm providing an operating stack pressure of ~50 MPa"(토크 명목 · 계측 0 · 환산 근거 0) · 성형 "3 tons" · Q8 NCM83(MSE) · OCV 0 | `identif` 3(일반 뜻) · `uniq` · `uncertain` · `error` · `reproduc` · `±` 0 · 본문 `pressure` 0 회 · `[재현]` 50 MPa × 0.785 cm² = 3.93 kN · "3 tons" = 374.6 MPa(미터 톤 `[재현·가정]`) — (캐)(해) 표본 |
| **(g) 우리 위키와의 관계** | Yu 2024(11호)와 **같은 "시간분해 DRT 노화" 형식 · 다른 셀 · 다른 귀속 근거** — 이 편은 Yu 2024 를 [33] 으로 **P_C1 · P_C2 의 τ 대역 근거**로 인용(그러나 11호 양극 봉우리 P3 ≈500 Hz → τ ≈3×10⁻⁴ s 는 이 편 P_C1 대역 10⁻³–10⁻² s 보다 3–30 배 짧다 `[재현]`) · **Huo 2025(9호) 인용 둘 중 하나는 번호 오기로 읽힌다**(D4) | 9호 [11] 쓰임 ① "far less developed for their SSB counterparts"(서론 일반 배경 — 9호 digest 에 대조 문장 없음) ② "Hartel et al. … exceeded 3.7 V vs. In/InLi,¹¹" — Hartel = [13] · 9호 셀(NCM811(H₃BO₃) \| LPSCl \| Li₃.₇₅Si · `indium` 0 회)과 불일치 · 합성 truth 요구: 정전위 유지 노화는 **전위 · 시간 의존 계면층 R(t, V)** 와 **같은 상태 RPT(준평형)** 를 요구 — 0.1C RPT(ΔV 0.16–0.41 V)는 우리 OCV 적합 하네스의 입력이 못 된다 |
| **(h) SI** | **ESI 12 쪽 전부 봤다 — 그림 S1–S14 · 표 0 · 식 1 · 참고문헌 4 · 본문이 S1–S14 를 전부 부른다**(범위 인용 포함) | 실험 절 전부가 ESI 에만 — 압력 · 조성 · 질량 · 전류 기준 · DRT 방법 · 휴지 30 분 |
| **(i) 후속** | **원전 우선 — Hori 2023 *JPS* 556, 232450 [34](지목 누락: 11호 ★★★ · 원장 행 0 → 2)** · Zuo 2021 *Nat. Commun.* [5](재지목 → 2) · Walther 2019 [8](재지목 → 4) · Wenzel 2018 [37](재지목 → 3) · 새: Hartel 2024 [13] · Zuo 2023 [15] · Schulze 2022 [7] · Huang 2023 [30] · Lu 2022 [31] · Whang 2024 [32] | 지목 누락(★ 이상 · 원장 행 0 · 앞 호 후속 절): **[34] 하나** |
| ★★ 가장 날카로운 어긋남 | **그림 2 자료의 4.1 V calendar RPT 구간이 3.9 V 셀 RPT 의 복사다(D1) · 인쇄 Q_loss 의 기준이 지면 정의와 다르게 재현된다(D2) · 그림 6 의 "before aging" 한 스펙트럼이 여섯 셀의 공통 기준이다(D3)** | + Hartel 인용 번호 [11](D4) · 액체 Si 편 [7] 을 황화물 계면 산소 종 근거로(D5) · cycle "Pristine" ΔV 0.16 ↔ `[재현]` 0.177(D6) · 사이클 번호 78 · 76 ↔ 자료 80 · 80(D7) · 시간 축 휴지 제외(D8) · 그림 6 · S4 세로 어긋남 캡션 미표기(D9) |
| 그림 | **자동 21 = 21/21 봤다**(본문 7 · ESI 14) + 화소 판독(S4 저주파 끝 열) | ⚠ 자동 크롭 과대 둘(fS1 위 본문 한 줄 "the main text." · fS3 위 S2 캡션 끝 줄) · 캡션 필드 셋(f1 십자 표지 글리프 = 인라인 이미지 · f2 줄 끝 하이픈 · fS14 수식 글리프 뒤섞임 + "References") · 표 0 · 누락 0 |
| 보충 자료 | **ESI 1 ✅ · 데이터 ZIP 1 ✅**(본문 그림 1–7 · 세 컷오프) | SI 그림 자료 0 · 3.8 · 4.0 V 시계열 0 · 저장소 열람 0 |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | Probing solid-state battery aging: evaluating calendar *vs.* cycle aging protocols *via* time-resolved electrochemical impedance spectroscopy† |
| 저자 (5) | **Thao Kim Truong**ᵃ(ORCID 0000-0003-0145-2415 링크), Grace Whangᵃ, Jake Huangᵃ, Stephanie Elizabeth Sandovalᵃ, **Wolfgang G. Zeier**\*ᵃᵇ(ORCID 0000-0001-7749-5089 링크 · 교신 wzeier@uni-muenster.de) — 공동 1저자 표기 0 |
| 소속 | `[인쇄]` ᵃ Institute of Inorganic and Analytical Chemistry, University of Münster, 48149 Münster · ᵇ Institute of Energy Materials and Devices (IMD), IMD-4: Helmholtz-Institut Münster, Forschungszentrum Jülich, 48149 Münster |
| 서지 | *J. Mater. Chem. A* **2025**, 13, 17261–17270 · doi `10.1039/d5ta01083g` · rsc.li/materials-a · 10 쪽 · 기사 유형 띠 "REVIEW"(D10) |
| 일정 | `[인쇄]` Received 10th February 2025 · Accepted 12th May 2025 · Published on 13 May 2025 — `[재현]` 접수 → 승인 **91 일** · 승인 → 공개 1 일 · XMP publicationDate 2025-06-5(권호 — 접수 뒤 115 일) |
| 자금 | `[인쇄]` "ProRec project funded by the Bundesministerium für Bildung und Forschung (BMBF, project 03XP0537A)" |
| COI | `[인쇄]` "The authors declare no conflicts." |
| 저자 기여 | **절 없음**(본문 · ESI) |
| 자료 · 코드 | `[인쇄]` "After publication, the underlying data of this work will be available on the research data repository of the University of Münster at https://doi.org/10.17879/14908422666." · DRT 코드 = 공개 파이썬 패키지 hybrid-drt(ESI — 판 · 설정 인쇄 0) · 사용자가 보충 ZIP 을 공급(§보충 자료) |
| 자기 인용 | `[재현]` 참고문헌 37 중 교신 Zeier 가 든 항목 **8**([2] · [4] · [8] · [13] · [25] · [27] · [32] · [37]) · 공저자와 이름이 같은 Huang J.(D.) 의 DRT 방법 둘([29] · [30])과 Whang · Huang · Zeier 의 [32] — `[해석]` 공저자 Jake Huang 이 hybrid-drt 의 저자와 같은 사람으로 읽히나 지면 확인 0 · ESI 참고문헌 4 중 [1] Kraft … Zeier 2017 *JACS*(SE 합성) · [2] Zuo … Janek 2021(= 본문 [5] · 셀 하우징) · [4] = 본문 [30] |
| 라이선스 | `[인쇄]` "Licensed under CC-BY 4.0"(p. 1 띠 · 링크) · 쪽 바닥 "This journal is © The Royal Society of Chemistry 2025" — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures — 변형 없는 잘라내기 · 화소 판독은 판독용 · 커밋 안 함) · 원자료 ZIP 은 저장소에 커밋하지 않는다(구조 · sha256 · 재현에 쓴 파일 이름과 결과만) |
| sha256 | 본문 `585bba0d4fcddc6015b36d847b689efbc04204643ad6e70faec4c2fdd5aacee2`(1,560,581 B) · ESI `d0b39576974b0586b1d47c7ec1171772f95f8db94117c38e036e4a56c125971b`(5,612,169 B) · 바깥 ZIP `0f792d1164ec71c48764028e66f71263d9f99a278eb7d1937febede6415e796e`(7,671,637 B) · 안쪽 `data.zip` `ba108aba62c471311dfa5ce62b44acedbb4f90502754a47405f0f34fef559143`(7,671,479 B) — 앞 셋은 호출자 명시값과 일치 |
| 본문 PDF 메타데이터 | `%PDF-1.6` · title(본문 제목과 같음) · author "Thao Kim Truong"(제1저자만) · subject "Journal of Materials Chemistry A: Materials for energy and sustainability (2025), 13, 17261-17270, doi:10.1039/D5TA01083G" · keywords 빈칸 · creator "Aspose Ltd." · producer "Aspose.PDF for .NET 22.3.0" · 생성 2025-06-05 11:31:52 +05'30'(권호 조판일) · **수정 2026-03-19 12:22:45 +00'00'** · XMP 3,820 B(dc:creator 5 인 · dc:rights © RSC 2025 · prism doi · issn 2050-7488 · eIssn 2050-7496 · volume 13 · 17261–17270 · publicationDate 2025-06-5 · crossmark MajorVersionDate 2025-06-5 · xap CreatorTool "Arbortext Advanced Print Publisher 9.1.510/W Unicode" · XMP pdf:Producer "Acrobat Distiller 8.1.0 (Windows)"(정보 사전 producer 와 다름 — 재처리 흔적 `[해석]`) · xap 날짜 2025-06-05T11:31:52–11:32:49+05:30 · DocumentID · InstanceID) · **개요(outline) 7 항목 — 전부 제목 + "Electronic..." 로 같은 문자열**(쪽 1 · 1 · 2 · 9 · 9 · 9 · 9 — 절 이름이 깨진 개요 `[해석]`) · 링크 7(ORCID 둘 · 본문 DOI · CC BY 4.0 · 자료 DOI · NREL 둘) · 10 쪽 595.3 × 779.5 pt · 글꼴 29(AdvOT/AdvPS 계열 · LiberationSans) · 내장 이미지 8 = 그림 7(JPEG 1479×1116 · 1889×1405 · 847×1194 · 1878×1839 · 1878×1297 · 1479×1299 + 그림 3 Flate 1527×2050) + **p. 2 의 45×45 인라인 이미지 = 그림 1 캡션 "Cross mark ( ) symbols" 의 십자 글리프**(텍스트 층 빈칸) · 암호화 0 · 텍스트 층에 내려받기 띠 0 |
| ESI PDF 메타데이터 | `%PDF-1.3` · title · author · subject · keywords 빈칸 · creator "Aspose Ltd." · producer "Aspose.Pdf for .NET 9.3.0" · 생성 2025-04-03 05:22:00Z(**접수 뒤 · 승인 전 — 수정 단계**) · 수정 2025-05-13 10:24:26(시간대 없음 — 공개일) · XMP 237 B(빈) · 개요 0 · 링크 0 · 12 쪽 A4 595.2 × 841.9 pt · 글꼴 15(Arial 계열 · CambriaMath · SymbolMT — Word 원고 계열) · 내장 이미지 14(그림 S1–S14 하나씩 · Flate · 1039–3000 px 폭) · 쪽 번호 "S1"–"S12" 인쇄 · p. 1 "Supplementary Information (SI) for Journal of Materials Chemistry A. This journal is © The Royal Society of Chemistry 2025" |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | ★★★ **조건당 셀 수 · 반복 · 산포** — 컷오프 다섯 × 프로토콜 둘 = 셀 열(S4 곡선 열)로 읽힌다 · ± · 오차 막대 · 반복 0 | 신품 셀 간 저주파 Re 산포 **694–1019 Ω**(`[도표·화소]` S4)가 cycle 노화 변화(그림 6)와 같은 크기 — 산포 없이 "증가" 를 읽을 수 없다(D3) |
| **G2** | ★★★ **두 프로토콜의 정규화 축** — 명목 48 h 외에 상한 체류 · 통과 전하 · 최대 충전 깊이 · 휴지 시간을 맞추거나 적지 않았다 | (a) — 같은 "컷오프" 가 같은 상태가 아니다(calendar ≈158–169 ↔ cycle ≈92–104 mAh g⁻¹ 탈리튬 `[도표]`/`[재현·가정]`) |
| **G3** | ★★★ **대조 셀(형성 → 48 h 개회로 휴지 → RPT)** — 없다 | 형성 셋째 사이클에도 방전 용량이 사이클당 **−1.6 ~ −3.0 %** 줄고 있다(`[데이터]` 여섯 셀) — RPT 손실에서 "노화 프로토콜 몫" 과 "형성 연속 감쇠 몫" 을 못 가른다 |
| **G4** | ★★★ **DRT 봉우리 귀속의 독립 근거** — 대칭셀(In/InLi \| SE \| In/InLi · 양극 대칭) · 3전극 · 온도 의존 · 정전용량 대조 0 | (c) — P_A(음극)과 P_C(양극)을 τ 대역 문헌값으로만 가른다 · 지배 봉우리가 P_A 창으로 이동해도 이름 유지 |
| **G5** | ★★ **EIS 측정 상태의 일치** — calendar 시간분해 EIS = 유지 전위(고 SOC) · cycle = 1C 방전 끝(30 분 휴지 뒤 — 끝 상태가 사이클마다 표류) · 형성 · RPT = 0.1C 방전 끝 | 서론은 `[인쇄]` "Diagnostic measurements for cells at the same SoC are also needed for comparison after an aging period" 라고 적고, 시간분해 비교(그림 5 a ↔ b)는 다른 상태끼리다 |
| **G6** | ★★ **Q_loss 기준선의 실제 계산** — 식 (1) 은 "last formation discharge" · 본문 "last (3rd) formation cycle" · 그런데 자료로는 cycle 셀 둘이 첫 형성 기준으로 재현 | (e) · D2 — 계산 파일 · 셀별 기준값 미인쇄 |
| **G7** | ★★ **"before aging" 의 정체** — 그림 3 · 6 의 "Before aging" 곡선 · 스펙트럼이 어느 셀의 것인지 · 왜 하나인지 | 그림 6 은 한 스펙트럼(= 그림 4)을 calendar · cycle 두 판에 공유(`[데이터]` 같은 파일 내용) · 그림 3 은 두 판에 다른 곡선 둘 |
| **G8** | ★★ **음극 Li 의 접근성(원천 역할)** — Li 1.2 mg(4.63 mAh 공칭)이 SE 쪽에 닿는가 | InLi-(In) 조립(21호: 이 방향은 0.2 mA cm⁻² 탈리튬에서 0.39 µAh cm⁻² 만) — 접근 가능하면 LLI 는 용량에 안 보이고, 아니면 보인다 → Q7 판정 불가 |
| **G9** | ★★ **운전 압력의 근거** — "torque of 10 Nm providing … ~50 MPa" 의 환산(볼트 수 · 지름 · 마찰) · 계측 · 사이클 중 변화 | (캐)(해) — 본문에는 압력 낱말이 0 회 |
| **G10** | ★ **DRT 설정** — hybrid-drt 판 · 사전 · 초모수 · 기저 함수 · 비음 제약 · 적합 잔차 · R_∞ · L 처리 | 봉우리 크기 · 개수 · 창 밖 몫(26 %)의 재현 조건 |
| **G11** | ★ **NCM83 입도 · 표면 코팅 · BET** — "supplied by MSE" 만 | C_eff 를 CAM 표면적으로 나눠 이중층 상한 검사를 할 수 없다(기하 면적까지만) |
| **G12** | ★ **4.0 · 4.1 V 사후 방전의 "kink" 기구** — "may originate from lithiation processes of decomposition products" 한 문장 | `[데이터]` 4.1 V: 4.1 → 2.86 V 로 떨어진 뒤 3.01 V 까지 오른다 · S12e 는 다른 모양(D17) |
| **G13** | ★ **1C 구간 사이클 수 · 끝 처리** — "approximately 48 h (actual durations varied slightly …)" | 그림 5 · 7 은 78 · 76 · 74 사이클 · 그림 2 자료는 80 · 80 · 74 사이클(D7) |
| **G14** | ★ **사후 분석** — XPS · SEM · ToF-SIMS · 단면 0 | 계면층 · 접촉 손실 · 균열 서술은 전부 인용 · 가능성 문장 |

# 보충 자료 — 받은 것 · 대조

- **ESI PDF 12 쪽** — 실험 절(pp. 2–4) + 그림 S1–S14(pp. 4–12) + 참고문헌 4. **표 0.** 본문 각주 † 의 목록 `[인쇄]` "Li6PS5Cl synthesis, cathode composite preparation, cell assembly procedure, Nyquist and Bode plots during aging steps, galvanostatic charge–discharge data during accelerated calendar aging periods" — ESI 와 맞다(DRT 방법 · 노화 절차 · 유지 전류(S11) · Q_re/Q_irr(S14)는 각주 목록 밖이나 ESI 에 있다).
- **본문이 부르는 SI 그림**(본문 텍스트 층 `Fig. S` 7 회 · 캡션 포함): S1(그림 2 캡션) · "Fig. S1–S4 and S5"(형성 · RPT — p. 3) · S2(그림 3 캡션) · "S6–S9"(그림 5 캡션) · S10(그림 6 캡션) · S11(p. 8) · "S12–S14"(그림 7 캡션) ⇒ **S1–S14 전부 불린다**(범위 인용 포함). ESI 안에서는 "Figure 1 of the main text" 한 번.
- **데이터 ZIP**(사용자 공급 · 업로드 이름 "1._Sup1_…zip"):

| 층 | 내용 |
|---|---|
| 바깥 ZIP | 7,671,637 B · 항목 1 = `data.zip`(무압축 저장 · 7,671,479 B · 항목 시각 2026-10-02 13:38:44 — 사용자 쪽 재포장 `[해석]`) · 주석 0 |
| 안쪽 `data.zip` | **1,273 항목 = 폴더 47 + 파일 1,226** · deflate · 항목 시각 전부 **2025-06-02**(공개 뒤 · 권호 조판 전) · 풀린 크기 합 18,522,059 B · 탭 구분 txt |
| 그림 1 | `Calendar aging/s0–s2.txt` · `Cycle aging/s0–s2.txt`(시간/h · Ewe/V — s0 형성 · s1 노화 · s2 RPT) — **3.9 V 두 셀**(그림 2 의 3.9 V 파일과 시각 · 전위가 같다 `[데이터]`) — 캡션에 컷오프 표기 0 |
| 그림 2 | 3.7 · 3.9 · 4.1 V × calendar · cycle **6 파일**(47,933–64,454 행 · ≈10 s 간격) |
| 그림 3 | a · b 전위–용량(before + 세 컷오프 × 충 · 방 = 8 씩) · c · d dQ/dV(8 씩) · e · f "Voltage gap - Q loss" 표 **2**(다섯 컷오프 + Pristine — 3.8 · 4.0 V 값이 있는 유일한 자리) |
| 그림 4 | Nyquist(주파수 · Re · −Im · cycle number 3.0 · 164 점) · fit(164 점) · DRT(τ · γ/Ω · 284 점) |
| 그림 5 | calendar 3 × 48 시간별 DRT(`cycle_01`–`cycle_48`) + cycle 40 · 39 · 38 DRT(`cycle_01`, `02`, `04`, … — 첫 사이클 뒤 · 이후 두 사이클마다) = **261** |
| 그림 6 | Nyquist · DRT × (before + 세 컷오프) × 두 판 = **16** — **"before aging" 은 두 판 · 그림 4 와 같은 내용**(`[데이터]`) |
| 그림 7 | 1C 충 · 방 곡선 + dQ/dV × 세 컷오프 = **900**(3.7 V `c01`–`c74` + `c78` · 75–77 없음 · 3.9 V 1–76 · 4.1 V 1–74) |
| 없는 것 | **SI 그림 S1–S14 자료 0** · **3.8 · 4.0 V 시계열 0**(그림 3e · f 표 두 줄 제외) · 그림 S4 신품 열 스펙트럼 0 · 정전위 유지 전류 · 용량(S11) 0 · 전류 열 0(모든 시계열이 시간 · 전위만) |
| 저장소 대조 | 본문 "Data availability" 의 DOI 10.17879/14908422666 은 **열람하지 않았다** — ZIP 의 폴더 이름이 본문 그림 번호와 1 : 1 이고 SI 그림 폴더가 없다는 것까지가 대조다(같은 예치본인지 미확정) |

# 그림 — 자동 21 항목, 실제로 연 것 **21/21** (+ 화소 판독: 그림 S4 저주파 끝 · 판독용 · 커밋 안 함)

`raw/figures/truong2025_calendar-vs-cycle-aging-protocols-drt-assb/` · `figures.json` 에 항목별 note.

- 추출: 본문 · ESI 원 파일명 그대로 `--pdf` 두 개 · `SI_TAG` 판별을 먼저 확인(본문 False · `…_Sup2_…` True — 호출자 확인과 같음) · 결과를 눈으로 확인: 본문 `fig_1 … fig_7` · ESI `fig_S1 … fig_S14` · 표 0 · 누락 0.
- **자동 크롭 문제**: **fS1 위쪽에 ESI 본문 한 줄 "the main text."** · **fS3 위쪽에 그림 S2 캡션 끝 줄 "accelerated calendar and cycle aging cells, respectively."** — 둘 다 과대 영역(그림 내용 손실 0). 나머지 19 개 크롭 온전.
- **캡션 필드 문제**: f1 — "Cross mark ( ) symbols" 의 십자는 PDF 안 45×45 인라인 이미지라 텍스트 층이 빈칸(크롭 온전) · f2 — "cut- oﬀs"(줄 끝 하이픈 잔재) · **fS14 — 수식 글리프(𝑄, 위 · 아래 첨자)가 뒤섞여 문장이 깨지고 끝에 ESI 참고문헌 머리 "References" 가 붙음.** 900 자 잘림 0.

## Fig. 1 — 프로토콜 예시(p. 2 · 봤다) ★★★ (a)

위 "Calendar aging": Formation 0.1C(셋) → **회색 "Potentiostatic hold 48 h"**(≈43 → ≈104 h `[도표]` — CC 충전 · 48 h 유지 · CC 방전을 모두 회색 칸에 넣음) → RPT 0.1C(셋) · 오른쪽 확대(52–54 h): 3.9 V 수평선 위 EIS 표지(×) 매 시간. 아래 "Cycle aging": Formation → **회색 "1C cycling 48 h"**(≈40.5 → ≈91 h) → RPT · 확대(52–53.8 h): 2.0 ↔ 3.9 V 톱니, 충전 시작 ≈3.4 V(2.0 V 에서 바로 도약) · 상단 3.9 → ≈3.2 V 도약 · EIS 표지는 **방전 끝 두 번에 한 번**. EIS 표지 아래 · 위 모두 2.0 V(방전 끝). 컷오프 표기는 그림 안 "3.9" 뿐 — `[데이터]` 그림 1 자료 = 그림 2 의 3.9 V 두 셀(시각 · 전위 동일). ⚠ 시간 축에 30 분 휴지 · EIS 가 없다(D8 — 확대 판에서도 휴지 간격 0).

## Fig. 2 — 전위–시간 세 컷오프(p. 3 · 봤다) ★★★ (a) · D1

(a) calendar 4.1 · 3.9 · 3.7 V — 유지 구간 `[데이터]` 48.27–96.27 · 49.62–97.62 · 48.93–96.94 h(각 **48.00 h**) · 4.1 V 유지 뒤 방전 첫머리 **≈2.86 V 로 떨어졌다가 ≈3.01 V 까지 오르는 굽음**(본문 "kink" — 4.0 V 도 S1 에 같은 꼴) · 사후 RPT 세 사이클이 짧아짐. (b) cycle — 1C 띠 ≈40.4–91.2 h · 띠 아랫선이 사이클을 따라 오른다(충전 시작 도약점의 표류 `[해석]`) · 사후 RPT 는 형성과 비슷. ⚠⚠ **(a) 4.1 V 판의 RPT 세 사이클(≈103.5–128.9 h)은 자료상 3.9 V 셀 RPT 의 시간 이동 복사(D1)** — 그림에서도 두 판의 RPT 충 · 방 길이가 같다(≈4.0 · 4.2 · 4.2 · 4.3 · 4.3 · 4.4 h `[데이터]`). 3.7 V calendar 판 ≈114 h 의 홈 = 자료 0.48 h 공백(113.80 → 114.28 h · 2.0035 → 2.040 V — D18).

## Fig. 3 — 마지막 형성 ↔ 마지막 RPT(p. 4 · 봤다) ★★★ (d) · (e)

(a) calendar — "Before aging"(점선 하나) 충전 끝 ≈131 · 3.7 V ≈114 · 3.9 V ≈88 · 4.1 V ≈74 mAh g⁻¹ `[도표]`(`[데이터]` 130.75 · 113.63 · 87.99 · 73.80) · 방전 곡선이 0 근처 또는 약간 음수에서 끝남(Q_dis > Q_ch — `[데이터]` CE 100.05 · 101.22 · 101.78 %). (b) cycle — before ≈130 · 3.7 V ≈128 · 3.9 · 4.1 V ≈117–118 `[도표]`. (c) calendar dQ/dV — 충전 봉우리 ≈377 → 305 → 215 → 184 · 방전 ≈−298 → −266 → −194 → −142 mAh g⁻¹ V⁻¹(`[데이터]` §재현) · 봉우리 사이 간격 ↑. (d) cycle — 작은 변화 · 3.08 V 충전 시작 가시(4.1 V 빨강이 축 위로 — `[데이터]` 767 — 첫 단계 인공물). (e) calendar ΔV 0.16 → 0.21 · 0.28 · 0.33 · 0.40 · 0.41 V · Q_loss 13 · 23 · 33 · 35 · 44 % `[도표]`(`[데이터]` 표 = §재현). (f) cycle ΔV 0.16 → 0.19 · 0.22 · 0.23 · 0.17 · 0.22 · Q_loss 1.4 · 5.6 · 9.8 · 6.5 · 9.3 %. ⚠ "Pristine" 점은 두 판 모두 0.16 하나(D6) · "Before aging" 곡선은 두 판에 서로 다른 곡선 하나씩(G7).

## Fig. 4 — 전형 Nyquist + DRT(p. 5 · 봤다) ★★★ (c)

(a) Re 0–800 Ω · 자료 25 → ≈720 Ω · 원호 꼭대기 ≈125 Ω @Re ≈380 · 저주파 꼬리 ≈100–110 · "Fit"(빨강)이 자료 위. (b) γ(Ω) — P_SE ≈2×10⁻⁸ s(≈17 Ω) · 점선 ≈2.3×10⁻⁸ · ≈3.2 s(측정 창 경계 — `[재현]` 1/(2π·7 MHz) = 2.27×10⁻⁸ · 1/(2π·50 mHz) = 3.18 s) · P_C 괄호 아래 P_C1 ≈10⁻² s(≈92 Ω) · P_C2 어깨 ≈4×10⁻² · P_A ≈0.4 s(≈63 Ω) · **P_D ≈10 s(≈118 Ω) — 창 밖**. 어느 셀 · 상태인지 캡션 0 — `[데이터]` 그림 6 "before aging" 과 같은 파일 내용(Re(50 mHz) 719.5 Ω — S4 의 calendar 3.7 V 셀 ≈709 Ω 과 가깝다 `[도표·화소]`).

## Fig. 5 — 시간분해 DRT + 2D 면(p. 6 · 봤다) ★★★ (c) · D14

(a) calendar — 3.7 V: γ 축 Ω(0–700) · P_SE · P_C(괄호) · P_A · P_D 표지 · 2D 색 막대 543 · 흰 점선(초기 P_C) ≈10⁻³ s → 검은 점선 ≈5×10⁻³ s · "P_C shift" 화살 · P_D(≈10 s)도 자란다. 3.9 V: **γ 축 kΩ(0–≈28)** · 지배 봉우리 ≈0.1–0.2 s · 삽도(P_SE · 단위 표기 0 — 0–50) · 4.1 V: **γ 축 kΩ(0–≈350)** · 날카로운 봉우리 ≈0.3–0.5 s · 2D 에서 봉우리가 시간에 따라 오른쪽으로 휘어 감. (b) cycle — 3.7 V(색 1–78): P_C1(≈5×10⁻⁴ s) 34 → 19 Ω ↓ · **P_A ≈0.05 → 0.3 s 로 이동하며 6 → 65 Ω ↑** · P_D · 3.9 V(1–76) · 4.1 V(1–74): P_C1 이 가장 크고(73 · 135 Ω 최댓값) 사이클을 따라 줄며 P_A 는 초기 몇 사이클에 자라 멈춤. `[데이터]` 색 막대 최댓값 여섯 모두 자료 최댓값과 일치(§재현). ⚠ 3.9 · 4.1 V 유지 48 h 의 지배 봉우리 τ 0.19 · 0.54 s 는 본문이 P_A 에 준 창(10⁻¹–1 s) 안 — 이름은 2D 연속성으로 유지(D14).

## Fig. 6 — 마지막 형성 ↔ 마지막 RPT 의 Nyquist · DRT(p. 7 · 봤다) ★★★ (c) · D3 · D9

(a) calendar Nyquist(kΩ) — 곡선 넷이 **세로로 어긋나 쌓여 있다**(시작 −Im ≈0 · 0.18 · 0.35 · 0.52 kΩ `[도표]` — 캡션에 쌓기 표기 0, D9) · 끝 Re ≈0.72 · 0.85 · 1.15 · 1.52 kΩ. (b) cycle — 끝 Re ≈0.72 · 0.78 · 0.99 · 0.95 kΩ. (c) calendar DRT — P_C 93(before) → 137 · 175 · 313 Ω · 4.1 V 에 P_A 어깨(≈110 Ω @0.3 s) · P_D ≈120–130 거의 불변. (d) cycle DRT — P_C 93 → 100 · 121 · 125 · **P_A 63 → 100 · 155 · 140** · P_D 118 → 143 · 169 · 145 Ω `[도표]`. ⚠ "Before aging" 은 (a)–(d) 모두 **같은 스펙트럼 하나**(`[데이터]` 두 판 파일 내용 동일 · = 그림 4) — 셀마다 자기 형성 스펙트럼이 아니다(D3).

## Fig. 7 — 1C 충 · 방전과 dQ/dV(p. 8 · 봤다) ★★ (a) · (c)

(a) 3.7 V(1–78): 충전 ≈53–68 · 방전 ≈47 → ≈63 mAh g⁻¹(사이클을 따라 ↑) · 3.9 V(1–76): 방전 ≈47 → ≈68 · 4.1 V(1–74): 첫 충전 ≈87 · 방전 ≈62 → ≈72 `[도표]`(`[데이터]` §재현). 충전 곡선 시작 ≈3.3–3.45 V · 방전 시작 ≈3.2 V — 1C 분극 큼. (b) dQ/dV — 충전 쪽 ≈3.3–3.45 V 의 날카로운 첫머리(시작 인공물 `[해석]`) · 방전 봉우리 ≈−100–130 · 사이클 따라 커짐.

## ESI 그림 S1–S14 (전부 봤다)

| 그림 | 본 것 | 우리 축 |
|---|---|---|
| **S1** (p. 4) | 다섯 컷오프 × 두 프로토콜 전위–시간 · 4.0 V calendar 도 유지 뒤 굽음(≈2.95 V) · ⚠ 크롭 위 본문 한 줄 | 3.8 · 4.0 V 의 유일한 시계열(자료 0) |
| **S2** (p. 5) | 다섯 컷오프 마지막 형성 ↔ RPT — calendar 충전 끝 ≈131(before) · 113 · 101 · 88.5 · 85 · 74 · cycle ≈130 · 128 · 122 · 117.5 · 120 · 117.5 `[도표]` · dQ/dV 점선 기준선 ≈3.16(충) · 3.10 V(방) · 축 이름 **"V vs. In/LiIn"**(본문 In/InLi — D11) · 색 배정이 본문 그림 3 과 다름(4.1 V 초록) | 3.8 · 4.0 V Q_loss · ΔV 는 표 e · f 의 값과 정합(그림 판독) |
| **S3** (p. 5) | (a) 형성 세 사이클: 첫 충전 ≈197 · 첫 방전 ≈138(첫 CE ≈70 % `[도표]`) · 2 · 3 번째 ≈136/134 · ≈131/131 · (b) 형성 전 Nyquist −Im ≈6 kΩ(차단형) → 형성 뒤 ≈0.7 kΩ 원호(삽도 0–700 Ω) · ⚠ 크롭 위 S2 캡션 끝 줄 | Q7 · (도) — 첫 사이클 결손 ≈59 mAh g⁻¹ 의 정체 미논의 |
| **S4** (p. 6) | **형성 뒤 신품 Nyquist 열(calendar 다섯 · cycle 다섯)** · 세로 쌓기(≈110 Ω 간격 · 캡션 표기 0) · `[도표·화소]` 저주파 끝 Re: calendar 3.7 **≈709** · 3.8 ≈694 · 3.9 ≈828 · 4.0 ≈823 · 4.1 ≈793 · cycle 3.7 **≈816** · 3.8 ≈913 · 3.9 **≈1019** · 4.0 ≈847 · 4.1 **≈958 Ω**(±≈10) | ★★★ 셀 간 산포 694–1019 Ω — 그림 6 의 공통 기준(719.5)과 대조(D3) |
| **S5** (p. 6) | RPT 세 사이클 — calendar: 1 → 3 번째로 용량이 **오른다**(3.9 V ≈78 → 84 → 88 · 4.1 V ≈66 → 71 → 74 `[도표]`) · cycle: 1 번째 점선이 ≈−28 mAh g⁻¹ 에서 시작(1C 끝 미반환 Li 를 0.1C 로 더 방전한 몫 `[해석]` — `[데이터]` RPT1 방전 − 충전 = +29.3 · +27.6 · +31.8 mAh g⁻¹) | 회복 · 기준 사이클 선택(D2 · (네)) |
| **S6** (p. 7) | 다섯 컷오프 시간분해 DRT · 2D — calendar 최댓값 543 Ω · **3 kΩ** · 28 · **88** · 347 kΩ · cycle 65 · 56 · 74 · **83** · 135 Ω · 사이클 수 78 · 76 · 76 · **68** · 74 · 3.8 V calendar 는 P_C · P_D 함께 자람 | 3.8 · 4.0 V 의 유일한 DRT |
| **S7** (p. 7) | Nyquist 시간분해(쌓기 — 캡션 표기 ✅) · calendar 4.1 V 48 h 끝 Re ≈225 kΩ · cycle 원호 ≈300–430 Ω | 1C 방전 끝 스펙트럼(≈0.2–0.4 kΩ)이 RPT 방전 끝(≈0.7–1.0 kΩ)보다 작다 — 다른 상태(G5) |
| **S8** (p. 8) | Bode \|Z\| — calendar 50 mHz 끝 ≈2.45 · 9.7 · 68 · 118 · 230 kΩ(48 h) · cycle ≈220–430 Ω | — |
| **S9** (p. 9) | Bode 위상 — calendar 최대 −θ ≈40 → 76° · cycle ≈15–30° · ⚠ **4.0 V cycle 색 막대 70**(S6 · S8 · S13 은 68 — D7) | — |
| **S10** (p. 10) | 다섯 컷오프 그림 6 판 — calendar P_C **4.0 V ≈333 > 4.1 V ≈313 · 3.8 V ≈189 > 3.9 V ≈175 Ω** `[도표]`(비단조) · Nyquist 끝 Re 3.8 ≈1.15 · 3.9 ≈1.13 · 4.0 ≈1.62 · 4.1 ≈1.53 kΩ | 본문 "increases gradually with increasing cut-off" 는 세 컷오프 선택에서만 단조(D19) |
| **S11** (p. 10) | (a) Q_hold 48 h ≈28.5–29.5 mAh g⁻¹ — **컷오프와 거의 무관** · (b) I_hold ≈20 → ≈0.12–0.15 mA g⁻¹(4.1 V 가 가장 높음) `[도표]` | 유지 용량이 손실과 짝이 아니다(본문도 인정) |
| **S12** (p. 11) | 유지 사이클(CC 충전 · 유지 · CC 방전) — 충전 끝 ≈129 · 135 · 136 · 142 · 139 → 유지 끝 ≈158 · 164 · 166 · 171 · 169 · 방전 ≈144 · 147 · 135 · 141 · 131 mAh g⁻¹ `[도표]` · 4.0 · 4.1 V 방전 첫머리 굽음(≈2.95 · ≈2.6 → 2.87 V) | ⚠ 3.7 · 4.1 V 는 그림 2 자료(138.5 · 144.5 mAh g⁻¹ @20 mA g⁻¹)와 다르다(D17) |
| **S13** (p. 11) | 다섯 컷오프 1C 곡선 · dQ/dV — 4.0 V 첫 충전 ≈100 · 방전 ≈68 → ≈80 · 4.1 V 첫 충전 ≈87 | — |
| **S14** (p. 12) | (a) 유지 사이클 모식(Q_charge · Q_hold · Q_discharge) · (b) `[인쇄 — 그림 안]` Q_re^tot / Q_irr^tot = **91/9 · 90/10 · 81/19 · 82/18 · 78/22 %**(3.7–4.1 V) · 정의 Q_re^tot = Q_discharge · Q_irr^tot = Q_charge + Q_hold − Q_re^tot | `[재현]` S12 판독으로 91.1 · 89.6 · 81.3 · 82.5 · 77.5 % ✅ · ⚠ 캡션 필드 깨짐 |

## 본문 서술과 어긋난 그림 (요약)

- 그림 2a 4.1 V — RPT 구간이 3.9 V 셀의 복사(자료) — "increasing cut-off potentials resulted in decreasing post-aging cycle times" 를 3.9 ↔ 4.1 V 사이에서 이 그림으로 읽을 수 없다(D1).
- 그림 6 — "before aging" 한 스펙트럼을 여섯 셀 공통 기준으로(자료) · S4 의 셀 간 산포가 cycle 변화와 같은 크기(D3) · 세로 쌓기 미표기(D9).
- 그림 5a 3.9 · 4.1 V — "P_C" 가 P_A 창(0.1–1 s)으로 이동(D14).
- 그림 3f · e — "Pristine" ΔV 0.16 하나(cycle before 곡선은 `[재현]` 0.177 — D6).
- S10c — calendar P_C 가 컷오프에 비단조(4.0 > 4.1 · 3.8 > 3.9 V) ↔ 본문 "increases gradually with increasing cut-off potential"(그림 6 은 세 컷오프만 — D19).
- S9 — 4.0 V cycle 색 막대 70 ↔ S6 · S8 · S13 의 68(D7).
- S12 · S14 — 3.7 · 4.1 V 유지 사이클 방전이 그림 2 자료와 다르다(D17).

# 절별 해체 (본문)

## 초록 (p. 1)

- 문제 `[인쇄]`: "Aging protocols which can quickly identify and monitor degradation of cells can help expedite solid-state battery development by predicting the possible long-term aging trend of cells in a time efficient manner."
- 결과 `[인쇄]`: "Cells with various cut-off potentials were investigated using the two aging protocols showing significantly greater performance deterioration under calendar aging relative to cycle aging. Applying distribution of relaxation times analyses …, the cathode–electrolyte interfacial resistance evolution is found to be the dominant degradation mechanism during calendar aging while changes at the anode–electrolyte interface are influential during cycle aging tests."
- 일반화 `[인쇄]`: "The aging protocol and analyses applied in this work can potentially be further extended to other systems … and quickly screen cells for optimization."

## 서론 (pp. 1–2)

- 노화 분류 `[인쇄]`: calendar = "Under long-term storage, cells undergo continuous degradation that reduces usable capacity"[7] · cycle = "performance deterioration stemming from repeated cycling"[10] — **정의는 개회로 보관인데, 이 편의 calendar 는 정전위 유지다**(본문이 곧바로 "potentiostatic hold (also known as float test or voltage hold) protocol[3,6] was employed as a qualitative accelerated tool for calendar aging tests" 로 바꿔 부른다).
- SSB 노화 연구의 자리 `[인쇄]`: "While cell aging studies have been well established for LIBs, they are far less developed for their SSB counterparts.[11]"(← 9호) · 기존 SSB calendar 연구 `[인쇄]` "only a few studies … using calendar aging protocols,[5,13–15] which used rest periods at OCV or held a specific potential for 20–30 hours with electrochemical impedance spectra (EIS) measured periodically. However, short-term OCV and voltage hold phases may provide limited information on cell degradation due to significant reversible lithiation/delithiation relaxation.[7] Diagnostic measurements for cells at the same SoC are also needed for comparison after an aging period."
- 설계 `[인쇄]`: "The aging period, which was conducted in between the formation and reference performance test (RPT) steps, was fixed at 48 hours, while the upper cut-off potential is varied." · 1C 사이클은 "a high C-rate (1C) cycling approach[19]".
- 셀 선택의 근거 `[인쇄]`: "In/InLi|Li6PS5Cl|NCM:Li6PS5Cl, which has been thoroughly studied with known degradation mechanisms,[8,15,18] was employed as a well-characterized system".

## 결과 1 — 전위–시간 · 용량 · dQ/dV · ΔV(pp. 2–5 · 그림 1–3 · S1–S5)

- 컷오프 `[인쇄]`: "3.7 V, 3.8 V, 3.9 V, 4.0 V, and 4.1 V vs. In/InLi, which correspond to 4.32 V, 4.42 V, 4.52 V, 4.62, and 4.72 V vs. Li+/Li, respectively. These high potentials were selected because typical degradation of sulfide solid electrolytes (SEs) against NCM is triggered when CAM potential exceeds 3.58–3.7 V vs. In/InLi.[5,13,15]" — 본문에는 3.7 · 3.9 · 4.1 V 만("for brevity and visual clarity"), 나머지는 ESI.
- 그림 2 관측 `[인쇄]`: "(1) a significant decrease in post-aging cycle time was observed across all cells whereby increasing cut-off potentials resulted in decreasing post-aging cycle times. (2) For calendar aged cells with a 4.1 V potentiostatic hold cycle, … a kink is observed … This may originate from lithiation processes of decomposition products".
- 비교 기준 `[인쇄]`: "the last (3rd) formation cycle in this study was chosen to represent the nominal pristine cell conditions, while the final (3rd) RPT cycle was chosen to represent cell conditions after accelerated aging. This should mitigate most effects of potential residual reactions after the aging period."
- 용량 초과 `[인쇄]`: "The slight excess discharge capacity (Qdischarge > Qcharge) in the last RPT cycles … is likely due to continuous side reactions or residual reversible capacity gained from potentiostatic hold."
- dQ/dV 해석 `[인쇄]`: "calendar aged cells, which show a significant decrease in dQ/dV peak intensity post-aging. This suggests the loss of lithium inventory in the CAM[23] due to parasitic processes during the voltage hold. Additionally, the increase in peak-to-peak separation … suggests that exposure of the cell to higher voltages not only further expedite degradation but also lead to increased polarization."
- ΔV · Q_loss `[인쇄]`: "ΔV was calculated at 50% SoC" · 식 (1) "Q_loss = 1 − Q_last RPT discharge / Q_last formation discharge" · "both calendar and cycle aged cells exhibit a correlation between ΔV and capacity loss. … Cycle aged cells show a similar, but much less severe, trend up to 3.9 V, but degradation appears to plateau at higher voltages."

## 결과 2 — DRT(pp. 5–7 · 그림 4–6 · S6–S10)

- 왜 DRT `[인쇄]`: "the deconvolution of physical processes from Nyquist plots via equivalent circuit models can be highly ambiguous due to overlapping response frequency ranges.[28] Therefore, the fitting of impedance data was implemented using DRT analysis, which does not require an a priori established model".
- 봉우리 배정 `[인쇄]`: "The DRT in this work generally indicates five main peaks, … PSE, PC1, PC2, PA, and PD" · P_SE(τ ∼10⁻⁸ s) "bulk resistance of the SE"[31,32] · "Two overlapping peaks PC1 (τ ∼10⁻³ to 10⁻²) and PC2 (τ ∼10⁻² to 10⁻¹ s) can be ascribed to Li-ion transport through the cathode–electrolyte interface (RC1) and interfacial charge transfer resistance (RC2) within the cathode composite, respectively.[31,33]" · "PA (τ ∼10⁻¹ to 1 s) can be attributed to the charge-transfer resistance at the anode–electrolyte interface (RA).[31,34]" · P_D(τ ∼10 s) "solid-state lithium diffusion process within the cathode electrode.[34]" · 경고 `[인쇄]` "the relaxation of PSE and PD occurs largely out of the measured frequency range" · "Since PC1 and PC2 overlap strongly in almost all experiments, we refer to their combination simply as the PC region."
- 원인 서술 `[인쇄]`: 양극 계면 저항 증가는 계면층 형성[5,25] + "it was reported that the increased cathode–electrolyte interfacial resistance may also be contributed by the contact loss between them.[27]"(← 23호) · cycle 의 P_A 성장 "could be attributed to the non-uniform local current density distribution at the interface with the In/InLi alloy electrode at high current density, which may lead to inhomogeneous lithiation/delithiation processes[32] and induce chemo-mechanical degradation such as contact loss or void formation at the anode–electrolyte interface.[35,36]"
- 2D DRT `[인쇄]`: "PC tends to shift to longer time constants as the potentiostatic hold time increases. This may be caused by an increase in the RC2/RC1 ratio, or a simple increase of RC1 while the corresponding capacitance value of PC1 remains almost constant." · "During cycle aging (Fig. 5b), only PA shifts to longer timescales at the beginning of the aging period."
- 형성 ↔ RPT EIS `[인쇄]`: calendar "a noticeable domination of PC that increases gradually with increasing cut-off potential, while PA has a smaller contribution" · 해석 "post-aging capacity fading in calendar aged cells … may be caused by irreversible loss of cyclable lithium into building up resistive cathode–electrolyte interphase layer … may also cause chemomechanical degradation of the composite cathode such as cracking or contact loss due to volume expansion from overcharging." · cycle "only show a slight increase in the overall post-aging impedance. Again, a larger contribution from PA is observed".

## 결과 3 — 유지 용량 · 1C 곡선 · 권고(pp. 7–9 · 그림 7 · S11–S14)

- 유지 용량의 한계 `[인쇄]`: "At the beginning of the potentiostatic hold regime, the measured capacity can be dominated by residual reversible processes due to depolarization effect … Schulze et al. reported that the potentiostatic hold method is incapable of quantitatively forecasting the actual rate of capacity fade, but can be applied as a qualitative method for fast screening[7]" · "the contribution of irreversible capacity loss due to parasitic reactions remains ambiguous and is yet to be quantitatively deconvoluted. Thus, an attempt to fit and extrapolate potentiostatic hold data using classical time dependency models employed in literature[5,37] may yield inaccurate results."
- cycle 의 한계 `[인쇄]`: "the employed cycle aging protocol does not fully capture the expected cell aging behavior driven by interfacial degradation. In 48 hours of aging, the reduced time spent at unfavorable upper cut-off potentials during high C-rate cycling likely explains its less detrimental impact compared to potentiostatic holds." · 1C 저용량 "may be primarily attributed to kinetic limitations" · "The slight increase in capacity and dQ/dV peak intensity during cycle aging may be explained by the decline of RC1 over time (Fig. 5b)."
- 검증 주장 `[인쇄]`: "Long-term cycling data from comparable SSB cell systems have shown that cathode–electrolyte interfacial resistance evolution is one of the main factors contributing to capacity fading.[13,15] This is in good agreement with the results of accelerated calendar aging tests in this work, suggesting the feasibility of this method for fast cell screening." — **이 편 안의 장기 사이클 대조 0**(인용 대조).

## 결론 (p. 9)

`[인쇄]` "cathode–electrolyte interfacial resistance evolution is found to be the dominant degradation mechanism during the calendar aging tests, while increasing charge-transfer resistance at the anode–electrolyte interface is an influencing factor during cycle aging tests. … the employed potentiostatic hold protocol, which is recommended over the high C-rate cycling approach to qualitatively inspect and screen promising new solid-state cell chemistries in a fraction of time."

## ESI 실험 절 (pp. 2–4)

- SE `[인쇄]`: Li₆PS₅Cl 고상법(Li₂S · P₂S₅ · LiCl 손 분쇄 → 펠릿 → 탄소 코팅 석영 앰플(내경 12 mm) 진공 밀봉 → **550 °C 2 주**)[ESI 1].
- 복합 양극 `[인쇄]`: NCM83(LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂ · "supplied by MSE") : Li₆PS₅Cl = **7 : 3 wt** · "egg shape" 진동 볼밀(FRITSCH P-23) 20 Hz 15 min · ZrO₂ 볼(∅3 mm) 10 개 / 100 mg — **탄소 0**.
- 셀 `[인쇄]`: 기밀 프레스 셀 · 스테인리스 집전체 ∅1 cm[ESI 2] · SE 70 mg(분리막 · 손 압착) · 양극 복합 10 mg("corresponding to an areal capacity of 1.783 mAh cm⁻² based on NCM83 theoretical specific capacity of 200 mAh g⁻¹") · "a uniaxial pressure of 3 tons was applied for 3 min" · In/InLi 51.2 mg("≈28.42 at% Li" — In 박 50 mg(∅9 mm · chemPUR 99.999 %) + Li 1.2 mg(abcr 99.8 %, 얇게 눌러 박)) · "the In foil was in contact with the solid electrolyte while the Li foil was in contact with the current collector" · "fixed in an aluminum frame, with a torque of 10 Nm providing an operating stack pressure of ~50 MPa" · 25 °C 6 h 평형.
- 전기화학 `[인쇄]`: 25 °C Binder 항온조 · BioLogic VMP-300 · "The theoretical specific capacity of NCM83 used in this work was assumed to be 200 mAh g⁻¹ as basis of calculation for charge and discharge current" · PEIS 10 mV rms "superimposed to the open-circuit voltage (OCV)" · 7 MHz–50 mHz.
- DRT `[인쇄]`: "we apply the self-tuning DRT inversion algorithm implemented in the python package hybrid-drt by Huang et al.[4] This uses a hierarchical Bayesian model to obtain the maximum a posteriori estimates of the DRT without manual parameter tuning" · "the impedance over the entire measured frequency range (7 MHz–50 mHz Hz) was found to obey the Kramers-Kronig relations, no frequencies were truncated" · "The τ basis range used for the DRT was extended by 1 decade beyond the measured frequency bounds".
- 노화 절차 `[인쇄]`: 형성 · RPT "three times at 0.1C rate between 2.0 and 3.7 V vs In/InLi" · calendar "charged up to a cut-off with a constant current (CC) mode at 0.1C, followed by a constant voltage mode for 48 h before being discharged by another CC mode at 0.1C" · cycle "charge-discharge cycles at 1C rate were conducted for approximately 48 h (actual durations varied slightly due to variations in cycle duration)" · 하한 2 V · EIS "every one hour during the potentiostatic hold, and at the end of discharge every two cycles during 1C cycling" · 형성 · RPT "at the end of discharge of every cycle" · "before impedance measurement for formation, RPT, and 1C cycling periods, cells were rested at OCV for 30 minutes to ensure a pseudo-steady state."

# ★ (a) "calendar aging" 의 실체 — 그리고 두 프로토콜을 무엇으로 맞췄나

## 1. 조건 표 (`[인쇄]` ESI · 본문 — 괄호 안 `[재현]` · `[데이터]`)

| 항목 | calendar ("potentiostatic hold" = float) | cycle ("high C-rate (1C) cycling") | 공통 |
|---|---|---|---|
| 앞 단계 | — | — | 형성 0.1C × 3 · 2.0–3.7 V vs In/InLi · 방전 끝 EIS(30 분 OCV 휴지 뒤) |
| 노화 단계 | 0.1C CC 충전 → 컷오프 → **CV 48 h** → 0.1C CC 방전(2.0 V) | **1C CC 충 · 방**(2.0 V ↔ 컷오프) "for approximately 48 h" · CV 0 | 컷오프 3.7 · 3.8 · 3.9 · 4.0 · 4.1 V vs In/InLi |
| 노화 중 EIS | **매 시간 · 유지 전위에서**(48 회) | **두 사이클마다 · 방전 끝 · 30 분 OCV 휴지 뒤**(`[데이터]` 40 · 39 · 38 회) | 10 mV rms · 7 MHz–50 mHz |
| 뒤 단계 | — | — | RPT 0.1C × 3 · 2.0–3.7 V · 방전 끝 EIS · 비교는 **형성 3번째 ↔ RPT 3번째** |
| 온도 | 25 °C | 25 °C | Binder 항온조 · 조립 뒤 25 °C 6 h |
| 전류 기준 | 0.1C = 20 mA g⁻¹(NCM83 이론 200 mAh g⁻¹ — `[재현]` 0.140 mA · 0.178 mA cm⁻²) | 1C = 200 mA g⁻¹(`[데이터]` 그림 7 Q ÷ 그림 2 CC 시간 = 199.6–200.6 mA g⁻¹ ✅) = 1.40 mA · 1.78 mA cm⁻² | 실측 0.1C 방전 ≈117–131 mAh g⁻¹ → **측정 용량 기준 "1C" ≈1.5–1.7 h⁻¹**(`[재현]`) |
| 사이클 수 | 유지 1 회 | 그림 5 · 7: 78 · 76 · 74 · `[데이터]` 그림 2 시계열: 80 · 80 · 74(D7) | — |
| 셀 수 | 컷오프당 1(인쇄 0 — S4 의 열 · `[해석]`) | 컷오프당 1 | 반복 · ± 0 |

⇒ **개회로 보관이 아니라 상한 전위 정전위 유지다.** 서론의 calendar 정의(`[인쇄]` "Under long-term storage, cells undergo continuous degradation"[7])와 실제 프로토콜("potentiostatic hold (also known as float test or voltage hold)"[3,6])은 다르고, 본문은 이 차이를 "qualitative accelerated tool" 로 명시한다. OCV 보관 대조 · 저 SOC 유지 대조는 0.

## 2. 무엇으로 맞췄나 — `[데이터]` 그림 2 시계열(시간 · 전위)로 잰 것

| 축 | calendar 3.7 · 3.9 · 4.1 V | cycle 3.7 · 3.9 · 4.1 V | 맞췄나 |
|---|---|---|---|
| 명목 "48 h" | CV **48.00 · 48.00 · 48.00 h** | 1C CC **47.73 · 50.04 · 50.76 h** | ✅ 명목만 |
| 노화 단계 전체(그림 축) | 61.31 · 61.54 · 62.05 h(CC 충전 + CV + CC 방전 — 그림 1 회색 칸) | 47.73 · 50.04 · 50.76 h | ⚠ |
| 축 밖 시간(`[인쇄]` 절차 → `[재현]`) | 유지 중 EIS 48 회(시간 미인쇄) | 30 분 OCV 휴지 × 40 · 39 · 38 ≈**19–20 h** + EIS 38–40 회 | ❌ — 시간 축이 휴지 · EIS 를 뺀다(D8) |
| 상한 ±1.5 mV 체류 | **48.00 h** | **0.01 · 0.01 · 0.00 h** | ❌ |
| 상한 50 mV 안 | 48.21 · 48.07 · 48.03 h | **2.47 · 1.52 · 0.88 h** | ❌ ×20–55 |
| ≥ 3.70 V(형성 · RPT 상한) | 48.00 · 48.43 · 48.59 h | 0.01 · 8.03 · 12.35 h | ❌ |
| ≥ 3.58 V(분해 개시 하단[15]) | 48.73 · 49.18 · 49.28 h | 6.40 · 14.10 · 17.78 h | ❌ ×2.8–7.6 |
| 통과 전하 | **≈300 mAh g⁻¹**(3.9 V: CC 충전 135.7 · 방전 135.1 `[데이터]` @20 mA g⁻¹ + 유지 ≈29.5 `[도표]` S11 · 3.7 · 4.1 V 는 S12 판독 ≈302 · ≈300) | **9,006 · 9,465 · 10,154 mAh g⁻¹**(그림 7 파일 Σ(충 + 방)) · 그림 2 CC 시간 × 200 = 9,544 · 10,008 · 10,148 | ❌ ×30–34 |
| 등가 완전 사이클(÷ 2 × 130 mAh g⁻¹) | ≈1.2 | ≈35–39 | ❌ |
| 최대 탈리튬 깊이 | CC + 유지 ≈**158 · 166 · 169 mAh g⁻¹**(S12 `[도표]`) | 마지막 1C 충전 + RPT1 초과 반환분 ≈**92 · 96 · 104**(`[재현·가정]` — 62.8 + 29.3 · 68.3 + 27.6 · 72.6 + 31.8) | ❌ ×1.6–1.8 — **같은 "컷오프" 가 같은 충전 상태가 아니다** |
| RPT 틀 | 같은 형성 · RPT | 같은 형성 · RPT | ✅ |

- `[해석]` 1C 에서 셀은 IR(`[데이터]` 전류 반전 도약: 상단 3.9 → ≈3.25 V · 하단 2.0 → ≈3.25–3.4 V)로 컷오프에 **일찍** 닿는다 — 양극은 컷오프 전위의 평형 상태에 한 번도 가지 않는다. 그래서 "같은 컷오프" 라벨 아래 calendar 는 양극을 **≈1.6–1.8 배 깊게 탈리튬한 채 48 h** 두고, cycle 은 그 아래 창에서 ≈35–39 등가 사이클을 돈다.
- 본문 자신이 `[인쇄]` "In 48 hours of aging, the reduced time spent at unfavorable upper cut-off potentials during high C-rate cycling likely explains its less detrimental impact" 로 원인을 짚는다 — 그러나 **체류 시간 · 충전 깊이 · 통과 전하를 재거나 맞추지 않았고**, 1C 의 낮은 충전 깊이는 언급하지 않는다.

## 3. 판정

"calendar aging 이 cycle aging 보다 훨씬 나쁘다"(Q_loss 13.09 · 32.71 · 43.56 % 손실 ↔ 1.39 · 9.80 · 9.29 % 손실 — 인쇄 표)는 **"같은 명목 48 h · 25 ℃ · 같은 컷오프 숫자 · 셀 하나씩 · 인쇄 기준선"** 조건에서만 선다. 그 조건이 같은 열화 구동력(고전위 체류 · 충전 깊이 · 통과 전하)을 뜻하지 않는다:

- **고전위 체류로 맞추면**(상한 50 mV 안 시간): calendar 48 h ↔ cycle 0.9–2.5 h — 시간당 손실로 비교할 근거가 지면에 없다(체류 시간에 대한 손실의 함수형 0).
- **통과 전하로 맞추면**: calendar 는 cycle 의 1/30–1/34 전하로 3–9 배 손실(인쇄 Q_loss 비) — 전하당 손실은 calendar 쪽이 두 자릿수 크다.
- **기준선을 지면 정의(3번째 형성)로 맞추면**(§(e) D2): cycle 3.9 · 4.1 V 손실은 9.80 · 9.29 → **2.99 · 2.83 % 손실** — 대비는 오히려 커진다(3.9 V: 32.17 ↔ 2.99).
- ⇒ `[해석]` 결론의 **방향**(같은 명목 시간에서 정전위 유지가 더 가혹하다)은 자료와 양립한다. 그러나 "정전위 유지가 장기 사이클 열화를 예측 · 선별한다" 는 **이 편 안에서 검증되지 않았다** — 장기 사이클 대조는 인용[13,15]이고, 저자도 [7] 을 따라 "qualitative" 로 한정한다.

# ★ (b) 전위 기준 — In/InLi 인쇄 · Li⁺/Li 환산 인쇄(+0.62 V · 출처 0)

| 지면 값 | vs In/InLi `[인쇄]` | vs Li⁺/Li | 비고 |
|---|---|---|---|
| 노화 컷오프 | 3.7 · 3.8 · 3.9 · 4.0 · 4.1 V | **4.32 · 4.42 · 4.52 · "4.62" · 4.72 V `[인쇄]`** | 오프셋 0.62 V(출처 인용 0) · "4.62" 단위 누락(D12) |
| 형성 · RPT 창 | 2.0–3.7 V | `[재현]` 2.62–4.32 V | 형성 상한 = 3.7 V 유지와 같은 숫자 |
| 분해 개시(인용) | 3.58–3.7 V[5,13,15] | `[재현]` 4.20–4.32 V | 형성 · RPT 자체가 개시 띠 끝까지 간다 `[해석]` |
| 음극 | In 50 mg(∅9 mm · `[재현]` 0.636 cm²) + Li 1.2 mg | — | `[재현]` Li 0.1729 mmol · In 0.4355 mmol → **28.42 at% ✅** · 양극 이론 1.40 mAh 를 다 받아도 **34.08 at%**(LiIn 까지 여유 7.04 mAh) |

- **42호(Santhosha 2019) 값과 그 조건**: In–Li 평탄 0.62 V(그림 2a 그림 속 "0.622 V") · 평탄 창 ≈1–47 at% Li · 이완 OCV ≈0.625(1–30 at%) → ≈0.622(30–40) → ≈0.617(40–44) → ≈0.610 V(46–47 at%) — 2상역 안 ≈15 mV 처짐 — **액체 3전극(DOL/DME) · 실온 · 0.5 h 이완 · 전기화학으로 리튬화한 In 박**의 값(42호 digest 전사). 이 편의 조성 띠(28.4 → ≤34.1 at%)는 그 **0.622–0.625 V 띠 안**이다 ⇒ `[재현·외부 값]` 환산 오프셋 0.62 V 는 **조성 기준으로 ±≈5 mV 안에서 정합** — 단 고체 · 압착 박 · 50 MPa 명목에서 42호 액체 값이 그대로 옮겨 오는지는 이 편이 재지 않았다(기준극 0).
- **조립 방향**: `[인쇄]` "the In foil was in contact with the solid electrolyte while the Li foil was in contact with the current collector" = **21호(Sedlmeier 2023)의 InLi-(In) 형**. 21호는 이 방향이 개방회로 0.62 V 는 지키지만 0.2 mA cm⁻² 탈리튬에서 **0.39 ± 0.21 µAh cm⁻²** 만 내놓았다고 인쇄(21호 digest 전사 · 파우치 20 MPa · 다른 SE) — 이 편의 방전 전류는 In 면 기준 `[재현]` 0.22 mA cm⁻²(0.1C) · 2.2 mA cm⁻²(1C). ⇒ **기준 역할은 정합, 원천 역할(뒷면 Li 1.2 mg 의 접근성)은 미검사** — 이식 메모 §2-1 의 M1(조립 방향) · M2(조성 · 재고) ✅ 인쇄 · **M3(원천 역할 검사) ✗**.
- **64호(Koerver 2017 *JMCA*)와 같은 축**: 64호 상한 3.4 · 3.7 · 4.0 · 4.4 V vs In(무 Li In 박 · 오프셋 0.6) = 4.0 · 4.3 · 4.6 · 5.0 V vs Li(64호 digest 전사) ↔ 이 편 4.32–4.72 V(오프셋 0.62). 같은 Li 축에서 **이 편 3.7 V ≈ 64호 3.7 V vs In(4.3 V)** 이고, 이 편 4.0 · 4.1 V(4.62 · 4.72)는 64호 4.6 V 근처다. 64호: 4.3 V 는 양극 호 변화 "rather small but well reproducible" · 4.6 · 5.0 V 는 25 사이클에 양극 호 R ×4.5–5.5(64호 판독) — 이 편 calendar 의 컷오프 의존(3.7 V 손실 13 % ↔ 4.0 · 4.1 V 35 · 44 %)은 **같은 방향**이다(`[해석]` — 셀 · SE · NCM · 노화 형식이 다르다: 64호 β-Li₃PS₄ · NCM811 · 사이클 25 회 ↔ 이 편 Li₆PS₅Cl · NCM83 · 48 h 유지). 64호 첫 충전(4.3 V vs Li) 176 mAh g⁻¹ ↔ 이 편 첫 형성 충전(4.32 V vs Li) `[데이터]` 194.0 mAh g⁻¹(3.9 V calendar 셀 @20 mA g⁻¹) · S3 ≈197 `[도표]`.

# ★ (c) DRT 귀속의 근거 — 판정: calendar 는 조건부 성립 · cycle 은 가정 의존(RPT 비교는 기준선 문제로 불성립)

## 1. 지면이 쓴 근거

| 근거 | 이 편 | 판정 |
|---|---|---|
| 문헌 τ 대역 [31,33,34] | P_SE ∼10⁻⁸ · P_C1 10⁻³–10⁻² · P_C2 10⁻²–10⁻¹ · P_A 10⁻¹–1 · P_D ∼10 s | **가정** — [33] = 11호 Yu 2024 의 양극 봉우리 P3 ≈500 Hz 는 `[재현]` τ = 1/(2πf) ≈3.2×10⁻⁴ s 로 이 편 P_C1 창보다 **3–30 배 짧다**(11호 digest 전사 · 다른 셀: 흑연 완전지 · 20 MPa · 50 % SOC) · 11호는 자기 지도에서 P3 에 양극 · 음극을 함께 둔다(11호 digest) |
| 2D DRT 연속성 | calendar 지배 봉우리가 시간에 따라 연속 이동 | **지지** — 아래 C_eff 평탄 |
| 대칭셀 · 3전극 · 구성 교체 · 온도 | 0 | — |
| 정전용량 | `[인쇄]` "a simple increase of RC1 while the corresponding capacitance value of PC1 remains almost constant"(가능성 문장 · 값 0) | 우리 `[재현]` 이 처음 값을 낸다 ↓ |
| 측정 상태 | calendar = 유지 전위(고 SOC) · cycle = 1C 방전 끝(표류) · RPT = 0.1C 방전 끝 | **불일치**(G5) |
| 기준선 | 그림 6 = 한 스펙트럼 공통 | **불일치**(D3) |
| 방법 설정 | hybrid-drt 계층 베이즈 MAP · "without manual parameter tuning" · K–K 통과 · 기저 ±1 자릿수 | λ 는 "수동 0" 이지 "없음" 이 아니다 — 사전 · 초모수 인쇄 0(G10) |

## 2. `[데이터]` · `[재현]` — 봉우리 위치 · R · C_eff(= τ_peak ÷ 골–골 ln τ 적분 R)

| 스펙트럼 | τ_peak | γ_max | R(골–골) | C_eff | 메모 |
|---|---|---|---|---|---|
| calendar 3.7 V 1 h → 48 h | 0.905 → 5.12 ms | 111 → 543 Ω | 564 → 2,343 Ω | **1.61 → 2.19 µF** | 창 P_C 안 |
| calendar 3.9 V 1 h → 48 h | 5.37 ms → **0.19 s** | 672 Ω → **27.9 kΩ** | 2.73 → 75.4 kΩ | **1.97 → 2.53 µF** | 48 h 봉우리 = P_A 창(10⁻¹–1 s) 안 |
| calendar 4.1 V 1 h → 48 h | 17 ms → **0.54 s** | 4.14 → **347 kΩ** | 9.25 → 253.6 kΩ | **1.83 → 2.12 µF** | 24 h 부터 P_A 창 안 |
| cycle P_C1 첫 → 끝 (3.7 · 3.9 · 4.1 V) | 0.51 → 0.51 · 0.57 → 0.64 · 0.72 → 0.81 ms | 34 → 19 · 67 → 46 · 82 → 67 Ω | 149 → 77 · 242 → 155 · 262 → 200 Ω | 3.4 → 6.6 · 2.4 → 4.1 · 2.8 → 4.0 µF | **R ↓ · C ↑ · τ ≈ 일정 — 면적 증가형 서명**(전제 C ∝ 면적) |
| cycle P_A 끝 (3.7 · 3.9 · 4.1 V) | 0.33 · 0.26 · 0.16 s | 65 · 33 · 27 Ω | 창 0.05–2 s 적분 140 · 79 · 70 Ω(골–골 215 · 94 · 84) | **≈1.5–3.3 mF** | 첫 스펙트럼 6–8 Ω · τ ≈0.05 s |
| cycle P_D 끝 | 2.1 · 8.3 · 7.4 s | 21 · 21 · 19 Ω | 47 · 61 · 60 Ω | ≈0.04–0.14 F | 창 밖 쪽 |
| 전형(그림 4 = before) | P_C 9.1 ms · P_A ≈0.74 s · P_D 10.5 s | 92 · 64 · 119 Ω | P_C(C1 + C2 골–골) 532 Ω | P_C ≈17 µF · P_D ≈37 mF | τ > 3.18 s 몫 257 / 970 Ω(26 %) |

- **calendar**: 지배 봉우리의 τ 가 ×5.7 · ×35 · ×32 움직이는 동안 C_eff 는 **1.6–2.5 µF 로 평탄**하다 — `[해석]` 같은 정전용량 요소의 저항만 커지는 "저항형" 성장이고, cycle P_A(≈mF)와는 **세 자릿수 다른 요소**다 ⇒ "P_A 창으로 들어간 봉우리 = P_C 의 연장" 이라는 저자의 연속성 귀속은 우리 정전용량 검사로 **지지된다**(기하 면적 0.785 cm² 당 2–3 µF cm⁻² — 이중층 ≈10 µF cm⁻² 이하 ✓). 위치(양극–전해질 계면)는 τ 문헌 가정 + 고전위에서만 자란다는 정황(유지 전위 의존)이고, In/InLi 쪽 대조는 0 — **조건부 성립**.
- ⚠ **유지 중 스펙트럼의 크기는 상태 효과를 포함한다**: 1 h 스펙트럼부터 R_tot 0.81 · 3.5 · 9.3 kΩ(3.7 · 3.9 · 4.1 V) — 노화 전에 이미 ×4–11 차이(고 SOC 양극 계면) · 48 h 성장 ×3.9 · ×21 · ×27 의 일부가 "노화" 인지 "그 전위의 상태 이완" 인지 지면은 가르지 않는다(같은 상태 비교는 RPT 의 그림 6 뿐).
- **cycle**: P_A 의 C_eff ≈1.5–3.3 mF = 기하 면적(0.785 cm²) 당 **≈1.9–4.2 mF cm⁻²**(In 박 0.636 cm² 당 ≈2.4–5.2) — 이중층 ≈10 µF cm⁻² 의 **×190–520**. ⇒ 곱 축퇴 처방 3단계-b(C 상한)에서 **"전하 이동" 이름표가 통과하지 못한다** — 23호(R_SE/Anode 0.5–6.4 mF cm⁻² — "합금의 화학 용량 `[추론]`") · 84호(Li C3 ≈1 mF cm⁻²)와 같은 형태. 그 요소가 음극(In/InLi 합금 화학 용량)인지 다른 화학 용량인지는 이 편 자료로 가를 수 없다.
- ⚠ **cycle 시간분해 EIS 의 상태 표류**: 같은 사이클 동안 `[데이터]` 1C 방전 용량 46.99 → 62.77 · 47.30 → 67.71 · 61.86 → 71.71 mAh g⁻¹ · 누적 Σ(Q_ch − Q_dis) 31.3 · 38.4 · 56.1 mAh g⁻¹ · RPT1 방전 − 충전 = +29.3 · +27.6 · +31.8 mAh g⁻¹(@20 mA g⁻¹) ⇒ "1C 방전 끝" 의 리튬화 상태가 사이클마다 움직인다. P_A 성장(봉우리 높이 γ 6–8 → 27–65 Ω · 창 0.05–2 s 적분 R 17–24 → 70–140 Ω)은 **첫 ≈18 사이클**에 몰리고, 그 구간이 1C 방전 용량이 가장 빨리 오르는 구간과 겹친다 — `[해석]` 상태 표류 · 활성화 · 음극 계면 열화를 이 편 자료는 가르지 않는다.
- ⚠ **RPT(같은 상태) 비교의 기준선**: 그림 6 의 "before aging" 은 한 스펙트럼(Re(50 mHz) 719.5 Ω `[데이터]` — S4 의 calendar 3.7 V 셀 ≈709 Ω `[도표·화소]` 와 가깝다)이고, 신품 열 S4 의 셀 간 산포는 **694–1019 Ω** 다. 자기 셀 기준으로 바꾸면 RPT 저주파 Re 변화는:

| 셀 | 신품(S4 `[도표·화소]` ±≈10) | RPT(`[데이터]`) | 공통 기준(719.5) 대비 | **자기 셀 대비** |
|---|---|---|---|---|
| calendar 3.7 V | ≈709 | 845.9 | +126 | **+137 Ω(+19 %)** |
| calendar 3.9 V | ≈828 | 1,147.4 | +428 | **+319 Ω(+39 %)** |
| calendar 4.1 V | ≈793 | 1,524.7 | +805 | **+732 Ω(+92 %)** |
| cycle 3.7 V | ≈816 | 775.8 | +56 | **−40 Ω(−5 %)** |
| cycle 3.9 V | ≈1,019 | 989.3 | +270 | **−30 Ω(−3 %)** |
| cycle 4.1 V | ≈958 | 954.3 | +235 | **−4 Ω(−0.4 %)** |

  ⇒ 그림 6b · d 의 "only show a slight increase in the overall post-aging impedance. Again, a larger contribution from PA" 는 **다른 셀의 스펙트럼 대비**다. 자기 신품 대비 cycle 셀의 저주파 Re 는 오르지 않았다(판독 폭 안 · 저주파 끝 한 점 요약 — 봉우리별 자기 기준 DRT 는 S4 원자료가 없어 재현 불가).

## 3. 판정

- **calendar — "양극–전해질 계면 저항 성장이 지배"**: **조건부 성립** — 근거는 (i) 고전위 · 시간에 따라 연속 이동하는 한 봉우리 (ii) 우리 `[재현]` C_eff 평탄(µF — 이중층 자릿수 · P_A 의 mF 요소와 구별) (iii) 같은 상태 RPT 에서도 자기 셀 대비 저주파 Re +19 · +39 · +92 % · 위치 귀속은 τ 문헌 가정 · 계면층 ↔ 접촉 손실은 가르지 않는다(`[인쇄]` 둘 다 서술).
- **cycle — "음극–전해질 계면이 영향"**: **가정 의존 — 직접 증거 0.** (i) 대칭셀 · 3전극 · 온도 0 (ii) P_A 요소는 C 상한에서 "전하 이동" 이름표가 서지 않는다 (iii) 시간분해 측정 상태가 표류 (iv) RPT 비교는 공통 기준선 탓에 자기 셀 대비로는 증가가 없다. "non-uniform local current density … contact loss or void formation"[32,35,36] 은 기구 가설이다.
- [[drt-peak-count-nonidentifiability]] 에 비추면: 이 편은 λ 수동 조율을 없앤 대신 **이름표를 τ 창에 두고, 창을 넘는 이동을 연속성으로 덮는다** — 11호(λ 미인쇄) · 84호(창 밖 봉우리 이름)에 이은 일곱 번째 경보 자리(개념 갱신).

# ★ (d) 용량 손실의 분해 — 무엇을 재는가

- **ΔV(50 % SoC)** · **Q_loss** 는 같은 0.1C 마지막 형성 · RPT 곡선 쌍에서 뽑은 두 수이고, 그림 3e · f 의 "correlation" 은 그 둘의 동행이다 — 동역학(분극) 몫과 열역학 몫(LAM_PE · LLI · 접촉 손실)을 가르는 설계(준평형 RPT · GITT · OCV · 율 대조)는 0.
- `[재현·가정]` **균일 분극 이동 상한**: ΔV 증가분의 절반 η = 23.5 · 85.0 · 126.5 mV(calendar)를 "before" 곡선에 균일하게 얹으면 충전은 3.7 − η 에서 · 방전은 2.0 + η 에서 끊긴다 → 예상 손실 **1.5 · 7.3 · 13.4 %** ↔ 관측(같은 before 대비) **12.0 · 31.0 · 41.8 %** ⇒ 50 % SoC 의 ΔV 로 설명되는 몫은 **≈1/8–1/3**. 나머지는 (i) 열역학 손실(LAM_PE · CAM 안 Li 갇힘) 또는 (ii) **SOC 의존 분극**(고 SOC 쪽에서만 큰 저항 — 유지 중 스펙트럼이 그쪽을 가리킨다)이고, 이 편 자료로는 가를 수 없다(cycle: 0.3 · 1.7 · 1.2 % ↔ 1.0 · 9.0 · 8.7 %).
- **dQ/dV**: `[데이터]` calendar 충전 봉우리 377.1 → 305.1 → 215.1 → 184.3(3.166 → 3.219 V) · 방전 −298.0 → −265.6 → −194.0 → −141.9(3.100 → 3.017 V) · 봉우리 간격 0.066 → 0.087 → 0.164 → 0.202 V — 세기 ↓ 와 함께 **충전 봉우리는 위로 · 방전 봉우리는 아래로** 이동(분극 서명). 저자는 세기 ↓ 를 "loss of lithium inventory in the CAM[23]"(액체 · 흑연 NCM 문헌)으로 읽는다 — 분극이 봉우리를 넓히고 낮추는 몫과 가르지 않았다.
- **RPT 회복**: `[데이터]` calendar RPT 방전 1 → 3 사이클 +0.72 · +2.13 %(3.9 V 셀 @20 mA g⁻¹: 84.9 → 85.5 → 87.3 mAh g⁻¹) · S5 판독 3.9 V ≈78 → 88 · 4.1 V ≈66 → 74 — **가역 몫이 있다**(본문은 3번째 RPT 를 골라 "residual reactions" 를 줄였다고 적음). cycle 셀은 RPT2 → 3 −0.27 · −0.70 % 로 거의 평탄.
- **형성 연속 감쇠**: `[데이터]` 여섯 셀 형성 방전이 사이클당 −1.6 ~ −4.6 %(마지막 단계 −1.57 ~ −2.96 %) — 기준선(3번째 형성)이 아직 움직이는 중이다(G3).
- **Q7 — In/InLi 의 과잉 Li**: `[재현]` Li 1.2 mg = **4.63 mAh** ↔ 양극 이론 1.40 mAh(**×3.31**) · 실측 첫 충전 1.36 mAh(194 mAh g⁻¹ × 7 mg) ⇒ 뒷면 Li 가 접근 가능하면 부반응 Li 소모는 방전 용량에 **보이지 않는다**(재고가 메운다) — 그 경우 calendar 손실은 LLI 가 아니라 LAM_PE · CAM 리튬화 실패 · 동역학 몫이다. 그러나 조립이 InLi-(In) 형이라 접근성은 미검사(21호 · M3 ✗) ⇒ **"LLI 가 용량에 보이는가" 는 이 편에서 판정 불가**. 정황: calendar RPT CE 100.05 · 101.22 · 101.78 %(Q_dis > Q_ch — 음극 쪽 Li 가 양극으로 더 돌아온다 `[데이터]`) · 1C 뒤 RPT1 초과 반환 +28–32 mAh g⁻¹ — 둘 다 음극에 쌓인 Li 가 다시 쓰인다는 표본이지만, 그 Li 가 뒷면 Li 박에서 온 것인지(재고)는 가르지 않는다.
- **Q1 — 접촉 손실**: `contact loss` 3 회 전부 가능성 · 인용 문장(양극 계면[27] · 음극 계면[35,36] · 과충전 부피 팽창 → 복합 양극 균열 · 접촉 손실) · `θ(N)` **0/90**. 우리 `[재현]` C_eff 평탄(calendar)은 **면적 손실형이 아니라 저항형**(전제 C ∝ 면적)이라 유지 노화의 지배 성장은 접촉 면적 손실보다 계면층 쪽 서명이다 — `[해석]` 판독 한 층(곱 축퇴 처방 1단계 판독).
- **채움표 칸**: Q1 층 하나(C_eff 판독) · Q2 없다(독립 관측 0) · Q3 층(τ 창 이름표 + 연속성 · 공통 기준선) · Q4 여든두 번째 성질 · Q5 서른네 번째 형태 · Q6 보고(SI) · Q7 해당 없음(층 하나 — 재고 ×3.31 · 접근성 미검사) · Q8 층 하나(균일 이동 1/8–1/3) — §(f).

# ★ (e) 데이터 재현 — ZIP 으로 인쇄 수치 대조 (`[데이터]` · `[재현]`)

재현에 쓴 파일(안쪽 `data.zip` 경로): `Figure 2 …/{3.7,3.9,4.1} V {calendar,cycle} aging.txt` · `Figure 3 …/{a,b} Potential vs capacity_*/…_{charge,discharge}.txt` · `Figure 3 …/{c,d} Differential capacity_*/…` · `Figure 3 …/{e,f} Voltage gap - Q loss_*.txt` · `Figure 4 …/{fit,Nyquist plot,b DRT}.txt` · `Figure 5 …/{a,b}/…/cycle_NN.txt` · `Figure 6 …/{a–d}/…` · `Figure 7 …/a …/{charge,discharge}/cNN.txt`. 계산 스크립트는 세션 스크래치(커밋 안 함).

| 무엇 | 입력 | 결과 | 판정 |
|---|---|---|---|
| 1C 전류 | 그림 7 사이클 Q ÷ 그림 2 CC 시간 | 충 199.7–200.6 · 방 199.5–200.5 mA g⁻¹ | ✅ 1C = 200 mA g⁻¹(이론 기준 인쇄와 같음) · 시간 축이 CC 단계 안에서는 충실 |
| ΔV(50 % SoC) | 그림 3a · b 곡선(자기 곡선 용량의 50 %) | calendar 0.162 · 0.209 · 0.332 · 0.415(같은 Q 기준 0.410) · cycle 0.177 · 0.188 · 0.232 · 0.218 V | 표 e · f(0.16 · 0.21 · 0.33 · 0.41 · 0.19 · 0.23 · 0.22) ✅ · **cycle "Pristine" 0.16 ❌ — 그 판 before 곡선은 0.177(D6)** |
| 마지막 형성 · RPT 용량 | 그림 3a · b | calendar before 130.75/129.13 · 3.7 V 113.63/113.69 · 3.9 V 87.99/89.06 · 4.1 V 73.80/75.11 · cycle before 130.05/128.45 · 127.16 · 116.93 · 117.23(방전) mAh g⁻¹ | CE: calendar RPT 100.05 · 101.22 · 101.78 %(Q_dis > Q_ch — 본문 서술 ✅) |
| Q_loss — 그림 3 의 before 곡선 대비 | 같은 판 before | calendar 11.96 · 31.03 · 41.83 % 손실 · cycle 1.00 · 8.97 · 8.73 % 손실 | 표(13.09 · 32.71 · 43.56 · 1.39 · 9.80 · 9.29) ❌ — 그림의 before 곡선은 Q_loss 의 분모가 아니다 |
| **Q_loss — 셀마다 자기 형성 대비(시간 비)** | 그림 2 CC 방전 시간 비(0.1C 정전류 — 정규화 무관) · 그림 2 ↔ 3 폐합 검사 | **cycle 3.9 V**(폐합 ✅ f 19.98–20.03 mA g⁻¹): 3번째 형성 기준 **2.99 %** · 1번째 **9.69 %** · **cycle 4.1 V**(✅ 19.94–20.07): **2.83 %** · **9.32 %** · calendar 3.9 V(⚠ 2 % 비례 · 충방 비 0.19 %): **32.17 %** · 36.44 % · calendar 4.1 V(그림 2 RPT = 복사 → 그림 3 RPT3 · f = 20 가정): 39.85 % · **43.50 %** | 인쇄 9.80 · 9.29 · 43.56 % = **첫 형성 기준**과 0.03–0.11 %p · calendar 3.9 V 인쇄 32.71 % 는 3번째 기준과 0.54 %p ⇒ **지면 정의("last (3rd) formation") 로 일관되게 재현되지 않는다(D2)** · 3.7 V 두 셀은 그림 2 ↔ 3 폐합 실패로 판정 불가(D15) |
| 형성 감쇠 | 그림 2 형성 방전(@20 mA g⁻¹) | 3.9 V calendar 137.4 → 132.1 → 128.7 · 3.9 V cycle 129.3 → 123.9 → 120.4 · 4.1 V cycle 129.7 → 124.7 → 121.0 mAh g⁻¹ | 형성 셋째 단계에도 −1.6 ~ −3.0 %/사이클(G3) |
| 그림 2 ↔ 그림 3 폐합(RPT3) | f = Q(그림 3) ÷ CC 시간(그림 2) | calendar 3.7 V f_충 20.94 · f_방 21.96(4.6 % 불일치) · 3.9 V 20.44 · 20.40 · 4.1 V 17.14 · 17.20(복사 구간) · cycle 3.7 V 19.34 · 19.16(1.0 %) · 3.9 V 19.98 · 20.03 · 4.1 V 20.07 · 19.94 | ✅ 3.9 · 4.1 V cycle · ⚠ 3.9 V calendar(2 % 비례) · ❌ 3.7 V 두 셀 · 4.1 V calendar(D15 · D1) |
| **그림 2 4.1 V calendar RPT** | 두 파일 전위 열 대조 | 4.1 V 파일 103.504–128.881 h 의 **9,794 연속 표본이 3.9 V 파일 104.377–129.754 h 와 전위 · 시간 증분이 같다**(Δt 0.8732 h · 시간 증분 차 ≤3×10⁻¹⁴ h) · 나머지 30 쌍 대조에서 중복 0 | ❌ 복사(D1) — 원본은 3.9 V 쪽(그림 3 3.9 V RPT3 충전 곡선과 모양 차 4.7 mV ↔ 4.1 V 15.0 mV) |
| 그림 1 정체 | 그림 1 s0–s2 ↔ 그림 2 | calendar · cycle 모두 **3.9 V 셀**(시각 · 전위 동일) | 캡션 미표기 · 그림 안 "3.9" |
| dQ/dV 봉우리 | 그림 3c · d | calendar 충 377.1 · 305.1 · 215.1 · 184.3(3.166 · 3.168 · 3.209 · 3.219 V) · 방 −298.0 · −265.6 · −194.0 · −141.9(3.100 · 3.081 · 3.045 · 3.017 V) · cycle 충 373.9 · 339.5 · 296.3 · 313.8 · 방 −284.7 · −283.1 · −240.8 · −246.2 | 그림 판독과 일치 · cycle 3.9 · 4.1 V 충전 최댓값은 3.086 V 첫머리 인공물(347 · 767) |
| 2D DRT 색 막대 | 그림 5 자료 최댓값 | calendar 542.8 Ω · 27.88 kΩ · 347.1 kΩ · cycle 64.5 · 73.7 · 134.6 Ω | ✅ 543 · 28 · 347 · 65 · 74 · 135 |
| 지배 봉우리 이동 | 그림 5a | 3.7 V 0.905 → 5.12 ms · 3.9 V 5.37 ms → 0.19 s · 4.1 V 17 ms → 0.537 s(1 → 48 h) | "P_C shift" ✅ · P_A 창 진입(D14) |
| C_eff | 그림 5 · 4 | §(c) 표 | 지면 값 0 → 우리 첫 값 |
| 그림 6 기준선 | 그림 6 a · b · c · d "before aging" · 그림 4 | **같은 내용**(Nyquist 164 점 · DRT 284 점 동일) · Re(50 mHz) 719.5 Ω | 공통 기준선(D3) |
| 그림 6 RPT 저주파 Re | 그림 6 Nyquist | calendar 845.9 · 1,147.4 · 1,524.7 · cycle 775.8 · 989.3 · 954.3 Ω | S4 자기 셀 대비 §(c) 표 |
| 1C 용량 · CE | 그림 7 | 방전 첫 → 끝 46.99 → 62.77 · 47.30 → 67.71 · 61.86 → 71.71 · 첫 충전 68.29 · 68.75 · 86.68 · 평균 CE 99.35 · 99.22 · 99.00 % · Σ(Q_ch − Q_dis) 31.3 · 38.4 · 56.1 mAh g⁻¹ | "slight increase in capacity" ✅ · 3.9 V 충전 용량이 두 사이클 주기로 엇갈림(53.8 · 55.9 · 55.3 · 57.6 …) — 두 사이클마다 휴지 정황 |
| 사이클 수 | 그림 2 · 5 · 7 | 그림 2 1C 충전 80 · 80 · 74 · 그림 7 파일 75(1–74 · 78) · 76 · 74 · 그림 5 스펙트럼 40(…78) · 39(…76) · 38(…74) | ❌ 3.7 · 3.9 V(D7) — 3.7 V 시계열 끝 넷(52.3 · 56.6 · 51.0 · 45.8 mAh g⁻¹)은 그림 7 에 없음 |
| 셀 · 전류 산술 | ESI 인쇄 | 1.783 mAh cm⁻² ✅(7 mg × 200 ÷ 0.7854) · 28.42 at% ✅ · 0.1C 0.140 mA = 0.178 mA cm⁻² · 1C 1.78 mA cm⁻² | ✅ |
| 압력 산술 | "3 tons" · "10 Nm … ~50 MPa" | 3 t-f ÷ 0.785 cm² = **374.6 MPa**(미터 톤 · 미국 톤이면 339.8 — `[재현·가정]`) · 50 MPa × 0.785 cm² = **3.93 kN** | 토크 → 압력 환산 재현 불가(볼트 수 · 지름 · 마찰 미인쇄 — G9) |
| S14 막대 | S12 판독 | 91.1 · 89.6 · 81.3 · 82.5 · 77.5 % | ✅ 91 · 90 · 81 · 82 · 78(그림 안 인쇄) |
| 일정 | 2025-02-10 → 05-12 → 05-13 → 06-05 | 91 · 92 · 115 일 | — |

⇒ **판정**: ΔV 표 · 색 막대 · 1C 기준 · 셀 산술은 **일치**. Q_loss 는 **지면 정의로 일관 재현 불가**(cycle 두 셀은 첫 형성 기준으로 일치). 자료 무결성 문제 **둘**(4.1 V calendar RPT 복사 · 3.7 V 두 셀의 그림 2 ↔ 3 불폐합)과 사이클 번호 불일치. ZIP 은 **본문 그림 1–7 · 세 컷오프만**이라 3.8 · 4.0 V 의 시계열 · SI 그림은 재현 불가.

# ★ (f) Q1–Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/90** · 층 하나: 우리 C_eff 판독(유지 노화 지배 성장 = 저항형 · 면적형 아님 — 전제 C ∝ 면적) | `contact loss` 3 회 = 가능성 · 인용 서술 · 사후 분석 0 |
| **Q2** 독립 관측 | **없다** — 같은 셀 · 같은 전기화학의 두 채널(0.1C 곡선 · DRT) | 대칭셀 · 3전극 · 영상 · 분광 0 |
| **Q3** 라벨 층위 | **층 하나: "τ 창 이름표 + 연속성 · 공통 기준선"** — 계층 베이즈 MAP 역변환(λ 수동 0 · 사전 미인쇄) 위에 문헌 τ 대역으로 이름 · 창을 넘는 이동은 연속성으로 이름 유지 · 비교 기준선 한 셀 · 셀 수 1 · ± 0 · 원자료 부분 예치 | D3 · D13 · D14 |
| **Q4** 유일성 · 식별성 | **0/90 — ASSB 누적 0.5(29호) 유지. 여든두 번째 성질 "시간분해 DRT 로 '어느 계면이 지배하나' 를 판정하되, 봉우리 이름을 문헌 τ 창으로만 정하고(대칭셀 · 3전극 · 온도 · 정전용량 대조 0) 지배 봉우리가 다른 이름의 창으로 넘어가도 연속성으로 이름을 유지하며, 두 프로토콜의 시간분해 EIS 를 서로 다른 상태(유지 전위 ↔ 표류하는 1C 방전 끝)에서 재고, RPT 비교의 기준선을 한 셀 스펙트럼으로 공유해 셀 간 산포(신품 694–1019 Ω)를 효과로 읽는다"** | `identif` 3(전부 "identifying/identify … degradation" — 일반 뜻) · `uniq` · `uncertain` · `error` · `reproduc` · `±` 0 · `regulari` · `λ` 0 · `Bayesian` 1(ESI — 방법 이름) |
| **Q5** Li-In 기준 | **층 하나 — 서른네 번째 형태**: In 박 50 mg(∅9 mm) + Li 1.2 mg = 28.42 at%(`[재현]` ✅) · **조립 방향 인쇄**(In 이 SE 쪽 · Li 박 집전체 쪽 = 21호 InLi-(In) 형) · 컷오프 · 창 전부 vs In/InLi · **Li⁺/Li 환산 인쇄(+0.62 V · 출처 0)** · 기준극 0 · 원천 역할 검사 0 | 이식 메모 M1 · M2 ✅ · M3 ✗ · 42호 평탄 띠 안(0.622–0.625 V · 액체 조건) |
| **Q6** 압력 | **보고 — 칸 이동 없음**: 운전 "a torque of 10 Nm providing an operating stack pressure of ~50 MPa"(**ESI 에만** · 토크 명목 · 계측 0 · 환산 근거 0) · 성형 "a uniaxial pressure of 3 tons … for 3 min"(`[재현·가정]` ≈375 MPa) · 본문 `pressure` **0 회** | (캐)(해) 표본 · `[재현]` 50 MPa ↔ 3.93 kN |
| **Q7** dead Li · Li 재고 | **해당 없음(무음극 아님) — 층 하나: In/InLi 공칭 재고 ×3.31(4.63 ↔ 1.40 mAh `[재현]`) · InLi-(In) 조립으로 접근성 미검사 → "LLI 가 용량에 보이는가" 판정 불가** · 저자는 dQ/dV 세기 ↓ 를 "loss of lithium inventory in the CAM" 으로 읽음 | RPT CE > 100 % · RPT1 초과 반환 +28–32 mAh g⁻¹(`[데이터]`) |
| **Q8** 화학 · OCP | **층 하나 — 0.1C 곡선만(OCV 0) · `[재현·가정]` 50 % SoC ΔV 의 균일 이동은 calendar 손실의 1/8–1/3 만 설명** | NCM83(MSE · 입도 · 코팅 미인쇄) · 탄소 0 복합 · 첫 형성 CE ≈70 %(S3 `[도표]`) · 첫 충전 194.0 mAh g⁻¹(`[데이터]` @20 mA g⁻¹) |

# 어휘 집계 — 텍스트 층 · NFKC · 줄 끝 하이픈 복원 · 쪽 머리 · 바닥글 제외 · 본문(제목 → 사사 · 캡션 포함 · 참고문헌 제외) | ESI(p. 1 → p. 12 · 캡션 · 참고문헌 제외)

| 열 | 본문 | ESI | 메모 |
|---|---:|---:|---|
| `contact` · `contact loss` | 3 · 3 | 2 · 0 | 본문 셋 = 전부 "contact loss"(양극[27] · 음극[35,36] · 과충전 균열) · ESI 둘 = In 박 · Li 박 배치 |
| `crack` · `void` · `chemo(-)mechanical` | 1 · 1 · 2 | 0 | 가능성 문장 |
| `pressure` · `stack pressure` · `MPa` · `torque`/`Nm` | **0** · **0** · **0** · **0** | 2 · 1 · 1 · 2 | **압력은 ESI 에만** |
| `lithium inventory`/`cyclable lithium` · `LAM` · `LLI` | 3 · **0** · **0** | 0 | |
| `OCV`/`open circuit` · `dQ/dV`/`differential capacity` | 5 · 12 | 3 · 2 | OCV 는 보관 정의 · 휴지 · EIS 바탕 |
| `DRT` · `resistan` · `capacitan` | 28 · 14 · 4 | 15 · 0 · 0 | capacitance 값 0 |
| `three-electrode`/`reference electrode` · `symmetric` | **0** · **0** | 0 · 0 | |
| `temperature` · `°C` | 1 · 0 | 0 · 3 | 25 ℃ 한 점 |
| `SoC` · `cut-off` · `In/InLi`(+In/LiIn) · `Li+/Li` | 5 · 25 · 8 · 1 | 0 · 7 · 5 · 0 | |
| `calendar` · `cycle aging/aged` · `potentiostatic hold`/`voltage hold`/`float` | 35 · 27 · 25 | 12 · 9 · 3 | |
| `interphase` · `decomposition` · `anode` · `cathode` | 7 · 7 · 6 · 16 | 0 · 0 · 1 · 4 | |
| `screen` | 8 | 0 | 권고 문장 |
| `identif` · `uniq` · `uncertain` · `error` · `reproduc` · `±` | 3 · 0 · 0 · 0 · 0 · 0 | 0 | identif = 일반 뜻 |
| `regulari`/`λ` · `Kramers` · `Bayesian` | 0 · 0 · 0 | 0 · 1 · 1 | |
| `ESI`/`†` · `Fig. S` | 36 · 7 | 6 · 0 | S1–S14 전부 불림 |

# ★ (g) 우리 위키와의 관계

## 1. Yu 2024(11호)와의 대조 — 가장 가까운 선행 (11호 값은 digest 전사 · 원문 재열람 0)

| 항목 | 11호 Yu … Kim 2024 *JPS* 597, 234116 | 90호(이 편) |
|---|---|---|
| 셀 | LiNbO₃-NMC622 \| Li₆PS₅X(Cl · Br) \| **흑연** 완전지 + NMC/In–Li · 흑연/In–Li 반쪽 | NCM83 : Li₆PS₅Cl 7 : 3(탄소 0) \| Li₆PS₅Cl \| **In/InLi**(28.42 at%) 반쪽 |
| 노화 | C/3 사이클(완전지 500 사이클 · 반쪽 48–133) + 재가압 개입 | 48 h 정전위 유지 ↔ ≈48 h 1C 사이클 · 컷오프 다섯 |
| EIS 상태 | **50 % SOC 를 매 측정 유지** · 2 MHz–0.1 Hz · 10 mV | 유지 전위 / 1C 방전 끝(30 분 휴지) / 0.1C 방전 끝 · 7 MHz–50 mHz · 10 mV rms |
| DRT | DRTtools(Wan 외) · **λ · 정규화 미인쇄** · K–K 0 | hybrid-drt 계층 베이즈 MAP("without manual parameter tuning") · K–K 통과 인쇄 · 사전 미인쇄 |
| 귀속 근거 | **세 구성(완전지 ↔ 두 반쪽) 비교** · SE 입도 · 코팅 · 재가압 조작 · 단 P3 에 양극 · 음극을 함께 둔다 | **문헌 τ 대역 + 2D 연속성**(구성 비교 · 조작 0) |
| 결론 | P3(≈500 Hz) 성장 = 주로 양극 · 재가압으로 되돌림 → 접촉 손실 대리 | calendar = 양극 계면(P_C) · cycle = 음극 계면(P_A) · 정전위 유지를 선별 프로토콜로 권고 |
| 압력 | 제작 >500 · 운전 20 · 재가압 150 / >500 MPa(본문) | ESI 에만 ~50 MPa(토크 명목) |
| 원자료 | "do not have permission to share data" | 본문 그림 1–7 예치(부분) |

- **인용 여부**: ✅ 이 편 [33] = 11호 — 쓰임 `[인쇄]` "Two overlapping peaks PC1 (τ ∼10⁻³ to 10⁻²) and PC2 (τ ∼10⁻² to 10⁻¹ s) can be ascribed to Li-ion transport through the cathode–electrolyte interface (RC1) and interfacial charge transfer resistance (RC2) within the cathode composite, respectively.[31,33]" — `[재현]` 11호의 양극 봉우리 P3 ≈500 Hz(τ ≈3.2×10⁻⁴ s)는 이 편 P_C1 창의 3–30 배 짧은 쪽이다(D20 — 셀 · 상태 · 압력이 다르니 τ 가 다를 수 있다. 다만 [33] 은 이 편 τ 대역의 값 근거가 될 수 없다 `[해석]`).
- `[해석]` 두 편은 같은 "시간분해 DRT 노화" 형식이지만 **귀속 근거의 강도가 반대 방향으로 기운다** — 11호는 구성 비교 · 조작이 있으나 λ · 정규화가 비어 있고, 이 편은 역변환 설정이 자동 · K–K 검사까지 있으나 구성 비교 · 조작이 없다. 둘 다 같은 상태 반복(11호 50 % SOC ↔ 이 편 RPT 방전 끝)은 지켰고, 둘 다 셀 수 · 산포가 없다.

## 2. Huo 2025(9호) 인용의 쓰임

| 자리 | `[인쇄]` 문장 | 9호 digest 와 대조 | 판정 |
|---|---|---|---|
| p. 1 서론 | "While cell aging studies have been well established for LIBs, they are far less developed for their SSB counterparts.¹¹" | 9호는 황화물 ASSB 노화 실험 + 결합 노화 모형 편(SJTU · NCM811(H₃BO₃) : LPSCl : VGCF 56 : 40 : 4 \| LPSCl \| Li₃.₇₅Si · 1C 사이클 · 셀 둘) — 9호 digest 에 이 명제의 원문 문장 전사 0 | **판정 보류**(일반 배경 · 9호 원문 대조 전) |
| p. 5 결과 | "Similar phenomena were observed for the Li5.5PS4.5Cl1.5-NCM83 interface by Hartel et al., where strong interfacial degradation was triggered in the In/InLi\|Li5.5PS4.5Cl1.5\|NCM83:Li5.5PS4.5Cl1.5 half-cells when the cathode potential exceeded 3.7 V vs. In/InLi,¹¹"(위첨자 "11" 화면 확인) | 9호 셀은 In/InLi 도 Li₅.₅PS₄.₅Cl₁.₅ 도 NCM83 도 아니고(`indium` 0 회 · 9호 digest), "Hartel et al." 은 이 편 **[13]**(Hartel … Zeier 2024 *Chem. Mater.*) · p. 3 같은 문턱에 [5,13,15] 를 단다 | ❌ **번호 오기로 읽힌다(D4 · `[해석]`)** — 9호를 "3.7 V 문턱" 의 근거로 옮기지 않는다 |

## 3. 정전위 유지 노화가 우리 합성 truth · 모형에 요구하는 것 (`ASSB_TRANSFER_NOTE.md` §2–§4 를 읽기만 · `[해석]`)

- **이식 메모의 전제**(§1): 평탄 상대극(In/InLi 0.62 V 상수)에서 3-파라미터(a_PE · b_PE + 상대극 상수)로 OCV 를 적합. 이 편의 RPT 는 **0.1C · ΔV 0.16–0.41 V** — 준평형이 아니라서 **현행 OCV 적합 하네스의 입력이 못 된다**: 분극이 a_PE(겉보기 LAM_PE) · b_PE(겉보기 LLI)로 새어 들어간다(우리 균일 이동 산술로도 손실의 1/8–1/3 이 분극 몫).
- **정전위 유지가 truth 생성에 요구하는 것**: (i) **전위 · 시간 의존 계면층 저항 R_int(t, V_hold)**(이 편: C_eff ≈2 µF 평탄 · R ×4–27 — "저항형" 성장 · 시간 의존 함수형은 [5,37] "classical time dependency models" 를 저자도 "may yield inaccurate results" 로 피함) (ii) **SOC 의존 분극**(고 SOC 쪽 저항 — 유지 중 1 h 스펙트럼부터 컷오프에 따라 ×4–11) (iii) 열역학 손실 몫(LAM_PE · CAM Li 갇힘)과 동역학 몫을 **같은 상태 · 준평형 RPT** 로 가를 수 있는 관측 설계 — 이것이 A1(접촉 손실 ↔ LAM_PE) 판정의 전제와 같은 요구다.
- **M1–M3**: 이 편은 조립 방향(M1) · 재고(M2)를 인쇄한 드문 표본이고, M3(원천 역할 검사)는 0 — "LLI 가 상대극을 거쳐 LAM_PE 로 샌다"(§2-1)의 판정 조건이 그대로 남는다.
- `[해석]` **선별 프로토콜로서의 쓸모**: 이 편 권고는 "정성적 선별" 이고, 우리 합성 truth 쪽에서 보면 정전위 유지는 **한 손잡이(컷오프)가 체류 · 충전 깊이 · 측정 상태를 함께 움직이는** 프로토콜이다(§(a)) — 이식판 truth 에 넣는다면 그 셋을 따로 기록하는 메타데이터가 먼저다.

# ★ (h) SI — 12 쪽 전부 봤다

- 구성: p. 1 표지 · pp. 2–4 실험(§절별 해체 마지막) · pp. 4–12 그림 S1–S14(§그림) · p. 12 참고문헌 4([1] Kraft … Zeier 2017 *JACS* 139, 10909 · [2] Zuo … Janek *Nat. Commun.*(DOI 만) · [3] Pan, Zou, Canova, Zhu, Kim 2020 *JPS* 479, 229083(DRT 기본식) · [4] Huang … O'Hayre 2023 *Electrochim. Acta* 443, 141879).
- 표 0 · 식 1(DRT 적분식 `Z(ω) = ∫ g(ln τ)/(1 + jωτ) d ln τ` — 텍스트 층 글리프 깨짐 · 그림 확인).
- 본문 참조 대조: S1–S14 전부 본문이 부른다(범위 포함) · 본문 † 목록에 없는 내용(DRT 방법 · 노화 절차 · S11 · S14)이 ESI 에 있다.
- ⚠ ESI 가 본문보다 무거운 정보를 든다: **압력 · 셀 질량 · 조성 · 전류 기준 · 휴지 30 분 · DRT 설정** 전부 ESI 에만 — 카드 · 개념으로 옮길 때 출처 칸에 "ESI" 를 적는다.

# 재현 (`[재현]` — 지면 · 자료 숫자로 우리가 계산 · 외부 값 · 가정 표시)

| 무엇 | 입력 | 결과 | 판정 |
|---|---|---|---|
| 면적 · 면적 용량 | ∅1 cm · 7 mg NCM × 200 | 0.7854 cm² · 1.40 mAh · **1.783 mAh cm⁻²** | 인쇄 1.783 ✅ |
| 음극 조성 | In 50 mg · Li 1.2 mg | **28.42 at%** · Li 4.634 mAh · 양극 대비 ×3.31 · 만충 뒤 34.08 at% · LiIn 까지 여유 7.04 mAh | 인쇄 28.42 ✅ |
| In 박 면적 | ∅9 mm | 0.636 cm² · 0.1C 0.22 · 1C 2.2 mA cm⁻²(In 면) | — |
| 전류 | 0.1C · 1C | 0.140 · 1.40 mA · 0.178 · 1.78 mA cm⁻² · 측정 용량 기준 1C ≈1.5–1.7 h⁻¹ | — |
| 성형 압력 | "3 tons" ÷ 0.785 cm² | 374.6 MPa(미터 톤) · 339.8 MPa(미국 톤) | `[재현·가정]` 단위 미인쇄 |
| 운전 힘 | 50 MPa × 0.785 cm² | 3.93 kN | 토크 → 힘 재현 불가 |
| 전위 환산 | +0.62 V | 2.62–4.32 V(창) · 4.20–4.32 V(분해 개시 인용) | 인쇄 환산과 같은 오프셋 |
| 체류 · 전하 · 깊이 | §(a) 표 | 48.00 ↔ 0.00–0.01 h · ≈300 ↔ 9,006–10,154 mAh g⁻¹ · ≈158–169 ↔ ≈92–104 mAh g⁻¹ | `[데이터]` · `[도표]` · `[재현·가정]` |
| ΔV · Q_loss · dQ/dV | §(e) 표 | — | 부분 일치 |
| 균일 분극 이동 | η = ΔV 증가 ÷ 2 | calendar 1.5 · 7.3 · 13.4 % ↔ 12.0 · 31.0 · 41.8 % | 1/8–1/3 |
| C_eff | τ ÷ R(골–골) | P_C 1.6–6.6 µF · P_A 1.5–3.3 mF · P_D 0.04–0.14 F | §(c) |
| 창 밖 몫 | 그림 4 DRT | τ > 3.18 s 257 Ω / 970 Ω(26 %) · τ < 2.27×10⁻⁸ s 27.5 Ω | — |
| 11호 τ | 500 Hz | 3.2×10⁻⁴ s | D20 |
| S4 저주파 끝 | 화소(눈금 208 · 405.5 · 603.5 px = 0 · 500 · 1000 Ω · 표지 지름 20 px) | §(c) 표 | `[도표·화소]` ±≈10 Ω |

# 참고문헌 37 — 우리 축에 닿는 것 (번호는 PDF 목록에서 직접 확인 · 목록은 번호 붙은 1–37)

- **우리 위키에 원전(ingest 된 digest) 셋**: **[11] Huo D., Li G., Fan G., Zhang X., Han J., Wang Y., Zhou B., Chen S., Jia L. *J. Power Sources* 2025, 627, 235830 = 9호** · **[27] Koerver R., Aygün I., Leichtweiß T., Dietrich C., Zhang W., Binder J.O., Hartmann P., Zeier W.G., Janek J. *Chem. Mater.* 2017, 29, 5574 = 23호** · **[33] Yu C.-Y., Choi J., Dunham J., Ghahremani R., Liu K., Lindemann P., Garver Z., Barchiesi D., Farahati R., Kim J.-H. *J. Power Sources* 2024, 597, 234116 = 11호**.
- **원장 §1 행 있음**: [3] Tan D.H.S. … Meng Y.S. *Science* 2021, 373, 1494(★ · 85 · 88 · 89 — 이 편 쓰임 서론 [2,3] · "potentiostatic hold (also known as float test …) protocol[3,6]" — 재지목 안 함) · [5] Zuo T.T., Rueß R., Pan R., Walther F., Rohnke M., Hori S., Kanno R., Schröder D., Janek J. *Nat. Commun.* 2021, 12, 6669(★★ · 85 — **재지목**: 분해 개시 3.58 V · 정전위 유지 + EIS 선행 · "classical time dependency models"[5,37]) · [8] Walther F., Koerver R., Fuchs T., Ohno S., Sann J., Rohnke M., Zeier W.G., Janek J. *Chem. Mater.* 2019, 31, 3745(★★ · 82 · 86 · 87 — **재지목**: 계면층 · 노화 상관 [7,8] · 셀 계 "known degradation mechanisms"[8,15,18]) · [37] Wenzel S., Sedlmaier S.J., Dietrich C., Zeier W.G., Janek J. *Solid State Ionics* 2018, 318, 102(★ · 46 · 73 — **재지목**: 시간 의존 성장 모형 [5,37]).
- **앞 호 후속 절에 올랐으나 원장 행 0 — 지목 누락**: **[34] Hori S., Kanno R., Sun X., Song S., Hirayama M., Hauck B., Dippon M., Dierickx S., Ivers-Tiffée E. *J. Power Sources* 2023, 556, 232450**(11호 §20 후속 ★★★ 2 순위 — "같은 재료계 EIS–DRT, 봉우리 귀속의 외부 검증" · 이 편 P_A · P_D 배정의 근거).
- **원장 · 위키 둘 다 없음 · 우리 축**: [13] Hartel J., Banik A., Ali M.Y., Helm B., Strotmann K., Faka V., Maus O., Li C., Wiggers H., Zeier W.G. *Chem. Mater.* 2024, 36, 10731(같은 연구실 · NCM83 + Li₅.₅PS₄.₅Cl₁.₅ · 3.7 V 개시 · 장기 사이클 검증 인용) · [15] Zuo T., Walther F., Teo J.H., Rueß R., Wang Y., Rohnke M., Schröder D., Nazar L.F., Janek J. *Angew. Chem. Int. Ed.* 2023, 62, e202213228(3.58 V 개시 · 장기 사이클) · [14] Riegger L.M., Mittelsdorf S., Fuchs T., Rueß R., Richter F.H., Janek J. *Chem. Mater.* 2023, 35, 5091(SSB calendar 프로토콜 선행 넷 중 하나) · [7] Schulze M.C., Rodrigues M.-T.F., McBrayer J.D., Abraham D.P., Apblett C.A., Bloom I., Chen Z., Colclasure A.M., Dunlop A.R., Fang C., Harrison K.L., Liu G., Minteer S.D., Neale N.R., Robertson D., Tornheim A.P., Trask S.E., Veith G.M., Verma A., Yang Z., Johnson C. *J. Electrochem. Soc.* 2022, 169, 050531(정전위 유지의 한계 — 액체 · 이 편이 "critical study on different LIB systems" 로 부름) · [12] Schulze M. 외 NREL Silicon Consortium "Calendar Aging Electrochemical Screening Protocol 1.2"(웹) · [19] Kalaga K., Rodrigues M.-T.F., Trask S.E., Shkrob I.A., Abraham D.P. *Electrochim. Acta* 2018, 280, 221("high C-rate (1C) cycling approach" 의 인용처) · [30] Huang J., Sullivan N.P., Zakutayev A., O'Hayre R. *Electrochim. Acta* 2023, 443, 141879(hybrid-drt · 위키 액체 갈래 su2024 digest 가 본문에서 언급 — 후속 절 0) · [29] Huang J.D., Meisel C., Sullivan N.P., Zakutayev A., O'Hayre R. *Joule* 2024, 8, 2049 · [31] Lu Y., Zhao C.-Z., Huang J.-Q., Zhang Q. *Joule* 2022, 6, 1172(τ 대역 배정의 주 근거) · [32] Whang G., Huang J., Pham P.N.L., Kraft M.A., Zeier W.G. *ACS Electrochem.* 2024, 1, 249(같은 연구실 · In/InLi 전류 분포 · P_SE) · [28] Dierickx S., Weber A., Ivers-Tiffée E. *Electrochim. Acta* 2020, 355, 136764(ECM 모호성) · [35] Jeong W.J., Wang C., Yoon S.G., Liu Y., Chen T., McDowell M.T. *ACS Energy Lett.* 2024, 9, 2554 · [36] Vishnugopi B.S., Naik K.G., Kawakami H., Ikeda N., Mizuno Y., Iwamura R., Kotaka T., Aotani K., Tabuchi Y., Mukherjee P.P. *Adv. Energy Mater.* 2023, 13, 2203671(음극 접촉 손실 · void 기구 인용) · [23] Zhu J., Dewi Darma M.S., Knapp M., Sørensen D.R., Heere M., Fang Q., Wang X., Dai H., Mereacre L., Senyshyn A., Wei X., Ehrenberg H. *J. Power Sources* 2020, 448, 227575("loss of lithium inventory in the CAM" 의 인용처 — 셀 계 미인쇄).
- 서술 배경(우리 축 밖 · 행 없음): [1] Kamaya 2011 · [2] Krauskopf … Janek 2020 *Chem. Rev.* · [4] Janek & Zeier 2023 *Nat. Energy* 8, 230(15 · 36 · 60호 digest 의 인용 표에만 — 36호는 등급 칸 없는 후속 표) · [6] Famprikis 2019 *Nat. Mater.* · [9] Che 2023 *EES* · [10] Diao 2019 *JPS* · [16] Yang R. 2024 *Appl. Therm. Eng.* · [17] Li Y. 2025 *Mater. Horiz.* · [18] Tan D.H.S. … Meng 2019 *ACS Energy Lett.* 4, 2418(86 · 87 · 73호 참고문헌 절) · [20] Schomburg 2024 *EES* · [21] Weng … Stefanopoulou 2023 *JES* · [22] Kim J. … Yoon W.-S. 2023 *Cell Rep. Phys. Sci.* · [24] Van der Ven 2022 *Battery Energy* · [25] Zhang W. … Janek 2018 *ACS AMI* 10, 22226(우리 63호 Zhang W. 2017 *ACS AMI* 와 다른 편 — 제목 미인쇄) · [26] Zhu Y., He X., Mo Y. 2015 *ACS AMI*.
- ⚠ **이름 겹침**: [11] Huo D. 2025 ≠ 89호 [12] Huo H. & Janek 2022 ≠ 원장 Huo H. … Janek 2024 *Nat. Mater.* · [25] Zhang W. 2018 *ACS AMI* 10, 22226 ≠ 63호 Zhang W. 2017 *ACS AMI* · [27] = 23호(*Chem. Mater.*) ≠ 64호 Koerver 2017 *JMCA* · [33] 의 "Yu" = Yu C.-Y.(11호) — 우리 액체 갈래 다른 Yu 와 무관.

# 인용 대조 — 이 편이 인용한 편 중 우리 위키가 기록을 가진 것

| 이 편 | 이 편의 쓰임 | 위키 기록(digest 전사 · 원전 재열람 0) | 대조 |
|---|---|---|---|
| [27] Koerver 2017 *Chem. Mater.*(23호) | "the increased cathode–electrolyte interfacial resistance may also be contributed by the contact loss between them" | 23호: 접촉 손실 → 용량 손실은 서술 · 용량 몫 미정(카드 Evidence 열아홉 번째) · 23호 음극 호 C 0.5–6.4 mF cm⁻² | ✅ 같은 층위(서술)로 옮김 — 이 편도 몫을 정하지 않는다 |
| [33] Yu 2024(11호) | P_C1 · P_C2 τ 대역 근거 | 11호 P3 ≈500 Hz · P3 에 양 · 음극 함께 | ⚠ τ 값 불일치(D20) |
| [11] Huo 2025(9호) | ① SSB 노화 연구 부족 ② Hartel 3.7 V | 9호 셀 · 내용 | ① 보류 ② ❌ 번호 오기(D4) |
| [5] Zuo 2021 | 분해 개시 · 정전위 유지 + EIS 선행 · 시간 모형 | 85호 후속 ★★(계면 호 배정 기둥) · 원장 ★★ | 재지목 |
| [8] Walther 2019 | 계면층 · 노화 상관 · 셀 계 기구 | 82 · 86 · 87호 후속(계면층 배정 원전) · 원장 ★★ | 재지목 |
| [37] Wenzel 2018 | "classical time dependency models" | 46 · 73호(Li \| 아지로다이트 계면층 성장) · 원장 ★ | 재지목 — 양극 쪽 유지 데이터에 Li 금속 계면층 성장 법칙을 대는 쓰임 `[해석]` |
| [34] Hori 2023 | P_A(음극 CT) · P_D(확산) 배정 | 11호 후속 ★★★ · 원장 행 0 | 지목 누락 |
| [30] Huang 2023 | DRT 방법(hybrid-drt) | su2024(액체) 본문 언급 "How reliable is DRT analysis?" | 후속 절 0 · 새 행 후보 |

⚠ 이 편은 우리 3전극 계열(17 · 18 · 19 · 21 · 40 · 41 · 45 · 46 · 48호 — 16호는 이 편 뒤 2026)을 하나도 인용하지 않는다 — 귀속에 쓸 수 있는 전극 분해 선례가 인용 그물 밖에 있다.

# 곱 축퇴 처방 — 일흔세 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

- **입력 점검**: **1단계(`R` · `C`) — ✅ 우리 `[재현]`**: 예치 DRT(시간분해 261 + 형성 · RPT 8)에서 봉우리마다 R(골–골 ln τ 적분)과 τ_peak 를 읽어 C_eff = τ/R 를 냈다(저자 인쇄 C 값 0) · **2단계(면적 대조군) ❌** — 면적 · CAM 표면적 · 입도 0 · **3단계-a(Ea) ❌** — 25 ℃ 한 점 · **3단계-b(C 상한) ✅ 우리 적용** — P_C ≈1.6–6.6 µF(기하 2–8 µF cm⁻² — 이중층 자릿수 ✓) · P_A ≈1.5–3.3 mF(기하 1.9–4.2 mF cm⁻² — 이중층의 ×190–520 ❌ "전하 이동" 이름표 불통과) · P_D ≈0.04–0.14 F(화학 용량 ✓) · **4단계(시간 영역 · 같은 시편) — 부분** — 같은 셀 시간분해(유지 매 시간 · 1C 두 사이클마다)는 있으나 두 프로토콜의 측정 상태가 다르고(유지 전위 ↔ 1C 방전 끝) cycle 쪽은 상태가 표류.
- **1단계 판독(전제 C ∝ 면적)**: calendar 유지 — τ ×5.7–35 · R ×4–27 · **C 평탄(1.6–2.5 µF)** ⇒ **저항형**(계면층 · `j₀` 쪽) — 면적 손실이면 C 가 같이 줄어야 한다 · 64호 사이클 축 "노화분 = 저항형"(4.6 · 5.0 V)과 같은 방향. cycle P_C1 — **R ↓(×0.52–0.76) · C ↑(×1.5–1.9) · τ ≈ 일정** ⇒ **면적 증가형 서명**(활성화 · 젖음 `[해석]`) — 또는 1C 방전 끝 상태 표류의 `j₀(x)` · 화학 용량 몫(가르지 않음). cycle P_A — C 가 mF 라 1단계 전제(C = 이중층 ∝ 면적) 자체가 서지 않는다.
- **처방 표 후보 줄(새 줄 아님 — 후보)**: **"DRT 봉우리별 C_eff 연속성 검사"** — 봉우리가 τ 창을 넘어 이동할 때 C_eff 가 평탄하면 같은 요소의 R 성장(이름 유지 정당), 자릿수가 바뀌면 다른 요소(이름 재검토) — 이 편: 이동하는 calendar 봉우리 µF 평탄 ↔ 같은 τ 대역 cycle P_A mF. 3단계-b(C 상한)를 봉우리 이름표 검사에 쓰는 형태이고, 84호 (피)(창 밖 봉우리 표기)와 짝이다.
- **곱 문장(`[인쇄]` → `[해석]`)**: "increased cathode–electrolyte interfacial resistance may also be contributed by the contact loss between them[27]" · "irreversible loss of cyclable lithium into building up resistive cathode–electrolyte interphase layer … may also cause chemomechanical degradation … cracking or contact loss due to volume expansion from overcharging" — 계면층(`j₀` 쪽)과 접촉 면적(`A` 쪽)을 **한 저항 이름(P_C)** 에 함께 담고 가르지 않는다. 한 손잡이(컷오프)가 계면층 구동력 · 탈리튬 깊이(부피 변화) · 측정 상태를 함께 움직인다.
- ⚠ **이것이 곱을 푼 것은 아니다** — C_eff 는 우리 판독(골–골 적분 · 창 경계 선택에 ±≈30 % 흔들림 — P_A 1.5 ↔ 3.3 mF)이고, 면적 대조 · 온도 · 3전극이 없다. 판독이 주는 것은 "유지 노화의 지배 성장이 면적형이 아니다" 라는 **전제 위 방향**까지다.

# 보류 결정 (가)–(히) · (개)–(해) · (게) · (네) · (데) — 이 편이 주는 근거 (결정 안 함)

원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 와 대조(읽기만). **결정은 사용자 몫이고, 이 편은 근거 유무만 표시한다.**

| # | 근거 | 내용 |
|---|---|---|
| **(네)** 유지율 · "80 % 도달 사이클" 인용 규칙 | **근거(강)** | 손실 % 의 **기준 사이클**이 결과를 ×3 바꾸는 표본 — 지면 정의(3번째 형성)와 달리 cycle 3.9 · 4.1 V 인쇄값은 첫 형성 기준으로만 재현(9.80 · 9.29 ↔ 3번째 기준 2.99 · 2.83 % 손실) · RPT 1 → 3 회복 +0.7 · +2.1 %(calendar) · 형성 연속 감쇠 −1.6 ~ −3.0 %/사이클 — 기준 사이클 · 비교 사이클 · 회복을 값 옆에 적어야 하는 표본 |
| **(대)** C-rate 기준 용량 표기 | **근거(강)** | **기준이 인쇄된 쪽 끝** — "theoretical specific capacity of NCM83 … 200 mAh g⁻¹ as basis of calculation for charge and discharge current" · `[데이터]` 1C = 199.6–200.6 mA g⁻¹ ✅ · 그러나 실측 0.1C 용량 ≈117–131 mAh g⁻¹ → 측정 용량 기준 1C ≈1.5–1.7 h⁻¹ · 1C 실용량 47–72 mAh g⁻¹ — "1C" 가 같은 숫자로 89호(함축 기준 셋)와 반대 끝 |
| **(피)** DRT 창 밖 봉우리 표기 | **근거(강)** | P_D(τ ≈10 s)가 τ_max 3.18 s 밖인데 "solid-state lithium diffusion process within the cathode electrode" 이름 · 그림 6d 에서 크기 비교 · `[재현]` 전형 DRT 의 τ > 3.18 s 몫 26 %(257 / 970 Ω) · 저자 스스로 "largely out of the measured frequency range" 인쇄 — 84호에 이은 둘째 표본 |
| **(차)** PyBaMM 면적 / `j₀` 노브 분리 forward | **근거(중)** | 유지 노화의 지배 성장 = C 평탄 · R ↑(저항형 — `[재현]`) ↔ 1C 의 P_C1 = R ↓ · C ↑(면적 증가형) — 같은 셀 계에서 두 노브가 다른 프로토콜에 다르게 찍히는 표본 |
| **(루)** SOC 축 신품 `j₀(x)` 기준선 | **근거(중)** | 유지 1 h 스펙트럼부터 R_tot 0.81 · 3.5 · 9.3 kΩ(3.7 · 3.9 · 4.1 V) — 노화 전 상태 차 ×4–11 이 "시간분해 노화" 의 출발점에 섞인다 · cycle 1C 방전 끝 상태 표류 |
| **(캐)** "stack pressure" 명목 ↔ 계측 표기 | **근거(중)** | **넷째 형태 — 토크 환산 명목**("torque of 10 Nm providing an operating stack pressure of ~50 MPa" · 환산 근거 · 계측 0 · `[재현]` 3.93 kN) |
| **(해)** 운전 압력 값의 출처 층위 표기 | **근거(중)** | 값이 **ESI 에만**(본문 `pressure` 0 회) — 출처 칸에 "ESI · 토크 명목" 을 적어야 하는 표본 |
| **(츠)** CE 결손 → LLI 배정 전 구조 채널 대조 | **근거(중)** | 유지 손실을 "irreversible loss of cyclable lithium" 으로 읽는다 · RPT CE > 100 % · 1C 뒤 RPT1 초과 반환 +28–32 mAh g⁻¹ — Li 가 음극에 쌓였다가 돌아오는 셀 · 구조 채널 대조 0 |
| **(브)** 실측 LLI 의 정의 표기 | **근거(중)** | "loss of lithium inventory in the CAM"(dQ/dV 세기) = 정의 B(양극 결손) 쪽 · 공칭 재고 ×3.31 이면 정의 A(용량 유효)는 0 일 수 있다 · 접근성 미검사 |
| **(게)** Li 저장고 셀 ICE · CE 인용 규칙 | **근거(중)** | In/InLi 재고 ×3.31(공칭) · InLi-(In) 조립(접근성 미검사) · 첫 형성 CE ≈70 %(S3 `[도표]`) · RPT CE > 100 % — 재고비 · 조립 방향을 값 옆에 |
| **(오)** In 영점 표기 | **근거(중)** | 환산 **0.62 V 인쇄**(4.32 ↔ 3.7 V) · 출처 0 · 조성 28.42 at% 인쇄 — 42호 0.622–0.625 V 띠 안(액체 조건) |
| **(가)** 29호 Q4 +0.5(정적 ↔ 동적 축) | **약** | `[재현·가정]` 50 % SoC ΔV 의 균일 이동이 calendar 손실의 1/8–1/3 — 정적 ↔ 동적 분해가 0.1C RPT 손실의 핵심 축이라는 표본 · 공분산 진단 0 |
| **(나)** 38호 Q2 +0.5(두 채널 설계상 결합) | **약** | ΔV 와 Q_loss 가 같은 곡선 쌍에서 나온 두 수 — "correlation" 이 설계상 결합 |
| **(두)** θ 판정의 시간 궤적 조건 | **약** | RPT 1 → 3 회복(다음 사이클 회복) 표본 · 휴지 30 분 · 그러나 θ 판정 시도 0 |
| **(러)** `θ` → `LAM_PE` 결합 | **약** | "cracking or contact loss due to volume expansion from overcharging" — 결합 서술 · 양 0 |
| **(머)** 64호 후속(Oh 2016 In/LiInₓ 대칭셀) | **약** | 이 편 음극 귀속에 대칭셀 0 — 요청 동기 +1 |
| **(저)** 첫 충전 상한 검사 | **약** | 첫 형성 충전 194.0 mAh g⁻¹(`[데이터]`)·S3 ≈197 ≪ 이론(NCM83 ≈275 `[재현·외부 값]`) — 무조건 통과 |
| **(도)** 첫 사이클 CE 결손의 정체 | **약** | 첫 형성 CE ≈70 %(결손 ≈59 mAh g⁻¹ `[도표]`) — 논의 0 |
| **(므)** "읽기 쪽 기준(LLI 영점)" | **약** | 형성 연속 감쇠 · 공칭 재고 — 영점이 움직이는 표본 |
| **(주)** "X-limited" 판정 기준 | **약** | "the high-current cycling approach is mainly inhibited by kinetic limitations" · "dominant degradation mechanism" — 순위 · 문턱 · 시간 기준 0 |
| **(히)** 구성 교체형 전극 몫 배정 표기 | **약** | 반대쪽 끝 — 구성 교체 0 · τ 창만으로 전극 몫 배정 |
| **(티)** 25호 ref 23(84호) 배정 근거 | **약** | 같은 τ 창 배정 관행 · 84호는 구성 교체로 갈랐다 — 이 편은 안 갈랐다 |
| **(너)** 셀 면적 조건부 값 | **약(표본)** | ∅1 cm 집전체 인쇄 → 0.785 cm² · 1.783 mAh cm⁻² 와 폐합 ✅ — 면적 인쇄 표본 +1 |
| **(처)** 한 손잡이 여러 노브 | **정성 메모** | 컷오프 = 계면층 구동력 · 탈리튬 깊이 · 고전위 체류 · EIS 측정 상태를 함께 움직인다 |
| (라)(마)(바)(사) | 결정 · 반영됨 | — |
| 나머지(다 · 아 · 자 · 카 · 타 · 파 · 하 · 거 · 더 · 버 · 서 · 어 · 커 · 터 · 퍼 · 허 · 고 · 노 · 로 · 모 · 보 · 소 · 조 · 초 · 코 · 토 · 포 · 호 · 구 · 누 · 무 · 부 · 수 · 우 · 추 · 쿠 · 투 · 푸 · 후 · 그 · 느 · 드 · 르 · 스 · 으 · 즈 · 크 · 트 · 프 · 흐 · 기 · 니 · 디 · 리 · 미 · 비 · 시 · 이 · 지 · 치 · 키 · 개 · 내 · 래 · 매 · 배 · 새 · 애 · 재 · 채 · 태 · 패 · 데) | **근거 0** | 압력 조작 · 저압 · 측면 · 영상 · 모형 · 입도 · Ea · 문헌 표 0 · 13호 가닥 무관 |

## 새 판단 거리 (셋 — 글자는 호출자가 붙인다)

1. **노화 프로토콜 비교의 정규화 축 표기** — calendar ↔ cycle(또는 두 노화 프로토콜) 비교를 카드 · 원장 · 개념 · 합성 truth 설계에 옮길 때 무엇으로 맞췄는지(명목 시간 · 상한 체류 · 충전 깊이 · 통과 전하 · 휴지 · EIS 시간)와 시간 축에 휴지 · EIS 가 들어갔는지를 값 옆에 적게 할지 — 이 편: 명목 48 h 만 · 상한 체류 48 h ↔ ≈0 h · 통과 전하 ≈300 ↔ ≈9,000–10,000 mAh g⁻¹ · 탈리튬 깊이 ×1.6–1.8 · 시간 축이 휴지 ≈19–20 h 를 뺀다.
2. **예치 원자료의 교차 폐합 · 중복 검사 규칙** — 논문의 원자료(ZIP · 저장소)를 재현 · truth 입력에 쓰기 전에 그림 사이 폐합(같은 셀 · 같은 사이클의 용량이 그림마다 같은가) · 시계열 중복(한 셀 구간이 다른 셀로 복사됐는가) · 번호 정합(사이클 · 스펙트럼 수)을 먼저 검사하고 결과를 digest 에 적게 할지 — 이 편: 4.1 V calendar RPT = 3.9 V 복사 · 여섯 셀 중 셋만 폐합 · 사이클 80 ↔ 78 · 76.
3. **시간분해 EIS 의 측정 상태 표기** — 시간분해 · 노화 전후 EIS 값을 옮길 때 측정 상태(유지 전위 · 방전 끝 · SOC · 휴지 길이)와 그 상태가 시계열 동안 고정됐는지, 비교 기준선이 같은 셀인지를 값 옆에 적게 할지 — 이 편: 유지 전위 ↔ 표류하는 1C 방전 끝 · 공통 기준 스펙트럼(셀 간 산포 694–1019 Ω) — (루)(피)와 묶어도 된다.

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것, 그리고 인용

| # | 등급 | 내용 | 자리 |
|---|---|---|---|
| **D1** | ★★★ | `[데이터]` 그림 2 자료 "4.1 V calendar aging.txt" 의 RPT 구간(103.504–128.881 h) **9,794 연속 표본이 "3.9 V calendar aging.txt"(104.377–129.754 h)와 전위 · 시간 증분이 같다**(Δt 0.8732 h · 증분 차 ≤3×10⁻¹⁴ h · 다른 30 쌍 중복 0) · 원본은 3.9 V 쪽(그림 3 RPT3 충전 모양 차 4.7 ↔ 15.0 mV · 그림 3 의 4.1 V RPT3 73.80 · 75.11 mAh g⁻¹ ↔ 복사 구간 @20 mA g⁻¹ 86.1 · 87.3) — 그림 2a · S1a 4.1 V 판의 RPT 세 사이클이 3.9 V 셀의 것으로 읽힌다 · 본문 "(1) … increasing cut-off potentials resulted in decreasing post-aging cycle times" 를 3.9 ↔ 4.1 V 에서 이 그림으로 읽을 수 없다 | 그림 2a · S1a · 자료 |
| **D2** | ★★★ | Q_loss 기준 — 식 (1) "Q_last formation discharge" · 본문 "the last (3rd) formation cycle … nominal pristine" ↔ `[데이터]` 그림 2 ↔ 3 이 닫히는 cycle 3.9 · 4.1 V 에서 인쇄 9.80 · 9.29 % 는 **첫 형성 방전 기준**(9.69 · 9.32 %)으로만 재현 · 3번째 기준이면 2.99 · 2.83 % · calendar 4.1 V 도 첫 형성(f = 20 가정) 43.50 ↔ 인쇄 43.56 · calendar 3.9 V 는 3번째 기준 32.17 ↔ 인쇄 32.71(0.54 %p) — 한 정의로 닫히지 않는다 | 식 (1) · 그림 3e · f · 자료 |
| **D3** | ★★★ | 그림 6 "before aging" = 한 스펙트럼(그림 4 와 같은 파일 내용 · Re(50 mHz) 719.5 Ω)을 여섯 셀 공통 기준으로 ↔ S4 신품 열 694–1019 Ω(`[도표·화소]`) · 자기 셀 대비 cycle 저주파 Re −40 · −30 · −4 Ω — 본문 "cycle aged cells (Fig. 6d) only show a slight increase … a larger contribution from PA" 는 다른 셀 대비 | 그림 6 · S4 |
| **D4** | ★★ | "Hartel et al., … exceeded 3.7 V vs. In/InLi,¹¹" — [11] = Huo D. 2025 *JPS*(9호: NCM811(H₃BO₃) \| LPSCl \| Li₃.₇₅Si · `indium` 0) · Hartel = [13] · p. 3 같은 문턱엔 [5,13,15] — 번호 오기로 읽힌다(`[해석]` · 위첨자 화면 확인) | p. 5 |
| **D5** | ★★ | "oxygenated decomposition species such as sulfites/sulfates, phosphates, O₂ and SO₂.⁷" — [7] 은 이 편 자신이 "a critical study on different LIB systems"(정전위 유지 · 액체)로 부르는 편 — 황화물 SE–CAM 계면 산소 종의 근거로 쓰임이 어긋난다(`[해석]` · [7] 원문 미열람) | p. 5 |
| **D6** | ★★ | 그림 3f(cycle) "Pristine" ΔV 0.16 V(표 f) ↔ `[재현]` 같은 판 before 곡선 0.177 V(0.18) — 0.16 은 calendar before(0.162)의 값 | 그림 3e · f · 표 |
| **D7** | ★★ | 사이클 번호 — 그림 5 · 7 색 막대 78 · 76 · 74 ↔ `[데이터]` 그림 2 1C 충전 80 · 80 · 74 · 그림 7 3.7 V 파일 c01–c74 + c78(c75–c77 없음 · c78 = 시계열 76번째) · 시계열 끝 넷(3.7 V 52.3 · 56.6 · 51.0 · 45.8 mAh g⁻¹)은 그림 7 밖 · S9 4.0 V 색 막대 **70** ↔ S6 · S8 · S13 **68** | 그림 5 · 7 · S6 · S8 · S9 · S13 · 자료 |
| **D8** | ★★ | 시간 축 — 그림 1 · 2 · S1 · 자료의 시간이 휴지 · EIS 를 뺀다(`[데이터]` 방전 끝 이완이 같은 시각 값으로 기록 · 유지 구간 정확히 48.00 h · 1C 3.9 V 는 두 사이클 주기로 충전 용량 엇갈림) ↔ ESI "rested at OCV for 30 minutes" before EIS — 캡션 미표기 · 1C 구간 "48 h" 는 CC 시간 | 그림 1 · 2 · S1 |
| **D9** | ★ | 그림 6a · b · S4 Nyquist 곡선이 세로로 쌓여 있다(어긋남 ≈0.18 kΩ · ≈110 Ω) — 캡션 표기 0(S7 캡션만 "stacked at arbitrary constant offsets") | 그림 6 · S4 |
| **D10** | ★ | p. 1 띠 기사 유형 "REVIEW" · 쪽 머리 "Review" ↔ 내용은 1차 실험 편(서론 · 결과 · 결론 · ESI 실험) | p. 1–10 |
| **D11** | ★ | 축 · 열 이름 "V vs. In/LiIn"(S2 · 자료 dQ/dV 머리) ↔ 본문 "In/InLi" | S2 · 자료 |
| **D12** | ★ | 오기 — "PC1 (τ ∼10⁻³ to 10⁻²)" 단위 s 누락 · "4.62" 단위 누락 · ESI "7 MHz–50 mHz Hz" · "potential static hold"(p. 3 — potentiostatic) · [32] "M. A. Kraand"(텍스트 층 합자 소실 — "Kraft and") · 본문 "eﬃciently" 류 합자 소실 다수(텍스트 층) | p. 3 · 5 · ESI · 참고문헌 |
| **D13** | ★★ | "The DRT in this work generally indicates five main peaks" ↔ `[데이터]` 전형 DRT(그림 4) 국소 극대: 1.38×10⁻⁸(P_SE) · 7.9×10⁻⁷(이름 없는 작은 봉우리 4.4 Ω) · 9.1×10⁻³(P_C) · 0.74(P_A) · 10.5 s(P_D) — **P_C2 는 극대가 아니라 어깨** · P_D 는 창 밖 · 창 밖 몫 26 % | 그림 4 · 자료 |
| **D14** | ★★ | P_A 창 `[인쇄]` "PA (τ ∼10⁻¹ to 1 s)" ↔ `[데이터]` 3.9 · 4.1 V 유지 48 h 지배 봉우리("P_C") τ 0.19 · 0.54 s — 이름은 2D 연속성으로 유지(우리 C_eff 평탄으로는 지지 — §(c)) | 그림 5a · S6a |
| **D15** | ★★ | 그림 2 ↔ 그림 3 불폐합 — 3.7 V calendar(그림 2 RPT3 @20 mA g⁻¹ 108.5 · 103.6 ↔ 그림 3 113.63 · 113.69 · 충방 비 4.6 % 불일치) · 3.7 V cycle(132.6 · 132.8 ↔ 128.24 · 127.16 · 1.0 %) — 같은 이름 셀의 같은 사이클로 볼 수 없다(반복 셀 존재 여부 미인쇄) | 그림 2 · 3 · 자료 |
| **D16** | ★ | "Before aging" 처리 — 그림 3 은 두 판에 **다른 곡선**(130.75/129.13 ↔ 130.05/128.45) · 그림 6 은 두 판에 **같은 스펙트럼** — 기준선 규칙이 그림마다 다르다 | 그림 3 · 6 · 자료 |
| **D17** | ★★ | 유지 사이클 방전 — S12a 3.7 V ≈144 · S12e 4.1 V ≈131 mAh g⁻¹(`[도표]` · S14 막대와 정합) ↔ `[데이터]` 그림 2 의 3.7 · 4.1 V 유지 뒤 방전 138.5 · 144.5 mAh g⁻¹ @20 mA g⁻¹(4.1 V 모양도 다름: 자료 2.86 → 3.01 V ↔ S12e ≈2.6 → 2.87 V) · 3.9 V 는 135.1 ↔ ≈135 ✅ | S12 · S14 · 그림 2 |
| **D18** | ★ | 3.7 V calendar 둘째 RPT 방전 끝 0.48 h 자료 공백(113.80 → 114.28 h · 2.0035 → 2.040 V) — 그림 2a · S1a ≈114 h 의 홈 | 그림 2a · S1a · 자료 |
| **D19** | ★★ | 본문 "calendar aged cells (Fig. 6c) show a noticeable domination of PC that increases gradually with increasing cut-off potential" ↔ S10c 다섯 컷오프: P_C 3.8 V ≈189 > 3.9 V ≈175 · 4.0 V ≈333 > 4.1 V ≈313 Ω `[도표]` — 단조는 본문 세 컷오프 선택에서만 | p. 7 · S10 |
| **D20** | ★ | [33](11호) 을 P_C1 · P_C2 τ 대역(10⁻³–10⁻¹ s)의 근거로 ↔ 11호 양극 봉우리 P3 ≈500 Hz → τ ≈3.2×10⁻⁴ s(`[재현]` · 11호 digest 전사) | p. 5 |
| **D21** | ★ | 용어 — 서론의 calendar 정의(장기 보관 · OCV ↔ RPT 교대[7]) ↔ 실제 프로토콜(상한 정전위 유지) — 본문이 "qualitative accelerated tool" 로 명시는 함 | p. 1–2 |

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. **"calendar aging" = 상한 정전위 유지(float) 48 h** 이고, cycle 과는 **명목 시간만** 맞췄다 — `[데이터]` 상한 체류 48 h ↔ ≈0 h · 통과 전하 ≈1/30 · 탈리튬 깊이 ×1.6–1.8. "calendar 가 더 나쁘다" 는 그 조건부 명제다(새 판단 거리 1).
2. **DRT 귀속 — calendar 는 조건부 성립 · cycle 은 가정 의존.** 우리 `[재현]` C_eff 가 처음으로 두 τ-겹침 요소를 가른다(µF 평탄 ↔ mF) — calendar 의 "P_C 연장" 해석을 지지하고, cycle 의 "음극 CT" 이름표는 C 상한에서 서지 않는다(23 · 84호와 같은 형태). [[drt-peak-count-nonidentifiability]] 일곱 번째 경보 · 곱 축퇴 처방 후보 줄.
3. **기준선 · 상태 문제** — 그림 6 의 공통 기준 스펙트럼 · 1C 방전 끝 표류 · 유지 전위의 상태 효과 — "시간분해 EIS 노화" 를 옮길 때 측정 상태와 기준 셀을 붙여야 한다(새 판단 거리 3).
4. **Q7 — In/InLi 공칭 재고 ×3.31 · InLi-(In) 조립** — LLI 가 용량에 보이는지 판정 불가(원천 역할 미검사) · 저자의 "lithium inventory" 해석은 검사되지 않은 가설 — 이식 메모 M3 의 필요를 다시 보인다.
5. **0.1C RPT 는 우리 OCV 하네스 입력이 아니다** — 50 % SoC ΔV 의 균일 이동만으로 손실의 1/8–1/3, 나머지는 열역학 ↔ SOC 의존 동역학 미분리 · 합성 truth 에 정전위 유지를 넣으려면 R_int(t, V) 와 준평형 RPT 가 먼저다.
6. **자료 무결성** — 예치 ZIP 의 4.1 V calendar RPT 복사 · 세 셀 불폐합 · Q_loss 기준 불일치 — 원자료를 truth 입력으로 쓰기 전 교차 폐합 검사(새 판단 거리 2).
7. **인용 그물** — 9호 인용 둘 중 하나는 번호 오기 · 11호 인용은 τ 값과 안 맞음 · 23호 인용은 같은 층위(서술) · 우리 3전극 계열 인용 0 · **Hori 2023(지목 누락)** 이 귀속 외부 검증의 공통 후보.

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 서지(`[인쇄]` 참고문헌 그대로) | ref | 지목(이 편 포함) | 왜 | 축 | 우선 |
|---|---|---|---|---|---|
| **S. Hori, R. Kanno, X. Sun, S. Song, M. Hirayama, B. Hauck, M. Dippon, S. Dierickx, E. Ivers-Tiffée, *J. Power Sources*, 2023, 556, 232450** | [34] | **11 · 90 = 2 — 지목 누락(11호 §20 ★★★ · 원장 행 0)** | 이 편 P_A(음극 CT) · P_D(양극 확산) 배정의 근거 · 같은 재료계(황화물 + In–Li) EIS–DRT 를 Ivers-Tiffée 그룹이 — 11호 · 이 편 귀속을 함께 외부 검증할 공통 원전 | Q2 · Q5 · DRT | ★★★ |
| **J. Hartel, A. Banik, M. Y. Ali, B. Helm, K. Strotmann, V. Faka, O. Maus, C. Li, H. Wiggers, W. G. Zeier, *Chem. Mater.*, 2024, 36, 10731–10745** | [13] | 90 = 1 | 같은 연구실 · NCM83 · Li₅.₅PS₄.₅Cl₁.₅ · "3.7 V vs In/InLi 개시" · 장기 사이클의 계면 저항 — 이 편 "선별 ↔ 장기" 검증 주장의 같은 계열 대조(유일) | (a) · 컷오프 · 계면층 | ★★★ |
| **T. T. Zuo, R. Rueß, R. Pan, F. Walther, M. Rohnke, S. Hori, R. Kanno, D. Schröder, J. Janek, *Nat. Commun.*, 2021, 12, 6669** | [5] | **85 · 90 = 2**(원장 ★★ — 재지목) | 3.58 V 분해 개시 · 정전위 유지 + 주기 EIS 의 선행("20–30 hours") · "classical time dependency models"[5,37] | (a) · 계면층 · R(t) | ★★ |
| **T. Zuo, F. Walther, J. H. Teo, R. Rueß, Y. Wang, M. Rohnke, D. Schröder, L. F. Nazar, J. Janek, *Angew. Chem., Int. Ed.*, 2023, 62, e202213228** | [15] | 90 = 1 | LPSCl · Li₅.₅PS₄.₅Cl₁.₅ \| NCM85 계면 3.58 V 개시 · 장기 사이클 계면 저항(검증 인용 [13,15]) | 컷오프 · 계면층 | ★★ |
| **M. C. Schulze, M.-T. F. Rodrigues, J. D. McBrayer, D. P. Abraham, C. A. Apblett, I. Bloom, Z. Chen, A. M. Colclasure, A. R. Dunlop, C. Fang, K. L. Harrison, G. Liu, S. D. Minteer, N. R. Neale, D. Robertson, A. P. Tornheim, S. E. Trask, G. M. Veith, A. Verma, Z. Yang, C. Johnson, *J. Electrochem. Soc.*, 2022, 169, 050531** | [7] | 90 = 1 | 정전위 유지가 감쇠 속도를 정량 예측하지 못한다는 비판적 원전(액체) — 이 편 "qualitative" 한정의 근거 · D5 대조처 | 노화 프로토콜 | ★★ |
| **J. Huang, N. P. Sullivan, A. Zakutayev, R. O'Hayre, *Electrochim. Acta*, 2023, 443, 141879** | [30] | 90 = 1 | hybrid-drt(계층 베이즈 · 자동 조율) 원전 — λ 를 "고르지 않는" 역변환의 사전 · 초모수 · 불확실성 출력 여부 | DRT 식별성 | ★★ |
| **Y. Lu, C.-Z. Zhao, J.-Q. Huang, Q. Zhang, *Joule*, 2022, 6, 1172–1198** | [31] | 90 = 1 | τ 대역 → 과정 배정의 주 근거(P_SE · P_C · P_A) — 대역이 어떤 셀 · 상태에서 나왔는지 | DRT 귀속 | ★★ |
| **G. Whang, J. Huang, P. N. L. Pham, M. A. Kraft, W. G. Zeier, *ACS Electrochem.*, 2024, 1, 249–262** | [32] | 90 = 1 | 같은 연구실 · In/InLi 전류 분포 → 불균일 리튬화 · P_SE 배정 — cycle "음극 계면" 가설의 근거 | Q5 · DRT | ★★ |
| **F. Walther, R. Koerver, T. Fuchs, S. Ohno, J. Sann, M. Rohnke, W. G. Zeier, J. Janek, *Chem. Mater.*, 2019, 31, 3745–3755** | [8] | **82 · 86 · 87 · 90 = 4**(원장 ★★ — 재지목) | 계면층 배정 원전 · 이 편 셀 계 "known degradation mechanisms" | Q1 · Q8 | ★ |
| **S. Wenzel, S. J. Sedlmaier, C. Dietrich, W. G. Zeier, J. Janek, *Solid State Ionics*, 2018, 318, 102–112** | [37] | **46 · 73 · 90 = 3**(원장 ★ — 재지목) | 시간 의존 계면층 성장 법칙 — 정전위 유지 R(t) 를 truth 에 넣을 때의 함수형 후보(Li \| 아지로다이트 원 맥락) | R(t) · truth | ★ |
| **L. M. Riegger, S. Mittelsdorf, T. Fuchs, R. Rueß, F. H. Richter, J. Janek, *Chem. Mater.*, 2023, 35, 5091–5099** | [14] | 90 = 1 | SSB calendar 프로토콜 선행 넷 중 하나 — 개회로 보관 ↔ 유지 비교의 선례 여부 | (a) | ★ |
| K. Kalaga, M.-T. F. Rodrigues, S. E. Trask, I. A. Shkrob, D. P. Abraham, *Electrochim. Acta*, 2018, 280, 221–228 | [19] | 90 = 1 | "high C-rate (1C) cycling approach" 의 출처 — 1C 를 cycle 노화 대리로 쓴 근거(셀 계 미인쇄) | (a) | ☆ |
| J. Zhu, M. S. Dewi Darma, M. Knapp, D. R. Sørensen, M. Heere, Q. Fang, X. Wang, H. Dai, L. Mereacre, A. Senyshyn, X. Wei, H. Ehrenberg, *J. Power Sources*, 2020, 448, 227575 | [23] | 90 = 1 | dQ/dV 세기 → "loss of lithium inventory in the CAM" 해석의 출처(셀 계 미인쇄) — 반쪽전지 · 재고 과잉 셀로 옮겨 오는 조건 | Q7 · (브) | ☆ |
| W. J. Jeong, C. Wang, S. G. Yoon, Y. Liu, T. Chen, M. T. McDowell, *ACS Energy Lett.*, 2024, 9, 2554–2563 | [35] | 90 = 1 | 음극 계면 접촉 손실 · void 기구(cycle P_A 가설의 인용) | Q1 음극 | ☆ |
| B. S. Vishnugopi, K. G. Naik, H. Kawakami, N. Ikeda, Y. Mizuno, R. Iwamura, T. Kotaka, K. Aotani, Y. Tabuchi, P. P. Mukherjee, *Adv. Energy Mater.*, 2023, 13, 2203671 | [36] | 90 = 1 | 같은 인용 자리 · 75호 연구실(Mukherjee) | Q1 음극 | ☆ |

지목 누락 검사: 이 편 참고문헌 37 중 **앞 호 후속 절에 ★ 이상으로 올랐으나 원장 §1 행이 없는 편 1 — [34] Hori 2023 *JPS* 556, 232450(11호 §20 ★★★ 2 순위)**. 원장 행이 있는 편: [3] Tan 2021(★ · 85 · 88 · 89 — 이 편 쓰임이 축 밖이라 재지목 안 함) · [5] Zuo 2021(★★ · 85) · [8] Walther 2019(★★ · 82 · 86 · 87) · [37] Wenzel 2018(★ · 46 · 73). **등급 칸 없는 옛 후속 표에만 오른 편 1 — [4] Janek & Zeier 2023 *Nat. Energy* 8, 230(36호 후속 표 "서지 · ref · 왜 · 축" — 원장 행 0 · 누락으로 단정하지 않음 · 이 편 쓰임은 서론 배경이라 재지목 안 함)**. 받은 편: [11] = 9호 · [27] = 23호 · [33] = 11호. **이 편 자체**: 원장 · 위키 지목 0(사용자 직접 공급).

`[해석]` 귀속 축을 닫는 쪽으로 이 편의 인용 그물은 약하다 — 전극 분해(대칭셀 · 3전극 · 구성 교체)를 한 인용이 0 이고, τ 대역의 값 근거([31] · [33] · [34])는 다른 셀 · 상태의 것이다. 같은 연구실의 장기 사이클 대조([13])와 같은 재료계 DRT 외부 검증([34])이 가장 가까운 확인처다.

# 이 digest 가 주장하지 않는 것

- **calendar(정전위 유지)가 더 가혹하지 않다고 하지 않는다** — 같은 명목 시간 · 같은 컷오프 숫자에서 더 가혹하다는 방향은 자료와 양립한다. 주장은 "그 비교가 상한 체류 · 충전 깊이 · 통과 전하로 맞춰지지 않았다" 까지다.
- **cycle 노화에서 음극 계면이 변하지 않았다고 하지 않는다** — 시간분해 P_A 성장은 자료에 있다. 주장은 그 이름표(음극 CT)가 τ 문헌값 가정이고 C 상한을 못 넘으며, 측정 상태가 표류하고, RPT 비교의 기준선이 다른 셀이라는 것까지다(자기 셀 대비 저주파 Re 는 판독 폭 안 · 한 점 요약).
- **그림 2 자료의 4.1 V RPT 복사가 의도적이라고 하지 않는다** — 예치 자료 · 그림의 사실(9,794 표본 동일)까지다. 그림 3 · S12 의 4.1 V 값이 틀렸다고도 하지 않는다(그쪽은 그림 2 자료와 다를 뿐이다).
- **인쇄 Q_loss 가 틀렸다고 단정하지 않는다** — 계산 파일 · 셀별 기준값이 미인쇄이고, 우리가 보인 것은 "지면 정의(3번째 형성)로는 cycle 두 셀이 재현되지 않고 첫 형성으로는 0.1 %p 안에서 재현된다" 까지다(0.1C = 20 mA g⁻¹ 정전류 · 시간 축 CC 충실 · 그림 2 ↔ 3 같은 셀 조건).
- **C_eff 가 이중층이나 화학 용량 그 자체라고 하지 않는다** — τ_peak ÷ 골–골 적분 R 의 판독이고(창 경계 선택에 ±≈30 %), 기하 면적으로만 나눴다(CAM 표면적 미인쇄).
- **[11] · [7] 인용이 틀렸다고 단정하지 않는다** — [11] 은 저자 이름 · 같은 문턱의 다른 자리 인용 · 9호 digest 내용으로 번호 오기로 "읽힌다" 까지이고, [7] 원문은 열지 않았다.
- **In/InLi 뒷면 Li 가 접근 불가라고 하지 않는다** — 21호의 InLi-(In) 관측(다른 셀 · 다른 압력)을 조건으로 적었을 뿐, 이 편 셀은 검사하지 않았다.
- **저장소 DOI 의 자료가 이 ZIP 과 같다고 하지 않는다** — 열람하지 않았다.
- `[도표]` · `[도표·화소]` 값은 판독이고, `[재현·외부 값]`(NCM83 이론 용량 · 이중층 ≈10 µF cm⁻² 기준) · `[재현·가정]`(톤 단위 · RPT1 초과분 = 1C 끝 미반환 Li · 균일 분극 이동)은 크기 검사다.
- 수치는 전부 사본이다 — 정본은 원문 PDF · ESI · 예치 자료. 우리 연구 수치(artifact + `degradation-degeneracy/docs/RESULTS*.md`)와 대조하지 않았다.

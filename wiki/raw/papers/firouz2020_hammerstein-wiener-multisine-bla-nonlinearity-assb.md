---
title: "Firouz Y., Goutam S., Cazorla Soult M., Mohammadi A., Van Mierlo J., Van den Bossche P. 2020 — Block-oriented system identification for nonlinear modeling of all-solid-state Li-ion battery technology (J. Energy Storage 28, 101184)"
source_url: local-upload/52._Block-oriented_system_identification_for_nonlinear_modeling_of_all-solid-state_Li-ion_battery_technology.pdf
source_url_note: "본문 PDF 12 쪽(Elsevier 판 · 인쇄 쪽 1–12 = PDF p. 1–12 · 그림 13 전부 래스터 · 표 0 · 번호 식 35 · 참고문헌 60 — Further reading [24] 포함) 6,118,709 B · 업로드 접두사 430260f1 · 4차 묶음 파일 52 · SI 없음(원문에 보충 언급 0) · 예치 원자료 0 — 자동 크롭 13 전부 봤다 · 그림 2 · 6 · 7 · 8a · 8c · 9 · 12a · 13 은 내장 래스터를 원 해상도로 꺼내 축선 · 격자선 화소로 눈금을 보정해 읽었다(판독 배열 · 재현 코드는 커밋 안 함)"
source_doi: 10.1016/j.est.2019.101184
source_license: "© 2019 Elsevier Ltd. All rights reserved.(p. 1 · XMP prism:copyright) — 오픈 액세스 표기 0 · 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: 9cf5d53f1aea0281d942fb56beb6d2d0acf84ed25eefdfe6927599a12a9f7449
ingested: 2026-10-02
sha256: 9c3b54aa2e21cad1436fcda921dbbfdcd7200f78a4a786b667b79e39622c46f6
---
# 수집 목적

`assb` 섹션 **92호** — **4차 묶음 파일 52**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 둘째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). 닻은 `questions/assb-contact-loss-vs-lampe.md` — 이 편이 걸리는 축은 **Q4(유일성 · 식별성)** 가 중심이고, 저자가 주장하는 "비선형도로 계면 고장 검출" 이 Q1 · Q2 에 무엇을 주는지(또는 안 주는지)가 둘째다.

Vrije Universiteit Brussel(MOBI · SURF) + **Toyota Motor Europe**(셀 개발 · 사사)의 *J. Energy Storage* 2020 편으로, **LiNbO₃ 코팅 LiCoO₂ ‖ 흑연 전고체 코인셀 둘**(1 cm² · 0.55 mAh · 분리막 LiI-Li₂S-P₂S₅ 유리 · **양극층 고체전해질만 다름**: 셀 1 Li₂S-P₂S₅ 유리 "σ₂₅ ≈10⁻⁴ S/cm" ↔ 셀 2 γ-Li₃PS₄ "≈10⁻⁵ S/cm")에 **무작위 위상 다중정현 전류**(33 선 · 4 mHz–1 Hz · 첨두 2.8 mA = 5C · 실현 4 × 주기 6 · 50 % SoC · 60 ℃)를 걸어 **BLA(최선 선형 근사)** 로 선형 FRF 와 비선형 왜곡을 가르고, 셀 2 에 **Hammerstein · Wiener · Hammerstein-Wiener** 블록 지향 모형을 맞춘 뒤 "Hammerstein 함수 = 전하이동 한계 · Wiener 함수 = 물질전달 한계" 로 물리를 배정한 편이다.

들어온 경로: 원장 행(그대로) "★★★ | **Firouz·Goutam·Soult·…·Van den Bossche 2020** — *J. Energy Storage* **28**, 101184 | 26 | 1 | **Q4** | 26호 인용 24편 중 **유일하게 제목에 "system identification"** 이 있는 ASSB 논문 (경험 모델) — **구조적 공백 1번 후보**". 원장 §2 **구조적 공백 1번 = "역문제 · 식별성을 다루는 ASSB 논문"**(28호까지 Q4 0/28 · 29호 반 칸 · 후보 목록 첫째가 이 편). 위키 grep(`101184` · `Firouz` · `Hammerstein` · `block-oriented`): **26호**(Iwakiri 2024 — [17] · Table 1 "Parameter Estimation Yes" 넷 중 하나 "경험식, block-oriented system identification" · 후속 ★★★ "제목에 'system identification' 이 들어간 유일한 인용") · 27호(Sinzig 2024 — "이 편이 인용하지 않는 것" 목록에만) · `log.md`:2087 · 카드:4995(둘 다 26호 항의 후속 나열). **지목은 26호 후속 표 하나(1) — 원장 "26 | 1" 과 일치.** 이 편은 우리 digest 를 하나도 인용하지 않는다(참고문헌 60 전수 대조 — 4차 묶음 13 편 · 앞 호 원전 0).

⚠ **원장 행의 셋째 저자 "Soult"** — PDF 저자 줄 · XMP `dc:creator` · CRediT("M. Cazorla Soult: Resources") 셋 다 **"M. Cazorla Soult"**(소속 b, VUB SURF) 한 사람이다. 원장 · 26호 digest 의 "Soult" 는 이 복합 성(Cazorla Soult)의 뒷부분만 옮긴 표기이고 저자 순서 · 서지(권 · 논문 번호 · 제목)가 같다 → **같은 사람, 표기만 다름**(이름 "M." 은 PDF 어디에도 풀어 쓰이지 않는다).

이 digest 의 일 (지시):

1. **(a) 셀과 대조군** — 두 셀 차이의 실체(양극층 SE 재료 · 조성 · 전도도 측정값 · 측정법) · n · 제조 · 압력(코인셀 하중 · 스프링 — 원장 §3-b (배)) · 온도 · SOC.
2. **(b) 식별의 실체 (Q4)** — 다중정현 설계 · BLA 의 잡음 / 왜곡 분산(식 9–11) · Hammerstein-Wiener 구조(차수 · 꺾인점 근거) · 비용 · 검증 자료 · 유일성 · 불확실도 · 구조적 식별성(어휘 전수 · NFKC 전후) — BLA 의 "분산" 은 매개변수 분산이 아님을 가른다.
3. **(c) "고장 검출" 주장** — 통계량 · 문턱 · 대조 · 셀 수 · 교란(온도 · SOC · 진폭) · 두 셀 차이를 비선형도 차이로 읽는 것이 성립하는 조건 · Q2 · Q1.
4. **(d) 34호 처방과의 관계** — 이 다중정현이 34호(Liang 2026)가 처방한 "식별성을 입력 설계로 사는" 설계인가.
5. **(e) 우리 합성 truth · 모형에 주는 것** — `ASSB_TRANSFER_NOTE.md` §2–§4(읽기만) · 다중정현 진폭 의존 = 비선형 진단 채널인가.
6. **(f) Q5 · Q6 · Q7 · Q8** · **(g) 후속 후보**(시스템 식별 · 입력 설계 · 비선형 진단 계보 · 지목 수는 각 digest 후속 절 grep 값만 · 4차 묶음 13 편은 "도착").

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·화소]`** = 이 편 그림이 **전부 래스터**(PDF p. 3–11 그림 13 장 = 내장 이미지 13 개 · 벡터 경로 0)라 **내장 이미지를 원 해상도로 꺼내 격자선 · 축선 화소 위치로 눈금을 보정해 읽은 값** — 판독 폭은 그림마다 보정 잔차 · 표지 크기로 적는다(예: 그림 7 주파수 ±0.0004 Hz · 크기 ±0.2 dB · 표지 중심 ±0.3 dB) · 저자 원자료가 아니다 · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · `[재현·외부 값]` = 원문 밖 상수를 쓴 재현 · `[해석]` = 우리 해석. **`[데이터]` 0** — 예치 원자료 없음. 그림 판독 값 · 재현 값은 인쇄 수치와 섞지 않는다.

⚠ **쪽 표기**: Elsevier 판 12 쪽 — 인쇄 쪽 번호 1–12 = PDF p. 1–12 = PageLabels(규칙 하나 · 십진 · 1 부터). 이 digest 는 "p. 7" 하나로 적는다.

---

# 판정 먼저

1. ★★★ **(a) 대조군은 "전도도 한 변수" 가 아니라 "양극층 SE 재료 교체" 다.** 두 셀(각 **하나** — "two solid-state coin cells")은 LiNbO₃ 코팅 LCO ‖ 흑연 · 1 cm² · 0.55 mAh · 분리막 LiI-Li₂S-P₂S₅ 유리(σ₂₅ 10⁻³ S/cm)까지 같고 양극층 SE 만 **Li₂S-P₂S₅ 유리(σ₂₅ ≈10⁻⁴) ↔ γ-Li₃PS₄(≈10⁻⁵ S/cm)** 다(`[인쇄]` p. 2 "the only difference is the ionic conductivity inside the cathode layer"). 그러나 ① 전도도는 **25 ℃ 공칭 이름표**다 — 측정법 · 출처 · 시편 인쇄 0, 시험은 **60 ℃**(그림 2 캡션 · 결론). `[재현]` 그림 1 이 인쇄한 분리막 **500 µm** × 10⁻³ S/cm = **50 Ω cm²** 인데 셀 1 의 **전체** Re(1 Hz) 가 ≈20–21 Ω(`[도표·화소]` 그림 8c) → 60 ℃ 전도도는 인쇄 값의 **≥2.4 배**이고, 운전 온도에서 두 SE 의 비가 "10 배" 인지는 지면에 없다. ② 유리 ↔ 결정 γ 상 교체는 σ 말고도 변형성(접촉) · 형태 · 계면 화학을 같이 바꾼다(`[해석]`) — 그리고 지면 자신이 같은 조작을 "ionic conductivity"(p. 2) · "**boundary resistance** between solid electrolyte and active material"(p. 7) · "different materials in the **interface** of cathode active material and solid electrolyte"(p. 10)로 번갈아 부른다(벌크 수송 ↔ 계면 — D5). ③ 양극 조성비 · 적재 · 비용량 · 코팅 두께 · 음극층 SE · 성형 / 운전 압력 · 코인셀 부품(스프링 · 하중) · 온도 제어 · 측정 장비 **전부 인쇄 0**(`pressure` · `MPa` · `spring` · `torque` 0 회 — 셀은 TME 제작 · 사사). 두께는 **그림 1 에만**(양극 25 · 분리막 500 · 음극 25 µm — 본문 "similar").
2. ★★★★ **(b) Q4 — "system identification" 의 실체는 "구조 판정 + 그림으로만 남은 적합" 이다.** 입력 설계는 실재한다 — 무작위 위상 · 등진폭 33 선 · 홀수 지표 · 4 mHz–1 Hz · M 4 × P 6 · 10 Hz · 첨두 ≤2.8 mA · SoC ≤1 %(`[인쇄]`). `[도표·화소]` 그림 7 · 8a 의 표지 위치로 격자를 다시 세우면 **k = 1 · 3 · 11 · 19 · … · 251(f₀ = 1/250 s = 4 mHz — 그림 2a 주기 250 s ✅)** — **선형 간격(0.032 Hz)이라 0.04 Hz 아래(저자가 겨냥했다는 확산 대역)에 33 선 중 2 선**뿐이다. BLA 가 가르는 것은 **FRF 의 잡음 분산 ↔ 확률적 비선형 왜곡 분산**(식 9–11)이지 **매개변수 분산이 아니다** — 그리고 `[재현]` 인쇄 식 그대로면 식 9 · 10 이 이미 "한 주기 FRF 의 분산" 이라 식 11 의 ×M 이 왜곡 분산을 **≈3.13 배(진폭 ≈+5 dB)** 키운다(Monte Carlo · M 4 · P 6 · 저자가 인쇄 식대로 계산했다는 가정). 모수 모형: "**3rd order discrete FIR**" 전달함수라고 쓰고 식 12 · 그림 3 은 분모가 있는 유리함수(IIR — D1) · H 3차 다항식 · W 6차 다항식 · H-W 는 "arbitrary breaking points" 의 구간 선형(`[도표·화소]` f_h 꺾인점 ≈4 · f_w ≈3–4) — **차수 · 꺾인점 선택 근거 0 · 식별된 값(전달함수 계수 · 다항 계수 · 꺾인점) 인쇄 0**(함수는 그림뿐 — 재풀이 불가). 식별성 어휘: `identifiab*` · `confiden*` · `Fisher` · `D-optim*` · `standard deviation` · `±` **0**, `uniqu*` 1("a unique model" — 하나의 모형이라는 뜻) · `uncertain*` 1(SINAD 문장) · `variance` 6(전부 BLA). **구조적 비식별 — 블록 사이 이득 · 오프셋 교환**: 선형 블록을 고정해도 `(k·f_h, f_w(·/k))` · `(f_h + c, f_w(· − G(1)c))` 가 **같은 출력**을 낸다(`[재현]` 대수 + 수치 — 차 0) → 정규화가 인쇄되지 않았으므로 블록별 "선형선에서의 이탈"(그림 13)과 **f_w 꺾인점 "−0.4"(선형 모형 출력 좌표)** 는 정규화 의존이다(입력 좌표의 f_h 꺾인점 −0.7 · −1.8 mA 는 불변). 그리고 **입력 블록의 모양이 구조에 따라 뒤집힌다**: H 단독(그림 10a)은 방전 쪽에서 **확장**(−2.75 mA → −4.15 mA) ↔ H-W(그림 12a · 13b)는 **포화**(기울기 1.44 → 0.84 → 0.40) — 저자 `[인쇄]` "different … which will be investigated more in the following sections" 는 다음 절에서 다뤄지지 않고, 물리 배정("current saturation because of the charge-transfer limit")은 13b 하나에 선다(D8). ⇒ **Q4 0/92 — 여든네 번째 성질** · 원장 §2 **구조적 공백 1번은 그대로**(이 편은 후보에서 내려간다).
3. ★★★ **(c) "고장 검출" 은 셀 하나 ↔ 하나 · 한 진폭 · 한 온도 · 한 SOC 의 대비다.** 통계량 · 문턱 · ROC · 반복 · 교란(온도 · SOC · 진폭) **0**; "고장" = 일부러 바꾼 재료(진행하는 고장 아님); 검출 절차는 초록("utilized to detect possible faults")에만 있고 본문은 미래 과제("coupled with an online fault detection algorithm")다(D15). `[도표·화소]` 그림 7 의 ">100 times" 는 **≈0.07 Hz 위에서만**(40–72 dB) 맞고 **가장 낮은 두 선(≈4 · 12 mHz)은 ≈31–35 dB(×35–56)** — 저자가 겨냥한 저주파 끝에서 조건이 깨진다(D12). 그리고 두 셀은 **같은 전류 진폭**으로 비교됐는데 셀 2 의 |Z| 가 **×10.5–12.4**(`[도표·화소]`)라 셀 2 단자 전압이 **≈2.26–4.2 V** 를 오간다(셀 1 은 ±0.05 V · 60 ℃ RT/F = 28.7 mV `[재현]`). `[재현·가정]` BV 계면의 3차 상대 왜곡은 ≈(F/RT)²(R_ct·I)²/24 라 고정 I 에서 R_ct ×12 면 ×144(+43 dB) — **고정 전류 진폭의 비선형도는 "활성 계면 면적당 분극" 의 가파른 함수**이고, 양극층 전도도 저하 · 접촉 손실 · LAM_PE · 계면층이 **모두 같은 방향**으로 올린다(`[해석]`). 순수 BV 는 `I/(A·j₀)` 하나로만 들어가므로(`[재현]` asinh 항등) 비선형 채널 자체가 **면적 ↔ j₀ 곱을 가르지 못한다**. ⇒ 비선형도는 **검출 채널**이지 **귀속 채널이 아니다** — Q2 · Q1 에 주는 것 없음(층 하나).
4. ★★★ **(d) 34호 처방과의 관계** — 이 편은 **입력 설계를 실제로 한 ASSB 계보 첫 편**(위키 grep `multisine` · `다중사인` · `random phase` · `PRBS` — ASSB digest 0 · 액체셀 49호 하나)이지만, 설계 목적은 **BLA 의 잡음 ↔ 비선형 왜곡 분리**(Schoukens 계보 [40–45])이고 **매개변수 정보량이 아니다** — FIM · D-optimality · 정보 기준 0, 격자 선형(저주파 2 선), **진폭 한 수준**(비선형 구조 식별에 정작 필요한 축). 그리고 블록 지향 구조의 이득 · 오프셋 교환은 **어떤 입력으로도 못 사는 구조적 비식별**이다 — 34호 `[해석]` "구조적 비식별에서는 D-optimality = 0" 의 구체 표본. ⇒ 새 성질이다: **"식별성을 입력 설계로 사는 처방(34호) ↔ 입력 설계로 구조 판정만 산 첫 실측(92호)"**.
5. ★★ **(e) 우리 쪽** — α·β OCV 하네스와는 **직교**한다(고정 SoC · OCV 는 상수로 "더함" · 값 인쇄 0). 합성 truth(§3 1단계 · 셀 0)에는 **BLA + σ_S 를 진폭 둘 이상에서** 내는 순방향 관측을 후보로 넘길 수 있다 — 단 `[해석]` BV 만이면 비선형 채널은 `A·j₀` 하나만 보고, 면적을 가르는 것은 여전히 `C_dl ∝ A`(처방 1단계) 또는 면적 스케일이 다른 수송 비선형(입자 확산)이다 — truth 에서 시험할 물음이지 이 편이 답한 것이 아니다. 그리고 측정 자체가 상태를 움직인다: `[도표·화소]` 그림 2c SoC 49.98 → **48.86** → 50.40 %(최대 이탈 −1.12 % · p-p 1.55 % ↔ 설계 "≤1 %" — D3) · 셀 2 는 2.26 V 까지 내려간다.
6. **(f) 채움표** — Q1 없다(`θ(N)` 0/92 · 층 하나 — 비선형도 = 활성 면적당 분극의 단조 함수) · Q2 없다(재료 교체 · 2전극 · 대역이 계면 호 아래 · `C` 0) · Q3 층 하나("원인 이름표 = 25 ℃ 공칭 전도도 · 블록 함수 = 그림뿐 · accuracy % 정의 0") · **Q4 0/92 — 여든네 번째 성질** · Q5 해당 없음(흑연 완전지 · 2전극) · Q6 보고 0(코인셀 · 하중 · 성형 압력 인쇄 0 — (배) 표본) · Q7 해당 없음(흑연) · Q8 층 하나(OCV 상수 · 값 0 · 두 셀 선형 모형 중심 3.80 ↔ ≈3.6 V `[도표·화소]`). **누적 ≈20.0 → ≈20.0 (새 칸 0).**
7. **(g) 후속** — ★★ [46] Firouz 2016 *Energy* 106(NMC 파우치 BLA — **액체셀 도구** · 식 1–9 의 직접 원전) · ★★ [52] Widanage 2016 *JPS* 324, 61(**재지목 49 · 92 = 2**) · ★★ [48] Schoukens & Tiels 2017 *Automatica* 85(블록 지향 식별 개관 — 정규화 · 구조 판정) · ★★ [40] Schoukens 2004 *MSSP* 18(입력 설계 원전) · ★★ [58] Relan 2017 *IEEE TCST* 25(PNLSS · 저 SoC 비선형 — 액체셀 도구) · ★ [5] Kato 2016 *Nat. Energy* 1, 16030(**재지목 64 · 92 = 2 · 지목 누락** — 64호 ★ · 원장 행 0) 외.

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 1 · p. 11 · XMP) |
|---|---|
| 제목 | **"Block-oriented system identification for nonlinear modeling of all-solid-state Li-ion battery technology"** |
| 저자 · 소속 | **Yousef Firouz**ᵃ,\* · **S. Goutam**ᵃ · **M. Cazorla Soult**ᵇ · **A. Mohammadi**ᶜ · **J. Van Mierlo**ᵃ · **P. Van den Bossche**ᵃ — ᵃ Department ETEC – Mobility, Logistics and Automotive Technology Research group (MOBI), Vrije Universiteit Brussel, Pleinlaan 2, 1050 Brussels, Belgium · ᵇ Department SURF – Vrije Universiteit Brussel, Pleinlaan 2, 1050 Brussels, Belgium · ᶜ Advanced powertrain division, Toyota Motor Europe NV/SA, Hoge wei 33, Zaventem, Belgium · \* 교신 yousef.firouz@vub.be |
| 저널 | *Journal of Energy Storage* **28** (2020) **101184** · ISSN 2352-152X · **doi 10.1016/j.est.2019.101184** · XMP `prism:coverDisplayDate` "April 2020" |
| 일정 | 투고 2019-07-23 · 수정 2019-11-16 · 승인 2019-12-25 · 온라인 **2020-02-27** |
| 라이선스 | "2352-152X/ © 2019 Elsevier Ltd. All rights reserved."(p. 1 · XMP `prism:copyright` 같음) — 오픈 액세스 표기 0 · XMP `xapRights:Marked` True · `jav:journal_article_version` VoR · 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 `raw/figures/` 에 — 변형 없는 잘라내기) |
| CRediT | Firouz: Conceptualization · Methodology · Software · Writing – original draft · Investigation / Goutam: Methodology / **Cazorla Soult: Resources** / Mohammadi: Supervision · Project administration / Van Mierlo: Project administration / Van den Bossche: Supervision |
| 이해 상충 · 사사 | "no known competing financial interests" · **"This work was supported by Toyota Motor Europe (TME). The all-solid-state cells which were prepared, tested and analyzed are developed in TME."** |
| 분량 | 12 쪽 · 그림 13(전부 래스터) · 표 0 · 번호 식 35(1–35) · 참고문헌 **60**(References [1]–[23] · [25]–[60] = 59 + "Further reading" [24] 1 — [24] 본문 인용 0 · PDF p. 11–12 목록에서 직접 셈) |
| 셀 | 코인셀 둘(셀 1 · 셀 2 — 각 하나) · 양극 **LiNbO₃-coated LiCoO₂** · 음극 **graphite** · 면적 1 cm² · 용량 0.55 mAh("similar") · 분리막 **LiI-Li₂S-P₂S₅ glass**(σ₂₅ 10⁻³ S/cm) · 양극층 SE: 셀 1 **Li₂S-P₂S₅ glass**(σ₂₅ ≈10⁻⁴) ↔ 셀 2 **γ-Li₃PS₄**(σ₂₅ ≈10⁻⁵ S/cm) · 두께는 그림 1 에만(25 · 500 · 25 µm) · 제조 TME(사사) · 조성비 · 적재 · 음극층 SE · 압력 · 부품 인쇄 0 |
| 시험 | 무작위 위상 다중정현 전류(식 1) · **33 선 · 등진폭 · 홀수 지표 · 4 mHz–1 Hz** · 위상 [0, 2π] 무작위 · **실현 M 4 × 주기 P 6** · 샘플링 10 Hz · 첨두 **2.8 mA (5C)** · 설계 조건 "SoC variation should not be more than 1%" · **50 % SoC · 60 ℃**(그림 2 캡션 · 결론) · 검증 = "a multisine excitation other than the ones used for the identification algorithm" · 장비 · 온도 제어 · SoC 설정 방법 인쇄 0 |
| 모형 | 선형: 비모수 BLA(식 4–8) + 잡음 / 비선형 왜곡 분산(식 9–11) → 모수 z 영역 유리함수(식 12 — 본문 "3rd order discrete FIR") · 비선형: Hammerstein(3차 다항식 · 식 13–15) · Wiener(6차 다항식 · 식 16–19) · Hammerstein-Wiener(중간 분할 · 구간 선형 · 쌍선형 최소제곱 · 식 20–32) · OCV(SOC) 를 출력에 더함(그림 3) · 물리 해석: 식 33(Nernst 확산층 — [59]) · 식 34–35(BV · j₀(c_s) — [60]) |

**PDF 메타데이터 (직접 읽음 · pymupdf)**: 6,118,709 B · sha256 `9cf5d53f1aea0281d942fb56beb6d2d0acf84ed25eefdfe6927599a12a9f7449`(호출자 접두 `9cf5d53f1aea0281` ✅) · `%PDF-1.7` · 12 쪽 전부 595.28 × 793.70 pt · 정보 사전: title = 논문 제목 그대로 · author **"Yousef Firouz"** · subject **"Journal of Energy Storage, 28 (2020) 101184. doi:10.1016/j.est.2019.101184"** · keywords "Block-oriented system identification; All-solid-state Li-Ion battery; Ionic conductivity; Multisine excitation; Hammerstein-Wiener system; " · creator **"Elsevier"** · producer 빈 값 · 생성 **2020-05-10 21:53:33Z** · 수정 **2023-08-11 09:08:08 +05'30'** · 암호 0 · XMP 7,318 B(`dc:creator` 여섯 — 셋째 "M. Cazorla Soult" · `dc:identifier` doi · `prism` 권 28 · 쪽 101184 · 표지 날짜 "April 2020" · `crossmark:MajorVersionDate` 2010-04-23 · `pdfx:robots` noindex · `jav` VoR · `xmpMM:DocumentID` uuid:b5c7d251-7073-4ddc-ace6-738cdf0e54d4 · InstanceID uuid:50490895-3e28-4699-bb8c-7d97fa515971) · PageLabels 규칙 하나(십진 · 1 부터 — 인쇄 쪽과 같다) · 개요(북마크) 29 항목(절 제목 + Elsevier 표지 `mk:H1_24` · `mk:H2_28`) · 이미지: p. 1 셋(Elsevier 로고 247×272 · 저널 표지 236×298 · Crossmark 120×120) · **p. 3–11 그림 13 장 = 래스터 13 개**(1300×644 · 1300×1341 · 1025×391 · 1300×750 · 1300×367 · 1500×800 · 1025×551 · 1500×986 · 1500×1013 · 1300×673 · 1300×670 · 1300×753 · 1300×898 px) · p. 12 이미지 0.

⚠ **텍스트 층**: 전도도 첨자 "σ25ºC" 의 "º" 는 남성 서수 기호(U+00BA)라 NFKC 뒤 "oC" 가 된다(어휘 집계 `°C` 5 → 2) · 지수의 음수 부호가 텍스트 층에서 빠진다("10 4 S/cm" · "10 5 S/cm" — 렌더 · 그림 1 로 10⁻⁴ · 10⁻⁵ 확인 · p. 2 첫 값은 "10–3" 으로 엔 대시) · 식 1–35 는 그리스 문자 · 분수가 흩어져 **렌더로 읽었다**.

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **셀 제조** — 양극 조성비(LCO : SE : 탄소?) · 적재 · 비용량 · LiNbO₃ 두께 · **음극층 SE**(그림 1 음극에 SE 이름표 0 — 그런데 p. 10 은 "high ionic conductivity (10⁻³ S/cm) in the **anode** and separator layer") · 성형 압력 · **운전 압력 · 코인셀 부품(스프링 · 스페이서 · 하중)** · 셀 수(각 하나로 읽힘) | 두 셀 차이가 "σ 하나" 인지 가를 입력이 없다 — 재료 교체가 조성 · 접촉 · 압밀을 같이 바꾸는지 지면으로 판정 불가 · Q6 |
| **G2** | **전도도 값의 출처 · 측정법 · 60 ℃ 값** — 세 값 모두 "σ₂₅ ≈10⁻ⁿ" 자릿수 이름표 | 시험은 60 ℃ — 운전 온도에서 두 SE 의 비가 "10 배" 인지(활성화 에너지가 다르면 비가 바뀐다 `[해석]`) · `[재현]` 분리막 값은 60 ℃ 에서 ≥2.4 배여야 그림 8c 와 맞는다 |
| **G3** | **장비 · 온도 제어 · SoC 설정** — 전류원 · 전압 분해능 · 챔버 · 50 % SoC 를 어떻게 맞췄는지(쿨롱 계수 ↔ OCV) 인쇄 0 | 그림 2c SoC 축의 기준 · 셀 2 선형 모형 중심이 셀 1 과 0.2 V 다른 것(`[도표·화소]`)의 해석 |
| **G4** | **다중정현 격자 · 선 진폭 · RMS · 파고율 · 실현별 위상** — "odd indexes … 4 mHz up to 1 Hz" 와 33 만 인쇄 · 검증 실현 수 · 그림 2 · 6 · 9 가 어느 실현인지 | `[도표·화소]` 로 격자(k = 1 · 3 · 11 · … · 251)를 재구성했다 — 저자 확인 아님 · 선 진폭 ≈0.25 mA · RMS ≈1.0 mA 는 `[재현·가정]` |
| **G5** | **식별된 값** — 전달함수 계수 a · b · 다항 계수 α_t · β_t · 구간 선형 K · A · 꺾인점 c 와 그 **불확실도** · 블록 사이 **정규화**(이득 · 오프셋 고정 규약) | 식별 편인데 식별 결과가 그림으로만 있다 — 재풀이 · 다른 셀 이식 · 유일성 검사 전부 불가 |
| **G6** | **차수 · 꺾인점 선택 근거 · 학습 ↔ 검증 분할(비선형 모형) · "accuracy %" 정의** — "3rd order" · "third-order" · "sixth-order" · "arbitrary breaking points" · 정확도 74.5 · 81 · 86.5 % | 과적합 여부 · 검증이 표본 밖인지 · 백분율이 무엇의 백분율인지 판정 불가 |
| G7 | **OCV 값 · 곡선** — "open circuit voltage (OCV) is added to the estimated voltage" · OCV(SOC) 블록(그림 3) | 정적 몫(OCV) ↔ 동적 몫의 경계 · Q8 |
| G8 | **잡음 분산 곡선 σ_N** — 식 9 로 계산했다고 쓰고 그림 7 은 비선형 왜곡만 그린다 · **홀 ↔ 짝 검출선 분석 0**(격자상 비여기 홀 · 짝 선이 있다 `[해석]`) | "잡음 무시" 가정의 정량 근거 · 짝수 비선형(비대칭 — 충 ↔ 방)의 분리 |
| G9 | **고장 검출 절차** — 통계량 · 문턱 · 오경보 · 셀 수 | 초록 명제의 근거 |
| G10 | **반복 · 교란** — 같은 종류 셀 둘 이상 · 온도 · SoC · 진폭 의존 | 비선형도 차이가 셀 산포 · 상태 · 진폭의 함수인지 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 직접 다시 셌다 — 본문 · 캡션 · 참고문헌 전문(NFKC 전후)에서 `supplement*` · `appendix` · `data availability` · `supporting information` · `video` · `movie` · `zenodo` · `github` **0 회**. 원자료 예치 0 · 코드 0(`MATLAB` · `software` · `toolbox` 0 회). 그래서 이 digest 의 재현은 **인쇄 수치 + 그림 래스터 화소** 두 층뿐이다.

---

# 그림 — 자동 13 항목, 실제로 연 것 **13/13** (+ 화소 판독 여덟: 그림 2 · 6 · 7 · 8a · 8c · 9 · 12a · 13 — 판독용 · 커밋 안 함)

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 **13** 을 `fig_1 … fig_13` 으로 잡았다(SI 오판 0 — 파일명 `52._Block-oriented_system_identification_…` 의 `SI_TAG` False 를 첫 실행 전에 확인 · 실행 뒤 이름을 눈으로 확인). 표는 이 편에 **없다**(본문 "Table" 0 회). **열세 장 전부 직접 봤다 — 안 본 그림 0.** 그림이 전부 래스터라(내장 이미지 13 개) 원 해상도 이미지를 꺼내 축선 · 격자선 화소로 눈금을 보정해 여덟 장을 읽었다(`[도표·화소]` · 판독 배열은 `scratchpad` 에만).

자동 크롭 점검(`figures.json` `note` 에 적음): 열세 장 모두 **라벨 · 축 · 내용 온전 · 과대 영역 0**. 크롭 문제 하나 — **fig_13 아래 가장자리에 캡션 첫 줄의 윗부분이 잘린 채 걸렸다**(캡션 겹침 잘림 — 그림 내용은 온전). 캡션 필드 문제: f1 · f4 · f5 · f6 · f9 · f10 · f12 · f13 **900 자에서 잘림 + 본문 섞임**(식 1–35 의 흩어진 글자 · 절 본문), f2 520 자(식 9–10 글자 섞임), f7 844 자(§4.1 본문 섞임), f11 286 자(쪽 바닥글 "9" 섞임) · f3 · f8 만 깨끗하다. 캡션 정본은 이 digest 의 각 그림 절에 옮긴 `[인쇄]` 캡션이다.

## Fig. 1 — 두 코인셀 모식 (p. 3 · 봤다) ★★★ (a) · G1 · D7

`[인쇄]` 캡션 "Developed all-solid-state coin cells with different ionic conductivity at cathode." `[도표]` 두 기둥 — 위 "cathode"(타원 = "LCO") · 가운데 "SE: LiI-Li2S-P2S5 σ = 10⁻³ S/cm" · 아래 "Anode"(육각 = 흑연). 셀 1 양극 초록 + 이름표 "Li2S-P2S5 glass" · 머리 "Cell 1: σ = 10⁻⁴ S/cm" · 셀 2 양극 빨강 + "γ-Li3PS4" · "Cell 2: σ = 10⁻⁵ S/cm". 왼쪽 치수 화살 **"25um"(양극) · "500um"(분리막 — 생략 꺾쇠) · "25um"(음극)** — **이 편에서 두께가 인쇄된 유일한 자리**(본문은 "the corresponding parts' thickness … of both cells are similar"). 음극 층에는 SE 이름표가 없다(D7). 코인셀 캔 · 스프링 · 집전체 · 압력 표시 0.

## Fig. 2 — 측정 다중정현 전류 · 스펙트럼 · SoC (p. 4 · 봤다 + 화소) ★★★★ (b) · D3 · D4

`[인쇄]` 캡션 "(a) Measured multisine current at 50% SoC and 60 °C, (b) Fourier transformation of measured multisine current, (c) SoC variation during multisine current." — **온도 60 ℃ 가 실험 조건으로 인쇄된 두 자리 중 하나**(다른 하나는 결론).
- (a) `[도표·화소]`(시간 ±0.25 s · 전류 ±0.02 mA) 0–250 s 한 주기 · **첨두 +2.74 / −2.74 mA**(축 ±3 mA) · 평균 −0.001 mA(영평균 ✅) · RMS 는 열별 포락선으로 **0.72–1.09 mA** 사이 → 파고율 ≈2.5–3.8. 한 주기 **250 s = f₀ 4 mHz** ✅(인쇄 최저 주파수와 같다).
- (b) `[도표]` y 축 **"Power Spectral Density (dB/Hz)"** · 0–5 Hz(나이퀴스트 = 10 Hz ÷ 2 ✅) · 여기 선 ≈ −71 dB/Hz 의 점선(0–1 Hz) · 잡음 ≈ −160(−145 … −185) — 본문은 같은 두 수준을 "blue dots with −70 dB **amplitude**" · "−160 dB" 로 부르고, 그림 6a 는 같은 수준(−72 · −160)을 **"Current Amplitude (dB)"** 로 그린다(단위 이름 불일치 — D4).
- (c) `[도표·화소]`(SoC ±0.01 %) **49.98 → 48.86 %(t ≈99 s) → 50.40 %(≈224 s) → 50.01 %** — **최대 이탈 −1.12 % · 정점 간 1.55 %** ↔ 본문 설계 조건 "the SoC variation should not be more than 1%"(D3). 모양은 250 s 주기 성분 하나가 지배(최저 선 4 mHz).

## Fig. 3 — 제안 모형 구성 (p. 4 · 봤다) ★★ (b) · D1 · D19

`[도표]` I(k) → **g(x)**("Nonlinear function") → **(b₀ + b₁z⁻¹ + b₂z⁻² + ⋯ + bₙz⁻ⁿ)/(1 + a₁z⁻¹ + a₂z⁻² + ⋯ + aₙz⁻ⁿ)**("Linear transfer function model") → **f(x)** → ⊕ → V(k), 그리고 I(k) → **OCV(SOC)** → ⊕. 분자 · 분모 차수가 같은 n — **분모가 있는 유리함수(IIR)** 인데 §4.1 은 같은 블록을 "3rd order discrete **FIR**" 로 부른다(D1). 블록 이름 g/f ↔ 본문 f_h/f_w(D19 · 사소).

## Fig. 4 — 세 직렬 블록 구조 (p. 5 · 봤다) ★★ (b) · D18

`[도표]` (a) Hammerstein: u(k) → f_h(u(k), η) → h(k) → Ĝ_BLA(jω_n, θ) → ⊕ε(k) → v_l(k) · (b) Wiener: u → Ĝ_BLA → v_l → f_w(v_l(k), η) → ⊕ε → w(k) · (c) Hammerstein-Wiener: u → f_h → h → Ĝ_BLA → v_l → f_w → ⊕ε → w. 잡음 ε 는 **출력**에 더해진다(그림 5 · 식 15 와 다름 — D18). 두 비선형 블록의 매개변수를 같은 기호 η 로(본문은 α · β · ζ · γ — D19).

## Fig. 5 — H-W 중간 분할 (p. 6 · 봤다) ★★ (b)

`[도표]` u → f_h → h → **B(z⁻¹)** → ⊕ε(k) → **S_f(k)** → 1/A(z⁻¹) → v_l → f_w → w. 분할점 S_f(k) 에서 입력 쪽(식 25)과 출력 쪽(f_w 역함수 — 식 24 · 26)을 맞대 쌍선형 문제(식 27)로 만든다 — **f_w 가 역함수를 가져야(단조) 성립**(본문 전제 문장 0 · `[해석]`). 잡음은 분할점(방정식 오차형)에 들어간다(D18).

## Fig. 6 — 입력 전류 · 두 셀 전압의 스펙트럼 (p. 7 · 봤다 + 화소) ★★★★ (b) · (c) · D4

`[인쇄]` 캡션 "Fourier transform of (a) input multisine current, (b) measured response voltage in the case of cell1 and (c) measured response voltage in the case of cell2." `[도표·화소]`(축 보정 잔차 ≤0.3 dB · 점 중심 ±0.5 dB):
- (a) 여기 선 **−72 dB**(0–1 Hz) · 잡음 중앙 −160 … −162 dB(p90 −149 … −152 · 최대 −144.4) · 화살 "SNR>70dB" — `[재현]` 여기 ↔ 잡음 최대 72.4 dB · 중앙 ≈88 dB.
- (b) 셀 1: 여기 선 ≈ −42(최저 주파수) … −46 dB(1 Hz) · 비여기 대역 안 중앙 **−89 (≤0.05 Hz) / −101 (0.05–0.5) / −107 dB (0.5–1)** · 최대 −80.4 / −90.2 / −99.2 · **대역 밖 1–5 Hz 중앙 ≈ −112 dB 평탄**(잡음 바닥) · 화살 "SINAD = 50dB". `[재현]` (여기 − 최대 비여기) ≈38 dB(≤0.05 Hz) · ≈45 dB(0.05–0.5) · ≈53 dB(0.5–1) — "≈50 dB" 는 0.05 Hz 위의 값이고 저주파 끝은 ≈38 dB.
- (c) 셀 2: 여기 선 ≈ −19(최저 선 · 눈) / −22.2 … −25.5 dB · 비여기 대역 안 중앙 **−42.7 / −44.2 / −45.7 dB** · 최대 −39.1 / −33.8 / −37.0 · **대역 밖 중앙 −57.9 (1–2 Hz) → −72.6 → −79.4 → −82.6 dB (4–5 Hz)** · 화살 "SINAD < 15dB". `[재현]` 0.05–0.5 Hz 최악 SINAD ≈11 dB ✅ · **대역 밖 왜곡이 셀 1 잡음 바닥보다 +54 · +39 · +33 · +29 dB** — 여기 대역(≤1 Hz) 밖으로 번진 고조파 · 상호변조는 모형 없이 읽히는 비선형 지문인데 본문은 이 대역 밖 부분을 정량하지 않는다.
- `[재현]` 같은 dB 척도끼리(여기 전류 −72 dB) 셀 전압 선을 빼면 |Z| ≈30 dB(셀 1 최저 선) · 26 dB(1 Hz) · ≈53 dB(셀 2 최저 선) · 46.5 dB(1 Hz) — 그림 7 · 8a 와 ±2 dB 안에서 맞는다(정규화가 같다는 뜻 · 절대 단위는 미인쇄).

## Fig. 7 — BLA 와 비선형 왜곡 (p. 7 · 봤다 + 화소) ★★★★ (b) · (c) · D2 · D12

`[인쇄]` 캡션 "Bode plot (amplitude) of BLA and nonlinear distortion for call1 and cell2."(오기 "call1") · y 축 "Impedance Amplitude (dB)" · x 0–1.2 Hz 선형. 범례 BLA cell2(빨간 별) · NL dist cell2(빨간 역삼각 점선) · BLA cell1(파란 별) · NL dist cell1(파란 역삼각). 주석 화살 "12 times"(두 BLA 사이 · ≈0.9 Hz) · ">100 times"(두 NL 사이 · ≈0.5 Hz).
`[도표·화소]`(주파수 보정 잔차 ±0.0004 Hz · dB ±0.2 + 표지 중심 ±0.3):
- **선 33 개** — 0 근처에 겹친 둘(그림 8a 에서 ≈0.005 · ≈0.011 Hz 로 갈림) + **0.0434 … 1.0018 Hz 의 31 개, 간격 0.0320 Hz(= 8 × 4 mHz)** → 격자 **k = 1 · 3 · 11 · 19 · … · 251**(f = 0.004 k Hz · 최고 1.004 Hz) `[재현]` — 2 + 31 = 33 ✅ · 홀수 지표 ✅. 0.04 Hz 아래 2 선 · 0.04–0.4 Hz 12 선 · 0.4–1.004 Hz 19 선(선형 격자).
- BLA 셀 2: ≈52.5(겹친 둘) · 49.5(0.044) · 49.0(0.075) · 47.8(0.2) · 47.0(0.5) · **46.6 dB(1.0 Hz)** / BLA 셀 1: ≈30.9(겹친 둘) · 27.7 · 27.2 · 26.4 · 26.4 · **26.1 dB**. `[재현]` 비 **21.6–21.8 dB(×12.0–12.4 · ≤0.044 Hz) → 20.5–20.6 dB(×10.5–10.8 · 0.5–1 Hz)** — "12 times" 는 저주파 쪽 값.
- NL dist 셀 2: ≈30.0–30.9(최저 둘) · 24.3(0.044) · 16.9–30.9 사이(나머지 · 대부분 22–25) / NL dist 셀 1: ≈ −1 … −5(최저 둘) · −15.5(0.044) · −18 … −26(0.07–0.43) · −28 … −40 · **−48.6(0.554 Hz 골)**. `[재현]` 두 셀 NL 차 **≈31–35 dB(×35–56 · 최저 두 선) · 39.7 dB(×97 · 0.044) · 41–54 dB(×110–525 · 0.07–0.5) · 54–72 dB(0.55–0.78)** — ">100 times" 는 ≈0.07 Hz 위(D12).
- `[재현]` 상대 왜곡(NL ÷ BLA): 셀 1 ≈ −34(최저) · −43(0.044) · −55 dB(0.5–1) ↔ 셀 2 ≈ −22.5 · −25.3 · −22.5 … −24.4 dB(**셀 2 는 선형 응답의 ≈3–8 % 가 선마다 실현에 따라 흔들린다**) · 증가 +11.5 → +18 → +31–33 dB(주파수가 오를수록 커진다).
- ⚠ 본문 "the amplitude of linearized impedance of **cell 1** increased around 12 times" — 그림에서 큰 쪽은 셀 2 다(D2). 그리고 그린 것은 σ_S(비선형)뿐 · σ_N(잡음) 곡선 0(G8).

## Fig. 8 — BLA ↔ 선형 모형: 크기 · 위상 오차 · Nyquist (p. 8 · 봤다 + 화소) ★★★★ (b) · D1

`[인쇄]` 캡션 "Comparison of calculated BLA of cell1 and cell2 and identified linear model by (a) impedance amplitude, (b) impedance phase and (c) Nyquist plot."
- (a) `[도표·화소]`(±0.1 dB) 셀 1 측정(파란 원) ≈32.2(≈0.005 Hz) · 29.2(≈0.011) · 27.4(0.044) · 26.5(0.17) · 26.1 dB(1 Hz) + 모형(빨간 파선) · 셀 2 측정(검은 사각) ≈53 → 49.5 → 47.5 → 46.6 dB + 모형(하늘 점선) — 크기는 겹친다. **0 근처의 두 표지가 갈려 보여 최저 두 선이 ≈0.004 · ≈0.012 Hz(k = 1 · 3)임을 확인**(±0.002 Hz).
- (b) `[도표]` y 축 "Phase error (Deg)" ±10° — **위상 자체가 아니라 모형 오차만** 그렸다: 셀 1 ≈0(±0.3°) · 셀 2 대부분 ±1.5° · 큰 것 ≈ −2.8°(≈0.5 Hz) · ≈ −3.5°(≈0.85 Hz) — 본문 "a few degrees" ✅.
- (c) `[도표·화소]`(±0.8 Ω) **셀 1**: 1 Hz 끝 ≈(20–21, ≈3) Ω → 최저 선 **(32.4, 23.5) Ω**(|Z| 40.0 Ω = 32.0 dB ✅) — 점 사이 기울기 ≈60° · **셀 2**: 1 Hz 끝 **(209.5, 11.8)**(|Z| 209.8 Ω = 46.4 dB ✅) · (236.4, 36.1) · (290.5, 65.6)(0.044 Hz · 49.5 dB ✅) · (348.8, 113.6)(≈0.012 Hz · 51.3 dB) · **(405.6, 209.8) Ω**(최저 선 · |Z| 456.6 Ω = 53.2 dB ✅) — 0.1 Hz 위의 점 대부분이 Re 205–236 Ω 한 덩어리로 겹친다(선형 격자의 결과 — 덩어리 밖 점은 최저 네댓 선뿐). Bode ↔ Nyquist 폐합 ✅(±0.3 dB).
- `[해석]` 대역 4 mHz–1 Hz 의 고주파 끝이 이미 Re ≈20 · ≈210 Ω — **계면 호(대개 >1 Hz)는 대역 밖**이라 이 Nyquist 로는 옴 · 전하이동 · 이중층을 가를 수 없다. 본문 "the curve has been shifted to the right side, which is considered as ohmic resistance increase" 의 "옴" 은 1 Hz 실부(전하이동 · 수송 포함)다.

## Fig. 9 — 선형 모형 검증 (p. 8 · 봤다 + 화소) ★★★★ (b) · (c)

`[인쇄]` 캡션 "Comparison of linear model validation with measured data in the case (a) cell1 and (b) cell2." 본문 "The identified linear model has been validated with a multisine excitation other than the ones used for the identification algorithm."
- (a) `[도표·화소]`(±3 mV) 셀 1 전압 ≈3.75–3.86 V · 선형 모형 중심 **≈3.80 V** · 오차 판(mV): t = 0 에서 ≈ +2.6 mV → 50 s ≈ +0.5 → 250 s ≈ −1.6 mV 의 **느린 표류**(무작위 오차가 아니다 — 초기 과도 + OCV · SoC 표류 꼴 `[해석]`) — 본문 "maximum voltage error is around 3 mV" ✅.
- (b) `[도표·화소]`(±0.02 V) 셀 2 측정 **최저 ≈2.26 V**(≈80–85 s · 65–100 s 에 아래로 뾰족한 다발) · 선형 모형 **≈3.04–4.19 V** · 모형 중심 **≈3.58–3.61 V**(셀 1 과 ≈0.2 V 차 — 같은 "50 % SoC" · G7) · 오차 판(V): 대부분 ±0.1 V · 아래로 −0.45(≈65 s) · −0.6(≈73 · 90 s) · **−0.8 V(≈82–85 s)** — 본문 "the model error reaches to 0.8 V" ✅. 뾰족한 다발이 한 주기의 **한 구간(≈60–100 s)에 몰린다** — 같은 첨두 방전 전류라도 느린 성분(저주파 선의 위상)이 낮은 때만 크게 떨어진다는 그림이다(`[해석]` 순간 전류만의 정적 함수가 아니라 이력(저주파 상태)에 걸린 비선형 · 이 검증 실현의 전류 · SoC 궤적은 인쇄 0 이라 대조 불가).

## Fig. 10 — Hammerstein (p. 9 · 봤다) ★★★★ (b) · D8

`[인쇄]` 캡션 "a) input distortion and identified Hammerstein function (red line) and (b) comparison of measured voltage with linear model and Hammerstein system output."
- (a) `[도표]`(±0.1 mA) 축 "Output Hammerstein (A)" ↔ "Input current (A)" ×10⁻³ · 파란 점 "Measured NL dist" · 빨간 "Polynomial Fun"(3차): **(−2.75, −4.15) mA … (0, 0) … (2.75, 2.25) mA** — 방전 쪽 **확장**(평균 기울기 ≈1.5) · 충전 쪽 압축(≈0.82) · 점은 −2 mA 에서 −1.5 … −5.5 mA 로 흩어진다(본문 "distortions are scattered widely") · "Discharge" · "Charge" 이름표. x 범위 ±2.75 mA(자료 첨두와 같다).
- (b) `[도표]` 범례 **"Linear (68.5%)"** · **"Hammerstein (74.5%)"** — 선형 모형의 정확도 **68.5 % 는 이 범례에만** 인쇄돼 있다(본문은 차이만). 초록 H 출력도 65–100 s 의 깊은 낙하(≈2.26 V)를 못 따라간다. 측정선 = 그림 9b 와 같은 궤적.

## Fig. 11 — Wiener (p. 9 · 봤다) ★★★ (b)

`[인쇄]` 캡션 "(a) input distortion and identified Wiener function (red line) and (b) comparison of measured voltage with linear model and Wiener system output." (a) `[도표]`(±0.02 V) 축 "Output voltage Wiener (V)" ↔ "Linear model (V)" · 빨간 6차 다항식(범례 오기 **"Ploynomial Fun"**) **(−0.63, −1.1) V … (0, ≈0.05) … (0.63, 0.55) V** — 충전 쪽 거의 직선(≈0.87) · 방전 쪽 아래로 휜다(본문 "logarithmic pattern") · 점은 −0.6 V 에서 −0.75 … −1.4 V. (b) 범례 **"Linear (68.5%)" · "Wiener (81%)"** · 측정선 = 그림 9b 궤적.

## Fig. 12 — Hammerstein-Wiener (p. 10 · 봤다 + 화소) ★★★★ (b) · D8 · D10 · D11

`[인쇄]` 캡션 "(a) identified Hammerstein function, (b) identified Wiener function and (c) comparison of measured voltage with linear model and Hammerstein-Wiener system output."
- (a) `[도표·화소]` h(k) ↔ input current(A) · 구간 선형 — 그림 13b 의 파란 선과 같은 함수 · **x 범위 −3.29 … +3.27 mA**(자료 첨두 ±2.74 mA 밖 0.5 mA — D11).
- (b) `[도표]` "output voltage (V)" ↔ "Vl(k)" — **x 축 눈금 이름이 "−0.43 · 0 · 0.43 · −0.43 · 0"**(단조가 아님 — 그림 오류 D10) · 곡선 모양은 그림 13d 와 같다.
- (c) `[도표]` 범례 **"Linear (68.5%)" · "Hammerstein-Wiener (86.5%)"** · 초록 H-W 가 65–100 s 의 깊은 낙하(≈2.2–2.4 V)를 거의 따라간다 — 본문 "the high amplitude voltage drops are almost predicted" ✅(시각).

## Fig. 13 — 셀 1 ↔ 셀 2 블록 함수와 "선형선" (p. 11 · 봤다 + 화소) ★★★★ (b) · (c) · D8 · D9

`[인쇄]` 캡션 "classifying of Hammerstein and Wiener systems regarding charging zone, discharging zone and their deviation from the linear line (dashed red line): (a,c) cell1 and (b,d) cell2." `[도표·화소]`(입력 ±0.02 mA · ±0.003 V · 출력 ±0.03 mA · ±0.01 V):
- (a) 셀 1 Hammerstein: 직선 (−3.30, −3.09) … (3.29, 3.04) mA — **기울기 0.93**(본문 "(Y = X)").
- (c) 셀 1 Wiener: 직선 · x −0.067 … +0.065 V(셀 1 의 선형 출력 폭) · **y 축에 눈금 숫자가 "0" 하나뿐**(척도 없음 — "Y = X" 확인 불가 · D9).
- (b) 셀 2 Hammerstein(파란): 방전 쪽 기울기 **1.44(0 → −0.57 mA) → 0.73–0.95(→ −1.65) → 0.35–0.46(→ −3.29 mA)** · 충전 쪽 1.2(→ +0.5) → 1.07–1.11 · 꺾인점 ≈ **−1.8 · −0.7 · 0 · +0.45 mA**(±0.1) · f_h(0) ≈ +0.1 mA · 빨간 파선("linear line") **기울기 1.12**.
- (d) 셀 2 Wiener(파란): 방전 쪽 기울기 **0.81 → 1.06 → 1.68 → 2.78 → 5.2–5.5(< −0.475 V)** · 충전 쪽 0.78–0.88 · 꺾인점 ≈ −0.45 · −0.3 · −0.15 V · f_w(0) ≈ +0.05–0.08 V · x 범위 −0.695 … +0.617 V · 빨간 파선 **기울기 0.92 · 절편 +0.04 V**.
- ⇒ 두 파선은 Y = X 가 아니다(1.12 · 0.92) · 그리고 `[재현]` 충전 쪽 두 기울기 곱 1.09 × 0.84 ≈0.91 만 블록 사이 정규화에 불변이다(판정 2 · §(b) 4).
- 본문 서술 대조: "the input galvanostatic current … becomes saturated in the case of values bigger than 2 mA" ↔ (b) 기울기가 ≈ −1.8 mA 아래에서 0.4 로 꺾인다 ✅(≈"2 mA") · "the output voltage drops logarithmic for amplitudes smaller than −0.4" ↔ (d) −0.45 V 아래 기울기 ≈5.3 의 **직선 구간**(구간 선형 모형이라 "로그" 는 모양 비유).

## 본문 서술과 어긋난 그림 (요약)

| # | 그림 | 서술 | 어긋남 |
|---|---|---|---|
| D2 | 7 | "the amplitude of linearized impedance of **cell 1** increased around 12 times" | 큰 쪽은 셀 2 · 비는 ×10.5(1 Hz)–×12.4(저주파) |
| D3 | 2c | "SoC variation should not be more than 1%" | 최대 이탈 −1.12 % · 정점 간 1.55 % |
| D4 | 2b ↔ 6a | "−70 dB amplitude" · "−160 dB" | 2b 축 "dB/Hz"(PSD) · 6a 축 "Current Amplitude (dB)" — 같은 수준 |
| D8 | 10a ↔ 12a · 13b | "The Hammerstein curve in Fig. 12a is different from the one seen in Fig. 10a, which will be investigated more in the following sections" | 다음 절에서 다루지 않음 · 두 그림의 방전 쪽 모양이 **확장 ↔ 포화** 로 반대 |
| D9 | 13 | 셀 1 "totally linear curves … (Y = X)" · "linear line (dashed red line)" | 셀 1 H 기울기 0.93 · 13c y 척도 없음 · 13b · 13d 파선 기울기 1.12 · 0.92 |
| D10 | 12b | — | x 눈금 이름 "−0.43 · 0 · 0.43 · −0.43 · 0" |
| D11 | 12a · 13a · 13b | 최대 전류 "2.8 mA (5C)" | 함수가 ±3.3 mA 까지 그려짐(자료 ±2.74 mA) — 외삽 서술 0 |
| D12 | 7 | "the level of nonlinear distortion has been increased more than 100 times" | 최저 두 선 ≈31–35 dB(×35–56) · 0.044 Hz ×97 |

---

# 절별 해체 (본문)

## 초록 · 키워드 (p. 1)

`[인쇄]` "due to the low ionic conductivity of solid materials and existing issues in active material-solid electrolyte interfaces, all-solid-state batteries show strong nonlinear behavior when the amplitude of input current is relatively high. In this paper, we have developed a methodology based on block-oriented nonlinear systems that can detect, quantize, and model the battery behavior, accurately. For this purpose, two solid-state coin cells, which have different ionic conductivity at the cathode interface are manufactured and excited with multisine input current. The Best Linear Approximation (BLA) method has been used to separate linear frequency response function (FRF) from nonlinear distortion. Then, a Hammerstein-Wiener system has been developed and parametrized to model the nonlinear distortions caused by ionic conductivity variation of the solid electrolyte at the cathode layer. **Furthermore, the developed model has been utilized to detect possible faults in the electrode-electrolyte interface based on the nonlinearity level of the measured voltage.**" · 키워드: Block-oriented system identification · All-solid-state Li-Ion battery · Ionic conductivity · Multisine excitation · Hammerstein-Wiener system.
- "when the amplitude of input current is relatively high" — **진폭 의존을 명제의 조건으로 인쇄**하지만 본문은 **진폭 한 수준**만 쟀다(§(c)).
- "different ionic conductivity **at the cathode interface**" ↔ §2.1 "inside the cathode layer"(벌크) — D5.
- "detect possible faults" — 검출 절차 · 통계량은 본문에 없다(D15).

## §1 서론 (p. 1–2)

`[인쇄]` 계보: ECM(HPPC 시간 영역[13–15] · EIS 주파수 영역[16–18] — "the amplitude of sines must be limited in the range of 5 to 10 mV" · "only accurate in the mid-range of SoC") · AI("[21–23,35] ANN and GA" — "does not provide any physical interpretation") · 비선형 모형("Authors in [35–39] have claimed that they developed nonlinear models for the batteries, while those are linear parameter varying (LPV) models") · **BLA**("Schoukens et al. [40–45] proposed the best linear approximation (BLA) method to detect, qualify, and quantify nonlinearities … periodic zero-mean multisine excitation") · 같은 저자 선행 "**Firouz et al. [46] performed BLA analysis on nickel manganese cobalt oxide NMC pouch cells** … However, they only developed a nonparametric model and the extracted linear and nonlinear parts were not parameterized" · 블록 지향 계보: "[52] … multisine current … Wiener system … However, the detected nonlinearity is very weak and the identified Wiener function is almost linear" · "[53] … online parameter estimation for the Wiener battery model … weak as well" · "[58] … polynomial nonlinear state-space (PNLSS), which mainly focuses on low SoC (<10%) as nonlinearity is strong on that range."
- §1.1 기여: "in some cases of solid electrolyte materials, battery voltage shows strong nonlinearity in high input currents which cannot be predicted with linear electrical models. In order to avoid complicated electrochemical models, this paper utilizes innovative nonlinear models … three nonlinear models—Hammerstein, Wiener, and Hammerstein-Wiener (**which is not investigated yet in any other publications**)—are developed" — 같은 편이 [50] "Identification of hammerstein-wiener systems" · [56] Bai 1998 을 인용한다(전지 맥락으로 읽어야 성립 — D14).
- ⚠ 인용 어긋남(D16): "[6,7]" 를 BMS SoC/SoH 추정 근거로 쓰는데 [6] = Sakuda 2011 *JPS*(LiCoO₂ 입자 + Li₂S–P₂S₅ PLD 코팅 — 재료 편) · "[21–23,35] ANN and GA" 의 [21] = Westerhoff 2016(EIS 기반 모형 분석).
- `[해석]` 서론이 스스로 "[58] … low SoC (<10%) as nonlinearity is strong" — **비선형도가 SoC 의 함수**라는 같은 연구실 결과를 인쇄해 두고, 본 편 "고장 검출" 은 SoC 50 % 한 점이다(§(c) 교란).

## §2.1 시험 셀 (p. 2)

`[인쇄]` "two solid-state coin cells with different materials in the cathode layer have been prepared as shown in Fig. 1. All cells have the same cathode and anode materials—LiNbO3-coated LiCoO2 and graphite. Surface area is 1cm2 and the corresponding parts' thickness and capacity of both cells are similar (0.55 mAh). Both cells have been equipped with LiI-Li2S-P2S5 glass for separator exhibiting ionic conductivity (σ25ºC) of 10⁻³ S/cm. **However, the only difference is the ionic conductivity inside the cathode layer.** The ionic conductivity of the cathode layer has been controlled by changing solid electrolyte (SE) materials; in cell number 1, Li2S-P2S5 glass exhibiting ionic conductivity (σ25ºC ≈10⁻⁴ S/cm) was equipped, while for cell 2, the solid electrolyte of γ-Li3PS4 (σ25ºC ≈ 10⁻⁵ S/cm) was used."
- **n = 1 · 1**("two solid-state coin cells" — 반복 · 산포 0). 조성비(LCO : SE) · 적재 · LiNbO₃ 두께 · 음극층 조성 · 성형 · 운전 압력 · 코인셀 부품 · 온도 제어 · 장비 **인쇄 0**(G1 · G3).
- 전도도 셋은 **25 ℃ 이름표**("σ25ºC") · 출처 · 측정 0(G2) · 시험 60 ℃.
- `[재현]` C-rate 삼각: 0.55 mAh · 1 cm² → 1C = 0.55 mA cm⁻² · 2.8 mA = **5.09C** ✅("5C") · 2.8 mA cm⁻². 비용량 · 적재는 인쇄 0 이라 삼각의 셋째 변(mAh g⁻¹)은 닫히지 않는다.

## §2.2 다중정현 설계 (p. 2–3 · 식 1)

`[인쇄]` "the random phase multisine, which belongs to the extended class of Gaussian signals with a fixed power spectrum" · "This paper's main interest is to analyze the nonlinear behavior caused by low cathode ionic conductivities; therefore, we focused at low frequencies (f < 1 Hz) where diffusion reaction has the most contribution to the output voltage." · **식 1** u(t) = Σ_{n=−N}^{N} (Aₙ/2) e^{j(2πfₙt+θₙ)} = Σ_{n=1}^{N} Aₙ cos(2πfₙt + θₙ) · "The amplitude of all sines is identical and their phases are selected randomly between [0,2π]." · "The input u(t) is repeated P times" · "**The robustness of this method highly depends on the repeating number M with different phase realization**" · "The maximum current amplitude is limited to 2.8 mA (5C) which is 5 times larger than cell nominal capacity, 0.55 mAh. As can be seen in Fig. 2.b, each excited sine (blue dots with −70 dB amplitude) is quite larger than the noise level, which appeared as a very small amplitude around −160 dB." · "As multisine is made from the accumulation of sine waves, it is zero mean, inherently. Therefore, at the end of the measurement, the state of charge remains the same as it was at the beginning of the test." · "**During input excitation design, it has been considered that the SoC variation should not be more than 1%. This constraint helps to neglect OCV variation during the multisine test.**"
- 설계 변수로 인쇄된 것: 대역 상한(f < 1 Hz — "diffusion" 근거) · 등진폭 · 무작위 위상 · M · P · 첨두 · SoC 변화 상한. **정보 기준(FIM · D-optimality · 분산 최소) 0** — 설계 목적은 "robustness" 와 잡음 · 과도 제거다(§(d)).
- `[재현·가정]` 선 진폭: 그림 6a 여기 선 −72 dB 를 "선 진폭(A 단위)" 정규화로 읽으면 **≈0.25 mA(≈0.46C)** → 등진폭 33 선의 RMS = 0.25·√(33/2) ≈ **1.02 mA** · 파고율 2.74 ÷ 1.02 ≈ **2.7** — 그림 2a 화소 포락선 0.72–1.09 mA 안 ✅(정규화 가정 — 단위 미인쇄 D4).
- `[재현·가정]` 최저 선(4 mHz) 하나의 SoC 진폭 = A/(2πf·Q) = 0.25 mA ÷ (2π · 0.004 s⁻¹ × 1980 mA s) ≈ **0.50 %(정점 간 1.0 %)** — 등진폭 설계에서 **최저 선 하나가 이미 "≤1 %" 경계**이고, 12 mHz 선이 더해 그림 2c 의 1.55 % 가 된다(D3 의 산술 원인 · `[해석]`).
- `[재현·가정]` 통과 전하: 평균 |I| ≈ √(2/π)·RMS ≈0.81 mA(가우스 근사) → 주기당 ≈203 mA s = 0.056 mAh(공칭의 10 %) · 식별 자료 24 주기(100 분)에 ≈1.36 mAh = **공칭 용량의 ≈2.5 배를 양방향으로** 흘린다(알짜 0).

## §3 선형 · 구조 비선형 모형 (p. 3–4 · 식 2–12 · 그림 3)

`[인쇄]` "a structured nonlinear system has been considered … a transfer function model that handles the linear part of the system. Two nonlinear functions at the input and output of the linear system take care of the nonlinear distortions and, in the end, open circuit voltage (OCV) is added to the estimated voltage."
- **§3.1 BLA**: 식 2 측정 u^[r,p](k) · y^[r,p](k)(r = 1…M · p = 1…P) · 식 3 FFT U^[r,p] · Y^[r,p] · "this paper has assumed that the amplitude of the input noise is very small and, therefore, can be neglected, thus inputs in all periods in a realization are identical (U^[r,p] = U^[r])" · **식 4** G_BLA(jω_k) = argmin_G Σ_r |Y^[r](k) − G(jω_k)U^[r](k)|² · 식 5 Ĝ^[r] = Ŷ^[r]/Û^[r] · 식 6–7 주기 평균 · **식 8** Ĝ_BLA = (1/M) Σ_r Ĝ^[r] · "at least two realizations are needed" · "Increasing the number of random phase realizations guarantees the reliability of this method as it increases the time needed for measurement" · "by applying more periods for each realization, we give a chance to the system to reach the steady-state and eliminate the transient state."
- **식 9** σ²_N(jω_k) = [1/(M·(P−1))] Σ_r Σ_p |G^[r,p] − G_p^[r]|² · **식 10** σ²_Total(jω_k) = [1/(M·P − 1)] Σ_r Σ_p |G^[r,p] − G_p|² · **식 11** σ²_S(jω_k) = M·|σ²_Total − σ²_N| — `[인쇄]` "Total variance includes the nonlinear response of the battery as well" · "the variance of nonlinear distortion is calculated based on Eq. (11)". (렌더로 읽음 — 텍스트 층은 깨짐.) → §(b) 3 에서 표준 추정식과 대조.
- **식 12** Ĝ_BLA(jω_k, θ) = B(jω_k)/A(jω_k) = (b₀ + b₁z⁻¹ + ⋯ + bₙz⁻ⁿ)/(1 + a₁z⁻¹ + ⋯ + aₙz⁻ⁿ) · "The parameters of Eq. (12) can be identified by using the least square or maximum likelihood estimation methods, which will not be discussed in detail as they are quite well known [14,57]." — **어느 쪽을 썼는지 · 가중 · 잔차 미인쇄**.

## §3.2 블록 지향 구조 (p. 4–6 · 식 13–32 · 그림 4–5)

`[인쇄]` "in the case of lithium-ion batteries, structured models are quite appropriate for physics-based models as each main or side reaction can be modeled independently [48]. **However, using structures with high complexity makes the parameter identification process very difficult.**"
- **§3.2.1 Hammerstein**: 정적 비선형 f(x) = α₁x + ⋯ + α_p x^p(식 13) → 선형 블록(식 14) · 분모를 곱해 방정식 오차형(식 15) · "the noise level is very low and could be neglected. Therefore, the input noise term e(k) will not be considered in the identification process."
- **§3.2.2 Wiener**: v_l = Ĝ_BLA u(식 16–17) · w = Σ β_t v_l^t(식 18) · 대입한 식 19 — "both output and input coefficients exist in the cost function".
- **§3.2.3 Hammerstein-Wiener**: w = f_w(G_BLA(z) f_h(u))(식 20 — [50,56]) · "no direct access to the linear model is evident initially … split up from the middle"(그림 5) · 미지수 a · b · ζ · γ(식 21) · f_w 역함수(식 24) · 분할점 s_f(식 25–26) · 차를 맞대 식 27 — "**This assumption helped convert the nonlinear problem to bilinear in the parameters a, b, γ, and ζ. Then the bilinear problem can be solved by iterative optimization approaches such as least square or particle swarm optimization (PSO).**" · H-W 에서는 두 비선형을 **구간 선형**(식 28 y = Kₙ + Aₙu, cₙ < u ≤ cₙ₊₁ · c₁ = min(u) · cₙ₊₁ = max(u)) — "the input data is divided into several **arbitrary breaking points** c … It is important that the function continuity at each breaking point must be satisfied. This method gives more degrees of freedom (depending on the number of breaking points)" · 식 29–31 · **식 32** argmin F(a_i, b_l, K_uj, A_uj, K_yj, A_yj) "solved by the least squares method".
- `[해석]` ① **f_w 의 역(식 24)** 은 f_w 가 단조일 때만 있다 — 단조 제약의 인쇄 0(그림 13d 는 단조). ② **쌍선형 매개변수화의 고유한 비식별** — 식 27 은 (a, b) 와 (γ, ζ)의 곱으로 들어가므로 **한 상수 배를 두 묶음 사이에서 옮겨도 같다**; 블록 지향 식별에서는 보통 한 계수를 1 로 고정하는 정규화가 필요하다(일반 성질 · 이 편 지면에 정규화 문장 0). 그리고 이 편은 BLA 를 선형 블록으로 **고정**한 뒤 비선형을 맞췄다(§4.2 "As the linear part has been already identified in Section 4.1, it will be used as a baseline") — 그래도 두 정적 블록 사이의 이득 · 오프셋 교환은 남는다(§(b) 4).
- 결어 `[인쇄]` "Considering the simplicity of the Hammerstein and Wiener systems in comparison with pure physical models, they are a strong and flexible solution … can be implemented for online parameter identification, Furthermore, they increase the accuracy of state of charge estimation." — SOC 추정 정확도 향상은 이 편에서 시험되지 않았다.

## §4 결과 머리 (p. 6–7 · 그림 6)

`[인쇄]` "the input multisine excitation has been designed in **four realizations and each realization is repeated six times (6 periods). Accumulation of 33 individual sine waves with identical amplitude but randomly selected phases** have been implemented in each multisine realization. **The frequency of each sine is selected from odd indexes and is in the range of 4mHz up to 1 Hz. The measurement sampling frequency is 10 Hz** and it is already 10 times larger than the highest multisine frequency, which is 1 Hz. The maximum current altitude has been limited to 2.8 mA (5C)." · "the SNR … of excited frequencies is at least 70 dB (≈3200 times larger than the noise level)" · "In Fig. 6b, the SINAD … of the measured voltage is approximately 50 dB (320 times larger), which is still large enough to neglect the distortions" · "in the case of cell 2, the SINAD … has been considerably reduced to less than 15 dB (around 5 times larger than the distortion level), which cannot be neglected anymore as it causes huge errors and uncertainty in the whole model. **As the measurement noise is negligible, all anomalies in output voltage are approximated as pure distortion caused by the nonlinear nature of the cell 2.**"
- `[재현]` 20·log₁₀: 70 dB = ×3162(≈"3200") ✅ · 50 dB = ×316(≈"320") ✅ · 15 dB = ×5.6("around 5") ✅ — 진폭 관례.
- `[재현]` f₀ = 1/250 s = 4 mHz(그림 2a) · Np = 2500 표본/주기 · 식별 자료 = 4 × 6 × 250 s = **6000 s(100 분) · 60,000 표본** + 검증 실현(주기 수 미인쇄 — 그림 9 는 250 s 한 주기).

## §4.1 선형 모형 (p. 7–8 · 그림 7–9)

`[인쇄]` "As is expected, the amplitude of linearized impedance of **cell 1** increased around 12 times as ionic conductivity reduced approximately 10 times. However, in cell 2, the level of nonlinear distortion has been increased more than 100 times, which is totally unproportioned with the reduced amount of conductivity." · "**a 3rd order discrete FIR (of finite impulse response) transfer function in the z domain** has been considered for the linear system" · Nyquist "The first point is that the curve has been shifted to the right side, which is considered as ohmic resistance increase due to lower ionic conductivity in cell 2. The second important point is the growth of the diffusion impedance (45º line in Nyquist plot) for real as well as the imaginary part. **As we deliberately increased the boundary resistance between solid electrolyte and active material in the cathode**, the ohmic resistance increase was expected. However, as ionic conductivity has been decreased, the LiCoO2 particles on the surface of the cathode consume more lithium as concentration is increased [5]." · 검증 "with a multisine excitation other than the ones used for the identification algorithm" · "a linear model is sufficient as the maximum voltage error is around 3 mV" · 셀 2 "the model error reaches to 0.8 V".
- "cell 1" → 문맥상 셀 2(D2) · "FIR" ↔ 식 12 IIR(D1 — `[해석]` FIR 의 |H| 는 직류 근처에서 평탄하거나 오르므로 저주파로 갈수록 커지는 |Z|(그림 8a 46.6 → 53 dB)를 3 탭으로 못 그린다) · "boundary resistance" ↔ 벌크 전도도(D5) · [5] Kato 2016 이 "표면 LCO 가 더 많은 Li 를 소비" 의 근거인지 미확인(후속 ★).
- `[해석]` "45º line" — 그림 8c 셀 2 저주파 가지의 점 사이 기울기는 ≈29°((236, 36) → 0.044 Hz 점) · ≈40°(0.044 → 0.012 Hz) · ≈59°(0.012 → 0.004 Hz)(`[도표·화소]`) — 45° 직선이 아니라 저주파로 갈수록 가팔라지는 곡선(확산 → 용량성 쪽)이고, 45° 를 넘는 것은 최저 두 선 사이뿐이다.

## §4.2 비선형 모형 (p. 8–10 · 그림 10–12)

`[인쇄]` "Series Hammerstein-wiener structured models have been chosen to model the nonlinear characteristic of **the cell 2**" · H: "identified based on a **third-order polynomial** … the Hammerstein model accuracy is **74.5%, which provides 6% less RMS error than the linear model** … the input distortion is not normally distributed, especially in the discharge zone … these data is not responding very well to the Hammerstein system" · W: "a **sixth-order polynomial** function … reached **81%, which shows a 6.5% improvement** when compared with the Hammerstein model … the distortions in the charge zone is almost linear and in the discharge zone, it has a logarithmic pattern. However, the model still is not accurate enough as it couldn't predict severe voltage drops during discharge." · H-W: "this configuration has the potential to provide a good fit … as this system has a third degree of freedom" · "In order to reduce the calculation efforts, the piecewise-linear method has been used" · "**The Hammerstein curve in Fig. 12a is different from the one seen in Fig. 10a, which will be investigated more in the following sections.** However, the patterns of the Wiener curve are almost the same with a slight difference in output range" · "The Hammerstein-Wiener model has been validated … The total accuracy has reached **86.5%** and the model has kept the accumulation of the individual Hammerstein and Wiener accuracies together" · "It has been proposed and proved that, by using block-oriented nonlinear modeling, the model accuracy and flexibility can be improved remarkably."
- `[재현]` 범례 68.5(선형) · 74.5 · 81 · 86.5 % → 차 **6.0 · 6.5 · 18.0** ✅(본문 · 결론 "increased the accuracy by 18%" = **백분율 포인트** · 상대로는 +26 %) · H · W 각각의 향상 6.0 + 12.5 = **18.5 ≈ H-W 18.0** ✅("accumulation").
- `[재현·가정]` "accuracy" 를 정규화 RMS 적합도 100·(1 − ‖e‖/‖y − ȳ‖) 로 읽으면(정의 인쇄 0) ‖e‖/‖y − ȳ‖ = 0.315 · 0.255 · 0.19 · 0.135 → "6 % less RMS error" 는 표준편차 대비 6 %p 이고 상대로는 −19 %.
- "has been validated" — 비선형 모형의 학습 자료와 검증 자료가 다른 신호인지 인쇄 0(G6). 그림 9b · 10b · 11b · 12c 의 측정선은 같은 궤적(선형 검증 실현)이다(`[도표]`).
- "proposed and **proved**" — 셀 하나 · 실현 하나의 적합 향상이다.

## §4.3 물리 해석 (p. 10–11 · 식 33–35 · 그림 13)

`[인쇄]` "the ionic conductivity of cell 2, deliberately, has been reduced 10 times by using different materials **in the interface of cathode active material and solid electrolyte**. Therefore, we almost know where the source of nonlinear distortion is" · "the identified Hammerstein and Wiener functions for cell 1 gives totally linear curves for inputs and outputs (Y = X) … In the Hammerstein curve, in Fig. 13b, obviously, the input galvanostatic current has been limited by some internal causes and becomes saturated in the case of values bigger than 2 mA. On the other hand, in the Wiener curve in the discharge zone, as shown in Fig. 13d, the output voltage drops logarithmic for amplitudes smaller than −0.4" · "During charge, lithium ions migrate from the cathode to the anode and intercalate in graphite particles. **Due to high ionic conductivity (10⁻³ S/cm) in the anode and separator layer, no nonlinearity has been detected in the charge zone**".
- **Remark 1** `[인쇄]` "During discharge, lithium ions intercalate into cathode particles, where the non-uniformities are taking place. As LiCoO2 particles are surrounded by very low ionic conductive materials (10⁻⁵ S/cm), the LiCoO2 close to the separator is the easiest target … if the intercalation rate becomes very high, then the lithium concentration at the surface layer of the active particle reaches the maximum amount and causes high voltage drops. These phenomena, so-called **Nernst diffusion layer**, are formulated in Eq. (33)" — **식 33** V_diff = (RT/F) Ln(C_s/(C_sm − C_s)) · "those logarithmic voltage drops … could originate from the Nernst layer [59]".
- **Remark 2** `[인쇄]` BV **식 34** j^BV = j₀·(e^{α_o η(x)/u_T} − e^{−α_r η(x)/u_T}) (u_T = RT/F) · **식 35** j₀ = F·k_c·c_e^{α_o}(c_s,max − c_s(0,t))^{α_o}(c_s(0,t))^{α_r} · "when surface concentration increases and reaches maximum c_s,max, the j₀ will be reduced … **Therefore, it can be interpreted that the Hammerstein function indicates the current saturation because of the charge-transfer limit and the Wiener function explains the severe voltage drops due to the mass-transfer limit.**"
- `[해석]` 식 33 · 35 에 **값이 하나도 들어가지 않는다**(c_s · c_s,max · k_c · α · 온도 0) — 배정은 **모양(포화 ↔ 로그 꼴) 대응**뿐이고, 구조를 바꾸면 그 모양이 뒤집힌다(D8 · §(b) 4) · 온도 · 율 · SoC 대조 0. 식 33 은 격자 기체 OCP 의 로그 항과 같은 꼴(표면 농도 포화에서 발산)이고, "Nernst diffusion layer" 라는 이름은 [59](상장 모형 편)에서 왔다.
- "Due to high ionic conductivity … in the **anode** and separator layer" — 음극층 SE 는 §2.1 · 그림 1 어디에도 없다(D7 · G1). 그리고 방전 쪽 비선형을 양극에 돌린 근거가 이 문장 하나다 — 2전극이라 흑연 쪽 몫은 검사되지 않았다(Q5 층).

## §5 결론 · 미래 과제 (p. 11)

`[인쇄]` "Those cells have been characterized at 60 °C with galvanic multisine excitation as input. Measurement results indicated that the measured voltage in cell 2 contains very high levels of nonlinear distortion, despite cell 1, for which the measured data was totally linear." · "the Hammerstein-Wiener system increased the accuracy by 18% compared to the conventional transfer function based linear model" · "This paper proposed that the identified Hammerstein and Wiener functions are related to charge and mass-transfer respectively." · 미래 과제 "more complex nonlinear structures such as parallel and feedback systems … by implementing the nonlinear model for online parameter estimation in a battery pack **coupled with an online fault detection algorithm**, we can increase the safety and reliability of the energy storage system."
- "totally linear"(셀 1) ↔ 그림 7 셀 1 상대 왜곡 −34 … −55 dB(`[재현]`) — 작지만 0 은 아니다(최저 선 −34 dB = 2 %).
- 결론은 물리 배정을 "proposed" 로 낮췄다(본문 "proved" 와 다른 수위).

---

# ★ (a) 셀과 대조군 — "전도도 한 변수" 인가

| 항목 | 셀 1 | 셀 2 | 출처 층위 |
|---|---|---|---|
| 양극 활물질 | LiNbO₃-coated LiCoO₂ | 같음 | `[인쇄]` p. 2 |
| **양극층 SE** | **Li₂S-P₂S₅ glass** | **γ-Li₃PS₄** | `[인쇄]` p. 2 · 그림 1 |
| 양극층 SE 전도도 | "σ₂₅ ≈10⁻⁴ S/cm" | "σ₂₅ ≈10⁻⁵ S/cm" | `[인쇄]` 25 ℃ 자릿수 이름표 · **측정법 · 출처 · 60 ℃ 값 0**(G2) |
| 분리막 | LiI-Li₂S-P₂S₅ glass · σ₂₅ 10⁻³ | 같음 | `[인쇄]` |
| 음극 | graphite(층 SE 미기재) | 같음 | `[인쇄]` · p. 10 "anode … 10⁻³" 은 근거 없는 서술(D7) |
| 면적 · 용량 | 1 cm² · 0.55 mAh | "similar" | `[인쇄]` |
| 두께 | 양극 25 · 분리막 500 · 음극 25 µm | 같음 | **그림 1 에만** · 본문 "similar" |
| 조성비 · 적재 · 비용량 · 코팅 두께 | — | — | **인쇄 0**(G1) |
| 성형 · 운전 압력 · 코인셀 부품 · 하중 | — | — | **인쇄 0** — `pressure` · `MPa` · `spring` · `torque` 0 회 |
| 온도 · SoC | 60 ℃ · 50 % | 같음 | `[인쇄]` 그림 2 캡션 · 결론 · §4 |
| 셀 수 | **1** | **1** | `[인쇄]` "two solid-state coin cells" |
| 제조 | Toyota Motor Europe | 같음 | `[인쇄]` 사사 |

- `[재현]` **분리막 옴 상한 검사**: 500 µm ÷ (10⁻³ S/cm × 1 cm²) = **50 Ω** ↔ 셀 1 의 **전체** Re(1 Hz) ≈20–21 Ω(`[도표·화소]` 그림 8c) → 60 ℃ 에서 분리막 전도도가 인쇄 25 ℃ 값의 **≥2.4 배**여야 그림이 선다(두께가 그림 1 그대로라면). 같은 이유로 **양극층 두 SE 의 60 ℃ 비가 "10 배" 인지는 지면에 없다** — 유리 ↔ 결정 γ 상의 활성화 에너지가 다르면 비는 온도에 따라 바뀐다(`[해석]` · 값은 원전 미대조라 적지 않는다).
- `[재현·가정]` **벌크 옴 자릿수 대조**: 양극층을 조밀 평판(σ_eff = σ₂₅)으로 놓으면 25 µm ÷ σ = 25 Ω(셀 1) ↔ 250 Ω(셀 2) — 차 225 Ω 이 그림 8c 의 1 Hz 실부 차 **≈189 Ω**(209.5 − 20.5)과 **자릿수만** 맞는다. 복합 전극은 σ_eff < σ(부피 분율 · 굴곡도)라 차를 키우고, 60 ℃ 는 줄인다 — 두 미지가 반대로 움직여 **검사로 쓸 수 없다**(조성 · 온도 값이 지면에 없다).
- ★ `[해석]` **재료 교체는 σ 하나만 바꾸지 않는다** — Li₂S-P₂S₅ 유리와 γ-Li₃PS₄(결정)는 변형성(압착 시 CAM 과의 접촉 면적) · 입자 형태 · LiNbO₃ 와의 계면 화학 · 전위 창이 다를 수 있고, 지면은 이 중 어느 것도 재거나 같다고 확인하지 않는다(접촉 · 형태 · XPS · 대칭셀 0). 그런데 같은 조작을 지면이 세 이름으로 부른다: **"ionic conductivity inside the cathode layer"**(p. 2) · **"boundary resistance between solid electrolyte and active material"**(p. 7) · **"different materials in the interface of cathode active material and solid electrolyte"**(p. 10 · 초록 "at the cathode interface") — **벌크 수송 ↔ 계면 저항**이 한 조작의 이름으로 섞인다(D5). ⇒ 셀 2 의 비선형을 "전도도" 에 돌리는 것은 **재료 교체에 함께 실린 변화 전부**에 돌리는 것이다 — 카드 물음(접촉 손실 ↔ LAM_PE)의 언어로는 **"접촉 · 계면 · 수송이 한 손잡이에 묶인 대조"**.
- **코인셀 하중 칸 (원장 §3-b (배))**: 값 미인쇄 코인셀 ASSB 표본 하나 더 — 이 편은 **성형 압력까지 0**이고 셀은 TME 제작이라 공정이 지면 밖에 있다. (배)의 셋째 칸(셀 형식 하중)에 "값 0 · 성형 0" 으로만 들어간다.

---

# ★ (b) 식별의 실체 (Q4)

## 1. 입력 설계 — 인쇄한 것 · 재구성한 것

| 설계 변수 | `[인쇄]` | 우리 재구성 | 비고 |
|---|---|---|---|
| 신호 | random-phase multisine · 등진폭(식 1) | — | Schoukens 계보 [40–45] |
| 선 수 · 대역 | 33 · "odd indexes" · 4 mHz–1 Hz | `[도표·화소]` **k = 1 · 3 · 11 · 19 · … · 251**(f₀ 4 mHz) · 최고 1.004 Hz | **선형 격자** — 0.04 Hz 아래 **2 선** · 0.04–0.4 Hz 12 · 0.4–1.004 Hz 19 |
| 주기 · 표본 | f_s 10 Hz | `[재현]` T = 250 s(그림 2a) · Np 2500 | 나이퀴스트 5 Hz = 그림 2b · 6 축 끝 ✅ |
| 실현 · 주기 수 | M = 4 · P = 6 | `[재현]` 6000 s(100 분) · 60,000 표본 + 검증 실현 | "at least two realizations are needed" |
| 진폭 | 첨두 ≤2.8 mA(5C) | `[도표·화소]` 첨두 ±2.74 mA · RMS 0.72–1.09 mA · `[재현·가정]` 선 진폭 ≈0.25 mA · RMS ≈1.02 mA · 파고율 ≈2.7 | **진폭 수준 하나** |
| 상태 제약 | SoC 변화 ≤1 % · 50 % SoC · 60 ℃ | `[도표·화소]` 49.98 → 48.86 → 50.40 %(−1.12 % · p-p 1.55 %) | 최저 선 하나로 이미 p-p ≈1.0 %(`[재현·가정]`) |
| 설계 기준 | "robustness … depends on the repeating number M" · 과도 제거 · 잡음 상쇄 | — | **정보 기준 0**(FIM · D-optimality · 분산 최소화 0 회) |

`[해석]` 저자가 겨냥했다고 인쇄한 확산 대역("f < 1 Hz where diffusion reaction has the most contribution")에 대해 선형 격자는 **에너지를 위쪽 끝에 쏟는다** — 4–40 mHz(한 디케이드)에 2 선 · 0.4–1 Hz 에 19 선. Nyquist(그림 8c)에서 셀 2 의 저주파 가지가 점 넷뿐이고 나머지가 한 덩어리로 겹치는 것이 그 결과다.

## 2. BLA 가 가르는 것 — "분산" 은 매개변수의 분산이 아니다

`[인쇄]` 식 9 "noise variance" · 식 10 "total variance of BLA … includes the nonlinear response" · 식 11 "the variance of nonlinear distortion". 셋 다 **주파수 선 하나하나에서 FRF 값이 주기 · 실현 사이에 흔들리는 폭**이다 — 잡음(주기 사이)과 **확률적 비선형 왜곡**(위상 실현 사이 — 비선형계가 무작위 위상 입력에 대해 선마다 내는 "가짜 FRF" 의 흔들림)을 가른다. **전달함수 계수 · 다항 계수 · 꺾인점의 분산 · 공분산 · 신뢰구간은 하나도 계산되지 않는다.** 그리고 그림 7 은 σ_S 만 그리고 σ_N 은 그리지 않는다(G8).

## 3. 식 9–11 ↔ 표준 강건 추정식 (`[재현]` — 기대값 산술 + Monte Carlo · 코드 `scratchpad` · 커밋 안 함)

표준(주기 · 실현 구조): 실현 평균 FRF 의 잡음 분산 = (1/(P(P−1))) Σ_p |G^[r,p] − Ĝ^[r]|² · BLA 잡음 분산 = (1/M²) Σ_r(그것) · BLA 총분산 = (1/(M(M−1))) Σ_r |Ĝ^[r] − Ĝ_BLA|² · **실현당 확률적 왜곡 분산 = M(총 − 잡음)** — 앞 두 양이 **평균의 분산**이라 ×M 으로 실현 하나 단위로 되돌린다.
인쇄 식은 식 9 · 10 이 이미 **한 주기 FRF 의 분산**(평균의 분산이 아님)이다. G^[r,p] = G_BLA + S_r + N_rp(S 실현 왜곡 · N 주기 잡음)로 놓으면 E[식 9] = σ_N² · **E[식 10] = σ_N² + P(M−1)/(MP−1)·σ_S²** → **E[식 11] = M·P(M−1)/(MP−1)·σ_S² = 3.13 σ_S²**(M 4 · P 6). Monte Carlo(20 만 회) **3.129 σ_S²** ✅ · 표준식 0.9996 σ_S² ✅ → **인쇄 식대로 계산했다면 그림 7 의 σ_S 는 실현당 왜곡보다 진폭으로 ≈+5.0 dB 크다.** 두 셀에 같은 배수라 "셀 2/셀 1" 비(D12)는 그대로이고, 절대 수준("NL dist cell2 ≈ BLA cell1 수준")만 움직인다. 그리고 식 11 의 |·| 는 잡음이 왜곡보다 큰 선(셀 1 고주파 쪽)에서 음수 추정을 양수 "왜곡" 으로 바꾼다. ⚠ 저자 코드가 인쇄 식과 같은지는 모른다(식 1–8 의 원전 [46] 대조 — 후속 ★★).

## 4. ★★★★ 구조적 비식별 — 블록 사이 이득 · 오프셋 교환, 그리고 구조를 바꾸면 뒤집히는 모양

- **대수(일반 성질 · `[재현]`)**: 선형 블록 G 를 BLA 로 고정해도 H-W 의 두 정적 블록은
  (i) **이득 교환** `f_h → k·f_h` · `f_w(v) → f_w(v/k)` (k > 0)
  (ii) **오프셋 교환** `f_h → f_h + c` · `f_w(v) → f_w(v − G(1)·c)` (G(1) = 직류 이득)
  에 대해 **출력이 같다**. 우리 수치 점검(구간 선형 f_h · f_w + 임의 안정 G · 5000 표본): k = 0.5 · 2 에서 출력 차 **0**(기계 정밀도) · 오프셋 c = 0.3 에서 과도 뒤 **3×10⁻¹³**. ⇒ 블록 하나하나의 "선형선(Y = X)에서의 이탈"(그림 13)과 **f_w 의 꺾인점(선형 모형 출력 좌표 "−0.4")** 은 인쇄되지 않은 정규화에 달렸다(k = 2 면 −0.9 V · 0.5 면 −0.23 V). 불변인 것은 **입력 좌표의 f_h 꺾인점(≈ −0.7 · −1.8 mA)** · **충전 쪽 두 기울기의 곱**(1.09 × 0.84 ≈0.91 `[도표·화소]`) · 전체 입출력 사상이다. 지면에 정규화 문장 · `normali*` · `gain` · `scal*` **0 회**.
- **구조 의존 모양(지면 안 증거 · D8)**: 같은 셀 · 같은 자료에서 입력 블록이 **H 단독(그림 10a · 3차 다항) 방전 쪽 확장(−2.75 → −4.15 mA · 평균 기울기 ≈1.5)** ↔ **H-W(그림 12a · 13b · 구간 선형) 방전 쪽 포화(1.44 → 0.84 → 0.40)** 로 **반대 곡률**이다. `[해석]` 출력 블록이 없으면 입력 블록이 출력 쪽 급락까지 떠안아 확장하고, 출력 블록이 생기면 그 급락을 출력 블록이 가져가고 입력 블록은 오히려 포화한다 — **비선형을 두 블록에 나누는 몫이 데이터가 아니라 구조 선택으로 정해진다.** 저자는 차이를 인쇄하고 "will be investigated more" 라 했으나 §4.3 은 13b 하나로 "charge-transfer limit" 을 배정한다.
- ⇒ **"Hammerstein = 전하이동 · Wiener = 물질전달" 배정은 (i) 정규화 의존 모양과 (ii) 구조 의존 모양 위에 서 있다** — 식 33 · 35 에 값도 넣지 않았다. 이 배정을 카드로 옮길 수 있는 층위는 "모양 비유" 다.

## 5. 차수 · 꺾인점 · 비용 · 검증

| 항목 | `[인쇄]` | 근거 · 결과 |
|---|---|---|
| 선형 블록 | "3rd order discrete FIR" ↔ 식 12 유리함수 | 차수 선택 근거 0 · LS 인지 ML 인지 미인쇄 · 계수 0 · `[해석]` FIR 로는 저주파 상승 \|Z\| 불가(D1) |
| H 블록 | 3차 다항식 | 근거 0 · 계수 0 |
| W 블록 | 6차 다항식 | 근거 0 · 계수 0 |
| H-W 블록 | 구간 선형 · "arbitrary breaking points" · 연속 조건 | 꺾인점 수 · 위치 인쇄 0 — `[도표·화소]` f_h ≈4(−1.8 · −0.7 · 0 · +0.45 mA) · f_w ≈3–4(−0.45 · −0.3 · −0.15 V …) |
| 비용 | 식 32 최소제곱(쌍선형 · "least square or PSO") | 반복 · 시작점 · 수렴 · 잔차 0 |
| 검증 | 선형: "a multisine excitation other than the ones used for the identification" ✅ · 비선형: "has been validated" | 비선형 블록 학습 자료 미인쇄(G6) · 그림 9b · 10b · 11b · 12c 측정선 = 같은 한 주기 |
| 적합 지표 | accuracy 68.5 · 74.5 · 81 · 86.5 %(범례) | **정의 0** · `[재현]` 차 6.0 · 6.5 · 18.0 ✅ · H + W 향상 합 18.5 ≈ H-W 18.0 |

## 6. 어휘 (요약 — 전체는 아래 "어휘 집계")

`identifiab*` · `confiden*` · `sensitiv*` · `Fisher` · `Cram(é)r` · `D-optim*` · `persisten*` · `normali*` · `gain` · `scal*` · `±` · `standard deviation` · `residu*` **0**(NFKC 전후 같음) · `uniqu*` **1**("brings them all together in a unique model" — 하나의 모형) · `uncertain*` **1**("huge errors and uncertainty in the whole model" — SINAD 문장) · `variance` **6**(전부 BLA 잡음 · 왜곡) · `identif*` 43(전부 "identification · identified" — 적합의 뜻) · `accura*` 20 · `validat*` 4 · `error*` 7.

## 7. 판정 (Q4)

**Q4 0/92 — 여든네 번째 성질.** 기준(10호 이래 — "이 조합은 이 데이터로 유일하게 정해지지 않는다" 를 지면이 계산으로 보였나): **0**. 이 편은 **식별(identification)을 "구조를 고르고 맞추는 일"** 로 쓰고, 그 결과를 그림으로만 남겼으며(값 · 불확실도 0), BLA 의 분산(잡음 · 왜곡)을 매개변수 분산 자리에 두지 않았고(맞다 — 그러나 매개변수 분산은 아예 없다), 블록 지향 구조에 원래 있는 **이득 · 오프셋 교환(구조적 비식별)** 을 정규화로 닫지 않은 채 블록별 모양에 물리를 배정했다 — 그 모양은 구조를 바꾸면 뒤집힌다.
**여든네 번째 성질 = "제목에 'system identification' 을 걸고 ASSB 계보 첫 설계 가진(무작위 위상 다중정현)을 썼으나, 그 설계가 산 것은 선형 ↔ 비선형 ↔ 잡음의 분리이고(BLA '분산' = 잡음 · 왜곡 분산 · 인쇄 식대로면 ≈+5 dB 과대), 식별한 블록의 값 · 불확실도 · 블록 사이 정규화(입력 설계로 못 사는 이득 · 오프셋 교환)를 인쇄하지 않은 채, 구조를 바꾸면 곡률이 뒤집히는 입력 블록(H 단독 확장 ↔ H-W 포화)에 전하이동 · 물질전달을 배정했다."**
⇒ 원장 §2 **구조적 공백 1번("역문제 · 식별성을 다루는 ASSB 논문") — 이 편은 후보에서 내려가고 공백은 그대로**(75호 Naik 2022 확인과 같은 형식의 "확인으로 닫음").

---

# ★ (c) "고장 검출" 주장 — 무엇이 검출되고 무엇이 귀속되나

## 1. 검출 장치의 실체

| 요소 | 지면 |
|---|---|
| 통계량 | 정성 대비 두 개 — SINAD ≈50 → <15 dB(그림 6) · NL 왜곡 ">100 times"(그림 7) · 모형 정확도(68.5 → 86.5 %) |
| 문턱 · 오경보 · ROC | **0** |
| 대조 | 셀 1(정상 역할) ↔ 셀 2("고장" 역할) — **각 하나** · 고장 = 일부러 바꾼 재료(진행형 고장 0) |
| 교란 | 온도 60 ℃ 하나 · SoC 50 % 하나 · 진폭 하나 · 셀 산포 0 · 노화 0 |
| 절차 | 초록 "the developed model has been utilized to detect possible faults" ↔ 본문 0 · 미래 과제 "coupled with an online fault detection algorithm"(D15) |

## 2. ★★★ 교란 — 같은 전류 진폭은 같은 시험이 아니다

- `[도표·화소]` 두 셀의 |Z| 비 **×10.5–12.4**(그림 7) → 같은 전류(첨두 2.74 mA)에서 **셀 1 단자 전압 ≈3.75–3.86 V(±0.05 V) ↔ 셀 2 ≈2.26 … ≈4.2 V**(그림 9). 60 ℃ RT/F = **28.71 mV**(`[재현]` 8.3145 × 333.15 ÷ 96485) — 셀 2 는 모형 중심(≈3.6 V)에서 아래로 ≈1.3 V(RT/F 의 ≈45 배) · 위로 ≈0.6 V 를 오간다. "50 % SoC 의 소신호 측정" 이 셀 2 에서는 **방전 컷오프 근처까지 가는 대신호 측정**이다.
- `[재현·가정]` 단일 BV 계면(대칭 α 0.5): η = (2RT/F)·asinh(I/(2A·j₀)) → 전개 η ≈ R_ct·I − (F/RT)²·R_ct³·I³/24(R_ct = RT/(F·A·j₀)) → **3차 상대 왜곡 ≈(F/RT)²·(R_ct·I)²/24 — 고정 I 에서 R_ct 의 제곱**. R_ct 가 ×12 면 상대 왜곡 ×144(+43 dB), 절대 왜곡 ×1728(+65 dB). 그림 7 의 관측(상대 +11.5 … +33 dB · 절대 +31 … +72 dB)은 이 자릿수 안에 있다 — 셀 2 의 늘어난 임피던스 중 큰 몫이 선형(옴 · 수송)이면 덜 늘고, 국소 전류 집중이면 더 는다(`[해석]` — 어느 쪽인지 지면으로 못 가른다).
- ⇒ **"비선형도 수준" 은 고정 전류 진폭에서 '활성 계면 면적당 분극' 의 가파른 함수**이고, 그것을 올리는 것은 **양극층 전도도 저하(분리막 쪽 입자로 전류 집중 — 저자 Remark 1 의 그림)** · **접촉 손실(남은 접촉으로 전류 집중)** · **LAM_PE(남은 입자로 집중)** · **계면층(j₀ ↓)** · **SoC 이동(j₀(x) · 표면 농도 포화 — [58] "low SoC")** · **온도 ↓** — **전부 같은 방향**이다(`[해석]`).
- 그리고 순수 BV 는 `I/(A·j₀)` 하나로만 들어간다(`[재현]` 위 식 — 항등) → **비선형 진폭 채널은 면적 ↔ j₀ 곱을 가르지 못한다**(곱 축퇴의 비선형판). 면적을 따로 보는 것은 여전히 `C_dl ∝ A`(처방 1단계) 또는 면적 스케일이 다른 수송 비선형(입자 확산 — 면적당 플럭스로 표면 농도가 움직인다)이다 — 이 편은 둘 다 없다(대역이 계면 호 아래 · `C` 0).

## 3. 두 셀 차이를 "비선형도 차이" 로 읽는 것이 성립하는 조건

1. **진폭을 전압 기준으로 맞추거나 진폭을 둘 이상 스윕** — 같은 전압 진폭에서 순수 BV 두 셀(j₀ 만 다름)은 **같은 상대 왜곡**을 낸다(`[재현·가정]` x = I/(2A·j₀) 같음). 그래도 남는 차이가 "진짜" 비선형 구조 차이다. 이 편: 진폭 하나 · 전류 기준.
2. **상태 고정 확인** — 셀 2 는 측정 중 2.26 V 까지 내려가고(그림 9b) SoC 는 설계 상한을 넘는다(그림 2c). 상태 이동이 왜곡에 섞인다.
3. **셀 산포** — 같은 재료 셀 둘 이상(n = 1 · 1).
4. **전극 분해** — 3전극 또는 대칭셀(2전극 · 흑연 몫 미검사 · "anode σ 10⁻³" 근거 0).
5. **재료 교체의 교락 목록** — σ 외에 접촉 · 형태 · 계면 화학이 같은지(§(a)).
⇒ 이 다섯이 없으므로 이 편이 보인 것은 **"양극층 SE 를 바꾼 셀 하나는 같은 전류에서 훨씬 비선형이다"** 까지다. "이온 전도도 차이 → 비선형도 차이" 의 인과도, "비선형도로 계면 고장을 검출" 도 이 지면에서 서지 않는다(조건부).

## 4. Q2 · Q1 판정

- **Q2(접촉 손실 ↔ LAM 독립 관측)**: **없다** — 관측 채널이 하나(단자 전압의 비선형)이고, 그 채널은 위 2 처럼 접촉 · LAM · 계면 · 수송을 같은 방향으로 본다. 오히려 **"비선형도는 귀속 채널이 아니다"** 의 표본이다.
- **Q1(접촉 손실 정량)**: **없다**(`θ(N)` 0/92 · `contact` 0 회 · 열화 0) — 층 하나: "고정 전류 진폭 비선형도 = 활성 면적당 분극의 단조 함수 — 검출 쪽 대리량 후보, 단위 · 사상 0".
- **Q2 계면층 ↔ 접촉 손실([[assb-interphase-vs-contact-loss-attribution]])**: 저자는 같은 조작을 전도도 · 경계 저항 · 계면으로 부르고(D5), 물리 배정은 "전하이동(H) · 물질전달(W)" — 두 비-LAM 기구 어느 쪽으로도 가르지 않는다. 가르는 입력(`R`·`C` · 온도 · 대칭셀) 0.

---

# ★ (d) 34호 처방과의 관계 — 입력 설계로 무엇을 샀나

| 34호(Liang 2026 Comment)가 처방한 것 | 92호에서 | 판정 |
|---|---|---|
| "observability is redefined as a controllable resource" — 입력을 설계해 정보를 산다 | 입력을 **실제로 설계했다**(무작위 위상 · 등진폭 33 선 · M · P · 대역 · 상한) — **ASSB 계보 첫 설계 가진 실측**(위키 grep `multisine` · `다중사인` · `random phase` · `PRBS` · `chirp` — ASSB digest 0 · 액체셀 49호 하나) | ✅ 설계는 있다 |
| FIM · CRLB · **D-optimality** 로 진폭 · 폭 · 순서를 정하라 | 설계 기준 = 잡음 상쇄 · 과도 제거 · 실현 수("robustness") · SoC 상한 — **정보 기준 0** | ❌ |
| 진폭 · 폭 · 순서를 함께 최적화 | **진폭 한 수준** · 선형 격자(저주파 2 선) · 위상 무작위(최적화 아님) | ❌ — 비선형 구조 식별에 정작 필요한 축(진폭)이 설계되지 않았다 |
| PE(지속 가진) | 다중정현 = 주기 가진 · 33 선(선형 블록 3차 계수 일곱 남짓에는 충분 · `[해석]`) | ⚠ 선형 블록에는 충분 · 정적 비선형은 방문한 진폭 범위(±2.74 mA)에서만 정해진다 — 그런데 그림 12 · 13 은 ±3.3 mA 까지 그린다(D11) |
| 34호 `[해석]` "구조적 비식별(모든 u 에서 FIM 특이)에는 D-optimality = 0" | **블록 이득 · 오프셋 교환**(§(b) 4) — 어떤 입력으로도 안 풀리는 구조적 비식별이 이 모형에 실제로 있다 | ✅ 34호 경고의 구체 표본 |
| — | 설계가 **산 것**: BLA 의 잡음 ↔ 확률적 왜곡 분리 · 선형 ↔ 비선형 판정(구조 판정) | 매개변수 식별성이 아니라 **구조 판정**을 샀다 |

⇒ **새 성질이다** — 34호 "식별성을 입력 설계로 살 수 있는 자원으로 인쇄했다(스물여섯 번째)" ↔ **92호 "입력 설계를 실제로 한 첫 ASSB 편 — 산 것은 구조 판정(선형 ↔ 비선형 ↔ 잡음)이고 매개변수 식별성은 사지 않았다(값 · 불확실도 0 · 구조적 교환은 입력으로 못 산다)"**(여든네 번째). 두 편을 나란히 놓으면 "입력 설계" 라는 낱말이 **정보량 설계(34호 처방)** 와 **분리 설계(92호 실측 — Schoukens 계보)** 두 뜻으로 쓰인다 — 카드 · 개념으로 옮길 때 어느 뜻인지 적어야 한다(새 판단 거리 셋째).

---

# ★ (e) 우리 합성 truth · 모형에 주는 것 (`ASSB_TRANSFER_NOTE.md` §2–§4 를 읽기만 · `[해석]`)

| 이 편의 것 | 우리 쪽 자리 | 넘기나 |
|---|---|---|
| 고정 SoC 다중정현 · OCV 는 상수로 "더함"(값 0) | §4 하네스(OCV 곡선 → α·β) | ❌ **직교** — OCV 정보 0 · 정적 몫은 버린 측정이다 |
| BLA(선형 FRF) + 실현당 왜곡 분산 σ_S(주파수별) | §3 1단계(셀 0 · 합성 truth 의 순방향 관측 후보) | ⚠ **관측 후보로만** — 합성 truth 에 "다중정현 진폭 둘 이상에서 BLA + σ_S" 를 순방향으로 내는 것은 가능한 설계다. 단 기대(`[해석]`): BV 만이면 비선형은 `A·j₀` 하나 → A1(접촉 ↔ LAM_PE)을 못 가른다 · 가른다면 `C_dl ∝ A`(R·C 1단계) 또는 면적 스케일이 다른 확산 비선형 쪽 — **truth 에서 시험할 물음**이고 이 편이 답한 것은 아니다. 코드로 옮기면 RUN_SCOPE 밖 설계 메모일 때만(별도 승인) |
| **다중정현 진폭 의존 = 비선형 진단 채널인가** | §2 A1 · 진단 관측 | ⚠ **검출 채널로는 예, 귀속 채널로는 아니오** — ① 이 편은 진폭 **하나**라 진폭 의존을 재지 않았다 ② 고정 전류 진폭 비선형도는 활성 면적당 분극의 함수(LAM_PE · 접촉 · 계면층 · 수송 같은 방향) ③ 진단으로 쓰려면 진폭 스윕(전압 기준 정규화)이 최소 조건 — 49호(액체 · 1 → 15C 펄스 저항 −18 … −27 % · 다중사인 ↔ EIS 저주파 −24 %)가 진폭 의존의 액체셀 표본 |
| 블록 지향 경험 모형(H · W · H-W) | §2–§3 기계론 forward(91호 계보) ↔ 경험 모형 | ❌ 값 0 · 구조적 교환 · 물리 배정은 모양 비유 — 기계론 truth 의 대체가 아니다. 넘길 것은 **"블록 지향 모형의 블록별 물리 배정은 정규화 · 구조 의존" 경고** |
| 측정 중 상태 이동(SoC −1.12 % · 셀 2 2.26 V) | §2-1 M 메타데이터 · 시험 규약 | ✅ 경고 — 고임피던스 셀의 다중정현은 "고정 상태" 가 아니다(상태 이동을 측정 메타데이터로) |
| 두 셀 대조(재료 교체 · n 1) | §3 2단계(실셀 · 압력 통제) | ❌ 압력 · 셀 수 · 조성 0 |

⇒ **넘어가는 것은 "경고 둘" 과 "관측 후보 하나" 다** — (i) 비선형도 = 검출이지 귀속이 아님 (ii) 블록별 물리 배정은 정규화 · 구조 의존 (iii) 진폭 스윕 다중정현을 합성 truth 의 순방향 관측 후보로(시험 전). 91호(기계론 원형 · 값의 문제)와 짝을 이루면, **경험 모형 쪽은 값이 아예 없고 구조가 문제**다.

---

# ★ (f) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 이 편 | 칸 |
|---|---|---|
| **Q1 정량** | **없다** — `contact` 0 회 · 열화 0 · `θ(N)` 0/92. 층 하나: 고정 전류 진폭의 비선형 왜곡 = 활성 계면 면적당 분극의 가파른 단조 함수(`[재현·가정]` BV 3차 상대 왜곡 ∝ (R_ct·I)²) — 접촉 손실 · LAM_PE · 계면층 · 양극층 전도도 저하가 같은 방향 → 검출 대리량 후보 · 귀속 0 | `θ(N)` 0/92 |
| **Q2 독립관측** | **없다** — 관측 채널 하나(단자 전압 비선형) · 재료 교체(σ · 접촉 · 형태 · 계면 화학 교락) · 2전극 · 대역 4 mHz–1 Hz(계면 호 아래) · `C` 0 · 사후 분석 0 | 없다 |
| **Q3 라벨층위** | 칸 없음 · **층 하나: "원인 이름표 = 25 ℃ 공칭 재료 전도도(측정 · 출처 0 · 시험 60 ℃ — `[재현]` 분리막 50 Ω cm² ↔ 셀 1 전체 ≈20 Ω) · 블록 함수 = 그림뿐(계수 · 꺾인점 · 불확실도 0) · 'accuracy %' 정의 0 · 셀 하나씩"** | 층 |
| **Q4 유일성** | **0/92 — 여든네 번째 성질**(§(b) 7) · 식별성 어휘 전수 0 · BLA 분산 = 잡음 · 왜곡 · 블록 이득 · 오프셋 교환 미정규화(`[재현]`) · 구조 의존 모양(D8) | 0 |
| **Q5 Li-In** | **해당 없음** — LCO ‖ 흑연 완전지 2전극(In 0 · 기준극 0) · 층 하나: 방전 비선형을 양극에 배정한 근거 = "anode … 10⁻³ S/cm"(음극층 SE 미기재 — D7) · 흑연 쪽 몫 미검사 | 해당 없음 |
| **Q6 압력** | **보고 0** — 코인셀 · 성형 · 운전 압력 · 스프링 · 하중 인쇄 0(`pressure` · `MPa` · `spring` · `torque` 0 회 · 셀 TME 제작) — (배) 표본 | 칸 이동 없음 |
| **Q7 dead Li** | **해당 없음**(흑연 · 무음극 아님 · 열화 0) · 층 하나: 5C 첨두 충전 펄스(≈2.74 mA cm⁻² `[도표·화소]`)의 흑연 Li 도금 검사 0 | 해당 없음 |
| **Q8 화학 · OCP** | **층 하나** — LiNbO₃ 코팅 LCO ‖ 흑연 · **OCV 곡선 · 값 인쇄 0**(모형에 상수로 "더함") · 50 % SoC 설정법 0 · `[도표·화소]` 두 셀 선형 모형 중심 ≈3.80 ↔ ≈3.58–3.61 V(같은 "50 % SoC" 인데 ≈0.2 V 차 — 정류 직류 이동 · SoC 기준 · OCV 상수 미분리) · SoC 변화 −1.12 % / p-p 1.55 % ↔ 설계 ≤1 % | 층 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 어휘 집계 — 텍스트 층 · 줄 끝 하이픈 복원 · 쪽 머리 · 바닥글(147 줄) 제외 · 본문(제목 → 사사 · 캡션 포함) | 참고문헌, NFKC 뒤 (앞과 다른 것만 괄호)

| 낱말 | 본문 | 참고문헌 |
|---|---|---|
| `identifiab*` · `confiden*` · `sensitiv*` · `Fisher` · `Cram(é)r` · `D-optim*` · `persisten*` · `crest` · `normali*` · `gain` · `scal*` · `±` · `standard deviation` · `residu*` · `threshold*` · `n =` | **0** | 0 |
| `uniqu*` | 1("a unique model" — 하나의 모형) | 0 |
| `uncertain*` | 1(SINAD 문장 "huge errors and uncertainty") | 0 |
| `variance` | **6**(식 9–11 — 잡음 · 총 · 비선형 왜곡) | 0 |
| `identif*` | 43(전부 "identification · identified · identify") | 11 |
| `accura*` · `validat*` · `error*` · `RMS` | 20 · 4 · 7 · 1 | 0 · 1 · 0 · 0 |
| `optimal*` · `information` | 0 · 2(일반 뜻) | 1([56] 제목) · 0 |
| `fault*` · `detect*` · `safety` | 3 · 7 · 3 | 0 · 3 · 0 |
| `pressure*` · `MPa` · `spring` · `torque` · `stack` | **0** | 0 · 0 · 1("Springer") · 0 · 0 |
| `load*` | 1("input current load realizations") | 1 |
| `temperature*` · `°C`(ºC 포함) · `60 °C` | 1(식 33 기호 설명) · 5(2) · 2 | 1 · 0 · 0 |
| `SoC`/`SOC` · `OCV` · `open circuit` | 10 · 2 · 1 | 2 · 0 · 0 |
| `contact*` · `interphase*` · `LAM` · `LLI` · `degrad*` · `DRT` · `Kramers` | **0** | 0 |
| `interface*` · `boundary` | 10 · 2 | 0 · 0 |
| `capacit*` | 2(전부 "capacity") | 4 |
| `impedanc*` · `EIS` · `Nyquist` | 15 · 2 · 5 | 3 · 0 · 0 |
| `nonlinear*`(non-linear 포함) · `BLA` · `multisine*` · `realiz*` · `period*` | 123 · 25 · 30 · 22 · 16 | 26 · 0 · 4 · 0 · 0 |
| `Hammerstein` · `Wiener` | 57 · 55 | 5 · 6 |
| `diffusion` · `charge(-)transfer` · `mass-transfer` · `Butler` · `Nernst` · `polariz*` · `saturat*` · `logarithm*` | 6 · 6 · 1 · 1 · 3 · 1 · 3 · 4 | 0 · 1 · 0 · 0 · 0 · 0 · 0 · 0 |
| `ionic conductivit*` · `conductiv*` | 20 · 22 | 0 · 0 |
| `FIR` · `finite impulse` · `piecewise` · `breaking point*` · `polynomial*` · `least square*` · `maximum likelihood` · `PSO` | 1 · 1 · 5 · 6 · 13 · 3 · 1 · 1 | 0 · 0 · 0 · 0 · 1 · 0 · 0 · 0 |
| `noise` · `SNR` · `SINAD` · `distortion*` · `FRF` | 21 · 1 · 2 · 37 · 7 | 1 · 0 · 0 · 8 · 2 |
| `repeat*`/`replica*`/`reproduc*` | 3(전부 주기 · 실현 반복) | 0 |
| `supplement*` · `appendix` · `data availability` · `supporting information` · `video` · `movie` · `zenodo` · `github` · `MATLAB` · `software` | **0** | 0 |

⚠ 텍스트 층 한계: ① "σ25ºC" 의 "º"(U+00BA)는 NFKC 뒤 "o" 라 `°C` 5 → 2 ② 지수 음수 부호 소실("10 4 S/cm") ③ **그림 13 캡션 첫 줄이 텍스트 층에서 참고문헌 [5] 줄 사이에 끼어 있다**(p. 11 배치) — 참고문헌 열의 `Hammerstein` · `Wiener` · `charg*` 일부가 그 캡션이다 ④ 참고문헌 [40]–[45] 쪽 범위의 "e"(예: "727e38")는 엔 대시 자리의 조판 흔적.

---

# 재현 (`[재현]` — 지면 · 그림 화소 숫자로 우리가 계산 · 가정 · 외부 값 표시)

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| R1 | C-rate 삼각 | 2.8 mA ÷ 0.55 mAh = 5.09C · 1C = 0.55 mA cm⁻² · 첨두 2.8 mA cm⁻² | ✅("5C") · 비용량 · 적재 0 이라 셋째 변 미폐합 |
| R2 | dB ↔ 배수(진폭 관례) | 70 dB ×3162 · 50 dB ×316 · 15 dB ×5.6 | ✅("≈3200 · 320 · around 5") |
| R3 | 주기 · 격자 | T 250 s(그림 2a) → f₀ 4 mHz ✅ · Np 2500 · 나이퀴스트 5 Hz ✅ · `[도표·화소]` 33 선 = k 1 · 3 · 11 + 8j(j 0–30) · 최고 1.004 Hz | ✅ 33 · 홀수 · 선형 격자(저주파 2 선) |
| R4 | 시험 길이 | 4 × 6 × 250 s = 6000 s · 60,000 표본 + 검증 | 계산값 |
| R5 | 선 진폭 · RMS · 파고율 | `[재현·가정]` −72 dB → 0.25 mA · RMS 1.02 mA · CF 2.7 ↔ `[도표·화소]` 첨두 2.74 · RMS 0.72–1.09 mA | ✅ 정규화 가정(D4) |
| R6 | SoC 궤적 | `[도표·화소]` 49.98 → 48.86 → 50.40 → 50.01 % · `[재현·가정]` 최저 선 하나 p-p 1.01 % | ❌ 설계 "≤1 %"(D3) |
| R7 | 통과 전하 | `[재현·가정]` 주기당 0.056 mAh(10 %) · 24 주기 1.36 mAh(공칭 ×2.5) | 가우스 근사 |
| R8 | 두 셀 BLA 비 | `[도표·화소]` 21.6–21.8 dB(×12.0–12.4 · ≤0.044 Hz) → 20.5 dB(×10.5 · 1 Hz) | ✅ "12 times"(저주파) · 주어 셀 1 ✗(D2) |
| R9 | 두 셀 NL 비 | 31–35 dB(최저 두 선) · 39.7(0.044) · 41–54(0.07–0.5) · 54–72 dB(0.55–0.78) | ⚠ ">100 times" 는 ≈0.07 Hz 위(D12) |
| R10 | 상대 왜곡(NL ÷ BLA) | 셀 1 −34 / −43 / −55 dB · 셀 2 −22.5 / −25.3 / −22.5 … −24.4 dB | 셀 2 ≈3–8 % |
| R11 | Bode ↔ Nyquist 폐합 | 셀 1 (32.4, 23.5) → 32.0 dB · 셀 2 (405.6, 209.8) → 53.2 · (290.5, 65.6) → 49.5 · (209.5, 11.8) → 46.4 dB | ✅ ±0.3 dB |
| R12 | 스펙트럼 dB 차 → \|Z\| | −72 dB 전류 기준 셀 1 ≈30 · 26 dB · 셀 2 ≈53 · 46.5 dB | ✅ ±2 dB(같은 정규화) |
| R13 | SINAD(최악) | 셀 1 ≈38(≤0.05 Hz) · 45 · 53 dB · 셀 2 ≈11 dB | "≈50" 은 0.05 Hz 위 · "<15" ✅ |
| R14 | 대역 밖 왜곡 | 셀 2 − 셀 1 바닥 = +54 · +39 · +33 · +29 dB(1–5 Hz) | 모형 없는 비선형 지문 · 본문 정량 0 |
| R15 | 분리막 옴 | 500 µm ÷ 10⁻³ S/cm = 50 Ω cm² ↔ 셀 1 전체 Re(1 Hz) ≈20–21 Ω | ❌ 25 ℃ 값 그대로면 불가 → 60 ℃ σ ≥2.4 배 |
| R16 | 양극층 벌크 자릿수 | `[재현·가정]` 조밀 평판 Δ 225 Ω ↔ 1 Hz 실부 차 ≈189 Ω | 자릿수만 · 검사 아님 |
| R17 | 정확도 산술 | 범례 68.5 · 74.5 · 81 · 86.5 → 6.0 · 6.5 · 18.0 ✅ · H + W 향상 18.5 ≈ H-W 18.0 | ✅ · "18 %" = %p(상대 +26 %) |
| R18 | "6 % less RMS error" | `[재현·가정]` NRMSE 적합도면 ‖e‖/‖y − ȳ‖ 0.315 → 0.255(상대 −19 %) | 정의 미인쇄(G6) |
| R19 | **식 9–11 기대값** | E[식 11] = M·P(M−1)/(MP−1)·σ_S² = 3.13 σ_S²(M 4 · P 6) · Monte Carlo 3.129 · 표준식 0.9996 | ⚠ 인쇄 식대로면 σ_S 진폭 **+5.0 dB**(D13) |
| R20 | **블록 이득 · 오프셋 교환** | (k·f_h, f_w(·/k)) · (f_h + c, f_w(· − G(1)c)) 출력 차 0 · 3×10⁻¹³ | ✅ 구조적 비식별 · 정규화 미인쇄 |
| R21 | 블록 모양 | `[도표·화소]` f_h(H-W) 방전 기울기 1.44 → 0.84 → 0.40 · f_h(H 단독) 방전 확장 ≈1.5 · f_w 0.81 → 5.3 · 셀 1 f_h 0.93 · 파선 1.12 · 0.92 | ❌ 구조 의존(D8) · Y = X 아님(D9) |
| R22 | 함수 범위 | `[도표·화소]` 그림 12a · 13 x ±3.29 mA ↔ 자료 첨두 ±2.74 mA | ❌ 외삽 서술 0(D11) |
| R23 | 60 ℃ 열전압 | RT/F = 28.71 mV · 셀 2 아래 ≈1.3 V(×45) | 대신호 |
| R24 | BV 비선형 척도 | `[재현·가정]` 3차 상대 왜곡 ≈(F/RT)²(R_ct I)²/24 · R_ct ×12 → ×144(+43 dB) · η = (2RT/F) asinh(I/(2A j₀)) 은 A·j₀ 하나 | 항등 · 관측 R10 · R9 자릿수 안 |
| R25 | 선형 모형 중심 | `[도표·화소]` 셀 1 ≈3.80 V · 셀 2 ≈3.58–3.61 V | 같은 "50 % SoC" 에 ≈0.2 V 차(G7) |

---

# 참고문헌 60 — 우리 축에 닿는 것 (번호는 PDF p. 11–12 목록에서 직접 확인 · References [1]–[23] · [25]–[60] + Further reading [24])

| [#] | 서지 `[인쇄]` | 이 편의 쓰임 | 우리 축 |
|---|---|---|---|
| [46] | Y. Firouz, R. Relan, J.M. Timmermans, N. Omar, P. Van den Bossche, J. Van Mierlo, "Advanced lithium ion battery modeling and nonlinear analysis based on robust method in frequency domain: Nonlinear characterization and non-parametric modeling", *Energy* **106** (2016) 602–617 | 식 1 · 식 2 · 식 3–8 의 직접 인용처 · "performed BLA analysis on NMC pouch cells … only developed a nonparametric model" | Q4 도구(**액체셀**) · 식 9–11 의 원형 대조(R19) · 진폭 · SoC 의존 |
| [58] | R. Relan, Y. Firouz, J.-M. Timmermans, J. Schoukens, "Data-driven nonlinear identification of Li-ion battery based on a frequency domain nonparametric analysis", *IEEE Trans. Control Syst. Technol.* **25** (5) (2017) 1825-183[sic] | "PNLSS … mainly focuses on low SoC (<10%) as nonlinearity is strong on that range" | (c) 교란(SoC) · Q4 도구(액체셀) |
| [52] | W.D. Widanage, A. Barai, G.H. Chouchelamane, K. Uddin, A. McGordon, J. Marco, P. Jennings, "Design and use of multisine signals for Li-ion battery equivalent circuit modelling. Part 2: Model estimation", *J. Power Sources* **324** (Aug. 2016) 61–69 | "multisine … Wiener system … the detected nonlinearity is very weak" | 입력 설계 · Wiener(액체셀) — **49호 후속 표 · 원장 ★ 행** |
| [53] | W. Allafi, K. Uddin, C. Zhang, R.M.R.A. Sha, J. Marco, "On-line scheme for parameter estimation of nonlinear lithium ion battery equivalent circuit models using the simplified refined instrumental variable method for a modified Wiener continuous-time model", *Appl. Energy* **204** (2017) 497–508 | 온라인 Wiener 추정 · "weak as well" | Q4 도구(액체셀) |
| [48] | M. Schoukens, K. Tiels, "Identification of block-oriented nonlinear systems starting from linear approximations: a survey", *Automatica* **85** (2017) 272–292 | 블록 지향 일반론 · "structured models are quite appropriate for physics-based models" | **Q4 — 블록 사이 정규화 · 구조 판정(R20 · D8)의 방법 원전** |
| [50] · [56] | M. Schoukens, Er-W Bai, Y. Rolain, "Identification of hammerstein-wiener systems", *IFAC Proceed. Volumes* **45** (16) (2012) 274–279 · Er-W Bai, "An optimal two-stage identification algorithm for Hammerstein–Wiener nonlinear systems", *Automatica* **34** (3) (1998) 333–338 | 식 20 · H-W 정식화 | Q4 — H-W 식별 조건 · 정규화 |
| [40] | J. Schoukens, J. Sweversb[sic], R. Pintelon, H. Van der Auweraer, "Excitation design for FRF measurements in the presence of non-linear distortions", *Mech. Syst. Signal Process.* **18** (2004) 727–38 | BLA 계보 [40–45] | **(d) — 이 다중정현의 설계 목적(FRF 분산 ↔ 정보량)의 원전** |
| [41] · [42] | K. Vanhoenacker, T. Dobrowiecki, J. Schoukens, *IEEE Trans. Instrum. Meas.* **50** (2001) 1097–102 · K. Vanhoenacker, J. Schoukens, 같은 저널 **52** (3) (2003) 748–53 | 같음 | 검출선(홀 · 짝) 설계 — 이 편 미사용(G8) |
| [43] · [45] · [44] | J. Schoukens, R. Pintelon, T. Dobrowiecki[b sic], Y. Rolain, *Automatica* **41** (2005) 491–504 · R. Pintelon, J. Schoukens, *MSSP* **16** (5) (2002) 785–801 · B. Peeters 외 2003 Benelux meeting p. 49–52 | 같음 | BLA 분산 추정식의 원전(R19) |
| [51] · [47] · [49] · [54] · [55] | Zhang · Schoukens 2017 *IEEE TIM* 66(3) 569(W-H 구조 검출) · Cheng 외 2017 *MSSP* 87, 340(Volterra 개관) · Decuyper 외 2018 *MSSP* 98, 209 · Esfahani 외 2017 *IFAC-PapersOnLine* 50(1) 458 · F. Guo 2004 학위논문 | 비선형 표현 · 구조 검출 | 일반 도구 |
| [5] | Y. Kato, S. Hori, T. Saito, K. Suzuki, M. Hirayama, A. Mitsui, M. Yonemura, H. Iba, R. Kanno, "High-power all-solid-state batteries using sulfide superionic conductors", *Nat. Energy* **1** (2016) 16030 | SSB 이점[4,5] · **"the LiCoO2 particles on the surface of the cathode consume more lithium as concentration is increased [5]"**(셀 2 임피던스 증가의 기구 근거) | (c) · Q2 — **64호 후속 ★ · 원장 행 0(지목 누락)** |
| [6] | A. Sakuda, A. Hayashi, T. Ohtomo, S. Hama, M. Tatsumisago, "All-solid-state lithium secondary batteries using LiCoO2 particles with pulsed laser deposition coatings of Li2S–P2S5 solid electrolytes", *J. Power Sources* **196** (16) (2011) 6735–6741 | BMS SoC/SoH 추정[6,7]의 근거로 인용(재료 편 — D16) | ASSB 코팅(이 편과 다른 쓰임) |
| [59] · [60] | B.C. Han, A.V.D. Ven, D. Morgan, G. Ceder, *Electrochim. Acta* **49** (2004) 4691–4699 · M.Z. Bazant, *Accounts Chem. Res.* **46** (5) (2013) 1144–1160 | 식 33("Nernst diffusion layer") · 식 34–35(BV · j₀(c_s)) | 물리 해석의 식 출처 |
| [19] · [20] | Mu 외 2017 *Appl. Energy*(분수차 모형 · "SoC variations for avoiding nonlinear distortions [19]") · Andre 외 2011 *JPS* 196(12) 5334(EIS I) | EIS 소진폭 · 비선형 회피 | 진폭 관례 |
| [14] · [15] · [16] · [17] · [57] | 같은 연구실 ECM · 노화 · 매개변수 도구(2014–2016) | ECM · 식별 방법("quite well known [14,57]") | — |
| [21]–[23] · [35]–[39] | ANN · GA · LPV 모형 | "claimed … nonlinear … while those are LPV" | — |
| [24] | G. Dong 외 2015 *Energy* 90, 879(Further reading) | **본문 인용 0** | — |

---

# 인용 대조 — 이 편을 인용한 우리 digest 와 그 쓰임

| 호 | 자리 | 그 digest 가 이 편에 매단 것 | 원문 대조 |
|---|---|---|---|
| **26호** Iwakiri 2024 | [17] · Table 1 "Parameter Estimation **Yes**"(This work · [15] Danilov 2011 · [18] Kroeze 2008 · [17] 넷 — "경험식, block-oriented system identification") · 후속 ★★★(:384) "**제목에 'system identification' 이 들어간 유일한 인용** — 경험 모델이지만 ASSB 식별 문헌(공백 1번 후보)" · :391 "식별성 · 역문제를 제목에 단 것은 Firouz 2020 하나" | 추정을 한 경험 모형 · ASSB 식별 문헌 후보 | ✅ "Parameter Estimation Yes"(블록 함수 · 전달함수를 맞췄다 — 단 **값 · 불확실도 0**) · ❌ **"ASSB 식별 문헌"** — 식별성(유일성 · 불확실도 · 구조적 비식별)은 0 · 공백 1번 후보에서 내려감 · ⚠ 26호 표기 "Soult" = PDF "M. Cazorla Soult" |
| 27호 Sinzig 2024 | "이 편이 인용하지 않는 것" 목록(:394) | — | — |

**지목 수 확인**: 지목은 **각 digest 의 후속 절**만 센다 — 26호 후속 표(:384 ★★★) 하나 · 27호는 "인용하지 않는 것" 목록(지목 아님) · `log.md` · 카드의 26호 항은 digest 후속 절이 아니다 ⇒ **26 = 1 — 원장 행 "26 | 1" 과 일치(정정 없음).**

**교차 참조 (이 편과 같은 축 · 이 편이 인용하지 않음)**: 49호 Barai 2018(액체 · 진폭 · 시간 창 · 다중사인 ↔ EIS 저주파 −24 %) · **10호 Vadhva 2021** `[인쇄]` "**no NLEIS measurements have been reported on ASBs**" — 이 편(2020-02 온라인 · 10호보다 앞)은 다중정현 BLA 로 ASSB 코인셀의 비선형 왜곡을 정량하고 대역 밖 왜곡까지 그렸다(그림 6c) → 10호 문장은 "NLEIS(정현 하나의 고조파 분석)" 로 좁게 읽어야 성립한다(`[해석]`) · 10호 후속 ★ [184] Harting · Wolff · Krewer 2018 *Electrochim. Acta* 281, 378(NLEIS Li 도금 검출 — 액체 · **원장 행 0**) · 34호 Liang 2026(OED 처방 — §(d)) · 32호 Biçer 2025 `[인쇄]` "some solid electrolytes exhibit nonlinear impedance behavior, especially at interfaces" — 이 편이 그 1차 표본 중 하나지만 32호 지면에서 인용 대조는 하지 않았다.

---

# 곱 축퇴 처방 — 일흔다섯 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

**실험 데이터가 있다**(셀 둘 · 다중정현 · 신품) ⇒ 처방을 적용한다. 단 **열화 0 · 재료 교체 대조 · 2전극**이다.

| 처방 단계 | 필요한 입력 | 92호 | 판정 |
|---|---|---|---|
| **1단계** (16 · 23호) | 같은 상태축 위 `R` · `C` | 대역 4 mHz–1 Hz — 고주파 끝이 이미 Re ≈20 · ≈210 Ω(`[도표·화소]`) · **계면 호(대개 >1 Hz) 대역 밖** · `C` 0 · 위상 자체 그림 0(오차만) | ❌ 대역이 1단계 아래 |
| **2단계** (18호) | + 면적을 아는 대조군 | 재료 교체(σ · 접촉 · 형태 · 계면 화학 교락) · 셀 하나씩 | ❌ |
| **3단계-a** (19호) | `Ea` | 60 ℃ 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | `C` 0 | ❌ |
| **4단계** (20호) | 시간 영역 상한 | 시간 영역 검증(그림 9)은 있으나 이완 · 휴지 0 | ❌ |
| 처방 표 "율 스윕(최소 2 율, `i → 0` 포함)" | 여러 율 | **진폭 한 수준**(첨두 2.74 mA) · 율 · 진폭 스윕 0 | ❌ — 바로 이 축이 "비선형 진단" 의 최소 조건인데 비었다 |
| 처방 표 "`J^T J` 최소 고유벡터" | 적합점 야코비안 | 저자 0 · 값 0 이라 우리도 못 낸다 · 대신 **블록 이득 · 오프셋 교환 = 정확한 null 방향**(`[재현]` R20) | ⚠ 구조로만 |

**곱 문장**(`[인쇄]` → `[해석]`): 식 35 "j₀ = F·k_c·c_e^{α_o}(c_s,max − c_s(0,t))^{α_o}(c_s(0,t))^{α_r}" 와 식 34 BV — 셀 전류로 옮기면 I = A·j₀·f(η) 라 **면적 A 와 k_c(j₀)가 한 곱으로만** 들어간다(이 편은 A 를 쓰지 않는다 — 모형이 경험적이라 곱 자체가 블록 이득에 흡수). `[재현]` 비선형 영역까지 가도 순수 BV 의 η 는 `I/(A·j₀)` 하나의 함수(asinh)라 **다중정현 진폭 · 비선형 왜곡이 곱을 풀지 못한다** — 곱을 푸는 것은 처방 표의 기존 줄(`C_dl ∝ A` · 면적 스케일이 다른 확산 항)뿐이다. ⇒ 처방 표에 새 줄은 없고 **경고 하나**: "비선형 진폭 채널(BLA 왜곡 · SINAD · 블록 함수)은 BV 안에서 `A·j₀` 곱을 가르지 못한다 — 진폭 스윕을 1단계 대신으로 쓰지 않는다."

---

# 보류 결정 (가)–(히) · (개)–(해) · (게)–(체) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 92호 근거 | 세기 |
|---|---|---|---|
| **(다)** | 28호 Bizeray(액체셀 도구)를 ASSB Q4 분모에 | **이 편이 (다) 의 "닿는 논문" 목록에 직접 있다**(Forman 2012 · Khalik 2021 · Lu 2022 · **Firouz 2020**) — 결과: ASSB 쪽 "system identification" 편에 식별성 도구 0(FIM · 신뢰구간 · 유일성 0 · BLA 분산 = 잡음 · 왜곡) · 블록 이득 · 오프셋 교환(구조적 비식별 — `[재현]`)도 언급 0 → ASSB 분모에 "식별 어휘를 단 편도 0" 한 점 · 식별성 도구는 여전히 액체셀(28호)뿐 | **중** |
| **(주)** | "X-limited" 명제의 판정 기준 표기 | "the Hammerstein function indicates the current saturation because of the **charge-transfer limit** and the Wiener function explains the severe voltage drops due to the **mass-transfer limit**" — ① 순위 · 문턱 0 ② 시간 기준 0 ③ 조건 60 ℃ · 50 % SoC · 진폭 하나 ④ 저항 정의 0 ⑤ 동역학 손잡이 = 식 35 의 c_s → c_s,max(값 0) — 그리고 배정 근거인 블록 모양이 정규화 · 구조 의존(R20 · D8) | **중** |
| **(치)** | 모형 결론 옆 "배제 가정" 표기 | "nonlinear distortions caused by ionic conductivity variation of the solid electrolyte at the cathode layer"(초록) — 결론을 구성상 정한 가정: "the only difference is the ionic conductivity"(재료 교체의 다른 변화 배제) · 정적 블록(이력 0 — 그림 9b 낙하는 저주파 위상 구간에 몰림) · 잡음 무시 · 음극층 σ 10⁻³(근거 0) — 결론 옆에 붙지 않음 | **중** |
| **(히)** | 구성 교체형 전극 몫 배정의 표기 | 양극층 SE 교체 + 2전극으로 비선형을 양극에 배정 · 이식 가정(같은 접촉 · 같은 압력 · 같은 음극 상태) 0 · 자기 기준(`C` 일치) 0 · n 1 · 1 | **중** |
| (세) | 인쇄 매개변수 표의 재풀이 폐합 검사 | **식별 편이 식별값을 하나도 인쇄하지 않는다**(전달함수 · 다항 · 꺾인점) — 재풀이 검사 자체가 불가 · 남은 것은 그림 화소 판독(R21) | 약 |
| (제) | 모형 "일치" 의 잔차 표기 | "accuracy 68.5 → 86.5 %" 정의 0 · 시간 영역 시각 비교 · 최대 오차 −0.8 V(선형)는 방전 낙하 구간에만 | 약 |
| (이) | 모형 값 인용 규칙 | σ 셋 = 25 ℃ 공칭 이름표(측정 · 출처 0) · 시험 60 ℃ · `[재현]` 분리막 50 Ω cm² ↔ 셀 1 전체 ≈20 Ω | 약 |
| (가) | 29호 Q4 +0.5(정적 ↔ 동적) | 정적 몫(OCV)을 상수로 더하고 동적 몫만 식별하는 **설계형 분리**(영평균 · SoC ≤1 %) — 그러나 SoC 이탈 −1.12 % · 두 셀 모형 중심 0.2 V 차(G7) | 약 |
| (차) | PyBaMM 면적 / j₀ 노브 분리 forward | `[재현]` BV 의 η 는 `I/(A·j₀)` 하나 — 비선형 진폭 채널로는 두 노브가 안 갈린다 → forward 에 진폭 스윕을 넣어도 `C_dl ∝ A` 없이는 같은 곱 | 약 |
| (무) | j₀(x) 모양 선택지 | 식 35 (c_s,max − c_s)^{α_o} c_s^{α_r} 의 포화 쪽 소멸을 Hammerstein 포화의 설명으로 인쇄(값 · 시험 0) | 약 |
| (배) · (미) | 코인셀 하중 칸 · 저압 표기 | 값 미인쇄 코인셀 ASSB 하나 더 — **성형 압력까지 0**(셀 TME 제작) | 약 |
| (대) | C-rate 기준 용량 표기 | 기준 = 공칭 0.55 mAh 로 닫힌 쪽(5.09C ✅ · 2.8 mA cm⁻²) · 비용량 · 적재 0 | 약 |
| (메) | 원자료 교차 폐합 · 중복 검사 | 원자료 없음 → **그림 사이 폐합**으로 대신: 그림 6 ↔ 7 ↔ 8 dB 척도 ✅(±2 dB) · 8a ↔ 8c ✅(±0.3 dB) · 9b ≡ 10b ≡ 11b ≡ 12c 측정선(같은 검증 실현) · 12a ≡ 13b · 12b ≡ 13d(12b 눈금 오류 D10) · 2b ↔ 6a 같은 수준 다른 단위(D4) | 약 |
| (베) | 시간분해 EIS 의 측정 상태 표기 | 측정 상태는 인쇄(50 % SoC · 60 ℃ · 영평균)되지만 **측정 중 상태가 움직인다**(SoC −1.12 % · 셀 2 2.26 V) — 상태 고정이 설계 목표인 측정의 이탈 표본 | 약 |

나머지 — (라)(마)(바)(사)는 결정 · 반영됨, 그 밖의 글자는 **근거 0**(Li-In · 기준극 · 노화 · DRT · LLI 정의 · 압력 시계열 · 프로토콜 비교 축이 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (셋 — 글자는 호출자가 붙인다)

1. **비선형도 지표의 측정 조건 표기** — "비선형 왜곡 · SINAD · 블록 함수 이탈" 을 열화 · 고장 지표로 카드 · 개념 · 합성 truth 에 옮길 때, 가진 진폭(전류 첨두 · RMS)과 그 결과 **전압 진폭(또는 |Z|)** · 온도 · SoC · **진폭 스윕 유무(전압 기준 정규화)** · 셀 수를 값 옆에 적고, 임피던스가 다른 셀을 **같은 전류 진폭**으로 비교한 결과는 "임피던스 크기 교락" 으로 표시할지 — 92호: 진폭 하나(첨두 2.74 mA ≈5C · RMS ≈1.0 mA) · |Z| 비 ×10.5–12.4 · 셀 2 전압 2.26 … ≈4.2 V ↔ 셀 1 ±0.05 V · 상대 왜곡 −22 … −30 ↔ −34 … −55 dB · `[재현·가정]` BV 상대 왜곡 ∝ (R_ct I)².
2. **블록 지향 · "system identification" 편의 식별 산출물 표기** — 식별 편의 결과를 옮길 때 ① 식별된 값 · 불확실도 ② 블록 사이 정규화(이득 · 오프셋) ③ 차수 · 꺾인점 선택 근거 ④ 학습 ↔ 검증 신호 분할 ⑤ 적합도 백분율의 정의식을 확인해 적고, 블록 하나의 모양에 물리 기구를 배정한 명제는 **구조를 바꿔도 그 모양이 유지되는지**(H 단독 ↔ H-W) 함께 적게 할지 — 92호: ①–⑤ 전부 0 · 입력 블록 확장 ↔ 포화 · BLA "분산" = 잡음 · 왜곡(인쇄 식대로면 +5 dB).
3. **"입력 설계" 의 목적 표기 (34호 처방 판)** — 설계 가진(다중정현 · PRBS · 펄스 열)을 쓴 편을 Q4 로 옮길 때 설계 목적(잡음 ↔ 비선형 분리 · FRF 분산 · **매개변수 정보량(FIM · D-optimality)**)과 설계 변수(대역 · 격자 선형 / 로그 · 진폭 수준 수 · 실현 · 주기)를 적고, 분리 설계를 식별성 근거로 세지 않게 할지 — 92호: 분리 설계(Schoukens 계보) · 선형 격자(0.04 Hz 아래 2 / 33) · 진폭 하나 · 정보 기준 0 ↔ 34호 처방(정보량 설계 · 실측 0).

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | "a **3rd order discrete FIR** (of finite impulse response) transfer function" ↔ 식 12 · 그림 3 의 분모 1 + a₁z⁻¹ + ⋯ (IIR) · `[해석]` FIR 은 저주파로 갈수록 커지는 \|Z\| 를 못 그린다 | p. 7 ↔ p. 4 |
| **D2** | "the amplitude of linearized impedance of **cell 1** increased around 12 times" ↔ 그림 7 큰 쪽은 셀 2 · 비 ×10.5–12.4 | p. 7 · 그림 7 |
| **D3** | "the SoC variation should not be more than 1%" ↔ 그림 2c −1.12 % · p-p 1.55 % · `[재현·가정]` 최저 선 하나로 p-p ≈1.0 % | p. 3 · 그림 2c |
| D4 | 본문 "−70 dB amplitude" · "−160 dB" ↔ 그림 2b "Power Spectral Density (dB/Hz)" ↔ 그림 6a "Current Amplitude (dB)"(같은 수준) | p. 3 · 그림 2b · 6a |
| **D5** | 한 조작(양극층 SE 교체)의 이름이 "ionic conductivity inside the cathode layer"(p. 2) · "boundary resistance between solid electrolyte and active material"(p. 7) · "different materials in the interface of cathode active material and solid electrolyte"(p. 10) · "at the cathode interface"(초록) — 벌크 ↔ 계면 | p. 1 · 2 · 7 · 10 |
| **D6** | "the only difference is the ionic conductivity" ↔ 다른 재료(유리 ↔ 결정 γ 상)의 다른 성질 교락(`[해석]`) · 전도도는 25 ℃ 이름표 · 시험 60 ℃ · `[재현]` R15 | p. 2 |
| D7 | "Due to high ionic conductivity (10⁻³ S/cm) in the **anode** and separator layer" ↔ §2.1 · 그림 1 에 음극층 SE 없음 | p. 10 ↔ p. 2 · 그림 1 |
| **D8** | "The Hammerstein curve in Fig. 12a is different from the one seen in Fig. 10a, which will be investigated more in the following sections" ↔ §4.3 미검토 · 두 그림 방전 쪽 곡률 반대(확장 ↔ 포화) · 물리 배정은 13b 하나 | p. 9–10 · 그림 10a · 12a · 13b |
| D9 | 셀 1 "(Y = X)" · "deviation from the linear line (dashed red line)" ↔ 셀 1 f_h 기울기 0.93 · 13c y 척도 없음 · 13b · 13d 파선 1.12 · 0.92 | p. 10 · 그림 13 |
| D10 | 그림 12b x 눈금 이름 "−0.43 · 0 · 0.43 · −0.43 · 0" | 그림 12b |
| D11 | 최대 전류 "2.8 mA (5C)" ↔ 그림 12a · 13 함수 ±3.3 mA | p. 3 · 7 ↔ 그림 12 · 13 |
| **D12** | "more than 100 times" ↔ 최저 두 선 ≈31–35 dB(×35–56) · 0.044 Hz ×97 | p. 7 · 그림 7 |
| **D13** | 식 9–10(한 주기 FRF 분산) + 식 11 ×M ↔ 표준 강건 추정식 — `[재현]` 인쇄 식대로면 σ_S² ×3.13(+5.0 dB) · 식 11 의 \|·\| | p. 4 |
| D14 | "Hammerstein-Wiener (which is not investigated yet in any other publications)" ↔ 같은 편 [50] "Identification of hammerstein-wiener systems" · [56] | p. 2 ↔ 참고문헌 |
| **D15** | 초록 "the developed model has been utilized to detect possible faults in the electrode-electrolyte interface" ↔ 본문 검출 절차 0 · 미래 과제 "coupled with an online fault detection algorithm" | p. 1 ↔ p. 11 |
| D16 | 인용 쓰임: [6] Sakuda 2011(재료)을 BMS SoC/SoH 근거로 · [21] Westerhoff 2016(EIS 모형)을 "ANN and GA" 묶음에 · [24] 본문 인용 0 | p. 1–2 |
| D17 | 참고문헌 표기: [16] · [57] "O. Noshin" ↔ [15] · [46] "N. Omar"(같은 이름의 성 · 이름 순서가 뒤바뀐 표기로 읽힌다 `[해석]`) · [58] 끝 쪽 "183" · [40] "Sweversb" · [43] "Dobrowieckib" | 참고문헌 |
| D18 | 잡음 위치: 그림 4 출력 ε(k) ↔ 그림 5 분할점(방정식 오차) ↔ 식 15 "input noise term e(k)" | p. 5–6 |
| D19 | 기호: 그림 3 g(x) · f(x) ↔ 본문 f_h · f_w · 그림 4 η ↔ 본문 α · β · ζ · γ | 그림 3 · 4 |
| D20 | "accuracy 74.5% … 6% less RMS error" — 정의 0 · 결론 "increased the accuracy by 18%" = %p(상대 +26 %) | p. 9 · 11 |
| D21 | "proposed and **proved**"(p. 10) ↔ 결론 "This paper **proposed** that …"(p. 11) | p. 10 ↔ 11 |
| D22 | 오기: "call1"(그림 7 캡션) · "Ploynomial"(그림 11a) · "current altitude"(p. 7) · "quantize"(초록) · "try and error"(p. 2) · "simply the identification problem"(그림 5 캡션) | — |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. **구조적 공백 1번의 확인 — 후보 하나가 내려간다.** 원장이 "제목에 system identification" 으로 Q4 공백 1번 후보 첫째에 올린 편은 **식별성을 다루지 않는다** — 다룬 것은 구조 판정(선형 ↔ 비선형)과 그림으로만 남은 블록 적합이다. 75호(Naik 2022)와 같은 형식의 "후보 → 확인으로 닫음" 표본.
2. **Q4 — "식별" 이라는 낱말의 셋째 뜻**: 26호의 "sensitivity = 스윕" · 34호의 "입력 설계 = 정보량" 에 이어, 이 편은 "identification = 구조를 고르고 맞추기" 다. 그리고 그 구조 자체에 **입력으로 못 사는 비식별(블록 이득 · 오프셋 교환)** 이 있고, 저자가 그 비식별 방향 위의 한 점(정규화 미인쇄)에서 블록 모양을 읽어 물리를 배정했다 — `degradation-degeneracy/` 가 합성 truth 로 채점하는 "맞는 곡선 ≠ 맞는 성분 분할" 의 **경험 모형판** 표본이다(우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본 — 여기 옮기지 않는다).
3. **비선형 진단 = 검출이지 귀속이 아니다.** 고정 전류 진폭에서 비선형도는 활성 면적당 분극의 가파른 함수라 접촉 손실 · LAM_PE · 계면층 · 수송이 같은 방향으로 올리고, 순수 BV 는 `A·j₀` 곱 하나만 본다 — 카드의 A1(접촉 ↔ LAM_PE)을 가르는 채널 목록에 **"비선형 진폭 채널은 넣지 않는다(진폭 스윕이 있어도 `C_dl ∝ A` 없이는)"** 를 근거와 함께 남긴다.
4. **측정 규약 경고** — 고임피던스 ASSB 셀의 "소신호 · 고정 상태" 다중정현은 상태를 움직인다(셀 2 2.26 V · SoC 설계 이탈). 합성 truth 에 다중정현 관측을 넣는다면 **진폭을 전압 기준으로 · 둘 이상 · 상태 이동을 메타데이터로**.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★ | **Firouz Y., Relan R., Timmermans J.M., Omar N., Van den Bossche P., Van Mierlo J. 2016** — *Energy* **106**, 602–617 ([46]) | 92 = 1 (새) | **액체셀 도구** — NMC 파우치 BLA(같은 제1저자 선행) · 식 1–9 의 직접 인용처: 분산 식의 원형(R19 ×3.13 이 원형에서도 그런가) · 진폭 · SoC · 온도별 비선형 왜곡을 쟀는가(이 편 "고장 검출" 의 교란 기준선) | Q4 도구 · (c) |
| ★★ | **Widanage W.D., Barai A., Chouchelamane G.H., Uddin K., McGordon A., Marco J., Jennings P. 2016** — *J. Power Sources* **324**, 61–69 (Part 2 · [52]) | 49 · **92** = **2** (재지목) | 다중정현 설계 + Wiener 추정의 리튬이온 선행 — 이 편이 "detected nonlinearity is very weak" 로 요약한 진폭 · SoC 조건 확인 · 49호 진폭 의존(−18 … −27 %)과 같은 연구실 계보 · **원장 ★ 행("Widanage 외 2016 … 49 \| 1") → 49 · 92 = 2**(액체셀 도구) | 입력 설계 · (c) |
| ★★ | **Schoukens M., Tiels K. 2017** — *Automatica* **85**, 272–292 ([48]) | 92 = 1 (새) | 블록 지향 식별 개관 — **블록 사이 정규화 · BLA 로 구조(H ↔ W ↔ H-W) 판정**하는 방법의 원전: 이 편의 이득 · 오프셋 교환(R20)과 구조 의존 모양(D8)을 저자 계보가 어떻게 닫는지 | Q4 도구 |
| ★★ | **Schoukens J., Swevers J., Pintelon R., Van der Auweraer H. 2004** — *Mech. Syst. Signal Process.* **18**, 727–738 ([40]) | 92 = 1 (새) | **입력 설계의 원전** — 비선형 왜곡 아래 FRF 측정을 위한 가진 설계(선 배치 · 진폭 · 실현 · 주기)의 목적함수가 무엇인지 → (d) "분리 설계 ↔ 정보량 설계" 판정의 원전 대조 | (d) · Q4 |
| ★★ | **Relan R., Firouz Y., Timmermans J.-M., Schoukens J. 2017** — *IEEE Trans. Control Syst. Technol.* **25**(5), 1825– ([58]) | 92 = 1 (새) | **액체셀 도구** — 비모수 분석 → PNLSS · "nonlinearity is strong" at low SoC(<10 %) — 비선형도의 **SoC 의존**(고장 검출 교란)을 같은 연구실이 잰 자리 | (c) · Q4 도구 |
| ★ | **Kato Y., Hori S., Saito T., Suzuki K., Hirayama M., Mitsui A., Yonemura M., Iba H., Kanno R. 2016** — *Nat. Energy* **1**, 16030 ([5]) | 64 · **92** = **2** (재지목) | 이 편이 셀 2 임피던스 증가의 기구("the LiCoO2 particles on the surface of the cathode consume more lithium as concentration is increased")를 [5] 에 걸었다 — [5] 가 그 명제를 담는지 확인 · ⚠ **지목 누락** — 64호 후속 표 ★(:559)인데 원장 §1 행 0(원장의 Kato 행은 2018 *JPCL* 9, 607 — 다른 편) | Q2 · (c) |
| ★ | **Schoukens M., Bai E.-W., Rolain Y. 2012** — *IFAC Proc. Volumes* **45**(16), 274–279 ([50]) · **Bai E.-W. 1998** — *Automatica* **34**(3), 333–338 ([56]) | 92 = 1 (새) · 92 = 1 (새) | H-W 식별의 정식화 · 두 단계 알고리즘 — 식별 조건 · 정규화 가정 | Q4 도구 |
| ★ | **Schoukens J., Pintelon R., Dobrowiecki T., Rolain Y. 2005** — *Automatica* **41**, 491–504 ([43]) | 92 = 1 (새) | BLA 이론 · 잡음 / 확률적 왜곡 분산 추정식의 원전 — R19(×3.13)를 닫을 대조처 | Q4 도구 |
| ★ | **Vanhoenacker K., Dobrowiecki T., Schoukens J. 2001** — *IEEE Trans. Instrum. Meas.* **50**, 1097–1102 ([41]) | 92 = 1 (새) | 비선형 왜곡 특성화용 다중정현(검출선 · 홀 ↔ 짝) 설계 — 이 편이 안 쓴 검출선 분석(G8)으로 충 ↔ 방 비대칭(짝수 비선형)을 가를 수 있었는가 | (d) |
| ★ | **Allafi W., Uddin K., Zhang C., Sha R.M.R.A., Marco J. 2017** — *Appl. Energy* **204**, 497–508 ([53]) | 92 = 1 (새) | 온라인 Wiener 추정(액체셀 도구) — "weak as well" 의 조건 | Q4 도구 |
| ☆ | Han B.C., Van der Ven A., Morgan D., Ceder G. 2004 *Electrochim. Acta* 49, 4691 ([59]) · Bazant M.Z. 2013 *Acc. Chem. Res.* 46, 1144 ([60]) | 행 없음 | 식 33 · 34–35 의 출처(물리 해석의 식) | 모형 |
| ☆ | Sakuda A. 외 2011 *J. Power Sources* 196, 6735 ([6]) | 행 없음 | LCO + PLD Li₂S–P₂S₅ 코팅(이 편은 BMS 근거로 잘못 씀 — D16) | Q1 인접 |
| ☆ | Vanhoenacker & Schoukens 2003 ([42]) · Pintelon & Schoukens 2002 ([45]) · Peeters 외 2003 ([44]) · Zhang · Schoukens 2017 ([51]) · Cheng 외 2017 ([47]) · Decuyper 외 2018 ([49]) · Esfahani 외 2017 ([54]) · Guo 2004 학위논문([55]) | 행 없음 | 비선형 검출 · 표현 · 구조 검출 일반 도구 | 도구 |
| ☆ | Mu 외 2017 ([19]) · Andre 외 2011 *JPS* 196, 5334 ([20]) | 행 없음 | EIS 소진폭 관례 | 진폭 |

**교차 참조 (지목 아님 — 이 편이 인용하지 않음)**: Harting N., Wolff N., Krewer U. 2018 *Electrochim. Acta* 281, 378–385(NLEIS Li 도금 검출 — 액체 · **10호 후속 ★ [184] · 원장 행 0 → 지목 누락**) · Barai 2018(49호 흡수 · 진폭 의존) · 34호 Liang 2026(OED 처방).

**4차 묶음 13 편과의 관계**: 이 편은 **어느 편도 인용하지 않는다**(Danilov · Raijmakers · Kim · Deng · Bielefeld · Schmidt · Khalik · Lu · Koerver · Xie · Shao · Ansah — 참고문헌 전수 대조 0). 같은 Q4 축의 다음 도착분은 파일 55 Khalik 2021(DFN 정규화 · 묶음 · 민감도 — 액체셀 도구) · 56 Lu 2022(EIS 로 물리 모형 매개변수 일부 — 액체셀 도구) — **4차 묶음 파일 55 · 56 으로 도착 · 처리 대기**.

**지목 누락 둘** — Kato 2016 *Nat. Energy* 1, 16030(64호 후속 ★ · 원장 행 0 — 이 편 [5] 로 재지목) · Harting 2018 *Electrochim. Acta* 281, 378(10호 후속 ★ [184] · 원장 행 0 — 이 편은 인용 안 함 · 교차 참조로만). 49호 후속 표(등급 칸 없는 옛 표)의 Widanage 2016 은 원장에 ★ 행이 있어 누락 아님.

---

# 이 digest 가 주장하지 않는 것

1. **셀 2 의 비선형이 양극층 전도도 때문이 아니라고 하지 않는다** — 재료 교체가 σ 와 함께 접촉 · 형태 · 계면 화학을 바꿀 수 있고(지면 확인 0), 같은 전류 진폭 비교가 임피던스 크기와 교락된다는 것까지다. 전도도가 주 원인일 수도 있다.
2. **블록 지향 모형이 쓸모없다고 하지 않는다** — H-W 가 낙하 구간을 따라가는 것은 그림에서 보인다(86.5 % · 정의 미인쇄). 주장은 "그 블록 모양에 물리를 배정하는 것은 정규화 · 구조 의존이고, 식별 값 · 불확실도가 지면에 없다" 까지다.
3. **인쇄 식 9–11 로 저자가 실제 계산했다고 단정하지 않는다** — ×3.13(+5 dB)은 인쇄 식 그대로의 기대값이고, 저자 코드 · [46] 원형은 미대조다. 셀 사이 비(">100 times")는 그 배수와 무관하다.
4. **우리 격자 재구성(k = 1 · 3 · 11 + 8j)을 저자 설계로 확정하지 않는다** — 그림 7 · 8a 표지 위치(±0.0004 · ±0.002 Hz)와 f₀ 4 mHz 로 맞춘 것이고, 최저 두 선은 겹친 표지에서 갈랐다.
5. **비선형 진폭 채널이 원리상 접촉 ↔ LAM 을 절대 못 가른다고 하지 않는다** — 순수 BV 의 `A·j₀` 항등과 "같은 방향" 은 `[재현·가정]` · `[해석]` 이고, 면적 스케일이 다른 확산 비선형이 섞이면 지렛대가 생길 수 있다(합성 truth 에서 시험할 물음).
6. **고장 검출이 불가능하다고 하지 않는다** — 이 지면이 문턱 · 반복 · 교란 통제 없이 셀 하나 ↔ 하나의 대비만 보였다는 것까지다.
7. **26호의 인용이 틀렸다고 하지 않는다** — "Parameter Estimation Yes" 는 맞고, "ASSB 식별 문헌" 이라는 기대가 이 편 지면에서 서지 않는다는 것까지다(원장 · 26호 raw 는 그대로).

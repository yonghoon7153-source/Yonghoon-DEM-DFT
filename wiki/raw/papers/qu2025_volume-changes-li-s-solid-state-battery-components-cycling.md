---
title: "Qu et al. 2025 — Deciphering volume changes in Li-S solid-state battery components during cycling: Implication for advanced battery design (Nano Energy 138, 110887)"
description: "정압(스프링+LVDT)·정용적(나사+압력변환기) 자작 fixture 로 전고체 Li–S 셀의 수직 변위와 스택 압력을 실시간 측정해 S·Li2S 양극, LixIn 음극, LPSCl 의 부피 기여를 분리한 측정 논문 — 운전 7 MPa, 첫 몇 사이클에 14–20 µm 수축, Li2S 첫 충전 한 번에 절반"
source_url: local-upload/08d276a4-deciphering_volume_changes_in_ASSLSB_components_during_cycling.pdf (SI 미확보)
doi: 10.1016/j.nanoen.2025.110887
ingested: 2026-09-30
sha256: 6a8801651df911a502218461d06789d95ad8edabfafe3e1cc64b28b2dc44b7b7
tags: [assb, sulfide-electrolyte, li2s, composite-cathode, li-in, mixing-process]
compare:
  system: "ASSB Li–S (sulfide) — 성능 논문이 아니라 부피 변화·스택 압력 측정 논문. 운전 스택 압력 7 MPa 정압 vs 정용적(초기 7 MPa) 비교"
  electrolyte: "Li6PS5Cl (LPSCl, NEI Corporation). 건식 필름 = LPSCl + PTFE 0.5 wt%, heat grinding + rolling → 100 µm, 7/16 in 지름으로 300 MPa 3 min 성형 (사이클 전 단면 SEM 83.2 µm). full cell 은 분말 0.1 g 을 500 MPa 펠릿"
  cathode: "Li2S 또는 S : Super C65 : LPSCl = 2 : 1 : 3 (질량) = 33.3 : 16.7 : 50.0 wt%, 바인더 언급 없음. SE 필름 위에 300 MPa 3 min 압착 (사이클 전 단면 SEM 80.5 µm)"
  li2s_source: "상용 Li2S 99.98 % (Sigma-Aldrich) — 입도·전처리 미기재"
  mixing: "one-step — Li2S(또는 S) + Super C65 + LPSCl 을 한 번에 ZrO2 용기, Fritsch Planetary Micro Mill PULVERISETTE 7, 300 rpm, 4 h. 볼 재질·직경·개수·BPR·총 투입량·분위기 미기재. 성형 압력 300 MPa 3 min (양극/SE), 500 MPa (SE 펠릿), 50 MPa 20 s (Li–In)"
  loading_mg_cm2: "미기재"
  li2s_wt_pct: 33.3
  anode: "Li–In (In 박 0.127 mm 99.99 % + Li 박, Li:In 몰비 1.3, 50 MPa 20 s, 3/8 in) · 부피 분리용 대극은 LTO 필름 (LTO : Super C65 : LPSCl = 6:1:3 + PTFE 0.75 wt%, 100 µm, 5/16 in, 0.7 V vs Li–In 까지 전리튬화). 집전체는 스테인리스 로드"
  first_charge: "본문에 컷오프 수치 없음. Li2S 셀 첫 충전은 [도표, Fig. 3c] 0.85 → 2.4 V vs LTO 대극, 약 11 h. full cell 은 formation 3 사이클 0.05 C 후 0.1 C"
  first_discharge_mAh_gS: "해당 없음 — 측정 논문 (절대 용량 미보고)"
  first_discharge_mAh_gLi2S: "해당 없음 — 측정 논문 (절대 용량 미보고)"
  cycle_capacity_mAh_gS: "해당 없음 — 측정 논문 (Fig. 8a 의 y축은 유지율 %)"
  cycle_capacity_mAh_gLi2S: "해당 없음 — 측정 논문 (Fig. 8a 의 y축은 유지율 %)"
  areal_mAh_cm2: "해당 없음 — 측정 논문 (로딩 미기재)"
  cycles: "100 — [도표, Fig. 8a] 유지율 정압 7 MPa ≈63 % · 정용적 ≈50 % (10·20·30·40·50·60 사이클마다 7 MPa 재압축). CE 는 양쪽 모두 ≈100 %"
  temperature_C: 60
  mechanism: "정압 LVDT 변위 + 정용적 압력변환기 + LTO zero-strain 대극으로 성분 분리. [도표] 총 변위: LTO 대조셀 −2 µm / S 양극 −15 µm / Li2S 양극 −19 µm / LixIn 음극 −42 µm; 압력 강하 −0.12 / −0.41 / −0.60 / −1.4 MPa. 사이클 후 단면 SEM 두께: 정압 양극 −9.4 % SE −12.4 %, 정용적 양극 +9.4 % SE −10.9 %. EIS Ohmic 40 → 60 Ω(정용적, +50 %), 재압축하면 오히려 65 Ω. DRT τ≈1 s 어깨가 정용적에서 소멸. 결론 — 균열은 비가역, 공극은 스택 압력으로 가역. 상 동정(EDS·XRD·라만) 없음"
  our_axis: "★ 조성이 우리와 거의 같다 (SE 50 wt% 동일, 활물질 33.3 vs 30). fixture 설계 수치·성형 압력 세트·LTO 대극 성분분리법·'압력은 절대값보다 유지' 명제가 이식 가능. 절대 용량·로딩·anode-free 구성·집전체 데이터는 없음"
---

# 수집 목적

H. Qu, T. Ding, X. Zhang, D. Qiu, P. Chen, D. Zheng, D. Lu, **D. Qu**,
**"Deciphering volume changes in Li-S solid-state battery components during cycling:
Implication for advanced battery design"**, *Nano Energy* **138** (2025) 110887,
**DOI 10.1016/j.nanoen.2025.110887** (UW–Milwaukee + PNNL, accepted 14 Mar 2025) 의
**절별 해체분석**.

이 위키가 이 논문을 흡수하는 이유는 하나로 모인다 — **이 위키의 가장 큰 구멍이 스택 압력**이기
때문이다.

1. 먼저 들어온 두 digest 가 압력에서 반대 방향으로 비어 있었다. `raw/papers/huang2026_…` 는
   **성형 압력(SE 350 MPa, 양극 450 MPa)만 있고 운전 스택 압력이 한 글자도 없다**(그 digest 의
   G1). `raw/papers/zhang2026_…` 는 **운전 압력 0 / 1 / 4 MPa 를 실측**했지만 그 압력이 셀 안에서
   무엇을 하는지는 성능 곡선으로만 말한다. 이 논문(doi 10.1016/j.nanoen.2025.110887)은 그 사이
   — **운전 압력이 셀 내부에서 무엇을 하는가** — 를 직접 잰 첫 자료다.
2. 이 논문의 복합양극은 **Li2S : Super C65 : LPSCl = 2 : 1 : 3 (질량) = 33.3 : 16.7 : 50 wt%** 다.
   우리 [[li2s-assb-reference-cell]] 의 **Li2S : LPSCl : AB = 30 : 50 : 20** 과 **SE 50 wt% 가
   정확히 같고** 활물질도 30 vs 33 으로 거의 같다. 이 위키에 들어온 논문 중 **우리 조성에 가장
   가까운 셀**이며, 그래서 이 논문의 부피·압력 수치는 우리 셀에 거의 그대로 걸린다.
3. [[anode-free-li2s-assb]] 의 미결 항목 4번("스택 압력·집전체 계면이 침적 형태를 정한다 — 이
   위키에 아직 근거 논문이 없다")의 **첫 근거**가 여기서 나온다. 단 이 논문은 anode-free 가 아니라
   Li–In / LTO 대극이고, 그래서 채울 수 있는 것은 "압력" 쪽이지 "집전체" 쪽이 아니다.

**이 논문은 성능 논문이 아니라 측정·기전 논문이다.** 절대 용량(mAh g⁻¹)·로딩(mg cm⁻²)·
면적용량(mAh cm⁻²)이 **논문 전체에 한 번도 나오지 않는다.** 그래서 아래 `compare:` 의 성능 키는
"해당 없음 — 측정 논문" 으로 두었고, 대신 **fixture 설계·측정 조건·변위/압력 실측값**에 지면을
몰았다.

**표기 규칙** (이 위키 관례 3구분 + 1):
- `[인쇄]` — 논문 본문/캡션/그림 주석에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

- 원본 파일: 업로드된 `08d276a4-deciphering_volume_changes_in_ASSLSB_components_during_cycling.pdf`
  (**9쪽**, *Nano Energy* 138 (2025) 110887 조판 그대로). 저장소에 바이너리 원문은 넣지 않는다.
- **SI 는 확보하지 못했다.** 본문이 인용하는 SI 는 **Fig. 1S**(스택 압력 fixture 무게가 셀 무게의
  80–90 %)와 **Video 1S**(Li∣SSE∣Li 대칭셀의 상보적 부피 거동) **둘뿐**이고, 둘 다 이 digest 에서는
  **"SI 미확보"** 로만 표시한다 (아래 §12). Table S 는 인용 자체가 없다.
- 크로핑 그림: `raw/figures/qu2025_volume-changes-li-s-solid-state-battery-components-cycling/`
  — Fig. 1–8 전부 (`fig_1.png` … `fig_8.png`), 캡션 앵커로 자동 크로핑. **8장 전부 Read 로 봤다**
  (§18).
- **압력 표기 규율** (이 digest 의 하드룰): 모든 압력에 **성형(fabrication/formation)** 인지
  **운전(operating/stack)** 인지를 붙인다. 이 논문은 두 압력이 **50배 이상** 차이 난다
  (성형 300–500 MPa vs 운전 7 MPa).

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

이 절이 이 digest 의 가장 중요한 산출물이다.

| # | 공백 | 왜 문제인가 |
|---|---|---|
| G1 | **절대 용량이 논문 전체에 없다.** mAh g⁻¹(S) 도 mAh g⁻¹(Li2S) 도 mAh cm⁻² 도 없다. Fig. 8a 의 y축은 **"Capacity retention / %"** 다. | 이 논문의 셀이 "좋은 셀" 인지 "죽은 셀" 인지 알 수 없다. 63 % 유지가 500 mAh g⁻¹(Li2S) 에서인지 100 에서인지에 따라 해석이 완전히 달라진다. 우리 reference cell 과의 성능 대조는 **불가능**하다. |
| G2 | **활물질 로딩(mg cm⁻²)이 없다.** 양극 조성비(2:1:3)와 성형 압력은 있으나 질량도 두께도 본문에 없다 (두께는 Fig. 7d 의 SEM 주석 ~80.5 µm 가 유일). | 부피 변화의 절대값(µm)을 **활물질 몰수로 정규화할 수 없다.** "14–20 µm 수축" 이 우리 셀에서 얼마가 될지 환산이 막힌다 — 이 논문의 **가장 뼈아픈 공백**이다. |
| G3 | **Fig. 8 의 셀 화학이 명시되지 않았다.** 본문은 "ASSLB full cells" 라고만 쓴다. 양극이 S 인지 Li2S 인지, 음극이 Li–In 인지 LTO 인지 캡션에도 본문에도 없다. Fig. 7 의 SEM 은 "sulfur cathode" 라고 못 박혀 있으므로 **S 양극으로 추정되나 확인 불가**. | 이 논문의 **결론 그림(성능·EIS)이 어느 셀의 것인지 모른다.** Li2S 양극이 S 양극보다 부피 변화가 크다는 것이 §5 의 핵심인데, 성능 비교는 (아마) S 양극으로만 했다. |
| G4 | **전압창이 본문에 없다.** "prelithiated to 0.7 V versus a Li/In alloy" 외에 충·방전 컷오프 수치가 한 번도 안 나온다. 그림 y축에서 읽을 수밖에 없다 (`[도표]` §5). 기준전극도 셀마다 다르다 (vs Li–In / vs LTO / vs Li_x-LTO). | 이 위키의 단위 규율(전압에 기준 명시)을 원문이 지키지 않는다. Li2S 셀의 첫 충전 컷오프가 몇 V 인지가 활성화 논의의 핵심인데 그 값이 없다. |
| G5 | **C-rate 가 본문과 캡션에서 어긋난다.** `[인쇄, §2.4]` "Constant current cycling at a rate of **0.05 C** … for displacement or pressure" 인데 **Fig. 3 캡션은 "C/10"**, Fig. 2·4 캡션은 "C/20"(=0.05 C). | Fig. 3 이 이 논문의 본체인데 그 셀의 전류가 본문과 다르다. 두 값 중 어느 것이 맞는지 알 수 없다. |
| G6 | **"14–20 μm shrinkage out of 100 μm" 의 분모 100 µm 가 무엇인지 모른다.** `[인쇄, §3]`. SE 필름도 100 µm, LTO 필름도 100 µm 로 만들지만, Fig. 7d 의 사후 SEM 은 양극 ~80.5 µm + SE ~83.2 µm = **163.7 µm** 이고 여기에 음극이 더 붙는다. | "15–20 % 수축" 이라는 이 논문의 대표 수치의 **분모가 정의되지 않았다.** `[재현]` 만약 분모가 양극+SE(163.7 µm)라면 14–20 µm 는 **8.6–12.2 %** 다. |
| G7 | **셀 개수·오차·재현성이 없다.** 유일한 언급은 `[인쇄, §3]` "achieving exact reproducibility of the prelithiation for LTO and Li_xIn was challenging, and the results presented were based on the data from **three different cells**" — 이것도 재현성 데이터가 아니라 **Fig. 5 의 세 곡선이 서로 다른 셀에서 왔다**는 고백이다. | Fig. 5 의 "성분 분해" 는 **세 개의 다른 셀을 100 % 로 정규화해 겹친 것**이고, 저자 스스로 "more qualitative than quantitative", "adding the red and blue lines might not exactly result in the black curve" 라고 쓴다. 논문 제목의 "Deciphering" 이 얹혀 있는 자리가 여기다. |
| G8 | **"around 6 mm" 오기.** `[인쇄, §3]` 1차 방전의 전체 셀 부피 감소를 "**around 6 mm**" 라고 쓴다. 단위가 µm 여야 한다 (Fig. 5a 의 축은 µm). | 이 논문에서 발견한 명백한 단위 오기. 그대로 인용하면 1000배 틀린다. |
| G9 | **성분 합이 맞지 않는다.** `[인쇄]` 1차 방전에서 양극 **+3 µm**, 음극 **−11 µm** → 합 **−8 µm** 인데 전체 셀은 "**−6 µm**" 라고 쓴다. `[재현]` 차이 2 µm (25 %). | G7 의 정규화 문제의 직접 결과. 저자도 미리 면피해 두었지만, **성분 분해의 정량성이 ±25 % 수준**이라는 뜻이다. |
| G10 | **fixture 의 "20 µm = 10⁻² MPa" 환산이 자기 수치와 맞지 않는다.** `[인쇄, §2.1]` 스프링 **4개**, 각 **14.29 lb mm⁻¹**, 플런저 지름 **0.495 in**. `[재현]` 4개 병렬 = 254.3 N mm⁻¹, 플런저 단면적 1.242 cm² → 20 µm 압축 = 5.09 N = **0.041 MPa**. 논문의 10⁻² MPa 은 **스프링 1개**로 계산해야 나온다 (0.0102 MPa). | fixture 를 그대로 베껴 만들 때 **정압 허용오차가 4배 나빠진다.** 우리가 만든다면 스프링 상수를 1/4 로 하거나 변위 허용범위를 5 µm 로 잡아야 논문이 주장하는 "10⁻² MPa 이내" 가 된다. |
| G11 | **"SSE 는 부피 변화가 없다" 의 근거가 약하다.** `[인쇄, §3]` LTO∣LPSCl∣LTO 대조셀에서 "our observation did not show any volume changes in LPSCl". 그런데 `[도표, Fig. 2b]` 같은 셀의 압력은 **0 → −0.12 MPa** 로 떨어지고 `[도표, Fig. 2a]` 변위도 120 h 부근에서 −2 µm 로 내려간다. | "LPSCl 은 안 움직인다" 는 전제 위에 §5–§7 의 성분 분해 전체가 서 있다. 그 전제의 잔차가 −2 µm / −0.12 MPa 이고, Fig. 3 의 신호(−13 ~ −19 µm)의 **10–15 %** 다. 작지만 0 이 아니다. |
| G12 | **Fig. 7 의 SEM 수치와 본문 서술이 어긋난다.** `[인쇄, 그림 주석]` 사이클 전 SSE 83.2 / 양극 80.5 µm · 정압 후 SSE 72.9 / 양극 72.9 · 정용적 후 SSE 74.1 / 양극 **88.1**. 본문은 정용적에 대해 "the cathode's thickness increased **slightly** while the SSE's thickness **slightly** decreased" 라고 쓴다. `[재현]` 양극 **+9.4 %**, SSE **−10.9 %** — 정압의 −9.4 % / −12.4 % 와 **같은 크기**다. | "slightly" 라는 단어가 **자기 데이터의 10 % 변화**를 가린다. 정용적에서 SSE 는 정압과 거의 똑같이 얇아졌고, 그만큼을 양극이 부풀어 먹었다. 이게 실은 이 논문에서 가장 깔끔한 결과인데 서술이 그것을 흐린다. |
| G13 | **볼밀 조건이 반쯤 없다.** `[인쇄, §2.2]` ZrO2 용기 · **300 rpm 4 h** · Fritsch Planetary Micro Mill **PULVERISETTE 7** 까지는 있다. 없는 것: 볼 재질·직경·개수, **BPR**, 용기 용량, 총 투입량, 정/역회전·휴지 주기, 분위기(글로브박스 안이라는 것 외). | Kim 2023 의 G1(전부 없음)보다 낫고 Huang 2026 의 G14 와 같은 수준이다. [[composite-cathode-mixing-routes]] 의 칸이 반만 찬다. 단 이 논문은 **Li2S·탄소·LPSCl 을 한꺼번에 넣는 명백한 one-step** 이라 그 축은 확정된다. |
| G14 | **Li2S 입도·전처리가 없다.** `[인쇄]` "Lithium Sulfide (99.98 %) … Sigma-Aldrich" 가 전부. 볼밀 후 입도도 없다. | 우리 pristine Li2S 와 같은 출처일 가능성이 높으나 확인 불가. 입자 크기가 부피 변화의 파괴 양상을 정하는데 그 값이 없다. |
| G15 | **Fig. 7 의 "sulfur deposition" 결론이 정량 없이 그림 3장에 얹혀 있다.** 결정 크기·공극률 수치가 하나도 없다 (`[도표]` 로만 읽을 수 있다). EDS·XRD·라만 등 상 동정이 전혀 없어 그 "sulfur crystal" 이 S 인지 LPSCl 결정인지 **원소 증거가 없다**. | ASSB 단면 SEM 에서 S 와 LPSCl 은 모두 밝은 결정으로 보인다. 상 동정 없는 "sulfur crystal" 은 형태학적 추정이다. |
| G16 | **Li2S 양극 셀의 성능·사후분석이 없다.** Li2S 는 Fig. 3c,d(변위·압력)에만 나오고 Fig. 7(SEM)·Fig. 8(성능·EIS)에는 없다. | 제목은 "Li-S solid-state battery components" 이고 초록도 "sulfur, Li₂S cathodes" 를 나란히 쓰지만, **Li2S 양극은 부피 측정 한 세트가 전부**다. 우리에게 가장 중요한 축이 반만 있다. |
| G17 | **LTO 의 화학식이 틀렸다.** `[인쇄, §2.2]` "**Li4Ti4O12** (LTO)". 상용 zero-strain LTO 는 Li4Ti5O12 다. | 교정 누락. 실제로 산 것은 battery-grade LTO 일 것이나, 논문에 적힌 식은 다른 물질이다. |
| G18 | **SI 미확보.** Fig. 1S(스택 압력 fixture 가 셀/배터리 무게의 80–90 %)와 Video 1S(Li∣SSE∣Li 대칭셀)를 보지 못했다. | 본문의 두 주장 — (a) 압력 fixture 무게 80–90 %, (b) Li 대칭셀의 상보적 부피 거동으로 전체 부피 변화 ≈ 0 — 의 근거를 **확인하지 못했다.** 둘 다 이 digest 에서는 인용만 하고 값으로 쓰지 않는다. |
| G19 | **"cycling stack pressure above 7 MPa are crucial" 의 출처가 없다.** `[인쇄, §1]` 이 문장에 인용번호가 붙어 있지 않다. 7 MPa 라는 이 논문의 **모든 설정값의 근거**인데 문헌도 자체 실험도 없다. | 7 MPa 가 어디서 왔는지 모른 채 논문 전체가 그 값 하나로 돌아간다. Zhang 2026 은 같은 계(LPSCBr, Li2S)에서 **4 MPa·심지어 1 MPa** 로 돌렸다 — 이 위키 안에서 이미 충돌한다. |
| G20 | **정압 셀도 100 사이클에 유지율이 떨어진다.** `[인쇄, §3]` "the cell cycled at constant pressure **maintained it capacity well** throughout the 100 cycles" 인데 `[도표, Fig. 8a]` 검은 점은 **≈63 %** 로 끝난다. | 초록·결론이 "정압이 좋다" 로 읽히지만, 정압도 100 사이클에 37 % 를 잃는다. 차이는 **63 % vs 50 %** (13 포인트)다. **"maintained well" 은 상대 진술이다.** |

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 1·9쪽:

| 항목 | 값 |
|---|---|
| 제목 | Deciphering volume changes in Li-S solid-state battery components during cycling: Implication for advanced battery design |
| 저자 | Huainan Qu ᵃ, Tianyao Ding ᵃ, Xiaoxiao Zhang ᵃ, Dantong Qiu ᵃ, Peng Chen ᵃ, Dong Zheng ᵃ, Dongping Lu ᵇ, **Deyang Qu ᵃ** |
| 소속 | a. Department of Mechanical Engineering, College of Applied Science and Engineering, **University of Wisconsin Milwaukee**, Milwaukee, WI 53072, United States · b. Energy and Environment Directorate, **Pacific Northwest National Laboratory**, Richland, WA 99354, United States |
| 학술지 | *Nano Energy* **138** (2025) **110887**, "Full paper" (Elsevier) |
| DOI | **10.1016/j.nanoen.2025.110887** |
| 접수/개정/게재 | Received **26 November 2024** · Received in revised form **13 February 2025** · Accepted **14 March 2025** · Available online **22 March 2025** |
| 키워드 | Solid-state Li-S battery · **Stack pressure** · **Fracture and void formation** · Cell design |
| 재정 | US DOE EERE Office of Vehicle Technologies, Advanced Battery Materials Research Program (**Battery500 Consortium**); Contract DEAC02–5CH11231, DEAC02–98CH10886; PNNL 은 Battelle, DE-AC05–76RL01830 |
| 저작권 | © 2025 Elsevier Ltd. All rights reserved (**open access 아님**) |
| 데이터 | "Data will be made available on request" |
| 참고문헌 | **11개** (매우 짧다 — G19 와 함께 읽을 것) |
| CRediT | Qu Huainan(Visualization·Investigation·Formal analysis·Data curation) · Ding Tianyao · Zhang Xiaoxiao · Qiu Dantong · Chen Peng · Zheng Dong · **Lu Dongping**(Writing–review & editing·Funding) · **Qu Deyang**(Writing–original draft·Supervision·Conceptualization, 교신) |

`[해석]` 교신저자 Deyang Qu 는 UWM Distinguished Professor / Johnson Controls Endowed Chair in
Energy Storage Research 이고, 공저자 Dongping Lu 는 PNNL(Battery500) 쪽이다. **Battery500 의
관심(셀 수준 실용성)**이 초록이 아니라 서론의 문제 설정 — "3×6 in. 파우치에 수백 톤을 못 건다"
— 에 그대로 드러난다.

---

## 1. 한 문단 요약

`[인쇄, Abstract]` 저자들은 **정압(constant pressure)과 정용적(constant volume)** 두 조건에서
전고체 셀을 돌릴 수 있는 **자작 fixture 두 개**를 만들었다. 정압 쪽은 스프링 4개로 7 MPa 를
유지하며 **LVDT** 로 수직 변위를 실시간으로 재고, 정용적 쪽은 나사로 높이를 고정하고
**압력 변환기**로 압력 변화를 실시간으로 잰다. zero-strain 물질인 **LTO 를 대극**으로 써서 황
양극·Li2S 양극·Li_xIn 음극·SSE 의 부피 기여를 **하나씩 분리**했다. 관측: 셀 전체 부피는 첫 몇
사이클에서 **14–20 µm 줄고**(총 두께의 "15–20 %"·분모 불명 G6) 그 뒤 **±1 µm** 진폭으로
안정화한다. **Li2S 양극이 S 양극보다 수축이 크다** — Li2S 는 첫 단계가 충전(산화·탈리튬화)이고
Li2S 의 몰부피가 S 의 약 2배이기 때문이다. Li_xIn 음극은 **−42 µm** 로 세 성분 중 가장 크게
줄어든다. 단면 SEM + EIS/DRT 로 사이클 중 두 가지 구조 변화를 확인했다: **(1) 활물질 1차 입자의
비가역 균열, (2) 전극 매트릭스 내 공극 형성**. 저자들의 결론은 **"균열은 영구적이지만 공극은
스택 압력으로 막을 수 있다"** — 압력이 입자 재배열을 유도해 삼상 계면을 유지하기 때문이다.

`[해석]` 한 문장으로: **이 논문은 "압력이 왜 필요한가" 에 처음으로 µm 단위의 답을 준다.
그러나 "얼마나 필요한가" 는 답하지 않는다** (7 MPa 하나만 시험했다 — G19, §15).

---

## 2. p.1 — Abstract / Introduction

### 2.1 Introduction 이 세운 문제 `[인쇄]`

- 산화물 양극 + 흑연 음극의 기존 Li-ion 은 **300 Wh kg⁻¹** 에서 거의 한계. Li 금속 음극 ASSLB 는
  **최대 500 Wh kg⁻¹** 가능. 황화물 SE 는 이미 **10⁻³ S cm⁻¹ 이상**[1,2].
- 병목은 **계면 저항과 느린 전하이동**[3].
- 액체 셀과의 결정적 차이: "Unlike liquid cells, where electrolyte fluid fills pores, restoring the
  interface and mending damage, in SSE cells, **the immobility of the SSE shuts down the
  electrochemical interface when pore emerge**."
- ★ **압력 수치의 출처 문장** `[인쇄]`: "Typically, a **formation pressure exceeding 350 MPa** and a
  **cycling stack pressure above 7 MPa** are crucial for satisfactory battery operation."
  → **인용번호 없음** (G19).
- 실용성 문제: 대면적 SE 에 수백 톤을 거는 것은 불가 — 예로 **3×6 in. 파우치**. 비용·덴드라이트·
  조기 단락[3] 도 문제. **압력 fixture 무게가 셀/배터리 무게의 80–90 %** 를 차지한다 (Fig. 1S —
  SI 미확보 G18).
- 목표: 각 성분의 부피 변화를 이해해 **"cell breathing"** 을 상쇄하는 공학 전략을 만드는 것.

`[해석]` 서론의 논지는 명확하다 — **7 MPa 를 걸 수 있으니 좋다가 아니라, 7 MPa 를 걸어야만
한다면 상용화가 막힌다.** 그래서 이 논문은 "압력을 어떻게 줄일까" 의 전 단계로 "압력이 하는 일이
정확히 무엇인가" 를 잰다. 이 프레임은 Zhang 2026 이 1 MPa 로 내려간 동기와 **같은 문제의식**이다.

### 2.2 Abstract 의 명제 4개 `[인쇄]`

1. 정압·정용적 fixture 를 자작해 기계·전기화학 거동을 동시에 관측했다.
2. 정압 사이클에서 **수직 변위**, 정용적 사이클에서 **압력 변화**를 모니터해
   **S / Li2S 양극, Li_xIn 음극, SSE 의 부피 변화를 decouple** 했다.
3. SEM + EIS 가 두 가지 구조 변화를 확인: **(1) 활물질 입자의 비가역 균열, (2) 전극 매트릭스 내
   공극 형성**.
4. **"While the fractures in primary particles are permanent, void formation can be mitigated
   through stack pressure, which promotes particle rearrangement in the electrode matrix."**

---

## 3. p.2–3 — §2 Methods (★ 재현에 필요한 전부)

### 3.1 정압 fixture — 변위 셀 (Fig. 1a) `[인쇄, §2.1]`

| 항목 | 값 |
|---|---|
| 셀 형식 | 자작 원통형(cylindrical) 셀 |
| 플런저 | **Cr12MoV 계 스테인리스강** 2개, 각 **지름 0.495 in** |
| 몸통 | **PEEK 튜브, 내경 0.5 in** |
| 밀봉 | 양단 **Teflon seal**, 개스킷에 **수동으로** 조여 기밀 |
| 구속 | 고정 하판 + **조절 가능한 상판** 사이에 셀 고정 |
| 스프링 | **4개**, 각 **스프링 상수 14.29 pounds per millimeter** |
| 초기 압력 | **7 MPa (운전 스택 압력)** |
| "정압" 의 정의 | 운전 중 변위 범위 **20 µm 또는 10⁻² MPa** 이내면 정압으로 간주 (G10 — 자기모순) |
| 변위 센서 | **LVDT, HGSI LPPS-SL-010** |
| 왜 LVDT 인가 | `[인쇄]` 레이저 변위 센서를 쓴 선행 fixture[4] 보다 **훨씬 싸고 내구성이 좋다** |

★ `[재현]` **우리가 만들 수 있게 환산한 수치** (계산식 병기):

| 유도량 | 값 | 식 |
|---|---|---|
| PEEK 튜브 내경 | **12.70 mm** | 0.5 in × 25.4 |
| 플런저 지름 | **12.573 mm** | 0.495 in × 25.4 → 반경 틈새 편측 **63.5 µm** |
| 플런저 단면적 | **1.2416 cm²** | π(12.573/2)²/100 |
| 7 MPa 에 필요한 축력 | **869 N = 88.6 kgf = 195 lbf** | 7×10⁶ Pa × 1.2416×10⁻⁴ m² |
| 스프링 1개 상수 | **63.56 N mm⁻¹** | 14.29 lb mm⁻¹ × 4.4482 N/lb |
| 스프링 4개(병렬) 합 | **254.3 N mm⁻¹** | ×4 |
| 7 MPa 를 만드는 스프링 압축량 | **3.42 mm** | 869 N ÷ 254.3 N mm⁻¹ |
| 변위 20 µm 당 압력 변화 (4개) | **0.041 MPa** | 254.3 × 0.02 mm ÷ 1.2416 cm² |
| 변위 20 µm 당 압력 변화 (1개) | **0.0102 MPa** | → 논문의 "10⁻² MPa" 은 **스프링 1개 기준** (G10) |
| 0.01 MPa 를 넘지 않는 변위 허용범위 (4개) | **4.9 µm** | 0.01 MPa × 1.2416 cm² ÷ 254.3 N mm⁻¹ |

`[해석]` 즉 **논문의 fixture 는 실측 변위 20 µm 구간에서 압력이 7.00 → 6.96 MPa (−0.6 %) 로
떨어진다.** 이것을 "정압" 이라 부르는 것은 타당하지만, 논문이 적은 "10⁻² MPa" 은 4배 낙관이다.
우리가 복제한다면: **스프링 4개 + LVDT 는 그대로 두되, 압력 허용오차를 0.04 MPa 로 정직하게
적거나, 스프링 상수를 3.6 lb mm⁻¹ 급으로 낮추고 초기 압축량을 13.7 mm 로 키운다.**

`[도표, Fig. 1a]` 도면은 폭발도 + 단면도 2장. 위에서부터 **LVDT → 상판 → 스프링 4개가 끼워진
나사봉 4개 → 상부 플런저 → (PEEK 셀 몸통 = 노란 원통) → Seal → 하부 플런저 → 고정 하판**.
LVDT 는 상판을 관통해 **상부 플런저의 머리에 직접 닿는다**(단면도에서 확인). 나사봉이 곧
스프링 가이드다. **치수 표기는 도면에 없다** — 위 표의 두 치수(0.495 in, 0.5 in)가 논문이 주는
전부다.

### 3.2 정용적 fixture — 압력 셀 (Fig. 1c) `[인쇄, §2.1]`

| 항목 | 값 |
|---|---|
| 셀 | **동일한 원통형 셀** (스프링만 없다) |
| 압력 센서 | **압력 변환기(pressure transducer), ATO DYHW-116** — 셀과 함께 **두 고정판 사이**에 둔다 |
| 가압 | **수동 프레스(hand press)로 7 MPa 까지** 올린 뒤 |
| 높이 고정 | **나사 4개를 조여** 그 초기 압력에서의 높이를 유지 |
| 측정 | 충·방전 중 셀에 걸리는 압력을 실시간 모니터 → **정용적 운전** |

`[도표, Fig. 1c]` 도면: 상판에 **나비너트(wing nut) 4개**가 보이고 스프링이 없다. 하부에 **검은
원통형 로드셀/압력변환기**가 플런저 아래 깔려 있다. 단면도에서 셀 몸통 중간의 초록·빨강 링이
개스킷·시일이다.

`[해석]` **두 fixture 의 차이는 "스프링이 있나 없나" 하나다.** 같은 셀 몸통·같은 플런저를
쓰므로 두 조건의 비교는 깨끗하다. 이 단순함이 이 논문의 최대 장점이다. 우리가 복제할 때도
**셀 몸통 1종 + 상부 어셈블리 2종**으로 만들면 된다.

`[인쇄, Fig. 1 캡션]` "Illustration of home-made fixtures for the real-time monitoring cell
displacement under **constant pressure (a)** and **pressure changes in a constant volume (c)**.
The corresponding height variations and pressure variations during cycling are shown in (b) and
(d), respectively." — `[인쇄, §2.1]` **(b)·(d) 는 S∣SSE∣LiIn full cell** 의 높이·압력 변화다.
`[도표, Fig. 1b]` 전압 **0.6–2.4 V** (vs Li–In), 80 h 에 **≈10 사이클**, 변위 **0 → −22 µm**.
`[도표, Fig. 1d]` 같은 전압창, 80 h, 압력 **0 → −1.0 MPa**.

### 3.3 재료와 전극 (★ 우리 조성과 거의 같다) `[인쇄, §2.2]`

| 재료 | 출처·사양 |
|---|---|
| **Li6PS5Cl (LPSCl)** | **NEI Corporation** 구매 |
| Indium 박 | **0.127 mm 두께, 99.99 %**, ThermoFisher Scientific |
| LTO | "battery grade **Li4Ti4O12**" (식 오기 G17), Sigma-Aldrich |
| **Li2S** | **99.98 %**, Sigma-Aldrich (입도 미기재 G14) |
| S | **99.98 %**, Sigma-Aldrich |
| Li 박 | Sigma-Aldrich |

**LTO 대극 (zero-strain 기준 전극)**

| 단계 | 조건 |
|---|---|
| 조성 | **LTO : Super C65 : LPSCl = 6 : 1 : 3 (질량)** = 60 : 10 : 30 wt% |
| 볼밀 | **ZrO2 용기**, **300 rpm, 4 h**, **Fritsch Planetary Micro Mill PULVERISETTE 7** |
| 필름화 | 건식 공정[5] · **PTFE 0.75 wt%** 첨가 → **heat grinding + rolling** → **100 µm 필름** |

**복합양극 (S 또는 Li2S)** ★

| 단계 | 조건 |
|---|---|
| 조성 | **Li2S 또는 S : Super C65 : LPSCl = 2 : 1 : 3 (질량)** |
| `[재현]` wt% | **활물질 33.3 : 탄소 16.7 : LPSCl 50.0 wt%** |
| 볼밀 | **"the same conditions as LTO electrode"** → ZrO2 용기, **300 rpm 4 h, Pulverisette 7** |
| 혼합 경로 | **one-step** — 활물질·탄소·SE 를 한 번에 넣는다 (별도 전처리·탄화·용액 단계 없음) |
| 바인더 | 양극에는 **언급 없음** (SE 필름·LTO 필름에만 PTFE) |
| 미기재 | 볼 재질/직경/개수, BPR, 총 투입량, 분위기, 로딩(G2), 양극 필름 두께(G2) |

**SE 필름**

| 단계 | 조건 |
|---|---|
| 조성 | LPSCl 분말 + **PTFE 0.5 wt%** |
| 공정 | heat grinding + rolling → **100 µm 필름** |

★ `[해석]` **이 양극은 우리 [[li2s-assb-reference-cell]] 과 사실상 같은 계열이다.**

| | 이 논문 | 우리 |
|---|---|---|
| 활물질 | Li2S **33.3 wt%** | Li2S **30 wt%** |
| SE | LPSCl **50.0 wt%** | LPSCl **50 wt%** ← **동일** |
| 탄소 | Super C65 **16.7 wt%** | AB **20 wt%** |
| 바인더 | 없음 (양극) | 없음 |
| 혼합 | **one-step** planetary 300 rpm 4 h | one-step BM (주 경로) |

**SE 50 wt% 가 정확히 같고 나머지도 ±3 wt% 안**이다. 이 위키에 들어온 논문 중 우리 조성에 가장
가깝다 (Kim 2023 은 SE 0 %/액체, Huang 2026 은 SE 40 %, Zhang 2026 은 SE 40 %). → 이 논문의
부피·압력 수치는 **조성 보정 없이** 우리 셀에 1차 근사로 쓸 수 있다.

### 3.4 셀 제작 — 성형 압력 전부 `[인쇄, §2.3]`

| 부품 | 치수 | **성형 압력 (fabrication)** |
|---|---|---|
| SE 필름 | **지름 7/16 in** (= 11.11 mm, `[재현]` 0.970 cm²) | **300 MPa, 3 min** |
| LTO 필름 | **지름 5/16 in** (= 7.94 mm, `[재현]` 0.495 cm²) | **300 MPa, 3 min** |
| Li/In 합금 | **지름 3/8 in** (= 9.53 mm, `[재현]` 0.713 cm²) | In 박 + Li 박, **Li:In 몰비 1.3**, **50 MPa, 20 s** |
| 양극/SE 접합체 | 양극을 **7/16 in SE 필름 위에** 압착 | **300 MPa, 3 min** |
| **full cell 용 SE 펠릿** | LPSCl **분말 0.1 g** | **500 MPa** (시간 미기재) |
| 집전체 | **스테인리스 로드 2개** (PEEK 원통 셀 케이스의 양단 플런저) | — |

조립:
- **LTO 반쪽셀** = Li/In 박 + SE 필름 + LTO 필름 을 PEEK 원통 셀에.
- **변위/압력 시험 셀** = LTO 필름 + 압착된 SE 필름 + 양극 필름.
- **정압·정용적 full cell** = 0.1 g SE 분말을 **500 MPa** 로 펠릿 → 한쪽에 압착된 양극 필름,
  반대쪽에 Li/In 박.

★ `[해석]` **성형 압력과 운전 압력은 43–71배 차이난다** (300–500 MPa vs 7 MPa). 이 위키에서
Huang 2026(350/450 MPa 성형, 운전 미기재)·Zhang 2026(250/400 MPa 성형, 0–4 MPa 운전)과
**같은 자릿수 구조**다. 아래 §15 에 세 논문을 나란히 놓았다.

`[해석]` 주목할 비대칭: **Li–In 은 50 MPa 로만 눌렸다** (다른 성형의 1/6–1/10). Li 은 연해서
고압에서 흘러나온다는 실무 때문으로 보이나 논문은 이유를 적지 않는다.

### 3.5 셀 시험 조건 `[인쇄, §2.4]`

| 항목 | 값 |
|---|---|
| 사이클러 | **Landt Battery Testing System** |
| LTO 전리튬화 | **0.7 V vs Li/In 합금** 까지, **0.05 C**, **운전 압력 7 MPa** |
| full cell 사이클 | **formation 3 사이클 @0.05 C** → 이후 **0.1 C** |
| 정압 조건 | **7 MPa 로 유지하며** 사이클 |
| 정용적 조건 | **초기에만 7 MPa 까지** 가압 후 높이 고정 |
| **온도** | **모든 전기화학 시험 60 °C** |
| 변위/압력 측정 | **정전류 0.05 C** + 동시 모니터, **BioLogic** 장비 (G5 — Fig. 3 캡션은 C/10) |
| 측정 온도 | **시험 내내 60 °C 유지** |

### 3.6 분석 `[인쇄, §2.4]`

| 기법 | 조건 |
|---|---|
| AC 임피던스 | **PARSTAT 4000**, **상온에서 측정**(사이클은 60 °C), **1 MHz – 1 Hz**, 섭동 **10 mV**, 여러 사이클에서 |
| DRT | 임피던스 스펙트럼을 시간영역으로 변환 (알고리즘·정규화 파라미터 **미기재**) |
| 단면 SEM | **Hitachi S-4800 FESEM**. `[도표, Fig. 7 정보바]` **3.0 kV, WD 8.6–8.9 mm, ×8.00k(상단행) / ×700(하단행)**, 촬영일 **2024-08-12** |
| 분위기 | **모든 재료 준비·조립·시험을 Ar 글로브박스**(O₂·H₂O **< 1 ppm**)에서 |

`[해석]` ★ **EIS 를 상온에서 재고 사이클은 60 °C 에서 했다** — 임피던스 값(Ohmic ≈40 Ω)은 운전
온도의 값이 아니다. 논문은 이 차이를 언급하지 않는다. 절대값 비교는 불가, **같은 온도에서의
상대 비교**로만 읽어야 한다.

---

## 4. p.3 — §3 결과 ① LTO∣LPSCl∣LTO 대조셀 (Fig. 2)

`[인쇄]` LTO 를 고른 이유는 **zero-strain** — 충·방전 내내 부피가 일정하다[6]. 이 대극 덕분에
양극·음극의 부피 변화를 **독립적으로** 볼 수 있다. LAGP[7]·LPSCl[4] 의 부피 변화가 보고된 바
있으나 **"our observation did not show any volume changes in LPSCl"**. 이 무변화는 LPSCl 이
보관·사이클 중 활물질과 화학반응하지 않는다는 가정을 깐다.

`[인쇄, Fig. 2 캡션]` "Displacements (a) and pressure variations (b) during the cycling of a
pre-lithiated LTO∣**LIPSCl**∣LTO symmetrical cell. The cells were cycled at **C/20** rate."
(캡션의 "LIPSCl" 은 오타; 캡션에서만 반복된다.)

`[도표, Fig. 2a]` 좌축 전압 **−1 ~ +1 V**(대칭셀이므로 ±0.8 V 로 컷오프), 우축 변위
**+10 ~ −10 µm**, x축 **0–130 h, 약 13 사이클**. 빨간 변위선은 **±0.5 µm 안에서 흔들리며 거의
수평**, 110–125 h 구간에서 **−2 µm** 까지 내려갔다가 돌아온다.

`[도표, Fig. 2b]` 우축 **+0.2 ~ −0.4 MPa**, x축 **0–210 h, 약 14 사이클**. 압력은 초기
**0 → −0.12 MPa** 로 떨어진 뒤 평평해진다 (50 h 이후 −0.10 ~ −0.13 MPa 사이에서 진동).

★ `[해석]` **"LPSCl 은 안 움직인다" 는 문자 그대로는 참이 아니다** (G11). 이 대조셀도
**−0.12 MPa** 의 영구 압력 강하를 보인다 — 이것은 Fig. 3d(Li2S, −0.6 MPa)의 **20 %**, Fig. 4b
(Li_xIn, −1.4 MPa)의 **9 %** 다. 즉 **§5–§7 의 성분 분해에는 −0.12 MPa / −2 µm 의 바닥 잡음이
깔려 있다.** 저자는 이 잔차를 빼지 않았다. 다만 이 잔차가 LPSCl 자체의 상변화인지, **LTO 전극
매트릭스의 입자 재배열**인지도 구분하지 않았다 — 후자일 가능성이 더 높다 `[해석]`, 왜냐하면
LTO 필름도 60 wt% LTO + 30 wt% LPSCl 의 **복합 전극**이고 이 논문의 주장대로라면 어떤 복합
전극이든 첫 사이클에 재배열로 수축하기 때문이다.

---

## 5. p.3–4 — 결과 ② S 양극 vs Li2S 양극 (Fig. 3) ★ 이 논문의 본체

`[인쇄, Fig. 3 캡션]` "Comparison of displacements (a) and pressure changes (b) of a
**S|LIPSCl|LTO (prelithiated)** cell; displacements (c) and pressure changes (d) of a
**Li2S|LIPSCl|LTO** ASSLB. The cells were cycled at **C/10** rate." (본문 §2.4 는 0.05 C — G5)

`[인쇄]` Li2S 를 쓰는 이유 3가지:
1. Li2S 는 황의 **완전 리튬화 상**이자 방전 최종 생성물[8].
2. **비금속 Li 음극(예: Si)** 을 쓸 수 있어 **덴드라이트를 피하면서 에너지밀도 손실이 적다**
   — "the theoretical capacity of Li2S is **1166 MAh g⁻¹**" (대문자 MAh 는 원문 오기).
   `[재현]` 1166 mAh g⁻¹**(Li2S)** = 1166 ÷ 0.698 = **1670 mAh g⁻¹(S)** (이론 1672 와 일치).
3. **열안정성**: Li2S 융점 **938 °C** vs S **113 °C**.

★ `[해석]` 2번은 **우리 [[anode-free-li2s-assb]] 의 논거와 정확히 같다** — Li 원천이 양극에
있으니 Li-free 음극이 가능하다. 단 이 논문은 그 방향으로 가지 않고 **Li–In 과 LTO 만** 쓴다.

### 5.1 본문이 말하는 것 `[인쇄, §3]`

- 두 ASSLB 모두 **첫 몇 사이클에서 전체 부피가 감소**하다가 수축률이 느려지고 안정화.
- **Li2S 양극 셀의 부피 감소가 더 크다** — "the difference is considerable, not small".
- **"Approximately, 15–20 % of total shrinkages (14–20 μm shrinkage out of 100 μm.) occurred
  with most of it happening in the initial cycles."** (분모 100 µm 불명 — G6)
- 안정화 후 **변위 진동 진폭 ≈ 1 µm**.
- 압력도 같은 추세. **Li2S 쪽 압력 강하가 더 크다.** 안정화 후 **압력 진동 ≈ 0.15 MPa**.
- 압력은 계속 떨어지지만 변위보다 덜 뚜렷 → **"the pressure transducer is less sensitive than
  the displacement sensor"**.
- **가장 큰 부피 변화는 첫 사이클**. 이는 기계적 파손에 의한 열화가 초기 사이클에 집중된다는
  선행 보고[6]와 일치.
- **초기 방전(환원)과 충전(산화)의 부피 변화가 비대칭**이고, 이 비대칭은 첫 몇 사이클 안에
  사라져 대칭이 된다.

### 5.2 저자의 2인자 가설 `[인쇄, §3]`

부피 변화 = **(i) 전기화학 반응에 의한 1차 입자의 부피 변화** + **(ii) 공극률 변화로 인한 1차
입자의 이동(재배열)**.

- (i) 은 **진동(oscillation)** 이다 — LTO 를 뺀 거의 모든 활물질의 고유 성질.
- (ii) 는 **단방향(부피 감소)** 이다 — 입자가 수축하며 생긴 공극으로 **작은 입자가 흘러든다**.
  주로 **첫 사이클**에 일어나고, 끝나면 남는 것은 (i) 의 진동뿐.
- **S 양극 (Fig. 3a,c)**: 방전(환원) 시 팽창 → 양(+)의 변위·압력 상승. 그런데 **첫 방전의 증가분이
  뒤이은 충전의 감소분보다 뚜렷이 작다.** 이유: 방전 중에는 (i) 팽창과 (ii) 수축이 **상쇄**되고,
  충전 중에는 (i) 수축과 (ii) 수축이 **합쳐지기** 때문.
- **Li2S 양극 (Fig. 3c,d)**: Li2S 는 **충전(산화)부터** 시작하므로 첫 단계의 감소폭이
  **훨씬 크다** — S 양극의 감소보다도, 뒤이은 방전의 증가보다도.
- ★ `[인쇄]` 선행 보고[9]는 완전리튬화 Li2S 구조의 부피 변화가 **무시할 만하다**고 했으나
  **"our observation does not seem to align with this"**. 근거: **Li2S 의 부분 몰부피
  2.768 × 10⁻⁵ m³ mol⁻¹ 은 원소 황의 약 2배**[10] → Li2S 의 탈리튬화(충전)에서 큰 부피 감소.

★ `[재현]` **몰부피를 직접 계산해 확인한다** (ρ(Li2S) ≈ 1.66, ρ(S8, α) ≈ 2.07 g cm⁻³):

| 물질 | M (g mol⁻¹) | ρ (g cm⁻³) | V_m (cm³ mol⁻¹) | V_m (m³ mol⁻¹) |
|---|---|---|---|---|
| Li2S | 45.95 | 1.66 | **27.68** | **2.768 × 10⁻⁵** |
| S (원자 기준, α-S8) | 32.06 | 2.07 | **15.49** | 1.549 × 10⁻⁵ |

- **논문이 인용한 2.768 × 10⁻⁵ m³ mol⁻¹ 은 ρ = 1.66 g cm⁻³ 의 Li2S 몰부피와 정확히 일치한다.**
- `[재현]` 비 = 27.68 / 15.49 = **1.79** — "twice" 는 **1.79배의 반올림**이다 (2.0 이 아니다).
- `[재현]` **S → Li2S 방전 팽창 = +78.7 %**, **Li2S → S 충전 수축 = −44.0 %**
  (= 1 − 15.49/27.68).
- `[해석]` 즉 **황 1 mol 기준으로 방전은 +79 %, 충전은 −44 %** 다. 같은 양의 물질이 왕복하는데
  퍼센트가 다른 것은 분모가 다르기 때문이며, **절대 부피 변화량(12.19 cm³ mol⁻¹)은 같다.**
  양극에 활물질이 33.3 wt% 뿐이고 SE·탄소가 66.7 wt% 이므로 **전극 수준 변화는 이보다 훨씬 작다**
  — 그러나 로딩이 없어(G2) 그 환산을 할 수 없다.

### 5.3 그림에서 읽은 값 `[도표]`

| 패널 | 셀 | 축 범위 | 시작 → 끝 | 사이클 수 |
|---|---|---|---|---|
| **Fig. 3a** | S∣LPSCl∣LTO(전리튬화), 변위 | 전압 −1.5 ~ +2 V · 변위 +2 ~ −18 µm · 0–270 h | **+2 → −13 µm** (Δ ≈ **15 µm**) | ≈14 |
| **Fig. 3b** | 같은 계, 압력 | 압력 +0.2 ~ −0.4 MPa · 0–270 h | **+0.13 → −0.28 MPa** (Δ ≈ **0.41 MPa**), 100 h 부근 일시적 **−0.38 MPa** 급강하 후 회복 | ≈13 |
| **Fig. 3c** | **Li2S∣LPSCl∣LTO**, 변위 | 전압 −1.5 ~ +2.5 V · 변위 0 ~ −28 µm · 0–160 h | **0 → −18/−19 µm** (Δ ≈ **19 µm**) | ≈14 |
| **Fig. 3d** | 같은 계, 압력 | 압력 +0.1 ~ −0.8 MPa · 0–220 h | **0 → −0.60 MPa** | ≈14 |

★★ `[도표, Fig. 3c]` **이 논문에서 우리에게 가장 중요한 한 장면**: Li2S 셀의 **첫 충전**
(전압이 **0.85 → 2.4 V 로 단조 상승**하는 처음 **≈11 h**) 동안 변위가 **0 → 약 −10 µm** 로
떨어진다. 그 뒤 150 h 동안 추가로 −8~9 µm 만 더 내려간다.
`[재현]` **총 수축 19 µm 중 절반 이상(≈53 %)이 첫 충전 한 번에 일어난다.**

`[해석]` 이것이 **Li2S 활성화의 기계적 얼굴**이다 — [[li2s-activation-first-charge]] 는 지금까지
전기화학(과전압·용량)으로만 기술돼 있는데, 이 논문은 같은 사건이 **셀 두께 −10 µm** 로도
보인다는 것을 보여준다. 첫 충전 컷오프 **2.4 V**(기준: LTO 대극, G4) 도 그림에서만 읽힌다.

`[도표, Fig. 3c]` 첫 충전 이후 전압창은 **약 −0.9 ~ +1.6 V** (vs LTO 대극) 로 좁혀진다.
`[도표, Fig. 3a]` S 셀은 **−1.0 ~ +1.6 V** (vs 전리튬화 LTO).
`[도표, Fig. 3a,c]` 파란 **보조선 두 개**가 안정화 구간(a: 140–260 h, c: 110–160 h)의 진동
포락선을 표시한다 — 포락선 폭 **≈3 µm**(c), 기울기는 여전히 하향. 본문의 "진폭 ≈1 µm" 은
이 포락선 안쪽의 사이클당 진동을 말한다.

★ `[해석]` **본문과 그림의 어긋남 하나**: 본문은 "**Li2S 쪽 수축이 S 쪽보다 훨씬 크다**
(considerable, not small)" 고 쓰지만, 그림에서 읽으면 **15 µm vs 19 µm** — **27 % 차이**다.
큰 차이이긴 하나 "considerable, not small" 이라는 강조에 비하면 온건하다. 게다가 두 셀은
**사이클 시간 축이 다르고**(270 h vs 160 h) **변위 축 눈금도 다르다**(−18 vs −28 µm 만재).
**같은 축에 겹쳐 그린 그림이 없다** — 이 논문의 핵심 비교인데도.

---

## 6. p.4–5 — 결과 ③ Li_xIn 음극 (Fig. 4)

`[인쇄, Fig. 4 캡션]` "The displacement (a) and pressure changes (b) of an **LTO|LPSCl∣Li_xIn**
cell during cycling at **C/20** rate."

`[인쇄, §3]` 셀 배치 주의 — Fig. 3 에서는 LTO 가 **음극**이었지만 Fig. 4 에서는 **LTO 가 양극,
Li_xIn 이 음극**이다. 그래서 "충전/방전" 이 아니라 **산화/환원**으로 불러야 한다. (Fig. 3a 에서
전리튬화 LTO 는 방전 중 **산화**되지만, Fig. 4 에서 LTO 는 방전 중 **환원**된다.)

`[인쇄]` Li_xIn 형성의 기전:
- In 이 **정방정(tetragonal) → 입방정(cubic) Li_xIn** 으로 상전이.
- 이 상전이를 수용하려면 **단위포가 z 방향보다 x–y 면내에서 더 많이 팽창**한다 (이방성).
- 이 이방성 팽창이 **단위포 수준에서 약 100 % 부피 변화**를 만든다.
- 추가로 저자는 **합금화 중 불균일(inhomogeneity)** 을 의심한다 — Li 가 In 전극 전체에
  재분배되는 과정이 사이클 내내 일어날 것이다.
- 면내 비대칭 팽창 + Li 재분배 → **상당한 입자 재배열** → **안정화 전까지 큰 부피 감소**.

`[도표, Fig. 4a]` 전압 **0.8 – 1.6 V** (vs Li–In), 변위 축 **0 ~ −50 µm**, x축 **0–180 h,
≈14 사이클**. 변위는 **0 → 약 −42 µm**. 처음 **60 h(≈5 사이클)에 −35 µm** 가 일어나고 그 뒤는
완만. 데이터가 **점(dot)** 으로 찍혀 있어 Fig. 2·3 의 연속선과 다르다.

`[도표, Fig. 4b]` 압력 축 **0 ~ −1.8 MPa**, x축 **0–210 h, ≈15 사이클**. 압력은
**0 → 약 −1.4 MPa**. 역시 처음 60 h 에 −1.2 MPa 가 집중.

★★ `[해석]` **세 성분 중 Li_xIn 이 압도적으로 크다.**

| 성분 (해당 셀) | 총 변위 `[도표]` | 총 압력 강하 `[도표]` |
|---|---|---|
| LPSCl / LTO 매트릭스 (LTO∣LPSCl∣LTO) | **−2 µm** | **−0.12 MPa** |
| S 양극 (S∣LPSCl∣LTO) | **−15 µm** | **−0.41 MPa** |
| **Li2S 양극** (Li2S∣LPSCl∣LTO) | **−19 µm** | **−0.60 MPa** |
| **Li_xIn 음극** (LTO∣LPSCl∣Li_xIn) | **−42 µm** | **−1.4 MPa** |

`[해석]` 즉 **Li–In 음극이 Li2S 양극보다 2.2배 더 수축한다.** 이 위키의 [[li2s-assb-reference-cell]]
은 1단계에서 **Li–In 을 쓴다** — 그렇다면 **우리 셀에서 첫 사이클 압력 강하의 주범은 양극이
아니라 음극**일 가능성이 크다. 그리고 [[anode-free-li2s-assb]] 로 가면 이 −42 µm 항이 사라지고
**Li 석출/용해의 부피 항**으로 대체된다. 그 교체가 이득인지 손해인지 이 논문은 답하지 않는다
(Li 대칭셀은 Video 1S 로만 언급 — SI 미확보 G18).

`[인쇄, §3]` 중요한 단서: "it's essential to understand that **Li_xIn was never intended to serve
as an anode material in commercial ASSLBs**. Researchers used Li_xIn in an ASSLB cell primarily
due to the instability of the Li/SSE interface."

`[인쇄, §3, Video 1S]` **Li∣SSE∣Li 대칭셀**은 **상보적(reciprocal)** 거동을 보였다 — 한쪽 Li
전극의 부피 증가가 반대쪽의 감소를 상쇄해 **셀 전체의 부피 변화가 무시할 만했다**. 따라서
양극·음극의 부피 변화는 **협조적으로(in a coordinated manner)** 다뤄야 하고, **동기화하면 셀
전체 응력이 줄고**, 어긋나면 SSE 와 계면에 균열·공극이 생긴다. (영상 미확보 — G18)

★ `[해석]` **이것이 이 논문이 주는 설계 원리 중 가장 이식 가능한 것이다**: "양극이 팽창할 때
음극이 수축하도록 짝지어라." Li–S 계는 방전에서 양극이 팽창(+79 %)하고 Li 음극이 소모(수축)되므로
**원리적으로 상보적**이다. Li–In 은 그 상보성을 깬다 — 합금 음극은 방전에서 **탈리튬화되어
수축**하지만 재배열 수축이 그보다 크게 겹친다.

---

## 7. p.5 — 결과 ④ 성분 분해 (Fig. 5) ★ 제목의 "Deciphering" 이 있는 자리

`[인쇄, Fig. 5 캡션]` "Comparison of the displacements of **sulfur cathode (in S8∣LiPSCl∣LTO)**,
**Li_xIn anode (in LTO∣LiPSCl∣Li_xIn)** and **S8∣LiPSCl∣Li_xIn full ASSLB** during the
**1st discharge (a)** and **recharge (b)**, and **2nd discharge (c)** and **recharge (d)**."

### 7.1 저자가 미리 밝힌 한계 `[인쇄, §3]` ★

> "It is important to note that achieving exact reproducibility of the prelithiation for LTO and
> Li_xIn was challenging, and the results presented were based on the data from **three different
> cells**. To facilitate comparison, **all results were normalized to 100 %**, making the
> comparison **more qualitative than quantitative**. For example, **adding the red and blue lines
> might not exactly result in the black curve**, but the trends indicated by the red and blue
> lines combine to produce the black line."

`[해석]` **논문 제목의 동사("Deciphering")가 이 문단 위에 서 있다.** 세 개의 다른 셀에서 잰
곡선을 각각 100 % 로 정규화해 겹친 것이므로, **"양극 몫 3 µm, 음극 몫 11 µm" 같은 수치는 서로
다른 셀의 수치**다. 이 논문의 정량성은 여기서 끝난다 (G7, G9).

### 7.2 본문이 적은 값 `[인쇄, §3]`

**1차 방전** (S 환원):
- 양극 부피 **약 +3 µm 증가**
- Li_xIn 음극 **약 −11 µm 감소**
- 전체 셀 **약 −6 "mm" 감소** ← **단위 오기, µm 여야 함 (G8)**
- `[재현]` +3 + (−11) = **−8 µm** ≠ −6 µm. 차이 **2 µm (25 %)** (G9)

**1차 충전** (S 산화):
- 양극 **약 −4 µm 소폭 감소**
- Li_xIn 음극 **거의 변화 없음** — Li 합금화에 의한 증가가 재배열에 의한 감소로 **상쇄**
- 전체 셀 **거의 변화 없음**

**2차 사이클**: 같은 추세, **변화폭은 더 작다**.

### 7.3 그림에서 읽은 값 `[도표, Fig. 5]`

x축은 **"Properation / %"** (= proportion 의 오기), 0–100 % 로 정규화된 반응 진행도.
**패널마다 변위 축 범위가 다르다** (a: +9~−12 · b: +10~−12 · c: 0~−20 · d: +10~−20 µm) —
**패널 간 절대 비교 금지**.

| 패널 | 빨강 = S 양극 | 파랑 = Li_xIn 음극 | 검정 = full cell |
|---|---|---|---|
| (a) 1차 방전 | 0 → **+3 µm** | 0 → **−11 µm** | 0 → **−6 µm** |
| (b) 1차 충전 | +2 → **−2 µm** (Δ ≈ −4) | −11.5 → −12 (Δ ≈ **−0.5**) | −5.8 → −6.5 (Δ ≈ **−0.7**) |
| (c) 2차 방전 | −1 → 0 (Δ ≈ **+1**) | −13 → −19.5 (Δ ≈ **−6.5**) | −6.5 → −9.5 (Δ ≈ **−3**) |
| (d) 2차 충전 | 0 → **−2 µm** | ≈ −20 (평탄) | ≈ −10 (평탄) |

★ `[해석]` **2차 방전에서도 음극이 −6.5 µm 나 더 줄어든다** (c). 본문은 "2차 사이클은 변화가
더 작다" 고 쓰지만 음극만 보면 1차(−11)와 같은 자릿수다. **Li–In 의 재배열은 2사이클로 끝나지
않는다** — Fig. 4a 가 60 h(≈5 사이클)까지 −35 µm 로 계속 내려간 것과 일치한다.

`[도표, Fig. 5 상단 반응식]` 각 패널 상단에 전압 분해식이 인쇄돼 있다:
- (a),(c) 방전: 빨강 `S8 + Li_x−LTO → Li2S + LTO` (V1) · 파랑 `Li_xIn + LTO → Li_x−LTO + In` (V2)
  · 검정 `S8 + Li_xIn → Li2S + In` (V = V1 + V2)
- (b),(d) 충전: 빨강 `Li2S + LTO → S8 + Li_x−LTO` (V1) · 파랑 `Li_x−LTO + In → Li_xIn + LTO` (V2)
  · 검정 `Li2S + In → S8 + Li_xIn`

`[도표]` (a) 와 (c) 에는 **회색 곡선이 하나 더** 있다 (검정 full-cell 전압 위쪽, ~1.5 → 0.3 V).
캡션·본문 어디에도 설명이 없다. `[해석]` V1+V2 의 계산값으로 보이나 **확인 불가** — 범례가 없다.

`[도표]` 전압 축: (a) 1차 방전 full cell 은 **≈1.35 → 0.15 V** (vs Li–In), (b) 1차 충전은
**≈1.25 → 2.40 V** (vs Li–In). 즉 **S∣LPSCl∣Li–In full cell 의 전압창은 ≈0.15–2.4 V vs Li–In**
`[도표]` 이고, 이것이 Fig. 1b,d 의 전압 범위(0.6–2.4 V)와 대체로 맞는다.

---

## 8. p.5–6 — 기전 가설과 압력 권고 (Fig. 6)

### 8.1 부피 변화가 SSE 셀에 남기는 것 `[인쇄, §3]`

- 무작위 배향 입자가 **이방성 부피 변화** → 양극 내 **미세균열(microcracks)**.
- 큰 부피 변화 → **새 기공·공극** → **활물질–SE–탄소 삼상 계면 파괴** → 미세구조 실패.
- 실시간으로 막지 못하면 **활물질/SSE 계면 불안정의 주원인**.
- **전극–전해질 박리(delamination)** 로 양극/SE 접촉의 기계적 손상.
- 공극에 의한 접촉 부족 → **계면 저항 증가, 전하이동 방해**, SSE 구조 건전성 저하 → 이온 확산
  방해 → **불균일 증가 → 불균일 분극 → Li 덴드라이트 가능성**.

### 8.2 압력 권고 수치 `[인쇄, §3]` ★

| 문장 | 값 |
|---|---|
| SSE 고밀도·저공극·큰 결정립을 위한 **성형 압력** | **"such as 370 MPa"**[11] |
| ASSLB **장기 사이클에 필요한 운전 스택 압력** | **"approximately 7 MPa"** |
| 정용적으로 돌릴 때 **셀 부피 감소** | **"could decrease by 10 %"** |
| 정용적으로 돌릴 때 **스택 압력 강하** | **"could drop by nearly 1 MPa"** |

★ `[재현]` **"10 % 감소"·"1 MPa 강하" 를 이 논문의 자기 데이터로 검산한다.**
- 부피 10 %: `[도표]` Li2S 셀 −19 µm. Fig. 7d 의 사이클 전 **양극 80.5 + SE 83.2 = 163.7 µm**
  → **−11.6 %**. **맞는다** (분모를 양극+SE 로 잡았을 때).
- 압력 1 MPa: `[도표]` Li_xIn 셀 −1.4 MPa, Li2S 양극 셀 −0.6 MPa, S 양극 셀 −0.41 MPa.
  **음극을 포함한 full cell 기준으로 ≈1 MPa 은 타당**하다.
- `[해석]` 따라서 **G6 의 "100 µm" 은 오기이고 실제 분모는 ≈164 µm 로 보인다** — 다만 그렇게
  읽으면 "15–20 %" 가 아니라 **8.6–12.2 %** 가 되어 본문의 두 수치가 서로 맞지 않는다.
  ★ **이 논문에서 인용할 안전한 값은 "정용적 운전 시 스택 압력이 7 → 6 MPa 로 약 1 MPa 떨어진다"
  하나다.**

### 8.3 Fig. 6 만화 — 가설의 그림 `[도표]`

`[인쇄, Fig. 6 캡션]` "Illustration showing the hypothesized morphology changes in an ASSLB
during cycling under constant pressure and constant volume conditions."

`[도표, Fig. 6]` 2행 × 3열. 각 칸은 **위: 복합양극(파란 큰 구 = SE, 노란 구 = 활물질, 검은 점 =
탄소) / 중간: SSE 층 / 아래: Anode(회색)**. 좌 → 우로 **초기 → Discharge → Charge**.

- **1행 정압(Constant Pressure)**: 방전 후 노란 활물질 입자가 **커지고 내부에 균열선**이 생긴다.
  충전 후 입자가 **작아지고 균열은 남지만**, 전극 상단 경계가 **아래로 내려온다**(빨간 "Displacement"
  화살표로 표시) — **압력이 전극 전체를 눌러 입자 재배열로 공극을 메운다**. 매트릭스에 흰 공백이
  거의 없다.
- **2행 정용적(Constant Volume)**: 방전은 같지만, **충전 후 입자 주위에 노란 점선 테두리와 흰
  공극**이 뚜렷하게 남는다. 전극 상단 높이는 그대로다. → **공극이 갇힌다**.

`[인쇄, §3]` 저자의 해설:
- 방전(환원) 시 황 입자가 크게 팽창 → **정압 구속이 없으면 미세균열이 더 잘 생긴다**.
- 충전(산화) 시 황 양극이 수축 → **정용적에서는 그 수축이 공극이 된다**.
- 스택 압력을 걸면 고체 양극이 눌려 **입자 재배열 → 공극 감소 → 삼상 계면 보존**.
- ★ "**it is the stack pressure, rather than the capillary effect, that drives the movement of the
  solid-state electrolyte**" (액체 전해질의 모세관 젖음과 대비).
- 결론 명제: **"while void formation can be mitigated by the external stack pressure, the cracking
  is permanent."**

`[해석]` Fig. 6 은 **가설의 그림이지 데이터가 아니다.** 논문도 "hypothesized" 라고 쓴다. 균열이
정압에서 "덜" 생긴다는 부분(1행 vs 2행의 균열선 개수)은 **SEM 으로 뒷받침되지 않았다** — Fig. 7
상단행은 균열이 아니라 **결정 크기**를 비교한다. 즉 **"압력이 균열을 줄인다" 는 그림에만 있다.**
논문 본문 §3 후반에도 "The fracturing **worsened under unconstrained conditions**" 라고 쓰지만
그 근거는 EIS 의 비가역성(회복 안 됨)이지 균열의 직접 관측이 아니다.

---

## 9. p.6–7 — 사후 단면 SEM (Fig. 7) ★ 유일한 정량 구조 데이터

`[인쇄, Fig. 7 캡션]` "Cross-section SEM images show (a) the sulfur cathode **before cycle**,
(b) after cycling under **7 MPa constant pressure** cycling, (c) after cycling under **constant
volume with an initial pressure of 7 MPa**, (d) the S|SSE interface before cycle, (e) after
constant pressure cycling and (f) after constant volume cycling."

`[인쇄, §3]` 시료: **갓 조립한 셀**과 **10 사이클 후 셀**.

### 9.1 두께 (그림 주석의 숫자 — 이 논문 유일의 구조 정량값) `[인쇄, Fig. 7d–f 주석]`

| 조건 | 양극 두께 | SSE 두께 | `[재현]` 양극 변화 | `[재현]` SSE 변화 | `[재현]` 합 |
|---|---|---|---|---|---|
| **사이클 전** (d) | **~80.5 µm** | **~83.2 µm** | — | — | 163.7 µm |
| **정압 7 MPa, 10 cyc** (e) | **~72.9 µm** | **~72.9 µm** | **−9.4 %** | **−12.4 %** | 145.8 µm (**−10.9 %**) |
| **정용적(초기 7 MPa), 10 cyc** (f) | **~88.1 µm** | **~74.1 µm** | **+9.4 %** | **−10.9 %** | 162.2 µm (**−0.9 %**) |

★★ `[재현]` **이 표가 이 논문에서 가장 깨끗한 결과다** — 그리고 논문은 이 계산을 하지 않았다.
- **정압**: 양극+SE 합계가 **−17.9 µm (−10.9 %)** 줄었다. → LVDT 로 잰 **−14~20 µm** 와 **일치**.
  두 독립 측정(LVDT, 단면 SEM)이 같은 값을 준다.
- **정용적**: 양극+SE 합계는 **−1.5 µm (−0.9 %)** — 거의 변하지 않았다. **당연하다. fixture 가
  높이를 고정했으니까.** 대신 **내부에서 재분배**가 일어났다: **SE 가 −9.1 µm 얇아진 만큼
  양극이 +7.6 µm 두꺼워졌다.**
- `[해석]` **즉 정용적 셀에서는 "양극이 SE 를 밀어내며 부푼다".** 양극은 공극 때문에 부피가
  늘고, 그 팽창이 갈 곳이 없어 **SE 층을 압축해 버린다.** 이것이 본문이 말한 "SSE 가 훨씬
  비정질스러워졌다" 의 기계적 원인일 것이다 `[해석]`.
- 본문은 이 재분배를 "the cathode's thickness increased **slightly** while the SSE's thickness
  **slightly** decreased" 라는 한 줄로 흘려보낸다 (G12). **9–11 % 는 slightly 가 아니다.**

### 9.2 형태 `[인쇄, §3]` + `[도표, Fig. 7a–c]`

`[인쇄]` 정압: SSE·양극 모두 **약 10 % 얇아지고 더 치밀·저공극**. SSE 형태는 사이클 전과
**유사하게 유지**.
`[인쇄]` 정용적: 양극 두께는 **약간 증가**, SSE 두께는 **약간 감소**. 가장 두드러진 관측은
**"the SSE became a lot more amorphous under constant volume cycling"**.

`[도표, Fig. 7a–c]` (×8.00k, 스케일바 5.00 µm, 3.0 kV):
- (a) **사이클 전**: 거칠고 불규칙한 파쇄면. 뚜렷한 결정면 없음. 미세한 요철 다수.
- (b) **정압 후**: **크고 매끈한 판/막대 결정** — 길이 **≈5–10 µm**, 면이 평평하고 모서리가 뚜렷.
  배경 기공은 적다.
- (c) **정용적 후**: **작고 짧은 막대 결정 다수** — 길이 **≈1–2 µm**, 결정 사이에 **어두운 공극이
  촘촘히** 보인다. (a) 보다도 공극이 많아 보인다.

`[인쇄, §3]` 저자의 해석: 크고 매끈한 황 결정은 **끊기지 않은 삼상 계면**의 결과다. 연속된
전하이동 네트워크가 **Li2S 의 산화를 뒷받침**하므로 결정이 크게 자란다. 공극이 생겨 계면이
끊기면 **작은 황 결정**이 된다. 정용적 후 공극률 증가(c)와 정압 후 공극률 감소(b)가 Fig. 6 의
가설과 **일치**.

★ `[해석]` **이 해석은 매력적이지만 원소 증거가 없다** (G15). ×8k 이미지 3장에서 "결정 크기" 를
눈으로 비교했을 뿐, **EDS 도 XRD 도 라만도 없다.** 황화물 SE(LPSCl)의 결정 입자와 S8 결정은
2차전자 상에서 구별되지 않는다. 또 (a) 와 (b),(c) 는 **서로 다른 파단면**이므로 파단 방식의
차이가 형태를 만들었을 수도 있다.

`[도표, Fig. 7d–f]` (×700, 스케일바 50.0 µm): 노란 점선이 **양극/SSE 경계**, 빨간 막대가 두께
측정선. (f) 정용적 시료는 (d),(e) 보다 **경계가 울퉁불퉁**하고 상부(SSE)에 **큰 어두운 공동**이
보인다 — 다만 이 공동이 시료 준비(파단) 인공물인지 구분할 수 없다 `[해석]`.

---

## 10. p.7–8 — 전기화학 검증: 사이클·EIS·DRT (Fig. 8)

`[인쇄, Fig. 8 캡션]` "(a) Comparison of the cyclability of ASSLB cells cycled under **constant
pressure of 7 MPa** versus that cycled at a **constant volume with an initial pressure of 7 MPa**.
(b) AC impedance comparison after **0, 3 and 10 cycles** under constant pressure and constant
volume conditions, with the inset showing an enlarged view of the high-frequency region.
(c) Comparison of the **DRT** derived from the impedance spectra in (b). After 10 cycles of
constant volume conditions, the ASSLB cell was **recompressed to 7 MPa**."

★ **셀의 화학은 캡션에도 본문에도 없다** (G3).

### 10.1 사이클 (Fig. 8a)

`[인쇄, §3]`
- 정압 셀은 **"maintained it capacity well throughout the 100 cycles"**.
- 정용적 셀은 **3번째 사이클부터 감소 시작**, 계속 하락.
- **10번째 사이클 후 7 MPa 로 재압축** → 용량이 **부분 회복**, 정압 셀에 근접.
  그러나 **곧 다시 감소**.
- **20 사이클 후 재압축** → **약간만** 개선, 이후 **급격히** 하락.
- 이후 **10 사이클마다 재압축** → **최소한의 회복만**.
- 정압 셀은 계속 용량을 잘 유지.

`[도표, Fig. 8a]` y축 좌 = **Capacity retention / %** (0–140), y축 우 = **Coulombic Efficiency / %**
(0–120), x축 **Cycle Number 3–100**. 그림 주석: **"Repressed to 7 MPa after 10, 20, 30, 40, 50
and 60 cycles"** (화살표 6개).

| 곡선 | 사이클 3 | 사이클 100 |
|---|---|---|
| **정압 7 MPa** 유지율 (검정) | 100 % | **≈63 %** |
| **정용적** 유지율 (빨강) | 100 % | **≈50 %** |
| **CE** (검정·빨강 모두) | ≈100 % | **≈100 %** (양쪽 모두, 산발적 이상점 제외) |

★★ `[해석]` **G20 의 자리.** 그림이 실제로 말하는 것은:
1. **정압 셀도 100 사이클에 37 % 를 잃는다.** "maintained well" 은 **상대 진술**이다.
2. 두 조건의 차이는 **63 vs 50 %, 13 포인트**다 — 실재하지만 극적이지 않다.
3. **CE 는 양쪽 다 ≈100 %** 다. 즉 **"안정" 을 CE 로 말하면 두 셀이 똑같이 안정**하다.
   이 위키의 규율대로 **"안정" 이 CE 인지 용량인지 갈라야 한다** — 여기서는 **용량**이다.
4. **재압축의 회복은 실재한다** — 10사이클 후 빨강이 **≈63 → 72 %** 로 튀어오르고(그림에서
   화살표가 가리키는 첫 회복), 이후 회복폭이 점점 작아져 50 사이클 이후에는 거의 없다.
   ★ 이것이 논문의 핵심 주장("공극은 압력으로 되살릴 수 있으나 균열은 아니다")의 **가장 강한
   증거**다.
5. `[도표]` 정용적 곡선은 **60 사이클 부근에서 ≈50 % 로 주저앉은 뒤 평탄**해진다. 재압축을
   60 사이클까지만 한 것도 그 때문으로 보인다 `[해석]`.

### 10.2 임피던스 (Fig. 8b)

`[인쇄, §3]`
- 정압 7 MPa 셀의 **Ohmic 저항은 첫 10 사이클 동안 안정**.
- 정용적 셀의 **Ohmic 저항은 거의 50 % 증가**.
- ★ **"the Ohmic resistance increases – rather than decreases as conventional wisdom might
  suggest - when the cell is recompressed to 7 MPa after cycling for 10 cycles under constant
  volume condition."**

`[도표, Fig. 8b]` 주 그림: 6개 곡선이 모두 **거의 직선(≈45°)** — 저주파에서 확산/블로킹 거동.
실축 0–500 Ω. **반원이 사실상 보이지 않는다** (60 °C 에서 만든 셀을 상온에서 쟀는데도).
인셋(실축 25–100 Ω, 허축 0 ~ −50 Ω) 의 고주파 절편 `[도표]`:

| 곡선 | Ohmic 절편 `[도표]` |
|---|---|
| Before cycle (검정) | **≈38–40 Ω** |
| CP-after 3rd (빨강) | **≈40 Ω** |
| CP-after 10th (파랑) | **≈40 Ω** |
| CV-after 3rd (초록) | **≈45 Ω** |
| CV-after 10th (자홍) | **≈55 Ω** |
| **CV-after 10th, back 7 MPa** (갈색) | **≈62–65 Ω** ← **가장 높다** |

`[재현]` 40 → 58–60 Ω 이면 **+45–50 %** — 본문의 "nearly 50 %" 와 맞는다.
인셋에는 **빨간 원(정압 7 MPa 무리)** 과 **파란 화살표 "Increase with cycling"** 이 인쇄돼 있다.

★ `[해석]` **재압축이 Ohmic 저항을 더 올린다는 것이 이 논문에서 가장 반직관적인 관측**이고,
저자의 설명(균열이 이미 났고 7 MPa 로는 못 붙인다)은 그럴듯하지만 **대안 설명을 배제하지
않았다**: 재압축 자체가 이미 균열된 입자를 **더 부수거나** 접촉을 국소적으로 끊었을 수 있다.
같은 데이터가 **"재압축은 해롭다"** 로도 읽힌다 — 그런데 Fig. 8a 에서는 재압축이 **용량을
올린다**. 즉 **Ohmic 은 나빠지고 용량은 좋아진다.** 논문은 이 모순을 다루지 않는다.

### 10.3 DRT (Fig. 8c)

`[인쇄, §3]`
- 주 피크(**시간상수 0.1–1 s**)가 셀 동역학·저항의 병목.
- 정압 셀은 **3사이클 후 시간상수 불변**, 전하이동 저항만 **소폭 증가**.
- 정용적 셀은 **시간상수와 저항이 모두 증가**.
- 갓 조립한 셀의 **작은 어깨 피크**가 정압 3사이클 후에는 **유지**되지만 정용적에서는 **사라진다**.
- 10사이클 후에는 두 조건의 **시간상수가 비슷**해지지만, 정용적 셀의 **저항이 뚜렷이 높다**.
- 재압축 후에도 동역학·저항에 **큰 변화 없음**, **저항만 약간 더 증가**.

`[도표, Fig. 8c]` y = G(τ) / Ω s⁻¹ (0–600), x = τ / s (10⁻³–10). 주 피크와 중간 피크를 읽으면:

| 곡선 | 주 피크 위치 τ | 주 피크 높이 G | τ≈0.02–0.03 s 피크 | τ≈1 s 어깨 |
|---|---|---|---|---|
| Before cycle (검정) | **≈0.27 s** | **≈305** | ≈50 | **있음 (≈105)** |
| CP-after 3rd (초록) | **≈0.30 s** | **≈348** | ≈75 | **있음 (≈110)** |
| CV-after 3rd (빨강) | **≈0.45 s** | **≈310** | ≈65 | **없음** |
| CP-after 10th (파랑) | **≈0.45 s** | **≈372** | ≈70 | 없음 |
| CV-after 10th (자홍) | **≈0.45 s** | **≈525** | ≈105 | 없음 |
| **CV-after 10th, back 7 MPa** (갈색) | **≈0.45 s** | **≈570** | ≈112 | 없음 |

★ `[해석]` **그림은 본문 주장을 대체로 뒷받침하지만 한 군데가 어긋난다**:
- **τ≈1 s 어깨의 존재/소멸은 정확히 맞는다** — 검정·초록에는 있고 빨강에는 없다. 이 관측은
  이 논문에서 가장 미세하고 가장 설득력 있는 증거다.
- **CV-10th(525) ≫ CP-10th(372)** 도 맞는다. **재압축 후 570 으로 더 오른다** 도 맞는다
  (Fig. 8b 와 같은 방향).
- **어긋나는 것**: "정용적은 3사이클 후 저항이 증가" 라는데 **빨강(310)은 검정(305)과 거의
  같고 초록(348)보다 낮다.** 시간상수는 확실히 오른쪽(0.27 → 0.45 s)으로 갔지만, **피크 높이로는
  정압 쪽이 더 높다.** 저항은 G(τ) 의 **면적**이고 빨강이 더 넓으므로 면적으로는 뒤집힐 수
  있으나, **논문은 면적을 계산해 보이지 않았다.**
- DRT 의 **정규화 파라미터(λ)·알고리즘이 미기재**여서 피크 높이 비교의 신뢰구간을 알 수 없다.

---

## 11. p.8 — §4 Conclusion `[인쇄]`

> "Using our custom-made fixture, we successfully monitored the vertical displacement of ASSLBs
> under constant pressure cycling and observed pressure variations during constant volume cycling.
> Additionally, we were able to **decouple the volume changes of the sulfur, Li₂S cathodes, Li_xIn
> anode, and SSE**. Our hypothesis was confirmed through SEM imaging and electrochemical impedance
> analysis, revealing that **at least two types of changes** occur during ASSLB cycling: volume
> expansion and contraction, material fracturing, and the formation of voids. We found that while
> the **structural changes to the primary active material particles are irreversible**, **void
> formation can be mitigated through the application of stack pressure**. Stack pressure reduces
> fracturing and promotes void healing by enabling particle rearrangement. In conclusion, the
> **primary role of stack pressure is to maintain microscale integrity by ensuring continuous
> physical contact between particles, thus preventing the formation of voids.**"

`[해석]` 결론 문장 자체에 **"two types" 라 해놓고 세 가지를 나열**하는 오류가 있다 (팽창/수축,
파단, 공극). 초록은 제대로 둘(균열, 공극)로 쓴다.

---

## 12. SI 대조 — **미확보**

| SI 항목 | 본문에서의 쓰임 | 이 digest 의 처리 |
|---|---|---|
| **Fig. 1S** | `[인쇄, §1]` "The excessive weight of the stack pressure fixture, **accounting for 80–90 % of the cell/battery weight**, as shown in Fig. 1S, necessitates a redesign of the cell for practical use." | **SI 미확보.** 80–90 % 라는 수치의 계산 근거(어느 fixture, 어느 셀 크기)를 확인하지 못했다. 인용 시 "저자 주장" 으로만. |
| **Video 1S** | `[인쇄, §3]` "a symmetric **Li\|SSE\|Li** cell demonstrated **reciprocal behavior** during cycling. The volume increase on one Li electrode compensated for the volume shrinkage of the opposite Li electrode, making the overall volume change of the entire cell **negligible**." | **SI 미확보.** 이 위키에서 **Li 금속 전극의 부피 항을 정량으로 쓸 수 없다.** §6 의 "상보성" 설계 원리는 이 영상에만 근거한다. |

`[인쇄]` 본문의 SI 링크: "Supplementary material related to this article can be found online at
doi:10.1016/j.nanoen.2025.110887." **Table S 는 인용 자체가 없다.**

★ **후속 작업**: SI(특히 Video 1S)를 구하면 anode-free 의 Li 석출 부피 항에 직접 걸린다.
지금은 [[anode-free-li2s-assb]] 에 **"압력" 만 채우고 "Li 부피" 는 비워 둔다.**

---

## 13. 이론 부피 변화 vs 실측 — `[재현]` 대조

이 절은 **원문에 없는 계산**이다. 모두 `[재현]`/`[해석]` 이며, 가정을 명시한다.

**가정**: ρ(Li2S) = 1.66, ρ(S, α-S8) = 2.07 g cm⁻³ (§5.2 표) · 양극 두께 **80.5 µm**
(Fig. 7d 주석) · 두께 변화는 면내 구속 하에서 부피 변화가 **전부 두께로만** 나타난다고 본다
(원통 셀이므로 타당) · 전환은 완전하다고 본다.

| 물음 | 계산 | 값 |
|---|---|---|
| Li2S 1 mol 의 완전 탈리튬화(충전)로 줄어드는 부피 | 27.68 − 15.49 | **12.19 cm³ mol⁻¹ = −44.0 %** |
| 같은 반응의 역방향(방전) 팽창률 | 12.19 / 15.49 | **+78.7 %** |
| 양극 두께 80.5 µm 가 −10 µm 줄려면 필요한 **Li2S 부피분율** | 10 / (0.440 × 80.5) | **f ≈ 0.28 (28 vol%)** |
| 안정화 후 진동 ±1 µm 에 대응하는 **가역 전환 부피분율** | 1 / (0.440 × 80.5) | **f ≈ 0.028 (2.8 vol%)** |

★★ `[해석]` **여기서 이 논문이 말하지 않은 것이 나온다.**
1. **첫 충전의 −10 µm** 는 Li2S 부피분율 ≈28 % 의 **완전 전환**과 같은 크기다. 33.3 wt% 의
   Li2S 가 (SE·탄소보다 가벼우므로) 부피로 30 % 안팎을 차지한다고 보면 **정확히 맞는 자릿수**다
   — 즉 **첫 충전의 셀 수축은 Li2S → S 전환만으로도 거의 전부 설명된다.**
   (저자는 이 몫을 "재배열" 과 나누지 않았다.)
2. 그런데 **안정화 후의 사이클당 진동은 ±1 µm**, 즉 위 값의 **1/10** 이다. 같은 반응이
   같은 양만큼 왕복한다면 매 사이클 ±10 µm 가 나와야 한다.
   → 셋 중 하나다: **(a) 몇 사이클 만에 활물질 이용률이 1/10 로 떨어졌거나, (b) 복합양극 내부
   공극이 활물질의 변형을 흡수해 셀 두께로 나오지 않거나, (c) 둘 다.**
   Fig. 8a 가 100 사이클에 63 % 를 유지한다는 것(정압)을 보면 **(a) 만으로는 설명이 안 된다.**
   → ★ **SE 50 wt% 복합양극은 활물질 변형의 대부분을 내부에서 흡수한다**는 뜻이 된다.
   이것이 사실이라면 **"cell breathing" 의 주범은 반응이 아니라 비가역 치밀화(재배열)** 다.
3. `[해석]` 이 추론이 우리에게 중요한 이유: **우리 조성(SE 50 wt%)이 이 논문과 같으므로**,
   우리 셀에서도 **첫 사이클 이후의 셀 두께 변화는 작을 것**이고, **압력 관리의 초점은
   "첫 충전 + 초기 몇 사이클" 에 놓여야 한다.** 이 논문의 모든 데이터(Fig. 3, 4, 8a 의 초기
   구간)가 같은 방향을 가리킨다.

---

## 14. 우리 연구와의 접점

### 14.1 이식 가능 / 불가 표

| 이 논문 | 우리 ([[li2s-assb-reference-cell]] / [[anode-free-li2s-assb]]) | 옮겨 올 수 있는 것 | 옮겨 올 수 없는 것 |
|---|---|---|---|
| Li2S : C65 : LPSCl = **33.3 : 16.7 : 50 wt%**, 바인더 없음 | Li2S : LPSCl : AB = **30 : 50 : 20** | ★ **거의 그대로** — SE 50 wt% 동일, 활물질 ±3 wt% | 탄소 종류 (Super C65 vs AB) |
| **one-step** planetary BM, ZrO2 용기, **300 rpm 4 h**, Pulverisette 7 | one-step BM (주 경로) | ★ **장비·rpm·시간의 구체적 선례** → [[mixing-equipment-ball-mill-thinky]] | 볼/BPR/분위기 (미기재 G13) |
| **운전 스택 압력 7 MPa** 정압 | (기록 필요) | ★ **우리 셀의 압력을 기록·고정하라**는 규율 | 7 MPa 라는 값의 타당성 (G19, §15) |
| 성형: SE 필름 **300 MPa 3 min** / SE 펠릿 **500 MPa** / 양극 압착 **300 MPa 3 min** / Li–In **50 MPa 20 s** | (기록 필요) | ★ **성형 조건 세트 전부** | — |
| **LVDT + 스프링 4개** 정압 fixture, **압력변환기 + 나사** 정용적 fixture | 없음 | ★ **설계 수치 전부** (§3.1 `[재현]` 표) — 우리가 만들 수 있다 | 논문의 "10⁻² MPa" 환산 (G10 — 틀렸다) |
| **LTO 를 zero-strain 대극**으로 써서 성분 분해 | 없음 | ★ **방법 자체** — 어느 쪽이 움직이는지 가르는 값싼 수단 | LTO 화학식 표기 (G17) |
| Li2S 양극이 S 양극보다 수축 크다 (19 vs 15 µm) | Li2S 가 우리 활물질 | **Li2S 는 첫 단계가 수축**이라는 인식 | 절대값 (로딩 미기재 G2) |
| ★ **Li2S 첫 충전 한 번에 총 수축의 절반(≈10 µm)** `[도표]` | [[li2s-activation-first-charge]] | ★ **활성화의 기계적 얼굴** — 첫 충전에서 압력을 특히 관리 | 첫 충전 컷오프 수치 (G4) |
| **Li_xIn 음극 −42 µm** — 세 성분 중 최대 | 1단계 음극이 Li–In | ★ **우리 셀 부피 변화의 주범은 음극일 수 있다** | Li–In 조성·두께가 다르면 값도 다르다 |
| 정용적에서 **양극 +9.4 %, SE −10.9 %** (SEM) | — | ★ **"양극이 SE 를 밀어낸다"** 는 실측 | 우리 셀 두께로의 환산 |
| 재압축은 용량을 **부분 회복**시키나 **Ohmic 은 오히려 오른다** | — | **공극(가역) vs 균열(비가역) 이분법** | 이 이분법의 직접 증거는 약하다 (§16) |
| Li∣SSE∣Li 대칭셀의 **상보적 부피 거동** | anode-free 의 Li 석출 | 설계 원리("양극 팽창 ↔ 음극 수축을 동기화") | **정량값 없음 (Video 1S 미확보 G18)** |
| 60 °C 운전 | 우리 온도 (기록 필요) | — | **온도가 다르면 SE 소성·크리프가 다르다** |

### 14.2 [[anode-free-li2s-assb]] 의 "스택 압력·집전체" 항목에 넣을 것

그 페이지의 미결 항목 4번("스택 압력·집전체 계면이 침적 형태를 정한다 — 근거 논문 없음")에
대해 이 논문이 **채우는 것**과 **못 채우는 것**:

**채운다 (압력 쪽)**
1. ASSB 에서 **운전 스택 압력의 1차 역할은 "공극 방지" 이지 "접촉 압착" 이 아니다** —
   압력은 **입자 재배열**을 가능하게 해 활물질 수축이 만든 공극을 메운다 (`[인쇄]` 결론).
2. **정용적으로 두면 7 MPa 가 ≈1 MPa 떨어진다** (`[인쇄]`) — 즉 **스프링이나 벨빌 와셔 같은
   compliance 가 없는 구속은 몇 사이클 만에 압력을 잃는다.**
3. 압력 손실의 결과는 **Ohmic +50 %**, **DRT 주피크 +40 %**, **100 사이클 용량 50 vs 63 %**.
4. **되돌릴 수 없다** — 10사이클 후 재압축은 용량을 일부 되살리지만 회복폭이 사이클마다
   줄고, **Ohmic 저항은 오히려 더 오른다**.
5. **작은 셀에서도 fixture 가 무게의 80–90 %** (저자 주장, Fig. 1S 미확보) — anode-free 의
   에너지밀도 논거는 **압력 하드웨어를 포함해** 따져야 한다.

**못 채운다 (집전체 쪽)**
- 이 논문에 **anode-free 구성이 없다.** 음극은 Li–In 또는 LTO 이고, **집전체는 스테인리스 로드**
  뿐이다. Li 석출 형태·집전체 코팅·핵생성에 관한 데이터가 **전혀 없다.**
- Li 금속의 부피 항은 **Video 1S 하나**(미확보)에만 있다.
- → [[anode-free-li2s-assb]] 의 4번 항목은 이 논문으로 **절반만** 채워진다. 나머지 절반
  (집전체·Li 침적)은 여전히 비어 있고, 그 자리는 `raw/papers/zhang2026_…`(Na 박 집전체,
  0/1/4 MPa)가 더 가깝다.

### 14.3 가장 값싼 다음 실험 `[해석]`

1. **지금 당장, 장비 없이**: 우리 셀의 **성형 압력·운전 압력·유지 방식(강체 볼트인가 스프링인가)
   을 실험 노트에 수치로 기록한다.** 이 논문이 보여준 대로 그 값이 없으면 나중에 어떤 비교도
   불가능하다 (Huang 2026 G1 이 그 예다).
2. **볼트 구속이라면**: 우리 셀은 지금 **정용적 조건**일 가능성이 높다. 그렇다면 **첫 10 사이클
   후 한 번 재조임**만 해도 이 논문의 Fig. 8a 대로 용량이 튀어오를 수 있다 — **재조임 전후
   EIS** 로 확인한다 (장비 추가 없음).
3. **스프링 도입**: 이 논문의 §3.1 `[재현]` 표대로 **4개 병렬 254 N mm⁻¹, 초기 압축 3.4 mm**
   면 φ12.6 mm 셀에서 7 MPa 다. 우리 셀 지름에 맞춰 스케일하면 된다.
   (권장: **변위 허용범위를 5 µm 로 잡아야** 압력 변동이 0.01 MPa 이내다 — G10.)
4. **LVDT 없이 하는 근사**: 다이얼 게이지(1 µm 분해능)로도 이 논문의 신호(첫 충전 −10 µm)는
   보인다. **가장 값싼 관측은 "첫 충전 전후 셀 높이 1회 측정"** 이다.
5. **LTO 대극 트릭**: 우리 셀에서 양극/음극 중 누가 움직이는지 가르고 싶다면 **LTO 대극 셀 한
   개**면 된다 (이 논문의 방법 그대로). Li–In 이 주범인지 확인하는 가장 싼 방법.

### 14.4 열린 질문 카드와의 연결 `[해석]`

- [[reference-cell-500-600-mahg]] — 이 논문은 **절대 용량을 주지 않으므로(G1) 목표값 자체에는
  근거를 주지 못한다.** 대신 **"용량이 안 나올 때 의심할 변수" 목록에 스택 압력을 추가**한다.
  특히 **우리 셀이 볼트 고정(정용적)이라면 이 논문이 예측하는 열화 패턴(3사이클부터 감소,
  재조임으로 부분 회복)** 을 확인할 수 있고, 그 패턴이 보이면 원인이 조성이 아니라 **구속
  방식**이라는 뜻이다. → 이 카드에 **압력 가설**을 새로 붙일 자리.
- [[one-step-vs-two-step-mixing]] — 이 논문은 **one-step**(Li2S + C65 + LPSCl 동시 투입,
  planetary 300 rpm 4 h)으로 동작하는 셀을 만들었다는 **약한 for-evidence** 다. 단 **성능
  절대값이 없어(G1) one-step 의 우열을 말하지 못한다.** 조건만 [[composite-cathode-mixing-routes]]
  의 칸에 채워 넣는다.

---

## 15. ★ 압력 축에서 세 논문을 나란히 놓기

이 위키에 지금 있는 세 digest 의 압력 정보를 한 표로 모은다. **성형/운전을 반드시 갈라 읽는다.**

| | **Qu 2025** (이 논문) | `zhang2026_…` | `huang2026_…` |
|---|---|---|---|
| 계 | LPSCl, S 또는 Li2S 양극, Li–In / LTO | LPSCBr, Li2S-PI3 양극, **anode-free(Na 박)** | LPSC, S 양극 + HES |
| **성형 — SE** | 필름 **300 MPa 3 min** / 펠릿 **500 MPa** | **250 MPa 3 min** | **350 MPa** |
| **성형 — 양극** | **300 MPa 3 min** (SE 필름에 압착) | **400 MPa 3 min** | **450 MPa** |
| **성형 — 음극** | Li–In **50 MPa 20 s** | Li **75 MPa 30 s** · Na/Cu **25 MPa 30 s** | 미기재 |
| **운전 스택 압력** | **7 MPa** (정압) · 정용적(초기 7 MPa) | **0 / 1 / 4 MPa** (설정값) | **미기재 (G1)** |
| 온도 | **60 °C** | 25 °C (일부 90 °C) | 상온 |
| 압력이 성능에 미친 영향 | 정압 **63 %** vs 정용적 **50 %** @100 cyc `[도표]` | 4 MPa **92.2 %** · 1 MPa **70.54 %** @300 cyc · **0 MPa 는 60 cyc 에 붕괴** | 측정 없음 |
| 압력의 **기전**을 쟀는가 | ★ **쟀다** (변위 µm, 압력 MPa, 단면 SEM, DRT) | 안 쟀다 (성능 곡선만) | 안 쟀다 |
| 압력을 **낮추는 방법**을 제시했나 | 아니오 (7 MPa 유지를 권한다) | ★ **예** (Na 의 낮은 항복강도로 1 MPa 가능) | 아니오 |

★★ `[해석]` **두 논문을 나란히 놓으면 위키 수준의 충돌이 하나 드러난다.**

- Qu 2025 은 `[인쇄, §1·§3]` **"cycling stack pressure above 7 MPa are crucial"**,
  **"A stack pressure of approximately 7 MPa is necessary for the long-term cycling performance
  of an ASSLB"** 라고 두 번 쓴다. **출처 없음(G19), 다른 압력값을 시험하지 않음.**
- Zhang 2026 은 같은 아지로다이트 계·같은 Li2S 활물질에서 **4 MPa 로 300 사이클 92.2 %**,
  **1 MPa 로도 300 사이클 70.54 %** 를 보였다 (단 0 MPa 는 60 사이클에 붕괴).
- → **"7 MPa 가 필요하다" 는 명제는 이 위키 안에서 이미 반증 쪽으로 기운다.** 실제로 필요한
  것은 **"0 이 아닌, 그리고 사이클 중에 떨어지지 않는" 압력**이다. Qu 2025 자신의 데이터가
  그렇게 말한다 — 정용적 셀이 죽은 이유는 **압력이 낮아서가 아니라 압력이 7 → 6 MPa 로
  *떨어졌기* 때문**이고, Zhang 2026 의 1 MPa 셀은 **1 MPa 를 유지**했다.
- ★ **이 위키가 채택할 명제**: **절대값보다 "유지" 가 중요하다.** 낮은 압력이라도 compliance
  (스프링/벨빌)로 **일정하게** 유지되면 돌아가고, 높은 압력이라도 강체 구속이면 첫 몇
  사이클에 잃는다. 두 논문이 서로 다른 축에서 같은 결론을 가리킨다.
- `[해석]` 온도도 갈린다 — Qu 2025 은 **60 °C**, Zhang 2026 은 **25 °C**. 60 °C 에서는 황화물
  SE 의 크리프가 커서 재배열이 더 쉬울 것이고, 그렇다면 **Qu 의 "압력이 재배열을 유도한다"
  는 60 °C 의 이야기**일 수 있다. 상온에서 같은 효과가 나는지는 두 논문 어느 쪽도 답하지 않는다.

`[해석]` Huang 2026 의 G1(운전 압력 미기재)은 이 논문으로 **메워지지 않는다** — 다른 셀이다.
그러나 **"성형 300–500 MPa / 운전 1–7 MPa" 라는 두 자릿수 분리**가 세 논문 공통이므로,
Huang 2026 의 성능을 읽을 때 **"운전 압력이 7 MPa 근처였을 것" 으로 가정하는 것은 부당하지
않다** — 다만 그것은 가정이고 digest 에는 여전히 "미기재" 로 남긴다.

---

## 16. 비판 (이 digest 의 판단)

1. ★ **"측정 논문" 인데 측정의 정량성이 저자 스스로 부인된다.** Fig. 5(제목의 "Deciphering"
   이 사는 자리)는 **세 개의 다른 셀**을 100 % 로 정규화해 겹친 것이고, 저자도 "more
   qualitative than quantitative", "adding the red and blue lines might not exactly result in
   the black curve" 라고 적는다 (G7). 실제로 **+3 + (−11) = −8 ≠ −6 µm** 로 25 % 가 안 맞고
   (G9), 단위 오기("6 mm")까지 있다 (G8). **성분 분해는 방향성 결론까지만 유효하다.**
2. ★ **절대 용량·로딩이 없다** (G1, G2). 이 때문에 (a) 셀의 품질을 알 수 없고, (b) µm 를
   활물질 몰수로 정규화할 수 없고, (c) 우리 셀로의 환산이 막힌다. **부피 변화 논문이 활물질
   질량을 안 적는 것은 치명적이다** — 부피 변화는 정의상 반응한 물질의 양에 비례한다.
3. ★ **"maintained it capacity well" 이 63 % 다** (G20). 정압 셀도 100 사이클에 37 % 를 잃는다.
   **CE 는 양쪽 다 ≈100 %** 이므로, 이 위키의 규율대로 **"안정" 은 CE 가 아니라 용량으로
   읽어야 하고 그 값은 63 % vs 50 % 다.** 초록의 "enhance battery performance and durability"
   는 13 포인트의 차이다.
4. ★ **자기 데이터를 자기 서술이 가린다** (G12). Fig. 7 의 정용적 결과 — **양극 +9.4 %,
   SE −10.9 %** — 는 이 논문에서 가장 깨끗하고 가장 기계적으로 의미 있는 수치인데,
   본문은 "slightly" 두 번으로 넘어간다. 이 digest 는 그 계산(§9.1)을 복원해 둔다.
5. **"균열은 영구적, 공극은 가역" 이분법의 직접 증거가 없다.** 균열을 **본 적이 없다** —
   Fig. 6 은 만화이고, Fig. 7 상단행은 균열이 아니라 결정 크기를 비교한다. 균열의 근거는
   **EIS 의 비가역성**(재압축해도 Ohmic 이 안 내려감)이라는 **간접 추론 하나**다. 대안 설명
   (재압축이 접촉을 더 망쳤다, SE 층이 이미 비정질화됐다)을 배제하지 않았다.
6. **상 동정이 전혀 없다** (G15). "sulfur crystal 이 커졌다/작아졌다" 는 ×8k SEM 3장의
   형태 판독이고, **EDS·XRD·라만 어느 것도 없다.** 황화물 SE 결정과 S8 결정을 2차전자 상에서
   구별할 근거가 제시되지 않았다.
7. **7 MPa 의 출처가 없고 다른 압력을 시험하지 않았다** (G19). 이 논문은 "압력이 중요하다" 를
   보였지 **"7 MPa 가 필요하다" 를 보이지 않았다.** 비교군은 7 MPa 와 "7 MPa 에서 시작해
   떨어지는 것" 둘뿐이다. 3 MPa 정압, 1 MPa 정압이 없다. → §15 의 충돌.
8. **DRT 의 방법이 미기재**다. 정규화 파라미터·알고리즘 없이 피크 높이를 비교한다. 게다가
   그림에서 읽으면 **"정용적 3사이클 후 저항 증가" 가 피크 높이로는 성립하지 않는다**
   (CV-3rd 310 < CP-3rd 348 — §10.3).
9. **EIS 를 상온에서 쟀는데 사이클은 60 °C 였다** (§3.6). 논문은 이를 언급하지 않는다.
10. **표기 오류가 많다**: LTO 화학식 Li4Ti4O12 (G17), "1166 **MAh** g⁻¹", 캡션의 "LIPSCl"/
    "LiPSCl", x축 "Properation", "6 mm", 결론의 "two types" 뒤 세 가지 나열, "sulfur's113 °C".
    **교정이 거의 안 된 원고다.** 참고문헌도 11개뿐이다.
11. **좋은 점은 분명하다** `[해석]`:
    - **fixture 두 개의 설계가 단순하고 복제 가능**하다 (같은 셀 몸통, 스프링 유무만 차이).
      LVDT 를 쓴 것은 실용적 선택이고 부품번호까지 적어 두었다. **이 논문의 진짜 가치는
      여기 있다.**
    - **LTO zero-strain 대극으로 성분을 가른다**는 착상이 값싸고 명확하다.
    - **재압축 실험**(10·20·30…사이클마다)은 "공극 vs 균열" 가설을 **직접 시험하는 설계**다.
      회복폭이 사이클마다 줄어드는 곡선은 이 논문의 가장 강한 데이터다.
    - **τ≈1 s DRT 어깨의 소멸**은 미세하지만 재현 가능한 관측이고, 기전 주장과 정합한다.
    - **서론의 문제의식**(압력 fixture 가 셀 무게의 80–90 %)은 이 분야가 잘 안 적는 정직한
      지적이다.

---

## 17. 이 저장소가 가져갈 것

- **개념 신설 후보**: `stack-pressure-volume-change-assb` — "ASSB 의 운전 스택 압력: 무엇을
  하는가, 얼마가 필요한가, 어떻게 유지하는가". 뼈대는 (1) 성형 압력 ≠ 운전 압력(두 자릿수
  차이), (2) 압력의 1차 역할은 **공극 방지 = 입자 재배열 허용**, (3) **절대값보다 유지**
  (정압 vs 정용적, compliance 의 필요), (4) 가역(공극) vs 비가역(균열) 이분법과 그 증거의
  한계, (5) 실측 자릿수 표(이 digest §6 의 성분별 변위·압력 표), (6) 미해결 — 최소 필요
  압력은 계·온도·음극에 따라 다르며 1–7 MPa 사이 어딘가.
  `sources:` 는 이 digest + `raw/papers/zhang2026_…` → **multi-source-primary** 가 된다.
- **[[li2s-activation-first-charge]] 갱신**: "Li2S 첫 충전은 **기계적 사건이기도 하다** —
  Qu 2025 `[도표, Fig. 3c]` 에서 첫 충전 한 번에 셀이 ≈10 µm 줄고 이는 전체 수축의 절반이다"
  한 줄. `sources:` 에 이 digest 추가.
- **[[li2s-assb-composite-cathode]] 갱신**: 우리와 같은 **SE 50 wt%** 복합양극의 실측 두께
  (≈80 µm), 성형 조건(300 MPa 3 min), 사이클 후 두께 변화(정압 −9.4 %, 정용적 +9.4 %).
- **[[mixing-equipment-ball-mill-thinky]] 갱신**: "Fritsch **Pulverisette 7** planetary,
  **ZrO2 용기, 300 rpm, 4 h**, Li2S+C65+LPSCl **one-step**" 한 줄 (볼·BPR 미기재).
- **[[composite-cathode-mixing-routes]] 갱신**: one-step 열에 위 조건과 조성(2:1:3) 추가.
- **[[anode-free-li2s-assb]] 갱신**: 미결 항목 4번의 **"스택 압력" 절반**을 §14.2 의 5개
  항목으로 채우고, **"집전체·Li 침적" 절반은 여전히 공백**임을 명시.
- **[[li2s-assb-reference-cell]] 갱신**: "구속 방식(볼트=정용적 / 스프링=정압)을 기록한다"
  를 미결 항목으로 추가. §14.3 의 값싼 실험 5개.
- **[[reference-cell-500-600-mahg]] 에 가설 추가**: "용량 미달의 원인 후보에 **구속 방식**이
  있다 — 정용적(강체 볼트) 구속이면 3사이클부터 감소하고 재조임으로 부분 회복한다는 서명이
  있다 (Qu 2025 Fig. 8a)." Evidence 는 **간접**(절대 용량 없음 G1)임을 명시.
- **[[one-step-vs-two-step-mixing]]**: 약한 for-evidence(one-step 으로 동작하는 셀) + 성능
  절대값 부재로 **우열 판단 불가**라고 명시.
- **`comparisons/` 후보**: §15 의 "압력 축 3논문 표" 를 `comparisons/` 한 페이지로 승격.
- **주의**: 이 digest 의 `compare:` 성능 키는 비어 있다 (측정 논문). `/compare` 화면에서
  이 행은 **조성·혼합·압력 열만** 채워진다 — 정상이다.

---

## 18. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

| 그림 | 봤는가 | 어디에 썼는가 |
|---|---|---|
| **Fig. 1** (a–d) | ✓ | §3.1, §3.2 — fixture 도면. 가장 오래 봤다. LVDT/스프링/압력변환기 배치 확인 |
| **Fig. 2** (a,b) | ✓ | §4 — LTO 대조셀. **본문이 "변화 없음" 이라 한 곳에서 −2 µm / −0.12 MPa 를 읽었다** (G11) |
| **Fig. 3** (a–d) | ✓ (+ 패널 c 확대) | §5.3 — 이 논문의 본체. **Li2S 첫 충전 −10 µm** 를 여기서 읽었다 |
| **Fig. 4** (a,b) | ✓ | §6 — Li_xIn −42 µm / −1.4 MPa |
| **Fig. 5** (a–d) | ✓ | §7.3 — 성분 분해. **패널마다 축 범위가 달라** 표에 명시 |
| **Fig. 6** | ✓ | §8.3 — 가설 만화 (데이터 아님) |
| **Fig. 7** (a–f) | ✓ | §9 — **두께 6개 값**과 결정 형태. 이 논문 유일의 구조 정량값 |
| **Fig. 8** (a–c) | ✓ (+ a·b·c 각각 확대) | §10 — 유지율 63/50 %, Ohmic 40→65 Ω, DRT 피크 6개 |
| **Fig. 1S** | **✗ SI 미확보** | §2.1·§12 에 "저자 주장" 으로만 인용 (fixture 무게 80–90 %) |
| **Video 1S** | **✗ SI 미확보** | §6·§12 에 "저자 주장" 으로만 인용 (Li 대칭셀 상보성) |

**본문 서술과 어긋난 그림**: 세 군데.
1. Fig. 2 — "LPSCl 부피 변화 없음" vs 실제 −2 µm / −0.12 MPa (G11).
2. Fig. 7 — "slightly" vs 실제 ±9–11 % (G12).
3. Fig. 8c — "정용적은 3사이클 후 저항 증가" vs DRT 피크 높이로는 정압 쪽이 더 높다 (§10.3).

**본문 안에서 서로 어긋난 수치**: G5(0.05 C vs C/10), G6(100 µm 분모), G8(6 mm),
G9(3 − 11 ≠ −6), G10(20 µm = 10⁻² MPa), G20(maintained well = 63 %).

**크로핑 파일**: `raw/figures/qu2025_volume-changes-li-s-solid-state-battery-components-cycling/`
— `fig_1.png` … `fig_8.png` + `figures.json` (8장, 전부 본문 그림. SI 그림 없음).

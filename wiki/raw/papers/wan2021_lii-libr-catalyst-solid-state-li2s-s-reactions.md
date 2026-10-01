---
title: "Wan et al. 2021 — Understanding LiI-LiBr Catalyst Activity for Solid State Li2S/S Reactions in an All-Solid-State Lithium Battery (Nano Lett. 21, 8488)"
description: "활물질이 MoS2 인 전고체 Li 셀에 LiI-LiBr(75:25 몰) + 카본블랙을 볼밀로 넣어 방전 생성물 Li2S 의 산화를 돕는다는 논문 — 우리에게 쓸모 있는 것은 본류가 아니라 Figure 2 의 곁가지(Li2S@LiI-LiBr vs 첨가제 없는 Li2S 직접 대조)다. 첨가제가 있으면 첫 충전이 2.80 V 평탄 plateau 로 이론용량까지 가고, 없으면 plateau 없이 3.5 V 까지 끌려간다. SI 미확보"
source_url: local-upload/9835470f-LiI-LiBr_catalyst_for_ASSLSBs.pdf
doi: 10.1021/acs.nanolett.1c03415
ingested: 2026-10-01
sha256: 01a9c2209a0948d760a705d54a90279c715c84c68efd6d80192d88cc9acf2ef8
tags: [li2s, assb, activation, composite-cathode, mixing-process, carbon, units]
compare:
  system: "ASSB — ★ 활물질은 MoS2(전이금속 황화물)이고 Li2S 는 방전 생성물. 별도 대조실험으로 Li2S 양극 전고체셀(Fig. 2)이 있고 우리에게 유효한 것은 그쪽뿐이다"
  electrolyte: "미기재 — 본문 7쪽 어디에도 자기 셀의 SE 이름·조성·두께가 없다 (Experimental 이 SI 에만 있고 SI 미확보)"
  cathode: "MoS2@LiI-LiBr@C — MoS2 : LiI-LiBr = 2:1 (몰), LiI:LiBr = 75:25 (몰) → [재현] MoS2 72.4 wt% / LiI-LiBr 27.6 wt%. 카본블랙 함량·SE·바인더 미기재. 대조군 Li2S@LiI-LiBr = Li2S : LiI-LiBr 4:1 (몰) → [재현] Li2S 60.1 wt% / 첨가제 39.9 wt%"
  li2s_source: "해당 없음 — Li2S 는 MoS2 의 방전 생성물(in-situ). 단 Fig. 2 대조실험의 Li2S 는 분말 출발이며 출처·순도·입도 미기재"
  mixing: "2단계 볼밀 — (1) MoS2 + LiI-LiBr 밀링 (2) 카본블랙 추가 밀링. 장비·rpm·시간·BPR·볼 재질·분위기 전부 미기재. 2차 밀링이 입도를 µm → nm 로 바꿈 [도표, Fig. 4e–g]"
  loading_mg_cm2: "0.922 / 1.844 / 4.058 (MoS2 기준). Li2S 대조셀의 로딩은 미기재"
  li2s_wt_pct: "해당 없음 — MoS2 양극"
  anode: "Li 금속 (두께·형태 미기재). Li 재고가 무한 공급이라 첫 CE·Li 재고 수지를 시험하지 않는다"
  first_charge: "MoS2 셀은 방전 선행 (0.5–3.0 V vs Li/Li⁺ 1사이클 → 1.0–2.8 V 이후, 200 mA g⁻¹). ★ Li2S 대조셀(100 mA g⁻¹, 1사이클 3.5 V 컷오프)은 충전 선행 — Li2S@LiI-LiBr 첫 충전 [도표] ≈1165 mAh g⁻¹(Li2S) 로 2.80 V vs Li/Li⁺ 평탄 plateau, 첨가제 없는 Li2S 는 plateau 없이 2.5 → 3.5 V 단조 상승하며 [도표] ≈900"
  first_discharge_mAh_gS: "Li2S 대조셀만: Li2S@LiI-LiBr [재현] ≈1196 · 첨가제 없는 Li2S [재현] ≈731 (각각 [도표] 835 · 510 mAh g⁻¹(Li2S) ÷ 0.698). MoS2 셀은 분모가 달라 환산 불가"
  first_discharge_mAh_gLi2S: "Li2S 대조셀만: Li2S@LiI-LiBr [도표] ≈835 (이론의 72 %) · 첨가제 없는 Li2S [도표] ≈510 (44 %). 분모가 Li2S 질량이라는 것은 [재현] 추론 (G4)"
  cycle_capacity_mAh_gS: "Li2S 대조셀 3사이클 [재현] ≈931 (Li2S@LiI-LiBr) · ≈602 (무첨가)"
  cycle_capacity_mAh_gLi2S: "Li2S 대조셀 3사이클 [도표] ≈650 (Li2S@LiI-LiBr) · ≈420 (무첨가). MoS2 셀 100사이클은 [인쇄] 437.8 mAh g⁻¹(MoS2@LiI-LiBr) = [재현] 604.8 mAh g⁻¹(MoS2) — 분모가 다르므로 Li2S 기준 환산 금지"
  areal_mAh_cm2: "0.87 (0.922 mg cm⁻² MoS2) · 1.15 (1.844) · 2.02 (4.058) — 전부 1사이클 값. Li2S 대조셀은 면적용량 미기재"
  cycles: "100 (MoS2 계, 200 mA g⁻¹, 최저 로딩만) · 20 (로딩 시험; 4.058 mg cm⁻² 는 [도표] 52 % 로 반감) · Li2S 계는 3사이클 프로파일 + [인쇄] 30사이클 유지율 79.7 % (MoS2 계는 94.7 %)"
  temperature_C: "미기재"
  mechanism: "LiI-LiBr 이 Li2S 의 Li⁺–S²⁻ 상호작용을 줄이고 이온전도를 올린다는 주장. 근거 다섯 갈래 전부 간접이고 사후 분석 0건 — (i) 분말 라만 Li–S 적색편이 [도표] ≈7 cm⁻¹, (ii) 분말 EIS Li2S@LiI 6.4×10⁻⁸ → Li2S@LiI-LiBr 1.08×10⁻⁶ S cm⁻¹ ([재현] 16.9배; 초록의 '7 orders' 는 남의 문헌값 10⁻¹³ 과의 비교), (iii) DFT 결함 형성에너지(Vac_Li + I/Br_on_S 복합결함)와 COHP [도표] ICOHP 1.66 → 1.59(Br)/1.61(I) eV = 3–4 % 감소, (iv) CV b 값 0.52–0.57 → 0.79–0.81 (단 논문 스스로 입도 탓이라 쓰고 같은 데이터로 촉매를 증명한다), (v) 과전압·용량 비교. XPS·in situ·TEM 0건, LiI-LiBr 의 용량 기여 분리 0건, Li4I3Br 상의 실험 확인 없음"
  our_axis: "Fig. 2 의 Li2S 양극 직접 대조가 H1(활성화 완료 전위 > SE 산화 전위)의 고체계 근거를 하나 더 준다 — 할로겐화물이 활성화 plateau 를 2.80 V 에 만든다. 그러나 첨가제가 무게의 39.9 wt% 이고, Li2S 양극 쪽 30사이클 유지율이 MoS2 쪽보다 나쁘며(79.7 vs 94.7 %), 요오드 자신의 용량 기여([재현] 109.4 mAh g⁻¹(Li2S))를 분리하지 않아 Zhang 2026 의 요오드 혼입 의심을 해소하지 못한다. MoS2 계 수치(이론의 122–141 %)는 이식 불가"
---

# 수집 목적

H. Wan, B. Zhang, S. Liu, J. Zhang, X. Yao, C. Wang,
**"Understanding LiI-LiBr Catalyst Activity for Solid State Li2S/S Reactions in an
All-Solid-State Lithium Battery"**, *Nano Letters* **21** (2021) 8488–8494,
DOI 10.1021/acs.nanolett.1c03415 (2021-10-04 게재) 의 **절별 해체분석**.

## ★ 먼저 읽어야 할 경고 — 이 논문의 양극은 Li2S 가 아니다

제목에 "Li2S/S Reactions" 가 들어 있지만 **주 셀의 활물질은 MoS2 다.** 초록 첫 문장이
`[인쇄]` "Li||MoS2 solid-state batteries have higher volumetric energy density and power
density than Li||Li2S batteries" 로 시작한다. 즉 저자들은 **Li2S 양극을 일부러 피하고**
MoS2 를 썼고, 여기서 Li2S 는 **방전 생성물**(MoS2 + 4Li → Mo⁰ + 2Li2S)로서 등장한다.
첫 사이클 이후 셀이 "Li‖MoS2 와 Li‖S 의 혼성" 으로 바뀌고 그때 생긴 Li2S 가 느려서 용량이
죽는다 — 그 Li2S 를 깨우는 것이 LiI-LiBr 의 역할이라는 구성이다.

그러므로 **이 논문을 "Li2S 양극 논문" 으로 읽으면 틀린다.** 우리가 쓸 수 있는 부분은
좁고 분명하다:

| 쓸 수 있는 것 | 쓸 수 없는 것 |
|---|---|
| **Figure 2 의 Li2S 양극 대조 실험** — Li2S@LiI-LiBr vs 첨가제 없는 Li2S 를 같은 전고체셀에서 비교한 유일한 자리. 우리 pristine Li2S reference cell 과 **직접 같은 질문**이다. | MoS2 쪽 성능 수치 전부 (816.2 / 626.3 / 498 / 437.8 / 604.8 mAh g⁻¹). 분모가 MoS2 이고 활물질이 다르다. |
| **Figure 3 의 DFT** — Li2S 에 I⁻/Br⁻ 가 S 자리를 치환하면 Li 공공과 짝지은 복합결함이 생겨 Li⁺ 전도가 오르고 Li–S 결합이 약해진다는 계산. 대상 물질이 **Li2S 그 자체**다. | "0.5–3.0 V 1사이클 → 1.0–2.8 V" 전압 프로토콜. MoS2 의 2단계 리튬화에 맞춘 창이다. |
| **LiI-LiBr 조성 최적화의 방향** (LiI:LiBr = 75:25, 양을 늘리면 kinetics↑·총용량↓) | 첨가제의 절대량 처방 (MoS2 2:1 몰비는 MoS2 기준이고, Li2S 기준은 4:1 로 따로다) |
| **Li2S@LiI / Li2S@LiI-LiBr 의 이온전도도 실측** (6.4×10⁻⁸ / 1.08×10⁻⁶ S cm⁻¹) | Li 금속 음극 · 0.5 V 심방전. 우리 Li–In / anode-free 와 전혀 다른 음극 조건이다. |

## 표기 규칙

`[인쇄]` 원문 글자 그대로 / `[도표]` 그림에서 눈으로 읽은 근사값 / `[해석]` 우리 판단 /
`[재현]` 원문 값의 산술 환산(식 병기). 비용량은 분모를 항상 적는다 —
이 논문은 **`mAh g⁻¹(MoS2)`** 와 **`mAh g⁻¹(MoS2@LiI-LiBr)`** 두 분모를 경고 없이 섞어 쓴다 (G1).
전압은 전부 `vs Li/Li⁺` (논문이 축에 그렇게 적었다).

## ★ SI 미확보

본 수집은 **본문 PDF 7쪽만** 확보했다. 이 논문은 **Experimental Section 이 통째로 SI 에 있고**
Figure S1–S9 · Table S1 도 전부 SI 에 있다. 본문이 "Figure S*n*" 으로 인용한 지점은 아래에서
모두 **"SI 미확보"** 로 표시했다. **그 자리를 추측으로 메우지 않았다.**

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

| # | 공백 | 왜 문제인가 |
|---|---|---|
| **G1** | **★ 분모를 경고 없이 바꾼다.** 본문 p.2 `[인쇄]` "reversible capacity of **437.8 mAh g⁻¹ (mass of MoS2@LiI-LiBr)** … for 100 cycles"; 초록 `[인쇄]` "maintain **604.8 mAh g⁻¹ (based on the mass of MoS2)** for 100 cycles". | `[재현]` 두 값은 **같은 데이터다**. MoS2:LiI-LiBr = 2:1 몰, LiI:LiBr = 75:25 몰 → M(LiI-LiBr 단위) = 0.75×133.845 + 0.25×86.845 = **122.09 g mol⁻¹**, MoS2 질량분율 = 2×160.07/(2×160.07+122.09) = **0.7239**. 437.8 ÷ 0.7239 = **604.8** — 소수점까지 일치. 즉 초록은 **첨가제를 분모에서 빼서 같은 셀을 1.38배 좋아 보이게** 적었다. 이 환산이 우리 `compare:` 블록이 이 논문을 인용할 때의 유일한 안전장치다. |
| **G2** | **★ 고체전해질이 무엇인지 본문 어디에도 없다.** 7쪽 전문에서 자기 셀의 SE 이름·조성·두께·전도도가 한 번도 안 나온다. "Li7P3S11" 과 "Li2S-P2S5" 는 **남의 논문(ref 17, 18) 얘기**로만 등장한다. | 전고체 Li–S 논문에서 SE 를 모르면 **활성화 전위도 분해 전압도 해석할 수 없다.** 특히 첫 사이클을 **0.5 V vs Li/Li⁺ 까지 방전**하는데, 황화물 SE 는 그 전위에서 환원 분해된다. 그 비가역 용량이 "MoS2 첫 방전" 에 얼마나 섞였는지 판정 불가. Methods 가 SI 에만 있고 SI 미확보. |
| **G3** | **★ LiI-LiBr 자체의 용량 기여를 한 번도 분리하지 않았다.** 대조군은 MoS2 / MoS2@LiI-LiBr / MoS2@LiI-LiBr@C 셋뿐이고, **"LiI-LiBr + 카본만 넣은 양극"(활물질 없는) 대조셀이 없다.** LiI 의 산화 전위를 자기 셀에서 측정한 적도 없다. | `[재현]` LiI 전량 1 e⁻ 산화(I⁻ → ½I2) 몫 = 0.375 mol LiI per mol MoS2 × 26801 / 160.07 = **62.8 mAh g⁻¹(MoS2)**; LiBr 까지 더하면 83.7. Li2S 셀 쪽(Li2S:LiI-LiBr = 4:1)은 **109.4 mAh g⁻¹(Li2S)**. **이것은 Zhang 2026 의 요오드 혼입 의심(그쪽 `[재현]` 152 mAh g⁻¹(Li2S))과 같은 크기의 양이다.** 논문은 반대로 LiI-LiBr 을 **불활성 사표(dead mass)** 로 전제한다 — `[인쇄]` "it also **reduces the total capacity**, so the molar ratio of LiI-LiBr to MoS2 is controlled at 1:2". 그 전제를 **시험한 실험이 없다.** |
| **G4** | **Figure 2 의 비용량 분모가 적혀 있지 않다.** 축은 그냥 "Specific capacity (mAh g⁻¹)" 이고, Li2S 질량인지 Li2S@LiI-LiBr 복합체 질량인지 캡션·본문 어디에도 없다. | `[재현]` **산술로 Li2S 기준이라고 거의 확정할 수 있다.** 복합체 기준이면 이론용량 = 1166.6 × 0.6008 = **700.9 mAh g⁻¹(composite)** 인데 관측된 첫 충전이 `[도표]` ≈1165 로 **166 %** 가 된다. LiI(65.7) + LiBr(21.9) 을 전부 더해도 788 이라 메울 수 없다. Li2S 기준이면 1165/1166.6 = **99.9 %** 로 딱 맞는다. → **분모는 Li2S 질량**으로 읽는다. 단 이것은 우리 추론이지 원문 진술이 아니다. |
| **G5** | **Figure 2 셀의 전압 프로토콜·로딩이 없다.** `[도표]` 1사이클은 **3.5 V 까지**, 2·3사이클은 **3.0 V 까지** 충전하고 방전은 1.0 V 다 — MoS2 셀의 "0.5–3.0 V → 1.0–2.8 V" 와 **다른 프로토콜**인데 본문은 아무 말이 없다. 로딩(mg cm⁻²)·면적용량도 없다. | 첫 충전 컷오프 3.5 V 는 황화물 SE 의 산화 분해 영역을 깊이 넘는다. Li2S 활성화를 "끝까지" 밀어붙인 값이므로, 우리 셀(SE 를 지키려 3.0 V 부근에서 끊는)과 **직접 비교하면 안 된다.** 이 위키의 Lee 2026(3.62 V) ↔ Zhang 2026(3.0 V) 대립과 같은 축이다. |
| **G6** | **쿨롱 효율이 어디에도 없다 — 숫자로도, 그래프 축으로도.** 본문에서 "Coulombic" 이라는 단어가 0회. Figure 4d 의 사이클 그래프에 CE 축이 없다. | `[재현/도표]` Figure 2a 에서 눈으로 재면 첫 충전 ≈1165 / 첫 방전 ≈835 → **ICE ≈72 %**; 첨가제 없는 Li2S 는 ≈900 / ≈510 → **≈57 %**. 2·3 사이클은 방전(≈650)이 같은 사이클 충전(≈580·≈630)보다 **커 보인다** — 도표 분해능에서 **CE > 100 %** 가 의심되지만 확정 불가. 이 위키 digest 8편 중 4편이 첫 CE 100 % 초과였는데(Cronk 129 %, Yu 110–113 %, Lee 101–107 %, Zhang 114 %) **이 논문은 그 판정 자체가 불가능하다.** |
| **G7** | **"안정" 의 정체.** 100 사이클 유지율을 글자로 안 적었다. SI 쪽 값으로 `[인쇄]` "capacity retention for Li2S@LiI-LiBr was only **79.7 %**, while for MoS2@LiI-LiBr … **94.7 %** after 30 cycles" 만 있다 (Figure S6, SI 미확보). | **활성화 이후 30 사이클 기준이고 100 사이클 기준이 아니다.** 그리고 **Li2S 쪽이 MoS2 쪽보다 훨씬 빨리 죽는다** — 즉 이 촉매는 **Li2S 를 직접 양극으로 쓸 때 더 나쁘다.** 우리에게 가장 중요한 숫자인데 그림이 SI 에 있어 확인할 수 없다. |
| **G8** | **CV 비교의 변수가 최소 셋 동시에 바뀐다.** Figure 5 의 b 값 비교는 **MoS2(마이크로 시트, 첨가제 없음, 탄소 없음)** vs **MoS2@LiI-LiBr@C(나노화, 첨가제 있음, 카본블랙 있음)** 다. | 본문 스스로 `[인쇄]` "implying the surface-controlled process dominates in the MoS2@LiI-LiBr@C cathode **due to the reduced particle size**" 라고 **입자 크기 탓**으로 돌려놓고, 두 문장 뒤에 `[인쇄]` "The significantly improved b value for reaction O1 … **further proved the catalytic effect of LiI-LiBr**" 라고 **같은 데이터로 촉매를 증명**한다. **논리가 자기모순이다.** 입자 크기를 맞춘 대조군(MoS2@C, 첨가제 없이 카본블랙만 밀링)이 **없다.** |
| **G9** | **카본블랙 함량이 없다.** "adding carbon black into the MoS2@LiI-LiBr composite by ball-milling" 이 전부. wt%·종류·비표면적 미기재. | 그래서 MoS2@LiI-LiBr@C 의 용량을 **복합양극 기준(mAh g⁻¹(composite))으로 환산할 수 없다.** 우리 AB 20 wt% 와 무게 배분을 비교할 다리가 없다. Kim 2023 G1·Yu 2024 G1 과 같은 공백의 반복. |
| **G10** | **혼합 조건이 "ball-milling" 네 글자뿐이다.** 장비·rpm·시간·BPR·볼 재질·용기·분위기·건식/습식 전부 없다 (Methods 가 SI). | 우리 [[composite-cathode-mixing-routes]]·[[one-step-vs-two-step-mixing]] 이 필요로 하는 바로 그 변수다. 다만 **순서만은 읽을 수 있다 — 2단계다**: (1) MoS2 + LiI-LiBr 밀링 → (2) 카본블랙 추가 밀링. |
| **G11** | **온도·스택압·셀 구성이 전부 없다.** 운전 온도, 성형 압력, 운전 압력, 펠릿 지름·두께, SE 층 두께, Li 음극 두께 — 한 줄도 없다. | 전고체셀 성능은 압력의 함수다(Qu 2025). 압력 없이 보고된 100 사이클 유지는 재현 근거가 되지 못한다. |
| **G12** | **셀 개수·오차·재현성 없음.** 모든 곡선이 단일 셀로 보인다. 통계 언급 0회. | 이 위키 9편 전부가 같은 공백이다. |
| **G13** | **초록과 본문의 수치가 어긋난다.** 초록 `[인쇄]` "reversible capacity of **816.2 mAh g⁻¹ at 200 mA g⁻¹**"; 본문 p.5 `[인쇄]` "at low current density of **100 mA g⁻¹** … reversible capacity of **819.6 mAh g⁻¹** … after 20 cycles" 이고 "When increasing the current density to 200 mA g⁻¹, a high reversible capacity of **711.3** mAh g⁻¹ was still maintained after 20 cycles". | **816.2 는 어느 조건의 값인지 본문에 대응이 없다.** 결론부는 816.2 를 "areal capacity 0.87 mAh cm⁻² 에서의 가역용량" 으로 다시 쓴다. `[재현]` 0.87 mAh cm⁻² ÷ 0.922 mg cm⁻² = **943.6 mAh g⁻¹(MoS2)** 라 816.2 와도 819.6 과도 안 맞는다 — 면적용량은 **1사이클** 값, 816.2/819.6 은 **20사이클** 값으로 보인다. 다른 두 로딩은 깨끗이 맞는다: 626.3×1.844 = **1.155** ≈ 1.15 ✓, 498×4.058 = **2.021** ≈ 2.02 ✓. |
| **G14** | **★ 보고된 용량이 MoS2 의 이론용량을 넘는다 — 언급이 없다.** `[재현]` MoS2 + 4Li → Mo⁰ + 2Li2S 는 4 e⁻ = 4×26801/160.07 = **669.7 mAh g⁻¹(MoS2)**. 첫 사이클 이후 활물질이 S 로 바뀌어도 S 2원자 × 2 e⁻ = 같은 4 e⁻ 라 **상한은 그대로 669.7** 이다. | 그런데 보고값은 816.2 (**122 %**), 819.6 (**122 %**), 면적 환산 943.6 (**141 %**) 이다. LiI+LiBr 1 e⁻ 전량(`[재현]` 83.7 mAh g⁻¹(MoS2))을 더해도 753 으로 **메워지지 않는다.** 남는 몫의 후보는 **SE 산화환원·카본블랙·0.5 V 심방전의 SE 환원**인데 논문은 **하나도 검토하지 않는다.** → 이 위키의 규율("이론 초과 용량을 보면 SE redox 를 먼저 의심한다")이 그대로 걸린다. |
| **G15** | **Li2S 의 이온전도도 10⁻¹³ S cm⁻¹ 을 자기가 재지 않았다.** `[인쇄]` "It is reported that Li2S has a low ionic conductivity of 10⁻¹³ S cm⁻¹;²²" — ref 22(Lin 2013)의 값이다. Figure 2d 에는 **Li2S@LiI 와 Li2S@LiI-LiBr 둘만** 있고 bare Li2S 가 없다. | 초록·본문의 **"7 orders of magnitude increase"** 는 자기 측정값과 **남의 문헌값**을 비교한 것이다. 같은 장비·같은 펠릿·같은 압력에서 잰 bare Li2S 가 없으므로 그 7자리는 **방법 차이를 포함한 수**다. 자기 데이터 안에서의 증가는 LiI → LiI-LiBr 의 `[재현]` **16.9배**(1.08×10⁻⁶ / 6.4×10⁻⁸)뿐이다. |
| **G16** | **"촉매(catalyst)" 를 정의하지 않는다.** 논문은 "catalyzer / catalytic effect" 를 10회 쓰지만 **촉매의 정의(반응 전후 불변, 회전수)를 보이는 실험이 없다.** 사이클 후 LiI-LiBr 이 그대로 남아 있는지(XRD·XPS·라만 사후 분석) 확인하지 않았다. | **XPS 가 0회, in situ/operando 가 0회, TEM·EDS 가 0회다.** 기전 증거는 (i) 분말 라만 적색편이, (ii) 분말 EIS, (iii) DFT, (iv) CV b 값, (v) 전기화학 성능 — **전부 간접**이고 사후 분석이 하나도 없다. 그래서 "촉매" 와 "리독스 매개체(소모·재생되는 활성 첨가제)" 와 "이온 전도 보조상" 이 **구분되지 않는다.** |
| **G17** | **"LiI-LiBr compound" 의 상(phase)이 무엇인지 모른다.** XRD(Fig. 1a)에 LiI·LiBr 피크가 안 보이고 `[인쇄]` "due to the low amount or **amorphous property** of the LiI-LiBr compound after ball-milling" 라고만 한다. DFT 에서는 **Li4I3Br** 라는 결정상을 계산한다. | **실험에서 Li4I3Br 가 생겼다는 증거가 없다.** 계산은 Li4I3Br 를, 실험은 "비정질 또는 소량" 을 말한다. 즉 **계산 대상과 실험 대상이 같은 물질이라는 보장이 없다.** 이 논문 기전 논증의 가장 약한 연결이다. |
| **G18** | **Figure 3 의 DFT 수치가 본문에 없다.** 본문은 "lower than", "decreases", "lower intrinsic Li vacancy formation energy" 라고만 쓰고 **eV 값을 한 개도 인쇄하지 않았다.** | `[도표]` 그림 범례에서만 읽을 수 있다 — ICOHP: Li–S_bulk **1.66 eV**, Li–S(Vac_Li+Br_S) **1.59 eV**, Li–S(Vac_Li+I_S) **1.61 eV**. **차이가 0.05–0.07 eV (3–4 %) 뿐이다.** 본문의 "effectively improve the decomposition of Li2S" 라는 표현이 이 크기에 걸맞은지 독자가 판단할 수 없게 되어 있다. Fig. 3c/3d 의 "LiI 보다 Li4I3Br 의 Li 공공 형성에너지가 낮다" 는 주장도 `[도표]` 둘 다 ≈0.7–0.9 eV 로 **그림 분해능에서 구별되지 않는다.** |
| **G19** | **Figure 1c,d 의 CV 전류가 "Amps cm⁻²" 인데 두 셀의 로딩이 같은지 안 적혀 있다.** | 면적 기준 전류를 비교하려면 활물질 로딩이 같아야 한다. 다르면 "MoS2@LiI-LiBr 의 피크 전류가 3배" 가 촉매가 아니라 로딩 차이일 수 있다. |
| **G20** | **SI 전체 미확보.** Figure S1(Li2S@LiI-LiBr XRD) · S2(Li2S EIS) · S3(MoS2 100사이클 EIS) · S4/S5(LiI:LiBr = 100:0, 50:50) · S6(30사이클 유지율) · S7(EIS 비교) · S8(0.5–3.0 V 전 구간 사이클) · S9(FeS2@S@LiI-LiBr) · Table S1(문헌 비교) · Experimental Section 전부. | 본 digest 가 "미기재" 로 적은 항목의 **상당수는 SI 에 있을 것이다.** SI 를 구하면 G2·G5·G9·G10·G11 은 메워질 가능성이 높고, G1·G3·G6·G8·G14·G16·G17 은 **SI 로도 안 메워진다**(설계의 문제이지 기재의 문제가 아니다). |

---

## 0. 서지사항 (직접 확인)

| 항목 | 값 |
|---|---|
| 제목 | `[인쇄]` Understanding LiI-LiBr Catalyst Activity for Solid State Li2S/S Reactions in an All-Solid-State Lithium Battery |
| 저자 | `[인쇄]` Hongli Wan‡, Bao Zhang‡, Sufu Liu, Jiaxun Zhang, Xiayin Yao*, Chunsheng Wang* (‡ H.W. 와 B.Z. 동등기여) |
| 소속 | `[인쇄]` Department of Chemical and Biomolecular Engineering, University of Maryland, College Park, MD 20740, USA. 교신 Xiayin Yao 의 메일은 `yaoxy@nimte.ac.cn` (닝보재료기술공정연구소), Chunsheng Wang 은 `cswang@umd.edu` |
| 저널 | `[인쇄]` Nano Letters 2021, 21, 8488−8494 (Letter) |
| DOI | `[인쇄]` 10.1021/acs.nanolett.1c03415 |
| 일자 | `[인쇄]` Received September 2, 2021 / Revised September 28, 2021 / Published October 4, 2021 |
| 키워드 | `[인쇄]` all-solid-state lithium battery, transition-metal sulfide, MoS2@LiI-LiBr, redox kinetic, DFT calculation |
| 연구비 | `[인쇄]` DOE Award DE-EE0008856; H.W. 는 ARPA-E DE-AR0000781 |
| 이해충돌 | `[인쇄]` "The authors declare no competing financial interest." |
| 분량 | 본문 7쪽, 그림 5개, 참고문헌 26개. **Experimental Section 은 본문에 없음 (SI)** |

`[해석]` **Chunsheng Wang(UMD) 그룹**이다. 이 위키의 [[anode-free-li2s-assb]] 계보에서 자주
나오는 그룹이고, ref 5 는 같은 그룹의 Han et al. *Nano Lett.* **16** (2016) 4521 —
"High-performance all-solid-state lithium-sulfur battery enabled by a **mixed-conductive
Li2S nanocomposite**" 다. 즉 **이 그룹은 2016 년에 이미 Li2S 양극을 했고, 2021 년에는
MoS2 로 갈아탔다.** 초록 첫 문장("Li‖MoS2 가 Li‖Li2S 보다 체적 에너지밀도가 높다")이
그 전환의 이유다. 우리가 그 반대 방향(Li2S 양극 고수)을 택하고 있다는 점에서,
**이 논문은 우리 노선에 대한 한 줄짜리 반론이기도 하다.**

---

## 1. 한 문단 요약

전고체 Li‖MoS2 셀을 0.5–3.0 V vs Li/Li⁺ 로 한 번 돌리면 MoS2 가 Mo⁰ + 2Li2S 로 깨지고
충전에서 MoS2 가 온전히 복원되지 않아, 셀은 **"Li‖MoS2 + Li‖S 혼성"** 이 되며 거기서 생긴
Li2S 의 느린 산화가 수명·율속의 병목이 된다. 저자들은 **LiI-LiBr 화합물(LiI:LiBr = 75:25 몰)을
MoS2 에 2:1 몰비로 볼밀로 섞고, 다시 카본블랙을 볼밀로 섞어** MoS2@LiI-LiBr@C 를 만들었다.
근거는 네 갈래다 — (i) 분말 라만에서 Li2S 의 Li–S 진동이 **적색편이**(Li⁺–S²⁻ 상호작용 감소),
(ii) 분말 EIS 에서 Li2S@LiI 6.4×10⁻⁸ → Li2S@LiI-LiBr **1.08×10⁻⁶ S cm⁻¹**,
(iii) DFT 에서 I/Br 의 S 자리 치환이 **Li 공공과 짝지은 복합결함**을 만들어 형성에너지가
고유 Li 공공보다 낮아지고 COHP 로 본 Li–S 결합이 약해짐, (iv) CV 의 b 값이 0.52–0.57 →
0.79–0.81 로 올라 표면제어로 바뀜. 성능은 MoS2@LiI-LiBr@C‖Li 셀이 200 mA g⁻¹ 100 사이클에서
**437.8 mAh g⁻¹(MoS2@LiI-LiBr)** = `[재현]` **604.8 mAh g⁻¹(MoS2)**, 같은 조건의 순수 MoS2 는
**110.7**. 로딩 0.922 / 1.844 / 4.058 mg cm⁻²(MoS2) 에서 면적용량 **0.87 / 1.15 / 2.02 mAh cm⁻²**.
**우리에게 결정적인 것은 본류가 아니라 Figure 2 의 곁가지다** — 같은 전고체셀에서
**Li2S@LiI-LiBr(Li2S:LiI-LiBr = 4:1 몰) vs 첨가제 없는 Li2S** 를 비교했고, 첨가제가 있으면
첫 충전이 **2.80 V 평탄 plateau** 로 ≈1165 mAh g⁻¹(Li2S) 까지 가는 반면, 없으면
**plateau 없이 2.5 → 3.5 V 로 단조 상승**하며 ≈900 에서 끝난다.

---

## 2. p.1 — Abstract

### 2.1 초록 전문 `[인쇄]`

> "Li||MoS2 solid-state batteries have higher volumetric energy density and power density than
> Li||Li2S batteries. However, they suffer from energy and power decay due to the formation of
> lithium sulfide that has low ionic/electronic conductivity and a strong Li−S bond. Herein, we
> overcome these challenges by incorporating the catalytic LiI-LiBr compound and carbon black
> into MoS2. The comprehensive simulations, characterizations, and electrochemical evaluations
> demonstrated that LiI-LiBr significantly reduces Li+/S2− interaction and increases the ionic
> conductivity of Li2S, thus enhancing the reaction kinetics and Li2S/S redox reversibility.
> MoS2@LiI-LiBr@C||Li cells with an areal capacity of 0.87 mAh cm−2 provide a reversible
> capacity of 816.2 mAh g−1 at 200 mA g−1 and maintain 604.8 mAh g−1 (based on the mass of
> MoS2) for 100 cycles. At a high areal capacity of 2 mAh cm−2, the battery still delivers
> reversible capacity of 498 mAh g−1. LiI-LiBr-carbon additive can be broadly applied for all
> transition-metal sulfide cathodes to enhance the cyclic and rate performance."

### 2.2 초록이 세운 두 문제와 두 처방

| 문제 `[인쇄]` | 처방 `[인쇄]` | 그것을 받치는 데이터 |
|---|---|---|
| Li2S 의 **low ionic/electronic conductivity** | LiI-LiBr 이 **"increases the ionic conductivity of Li2S"** (이온) · 카본블랙이 전자 (`[인쇄]` "ensure a sufficient electronic conduction pathway") | 이온: Fig. 2d 분말 EIS + Fig. 3a/3c/3d DFT 결함 형성에너지. **전자 전도도는 이 논문에서 한 번도 측정되지 않았다** — 카본블랙의 역할은 전부 간접(과전압 감소, 입도 감소) |
| Li2S 의 **strong Li−S bond** | LiI-LiBr 이 **"significantly reduces Li+/S2− interaction"** | Fig. 2c 라만 적색편이(정성, 값 미인쇄) + Fig. 3b COHP (`[도표]` ICOHP 1.66 → 1.59/1.61 eV) |

`[해석]` 두 처방의 분담은 깔끔하다 — **LiI-LiBr 은 이온·결합, 카본블랙은 전자·입도**.
문제는 **실험이 이 분담대로 설계되지 않았다**는 것이다. MoS2@LiI-LiBr@C 는 세 변수(첨가제·탄소·입도)가
동시에 바뀐 시료이고, 분담을 가를 대조군(MoS2@C)이 없다 (G8).

---

## 3. p.1–2 — Introduction

### 3.1 MoS2 의 반응식 (원문 번호 그대로) `[인쇄]`

리튬화(방전):

| # | 반응 | 전위 |
|---|---|---|
| (1) | MoS2 + *x*Li⁺ + *x*e⁻ → Li*x*MoS2 | `[인쇄]` ∼1.1 V vs Li/Li⁺ |
| (2) | Li*x*MoS2 + (4−*x*)Li⁺ + (4−*x*)e⁻ → Mo⁰ + 2Li2S | `[인쇄]` ∼0.6 V vs Li/Li⁺ |

탈리튬화(충전):

| # | 반응 |
|---|---|
| (3) | Mo⁰ + Li2S → MoS2 + Li⁺ + e⁻ |
| (4) | Li2S → S + 2Li⁺ + 2e⁻ |

`[인쇄]` "After the full lithiation process, MoS2 converts to metal Mo⁰ and Li2S (Reactions 1 and 2).
However, in the following charge process, the **regeneration of MoS2 is limited** (Reaction 3), and
the **unreacted Li2S will be oxidized to sulfur** (Reaction 4), suggesting that, after the first
cycling at 0.5−3.0 V (vs. Li/Li⁺), **MoS2 will transfer to a hybrid of Li||MoS2 and Li||S batteries**,
where the S suffers from the similar challenges of Li||S batteries, although the in-situ formed
conductive Mo⁰@MoS2 can improve the reversibility of sulfur."

`[해석]` **이 문단이 이 논문을 우리 위키에 들어오게 하는 유일한 다리다.** 저자들 자신이
"첫 사이클 뒤에는 사실상 Li‖S 전지" 라고 쓴다. 그러므로 2사이클 이후의 거동은
**S/Li2S 전환 반응**이고, 그 Li2S 는 **in-situ 로 Mo⁰ 와 함께 나노스케일로 태어난 Li2S** 다.
우리의 **상용 분말 pristine Li2S** 와는 태생이 다르다 — 이 차이가 §12 의 이식 가능/불가 판정의 축이다.

### 3.2 선행 연구의 한계 `[인쇄]`

- `[인쇄]` "the capacity retention of Li7P3S11 solid electrolyte coated MoS2 was **75 %**,¹⁷"
- `[인쇄]` "the initial reversible capacity of the MoS2 nanosheet is **439 mAh g⁻¹** due to the
  incomplete solid-state reaction.¹⁶"
- `[인쇄]` "Narrowing the cutoff voltage to 1.0−3.0 V can suppress the generation of the Li2S/S
  redox couple with low reaction kinetics, however, the reversible reaction between MoS2 and
  LixMoS2 significantly reduced the capacity."

`[해석]` 세 번째가 핵심이다. **전압창을 좁혀 Li2S 를 아예 안 만드는 길**이 있는데 그러면
용량이 작다. 이 논문의 선택은 **Li2S 를 만들되 깨우는 쪽**이다 —
우리와 같은 선택지 구조이고, 그래서 결론이 우리에게 쓸모가 있다.

### 3.3 왜 할로겐인가 `[인쇄]`

> "Inspired by the significant enhancement of ionic conductivity of solid sulfide electrolyte
> (Li2S-P2S5) by replacing S with halogen (Cl, Br, and I),¹⁸ we introduced LiI-LiBr into MoS2 to
> facilitate the oxidation and enhance the ionic conductivity of Li2S because LiI-LiBr can **reduce
> the interaction between Li⁺ and S²⁻**, leading to a **decreased overpotential for the Li2S
> delithiation process**."

> "To further enhance the reaction kinetics, we also added carbon black into the MoS2@LiI-LiBr
> composite by **ball-milling** the mixture to **decrease the particle size of MoS2** and ensure a
> sufficient electronic conduction pathway in the cathode."

`[해석]` 발상의 출처가 **황화물 SE 의 할로겐 치환**(우리 LPSCl 의 Cl 과 같은 원리)이라는
점이 중요하다. 저자들은 그 아이디어를 SE 가 아니라 **활물질 Li2S 자체**에 적용했다.
**"Li2S 를 조금 SE 처럼 만든다"** 가 이 논문의 한 줄 요약이다.

### 3.4 프로토콜 `[인쇄]`

> "Under charge/discharge protocol of **0.5−3.0 V cutoff voltage in the first cycle and 1.0−2.8 V
> in the following cycles**, the MoS2@LiI-LiBr@C||Li all-solid-state battery provided a reversible
> capacity of **437.8 mAh g⁻¹ (mass of MoS2@LiI-LiBr)** at a current density of 200 mA g⁻¹ for 100 cycles."

`[해석]` 여기 인쇄된 분모가 **MoS2@LiI-LiBr** 다. 초록은 같은 데이터를 **MoS2** 분모로
604.8 이라 쓴다 (G1). **같은 논문 2쪽 차이로 분모가 바뀐다.**

---

## 4. Figure 1 — XRD · ex-situ 라만 · CV (기전의 바탕)

### 4.1 Fig. 1a XRD `[인쇄 + 도표]`

- `[인쇄]` MoS2 주피크 2θ = **14.1°, 32.9°, 39.5°, 58.7°**.
- `[인쇄]` MoS2@LiI-LiBr@C 의 **2θ = 26.0°** 는 카본블랙.
- `[인쇄]` "**No diffraction peaks assigned to LiI and LiBr were observed** due to the low amount
  or amorphous property of the LiI-LiBr compound after ball-milling."
- `[도표]` 세 곡선을 겹쳐 보면 **MoS2 → MoS2@LiI-LiBr → MoS2@LiI-LiBr@C 로 갈수록 피크가
  뚜렷이 뭉개지고 배경이 커진다.** 바닥에 표준 막대(2H-MoS2)가 그려져 있다.

`[해석]` XRD 의 실질적 정보는 **"볼밀이 MoS2 결정성을 크게 떨어뜨렸다"** 하나다.
LiI-LiBr 상을 확인하는 데는 실패했고(G17), 그래서 "LiI-LiBr compound" 라는 이름이
**무엇을 가리키는지 끝까지 미확정**이다 — 물리 혼합물인지, 고용체인지, DFT 가 계산한
Li4I3Br 인지.

### 4.2 Fig. 1b ex-situ 라만 — 첫 사이클의 상 변화 `[인쇄 + 도표]`

대상은 **첨가제 없는 MoS2 전극**이다. `[도표]` 아래에서 위로 Pristine → D1.1 → D0.5 →
C1.7 → C2.1 → C3.0 (D = 방전, C = 충전, 숫자는 V vs Li/Li⁺). 세로 점선 3개: **S ≈218 cm⁻¹(빨강)**,
**MoS2 ≈376 과 ≈401 cm⁻¹(검정)**.

| 상태 | `[인쇄]` 본문 서술 | `[도표]` 그림에서 본 것 |
|---|---|---|
| Pristine | "Raman shifts at **376 and 401 cm⁻¹** are assigned to vibrational modes of **2H-MoS2**" | 두 피크가 가장 또렷 |
| D1.1 → D0.5 | "When MoS2 was discharged to 0.5 V, the **Raman peaks for MoS2 disappeared**" | D1.1·D0.5 에서 376/401 소멸, 배경만 |
| C1.7 | "After it was charged back to 1.7 V, and **no Raman peaks for MoS2** can be observed" | 여전히 없음 |
| C2.1 | "Only when the MoS2 was further charged to **2.1 and 3.0 V**, the peaks for **MoS2 and S appear**" | 401 cm⁻¹ 가 또렷이 재등장, 218 부근에 작은 혹 |
| C3.0 | 〃 | 401 약해지고 218 부근 혹 유지 |

`[인쇄]` 결론: "demonstrating that the Li||MoS2 cell has **transferred to a hybrid of Li||MoS2
and Li||S cells after the first cycle** at a cutoff voltage of 0.5−3.0 V. In the following cycles,
the battery was discharged and charged at a cutoff voltage of **1.0−2.8 V to suppress the
accumulation of sulfur**."

`[해석]` 라만은 **정성적**이다. S 와 MoS2 가 "나타난다" 까지가 전부이고 **정량(몇 %가 S 인가)은
없다.** 그런데 뒤의 모든 용량 해석은 "S 가 지배적" 이라는 전제 위에 선다. 그 전제를 받치는
유일한 반정량 근거는 **CV 피크 세기 비교**(아래 4.3)다 — 둘 다 약하다.
그리고 **2.1 V 에서 S 가 보인다**는 것은 중요하다: `[해석]` Li2S → S 산화가 **2.1 V vs Li/Li⁺
부근에서 이미 진행**된다는 뜻이고, 이것은 Cronk 2026 의 "2.4 V 활성화" 와 같은 대역이다.

### 4.3 Fig. 1c,d CV (0.2 mV s⁻¹, 1–3 사이클) `[인쇄 + 도표]`

`[도표]` 두 패널의 세로축은 같은 눈금(±6×10⁻⁴ A cm⁻²), 가로축 0.5–3.0 V vs Li/Li⁺.

| | MoS2 (Fig. 1c) | MoS2@LiI-LiBr (Fig. 1d) |
|---|---|---|
| 1사이클 환원 최저점 `[도표]` | ≈ −2.3×10⁻⁴ A cm⁻² (≈0.6 V) | ≈ **−6.3×10⁻⁴** A cm⁻² (≈0.5 V), 그리고 **≈1.05 V 에 뚜렷한 별도 환원 피크** |
| 1사이클 산화 최고점 `[도표]` | ≈ +1.0×10⁻⁴ (2.2–2.3 V) | ≈ **+4.0×10⁻⁴** (≈2.3 V) |
| 2·3사이클 곡선 면적 `[도표]` | 매우 납작, 거의 직선 | 뚜렷한 닫힌 고리, 1.5 V·1.85 V 부근 환원 어깨 |

`[인쇄]` "the LiI-LiBr compound acts as a **catalyzer** to promote the S/Li2S redox reaction in
the MoS2@LiI-LiBr cathode (Figure 1d) compared with that in the MoS2 cathode (Figure 1c)."

`[인쇄]` 피크 귀속 (2사이클): 환원 **1.7 V = S → Li2S**, **1.1 V = MoS2 → Li*x*MoS2**;
산화 **1.9 V = Li*x*MoS2 → MoS2**, **2.3 V = Li2S → S**.

`[인쇄]` "the peak intensity for the **S/Li2S redox couple is much higher than that of
MoS2/Li*x*MoS2**, implying the S/Li2S is the **dominant redox couple after the first cycle**."

`[해석]` 두 가지를 짚는다.
1. **이 그림이 이 논문에서 "첨가제만" 을 비교한 유일한 전기화학 자리다** (탄소도 입도도
   아직 안 바뀐 2단계 중 1단계). 그래서 촉매 주장의 가장 깨끗한 근거가 Fig. 1c,d 인데,
   저자들은 정작 **Fig. 5 의 b 값**(세 변수가 동시에 바뀐)으로 촉매를 증명하려 한다 (G8).
2. **전류 축이 면적 기준인데 두 셀의 로딩이 같은지 안 적혀 있다** (G19). 3배 차이가
   촉매인지 로딩인지 이 그림만으로는 못 가른다.
   더불어 1사이클 산화 피크가 **2.3 V** 인데, `[해석]` **LiI 의 I⁻/I₃⁻·I₂ 산화도 2.8–3.0 V
   부근 대역**이라 CV 창(≤3.0 V) 안에 들어온다. 논문은 **요오드 피크를 찾아본 적이 없다.**

---

## 5. ★ Figure 2 — Li2S 양극 직접 비교 (우리에게 가장 중요한 절)

> `[인쇄]` 캡션: "Galvanostatic discharge/charge profiles for (a) Li2S@LiI-LiBr and (b) Li2S.
> (c) Raman spectra of Li2S, Li2S@LiI, and Li2S@LiI-LiBr. (d) Impedance spectra for Li2S@LiI and
> Li2S@LiI-LiBr."

`[인쇄]` 실험 설계: "To investigate the catalytic effect of the LiI-LiBr compound on the reaction
of the S/Li2S redox couple, **Li2S and Li2S@LiI-LiBr composite (Figure S1) were prepared by the
same ball-milling procedure**, and then the performances of the two cathodes were compared in
all-solid-state battery."

`[인쇄]` 조성: "the mole ratio of MoS2 to LiI-LiBr was **2:1** and that of **Li2S to LiI-LiBr was
4:1**" (같은 LiI-LiBr/S 몰비를 맞추기 위함).
→ `[재현]` Li2S@LiI-LiBr 의 질량 배분 = 4×45.947 / (4×45.947 + 122.09) = **Li2S 60.1 wt% /
LiI-LiBr 39.9 wt%**. **첨가제가 무게의 40 %다** — "소량 첨가제" 가 아니다.
(참고: Zhang 2026 의 PI3 8 mol% = 43.8 wt% 와 같은 급이다.)

### 5.1 Fig. 2a — Li2S@LiI-LiBr, 100 mA g⁻¹ `[도표]`

**충전 선행**(Li2S 양극이므로). 세로축 1.0–3.5 V, 가로축 0–1200 mAh g⁻¹.

| 곡선 | 충전 | 방전 |
|---|---|---|
| 1st (검정) | 2.4 V 로 급상승 후 **≈2.80 V 평탄 plateau 가 ≈1150 까지 유지**, 끝에서 3.5 V 로 수직 상승 → **총 ≈1165 mAh g⁻¹** | 2.4 → **≈2.0 V plateau** → 경사 하강, 1.0 V 에서 **≈835** |
| 2nd (빨강) | 2.3 V 에서 시작, ≈2.5 V 완만한 어깨 → 3.0 V 에서 **≈580** | ≈2.05 V plateau 후 경사, 1.0 V 에서 **≈650** |
| 3rd (파랑) | 2nd 와 거의 겹침, 3.0 V 에서 **≈630** | 2nd 와 **완전히 겹침**, **≈650** |

### 5.2 Fig. 2b — 첨가제 없는 Li2S, 100 mA g⁻¹ `[도표]`

| 곡선 | 충전 | 방전 |
|---|---|---|
| 1st (검정) | **plateau 가 없다.** 2.5 V 에서 시작해 **2.5 → 3.5 V 로 단조·연속 상승**, 3.5 V 도달 시 **≈900** | ≈2.1 V 에서 꺾여 경사 하강, 1.0 V 에서 **≈510** |
| 2nd/3rd | 2.5 → 3.0 V 단조 상승, **≈420** | ≈2.05 V 이후 경사, **≈420** |

### 5.3 두 패널의 대조 — 우리 축으로 정리

| 항목 | Li2S@LiI-LiBr `[도표]` | Li2S `[도표]` | 비 |
|---|---|---|---|
| 첫 충전 용량 | **≈1165** mAh g⁻¹(Li2S) | **≈900** | 1.29배 |
| 첫 충전 이용률 `[재현]` (÷1166.6) | **≈100 %** | **≈77 %** | |
| 첫 충전 plateau | **≈2.80 V vs Li/Li⁺, 평탄** | **없음 (2.5→3.5 V 단조 상승)** | |
| 첫 방전 | **≈835** mAh g⁻¹(Li2S) = `[재현]` **≈1196 mAh g⁻¹(S)** | **≈510** = `[재현]` **≈731 mAh g⁻¹(S)** | 1.64배 |
| 첫 사이클 CE `[재현]` | **≈72 %** (835/1165) | **≈57 %** (510/900) | |
| 3사이클 방전 | **≈650** mAh g⁻¹(Li2S) = `[재현]` **≈931 mAh g⁻¹(S)** | **≈420** = `[재현]` **≈602** | 1.55배 |
| 방전 plateau | ≈2.05 V, 더 길고 평탄 | ≈2.05 V, 짧고 바로 경사 | |

`[인쇄]` 본문의 서술은 이 한 문장이 전부다: "the Li2S/S redox overpotential in the Li2S@LiI-LiBr
(Figure 2a) cathode was **obviously decreased after the first cycle**, and the capacity is also
**much larger** than that of the Li2S cathode without LiI-LiBr compound (Figure 2b)."
→ **숫자를 하나도 인쇄하지 않았다.** 위 표의 모든 값은 우리가 그림에서 읽은 `[도표]` 다.

### 5.4 ★★ 이 그림이 우리 H1(활성화)에 하는 말

`[해석]` 이 위키의 [[reference-cell-500-600-mahg]] 는 2026-09-30 에 H1 을
**"활성화가 덜 된다" → "활성화 완료 전위 > SE 산화 전위"** 로 재정의했다 (Lee 2026 ↔ Zhang 2026).
**Fig. 2 는 그 재정의에 정확히 들어맞는 세 번째 데이터점이다.**

- 첨가제 없는 Li2S 의 첫 충전은 **plateau 가 없고 3.5 V 까지 끌려 올라간다.** 이것이
  "활성화 완료 전위가 높다" 의 교과서적 모습이다 — 그리고 그 전위대는 황화물 SE 가
  산화되는 영역이다.
- LiI-LiBr 을 넣으면 **plateau 가 2.80 V 에 생기고 거기서 활성화가 끝난다.**
  즉 **첨가제가 활성화 완료 전위를 끌어내렸다.**
- 이 위키에 모인 "활성화 완료 전위" 값을 한 줄에 놓으면:

| 논문 | 활성화 전위 | 방식 | 무게 대가 |
|---|---|---|---|
| Cronk 2026 | `[인쇄]` **2.4 V** vs Li/Li⁺ | 밀링이 만든 thiophosphate interphase, **촉매 없음** | **0** |
| **Wan 2021 (이 논문)** | `[도표]` **≈2.80 V** vs Li/Li⁺ (평탄 plateau) | **LiI-LiBr 39.9 wt%** | **매우 큼** |
| Zhang 2026 | `[인쇄]` LSV 피크 **2.87 V**(PI3 계) / **3.05 V**(pristine) | PI3 → in-situ LiI + thiophosphate | **43.8 wt% PI3** |
| Lee 2026 | 3.62 V 컷오프까지 밀어붙임 | 없음 | 0 (대신 이론 초과 용량) |
| Yu 2024 | `[인쇄]` CV 활성화 피크 **2.14 V vs Li–In** | CuS 나노결정 호스트 | 호스트가 활물질만큼 무거움 |

  → `[해석]` **Wan 2021 의 2.80 V 는 Zhang 2026 의 2.87 V 와 거의 같다.** 두 논문 모두
  **요오드화물(LiI)** 이 들어 있다는 점에서 일관적이다. **그리고 둘 다 Cronk 의 2.4 V 보다 높다.**
  즉 "요오드 경로" 는 활성화 전위를 **2.8–2.9 V 까지만** 내리고, Cronk 의 "밀링 interphase 경로" 가
  더 낮다 — **무게 대가는 Cronk 가 0인데 결과가 더 좋다.**

### 5.5 ★★ 그리고 이 그림이 Zhang 2026 의 요오드 의심에 하는 말

Zhang 2026 digest 의 G6 는 이렇게 적혀 있다 — "LiI 전량 1 e⁻ 산화 몫 `[재현]` 152 mAh g⁻¹(Li2S)
가 첫 충전의 이론 초과분(≈164)과 크기가 맞아 요오드 산화환원이 Li2S 용량에 섞였을 가능성을
배제 못 한다."

**이 논문은 그 의심을 풀어주지 못한다. 오히려 같은 자리에 같은 구멍을 낸다.**

| 질문 | Wan 2021 의 답 |
|---|---|
| LiI-LiBr 의 용량 기여를 분리했는가 | **아니다** (G3). LiI-LiBr+카본만의 대조셀도, LiI 산화 전위 측정도 없다. |
| LiI 를 "활성 첨가제" 로 보는가 | **아니다 — 정반대로 불활성 사표로 본다.** `[인쇄]` "increasing the amount of LiI-LiBr can enhance the cycling stability and reaction kinetics. However, **it also reduces the total capacity**, so the molar ratio of LiI-LiBr to MoS2 is controlled at 1:2." → **첨가제가 늘면 용량이 준다**는 관측은 "첨가제는 용량을 내지 않는다" 와 **정합적**이다. |
| 그 관측이 의심을 해소하는가 | **부분적으로만.** `[해석]` 첨가제를 늘려 용량이 "준다" 는 것은 **분모(MoS2 질량)를 고정한 채 활물질 비율이 줄어서**일 수도 있다. 저자들은 어느 쪽인지 가르지 않았다. 요오드가 100 mAh g⁻¹ 급으로 기여하더라도 활물질 희석 손실이 더 크면 **같은 관측**이 나온다. |
| 수치로 보면 | `[재현]` Li2S:LiI-LiBr = 4:1 에서 LiI 1 e⁻ 몫 = 0.75 × 26801 / 183.79 = **109.4 mAh g⁻¹(Li2S)**. 관측된 첫 충전 ≈1165 중 **9.4 %** 에 해당한다. 그것을 빼면 Li2S 순 이용률은 **≈90.5 %** 로 내려간다. **어느 쪽인지 이 논문의 데이터로는 결정할 수 없다.** |

`[해석]` **결론: Zhang 2026 의 요오드 의심은 이 논문으로 해소되지 않고, 오히려 "같은 그룹 계보의
두 논문이 모두 같은 분리 실험을 빠뜨렸다" 는 사실로 강화된다.** 그리고 이 논문의 Fig. 2a 는
그 의심을 **가장 날카롭게 만드는 그림**이기도 하다 — **2.80 V 평탄 plateau 는 Li2S 의 산화
plateau 라기엔 너무 평탄하고 너무 길다**(이론용량의 거의 전부). 고체계 Li2S 의 첫 충전은
보통 경사지거나 과전압 봉우리를 동반하는데(Fig. 2b 가 바로 그 모습이다), 2a 는 **전형적인
매개체(mediator) 반응의 모양**이다. 그 매개체 후보가 바로 I⁻/I₃⁻ 다.
**논문은 "catalyzer" 라고만 쓰고 "mediator" 라는 단어를 한 번도 쓰지 않는다** (본문 0회).

### 5.6 Fig. 2c 라만 — Li–S 결합 약화 `[인쇄 + 도표]`

`[인쇄]` "Raman spectra of Li2S, Li2S@LiI, and Li2S@LiI-LiBr in Figure 2c shows that adding the
LiI-LiBr compound into Li2S induced a **red-shift for the Li−S bond** due to the reduced
interaction between Li⁺ and S²⁻,²¹ which can facilitate the delithiation of Li2S."

`[도표]` 세로 점선이 **≈372 cm⁻¹** 에 있고 bare Li2S 피크가 그 위다. Li2S@LiI 와 Li2S@LiI-LiBr 의
봉우리는 점선 **왼쪽 ≈365 cm⁻¹** 으로 밀려 있다 → **적색편이 ≈7 cm⁻¹**. 첨가제가 들어간
두 시료는 봉우리가 **훨씬 넓어지고 세진다**(비정질화·결함 증가와 정합).

`[해석]` 값을 본문에 안 적었다. ≈7 cm⁻¹ 는 **Li2S 의 ~372 cm⁻¹ 모드 기준 2 % 수준**이다.
그리고 **Li2S@LiI 와 Li2S@LiI-LiBr 사이의 차이는 그림에서 구별되지 않는다** — 즉 라만은
"할로겐화물을 넣으면 편이한다" 까지만 말하고 **"Br 을 더 넣으면 더 좋다" 는 말하지 못한다.**

### 5.7 Fig. 2d EIS — 이온 전도도 `[인쇄 + 도표]`

| 시료 | 이온 전도도 | 출처 |
|---|---|---|
| Li2S | **10⁻¹³ S cm⁻¹** | `[인쇄]` "It is reported that … ;²²" — **남의 문헌값 (ref 22, Lin 2013). 이 논문이 재지 않았다** (G15) |
| Li2S@LiI | **6.4 × 10⁻⁸ S cm⁻¹** | `[인쇄]` 이 논문 측정 |
| Li2S@LiI-LiBr | **1.08 × 10⁻⁶ S cm⁻¹** | `[인쇄]` 이 논문 측정 |

`[인쇄]` "the obtained Li2S@LiI-LiBr composite exhibits a **7 orders of magnitude increase** in
ionic conductivity (1.08 × 10⁻⁶ S cm⁻¹) compared with Li2S."

`[도표]` 나이퀴스트: Li2S@LiI 의 반원이 **Z′ ≈2×10⁶ Ω** 까지 뻗고, Li2S@LiI-LiBr 는
**≈0.4×10⁶ Ω 이내**에 머문다 (약 5배 축소).

`[재현]` **자기 데이터 안에서의 증가는 1.08×10⁻⁶ / 6.4×10⁻⁸ = 16.9배**(LiI → LiI-LiBr).
"7 orders" 는 자기 측정값 ÷ 남의 문헌값이다.

`[해석]` 더 중요한 맥락: **1.08×10⁻⁶ S cm⁻¹ 은 여전히 매우 낮다.** LPSCl 급 황화물 SE 는
10⁻³ S cm⁻¹ 대이므로 **아직 3자리 아래**다. 즉 LiI-LiBr 은 Li2S 를 "SE 처럼" 만들지 못했고,
**Li2S 입자 내부의 Li⁺ 수송을 바닥에서 조금 띄웠을 뿐**이다. 이 숫자를 우리가 인용할 때는
**"Li2S 자체의 이온전도도" 이지 "복합양극의 이온전도도" 가 아니다**라는 점을 반드시 붙여야 한다.

---

## 6. Figure 3 — DFT (Li2S-I-Br 계)

> `[인쇄]` 캡션: "DFT calculations of the Li2S-I-Br system. (a) Defect formation energies in Li2S.
> (b) Crystal orbital Hamilton population (COHP) of the Li−S bond in Li2S bulk and around complex
> defects. (c) Defect formation energies in LiI. (d) Defect formation energies in Li4I3Br."

### 6.1 Fig. 3a 결함 형성에너지 (Li2S) `[인쇄 + 도표]`

`[인쇄]` "the **Li vacancies (V_Li) are the main intrinsic defects in Li2S**. With incorporating
LiBr in Li2S, **Li vacancies along with Br-on-S substitution (complex defect)** will be formed.
The **formation energy of this complex defect is even lower than that of intrinsic Li vacancies**.
For the LiI incorporation, the complex defect of Li vacancies along with I-on-S substitution is
also one of the most possible states. These complex defects are mainly due to **valence
inconsistencies between Br/I and S**. Therefore, a small amount of Br and I doped into Li2S will
generate complex defects in Li2S, **increasing the Li-ion conductivity**."

`[도표]` 범례 6개: Br_S, I_S, Vac_Li, Vac_S, **Vac_Li+Br_S**, **Vac_Li+I_S**. 가로축 Fermi
energy (eV), 세로축 Defect Formation Energy (eV). 두 굵은 점선이 밴드 가장자리(0 과 ≈3.4 eV),
점쇄선이 ≈1.8 eV. `[도표]` **Vac_Li+Br_S(갈색)와 Vac_Li+I_S(회색)가 넓은 Fermi 구간에서
0 eV 선 근처에 납작하게 깔린다** — 고유 Vac_Li(분홍, 별이 ≈1.2 eV)보다 낮다.

### 6.2 Fig. 3b COHP — Li–S 결합 `[인쇄 + 도표]`

`[인쇄]` "the **bonding state of the Li−S bond around complex defects decreases and reduces the
integral COHP value**. Therefore, Br/I incorporation can effectively improve the decomposition of
Li2S, implying Br/I incorporation can **promote the Li2S/S reaction**."

`[도표]` **범례에 ICOHP 값이 인쇄되어 있다 (본문에는 없다)**:

| 계 | ICOHP |
|---|---|
| Li–S_bulk | **1.66 eV** |
| Li–S_(Vac_Li + Br_S) | **1.59 eV** |
| Li–S_(Vac_Li + I_S) | **1.61 eV** |

`[재현]` 감소폭 **0.07 eV (4.2 %, Br)** / **0.05 eV (3.0 %, I)**.

`[해석]` **이것이 이 논문의 "strong Li–S bond 를 약화한다" 주장의 전부이고, 크기는 3–4 % 다.**
본문이 eV 값을 인쇄하지 않은 선택(G18)이 이 크기를 가린다. 3–4 % 결합 약화가
Fig. 2a 의 1.29배 첫 충전 용량 차이를 설명하는지는 **논문이 연결하지 않는다** —
NEB 로 산화 장벽을 계산한 것도 아니다(Huang 2026 은 NEB 0.20 vs 0.25 eV 를 제시한다).

### 6.3 Fig. 3c,d — 왜 LiI 단독이 아니라 LiI-LiBr 인가 `[인쇄 + 도표]`

`[인쇄]` "Besides, **Li4I3Br shows lower intrinsic Li vacancy formation energy than that of LiI**
(Figure 3c,d), implying Br incorporation can also improve the Li-ion conductivity of LiI, thus
improving the ionic conductivity of the Li2S@LiI-LiBr composite."

`[도표]` Fig. 3c (LiI): Vac_Li(청록) 별이 ≈**0.8 eV**, Vac_I(회색) 별이 ≈**3.2 eV**.
Fig. 3d (Li4I3Br): Vac_Li 두 곡선(청록·보라)이 겹쳐 별이 ≈**0.8 eV**, Vac_Br(주황) ≈2.9 eV,
Vac_I(회색) ≈3.3 eV.

`[해석]` **두 별의 높이가 그림에서 구별되지 않는다**(둘 다 ≈0.8 eV). 본문은 "lower" 라고만
쓰고 값을 안 준다. **즉 "왜 LiI 단독이 아니라 LiI-LiBr 인가" 에 대한 계산 근거는 그림으로
검증되지 않는다.** 실험 근거(Fig. 2d 의 16.9배, Fig. S4/S5 의 조성 최적화)가 더 강하다.
그리고 **Li4I3Br 라는 상이 실제로 생겼다는 실험 증거가 없다**(G17) — XRD 는 아무것도 못 봤다.

### 6.4 DFT 방법론

**본문에 계산 조건이 한 줄도 없다** (범함수·컷오프·k-point·슈퍼셀·화학퍼텐셜 기준 전부).
Methods 가 SI 에 있고 SI 미확보. → `[해석]` 결함 형성에너지는 **화학퍼텐셜 기준(Li-rich/S-rich)**에
따라 수 eV 씩 움직이는 양인데, 그 기준이 명시되지 않으면 **Fig. 3a 의 절대 높이는 인용할 수 없다.**
우리가 쓸 수 있는 것은 **같은 그림 안의 상대 순서**뿐이다.

---

## 7. Figure 4 — MoS2 계 전기화학 (본류)

`[인쇄]` 조건: "All the batteries are cycled at a cutoff voltage of **0.5−3 V (vs. Li/Li⁺) in the
first cycle** and then tested at a cutoff voltage of **1.0−2.8 V (vs. Li/Li⁺) in the following
cycles** at a current density of **200 mA g⁻¹**."

### 7.1 Fig. 4a–c 충방전 곡선 (1–3 사이클) `[도표]`

**방전 선행**(MoS2 양극). 세로축 0.5–3.0 V, 가로축 0–1200 mAh g⁻¹.

| 시료 | 1차 방전 | 1차 충전 | 1차 CE `[재현]` | 2·3차 방전 |
|---|---|---|---|---|
| (a) MoS2 | **≈470** | **≈300** | ≈64 % | **≈170** |
| (b) MoS2@LiI-LiBr | **≈790** | **≈700** | ≈89 % | **≈400** |
| (c) MoS2@LiI-LiBr@C | **≈1150** | **≈1000** | ≈87 % | **≈560–600** |

`[도표]` 1차 방전 곡선 모양: (a) 는 ≈1.1 V 에 짧은 어깨 뒤 0.5 V 로 급락; (b),(c) 는
≈1.1 V 어깨가 길고 0.5 V 바닥 구간이 넓다 — **(c) 가 가장 길다.**
과전압(2·3사이클 충·방전 곡선 간격)은 `[도표]` **(a) ≫ (b) > (c)** 순으로 좁아진다.

`[인쇄]` "the overpotential for the MoS2@LiI-LiBr cathode is **smaller** than that of MoS2. …
After introducing carbon, the overpotential **further decreased** for MoS2@LiI-LiBr@C."

### 7.2 Fig. 4d 100 사이클 (200 mA g⁻¹) `[인쇄 + 도표]`

| 시료 | `[인쇄]` 100사이클 값 | `[도표]` 그림 판독 (시작 → 100사이클) |
|---|---|---|
| MoS2@LiI-LiBr@C | **437.8** mAh g⁻¹(MoS2@LiI-LiBr) = `[재현]` **604.8** mAh g⁻¹(MoS2) | ≈**600** → ≈**480** |
| MoS2@LiI-LiBr | (본문 수치 없음) | ≈**460** → ≈**330** |
| MoS2 | **110.7** mAh g⁻¹ (분모 미기재) | ≈**175** → ≈**130** |

`[해석]` **그림의 분모가 무엇인지 캡션·축·본문 어디에도 없다** (G1 의 연장). 437.8 로도
604.8 로도 그림의 ≈480 과 맞지 않는다. **이 그림에서 읽은 값은 인용하지 말고, 인쇄된
437.8(및 그 환산 604.8)만 쓰는 것이 안전하다.**
그리고 **CE 축이 없다** (G6) — 전고체 Li–S 에서 CE 없이 "100 사이클 유지" 를 말하는 것은
이 위키의 규율상 "안정" 의 정체를 판정할 수 없다는 뜻이다.

### 7.3 Fig. 4e–g SEM `[인쇄 + 도표]`

`[인쇄]` "For both MoS2 (Figure 4e) and MoS2@LiI-LiBr (Figure 4f), a **micrometer sized sheet with
thickness of several nanometers** was observed. After carbon black was introduced during
ball-milling, the particle size of obtained MoS2@LiI-LiBr@C was **significantly reduced from the
microscale to the nanoscale** (Figure 4g)."

`[도표]` 세 이미지 모두 스케일바 **1 µm**. (e) 는 수 µm 급 판상 결정이 뚜렷, (f) 는 판상이
뭉개지고 응집, (g) 는 **≈100–200 nm 급 입자 덩어리**로 완전히 바뀌었다.

`[해석]` ★★ **이것이 이 논문에서 가장 과소평가된 사실이다.** 카본블랙을 넣은 2차 밀링이
**입도를 µm → nm 로 바꿨다.** 즉 MoS2@LiI-LiBr@C 와 MoS2 사이에는 **첨가제·탄소·입도** 세 변수가
모두 다르다. 그런데 Fig. 5 의 b 값 비교(촉매 증명)는 **이 두 시료를 비교한다** (G8).
`[해석]` **"카본블랙이 전자 경로를 준다" 와 "2차 밀링이 입도를 줄인다" 를 가르는 실험이 없다** —
이것은 우리 [[one-step-vs-two-step-mixing]] 의 질문 그 자체다. 이 논문은 **2단계 밀링을
썼고, 2단계째가 입도를 바꿨다**는 것을 SEM 으로 보여주면서도 그 효과를 분리하지 않았다.

### 7.4 조성 최적화 (전부 SI 그림, SI 미확보) `[인쇄]`

| 변수 | 결과 `[인쇄]` | 출처 |
|---|---|---|
| LiI:LiBr 몰비 | **100:0 과 50:50 모두 75:25 보다 가역용량이 낮다** → 최적 **75:25** | Figure S4, S5 — **SI 미확보** |
| LiI-LiBr : 활물질 | MoS2 는 2:1, Li2S 는 4:1 (같은 LiI-LiBr/S 몰비). **"Since only partial MoS2 was converted into Li2S, the ratio of LiI-LiBr to Li2S in MoS2@LiI-LiBr is high."** | 본문 |
| 그 결과 | "after the initial activation process, the **capacity retention for Li2S@LiI-LiBr was only 79.7 %, while for MoS2@LiI-LiBr, the capacity retention was 94.7 % after 30 cycles**" | Figure S6 — **SI 미확보** |
| 저항 | "the charge transfer resistance of the MoS2@LiI-LiBr‖Li cell was **much lower** than that of the Li2S@LiI-LiBr‖Li cell after cycling" | Figure S7 — **SI 미확보** |
| 전압창 | "when the battery was cycled at **0.5−3.0 V in all discharge/charge processes** to increase the Li2S amount, the capacity of the MoS2@LiI-LiBr@C‖Li cell **decreased rapidly after 30 cycles**" | Figure S8 — **SI 미확보** |
| 저자 결론 | "increasing the amount of LiI-LiBr can **enhance the cycling stability and reaction kinetics**. However, it also **reduces the total capacity**, so the molar ratio of LiI-LiBr to MoS2 is controlled at **1:2**." | 본문 |

`[해석]` ★ **79.7 % vs 94.7 % 가 이 논문에서 우리에게 가장 불리한 숫자다.**
LiI-LiBr 의 상대량이 **더 많은** Li2S@LiI-LiBr 쪽이 **더 빨리 죽는다.** 저자들은 이것을
"MoS2 쪽은 LiI-LiBr/Li2S 비가 높아서 좋다" 로 읽지만, `[해석]` 같은 데이터는
**"Li2S 를 직접 양극으로 쓰면 이 촉매로도 수명이 안 나온다"** 로도 읽힌다.
그리고 **0.5–3.0 V 전 구간 사이클이 30 사이클 만에 급락한다**(Fig. S8)는 것은
**Li2S 를 많이 만들수록 셀이 빨리 죽는다**는 뜻이다 — 우리처럼 **Li2S 가 100 % 활물질인 계**에는
직접적인 경고다.

---

## 8. Figure 5 — 속도론(b 값)과 로딩

### 8.1 b 값 해석 `[인쇄]`

> "the relationship between peak current (i) and scan rate (v) follows the equation
> **log(i) = b log(v) + log(a)**. When the b value equals **0.5**, the electrochemical reaction is
> an ideally **diffusion-controlled** process, whereas **b = 1.0** indicates a **surface-controlled**
> process, and when the b value lies between 0.5 and 1.0, the electrochemical reactions involve
> both processes."

`[도표]` Fig. 5e 표 전문:

| b value | MoS2 | MoS2@LiI-LiBr@C |
|---|---|---|
| R1 (S → Li2S) | **0.5292** | **0.8073** |
| R2 | – | – |
| O2 (Li*x*MoS2 → MoS2) | **0.5734** | **0.8011** |
| O1 (Li2S → S) | **0.5173** | **0.7877** |

`[인쇄]` "the b value of **O1 is low in both** MoS2 and MoS2@LiI-LiBr@C cathodes, implying
**reaction O1, where Li2S was oxidized to S, is the rate-determining step**."

`[인쇄]` 그리고 두 문장이 충돌한다 (G8):
1. "implying the surface-controlled process dominates in the MoS2@LiI-LiBr@C cathode **due to the
   reduced particle size**."
2. "The significantly improved b value for reaction O1 in the MoS2@LiI-LiBr@C cathode **further
   proved the catalytic effect of LiI-LiBr** on the Li2S/S redox reaction."

`[해석]` **같은 숫자를 두 원인에 동시에 귀속했다.** 입도 효과를 배제하려면 MoS2@C(첨가제 없이
같은 2차 밀링) 대조가 필요한데 없다.
그러나 **"Li2S → S 산화가 율속 단계" 라는 결론 자체는 두 시료 모두에서 O1 이 가장 낮다는
내부 비교로 서므로 비교적 견고하다** — 그리고 그것이 우리 H1 과 같은 말이다.

`[도표]` CV 전류 규모: Fig. 5a(MoS2@LiI-LiBr@C) 세로축 ±12×10⁻⁴ A cm⁻², Fig. 5b(MoS2) ±3×10⁻⁴.
**같은 scan rate 에서 피크 전류가 약 4–5배 차이** — 축 자체가 4배 다르다는 점을 주의해 읽어야 한다.

### 8.2 Fig. 5f,g 로딩 시험 `[인쇄 + 도표]`

**모든 값의 분모는 `[인쇄]` "based on the mass of MoS2"** (캡션에 명시).

| 로딩 (MoS2) | 전류 | 면적용량 `[인쇄]` | 초기 가역용량 `[인쇄]` | 20사이클 후 `[인쇄]` | `[재현]` 이론 대비 (÷669.7) |
|---|---|---|---|---|---|
| **0.922** mg cm⁻² | 100 mA g⁻¹ | **0.87** mAh cm⁻² | (초록 816.2) | **819.6** | **122 %** |
| 0.922 | 200 mA g⁻¹ | – | – | **711.3** | 106 % |
| **1.844** | 200 | **1.15** | **626.3** | **546.6** | 94 % |
| **4.058** | 200 | **2.02** | **498** | **255.9** | 74 % |

`[재현]` 면적용량 교차검증: 626.3 × 1.844 mg = **1.155 mAh cm⁻²** ✓ / 498 × 4.058 = **2.021** ✓ /
**816.2 × 0.922 = 0.753 ≠ 0.87** ✗ — 0.87 에 대응하는 비용량은 **0.87/0.922 = 943.6 mAh g⁻¹(MoS2)**
이고, 이는 `[도표]` Fig. 5g 의 1사이클 값(≈930–940)과 일치한다. → **면적용량은 1사이클 기준,
816.2/819.6 은 20사이클 기준이다. 초록이 둘을 한 문장에 섞었다** (G13).

`[도표]` Fig. 5g 20사이클 추이: 0.922@100 ≈930 → ≈810 (유지 ≈87 %) · 0.922@200 ≈800 → ≈705 (≈88 %) ·
1.844@200 ≈625 → ≈545 (≈87 %) · 4.058@200 ≈490 → ≈255 (**≈52 %**).
→ `[해석]` **로딩 4 mg cm⁻² 에서 20 사이클 만에 절반이 날아간다.** 이 논문의 "고로딩 2 mAh cm⁻²"
주장은 **초기 1~2 사이클의 숫자**이고 수명은 따라오지 않는다. 100 사이클 데이터는
**가장 낮은 로딩(0.922 mg cm⁻²)에서만** 제시된다.

### 8.3 이론용량 초과 (G14 상술) `[재현]`

MoS2 의 4 e⁻ 이론용량 = 4 × 26801 / 160.07 = **669.7 mAh g⁻¹(MoS2)**.
(첫 사이클 후 활물질이 S 로 바뀌어도 MoS2 1몰당 S 2몰 × 2 e⁻ = 같은 4 e⁻ → 상한 불변.)

| 보고값 | 이론 대비 | 설명 가능한가 |
|---|---|---|
| 943.6 (면적 환산, 1사이클) | **141 %** | LiI+LiBr 1 e⁻ 전량 `[재현]` 83.7 을 더해도 753 — **못 메운다** |
| 819.6 (20사이클, 100 mA g⁻¹) | **122 %** | 〃 |
| 816.2 (초록) | **122 %** | 〃 |
| 604.8 (100사이클, MoS2 기준) | 90 % | 이론 내 |

`[해석]` 1사이클이 이론을 40 % 넘는 것은 **0.5 V 심방전에서의 SE·카본 환원(비가역)** 으로
흔히 설명되지만, **20사이클째에도 122 % 가 유지되는 것은 그렇게 설명되지 않는다.**
남는 후보는 **황화물 SE 자신의 가역 리독스**(Cronk 2026 이 LPSCl+AB 대조셀로 환원 115 /
산화 355 mAh g⁻¹ 를 측정했다)와 **요오드 리독스**다. **논문은 둘 다 검토하지 않는다.**
→ 이 위키의 규율대로, **이 논문의 MoS2 비용량 수치는 "활물질 용량" 으로 인용하면 안 된다.**

---

## 9. p.6 — 결론과 확장

`[인쇄]` "we demonstrated that the redox kinetics of Li2S in solid-state batteries can be
significantly enhanced by LiI-LiBr due to its **high catalytic activity and improved ionic
conductivity to Li2S**. After ball-milling carbon black and MoS2@LiI-LiBr, the **reduction of the
particle size** of MoS2@LiI-LiBr and the enhancement of electronic conductivity further enhance the
MoS2 reversibility and kinetics."

`[인쇄]` 확장: "Such a universal design principle can also be employed in the **FeS2@S@LiI-LiBr**
composite … a reversible discharge capacity of **795.0 mAh g⁻¹** was maintained after **10 cycles**
at a current density of 150 mA g⁻¹, which is higher than the capacity of FeS2@S that was reported
in our previous work.²⁶" (Figure S9 — **SI 미확보**; ref 26 = Mwizerwa et al., *ACS Appl. Mater.
Interfaces* **12** (2020) 18519)

`[해석]` 확장 실험은 **10 사이클**이다. "universal design principle" 이라는 표현의 근거로는 약하다.
그리고 FeS2 역시 전이금속 황화물이어서 **Li2S 를 직접 양극으로 쓴 확장은 끝내 없다.**

---

## 10. SI 인용 지점 목록 (전부 미확보)

| SI 항목 | 본문이 그것으로 주장하는 것 | 본 digest 의 처리 |
|---|---|---|
| Experimental Section | 합성·셀 조립·측정 전부 | **SI 미확보** → G2·G9·G10·G11 |
| Figure S1 | Li2S@LiI-LiBr 의 XRD | SI 미확보 |
| Figure S2 | 사이클 후 Li2S@LiI-LiBr 의 전하이동 저항 < Li2S | SI 미확보 (본문 한 문장만) |
| Figure S3 | 100사이클 후 MoS2@LiI-LiBr‖Li 의 저항 ≪ MoS2‖Li | SI 미확보 |
| Figure S4 / S5 | LiI:LiBr = 100:0 / 50:50 이 75:25 보다 나쁨 | SI 미확보 — **"75:25 가 최적" 의 유일한 근거** |
| Figure S6 | 30사이클 유지율 Li2S@LiI-LiBr **79.7 %** vs MoS2@LiI-LiBr **94.7 %** | SI 미확보 (수치는 본문에 인쇄됨) |
| Figure S7 | MoS2@LiI-LiBr 의 전하이동 저항 ≪ Li2S@LiI-LiBr | SI 미확보 |
| Figure S8 | 0.5–3.0 V 전 구간 사이클은 30사이클 후 급락 | SI 미확보 (수치 없음) |
| Figure S9 | FeS2@S@LiI-LiBr 795.0 mAh g⁻¹ / 10 사이클 | SI 미확보 |
| Table S1 | MoS2·TiS2·FeS2 계 ASSB 문헌 비교 | SI 미확보 |

`[해석]` **SI 를 구하면 반드시 다시 볼 것**: (1) Experimental 의 **SE 이름·온도·스택압**,
(2) Figure S1 의 Li2S@LiI-LiBr XRD — **Li4I3Br 상이 보이는가**(G17 의 직접 판정),
(3) Figure S6 의 Li2S 계 30사이클 곡선 — **첫 충전 이후 거동**,
(4) Figure S4/S5 의 조성 최적화 곡선.
단 **G1·G3·G6·G8·G14·G16 은 SI 로도 안 메워진다** — 설계가 빠뜨린 실험이기 때문이다.

---

## 11. ★ 촉매파 vs 무촉매파 — 이 위키 안의 대립

`[해석]` 이 digest 를 넣으면서 이 위키의 Li2S 활성화 처방이 **두 진영**으로 정리된다.

### 11.1 촉매·첨가제파 (무게를 내주고 kinetics 를 산다)

| 논문 | 첨가제 | 양 | 주장 근거 | 무게 대가 |
|---|---|---|---|---|
| **Wan 2021 (이 논문)** | LiI-LiBr (75:25 몰) | Li2S 계 **39.9 wt%** / MoS2 계 **27.6 wt%** `[재현]` | 라만 적색편이 · 분말 EIS 16.9배 · DFT(결함·COHP 3–4 %) · CV b 값 | **매우 큼** |
| Zhang 2026 | PI3 → in-situ LiI + thiophosphate | **43.8 wt%** | LSV 피크 3.05 → 2.87 V · 분말 전도도 | 매우 큼 |
| Yu 2024 | CuS 나노결정 / N-도핑 탄소 호스트 | 호스트가 활물질과 동급 질량 | DFT 흡착·장벽 · Tafel · CV 피크 2.41 → 2.14 V vs Li–In | 큼 (+ 첫 CE 110–113 %, Li 재고 손실) |
| Huang 2026 | 고엔트로피 황화물 | **6 wt%** | 토모그래피 · DC 분극 · GITT · NEB 0.20 vs 0.25 eV | 작음 |

### 11.2 무촉매파 (공정으로 만든다)

| 논문 | 수단 | 주장 근거 | 무게 대가 |
|---|---|---|---|
| **Cronk 2026** | one-step 고에너지 밀링이 황 표면에 **Li3PS4+n interphase** 를 만든다. `[인쇄]` "**without requiring the use of catalysts or kinetic promoters**" | Raman 152→149 cm⁻¹ · XANES pre-edge/LCF · EDS 라인스캔 · cryo-TEM · dQ/dV 4영역 분해 | **0** (기존 성분만 씀) |

### 11.3 판정

`[해석]`
1. **활성화 전위로 보면 무촉매파가 이긴다.** Cronk **2.4 V** < Wan **≈2.80 V** ≈ Zhang **2.87 V**.
   요오드 계열이 더 비싼 값을 치르고 더 높은 전위에 머문다.
2. **증거의 질로도 무촉매파가 앞선다.** Cronk 는 **기여 분해(dQ/dV 4영역 + XANES LCF 로 S /
   interphase / LPSCl = 83 / 7.5 / 9.2 %)** 를 했다. Wan 2021 은 **사후 분석이 0건**이고
   첨가제 기여 분리도 0건이다 (G3, G16).
3. **그러나 촉매파가 주는 것이 하나 있다 — "Li2S 입자 내부" 를 건드리는 유일한 경로다.**
   Cronk 의 interphase 는 **활물질 표면**을 바꾸고, Wan 의 I/Br 치환은 **Li2S 격자 내부**의
   Li 공공을 만든다(Fig. 3a). 두 처방은 **배타적이지 않다.**
   `[해석]` **가장 값싼 다음 수는 "Cronk 의 one-step 밀링 + 소량 LiI" 의 교차**다 —
   Wan 의 39.9 wt% 가 아니라 **Huang 급 수 wt%** 로.
4. **공통의 구멍**: 네 논문 모두 **첨가제/SE 자신의 용량 기여를 분리한 것은 Cronk 뿐**이다.
   나머지 셋은 전부 이론용량 초과를 내면서 설명하지 않는다 (Wan G14, Zhang G6, Yu G8).

---

## 12. 우리 연구와의 접점 (이식 가능 / 불가)

### 12.1 이식 가능

| 가져갈 것 | 이 논문의 근거 | 우리 쪽 연결 | 주의 |
|---|---|---|---|
| **할로겐화물이 Li2S 첫 충전 plateau 를 만든다** — 없으면 plateau 자체가 없다 | `[도표]` Fig. 2a/2b 직접 비교 | [[li2s-activation-first-charge]] · [[reference-cell-500-600-mahg]] **H1** | 전압값(2.80 V)은 SE 미상(G2)·컷오프 3.5 V(G5) 조건의 값 |
| **Li2S 격자에 I/Br 를 넣으면 Li 공공 복합결함이 생긴다** (기전 가설) | `[인쇄 + 도표]` Fig. 3a, COHP 1.66 → 1.59/1.61 eV | [[li2s-activation-first-charge]] 의 "왜 할로겐인가" | 계산 조건 미기재(§6.4), Li4I3Br 실험 미확인(G17), 효과 크기 3–4 % |
| **Li2S 자체의 이온전도도 실측값** 6.4×10⁻⁸(@LiI) / 1.08×10⁻⁶(@LiI-LiBr) S cm⁻¹ | `[인쇄]` Fig. 2d | [[interface-quality-not-bulk-conductivity]] 의 반례 검토 | bare Li2S 는 **남의 문헌값**(G15). **복합양극 전도도가 아니다** |
| **"Li2S → S 산화가 율속 단계"** (b 값 O1 이 양쪽 다 최저) | `[도표]` Fig. 5e | H1 | 절대값은 시료 간 비교라 약함 |
| **조성 최적화의 방향** — LiI 단독(100:0)도 50:50 도 75:25 보다 나쁘다 | `[인쇄]` (근거 그림은 SI 미확보) | 첨가제 설계 | 근거 미확인 |
| **첨가제를 늘리면 kinetics↑·총용량↓ 의 트레이드오프가 실재한다** | `[인쇄]` 본문 | 우리 복합양극 무게 배분 | 그 "총용량 감소" 가 희석 때문인지 미분리(G3) |
| **2단계 밀링의 2차가 입도를 µm → nm 로 바꾼다** | `[도표]` Fig. 4e–g SEM | [[one-step-vs-two-step-mixing]] · [[composite-cathode-mixing-routes]] | **조건이 전부 미기재**(G10) — 방향만 가져온다 |

### 12.2 이식 불가

| 못 가져갈 것 | 이유 |
|---|---|
| **MoS2 계의 모든 용량 수치** (816.2 / 819.6 / 711.3 / 626.3 / 546.6 / 498 / 437.8 / 604.8 / 255.9 / 110.7) | 활물질이 MoS2 다. 분모가 MoS2 또는 MoS2@LiI-LiBr 이고 Li2S 환산이 **물리적으로 성립하지 않는다** (몰비 2 S/MoS2 이지만 활물질 정체가 다르다). 게다가 상당수가 이론용량 초과(G14) |
| **전압 프로토콜 0.5–3.0 V → 1.0–2.8 V** | MoS2 의 2단계 리튬화에 맞춘 창이다. 우리 Li2S 셀에 0.5 V 심방전은 SE 를 환원 분해시킨다 |
| **"LiI-LiBr 을 넣으면 수명이 좋아진다"** | **Li2S 양극에서는 반대다** — `[인쇄]` Li2S@LiI-LiBr 30사이클 유지 **79.7 %** < MoS2@LiI-LiBr **94.7 %**. 그리고 Li2S 를 많이 만드는 전압창(0.5–3.0 V 전 구간)에서는 30사이클에 급락(Fig. S8) |
| **Li 금속 음극 결과** | 우리는 Li–In → anode-free 다. 이 논문의 Li 금속은 Li 재고 무한 공급이라 **첫 CE·Li 재고 수지를 전혀 시험하지 않는다** — anode-free 로 옮길 근거가 0 |
| **첨가제 39.9 wt% 라는 양** | 우리 reference cell 은 Li2S:LPSCl:AB = 30:50:20 이다. 여기에 40 wt% 첨가제를 넣을 자리가 없다. 넣으려면 SE 나 탄소를 빼야 하고 그러면 다른 실험이 된다 |
| **"catalyst" 라는 명명** | 촉매의 정의를 보인 실험이 없다(G16). 우리 위키에서는 **"할로겐화물 첨가제"** 로 부르고, 촉매/매개체/전도보조 중 무엇인지는 **미결**로 둔다 |

### 12.3 질문 카드 라우팅

| 카드 | 가설 | 이 논문이 주는 것 | 방향 |
|---|---|---|---|
| [[reference-cell-500-600-mahg]] | **H1 (활성화 — 재정의판: 활성화 완료 전위 > SE 산화 전위)** | `[도표]` Fig. 2a/2b — **첨가제 없는 Li2S 는 첫 충전 plateau 가 없고 3.5 V 까지 끌려간다 / LiI-LiBr 은 2.80 V 평탄 plateau 를 만든다.** 고체계 Li2S 양극의 직접 대조다 | **Evidence For (H1)** |
| [[reference-cell-500-600-mahg]] | **H4 (단위 착시)** | `[재현]` 437.8 ↔ 604.8 이 **같은 데이터의 두 분모**라는 실례. 그리고 이론용량 초과 122 % | **Evidence For (H4)** — "분모를 바꿔 1.38배" 의 교과서 사례 |
| [[reference-cell-500-600-mahg]] | H3 (입자) | `[도표]` Fig. 4e–g: 2차 밀링이 µm → nm. 단 **입도만 바꾼 대조가 없어** 효과 크기를 못 준다 | 중립 (G8 로 기록) |
| [[one-step-vs-two-step-mixing]] | — | **2단계 밀링**(활물질+첨가제 → +탄소)을 썼고 2차가 입도를 바꿨다는 SEM 증거. 단 조건 전무 | 약한 For (two-step 의 2차가 입도 기능을 겸한다) |
| [[anode-free-li2s-assb]] | — | **근거 없음.** Li 금속 음극이라 Li 재고 수지를 시험하지 않았고 CE 가 보고되지 않았다(G6) | 공백으로 기록 |
| [[li2s-activation-first-charge]] | — | "활성화를 돕는 네 번째 방식" 이 아니라 **Zhang 2026 과 같은 요오드 경로의 2021년 원형**. 계보를 잇는다 | 개념 갱신 |

### 12.4 가장 값싼 다음 실험 `[해석]`

1. **LiI 소량(3–7 wt%) × 우리 one-step 밀링.** Wan 의 39.9 wt% 가 아니라 Huang 급 소량으로
   Li2S:LPSCl:AB = 30:50:20 에 얹고, **첫 충전 plateau 가 2.8 V 에 생기는지**만 본다.
   비교 대상은 우리 pristine 기준선 — 0.1 C, 같은 컷오프.
2. **대조셀 하나를 반드시 같이 돌린다: LiI + LPSCl + AB (활물질 없이).**
   이것이 Wan 2021·Zhang 2026 이 **둘 다 빠뜨린** 실험이고, `[재현]` 100 mAh g⁻¹ 급 요오드
   기여가 실재하는지 한 셀로 판정된다. Cronk 가 LPSCl+AB 대조셀로 한 것과 같은 수법이다.
3. **첫 충전 컷오프를 2.9 V / 3.2 V / 3.6 V 로 나눠 본다.** Wan(3.5 V) · Zhang(3.0 V) ·
   Lee(3.62 V) 가 서로 다른 컷오프를 쓰고 있어 비교가 안 된다 — 우리 셀에서 한 번 가른다.

---

## 13. 비판 (이 digest 의 판단)

1. **"촉매" 를 주장하면서 촉매임을 보이는 실험이 없다.** 사후 분석(XRD·XPS·라만)이 0건이라
   LiI-LiBr 이 사이클 후에도 그대로인지 알 수 없다. **XPS 0회, in situ/operando 0회,
   TEM·EDS 0회.** 기전 증거 다섯 갈래(라만·EIS·DFT·b 값·성능)가 **전부 간접**이고, 그중
   라만·EIS·DFT 는 **셀이 아니라 분말**에서 나왔다. 그 결과 **촉매 / 리독스 매개체 /
   이온 전도 보조상**이 구분되지 않는다. 특히 Fig. 2a 의 **2.80 V 평탄 plateau 는
   매개체 반응의 전형적 모양**인데 논문은 "mediator" 라는 단어를 한 번도 쓰지 않는다.

2. **촉매 증명의 핵심 데이터가 세 변수를 동시에 바꾼 비교다.** Fig. 5 의 b 값은
   MoS2(마이크로·무첨가·무탄소) vs MoS2@LiI-LiBr@C(나노·첨가·탄소)를 비교한다. 논문 자신이
   b 값 상승을 **"due to the reduced particle size"** 라고 쓴 뒤 같은 데이터로 촉매를
   "further proved" 한다 — **자기모순**이다. MoS2@C 대조가 없다.

3. **용량이 이론을 넘는데 언급이 없다.** `[재현]` MoS2 4 e⁻ = 669.7 mAh g⁻¹(MoS2) 인데
   보고값이 816.2 / 819.6 (**122 %**), 면적 환산 943.6 (**141 %**) 이다. 할로겐 1 e⁻ 전량
   (83.7)을 더해도 못 메운다. 황화물 SE 의 리독스·0.5 V 심방전의 SE 환원을 **검토조차
   하지 않았다.** 이 위키의 규율("이론 초과를 보면 SE redox 를 먼저 의심한다")이 그대로 걸린다.

4. **분모를 경고 없이 바꿔 같은 데이터를 1.38배로 보이게 한다** (437.8 → 604.8, G1).
   본문과 초록이 2쪽 차이로 다른 분모를 쓴다. 독자가 `[재현]` 0.7239 를 직접 계산해야
   같은 데이터임을 안다.

5. **CE 가 없다 — 숫자로도 그래프 축으로도.** 전고체 Li–S 에서 CE 없이 "100 사이클 유지" 를
   말하면 "안정" 이 용량인지 효율인지 가를 수 없다. 이 위키 9편 중 이 논문만 **판정 자체가
   불가능**하다.

6. **고체전해질이 무엇인지 안 적혀 있다** (G2). 전고체 논문의 가장 기본 정보이고, 이것 없이는
   0.5 V 심방전도 3.5 V 충전도 해석할 수 없다. 온도·스택압·셀 치수도 전부 없다. (SI 에 있을
   가능성이 높지만, **본문만으로 재현 불가**라는 사실은 그대로다.)

7. **고로딩 주장이 수명으로 받쳐지지 않는다.** 100 사이클 데이터는 **0.922 mg cm⁻²** 하나뿐이고,
   4.058 mg cm⁻² 는 `[도표]` **20 사이클에 52 %** 로 반 토막 난다. 초록의 "At a high areal
   capacity of 2 mAh cm⁻², the battery still delivers reversible capacity of 498 mAh g⁻¹" 은
   **1~2 사이클 값**이다.

8. **DFT 수치를 본문에 하나도 인쇄하지 않았다** (G18). ICOHP 1.66 → 1.59/1.61 eV 를 범례에서만
   읽을 수 있고, 그 크기는 **3–4 %** 다. 계산 조건(범함수·화학퍼텐셜 기준)도 본문에 없어
   절대값 인용이 불가능하다. "Li4I3Br 가 LiI 보다 낫다" 는 그림에서 **구별되지 않는다.**

9. **제목이 내용보다 넓다.** "Solid State Li2S/S Reactions" 라고 썼지만 Li2S 를 활물질로 쓴
   실험은 **Figure 2 한 장(+SI S1·S2·S6·S7)** 뿐이고, 그 결과는 오히려 **Li2S 양극이 더 빨리
   죽는다**(30사이클 79.7 %)는 쪽이다. 본문 7쪽 중 Li2S 양극에 할애된 분량은 한 문단이다.

10. **셀 개수·오차·재현성 전무**(G12). 모든 곡선이 단일 셀로 보인다.

---

## 14. 이 저장소가 가져갈 것 (한 줄 요약)

| # | 가져갈 것 |
|---|---|
| 1 | **고체계에서 pristine Li2S 의 첫 충전은 plateau 자체가 없다** (`[도표]` Fig. 2b: 2.5 → 3.5 V 단조 상승, ≈900 mAh g⁻¹(Li2S) = 이론의 77 %). **할로겐화물을 넣으면 2.80 V 평탄 plateau 가 생기고 ≈1165 (≈100 %) 까지 간다.** → H1 의 고체계 직접 근거 하나 추가. |
| 2 | **Li2S 양극 첫 사이클 CE `[재현]` 72 %(첨가제) / 57 %(무첨가)** — 이 위키에서 **100 % 를 넘지 않는 몇 안 되는 Li2S 첫 CE** 다. 단 Li 금속 음극이라 anode-free 로 못 옮긴다. |
| 3 | **"요오드 경로" 의 2021년 원형**. Zhang 2026(PI3 → in-situ LiI)은 이 논문의 후손이다. **두 논문 모두 요오드 자신의 용량 기여를 분리하지 않았다** — 의심은 미해소. `[재현]` 이 논문에서의 몫은 **109.4 mAh g⁻¹(Li2S)** (Zhang 의 152 와 같은 급). |
| 4 | **활성화 전위 비교표에 값 하나 추가**: Cronk 2.4 V (무촉매) < Wan ≈2.80 V ≈ Zhang 2.87 V (요오드) < Lee 3.62 V 컷오프. **요오드는 비싸고 2.8 V 아래로 못 내린다.** |
| 5 | **Li2S 를 직접 양극으로 쓰면 이 첨가제로도 수명이 안 난다** — `[인쇄]` 30사이클 유지 79.7 %(Li2S 계) vs 94.7 %(MoS2 계). 우리 노선에 대한 **반례로 기록**해 둔다. |
| 6 | **분모 바꾸기의 교과서 사례** (437.8 ↔ 604.8, `[재현]` ÷0.7239). [[capacity-normalization-li2s-vs-sulfur]] 의 예시로 쓸 수 있다. |
| 7 | **다음 실험의 설계 하나**: LiI 소량 + 우리 one-step 밀링, 그리고 **"LiI + LPSCl + AB (활물질 없음)" 대조셀**. 이 대조셀이 Wan 2021·Zhang 2026 이 둘 다 빠뜨린 실험이다. |
| 8 | **이 그룹(C. Wang, UMD)은 2016년 Li2S 나노복합체 → 2021년 MoS2 로 갈아탔다** (초록 첫 문장이 그 이유). 우리 노선에 대한 한 줄 반론으로 기억해 둘 것. |

---

## 15. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

크로핑: `.venv/bin/python wiki/tools/extract_figures.py --slug wan2021_lii-libr-catalyst-solid-state-li2s-s-reactions --pdf wiki/inbox/9835470f-LiI-LiBr_catalyst_for_ASSLSBs.pdf --clean`
→ `wiki/raw/figures/wan2021_lii-libr-catalyst-solid-state-li2s-s-reactions/` (5장 + `figures.json`)

| 그림 | 파일 | 봤나 | 이 digest 에서 쓴 곳 |
|---|---|---|---|
| Fig. 1 (XRD · ex-situ 라만 · CV ×2) | `fig_1.png` | **봤다** | §4.1–4.3 — 라만 D/C 라벨 순서, CV 전류 규모, XRD 피크 뭉개짐 |
| Fig. 2 (Li2S 양극 ★) | `fig_2.png` | **봤다 (+ 2a 확대 재판독)** | §5 전부 — 모든 용량·plateau 값이 여기서 나왔다 |
| Fig. 3 (DFT) | `fig_3.png` | **봤다** | §6 — ICOHP 1.66/1.59/1.61 eV 는 **범례에서만** 읽었다 |
| Fig. 4 (MoS2 성능 + SEM) | `fig_4.png` | **봤다 (+ 4d 확대 재판독)** | §7 — 1–3사이클 용량, 100사이클 추이, SEM 입도 |
| Fig. 5 (CV b 값 + 로딩) | `fig_5.png` | **봤다** | §8 — b 값 표 전문, 로딩별 추이 |
| **SI 전부 (S1–S9, Table S1, Experimental)** | — | **없다 (SI 미확보)** | §10 에 인용 지점만 목록화. **값은 본문에 인쇄된 것만 사용** |

확대 재판독한 것 (스크래치 전용 디렉토리에서 생성, 저장소에는 넣지 않음):
Fig. 2a (Li2S@LiI-LiBr 충방전 곡선) · Fig. 4d (100사이클).

**그림에서만 읽은 값은 본문에서 전부 `[도표]` 로 표시했다.** 특히 §5.3 표의 모든 용량값
(1165 / 900 / 835 / 510 / 650 / 420), §7.1·7.2 의 모든 값, ICOHP 세 값, Fig. 3c/3d 의
≈0.8 eV 는 **원문이 인쇄한 적이 없는 수**다.

### 원문 내부 수치 불일치 (한곳에 모음)

| # | 불일치 | 판정 |
|---|---|---|
| 1 | 초록 816.2 @ **200 mA g⁻¹** ↔ 본문 819.6 @ **100 mA g⁻¹**, 711.3 @ 200 mA g⁻¹ | 초록의 전류값이 본문과 안 맞는다 (G13) |
| 2 | 초록 "areal capacity 0.87 mAh cm⁻² 에서 816.2" ↔ `[재현]` 0.87/0.922 = **943.6** | 면적용량은 1사이클, 816.2 는 20사이클 — 한 문장에 섞였다 |
| 3 | 본문 437.8 (분모 MoS2@LiI-LiBr) ↔ 초록 604.8 (분모 MoS2) | `[재현]` 같은 데이터. 437.8 ÷ 0.7239 = 604.8 (G1) |
| 4 | Fig. 4d `[도표]` 100사이클 ≈480 ↔ 인쇄값 437.8 / 604.8 | 그림의 분모 미기재. **그림 값은 인용하지 않는다** |
| 5 | b 값 상승을 "입자 크기 때문" 이라 쓰고 두 문장 뒤 "촉매를 증명" 이라 씀 | 논리 충돌 (G8) |
| 6 | "7 orders of magnitude increase" ↔ 자기 측정 범위는 LiI → LiI-LiBr **16.9배**뿐 | bare Li2S 는 남의 문헌값 (G15) |

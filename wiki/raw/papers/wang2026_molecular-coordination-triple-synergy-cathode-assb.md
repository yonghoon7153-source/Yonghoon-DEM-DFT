---
title: "Wang Yanjie et al. 2026 — Molecular coordination engineering enables triple-synergy cathode design for all-solid-state Li-S batteries (Energy Storage Mater. 91, 105492)"
description: "LGPS 기반 전고체 S8/C 양극에 유기 소분자 DABDT(2,5-diamino-1,4-benzenedithiol 이염산염)를 LiTFSI 와 함께 넣어 100 사이클 평균 황 이용률 48.5 → 97.04 % 를 주장한 논문 — 본문에 Experimental 절이 통째로 없고(SI 미확보) 전도도 실측이 0회이며, Li+ 확산 3자릿수 향상 주장이 같은 논문의 EIS/DRT 결과와 10^10 배 어긋난다"
source_url: local-upload/024d57f9-Molecular_coordination_engineering_enables_triple-synergy_cathode_design_for_all-solid-state_Li-S_batteries.pdf
doi: 10.1016/j.ensm.2026.105492
ingested: 2026-10-01
sha256: e8f35e3c951fa00df5789816f4c8aefb451d29114284fcffe6ef1166853e491f
tags: [assb, sulfide-electrolyte, composite-cathode, activation, carbon, li-in, units]
compare:
  system: "ASSB Li–S (S8 양극 — Li2S 아님). 본문에 Experimental 절이 없고 SI 미확보라 셀 구성 대부분이 미기재"
  electrolyte: "Li10GeP2S12 (LGPS) — 분리층 두께·질량·가압 전부 미기재"
  cathode: "S/C 복합체 + LGPS + LiTFSI + DABDT [인쇄, Scheme 1 범례]. 조성비·탄소 종류·탄소 함량·DABDT 함량·바인더 유무 전부 미기재"
  li2s_source: "해당 없음 — 원소 S8 출발 (Li2S 는 방전 생성물). Li2S 첫 충전 활성화 데이터 없음"
  mixing: "미기재 — 장비·rpm·시간·BPR·볼 재질·분위기·용매·온도가 본문에 한 글자도 없다 (Experimental 절 자체가 없음)"
  loading_mg_cm2: "미기재 — 면적용량 계산 불가"
  li2s_wt_pct: "해당 없음 (S8 계)"
  anode: "Li–In [도표, Fig. 2h·3a 가로축 'Voltage (V vs. Li+/Li-In)']. 본문에는 음극 언급 자체가 없고 조성·두께·N/P 미기재"
  first_charge: "해당 없음 — S8 출발이라 첫 스텝이 방전. 창 0.6–2.4 V vs Li–In (GITT 만 ~0.3–3.0 V), 상온"
  first_discharge_mAh_gS: "1643 @0.2 C (DABDT+LiTFSI) [인쇄] · 1370 (DABDT+LiI) [인쇄] · ≈899 (LiTFSI 단독) [재현 810+89] · ≈810 (무첨가) [도표]"
  first_discharge_mAh_gLi2S: "1147 / 956 / 627 / 565 [재현] ×0.698"
  cycle_capacity_mAh_gS: "≈1650–1700 @0.2 C 10–50사이클 [도표] · 1476 @0.2 C 100사이클 (이용률 88.1 %) [재현] · ≈1175 @0.3 C 500사이클 상온 (70.14 %) [재현] · ≈1588 @0.3 C 500사이클 60 °C (94.81 %) [재현]. 대조군(LiTFSI만) ≈950 → 551 @100사이클"
  cycle_capacity_mAh_gLi2S: "1152–1187 / 1030 / 820 / 1108 [재현] ×0.698. 대조군 663 → 385"
  areal_mAh_cm2: "계산 불가 — 로딩(mg cm⁻²)이 미기재"
  cycles: "100 (0.2 C, 평균 S 이용률 97.04 % vs 대조 ~48.5 %) · 125 (0.2 C, 60 °C) · 500 (0.3 C, 유지율 상온 88.67 % / 60 °C 99.62 %) — 셀 개수·오차막대 없음, 셀 간 수치 불일치 있음"
  temperature_C: "room temperature (수치 미기재) · 60"
  mechanism: "DABDT(-SH + -NH2 방향족 소분자) 첨가제의 'triple synergy' — ①S–Li 배위로 LGPS 표면에 화학 고정(DFT 계면 전하이동 0.269 vs 0.116 |e|, 결합에너지 Li2S −4.21 vs −2.39 eV) ②계면 쌍극자층이 Li+ 수송 가속 ③-SH 가 Li2S2→Li2S 촉매(DFT ΔG, GITT plateau III 28.94 → 50.13 %). 실측은 XPS depth profiling·DRT·ex situ FTIR/XRD/Raman. σ_e⁻·σ_Li⁺ 실측은 0회이고, CV-Randles-Sevcik D_Li+(10^6배)와 EIS/DRT D_Li+(≤2배)가 자기모순"
  our_axis: "Huang 2026(첨가제)·Yu 2024(호스트)에 이은 세 번째 '소량 기능성 상' 논문이지만 전도도를 재지 않아 σ 논쟁에 참여하지 못한다. 세 논문이 공통으로 움직인 양은 다시 활물질–황화물 계면 친화(DFT)뿐 → [[interface-quality-not-bulk-conductivity]] 약한 지지. H4(SE redox)에 강한 근거 — Fig. 2g 를 [재현] 하면 plateau II 가 자기 이론용량의 111 %, plateau III 가 100.3 % 다. 방법 규율 하나를 준다: 고체셀 D_Li+ 를 CV-Randles-Sevcik 으로 재지 않는다. 활물질이 S8 이라 H1(Li2S 첫 충전 활성화)에는 무근거. DABDT 는 이염산염이라 황화물계 H2S 위험을 먼저 확인해야 한다"
---

# 수집 목적

Wang Yanjie, Du Pengyu, Liu Songtao, Liang Fei, Gu Yi, Yao Yao, Liu Hengzhi, Liao Jiaxuan,
Chen Chuanmin, Wang Sizhe, **"Molecular coordination engineering enables triple-synergy cathode
design for all-solid-state Li-S batteries"**, *Energy Storage Materials* **91** (2026) 105492,
DOI 10.1016/j.ensm.2026.105492 (화북전력대 + 전자과기대 Yangtze Delta Region Institute +
섬서과기대 + 남방과기대 + 쿤밍이공대) 의 **절별 해체분석**.

> ⚠ **동명이인 주의.** 이 위키에는 `raw/papers/wang2023_high-capacity-assb-li-s-low-density-solid-electrolyte.md`
> (Dong Wang 외, *Nat. Commun.* 14, 1895, LBPSI 저밀도 SE)가 따로 있다. **다른 그룹·다른 논문이다.**
> 이쪽은 2026년 *Energy Storage Materials*, 교신저자 Wang Sizhe, 주제는 **양극 첨가제**다.
> 재미있게도 Wang 2023 은 이 논문의 Fig. 3h 문헌 비교 차트에 `2 C, S/KB-Super P-LBPSI` 로
> **경쟁 데이터점으로 찍혀 있다** (§7.8).

이 위키가 이 논문을 흡수하는 이유는 넷이다.

1. **"소량 기능성 상으로 ASSLSB 의 kinetics 를 고친다" 계보의 세 번째 논문**이다.
   `raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md`(첨가제 HES 6 wt%)·
   `raw/papers/yu2024_nanocrystallite-cus-n-doped-carbon-host-all-solid-state-li2s.md`(호스트 CuS/NC)
   와 나란히 놓으면 **무엇이 공통으로 움직였는가**가 보인다 (§11 3편 대조표).
   이 위키의 현재 결론 — σ_e⁻ 의 방향은 무관하고 움직인 것은 σ_Li⁺ 와 **활물질–황화물 계면 친화**뿐
   ([[interface-quality-not-bulk-conductivity]]) — 을 이 논문이 지지하는지 기각하는지가 관건이었다.
   **답: 이 논문은 σ_e⁻ 도 σ_Li⁺ 도 실측하지 않았다.** 그래서 전도도 축에는 아무 것도 더하지 못하고,
   **계면 친화 축에만** DFT 근거를 더한다 (§11.3).
2. **활물질이 S8 이다 (Li2S 가 아니다).** 그러므로 우리 최대 난점인 **Li2S 첫 충전 활성화**에는
   근거를 주지 않는다. 이 경계선을 명시적으로 긋는 것 자체가 수집 목적의 일부다 (§10, §12).
3. **이론용량에 거의 닿는 "황 이용률 97.04 %"** 를 주장한다. 이 위키의 규율 — *이론값을 넘거나
   닿는 용량을 보면 황화물 SE 자신의 리독스를 먼저 의심한다* ([[reference-cell-500-600-mahg]] H4) —
   를 적용할 아홉 번째 사례다. **이 논문의 자체 수치(Fig. 2g)가 plateau II 에서 자기 이론용량의
   111 % 를 내고 있다** (§5.3 [재현]). 하한 컷오프가 **0.6 V vs Li–In** 이고 SE 가 **LGPS**(Ge 함유)다.
4. **방법론 경고를 하나 준다.** 같은 셀에서 **CV-Randles-Sevcik 로 구한 D_Li⁺ 와 EIS/DRT 로 구한
   D_Li⁺ 가 10¹⁰배 어긋난다** (§6.2 vs §8.4). 우리가 H2b(이온 네트워크)를 판정할 때 **고체셀에
   Randles-Sevcik 을 쓰면 안 된다**는 선례다.

**표기 규칙** (이 위키 관례 4구분):
- `[인쇄]` — 논문 본문·캡션·그림 안에 글자로 인쇄된 것 (그림 안이면 위치를 밝힌다)
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**)
- `[해석]` — 이 digest 를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값의 산술 환산 (계산식을 함께 적는다)

**단위 선언**: 이 논문은 비용량을 전부 `mAh g⁻¹` 로만 쓰고 **분모를 글자로 밝히지 않는다.**
그러나 "sulfur utilization" 을 쓰고 이론값으로 1675 mAh g⁻¹ 를 들며(§3.1), Fig. 3f 의 이용률
수치 × 1675 가 Fig. 3e 의 용량 눈금과 정확히 맞는다 (§7.6 [재현]). **따라서 이 digest 의
`mAh g⁻¹` 는 전부 `(S)` 기준**이고, `(Li2S)` 기준은 **×0.698** 한 `[재현]` 이다
(0.698 = M(S)/M(Li2S) = 32.065/45.948; 1675 × 0.698 = 1169 ≈ Li2S 이론 1166).
전압은 **vs Li–In** 이다 — 본문에는 기준전극이 한 번도 안 나오지만 **Fig. 2h · Fig. 3a 의
가로축이 `Voltage (V vs. Li⁺/Li-In)`** 로 인쇄돼 있다 `[인쇄, 그림 축라벨]`.
Li–In 과 Li/Li⁺ 사이 오프셋 값은 이 위키에 raw 근거가 없으므로 **환산하지 않는다**.

- 원본: 로컬 업로드 PDF 11쪽 (저널 조판 1–11, article no. 105492). **SI 미확보.**
- 크로핑 그림: `raw/figures/wang2026_molecular-coordination-triple-synergy-cathode-assb/`
  — Scheme 1 + Fig. 1–5, 총 6장. 본문 그림은 이것이 전부다.

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

> **★ 이 논문의 가장 큰 공백은 "Experimental 절 자체가 본문에 없다" 는 것이다.**
> 본문은 `1. Introduction → 2. Results and discussion → 3. Conclusion → CRediT` 로 끝난다.
> 재료·합성·셀 조립·측정 조건이 **한 줄도 없다.** 전부 SI 에 있고 SI 는 미확보다.
> 아래 G1–G6 은 "저자가 안 쟀다" 가 아니라 "**이 digest 로는 알 수 없다**" 는 뜻이다 —
> SI 를 구하면 대부분 메워진다. G7 이후는 **SI 를 구해도 안 메워질 가능성이 큰** 공백이다.

| # | 공백 | 왜 중요한가 | 메우는 법 |
|---|---|---|---|
| **G1** | **복합양극 조성비 전부.** S : C : LGPS : LiTFSI : DABDT 의 wt% 가 하나도 없다. 성분 목록만 Scheme 1 범례에서 읽힌다 (`S/C`, `LGPS`, `LiTFSI`, `DABDT`) `[인쇄, Scheme 1 범례]` | **DABDT 가 몇 wt% 인지 모르면 이 논문의 주장 자체를 평가할 수 없다.** Huang 2026 은 6 wt%, Yu 2024 는 호스트 내 29 wt% 로 명시했다 | SI Experimental |
| **G2** | **탄소의 정체와 함량.** "S/C" 라고만 하고 종류(AB/KB/Super P/CNT), 함량, S:C 비가 전부 없다 | [[carbon-dimensionality-electron-network]] 의 열을 못 채운다. "삼상 계면 의존을 극복했다" 는 주장은 탄소량을 알아야 검증된다 | SI |
| **G3** | **혼합·합성 경로 전무.** 장비·rpm·시간·BPR·볼 재질·분위기·용매·온도 — **한 글자도 없다** | [[composite-cathode-mixing-routes]] 에 아무 행도 못 넣는다. Cronk 2026 은 혼합 경로만으로 첫 방전이 1500↔200 으로 갈린다고 보였다 | SI |
| **G4** | **로딩(mg cm⁻²)·전극 두께·면적.** 면적용량(mAh cm⁻²)을 **계산조차 못 한다** | 우리 셀과 수치를 나란히 놓을 수 없다. Fig. 1c EDS 단면에 100 µm 스케일바가 있으나 전극 두께 경계가 불명확해 읽지 않았다 | SI |
| **G5** | **음극의 정체·두께·N/P.** 본문에 "anode" 라는 단어가 **실험 맥락에서 한 번도 안 나온다.** Li–In 은 **그림 축라벨에서만** 확인된다 | Li–In 의 In 과잉은 Li 재고 무한을 뜻한다 — [[anode-free-li2s-assb]] 로 옮길 때 핵심 변수 | SI |
| **G6** | **성형 압력 / 운전 스택 압력.** 둘 다 없다. "~80 % 부피 팽창" 을 문제로 들면서 구속 조건을 안 밝힌다 | Qu 2025 는 정압(스프링) vs 정용적(볼트)에서 100 사이클 유지가 63 % vs 50 % 로 갈린다고 보였다 ([[reference-cell-500-600-mahg]] H5) | SI |
| **G7** | **σ_e⁻ 도 σ_Li⁺ 도 실측하지 않았다.** "ionic/electronic dual-conductive network" 가 제목급 주장인데 **복합체 전도도 측정이 하나도 없다.** 근거는 DFT 밴드갭(1.63 → 1.26 eV)과 CV 기울기뿐 | **Yu 2024 · Huang 2026 과 σ 를 나란히 놓을 수 없다.** 이 논문은 전도도 논쟁에 참여하지 않는다 | DC 분극 측정이 필요 — 저자가 안 했다 |
| **G8** | **D_Li⁺ 가 같은 논문 안에서 10¹⁰배 어긋난다.** Fig. 3c(CV) ≈ 2×10⁰ cm² s⁻¹, Fig. 4j(EIS/DRT) ≈ 5×10⁻¹⁰ cm² s⁻¹ `[도표]` | 둘 중 하나(또는 둘 다)가 틀렸다. 본문은 둘이 "consistent" 하다고 쓴다 (§8.4) | 저자 정오표 외엔 방법 없음 |
| **G9** | **셀 개수·오차막대·재현성 전무.** 모든 그림이 단일 곡선. "with/without" 각 1 셀로 보인다 | 97.04 % vs 48.5 % 라는 2배 차이의 통계적 의미를 알 수 없다 | 원저자 |
| **G10** | **"sulfur utilization" 의 정의식이 글자로 없다.** 용량/1675 로 보이지만 명시 안 됨 | 분모가 S 인지 S+C 복합체인지에 따라 97 % 가 달라진다 | §7.6 [재현] 로 간접 확정했다 |
| **G11** | **SE 기여 대조셀이 없다.** LGPS + C 만 넣은 셀의 용량을 재지 않았다 | 0.6–2.4 V vs Li–In 창에서 LGPS 의 Ge 환원 몫을 뺄 방법이 없다. Cronk 2026 은 `LPSCl + AB (80:20)` 대조셀로 이것을 쟀다 (환원 115 / 산화 355 mAh g⁻¹) | 우리가 직접 할 수 있다 |
| **G12** | **DABDT·2HCl 의 염산 2당량 거동.** 전구체가 **dihydrochloride** 인데 황화물 SE·Li2S 와의 반응(H2S 발생 가능성)을 언급조차 안 한다. EDS 에 Cl 이 분명히 잡힌다 `[인쇄, Fig. 1c 범례]` | 우리가 이식하려면 **가장 먼저 확인해야 할 안전·열화 항목** | §12.2 |
| **G13** | **DABDT 단독 대조군 없음.** 비교군은 (무첨가) / (LiTFSI) / (DABDT+LiI) / (DABDT+LiTFSI) 넷뿐 — **DABDT 단독**이 없다 | "LiTFSI 는 기본 이온전도, DABDT 는 계면" 이라는 역할 분리가 실험으로 안 갈린다 | 원저자 |
| **G14** | **SI 인용 지점**: Fig. S5(무DABDT CV), Fig. S11(0.5 C 첫 5 사이클), Fig. S13(사이클 후 단면 SEM), Tab. S1(문헌 비교표). **SI 미확보라 전부 미검증.** S1–S4·S6–S10·S12 는 본문에서 인용조차 안 된다 (= 본문에 없는 Experimental 절이 인용했을 것) | 구조 안정성 주장(균열 유무)의 **유일한 실측 근거가 Fig. S13** 인데 못 봤다 | SI 입수 |

---

## 0. 서지사항 (직접 확인)

| 항목 | 값 `[인쇄]` |
|---|---|
| 제목 | Molecular coordination engineering enables triple-synergy cathode design for all-solid-state Li-S batteries |
| 저자 | Wang Yanjie, Du Pengyu, Liu Songtao, Liang Fei, Gu Yi, Yao Yao, Liu Hengzhi, Liao Jiaxuan, Chen Chuanmin, Wang Sizhe |
| 교신 | Wang Sizhe (kevinwang@sust.edu.cn, UESTC Yangtze Delta Region Institute / SUST) · Chen Chuanmin (hdccm@126.com, NCEPU) · Liao Jiaxuan (jxliao@uestc.edu.cn) · Liu Hengzhi (liuhz@sustech.edu.cn, SUSTech) |
| 저널 | *Energy Storage Materials* **91** (2026) 105492 |
| DOI | 10.1016/j.ensm.2026.105492 |
| 접수/수정/게재승인 | 2026-07-06 / 2026-08-13 / 2026-08-23 (online 2026-08-24) |
| 키워드 | Sulfur utilization · All-solid-state lithium-sulfur batteries · Molecular coordination |
| 참고문헌 | 33편 |
| 구성 | 1. Introduction / 2. Results and discussion / 3. Conclusion — **Experimental 절 없음** |

---

## 1. 한 문단 요약

LGPS(Li10GeP2S12) 기반 전고체 Li–S 셀의 S8/C 복합양극에 **DABDT
(2,5-diamino-1,4-benzenedithiol dihydrochloride)** 라는 유기 소분자를 **LiTFSI 와 함께** 넣으면,
0.2 C 첫 방전이 `[인쇄]` **1643 mAh g⁻¹(S)**(무첨가 `[도표]` ≈810, LiTFSI 단독 ≈899)로 오르고
100 사이클 평균 황 이용률이 `[인쇄]` **97.04 %**(대조군 ~48.5 %)가 된다. 저자는 이를 **"강한 화학결합
+ 쌍극자층 가속 + 표적 촉매" 라는 3중 상승효과(triple synergy)** 로 설명한다 — DABDT 의 -SH 가 LGPS
표면 Li⁺ 와 S–Li 배위(거리 ~2.7 Å, 계면 전하이동 0.269 |e| = LiTFSI 의 2.32배)를 이루어 고정되고,
그 계면 쌍극자층이 Li⁺ 이동을 가속하며, -SH 가 율속단계 Li2S2 → Li2S 를 촉매한다는 것이다.
근거의 대부분은 **DFT**(PDOS·밴드갭 1.63→1.26 eV·d-band center·결합에너지·Gibbs 자유에너지)와
**GITT plateau 분해**(plateau III 기여 28.94 → 50.13 %)이고, 실측 분광은 XPS depth profiling,
DRT, ex situ 마이크로-FTIR/XRD/Raman 이다. **그러나 복합양극 조성·로딩·혼합·음극·압력이 본문에
하나도 없고(SI 전담, 미확보), 전자·이온 전도도를 실측하지 않았으며, 핵심 주장인 "Li⁺ 확산 3자릿수
향상" 은 같은 논문의 EIS/DRT 결과(≤2배)와 정면으로 충돌한다.**

---

## 2. p.1 — Abstract 의 명제 `[인쇄]`

> "All-solid-state lithium-sulfur batteries (ASSLSBs) … High sulfur utilization is key to boosting
> practical energy density but is severely hindered by sluggish sulfur conversion kinetics at
> solid-solid interfaces. Herein, a coordination chemistry strategy is proposed using
> 2,5-diamino-1,4-benzenedithiol dihydrochloride (DABDT) as a multifunctional additive."

초록이 내건 수치 네 개:

| 수치 `[인쇄]` | 조건 | `(Li2S)` 환산 `[재현]` ×0.698 |
|---|---|---|
| 평균 황 이용률 **97.04 %** | 0.2 C, 100 사이클 | = 1625 mAh g⁻¹(S) → **1134 mAh g⁻¹(Li2S)** |
| 황 이용률 **70.14 %** | 0.3 C, 500 사이클 후, 상온 | = 1175 → **820** |
| 황 이용률 **94.81 %** | 0.3 C, 500 사이클 후, 60 °C | = 1588 → **1108** |
| 용량 감쇠율 **0.0228 % / 0.0008 %** per cycle | 0.3 C, 상온 / 60 °C | — |

초록이 말하는 기전 세 가지 `[인쇄]`:
(i) "forms strong electronic coupling and coordination anchors with the Li10GeP2S12 (LGPS) electrolyte",
(ii) "constructs an ionic/electronic dual-conductive network, overcoming reliance on physical
three-phase contact interfaces",
(iii) "forms a dipole layer via interfacial charge redistribution to accelerate Li⁺ migration,
simultaneously upshifts the D-band center and lowers the Gibbs free energy of the rate-determining
step (Li2S2 → Li2S)".

`[해석]` (ii) 의 "dual-conductive network" 가 이 논문에서 **단 한 번도 전도도로 측정되지 않는다**는
점을 미리 적어 둔다 (G7). 근거는 전부 계산이거나 전기화학 응답의 간접 해석이다.

---

## 3. p.1–4 — §1 Introduction 의 문제 설정 `[인쇄]`

### 3.1 저자가 세운 세 가지 벽

| # | 벽 | 원문 표현 |
|---|---|---|
| 1 | **구조 불안정** | "sulfur undergoes ~80 % volume expansion during cycling; the resulting cyclic stress disrupts interfacial contact" |
| 2 | **삼상 계면 제한** | "sulfur conversion relies entirely on the three-phase boundary among the active material, solid electrolyte, and electronic conductor … much of the sulfur cannot access both ions and electrons … becoming 'dead sulfur'" |
| 3 | **율속단계 Li2S2 → Li2S** | "the Li2S2 → Li2S step, which contributes most of the capacity, exhibits sluggish kinetics. Its high reaction barrier and solid-phase nucleation barrier severely hinder deep conversion" |

이론용량은 `[인쇄]` "high theoretical specific capacity of 1675 mAh g⁻¹" — **분모를 안 밝혔지만
1675 는 S 기준 값이다** `[해석]`.

### 3.2 기존 전략 분류 `[인쇄]`

| 분류 | 예시 | 저자가 든 한계 |
|---|---|---|
| 양극 구조 설계 | 탄소와 복합화 [12–14], 활물질 표면 SE 코팅/in-situ 생성 [15,16], 유기황·폴리머 유연 구조 [7,17] | "carbon-induced side reactions, increased inert components, and hindered charge transport" |
| 전해질 설계 | 신규 전해질, 황화물에 헤테로원자 도핑 [18–20] | "does not directly increase the intrinsic reactivity of sulfur or expand the effective three-phase boundary" |
| 촉매/첨가제 설계 | 전기촉매 NiO [21], 리독스 매개체 Li_xIn2S3 [22–25], 계면 안정제·기능성 염 LiI·S9.3I [26–29] | "can alleviate one or two of the problems … still cannot simultaneously regulate all three" |

`[해석]` 인용 [22] 는 Yu Peng 외 *Adv. Funct. Mater.* 34, 2306939 (interfacial redox mediator로
micrometer-size Li2S 다룸)이고, [18] 은 이 위키의 `wang2023_…`(Dong Wang, LBPSI)다. 즉 이 논문은
우리가 이미 가진 두 digest 를 "한두 문제만 푼 선행" 으로 분류한다.

### 3.3 이 논문의 제안 `[인쇄]`

"introducing for the first time 2,5-diamino-1,4-benzenedithiol dihydrochloride (DABDT), which
contains both mercapto (-SH) and amino (-NH2) groups, as a functional component into the cathode".
그리고 결론 문장: **"a triple synergistic mechanism of 'strong chemical bonding, dipole-layer
acceleration, and targeted catalysis'"**.

---

## 4. Scheme 1 — 셀 구성에 대해 **그림이 본문보다 많이 말한다** (★)

`[인쇄, Scheme 1 범례]` 범례의 성분이 이 논문에서 복합양극 조성에 가장 가까운 정보다:

| 기호 | 성분 |
|---|---|
| 노랑/검정 구 | **S/C** (황–탄소 복합체) |
| 연파랑 큰 구 | **LGPS** |
| 회색 구 | **LiTFSI** |
| 분자 모형 | **DABDT** |
| 어두운 구 | **Li2S** (방전 생성물) |
| 빨간 점선 구 | **Inactive S/C** (대조군에서) |

`[도표, Scheme 1b/c]` 양극층은 `Current Collector` 와 `Electrolyte`(SE 분리층) 사이에 있고,
**바인더는 범례에도 그림에도 없다.** 구 비율은 LGPS 가 부피의 대부분이고 S/C 가 그 사이에 분산된
모습 — 다만 **모식도이므로 조성비 근거로 쓸 수 없다** `[해석]`.
오른쪽 확대도의 라벨 셋이 곧 "triple synergy" 다: ① `Stabilized Interfacial Anchoring`,
② `Accelerated Li⁺ transport`, ③ `Facilitates e⁻ transport`. 그리고 `Lithium Compensation`
이라는 화살표가 LiTFSI(회색 구) → LGPS 로 그려져 있다.

`[해석]` **"triple synergy" 의 세 축은 ①계면 고정(화학) ②이온 전도 ③전자 전도이고,
촉매(Li2S2→Li2S)는 Scheme 1a 의 네 번째 불릿으로 따로 적혀 있다.** 즉 본문의 "strong chemical
bonding / dipole-layer acceleration / targeted catalysis" 와 Scheme 1 의 세 축이 **서로 다르다**
(Scheme 1 은 전자 전도를 세 번째로, 본문은 촉매를 세 번째로 센다). 저자 스스로 3축의 목록을
두 가지로 쓰고 있다 — §12.1 에서 다시 다룬다.

---

## 5. p.4–5 — Fig. 1 + Fig. 2e–g: DFT 와 GITT (★ 수치의 중심)

### 5.1 Fig. 1a–c — 재료 확인

- `[인쇄]` XRD: LiTFSI 는 2θ = 13.6°, 15.9°, 18.6°, 18.9°, 21.4° 에 날카로운 피크. DABDT 는
  20–45° 에 중간 세기 피크들 (23.2°, 23.7°, 27.4°, 28.3°, 30°, 30.4° 등).
- `[인쇄]` 마이크로-FTIR(양극, Fig. 1b): ~2470 cm⁻¹ (-SH 신축), ~3440/~3400 cm⁻¹ (-NH2 대칭/비대칭
  신축), ~1570/1512/1492 cm⁻¹ (벤젠 C=C) = DABDT; ~1050 (S-N-S), ~1171/1227 (CF3 대칭/비대칭),
  ~1380 cm⁻¹ (SO2 비대칭) = LiTFSI. 2300–2400 cm⁻¹ 구간은 CO2 흡수로 생략.
- `[도표, Fig. 1b]` **-SH(2470)와 -NH2(3400/3440) 영역은 육안으로 봉우리가 아니라 평탄한
  잡음 바닥이다.** 회색 띠로 위치만 표시돼 있다. 1000–1700 cm⁻¹ 구간의 LiTFSI 피크들만 뚜렷하다.
  `[해석]` 이 관측이 §9 의 ex situ FTIR 추적 전체의 신뢰도를 깎는다.
- `[인쇄, Fig. 1c 범례]` EDS 원소: **C, N, O, F, P, S, Cl, Ge** — 스케일바 100 µm.
  `[해석]` **Cl 이 있다.** LGPS(Li10GeP2S12)에는 Cl 이 없으므로 Cl 의 출처는 **DABDT·2HCl 의
  염산 2당량**뿐이다 (G12). 저자는 Cl 을 매핑해 놓고 한 글자도 설명하지 않는다.

### 5.2 Fig. 1d–j — DFT (LGPS 슬래브 + 분자)

| 양 | LGPS-DABDT | LGPS(pristine) | LGPS-LiTFSI | 출처 |
|---|---|---|---|---|
| 에너지 갭 | **1.26 eV** | 1.63 eV | 1.77 eV | `[인쇄, Fig. 1e 안]` |
| d-band center | **−4.43 eV** | −6.51 eV | −8.91 eV | `[인쇄, Fig. 1f 안]` |
| 계면 순 전하이동 | **0.269 \|e\|** (LGPS → DABDT) | — | 0.116 \|e\| | `[인쇄, 본문 + Fig. 1h/i 안]` |
| S–Li 배위 거리 | ~2.7 Å | — | — | `[인쇄]` |
| N–Li 거리 | ~4.0 Å | — | — | `[인쇄]` |
| ΔG_ads(Li) = G(DABDT-Li) − G(DABDT) − G(Li) | **−0.60 eV** | — | — | `[인쇄, Fig. 1j 안]` |
| Li 이동 장벽 (TS) | **0.48 eV** | — | — | `[인쇄, Fig. 1j 안]` |

`[재현]` 0.269 / 0.116 = **2.319** — 본문의 "2.32 times" 와 일치한다.

본문 논지 `[인쇄]`: DABDT 의 S 원자와 LGPS 표면 Li⁺ 사이에 "continuous electron cloud bridge" 가
형성되고, 벤젠 고리의 비편재 π 전자가 Fermi 준위 근처에 새 상태를 만들어 "enhancing the electronic
conductivity of the interfacial region" 한다. Ge·P 주변은 색 변화가 없어 "framework cations do not
directly participate in electron transfer".

`[해석]` 세 가지 문제.
1. **"d-band center" 는 전이금속 촉매 기술어다.** LGPS 의 Ge 는 3d¹⁰ 닫힌 껍질 주족 원소이고
   DABDT 에는 d 전자가 없다. 이 계에서 d-band center 를 촉매 활성 기술어로 쓰는 것은 물리적
   근거가 약하다. 더구나 −8.91 → −6.51 → −4.43 eV 라는 **2.4 eV 씩의 거대한 이동**은 흡착종이
   바뀐 것이 아니라 슬래브 참조 준위가 달라졌을 가능성을 먼저 배제해야 한다.
2. **밴드갭을 1.63 → 1.26 eV 로 좁히는 것은 고체전해질에서는 "개선" 이 아니라 "결함" 이다.**
   SE 의 전자 전도가 커지면 자가방전과 SE 자체 분해가 빨라진다. 저자는 이것을 성과로 제시한다.
3. 0.48 eV 는 **DABDT–Li 복합체 형성의 전이상태**이지 복합양극 속 Li⁺ 수송 장벽이 아니다.
   Yu 2024(0.3 vs 1.5 eV)·Huang 2026(0.20 vs 0.25 eV)의 NEB 값과 **같은 양이 아니므로 나란히
   놓으면 안 된다**.

### 5.3 Fig. 2e–g — GITT plateau 분해 (★ 이 논문에서 가장 값진 수치)

GITT 는 **0.05 C**, 창은 `[도표]` 충전 상한 **3.0 V**, 방전 하한은 0.6 V 아래까지 내려간다
(Fig. 2a–d 의 0.6–2.4 V 와 **다른 창**이다 — §12.3).

`[인쇄, Fig. 2e/f 안]` 총용량 대비 plateau 기여:

| plateau | 반응 | with DABDT | without DABDT |
|---|---|---|---|
| I | S8 → LiPSs | 8.08 % | 8.00 % |
| II | LiPSs → Li2S2 | 41.73 % | 49.87 % |
| III | **Li2S2 → Li2S** | **50.19 %** | **42.14 %** |

`[인쇄, Fig. 2g 안]` "Contribution Rate to Theoretical Capacity":

| plateau | with DABDT | without DABDT |
|---|---|---|
| I | 8.07 % | 5.45 % |
| II | 41.68 % | 34.21 % |
| III | **50.13 %** | **28.94 %** |

**[재현] — Fig. 2g 의 분모가 무엇인지 역산한다.**
with DABDT 합계 = 8.07 + 41.68 + 50.13 = **99.88 %**.
각 plateau 를 이 합계로 나누면 8.07/99.88 = 8.08 %, 41.68/99.88 = 41.73 %, 50.13/99.88 = 50.19 % —
**Fig. 2f 의 세 값과 소수 둘째 자리까지 일치한다.**
without DABDT 합계 = 5.45 + 34.21 + 28.94 = **68.60 %**;
5.45/68.60 = 7.95 %(Fig. 2e 8.00), 34.21/68.60 = **49.87 %**(일치), 28.94/68.60 = 42.19 %(Fig. 2e 42.14).
→ **Fig. 2g 의 분모는 각 plateau 자신의 이론용량이 아니라 1675 mAh g⁻¹(S) 전체다.**
본문의 "the ratio of the actual contribution of each plateau to its theoretical capacity" 는
**그림이 실제로 보여주는 것과 다르다** `[해석]`.

따라서 GITT 총용량은:
- with DABDT: 0.9988 × 1675 = **1673 mAh g⁻¹(S)** = `[재현]` **1168 mAh g⁻¹(Li2S)**
- without DABDT: 0.6860 × 1675 = **1149 mAh g⁻¹(S)** = `[재현]` **802 mAh g⁻¹(Li2S)**
(Fig. 2f/2e 가로축 끝 `[도표]` ≈1690 / ≈1230 과 맞는다.)

**[재현] — 각 plateau 를 자기 이론용량으로 나누면 (이것이 본문이 말한 양이다):**
plateau I 이론 = 1675 × 1/8 = 209; II 이론 = 1675 × 3/8 = 628; III 이론 = 1675 × 1/2 = 838.

| plateau | with DABDT 실측 | 자기 이론 대비 | without DABDT 실측 | 자기 이론 대비 |
|---|---|---|---|---|
| I | 135 mAh g⁻¹(S) | 64.6 % | 91 | 43.6 % |
| II | 698 | **111.2 %** ⚠ | 573 | 91.2 % |
| III | 840 | **100.3 %** ⚠ | 485 | 57.9 % |

> ★ **with DABDT 의 plateau II 가 자기 이론용량의 111 %, plateau III 가 100.3 % 다.**
> 황만으로는 불가능하다. **황 이외의 리독스(가장 유력하게는 LGPS 자신의 환원)가 섞여 있다**는
> 뜻이거나, plateau 경계선을 그은 방식이 자의적이라는 뜻이다 `[해석]`.
> 이 위키의 규율 — *이론을 넘는 용량을 보면 SE redox 를 먼저 의심한다* — 의 교과서적 사례다
> ([[reference-cell-500-600-mahg]] H4). 저자는 SE 기여 대조셀을 돌리지 않았다 (G11).

---

## 6. p.5–6 — Fig. 2a–d, 2h–i, Fig. 3a–c: 전기화학

### 6.1 Fig. 2a–d — 네 가지 양극 조성의 0.2 C 첫 사이클

창 `[도표]` **0.6–2.4 V vs Li–In**, 0.2 C, 상온.

| 패널 | 조성 | 첫 방전 mAh g⁻¹(S) | `(Li2S)` `[재현]` ×0.698 | S 이용률 `[재현]` /1675 |
|---|---|---|---|---|
| a | **without DABDT & LiTFSI** (무첨가) | `[도표]` ≈810 | ≈565 | ≈48 % |
| b | **with LiTFSI** (= 이후 모든 그림의 "without DABDT") | `[도표]` ≈890 · `[재현]` 810+89 = **899** | ≈627 | ≈54 % |
| c | **with DABDT & LiI** | `[인쇄]` **1370** (`[도표]` 곡선 끝 ≈1300) | 956 | 82 % |
| d | **with DABDT & LiTFSI** (= "with DABDT") | `[인쇄]` **1643** | **1147** | **98.1 %** |

`[인쇄]` "the addition of LiTFSI alone increased the capacity by 89 mAh g⁻¹, indicating that LiTFSI
improves ionic conduction."
`[인쇄]` DABDT+LiI 는 "the smallest polarization, but its steep discharge plateau indicated a
suboptimal conversion pathway."
`[인쇄]` DABDT+LiTFSI 는 "smooth voltage plateaus highly similar to the typical discharge
characteristics of liquid lithium-sulfur batteries".

`[해석]` 마지막 문장이 이 논문에서 가장 위험한 수사다 — **액체계와 닮은 평탄구간은 전고체셀에서
"좋음" 의 증거가 아니다.** 액체계는 용해된 LiPSs 가 매개하기 때문에 평탄하고, 전고체셀에서 같은
모양이 나오면 (i) 진짜로 매개종이 생겼거나 (ii) 다른 상(SE)이 함께 반응하고 있다는 뜻일 수 있다.
저자는 (ii) 를 검토하지 않았다.

`[도표]` **첫 사이클 CE** 는 a 에서 ≈93 %(방전 810 / 충전 ≈750), b·c·d 에서 ≈98–100 %.
Fig. 3e/3g/3i 의 CE 는 1사이클부터 100 % 에 붙어 있다. `[해석]` 전고체 Li–S 에서 **0.6 V 하한까지
내려가고도 첫 CE 가 ~100 %** 라는 것은, SE 환원이 비가역이라면 나타나기 어렵다. 오히려 §7.4 의
"처음 10 사이클 동안 용량이 **증가**한다" 는 현상이 비가역 성분의 자리를 대신 차지하고 있을
가능성이 있다 `[해석]`.

### 6.2 Fig. 2h–i · Fig. 3a–c — CV / dQ-dV / Randles-Sevcik

**Fig. 2h (CV, 0.1 mV s⁻¹, 0.6–2.4 V vs Li–In)** `[인쇄, 그림 안]`

| | 환원 피크 | 산화 피크 | 분리 `[재현]` |
|---|---|---|---|
| with DABDT | **0.91 V** | **2.00 V** | **1.09 V** |
| without DABDT | 0.88 V | 1.97 V | **1.09 V** |

`[인쇄, 그림 안]` ΔQ_c = ~513 mAh/g ("interface activation", Li2S2→Li2S 쪽 음영),
ΔQ_a = ~502 mAh/g ("kinetics gain", LiPSs→S8 쪽 음영).

> `[재현]` **두 셀의 CV 피크 분리가 1.09 V 로 완전히 같다.** 본문은 "a much smaller separation
> between oxidation and reduction peaks" 라고 쓰는데 **Fig. 2h 에서는 사실이 아니다.** 그 문장은
> Fig. 2i(dQ/dV)에만 해당한다 (아래).

**Fig. 2i (dQ/dV)** `[인쇄, 그림 안]`

| | 환원 피크 | 산화 피크 | 분리(주피크 기준) `[재현]` |
|---|---|---|---|
| with DABDT | **1.32 V**(S8→LiPSs) · **1.21 V**(LiPSs→Li2S2/Li2S) | **1.77 V** | 1.77 − 1.32 = **0.45 V** |
| without DABDT | 1.17 V · 1.11 V | 1.85 V | 1.85 − 1.17 = **0.68 V** |

`[인쇄]` "the high-voltage reduction peak was suppressed" (대조군), "the emergence of a high-voltage
reduction peak indicating promoted initial sulfur activation".
`[도표]` dQ/dV 최대값도 with DABDT 가 ~4700 vs ~1100 (mAh g⁻¹ V⁻¹) 으로 4배 이상 크다.

**Fig. 3b–c (Randles-Sevcik)** `[인쇄, 그림 안]`

| | 음극(cathodic) 기울기 | 양극(anodic) 기울기 | I_p 축 범위 |
|---|---|---|---|
| with DABDT | **89.2046** | **69.8239** | 0 – 2.5 mA |
| without DABDT | **0.0531** | **0.0411** | 0 – 1.4×10⁻³ mA |

`[도표, Fig. 3c]` 0.1 mV s⁻¹ 에서 D_Li⁺: with DABDT ≈ **1.65–2.0** cm² s⁻¹ (축 라벨 `2.0E+0`),
without DABDT ≈ **9.2×10⁻⁷ – 1.4×10⁻⁶** cm² s⁻¹.

> ★ **[재현] 세 겹의 문제.**
> (1) 기울기 비 89.2046 / 0.0531 = **1680** ≈ 3자릿수. D ∝ (기울기)² 이므로 D 비는
>     1680² = **2.8×10⁶** ≈ **6자릿수**. Fig. 3c 의 2.0 / 9.2×10⁻⁷ = 2.2×10⁶ 와 맞는다.
>     **본문의 "increases the Li⁺ diffusion coefficient by nearly three orders of magnitude" 는
>     기울기 비를 D 비로 잘못 옮긴 것이다** — 그림은 6자릿수를 말한다.
> (2) **D_Li⁺ ≈ 2 cm² s⁻¹ 는 물리적으로 불가능하다** (기체 분자의 자체확산보다 빠르다).
>     Randles-Sevcik 는 반무한 액상 확산을 가정하는 식이고, 고체 복합양극 + 고체전해질 셀에
>     적용하면 유효 전극 면적·농도 항이 전부 허구가 된다.
> (3) `[도표, Fig. 3c]` **D 가 스캔속도에 따라 단조 감소한다** (0.1 → 1.0 mV s⁻¹ 에서 2.0 → ~0.03).
>     확산계수는 스캔속도의 함수가 아니어야 한다. 식의 전제가 깨졌다는 자기 증거다.
> → **이 수치는 우리 위키가 인용해서는 안 된다.** 같은 논문의 EIS/DRT 값(§8.4)과 비교하면
>   **10¹⁰배** 어긋난다.

---

## 7. p.6–8 — Fig. 3d–i: 사이클·율속·이용률

### 7.1 Fig. 3d — 율속 (with DABDT)

`[도표]` 각 단계 5 사이클, 전부 mAh g⁻¹(S):

| C-rate | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.8 | 1.0 | 0.1 (복귀) |
|---|---|---|---|---|---|---|---|---|---|
| 용량 (S) | ≈1200→1350 | ≈1240 | ≈1200→1080 | ≈1050→980 | ≈950→880 | ≈870→780 | ≈750→620 | ≈600→550 | ≈1280–1320 |
| `(Li2S)` `[재현]` | ≈840–940 | ≈865 | ≈755–840 | ≈685–735 | ≈615–665 | ≈545–610 | ≈435–525 | ≈385–420 | ≈895–920 |

`[인쇄]` "when returned to 0.1 C, the capacity recovers to ~1300 mAh g⁻¹, and the Coulombic
efficiency remains close to 100 % throughout the entire rate test."
`[인쇄]` Fig. S11(미확보): 0.5 C 첫 5 사이클이 "almost overlap, with a stable capacity around
1270 mAh g⁻¹".

> ★ `[해석]` **율속시험과 사이클시험이 충돌한다.** Fig. 3d 에서 **0.1 C 의 최대가 ≈1350** 인데
> Fig. 3e 에서는 **0.2 C 에서 ≈1700** 이 나온다. 더 느린 율속에서 용량이 더 작다 — 같은 셀이라면
> 불가능하다. 또 Fig. 3d 의 0.5 C 는 ≈880–950 인데 Fig. S11 인용은 0.5 C 에서 1270 이라고 한다.
> **최소 세 개의 서로 다른 셀이 "with DABDT" 라는 한 이름으로 보고되고 있다** (G9).

### 7.2 Fig. 3e — 0.2 C 100 사이클

`[도표]` mAh g⁻¹(S):

| | 1사이클 | 2사이클 | 10–50사이클 | 100사이클 |
|---|---|---|---|---|
| with DABDT | ≈1300 | ≈1520 | **≈1650–1700** | ≈1480 |
| without DABDT | ≈950 | ≈950 | ≈950 (60사이클까지) | ≈520 |

`[인쇄, 그림 안]` "Average Sulfur utilization: 97.04 %".
`[인쇄]` "the ASSLSBs with DABDT exhibit a unique activation behavior at room temperature: the
capacity increases slightly in the initial cycles, stabilizes after about 10 cycles … in contrast,
the ASSLSBs without DABDT shows stable capacity initially but begins to decay after 60 cycles."
저자는 이를 "interfacial activation" 이라 부른다 `[인쇄]`.

`[해석]` Fig. 2d 의 첫 방전 **1643** 과 Fig. 3e 의 1사이클 **≈1300** 이 어긋난다 (§7.1 과 같은 문제).

### 7.3 Fig. 3f — 황 이용률 (★ 분모를 역산할 수 있는 그림)

`[인쇄, 그림 안]` 사이클별 이용률 %:

| 사이클 | 2 | 10 | 20 | 25 | 50 | 75 | 100 |
|---|---|---|---|---|---|---|---|
| with DABDT | **90.5** | 98.1 | 98.2 | **99.3** | 98.3 | 95.0 | 88.1 |
| without DABDT | 56.2 | 56.2 | 55.6 | 55.9 | 54.7 | 47.2 | **32.9** |

**[재현] 이용률 × 1675 = Fig. 3e 의 용량과 맞는가:**
90.5 % → 1516 (Fig. 3e 2사이클 ≈1520 ✓) · 99.3 % → 1663 (≈1650–1700 ✓) · 88.1 % → 1476 (≈1480 ✓) ·
56.2 % → 941 (≈950 ✓) · 32.9 % → 551 (≈520 ✓). **→ "sulfur utilization" = 용량 ÷ 1675 mAh g⁻¹(S)
로 확정** (G10 해소).

`(Li2S)` 환산 `[재현]` ×0.698: with DABDT 2사이클 **1058** · 25사이클 **1161** · 100사이클 **1030**;
without DABDT 2사이클 **657** · 100사이클 **385**.

`[재현]` 위 7개 점의 산술평균은 with 95.4 %, without 51.2 % — 본문의 97.04 % / ~48.5 % 와 다르다.
저자의 평균은 100개 전 사이클 평균일 것이다 `[해석]`.

> ★ `[해석]` **25사이클 황 이용률 99.3 %** 는 "거의 모든 황이 Li2S 까지 갔다" 는 뜻이다.
> 그런데 같은 논문 Fig. 4d 의 **XPS Li2S/LiPSs 면적비는 방전 상태에서 평균 0.1583** 이다 (§8.2).
> 황의 99 % 가 Li2S 라면 이 비는 1 보다 훨씬 커야 한다. **두 주장이 양립하지 않는다** (§12.4).

### 7.4 Fig. 3g — 60 °C, 0.2 C, 125 사이클

`[도표]` 용량 ≈1370(1사이클) → ≈1500–1600(안정), CE ≈100 %.
`[인쇄]` "after 125 cycles at 60 °C and 0.2 C, the capacity decay rate is as low as 0.0009 % per cycle."
`[재현]` 0.0009 %/cyc × 125 = 0.11 % 손실 → 유지율 99.89 %. 그림의 1370 → 1550 (증가)와는
**부호가 반대다** — 감쇠율을 (첫/끝) 중 무엇 기준으로 계산했는지 불명.

### 7.5 Fig. 3i — 0.3 C, 500 사이클 (★ 수명의 본체)

`[인쇄, 그림 안]` 상온 유지율 **88.67 %**, 감쇠율 **0.0228 % cycle⁻¹**;
60 °C 유지율 **99.62 %**, 감쇠율 **0.0008 % cycle⁻¹**.
초록 `[인쇄]`: 500 사이클 후 황 이용률 상온 **70.14 %**, 60 °C **94.81 %**.

`[재현]` 70.14 % × 1675 = **1175 mAh g⁻¹(S)** = **820 mAh g⁻¹(Li2S)**;
94.81 % × 1675 = **1588** = **1108**.
`[재현]` 유지율에서 역산한 초기값: 상온 1175 / 0.8867 = **1325 mAh g⁻¹(S)** (= 이용률 79.1 %);
60 °C 1588 / 0.9962 = **1594** (= 95.2 %).
`[재현]` 0.0228 %/cyc × 500 = 11.4 % 손실 → 88.6 % ✓ 자기정합.

`[도표, Fig. 3i]` **상온 곡선은 단조감소가 아니다** — 5사이클 ≈1400 에서 220–250사이클 ≈1000 까지
떨어졌다가 500사이클에 ≈1180 으로 **회복한다**. 60 °C 곡선은 ≈1150 에서 시작해 끝에서 ≈1550–1600
으로 **증가한다**. 본문은 이를 "minor fluctuations … recover quickly, demonstrating … good
self-healing ability" 로 설명한다 `[인쇄]`.

> `[해석]` **"유지율" 의 기준 사이클이 정의되지 않았다.** 60 °C 곡선이 끝에서 시작보다 높은데
> 유지율 99.62 % 가 나오려면 그림에 보이지 않는 더 높은 1사이클 값(≈1594)이 있어야 한다.
> 그리고 상온 곡선의 U자 거동은 "self-healing" 보다 **실온 변동 또는 스택 압력 이완/재접촉**으로
> 설명하는 것이 더 단순하다 — 저자는 압력을 기록하지 않았다 (G6).
> `[도표]` CE 산점은 ~100 % 에 모여 있으나 **100 % 를 넘는 점들과 440사이클 근처 ~5 % 의 점**이
> 섞여 있다 (단일 셀의 노이즈).

### 7.6 "안정" 이 CE 인가 용량인가

`[해석]` 이 논문에서 **CE 는 어떤 그림에서도 정량값으로 인쇄되지 않았다** ("close to 100 %" 만).
"안정" 주장의 근거는 전부 **용량 유지율**이고, 그것도 셀 1개 기준이다 (G9).

### 7.7 Fig. 3h — 문헌 비교 버블차트

`[인쇄, 그림 안]` 가로축 Sulfur Utilization (%), 세로축 Capacity Decay Rate (% cycle⁻¹),
버블 면적 = 사이클 수. 찍힌 선행 연구:

| 라벨 `[인쇄]` | 비고 |
|---|---|
| 0.1 C, S-super P-Li10GeP2S12-EVA (30 °C) | 감쇠율 ~12 %/cyc |
| 0.1 C, S-P2S5-C-LPSC | 감쇠율 ~11 %/cyc |
| 0.1 C, S@CNTs-Li10GeP2S12 | |
| 0.1 C, CNG–S–Li5.5PS4.5Cl1.5 | **Yu 2024 그룹(Nazar)의 SE 와 같은 조성** |
| 0.2 C, S-hCNC-Li7P3S11 (30 °C) | |
| 0.5 C, CNT@Co/S-LPSC | |
| 1 C, MCS-3–S–Co | |
| 1.19 C, S/LGPS/CNT/LiI | |
| 2 C, S/KB-Super P-LBPSI | **= `raw/papers/wang2023_…` (Dong Wang, Nat. Commun. 2023)** |
| 2 C, S-KB-MIECs (60 °C) | **= Nat. Mater. 24, 243 (2025) 혼합전도체 논문 [8]** |
| **0.2 C, this work (1st / 6th / avg.)** | 별표 3개, 이용률 83–97 % |

`[해석]` 비교축이 **이용률과 감쇠율 둘뿐**이다. **로딩·면적용량·온도·전압창이 축에 없다.**
2 C·5000사이클 데이터(가장 큰 원)가 이용률 55–60 % 대에 있는 것은 당연한 trade-off인데,
이 차트는 그것을 "뒤처진 연구" 로 보이게 배치한다. 상세 수치는 Tab. S1 (미확보, G14).

---

## 8. p.7–8 — Fig. 4: XPS depth profiling · DRT

### 8.1 Fig. 4a–b — XPS 깊이 프로파일 (10 사이클 후, 방전 상태)

`[인쇄]` 스퍼터링 속도 **0.1 nm s⁻¹**, **20 s / cycle** → `[재현]` 사이클당 **2 nm**, 10사이클 = 20 nm.
`[인쇄, 그림 안]` 할당된 피크: C-F, Li-F, C-O, C=O, Li-O, C-NH2, O-C=O, C-O-C, C-C, S-C, R-SH,
LPSs, P–S–Li, P-S-P, Li2S.
`[인쇄]` with DABDT 는 "sulfur species are uniformly distributed from the surface to the bulk",
without DABDT 는 "a clear depth-dependent variation".

> `[해석]` **Li-F 와 C-F 가 둘 다 잡힌다.** Li-F 는 **LiTFSI 의 비가역 분해 생성물**이다.
> §9.2 에서 저자는 ex situ FTIR 로 "no chemical bond breakage occurs in TFSI⁻ … without
> irreversible decomposition" 라고 결론하는데, **같은 논문의 XPS 가 Li-F 를 보여준다.**
> 정량(면적비)이 없어 양은 모르지만, "완전 가역" 주장은 과하다.

### 8.2 Fig. 4c–d — Li2S / LiPSs 면적비

`[인쇄, Fig. 4c 안]` 3번째 스퍼터링(≈6 nm): Li2S:LPSs = **0.1839**(with) vs **0.0894**(without).
`[인쇄, Fig. 4d 안]` 스퍼터링 사이클별 비 (%):

| 사이클 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | **평균** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| with DABDT | 24.92 | 18.94 | 13.89 | 18.39 | 15.58 | 16.98 | 13.61 | 12.45 | 10.66 | 12.87 | **15.83** |
| without DABDT | 0.11 | 9.22 | 8.85 | 7.78 | 6.13 | 8.94 | 5.64 | 7.60 | 4.64 | 5.42 | **6.43** |

> `[재현]` **Fig. 4c 의 without 값 0.0894 가 Fig. 4d 의 3번째 사이클 값 7.78 % 와 다르다**
> (8.94 % 는 5번째 사이클 값이다). 둘 중 하나는 라벨 오류다.
> `[해석]` 더 중요한 것: **방전 상태에서 Li2S:LiPSs 가 with DABDT 에서도 평균 0.158 밖에 안 된다
> — 즉 Li2S 가 소수다.** 그런데 §7.3 은 황 이용률 99.3 % 를 주장한다. 두 결과는 양립하지 않는다.
> (완화 요인: 황화물 SE 의 P–S–Li 와 LiPSs 의 S 2p 결합에너지가 심하게 겹쳐 분해능이 낮다.
> 그러나 **그 사실 자체가 이 정량의 신뢰도를 낮춘다.**)

### 8.3 Fig. 4e–i — DRT

`[인쇄]` with DABDT 는 "the relaxation peaks corresponding to polysulfide conversion and Li2S
nucleation display a clear dynamic balance relationship"; without DABDT 는 "an additional
relaxation process appears … (e.g., upon discharging to ~1.3 V), indicating extra interfacial
polarization".
`[도표, Fig. 4f/4i]` τ1–τ4 네 개의 이완 영역이 라벨돼 있고 τ4 (~1–10 s) 가 가장 크다.
`[해석]` **τ1–τ4 를 어떤 물리 과정에 귀속했는지 본문에 할당표가 없다.** "polysulfide conversion",
"Li2S nucleation" 이라는 말만 있고 어느 τ 인지 명시하지 않는다. DRT 의 전형적 약점이다.

### 8.4 Fig. 4g, 4j — R_ct, R_diff, D_Li⁺ (★ 결정적)

`[도표, Fig. 4g]` 가로축은 방전(1.5→1.2→0.9→0.6) 후 충전(0.9→1.2→1.5→1.8→2.1→2.4) V:

| | 범위 (with DABDT) | 범위 (without DABDT) |
|---|---|---|
| **R_ct** | ≈2 – 85 Ω | ≈38 – 192 Ω |
| **R_diff** | ≈150 – 3900 Ω | ≈450 – 4400 Ω |

`[해석]` R_ct 는 분명히 낮아졌다 (특히 충전 2.1 V 에서 10 vs 192 Ω). 그러나 **R_diff 는 충전
0.9–1.5 V 구간에서 거의 같다** (3650 vs 4150, 3350 vs 3700, 3900 vs 4100). 본문의 "Both R_ct and
R_diff … are significantly lower" 는 R_diff 에 대해서는 과장이다.
(세로축 라벨이 저항인데 `-Z″(Ω)` 로 인쇄돼 있다 — 조판 오류로 보인다 `[해석]`.)

`[도표, Fig. 4j]` **Li⁺ 확산계수 (세로축 3×10⁻¹⁰ – 1×10⁻⁹ cm² s⁻¹)**:

| 전압 | 1.5↓ | 1.2↓ | 0.9↓ | 0.6 | 0.9↑ | 1.2↑ | 1.5↑ | 1.8↑ | 2.1↑ | 2.4↑ |
|---|---|---|---|---|---|---|---|---|---|---|
| with DABDT | ≈6.2e-10 | **≈9.7e-10** | ≈5.5e-10 | ≈5.8e-10 | ≈5.4e-10 | ≈5.8e-10 | ≈5.8e-10 | ≈6.2e-10 | ≈5.0e-10 | ≈5.0e-10 |
| without DABDT | ≈6.2e-10 | ≈4.8e-10 | ≈5.0e-10 | ≈5.4e-10 | ≈5.2e-10 | ≈5.6e-10 | ≈5.5e-10 | ≈6.0e-10 | ≈4.8e-10 | ≈4.9e-10 |

> ★★ **[해석] 이 논문의 가장 심각한 내적 모순.**
> 본문은 Fig. 4j 를 두고 "the ASSLSBs with DABDT exhibits markedly higher diffusion coefficients
> across the entire voltage range, consistent with the trend observed in the CV-based calculations
> in Fig. 3c" 라고 쓴다 `[인쇄]`. **그림은 그렇지 않다.** 10개 전압점 중 **9개에서 두 곡선이
> 겹치고**, 유일하게 벌어지는 1.2 V(방전)에서도 차이는 **2.0배**다.
> 그리고 Fig. 3c 의 D(≈2×10⁰ cm² s⁻¹)와 Fig. 4j 의 D(≈5×10⁻¹⁰ cm² s⁻¹)는 **10¹⁰배** 다르다.
> → **"Li⁺ 확산을 3자릿수 올렸다" 는 이 논문의 두 번째 축(dipole-layer acceleration)은
> 저자 자신의 EIS/DRT 데이터가 반증한다.** 신뢰할 수 있는 값은 Fig. 4j 쪽이고, 그 값은
> **차이가 사실상 없다**고 말한다.

---

## 9. p.8–10 — Fig. 5: ex situ 분광과 두 번째 DFT

### 9.1 Fig. 5a–d — ex situ 마이크로-FTIR

`[인쇄]` DABDT 의 벤젠 C=C(~1570/1512/1492)와 -SH(~2470)는 "remained unchanged throughout cycling,
with only weak reversible variations in peak intensity"; -NH2(~3440/~3400)는 "significant reversible
shifts and intensity changes" — 방전 초기에 대칭신축 적색이동·비대칭신축 청색이동, 중후기에 역전,
충전에서 완전 복원. 결론 `[인쇄]`: "-NH2 acts as the core site for reversible Li⁺ coordination and
hydrogen bonding, while the benzene ring and -SH serve as a stable, inert backbone."
LiTFSI 쪽: S-N-S(~1050), CF3(~1171/1227), O=S=O(~1380)가 방전 중 "slight red shifts and weakened
intensities, which fully recovered after charging" → "reversible dissociation-reassociation behavior
of LiTFSI without irreversible decomposition" `[인쇄]`.

> `[도표, Fig. 5a]` **2400–3500 cm⁻¹ 구간(= -SH 와 -NH2 가 있는 곳)은 모든 전압에서 평탄한
> 잡음이다.** 회색 띠로 위치만 표시돼 있고 봉우리가 보이지 않는다. 신호가 뚜렷한 곳은
> 700–1700 cm⁻¹(LiTFSI + 벤젠 고리)뿐이다.
> `[해석]` **이 논문의 "동적 계면 조절자(dynamic interface regulator)" 라는 핵심 서사의 유일한
> 실측 근거가 -NH2 의 가역 이동인데, 그 봉우리가 그림에서 보이지 않는다.** 봉우리 위치 이동을
> 주장하려면 확대도와 피크 피팅이 필요한데 둘 다 없다.
> Fig. 5b–d 의 "chemical image" 는 공간 구조가 없는 매끄러운 2색 그라데이션 맵이어서
> 정량 근거로 읽기 어렵다 `[도표]`.

### 9.2 Fig. 5e–f — ex situ XRD / Raman heatmap

`[인쇄]` XRD: ~27°(LGPS), ~30/32/34°(DABDT), ~42/61°(LiTFSI) 는 전 과정에서 위치가 유지 →
"the crystal structure of LGPS is maintained. DABDT and LiTFSI remain as structurally stable
additives". **~47° 와 ~53° 를 Li2S 로 할당**하고, 방전에서 커지고 충전에서 작아진다고 기술.
Raman: 방전 초 ~470 cm⁻¹ 에 S8, 깊어지면 약해지고 단쇄 LiPSs/Li2S 신호 등장, 방전 말에 Li2S 지배,
충전에서 역전 `[인쇄]`.

> `[해석]` 세 가지 유보.
> 1. **Li2S 의 최강 반사 (111) 이 27.0° 인데 저자는 27° 를 LGPS 로 할당했다.** 두 상이 겹치는
>    자리다. 대신 약한 47°·53° 로 Li2S 를 추적하는데, Li2S(220)은 44.8° 이지 47° 가 아니다.
> 2. `[도표, Fig. 5e]` 히트맵에서 **강도 변화는 거의 전부 25–32° 구간에서 일어나고 40–65° 구간은
>    전 전압에서 균일한 파란색(저강도)이다.** 즉 "47°·53° Li2S 피크의 생성·소멸" 은 매우 약한
>    신호를 읽은 것이다.
> 3. `[도표, Fig. 5f]` Raman 의 지배적 신호는 **~370 cm⁻¹ 의 붉은 덩어리**인데, 이 위치는
>    Li2S 와 **티오포스페이트 PS4³⁻ 진동**이 겹치는 영역이다. 디콘볼루션이 없다.
> → §9.2 의 결론은 **정성적**으로만 받아들이고, 정량(이용률·전환율) 근거로 쓰면 안 된다.

### 9.3 Fig. 5g — 황종 결합에너지 (DFT) `[인쇄, 그림 안]`

| 황종 | LGPS(100)-DABDT | LGPS(100)-LiTFSI | 차이 `[재현]` |
|---|---|---|---|
| S8 | −0.73 eV | −0.65 eV | −0.08 |
| Li2S8 | −1.89 | −1.31 | −0.58 |
| Li2S6 | −1.69 | −1.11 | −0.58 |
| Li2S4 | −0.79 | −0.36 | −0.43 |
| Li2S2 | −2.08 | −1.39 | −0.69 |
| **Li2S** | **−4.21** | **−2.39** | **−1.82** |

`[인쇄]` "for all examined sulfur species, the LGPS-DABDT interface exhibits more negative binding
energies … constructing a universally strong chemical affinity region within the cathode, which
helps anchor the active material, prevent its loss, and guide the uniform nucleation of Li2S."

`[해석]` 두 가지. (a) Li2S4(−0.79)가 Li2S6(−1.69)보다 **약하게** 결합하는 비단조 경향은 설명이 없다.
(b) **Li2S 를 −4.21 eV 로 가장 강하게 붙잡는 것은 충전(Li2S 분해)에는 불리하다.** "가역성이
좋아진다" 는 주장과 같은 방향이 아니다. 흡착이 너무 강하면 촉매는 피독된다 (Sabatier).

### 9.4 Fig. 5h — Gibbs 자유에너지 프로파일 (★ "표적 촉매" 의 근거)

`[인쇄, 그림 안]` 단계별 ΔG (eV), 경로 S8 → *S8 → *Li2S8 → *Li2S6 → *Li2S4 → *Li2S2 → *Li2S:

| 단계 | LGPS-DABDT | LGPS-LiTFSI | LGPS |
|---|---|---|---|
| S8 → *S8 | −0.88 | −0.82 | −1.36 |
| *S8 → *Li2S8 | −3.38 | −2.91 | −3.54 |
| *Li2S8 → *Li2S6 | +0.14 | +0.19 | +0.27 |
| *Li2S6 → *Li2S4 | **+1.36** | **+1.14** | **+1.49** |
| *Li2S4 → *Li2S2 | −0.09 | +0.20 | −0.19 |
| **\*Li2S2 → \*Li2S** | **−1.11** | −0.05 | −0.43 |

`[인쇄]` "for the kinetically slowest rate-determining step Li2S2 → Li2S, the LGPS-DABDT interface
exhibits the most negative reaction free energy among the three systems … meaning that this step has
the largest driving force and the lowest activation barrier."

> ★★ `[해석]` **두 겹의 문제.**
> 1. **ΔG 는 활성화 장벽이 아니다.** 반응 자유에너지가 더 음수라는 것은 열역학적 구동력이
>    크다는 뜻이지 **동역학 장벽이 낮다는 뜻이 아니다.** 저자는 두 개념을 한 문장에서 동일시한다.
>    장벽을 말하려면 전이상태(NEB)가 필요한데 이 그림에는 없다 (Fig. 1j 의 0.48 eV 는 Li–DABDT
>    복합체 형성이지 황 전환이 아니다).
> 2. **저자의 자기 데이터에서 율속단계는 Li2S2 → Li2S 가 아니다.** 세 계 모두 가장 큰 양의 ΔG 는
>    ***Li2S6 → *Li2S4** (+1.36 / +1.14 / +1.49 eV)다. 그리고 **그 단계에서 DABDT(+1.36)는
>    LiTFSI(+1.14)보다 나쁘다.** 즉 이 DFT 는 "DABDT 가 실제 율속단계를 악화시킨다" 고 말하고
>    있고, 저자는 그 단계를 논의하지 않은 채 마지막 단계만 "targeted catalysis" 라는 분홍 음영으로
>    강조한다. **그림 안의 분홍 음영이 논증을 대신하고 있다.**

---

## 10. 우리 연구와의 접점 (이식 가능 / 불가 표)

우리 기준선: **pristine Li2S : LPSCl : AB = 30 : 50 : 20 + Li–In, 목표 500–600 mAh g⁻¹**
([[li2s-assb-reference-cell]]).

| 항목 | 이 논문 | 우리 | 이식 가능? |
|---|---|---|---|
| 활물질 | **S8**(방전 선행) | **Li2S**(충전 선행) | ✗ **불가.** 첫 충전 활성화에 대해 이 논문은 아무 말도 하지 않는다 |
| SE | **LGPS** (Li10GeP2S12, Ge 함유) | **LPSCl** (Li6PS5Cl) | ✗ 환원 안정성이 다르다. LGPS 의 Ge⁴⁺ 환원은 LPSCl 보다 심하다 — 0.6 V vs Li–In 하한의 의미가 서로 다르다 |
| 음극 | Li–In `[도표, 축라벨]` | Li–In | ○ 같다 (조성·두께 미기재는 양쪽 공통 문제) |
| 전압창 | 0.6–2.4 V vs Li–In (GITT 는 ~0.3–3.0 V) | 우리 창은 실험 노트가 정본 | △ 하한 0.6 V 는 **우리가 따라가면 안 되는 수치** — SE 환원 영역 |
| 탄소 | "S/C" 뿐, 종류·함량 미기재 (G2) | AB 20 wt% | ✗ 비교 불가 |
| 혼합 | **전무** (G3) | 볼밀 조건 기록 중 | ✗ [[composite-cathode-mixing-routes]] 에 행을 못 만든다 |
| **첨가제 아이디어** | **-SH + -NH2 양쪽을 가진 방향족 소분자를 소량 넣는다** | AB 외 첨가제 없음 | △ **개념만 이식 가능.** 무게 대가가 작다는 점은 Cronk 2026 의 "매개체를 밀링으로 미리 만든다" 와 경쟁 가능. **단 G12(염산 2당량)를 먼저 해결해야 한다** |
| 전도도 측정 | **없음** (G7) | DC 분극 예정 | ✗ 가져올 방법이 없다 |
| D_Li⁺ 측정 | CV-Randles-Sevcik(불가) + EIS/DRT(≤2배) | 미실시 | ✓ **반면교사로 이식**: 고체셀에 Randles-Sevcik 을 쓰지 않는다 |
| SE 기여 대조셀 | **없음** (G11) | Cronk 방식 1셀 예정 | ✓ 이 논문이 그 필요를 다시 증명한다 |

### 10.1 질문 카드 라우팅 — [[reference-cell-500-600-mahg]]

| 가설 | 이 논문의 기여 |
|---|---|
| **H1 (활성화 / 전위 창)** | **없음.** S8 출발이라 첫 충전 활성화가 존재하지 않는다. Li2S 첫 충전 과전압·컷오프에 대해 한 글자도 없다. Huang 2026 과 같은 공백이다 |
| **H2a (전자 네트워크)** | **없음 — 측정이 없다.** DFT 밴드갭 1.63 → 1.26 eV 라는 **계산값**뿐이다. [[interface-quality-not-bulk-conductivity]] 의 찬반 어느 쪽으로도 쓸 수 없다. (방향만 보면 Huang 쪽 = 전자 전도 증가) |
| **H2b (이온 네트워크)** | **방법론적 기여.** 같은 셀에서 CV-Randles-Sevcik(10⁶배)과 EIS/DRT(≤2배)가 충돌한다 → **H2b 를 CV 로 판정하면 안 된다.** 그리고 **믿을 만한 쪽(EIS/DRT)은 "차이 없음" 을 말한다** — 첨가제로 Li⁺ 확산을 바꿨다는 주장에 대한 간접 반증 |
| **H3 (입자)** | **없음.** 입도·결정성 정보 전무 |
| **H4 (단위 · SE redox)** | **강한 기여 (★).** ① "sulfur utilization" 의 정의식을 역산으로 확정할 수 있는 드문 사례(§7.3). ② **Fig. 2g 에서 plateau II 가 자기 이론용량의 111 %, plateau III 가 100.3 %** — 황 이외 리독스의 직접 신호. ③ 하한 0.6 V vs Li–In + LGPS + SE 대조셀 없음. **이 위키의 "이론 초과 = SE redox 먼저 의심" 목록에 추가된다** |
| **H5 (기계적)** | **약한 기여.** "~80 % 부피 팽창" 을 문제로 들고 사이클 후 단면 SEM(Fig. S13)으로 균열 유무를 비교했다고 하지만 **SI 미확보**라 검증 불가. 압력·구속 조건도 없다 (G6) |

---

## 11. 3편 대조 — Wang 2026 vs Huang 2026 vs Yu 2024 (★ 이 digest 의 핵심 산출물)

### 11.1 셀·설계 축

| | **Yu 2024** | **Huang 2026** | **Wang 2026 (이 논문)** |
|---|---|---|---|
| 개입 층위 | **호스트** (탄소 골격 자체를 바꿈) | **첨가제** (6 wt%) | **첨가제** (**함량 미기재**) |
| 개입 물질 | CuS 나노결정 / N-도핑 탄소 | 고엔트로피 황화물 NiCoCuFeMnS_x | **유기 소분자 DABDT + LiTFSI** |
| 활물질 | **nano-Li2S** | S8 | **S8** |
| SE | Li5.5PS4.5Cl1.5 | Li6PS5Cl | **Li10GeP2S12 (LGPS)** |
| 음극 | Li–In | Li–In | Li–In `[도표]` |
| 로딩 | 2 / 4 / 10 mg cm⁻²(Li2S) | 1.5–1.7 / 6.0 mg cm⁻²(S) | **미기재** |
| 복합양극 조성 | 부분 미기재 | 전부 명시 (42:6:12:40) | **전부 미기재** |

### 11.2 "무엇을 얼마나 고쳤나"

| | Yu 2024 | Huang 2026 | Wang 2026 |
|---|---|---|---|
| 이용률 개선 | **51 → 91 %** (첫 충전, Li2S 기준) | **39 → 76 %** (0.1 C 첫 방전, S 기준) | **48.5 → 97.04 %** (0.2 C 100사이클 평균, S 기준) |
| 대조군의 정체 | NC 호스트(CuS 없음) | 첨가제 0 wt% (첫 사이클 1회만) | **LiTFSI 있음·DABDT 없음** (DABDT 단독 대조군 없음, G13) |

### 11.3 ★ 전도도 축 — 이 논문은 참여하지 않는다

| | Yu 2024 | Huang 2026 | **Wang 2026** |
|---|---|---|---|
| **σ_e⁻** | **÷200** (5.7×10⁻² → 2.9×10⁻⁴ S cm⁻¹) | **×14** (1.71 → 23.80 mS cm⁻¹) | **측정 없음.** DFT 계면 밴드갭 1.63 → 1.26 eV 만 |
| **σ_Li⁺** | ×1.8 (3.5 → 6.4 ×10⁻⁵ S cm⁻¹) | ×270 (2.41×10⁻⁵ → 6.50×10⁻³ mS cm⁻¹) | **측정 없음** |
| **D_Li⁺** | GITT | GITT | **CV 10⁶배 ↔ EIS/DRT 2배 (자기모순, §8.4)** |
| **활물질–황화물 계면 친화** | DFT Li2S 흡착 **−3.2 vs −2.1 eV** | 토모그래피 분산 + NEB 0.20 vs 0.25 eV | DFT Li2S 결합 **−4.21 vs −2.39 eV** |

> ★★ **결론.** 이 위키의 현재 논지 — *σ_e⁻ 의 방향은 무관하고(Yu 는 200배 낮추고 Huang 은
> 14배 올려서 비슷한 개선), 공통으로 움직인 것은 σ_Li⁺ 와 **활물질–황화물 계면 친화**뿐*
> ([[interface-quality-not-bulk-conductivity]]) — 에 대해 Wang 2026 은:
> - **σ_e⁻ 축: 기여 없음** (측정 안 함). 반증도 지지도 아니다.
> - **σ_Li⁺ 축: 약한 반증.** 믿을 만한 측정(EIS/DRT)이 "차이 없음(≤2배)" 인데도 이용률이
>   48.5 → 97 % 로 올랐다. σ_Li⁺ 가 공통 원인이라는 가설도 흔들린다.
> - **계면 친화 축: 지지.** 세 논문 모두 **Li2S 에 대한 계면 결합을 강화**했다는 DFT 를 댄다
>   (Yu −3.2, Wang −4.21 eV). 세 논문에서 **유일하게 같은 방향으로 움직인 양**이 다시 이것이다.
> → **남는 처방은 "전자든 이온이든 양을 늘려라" 가 아니라 "Li2S 와 황화물 사이의 계면을
>   화학적으로 설계하라" 다.** 다만 세 논문 모두 그 근거가 **DFT 흡착에너지**뿐이라는 점도
>   같다 — 실측으로 계면 친화를 재는 방법은 아직 이 위키에 없다 `[해석]`.

### 11.4 Wang 2026 이 둘보다 나은 점 / 못한 점

| | 나은 점 | 못한 점 |
|---|---|---|
| vs Huang 2026 | 사이클 수가 많다 (500 vs 160); GITT plateau 분해가 있다 | **조성·로딩·혼합·전도도가 전부 없다** (Huang 은 전부 있다) |
| vs Yu 2024 | 사이클 수가 많다 (500 vs 100/500); 기전 분광이 많다 | **활물질이 S8 이라 Li2S 첫 충전에 무근거**; 면적용량 계산 불가 |

---

## 12. 비판 (이 digest 의 판단) `[해석]`

### 12.1 "triple synergy" 의 세 축이 본문과 그림에서 다르다
본문·초록·결론은 **"strong chemical bonding / dipole-layer acceleration / targeted catalysis"**,
Scheme 1b 의 번호 라벨은 **"① Stabilized Interfacial Anchoring / ② Accelerated Li⁺ transport /
③ Facilitates e⁻ transport"**. **촉매와 전자전도가 세 번째 자리를 번갈아 차지한다.**
실제로 이 논문이 다루는 축은 **넷**(계면 고정·이온·전자·촉매)이고, 그중 **전자 축은 측정이
전혀 없으며**(G7) **이온 축은 자기모순**(§8.4)이다. 남는 것은 계면 고정과 촉매 두 축인데,
둘 다 근거가 **DFT 와 GITT 분해**에 집중돼 있다.

### 12.2 증거–주장 대응표 (각 축을 무엇이 받치는가)

| 주장 축 | 받치는 측정 | 이 digest 의 판정 |
|---|---|---|
| ① 강한 화학결합 (계면 고정) | DFT 전하이동 0.269 vs 0.116 \|e\|, S–Li 2.7 Å, 결합에너지 6종; ex situ XRD 피크 위치 불변; 사이클 후 SEM(Fig. S13, 미확보) | **DFT 는 일관되나 실측 뒷받침이 약하다.** XRD 위치 불변은 "DABDT 가 결정 구조를 유지한다" 는 뜻이지 "LGPS 에 배위했다" 는 직접 증거가 아니다. **배위 결합의 실측 증거(예: Li NMR, S 2p 화학이동)가 없다** |
| ② 쌍극자층 → Li⁺ 가속 | CV-Randles-Sevcik D_Li⁺; EIS/DRT D_Li⁺; R_diff | **기각 수준.** 두 측정이 10¹⁰배 어긋나고, 신뢰 가능한 쪽은 차이가 없다 (§8.4) |
| ③ 표적 촉매 (Li2S2→Li2S) | DFT ΔG; GITT plateau III 28.94 → 50.13 %; XPS Li2S/LiPSs 비; CV ΔQ_c 513 mAh/g | **부분 지지, 단 심각한 유보 셋.** (a) DFT 의 실제 율속단계는 Li2S6→Li2S4 이고 거기서 DABDT 가 더 나쁘다 (§9.4); (b) plateau III 가 자기 이론의 100.3 % 라 SE redox 혼입 의심 (§5.3); (c) XPS 비가 0.16 으로 Li2S 가 소수 (§8.2) |
| ④ 전자 전도 네트워크 | DFT PDOS / 밴드갭 | **근거 없음.** 복합체 전자 전도도 측정 0회. 게다가 **SE 밴드갭 축소는 고체전지에서 바람직하지 않다** |

### 12.3 전압창이 그림마다 다르다
Fig. 2a–d·3a·3e: **0.6–2.4 V vs Li–In**. Fig. 2e–f(GITT): 충전 상한 **3.0 V**, 방전 하한 0.6 V 아래.
Fig. 4g·4j: 0.6–2.4 V. **창이 다른 데이터로 같은 셀을 논증한다** — GITT 총용량(1673)이 0.2 C
용량(1643)보다 큰 것은 율속 차이만이 아니라 **창 차이** 때문일 수 있다. 본문에 설명이 없다.

### 12.4 "97 % 이용률" 과 "Li2S:LiPSs = 0.16" 은 양립하지 않는다
§7.3 과 §8.2 가 서로를 부정한다. 가능한 설명은 셋: (i) XPS 의 LiPSs 피크가 실제로는 LGPS 의
P–S–Li 를 포함한다, (ii) 용량의 상당 부분이 황이 아닌 것(LGPS 환원·LiTFSI 분해)에서 나온다,
(iii) 둘 다. **어느 쪽이든 "97.04 % 황 이용률" 을 액면 그대로 인용하면 안 된다.**

### 12.5 DABDT·2HCl — 저자가 피한 화학 (★ 우리에게 가장 실질적인 경고)
전구체는 **이염산염**이다. 황화물 SE·Li2S 계에서 HCl 은 **H2S 를 낼 수 있고**, -SH 자체도
Li2S/LPSCl 과 반응해 Li 티올레이트 + H2S 를 만들 수 있다. EDS 에 Cl 이 분명히 잡혀 있는데
(Fig. 1c) 본문에는 Cl 에 대한 언급이 **한 글자도 없다.** 전처리(탈염산화·건조·중화) 여부도 모른다.
`[해석]` 우리가 이 아이디어를 LPSCl 계로 가져오려면 **먼저 free base 형태(2,5-diamino-1,4-
benzenedithiol)를 쓸 수 있는지, 혹은 DABDT·2HCl 과 LPSCl 의 가스 발생을 재야 한다.**

### 12.6 셀 1개 · 오차 없음 · 셀 간 수치 불일치
Fig. 2d(1643) ↔ Fig. 3e 1사이클(≈1300) ↔ Fig. 3d 0.1 C(≈1350) ↔ Fig. S11 0.5 C(1270) 이 서로
맞지 않는다 (§7.1). **"with DABDT" 라는 이름 아래 최소 3~4개의 서로 다른 셀이 섞여 있다.**
오차막대·셀 개수·재현 횟수가 한 군데도 없다.

### 12.7 Experimental 절을 본문에서 통째로 뺀 편집
*Energy Storage Materials* 의 조판 관행이기도 하지만, **"molecular coordination engineering" 이라는
제목을 내걸고 분자를 어떻게 넣었는지(용매? 건식 혼합? 농도? 온도?)를 본문에 한 줄도 안 쓴 것**은
재현성 측면에서 심각하다. 이 digest 가 G1–G6 을 메우지 못하는 이유 전부가 여기서 온다.

---

## 13. 이 저장소가 가져갈 것

1. **[[interface-quality-not-bulk-conductivity]] 에 세 번째 사례로 올린다 — 단 "약한 지지" 로.**
   계면 친화(DFT Li2S 결합 −4.21 vs −2.39 eV)만 세 논문의 공통 방향이고, σ_e⁻·σ_Li⁺ 는
   이 논문이 측정하지 않았다. **반론 항목으로 "세 논문 모두 계면 친화의 근거가 DFT 뿐" 을 추가.**
2. **[[reference-cell-500-600-mahg]] H4 에 아홉 번째 "이론 초과/근접" 사례를 추가한다** —
   근거는 본문 수치가 아니라 **우리의 [재현]**: Fig. 2g 에서 plateau II = 자기 이론의 111 %.
   → **`LPSCl + AB (80:20)` 대조셀**(Cronk 2026 방식)의 우선순위를 다시 올린다.
3. **방법 규율 하나를 세운다**: **고체셀의 D_Li⁺ 를 CV-Randles-Sevcik 으로 재지 않는다.**
   근거는 이 논문의 자기모순(§8.4) + 스캔속도 의존성(§6.2 (3)). GITT 또는 EIS/DRT 를 쓴다.
4. **첨가제 후보 목록에 "이작용기 방향족 소분자(-SH + -NH2)" 를 올리되 G12(염산 2당량)를
   선행 조건으로 묶는다.** 무게 대가가 작다는 점에서 Cronk 의 밀링 유래 매개체와 경쟁 가능.
5. **LGPS 계 논문의 수치를 LPSCl 계로 옮기지 않는다** — 특히 0.6 V vs Li–In 하한과
   "황 이용률 97 %". SE 의 환원 안정성이 다르다.
6. **읽기 규율**: 이 논문은 **본문 문장과 그림이 어긋나는 지점이 최소 5곳**이다
   (§6.2 피크 분리 · §8.4 D_Li⁺ · §5.3 Fig. 2g 분모 · §9.4 율속단계 · §8.2 Fig. 4c↔4d).
   **그림을 먼저 보고 본문을 나중에 읽는** 이 위키의 절차가 그대로 정당화된 사례다.

---

## 14. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

크로핑 결과: `raw/figures/wang2026_molecular-coordination-triple-synergy-cathode-assb/`
**총 6장** (Scheme 1 + Fig. 1–5). 본문 그림은 이것이 전부이고 누락은 없다.
SI 그림(Fig. S1–S13 이상, Tab. S1)은 **SI 미확보로 한 장도 없다.**

| 파일 | 대상 | 봤는가 | 이 digest 에서 읽은 것 |
|---|---|---|---|
| `sch_1.png` | Scheme 1 (DABDT 구조·셀 모식도) | **봄 (전체)** | **범례에서 복합양극 성분 5종 확정**(S/C·LGPS·LiTFSI·DABDT·Li2S) · 3축 라벨 ①②③ · 바인더 없음 (§4) |
| `fig_1.png` | Fig. 1 (XRD·FTIR·EDS·DFT) | **봄 (전체)** | 밴드갭 1.26/1.63/1.77 · d-band −4.43/−6.51/−8.91 · 전하이동 0.269/0.116 · ΔG −0.60 · TS 0.48 · **EDS 에 Cl** · **FTIR 의 -SH/-NH2 영역이 잡음** (§5.1–5.2) |
| `fig_2.png` | Fig. 2 (충방전·GITT·CV·dQdV·모식) | **봄 (전체 + a–d, e–f 확대 재크롭)** | 4조성 첫 방전 · **CV 피크 분리 1.09 V 동일** · dQ/dV 1.32/1.21/1.77 vs 1.17/1.11/1.85 · **plateau 백분율 6개 전부** · **CV 축 라벨 `V vs. Li⁺/Li-In`** (§5.3, §6.1–6.2) |
| `fig_3.png` | Fig. 3 (CV 스캔·D_Li⁺·율속·사이클·이용률·문헌비교·500사이클) | **봄 (전체 + b–c, d–e, i 확대 재크롭)** | 기울기 89.2046/69.8239/0.0531/0.0411 · **D_Li⁺ 축이 `2.0E+0 cm² s⁻¹`** · 율속 9단계 · **이용률 14개 숫자 전부** · 문헌비교 11개 라벨 · 500사이클 유지율 (§6.2, §7.1–7.7) |
| `fig_4.png` | Fig. 4 (XPS depth·DRT·R_ct/R_diff·D_Li⁺) | **봄 (전체 + g·j 확대 재크롭)** | **Li2S/LiPSs 비 20개 숫자 + 평균 15.83/6.43** · **Li-F·C-F 피크 존재** · R_ct·R_diff 범위 · **D_Li⁺ 10개 전압점 — 두 곡선이 9곳에서 겹침** (§8.1–8.4) |
| `fig_5.png` | Fig. 5 (ex situ FTIR·chemical image·XRD/Raman heatmap·DFT 2종) | **봄 (전체)** | **결합에너지 12개 숫자 전부** · **ΔG 18개 숫자 전부** · **FTIR 2400–3500 cm⁻¹ 가 잡음** · XRD 히트맵 강도 변화가 25–32° 에 집중 · Raman ~370 cm⁻¹ 덩어리 (§9.1–9.4) |

**안 본 것 / 못 본 것**
- **SI 전체** — Experimental Section, Fig. S1–S13(이상), Tab. S1. **미확보.** 본문이 인용한
  Fig. S5(무DABDT CV)·S11(0.5 C 첫 5사이클)·S13(사이클 후 단면 SEM)·Tab. S1(문헌비교 수치)은
  전부 **검증하지 못했다.** 특히 **구조 안정성 주장의 유일한 실측 근거가 Fig. S13** 이다.
- Fig. 1c EDS 단면의 **전극 두께**는 읽지 않았다 — 100 µm 스케일바는 있으나 전극/집전체 경계가
  흐려 `[도표]` 로도 신뢰할 수 없다고 판단했다.
- Fig. 4a–b 의 3D XPS 스택에서 **개별 피크 면적**은 읽지 않았다 (3D 투시라 정량 불가).
  읽은 것은 **어떤 종이 할당됐는가**(Li-F 포함)뿐이다.
- Fig. 5b–d 의 chemical image 는 **정량값을 읽지 않았다** (컬러바가 `High/Low` 상대 눈금뿐).
- Fig. 2e–f GITT 의 **완화 전압값**(각 pulse 의 OCV)은 읽지 않았다 — 해상도상 불가.

**원문 내부 불일치 목록** (전부 §12 에 근거와 함께 기재):
① 본문 "3자릿수" ↔ Fig. 3b/3c 가 말하는 6자릿수 ·
② Fig. 3c D(≈10⁰) ↔ Fig. 4j D(≈10⁻¹⁰) ·
③ 본문 "peak separation 이 작아졌다" ↔ Fig. 2h 는 둘 다 1.09 V ·
④ 본문 "각 plateau 의 자기 이론용량 대비" ↔ Fig. 2g 의 실제 분모는 1675 전체 ·
⑤ 본문 "율속단계 Li2S2→Li2S" ↔ Fig. 5h 의 최대 ΔG 는 Li2S6→Li2S4 ·
⑥ Fig. 4c(0.0894) ↔ Fig. 4d(3번째 사이클 7.78 %) ·
⑦ Fig. 2d(1643) ↔ Fig. 3e 1사이클(≈1300) ↔ Fig. 3d 0.1 C(≈1350) ·
⑧ 본문·FTIR "LiTFSI 비가역 분해 없음" ↔ Fig. 4a/b 의 Li-F 피크 ·
⑨ 황 이용률 99.3 % ↔ XPS Li2S:LiPSs = 0.16 ·
⑩ Fig. 3g 60 °C 곡선은 상승 ↔ "감쇠율 0.0009 %/cyc".

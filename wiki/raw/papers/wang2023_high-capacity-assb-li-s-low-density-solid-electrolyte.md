---
title: "Wang et al. 2023 — Realizing high-capacity all-solid-state lithium-sulfur batteries using a low-density inorganic solid-state electrolyte (Nat. Commun. 14, 1895)"
description: "액상(THF) 합성 Li3PS4–2LiBH4 glass-ceramic SE(밀도 1.491 g cm⁻³, 일차입자 ~500 nm, 6.0 mS cm⁻¹ @25 °C)로 60 wt% 황 양극의 SE 부피분율을 35.4 vol%까지 올려 1144.6 mAh g⁻¹(S)·800 사이클을 낸 논문 — 활물질이 S8 이고 SI 미확보이며, 우리 30:50:20 은 이미 SE 48–52 vol%[재현]라 이 논문의 병목에 해당하지 않는다"
source_url: local-upload/9ada0d4c-High_capacity_ASSLSBs_with_low_density_SE.pdf
doi: 10.1038/s41467-023-37564-z
ingested: 2026-09-30
sha256: f703bd069bc8b8748ef6a1aa18df931ba4aa4f73252a0d1e8a25e2d2e3afd9c4
tags: [assb, sulfide-electrolyte, composite-cathode, mixing-process, li-in, units]
compare:
  system: "Li–S ASSB (Swagelok, 60 °C, 대기 중, 운전 스택압 50–60 MPa)"
  electrolyte: "Li3PS4–2LiBH4 (LPB) glass-ceramic argyrodite — THF 액상 합성, 밀도 1.491 g cm⁻³, 일차입자 ~500 nm, σ25 = 6.0 mS cm⁻¹(열간가압, 상대밀도 91.5 %) / 3.8(냉간압축, 86.0 %), Ea 0.216 eV; 분리층 80 mg @100 MPa ≈ 600 µm ≈ 102 mg cm⁻² [재현]. 대조군 SE: β-Li3PS4(≈1.81 g cm⁻³ [도표]) · LGPS(≈2.04 [도표])"
  cathode: "S : KB : LPB = 50 : 10 : 24 (w/w/w) = 59.5 : 11.9 : 28.6 wt% [재현] = 53.1 : 11.6 : 35.4 vol% [재현]; 바인더 없음, 성형 294 MPa 3 min"
  li2s_source: "해당 없음 — 활물질은 Li2S 가 아니라 원소황 S8 (Sigma ≥99.0 %)을 KB(Ketjenblack EC-600JD)에 160 °C 10 h melt-diffusion"
  mixing: "two-step — ① S+KB 160 °C 10 h 융합(복합체 황 83.3 wt%) → ② SE 와 건식 planetary BM 350 rpm 10 h, 45 mL ZrO2 jar (FRITSCH PULVERISETTE 7 premium line), Ar; 볼 재질·지름·개수·BPR 미기재"
  loading_mg_cm2: "2.0–3.0 (S, 기본) · 2.57 (800 사이클) · 4.2/4.6 (GITT) · ~6 (SI Fig. 20, SI 미확보)"
  anode: "Li–In — Li 박 3–4 mg (0.6 mm chip) + In 박 ⌀10 mm × 0.127 mm, 100 MPa 1 min. 논문 인쇄: ~0.62 V vs Li/Li⁺"
  first_charge: "해당 없음 — S8 양극이라 방전부터 시작. 전압창 0.5–2.5 V vs Li–In/Li⁺ = 1.12–3.12 V vs Li/Li⁺ [재현]"
  first_discharge_mAh_gS: "1047.5 @167.5 mA g⁻¹ (ICE 100.2 %) · 율속시험 최고 1144.6"
  first_discharge_mAh_gLi2S: "731.2 [재현] · 798.9 [재현]"
  cycle_capacity_mAh_gS: "1004.6 (초기) → 1068.1 (20 cyc, 최대) → 778.9 (800 cyc) @837.5 mA g⁻¹ CCCV. 이 중 황 기여는 >82 % [인쇄] → 최악 638.7 [재현]"
  cycle_capacity_mAh_gLi2S: "701.2 → 745.5 → 543.7 [재현] (황 기여 하한 적용 시 445.8 [재현])"
  areal_mAh_cm2: "2.58 초기 → 2.00 (800 cyc) [재현] @2.57 mg(S) cm⁻² · 2.86 [재현] @2.5 mg · 6.0 [재현] @~6 mg(S) cm⁻²"
  cycles: "800 @0.5 C, 유지 77.5 % (최대값 기준이면 72.9 % [재현]), 감쇠 0.028 %/cyc, CE ≈100.0–100.2 % 전 구간 [도표]"
  temperature_C: 60
  mechanism: "SE 부피분율 부족 → 조성 불균일 → 불활성 bulky sulfur → 이온 경로 차단 → 낮은 황 이용률. 저밀도 SE 가 같은 wt% 에서 부피분율을 올려 해결한다는 주장. 근거: ICE vs SE vol% 3점 상관(Fig. 3d), 양극 분말 XRD 의 결정질 황 유무(Fig. 4a), 전극 EDS 균일도(Fig. 4c–f), GITT 과전압(방전 η_max 0.42 vs 0.74 V). 밀도·입도·전도도 변수는 분리되지 않았다"
  our_axis: "우리 Li2S:LPSCl:AB = 30:50:20 의 SE 50 wt% 자리 — 부피로는 48–52 vol% [재현, 외부 밀도 입력]로 이 논문의 '충분' 기준 35.4 vol% 를 크게 넘는다. 가져갈 것은 (i) wt%→vol% 부피 회계, (ii) GITT η(OCV) 비교법, (iii) Li–In ≈0.62 V vs Li/Li⁺ 의 인쇄 근거. 못 가져갈 것은 LPB 합성·melt-diffusion·활성화 프로토콜(S8 계)"
---

# 수집 목적

D. Wang, L.-J. Jhang, R. Kou, M. Liao, S. Zheng, H. Jiang, P. Shi, G.-X. Li, K. Meng, D. Wang,
**"Realizing high-capacity all-solid-state lithium-sulfur batteries using a low-density
inorganic solid-state electrolyte"**, *Nature Communications* **14** (2023) 1895,
DOI 10.1038/s41467-023-37564-z (open access, CC BY) 의 **절별 해체분석**.

이 위키가 이 논문을 흡수하는 이유는 하나다. **우리 복합양극 Li2S : LPSCl : AB = 30 : 50 : 20
의 "50" 자리를 정면으로 다루는 논문**이기 때문이다 ([[li2s-assb-composite-cathode]]).
우리가 지금까지 흡수한 논문들은 같은 문제(황 이용률)를 **양극 첨가제**로 풀거나
(Huang 2026 — 고엔트로피 황화물 6 wt%) **음극·집전체**로 풀었는데 (Zhang 2026 — anode-free Na
집전체), 이 논문은 **SE 자체의 밀도를 바꿔서** 푼다. 그래서 이 digest 의 축은 다른 digest 와
다르다 — **질량비(wt%)가 아니라 부피비(vol%)**다.

**단위 경고 (이 논문에서 가장 중요한 규율)**: 이 논문의 주인공은 "밀도" 다. 따라서
`wt%` 와 `vol%` 를 **절대 섞어 읽으면 안 된다**. 같은 `28.6 wt%` 의 SE 가 밀도 1.491 에서는
`35.4 vol%`, 밀도 2.04 에서는 `28.6 vol%` 다. 이 digest 는 조성을 적을 때마다 둘 다 적는다.

또 하나: **이 논문의 활물질은 Li2S 가 아니라 원소황 S8 이다.** 첫 충전 활성화 문제가 없고
(방전부터 시작한다), 따라서 [[li2s-activation-first-charge]] 에는 근거를 주지 않는다.
비용량은 전부 **mAh g⁻¹(S)** 기준이고, `(Li2S)` 환산은 이 digest 가 `[재현]` 으로 병기한다
(×0.698 = 32.065/45.95 — [[capacity-normalization-li2s-vs-sulfur]]).

**표기 규칙** (이 위키 관례 4구분):
- `[인쇄]` — 논문 본문/식/표/캡션에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

- 원본 파일: 본문 PDF 10쪽 (`wiki/inbox/9ada0d4c-High_capacity_ASSLSBs_with_low_density_SE.pdf`).
  **Supplementary Information 은 이 세션에서 확보하지 못했다.** Nat. Commun. 의 SI 는 별도
  파일이고, 본문이 인용하는 Supplementary Fig. 1–34 · Supplementary Table 1–4 ·
  Supplementary Note 1–8 을 **한 장도 보지 못했다.** 아래 공백표에서 `SI 미확보` 로 표시한
  항목은 "논문에 없다" 가 아니라 **"이 digest 가 확인하지 못했다"** 는 뜻이다. 혼동하면 안 된다.
- 크로핑 그림: `raw/figures/wang2023_high-capacity-assb-li-s-low-density-solid-electrolyte/`
  — 본문 Fig. 1–4 네 장. 추출기가 Fig. 3 을 캡션 아래 좁은 띠로만 자르고 Fig. 4 를 놓쳐서,
  두 장은 캡션 좌표 기준으로 다시 잘라 넣었다 (§17).
- 페이지 참조는 **PDF 페이지**(1–10) = 저널 조판 페이지.

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

이 절이 이 digest 의 가장 중요한 산출물이다. **G1–G6 은 SI 를 구하면 풀릴 수 있는 것**,
**G7–G16 은 SI 가 있어도 논문이 답하지 않는 것**으로 나눠 둔다.

## A. SI 미확보로 확인 못 한 것 (SI 를 구하면 풀릴 수 있다)

| # | 공백 | 왜 문제인가 |
|---|---|---|
| G1 | **Fig. 1b 의 셀 수준 에너지밀도 모델의 전제가 전부 SI 에 있다** (Supplementary Fig. 4 + Supplementary Note 1). 본문이 주는 것은 `[인쇄]` "50 vol% sulfur, 4 mg(S) cm⁻²" 와 "The weight of the sulfur cathode, SE membrane, Li anode, and current collectors was considered" 뿐. | **SE 분리막 두께·Li 두께·집전체 두께를 모른다.** 이 논문의 핵심 주장("400 Wh kg⁻¹ 을 넘으려면 ρ_SE < 1.5 g cm⁻³ 이어야 한다")은 전적으로 그 전제에 달려 있다. 전제 없이는 재현도 반박도 불가. Zhang 2026 의 127 mg cm⁻² 전해질층 문제(그쪽 G11)를 이 논문이 실제로 푼 것인지 **본문만으로는 확인할 수 없다**. |
| G2 | **양극 성분별 부피분율의 원표가 SI 에 있다** (Supplementary Fig. 25). 본문에 인쇄된 vol% 는 S-C-LPB-65 의 `[인쇄]` "LPB 27.9 vol% / sulfur 59.2 vol%" **한 쌍뿐**이다. | 주력 60 wt% 양극의 vol% 를 본문이 숫자로 주지 않는다. 이 digest 는 §7 에서 그 한 쌍을 역산해 **밀도 집합(S 2.07 · C 1.90 · LPB 1.491 g cm⁻³)을 복원**하고 나머지를 `[재현]` 했으나, 그 복원이 저자가 쓴 값과 같은지는 SI 없이는 확정 못 한다. |
| G3 | **LPB 의 전기화학 안정창(LSV) 데이터가 SI 에 있다.** Methods 는 측정 방법만 준다 — `[인쇄]` "linear sweep voltammetry of Li-In\|SE\|C-SE cells … 0.05 mV s⁻¹ from OCV to **4.38 or −0.62 V vs Li-In/Li⁺ (5 or 0 V vs Li/Li⁺)** at 60 °C". | 우리 위키 [[li2s-assb-composite-cathode]] 의 "전압창 제약(미검증 배경)" 구멍을 메울 **가장 유력한 후보 데이터가 정확히 여기**인데, 곡선도 산화 개시 전위도 본문에 없다. **이 digest 는 그 구멍을 메우지 못한다** (§11). |
| G4 | **LPB 의 용량 기여분 정량이 SI 에 있다** (Supplementary Fig. 17·23, Supplementary Note 5·6). 본문이 주는 숫자는 `[인쇄]` "the high discharge capacity is mainly contributed by the lithiation of sulfur to Li2S (**99.5 % in the first cycle and >82 % in the following cycles**)" 한 줄. | ">82 %" 는 **하한**이다. 즉 사이클 용량의 **최대 18 % 가 황이 아니라 SE 의 산화환원**일 수 있다. 800 사이클 778.9 mAh g⁻¹(S) 는 `[재현]` 최악의 경우 **638.7 mAh g⁻¹(S) (= 445.8 mAh g⁻¹(Li2S))** 까지 내려간다. 이 보정을 논문은 한 번도 반영하지 않고 원수치를 그대로 광고한다. |
| G5 | **Li 금속과의 계면·Li\|LPB\|Li 대칭셀 결과가 SI 에 있다** (Supplementary Fig. 14·15, Note 3). 본문은 `[인쇄]` "metastable interphase can be formed between LPB pellet and Li metal to inhibit the degradation of LPB" 라고만 적고, 바로 `[인쇄]` "cell failure caused by lithium penetration may still occur under practical testing conditions" 라며 **Li–In 으로 도망간다**. | LiBH4 를 넣은 대가(Li 금속 안정성·단락 임계전류)를 본문이 숫자로 주지 않는다. Methods 에는 대칭셀 조건만 있다 — 0.1/0.25/0.5/0.75/1.0 mA cm⁻², 1 h, 25 °C, 6–8 MPa, **셀 3개**. 임계전류밀도(CCD)는 미인쇄. |
| G6 | **LPSCl(Li6PS5Cl)의 밀도가 이 논문 어디에도 없다.** Fig. 1c 의 막대는 `[도표]` LE ≈1.13 · PEO ≈1.20 · **LPB 1.491** · TTE ≈1.52 · LPS ≈1.81 · LGPS ≈2.04 · LATP ≈2.91 · LLZO ≈5.12 로 **argyrodite LPSCl 이 빠져 있다.** (Fig. 1e 의 전도도-합성온도 비교에는 Li6PS5Cl 이 나오지만 그건 밀도 축이 아니다.) | 우리 SE 가 바로 LPSCl 이다. 이 논문의 논리를 우리 조성에 적용하려면 LPSCl 밀도가 필요한데 **이 논문은 근거를 주지 않는다.** §14 의 `[재현]` 은 외부 값(1.64–1.90 g cm⁻³)을 **입력으로 명시**하고 계산했으며, 그 입력 자체는 이 위키에 아직 근거 raw 가 없다. |

## B. SI 가 있어도 논문이 답하지 않는 것

| # | 공백 | 왜 문제인가 |
|---|---|---|
| G7 | **밀도 효과와 입도 효과를 분리하지 않았다.** LPB 는 저밀도(1.491)**이면서 동시에** 일차입자가 작고(~500 nm) 전도도가 높다(6.0 mS cm⁻¹). 대조군 LPS·LGPS 는 `[인쇄]` "particle sizes of ≤5 μm" 로만 묶였다. 저자도 이 문제를 알고 `[인쇄]` "there is no apparent correlation between cathode performance and SE's ionic conductivity/particle size" 라고 방어하지만, 그 근거는 **세 점(LPB·LPS·LGPS)의 상관 관찰**이다. | **N=3 의 상관으로 세 변수(밀도·입도·전도도) 중 하나를 고른 것**이다. 결정적 실험은 "**같은 밀도·같은 전도도의 SE 를 입도만 바꿔서**" 또는 "**같은 LPB 를 밀도만 바꿔서**" 인데 둘 다 없다. 실제로 논문 자신이 뒤에서 `[인쇄]` "in addition to SE volume ratio, the large particle size of SE may likewise cause deficient Li⁺ transport pathways" 라고 입도 효과를 되살린다 (SI Fig. 31–33). **논문 안에서 인과 귀속이 흔들린다.** |
| G8 | **`S/KB/SE = 50/10/24` 는 100 으로 정규화되지 않는다.** `[인쇄, p.4]` "a high sulfur content of ~60 wt% (S/KB/SE = 50/10/24, w/w/w)". 합이 84 다. `[재현]` 정규화하면 **59.52 / 11.90 / 28.57 wt%**. 반면 다른 조성은 정규화되어 있다 — 50 wt% 계열은 50/20/30 과 50/10/40 로 합이 100. | 같은 문장 안에서 **표기 관례가 바뀐다**. "SE 24 wt%" 로 잘못 읽으면 부피분율 계산이 전부 틀린다. 세미나·인용 시 반드시 정규화해서 쓴다. |
| G9 | **본문의 목표치가 400 → 300 Wh kg⁻¹ 로 미끄러진다.** `[인쇄, 서론]` "it is imperative to employ SEs with a density <1.5 g cm⁻³ for fabricating **>400 Wh kg⁻¹** Li-S ASSBs" · `[인쇄, 결론]` "can potentially allow Li-S ASSB to reach a high specific energy **above 300 Wh kg⁻¹** if combined with thin Li and SE membranes". | 서론의 400 은 **모델(Fig. 1b)** 값이고 결론의 300 은 **실제 셀에 대한 기대**다. 같은 논문이 같은 지표를 다른 숫자로 두 번 말한다. 어느 쪽도 **이 논문에서 실측되지 않았다**. |
| G10 | **Fig. 3h 의 y축 라벨이 "Cell specific energy (Wh kg⁻¹)" 인데, 캡션은 "The specific energy was estimated based on the weight of sulfur cathodes" 라고 한다.** | **축 라벨이 틀렸다.** "This work" 의 1318.7 Wh kg⁻¹ 은 셀 수준이 아니라 **복합양극 질량 기준**이다 (`[재현]` 1144.6 mAh g⁻¹(S) × 1.935 V × 0.5952 = **1318.2** — 분모가 S+KB+SE 복합체 질량임이 산술로 확인된다). SE 분리막(80 mg, ~600 µm)·Li–In·집전체가 전부 빠졌다. 그림만 보고 "셀 1318 Wh kg⁻¹" 이라고 옮기면 틀린다. |
| G11 | **부피 에너지밀도 2561.8 Wh L⁻¹ 의 분모가 물리적으로 의심스럽다.** `[재현]` 2561.8 / 1318.7 = **1.943 g cm⁻³** 의 복합양극 밀도를 함의한다. 그런데 §7 에서 복원한 밀도 집합으로 계산한 **완전치밀(공극 0) 이론 혼합밀도는 1.846 g cm⁻³** 다. | 294 MPa 로 누른 전극에 공극이 0 인 것도 비현실적인데, 함의된 밀도는 **이론 치밀도를 5 % 초과**한다. 성분 밀도를 다르게 썼거나(예: LPB 를 결정 이론밀도 1.59 로) 공극을 음수로 둔 셈이다. 전극 두께·공극률 실측이 **하나도 없다** (§5). |
| G12 | **ICE 가 100 % 를 넘고, 800 사이클 내내 CE 가 100 % 위에 있다.** `[인쇄]` S-C-LPB ICE **100.2 %**. `[도표, Fig. 3g]` CE 는 800 사이클 동안 **≈100.0–100.2 %** 에 머문다 (우축 96–101 % 범위). | CE > 100 % 가 지속되면 **매 사이클 충전전기량이 방전보다 크다** = 기생 산화(LPB 탈리튬화)가 계속 일어난다는 뜻이다. 논문은 이것을 "높은 ICE" 라는 **장점**으로 제시하고(Fig. 3d 막대) 기생반응으로 읽지 않는다. G4 의 ">82 %" 와 합치면 해석이 정반대가 된다. |
| G13 | **셀 개수가 일부에만 있다.** `[인쇄, Methods]` "All electrochemical tests have been carried out **at least two times** and most of them have been tested for three times" · Fig. 1d 와 3d 의 오차막대는 각각 전도도·평균 ICE 의 표준편차. 반면 **800 사이클 곡선(Fig. 3g)·율속(3e)·GITT(4h,i)·6 mg cm⁻² 는 전부 단일 곡선**이고 n 이 적히지 않았다. | 800 사이클 77.5 % 가 n=1 인지 n=3 의 대표인지 알 수 없다. 이 논문에서 가장 많이 인용될 수치가 바로 그것이다. |
| G14 | **77.5 % 유지율의 기준점이 초기값이고 최대값이 아니다.** `[인쇄]` 초기 1004.6 → 20 사이클에 **1068.1 로 상승** → 800 사이클 778.9. `[재현]` 778.9/1004.6 = 77.5 % 이지만 **778.9/1068.1 = 72.9 %** 다. | 초기 20 사이클의 상승을 논문 스스로 `[인쇄]` "possibly attributed to the growth of capacity contribution from LPB's redox reaction" 라고 SE 기여로 설명한다. 그러면 **분모가 황 용량이 아니다**. 유지율 정의가 유리한 쪽으로 잡혀 있다. |
| G15 | **혼합 조건의 절반이 미기재다.** `[인쇄, Methods]` "mechanical ball milling under **350 rpm for 10 h** in **45 ml ZrO2 jars** (FRITSCH PULVERISETTE. 7 premium line)" 까지는 있다. **볼 재질·볼 지름·볼 개수·BPR(ball-to-powder ratio)·정회전/역회전 주기·휴지시간이 없다.** | 우리 [[composite-cathode-mixing-routes]] 의 핵심 변수다. 350 rpm × 10 h 는 **상당한 고에너지 조건**인데(Huang 2026 은 350 rpm × 4 h), BPR 없이는 투입 에너지를 비교할 수 없다. Fig. 4a 에서 S-C-LPB 의 황이 **비정질화**된 것이 밀도 때문인지 밀링 에너지 때문인지도 이 공백 때문에 못 가른다. |
| G16 | **황이 왜 LPB 와 섞으면 비정질이고 LPS 와 섞으면 결정질인가**에 대한 대조 실험이 없다. `[인쇄]` Fig. 4a 는 사실만 보고하고, 설명은 "부피분율 → bulky sulfur" 로 곧장 간다. | 두 시료는 **같은 S/KB 융합체에서 출발해 같은 350 rpm 10 h 로 밀링**된다. 차이는 SE 뿐이다. 저밀도 SE 가 같은 질량에서 **부피가 크니 밀링 중 황에 가하는 전단이 다르다**는 기계적 설명도 가능한데, 그 가능성이 검토되지 않는다. `[해석]` 이것은 "부피분율" 서사의 대안 가설이고, 우리 one-step/two-step 질문에도 직접 걸린다. |
| G17 | **Swagelok 셀이 대기 중에서 돌아간다.** `[인쇄, Methods]` "the cells were compressed by three insulated bolts at 50–60 MPa, **removed from the glovebox, and tested using a Landt cycler at 60 °C under ambient air**" + `[인쇄]` "Note that the Swagelok cell could not fully prevent the electrode from contacting ambient air." | 저자 스스로 밀봉 불완전을 인정한다. 800 사이클 열화의 원인으로 `[인쇄]` "chemical reactivity against moisture" 를 지목하면서도, **건조 아르곤 대조 셀을 돌리지 않았다.** 열화 기전 결론(§9)이 셀 설계 결함과 분리되지 않는다. |
| G18 | **스택 압력이 범위로만 주어지고 운전 중 제어되지 않는다.** `[인쇄]` 조립 성형 **294 MPa 3 min**, 운전 **50–60 MPa** (볼트 3개), 초록은 "average stack pressure of ~55 MPa". | 볼트는 정압(constant pressure)이 아니라 **정변위**다. 황 → Li2S 의 큰 부피변화(≈80 %) 동안 압력이 어디까지 올라갔는지 기록이 없다. Zhang 2026 이 1–4 MPa 에서 돌린 것과 **한 자릿수 이상 차이**나는 조건이라, 이 논문의 결과는 "고압 셀의 결과" 로 한정해 읽어야 한다. |

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 1쪽 + 10쪽:

| 항목 | 값 |
|---|---|
| 제목 | Realizing high-capacity all-solid-state lithium-sulfur batteries using a low-density inorganic solid-state electrolyte |
| 저자 | Daiwei Wang¹, Li-Ji Jhang², Rong Kou¹, Meng Liao¹, Shiyao Zheng¹, Heng Jiang¹, Pei Shi², Guo-Xing Li¹, Kui Meng¹, **Donghai Wang¹ (교신, dwang@psu.edu)** |
| 소속 | 1 Department of Mechanical Engineering, The Pennsylvania State University · 2 Department of Chemical Engineering, Penn State |
| 학술지 | *Nature Communications* **14** (2023) 1895 |
| DOI | 10.1038/s41467-023-37564-z |
| 접수/게재수락 | Received 1 June 2022 · **Accepted 22 March 2023** |
| 저작권 | CC BY 4.0 (open access) |
| 지원 | US DOE, Office of Vehicle Technologies, Advanced Battery Materials Research (BMR), award DE-EE0008862 |
| 이해충돌 | 없음 (선언) |
| 데이터 | `[인쇄]` "available from the corresponding author on reasonable request" — **공개 저장소 없음** |
| 심사 | `[인쇄]` Peer review: Fei Chen, Hyung-Tae Lim, Jinghua Wu + 익명 심사자 |

`[해석]` 그룹의 축은 **SE 재료 합성**이다 (기계공학과 Donghai Wang 그룹). 양극 설계·탄소
구조·활성화는 이 논문의 관심사가 아니고, 양극은 의도적으로 **가장 평범한 방식**(melt-diffusion
+ 건식 볼밀)으로 만들어 **SE 만 바꿔 끼운다**. 그것이 이 논문의 강점(변수 통제)이자 약점(G7 —
통제한 변수가 하나가 아니다)이다.

---

## 1. 한 문단 요약

`[해석]` 저자들은 "고황함량(>50 wt%) 양극에서 황 이용률이 낮은 근본 원인은 **양극 내 이온
전달 부족**이고, 그 부족은 SE 의 전도도가 아니라 **SE 의 부피분율**이 결정한다" 고 주장한다.
무기 SE 의 밀도가 2 g cm⁻³ 를 넘기 때문에 질량으로 35 wt% 를 넣어도 부피로는 35 vol% 아래로
떨어진다는 것이다. 이를 풀기 위해 **THF 액상법으로 Li3PS4–2LiBH4 (LPB) glass-ceramic
argyrodite** 를 합성했다 — 밀도 **1.491 g cm⁻³** (He 피크노미터, 21 °C, 10회 측정), 일차입자
**~500 nm** (5 µm 응집체 내부), 열간가압 펠릿 이온전도도 **6.0 mS cm⁻¹ @25 °C** (Ea 0.216 eV),
합성온도 **160 °C**. 이 LPB 를 쓴 S : KB : SE = 50 : 10 : 24 (w/w/w, `[재현]` = 59.5 : 11.9 :
28.6 wt% = **53.1 : 11.6 : 35.4 vol%**) 양극은 Li–In \| LPB \| S-C-LPB Swagelok 셀(60 °C,
스택압 50–60 MPa, 0.5–2.5 V vs Li–In/Li⁺)에서 167.5 mA g⁻¹ 에 **1047.5 mAh g⁻¹(S)**
(ICE 100.2 %), 율속시험 최고 **1144.6 mAh g⁻¹(S)** (`[재현]` = 798.9 mAh g⁻¹(Li2S) =
**S 이용률 68.3 %**) 를 냈고, 같은 조성의 LPS(β-Li3PS4)·LGPS 양극은 802.1 (ICE 74.3 %)·
742.0 mAh g⁻¹(S) (ICE 31.4 %) 에 그쳤다. 837.5 mA g⁻¹ CCCV 로 **800 사이클, 초기 1004.6 →
778.9 mAh g⁻¹(S), 유지 77.5 %, 감쇠 0.028 %/cyc** 을 보였다. 원인 규명은 XRD(LPS 양극에만
결정질 황)·SEM/EDS(LPS 양극에만 bulky sulfur 와 리튬화 후 상분리)·GITT(방전 최대 과전압
LPB 0.42 V vs LPS 0.74 V)로 하고, 결론은 "**적정 SE 부피분율이 불활성 bulky sulfur 를 없애고
조성 균일도를 확보하는 전제조건**" 이다.

---

## 2. 저자의 논리 사슬 (서론, p.1–2)

논문 전체가 아래 5단 논증 위에 서 있다. **각 단계의 근거 강도를 구분해 둔다.**

| 단계 | `[인쇄]` 주장 | 근거 |
|---|---|---|
| ① | Li–S ASSB 가 실용 수준을 넘으려면 **황함량 >50 wt% 에서 이용률 >1000 mAh g⁻¹(S)** 가 필요하다 | Supplementary Fig. 1 (**SI 미확보**) |
| ② | 기존 전략(계면 개량, 이온성 액체 첨가, conversion-intercalation 혼성, SeSx)은 **저황함량에서만** 성공했다 | 문헌 [6–14] |
| ③ | 근본 원인은 양극 내 **이온 전달 부족**이다. 황/Li2S 가 이온전도를 못 하므로 SE 가 유일한 Li⁺ 경로다 | `[인쇄]` "We deem the root cause…" — **연역, 실험 근거 아님** |
| ④ | SE 의 **전도도**는 수송 *속도*를, **부피분율과 입도**는 경로의 *충분성*을 결정한다 | Fig. 1a 모식도 + Supplementary Fig. 2 (**SI 미확보**) |
| ⑤ | 따라서 **밀도 <1.5 g cm⁻³ 의 SE** 가 있어야 >400 Wh kg⁻¹ Li–S ASSB 가 가능하다 | Fig. 1b 모델 + Supplementary Note 1 (**SI 미확보**, G1) |

`[인쇄, p.1]` 핵심 산술 문장 그대로: "Especially at a high sulfur content of >50 wt%, the weight
ratio of SE becomes as low as 35 wt%. Considering the high density of inorganic SE (typically
>2 g cm⁻³), the volume ratio of SE drops even lower in the cathode (<35 vol%), giving rise to
deficient Li⁺ pathways and hence mediocre sulfur utilization."

`[해석]` ③이 이 논문의 **공리**다. 실험으로 확립한 것이 아니라 전제로 깔고 들어간다. 논문의
모든 관측(XRD·EDS·GITT)은 ③이 참일 때 자연스럽게 읽히도록 배열되어 있고, **③에 대한 반증
가능한 대조 실험은 없다**. 특히 "전자 전달" 은 처음부터 용의선상에서 제외된다 — 탄소
부피분율이 세 양극에서 `[도표, Fig. 3d]` 11.6 / 12.3 / 12.8 % 로 거의 같으니 통제된 셈이라는
암묵적 논리인데, **명시되지 않는다**.

### Fig. 1b 의 모델 (`[도표]`, 우리 목적에 중요)

가로축 = SE 밀도(1.0–5.5 g cm⁻³), 고정 조건 `[인쇄, 그림 안]` **"50 vol% Sulfur, 4 mg(S) cm⁻²"**.

| ρ_SE (g cm⁻³) | 셀 비에너지 `[도표]` (Wh kg⁻¹) | 양극 황함량 `[도표]` (wt%) |
|---|---|---|
| 1.0 | ≈473 | ≈61 |
| **1.5** | ≈425 | ≈56 |
| 2.0 | ≈386 | ≈50 |
| 2.5 | ≈353 | ≈47 |
| 3.0 | ≈325 | ≈44 |
| 3.5 | ≈302 | ≈41 |
| 4.0 | ≈281 | ≈38 |
| 4.5 | ≈263 | ≈35 |
| 5.0 | ≈247 | ≈33 |
| 5.5 | ≈232 | ≈31 |

`[해석]` 이 표의 진짜 메시지는 **"황 부피분율을 50 vol% 로 고정하면, SE 밀도가 올라갈수록
양극의 황 wt% 가 자동으로 떨어진다"** 는 항등식이다. 즉 Fig. 1b 의 파란 막대는 물리 결과가
아니라 **정의상 따라 나오는 산술**이다. 빨간 막대(셀 비에너지)만이 모델 가정(G1)에 의존한다.
**이 논문이 셀 수준 에너지밀도를 "계산" 한 유일한 자리가 Fig. 1b 이고, 그것은 실측이 아니라
가정 모델이다.** 실제 셀에 대해 인쇄된 에너지밀도는 전부 **복합양극 질량 기준**이다 (G10).

---

## 3. LPB 액상 합성법 (재현 가능하게 — Methods p.7)

**`[인쇄]` 전문 옮김. 우리가 이 SE 를 직접 만들 수 있는지 판단할 근거다.**

| 단계 | 조건 |
|---|---|
| 분위기 | 전 과정 **Ar 글로브박스 (H2O < 1 ppm, O2 < 5 ppm)** |
| 원료 | THF (anhydrous, ≥99.9 %, Sigma-Aldrich) · Li2S (99.98 %, Sigma) · P2S5 (99 %, Sigma) · **LiBH4 solution (2.0 M in THF, Sigma)** — 전부 **무처리 사용** |
| 1단계 | **Li2S : P2S5 = 3 : 1 (몰비)** 를 anhydrous THF 에 넣고 **25 °C, 24 h 교반** |
| 2단계 | 위 현탁액에 **LiBH4 용액**을 **single-channel high-precision pipette** 로 적가 — **LiBH4 : Li2S : P2S5 = 4 : 3 : 1 (몰비)** |
| 3단계 | **48 h 교반** |
| 4단계 | Schlenk flask 로 옮겨 **100 °C, 진공 2 h** 건조 (용매 제거) |
| 5단계 | 분말 회수 후 **160 °C, 3 h, Ar 분위기 어닐링** → LPB glass-ceramic argyrodite |

**대조군 LPS (β-Li3PS4) 합성** `[인쇄]`: Li2S : P2S5 = 3 : 1 을 THF 에 25 °C 24 h 교반 →
원심분리로 침전 회수 → **anhydrous THF 로 3회 세척** → **140 °C 진공 3 h 건조**. (문헌 [19] 따름)

**LGPS·LPSC** `[인쇄]`: Li10GeP2S12 (>99.9 %) 와 Li6PS5Cl (>99.9 %) 는 **MSE Supplies LLC 구매**.
— `[해석]` LPSC 는 C-SE 대조 전극(Super C / LPSC = 30/70)에만 쓰이고 **황 양극에는 쓰이지 않았다.**
우리 SE 와 같은 물질이 이 논문에 등장하지만 **양극 비교군이 아니다.** 중요한 한계다.

`[해석]` **우리가 재현 가능한가**: 원료가 전부 Sigma 카탈로그 품목이고 특수 장비가 없다
(교반기·Schlenk line·관상로·글로브박스). 총 소요 ≈ 24 h + 48 h + 2 h + 3 h ≈ **3.5일**.
LiBH4 를 **2.0 M THF 용액**으로 넣는 것이 요령이다 (고체 LiBH4 를 넣지 않는다 — 계량 정확도와
분산 때문으로 보이나 이유는 미기재). 단, **어닐링 160 °C 의 승온·냉각 속도, 분말 회수 수율,
입도 제어 방법(응집체 5 µm 는 의도인가 결과인가)이 전부 미기재**다.

---

## 4. LPB 의 물성 (p.3–4, Fig. 1–2)

| 물성 | 값 | 출처 |
|---|---|---|
| **밀도** | **1.491 g cm⁻³ @21 °C** — He 피크노미터, 시료 ~0.4 g, Ar 박스에서 밀봉, **대기 노출 <1 min**, **10회 측정** | `[인쇄]` |
| 이온전도도 (냉간압축 펠릿) | **3.8 mS cm⁻¹ @25 °C**, 상대밀도 **~86.0 %** | `[인쇄]` (SI Fig. 6, **미확보**) |
| 이온전도도 (열간가압 펠릿) | **6.0 mS cm⁻¹ @25 °C**, 상대밀도 **~91.5 % (벌크밀도 1.364 g cm⁻³)** | `[인쇄]` |
| 활성화에너지 | **Ea = 0.216 eV** (25–100 °C Arrhenius, 5점, 오차막대 있음) | `[인쇄]` + `[도표, Fig. 1d]` |
| 합성온도 | **160 °C** — `[인쇄]` "lower than other liquid-phase-synthesized sulfide SEs with room-temperature ionic conductivity above 1 mS cm⁻¹" | `[인쇄]` |
| 응집체 크기 | **~5 µm** (SEM), S·P 가 표면에 균일 분포 (EDS) | `[인쇄]` + `[도표, Fig. 2a]` |
| **일차입자** | **~500 nm**, **뚜렷한 다공 구조 없음** (STEM/TEM) | `[인쇄]` + `[도표, Fig. 2b]` |
| BET 비표면적 | **~3.705 m² g⁻¹** | `[인쇄]` (SI Fig. 9, **미확보**) |
| 상 | **결정질 + 비정질 공존** — SAED 에 회절 반점과 확산 링 동시 | `[인쇄]` + `[도표, Fig. 2c]` |
| 결정상 | **Li6-xPS5-x(BH4)1+x (−1 < x ≤ 1) cubic argyrodite**, PDF#01-086-9370 (Li6PS5(BH4)0.9) 대조 | `[인쇄]` + `[도표, Fig. 2d]` |
| 격자상수 | **≈10.05 Å** → 결정 이론밀도 **≈1.59 g cm⁻³** | `[인쇄]` |

`[인쇄]` 밀도 해석: "Due to the amorphous phase's presence, the LPB SE density shall be lower
than the pure Li6-xPS5-x(BH4)1+x crystal, explaining the measured lower density (1.491 g cm⁻³)."

`[해석]` **저밀도의 출처는 두 겹**이다. (i) BH4⁻ 가 S²⁻/Cl⁻ 자리를 대체해 **결정 자체가 가볍다**
(1.59 g cm⁻³), (ii) 비정질 상이 섞여 **거기서 더 내려간다** (1.491). 즉 저밀도는 조성(붕수소화물)
과 미세구조(유리질) 양쪽에서 온다. **우리 LPSCl 에 이 경로를 그대로 옮길 수는 없다** — Cl⁻ 를
BH4⁻ 로 바꾸는 순간 그것은 다른 물질이다.

### 불순물 (저자가 스스로 밝힌 것)

| 기법 | 관측 | 귀속 |
|---|---|---|
| XRD `[인쇄]` | **low-intensity unknown peaks** | "side reaction products or precursors/intermediate product residuals" (SI Fig. 12, **미확보**) |
| Raman `[인쇄]` | **~418 cm⁻¹ 고강도** | PS4³⁻ (LPB 본체) |
| Raman `[인쇄]` | **~386 cm⁻¹ 저강도** | **P2S6⁴⁻ — 불순물 Li4P2S6** |
| Raman `[인쇄]` | **~2300 cm⁻¹ 광폭** | BH4⁻, **고온 육방정 LiBH4 와 유사** = BH⁻–Li⁺ 정전기 상호작용이 약함 → Li⁺ 이동도 유리 |
| ³¹P NMR `[인쇄]` | Peak I **96–87 ppm** (비대칭, 두 선으로 deconvolution) | Li6-xPS5-x(BH4)1+x 의 PS4³⁻ — **S²⁻/BH4⁻ 부격자 무질서**가 전도도에 유리 |
| ³¹P NMR `[인쇄]` | Peak II **~86 ppm** | **β-Li3PS4 (LPS)** — 잔류 Li3PS4·3THF 의 열처리 산물 |
| ³¹P NMR `[인쇄]` | Peak III **~109 ppm** | **Li4P2S6 의 P2S6⁴⁻** |
| ⁷Li NMR `[인쇄]` | LPB **~1.93 ppm (샤프)** vs LPS ~2.07 vs LiBH4 ~0 ppm (광폭) | 샤프한 선 = Li⁺ 이동도 증가 |

`[해석]` **LPB 는 단상이 아니다** — argyrodite 결정 + 비정질 + β-Li3PS4 + Li4P2S6 + 미확인상의
혼합물이다. 저자도 숨기지 않는다. 그러나 **각 상의 분율을 정량하지 않았다.** 밀도 1.491 은
이 혼합물 전체의 값이고, "argyrodite 결정의 밀도가 낮아서" 라는 설명(1.59)은 **혼합물 중
일부에만 해당**한다. Li4P2S6 은 알려진 저전도 상이다.

---

## 5. 복합양극 제조·셀 조립 — 전 조건 (Methods p.7–8)

### 5.1 양극 분말 (**two-step 계열**)

| 단계 | `[인쇄]` 조건 |
|---|---|
| ① C–S 복합체 | 황 (≥99.0 %, Sigma) + **KB (Ketjenblack EC-600JD, AkzoNobel)** 를 **S:KB = 50:10 또는 50:20 (w/w)** 로 혼합 후 **160 °C, 10 h** 가열 (melt-diffusion) → 복합체의 황함량 **83.3 wt% 또는 71.4 wt%** |
| ② SE 혼합 | ①의 분말 + SE(LPB/LPS/LGPS) 를 **기계식 건식 볼밀 350 rpm, 10 h, 45 mL ZrO2 jar, FRITSCH PULVERISETTE 7 premium line** |
| 분위기 | **전 과정 Ar (H2O <1 ppm, O2 <5 ppm)** |
| 바인더 | **없음** (언급 자체가 없다) |
| 미기재 | **볼 재질·지름·개수·BPR·회전 주기·휴지** (G15) |

**C-SE 대조 전극** `[인쇄]`: **Super C : SE = 30 : 70 (w/w)**, SE 는 **LPB 또는 LPSC**, 같은
350 rpm 10 h. → SE 자체의 산화환원 용량 측정용 (Li–In \| LPB \| C-LPB 셀).

`[해석]` 이것은 우리 분류로 **two-step** 이다 — 활물질과 탄소를 먼저 결합시키고(융합),
**SE 는 두 번째 단계에서** 넣는다. 다만 두 번째 단계가 **350 rpm × 10 h** 로 결코 mild 하지
않다는 점이 중요하다. [[one-step-vs-two-step-mixing]] 의 H2("고에너지 BM 이 SE 를 손상시키는가")
관점에서 보면, **이 논문은 SE 를 10시간 350 rpm 으로 밀링하고도 800 사이클을 돌렸다.**
단, 밀링 후 SE 의 전도도·XRD 를 재지 않았으므로 "손상되지 않았다" 는 결론은 낼 수 없고,
"손상되었더라도 작동했다" 까지만 말할 수 있다. `[인쇄]` 저자 스스로 "the cathode composite
powders were prepared using the **conventional** mechanical dry powder ball-milling method, and
further performance improvement might be achievable by fine-tuning local interfacial contact
among carbon, sulfur, and SE" 라고 개선 여지를 남긴다.

### 5.2 조성 (wt% / vol% 를 항상 함께)

| 시료 | `[인쇄]` 비 (w/w/w) | `[재현]` 정규화 wt% | `[재현]` vol% (§7 밀도 집합) | `[도표, Fig. 3d]` SE vol% |
|---|---|---|---|---|
| **S-C-LPB (주력)** | S/KB/LPB = **50/10/24** | S 59.5 · KB 11.9 · SE 28.6 | S **53.1** · C **11.6** · SE **35.4** | ≈**35.4** |
| S-C-LPS | S/KB/LPS = 50/10/24 | 동일 | S 56.6 · C 12.3 · SE **31.1** | ≈**30.8** |
| S-C-LGPS | S/KB/LGPS = 50/10/24 | 동일 | S 58.7 · C 12.8 · SE **28.6** | ≈**28.5** |
| S-C-LPB-65 | 65 wt% 황 | — | `[인쇄]` **S 59.2 · LPB 27.9** | — |
| S-C-LPB (저황) | S/KB/LPB = **50/20/30** | S 50 · KB 20 · SE 30 | S 44.1 · C 19.2 · SE 36.7 | — |
| S-C-LPS/LGPS (저황) | S/KB/SE = **50/10/40** | S 50 · KB 10 · SE 40 | S 46.9 · C 10.2 · SE **42.9** (LPS) | — |

### 5.3 셀 조립·운전

| 항목 | `[인쇄]` 값 |
|---|---|
| 셀 형식 | **Swagelok**, 스테인리스 로드 2개가 집전체, Ar 박스에서 조립 |
| SE 분리층 | **LPB 분말 80 mg** 을 셀 안에서 **100 MPa, 1 min** 성형 → **평균 두께 ~600 µm** |
| 양극 성형 | 분말을 펠릿 위에 균일하게 뿌리고 **294 MPa, 3 min** |
| 음극 | **Li 박 3–4 mg** (Li chip, 99.9 %, 0.6 mm, China Energy Lithium) + **In 박 (⌀10 mm, 0.127 mm, 99.99 %, Sigma)** 를 차례로 눌러 붙임, **100 MPa, 1 min** |
| **Li–In 전위** | `[인쇄]` **"Li-In alloy (~0.62 V vs. Li/Li⁺)"** |
| 운전 스택압 | **절연 볼트 3개로 50–60 MPa** (초록: "average stack pressure of ~55 MPa") |
| 온도·분위기 | **60 °C, 대기 중** (강제순환 오븐), Landt cycler |
| 전압창 | 기본 **0.5–2.5 V vs Li–In/Li⁺** (`[재현]` = **1.12–3.12 V vs Li/Li⁺**), 800 사이클은 **0.8–2.5 V** |
| 비용량 기준 | `[인쇄]` **"based on the mass of sulfur in the positive electrode"** — 황 질량 |
| EIS | 0.1 Hz–1 MHz, 5 mV, 60 °C, 1 h 휴지 후 |
| GITT | 167.5 mA g⁻¹ 로 2 사이클 예비 → **펄스 50.25 mA g⁻¹ 30 min + 휴지 4 h**, 60 °C |
| 셀 개수 | `[인쇄]` "at least two times and most of them … three times" (G13) |

`[재현]` **C-rate 환산**: 1 C ≡ 1675 mA g⁻¹(S) 로 잡으면 **167.5 = C/10 · 502.5 = 0.3 C ·
837.5 = 0.5 C · 1675 = 1 C**. 로딩 2.57 mg(S) cm⁻² 에서 837.5 mA g⁻¹ = **2.15 mA cm⁻²**,
로딩 6 mg cm⁻² 에서 167.5 mA g⁻¹ = **1.01 mA cm⁻²**.

`[재현]` **SE 분리층의 면적질량**: 80 mg / (⌀10 mm = 0.785 cm²) = **102 mg cm⁻²**. 두께
600 µm 에서 겉보기 밀도 = 0.102 g cm⁻² / 0.06 cm = **1.70 g cm⁻³** — LPB 진밀도 1.491 보다
크다. `[해석]` 이 불일치는 (i) 실제 전극 면적이 ⌀10 mm 보다 작거나, (ii) 80 mg 중 일부가
셀 벽에 붙었거나, (iii) 두께 "~600 µm" 가 근사치이기 때문일 것이다. 어느 쪽이든 **분리층
면적질량을 정확히 계산할 수 없다** — Zhang 2026 (127 mg cm⁻²) 과 정량 비교하려면 필요한 값인데,
이 논문도 같은 문제를 갖고 있다. **`[해석]` 저밀도 SE 를 내세운 논문이 정작 자기 셀의
전해질층은 얇게 만들지 않았다** (600 µm, ~102 mg cm⁻²).

---

## 6. 전기화학 결과 — 양단위 종합표

**환산**: (Li2S) = (S) × 0.698 · (composite) = (S) × 0.5952 (60 wt% 계열) · S 이용률 = (S)/1675.

| 조건 | `[인쇄]` mAh g⁻¹(S) | `[재현]` (Li2S) | `[재현]` (composite) | `[재현]` 이용률 | `[재현]` mAh cm⁻² |
|---|---|---|---|---|---|
| **S-C-LPB 첫 방전** @167.5 mA g⁻¹ | **1047.5** (ICE **100.2 %**) | 731.2 | 623.5 | **62.5 %** | 2.1–3.1 (2.0–3.0 mg cm⁻²) |
| S-C-LPS 첫 방전 @167.5 | 802.1 (ICE 74.3 %) | 559.9 | 477.4 | 47.9 % | — |
| S-C-LGPS 첫 방전 @167.5 | 742.0 (ICE **31.4 %**) | 517.9 | 441.6 | 44.3 % | — |
| **S-C-LPB 율속 최고** @167.5 | **1144.6** | **798.9** | 681.3 | **68.3 %** | ≈2.86 (2.5 mg 가정) |
| S-C-LPB @502.5 (0.3 C) | 1024.0 | 714.8 | 609.5 | 61.1 % | — |
| S-C-LPB @837.5 (0.5 C) | 907.8 | 633.6 | 540.3 | 54.2 % | — |
| S-C-LPB @1675 (1 C) | 663.0 | 462.8 | 394.6 | 39.6 % | — |
| **800 사이클 초기** @837.5 CCCV | **1004.6** | 701.2 | 597.9 | 60.0 % | **2.58** `[인쇄, 그림 안]` |
| 800 사이클 20 cyc (최대) | 1068.1 | 745.5 | 635.7 | 63.8 % | 2.74 |
| **800 사이클 후** | **778.9** | **543.7** | 463.6 | 46.5 % | 2.00 |
| 저황 50 wt% S-C-LPB @167.5 | `[인쇄]` **>1300** | >907 | >650 | **>78 %** | — (SI Fig. 18, **미확보**) |
| S-C-LPB-65 (65 wt% S) | `[인쇄]` **678** (ICE **62.3 %**) | 473.2 | — | 40.5 % | — (SI Fig. 29, **미확보**) |
| 고로딩 ~6 mg cm⁻² @167.5 | `[인쇄]` **999.7** | 697.8 | 595.0 | 59.7 % | **6.0** (SI Fig. 20, **미확보**) |

### 6.1 사이클 (Fig. 3g)

| 항목 | 값 |
|---|---|
| 조건 | `[인쇄]` **837.5 mA g⁻¹ (0.5 C), CCCV** — 컷오프 전류 167.5 mA g⁻¹, 컷오프 전압 2.5 V, **0.8–2.5 V vs Li–In/Li⁺**, 60 °C |
| 로딩 | `[인쇄]` **~2.57 mg(S) cm⁻²**, 초기 면적용량 **2.58 mAh cm⁻²** |
| 유지 | `[인쇄]` **800 사이클 77.5 %**, 감쇠 `[인쇄]` **~0.028 %/cyc** (`[재현]` (100−77.5)/800 = 0.0281 ✓) |
| **CE** | `[도표, Fig. 3g]` **≈100.0–100.2 % 가 800 사이클 내내 유지** (우축 96–101 %). **100 % 아래로 내려가지 않는다** |
| 셀 개수 | 미기재 (G13) |

`[해석]` **"stable cycling" 이 무엇의 안정인가**: 용량은 명확히 감소한다(77.5 %). CE 는
100 % 위에 붙어 있다. **CE 가 100 % 를 넘는 것은 좋은 신호가 아니다** — 충전에 들어간
전기량이 방전보다 크다는 뜻이고, 그 여분은 되돌아오지 않는 산화(LPB 분해)로 간다. 논문
자신이 G4 에서 "사이클 용량의 >82 % 만 황" 이라고 적고, 초기 20 사이클의 용량 상승을
"LPB 산화환원 기여의 성장" 으로 설명한다. **즉 이 셀의 CE ≈100 % 는 기생반응이 준정상
상태에 든 것이지 가역성의 증거가 아니다.**

### 6.2 dQ/dV (Fig. 3c) 와 전압

`[인쇄]` S-C-LPB 의 피크:

| 피크 | `[인쇄]` vs Li–In/Li⁺ | `[인쇄]` vs Li/Li⁺ | 과정 |
|---|---|---|---|
| I | **~1.51 V** | **2.13 V** | 방전 1단 |
| II | **~1.40 V** | **2.02 V** | 방전 2단 |
| III | **~1.70 V** | **2.32 V** | 충전 |

`[인쇄]` "for the S-C-LPS and S-C-LGPS cathodes, peaks I and II become indistinguishable and
shift to lower potentials with smaller areas, and peak III shifts to higher potentials,
suggesting greater voltage polarization, lower sulfur utilization, and more sluggish reaction
kinetics." `[도표, Fig. 3c]` 확인 — LPB 의 III 피크가 ≈8800 mAh g⁻¹ V⁻¹ 로 **LPS/LGPS(≈1300)보다
6배 이상 날카롭다**. `[해석]` 피크 높이는 분극이 작을수록 커지므로, 이 그림은 "LPB 양극이
훨씬 균일한 전위에서 반응한다" 를 시각적으로 강하게 말한다. 다만 **면적(=용량)이 아니라
높이가 눈에 띄는 그림**이라 과대인상을 준다.

`[인쇄]` 평균 방전전압: **1.935 V vs Li/Li⁺** (= `[재현]` 1.315 V vs Li–In/Li⁺).

### 6.3 ICE 와 SE 부피분율의 상관 (Fig. 3d — 이 논문의 중심 그림)

| 시료 | `[인쇄]` ICE | `[도표]` SE vol% | `[도표]` C vol% | `[도표]` ICE 오차막대 |
|---|---|---|---|---|
| S-C-LPB | **100.2 %** | ≈35.4 | ≈11.6 | ≈±2 |
| S-C-LPS | **74.3 %** | ≈30.8 | ≈12.4 | ≈±4 |
| S-C-LGPS | **31.4 %** | ≈28.5 | ≈12.7 | ≈±5 |

`[인쇄]` "we notice both ICE and initial discharge capacity, especially ICE, increase as the
SE's volumetric content ascends (Fig. 3d), while there is no apparent correlation between
cathode performance and SE's ionic conductivity/particle size."

`[해석]` **세 점으로 그린 상관이다.** SE 부피분율이 28.5 → 30.8 → 35.4 % 로 **6.9 %p 움직이는
동안 ICE 가 31.4 → 100.2 % 로 69 %p 움직인다.** 이 민감도가 사실이라면 퍼콜레이션 임계
근방이라는 뜻인데, 그 주장을 하려면 **같은 SE 로 부피분율만 훑은 시리즈**가 필요하다. 논문이
가진 그런 시리즈는 S-C-LPB(35.4 vol%) → S-C-LPB-65(27.9 vol%, ICE 62.3 %) **두 점뿐**이고,
그 두 점은 **SE 종류는 같지만 황함량이 다르다**. 여전히 변수가 하나가 아니다.

---

## 7. 밀도 → 부피분율 산술 (`[재현]`, 이 digest 의 핵심 계산)

논문은 주력 양극의 vol% 를 본문에 숫자로 주지 않는다 (G2). 그러나 **S-C-LPB-65 에 대해
인쇄된 한 쌍**(`[인쇄]` LPB **27.9 vol%**, sulfur **59.2 vol%**)으로 저자가 쓴 밀도 집합을
역산할 수 있다.

**가정**: S-C-LPB-65 는 황 65 wt%, S:KB = 50:10 비 유지 → 질량비 S : KB : LPB = 65 : 13 : 22.

```
V_LPB / V_S = (22/1.491) / (65/2.07) = 14.755 / 31.401 = 0.470
인쇄값      = 27.9 / 59.2                                = 0.471   ✓
V_C 로부터  ρ_C = 13 / (12.9/59.2 × 31.401) = 13 / 6.843  = 1.90 g cm⁻³
```

→ **저자의 밀도 집합은 ρ(S) = 2.07 · ρ(KB) = 1.90 · ρ(LPB) = 1.491 g cm⁻³** 이다 `[재현]`.

이 집합으로 주력 양극(50/10/24)을 계산하면:

| SE | ρ_SE (g cm⁻³) | `[재현]` S vol% | `[재현]` C vol% | `[재현]` **SE vol%** | `[도표, Fig. 3d]` 대조 |
|---|---|---|---|---|---|
| **LPB** | **1.491** `[인쇄]` | 53.1 | 11.6 | **35.4** | ≈35.4 ✓ |
| LPS | ≈1.81 `[도표, Fig. 1c]` | 56.6 | 12.3 | **31.1** | ≈30.8 ✓ |
| LGPS | ≈2.04 `[도표, Fig. 1c]` | 58.7 | 12.8 | **28.6** | ≈28.5 ✓ |

`[해석]` 세 값이 모두 그림 판독과 0.3 %p 이내로 일치한다. **§7 의 밀도 집합은 신뢰할 수 있다**
— 이후의 모든 `[재현]` vol% 계산은 이 집합 위에 선다.

### 7.1 같은 wt% 에서 저밀도 SE 가 갖는 부피 이득 (우리 LPSCl 자리)

**입력 경고**: LPSCl 밀도는 **이 논문에 없다** (G6). 아래는 외부 값 **1.64–1.90 g cm⁻³** 를
입력으로 넣은 `[재현]` 이며, **그 입력 자체는 이 위키에 아직 근거 raw 가 없다**.

```
SE 24 g 이 차지하는 부피
  LPB   (1.491) : 16.10 cm³
  LPSCl (1.64)  : 14.63 cm³   → LPB 가 +10.0 % 부피
  LPSCl (1.90)  : 12.63 cm³   → LPB 가 +27.4 % 부피
```

같은 양극(S 50 / KB 10 / SE 24)에서의 SE 부피분율:

| SE | ρ (g cm⁻³) | SE vol% | LPB 대비 |
|---|---|---|---|
| **LPB** | 1.491 | **35.4** | — |
| LPSCl (하한 가정) | 1.64 | **33.2** | −2.2 %p |
| LPSCl (상한 가정) | 1.90 | **30.0** | −5.4 %p |
| LGPS | 2.04 | 28.6 | −6.8 %p |

`[해석]` **"저밀도" 의 이득은 생각보다 작다.** SE 밀도를 1.90 → 1.491 로 **21 % 낮춰도**
부피분율은 30.0 → 35.4 %, 즉 **5.4 %p** 만 오른다. 나머지는 황과 탄소가 차지하기 때문이다.
그런데 논문은 그 5.4 %p 구간에서 ICE 가 31 → 100 % 로 변한다고 말한다 (Fig. 3d). **이득의
크기와 효과의 크기가 맞지 않는다** — 밀도만으로 설명하기에는 효과가 너무 크다. G7(변수 미분리)이
여기서 산술로 드러난다.

### 7.2 복합양극의 이론 혼합밀도 (G11 의 근거)

```
50/2.07 + 10/1.90 + 24/1.491 = 24.155 + 5.263 + 16.097 = 45.515 cm³ (84 g)
→ 공극 0 일 때의 이론밀도 = 84 / 45.515 = 1.846 g cm⁻³
논문의 부피 에너지밀도가 함의하는 밀도 = 2561.8 / 1318.7 = 1.943 g cm⁻³
```

`[해석]` 함의값이 이론 치밀도를 **5.3 % 초과**한다. 물리적으로 불가능한 값이므로, 저자는
다른 성분 밀도(예: LPB 를 결정 이론밀도 1.59, 탄소를 흑연 2.2)를 썼거나 SI Note 4 에서
다른 정의를 쓴 것으로 보인다. 어느 쪽이든 **2561.8 Wh L⁻¹ 는 그대로 인용하면 안 된다.**

---

## 8. 왜 저밀도가 이득인가 — 저자의 논리와 그 근거 (p.6–7, Fig. 4)

저자의 인과 사슬은 **"낮은 SE 부피분율 → 조성 불균일 → bulky sulfur 형성 → 이온 경로 차단 →
낮은 이용률"** 이다. 근거로 제시된 관측 4종:

| # | 관측 | `[인쇄]` 내용 | 강도 |
|---|---|---|---|
| ① | **XRD (Fig. 4a)** | S-C-LPS 분말에는 **결정질 황 피크**, S-C-LPB 분말에는 **비정질 황** | 명확한 사실. 단 원인은 미분리 (G16) |
| ② | **SEM 분말 (Fig. 4b)** | S-C-LPB 응집체가 S-C-LPS 보다 **작다** | 정성 |
| ③ | **SEM/EDS 전극 (Fig. 4c,d)** | pristine S-C-LPS 표면에 **voids** 와 **국부 고강도 황 신호(bulky sulfur, 점선 원)**; S-C-LPB 는 모든 원소 균일 | 정성, 표면 관찰 |
| ④ | **리튬화 후 (Fig. 4e,f)** | S-C-LPS: **bulky Li2S 응집 + 탄소와 상분리** (100 µm 스케일); S-C-LPB: 균일 유지 | 정성, 표면 관찰 |

`[인쇄]` 결정적 문장: "upon further decreasing LPB's volume ratio to **27.9 vol%** and increasing
sulfur volume ratio to **59.2 vol%** in S-C-LPB (65 wt% of sulfur, denoted as S-C-LPB-65), we
also observed larger powder size, worsened content uniformity, and deteriorated battery
performance with lower discharge capacity (**678 mAh g⁻¹**) and poor ICE (**62.3 %**). It
demonstrates that **this phenomenon is independent of the type of SE but related to the SE
volume ratio.**"

`[해석]` **이 한 문장이 논문에서 가장 중요한 대조실험이다** — 같은 LPB 로 부피분율만 내려도
같은 열화가 나타난다는 것. 그러나 (i) 부피분율만 바꾼 게 아니라 **황함량도 바꿨고**,
(ii) 두 점뿐이며, (iii) Fig. 4 의 미세구조 관측은 **SI Fig. 27–29 에 있어 이 digest 가 보지
못했다**. "independent of the type of SE" 라는 강한 일반화가 **2점 비교** 위에 서 있다.

### 8.1 물음에 대한 답: 이득의 메커니즘은 무엇인가

작업 의뢰에서 물은 세 갈래 — (a) 같은 질량비에서 부피분율이 커져 이온 경로가 촘촘해지는가,
(b) 황 함량을 올릴 여지가 생기는가, (c) 둘 다인가 — 에 대해 **논문의 답은 (a) 다.**

`[인쇄]` 근거: "A higher SE volume ratio and lower sulfur volume ratio in S-C-LPB are obtained
compared with S-C-LPS **at the same weight contents, thanks to the lower density of LPB**."
즉 실험 전부가 **같은 질량비(50/10/24)에서 SE 만 바꿔** 수행되었다. (b)는 Fig. 1b 의
**모델 예측**으로만 등장하고 실험되지 않았다 — 오히려 황함량을 65 wt% 로 올린 실험은
**실패**했다(678 mAh g⁻¹, ICE 62.3 %). `[해석]` **논문은 "저밀도 SE 덕에 황을 더 넣을 수
있다" 를 실험으로 보이지 못했다.** 보인 것은 "같은 조성에서 더 잘 된다" 뿐이다.

### 8.2 밀도 효과 vs 입도 효과 — 저자는 분리했는가

**분리하지 않았다** (G7). 논문의 방어는 두 문장이다:

- `[인쇄]` "there is no apparent correlation between cathode performance and SE's ionic
  conductivity/particle size (Figs. 1d, 2a, b and Supplementary Figs. 13 and 16)"
- 그러나 같은 페이지 뒤에서: `[인쇄]` "**in addition to SE volume ratio, the large particle
  size of SE may likewise cause deficient Li⁺ transport pathways and thus the mediocre
  performance of sulfur cathodes** by inducing poor cathode content uniformity with inactive
  bulky sulfur particles and phase separation between carbon and large SE powders
  (Supplementary Fig. 31, 32 and 33 and Supplementary Note 7)"

`[해석]` **앞에서 배제한 변수를 뒤에서 되살린다.** 두 문장이 양립하려면 "≤5 µm 범위 안에서는
입도 효과가 없고 그보다 크면 있다" 여야 하는데, 그 임계를 논문이 제시하지 않는다.
**LPB 의 일차입자 ~500 nm 가 이득에 기여한 몫은 이 논문으로 알 수 없다.**

---

## 9. 용량 감쇠 기전 (p.5–6)

| 관측 | `[인쇄]` |
|---|---|
| 전압 분극 | 첫 몇 사이클에 **좁아졌다가**(활성화 — 부피변화에 의한 성분 재배치로 추정) 이후 **계속 증가** (SI Fig. 21, **미확보**) |
| EIS | **전하전달저항이 1000 사이클 후 수백 옴**까지 증가 — `[인쇄]` "is the culprit" (SI Fig. 22, Table S4, **미확보**) |
| 원인 지목 | `[인쇄]` "the continuous **electrochemical and chemical degradation of LPB SE** during cycling" |
| LPB 산화환원 | `[인쇄]` "LPB would undergo **relatively reversible** lithiation/delithiation for over **100 cycles** in the designated voltage window (i.e., **0.5–2.5 V vs Li–In/Li⁺**)" (SI Fig. 17·23, Note 6, **미확보**) |
| XPS (사이클 후 전극) | `[인쇄]` **P–Sx–P 관찰 = LPB 의 전기화학적 산화 확인** · **S 2p 의 sulfate 종 = 화학적 열화** (SI Fig. 24, **미확보**) |

`[해석]` 열화 서사가 **셀 설계 결함과 섞여 있다** (G17). "chemical degradation" 과 "sulfate"
는 수분·산소 노출의 전형적 산물인데, 이 셀은 **대기 중에서 800 사이클을 돌았고 저자도
밀봉 불완전을 인정한다**. 건조 아르곤 대조군이 없으므로 "LPB 가 본질적으로 화학적으로
불안정하다" 와 "이 셀이 공기를 마셨다" 를 구분할 수 없다. **LiBH4 계 SE 의 수명 한계를 이
논문에서 배울 수는 없다.**

또 하나: `[인쇄]` "relatively reversible … for over 100 cycles" 는 **800 사이클 셀의 앞
1/8 구간에 대한 진술**이다. 나머지 700 사이클 동안 LPB 산화환원이 어떻게 변하는지는 미측정.

---

## 10. GITT 와 과전압 (Fig. 4h,i)

| 항목 | `[인쇄]`/`[도표]` |
|---|---|
| 조건 | `[인쇄]` **3rd cycle**, 펄스 **50.25 mA g⁻¹ 30 min** + **휴지 4 h**, 60 °C |
| 로딩 | `[도표, Fig. 4h]` **S-C-LPS 4.2 mg(S) cm⁻² · S-C-LPB 4.6 mg(S) cm⁻²** — **본 실험만 고로딩** |
| 방전 plateau | `[인쇄]` **~1.59 V 와 ~1.48 V vs Li–In/Li⁺** (= **2.21 · 2.10 V vs Li/Li⁺**) — 1단은 황 → LiPS, 2단은 → Li2S 로 **추정** ("might involve") |
| 같은 2단이 LPS/LGPS 에도 | `[인쇄]` 저황(50 wt% S, SE 40 wt%) 조건에서는 LPS·LGPS 에서도 관찰 (SI Fig. 19a,b, **미확보**) |
| **방전 최대 과전압** | `[도표, Fig. 4i]` **LPB η_max = 0.42 V (OCV 1.27 V) · LPS η_max = 0.74 V (OCV 1.25 V)** `[인쇄, 그림 안]` |
| **충전 최대 과전압** | `[도표, Fig. 4i]` **LPB η_max = 0.72 V · LPS η_max = 0.82 V**; LPB 는 같은 OCV(≈1.68 V)에서 **η = 0.22 V** `[인쇄, 그림 안]` |
| 동일 OCV 구간 용량 비교 | `[인쇄]` 리튬화 OCV **1.57→1.28 V** (2.19→1.90 vs Li/Li⁺), 탈리튬화 **1.58→1.68 V** (2.20→2.30): **LPB 860/950 vs LPS 604/806 mAh g⁻¹** (SI Fig. 34, **미확보**) |
| GITT 방전 종점 | `[도표, Fig. 4h]` LPB ≈**1200** mAh g⁻¹(S), LPS ≈**680** mAh g⁻¹(S) |

`[해석]` **이 분석법이 우리에게 이식 가치가 가장 높다.** "같은 OCV = 같은 반응 진행도" 를
가정하고 **특정 OCV 구간에서 뽑힌 용량을 비교**해 "전기화학적으로 활성인 황의 양" 을 가른다.
가정이 강하지만(`[인쇄]` "assuming that the batteries reached thermodynamic equilibrium after
each 4-h resting and the electrochemical reactions in both cathodes are identical at the same
OCV"), **과전압 곡선 η(OCV) 를 그려 두 셀을 겹치는 표현**은 우리 reference cell 의 혼합 경로
비교에 그대로 쓸 수 있다. 4 h 휴지 × 수십 펄스라 실험 시간이 길다는 것이 비용.

주의: **GITT 셀만 로딩이 4.2/4.6 mg cm⁻² 로 다른 실험(2.0–3.0)의 2배**다. 논문은 이 차이를
언급하지 않는다. 과전압 절대값을 다른 그림의 셀과 비교하면 안 된다.

---

## 11. 전압창·LSV·Li 금속 — 우리 위키 구멍과의 관계

**결론부터: 이 논문은 [[li2s-assb-composite-cathode]] 의 "전압창 제약" 구멍을 메우지 못한다.**

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| **Li–In 기준전위** | `[인쇄]` **"Li-In alloy (~0.62 V vs. Li/Li⁺)"** — **메워진다.** 이제 이 위키에 이 값의 근거 raw 가 생겼다 (본문 p.4, Methods 는 LSV 환산으로 재확인: **4.38 V vs Li–In/Li⁺ = 5 V vs Li/Li⁺**, **−0.62 V vs Li–In/Li⁺ = 0 V vs Li/Li⁺** → 차이 정확히 0.62 V) |
| **황화물 SE 의 산화 한계 수치** | **못 메운다.** LSV 측정 *방법*만 Methods 에 있고 곡선·개시전위는 SI (G3) |
| LPSCl 의 산화 한계 | **없다.** LPSC 는 C-LPSC 대조 전극에만 등장 |
| Li2S 활성화에 필요한 전위 | **해당 없음** — 이 논문은 S8 에서 출발한다 |
| Li 금속 안정성 | `[인쇄]` "metastable interphase … to inhibit the degradation of LPB" 라는 정성 문장 + "lithium penetration may still occur" (G5) |

`[재현]` **이 논문의 전압창을 우리 기준으로 환산**: 운전 0.5–2.5 V vs Li–In/Li⁺ =
**1.12–3.12 V vs Li/Li⁺**; 800 사이클은 0.8–2.5 = **1.42–3.12 V vs Li/Li⁺**.

`[해석]` **상한 3.12 V vs Li/Li⁺ 는 Kim 2023 의 3.6 V 보다 0.5 V 낮다.** 황화물 SE 계에서
실제로 쓰이는 상한이 어디쯤인지에 대한 **실측 사례**로서는 값이 있다 (LPB 는 이 창에서
"relatively reversible" 하다고 저자가 말한다). 그러나 이것은 **작동 사례**이지 **안정창 측정**이
아니다. LPB 가 그 창에서 산화되고 있다는 증거를 논문 스스로 대고 있으므로 (XPS 의 P–Sx–P,
CE >100 %), "3.12 V 까지는 안전하다" 로 읽으면 **틀린다**.

---

## 12. 다른 전략과의 대조 (이 위키 내부)

같은 문제 — **고체계에서 황 이용률이 왜 낮고 어떻게 올리는가** — 를 세 논문이 다른 변수로 푼다.

| | **Wang 2023 (이 논문)** | **Huang 2026** (`raw/papers/huang2026_…`) | **Zhang 2026** (`raw/papers/zhang2026_…`) |
|---|---|---|---|
| 바꾼 변수 | **SE 자체 (밀도·입도·전도도)** | **양극 첨가제** (고엔트로피 황화물 6 wt%) | **음극·집전체** (anode-free Na 박) |
| 활물질 | **S8** (melt-diffusion into KB) | S8 | **Li2S** (+PI3) |
| SE | **LPB, 28.6 wt% / 35.4 vol%** `[재현]` | **LPSC, 40 wt%** | LPSCBr, 40 wt% |
| 온도 | **60 °C** | **상온** | 상온 (일부 90 °C) |
| 스택압 | **50–60 MPa** | 미기재(성형 450 MPa) | **1–4 MPa** |
| 황 이용률 (첫 방전) | **62.5 % (1047.5)** / 최고 **68.3 % (1144.6)** `[재현]` | 첨가제 없음 **39 %** → 있음 **76 %** | — (Li2S 기준 971 mAh g⁻¹(Li2S)) |
| 사이클 | **800 (77.5 %)** | 160 | 200–400 |
| 셀 수준 에너지밀도 | **계산 안 함** (Fig. 1b 는 모델, Fig. 3h 는 양극 기준 — G10) | 계산 안 함 | 계산 안 함 (그쪽 G11) |

`[해석]` 세 가지가 동시에 보인다.

1. **온도가 비교를 망친다.** Wang 은 60 °C, Huang 은 상온이다. Wang 의 68.3 % 가 Huang 의
   76 % 보다 낮은데 **온도는 Wang 이 유리**하다. 즉 "SE 를 바꾸는 전략" 이 "첨가제를 넣는
   전략" 보다 이용률에서 앞섰다고 말할 수 없다. 오히려 **Huang 의 상온 76 % 가 더 어려운
   조건의 결과**다.
2. **저밀도 SE 는 Zhang 2026 의 전해질층 문제를 풀지 않았다.** Zhang 은 전해질층이
   127 mg cm⁻² (복합양극의 27배)라 셀 수준 계산이 불가능했다. Wang 의 분리층은 **80 mg /
   ⌀10 mm ≈ 102 mg cm⁻², 두께 ~600 µm** 로 **같은 크기의 문제**를 갖는다 `[재현]`.
   저밀도 SE 가 겨냥한 것은 **양극 내부의 SE** 이지 분리층이 아니며, **이 논문도 셀 수준
   에너지밀도를 실측하지 않았다.**
3. **세 논문 모두 셀 수준 에너지밀도를 계산하지 않았다.** 이 위키가 아직 어느 논문에서도
   "분모가 명확한 셀 수준 Wh kg⁻¹" 을 확보하지 못했다는 뜻이다.

---

## 13. SI 대조 — 미확보 목록 (정직한 기록)

본문이 인용하는 SI 항목 전부를 여기 적어 둔다. **이 digest 는 아래 중 한 장도 보지 못했다.**
나중에 SI 를 구하면 이 목록이 체크리스트가 된다.

| SI 항목 | 본문이 그것으로 뒷받침하는 주장 | 우리에게 중요한가 |
|---|---|---|
| Supplementary Fig. 1 | ">50 wt% 황에서 >1000 mAh g⁻¹ 를 낸 선행 결과가 거의 없다" (문헌 지도) | 중간 |
| Supplementary Fig. 2 | SE 부피분율·입도가 경로 충분성을 정한다 (모식) | 낮음 |
| **Supplementary Fig. 3, 4 + Note 1** | **저밀도 SE → 높은 SE 부피분율 → >400 Wh kg⁻¹ 셀 모델** | **매우 높음 (G1)** |
| Supplementary Fig. 5 | LPB 액상 합성 절차 도해 | 중간 (Methods 로 대체 가능) |
| Supplementary Fig. 6 | 냉간압축 LPB 3.8 mS cm⁻¹, 상대밀도 86.0 % | 중간 |
| Supplementary Table 1 | **SE 밀도 비교표** (Fig. 1c 의 원값) | **높음 — LPSCl 이 여기 있을 수 있다 (G6)** |
| Supplementary Fig. 7–10 | LPB EDS·TEM·BET·TEM(SAED 대응) | 낮음 |
| Supplementary Fig. 11, 12 | Be 홀더 배경 XRD · 미확인 피크의 출처 | 중간 |
| Supplementary Table 2 | 액상합성 황화물 SE 의 전도도·합성온도 비교 (Fig. 1e 원값) | 중간 |
| Supplementary Fig. 13, 16 | LPS·LGPS 입도 · 성능-입도 상관 | **높음 (G7 의 핵심)** |
| **Supplementary Figs. 14, 15 + Note 3** | **Li\|LPB 계면·대칭셀** | **높음 (G5)** |
| **Supplementary Fig. 17, 23 + Notes 5, 6** | **LPB 의 용량 기여분과 가역성** | **매우 높음 (G4·G12)** |
| Supplementary Fig. 18 | 50 wt% 황 S-C-LPB 가 >1300 mAh g⁻¹ | 높음 |
| Supplementary Fig. 19 | LPS·LGPS 도 SE 40 wt% 면 잘 된다 | **높음 — 우리 50 wt% 와 직결** |
| Supplementary Fig. 20 | ~6 mg cm⁻² 에서 999.7 mAh g⁻¹ | 높음 |
| Supplementary Fig. 21, 22 + Table 4 | 전압 프로파일 변화 · EIS 저항 증가 | 중간 |
| Supplementary Fig. 24 | 사이클 후 XPS (P–Sx–P, sulfate) | 중간 |
| **Supplementary Fig. 25** | **성분별 부피분율 계산표** | **높음 (G2)** |
| Supplementary Fig. 26–30 | S-C-LPB-65 의 형태·성능·모식 | 높음 |
| Supplementary Figs. 31–33 + Note 7 | **큰 입도 SE 의 악영향** | **높음 (G7)** |
| Supplementary Fig. 34 + Note 8 | GITT 상세·OCV 구간 용량·IR drop | 높음 |
| Supplementary Table 3 | Fig. 3h 문헌 비교 셀 조건 | 중간 |

---

## 14. 우리 연구와의 접점

### 14.1 우리 조성의 부피 회계 (`[재현]`)

우리 [[li2s-assb-reference-cell]] 의 복합양극은 **Li2S : LPSCl : AB = 30 : 50 : 20 (wt%)** 이다.
§7 의 방법으로 부피분율을 계산한다.

**입력 경고**: ρ(Li2S) 와 ρ(LPSCl) 는 **이 논문에 없다**. 아래는 ρ(Li2S) = 1.66,
ρ(LPSCl) = 1.64 및 1.90, ρ(AB) = 1.90 (§7 에서 복원한 저자의 탄소 밀도)을 **입력으로 명시**한
`[재현]` 이다. 입력값 자체의 근거 raw 는 이 위키에 아직 없다.

| ρ(LPSCl) 가정 | Li2S vol% | AB vol% | **LPSCl vol%** | 혼합 이론밀도 |
|---|---|---|---|---|
| 1.64 | 30.6 | 17.8 | **51.6** | 1.69 g cm⁻³ |
| 1.90 | 32.9 | 19.2 | **47.9** | 1.82 g cm⁻³ |

`[해석]` **이것이 이 논문에서 우리가 얻는 가장 실질적인 한 줄이다.**

우리 양극의 SE 부피분율은 **48–52 vol%** 로, 이 논문이 "충분" 하다고 판정한 **LPB 양극의
35.4 vol% 보다 13–16 %p 높다.** 즉 **Wang 2023 의 기준으로 보면 우리 조성은 이미 SE 부피가
넉넉하고, "SE 부피분율 부족" 은 우리 500–600 mAh g⁻¹ 정체의 원인 후보에서 내려가야 한다.**
역으로 말하면 우리는 **Wang 이 실패한 영역(S 59 vol%)이 아니라 성공 영역의 더 안쪽**에 있다 —
문제는 다른 데 있다.

이것은 [[reference-cell-500-600-mahg]] 의 **H2(퍼콜레이션 제한)를 이온 쪽과 전자 쪽으로
쪼개야 한다**는 뜻이다. 이온 퍼콜레이션은 부피분율만 보면 문제가 아니고, 남는 후보는
(i) **전자 네트워크**(AB 17–19 vol% 가 절연체 Li2S 30 vol% 를 감싸기에 충분한가),
(ii) **Li2S 입자 크기**(H3), (iii) **활성화**(H1) 다.

### 14.2 이식 가능/불가

| 이 논문의 것 | 우리 reference cell 로 | 이유 |
|---|---|---|
| **부피분율 회계 (wt% → vol%)** | **○ 즉시** | 산술이고 재료 무관. 우리 조성표에 vol% 열을 붙이면 끝. **가장 값싼 이식** |
| **GITT η(OCV) 곡선 비교법** (Fig. 4i) | **○** | 혼합 경로 A/B 를 같은 축에서 비교할 수 있다. 비용은 시간(펄스 30 min + 휴지 4 h) |
| **같은 OCV 구간 용량 비교로 "활성 활물질량" 추정** | **△** | 가정이 강하다(열역학 평형·동일 반응). Li2S 계는 첫 충전 활성화 때문에 3rd cycle 에서도 상태가 다를 수 있다 |
| **Li–In ≈ 0.62 V vs Li/Li⁺** | **○** | `[인쇄]` 근거 확보. 우리 전압 표기 환산의 근거가 된다 |
| **Two-step 혼합 (활물질–탄소 먼저, SE 나중)** | **○ 참고** | 단 이 논문의 2단계는 **350 rpm × 10 h** 로 고에너지다. [[one-step-vs-two-step-mixing]] H2 에 "고에너지 2단계도 800 사이클을 돌렸다" 는 정황 하나가 추가된다 (SE 손상 여부는 미측정이므로 약한 근거) |
| **저밀도 LPB SE 자체** | **✕ 단기** | Cl → BH4 치환은 다른 물질이다. 합성 3.5일 + 160 °C 어닐링 + 액상 취급. 우리 축(Li2S 활성화)과 직교하며, **Li 금속 안정성 데이터가 없다**(G5) |
| **melt-diffusion (160 °C 10 h) 으로 활물질–탄소 결합** | **✕** | **Li2S 는 녹지 않는다** (mp 938 °C). S8 전용 공정이다 |
| **"SE 부피분율을 올려라" 는 처방** | **✕ 우리에게는 이미 해결됨** | §14.1 — 우리는 48–52 vol% 다 |
| **60 °C 운전** | **△** | 이 논문의 모든 수치는 60 °C 다. 상온 목표라면 이 논문의 이용률을 기준선으로 삼을 수 없다 |
| **50–60 MPa 스택압** | **△** | Zhang 2026 의 1–4 MPa 와 한 자릿수 이상 차이. 우리 셀의 압력 조건을 명시하지 않으면 어느 쪽과도 비교 불가 |
| **첫 충전 활성화 프로토콜** | **✕ 해당 없음** | S8 양극이라 활성화 단계가 없다 |

### 14.3 질문 카드 라우팅 (부모 에이전트가 컴파일할 것)

| 카드 | 가설 | 이 논문이 주는 것 | 방향 |
|---|---|---|---|
| [[reference-cell-500-600-mahg]] | **H2 (퍼콜레이션 제한)** | Wang 기준 "충분한 SE 부피분율" = **35.4 vol%**. 우리는 `[재현]` **48–52 vol%** | **Against (이온 퍼콜레이션 한정)** — SE 부피 부족은 우리 병목이 아닐 가능성이 크다. H2 를 이온/전자로 분할 제안 |
| [[reference-cell-500-600-mahg]] | **H4 (단위 착시)** | 이 논문의 모든 수치가 **mAh g⁻¹(S)** 다. 1144.6(S) = `[재현]` 798.9(Li2S). 문헌의 "1000 mAh g⁻¹ 급" 이 Li2S 기준으로는 700 대라는 실례 | **For (보강)** — 문헌 비교 시 기준 혼동의 크기를 구체적으로 보여주는 사례 |
| [[reference-cell-500-600-mahg]] | (신규 관찰) | **S 이용률 68.3 % 가 60 °C·2.5 mg cm⁻²·스택압 55 MPa 에서의 최고값**. 상온·저압이면 더 낮다 | 기준선 정보 |
| [[one-step-vs-two-step-mixing]] | **H2 (SE 보호 이유)** | two-step 이되 **2단계가 350 rpm × 10 h 고에너지**. 800 사이클 작동. 단 **밀링 후 SE 전도도·XRD 미측정** | **약한 Against** — "SE 를 고에너지에서 빼야 한다" 의 반례 후보이나 증거가 간접적 |
| [[one-step-vs-two-step-mixing]] | (신규 관찰) | **같은 밀링 조건에서 SE 종류만 바꿨는데 황의 결정성이 달라졌다** (Fig. 4a) | 혼합 중 상호작용이 SE 물성에 의존한다는 직접 관측 |

### 14.4 가장 값싼 다음 실험

`[해석]` 이 논문을 읽고 우리가 **오늘 할 수 있는 것**:

1. **계산 하나** — 우리 조성표에 **vol% 열을 추가**한다 (필요한 것은 ρ(Li2S)·ρ(LPSCl)·ρ(AB)
   뿐). 실험 없이 "SE 부피분율 가설" 을 판정할 수 있다. §14.1 이 이미 초안이다.
2. **측정 하나** — **LPSCl 분말의 실측 밀도** (He 피크노미터, 이 논문과 같은 방법: ~0.4 g,
   Ar 밀봉, 대기 노출 <1 min, 10회). 이 값 하나가 위키의 G6 구멍을 닫고 §14.1 의 범위를
   한 점으로 줄인다.
3. **실험 하나** — 우리 reference cell 에 **GITT (펄스 30 min / 휴지 4 h)** 를 걸어
   **η(OCV) 곡선**을 얻는다. 방전 η_max 가 0.4 V 대면 이온 수송이 문제가 아니고, 0.7 V 대면
   무언가 막혀 있다는 1차 판별이 된다 (단 이 논문은 60 °C 이므로 절대값 비교는 불가,
   **우리 셀들 사이의 상대 비교용**).

---

## 15. 비판

1. **핵심 변수가 분리되지 않았다 (G7).** LPB 는 저밀도·소입경·고전도를 동시에 갖는다.
   "밀도가 원인" 이라는 결론은 **세 점의 상관**과 **두 점의 부피분율 시리즈**로 지탱된다.
   §7.1 의 산술은 이 문제를 정량으로 드러낸다 — SE 밀도를 21 % 낮춰도 부피분율은 5.4 %p 만
   오르는데, 그 구간에서 ICE 가 69 %p 움직인다는 것은 **밀도 외의 무언가가 작동하고 있다**는
   뜻이다. 가장 유력한 후보는 입도(500 nm vs ≤5 µm)이고, 논문은 그것을 앞에서 배제했다가
   뒤에서 되살린다.

2. **"높은 ICE" 가 사실은 기생 산화의 신호다 (G12·G4).** ICE 100.2 %, 800 사이클 CE
   ≈100.1 % `[도표]`, 초기 20 사이클 용량 상승을 저자 스스로 "LPB 산화환원 기여의 성장" 으로
   설명, 사이클 용량의 ">82 %" 만 황. 이 네 가지는 **같은 현상의 네 얼굴**인데 논문은 앞의
   둘을 장점으로, 뒤의 둘을 각주로 배치한다. **광고된 778.9 mAh g⁻¹(S) 는 최악의 경우
   638.7 (= 445.8 mAh g⁻¹(Li2S))** 까지 내려갈 수 있고, 논문은 그 보정값을 한 번도 제시하지
   않는다.

3. **에너지밀도 수치가 분모를 흐린다 (G9·G10·G11).** Fig. 3h 의 축은 "**Cell** specific
   energy" 인데 캡션은 "**sulfur cathodes** 의 무게 기준" 이다. `[재현]` 1144.6 × 1.935 ×
   0.5952 = 1318.2 로 분모가 복합양극 질량임이 확인된다 — SE 분리막 ~102 mg cm⁻²,
   Li–In, 집전체가 전부 빠졌다. 부피 에너지밀도 2561.8 Wh L⁻¹ 는 **이론 치밀도를 5 % 초과하는
   복합양극 밀도**를 함의한다. 그리고 목표치는 서론 400 → 결론 300 Wh kg⁻¹ 로 미끄러진다.
   **"고밀도 SE 때문에 에너지밀도가 낮다" 로 시작한 논문이 자기 셀의 에너지밀도를 재지
   않았다.**

부가로: 셀 개수가 핵심 그림들에 없고 (G13), 유지율 기준점이 유리하게 잡혔으며 (G14),
셀이 대기 중에서 돌아가 열화 기전이 설계 결함과 섞였고 (G17), 혼합 조건의 절반이 빠졌다 (G15).

---

## 16. 이 저장소가 가져갈 것

1. **부피 회계라는 도구.** 복합양극 조성을 wt% 로만 적는 관행을 버리고 **vol% 를 병기**한다.
   §7 의 계산 절차(밀도 집합 → 부피 → 분율)를 우리 조성표에 붙인다. 이것이 이 논문에서
   가장 확실하게 남는 것이다.
2. **우리 SE 부피분율은 이미 높다 (48–52 vol%, `[재현]`).** Wang 의 "충분" 기준 35.4 vol%
   보다 훨씬 위다 → [[reference-cell-500-600-mahg]] H2 의 이온 쪽 갈래를 약화시킨다.
3. **Li–In ≈ 0.62 V vs Li/Li⁺ 의 근거 raw 확보.** `[인쇄]` 본문 p.4 + Methods 의 LSV 환산
   (4.38 vs Li–In = 5 vs Li/Li⁺). 이 위키의 단위 규율이 지금까지 "인용 금지" 로 두었던 값이다.
4. **GITT η(OCV) 비교법.**
5. **"전압창 제약" 구멍은 아직 열려 있다** — LSV 방법은 알았으나 데이터는 SI (G3).
   SI 를 구하거나 다른 논문을 흡수해야 한다.
6. **셀 수준 에너지밀도를 분모까지 적은 논문이 아직 이 위키에 하나도 없다** (Wang·Huang·Zhang
   전부). 이것을 열린 공백으로 기록해 둔다.

---

## 17. 그림 판독 기록

`raw/figures/wang2023_high-capacity-assb-li-s-low-density-solid-electrolyte/` 에 **본문 Fig. 1–4
네 장**이 있다. SI 그림은 **한 장도 없다** (SI 파일 미확보).

**추출기 보정 기록**: `extract_figures.py` 가 Fig. 1 을 좌측 컬럼(패널 d 부근)만, Fig. 3 을
캡션 바로 위 289 px 띠로만 잘랐고 **Fig. 4 는 통째로 놓쳤다**. 캡션 블록 좌표(p.5 y=459.8,
p.6 y=521.1)를 기준으로 **Fig. 1·3·4 를 다시 잘라 넣었다.** `figures.json` 의 해당 항목도
새 bbox·크기로 갱신했다.

| 그림 | 파일 | 실제로 보았나 | 무엇을 읽었나 |
|---|---|---|---|
| **Fig. 1 (전체)** | `fig_1.png` | **보았다** (+ 패널 b·c·d 확대 별도) | — |
| Fig. 1a | (패널) | 보았다 | SE 부피분율 증가 → 경로 충분성 모식 |
| **Fig. 1b** | (패널) | **보았다** | 밀도 1.0–5.5 에 대한 셀 비에너지·황 wt% 막대 10쌍 전부 판독 (§2 표). 고정조건 "50 vol% Sulfur, 4 mg(S) cm⁻²" |
| **Fig. 1c** | (패널) | **보았다** | 밀도 막대 8종: LE ≈1.13 · PEO ≈1.20 · **LPB 1.491** · TTE ≈1.52 · LPS ≈1.81 · LGPS ≈2.04 · LATP ≈2.91 · LLZO ≈5.12. **LPSCl 없음 (G6)** |
| Fig. 1d | (패널) | 보았다 | Arrhenius 5점(25–100 °C) + 오차막대, Nyquist 삽입, σ25 6.0 mS cm⁻¹, Ea 0.216 eV |
| Fig. 1e | (패널) | **부분** | 적색 별(this work)이 ≈6×10⁻³ S cm⁻¹ / 합성온도 축 좌측. 범례 일부만 확인, 개별 문헌 점은 판독 안 함 |
| **Fig. 2 (전체)** | `fig_2.png` | **보았다** | 2a SEM 응집체(20 µm 스케일) · 2b STEM 일차입자 ~500 nm · 2c SAED 반점+링 · 2d XRD (111)(200)(220)(311)(222)(331)(400)(422)(511) + Holder 피크 · 2e Raman PS4³⁻ 418 / P2S6⁴⁻ 386 / BH4⁻ ~2300 · 2f ³¹P I·II·III · 2g ⁷Li LPB/LPS/LiBH4 |
| **Fig. 3 (전체)** | `fig_3.png` | **보았다** (+ 패널 b–h 확대) | — |
| Fig. 3a | (패널) | 보았다 | Swagelok 모식 + 양극/SE막/Li합금 3층 |
| **Fig. 3b** | (패널) | **보았다** | 3곡선, "60 wt% sulfur", "2.0~3.0 mg(S) cm⁻²", 167.5 mA g⁻¹. LPB 방전 종점 ≈1050 |
| **Fig. 3c** | (패널) | **보았다** | dQ/dV. LPB 충전피크 III ≈8800 mAh g⁻¹ V⁻¹ vs LPS/LGPS ≈1300. 축 **V vs Li–In/Li⁺** |
| **Fig. 3d** | (패널) | **보았다** | ICE ≈102 / 72 / 29 (오차막대 있음) · **SE vol% ≈35.4 / 30.8 / 28.5** · C vol% ≈11.6 / 12.4 / 12.7 |
| **Fig. 3e,f** | (패널) | **보았다** | 율속 4구간 + 복귀. f 는 LPB 4전류 방전곡선 (1675 mA g⁻¹ 에서 ≈650) |
| **Fig. 3g** | (패널) | **보았다** | 800 사이클. "Initial: 2.58 mAh cm⁻²", "2.57 mg(S) cm⁻²", "0.8~2.5 V", "837.5 mA g⁻¹, CCCV". **CE(우축 96–101 %) 가 전 구간 ≈100.0–100.2 %** |
| **Fig. 3h** | (패널) | **보았다** | y축 "**Cell** specific energy (Wh kg⁻¹)" ← 캡션과 불일치 (G10). This work ≈1320 @800 cyc; Ref 54 ≈960 @~10, Ref 14 ≈915 @100, Ref 56 ≈780, Ref 52 ≈755, Ref 53 ≈640, Ref 6 ≈370 @750, Ref 13 ≈355 @~20, Ref 55 ≈330 @400, Ref 12 ≈260 @200 |
| **Fig. 4 (전체)** | `fig_4.png` | **보았다** (+ 패널 a–i 확대) | — |
| **Fig. 4a** | (패널) | **보았다** | S-C-LPS 에 **황 결정 피크(◆)** 다수, S-C-LPB 는 **Holder 피크만** |
| Fig. 4b | (패널) | 보았다 | S-C-LPS 응집체가 크고 매끈, S-C-LPB 는 작고 거칢 (20 µm 스케일) |
| **Fig. 4c–f** | (패널) | **보았다** | c: LPS 전극 voids + 점선 원 "Bulky sulfur" (25 µm) · d: LPB 전극 3원소 균일 (25 µm) · e: 리튬화 LPS "Bulky Li2S" 노란 점선 + 탄소 "Phase separation" (100 µm) · f: 리튬화 LPB 균일 (100 µm) |
| Fig. 4g | (패널) | 보았다 | Low / Moderate SE 부피분율 모식, "Active / Bulky / Inactive sulfur" |
| **Fig. 4h** | (패널) | **보았다** | GITT 2단. 상단 LPS **4.2 mg(S) cm⁻²** 방전 종점 ≈680, 하단 LPB **4.6 mg(S) cm⁻²** 종점 ≈1200. 우축 vs Li/Li⁺, 좌축 vs Li–In/Li⁺ 병기 |
| **Fig. 4i** | (패널) | **보았다** | η(OCV) 2단. 방전 η_max LPB 0.42 (OCV 1.27) vs LPS 0.74 (OCV 1.25); 충전 η_max LPB 0.72 vs LPS 0.82, LPB η=0.22 표시 |

**보지 못한 것** (정직한 기록):
- **Supplementary Fig. 1–34, Supplementary Table 1–4, Supplementary Note 1–8 전부** — SI 파일 미확보.
- Fig. 1e 의 개별 문헌 데이터점(refs 19–36)과 전체 범례.
- Fig. 2 의 XRD 미확인 피크 위치를 정밀 판독하지 않았다 (저자도 "low-intensity unknown" 으로만 적는다).
- Fig. 3h 의 문헌점 좌표는 눈대중이며 ±5 % 수준의 오차가 있다.

---

## 부록 A. 이 digest 가 쓴 환산 상수와 식

```
(Li2S) 기준 = (S) 기준 × 0.698            [M(S)/M(Li2S) = 32.065/45.95]
(composite) 기준 = (S) 기준 × w_S          [w_S = 0.5952 (60 wt% 계열), 0.50 (50 wt% 계열)]
S 이용률 = (S) 기준 / 1675 mAh g⁻¹(S)
1 C ≡ 1675 mA g⁻¹(S)
전압: V(vs Li/Li⁺) = V(vs Li–In/Li⁺) + 0.62      [인쇄: p.4, Methods]
부피분율: φ_i = (m_i/ρ_i) / Σ(m_j/ρ_j)
밀도 집합 (저자 값 역산, §7): ρ(S)=2.07 · ρ(C)=1.90 · ρ(LPB)=1.491 g cm⁻³
그림 판독 밀도: ρ(LPS)≈1.81 · ρ(LGPS)≈2.04 g cm⁻³   [도표, Fig. 1c]
외부 입력(이 논문에 없음): ρ(LPSCl)=1.64–1.90 · ρ(Li2S)=1.66 g cm⁻³
```

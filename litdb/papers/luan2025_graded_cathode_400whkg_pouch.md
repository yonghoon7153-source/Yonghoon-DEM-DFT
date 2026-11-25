# Luan 2025 (Adv. Funct. Mater. 36, e26239) — **이온/전자 flux 에 맞춘 전하운반체 공간분포**로 만든 graded 복합양극 → **5 Ah 파우치 404 Wh/kg** ★ 우리 **Phase-5(층상 양극) + 백로그 A7(graded-z)** 의 실험적 실현판

> slug `luan2025_graded_cathode_400whkg_pouch` · DOI `10.1002/adfm.202526239` · type `exp + FEM (COMSOL phase-field)` · PDF `1b324395-56._Adv_Funct_Materials__2025__Luan__Electrode_Engineering_Strategy_for_400_Wh_kg_1_All_Solid_State_Pouch_Cells__Spatial.pdf` · digested `2026-08-11` · status ✅

**인용:** Tengjiao Luan, Hang Zhang, Yue Ji, Yuqi Gong, Zaifa Wang, Shuaike Wang, Yu Xia, Yue Gong,
Zhenghao Li, Chenyang Li, Yingying Jiang, Biwei Xiao, Xiaona Li, Jianwen Liang, **Xueliang Sun\***,
**Changtai Zhao\***, "Electrode Engineering Strategy for 400 Wh kg⁻¹ All-Solid-State Pouch Cells:
Spatial Optimization of Charge Carriers Based on Electron and Ion Transport Flux",
*Adv. Funct. Mater.* **2026**, *36*, e26239. DOI 10.1002/adfm.202526239.
Received 2025-10-03 · Published online 2025-11-17. 본문 13 pp (Fig 1–7, refs 59) + SI (Fig S1–S10, Table S1–S2).

**소속:** National Power Battery Innovation Center, **GRINM Group Co. Ltd** (Beijing) · **GRINM
(Guangdong) Institute for Advanced Materials and Technology** (Foshan) · China Automotive Battery
Research Institute · General Research Institute for Nonferrous Metals · **Eastern Institute of
Technology (EIT), Ningbo** (Xiaona Li, **Xueliang Sun** — Ningbo Key Lab of All-Solid-State Battery).
교신 zhaocht@glabat.com / xsun@eitech.edu.cn. ⚠ Sun 그룹은 Western Univ. 가 아니라 **EIT Ningbo** 소속으로
표기됨(2025 이적 후). 산업체(GRINM/CABRI) 주도의 **파일럿 스케일** 논문.

**소재계 (★우리와 사실상 동일):** **NCM88 = LiNi₀.₈₈Co₀.₀₈₅Mn₀.₀₃₅O₂** (3–5 µm) + **LPSC = Li₆PS₅Cl**
(1–2 µm, σ_ion **2±0.1 mS/cm**) + **Super P** (60–80 nm) + **PTFE**(파우치/건식전극 한정) ·
음극 = 코인셀 **Li–In**(In foil 0.2 mm + Li 3 mg) / 파우치 **순수 Si**.
⇒ 우리 production (NMC811 + LPSCl + Super P/VGCF + PTFE, 건식) 과 **1:1 대응**. Ni 함량만 0.80→0.88.

**DB 동반 파일:** 없음(생성 안 함). 모든 수치는 본 MD 표에 정리. 그림 크로핑 =
`litdb/figures/luan2025_graded_cathode_400whkg_pouch/fig_1..7.png` (본문 7장; **SI PDF 미보유** — SI 는
사용자가 .docx 에서 뽑은 **캡션 텍스트만** 확보, SI 그림 실물은 못 봤다).

---

## 1. 한 줄 요약

두꺼운 ASSB 양극에서 **Li⁺ flux 는 분리막쪽이 최대·집전체쪽이 0** 이고 **전자 flux 는 정확히 반대**라는
자명하지만 아무도 설계에 안 쓰던 사실을 **층별 조성 구배**로 구현 — SE 를 분리막쪽에 몰고(positive)
도전재를 집전체쪽에 몰면, **총량을 바꾸지 않고도** 4 mAh cm⁻² · CAM 91.5 wt% 에서 방전용량이
**204.7 vs 186.1(uniform) vs 178.0(reverse) mAh g⁻¹** 로 갈리며, 이를 건식 롤프레스로 만들어
**5 Ah 파우치 404 Wh kg⁻¹** 을 실증했다.
★ **우리에게 중요한 이유:** ① 우리 Phase-5(층상 복합양극)·백로그 A7(graded-z)의 **published archetype**,
② 그들의 핵심 결론("전자망은 아주 조금이면 충분, 병목은 이온")이 우리 **STEP4 실측**(2C 옴강하 = 전자
0.01–0.03 mV vs 이온 84–90 mV)과 **독립적으로 같은 답** = frame[4] 교차검증,
③ **입자 형상 소성 없음·DEM 없음** → Varkey·Bazzoun·Duquesnoy·Nam 에 이은 **frame[5] 5번째 독립 확증**.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저널/년 | Adv. Funct. Mater. 2026, 36, e26239 (online 2025-11-17) |
| DOI | 10.1002/adfm.202526239 |
| 소재 (SE/CAM/도전재/바인더) | Li₆PS₅Cl / LiNi₀.₈₈Co₀.₀₈₅Mn₀.₀₃₅O₂ / Super P / PTFE(건식만) |
| 연구유형 | **실험 주도** (전기화학·XRD·SEM-EDS·TOF-SIMS·EIS-DRT·GITT·CV·DC분극) + **COMSOL phase-field FEM 보조** |
| DEM / 입자-레벨 시뮬 | **없음** (§4-3 판정) |
| 스케일 | 코인셀(⌀10 mm 급 펠릿) → **5 Ah 파우치 60 × 80 mm** |
| 우리 축 매핑 | **A**(제조압 300 MPa 일치, porosity 미보고) · **B**(σ_e vs SE% 6-decade + LPSC bulk 2 mS/cm) · **C**(PTFE fibril 실사) · **D**(단봉 AM 3–5 µm : SE 1–2 µm ≈ 3:1) · **E**(우리 STEP4 φ_e/φ_i 가 그들 결론을 정량 확인) · **F**(사이클·파우치·건식 롤프레스 = 우리 미보유) |

---

## 3. 핵심 수치

> 표기 규약: **stated** = 본문/SI 텍스트에 적힌 값 · **figure-read ≈** = 내가 크로핑한 그림에서 눈으로
> 읽은 값(추세 전용, 유효숫자 신뢰 금지) · **DERIVED(ours)** = 내가 논문 값 + 명시한 가정으로 계산한 값
> (논문에 없음).

### 3-1. 소재·공정 파라미터

| 항목 | 값 | 출처 |
|---|---|---|
| NCM88 입경 | **3–5 µm** | stated (SI Fig S2 캡션) |
| LPSC 입경 | **1–2 µm** | stated (SI Fig S2 + 본문) |
| Super P 입경 | **60–80 nm** | stated (SI Fig S2 캡션) |
| LPSC 이온전도도 | **2 ± 0.1 mS cm⁻¹** | stated (본문 §2.1) |
| SE 분리막층 예압 | **100 MPa** | stated (Experimental) |
| **양극 성형압** | **300 MPa** | stated ★ **우리 production 과 동일** |
| Li–In 음극 압력 | 100 MPa | stated |
| 셀 최종 consolidation | **200 MPa** | stated |
| 파우치 등방압(isostatic) | **500 MPa, 2 min** | stated |
| **사이클 중 외부 스택압** | **30 MPa** | stated ★ 제조압(300–500)과 **명확히 분리** |
| 전압창 (코인, vs Li⁺/Li–In) | 1.9–3.7 V | stated |
| 1 C 기준 | **4 mA cm⁻²** | stated |
| 파우치 dry room 이슬점 | −45 °C | stated |
| porosity / 전극 밀도 / 두께 | **n/a — 논문이 어디에도 안 준다** | ⚠ 결손 (SI Fig S6b 가 두께 그림이나 SI PDF 미보유) |

### 3-2. 조성 · 구배 설계 ★ (총량 보존 여부 = 핵심 점검)

**실험 3종 (평균 CAM 91.5 wt%, 4 mAh cm⁻², 2층):** NCM88 : LPSC : Super P (wt%)

| 배치 | 분리막(SE층) 쪽 층 | 집전체 쪽 층 | 총 CAM | 총 SE | 총 carbon |
|---|---|---|---|---|---|
| **Ⅰ positive** | **90 : 9 : 1** (SE-rich) | **93 : 6 : 1** (CAM-rich) | 91.5 | 7.5 | 1.0 |
| **Ⅱ uniform** | 91.5 : 7.5 : 1 | 91.5 : 7.5 : 1 | 91.5 | 7.5 | 1.0 |
| **Ⅲ reverse** | 93 : 6 : 1 | 90 : 9 : 1 | 91.5 | 7.5 | 1.0 |

★★ **세 배치의 CAM·SE·carbon 총량이 완전히 같다 = 공정한 비교** (우리 `--poro-grad` 의 *총량 고정 게이트*
와 같은 규율). **이 논문의 +10~15 % 용량 차이는 "SE 를 더 넣어서"가 아니라 순수하게 "SE 를 어디에 두느냐"
에서 나온 것**이다 — 이것이 이 논문의 유일하고 진짜인 헤드라인.

**COMSOL Table S1 (SE 부피분율):**

| 배치 | cathode region 1 | cathode region 2 | 평균 | 대비(Δ) |
|---|---|---|---|---|
| Ⅰ | **0.1875** | **0.3125** | 0.25 | 0.125 |
| Ⅱ | 0.25 | 0.25 | 0.25 | 0 |
| Ⅲ | 0.3125 | 0.1875 | 0.25 | 0.125 |

시뮬도 총량 보존 ✓ (평균 0.25 고정). **region 1 = 집전체쪽(위), region 2 = 분리막쪽(아래)** — Fig 4j–l
캡션 "Region 1 (upper) / Region 2 (lower)" + 패널의 Current collector(위)/Electrolyte(아래) 배치로 확정.

⚠★ **DERIVED(ours) — 시뮬 조성이 실험 조성과 안 맞는다.** ρ(NCM88)=4.8, ρ(LPSC)=1.86, ρ(SuperP)=2.0 g cm⁻³
(우리 production 값, 논문 미제시 = **ASSUMED**) 로 wt%→vol% 환산하면 실험 층들의 **고체기준 φ_SE** 는

| 층 | wt% | **φ_SE(of solid)** DERIVED |
|---|---|---|
| 93 : 6 : 1 | CAM-rich | **0.140** |
| 91.5 : 7.5 : 1 | uniform | **0.171** |
| 90 : 9 : 1 | SE-rich | **0.201** |

즉 **실험 평균 φ_SE ≈ 0.171 · 대비 Δ ≈ 0.061** 인데, COMSOL 은 **평균 0.25 · 대비 Δ 0.125** — 평균이
**1.5×**, 대비가 **2.0×** 더 크다. ⇒ **COMSOL 은 실험의 정량적 쌍둥이가 아니라, 더 SE-rich·더 극단대비
조건의 정성적 동반자**다. (실제로 시뮬의 positive/reverse 격차가 실험보다 훨씬 크게 나온다 — §3-3 비교.)

**SI Fig S9 — 이중 구배(SE + 도전재 동시, 서로 반대 방향):**
분리막쪽 **85 : 14.5 : 0.5** / 집전체쪽 **88 : 11 : 1** (4 mAh cm⁻², 25 °C, 0.1/0.3/0.5/1 C) — stated.
★ SE 14.5→11(집전체로 감소) ∧ carbon 0.5→1(집전체로 증가) = **논문 제목의 "dual flux" 설계를 실제로
만든 유일한 조성**. 단 이 조성의 성능 수치는 SI 그림에만 있고 본문 텍스트에 없다(SI PDF 미보유 → **n/a**).

### 3-3. 전기화학 — 배치 3종 (4 mAh cm⁻², 0.1 C)

| 지표 | Ⅰ positive | Ⅱ uniform | Ⅲ reverse | 출처 |
|---|---|---|---|---|
| **1st 방전용량** | **204.7** | **186.1** | **178.0** mAh g⁻¹ | **stated** |
| positive 대비 이득 | — | **+10.0 %** | **+15.0 %** | DERIVED(ours), stated 값에서 |
| 1st 충전용량 | ≈240 | ≈220 | ≈213 mAh g⁻¹ | figure-read ≈ (Fig 4d–f) |
| **COMSOL 방전시간** | ≈580 | ≈540 | ≈400 s | figure-read ≈ (Fig 4g–i) |
| 시뮬 이득(pos 기준) | — | ≈+7 % | ≈**+45 %** | DERIVED(ours) from figure-read |

★ **실험 +15 % vs 시뮬 +45 %** (reverse 대비) — 시뮬이 reverse 페널티를 **3× 과장**. §3-2 에서 본
"시뮬 φ_SE 대비가 실험의 2.05×" 와 방향·크기 모두 정합 ⇒ **시뮬은 정성 동반자로만 인용할 것.**

**Rate (Fig 5b, figure-read ≈, mAh g⁻¹):**

| C-rate | positive | uniform | reverse |
|---|---|---|---|
| 0.1 C | ≈218 | ≈211 | ≈208 |
| 0.2 C | ≈205 | ≈197 | ≈193 |
| 0.3 C | ≈197 | ≈186 | ≈181 |
| 0.4 C | ≈189 | ≈178 | ≈172 |
| 0.5 C | ≈181 | ≈170 | ≈163 |
| **1 C** | **≈155** | **≈137** | **≈124** |
| 복귀 0.3 C | ≈196 | ≈185 | ≈180 |

★ **격차가 rate 와 함께 벌어진다** (0.1 C 에서 +5 % → 1 C 에서 **+25 %**) = 구배 이득이 **열역학 용량이
아니라 수송(rate capability)** 에서 온다는 결정적 증거. **우리 SDCP 2C CCCV 서사(rate-capability 이득이지
열역학 용량 아님)와 정확히 같은 논법.**
⚠ Fig 5b 의 0.1 C 값(≈218/211/208)이 Fig 4d–f 의 stated 204.7/186.1/178.0 과 다르다 — **다른 셀/다른 시험**
으로 보인다. 논문이 설명 안 함. **stated 값을 쓸 것.**

### 3-4. CAM 분율 × 면적용량 = **설계창 (가장 전이 가능한 표)** ★★

| 면적용량 | CAM 80 % | 85 % | 90 % | 93 % | 95 % |
|---|---|---|---|---|---|
| **4 mAh cm⁻²** | ≈214 | ≈210 | ≈203 | **178.0** ⛔ | — |
| **2 mAh cm⁻²** | — | ≈207 | ≈200 | **199.9** ✓ | **160.6** ⛔ |
| **1 mAh cm⁻²** | — | — | — | — | **199.6** ✓ |

(⛔/✓ = 명목용량 미달/도달. 4·2·1 mAh 열의 93/95/95 값과 "80·85·90 % 는 ~200" 은 **stated**;
나머지 막대는 **figure-read ≈** Fig 2d.)

★ **"허용 최대 CAM 분율은 면적용량(=두께)의 감소함수"** — 1 mAh cm⁻² 에선 95 % 도 되지만
4 mAh cm⁻² 에선 90 % 가 천장. 논문이 이 문턱의 지배 변수를 **"SE 의 이온전도도와 입경"** (여기선
2 mS/cm · 1–2 µm)으로 명시 ⇒ **σ_SE·r_SE 를 바꾸면 문턱이 움직인다** = 우리 σ_ionic 폼이 예측해야 할
바로 그 축. **우리 ML 설계 폐루프(ml_design_loop.py)의 외부 설계창 앵커로 즉시 사용 가능.**

**Fig 2f XRD (delithiation 깊이의 공간 불균일 직접 증거):** 집전체쪽 표면에서 측정, Al₂O₃ 내부표준,
0.59 mA cm⁻² 충전 종료 시 (003) 피크 이동 — **3 mAh cm⁻²: Δ2θ = 0.78° · 6 mAh cm⁻²: Δ2θ = 0.62°** (stated).
두꺼운 쪽이 **덜 탈리튬화** + 피크 broadening 증가(구조 무질서·응력 축적). ★ **"두꺼우면 집전체쪽 CAM 이
안 쓰인다"의 유일한 재료-직접 증거**(TOF-SIMS 는 분리막쪽만 봄).

### 3-5. SE 함량 → 전자전도도·용량 (Fig 7a,b) ★★ B축 앵커

도전재 **0.5 wt% 고정**, SE 10→90 wt% 스윕. DC 분극(SS | 압축 복합양극 펠릿 | SS, 100 mV, 정상상태).

| SE wt% | 비용량 (mAh g⁻¹) | σ_e (Fig 7b 축 라벨 = S cm⁻¹) | **DERIVED φ_AM(of solid)** |
|---|---|---|---|
| 10 | ≈201 | ≈2 | 0.768 |
| **20** | **≈213 (최대)** | ≈0.17 | 0.601 |
| 30 | ≈200 | ≈0.02 | 0.469 |
| 40 | ≈181 | ≈2.7e−3 | 0.363 |
| 50 | ≈127 | ≈2.4e−5 | 0.275 |
| **60** | **≈7 ⛔붕괴** | ≈2.4e−6 | **0.202** |
| 70 | ≈6 | ≈2.3e−6 | 0.140 |
| 80 | ≈2 | ≈1.5e−6 | 0.086 |
| 90 | ≈1 | ≈8e−7 | 0.039 |

(용량·σ_e 전부 **figure-read ≈**; φ_AM 은 **DERIVED(ours)** — CAM wt% = 99.5 − SE wt%, carbon 0.5 wt%,
ρ = 4.8 / 1.86 / 2.0 g cm⁻³ **ASSUMED**(논문 미제시). 3번째 자리는 ρ 가정에 종속 → **≈ 로만 읽을 것.**)

★★ **두 개의 진짜 발견:**
1. **용량 대 SE 함량은 단봉(dome)이고 최적이 SE ≈ 20 wt%** — "SE 많을수록 이온경로 좋다"가 아니다.
   SE 를 더 넣으면 **절연체 부피가 늘어 전자망이 죽는다.**
2. **σ_e 가 SE 10→60 wt% 에서 ~6 자릿수 붕괴**하고 **용량 붕괴가 σ_e 붕괴와 같은 자리(50→60 wt%)** 에서
   일어난다. **DERIVED φ_AM ≈ 0.28→0.20 구간** = 전형적 3D 구-충전 퍼콜레이션 문턱대.

⚠⚠ **단위 정합 결함 — σ_e 절대값 인용 금지.** 본문 Experimental 은 COMSOL 입력을 "**0.5 % carbon →
1.7 S m⁻¹, 0 % → 0.0017 S m⁻¹**"(stated) 이라 적는다. 1.7 S m⁻¹ = **0.017 S cm⁻¹**. 그런데 Fig 7b 는
가장 가까운 조성(SE 10–20 wt%, carbon 0.5 %)에서 **≈0.17–2 S cm⁻¹** 을 보인다 — **정확히 100× (= cm↔m)
차이**. 둘 중 하나가 단위 오기다(어느 쪽인지 논문으로는 판별 불가). ⇒ **σ_e 의 절대값은 우리 앵커로 쓰지
말 것.** 쓸 수 있는 것은 **(a) 6-decade 하강의 *모양*, (b) 붕괴 φ_AM 위치, (c) 용량-σ_e 동시붕괴** 세 가지뿐.

### 3-6. 반응속도론 지표 (positive vs uniform)

| 지표 | positive | uniform | 출처 / 해석 |
|---|---|---|---|
| CV I_p vs v^½ 기울기 (산화) | **9.46** | **5.34** | stated (기울기 값), **배정은 figure-read** (본문은 "positive 가 더 가파르다"만 말함) |
| 동 (환원) | **−8.13** | **−5.63** | 동일 |
| 겉보기 D 비 (Randles–Ševčík) | **≈3.1× (산화) / ≈2.1× (환원)** | 1 | **DERIVED(ours)**: (9.46/5.34)², (8.13/5.63)² |
| GITT log D (cm² s⁻¹) | ≈−8 대부분 구간, 종단 −10~−11 | 동일 대역, positive 가 약간 위 | figure-read ≈ (Fig 5c) |
| GITT 총 시험시간 | ≈93 h | ≈86 h | figure-read ≈ |
| CV redox 피크 | 3.3 / 3.0 V (Ni²⁺/Ni³⁺↔Ni⁴⁺) | 고속에서 3.0 V 환원피크 감쇠 | stated |
| Nyquist 고주파 절편 | ≈13–16 Ω (3배치 유사) | | figure-read ≈ (Fig 5a inset) |
| 저주파 기울기 | 가장 가파름(=이온수송 저항 최소) | 중간 / reverse 최소 | stated (정성) |

⚠ **D 비 3.1×/2.1× 를 "확산계수 비"로 인용 금지.** Randles–Ševčík 기울기 ∝ **A·C·D^½** 이고,
positive 배치는 분리막쪽에 SE 가 더 많아 **전기화학 활성면적 A 자체가 다르다** ⇒ D 와 A 가 뒤섞인 값이다.
논문도 A 를 분리하지 않았다. (GITT log D ≈ −8 = 1e−8 cm² s⁻¹ 도 층상 NCM 문헌대(1e−10~1e−13)보다 크다
— 기하면적 가정 탓으로 보이며, **절대 D 앵커로 쓰지 말 것.**)

**DRT 시간상수 배정 (stated):**
| τ 대역 | 귀속 |
|---|---|
| 10⁰–10¹ s | 고상확산 + 입자간 반응 |
| 10⁻¹–10⁰ s | **R_ct** (CAM–SE 계면 전하전달) |
| 10⁻⁶–10⁻⁴ s | **R_CEI** (계면 이온수송 저항) |

★ 정직한 서술 하나: **positive 가 10⁰–10¹ s 대역에서는 오히려 저항이 *높다*** — SE-lean(93 % CAM) 층의
국소 단거리 이온수송이 제한되기 때문(stated). 논문은 "전 사이클에서 차지하는 비중이 작다"로 넘어간다.
⇒ **구배는 공짜가 아니라 trade-off** — SE 를 뺀 쪽 층에 국소 페널티가 생긴다. **우리 STEP4 층별 반응분포로
바로 검증 가능한 예측**(§8 P-2).

**ELSCL (electrode-level space-charge layer) — 이 논문의 신조어 (stated):**
uniform 은 분리막쪽 CAM 분율이 positive 보다 높아 **Li⁺ flux 수요가 최대인 자리에 CAM–SE 미세계면이
집중** → Li-poor 영역이 다수 생기고 이것이 **전극 스케일의 SCL** 로 작동, 방전 후반 R_ct 상승.
⚠ 이것은 **가설/명명**이지 측정된 공간전하가 아니다. (참고: 우리 정본 `li2026_sulfide_stability_review_ecer`
는 "SCL 은 유일 원인 아님 — 화학 부산물 축적이 더 직접적" 이라고 경계한다.) **인용 시 "저자 제안 개념" 명시.**

**TOF-SIMS (stated):** 분리막쪽 표면에서 1 사이클 후 채취. Li⁻ = SE + 산화물 전체의 Li 추적,
**LiO₂⁻ = 층상산화물의 Li 전용** 추적자. positive 가 Li⁻·LiO₂⁻ 둘 다 강함. Li⁻ 강함은 그 위치의 SE 분율이
높으니 당연하지만, **CAM 분율이 더 낮은데도 LiO₂⁻ 가 강하다** = 방전 종료 시 CAM 안으로 들어간 Li 가 더
많다 ⇒ **총 CAM 총량을 바꾸지 않고 Li⁺ flux 만 최적화했다**는 저자 주장의 핵심 증거.
(Fig 5m 2D 맵 50 × 50 µm: positive LiO₂⁻ 카운트 ≈40–60 vs uniform ≈30–45, **figure-read ≈**.)

### 3-7. 도전재 공간분포 (Fig 7c,d — 전부 COMSOL, 실험 아님) ★

x축 표기 = (분리막쪽 wt% / 집전체쪽 wt%). 방전시간(s), **figure-read ≈**:

| carbon 분할 | Positive(분리막쪽 집중) | Inverse(집전체쪽 집중) |
|---|---|---|
| 0.00 / 1.00 | **≈0 (완전 실패)** | ≈565 |
| 0.01 / 0.99 | ≈500 | ≈950 |
| **0.05 / 0.95** | ≈1020 | **≈1040 (최대)** |
| 0.5 / 0.5 (uniform) | ≈1035 | ≈1035 |

★★ **세 줄 결론:**
1. **도전재의 최적 구배는 SE 와 *반대* 방향** (집전체쪽 rich) — 전자 flux 가 집전체쪽에서 최대이므로.
   **stated**: "the cathode with conductive agent concentrated near the current collector (reverse
   distribution) exhibited the highest discharge capacity."
2. **그 이득의 크기는 무시할 만하다** — 0.05/0.95 에서 1040 vs 1020 s (**≈2 %**), 0.5/0.5 uniform 과도 ≈0.5 %.
   **stated**: "even limited amounts of conductive agent can fulfill the electronic transport requirements."
3. **극단으로 밀면 양방향 다 붕괴** (0.01/0.99, 0.00/1.00) = 국소 carbon 이 전자망 퍼콜레이션 문턱 밑으로.
   특히 **집전체쪽 carbon 0 → 방전시간 0** (완전 실패) — 집전체 접촉면의 전자 공급이 절대 조건.

⇒ **비대칭성이 핵심**: 이온 구배는 **+10~15 % (실험)**, 전자 구배는 **+2 % (시뮬만)**. 이것이 그들이
논문 제목엔 "electron and ion" 을 둘 다 넣고 실제로 만든 셀은 SE 구배만 쓴 이유다.

### 3-8. 파우치셀 / 에너지밀도

| 항목 | 값 | 출처 |
|---|---|---|
| 소형 파우치 1st 방전 | **201.2 mAh g⁻¹ @ 0.05 C** | stated |
| 동, 0.33 C | **149.2 mAh g⁻¹** | stated |
| 사이클 유지 | **92.9 % @ 50 cyc, 0.33 C** | stated |
| 소형 파우치 전압창 | 1.9–4.3 V vs Li/Li⁺, NCM ǀ LPSC ǀ **Si** | figure-read (Fig 6i 주석) |
| 1st CE (소형) | ≈83 % (충전 ≈240 → 방전 ≈200) | DERIVED from figure-read (Fig 6h) |
| CE 안정화 | ≈100 % @ 8 사이클 이후 | figure-read ≈ (Fig 6i) |
| **대형 파우치** | **5.3 Ah @ 0.05 C · 60 × 80 mm** | stated |
| 대형 파우치 양극 | **85 % / 88 % 이층** (91.5 % 아님!) | stated |
| **에너지밀도** | **404.0 Wh kg⁻¹** | stated |
| Table S2 산출 | C = **5.33 Ah** · V_avg = **3.396 V** · M_cell = **44.8 g** → **404.03** | stated (SI) |

⚠⚠ **404 Wh kg⁻¹ 의 분모 정의 — 반드시 같이 인용할 것.** SI Table S2: *"the total mass of the cathode
and anode sheets, their current collectors, and the electrolyte membranes **except for the
aluminum-laminated pouch film and tabs**"*. 즉 **stack-level**(파우치 외장·탭 제외)이지 **패키지 포함
셀-레벨이 아니다.** ⚠ 본문 Equation (1) 은 분모에 **M_package(알루미늄 라미네이트 필름·집전체·실링)를
포함**한다고 써 있어 **본문과 SI 가 서로 어긋난다.** 제외 질량의 크기를 논문이 정량하지 않으므로
**패키지 포함 실제 값은 404 보다 낮다(폭 미상)**. 인용 시 "404 Wh kg⁻¹ (stack-level, pouch film/tabs 제외)".
또한 **적층수·층당 면적용량 미기재** → 5.33 Ah 를 면적용량으로 역산 불가.

**Fig 1 설계 민감도 (figure-read ≈, Wh kg⁻¹):**
- (b) CAM wt% @ 4 mAh cm⁻²: 30→≈185 · 50→≈272 · 70→≈341 · **80→≈370** · 90→≈398 · 100→≈420
- (c) 면적용량 @ CAM 80 wt%: 1→≈183 · 3→≈332 · **4→≈370** · 5→≈398 · 7→≈432
- (a) 4-인자 막대: 면적용량 1→185 / 3→336 (최대 5) · 가역용량 100→236 / 150→320 (최대 210 mAh g⁻¹) ·
  **활물질분율 50 %→273 / 70 %→349 (최대 87 %)** · 적층수 2→307 / 5→373 (최대 10)
- **stated 결론**: 400 Wh kg⁻¹ 에는 **CAM > 80 wt%** 와 **면적용량 > 4 mAh cm⁻²** 가 동시에 필요.

---

## 4. 방법 ★

### 4-1. 실험 (전부 stated)
- **혼합**: 코인셀 = 아르곤 글로브박스, **막자사발 15 min 수동혼합** (NCM88 + Super P + LPSC; 바인더 없음).
  파우치 = NCM88 + Super P + LPSC + **PTFE** 막자사발 혼합 → **층별 적층 + 롤프레스**(건식전극).
- **셀 조립(코인)**: LPSC 분말 → 다이에 100 MPa 예압(SE층) → 양극 **300 MPa** / Li–In **100 MPa** →
  전체 **200 MPa** consolidation. **이층 양극은 순차 성형**(1층 분말 투입·가압 → 2층 투입·가압).
- **파우치**: dry room(−45 °C 이슬점), 건식 시트, 순차 적층 → **등방압 500 MPa 2 min**, 사이클 중 **30 MPa**.
- **전기화학**: LAND 사이클러, 1.9–3.7 V vs Li–In, 1 C = 4 mA cm⁻².
  GITT 0.1 C(10 min 충전 + 30 min 완화). CV CHI760E, 0.075/0.1/0.125/0.15 mV s⁻¹.
  EIS Bio-Logic SP-300, **7 MHz–0.1 Hz**, 10 mV, OCV. **in-situ EIS** 200 kHz–**0.01 Hz**, ±10 mV,
  40 min 충/방전 + 30 min 휴지 후 측정.
- **σ_e 측정**: **DC 분극** — 양극 분말을 치밀 펠릿으로 성형, **SS ǀ 복합양극 ǀ SS** 대칭셀, 100 mV 정전압,
  정상상태 전류. SI eq (S1) `σ_e = L / (S·R_e)` (SI 원문 `σe=LSRe` 는 분수 서식 손실).
- **구조분석**: XRD Empyrean, λ=1.54051 Å, 10–90°, 0.02°/step, 5 s/step, Kapton 밀봉, Al₂O₃ 내부표준.
  SEM Zeiss Crossbeam 350 @15 kV + Bruker EDS.
  **TOF-SIMS**: Bi₃⁺ 30 keV/45°, 분석 50 × 50 µm (128 × 128 px); Cs⁺ 스퍼터 1 keV/60 nA/45°, 200 × 200 µm;
  음이온 모드, flood gun.

### 4-2. 시뮬레이션 (COMSOL) — stated 전부
- **도구/유형**: COMSOL Multiphysics, **phase-field 시뮬레이션**(본문 표현). 모델 양극 = **4 mAh cm⁻²**,
  NCM88 + LPSC + 도전재. **갈바노스태틱**, 다양한 C-rate.
- **유효 전자전도도**: "**percolation theory 기반 계산**" — **0.5 % carbon → 1.7 S m⁻¹ · 0 % → 0.0017 S m⁻¹**.
  (퍼콜레이션 모형의 형태·문턱·지수는 **미제시**.)
- **기하**: **2-region(상/하) 균질 연속체**. Table S1 이 각 region 의 SE 부피분율만 지정.
- **출력**: 시간–전압 곡선(Fig 4g–i), 방전 후 **Li 농도 분포**(Fig 4j–l), 도전재 구배 방전시간·곡선(Fig 7c,d).

⚠ **미제시 항목이 많다(재현 불가):** 격자/요소수·수렴기준·도메인 두께·초기/경계조건·SE 이온전도도 입력값·
CAM 확산계수·교환전류밀도 i₀·BV 파라미터·활성면적 규약·phase-field 의 order parameter 정의 — **전부 없음**.
Fig 4j–l 컬러바 단위 **"mol cm⁻³, 3.21–3.58 × 10⁴"** 는 물리적으로 불가(≈35,000 mol cm⁻³) —
**mol m⁻³ 의 오기**로 보인다(3.5 × 10⁴ mol m⁻³ ≈ 0.7 × NCM811 c_max ~4.9–5.1 × 10⁴). §F1 규율상 **컬러바
절대값 인용 금지, 상대 대비만.**

### 4-3. ★ 입자 처리 판정 (우리 frame[5] 체크리스트)

| 질문 | 답 |
|---|---|
| DEM 있나 | **없음.** "DEM/discrete element/particle" 단어 0회. |
| 입자를 개별 해상하나 | **아니오.** COMSOL 모델은 **2-region 균질 연속체**(부피분율만). Fig 4a–c 의 구(球) 그림은 **개념 모식도**이지 계산 도메인이 아니다. |
| 접촉 탄소성 (Hertz/Thornton–Ning) | **없음** |
| **진짜 입자 형상 소성** | **없음** |
| 압밀/porosity 시뮬 | **없음** — 300 MPa 성형은 실험에서만 하고 모델은 압밀 후 구조를 가정 |
| 미세구조 → 유효물성 | σ_e 만, 그것도 **미공개 퍼콜레이션 상관식**으로 (구조 해상 없음) |
| 전달 솔버 | 연속체 전기화학(BV 추정) — **접촉망 없음**, Holm 협착 없음 |

⇒ ★★ **frame[5] 5번째 독립 확증.** 2025년 산업체 파일럿 논문이 **4 mAh cm⁻² 두꺼운 graded 양극을
실제로 만들고 5 Ah 파우치까지 갔는데**, 그 설계를 뒷받침한 계산은 **입자 하나도 해상하지 않은
2-region 연속체**다. 즉 **"구조가 왜 그렇게 되는가"(압밀·패킹·접촉망)는 통째로 비어 있다.**
Varkey(구형 DEM·형상소성 없음) → Bazzoun(구형 DEM+RNM) → Duquesnoy(제조 DEM+ML) → Nam(DPE 리뷰/primer)
에 이어, **이 논문은 "설계는 층 단위 조성으로 하되 미세구조는 안 푼다"는 산업 관행을 그대로 보여준다.**
**우리 DEM(패킹·접촉망 σ) + MPM(소성 형상) 가 정확히 그 빈칸이다.**

---

## 5. Figure set ★

| Fig | 무엇을 보여주나 | **우리가 쓸 수 있는 것** |
|---|---|---|
| **1a** | 에너지밀도 4-인자 민감도 막대 (면적용량·가역용량·활물질분율·적층수) | 우리 grade_engine 의 Q_gravimetric 축과 같은 프레임의 **문헌 감도표** |
| **1b,c** | E_grav vs CAM wt%(@4 mAh cm⁻²) / vs 면적용량(@80 wt%) | **400 Wh kg⁻¹ = CAM>80 wt% ∧ 면적용량>4 mAh cm⁻² 이중조건** = ML 설계루프의 목적함수 경계 |
| **2a–c** | 충방전 곡선 × CAM 분율 × 면적용량 3세트 | 과전압 증가의 육안 대조(93 %@4 mAh 에서 ΔV 급증) |
| **2d** | ★ **설계창 막대** (CAM 분율 × 면적용량 → 용량) | **§3-4 표 = 이 카드에서 가장 전이 가능한 데이터.** σ_SE·r_SE 의존 명시 |
| **2e** | A+B 두 조각 이론 vs 실제 모식 | "얇은 전극 2개 ≠ 두꺼운 전극 1개" 논증 — 우리 RVE 두께 외삽 금지 근거 |
| **2f** | ★ **XRD (003) 이동**: 3 mAh 0.78° vs 6 mAh 0.62° | **집전체쪽 미반응의 재료-직접 증거**. 우리 STEP4 SOC(z) 프로파일의 실험 카운터파트 |
| **3a,b** | normal vs optimized 양극 모식 + J₁ = 2j_a+2j_b+j_c, J₂ = j_c | **flux 누적식 = 우리 STEP4 이온전류 보존과 동형**(분리막쪽 = 총전류, 집전체쪽 = 0) |
| **3c** | ★★ **이온 flux(감소) ↔ 전자 flux(증가) 교차 그래프** (실선=이상, 점선=실현) | **이 논문의 개념 심장.** 우리 `viz phi_z`(φ_i 수십 mV 미러 vs φ_e µV 평평)의 **문헌 대응 그림** |
| **3d,e** | 배·짐꾼 카툰 (수송 정체 비유) | 발표용 |
| **4a–c** | positive/uniform/reverse 3구조 (93 %·91.5 %·90 % 층 라벨) | **§3-2 조성표의 그림 근거** — 총량 보존 확인 |
| **4d–f** | 실험 충방전 (204.7 / 186.1 / 178.0) | **헤드라인 stated 수치** |
| **4g–i** | COMSOL 시간–전압 (≈580/540/400 s) | 실험 대비 reverse 페널티 3× 과장 → **정성 인용만** |
| **4j–l** | ★ COMSOL **Li 농도 분포**(방전 후). positive=거의 균일 적색, reverse=집전체쪽 청색 | **우리 STEP3/STEP4 필드맵과 같은 종류의 그림** — 컬러바 단위 오기(§4-2) 주의 |
| **5a** | Nyquist 3배치 (고주파 절편 ≈13–16 Ω 유사, 저주파 기울기 positive 최급) | 이온수송 저항 서열의 EIS 근거 |
| **5b** | ★ **rate 0.1→1 C** | **격차가 rate 와 함께 확대(+5 %→+25 %)** = 수송 기원 증명 |
| **5c** | GITT log D vs 시간 | ⚠ 절대 D(1e−8 cm² s⁻¹) 인용 금지, 비교만 |
| **5d** | ★ CV I_p ∝ v^½ 기울기 9.46/5.34, −8.13/−5.63 | D 와 A 가 뒤섞인 값 — **"수송 개선"의 정성 근거로만** |
| **5e–h** | in-situ Nyquist 3D 적층 (충전/방전 × positive/uniform) | 우리 EIS 트랙(`eis_drt_ica.py`)의 데이터 형식 참고 |
| **5i–l** | ★ **3D-DRT 등고선** γ(τ) vs τ vs 전압 (R_CEI·R_ct 라벨) | **우리 v3-1 DRT 구현의 문헌 판독 예시.** positive 가 10⁰–10¹ s 에서 오히려 높다(구배의 대가) |
| **5m–o** | TOF-SIMS LiO₂⁻ 2D 맵 + 3D 렌더 | **총 CAM 불변 상태에서 Li 삽입량 증가**의 직접 증거 |
| **6a–c** | 건식 롤프레스 개념도 + 실물 사진 | Phase-5 층상 제조의 **현실 공정 경로** |
| **6d,e** | 단면 SEM: 두 층 사이 **뚜렷한 계면 없음** + **PTFE fibril**(2 µm 스케일) | ★ **PTFE 피브릴 실사** = 우리 F1 PTFE-브릿지 훅의 형태 근거; "층 계면이 물리적 경계가 아니다"는 우리 Phase-5 층간 처리에 직결 |
| **6f** | EDS Ni/P/S/Cl 매핑 (S·P·Cl 이 분리막쪽 농후) | 구배가 실재함을 원소로 확인 |
| **6g** | ★ **4층 graded 양극 단면 SEM** (30 µm 스케일바, Cathode 1–4) | **4층 = 우리 Phase-5 목표 그 자체.** ⚠ 스케일바 기준 촬영 컬럼 ≈60 µm 로 4 mAh cm⁻² 전극치고 얇다 → **부분 시야일 가능성, 두께 인용 금지** |
| **6h,i** | 소형 파우치 곡선 + 50 사이클 92.9 % | 유일한 사이클 데이터 |
| **6j–l** | 5 Ah 파우치 구조·실물·곡선(404 Wh kg⁻¹) | ★ 분모 정의 주의(§3-8) |
| **7a** | ★★ **용량 vs SE 10–90 wt% (SE 20 wt% 최적 단봉)** | **"SE 많을수록 좋다"의 반증** — 우리 σ_e/σ_ion trade-off 서사의 실험판 |
| **7b** | ★★ **σ_e vs SE wt% (6-decade 붕괴)** | **φ_AM 퍼콜레이션 문턱의 외부 증거** — ⚠ 절대값 단위 결함(§3-5) |
| **7c,d** | COMSOL 도전재 구배 (Positive vs Inverse × 4 분할) | **도전재 최적은 SE 와 반대 방향이되 이득 ≈2 %** — 우리 `--cb-grad` 의 방향 답 |
| **S2** | 원료 SEM (NCM88 3–5 / LPSC 1–2 µm / SuperP 60–80 nm) | **우리 DEM 입력 r_AM·r_SE 와 직접 대조**(§7-D) |
| **S9** | 이중 구배(SE+carbon) rate 성능 — 85:14.5:0.5 ǀ 88:11:1 | **논문 제목을 실제로 구현한 유일 조성** — 수치는 SI 그림에만(**우리 미보유 → n/a**) |
| **S10** | DC 분극 원시 전류–시간 | σ_e 추출 절차 |
| **S1,S3–S8** | 이론용량 막대·사이클(0.3 C)·80 % 평균 3배치·CV·건식전극 사진/두께·4층 EDS·SE 함량별 곡선 | **S6b = 전극 두께 그림 → 우리 미보유(두께 n/a 의 원인)** |

---

## 6. Post-processing ★

| 무엇 | 어떻게 | 우리 대응 |
|---|---|---|
| **에너지밀도 산정** | Eq (1) 총에너지/총질량 (분모에 M_package 포함이라 *본문*은 서술) · SI Eq (S2) `E = C·V_avg·1000/M_cell` (파우치필름·탭 **제외**) | 우리 grade_engine Q_gravimetric — **분모 규약 명시가 인용의 전제** |
| **flux 분해** | Eq (2)(3): `J₁ = 2j_a + 2j_b + j_c`, `J₂ = j_c` — 깊이별 누적 Li⁺ flux | 우리 STEP4 이온전류 보존과 동형 |
| **σ_e 추출** | DC 분극 정상상태 → `σ_e = L/(S·R_e)` (초기 이온성 감쇠 후 잔류전류 = 전자성) | 우리 σ_e 는 **Kirchhoff 망 해**(측정 아님) → 방법 자체가 다름, 절대비교 금지 |
| **σ_e 모델화** | "percolation theory" (모형 미공개) → COMSOL 입력 2점 (0.5 %/0 % carbon) | 우리 σ_e Stage 22.5 (φ_AM⁴·√A·Trevisanello endpoints) — **우리 쪽이 훨씬 명시적** |
| **XRD 정량** | Al₂O₃ 내부표준 보정, (003) 피크 Δ2θ + broadening = 탈리튬화 깊이·무질서 | 우리 미보유 (구조분석 실험축) |
| **EIS → DRT** | in-situ Nyquist → **DRT γ(τ)** 3D 등고선(전압축) → τ 대역별 R_CEI/R_ct/확산 배정 | ★ 우리 **v3-1 `eis_drt_ica.py`**(Tikhonov DRT)의 판독 레퍼런스. 단 **정량 R 값은 논문이 표로 안 준다** |
| **CV 운동학** | I_p vs v^½ 선형회귀 기울기 비교 (Randles–Ševčík 확산지배 확인) | ⚠ A·C·D 혼재 (§3-6) |
| **GITT** | 10 min 펄스 + 30 min 완화 → log D vs 시간 | 우리 미보유 |
| **TOF-SIMS** | Li⁻(전체 Li) vs **LiO₂⁻(층상산화물 Li 전용)** 2-추적자 대비, 2D 맵 + 3D 렌더 | ★ **"CAM 안의 Li"만 보는 추적자 선택**이 방법론적 핵심 — 우리 SOC(z) 검증의 실험 짝 |
| **SEM/EDS** | 단면 + Ni/P/S/Cl 매핑으로 구배 확인 | 우리 2D synth 의 검증 대상 형식 |

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (동결본) / `comparison_vs_ours_DEM.md`

### A. 압밀 / porosity

| 항목 | Luan 2025 | 우리 | 판정 |
|---|---|---|---|
| **양극 성형압** | **300 MPa** (코인) | **300 MPa** | ★ **완전 일치** — 우리 압밀 조건이 산업 파일럿과 같은 자리 |
| 셀 consolidation | 200 MPa | — | 우리 모델에 없는 2차 가압 단계 |
| 파우치 등방압 | **500 MPa 2 min** | 우리는 **단축 다이 압축**만 | ⚠ **isostatic ≠ uniaxial** — 응력상태가 달라 porosity·이방 tortuosity 전이 금지 |
| 사이클 스택압 | **30 MPa** | 우리 작동압 축 없음 | Doux 5 / Minnmann 40 / **Luan 30** — 작동압 밴드에 3번째 값 추가 |
| **porosity** | **미보고** | real_14 **15.6 %**(DEM) / 15.93 %(MPM) | ⛔ **A축 정량대조 불가** — 이 논문 최대 결손 |
| 전극 밀도·두께 | 미보고(SI Fig S6b 에만) | 30.28 µm (real_14) | ⛔ 동일 |
| Heckel / 다압력 | 없음 | P_y 138 MPa, R² 0.965 | 우리 고유 |

⇒ **A축에서 이 논문은 앵커를 주지 않는다.** 줄 수 있었는데(밀도·두께·porosity 모두 측정했을 것) 안 실었다.
우리 15.6 % 를 검증할 기회를 놓친 것 — **위시리스트: 저자 SI Fig S6b 확보 시 두께 대조 가능.**

### B. 전달 삼중항

| 항목 | Luan 2025 | 우리 | 판정 |
|---|---|---|---|
| **LPSC bulk σ_ion** | **2 ± 0.1 mS cm⁻¹** (stated) | σ_grain 3.0 (Cronau 단결정) × Cronau(r_SE) | ★ **펠릿급 4번째 앵커**: Bazzoun 1.02 · Minnmann 1.6 · Kim2025 1.6 · **Luan 2.0** → 펠릿 밴드 **1.0–2.0**, 단결정 3.0 아래 = GB 포함 일관 ✓ |
| **복합 σ_ion** | **측정 안 함** | 0.108–0.127 (real_9 계열) | ⛔ B축 이온 절대앵커 없음 (Bazzoun/Minnmann 이 여전히 유일) |
| **복합 σ_e** | DC 분극 9점 (SE 10–90 wt%) | Kirchhoff 망 (Stage 22.5, LOOCV 0.953) | ⚠ **절대값 단위 결함(100× cm↔m)** → **추세만** |
| σ_e 모델 입력 | 0.5 % carbon **1.7 S m⁻¹** = 17 mS cm⁻¹ / 0 % **0.0017 S m⁻¹** = 0.017 mS cm⁻¹ | 우리 σ_e ≈ **1.0–3.0 mS cm⁻¹** (real_9 Stage-E 1.056–1.087; SDCP SBE 1.979 / DBE 3.002) | ★ **우리 값이 그들 두 입력 사이에 낀다**(0.017 < **1–3** < 17) — 자릿수 정합, 절대 일치 주장 금지 |
| **σ_e 퍼콜레이션 문턱** | 용량·σ_e 동시붕괴 @ **φ_AM(solid) ≈ 0.28→0.20** (DERIVED) | 우리 폼은 **φ_AM⁴ 만, 문턱항 없음** | ★★ **모델 경계 발견**: 우리 corpus 는 φ_AM(solid) **0.37–0.88**(AM 60–95 wt%) 로 **전부 문턱 위** → 폼은 유효하되 **φ_AM < 0.3 외삽 금지** 를 명문화해야 함 |
| σ_thermal | 없음 | 보유 (Ridge, LOOCV 0.903) | 우리 고유 |
| **전자 vs 이온 병목 비대칭** | 이온 구배 **+10–15 %**(실험) vs 전자 구배 **+2 %**(시뮬) | STEP4 2C 옴강하 **전자 0.01–0.03 mV vs 이온 84–90 mV** (≈3000–9000×) | ★★★ **frame[4] 교차검증** — 완전히 다른 두 방법(실험/COMSOL vs 우리 Kirchhoff+STEP4)이 **같은 결론**. §8 P-1 |

### C. 역학 / morphology

| 항목 | Luan 2025 | 우리 | 판정 |
|---|---|---|---|
| 입자 형상 소성 | **없음** (연속체) | **MPM J2** 진짜 형상변화 | 우리 고유 (frame[5] 5번째 확증) |
| 접촉망 | **없음** | DEM 접촉 + Holm 협착 | 우리 고유 |
| **PTFE fibril** | **SEM 실사** (Fig 6e, 2 µm 스케일; "CAM 입자를 고정") | 우리 PTFE = **절연 배선만, 기계 기여 0** (F1) | ★ **형태 근거 확보**. 단 **fibril 직경·밀도·강성 수치 없음** → 여전히 훅만, §F1 유지 |
| 층 계면 | 단면 SEM 상 **뚜렷한 계면 없음** (롤프레스가 지움) | Phase-5 는 층간 처리 미정 | ★ **설계 지침**: 우리 층상 합성에서 **날카로운 층 경계를 만들면 비물리적** — smooth interface 필요 |
| 균열 / 파괴 | 없음 | Auerbach fracture 보유 | 우리 고유 |
| CAM 응력·팽창 | 없음 (XRD broadening 정성 언급만) | MPM 응력장 + A10 사이클 | 우리 고유 |

### D. 패킹 / Furnas dip

| 항목 | Luan 2025 | 우리 | 판정 |
|---|---|---|---|
| AM 입경 | **3–5 µm 단봉** | **bimodal** AM_P/AM_S (12:4:1 = AM_P:AM_S:SE) | ⚠ **단봉 vs bimodal** — dip 위치·깊이가 다를 것 |
| SE 입경 | **1–2 µm** | r_SE 0.5–1.5 µm (production ⌀1.0) | ★ **거의 동일** (그들 ⌀1–2 vs 우리 ⌀1.0) |
| **크기비 AM:SE** | ≈ **4 : 1.5 ≈ 2.7 : 1** (D50 추정) | mono 케이스 4:1 ~ 8:1, bimodal 12:4:1 | ★ **우리 mono-AM_S 케이스(4:1)와 가장 가까움** |
| Furnas dip | **측정 없음**(porosity 미보고) | AM 70–85 wt% dip (DEM·de Larrard) | ⛔ 대조 불가 |
| **CAM wt% 범위** | **80–95 wt%** | corpus AM **60–95 wt%** | ★ 그들 전 범위가 우리 corpus 안 — **우리가 그들 설계창을 커버한다** |
| Fan2026 §3.5 입경 설계창 | LPSC **1–2 µm** = 협동변형(<3 µm 파쇄임계 아래) | 우리 production ⌀1.0 = 이온·기계 동시 최적점 | ★ **Luan 의 상용 LPSC 도 같은 창 안** — 우리 r_SE 선택의 4번째 사후 정당화 |

### E. 우리가 문헌을 검증/교차검증하는 지점 (★ 강점)

1. ★★★ **"전자망은 조금이면 충분, 병목은 이온" — 우리가 정량으로 먼저 갖고 있었다.**
   Luan 은 이것을 **정성**으로 말한다("even limited amounts of conductive agent can fulfill the electronic
   transport requirements", 시뮬 이득 ≈2 %). 우리 STEP4 운전-φ(z) export 는 **2C 에서 전자 옴강하
   0.01–0.03 mV vs 이온 84–90 mV** 라는 **숫자**를 준다. ⇒ 우리가 그들 결론의 **정량 근거를 제공**한다.
   (⚠ 조건부: 이는 **CAM-rich 영역** 한정. 그들 Fig 7a/b 가 SE ≥ 50 wt% 에서 전자가 율속으로 **역전**됨을
   보였고, 우리 corpus 는 그 영역에 없다 — 서로의 유효범위를 정확히 보완.)
2. ★ **총량 보존 게이트의 정당성.** 우리 `--poro-grad` 가 총 porosity 를 고정하고 프로파일만 움직이는
   설계는 **Luan 의 실험/시뮬이 둘 다 총량 보존으로 대조군을 짠 것**과 같은 규율 = 방법론적 승인.
3. ★ **σ_grain 이중계상 점검 재확인**: Luan 의 LPSC 펠릿 2.0 mS/cm 가 Cronau 단결정 3.0 아래 →
   "펠릿 < 단결정" 서열이 4번째 독립 확인.

### F. 우리가 못 하는 것 (정직 목록)

| 그들이 갖고 우리가 없는 것 | 비고 |
|---|---|
| **실제 사이클 데이터** (50 cyc 92.9 %) | 우리 A10 은 접촉-원장 후처리(assumed-form) 수준 |
| **5 Ah 파우치 · 스케일업** | 우리는 µm RVE — 셀-레벨 검증 없음 |
| **건식 롤프레스 + 층별 적층 실공정** | 우리 압밀은 단축 다이만 |
| **TOF-SIMS Li 공간분포 / XRD 깊이별 탈리튬화** | 우리 STEP4 SOC(z) 의 실험 검증 수단 부재 |
| **GITT·CV·DRT 로 분해한 반응속도론** | 우리 z₁(이온수송) 레일만 (Kim2025 카드와 같은 결손) |
| **Si 음극 풀셀** | 우리는 양극 전용 |
| **404 Wh kg⁻¹ 급 셀 설계 파라미터 세트** | 다만 stack-level 정의 주의 |

역으로 **우리가 갖고 그들이 없는 것**: porosity·두께·접촉망 σ 삼중항·Holm 협착·퍼콜레이션/배위수/coverage·
tortuosity·Furnas dip·소성 형상변화·응력·균열·Heckel — **즉 미세구조 전체.**

---

## 8. 적용 인사이트 — 실행 가능한 P-항목

### P-1 (즉시·무비용) — **STEP4 φ(z) 결과를 이 논문에 앵커한다**
우리 `viz phi_z`(φ_e µV-평평 / φ_i 수십 mV 미러, 2C 옴강하 전자 0.01–0.03 vs 이온 84–90 mV)는
**Luan Fig 3c(이온 flux 감소 ↔ 전자 flux 증가 교차)의 정량 실현**이다. 발표·원고에서
"우리 STEP4 가 문헌의 정성 주장을 숫자로 확인" 이라는 문장을 **이 논문을 근거로** 쓸 수 있다.
⚠ 단서: 우리 φ 는 **@1V 수송프로브 아니라 @1C 운전 프레임** 값이어야 비교가 성립(CLAUDE.md 필드 라벨링 규약).

### P-2 (핵심·중간비용) — **`--se-grad` 신설: 우리 A7 은 잘못된 물리량을 구배하고 있다** ★★
현행 `extract_2d_microstructure.py --poro-grad` 는 **porosity(z)** 를 구배한다(#286 Yoo, 흑연/액체계).
**Luan 이 구배하는 것은 조성 φ_SE(z) 이지 porosity 가 아니다.** 두 노브는 다른 물리다:
- porosity 구배 = **어디에 공극이 있나** (Yoo, 급속충전 액체계)
- **SE 구배 = 어디에 이온 도체가 있나** (Luan, ASSB — 우리 소재계)

⇒ **제안**: `--se-grad [−1..1]`(>0 = 분리막쪽 SE-rich = Luan positive)을 `--poro-grad` 와 **같은 규약**
(총 SE 고정, K=8 밴드 리포트, 마지막 pass UNGATED 폴백)으로 추가. 검증 케이스는 논문이 다 지정해준다:

| 런 | φ_SE(집전체측 / 분리막측) | 근거 |
|---|---|---|
| exp-Ⅰ positive | **0.140 / 0.201** | 실험 93:6:1 / 90:9:1 (DERIVED vol%) |
| exp-Ⅱ uniform | 0.171 / 0.171 | 91.5:7.5:1 |
| exp-Ⅲ reverse | 0.201 / 0.140 | — |
| sim-Ⅰ/Ⅱ/Ⅲ | **0.1875/0.3125 · 0.25/0.25 · 0.3125/0.1875** | **Table S1 그대로** |

그 다음 **STEP3 로 밴드별 σ_ion·σ_e·τ**, **STEP4 로 반응분포·용량**을 뽑아 **순서 positive > uniform >
reverse** 가 재현되는지 본다. 재현되면 = 우리 STEP3→STEP4 체인의 **외부 앵커 통과**(방향+순서만 요구,
절대값 요구 안 함 → 안전). 안 되면 = 정량화된 모델 한계(frame[4]).
★ 추가 예측(반증 가능): **Luan DRT 는 positive 가 10⁰–10¹ s 대역에서 오히려 저항이 높다**고 했다 —
우리 STEP4 층별 반응분포도 **SE-lean 층(93 % CAM)에서 국소 과전압 증가**를 보여야 한다. 안 보이면
우리 모델이 층내 국소 이온부족을 못 잡는 것.

### P-3 — **RVE 두께가 부족하다: 구배 효과는 4 mAh cm⁻² 에서만 큰 신호다** ★
Luan Fig 2d: **1 mAh cm⁻² 에선 CAM 95 % 도 문제없고, 4 mAh cm⁻² 에서만 90 % 가 천장.**
우리 real_14 는 **30.3 µm** — DERIVED(ours, ρ_electrode 3.2–3.4 g cm⁻³ **ASSUMED**, 200 mAh g⁻¹)로
**≈1.6–2 mAh cm⁻²** 에 해당한다. 즉 **우리 production RVE 는 구배 효과가 거의 안 나타나는 두께대**다.
⇒ Phase-5 층상 케이스는 **두께 ~2–2.5× (≈65–70 µm, 4 mAh cm⁻²)** 로 키워야 신호가 나온다.
⚠ 두께 2.5× = MPM 격자 부담 급증 + `d_h/dx ≳ 3.5` 규칙 재점검 필요(CLAUDE.md 2026-08-06/07).
⚠ 이 두께 환산은 **논문 값이 아니라 우리 가정** — 논문은 두께를 안 준다.

### P-4 — **`--cb-grad` 의 방향 답이 나왔다 (단, 크기는 무시할 만함)**
A7 규약은 "carbon:binder optimum 은 재료의존(#286 gradient vs #20 uniform) → 둘 다 노출, 여기서 안 고름"
이었다. **황화물 ASSB 축에 대해 Luan 이 답을 준다: 도전재는 집전체-rich(= SE 와 반대), 이득 ≈2 %.**
⇒ A7 문서에 **"sulfide-ASSB 도전재 축 = reverse(집전체 rich) 방향, 크기 2 % (Luan 2025 COMSOL)"** 를
기록. ⚠ 우리 `--cb-grad` 는 **carbon:binder 비**이고 Luan 은 **carbon:총량** — 매핑 시 바인더 축 분리 필요.
⚠ 그리고 이 2 % 는 **시뮬만**이다(실험 대조군 없음) → **설계 기본값 변경 근거로는 약함**, 문서화까지만.

### P-5 — **설계창 표를 ML 설계 폐루프의 제약으로 넣는다**
§3-4 (CAM 분율 × 면적용량 → 명목용량 도달 여부) + Fig 1b,c(400 Wh kg⁻¹ = CAM>80 wt% ∧ >4 mAh cm⁻²)
= `scripts/ml_design_loop.py` 의 **실행 가능 영역(feasible region) 외부 제약**. 우리 예측기가
"CAM 95 % @ 4 mAh cm⁻²" 같은 점을 최적으로 뱉으면 **문헌이 이미 기각한 설계**임을 게이트할 수 있다.
⚠ 이 창은 **σ_SE = 2 mS/cm, r_SE = 1–2 µm** 조건부 — 다른 SE 로 옮기면 창이 움직인다(논문 자신이 명시).

### P-6 — **Phase-5 층 계면 처리 지침**
Fig 6d/e: 롤프레스 후 **두 층 사이에 뚜렷한 계면이 없다**(PTFE fibril 이 가로질러 고정). ⇒ 우리 Phase-5
z-stacking 에서 **날카로운 조성 계단을 만들면 비물리적** — smooth interface(또는 몇 µm 혼합대)가 맞다.
(현행 2D synth 는 z-band 를 이미 지원하나 계면 폭 규약이 없다 → 추가 필요.)

### P-7 — **σ_e 폼의 유효범위를 문서에 못 박는다**
Luan Fig 7a/b 가 **φ_AM(solid) ≈ 0.28 → 0.20 에서 σ_e·용량 동시 붕괴**를 보인다.
우리 Stage 22.5 σ_e 폼에는 **퍼콜레이션 문턱항이 없다**(φ_AM⁴ 만). corpus 는 φ_AM 0.37–0.88 로 전부
문턱 위라 폼은 안전하지만, **"φ_AM(of solid) < 0.3 에서는 폼을 쓰지 말 것"** 을 `our_dem_baseline.md §4`
와 σ_e 문서에 명시. ⚠ 문턱값 0.2–0.28 은 **DERIVED(ours)** — 그들 wt% 를 우리 ρ 가정으로 환산한 값.

---

## 9. 인용 가능 문장 (deck/paper 용)

- "Luan et al. (Adv. Funct. Mater. 2026, 36, e26239) demonstrated that, **at fixed total CAM, SE and
  carbon content**, redistributing the solid electrolyte so that its local fraction increases toward
  the separator raises the discharge capacity of a 4 mAh cm⁻² NCM88/Li₆PS₅Cl cathode from
  **186.1 mAh g⁻¹ (uniform) and 178.0 (reverse) to 204.7 mAh g⁻¹ (positive gradient)** at 0.1 C,
  and that the advantage grows with rate."
- "The same work reports that the conductive-agent gradient must run **opposite** to the SE gradient
  (carbon-rich at the current collector) but that its benefit saturates above ~0.05 wt% locally —
  i.e. **the electronic network is cheap and the ionic network is the bottleneck** in CAM-rich
  sulfide cathodes. Our STEP4 operating-potential export quantifies exactly this asymmetry:
  at 2 C the ohmic drop is **0.01–0.03 mV on the electronic rail versus 84–90 mV on the ionic rail**."
- "Empirically, the maximum tolerable CAM fraction falls with areal loading —
  **95 wt% at 1 mAh cm⁻², 93 wt% at 2, and ≤90 wt% at 4 mAh cm⁻²** — with the threshold explicitly
  set by the SE's ionic conductivity (2 ± 0.1 mS cm⁻¹) and particle size (1–2 µm) (Luan 2025)."
- "A 4-layer graded cathode fabricated by a dry roll-pressing route showed **no distinguishable
  interface between layers**, the CAM particles being immobilized by PTFE fibrils — indicating that
  a layered composite cathode should be modelled with a **graded, not stepped, composition profile**."
- ⚠ **인용 금지**: Fig 7b 의 σ_e 절대값 · Fig 4j–l 컬러바 절대 농도 · GITT D 절대값 · CV 기울기비의
  "확산계수 비" 해석 · **"404 Wh kg⁻¹ full-cell"**(반드시 "stack-level, pouch film/tabs 제외" 병기).

---

## 10. 주의 / 한계 (over-claim 방지)

1. **미세구조 시뮬이 없다.** COMSOL 은 **2-region 균질 연속체** — 입자·접촉·공극이 없다. Fig 4a–c 의
   구 그림은 **모식도**다. ⇒ 이 논문을 "시뮬 논문"으로 소개하지 말 것. frame[5] 5번째 확증.
2. **시뮬 조성 ≠ 실험 조성.** COMSOL φ_SE 평균 0.25·대비 0.125 vs 실험 DERIVED 0.171·0.061
   (평균 1.5×, 대비 2.0×). 그래서 시뮬의 reverse 페널티(+45 %)가 실험(+15 %)의 3배다. **정성만.**
3. **σ_e 절대값 단위 결함 100×.** 본문 COMSOL 입력 1.7 S m⁻¹ ↔ Fig 7b ≈2 S cm⁻¹ (같은 조성대).
   어느 쪽이 옳은지 논문으로 판별 불가 ⇒ **모양·문턱만 사용**.
4. **404 Wh kg⁻¹ 는 stack-level.** SI Table S2 가 알루미늄 라미네이트 파우치필름·탭을 명시적으로 제외
   (본문 Eq (1) 은 M_package 포함이라고 써서 **본문↔SI 불일치**). 패키지 포함 값은 더 낮고, 논문은
   그 폭을 정량하지 않는다. 또 **적층수·층당 면적용량 미기재** → 5.33 Ah 역산 불가.
5. **porosity·밀도·두께 전무.** A축(압밀) 정량대조 불가. 우리 15.6 % 를 검증할 기회 상실.
6. **대형 파우치는 91.5 % 설계가 아니다** — 85 %/88 % 이층. 즉 **404 Wh kg⁻¹ 셀과 §3-3 의 구배 실험은
   서로 다른 조성**이다. "91.5 % 구배로 404 달성" 은 **오독**.
7. **Fig 5b 의 0.1 C 값(218/211/208)이 Fig 4d–f stated(204.7/186.1/178.0)와 불일치** — 다른 시험으로
   보이나 논문이 설명 안 함. **stated 값 우선.**
8. **CV·GITT 는 D 와 활성면적 A 가 뒤섞임.** positive 는 설계상 분리막쪽 SE-CAM 계면이 더 많아
   A 가 다르다. "확산이 3× 빠르다"는 주장은 논문에도, 우리 인용에도 넣지 말 것.
9. **ELSCL 은 저자 제안 개념**이지 측정된 공간전하가 아니다. 우리 정본 리뷰(li2026 ECER)가 "SCL 은 유일
   원인 아님, 부산물 축적이 더 직접적"이라 경계한 것과 함께 읽을 것.
10. **도전재 구배 결론은 시뮬 전용.** 실험 대조군(도전재 구배 3배치)이 없다. SI Fig S9 의 이중구배
    조성(85:14.5:0.5 ǀ 88:11:1)만 실험이 있으나 **수치는 SI 그림에만 있고 우리는 SI PDF 미보유 → n/a**.
11. **소재 차이 미소하지만 존재**: NCM88(Ni 0.88) vs 우리 NMC811(Ni 0.80). 용량·팽창·계면반응성이 다르다
    (참고: `kang2025_toughened_bimodal_nca_lzo` 는 Ni 0.88 NCA). **σ·용량 절대값 전이 시 주의.**
12. **가압 방식 차이**: 파우치는 **등방압 500 MPa**, 우리는 **단축 300 MPa**. 응력상태가 달라
    porosity·이방 tortuosity·접촉면적 전이 금지.
13. **SI 그림 실물 미보유** (캡션 텍스트만). Fig S3–S10 의 수치는 전부 **n/a**로 두었다.

---

## 11. 기법 미니 사전 (이 논문 읽기용)

- **Positive / uniform / reverse distribution**: 저자 명명. **positive = 분리막(SE층) 쪽으로 갈수록
  SE 분율↑ (CAM 분율↓)**. reverse 는 그 반대. 우리 `--poro-grad` 부호 규약(>0 = 상단/분리막쪽)과
  방향이 같아 그대로 매핑된다.
- **Li⁺ / e⁻ transport flux**: 두께 z 에서 그 단면을 통과하는 전류. 이온은 분리막쪽에서 **총 전류**이고
  집전체쪽에서 **0**, 전자는 정확히 반대. Eq (2)(3) 이 이 누적을 쓴 것.
- **DRT (Distribution of Relaxation Times)**: Nyquist 를 τ 축의 분포 γ(τ) 로 역변환해 겹친 반원을 분리.
  본 논문 배정 = 10⁻⁶–10⁻⁴ s: R_CEI / 10⁻¹–10⁰ s: R_ct / 10⁰–10¹ s: 고상확산+입자간.
  (우리 v3-1 `eis_drt_ica.py` 가 Tikhonov DRT 로 같은 분해를 한다.)
- **ELSCL (electrode-level space-charge layer)**: 저자 신조어. 통상 SCL 은 CAM/SE **미세계면**의 nm 스케일
  Li-poor 층인데, 이온 flux 가 부족한 쪽에 그런 미세계면이 몰리면 **전극 스케일**의 Li-poor 영역이
  생긴다는 주장. **측정된 전위분포가 아니라 해석**이다.
- **TOF-SIMS Li⁻ vs LiO₂⁻**: Li⁻ 는 SE 와 산화물 양쪽의 Li 를 다 잡지만 **LiO₂⁻ 는 층상산화물 쪽 Li 만**
  따라간다. 그래서 "CAM 안에 Li 가 실제로 얼마나 들어갔나"를 보려면 LiO₂⁻ 를 본다.
- **Randles–Ševčík**: 확산지배 CV 에서 I_p ∝ n^{3/2} A C D^{1/2} v^{1/2}. **기울기 비교는 D 뿐 아니라
  A·C 도 같이 담는다** — 이 논문 §3-6 caveat 의 근거.
- **DC 분극 σ_e**: 이온 차단 전극(SS) 사이에 정전압을 걸면 초기엔 이온+전자가 흐르다 이온이 분극돼
  멈추고 **정상상태 전류 = 전자성**만 남는다. 그 저항으로 σ_e 산출.
- **건식전극 PTFE fibrillation**: 전단으로 PTFE 를 실(fibril)로 늘려 입자를 그물처럼 묶는 것.
  Fig 6e 가 2 µm 스케일에서 그 실을 보여준다. 우리 F1 PTFE 브릿지 훅의 형태 근거.
- **Isostatic pressing**: 유체압으로 전 방향 동일 압력. 단축 다이 압축과 응력상태(편차응력)가 달라
  **같은 MPa 라도 같은 압밀이 아니다**.

---

## Supplementary Information (사용자 .docx 추출 텍스트 기준, 2026-08-11)

**보유 = 캡션·표 텍스트만** (SI PDF/그림 실물 미보유). 확보된 정량 정보:
- **Fig S2**: NCM88 **3–5 µm** · LPSC **1–2 µm** · Super P **60–80 nm** (입경의 유일 출처).
- **Fig S9**: 이중 구배 조성 **85:14.5:0.5(SE층쪽) / 88:11:1(집전체쪽)**, 4 mAh cm⁻², 25 °C,
  0.1/0.3/0.5/1 C. **성능 수치 n/a**(그림에만).
- **Fig S10 + eq (S1)**: `σ_e = L/(S·R_e)`, DC 분극 정상상태.
- **Table S1**: COMSOL SE 부피분율 Ⅰ 0.1875/0.3125 · Ⅱ 0.25/0.25 · Ⅲ 0.3125/0.1875 (**총량 보존**).
- **Table S2 + eq (S2)**: `E = C·V_avg·1000 / M_cell`; C **5.33 Ah**, V_avg **3.396 V**,
  M_cell **44.8 g** → **404.03 Wh kg⁻¹**; 분모 = 양극·음극 시트 + 각 집전체 + SE 막
  (**알루미늄 라미네이트 필름·탭 제외**).
- 그 외 S1(이론용량 막대), S3(0.3 C 사이클), S4(평균 CAM 80 % 3배치 첫사이클),
  S5(CV 스캔속도별), S6(건식전극 사진 + **단면 두께** ← 우리 두께 결손의 열쇠), S7(4층 EDS),
  S8(SE 함량별 첫사이클) — **전부 그림, 수치 n/a**.

★ **위시리스트**: SI PDF 원본 확보 시 (a) **Fig S6b 전극 두께** → A축 두께 대조 성립,
(b) **Fig S9 이중구배 rate 곡선** → 우리 P-2 의 이중구배 검증 타깃 확보.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

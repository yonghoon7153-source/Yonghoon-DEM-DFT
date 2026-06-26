# Minnmann 2021 JES — 복합 양극 전하수송 병목 정량화 (EIS-TLM) ★ 우리 porosity/σ_ion/τ_ion 앵커의 진짜 출처

> slug `minnmann2021_jes_charge_transport_bottlenecks` · DOI `10.1149/1945-7111/abf8d7`
> · type `experiment (EIS-TLM + cell cycling)` · 저널 `J. Electrochem. Soc. 168 (2021) 040537`
> · PDF `ec8f708f-04._Minnmann_2021_J._Electrochem._Soc._168_040537.pdf`
> · digested `2026-06-26` · status ✅
>
> ★★ **이 논문이 우리 "Minnmann porosity ~14 % / 13–17 %", "σ_ion_eff 0.17 mS/cm", "τ_ion 2.07 @ 42 vol% CAM"
> 앵커의 진짜 출처다.** 그동안 Minnmann *2022* AEM Perspective(설계 리뷰, 정량 데이터 0개)로 잘못 인용돼
> 왔으나, 2022 리뷰 digest가 그게 거기 없음을 증명했고 → 실제 1차 측정값은 **여기(2021 JES)** 에 있다.
> 우리 소재계(NCM-622 + LPSCl)의 EIS-TLM 1차 측정 = Bazzoun/Lee와 더불어 우리가 가진 **최강 실험 앵커**.

---

## §0. ★ ANCHOR-PROVENANCE 확정 (이 절이 이 digest의 존재 이유)

CLAUDE.md / our_dem_baseline.md / comparison_vs_ours.md 가 "Minnmann ~14 %", "σ_ion_eff 0.17 mS/cm",
"τ_ion 2.07 @ 42 vol% CAM" 로 인용해 온 세 앵커를 **PDF에서 직접 확인**했다. 결론:

| 앵커 | 우리가 써온 값 | 이 논문(2021 JES)서 확인된 값 | 정확한 조건 | stated/계산 |
|---|---|---|---|---|
| **복합 양극 porosity** | ~14 % (13–17 %) | **avg 14 %** (가정값) · **13–17 %** (실측 range) | **dry mixing + 단축 380 MPa** 압밀, Table SIII | ✅ 둘 다 stated |
| **σ_ion_eff @ ~42 vol% CAM** | 0.17 mS/cm | **0.17 mS/cm** (= 1.7×10⁻⁴ S/cm) | **42 vol% NCM-622**, EIS-TLM, 측정압 ~40 MPa | ✅ stated |
| **τ_ion @ 42 vol% CAM** | 2.07 | **τ_ion² = 4.3 → τ_ion = √4.3 = 2.07** | **42 vol% NCM-622**, EIS-TLM | ✅ τ²=4.3 stated; τ=2.07 = √ |

**세 앵커 전부 이 논문에 정확히 있다. 출처 정정 확정:**

1. **"Minnmann porosity 14 % / 13–17 %"** → **Minnmann 2021 JES 040537** (Table SIII; dry-mix 380 MPa).
   *2022 AEM Perspective 아님.* 2022 리뷰는 porosity 측정값 0개(전부 정성).
2. **"σ_ion_eff 0.17 mS/cm"** → **Minnmann 2021 JES 040537**, 본문 p.5 명시
   ("the effective ionic conductivity of the composite cathode is still 0.17 mS cm⁻¹").
3. **"τ_ion 2.07"** → **Minnmann 2021 JES 040537**. ★ **중요한 미묘함**: 논문은 *tortuosity factor* τ²
   를 보고한다(Fig 2b 세로축 = "Tortuosity Factor τ²"; Eq 4 = τᵢ² = (σ_i,eff/σ_i,0)⁻¹·φ_i). 42 vol%서
   **τ_ion² = 4.3**. 우리가 인용하는 **2.07 = √4.3** 즉 *선형 tortuosity* τ_ion. 둘 다 맞고 일관 —
   **단, 인용 시 "τ_ion = 2.07 (= √(τ²=4.3))" 로 명기**해야 τ vs τ² 혼동을 막는다.

**압력 구분 (인용 시 필수):**
- **압밀(fabrication) 압력 = 380 MPa** 단축 (dry mix, RT, 3 min). 우리 production 300 MPa cold-press와 같은 계열.
  - (separator SE 층만 100 MPa, 그 위 양극 적층 후 bilayer 전체 380 MPa로 consolidation.)
- **EIS 측정 압력 = ~40 MPa** (스택을 force sensor + spring으로 ~40 MPa 유지하며 측정). 이건 압밀압이 아니라
  *측정 중 접촉 유지*용. 우리가 σ를 비교할 땐 "**380 MPa로 압밀된 14 % porosity 구조를 ~40 MPa 하에서 측정**"이
  정확한 조건이다.
- (참고: cell cycling도 ~40 MPa 일정 압력.)

**우리 다른 앵커들과의 분리(2022 리뷰 digest 결론 재확인):**
- "밀도 87 % @300 MPa" = **Sakuda 2013** (75Li₂S-25P₂S₅), 이 논문 아님.
- "pure-SE 10 % @300 MPa" = 우리 MPM 3D(σ_y 0.30) 수렴값 (Sakuda/이 논문 cold-press 거동 위에 보정).
  ⚠ **이 논문은 pure-SE porosity를 별도 측정하지 않는다** — 14 %는 *복합 양극* 값이다(아래 §3 주의).

---

## §1. 메타 / 한 줄 요약

| 항목 | 값 |
|---|---|
| 저자 | **Philip Minnmann, Lars Quillman, Simon Burkhardt, Felix H. Richter, Jürgen Janek** |
| 소속 | Institute of Physical Chemistry & Center for Materials Research (LaMa), Justus-Liebig-University **Giessen** (Janek 그룹) |
| 저널 | *J. Electrochem. Soc.* **168** (2021) 040537 — **Editors' Choice**, Open Access (CC BY 4.0) |
| DOI | **10.1149/1945-7111/abf8d7** |
| 투고/수정/게재 | 2021-02-22 / 2021-04-01 / 2021-04-27 |
| 소재 | **NCM-622** (LiNi₀.₆Co₀.₂Mn₀.₂O₂, BASF, D̄≈3 µm) + **Li₆PS₅Cl** (LPSCl, NEI Corp) |
| 도전제 | 무첨가 기본 / VGCF(vapor-grown carbon fiber) 비교군 |
| 음극 | In/(InLi)ₓ (x≈0.3), 0.62 V vs Li⁺/Li |
| 연구유형 | **실험** — EIS + **TLM(transmission-line-model)** 피팅 + DC polarization + galvanostatic cell cycling |

**한 줄 요약**: 우리 소재계(NCM-622 + LPSCl)의 복합 양극을 **이온/전자 차단 대칭셀 EIS + TLM 피팅**으로
**유효 이온/전자 부분 전도도 σ_i,eff·σ_el,eff 와 tortuosity factor τ²** 를 CAM vol% 25→61 %에 걸쳐
1차 측정하고, 이를 cell cycling 비용량과 상관시켜 **"저-CAM = 전자 percolation 병목 / 고-CAM = 이온 수송
병목"** 이라는 전하수송 병목 프레임을 정량화. **고-CAM 적재가 carbon 무첨가를 가능케 함**과 **SE 입자 미세화로
이온 tortuosity↓ → C-rate↑** 를 demonstrate. → 우리 DEM σ_ionic 솔버·Stage-E·percolation·coverage의
**실험 절대 앵커**이자, σ_ion_eff/τ/porosity 핵심 수치의 1차 출처.

---

## §2. 실험 방법 (Experimental) — 상세

### 2.1 재료 (intrinsic 물성 — 우리 σ_grain 교차점)
| 재료 | 물성 | 값 | 비고 |
|---|---|---|---|
| LPSCl (NEI) | **이온 bulk σ** | **1.6 mS/cm @ 25 °C** | EIS 측정 (★ 우리 Cronau 단결정 3.0 / Bazzoun pellet 1.02 / Lee 2.19 사이) |
| LPSCl | **전자 bulk σ** | **1×10⁻⁶ S/cm** | DC polarization (이온의 1600×↓ → 전자 무시 가능) |
| LPSCl (fine) | 밀링 σ | 1.6 → **1.2 mS/cm** | wet-mill(heptane/dibutyl-ether 8:1, 30:1 media, 200 rpm, 10 h) 후 약간↓ (GB/분해) |
| NCM-622 (BASF) | **전자 partial σ** | **10 mS/cm** | SI Table S2; 이온 σ는 무시(혼합전도 무시 단순화) |
| NCM-622 | D̄ | **3 µm** | 200 °C 진공 건조 |
| LPSCl | density | **1.87 g/cm³** | vol%↔wt% 변환용 |
| NCM-622 | density | **4.65 g/cm³** | (다른 부분 4.65, 일부 4.77 표기 혼재) |

### 2.2 셀 구성 (병목 분리의 핵심 = 차단전극 선택)
복합 양극은 이온(SE)·전자(CAM) 두 경로가 동시에 흐른다. 한쪽만 보려면 **반대쪽을 막는 대칭셀**:
- **전자 측정** → **이온-차단(ion-blocking) 셀**: steel | 복합양극 | steel (양 끝 stainless steel = 이온 막음).
- **이온 측정** → **전자-차단(electron-blocking) 셀**: In/(InLi)ₓ | LPSCl | 복합양극 | LPSCl | In/(InLi)ₓ
  (LPSCl 층이 전자 막음, In/InLi = Li reservoir + low-viscosity polarization).
- 셀 제작: 분말 100 mg(전도도용) → ⌀10 mm 다이 → **단축 380 MPa, 3 min, RT**.
  ASSB(cycling)용: SE 60 mg를 100 MPa로 separator(~200–380 µm) 압밀 → 양극 12 mg(15.3 mg/cm², 214 mAh/cm²)
  적층 → **bilayer 전체 380 MPa, 3 min**.

### 2.3 EIS / cycling 조건
- EIS: Biologic VMP-300, 10 mV, **7 MHz–50 mHz**, **측정압 ~40 MPa** (force sensor + spring으로 압력완화 보상),
  RELAXIS-3 피팅, Kramers-Kronig stationarity 검증.
- Cycling: MACCOR, 25 °C, 일정전류, **~40 MPa**, theoretical capacity 200 mAh/g 가정, C-rate 0.1/0.25/0.5/1 C.
- CAM vol% 범위: **25–61 vol%** (전도도), cycling은 33/42/52/53/61 vol%.

---

## §3. ★ POROSITY (우리 1번 앵커)

- **avg 14 %** : 본문 p.5 — vol% 계산 시 "an average porosity of 14 % is assumed" (Fig 2 vol% 변환의 기준 가정).
- **13–17 % range** : Conclusions/recommendations(p.9) — "composite cathodes prepared by a dry mixing process
  with subsequent uniaxial consolidation exhibit a typical porosity of **13 %–17 %** (Table SIII), which is
  comparable to values reported in literature." (Sakuda 등 계열).
- 조건: **dry mixing(agate mortar 15 min) + 단축 380 MPa**. (= 우리 production cold-press 300 MPa와 같은 계열,
  약간 더 높은 압력.)
- porosity의 의미(논문 자체 강조): porosity는 **부피 에너지/출력 밀도뿐 아니라 이온·전자 전달 둘 다 차단** →
  낮은 유효 전도도 + 높은 tortuosity의 직접 원인. **"porosity를 최대한 줄여라"** 가 첫 번째 최적화 권고
  (cold/warm isostatic press로 single-digit porosity 가능 — Lee et al. 인용; 또는 저점도 액/폴리머 침투).

⚠ **주의 (인용 정밀도)**:
- 이 14 %·13–17 %는 **복합 양극(NCM+LPSCl) 전체 porosity** 이다. **pure-SE porosity 아님.**
  우리 "pure-SE ~10 % @300" 은 이 논문이 주는 값이 아니라 우리 MPM 수렴값(+Sakuda 87 % 밀도).
- 14 %는 일부 맥락에서 *vol% 계산용 가정값*, 13–17 %는 *실측 range*. 둘 다 같은 dry-380MPa 공정.
- 압밀 380 MPa ≠ 측정 40 MPa ≠ 작동압. porosity는 **380 MPa 압밀** 결과다.

---

## §4. ★ EIS-TLM 방법 (우리 네트워크 솔버 + τ_Laplace,eff 의 실험 아날로그)

### 4.1 왜 단순 병렬회로가 안 되나
복합 양극은 여러 상·여러 전하경로가 **공간적으로 분포**해 흐른다. 단순 R∥C 병렬조합으로 안 됨 →
다공막의 물질수송에 쓰는 **transmission-line-model(TLM, "T-type")** 사용 (Siroma et al. 유도, Eq 1).

### 4.2 TLM 임피던스 (Eq 1, Siroma "open-open")
```
Z_CC(ω) = z_ion·z_el/(z_ion+z_el)·L
        + 2·z_el²·√z_ion / (z_ion+z_el)²
          · [ cosh(L·√((z_ion+z_el)/z_int)) − 1 ] / sinh(L·√((z_ion+z_el)/z_int))
```
- **z_el** [Ω m] = 전자 전도상(CAM) 단위길이 임피던스, **z_ion** [Ω m] = 이온 전도상(SE), **z_int** [Ω m⁻¹] =
  두 상 사이 계면 임피던스. **L** [m] = 복합 양극 두께.
- 등가회로(Fig 1): z_el = (r_el,1, r_el,2, CPE_el) — r_el,1 = 전자 bulk, r_el,2 = 계면 전하전달; z_ion = r_ion;
  z_int = CPE_int. 계면은 **non-faradaic** 가정(fully-lithiated NCM = 확산제한 → 높은 전하전달저항).
- 피팅으로 **R_el, R_ion** 추출. (이온/전자 차단 셀에서 z_ion↔z_el 역할 교환.)

### 4.3 유효 전도도 & tortuosity (Eq 2–4) ★ 우리와 1:1 대응
```
σ_i,eff = L / (R_i · A)                                    [Eq 2]   (실린더 양극, A=단면적)
τ_i     = l_i / l_0   (최단경로/직선거리, 기하 정의)         [Eq 3]
τ_i²    = (σ_i,eff / σ_i,0) · φ_i                          [Eq 4]   ★ 보고값 = τ², 우리 τ_Laplace,eff와 대응
```
- **Eq 4 = 우리 τ_Laplace,eff 의 실험 정의.** σ_i,eff(유효) / σ_i,0(bulk) / φ_i(부피분율) 로부터 τ²를 역산.
  우리 솔버가 Kirchhoff/Laplace로 σ_eff를 풀고 τ_eff = √(σ_0·φ/σ_eff) 로 뽑는 것과 **수학적으로 동일**.
- 단, Eq 4 τ는 **current constriction / CEI / interface polarization / space-charge를 무시** → "geometric"
  tortuosity와 다를 수 있음(논문 명시). 우리 Holm 구속저항(Stage-E)이 바로 그 constriction을 일부 포함 →
  비교 시 **그들 τ는 constriction 미포함, 우리 τ_Laplace는 솔버에 따라 포함/미포함 명시** 필요.

### 4.4 핵심 측정값 (42 vol% NCM 기준점 — 우리 2·3번 앵커)
대표 셀: **42 vol% NCM**, 두께 **L = 470 µm**, 단면적 **A = 0.785 cm²**.
- **R_el = 107 Ω, R_ion = 360 Ω** (TLM 피팅).
- → **σ_el,eff = 5.6×10⁻⁴ S/cm = 0.56 mS/cm**, **σ_ion,eff = 1.7×10⁻⁴ S/cm = 0.17 mS/cm** ★.
- → **τ_el² = 7.4, τ_ion² = 4.3** ★ (즉 **τ_ion = 2.07**, τ_el = 2.72).
- 해석: 42 vol%서 σ_ion,eff(0.17)는 LPSCl bulk(1.6)의 **약 1/10(≈4×아님, 본문 "about four times lower"는
  다른 맥락; 실제 1.6/0.17 ≈ 9.4×)**. 그래도 0.17 mS/cm는 β-Li₃PS₄ bulk 수준이라 124 mAh/g cell 구동 가능.

---

## §5. ★ CAM vol% 스윕 (Fig 2) — 우리 AM:SE 스윕 + percolation 대응

Fig 2a = σ_i,eff·σ_el,eff vs φ_NCM(0–100 %); Fig 2b = τ_i² vs φ_NCM. (avg porosity 14 % 가정; dashed=eye-guide.)

| φ_NCM (vol%) | σ_ion,eff (S/cm) | σ_el,eff (S/cm) | τ_ion² | τ_el² | 비고 |
|---|---|---|---|---|---|
| 0 (pure SE) | ~1.6×10⁻³ (=bulk) | — | ~1 | — | τ→1 (순수상) |
| 25 | ~1.4×10⁻³ (높음) | ~2.1×10⁻⁵ (낮음) | **~2.4** | **~120** | ★ 전자 percolation 거의 끊김(τ_el²=120!) |
| 33 | ↓ | ~2.4×10⁻⁴ (+1 order) | ↑ | ↓ | 25→33서 σ_el **10×↑** (Eq: 2.1e-5→2.4e-4) |
| **42** | **1.7×10⁻⁴** | **5.6×10⁻⁴** | **4.3** | **7.4** | ★ **우리 앵커**; 이온≈전자 교차점 부근 |
| 53 | ↓↓ | ↑ | **~15.3** | ↓ | 이온 tortuosity 급등 |
| 61 | ~1×10⁻⁶ 수준 | ~1×10⁻³ | 매우 큼 | **~4.3** | 전자 충분(τ_el²=4.3), 이온 병목 극심 |
| 100 (pure NCM) | — | ~7×10⁻³ (=bulk 10 mS/cm) | — | ~1 | τ→1 |

**추세(우리와 직접 비교 가능):**
- **CAM↑ → σ_ion,eff↓, σ_el,eff↑** (정확히 역방향). 우리 AM:SE 스윕(AM↑→σ_ionic↓)과 **같은 방향**.
- **τ_ion² : 25 vol%서 ~2.4 → 53 vol%서 ~15.3** (단조 증가; CAM이 SE 경로를 막을수록 이온 우회로 길어짐).
- **τ_el² : 25 vol%서 ~120(거의 절연) → 61 vol%서 ~4.3** (단조 감소; CAM이 전자망을 채울수록 직선화).
- **σ_ion,eff·σ_el,eff 모두 10⁻⁶–10⁻³ S/cm 범위** (25–61 vol%).
- **교차(crossover)**: 저-CAM서 σ_ion > σ_el (이온 풍부, 전자 빈약); 고-CAM서 σ_el > σ_ion (반대).
  ≈ 42 vol% 부근이 균형점.

★ **우리 percolation-failure-at-SE-poor (Park 2020 90 wt%) 와 대응**: 저-CAM(25 vol%)서 τ_el²=120 =
**전자 percolation 거의 실패** → 이게 carbon이 필요한 이유. 우리 σ_e 폼의 φ_AM⁴ + percolation(f_p) 항이 잡는 영역.

---

## §6. CAM vol% × cycling 비용량 (Fig 3) — 병목의 cell-level 발현

- Fig 3 = 비용량 q vs φ_NCM(0–100 %) / w_NCM(0–100 %), 0.1/0.25/0.5/1 C, composite-specific(위)·CAM-specific(아래).
- **둘 다 inverse-U-shape** → **최적 CAM vol%가 중간(저·고 양 끝 사이)에 존재**.
- 33 vol% NCM: CAM-specific **137 mAh/g @0.1C → 83 @1C** (−40 %).
- 61 vol% NCM: **132 @0.1C → 16 @1C** (−88 %, 고-CAM이 C-rate서 급락 = 이온 병목).
- **최고**: **~42 vol% NCM, 154 mAh/g @0.1C, 91 @1C** ★ (= 우리 앵커 vol%와 일치!).
- composite-specific는 42→61 vol% 사이서 ~115 mAh/g(@0.1C)로 **포화**.
- "pure-SE 14 % porosity 경계"를 vertical dashed line으로 표시 (porosity 한계 강조).
- 해석: **저-CAM = 전자 percolation/utilization 병목, 고-CAM = 이온수송(τ_ion↑) 병목.** 중간이 최적.

★ **우리 production core(AM 70–85 wt% ≈ SE 30–50 % of solid)와의 매핑**: 42 vol% NCM ≈ w_NCM 73 %
(Fig 3 위 축; density 1.87/4.65로 변환) — 우리 AM-rich core와 같은 영역. **42 vol% = 154 mAh/g 최적**이
우리 production core 선택의 실험 근거.

---

## §7. 활물질 이용률 / dead-particle (utilization) — 우리 f_AM^cc / dead-AM 대응

- "utilization level" 정의 = **이온 + 전자 망에 *둘 다* 연결된 CAM 입자 비율** (둘 중 하나라도 끊기면
  electrochemically inactive = dead). ★ **우리 f_AM^cc (connected fraction) / dead-AM warning 과 정확히 같은 개념.**
- CAM vol%↑ → 어느 임계 넘으면 **추가 CAM이 ion-conducting phase에서 고립 → inactive**. (SE가 부족해서
  새 CAM을 덮지 못함.) → CAM vol% 더 올리면 utilization↓ → 비용량↓.
- 이게 inverse-U의 *고-CAM* 쪽 하강 메커니즘 중 하나. (다른 하나는 τ_ion↑ IR-drop.)
- 우리 대응: 우리 "dead-AM (f_AM^cc < 80 %)" 경고, ionically-vulnerable-AM, AM-no-perc(σ_i=0 SE-no-perc) 케이스.

---

## §8. 전자 한계 극복 — carbon(VGCF) 첨가 (Fig 4)

- **핵심 주장**: **고-CAM(≥42 vol%)이면 carbon 무첨가로 충분** (CAM 자체가 전자 percolation 형성).
  이는 conventional LIB(항상 carbon 필요)와의 **근본적 개념 차이**.
- VGCF 첨가(1 mg/100 mg composite) 실험:
  - **33 vol% NCM**(저-CAM): VGCF → material-specific 비용량 **+13 % @0.1C** (고립 CAM을 전자적으로 연결).
    하지만 효과가 C-rate 의존 약함 → **고립 CAM 회수**가 주효과(전자 percolation 신규 생성), 전도율 자체 개선 아님.
  - **61 vol% NCM**(고-CAM): VGCF 효과 **거의 없음/약간 악화** (이미 전자 충분; carbon-SE 계면 분해가 이온
    tortuosity↑ 유발 가능).
- 전자 tortuosity factor τ_el²: 25 vol%서 120 → 61 vol%서 **4.3** → 42 vol%(τ_el²≈7.4) 이상서 CAM이
  전자망에 연결됨 → carbon 불필요. (단, carbon의 전위가 CAM과 비슷 → 표면 SE/CAM 분해 위험도 있음.)

★ 우리 대응: σ_e 폼의 percolation·VGCF(도전제) 항. **Lee 2025 PTFE/VGCF σ_e 데이터**와 결이 같음
(도전제가 σ_e *기여* — 단 Lee는 PTFE wt%↑면 σ_e 급감 페널티도 보여줌, 이 논문엔 없음).

---

## §9. 이온 한계 극복 — SE 입자 미세화 (Fig 5, 6) ★ 우리 size=packing 과 직접 대응

### 9.1 전류밀도 스윕 (Fig 5)
- q vs current density j (mA/cm²), CAM 33/42/52/61 vol%.
- **j > 0.5 mA/cm²서 CAM > 53 vol% 셀이 급격히 하강** (이온 수송이 양극 내 비용량 제한).
- **j < 0.5 mA/cm²서는 최저-CAM(33 vol%)이 오히려 composite-specific 더 낮음** (저-CAM은 저전류서도
  전자 utilization 병목). → 다시 **42 vol% 균형 최적** 확인.
- C-rate(상수전류) 대신 **constant current density(j)**로 비교해야 anode-side overpotential 분리 가능(논문 강조).

### 9.2 SE 입자 크기 효과 (Fig 6) — coarse vs fine LPSCl, 61 vol% NCM
- ball-mill로 LPSCl 입자 미세화(coarse → fine, >10 µm 입자 제거, SE 분산↑).
- **σ_ion,eff(fine) > σ_ion,eff(coarse)** ★ (작은 SE → CAM 사이 더 균일 분산 → 이온 경로 개선,
  τ_ion↓). 단 fine은 σ_el,eff 약간↓(CAM clustering 감소로 전자망 약화).
- **C-rate 성능 fine이 우월** (이온 IR-drop↓). CAM-specific q: fine이 모든 C-rate서 더 높음.
- bulk σ는 coarse 1.6 → fine 1.2 mS/cm로 **오히려 약간↓**(밀링 GB/amorphization) — 그럼에도 **유효 σ는↑**
  (분산/tortuosity 개선이 bulk 손실을 압도). ★ "**작은 SE가 좋은 건 bulk σ 때문이 아니라 packing/분산
  (τ↓) 때문**" — 우리 "size effect = PACKING not overlap" 결론과 **정확히 일치**.

### 9.3 정량 목표(논문 자체 계산)
- 61 vol% NCM 최적 C-rate 위해선 σ_ion,eff = **0.4 mS/cm** 필요 → 현재 τ_ion²=34(61 vol%, fine)서는
  bulk σ가 **≥47 mS/cm** 여야 함(현 LPSCl 1.6의 ~30×). 비현실적.
- 만약 τ_ion²를 <10으로 낮추면(미세구조 개선) bulk **16 mS/cm**면 충분 → **고전도 SE + 저 tortuosity 둘 다** 필요.
- ★ **우리 인사이트와 직결**: σ_eff = σ_bulk·φ/τ² → bulk만 올리는 건 한계, **tortuosity(미세구조/packing)
  개선이 핵심.** 이게 우리 DEM이 미세구조-σ를 푸는 가치의 실험적 정당화.

---

## §10. Figure / Table 요약 (각각 우리가 쓸 점)

| Fig/Tab | 내용 | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **Fig 1** | 이온/전자 차단 대칭셀 + 대표 Nyquist + T-type TLM 등가회로 | 42 vol%: ion-block 0–140 Ω(1kHz/1Hz 표시), e-block 0–500 Ω | EIS-TLM이 **우리 솔버의 실험 아날로그** — z_ion/z_el/z_int 분리법 |
| **Fig 2a** | σ_ion,eff·σ_el,eff vs φ_NCM | 25→61 vol% 전 구간 10⁻⁶–10⁻³ S/cm; 42 vol% 교차 | ★ **CAM vol% 스윕 = 우리 AM:SE 스윕**; crossover |
| **Fig 2b** | **τ²** vs φ_NCM | τ_ion² 2.4→15.3, τ_el² 120→4.3 | ★ **τ_ion²=4.3 @42 → τ=2.07 앵커**; 우리 τ_Laplace,eff 대응 |
| **Fig 3** | 비용량 vs φ_NCM (4 C-rate) | **42 vol% 154 mAh/g @0.1C** 최적; inverse-U | ★ 최적 CAM = 우리 production core; 병목 cell 발현 |
| **Fig 4** | VGCF 효과 (33 vs 61 vol%) | 33 vol% +13 % @0.1C; 61 vol% 무효 | 고-CAM carbon 불필요; 우리 σ_e 도전제 항 |
| **Fig 5** | 비용량 vs current density (4 vol%) | j>0.5 서 >53 vol% 급락 | 이온 병목의 j-의존; 42 vol% 균형 |
| **Fig 6** | coarse vs fine SE (61 vol%) | fine σ_ion,eff↑·C-rate↑ (bulk 1.6→1.2) | ★ **작은 SE = packing/τ↓ (bulk 아님)** — 우리 결론 일치 |
| **Table SII** | vol%별 두께·areal capacity·τ² | (SI; L=470 µm @42 vol% 등) | porosity·τ 보조 |
| **Table SIII** | **porosity 13–17 %** | dry-mix 380 MPa | ★ **porosity 앵커 range 원전** |
| **Table S2(SI)** | NCM-622 전자 partial σ = **10 mS/cm** | | CAM 전자 bulk 앵커 |

(SI는 본 PDF에 미포함 — "04._Sup" 업로드는 *다른 논문*이라 무시. Table SII/SIII/S2 값은 본문 인용으로 확인.)

---

## §11. ★ 비교 vs 우리 DEM+MPM (focused §)

| 축 | 이 논문 (실험, NCM-622+LPSCl) | 우리 DEM+MPM (NMC811+LPSCl) | 차이 / 매핑 / 주의 |
|---|---|---|---|
| **porosity** | **14 % (13–17 %)** @ dry-mix **380 MPa** (복합 양극) | pure-SE ~10 % / real_14 15.6 % @300 MPa | ★ 우리 앵커 출처 확정; **복합 13–17 %는 우리 real_14 15.6 %와 직접 정합**(±조건). pure-SE 10 %는 이 논문 아님 |
| **σ_ion,eff** | **0.17 mS/cm @ 42 vol% NCM** (EIS-TLM, 측정 ~40 MPa) | DEM σ_ionic 0.04–0.18 mS/cm, envelope 0.03–0.14 | ★ **같은 소재 → 직접 비교 가능**; 0.17이 우리 상단(0.18)과 일치. 우리 솔버의 절대 앵커 |
| **τ_ion** | **2.07** (=√(τ²=4.3)) @ 42 vol% | 우리 τ_Laplace,eff (솔버 geodesic/Laplace) | ★ **같은 정의(Eq 4 = σ_0·φ/σ_eff)**; ⚠ 그들 = constriction 미포함, 우리 = 솔버 의존 명시 필요. τ vs τ² 혼동 주의 |
| **σ_grain (bulk)** | LPSCl **1.6 mS/cm @25°C** (제품 단결정/응집 EIS) | Cronau 단결정 **3.0** ×Cronau(r_SE) | 1.6 < 3.0 → 측정·GB·입자 차이. **Bazzoun 1.02 / Lee 2.19 / 이 논문 1.6** = bulk LPSCl 앵커 스프레드(절대 직접대조 금지, 범위로) |
| **CAM 전자 bulk** | NCM-622 **10 mS/cm** (SI S2) | NMC811 우리 σ_AM(e) Trevisanello 10/5 | ★ **우리 σ_e LOCKED endpoint 10 mS/cm 와 일치**(같은 NCM 계열) |
| **CAM vol% 스윕** | 25–61 vol%, σ↓/τ↑(이온), 최적 42 | AM:SE 스윕 + Furnas + percolation | ★ CAM↑→σ_ion↓ 추세 일치; 42 vol% 최적 = 우리 core |
| **utilization (dead)** | ion+e 둘 다 연결돼야 active; 고-CAM서 고립 | f_AM^cc / dead-AM / ionically-vulnerable | ★ **개념 동일** — 우리 dead-AM 경고의 실험 근거 |
| **전자 병목 (저-CAM)** | 25 vol%서 τ_el²=120 (percolation 실패) | σ_e φ_AM⁴ + percolation(f_p) | ★ Park 2020 90 wt% percolation 실패와 같은 물리 |
| **size 효과** | fine SE → σ_ion,eff↑ (bulk↓에도) = packing/τ | "size effect = PACKING not overlap" | ★ **결론 정확히 일치** |
| **transport 채널** | σ_ion + σ_el (이온·전자 둘 다) | σ_ion + σ_e + σ_thermal (삼중항) | 우리 σ_thermal 추가 우위 |
| **방법** | **실험 EIS-TLM** (solver 아님) | DEM Kirchhoff/Holm 솔버 + Stage-E | ★ **그들 실험 = 우리 솔버의 frame[4] 외부 검증** |
| **Stage-E 대응** | TLM이 constriction/CEI 무시(Eq 4 주의) | Stage-E 소성 접촉면적(Tabor+volume) | 우리 Stage-E가 그들이 무시한 constriction을 포함 → σ_eff 보정 방향 |
| **소성/morphology** | 없음(실험, 미세구조 가정만) | MPM 진짜 SHAPE 소성 | 우리 MPM 고유 (frame[5]) |

**핵심 정합 3가지:**
1. **σ_ion,eff 0.17 mS/cm @42 vol% = 우리 DEM σ_ionic 상단(0.18)과 일치** — 같은 소재, EIS-TLM = 실험 진실.
2. **복합 porosity 13–17 % = 우리 real_14 15.6 %** (둘 다 ~300–380 MPa cold-press 복합 양극).
3. **size·tortuosity 결론 일치**: "작은 SE가 좋은 건 packing/τ 때문(bulk σ 아님)" — 우리와 동일.

---

## §12. ★ 우리 σ_ionic / Stage-E / 솔버에 어떻게 쓰나 (적용 인사이트)

1. **σ_ion 절대 앵커 정정·도입**: "Minnmann 2021 JES 040537, σ_ion,eff = **0.17 mS/cm @ 42 vol% NCM,
   τ_ion = 2.07 (τ²=4.3), 복합 porosity 14 % (13–17 %), dry-mix 380 MPa**" 를 우리 σ_ionic·τ 외부 검증점으로
   고정. (그들 vol% NCM → 우리 φ_SE 매핑: 42 vol% NCM ≈ SE 58 vol%, w_NCM≈73 %.)
2. **τ vs τ² 표기 통일**: 우리 코드/문서에서 "Minnmann τ_ion 2.07" 인용 시 반드시 **"= √(tortuosity factor
   τ²=4.3)"** 병기. Eq 4 = σ_0·φ/σ_eff = 우리 τ_Laplace,eff 정의와 동일함을 명기.
3. **CAM vol% 스윕 σ_ion,eff·τ² 곡선 = 우리 AM:SE 스윕 검증 곡선** (Fig 2). 추세(CAM↑→σ↓, τ↑) 직접 대조.
   25 vol%서 τ_el²=120(전자 percolation 실패) = 우리 σ_e percolation 항 검증점.
4. **Stage-E constriction 기여 정량**: 그들 Eq 4 τ는 constriction 미포함 → 우리 Stage-E(Holm 구속) 포함
   σ_eff와 같은 구조서 비교하면 **Stage-E가 더하는 보정폭** 정량 가능 (Bazzoun RNM 과소 보정과 같은 lever).
5. **bulk σ 스프레드 확장**: LPSCl 1.6 mS/cm 추가 → {Cronau 단결정 3.0, Lee pristine 2.19, 이 논문 1.6,
   Bazzoun pellet 1.02} 의 측정/입자/GB 스프레드 (절대 직접대조 금지, 범위·민감도로만).
6. **σ_e endpoint 확인**: NCM-622 전자 10 mS/cm = 우리 σ_e LOCKED 10 mS/cm 와 일치 → 우리 endpoint 재확인.

---

## §13. 인용 가능 문장 (deck/paper용)

- "The composite-cathode porosity (~14 %, range 13–17 %), effective ionic conductivity (0.17 mS cm⁻¹ at
  42 vol% NCM-622) and ionic tortuosity (τ_ion = 2.07, i.e. τ² = 4.3) that anchor our DEM compaction and
  σ_ionic calibration are the EIS-TLM measurements of **Minnmann et al., J. Electrochem. Soc. 168 (2021)
  040537** on the identical NCM/Li₆PS₅Cl system, fabricated by dry mixing + 380 MPa uniaxial consolidation —
  *not* the 2022 design Perspective, which reports no quantitative porosity/σ data."
- "Our DEM σ_ionic (0.04–0.18 mS cm⁻¹) brackets the experimental σ_ion,eff = 0.17 mS cm⁻¹ measured by
  transmission-line-model EIS at 42 vol% CAM (Minnmann 2021), providing a same-material external validation."
- "Minnmann (2021) find, as we do, that finer solid-electrolyte particles raise the *effective* ionic
  conductivity (lower tortuosity) even though milling slightly lowers the *bulk* conductivity (1.6→1.2
  mS cm⁻¹) — confirming that the size benefit is a packing/tortuosity effect, not a bulk-σ effect."

---

## §14. 미니 용어집

- **EIS** (Electrochemical Impedance Spectroscopy): 정현파 전압 인가 후 주파수별 임피던스 Z(ω) 측정. Nyquist
  plot(−Im Z vs Re Z)의 호/직선으로 bulk·계면·확산 저항 분리.
- **TLM** (Transmission-Line-Model): 다공·복합 매질의 분포 임피던스 모델. 직렬 z_ion·z_el 경로 + 분포 계면
  z_int. "T-type open-open"(Siroma) = Eq 1. **단순 R∥C 병렬로 안 되는** 복합 양극에 필수.
- **ion-blocking / electron-blocking 셀**: 한쪽 전하만 막는 대칭 전극(steel=이온 막음, LPSCl=전자 막음)으로
  σ_el / σ_ion 을 *분리* 측정. 병목 분해의 핵심 실험 트릭.
- **tortuosity factor τ²** vs **tortuosity τ**: 논문 Fig 2b 세로축 = **τ²** (= σ_0·φ/σ_eff, Eq 4). 선형 τ =
  √(τ²). ★ 우리 "2.07" = √(4.3). 인용 시 구분.
- **partial / effective conductivity**: partial = 한 전하종(이온 또는 전자)의 전도도; effective = 그 partial이
  미세구조(porosity·tortuosity·분산) 때문에 *유효하게* 감소한 값. σ_eff = σ_bulk·φ/τ².
- **utilization level**: 이온·전자 망에 *둘 다* 연결된 CAM 비율 (= active CAM). 우리 f_AM^cc.
- **CEI** (Cathode-Electrolyte Interphase): CAM/SE 계면 반응층. Eq 4 τ는 이를 무시.
- **VGCF** (Vapor-Grown Carbon Fiber): 도전제. 저-CAM서 고립 CAM 회수.
- **inverse-U / 최적 CAM**: 비용량 vs CAM vol%가 ∩ 모양 → 중간(42 vol% NCM)서 최대.

---

## §15. 정직한 한계 / over-claim 방지

- **실험 논문 = 솔버 없음.** 우리 Kirchhoff/Holm·삼중항(σ_i/σ_e/σ_thermal)·Stage-E 소성면적·fracture-Holm·
  MPM 정량 변형장 우위는 유지. 이 논문은 *측정 앵커*지 *모델 경쟁자*가 아니다.
- **소재 일치하나 CAM grade 차이**: 이 논문 **NCM-622** vs 우리 **NMC811**. CAM 전자 bulk(둘 다 ~10 mS/cm 계열)는
  유사하나, 입자 형태/균열 거동/intrinsic σ는 다를 수 있음 → σ_ion,eff 절대값 비교는 "같은 LPSCl 매트릭스 +
  유사 CAM" 수준의 정합으로 해석(완전 동일 소재 아님).
- **τ vs τ² 혼동 위험**: 가장 흔한 인용 오류. 2.07(τ) vs 4.3(τ²) 반드시 구분.
- **압력 3종 구분 필수**: 압밀 380 MPa(porosity 결정) ≠ EIS/cycling 측정 40 MPa ≠ 작동압. σ는 380 MPa 압밀
  구조를 40 MPa서 측정한 값.
- **porosity는 복합 양극**(14 %/13–17 %), **pure-SE 아님.** "pure-SE 10 %"는 이 논문이 주지 않음(우리 MPM 수렴값).
- **digitized vs stated**: 42 vol% 기준점 수치(0.17, 4.3, 7.4, R_el/R_ion, L, A)는 전부 **stated(본문)**.
  Fig 2의 다른 vol% 곡선값(25/33/53/61 vol%의 σ·τ²)은 일부 본문 stated(2.4/15.3/120/4.3 등) + 일부
  **Fig에서 읽은 추세**(±) — 위 §5 표의 "~" 표기 값은 trend-only.
- **bulk σ 1.6 vs 우리 Cronau 3.0**: 측정/입자/GB 차 → 절대 직접대조 금지, 범위로만. 우리 σ_grain 이중계상
  점검(pellet/단결정/제품 EIS 혼용 주의)에 추가 데이터점으로.
- **이 논문 자체의 한계(저자 명시)**: porosity 정확 측정 어려움; Eq 4 τ는 constriction/CEI/space-charge 무시 →
  "true" geometric τ와 다를 수 있음; SI 미포함(본 PDF) → Table 값은 본문 인용으로 확보.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
</content>
</invoke>

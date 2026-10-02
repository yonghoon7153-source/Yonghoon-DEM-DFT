# Minnmann 2021 JES — 복합 양극 전하수송 병목 정량화 (EIS-TLM) ★ 우리 porosity/σ_ion/τ_ion 앵커의 진짜 출처

> slug `minnmann2021_jes_charge_transport_bottlenecks` · DOI `10.1149/1945-7111/abf8d7` · type `DEM` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


> slug `minnmann2021_jes_charge_transport_bottlenecks` · DOI `10.1149/1945-7111/abf8d7`
> · type `experiment (EIS-TLM + cell cycling)` · 저널 `J. Electrochem. Soc. 168 (2021) 040537`
> · PDF `ec8f708f-04._Minnmann_2021_J._Electrochem._Soc._168_040537.pdf`
> · digested `2026-06-26` · status ✅
>
> ★★ **이 논문이 우리 "Minnmann porosity ~14 % / 13–17 %", "σ_ion_eff 0.17 mS/cm", "τ_ion 2.07 @ 42 vol% CAM"
> 앵커의 진짜 출처다.** 그동안 Minnmann *2022* AEM Perspective(설계 리뷰, 정량 데이터 0개)로 잘못 인용돼
> 왔으나, 2022 리뷰 digest가 그게 거기 없음을 증명했고 → 실제 1차 측정값은 **여기(2021 JES)** 에 있다.
> 우리 소재계(NCM-622 + LPSCl)의 EIS-TLM 1차 측정 = Bazzoun/Lee와 더불어 우리가 가진 **최강 실험 앵커**.
>
> ⟦10-03 PDF 대조⟧ **본문 + SI 를 끝까지 원문 대조했다 (tortuosity 묶음).**  원문 = 인박스 `litdb/inbox/tortuosity_20261003/`
> 의 `1. Editors' choice…pdf` (10쪽 — **PDF 1쪽은 IOP 표지**, 논문은 PDF 2–10쪽, 인쇄된 쪽 번호 없음) + `1. Sup) Editors'
> choice…pdf` (SI 10쪽, Word 문서).  **이 카드의 쪽 번호는 그 PDF 의 쪽 번호다** (본문 "p.N" · SI "SI p.N").
> 바뀐 핵심 6가지 (상세는 각 절의 ⟦10-03 PDF 대조⟧ 표지 · 새 절 §16 · §17 · §18):
> 1. **인쇄된 Eq 4 는 σ 비가 뒤집혀 있다.**  원문 그대로 `τ_i² = (σ_i,eff / σ_i,0)·φ_i` (p.5, [4]).  이 꼴로 계산하면 τ² 가
>    전부 1 미만 (42 vol% 이온 0.046) 이고, 보고값 (SI Table S2 전 행) 은 **역수 꼴 `τ_i² = φ_i·σ_i,0 / σ_i,eff`** 로만
>    재현된다 — 전 행 **0.7 % 안** (Table S2 σ_eff 의 3자리 반올림 수준; 내 검산, §4.3).  ⇒ 인용은 *"Eq 4 (인쇄 꼴은 역수 오식; 보고값은 φσ₀/σ_eff)"* 로.
> 2. **σ_i,0 = 순수 시료 (펠릿) 의 EIS 겉보기 전도도** — SE 1.6 mS/cm @25 °C · NCM 10 mS/cm (완전 리튬화).  SI §3 (SI p.4) 이
>    *"순수 CAM·SE 시료에도 기공이 있어 측정 전도도를 낮추지만, 해석을 단순화하려고 순수 재료의 tortuosity factor 를 1 로
>    두었다"* 고 명시 ⇒ 보고 τ² 는 **펠릿 기준 상대값**이다 (결정립 내부 기준이 아니다).
> 3. **보고 τ² 는 협착·CEI·계면 효과를 '포함한' 값이다.**  원문 *"This equation neglects the effects originating from current
>    constriction, … CEI …"* 는 그 효과들을 따로 떼지 않아 **τ² 안에 흡수된다**는 뜻이다 (그래서 "true geometrical" τ² 와
>    다를 수 있다고 쓴다).  옛 카드의 *"그들 τ 는 constriction 미포함"* 은 반대로 읽은 것 → 정정 (§4.3 · §11 · §12).
> 4. **SI 수치를 확보했다** — Table S2 (σ_eff · τ² 전 조성, §5.0) · Table S1 (시료별 porosity **7.6 / 13 / 17 / 17 / 15 %**,
>    평균 14) · Table S3 (사이클 셀 조성 **33 / 42 / 47 / 58 / 61 vol%**).  옛 §5 표의 판독값 일부 · §2.3 의 사이클 조성 ·
>    §6·§12 의 "42 vol% ≈ 73 wt% · SE 58 vol%" 가 틀렸다 (42 vol% NCM = **70 wt%**, φ_SE **44 %** — SI Table S1).
> 5. 원문 **내부 불일치·오식**이 많다 (본문↔SI 표·그림 번호, Table S4 표지·ΔQ, Table S5 중복, "about four times",
>    "above eight", 47 mS/cm 산술, Fig 5 범례, Fig 6 축, "214 mAh cm⁻²") → **§17** 에 모았다.
> 6. **§16 tortuosity 정의 대조표** 신설 — 원문 τ_i (Eq 3) · τ_i² (Eq 4) ↔ 우리 τ_Dij · τ_Lap,eff · τ_Lap,geom · COMSOL τ_F ·
>    인계 열 사전 f / T / τ.  **§18** = 참고문헌 중 tortuosity 축 후속 목록.



> elements: Li P S
> methods: dft

---

## §0. ★ ANCHOR-PROVENANCE 확정 (이 절이 이 digest의 존재 이유)

CLAUDE.md / our_dem_baseline.md / comparison_vs_ours.md 가 "Minnmann ~14 %", "σ_ion_eff 0.17 mS/cm",
"τ_ion 2.07 @ 42 vol% CAM" 로 인용해 온 세 앵커를 **PDF에서 직접 확인**했다. 결론:

| 앵커 | 우리가 써온 값 | 이 논문(2021 JES)서 확인된 값 | 정확한 조건 | stated/계산 |
|---|---|---|---|---|
| **복합 양극 porosity** | ~14 % (13–17 %) | **avg 14 %** (가정값) · **13–17 %** ~~(실측 range)~~ ⟦10-03 PDF 대조⟧ "13–17 %" 는 **본문 문구** (p.9).  그 근거 표 (본문 표기 "Table SIII" = 실제 **SI Table S1**, SI p.4) 의 시료별 실측은 **7.6 · 13 · 17 · 17 · 15 %** (25→61 vol% 순) = **7.6–17 %**; 14 % = 이 다섯 값의 평균 (표 각주 "average value of the five measured Φ_Porosity values", 산술 13.9) | **dry mixing + 단축 380 MPa** 압밀, Table SIII (= SI Table S1) | ✅ 둘 다 stated (본문 + SI) |
| **σ_ion_eff @ ~42 vol% CAM** | 0.17 mS/cm | **0.17 mS/cm** (= 1.7×10⁻⁴ S/cm) · ⟦10-03 PDF 대조⟧ SI Table S2 정밀값 **1.66·10⁻⁴ S/cm** | **42 vol% NCM-622**, EIS-TLM, 측정압 ~40 MPa | ✅ stated |
| **τ_ion @ 42 vol% CAM** | 2.07 | **τ_ion² = 4.3 → τ_ion = √4.3 = 2.07** · ⟦10-03 PDF 대조⟧ SI Table S2 정밀값 τ_ion² = **4.27** (√4.27 = 2.07).  √ 는 원문이 아니라 **우리 산술**이고, 원문 Eq 3 의 기하 τ_i = l_i/l_0 가 **아니다** (§16) | **42 vol% NCM-622**, EIS-TLM | ✅ τ²=4.3 stated; τ=2.07 = √ |

**세 앵커 전부 이 논문에 정확히 있다. 출처 정정 확정:**

1. **"Minnmann porosity 14 % / 13–17 %"** → **Minnmann 2021 JES 040537** (Table SIII; dry-mix 380 MPa).
   ⟦10-03 PDF 대조⟧ 본문의 "Table SIII" 는 SI 에서 **Table S1** 이고, 시료별 값은 **7.6–17 %** 다 (§3 · §17 #6).
   *2022 AEM Perspective 아님.* 2022 리뷰는 porosity 측정값 0개(전부 정성).
2. **"σ_ion_eff 0.17 mS/cm"** → **Minnmann 2021 JES 040537**, 본문 p.5 명시
   ("the effective ionic conductivity of the composite cathode is still 0.17 mS cm⁻¹").
3. **"τ_ion 2.07"** → **Minnmann 2021 JES 040537**. ★ **중요한 미묘함**: 논문은 *tortuosity factor* τ²
   를 보고한다(Fig 2b 세로축 = "Tortuosity Factor τ²"; ~~Eq 4 = τᵢ² = (σ_i,eff/σ_i,0)⁻¹·φ_i~~). 42 vol%서
   **τ_ion² = 4.3**. 우리가 인용하는 **2.07 = √4.3** 즉 *선형 tortuosity* τ_ion. 둘 다 맞고 일관 —
   **단, 인용 시 "τ_ion = 2.07 (= √(τ²=4.3))" 로 명기**해야 τ vs τ² 혼동을 막는다.
   ⟦10-03 PDF 대조⟧ 취소선 사유 — `(σ_i,eff/σ_i,0)⁻¹·φ_i` 는 **보고값에 맞는 꼴이지만 인쇄된 Eq 4 가 아니다.**  원문 (p.5, [4])
   은 `τ_i² = (σ_i,eff / σ_i,0)·φ_i` 로 인쇄돼 있고, 이 꼴은 보고값과 **역수** 관계다 (§4.3 검산표: 인쇄 꼴로는 τ² 가 전부 < 1).
   → 정확한 인용: *"Eq 4 (인쇄 꼴은 σ 비가 뒤집힌 오식) — 보고값은 τ_i² = φ_i·σ_i,0/σ_i,eff"*.  "선형 tortuosity 2.07" 은
   **원문이 쓰지 않는 수** (우리 √ 산술) 이고, 원문 Eq 3 의 기하 τ_i = l_i/l_0 (경로 길이비) 와 **다른 양**이다 — 원문은 Eq 3 을
   정의만 하고 측정하지 않는다 (§16).

**압력 구분 (인용 시 필수):**
- **압밀(fabrication) 압력 = 380 MPa** 단축 (dry mix, RT, 3 min). 우리 production 300 MPa cold-press와 같은 계열.
  - (separator SE 층만 100 MPa, 그 위 양극 적층 후 bilayer 전체 380 MPa로 consolidation.)
- **EIS 측정 압력 = ~40 MPa** (스택을 force sensor + spring으로 ~40 MPa 유지하며 측정). 이건 압밀압이 아니라
  *측정 중 접촉 유지*용. 우리가 σ를 비교할 땐 "**380 MPa로 압밀된 14 % porosity 구조를 ~40 MPa 하에서 측정**"이
  정확한 조건이다.
- (참고: cell cycling도 ~40 MPa 일정 압력.)
- ⟦10-03 PDF 대조⟧ **이온 측정 시료는 380 MPa 로 두 번 눌렸다** — 전자 측정 (steel 단자) 을 마친 셀을 분해해 복합체 양쪽에
  SE 분말 ~60 mg 씩 얹고 **전체를 다시 380 MPa, 3 min, RT** (p.3).  재압 뒤 두께를 다시 쟀는지는 [미확인] (42 vol% 의
  L = 470 µm 가 두 측정에 같이 쓰였는지 원문이 말하지 않는다).
- ⟦10-03 PDF 대조⟧ **σ_i,0 용 순수 시료**: 순수 SE 임피던스는 stainless steel 전극 · **약 40 MPa 측정압** (SI Fig S6 캡션).
  순수 시료 (SE · NCM) 의 **압밀압 · 두께 · 기공률은 본문·SI 어디에도 없다** [미확인].

**우리 다른 앵커들과의 분리(2022 리뷰 digest 결론 재확인):**
- "밀도 87 % @300 MPa" = **Sakuda 2013** (75Li₂S-25P₂S₅), 이 논문 아님.
- "pure-SE 10 % @300 MPa" = 우리 MPM 3D(σ_y 0.30) 수렴값 (Sakuda/이 논문 cold-press 거동 위에 보정).
  ⚠ **이 논문은 pure-SE porosity를 별도 측정하지 않는다** — 14 %는 *복합 양극* 값이다(아래 §3 주의).
  ⟦10-03 PDF 대조⟧ **SI 까지 확인해 확정**: SI §3 은 순수 SE·CAM 시료에도 기공이 *"있다고 가정해야 한다"* 고만 쓰고 값을 주지
  않는다.  "300 MPa" 라는 압력도 본문·SI 어디에도 없다 (압밀은 380 MPa, 분리층 100 MPa, 측정 ~40 MPa 뿐).  ⇒ CLAUDE.md 프레임
  [1] 의 *"pure-SE porosity ≈ 10 % @ 300 MPa (Minnmann et al.)"* 는 **이 논문 (2021 JES, SI 포함) 의 값이 아니다** — 출처
  [미확인] (규율 ⑥).

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
| SI ⟦10-03 PDF 대조⟧ | 10쪽 Word 문서 — §1 TLM (식 S1–S7, SI p.1–3) · §2 In/(InLi)ₓ 계면 (Fig S1, SI p.3) · §3 porosity (식 S8–S9 · Table S1 · Table S2, SI p.4–5) · §4 사이클 (Table S3 · Fig S2, SI p.5–6) · §5 VGCF (Table S4 · Fig S3, SI p.6–7) · §6 입경 (Fig S4–S6 · Table S5 ×2, SI p.8–9) · 참고문헌 5편 (SI p.10).  ⚠ 본문은 SI 를 **다른 번호**로 인용한다 (§10 대응표) |
| DC polarization 의 쓰임 ⟦10-03 PDF 대조⟧ | **순수 LPSCl 의 전자 전도도 (< 10⁻⁶ S/cm) 한 곳뿐** (p.3).  복합체의 σ_el,eff · σ_ion,eff 는 전부 EIS-TLM 이다 |

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
| LPSCl (NEI) | **이온 bulk σ** | **1.6 mS/cm @ 25 °C** | EIS 측정 (★ 우리 Cronau ~~단결정~~ 3.0 / Bazzoun pellet 1.02 / Lee 2.19 사이) · ⟦10-03 PDF 대조⟧ "단결정" 취소 = 원장 CL-91 (3.0 은 Cronau 2021 SI Fig. S2c µC-LPSCl **펠릿** 평탄부 하단).  이 1.6 이 Eq 4 의 **σ_ion,0** 다 — 본문 p.5 "Data for the individual materials was obtained from impedance spectroscopy of **pure samples**", Fig 2 캡션 "ionic bulk conductivity of the solid electrolyte is 1.6 mS cm⁻¹".  측정 조건 = stainless steel 전극 · ~40 MPa (SI Fig S6).  SI §3: 그 순수 시료에도 기공이 있지만 τ² := 1 로 두었다 ⇒ **펠릿 겉보기값** (기공·입계 포함) |
| LPSCl | **전자 bulk σ** | ~~**1×10⁻⁶ S/cm**~~ → **< 10⁻⁶ S/cm** ⟦10-03 PDF 대조⟧ 원문 "less than 10⁻⁶ S cm⁻¹" (p.3) — 값이 아니라 **상한** | DC polarization (이온의 ~~1600×↓~~ **> 1600×↓** → 전자 무시 가능) |
| LPSCl (fine) | 밀링 σ | 1.6 → **1.2 mS/cm** | wet-mill(heptane/dibutyl-ether 8:1, 30:1 media, 200 rpm, 10 h) 후 약간↓ (GB/분해) · ⟦10-03 PDF 대조⟧ 원문 조건 = Fritsch Pulverisette 7 · 20 min 밀링 + 10 min 휴지 × 30 회 (실밀링 10 h) · media:powder 30:1 wt · powder:solvent 9:1 wt (p.3).  1.2 의 근거 그림 = **SI Fig S6** (본문은 "Fig. S4" 로 인용, p.8).  원문 해석 = 용매와의 약한 분해 또는 추가 입계 기여 (p.8) / 약한 비정질화 또는 분해 (SI Fig S6 캡션).  입도: D50 **3.45 → 2.45 µm**, D90 **20.05 → 8.57 µm** (SI Table S5) |
| NCM-622 (BASF) | **전자 partial σ** | **10 mS/cm** | SI Table S2; 이온 σ는 무시(혼합전도 무시 단순화) · ⟦10-03 PDF 대조⟧ = Eq 4 의 **σ_el,0** (SI Table S2 "100 (nominal)" 행 1.00·10⁻² S/cm, τ_el² := 1).  **완전 리튬화 (0 % SoC)** 상태 값 (p.6 "fully lithiated NCM (10 mS cm⁻¹)"; 탈리튬화되면 더 오른다는 문헌 [46] 언급).  순수 시료 EIS (p.5) — 전극·압력·기공 조건 [미확인] |
| NCM-622 | D̄ | **3 µm** | 200 °C 진공 건조 |
| LPSCl | density | **1.87 g/cm³** | vol%↔wt% 변환용 |
| NCM-622 | density | **4.65 g/cm³** | ~~(다른 부분 4.65, 일부 4.77 표기 혼재)~~ ⟦10-03 PDF 대조⟧ 원문 (본문+SI) 의 밀도 표기는 **4.65 하나뿐**이다 ("4.77" 은 SI Table S2 의 τ_el² @ 53 vol% 값 — 옛 메모는 착오로 보인다).  단 **SI Table S1 의 V_theo 열은 ρ_NCM ≈ 4.77 로만 재현**되고 (4.65 면 37.49 / 34.29 / 31.10 / 27.90 / 25.98 mm³ ≠ 표 37.2 / 33.9 / 30.7 / 27.4 / 25.5), φ_i 와 τ² 는 4.65 로 재현된다 — 원문 내부 불일치 (내 산술, §17 #8) |

### 2.2 셀 구성 (병목 분리의 핵심 = 차단전극 선택)
복합 양극은 이온(SE)·전자(CAM) 두 경로가 동시에 흐른다. 한쪽만 보려면 **반대쪽을 막는 대칭셀**:
- **전자 측정** → **이온-차단(ion-blocking) 셀**: steel | 복합양극 | steel (양 끝 stainless steel = 이온 막음).
- **이온 측정** → **전자-차단(electron-blocking) 셀**: In/(InLi)ₓ | LPSCl | 복합양극 | LPSCl | In/(InLi)ₓ
  (LPSCl 층이 전자 막음, In/InLi = Li reservoir + ~~low-viscosity polarization~~).
  ⟦10-03 PDF 대조⟧ 원문은 "used as lithium reservoirs and **to avoid low-frequency polarization**" (p.3) — "low-viscosity" 는
  오전사.  In/(InLi)ₓ = In 박 100 µm·⌀9 mm (99.999 %) + Li 박 120 µm·⌀6 mm 압착, x ≈ 0.3 (p.3).
- 셀 제작: 분말 100 mg(전도도용) → ⌀10 mm 다이 → **단축 380 MPa, 3 min, RT**.
  ⟦10-03 PDF 대조⟧ PEEK 셀 (내경 10 mm), steel 봉 단자 (p.3).  **이온 측정 시료** = 전자 측정을 끝낸 같은 복합체 펠릿에 SE
  ~60 mg 씩 양면 추가 → **380 MPa 3 min 재압** (§0 압력 구분 참조).
  ASSB(cycling)용: SE 60 mg를 100 MPa로 separator(~~~200–380 µm~~ → **~200–300 µm** ⟦10-03 PDF 대조⟧ 원문 "approximately
  200–300 μm", p.3) 압밀 → 양극 12 mg(15.3 mg/cm², ~~214 mAh/cm²~~) 적층 → **bilayer 전체 380 MPa, 3 min**.
  ⟦10-03 PDF 대조⟧ 원문 인쇄 "a CAM loading of **214 mAh cm⁻²**" (p.3) 는 **2.14 mAh cm⁻² 의 오식** — SI Table S3 의 42 vol%
  행 = 10.7 mg_NCM/cm² · **2.14 mAh/cm²** (12 mg × 0.70 / 0.785 cm² × 200 mAh/g = 2.14, 내 산술).  조성별 면적용량은
  1.83 – 2.62 mAh/cm² (SI Table S3, §10-SI).  15.3 mg/cm² = 12 mg / 0.785 cm² (복합체 기준).

### 2.3 EIS / cycling 조건
- EIS: Biologic VMP-300, 10 mV, **7 MHz–50 mHz**, **측정압 ~40 MPa** (force sensor + spring으로 압력완화 보상),
  RELAXIS-3 피팅, Kramers-Kronig stationarity 검증.
- Cycling: MACCOR, 25 °C, 일정전류, **~40 MPa**, theoretical capacity 200 mAh/g 가정, C-rate 0.1/0.25/0.5/1 C.
  ⟦10-03 PDF 대조⟧ 조건마다 **셀 2 개** (p.3).  전압창은 본문에 없다 — SI Fig S2 축 판독 ≈ **2.6–4.3 V** (축 표기 "vs. Li⁺/Li")
  [판독].  EIS 측정 온도는 "room temperature" (p.3), σ_ion,0 은 25 °C (p.3).
- CAM vol% 범위: **25–61 vol%** (전도도), cycling은 ~~33/42/52/53/61 vol%~~.
  ⟦10-03 PDF 대조⟧ 사이클 셀 = **33 / 42 / 47 / 58 / 61 vol%** (SI Table S3 · SI Fig S2 패널 제목 · Fig 3 데이터 위치).
  Fig 5 범례의 "53 vol.-%"(왼쪽) / "52 vol.-%"(오른쪽) 계열은 1C 전류밀도 ≈ 2.3 mA/cm² 와 비용량이 **47 vol% 셀**
  (Table S3 면적용량 2.29 mAh/cm², Fig 3) 과 같다 → 범례 오기로 판단 (§17 #14).  ⚠ **전도도 시료 (25/33/42/53/61) 와 사이클 셀
  (33/42/47/58/61) 은 조성 집합이 다르다** — 겹치는 것은 33 · 42 · 61 뿐.

---

## §3. ★ POROSITY (우리 1번 앵커)

- **avg 14 %** : 본문 p.5 — vol% 계산 시 "an average porosity of 14 % is assumed" (Fig 2 vol% 변환의 기준 가정).
  ⟦10-03 PDF 대조⟧ 14 % = SI Table S1 의 **다섯 시료 실측값의 평균** (표 각주; 7.6/13/17/17/15 → 13.9).  이 평균을 식 S9
  `Φ_i = (1 − Φ_Porosity)·Φ_i,nom` (SI p.4) 에 **모든 조성 공통으로** 넣었다 — 시료별 값이 아니다.  (SI 본문은 "using an average
  **density** of 14 % (Equation S8)" 로 썼는데 문맥상 porosity · 식 S9 의 오식, §17 #19.)
- **13–17 % range** : Conclusions/recommendations(p.9) — "composite cathodes prepared by a dry mixing process
  with subsequent uniaxial consolidation exhibit a ~~typical~~ porosity of **13 %–17 %** (Table SIII), which is
  comparable to values reported in literature." (~~Sakuda 등 계열~~).
  ⟦10-03 PDF 대조⟧ 원문 낱말은 "**a high porosity** of 13 %–17 %" (p.9) 이고 비교 문헌은 **[43] Hlushkou et al. 2018** 이다
  ("Sakuda 등 계열" 은 원문 근거 없음).  "Table SIII" = **SI Table S1** 이며 그 표의 시료별 값은 **7.6 · 13 · 17 · 17 · 15 %**
  → 본문의 "13–17 %" 는 **25 vol% (50:50 wt) 시료의 7.6 % 를 뺀 범위**다 (§17 #6).
- ⟦10-03 PDF 대조⟧ **기공 정의와 오차** (SI §3, SI p.4): `Φ_Porosity = (V_meas − V_theo) / V_meas` (식 S8) — V_meas 는 측정 두께
  × 면적, V_theo 는 질량/밀도.  원문: *"All determined porosities are susceptible to errors, as high as 10 %, due to the
  inaccurate determination of the composite cathode thickness."* (상대/절대 여부 불명 [미확인]).  V_theo 열은 ρ_NCM ≈ 4.77 로만
  재현된다 (§2.1) — 본문 밀도 4.65 를 쓰면 시료별 기공이 7.0 / 12.1 / 15.7 / 15.2 / 12.8 % (평균 12.6 %) 가 된다 (내 산술).
  ⇒ **"14 %" 자체가 밀도 가정에 ±1–2 %p 민감**하다.
- 조건: **dry mixing(agate mortar 15 min) + 단축 380 MPa**. (= 우리 production cold-press 300 MPa와 같은 계열,
  약간 더 높은 압력.)
- porosity의 의미(논문 자체 강조): porosity는 **부피 에너지/출력 밀도뿐 아니라 이온·전자 전달 둘 다 차단** →
  낮은 유효 전도도 + 높은 tortuosity의 직접 원인. **"porosity를 최대한 줄여라"** 가 첫 번째 최적화 권고
  (~~cold/~~warm isostatic press로 single-digit porosity 가능 — Lee et al. 인용; 또는 저점도 액/폴리머 침투).
  ⟦10-03 PDF 대조⟧ 원문은 **warm-isostatic pressing 만** 언급한다 ("Lee et al. demonstrated that this approach can result in low
  single-digit porosity values", [59] Y.-G. Lee et al., Nat. Energy 5, 299 (2020), p.9) — "cold" 는 원문에 없다.

⚠ **주의 (인용 정밀도)**:
- 이 14 %·13–17 %는 **복합 양극(NCM+LPSCl) 전체 porosity** 이다. **pure-SE porosity 아님.**
  우리 "pure-SE ~10 % @300" 은 이 논문이 주는 값이 아니라 우리 MPM 수렴값(+Sakuda 87 % 밀도).
- 14 %는 일부 맥락에서 *vol% 계산용 가정값*, ~~13–17 %는 *실측 range*~~. 둘 다 같은 dry-380MPa 공정.
  ⟦10-03 PDF 대조⟧ 실측 range 는 **7.6–17 %** (SI Table S1); "13–17 %" 는 본문 요약 문구.  14 % 는 그 실측 다섯의 평균을
  공통 가정값으로 쓴 것.
- 압밀 380 MPa ≠ 측정 40 MPa ≠ 작동압. porosity는 **380 MPa 압밀** 결과다.
- ⟦10-03 PDF 대조⟧ **기공 가정이 τ² 에 주는 민감도** (내 산술): 평균 14 % 대신 시료별 기공을 넣으면 τ_ion² = 2.58 / 3.26 /
  4.13 / 14.8 / 128 (보고 2.40 / 3.23 / 4.27 / 15.3 / 130 — 차이 −3.5 ~ +7.4 %).  결론은 바뀌지 않는다.
- ⟦10-03 PDF 대조⟧ fine-SE 복합체 (61 vol%) 의 기공은 **따로 재지 않았다** — 같은 평균 14 % 로 φ 를 잡았다 (SI Table S2 의
  φ_SE 25 % 그대로).  §9.2 의 "입경 효과 = tortuosity" 해석에 걸리는 단서.

---

## §4. ★ EIS-TLM 방법 (우리 네트워크 솔버 + τ_Laplace,eff 의 실험 아날로그)

### 4.1 왜 단순 병렬회로가 안 되나
복합 양극은 여러 상·여러 전하경로가 **공간적으로 분포**해 흐른다. 단순 R∥C 병렬조합으로 안 됨 →
다공막의 물질수송에 쓰는 **transmission-line-model(TLM, "T-type")** 사용 (Siroma et al. 유도, Eq 1).

### 4.2 TLM 임피던스 (Eq 1, Siroma "open-open")

⟦10-03 PDF 대조⟧ ⚠ 아래 **옛 전사 블록의 둘째 항은 원문과 다르다** (`√z_ion` → 원문 `√z_int` · 분모 지수 `2` → 원문 `3/2`).
원문 그대로 (본문 p.4 식 [1] = SI p.2 식 (S1), 두 곳 모양 같음):
```
Z_CC(ω) = (z_ion·z_el)/(z_ion + z_el) · L
        + [ 2·z_el²·√z_int / (z_ion + z_el)^(3/2) ]
          · [ cosh( L·√((z_ion + z_el)/z_int) ) − 1 ] / sinh( L·√((z_ion + z_el)/z_int) )          [1] = (S1)
```
SI §1 의 나머지 식 (SI p.2–3, 원문 그대로):
```
z_ion    = r_ion                                                  (S2)  이온 경로 = 저항 하나 ("ionic bulk resistance of the SE")
z_el     = z_el,bulk + z_el,int                                   (S3)
z_el,int = r_el,int / (1 + r_el,int·(jω·Q_el,int)^α_el,int)       (S4)  NCM–NCM 입자 접촉의 R-CPE
z_int    = 1 / (jω·Q_int)^α_int                                   (S5)  CAM|SE 계면 = CPE (non-faradaic, 완전 리튬화)
R_el     = L·(r_el,bulk + r_el,int)                               (S6)  ★ NCM–NCM 접촉저항 포함
R_ion    = L·r_ion                                                (S7)
```
- ★ 식 S6 ⇒ **R_el (→ σ_el,eff → τ_el²) 은 입자 접촉저항 r_el,int 을 포함**한다.  식 S2·S7 ⇒ 이온 쪽은 저항 하나라 SE–SE
  접촉·입계 저항도 **r_ion 안에 뭉쳐** 들어간다.  ⇒ 두 τ² 모두 접촉·협착을 품은 **수송 유도 값**이다 (§4.3 · §16).
- 단위 표기 혼선 (원문 그대로 옮김): 본문 p.4 는 z_el · z_ion [Ω m], z_int [Ω m⁻¹]; SI 는 r_ion (Ω m), r_el,bulk · r_el,int
  (Ω m⁻¹).  식 S6–S7 (R = L·r) 이 성립하려면 r 은 Ω m⁻¹ 이어야 하고, 식 S1 의 L·√((z_ion+z_el)/z_int) 가 무차원이려면 z_int 는
  Ω m 이어야 한다 → 원문 단위 라벨은 서로 맞지 않는다 (§17 #16).  계산에는 영향 없음.

(옛 전사 — 둘째 항 틀림, 이력 보존:)
```
Z_CC(ω) = z_ion·z_el/(z_ion+z_el)·L
        + 2·z_el²·√z_ion / (z_ion+z_el)²
          · [ cosh(L·√((z_ion+z_el)/z_int)) − 1 ] / sinh(L·√((z_ion+z_el)/z_int))
```
- **z_el** [Ω m] = 전자 전도상(CAM) 단위길이 임피던스, **z_ion** [Ω m] = 이온 전도상(SE), **z_int** [Ω m⁻¹] =
  두 상 사이 계면 임피던스. **L** [m] = 복합 양극 두께.
- 등가회로(Fig 1): z_el = (r_el,1, r_el,2, CPE_el) — r_el,1 = 전자 bulk, r_el,2 = 계면 전하전달; z_ion = r_ion;
  z_int = CPE_int. 계면은 **non-faradaic** 가정(fully-lithiated NCM = 확산제한 → 높은 전하전달저항).
  ⟦10-03 PDF 대조⟧ r_el,2 의 정체를 원문 두 곳이 다르게 쓴다 — 본문 Fig 1 캡션 "interfacial **charge transfer**" vs SI §1
  "interfacial impedance **at the NCM-NCM particle contacts**" (표면 오염·제조 중 열화 기원 접촉저항, SI p.2–3) (§17 #18).
  수식 (S3–S4) 상으로는 전자 경로 안의 NCM–NCM 접촉 R-CPE 다.
- 피팅으로 **R_el, R_ion** 추출. (이온/전자 차단 셀에서 z_ion↔z_el 역할 교환.)
  ⟦10-03 PDF 대조⟧ 이온 측정 (전자 차단 셀) 의 보정: 고주파 실축 오프셋 = **SE 분리층 저항**, In/(InLi)ₓ|LPSCl 계면 기여는
  In/(InLi)ₓ|LPSCl|In/(InLi)ₓ 대칭셀로 따로 정했다 (본문 p.5 는 "Fig. S3" 로 인용하나 실제는 **SI Fig S1**; 그 적합값은 두 계면
  합이라 R 은 단일 계면의 2 배 · C 는 1/2, SI §2).  RelaxIS 3 적합 · Kramers-Kronig 로 정상성 검사 후 주파수 범위 조정 (p.3).

### 4.3 유효 전도도 & tortuosity (Eq 2–4) ★ 우리와 1:1 대응
```
σ_i,eff = L / (R_i · A)                                    [Eq 2]   (실린더 양극, A=단면적)
τ_i     = l_i / l_0   (최단경로/직선거리, 기하 정의)         [Eq 3]
τ_i²    = (σ_i,eff / σ_i,0) · φ_i                          [Eq 4]   ★ 보고값 = τ², 우리 τ_Laplace,eff와 대응
                                                   ⟦10-03 PDF 대조⟧ ↑ 원문 인쇄 그대로 — 그러나 보고값은 이 식의 역수 꼴로만 나온다 (아래)
보고값을 재현하는 꼴:  τ_i² = φ_i · σ_i,0 / σ_i,eff       ⟦10-03 PDF 대조⟧ (= σ_i,eff = σ_i,0 · φ_i / τ_i²)
```
⟦10-03 PDF 대조⟧ **세 식의 원문 위치**: 전부 본문 p.5 — [2] `σ_i,eff = L/(R_i A)` · [3] `τ_i = l_i/l_0` ("The geometric tortuosity
τ_i of a trajectory is the ratio of the length of the shortest charge transport pathway l_i to the shortest distance l_0 between two
points") · [4] `τ_i² = (σ_i,eff/σ_i,0) φ_i` ("the tortuosity factor τ_i² can be calculated according to Eq. 4,⁶ using the respective
effective partial conductivity σ_i,eff, the partial (bulk) conductivity σ_i,0 and the volume fraction φ_i of the respective material").

⟦10-03 PDF 대조⟧ **인쇄 Eq 4 는 보고값과 맞지 않는다** — 같은 입력으로 두 꼴을 계산한 결과 (내 검산; φ_i = 식 S9 를 ρ_NCM 4.65 ·
ρ_SE 1.87 · 기공 14 % 로 재계산, σ_ion,0 = 1.6·10⁻³, σ_el,0 = 1.0·10⁻² S/cm, σ_eff = SI Table S2):

| φ_NCM 표기 % | 보고 τ_el² | φσ₀/σ_eff | 인쇄 꼴 (σ_eff/σ₀)·φ | 보고 τ_ion² | φσ₀/σ_eff | 인쇄 꼴 (σ_eff/σ₀)·φ |
|---|---|---|---|---|---|---|
| 25 | 120 | 119.7 | 0.00051 | 2.40 | 2.405 | 0.156 |
| 33 | 13.7 | 13.71 | 0.0076 | 3.23 | 3.227 | 0.089 |
| 42 | 7.44 | 7.488 (본문 R 로는 7.440) | 0.023 | 4.27 | 4.276 (본문 R 로는 4.268) | 0.046 |
| 53 | 4.77 | 4.778 | 0.059 | 15.3 | 15.29 | 0.0071 |
| 61 | 4.29 | 4.281 | 0.088 | 130 | 129.6 | 0.00047 |
| 61 (fine SE) | 8.79 | 8.783 | — | 33.8 | **33.89 (σ₀ = 1.6) / 25.42 (σ₀ = 1.2)** | — |

⇒ **보고 τ² 는 전부 `τ_i² = φ_i·σ_i,0/σ_i,eff` 로 재현되고, 인쇄 꼴로는 하나도 재현되지 않는다 (전부 < 1).**  최대 차 0.65 % (42 vol% 전자, Table S2 의
반올림된 σ_eff 로 계산할 때 — 본문 R 값으로 계산하면 7.440 으로 일치).  인쇄 Eq 4 는
σ 비가 뒤집힌 **오식**으로 판단한다 (§17 #1).  Eq 4 가 인용한 [6] Bielefeld 2020 의 정본 카드
(`bielefeld2020_effective_ionic_conductivity_binder`) 는 그 논문 식 (3)·(11) 을 `σ_eff,ion = (ε_SE/τ²)·σ_bulk,SE` ⇒
`τ² = (σ_bulk,SE/σ_eff,ion)·ε_SE` 로 기록한다 — 보고값과 같은 꼴 (그 카드 기준; 이 카드에서 Bielefeld 원문은 대조하지 않았다).
- 42 vol% 를 본문 숫자만으로 재현: σ_el,eff = 0.047 cm / (107 Ω × 0.785 cm²) = **5.596·10⁻⁴**, σ_ion,eff = 0.047 / (360 × 0.785) =
  **1.663·10⁻⁴ S/cm**; φ_NCM = 0.4163 · φ_SE = 0.4437 ⇒ τ_el² = **7.440** · τ_ion² = **4.268** (보고 7.4 / 4.3, Table S2 7.44 / 4.27) ✓.
  A = 0.785 cm² = π·(0.5 cm)² = ⌀10 mm 다이 전체 단면.
- fine-SE 행의 τ_ion² 33.8 은 **pristine σ₀ = 1.6 mS/cm 로만 재현**된다 — 밀링 SE 자신의 1.2 mS/cm (SI Fig S6) 로 하면 25.4.
  원문은 fine-SE 복합체도 **pristine SE 기준으로 정규화**했다 (원문에 그 선택의 서술은 없다; §9.2 · §17 #17).
- ⟦10-03 PDF 대조⟧ **σ_i,eff 정규화 기준 = 전극 전체 단면.**  식 [2] 의 A 는 "geometrical thickness L and area A of the cylindrical
  composite cathode" (p.5) — 상 (phase) 단면이 아니다.  φ_i 는 식 [4] 에서 **따로** 곱한다 ⇒ `σ_eff = σ₀·φ/τ²` 관례 = 우리
  `σ_eff = G·T/A` (A = box_x·box_y 전체, `network_conductivity.py:850–857`) 와 같은 관례.  (원문의 말 "describes the average
  conductivity of the charge transporting material in this configuration" 은 상 기준처럼 들리지만, 계산은 전체 단면이다.)
- **Eq 4 = 우리 τ_Laplace,eff 의 실험 정의.** σ_i,eff(유효) / σ_i,0(bulk) / φ_i(부피분율) 로부터 τ²를 역산.
  우리 솔버가 Kirchhoff/Laplace로 σ_eff를 풀고 τ_eff = √(σ_0·φ/σ_eff) 로 뽑는 것과 **수학적으로 동일**.
  ⟦10-03 PDF 대조⟧ "수학적으로 동일" 은 **보고값 기준 꼴 (φσ₀/σ_eff) 에 대해서만** 참이다 — 인쇄 꼴과는 역수.  또 σ_i,0 의 뜻이
  다르다: 원문 = **순수 시료 펠릿의 측정값** (기공·입계 포함, τ² := 1, SI §3), 우리 = **망 간선의 σ_grain** (3.0 mS/cm @25 °C) 이고
  우리 τ 에서는 σ_full 의 같은 σ_grain 과 **약분**된다 (§16).
- 단, Eq 4 τ는 **current constriction / CEI / interface polarization / space-charge를 무시** → "geometric"
  tortuosity와 다를 수 있음(논문 명시). 우리 Holm 구속저항(Stage-E)이 바로 그 constriction을 일부 포함 →
  비교 시 ~~**그들 τ는 constriction 미포함**~~, 우리 τ_Laplace는 솔버에 따라 포함/미포함 명시 필요.
  ⟦10-03 PDF 대조⟧ 취소 사유 — **반대로 읽었다.**  원문 (p.5): *"This equation neglects the effects originating from current
  constriction, cathode-electrolyte-interphase (CEI) formation, interface polarization, and space charge layers. Therefore, the
  determined tortuosity factor might deviate from the 'true' geometrical tortuosity factor."*  σ_i,eff 는 **측정값**이라 그 효과들을
  이미 다 겪었다; Eq 4 가 그것들을 따로 떼지 않으니 **전부 τ² 에 흡수**된다 → 보고 τ² ≥ "참 기하" τ² 쪽으로 치우친다.  게다가
  식 S6 의 R_el 은 NCM–NCM 접촉저항을 **명시적으로** 포함한다 (§4.2).  ⇒ 그들 τ² 는 **협착·접촉 포함 수송 τ²** = 우리
  **τ_Lap,eff** (σ_full, Holm 협착 포함) 와 같은 범주; 우리 **τ_Lap,geom** (σ_bulk_net, 협착 제외) 은 원문에 짝이 없다.

### 4.4 핵심 측정값 (42 vol% NCM 기준점 — 우리 2·3번 앵커)
대표 셀: **42 vol% NCM**, 두께 **L = 470 µm**, 단면적 **A = 0.785 cm²**.
- **R_el = 107 Ω, R_ion = 360 Ω** (TLM 피팅).
- → **σ_el,eff = 5.6×10⁻⁴ S/cm = 0.56 mS/cm**, **σ_ion,eff = 1.7×10⁻⁴ S/cm = 0.17 mS/cm** ★.
- → **τ_el² = 7.4, τ_ion² = 4.3** ★ (즉 **τ_ion = 2.07**, τ_el = 2.72).
  ⟦10-03 PDF 대조⟧ 본문 p.5 의 값 그대로 ✓.  SI Table S2 정밀값 **7.44 / 4.27** (√ = 2.73 / 2.07 — √ 는 우리 산술).  재계산은
  §4.3 표 (본문 R 로 7.440 / 4.268).
- 해석: 42 vol%서 σ_ion,eff(0.17)는 LPSCl bulk(1.6)의 **약 1/10(≈4×아님, 본문 "about four times lower"는
  ~~다른 맥락~~; 실제 1.6/0.17 ≈ 9.4×)**. 그래도 0.17 mS/cm는 β-Li₃PS₄ bulk 수준이라 124 mAh/g cell 구동 가능.
  ⟦10-03 PDF 대조⟧ "다른 맥락" 취소 — 원문 (p.5) 은 **바로 이 42 vol% 에 대해** "At approx. 42 vol.-% CAM the effective ionic
  conductivity of the composite is about four times lower than the ionic conductivity of the bulk solid electrolyte" 라고 쓴다.
  실제 비는 1.6 / 0.1663 = **9.6×** 이고, "4" 는 φ_SE 로 나눈 뒤의 **τ² (= 4.27)** 와 맞는다 ⇒ **원문 문장의 오류** (σ_eff/σ₀ 와
  σ_eff/(φσ₀) 를 혼동, §17 #2).  124 mAh/g 는 [44] Koerver 2017 의 β-Li₃PS₄ 셀 값 (p.5).

---

## §5. ★ CAM vol% 스윕 (Fig 2) — 우리 AM:SE 스윕 + percolation 대응

Fig 2a = σ_i,eff·σ_el,eff vs φ_NCM(0–100 %); Fig 2b = τ_i² vs φ_NCM. (avg porosity 14 % 가정; dashed=eye-guide.)

### §5.0 ⟦10-03 PDF 대조⟧ ★ τ² 정본 표 — SI Table S2 원값 (아래 옛 표의 "~" 판독값을 대체)

**조건 (전 행 공통)**: 건식 혼합 (마노 유발, 손 15 min) 100 mg · ⌀10 mm PEEK 셀 · **380 MPa 3 min RT** (이온 시료는 SE 층을 붙여
380 MPa 한 번 더) · **EIS** 7 MHz–50 mHz · 10 mV · RT · **~40 MPa** · T-type TLM (식 1 / S1–S7) · 전자 = ion-blocking (steel |
복합체 | steel) · 이온 = electron-blocking (In/(InLi)ₓ | LPSCl | 복합체 | LPSCl | In/(InLi)ₓ) · σ_i,eff = L/(R_i A) (전체 단면) ·
φ_i = (1 − 0.14)·φ_i,nom (식 S9) · σ_ion,0 = **1.6 mS/cm** (순수 SE, 25 °C) · σ_el,0 = **10 mS/cm** (순수 NCM, 0 % SoC) · 순수 재료
τ² := 1 (SI §3) · τ_i² = φ_i σ_i,0 / σ_i,eff (보고값 기준 꼴, §4.3).  **전 값 stated (SI Table S2, SI p.5)** — 질량비·시료 기공은
SI Table S1 (SI p.4).

| φ_NCM % | φ_SE % | m_NCM : m_SE (mg) | 시료 기공 % (S1) | σ_el,eff / S cm⁻¹ | **τ_el²** | σ_ion,eff / S cm⁻¹ | **τ_ion²** |
|---|---|---|---|---|---|---|---|
| 0 | 100 (nominal) | — | — | — | — | 1.60·10⁻³ | 1.00 (정의) |
| 25 | 61 | 50 : 50 | 7.6 | 2.06·10⁻⁵ | **120** | 4.08·10⁻⁴ | **2.40** |
| 33 | 53 | 60 : 40 | 13 | 2.36·10⁻⁴ | **13.7** | 2.66·10⁻⁴ | **3.23** |
| **42** | **44** | **70 : 30** | 17 | **5.56·10⁻⁴** | **7.44** | **1.66·10⁻⁴** | **4.27** |
| 53 | 33 | 80 : 20 | 17 | 1.11·10⁻³ | **4.77** | 3.45·10⁻⁵ | **15.3** |
| 61 | 25 | 86 : 14 | 15 | 1.43·10⁻³ | **4.29** | 3.06·10⁻⁶ | **130** |
| 61 | 25 (fine SE) | 86 : 14 | [미측정] | 6.97·10⁻⁴ | **8.79** | 1.17·10⁻⁵ | **33.8** |
| 100 (nominal) | 0 | — | — | 1.00·10⁻² | 1 (정의) | — | — |

**환산 열 — 내 산술** (원문에 없는 수; φ 는 식 S9 재계산, f = σ_eff/σ₀, N_M = σ₀/σ_eff = "MacMullin 수" — 원문에 없는 이름 ·
√τ² 는 원문이 쓰지 않는 수 · Bruggeman τ_F = φ^(−1/2) 는 §16 의 COMSOL 대조용):

| 조성 (φ_NCM 표기) | φ_NCM 재계산 | φ_SE 재계산 | √τ_ion² | f_ion | N_M,ion | τ_ion² ÷ φ_SE^(−½) | √τ_el² | f_el | N_M,el | τ_el² ÷ φ_NCM^(−½) |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 0.2467 | 0.6133 | 1.55 | 0.255 | 3.92 | 1.88× | 10.95 | 0.00206 | 485 | 59.6× |
| 33 | 0.3236 | 0.5364 | 1.80 | 0.166 | 6.02 | 2.37× | 3.70 | 0.0236 | 42.4 | 7.8× |
| **42** | **0.4163** | **0.4437** | **2.07** | **0.104** | **9.64** | **2.84×** | **2.73** | **0.0556** | **18.0** | **4.8×** |
| 53 | 0.5303 | 0.3297 | 3.91 | 0.0216 | 46.4 | 8.8× | 2.18 | 0.111 | 9.01 | 3.5× |
| 61 | 0.6122 | 0.2478 | 11.40 | 0.00191 | 523 | 64.7× | 2.07 | 0.143 | 6.99 | 3.4× |
| 61 fine SE | 0.6122 | 0.2478 | 5.81 | 0.00731 | 137 | 16.8× | 2.96 | 0.0697 | 14.3 | 6.9× |

- ★ **"2.07" 이 두 번 나온다** — 42 vol% 이온 √4.27 = 2.07 과 61 vol% 전자 √4.29 = 2.07.  인용할 때는 상 (이온/전자) 과 조성을
  반드시 같이 쓴다.
- 표기 정수 vol% 는 반올림 표지다 — 역산에 실제로 쓰인 φ 는 재계산 열 (33 vol% 행은 재계산 32.4 / 53.6 인데 표기는 33 / 53,
  합 86 을 맞춘 반올림으로 보임 — §17 #9).
- 본문 서술값과 대조: "τ_ion² ≈ 2.4 (25) → ≈ 15.3 (53)" (p.6) ✓ · "≈ 130 (61)" (p.7) ✓ · "τ_el² 120 (25) → ≈ 4.3 (61)" (p.6) ✓ ·
  "fine SE ≈ 34" (p.9) ✓ · "σ_el,eff 2.1·10⁻⁵ → 2.4·10⁻⁴ (25 → 33)" (p.6) ✓ · ⚠ "42 vol% 의 전자 τ² 는 **above eight**" (p.6) ✗ —
  표는 7.44, 본문 p.5 도 7.4 (§17 #3).
- Fig 2b 의 오차막대는 원문에 정의가 없다 [미확인] (SI 는 porosity 오차 "최대 10 %" 만 언급).  전도도 측정의 반복 수도 [미확인]
  (사이클만 "two ASSB cells" 명시).
- 교차점 (Table S2 기준): **σ** 는 33 vol% 에서 이미 거의 같다 (σ_ion 2.66·10⁻⁴ vs σ_el 2.36·10⁻⁴) → σ 교차 ≈ 33–42 vol%;
  **τ²** 교차는 42 (4.27 vs 7.44) 와 53 (15.3 vs 4.77) 사이.  사이클 최적 (Fig 3) 은 42 vol%.

(옛 표 — 아래. ⟦10-03 PDF 대조⟧ 표지가 붙은 칸은 SI Table S2 와 다르던 판독값이다.)

| φ_NCM (vol%) | σ_ion,eff (S/cm) | σ_el,eff (S/cm) | τ_ion² | τ_el² | 비고 |
|---|---|---|---|---|---|
| 0 (pure SE) | ~1.6×10⁻³ (=bulk) | — | ~1 | — | τ→1 (순수상) · ⟦10-03 PDF 대조⟧ S2: 1.60·10⁻³, τ² = 1.00 은 **정의로 1** (SI §3) |
| 25 | ~~~1.4×10⁻³ (높음)~~ **4.08·10⁻⁴** ⟦10-03 PDF 대조⟧ | ~2.1×10⁻⁵ (낮음) (S2: 2.06·10⁻⁵) | **~2.4** (S2: 2.40) | **~120** (S2: 120) | ★ 전자 percolation 거의 끊김(τ_el²=120!) |
| 33 | ↓ (S2: 2.66·10⁻⁴) | ~2.4×10⁻⁴ (+1 order) (S2: 2.36·10⁻⁴) | ↑ (S2: 3.23) | ↓ (S2: 13.7) | 25→33서 σ_el **10×↑** (Eq: 2.1e-5→2.4e-4) |
| **42** | **1.7×10⁻⁴** (S2: 1.66·10⁻⁴) | **5.6×10⁻⁴** (S2: 5.56·10⁻⁴) | **4.3** (S2: 4.27) | **7.4** (S2: 7.44) | ★ **우리 앵커**; ~~이온≈전자 교차점 부근~~ ⟦10-03 PDF 대조⟧ σ 교차는 33–42 사이 (33 에서 이미 거의 같음), τ² 교차는 42–53 사이 |
| 53 | ↓↓ (S2: 3.45·10⁻⁵) | ↑ (S2: 1.11·10⁻³) | **~15.3** (S2: 15.3) | ↓ (S2: 4.77) | 이온 tortuosity 급등 |
| 61 | ~~~1×10⁻⁶ 수준~~ **3.06·10⁻⁶** ⟦10-03 PDF 대조⟧ | ~~~1×10⁻³~~ **1.43·10⁻³** ⟦10-03 PDF 대조⟧ | ~~매우 큼~~ **130** ⟦10-03 PDF 대조⟧ (S2 · 본문 p.7) | **~4.3** (S2: 4.29) | 전자 충분(τ_el²=4.3), 이온 병목 극심 |
| 100 (pure NCM) | — | ~~~7×10⁻³ (=bulk 10 mS/cm)~~ **1.00·10⁻²** ⟦10-03 PDF 대조⟧ (Fig 2a 의 점이 10⁻² 눈금 아래로 그려져 생긴 판독 오차 — 정본은 S2) | — | ~1 (S2: 1, 정의) | τ→1 |

**추세(우리와 직접 비교 가능):**
- **CAM↑ → σ_ion,eff↓, σ_el,eff↑** (정확히 역방향). 우리 AM:SE 스윕(AM↑→σ_ionic↓)과 **같은 방향**.
- **τ_ion² : 25 vol%서 ~2.4 → 53 vol%서 ~15.3** (단조 증가; CAM이 SE 경로를 막을수록 이온 우회로 길어짐).
- **τ_el² : 25 vol%서 ~120(거의 절연) → 61 vol%서 ~4.3** (단조 감소; CAM이 전자망을 채울수록 직선화).
- **σ_ion,eff·σ_el,eff 모두 10⁻⁶–10⁻³ S/cm 범위** (25–61 vol%).
- **교차(crossover)**: 저-CAM서 σ_ion > σ_el (이온 풍부, 전자 빈약); 고-CAM서 σ_el > σ_ion (반대).
  ~~≈ 42 vol% 부근이 균형점.~~
  ⟦10-03 PDF 대조⟧ SI Table S2 로 보면 **σ 교차는 33–42 vol% 사이** (33 에서 2.66·10⁻⁴ vs 2.36·10⁻⁴ — 거의 같음), **τ² 교차는
  42–53 vol% 사이**.  "42 vol% = 균형" 은 σ 교차가 아니라 **사이클 비용량 최적** (Fig 3, 154 mAh/g @0.1C) 의 위치다.

★ **우리 percolation-failure-at-SE-poor (Park 2020 90 wt%) 와 대응**: 저-CAM(25 vol%)서 τ_el²=120 =
**전자 percolation 거의 실패** → 이게 carbon이 필요한 이유. 우리 σ_e 폼의 φ_AM⁴ + percolation(f_p) 항이 잡는 영역.
⟦10-03 PDF 대조⟧ **짝이 어긋나 있다**: 25 vol% 는 **CAM-poor (= SE-rich)** 쪽의 **전자** 경로 붕괴다.  이 카드가 쓴 "SE-poor
(Park 2020 90 wt%)" 에 대응하는 이 논문의 점은 **61 vol% 의 이온 붕괴 (τ_ion² = 130, σ_ion,eff 3.06·10⁻⁶)** 다.  (Park 2020 원문은
이 카드에서 대조하지 않았다 — 정본 카드 `park2020_digitaltwin_assb_foundational` 참조.)  25 vol% 의 τ_el² 120 이 대응하는 우리 쪽은
σ_e 폼의 **저-φ_AM 끝** — 그 폼은 φ_AM < 0.3 외삽 금지 (CLAUDE.md G4 가드) 이고, 25 vol% 의 φ_NCM = 0.247 은 **그 금지 구역 안**이다.

---

## §6. CAM vol% × cycling 비용량 (Fig 3) — 병목의 cell-level 발현

- Fig 3 = 비용량 q vs φ_NCM(0–100 %) / w_NCM(0–100 %), 0.1/0.25/0.5/1 C, composite-specific(위)·CAM-specific(아래).
- **둘 다 inverse-U-shape** → **최적 CAM vol%가 중간(저·고 양 끝 사이)에 존재**.
- 33 vol% NCM: CAM-specific **137 mAh/g @0.1C → 83 @1C** (−40 %).
- 61 vol% NCM: **132 @0.1C → 16 @1C** (−88 %, 고-CAM이 C-rate서 급락 = 이온 병목).
- **최고**: **~42 vol% NCM, 154 mAh/g @0.1C, 91 @1C** ★ (= 우리 앵커 vol%와 일치!).
- composite-specific는 42→61 vol% 사이서 ~115 mAh/g(@0.1C)로 **포화**.
  ⟦10-03 PDF 대조⟧ composite-specific 의 0.1C → 1C 감소: 33 vol% **−40 % (33 mAh/g)**, 61 vol% **−88 % (100 mAh/g)** (p.7).
  Fig 3 의 데이터 점 = **33 · 42 · 47 · 58 · 61 vol%** (SI Table S3 · Fig S2 와 같은 집합; 면적용량 1.83–2.62 mAh/cm²).
- "~~pure-SE~~ 14 % porosity 경계"를 vertical dashed line으로 표시 (porosity 한계 강조).
  ⟦10-03 PDF 대조⟧ 캡션 원문: "The dashed vertical line illustrates the boundary of a **pure NCM cathode** with 14 % porosity" —
  즉 φ_NCM = **86 %** (기공 14 % 를 빼면 NCM 이 차지할 수 있는 최대) 위치의 점선이다.  pure-SE 와 무관.
- 해석: **저-CAM = 전자 percolation/utilization 병목, 고-CAM = 이온수송(τ_ion↑) 병목.** 중간이 최적.

★ **우리 production core(AM 70–85 wt% ≈ SE 30–50 % of solid)와의 매핑**: 42 vol% NCM ~~≈ w_NCM 73 %
(Fig 3 위 축; density 1.87/4.65로 변환)~~ — 우리 AM-rich core와 같은 영역. **42 vol% = 154 mAh/g 최적**이
우리 production core 선택의 실험 근거.
⟦10-03 PDF 대조⟧ 42 vol% NCM = **70 wt%** (SI Table S1: m_NCM 70 mg : m_SE 30 mg) — φ_SE 44 % (전체 부피) · 고체 중 SE 51.6 %
(내 산술).  Fig 3 위 축의 "73" 눈금은 φ_NCM **50 %** 자리에 있다 (위 축 47 · 73 · 89 가 아래 축 25 · 50 · 75 % 위; 기공 보정 없이
밀도 1.87/4.65 로 환산하면 45 · 71 · 88 % — 위 축 눈금 자체도 근사, 내 산술).  ⇒ 우리 production core (AM 70–85 wt%) 에 대응하는
이 논문 조성은 **42 vol% (70 wt%) ~ 61 vol% (86 wt%)** 이다.

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

- **핵심 주장**: **고-CAM~~(≥42 vol%)~~이면 carbon 무첨가로 충분** (CAM 자체가 전자 percolation 형성).
  이는 conventional LIB(항상 carbon 필요)와의 **근본적 개념 차이**.
  ⟦10-03 PDF 대조⟧ "≥42 vol%" 라는 문턱은 원문에 없다.  원문 근거는 **61 vol% 의 τ_el² ≈ 4.3** 이고 (p.6 "This could imply that a
  high CAM fraction in the cathode composite provides sufficient electronic percolation … even without the use of carbon
  additives"), 42 vol% 에 대해서는 **반대로** 쓴다: "For this volume fraction [≈42 %], the electronic tortuosity factor is above
  eight. Hence, we assume that not all CAM particles are connected to the electronically conducting network" (p.6) — 문헌에서
  carbon 이 이득이었던 이유를 이것으로 설명.  (그 "above eight" 은 본문 p.5 의 7.4 · Table S2 의 7.44 와 어긋난다, §17 #3.)
- VGCF 첨가(1 mg/100 mg composite) 실험:
  - **33 vol% NCM**(저-CAM): VGCF → material-specific 비용량 **+13 % @0.1C** (고립 CAM을 전자적으로 연결).
    하지만 효과가 C-rate 의존 약함 → **고립 CAM 회수**가 주효과(전자 percolation 신규 생성), 전도율 자체 개선 아님.
    ⟦10-03 PDF 대조⟧ "+13 %" 는 본문 값 (p.7).  SI Table S4 로 계산하면 **+16 %** (방전 135 → 157, 충전 137 → 159 mAh/g) — 불일치
    (§17 #12).  ΔQ 는 22 / 22 / 16 / 10 mAh/g (0.1 / 0.25 / 0.5 / 1C, 방전) — 본문 "10–20 mAh g⁻¹".  SI Table S4 는 이 셀을
    **"25 vol.-%"** 로 표기하지만 값은 Fig 4 범례의 33 vol% 계열과 같고, 사이클 조성 집합 (Table S3) 에 25 vol% 가 없다 → 표지 오기
    (§17 #10).
  - **61 vol% NCM**(고-CAM): VGCF 효과 **거의 없음/약간 악화** (이미 전자 충분; carbon-SE 계면 분해가 이온
    tortuosity↑ 유발 가능).
    ⟦10-03 PDF 대조⟧ SI Table S4 (SI p.6–7) 방전: 0.1C 132 → 130 · 0.25C 80.2 → 71.5 · 0.5C 43.2 → 32.9 · 1C 15.9 → 7.7 mAh/g.
    표의 ΔQ_dis 열이 0.25C "8.8" · 0.5C "−7.3" 으로 인쇄돼 있으나 산술은 −8.7 · −10.3 (§17 #11).  SI Fig S3 캡션: VGCF 는 고-CAM 에서
    "detrimental" — 한계가 전자 수송이 아님을 보인다.
- 전자 tortuosity factor τ_el²: 25 vol%서 120 → 61 vol%서 **4.3** ~~→ 42 vol%(τ_el²≈7.4) 이상서 CAM이
  전자망에 연결됨 → carbon 불필요~~. (단, carbon의 전위가 CAM과 비슷 → 표면 SE/CAM 분해 위험도 있음.)
  ⟦10-03 PDF 대조⟧ 취소 사유 = 위 첫 항목 — 원문은 42 vol% 에서 **일부 CAM 이 전자망에서 끊겼다고 가정**한다.  τ_el² 전 조성:
  120 / 13.7 / 7.44 / 4.77 / 4.29 (25 / 33 / 42 / 53 / 61 vol%, SI Table S2).

★ 우리 대응: σ_e 폼의 percolation·VGCF(도전제) 항. **Lee 2025 PTFE/VGCF σ_e 데이터**와 결이 같음
(도전제가 σ_e *기여* — 단 Lee는 PTFE wt%↑면 σ_e 급감 페널티도 보여줌, 이 논문엔 없음).

---

## §9. 이온 한계 극복 — SE 입자 미세화 (Fig 5, 6) ★ 우리 size=packing 과 직접 대응

### 9.1 전류밀도 스윕 (Fig 5)
- q vs current density j (mA/cm²), CAM 33/42/52/61 vol%.
  ⟦10-03 PDF 대조⟧ 범례 원문 = 33 / 42 / **53** (왼쪽 패널) · **52** (오른쪽 패널) / 61 vol%.  셋째 계열의 1C 점 j ≈ 2.3 mA/cm² 와
  비용량 (≈ 152 → 71 mAh/g, 판독) 은 **47 vol% 셀** (SI Table S3 면적용량 2.29 mAh/cm² · Fig 3) 과 일치 → 범례 오기 (§17 #14).
  각 점의 j = C-rate × 면적용량 (Table S3: 1C 에서 1.83 / 2.14 / 2.29 / 2.62 mA/cm²) 과 맞는다 (판독).  58 vol% 셀은 Fig 5 에 없다.
- **j > 0.5 mA/cm²서 CAM > 53 vol% 셀이 급격히 하강** (이온 수송이 양극 내 비용량 제한).
- **j < 0.5 mA/cm²서는 최저-CAM(33 vol%)이 오히려 composite-specific 더 낮음** (저-CAM은 저전류서도
  전자 utilization 병목). → 다시 **42 vol% 균형 최적** 확인.
- C-rate(상수전류) 대신 **constant current density(j)**로 비교해야 anode-side overpotential 분리 가능(논문 강조).

### 9.2 SE 입자 크기 효과 (Fig 6) — coarse vs fine LPSCl, 61 vol% NCM
- ball-mill로 LPSCl 입자 미세화(coarse → fine, >10 µm 입자 제거, SE 분산↑).
  ⟦10-03 PDF 대조⟧ 습식 유성 볼밀 200 rpm — 원문은 고에너지 밀링에서 흔한 비정질화 영향을 줄이려는 선택이라고 쓴다 (p.7–8).
  D50 **3.45 → 2.45 µm** · D90 **20.05 → 8.57 µm** (SI Table S5) — 주효과는 >10 µm 조대 입자 제거 (D50 은 조금만 변함).
  XRD (SI Fig S4) 는 같은 LPSCl 반사가 넓어진 모습 (판독; 원문은 그림에 해석을 달지 않음).
- **σ_ion,eff(fine) > σ_ion,eff(coarse)** ★ (작은 SE → CAM 사이 더 균일 분산 → 이온 경로 개선,
  τ_ion↓). 단 fine은 σ_el,eff 약간↓(CAM clustering 감소로 전자망 약화).
  ⟦10-03 PDF 대조⟧ SI Table S2 (61 vol%): σ_ion,eff **3.06·10⁻⁶ → 1.17·10⁻⁵** (×3.8) · τ_ion² **130 → 33.8**; σ_el,eff
  **1.43·10⁻³ → 6.97·10⁻⁴** (×0.49 — "약간↓" 이 아니라 **절반**) · τ_el² **4.29 → 8.79**.  원문 해석: 전자 전도도 감소는 고립 CAM
  증가를 뜻할 수 있으나 저율 CAM 비용량이 오히려 늘었으므로 **CAM 응집 (clustering) 감소**로 설명 (p.8–9).
- **C-rate 성능 fine이 우월** (이온 IR-drop↓). CAM-specific q: fine이 모든 C-rate서 더 높음.
  ⟦10-03 PDF 대조⟧ SI Fig S3 판독 (61 vol%, 0.1 / 0.25 / 0.5 / 1C): coarse ≈ 132 / 80 / 43 / 16 · fine ≈ 155 / 130 / 106 / 63 mAh/g.
  ⚠ Fig 6 오른쪽 막대 (축 라벨 "CAM-Specific Charge") 의 판독값 coarse ≈ 113 / 69 / 37 / 13 · fine ≈ 133 / 112 / 91 / 54 는
  Fig S3 의 **≈ 0.86 배** (= w_NCM 86 %) 이고 Fig 4b 의 **composite-specific** 61 vol% 값과 같다 → 축 라벨 오기 가능성 (판독 기반
  추정, §17 #15).  coarse vs fine 용량을 담았다는 **둘째 SI Table S5 는 복사 오류** (Table S4 저-CAM 블록과 전 칸 동일) → 인용 금지.
- bulk σ는 coarse 1.6 → fine 1.2 mS/cm로 **오히려 약간↓**(밀링 GB/amorphization) — 그럼에도 **유효 σ는↑**
  (분산/tortuosity 개선이 bulk 손실을 압도). ★ "**작은 SE가 좋은 건 bulk σ 때문이 아니라 packing/분산
  (τ↓) 때문**" — 우리 "size effect = PACKING not overlap" 결론과 ~~**정확히 일치**~~ **방향 일치**.
  ⟦10-03 PDF 대조⟧ "정확히 일치" → "방향 일치" 로 낮춘다 — 단서 두 개: (i) fine-SE 의 τ_ion² 33.8 은 **pristine σ₀ = 1.6 으로
  정규화**한 값이다 (§4.3) — 밀링 SE 자신의 1.2 로 하면 **25.4** (내 산술) — 어느 쪽이든 τ² 는 크게 준다; (ii) fine-SE 복합체의
  **기공률은 따로 재지 않았다** (φ_SE 는 같은 평균 14 % 로 0.25) → σ_ion,eff 이득 ×3.8 중 **기공 변화 몫을 원문으로는 가를 수
  없다**.  "packing (기공) vs 분산 (경로)" 의 분리는 이 논문 데이터 밖이다.

### 9.3 정량 목표(논문 자체 계산)
- 61 vol% NCM 최적 C-rate 위해선 σ_ion,eff = **0.4 mS/cm** 필요 → 현재 τ_ion²=34(61 vol%, fine)서는
  bulk σ가 **≥47 mS/cm** 여야 함(현 LPSCl 1.6의 ~30×). 비현실적.
- 만약 τ_ion²를 <10으로 낮추면(미세구조 개선) bulk **16 mS/cm**면 충분 → **고전도 SE + 저 tortuosity 둘 다** 필요.
- ⟦10-03 PDF 대조⟧ 원문 (p.9): "for that composite cathode, which showed the best C-rate performance in our experiments, an
  effective ionic conductivity of 0.4 mS cm⁻¹ was determined. To achieve this value in a composite cathode with 61 vol.-% and a
  tortuosity factor of 34, the ionic conductivity of the employed solid electrolyte has to be at least 47 mS cm⁻¹ … if the
  tortuosity factor could be decreased to a value below 10, the necessary ionic conductivity would yield 16 mS cm⁻¹."
  **산술 검산 (내 것)**: σ₀ = σ_eff·τ²/φ_SE 로 16 = 0.4 × 10 / **0.25** ✓ — 그런데 같은 φ 로는 0.4 × 34 / 0.25 = **54.4 ≠ 47**.
  47 은 φ_SE ≈ **0.288** (= 고체 중 SE 몫, 기공 무시) 일 때 나온다 (47.2) ⇒ **한 문단 안에서 φ 기준이 다르다** (§17 #5).
  또 0.4 mS/cm 는 Table S2 에서 **25 vol% 전도도 시료 (4.08·10⁻⁴)** 에만 해당하는데, 25 vol% 사이클 셀은 Table S3 에 없다 →
  "가장 좋은 C-rate 복합체" 가 어느 셀인지 [미확인].  "47 mS/cm 는 지금까지 보고된 최고값의 거의 두 배" 의 비교 대상 = [8] Kato
  2016 Nat. Energy.
- ★ **우리 인사이트와 직결**: σ_eff = σ_bulk·φ/τ² → bulk만 올리는 건 한계, **tortuosity(미세구조/packing)
  개선이 핵심.** 이게 우리 DEM이 미세구조-σ를 푸는 가치의 실험적 정당화.

---

## §10. Figure / Table 요약 (각각 우리가 쓸 점)

| Fig/Tab | 내용 | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **Fig 1** | 이온/전자 차단 대칭셀 + 대표 Nyquist + T-type TLM 등가회로 | 42 vol%: ion-block 0–140 Ω(1kHz/1Hz 표시), e-block 0–500 Ω · ⟦10-03 PDF 대조⟧ 판독: ion-blocking 스펙트럼 ≈ 25 → **≈ 107 Ω** (저주파 끝 = R_el 107 Ω 과 일치), electron-blocking ≈ 85 → ≈ 455 Ω (고주파 오프셋 ≈ SE 분리층, 끝에는 In 계면 포함 — R_ion 360 Ω 은 그 사이 몫) | EIS-TLM이 **우리 솔버의 실험 아날로그** — z_ion/z_el/z_int 분리법 |
| **Fig 2a** | σ_ion,eff·σ_el,eff vs φ_NCM | 25→61 vol% 전 구간 10⁻⁶–10⁻³ S/cm; ~~42 vol% 교차~~ ⟦10-03 PDF 대조⟧ σ 교차는 33–42 vol% (§5.0) · 값은 SI Table S2 가 정본 | ★ **CAM vol% 스윕 = 우리 AM:SE 스윕**; crossover |
| **Fig 2b** | **τ²** vs φ_NCM | τ_ion² 2.4→15.3, τ_el² 120→4.3 · ⟦10-03 PDF 대조⟧ 61 vol% τ_ion² = **130** 까지 (로그축 1–~300) · 0 · 100 % 점은 **정의로 1** · 오차막대 정의 없음 [미확인] · 값은 SI Table S2 (§5.0) | ★ **τ_ion²=4.3 @42 → τ=2.07 앵커**; 우리 τ_Laplace,eff 대응 (⟦10-03 PDF 대조⟧ 정확히는 τ² ↔ 우리 T = τ_Lap,eff², §16) |
| **Fig 3** | 비용량 vs φ_NCM (4 C-rate) | **42 vol% 154 mAh/g @0.1C** 최적; inverse-U · ⟦10-03 PDF 대조⟧ 데이터 점 33/42/47/58/61 vol% · 세로 점선 = pure **NCM** + 14 % 기공 경계 (φ_NCM 86 %) · 위 축 w_NCM 눈금 (47/73/89) 은 φ_NCM 25/50/75 % 위 (근사) | ★ 최적 CAM = 우리 production core; 병목 cell 발현 |
| **Fig 4** | VGCF 효과 (33 vs 61 vol%) | 33 vol% +13 % @0.1C; 61 vol% 무효 · ⟦10-03 PDF 대조⟧ SI Table S4 로는 +16 % (§8) | 고-CAM carbon 불필요; 우리 σ_e 도전제 항 |
| **Fig 5** | 비용량 vs current density (4 vol%) | j>0.5 서 >53 vol% 급락 · ⟦10-03 PDF 대조⟧ 범례 "53"/"52" 계열 = 실제 47 vol% 셀 (§9.1) | 이온 병목의 j-의존; 42 vol% 균형 |
| **Fig 6** | coarse vs fine SE (61 vol%) | fine σ_ion,eff↑·C-rate↑ (bulk 1.6→1.2) · ⟦10-03 PDF 대조⟧ 왼쪽 막대 = SI Table S2 값 (판독 일치) · 오른쪽 막대는 축이 "CAM-specific" 인데 값은 composite-specific 으로 보임 (§9.2) | ★ **작은 SE = packing/τ↓ (bulk 아님)** — 우리 결론 ~~일치~~ **방향 일치** (⟦10-03 PDF 대조⟧ 기공 미측정 · σ₀ 정규화 단서, §9.2) |
| **Table SII** | vol%별 두께·areal capacity·τ² | (SI; L=470 µm @42 vol% 등) · ⟦10-03 PDF 대조⟧ 본문 "Table SII" 는 **두 곳에서 다른 내용**을 가리킨다 — p.6 (두께·면적용량) → 실제 **SI Table S3** (면적용량만, 두께 열 없음) · p.9 (fine-SE τ² ≈ 34) → **SI Table S2**.  L = 470 µm 은 본문 p.5 값 (SI 표에 없음) | porosity·τ 보조 |
| **Table SIII** | **porosity 13–17 %** | dry-mix 380 MPa · ⟦10-03 PDF 대조⟧ 실제 **SI Table S1** — 시료별 7.6 / 13 / 17 / 17 / 15 % (= **7.6–17 %**), 평균 14 | ★ **porosity 앵커 range 원전** |
| **Table S2(SI)** | NCM-622 전자 partial σ = **10 mS/cm** | ⟦10-03 PDF 대조⟧ + σ_eff · τ² **전 조성** (8 행, §5.0) | CAM 전자 bulk 앵커 · ★★ τ² 정본 |

~~(SI는 본 PDF에 미포함 — "04._Sup" 업로드는 *다른 논문*이라 무시. Table SII/SIII/S2 값은 본문 인용으로 확인.)~~
⟦10-03 PDF 대조⟧ 취소 사유 — SI 를 확보해 끝까지 읽었다 (인박스 `1. Sup) Editors' choice…pdf`, 10쪽).  아래 §10-SI 가 SI 전 항목,
그 아래 표가 본문 인용 번호 ↔ SI 실제 번호 대응이다.

### §10-SI ⟦10-03 PDF 대조⟧ SI 그림·표 세트 (그림 파일 = `litdb/figures/minnmann2021_jes_charge_transport_bottlenecks/`)

| SI 항목 (SI 쪽) | 파일 | 무엇을 보여주나 | 핵심 수치 (stated / 판독) | 우리가 쓸 점 |
|---|---|---|---|---|
| §1 식 S1–S7 (p.2–3) | — | T-type TLM 전체 식 · z_ion = r_ion · z_el = bulk + NCM–NCM 접촉 R-CPE · z_int = CPE · R_el = L(r_el,bulk + r_el,int) · R_ion = L·r_ion | 식 (stated, §4.2) | R_el 이 **입자 접촉저항을 포함** → τ_el² 는 접촉 포함 수송 τ² |
| Fig S1 (p.3) | `fig_S1.png` | In/(InLi)ₓ \| LPSCl \| In/(InLi)ₓ 대칭셀 Nyquist + 등가회로 R_SE + (2·R_SE\|In/(InLi)ₓ ∥ ½·C) | R_SE ≈ 47 Ω · 2×R_SE\|In ≈ 25 Ω · 꼭짓점 5 Hz (판독) | 이온 측정에서 분리층·In 계면 저항을 빼는 법 (본문은 "Fig. S3" 로 인용) |
| 식 S8–S9 + Table S1 (p.4) | `tab_S1.png` | 다섯 조성의 질량 · V_theo · V_meas · 시료별 기공 · 평균 기공 · φ_NCM · φ_SE | 기공 7.6 / 13 / 17 / 17 / 15 % · 평균 14 · φ_NCM 25/33/42/53/61 · φ_SE 61/53/44/33/25 (stated) | ★ porosity 앵커 원전 (본문 "Table SIII") · V_theo 는 ρ_NCM ≈ 4.77 로만 재현 (§17 #8) |
| Table S2 (p.5) | `tab_S2.png` | φ · σ_el,eff · τ_el² · σ_ion,eff · τ_ion² (8 행, fine-SE 포함; 순수 재료 τ² := 1) | §5.0 표 (stated) | ★★ **τ² 정본 값** |
| Table S3 (p.5) | (그림 파일 없음 — figures.json 이 "p5 거의 백지" 로 놓침; 실제로는 p.5 아래쪽에 있다) | 사이클 셀 5 조성의 NCM 면적 적재 · 면적용량 (복합체 12 mg, 200 mAh/g 가정) | 33: 9.17 mg/cm² · 1.83 mAh/cm² / 42: 10.7 · 2.14 / 47: 11.5 · 2.29 / 58: 12.8 · 2.55 / 61: 13.1 · 2.62 (stated) | 사이클 조성 집합의 원전 · 본문 "214 mAh cm⁻²" 오식 판정 근거 · Fig 5 의 j 축 해석 |
| Fig S2 (p.6) | `fig_S2.png` | 33/42/47/58/61 vol% 충방전 곡선 (C/10 · C/4 · C/2 · 1C), 가로축 CAM-specific q_mat | 전압창 ≈ 2.6–4.3 V (축 "vs. Li⁺/Li", 판독) · 42 vol% C/10 방전 ≈ 157 · 1C ≈ 91 mAh/g (판독) | 고-CAM 에서 1C 분극 급증 = 이온 IR 강하의 시각 증거 |
| Table S4 (p.6–7) | `tab_S4.png` (61 vol% 블록은 첫 행만 — 나머지는 SI p.7) | VGCF 유무 충·방전 비용량: 저-CAM (표지 "25 vol.-%") / 61 vol% | 저-CAM 방전 0.1C 135 → 157 · 1C 83.0 → 93.0; 61 vol% 방전 0.1C 132 → 130 · 0.25C 80.2 → 71.5 · 0.5C 43.2 → 32.9 · 1C 15.9 → 7.7 (stated) | VGCF 효과의 정량 원값 — 단 표지 · ΔQ 오식 (§17 #10 · #11) |
| Fig S3 (p.7) | `fig_S3.png` | 61 vol%: 기본 · +VGCF · fine SE · fine SE + VGCF 의 C-rate 성능 | fine ≈ 155 / 130 / 106 / 63 vs 기본 ≈ 132 / 80 / 43 / 16 mAh/g (0.1 / 0.25 / 0.5 / 1C, 판독) | 고-CAM 한계는 전자 아님 (VGCF 가 오히려 손해) · 입경 효과의 정량 판독원 |
| Fig S4 (p.8) | `fig_S4.png` | 밀링 전·후 SE XRD (Li₆PS₅Cl · Li₂S · LiCl 참조선) | 밀링 후 같은 반사가 넓어짐 (판독; 캡션에 해석 없음) | 밀링 후 결정성 변화의 정성 근거 |
| Fig S5 (p.8) | `fig_S5.png` | 밀링 전·후 누적 입도 분포 (로그 0.1–100 µm) | pristine 최대 ≈ 60 µm · milled ≈ 23 µm (판독) | >10 µm 조대 입자 제거가 주효과 |
| Table S5 — PSD (p.9) | `tab_S5.png` | D50 · D90 (캡션은 "50 % and 90 % median particle size values") | D50 3.45 → 2.45 µm · D90 20.05 → 8.57 µm (stated) | SE 입경 앵커 — 측정법은 원문에 없음 [미확인] (사의에 TU Braunschweig iPat 측정) |
| Fig S6 (p.9) | `fig_S6.png` (위에 Table S5 PSD 가 함께 잘림) | 순수 SE 임피던스, 밀링 전·후 · stainless steel · ~40 MPa | 고주파 절편 ≈ 51 Ω → ≈ 64 Ω (inset 판독) · 1.6 → 1.2 mS/cm (본문 stated) | ★ **σ_ion,0 측정 조건의 유일한 원문 서술** (본문은 "Fig. S4" 로 인용) |
| Table S5 — 둘째 (p.9) | (그림 파일 없음) | "61 vol.-% CAM 의 coarse vs fine SE 충방전 용량" 이라는 표 | 값이 Table S4 저-CAM 블록과 **전 칸 동일** (137 / 159 / 22 …) — Fig S3 의 61 vol% (0.1C ≈ 132, 1C ≈ 16) 와 불일치 | **복사 오류로 판단 — 인용 금지** (§17 #13) |

**본문 인용 번호 ↔ SI 실제 항목** (⟦10-03 PDF 대조⟧ — 본문은 SI 를 로마 숫자/다른 번호로 부른다):

| 본문 표기 (쪽) | 본문이 가리키는 내용 | SI 실제 항목 |
|---|---|---|
| "Table S2" (p.3) | NCM-622 전자 10 mS/cm | Table S2 마지막 행 ✓ |
| "Section 1" (p.4) | TLM 상세 | SI §1 (식 S1–S7) ✓ |
| "Fig. S3" (p.5) | In/(InLi)ₓ\|LPSCl\|In/(InLi)ₓ 대칭셀 | **Fig S1** |
| "Section 3" (p.5) | 평균 기공 도출 | SI §3 (식 S8–S9 · Table S1) ✓ |
| "Table SII" (p.6) | 조성별 두께 · 면적용량 | **Table S3** (면적용량만; 두께 열 없음) |
| "Fig. S2" (p.7) | 충방전 곡선 | Fig S2 ✓ |
| "Table SIV" (p.7) | VGCF 충전 비용량 | Table S4 ✓ (표지는 "25 vol.-%") |
| "Fig. S4" (p.8) | pristine vs milled 순수 SE 임피던스 | **Fig S6** |
| "Fig. S2" (p.8) | 61 % · 두 입도 SE 복합체의 이온·전자 전도도 | **해당 그림 없음** — 값은 Table S2 "61 / 25 (fine SE)" 행, 그림은 본문 Fig 6 |
| "Table SV" (p.8) | >10 µm 입자 감소 | Table S5 (PSD) ✓ |
| "Fig. S3" (p.8) | VGCF 불필요 | Fig S3 ✓ |
| "Table SIII" (p.9) | 기공 13–17 % | **Table S1** (7.6–17 %) |
| "Table SII" (p.9) | fine-SE τ² ≈ 34 | Table S2 ✓ |
| (본문 인용 없음) | — | Fig S4 (XRD) · Fig S5 (PSD 곡선) · 둘째 Table S5 |

---

## §11. ★ 비교 vs 우리 DEM+MPM (focused §)

| 축 | 이 논문 (실험, NCM-622+LPSCl) | 우리 DEM+MPM (NMC811+LPSCl) | 차이 / 매핑 / 주의 |
|---|---|---|---|
| **porosity** | **14 % (13–17 %)** @ dry-mix **380 MPa** (복합 양극) · ⟦10-03 PDF 대조⟧ 시료별 **7.6–17 %** (SI Table S1) | pure-SE ~10 % / real_14 15.6 % @300 MPa | ★ 우리 앵커 출처 확정; **복합 13–17 %는 우리 real_14 15.6 %와 직접 정합**(±조건). pure-SE 10 %는 이 논문 아님 (⟦10-03 PDF 대조⟧ SI 까지 확인 — 순수 시료 기공 값 없음, §0) |
| **σ_ion,eff** | **0.17 mS/cm @ 42 vol% NCM** (EIS-TLM, 측정 ~40 MPa) | DEM σ_ionic 0.04–0.18 mS/cm, envelope 0.03–0.14 | ★ **같은 소재 → 직접 비교 가능**; 0.17이 우리 상단(0.18)과 일치. 우리 솔버의 절대 앵커 · ⟦10-03 PDF 대조⟧ ⚠ **σ₀ 가 다르다** — 원문 σ_ion,0 = 1.6 (펠릿), 우리 망 σ_bulk = 3.0 mS/cm.  같은 미세구조면 우리 σ_eff 는 σ₀ 비만큼 (×1.9) 크게 나온다 ⇒ σ_eff 끼리의 "일치" 는 같은 척도 비교가 아니다.  같은 척도 비교는 **f = σ_eff/σ₀ (원문 0.104) 또는 T = τ² (원문 4.27)** 로 (§16) |
| **τ_ion** | **2.07** (=√(τ²=4.3)) @ 42 vol% | 우리 τ_Laplace,eff (솔버 geodesic/Laplace) | ★ **같은 정의(Eq 4 = σ_0·φ/σ_eff)**; ⚠ ~~그들 = constriction 미포함~~, 우리 = 솔버 의존 명시 필요. τ vs τ² 혼동 주의 · ⟦10-03 PDF 대조⟧ (i) 인쇄 Eq 4 는 역수 오식 — "같은 정의" 는 **보고값 기준 꼴**에서만; (ii) 그들 τ² 는 협착·접촉·CEI 를 **흡수** (§4.3) → 우리 **τ_Lap,eff** (σ_full, Holm 협착 포함 — Laplace, geodesic 아님) 와 같은 범주, τ_Lap,geom 과는 다른 범주; (iii) 원문 σ₀ = 펠릿, 우리 τ 에서는 σ_grain 약분 (§16) |
| **σ_grain (bulk)** | LPSCl **1.6 mS/cm @25°C** (제품 ~~단결정/응집~~ EIS) | Cronau ~~단결정~~ **3.0** ×Cronau(r_SE) | 1.6 < 3.0 → 측정·GB·입자 차이. **Bazzoun 1.02 / Lee 2.19 / 이 논문 1.6** = bulk LPSCl 앵커 스프레드(절대 직접대조 금지, 범위로) · ⟦10-03 PDF 대조⟧ "단결정" 두 곳 취소: 이 논문의 1.6 = **순수 SE 시료 (펠릿) EIS**, stainless steel · ~40 MPa (SI Fig S6), 펠릿 기공 포함 (SI §3) / 3.0 = Cronau 2021 SI Fig. S2c µC-LPSCl **펠릿** 하단 (원장 CL-91).  ⇒ **둘 다 펠릿값**이고 차이 1.9× 는 재료 lot · 펠릿 밀도 · 측정 조건 차 (원문으로 가를 수 없음).  Cronau(r_SE) 는 출처 없는 모델 가정 (원장 SELF-51) — 우리 τ_Lap 계산에는 들어가지 않는다 |
| **CAM 전자 bulk** | NCM-622 **10 mS/cm** (SI S2) | NMC811 우리 σ_AM(e) Trevisanello 10/5 | ★ **우리 σ_e LOCKED endpoint 10 mS/cm 와 일치**(같은 NCM 계열) · ⟦10-03 PDF 대조⟧ 원문 10 mS/cm = **완전 리튬화 (0 % SoC) NCM-622 순수 시료 EIS** (τ_el² := 1).  우리 10/5 의 라벨은 CLAUDE.md A1 (2026-06-30) 기준 **corpus-fit endpoint** (Trevisanello 는 GB 방향만 지지) — 수치 일치는 출처 공유가 아니다 |
| **CAM vol% 스윕** | 25–61 vol%, σ↓/τ↑(이온), 최적 42 | AM:SE 스윕 + Furnas + percolation | ★ CAM↑→σ_ion↓ 추세 일치; 42 vol% 최적 = 우리 core |
| **utilization (dead)** | ion+e 둘 다 연결돼야 active; 고-CAM서 고립 | f_AM^cc / dead-AM / ionically-vulnerable | ★ **개념 동일** — 우리 dead-AM 경고의 실험 근거 |
| **전자 병목 (저-CAM)** | 25 vol%서 τ_el²=120 (percolation 실패) | σ_e φ_AM⁴ + percolation(f_p) | ★ ~~Park 2020 90 wt% percolation 실패와 같은 물리~~ · ⟦10-03 PDF 대조⟧ 짝 어긋남 — 25 vol% 는 CAM-poor 의 **전자** 붕괴, "SE-poor 90 wt%" 에 대응하는 것은 61 vol% 의 **이온** 붕괴 (τ_ion² 130) (§5).  또 φ_NCM 0.247 은 우리 σ_e 폼의 φ_AM < 0.3 외삽 금지 구역 안 |
| **size 효과** | fine SE → σ_ion,eff↑ (bulk↓에도) = packing/τ | "size effect = PACKING not overlap" | ★ **결론 ~~정확히~~ 일치** · ⟦10-03 PDF 대조⟧ **방향 일치**로 낮춤 — fine-SE 시료 기공 미측정 · τ² 가 pristine σ₀ 로 정규화 (§9.2) |
| **transport 채널** | σ_ion + σ_el (이온·전자 둘 다) | σ_ion + σ_e + σ_thermal (삼중항) | 우리 σ_thermal 추가 우위 |
| **방법** | **실험 EIS-TLM** (solver 아님) | DEM Kirchhoff/Holm 솔버 + Stage-E | ★ **그들 실험 = 우리 솔버의 frame[4] 외부 검증** |
| **Stage-E 대응** | TLM이 constriction/CEI 무시(Eq 4 주의) | Stage-E 소성 접촉면적(Tabor+volume) | ~~우리 Stage-E가 그들이 무시한 constriction을 포함 → σ_eff 보정 방향~~ · ⟦10-03 PDF 대조⟧ 전제가 반대였다 — 그들 τ² 는 constriction 을 *모델하지 않고* **측정값 안에 흡수**한다 (§4.3).  즉 실험 σ_eff 자체가 협착 포함 "정답" 이고, 우리 Stage-E·Holm 은 그 협착을 **모델로 넣는** 쪽이다 ⇒ 질문은 "우리 협착 모델이 실험 σ_eff (= τ²) 를 맞추나" 이지 "그들이 빠뜨린 것을 우리가 더한다" 가 아니다 |
| **소성/morphology** | 없음(실험, 미세구조 가정만) | MPM 진짜 SHAPE 소성 | 우리 MPM 고유 (frame[5]) |

**핵심 정합 3가지:**
1. **σ_ion,eff 0.17 mS/cm @42 vol% = 우리 DEM σ_ionic 상단(0.18)과 일치** — 같은 소재, EIS-TLM = 실험 진실.
   ⟦10-03 PDF 대조⟧ 단서: σ₀ 가 1.6 (원문 펠릿) vs 3.0 (우리 망) — σ_eff 끼리 맞대면 척도가 1.9× 어긋난다.  "일치" 를 주장하려면
   **τ² (= T) 나 f = σ_eff/σ₀ 로** 비교해야 한다 (원문 42 vol%: T 4.27 · f 0.104).
2. **복합 porosity 13–17 % = 우리 real_14 15.6 %** (둘 다 ~300–380 MPa cold-press 복합 양극).
   ⟦10-03 PDF 대조⟧ 시료별 범위는 7.6–17 % (SI Table S1).
3. **size·tortuosity 결론 일치**: "작은 SE가 좋은 건 packing/τ 때문(bulk σ 아님)" — 우리와 동일.
   ⟦10-03 PDF 대조⟧ "방향 일치" 로 낮춘다 — fine-SE 시료의 기공을 재지 않아 packing (기공) 과 경로 (τ) 를 원문으로는 가를 수 없다
   (§9.2).

---

## §12. ★ 우리 σ_ionic / Stage-E / 솔버에 어떻게 쓰나 (적용 인사이트)

1. **σ_ion 절대 앵커 정정·도입**: "Minnmann 2021 JES 040537, σ_ion,eff = **0.17 mS/cm @ 42 vol% NCM,
   τ_ion = 2.07 (τ²=4.3), 복합 porosity 14 % (13–17 %), dry-mix 380 MPa**" 를 우리 σ_ionic·τ 외부 검증점으로
   고정. (그들 vol% NCM → 우리 φ_SE 매핑: 42 vol% NCM ~~≈ SE 58 vol%, w_NCM≈73 %~~.)
   ⟦10-03 PDF 대조⟧ SI Table S1: 42 vol% NCM ↔ **φ_SE 44 %** (기공 14 % 를 포함한 전체 부피 기준; 재계산 0.4437) · 고체 중 SE 몫
   **51.6 %** (내 산술) · **w_NCM 70 %** (70 mg : 30 mg).  "SE 58 vol%" 는 근거가 없고 "73 %" 는 Fig 3 위 축 눈금의 오독이다 (§6).
2. **τ vs τ² 표기 통일**: 우리 코드/문서에서 "Minnmann τ_ion 2.07" 인용 시 반드시 **"= √(tortuosity factor
   τ²=4.3)"** 병기. Eq 4 = σ_0·φ/σ_eff = 우리 τ_Laplace,eff 정의와 동일함을 명기.
   ⟦10-03 PDF 대조⟧ 인용 꼴 정정: **"Minnmann 2021 Eq 4 (인쇄 꼴 τ² = (σ_eff/σ₀)·φ 는 역수 오식; 보고값은 τ² = φσ₀/σ_eff, SI
   Table S2)"**.  τ² 정밀값은 4.27, √ 2.07 은 우리 산술, Eq 3 기하 τ 아님, 원문 σ₀ = 펠릿값 — 넷 다 같이 적는다 (§16).
3. **CAM vol% 스윕 σ_ion,eff·τ² 곡선 = 우리 AM:SE 스윕 검증 곡선** (Fig 2). 추세(CAM↑→σ↓, τ↑) 직접 대조.
   25 vol%서 τ_el²=120(전자 percolation 실패) = 우리 σ_e percolation 항 검증점.
4. **Stage-E constriction 기여 정량**: ~~그들 Eq 4 τ는 constriction 미포함 → 우리 Stage-E(Holm 구속) 포함
   σ_eff와 같은 구조서 비교하면 **Stage-E가 더하는 보정폭** 정량 가능~~ (Bazzoun RNM 과소 보정과 같은 lever).
   ⟦10-03 PDF 대조⟧ 취소 사유 = 전제가 반대 (그들 τ² 는 협착을 **흡수**, §4.3).  고친 쓰임: 실험 τ² (협착 포함) ↔ 우리
   **τ_Lap,eff²** (Holm 포함) 를 맞대 **우리 협착 모델의 절대 검증**에 쓰고, 협착 몫 자체는 **우리 모델 안에서만** τ_Lap,eff /
   τ_Lap,geom 비로 본다 — 실험 쪽에는 협착을 떼어낸 값이 없다.  비교 전에 σ₀ 기준 (펠릿 1.6 vs 망 간선 3.0) 과 φ 관례 (평균 14 %
   보정 vs DEM 기하) 를 맞출 것 (§16).
5. **bulk σ 스프레드 확장**: LPSCl 1.6 mS/cm 추가 → {Cronau ~~단결정~~ 3.0, Lee pristine 2.19, 이 논문 1.6,
   Bazzoun pellet 1.02} 의 측정/입자/GB 스프레드 (절대 직접대조 금지, 범위·민감도로만).
   ⟦10-03 PDF 대조⟧ "단결정" 취소 (원장 CL-91 — 3.0 은 펠릿값).  이 논문 1.6 도 펠릿 (순수 시료) 값이다.
6. **σ_e endpoint 확인**: NCM-622 전자 10 mS/cm = 우리 σ_e LOCKED 10 mS/cm 와 일치 → 우리 endpoint 재확인.
   ⟦10-03 PDF 대조⟧ "재확인" 은 과하다 — 원문 10 mS/cm 은 **완전 리튬화 NCM-622 순수 시료 펠릿**의 EIS 값 (τ_el² := 1) 이고, 우리
   10 mS/cm 은 CLAUDE.md A1 기준 corpus-fit endpoint 다 (§11).  **같은 자릿수라는 정합**까지만 말한다.

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

⟦10-03 PDF 대조⟧ **위 세 문장을 쓰기 전에 고칠 것** (원문 + SI 대조 결과):
- 첫 문장 "range 13–17 %" → 본문 문구다.  SI Table S1 의 시료별 값은 **7.6–17 %** — 범위를 쓰려면 SI 값으로.
  "τ_ion = 2.07, i.e. τ² = 4.3" → τ² 는 SI Table S2 에서 **4.27**; 2.07 은 우리 √ 산술이고 원문이 쓰지 않는 수다.
- 둘째 문장 "brackets the experimental σ_ion,eff = 0.17" → σ₀ 가 다르다 (원문 1.6 펠릿 vs 우리 3.0).  같은 척도로 쓰려면
  "τ² (tortuosity factor) 4.27" 또는 "σ_eff/σ₀ = 0.104" 와 비교하는 문장으로 바꾼다.
- 셋째 문장 "confirming that … a packing/tortuosity effect" → fine-SE 복합체의 기공을 재지 않았고 τ² 를 pristine σ₀ 로 정규화했다
  (§9.2).  "consistent with" 수준으로 낮춘다.
- Eq 4 를 인용할 때: "Eq. 4 of Minnmann et al. is printed as τ² = (σ_eff/σ₀)φ; the reported values follow τ² = φσ₀/σ_eff."

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
  ⟦10-03 PDF 대조⟧ 세 가지를 더 구분한다: (1) **원문 Eq 3 τ_i = l_i/l_0** = 기하 tortuosity (최단 경로 길이 / 직선 거리) — 정의만
  있고 측정 없음; (2) **원문 Eq 4 τ_i²** = "tortuosity factor" — 측정 σ_eff 에서 역산한 **수송 유도** 값 (협착·접촉 포함), 원문도
  "참 기하 tortuosity factor 와 다를 수 있다" 고 씀 → **√(Eq 4) ≠ Eq 3** 일반적으로; (3) 인쇄 Eq 4 는 σ 비가 뒤집힌 오식 — 보고값은
  σ₀φ/σ_eff.  우리 쪽 대응은 §16.
- **MacMullin 수 N_M** ⟦10-03 PDF 대조⟧ = σ₀/σ_eff = τ²/φ (42 vol% 이온 9.64).  **원문에 없는 이름** — 문헌 비교용 우리 분류.
  "formation factor" · "Bruggeman" 이라는 낱말도 원문에 없다.
- **partial / effective conductivity**: partial = 한 전하종(이온 또는 전자)의 전도도; effective = 그 partial이
  미세구조(porosity·tortuosity·분산) 때문에 *유효하게* 감소한 값. σ_eff = σ_bulk·φ/τ².
- **utilization level**: 이온·전자 망에 *둘 다* 연결된 CAM 비율 (= active CAM). 우리 f_AM^cc.
- **CEI** (Cathode-Electrolyte Interphase): CAM/SE 계면 반응층. Eq 4 τ는 이를 무시.
  ⟦10-03 PDF 대조⟧ "무시" = **따로 모델하지 않는다**는 뜻 → 측정 σ_eff 가 겪은 CEI·협착 저항은 **τ² 에 흡수**된다 (§4.3).
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
  ⟦10-03 PDF 대조⟧ 시료별 7.6–17 % (SI Table S1) · 순수 시료 기공은 SI 에도 없다 (§0).
- **digitized vs stated**: 42 vol% 기준점 수치(0.17, 4.3, 7.4, R_el/R_ion, L, A)는 전부 **stated(본문)**.
  Fig 2의 다른 vol% 곡선값(25/33/53/61 vol%의 σ·τ²)은 일부 본문 stated(2.4/15.3/120/4.3 등) + 일부
  **Fig에서 읽은 추세**(±) — 위 §5 표의 "~" 표기 값은 trend-only.
  ⟦10-03 PDF 대조⟧ **이제 전 조성의 σ_eff · τ² 가 stated** (SI Table S2, §5.0) — 판독값을 쓸 이유가 없다.  판독 (digitized) 으로
  남는 것은 사이클 비용량 곡선 (Fig 3–6, S2–S3) · Nyquist 절편 (Fig 1, S1, S6) · 전압창 (Fig S2) 뿐이고, 이 카드에서 "판독" 으로
  표지했다.
- **bulk σ 1.6 vs 우리 Cronau 3.0**: 측정/입자/GB 차 → 절대 직접대조 금지, 범위로만. 우리 σ_grain 이중계상
  점검(pellet/~~단결정~~/제품 EIS 혼용 주의)에 추가 데이터점으로.
  ⟦10-03 PDF 대조⟧ "단결정" 취소 (CL-91).  ★ 이중계상 점검에 직접 쓰이는 원문 문장이 있다 — SI §3: 순수 시료의 기공이 측정
  전도도를 낮추지만 τ² := 1 로 두었다 ⇒ **원문 τ² 자체가 "펠릿 기준"** 이다.  CLAUDE.md CL-91 의 "STEP3 입력 σ 가 펠릿값이면 기공이
  부분 이중계상" 과 **같은 구조가 실험 쪽에도 있다** (§16).
- **이 논문 자체의 한계(저자 명시)**: porosity 정확 측정 어려움; Eq 4 τ는 constriction/CEI/space-charge 무시 →
  "true" geometric τ와 다를 수 있음; ~~SI 미포함(본 PDF) → Table 값은 본문 인용으로 확보.~~
  ⟦10-03 PDF 대조⟧ SI 확보·대조 완료.  저자 명시 한계 추가: porosity 오차 "최대 10 %" (두께 측정 부정확, SI §3) · 순수 재료 τ² := 1
  (SI §3).
- ⟦10-03 PDF 대조⟧ **원문 대조로 새로 드러난 한계** (상세 §17):
  - 인쇄 Eq 4 가 보고값과 역수 — 식만 보고 재계산하면 τ² 가 1 미만으로 나온다.
  - φ 는 **평균 기공 14 %** 하나로 모든 조성에 적용 (시료별 7.6–17 %) · fine-SE 시료는 기공 미측정.
  - σ₀ = 순수 시료 펠릿값 (압밀압 · 기공 · 두께 미보고) · fine-SE τ² 는 pristine σ₀ 로 정규화.
  - 전도도 시료 집합 (25/33/42/53/61) ≠ 사이클 셀 집합 (33/42/47/58/61) — σ·τ² 와 용량을 같은 조성에서 맞대는 것은 33·42·61 뿐.
  - 오차막대 · 반복 수 정의 없음 (Fig 2b) — 사이클만 "두 셀".
  - 본문↔SI 번호 체계 불일치 · Table S4 표지·ΔQ 오식 · Table S5 중복 · Fig 5 범례 · Fig 6 축 — SI 수치를 인용할 때는 **SI 의 실제
    번호와 이 카드 §10-SI 를 함께** 적는다.

---

## §16. ⟦10-03 PDF 대조⟧ ★ tortuosity 정의 대조표 — 원문 기호 ↔ 우리 τ 들

이 묶음 (tortuosity, 2026-10-03) 의 목적 = **정의를 닫는다**.  원문 쪽은 본문 p.5 식 [2]–[4] · SI 식 S6–S9 · SI Table S2 에서,
우리 쪽은 stoic-knuth 브랜치 코드를 이 카드 작성 중 직접 읽어 확인했다: 웹앱 `webapp/app.py:2610` 부근 (τ_Lap,eff ·
τ_Lap,geom) · `scripts/network_conductivity.py:850–857` (σ_eff = G·T/A, A = box_x·box_y) · `:1156–1157` (σ_full_mScm ·
σ_bulk_net_mScm = 비 × σ_bulk) · `:1226` (이온 σ_bulk = `se_material.sigma_grain_S_cm`) · `scripts/dem_analysis_core.py`
`calc_tortuosity` (τ_Dij = 경로 길이 / z 거리).  COMSOL 식 (5.6 사용자 안내서 식 6-6, 375쪽: `f_e = ε_p/τ_F`, Bruggeman
`τ_F = ε_p^(−1/2)`) 은 **메인 제공 — 이 카드에서 COMSOL 원문은 대조하지 않았다**.

| 원문 기호 | 정의식 (식 번호 · 쪽) | 이름 (원문 낱말) | σ_eff 정규화 기준 | 우리 어느 τ 와 같은 양인가 | 환산식 |
|---|---|---|---|---|---|
| **τ_i** | `τ_i = l_i / l_0` — "the ratio of the length of the shortest charge transport pathway l_i to the shortest distance l_0 between two points" (식 [3], p.5) | "geometric tortuosity" (of a trajectory) | 해당 없음 — 길이 비, σ 를 쓰지 않는다 | **τ_Dijkstra 계열** — `tortuosity_mean/median/std` (SE 접촉망 거리가중 최단 경로 / 두 끝점의 **z 거리**, 바닥→위 표본쌍) · τ_Dij,all (바닥 SE 전부 → 위 띠) · 벽 τ (수확기, 벽 기준 기하 최단 경로) = **같은 범주** (기하 경로 길이 비).  분모 관례 차: 원문 l_0 = 두 점 사이 직선 거리, 우리 = z 거리 (≤ 직선 거리 → 우리 값이 같거나 크다).  ⚠ 원문은 Eq 3 을 **정의만 하고 측정하지 않는다** → 우리 τ_Dij 의 수치 앵커는 이 논문에 **없다** | 없음 — 일반적으로 τ_i (Eq 3) ≠ √(τ_i² of Eq 4) (원문: Eq 4 값이 "true geometrical tortuosity factor" 와 다를 수 있다) |
| **τ_i²** (인쇄 그대로) | `τ_i² = (σ_i,eff / σ_i,0) · φ_i` (식 [4], p.5) | "tortuosity factor" | 식 [2] 와 같음 | **어느 것과도 같지 않다** — 보고값과 역수 관계, 계산하면 전부 < 1 (§4.3) ⇒ **오식** | (σ_eff/σ₀)·φ = f·φ = φ²/T — 의미 있는 양 아님 |
| **τ_i²** (보고값 — Fig 2b · SI Table S2 · 본문 수치) | `τ_i² = φ_i · σ_i,0 / σ_i,eff` — Table S2 전 행을 **0.7 % 안**에서 재현하는 꼴 (내 검산, §4.3).  입력: σ_i,eff = L/(R_i A) (식 [2], p.5) · σ_i,0 = 순수 시료 펠릿 EIS (SE 1.6 · NCM 10 mS/cm) · φ_i = (1 − 0.14)·φ_i,nom (식 S9, SI p.4) | "tortuosity factor" (Fig 2b 축 "Tortuosity Factor τ²") | **전극 전체 단면**: A = 0.785 cm² (⌀10 mm 원기둥 전체) · L = 측정 두께; φ_i 는 **기공 포함 전체 부피** 기준으로 따로 곱한다 ⇒ `σ_eff = σ₀·φ/τ²` 관례 | ★ **우리 T = φ_SE·σ₀/σ_eff = τ_Lap,eff²** (웹앱 τ_Lap,eff = √(φ_SE·σ_grain/σ_full); σ_full = 접촉망 Kirchhoff 해, σ_eff = G·T/A 전체 단면) ≡ **COMSOL τ_F** (`f_e = ε_p/τ_F` ⇒ σ_eff = σ·ε_p/τ_F) ≡ **인계 열 사전 T**.  같은 범주인 근거: 둘 다 σ_eff 안에 접촉·협착 저항이 든 채로 정의된다 (원문 R_el 은 NCM–NCM 접촉저항 포함 — 식 S6; R_ion 은 SE 내부 전부 — 식 S7 / 우리 σ_full 은 Holm 협착 포함) | **T = τ²** · τ(인계) = √T · f = σ_eff/σ₀ = φ/T · N_M = σ₀/σ_eff = T/φ (원문에 없는 이름) · Bruggeman (COMSOL 기본) τ_F = φ^(−1/2) |
| (원문에 없음) √τ_i² — 이 카드의 "τ_ion = 2.07" | √(보고 τ²) — **우리 산술** | 원문은 √ 를 쓰지 않는다 | 위와 같음 | **우리 τ_Lap,eff ≡ 인계 τ = √T** | τ = √T — 42 vol% 이온 √4.27 = 2.07 (⚠ 61 vol% 전자 √4.29 = 2.07 과 같은 수) |
| (개념만) "true geometrical tortuosity factor" | 정의식 없음 — Eq 4 가 협착 · CEI · 계면분극 · 공간전하를 따로 다루지 않아 이것과 달라질 수 있다는 문장에만 나온다 (p.5) | — | — | 가장 가까운 우리 양 = **τ_Lap,geom** (= √(φ_SE·σ_grain/σ_bulk_net), 협착을 뺀 망) — 그러나 **같은 양이 아니다** (τ_Lap,geom 은 협착 없는 *수송* τ, 원문 개념은 기하 tortuosity factor) | 원문 수치 없음 → 대조 불가 |

### 16-1. 판정 요약

| 우리 양 | 원문 대응 | 판정 |
|---|---|---|
| **T = τ_Lap,eff²** (웹앱, σ_full 기반) | 보고 τ_i² (Eq 4 보고값 꼴) | ✅ **같은 관례 · 같은 범주** (전체 단면 σ_eff · φ 별도 곱 · 협착·접촉 포함).  다른 것은 **σ₀ 기준** (16-2) |
| **τ_Lap,eff** | √(보고 τ_i²) | ✅ 같은 양 — 단 원문은 √ 를 보고하지 않는다 |
| **τ_Lap,geom** (σ_bulk_net, 협착 제외) | 없음 ("true geometrical" 은 개념만) | ⬜ 실험 짝 없음 |
| **τ_Dij · τ_Dij,all · 벽 τ** (기하 최단 경로) | Eq 3 τ_i = l_i/l_0 | ✅ 같은 범주 (정의; 분모 z 거리 vs 직선 거리) — ⚠ 원문 측정값 없음, **수치 앵커 아님** |
| **COMSOL τ_F** | 보고 τ_i² | ✅ 같은 양 (메인 제공 식 기준) |
| **인계 f · T · τ** | σ_eff/σ₀ · 보고 τ² · √ | ✅ f = φ/τ² · T = τ² · τ = √τ² — **σ₀ 정의 병기 필수** |
| (인쇄 Eq 4) | — | ❌ 오식 — 어느 우리 양과도 대응시키지 말 것 |

### 16-2. σ₀ 와 φ — 같은 식인데 숫자가 달라지는 두 자리
- **원문 σ_i,0 = 순수 시료 (펠릿) 의 EIS 겉보기값** — SE 1.6 mS/cm @25 °C (p.3; stainless steel · ~40 MPa, SI Fig S6) · NCM
  10 mS/cm (값 p.3 · "0 % SoC" p.4 · "fully lithiated NCM (10 mS cm⁻¹)" p.6).  SI §3: 그 펠릿에도 기공이 있어 측정 전도도를 낮추지만 τ² := 1 로 두었다 ⇒ **원문 τ² 는 "펠릿
  대비" 상대값**이다.  펠릿 기공 ε_p 와 펠릿 자체의 수송 인자를 모르므로 결정립 기준 τ² 와의 차이는 [미확인] — 방향만 확실하다:
  결정립 기준이면 τ² 가 **더 크다** (σ₀^펠릿 < σ_grain).
- **우리 σ₀** — 이온 망 간선의 σ_bulk = `se_material.sigma_grain_S_cm(T)` (25 °C 3.0 mS/cm) 이고 웹앱 τ 의 σ_grain 도 같은 출처라,
  `σ_full_mScm = (σ_eff/σ_bulk)·σ_bulk` 이므로 **τ_Lap,eff² = φ_SE / (σ_eff/σ_bulk)_망 — σ_grain 이 정확히 약분**된다 (τ 는 순수 망
  성질).  ⇒ 원문 T 는 "펠릿 기준", 우리 T 는 "망 간선 기준" — **이름이 같아도 기준이 다르다.**  (3.0 자체도 Cronau 2021 SI S2c
  펠릿값이지만 — 원장 CL-91 — 우리 τ 에서는 약분되고 σ_eff 절대값에만 들어간다.)  CL-91 의 "입력 σ 가 펠릿값이면 기공이 부분
  이중계상" 과 같은 구조가 **실험 쪽 τ² 에도** 있다.
- **φ_i** — 원문: (1 − 0.14)·φ_i,nom (평균 기공 하나를 전 조성에 공통) · 우리: DEM 기하 φ_SE (케이스별).  시료별 기공을 쓰면 원문
  τ_ion² 가 −3.5 ~ +7.4 % 움직인다 (§3).
- **fine-SE 행** — σ₀ = 1.6 (pristine) 으로 정규화.  밀링 SE 의 1.2 를 쓰면 τ_ion² 33.8 → 25.4.

### 16-3. Bruggeman (COMSOL 기본값) 이 원문 데이터에서 얼마나 빗나가나 (내 산술)

| φ_NCM % | φ_SE^(−½) | 보고 τ_ion² | τ_ion² ÷ Bruggeman | φ_NCM^(−½) | 보고 τ_el² | τ_el² ÷ Bruggeman |
|---|---|---|---|---|---|---|
| 25 | 1.28 | 2.40 | 1.9× | 2.01 | 120 | 60× |
| 33 | 1.37 | 3.23 | 2.4× | 1.76 | 13.7 | 7.8× |
| **42** | **1.50** | **4.27** | **2.8×** | **1.55** | **7.44** | **4.8×** |
| 53 | 1.74 | 15.3 | 8.8× | 1.37 | 4.77 | 3.5× |
| 61 | 2.01 | 130 | 65× | 1.28 | 4.29 | 3.4× |
| 61 fine SE | 2.01 | 33.8 | 17× | 1.28 | 8.79 | 6.9× |

⇒ COMSOL 에 Bruggeman τ_F 를 그대로 넣으면 42 vol% 에서 이온 τ_F 를 **2.8 배**, 61 vol% 에서 **65 배** 과소평가한다.  [6] Bielefeld
2020 카드의 "모델 τ² 가 Bruggeman 의 4 배" 와 같은 방향 (그 카드 기준).  ⚠ 원문 τ² 는 펠릿 기준이라 (16-2) 결정립 기준이면 배수는
더 커진다.

### 16-4. 인계 열 사전 계획 (f = σ_eff/σ₀ · T = φ/f · τ = √T) 에 원문 값을 넣으면

| 조성 | 상 | f = σ_eff/σ₀ | T = φ/f | τ = √T | σ₀ 기준 |
|---|---|---|---|---|---|
| 42 vol% | 이온 | 0.104 | 4.27 | 2.07 | 펠릿 1.6 mS/cm |
| 42 vol% | 전자 | 0.0556 | 7.44 | 2.73 | 펠릿 10 mS/cm |
| 61 vol% | 이온 | 0.00191 | 130 | 11.4 | 펠릿 1.6 mS/cm |
| 61 vol% | 전자 | 0.143 | 4.29 | 2.07 | 펠릿 10 mS/cm |

⚠ 인계 열 사전 계획 문구에는 σ₀ 의 정의가 없다 [미확인].  우리 f · T 를 망 간선 σ₀ (3.0 mS/cm, σ_full 과 같은 출처) 로 정의하면
원문 f · T (펠릿 σ₀) 와 **같은 이름 · 다른 기준**이 된다 ⇒ **열 사전에 "σ₀ = 무엇" 을 반드시 적는다**.  (원문 T 는 측정 σ₀ 값에
의존하고, 망 간선 기준의 우리 T 는 σ₀ 값에 무관하다 — 16-2.)

---

## §17. ⟦10-03 PDF 대조⟧ 원문 내부 불일치 · 오식 목록 (인용 전에 볼 것)

| # | 위치 | 원문 | 대조 | 판단 |
|---|---|---|---|---|
| 1 | 식 [4] (p.5) | τ_i² = (σ_i,eff/σ_i,0)·φ_i | 보고 τ² 는 φσ₀/σ_eff 로만 재현 (§4.3) | 오식 (σ 비 역전) |
| 2 | 본문 p.5 | 42 vol% σ_ion,eff 가 bulk 보다 "about four times lower" | 1.6/0.166 = 9.6×; τ² = 4.27 | 문장 오류 (σ_eff/σ₀ 와 τ² 혼동) |
| 3 | 본문 p.6 | 42 vol% 전자 τ² "above eight" | 본문 p.5 7.4 · Table S2 7.44 | 불일치 |
| 4 | 본문 p.3 | "a CAM loading of 214 mAh cm⁻²" | SI Table S3: 2.14 mAh cm⁻² (42 vol%) | 소수점 오식 |
| 5 | 본문 p.9 | 0.4 mS/cm · τ² 34 · 61 vol% → SE ≥ 47 mS/cm; τ² < 10 → 16 | 0.4·34/0.25 = 54.4 (47 은 φ_SE 0.288 일 때); 16 = 0.4·10/0.25 | 한 문단 안 φ 기준 혼용 |
| 6 | 본문 p.9 | "13 %–17 % (Table SIII)" | SI Table S1: 7.6 · 13 · 17 · 17 · 15 % | 범위가 7.6 % 시료를 뺌 |
| 7 | 본문 ↔ SI | "Table SII/SIII", "Fig. S2/S3/S4" | §10 대응표 | 번호 체계 불일치 (Fig S3→S1, Fig S4→S6, Table SII→S3, Table SIII→S1) |
| 8 | SI Table S1 | V_theo 열 | ρ_NCM ≈ 4.77 로만 재현 (본문 밀도 4.65; φ·τ² 는 4.65 로 재현) | 내부 불일치 |
| 9 | SI Table S1 | 60:40 행 φ_NCM 33 · φ_SE 53 | 재계산 32.4 · 53.6 | 반올림 표기 (합 86 맞춤으로 보임) |
| 10 | SI Table S4 표지 | "25 vol.-% CAM" | 값 = Fig 4 의 "33 vol.-%" 계열; 사이클 집합 (Table S3) 에 25 없음 | 표지 오기 |
| 11 | SI Table S4 ΔQ_dis | 0.25C "8.8" · 0.5C "−7.3" | 71.5 − 80.2 = −8.7 · 32.9 − 43.2 = −10.3 | 산술 · 부호 오식 |
| 12 | 본문 p.7 | 33 vol% VGCF "+13 % @0.1C" | SI Table S4: 방전 135 → 157 = +16 % (충전 137 → 159 = +16 %) | 불일치 |
| 13 | SI Table S5 (둘째, p.9) | 61 vol% coarse vs fine 충방전 용량 | Table S4 저-CAM 블록과 전 칸 동일; Fig S3 의 61 vol% 와 불일치 | 복사 오류 — **인용 금지** |
| 14 | Fig 5 범례 | "53 vol.-%" (왼) · "52 vol.-%" (오) | j · 비용량 = 47 vol% 셀 (Table S3, Fig 3) | 범례 오기 |
| 15 | Fig 6 오른쪽 | 축 "CAM-Specific Charge q_mat" | 판독 113 / 69 / 37 / 13 (coarse) = Fig 4b composite-specific 61 vol% 와 같고 Fig S3 의 ≈ 0.86 배 (= w_NCM 86 %) | 축 라벨 오기 가능성 (판독 기반 추정) |
| 16 | 본문 p.4 · SI §1 | z_el · z_ion [Ω m], z_int [Ω m⁻¹]; SI r_ion (Ω m), r_el (Ω m⁻¹) | 식 S6–S7 (R = L·r) 이면 r 은 Ω m⁻¹; 식 S1 무차원 조건이면 z_int 는 Ω m | 단위 표기 혼선 (계산 무영향) |
| 17 | SI Table S2 fine-SE 행 | τ_ion² 33.8 | σ₀ = 1.6 (pristine) 로만 재현; 밀링 SE 의 1.2 이면 25.4 | 정규화 선택 미기재 |
| 18 | 본문 Fig 1 캡션 vs SI §1 | r_el,2 = "interfacial charge transfer" vs "NCM-NCM particle contacts" | — | 서술 불일치 |
| 19 | SI p.4 | "using an average density of 14 % (Equation S8)" | 문맥상 porosity · 식 S9 | 낱말 · 식 번호 오식 |

---

## §18. ⟦10-03 PDF 대조⟧ 참고문헌 중 tortuosity 축 후속 (원문 목록 그대로 · 카드 유무 = 정본 `litdb/papers/` 파일 검색)

| 원문 번호 · 서지 (목록 그대로) | 정본 카드 | 왜 볼 만한가 |
|---|---|---|
| [6] A. Bielefeld, D. A. Weber, and J. Janek, ACS Appl. Mater. Interfaces, 12, 12821 (2020). | ✅ `bielefeld2020_effective_ionic_conductivity_binder` | **식 [4] 의 인용원** — 인쇄 오식을 원전 식으로 확정할 곳 (그 카드는 τ² = (σ_bulk/σ_eff)·ε_SE 로 기록) · 원문이 τ_ion² 2.4 → 15.3 을 이 모델과 비교 ("slightly higher than microstructural models generated by Bielefeld et al. have predicted", p.6) |
| [24] A. Bielefeld, D. A. Weber, and J. Janek, J. Phys. Chem. C, 123, 1626 (2019). | ✅ `bielefeld2019_microstructural_modeling_composite_cathode` | 원문이 "42 vol% 에서 모든 CAM 이 전자망에 연결되지는 않았다" 는 가정의 근거로 인용 (p.6) · CAM 분율·입도 → utilization·이온 tortuosity 모델 (p.2) |
| [32] Z. Siroma, N. Fujiwara, S. Yamazaki, M. Asahi, T. Nagai, and T. Ioroi, Electrochim. Acta, 160, 313 (2015). | ❌ | **식 [1] 의 원전** ("see Table 3 in Ref. 32, condition 'open-open'") — √z_int · (z_ion+z_el)^(3/2) 꼴을 원전으로 확인 |
| [26] Z. Siroma, T. Sato, T. Takeuchi, R. Nagai, A. Ota, and T. Ioroi, J. Power Sources, 316, 215 (2016). | ❌ | T-type TLM 을 복합 전극에 적용한 선행 — EIS→유효전도도 방법의 근거 |
| [25] N. Kaiser, S. Spannenberger, M. Schmitt, M. Cronau, Y. Kato, and B. Roling, J. Power Sources, 396, 175 (2018). | ❌ | 임피던스에서 유효 이온전도도 = tortuosity 를 끌어낸 선행 (p.2) · ">10 mS/cm 필요" 결론의 비교 대상 (p.9) |
| [43] D. Hlushkou, A. E. Reising, N. Kaiser, S. Spannenberger, S. Schlabach, Y. Kato, B. Roling, and U. Tallarek, J. Power Sources, 396, 363 (2018). | ❌ | 원문이 기공 13–17 % 의 비교 문헌 (p.9) 및 ASSB tortuosity 문헌 (p.5) 으로 인용 |
| [33] Y. Kato, S. Shiotani, K. Morita, K. Suzuki, M. Hirayama, and R. Kanno, The journal of physical chemistry letters, 9, 607 (2018). | ❌ | 사이클 데이터 적합으로 유효전도도·tortuosity 를 얻는 **EIS 와 독립인 방법** (p.2) — [6] 카드는 Kato 의 void 제외 ε 관례를 지적 (그 카드 기준) |
| [27] T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, and M. Tatsumisago, J. Electrochem. Soc., 164, A3960 (2017). | ❌ | NCM111–Li₃PS₄ 의 CAM 적재 ↔ 수송 스윕 (49 vol% 최적, p.7) — 같은 실험 축의 두 번째 점 |
| [61] J. Landesfeind, M. Ebner, A. Eldiven, V. Wood, and H. A. Gasteiger, J. Electrochem. Soc., 165, A469 (2018). | ❌ | "LIB 의 tortuosity factor 는 한 자릿수 낮다" (p.9) 의 근거 — 그 값이 τ² 척도인지 τ 척도인지 확인해야 비교가 성립 |
| [42] J. Landesfeind, J. Hattendorff, A. Ehrl, W. A. Wall, and H. A. Gasteiger, J. Electrochem. Soc., 163, A1373 (2016). | (이번 묶음에서 카드화 중 — `landesfeind2016_tortuosity_eis_electrodes_separators`) | LIB tortuosity 관례 (p.5 인용) — 정의 대조표에 행 추가 후보 |
| [31] A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Ning, J. Marrow, F. H. Richter, J. Janek, and A. Latz, ACS Appl. Mater. Interfaces, 12, 9277 (2020). | ❌ | utilization 정의의 출처 (p.6) — 우리 f_AM^cc 와 대응 |
| [59] Y.-G. Lee et al., Nat. Energy, 5, 299 (2020). | ❌ | warm isostatic pressing 으로 한 자릿수 기공 (p.9) — 기공 하한 맥락 |
| [28] T. Shi, Q. Tu, Y. Tian, Y. Xiao, L. J. Miara, O. Kononova, and G. Ceder, Adv. Energy Mater., 2, 1902881 (2019). | ✅ `shi2019_high_am_loading_particle_size_assb` | SE:CAM 입경비 최적 — 입경 효과 비교 (원문 권호 표기 "2" 그대로) |
| [30] J. Park, K. T. Kim, D. Y. Oh, D. Jin, D. Kim, Y. S. Jung, and Y. M. Lee, Adv. Energy Mater., 10, 2001563 (2020). | ✅ `park2020_digitaltwin_assb_foundational` | (§5 의 Park 2020 대응 문장 재검토용) |
| [34] G. F. Dewald, S. Ohno, J. G. C. Hering, J. Janek, and W. G. Zeier, Batteries Supercaps, 4, 183 (2021). | ❌ | DC 분극으로 유효 부분전도도 — EIS 대안 방법 (우선순위 낮음) |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

# Materials Design Principles for Air-Stable Lithium/Sodium Solid Electrolytes — Zhu & Mo (Angew. Chem. Int. Ed. 2020)

> slug `zhu2020_air_stable_se_design_principles` · DOI `10.1002/anie.202007621` · type `DFT (database thermodynamics, 실험 0)` · PDF `litdb/inbox/30. Angew Chem Int Ed - 2020 - Zhu - ….pdf` + **SI PDF** `30. anie202007621-sup-0001-misc_information.pdf` + **★ SI xlsx `anie_202007621_sm_miscellaneous_information.xlsx` 확보·전수 전사 완료 (2026-08-05)** (본문 5 pp Communication + SI 5 pp: Methods 2 pp·Fig S1·S2·refs + xlsx 6 시트 269 화합물) · digested `2026-07-17` (SI PDF 반영 2026-07-17 · **SI xlsx 전사 + 그림 재판독 2026-08-05** · **본문 재투입 #54 + 그림 기계판독 2026-08-06 → §14**) · status ✅ · 사용자 분류 `DFT`
> **검증 이력**: 1차 digest 2026-07-17(본문+SI PDF) · 2차 SI xlsx 전수 전사 + 그림 재판독 2026-08-05(§3b, 염화물 오프셋 오류 적발) · **3차 본문 재투입(#54) 중복 판정 + 그림 픽셀 검산 2026-08-06(§14 — 신규 내용 0건, 그러나 `Fig. 3` 색인 누락 복구 · Fig 2 x축 서술 정정 · Cr⁶⁺ 미해결 항목 해소)**
> elements: S, Cl, O, H, Li, Be, B, Na, Al, Si, P, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Cu, Zn, Ga, Ge, As, Sr, Y, Zr, Nb, Ag, Cd, In, Sn, Sb, Te, Ba, La, Ce, Pr, Nd, Sm, Gd, Tb, Dy, Ho, Er, Tm, Hf, Ta, W, Au, Hg, Pb, Bi
> methods: DFT, ESW
> **저자**: Yizhou Zhu*(UMD→Northwestern) · **Yifei Mo***(UMD) — **🔑 우리 grand-potential ESW 방법의 원저자 그룹**(Zhu/He/Mo ACS AMI 2015 · JMCA 2016 = 이 논문 ref [2] = 우리 ESW 계보의 그 논문) + **[Banik]의 Mo와 동일 인물**. Angew 2020, 59, 17472–17476 (Energy Storage Hot Paper).
> **저장소 전사본**: `db/properties/zhu2020_si_hydrolysis_energies.csv` (binary 99행) · `db/properties/zhu2020_si_redox_reactions.csv` (ternary 170행) — **문헌 소환값, 우리 계산 아님**(헤더에 명시).

---

## 0. 이 digest를 읽는 법
이 논문은 **"황화물 SE는 왜 공기(수분)에서 H₂S를 내며 죽는가, 어떤 양이온/음이온/조성이면 안 죽는가"** 를 실험이 아니라 **Materials Project 열역학 데이터베이스 하나로** 전 주기율표 스케일에서 답한다. 즉 우리 ESW(grand-potential)와 **완전히 같은 계산 장치**를, 전압축(μ_Li)이 아니라 **수분축(μ_H₂O, μ_H₂S)** 으로 돌린 것. 경험칙이던 HSAB("soft acid Sn/Sb가 S를 좋아해 대기안정")를 **가수분해 반응에너지(eV/H₂O)라는 단일 정량 지표**로 바꾼 원전이고, 이후 대기안정 논문들([Taklu] CuCl·[Li25] CuBr₂·[Ma24] Sn/Sb·[Yang25] La-O·[Fan26] 리뷰 §공기축)이 전부 이 프레임 위에 서 있다.
⚠ 용어 주의: 본문 "electrochemical stability"는 **환원(0 V vs Li/Li⁺) 안정성**을 뜻함 — 우리 산화 축(B①)이 아니라 **음극 축(E)**. 축 혼동 금지.

## 1. 한 줄 요약
Li/Na 황화물·염화물 총 **177종**(46 binary M–S + 52 Li–M–S + 65 Na–M–S + 14 Li–M–Cl)의 **가수분해 반응에너지**(H₂S/HCl 생성, eV/H₂O)와 **0 V 환원 반응에너지**를 MP 데이터베이스로 전수 계산 → (i) 수분 민감성의 근원은 **초안정 인산염 Li₃PO₄/Na₃PO₄ 형성 구동력**(Li₃PS₄ ΔG=−0.608 eV, 심지어 P₂S₅보다 나쁨), (ii) **HSAB 트렌드를 정량 재현**(Sn/Ge/Sb/Bi ≫ P; 최고는 후기전이금속 Zn/Cd/Cu/Ag와 In), (iii) **염화물·Na 화합물은 본질적으로 수분안정**, (iv) 수분+환원을 동시에 만족하는 **Li 황화물은 없음**(Na는 Sc/Y/Zr/란타나이드가 가능) — "cation 선택 가이드 차트"(Fig 3)로 설계 원칙 제시.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 질문 | 황화물 SE 가수분해(H₂S)의 열역학 전모 + 어떤 cation/anion/조성이 수분·환원 동시 안정인가 |
| 배경 | 산화물 도핑(P₂O₅·Bi₂O₃·ZnO·Fe₂O₃)은 H₂S 억제하나 σ 희생; HSAB 기반 Sn⁴⁺/Ge⁴⁺/As⁵⁺/Sb⁵⁺ 치환은 성공례 있으나 **경험/직관 의존 + 환원 안정성 희생**(Sn/Ge) |
| 갭 | cation·anion·Li/Na 함량의 수분안정 효과를 **체계적·정량적으로** 본 적 없음 |
| 방법 계보 | ref [2] Zhu/He/Mo 2015·2016 = grand-potential ESW 원전(=우리 방법) — 같은 장치의 **화학축(수분) 확장판** |
| 대상 | 실존 SE 조성이 아니라 **화학공간 전수** — MP에서 **hull 위 50 meV/atom 이내** 화합물 전부(준안정 포함, SI) + 자체 DFT 4종(Li₃AsS₄·Na₃AsS₄·Li₃YCl₆·Li₂ZrCl₆); 계열은 M–S·M–Cl·Li–M–S·Na–M–S·Li–M–Cl·**Na–M–Cl**(본문 없음, Fig S1에만). argyrodite·Cl-rich 자체는 직접 계산 안 함 |

## 3. 핵심 수치 (전부)
| # | 반응 / 항목 | 값 | 판정 |
|---|---|---|---|
| (1) | ½Li₂S + H₂O → LiOH + ½H₂S | **ΔG = +0.225 eV/H₂O** | Li₂S는 preset 조건서 안정(양수=불리) |
| (2) | Li₂S + H₂O → Li₂O + H₂S | +0.863 eV/H₂O | 산화물 경로 더 불리 |
| (3) | ½Na₂S + H₂O → NaOH + ½H₂S | **+0.416 eV/H₂O** | Na₂S가 Li₂S보다 더 안정 |
| (4) | Na₂S + H₂O → Na₂O + H₂S | +1.915 eV/H₂O | — |
| (5) | ¼Li₃PS₄ + H₂O → ¼**Li₃PO₄** + H₂S | **ΔG = −0.608 eV** | 강한 자발 = thiophosphate 과민성의 열역학 근원 |
| (6) | LiCl + H₂O → LiOH + HCl | **+0.977 eV/H₂O** (SI) | LiCl 수분안정의 정량치 — 우리 LiCl-buffer 서사 지지 |
| (7) | NaCl + H₂O → NaOH + HCl | +1.532 eV/H₂O (SI) | Na 염화물이 더 안정 |
| (8) | 2LiCl + H₂O → Li₂O + 2HCl | +2.368 eV/H₂O (SI) | 산화물 경로 더 불리 |
| (9) | 2NaCl + H₂O → Na₂O + 2HCl | +4.129 eV/H₂O (SI) | — |
| (10) | 2LiOH → Li₂O + H₂O | +0.413 eV (SI) | 습윤측 최종 안정 산물은 Li₂O가 아니라 **LiOH** |
| (11) | 2NaOH → Na₂O + H₂O | +1.083 eV (SI) | — |
| — | preset 조건 | H₂O 몰분율 **0.1 %**(= **300 K 상대습도 ~3 %**, SI), H₂S/HCl **1 ppm**(= 작업환경 허용노출한계, SI), T=300 K | Fig 1 주황 별; 모든 ΔG가 이 기준 |
| — | Sn⁴⁺/Ge⁴⁺/As⁵⁺/Sb⁵⁺ 환원전위 | **~1.0–1.5 V vs Li/Li⁺** (환원 반응에너지에서 환산) | 기존 실험과 일치 — 대기안정 cation의 환원 비용 |
| — | 데이터셋 | 46 M–S / 52 Li–M–S / 65 Na–M–S / 14 Li–M–Cl (+ binary M–Cl·**Na–M–Cl**은 Fig S1) | 개별 값 전표는 **SI xlsx(미보유)**; 화합물별 ~값은 Fig S2 막대 판독 가능 |

**정성 서열 (Fig 2, 황화물 가수분해)**: 후기전이금속 **Zn²⁺·Cd²⁺·Cu²⁺·Ag⁺ 최고** > 알칼리/알칼리토 양호 > 금속반도체(4–6주기) **Ga³⁺·Ge⁴⁺·Sn⁴⁺·Sb⁵⁺·Pb⁴⁺·Bi³⁺** (P⁵⁺보다 뚜렷이 좋음) > Y³⁺·Cr³⁺ 중간 > 초기전이금속 **Zr⁴⁺·Hf⁴⁺·Ta⁵⁺·Nb⁵⁺·Cr⁶⁺·W⁶⁺ 나쁨** ≈ 란타나이드(Li계) 나쁨 > **P⁵⁺·B³⁺·Be²⁺·Al³⁺ 최악**(Fig 2 왼쪽 끝, ~−0.5…−1.0 eV/H₂O). Na–M–S는 전반 상향(란타나이드 Na계는 거의 안정).

## 3b. ★★ SI xlsx 전수 데이터 (2026-08-05 확보·전사) — 이 digest의 새 본체

> 2026-07-17 판에서 "미보유"로 남겨 뒀던 **원소별 수치 전표**가 들어왔다. 이제 Fig 2·3·S1·S2의
> "판독 ~값"을 **정확값**으로 교체할 수 있고, 본문이 논의조차 안 한 **4.5 V 산화 + ESW 창**까지 손에 있다.
> ⚠ 전부 **문헌 소환값**이다 — 우리 db 절대값과 같은 표에 넣지 않는다.

### 3b.1 전사 + 검증 로그
| 시트 | 행 수 | 본문/캡션 주장 | 대조 | 내용 |
|---|---|---|---|---|
| `M-S` | **46** | "46 binary M–S" (Fig 2 캡션) | ✅ 일치 | 가수분해 반응식 + ΔG |
| `M-Cl` | **53** | 본문에 개수 언급 없음 | — (신규) | 가수분해 반응식 + ΔG |
| `Li-M-S` | **52** | "52 ternary Li–M–S" | ✅ 일치 | 0 V + **4.5 V** + 가수분해 + **ESW 양끝** |
| `Na-M-S` | **65** | "65 Na–M–S" | ✅ 일치 | 동일 |
| `Li-M-Cl` | **14** | "14 lithium ternary chlorides" (Fig 3 캡션) | ✅ 일치 | 동일 |
| `Na-M-Cl` | **39** | 개수 미명시 (Fig S1에만 존재) | — (신규) | 동일 |
| **합계** | **269** | 본문 기준 177 | **+92**(M–Cl 53 + Na–M–Cl 39) | |

**기계 검증 (전사 스크립트 자동)**
- 반응식 좌변 **H₂O 계수 = 1.0** — 269행 전부 통과(= per-H₂O 정규화 확인). 위반 0.
- 기체 생성물(H₂S/HCl) 계수 파싱 실패 0.
- 표본 19건 원본 재조회 대조 — 전부 `OK`: `Li₂S 0.225` · `Na₂S 0.416` · `P₂S₅ −0.156` · `B₂S₃ −0.901` · `Au₂S 1.339` · `LiCl 1.335` · `NaCl 1.880` · `PCl₅ −0.687` · `AgCl 2.688` · `Li₃PS₄ −0.594` · `Li₇PS₆ −0.682` · `LiNdS₂ −0.273` · `LiInS₂ 0.622` · `Na₃PS₄ −0.449` · `NaNdS₂ 0.221` · `Li₃YCl₆ 0.886` · `Li₂ZrCl₆ 0.632` · `Li₃InCl₆ 1.382` · `Na₃Nd₅Cl₁₈ 1.220`.
- **본문 대조**: Li₂S(+0.225)·Na₂S(+0.416)는 본문 식 (1)·(3)과 **소수 3자리까지 일치**. Li₃PS₄는 xlsx **−0.594** vs 본문 **−0.608**(Δ 0.014) — 규약 차이가 아니라 MP entry/버전 차이로 보인다(반응식은 동일 `¼Li₃PS₄+H₂O→H₂S+¼Li₃PO₄`). **인용 시 본문값 −0.608을 쓰고 xlsx −0.594를 병기**하면 안전하다.
- **자체 DFT 4종은 entry id 칸이 빈 행**으로 식별된다 — `Li₃AsS₄`·`Na₃AsS₄`·`Li₃YCl₆`·`Li₂ZrCl₆`. CSV에서 `mp_entry_id = n/a_own_DFT`. (`Li₄SiS₄`도 entry id 공란인데 SI Methods 목록엔 없음 — **미해결 1건**, 인용 시 주의.)

### 3b.2 ⚠⚠ 우리가 전사 중 발견한 것 — **염화물 부분압 규약 불일치** (이 논문의 실제 오류)
xlsx의 **황화물** 시트는 SI 본문과 맞는데, **염화물** 시트는 안 맞는다:

| | xlsx | SI 본문 식 | 차이 |
|---|---|---|---|
| LiCl + H₂O → LiOH + HCl | **1.335** | **+0.977** (식 6) | **0.358** |
| NaCl + H₂O → NaOH + HCl | **1.880** | **+1.532** (식 7) | 0.348 |
| ½Li₂S + H₂O → ½H₂S + LiOH | 0.225 | +0.225 (식 1) | **0** |
| ¼Li₃PS₄ + H₂O → H₂S + ¼Li₃PO₄ | −0.594 | −0.608 (식 5) | 0.014 |

차이 **0.357 eV = k_BT·ln(10⁶) @ 300 K = HCl 1 ppm 보정항**, 그리고 **HCl 1개당**이다.
증거 3중(전부 우리가 직접 확인):
1. **Fig 1b**(figure-read): 0.1 % 세로선이 μ_H₂O ≈ **−0.18 eV**, 1 ppm 가로선이 ≈ **−0.36 eV** = 정확히 k_BT·ln x. preset 별에서 LiCl/LiOH 경계까지의 세로 거리를 읽으면 ≈ **0.98** → **SI 본문 규약**.
2. **Fig S1**(figure-read): LiCl 초록 점선이 **≈0.98**, NaCl 주황 점선이 **≈1.53** → 기준선도 **SI 본문 규약**.
3. **그런데 같은 Fig S1의 LiCl·NaCl 데이터 점**은 **≈1.34·≈1.88**(= xlsx), **Fig 3c의 Li–M–Cl 14종 전부**도 xlsx와 정확히 일치(In 1.38·Cd 1.30·Zn 1.29·Ga 1.21·Sc 0.90·Y 0.89·Cr 0.845·Er 0.84·Mn 0.73·Zr 0.63·Fe³⁺ 0.62·Al 0.38·Fe²⁺ 0.30·Be −0.03).

→ **판정**: 논문의 **염화물 표·산점도는 HCl 1 ppm 보정을 빠뜨렸다**(H₂O 0.1 % 보정은 들어가 있음). 그 결과 **Fig S1 한 장 안에서 기준선과 데이터 점의 규약이 다르다** — "이 염화물은 LiCl 점선보다 위/아래"라는 판독이 **0.357 eV씩 어긋난다**. 독립 확인: 우리 환산 `xlsx − 0.357×n_HCl` 이 SI 본문값을 재현 — LiCl **0.978**(본문 0.977) · NaCl **1.523**(본문 1.532, Δ0.009는 SI 본문 Na 식들 자체의 내부 불일치 0.018 범위 안).
⚠ **오프셋이 HCl 개수에 비례하므로 순위까지 바뀐다** (n_HCl이 1인 반응과 2인 반응이 섞여 있다). CSV에 원본값(`_as_published`)과 우리 환산값(`_preset_OURS`)을 **둘 다** 넣었고, 환산은 **우리 추론**임을 헤더에 박아 뒀다.

**바뀌는 판정 (Li–M–Cl)** — 논문 그림에서는 전부 양수("전부 수분안정")인데, 논문 자신의 preset 조건으로 환산하면 **4종이 음수로 넘어간다**:

| | 그림/xlsx | 우리 환산 preset | n_HCl |
|---|---|---|---|
| Li₃InCl₆ | 1.382 | **0.935** | 1.25 |
| Li₂CdCl₄ | 1.298 | **0.941** | 1 |
| Li₂ZnCl₄ | 1.290 | **0.933** | 1 |
| LiGaCl₄ | 1.209 | **0.495** | 2 |
| Li₃ScCl₆ | 0.900 | **0.186** | 2 |
| **Li₃YCl₆** | 0.886 | **0.172** | 2 |
| Li₅CrCl₈ | 0.845 | 0.131 | 2 |
| Li₃ErCl₆ | 0.842 | 0.128 | 2 |
| Li₄Mn₃Cl₁₀ | 0.728 | 0.371 | 1 |
| **Li₂ZrCl₆** | 0.632 | **−0.082** ⚠ | 2 |
| LiFeCl₄ | 0.619 | −0.095 ⚠ | 2 |
| LiAlCl₄ | 0.383 | −0.331 ⚠ | 2 |
| Li₂FeCl₄ | 0.295 | −0.419 ⚠ | 2 |
| Li₂BeCl₄ | −0.033 | −0.747 ⚠ | 2 |

🔑 **Li₂ZrCl₆·Li₃YCl₆는 실제 할라이드 SE 후보**다. 그림대로면 "여유 있게 수분안정"(0.63·0.89)인데, 논문 자신의 조건으로는 **경계선(−0.08·+0.17)**이다 — 그리고 이쪽이 **실험(Li₃YCl₆·Li₂ZrCl₆는 습기에서 수화·열화)과 더 잘 맞는다**. 상위 3종(In/Cd/Zn)도 1.3급에서 0.93급으로 내려와 **거의 축퇴**한다.

### 3b.3 양이온별 가수분해 서열 — **정량 (경계값 포함)**
기준선: **Li₂S +0.225** / **Na₂S +0.416** (이 위면 Li₂S보다 수분에 강함). **0이 안정/민감의 경계**.

**Binary M–S 46종 전수 (eV/H₂O, 오름차순 = 나쁜 것부터)**
`BeS −1.053 · Al₂S₃ −0.910 · B₂S₃ −0.901 · SiS₂ −0.847 · HfS₂ −0.625 · Tm₂S₃ −0.583 · Er₂S₃ −0.568 · Ho₂S₃ −0.535 · Dy₂S₃ −0.511 · Tb₂S₃ −0.467 · ZrS₂ −0.459 · Sc₂S₃ −0.449 · Y₂S₃ −0.400 · La₂S₃ −0.365 · Gd₂S₃ −0.342 · TiS₂ −0.304 · Sm₂S₃ −0.303 · Ce₂S₃ −0.216 · Nd₂S₃ −0.191 · Ti₂S₃ −0.168 · Sb₂S₅ −0.167 · P₂S₅ −0.156 · Pr₂S₃ −0.140` ‖ **0 경계** ‖ `MnS +0.170 · Li₂S +0.225 · PbS₂ +0.236 · CaS +0.264 · SrS +0.359 · Ga₂S₃ +0.362 · K₂S +0.403 · GeS₂ +0.412 · Na₂S +0.416 · BaS +0.422 · SnS₂ +0.441 · Sb₂S₃ +0.535 · As₂S₃ +0.537 · FeS +0.550 · In₂S₃ +0.599 · Bi₂S₃ +0.750 · CuS +0.939 · CdS +0.948 · HgS +1.001 · Ag₂S +1.040 · ZnS +1.081 · Cu₂S +1.267 · Au₂S +1.339`

🔑 **경계는 Pr³⁺(−0.140)과 Mn²⁺(+0.170) 사이** — 0을 건너는 화합물이 없고 **0.31 eV 폭의 빈 구간(gap)** 이 있다. 즉 "수분안정/민감"이 연속 스펙트럼이 아니라 **두 무리로 갈린다**: 산화물이 황화물보다 훨씬 안정한 **oxophilic 양이온**(Be/Al/B/Si/초기TM/희토류) vs 그렇지 않은 **후기TM·중금속**.

**Li–M–S 52종 — 상·하위**
- **최악** `Li₅B₇S₁₃ −0.908` > `Li₃BS₃ −0.893` > `Li₈Nb₂S₉ −0.689` > **`Li₇PS₆ −0.682`** > `Li₇P₃S₁₁ −0.650` > `LiAlS₂ −0.631` > `Li₂WS₄ −0.602` > **`Li₃PS₄ −0.594`**
- **최상** `LiInS₂ +0.622` > `Li₃AsS₄ +0.434` > `LiGaS₂ +0.333` > `LiBiS₂ +0.306` > `LiSbS₂ +0.279` > `Li₄SnS₄ +0.276` > `Li₃VS₄ +0.254`
- **희토류(Li계) 전부 음수**: Ho/Er −0.309 · Tb −0.298 · Dy −0.295 · **Nd −0.273** · Pr −0.264 · Sm −0.261 · Gd −0.213 · Y −0.192 · Sc −0.187. (Li–La–S는 데이터셋에 **없음**.)
- **Li₂S(+0.225)보다 나은 Li 삼원 황화물은 52종 중 12종뿐** — In·As⁵⁺·Ga·Bi·Sb·Sn·V·K·Cu(일부)·Au·Ge·Cr³⁺.

**Na–M–S 65종**: 전반 상향. 최상 `NaInS₂ +0.732` · `NaBiS₂ +0.689` · `Na₃AsS₄ +0.686` · `Na₄SnS₄ +0.593` · `NaSbS₂ +0.541`. **희토류 Na계는 대부분 양수** (Nd +0.221 · Y +0.204 · La +0.199 · Pr +0.244 · Gd +0.234 vs Li계 −0.19…−0.31) — Li→Na 치환만으로 RE가 부호를 바꾼다. 최악은 여전히 B(−0.806/−0.841) · Si(−0.599) · P(−0.415/−0.449).

**Binary M–Cl 53종** (as-published; 우리 환산 preset은 `−0.357×n_HCl`): 음수는 **PCl₅ −0.687 · BCl₃ −0.120** 둘뿐, 나머지 51종 양수. 최상 `AgCl 2.688 · HgCl₂ 2.431 · KCl 2.177 · AuCl 2.046 · NaCl 1.880 · ZnCl₂ 1.809`. **LiCl 1.335**(→ preset 0.978). ⚠ 우리 환산 preset을 적용하면 **AlCl₃(−0.486)·SiCl₄(−0.540)·BeCl₂(−0.687)·ZrCl₄(−0.045)** 도 음수로 넘어간다.

### 3b.4 HSAB 논리와 맞나 — **부분적으로만 맞다**
논문은 "HSAB의 제1원리 정량화"로 프레이밍하지만, 전수 데이터를 세워 보면 **HSAB만으로는 서열이 안 나온다**.

| 검정 | 결과 | 판정 |
|---|---|---|
| soft acid(Cu⁺·Ag⁺·Au⁺·Cd²⁺·Hg²⁺)가 상위인가 | Au₂S 1.339 · Cu₂S 1.267 · Ag₂S 1.040 · HgS 1.001 · CdS 0.948 = **최상위 독점** | ✅ 강하게 성립 |
| hard acid(Be²⁺·Al³⁺·B³⁺·Si⁴⁺)가 최악인가 | −1.053 / −0.910 / −0.901 / −0.847 = **최하위 독점** | ✅ 강하게 성립 |
| **Sn⁴⁺·Sb⁵⁺·As⁵⁺** (실험에서 "HSAB soft acid 치환"으로 쓰이는 바로 그 셋) | **SnS₂ +0.441 (양수, 중상위)** / **Sb₂S₅ −0.167 (음수!)** / As₂S₃ +0.537 vs 자체 DFT Li₃AsS₄ +0.434 | ⚠ **엇갈림** — Sn은 성립, **Sb⁵⁺는 반증**(Sb³⁺ +0.535 ≫ Sb⁵⁺ −0.167) |
| **산화수 의존**이 원소 정체성보다 큰가 | Sb³⁺ +0.535 vs Sb⁵⁺ −0.167 (Δ0.70) · Cu⁺ 1.267 vs Cu²⁺ 0.939 · Ti³⁺ −0.168 vs Ti⁴⁺ −0.304 · Fe²⁺ 0.550 vs Fe³⁺(M–S 없음) | ⚠ **크다** — "soft acid 원소"가 아니라 **"그 산화수에서의 M–O 친화도"** 가 진짜 변수 |
| Zn²⁺(hard-ish borderline)가 왜 최상위인가 | ZnS +1.081 — HSAB상 Zn²⁺는 borderline인데 Ag⁺보다 위 | ⚠ HSAB로 설명 안 됨 |
| 희토류(hard acid)가 최악군인가 | Y/La/Nd/Sm −0.19…−0.40 = **중하위지만 Be/Al/B(−0.9급)보다 훨씬 낫다** | △ 연속적 |

🔑 **우리 판정**: 이 지도의 실제 구동변수는 "soft/hard"가 아니라 **가수분해 산물 산화물의 안정성**(= M의 oxophilicity)이다. HSAB는 그 **상관 대리지표**로서 양 끝(Cu/Ag/Au vs Be/Al/B)에서만 잘 맞고, **중간대(Sn/Sb/Ge/Ga/In)와 산화수 효과는 설명하지 못한다**. Li₃PS₄의 −0.594가 P₂S₅(−0.156)보다 나쁜 것도 HSAB로는 안 나오고 **Li₃PO₄라는 특정 산물의 초안정성**으로만 설명된다. → **우리 `air_hsab` 정성 tier를 "HSAB 등급"이라고 부르는 것 자체가 이 데이터에 비추면 부정확**하다(§10b-③).

### 3b.5 우리 관심 원소 — 표에 있는 것 전부 (eV/H₂O)
> 염화물은 `as-published → 우리 환산 preset` 병기. **Mg는 데이터셋에 아예 없다**(MgS·MgCl₂ 둘 다 부재 — Mg(OH)₂는 hydroxide 목록에 있는데도).

| 원소 | binary S | binary Cl | Li 삼원 S | Li 삼원 Cl | Na 삼원 |
|---|---|---|---|---|---|
| **P** | P₂S₅ −0.156 | PCl₅ −0.687→−1.401 | **Li₃PS₄ −0.594** · Li₇P₃S₁₁ −0.650 · **Li₇PS₆ −0.682** | — | NaPS₃ −0.415 · Na₃PS₄ −0.449 |
| **B** | B₂S₃ **−0.901** | BCl₃ −0.120→−0.834 | Li₅B₇S₁₃ **−0.908** · Li₃BS₃ −0.893 | — | Na₃B₅S₉ −0.806 · NaBS₂ −0.841 · Na₃BS₃ −0.552 |
| **Nd** | Nd₂S₃ −0.191 | NdCl₃ 1.298→0.584 | LiNdS₂ −0.273 | (없음) | NaNdS₂ **+0.221** · Na₃Nd₅Cl₁₈ 1.220→0.506 |
| **Sn** | SnS₂ +0.441 | SnCl₄ 1.127→0.413 | Li₂SnS₃ +0.169 · **Li₄SnS₄ +0.276** | — | Na₄SnS₄ +0.593 |
| **Sb** | Sb₂S₃ +0.535 / **Sb₂S₅ −0.167** | SbCl₃ 1.219→0.505 | LiSbS₂ +0.279 · Li₃SbS₃ +0.227 · **Li₃SbS₄ −0.016** | — | NaSbS₂ +0.541 · **Na₃SbS₄ −0.151** |
| **Zr** | ZrS₂ −0.459 | ZrCl₄ 0.669→−0.045 | (없음) | **Li₂ZrCl₆ 0.632→−0.082** | Na₂ZrS₃ +0.045 |
| **Y** | Y₂S₃ −0.400 | YCl₃ 1.131→0.417 | LiYS₂ −0.192 | **Li₃YCl₆ 0.886→0.172** | NaYS₂ +0.204 · Na₃YCl₆ 1.154→0.440 |
| **In** | In₂S₃ +0.599 | InCl₃ 1.035→0.321 | **LiInS₂ +0.622 (Li계 1위)** | **Li₃InCl₆ 1.382→0.935 (Cl계 1위)** | NaInS₂ +0.732 · Na₃InCl₆ 1.659→0.945 |
| **Ga** | Ga₂S₃ +0.362 | GaCl₃ 1.053→0.339 | LiGaS₂ +0.333 | LiGaCl₄ 1.209→0.495 | Na₄Ga₂S₅ +0.525 |
| **La** | La₂S₃ −0.365 | LaCl₃ 1.375→0.661 | **(없음)** | (없음) | NaLaS₂ +0.199 · Na₃La₅Cl₁₈ 1.328→0.614 |
| **Cu** | Cu₂S +1.267 / CuS +0.939 | CuCl 1.527→0.813 | Li₂Cu₄S₃ +0.130 · LiCuS +0.223 · Li₃CuS₂ +0.239 | — | Na₄Cu₂S₃ +0.484 |
| **Mg** | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 |
| **Al** (참고) | Al₂S₃ −0.910 | AlCl₃ 0.228→−0.486 | LiAlS₂ −0.631 | LiAlCl₄ 0.383→−0.331 | Na₃AlS₃ −0.306 |
| **Si** (참고) | SiS₂ −0.847 | SiCl₄ 0.174→−0.540 | Li₄SiS₄ −0.217 | — | Na₂Si₂S₅ −0.599 |

🔑 우리에게 직접 걸리는 세 줄:
- **B는 황화물에서 전 데이터셋 최악급**(binary −0.901, Li 삼원 −0.893/−0.908) — 그런데 **염화물 BCl₃도 −0.120(환산 −0.834)로 음수**. B는 S계·Cl계 **양쪽에서 나쁘고**, 유일한 탈출구가 **B–O로 남는 것**이다(B₂O₃는 이미 산화물이라 가수분해 반응 자체가 없다). §10b-② 참조.
- **Nd는 Li 황화물에서 −0.273(민감)인데 Na 황화물에서 +0.221(안정)** — 부호가 알칼리에 뒤집힌다. Li계에서 "Nd가 대기안정을 준다"는 주장은 이 표로는 **지지 안 됨**.
- **In이 S계·Cl계 양쪽 1위** (LiInS₂ +0.622 / Li₃InCl₆ 환산 +0.935). 논문이 명시 추천하는 유일한 도판트.

### 3b.6 본문에 없던 두 열 — **4.5 V 산화 + ESW 창** (우리 축과 직결)
xlsx ternary 4시트에는 `4.5V reaction / 4.5V reaction energy` 와 **`Cathodic limit` / `Anodic limit` (V vs Li/Li⁺ 또는 Na/Na⁺)** 가 들어 있다. **논문 본문은 이 중 어느 것도 논의하지 않는다** — 즉 인용 시 "본문에 없는 SI 데이터"라고 밝혀야 한다.

우리 계에 걸리는 값 (Li–M–S, V vs Li/Li⁺):

| 화합물 | cathodic | anodic | ΔE(0 V) | ΔE(4.5 V) | 가수분해 |
|---|---|---|---|---|---|
| **Li₇PS₆** (argyrodite 모체) | **1.708** | **2.129** | −1.460 | −2.224 | −0.682 |
| **Li₃PS₄** | 1.708 | 2.369 | −1.416 | −2.095 | −0.594 |
| Li₇P₃S₁₁ | 2.291 | 2.320 | −1.463 | −2.219 | −0.650 |
| Li₄SnS₄ | 1.720 | 2.220 | −1.023 | −2.153 | +0.276 |
| Li₃SbS₄ | 1.957 | 2.299 | −1.474 | −2.006 | −0.016 |
| Li₃InCl₆ | 2.282 | **4.176** | −1.045 | −0.324 | 1.382→0.935 |
| Li₂ZrCl₆ | 1.750 | **4.013** | −1.458 | −0.524 | 0.632→−0.082 |
| Li₃YCl₆ | 0.653 | **4.013** | −0.696 | −0.568 | 0.886→0.172 |

🔑 **Li₇PS₆ = 우리 comp1(Li₆PS₅Cl)의 Cl 없는 모체**이고, Zhu-Mo 스킴에서 창이 **1.708–2.129 V**다. 우리 comp1 환원한계 **1.242 V**와 비교하려면 **조성(Cl 유무)·구조·상집합이 전부 다르다**는 걸 먼저 말해야 한다 — 같은 물질의 두 값이 아니다(§9 참조).
🔑 **염화물의 anodic limit이 4.0–4.2 V** — "할라이드는 양극 쪽이 넓다"의 Zhu-Mo판 수치. 우리 [Son]/[Cha] 할라이드 서사와 같은 자릿수.

---

## 4. DFT/계산 방법 ★ (SI Methods 전문 반영)
- **code / DB**: 대부분 고체상은 **Materials Project 형성에너지** 직접 소환(고체는 **엔트로피·PV 항 무시** — ref [1]=Zhu/He/Mo 2015·2016 관례 명시). **자체 DFT는 MP에 없던 4종만**: Li₃AsS₄·Na₃AsS₄(enargite Cu₃AsS₄ iso-structure, **Pmn2₁**; Al-Qawasmeh & Holzwarth 2016), Li₃YCl₆(Asano 2018·Wang/Mo 2019 실험 구조), Li₂ZrCl₆(Li₂ZrF₆ iso-structure, **P3̄1m**).
- **DFT 세팅(그 4종)**: **VASP + PAW, GGA-PBE, ecut 520 eV**, pseudopotential **Li_sv·Na_pv·P·S**(표준 VASP), **MP 표준 anion correction** 적용. k-mesh·이완 조건은 SI에도 미기재(n/a); **DFT+U·vdW 언급 없음**.
- **hydroxide 고체 19종은 실험 표준생성엔탈피**(NIST-JANAF) — "벤치마크된 correction scheme이 없어서"라고 명시. 목록: LiOH·NaOH·KOH·RbOH·CsOH·Be/Mg/Ca/Sr/Ba(OH)₂·B(OH)₃·Al(OH)₃·Cd/Fe/Co/Ni/Cu/Pb/Mn(OH)₂.
- **기체 H₂O·H₂S·HCl: 실험 생성엔탈피+엔트로피**(NIST-JANAF), **T=300 K, 엔트로피는 기체 3종만** 포함. 부분압 보정 **Δμ(x)=k_B·T·ln x** (표준상태 기준); x(H₂O)=0.1 % = **300 K RH ~3 %**, x(H₂S)=1 ppm = **작업환경 허용노출한계**, HCl도 1 ppm. → **0 K hull이 아니라 유한-부분압 grand-potential**(전압축의 μ_Li를 μ_H₂O·μ_H₂S로 바꾼 것). **DFT(고체)+실험(기체·OH) 혼합 스킴**이라는 점이 방법의 핵심이자 주의점.
- **화합물 선정**: MP에서 **convex hull 위 50 meV/atom 이내** 전부(= 준안정 포함) + 자체 계산 Li₃AsS₄/Na₃AsS₄ 추가.
- **대표 가수분해 반응 선정 알고리즘 (SI 핵심, 재현 가능 수준)**: 후보 반응들을 **H₂O당 정규화 후 최저 ΔG 반응 채택** — "미량 H₂O가 과량 황화물/염화물과 반응하는" 극한의 수분민감도로 해석(저자 명시). 절차: **Step 1** LiₓMᵧS_z–LiₓMᵧO_z **pseudo-binary 상평형 프로파일**(hydroxide 제외)에서 출발 조성에 가장 가까운 전이 상평형 = 대표 반응 + 임계 μ_c(H₂O) 산출 → **Step 2** 그 계에 hydroxide M(OH)_t 존재 확인 → **Step 3** hydroxide↔oxide 전이 μ_t 계산, μ_t>μ_c면 Step 1 결과 확정 → **Step 4** μ_t<μ_c면 **"pseudo-oxide"** 상(조성 MO_{t/2}, E = E(M(OH)_t) − t·μ_c)을 상도에 삽입해 Step 1 재계산, μ_c′와 비교해 최종 확정(에너지는 실제 M(OH)_t 기준으로 환산). 산물 후보: Li₂S·Li₂O·M–S·M–O·Li–M–S·Li–M–O·M(OH)/LiOH·**oxysulfide/sulfate(M–S–O·Li–S–O)**.
- **predominance diagram**: (μ_H₂O, μ_H₂S) 2축 평면에서 Li₂S/LiOH/Li₂O (및 Na·Cl 계열) 안정영역 분할 — Pourbaix의 기체-화학 버전.
- **redox 안정성**: **0 V *와 4.5 V***(vs Li/Li⁺·Na/Na⁺) 반응에너지를 ref [1] grand-potential 스킴으로 전 화합물 계산, **alkali당 정규화 — 전표는 SI 첨부 xlsx**(✅ **2026-08-05 확보·전사**, §3b.6). 본문은 0 V(환원)만 사용; **4.5 V 산화 + cathodic/anodic limit(V)은 xlsx에만 있고 본문에서 논의 안 함**.
- **없는 것**: AIMD 0 · MLIP 0 · 무질서/고용체 처리 0 · **kinetics/표면 passivation 0** (저자 스스로 "kinetics도 중요, 고려해야" 명시). XSEDE/MARCC 크레딧은 위 4종 보조계산 몫으로 해석됨.

## 5. 결과 — 섹션별 상세

### 5.1 Binary 기준선 + predominance diagram (Fig 1)
Li₂S·Na₂S·LiCl·NaCl의 경쟁상은 hydroxide/oxide. (μ_H₂O, μ_H₂S/HCl) 평면에서 **Li 화합물 안정영역 < Na 화합물** (Li₂S·LiCl 영역이 좁음), **염화물 ≫ 황화물**. preset 조건(주황 별)에서 4종 모두 안정 쪽 — 단 μ_H₂O 높이면(습한 공기) Li₂S는 LiOH 영역으로 넘어감. 🔑 **"Li₂S는 0.1 % H₂O에선 열역학적으로 버틴다(+0.225 eV)"** — 습도 조건부 안정이지 절대 안정 아님.

### 5.2 Thiophosphate 과민성의 근원 (식 5)
¼Li₃PS₄+H₂O→¼Li₃PO₄+H₂S, **−0.608 eV/H₂O**. 게다가 **Li₃PS₄·Na₃PS₄는 자기 binary인 P₂S₅보다도 나쁨** — 일반 규칙("ternary는 M–S와 Li₂S의 중간") 의 유일한 명시적 예외. 이유: 가수분해 산물이 **초안정 인산염**(Li₃PO₄/Na₃PO₄)이라 구동력이 비정상적으로 큼. → 실험서 관찰되는 thiophosphate 초민감성(H₂S 폭발적 발생)의 열역학 설명.

### 5.3 Cation 전수 지도 (Fig 2)
§3 정성 서열 참조. 부가 논점:
- HSAB와 정합(soft-acid 금속반도체·후기TM이 S 선호→가수분해 저항) — **경험칙의 제1원리 정량화**.
- ZnO 나노입자 첨가가 H₂S 억제한 기존 실험(Hayashi 계열)과 일관(Zn²⁺ 최상위).
- **일반 규칙**: Li–M–S의 가수분해 에너지는 대략 **M–S(binary)와 Li₂S 사이의 내삽** — Li 함량↑ ⇒ Li₂S 수준으로 수렴. Na도 동일(Na₂S가 더 안정하므로 Na ternary 전반 우위).
- **란타나이드**: Li계에선 나쁨(음수), **Na계에선 거의 안정** — RE는 Na SE 쪽에서 대기안정 후보.

### 5.4 염화물 (Fig S1·S2·Fig 3c)
기준선(SI 정확값): **LiCl +0.977 / NaCl +1.532 eV/H₂O** — Fig S1의 초록/주황 점선. Binary 염화물은 **P⁵⁺(판독 ~−0.7)·B³⁺(판독 ~−0.1) 빼고 전부 양수**(수분 안정; Be²⁺는 ~0 경계, 판독); ternary Li–M–Cl 14종은 **Be²⁺(판독 ~−0.05) 빼고 전부 양수** — 최상위 In³⁺ ~+1.4 > Cd²⁺·Zn²⁺ ~+1.3 > Ga³⁺ ~+1.2, 중위 Sc³⁺·Y³⁺·Er³⁺·Cr³⁺ ~+0.85–0.90, 하위 Fe²⁺ ~+0.3·Al³⁺ ~+0.4 (전부 Fig S2 판독). **Na–M–Cl도 SI에서 조사됨**(Fig S1 주황 △, 개수 미명시) — 전반적으로 Li계 위. hydroxide→oxide 반응 (10)·(11)이 양수 = 습윤측 최종 산물은 산화물이 아니라 **LiOH/NaOH**. 염화물의 병목은 수분이 아니라 **환원**(Fig 3c: x축 −0.5…−3.0 eV 전부 음수 큼) — "halide SE는 대기 OK·음극 NG"의 열역학 원전([Son]의 할라이드 4 V 천장과 상보, 그쪽은 산화).

### 5.5 설계 가이드 차트 (Fig 3) — 수분(y) × 환원(x) 2축
- **Fig 3a (Li–M–S 52종)**: 오른쪽 위(둘 다 안정)가 목표인데 **거기 아무도 없음** — "Li 황화물로는 수분+Li금속 동시 안정 불가"가 이 논문의 가장 강한 부정 결과. P⁵⁺는 왼쪽 아래 구석(둘 다 최악, 실험과 일치). 기존 대기안정 cation(Sn/Ge/As/Sb)은 **왼쪽 위**(수분 OK·환원 NG, ~1.0–1.5 V). **희토류(Sc³⁺·Y³⁺·란타나이드, Nd 포함)가 Li 황화물 중 환원안정 최우수**(x가 가장 0에 가까운 군, 판독 ~−0.2…−0.5 eV), 수분은 Ti⁴⁺/Sb⁵⁺급(판독 ~−0.1…−0.4 = 약간 민감). **In³⁺ = 수분 최고(판독 ~+0.6) + 환원도 Sn/Ge보다 나음** → 도핑 후보로 명시 추천.
- **Fig 3b (Na–M–S 65종)**: **Sc³⁺·Y³⁺·Zr⁴⁺·대부분 란타나이드가 오른쪽 위** — Na SE는 환원+수분 동시 달성 가능. Na 금속전지의 구조적 이점.
- **Fig 3c (Li–M–Cl 14종)**: 수분 전부 안정(In³⁺·Cd²⁺ ~1.3 eV 최고)·환원 전부 불안정 — §5.4.

### 5.6 설계 원칙 (결론)
① 수분안정 cation 도핑/치환(신규 후보: In³⁺·후기TM·(Na계) RE/Zr) ② **Li/Na 함량 조절**(↑ ⇒ binary Li₂S/Na₂S 수준으로) ③ 염화물 물질군(수분 무문제, 환원만 관리) ④ Na 시스템의 본질적 우위(수분+환원+저비용 공정).

## 6. 논증 흐름 (한 문단)
binary predominance(Fig 1)로 기준선·조건 고정 → 대표 가수분해 반응 ΔG(eV/H₂O)를 전 cation에 일괄 적용(Fig 2) → "ternary=binary와 Li₂S의 내삽" 규칙 + 유일 예외 thiophosphate(인산염 구동력) → 여기에 환원축(0 V lithiation)을 직교로 붙여 2축 가이드 차트(Fig 3) → "Li 황화물론 동시 만족 불가, In/RE 도핑·Li함량·염화물·Na계가 출구" 설계 원칙으로 닫음.

## 7. Figure set ★
> 크로핑 `litdb/figures/zhu2020_air_stable_se_design_principles/` (5장). **2026-08-05에 실제로 본 것: Fig 1 · Fig 2 · Fig 3 · Fig S1** (4장) — **2026-08-06 재투입 때 같은 4장을 다시 봤고, `Fig. 2`는 픽셀 좌표까지 기계 판독했다(§14b)**. **안 본 것: Fig S2**(화합물별 막대그래프 — xlsx 정확값이 들어와 그림 판독이 불필요해졌다). 그림에서만 읽은 값은 `figure-read ≈`.
> ⚠ **`fig_3.png`는 2026-08-06까지 `figures.json`에 색인돼 있지 않았다**(디스크엔 있는데 목록엔 없음 → webapp의 `Fig. 3` 링크가 안 걸림). 원인·복구는 §14a.

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | predominance diagram: (μ_H₂O, μ_H₂S) 및 (μ_H₂O, μ_HCl) 평면. a=Li₂S/LiOH/Li₂O(좌)·Na₂S/NaOH/Na₂O(우), b=LiCl/LiOH/Li₂O(좌)·NaCl/NaOH/Na₂O(우). preset 주황별 = `figure-read ≈ (μ_H₂O −0.18, μ_gas −0.36) eV` (= k_BT·ln 10⁻³ / ln 10⁻⁶ ✓). Li/LiOH 세로경계 `figure-read ≈ −0.63 eV`, Na/NaOH `≈ −1.27 eV` (= 2MOH→M₂O+H₂O의 μ_t, SI 식 10·11과 정합) | **우리 comp1/modelc 가수분해 지도의 축·조건 템플릿**. 세로경계 = SI 알고리즘 Step 3의 **μ_t 그 자체** — 그림이 알고리즘을 그대로 보여준다. "조건 명시 없는 대기안정 주장 금지"의 시각적 근거 |
| 2 | 46 M–S(회색 ○)/52 Li–M–S(초록 ▽)/65 Na–M–S(주황 △) 가수분해 ΔG vs 양이온. y −1.0…1.5 eV/H₂O(프레임은 −1.10…1.50), x = **양이온 55칸 고정축**. ⚠ **"binary 값 오름차순"이 아니다** — 대체로 오르되 P⁵⁺·초기TM 블록에서 단조가 깨지고 4칸(Ta⁵⁺·Nb⁵⁺·W⁶⁺·Cr⁶⁺)은 binary M–S 자체가 없다(§14b-2). 점선 Li₂S `figure-read ≈0.22`·Na₂S `≈0.42` = xlsx 0.225/0.416 ✓ | **47-dopant cascade '수분축' 랭킹 원판** — 이제 판독이 아니라 **xlsx 정확값**(§3b.3)으로 인용한다. 차트 포맷(**공유 양이온 축 + 3계열 겹쳐 그리기 + 기준선 2개**)은 우리 cascade 그림에 그대로 차용 — 단 "정렬 = 값 순"이라고 캡션에 쓰면 이 논문과 같은 흠을 반복한다 |
| 3a | Li–M–S 52종: 가수분해 ΔG(y, −1.2…0.8) × 0 V 환원 ΔG(x, −2.0…0.15). **오른쪽 위(둘 다 안정) 비어 있음** — 이 논문의 가장 강한 부정 결과. In³⁺ 단독 최상단(`figure-read ≈ x −0.75, y +0.62`), P⁵⁺/B³⁺는 좌하단 구석, **희토류 군집이 x≈−0.2…−0.35(가장 0에 가까움)·y≈−0.2…−0.4** | **2축 multi-objective 도판트 선정 차트 = 우리 cascade 시각화 포맷**. RE 군집 = Nd 선택의 환원측 외부 지지(단 y는 음수 = 수분 손해) |
| 3b | Na–M–S 65종. **오른쪽 위가 채워진다** — Pr/La/Gd/Nd/Sm/Y가 x>0·y>0 박스, Zn/Hg/Au/Ga/In/Sn도 상단. Na 금속전지의 구조적 이점 | Li vs Na의 구조적 차이를 한 장으로 — "Li 황화물의 한계는 물질이 아니라 Li 자체"라는 논지 |
| 3c | Li–M–Cl 14종: y **−0.3…1.5**(Be²⁺ 한 종만 0 아래 — "전부 양수"가 아니다) × x −3.0…0(전부 음수). 판독값이 xlsx와 **정확히 일치**(In 1.38·Cd 1.30·Zn 1.29·Ga 1.21·Sc 0.90·Y 0.89·Cr 0.845·Er 0.84·Mn 0.73·Zr 0.63·Fe³⁺ 0.62·Al 0.38·Fe²⁺ 0.30·Be −0.03) | ⚠ **이 패널이 §3b.2 오프셋을 그대로 물려받는다** — preset 환산하면 Zr/Fe/Al/Be 4종이 음수로 내려간다. "할라이드는 대기 OK·음극 NG"의 원판이지만 **y축 절대값은 재인용 금지** |
| S1 | 염화물 산점도: M–Cl(회색 ○ 53)·Li–M–Cl(초록 ▽ 14)·**Na–M–Cl(주황 △ 39, 본문에 없는 계열)**. y −0.75…2.8 | 🔴 **우리가 오류를 잡은 그림**: LiCl 초록점선 `figure-read ≈0.98`·NaCl 주황점선 `≈1.53`(SI 본문 규약)인데 **같은 그림의 LiCl·NaCl 데이터 점은 ≈1.34·≈1.88(xlsx 규약)** — 기준선과 점의 규약 불일치(§3b.2). 판독 확인: 음수는 P⁵⁺ `≈−0.69`·B³⁺ `≈−0.12` 둘뿐 ✓ xlsx |
| S2 | 4계열 화합물별 가수분해 ΔG **막대그래프** | **이번에 안 봄** — xlsx가 같은 데이터를 정확값으로 주므로 그림 판독이 불필요. 필요 시 `fig_S2.png` |
| xlsx | **269 화합물 전표**(가수분해 + 0 V + **4.5 V** + **ESW 양끝**) | ✅ **확보·전사 완료** → `db/properties/zhu2020_si_*.csv` (§3b) |

## 8. Post-processing ★
- **무엇**: (i) 유한-부분압 grand-potential 가수분해 ΔG (eV/H₂O 정규화, **대표반응 = 최저 ΔG 선택 알고리즘** §4) (ii) predominance diagram (iii) **0 V·4.5 V** 반응에너지(eV/alkali) — 전부 convex-hull 부산물, NEB/Bader/COHP/DOS 없음.
- **도구**: pymatgen phase-diagram 계열로 추정(SI도 코드명 미기재; 명시는 MP DB + ref [1] 스킴). 단 **알고리즘 자체는 SI에 Step 1–4로 완전 명세** — pseudo-binary S–O 프로파일 + hydroxide pseudo-oxide 삽입(§4) → 우리가 그대로 재구현 가능.
- **수치화·기록**: 반응식+ΔG를 본문 식 (1)–(5) + SI 반응 6종(식 (6)–(11))으로, 전수 데이터는 산점도(Fig 2·3·S1)와 막대(Fig S2)로. **개별 조성 수치표는 SI xlsx(미보유)** — 특정 원소 정확값 인용은 xlsx 확보 후; 현재는 그림 판독 ~값(본 digest에 "판독"으로 명시).

## 9. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
| 항목 | Zhu2020 | 우리 | 일치/차이 + 이유 |
|---|---|---|---|
| **방법 계보** | grand-potential(μ_Li→μ_H₂O·μ_H₂S 확장), MP hull | grand-potential ESW(get_element_profile, μ_Li) | **✓✓✓ 동일 장치·동일 원저자(Mo 그룹)** — 이 논문 ref [2]가 우리 방법 원전. real difference 아님, 축만 다름(전압 vs 수분) |
| **가수분해 축(B④ moisture)** | 전 화학공간 계산 | **우리 계산 0** ("기체 H₂O/H₂S는 0K hull 밖"이라고만 해옴) | ✗ 우리 공백 — 단 Zhu 레시피(MP+NIST-JANAF 기체 μ)로 **우리 파이프라인에서 즉시 구현 가능** (§10-①) |
| thiophosphate 과민성 근원 | **Li₃PO₄ 형성 구동력**(식 5, −0.608 eV) | ICOHP **P–O −8.43 ≫ P–S −5.98**·O@PS₄ −0.67 eV/O·500 K AIMD P–O 자발형성 | **✓✓ 같은 물리의 두 층위**: Zhu=반응 열역학, 우리=결합 수준. O-doping(LPSOCl)은 이 구동력을 **합성 단계에서 선지불**하는 전략 — 우리 P–O 서사의 열역학 원전 |
| 환원 스킴 | 0 V lithiation ΔG (eV/Li) | 환원한계 1.242 V·0 V 산물 Li₃P+Li₂S+LiCl | ✓ 동일 방법; Zhu는 조성 스캔, 우리는 argyrodite 특정 — Zhu Fig 3a에서 P⁵⁺ 최악 = 우리 PS₄ 환원분해와 정합 |
| **RE(Nd) 도핑** | Li–M–S 중 **RE=환원안정 최우수**·수분 중하위(Fig 3a); "doping candidate" 명시 | Nd₂O₃ cascade(NdPO₄/NdCl₃ passivator·음극 Nd⁰+LiCl) | **✓ 환원측 외부 지지**(2020 계산 선례) — 단 **수분측은 Zhu상 Li–RE–S 음수(민감)** → "Nd가 대기안정도 준다" 주장 금지; [Yang25] La-O의 대기 개선은 **O(P–O) 몫**이지 RE 몫 아님(Zhu가 그 분리를 정량 근거로 뒷받침) |
| **B³⁺** | 황화물·염화물 양쪽에서 **최악급 가수분해**(Fig 2 왼쪽 끝 ~−0.9; 염화물 예외 P·B) | +B₂O₃ 도핑: 산화 onset +0.18 V·B–S −2.15 eV 안정화(전자·산화 축 이득) | **⚠ 축-긴장(real, 방법 아님)**: B–S 결합 형성은 **수분축(B④) 부채** 가능성 — B가 B–O 배위로 남으면 회피, B–S로 가면 Zhu 지도상 위험. B₂O₃ 조성의 가수분해 ΔG 확인 필요 (§10-②) |
| Li₂S(=free S²⁻ 유사체) | **0.1 % H₂O에선 +0.225 eV로 안정** | (우리 free-S 서사: 산화축에서 가장 취약한 자리) | **△ 뉘앙스**: "free S²⁻가 H₂S 원천"이라는 통념([Fan26] 공기축)과 달리, 저습도 열역학에선 **PS₄→PO₄ 전환이 주 엔진**이고 Li₂S형 S는 조건부 안정. 습도 올리면(μ_H₂O↑) Li₂S도 넘어감 — **조건 명시가 판정을 가름**(method-boundary, real difference 아님) |
| 염화물 수분안정 | LiCl 등 거의 전부 양수 — **LiCl+H₂O→LiOH+HCl +0.977 eV/H₂O**(SI 본문) / xlsx 1.335 | 우리 분해산물 LiCl(SEI/CEI 절연 buffer) | ✓ **LiCl 산물은 대기·수분에도 불활성**이라는 보너스 의미 부여(정량 인용 가능) — 단 Cl-rich *argyrodite*가 수분안정이란 뜻 아님(호스트는 여전히 황화물; [Wu] 90 °C calendar는 Cl-rich 열세). ⚠ **인용은 본문 0.977로** — xlsx/그림값 1.335는 §3b.2 오프셋 |
| **ESW 창** (xlsx 신규) | **Li₇PS₆ 1.708–2.129 V** · Li₃PS₄ 1.708–2.369 V · Li₇P₃S₁₁ 2.291–2.320 V (MP-GGA ordered 상, grand-potential) | comp1 환원한계 **1.242 V** · 산화 onset 2.256 V(LiS₄ 제외) | **⚠ 같은 물질 아님 — 직접 비교 금지**: Li₇PS₆는 **Cl 없는** argyrodite 모체이고 우리는 Li₆PS₅Cl. 차이(1.708 vs 1.242)는 **조성(Cl)·구조·상집합**이 전부 달라서지 방법 차이가 아니다. **✓ 방법 계보는 동일**(둘 다 Zhu/He/Mo 스킴) → **A6 검산 앵커**로 쓰는 게 맞는 용법(§10b.2): 우리 파이프라인에 Li₃PS₄를 넣어 1.708–2.369가 나오는지 확인 |
| **4.5 V 산화** (xlsx 신규) | Li₃PS₄ ΔE=−2.095 · Li₇PS₆ −2.224 eV/Li (전 화합물 계산됐으나 **본문 미논의**) | 우리 산화 4축(B①–④) | ✗ **아직 아무도 안 쓴 데이터** — 우리 B① 산화 onset 서사에 외부 대조군으로 붙일 수 있는 미개척 칸. 단 4.5 V **고정 전압 1점**이라 우리 onset(연속 μ_Li 프로파일)과 축이 다름 |
| gap/σ/기계 | 없음(전부 n/a) | — | 비교 대상 아님 |
| 무질서·kinetics | 0 (ordered MP 상·열역학만; 저자도 passivation 별도 명시) | 우리도 0K hull 동일 한계 + 표면 kinetics 없음 | ✓ 같은 한계 공유 — 실험 H₂S 발생량(cm³/g)과의 정량 대응은 양쪽 다 불가(방향·서열만) |

## 9b. 심사 중인 리뷰 [Fan26]가 이 논문에서 무엇을 가져갔나 (ref [84] 감사)
> `papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md` (ECER-D-26-00097) §3.1 전략① 말미와 §4 표에서
> **ref 84 = 이 논문**. 리뷰 자신의 **Fig 3b**로 "가수분해 반응에너지 원소 지도 + 환원안정성 2D 선택 차트"를 싣는다.
> 리뷰어 노트: `kb/reviews/ECERD2600097_review_notes.md`.

| 항목 | 리뷰가 가져갔나 | 판정 |
|---|---|---|
| Fig 2 원소 지도 (가수분해 ΔG vs 양이온) | ✅ 가져감 (Fig 3b 왼쪽) | 정확히 인용 |
| Fig 3 2축 선택 차트 (수분 × 환원) | ✅ 가져감 (Fig 3b 오른쪽) | 정확히 인용 |
| "강한 M–S 결합 양이온 치환" 프레임 | ✅ — §3.1 전략①에 "격자 경도↑·분극률↓"로 서술 | ⚠ **원문과 다른 근거**: Zhu의 지표는 M–S 결합세기가 아니라 **가수분해 산물(산화물) 안정성**이다. 리뷰의 "M–S 결합 강화" 해석은 HSAB 서사에 맞춘 재포장 — §3b.4의 Sb³⁺/Sb⁵⁺ 반전이 그 해석을 반증 |
| **부분압 조건 (0.1 % H₂O = RH ~3 %, 1 ppm H₂S)** | ❌ **안 가져감** | 🔴 **가장 큰 누락**. Zhu의 모든 판정이 이 조건부인데 리뷰는 "moisture stable/sensitive"를 무조건부로 옮긴다. Li₂S가 +0.225로 "안정"인 것도 이 조건에서만 — 리뷰 §3.1의 "S²⁻가 가수분해를 일으킨다"와 정면 긴장 |
| **부정 결과: Li 황화물 중 수분+환원 동시 만족 0** | ❌ 안 가져감 | 리뷰는 도핑을 해법으로 제시하는데, 원전은 **"Li 황화물로는 안 된다"**고 못박는다. 리뷰의 낙관을 원전이 지지하지 않는다 |
| **Li₃PO₄ 형성 구동력 = thiophosphate 과민성의 근원** (−0.608) | ❌ 안 가져감 (리뷰는 HSAB S²⁻/H⁺로 설명) | 🔑 **우리 O-doping 서사에 유리한 누락** — 리뷰가 안 쓴 정량 근거가 우리 P–O ICOHP 서사와 직결(§9) |
| 염화물 데이터 (Fig S1·3c, "대기 OK·음극 NG") | ❌ 안 가져감 | 리뷰 §공기축은 황화물만. 우리 LiCl-buffer 논의는 원전을 직접 인용해야 |
| Na 계열 우위 | ❌ 안 가져감 | 리뷰 범위 밖(황화물 Li) — 정당한 누락 |
| 4.5 V 산화 / ESW 창 (xlsx) | ❌ (원전 본문에도 없음) | 아무도 안 쓴 데이터 — **우리가 먼저 쓸 수 있는 칸** |
| **Li 함량 규칙** (삼원 ≈ M–S와 Li₂S의 내삽) | ❌ 안 가져감 | 도핑 설계에 바로 쓰이는 규칙인데 누락 |

**한 줄 판정**: 리뷰는 이 논문에서 **그림 두 장(원소 지도 + 2축 차트)만** 가져가고, **조건·부정 결과·인산염 구동력·염화물·Li 함량 규칙은 전부 버렸다**. 그래서 리뷰의 §3.1은 "soft-acid 치환하면 대기안정해진다"는 낙관으로 읽히는데, **원전은 같은 데이터로 "Li 황화물에서는 수분을 얻으면 환원을 잃는다"는 trade-off를 말한다**. → 리뷰어 노트 A2("HSAB=열역학인데 속도론으로 연결")와 같은 계열의 문제이고, **리비전 코멘트로 "ref 84의 조건 명시와 trade-off를 함께 인용하라"**를 붙일 근거가 이 digest에 생겼다.

## 10. 적용 인사이트 (내 연구에 어떻게)
1. **🔑 B④ moisture 축을 "못 하는 것" 목록에서 지울 수 있다 — SI로 '레시피'가 '절차 명세'로 격상**: MP hull(+50 meV 준안정 창) + NIST-JANAF 기체(H₂O/H₂S) 실험 μ + Δμ=k_BT ln x 부분압 보정 + **대표반응 알고리즘(pseudo-binary S–O 프로파일→최저 ΔG, hydroxide는 pseudo-oxide 삽입; §4 Step 1–4)** — 전 단계가 SI에 재현 가능 수준으로 명세됨. 우리 6원소(+도판트) chemsys에서 comp1/modelc/**LPSOCl(+O)/+B₂O₃/Nd-doped**의 가수분해 ΔG(eV/H₂O)를 같은 조건(0.1 % H₂O=RH ~3 %/1 ppm)으로 계산하면 — [Yang25] H₂S 실측·[Taklu]/[Li25] HSAB 주장들과 우리를 잇는 **정량 다리**가 생긴다. 예상: O-doped가 ΔG 덜 음수(구동력 선지불), 산물에 Li₃PO₄. 재구현 시 주의: 고체 엔트로피/PV 무시·hydroxide는 실험값(무보정)·엔트로피는 기체만 — 같은 혼합 규칙을 써야 Zhu 수치와 비교 가능.
2. **+B₂O₃의 수분 리스크 체크가 급소**: 우리 B 서사는 산화·전자 축 이득인데, Zhu 지도에서 **B³⁺는 S계·Cl계 모두 가수분해 최악급**. B₂O₃-doped 조성의 가수분해 ΔG와 B 배위(B–O 유지 vs B–S 형성)를 확인해 "B는 산화축 이득·수분축 중립(B–O 유지 시)"으로 방어선을 미리 치자 — 리뷰어가 이 논문 들고 물어볼 자리.
3. **Nd 서사의 축 정리**: Zhu가 RE를 "Li 황화물 중 환원안정 최우수 + doping 후보"로 2020년에 이미 지목 — 우리 Nd 선택의 외부 계산 선례로 인용. 단 **수분 개선은 O의 공로로 명확히 분리**(Li–RE–S는 Zhu상 수분 음수). [Yang25]와 3자 정합: RE=환원/interphase, O=대기.
4. **인용·프레임**: 대기안정 주장엔 항상 **조건(습도 부분압) 명시** — Zhu의 Li₂S 조건부 안정이 교훈. 또 "HSAB적으로 안정" 대신 "가수분해 반응에너지 기준(Zhu 스킴)"으로 말하면 정량 인용 가능.
5. **차트 포맷 차용**: Fig 3의 2축(수분×환원) 가이드 차트에 우리 축(σ-blocking·산화 onset·기계)을 붙인 다차원 cascade 차트 = deck/논문 Figure 후보.

## 10b. ★★ B④ moisture 축 실행 레시피 — 이제 정답지까지 있다 (`kb/open_items.md` §H 대응)
> `comparison_vs_ours.md` §H가 *"가수분해(수분) 축 — B④ moisture ΔG_hyd 계산 **0**"* 을 열어 두고 [Zhu20]을
> 레시피 원전으로 지목해 왔다. SI PDF로 **절차**가 왔고, 이번 xlsx로 **정답지(검산 앵커)** 가 왔다.
> ⚠ **우리는 아직 가수분해를 한 건도 계산하지 않았다.** 아래는 실행 계획이지 결과가 아니다.

### 10b.1 절차 — 우리 언어로 (SI Step 1–4 재서술)
| 단계 | 무엇을 하나 | 필요한 입력 | 우리 보유 |
|---|---|---|---|
| **0. 기준 에너지 세팅** | 고체는 MP 형성에너지(GGA-PBE + MP anion correction), **엔트로피·PV 무시**. hull 위 **50 meV/atom 이내 전부** 포함(준안정 포함) | MP API key, chemsys | ✅ (우리 hull 파이프라인 그대로) |
| **0'. 기체·수산화물 예외 처리** | H₂O·H₂S·HCl은 **NIST-JANAF 실험 ΔH+S @300 K**, 수산화물 19종도 **실험 ΔH**(DFT 아님) | JANAF 표 값 하드코딩 | ⚠ **새로 넣어야 함** — 우리 파이프라인에 기체 μ 자리가 없다 |
| **0''. 부분압 보정** | `Δμ(x) = k_BT·ln x`; preset `x(H₂O)=10⁻³`(RH ~3 % @300 K), `x(H₂S)=x(HCl)=10⁻⁶`. 수치로 **−0.1786 / −0.3572 eV** | — | ✅ 한 줄 |
| **1. pseudo-binary 프로파일** | `Li_xM_yS_z – Li_xM_yO_z` 축을 따라 상평형 프로파일을 뽑고(**수산화물 제외**), 출발 조성에 **가장 가까운 전이 상평형**을 대표 반응으로. 임계 `μ_c(H₂O)` 동시 산출 | pymatgen `PhaseDiagram` + `get_transition_chempots` 계열 | ✅ 우리 ESW의 `get_element_profile`과 같은 장치 |
| **2. 수산화물 존재 확인** | 그 계에 `M(OH)_t`가 있나? 없으면 **Step 1이 최종** | 수산화물 19종 목록 | ✅ |
| **3. μ_t 계산** | `M(OH)_t ↔ MO_{t/2}` 전이 화학퍼텐셜 `μ_t`. **μ_t > μ_c 면 Step 1이 최종** | — | ✅ |
| **4. pseudo-oxide 삽입** | `μ_t < μ_c`면 조성 `MO_{t/2}`, 에너지 `E = E(M(OH)_t) − t·μ_c` 인 **가상 상**을 상도에 넣고 Step 1 재계산 → `μ_c′`. `μ_c > μ_c′`면 Step 4 채택, 아니면 Step 1. **에너지는 실제 `M(OH)_t` 기준으로 환산** | — | ✅ |
| **5. 대표 반응 선정** | 후보 반응 전부 **H₂O 1몰로 정규화**한 뒤 **ΔG 최저**를 채택 (= tracer-H₂O 극한: 미량 물 vs 과량 황화물) | — | ✅ |
| **산물 후보 집합** | `Li₂S · Li₂O · M–S · M–O · Li–M–S · Li–M–O · M(OH)_t/LiOH · oxysulfide/sulfate(M–S–O, Li–S–O)` | 우리 chemsys에 **S–O 화합물(Li₂SO₄ 등) 포함 필수** | ⚠ 확인 필요 |

🔑 **Fig 1이 이 알고리즘의 그림 버전**이다: 세로 경계 = Step 3의 `μ_t`(Li ≈ −0.63 / Na ≈ −1.27 eV, `figure-read`), 대각선 = Step 1의 전이, 별 = preset. 구현 후 **Fig 1을 재현하는 것이 첫 단위테스트**다.

### 10b.2 검산 앵커 — xlsx의 어느 값으로 우리 구현을 검증하나
우리 계(Li–P–S–Cl–O–B–Nd)의 구성 이성분·삼성분 중 **xlsx에 정답이 있는 것**을 순서대로:

| 순위 | 검산 대상 | 정답 (xlsx / 본문) | 왜 이것부터 |
|---|---|---|---|
| **A1** | `½Li₂S + H₂O → ½H₂S + LiOH` | **+0.225** (본문 식 1과 일치) | 가장 단순. 수산화물 실험값 + 기체 μ + 부분압이 **전부** 걸리는 최소 테스트. 여기서 틀리면 그 아래는 볼 필요 없음 |
| **A2** | `LiCl + H₂O → HCl + LiOH` | **본문 +0.977** (xlsx 1.335는 §3b.2 오프셋) | HCl 축 검증 **+ 우리가 어느 규약을 쓰는지 확정**. 0.977이 나오면 우리 구현이 논문 *본문* 규약. 1.335가 나오면 HCl 보정을 빠뜨린 것 |
| **A3** | `2LiOH → Li₂O + H₂O` | **+0.413** (SI 식 10) | 수산화물↔산화물 `μ_t` 자체 = Step 3 단위테스트. Fig 1의 세로선 위치와 동치 |
| **A4** | `¼Li₃PS₄ + H₂O → H₂S + ¼Li₃PO₄` | **본문 −0.608 / xlsx −0.594** | **우리 계의 핵심 반응**. Step 1(S–O pseudo-binary)이 제대로 도는지. 산물이 Li₃PO₄로 나와야 함 |
| **A5** | `Li₇PS₆` (argyrodite 모체) | **−0.682**, ESW 1.708–2.129 V | comp1에 가장 가까운 xlsx 화합물. **Cl 없는 우리 계**의 정답지 |
| **A6** | `Li₃PS₄` 0 V/4.5 V + ESW | ΔE(0V) −1.416 · ΔE(4.5V) −2.095 · **1.708–2.369 V** | 우리 ESW 파이프라인이 Zhu-Mo 스킴을 재현하는지 (가수분해와 독립 검증) |
| **A7** | `B₂S₃` / `Li₃BS₃` | **−0.901 / −0.893** | +B₂O₃ 리스크 판정의 기준선 (§10b.3-②) |
| **A8** | `Nd₂S₃` / `LiNdS₂` / `NdCl₃` | **−0.191 / −0.273 / 1.298(→0.584)** | Nd 도핑 서사의 수분측 기준선 |

⚠ **A1–A3이 통과해야 A4 이후가 의미 있다.** 그리고 **A1·A3(황화물·수산화물)은 xlsx=본문이라 안전**하지만, **A2(염화물)는 두 값 중 어느 쪽을 목표로 하는지 먼저 정하고 시작해야 한다** — 우리는 **본문 규약(0.977)** 을 목표로 잡는다(preset 조건 정의와 일치하므로).
⚠ **재현 규율**: 고체 엔트로피/PV 무시 · 수산화물 무보정 실험값 · 엔트로피는 기체 3종만 · hull+50 meV 준안정 포함 — **같은 혼합 규칙을 써야 Zhu 수치와 비교 가능**. 규칙 하나만 바꿔도 ±0.1 eV급으로 흔들린다.

### 10b.3 그 다음 — 우리 조성에 돌릴 때
① **대상**: `comp1(Li₆PS₅Cl)` · `modelc(LPSCl1.6)` · `LPSOCl(+O)` · `+B₂O₃` · `Nd-doped`. 예상 결과와 그 의미:
- LPSOCl은 **ΔG_hyd가 덜 음수**여야 한다 — O-doping이 Li₃PO₄ 형성 구동력을 **합성 단계에서 선지불**했으므로. 그게 안 나오면 우리 O-doping 서사의 열역학 해석을 재검토해야 한다.
- 산물에 **Li₃PO₄가 나오는지**가 §5.2 서사의 직접 확인.
② **⚠ +B₂O₃가 급소**: B는 **황화물 최악(−0.90)·염화물도 음수(BCl₃ −0.120→환산 −0.834)** 다. 유일한 방어선은 **B가 B–O 배위로 남는 것**. 그러므로 계산 목표는 "B₂O₃-doped의 ΔG_hyd 값" 하나가 아니라 **분해 산물에서 B가 어디로 가는가**(B–O 유지 vs B–S 형성)다. 리뷰어가 이 논문을 들고 물어볼 자리 — 미리 답을 만들어 둔다.
③ **`air_hsab` 정성 tier의 승급 — 차이와 한계**:

| | 지금 (`air_hsab`) | Zhu 정량축 | 승급 시 문제 |
|---|---|---|---|
| 값 | 4단 큐레이션 `0.2 / 0.45 / 0.6 / 1.0` (47 도판트, 32종이 0.2 동점) | 연속 ΔG (eV/H₂O) | ✅ 동점 해소 — 0.2 동점 32종이 −0.9…+0.6으로 펼쳐진다 |
| 근거 | HSAB soft-S 친화 + F 보너스 (**우리 계산 아님**) | 반응 열역학 | ✅ 근거 격상 |
| 이름 | "HSAB 등급" | — | 🔴 **이름부터 부정확**: §3b.4대로 실제 구동변수는 soft/hard가 아니라 **oxophilicity(산물 산화물 안정성)**. Sb³⁺(+0.535) vs Sb⁵⁺(−0.167) 반전을 HSAB는 못 낸다 → **`air_dGhyd`로 개명**하고 HSAB는 해석 주석으로 강등 |
| 대상 | 도판트 **산화물**(B₂O₃·Nd₂O₃·ZnO…) 47종 | 도판트의 **황화물/염화물** | 🔴 **범주 불일치** — 산화물은 가수분해 반응 자체가 (거의) 없다. "도판트가 들어간 뒤 형성되는 M–S 종"을 대상으로 재정의해야 한다 |
| 커버리지 | 47 도판트 | Mg **없음**, Co/Ni/Mo **없음**, La는 Li계 없음 | ⚠ 우리 47종 중 **일부는 Zhu 표에 정답이 없다** → 그 칸은 우리가 직접 계산하거나 `n/a`로 남긴다. **문헌값으로 채운 칸과 우리 계산 칸을 반드시 구분 표시** |
| 게이트 승격 | `screening_roadmap` §8: 큐레이션 값은 **게이트 승격 금지** | — | 우리가 직접 계산한 칸만 게이트로 쓸 수 있다. Zhu 소환값은 **참조열**로만 |

④ **[Yang25] H₂S 실측·[Taklu]/[Li25] HSAB 주장과의 다리**: 우리가 A1–A8을 통과한 뒤 우리 조성 ΔG_hyd를 내면, 문헌의 정성 주장과 실측 H₂S(cm³/g) 사이에 **정량 중간항**이 생긴다. ⚠ 단 **열역학 서열 ↔ 실측 발생량은 1:1 대응 불가**(kinetics·표면적·결정성) — 방향과 서열까지만.

## 11. 인용 가능 문장 (deck/paper용)
- "Zhu & Mo's database thermodynamics traces the moisture hypersensitivity of thiophosphates to the formation of highly stable Li₃PO₄ (ΔG_hyd = −0.608 eV/H₂O for Li₃PS₄); our ICOHP (P–O −8.43 vs P–S −5.98) and O-site preference (−0.67 eV/O) provide the bond-level counterpart, and O-doping pre-pays exactly this driving force."
- "Rare-earth cations were computationally identified (Zhu 2020) as the most reduction-tolerant dopants among lithium sulfides — an external precedent for our Nd-based cascade — while their moisture benefit is marginal, so the air-stability gain of RE–O co-doping must be credited to P–O bond formation."
- "Hydrolysis energetics are condition-dependent: even Li₂S is thermodynamically stable at 0.1 % H₂O (+0.225 eV/H₂O) — air-stability claims require an explicit humidity chemical potential."
- "Across the 269 compounds tabulated by Zhu & Mo, the hydrolysis energy of binary sulfides splits into two disjoint groups separated by a 0.31 eV gap (Pr₂S₃ −0.140 to MnS +0.170 eV/H₂O), indicating that moisture tolerance is governed less by a continuous soft/hard-acid scale than by whether the cation's oxide is markedly more stable than its sulfide."
- "The soft-acid rationale holds at the extremes (Au⁺/Cu⁺/Ag⁺ ≥ +1.0 vs Be²⁺/Al³⁺/B³⁺ ≤ −0.90 eV/H₂O) but not in between: Sb³⁺ (+0.535) and Sb⁵⁺ (−0.167) differ by 0.70 eV for the same element, so oxidation state — not softness alone — sets the hydrolysis energy."
- ⚠ **내부용 (외부 인용 전 재확인 필요)**: "In the published spreadsheet and the chloride scatter plots, hydrolysis energies of chlorides appear to omit the 1 ppm HCl partial-pressure term (0.357 eV per HCl at 300 K) that the SI text applies; correcting for it moves Li₂ZrCl₆ (0.632 → −0.08) and LiAlCl₄ (0.383 → −0.33 eV/H₂O) to the moisture-sensitive side." — **우리 유도**이지 논문 주장이 아니다.

## 12. 주의/한계 (over-claim 방지)
- ✅ **SI PDF + xlsx 전부 확보 (2026-08-05)**: 대표반응 알고리즘·DFT 세팅·SI 반응 6종(§4) + **269 화합물 전표**(§3b). Fig 2·3·S1의 좌표는 이제 **정확값**으로 인용한다(Fig S2만 미판독).
- 🔴 **염화물 부분압 규약 불일치 (§3b.2)** — 논문의 chloride 표·산점도가 **HCl 1 ppm 보정을 빠뜨렸다**(HCl 1개당 +0.357 eV). **Fig S1 한 장 안에서 기준선(맞음)과 데이터 점(틀림)의 규약이 다르다.** 인용 시: (a) 황화물은 xlsx 그대로 안전, (b) **염화물은 `−0.357×n_HCl` 환산 후 인용하거나 as-published임을 명시**, (c) "Li₂ZrCl₆·Li₃YCl₆는 수분안정"이라는 Fig 3c 기반 인용은 **하지 말 것**(환산하면 −0.08 / +0.17 = 경계선). ⚠ 이 환산은 **우리 추론**이고 논문이 제시한 값이 아니다.
- **xlsx vs 본문의 소소한 불일치**: Li₃PS₄ 본문 −0.608 vs xlsx −0.594 (Δ0.014, entry/버전 차이로 추정). 인용은 **본문값 우선 + xlsx 병기**.
- **`Li₄SiS₄`가 entry id 공란**인데 SI Methods의 자체-DFT 4종 목록엔 없다 — 출처 미상 1건, 인용 주의.
- ✅ **`Cr⁶⁺` 항목 해소 (2026-08-06, §14b-3)**: Fig 2·3a·S1에 `Cr⁶⁺` 라벨이 있는데 xlsx엔 Cr⁶⁺ 화합물이 없다(Cr은 Cr³⁺만: LiCrS₂ +0.219·NaCrS₂ +0.402·CrCl₃ +1.002·Li₅CrCl₈·Na₃CrCl₆). **픽셀 검산 결과 = 데이터 없는 유령 라벨**이 맞다 — Fig 2의 Cr⁶⁺ 칸은 회색 ○·초록 ▽·주황 △ **셋 다 0개(완전 공백)**, Fig 3a의 `Cr⁶⁺ W⁶⁺` 는 **초록 원 1개를 두 라벨이 가리킨다**(그 1개 = Li₂WS₄ −0.602, Fig 2에서 W⁶⁺ 칸 −0.585로 재확인). → **전사 누락이 아니라 논문의 라벨 오류**. 인용 시 Cr⁶⁺는 이 논문 데이터에 없다고 말한다.
- **열역학 only**: kinetics·표면 passivation·수화층·입계 없음(저자 명시). 실험 H₂S 부피(cm³/g)와 1:1 대응 불가 — 서열/방향만.
- **MP GGA + 실험 기체/OH 혼합 스킴**: 절대 ΔG ±0.1 eV급 스킴 의존성 예상(anion correction·OH 실험값 무보정 명시·고체 엔트로피/PV 무시·hull+50 meV 준안정 포함). 우리가 재구현할 때 같은 혼합 규칙을 써야 비교 가능.
- **조성 대표성**: "Li–M–S"는 MP 등재(hull+50 meV) 화합물 — argyrodite(Li₆PS₅Cl)·Cl-rich·도핑 고용체는 직접 계산 대상 아님. 우리 조성 이식은 우리가 직접 계산해야.
- **0.1 %/1 ppm 조건 고정**: 조건 바꾸면 판정 뒤집힘(Li₂S). "안정/불안정" 이분법 인용 금지, 조건 병기(0.1 % = RH ~3 %라는 SI 환산이 인용 시 유용).
- 본문 "electrochemical stability" = **환원(0 V)** 전용 — 단 **SI에 따르면 4.5 V 산화 반응에너지도 전 화합물 계산돼 xlsx에 수록**(본문 미논의·xlsx 미보유). 산화 onset(우리 B①) 논의가 "없다"가 아니라 "본문에서 안 다뤘다"가 정확.
- **대표반응 = 최저 ΔG(미량 H₂O 극한)** 선택: 실제 노출(과량 H₂O·습윤 공기)에서는 다른 반응 경로(LiOH 등 습윤측 산물)가 지배할 수 있음 — 인용 시 "tracer-H₂O 한계" 명시.
- 2020년 논문 — 이후 실험(oxy-sulfide·[Yang25] 계열)이 이 프레임을 검증해 온 방향이지, 이 논문이 그 실험들을 안 것 아님.

## 13. 기법 용어 미니사전
- **가수분해 반응에너지 (eV/H₂O)**: 물 1분자당 H₂S/HCl 생성 반응의 ΔG(부분압 보정 포함). 음수=자발(수분 민감), 양수=안정. H₂O로 정규화해 조성 간 공정 비교.
- **predominance diagram**: 두 기체 화학퍼텐셜(μ_H₂O, μ_H₂S) 평면에서 어느 고체상이 안정한지 영역 분할 — 전기화학의 Pourbaix를 기체-화학으로 옮긴 것.
- **grand-potential 분석**: 열린 계(기체·Li 저장고와 물질 교환) 자유에너지 최소화 — 우리 ESW의 μ_Li 자리에 μ_H₂O·μ_H₂S를 넣으면 이 논문.
- **HSAB**: hard/soft acid–base 경험칙 — soft acid(Sn⁴⁺·Cu⁺ 등)는 soft base(S²⁻) 선호 → 황화물 결합 강해 가수분해 저항. 이 논문이 이를 ΔG로 정량화.
- **환원 반응에너지 (0 V)**: Li/Na 금속 접촉 상황(μ_alkali=0)에서 alkali 흡수 분해 ΔG(eV per alkali) — 음수 클수록 음극에서 잘 분해.
- **cathodic / anodic limit (V)**: 같은 grand-potential 스캔에서 분해가 시작되는 **아래 전압 / 위 전압** = ESW 양끝. xlsx에만 있고 본문엔 없다. **eV 단위 반응에너지(0 V·4.5 V)와 V 단위 limit은 다른 양** — 전자는 "그 전압에서 얼마나 세게 분해되나", 후자는 "몇 V부터 분해되나".
- **부분압 보정 `Δμ(x) = k_BT·ln x`**: 기체를 표준상태(1 bar)가 아니라 실제 희박 농도에서 볼 때 화학퍼텐셜을 낮추는 항. 300 K에서 **0.1 % → −0.1786 eV**, **1 ppm → −0.3572 eV**. 생성 기체(H₂S/HCl)에 붙으면 반응을 **더 자발적으로**, 반응물(H₂O)에 붙으면 **덜 자발적으로** 만든다. 이 항 하나를 빠뜨리면 판정 부호가 바뀔 수 있다 — 실제로 이 논문의 염화물 표에서 그런 일이 일어났다(§3b.2).
- **oxophilicity (산소친화도)**: 어떤 양이온이 S보다 O와 결합하기를 얼마나 더 선호하는가. §3b.4의 결론 — 가수분해 지도의 실제 구동변수는 HSAB의 soft/hard가 아니라 이것이다(같은 원소도 산화수가 바뀌면 뒤집힌다).

---

## 14. ★ 3차 검증 — 본문 재투입(inbox #54, 2026-08-06)

> **계기**: 사용자가 `litdb/inbox/54. Materials Design Principles for Air-Stable LithiumSodium Solid
> Electrolytes.pdf`(5 pp)를 "논문 에이전트로 처리" 요청(사용자 분류 폴더 `DFT`).
> **새 논문이 아니라 이 digest 의 본문이다** — 같은 논문의 **세 번째** 투입(#30 → 업로드해시 #55 → #54).

### 14a. 파일 판정 — **중복 확정, 신규 내용 0건**. 단 부산물로 색인 결함 1건을 잡았다

**A. 중복 판정 (기계 대조)**
- 이번 파일은 **본문 5 pp 단독**이다 — SI PDF·SI xlsx 없음. 즉 이 digest 가 이미 가진 것(본문 + SI 5 pp + xlsx 269행)의 **부분집합**이라 새로 들어올 내용이 원리상 없다.
- **판본 동일성**: `figures.json` 에 저장돼 있던 **Fig 1·Fig 2 캡션**(2026-08-05 에 업로드해시 #55 본문에서 뜬 것)이 이번 PDF 평문에 **문자 단위로 그대로 들어 있다**(공백·NFKC 정규화 후). → 같은 조판본 확정.
- **본문 수치 전수 재확인** — 식 (1) +0.225 · (2) +0.863 · (3) +0.416 · (4) +1.915 · (5) −0.608 / 데이터셋 46·52·65·14 / preset 0.1 % H₂O·1 ppm / 환원전위 1.0–1.5 V / LGPS류 25 mS cm⁻¹ / `Figure S1`·`Be2+`·`In3+` 언급 — **전부 §3·§5 기재값과 일치, 불일치 0건**.
  ⚠ 도구 노트: 이 PDF 는 수식 조판에서 **소수점을 콜론(`0:225`)으로, `+`를 `þ`, `=`를 `¼`, `(`를 `ð`** 로 넣는다. 평문 추출 후 `(\d):(\d)→\1.\2` 치환을 안 하면 **본문 수치가 통째로 검색에 안 걸린다**(1차 대조에서 0.863·1.915·0.608 이 전부 MISS 로 나왔다가 치환 후 전부 OK). `_53` 의 `\x02`→`−` 와 같은 계열의 함정.
- SI 전용 값(LiCl +0.977 · NaCl +1.532 · 2LiOH +0.413 · 2NaOH +1.083)은 예상대로 이 파일에 **없다** — SI 근거는 여전히 §3b·§4 와 `db/properties/zhu2020_si_*.csv` 뿐이다.

**B. 🔴 그런데: `Fig. 3` 이 색인에서 빠져 있었다 (복구 완료)**
- `fig_3.png`(1034×2217 px, 1.1 MB)는 디스크에 있는데 **`figures.json` 에 엔트리가 없었다** — 그래서 (i) webapp 이 digest 본문의 `Fig. 3` 표기를 링크하지 못하고 (ii) 문서 하단 그림 카드에도 안 뜬다. **이 논문의 중심 그림(2축 가이드 차트)이 통째로**.
- **원인** (`--why` 로 확인): 추출기가 **p3 의 `Figure 3.` 캡션을 ⛔ 로 기각**한다. Fig 3 은 오른쪽 단 세로로 긴 그림(`img (302,157,546,679)`)이고 캡션은 그 아래 오른쪽 단(`305,687–542,735`)에 있는데, **캡션 블록이 왼쪽 단 본문(`52,680–291,735`)과 같은 높이라 병합되며 x 가 18…543 으로 퍼진다** → "캡션 위 후보 영역"이 높이 36 pt 미만으로 쪼그라들어 탈락. **2단 조판 + 세로로 긴 단일-단 그림**의 조합에서 나는 구조적 오탐이다(README 의 알려진 한계 목록에 없던 유형).
- **복구**: bbox `(300,152,548,684)` @300 dpi 로 재렌더 → **1034×2217 px 로 기존 PNG 와 픽셀 크기까지 동일**(= 2026-08-05 수동 크롭이 쓴 박스를 정확히 재현). `figures.json` 에 `f3` 엔트리 추가(`note` 에 수동 크롭 사유 기록), `sources` 에 #54 파일명 추가. 이제 본문의 `Fig. 3`·`Fig. 3a` 표기가 webapp 에서 링크된다.

### 14b. 그림 재판독 — 이번엔 **픽셀 검산**까지 (본 것 4장 / 안 본 것 1장)

**본 것**: `fig_1.png` · `fig_2.png`(+ 좌측 30 % 확대) · `fig_3.png`(+ Cr⁶⁺ 구역 4× 확대) · `fig_S1.png`.
**안 본 것**: `fig_S2.png`(2026-08-05 과 같은 이유 — xlsx 정확값이 있어 막대 판독이 불필요).

`fig_2.png` 는 눈 판독 대신 **좌표를 기계로 뽑았다**: 프레임(213–2071, 38–718) 검출 → **두 점선(Li₂S 0.225 / Na₂S 0.416)으로 y 선형보정**(프레임 상단이 1.501 로 떨어짐 = 축 최대 1.5 ✓) → 색 분리(회색/초록/주황) 후 연결성분 중심좌표 → 55칸 등간격 범주축에 매핑.

1. **✅ xlsx 전사(2026-08-05)의 독립 검산 통과** — 가려지지 않은 온전한 회색 ○(≈315 px) **26개가 §3b.3 값과 ≤0.002 eV 일치**: Al −0.908/−0.910 · Si −0.845/−0.847 · **P −0.154/−0.156** · Hf −0.623/−0.625 · Zr −0.458/−0.459 · Tm…Gd 9종 전부 · Pr −0.139/−0.140 · Na +0.417/+0.416 · Fe²⁺ +0.551/+0.550 · Pb⁴⁺ +0.236/+0.236 · Cd +0.947/+0.948 · Cu²⁺ +0.939/+0.939 · Ag +1.039/+1.040 · Zn +1.080/+1.081 · Hg +1.001/+1.001 · Cu⁺ +1.267 · Au⁺ +1.339. 편차가 0.01–0.03 인 칸(Ti⁴⁺·Sm·Nd·Ce·Ti³⁺·Sb⁵⁺)은 **전부 블롭이 잘린 칸**(165–247 px = 다른 마커에 가려짐)이라 중심좌표가 밀린 것 — 전사 오류가 아니다. → **xlsx CSV 두 개를 그림으로 교차검증한 셈**.
2. **🔴 §7 의 "x축 = binary 값 오름차순" 서술 정정** (위 §7 표 반영 완료). 실측 회색 ○ 수열은 좌→우로
   `Be −1.042 → B −0.92 → Al −0.908 → Si −0.845 → P −0.154 → (Ta 없음) → Hf −0.623 → Zr −0.458 → (Nb·W·Cr⁶⁺ 없음) → Tm −0.581 → Er −0.566 → …`
   **단조가 세 군데서 깨진다**: (i) P⁵⁺ 가 Si 와 Hf 사이에서 +0.7 eV 튀었다 내려오고, (ii) Zr(−0.458) 다음 Tm(−0.581) 로 떨어지고, (iii) Nd(−0.171)→Pr(−0.139)→Ce(−0.201) 국소 역전. 게다가 **55칸 중 Ta⁵⁺·Nb⁵⁺·W⁶⁺·Cr⁶⁺ 는 binary M–S 가 아예 없어** binary 값으로 자리를 정할 수가 없다. **`Fig. S1`(염화물)이 같은 55칸을 순서까지 그대로 재사용**한다는 사실이 결정적이다 — 즉 이 축은 패널별 정렬이 아니라 **논문 전체가 공유하는 고정 양이온 축**이고, 배열은 "대체로 오름차순 + 화학군 블록(주족 hard → 초기TM d⁰ → 란타나이드/Sc·Y → 알칼리·알칼리토 → 후기TM/후전이금속)"이다. **정렬 규칙은 본문에도 SI 에도 없다.**
   → 우리 cascade 그림에 이 포맷을 차용할 때 **"값 순 정렬"이라고 캡션에 쓰면 안 된다**(같은 흠의 복제).
3. **✅ §12 의 `Cr⁶⁺` 미해결 항목 해소 — 논문의 라벨 오류로 확정**. Fig 2 의 Cr⁶⁺ 칸은 **세 계열 마커가 전부 0개(완전 공백)**이고, Fig 3a 의 `Cr⁶⁺ W⁶⁺` 는 4× 확대 결과 **초록 원 딱 1개를 두 라벨이 가리킨다**(그 1개 = Li₂WS₄, Fig 2 W⁶⁺ 칸 −0.585 ≈ xlsx −0.602). 전사본 전수 검색으로도 Cr 은 **Cr³⁺ 5종뿐**(LiCrS₂ +0.219 · NaCrS₂ +0.402 · CrCl₃ +1.002 · Li₅CrCl₈ · Na₃CrCl₆). → **xlsx 전사 누락이 아니라 그림 라벨이 잘못 붙은 것.**
4. **✅ §3b.2 염화물 오프셋 주장 재확인** — `Fig. S1` 한 장 안에서 **기준선**(LiCl 초록 점선 `figure-read ≈0.98` · NaCl 주황 `≈1.53` = SI 본문 규약)과 **데이터 점**(Li⁺ 칸 회색 ○ `≈1.34` · Na⁺ 칸 `≈1.88` = xlsx 규약)이 **동시에 보인다**. 음수는 P⁵⁺ `≈−0.69` · B³⁺ `≈−0.12` · Li₂BeCl₄ `≈−0.03` 뿐 ✓. 2026-08-05 판정 유지.
5. **✅ `Fig. 3` 좌표 전수 재확인** — 3c 의 14점이 §3b.2 표와 정확히 일치(In 1.38 · Cd 1.30 · Zn 1.29 · Ga 1.21 · Sc 0.90 · Y 0.89 · Cr³⁺ 0.845 · Er 0.84 · Mn 0.73 · Zr 0.63 · Fe³⁺ 0.62 · Al 0.38 · Fe²⁺ 0.30 · Be −0.03). 3a **오른쪽 위 사분면 비어 있음** 확정(x>0 점 0개), In³⁺ `figure-read ≈ (x −0.78, y +0.62)`. 3a 의 희토류 군집은 §5.5 가 적은 `x ≈ −0.2…−0.35` 보다 **넓다 — 실측 x ≈ −0.5…−0.15**(Sc³⁺·Gd³⁺ 가 왼쪽 끝, Er/Ho/Dy/Tb 가 오른쪽 끝). 결론(=RE 가 Li 황화물 중 환원 최우수)은 그대로.
6. **⚠ 그림 vs 본문 긴장 1건 (약함)** — 본문은 Na 계에서 "Sc³⁺·Y³⁺·Zr⁴⁺·대부분 란타나이드가 환원+수분 동시 달성"이라 쓰는데, `Fig. 3b` 실물에선 **Zr⁴⁺ 가 x ≈ −0.3·y ≈ +0.05**(둘 다 겨우 경계)이고 **Ce³⁺ 는 y ≈ −0.27 로 수분 음수**다. xlsx 도 같은 방향(Na₂ZrS₃ +0.045). → "동시 달성"은 **여유가 아니라 경계선**이라는 단서를 붙여 인용한다. 단 3b 의 주황 점선 상자들은 **겹친 점을 빼서 적은 라벨 상자**이지 데이터 위치가 아니므로, 상자 높이로 값을 읽으면 안 된다(RE 군집 실제 위치는 x ≈ +0.3·y ≈ +0.2 대, xlsx Nd +0.221 · Y +0.204 와 정합).

### 14c. 운영 조치
- `figures.json` 에 `f3` 추가 + `sources` 에 #54 등록, `generated` 2026-08-06.
- `litdb/pdf_map.tsv` 에 **재추출 가드** 추가 — 지금 inbox 엔 **본문 PDF 만** 있고 **SI PDF 는 로컬에서 사라졌다**. 이 상태로 `--slug … --clean` 을 돌리면 **`fig_S1`·`fig_S2` 가 지워지고 복구할 원본이 없다**. (`--inbox --run --skip-done` 은 안전.)
- 평문 보존: `litdb/inbox/_54_text.txt`(콜론-소수점 원본 그대로), 판독 보조 이미지 `_54_f2_left.png`·`_54_f3a_cr6.png`. ⚠ `litdb/inbox/` 는 .gitignore 대상이라 **로컬 전용** — repo 로 넘어오는 근거는 `figures/<slug>/*.png` 5장과 이 digest 뿐이다.

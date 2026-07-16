# Materials Design Principles for Air-Stable Lithium/Sodium Solid Electrolytes — Zhu & Mo (Angew. Chem. Int. Ed. 2020)

> slug `zhu2020_air_stable_se_design_principles` · DOI `10.1002/anie.202007621` · type `DFT (database thermodynamics, 실험 0)` · PDF `litdb/inbox/30. Angew Chem Int Ed - 2020 - Zhu - ….pdf` + **SI** `litdb/inbox/30. anie202007621-sup-0001-misc_information.pdf` (본문 5 pp Communication + SI 5 pp: Methods 2 pp·Fig S1·S2·refs — **원소별 수치표는 별도 xlsx**(anie_202007621_sm_miscellaneous_information.xlsx) **미보유**) · digested `2026-07-17` (SI 반영 2026-07-17) · status ✅ · 사용자 분류 `DFT`
> **저자**: Yizhou Zhu*(UMD→Northwestern) · **Yifei Mo***(UMD) — **🔑 우리 grand-potential ESW 방법의 원저자 그룹**(Zhu/He/Mo ACS AMI 2015 · JMCA 2016 = 이 논문 ref [2] = 우리 ESW 계보의 그 논문) + **[Banik]의 Mo와 동일 인물**. Angew 2020, 59, 17472–17476 (Energy Storage Hot Paper).

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

## 4. DFT/계산 방법 ★ (SI Methods 전문 반영)
- **code / DB**: 대부분 고체상은 **Materials Project 형성에너지** 직접 소환(고체는 **엔트로피·PV 항 무시** — ref [1]=Zhu/He/Mo 2015·2016 관례 명시). **자체 DFT는 MP에 없던 4종만**: Li₃AsS₄·Na₃AsS₄(enargite Cu₃AsS₄ iso-structure, **Pmn2₁**; Al-Qawasmeh & Holzwarth 2016), Li₃YCl₆(Asano 2018·Wang/Mo 2019 실험 구조), Li₂ZrCl₆(Li₂ZrF₆ iso-structure, **P3̄1m**).
- **DFT 세팅(그 4종)**: **VASP + PAW, GGA-PBE, ecut 520 eV**, pseudopotential **Li_sv·Na_pv·P·S**(표준 VASP), **MP 표준 anion correction** 적용. k-mesh·이완 조건은 SI에도 미기재(n/a); **DFT+U·vdW 언급 없음**.
- **hydroxide 고체 19종은 실험 표준생성엔탈피**(NIST-JANAF) — "벤치마크된 correction scheme이 없어서"라고 명시. 목록: LiOH·NaOH·KOH·RbOH·CsOH·Be/Mg/Ca/Sr/Ba(OH)₂·B(OH)₃·Al(OH)₃·Cd/Fe/Co/Ni/Cu/Pb/Mn(OH)₂.
- **기체 H₂O·H₂S·HCl: 실험 생성엔탈피+엔트로피**(NIST-JANAF), **T=300 K, 엔트로피는 기체 3종만** 포함. 부분압 보정 **Δμ(x)=k_B·T·ln x** (표준상태 기준); x(H₂O)=0.1 % = **300 K RH ~3 %**, x(H₂S)=1 ppm = **작업환경 허용노출한계**, HCl도 1 ppm. → **0 K hull이 아니라 유한-부분압 grand-potential**(전압축의 μ_Li를 μ_H₂O·μ_H₂S로 바꾼 것). **DFT(고체)+실험(기체·OH) 혼합 스킴**이라는 점이 방법의 핵심이자 주의점.
- **화합물 선정**: MP에서 **convex hull 위 50 meV/atom 이내** 전부(= 준안정 포함) + 자체 계산 Li₃AsS₄/Na₃AsS₄ 추가.
- **대표 가수분해 반응 선정 알고리즘 (SI 핵심, 재현 가능 수준)**: 후보 반응들을 **H₂O당 정규화 후 최저 ΔG 반응 채택** — "미량 H₂O가 과량 황화물/염화물과 반응하는" 극한의 수분민감도로 해석(저자 명시). 절차: **Step 1** LiₓMᵧS_z–LiₓMᵧO_z **pseudo-binary 상평형 프로파일**(hydroxide 제외)에서 출발 조성에 가장 가까운 전이 상평형 = 대표 반응 + 임계 μ_c(H₂O) 산출 → **Step 2** 그 계에 hydroxide M(OH)_t 존재 확인 → **Step 3** hydroxide↔oxide 전이 μ_t 계산, μ_t>μ_c면 Step 1 결과 확정 → **Step 4** μ_t<μ_c면 **"pseudo-oxide"** 상(조성 MO_{t/2}, E = E(M(OH)_t) − t·μ_c)을 상도에 삽입해 Step 1 재계산, μ_c′와 비교해 최종 확정(에너지는 실제 M(OH)_t 기준으로 환산). 산물 후보: Li₂S·Li₂O·M–S·M–O·Li–M–S·Li–M–O·M(OH)/LiOH·**oxysulfide/sulfate(M–S–O·Li–S–O)**.
- **predominance diagram**: (μ_H₂O, μ_H₂S) 2축 평면에서 Li₂S/LiOH/Li₂O (및 Na·Cl 계열) 안정영역 분할 — Pourbaix의 기체-화학 버전.
- **redox 안정성**: **0 V *와 4.5 V***(vs Li/Li⁺·Na/Na⁺) 반응에너지를 ref [1] grand-potential 스킴으로 전 화합물 계산, **alkali당 정규화 — 전표는 SI 첨부 xlsx**(⚠ 미보유). 본문은 0 V(환원)만 사용; **4.5 V 산화 데이터는 본문에서 논의 안 함**.
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
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | predominance diagram: (μ_H₂O, μ_H₂S/HCl) 평면 Li₂S–LiOH–Li₂O / Na₂S– / LiCl– / NaCl– 안정영역 + preset 별(0.1 %/1 ppm) | **우리 comp1/modelc 가수분해 지도의 축·조건 템플릿** — μ_Li 대신 μ_H₂O·μ_H₂S 2축; "조건 명시 없는 대기안정 주장 금지"의 시각적 근거 |
| 2 | cation별 가수분해 ΔG 산점도(46 M–S 회색 ○ / 52 Li–M–S 초록 ▽ / 65 Na–M–S 주황 △) + Li₂S/Na₂S 점선 기준 | **우리 47-dopant cascade에 '수분축' 열을 추가할 때의 랭킹 원판** — 도판트별 대략값 판독 가능(B³⁺ 최악, In/Zn/Cu/Ag 최고, RE 중하위); 차트 포맷 자체가 cascade용 |
| 3a–c | 가이드 차트: 가수분해ΔG(y) × 0 V 환원ΔG(x), Li–M–S/Na–M–S/Li–M–Cl | **2축 multi-objective 도판트 선정 차트 = 우리 cascade 시각화 포맷 그대로**(우리는 σ-blocking·산화 onset 축까지 확장 가능); RE 군집=Nd 선택의 외부 열역학 지지(환원측) |
| S1 | 염화물 가수분해 산점도: M–Cl(회색 ○)·Li–M–Cl(초록 ▽)·**Na–M–Cl(주황 △, 본문에 없는 계열)** + LiCl(+0.977)/NaCl(+1.532) 점선 기준 | 염화물 수분안정의 원판 — binary 음수는 P⁵⁺(~−0.7)·B³⁺(~−0.1)뿐(판독); Li–M–Cl 최상위 Ga/In/Cd/Zn ~+1.2–1.4(판독) = **우리 LiCl-buffer "수분 불활성" 서사의 정량 지지** |
| S2 | 4계열(M–S 파랑 / Li–M–S 초록 / Na–M–S 주황 / Li–M–Cl 보라) 가수분해 ΔG **화합물별 막대그래프** | Fig 2 산점도의 화합물-단위 버전 = **cascade 수분축 랭킹 판독 원판**. 판독 예: M–S에서 P₂S₅ ~−0.1 vs Li₃PS₄ −0.608(ternary가 binary보다 나쁜 유일 예외의 시각화)·Be²⁺ ~−1.05 최악·Au⁺/Cu⁺ ~+1.3 최고; Li–M–S 최고 In³⁺ ~+0.6·Sn⁴⁺ ~+0.43·Ga³⁺ ~+0.33, B³⁺ ~−0.9 최악 |
| xlsx | **전 화합물 가수분해·0 V·4.5 V 반응에너지 수치표** (anie_202007621_sm_miscellaneous_information.xlsx) | **미보유** — 확보 시 그림 판독을 정확값으로 교체 + **4.5 V 산화축 데이터**(본문 미논의)까지 얻음 |

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
| 염화물 수분안정 | LiCl 등 거의 전부 양수 — **LiCl+H₂O→LiOH+HCl +0.977 eV/H₂O**(SI 정확값) | 우리 분해산물 LiCl(SEI/CEI 절연 buffer) | ✓ **LiCl 산물은 대기·수분에도 불활성**이라는 보너스 의미 부여(이제 정량 인용 가능) — 단 Cl-rich *argyrodite*가 수분안정이란 뜻 아님(호스트는 여전히 황화물; [Wu] 90 °C calendar는 Cl-rich 열세) |
| gap/σ/기계 | 없음(전부 n/a) | — | 비교 대상 아님 |
| 무질서·kinetics | 0 (ordered MP 상·열역학만; 저자도 passivation 별도 명시) | 우리도 0K hull 동일 한계 + 표면 kinetics 없음 | ✓ 같은 한계 공유 — 실험 H₂S 발생량(cm³/g)과의 정량 대응은 양쪽 다 불가(방향·서열만) |

## 10. 적용 인사이트 (내 연구에 어떻게)
1. **🔑 B④ moisture 축을 "못 하는 것" 목록에서 지울 수 있다 — SI로 '레시피'가 '절차 명세'로 격상**: MP hull(+50 meV 준안정 창) + NIST-JANAF 기체(H₂O/H₂S) 실험 μ + Δμ=k_BT ln x 부분압 보정 + **대표반응 알고리즘(pseudo-binary S–O 프로파일→최저 ΔG, hydroxide는 pseudo-oxide 삽입; §4 Step 1–4)** — 전 단계가 SI에 재현 가능 수준으로 명세됨. 우리 6원소(+도판트) chemsys에서 comp1/modelc/**LPSOCl(+O)/+B₂O₃/Nd-doped**의 가수분해 ΔG(eV/H₂O)를 같은 조건(0.1 % H₂O=RH ~3 %/1 ppm)으로 계산하면 — [Yang25] H₂S 실측·[Taklu]/[Li25] HSAB 주장들과 우리를 잇는 **정량 다리**가 생긴다. 예상: O-doped가 ΔG 덜 음수(구동력 선지불), 산물에 Li₃PO₄. 재구현 시 주의: 고체 엔트로피/PV 무시·hydroxide는 실험값(무보정)·엔트로피는 기체만 — 같은 혼합 규칙을 써야 Zhu 수치와 비교 가능.
2. **+B₂O₃의 수분 리스크 체크가 급소**: 우리 B 서사는 산화·전자 축 이득인데, Zhu 지도에서 **B³⁺는 S계·Cl계 모두 가수분해 최악급**. B₂O₃-doped 조성의 가수분해 ΔG와 B 배위(B–O 유지 vs B–S 형성)를 확인해 "B는 산화축 이득·수분축 중립(B–O 유지 시)"으로 방어선을 미리 치자 — 리뷰어가 이 논문 들고 물어볼 자리.
3. **Nd 서사의 축 정리**: Zhu가 RE를 "Li 황화물 중 환원안정 최우수 + doping 후보"로 2020년에 이미 지목 — 우리 Nd 선택의 외부 계산 선례로 인용. 단 **수분 개선은 O의 공로로 명확히 분리**(Li–RE–S는 Zhu상 수분 음수). [Yang25]와 3자 정합: RE=환원/interphase, O=대기.
4. **인용·프레임**: 대기안정 주장엔 항상 **조건(습도 부분압) 명시** — Zhu의 Li₂S 조건부 안정이 교훈. 또 "HSAB적으로 안정" 대신 "가수분해 반응에너지 기준(Zhu 스킴)"으로 말하면 정량 인용 가능.
5. **차트 포맷 차용**: Fig 3의 2축(수분×환원) 가이드 차트에 우리 축(σ-blocking·산화 onset·기계)을 붙인 다차원 cascade 차트 = deck/논문 Figure 후보.

## 11. 인용 가능 문장 (deck/paper용)
- "Zhu & Mo's database thermodynamics traces the moisture hypersensitivity of thiophosphates to the formation of highly stable Li₃PO₄ (ΔG_hyd = −0.608 eV/H₂O for Li₃PS₄); our ICOHP (P–O −8.43 vs P–S −5.98) and O-site preference (−0.67 eV/O) provide the bond-level counterpart, and O-doping pre-pays exactly this driving force."
- "Rare-earth cations were computationally identified (Zhu 2020) as the most reduction-tolerant dopants among lithium sulfides — an external precedent for our Nd-based cascade — while their moisture benefit is marginal, so the air-stability gain of RE–O co-doping must be credited to P–O bond formation."
- "Hydrolysis energetics are condition-dependent: even Li₂S is thermodynamically stable at 0.1 % H₂O (+0.225 eV/H₂O) — air-stability claims require an explicit humidity chemical potential."

## 12. 주의/한계 (over-claim 방지)
- **SI PDF는 확보, 수치표 xlsx는 미보유**: 대표반응 알고리즘·DFT 세팅·SI 반응 6종은 확보(§4). 그러나 **화합물별 정확값 전표(가수분해·0 V·4.5 V)는 xlsx에만** — 본 digest의 Fig 2·3·S1·S2 좌표값은 전부 "판독 ~값".
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

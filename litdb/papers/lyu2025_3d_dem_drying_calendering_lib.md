<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# LIB 전극 구조진화를 건조+압연 한 번에 — 3D RVE DEM(AM + carbon-binder domain + 용매 + 입자접촉), 3-stage 건조법 + 압연→σ_e·두께방향 응력 — Lyu (Int. J. Electrical Power & Energy Systems 2025)

> slug `lyu2025_3d_dem_drying_calendering_lib` · DOI `10.1016/j.ijepes.2025.110521` · type `DEM (3D RVE, 건조+압연 연속; exp 검증)` · PDF `Lyu_2025_IJEPES_3D_DEM_ElectrodeEvolution_DryingCalendering.pdf` · digested `2026-06-26` · status ✅ · OPEN ACCESS (CC BY 4.0)

> ⚠ **2026-11-16 보강 (68-2 번 파일 · 원문 PDF 12 쪽 + 보충 영상 4 재정독)**: 옛 양식 본문은 지우지 않고, 원문과 다른 자리에 `[정정 2026-11-16 · 원문 p.N: …]` · 더한 근거에 `[보강 2026-11-16 · …]` 표지를 붙였다 (줄 번호 그대로).  새 절 = §11 보강 의도 대조 (참고문헌 22 행) · §12 핵심 수치 원문 대조판 · §13 방법 (식 1–29 · 크롭) · §14 그림 · 표 · 영상 · 판독 · §15 원문 문장 (DEM 한계 · 소성 · 차원 · 탈압) · §16 ★ 자세한 분석 · §17 [미확인] · §18 참고문헌 57 개 원문 그대로 · 🔗 관련 카드 · 보강 기록.  ⚠ 핵심 정정: 모델 활물질은 원문에 **'NCM'** 뿐 (811 아님) · 집전체 접촉 **897 → 2038 = +127 %** (원문 '230 %' 는 비) · 식 (8)–(9) = 접점 **속도** δ̇ · 식 (9) 근호 안 **k_s** · 서론의 Xu [48] 문장 = *'The cell performance increased with increasing calendering'* · 검증 그림 3 = **DEM 누른 채 ↔ 실험 압연 뒤** (두 상태).

> elements: Li

---

## 1. 한 줄 요약
**액체전해질 LIB 양극(NCM811 + carbon-binder domain CBD) [정정 2026-11-16 · 원문 p.4: 모델 활물질은 'NCM' 뿐 (화학식 · 조성 기호 없음) — 'NCM811' 은 서론 Sahore [13] 문장 (p.1) 에만]의 미세구조 진화를 *건조(solvent evaporation) → 압연(calendering)* 두 공정을 한 3D RVE DEM 안에서 *끊김 없이 연속으로* 시뮬레이션한 논문** — Sangrós(2020)·Ngandjong(2021)이 압연만(또는 슬러리·건조·압연을 *별 코드*로 이어붙임) 다룬 데 비해, **본 논문의 차별점은 (a) 용매를 *fluid-substitution*(부력+점성감쇠, eq 27–29; 명시 CFD 아님)으로 넣어 건조 자체를 DEM으로 굴리고, (b) 그 건조-종료 구조를 그대로 압연 초기조건으로 물려 한 시뮬레이션 사슬로 연결**한 것. 결과: ① 배위수(coordination number) 진화로부터 **3-stage 건조 스킴**(HDR-LDR-HDR = 高-低-高 건조속도)을 도출(실험 [19,20]과 정성 일치), ② 압연이 **기계적 무결성(입자-집전체 접촉 897→2038, +230 %) [정정 2026-11-16 · 원문 p.11: 원문 문장 'an increase of approximately 230 %' — 2038/897 = 2.27 → 증가 +127 % [카드 산술] · 230 % 는 비 (≈227 %) 로 읽힌다]·배위수(3.6→8.3) [보강 2026-11-16 · 3.6 · 8.3 = 본문 p.9 · p.10 · 그림 판독 = 3.6 → 최저 2.28 → 끝 8.10 (그림 7c) · 건조 끝 그림 6 ≈3.45]·전자전도도**를 향상시키되 **두께방향(z) 응력이 최대**(σ_zz≈−165 vs σ_xx=σ_yy≈−130 MPa)라 [보강 2026-11-16 · 판독 (t = 1): σ_zz −163.9 · σ_xx −127.4 · σ_yy −129.5 MPa — §12 · digitized.csv] **입자 파쇄(실험 200 MPa) 회피를 위해 z-응력 관리 필요**. **⚠ σ_e는 이 논문에서 *정성*(접촉망 완전도 논증)일 뿐 — Bruggeman/RNM 같은 전도도 솔버로 *수치값을 산출하지 않는다*** (peer Sangrós/Ngandjong과의 핵심 차이; over-claim 금지).

**소재·이온위상 주의**: NCM811 + **액체전해질 LIB**라 (i) **이온 전도체가 *공극(pore)*** → 우리 ASSB(SE 고체 입자망=전도체, Holm 구속)와 **위상 정반대**, (ii) **porosity = GOOD**(전해질 충전) → 우리 ASSB(porosity = BAD)와 **목표 정반대**. 우리에겐 **frame[5] 분업의 또 하나 독립 확인(rigid 구 + bond, 형상소성 없음)** + **건조/CBD라는 우리가 안 가진 wet-process 역량의 청사진**(backlog A3/A4/D5)으로서 가치.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/binder/전해질) | 연구유형 |
|---|---|---|---|---|
| **Yuhang Lyu, Shaohai Dong, Li Ting Gao, Zhan-Sheng Guo**(교신, davidzsguo@shu.edu.cn) — Shanghai Institute of Applied Mathematics and Mechanics, School of Mechanics and Engineering Science, **Shanghai University**, Shanghai Key Laboratory of Mechanics in Energy Engineering | **Int. J. Electrical Power & Energy Systems 165, 110521 (2025)** (접수 2024-12-13, 개정 2025-01-17, 게재 2025-02-09 [보강 2026-11-16 · 원문 p.1: 승인 2025-02-05 · 'Available online 9 February 2025'], **open access CC BY 4.0**) | 10.1016/j.ijepes.2025.110521 | **NCM811** LiNi₀.₈Co₀.₁Mn₀.₁O₂ AM(ρ 4.74, E 142 GPa) [정정 2026-11-16 · 원문 p.4 · 표 1: 'NCM' · 'AM' 만 — 화학식 · 811 없음] + **carbon-binder domain(CBD)** 입자(carbon black + binder, ρ 2.2, E 0.65 GPa) + **용매(fluid-substitution)** + 액체전해질(공극); [보강 2026-11-16 · 원문에 '액체 전해질' 낱말 없음 — NMP · PVDF 슬러리 LIB · p.10 의 '[48] ionic resistance' 문장이 공극 전해질을 전제 (카드 추론)] AM:CBD = **94:6 wt**, 고체분율 65 wt% | **DEM**(PFC3D 5.00; 건조+압연 연속) + 후처리(coordination·porosity·stress·contact network) + 압연 porosity 실험검증(Giménez [45]) |

> ★ **본 논문의 자리매김**: 같은 "LIB 전극 제조 DEM" 가문의 세 번째 — **Sangrós(2020, TU-BS, 압연역학+삼중 균질화)** [보강 2026-11-16 · 원문 p.2 · p.12: 이 논문이 인용한 Sangrós Giménez 논문은 [44] 2018 Adv Powder Technol · [45] 2019 Powder Technol (= 정본 `sangros2019_dem_calendering_lib_electrode`) — 'Sangrós 2020' 은 이 원문 참고문헌에 없다 (카드의 계보 구성)], **Ngandjong(2021, Franco/LRCS, 슬러리→건조→압연→전기화학 멀티스케일)**, **Lyu(2025, Shanghai, *건조+압연을 한 DEM에 연속*)**. 본문 Introduction이 이 계보를 직접 인용: Sonzogni [46](압연 DEM) [보강 2026-11-16 · 원문 p.2 그대로: '…studied the effect of calendering on the microstructure and electronic properties of the electrodes by DEM. The bonding structure induced by calendering involves mostly vertical tensile contacts and horizontal compressive contacts.']·Sun [47](압연 FEM)·Xu [48](과압연→이온저항↑) [정정 2026-11-16 · 원문 p.2 · p.10: 서론 p.2 의 [48] 문장 = 'investigated the effect of calendering on the effective cathode transport properties using a multiscale approach. The cell performance increased with increasing calendering.' · '과압연 → 이온 저항↑' 은 결과 절 p.10 의 [48] 문장 — 서론 계보 서술로는 일부 다름]·Zhang [49,50](압연 DEM 응력분포) [정정 2026-11-16 · 원문 p.2: Zhang [49,50] = 'structural mechanics and microstructural evolution … increasing the number of contacts between particles can improve the conductive path' — '응력 분포' 는 Ge [51,52] 문장 ('inhomogeneous stress distribution and anisotropic properties')]·Ge [51,52](압연 + bonding model)·**Ngandjong [53](압연 DEM, CBD+건조 *함께 다룸*)** 를 선행으로 들고, **"위 DEM 압연 시뮬들은 *건조 구조*를 초기상태로 거의 안 쓰고 랜덤 생성 구조를 쓴다 → 압연 분석에 부적절"**(본문 §1 끝)을 *본 연구의 동기*로 명시. 즉 **"검증된 건조-종료 구조를 압연 초기조건으로 물려준다"가 셀링 포인트**(Ngandjong과 같은 철학이되, *한 DEM 코드(PFC3D)로 건조와 압연을 끊김 없이*). 저자 1저자 본인의 선행 **Lyu [22] = *2D* DEM 건조** → 본 논문이 그 **3D 확장 + 압연 연결** [정정 2026-11-16 · 원문 p.2 · p.12: 서론 문장은 '2D model … during the drying process' 이지만 목록 [22] 제목 = '2D Discrete element simulation of electrode structural evolutions in Li-ion battery during drying and calendering' (Energ Technol 2024;12:2400583) — 2D 판도 제목상 압연을 다룬다 → '압연 연결' 이 새것이라는 읽기는 목록과 일부 다름 (2D 판 원문 미확인)].

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **porosity (압연)** | **57 → 22 %** | 건조종료(압연시작) → 압연종료 | stated(Fig 7b) | 두께 80→40 µm(−50 %); ★실험 Hg-intrusion **57→~20 %**[ref32]와 일치 [보강 2026-11-16 · 본문 p.8 'approximate initial value of 57 %' → 'approximate final value of 22 %' · 판독 그림 7b 57.0 → 21.7 % · (1 − P)·h = 34.4 → 31.3 µm (−9 %) [카드 산술 — 주기 단면이면 같아야 함 · 측정 영역 V_reg 원문에 없음] · 실험 '57 %' = 정본 meyer2017 카드 기준 기하 (피크노미터) 기공 · 수은 압입 맞춤식은 0.52 에서 시작 (그 카드 기준 · 판정 안 함)] |
| **porosity 곡선 형태** | 0–0.25 평탄(57 %) → 선형 급강하 → 22 % | dimensionless time | digitized(Fig 7b) | **초기 평탄 = 거친 top이라 plate가 高점만 접촉**(RVE 밀도 거의 안 변함); top 평탄화 후 선형 압밀 [보강 2026-11-16 · 판독: t ≤ 0.20 57.0 · 0.25 56.4 · 0.30 56.2 · 0.40 53.3 · 0.60 45.3 · 0.80 33.3 · 1.00 21.7 % · 원문 p.9 'the porosity decreased linearly and rapidly until the final porosity was reached'] |
| **두께 (압연)** | **80 → 60 → 40 µm** | t=0 / 0.5 / 1.0 | stated(Fig 7a) | ~40 % 두께감소 = ~75.4 % 밀도증가[ref32,33] [정정 2026-11-16 · 원문 그림 7a 글자 = 'h ≈ 80µm' (Initial state) · 'h = 60µm' (Interim state) · 'h = 40µm' (End of calendering) — 중간 상태의 시각 t = 0.5 는 원문에 없다 [미확인] · 본문 p.8: 실험 두께 −40 % [32,33] → 밀도 +75.4 % [32] ↔ 시뮬 두께 −50 % · 밀도 비 (1 − 0.217)/(1 − 0.570) = 1.82 [카드 산술]] |
| **coordination number Z (건조)** | **~0 → 3.6** | 슬러리 → 건조종료 | stated/digitized(Fig 6) | 3-stage: I(느림)·II(급증)·III(느림-안정) [보강 2026-11-16 · 본문 p.9 = 압연 시작 3.6 'which was the final value at the end of the drying process' ↔ 그림 6 끝 [판독] ≈3.45 (3.40–3.49) — 원문 안 0.15 차 · 단계 경계 [판독] t 0.437 · 0.888] |
| **coordination number Z (압연)** | **3.6 → (dip ~2.3) → 8.3** | 압연시작 → 초기 → 종료 | stated/digitized(Fig 7c) | ★초기 dip(건조구조 안정성 파괴, 접촉분리) 후 **최대 8.3**(치밀화) [보강 2026-11-16 · 판독 그림 7c: 시작 3.58–3.61 · 최저 2.27–2.29 (t 0.22–0.30) · 끝 8.10 ↔ 본문 'a maximum value of 8.3' (p.10) — 그림 ↔ 본문 0.2 차 · 원문 'decreased slightly' ↔ 3.6 → 2.28 = −37 % [카드 산술]] |
| **입자-집전체 접촉수** | **897 → 1087 → 2038** | t=0 / 0.5 / 1.0 (압연) | stated(Fig 8) | **+230 %** — 계면접착↑·계면저항↓[ref38] [정정 2026-11-16 · 원문 p.11 'an increase of approximately 230 %' — 2038/897 = 2.27 → +127 % · 1087/897 → +21 % [카드 산술] · 897 · 2038 = 본문 p.11 · 1087 = 그림 8 글자만] |
| **평균응력 σ_zz (두께방향)** | **~−165 MPa** | 압연종료 | digitized(Fig 9a) | **★PEAK** — z 우선박막화; 접촉력이 주로 두께방향 [보강 2026-11-16 · 판독 t = 1: −163.9 MPa (t 0.5 −70.2 · 0.8 −136.1) · 원문은 숫자를 적지 않는다 ('a notable increase along the z-axis due to preferential thinning' p.11)] |
| **평균응력 σ_xx=σ_yy (면내)** | **~−130 MPa** | 압연종료 | digitized(Fig 9a) | 주기경계 x·y라 등방; σ_zz보다 작음 [보강 2026-11-16 · 판독 t = 1: σ_xx −127.4 · σ_yy −129.5 MPa → σ_xx/σ_zz 0.78 [카드 산술]] |
| **입자파쇄 임계응력(실험)** | **200 MPa** | fracture onset | stated(ref [57]) | ★ z-응력을 이 아래로 유지해야 입자 안 깨짐 [보강 2026-11-16 · 원문 p.11 'The experiment showed that particle fracture occurred when the stress of the electrode reached 200 MPa [57]' · 정본 stershic2015 카드 기준 200 MPa = Ebner 2013 자료의 최고 명목 압연 압력 (2000 bar) 에서 깨진 입자가 보인 것 — 파쇄 문턱 측정 아님 (그 카드 기준 · [57] 원문 미확인)] |
| **압연력(plate / collector)** | **~−4.9 / −5.7 N** | 압연종료 | digitized(Fig 9b) | 0에서 **지수적** 증가; collector가 약간 큼(top 국소 불안정) [보강 2026-11-16 · 판독: 판 −4.84 N (t = 1) · 집전체 마지막 점선 −5.59 N (t 0.987 · t = 1 외삽 ≈ −5.7) · 판 힘 ÷ (200 µm)² = 121 MPa ↔ 집전체 140–142 MPa ↔ 접촉 virial σ_zz 164 MPa [카드 산술 · 단면 유지 가정] · ln F 증분 0.85 → 0.64 → 0.45 로 줄어 시간 지수꼴이 아니다 [카드 산술] (원문 'escalated exponentially')] |
| **σ_electronic** | **수치 없음 — 정성만** | 압연↑ → σ_e↑ | stated | ★ "접촉망 완전도↑ → 전자경로 짧아짐·접촉↑ → e-저항↓"[ref38] *논증*만. **Bruggeman/RNM 솔버로 σ_e 값 산출 안 함** |
| **E_AM (DEM 입력)** | **142 GPa** | NCM811 단입자 [정정 2026-11-16 · 원문 표 1: 'AM' 142 GPa (출처 [45,49,50]) — 'NCM811 단입자' 표기는 원문에 없다] | stated(Table 1) | cf 우리 E_CAM 140 / Sangrós 142.5 / Ngandjong 200 |
| **E_CBD (DEM 입력)** | **0.65 GPa** | CBD 입자 | stated(Table 1) | ~AM의 1/220 → **부드러운 변형상**(cf Ngandjong 2 GPa) |
| **ρ_AM / ρ_CBD** | **4.74 / 2.2 g/cm³** | 소재 | stated(Table 1) | NCM811 / CBD |
| **ν_AM / ν_CBD** | **0.25 / 0.2** | 소재 | stated(Table 1) | |
| **마찰(sliding/rolling) AM** | **0.12 / 0.012** | DEM | stated(Table 1) | CBD = 0.1 / 0.01 |
| **AM PSD** | **Gaussian 평균 13 µm, std 0.61** | 실측[ref51] [정정 2026-11-16 · 원문 p.4: 'mean value of 13 μm [51] and standard deviation of 0.61' — '실측' 낱말 없음 · 표준편차 단위 없음 (µm 로 읽으면 CV 4.7 % [카드 산술])] | stated | **거의 단분산**(std 매우 작음) — bimodal 아님 |
| **CBD 직경** | **2.2 µm** | [ref28] | stated | AM·CBD 둘 다 구 가정 |
| **조성** | AM:CBD **94:6 wt**, 고체분율 **65 wt%** | 슬러리[ref26] | stated | |
| **bond gap λ** | **1.67** | bond 형성 기준 | stated[ref51] | ‖Pi−Pj‖ ≤ λ(Ri+Rj)면 bond [보강 2026-11-16 · 정본 ge2022 카드: 결합 생성 기준 ζ_b 1.67 = 같다 (그 카드 기준)] |
| **압연 plate 속도** | **0.01 m/s** | const z-speed | stated[ref51] | quasi-static 압축 [보강 2026-11-16 · 'quasi-static' 은 원문 낱말 아님 · 우리 DEM 판 속도 0.01 mm/s 의 1000 배 · 판 이동 = 두께 감소 40 µm 이면 4 ms · 처음 변형률 속도 125 s⁻¹ [카드 산술] · 준정적 점검 원문 없음] |
| **RVE** | **200×200×200 µm**(슬러리) → 건조후 z≈**80 µm** | 주기 x·y | stated | bottom=집전체, top=자유(건조)/plate(압연) [보강 2026-11-16 · 입자 수 원문 없음 — 94:6 · ρ 4.74/2.2 · 지름 13/2.2 µm · 단면 200 × 200 µm 로 AM ≈960–1050 · CBD ≈2.7–3.0 × 10⁴ [카드 산술 · 추정]] |

## 4. 시뮬레이션 방법 ★
- **code / version**: **PFC3D 5.00**(Particle Flow Code 3D, Itasca — 상용 DEM). 후처리(coordination·porosity·stress·contact-network 진화)는 PFC3D 내장 + 본문 정의식(eq 24–26). **전기화학 솔버 없음**(σ_e는 정성 논증). [보강 2026-11-16 · 원문 p.5 'The computational software was PFC3D version 5.00' · 후처리 도구 · 시간 간격 · 계산 시간 원문에 없음]
- **DEM 지배식(eq 1–2)**: 병진 `m_i du_i/dt = F_c + F_i`, 회전 `I_i dω_i/dt = F_t × R_i`. F_c=접촉력, F_t=접선접촉력, F_i=입자에 가해진 힘(건조 시 유체력).
- **DEM 접촉법칙** ★ (**eq 3–14, Hertz 계열 + 마찰**): 접촉력 `F_c = F^l + F^d` (eq 3) = **탄성+마찰(elastic no-tension + friction) F^l** + **점성감쇠(energy dissipation) F^d**. 법선·접선 분해(eq 4–5): [보강 2026-11-16 · 원문 p.3: 자기 접촉 모델에 'Hertz' 이름을 붙이지 않는다 ('Hertz-Mindlin' 은 p.2 Lippke [28] 설명에만) · 식 (6) 의 3/2 승 + 식 (14) k_n = AE*/L (N/m) 를 같이 쓰면 k_n(Δδ_n)^{3/2} 이 힘의 단위가 아니다 [카드 산술 · 차원]]
  - **법선 탄성** `F^l_n = (F^l_n)₀ − k_n·Δδ_n^(3/2)` (eq 6) — **Hertz 비선형(δ^1.5)**, k_n=A·E*/L(eq 14, A=접촉면적, L=중심거리). [보강 2026-11-16 · 원문 p.3 은 식 (6) 앞에 'The F^l_n is calculated as follows [46]:' — 정본 sonzogni2024 카드 (정독 122) 기록 = 그 원문에 이 식이 없다 → lyu2025 원문의 인용 문제 (이 카드 문제 아님) · 크롭 `eq_06_*`]
  - **접선 탄성** `F^l_s = (F^l_s)₀ − k_s·Δδ_s` (eq 7) — 선형 접선강성 k_s.
  - **법선·접선 감쇠** `F^d_n = (2β_n√(m_c·k_n))·δ_n` (eq 8), `F^d_s = (2β_s√(m_c·k_n))·δ_s` (eq 9) — β_n/β_s=감쇠계수, m_c=감쇠질량(eq 13). [정정 2026-11-16 · 원문 p.3 식 (8)–(9): 마지막 인자 = 접점 상대 속도 δ̇_n · δ̇_s (점 붙음 · 'normal and tangential velocity of the contact point') · 식 (9) 근호 안 = m_c k_s (k_n 아님) · β_n · β_s = 'coefficients of influence of the normal and tangential particles' (값 없음)]
  - **유효물성** E*(eq 10, Hertz)·G*(eq 11)·R*(eq 12)·m_c(eq 13). ⚠ **이는 PFC3D의 *Hertz-Mindlin류 접촉*** — **항복압(p_y/H) 캡 없음**(Thornton–Ning 아님). 즉 **Luding/우리 hooke-hysteresis와 같은 *no-cap* 층**(접촉모델 층위지도 §1-A). 입자는 강체 구, δ=소성의 기하 프록시일 뿐 **형상 안 변함**. [정정 2026-11-16 · 원문 p.3 식 (10) 인쇄 = 1/E* = (1 − ν₁)²/E₁ + (1 − ν₂)²/E₂ — 보통 Hertz 꼴 (1 − ν²) 과 다르게 인쇄 (크롭 `eq_10_*`) · 'Hertz-Mindlin류' · 'PFC3D 의' 는 원문에 없는 이름 (카드 추론) · 항복 캡 없음은 맞다 (식 3–14 에 소성 · 항복 항 없음)]
- **재료 파라미터(Table 1)**: E_AM=142 GPa, E_CBD=0.65 GPa(AM의 1/220), ρ_AM=4.74, ρ_CBD=2.2 g/cm³, ν_AM=0.25, ν_CBD=0.2, 마찰 AM(slide 0.12/roll 0.012)·CBD(0.1/0.01).
- **bond/binder 모델** ★★ (**PFC3D 2종 bond — linear contact vs linear parallel; eq 15–23 + Fig 1**):
  - **linear PARALLEL bond(Fig 1b, eq 15–23)** = **CBD에 적용**(CBD-CBD, CBD-AM, CBD-collector). 법선·접선 *힘* `F = −F̄_n·n_c + F̄_s` (eq 15) **+ twisting·bending *모멘트* M̄ = M̄_t·n_c + M̄_b** (eq 16) 까지 전달 — **bond가 굽힘/비틀림 모멘트를 두 입자 사이에 전달**(eq 19–20). 힘-변위 법칙 eq 17–18(법선 F̄_n=(F̄_n)₀+k̄_n·Ā·Δδ_n, 접선 F̄_s). **최대 법선응력 σ̄ = F̄_n/Ā + ‖M̄_b‖R/I (eq 21), 최대 전단응력 τ̄ = ‖F̄_s‖/Ā + ‖M̄_t‖R/J (eq 22)** → bond breakdown stress σ̄_c/τ̄_c 도달 시 파단(Fig 1a). Ā=단면적, Ī=관성모멘트, J̄=극관성모멘트. [보강 2026-11-16 · 원문 식 (19) M̄_t = (M̄_t)₀ − k̄_s J̄ Δθ_t · 식 (20) M̄_b = (M̄_b)₀ − k̄_b Ī Δθ_b (k̄_b 정의 없음) · 파단 문턱 σ̄_c · τ̄_c 는 그림 1a 글자뿐 — 값 · 결합 강성 k̄_n · k̄_s · 결합 반경 원문에 없음 [미확인]]
  - **linear CONTACT bond(Fig 1c)** = **AM에 적용**(AM-AM, AM-collector). **모멘트 미전달**(parallel bond에서 bending moment M̄를 무시하면 contact bond로 degenerate, 본문 eq 23 주변) [보강 2026-11-16 · 원문 p.4: 'When the effect of the parallel-bond moment M is not considered' — M 전체 (비틀림 + 굽힘)]. 즉 **AM-AM = 힘만, CBD = 힘+모멘트**(CBD 망이 더 "구조적"). ⇒ **소재별 다른 bond 모델 = 본 논문의 명시적 설계**(CBD cohesion + AM-CBD adhesion 물성차 [ref31] 반영).
  - **bond 형성 기준(eq 23)**: 두 입자 중심거리 ‖Pi−Pj‖ ≤ **λ(Ri+Rj), λ=1.67**[ref51]이면 bond 생성. **Fig 1a = bond-to-bond failure 모식**(breakdown stress σ̄_c/τ̄_c에서 끊김; tension/bend/shear/torsion으로 파단, "open" 상태로). ⚠ Sangrós(영구파단)·Ngandjong(SJKR 재형성)과 **또 다른 갈래** — 여기선 **PFC3D linear parallel/contact bond(모멘트 전달 여부로 2종)**.
- **★ 용매/건조 모델 (fluid-substitution; eq 27–29) — 이 논문 차별점**:
  - **명시 CFD/capillary 아님**, **fluid-substitution model**[ref28](=DNS 유체 회피, 계산비 大절감)을 채택. 용매가 입자에 주는 영향을 **3개 힘**으로 대리:
    - **부력 F_b = 4/3·πR³·ρ_liquid·g** (eq 27) — 용매 부력.
    - **중력 F_g = 4/3·πR³·ρ_solid·g** (eq 28) — 입자 중력.
    - **점성감쇠 F_r = α·v** (eq 29) — **점성저항**(α=감쇠계수, v=입자속도; **상수 아님, 속도의존**).
  - **건조 = 용매가 마르며 부력 사라지고 입자가 가라앉아 충돌·압밀**(Fig 4). 슬러리 RVE 200³ µm에서 시작 → top free·bottom collector(입자 못 빠짐) → **안정 구조 형성 시 건조 종료**(두께 ~80 µm). ⚠ **모세관력(capillary bridge)·용매 표면장력은 명시 항으로 없음** — 부력+점성감쇠로 coarse-grain. ("solvent evaporation"을 *유체 부력 소멸*로 모사; 표면장력 유발 바인더 이동은 *결과*로 나타남, Fig 5 CBD top-enrichment). [보강 2026-11-16 · 증발 (용매 감소) 을 계산에 어떻게 넣었는지 (ρ_liquid · α 의 시간 변화 · 용매 부피 · 건조 시간) 원문에 없음 [미확인] — '부력이 사라진다' 는 카드 추론 · 원문은 'As the drying progressed, the thickness of the slurry decreased significantly' (p.5) 만]
- **MPM/continuum**: **없음**. 압밀역학·전기 모두 DEM(전기는 *정성*). **입자 형상소성(SHAPE flow)·void-fill 없음** — 접촉은 CONTACT 레벨.
- **전달 솔버** ★ (**없음 — σ_e는 정성 논증**): ⚠⚠ **본 논문은 σ_e/σ_ion을 수치로 산출하는 솔버(Bruggeman·RNM·Kirchhoff·FEM)를 *돌리지 않는다*.** "calendering이 전자전도를 향상"이라는 결론은 **접촉망 완전도(배위수↑·입자-집전체 접촉↑)로부터의 *물리 논증***(본문: tighter network → shorter e-paths → lower e-resistance[ref38]) + **"과압연은 이온저항↑[ref48]"** caveat. 따라서 **σ_e/σ_ion 수치는 우리 비교표에서 *정성 추세*로만** 다뤄야 함(Sangrós eq1 균질화·Ngandjong FEM과 *결정적으로 다른 점*).
- **입자 처리** ★ (DEM판 "무질서 처리"): **구만**(AM=Gaussian 평균 13 µm·std 0.61 = **거의 단분산** 강체 구; CBD=2.2 µm 단일 구). **rigid 입자 + Hertz CONTACT(항복캡 없음, δ 프록시) + bond(AM=contact bond, CBD=parallel bond)** — 입자 **형상 안 변함**. **초기구조 = 슬러리 RVE 균일분포 → *건조 DEM으로 형성*(랜덤 placement 아님)** — 이게 본 논문 novelty(건조-종료 구조를 압연 초기조건으로). PSD가 **bimodal 아님**(std 0.61로 사실상 mono) → **Furnas dip 다루지 않음**. [보강 2026-11-16 · std 단위 원문에 없음]
- **도메인/RVE / servo / seeds / 압력범위**:
  - **RVE 200×200×200 µm**(슬러리), x·y **주기경계**, bottom **집전체(current collector)**(입자 하강 차단), top=자유표면(건조)/**pressure plate**(압연).
  - **건조**: fluid-substitution → 안정 구조 시 종료(두께 ~80 µm). **압연**: 건조-종료 구조를 *그대로* 초기조건으로, **plate가 z축 아래로 const 0.01 m/s** 하강(servo 압력제어 아니라 *변위/속도 제어* — 우리 MPM "hold"와 같은 결).
  - **압력범위**: 명시 절대 압력 sweep 없음(평균응력 −165 MPa까지 발달, Fig 9a). 압연 검증은 Giménez [45] porosity-vs-압력 실험과 대조(Fig 3, ~0–160 MPa 범위에서 sim≈exp). [보강 2026-11-16 · 판독 그림 3: DEM 57.0 · 43.0 · 38.0 · 31.0 · 23.0 % ↔ 실험 52.2 · 41.6 · 37.2 · 29.5 · 21.7 % at ≈0 · 20 · 43 · 79 · 159 MPa (차 +4.8 · +1.4 · +0.8 · +1.5 · +1.3 %p) · 실험 점 = 정본 sangros2019 카드 표 1 (0.522 · 0.416 · 0.372 · 0.295 · 0.217 at 0 · 19.82 · 42.71 · 79.13 · 159.37 MPa) = 압연 뒤 측정 ↔ 이 논문 DEM 은 탈압 없음 (누른 채) [카드 추론 · 두 상태] · DEM 점의 압력이 어느 응력 (판 힘 ÷ 면적 / σ_zz) 인지 원문에 없음]
  - **seeds**: 명시 안 됨(단일 RVE 추정).
- **특이사항/튜닝**:
  (1) **건조+압연 한 DEM 연속** — 건조 출력(구조·접촉·bond)이 압연 입력. **이게 핵심 novelty**(Ngandjong은 CGMD→DEM 코드 전환; Lyu는 PFC3D 한 코드).
  (2) **소재별 bond 차등**(AM=contact bond 모멘트無, CBD=parallel bond 모멘트有) — CBD가 더 "구조 잡는" 상.
  (3) **fluid-substitution**(부력+점성, 명시 모세관 無)으로 용매 coarse-grain — 계산비 절감하되 표면장력 물리는 간접.
  (4) **검증 = Giménez [45] 압연 porosity-vs-압력**(Fig 3) + Hg-intrusion 57→~20 %[ref32] + 입자파쇄 200 MPa[ref57] + EDS CBD top-enrichment[ref18,21]. **σ_e/σ_ion 실측 검증 없음**(정성 결론이라).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **bond 모식**: (a) bond-to-bond failure(법선/모멘트/전단/토크 vs 변위; breakdown stress σ̄_c/τ̄_c에서 파단→open), (b) **linear parallel bond**(힘+모멘트 전달, CBD용), (c) **linear contact bond**(힘만, AM용) | **PFC3D bond 2종(모멘트 전달 여부)의 정의도** — 우리 CBD bond 모델화(backlog A3) 시 *모멘트 전달 CBD vs 힘만 AM* 차등의 청사진 |
| **2** | **초기 RVE**: (a) 건조용(200³ µm, AM 녹색 구 + CBD 적색 점, bottom collector), (b) 압연용(같은 RVE + 상단 **pressure plate**) | 시뮬 셋업; AM:CBD 크기·수 비율 시각화 |
| **3** | ★ **porosity vs 압축응력**(실험■ Giménez[45] + DEM● 적선) — 0→160 MPa서 ~57→~22 %, **sim≈exp 양호**(저압서 급강하 후 완만) | **압연 P-vs-porosity 검증**(우리 P-vs-porosity·Heckel과 대조; LIB 저압 급강하 — 단 압력대 다름) [보강 2026-11-16 · 판독 값 = §12 · 실험 = 압연 뒤 · DEM = 누른 채] |
| **4** | **건조 3D 구조진화**: (a₁–a₃) 거시구조(슬러리 분산→충돌→치밀 다공), (b₁–b₃) **입자 속도장**(건조 진행에 top 입자가 빠름 = 두께방향 속도구배), (c₁–c₃) **접촉망 진화**(초기 희박→집전체측부터 AM 굵은선 망 형성→안정) | **건조가 집전체측부터 AM 접촉망을 쌓는 것** 시각화; 속도구배=건조 비균질의 직접증거. 우리 압밀 진화 영상의 LIB-건조판 |
| **5** | **CBD 분포 진화(건조)**: (a–c) 3D + 2D 수직단면 — 건조 종료 시 **CBD가 전극 *상단(top)*에 농축**(binder migration). EDS 실험[ref18,21]과 일치 | ★ **건조 시 바인더가 위로 쏠려 *집전체 계면 바인더↓→접착↓*** — 우리가 안 가진 *건조-유발 조성 구배* 현상. backlog A4(coating)·CBD morphology와 개념 연결 |
| **6** | ★ **배위수 vs dimensionless time(건조)** — **3 stage**: I(HDR, 느림 0–0.45)·II(LDR, 급증 0.45–0.9)·III(HDR, 느림-안정 0.9–1.0). Z 0→3.5 | ★ **3-stage 건조 스킴의 근거**(Z 증가율로 stage 구분 → 중간 LDR·양끝 HDR 권장). 우리 압밀 단계론과 개념 대응 [보강 2026-11-16 · 판독: 단계 경계 t 0.437 · 0.888 · 끝 Z ≈3.45 (본문 3.6)] |
| **7** | ★ **압연 구조진화**: (a₁–a₃) 3D+front(h 80→60→40 µm), (b) **porosity vs time**(57→22 %, **초기 평탄 후 선형 급강하**), (c) **배위수 vs time**(3.6→**dip ~2.3**→**8.3**) | **압연 압밀 곡선 + 배위수 dip-then-rise**(초기 거친 top·구조파괴 → 재배열 → 치밀). 우리 압밀 Z 진화와 대조 [보강 2026-11-16 · (c) 는 p.9 'Fig. 7 (continued)' — 옛 크롭 fig_7 에 빠져 있어 `fig_7c.png` 로 더함 · h 60 µm 의 시각 원문에 없음] |
| **8** | ★ **입자-집전체 접촉수 vs time(압연)** — **897→1087→2038**(+230 %) [정정 2026-11-16 · +127 % (2038/897 = 2.27) [카드 산술] · 원문 '230 %'], 인셋=집전체 접촉키 분포 | **압연이 계면접착·계면저항을 직접 개선**(접촉↑) — 우리 coverage(집전체 계면 아님)와 개념 대응 |
| **9** | ★ **압연 역학**: (a) **평균응력 σ_xx/σ_yy/σ_zz vs time**(전부 압축음수; **σ_zz≈−165 PEAK** > σ_xx=σ_yy≈−130; 인셋=접촉력 벡터도 t=0/0.5/1.0), (b) **plate·collector 힘 vs time**(0에서 **지수증가**, collector −5.7 > plate −4.9 N) | ★ **두께방향(z) 응력 최대 + 지수적 힘 증가** — 우리 MPM 압밀 응력장(z 우선)과 직접 대응; **입자파쇄 200 MPa 회피 = z-응력 관리**가 우리 fracture와 연결 [보강 2026-11-16 · 판독 σ_zz −163.9 · σ_xx −127.4 · σ_yy −129.5 MPa · 판 −4.84 N · 집전체 −5.59 N (t 0.987) · 본문은 그림 9a 를 'Fig. 8a' 로 부른다 (p.11 두 번)] |

## 6. Post-processing ★
- **무엇**:
  - **coordination number(eq 24)**: `C_n = n_c^(b)/N_b` (N_b=입자수, n_c^(b)=총 접촉수). 건조(Fig 6)·압연(Fig 7c) 진화. **stage 구분·치밀화 정량의 1차 지표**. [보강 2026-11-16 · 원문 식 (24) 귀속 [45] · 접촉 하나를 몇 번 세는지 원문에 없음 — 한 번 세면 보통 평균 배위수 Z = 2N_c/N_p 의 절반 (압연 끝 8.3 → Z 16.6 은 구 충전으로 어색 → 보통 Z 로 읽힌다 [카드 추론])]
  - **porosity(eq 25)**: `P = V_void/V_reg = 1 − V_mat/V_reg`(측정영역 내 공극/영역부피). 압연 진화(Fig 7b), 실험(Giménez[45], Hg-intrusion[ref32])과 대조. [보강 2026-11-16 · 측정 영역 V_reg 의 위치 · 크기와 겹침 처리 (구 부피 합 / 합집합) 원문에 없음 [미확인]]
  - **average stress(eq 26)**: `σ̄ = −1/V·Σ_{N_c} F^(c)⊗L^(c)` (N_c=측정영역 접촉수, F^(c)=접촉력벡터, L^(c)=두 입자 중심 잇는 branch vector, ⊗=외적, **압축이 음수**). 방향별 σ_xx/σ_yy/σ_zz(Fig 9a) — **두께방향 응력 추출이 핵심**. [보강 2026-11-16 · 원문 귀속 [49,57] · 측정 부피 V 정의 없음 — 판 힘 ÷ 단면 (121 MPa) 과 σ_zz (164 MPa) 가 1.36 배 다르다 [카드 산술]]
  - **contact network 진화**: 접촉망 완전도(굵은선=AM, 가는선=기타; Fig 4c) — **전자전도 *정성* 논증의 근거**(망 완전→e-경로↑).
  - **입자-집전체 접촉수**: 압연 진화(Fig 8) — 계면접착·계면저항 대리.
- **도구**: **PFC3D 5.00**(DEM + 내장 후처리), 본문 정의식(eq 24–26). **외부 전도도/τ 솔버(GeoDict·COMSOL·자체 Kirchhoff) 없음**. 실험 비교: Giménez [45] 압연 porosity, Hg-intrusion[ref32], EDS binder 분포[ref18,21], 입자파쇄[ref57].
- **수치화·플롯·기록 방식**: 모든 진화량을 **dimensionless time의 함수**로(Fig 6·7·8·9). porosity만 압력의 함수로도(Fig 3 검증). **σ_e/σ_ion은 plot 없음**(정성 결론).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (LIB, 건조+압연) | 우리 (ASSB cold-press) | 차이 / 이유 |
|---|---|---|---|
| **공정 모델링 범위** | **건조(fluid-sub) + 압연(plate)을 한 DEM 연속** | DEM 압밀(cold-press) → 네트워크 σ → grade + MPM morphology | ★ **그들은 건조까지** — 우리는 압밀에서 시작(건조=우리 미보유) |
| **★ 이온 채널 위상** | **공극(pore)=전도체**(액체전해질) → porosity GOOD | **SE 고체 입자망=전도체**(Holm 구속) → porosity BAD | **★★ 위상 정반대.** 압밀↑ → LIB 이온↓(공극↓) vs ASSB σ_ionic↑(SE접촉↑) |
| **★ 전달 솔버** | **없음 — σ_e *정성*(접촉망 완전도 논증), Bruggeman/RNM 미사용** | **명시 Kirchhoff + Holm 구속 + Stage-E** σ_ionic/e/thermal **삼중항**(수치) | ★★ **우리가 압도적 우위.** 그들은 σ_e 수치를 *안 줌*; 우리는 3채널 솔버 + LOOCV 스케일링 법칙 |
| **압밀 모드** | **calendering(압연 plate, z-속도 제어)** + 건조 침강 | **cold-press(단축, 변위 hold)** | 압연(저압·z-박막화) ≠ 고압 프레싱. 둘 다 변위/속도 제어(servo 아님) |
| **접촉법칙** | **PFC3D Hertz-Mindlin류(항복캡 없음, δ^1.5)** | Luding hooke/hysteresis(항복캡 없음) + Stage-E 소성면적 | **같은 no-cap 층**(층위지도 §1-A). 우리는 Stage-E로 소성면적 후보정 |
| **★ bond/binder** | **PFC3D linear bond 2종**: CBD=parallel(힘+모멘트), AM=contact(힘만), breakdown stress 파단 | CBD = Stage-2 부피점유(PTFE/VGCF); 명시 bond **없음**(backlog A3) | **세 번째 bond 청사진**(Sangrós 영구파단·Ngandjong SJKR재형성에 더해 *PFC3D 모멘트-전달 parallel bond*) |
| **★ 용매/건조** | **fluid-substitution**(부력+점성, eq 27–29; 모세관 명시無) | **없음**(ASSB는 dry-process/cold-press, 용매 無) | ★ **건조 = 우리가 *근본적으로* 안 다루는 축**(ASSB 건식공정). 단 dry-process 혼합/fibrillation 모델화 시 참고 |
| **접촉 소성** | **CONTACT 레벨(δ 프록시), 형상 불변** | MPM 진짜 SHAPE 소성 + DEM hooke/hysteresis | 입자 형상 안 변함(DEM); **형상변화 = 우리 MPM 고유**(frame[5]) |
| **E_AM** | E_NCM811 [정정 2026-11-16 · 원문 'AM' (NCM · 811 표기 없음)] **142 GPa** | E_CAM **140 GPa** | **거의 동일**(둘 다 NCM811; Sangrós 142.5·Ngandjong 200와도 정합대) |
| **E_CBD** | **0.65 GPa**(AM의 1/220, 매우 부드러움) | n/a(부피점유만) | Ngandjong 2 GPa보다 더 부드럽게 잡음 |
| **PSD** | **Gaussian 평균 13 µm std 0.61 = 거의 mono** | **bimodal 12:4:1**(AM_P/AM_S/SE) | ★ **그들은 mono-AM → Furnas dip 안 다룸**; 우리는 bimodal + dip 정량 |
| **검증** | **압연 porosity 실측**(Giménez[45], Hg[ref32]) + 입자파쇄 200 MPa | solver=ground truth(Minnmann [정정 2026-11-16 · 우리 쪽: 'Minnmann' 순수 SE 기공 앵커 = 출처 철회 (원장 CL-94 — Minnmann 2021 에 300 MPa 순수 SE 기공 값 없음) · 랩 표준 = 순수 SE 기공 10–13 %]·Cronau·Bazzoun 등) | 그들 압연 porosity 검증은 LIB 앵커(ASSB 직접 전이 불가) |
| **소재/전해질** | **NCM811 + 액체전해질**(LIB) [정정 2026-11-16 · 원문 'NCM' · '액체 전해질' 낱말 없음] | **LPSCl SE + NCM811**(ASSB) | CAM은 같으나 **전해질·이온위상 다름** → 절대 porosity·σ 직접 전이 금지 |

> ★★★ **위 표는 §A에서 모두 풀어 씀 — 아래 "## 우리 DEM+MPM 대비"가 정식 비교 섹션**(사용자 mandatory). §7은 요약표.

### frame[5] 위치
- **이 논문 = 전달/패킹 측 + LIB 건조/압연 공정**: rigid 구(AM+CBD) + Hertz 접촉 + PFC3D bond → DEM 압밀(건조+압연). **입자 형상소성·void-fill 없음**(CONTACT 레벨) — 우리 MPM이 메우는 *형상-morphology 절반*이 LIB DEM에도 빠짐 (**Sangrós·Ngandjong·Varkey·Bazzoun과 동일 — frame[5] 5번째 독립 확인**).
- **그들 σ_e는 *솔버 없는 정성 논증***(Bruggeman/RNM 미사용) → 우리 Kirchhoff/Holm/Stage-E 삼중항이 *수치로* 채우는 바로 그 칸 → **우리 transport novelty가 가장 선명하게 드러나는 peer**(§C).
- **그들 건조(fluid-substitution) = 우리가 *아예 안 가진* wet-process 절반** → frame[5]의 우리 쪽이 *압밀부터*임을 확인(건조 전 단계는 ARTISTIC/Lyu 영역).

---

## ★ 우리 DEM+MPM 대비 (comparison vs ours)

> 사용자 mandatory 섹션 A. 그들 DEM(rigid + CBD bond + 용매 + 건조) vs 우리 Luding hooke/hysteresis + Stage-E + 18× 연화; 그들 σ_e(DEM 정성) vs 우리 Kirchhoff+Holm 삼중항; LIB pore=전도체(Bruggeman) vs 우리 ASSB SE-network=전도체(Holm) 위상역전; 그들이 모델하는 *건조*(용매 증발)를 우리는 안 함(ASSB dry-process/cold-press).

### A-1. 접촉·압밀 머신: 같은 rigid-sphere DEM, no-cap 접촉, 형상 불변 (공통)
- **그들**: PFC3D 5.00, 입자 = 강체 구(AM 13 µm·CBD 2.2 µm), 접촉 = **Hertz-Mindlin류**(법선 δ^1.5, 접선 선형, 점성감쇠; eq 6–9) — **항복압 캡 없음**. CBD가 E=0.65 GPa로 부드러워 압밀을 흡수.
- **우리**: LIGGGHTS, 입자 = 강체 구(AM_P/AM_S/SE), 접촉 = **Luding hooke/hysteresis**(k₁ 로딩 / k₂ 언로딩 / k_c 점착) — **항복압 캡 없음**(접촉모델 층위지도 §1-A에 둘 다 같은 *no-cap* 층). **E_SE 18× 연화**(real 24 → effective 1.35 GPa)로 강체 구가 못 잡는 granular 재배열을 럼핑.
- **공통 한계(frame[5])**: 둘 다 **입자 형상 안 변함**(δ=소성 기하 프록시, 진짜 흐름 아님). Lyu도 Sangrós·Ngandjong·Varkey·Bazzoun처럼 *rigid-sphere + CONTACT-레벨*이라 **morphology/void-fill 절반이 빠짐** → **우리 MPM(J2 진짜 SHAPE 소성)이 메우는 칸**. **LIB DEM 5편 연속으로 같은 한계** = frame[5] 분업이 우리만의 변명이 아니라 *분야 공통 구조*임을 다섯 번째 독립 확인.
- **차이점(우리 후처리 우위)**: 그들은 접촉면적 후보정 없음(PFC3D 내장 Hertz 면적). 우리는 **Stage-E**(Tabor F/H + volume V/h 소성 접촉면적 재유도)로 *소성 접촉면적*을 명시 보정 → 전도도 솔버 입력 정밀화. Lyu에는 이 층이 없음(σ_e가 정성이라 불필요했음).

### A-2. ★★ σ_e: 그들 DEM *정성 논증* vs 우리 Kirchhoff+Holm *수치 삼중항* — 우리 결정적 우위
- **그들**: **σ_e/σ_ion을 수치로 산출하는 솔버를 돌리지 않는다.** "calendering이 전자전도를 향상"은 **접촉망 완전도**(배위수 3.6→8.3, 입자-집전체 접촉 897→2038)로부터의 *물리 논증*(tighter network → shorter e-paths → lower e-resistance[ref38]) + **"과압연 → 이온저항↑[ref48]"** caveat. **Bruggeman ε^1.5도, RNM/Kirchhoff도 없음.**
- **우리**: **명시 Kirchhoff 망**(Σ(φi−φj)/R=0) + **Holm 구속저항**(R=1/(2σr_c), 1967) + **Stage-E 소성 접촉면적** → **σ_ionic·σ_electronic·σ_thermal 삼중항을 *수치로*** 산출. 게다가 **솔버 출력을 LOOCV 스케일링 법칙으로 압축**(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.903).
- **대비의 의미**: **이게 우리 DEM novelty가 가장 선명한 칸.** Lyu는 "압연→전자전도↑"를 *접촉수로 추론*만 하는데, 우리는 *같은 접촉망에서 Holm 구속저항으로 σ를 풀어* 수치를 준다. **peer Sangrós(eq1 fabric 균질화)·Ngandjong(COMSOL FEM)은 적어도 σ 수치를 줬는데, Lyu는 그조차 안 줌** → **Lyu 대비 우리 transport 우위는 Sangrós/Ngandjong 대비보다 *더 큼***(그들은 솔버 자체가 없음). ⚠ 단 정직: Lyu의 *목적*은 구조진화·역학이지 transport 수치가 아니었음(그래서 정성으로 충분했음) — "그들이 못 했다"가 아니라 "그들 scope 밖, 우리 scope 안"이 정확.

### A-3. ★★ 이온 채널 위상 역전 — LIB pore=전도체(Bruggeman) vs ASSB SE-network=전도체(Holm)
- **LIB(이 논문)**: 활물질·CBD는 절연 매트릭스, Li⁺는 **공극을 채운 액체전해질**로 흐름. → 이온 전도체 = **공극상(pore phase)**, σ_ion = f(ε, τ) = **Bruggeman ε^1.5**(Lyu는 이걸 *명시 계산 안 하지만*, 본문이 "과압연→이온저항↑[ref48]"로 *공극 축소→이온 악화* 위상을 분명히 전제). **porosity = GOOD**(전해질 충전 공간).
- **우리 ASSB**: 액체전해질 없음. Li⁺는 **SE 입자가 서로 닿은 접촉망**으로만 흐름 → **공극 = 순수 방해물**, σ_ionic = **SE-SE 구속저항**(Holm) + Kirchhoff. **압밀하면 SE 접촉↑ → σ_ionic↑**. **porosity = BAD**(없앨수록 좋음, ~10 % 목표).
- **위상 정반대의 두 발현**:
  - **목표함수**: Lyu/LIB는 **porosity를 적당히 남김**(과압연 = 이온저항↑ 손해 → moderate calendering이 최적, trade-off). 우리 ASSB는 **porosity 최대 제거**(~10 %).
  - **압밀 방향성**: 압밀↑ → **LIB σ_ion↓**(공극↓·τ↑) vs **ASSB σ_ionic↑**(SE접촉↑). **부호 반대.**
- **→ 깔끔한 대조(Sangrós·Ngandjong 대비와 동일 축, 3번째 LIB peer로 보강)**: "액체전해질 LIB에서는 *공극*이 이온 전도체(porosity GOOD, 과압연은 이온저항↑)인 반면, all-solid-state 전극에서는 *고체전해질 입자망*이 이온 전도체(porosity BAD, 압밀↑→σ_ionic↑)다 — Lyu(2025)가 압연을 *moderate*에서 멈춰야 하는 이유(과압연→이온저항↑[ref48])가 바로 우리 ASSB가 *최대 압밀*을 추구하는 이유의 거울상이다." **Lyu·Sangrós·Ngandjong 3편이 같은 위상역전을 LIB쪽에서 독립 확인** → 우리 SE-network 솔버의 존재 이유를 3중 정당화.

### A-4. ★ 용매/건조 — 우리가 *근본적으로* 안 가진 wet-process 축
- **그들**: **fluid-substitution**(부력 F_b + 중력 F_g + 점성감쇠 F_r, eq 27–29)으로 용매를 coarse-grain → **건조(solvent evaporation) 자체를 DEM으로** 굴림. 건조 결과: 두께방향 속도구배(Fig 4b), **CBD top-enrichment**(binder migration, Fig 5; 집전체 계면 바인더↓→접착↓), 3-stage 건조 스킴(Fig 6).
- **우리**: **건조 없음.** ASSB는 **dry-process / cold-press**(용매 無 또는 최소). 우리 파이프라인은 *이미 형성된 분말 bed의 압밀*에서 시작.
- **대비의 의미**: **건조는 frame[5]의 우리 쪽에 *없는* 축** — 그들이 *앞서는* 정직한 칸. 단 **ASSB는 본질적으로 건식**이라 "우리가 뒤처졌다"가 아니라 **"셀 화학이 달라 건조 단계가 없다"**가 정확. 그래도 **ASSB dry-process 혼합·PTFE fibrillation을 언젠가 모델하려면** Lyu의 fluid-substitution(또는 Ngandjong의 CGMD 용매수축)이 *방법 청사진*. ⚠ 단 **모세관력(capillary)·표면장력은 Lyu도 명시 항으로 없음**(부력+점성만) → 건조 후기 모세관 압밀은 그들도 간접 — 우리가 dry-process 가면 *모세관 없는* 점이 오히려 단순화 이점.

### A-5. 압밀 곡선·응력·검증
- **압밀 P-vs-porosity**: Lyu Fig 3은 ~0–160 MPa서 57→22 %(저압 급강하 후 완만), Giménez[45] 실측과 일치. 우리 Heckel(pure-SE 4압력)은 R²=0.965·**P_y=138 MPa**. **둘 다 elastic→plastic knee + 포화** 형태지만 **압력대 다름**(LIB 압연 저압 vs ASSB 고압 300 MPa) + **소재·이온위상 다름** → **Fig 3 곡선을 우리 P-vs-porosity·Heckel과 직접 겹치면 안 됨**(정성 형태만 대응). LIB floor ~22 %(stiff NMC E=142 + 저압 + porosity 일부러 남김)는 우리 **강체 구 floor ~20 %**와 *우연히 비슷*하나 *물리는 다름*(우리는 소성흐름으로 그 아래 ~10 % 도달).
- **응력장**: Lyu Fig 9a의 **σ_zz≈−165 PEAK > σ_xx=σ_yy≈−130 MPa**(두께방향 우선) = 우리 **MPM 압밀 응력장**(z 우선 박막화)과 **직접 대응**. 그들 "z-응력을 입자파쇄 200 MPa 아래로"는 우리 **fracture-aware transport**(Auerbach/f_intact)와 연결 — 단 그들은 *경고*만(파쇄 모델 없음), 우리는 *fracture 솔버*로 깨진 접촉의 σ 손실을 정량.
- **검증 깊이**: Lyu = 압연 porosity 1개(Giménez) + Hg + 파쇄 + EDS 정성. 우리 = Minnmann porosity [정정 2026-11-16 · CL-94 출처 철회 · 랩 표준 10–13 %]·Cronau overlap·Bazzoun σ_ionic·SEM morphology 다중 앵커. ⚠ 둘 다 LIB/ASSB로 *절대값 직접 전이 금지*.

---

## 적용가능성 (applicability to our LIGGGHTS DEM model)

> 사용자 mandatory 섹션 B. 그들 명시 CBD + 용매 + 건조-stage 모델이 우리 backlog A3/A4/D5(CBD 명시 bond)와 co-rolling/dry-process 방향(Lee2025)의 청사진; 압연→두께방향 응력이 우리 압밀 응력에 매핑; LIGGGHTS에 CBD/용매 상을 추가할 수 있나; dry-ASSB vs wet-LIB 차이 명시. 우리 scripts/knobs에 매핑.

### B-1. CBD 명시 bond — *세 번째* 청사진(PFC3D parallel/contact bond) → backlog A3
- **현재 우리**: CBD를 **Stage-2 부피점유**(PTFE/VGCF가 SE 도메인 부피 차지)로만, 명시 입자-입자 bond 없음(`docs/digest_model_application_backlog.md` A3).
- **Lyu가 주는 것**: **PFC3D linear bond 2종** — **CBD = parallel bond(힘+모멘트 전달, eq 15–22)**, **AM = contact bond(힘만)**, breakdown stress σ̄_c/τ̄_c 파단. ★ **소재별 bond 차등이 핵심 시사**: 바인더상(CBD)은 *굽힘/비틀림 모멘트를 전달*(parallel bond)해야 "구조를 잡는" 거동이 나오고, AM-AM은 힘만으로 충분.
- **3개 CBD 청사진 비교(우리 선택지)**:
  | 모델 | bond 물리 | 파단 | 우리 적용 |
  |---|---|---|---|
  | **Sangrós 2020** | 점-bond(법선·접선 힘, 강성 6e12 N/m³) | **영구파단**(2e13 N/m²) | 단순·검증됨; 모멘트 無 |
  | **Ngandjong 2021** | SJKR 점착(CED×A) | **끊김·재형성**(reversible) | PTFE cold-weld(`--coh`)에 직결 |
  | **Lyu 2025(PFC3D)** | **parallel bond(힘+모멘트)** vs contact bond(힘) | breakdown stress, open | **모멘트 전달 = 섬유망 휨강성**에 가장 가까움 |
- **→ LIGGGHTS 매핑**: LIGGGHTS는 PFC3D parallel bond에 해당하는 **`bond` fix(cohesive bond, Potyondy-Cundall류)**가 있음 → **CBD-CBD에 모멘트-전달 bond, AM-AM에 힘-only bond**를 Lyu처럼 차등 적용 가능. ★ **PTFE 섬유는 *휨강성*이 있으므로**(fibrillated 망) **Lyu의 parallel bond(모멘트 전달)가 Sangrós 점-bond보다 PTFE에 더 적합** — Ngandjong SJKR(재형성·등방)과 Lyu parallel-bond(모멘트·구조적)를 *결합*(끊김재형성 + 휨강성)하는 게 우리 fibrillated-PTFE 1차 근사로 이상적. 코드: `--coh`(점착) + bond fix(모멘트) 조합.

### B-2. ★ 용매/건조 상 — LIGGGHTS에 추가 가능하나, dry-ASSB라 *우선순위 낮음*
- **추가 가능성**: Lyu의 **fluid-substitution(eq 27–29)**은 *명시 CFD 없이* 입자별 부력+점성감쇠 힘만 추가 → **LIGGGHTS에 `fix addforce`(부력·중력 차) + `fix viscous`(속도비례 감쇠 F=−αv)로 거의 그대로 구현 가능**(매우 저렴). 건조 = α를 시간에 따라 키우거나(점성↑) 부력 ρ_liquid를 0으로 ramp.
- **⚠ dry-ASSB vs wet-LIB**: 우리 소재계(LPSCl + NCM811 + PTFE/VGCF)는 **건식 co-rolling / cold-press**(`papers/lee2025_*` = 건식 공정 실험 앵커)라 **용매 건조 단계가 *원천적으로 없음***. 따라서 Lyu의 건조 모델은 **우리 production 파이프라인엔 직접 쓸 일 없음**.
- **단 D5(co-rolling/dry-process) 방향엔 유용**: 만약 ASSB **dry-process 혼합·PTFE fibrillation의 동역학**을 모델하려면(Lee2025 co-rolling의 *공정* 재현), Lyu의 fluid-sub *프레임*(입자별 환경력 추가)을 **용매 대신 *전단/혼합력*으로** 변용 가능. fibrillation은 PTFE의 shear-draw(`docs/cbd_morphology_roadmap.md`)라 *유체*가 아니라 *전단*이지만, "입자에 공정-환경력을 per-particle로 더한다"는 *구조*는 동일.

### B-3. 압연→두께방향 응력 → 우리 압밀 응력·fracture에 매핑
- **Lyu Fig 9a(σ_zz PEAK −165 MPa, 두께방향) + 입자파쇄 200 MPa 경고** → 우리 **MPM 압밀 응력장**(이미 z 우선)과 직접 대응. ★ **흡수 포인트**: Lyu는 "z-응력 < 입자 파쇄응력 유지"를 *설계 기준*으로 명시 — 우리 **fracture-aware σ**(Auerbach/f_intact/frac_severe)에 **"압밀 z-응력이 입자강도 초과 시 파쇄→접촉손실→σ 손실"** 인과를 더 명시적으로 넣을 근거(우리는 이미 fracture 솔버 보유 → Lyu의 *경고*를 *정량 솔버*로 이미 채움 = 우리 우위 + 그들 동기 정당화).
- **코드 매핑**: 우리 `scripts/network_conductivity.py`의 fracture 분기(Auerbach 임계) + MPM 응력장(`scripts/mpm3d_compaction.py` wallP/σzz readout)이 Lyu의 σ_zz·파쇄경고를 *이미 정량화*. Lyu는 "압밀응력이 z-편향"을 LIB-DEM으로 확인 → 우리 MPM σzz가 같은 z-편향을 ASSB로 재현하는지 cross-check 거리.

### B-4. 3-stage 건조 + 배위수 진화 → 우리 압밀 단계론과 개념 대응
- Lyu의 **배위수 증가율로 건조를 3-stage 구분**(HDR-LDR-HDR, Fig 6) + **압연 Z dip-then-rise**(Fig 7c, 3.6→2.3→8.3)는 *공정 진화를 Z로 추적*하는 방법론. 우리는 압밀을 *압력의 함수*로 보지만, **Lyu처럼 *시간/변위의 함수로 Z 진화*를 추적**하면 압밀 중 재배열·접촉형성 단계를 더 미시적으로 볼 수 있음 → 우리 DEM dump 시계열에서 Z(t) 추출은 이미 가능(`coordination` 후처리). **압연 초기 Z dip**(구조 안정성 파괴→재배열)은 우리 압밀 초기 거동과 비교 거리.

### B-5. dry-ASSB vs wet-LIB — 종합 정리
- **우리가 가져갈 것**: ① CBD 명시 bond(parallel-bond 모멘트 전달, B-1) — *직접 유용*(backlog A3); ② z-응력/파쇄 인과(B-3) — *이미 보유, 정당화*; ③ Z(t) 진화 추적(B-4) — *방법론*.
- **우리가 안 가져갈 것**: ① 건조/용매(B-2) — ASSB 건식이라 원천 무관(단 D5 dry-process엔 *프레임*만); ② Bruggeman/pore-이온(위상역전) — 우리 SE-network와 정반대; ③ porosity GOOD 목표 — 우리 BAD.
- **결론**: Lyu는 **CBD bond 모델화(A3)의 세 번째·가장 구조적(모멘트) 청사진**이자 **압밀 z-응력·파쇄의 LIB 확인**으로 우리에게 *부분적으로* 유용. 건조·이온위상·porosity-목표는 LIB 특유라 전이 불가. **핵심: "CBD parallel-bond(모멘트) 차등 적용 + z-응력 파쇄 인과"가 우리 LIGGGHTS에 실제 흡수 가능한 두 조각.**

---

## ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)

> 사용자 mandatory 섹션 C. 사용자가 firm한 DEM novelty를 원함 — **우리가 SOTA임을 분명히 주장.** 7개 차별점을 Lyu 2025 대비 매핑. 정직하게 그들이 앞서는 칸(건조·CBD·용매)도 명시. evidence-based; LIB-not-ASSB scope 명시.

**총평: Lyu 2025는 "LIB 전극 구조진화(건조+압연)를 한 DEM으로 연속 시뮬"한 견고한 *공정-역학* 논문이지만, *transport(전도도)는 정성 논증에 그치고, 입자는 rigid 구(형상소성 없음)이며, 단분산 AM(dip 없음)이다.* 우리는 그 *비어 있는 칸 셋*(수치 transport 삼중항 / 진짜 소성 morphology / bimodal dip)을 정면으로 채우면서, 추가로 fracture·literature-grounded σ·dual-model 독립검증·LOOCV 예측기까지 갖춘다. 따라서 *transport·morphology·예측* 축에서 우리가 명백히 SOTA이고, Lyu는 *건조/CBD/용매*라는 wet-process 공정 축에서 우리보다 앞선다.** (단, 우리 = ASSB, Lyu = LIB — *셀 화학이 다른 보완 관계*임을 항상 병기.)**

| # | 우리 차별점 | Lyu 2025는? | 증거 / 우위 정도 |
|---|---|---|---|
| **1** | ★ **전달 TRIAD via Kirchhoff + Holm 구속** (σ_ionic/e/thermal *수치*) | **σ_e *정성*만**(접촉망 완전도 논증), σ_ion 미산출, Holm 구속 물리 無, Bruggeman/RNM 無 | ★★★ **압도적 우위.** Lyu는 transport *수치 자체가 없음* — Sangrós(균질화)·Ngandjong(FEM)보다도 transport는 *덜* 함. 우리 Holm R=1/(2σr_c)+Kirchhoff 3채널 = *완전히 비어 있는 칸* |
| **2** | ★ **Stage-E 소성 접촉 AREA**(Tabor F/H + volume V/h 재유도) | **없음**(PFC3D 내장 Hertz 면적; σ_e 정성이라 면적 정밀화 불요) | ★★ 우위. 우리는 *소성 접촉면적*을 별도 보정 → 전도도 솔버 입력 정밀(Lyu엔 해당 층 자체가 없음) |
| **3** | ★ **DEM↔MPM scaffold + J2 진짜 소성 MORPHOLOGY**(SEM 코어보존+경계평탄화 ✓, void-fill flow, Σdg 변형장) | **rigid 구 + bond, 형상 불변**(CONTACT 레벨, δ 프록시) | ★★★ 우위. Lyu는 *형상소성 절반이 빠짐*(frame[5]) — Sangrós·Ngandjong·Varkey·Bazzoun과 **5번째 동일 한계**. 우리 MPM이 *유일하게* 그 칸 보유 |
| **4** | ★ **fracture-aware transport**(Auerbach/Lawn, 깨진 접촉의 σ 손실 정량) | **입자파쇄 *경고*만**(실험 200 MPa 인용; 파쇄 솔버 無) | ★★ 우위. Lyu는 "z-응력<파쇄응력 유지"를 *설계 기준*으로 말만 함 — 우리는 *fracture 솔버*로 파쇄→접촉손실→σ 손실을 *정량*(그들 동기를 우리가 이미 채움) |
| **5** | ★ **literature-grounded σ_grain**(Cronau 단결정 3.0 + Cronau(r_SE) sub-µm 인자) [정정 2026-11-16 · 우리 쪽 (원장 CL-91 · SELF-51): σ_grain 3.0 = Cronau 2021 SI 그림 S2c µC 펠릿 값 ('단결정' 아님) · Cronau(r_SE) = Cronau 2022 원문에 없는 모델 가정] | **n/a**(LIB·σ 정성이라 σ_grain 입력 자체 없음) | ★ 우위(축이 다름). 우리 σ는 *재료물성에 anchor*; Lyu σ_e는 *접촉수 추론* |
| **6** | ★ **실험-anchored INDEPENDENT dual-model**(DEM·MPM 각각 실험에 보정, 서로 cross-fit 금지 — frame[4]/[5]) | **단일 DEM**(MPM·이중모델 無; 검증=압연 porosity 1점 + 정성) | ★★ 우위. 우리는 *두 독립 모델의 수렴=교차검증*(frame[4]) — Lyu는 단일 모델·단일 porosity 앵커 |
| **7** | ★ **solver→scaling-law LOOCV 예측기**(σ_ionic 0.975/σ_e 0.953/σ_thermal 0.903; design knobs→metrics) | **없음**(공정진화 시뮬, 예측 법칙 無) | ★★ 우위. 우리는 솔버를 *예측 가능한 법칙으로 압축* — Lyu는 case-by-case 시뮬 |

### ★ 정직하게, Lyu가 *앞서는* 칸 (over-claim 방지)
- **(가) 건조(solvent evaporation)를 DEM으로 연속 시뮬** — **우리 *근본적으로* 미보유**. fluid-substitution(부력+점성)으로 건조 침강·CBD top-enrichment·3-stage 스킴을 잡음. ⚠ 단 **ASSB는 건식**이라 "우리가 뒤처졌다"가 아니라 *셀 화학상 건조 단계가 없다* — 보완 관계.
- **(나) CBD를 *명시 입자상 + bond*로 모델** — 우리는 Stage-2 부피점유만(명시 bond는 backlog A3, *미구현*). Lyu(+Sangrós/Ngandjong)가 CBD bond를 *이미 구현*. ★ **이건 우리가 *따라가야 할* 칸**(그들 청사진 = §B-1).
- **(다) 건조+압연 *한 코드 연속*** — Ngandjong은 CGMD→DEM 코드전환, Lyu는 PFC3D 한 코드로 끊김 없이. *공정 사슬 연속성*은 그들이 앞섬(우리는 압밀 단일 공정).
- **(라) 압연 porosity 실측 직접검증**(Giménez[45]) — LIB 압연 앵커. 단 ASSB로 전이 불가.

### ★ 종합 positioning (한 문단, deck용)
"Lyu(2025)·Sangrós(2020)·Ngandjong(2021) — LIB 전극 제조 DEM의 세 SOTA — 는 모두 **rigid 구 + CONTACT 접촉 + CBD bond**로 압밀을 굴리고 **이온 전도체를 *공극*(Bruggeman, porosity GOOD)**으로 둔다. 우리 ASSB DEM+MPM은 이 셋과 **이온위상이 정반대**(SE 입자망=전도체, Holm 구속, porosity BAD)이고, 세 가지를 *추가*한다: ① **수치 transport 삼중항**(Kirchhoff/Holm/Stage-E — Lyu는 σ_e조차 정성), ② **진짜 소성 morphology**(MPM J2 — LIB DEM 5편 전부 형상 불변), ③ **bimodal Furnas dip**(Lyu는 단분산 AM). 거기에 fracture 솔버·literature σ_grain·independent dual-model·LOOCV 예측기까지 더해 **transport·morphology·예측 축에서 SOTA**다. 정직히 **건조/CBD-bond/용매는 그들이 앞서지만**(wet-process 공정 — ASSB 건식엔 원천 무관하거나 우리 backlog A3), 이는 *셀 화학이 다른 보완 관계*이지 우리 핵심 novelty(고체 transport + 소성 morphology)를 잠식하지 않는다."

---

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **paper 대조축 — "LIB 제조 DEM 3종(Sangrós·Ngandjong·Lyu) 모두 이온=공극(porosity GOOD), transport는 균질화/FEM/*정성* — 우리만 SE-network 수치 솔버 + porosity BAD"**: Lyu는 *transport 수치가 아예 없는* 가장 극단 케이스라 우리 Kirchhoff/Holm 삼중항의 우위가 *가장 선명*. 세 LIB peer를 묶어 우리 ASSB transport novelty를 3중 정당화.
- ② **CBD 명시 bond 3번째 청사진(backlog A3)**: Lyu의 **PFC3D parallel bond(힘+모멘트, CBD) vs contact bond(힘, AM)** 차등 = **PTFE 섬유 *휨강성*에 가장 적합**(Sangrós 점-bond·Ngandjong SJKR보다). LIGGGHTS bond fix(모멘트) + `--coh`(점착) 조합 → Ngandjong 재형성 + Lyu 모멘트 = fibrillated-PTFE 1차 근사.
- ③ **z-응력/파쇄 인과 = 우리 fracture 솔버 *정당화***: Lyu의 "압밀 σ_zz PEAK > 면내 + 입자파쇄 200 MPa 회피" = 우리가 *이미 fracture 솔버로 정량화한* 인과의 LIB 확인. 우리 MPM σzz(z 우선)이 같은 편향을 ASSB로 재현하는지 cross-check.
- ④ **건조 = 우리 미보유 축(정직)**: ASSB 건식이라 직접 무관하나, **D5 dry-process/Lee2025 co-rolling** 모델 시 fluid-sub *프레임*(per-particle 환경력)을 *전단력*으로 변용 가능(방법론).
- ⑤ **데이터**: `docs/data/lyu2025_drying_calendering.csv` — 압연 porosity(57→22 %, stated/digitized)·두께(80→40 µm)·배위수(건조 0→3.6, 압연 3.6→2.3→8.3)·입자-집전체 접촉(897→2038)·응력(σ_zz −165 PEAK, σ_xx=σ_yy −130)·압연력(plate/collector −4.9/−5.7 N)·DEM 파라미터(E_AM 142/E_CBD 0.65 등)·bond·fluid-sub. **⚠ σ_e는 정성(수치 행 없음); LIB·액체전해질·저압 압연이라 절대 porosity·이온위상 ASSB 전이 금지, 추세·방법·CBD-bond 대조용.** [보강 2026-11-16 · 이 CSV 는 정본 litdb 가지에 없다 (코드 가지 docs/data) · 판독 원자료 = `litdb/figures/lyu2025_3d_dem_drying_calendering_lib/digitized.csv` (129 행)]

## 9. 인용 가능 문장 (deck/paper용)
- "Lyu et al. (2025, Shanghai University) simulated Li-ion cathode (NCM811 + carbon-binder domain) [정정 2026-11-16 · 원문 'NCM'] microstructure evolution through **both drying and calendering in a single continuous 3D DEM** (PFC3D), representing the solvent by a **fluid-substitution model** (buoyancy + velocity-dependent viscous damping, no explicit CFD/capillary) and using **two PFC3D bonds — a moment-transmitting linear parallel bond for the CBD and a force-only linear contact bond for the active material**; they derived a **three-stage drying scheme** (high-low-high drying rate) from the coordination-number evolution and showed calendering raises mechanical integrity (particle–collector contacts 897→2038, +230 % [정정 2026-11-16 · 2038/897 = 2.27 → +127 %]; coordination 3.6→8.3) with the **peak compressive stress in the thickness direction** (σ_zz ≈ −165 vs σ_xx=σ_yy ≈ −130 MPa)."
- "Unlike Sangrós (analytic homogenization) or Ngandjong (COMSOL FEM), Lyu (2025) reports **no numerical conductivity** — the calendering→electronic-conductivity claim rests on a **qualitative contact-network-completeness argument**, with no Bruggeman or resistor-network solver. Our ASSB DEM+MPM fills exactly this gap with a **numerical Kirchhoff/Holm constriction-resistance triad** (σ_ionic/electronic/thermal), making the transport-side novelty against Lyu even larger than against the homogenization/FEM LIB peers."
- "Across the three state-of-the-art Li-ion manufacturing DEMs (Sangrós 2020, Ngandjong 2021, Lyu 2025) the ionic conductor is always the **pore phase** (Bruggeman, porosity beneficial, over-calendering raises ionic resistance), whereas in our all-solid-state electrode the **solid-electrolyte particle network** is the ionic conductor (Holm constriction, porosity detrimental, densification raises σ_ionic) — Lyu's need to stop at *moderate* calendering is the mirror image of our drive toward *maximum* densification."

## 10. 주의/한계 (over-claim 방지)
- **LIB (액체전해질)** — 이온 채널이 **공극(Bruggeman·porosity GOOD)**이라 이온 위상·porosity 목표·압밀방향(압밀↑→이온↓)을 우리 ASSB(SE-network, 압밀↑→σ_ionic↑, porosity BAD)로 전이 **금지**. 전자·압밀역학·bond·z-응력만 물리 대응; **이온은 위상 자체가 반대**(대조용).
- **★ σ_e/σ_ion 수치 없음 — *정성* 결론** — Lyu는 Bruggeman/RNM/Kirchhoff/FEM **전도도 솔버를 안 돌린다.** "압연→전자전도↑"는 **접촉망 완전도 논증**(배위수·집전체 접촉수↑)일 뿐 *수치 σ 산출 아님*. → 우리 비교에서 **σ_e는 *정성 추세*로만**(Sangrós eq1·Ngandjong FEM과 *결정적으로 다름* — 그들조차 수치를 줬는데 Lyu는 안 줌). CSV의 σ_e 행은 *qualitative*로 표기.
- **강체 구 + Hertz CONTACT(항복캡 없음)** — 입자 **형상 안 변함**(δ=기하 프록시). **형상소성·void-fill 없음** → 우리 MPM 영역과 별개(frame[5], LIB DEM 5번째 동일 한계). CBD의 "변형"도 입자 E가 낮을 뿐(0.65 GPa) 형상흐름 아님.
- **fluid-substitution(부력+점성)만 — 모세관·표면장력 명시 항 없음** — 건조 후기 capillary 압밀·표면장력 유발 바인더 이동은 *간접*(부력 소멸의 결과로 CBD top-enrichment가 *나타남*). 명시 capillary-bridge 모델(Lippke[28] 등) 대비 coarse. **건조 절대 동역학(시간 스케일)은 fluid-sub α 보정에 의존.**
- **압연 = calendering(저압, plate z-속도)** ≠ ASSB cold-press(고압 ~300 MPa, 변위 hold) — 압력대 다름 + 압밀모드(압연 z-박막화 vs 단축 hold) 달라 **Fig 3 P-vs-porosity 곡선을 우리 곡선/Heckel과 직접 겹치면 안 됨**(knee·floor 형태만 정성). LIB floor ~22 %가 우리 강체 floor ~20 %와 비슷한 건 *우연*(물리 다름 — 우리는 소성으로 그 아래 도달).
- **NCM811 + 액체전해질** [정정 2026-11-16 · 원문 'NCM' · '액체 전해질' 낱말 없음] — CAM은 우리와 같으나(E 142≈우리 140) **전해질·이온위상이 다름**. AM PSD = **Gaussian std 0.61 = 거의 단분산** → **bimodal/Furnas dip 안 다룸**(우리 12:4:1과 다름). 절대 porosity·σ 전이 금지.
- **응력·porosity·힘 값 일부 digitized**(Fig 7b/9a/9b 그래프에서 읽음) → **추세만(±)**. **stated**: porosity 57→22 %, 두께 80/60/40 µm, 배위수(3.6 start·8.3 max), 입자-집전체 접촉(897/1087/2038), 입자파쇄 200 MPa, Table 1(E·ρ·ν·마찰), AM PSD(13 µm·std 0.61), CBD 2.2 µm, 조성 94:6·65 wt%, bond λ=1.67, plate 0.01 m/s. **σ_zz/σ_xx/압연력 절대값은 digitized**(Fig 9 그래프).
- **검증 = 압연 porosity 1개 + Hg + 파쇄 + EDS 정성** — Sangrós(σ_el 4-point·접착 pull-off·porosity)·Ngandjong(indentation+porosity 2개 동시 + discharge + EIS)보다 *검증 descriptor 적음*. σ_e/σ_ion 실측 검증 없음(정성이라).
- 🔗 **관련 카드 (2026-11-16 한 줄 추가)**: [`sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811`](sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811.md) = 이 카드 L22 의 'Sonzogni [46] (압연 DEM)' 원문 카드 — lyu2025 원문 서론의 [46] 문장 (전자 성질 · 수직 인장 / 수평 압축 접촉) 은 그 원문과 같다 · 다만 lyu2025 원문 식 (6) F^l_n = (F^l_n)₀ − k_n(Δδ_n)^(3/2) 에 붙은 [46] 은 그 원문에 없는 식이다 (그쪽 법선 법칙 = 구간 선형 + 거듭제곱 경화 ζ 0.15) — 이 카드 L54 는 귀속 없이 옮겼다.

---

## 11. ★ 보강 의도 대조 — 이 논문의 참고문헌 = 후보 표 · wishlist 의 원 인용처 (68-2 번 파일 · 2026-11-16)

1저자가 이 원문을 준 까닭 (지시서): 이 논문의 참고문헌이 후보 표 여러 행의 **원 인용처**다 — N-68 Sonzogni 2024 = 참고 [46] (제목까지 적힌 목록) · [44] · [45] Sangrós Giménez · [47] Sun · [48] Xu · [49] · [50] Zhang · [51] · [52] Ge · [53] Ngandjong.  그래서 (가) 참고문헌 57 개를 원문 그대로 §18 에 옮기고 (나) 아래 표에서 **이 논문이 그 참고에 대해 한 말** (원문 문장 · 쪽) 과 **이 카드의 2 차 서술** (보강 전 줄 번호 — 보강은 줄 끝 · 줄 안 표지라 번호가 그대로다) 을 대조한다.  원문 문장 크롭 = `txt_p2_*` · `txt_p3_*` · `txt_p4_*` · `txt_p8_*` · `txt_p10_*` · `txt_p11_*` · 목록 크롭 = `txt_p12_references_44_57_*`.

| 참고 | 원문 목록 (줄임 · 전문 §18) | 이 논문이 그 참고에 대해 한 말 (원문 · 쪽) | 이 카드의 2 차 서술 (줄) | 판정 | 정본 카드 · 후보 표 · wishlist |
|---|---|---|---|---|---|
| [13] | Sahore 2020 ACS Sustain Chem Eng 8:3162 — '… aqueous-processed LiNi0.8Mn0.1Co0.1O2 cathodes' | p.1 *"Sahore et al. [13] investigated the cracking behavior of thick water-based LiNi0.8Co0.1Mn0.1O2 (NCM811) cathodes during drying"* — 이 논문에서 '811' 이 나오는 유일한 자리 | L13 · L20 · L38 · L117 · L121 · L236 · L246 이 'NCM811' 을 **이 논문 모델의 활물질**로 적음 | **다름** — 모델 쪽은 p.4 *"the slurry was composed of NCM, carbon black, polyvinylidene difluoride, and N-methyl-2-pyrrolidone"* · 표 1 'AM' → 일곱 줄 정정 표지 | 정본 카드 없음 (papers/ grep 'Sahore' 0) |
| [18] · [21] | Jaiser 2016 J Power Sources 318:210 (흑연 음극 · 막 고화 · 결합재 이동) · Font 2018 J Power Sources 393:177 (모델 + 실험 비교) | p.6 *"Energy-dispersive x-ray spectroscopy (EDS) experiments also demonstrated the existence of a binder concentration gradient in the thickness direction [18,21]"* · *"The phenomenon of binder enrichment at the top of the electrode after drying was observed in previous EDS experiments [18]"* · p.2 Font [21] *"constant high drying rates are unfavorable and result in the accumulation of binder near the surface and depletion near the current collector"* | L81 'EDS CBD top-enrichment[ref18,21]' · L90 'EDS 실험[ref18,21]과 일치' | **같음** · 한정: 목록 제목상 [18] = 흑연 **음극** · [21] = 모델 논문 — 양극 EDS 가 아니다 | 정본 카드 없음 |
| [19] · [20] | Jaiser 2017 Drying Technol 35:1266 ('threestage drying profile … anodes') · Altvater 2024 Energ Technol (흑연 음극 · 적외선 다단 건조) | p.6–7 *"90° peeling experiments have shown that using LDR in the middle of drying and HDR in the early and late stages of drying reduces the drying time while maintaining a high level of adhesion [19,20]"* · p.7 *"Qualitatively … consistent … Therefore, we speculate that both have the same intrinsic mechanism"* · p.1 [19] · [20] = *"for graphite anodes"* | L13 '실험 [19,20]과 정성 일치' | **같음** · 한정: 비교 대상 = **흑연 음극** 실험 (원문 p.1 이 적는다) ↔ NCM 양극 모델 · 같은 기전은 저자의 *"speculate"* | 정본 카드 없음 |
| [22] | Lyu · Dong · Guo 2024 Energ Technol 12:2400583 — '2D … during drying **and calendering**' | p.2 *"Lyu et al. [22] used the discrete element method (DEM) to develop a 2D model to study the evolution of the electrode structure during the drying process."* · p.4 유체 대리 *"was also used in our previous work [22]"* | L22 'Lyu [22] = 2D DEM 건조 → 본 논문이 그 3D 확장 + 압연 연결' | **일부 다름** — 서론 문장은 건조만이지만 목록 제목은 압연까지 (2D 판 원문 미확인) → L22 정정 표지 | wishlist L329 (다른 카드가 올림) |
| [25]–[27] | 목록: [25] Lombardo 2021 (탄소-결합재 이동 3D 건조) · [26] Yao 2023 (CGMD · 수계 양극 건조) · [27] Nikpour 2021 (불균일 · 건조 · 압연) | p.2 *"Nikpour et al. [25] used a multiphase smoothed-particle model"* · *"Lombardo et al. [26] proposed a physics-based 3D molecular dynamics model"* · *"Yao et al. [27] used coarse-grained molecular dynamics (CGMD)"* — 본문 이름과 목록 번호가 한 칸씩 어긋난다 | 카드 언급 없음 | **원문 문제** (카드 문제 아님 · 판정 안 함) | — |
| [26] (사례 조성) | Yao 2023 J Mater Process Technol 321:118154 — '… **water-based** cathode electrode drying' | p.4 *"In the case study reported here [26], the slurry was composed of NCM, carbon black, polyvinylidene difluoride, and N-methyl-2-pyrrolidone. The weight ratio of AM to CBD was 94:6, with the solid component accounting for 65 %."* | L45 '조성 … 슬러리[ref26]' | **같음** · 한정: 목록 [26] 제목 = 수계 ↔ 본문 NMP · PVDF — 위 행의 번호 어긋남과 같은 자리일 수 있다 [카드 관찰] | — |
| [28] | Lippke 2022 Energ Technol 11:2200724 (DEM 건조 구조 형성) | p.2 *"Lippke et al. [28] proposed a DEM-based model to study the drying process and captured the evolution in electrode thickness during the drying process. Hertz-Mindlin contact model was used for the contact between particles."* · p.4 CBD *"2.2 μm in diameter [28]"* · *"a fluid substitution model that is common in the literature [28]"* · F_b · F_g · F_r [28] | L44 'CBD 2.2 µm[ref28]' · L64 'fluid-substitution model[ref28]' · L244 '명시 capillary-bridge 모델(Lippke[28] 등) 대비 coarse' | L44 · L64 **같음** · L244 **원문 밖** — 이 원문은 [28] 을 세 힘의 출처로만 인용 · 정본 lippke2023 카드는 모세관 (Breinlinger) 항을 적는다 (그 카드 기준 맞음) | 정본 `lippke2023_dem_drying_structure_formation_lib` (DOI 10.1002/ente.202200724 · 그 카드 2023 ↔ 이 목록 '2022;11') |
| [31] | Srivastava 2020 ACS Appl Mater Interf 12:34919 (결합재 점착 · 중간 구조 · 수송) | p.2 *"the complex spatial interactions between the active material (AM) and CBD phases require different contact models [31]"* · p.4 *"(CBD cohesion strength and AM-CBD adhesion strength [31])"* | L61 'CBD cohesion + AM-CBD adhesion 물성차 [ref31] 반영' | **같음** | 정본 카드 없음 (ge2022 · lippke2023 · ngandjong2021 · zhang2026_xct 가 인용) |
| [32] · [33] | Meyer 2017 J Mater Process Technol 249:172 · Dominguez 2023 J Power Sources 580:233367 (흑연 + Si) | p.8 *"when the electrode thickness was reduced by approximately 40 % [32,33], the electrode density increased by approximately 75.4 % [32]"* · *"The porosity of the electrodes measured experimentally by the mercury intrusion method decreased from 57 % to about 20 % [32]"* · p.11 *"the pressure increased exponentially with decreasing porosity [32]"* | L27 'Hg-intrusion 57→~20 %[ref32]' · L29 '~40 % 두께감소 = ~75.4 % 밀도증가[ref32,33]' | **같음** · 한정 (정본 meyer2017 카드 기준 · 판정 안 함): 압연 전 57 % = 기하 (피크노미터) 기공 · 수은 압입 맞춤식은 0.52 에서 시작 (점근 0.16) — '수은 압입 57 %' 는 두 방법을 섞은 인용일 수 있다 · 75.4 % · 40 % 는 그 카드에 없다 | 정본 `meyer2017_calendering_compaction_resistance_line_load_exponential_model` · 후보 표 N-55 |
| [38] | Westphal 2017 J Storage Mater 11:76 (두 점 저항 · 건식 혼합 · 압연) | p.2 *"concluded that a more intimate network of particles enables shorter electron paths and more electrical contacts"* · p.10 *"tighter particle networks achieve shorter electron paths and more electrical contacts effectively reducing resistance [38]"* · p.11 *"the closer contact achieved at the active layer/current collector interface is directly correlated with a reduction in contact resistance at the interface [38]"* | L32 · L37 · L70 · L143 | **같음** | 정본 카드 없음 |
| [42] · [43] | Lundkvist 2023 Powder Technol 425:118574 · 2024 443:119873 | p.2 *"developed a DEM simulation model to link the local mechanical behavior of the positive electrode active layer to its global mechanical properties after calendering. They found that the mechanical properties of the electrodes are influenced by the structure and require a deeper analysis of the structural evolution."* | 카드 언급 없음 | — | wishlist L106 ([43] · 다른 카드가 올림) |
| [44] | Giménez 2018 Adv Powder Technol 29:2312–21 | p.2 *"Giménez et al. [44,45] characterized the electrode structure from the micro- to macro-scale by the developed DEM model and nano-indentation measurements. The changes in the bond number during calendering were also investigated in detail and quantitatively."* | 번호로는 언급 없음 · L13 · L22 의 'Sangrós (2020)' 은 이 목록에 없는 다른 논문 (= 정본 `sangros2020_lib_electrode_dem_mech_elec_ionic`) | **목록 밖 서술** → L22 보강 표지 | wishlist L328 (다른 카드가 올림) · 정본 카드 없음 |
| [45] | Giménez 2019 Powder Technol 349:1–11 | p.2 (위 문장) · p.4 *"The coordination number Cn was calculated as follows [45]"* · p.5 표 1 출처 [45,49,50] · *"the results of the calendering simulation were compared with the data of the electrode porosity data at different pressures measured by Giménez et al. [45] through the calendering experiment, as shown in Fig. 3. The simulation results are in good agreement with the experimental data."* | L20 · L75 · L81 · L88 'Giménez [45]' | **같음** · 판독 대조: 그림 3 실험 점 52.2 · 41.6 · 37.2 · 29.5 · 21.7 % = 정본 sangros2019 카드 표 1 (0.522 · 0.416 · 0.372 · 0.295 · 0.217 at 0 · 19.82 · 42.71 · 79.13 · 159.37 MPa) — 그 값은 **압연 뒤** 측정 · 이 논문 DEM 은 누른 채 [카드 추론] | 정본 `sangros2019_dem_calendering_lib_electrode` (DOI 10.1016/j.powtec.2019.03.020) |
| [46] | Sonzogni 2024 Powder Technol 442:119891 | p.2 *"Sonzogni et al. [46] studied the effect of calendering on the microstructure and electronic properties of the electrodes by DEM. The bonding structure induced by calendering involves mostly vertical tensile contacts and horizontal compressive contacts."* · p.3 *"The Fl n is calculated as follows [46]:"* → 식 (6) | L22 'Sonzogni [46](압연 DEM)' · L54 식 (6) (귀속 없이) | L22 **같음 (줄임)** → 원문 문장 보강 표지 · 식 (6) 의 [46] 귀속 = **원문 인용 문제** (정본 sonzogni2024 카드 · 정독 122: 그 원문에 이 식 없음) — 이 카드 문제 아님 | 정본 `sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811` · 후보 표 N-68 · wishlist L61 |
| [47] | Sun · Huang 2024 J Power Sources 611:234774 — '… 3D image-based modelling' | p.2 *"Sun et al. [47] developed a finite element model to study the evolution of electrode microstructure and mechanical properties during calendering. The microstructure of the electrode under different calendering degrees affects the electrochemical properties."* | L22 'Sun [47](압연 FEM)' | **같음** | 정본 · wishlist 없음 → 정독 batch_124 `## n` |
| [48] | Xu 2024 J Storage Mater 77:109939 — 'Pore-scale modeling … effect of calendering on … cathodes' | p.2 *"Xu et al. [48] investigated the effect of calendering on the effective cathode transport properties using a multiscale approach. The cell performance increased with increasing calendering."* · p.10 *"Note that light calendering results in reduced contact between particles, whereas excessive calendering leads to an increase in ionic resistance [48]."* | L22 'Xu [48](과압연→이온저항↑)' (서론 계보로) · L37 · L70 · L110 · L143 · L151 '과압연 → 이온저항↑[ref48]' | L22 **일부 다름** (서론 문장 = '압연할수록 셀 성능↑') → 정정 표지 · 나머지 줄 **같음** (p.10) · 원문 안 두 문장의 방향이 다르다 (원문 문제 · 판정 안 함) | 정본 · wishlist 없음 → `## n` |
| [49] · [50] | Zhang 2022 Powder Technol 409:117828 · Zhang 2024 Particuology 85:252 (구조 역학 + 열전달) | p.2 *"Zhang et al. [49,50] investigated the structural mechanics and microstructural evolution of porous electrodes during calendering using DEM, and found that increasing the number of contacts between particles can improve the conductive path within the electrode."* · p.4 배위수 분포 [49] · 평균 응력 [49,57] · 표 1 [45,49,50] · p.11 *"calendering can facilitate improved adhesion between AM particles and current collector [49] … excessive stress can also precipitate particle degradation [49,57]"* | L22 'Zhang [49,50](압연 DEM 응력분포)' | **일부 다름** ('응력 분포' 는 Ge [51,52] 문장) → 정정 표지 | [49] = wishlist L232 · L330 · [50] 정본 · wishlist 없음 → `## n` |
| [51] | Ge · Cumming · Smith 2022 Powder Technol 403:117366 | p.2 *"Ge et al [51,52] used the DEM to investigate the evolution of the electrode structure under different calendering conditions and used the bonding model to describe the mechanical response of the particles. The simulation results revealed the inhomogeneous stress distribution and anisotropic properties …"* · p.3 *"popular models for describing bond failure between particles [51,56]"* · p.4 식 (21)–(22) [51,52] · *"λ is 1.67 [51]"* · 기공 [51] · 평균 13 μm [51] · 판 0.01 m/s [51] | L22 'Ge [51,52](압연 + bonding model)' · L43 '실측[ref51]' · L46 λ · L47 0.01 m/s | L22 · L46 · L47 **같음** · L43 **일부 다름** ('실측' 낱말 없음) → 정정 표지 · 정본 ge2022 카드: 결합 생성 ζ_b 1.67 · 판 0.01 m s⁻¹ = 같다 · 평균 13 μm 은 그 카드에서 못 찾음 | 정본 `ge2022_xct_initial_structure_dem_calendering_nmc333` · 후보 표 N-67 |
| [52] | Ge 2023 Chem Eng J 465:142749 | p.3 *"The bond model is used to describe the mechanical responses of the binder phase [52]."* · p.4 식 (21)–(22) [51,52] · p.2 (위 Ge 문장) | L22 'Ge [51,52]' | **같음** | wishlist L326 (다른 카드가 올림) · 정본 카드 없음 |
| [53] | Ngandjong 2021 J Power Sources 485:229320 | p.2 *"Ngandjong et al. [53] used the DEM to study the effect of calendering on the mesostructure of the electrodes, and the effects of CBD distribution and drying were considered in the model."* · *"Drying and calendering are unavoidable continuous processes in the production chain of electrode manufacturing [53]"* | L22 'Ngandjong [53](압연 DEM, CBD+건조 함께 다룸)' | **같음** | 정본 `ngandjong2021_dem_calendering_digital_twin` |
| [56] | So 2021 J Power Sources 508:230344 (ASSB 금형 압력 · DEM) | p.3 *"The linear parallel bond model (Fig. 1b) and linear contact bond model (Fig. 1c) are popular models for describing bond failure between particles [51,56]."* | 카드 언급 없음 | — · 한정: 정본 so2021 카드 L58 = '명시 binder 없음 · 융착 결합 = cohesive 접촉' — linear parallel · contact bond 서술이 그 카드에 없다 (원문 인용 문제일 수 있다 · 그 카드 기준) | 정본 `so2021_dem_mold_pressure_assb_coldpress` |
| [57] | Stershic 2015 J Power Sources 297:540–50 | p.4 평균 응력 [49,57] · p.11 *"The experiment showed that particle fracture occurred when the stress of the electrode reached 200 MPa [57]."* · *"excessive stress can also precipitate particle degradation [49,57]"* | L35 '입자파쇄 임계응력(실험) 200 MPa · fracture onset · stated(ref [57])' | **같음 (원문 그대로)** · 한정: 정본 stershic2015 카드 기준 200 MPa = Ebner 2013 의 명목 2000 bar 압연에서 깨진 입자가 보인 것 (문턱 측정 아님) → '임계응력 · fracture onset' 은 그만큼 좁혀 읽는다 (L35 보강 표지) | 정본 `stershic2015_fabric_tensor_calendering_nmc_xct_dem` · 후보 표 N-69 |

⇒ **보강 의도 대조 결과: 일부 다름** — 카드가 다룬 참고의 2 차 서술 = 같음 15 ([18,21] · [19,20] · [26] · [28] L44 · L64 · [31] · [32,33] · [38] · [45] · [46] · [47] · [48] L37 등 · [51] L22 · L46 · L47 · [52] · [53] · [57]) · **일부 다름 4** ([22] L22 · [48] L22 · [49,50] L22 · [51] L43) · **다름 1** ([13] 의 'NCM811' 을 모델 활물질로 — 일곱 줄) · **원문 밖 2** (L13 · L22 'Sangrós 2020' · L244 Lippke 모세관).  고친 곳은 모두 그 줄에 정정 표지 (옛 표기 남김).
- **원문 자체의 인용 문제 (카드 문제 아님 · 판정 안 함)**: [25]–[27] 이름 ↔ 번호 어긋남 · [26] 수계 ↔ NMP · PVDF · [46] 식 (6) (sonzogni2024 카드) · [56] So 2021 결합 모델 (so2021 카드) · [57] 200 MPa 의 성격 (stershic2015 카드) · [32] 수은 압입 57 % (meyer2017 카드) · [48] 서론 ↔ p.10 의 방향 · [18] · [19] · [20] = 음극 실험 · 본문 'Fig. 8a' (= 그림 9a · p.11 두 번).

---

## 12. ★ 핵심 수치 — 원문 대조판 (쪽 · 표지 병기 · 2026-11-16)

표지: [인쇄] = 본문 · 표 · 그림 안 글자 · [판독] = 그림에서 읽은 값 (원 래스터 · 눈금 직선 맞춤 · `digitized.csv` 129 행) · [카드 산술] = 식을 같이 · [미확인] = 원문 12 쪽 + 영상 4 에 없음.

### 12-1. 입력 (표 1 · §2.3)
| 항목 | 값 | 원문 위치 | 표지 | 이 카드 (보강 전 줄) |
|---|---|---|---|---|
| 입자 밀도 AM / CBD | 4.74 / 2.2 g cm⁻³ | 표 1 (p.5) | [인쇄] | L40 같음 |
| 영률 AM / CBD | 142 / 0.65 GPa | 표 1 | [인쇄] | L38–L39 같음 ('NCM811' 만 정정) |
| 푸아송 비 AM / CBD | 0.25 / 0.2 | 표 1 | [인쇄] | L41 같음 |
| 미끄럼 마찰 AM / CBD | 0.12 / 0.1 | 표 1 | [인쇄] | L42 같음 |
| 구름 마찰 AM / CBD | 0.012 / 0.01 | 표 1 | [인쇄] | L42 같음 |
| 표 1 출처 | [45,49,50] | 표 1 머리 | [인쇄] | 카드에 없었음 |
| AM 지름 | 가우스 평균 13 μm [51] · 표준편차 0.61 (단위 없음) | p.4 | [인쇄] | L43 일부 ('실측' 정정) |
| CBD 지름 | 2.2 μm — 카본 + 결합재 유효 입자 [28] | p.4 | [인쇄] | L44 같음 |
| 입자 모양 | 구 — *"assumed to be spherical for simple"* | p.4 | [인쇄] | L44 같음 |
| 조성 | AM : CBD = 94 : 6 (무게) · 고체 65 % (AM + CBD 질량 ÷ 슬러리 질량) [26] | p.4 | [인쇄] | L45 같음 |
| 슬러리 재료 | NCM · 카본블랙 · PVDF · NMP | p.4 | [인쇄] | L20 'NCM811' 정정 |
| RVE | 슬러리 200 × 200 × 200 μm · 처음 두께 = 실제 슬러리 두께 [11] | p.4 | [인쇄] | L48 같음 |
| 경계 | x · y 주기 · 아래 집전체 (입자가 못 내려감) · 위 자유 (건조) / 누름판 (압연) | p.4 | [인쇄] | L48 같음 |
| 건조 끝 | *"The drying simulation ends when a stable structure is formed."* | p.4 | [인쇄] | L68 같음 |
| 압연 | 판 z 방향 일정 0.01 m/s [51] · 처음 상태 = 건조 끝 구조 · *"The top pressure plate represents the roller"* | p.4 | [인쇄] | L47 · L74 같음 |
| 결합 생성 | λ = 1.67 [51] (식 23) | p.4 | [인쇄] | L46 같음 |
| 결합 배정 | 선형 접촉 결합 = AM–AM · AM–집전체 / 선형 병렬 결합 = CBD–CBD · CBD–AM · CBD–집전체 | p.4–5 | [인쇄] | L60–L61 같음 |
| 코드 | PFC3D version 5.00 | p.5 | [인쇄] | L51 같음 |
| 감쇠 β_n · β_s · α · 용매 밀도 ρ_liquid · k_n · k_s 값 · 결합 강성 k̄_n · k̄_s · k̄_b · 결합 강도 σ̄_c · τ̄_c · 결합 반경 · 시간 간격 · 입자 수 · 건조 · 압연 실제 시간 · 씨앗 · 측정 영역 V_reg · V | — | 원문 12 쪽 전수 | [미확인] | L76 (씨앗) 만 |

### 12-2. 결과
| 양 | 원문 값 | [판독] | 위치 | 이 카드 |
|---|---|---|---|---|
| RVE 두께 (압연) | 80 → 40 µm (본문 p.8) · 그림 7a 글자 'h ≈ 80µm' · 'h = 60µm' · 'h = 40µm' | — | p.7 · p.8 · 그림 7a | L29 (중간 시각 t 0.5 → [미확인]) |
| 기공 (압연) | ≈57 → ≈22 % (p.8) | 57.0 (t ≤ 0.2) · 53.3 (0.4) · 45.3 (0.6) · 33.3 (0.8) · 21.7 % (1.0) | 그림 7b | L27–L28 같음 |
| 배위수 건조 끝 = 압연 시작 | 3.6 (p.9) | 그림 6 끝 ≈3.45 (3.40–3.49) · 그림 7c 시작 3.58–3.61 | p.9 · 그림 6 · 7c | L30 (0.15 차 표지) |
| 배위수 최저 (압연) | *"decreased slightly"* (p.9) | 2.27–2.29 (t 0.22–0.30) | 그림 7c | L31 같음 (≈2.3) |
| 배위수 끝 (압연) | 8.3 (p.10) | 8.10 | 그림 7c | L31 (0.2 차 표지) |
| 건조 단계 경계 | 말로만 (I · III 느림 · II 빠름 · p.6) | t 0.437 · 0.888 | 그림 6 | L91 (0.45 · 0.9) |
| 건조 중 배위수 | stage I *"decreased at first and then increased slowly"* (p.6) | 0.20 (t 0.05) · 0.22 (0.10) · 0.20 (0.15–0.20) · 0.36 (0.30) · 0.64 (0.437) · 1.06 (0.48) · 1.98 (0.6) · 2.59 (0.7) · 2.99 (0.8) · 3.33 (0.9) | 그림 6 | 카드에 없었음 |
| 집전체 접촉 수 | 897 → 2038 *"an increase of approximately 230 %"* (p.11) · 그림 8 글자 897 · 1087 · 2038 | — | p.11 · 그림 8 | L32 (+127 % 정정) |
| σ_zz (t 1) | 숫자 없음 (*"a notable increase along the z-axis"*) | −163.9 MPa | 그림 9a | L33 (≈−165 같음) |
| σ_xx · σ_yy (t 1) | 숫자 없음 (*"The equivalent average stresses along the x-y plane were maintained due to the periodic boundary conditions"*) | −127.4 · −129.5 MPa | 그림 9a | L34 (≈−130 같음) |
| 응력이 서는 때 | *"Initially, stress levels were negligible and isotropic"* | t ≈ 0.15–0.20 (σ_zz −1.8 → −5.5 MPa) | 그림 9a | 카드에 없었음 |
| 판 · 집전체 힘 (t 1) | 숫자 없음 · *"approximately equivalent"* · 끝에 집전체가 *"slightly greater"* | 판 −4.84 N · 집전체 −5.59 N (t 0.987 · t 1 외삽 ≈ −5.7) | 그림 9b | L36 같음 |
| 그림 3 DEM | — | 57.0 · 43.0 · 38.0 · 31.0 · 23.0 % (0.3 · 19.9 · 42.8 · 79.2 · 159.2 MPa) | 그림 3 | L75 · L88 (≈57 → ≈22) |
| 그림 3 실험 [45] | — | 52.2 · 41.6 · 37.2 · 29.5 · 21.7 % (0.2 · 19.7 · 42.6 · 79.1 · 159.2 MPa) | 그림 3 | = sangros2019 카드 표 1 |
| 입자 파쇄 응력 (인용) | 200 MPa [57] (p.11) | — | p.11 | L35 같음 (한정 표지) |
| 실험 압연 (인용) | 두께 −40 % [32,33] · 밀도 +75.4 % [32] · 수은 압입 57 → 약 20 % [32] | — | p.8 | L27 · L29 같음 |

### 12-3. 카드 산술 (식 병기)
- **고체 보존 점검**: (1 − P)·h = 0.430 × 80 = 34.4 µm ↔ 0.783 × 40 = 31.3 µm (−9 %) — x · y 주기라 단면이 같으면 같아야 하는 양 → 기공의 측정 영역 V_reg (식 25) 이 두께 전체가 아니거나 'h ≈ 80 µm' 의 ≈ 때문 [카드 추론 · V_reg 정의 원문 없음].
- **밀도 비**: (1 − 0.217)/(1 − 0.570) = 1.82 (+82 %) ↔ 실험 +75.4 % (두께 −40 % [32]) · 시뮬 두께 −50 %.
- **집전체 접촉**: 2038/897 = 2.272 (+127 %) · 1087/897 = 1.212 (+21 %) — 원문 '230 %' 는 비 2.27 을 증가율로 적은 것으로 읽힌다.
- **경계 반력 ↔ 접촉 virial**: 판 4.84 N ÷ (200 µm)² = 4.84 / 4.0 × 10⁻⁸ m² = **121 MPa** · 집전체 5.59–5.7 N → **140–142 MPa** ↔ σ_zz **164 MPa** → σ_zz 가 판 기준의 1.36 배 · 집전체 기준의 1.15–1.17 배 (단면 200 × 200 µm 유지 가정 · 식 26 의 V 정의 원문 없음).
- **측압 비** (t 1): σ_xx/σ_zz = 127.4/163.9 = 0.78 · σ_yy/σ_zz = 0.79.
- **'지수적' 힘 증가 점검**: 판 힘 t 0.4 · 0.6 · 0.8 · 1.0 = 0.70 · 1.63 · 3.09 · 4.84 N → ln 증분 0.85 · 0.64 · 0.45 (줄어든다) — 같은 Δt 마다 같은 비가 아니라 시간 지수꼴 아님 · 기공 축으로도 Δln F / ΔP = −0.106 · −0.053 · −0.039 (%p 당) 로 줄어 지수꼴 아님 (원문 *"escalated exponentially"* · [32] *"increased exponentially with decreasing porosity"*).
- **압연 시간 · 변형률 속도**: 판 0.01 m/s · 판 이동 = 두께 감소 40 µm 라면 4 ms · 처음 변형률 속도 0.01 ÷ 80 × 10⁻⁶ = 125 s⁻¹ (판 출발 위치 · 계산 시간 원문 없음).  우리 DEM 판 속도 0.01 mm/s 의 1000 배.
- **입자 수 추정**: 고체 중 AM 부피 분율 = (94/4.74)/(94/4.74 + 6/2.2) = 0.879 · 압연 끝 고체 0.783 × 200² × 40 = 1.253 × 10⁶ µm³ → AM 957 · CBD 27 170 · 건조 끝 고체 0.430 × 200² × 80 = 1.376 × 10⁶ µm³ → AM 1052 · CBD 29 840 (단분산 가정 · 표준편차 0.61 µm 이면 AM 부피 +0.7 %) — 두 값의 차 9 % = 위 고체 보존 어긋남.
- **그림 3 DEM − 실험**: +4.8 · +1.4 · +0.8 · +1.5 · +1.3 %p — 0 MPa 차가 가장 크다 (DEM 건조 끝 57 % ↔ 미압연 실험 52.2 %).
- **배위수 그림 ↔ 본문**: 건조 끝 3.45 ↔ 3.6 (−4 %) · 압연 끝 8.10 ↔ 8.3 (−2.4 %) · 압연 초기 3.6 → 2.28 = −37 % (원문 *"slightly"*).

---

## 13. ★ 방법 — 원문 식 전부 (식 1–29 · 크롭 = `eq_NN_*.png` · 2026-11-16)

### 13-1. 식 원장 (인쇄 그대로 · 뜻 · 주의)
| 식 | 원문 인쇄 (크롭) | 뜻 | 주의 · 표지 |
|---|---|---|---|
| (1) | m_i du_i/dt = F_c + F_i (`eq_01_translational_motion`) | 병진 운동 | F_i = *"the force exerted on the particle"* (건조 때는 식 27–29 의 힘 [카드 추론]) |
| (2) | I_i dω_i/dt = F_t × R_i (`eq_02_rotational_motion`) | 회전 운동 | R_i 를 *"radius"* 로 정의 — 벡터 곱 표기는 인쇄 그대로 |
| (3) | F_c = F^l + F^d (`eq_03_*`) | 접촉력 = 탄성 (인장 없음) · 마찰 + 소산 [54,55] | *"F^l provides elastic (no tension) and friction behaviors, and F^d provides the energy dissipation"* (p.3) |
| (4) · (5) | F^l = −F^l_n n_c + F^l_s · F^d = −F^d_n n_c + F^d_s (`eq_04_*` · `eq_05_*`) | 법선 · 접선 분해 | n_c = 접촉면 단위 법선 |
| (6) | F^l_n = (F^l_n)_0 − k_n(Δδ_n)^{3/2} (`eq_06_*`) | 법선 탄성력 — 시간 걸음 처음 값에서 법선 변위 **증분**의 3/2 승만큼 | 앞 문장 *"as follows [46]"* (원문 인용 문제 · §11) · (14) 의 k_n (N/m) 와 함께면 차원이 맞지 않는다 [카드 산술] |
| (7) | F^l_s = (F^l_s)_0 − k_s Δδ_s (`eq_07_*`) | 접선 (선형 증분) | 쿨롱 상한 식은 인쇄 없음 — 표 1 마찰 계수만 |
| (8) · (9) | F^d_n = (2β_n√(m_c k_n)) δ̇_n · F^d_s = (2β_s√(m_c k_s)) δ̇_s (`eq_08_*` · `eq_09_*`) | 감쇠 (dashpot) | δ̇ = 접점 법선 · 접선 속도 · β = *"coefficients of influence"* — 값 없음 |
| (10) | 1/E* = (1 − ν₁)²/E₁ + (1 − ν₂)²/E₂ (`eq_10_*`) | 유효 영률 | **인쇄 그대로 (1 − ν)²** — 보통 Hertz 꼴 (1 − ν²) 과 다르다 |
| (11) | 1/G* = 2(2 − ν₁)(1 + ν₁)/E₁ + 2(2 − ν₂)(1 + ν₂)/E₂ (`eq_11_*`) | 유효 전단 탄성률 | 정의 뒤 쓰이는 곳 원문에 없음 |
| (12) · (13) | 1/R* = 1/R₁ + 1/R₂ · m_c = m₁m₂/(m₁ + m₂) (`eq_12_*` · `eq_13_*`) | 유효 반지름 · 질량 | R* 가 쓰이는 식 원문에 없음 |
| (14) | k_n = AE*/L (`eq_14_*`) | 법선 강성 | A = *"contact area"* (구하는 식 없음) · L = 중심 거리 |
| (15) · (16) | F̄ = −F̄_n n_c + F̄_s · M̄ = M̄_t n_c + M̄_b (`eq_15_*` · `eq_16_*`) | 병렬 결합 힘 · 모멘트 | *"F_n > 0 denotes tension"* |
| (17)–(20) | F̄_n = (F̄_n)_0 + k̄_n Ā Δδ_n · F̄_s = (F̄_s)_0 − k̄_s Ā Δδ_s · M̄_t = (M̄_t)_0 − k̄_s J̄ Δθ_t · M̄_b = (M̄_b)_0 − k̄_b Ī Δθ_b (`eq_17_*`–`eq_20_*`) | 결합 증분 법칙 | (19) 소문자 j̄ · (20) k̄_b 인쇄 그대로 (k̄_b 정의 없음) · 강성 값 없음 |
| (21) · (22) | σ̄ = F̄_n/Ā + ‖M̄_b‖R̄/Ī · τ̄ = ‖F̄_s‖/Ā + abs(M̄_t)R̄/J̄ (`eq_21_*` · `eq_22_*`) | 결합 최대 수직 · 전단 응력 [51,52] | 파단 판정 문장 없음 — 그림 1a 에 *"σ̄_c / τ̄_c breakdown stress"* · *"Bond breaks in tension bend/shear torsion"* · *"(open)"* 글자만 · 강도 값 없음 |
| (23) | ‖P_i − P_j‖ ≤ λ(R_i + R_j) · λ = 1.67 [51] (`eq_23_*`) | 결합 생성 기준 | 결합이 언제 생기는지 (처음만 / 매 걸음) 원문에 없음 · *"particles either bond or separate from each other numerous times"* (p.3) |
| (24) | C_n = n_c^(b)/N_b (`eq_24_*`) | 배위수 [45] | 쌍 세기 미기재 (§6 표지) |
| (25) | P = V_void/V_reg = 1 − V_mat/V_reg (`eq_25_*`) | 기공 [51] | V_reg 위치 · 겹침 처리 미기재 |
| (26) | σ̄ = −(1/V) Σ_{N_c} F^(c) ⊗ L^(c) (`eq_26_*`) | 평균 (접촉 virial) 응력 [49,57] | *"compressive stress is negative by convention"* · V 미기재 |
| (27)–(29) | F_b = (4/3)πR_i³ρ_liquid g · F_g = (4/3)πR_i³ρ_solid g · F_r = α × v (`eq_27_*`–`eq_29_*`) | 유체 대리 [28] | *"the Fr is affected by the particle velocity and is not constant"* · α · ρ_liquid 값 없음 · 증발 구현 미기재 |

### 13-2. 계산 사슬 (재구성)
슬러리 RVE 200³ µm (AM + CBD 고르게 · 고체 65 wt%) → **건조**: 유체 대리 세 힘 (부력 · 중력 · 점성 감쇠) · x · y 주기 · 아래 집전체 · 위 자유 → 입자가 내려앉으며 부딪고 결합 → *"stable structure"* 에서 끝 (두께 ≈80 µm · 위 표면이 거칠다) → **같은 구조를 압연 입력으로** → 위 누름판이 z 로 0.01 m/s 하강 → 두께 40 µm 에서 끝 (**탈압 없음**) → 배위수 (식 24) · 기공 (식 25) · 평균 응력 (식 26) · 판 / 집전체 힘 · 집전체 접촉 수.  시간 축은 그림마다 **무차원 시간** (0–1 · 그림 6–9 축 이름 · 실제 시간 [미확인]).
- 압연 = 롤이 아니라 **평판**: *"The top pressure plate represents the roller used during calendering."* (p.4) — 롤 곡률 · 전단 · 마찰 구동 없음 (정본 sonzogni2024 의 실제 크기 회전 롤과 대비).
- 출발 상태의 효과: *"The change in porosity is not evident at the beginning of calendering because the rough top of the RVE causes the pressure plate to touch only the higher points of the top layer"* (p.8) — 판독상 t ≤ 0.2 기공 57.0 % 그대로 · σ_zz 가 t ≈ 0.15–0.2 에야 선다 (그림 9a) · 배위수는 그 사이 3.6 → 2.3 으로 먼저 떨어진다 (그림 7c).

### 13-3. 검증 (원문이 내세운 것 · 성격)
| 검증 | 원문 | 성격 |
|---|---|---|
| 그림 3 기공 ↔ 압력 | Giménez [45] 실험 (p.5) *"in good agreement"* | DEM = 누른 채 (탈압 없음) ↔ 실험 = 압연 뒤 (sangros2019 카드 표 1) · 차 +0.8 ~ +4.8 %p [판독 · 카드 산술] · DEM 점의 압력이 어느 응력인지 미기재 |
| 두께 · 밀도 | *"thickness was reduced by approximately 40 % [32,33], the electrode density increased by approximately 75.4 % [32]"* ↔ 시뮬 80 → 40 µm · *"a high degree of comparability"* (p.8) | 시뮬 −50 % · 밀도 +82 % [카드 산술] — 같은 압력 조건 대조 아님 |
| 수은 압입 기공 | *"decreased from 57 % to about 20 % [32]"* ↔ 시뮬 ≈57 → ≈22 % (p.8) | 끝값 대조 (압력 · 상태 표지 없음) |
| CBD 위쪽 몰림 | EDS [18,21] (p.6) | 정성 · [18] = 흑연 음극 |
| 3 단계 건조 | 90° 박리 실험 [19,20] · *"we speculate that both have the same intrinsic mechanism"* (p.7) | 정성 · 흑연 음극 |
| 판 · 집전체 힘 지수 증가 | *"consistent with previous experimental calendering results where the pressure increased exponentially with decreasing porosity [32]"* (p.11) | 정성 · 판독 곡선은 지수꼴 아님 [카드 산술] |
| 맞춘 값 | 없음 (표 1 = 문헌 [45,49,50] · 결합 · 감쇠 값 미기재) | 무엇을 무엇에 맞췄는지 원문 없음 |

### 13-4. 원문에 없는 것 (재현 불가 지점)
감쇠 β_n · β_s · 점성 계수 α · 용매 밀도 · 증발 구현 (ρ_liquid · α 의 시간 변화 · 용매 부피) · k_n · k_s 의 값 (식 14 의 A · L 을 어떻게 정했는지) · 결합 강성 · 강도 · 반경 · 결합 생성 시점 · 판 · 벽의 접촉 규칙 (판 쪽 결합 유무) · 시간 간격 · 입자 수 · 계산 시간 · 무차원 시간의 실제 길이 · 측정 영역 V_reg · V · 배위수 쌍 세기 · 씨앗 · 반복 수.

---

## 14. 그림 · 표 · 영상 — 크롭 원장 · 판독 (2026-11-16)

### 14-1. 그림 · 표 (11 장 — 전부 직접 열어 봄)
| 파일 | 내용 | 상태 |
|---|---|---|
| `fig_1.png` | 결합 모식: (a) bond-to-bond failure (F̄_n · M̄_b / F̄_s · M̄_t ↔ Δδ_n · Δθ_b / Δδ_s · Δθ_t · σ̄_c / τ̄_c breakdown stress · open) · (b) 선형 병렬 결합 (F̄_n · F̄_s · M̄) · (c) 선형 접촉 결합 (F̄_n · F̄_s) | **다시 자름** — 옛 크롭에 본문 식 (17) 줄이 섞였다 → 래스터 (xref 38) ± 1.5 pt |
| `fig_2.png` | 처음 RVE: (a) 건조 (200 µm 상자 · AM 초록 · CBD 빨강 · 집전체 노랑) · (b) 압연 (+ 누름판) | 자동 그대로 |
| `fig_3.png` | 기공 (%) ↔ 압축 응력 (MPa) · 실험 [45] (회색 네모) · DEM (빨강 원) | 자동 그대로 · 캡션 고침 (본문이 섞였던 것) |
| `fig_4.png` | 건조 3D: (a1–a3) 거시 · (b1–b3) 속도장 (색 막대 0–1 · 단위 없음) · (c1–c3) 접촉망 (AM 접촉 결합 = 굵은 선) · Initial / Interim / End of drying | 자동 그대로 · 캡션 고침 |
| `fig_5.png` | CBD 분포 (3D + 2D 수직 단면) — 건조가 끝나면 위쪽 몰림 | 자동 그대로 |
| `fig_6.png` | 건조 중 배위수 ↔ 무차원 시간 · 단계 I HDR · II LDR · III HDR | 자동 그대로 · 캡션 고침 |
| `fig_7.png` | 압연: (a1–a3) 3D + 앞 단면 (h ≈ 80 · 60 · 40 µm) · (b) 기공 ↔ 무차원 시간 | 자동 그대로 (p.8 부분만) |
| `fig_7c.png` | 압연: (c) 배위수 ↔ 무차원 시간 (p.9 'Fig. 7 (continued)') | **새로 자름** — 옛 크롭에 빠져 있었다 (xref 143) |
| `fig_8.png` | 집전체 접촉 수 막대 897 · 1087 · 2038 (t 0 · 0.5 · 1.0 · 축 이름 오타 'Domensionless') · 삽화 = 집전체 위 contact key | 자동 그대로 · 캡션 고침 (쪽 번호) |
| `fig_9.png` | (a) 평균 응력 σ_xx · σ_yy · σ_zz (MPa) ↔ 무차원 시간 (삽화 t = 0 · 0.5 · 1.0 접촉력 벡터) · (b) 판 · 집전체 힘 (N) (축 이름 'Dimensionles') | 자동 그대로 · 캡션 고침 (쪽 번호) |
| `tab_1.png` | 표 1 입자 입력 (AM · CBD 다섯 줄 · 출처 [45,49,50]) | **다시 자름** — 옛 크롭은 5 쪽 전체였다 |

### 14-2. ★ 보충 영상 S1–S4 (원문 S 번호 = 내용으로 맞춤 · inbox 파일 번호와 거꾸로)
| 원문 | 원문 설명 (쪽) | inbox 파일 | 길이 · 화면 | 정지 화면 (`litdb/figures/<slug>/`) | 보이는 것 [관찰] |
|---|---|---|---|---|---|
| **S1** | *"The animation of 3D structural evolution during drying can be found in video S1 (Supporting information)."* (p.5) | `37bc0003-68-2._Sup4_…mp4` | 15.72 s · 1280 × 720 · 29.97 fps · 471 프레임 · 소리 줄 있음 (안 들음) | `vid_S1_t01s.png` · `vid_S1_t15s.png` | AM (초록) · CBD (빨강) 가 200 µm 상자 전체에 흩어진 슬러리 → 집전체 위에 내려앉은 조밀한 층 · 위 표면에 CBD (그림 4a · 5 와 같음) |
| **S2** | *"The real time change of the contact network can be found in video S2."* (p.5) | `5d959c56-68-2._Sup3_…mp4` | 24.22 s · 726 프레임 | `vid_S2_t01s.png` · `vid_S2_t23s.png` | 흩어진 짧은 결합 → 아래 (집전체) 부터 쌓인 조밀한 접촉망 (그림 4c1 → c3) |
| **S3** | *"The animated evolution of the entire 3D structure during calendering is shown in video S3."* (p.8) | `bdc317ef-68-2._Sup2_…mp4` | 21.76 s · 652 프레임 | `vid_S3_t01s.png` · `vid_S3_t21s.png` | 거친 위 표면 위의 반투명 누름판 → 얇게 눌린 층 (그림 7a1 → a3) |
| **S4** | *"As shown in the insets in Fig. 7c and video S4, the RVE contact network became more complete both before and after calendering"* (p.10) | `77021b35-68-2._Sup1_…mp4` | 23.49 s · 704 프레임 | `vid_S4_t01s.png` · `vid_S4_t22s.png` | 건조 끝의 두꺼운 접촉망 → 얇고 조밀한 접촉망 (그림 7c 삽화) |
- 원문 부록: *"Appendix A. Supplementary material — Supplementary data to this article can be found online at https://doi.org/10.1016/j.ijepes.2025.110521."* (p.11) — 영상 수 · 파일 이름 · 길이는 원문에 없다.  ⚠ **inbox 파일의 Sup 번호는 원문 S 번호와 거꾸로다** (Sup4 = S1 · Sup3 = S2 · Sup2 = S3 · Sup1 = S4 — 정지 화면 4 장씩으로 맞춤 [관찰]) · 정지 화면 = ffmpeg 한 프레임 + 검은 옆 띠만 잘라냄 (`figures.json` movie_frame · movies).  영상 안에 시간 · 압력 · 눈금 글자 없음 → 숫자를 읽을 수 없다.

### 14-3. 판독 원장 (`digitized.csv` 129 행)
그림 3 (DEM 5 · 실험 5 = sangros2019 표 1 과 같은 값으로 판독 재현 확인) · 그림 6 (단계 경계 2 · 상자 윗선 1 · 배위수 19) · 그림 7b (기공 17) · 그림 7c (배위수 20) · 그림 8 (인쇄 막대 3) · 그림 9a (σ_zz 12 · σ_xx 13 · σ_yy 11) · 그림 9b (판 11 · 집전체 10).  방법 = 원 래스터 (PDF 안 이미지 그대로) 에서 축 틀 · 눈금 위치를 화소로 찾아 직선 맞춤 → 색 거르기 (빨강 · 파랑 · 회색 · 검정) 로 곡선 · 표지 중심 · 범례 · 삽화 · 눈금 줄은 빼고 읽음 — 행마다 `note` 에 눈금 화소 · 색 문턱.

### 14-4. 식 · 근거 문단 크롭
- 식 29 장 = `eq_01_translational_motion` … `eq_29_viscous_damping_force` (식 번호마다 한 장 · 400 dpi · 식 번호 포함).
- 근거 문단 20 장 = `txt_p2_intro_lyu22_*` · `txt_p2_intro_refs44_53_*` · `txt_p3_contact_force_*` · `txt_p3_bond_model_*` · `txt_p4_bond_generation_*` · `txt_p4_rve_psd_*` · `txt_p4_fr_not_constant_*` · `txt_p4_boundary_*` · `txt_p5_contact_assignment_*` · `txt_p6_cbd_top_enrichment_*` · `txt_p7_calendering_initial_state_*` · `txt_p8_thickness_*` · `txt_p8_porosity_*` · `txt_p9_cn_36_*` · `txt_p10_cn_max_83_*` (두 단 띠) · `txt_p11_collector_contacts_*` · `txt_p11_stress_*` · `txt_p11_forces_*` · `txt_p11_conclusions_*` · `txt_p12_references_44_57_*` (카드가 숫자 · 정의 · 단정의 근거로 인용한 문장만).

---

## 15. ★ 원문 문장 대조 — DEM 한계 · 소성 · 차원 · 탈압 (정독 질문 k · l 의 근거)

**(i) DEM 한계 — 말 없음.**  이 논문은 DEM 을 쓰면서 그 한계 (구 · 점접촉 · 겹침 상한 · 조밀 영역 강성) 를 말하지 않는다.  가까운 문장:
- *"Both AM and CBD particles are assumed to be spherical for simple."* (p.4) — 구 가정은 이 한 줄.
- *"The focus of this work is on the evolution of the solid components within the electrode. Therefore, direct numerical description of the fluid phase is avoided by utilizing a variety of fluid substitution models, which greatly reduces simulation time and computational cost [28]."* (p.4) — 비용 때문에 유체를 대리.
- *"The selection of an appropriate contact model from numerous available options is of importance in DEM."* (p.3) · *"different contact models must be selected based on the specific physical properties of the particles"* (p.4).
- 다른 DEM 에 대한 비판: *"the above DEM-based drying models rarely explicitly consider the carbon binder domain (CBD) phase"* (p.2) · *"randomly generated DEM models that do not consider the final structure state of drying are inappropriate for calendering simulation analysis"* (p.2) — 출발 상태의 한계 (모델 물리의 한계 아님).

**(ii) 소성 · 큰 변형 — 계산에 없음 · 이유 논의 없음.**  접촉 = 탄성 (인장 없음 · 3/2 승 증분) + 마찰 + 감쇠 (식 3–14) · 결합 = 선형 탄성 + 최대 응력 (식 15–22) — 항복 · 소성 · 입자 형상 변화 항이 없다.  우회 = **무른 상 (CBD · E 0.65 GPa) + 결합** 으로 압밀을 흡수 · 맞춘 값 0 (표 1 = 문헌) · 비용 미기재.  파쇄는 경고뿐: *"it is necessary to ensure that the stress in the direction of the electrode thickness is less than the fracture stress of the particles during calendering"* (p.11) · *"excessive stress can also precipitate particle degradation [49,57]"* (p.11).

**(iii) 차원 — 3D.**  *"Two-dimensional (2D) models are commonly used."* (p.1–2) · *"Compared with 2D models, three-dimensional (3D) models can better characterize the changes in the electrode structure."* (p.2) — 정성 · 2D ↔ 3D 숫자 대조 없음 · 같은 그룹 2D 판 = [22] (제목상 건조 + 압연).

**(iv) 탈압 — 없음.**  판은 내려가기만 한다 (*"moving the pressure plate downward along the z-axis with a constant speed of 0.01 m/s [51]"* p.4) · 그림 7–9 는 무차원 시간 0–1 의 가압 · 되돌아옴 · 판 분리 · 이완 없음.  ⚠ 그런데 검증 그림 3 의 실험 점 [45] 은 **압연 뒤** 값 (sangros2019 카드 표 1) — 상태가 다른 두 값을 같은 압력 칸에 놓았다 [카드 추론].
- 인용 서지: Y. Lyu, S. Dong, L.T. Gao, Z.-S. Guo, *Int. J. Electr. Power Energy Syst.* 165 (2025) 110521.

---

## 16. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 값은 모두 **액체 LIB 양극 (NCM + CBD) · SE 없음** = 랩 표준과 다른 문헌 값.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) 검증 그림 3 이 같은 압력 칸에 **DEM 누른 채** 와 **실험 압연 뒤** (sangros2019 카드 표 1) 를 넣었다 → 우리 등록 칸 = 압력 + 상태 (누른 채 / 뺀 뒤) + 기공 연산자 + 측정 영역 (2) **(1 − P)·h 고체 보존 점검이 9 % 어긋난다** [카드 산술] → 우리 기공 보고에 '(1 − ε)·두께 = 상수' 자기 점검 줄 (3) 식 (24) 배위수 쌍 세기 · 식 (25) V_reg · 식 (26) V 가 원문에 없다 → 결과 전에 정의 등록 (4) '압력' 이 판 힘 ÷ 단면 (121 MPa) 인지 접촉 virial σ_zz (164 MPa) 인지에 따라 1.36 배 [카드 산술] → 우리 wallP (벽 반력) ↔ σ_zz 규약과 같은 질문 | 순수 SE 기공 · 진밀도 없음 |
| **단계 1** (3D 메모리 · 장 수) | 입자 수 AM ≈960–1050 · CBD ≈2.7–3.0 × 10⁴ [카드 산술 · 추정] — 우리 real_14 스캐폴드 (AM 457 · SE 32 832) 와 같은 자릿수 · 단면 200 × 200 µm | 메모리 · 시간 · 장 수 [미확인] · 입자별 장 없음 (DEM) |
| **단계 2 · 3** (2D MPM · 접촉 표현 비교) | 없음 (DEM 만) | — |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 없음 (순수 SE 없음) | — |
| **단계 5** (3D 복합 압밀) | 복합 (단단한 AM + 무른 상) 압밀 DEM 의 곡선 모양: 기공 57.0 → 21.7 % (t 0 → 1) · σ_zz 0 → −164 MPa · 측압 비 σ_xx/σ_zz 0.78 (t 1) [판독 · 카드 산술] · ★ **출발 상태 (건조 끝 · 거친 위 표면) 가 앞 20 % 를 정한다** (t ≤ 0.2 기공 그대로 · 그 사이 배위수 3.6 → 2.3) — 우리 침대의 위 표면 처리 · 판 접촉 시작점을 결과 전에 적어야 하는 근거 | 랩 표준과 다른 문헌 값 (액체 LIB · SE 없음 · ≤ 164 MPa) · 무른 상 = CBD (E 0.65 GPa · 결합) ↔ 우리 SE (DEM E_eff 1.35 GPa · MPM E 1.53 · σ_y 0.30 · ν 0.49) — 역할 · 물리가 다르다 · 강체 AM E 142 GPa ↔ 우리 E_CAM 140 GPa (값만 비슷) |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 탈압 계산 없음 | 되돌아옴 표적 없음 |
| **단계 7** (형상 · 피복 · 수송) | 접촉망 · 집전체 접촉 (897 → 2038 = +127 %) 을 σ_e 의 **정성** 근거로 · 수치 σ 없음 → 우리 Kirchhoff 망 (Holm 협착) 이 같은 종류 구조에서 수치로 채우는 자리 · 배위수 정의 (쌍 세기) 를 맞춘 뒤에 견줌 | 수송 계산 없음 · 액체 전해질 (공극 = 이온 통로) ↔ 우리 SE 망 — 이온 위상 반대 |
| **후보 D0** (지금 DEM) | 같은 부류 (구 · 탄성 접촉 · 결합) 의 독립 사례 — 형상 · 소성 · 파쇄 없음 (frame[5] 의 독립 확인 한 줄 더) · ⚠ 식 (6) · (14) 차원 · 식 (10) (1 − ν)² 인쇄 · 식 (6) 의 [46] 귀속 → 이웃 DEM 의 접촉식을 옮겨 쓸 때 원문 식을 그대로 믿지 않는다 | 연화 · 보정 근거 없음 (표 1 = 문헌 · 맞춘 값 0) |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 벽 둘의 규칙이 다르다: 집전체 = AM 접촉 결합 · CBD 병렬 결합 (점착 벽) · 판 = 결합 언급 없음 · 끝에 집전체 힘이 판 힘보다 ≈15 % 크다 (*"weak local particle stability on the top"* p.11) → 우리 벽 반력은 위 · 아래를 따로 기록 | 판 접촉 규칙 원문 미기재 |
| **후보 A · A′ · B · C · C′** | 없음 — 항복 캡 없음 (C′ 아님) · MPM · 입자별 FE 없음 | — |
| **후보 M0** (균질화 · Heckel · 캡) | p.11 *"the pressure increased exponentially with decreasing porosity [32]"* 언급뿐 | 판독 곡선은 기공에 대해 지수꼴이 아니다 [카드 산술] · Heckel 맞춤 없음 |
| **U0–U6** | 없음 — 건조 침강 (U5 류 다물체 충돌) 은 정성 영상 (S1 · S2) 뿐 · 해상도 · RVE 크기 · 씨앗 시험 없음 | — |
| **R1** (AM 이 움직이고 하중을 나눔) | AM 이 움직이고 AM–AM 접촉 결합으로 하중 경로 · *"the contact force is mainly along the thickness"* (그림 9a 삽화) | AM 하중 몫 숫자 없음 |
| **R2** (미끄럼 · 분리) | 압연 초기 배위수 3.6 → 2.28 (−37 %) · *"the particles that were initially in contact with each other were now separated"* (p.10) | 미끄럼 · 분리 법칙의 숫자 없음 |
| **R3 · R6** (SE 경계 · SE 형상) | 없음 (SE 없음 · 형상 불변) | — |
| **R4** (탈압) | 없음 | — |
| **R5** (맞추는 값 하나) | 맞춘 값 0 (문헌 표 1) — 결합 · 감쇠 값 미기재라 '무엇을 맞췄나' 를 말할 수 없다 | — |
| **R7** (AM 파괴) | 200 MPa 파쇄 경고 [57] (모델 없음) — 정본 stershic2015 카드 기준 명목 압연 압력에서 깨진 입자가 보인 것 | 파쇄 모델 · 문턱 측정 없음 |
| **결과 전 대조 항목** | 그림 3 (DEM ↔ 실험 · **상태 표지 필수**) · 그림 7b · 7c · 9a 곡선 모양 (액체 LIB · 결합 DEM) · 측압 비 0.78 · 판 힘 ÷ 단면 ↔ virial σ_zz 1.36 배 · 출발 상태 효과 (t ≤ 0.2) | 절대값 전이 금지 (재료 · 압력 · 상태 다름) |

- **재료 · 차원 · 조건 차이**: 액체 LIB 양극 NCM (화학식 미기재) + CBD (카본블랙 + PVDF) ↔ 우리 LPSCl SE + NCM811 · 3D = 같음 · 평판 압연 (판 0.01 m/s · 우리의 1000 배) ↔ 단축 냉간 압축 · 끝 σ_zz ≈164 MPa ↔ 우리 300 MPa · 누른 채만 (탈압 없음) · 단분산에 가까운 AM 13 µm (σ 0.61 · 단위 없음) ↔ 우리 이봉 12 : 4 : 1.

---

## 17. [미확인] 목록 (보강 · 2026-11-16 · 원문 12 쪽 + 영상 4 전수)
- 감쇠 β_n · β_s · 점성 계수 α · 용매 밀도 ρ_liquid · 증발 구현 (용매 부피 · 시간) · 건조 · 압연의 실제 시간 · 무차원 시간의 기준.
- k_n · k_s 값 (식 14 의 A · L 을 정한 법) · 결합 강성 k̄_n · k̄_s · k̄_b · 강도 σ̄_c · τ̄_c · 결합 반경 · 결합 생성 시점 (처음만 / 매 걸음).
- 입자 수 (AM · CBD) · 시간 간격 · 계산 시간 · 씨앗 · 반복 수 · RVE 크기 시험.
- 측정 영역 V_reg (식 25) · V (식 26) · 배위수 쌍 세기 (식 24) · 그림 3 DEM 점의 '압력' 이 어느 응력인지.
- 판 쪽 접촉 규칙 (결합 · 마찰) · 판 출발 위치.
- 표준편차 0.61 의 단위 · 평균 13 µm 를 [51] 에서 어떻게 얻었는지 · 모델 NCM 의 조성.
- 그림 7a 중간 상태 (h = 60 µm) 의 시각.
- 영상 S1–S4 의 압력 · 시간 눈금 (영상 안 글자 없음).

---

## 18. 참고문헌 목록 (원문 그대로 · p.11–12 · 57 개)
(텍스트 층에서 옮기고 줄바꿈만 이었다 — 철자 · 학술지 줄임 · 오타 ('threestage' · 'spproach') 는 인쇄 그대로 · 크롭 = `txt_p12_references_44_57_*` ([44]–[57]))

| # | 원문 그대로 |
|---|---|
| 1 | Hawley WB, Li J. Electrode manufacturing for lithium-ion batteries—Analysis of current and next generation processing. J Storage Mater 2019;25:100862. |
| 2 | Li J, Fleetwood J, Hawley WB, Kays W. From materials to cell: State-of-the-art and prospective technologies for lithium-ion battery electrode processing. Chem Rev 2021;122:903–56. |
| 3 | Carpinelli G, Noce C, Russo A, Varilone P, Verde P. Optimal siting and sizing of battery energy storage systems in unbalanced distribution systems: a multi objective problem under uncertainty. Int J Electr Power Energy Syst 2024;162:110316. |
| 4 | Liu Y, Zhang R, Wang J, Wang Y. Current and future lithium-ion battery manufacturing. iScience 2021;24:102332. |
| 5 | Niri MF, Reynolds C, Román Ramírez LAA, Kendrick E, Marco J. Systematic analysis of the impact of slurry coating on manufacture of Li-ion battery electrodes via explainable machine learning. Energy Storage Mater 2022;51:223–38. |
| 6 | Román-Ramírez LA, Apachitei G, Faraji-Niri M, Lain M, Widanage WD, Marco J. Understanding the effect of coating-drying operating variables on electrode physical and electrochemical properties of lithium-ion batteries. J Power Sources 2021;516:230689. |
| 7 | Wood DL, Li J, Daniel C. Prospects for reducing the processing cost of lithium ion batteries. J Power Sources 2015;275:234–42. |
| 8 | Horstig M-Wv, Schoo A, Loellhoeffel T, Mayer JK, Kwade A. A perspective on innovative drying methods for energy-efficient solvent-based production of lithium-ion battery electrodes. Energ Technol 2022;10:2200689. |
| 9 | Zhang YS, Courtier NE, Zhang Z, Liu K, Bailey JJ, Boyce AM, et al. A review of lithium-ion battery electrode drying: Mechanisms and metrology. Adv Energy Mater 2021;12:2102233. |
| 10 | Li B, Song J, Zhou J, Chen J, Li J, Chen J, et al. Optimization of electrode manufacturing processes from the perspective of mechanical properties. J Electrochem Energy Convers Storage 2024;22:1–17. |
| 11 | Rollag K, Juarez-Robles D, Du Z, Wood DL, Mukherjee PP. Drying temperature and capillarity-driven crack formation in aqueous processing of Li-ion battery electrodes. ACS Appl Energy Mater 2019;2:4464–76. |
| 12 | Zhang YS, Bailey JJ, Sun Y, Boyce AM, Dawson W, Reynolds CD, et al. Applications of advanced metrology for understanding the effects of drying temperature in the lithium-ion battery electrode manufacturing process. J Mater Chem A 2022;10:10593–603. |
| 13 | Sahore R, Wood DL, Kukay A, Grady KM, Li J, Belharouak I. Towards understanding of cracking during drying of thick aqueous-processed LiNi0.8Mn0.1Co0.1O2 cathodes. ACS Sustain Chem Eng 2020;8:3162–9. |
| 14 | Klemens J, Schneider L, Herbst EC, Bohn N, Müller M, Bauer W, et al. Drying of NCM cathode electrodes with porous, nanostructured particles versus compact solid particles: Comparative study of binder migration as a function of drying conditions. Energ Technol 2022;10:2100985. |
| 15 | Klemens J, Burger D, Schneider L, Spiegel S, Müller M, Bohn N, et al. Drying of compact and porous NCM cathode electrodes in different multilayer architectures: Influence of layer configuration and drying rate on electrode properties. Energ Technol 2023;11:2300267. |
| 16 | Niesen S, Kappler J, Trück J, Veith L, Weil T, Soczka-Guth T, et al. Influence of the drying temperature on the performance and binder distribution of sulfurized poly (acrylonitrile) cathodes. J Electrochem Soc 2021;168:050510. |
| 17 | Jaiser S, Sanchez Salach N, Baunach M, Scharfer P, Schabel W. Impact of drying conditions and wet film properties on adhesion and film solidification of lithium-ion battery anodes. Drying Technol 2017;35:1807–17. |
| 18 | Jaiser S, Müller M, Baunach M, Bauer W, Scharfer P, Schabel W. Investigation of film solidification and binder migration during drying of Li-ion battery anodes. J Power Sources 2016;318:210–9. |
| 19 | Jaiser S, Friske A, Baunach M, Scharfer P, Schabel W. Development of a threestage drying profile based on characteristic drying stages for lithium-ion battery anodes. Drying Technol 2017;35:1266–75. |
| 20 | Altvater A, Klemens J, Borho J, Smith A, Heckmann T, Scharfer P, et al. Application of multistage drying profiles for accelerated production of Li-ion battery anodes using infrared radiation: validation with electrochemical performance and structural properties. Energ Technol 2024;10:2301272. |
| 21 | Font F, Protas B, Richardson G, Foster JM. Binder migration during drying of lithium-ion battery electrodes: modelling and comparison to experiment. J Power Sources 2018;393:177–85. |
| 22 | Lyu Y, Dong S, Guo ZS. 2D Discrete element simulation of electrode structural evolutions in Li-ion battery during drying and calendering. Energ Technol 2024;12:2400583. |
| 23 | Kumberg J, Baunach M, Eser JC, Altvater A, Scharfer P, Schabel W. Influence of layer thickness on the drying of lithium-ion battery electrodes—simulation and experimental validation. Energ Technol 2021;9:2100013. |
| 24 | Kumberg J, Baunach M, Eser JC, Altvater A, Scharfer P, Schabel W. Investigation of drying curves of lithium-ion battery electrodes with a new gravimetrical double-side batch dryer concept including setup characterization and model simulations. Energ Technol 2020;9:2000889. |
| 25 | Lombardo T, Ngandjong AC, Belhcen A, Franco AA. Carbon-binder migration: a three-dimensional drying model for lithium-ion battery electrodes. Energy Storage Mater 2021;43:337–47. |
| 26 | Yao X, Xiao Y, Wang Z, Zhang Z, Cai W, Zeng Y, et al. Coarse-grained molecular dynamics simulations of microstructure evolution and debonding in water-based cathode electrode drying. J Mater Process Technol 2023;321:118154. |
| 27 | Nikpour M, Barrett N, Hillman Z, Thompson AI, Mazzeo BA, Wheeler DR. A model for investigating sources of Li-ion battery electrode heterogeneity: part I. electrode drying and calendering processes. J Electrochem Soc 2021;168:060547. |
| 28 | Lippke M, Ohnimus T, Heckmann T, Ivanov D, Scharfer P, Schabel W, et al. Simulation of structure formation during drying of lithium-ion battery electrodes using discrete element method. Energ Technol 2022;11:2200724. |
| 29 | Wolf S, Lippke M, Schoo A, Kwade A, Schilde C. A computational fluid dynamics–discrete element method model for physics-based simulation of structure formation during battery electrode drying. Energ Technol 2024;10:2301004. |
| 30 | Chouchane M, Rucci A, Lombardo T, Ngandjong AC, Franco AA. Lithium ion battery electrodes predicted from manufacturing simulations: assessing the impact of the carbon-binder spatial location on the electrochemical performance. J Power Sources 2019;444:227285. |
| 31 | Srivastava I, Bolintineanu DS, Lechman JB, Roberts SA. Controlling binder adhesion to impact electrode mesostructures and transport. ACS Appl Mater Interf 2020;12:34919. |
| 32 | Meyer C, Bockholt H, Haselrieder W, Kwade A. Characterization of the calendering process for compaction of electrodes for lithium-ion batteries. J Mater Process Technol 2017;249:172–8. |
| 33 | Dominguez DZ, Mondal B, Gaberscek M, Morcrette M, Franco AA. Impact of the manufacturing process on graphite blend electrodes with silicon nanoparticles for lithium-ion batteries. J Power Sources 2023;580:233367. |
| 34 | Abdollahifar M, Cavers H, Scheffler S, Diener A, Lippke M, Kwade A. Insights into influencing electrode calendering on the battery performance. Adv Energy Mater 2023;13:2300973. |
| 35 | Primo EN, Chouchane M, Touzin M, Vazquez P, Franco AA. Understanding the calendering processability of Li(Ni0.33Mn0.33Co0.33)O2-based cathodes. J Power Sources 2021;488:229361. |
| 36 | Kang H, Lim C, Li T, Fu Y, Yan B, Houston N, et al. Geometric and electrochemical characteristics of LiNi1/3Mn1/3Co1/3O2 electrode with different calendering conditions. Electrochim Acta 2017;232:431–8. |
| 37 | Li D, Wan H, Liu J, Jiang H, Wang Y, Zhang J, et al. Effects of calendering state on coupled electrochemical-mechanical performance of silicon based composite electrodes. Green Energy Intell Transp 2024;3:231–8. |
| 38 | Westphal BG, Mainusch N, Meyer C, Haselrieder W, Indrikova M, Titscher P, et al. Influence of high intensive dry mixing and calendering on relative electrode resistivity determined via an advanced two point approach. J Storage Mater 2017;11:76–85. |
| 39 | Lu X, Daemi SR, Bertei A, Kok MDR, O’Regan KB, Rasha L, et al. Microstructural evolution of battery electrodes during calendering. Joule 2020;4:2746–68. |
| 40 | Schreiner D, Lindenblatt J, Daub R, Reinhart G. Simulation of the calendering process of NCM-622 cathodes for lithium-ion batteries. Energ Technol 2022;11:2200442. |
| 41 | Lippke M, Meister J, Schilde C, Kwade A. Preheating of lithium-ion battery electrodes as basis for heated calendering—A numerical spproach. Processes 2022;10:1667–79. |
| 42 | Lundkvist A, Larsson P-L, Olsson E. A discrete element analysis of the mechanical behaviour of a lithium-ion battery electrode active layer. Powder Technol 2023;425:118574. |
| 43 | Lundkvist A, Larsson P-L, Iyer AHS, Olsson E. Discrete element modelling of the elastic-plastic and viscoelastic properties of a lithium-ion battery electrode layer. Powder Technol 2024;443:119873. |
| 44 | Giménez CS, Finke B, Nowak C, Schilde C, Kwade A. Structural and mechanical characterization of lithium-ion battery electrodes via DEM simulations. Adv Powder Technol 2018;29:2312–21. |
| 45 | Giménez CS, Finke B, Schilde C, Froböse L, Kwade A. Numerical simulation of the behavior of lithium-ion battery electrodes during the calendaring process via the discrete element method. Powder Technol 2019;349:1–11. |
| 46 | Sonzogni M, Vanson J-M, Reynier Y, Martinet S, Ioannidou K, Radjai F. Discrete modeling of the calendering process for positive electrodes of Li-ion batteries. Powder Technol 2024;442:119891. |
| 47 | Sun W, Huang C. Elucidating the effect of electrode calendering on electrochemical performance using 3D image-based modelling. J Power Sources 2024;611:234774. |
| 48 | Xu J, Hu H, Zhu L, Li X, Xiao L, Jung J-C-Y, et al. Pore-scale modeling and investigation on the effect of calendering on lithium-ion battery cathodes. J Storage Mater 2024;77:109939. |
| 49 | Zhang J, Huang H, Sun J. Investigation on mechanical and microstructural evolution of lithium-ion battery electrode during the calendering process. Powder Technol 2022;409:117828. |
| 50 | Zhang J, Sun J, Huang H, Yuan Z. Influence of calendering process on the structural mechanics and heat transfer characteristics of lithium-ion battery electrodes via DEM simulations. Particuology 2024;85:252–67. |
| 51 | Ge R, Cumming DJ, Smith RM. Discrete element method (DEM) analysis of lithium ion battery electrode structures from X-ray tomography-the effect of calendering conditions. Powder Technol 2022;403:117366. |
| 52 | Ge R, Boyce AM, Shui Zhang Y, Shearing PR, Cumming DJ, Smith RM. Discrete element method and electrochemical modelling of lithium ion cathode structures characterised by X-ray computed tomography. Chem Eng J 2023;465:142749. |
| 53 | Ngandjong AC, Lombardo T, Primo EN, Chouchane M, Shodiev A, Arcelus O, et al. Investigating electrode calendering and its impact on electrochemical performance by means of a new discrete element method model: towards a digital twin of Li-Ion battery manufacturing. J Power Sources 2021;485:229320. |
| 54 | Lischka C, Nirschl H. Calibration of Li-ion cathode materials for discrete element method simulations. Energ Technol 2022;11:2200849. |
| 55 | Becker V, Birkholz O, Gan Y, Kamlah M. Modeling the influence of particle shape on mechanical compression and effective transport properties in granular lithium-ion battery electrodes. Energ Technol 2021;9:2000886. |
| 56 | So M, Inoue G, Hirate R, Nunoshita K, Ishikawa S, Tsuge Y. Effect of mold pressure on compaction and ion conductivity of all-solid-state batteries revealed by the discrete element method. J Power Sources 2021;508:230344. |
| 57 | Stershic AJ, Simunovic S, Nanda J. Modeling the evolution of lithium-ion particle contact distributions using a fabric tensor approach. J Power Sources 2015;297:540–50. |

---

## 🔗 관련 카드 (보강 2026-11-16)
- 이 논문이 인용한 정본 카드: [45] `sangros2019_dem_calendering_lib_electrode` (그림 3 실험 점의 원 출처 — 그 카드 표 1 값과 판독이 같다) · [46] `sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811` (L249 의 한 줄 · 식 (6) 귀속) · [51] `ge2022_xct_initial_structure_dem_calendering_nmc333` (λ 1.67 · 판 0.01 m/s) · [53] `ngandjong2021_dem_calendering_digital_twin` · [56] `so2021_dem_mold_pressure_assb_coldpress` (결합 모델 귀속) · [57] `stershic2015_fabric_tensor_calendering_nmc_xct_dem` (200 MPa) · [28] `lippke2023_dem_drying_structure_formation_lib` (유체 대리 · CBD 2.2 µm) · [32] `meyer2017_calendering_compaction_resistance_line_load_exponential_model` (57 → 약 20 % · 지수) · [39] `lu2020_insitu_nanoct_calendering_microstructural_evolution`.
- 이 논문을 인용한 정본 카드: `lyu2026_two_layer_gradient_electrode_calendering_dem_fem` (같은 그룹 · 그 논문 ref [82] · 다른 해 · 다른 논문 — 표 1 입력이 다르다 (그 카드 L90)).
- 같은 계열 (결합 DEM · 압연): `zhang2026_xct_dem_cathode_calendering_peel_calibration` · `xu2023_dem_bonded_particle_fracture_calendering` · `sangros2020_lib_electrode_dem_mech_elec_ionic` (카드 L13 · L22 의 'Sangrós 2020' — 이 원문의 목록에는 없다).
- 비교 문서: `comparison_vs_ours_DEM.md` A 절 · D 절 (2026-11-16 보강 줄).

---

## 보강 기록 (2026-11-16 작업 · 1저자 2026-11-12 요청 · 68-2 번 파일)
| 항목 | 내용 |
|---|---|
| 요청 | 1저자 11-12 *"먹여준 위 두 논문도 논문에이전트 부탁"* — 기존 카드 보강 (새 카드 아님) · 정독 출력 NN 124 |
| 쓴 원문 | PDF `e896e74a-68-2._Three-dimensional_discrete_element_simulation_of_electrode_structural_evolution_in_lithium-ion_batteries_during_drying_and_calendering.pdf` (12 쪽) + 보충 영상 4 (`77021b35-68-2._Sup1_…mp4` · `bdc317ef-68-2._Sup2_…` · `5d959c56-68-2._Sup3_…` · `37bc0003-68-2._Sup4_…`) — 메타 줄의 옛 PDF 이름 (`Lyu_2025_IJEPES_…pdf`) · 옛 그림 출처 (`DEM 논문/28. …pdf`) 는 그대로 둠 |
| 서지 대조 | 저자 넷 (Yuhang Lyu · Shaohai Dong · Li Ting Gao · Zhan-Sheng Guo*) · 제목 · *International Journal of Electrical Power and Energy Systems* 165 (2025) 110521 · DOI = 원문 p.1 · PDF 메타와 같다 · 접수 2024-12-13 · 개정 2025-01-17 · 승인 2025-02-05 · 온라인 2025-02-09 · CC BY 4.0 · 연구비 NSFC 12172206 · 11972218 · 자료 *"available on request"* (p.11) — 다른 점 없음 |
| 대조한 범위 | §1 · §2 · §3 (표 24 줄 전부) · §4 (방법 전부) · §5 (그림 표 9 줄) · §6 · §7 표의 이 논문 칸 · §8–§10 의 수치 · 참고문헌 귀속 — 원문 12 쪽 텍스트 층 + 렌더 (식 · 그림 · 표) · 그림 원 래스터 판독 · 영상 4 정지 화면 |
| 고친 것 (정정 표지 21) | 'NCM811' → 원문 'NCM' (L13 · L20 · L38 · L117 · L121 · L236 · L246) · '+230 %' → +127 % (L13 · L32 · L93 · L236) · 서론 계보 (L22 Xu [48] · Zhang [49,50] · Lyu [22]) · L29 중간 두께의 시각 · L43 '실측' · L56 식 (8)–(9) (δ̇ · k_s) · L57 식 (10) 인쇄 꼴 · 우리 쪽 출처 (L120 · L163 Minnmann = CL-94 · L213 Cronau = CL-91 · SELF-51) |
| 더한 것 (보강 표지 33) | 판독 값 (그림 3 · 6 · 7b · 7c · 9a · 9b) · 원문 문장 · 정본 카드 대조 (sangros2019 · ge2022 · meyer2017 · stershic2015 · sonzogni2024 · lippke2023) · 차원 · 단위 · 고체 보존 점검 · [미확인] · 머리 L6 안내 한 줄 (빈 줄 자리 — 줄 번호 그대로) |
| 새 절 | §11 보강 의도 대조 (22 행) · §12 핵심 수치 원문 대조판 · §13 방법 (식 1–29) · §14 그림 · 표 · 영상 · 판독 · §15 원문 문장 · §16 ★ 자세한 분석 · §17 [미확인] · §18 참고문헌 57 · 🔗 관련 카드 · 이 기록 |
| 크롭 | **10 → 68 장** — 다시 자름 2 (`fig_1` 본문 식 (17) 섞임 · `tab_1` 쪽 전체) · 새 그림 1 (`fig_7c` = p.9 'Fig. 7 (continued)' 빠져 있던 것) · 식 29 (`eq_01`–`eq_29`) · 근거 문단 20 (`txt_*`) · 영상 정지 8 (`vid_S1`–`vid_S4` 두 장씩) · 캡션 고침 6 (f1 · f3 · f4 · f6 · f8 · f9 — 옛 문자열 = `caption_original_auto`) · 자동 크롭 8 장 그대로 (전부 열어 봄) · `--clean` 쓰지 않음 · 옛 폴더 백업 = 작업 scratchpad · `digitized.csv` 129 행 새로 · `figures.json` movies 4 · key_note |
| 줄 수 | 252 → 576 (옛 줄 지운 것 0) |
| 정독 출력 | `litdb/_curation/reading/batch_124.tsv` · `batch_124_findings.md` |
| 원문 자체 문제 (판정 안 함 · 카드 문제 아님) | [25]–[27] 이름 ↔ 번호 · [26] 수계 ↔ NMP · [46] 식 (6) 귀속 · [56] · [57] · [32] 의 성격 (각 정본 카드 기준) · [48] 서론 ↔ p.10 방향 · 'an increase of approximately 230 %' · 본문 'Fig. 8a' (= 9a) · 축 이름 'Domensionless' · 'Dimensionles' · 식 (10) (1 − ν)² · 식 (6) ↔ (14) 차원 · 그림 6 끝 3.45 ↔ 본문 3.6 · 그림 7c 끝 8.10 ↔ 본문 8.3 · (1 − P)·h 9 % · 영상 파일 번호 ↔ 원문 S 번호 거꾸로 (inbox 이름) |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

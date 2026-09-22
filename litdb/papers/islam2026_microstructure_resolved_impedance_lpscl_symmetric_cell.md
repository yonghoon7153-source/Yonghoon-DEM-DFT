# Microstructure-Resolved Impedance Modeling of Solid-State Batteries — Li/Li₆PS₅Cl/Li 대칭셀의 phase-field 소결·SEI 미세구조를 COMSOL 옴익-전도 + Butler–Volmer + C_dl 임피던스 모델로 — Islam, Katsube, Ji (Ohio State Univ., 2026 manuscript)

> slug `islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell` · DOI `n/a (manuscript — 저널·DOI 미확인; Word→PDF 2026-09-14 생성본, 16 pp, refs 16)` · type `FEM (COMSOL Multiphysics 2D 옴익 전도 + Butler-Volmer + C_dl, 1 mHz–1 MHz 임피던스) + phase-field 소결/입성장 미세구조 생성 + AI 픽셀 분할(SEM→phase map)` · PDF `79b422f7-5._Microstructure-Resolved_Impedance_Modeling_of_Solid-State_Batteries.pdf` · digested `2026-09-22` · status ✅ · 태그 **[외부 · 우리 SE 그 자체(Li₆PS₅Cl) · Li 대칭셀 = 복합양극 없음 · 시뮬 전용(실험 검증 0)]**
>
> 저자 = **Kaniza Islam** (a), **Noriko Katsube** (a), **Yanzhou Ji**\* (b, ji.730@osu.edu) — a) Dept. Mechanical & Aerospace Engineering, b) Dept. Materials Science Engineering, **The Ohio State University**, Columbus OH.
> 서지 지위: 표지에 저널·접수일·DOI 가 **없다** (Acrobat PDFMaker from Word, 2026-09-14). 인용은 *"Islam, Katsube, Ji, manuscript (2026)"* 로만. 게재본에서 수치가 바뀔 수 있다.
> 그림: `litdb/figures/islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell/` (Fig 1–9, pypdf 임베디드 이미지 조립 — PyMuPDF 크로핑 아님). Table 1·2 는 아래 §4 에 전사.
>
> elements: Cl Li P S

## 1. 한 줄 요약
**우리 SE(Li₆PS₅Cl) 층 자체의 미세구조 — 기공·입계(GB)·SEI 상 — 를 2D phase map 으로 풀어 COMSOL 에서 EIS 를 "계산"** 한 논문. 결론 셋: ① 소결 시 **기공률↑ → 임피던스↑, 입자 간 접촉(neck)↑ → 임피던스↓**; ② **GB 만으로는(σ_GB = 0.01 σ_bulk 여도) 임피던스가 거의 안 변한다** — 대신 **SEI 부피분율·상별 σ** 가 지배; ③ 다상 SEI(Li₂S+Li₃P+LiCl)는 옴 오프셋을 **22–32 → 586–599 Ω cm²** 로 키운다 (단 SEI 두께는 *일부러 과장*). 실험 EIS 대조는 **없다**. 우리에게는 **"복셀/연속체 σ 에 계면·입계 저항을 어떻게 넣는가"(CL-81) 의 직접 선례**이자, **그 선례가 표현 규약에 얼마나 취약한지**를 보여 주는 반면교사다 (§10).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/전극) | 연구유형 |
|---|---|---|---|---|
| K. Islam, N. Katsube, Y. Ji\* (Ohio State Univ.) | manuscript 2026 (저널 미기재) | n/a | **Li₆PS₅Cl** 700 µm + **Li 금속 50 µm ×2** (대칭셀); SEI = Li₂S / Li₃P / LiCl | 시뮬레이션 전용: phase-field (미세구조) → COMSOL (임피던스). 실험 EIS 0 건 |

## 3. 핵심 수치
| 물성 / 관측 | 값 | 조건 | stated / digitized / derived | 비고 |
|---|---|---|---|---|
| σ_Li⁺(Li₆PS₅Cl) 입력 | **0.319 S/m = 3.19 mS/cm** | 298 K, ref [11] Zhao 2022 (second sintering) | stated (Table 2) | ★ 우리 σ_grain **3.0** (Cronau 단결정) 과 같은 급 — 펠릿 1.02 (Bazzoun) · 1.6 (Kim 2025/Minnmann) 보다 높다 |
| i₀ (Li/SE) | **4.97 mA/cm²** | "Exp" (출처 미기재) | stated | BV 선형화 → R_ct = RT/(F i₀) = **5.17 Ω cm²/계면** (derived) |
| C_dl (Li/SE) | **0.22 F/m² = 22 µF/cm²** | ref [7] Li 2025 J. Energy Chem. | stated | 우리 `eis_drt_ica.py` ASSUMED 10 µF/cm² 의 **앵커 후보** (Li\|SE 계면임에 주의) |
| σ_e(Li) / σ_pore | 1.08×10⁷ S/m / 0 | | stated | |
| σ_Li⁺ SEI 상 | Li₂S **0.001** · Li₃P **0.01** · LiCl **3.54×10⁻⁴ S/m** | refs [13],[14] | stated | Li₃P 가 가장 좋은 Li⁺ 도체 (본문 서술과 일치) |
| 섭동 / 주파수 | 10 mV / 1 mHz–1 MHz; α = 0.5 | | stated | |
| 기하 | SE 700 µm, Li 50 µm; phase-field 도메인 700×350 µm (200×100 격자, **dx 3.75 µm**), 초기 원형 입자 **평균 반경 60 µm**, 방위 10 종 | | stated | ⚠ 실 LPSCl 분말(D50 ≈ 1.5 µm)보다 **40 배 큰 입자** — 스케일 카툰 (§10) |
| Nyquist — 단결정 SE | **22.0 → 31.2 Ω cm²** (호 폭 9.2) | Fig 2c·5c | digitized | R_bulk = L/σ = 0.07 cm / 3.19e-3 = **21.9** ✓ (derived) ; 2·R_ct = **10.3** vs 호 폭 9.2 (−10 %) |
| Nyquist — ~12 % / ~20 % 기공 (step 1000) | 32.5→44.1 / **38.0→49.3** | Fig 2c | digitized | 고주파 절편 +48 % / +73 % ; Bruggeman (1−ε)^1.5 예측 26.5 / 30.6 보다 **1.23× / 1.24× 더 크다** (derived) |
| 소결 진행 (~20 %) 고주파 절편 | step 500 **40.0** → 1000 **38.0** → 10,000 **34.5** → 20,000 **34.5** | Fig 3d | digitized | 기공률은 0.20 → 0.22 로 **늘었는데** R 은 −14 % ⇒ neck(접촉) 성장이 지배 |
| 기공률 / GB 분율 vs step | 기공 19.5 % (step 1) → ≈22 % (5k–10k) 정체 ; GB 0 → 피크 ≈4 % (2k–10k) → **2.5–3 %** (20k) | Fig 3e,f | stated(본문) + digitized | GB 분율은 **약 12,000 step 에서 계단식 급락** (0.037 → 0.023, digitized) |
| GB-only (σ_GB = 0.01 σ) vs 단결정 | **구별 불가** (둘 다 22.0→31.2) | Fig 5c | stated + digitized | ⚠ §10 — GB 표현 규약의 산물일 가능성 (derived 산술: 연속 GB 막이면 ~66 Ω cm² 가 나와야) |
| Li₂S 부피분율 8.8 / 8.0 / 7.6 % | 29.7→41.5 / 27.0→37.5 / 26.3→36.7 | Fig 6d | digitized | 단조: 부피분율 +1.2 %p 에 고주파 절편 +3.4 Ω cm² |
| SEI 상별 σ (8.8 %) | Li₃P 28.0→38.5 · Li₂S 29.7→41.5 · LiCl 29.8→42.0 | Fig 7b | digitized | σ 순서(Li₃P > Li₂S > LiCl) 그대로 호 크기 역순 |
| 다상 SEI (Li₂S+Li₃P+LiCl + 입자/GB) | **586.5 → 599.0 Ω cm²** (호 폭 12.5) | Fig 8b; 본문 "≈586–599" | stated + digitized | 옴 오프셋 +564 Ω cm² ≈ **Li₂S 56 µm / LiCl 20 µm 상당** (derived) — 저자 스스로 "두께 과장" 명시 |
| 실 SEM(LG-LPSCl, ref [16]) → AI 분할 → 임피던스 | **44.3 → 66.2 Ω cm²** (호 폭 21.9) | Fig 9c | digitized | 호 폭이 이상값(10.3)의 2.1 배 ⇒ 계면 유효 접촉분율 ≈ 0.47 로 읽힘 (derived, 해석은 우리 것) |

## 4. 시뮬레이션 방법 ★
### 4-1. 임피던스 모델 (COMSOL Multiphysics, 2D)
- **지배식**: SE 도메인 옴 법칙 `i = −σ∇φ`, `∇·i = 0` (eq 1–2). σ 는 **상별**(grain / GB / pore / SEI 각각) 로 배정. SE 는 **단일이온 도체**(counter-ion 격자 고정) — 농도분극·확산·역학 **없음** ("microstructure-resolved Ohmic conduction model").
- **Li/SE 계면**: Butler–Volmer `i_local = i₀[exp(αFη/RT) − exp(−(1−α)Fη/RT)]`, α = 0.5, η = φ_Li − φ_SE − E_eq (eq 3–4); **이중층** `i_Cdl = C_dl ∂η/∂t`, `i_total = Σ i_local + i_Cdl` (eq 5).
- **EIS 추출**: 왼쪽 경계 접지, 오른쪽 경계에 10 mV 정현 섭동, 상·하 절연. `Z(ω) = φ/i_total` (eq 6), 1 mHz–1 MHz. 면적-비 임피던스 (Ω cm²).
- **셀**: Li 50 µm | LPSCl 700 µm | Li 50 µm (Fig 1). ⚠ 700 µm = 펠릿급 두께 — 시트형 SE(<50 µm) 가 아니다.

| Table 2 (재료 파라미터) | 값 | 출처 |
|---|---|---|
| T | 298 K | |
| i₀ | 4.97 mA/cm² | "Exp" |
| σ_Li⁺ SE (Li₆PS₅Cl) | 0.319 S/m | [11] |
| σ_e Li 금속 | 1.08×10⁷ S/m | [12] |
| σ_Li⁺ Li₂S / Li₃P / LiCl | 0.001 / 0.01 / 3.54×10⁻⁴ S/m | [13] / [13] / [14] |
| σ pore | 0 | |
| C_dl | 0.22 F/m² | [7] |
| φ 섭동 | 10 mV | Exp |
| L_SE / L_Li | 700 / 50 µm | |

### 4-2. 미세구조 생성 (phase-field)
- **소결 모델** (Wang 2006 [9]): 보존 order parameter ρ (0 = pore, 1 = solid) + 비보존 {η_i} (입자 방위 10 종). 자유에너지 eq 7–8 (`f = Aρ²(1−ρ)² + B[ρ² + 6(1−ρ)Ση_i² − 4(2−ρ)Ση_i³ + 3(Ση_i²)²]`, 구배항 ½κ_ρ|∇ρ|² + Σ½κ_η|∇η_i|²), Cahn–Hilliard(ρ) + Allen–Cahn(η) 진화 (eq 9). 이동도 `M = M_s h(ρ) + M_p[1−h(ρ)] + M_surf ρ²(1−ρ)² + M_gb Σ η_i²η_j²` (eq 10), h(ρ) = 6ρ⁵−15ρ⁴+10ρ³. **어드벡션(강체 병진) 무시**.
- **수치**: 2D **200×100**, dx = 3.75 µm, Fourier 스펙트럴 반음해법 (Chen & Shen 1998 [10]). 초기: 반경 ~60 µm 원형 입자 랜덤 배치, 입자 수로 목표 기공률 조정.

| Table 1 (phase-field 무차원 파라미터) | A 16 · B 1 · κ_ρ 4 · κ_η 4 · M_s 0.01 · M_p 0.001 · M_surf 1 · M_gb 0.1 · L 10 |
|---|---|

- **SEI 미세구조**: ρ ≡ 1 로 두고 η₁–η₃ 를 세 SEI 상, η₄–η₁₀ 을 LPSCl 입자로 배정 → 소결 모델이 **입성장 모델**로 환원. 왼쪽 150 µm 영역에 작은 SEI 입자, 오른쪽에 큰 SE 입자, 나머지는 "가상 액상"(η 전부 0) → 액상이 없어질 때까지 진행. ⇒ **SEI 존 ≈ 150 µm** (실 SEI nm–sub-µm; 저자 명시 "exaggerated").
- **입자 처리 ★** (우리 "무질서/입자 처리" 축): **입자가 없다** — 전부 **연속체 phase map**. 형상은 phase-field 가 진화시키므로 "형상 소성" 이 아니라 **확산 소결(표면·GB 확산)** 이 형상을 바꾼다. 강체구도, 접촉 소성도, 하중도 없다. 우리 DEM(강체구+접촉) / MPM(J2 소성유동) 어느 쪽과도 **역학 층위가 다르다** (압력 축 자체가 없음).
- **도메인/RVE**: 700×350 µm 단면 1 개, 실현 1 개 (통계·시드 0). 3D 없음.

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | 셀 기하 (Li 50 \| SE 700 \| Li 50 µm), BC (접지/섭동/절연), 계면 BV+C_dl | 우리 STEP3 복셀 FV 의 Dirichlet 세팅과 동형 — 단 **계면 BV+C_dl 이 있다**(우리 STEP3 σ 솔브에는 없음; STEP4 에만 BV) |
| 2 | ~12 % / ~20 % 초기 기공률 미세구조의 초기·최종(step 1000) + Nyquist (단결정 22.0→31.2 / 12 % 32.5→44.1 / 20 % 38.0→49.3) | **기공률 → 옴 저항** 의 연속체 판; Bruggeman 초과분 1.23× = 기공 형상 효과 (우리 τ_Laplace 대응) |
| 3 | ~20 % 시료의 step 1/500/1000/10k/20k: (a) 미세구조 (b) 0/1 기공맵 (c) 0/1 GB맵 (d) Nyquist (e) 기공분율(step) (f) GB분율(step) | ★ **기공률 일정한데 R 이 14 % 준다** = neck 성장 = 우리 Holm 협착 `1/(2σa)` 의 연속체 관측. GB맵(c)이 **불연속 선분**인 점 = §10 의 근거 |
| 4 | 입자+GB+SEI 층 미세구조 (SEI 존이 Li 쪽 ~150 µm) | SEI 를 "상" 으로 넣는 표현 규약 |
| 5 | (a) 단결정 (b) GB 망(σ_GB = 0.01σ) (c) Nyquist 겹침 | "GB 무영향" 의 원 그림 — Kim 2025 (우리 랩 EIS, R_gb ≥ R_bulk) 와 **정면 충돌** → §7·§10 |
| 6 | Li₂S 8.8/8.0/7.6 vol% 미세구조 + Nyquist | SEI 부피분율 민감도 (단조) |
| 7 | 8.8 % SEI 존에 LiCl/Li₃P/Li₂S 각각의 σ 배정 → Nyquist | 상별 σ 민감도; Li₃P 최소 호 |
| 8 | 다상 SEI(파랑 LiCl·초록 Li₂S·주황 Li₃P) + Nyquist 586.5→599.0 | 옴 오프셋이 지배 (호 폭은 12.5 로 거의 그대로) |
| 9 | 문헌 SEM(LG-LPSCl, Singh 2022 [16]) → ChatGPT 픽셀 분류 phase map → Nyquist 44.3→66.2 | 실 미세구조 → 임피던스 파이프라인의 존재증명; 호 폭 2 배 = 계면 접촉 손실 신호 (우리 해석) |

## 6. Post-processing ★
- **무엇**: (i) phase map 의 0/1 임계화로 **기공분율·GB분율(step)** 정량 (Fig 3e,f); (ii) COMSOL 주파수 스윕 → Nyquist; 고주파 절편 = bulk SE 저항, 저주파−고주파 = 두 Li/SE 계면 분극저항 합 (본문 해석); (iii) 실 SEM → **AI(ChatGPT) 픽셀 분류** → grain/GB/pore 이산화 → 솔버 입력.
- **도구**: COMSOL Multiphysics(임피던스), 자체 Fourier-spectral phase-field 코드, ChatGPT(분할).
- **수치화**: 등가회로 피팅·DRT 는 **하지 않는다** — Nyquist 를 눈으로 읽는다. 오차·시드·수렴 보고 0.
- **우리가 한 검산 (derived, 이 카드 고유)**:
  - R_bulk = L/σ = 21.9 Ω cm² = 단결정 고주파 절편 22.0 ✓ ; R_ct(선형 BV, α_a+α_c = 1) = RT/(F i₀) = 5.17 Ω cm² × 2 계면 = 10.3 vs 호 폭 9.2 (−10 %, 디지타이즈 오차 범위) ✓ → **표 2 와 그림이 자기일관**.
  - 이중층 특성주파수 f = 1/(2π R_ct C_dl) = 1/(2π·5.17·22×10⁻⁶) ≈ **1.4 kHz** (그들이 안 적은 값).
  - 기공: 겉보기 굴곡인자 R_HF(1−ε)/R_bulk = **1.30 (12 %) / 1.39 (20 %)** ; 호 폭 증가(9.2 → 11.6/11.3)를 계면 접촉분율로 읽으면 **≈0.79 / 0.81** — 기공이 Li/SE 계면까지 닿아 유효 접촉면적을 깎는다는 뜻 (논문에 없는 해석, TREND 만).
  - GB: GB 분율 3 % 가 **전류를 가로막는 연속 막**이었다면 직렬 ASR ≈ f_GB·L/σ_GB = 0.03×0.07 cm/(3.19×10⁻⁵ S/cm) ≈ **66 Ω cm²** 가 나와야 하는데 관측 Δ < 0.5 Ω cm² ⇒ Fig 3c/5b 의 GB "상" 은 **닫힌 망이 아니라 끊긴 선분**(임계화 산물)이고 전류가 우회한다. "GB minor" 는 **표현 규약의 결론**이다 (§10).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 이산화 | 2D 연속체 phase map (grain/GB/pore/SEI 상별 σ), COMSOL FV/FE | DEM 접촉망(Kirchhoff + Holm `R = 1/(2σa)`, `scripts/network_conductivity.py`) **+** MPM 복셀 FV (`voxel_conductivity.py`/`step3_sigma.py`) | 그들 = 우리 **복셀 FV 쪽**과 동형. 접촉 단위 협착항은 양쪽 다 없음 |
| 계면(입계) 저항 표현 | **GB 를 두께 ~dx(3.75 µm) 의 "상"** 으로 해상, σ_GB = 0.01 σ | 접촉망: Holm 협착 직렬 (있음). 복셀 STEP3: **SE–SE 면 harmonic mean = 계면항 0** (`CONTACT_FREE` 가지, CL-81 `docs/voxel_contact_free_gap.md`) | ★ 그들의 "GB 상" = CL-81 이 말한 **빠진 항을 넣는 한 방법** — 그러나 §6 산술대로 **임계화된 2D GB 상은 항을 넣고도 효과 0** 을 냈다 ⇒ **면(face) 기반 계면 컨덕턴스**(Holm 형) 가 해상-상보다 강건하다는 근거 |
| GB 의 크기 | "minor" (Δ ≈ 0) | Kim 2025 (우리 랩 EIS-TLM): **R_i,gb 25.6 vs R_i,bulk 9.3 Ω cm² (62 wt%)** — GB ≥ bulk ; Cronau(r_SE) σ_grain 인자 | **정면 충돌**. 실험(Kim 2025) 이 이긴다 — 그들 결론은 시뮬 표현의 산물이지 재료 성질이 아니다 |
| σ_SE 입력 | 3.19 mS/cm (Zhao 2022, 2차 소결) | σ_grain 3.0 (Cronau 단결정) × Cronau(r_SE); 펠릿 앵커 1.02 (Bazzoun) / 1.6 (Kim·Minnmann) | 그들 값 = **단결정급**. 700 µm 펠릿에 단결정 σ 를 넣었으므로 그들 R_bulk 22 Ω cm² 는 **하한** (GB 포함 펠릿이면 ~2–3 배) |
| 기공→σ | 12/20 % 기공에 R +48/+73 %, Bruggeman 초과 1.23× | 우리 σ_ionic 폼 `(φ_eff)^½·CN²·cov^½·f_p³·C(τ)`; MPM STEP3 는 solved 경로 | 방향 일치(기공↑ σ↓). 크기 전이 금지 (2D·스케일 카툰) |
| 접촉/neck 성장 | 기공률 일정에 R −14 % (neck) | Holm 협착 `a` 가 커지면 R_constr↓ — 우리 접촉망의 핵심 물리; Stage-E 소성면적 | 같은 물리의 연속체 관측 = **frame[4] 방향 교차검증** (값 아님) |
| 계면 kinetics | BV(i₀ 4.97 mA/cm²) + C_dl 22 µF/cm² **Li\|SE** | STEP4 BV 는 **NCM\|SE** 만, Li 쪽 과전압 범위 밖; `eis_drt_ica.py` C_dl ASSUMED 10 µF/cm² | 그들 값은 우리가 비워 둔 **Li-anode 쪽 칸**의 후보 (출처 2차 → 앵커 후보) |
| SEI | Li₂S/Li₃P/LiCl σ 상별, 부피분율 스윕 | 없음 (STEP3/4 에 SEI 상 없음; SE-축 카드 `kim2026_li_argyrodite_sei_reactive_md` 가 Li\|LPSCl SEI MD) | 우리가 못 하는 축 → §F |
| 실험 검증 | **0** (문헌 SEM 1 장을 입력으로만) | σ_ionic 외부 앵커: Bazzoun EIS 0.137/0.101/0.065 · Kim 2025 TLM | 그들 쪽이 비어 있다 |
| 역학 | 없음 (압력·응력·형상소성 0) | DEM 압밀 + MPM J2 소성 | 축 자체가 다르다 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **CL-81 처방의 반례 확보**: "계면을 해상된 얇은 상으로 넣는다" 는 방식은 (a) 격자가 GB 두께(nm) 를 못 풀고 (b) 임계화가 망을 끊으면 **항을 넣고도 0** 이 된다. STEP3 에 계면 저항을 넣으려면 **SE–SE 면(face)마다 컨덕턴스 g_face = 2σa 형**으로 넣는 쪽(우리 접촉망과 같은 층위)이 격자 독립적이다. 이 카드가 그 선택의 문헌 근거.
- ② **Li-anode 쪽 BV 파라미터 후보**: i₀(Li\|LPSCl) 4.97 mA/cm² → R_ct 5.2 Ω cm²/계면 @25 °C, C_dl 22 µF/cm². STEP4 half-cell 이 "Li counter 과전압 범위 밖" 으로 둔 칸. `docs/data/rint_eis_anchors.csv` 에 **`source = islam2026 manuscript (i0 "Exp" 출처 미기재; C_dl = ref [7] 2차)`** 로 등재 가능 — pdf_verified 등급은 아니다.
- ③ **소결 neck 성장 = 협착 저항 감소** 의 연속체 그림(Fig 3d) 은 우리 Holm 협착·Stage-E 논리를 발표에서 설명할 때 쓸 수 있는 **직관 그림** (값 인용 없이).
- ④ **기공이 계면 접촉면적을 깎는다** (호 폭 +26 %) — 우리 coverage(Hertz/Tabor) ↔ R_ct 연결(`eis_drt_ica.py` 의 R_ct = RT/(F i₀ a_spec)) 의 연속체 대응. a_spec 이 기공에 의해 줄면 R_ct 가 오른다는 우리 배선과 같은 방향.

## 9. 인용 가능 문장 (deck/paper용)
- "A microstructure-resolved Ohmic impedance model of a Li/Li₆PS₅Cl/Li cell (Islam et al., manuscript 2026) shows that, at constant porosity, neck growth during sintering lowers the high-frequency intercept by ~14 %, i.e. inter-particle constriction — the quantity our Holm term `R = 1/(2σa)` carries per contact — controls the bulk resistance even in a continuum description."
- "The same model finds a resolved grain-boundary phase with σ_GB = 0.01 σ_bulk to be impedance-neutral; since a connected GB film of that fraction would add ~66 Ω cm² (our estimate), the result reflects the discontinuity of the thresholded 2D GB map rather than a material property — consistent with lab EIS (Kim et al. 2025) where R_gb ≥ R_bulk."

## 10. 주의/한계 (over-claim 방지)
- **실험 검증 0**. 모든 수치는 시뮬 출력. i₀ "Exp" 의 출처·조건 미기재.
- **2D, 실현 1 개, 시드 0, 격자수렴 0** — 통계적 주장 불가.
- **스케일 카툰**: 입자 반경 60 µm · dx 3.75 µm · SE 700 µm. 실 LPSCl D50 ≈ 1.5 µm (Bazzoun) 보다 **40 배** 크고, GB "두께" 가 격자 1–2 칸(≥ 3.75 µm) = 실 GB(nm) 의 10³ 배. 옴 모델은 L 에 대한 비율만 보므로 *상대* 추세는 살지만, **GB 비저항×두께(면비저항) 는 물리적으로 정의되지 않은 채** 들어갔다.
- **"GB minor" 인용 금지** — §6 산술 + Fig 3c 의 끊긴 GB 선분이 근거. 우리 Cronau(r_SE) GB 인자·Kim 2025 의 R_gb 와 충돌하며, 실험 쪽이 정본.
- **SEI 두께 과장(저자 명시)** → 586–599 Ω cm² 는 시연값. Li₂S/Li₃P/LiCl σ 는 2차 문헌값 [13][14].
- **Li 대칭셀** — 복합양극(AM·탄소·바인더) 없음. 우리 양극 σ_ionic/σ_e/σ_thermal 축과는 **SE 층 안쪽**만 겹친다.
- **AI 픽셀 분할(ChatGPT)** 은 재현·검증 불가 — 방법 선례로만.
- 본문 Fig 9 캡션이 SEM 출처를 "[10]" 으로 적었으나 본문·참고문헌상 **[16] Singh 2022** 가 맞다 (오기).

## 우리 DEM+MPM 프레임 대비 · 적용 후보
| # | 리포 훅 | 이 논문이 주는 것 | 라벨 |
|---|---|---|---|
| ① | `scripts/network_conductivity.py` — 접촉망 Kirchhoff + Holm `R = 1/(2σa)` (FULL / CONTACT_FREE / CONSTRICTION_ONLY 가지) | 그들 모델은 **CONTACT_FREE 가지의 연속체판**(계면항 0) 에 "GB 상" 을 얹은 것. neck 성장 → R −14 % (Fig 3d) 는 협착항의 연속체 관측 | 적용 후보 (방향 교차검증; 값 전이 금지) |
| ② | **CL-81** `docs/voxel_contact_free_gap.md` — 복셀 STEP3 σ 는 CONTACT_FREE, SE–SE 면 harmonic mean = 계면항 0 | 계면/입계를 **해상된 상**으로 넣는 처방의 실패 사례(임계화 → 망 단절 → 효과 0). ⇒ **면 기반 컨덕턴스(g_face = 2σa 형)** 가 강건. 격자(0.4→0.15 µm)에서 nm GB 를 상으로 풀 수 없다는 우리 서술의 외부 근거 | 적용 후보 (STEP3 계면항 설계 근거) |
| ③ | `scripts/eis_drt_ica.py` (Randles R0 + R_ct∥C_dl + Wo, Tikhonov DRT) · `docs/project_rint_fullcell_cycling.md` · `docs/data/rint_eis_anchors.csv` | Li\|LPSCl **i₀ 4.97 mA/cm² → R_ct 5.17 Ω cm²/계면**, **C_dl 22 µF/cm²**, f_ct ≈ 1.4 kHz (derived). 우리 C_dl ASSUMED 10 µF/cm² 는 NCM\|SE 계면용 — 계면이 다르므로 대체가 아니라 **Li-쪽 칸 후보** | 앵커 후보 (출처 2차 · pdf_verified 아님) |
| ④ | `scripts/step4_dyn.py` (voxel-DFN, NCM\|SE BV, half-cell vs Li) | Li counter 과전압을 넣을 때 필요한 (i₀, C_dl)_Li\|SE 한 쌍. 또 "기공이 계면 접촉분율을 깎아 호 폭 +26 %" 는 STEP4 의 a_spec(반응면) 감소 논리와 같은 방향 | 적용 후보 |
| ⑤ | 재료 정합 — LPSCl σ_grain 3.0 (Cronau) · 펠릿 1.02 (Bazzoun) · 1.6 (Kim 2025/Minnmann) | 그들 3.19 mS/cm 는 **단결정급 상단** 값 (Zhao 2022 2차 소결). 700 µm 펠릿 + 단결정 σ = R_bulk 하한. GB 인자는 우리 Cronau(r_SE) 유지 | 해당 없음(값 전이 금지) — 정합 확인만 |
| ⑥ | SE-축 SEI 원장 (comparison_vs_ours.md 축 E, `kim2026_li_argyrodite_sei_reactive_md`) | Li₂S 1e-3 / Li₃P 1e-2 / LiCl 3.54e-4 S/m (2차 인용값) 와 "부피분율 +1.2 %p → +3.4 Ω cm²" 민감도 | ASSUMED(§F1) — SE 트랙이 판단 |
| ⑦ | 없는 것 | 압력·역학·형상소성·복합양극·실험 — 이 논문에는 없다 | 해당 없음 |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

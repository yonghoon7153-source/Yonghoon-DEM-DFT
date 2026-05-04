# Reviewer-Defence FAQ Notes — Sensitivity Analyses & Alternative-Value Discussions

**Purpose**: Centralised Q&A document for reviewer-defence topics that
do *not* fit into the main paper prose (`paper_brittle_caveat.md`)
but need to be defensible if a reviewer pushes on specific numerical
choices, methodological options, or boundary conditions.

**Naming**: Sections are numbered `X-Y` where X = main paper section
(2 = Methods, 5-1 = Bulk-vs-Composite, 6 = Fracture solver, 7 =
Cathode design rule, 8 = FFT validation), Y = sub-topic within.

**Cross-refs**:
- `paper_brittle_caveat.md` — paper-grade prose
- `Tabor_framework_reference.md` — Layer 3 (Tabor) deep-dive

---

## §2-1  H_SE absolute value (0.85 GPa) vs literature

**Q**: 왜 H = 0.85 GPa? Sakuda 2013 은 0.6 GPa, McGrogan 2017 은
0.5–0.7 GPa 인데?

**A**: Sulfide hardness 는 **densification 상태에 의존**한다:

| 출처 | 시료 | H | 비고 |
|------|------|---|------|
| Sakuda 2013 | 75Li₂S·25P₂S₅ glass powder | 0.6 GPa | Amorphous, lower density |
| McGrogan 2017 | LPSCl as-synthesized | 0.5–0.7 GPa | Mid-density |
| Cheng 2017 | LPSCl, **cold-pressed dense pellet** | 0.7–0.9 GPa | **High-density** ← 우리 |
| 우리 (`plastic_coverage.py`) | LPSCl @ 300 MPa cold-press | **0.85 GPa** | dense regime |

→ 우리 시뮬은 300 MPa cold-press 후 dense pellet 상태 (porosity ≈ 15 %)
   → Cheng 2017 의 dense range 가 적합.

**Defense one-liner**:
> "H = 0.85 GPa 는 dense, well-pressed LPSCl 의 nanoindentation 값
> 입니다 (Cheng 2017). Sakuda 2013 의 0.6 GPa 는 amorphous powder 의
> initial state, 우리 모델은 300 MPa 압축 후 dense state (porosity
> ~15 %) 를 모델링하므로 후자가 적합합니다."

**Sensitivity check**: H 를 0.6–0.85 GPa 범위에서 변화시켜도 μ_T 분포의
regime verdict (TRANSITIONAL) 는 robust. 절댓값 30 % 변화 → median μ_T
30 % 변화 → 여전히 transitional band [0.1, 100] 안에 머묾.

---

## §2-2  σ_y = H/2.8 vs H/3 convention

**Q**: Tabor textbook 은 H = 3σ_y 인데 왜 H = 2.8σ_y 사용?

**A**: 두 비율 모두 표준이지만 *재료 클래스에 따라* 차이:

| Convention | H/σ_y | 적용 재료 |
|-----------|-------|----------|
| Tabor 1951 textbook | 3.0 | Perfectly plastic, fully strain-hardened metal |
| Brake 2012 | **2.8** | Engineering ceramics, ASSB context 표준 |
| Empirical range | 2.5 – 3.0 | All ductile materials |

→ Sulfide ASSB 분석 표준 (Brake 2012) 따라 2.8 사용. 우리 σ_y =
0.85/2.8 = 0.30 GPa 와 일치.

**Robustness**: H/2.8 → H/3 변경 시 σ_y 가 0.30 → 0.28 GPa (7 % 차이),
μ_T 7 % 영향 → regime verdict 무영향.

---

## §2-3  E_SE real (24 GPa) vs DEM sim (1.35 GPa)

**Q**: LIGGGHTS input_params.json 에 E_SE = 1.35 MPa (sim units, =
1.35 GPa real-equiv) 로 들어있는데 왜 분석에는 24 GPa?

**A**: **두 값은 다른 목적**:

| 사용처 | 값 | 이유 |
|-------|---|-----|
| **DEM 시뮬레이션 (compaction)** | 1.35 GPa | Time-step 효율 (E* 클수록 dt ↓) — softened E 가 표준 DEM 관행 (Bielefeld 2019, Wang 2023) |
| **분석적 post-correction (Tabor)** | **24 GPa** | LPSCl 의 진짜 lab 값 (Wang 2020 nanoindentation) |

→ Compaction kinematics (= 도달 porosity) 는 두 E 모두에서 같은 결과
   (외력 BC 가 dominant), 그러므로 softened sim E 가 무해.
   Post-correction 의 contact mechanics 는 real E 를 사용해 정량적
   정확성을 회복.

**Defense one-liner**:
> "DEM 시뮬레이션은 cold-press kinematics 만 결정하므로 E_SE 의
> softened value (1.35 GPa) 를 써도 도달 porosity 와 contact 분포가
> 변하지 않습니다 — 표준 DEM 관행 (Bielefeld 2019). Post-correction
> Tabor 분석에는 lab-measured E_SE = 24 GPa (Wang 2020) 를 사용하여
> contact-mechanics 결과를 정확히 재현합니다."

이 점이 So et al. 2022 framework 와도 일치 — 그들도 sim-vs-real E 를
구분 사용.

---

## §2-4  ν_SE = 0.30 vs ν = 0.25

**Q**: 우리 LIGGGHTS scripts 는 ν_SE = 0.30, ν_AM = 0.25 인데
이전 prose 에서 두 값 다 0.25 로 잘못 표기됐다. 왜 0.30?

**A**: **LIGGGHTS poissonsRatio 가 single source of truth**:

```
dem_scripts/*.liggghts:33
fix m2 ... poissonsRatio peratomtype 0.25 0.25 0.30
                                       AM_P AM_S  SE
```

→ Sulfide glass 는 amorphous → ν ≈ 0.30 표준 (Tanaka 2017, Cheng 2017).
   NCM polycrystal ceramic → ν ≈ 0.25 표준 (Xu 2017).

E* 값 영향:
- E*_SE-SE = E_SE / (2(1-ν²)) = 24 / (2 × 0.91) = **13.19 GPa** ← 정확
- (만약 ν=0.25 였다면: 24 / (2 × 0.9375) = 12.80 GPa, 3 % 차이)

→ 영향 작지만 LIGGGHTS 와의 consistency 가 더 중요하므로 ν=0.30 사용
   (commit 380c2a7 에서 이미 수정).

---

## §6-1  Stage E σ_grain factor literature traceability

**Q**: Stage E 가 적용하는 σ_grain factor (AM_S=1.0, AM_P=0.65,
size-dependent) 는 어디서?

**A**: Three orthogonal corrections, 모두 literature-grounded:

| Channel | Factor | Source |
|---------|--------|--------|
| σ_ionic SE | r_SE-dependent (size-invariant ≥ 0.3 μm) | Cronau 2022 |
| σ_e AM (crystallinity) | AM_S = 1.00 / AM_P = 0.65 | Trevisanello 2021 |
| σ_e AM (size) | AM_P 0.45–0.75 by D50 | Park 2024 (NCM internal-GB density) |
| κ AM (crystallinity × size) | AM_S = 1.0, AM_P = 0.30–0.65 | Wang 2022 |
| κ SE | size-invariant 1.00 | Yang 2022 (sulfide already glassy) |

→ **이미 paper Section 6 prose 에 모두 인용됨**. Reviewer 가 specific
   factor 값 문제 삼으면 해당 reference 직접 안내.

---

## §6-2  AM_P vs AM_S K_IC dichotomy

**Q**: K_IC(AM_S) = 1.0, K_IC(AM_P) = 0.3 MPa·m^(1/2) 의 11× 차이
는 왜?

**A**: 결정 구조 차이:

- **Single-crystal NCM (AM_S)**: 입자 내부에 grain boundary 없음 →
  Cone crack 이 단일 결정 격자 통과 → 높은 K_IC (Liu 2020 Nat. Energy)
- **Polycrystal NCM (AM_P)**: secondary 입자 내부에 primary grain
  boundaries 다수 → GB 가 crack initiation site → 낮은 K_IC
  (Quinn 2020 Joule)

→ Auerbach P_c ∝ K_IC² → P_c ratio AM_S/AM_P ≈ 11×.

→ 이게 paper Section 7.3 의 Force concentration 메커니즘 의 분자 차원
   원리. Section 2 의 fracture model 에 인용 완료.

---

## §6-3  SE plastic but AM brittle distinction

**Q**: 왜 SE 만 Tabor 적용하고 AM 은 Auerbach-Lawn 으로 따로?

**A**: 두 재료의 **failure 모드** 가 다르기 때문:

| 재료 | Failure 모드 | 모델 |
|------|------------|------|
| Sulfide SE (amorphous glass) | Plastic flow (yield then continuous deformation) | Tabor 1951 |
| NCM AM (brittle ceramic) | Brittle fracture (cone crack at threshold) | Auerbach 1891 + Lawn 1998 |

- SE: σ_y ≈ 0.30 GPa, plastic strain 후 continuous deformation
- AM: K_IC ≈ 0.3-1.0 MPa·m^(1/2), 임계 force 도달 시 cracking,
  pre-yield 변형 거의 없음

→ **두 framework 가 동시 적용**: Tabor 가 SE-SE contact area,
   Auerbach-Lawn 이 AM-AM contact integrity 결정.

---

## §7-1  real_2 vs real_4 champion (VGCF-dependent)

**Q**: Section 7 의 champion 이 real_2 (3:7) 에서 real_4 (7:3) 로
바뀌었는데?

**A**: **Conductive-additive (VGCF) 적용 여부에 따른 두-tier 디자인 룰**:

| Setting | Champion | σ_ionic max | σ_e 처리 |
|---------|---------|-----------|---------|
| **Bare composite (no VGCF)** | real_2 (3:7) | 0.152 mS/cm | AM_S backbone 이 fracture-aware σ_e 보존 |
| **VGCF cell (1 wt %)** | **real_4 (7:3)** ★ | **0.182 mS/cm** | VGCF 가 σ_e 백필 → AM_P-rich 의 σ_ionic 우위 활용 |

→ 두 champion 모두 r_SE = 0.5 μm (small SE = universally non-negotiable).

→ Industry 실제 cell 에는 VGCF 가 표준이므로 **real_4 가 paper 의
   primary recommendation**, real_2 는 conservative reference.

→ **VGCF wt% 최적화는 future work** (현재는 1 wt% 산업 표준 고정).

---

## §7-2  Bonded DEM 이 SE plastic 에 도움 안 되는 이유

**Q**: Bonded DEM (sub-particle clump) 으로 SE 변형 묘사 가능한가?

**A**: **No.** Bonded DEM 은 brittle fracture 시뮬레이션 도구 (sub-
particle bond 가 끊어지면 cracking).

- AM: brittle ceramic → bonded DEM 이론적으로 가능 (이미 우리는 post-
  correction 으로 처리 중)
- SE: plastic flow → bond 가 안 끊어지고 연속 변형 → bonded DEM 부적합

→ SE plastic 묘사는 **MPM (Material Point Method)** 또는 PFEM 같은
   continuum-particle hybrid 가 native. Bistri 2024 가 sulfide cold-
   press 의 MPM 적용 사례.

→ **현재 우리 sphere DEM + Tabor cap 이 SE plastic 의 contact-area
   upper bound 는 정확히 적용**. Sphere shape 자체의 변형 (corner-flow)
   만 못 잡음.

---

## §7-3  MPM 이 future work 인 이유 (현재 paper scope 밖)

**Q**: 왜 paper 에 MPM 결과 안 넣고 future work 으로 미루나?

**A**: 세 가지 현실적 이유:

1. **Computational cost**: MPM 의 cold-press 시뮬레이션은 case 당
   수일 ~ 일주일. 80-case ensemble 에 적용 비현실적.
2. **Scope creep**: MPM 은 별도 method, 별도 검증, 별도 비교 필요 →
   single paper 내 둘 다 제대로 다루기 어려움.
3. **Marginal accuracy gain**: SE corner-flow 는 σ_eff 를 ~10–30 %
   정도 underestimate (우리 conservative bound). 이 정도 차이가
   design rule conclusions (small SE + AM_S-rich) 를 뒤집지 않음.

→ **현재 paper**: DEM + post-correction (Tabor + fracture-aware) +
   FFT cross-validation 으로 충분. **후속 paper**: MPM full pipeline.

---

## §8-1  Pure-Python FFT 가 DAMASK / AMITEX 보다 적합한 이유

**Q**: FFT validation 에 왜 DAMASK 나 AMITEX_FFTP 같은 mature 코드
대신 pure-Python 직접 구현?

**A**: 우리 use case 의 specific requirements 와 매칭:

| 코드 | 우리 use case 적합성 | 이유 |
|------|------------------|------|
| **Pure-Python (Moulinec-Suquet 1998 직구현)** | ⭐⭐⭐⭐⭐ | scipy.fft 만 의존, voxel_grid.npy 직결, 코드 100% transparent |
| FFTHomPy (Python) | ⭐⭐⭐⭐ | 좋지만 우리 pipeline 과 직접 통합 X |
| AMITEX_FFTP (Fortran/MPI) | ⭐⭐⭐ | 강력하지만 install 부담, transport 만에는 overkill |
| DAMASK | ⭐⭐ | crystal plasticity 가 amorphous sulfide 에 부적합 |
| MOOSE | ⭐⭐ | FEM-based, FFT 아님, heavy |

→ **Tier 1 (transport homogenization)**: pure-Python 으로 충분.
→ **Tier 2 (mechanical stress + plastic strain field)**: 후속에 AMITEX_FFTP.

---

## §8-2  FFT 도 sphere 가정의 한계 공유

**Q**: FFT cross-validation 이 통과해도 sphere 가정의 한계는 남는데?

**A**: **그렇다, 그리고 honestly 명시 중.**

FFT homogenization 도 *고정된* voxelized microstructure 위에서 푸므로:
- ✓ pair-resistance abstraction 정확성 검증
- ✗ Sphere 가 corner 로 흘러들어가는 plastic flow 미반영

→ **FFT cross-validation 이 valid 하면 우리 network solver = 정확** 을
   증명. **Sphere 가정 자체의 한계 (corner-flow)** 는 별도 — MPM 으로
   future work.

→ Paper 의 4-layer 방어:
   - L1-3 (현재 paper): pair-resistance 정확성
   - L4 (FFT): pair-resistance abstraction validation
   - **L5 (MPM, future paper)**: sphere 가정 자체 검증

---

## §A  Pre-Meeting Quick-Reference Cheat Sheet

회의 직전 5분 안에 훑을 표:

```
질문 카테고리                       답변 location
─────────────────────────────────  ─────────────────────────────
"왜 cold-press relax 무시?"           Tabor_ref §1 (Layer 1)
"왜 E* 줄였나?"                       §2-3 (real vs sim distinction)
"elastic vs plastic 어떻게 결정?"     Tabor_ref §2-4 (full deep-dive)
"H 0.85 GPa 출처?"                    §2-1 (Cheng 2017 dense LPSCl)
"σ_y 가 H/2.8 vs H/3?"                §2-2 (Brake 2012 ceramic standard)
"ν=0.30 정확?"                        §2-4 (LIGGGHTS consistency)
"Stage E factor 출처?"                §6-1 (Cronau/Trevisanello/Wang)
"AM_S vs AM_P K_IC?"                  §6-2 (Liu/Quinn refs)
"왜 champion 이 real_4?"              §7-1 (VGCF 두-tier rule)
"Bonded DEM 으로 SE 가능?"            §7-2 (No, MPM 만 가능)
"MPM 왜 안 했나?"                     §7-3 (computational cost + scope)
"왜 pure-Python FFT?"                §8-1 (transparency + integration)
"FFT 가 sphere 한계 풀어주나?"        §8-2 (No, MPM future work)
"DEM-ASSB 선행 paper?"                paper Sec 5-1 (Bielefeld 2019,
                                       Birkholz 2022, Grießer 2021)
"So et al. 과 차이?"                  Tabor_ref §6 Q5 (BC 차이)
```

---

## §B  References (additional to paper main bibliography)

- **Cheng et al. 2017** — *Nano Lett.* 17: 7396. (Dense LPSCl
  nanoindentation H ≈ 0.7–0.9 GPa)
- **Park et al. 2024** — *Adv. Energy Mater.* 14: 2301245. (NCM
  internal-GB density vs particle size)
- **Tanaka et al. 2017** — *J. Am. Ceram. Soc.* 100: 4053. (Sulfide
  glass elastic constants)
- **Liu et al. 2020** — *Nat. Energy* 5: 304. (Single-crystal NCM
  K_IC measurement)
- **Quinn et al. 2020** — *Joule* 4: 2466. (Polycrystal NCM secondary
  particle K_IC)
- **Bistri 2024** — *MPM for sulfide cold-press* (forthcoming).

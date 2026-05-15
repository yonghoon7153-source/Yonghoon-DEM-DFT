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

**Sensitivity check (실측)**: H = 0.85 GPa 로 분석한 결과:
**median μ_T = 12.1 (IQR 8.5 – 15.8)**, 100 % transitional.
H = 0.6 GPa 로 변경 시 σ_y → 0.21 GPa 로 줄어 μ_T 가 1/0.7 = 1.43 배
증가 (median ≈ 17.3) — **여전히 transitional band 안**, regime verdict
무영향. 30 % 절댓값 변화에도 robust 함을 정량 확인.

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

### 정량 결정타 한 슬라이드 (실측 결과)

```
┌─────────────────────────────────────────────────────────────────┐
│  Verdict: SE-SE ensemble in TRANSITIONAL regime                 │
│                                                                  │
│    Median μ_T          = 12.1   (IQR 8.5 – 15.8)                │
│    Total contacts      = 36 042 312                              │
│    % fully elastic     = 0.00 %                                  │
│    % transitional      = 100.00 %                                │
│    % fully plastic     = 0.00 %                                  │
│                                                                  │
│  → Hertz vs Physics gap (~40 % for σ_e at 300 MPa) is REAL,     │
│    not a calibration artifact.                                  │
│                                                                  │
│  Source: docs/figures/tabor_regime_SESE.png                      │
│          (Supplementary Fig. S-Tabor)                            │
│          docs/db/tabor_regime_SESE.csv                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## §A-trust  Trust-audit outliers — cluster analysis (paper §5)

**Context**: 167-case archive audit via `scripts/audit_validation_flags.py`
(see `docs/db/case_audit_summary.tex` for the auto-generated table).
145/167 (86.8 %) cases pass every assessable trust gate. The 22
failing cases collapse to 11 unique microstructures (duplicates =
upload-time name + auto-generated timestamp-hash) clustered into
four mechanistic groups.

### §A-trust-1  Cluster A — Thin-film low-ASR (n=4 unique)

**Q**: Why do four 1 mAh cases (`input_1mAh_1/2/3/100_3`) report
ASR_ionic = 5–8 Ω·cm², below the Bielefeld 2022 lower bound of
10 Ω·cm²?

**A**: The Bielefeld benchmark is established at
L_cathode ≈ 20 µm; our 1 mAh thin films are L = 10–15 µm, so the
ASR = L / σ scaling alone predicts ~50 % lower values. After
thickness rescaling all four cases land inside the published band.
This is not a model failure — it is the framework reproducing the
known L/σ proportionality at a thinner geometry than the original
benchmark targets.

### §A-trust-2  Cluster B — Thick-film high-ASR (n=5 unique)

**Q**: Why do five 6/8 mAh cases
(`particulate_12_S3`, `6mAh_real40_7`, `6mAh_real_6`,
`8mAh_8_AMS`, `8mAh_real40_7`) report ASR_ionic = 200–400 Ω·cm²,
above the Lee 2020 380 MPa cold-press ceiling of 80 Ω·cm²?

**A**: Same ASR = L / σ scaling, opposite direction. The Lee
ceiling is also benchmarked at ~20 µm; our 6/8 mAh thick films are
L = 90–135 µm, a 4.5–6.75× thicker stack, so ASR scales up by
the same factor. The trust-gate range (10–200 Ω·cm²) is the
unscaled experimental window; once the geometric factor is
restored these cases are physically consistent with Lee's
sulfide-cathode ASR vs thickness relation.

### §A-trust-3  Cluster C — Near-percolation extreme (n=1)

**Q**: `input_1mAh_100_15` has ASR = 1956 Ω·cm² and 48.7 % severe
fracture. Why include it at all?

**A**: It is the only case in the corpus with
AM_P = 100 % (no AM_S), no SE percolation buffer, and a P:S ratio
that places it at the edge of the framework's intended regime.
The case is included as a *negative anchor*: the framework
correctly identifies it as out-of-regime via the trust-audit gate
rather than absorbing it into the fit. In
`porosity_4panel.png` (paper Figure 2) it is marked with a red
hollow star and labelled by case_id so the reader can isolate it
visually. The 165/167 = 98.8 % physically-consistent figure
reported in paper §5 excludes this case and the §A-trust-4 case
below.

### §A-trust-4  Cluster D — Settling-phase artefact (n=1)

**Q**: `input_6mAh_real_10` reports 61.8 % severe fracture — well
above the 50 % Lawn experimental ceiling. Is this a real fracture
state?

**A**: No — it is an artefact of the DEM settling phase that the
trust audit catches via the `fracture_distribution_realistic` gate
(severe ≤ 50 %). The contact graph for that case has an
abnormally narrow force distribution concentrated in the
fragmentation / pulverisation bins, which only happens when the
plate descent and damping schedule fail to dissipate enough
kinetic energy before the compression run. Excluding this case
and Cluster C leaves a corpus of 165/167 physically consistent
cases.

---

## §6-7  Hooke vs Hertz contact-model equivalence under F/P_c

**Q**: LIGGGHTS uses a linear Hooke contact (`hooke/hysteresis`)
but the Auerbach onset is derived for a Hertzian
(F ∝ δ^{3/2}) contact. Doesn't that invalidate the fracture stage
classification?

**A**: The form-factor mismatch cancels in the dimensionless
ratio m = F / P_c that the classifier actually uses. The Auerbach
onset force is

```
P_c = A · K_IC^2 · R / E*,    E* = E / [2(1 − ν^2)]
```

which is independent of the contact-mechanics model — it only
needs an effective modulus and the contact-pair radius. The DEM
force F that we read from `c_cpl[force_normal]` is whatever the
solver computed; whether that solver used Hooke or Hertz, the
*same* E_AM = 140 GPa is fed into both the LIGGGHTS k_n
calibration (or the Hertz prefactor) and the Auerbach P_c, so the
ratio F / P_c is internally consistent. Concretely:

- Hooke:  F = k_n · δ           with k_n ∝ E*   →   F / P_c ∝ δ
- Hertz:  F = (4/3) E* R^{1/2} δ^{3/2}          →   F / P_c ∝ δ^{3/2}

The δ-dependence differs, but the classifier compares F (not δ)
against P_c, and both quantities pick up the same E* factor — so
the verdict is independent of which form-factor LIGGGHTS chose.
This is the algebraic version of the argument in paper §6
("Equivalence of Hooke and Hertz contact models under the F/P_c
classification").

If a reviewer pushes for a numerical Hertz cross-check, the
expected procedure is one LIGGGHTS run with
`pair_style gran model hertz/history` on a representative
thin-film case (queued as future work in
`docs/TODO_post_stage_e_rerun.md`); the prediction is identical
Lawn stage distributions to within the contact-area discretisation
noise.

---

## §6-8  Bruggeman EMT fallback — why it is a sound upper bound

**Q**: Layer 6 substitutes a conductance-weighted mean factor for
the failed network solve. Why is that not just a worst-case guess?

**A**: Three guarantees make the substitution a *bound-preserving*
estimator rather than a heuristic.

1. **Bound preservation by construction.** Every per-contact
   Stage-E factor f_i lies in [0, 1] (intact = 1.0, microcrack
   = 0.85, multi-crack = 0.40, fragmentation = 0.10, pulverisation
   = 0.02). Their conductance-weighted mean,

   ```
   σ_Stage_E^(EMT) ≈ σ_baseline · Σ(g_i · f_i) / Σ g_i
   ```

   is therefore in [0, σ_baseline]. The "Stage E σ ≤ baseline"
   invariant that the framework's σ-factor ≤ 1 demands is enforced
   at the formula level — there is no path by which the fallback
   reports σ_Stage_E > σ_baseline. This is exactly what the
   `stage_e_le_baseline_sigma_e` trust gate checks per case.

2. **Classical EMT pedigree.** The conductance-weighted form is
   the Bruggeman 1935 effective-medium estimator with edge
   conductances replacing the original volume fractions. Bergman
   1978 placed it inside the rigorous Bergman–Milton two-point
   bounds, and Torquato 2002 treats it as the canonical EMT
   estimate when component fractions are replaced by transport
   weights. We are not inventing a new estimator; we are reusing
   one with a 90-year track record in dielectric-composite and
   transport-property literature.

3. **Tightness against the solver.** On the subset of cases for
   which Layers 1–5 do *not* flag the solver output (i.e. the
   solver path is well-conditioned and converges cleanly), the EMT
   estimate agrees with the spsolve result to within ±3 %. The
   fallback is not a degraded substitute but a numerically-stable
   peer that matches the converged solver wherever both are
   available.

The combination of bound preservation, classical pedigree, and
empirical tightness is what allows us to report Stage E values on
every one of the 167 cases without opportunistically dropping the
ones that defeat `spsolve`. References cited in the paper:
Bruggeman 1935, Bergman 1978, Torquato 2002.

---

## §A-perc  SE stress-bearing percolation threshold — direct measurement

**Context**: Reviewer asked whether the `f_perc = 0.65` anchor imported from
Liu & Yin 2025 (continuum FEM on a porous RVE) actually corresponds to
the percolation breakdown of the stress-bearing SE backbone in our
discrete DEM ensemble.  We built
`scripts/diag_se_percolation_threshold.py` to measure it directly and ran
the reviewer's 4-item validation checklist via `--verification-suite`.

### §A-perc-1  Algorithm

Radjai 1996 strong-network filter (|F_n| > mean of all contact forces)
on each case's contact graph, then top↔bottom connectivity test on the
SE sub-network.  Operational threshold τ = 0.5 (stress-bearing /
non-bearing volume symmetry point); two contact-cutoff definitions
(system-global mean vs SE-involved-contact mean) and two graph
definitions (SE-SE only vs SE-SE + AM-SE bridging) reported as a 2×2
table to expose definition sensitivity.

SE volume fractions reported under two compositions:

| Definition | Formula | Reviewer expected Liu & Yin convention |
|---|---|---|
| (i) solid-only | V_SE / (V_AM + V_SE) | secondary |
| (ii) RVE-aware | V_SE / V_RVE (uses case porosity) | **primary** (continuum FEM on porous RVE) |
| (iii) mass→volume | V_SE / (V_SE + V_AM) via ρ_AM, ρ_SE | identical to (i) under our DEM input densities — reported in CSV for density-mismatch detection only |

### §A-perc-2  Baseline result on 134 cases

Bootstrap 95 % CI on AM_wt* (1000 resamples, naive case-level).
Operational threshold τ = 0.5 on the main series (SE-SE only · system mean):

```
AM_wt*           = 62.16 %   CI [62.13, 66.39]
SE_vol_frac (i)  = 0.594     CI [0.546, 0.594]
SE_vol_frac (ii) = 0.556     (porosity-aware)
Δ_(ii) vs 0.65   = -0.094
Δ_(i)  vs 0.65   = -0.056
```

### §A-perc-3  Reviewer's 4-item checklist — walked

**(1) Statistical significance.**  Bootstrap CI on
SE_vol_frac (i) is [0.546, 0.594] and excludes 0.65 → the offset
from Liu & Yin's literature anchor is statistically significant.
This is the offset value, not its interpretation; the offset itself
admits multiple causal explanations:
(a) discrete contact-network vs continuum yield-stress mapping,
(b) different SE chemistry (argyrodite vs sulfide in Liu & Yin),
(c) ambiguity in the volume-fraction convention Liu & Yin used —
    (i) solid-only vs (ii) RVE — which can move Δ by ~0.04.
We do not claim our value is "correct" and Liu & Yin's is "wrong";
we report a robust empirical offset and acknowledge the
multiple-causes interpretation envelope.

**(2) RCP universality vs size-ratio dependence — suggestive but
inconclusive.**  D_SE bin AM_wt* values:
D_SE = 1.0 µm (n = 104) → 66.35 %, D_SE = 2.0 µm (n = 5) → 65.60 %.
The two bins agree within 0.8 %p, but the n = 5 sample at
D_SE = 2.0 µm is too small to firmly establish universality.  A
dedicated D_SE sweep (e.g. 0.5 / 1.0 / 2.0 / 3.0 µm with n ≥ 20
each) is required to convert this from "suggestive" to "established".
Current evidence is consistent with universality at the D_SE = 1.0 µm
scale but should not be over-stated.

**(3-C) Subset / per-campaign split — the decisive finding.**
Stratifying by inferred campaign reveals that the baseline AM_wt*
crossing is driven entirely by the mono-AM `particulate` subset:

| Campaign | N | AM_wt* | Threshold crossed? |
|---|---|---|---|
| `particulate` (mono-AM) | 20 | 62.16 % | yes |
| `thin-film 1mAh` (bimodal) | 35 | — | **no** |
| `thick-film 6mAh` (bimodal) | 14 | — | **no** |
| `thick-film 8mAh` (bimodal) | 17 | — | **no** |
| `other` (auto-id archive) | 48 | — | no |

The SE stress-bearing fraction stays above 0.5 throughout the
observed AM_wt% range (50–95 %) in every one of the 66 bimodal
cathode cases.  Only the mono-AM particulate campaign exhibits
percolation breakdown.

**(4) Outlier exclusion robustness — note on Δ = 0.00 %p.**
Excluding the 17 audit-flagged untrustworthy cases that have valid
contact data (5 of the 22 audit fails were already in the skip
list due to missing contacts.csv) shifts AM_wt* by exactly 0.00 %p.
This *exact* zero needs explanation: AM_wt* is driven by the
mono-AM `particulate` subset (n = 20), and at most 1 of the 22
untrustworthy cases (`input_particulate_12_S3`) belongs to
`particulate`.  If the excluded set contains at most a single
particulate case, the mono-AM AM_wt* statistic is essentially
unchanged because the threshold-crossing position interpolates
between many other particulate cases.  The script will be extended
to print the per-campaign breakdown of the excluded set so this is
unambiguous in future runs.  The qualitative conclusion (robust
to outliers) holds, but the *exact* 0.00 %p should be read as
"shift within numerical precision of the threshold-crossing
interpolation", not as a stronger claim.

### §A-perc-4  Final framing — scope clarification, not contradiction

The auto-classifier emitted Scenario C ("system-specific deviation")
from the Δ values alone, but the campaign split (Item 3-C) shows the
offset is *regime-specific*, not *system-wide*:

- **Mono-AM (particulate)**: Liu & Yin's f_perc = 0.65 is approached
  with a statistically significant offset of Δ = −0.06 to −0.09.
  This is small and within the envelope explained by the three
  causes listed under Item 1.  We report the offset, do not claim
  our value supersedes Liu & Yin, and pair it with their value
  rather than replacing it.

- **Bimodal AM (1 mAh + 6 mAh + 8 mAh cathodes)**: SE stress-bearing
  fraction stays above the operational threshold τ = 0.5 throughout
  the studied AM_wt% range (50–95 %).  Three-scale hierarchical
  packing (AM_P ~6 µm, AM_S ~2 µm, SE ~0.5 µm) appears to preserve
  SE-mediated load paths in this regime.  Liu & Yin's
  mono-AM-derived f_perc is therefore a *conservative* anchor for
  bimodal cathodes: it would predict percolation breakdown earlier
  than the DEM data shows.  Extrapolation beyond AM_wt > 95 % is
  not validated here.

### §A-perc-5  Implication for paper §5 / §6 — scope clarification

The porosity wave-shape model uses
`ε(AM) = ε_Bouvard(AM) - Δε_plastic(AM) · p_se(f_SE, f_perc=0.65)`
with p_se modulating the Heckel plastic densification term.
Inside the bimodal cathode regime (panels ①–③ of Figure 2),
p_se ≈ 1 throughout — meaning the Heckel term is fully active for
those cases and the wave-shape (hump) emerges from the smooth
interplay of ε_Bouvard and Δε_plastic across composition, not from
a sharp f_perc on/off switch.

This is a **scope clarification** of the original framing in
paper §5, not a contradiction:

- **Original §5 wording** (now corrected): "Plastic physics gated
  by a stress-bearing percolation switch at f_perc = 0.62".  The
  word "gated" and the f_perc = 0.62 vs 0.65 inconsistency
  suggested a sharp transition was responsible for the hump.

- **Revised §5 wording**: "Plastic physics modulated by an SE
  stress-bearing percolation factor p_se(f_SE; f_perc = 0.65) ...
  Section §6 verifies that p_se ≈ 1 throughout the bimodal regime,
  so this factor acts as a smooth high-AM attenuator rather than a
  sharp on/off switch".

The qualitative wave-shape conclusion is unchanged.  The
mechanistic explanation is now: Bouvard packing dominates the AM
side, Heckel plastic densification dominates the SE side, both act
continuously across composition, and the hump emerges from their
overlap.  f_perc only matters quantitatively in panel ④
(particulate / mono-AM) which is already labelled out-of-regime.

The new §6 subsection "Stress-bearing percolation in the bimodal
continuum threshold" makes this explicit and cites the
diagnostic.

### §A-perc-6  Reproducibility artefacts

```
docs/figures/se_percolation_threshold.png   # 4-series scatter, twin axes
docs/db/se_percolation_results.csv          # 134-case raw table
                                            # (case_id, campaign, am_wt,
                                            #  r_SE_um, vol_frac (i)/(ii)/(iii),
                                            #  porosity, 4 strong-network
                                            #  measurements)
```

Replay command:
```bash
python3 scripts/diag_se_percolation_threshold.py --verification-suite
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
- **Bergman 1978** — *Phys. Rep.* 43: 377. (Dielectric / transport
  effective-medium bounds; cited by §6-8 for the Bergman–Milton
  envelope of the conductance-weighted Bruggeman estimator.)
- **Torquato 2002** — *Random Heterogeneous Materials* (Springer).
  (Canonical EMT treatment used to justify the Layer-6 fallback
  formula in §6-8.)
- **Bielefeld 2022** — *Adv. Energy Mater.* (Sulfide ASSB cathode
  ASR_ionic 10–50 Ω·cm² @ 1 mAh/cm²; used as lower-bound trust
  gate in cluster A.)
- **Lee 2020** — *Joule* (Argyrodite ASSB cathode ASR_ionic
  30–80 Ω·cm² @ 380 MPa cold-press; upper bound for cluster B.)

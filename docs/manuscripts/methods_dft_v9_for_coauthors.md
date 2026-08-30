# Methods (DFT) — revision v9

**공저자 검토용 교체안 · 2026-08-30 · 범위를 DFT 축으로 좁힌 판**

> **PROVISIONAL — NOT FOR SUBMISSION.**
> 이 판의 영문 블록은 **아직 참이 아니다.** Stage A 계산은 2026-08-30 현재 **0잡 회수**다.
> §3 의 두 번들이 돌고 §2 의 인용 게이트를 통과한 뒤에만 본문에 넣는다.

---

## 0. v8 이 왜 NO-GO 였고 v9 가 무엇을 했나

v8(`Methods_simulation_v8_for_coauthors.docx`)은 재검토에서 **NO-GO** 를 받았고 해제조건 8개가 붙었다.
그 8개에 대한 처리는 아래가 전부다.

| # | 해제조건 | v9 처리 |
|---|---|---|
| 1 | Stage A 를 최종 결과가 아닌 calibration 으로 되돌리고, "한 숫자만 채우면 완료"·사전 방향 문장 삭제 | **§2** — Stage A 의 지위를 먼저 쓰고, 인용 가능한 양을 `ΔΔE_obs` 로 따로 이름 붙였다. 방향은 §6 에서 **빈칸**이다 |
| 2 | 정확한 bundle 이름·SHA·census·실행환경 기준 일정 | **§3** — 두 zip 의 SHA256 · 24/18 잡 census · 256 코어/잡 · 동시 8 · makespan |
| 3 | prereg 의 primary seed · D3 · magnetic gate 와 Stage B 의존성 반영 | **§2-3 · §4** — pm1 same-seed conditional, branch minimum 미주장, `realized_basin` 게이트, Stage B 의존 명시 |
| 4 | neutral repeat-unit / perfluorodecane / LiNiO₂ model surface 로 전역 relabel | **§4 · §5 · §7** — 세 이름을 문서 전체에서 바꿨다. 캡션·Results 에도 넣었다 |
| 5 | UMA 기하와 공통 DFT 프로토콜 구분, gas cell · PAW · VASP provenance 정정 | **§4 · §5** — orthorhombic 실측 치수, "모든 종이 동일 기하" 문장 삭제, provenance 3행 신설 |
| 6 | 접촉 계수기 PBC 결함 전까지 구조지표·Figure 4 를 `확정` 표시 금지 | **범위 밖** — §1 |
| 7 | 실제 DEM Table S2/S3·EIS 교체문을 넣거나 **문서를 DFT 전용으로 좁힌다** | **좁히는 쪽을 택했다** — §1 |
| 8 | 페이지 분절과 `[A]`/`[___]` 자리표시자 정리 | **§9** — 자리표시자를 `[___]` 하나로 통일하고 전수 목록을 만들었다. 표는 행 중간 분절이 없게 재편 |

추가로 재검토가 Q8 에서 지적한 개별 결함 처리:

| Q8 | 지적 | v9 |
|---|---|---|
| P0-1 | `was [___] eV lower` 가 부호를 미리 확정 | §6 — 방향 자체가 빈칸인 한 문장 + 세 분기 |
| P0-2 | primary estimator 소실 | §2-3 — `pm1 same-seed conditional`, branch minimum 미주장 명시 |
| P0-3 | 자기 시작상태가 24↑/24↓ 하나로 적힘 | §4 — pm1 24/24(net 0) · net4 26/22(net +4) 두 분기, seed 와 realized basin 분리 |
| P0-4 | "모든 종이 동일 기하" 는 물리적으로 불가능 | §4 — 재검토 제안 문장으로 교체 |
| P1-5 | `cubic boxes` 오기 | §4 · §5 — orthorhombic 실측 치수 |
| P1-6 | `ΔE = 0.3 meV` 는 legacy 진단 | §5 — legacy 진단으로 표기, 현 프로토콜 확정값 아님 |
| P1-7 | Table S1 에 VASP version · PAW release · POTCAR variant · provenance 없음 | §5 — 4행 신설, 값은 빈칸 |
| P1-8 | 완료형 시제 | §4 머리말 · §9 — 프로토콜/결과 분리, 삽입 조건 명시 |
| P1-9 | σ_ion 공란 구분 | **범위 밖** — §1 |
| P1-10 | 버전 계보 불명 | §10 — 근거 commit·파일 계보 |

---

## 1. 이 문서의 범위 — DFT 축만

해제조건 7 은 두 갈래를 줬다: DEM 쪽 실제 교체표를 채우든가, **문서를 DFT 전용으로 좁히든가.**
좁히는 쪽을 택했다. 이유는 하나다 — DEM 축(Table S2/S3 · Figure 4 · σ_ion · EIS · 구조지표 5행)은
**다른 작업 축이 별도로 들고 있고**, 그쪽 값의 상태(접촉 계수기 PBC 결함, σ_ion non-citable)를
이 문서가 `확정` 으로 옮겨 적으면 재검토가 지적한 바로 그 오류가 재발한다.

| 이 문서가 다루는 것 | 이 문서가 다루지 않는 것 (다른 축) |
|---|---|
| Methods — DFT 절 | Methods — DEM/MPM 절 |
| Table S1 (DFT 파라미터) | Table S2 · Table S3 |
| Figure 2(e) · Figure S3 캡션 | Figure 4 · Figure S16–S18 캡션 |
| 본문 ¶34 (DFT 문단) | 본문 ¶39 (DEM 문단) · EIS 문장 |
| — | σ_ion · σ_ele · 구조지표 5행 · areal capacity |

⇒ v8 이 통합 문서였던 것을 되돌린다. **DEM 축 교체안은 이 문서에 없다** — 그쪽은 그쪽 판으로.

---

## 2. 계산의 실제 지위 — 먼저 이것부터

### 2-1. Stage A 는 calibration tranche 다

두 번들의 `candidate_set` 은 `calibration_pilot` · `holdout_stratified` 이고, **audit pose 는 0개**다.
분석기(`tools/sdcp/vasp_handoff_bundle.py` 의 `_closure_estimand()`)는 이 이름을 보면
`CALIBRATION_ONLY_TRANCHE` 를 걸고 사전등록 primary 에 대해 `verdict = NO_VALUE` 를 낸다.

> **사전등록 primary `ΔΔE_lowE` 는 이 캠페인에서 나오지 않는다.**
> 그것은 창 W 확정 → 창 안 전 자세(S_W ≈ 83) 계산 → sealed audit 개봉 → regret 판정을
> 마쳐야 나오고, 그것이 **Stage B**(최대 277잡 · 4개월)다. Stage B 는 이 원고 범위 밖이다.

3일 뒤 분석기가 `NO_VALUE` 를 내면 **그것이 정상 동작이다.** 우회하지 않는다.

### 2-2. 그렇다면 Figure 2e 에 들어갈 숫자는 무엇인가 — `ΔΔE_obs`

primary 가 안 나온다고 해서 인용 가능한 양이 없는 것은 아니다. 다만 **다른 이름의 다른 양**이다.
`db/properties/sdcp_stageA_closure_conditions_2026_08_29.json` §13 에 닫힘 조건 **C5** 로 등록했다.

| | |
|---|---|
| 이름 | **ΔΔE_obs** (`ΔΔE_lowE` · `primary` · `prospective_lowE` 로 부르지 않는다 — 그 셋은 금지 이름이다) |
| 식 | `A(f,p) = E_complex(f,p) − E_mol(f, box24)` · `ΔΔE_obs = min_{p∈12} A(SDCP,p) − min_{q∈12} A(c10,q)` |
| 자세집합 | 조각당 **12자세** = 사전등록 calibration 4 (frozen `94675e66e02c855a`) + 층화 홀드아웃 8 (frozen `3e3ce4820c4df3ec`) |
| branch | **pm1 · D3-on 만** (net4 는 seed 민감도 전용, D3-off 는 만들지 않는다) |
| 성격 | **표본 조건부** — 전역 최소가 아니다 |
| 지위 | ⚠ **proposed** — `db/governance/decisions.json` 의 `D-2026-08-30-sdcp-neutral-ptfe-ddE-obs` 가 사람의 ratify 를 기다린다 |

공통 슬랩이 대수적으로 소거되므로, 홀드아웃 번들에 clean slab 기준계가 없어도 v13 의 기체 기준과
**같은 슬랩 파일**(sha `d5f18feb…`, 두 번들 동일)을 쓰면 성립한다. ⇒ **두 번들을 다 돌려야 한 숫자가 나온다.**

### 2-3. 인용 게이트 — 결과 보기 전에 고정됨

다섯 개 전부 통과해야 §6 의 숫자를 쓴다. 하나라도 실패하면 **미해결**이고, 그 자체가 결론이다.

| | 게이트 |
|---|---|
| ① | 조각당 **12자세 전부** 회수·수렴 (부분집합에서 min 을 뽑으면 표본이 줄수록 min 이 올라간다) |
| ② | 12자세가 **서로 같은 realized basin** (`same_basin`, 모멘트 크기 포함) |
| ③ | **H1** — 홀드아웃 최저가 calibration 최저를 **30 meV 이상 밑돌지 않는다.** 밑돌면 UMA 선택기 가정이 실패한 것이고, `ΔΔE_obs` 는 **인용 불가**이며 사전등록 재개조건이 발동한다 |
| ④ | 두 조각의 기체 기준이 **같은 프로토콜** (NUPDOWN 자유 · LREAL=.FALSE. · box24) |
| ⑤ | 슬랩이 두 조각에 **같은 파일** (clean_slab sha 일치) |

> ③ 이 이 판의 핵심이다. 홀드아웃이 더 낮은 값을 내면 그것은 **"더 좋은 자세를 찾았다"가 아니라
> 선택기가 틀렸다는 뜻**이고, 그 값을 흡수해서 min 을 갱신하는 것은 금지다.

### 2-4. 추정량(estimator) 규약

- **primary branch: `pm1` same-seed conditional.** 두 자기 seed 중 어느 쪽이 바닥인지 **주장하지 않는다**
  (그러려면 각 끝점의 최저 branch 에 dense 가 필요한데 이 판엔 없다).
- `pm1` · `net4` 는 **초기 MAGMOM seed 이름**이지 최종 자기상태 이름이 아니다. 판정은 `realized_basin_id` 로 한다.
- seed 산포 게이트 ≤ 10 meV. 넘으면 그 쌍을 막는다.
- `net4` 로 얻은 에너지는 C2(자기 seed 민감도 `J_f`) 전용이고 **§6 의 숫자에 들어가지 않는다.**

---

## 3. 발송 번들 정체 — 해제조건 2

문서가 인용하는 계산은 **정확히 이 두 파일**이다. 다른 번들(v9 의 40잡 등)은 이 문서와 무관하다.

| | `sdcp_stageA_v13.zip` | `sdcp_stageA_holdout_v4.zip` |
|---|---|---|
| ZIP sha256 | `3184de59706eddbb9d02a1143dae3df6e0912c81dcce931caf3413637bcc3147` | `892dc8699d9eb82540ace4535f2d61b1d7d3bc8ffc1d7141514aa467a19c5b74` |
| MANIFEST sha256 | `c5517f9e00604498ec5cb6586202ef3b9c4abad82b41a8a08c8b9295cd8be4b8` | `3daf5410c05bc5083af10233b9812a9bf52cb504f6e09af4a33c9da4da8f2e0b` |
| `candidate_set` | `calibration_pilot` (frozen `94675e66e02c855a`) | `holdout_stratified` (frozen `3e3ce4820c4df3ec`) |
| 잡 수 | **24** | **18** |
| 내역 | complex 16 (자세 8 × seed 2) + 기준계 8 | complex 16 (자세 16 × pm1) + clean-slab 대조 2 |
| D3-off 쌍둥이 | **0** — C3 는 D3-on OUTCAR 의 `Edisp` 로 낸다 | **0** |
| clean_slab sha | `d5f18feb15701f3fc932a1c8f64a09ed48c39ca270d8d8a8f5339658b6c43676` | 동일 |
| repo commit | `27d968c70ddc180b562da1bb19b8423dde443860` | 동일 |

**합계 42잡.** v8 이 적었던 "40잡" 은 옛 구성(24 D3-on + 16 D3-off)의 산술이었고, 그 16 을 지운
지금은 그 수도 함께 사라졌다.

**실행환경 기준 일정** (`tools/sdcp/vasp_cost_estimate.py`, baseline = 192원자·NKPTS 4·48코어·525 s/전자스텝):

| | v13 | holdout | 합 |
|---|---:|---:|---:|
| 코어/잡 | 256 | 256 | — |
| baseline(48코어) 대비 속도향상 모형 | 4.91× | 4.91× | — |
| 총 wall (직렬 환산) | 365.1 h | 334.3 h | 699.4 h |
| core-h | 93 477 | 85 591 | 179 068 |
| **최장 단일 잡** | **44.8 h** | 19.2 h | — |
| makespan @ 동시 8 | 2.37 d | 2.21 d | **≈ 4.6 d** |

> ⚠ 이 수치는 벤치마크가 아니라 두 구간 어림 모형이다. 속도향상 ±50 %, 잡 시간 자체 ±2배 —
> 곱하면 넓다. **외주처에 확인이 필요한 것**: 최대 동시 실행 수, 큐 wall-time 상한(44.8 h 잡이 있다),
> 사이트 PP allowlist.

**현재 상태**: 두 번들 모두 `✅ 제출 가능` (입력 preflight 0건) — 다만 **VASP 는 아직 한 잡도 안 돌았다.**

---

## 4. Methods — DFT 절 (영문 교체안)

> ⚠ **삽입 조건.** 아래 문단은 §2-3 의 게이트 다섯이 통과한 뒤에 넣는다. 그 전까지 이 문단의
> 과거형 서술(`were carried out`, `were recorded`)은 **참이 아니다** — 등록된 프로토콜이지 완료된 결과가 아니다.
> 게이트가 막히면 문단 전체가 바뀌지 문장 하나가 바뀌는 것이 아니다.

> **DFT calculations.** Spin-polarised DFT calculations were carried out with VASP using
> projector augmented-wave potentials and the Perdew–Burke–Ernzerhof functional, with
> Grimme's D3 dispersion correction in the zero-damping form (IVDW = 11) and a rotationally
> invariant Dudarev +U correction of U − J = 6.2 eV applied to the Ni 3d states
> (LMAXMIX = 4). The plane-wave cut-off was 520 eV with an electronic convergence threshold
> of 1 × 10⁻⁶ eV, Gaussian smearing of 0.05 eV, aspherical gradient corrections within the
> PAW spheres, and real-space projection disabled. The cathode surface was represented by a
> LiNiO₂(104) Ni-rich model slab (1 × 4, four layers, 192 atoms, 18.27 × 11.51 Å in plane)
> with more than 15 Å of vacuum, a Γ-centred 3 × 4 × 1 k-mesh, and a dipole correction along
> the surface normal; this is a model surface and not an explicit NCM811 termination. The
> binder chemistries were represented by a neutral sulfonic-acid-bearing repeat-unit model of
> SDCP (C₁₁H₁₆O₆S₂) and by a perfluorodecane fragment, CF₃–(CF₂)₈–CF₃ (C₁₀F₂₂). Gas-phase
> references were computed in orthorhombic cells obtained by padding the molecular bounding
> box, 32.64 × 29.29 × 29.70 Å for the repeat-unit model and 27.26 × 27.25 × 37.87 Å for the
> perfluorodecane fragment.
>
> Adsorption configurations were pre-screened over seven surface sites and 48 molecular
> orientations with the UMA-s-1p1 machine-learned interatomic potential, relaxing the
> adsorbate together with the outermost 15 % of the slab. **The DFT energies reported here
> are static single points on those machine-learned geometries (NSW = 0) and are not DFT
> local minima.** Each selected geometry was held fixed during the DFT single-point
> calculation, and a common electronic-structure protocol was applied across the compared
> calculations; the geometries themselves differ between species and between poses.
>
> The magnetic state of the slab was **declared rather than optimised.** Each calculation
> started from a collinear antiferromagnetic arrangement of the 48 Ni sites with ±1 μB
> initial moments, in two seeded branches: a compensated branch with 24 up and 24 down sites
> (zero net starting moment), used for all reported energies, and an uncompensated branch
> with 26 up and 22 down sites (net +4 μB starting moment), used only to test the sensitivity
> of pose ordering to the magnetic starting point. The total moment was left free
> (NUPDOWN = −1) in the complexes, the clean slab and the gas-phase references alike, so that
> no species was constrained relative to another. These labels denote initial moment
> assignments, not converged magnetic states: realised site-projected moments were recorded
> for every calculation, and energies were differenced only between calculations that realised
> the same magnetic configuration.
>
> Adsorption energies were obtained as
>
>     E_ads = E_slab+adsorbate − E_slab − E_adsorbate                (1)
>
> **Limitations.** These are vacuum, 0 K, single-molecule quantities evaluated on fixed,
> machine-learned geometries. They are not adhesion energies, interfacial resistances, or
> coverage-dependent quantities, and the two adsorbates are molecular fragments rather than
> polymers — a real polymer chain contacts the surface at many points simultaneously. Total
> energies are code- and pseudopotential-specific and are meaningful only as internal
> differences within this study. The reported comparison is conditional on the compensated
> magnetic branch and on the finite set of poses examined; it is not a global minimum over
> adsorption configurations. The spectroscopic evidence indicates that the as-synthesised
> SDCP is self-doped, whereas the adsorption model is the neutral repeat unit; the spin
> distribution of the doped state is moreover chain-length dependent, being side-group
> dominated in the monomer and backbone dominated for interior doping at n = 3.

**v8 대비 바뀐 문장 다섯** (설명형):

1. `NCM811 surface was represented by a LiNiO₂(104) slab` → **model surface** 로 명시.
   실제 NCM811 종단이 아니다. 재검토 Q7.
2. `sulfonate-functionalised EDOT repeat unit` → **neutral sulfonic-acid-bearing repeat-unit model**.
   "sulfonate" 는 이온화된 상태를 함의하는데 우리 모델은 중성 술폰산이다.
3. `PTFE C₁₀F₂₂ segment` → **perfluorodecane fragment, CF₃–(CF₂)₈–CF₃**. PTFE 라는 고분자 이름을
   조각에 붙이지 않는다.
4. `cubic boxes with 20 and 24 Å of padding` → **orthorhombic 실측 치수**. 실제 셀은 정육면체가
   아니라 분자 외형에 padding 을 더한 직육면체다 (POSCAR 실측).
5. `identical fixed geometries … for every species` → **삭제**. 물리적으로 불가능한 문장이었다.
   공통인 것은 기하가 아니라 **DFT 프로토콜**이다. 재검토 제안 문장을 그대로 썼다.

**새로 들어간 문장 둘**: 자기 두 분기(24/24 · 26/22)의 구분, 그리고 seed 이름 ≠ 수렴된 자기상태.

---

## 5. Table S1 — DFT 파라미터 (전면 교체)

| Category | Parameter | Value | Unit |
|---|---|---|---|
| Method | Code | VASP `[___]` (version) | – |
| | Functional | PBE (GGA = PE) | – |
| | Dispersion | Grimme D3, zero damping, IVDW = 11 | – |
| | Hubbard correction | Dudarev, U − J = 6.2 on Ni 3d; LMAXMIX = 4 | eV |
| | Plane-wave cut-off | 520 | eV |
| | Electronic convergence | 1 × 10⁻⁶ | eV |
| | Smearing | Gaussian, 0.05 | eV |
| | Aspherical PAW gradients | on (LASPH = .TRUE.) | – |
| | Real-space projection | off (LREAL = .FALSE.) | – |
| | k-point mesh | 3 × 4 × 1 Γ-centred (slab); Γ only (molecule) | – |
| Pseudopotentials | PAW dataset release | `[___]` | – |
| | Variants used | Li_sv, Ni_pv, O, C, F, H, S | – |
| | Provenance | per-job TITEL and SHA-256 recorded in `POTCAR_PROVENANCE.json` | – |
| Surface model | Slab | LiNiO₂(104) model surface, 1 × 4, four layers, 192 atoms (Li₄₈Ni₄₈O₉₆) | – |
| | Cell (in-plane) | 18.27 × 11.51 | Å |
| | Vacuum / adsorbate–image separation | > 15 | Å |
| | Dipole correction | along surface normal (LDIPOL = .TRUE., IDIPOL = 3) | – |
| Magnetic state | Starting branch — reported | collinear AFM, 24 ↑ / 24 ↓ Ni, ±1 μB (net 0) | – |
| | Starting branch — sensitivity only | collinear AFM, 26 ↑ / 22 ↓ Ni, ±1 μB (net +4 μB) | – |
| | Total-moment constraint | none (NUPDOWN = −1) for complexes, slab and gas references alike | – |
| | Reported | realised site-projected moments per calculation | μB |
| Geometry | Source | UMA-s-1p1 relaxation, outer 15 % of slab free | – |
| | DFT treatment | static single point, NSW = 0 — **not a DFT minimum** | – |
| Adsorbate | Neutral repeat-unit model (SDCP) | C₁₁H₁₆O₆S₂ | – |
| | Perfluorodecane fragment | C₁₀F₂₂, CF₃–(CF₂)₈–CF₃ | – |
| | Gas-phase cell — repeat-unit model | orthorhombic, 32.64 × 29.29 × 29.70 | Å |
| | Gas-phase cell — perfluorodecane | orthorhombic, 27.26 × 27.25 × 37.87 | Å |
| | Reference energy, 20 Å vs 24 Å padding | `[___]` | meV |
| Configuration search | Potential; sites / orientations | UMA-s-1p1; 7 / 48 | – |
| | Poses evaluated by DFT, per species | 12 (4 pre-registered + 8 stratified holdout) | – |
| Adsorption energy | Definition | Equation (1) | eV |
| Execution | Cores per job / max concurrency | 256 / 8 | – |
| | Site | `[___]` | – |

**v8 표에서 바뀐 것:**

- **PAW dataset release · Variants · Provenance 3행 신설.** v8 은 "공란 없음" 이라고 썼는데
  VASP 버전도 PAW release 도 없었다. 그래서 그 주장이 과장이었다.
- **자기 시작상태를 두 분기로.** v8 은 24/24 하나만 적어서 net4 분기를 감췄다.
- **기체 셀을 실측 orthorhombic 치수로.** `cubic … 20 and 24 Å padding` 은 오기였다.
- **`ΔE = 0.3 meV` 삭제.** 그 값은 legacy box 진단이지 이 프로토콜(자유 스핀 · LREAL=.FALSE.)의
  회수값이 아니다. box20/box24 대조는 이번 번들에 들어 있으므로, **회수 후** 실측값으로 다시 적는다.
- **DFT 평가 자세 수(12) · 실행 규격 행 추가.**

---

## 6. 본문 ¶34 — 교체안 (영문)

⛔ **삭제할 문장** (v6 원문):
*"The stronger interaction expected for SDCP originates from its polar sulfonate moieties, which can
interact more effectively with exposed surface sites of NCM811 than non-polar PTFE."*
— 우리 마감 문서의 **금지 서술**이다. 근거였던 `O···Li 2.09 Å` 는 2026-08-29 철회됐고(실측 4.88–5.39 Å),
평가된 기하의 실제 최근접 접촉은 **C–H ··· 표면 O/Ni 2.44 Å** 다. ⚠ 이 두 거리는 **legacy wave1 기하의
재판독**이지 새 prospective 후보 집합의 결과가 아니다 — 본문에 넣을 값이 아니라 삭제 근거일 뿐이다.

⛔ **자리표시자 삭제**: *"Additional text related to DFT."*

**교체안:**

> To evaluate a model-level contrast without assigning a functional-group mechanism, we compared a
> neutral sulfonic-acid-bearing repeat-unit model of SDCP with a perfluorodecane fragment on a
> LiNiO₂(104) Ni-rich model surface (Figure 2e), with the computational model and parameters given
> in Figure S3 and Table S1. For each species the adsorption geometry was selected by a
> machine-learned potential over seven surface sites and 48 orientations, and twelve poses per
> species — four pre-registered and eight drawn from a stratified prospective holdout — were then
> evaluated by DFT as static single points at fixed geometry under a common electronic-structure
> protocol. **[NUMBER SENTENCE]** The calculations describe an isolated repeat unit on a clean,
> vacuum-terminated surface at 0 K, on machine-learned rather than DFT-relaxed geometries, and are
> therefore a model-level comparison rather than a statement about the adhesion of the processed
> electrode or about the polymers themselves.

### `[NUMBER SENTENCE]` — 방향까지 빈칸이다

회수 전에 부호를 적지 않는다. 아래 **한 문장**이 정본이고, 빈칸 둘을 채운다.

> *"Across the twelve poses examined for each species, the lowest adsorption energies of the two
> models differed by `[___]` eV, the lower value being that of the `[___]`; none of the eight
> holdout poses fell more than 30 meV below the lowest of the four pre-registered poses."*

세 분기 중 하나가 실현된다 — **어느 것인지는 결과가 정한다**:

| 분기 | 조건 | 본문 |
|---|---|---|
| **A** | 게이트 5 통과 · 반복단위 모델이 낮음 | 위 문장, 둘째 빈칸 = `neutral repeat-unit model` |
| **B** | 게이트 5 통과 · perfluorodecane 이 낮음 | 위 문장, 둘째 빈칸 = `perfluorodecane fragment` |
| **C** | 게이트 하나라도 실패 (특히 H1) | 숫자 문장을 **넣지 않는다.** 대신: *"Under the pre-registered acceptance criteria the pose-selection assumption was not satisfied, and no pose-resolved energy comparison is quoted (Supporting Information)."* |

⛔ 그 문장에 **붙이면 안 되는 것**: "전역 최소" · "가장 안정한 자세" · "적어도 X eV" · "항상" ·
자리 선호(Li vs Ni — 판정 바닥 30 meV 아래라 미해결) · 술포네이트 기전 · `ΔΔE_lowE`/`primary` 라는 이름 ·
`binder chemistry` · `affinity` · `binding strength`.

---

## 7. 캡션 — 교체안 (영문)

대표성 한계를 **Methods 한 문단에만** 두면 오독을 못 막는다는 지적(Q7)에 따라 캡션에도 직접 넣는다.

| 위치 | 교체안 |
|---|---|
| Figure 2(e) | *"Model-level adsorption comparison: a neutral sulfonic-acid-bearing repeat-unit model of SDCP and a perfluorodecane fragment on a LiNiO₂(104) Ni-rich model surface, evaluated by DFT as static single points on machine-learned geometries. The models are molecular fragments and a model surface, not the processed polymers or an explicit NCM811 termination."* |
| Figure S3 | *"Computational models used for the DFT calculations: the LiNiO₂(104) model slab, the neutral SDCP repeat-unit model (C₁₁H₁₆O₆S₂) and the perfluorodecane fragment (C₁₀F₂₂), with the adsorption geometry of each species."* |

**Results 에 한 문장 추가** (Figure 2e 를 처음 부르는 문장 뒤):
> *"Both adsorbates are molecular fragments and the surface is a stoichiometric LiNiO₂(104) model
> rather than an explicit NCM811 termination, so the comparison is model-level."*

---

## 8. 이 판으로도 못 하는 것

| # | 무엇 | 왜 |
|---|---|---|
| 1 | 사전등록 primary `ΔΔE_lowE` | Stage B(창 W 전수 + audit 개봉) 없이는 정의되지 않는다 |
| 2 | "어느 조각이 더 강하게 붙는다" 종결형 | audit pose 0개 · 표본 조건부. `ΔΔE_obs` 는 조사한 12자세 안의 진술이다 |
| 3 | 자리 선호(Li vs Ni) 방향 | matched pose n ≥ 3 미충족 |
| 4 | legacy(wave1) 값과 혼합 | clean slab 이 다르다 (`daf71160` vs `d5f18feb`) — 평균·혼합·좋은 쪽 선택 전부 금지 |
| 5 | "재현 가능한 동결 기하" | `d5f18feb` 가 `daf71160` 과 달라진 원인을 아직 확인 못 했다 (P0-5, 미해결인 채로 던진다). 조각 간 대비는 **두 조각이 같은 슬랩**이므로 대수적으로 성립한다 |
| 6 | UMA 절대값 인용 · UMA 로 조각 간 비교 | rigid·relax 둘 다 DFT 와 부호가 반대다 |
| 7 | `sealed_audit` 2자세 | 열지 않는다. `ΔΔE_obs` 는 그것 없이 성립한다 |

---

## 9. 자리표시자 규약 — 해제조건 8

v8 은 `[A]` 라고 설명해 놓고 실제 표기는 `[___]` 였다. **`[___]` 하나로 통일한다.** 전수:

| 위치 | 빈칸 | 무엇이 채우나 | 언제 |
|---|---|---|---|
| §5 Table S1 | VASP version | 외주처 실행 로그 (`OUTCAR` 머리) | 회수 시 |
| §5 Table S1 | PAW dataset release | 외주처 POTCAR 세트 (`POTCAR_PROVENANCE.json`) | 회수 시 |
| §5 Table S1 | Site | 외주처 지정 | 제출 시 |
| §5 Table S1 | box20/box24 대조 ΔE | 이번 번들 기체 기준계 4잡 | 회수 시 |
| §6 NUMBER SENTENCE | `[___]` eV | `ΔΔE_obs` (C5, 게이트 5 통과 시) | 회수 + 게이트 |
| §6 NUMBER SENTENCE | `[___]` 조각 이름 | 같은 계산의 부호 | 회수 + 게이트 |

**조판**: 이 판의 표는 한 행이 페이지를 넘지 않도록 §5 를 두 덩이(Method/Pseudopotentials/Surface,
Magnetic/Geometry/Adsorbate/Search/Execution)로 나눠 조판한다. 한국어 본문은 페이지 경계에서
단어가 갈라지지 않게 문단 단위로 배치한다.

---

## 10. 근거 — commit · 파일 계보

| 무엇 | 어디 |
|---|---|
| 이 판의 전신 | `docs/manuscripts/methods_and_tables_v8_for_coauthors.md` (NO-GO, 2026-08-30) |
| 닫힘 조건 (C1–C5) | `db/properties/sdcp_stageA_closure_conditions_2026_08_29.json` |
| C5 결정 등재 (⚠ proposed) | `db/governance/decisions.json` → `D-2026-08-30-sdcp-neutral-ptfe-ddE-obs` |
| 사전등록 게이트 1–6 | `db/properties/prereg_sdcp_neutral_contrast_2026_08_29.json` |
| calibration 자세 동결 | `db/properties/prospective_basins_2026_08_29.json` (`94675e66e02c855a`) |
| 홀드아웃 자세 동결 | `db/properties/prospective_holdout_2026_08_30.json` (`3e3ce4820c4df3ec`) |
| 번들 생성기 | `tools/sdcp/vasp_handoff_bundle.py` @ `27d968c7` |
| 발송 후보 실물 + SHA | `runs/sdcp_stageA_2026_08_30/IDENTITY.json` |
| 파라미터 실측 출처 | 두 zip 안의 `MANIFEST.json` · `static/INCAR` · `POSCAR` (문서의 모든 수치는 여기서 읽었다) |

**v8 → v9 변경 요지 한 줄**: 범위를 DFT 로 좁히고, Stage A 를 calibration 으로 되돌리고,
인용 가능한 양을 `ΔΔE_obs` 로 따로 정의하고, 방향을 빈칸으로 만들었다.

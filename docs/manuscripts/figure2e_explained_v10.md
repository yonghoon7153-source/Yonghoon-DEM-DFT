# Figure 2e 계산 — 무엇을 왜 재는가

**공저자·신규 참여자용 설명서 · 2026-08-30 · v10**

> **이 문서를 읽는 법.**
> **1부**만 읽으면 무슨 계산인지, 왜 아직 숫자가 없는지 안다. DFT를 처음 보는 사람 기준으로 썼다.
> **2부**는 원고에 그대로 붙일 영문 문장이다. **3부**는 검증 세부라 필요한 사람만 보면 된다.
>
> ⚠ **아직 투고용이 아니다.** 이 계산은 2026-08-30 현재 **한 잡도 돌지 않았다.**
> 2부의 과거형 문장들은 계획된 프로토콜이지 완료된 결과가 아니다.

---

# 1부 — 배경

## 1-1. 이 계산이 원고 어디에 들어가나

원고의 이야기는 "SDCP라는 바인더를 넣으면 복합 양극이 좋아진다"이다. 그 이야기에는 두 갈래 근거가 있다.

| 갈래 | 무엇을 보이나 | 어디 |
|---|---|---|
| 구조·수송 (DEM/MPM) | SDCP를 넣으면 전자 전도 경로가 촘촘해진다 | Figure 4, Table S3 |
| **분자 수준 (DFT)** | **SDCP 조각이 활물질 표면과 어떻게 상호작용하나** | **Figure 2e, Table S1, 본문 ¶34** |

이 문서는 **아래 줄 하나**를 다룬다. Figure 2e는 패널 하나이고, 거기 들어갈 숫자를 만드는 것이 전부다.

## 1-2. 흡착에너지란 무엇인가

분자가 표면에 붙는 것이 에너지적으로 유리한지를 재는 양이다. 정의는 뺄셈 하나다.

```
E_ads  =  E(표면 + 분자)  −  E(표면)  −  E(분자)
```

- `E(표면 + 분자)` — 분자가 표면에 앉아 있는 계의 전체 에너지
- `E(표면)` — 분자 없이 표면만
- `E(분자)` — 표면 없이 분자만, 넓은 빈 상자 안에 (기체 상태)

**세 계산이 다 있어야 한 숫자가 나온다.** 값이 음수면 붙는 쪽이 유리하다는 뜻이고, 더 음수일수록 더 세게 붙는다.

우리가 답하려는 건 이거다 — **SDCP 조각과 PTFE 조각 중 어느 쪽이 더 음수인가.**

## 1-3. 왜 이게 오래 걸리나 — 이 계가 까다로운 이유 셋

같은 종류의 계산을 다른 논문들은 몇 주에 끝낸다. 우리가 오래 걸리는 이유는 셋이고, 셋 다 실제로 값을 바꾼다.

### ① 표면이 자석이다

활물질은 니켈이 많은 층상 산화물이다. 니켈은 **홀전자**를 가져서 자기 모멘트가 있고, 48개 니켈이 위/아래 스핀으로 어떻게 배열되느냐에 따라 계의 에너지가 갈린다. 배열이 다르면 **다른 계**다.

문제는 뺄셈이다. `E(표면+분자)`와 `E(표면)`이 서로 **다른 자기 배열**로 수렴하면, 뺄셈 결과에 흡착과 무관한 자기 배열 차이가 섞여 들어간다. 이 캠페인이 실제로 그렇게 한 번 물렸다 — 기준계는 자화를 강제로 고정해 놓고 복합체는 자유롭게 풀어서 뺐다. 그건 흡착에너지가 아니다.

그래서 지금은 **계산이 끝난 뒤 실제로 어떤 자기 배열로 수렴했는지 읽고, 같은 배열끼리만 뺀다.**

### ② 분자를 어디에 어떻게 놓느냐에 따라 값이 달라진다

분자를 표면 위에 놓는 방법은 무한하다. 어느 자리 위에, 어느 각도로, 어느 높이로. 각각을 **자세(pose)** 라고 부른다.

자세마다 E_ads가 다르다. 그래서 "SDCP의 흡착에너지"라는 단일한 값은 사실 존재하지 않는다. 있는 것은 **"우리가 본 자세들 중 최저값"** 이다. 이 구분이 이 프로젝트에서 계속 문제가 됐다.

### ③ 셀 설정이 값에 들어간다

DFT 계산은 상자를 무한히 반복해서 푼다(주기 경계). 표면 계산에서는 상자 위쪽에 **진공**을 충분히 둬서, 분자가 위쪽에 있는 "다음 표면"과 상호작용하지 않게 해야 한다.

⚠ **바로 여기서 이번에 결함이 나왔다** — 1-6에서 다룬다.

## 1-4. 이단 전략 — ML 퍼텐셜로 고르고, DFT로 잰다

자세가 문제라면 자세를 많이 봐야 한다. 그런데 DFT는 비싸다 — 이 계 한 자세가 256코어로 **20~45시간**이다. 우리가 훑고 싶은 자세는 7자리 × 48배향 = **336개**다. 전부 DFT로 돌면 수개월이다.

그래서 두 단계로 나눈다.

| 단계 | 도구 | 무엇 | 비용 |
|---|---|---|---|
| 1 | **UMA-s-1p1** (기계학습 퍼텐셜) | 336자세를 전부 훑고 이완시킨다 | 몇 시간 |
| 2 | **VASP** (DFT) | 그중 **12자세만** 골라 정확히 잰다 | 며칠 |

**대가가 있다.** DFT가 보는 기하는 UMA가 이완시킨 것이지 DFT 자신의 최소점이 아니다. 그래서 우리 값은 엄밀히 말하면 **"UMA 기하 위의 고정기하 단일점 에너지"** 이고, 원고에 그렇게 적어야 한다. "DFT로 최적화한 흡착에너지"라고 부르면 거짓이다.

> **용어**: *단일점(single point)* = 원자를 안 움직이고 그 배치에서 전자 구조만 푸는 계산.
> *이완(relaxation)* = 힘이 0이 될 때까지 원자를 움직이는 계산. 우리는 1단계에서만 이완한다.

## 1-5. 자세를 고른 놈이 답을 정하면 안 된다 — 홀드아웃

여기가 이 프로젝트에서 제일 신경 쓴 부분이다.

UMA가 336자세 중 좋아 보이는 것을 골라 주고, 우리는 그것만 DFT로 잰다. 그런데 **UMA가 틀렸으면?** UMA가 SDCP 쪽 좋은 자세는 잘 찾고 PTFE 쪽은 못 찾았다면, DFT 결과는 "SDCP가 더 잘 붙는다"고 나오지만 그건 **선택기의 편향**이지 물리가 아니다.

이걸 시험하려고 자세를 두 묶음으로 나눴다.

| 묶음 | 몇 개 | 어떻게 골랐나 | 역할 |
|---|---|---|---|
| **calibration** | 조각당 4 | UMA가 가장 좋다고 한 것들 | 값을 만든다 |
| **holdout** | 조각당 8 | UMA 점수 **사분위별로 2개씩**, 표면 접촉 원소가 서로 다르게 | **선택기를 시험한다** |

홀드아웃 8자세는 UMA 점수 전 구간에 걸쳐 있다 — 좋다고 한 것부터 나쁘다고 한 것까지. 그리고 **결과를 보기 전에 목록을 동결했다** (해시 `3e3ce482…`).

시험은 이렇다:

> **홀드아웃 자세 중 하나라도 calibration 최저보다 30 meV 이상 더 낮게 나오면,
> UMA의 순위가 틀렸다는 뜻이다.** 그러면 그 값을 "더 좋은 자세를 찾았다"고 흡수하지 않고,
> **선택기 실패로 판정하고 멈춘다.**

이게 중요한 이유: 흡수해 버리면 선택기가 틀렸다는 증거가 사라지고, 그냥 더 낮은 숫자만 남는다.

세 갈래로 갈린다.

| 홀드아웃 최저 − calibration 최저 | 판정 |
|---|---|
| **+30 meV 초과** (홀드아웃이 확실히 높다) | 선택기가 버텼다 → 값을 쓴다 |
| **−30 ~ +30 meV** (구분 안 됨) | **미해결** — 판정 해상도 안이라 어느 쪽도 말 못 한다 |
| **−30 meV 미만** (홀드아웃이 더 낮다) | **선택기 실패** — 값을 쓰지 않는다 |

가운데 칸이 중요하다. 종전 문서는 이 구간을 통과로 처리했는데, 그건 미해결을 성공으로 승격시키는 것이라 틀렸다.

## 1-6. ⚠ 2026-08-30에 발견된 결함 — 진공이 모자랐다

1-3 ③에서 말한 그 문제가 실제로 터졌다.

만들어 둔 자세들의 셀 높이는 30.26 Å이다. 그 안에 4층 슬랩이 들어가고, 남는 위쪽이 진공이다. 그런데 분자가 누워 있는지 서 있는지에 따라 남는 진공이 달라진다.

실측:

| | 값 |
|---|---|
| 검사한 자세 | 24 |
| 진공 15 Å 미만 | **9개** |
| 최악 (PTFE `b74`) | **8.63 Å** — 분자 F가 다음 주기 슬랩 O에서 8.63 Å |

그런데 우리 문서·Methods·Table S1은 전부 **">15 Å"** 라고 적고 있었다. **거짓이었다.**

왜 안 걸렸나 — **번들 생성기에 진공을 재는 코드가 한 줄도 없었다.** 검사는 원자 구성·역할 라벨만 봤다.

8.6 Å이 왜 문제인가: 우리가 쓰는 분산력 보정(D3)은 원자쌍 사이 거리로 계산되는 항이라, 8.6 Å 떨어진 다음 주기 슬랩과도 계속 상호작용한다. 쌍극자 보정(LDIPOL)은 정전기만 다루지 이걸 지우지 못한다.

**고친 방법**: 셀 높이를 늘려서 모든 자세가 15 Å 이상이 되게 한다. 원자 좌표는 그대로 두고 상자만 키운다.

| | 이전 | 이후 |
|---|---|---|
| 셀 높이 c | 30.26 Å | **36.66 Å** |
| 최소 진공 | 8.63 Å | **15.00 Å** |
| 셀 부피 | — | **+21 %** |

그리고 이제 생성기가 **미달이면 번들을 아예 안 만든다.** 문장이 아니라 게이트다.

## 1-7. 지금 상태 — 왜 아직 숫자가 없나

| | 상태 |
|---|---|
| 자세 선정 (UMA) | ✅ 끝 — 336자세 훑고 12자세/조각 동결 |
| 계산 묶음 생성 | 🔄 재생성 필요 (진공 결함) |
| **VASP 계산** | ⛔ **0잡** — 한 번도 안 돌았다 |
| 값 | ⛔ 없음 |

숫자가 없는 이유는 계산이 어려워서가 아니라 **아직 안 돌렸기 때문이다.** 돌리면 42잡 · 동시 8개 기준 약 5~6일이다.

## 1-8. 이 계산이 **말할 수 없는** 것

원고에 쓰기 전에 이 목록을 알아야 한다.

| 못 하는 것 | 왜 |
|---|---|
| "SDCP가 PTFE보다 항상 잘 붙는다" | 자세 12개만 봤다. 전역 최소가 아니다 |
| "술폰기가 표면을 붙잡는다" | 자세 집합이 그걸 시험하도록 설계되지 않았다 |
| 실제 전극의 접착력 | 진공·0 K·분자 하나. 접착은 다중 접촉·용매·온도의 문제다 |
| 고분자의 성질 | 우리 모델은 **반복단위 하나**와 **탄소 10개짜리 조각**이다 |
| 다른 논문 값과의 직접 비교 | 총에너지는 코드·유사퍼텐셜에 따라 다르다. 내부 차이만 유효하다 |
| 자리 선호 (Li 위 vs Ni 위) | 짝지은 자세가 3개 미만이라 판정 불가 |

---

# 2부 — 원고에 들어갈 문장

> ⚠ **삽입 조건**: 3부의 게이트가 전부 통과한 뒤에만 넣는다. 그 전까지 아래 과거형은 참이 아니다.

## 2-1. Methods — DFT 절

> **DFT calculations.** Spin-polarised DFT calculations were carried out with VASP using
> projector augmented-wave potentials and the Perdew–Burke–Ernzerhof functional, with
> Grimme's D3 dispersion correction in the zero-damping form (IVDW = 11) and a rotationally
> invariant Dudarev +U correction of U − J = 6.2 eV applied to the Ni 3d states
> (LMAXMIX = 4). The plane-wave cut-off was 520 eV (PREC = Accurate, ADDGRID = .TRUE.)
> with an electronic convergence threshold of 1 × 10⁻⁶ eV, Gaussian smearing of 0.05 eV,
> aspherical gradient corrections within the PAW spheres, real-space projection disabled,
> and symmetry switched off (ISYM = 0); each calculation was started from superposed atomic
> charge densities (ISTART = 0, ICHARG = 2). Reported energies are the extrapolated
> `energy(sigma→0)` values, not the finite-smearing free energies.
>
> The cathode surface was represented by a stoichiometric LiNiO₂(104) slab used as a proxy
> for a Ni-rich layered oxide (1 × 4, four layers, 192 atoms, Li₄₈Ni₄₈O₉₆, 18.27 × 11.51 Å
> in plane, cell height 36.66 Å), with a Γ-centred 3 × 4 × 1 k-mesh and a dipole correction
> along the surface normal (LDIPOL = .TRUE., IDIPOL = 3). Every adsorbate configuration was
> constructed so that the shortest distance between the adsorbate and the periodic image of
> the slab was at least 15 Å. The binder chemistries were represented by a neutral
> sulfonic-acid-bearing repeat-unit model of SDCP (C₁₁H₁₆O₆S₂) and by a perfluorodecane
> fragment, CF₃–(CF₂)₈–CF₃ (C₁₀F₂₂). Gas-phase references were single-point calculations on
> the same fragment conformers used to build the adsorbate configurations, in orthorhombic
> cells obtained by padding the molecular bounding box (IDIPOL = 4).
>
> Adsorption configurations were pre-screened over seven surface sites and 48 molecular
> orientations with the UMA-s-1p1 machine-learned interatomic potential, relaxing the
> adsorbate together with the outermost 15 % of the slab. **The DFT energies reported here
> are static single points on those machine-learned geometries (NSW = 0) and are not DFT
> local minima.** Each selected geometry was held fixed during the DFT single-point
> calculation, and a common electronic-structure protocol was applied across the compared
> calculations; the geometries themselves differ between species and between poses, so the
> reported values include the adsorbate and slab deformation of each pose.
>
> Calibration complexes were initialised from two magnetic seeds — a compensated
> arrangement of the 48 Ni sites (24 up, 24 down, ±1 μB) and an uncompensated one
> (26 up, 22 down) — whereas holdout complexes were evaluated only on the prespecified
> compensated branch. Total magnetisation was unconstrained (NUPDOWN = −1) in the
> complexes, the clean slab and the gas-phase references alike; the converged local-moment
> pattern was classified post hoc, and energies were differenced only between calculations
> that realised the same magnetic configuration.
>
> Adsorption energies were obtained as
>
>     E_ads = E_slab+adsorbate − E_slab − E_adsorbate                (1)
>
> **Limitations.** These are vacuum, 0 K, single-molecule quantities evaluated on fixed,
> machine-learned geometries at a single coverage; the coverage dependence was not
> examined. They are not adhesion energies or interfacial resistances, and the two
> adsorbates are molecular fragments rather than polymers — a real polymer chain contacts
> the surface at many points simultaneously. Total energies are code- and
> pseudopotential-specific and are meaningful only as internal differences within this
> study. The reported comparison is conditional on the compensated magnetic branch and on
> the finite set of poses examined; it is not a global minimum over adsorption
> configurations. The spectroscopic evidence indicates that the as-synthesised SDCP is
> self-doped, whereas the adsorption model is the neutral repeat unit.

## 2-2. 본문 ¶34

⛔ **삭제할 문장** (v6 원문): *"The stronger interaction expected for SDCP originates from
its polar sulfonate moieties, which can interact more effectively with exposed surface sites
of NCM811 than non-polar PTFE."* — 근거였던 `O···Li 2.09 Å`는 2026-08-29 철회됐다
(재측정 4.88–5.39 Å). 자리표시자 *"Additional text related to DFT."* 도 지운다.

> To evaluate a model-level contrast without assigning a functional-group mechanism, we
> compared a neutral sulfonic-acid-bearing repeat-unit model of SDCP with a perfluorodecane
> fragment on a stoichiometric LiNiO₂(104) model surface (Figure 2e), with the computational
> model and parameters given in Figure S3 and Table S1. For each species the adsorption
> geometry was selected by a machine-learned potential over seven surface sites and 48
> orientations, and twelve poses per species — four pre-registered and eight drawn from a
> stratified prospective holdout — were then evaluated by DFT as static single points at
> fixed geometry under a common electronic-structure protocol. **[숫자 문장]** The
> calculations describe an isolated repeat unit on a clean, vacuum-terminated surface at
> 0 K, on machine-learned rather than DFT-relaxed geometries, and are therefore a
> model-level comparison rather than a statement about the adhesion of the processed
> electrode or about the polymers themselves.

### `[숫자 문장]` — 방향까지 빈칸이다

결과를 보기 전에 부호를 쓰지 않는다. 빈칸 둘을 채운다.

> *"Across the twelve poses examined for each species, the lowest adsorption energies of the
> two models differed by `[___]` eV, the lower value being that of the `[___]`; none of the
> eight holdout poses fell more than 30 meV below the lowest of the four pre-registered
> poses."*

- 첫 빈칸 = **차이의 절댓값**
- 둘째 빈칸 = 그 부호가 정하는 조각 이름 (`neutral repeat-unit model` 또는 `perfluorodecane fragment`)

**게이트가 막히면 이 문장을 넣지 않는다.** 대신:
> *"Under the pre-registered acceptance criteria the pose-selection assumption was not
> satisfied, and no pose-resolved energy comparison is quoted (Supporting Information)."*

⛔ 붙이면 안 되는 것: "전역 최소" · "가장 안정한 자세" · "적어도 X eV" · "항상" ·
자리 선호 · 술포네이트 기전 · `binder chemistry` · `affinity` · `binding strength`.

## 2-3. Table S1 — DFT 파라미터

| Category | Parameter | Value | Unit |
|---|---|---|---|
| Method | Code | VASP `[___]` (version) | – |
| | Functional | PBE (GGA = PE) | – |
| | Dispersion | Grimme D3, zero damping, IVDW = 11 | – |
| | Hubbard correction | Dudarev, U − J = 6.2 on Ni 3d; LMAXMIX = 4 | eV |
| | Plane-wave cut-off | 520 (PREC = Accurate, ADDGRID = .TRUE.) | eV |
| | Electronic convergence | 1 × 10⁻⁶ | eV |
| | Smearing / reported energy | Gaussian 0.05; energy(sigma→0) | eV |
| | Aspherical PAW gradients | on (LASPH = .TRUE.) | – |
| | Real-space projection | off (LREAL = .FALSE.) | – |
| | Symmetry / start | ISYM = 0; ISTART = 0, ICHARG = 2; ALGO = Normal | – |
| | k-point mesh | 3 × 4 × 1 Γ-centred (slab); Γ only (molecule) | – |
| Pseudopotentials | PAW dataset release | `[___]` | – |
| | Variants used | Li_sv, Ni_pv, O, C, F, H, S | – |
| | Provenance | per-job TITEL and SHA-256 in `POTCAR_PROVENANCE.json` | – |
| Surface model | Slab | stoichiometric LiNiO₂(104) proxy, 1 × 4, four layers, 192 atoms | – |
| | Cell | 18.27 × 11.51 × 36.66 | Å |
| | Adsorbate–image separation | ≥ 15.0 (measured minimum 15.00) | Å |
| | Dipole correction | LDIPOL = .TRUE., IDIPOL = 3 (slab) / 4 (molecule) | – |
| Magnetic state | Calibration seeds | 24 ↑ / 24 ↓ (net 0) and 26 ↑ / 22 ↓ (net +4 μB) | – |
| | Holdout seed | 24 ↑ / 24 ↓ only | – |
| | Total-moment constraint | none (NUPDOWN = −1) throughout | – |
| | Reported | realised local moments, classified post hoc | μB |
| Geometry | Source | UMA-s-1p1 relaxation, outer 15 % of slab free | – |
| | DFT treatment | static single point, NSW = 0 — **not a DFT minimum** | – |
| Adsorbate | Neutral repeat-unit model (SDCP) | C₁₁H₁₆O₆S₂ | – |
| | Perfluorodecane fragment | C₁₀F₂₂, CF₃–(CF₂)₈–CF₃ | – |
| | Conformer source | same geometry as the adsorbate in the complexes | – |
| | Gas cell — repeat-unit model | orthorhombic, 32.64 × 29.29 × 29.70 | Å |
| | Gas cell — perfluorodecane | orthorhombic, 27.26 × 27.25 × 37.87 | Å |
| | 20 Å vs 24 Å padding — repeat unit | `[___]` | meV |
| | 20 Å vs 24 Å padding — perfluorodecane | `[___]` | meV |
| Configuration search | Potential; sites / orientations | UMA-s-1p1; 7 / 48 | – |
| | Poses evaluated by DFT, per species | 12 (4 pre-registered + 8 stratified holdout) | – |
| Adsorption energy | Definition | Equation (1) | eV |
| Execution | Jobs / VASP executions | 42 / 43 | – |
| | Cores per job; site | 256; `[___]` | – |

## 2-4. 캡션

| 위치 | 교체안 |
|---|---|
| Figure 2(e) | *"Model-level adsorption comparison: a neutral sulfonic-acid-bearing repeat-unit model of SDCP and a perfluorodecane fragment on a stoichiometric LiNiO₂(104) model surface, evaluated by DFT as static single points on machine-learned geometries. The models are molecular fragments and a proxy surface, not the processed polymers or an explicit NCM811 termination."* |
| Figure S3 | *"Computational models used for the DFT calculations: the LiNiO₂(104) model slab, the neutral SDCP repeat-unit model (C₁₁H₁₆O₆S₂) and the perfluorodecane fragment (C₁₀F₂₂), with the adsorption geometry of each species."* |

**Results 에 한 문장 추가** (Figure 2e를 처음 부르는 문장 뒤):
> *"Both adsorbates are molecular fragments and the surface is a stoichiometric LiNiO₂(104)
> model rather than an explicit NCM811 termination, so the comparison is model-level."*

---

# 3부 — 검증 세부 (필요한 사람만)

## 3-1. 숫자를 쓰기 전에 통과해야 하는 것

결과를 보기 전에 정해 뒀다. **하나라도 깨지면 숫자를 만들지 않는다.**

| | 게이트 | 왜 |
|---|---|---|
| ① | 조각당 12자세 **전부** 회수·수렴 | 부분집합에서 최저값을 뽑으면 표본이 줄수록 최저값이 올라간다 |
| ② | 24계산(12자세 × 2조각)이 **같은 자기 배열** | 다른 배열끼리 빼면 흡착이 아닌 것이 섞인다 |
| ③ | **홀드아웃 시험** — 1-5의 세 갈래 | 선택기 편향을 시험하는 자리 |
| ④ | 두 조각의 기체 기준이 **같은 프로토콜** | 자화 자유·실공간투영 off·같은 상자 관례 |
| ⑤ | 슬랩이 두 조각에 **같은 파일** | 해시 일치 |
| ⑥ | 두 자기 시드의 자세별 에너지차 산포 ≤ 10 meV | 시드 민감도가 크면 그 쌍을 막는다 |
| ⑦ | 두 묶음의 VASP·PAW·POTCAR가 **동일** | 다른 코드 세대의 값을 합치지 않는다 |
| ⑧ | 이 판정 규약을 **사람이 승인** | 현재 `proposed` — 미승인 |

## 3-2. 계산 묶음

계산은 두 묶음으로 나가고, 두 묶음이 **다 회수돼야** 한 숫자가 나온다.

| | calibration 묶음 | holdout 묶음 |
|---|---|---|
| 복합체 | 4자세 × 2시드 × 2조각 = 16 | 8자세 × 1시드 × 2조각 = 16 |
| 기준계 | clean 슬랩 2 + 기체 6 = 8 | clean 슬랩 2 |
| 잡 수 | 24 | 18 |

⚠ **왜 나눴나**: 합치면 홀드아웃이 사전등록 후보집합에 섞여서 "결과 보고 고른 것 아니냐"를 막을 수 없다. 나눈 대가는 clean 슬랩 2잡이다.

⚠ **왜 둘 다 필요한가**: 기체 기준은 calibration 묶음에만 있고, 12자세는 두 묶음을 합쳐야 나온다. 따라서 **두 묶음을 해시로 묶어 함께 분석**해야 하고, 그 결합 코드는 **아직 없다** — 현재 분석기는 묶음을 하나만 받는다. 이것이 지금 가장 큰 미완이다.

## 3-3. 현재 미완 목록

| # | 무엇 | 상태 |
|---|---|---|
| 1 | 두 묶음 결합 분석 (해시 결속) | ⛔ 미구현 — 이게 없으면 숫자가 나오지 않는다 |
| 2 | 진공 15 Å로 묶음 재생성 | 🔄 생성기는 고쳤다 (게이트 포함), 재생성 필요 |
| 3 | 홀드아웃 시험의 세 갈래 반영 | 🔄 코드가 아직 두 갈래다 |
| 4 | 판정 규약 사람 승인 | ⛔ `proposed` |
| 5 | POTCAR allowlist·provenance | ⛔ 미해결 |
| 6 | 빈칸 채우기 | ⛔ 계산 후 |

## 3-4. 용어 사전

| 말 | 뜻 |
|---|---|
| 슬랩(slab) | 표면을 흉내 내려고 결정을 몇 층만 잘라낸 판 |
| 자세(pose) | 분자를 표면 위에 놓은 한 가지 배치 |
| 단일점(single point) | 원자를 안 움직이고 전자 구조만 푸는 계산 |
| 이완(relaxation) | 힘이 0이 될 때까지 원자를 움직이는 계산 |
| D3 | 원자쌍 거리로 계산하는 분산력(반데르발스) 보정 |
| +U | 니켈 3d 전자의 자기상호작용을 보정하는 항 |
| 시드(seed) | 계산을 시작할 때 넣어 준 초기 자기 배열. **결과가 아니다** |
| 홀드아웃 | 결과 전에 봉인해 둔, 선택기를 시험하기 위한 자세 묶음 |
| 게이트 | 통과 못 하면 값을 만들지 않는 자동 검사 |

## 3-5. 출처

| 무엇 | 어디 |
|---|---|
| 게이트·판정 규약 | `db/properties/sdcp_stageA_closure_conditions_2026_08_29.json` |
| 판정 등재 (미승인) | `db/governance/decisions.json` |
| calibration 자세 동결 | `db/properties/prospective_basins_2026_08_29.json` |
| 홀드아웃 자세 동결 | `db/properties/prospective_holdout_2026_08_30.json` |
| 묶음 생성기 | `tools/sdcp/vasp_handoff_bundle.py` |
| 이 문서의 모든 수치 | 두 묶음의 `MANIFEST.json` · `INCAR` · `POSCAR` 실측 |

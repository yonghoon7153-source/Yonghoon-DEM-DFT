# Methods (simulation + DFT) — revision v8

**DFT · DEM 두 축을 한 문서로 — 공저자 검토용 교체안, 2026-08-30**

> **PROVISIONAL — NOT FOR SUBMISSION**
>
> v7 은 DEM 축만 다뤘다. 이 판은 **원고 본문 v6 · SI v6 를 실제로 대조해서**
> DFT 축(Table S1 · Figure 2e · Methods DFT)까지 넣었다.
>
> ⚠ **가장 큰 발견을 먼저 적는다.** 원고의 DFT 절은 **아직 안 쓰였다** —
> 본문에 `"Additional text related to DFT."`, Figure 2 캡션에 `"(e) DFT."`,
> SI 에 `"Figure S3. DFT"` 가 그대로 남아 있다. 그런데 **쓰여 있는 한 문장**
> (술포네이트가 표면과 상호작용한다)은 우리 판정에서 **금지 서술**이다.
> 즉 빈칸을 채우는 일이 아니라, **있는 문장을 빼고 빈칸을 채우는** 일이다.

---

## 0. 해제조건 — DFT 축과 DEM 축을 함께

| # | 조건 | 축 | 상태 |
|---|---|---|---|
| ① | 두 PTFE 규약을 동등한 sensitivity 두 점으로 표기 | DEM | **해소** |
| ② | 1.35 GPa 의 출처를 정확히 서술 | DEM | **해소** |
| ③ | '하한' 표현 철회 | DEM | **해소** |
| ④ | W4 32팔 원자료(축소 감사본) 리포 커밋 | DEM | **해소** (2026-08-29, `52f1cacc`) |
| ⑤ | σ_ion 행 | DEM | ⛔ **악화** — '미측정' 이 아니라 **'쟀는데 부호가 뒤집혀 못 쓴다'** |
| ⑥ | ε_union · thickness 의 연산 정의 | DEM | **해소** |
| ⑦ | Figure 4b 재작도 | DEM | **해소** (두 규약 병기) |
| ⑧ | Figure S16–S18 캡션 감사 | DEM | **해소** (`3e6aab4a`) |
| ⑨ | **구조 지표 5행** | DEM | **해소** (2026-08-29 등재) — 단 **절대값이 v6 과 5.8배 다르다** |
| ⑩ | **Table S1 이 어느 세대의 계산인가** | DFT | ⛔ **미해소** — SI 는 Quantum ESPRESSO 를 적는데 인용 후보 값은 **VASP** 산출이다 |
| ⑪ | **Eq (1) 흡착에너지 인용 자격** | DFT | ⛔ **미해소** — reference-equivalence 복구 전까지 **부등호 방향도 금지** |
| ⑫ | **Figure 2e · 본문 DFT 문단** | DFT | ⛔ **미작성** — 자리표시자 + 금지 서술 하나 |

⇒ v7 이 남긴 4건 중 3건이 닫혔고, **DFT 축에서 3건이 새로 열렸다.**

**지금 계산기에서 도는 것** (gabia, 2026-08-30 12:15 실측):

| 무엇 | 상태 |
|---|---|
| 트랙 A 슬랩 이완 (GPU, QE) | 🔄 힘 문턱 **도달**(6.6e-4 < 1e-3 Ry/bohr) · ΔE −0.2 meV · 53.6 h · ⛔ 재기동 금지 |
| band gap nscf (CPU 10팔, QE) | 🔄 진행 |
| ORCA Stage A (n=6 올리고머) | ⏹ **죽었다 — 8개 중 gs0 만** |
| 새 VASP Stage A 40잡 | ⏸ 미제출 |

---

## 1. v6/v7 대비 무엇이 바뀌나 (여섯)

| # | 종전 | v8 | 왜 바꾸는가 |
|---|---|---|---|
| 1 | Table S3 σ_ele 를 **S cm⁻¹** 로 1.98 / 3.00 | **mS cm⁻¹** 로 72.3 / 81.3 (또는 54.0 / 70.6) | 침대·격자 세대가 통째로 갈렸다. **단위가 바뀐다** — 27~40배 낮다 |
| 2 | Median CBD contacts 433 / 517 | **74 / 86** (전도성만) · **80 / 88** (절연 PTFE 포함) | v6 이 무엇을 셌는지 기록이 없다. 방향(+16 %)은 살고 **절대값은 규약과 함께** 갱신 |
| 3 | Areal capacity 3.11 / 3.07 | **n/a + 사유** | 두 전극이 **같은 AM scaffold · 같은 두께**다 ⇒ 면적용량이 다를 수 없다 |
| 4 | Porosity 7.87 / 7.39 | **ε_union 7.86 / 7.37** + 라벨 | 통상 전극 porosity 가 아니다. 실험 앵커(~15.6 %)의 절반 이하 = 과압축 |
| 5 | Table S1 = Quantum ESPRESSO | **어느 세대인지 결정 필요** | 인용 후보 값은 VASP PAW 산출이다. 두 코드의 파라미터가 표 하나에 섞여 있다 |
| 6 | "SDCP 의 극성 술포네이트가 표면과 더 잘 상호작용" | **삭제** | 우리 판정의 **금지 서술**이다 (2026-08-29 철회). 실측 접촉은 C–H ··· 표면 O/Ni 2.44 Å |

---

## 2. Methods — DFT 절 (교체안, 영문)

> ⚠ 아래는 **프로토콜 서술**이다. 결과 문장(어느 쪽이 더 세게 붙는가)은
> §8-1 이 풀리기 전까지 **쓸 수 없다** — 빈칸으로 둔다.

**DFT calculations.** Spin-polarised DFT calculations were performed with [CODE]
using the Perdew–Burke–Ernzerhof functional with Grimme's D3 dispersion correction
in the zero-damping form, and a rotationally invariant Dudarev +U correction of
U − J = 6.2 eV applied to the Ni 3d states. [BASIS/CUTOFF BLOCK — see Table S1].
Gaussian smearing of 0.05 eV was used with an electronic convergence threshold of
1 × 10⁻⁶. The NCM811 surface was represented by a LiNiO₂(104) slab (1 × 4, four
layers, 192 atoms, 18.27 × 11.51 Å in plane) with more than 15 Å of vacuum, a
Γ-centred 2 × 3 × 1 k-mesh, and a dipole correction along the surface normal.
SDCP was represented by its sulfonate-functionalised EDOT repeat unit
(C₁₁H₁₆O₆S₂) and PTFE by a C₁₀F₂₂ segment.

Adsorption configurations were pre-screened over seven surface sites and 48
molecular orientations with the UMA-s-1p1 machine-learned interatomic potential,
relaxing the adsorbate and the outermost fraction of the slab while the remainder
was held fixed. **The reported energies are single-point DFT evaluations on those
machine-learned geometries and are not DFT local minima**; the geometry is
therefore identical between the compared species only in the sense that the same
selection protocol was applied to each. The magnetic state of the slab was
**declared rather than optimised**: each complex was assigned a specified
collinear starting configuration, and the realised local-moment topology was
recorded and used to decide which pairs of calculations may be differenced.
Comparisons were formed only between calculations that realised the same
magnetic configuration.

Gas-phase references were relaxed in the same cell, with the box padding
increased from 20 to 24 Å; the resulting reference energy changed by 0.3 meV.
Adsorption energies were obtained as

    E_ads = E_slab+binder − E_slab − E_binder                (1)

**Limitations.** These are vacuum, 0 K, single-molecule quantities on a fixed,
machine-learned geometry. They are not adhesion energies, interfacial
resistances or coverage-dependent quantities, and the two fragments are
molecular segments rather than polymers — a real polymer contacts the surface
at many points. Total energies are code- and pseudopotential-specific and are
meaningful only as internal differences within this study.

---

## 3. Methods — DEM 절 (v7 의 설명형을 그대로 승계)

v7 §2 의 영문이 **그대로 유효**하다. 세 곳만 고친다:

1. `"reported as equivalent sensitivity points rather than one primary result"` →
   본문 공칭은 **centerline** 으로 정해졌다 (편집 결정). 문구:
   *"selected for reporting, but not calibrated"* 로 적고 **같은 문단에 off 값을 병기**한다.
2. 구조 지표 문장이 들어갈 자리를 만든다 (§6 Table S3 의 새 행들).
3. `"the eight phases are a complete factorial ... no standard error or confidence
   interval is implied"` — v6 본문 Methods 의 **`"the paired mean with its standard error"`**
   를 이 문장으로 **교체**해야 한다. v6 본문이 아직 옛 문구다.

⚠ **v6 본문 Methods(DEM)에 명백한 결함 셋이 더 있다** — v7 이 안 잡은 것들이다:

| 위치 | v6 원문 | 문제 |
|---|---|---|
| DEM 절 | *"Effective conductivities were obtained by rasterizing each microstructure onto a cubic grid with a voxel edge of 0.15 μm. Each microstructure was rasterized onto a cubic grid with a voxel edge of 0.15 μm."* | **같은 문장이 두 번** 있다 |
| DEM 절 | *"VGCF fibers, PTFE fibrils and SDCP particles were then seeded into the pore space"* | **틀렸다.** 이들은 압밀 **도중** material-point cloud 에 있었다 (그래서 강성이 압밀에 들어간다). "then seeded" 는 사후 삽입으로 읽힌다 |
| DEM 절 | *"which reproduces the ~10 % porosity and 11–12 % contact overlap reported for cold-pressed LPSCl at 300 MPa"* | ~10 % 는 복합·유리 문헌에서 유도한 표적이지 **순수 LPSCl 실측이 아니고**, 11–12 % 는 **우리 순수-SE 시뮬 결과**이지 실측 표적이 아니다 |

---

## 4. Table S1 — DFT 파라미터 (⛔ 먼저 결정할 것이 있다)

**결정 필요:** Figure 2e 에 실릴 숫자가 **어느 트랙**인가. 트랙이 **둘 다 살아 있다.**

| | 트랙 A — Quantum ESPRESSO | 트랙 B — VASP |
|---|---|---|
| 무엇 | Phase-B DFT+U **Δ 판정 5잡** (slab · complex_doped · complex_neutral · mol_doped · mol_neutral) | wave1 흡착 잡 (조각 2종 × 자세 × 자기 branch) |
| 지금 상태 (2026-08-30 12:15) | 🔄 **돌고 있다.** 슬랩 이완이 힘 문턱 도달(max성분 6.6e-4 < 1e-3 Ry/bohr, ΔE −0.2 meV), **Δ 판정 0/5 수렴** | ⏸ 계산은 끝났고 **인용이 보류** (reference-equivalence) |
| SI v6 Table S1 이 서술하는 것 | **이쪽이다** (60/480 Ry · 1e-6 Ry · AFM net 0) | 아니다 |
| 인용 자격 | ⛔ 아직 없다 — 5잡 중 0잡 수렴 | ⛔ 보류 — §8-1 |

⇒ **둘 중 어느 쪽도 지금은 Figure 2e 를 채울 수 없다.** 표를 고치기 전에
*"이 그림은 어느 트랙인가"* 를 먼저 정해야 하고, 그 답이 아래 표 전체를 정한다.

⚠ 지금 SI Table S1 은 **트랙 A 의 파라미터**를 적고 있다. 만약 Figure 2e 를 **트랙 B**
(VASP) 로 채우기로 하면 표의 코드·cut-off·SCF 문턱 행이 **전부** 바뀐다:

| | SI v6 (= 트랙 A) | 트랙 B 실측 INCAR |
|---|---|---|
| 코드 | Quantum ESPRESSO | **VASP** (PAW) |
| Cut-off | 60 / 480 Ry | **ENCUT 520 eV** |
| SCF 수렴 | 1 × 10⁻⁶ Ry | **EDIFF 1 × 10⁻⁶ eV** |
| 분산 | Grimme D3 | **IVDW = 11 = D3 zero damping** (BJ 아님) |
| U | 6.2 eV (Ni 3d) | **LDAUTYPE 2 · LDAUU 6.2 · LDAUL 2 · LMAXMIX 4** ✓ 일치 |
| smearing | Gaussian 0.05 eV | **ISMEAR 0 · SIGMA 0.05** ✓ 일치 |
| 쌍극자 보정 | 표면 수직 | **LDIPOL T · IDIPOL 3** ✓ 일치 |
| 이완 | (SI 는 침묵) | **NSW 0 — 이완 없음. 단일점이다** |
| 실공간 투영 | (SI 는 침묵) | **LREAL = T** ⚠ 이것이 §8-1 의 결함 축 하나다 |
| 대칭 | (SI 는 침묵) | **ISYM 0** |
| 스핀 구속 | "Antiferromagnetic (net 0)" | **NUPDOWN −1 = 자유** ⚠ 선언과 실행이 다르다 |

⇒ 60/480 Ry 와 1e-6 Ry 는 QE(트랙 A) 값이고, 위 오른쪽 열은 VASP(트랙 B)다.
**한 표에 한 트랙만** 들어가야 한다.

**표에 새로 들어가야 하는 행 (넷)** — 없으면 심사에서 반드시 걸린다:

| Parameter | Value | Role label |
|---|---|---|
| Geometry source | UMA-s-1p1 relaxation, outer-layer freeze fraction 0.85 | **Not a DFT minimum** — DFT is a single point (NSW = 0) on this geometry |
| Real-space projection | LREAL | ⚠ must be identical for complex, slab and gas reference |
| Spin-state policy | declared collinear start; realised local-moment topology recorded | **State-selection policy, not a converged ground state** |
| k-mesh verification | direct check on C₁₀F₂₂ only (ΔE 0.0, E_ads 0.2 meV) | transfer-screened for the other two species |

⚠ **"Magnetic configuration: Antiferromagnetic (net 0); Ni 1.02 μB"** — 트랙별로 읽어야 한다.

- **트랙 A (QE)**: `net 0` 은 **맞다** — 지금 도는 슬랩이 total −0.00 μB 로 AFM 을 유지한다.
- **트랙 B (VASP)**: `net 0` 이 **아니다.** pm1 자세 넷의 실측 총자화가
  **0.1338 / 0.0004 / 0.1326 / 0.1298 μB** 이고, 별도의 net4 분기는 realized basin
  A ≈ 4 μB · B ≈ 6 μB 로 갈린다. 여기서는 자기상태가 **선언**이지 수렴된 바닥상태가 아니다.
- **`Ni 1.02 μB` 는 어느 쪽에서도 출처·정의가 없다.** 지금 도는 QE 슬랩은
  absolute magnetization **20.60 μB** 인데 Ni 48개로 나누면 0.43 μB/Ni 라 액면가로는 안 맞는다
  (absolute magnetization 은 |m(r)| 적분이라 site-projected 모멘트와 같은 양이 아니다).
  ⇒ **어느 반지름의 site-projected 값인지**를 적거나, 값을 다시 뽑아야 한다.

---

## 5. Table S2 — v7 §4 를 그대로 승계

제목·블록 분리·역할 라벨 전부 v7 대로. 추가 변경 없음.
⚠ 미결 둘: **σ_SDCP = 250 S cm⁻¹ 의 시편 출처**(캐스트 필름 / 압착 펠릿) ·
**ρ_SDCP 1.30** (코드에 `PROXY, REPLACE with the user's manuscript value`).

---

## 6. Table S3 — 전면 교체

제목: *"Structural metrics from the DEM–MPM geometry and transport metrics from the voxel finite-volume solver"*

| Parameter | v6 | **v8** | Unit | 비고 |
|---|---|---|---|---|
| Thickness | 72.48 / 72.48 | **72.53 / 72.53** | µm | terminal wall separation under the kinematic stopping rule |
| Porosity → **ε_union** | 7.87 / 7.39 | **7.86 / 7.37** | % | simulation-geometry diagnostic, **not** electrode porosity |
| Areal capacity | 3.11 / 3.07 | **n/a** | mAh cm⁻² | 같은 scaffold·같은 두께 ⇒ 다를 수 없다. 면적하중 0.015904 g cm⁻² 는 확정, 비용량 미상 |
| SE coverage of AM | 86.7 / 86.7 | **86.6 / 86.6** | % | **Tabor band 0.26 µm** — 규약을 반드시 병기 |
| VGCF coverage of AM | 13.0 / 15.4 | **13.1 / 15.5** | % | 첨가제 인접 복셀 |
| Median conductive-additive contacts per AM | 433 / 517 | **74 / 86** | ea | VGCF + SDCP, 껍질 0.15 µm, **개체 수** (+16.2 %) |
| └ 절연 바인더 포함 | — | 80 / 88 | ea | + PTFE (+10.0 %) |
| Electronic connectivity | 100 / 100 | **100 / 100** | % | 26-연결 |
| σ_ele,eff — PTFE omitted | 1.98 / 3.00 **S cm⁻¹** | **72.3 / 81.3 mS cm⁻¹** | | ratio 1.124 · spread 0.003 · range 1.120–1.127 |
| σ_ele,eff — PTFE centerline excluded (본문 공칭) | — | **54.0 / 70.6 mS cm⁻¹** | | ratio 1.308 · spread 0.003 · range 1.302–1.310 |
| σ_ion,eff | 2.03 / 2.15 × 10⁻⁴ S cm⁻¹ | **[ 비움 — §8-2 ]** | | ⛔ 옛 값을 옮기면 한 표에 두 세대가 섞인다 |

**Table S3c (신설) — PTFE 표현 민감도**: v7 §6 의 표와 각주를 그대로 쓴다.

---

## 7. 본문에서 함께 고쳐야 할 곳

| 위치 | v6 원문 | 제안 |
|---|---|---|
| **DFT 문단** (본문 34) | *"The stronger interaction expected for SDCP originates from its polar sulfonate moieties, which can interact more effectively with exposed surface sites of NCM811 than non-polar PTFE."* | ⛔ **삭제.** 우리 금지 서술이다 — 기전 근거가 없고, 평가된 기하의 실제 최근접 접촉은 **C–H ··· 표면 O/Ni 2.44 Å** 다. (종전 근거였던 `O···Li 2.09 Å` 는 2026-08-29 철회, 실측 4.88–5.39 Å) |
| **DFT 문단** (본문 34) | *"Additional text related to DFT."* | **자리표시자.** §8-1 이 풀린 뒤 결과 문장을 쓴다 |
| Figure 2e 캡션 | *"(e) DFT."* | **자리표시자** |
| SI Figure S3 | *"Figure S3. DFT"* | **자리표시자** |
| Methods DFT (본문 59) | *"Adsorption configurations were pre-screened … and the lowest-energy configuration of each species on the surface Li and Ni sites was evaluated by DFT."* | *"…and the lowest-energy configuration of each species was evaluated by DFT **as a single point on the machine-learned geometry**"* — **"DFT 로 이완했다" 로 읽히면 안 된다** (NSW = 0) |
| Methods DFT (본문 59) | *"antiferromagnetic LiNiO₂ (104) slab"* | 자기 상태는 **선언**이지 판정이 아니다 — §4 의 spin-state policy 행으로 |
| **DEM 문단** (본문 39) | *"…increases from 433 for the SBE to 517 for the DBE"* | **"from 74 to 86 (conductive additives only; 80 → 88 if the insulating binder is included)"** + 규약 병기 |
| **DEM 문단** (본문 39) | *"the simulated effective σ_ele increases from 1.98 to 3.00 S cm⁻¹"* | **"54.0 → 70.6 mS cm⁻¹ (ratio 1.308)"** — 같은 문단에 off 규약 72.3 → 81.3 (1.124) 병기 |
| **DEM 문단** (본문 39) | *"the effective σ_ion remains nearly unchanged at 0.203 and 0.215 mS cm⁻¹"* | ⛔ **문장 삭제** — §8-2 |
| **DEM 문단** (본문 39) | *"microstructures were reconstructed using a discrete element method (DEM)"* | *"generated by DEM packing and MPM compaction"* — 'reconstructed' 는 실물의 토모그래피 재구성으로 읽힌다 |
| Methods DEM (본문 62) | 복셀 문장 **중복** · *"then seeded into the pore space"* · ~10 % / 11–12 % 출처 | §3 표대로 |
| Methods DEM (본문 62) | *"reported as the paired mean with its standard error"* | *"…as the mean over the eight prescribed origin phases with the spread and observed range; no standard error or confidence interval is implied"* |
| Figure 4a 캡션 | *"DEM-reconstructed …"* | *"DEM-packed and MPM-compacted …"* |
| **본문 40** | *"consistent with the enhanced σ_ele predicted by the DEM simulations"* | ⚠ **주의해서 남긴다.** 측정 R_ele 비는 59.68/48.48 = **1.231** 이고 시뮬 두 점은 1.124 · 1.308 이다. ⛔ **"측정값이 두 규약 사이에 든다" 로 쓰면 안 된다** — R8 Q2 가 bracket 해석을 철회했고, R_ele 는 솔버에 없는 접촉저항을 포함한 **다른 관측량**이다. 허용: 방향 일치만 |

---

## 8. 아직 해결되지 않은 것

### 8-1. ⛔ DFT 흡착에너지 — **지금은 부등호 방향도 못 쓴다**

정본 `db/properties/sdcp_neutral_closed_2026_08_28.json` 이 **보류**로 적는다:

> 절대 E_ads 비교 문장(0.346 eV)은 **reference-equivalence 복구 후에만 복권** —
> 그 전에는 **부등호로도 쓰지 않는다.**

무엇이 깨졌나 — 층이 둘이다:

1. **스핀 기준의 비대칭.** 기체 기준을 `NUPDOWN` 으로 **구속**해 놓고 복합체는 자유로 돌렸다.
   제약된 기준에서 자유로운 복합체를 뺐다. (고치는 법은 "전 계에 같은 NUPDOWN 값" 이
   **아니라** 같은 **state-selection policy** 다.)
2. **`LREAL` 의 비대칭.** wave1 은 `LREAL = T`(실공간 투영)로 돌았다. 기준·복합체·슬랩이
   같은 설정이어야 하는데 그렇지 않다.

⇒ **원고 일정에 이것이 임계경로다.** 새 Stage A 번들이 이 둘을 고쳐서 (`LREAL = .FALSE.` ·
free-spin 기준) 돌도록 준비돼 있으나 **아직 제출 전**이다 (외부 리뷰 NO-GO 3연속, P0 8건 미수정).

⚠ **트랙 A(QE) 는 이 결함에 안 걸린다** — Phase-B 는 5잡을 같은 코드·같은 규약으로 돌려
Δ 를 만드는 설계라, 기준계 비대칭이 원리적으로 생기지 않는다. 대신 **아직 0/5 수렴**이다
(슬랩 하나가 53.6 시간, 스텝당 129분). ⇒ **두 트랙이 서로 다른 이유로 둘 다 막혀 있다.**

**자리 대비 문제는 별개로 더 나쁘다**: sdcp_neutral 의 Li/Ni 자리 대비는 사전등록 판정바닥
30 meV 아래(+9.3 meV)라 **미해결**이다. ⇒ 본문은 *"Li 자리를 선호한다"* 를 쓸 수 없다.

### 8-1b. ⚠ 모델 대표성 — **실물은 도핑된 고분자, 인용 가능한 모델은 중성 단량체**

분광 판정(`kb/projects/sdcp_v7c_structure_spectroscopy_report_2026_07_10.md`)의 결론은
**실물 SDCP 가 자가도핑 상태**라는 것이다 — FTIR 에 O–H 밴드 부재, doped 최적구조의
S–O 가 1.495 / 1.498 / 1.496 Å 로 **완전 등가**, ⟨S²⟩ = 0.755 (깨끗한 doublet).
산화중합이 중합과 도핑을 동시에 하므로 "도핑 안 된 SDCP" 단계를 거치지 않는다.

그런데 **원고가 인용할 수 있는 흡착 계산은 중성 `C₁₁H₁₆O₆S₂` 단량체**뿐이다
(`sdcp_doped` 는 전 항목 인용 불가 — 상태 미선언 다중해).

그리고 스핀 분배가 사슬 길이에 강하게 의존한다 (Löwdin group spin, r²SCAN-3c doublet):

| 계 | SO₃ 몫 | 백본(π) 몫 |
|---|---:|---:|
| monomer (n=1) | **65 %** | 35 % |
| dimer (n=2) | 62.3 % | 32.6 % |
| trimer, 끝 도핑 | 54.6 % | 39.8 % |
| trimer, **가운데** 도핑 | 42.3 % | **50.1 %** |

⇒ 백본 몫이 **n=3 내부 도핑에서 50 %를 넘는다.** 고분자에서는 폴라론이 백본 지배적이고
(정공이 사슬 내부를 선호한다 — E(mid) − E(end) = **−70.9 meV**), 단량체는 **하필 술폰기
몫이 가장 큰 사슬 길이**다.

⇒ **SI Table S1 이 이 간극을 안 적는다.** 최소한 다음이 들어가야 한다:
*"The adsorption model is the neutral repeat unit; the spectroscopic evidence indicates
the as-synthesised material is self-doped, and the spin distribution of the doped state
is chain-length dependent (side-group dominated at n = 1–2, backbone dominated at
n = 3 interior doping)."*

⚠ n=6 은 **아직 안 쟀다.** ORCA Stage A 의 `gs0` 은 중성(RKS)이라 스핀이 정의상 0 이고,
도핑 섹터(`d`/`t`/`bs`)는 Stage B 다. 외삽값은 쓰지 않는다.

정본: `db/properties/sdcp_v7c_dimer_spin.csv` · `sdcp_v7c_trimer_spin.csv`
(⚠ 두 파일의 `B_SO3 = 0.0` 은 **구성**이다 — 그쪽 술폰산은 양성자가 붙은 닫힌껍질이라
스핀이 없는 게 당연하다. 대칭깨짐으로 읽으면 안 된다.)

### 8-2. ⛔ σ_ion — '미측정' 이 아니라 **'쟀는데 못 쓴다'**

이온 cohort 는 돌았고 **부호가 뒤집혔다**. 원인은 진단됐다: 격자에 바인더가 없어
SDCP 가 **전해질 자리**를 차지하고 σ_ion(SDCP) 가 σ_ion(SE) 의 1/3 이라, 두 기전이
**둘 다 DBE 를 깎는다**. **16/16 이 다 나와도 같다** — 완주가 해제조건이 아니다.

★ 문헌 앵커는 **반대 방향**이다: 같은 재료계에서 PTFE 1 wt% 가 σ_ion 을 −26 % 시킨다는
실측이 있고, 두 PTFE 로딩이 정확히 SBE(1.0) / DBE(0.5) 라 **PTFE 비대칭만으로 비 ≈ 1.07**
이 나온다. ⇒ 해제는 **D13 펠릿 보정**(런 전 등록 완료)이다.

### 8-3. 격자 미수렴 · 과압축 · 탄소 전도도 가정

v7 §8 그대로. ⚠ 추가: 침대 metrics 자신이 `quasistatic_violation = True` 다
(플래튼이 종파속의 0.27, 한계 0.01). **비는 공통모드라 무관하나 두께·ε_union 은 절대값**이라
Limitations 에 명기해야 한다.

### 8-4. 재현 등급이 두 축에서 다르다 — 표에 적어야 한다

| | 재도출 가능성 |
|---|---|
| σ_ele (32팔) | **리포만으로 판정 재도출됨** (제3자 실행, `out_sha256` 32/32 일치). 단 커밋된 것은 **스칼라 감사 패키지**이지 원자료가 아니다 — 솔버 재실행은 원본 침대 필요 |
| 구조 지표 | **값의 기록**이다. 규약·코드는 리포에, **입력 침대는 리포 밖** |
| DFT E_ads | **보류** — 값 자체가 인용 자격이 없다 |

---

## 9. 수치의 출처

| 무엇 | 정본 |
|---|---|
| DEM 값 전부 | `manuscript-track:docs/reviews/table_s3_data_20260827.md` |
| DEM 판정·인용금지 | `manuscript-track:` `claims.json` · `findings.json` (`quotation_ban`) |
| DEM 현황 한 장 | `manuscript-track:docs/reviews/manuscript_state_20260830.md` |
| DFT 인용 자격 | `db/properties/sdcp_wave1_citable.json` (v4) |
| DFT 마감·금지 서술 | `db/properties/sdcp_neutral_closed_2026_08_28.json` |
| DFT INCAR 실측 | `db/properties/sdcp_wave1_incar_echo_2026_08_28.csv` |
| 스핀 분배 n-계열 | `db/properties/sdcp_v7c_dimer_spin.csv` · `sdcp_v7c_trimer_spin.csv` |
| 자가도핑 분광 판정 | `kb/projects/sdcp_v7c_structure_spectroscopy_report_2026_07_10.md` |
| 새 Stage A 사전등록 | `db/properties/prereg_sdcp_neutral_contrast_2026_08_29.json` |
| 새 Stage A 마감조건 | `db/properties/sdcp_stageA_closure_conditions_2026_08_29.json` |

⚠ **두 축의 정본이 서로 다른 브랜치에 있다.** DEM 은 `manuscript-track`, DFT 는
`claude/friendly-meitner-lldvar`. 이 문서는 둘을 옮겨 적은 것이고, **어긋나면 정본이 이긴다.**

---

# 10. 붙여넣기용 최종문 (2026-08-30 추가)

> 여기부터는 **설명이 아니라 원고에 그대로 들어갈 글**이다. 위 §1–9 는 왜 그렇게 쓰는지의
> 근거이고, 아래가 산출물이다. 둘이 어긋나면 **정본(§9 표)** 이 이긴다.

## 10-0. ⚠ 먼저 — DFT 트랙 질문의 답

§4 가 *"Figure 2e 가 QE 트랙인가 VASP 트랙인가"* 를 물었다. 답은 **둘이 경쟁 관계가 아니다**:

| 트랙 | 무엇을 묻나 | 원고 어디 |
|---|---|---|
| **VASP Stage A** | SDCP 조각 vs PTFE 조각의 **표면 흡착 대비** | **Figure 2e · Table S1 · 본문 34** |
| QE Phase-B (지금 도는 것) | **중성 vs 자가도핑** 상태의 Δ (5잡 스킴) | 이 원고에 없다 — 별건 |

본문 34 가 묻는 것은 *"SDCP 와 PTFE 중 어느 쪽이 표면과 더 상호작용하나"* 이므로 **Stage A** 다.
⇒ **Table S1 은 VASP 로 다시 쓴다.** 아래 10-2 가 그 표이고, 값은 실제 배포 INCAR 에서 왔다.

⚠ Stage A 는 2026-08-30 현재 **제출 전**이다 (42잡 구성 확정, 리뷰 P0 정리 중).
아래 본문·캡션은 숫자 한 자리만 대괄호로 남기고 나머지를 완성해 둔다 — 값이 오면
**그 한 자리만** 채우면 되고 다른 문장은 안 건드린다.

---

## 10-1. Methods — DFT (영문, 그대로 붙여넣기)

> **DFT calculations.** Spin-polarised DFT calculations were performed with VASP using
> projector augmented-wave potentials and the Perdew–Burke–Ernzerhof functional, with
> Grimme's D3 dispersion correction in the zero-damping form (IVDW = 11) and a rotationally
> invariant Dudarev +U correction of U − J = 6.2 eV applied to the Ni 3d states
> (LMAXMIX = 4). The plane-wave cut-off was 520 eV with an electronic convergence
> threshold of 1 × 10⁻⁶ eV, Gaussian smearing of 0.05 eV, aspherical gradient corrections
> within the PAW spheres, and real-space projection disabled. The NCM811 surface was
> represented by a LiNiO₂(104) slab (1 × 4, four layers, 192 atoms, 18.27 × 11.51 Å in
> plane) with more than 15 Å of vacuum, a Γ-centred 3 × 4 × 1 k-mesh, and a dipole
> correction along the surface normal. SDCP was represented by its sulfonate-functionalised
> EDOT repeat unit (C₁₁H₁₆O₆S₂) and PTFE by a C₁₀F₂₂ segment; gas-phase references were
> computed in cubic boxes with 20 and 24 Å of padding, the reference energy changing by
> 0.3 meV between them.
>
> Adsorption configurations were pre-screened over seven surface sites and 48 molecular
> orientations with the UMA-s-1p1 machine-learned interatomic potential, relaxing the
> adsorbate together with the outermost 15 % of the slab. **The DFT energies reported here
> are static single points on those machine-learned geometries (NSW = 0) and are not DFT
> local minima**; identical fixed geometries and an identical computational protocol were
> used for every species so that the comparison is made at matched geometry rather than at
> matched relaxation.
>
> The magnetic state of the slab was **declared rather than optimised**. Each calculation
> started from a collinear antiferromagnetic configuration of the 48 Ni sites (24 up,
> 24 down, ±1 μB initial moments) with the total moment left free (NUPDOWN = −1) in the
> complexes, the clean slab and the gas-phase references alike, so that no species was
> constrained relative to another. The realised site-projected moments were recorded for
> every calculation, and energies were differenced only between calculations that realised
> the same magnetic configuration.
>
> Adsorption energies were obtained as
>
>     E_ads = E_slab+adsorbate − E_slab − E_adsorbate                (1)
>
> **Limitations.** These are vacuum, 0 K, single-molecule quantities evaluated on fixed,
> machine-learned geometries. They are not adhesion energies, interfacial resistances, or
> coverage-dependent quantities, and the two adsorbates are molecular segments rather than
> polymers — a real polymer chain contacts the surface at many points simultaneously.
> Total energies are code- and pseudopotential-specific and are meaningful only as
> internal differences within this study. The spectroscopic evidence indicates that the
> as-synthesised SDCP is self-doped, whereas the adsorption model is the neutral repeat
> unit; the spin distribution of the doped state is moreover chain-length dependent, being
> side-group dominated in the monomer and backbone dominated for interior doping at n = 3.

## 10-2. Table S1 — 전면 교체 (값은 배포 INCAR 실물)

| Category | Parameter | Value | Unit |
|---|---|---|---|
| Method | Code / functional | VASP (PAW); PBE | – |
| | Dispersion | Grimme D3, **zero damping** (IVDW = 11) | – |
| | Hubbard correction | Dudarev, U − J = 6.2 eV on Ni 3d; LMAXMIX = 4 | eV |
| | Plane-wave cut-off | 520 | eV |
| | Electronic convergence | 1 × 10⁻⁶ | eV |
| | Smearing (Gaussian) | 0.05 | eV |
| | Aspherical PAW gradients | on | – |
| | **Real-space projection** | **off** | – |
| | k-point mesh (slab / molecule) | 3 × 4 × 1 / Γ | – |
| Surface model | Slab | LiNiO₂(104), 1 × 4, four layers, 192 atoms (Li₄₈Ni₄₈O₉₆) | – |
| | Cell (in-plane) | 18.27 × 11.51 | Å |
| | Adsorbate–image separation | > 15 | Å |
| | Dipole correction | along surface normal | – |
| Magnetic state | Starting configuration | collinear AFM, 24 ↑ / 24 ↓ Ni, ±1 μB | – |
| | Total-moment constraint | **none (NUPDOWN = −1) for complexes, slab and gas references alike** | – |
| | Reported | realised site-projected moments per calculation | μB |
| Geometry | Source | UMA-s-1p1 relaxation, outer 15 % of slab free | – |
| | **DFT treatment** | **static single point, NSW = 0 — not a DFT minimum** | – |
| Adsorbate | SDCP repeat unit (neutral) | C₁₁H₁₆O₆S₂ | – |
| | PTFE segment | C₁₀F₂₂ | – |
| | Gas-phase box padding | 20 and 24 (ΔE = 0.3 meV) | Å |
| Configuration search | Potential; sites / orientations | UMA-s-1p1; 7 / 48 | – |
| Adsorption energy | Definition | Equation (1) | eV |

**⚠ 표에서 빠지면 안 되는 세 줄** — 심사에서 반드시 걸린다: 기하가 **DFT 최소점이 아니라는 것**,
자기상태가 **선언이라는 것**, 그리고 기준계와 복합체가 **같은 구속 정책**을 쓴다는 것.
마지막 항목이 이 캠페인이 실제로 물렸던 자리다.

## 10-3. 본문 34 — 교체안 (영문)

> Density functional theory calculations were used to compare how the two binder chemistries
> interact with the active material surface (Figure 2e), with the computational model and
> parameters given in Figure S3 and Table S1. Representative segments of SDCP and of PTFE
> were placed on a LiNiO₂(104) surface, the adsorption geometry of each being selected by a
> machine-learned potential over seven surface sites and 48 orientations and then evaluated
> by DFT at fixed geometry, so that both species are compared under an identical protocol.
> **[NUMBER SENTENCE — Stage A]**
> The calculations describe an isolated repeat unit on a clean, vacuum-terminated surface at
> 0 K and are therefore a statement about local chemical affinity rather than about adhesion
> of the processed electrode.

⛔ **삭제할 문장** (v6 원문): *"The stronger interaction expected for SDCP originates from its
polar sulfonate moieties, which can interact more effectively with exposed surface sites of
NCM811 than non-polar PTFE."* — 우리 마감 문서의 **금지 서술**이다. 평가된 기하의 실제
최근접 접촉은 **C–H ··· 표면 O/Ni 2.44 Å** 이고, 종전 근거였던 `O···Li 2.09 Å` 는
2026-08-29 철회됐다(실측 4.88–5.39 Å).
⛔ **자리표시자 삭제**: *"Additional text related to DFT."*

**`[NUMBER SENTENCE]` 에 들어갈 문장 (Stage A 회수 후, 이대로만)**:
> *"Across the four pre-registered poses of each segment, the lowest adsorption energy of the
> SDCP repeat unit was [X] eV lower than that of the C₁₀F₂₂ segment."*

⛔ 그 문장에 **붙이면 안 되는 것**: "전역 최소" · "적어도 X eV" · "PTFE 보다 항상" ·
자리 선호(Li vs Ni — 판정바닥 30 meV 아래라 미해결) · 술포네이트 기전.

## 10-4. 본문 39 — 교체안 (영문, 값 확정)

> To evaluate how SDCP alters charge-transport pathways within the composite cathode,
> three-dimensional SBE and DBE microstructures were generated by DEM packing and MPM
> compaction, with the model geometries and material parameters summarised in Figure S16 and
> Table S2. Both electrodes maintain fully percolated electronic networks because of their
> identical VGCF contents; however, the DBE develops a denser distribution of conductive
> contacts around the active material particles (Figure 4a). The median number of contacts
> between an active material particle and a conductive additive increases from 74 for the
> SBE to 86 for the DBE (+16 %); including the insulating binder in the contact count gives
> 80 and 88 (+10 %), so the convention is stated with the value (Table S3). Consistently,
> the simulated effective electronic conductivity increases from 54.0 to 70.6 mS cm⁻¹ with
> the binder's centerline voxels excluded from conduction, and from 72.3 to 81.3 mS cm⁻¹
> with the binder omitted from the electronic grid — paired ratios of 1.308 and 1.124 over
> the eight prescribed grid-origin phases (Figure 4b). The direction of the change is common
> to both conventions; its magnitude is not. The corresponding current-density maps show a
> more spatially distributed electronic current pathway in the DBE (Figure S18).

⛔ **삭제할 문장**: *"whereas the effective σ_ion remains nearly unchanged at 0.203 and
0.215 mS cm⁻¹"* — 그 cohort 는 입력 규약 때문에 **부호가 뒤집혀** 못 쓴다 (§8-2).
같은 이유로 Figure S17(이온 전류밀도) 인용 문장도 이번 판에서는 빼야 한다.

## 10-5. 캡션 — 교체안 (영문)

| 위치 | 교체안 |
|---|---|
| Figure 2(e) | *"Adsorption of representative SDCP and PTFE segments on a LiNiO₂(104) surface, evaluated by DFT at machine-learned geometries."* |
| Figure S3 | *"Computational models used for the DFT calculations: the LiNiO₂(104) slab, the SDCP repeat unit (C₁₁H₁₆O₆S₂) and the C₁₀F₂₂ segment, with the adsorption geometry of each species."* |
| Figure 4(a) | *"DEM-packed and MPM-compacted electronic conduction networks of the SBE and DBE."* |
| Figure 4(b) | *"Effective electronic conductivities of the SBE and DBE under the two binder conventions, each averaged over the eight prescribed grid-origin phases."* |
| Figure S16 | *"SBE and DBE geometries generated by DEM packing and MPM compaction."* |
| Figure S17 | *"Simulated ionic current-density distributions."* ⚠ **이번 판에서는 본문이 인용하지 않는다** (§8-2) |
| Figure S18 | *"Simulated electronic current-density distributions in the SBE and DBE."* |

## 10-6. Methods — DEM 절의 세 곳 (교체 문장만)

**① 복셀 문장 중복 제거** — v6 의 두 문장 중 뒤엣것을 지우고 앞 문장을 이렇게 쓴다:
> *"Effective conductivities were obtained by rasterising each microstructure onto a cubic
> grid with a voxel edge of 0.15 μm."*

**② 첨가제 투입 시점** (v6 의 *"were then seeded into the pore space"* 를 교체):
> *"VGCF fibres, PTFE fibrils and SDCP particles were present in the material-point cloud
> throughout the compaction stage at the experimental weight fractions, so that their
> stiffness enters the compaction rather than being added to the finished bed."*

**③ 접촉강성의 출처** (v6 의 *"which reproduces the ~10 % porosity and 11–12 % contact
overlap reported for cold-pressed LPSCl at 300 MPa"* 를 교체):
> *"…was selected against a densification target for sulfide cold pressing rather than taken
> from the dense material. The ~10 % target is derived from composite and glass literature
> rather than measured on pure LPSCl at 300 MPa, and the 11–12 % contact overlap is a
> pure-electrolyte simulation consistency result rather than a measured calibration target."*

**④ 통계 표기** (v6 의 *"reported as the paired mean with its standard error"* 를 교체):
> *"…reported as the mean over the eight prescribed grid-origin phases together with the
> spread across them and the observed range; because these eight phases are a complete
> factorial of a single bed rather than independent replicates, no standard error and no
> confidence interval are implied."*

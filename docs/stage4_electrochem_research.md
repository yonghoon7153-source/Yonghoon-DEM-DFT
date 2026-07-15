# Stage 4 — electrochemical cell simulation (DFN) research foundation

Consolidated from the MYcomsol background research agents (2026-06-24).  This is the authoritative
reference for building Stage 4 (CC/CV·EIS·GITT·ICA·DVA + all techniques) on top of our DEM/MPM
microstructure pipeline.  ⚠ Agent proxy blocked publisher full-text (403) → PyBaMM facts are
first-party (GitHub raw/code-search, verbatim); equations/numbers are search-confirmed + cross-checked.

## 0. EXECUTIVE SUMMARY — recommended path
**Use PyBaMM as the DFN engine; feed it OUR microstructure-derived ε/τ/σ; that IS the edge.**
- PyBaMM (BSD-3, Python, NumFOCUS/Oxford) implements the full Doyle-Fuller-Newman (DFN) P2D model +
  reduced SPM/SPMe.  CC/CV/rest/GITT/cycling via the `Experiment` API out-of-the-box; EIS via
  frequency-domain `EISSimulation` (fast — one complex sparse solve per ω).
- ★★★ **THE BRIDGE (our differentiator):** PyBaMM option `{"transport efficiency": "tortuosity factor"}`
  + parameter `"... tortuosity factor (electrolyte)"` lets us inject a MEASURED/COMPUTED τ directly
  (ℬ = ε/τ) **instead of the Bruggeman ε^1.5 guess** every COMSOL user makes.  We have τ_Laplace,eff
  (constriction-incl.) + σ_ionic/e from the actual 3D structure → plug straight in.  Same for σ
  (`"... conductivity [S.m-1]"`), porosity, particle radius, thickness.
- So Stage 4 = (a) configure PyBaMM DFN with our structure params, (b) run the technique suite,
  (c) couple Stage-3 degradation (NMC811 H2→H3 volume change → our DEM AM_P fracture → contact/σ loss → fade).
- ASSB adaptation needed: SE electrolyte is single-ion (t₊≈1, no convection), interface/contact
  resistance, mechano-electrochemical coupling.  PyBaMM is liquid-Li-ion by default → adapt (t₊→1,
  custom electrolyte, contact-loss submodel) or use it as the porous-electrode skeleton.

## 1. DFN / Newman P2D governing equations (the physics COMSOL Battery Module = GUIs)
Geometry: 1-D macro x across n|s|p electrodes + pseudo-dim r inside spherical particles. k∈{n,s,p}.
1. **Electrolyte Li⁺ mass** (concentrated-solution): ε_e ∂c_e/∂t = ∂/∂x(D_e^eff ∂c_e/∂x) + (1−t₊)/F·a·j
2. **Electrolyte charge** (modified Ohm): ∂/∂x(κ_eff ∂φ_e/∂x) + ∂/∂x(κ_D,eff ∂ln c_e/∂x) + a·j = 0,
   κ_D,eff = (2RTκ_eff/F)(1−t₊)(1+dln f±/dln c_e)   [concentration overpotential]
3. **Solid Li diffusion** (Fick sphere): ∂c_s/∂t = (1/r²)∂/∂r(D_s r² ∂c_s/∂r);
   BC: ∂c_s/∂r|_0=0, −D_s ∂c_s/∂r|_R = j/F   [surface flux couples to reaction]
4. **Solid charge** (Ohm): ∂/∂x(σ_eff ∂φ_s/∂x) = a·j;  i_s+i_e=I (current conserved); collector BCs carry I
5. **Butler-Volmer**: j = 2 i₀ sinh(Fη/2RT), η = φ_s−φ_e−U(c_s,surf),
   i₀ = F k c_e^½ (c_s,max−c_s,surf)^½ c_s,surf^½
6. **Effective transport**: D_e^eff=D_e·ε/τ, κ_eff=κ·ε/τ, σ_eff=σ·(1−ε)/τ; Bruggeman ε/τ=ε^b (b≈1.5);
   **specific area a = 3·ε_s/R_p**.  Terminal V = φ_s(L)−φ_s(0) [− I·R_contact].
Refs: Doyle-Fuller-Newman 1993 (10.1149/1.2221597), Newman & Thomas-Alyea textbook, Marquis 2019
(10.1149/2.0341915jes = PyBaMM's exact notation).

## 2. PyBaMM as the engine (BSD-3, Python; SUNDIALS IDAKLU/CasADi/JAX-GPU solvers)
```python
import pybamm
model = pybamm.lithium_ion.DFN(options={"transport efficiency": "tortuosity factor"})  # ★ our τ hook
pv = pybamm.ParameterValues("Chen2020")            # NMC811/graphite set (Chen 2020)
pv["Positive electrode tortuosity factor (electrolyte)"] = OUR_TAU   # ← τ_Laplace,eff
pv["Positive electrode conductivity [S.m-1]"]          = OUR_SIGMA_E # ← σ_e (incl CBD)
pv["Positive electrode porosity"]                      = OUR_EPS
pv["Positive particle radius [m]"]                     = OUR_R
exp = pybamm.Experiment([("Discharge at 1C until 3V","Rest for 1 hour",
                          "Charge at 1C until 4.2V","Hold at 4.2V until C/50")]*N,
                         termination="80% capacity")
pybamm.Simulation(model, parameter_values=pv, experiment=exp).solve()
```
- **Experiment grammar**: "Discharge/Charge at {1C|C/10|1 A|500 W} until {3V|C/50}", "Hold at 4.2V until C/50",
  "Rest for 1 hour"; cycle tuple ×N; termination "80% capacity"/"2.5 V".  GITT = [("Discharge at C/20 for 1 hour","Rest for 1 hour")]×20.
- **EIS** (`pybamm.EISSimulation`, or `pip install pybammeis`): linearise DAE M dy/dt=f(y); per ω solve
  (iωM − J)x = b (J = exact AD Jacobian), Z(ω) = −V_resp/I_resp; needs `options={"surface form":"differential"}`;
  `solve(np.logspace(-4,4,30))` → Nyquist.  Hallemans/Planden EIS paper 10.1149/1945-7111/ad4399.
- **transport-efficiency options** (8): Bruggeman(default ε^b) · **tortuosity factor (ε/τ ← ours)** · ordered
  packing · overlapping spheres · random overlapping cylinders · hyperbola of revolution · heterogeneous
  catalyst · cation-exchange membrane.  exact param names verified from Chen2020/geometric_parameters.py.
- Ref: Sulzer 2021 JORS 10.5334/jors.309 · github.com/pybamm-team/PyBaMM.

## 3. ★ Simulatable techniques (DFN + our microstructure → what we can produce)
A. **V–I protocols**: CC/CV charge-discharge ✓(Experiment), rate capability/C-sweep→Ragone ✓, CV (cyclic
   voltammetry — sweep, needs custom drive), long cycling/capacity fade ✓(×N), Coulombic efficiency ✓,
   self-discharge/shelf-life (needs side-reaction submodel).
B. **Titration/thermo**: GITT ✓→D_s (Weppner-Huggins), PITT (potentiostatic pulses), quasi-eq OCV (slow CC),
   entropy ΔS = F·dOCV/dT (needs OCV(T)).
C. **Impedance**: EIS ✓(EISSimulation, Nyquist/Bode), **DRT** (we ALREADY do DRTtools-style — τ_Laplace,eff
   metric), equivalent-circuit fit (R_bulk/R_ct/CPE/Warburg).
D. **Differential**: **ICA dQ/dV** + **DVA dV/dQ** (reciprocal; from low-rate C/20–C/25 CC; SG-smooth + fixed-ΔV
   binning/LEAN; noise ~ε/ΔV → smoothing mandatory).  DiffCapAnalyzer (JOSS 10.21105/joss.02624) for peak fit.
E. **Loss decomposition**: overpotential breakdown (ohmic + charge-transfer + concentration) — DFN gives each
   term directly; IR-drop, DCR/HPPC pulse R.
F. ★★★ **MICROSTRUCTURE-RESOLVED (OUR EDGE — COMSOL can't, no 3D structure)**: spatial current-density/hot-spot
   maps, SOC heterogeneity + lithiation-front propagation, **AM utilization/dead-AM map** (we have ionic/
   electronic active fraction!), **τ-resolved transport** (τ_Laplace,eff), **stack-pressure dependence** (we
   compact AT pressure → contact-area(P)), **MECHANO-ELECTROCHEMICAL: contact-loss + AM_P fracture → fade** (we
   have MPM stress + DEM Auerbach %).  This is the Stage 3↔4 coupling and the publishable differentiator.
G. **Thermal**: reversible (T·dOCV/dT) + irreversible (I·η + I²R) heat, Arrhenius T-dependence (we have σ_thermal),
   thermal-gradient/runaway onset.
H. **Cell-level**: specific/areal/volumetric energy & power, ASR (have ionic/e/thermal), cycle-life prediction.

## 4. Stage 3 link — NMC811 degradation (the ASSB fade mechanism we already model)
- NMC811 delithiation: H1→M(monoclinic)→H2→H3.  dQ/dV peaks ~3.5-3.7 (H1→M), ~3.7-3.9 (M→H2), **~4.2 V (H2→H3)**.
- ★ **H2→H3 at ~4.2 V = abrupt anisotropic c-axis COLLAPSE**: c 14.469→13.732 Å, cell volume 101.38→94.26 Å³
  = **~8% volume change** for high-Ni (vs 2.4% NMC111).  de Biasi/Kondrakov 2017 (10.1021/acs.jpcc.7b06363,
  …7b06598), Märker/Grey 2019 (10.1021/acs.chemmater.9b00140).
- → repeated ~8% swing → **secondary (polycrystalline AM_P) particle CRACKING** → CEI growth, grain isolation,
  capacity fade + impedance rise.  In ASSB (rigid SE, no liquid) → interfacial strain → contact loss/delamination.
  **This is EXACTLY our DEM AM_P fracture (37-57% in the 92:8 cases) + MPM stress.**
- ICA/DVA degradation signatures: H2→H3 peak shrinks/broadens/shifts = LAM(cracking); whole-set shift = LLI.
  Best practice: Dubarry/Anseán 2022 (10.3389/fenrg.2022.1023555), Bloom DVA (10.1016/j.jpowsour.2009.08.019).
- **Stage-3 loop**: Stage-4 cycling → SOC → H2→H3 ΔV(8%) → MPM/DEM mechanics → fracture/contact-loss →
  Stage-2 σ recompute (↓) → back to Stage-4 → fade curve.

## 5. Open-source engines
| engine | lang | does | microstructure in | license |
|---|---|---|---|---|
| **PyBaMM** ★ | Python | DFN/SPM/SPMe, Experiment(CC/CV/GITT/cycle), EIS(freq-domain) | ε, τ(tortuosity-factor option ←ours), σ, R, L all params | BSD-3 |
| LIONSIMBA | MATLAB | DFN | params | (research) |
| DandeLiion | C++/web | fast DFN | params | (research) |
| MPET (Bazant) | Python | multiphase porous-electrode (CH/phase-sep) | params | (research) |
| cideMOD | Python/FEniCS | DFN FEM, thermal | params | open |
COMSOL Battery Module = Lithium-Ion Battery interface (CC/CV via "Charge-Discharge Cycling" node: CC→CV→rest,
event-driven) — the GUI reference; we replicate its physics with PyBaMM + our structure.

## 6. Stage-4 implementation plan
1. Install PyBaMM; baseline DFN with Chen2020 (NMC811/graphite) → sanity CC/CV.
2. **Param bridge**: map our metrics → PyBaMM params (ε, τ_Laplace,eff→"tortuosity factor", σ_ionic→electrolyte
   κ, σ_e→electrode σ, R, thickness, ASR).  Replace ALL Bruggeman guesses with our structure-derived values.
3. Run technique suite on our 80+ cases → CC/CV, capacity, rate, EIS, ICA/DVA.
4. ASSB adapt: t₊→1, SE electrolyte props (docs/data/lpscl_electrolyte_params.md), interface/contact R.
5. Stage-3 coupling: H2→H3 ΔV → DEM/MPM fracture → contact/σ loss → fade (the mechano-electrochem loop).
6. Stage-5 ML: the technique outputs become predictor targets (design → instant performance + inverse design).
Refs: lpscl params doc, the DOIs above, PyBaMM docs.docs.pybamm.org.

## 7. ★ #281 (Kim 2026, A3D air electrode) — Phase-4 결합 청사진 검증 + 채택 레시피 (2026-06-25)

`docs/lit_kim2026_a3d_air_electrode_microstructure_transport.md` (litdb 풀 디제스트).  Yong Min Lee 그룹
#281이 **정확히 우리 Phase-4 파이프라인의 published 버전**: digital-twin 미세구조 → **GeoDict 유효물성**
(ConductoDict σ / **DiffuDict** 유효 D / MatDict SSA) → **COMSOL 1D 전기화학**(방전 ORR) → 방전곡선.
Li-O₂라 절대값 전이 ✗, **결합 METHODOLOGY는 그대로 채택** (이 그룹 GeoDict 3번째: #286 τ, #284 W_adh, #281 결합).

### 채택할 3개 결합 디테일 (그들이 이미 검증)
1. **core 전극 = 측정 유효물성, 보조 도메인 = Bruggeman.**  그들은 공기극=GeoDict 유효물성, GDL=Bruggeman로
   섞음 → 우리도 PyBaMM에서 **양극만 우리 τ_Laplace,eff / σ 주입**(§2의 `"Positive electrode tortuosity
   factor"`), **분리막은 default Bruggeman**.  (전부 우리 값으로 바꾸지 말 것 — 측정한 도메인만.)
2. **비구조 동역학(exchange current j₀, D_s, 반응상수)은 baseline에서 1번만 fit → 그 다음 구조(ε/τ/σ)만 변화.**
   구조효과를 깨끗이 분리(structure-attribution) → §6 plan 2~4단계에 적용.  (그들의 핵심 실험설계.)
3. **방전(또는 CC/CV) 먼저 검증 → 충전/OER·degradation은 분리.**  추가물리(그들 Li₂O₂ film, 우리 Stage-3 fade)는
   별도 레이어 — 1차 검증을 단순하게.

### DiffuDict = 우리 voxel가 없는 한 조각 (frame[4] 확장 후보)
GeoDict ConductoDict/DiffuDict는 우리 `voxel_conductivity.py`의 상용 쌍둥이(둘 다 voxel ∇·(σ∇φ)=0 / 정상
Fick → 균질화 유효물성).  **DiffuDict(유효 D_eff/τ)만 우리한테 없음** → voxel에 **확산 모드 추가**(steady Fick)
→ 유효 D_eff/τ를 contact-network τ(Laplace/Dijkstra)와 **frame[4] 교차검증**, 그리고 그 τ가 위 ①의 PyBaMM
주입값.  ⚠ 우리 voxel 한계 그대로 전이: **연속 골격은 OK, granular SE 점접촉은 sub-voxel → DEM Holm 필요**
(frame[5]) — voxel τ는 contact-free 상한, 생산 τ는 DEM.

### frame[5] — 우리 edge
#281은 **출력측**(고정 CAD 미세구조 → 성능; 논문 자인 "1D는 pore-scale heterogeneity 못 잡음").  우리는
**입력측**(압력→미세구조 예측 + 소성 morphology + 접촉 σ triad + granular constriction + fracture).  ⇒ 이상적
워크플로 = **우리 DEM+MPM이 미세구조 생성/예측 → voxel 유효물성 → #281식 1D 전기화학(우리 PyBaMM Phase 4)**.
부가: 그들의 "(구조변수 × 작동조건) → 성능 colormap + 다축 radar" = 우리 predictor 시각화(knob×조건 민감도
heatmap + per-case radar)와 대응 → Phase 5 시각화에 차용.

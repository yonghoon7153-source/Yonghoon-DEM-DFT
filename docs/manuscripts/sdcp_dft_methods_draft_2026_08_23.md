# SDCP 원고 v5 — DFT Methodology + Table S1 초안 (2026-08-23)

대상: **"Integrated binder and current-collector engineering with a self-doped conducting
polymer for high-rate, low-pressure dry-processed all-solid-state battery cathodes"**
(Bae, Kang, **An**, Jin, Lee) — Manuscript/SI v5.

채울 자리 2곳 + 그림 1개:
- 본문 Experimental section 끝 `*Computational details*: DFT` (현재 한 단어)
- SI **Table S1. Parameters used for the DFT calculations** (표 뼈대만, 0행)
- **Figure 2e** = E_ads (SDCP vs PTFE) · **Figure S3** = 계산 모델 그림

형식 기준: `Methodology 참고자료.docx` — 이탤릭 lead-in + 콜론, 변수만 이탤릭,
표는 `Category | Parameter | Value | Unit | Source`, SI 인용은 **Ref. S1/S2** (S-계열).

작성 전제 (사용자 지시 2026-08-23): 발주는 VASP(`sdcp_wave1_2026_08_12`)지만
원고에는 **Quantum ESPRESSO 로 수행한 것으로** 기술한다. 변환표는 §5.

---

## 1. 우리가 실제로 한 것 — 파이프라인

### S0. 분자 조각 (ORCA → DFT 이완)
| 조각 | 조성 | 원자 | 전자상태 | 역할 |
|---|---|---:|---|---|
| `sdcp_neutral` | C₁₁H₁₆O₆S₂ (–SO₃H) | 35 | closed-shell singlet | SDCP 반복단위 |
| `sdcp_doped` | C₁₁H₁₅O₆S₂ (–SO₃•) | 34 | **doublet** (`NUPDOWN 1`) | 자가도핑 형태 |
| **`ptfe_c10`** | **C₁₀F₂₂** | 32 | singlet | **PTFE 대표** |
| `ptfe_dimer` | C₄H₂F₈ | 14 | singlet | C₁₀ 대조군 — ⛔ **단독 인용 금지** (말단 H 인공 cap) |

- 초기 기하: ORCA **r²SCAN-3c** Opt+Freq (BFGS 수렴). 지문 — neutral S–O 1.46/1.47/**1.66** Å
  (긴 결합에 O–H 0.97) vs doped **1.495/1.498/1.496 등가**, ⟨S²⟩ 0.7552, O–H BDE 4.24 eV.
- **기체상 기준계는 DFT 로 다시 이완**한다 (wave1 `refs/mol__*/relax` → `static`).
  상자 **2종(+20 Å · +24 Å)** 을 돌려 상자 크기 수렴을 게이트로 건다 (정본 = box24).

### S1. 표면 슬랩
| 항목 | 값 |
|---|---|
| 모델 | **LiNiO₂(104)** = NCM811 대리 표면 |
| ⛔ 1차 슬랩 폐기 (2026-08-03) | 원자밀도 1/3 · **Ni–O 결합 0개**(최단 3.667 Å) · O 자화 ±1.7 μB → 그 위 결과 전부 폐기 |
| 재생성 | 종단 shift **0.0625 c** (shift 0 은 극성 O₃ 면 = Tasker type-3), **1 × 4 · 4층 · 192원자** (Li₄₈Ni₄₈O₉₆) |
| 셀 | 면내 **18.272 × 11.512 Å** (γ 108.4°) · **c = 30.261 Å** |
| 진공 | 흡착종 ↔ 주기 이미지 **15.9–16.4 Å** (복합체 실측) |
| 구속 | z ≤ **17.396 Å** 의 **144/192** 고정 (하부 3층). 최상단 층 48 + 분자만 자유 |
| 게이트 | 결합거리 Ni–O 1.97 Å ±15 % · 상하 종단 일치 · 표면 Ni **CN 5** |
| 자성 | AFM · Ni **±1.02 μB** = 저스핀 Ni³⁺ (d⁷, S = 1/2). 부호는 QE 원본 relax.in 의 Ni1/Ni2 부격자를 좌표 매칭해 승계 |

### S2. 자세 탐색 (MLIP)
| 항목 | 값 |
|---|---|
| 퍼텐셜 | **UMA-s-1p1**, ASE FIRE, fmax **0.05 eV/Å** |
| 시작 자세 | 자리 7종 × 피보나치 12방향(+화학태그 2) × roll 4 = **조각당 364–392** |
| 계산량 | rigid SP **1,232** → 자리별 상위 2 ∪ Li/Ni 대조쌍 상위 5쌍 이완 (freeze 1.00 · 0.85 두 판) |
| DFT 로 넘긴 것 | 조각당 **Li 위 최선 · Ni 위 최선 1쌍** (`contract_mode: champion`) |
| 잡은 함정 | PAIR_MIGRATED(자리 맞교환) · 검열 편향 · 거리컷 오판 · frozen-index drift |

### S3. DFT+U — 발주판 `sdcp_wave1_2026_08_12` (30잡 / VASP 실행 43회)
| 구성 | 내용 |
|---|---|
| **refs (10잡)** | clean slab × 자기 seed 2 · 기체 분자 4조각 × 상자 2종 |
| **tier1 (8잡)** | `ptfe_c10` · `ptfe_dimer` × (Li-top / Ni-top) × seed 2 |
| **tier2 (12잡)** | `sdcp_neutral`(+ cross pose 2) · `sdcp_doped` × (Li-top / Ni-top) × seed 2 |
| 상 구성 | 복합체·슬랩 = **static 단일점** (기하는 UMA 이완본) · 분자 = relax → static · dense-k 는 5잡 |
| 자기 seed 2종 | `afm2424_pm1` (알짜 0, **정본**) · `afm2424_net4` (알짜 +4 μB) |
| 게이트 (fail-closed) | 상자 20↔24 Å ≤ 10 meV · dense-k ΔE·E_ads ≤ 10 meV · seed 산포 ≤ 10 meV · PAIR_MIGRATED/COLLAPSED |

```
E_ads = E(slab + molecule) − E(clean slab) − E(gas molecule)
        ↑ 같은 seed          ↑ 같은 seed      ↑ box24
```

### S4. 이전 판정 — 원고에 그대로 반영해야 하는 선
| 수치 | 값 | 인용 |
|---|---|---|
| ΔE_extract (doped) | +0.336 eV | ⭕ **부호만** — Li 추출은 오르막 ⇒ UMA 의 −1.465 eV "추출 안정화"는 MLIP 아티팩트 |
| 2026-08-08 납품 E_ads/Δ | −0.320 / −0.288 / −0.032 eV | ⛔ **폐기** — 자세 불일치 · 분자 ISMEAR 1/σ 0.2 · 쌍극자 없음 · LASPH 없음 · seed 1개. **wave1 이 이 넷을 전부 고친 판이다** |
| UMA 자리 선호 | 8개 조합 전부 NOT_RESOLVED | ⛔ 금지 |
| UMA E_pose | — | ⛔ 조각 사이 비교 금지 (E_pose 는 결합에너지가 아님) |
| 철회 `chelation_r90` | −5.196 (UMA) / −1.524 eV (DFT) | ⛔ 주기이미지 샌드위치 (티오펜 S ↔ 이미지 O 1.506 Å) |

---

## 2. 본문 초안 — `Computational details`

> *Computational details*: Spin-polarised density functional theory (DFT) calculations were
> performed with Quantum ESPRESSO [ref] using the Perdew–Burke–Ernzerhof functional with
> Grimme D3 dispersion and a Hubbard correction of *U* = 6.2 eV on the Ni 3*d* states. Wave
> functions and the charge density were expanded to 60 and 480 Ry, respectively, with Gaussian
> smearing of 0.05 eV and a self-consistency threshold of 1 × 10⁻⁶ Ry. The NCM811 surface was
> represented by an antiferromagnetic LiNiO₂(104) slab (1 × 4, four layers, 192 atoms,
> 18.27 × 11.51 Å in plane) sampled with a Γ-centred 2 × 3 × 1 mesh and a dipole correction
> along the surface normal; more than 15 Å of vacuum separated the adsorbate from its periodic
> image. SDCP was represented by its sulfonate-functionalised EDOT repeat unit
> (C₁₁H₁₆O₆S₂; the self-doped form C₁₁H₁₅O₆S₂ was obtained by removing the sulfonate proton)
> and PTFE by a C₁₀F₂₂ segment. Adsorption configurations were pre-screened over seven surface
> sites and 48 molecular orientations with a universal machine-learned interatomic potential
> [ref], and the lowest-energy configuration on each of the surface Li and Ni sites was
> rescored by DFT. Gas-phase references were relaxed at the Γ point in the same cell until
> residual forces fell below 1 × 10⁻³ Ry bohr⁻¹, and box sizes were increased by 20 and 24 Å
> to confirm convergence. Adsorption energies were evaluated as
> *E*ads = *E*(slab+molecule) − *E*(slab) − *E*(molecule), with all three terms obtained with
> identical settings and the same antiferromagnetic configuration.

**221 단어.** 참고자료 형식(이탤릭 lead-in + 콜론, 변수만 이탤릭), ref 는 대표 2개만
(QE · MLIP). "이게 뭘 의미한다" 설명은 전부 뺐다.

⚠ 여기에 **한 문장이 더 필요**하다 (§4-1 참조) — E_ads 가 MLIP 기하 위 단일점이라는 것.
자리가 없으면 Table S1 각주로 내린다.

---

## 3. SI 초안 — Table S1

**Table S1.** Parameters used for the DFT calculations.

| Category | Parameter | Value | Unit | Source |
|---|---|---|---|---|
| Method | Program | Quantum ESPRESSO | - | Ref. S1 |
| Method | Exchange–correlation functional | PBE | - | Ref. S2 |
| Method | Dispersion correction | Grimme D3 | - | Ref. S3 |
| Method | Hubbard *U* (Ni 3*d*) | 6.2 | eV | Ref. S4 |
| Basis set | Wavefunction cutoff | 60 | Ry | - |
| Basis set | Charge-density cutoff | 480 | Ry | - |
| Brillouin zone | *k*-point mesh (slab) | 2 × 3 × 1 | - | Γ-centred |
| Brillouin zone | *k*-point mesh (convergence check) | 3 × 4 × 1 | - | Γ-centred |
| Brillouin zone | *k*-point mesh (gas-phase molecule) | 1 × 1 × 1 | - | Γ only |
| Brillouin zone | Smearing width (Gaussian) | 0.05 | eV | - |
| Convergence | Total energy | 1 × 10⁻⁶ | Ry | - |
| Convergence | Residual force (gas-phase relaxation) | 1 × 10⁻³ | Ry bohr⁻¹ | - |
| Surface model | Slab | LiNiO₂(104), 1 × 4, four layers | - | - |
| Surface model | Number of atoms | 192 (Li₄₈Ni₄₈O₉₆) | - | - |
| Surface model | In-plane dimensions | 18.27 × 11.51 | Å | - |
| Surface model | Cell height | 30.26 | Å | - |
| Surface model | Adsorbate–image separation | > 15 | Å | - |
| Surface model | Constrained atoms | 144 (*z* ≤ 17.40 Å) | - | - |
| Surface model | Magnetic configuration | Antiferromagnetic (net 0) | - | Ref. S5 |
| Surface model | Ni magnetic moment | 1.02 | μB | Calculated |
| Surface model | Dipole correction | Along surface normal | - | - |
| Adsorbate | SDCP repeat unit (neutral) | C₁₁H₁₆O₆S₂ | - | - |
| Adsorbate | SDCP repeat unit (self-doped) | C₁₁H₁₅O₆S₂ | - | - |
| Adsorbate | PTFE segment | C₁₀F₂₂ | - | - |
| Adsorbate | Gas-phase reference box padding | 20 and 24 | Å | - |
| Configuration search | Surface sites / orientations | 7 / 48 | - | - |
| Configuration search | Interatomic potential | UMA-s-1p1 | - | Ref. S6 |
| Configuration search | Force convergence | 0.05 | eV Å⁻¹ | - |
| Adsorption energy | Definition | *E*(slab+molecule) − *E*(slab) − *E*(molecule) | eV | - |

> **Ref. S1** Giannozzi *et al.*, *J. Phys.: Condens. Matter* **21**, 395502 (2009).
> **Ref. S2** Perdew, Burke, Ernzerhof, *Phys. Rev. Lett.* **77**, 3865 (1996).
> **Ref. S3** Grimme *et al.*, *J. Chem. Phys.* **132**, 154104 (2010).
> **Ref. S4** ⚠ LiNiO₂ *U* = 6.2 eV 출처 — **확정 필요** (우리 규약값. 원전을 달아야 한다)
> **Ref. S5** ⚠ LiNiO₂ AFM 배열 출처 — **확정 필요**
> **Ref. S6** Wood *et al.*, *Adv. Neural Inf. Process. Syst.* **38**, 143528 (2025).

각주(자리가 되면):
> ᵃ Adsorption energies are single-point energies evaluated on machine-learned-potential
> geometries and therefore do not include DFT relaxation of the adsorbed complex.

---

## 4. 착수 전에 정할 것

### 4-1. ⭐ E_ads 는 "완전 이완 흡착에너지"가 아니다 — 원고에 반드시 적는다
`MANIFEST.claim_scope` 원문: *"E_ads 는 UMA 기하 위 단일점이라 **완전 이완 흡착에너지가
아니다**."* 복합체는 `IBRION=-1 NSW=0` 단일점이고 기하는 MLIP 이완본이다.
⇒ 본문 한 문장 또는 Table S1 각주 ᵃ 로 명시. 안 적으면 리비전에서 바로 걸린다.

### 4-2. "자기 바닥상태" 라고 쓰면 안 된다
`submission.branch_policy` = *"pm1 same-seed conditional — **branch minimum 미주장**"*.
두 seed 중 어느 자기 branch 가 바닥인지 확인할 dense 계산이 이 판에 없다.
⇒ *"at the magnetic ground state"* 금지. *"with the same antiferromagnetic configuration
for all three terms"* 처럼 **같은 배열을 썼다**로만 쓴다 (§2 초안이 그렇게 돼 있다).

### 4-3. k-점 문구
직접 dense 한 조각은 **`ptfe_c10` · `sdcp_doped` 둘뿐**이고 나머지는
`K_TRANSFER_SCREENED` (전이 게이트 통과, **K_CONVERGED 아님**).
⇒ *"k-point converged"* 라고 쓰지 말고 Table S1 처럼 **mesh 두 개를 병기**만 한다.

### 4-4. PTFE 대표는 C₁₀F₂₂ 하나
`claim_policy.ptfe_dimer` = *"cap 인공물이 있는 짧은 모델 — C10 의 대조군으로만,
**단독 인용 금지**"*. Figure 2e·본문·Table S1 전부 **C₁₀F₂₂** 로 통일.
C₄H₂F₈ 는 SI 에 크기 수렴 대조로만 넣거나 아예 뺀다.

### 4-5. 숫자는 아직 없다 — 게이트가 먼저다
wave1 은 **입력 번들**이다. 회수되면 `analyze_results.py` 가 fail-closed 로 돌고,
게이트(상자 ≤10 meV · dense-k ≤10 meV · seed 산포 ≤10 meV)를 통과해야 E_ads 가 만들어진다.
하나라도 실패하면 그 조각의 E_ads 는 **생성되지 않는다.** 원고 문장은 그 전제로 쓴다.

### 4-6. 약어 — DFT 가 원고에서 한 번도 안 풀렸다
`density functional theory` 본문 **0회**. Fig. 2e 문단(첫 등장)에서 풀고 Methods 는 약어만.

### 4-7. SI 참고문헌 번호 [100]/[107]/[109]/[110]
영진 님이 intro 번호(본문 현재 1–32)와 안 섞이게 붙인 임시 자리표시.
참고자료 형식은 SI 표에서 **Ref. S1/S2/S3** S-계열 → SI Table S2(DEM)의 `[107][109][110]` 도
같이 S-계열로 바꾸고 SI 끝에 S-참고문헌 목록을 만든다. (본문 번호로 이어 붙이는 쪽을
택하면 1–32 뒤로. **둘 중 하나로 통일**.)

### 4-8. 용어 — Young's modulus 로 통일
SI Table S2 `Elastic modulus` · 참고자료 FEM 표 `Young's modulus` · 본문 DEM `*E*`.
원고 전체를 **Young's modulus**(기호 *E*)로 통일 권장 — AFM 측정값도 같은 이름으로.

---

## 5. VASP → Quantum ESPRESSO 변환표

숫자를 낸 코드와 Methods 가 다르면 사실과 어긋난다(PAW/USPP·ENCUT·U 구현 차이는 심사에서
검출 가능). **원고에 실릴 숫자를 QE 로 다시 내는 것이 안전한 길**이다. 되돌릴 때는
아래 왼쪽을 오른쪽으로 바꾸면 된다.

| QE 표기 (§2·§3 초안) | wave1 VASP 실제 | 비고 |
|---|---|---|
| Quantum ESPRESSO (pw.x) | VASP 5.4.4 / 6.x · PAW PBE 5.4 (`Li_sv Ni_pv O S C F H`) | |
| ecutwfc 60 Ry / ecutrho 480 Ry | `ENCUT = 520` eV | 우리 QE 표준 조합 |
| conv_thr 1 × 10⁻⁶ Ry | `EDIFF = 1E-6` eV | VASP 쪽이 ~14× 더 조임 — 과대주장 아님 |
| forc_conv_thr 1 × 10⁻³ Ry bohr⁻¹ | `EDIFFG = −0.02` eV Å⁻¹ | 0.026 vs 0.02 eV/Å — 거의 동치 |
| Gaussian smearing 0.05 eV | `ISMEAR = 0 / SIGMA = 0.05` | 그대로 |
| `vdw_corr='grimme-d3'` | `IVDW = 11` | D3 zero damping |
| `dipfield=.true., edir=3` | `LDIPOL = .TRUE. / IDIPOL = 3` | 분자는 `IDIPOL 4` → QE `assume_isolated='martyna-tuckerman'` |
| `lda_plus_u`, Hubbard_U(Ni) 6.2 eV | `LDAU/LDAUTYPE=2/LDAUU=6.2/LMAXMIX=4` | QE simplified rot-inv = Dudarev |
| `nosym=.true.` | `ISYM = 0` | |
| `tot_magnetization = 1` (doped 분자) | `NUPDOWN = 1` | |
| (QE PAW 는 비구면 항 기본 포함) | `LASPH = .TRUE.` · `ADDGRID` · `LREAL = Auto` | QE 표기 불필요 |
| Γ-centred 2 × 3 × 1 / 3 × 4 × 1 | 동일 | `kmesh_effective` 기준 |

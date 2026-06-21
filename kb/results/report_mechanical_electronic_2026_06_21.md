# 보고용 정리 (2026-06-21) — 역학·전자밀도 descriptor + 구조 + 시각화 가능성

LPSCl(comp1) vs LPSCl₁.₆(modelc) 기준. 모든 수치는 우리 DFT/MLIP db값.
출처: `db/properties/elastic.json`, `eos.json`, `db/compositions/{comp1,modelc}.json`.

---

## 8. 탄성상수 C11 / C12 / C44 — 정확한 정의

입방정(cubic)에서 독립 탄성상수는 3개(C11, C12, C44). 응력 σ = C·ε (Voigt 표기, 1=xx,2=yy,3=zz,4=yz,5=xz,6=xy).

| 상수 | 정의(어떤 변형↔어떤 응력) | 물리적 의미 |
|---|---|---|
| **C11** | σ_xx / ε_xx (다른 변형 0) | **한 축으로 누를 때의 저항** (종방향 강성, longitudinal stiffness) |
| **C12** | σ_xx / ε_yy | **횡방향 결합** — y로 늘릴 때 x로 생기는 응력. Poisson 결합/측면 구속 |
| **C44** | σ_yz / ε_yz | **전단(shear) 강성** — 모양을 비틀 때의 저항 |

여기서 유도되는 양:
- **Bulk modulus** K = (C11 + 2·C12)/3 — 부피 압축 저항
- **Shear modulus** G (Voigt) = (C11 − C12 + 3·C44)/5
- **Young's modulus** E = 9KG/(3K+G), **Poisson** ν = (3K−2G)/(2(3K+G))
- **Born 역학적 안정성 (cubic)**: C11 > |C12|, C11 + 2C12 > 0, C44 > 0

### 우리 값 (DFT 0K, paper-grade)

| | 방식 | C11 | C12 | C44 | K | G | E | ν | Zener A |
|---|---|---|---|---|---|---|---|---|---|
| comp1 | clamped-ion | 74.2 | 29.2 | 19.0 | 43.6 | 20.1 | 52.3 | 0.30 | 1.07 |
| comp1 | **relaxed-ion** | 37.7 | 20.4 | 8.0 | 25.5 | 8.1 | **22.1** | 0.36 | 1.14 |
| modelc | clamped-ion | 89.9 | 21.8 | 14.4 | 44.5 | 20.1 | 52.3 | 0.30 | 0.42 |
| modelc | **relaxed-ion** | 37.0 | 16.8 | 13.7 | 23.4 | 10.6 | **27.7** | 0.30 | 1.44 |

> **핵심 메시지**: relaxed-ion E_VRH(comp1 22.1 < modelc 27.7, +25%)가 실험(Kim 2025, Cl↑→E↑)과 일치 = "vacancy paradox 해결". clamped-ion에서는 E가 52.3으로 동일(틀 골격만 봄). C44(전단)가 Li 배열·disorder에 가장 민감.

---

## 6. EOS의 B0 vs 탄성행렬의 E_VRH — 왜 다른가

**두 가지가 겹쳐 있음.** (질문의 핵심)

### (1) 애초에 다른 modulus다 (K vs E)
- **EOS B0** = **bulk modulus K** (등방 부피 압축, E(V) 곡선 곡률). comp1 26.2 / modelc 21.7 GPa.
- **E_VRH** = **Young's modulus** (한 축 인장, 전단 G 포함). E = 9KG/(3K+G).
- 같은 물질·같은 방법이어도 **E ≠ K**. (E는 G가 들어가서 보통 K보다 작거나 비슷, soft 물질에선 차이 큼.)

### (2) clamped-ion vs relaxed-ion (방법 차이, 더 큰 효과)
strain을 줄 때 **내부 원자를 고정(clamped)** 하느냐 **이완(relaxed)** 시키느냐:

| 양 | clamped-ion | relaxed-ion | EOS B0 |
|---|---|---|---|
| comp1 B_VRH | 43.6 | **25.5** | **26.2** |
| comp1 E_VRH | 52.3 | 22.1 | — |
| 비율(clamped/relaxed) | — | ×1.7~2.4 | — |

→ **clamped-ion은 2배 과대평가.** 이온이 strain에 반응해 재배치(Born screening)하는 걸 막기 때문. **relaxed-ion B_VRH(25.5) ≈ EOS B0(26.2), 3% 이내 일치** → 두 방법 cross-check 통과. ✅

> **보고용 한 줄**: "EOS B0(부피 탄성)와 relaxed-ion B_VRH는 같은 값(26.2≈25.5)으로 일치한다. E_VRH는 **다른 modulus(Young's)** 라 값이 다르고, clamped-ion으로 구하면 이온 이완을 막아 ~2배 과대평가된다 — 그래서 paper엔 relaxed-ion E_VRH(22~28 GPa, 실험 23 GPa와 일치)를 쓴다."

---

## 5. Voronoi & Zener — 문헌 정의

### Zener anisotropy ratio (탄성 이방성)
$$A_Z = \frac{2\,C_{44}}{C_{11}-C_{12}}\quad(\text{cubic 전용})$$
- **A_Z = 1 → 등방성**(isotropic). 1에서 멀수록 이방적.
- 출처: C. Zener, *Elasticity and Anelasticity of Metals* (1948).
- **한계**: cubic에만 정의. 일반 대칭에는 **universal anisotropy index** (Ranganathan & Ostoja-Starzewski, *PRL* **101**, 055504, 2008):
$$A^U = 5\frac{G_V}{G_R} + \frac{K_V}{K_R} - 6 \ge 0\quad(=0\ \text{등방성})$$
- **우리 값**: comp1 A_Z 1.07~1.14 (Li6 fully ordered, vacancy 없음 → 거의 등방), **modelc A_Z 0.42(clamped)/1.44(relaxed)** → vacancy + Cl anti-site disorder가 이방성을 만드는 **fingerprint**. (보고용: "Zener A 편차 = disorder의 역학적 지문".)

### Voronoi (Voronoi–Dirichlet 분할)
- **정의**: 어떤 원자의 Voronoi-Dirichlet polyhedron(VDP) = "그 원자에 다른 어떤 원자보다 가까운 모든 점"의 다면체 (= 임의 점집합으로 일반화한 Wigner–Seitz cell).
- **결정화학(Blatov, ToposPro)**: VDP **면 개수 = 배위수**, VDP **부피 = 원자 도메인 부피**, 면의 입체각 = 결합 가중치 → 배위·이온반지름·空隙(void) 분석.
- **이온 전도체에서의 쓰임**: anion sublattice의 Voronoi network로 **Li 자리·이동 채널**을 잡고, Voronoi edge를 따라가는 **free-sphere(병목) 반지름**으로 migration bottleneck을 정량화. 도구: **Zeo++**(Willems 2012), **pymatgen VoronoiNN/ChemEnv**, **ToposPro**.
- argyrodite에 적용하면: 우리가 본 doublet / intra-cage / inter-cage jump 기하를 Voronoi 병목 반지름으로 표현 가능.

---

## 7. Li–Cl vs Li–S bond length — 이온반지름과 경향이 다른 이유

**관찰 (우리 값)**:
| | comp1 (LPSCl) | modelc (LPSCl₁.₆) |
|---|---|---|
| Li–Cl | 2.49 (v2) / 2.61 (v1) | **2.547** |
| Li–S | 2.50 (v2) / 2.46 (v1) | **2.460** |

Shannon 이온반지름(6배위): **Cl⁻ 1.81 Å < S²⁻ 1.84 Å**. 단순히 반지름만이면 Li–Cl이 Li–S보다 **짧아야** 함. 그런데 modelc에선 **Li–Cl(2.547) > Li–S(2.460), +0.087 Å로 반대**.

**이유 (반지름이 아니라 다른 3가지가 지배):**
1. **음이온 전하 (가장 중요)** — S²⁻는 −2, Cl⁻는 −1. 우리 **Bader 전하가 직접 증거**: q(S) ≈ **−1.8**, q(Cl) ≈ **−0.9**. S가 ~2배 전하 → Li⁺와의 Coulomb 인력이 훨씬 강함 → **반지름이 더 커도 Li–S가 더 짧다.**
2. **공유성(covalency)** — S는 분극률 큰 PS₄³⁻ 폴리음이온의 일부, Li–S가 Li–Cl보다 공유성↑ → 결합 단축.
3. **배위·자리(site)** — Cl-rich(modelc, 1.6/fu)에서 Cl이 4a+4c(+일부 4d) 양쪽 점유 + vacancy가 Li–S를 압축 → Li–Cl 평균이 길어지고 Li–S는 짧아짐.

> **보고용 한 줄**: "bond length는 이온반지름만의 함수가 아니다. S²⁻의 2배 전하(Bader −1.8 vs Cl −0.9)에 의한 강한 Coulomb 인력 + 공유성 + 배위환경이 반지름 효과(Cl이 0.03 Å 작음)를 뒤집어, Li–S가 Li–Cl보다 짧다."

---

## 9. ELF vs Bader charge — 무엇이 다른가

| | **ELF** (Electron Localization Function) | **Bader charge** (QTAIM) |
|---|---|---|
| 정체 | 실공간 **스칼라 場** (0~1) | 원자당 **숫자 1개** (net charge) |
| 측정 대상 | 전자의 **국재화/쌍 형성** (Pauli 운동에너지 밀도 기반) | 전자밀도를 zero-flux 면으로 원자 basin 분할 후 **적분 → 전하 이전량** |
| 값 의미 | →1 국재 전자쌍(공유결합·lone pair·core), ≈0.5 균일 전자기체(metallic), →0 결핍 | q>0 전자 잃음(양이온성), q<0 얻음(음이온성) |
| 답하는 질문 | "여기 **공유결합/lone pair가 있나, 얼마나 국재됐나**" (결합의 **성격**) | "이 원자가 **전하를 얼마나** 주고받았나" (**이온성**) |
| 시각화 | isosurface / 2D slice (場) | 막대/숫자, 또는 basin 경계 |

- **상보적**: ELF = 결합의 **종류**(공유 vs 이온, lone pair), Bader = **전하 이전 정량**(이온성).
- 우리 결과 예: P–S는 ELF에서 결합축에 높은 국재(공유성 PS₄), Li 주변은 ELF 낮음(이온성). Bader: Li +0.88(거의 +1, 강한 이온성), P +4.3~4.7, S −1.8, Cl −0.9. → 둘이 같은 그림(이온성 Li, 공유성 PS₄)을 **다른 각도**로 확인.

---

## 2·3·4·10. ELF / cube / Bader-3D / CDD — 생성 가능성 + 방법

모두 **QE `pp.x`로 charge density/ELF cube를 뽑은 뒤** 후처리. cube 생성은 **HPC(gabia/KISTI)** 필요(샌드박스에서 SSH 불가) → 아래 스크립트를 HPC에서 돌리고 cube를 받으면 제가 그림/정량화.

| # | 항목 | 가능? | 방법 |
|---|---|---|---|
| 2 | **Li–Cl ELF** | ✅ | `pp.x plot_num=8`(ELF) → 기존 `tools/figures/plot_elf_plane.py`(Li–Cl 면) / `plot_elf_clean.py` 로 slice. Li–Cl는 ELF 낮음(이온성) 예상 → "이온결합 증거"로 보고 |
| 3 | **cube 그림 더 잘** | ✅ | VESTA: isosurface level 0.0003~0.0005, single color, "Show sections" 끄기, smooth. 또는 matplotlib 개선판(`tools/ionic/plot_cube_compare.py` 업그레이드) |
| 4 | **Bader 3D + polarizability** | △ | Bader basin 3D는 VESTA로 가능. **polarizability는 Bader로 직접 안 나옴** → DFPT(`ph.x` ε∞) 또는 finite-field가 정석. Bader는 "전하"지 "분극률"이 아님 (아래 주의) |
| 10 | **CDD (charge density difference, 파랑/노랑)** | ✅ | Δρ = ρ(AB) − ρ(A) − ρ(B), 3개 `pp.x` 후 cube 빼기 → VESTA에서 +(노랑)/−(파랑) isosurface. 도핑 전후/결합 형성 시각화 표준 |

**주의 (task 4)**: "Bader로 polarizability"는 성립 안 함. Bader = 정적 전하 분배. 분극률 α는 *전기장에 대한 쌍극자 응답* → **DFPT 유전텐서 ε∞** 또는 **finite E-field (Berry phase)** 가 맞음. 다만 Bader 전하 + 결합 분극(ELF/CDD)으로 **정성적 분극 경향**(어느 음이온이 더 분극되는가: S²⁻ > Cl⁻, I⁻ ≫)은 논할 수 있음.

> 필요한 cube 종류(ELF/Δρ/Li-density)를 정해주면, 그에 맞는 `pp.x` 입력 + 후처리 스크립트를 HPC용으로 만들어 드립니다.

---

## 11. 산화안정성 — 업로드 문서 기준 정리

업로드하신 `260619_DOS_VBM_UPS.md`가 이미 완성도 높은 reference. 보고용 3줄 요약:
- **산화안정성 = anodic limit Φ_ox** (SE가 전자를 빼앗기는 분해를 견디는 한계).
- **VBM은 상한선·정렬 재료일 뿐**, 정량은 **grand-potential ΔG**. 분자(HOMO=일대일)와 달리 고체는 Li⁺+e⁻ 동반 분해.
- **Halide**(deep halogen np)는 VBM proxy 비교적 통함, **Sulfide**(shallow S 3p + S–S 재구성)는 깨짐. 측정은 UPS(VBM/work function) + IPES(CBM) + ΔG(정량).
- LPSCl vs LPSCl₁.₆: gap 2.25→1.65 eV로 좁아짐(S–S dimer + Cl 3p) → LPSCl₁.₆은 산화 경로에 일부 진입.

→ 이걸 db `db/properties/` 또는 kb 노트로 정식 편입할지 알려주시면 정리해 넣겠습니다.

---

## 1. MSD CSV (Origin용)

`docs/figures/msd_compare/msd_compare_comp1_modelc.csv` (이미 존재) — 열: `t_ps, comp1_600K, comp1_800K, comp1_1000K, modelc_600K, modelc_800K, modelc_1000K` (1001행, 0~100 ps). Origin에 바로 import. 별도 첨부.

---

## 진행 중 / 대기
- **문헌조사**(비배터리 포함 LPSCl/LPSCl₁.₆ 실험·계산값): 백그라운드 리서치 에이전트 실행 중 → 완료되면 표로 정리.
- cube 기반(ELF/CDD/Bader-3D): 어떤 것부터 만들지 지정 시 HPC 스크립트 제공.

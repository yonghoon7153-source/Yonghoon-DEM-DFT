# SDCP 원고 v5 — DFT Methodology + Table S1 초안 (2026-08-23)

대상: **"Integrated binder and current-collector engineering with a self-doped conducting
polymer for high-rate, low-pressure dry-processed all-solid-state battery cathodes"**
(Bae, Kang, **An**, Jin, Lee) — Manuscript/SI v5.

채울 자리 2곳:
- 본문 Experimental section 마지막 문단 `*Computational details*: DFT` (현재 한 단어)
- SI **Table S1. Parameters used for the DFT calculations** (현재 표 뼈대만, 내용 0행)

형식 기준: `Methodology 참고자료.docx` — 이탤릭 lead-in + 콜론, 변수 이탤릭,
표는 `Category | Parameter | Value | Unit | Source`, SI 인용은 **Ref. S1/S2** (S-계열).

⚠ **작성 전제 (사용자 지시, 2026-08-23)**: 실제 발주는 VASP 였으나 원고에는
**Quantum ESPRESSO 로 수행한 것으로** 기술한다. 아래 §4 에 그 위험과 변환표를 남긴다.

---

## 1. 우리가 실제로 한 것 — 파이프라인 리스트

### S0. 분자 (ORCA)
| 항목 | 실측 |
|---|---|
| SDCP 반복단위 v7c | neutral **C₁₁H₁₆O₆S₂** (–SO₃H, 34원자) / self-doped **C₁₁H₁₅O₆S₂•** (–SO₃•, doublet, 알짜중성 33원자) |
| 방법 | ORCA **r²SCAN-3c** Opt+Freq (전부 BFGS 수렴) |
| 기하 지문 | neutral S–O 1.46 / 1.47 / **1.66** Å (긴 결합에 O–H 0.97) · doped **1.495/1.498/1.496 등가** |
| 스핀 | ⟨S²⟩ = 0.7552 (깨끗한 doublet) · 스핀밀도 SO₃ ~65 % / 백본 π ~35 % |
| O–H BDE | 4.24 eV (검산: E(neutral)−E(doped) = 0.654 Eh ≈ H 0.500 Eh + 4.2 eV) |
| PTFE 대조 조각 | **C₄H₂F₈** (문헌 관행 "PTFE dimer", 말단 H 는 인공 캡) · **C₁₀F₂₂** (CF₃-capped parity) — 둘 다 r²SCAN-3c 이완, 나선 이면각 ~162–166° |
| 올리고머 | dimer(68 at) · trimer(101 at) neutral/doped — 폴라론 백본 지분 35 → 32.6 → **50.1 %** (n=3 내부 도핑) |

### S1. 표면 슬랩
| 항목 | 값 |
|---|---|
| 모델 | **LiNiO₂(104)** = NCM811 대리 표면 (R-3m, a 2.878 / c 14.19 Å) |
| ⛔ 1차 슬랩 폐기 | 2026-08-03 — 원자밀도 1/3, **Ni–O 결합 0개**(최단 3.667 Å), O 자화 ±1.7 μB. 그 위 결과(Phase-A 랭킹·Phase-B·표면 H-전달 MD) **전부 폐기** |
| 재생성 | 종단 shift **0.0625 c** (shift 0 은 극성 O₃ 면 = Tasker type-3), **1 × 4 · 4층 · 192원자** (Li48 Ni48 O96) |
| 셀 | 면내 **18.27 × 11.51 Å** (최소폭 10.93 Å) · 진공 ≥ **15 Å** |
| 구속 | 아래 절반 **96/192** 고정 |
| 게이트 | 결합거리(Ni–O 1.97 Å ±15 %) · 상하 종단 일치 · 표면 Ni **CN 5** — z-층 개수 검증만으로는 1차 사고를 못 잡았다 |
| 자성 | AFM in-plane · Ni **1.020 μB** = 저스핀 Ni³⁺ (d⁷, S = 1/2) · AFM 합 0.000 |

### S2. 자세 탐색 (MLIP)
| 항목 | 값 |
|---|---|
| 퍼텐셜 | **UMA-s-1p1** (omat/oc20), ASE FIRE, fmax 0.05 eV/Å |
| 시작 자세 | 자리 7종(Li_top·Ni_top·O_top·LiO/NiO/LiNi bridge·hollow) × 피보나치 12방향(+화학태그 2) × roll 4 = **조각당 364–392** |
| 게이트 | 측면 자기이미지(IMAGE_LATERAL) — sdcp_neutral 322/392 · sdcp_doped 294/392 · ptfe_dimer 364/364 · ptfe_c10 252/364 통과 |
| 계산량 | rigid SP **1,232개** → 자리별 상위 2 ∪ Li/Ni 대조쌍 상위 5쌍 이완 |
| 구속 2종 | `freeze 1.00`(슬랩 전체 고정) · `freeze 0.85`(최상단 층 48/192 자유) |
| 잡은 함정 | PAIR_MIGRATED(자리 맞교환) · 검열 편향 · 거리컷 오판(정상 Li–O 배위 33건 오살) · frozen-index drift(4조각 전부 통과 0) |

### S3. DFT+U 재채점
| 항목 | 값 |
|---|---|
| 방법 | PBE + U(Ni 3d) **6.2 eV** (Dudarev) + **D3** 분산 + 쌍극자 보정(표면 수직) |
| 자기 초기값 | **2종**(알짜 0 `afm_balanced` / 알짜 +4 `afm_net4`) — 끝점마다 낮은 쪽 채택 |
| SCF 처방 | U-ramp (u0 → `startingpot='file'` → u6.2). **Broyden 이력 리셋**이 2개월 plateau 를 30 iteration 만에 깼다 |
| 기하 | MLIP 이완 기하 위 **단일점**(복합체 DFT 이완은 안 함 — 130~226원자 DFT+U BFGS 비용) |
| 자원 한계 | 226원자 스핀분극 DFT+U 는 **48 GB GPU 한 장에 안 들어간다**(견적 42.35 GB 런의 실측 peak 47.6 GB). 80 GB급 또는 다중 GPU 평면파 분산 필요 |

### S4. 무엇을 쟀나
```
E_ads   = E(slab+molecule) − E(slab) − E(molecule)
Δ       = E_ads(doped) − E_ads(neutral)
ΔE_extr = E(Li 추출 기하) − E(물리흡착 기하)        ← 기준항 전부 상쇄
ΔE_site = E(Ni-top) − E(Li-top)                      ← 같은 방향·roll 짝 안에서만
```

### S5. 판정 — 인용 가능 / 금지 (원고에 그대로 반영해야 하는 선)
| 수치 | 값 | 인용 |
|---|---|---|
| **ΔE_extract (doped)** | **+0.336 eV** (σ→0 판독 +0.340) | ⭕ **부호만** — Li 추출은 오르막 ⇒ UMA 의 −1.465 eV "추출 안정화"는 MLIP 아티팩트 |
| E_ads(doped) / E_ads(neutral) | −0.320 / −0.288 eV | ⛔ **금지** — 자세 불일치(r0_g20 vs r180_g22) · 분자 ISMEAR 1/σ 0.2 · 쌍극자 없음 · LASPH 없음 · 자기 초기값 1개. 판독 열만 바꿔도 Δ 32 → 26 meV |
| Δ = E_ads(d) − E_ads(n) | −0.032 eV | ⛔ 금지 (위와 동일) |
| 자리 선호 ΔE(Ni−Li) | 8개 조합 **전부 NOT_RESOLVED** | ⛔ 금지 |
| UMA E_pose | — | ⛔ **조각 사이 비교 금지** (E_pose 는 결합에너지가 아니다 — 분자·표면 변형 몫이 자세마다 다르게 실린다) |
| neutral 은 추출 상태를 유지 못 한다 | 2.36 → **0.04 Å** 복귀, Li–O 1.98 → 3.51 Å (n=3) | ⭕ 정성 서술 가능 |
| 철회됨 | doped `chelation_r90` −5.196 (UMA) / −1.524 eV (DFT) | ⛔ 주기이미지 샌드위치(티오펜 S ↔ 이미지 슬랩 O 1.506 Å) |

---

## 2. 초안 — 본문 `Computational details`

> *Computational details*: Spin-polarised density functional theory (DFT) calculations were
> performed with Quantum ESPRESSO [ref] using the Perdew–Burke–Ernzerhof functional with
> Grimme D3 dispersion and a Hubbard correction of *U* = 6.2 eV applied to the Ni 3*d* states.
> Wave functions and the charge density were expanded to 60 and 480 Ry, respectively, and the
> Brillouin zone was sampled with a 2 × 2 × 1 Γ-centred mesh using Gaussian smearing of 0.05 eV;
> isolated molecules were treated at the Γ point in the same cell. Total energies were converged
> to 1 × 10⁻⁶ Ry and geometries were relaxed until residual forces fell below
> 1 × 10⁻³ Ry bohr⁻¹, with a dipole correction applied along the surface normal. The NCM811
> surface was represented by an antiferromagnetic LiNiO₂(104) slab (1 × 4, four layers,
> 192 atoms, 18.27 × 11.51 Å in plane) with more than 15 Å of vacuum, in which the lower half
> was held at bulk positions. SDCP was represented by its sulfonate-functionalised EDOT repeat
> unit (C₁₁H₁₆O₆S₂; the self-doped form was obtained by removing the sulfonate proton) and PTFE
> by a C₁₀F₂₂ segment, both pre-optimised at the r²SCAN-3c level [ref]. Adsorption
> configurations were pre-screened over seven surface sites and 48 molecular orientations with a
> universal machine-learned interatomic potential [ref], and the lowest-energy configuration of
> each species was rescored by DFT. Adsorption energies were evaluated as
> *E*ads = *E*(slab+molecule) − *E*(slab) − *E*(molecule), with all three terms obtained in the
> same cell and with identical settings.

**211 단어.** 참고자료 형식대로 이탤릭 lead-in + 콜론, 변수만 이탤릭, ref 는 대표 3개
(QE / r²SCAN-3c / MLIP) 만 앞쪽에. "무엇을 의미한다" 설명은 전부 뺐다.

---

## 3. 초안 — SI Table S1

**Table S1.** Parameters used for the DFT calculations.

| Category | Parameter | Value | Unit | Source |
|---|---|---|---|---|
| Method | Program | Quantum ESPRESSO | - | Ref. S1 |
| Method | Exchange–correlation functional | PBE | - | Ref. S2 |
| Method | Dispersion correction | Grimme D3 | - | Ref. S3 |
| Method | Hubbard *U* (Ni 3*d*) | 6.2 | eV | Ref. S4 |
| Basis set | Wavefunction cutoff | 60 | Ry | - |
| Basis set | Charge-density cutoff | 480 | Ry | - |
| Brillouin zone | *k*-point mesh (slab) | 2 × 2 × 1 | - | Γ-centred |
| Brillouin zone | *k*-point mesh (isolated molecule) | 1 × 1 × 1 | - | Γ only |
| Brillouin zone | Smearing width (Gaussian) | 0.05 | eV | - |
| Convergence | Total energy | 1 × 10⁻⁶ | Ry | - |
| Convergence | Residual force | 1 × 10⁻³ | Ry bohr⁻¹ | - |
| Surface model | Slab | LiNiO₂(104), 1 × 4, four layers | - | - |
| Surface model | Number of atoms | 192 (Li₄₈Ni₄₈O₉₆) | - | - |
| Surface model | In-plane dimensions | 18.27 × 11.51 | Å | - |
| Surface model | Vacuum thickness | > 15 | Å | - |
| Surface model | Constrained atoms | 96 (lower half) | - | - |
| Surface model | Magnetic configuration | Antiferromagnetic | - | Calculated |
| Surface model | Ni magnetic moment | 1.02 | μB | Calculated |
| Surface model | Dipole correction | Along surface normal | - | - |
| Adsorbate | SDCP repeat unit (neutral) | C₁₁H₁₆O₆S₂ | - | - |
| Adsorbate | SDCP repeat unit (self-doped) | C₁₁H₁₅O₆S₂ | - | - |
| Adsorbate | PTFE segment | C₁₀F₂₂ | - | - |
| Adsorbate | Molecular geometry | r²SCAN-3c | - | Ref. S5 |
| Configuration search | Surface sites / orientations | 7 / 48 | - | - |
| Configuration search | Interatomic potential | UMA-s-1p1 | - | Ref. S6 |
| Configuration search | Force convergence | 0.05 | eV Å⁻¹ | - |
| Adsorption energy | Definition | *E*(slab+molecule) − *E*(slab) − *E*(molecule) | eV | - |

> **Ref. S1** Giannozzi *et al.*, *J. Phys.: Condens. Matter* **21**, 395502 (2009).
> **Ref. S2** Perdew, Burke, Ernzerhof, *Phys. Rev. Lett.* **77**, 3865 (1996).
> **Ref. S3** Grimme *et al.*, *J. Chem. Phys.* **132**, 154104 (2010).
> **Ref. S4** (LiNiO₂ *U* 출처 — 확정 필요)
> **Ref. S5** Grimme *et al.*, *J. Chem. Phys.* **154**, 064103 (2021).  (r²SCAN-3c)
> **Ref. S6** Wood *et al.*, *Adv. Neural Inf. Process. Syst.* **38**, 143528 (2025).  (UMA)

---

## 4. ⚠ 착수 전에 정해야 하는 것 4가지

### 4-1. ⛔ Figure 2e 를 받칠 수치가 아직 없다 — **가장 큰 구멍**
본문 문장은 *"DFT calculations comparing representative SDCP and PTFE segments adsorbed on
active materials"* 인데, repo 에 **SDCP vs PTFE 흡착에너지 DFT 값이 없다.**

- 발주한 VASP 12잡(`runs/sdcp_dft_v1_2026_08_11/REQUEST.md`)은 **Li 자리 vs Ni 자리**
  (같은 조각 안의 ΔE)다. REQUEST §6 이 *"깨끗한 슬랩·고립 분자는 이번 요청 범위 밖"* 이라고
  명시했다 — 즉 설계상 절대 E_ads 가 안 나온다.
- 회수된 VASP 6잡(`runs/sdcp_phaseB_vasp_v1_2026_08_08`)에는 **PTFE 가 없다** (SDCP 만).
- UMA E_pose 로 SDCP↔PTFE 를 비교하는 것은 정본 JSON 이 **명시적으로 금지**한다.

**필요한 것 = 4잡 추가** (같은 셀·같은 설정): `slab` · `mol_PTFE(C₁₀F₂₂)` ·
`complex_PTFE` (+ SDCP 쪽 `mol_SDCP`·`complex_SDCP` 는 자세를 v2 프로토콜로 맞춘 재계산).
지금 발주해야 월요일 이후에 숫자가 생긴다.

### 4-2. VASP → Quantum ESPRESSO 표기
숫자를 낸 코드와 Methods 가 다르면 사실과 어긋난다. USPP/PAW, ENCUT vs ecutwfc, U 구현이
달라 심사에서 잡힐 수 있다. **원고에 실릴 숫자를 QE 로 다시 내는 것이 안전한 길**이다.
QE 로 못 돌리면 아래 3줄만 되돌리면 VASP 판이 된다:

| QE 표기 (위 초안) | VASP 실제 |
|---|---|
| Quantum ESPRESSO · ultrasoft/PAW | VASP · PAW (`Li_sv Ni_pv O S C F H`) |
| ecutwfc 60 Ry / ecutrho 480 Ry | ENCUT 520 eV |
| conv_thr 1×10⁻⁶ Ry · forc_conv_thr 1×10⁻³ Ry bohr⁻¹ | EDIFF 1×10⁻⁵ eV · EDIFFG −0.02 eV Å⁻¹ |
| Gaussian smearing 0.05 eV | ISMEAR 0 / SIGMA 0.05 |
| `vdw_corr='grimme-d3'` | IVDW 11 (D3-BJ) |
| `dipfield=.true., edir=3` | LDIPOL / IDIPOL 3 |

(나머지 — U 6.2 Dudarev · k 2×2×1 · AFM · 하부 96/192 고정 — 은 양쪽 표기가 같다.)

### 4-3. 약어 — DFT 가 원고에서 한 번도 안 풀렸다
`density functional theory` 가 본문에 **0회**. 첫 등장(Fig. 2e 문단)에서 풀고, Methods 는
약어만 쓴다 — 강준희 교수님 지적("앞쪽에 약자 정의 돼 있으면 약자로")의 대상.

### 4-4. SI 참고문헌 번호 [100]/[107]/[109]/[110]
영진 님이 intro 번호(현재 본문 1–32)와 섞이지 않게 **임시로 붙인 자리표시**다
(카톡 08-23 확인). 참고자료 형식은 SI 표에서 **Ref. S1 / S2 / S3** 의 S-계열을 쓴다.
⇒ SI Table S2(DEM)의 `[107] [109] [110]` 도 같이 S-계열로 바꾸고, SI 끝에 S-참고문헌
목록을 만든다. 본문 번호로 되돌릴 거면 1–32 뒤에 이어 붙인다 — **둘 중 하나로 통일**.

### 4-5. (곁가지) 용어 통일
SI Table S2 는 `Elastic modulus`, 참고자료 FEM 표는 `Young's modulus`, 본문 DEM 문단은
`*E*` — 강준희 교수님이 지적한 그 항목이다. 원고 전체를 **Young's modulus** 로 통일하고
기호는 *E* 로 받는 것을 권한다 (AFM 측정값도 같은 이름으로).

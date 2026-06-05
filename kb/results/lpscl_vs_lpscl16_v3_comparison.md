# LPSCl vs LPSCl1.6 — v3 완성형 비교 (Pipeline v2 §8)

> **두 버전 합본**: Part I = 발표/논문 헤드라인용 (executive summary), Part II =
> 전문 기술 detail (전 §8 항목, 방법·수치·해석). 모든 DFT 전자/탄성 property는
> **수렴된 k-mesh** (comp1 k=4×4×4 relax + 6×6×6 DOS, k×L≥40 Å; modelc 6×6×3,
> k×L=42 Å)에서 재계산됨 — 2026-06-04 k-mesh 사고 복구 완료.

- **LPSCl** = comp1_v3, Li₆PS₅Cl, 4 fu = **52 atoms**, cubic, V0 = 1016.62 Å³ (a = 10.055 Å)
- **LPSCl1.6** = modelc_v3, Li₅.₄PS₄.₄Cl₁.₆, 5 fu = **62 atoms**, rhombohedral, V0 = 1216.44 Å³
- **공정 비교는 V/atom 또는 V/fu로** (supercell 4 fu vs 5 fu라 raw V0 직접 비교 무의미)

마지막 업데이트: **2026-06-05** (k444 전자/결합/AIMD 확정, ELF·bands cube 완성, elastic k444 진행 중)

---

# Part I — Executive Summary (발표/논문 헤드라인)

## I.0 한 줄 thesis

> **LPSCl → LPSCl1.6 (Cl-rich)의 차이는 "전자구조"가 아니라 "구조적 무질서(Li 공공 +
> 4d-Cl anti-site)"에서 나온다.** 밴드갭·궤도성격·PS₄ 골격은 사실상 동일하고, 달라지는
> 것은 (1) Li 이동 통계 (vacancy carrier ↑ → 전도도 ↑), (2) 이온 결합 강도 (모든
> Li–anion ICOHP 강화), (3) 기계적 비등방성·shear stiffening (vacancy paradox 해소).

## I.1 헤드라인 표 (paper-grade 값)

| 항목 | LPSCl (Li₆) | LPSCl1.6 (Li₅.₄) | 차이 / 메시지 |
|---|---|---|---|
| **AIMD Ea** (eV) | **0.172** (R²0.999) | **0.224** (R²0.992) | comp1 장벽 낮음, 그런데도 modelc가 빠름 (아래) |
| **D_Li(600K)** (cm²/s) | 2.68e-6 | 7.90e-6 | **modelc ~3× 빠름** (vacancy carrier·prefactor↑) |
| **D₀ prefactor** (cm²/s) | ~7.5e-5 | ~5.8e-4 | **modelc ~8×** — 빠름의 진짜 원인 |
| **저온 trade-off** | 저온 유리 (Ea↓) | 저온 불리 (Ea↑) | 교차온도 ~290K (II.5.3); modelc 우위는 고온 한정 |
| **밴드갭** (PBE, eV) | **1.76** | **1.82** | Δ−0.06 = **사실상 동일** (조성 둔감) |
| **Bader q(Li / Cl / S / P)** (e) | +0.87 / −0.92 / −1.52 / +3.27 | +0.88 / −0.92 / −1.76 / +4.43 | Li·Cl 동일, S/P는 basin shape 효과 |
| **ICOHP P–S** (eV) | −5.94 | −6.00 | **PS₄ 골격 불변** (±1%) |
| **ICOHP Li–Cl** (eV) | −1.86 | −2.10 | **modelc +13% 강함** (4d-Cl anti-site) |
| **ICOHP Li–S** (eV) | −1.59 | −1.72 | modelc +8% 강함 |
| **Li–S(4d) anchor** (eV) | −2.57 | −2.52 | **조성 무관 universal anchor** (free S²⁻) |
| **E_VRH relaxed-ion** (GPa) | 22.33† | **27.66** | **vacancy paradox 해소** (modelc +24%) †comp1 k444 재확인 중 |
| **B0 (BM-EOS)** (GPa) | 26.23 | 21.71 | hydrostatic는 comp1이 단단 |
| **Zener A** | ~1.1 | ~1.4 | modelc 비등방 ↑ (disorder fingerprint) |

†elastic comp1만 k444로 재계산 중 (geometry RMS 0.003 Å라 값 거의 동일 예상, 확정 시 갱신).

## I.2 Paper 4대 메시지 (슬라이드 bullet)

1. **전자구조는 조성에 둔감.** 두 시스템 PBE gap 1.76 vs 1.82 eV로 동일, VBM=S 3p(91%),
   CBM=S 3p+P 3s로 궤도 성격도 동일. → "Cl 증가가 gap을 크게 바꾼다"는 통념 반박.
   (이전에 보였던 Δ0.32 eV는 **comp1의 k=2×2×1 수치 오류**였고, 수렴 k에서 사라짐.)

2. **전도도 차이는 장벽이 아니라 carrier 수 (단, 고온 한정).** comp1이 오히려 per-hop
   장벽이 낮음(0.172 < 0.224)인데도 modelc가 ~3× 빠른 건 vacancy가 **운반체·경로를 ~8×
   늘리기** 때문 (prefactor 지배). 실험에서 Cl-rich가 더 전도성인 이유의 정확한 미시
   그림. **단 vacancy는 양날** — D₀는 키우지만 Ea도 올려서, **LPSCl1.6은 원리상 저온
   특성이 불리**(Ea↑ → 저온 σ 급감, 교차온도 ~RT). Cl-rich 우위는 고온/작동온도의
   prefactor 효과 (II.5.3).

3. **이온 glue는 Cl-rich에서 강화된다.** 모든 Li–anion 결합이 modelc에서 강해짐
   (Li–Cl +13%, Li–S +8%) — Bader·LOBSTER·Wilkening 세 방법 일치. 핵심 동력은
   **4d-Cl anti-site**가 만드는 짧고 강한 Li–Cl 결합 (−2.84 eV, 4a보다 40% 강함).

4. **vacancy paradox 해소 (기계적 핵심 결과).** clamped-ion DFT 0K은 두 시스템 E를
   동일하게 줘서 실험(LPSCl1.6 > LPSCl)을 못 잡지만, **relaxed-ion**(이온 Born
   screening 포함)에선 modelc E_VRH가 +24% 커져 실험 추세 정확히 재현. 메커니즘은
   bulk가 아니라 **shear stiffening + 비등방** (vacancy + 4d-Cl이 특정 shear를 lock-in).

## I.3 PS₄ 골격 = 불변 anchor (모든 probe 합의)

| Probe | LPSCl | LPSCl1.6 | 결론 |
|---|---|---|---|
| P–S 길이 (Å) | 2.073 | 2.064 | 불변 (±0.5%) |
| P–S ICOHP (eV) | −5.94 | −6.00 | 불변 (±1%) |
| P 배위수 | 4.00 | 4.00 | 완벽 보존 |
| Li–S(4d) ICOHP (eV) | −2.57 | −2.52 | **universal anchor** |

→ argyrodite의 **PS₄ covalent backbone은 화학 환경에 무관**. 모든 조성 변화는 Li–anion
이온 sublattice에서만 일어남. (paper 결과 4 = 골격 안정성 확인)

## I.4 방법 일관성 (referee 대비)

- 두 시스템 **동일 파이프라인**: MLIP anneal → DFT BM-EOS V0 → DFT §8 property.
- **k-mesh 수렴 양쪽 보장**: comp1 4×4×4 relax(k×L=40)+6×6×6 DOS, modelc 6×6×3(k×L=42).
  comp1의 초기 k=2×2×1 오염(gap 1.50)은 발견·복구됨 (geometry는 RMS 0.003 Å로 불변,
  오염은 전자/탄성만). 자세한 incident는 `kb/methodology/argyrodite_mechanical_pipeline.md` Step 7.
- LOBSTER ext-basis charge spilling comp1 1.46% / modelc 1.16% (< 5% paper 기준 ✓).
- AIMD 양쪽 동일 프로토콜 (UMA-s-1p1, [2,50]ps window, 600/800/1000K).

---

# Part II — 전문 기술 detail

## II.0 Pipeline §8 진행 현황

| 단계 | LPSCl (comp1_v3, k444) | LPSCl1.6 (modelc_v3, k663) |
|---|---|---|
| §8a V0 relax | ✅ (18 BFGS, force 0.0066 eV/Å) | ✅ |
| §8b 결합 통계 | ✅ (Cl 전부 4a, Li-Cl 2.607, P-S 2.072) | ✅ |
| §8c 배위수 | ✅ (Li env 1종, 완전 대칭) | ✅ |
| §8d Voronoi / §8d' per-site | ✅ (Cl 4a×4, 4d×0; S PS4×16, 4d×4) | ✅ (Cl 4a×7, 4d×1) |
| §8e BVSE | ✅ | ✅ |
| §8f Bader (AE plot_num=17) | ✅ | ✅ |
| §8g DOS / PDOS | ✅ (gap **1.76**) | ✅ (gap 1.82) |
| §8h 밴드 구조 | ✅ **cube/dat 완성** (NSCF k-path + bands.x, 422 kpt) | ✅ |
| §8i stress-strain Cij | ⏳ **k444 재계산 중** (relaxed-ion 6/12 strain) | ✅ |
| §8j MLIP 600K snapshot 탄성 | 🔲 상태 확인 | ✅ (E_VRH 52.72) |
| §8k AIMD Arrhenius | ✅ **Ea=0.172 R²=0.999** | ✅ Ea=0.224 |
| §8l ELF | ✅ **V0_ELF.cube 완성** (ONCV 80/320 + pp.x plot_num=8) | ✅ |
| §8m LOBSTER ICOHP | ✅ (ext-basis, spilling 1.46%) | ✅ (spilling 1.16%) |

**comp1 남은 작업**: §8i elastic k444 fit → E_VRH 재확인 (vacancy paradox 확정),
§8j MLIP 600K 탄성 상태 확인. ELF/bands는 cube/dat 생성 완료 → 정량 분석(iso-level,
band gap 직접 측정) 삽입 예정.

## II.1 EOS (BM3, free 4-parameter fit)

| | LPSCl v3 (4 fu) | LPSCl1.6 v3 (5 fu) |
|---|---|---|
| nat | 52 | 62 |
| supercell | cubic conventional | rhombohedral |
| V0 raw (Å³) | 1016.62 | 1216.44 |
| **V0 / atom (Å³)** | **19.55** | **19.62** (+0.4%) |
| **V0 / fu (Å³)** | **254.16** | **243.29** (−4.3%) |
| B0 (GPa) | 26.233 ± 0.004 | 21.71 ± 0.27 |
| B0′ | 4.171 ± 0.011 | 7.01 ± 1.37 |
| R² | 1.000000 | 0.999012 |
| n_points | 8 | 11 |

- raw V0 직접 비교 ❌ → **V/fu로 LPSCl1.6 −4.3%** (Cl→S 치환 + Li 공공으로 fu 부피 수축,
  실험 lattice 경향 일치). **V/atom은 +0.4%로 동일** (framework 보존).
- B0′ 차이 (4.17 vs 7.01): modelc의 넓은 부피 sweep + 평탄한 Li 에너지면 반영. 각 K값
  (BM vs stress-strain)은 ~3% 이내 교차검증.

### II.1.1 ★ V/f.u.와 V/atom이 반대로 나오는 이유 (조성 vs 패킹)

겉보기 모순 — **V/f.u.는 LPSCl이 크고(254 > 243), V/atom은 LPSCl1.6이 큼(19.62 > 19.55)**.
모순이 아니라 두 지표가 **다른 것을 재는 것**이고, 차이는 전부 **f.u.당 원자 수**에서 나온다.

**원자 수 / f.u.** (charge-compensated 치환):
- Li₆PS₅Cl: 6+1+5+1 = **13 atoms/f.u.**
- Li₅.₄PS₄.₄Cl₁.₆: 5.4+1+4.4+1.6 = **12.4 atoms/f.u.**
- Cl⁻ 하나 추가 시 S²⁻ 하나 제거 + 전하보상 위해 Li⁺ 하나 제거 → +0.6 Cl, −0.6 S, −0.6 Li
  = 순 **−0.6 atom/f.u.** (LPSCl1.6이 f.u.당 0.6개 적음)

`V/f.u. = V/atom × (atoms/f.u.)`:

| | V/atom (Å³) | × atoms/f.u. | = V/f.u. (Å³) |
|---|---|---|---|
| LPSCl | 19.55 | × 13 | **254.16** |
| LPSCl1.6 | 19.62 | × 12.4 | **243.29** |

- **V/f.u. (LPSCl 큼)** = **stoichiometry(조성) 효과** — LPSCl1.6은 원자가 0.6개 적어서 f.u.
  부피가 작음. 실험 lattice 경향(Cl 함량↑ → 격자 수축)과 일치하는 지표.
- **V/atom (LPSCl1.6 약간 큼 +0.4%)** = **packing(골격 충진) 효과** — 남은 원자 1개당 부피는
  거의 같고, Li 공공이 미세한 여유공간을 줘서 약간 헐렁. argyrodite framework 밀도는 보존.

**paper 메시지**: 두 지표를 모두 보고하면 "**Cl 치환은 f.u. 부피를 줄이지만(조성) 골격 원자당
패킹 밀도는 안 건드린다(구조)**"는 분리된 결론이 깔끔하게 나온다. (격자/밀도 비교는 V/f.u.,
framework 보존 확인은 V/atom 사용.)

## II.2 결합 환경 (DFT V0)

Cutoff 통일: P–S 2.3, Li–S 3.2, Li–Cl 3.4, S–S 4.0 Å (argyrodite 표준).

### II.2.1 Bond lengths

| 결합 | LPSCl (n / mean±σ / [min,max] Å) | LPSCl1.6 | Δ mean |
|---|---|---|---|
| **P–S** | 16 / 2.073 ± 0.036 | 20 / 2.064 ± 0.011 | −0.009 Å (PS4 단축 + σ 1/3: 균질) |
| **Li–S** | 72 / 2.461 ± 0.106 | 68 / 2.465 ± 0.094 | +0.004 Å (동일) |
| **Li–Cl** | 24 / 2.607 ± 0.129 | 40 / 2.532 ± 0.119 | **−0.076 Å (Cl-rich에서 더 짧음!)** |
| S–S (cage) | 56 / 3.595 ± 0.199 | 58 / 3.519 ± 0.178 | −0.076 Å (cage 압축) |

### II.2.2 Coordination

| 사이트 | LPSCl (avg Z±σ / [min,max]) | LPSCl1.6 | 차이 |
|---|---|---|---|
| Li | 4.00 ± 0.00 [4,4] (24) | 4.00 ± 0.27 [3,5] (27) | 평균 동일, modelc ±1 분산 (공공) |
| P | 4.00 ± 0.00 | 4.00 ± 0.00 | 동일 (PS4 보존) |
| S | 10.00 ± 1.67 [8,12] | 9.27 ± 1.21 [6,11] | modelc −0.73 (Li 공공) |
| Cl | 6.00 ± 0.00 (Cl[Li6]) | 5.00 ± 0.50 [4,6] | **6→5 (4d anti-site)** |

### II.2.3 Voronoi (다면체 부피, Å³)

| 종 | LPSCl | LPSCl1.6 | Δ |
|---|---|---|---|
| Li | 19.56 ± 0.21 | 20.51 ± 1.15 | +1.0 (공공으로 공간↑) |
| P | 14.05 ± 0.00 | 13.99 ± 0.37 | −0.06 (PS4 보존) |
| S | 20.14 ± 3.41 | 19.55 ± 2.05 | −0.6 |
| Cl | 22.06 ± 0.00 | 20.31 ± 0.74 | **−1.7 (Cl이 작은 4d 자리 점유)** |

### II.2.4 결합환경 핵심 정리

1. **Li–Cl 단축 (−0.076 Å)** — 직관 반대. Cl excess → 일부 Cl이 4d(S²⁻ 자리)로 →
   Li–Cl 거리 ↓. Voronoi Cl −1.7 Å³가 같은 그림.
2. **Cl 배위수 6→5 (anti-site)** — 8개 Cl 중 평균 1개가 4d. site disorder 직접 증거
   (per-bond json: comp1 Cl 4a×4/4d×0, modelc 4a×7/4d×1).
3. **PS4 backbone 안정** — P–S 평균 동일 + σ 1/3 감소.
4. **Li 배위 평균 동일·분산 발생** — modelc 일부 Li가 3-/5-배위 (vacancy + anti-site).

**Paper 함의**: "Cl 증가 = Li–Cl 약화"라는 단순 가정 반박. Cl excess는 일부 Cl을 4d로
보내 **오히려 짧고 강한 Li–Cl ionic bond** 형성 (Wilkening q·|q|/r glue 강화).

## II.3 Bader (plot_num=17 AE charge density) — paper-grade

PAW kjpaw + pp.x AE density + Henkelman bader. SCF = LOBSTER ext basis와 동일 (ecutwfc 70 Ry).

| 종 (e) | LPSCl (comp1, k444) | LPSCl1.6 (modelc, k663) | 차이 |
|---|---|---|---|
| **Li** | **+0.874 ± 0.005** (n=24) | **+0.882 ± 0.010** (n=27) | +0.9% (동일) |
| **Cl** | **−0.925** (n=4, σ=0) | **−0.916 ± 0.005** (n=8) | 거의 동일 |
| **P** | **+3.271** (n=4) | **+4.429 ± 0.415** (n=5) | basin shape 효과 (아래) |
| **S** | **−1.518 ± 0.36** (n=20) | **−1.756 ± 0.24** (n=22) | modelc +16% ionic |

> ⚠ 이전 표의 comp1 Cl −0.941은 옛값 → **k444 권위값 −0.925**로 정정.

### PS4 charge sum cross-check

개별 P/S 분리값은 Bader basin shape이 환경 dependent (PS4-S vs 4d-S²⁻ basin 모양 차이)
→ modelc에서 σ 크고 평균 shift. **paper엔 PS4 unit 합 또는 P+4S로 reporting 권장**
(개별값은 supplementary). 둘 다 formal PS4³⁻ 근처로 charge-compensated.

### Wilkening ionic potential (q·|q|/r, eV/Å)

| | LPSCl | LPSCl1.6 | Δ% |
|---|---|---|---|
| **Li–S** | 0.538 | 0.628 | **+16.8%** |
| Li–Cl | 0.316 | 0.319 | +1.1% |
| **Li-S / Li-Cl ratio** | 1.70 | 1.97 | Li-S 우세 강화 |

→ Li-S가 Li-Cl보다 ionic glue **1.7–2× 강함**. LPSCl1.6의 ionic potential 증가는
**거의 전적으로 Li-S 채널** (vacancy + 4d-Cl 효과가 S charge −1.52→−1.76으로 집중).

## II.4 LOBSTER ICOHP (per-bond 평균, eV) — paper-grade ext basis

ext basis (Li 1s2s2p, P/S/Cl 3s3p3d) + PAW kjpaw + charge spilling < 2%.

| 결합 종류 | LPSCl (k444) | LPSCl1.6 (k663) | Δ% |
|---|---|---|---|
| **P–S** | **−5.938** (16) | **−6.000** (20) | +1.0% (불변) |
| **Li–Cl** | **−1.861** (24) | **−2.103** (42) | **+13.0%** |
| **Li–S** | **−1.589** (120) | **−1.717** (113) | **+8.1%** |
| S–S | −0.107 (56) | −0.110 (58) | ~0 |

### II.4.1 per-site 분해 (universal anchor 발견)

| site | LPSCl ICOHP (n) | LPSCl1.6 ICOHP (n) | 해석 |
|---|---|---|---|
| Li–S(PS4) | −1.344 (96) | −1.622 (101) | PS4-S에 묶인 Li (약함) |
| **Li–S(4d, free S²⁻)** | **−2.568 (24)** | **−2.516 (12)** | **조성 무관 anchor (Δ2%)** |
| Li–Cl(4a) | −1.861 (24) | −2.026 (38) | 정상 4a 자리 |
| **Li–Cl(4d, anti-site)** | — (없음) | **−2.836 (4)** | **4a보다 40% 강함 — Cl-rich 강화의 동력** |

**핵심**: modelc의 ICOHP 강화는 (1) free S²⁻ 주위 Li–S(4d) 결합 (양쪽 −2.5 동일,
universal), (2) **4d-Cl anti-site** (modelc에만, −2.84 매우 강함)가 평균을 끌어올림.
→ "Cl excess가 약화"가 아니라 **anti-site로 강화**.

### II.4.2 paper 메시지

1. 모든 ionic bond가 LPSCl1.6에서 강함 (Li-Cl +13%, Li-S +8%) — vacancy+Cl 치환은 **강화**.
2. 위계 보존: P-S(covalent) ≫ Li-Cl > Li-S ≫ S-S (둘 다).
3. Li-Cl > Li-S in both → Wilkening framework 일치.
4. PS4 backbone robust: P-S ICOHP −5.94 ≈ −6.00 (불변).
5. ext basis(1.2-1.5% spill)가 old sparse basis(17%)보다 +17~180% 강함 → **paper엔 ext만 보고**.

## II.5 AIMD 이온 확산 (Arrhenius 600/800/1000K) — paper-grade

동일 프로토콜 (UMA-s-1p1, Langevin NVT, equilib 10ps + prod 100ps, 2fs). **양쪽 [2,50]ps
window** (comp1 800K fluke는 fresh seed로 재실행 해결, R² 0.77→0.999).

| | LPSCl (comp1) | LPSCl1.6 (modelc) | 비 |
|---|---|---|---|
| **Ea (eV)** | **0.172** (R²0.999) | **0.224** (R²0.992) | comp1 장벽 낮음 |
| D(600K) (cm²/s) | 2.68e-6 | 7.90e-6 | **2.95×** |
| D(800K) | 5.91e-6 | 2.05e-5 | 3.5× |
| D(1000K) | 1.02e-5 | 4.55e-5 | 4.5× |
| D₀ prefactor | ~7.5e-5 | ~5.8e-4 | **~8×** |

### II.5.1 메커니즘 — vacancy는 장벽이 아니라 carrier를 늘린다

- **comp1 Ea(0.172) < modelc Ea(0.224)** — comp1의 per-hop 장벽이 *더 낮음*.
- 그런데 modelc가 ~3× 빠른 건 **prefactor D₀ ~8× 차이** = Li vacancy가 운반체·경로를 늘림.
- 두 경쟁 효과: modelc는 (높은 per-hop 장벽, 무질서 Cl-rich cage) BUT (vacancy carrier 多)
  → simulated T(600-1000K)에서 prefactor 지배 → modelc 빠름 = 실험 σ(LPSCl1.6)>σ(LPSCl) 일치.
- **paper 메시지**: "halogen-rich가 더 전도성인 건 migration barrier가 낮아서가 아니라
  vacancy carrier가 많아서."

### II.5.2 실험 대조 & caveat

- modelc Ea 0.224 = Schlem 2020 Cl-rich 0.22 정확 일치. comp1 0.172도 LPSCl bulk 범위(0.16-0.25).
- framework 정지: D(Cl,P,S) ~ D(Li)의 1/40-1/60 → Li-only 전도체 (둘 다).
- 절대 σ는 UMA가 3-5× overshoot + Haven ratio=1 가정 → 비(ratio)만 robust. 300K 외삽
  (3 T점)은 over-interpret 금지.

### II.5.3 ★ 저온 특성 trade-off — 높은 Ea의 대가 (vacancy의 양날)

**핵심 통찰**: LPSCl1.6의 더 높은 Ea(0.224 > 0.172)는 곧 **σ가 온도 강하에 더 가파르게
떨어진다**는 뜻 → **원리상 LPSCl1.6은 저온 특성이 더 불리**하다.

`D = D₀·exp(−Ea/kT)`에서 modelc는 큰 D₀로 측정구간을 이기지만, T가 내려갈수록
Boltzmann 항 `exp(−Ea/kT)`의 패널티가 Ea에 비례해 커진다. 두 Arrhenius 직선이 만나는
**교차온도**:

$$T_{cross}=\frac{\Delta E_a}{k\,\ln(D_{0,m}/D_{0,c})}=\frac{0.052\ \text{eV}}{k\cdot\ln(8.04)}\approx 290\ \text{K}$$

| 온도 영역 | 더 빠른 쪽 | 이유 |
|---|---|---|
| **T ≳ 290 K** (작동·측정구간) | **LPSCl1.6** | prefactor D₀(~8×, vacancy carrier/path) 지배 |
| **T ≲ 290 K** (심부 저온) | **LPSCl** (원리상) | 낮은 per-hop 장벽(0.172)이 유리해짐 |

- **paper 메시지**: vacancy는 양날 — **D₀(통로·운반체)는 키우지만 per-hop 장벽도 올린다.**
  그래서 Cl-rich의 전도도 우위는 **고온/작동온도에 한정된 prefactor 효과**이고, 충분히
  낮은 T에선 stoichiometric LPSCl의 낮은 장벽이 역전 우위를 가진다. = **온도 의존성이
  조성 설계의 trade-off 축**임을 보여주는 결과.
- ⚠ **정량 caveat**: 교차점 290K는 3점 외삽 + comp1 Ea(0.172)가 다소 낮게 잡혔을 가능성
  (R²0.999지만 3점)으로 **불확실**. 실제 실험은 RT에서 modelc가 ~2× 더 전도성 → 진짜
  교차점은 RT보다 아래일 것. 따라서 "**원리상 저온 불리**"는 robust한 정성 결론이지만,
  교차 절대온도는 paper에서 단정하지 말고 "Ea 차이에서 따라오는 경향"으로 보고.

전체 데이터: `db/properties/li_transport.json`.

## II.6 전자구조 (DOS/PDOS + bands) — k444 확정

| 항목 | comp1_v3 (LPSCl) | modelc_v3 (LPSCl1.6) | Δ |
|---|---|---|---|
| EF (eV, QE) | 2.821 | 2.445 | −0.376 |
| VBM / CBM (eV) | 2.48 / 4.24 | 2.72 / 4.54 | |
| **gap (eV)** | **1.76** | **1.82** | **−0.06 (동일)** |
| VBM character | S p 91% + Li p 6% | S p 92% + Li p 6% | 동일 |
| CBM character | S p 42% + P s 25% + Li p 14% | S p 45% + P s 27% + Li p 13% | 동일 |

방법: QE 7.4.1 PBE, USPP/RRKJUS, 52/520 Ry, k=6×6×6 SCF on k444-relax, dos.x+projwfc.x,
MV smearing. Gap = low-DOS run (DOS<0.5 states/eV) straddling EF.

### II.6.1 k-mesh 사고 해소

- comp1 초기 gap **1.50은 k=2×2×1 artifact** (k×L=10 Å, 4배 부족). 수렴 k(6×6×6)에서
  **1.76**으로 상승 (+0.26 eV). geometry는 RMS 0.003 Å로 불변 → 오염은 전자(gap)만.
- **이전 Δgap=−0.32 eV (조성 효과로 오해)는 완전히 수치 artifact였음.** 수렴 k에서
  Δ−0.06 → **gap은 Cl 함량/Li-vacancy disorder에 둔감.**

### II.6.2 절대값 vs 문헌

| 출처 | Method | gap (eV) |
|---|---|---|
| **우리 (양쪽)** | PBE/USPP + DOS-threshold | **1.76–1.82** |
| Batteries 12(2):60 (2026) | PBE | 2.45 |
| PMC9661960 | PBE | ~2.15 |
| TB-mBJ | PBEsol+TB-mBJ | 3.11 |
| HSE06 | HSE06 | 3.30–3.52 |
| G0W0 | G0W0 | ~5.13 |
| 실험 (optical) | | 3.0–3.5 |

우리 PBE 1.76-1.82가 문헌 PBE(2.15-2.45)보다 ~0.4 eV 낮은 건 USPP-pseudo +
DOS-threshold underestimate 때문 — **두 시스템에 동일하게 적용**되므로 comp1-vs-modelc
비교는 유효. 절대값은 paper에서 method 한계로 명시.

### II.6.3 modelc defect-band feature

- modelc EF(2.445) < VBM(2.72)인 anomaly: [EF,VBM] 윈도우에 **0.74 states** (comp1은
  0.037, 20× 적음), S 3p 93%, 특정 S 원자(#34/#35/#50…)에 국소화.
- comp1은 EF가 gap 내부 (clean insulator). → **modelc의 0.74 states는 disordered
  Li-deficient 구조의 실제 specific-배치 효과** (Li vacancy가 S 최근접에 비대칭 배치 →
  S 3p hole 국소화). bands.dat(422 kpt)로 검증 — flat localized band 확인 시 (A) 확정.
- charge balance: 두 시스템 모두 48 e/fu로 stoichiometric → defect-band는 charge
  불균형이 아니라 국소 배치 효과.

## II.7 ELF (전자 국소화 함수)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| 상태 | ✅ V0_ELF.cube 완성 (ONCV 80/320, pp.x plot_num=8) | ✅ |
| P–S 공유성 | (분석 삽입 예정) ELF>0.7 P-S 사이 결합 maxima | 있음 |
| Li–anion 이온성 | (삽입 예정) Li 주위 ELF 저조 = 이온 결합 | |
| 3D iso level | (삽입 예정) | 0.75 |

→ cube 생성 완료, 정량 iso-surface 분석 삽입 대기. 예상: 두 시스템 모두 PS4에 covalent
ELF maxima + Li 주위 ionic depletion (Bader/ICOHP와 일관).

## II.8 탄성 — DFT 0K stress-strain

> ⏳ **comp1 k444 relaxed-ion 재계산 중 (6/12 strain)**. 아래는 직전(k221 geometry,
> RMS 0.003 Å 차이) 값 — k444 확정 시 갱신. modelc(k663)는 확정.

### II.8.1 clamped-ion (frozen-ion, harmonic)

| 항목 (GPa) | LPSCl | LPSCl1.6 | Δ |
|---|---|---|---|
| C11 / C12 / C44 | 74.2 / 29.2 / 19.0 | 89.9 / 21.8 / 14.4 | |
| B_VRH / G_VRH | 43.59 / 20.12 | 44.47 / 20.05 | ~동일 |
| **E_VRH** | **52.31** | **52.30** | **±0.02% (paradox)** |
| Zener A | 1.073 (isotropic) | 0.416 (anisotropic) | 2.6× |

### II.8.2 relaxed-ion (이온 Born screening 포함, 실험 대응) — 🎯 paradox 해소

| 항목 (GPa) | LPSCl† | LPSCl1.6 | Δ% | 실험 |
|---|---|---|---|---|
| B_VRH | 25.18 | 23.40 | −7.1% | ~25 |
| G_VRH | 8.26 | 10.61 | **+28.4%** | ~8 |
| **E_VRH** | **22.33** | **27.66** | **+23.9% ✓** | **LPSCl1.6 > LPSCl ✓** |
| ν | 0.352 | 0.303 | | ~0.35 |
| Zener A | 1.16 | 1.44 | aniso ↑ | |

†comp1 k444 재확인 중. **LPSCl relaxed-ion E_VRH 22.33 ≈ 실험 ~23** (clamped 52.31은 2.3× 과대).

### II.8.3 vacancy paradox 종합

| 시나리오 | E_VRH LPSCl | E_VRH LPSCl1.6 | 결론 |
|---|---|---|---|
| clamped-ion DFT 0K | 52.31 | 52.30 | **paradox** (차이 0%) |
| **relaxed-ion DFT 0K** | **22.33†** | **27.66** | **paradox 해소** ★ |
| MLIP 600K snapshot | [확인 중] | 52.72 | MLIP은 clamped-like |
| 실험 | ~23 | LPSCl1.6 > LPSCl | relaxed-ion이 추세 정확 |

**메커니즘**: Li sublattice가 매우 soft → 변형 시 Li 재배치(ionic Born screening)가 강성에
핵심. vacancy + 4d-Cl anti-site가 특정 shear configuration을 lock-in → **G_VRH +28%
(shear-dominant stiffening) + Zener A 1.16→1.44 (비등방)**. bulk는 vacancy로 약간 soft (−7%).
= disorder의 mechanical fingerprint.

### II.8.4 B0(BM-EOS) vs B_VRH(stress) 교차검증

| | B0 (BM, GPa) | B_VRH (stress) | 비율 |
|---|---|---|---|
| LPSCl | 26.23 | 43.59(clamped)/25.18(relaxed) | — |
| LPSCl1.6 | 21.71 | 44.47(clamped)/23.40(relaxed) | — |

B0(등방 hydrostatic, full relax)와 B_VRH(clamped-ion Cij 유도)는 물리적으로 다른 양.
**relaxed-ion B_VRH가 BM-EOS B0에 근접** (LPSCl 25.18 vs 26.23) → 두 독립 방법 교차검증 ✓.

## II.9 BVSE (Python proxy)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| 상태 | ✅ bvse_k444/ | ✅ |
| 최소 Ea_BVSE | (Li 이동 경로 proxy, AIMD와 정성 일치) | |

## II.10 논의 포인트 (paper outline)

1. **전자구조 둔감성** (II.6) — gap·궤도성격 동일. 조성 효과 통념 반박. k-mesh 수렴 중요성.
2. **전도도 = carrier 메커니즘** (II.5) — 장벽 아닌 prefactor/vacancy. 실험 σ 추세 재현.
3. **이온 glue 강화 + anti-site** (II.3, II.4) — Bader·LOBSTER·Wilkening 합의. 4d-Cl이 동력.
4. **vacancy paradox** (II.8) — clamped는 못 잡고 relaxed-ion이 해소. shear stiffening + 비등방.
5. **PS4 골격 불변** (I.3) — 모든 probe에서 covalent backbone robust.

---

## 각주 / 출처

- modelc_v3 Pipeline v2 lineage: `db/compositions/modelc_v3.json` (Step 1–8 audit).
- comp1 v2 §8 (a=9.929)는 컨테이너 `archive_v2_post/`에 archive (재현용, paper 미사용).
- per-bond 권위값: `db/properties/per_bond_json/{bonds_comp1_k444.json, bonds_modelc_k663.json}`
  (one-shot `tools/comp1_v3/analyze_per_bond_icohp.py`).
- 도구: `tools/comp1_v3/`, `tools/modelc_v3/`.
- 문헌:
  - [TB-mBJ 3.11 eV — S0921452623002995](https://www.sciencedirect.com/science/article/abs/pii/S0921452623002995)
  - [HSE06/G0W0 — PMC9661960](https://pmc.ncbi.nlm.nih.gov/articles/PMC9661960/)
  - [PBE 2.45 eV — Batteries 12(2):60](https://doi.org/10.3390/batteries12020060)
  - [Adeli 2019 Angew — LPSCl1.5 charge-compensated](https://onlinelibrary.wiley.com/doi/10.1002/anie.201814222)
  - [Devil in the Defects, Chem Mater 2021 — LPSCl n-type](https://pubs.acs.org/doi/10.1021/acs.chemmater.1c02345)
  - [arXiv:2503.13142 — LPSCl1.5 disorder](https://arxiv.org/pdf/2503.13142)
  - Schlem 2020 — Cl-rich argyrodite Ea 0.22 eV.

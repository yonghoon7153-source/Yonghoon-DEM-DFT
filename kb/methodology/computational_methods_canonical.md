# 계산 방법 Canonical — 단일 기준 (2026-07-23 재정리)

> **왜 이 문서인가.** 물성마다 "무엇을 맞춰야 조성 간 비교가 성립하는가"(일관성 축)가 다르다.
> 이게 db에 안 적혀 있어서 PAW/USPP 혼동·셀타입 차이·MLIP-elastic 혼입 같은 사고가 반복됐다.
> **elastic·EOS·gap·ε∞ = DFT(QE)라 pseudo·ecut·k·셀에 민감** / **MD·phonon = UMA(MLIP)라 pseudo 무관, UMA버전·프로토콜만** / **ICOHP = LOBSTER라 all-PAW 필수.**
> 값을 인용하거나 새 계산을 걸기 전에 이 문서를 먼저 본다. (Explore 전수감사 2026-07-23 + 백업 입력 실측 종합.)

---

## 1. 물성별 일관성 축 (한눈에)

| 물성 | 코드 | 비교하려면 맞춰야 할 축 | pseudo 민감 |
|---|---|---|---|
| **Elastic (Cij→VRH)** | QE pw.x | pseudo · ecut · k-density · **셀타입** · strain · clamped/relaxed | **예** |
| **EOS B0** | QE + ASE BM3 | pseudo · ecut · k · 조성 | 예 (intensive라 셀크기는 OK) |
| **Band gap** | QE nscf (fixed-occ) | pseudo · ecut · k · 판독법(eigenvalue) | 예 |
| **ICOHP/ICOBI** | LOBSTER | **all-PAW 필수** · basis(ext) · nbnd | 예 (PAW 전용) |
| **MD (Ea, σ)** | UMA-s-1p1 (MLIP) | UMA버전 · MD프로토콜 · **멀티시드** | **아니오 (pseudo 없음)** |
| **Phonon (안정성)** | UMA (MLIP) | UMA버전 · 셀 | 아니오 |
| **ε∞ (유전텐서)** | QE ph.x epsil | pseudo · ecut · k · trans=.false. | 예 |

**황금률:** 조성 간 "절대값 표"를 만들 땐 위 축이 **전부** 같아야 한다. 하나라도 다르면 → "순위/방향 + 각주" 또는 재측정.

---

## 2. Elastic (DFT relaxed-ion stress-strain, 12 SCF = 6 Voigt × ±h) — 조성별 셋업 실측

⚠ **오늘의 대발견: elastic 셋업이 조성마다 제각각이다.** 아래는 백업 입력(`D:\v100, kisti 백업\runs\...`)에서 직접 확인한 값.

| 조성 | 방법 | strain | k-mesh | pseudo | ecut(wfc/rho) | 셀타입·원자수 | E/B/G_VRH (GPa) | 상태 |
|---|---|---|---|---|---|---|---|---|
| **comp1 (LPSCl)** | relaxed | 0.005 | **4 4 4** | **USPP** (li/s/cl v1.4.uspp + P rrkjus) | **52/520** | cubic-52 | **22.06 / 25.51 / 8.13** | ★ **기준 (paper-grade)**, 문헌 23 일치 |
| **comp2 (LPSClBr)** | relaxed | 0.005 | 4 4 4 | **USPP** (+Br v1.4.uspp) | 52/520 | cubic-52 | **재측정중** (`comp2_elastic_uspp`) | ★ **comp1과 유일한 완전비교쌍** (같은 cubic-52) |
| **modelc (LPSCl1.6)** | relaxed | 0.005 | **2 2 1** | USPP (동일 set) | **60/480** | **rhombo-62** | 27.66 / 23.40 / 10.61 | 셀·k·ecut 다름 → **각주비교만**; ⚠ **C66=4.85 shear산포 43%** |
| **lpsocl (+O)** | relaxed | 0.005 | 2 2 1 | USPP (동일 set) | 60/480 | rhombo-62 | 35.04 / 27.82 / 13.58 | **순위만** (단일 disorder config) |
| **comp3/4/5** | **v1 clamped (energy-curv)** | 0.005 | ? | ? | ? | rhombo-62 | (v1값, ordered-Li) | ⚠ **옛 방법 → 재측정 필요** |
| **b2o3** | relaxed | 0.005→0.01 | ? | (USPP 추정) | ? | **128-atom SC** | **K=27.02만**, G/E withheld | shear 붕괴(비물리) → bulk만 |

### 핵심 판정
- **comp1 ↔ comp2 = 유일한 "완전 통일" 비교쌍** (둘 다 cubic-52 · USPP · 52/520 · k444 · relaxed · 0.005). → LPSCl vs LPSClBr 슬라이드는 이 쌍으로.
- **modelc/lpsocl은 rhombo-62라 셀 자체가 comp1과 다름** → k·ecut를 맞춰도 통일 불가. **"순위/방향 + 각주"**로만 인용 (published comp1↔modelc 슬라이드도 이 각주 필요).
- **comp3/4/5는 아직 v1 clamped(ordered-Li, C44 과대)** → v3 relaxed-ion 재측정 대상.
- **PAW는 elastic에 안 씀.** comp2 champion 구조는 PAW(LOBSTER용)지만, **elastic만 USPP로 분리**(comp1도 elastic=USPP / LOBSTER=PAW로 분리했음).

### Clamped vs Relaxed (반드시 relaxed를 인용)
Clamped-ion(원자 고정)은 argyrodite 탄성을 ~2.3× 과대평가(comp1 clamped E=52.31 vs relaxed 22.06, 실험 ~23). **paper 값은 relaxed-ion만.**

---

## 3. EOS B0 (DFT BM3, ASE `birchmurnaghan`)

| 조성 | B0 (GPa) | 출처 | 비고 |
|---|---|---|---|
| comp1 | **26.23** | `eos.json` | PRIMARY |
| comp2 | 25.8 | `eos.json` | |
| modelc | **21.71** | `eos.json` (PRIMARY) | ⚠ `modelc.json` 의 19.59 "confirmed_final"은 **stale** |
| lpsocl | 24.71 | `lpsocl_eos_dft_result.json` | +O가 +3.0(+13.9%) 강화 |
| b2o3 | 24.48 | `b2o3_eos_dft_result.json` | |

> B0(hydrostatic)는 elastic B_VRH(harmonic)와 다른 양 — 둘 다 보고하되 혼동 금지 (comp1 B_VRH 25.51 vs B0_EOS 26.23).

---

## 4. Band gap (DFT fixed-occ nscf **eigenvalue** = canonical)

| 조성 | gap (eV) | 출처 |
|---|---|---|
| comp1 | **2.066** | `electronic.json` (eigenvalue) |
| comp2 | 2.04 | `electronic.json` |
| modelc | **2.099** | `electronic.json` |
| +B2O3 | 1.9671 | |
| lpsocl (+O) | 2.2309 | `lpsocl_dos_gap.json` |

> ⚠ **DOS-threshold 판독(comp1 1.76 / modelc 1.82) 및 `modelc.json:28` 의 1.65 는 폐기** (CLAUDE.md 규율: "DOS-threshold 판독 금지").

---

## 5. ICOHP / ICOBI (LOBSTER, **all-PAW**, **ext-basis**, nbnd500, spilling<5%)

- canonical: comp1 P-S ≈ **-6.0** / -5.94; comp2 P-S -5.913, Li-Cl -2.111, **Li-Br -1.934**(약함=이온성); lpsocl P-O **-8.413**(최강).
- ⚠ **`modelc_v3.json:107` 의 P-S = -5.12 (minimal-basis, spilling 17%) 는 stale** → ext-basis `bonds.json` 의 -6.0 이 정본. (b2o3도 동일 교훈: minimal-basis Li-X -0.8 은 artifact.)

---

## 6. MD 전도도 (UMA-s-1p1 task=omat, **pseudo 무관**)

**프로토콜 (고정):** Langevin NVT · dt 2 fs · friction 0.02 · equilib 5 ps + prod 200 ps · **MSD 창 2–50 ps** · Arrhenius **600/800/1000 K 3점** (400/500 K 제외) · **3-seed** · σ는 Nernst–Einstein(Haven=1).
**규율:** 절대값 인용 금지 · 비율도 멀티시드 판정만 · Ea 오차막대는 600 K 3-시드. **UMA는 Li₃N에 금지**(LPSCl 계열엔 검증된 표준).

| 조성 | Ea (eV) | 출처 |
|---|---|---|
| comp1 | **0.253** | `li_transport.json` (4fu, PRIMARY) |
| modelc | 0.224 | `li_transport.json` |
| lpsocl | 0.271±0.033 / 0.287±0.024 | `lpsocl_md_arrhenius.json` |
| comp2 | **계산중** (s2 단일 0.312, 3-seed 대기) | — |

> MD는 UMA라 pseudo(USPP/PAW)와 무관. comp1↔comp2 비교는 같은 UMA·프로토콜·멀티시드면 성립 (elastic처럼 재측정할 일 없음).

---

## 7. Phonon(UMA Γ) · ε∞(ph.x epsil)

- **Phonon:** UMA Γ-point, 안정성 판정 (comp2_v3 champion STABLE, lowest +32.7 cm⁻¹). MLIP라 pseudo 무관.
- **ε∞:** QE ph.x `epsil=.true. trans=.false.` (E-field DFPT, PAW). 52원자라 무거움(setup+iter). 슬라이드 5항목에 **미포함(곁가지)**. 진행: ibb 112952 (timeout 120h/5일). representation 156 나열은 trans=.false.여도 **정상**(오염 아님).

---

## 8. 정리 액션 목록 (이번 재구축에서 실행)

- [ ] **MLIP-elastic 11블록 삭제** — `elastic.json` 의 mlip_300K/600K 5섹션 + `comp1~5.json`·`modelc.json` 의 `elastic_mlip_*` + `_index.json` data_points. (MD/전도도/phonon/EOS의 MLIP은 **삭제 금지**.) 다운스트림 동기화: `adhesion.json` mlip 상관블록, `kb/methodology/elastic_constants.md`.
- [ ] **elastic.json 에 pseudo·ecut·k 메타 소급 기재** (표2 값) — 재발 방지의 핵심.
- [ ] **comp2 비정상 v2 elastic 격리** (`comp2.json` C44=77.6, E=120.2 `ANOMALOUS_DO_NOT_USE` 헤더 강화).
- [ ] **modelc ICOHP -5.12 stale 처리** (`modelc_v3.json:107` → "superseded by ext-basis -6.0").
- [ ] **modelc EOS 19.59 vs 21.71 통일** (`modelc.json` 의 19.59 "confirmed_final" → legacy 표기).
- [ ] **band gap canonical만** (DOS-thr·1.65 폐기 명기).
- [ ] **comp3/4/5 elastic 강등** ("v1 clamped ordered-Li, C44 과대, v3 재측정 필요").
- [ ] **doping_cascade UMA-elastic**(E_VRH/E_young) 삭제 여부 결정 (EOS_B0/형성E는 존치).

## 9. Pseudo 규율 (앞으로 새 DFT 계산 시)

- **elastic/EOS/gap/ε∞ (DFT):** **USPP** — li/s/cl/br `v1.4.uspp.F` + P `pbe-n-rrkjus_psl.1.0.0`. ecut는 계열별: **comp1/comp2 계열 = 52/520**, modelc/lpsocl 계열 = 60/480 (기존값 유지; 새 비교쌍은 comp1 기준 52/520).
- **comp2 champion 구조는 PAW**(kjpaw, LOBSTER용) — elastic은 **반드시 USPP로 분리**해서 comp1과 맞춘다.
- **ICOHP:** all-PAW 필수 (kjpaw).
- **MD/phonon:** UMA (pseudo 개념 없음).
- **★새 비교표를 만들기 전 체크리스트:** pseudo 같나? ecut 같나? k-density 같나? 셀타입 같나? clamped/relaxed 같나? — 하나라도 다르면 순위/각주 또는 재측정.

---

*갱신 이력: 2026-07-23 최초 작성 (Explore 전수감사 + 백업 입력 실측). db 정리 진행에 따라 §8 체크박스 갱신.*

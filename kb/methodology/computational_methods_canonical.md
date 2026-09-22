# 계산 방법 Canonical — 단일 기준 (2026-07-23 재정리 · **2026-08-20 축 4개 추가** · **2026-09-09 인용지위 정정**)

> ⛔ **이 문서가 정하는 것은 "무엇을 맞춰야 비교가 성립하는가"(일관성 축)뿐이다.**
> **그 값을 인용해도 되는가는 여기서 판정하지 않는다** — 순서대로 본다:
> ① `db/properties/canonical_registry.json` (값·status·comparison_group·prohibitions)
> → ② `db/properties/citation_hazards.json` (BLOCKED / HOLD / CONDITIONAL / SUPERSEDED)
> → ③ `db/governance/decisions.json` (판정, `decision_state: active` 만 유효).
> 2026-09-09 감사에서 이 문서의 ✅ 표기 몇 개가 **이력인데 현재 허가처럼** 읽히고 있었다
> (§6 MD Ea 표 · §6-2 의 "구간 0.2241" · §10). 아래에 그 정정이 들어 있다.

> 🆕 **2026-08-20 갱신 요약** — 값은 안 건드렸다(값의 정본은 각 db 파일). **일관성 축만** 늘렸다:
> ① **NEB 장벽** 축 신설(§1 표 + §6b) — 일주일째 생산하면서 이 문서에 없었다.
> ② **MD 에 "상자 크기" 축 추가**(§6-1) — 같은 계에서 상자만 키워도 **D 가 1.65배** 움직인다.
> ③ **골격(비-Li) MSD 게이트** 신설(§6-2) — β 게이트가 원리적으로 못 보던 구멍. **b2o3 는 판정 보류.**
> ④ **UMA 검증 앵커 기록**(§6-3) — 힘 MAE 30.0 meV/Å · 보존적. "황화물 PES 연화" 알리바이 철회.

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
| **MD (Ea, σ)** | UMA-s-1p1 (MLIP) | UMA버전 · MD프로토콜 · **멀티시드** · 🆕**상자 크기** · 🆕**골격 게이트** | **아니오 (pseudo 없음)** |
| 🆕 **NEB 장벽 (DFT)** | QE neb.x | pseudo · ecut · k · **셀 크기(수직폭)** · **전하 규약** · CI 순서 · **끝점이 진짜 최소인가** | 예 |
| 🆕 **NEB 장벽 (MLIP)** | UMA + ASE NEB | UMA버전 · **셀 크기** · 끝점 이완 깊이 · 경로(홉) 동일성 | 아니오 |
| **Phonon (안정성)** | UMA (MLIP) | UMA버전 · 셀 | 아니오 |
| **ε∞ (유전텐서)** | QE ph.x epsil | pseudo · ecut · k · trans=.false. | 예 |
| **표면에너지 γ / W_ad** | UMA 슬랩 | UMA버전 · **vacuum 30 Å 고정** · 슬랩 두께·종단면 | 아니오 |
| ~~**파괴인성 K_IC**~~ | ⛔ **없음** | — | **원자 스케일 산출물이 아니다** → §2 말미 |

**황금률:** 조성 간 "절대값 표"를 만들 땐 위 축이 **전부** 같아야 한다. 하나라도 다르면 → "순위/방향 + 각주" 또는 재측정.

> 🚧 **경계선도 이 문서의 일부다.** 무엇을 못 내는지 안 적어 두면 "안 했다"와 "못 한다"가 섞인다.
> 현재 명시적 경계 3개 — **K_IC**(시편 미세구조량), **μm 급 입자 역학**(DEM/연속체 몫),
> **공간전하층 정량**(두께·전위·Debye 길이 — 문헌도 정성뿐이라 "계산했다"고 말할 수 없다). 상세는 §2 말미.

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

#### 외부 앵커 (2026-08-05 추가) — 이 판정을 지지하는 문헌 소환값

| 앵커 | E | G | 출처 |
|---|---|---|---|
| **thiophosphate glass (실측)** | **≈ 20** | **≈ 7** | 나노인덴테이션 — [Famprikis19] *Nat. Mater.* 18, 1278 이 소환한 ref 108 (McGrogan) |
| 우리 **comp1 relaxed** | 22.06 | 8.13 | `elastic.json` — **+10 % / +16 %** |
| 우리 **comp1 clamped** | 52.31 | 20.12 | 같은 파일 — **2.4× / 2.9×** ❌ |
| (계열 대비) garnet | ≈ 150 | ≈ 60 | [Famprikis19] — 황화물이 한 자릿수 무르다 |
| (계열 대비) LiBH₄ | — | ≈ 4 | [Famprikis19] |

⚠ **인용 수위** — 실측 대상이 **thiophosphate 유리**이고 우리는 **결정 아지로다이트**다.
*"실험이 우리 값을 검증했다"* 는 **금지**. 쓸 수 있는 문장은 **"같은 자리에 있고, clamped 는 배제된다"** 까지.
(이 앵커는 `db/properties/external_benchmarks_symposium_2026.json` → `peer_reviewed_anchors` 에도 등록.)

### 파괴(K_IC) · 표면에너지(γ) — **우리 축이 아닌 것을 명시한다**

새로 계산을 걸기 전에 이 경계를 먼저 본다. 리뷰 원고 검토에서 이 축이 정면으로 걸렸다
(`kb/reviews/ECERD2600097_review_notes.md` A40·A53·A61).

| 양 | 우리 상태 | 등급 | 규율 |
|---|---|---|---|
| **탄성 Cij / E / G / B** | ✅ 있음 (relaxed-ion, k×L=40) | ★ paper-grade — 레지스트리 `E_VRH_GPa` **canonical 4건** | 위 §2 그대로. ⚠ 비교묶음은 **comp1↔comp2 만** 한 그룹이고 modelc·lpsocl 은 standalone 이다(`comparison_group` 이 그렇게 나뉘어 있다) |
| **표면에너지 γ / W_ad** | ✅ 계산은 있음 — `adhesion.json` `surface_energies` | ⚠ **UMA 슬랩 · 정본 등록 없음** | 같은 파일에 vacuum 아티팩트 이력(`vacuum_sensitivity`, 60 Å 에서 10× 폭주). **vacuum 30 Å 고정**. ⛔ **`canonical_registry.json` 에도 `citation_hazards.json` 에도 항목이 없다** — 즉 이 축은 결속 밖이다. W_ad 는 **어느 세대(20시드 전체 평균 vs 논문 5시드)를 정본으로 할지가 1저자 미결**이고, 100시드 통계는 Li5.4 내부 순위를 유의하지 않다고 한다(`kb/results/adhesion_100seeds_analysis.md`) |
| **Griffith 이상취성 하한** K_IC = √(E·2γ) | 🟡 조립 가능 (open_items #14) | ⚠ γ 가 UMA · 이상취성 | **"K_IC 를 계산했다" 라고 부르지 않는다.** "이상취성 하한을 냈다" 까지 |
| **실제 파괴인성 K_IC** | ⛔ **없다 — 그리고 낼 수 없다** | — | 아래 참조 |

> ⛔ **K_IC 는 원자 스케일 계산의 산출물이 아니다.** [Famprikis19] 가 못박기를,
> *"탄성계수와 달리 **파괴인성은 치밀도·입경·불순물·기존 균열·기공률에 강하게 의존하며 실험으로
> 결정해야 한다**. DFT 는 탄성계수는 줄 수 있다(ref 110 = Deng 2016)."*
> → 우리 K_IC 공백은 **누락이 아니라 방법론적 경계**다. 올바른 처방은
> **K_IC 를 DEM/CZM 의 sweep 파라미터로 받는 것**이지 계산해서 하나로 고정하는 것이 아니다.
> ⚠ 따라서 문헌 K_IC 값(0.2–0.4 MPa·m^½ 급)과 우리 Griffith 하한의 **근접성을 검증 논거로 쓰지 않는다** —
> **둘은 같은 양이 아니다**(전자는 특정 시편의 미세구조량, 후자는 이상취성 단결정 하한).

> ⛔ **Monroe–Newman(전단탄성률) 기준을 설계 원칙으로 쓰지 않는다.**
> 무기 SE 에는 적용되지 않는다 — 이론(Ahmad & Viswanathan, *PRL* 2017) + 실험(E ≈ 20 GPa 유리부터
> 150 GPa 가넷까지 **전 구간에서 Li 이 성장**), [Famprikis19] 판정.
> *"단단하게 만들면 덴드라이트가 막힌다"* 는 우리 결론에 넣지 않는다.

> ⚠ **μm 급 입자 역학은 우리 셀(nm)로 못 다룬다.** 우리가 대는 것은 **재료 상수**(E·G·B·γ·ΔV)이고,
> 입자·접촉·기공 스케일은 **DEM/연속체 몫**이다. 이 경계를 흐리지 않는다.

### 공간전하층(SCL) 정량 — **문헌 원전조차 정량한 적이 없다** (2026-09-22 실측으로 승격)

⚠ 이 절은 **§1 의 경계선 세 개 중 하나가 가리키던 빈 자리**였다. 44행이 *"상세는 §2 말미"* 라고
가리켰는데 여기에 해당 절이 없었다 — 가리키는 곳이 비어 있으면 다음 사람은 경계가 **약하다**고 읽는다.

| 양 | 우리 상태 | 문헌(원전) 상태 |
|---|---|---|
| SCL **두께** (nm) | ⛔ 없음 | ⛔ **원전에도 없음** |
| SCL **전위 프로파일** (V vs z) | ⛔ 없음 | ⛔ **원전에도 없음** |
| 층별 **전하 적분** | ⛔ 없음 | ⛔ **원전에도 없음** |
| **Debye 길이** | ⛔ 없음 | ⛔ **원전에도 없음** |
| 계면 **Li 공공 형성에너지** (자리별) | 🟡 미계산 | ✅ 있음 — Haruyama 2014 `Table 1` 21 자리 |

> ⛔ **"공간전하층을 계산했다" 고 쓰지 않는다.** 근거는 추측이 아니라 원전 실독이다 —
> 황화물 SE|산화물 양극 SCL 의 원전인 **Haruyama 2014**(*Chem. Mater.* **26**, 4248)를
> 본문 8 pp + SI 10 pp 전문으로 읽었고, 위 네 양이 **한 번도 나오지 않는다**.
> 그 논문의 `Fig. 5`(SCL 모식도)는 **세로축 라벨·눈금·단위가 전부 없는 개념도**다(크롭 실독).
> 저자들 자신이 못박는다 — *"long-range variation of the concentration needs to be analyzed
> by methods involving the long-range electrostatic interaction."*
> ⇒ SCL 은 **현상(phenomenon)의 원전**이지 **정량(quantification)의 원전이 아니다.**
> 인용할 때 쓸 수 있는 것은 *"그런 기전이 제안됐다"* 까지이고,
> *"SCL 두께가 ~nm 로 알려져 있다"* 류는 **원전에 근거가 없다**.

> ✅ **대신 쓸 수 있는 정량이 하나 있다 — 자리별 Li 공공 형성에너지의 *편차*.**
> Haruyama 2014 `Table 1` 을 우리가 재집계하면 LPS 쪽 6 자리의 자리 간 편차가
> **LCO|LPS 1.83 eV → LNO|LPS 0.76 eV (58 % ↓)** 다(digest §3f). 저자가 산문으로만 말한
> *"전압 프로파일 기울기 억제"* 의 수치판이고, **코팅 캠페인이 열리면 목표함수는
> 자리 에너지의 *평균*이 아니라 *편차*** 라는 뜻이다. 단 이건 **우리가 한 재집계**이지
> 논문이 보고한 값이 아니다 — 인용할 때 그렇게 밝힌다.
> 상세: `litdb/papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md`

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

### 3-1. 🆕 왜 **고정셀 + EOS** 인가 — vc-relax 를 쓰지 않는 진짜 이유 (2026-09-13 정리)

이 캠페인은 **vc-relax 를 쓰지 않는다.** 부피는 등방 스케일 + BM3 E(V) 적합으로 잡고,
그 V₀ 에서 **이온만** `calculation='relax'` 한다. 규약은 네 곳에 이미 박혀 있다:

| 출처 | 문구 |
|---|---|
| `kb/projects/cascade_v23_review_2026_07_11.md:28` | *"파이프라인 v2 원칙: **vc-relax 없음.** … (승격 시) KISTI **고정셀** volume grid"* |
| `db/compositions/modelc_nd_doped.json:80` | *"**vc-relax NOT used (distorts argyrodite)**"* |
| `kb/results/b2o3_champion_coordination_2026_06_29.md:13` | *"V₀ 로 셀 등방 스케일 + 이온만 relax … **argyrodite 입방 골격 보존**"* |
| `db/structures/lpsocl_candidates/README.md:24` | *"**NO vc-relax, DFT = fixed-cell only**"* |

**⚠ 그런데 "cubic 구조를 보존하려고" 는 이유의 절반이다.** 더 정확한 이유는 이것이다 —

> **우리 셀은 애초에 cubic 이 아니다.** 진짜 Li₆PS₅Cl 이 cubic 인 것은 Li 가 48h/24g 를
> **동적으로** 돌아다녀 **시간평균**이 cubic 이기 때문이다. 0 K 정적 계산에 Li 배치 하나를
> 얼려 넣으면 그 구성이 cubic 일 이유가 없다. vc-relax 를 걸면 **그 스냅숏의 최소점**으로 가고,
> 그러면 셀 뒤틀림은 *"어떤 배치를 골랐나"* 의 인공물이 된다.

⇒ 셀 고정은 **구조가 가진 대칭의 보존**이 아니라, **정적 계산이 알 수 없는 평균 대칭을
사람이 넣어 주는 것**이다.

> ⚠ **적용 범위 (2026-09-13, 회신 BP 지적 → 실물 확인).** 이 고정셀 정책은 **DFT 경로에만** 걸려 있다.
> 같은 README 의 바로 다음 줄이 *"Stage 2a: **UMA full relax** of the 4 candidates"* 이고,
> UMA 기본 경로(`run_uma_screening.py:56` · `run_mlip_postproc.py:293`)는 **형상 무제한
> `CellFilter(atoms)`** 를 쓴다. **두 방법의 셀 정책이 다르다** — `db/properties/cell_policy_gap_2026_09_13.json` GAP-1·2. 그리고 이 서술은 우리 원장이 이미 받치고 있다 —
`db/properties/elastic.json` 의 `_Zener_A_convention` 이 *"The cell is not perfectly cubic,
so the three symmetry-equivalent estimates differ"* 라 적고, comp1 relaxed 의 대칭동등
삼중항이 **1.144 / 0.751 / 0.918** 로 갈린다(산포가 인용하려던 문헌 간극 0.17 보다 크다).

**EOS 경로는 타협이 아니라 정공법이다.** 등방 스케일 + E(V) BM 적합은 *cubic 을 강제한 채
셀을 최적화하는 것*과 같은 일인데, 유한 기저에서 응력을 직접 최소화할 때 생기는
**Pulay stress** 를 피해 간다 (ecutwfc 60 USPP 에서 vc-relax 로 부피를 찾으면 그 함정에 걸린다).

#### 대가 — **잔류 편차응력**. 없앨 수 없고, 그러니 적는다

고정셀의 대가는 **편차(deviatoric) 응력이 남는 것**이다. 등방 성분은 EOS 가 0 으로 맞추지만
전단은 남는다 — 없애려면 cubic 을 깨야 하기 때문이다.

**실측 (comp1_V0_k444, 2026-09-13):** 평균압 **−0.002 GPa**(등방은 0) 인데
편차성분 **±1.3 GPa**, **yz 전단 1.08 GPa**.
출처 `db/properties/static_pair_dft_2026_09_13.json` `응력_GPa` — ⚠ 이 기록은 아직
**`status: proposed`**(1저자 비준 전)다. 값은 실측이고 산술은 확인됐으나 **정본이 아니다.**
comp1 relaxed-ion **C₄₄ = 18.98 GPa**(`elastic.json`) 로 나누면 **전단변형 ~5.7 % 어치**다 — 작지 않다.

⛔ 이것은 **고칠 결함이 아니라 명시할 사실**이다.

**⚠ 그런데 "모든 구조가 같은 편차응력을 공유한다" 고 쓰면 과하다** (회신 BP 정정).
형상 고정은 편차응력을 **허용**할 뿐, 모든 구조에 **같은 크기나 비영 값을 강제하지 않는다.**
위 ±1.3 GPa · yz 1.08 GPa 는 **comp1_V0_k444 의 값**이지 이 파이프라인의 상수가 아니다.

**"0 GPa" 를 쓸 때의 정확한 표현** (회신 BP 가 준 문구를 그대로 쓴다):

> *"셀 각도와 길이비를 고정하고 등방 E(V) 경로에서 부피를 최적화한다. **목표** 평균압은 0 GPa 이며,
> **실제 잔류 평균압과 편차응력을 별도로 보고한다.**"*

⛔ 이것은 *"전체 응력 0"* · *"자유 영응력 평형"* 과 **다른 조건**이다. BM 적합의 최소라고
실제 출력 압력까지 정확히 0 이 되지도 않는다.

> 곁가지 관측: 같은 기하에서 **UMA 가 그 편차응력을 0.193 GPa 안에서 재현**한다
> (전단 1.057 vs 1.080 GPa). 회신 BP 가 **조건부로 허용한 해석**은 여기까지다 —
> *"구성 a 의 고정 기하에서 UMA 가 DFT 의 비등방 응력텐서를 비교적 가깝게 재현한다."*
> ⛔ **그 이상은 안 된다**: 응력은 변형에 대한 에너지의 **1차 미분**이고 탄성률은 그 **변화율**이라,
> 한 점의 응력 일치가 탄성률·치환 효과를 보증하지 않는다. **힘 경보 초과를 상쇄하는 증거도 아니다.**
> (응력 부호 규약은 리뷰어가 확인했다 — `static_b_geom_gabia.sh:24` 가 ASE 응력에 음수를 곱해
> QE 규약으로 맞춰 두었으므로 이 비교는 유효하다.)

#### ★ 이 대가가 실제로 무는 자리 — **탄성 Cij**

편차응력을 진 기준상태에서 stress–strain 으로 Cij 를 뽑으면 그것은 **표준 Cij 가 아니다.**
응력을 진 기준계에는 보정항(Wallace 류)이 붙는데 관행적으로 무시된다. 1 GPa 는 무시하기에
애매한 크기다.

그리고 이것이 **b2o3 전단 실패와 겹친다.** `elastic.json` 은 원인을 이렇게 적었다 —
*"SHEAR BROKEN: ±shear relaxed into **DIFFERENT local minima** of the disordered 128-atom cell
→ C66 collapsed (5.15), eigenvalue **−2.87**, E_VRH −107.7 = unphysical, **WITHHELD**"*.

> ⛔ **그 `−2.87`·`5.15`·`−107.7` 은 인용 불가다** — 원장이 스스로 `WITHHELD` 로 표시한 값이고,
> 여기서는 *"탄성 계산이 깨졌다"* 는 **사실의 근거로만** 쓴다. b2o3 의 탄성 물성값으로
> 옮겨 적으면 안 된다. 조성 간 탄성 비교에는 `citation_hazards.json` 의
> **`HZ-elastic-cross-composition` (CONDITIONAL)** 도 함께 걸린다.

기준상태가 이미 전단응력을 지고 있으면
±변형이 서로 다른 골로 굴러가기 **더 쉬워진다.** 둘은 경쟁 가설이 아니라 **겹치는 메커니즘**이다.

⇒ **gabia `el`(modelc_2x) 이 "셀이냐 조성이냐" 를 가릴 때 세 번째 갈래를 같이 본다:
"기준상태 편차응력이냐".** 재는 값은 **`V0_relax.out` 의 응력 블록 한 줄**이고 —
이미 돌아간 계산이라 **추가 계산이 0** 이다. 12점 fit 때 같이 회수한다.


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
**규율:** 절대값 인용 금지 · 비율도 멀티시드 판정만 · Ea 오차막대는 600 K 3-시드 **(⛔ 결정계 box331 한정 — 회신 BS 2026-09-22. 비정질/유리는 카드가 온도·시드를 따로 선언한다: 소셀 유리 400/465/550 K · 구조 시드 5 의 IQR · 600 K 감김 배제)**. **UMA는 Li₃N에 금지**(LPSCl 계열엔 검증된 표준).

> ⛔⛔ **이 표는 "값 목록" 이지 "인용 가능 목록" 이 아니다 (2026-09-09 정정).**
> 레지스트리 기준 이 축의 `MD_Ea` 항목은 **철회 1 · 잠정 5 · canonical 2(인용 보류)** 이고,
> `kb/methodology/md_axis_status_2026_09_07.md` §0 이 못박는다 —
> **"지금 이 축에서 원고에 넣을 수 있는 활성화에너지는 0개다."**
> 그리고 레지스트리가 이 축 전반에 **`cross_composition_ranking` 을 금지**한다
> (계간 직접 비교는 `HZ-cross-system-Ea` BLOCKED · 회신 AK Q2=C).
> ⇒ 아래 표는 **어느 파일이 정본인가** 를 찾는 색인으로만 쓴다.

| 조성 | Ea (eV) | 레지스트리 status | 출처 |
|---|---|---|---|
| comp1 | 0.2532 (단일시드) | 🟡 `provisional` — `cross_composition_ranking`·`absolute_sigma` 금지 · `cite_until_beta_gate_passes` | `li_transport.json` (4fu) |
| modelc | 0.197 (3시드) / 0.2235 (단일시드 앵커) | 🟢 `canonical` **이나 계간 비교는 금지** — `absolute_sigma`·`single_seed_ratio` 금지 | `li_transport.json` |
| lpsocl | 0.2867 (62원자 4시드) | 🟡 `provisional` — 62원자 **셀 조건부** 값. 3×3×1 은 **다른 보고량**(회신 AK) | `lpsocl_md_arrhenius.json` |
| comp2 | 0.2755 (ordered 3시드) / 0.1512 (disorder d0.50) | 🟡 `provisional` — `cross_composition_ranking` 금지 · disorder 쪽은 config 산포 45 % (종전 "계산중" 은 낡았다) | `comp2_md_arrhenius.json` · `comp2_disorder_ensemble.json` |
| b2o3 | ~~0.199 ± 0.034~~ | ⛔ **retracted · 축 전체 마감** (`D-2026-09-07-b2o3-md-closure-retrospective`) — 인용 가능한 수 **0개** | `b2o3_md_arrhenius.json` |

> ~~MD는 UMA라 pseudo(USPP/PAW)와 무관. comp1↔comp2 비교는 같은 UMA·프로토콜·멀티시드면 성립 (elastic처럼 재측정할 일 없음).~~
> ⛔ **뒷문장 폐기 (2026-09-09)** — "같은 UMA·프로토콜·멀티시드면 성립" 은 **필요조건을 충분조건으로**
> 쓴 것이다. 최소한 **상자 크기**(§6-1, D 1.65배)와 **골격 게이트**(§6-2)가 더 필요하고, 그 둘을
> 맞춰도 레지스트리의 `cross_composition_ranking` 금지가 먼저다. 앞문장(pseudo 무관)만 유효하다.
> **이 문서는 축과 금지만 말한다 — 인용 가능 여부의 정본은 `db/properties/canonical_registry.json`
> · `db/properties/citation_hazards.json` 이다.**

### 6-1. 🆕 상자 크기도 일관성 축이다 (2026-08-20 추가)

`kb/results/lpsocl_box_size_600K_2026_08_18.md` — LPSOCl 600 K 를 3×3×1(558원자·3시드)로 키웠더니:

| | 기존 셀 | 3×3×1 | 비 |
|---|---|---|---|
| MSD@50ps | 25.3 Å² | **41.7 Å²** | **1.65×** |

**기울기(D)가 1.64 ± 0.14 배 움직인다.**
⚠ 초판의 *"곡선 모양(β)은 안 변한다"* 는 **STO 잣대 서술이고 원 카드 §2b 가 철회했다** —
정본 잣대(MTO)로는 β 가 +0.05 움직인다(0.76 → 0.81). "안 변한다" 고 쓰지 않는다.
⚠ **이 1.65배를 modelc·b2o3 에 이식하지 않는다** — 원 카드가 명시한다(유한크기 인자 f 는
그 계의 D 에 걸린다). LPSOCl **600 K 한 점**에서 잰 값이다.
⇒ **D·σ 절대값은 상자 크기에 묶여 있다.** 위 §6 표의 조성 간 Ea 비교가 성립하려면
**같은 상자**여야 한다 — "같은 UMA·프로토콜·멀티시드" 만으로는 부족하다(위 문장을 이 절이 좁힌다).

⚠ **셀 확대 처방에 붙는 단서**: `mlip_engine_probe` 실측(2026-08-20)으로
52 → 416원자가 **통계 2.7배를 비용 0.6배**에 준다는 것이 나왔지만(`uma_force_accuracy…` §5-3),
위 1.65배 때문에 **승격하면 전 조성을 다시 돌려야 한다.** 섞어 쓰면 안 된다.
또 1런 = 시드 1개라 멀티시드 규율과 충돌 ⇒ 처방은 **2–3시드 × 416원자**.

### 6-2. 🆕 골격(비-Li) MSD 게이트 — β 게이트가 못 보던 구멍 (2026-08-20 신설)

**왜.** 기존 β 게이트는 **Li MSD 만** 본다. 골격이 같이 움직이는 궤적은 Li β 가 정확히 1.0 이라
**게이트를 그냥 통과한다.** Zhang npj 2026 이 MACE-MP-0 의 LGPS 골격이 1050–1500 K 에서
인위적으로 녹는 것을 잡고 샘플링을 1050 K 로 낮췄는데, **우리 아레니우스 상한 1000 K 가 그 바로 아래**다.

**검사.** `python3 tools/ionic/msd_diffusive_check.py --framework --from_traj --glob '<…>/msd.json'`
판정량은 **비-Li 원소 MSD 의 로그기울기 β**(진동이면 평평해 β≈0, 자리를 뜨면 β→1).
⚠ **원소 8개 미만은 판정에서 뺀다** — 2–3개짜리 평균은 한 원자가 한 번 뛰면 β 가 1 을 넘는다.

**현재 판정 (2026-08-20)**

| 계 | 결과 |
|---|---|
| **modelc** 5온도 | β 0.01–0.13 — ⭕ 전부 정상 |
| **LPSOCl** 10런 | β −0.02–0.29 — ⭕ 전부 정상 |
| **b2o3** | 800 K **0.59** · 1000 K **0.63** (modelc 는 같은 온도에서 0.03/0.08) — 🔴 **판정 보류** |

🔴 **b2o3 는 결론이 아니라 보류다.** 자기리뷰에서 **이름과 기전을 둘 다 철회**했다:
"골격" 이라 부른 것 중 Cl·자유 S 는 **케이지 음이온**이고(우리 `cage_assign` 규약 그대로),
"D 과대·Ea 과소" 기전도 틀렸다(Li MSD 는 Li 자신의 변위다 — 진짜 위협은 **상태 혼합**,
즉 600 K 와 800/1000 K 가 **다른 음이온 질서 상태**를 표본하는 것).
⇒ `Ea 0.199±0.034` 는 **codex 교차검증까지 인용 보류.**

> ⛔⛔ **2026-08-23 갱신 — 보류가 아니라 철회다. 사유도 다르다.**
> 위 절의 보류 사유(골격 게이트 β)는 **더 이상 이 값의 문제가 아니다.** 3시드 × 3온도
> 재측정에서 **아레니우스가 800 K 위에서 굽는 것**이 확인됐다 —
> 구간 Ea **600→800 = 0.222 eV / 800→1000 = 0.077 eV**, 145 meV 차.
> 세 시드 모두 같은 경향이고(1000/800 비 1.09·1.22·1.45), 인공물 가설 셋을 각각
> 실측으로 반증했다(β 게이트 6/6 통과 · MSD 창 스캔에서 m 이 오히려 +4 % ·
> 1000 K 궤적 P 배위수 8/8 CN=4, 해리 0).
> **⇒ 600–1000 K 를 하나의 Ea 로 기술하지 않는다.** `0.199` · `0.206` · `0.1732` 전부 철회.
> ~~✅ 쓸 수 있는 것: **저온 구간 0.2241 ± 0.0606 eV** (600→800 K, 3시드 **각각** 적합).~~
> ⛔ **2026-09-07 마감으로 이것도 죽었다 (2026-09-09 정정).** `D-2026-09-07-b2o3-md-closure-retrospective`
> (active·비준)가 b2o3 UMA-MD 축 **전체**(D·Ea·σ·**구간 Ea 포함**)를 닫았다 —
> `db/properties/b2o3_md_closed_retrospective_2026_08_25.json` 금지 서술:
> *"b2o3 의 D · Ea · σ · 구간 Ea 중 **어느 것도** 물질 값으로 인용 — 0.222 eV 포함."*
> 사유는 굽음이 아니라 **골격 게이트 실측**(700 K 이상에서 비-Li β 가 rigid 기준을 넘는다) —
> 즉 그 D 가 무엇을 잰 값인지 정의되지 않는다. **이 축에서 쓸 수 있는 수는 0개**이고,
> 말할 수 있는 것은 그 카드의 `허용_서술_이대로만` 4문장뿐이다.
> (인용위험 원장: `citation_hazards.json` `HZ-b2o3-md-ea` = **BLOCKED**, 대체값 없음.)
> ⚠ σ(300 K) 도 같이 철회 — 재계산 **38.39 ± 51.09 mS/cm**(시드 8.46–97.38, 11.5배).
> 표준편차가 평균보다 크다: 철회한 18.51 은 이 범위 **안에** 있다. 틀렸다기보다
> **의미 없이 정밀했다.**
> 근거: `kb/results/b2o3_arrhenius_curvature_2026_08_23.md` ·
> `db/properties/b2o3_md_arrhenius.json` (`⛔_RETRACTED_2026_08_23`)
**⚠ 보류 범위를 정확히 (2026-08-20 전수 재독 정정)** — 초판이 *"+B₂O₃ 전도도 1등도 보류"* 라고
뭉뚱그렸는데 **과했다.** 그 서술의 근거를 추적하면 두 다리가 갈린다(`kb/open_items.md` #11):

| 주장 | 근거 | 이번 발견에 걸리나 |
|---|---|---|
| **"수송 축 1등"** (덱의 실제 문장) | **PMF ΔF_perc 0.1607 eV @600 K** (4시드) < modelc 0.173 | ⚠ **직접 안 걸린다** — 걸린 온도는 800/1000 K다. 600 K 는 b2o3_full β 0.01(rigid)이고 reseed s2 의 P(n=8, 경계 표본) 0.55 하나만 흔들린다 |
| ~~**Ea 0.199 ± 0.034**~~ | 아레니우스 600/800/1000 3점 | ⛔ **2026-08-23 철회** — 보류가 아니다. 굽음 145 meV (위 인용블록) |

⇒ **보류 대상은 Ea(아레니우스)이고, 600 K PMF 기반 "수송 축 1등" 은 별개로 판정해야 한다.**
(덱은 이미 *"best MD free-energy barrier @600 K — 정적 수송 축은 오히려 탈락"* 으로 좁혀 놨다.)
⚠ 그렇다고 PMF 가 무사하다는 뜻도 아니다 — 600 K reseed 시드 산포가 남았고, PMF 는
같은 궤적에서 나온 양이다. **"이번 발견으로는 못 건드린다" 까지**가 정확한 말이다.

상세: `kb/reviews/codex_B_neb_md_tools_2026_08_20.md` §0 · §5(B-R1, B-R2).
⚠ **문턱(β 0.30/0.60, MIN_N 8)은 13~19런 분포에서 정한 자의적 상수**다 — 교차검증 대상.

⚠ **옛 런 21개는 원리적으로 검사 불가**(traj 미보존). **앞으로는 `--save_traj` 를 켠다.**

### 6-3. 🆕 UMA 검증 앵커 (2026-08-19~20) — 이제 모델을 의심하지 않는다

`kb/results/uma_force_accuracy_li3ps4_2026_08_19.md` · `db/properties/mlip_bench_li3ps4_uma.json`

| 측정 | 값 | 무엇을 닫나 |
|---|---|---|
| Li₃PS₄ **힘 MAE** | **30.0 meV/Å** (Li 13.2) | 같은 test set 의 **전용 모델 35.6 · PET-MAD 기저 63.9** 보다 정확 ⇒ **"UMA 황화물 PES 연화" 알리바이 철회** |
| 보존성 | δ 의존성 6배↓ + 재실행 비재현 | 힘 = −∇E. "D 과대는 힘이 gradient 가 아니어서" 가설 사망 |
| Li₃P 잔여력 | fmax 0.0205 eV/Å | Li 금속 계면 1차 관문 통과 |

⚠ **한정**: 힘 축에서만이다(에너지는 전용 모델이 앞선다) · **응력·장벽은 안 쟀다** ·
보존성은 **near-minimum 배치 원자 4개** 표본 · 조성에 **Cl 이 없다**(Li₃PS₄).

---

## 6b. 🆕 NEB 장벽 (2026-08-20 신설)

**왜 축이 필요한가.** 일주일째 DFT(`neb.x`)와 MLIP(ASE NEB) 양쪽으로 장벽을 내면서
이 문서에 항목이 없었다. 그 사이 **같은 물질의 장벽이 세 값**으로 갈리는 일이 실제로 일어났다
(Li₃Nd: 0.229 수렴 / 2.56 미수렴 / 2.07 은 애초에 **자리 에너지 차**지 장벽이 아님).

**맞춰야 할 축**

1. **셀 크기(수직폭)** — 제일 크다. `1×1×1 → 2×2×2` 로 키우면 장벽이 **1.3–3.3배 내려간다**
   (6홉/4화합물, **예외 0** — `kb/results/neb_cell_size_trend_2026_08_20.md`).
   ⚠ `argyrodite_cage_neb.py` 의 `MIN_WIDTH_A = 10.0` 은 **최소 요건이지 수렴 보증이 아니다.**
2. **전하 규약** — DFT 는 `electronic_class` 로 갈린다(절연체 = V_Li⁻ + jellium / 금속 = 중성).
   **UMA 는 전하를 모른다**(중성 공공). ⇒ UMA↔DFT 장벽 비교에는 이 항이 섞여 있다.
3. **CI 를 켜는 순서** — **미수렴 밴드에 CI 를 걸면 안 된다.** 제일 높은 이미지가 안장 근처가
   아니라서 엉뚱한 방향으로 벽을 탄다(실측: +2.31/+2.38 eV 폭주).
   ⇒ `no-CI` 로 밴드를 먼저 수렴시키고 **그다음** CI. 총 iteration 이 오히려 준다.
4. **끝점이 진짜 국소 최소인가** — 공공을 뚫으면 부격자가 재배열하려 드는데 FIRE 는 **얕은 분지
   바닥에서 멈춘다.** comp1 2×1×1 에서 **55 meV** 를 회수했고 그때 ΔE(끝−시작)가
   −59.9 → −4.6 meV 로 대칭이 됐다. ⇒ 이완→rattle→재이완(`relax_endpoint_deep`).
5. **경로(홉) 동일성** — 두 값을 비교하기 전에 **같은 채널인지** 확인한다. 다르면 "셀 효과" 가
   아니라 "다른 사건" 이다.
6. 🆕 **그 경로가 elementary 인가** (2026-08-20 추가) — 이게 제일 먼저 물어야 할 것이다.
   comp1 inter (20,29) 는 **아니었다**: **중간 이미지가 두 끝점보다 낮고**(−0.46/−0.23 eV)
   밴드가 발산하며(fmax 상승 82 %) 홉 거리가 3.504 → **4.37 Å** 로 벌어진다
   — **심화 이완을 켜든 끄든 같다**(대조 실행 4.356 vs 4.369).
   ⇒ **경로 위에 중간 최소가 있다**. 이동 Li 가 **중간 자리를 거쳐 가는 다단계 과정**이고,
   그걸 7이미지 단일 밴드로 덮으면 스프링이 이미지를 반대로 끌어 발산한다.
   ⚠ 이것을 **협동 이동(다중 Li 동시)으로 읽으면 안 된다** — 초판이 그렇게 썼다가 철회했다.
   중간 최소도 홉 거리 변화도 **단일 Li 로 설명된다**(목표 자리가 그 Li 의 최소가 아니었다).
   협동이 없다는 뜻은 아니고 **이 데이터로는 못 가른다.**
   **처방**: 중간 이미지 배치를 뽑아 이완 → 중간 자리 동정 → **2분할 NEB**.
   ⭕ **실패가 아니라 결과다** — 그리고 **NEB 0.528 vs MD 0.253 격차의 "경로 선택" 가설에
   붙는 첫 실측**이다(동역학은 낮은 부분장벽의 다단계로 가는데 단일경로 NEB 가 복합 도약을 강제).
   유효 장벽의 정본은 이럴 때 **MD 축**(comp1 0.253 eV)이고 NEB 는 기전 확인용이다.

**믿으면 안 되는 신호** (도구가 자동으로 찍는다)
- 이웃 이미지 간 도약 > **0.8 eV** → 밴드 불연속(이미지가 터졌다)
- 중간 이미지가 두 끝점 중 **낮은 쪽보다 낮다** → 끝점이 국소 최소가 아니다
- 밴드 미수렴 시 **fmax 꼬리 추세** — `rising` 이면 `--neb_steps` 를 늘려도 소용없다

**⛔ MLIP 장벽 절대값 인용 금지.** Li₃Nd 에서 UMA 는 c–c 를 **1.76배 과대**했다(0.403 vs DFT 0.229).
MLIP NEB 의 용도는 **경로 선택**이다 — 실제로 정찰이 "b–c 는 안 일어나는 홉"(끝점차 +2206 meV)을
맞게 골랐고 DFT 자리차(+2072 meV)와 6 % 안에서 일치했다.

---

## 7. Phonon(UMA Γ) · ε∞(ph.x epsil)

- **Phonon:** UMA Γ-point, 안정성 판정 (comp2_v3 champion STABLE, lowest +32.7 cm⁻¹). MLIP라 pseudo 무관.
- **ε∞:** QE ph.x `epsil=.true. trans=.false.` (E-field DFPT, PAW). 52원자라 무거움(setup+iter). 슬라이드 5항목에 **미포함(곁가지)**. 진행: ibb 112952 (timeout 120h/5일). representation 156 나열은 trans=.false.여도 **정상**(오염 아님).

---

## 8. 정리 액션 목록 (2026-07-23 재구축) — **이력이다**

> 아래 ✅ 는 *그때 그 작업을 했다* 는 기록이지 *지금 인용해도 된다* 가 아니다.
> 인용 가능 여부는 언제나 `db/properties/canonical_registry.json` · `citation_hazards.json` 이 정한다.

- [x] **MLIP-elastic 삭제** — elastic.json 4섹션 + comp1~5·modelc 13키 + _index 152 data_points 제거(값 보존 검증). MD/전도도/phonon/EOS MLIP 유지. ✅
- [x] **elastic.json 셋업 메타 소급** — comp1_v3/modelc_v3 (pseudo·ecut·k·cell). ✅
- [x] **comp2 비정상 v2 elastic 격리** — `comp2.json` `_WARNING`(정본=comp2_elastic_uspp 재측정). ✅
- [x] **modelc ICOHP -5.12 stale** — `modelc_v3.json` `_superseded`(ext-basis -6.0 정본). ✅
- [x] **modelc EOS 19.59 통일** — `modelc.json` status LEGACY(eos.json 21.71 PRIMARY). ✅
- [x] **band gap 폐기 명기** — DOS-thr 1.76/1.82 + 1.65 `_DEPRECATED`(eigenvalue canonical). ✅
- [x] **comp3/4/5 elastic 강등** — elastic.json `_status`(v1 clamped, v3 재측정 필요). ✅
- [x] **다운스트림 동기화** — adhesion mlip 상관 deprecated, kb/methodology/elastic_constants.md 갱신. ✅
- [x] **litdb whitten2023 gap** — DOS-thr 1.76/1.82 → eigenvalue 2.066/2.099 (litdb 전수감사 결과 유일 stale). ✅

### 남은 것 (사용자 결정 대기)
- [ ] **doping_cascade UMA-elastic**(E_VRH/E_young) 삭제 여부 — EOS_B0/형성E는 존치.
- [ ] **litdb 커버리지 확장** — Kim 2025 halogen-modulus/Kim 2026 I-rich를 litdb papers에 등록(현재 elastic.json literature 섹션에만 존재); comp2/lpsocl/b2o3 문헌 비교행 추가; modelc elastic 각주(rhombo-62 셀 差).

## 9. Pseudo 규율 (앞으로 새 DFT 계산 시)

- **elastic/EOS/gap/ε∞ (DFT):** **USPP** — li/s/cl/br `v1.4.uspp.F` + P `pbe-n-rrkjus_psl.1.0.0`. ecut는 계열별: **comp1/comp2 계열 = 52/520**, modelc/lpsocl 계열 = 60/480 (기존값 유지; 새 비교쌍은 comp1 기준 52/520).
- **comp2 champion 구조는 PAW**(kjpaw, LOBSTER용) — elastic은 **반드시 USPP로 분리**해서 comp1과 맞춘다.
- **ICOHP:** all-PAW 필수 (kjpaw).
- **MD/phonon:** UMA (pseudo 개념 없음).
- **★새 비교표를 만들기 전 체크리스트 (DFT):** pseudo 같나? ecut 같나? k-density 같나? 셀타입 같나? clamped/relaxed 같나? — 하나라도 다르면 순위/각주 또는 재측정.
- 🆕 **★MD 표 체크리스트 (2026-08-20):** UMA버전 같나? 프로토콜 같나? **멀티시드인가?**
  **상자 크기 같나?**(1.65배 움직인다 — §6-1) **골격 게이트 통과했나?**(§6-2)
  — 하나라도 다르면 절대값 비교 금지.
- 🆕 **★NEB 표 체크리스트 (2026-08-20):** 셀 수직폭 같나?(1.3–3.3배 — §6b) 전하 규약 같나?
  **밴드가 수렴했나?**(미수렴 값은 값이 아니다) 끝점이 국소 최소인가? **같은 홉인가?**

---

## 10. 🆕 진행 중이라 아직 정본이 아닌 것 (2026-08-20)

이 절은 **"안 했다" 와 "하는 중" 과 "못 한다" 를 구분**하려고 둔다. 여기 있는 것은 인용 금지.

| 항목 | 상태 | 무엇을 기다리나 |
|---|---|---|
| ~~**b2o3 Ea 0.199±0.034**~~ | ⛔ **철회 (2026-08-23) → 축 전체 마감 (2026-09-07 비준)** | 기다릴 것이 없다. ~~쓸 값은 구간 0.2241±0.0606~~ ⛔ **그것도 인용 불가** — `b2o3_md_closed_retrospective_2026_08_25.json` |
| **b2o3 σ(300 K)** | ⛔ **철회 · 절대값 인용 금지** | 3시드 재계산 38.39±51.09 mS/cm — 표준편차>평균. 자릿수도 안 잡힌다 |
| **b2o3 vs modelc σ 비** (1.08/0.82/1.15) | ⛔ **`citable:false` · `source_pending`** | 재는 것이 없다 — 동등·보존·순위·기전·RT 외삽 전부 금지(레지스트리 `md-sigma-ratio-v1__NON_CITABLE`). 허용 문장은 그 항목의 `allowed_sentence` 하나 |
| **modelc 굽음 여부** | ⏸ **안 연다 (1저자 결정 2026-09-07)** | 대기가 아니다 — `md_axis_status_2026_09_07.md` §6-① *"나중에 한다 · 지금은 안 연다"*. LPSOCl 3×3×1 뒤로 |
| **"+B₂O₃ 수송 축 1등"** (PMF ΔF_perc 0.1607 @600 K) | 🟡 **별건** | 이번 발견은 800/1000 K 라 **직접 안 걸린다.** 600 K reseed 시드 산포만 남음 (§6-2 범위 표) |
| **Li₃Nd 장벽** (`sei_neb.json` 의 0.229 "인용 가능") | 🟡 재검토 | `cc333`(12.70 Å) 수렴. 셀 추세대로면 **0.229 이하**여야 정합 |
| **comp1 inter 장벽** | 🟡 미확정 | 밴드가 발산 중(fmax 상승). 끝점 구성부터 재진단 |
| **cascade 부피 편향 +32.7 %** | 🟡 미해결 | **응력을 아무것도 안 쟀다.** stress 파인튜닝(`efs`)이 후보 |
| **cascade predictor 보고 형식** | ✅ **형식만 해결 (2026-08-20)** | 질문의 전제가 틀렸다 — 아래 참조. ⚠ **축 자체는 회신 AL(2026-08-30) NO-GO hold** 이고 보고량은 2026-09-08 에 재정의됐다(`db/properties/cascade_d_rel_estimand_2026_09_08.json`). 형식 판정이 캠페인 승인이 아니다 |

> ⛔ **2026-08-20 정정 — "랜덤 0.986 vs LOCO 0.220" 은 누출 대 진짜의 대비가 아니다.**
> 두 숫자는 **다른 질문의 답**이라 나란히 놓으면 안 된다.
>
> `codoping_ml_v2_meta.json` 의 `stage1_single_dopant_ridge` 를 보면 **타깃이
> `cascade v23 score` — 우리가 만든 합성 지표이지 물성 실측이 아니다.** LOOCV R² **0.9998**
> 은 "점수를 만든 특징들로 그 점수를 되맞춘" 값이므로 높은 게 당연하고, **예측 성능 지표가
> 아니다.** 도구 자신의 `limitations` 가 이미 그렇게 적고 있다: *"이 모델은 그 휴리스틱의
> **해부+확장**이지 물성 예측이 아님"*.
>
> **보고 형식 (확정)**
> - 이 숫자는 **성능이 아니라 해부**로 보고한다 — "cascade score 의 분산이 16개 특징 +
>   group one-hot 의 선형결합으로 거의 전부 설명된다 ⇒ **우리 점수는 사실상 그 특징들의
>   가중합이다**". 이건 유용한 정보다: *점수가 무엇을 보고 있는지*를 말해준다.
> - **물성 예측력은 별도 지표로만** 말한다. repo 실측은 co-doping 쪽 `cascade_audit_ml_validation.csv`:
>   pair LOOCV **0.0892** · LODO **−0.1805** · L2DO **−0.2548** (⇒ *worse than mean*).
>   그리고 산출물 지위가 이미 `HYPOTHESIS GENERATOR — NOT VALIDATED` 다.
> - ⛔ 두 숫자를 **한 표에 나란히 쓰지 않는다.** "누출 상한 0.986 → 진짜 0.220" 이라는
>   서술은 **둘이 같은 것을 재는 척**하므로 금지한다.
> - ⚠ codex 리뷰가 인용한 **0.986 은 repo 실측(0.9998)과 다르다** — 출처 미상이다.
>   어느 쪽이든 결론은 같지만(둘 다 합성 점수 재현도), **인용할 때는 0.9998 을 쓴다.**
>
> ⚠ 남는 진짜 결함 (Kauwe 2021 기준, `litdb/comparison_vs_ours.md` J-4): 특징이 도펀트
> one-hot + 상수 2개라 **외삽 근거 이전 불가** · 상위 1 % 탐색인데 6타깃 전부 **회귀**
> (문헌은 분류가 precision 0.56 vs 0.39–0.44 로 우월) · 단일 시드 `random_state=42`
> (**우리 멀티시드 규율과 불일치**) · `DummyRegressor` 구현은 있으나 **미보고**.
> 이 넷은 보고 형식과 별개로 남는다.

교차검증 작업지시서: `kb/reviews/codex_A_cascade_ml_2026_08_20.md`(cascade+ML) ·
`kb/reviews/codex_B_neb_md_tools_2026_08_20.md`(NEB+MD+도구).

---

*갱신 이력:*
*· 2026-07-23 최초 작성 (Explore 전수감사 + 백업 입력 실측). db 정리 진행에 따라 §8 체크박스 갱신.*
*· **2026-08-20** 축 4개 추가 — NEB(§1 표·§6b) · MD 상자 크기(§6-1) · 골격 게이트(§6-2) ·*
*  UMA 검증 앵커(§6-3). §9 에 MD/NEB 체크리스트, §10 에 "정본 아님" 목록 신설.*
*  **값은 안 건드렸다** — 값의 정본은 각 db 파일이고 이 문서는 일관성 축만 정한다.*
*· **2026-09-09** 인용지위 정정 — §6 Ea 표에 레지스트리 status 열 + 계간 비교 금지 배너,*
*  "같은 UMA·프로토콜·멀티시드면 성립" 폐기, §6-2 의 "쓸 수 있는 것 0.2241" 을 b2o3 축 마감으로*
*  정정, §10 의 modelc 굽음·σ 비 행 갱신, §2 표에 γ/W_ad **정본 미등록** 표시, 머리에 인용 순서 3줄.*
*  **값은 이번에도 안 건드렸다** — 바꾼 것은 지위 표기다.*

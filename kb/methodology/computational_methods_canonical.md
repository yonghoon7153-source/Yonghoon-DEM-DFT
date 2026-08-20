# 계산 방법 Canonical — 단일 기준 (2026-07-23 재정리 · **2026-08-20 축 4개 추가**)

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
| **탄성 Cij / E / G / B** | ✅ 있음 (relaxed-ion, k×L=40) | ★ paper-grade | 위 §2 그대로 |
| **표면에너지 γ** | ✅ 있음 — `adhesion.json` `surface_energies` | ⚠ **UMA 슬랩** | 같은 파일에 vacuum 아티팩트 이력(`vacuum_sensitivity`, 60 Å 에서 10× 폭주). **vacuum 30 Å 고정** |
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

### 6-1. 🆕 상자 크기도 일관성 축이다 (2026-08-20 추가)

`kb/results/lpsocl_box_size_600K_2026_08_18.md` — LPSOCl 600 K 를 3×3×1(558원자·3시드)로 키웠더니:

| | 기존 셀 | 3×3×1 | 비 |
|---|---|---|---|
| MSD@50ps | 25.3 Å² | **41.7 Å²** | **1.65×** |

**곡선의 모양(β)은 안 변하고 기울기(D)만 1.64 ± 0.14 배 움직인다.**
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
⇒ `Ea 0.199±0.034` · "+B₂O₃ 전도도 1등" 은 **codex 교차검증까지 인용 보류.**
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
6. 🆕 **그 홉이 애초에 단일 Li 사건인가** (2026-08-20 추가) — 이게 제일 먼저 물어야 할 것이다.
   comp1 inter (20,29) 는 **아니었다**: 심화 이완을 켜든 끄든(대조 실행 확인) 홉 거리가
   3.504 → **4.37 Å** 로 벌어지고 **중간 이미지가 두 끝점보다 낮으며** 밴드가 발산한다
   (fmax 상승 82 %). 계가 **협동 재배열**을 더 선호하는데 단일 경로를 강제한 결과다.
   ⇒ 이 도구는 *"협동 이동(다중 Li 동시)을 못 본다"* 를 docstring 에 적어 두었고, 이 경우가 그것이다.
   ⭕ **실패가 아니라 결과다** — "이 홉은 단일 Li 로 일어나지 않는다" 는 기전 정보다.
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

## 8. 정리 액션 목록 (2026-07-23 재구축)

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
| **b2o3 Ea 0.199±0.034 · "+B₂O₃ 1등"** | 🔴 **보류** | 골격 게이트 β 0.59/0.63 의 해석 (§6-2) — codex 교차검증 |
| **Li₃Nd 장벽** (`sei_neb.json` 의 0.229 "인용 가능") | 🟡 재검토 | `cc333`(12.70 Å) 수렴. 셀 추세대로면 **0.229 이하**여야 정합 |
| **comp1 inter 장벽** | 🟡 미확정 | 밴드가 발산 중(fmax 상승). 끝점 구성부터 재진단 |
| **cascade 부피 편향 +32.7 %** | 🟡 미해결 | **응력을 아무것도 안 쟀다.** stress 파인튜닝(`efs`)이 후보 |
| **cascade predictor 보고 형식** | 🟡 미해결 | 랜덤 CV 0.986 은 누출값 · LOCO 0.220 — **무엇을 보고할지** 미정 |

교차검증 작업지시서: `kb/reviews/codex_A_cascade_ml_2026_08_20.md`(cascade+ML) ·
`kb/reviews/codex_B_neb_md_tools_2026_08_20.md`(NEB+MD+도구).

---

*갱신 이력:*
*· 2026-07-23 최초 작성 (Explore 전수감사 + 백업 입력 실측). db 정리 진행에 따라 §8 체크박스 갱신.*
*· **2026-08-20** 축 4개 추가 — NEB(§1 표·§6b) · MD 상자 크기(§6-1) · 골격 게이트(§6-2) ·*
*  UMA 검증 앵커(§6-3). §9 에 MD/NEB 체크리스트, §10 에 "정본 아님" 목록 신설.*
*  **값은 안 건드렸다** — 값의 정본은 각 db 파일이고 이 문서는 일관성 축만 정한다.*

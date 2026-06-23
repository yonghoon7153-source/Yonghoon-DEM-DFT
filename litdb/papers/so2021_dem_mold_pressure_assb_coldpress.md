# 몰드압력이 ASSB 압밀·이온전도도에 미치는 영향 — 소성변형 포함 3D DEM cold-press 모델 — So (J. Power Sources 2021)

> slug `so2021_dem_mold_pressure_assb_coldpress` · DOI `10.1016/j.jpowsour.2021.230344` · type `DEM` · PDF `So_2021_JPS_DEM_mold_pressure_ASSB_cold_pressing.pdf` · digested `2026-06-23` · status ✅

## 1. 한 줄 요약
**소성변형(plastic deformation)을 명시적으로 넣은 3D cold-press DEM**(in-house MATLAB, 비선형 Hertz+hysteresis)으로
LPS(Li₂S–P₂S₅) SE + Si AM 전극의 압밀(상대밀도)과 SE 이온전도도(σ_SE^rel)를 몰드압력·AM조성 함수로 예측 —
**볼밀 응집체(aggregate)가 SE 연결망에 강한 percolation threshold(φ_SE^crit ≈ 0.13)를 만든다**는 것이 핵심 발견이며,
이는 이온전도도가 표준 Bruggeman을 따르지 않고 percolation 보정식이 필요한 이유를 설명한다.
이 논문은 우리가 줄곧 인용·비교해 온 **So 2020 2D 모델 [27]의 3D 확장판**이자 LIGGGHTS 이전 시대의 DEM-ASSB 정초 논문이다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Magnus So, Gen Inoue (교신), Ryusei Hirate, Keita Nunoshita, Shota Ishikawa, Yoshifumi Tsuge (**Kyushu University**, Dept. Chemical Engineering) | J. Power Sources **508** (2021) 230344 | 10.1016/j.jpowsour.2021.230344 | **LPS = Li₂S–P₂S₅ (amorphous lithium-phosphate-sulfide)** SE + **Si** AM (음극) | **3D DEM** (소성변형 포함 cold-press), 실험 Sakuda·Nakamura와 대조 |

> ⚠ 소재 주의: 우리(LPSCl + NMC811)와 **다르다**. 여기 SE는 **LPS(Li₂S–P₂S₅, argyrodite 아님)**, AM은 **Si 음극활물질(NMC 양극 아님)**. 절대값 전이 금지, 추세·방법만.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| 상대밀도 (relative density) | 초기 ~0.30 → ~0.85 @ ~300 MPa → ~0.98 @ 600 MPa | f_AM=0 (pure-SE), 몰드압 sweep | digitized (Fig 4b/c) | **Sakuda 실험과 잘 일치** (Fig 4b 다이아) |
| 상대밀도 vs f_AM | @600 MPa: f_AM=0 ≈0.98 / 30% ≈0.93 / 50% ≈0.86 / 70% ≈0.76 | 600 MPa | digitized (Fig 4c) | AM↑ → 최종밀도↓ (Si가 덜 압밀) |
| 전극 두께 (SE층) | 80.0 µm(초기) → 33.6(@100MPa) → 26.5 µm(@400MPa) | pure-SE | stated (Fig 2 라벨) | 압력↑ → 압축↑ |
| 전극 두께 (anode f_AM=0.5) | 62.1 → 36.4(@100) → 29.3 µm(@400) | f_AM=0.5 | stated (Fig 3 라벨) | |
| σ_SE^rel (상대 이온전도) | φ_SE→1에서 ~1, **φ_SE^crit ≈ 0.13에서 0으로 급락** | 200–400 MPa fit | stated (eq 16, φ_SE^crit=0.13) | percolation threshold; Bruggeman 이탈 |
| σ_SE^rel vs f_AM | @~300MPa: f_AM=0 ≈0.7 / 30% ≈0.4 / 50% ≈0.2 / 70% ≈0.02 | Fig 7a | digitized | AM↑ → SE연결↓ → σ↓ |
| SE coverage on AM | @600MPa: f_AM=30% ≈0.73 / 50% ≈0.53 / 70% ≈0.30 | Fig 4d | digitized | AM↑ → coverage↓ (SE 부족) |
| tortuosity factor τ_SE | f_AM=0: ~3(@50MPa) → ~1.5(@400); f_AM=70%: ~10 → ~5 | Fig 7b | digitized | 압력↑→τ↓, AM↑→τ↑ |
| Bruggeman exponent α | α=1.5 (이상), 실험은 2.2<α<3.6 (modified) | 문헌 인용 §1.3 | stated | 그들 결론: modified Bruggeman도 부정확 → percolation식 필요 |
| equilibrium overlap ratio (h_ov/4R_eff) | median 0→@400 약 0.07; SE-SE ≈0.10(압력무관 高), AM-SE 0.025→0.082, AM-AM ≈0.007(거의 0) | Fig 6 | digitized | 소성 융착 정도; **AM-AM은 소성 거의 안 함** |
| compressive stress (입자간) | AM-AM 2.5→5.9 GPa, AM-SE ~1.0(flat), SE-SE 0.2→1.1 GPa (25→400MPa) | Fig 5d | digitized | **AM-AM에 응력 집중** (Si 단단) |
| **E_SE (LPS)** | **24 GPa** | Sakuda et al. [12] | stated (Table 1) | = 우리 real bulk와 같은 값(우연; 소재는 LPS) |
| **E_AM (Si)** | **70 GPa** | Sethuraman [37] | stated (Table 1) | Si 음극 (NMC 140과 다름) |
| **H_AM (Si hardness)** | **10.6 GPa** | de Vasconcelos [38] | stated (Table 1) | 소성항복 임계 (eq 14) |
| **H_SE (LPS hardness)** | **1.9 GPa** | McGrogan [8] | stated (Table 1) | LPS가 Si보다 5.6× 무름 → SE만 소성 |
| ν (Poisson) | 0.3 (both) | This study | stated (Table 1) | |
| μ (마찰계수) | 0.5 | This study | stated (Table 1) | |
| e (반발계수 COR) | 0.5 | This study | stated (Table 1) | damping η = f(e), eq 9 |
| 입자수 / aggregate | ~45,000 입자; aggregate 크기 20 µm | | stated | annealing으로 branch-like 응집체 |
| PSD (D10/D50/D90) | n/a (명시 PSD 표 없음; aggregate=20µm, 1 AM≈150 SE 이웃) | | n/a | SE는 random-walk 응집체, 단일 1차입경 미명시 |
| 도메인 | 25 × 25 µm (측방, 주기) × 가변높이; pure-SE 초기 80µm | | stated (Fig 2/3) | |
| Heckel P_y / knee | n/a (Heckel 안 함) | | n/a | relative-density-vs-P 곡선만; knee ~100 MPa 부근 |

## 4. 시뮬레이션 방법 ★
- **code / version**: **in-house MATLAB** DEM (LAMMPS/LIGGGHTS 아님). 2차 정확도 Verlet 적분. 이웃탐색은 **kd-tree(knnsearch/createns)**, AM-AM/AM-SE/SE-SE 그룹 분리 탐색(이웃수 20/150/20 — AM 1개를 SE ~150개가 감쌈). Intel Xeon W-2145(8코어), 1 sim ≈ 25분.
- **DEM 접촉법칙** ★: **비선형 Hertzian spring(탄성) + hysteresis 소성변형 모델**. 3단계로 다른 force law:
  - 법선력 `F_n = (−F_spring + η(u_i−u_j)·n)n` (eq 4).
  - **탄성/settling 단계**: `F_spring = k_n·h_ov`, `k_n = 4/3·E_eff·√R_eff·h_ov^{1/2}` (eq 5–6, Hertz). 소성 무시.
  - **소성/cold-press 단계** ★: 평형 overlap `h_eq` 도입 — 소성변형으로 접촉점이 비구형이 된 새 위치. `F_spring = k_n(h_ov − h_eq)` (eq 12). overlap 변화율 `∂h_eq/∂t = (F_spring − F_th)/(t_rel·k_n)` (eq 13), 임계력 `F_th = 2/3·min(H_i,H_j)·A_con` (eq 14, 포물선 응력분포 2/3 인자, **재료 경도 H로 항복 결정**), 접촉면적 `A_con = π·h_ov·R_eff` (eq 15). t_rel=완화시간.
  - 접선 마찰 Coulomb `|F_t| ≤ μ|F_n|` (eq 11). damping `η = −2ln(e)√(m_eff·k_n)/√(ln²(e)+π²)` (eq 9).
- **재료 파라미터**: E_SE(LPS)=24, E_AM(Si)=70 GPa, ν=0.3, μ=0.5, e=0.5, H_AM=10.6 GPa(Si), H_SE=1.9 GPa(LPS). 벽-입자는 R_wall=∞로 동일 접촉식 사용(eq 7).
- **bond/binder 모델**: 명시 binder 없음(LIB calendering의 carbon-binder 도메인과 달리 SE 전극). 대신 **annealing 응집체 내 융착결합(fusion bond)** = cohesive 접촉으로 표현(볼밀 후 응집체가 강한 결합 보유 → 초기 overlap≠0).
- **MPM/continuum**: 없음 (순수 DEM).
- **전달 솔버** ★: **Kirchhoff 망 아님**. cold-press 후 입자→3D grid 매핑으로 SE 부피분율 φ_SE 추출 후 **TauFactor**(Cooper et al. [39], 외부 MATLAB, 주기경계 포함 pre-release v2)로 **tortuosity factor τ_SE와 relative diffusion coefficient** 계산 → `σ_SE^eff = σ_SE^rel·σ_SE^bulk = (φ_SE/τ_SE)·σ_SE^bulk` (eq 1). **소성변형 때문에 단순 반경탐색은 부피분율을 과소평가** → 0.1% 허용오차로 threshold distance를 반복 보정.
  - **핵심 새 식 (eq 16)**: `σ_SE^rel = [(φ_SE − φ_SE^crit)/(1 − φ_SE^crit)]^{1/2}`, **φ_SE^crit = 0.13** (200–400 MPa fit). percolation 기반 — φ_SE^crit 이하에서 σ=0. (eq 3 표준 Bruggeman `σ_SE^rel = φ_SE^α/γ`, α=1.5 이상/2.2–3.6 modified와 대비.)
- **입자 처리** ★★ (DEM판 "무질서 처리"):
  - **구(sphere)만** — AM·SE 모두 구. **형상은 절대 변하지 않음**. 소성은 **CONTACT 소성**(평형 overlap h_eq 도입 = 접촉점 국소 함몰의 proxy)이며 **진짜 입자 SHAPE 흐름(void-fill flow)이 아님**. 논문 스스로 §4.3에서 "AM을 구로 모델 → 비구형/intraparticle cracking은 future work"라고 명시.
  - 단, **소성변형을 명시적으로 모델**한 점이 Bazzoun/Varkey류 순수 Hertz보다 진전: h_eq가 영구잔류(hysteresis)이며 H로 항복을 건다 → "응집체 파괴 + 재배열 + 소성압밀"의 3단계 압밀을 재현.
  - SE = annealing random-walk로 만든 **branch-like 응집체(20µm)**; 단일 1차입경의 mono-disperse 구 집합이지만 **응집 구조 자체가 multi-scale 무질서** (이것이 percolation threshold의 근원).
- **도메인/RVE / 압력범위**: 25×25 µm 측방(주기경계 + ghost 입자), pure-SE 초기높이 80µm. **압력 sweep 50/100/200/400 MPa**(일부 25·600 포함, Fig 4b는 ~600까지). f_AM = 0/30/50/70%. seed 다중실현 명시 없음(단일 실현으로 보임).
- **특이사항/튜닝**: 3단계 분리 시뮬레이션 — (i) annealing(응집체 생성, shoving max overlap 0.4 R_eff), (ii) settling(중력패킹, 소성 무시 순수 Hertz, 저응력), (iii) cold-press(상단벽을 **PI 제어**로 목표 몰드압까지 가압 후 release). 압축해제 시 전극이 약간 **팽창(springback)** 관찰.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | DEM 접촉모델 모식: (a) spring+slider+dashpot, **(b) cold-press 중 overlap h_ov, (c) 압축후 평형overlap h_eq** | 우리 hooke/hysteresis의 소성 잔류 overlap과 같은 개념도 — h_eq = 우리 δ 잔류와 대응 |
| 2 | pure-SE층 입자분포 (초기/before/during/after, 100·400 MPa) + **Sakuda SEM(j–l) 직접대조** | 두께 80→33.6(@100)→26.5µm(@400); SEM과 morphology 정성비교 — 우리 vis_zoom 대비 |
| 3 | anode(f_AM=0.5) 3D 입자분포 (검은 큰 Si AM + 노란 SE), 100·400 MPa | bimodal 구조(큰 AM + 작은 SE 응집체); 두께 62.1→29.3µm |
| 4 | **(a)** 높이-시간 곡선(4압력), **(b)** 상대밀도 vs 몰드압 + Sakuda 실험검증, **(c)** 상대밀도 vs P (f_AM 0/30/50/70), **(d)** SE coverage on AM vs P | **(b) 실험검증** = 우리 porosity@P 앵커와 대응; (c) AM↑→밀도↓; (d) coverage 정의가 우리 coverage_AM과 비교대상 |
| 5 | anode 내부응력: (a) boxplot stress vs P, **(b) 400MPa 3D force-chain**, **(c) AM-AM/AM-SE/SE-SE histogram**, **(d) 입자쌍별 평균응력 vs P** | **AM-AM 응력 집중(2.5→5.9 GPa)**, SE-SE는 H_SE=1.9서 capped — 우리 force-chain/Stage-E 응력과 직접대응; "단단한 AM에 응력 몰림 → AM cracking 위험" |
| 6 | equilibrium overlap ratio (h_ov/4R_eff): (a) boxplot vs P, **(b) 입자쌍별 평균** | SE-SE 융착 ≈0.10(압력무관, 응집체 잔류), AM-SE 0.025→0.082(라미네이션↑), **AM-AM≈0.007(소성 거의 안 함)** — 소성이 phase별로 극명히 다름 |
| 7 | SE 이온전달: **(a) σ_SE^rel vs 몰드압** (f_AM 0/30/50/70, Sakuda·Nakamura 실험중첩), **(b) τ_SE vs 몰드압** | (a) 실험검증; AM 70%서 σ_SE^rel ≈0.02로 급락(percolation 임박); (b) τ가 압력↑·AM↓로 감소 — 우리 τ_Laplace/Dijkstra와 비교 |
| 8 | **핵심 결과**: **(a) σ_SE^rel vs φ_SE log-log + Bruggeman 이탈** (몰드압 컬러), **(b) eq16 새식 vs Sakuda·Nakamura 실험** (φ_SE^crit 0/0.1/0.13/0.2/0.4 곡선) | **graphical abstract의 그 그림** — 응집체가 만든 percolation threshold가 Bruggeman을 깨뜨림; φ_SE^crit=0.13이 데이터 최적 |

## 6. Post-processing ★
- **무엇**: ① **상대밀도/porosity** (입자→3D grid, 소성 보정으로 threshold distance 반복조정, 0.1% tol). ② **tortuosity factor τ_SE + relative diffusion** (TauFactor, 라플라스 확산 풀이 — 우리 τ_Laplace와 같은 종류). ③ **σ_SE^rel = φ_SE/τ_SE** → eq16 **percolation 보정식**으로 재정리(φ_SE^crit=0.13 fit). ④ **coverage on AM** (SE가 AM 표면 덮는 비율, Fig 4d). ⑤ **응력장 분석** (boxplot/histogram/force-chain, 입자쌍 type별 분해). ⑥ **equilibrium overlap ratio** (소성 융착 정도 정량).
- **도구**: 자체 MATLAB DEM + **TauFactor [39]**(Cooper, Imperial College, 주기경계 pre-release v2). 응력·overlap·밀도는 자체 후처리.
- **수치화·플롯·기록 방식**: 상대밀도·σ_SE^rel·τ를 몰드압(50–600 MPa)과 f_AM(0–70%)의 2D sweep으로. **Sakuda et al.[12] (f_AM=0) + Nakamura et al.[42] (f_AM=0.742) 실험에 직접 중첩** 검증. σ는 log-log(φ_SE) plot으로 Bruggeman 직선과 비교 → 이탈 → percolation식 유도.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (So 2021) | 우리 | 차이 / 이유 (rigid·plastic / 소재 / 2D·3D / 단일·다중압력) |
|---|---|---|---|
| **DEM 소성** | **CONTACT 소성 명시**(h_eq 평형overlap + H항복, hysteresis) — 진전 | DEM hooke/hysteresis(plasticity 無 by construction) + Stage-E(Tabor) 사후보정 | **같은 부류**: 둘 다 CONTACT-level 소성(δ/h_eq 잔류 overlap) — **진짜 SHAPE 흐름 아님**. 우리 MPM만 shape-flow. So의 h_eq+H항복은 우리 Stage-E의 DEM-내장판에 가깝다 |
| **입자 형상** | 구만(AM·SE), 형상 불변 | 동일(구·rigid) | **같음** — 둘 다 rigid sphere. So 스스로 비구형·AM cracking은 future work라 명시 → frame[1] 한계 동일 |
| **소재 SE** | **LPS (Li₂S–P₂S₅)**, E_SE=24 GPa | **LPSCl (argyrodite)**, E_eff 1.35 / real 24 | **다른 SE**(LPS vs LPSCl). E 값은 24로 우연히 같으나 결정구조·σ_grain 다름 → 절대 σ 전이 금지 |
| **소재 AM** | **Si 음극** (E=70, H=10.6 GPa) | **NMC811 양극** (E=140 GPa) | **다른 AM**(Si 음극 vs NMC 양극). Si는 H=10.6서 소성 거의 안 함(우리 NMC rigid와 유사하나 더 무름) |
| **E 연화** | **연화 안 함** — real E=24 그대로 사용 | E_eff=1.35 (18× 연화) | **핵심 차이**: So는 real E를 쓰고도 압밀 재현(상대밀도 Sakuda 일치) — **왜냐 h_eq 소성모델이 H에서 항복을 강제**하기 때문(국소 응력 cap). 우리 DEM은 항복 cap이 없어 18× 연화로 보상 → **So의 H-cap 소성이 우리 연화의 물리적 대안**(우리 MPM J2 항복과 같은 역할) |
| **차원** | **3D** (2D So 2020 [27]의 확장) | DEM 3D / MPM 2D·3D | **둘 다 3D 가능** — So 2021은 정확히 우리가 인용한 2D[27]의 3D 버전 |
| **압력** | **다중**(50/100/200/400, ~600) | DEM 단일 300 위주 + Heckel 4압력 | So가 다중압력 상대밀도-vs-P 풀곡선 보유 → 우리 Heckel(P_y=138) 검증에 유용 |
| **전달 솔버** | **TauFactor(τ만) → φ/τ** (Kirchhoff 망 아님) | **Kirchhoff + Holm 접촉저항** (망 명시) | **다른 방법**: So는 연속체 라플라스 τ만(접촉저항 無), 우리는 명시적 저항망. **우리가 접촉구속저항(Holm)·coverage·Stage-E 면적을 더 정밀히 다룸** |
| **percolation** | **φ_SE^crit=0.13 명시식 (eq16)** | √(φ−φc) (φc_P 0.200 / φc_S 0.195) | **둘 다 percolation threshold 채택**. So 0.13 < 우리 0.195–0.20 — **소재·정의차**(So는 응집체 SE의 임계, 우리는 mono-disperse SE의 임계; 응집체가 더 낮은 φ서 percolate) |
| **전달 채널** | σ_ionic만 (τ 경유) | σ_ionic + σ_e + σ_thermal | **우리 삼중항 우위** |
| **벽 마찰** | 벽 접촉만(R=∞), **명시적 mold-wall 마찰 sweep 없음** | 우리도 mold-wall 마찰 미연구 | 둘 다 wall-friction 효과는 미탐구 (공통 공백) |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **"real E + 접촉소성 H-cap" = 우리 18× 연화의 물리적 대안**. So는 E_SE=24(real)를 그대로 쓰고도 상대밀도 Sakuda 실험과 일치 — 비결은 **h_eq 평형overlap + F_th=2/3·H·A_con 항복**(국소 응력을 경도 H에서 cap). 우리 DEM은 항복 cap이 없어 24→1.35 연화로 보상하는데, **So의 H-cap 소성은 우리 MPM J2-항복(σ_y)과 정확히 같은 역할을 DEM 내부에서 수행**. → "연화는 IRREDUCIBLE"라는 우리 결론은 *우리 hooke/hysteresis에 항복 cap이 없기 때문*임을 So가 역으로 증명: **항복 cap을 DEM에 넣으면 real E로도 압밀 가능**. 이는 frame[2]의 "rigid-sphere DEM은 소성 없음" 진술을 정교화한다 — So는 **rigid-sphere이지만 CONTACT 소성(H-cap)은 있는** 중간 지대.
- ② **응집체(aggregate)가 percolation threshold의 근원** (φ_SE^crit=0.13). 우리 σ_ionic 폼의 √(φ−φc)와 같은 percolation 구조지만, So는 **볼밀 응집체가 만든 SE-SE 연결 부족**이 임계의 물리적 원인임을 명시(Fig 8: 응집 때문에 Bruggeman 이탈). → 우리 φc(0.195–0.20)와 So(0.13) 차이는 **SE 분산도(응집 vs mono-disperse) 차이**일 수 있음. 우리가 만약 응집 SE를 다루면 φc가 낮아질 것 — wet-chemical(분산) vs ball-mill(응집) SE의 σ 차이를 우리 폼에 반영할 단서.
- ③ **phase별 소성 비대칭 = 우리 Stage-E AM/SE 하중분배의 직접 근거**. So Fig 5d/6b: **AM-AM 응력 2.5→5.9 GPa로 집중(Si 단단), SE-SE는 1.9 GPa(H_SE)서 capped, AM-AM은 소성 거의 안 함(overlap 0.007)**. = 우리 "rigid AM skeleton이 하중 지지, SE만 소성"(real_14 AM-shielding, 복합 SE overlap 1.75%)와 **정성·정량 일치**. So는 이를 "AM cracking 위험"으로 해석 → 우리 Auerbach 균열 모델과 연결.

## 9. 인용 가능 문장 (deck/paper용)
- "So et al. (2021)의 3D cold-press DEM은 입자를 구로 유지하면서도 **접촉점 평형 overlap(h_eq)과 경도 기반 항복(F_th=2/3·H·A_con)**으로 소성변형을 명시 구현하여, real E_SE=24 GPa로도 상대밀도를 실험(Sakuda)과 일치시킨다 — 이는 항복 cap이 없는 우리 hooke/hysteresis DEM이 18× 연화를 필요로 하는 이유를 역으로 설명한다."
- "볼밀로 만든 SE 응집체는 SE-SE 연결을 부족하게 만들어 표준 Bruggeman을 깨뜨리는 강한 percolation threshold(φ_SE^crit ≈ 0.13)를 유발하며, So et al.은 이를 `σ_SE^rel = [(φ_SE−φ_SE^crit)/(1−φ_SE^crit)]^{1/2}` 의 percolation 보정식으로 포착했다."
- "압밀 시 응력은 단단한 Si AM-AM 접촉(2.5→5.9 GPa, 25→400 MPa)에 집중되고 무른 LPS SE는 H_SE=1.9 GPa에서 소성 cap되어, AM cracking이 SE 압밀보다 먼저 일어날 위험을 시사한다."

## 10. 주의/한계 (over-claim 방지)
- **소재가 다르다**: SE는 **LPS(Li₂S–P₂S₅, argyrodite 아님)**, AM은 **Si 음극(NMC811 양극 아님)**. σ_grain·E_CAM·H 모두 우리와 다름 → **절대 porosity·σ 직접 전이 금지, 추세·방법론만**. E_SE=24 GPa가 우리 real bulk와 같은 수치인 건 우연(LPS도 sulfide라 비슷).
- **rigid sphere + CONTACT 소성**: 입자 형상은 변하지 않음(h_eq는 접촉 함몰 proxy). **진짜 void-fill SHAPE 흐름은 없음** → 우리 MPM morphology 영역은 못 다룸(frame[5] 전달·압밀 절반). So 스스로 "비구형 AM·intraparticle cracking은 future work"라 명시.
- **σ_SE^rel은 상대값(τ-기반)**: TauFactor 라플라스 확산의 φ/τ만 — **명시적 접촉저항(Holm)·coverage·field-spreading 없음**. 절대 σ는 σ_SE^bulk 곱으로만 추정. 우리 Kirchhoff+Holm 솔버가 접촉구속을 더 정밀히 다룸.
- **φ_SE^crit=0.13은 LPS-응집체·200–400 MPa fit값**: 우리 mono-disperse SE의 φc(0.195–0.20)에 직접 대입 금지. 응집 정도에 의존.
- **그림 읽은 값(digitized)은 추세만(±)**: 상대밀도·σ_SE^rel·τ·overlap·응력 곡선의 수치는 Fig 4–8에서 읽은 근삿값. stated(Table 1 파라미터, 두께 라벨, φ_SE^crit, E/H)와 구분.
- **단일 실현으로 보임**: seed 다중실현·통계 명시 없음 → 우리 multi-seed 분산과 다름.
- **2021년·LIGGGHTS 이전**: in-house MATLAB DEM. Bazzoun(2026 LIGGGHTS)·Varkey(2026 Thornton-Ning)보다 이른 정초 논문 — 우리가 인용한 **So 2020 2D[27]의 3D 확장**임을 명심(같은 그룹·같은 모델 계보).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

# ⏳ pending — `zaby2026_reliable_conductivity_estimates_md` 의 INDEX / comparison 반영분
> ✅ **①②③ 병합 완료 2026-09-13** (조율 세션) — INDEX.md: ① 병합됨 · comparison_vs_ours.md: ② → J-0 · ③ → J-7. ⏳ **남은 것**: ④ inbox 확보 후보 미처리.

> 2026-09-09, litdb-curator. **동시작업 충돌 회피**(curator 8개 동시 실행)로 `INDEX.md` · `comparison_vs_ours.md` 를 직접 안 고쳤다.
> 아래 세 블록을 **사람이(또는 조율 담당 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/zaby2026_reliable_conductivity_estimates_md.md`
> 그림: `litdb/figures/zaby2026_reliable_conductivity_estimates_md/` (**PNG 47장** = 그림 22 + 표 25)
>
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` →
> `litdb/talks/lee2026_skku_mlip_materials_design.md` 하나뿐이고, **이 논문은 그 대기열 6건에 없다**
> (그 큐는 MTP/SevenNet/SKKU 계열). ⇒ **역링크 작업 없음.**

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

```markdown
| `papers/zaby2026_reliable_conductivity_estimates_md.md` | **[외부·methods·★★σ 추정 통계 원전 · ⛔물성값 0 · 계는 액체]** **Paul Zaby**, **Johannes Ingenmey\***, **Tuanan C. Lourenço\***, **Yong Zhang**, J. L. F. Da Silva, M. Brehm, **Edward J. Maginn**, **Barbara Kirchner\*** (U Bonn / UNESP / **Notre Dame** / USP / Paderborn), "**Lessons Learned on Obtaining Reliable Conductivity Estimates From Molecular Dynamics Simulations**" (***ChemPhysChem* 2026, 27: e70477**, DOI `10.1002/cphc.70477`, **OA CC BY** · 본문 19 pp + SI 32 pp · Fig 9 + Fig S1–S20 + Table 3 + Table S2–S23 · 접수 2026-04-13/수락 2026-06-16). ⚠ **1저자 기억 "Zaby·Ingenmey·Lourenço·Zhang" 은 앞 4명뿐 — 저자 8명이고 7번째가 Maginn**(이 논문 ref [94] LiveCoMS 베스트프랙티스의 1저자) ⇒ **Maginn 계열 베스트프랙티스의 "전도도 확장판"**. **⛔ 계는 이온액체 [EMIm][DCA] 와 에테르 전해질 LiFSI/DME 뿐 — 황화물·고체전해질 0회, 온도 1점(353/333 K), 온도 스캔·Ea 0건, DFT 0회.** **본체 = TRAVIS 신규 `conduct` 모듈**(EH·GK·self/cross 분해·좌표계 on-the-fly) + `github.com/kirchners-manta/conductivity_tools` + MSDiff v0.2.0. **MD**: LAMMPS 23Jun2022, **CL&Pol**(Drude 분극) / CL&P(전하 ×0.8), dt **1.0 fs**, cutoff 1.2 nm, PPPM, **TGNH**(Drude 1.0 K), **replica 10개**(PACKMOL 박스를 새로 만들어 배열+속도 모두 다름, 단 **밀도는 공통 평균부피로 통일**), **EH 생산 111 ns→100 ns**(위치 1 ps 덤프, 상관깊이 30 ns=30 %) + **GK 별도 0.1 ns**(위치·속도 **매 1 fs**, 깊이 75 ps), IL¹²⁵_long 은 811→800 ns. **★★ 실패 모드 8종(방향+크기)**: **F1 NE 사용 → σ 과대 1.31–2.08×**(ionicity **0.48–0.76**; cross 항이 self 의 **30–52 %**) · **F2 MSD 후반부 고정 적합(tail fit) → σ 과소 1.6–2.8×**(LiFSI 1.0 M 자동창 **60 ps–24 ns → 2.03** vs tail 15–30 ns **→ 0.73 S m⁻¹**, 실험 2.14±0.28) · **F3 단일 긴 궤적 토막내기 → SE 를 1.33–1.52× 과소**(`Table 3` 6/6 예외 없음) · **F4 상관깊이 과다 → 평균 −8 % 인데 SE ×3.1**(1→30 ns; σ_NE 는 −1.8 %·SE 평평) · **F5 GK plateau 눈대중 → GK SE 가 EH SE 의 3.6–8.5×**(`Fig. 5` figure-read: 개별 replica 적분이 **−5~+12 S m⁻¹**, **replica 1개면 음의 σ**) · **F6 좌표계 미명시 → t(Li⁺) 3.5 M 이 +0.373(mass) → +0.168(number) → −0.174(solvent) 로 부호 반전** · **F7 유한크기 → self D +9–10 %(125→1000쌍)·YH 보정 +12–41 %, 그런데 total σ 는 cross 상쇄로 검출 불가** · **F8 분극 힘장 → D +18–21 % 인데 σ_EH 는 안 오름, ionicity 0.702→0.542** = *"단일입자 이동도가 거시 수송으로 번역되지 않는다"*. **★★ Haven**: ionicity `H⁻¹=σ_tot/σ_NE` (Eq. 16) IL **0.542–0.760** / LiFSI **0.480–0.610** ⇒ H_R 1.3–2.1. **🔴 `adeli2019` 우리 계열 실측 H_R 0.23–0.3 과 부호가 반대다**(그쪽은 σ_실측 > σ_NE) ⇒ **"NE 는 과대"를 argyrodite 로 옮기면 안 되고, 결론은 "H_R=1 은 보정이 아니라 미측정이며 오차의 부호조차 우리 계에서 미확정"**. **EH↔GK**: 본문 `Fig. 2` 의 0.7 S m⁻¹ 간극은 **방법 차이가 아니라 다른 궤적 세트**(100 ns vs 0.1 ns) — `Table S23` 에서 **같은 10×100 ps replica** 로 EH 3.220±0.282 vs GK 3.073±0.729 로 일치시킨다(단 이 자백이 초록·결론에 없다). 이상적 비교 궤적은 **900 GB** 라 replica 불가(`Table S22`). **★ 시간원점**: ⛔ **단일 vs 다중 원점의 정량 비교가 이 논문에 없다.** 대신 **오차가중치를 "시간원점에 걸친 MSD 요동"으로 정의**(§2.3.1) ⇒ 원점이 1개면 **오차가중·자동창·χ²_red 를 실행할 재료가 없다**; `Fig. S12` 에서 평균 CMSD 가 τ≳27 ns 에 **하강**(figure-read) = 후반부는 확산영역이 아니라 표본이 마른 영역. **replica 결합**: 역분산 가중평균(Eq. 25–26) + **χ²_red 재조정**(Eq. 27) + 부트스트랩; fit-first/average-first 는 **평균값이 같고 오차막대만 다르다**(*"averaged CMSD 로는 의미 있는 SE 가 안 나온다"*). **⛔ 한계(저자)**: 계 2종·온도 1점·힘장 2종 · *"observed trends should not be interpreted as general trends"* · 크기효과 미결 · 실험 불일치를 힘장 탓으로 · YH 는 *"qualitative approximations"* · **LiFSI 실험 기준값이 내삽(±13 %)** · 순수 IL 수송수는 *"no additional physicochemical meaning"* · **데이터 공개 저장소 없음**. **⛔ 한계(우리 지적)**: ★**실험선이 있는 5개 비교 중 3개에서 NE 가 실험에 더 가깝다**(IL CL&P Δ+0.49 vs EH Δ−1.70 등)인데 저자는 3.5 M 에서만 오차상쇄를 인정 ⇒ 논문 주장은 *"NE 가 부정확"* 이 아니라 ***"NE 는 다른 양을 재는 추정량"*** 으로 읽어야 한다 · **`nslice`·`tol`·`incr` 수치가 논문·SI 어디에도 없다**(＝"사용자 편향 제거" 를 표방하면서 재현 상수 미제공) + 선택 규칙이 **"데이터점 최다"** 라 **길이 최대화 편향 내장** · **자동창이 사실상 초·중기 적합**(1.0 M 창이 깊이의 80 %, `Fig. S12` 파랑선이 τ≳12 ns 부터 평균곡선 위로 이탈) 이고 **CMSD 하강이 통계인지 진짜 sub-diffusion 인지 구분 안 함** · **replica 밀도를 통일**해 밀도 축에서는 오히려 덜 독립 · **써모스탯이 집단 전하전류에 주는 영향 미논의**(전부 Nosé–Hoover ⇒ **우리 Langevin 으로 옮길 때의 경고가 없다**). **🔧 우리 좌표(§12–13)**: ✅ 지지 = `σ 절대값 인용 금지`·`비율도 멀티시드만` · 🔴 직격 = **`tools/doping/run_md_sigma.py:136` `fit_start = n_frames//2` 가 바로 반증된 Tail Fit**(방향만 이식, **2.8× 는 집단 MSD 값이라 우리 self-MSD 로 금지**) · 🔴 **단일 시간원점**(`⟨‖r(t)−r(0)‖²⟩`)이라 오차가중 자체가 불가 · ⚠ **경로마다 창이 다르다** — 이온 캠페인(`run_comp1_seeds.sh`)은 `--fit_window_ps 2 50` 정본, **도핑/σ 경로만 후반절반** ⇒ 한 repo 에 D 정의 2개 · ✅확인 **우리 3-seed 는 같은 `--v0_xyz` + 속도 시드만**(`--n_configs 1 --disorder_levels 0.0`) ⇒ 이 논문의 *distinct initial configurations* 미충족, 오차막대를 낙관치로 읽어야 함 · 🔴 **D_tr 랭킹으로 가면 후보계 원자수 통일이 새 제약**(D 가 크기에 9–10 %). **★★★ Stage 10 판정 = 조건부 지지**: 근거 ① `Fig. 8`·`Fig. 9` 에서 **self 량 SE 가 집단량의 1/10**(σ_NE 는 상관깊이에 −1.8 %·SE 평평 vs σ_EH −8 %·SE ×3.1) ⇒ *"판정 가능한 양으로 랭킹하라"* 에 self 쪽 손 ② ionicity 가 같은 물질계 안에서 **1.4배 범위**로 변동 = `adeli2019` 의 *"Cl 함량 1.34배 변동"* 과 같은 논증을 계산 쪽에서 반복 ⇒ NE-σ 랭킹에 조성 의존 계통편차 ③ 우리 예산은 이 논문 요구의 **1/500(200 ps vs 100 ns)·1/10(replica 1 vs 10)** + 반증된 tail 적합 + 단일 원점. ⚠ **단 이 논문은 σ 를 버리라고 하지 않는다 — σ 를 제대로 내는 도구를 만든 논문이다** ⇒ 인용 문장은 *"NE 가 틀려서"* 가 아니라 ***"우리 예산에서 σ 는 정의된 보고량이 아니고 같은 궤적에서 D_tr 은 정의된다"***. ⛔ **물성 4축(A/B/C/D) 편입 금지** — σ·ESW·탄성·gap 우리 계 값 0건 → `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만. ⛔ **어떤 σ·D 절대값도 이식 금지**(고전 CL&P(ol) 액체) · ⛔ **"replica 10개" 를 규칙화 금지**(저자가 계마다 다르다고 명시) · ⛔ **"권고 깊이 10 %" 를 우리 2–50 ps 창의 근거로 쓰지 말 것**(100 ns 기준 비율) | **방법론(σ/D 추정 통계·적합창·replica·Haven 정의)·Stage 10 σ→D_tr 판정** — 물성값 0, 액체 전용 |
```

**⚠ INDEX 행에 같이 반영할 것**
- 같은 묶음의 자매편 3행(`pranami2015_estimating_error_diffusion_coefficients_md`, `maginn2019_best_practices_transport_selfdiffusivity_viscosity`,
  그리고 UQ 계열)이 들어오면 **상호 참조**를 넣는다. 층위 구분:
  - **pranami2015** = *단일 궤적의 통계적 오류* (선형회귀 가정 위반·독립표본)
  - **maginn2019** = *self-diffusivity·점도의 베스트프랙티스* (이 논문 ref [94])
  - **이 편(zaby2026)** = *집단(collective) σ 로의 확장 + Haven/좌표계/도구*
- ⚠ 이 논문의 ref [26] **Frömbgen 2025** (*ChemPhysChem* 26: e202401048, 같은 그룹의 "Reliable **Dynamic Properties**" 선행편)은
  **자동 창 검출 알고리즘의 실제 정본**이다. **우리 미보유** — 확보 후보로 올린다.
- ⚠ 이 논문의 ref [45] **Kubisiak & Eilmes 2020** (*JPCB* 124, 9680, *"how to invest the computational effort"*)이
  **replica 개수 vs 궤적 길이 트레이드오프**의 정량 원전일 가능성이 높다. **우리 미보유** — 확보 후보.

---

## ② `litdb/comparison_vs_ours.md` — **§J-0 출처표** 에 추가할 줄

```markdown
| **[Zaby26σ]** 🔧 | `zaby2026_reliable_conductivity_estimates_md` — **MD 로 σ 를 낼 때의 통계 원전** (*ChemPhysChem* 2026, 27:e70477, DOI 10.1002/cphc.70477, OA). ⚠ **계가 이온액체·에테르 액체전해질 · 황화물 0회 · 물성값 0** → 아래 **J-7** 에만 등장, A–D 축 금지. ⚠ **NE 오차의 부호가 [Adeli19] 와 반대** — §J-7 의 부호 경고를 반드시 같이 인용 |
```

---

## ③ `litdb/comparison_vs_ours.md` — **§J-7 `🔧 방법 원전`** 에 추가할 블록

```markdown
**[Zaby26σ] `zaby2026_reliable_conductivity_estimates_md` — σ 를 *추정하는 절차* 의 원전**
(*ChemPhysChem* **27**, e70477, 2026 · Zaby/Ingenmey/Lourenço/Zhang/Da Silva/Brehm/**Maginn**/**Kirchner** ·
계 = **[EMIm][DCA] 이온액체 + LiFSI/DME 에테르 전해질** · **황화물·고체전해질 0회 · 온도 1점 · DFT 0회 · 물성값 0**)

> 🔑 **우리가 이 편에서 가져오는 것은 σ 값이 아니라 "σ 를 보고량으로 성립시키는 조건" 이다.**
> 그리고 그 조건 대비 **우리 Stage 10 σ 파이프라인이 어디서 죽는지**의 눈금.

| 항목 | [Zaby26σ] | 우리 (`tools/doping/run_md_sigma.py` · `tools/ionic/run_comp1_seeds.sh`) | 판정 |
|---|---|---|---|
| **σ 의 정의** | **집단**: EH(집단 MSD 기울기) 또는 GK(전하전류 ACF 적분). NE 는 **근사**로만 | **NE 단독**, `σ = n q² D /(k_B T)`, **H_R = 1** | 🔴 **부류가 다르다.** 우리 것은 그들 분류의 `σ_NE` 이고 **cross 항이 0으로 가정돼 있다** |
| **NE 오차의 크기** | ionicity **0.48–0.76** ⇒ NE **1.31–2.08× 과대** (cross 가 self 의 30–52 %) | 미측정 | 🔴 **크기는 이식 금지** (액체 값). 🟡 **"미측정" 이라는 사실만 이식** |
| **NE 오차의 부호** | **과대** (cross < 0) | 미측정 | 🔴🔴 **[Adeli19] 실측 H_R 0.23–0.3 은 반대 부호**(σ_실측 > σ_NE) ⇒ **부호조차 우리 계에서 미확정.** *"NE 라서 과대"* 라고 쓰면 틀린다 |
| **적합창** | 로그기울기 자동 검출(MSDiff v0.2.0). **고정 tail 은 σ 를 1.6–2.8× 낮춘다** (1.0 M: 자동 60 ps–24 ns → 2.03 vs tail 15–30 ns → 0.73 S m⁻¹) | **`fit_start = n_frames//2`**(도핑/σ 경로) / `--fit_window_ps 2 50`(이온 경로) | 🔴 **도핑 경로가 직격.** ⛔ **2.8× 는 집단 MSD 값이라 우리 self-MSD 로 못 옮긴다** — **방향(과소)만**. ⚠ 부수 발견: **한 repo 에 D 정의가 둘** |
| **시간원점** | **다중 원점 + 그 산포를 적합 가중치로** (§2.3.1) | **단일 원점** (`⟨‖r(t)−r(0)‖²⟩`) | 🔴 **정량 페널티는 이 논문에 없다**(원점 스캔 실험 0건). 판정 근거는 구조적 — **ΔMSD(τ) 가 없어 오차가중·자동창·χ²_red 를 실행할 수 없다** |
| **replica 정의** | **새 PACKMOL 박스 10개**(배열+속도 모두 다름, 밀도는 통일) | ✅확인 **동일 `--v0_xyz` + 속도 시드만** (`--n_configs 1 --disorder_levels 0.0`) | 🟡 §2.3.1 의 *"and/or"* 로는 통과하나, `Fig. 7`·`Table 3` 의 **위상공간 피복 논거는 배열 다양성에서 온다** ⇒ 우리 오차막대는 **within-replica 쪽** |
| **replica 수** | **10**. ⛔ 최소치를 처방하지 않음(*"defined independently for every simulated material"*) | **3** (600 K 만) | 🟡 self 량이면 부분 생존 · 🔴 집단 σ 면 부족 |
| **불확실도 산출** | **역분산 가중평균 + χ²_red 재조정**(Eq. 27) + **부트스트랩**. 단일 궤적 분할은 SE 를 **1.33–1.52× 과소**(6/6) | `linregress` 의 SE (점들이 상관 → 무의미) | 🔴 **죽는다.** ⭕ **χ²_red 재조정은 계산 0회로 이식 가능** — 시드 3개 σ_r 만 있으면 된다 |
| **궤적 길이** | EH **100 ns**, GK **0.1 ns + 1 fs 속도 저장**(이상적 비교 궤적 **900 GB**) | **200 ps** | 🔴 **집단 σ 는 우리 자원에서 열지 않는다** (판정) |
| **써모스탯** | Nosé–Hoover 계열(TGNH)만 | **Langevin (friction 0.02)** | ⚠ **이 논문이 다루지 않는 위험.** Langevin 은 운동량 비보존 ⇒ 집단 전하전류에 열욕이 개입한다. **⚠ 우리 가설이지 논문 주장 아님.** self MSD 영향은 훨씬 작다 |
| **셀 크기** | self D **+9–10 %**(125→1000쌍), YH 보정 **+12–41 %**. **total σ 는 cross 상쇄로 검출 불가** | 계마다 원자 수 통일 규약 **없음** | 🔴 **새 제약**: D_tr 랭킹으로 가면 **후보계 원자수를 고정**해야 한다 |
| **좌표계** | σ_tot·self 는 무관(self 는 열역학 극한에서), **cross·수송수는 의존**(t(Li⁺) 부호 반전) | 해당 없음(단일 가동종) | 🟡 우리가 cross 를 재기 시작하면 그때 필요 |
| **온도 의존 / Ea** | **0건** (단일 온도) | 600/800/1000 K Arrhenius | 중립 — **이 논문은 우리 Ea 축에 대해 아무 말도 하지 않는다** |
| **MLIP 검증** | 서론 언급뿐, 실험 0건 | UMA-s-1p1 | 중립 — ⛔ *"MLIP σ 가 검증됐다"* 의 근거로 쓸 수 없다 |

**★★★ Stage 10 판정 (Q10 — σ 를 랭킹 축에서 뺄 것인가)**

> **조건부 지지.** 이 논문은 *"σ 를 쓰지 마라"* 가 아니라 *"σ 는 집단량이라 이만큼의 통계 예산을 요구한다"* 를 말한다.

- **지지 ①** `Fig. 8`·`Fig. 9`: **self 기반 양의 SE 가 집단 양의 1/10.** σ_NE 는 상관깊이 1→30 ns 에서 **−1.8 %·SE 평평**,
  σ_EH 는 **−8 %·SE ×3.1**. self 항은 크기 추세를 **판정할 수 있고** total 은 **판정할 수 없다** ⇒ *"랭킹은 판정 가능한 양으로"*.
- **지지 ②** ionicity 가 **같은 물질계 안에서 1.4배 범위**(IL 0.542–0.760 / LiFSI 0.480–0.610)로 움직인다.
  = **[Adeli19] 의 *"Cl 함량 x=0→0.5 에서 H_R 1.34배 변동"* 과 같은 논증을 계산 쪽에서 반복**한 것.
  ⇒ H_R=1 고정 σ 로 도펀트를 줄 세우면 순위 안에 **미지의 조성 의존 인자**가 들어간다.
  (⚠ 1.4배·1.34배는 각각 그 논문의 계 값 — **논증 구조만** 가져온다.)
- **지지 ③** 우리 예산은 그들 요구의 **1/500(200 ps vs 100 ns) · 1/10(replica 1 vs 10)** 이고,
  게다가 **반증된 tail 적합 + 단일 시간원점**을 쓴다 ⇒ 보고량 규율 언어로 **집계 규칙 없는 스칼라 σ**.
- **반대/중립** — ① 이 논문은 σ 를 **살리려고** 쓴 논문이다 ② **D_tr 도 공짜가 아니다**(크기 9–10 %, YH 12–41 %)
  ⇒ 원자수 통일이라는 새 제약 ③ 재료계가 다르다 — 액체에서는 반대 부호 이온이 함께 움직여 σ 를 깎지만
  argyrodite 에서는 Li–Li 협동 이동이 σ 를 **키울** 수 있다(= [Adeli19] H_R<1).

⇒ **인용 문장은 *"NE 가 틀려서"* 가 아니라 *"우리 계산 예산에서 σ 는 정의된 보고량이 아니고, 같은 궤적에서 D_tr 은 정의된다"*.**

**⛔ [Zaby26σ] 에서 인용하면 안 되는 것**
- **어떤 σ·D 절대값의 이식** — 고전 CL&P(ol) 액체, 353/333 K.
- **"NE 는 σ 를 과대평가한다" 를 argyrodite 에 적용** — [Adeli19] 실측이 **반대 부호**.
- **"2.8× 과소" 를 우리 self-MSD D 에 적용** — 그 수치는 **집단 MSD** 값이다.
- **"replica 10개 필요" 를 규칙화** — 저자가 계마다 다르다고 명시.
- **"권고 상관깊이 10 %" 를 우리 2–50 ps 창의 근거로** — 100 ns 기준 비율이다. 200 ps 에 곱하면 20 ps 인데 그 산술에 물리적 근거가 없다.
- **ionicity 0.48–0.76 을 "액체의 보편값" 으로** — 계 2종·온도 1점.
- **이 편을 "MLIP σ 의 검증" 으로** — MLIP 실험 0건.

**⚠ 우리가 실측한 논문 내부의 미봉합** (digest §16-B): 실험 기준선이 있는 **5개 비교 중 3개에서 NE 가 실험에 더 가깝다**
(IL CL&P Δ+0.49 vs EH Δ−1.70 / IL CL&Pol Δ+1.96 vs Δ−2.08 / LiFSI 3.5 M Δ−0.17 vs Δ−0.54).
저자는 **3.5 M 에서만** 오차상쇄를 인정하고 `Fig. 2` 상단의 같은 현상에는 침묵한다.
⇒ 이 논문의 주장은 **정확도 논증이 아니라 추정량 논증**이다. 그 구분을 흐리고 인용하면 데이터가 안 받쳐준다.
```

---

## ④ (선택) `litdb/inbox/` 확보 후보 2건

| 후보 | 왜 |
|---|---|
| **Frömbgen et al. 2025**, *"Lessons Learned on Obtaining Reliable **Dynamic Properties** for Ionic Liquids"*, *ChemPhysChem* **26**, e202401048 (이 편 ref [26]) | **자동 창 검출(MSDiff) 알고리즘의 실제 정본.** 이 편은 그것을 인용만 하고 상수(`nslice`·`tol`·`incr`)를 안 준다 |
| **Kubisiak & Eilmes 2020**, *"Estimates of Electrical Conductivity from MD Simulations: How to Invest the Computational Effort"*, *J. Phys. Chem. B* **124**, 9680–9689 (이 편 ref [45]) | **replica 개수 vs 궤적 길이 트레이드오프**의 정량 원전 가능성. 이 편이 *"multiple independent replica simulations are required"* 의 근거로 두 번 인용 |

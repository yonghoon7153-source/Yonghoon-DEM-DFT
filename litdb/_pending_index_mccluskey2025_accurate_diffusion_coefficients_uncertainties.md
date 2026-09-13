# ⏸ 병합 대기 — `mccluskey2025_accurate_diffusion_coefficients_uncertainties`
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09 · litdb-curator **6개 동시 실행**으로 `INDEX.md`·`comparison_vs_ours.md` 직접 수정 금지를
> 받아, 넣어야 할 내용을 여기 적어 둔다. 충돌이 풀리면 **아래 두 블록을 그대로 옮기고 이 파일을 지운다.**
>
> ⛔ 이 논문의 물성값은 **LLZO D\* 단 하나**(그것도 시연용)다 → **A/B/C/D 물성 4축 표에 넣지 않는다.**
> `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만 둔다 (shapeev2016 · park2024 · grasselli2025 선례).

---

## ① `INDEX.md` 에 추가할 행

| `papers/mccluskey2025_accurate_diffusion_coefficients_uncertainties.md` | **[외부·methods·★②축(MD 통계 불확실도) 최신 정본 + 코드 실물]** **Andrew R. McCluskey\*** (Bristol · European Spallation Source ERIC DMSC · Diamond Light Source), **Samuel W. Coles** (Bath + Faraday Institution → 현 Cambridge), **Benjamin J. Morgan\*** (Bath + Faraday Institution), "**Accurate Estimation of Diffusion Coefficients and their Uncertainties from Computer Simulation**" (***J. Chem. Theory Comput.* 2025, 21, 79−87**, DOI `10.1021/acs.jctc.4c01249` · CC-BY 4.0 · 접수 2024-09-23 / 수리 2024-12-03 / 공개 2024-12-30 · arXiv 2305.18244; 본문 9 pp · **SI 8 pp(S-I~S-IV)** · Fig 6 + Fig S1–S6 · **DFT 0회**) — **물성 논문이 아니다. "MD 궤적 하나에서 D\* 와 오차막대를 어떻게 내야 맞나" 하나만 판다.** **핵심**: MSD 시간점은 **계열상관 + 이분산** 이라 OLS 의 두 가정이 **둘 다** 깨진다 → OLS 는 (i) 통계적으로 비효율이고 (ii) **자기 오차막대를 한 자릿수 이상 과소평가**한다. 해법 = **자유확산 입자계의 해석적 공분산 Σ′ 을 유도**(SI S-I, `Σ′[xᵢ,xⱼ]=σ²[xᵢ]·N′ᵢ/N′ⱼ`, ∀i≤j)하고 **분산 σ²[xᵢ] 만 궤적에서 재스케일 추정**(식 7, `σ̂²[xᵢ]=σ²[Δrᵢ²]/N′ᵢ`) → **최소고유값법 재조건화**(cond_max 1e16) → **emcee 베이지안 회귀**(32 walkers × 1500, burn 500, thin 10 → **3200 표본**, **improper prior D\*≥0**) ⇒ **궤적 1개로 GLS(Cramér–Rao) 급**. **★★ N′ᵢ 의 정의가 이 논문의 심장**: **겹치지 않는** 시간창 수 × 입자 수 = **N_atoms × N_t/i** — 총 관측 수 N_atoms×(N_t−i) 로 나누면 **독립성을 과대계상**한다(`Fig. S1` 도식). **검증**: ① 3D 격자 RW(128입자×128스텝, jump=√6→D\*=1, **4096회**) ② **c-LLZO**(**고전 MD** — METALWALLS + **DIPPIM 분극이온 힘장**, 2×2×2 = 1536원자·Li 448, **NVT 700 K, 6 ns, dt 0.5 fs**, Nosé–Hoover τ=121 fs → **192 유효궤적**(500 ps × 28 Li 무작위 비복원), **확산영역 시작 10 ps**). **수치**(전부 소환값): `Fig. 1` RW — σ_OLS≈0.078 / σ_WLS≈0.042 / σ_GLS≈0.020(figure-read), **σ_OLS/σ_GLS≈3.9(분산 15배)**, **OLS 는 자기 σ 를 ≈1/16 로 보고**; `Fig. S6` **실제계 LLZO** — σ_OLS≈0.14e-5 / σ_GLS≈0.031e-5 cm²/s, **비 4.6(분산 21배)**, OLS 자기오차 **≈1/9–1/10**, **세 방법의 중심값은 동일**(⇒ **OLS 는 D 자체를 편향시키지 않는다. 편향은 오차막대에만 있다**); `Fig. 5` LLZO D\*(700 K)**≈0.9e-5 cm²/s**·σ≈5–6 %; `Fig. 4`c 우리 방법이 이론최적보다 **≈17 % 넓음**, `Fig. 4`d·`Fig. 5`b **σ̂² 가 1.45–2배 과대**(=**보수적, SI 가 의도적 선택이라 명시**: *"overestimation … always preferable to underestimation"*). **🔴 `Fig. 6`b 가 제일 무섭다**: N_atoms 를 늘리면 네 방법 모두 σ²∝1/N 로 **평행**하게 좋아지는데(패널 a), **궤적을 길게 늘리면 OLS 만 평평하다**(기울기≈0; WLS≈−0.5, kinisi/GLS≈−1.1) — t_max=1024 에서 **kinisi 가 OLS 보다 σ² 250배 낮다**(figure-read) ⇒ *"오래 돌렸으니 통계가 좋아졌다"* 가 OLS 에선 성립 안 함. **SI S-II**: **Flyvbjerg–Petersen 블록 재규격화(pyblock)와 정면 비교 → 기각** — 블록법은 잡음 크고(`Fig. S3`e 산포) **체계적으로 과소**(하한 추정기라, 식 S-35), 재스케일은 매끄럽고 **과대(안전)** ⇒ **[Kahle20] 의 "블록 분산 오차"에 대한 정면 반론**. **★★★ 코드 실물 확보 — clone 성공** `github.com/arm61/msd-errors`(**MIT**/CC BY-SA 4.0, showyourwork ESI, 55파일; ⛔ `src/data/` 는 gitignore 라 **데이터 없음**, LLZO 궤적은 Zenodo `10.5281/zenodo.10532134`). **추정기 본체는 ESI 가 아니라 PyPI `kinisi==1.1.0`**: `kinisi/diffusion.py::Bootstrap.bootstrap_GLS()`(L305) · `generate_covariance_matrix()`(L397) · `_populate_covariance_matrix()`(L838, 식 6 그대로) · `minimum_eigenvalue_method()`(L870)+statsmodels `cov_nearest` · N′ᵢ 는 `kinisi/parser.py::Parser.get_disps()`(L170–221). **진입점 `DiffusionAnalyzer.from_ase`** ⇒ **우리 extxyz 궤적을 그대로 먹는다**(실측: 1001프레임/48 Li/200 ps → **5.2 초** 완주, D̂ 참값 1σ 안). **`dtype='identical'`** 이 **복제 시드 N′ᵢ 합산**을 이미 구현(= 우리 3-seed). 의존성 **가볍다**(numpy/scipy/statsmodels/sklearn/emcee/**uravu**/dynesty/tqdm; **pymatgen·ASE·MDAnalysis 불필요**). `kinisi/arrhenius.py` 가 **D 분포 → Ea 분포 + `extrapolate(T)` + Arrhenius vs super-Arrhenius 베이지안 evidence**까지 제공. **🔴 이식 차단요소 2건 실측**: ① **numpy≥2 에서 파서 즉사** (`parser.py:193 np.product` — NumPy 2.0 제거됨; `environment.yml` 은 numpy=1.26.4 로 고정. 해법: `numpy<2` 격리 venv 또는 `np.product=np.prod` 심기 — 둘 다 통과 확인) ② **`sampling='single-origin'` 이 잘못 색인된다** (`parser.py` L202-203 이 변위를 **루프 카운터 `i`** 로 가져오는데 가로축은 `time_intervals[i]` — 실측: 501프레임/n_steps=100 에서 **D 가 0.160×**(≈1/5), n_steps=500 으로 맞추면 0.871× 로 복구) ⚠ **우리 정본 MSD 가 바로 single-origin 이라 "규약 맞추기"로 이 옵션을 켜면 D 가 조용히 5배 틀린다**. **⛔ 용어 함정 3개**: (a) **"부트스트랩"이 아니다** — 본문에 그 단어가 0회, 클래스명 `MSDBootstrap`·`bootstrap_GLS` 는 **레거시 작명**이고 기본값 `bootstrap=False`(리샘플링 없음). 올바른 이름 = **근사 베이지안 회귀(≈GLS)** (b) **"AIMD/DFT"가 아니다** — LLZO 는 고전 MD (c) `Fig. 6`b 의 t_max 는 **총 시뮬 길이**이지 적합 창 상한이 아니다. **🔴 저자가 안 하는 것**: **비(ratio)·차이의 오차 전파 0**(*"ratio"* 는 `Fig. 3` 캡션 1회뿐) · σ(이온전도도)/Haven 0 · **`start_dt` 선택 규율·감도 0**(*"set by the user"* 로 끝) · **적합 창 상한 논의 0** · `cond_max` 민감도 0 · MLIP 모델오차 범위 밖 · **검증계 2개가 둘 다 Σ′ 가정에 유리**(격자 RW = 가정 그 자체 / LLZO = 700 K 초이온, 얕은 cage) ⇒ **느리고 caged 한 계(우리 LPSOCl 600 K, 절편이 MSD@50 의 18.2 %)에서 Σ′ 타당성은 미검증**. **★ digest 계산 4건**(우리 궤적 모양 200 ps·0.2 ps 덤프·48 Li 합성 브라운걸음 40회 반복, ⚠ **kinisi 가정 그 자체라 kinisi 에 유리**): ①**우리 실제 파이프라인(single-origin MSD + OLS 2–50 ps) 진짜 산포 14.8 %, 보고 stderr 0.63 % → 23배 과소**, 편향은 없음 ②**손실 분해 = 시간원점평균 8.7× × 추정기 10.0× = 87×**(두 축을 각각 고정해 잰 뒤 곱이 전체와 일치함을 확인) ⇒ **우리 D 한 점 = kinisi 한 점의 1/87**(N=48 조건, 한 자릿수로만 읽기) ⇒ **시드 3개는 kinisi 1회의 1/29**, **multi-origin 만 켜도 87→10** ③**2–50 ps 창은 정당** — 같은 200 ps 궤적에서 kinisi 2–50 진짜 sd 1.63e-7 vs 2–200 1.77e-7 로 **±11 % 해상도 안에서 구별 불가**(정보는 궤적 길이에 있지 긴 lag 점에 있지 않다) ④**비 전파 검증** — 참 비 1.60, 12쌍: 사후표본 나눗셈 sd 3.6 % vs 진짜 2.79 %(보수적 1.29×), **제곱합 검산 1.88 %⊕2.28 %=2.96 % ≈ 관측 2.79 %** ⇒ **`(σ_rel[D_rel])² = (σ_rel[des])² + (σ_rel[host])²` 확인**. **그림 12장 중 8장 실제 열람**(`Fig. 1`·`2`·`3`·`4`·`5`·`6`·`S3`·`S6`; 안 본 것 = `S1`·`S2` 도식 + `S4`·`S5` 보조검증). **🔧 도구 결함 1건 보고**: `tools/litdb/extract_figures.py` 의 `CAP_RE` 가 라벨을 `S?\d+` 로 잡아 REVTeX 식 **`FIG. S-1.`(하이픈)** 을 못 잡는다 → 이 SI 에서 0장 (동시 실행 충돌 우려로 **공용 도구는 안 고치고** 스크래치로 S1–S6 크로핑 후 `figures.json` 병합; `S?-?\d+` + `S-1→S1` 정규화면 해결). **⚠ SI 2개는 같은 문서** — 텍스트 대조 결과 `Sup`/`Sup2` 는 **ACS 다운로드 워터마크 한 줄만 다르고 내용 동일**(둘 다 8쪽) ⇒ 실질 SI 1개. **⛔ 물성 4축 편입 금지** → `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만. 🎤 talk 역링크 **해당 없음**(`talks/lee2026_skku_mlip_materials_design.md` 인입 대기열에 이 논문 없음). | **방법론(MD 통계 추정기)·②축 정본 + 코드 이식 경로** — 물성값 LLZO D\* 1건뿐, 아르지로다이트 0회 |

---

## ② `comparison_vs_ours.md` §J-7 `🔧 방법 원전` 에 추가할 블록

**[McC25D] `mccluskey2025_accurate_diffusion_coefficients_uncertainties` — D\* 추정기·오차막대의 정의 원본 (코드 실물 확보)**
(⛔ 물성값 LLZO D\* 1건뿐. A–D 4축 행 금지. 아래는 **절차**와 **우리 위치 판정**뿐이다.)

| 항목 | [McC25D] 가 정하는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **적합 모델** | 직선 + **자유 절편** (`fit_intercept=True` 기본) | 직선 + **자유 절편** | ✅ **일치** |
| **회귀** | **근사 베이지안(≈GLS)**, Σ′ 사용 | **OLS** | 🔴 **핵심 격차** |
| **D 값의 편향** | OLS/WLS/GLS **중심값 동일** (`Fig. 1`·`Fig. S6`) | — | ✅ **우리 D 는 안 틀린다.** ⛔ *"우리 D 가 과대/과소"* 서술 금지 |
| **OLS 오차막대** | 자기 σ 를 **1/9–1/26** 로 보고 | 우리는 `stderr` 를 **안 쓴다** — 오차막대는 **시드 3개 산포** | ✅ **관행은 무사.** 시드 산포 = 논문이 *"정직하지만 비싸다"* 고 부른 그 방법 |
| **정밀도(효율)** | GLS 가 OLS 보다 σ 3.9–4.6배 좁음 | — | 🔴 **여기서 진다** (아래 두 행) |
| **MSD 시간원점** | **multi-origin 기본** (모든 원점 평균) | **single-origin** (정본 `msd_per_elem_A2`, `aimd_mlip.py::compute_msd_per_element`) | 🔴 **분산 8.7× 손실**(digest 계산). **MD 0 스텝으로 회수 가능** — `msd_multi_origin` 이 이미 있다 |
| **N′ᵢ (독립 관측 수)** | **겹치지 않는** 창 수 × 입자 수 = **N_atoms·N_t/i** | `msd_multi_origin` 이 저장하는 `norig = nt−L` = **겹치는 원점 수** | ⚠ **가중에 쓰면 짧은 lag 에서 독립성 최대 L배 과대계상.** 지금은 가중에 안 쓰므로 사고는 없다 — **쓰기 전에 고쳐라** |
| **총 손실** | — | (single-origin + OLS) | 🔴 **var 비 87×** ⇒ **우리 D 한 점 = kinisi 한 점의 1/87** (digest 계산, N=48 합성. **한 자릿수로만**) |
| **시드 수 — 정밀도** | 궤적 1개로 충분 | **3** | 🔴 **kinisi 1회의 1/29.** multi-origin 만 켜도 3 → *10 상당*. **정밀도 목적의 시드 증설은 가장 비싼 길** |
| **시드 수 — 추정** | 다루지 않음 | **3** | 🔴 [Gra25UQ] 식 (27) 이 **M≥4** 요구 + 3개의 sd 는 상대오차 **50 %** ⇒ `Ea 0.197±0.032` 의 `±0.032` 는 **±50 % 짜리 숫자**. **3 → 5 권고**(정밀도가 아니라 추정 때문) |
| **적합 창 하한** | LLZO **10 ps** (ballistic·subdiffusive 제거). **선택 규율은 안 준다** | **2 ps** | ⚠ **근거 약함.** `Fig. 3` 이 **i,j ≲ 5–10 에서 Σ′ 이 분산을 2배 이상 과대**함을 보인다 = 우리 하한이 그 구역. 우리 LPSOCl 600 K 절편은 **MSD@50 의 18.2 %** 인데 이 모델은 **절편 없는 자유확산** 전제 ⇒ **`start_dt` 2/5/10 ps 스캔 필요** |
| **적합 창 상한** | **없음**(궤적 끝까지). 논의도 없음 | **50 ps** | ✅ **정당하다 (우리가 메운 공백).** digest 계산: 같은 200 ps 궤적에서 kinisi 2–50 sd 1.63e-7 vs 2–200 1.77e-7 → **±11 % 안에서 구별 불가.** 단 **보고 σ̂ 는 좁은 창에서 더 보수적**(3.05× vs 1.46×) |
| **창 고정 규율** | *"set by the user"* — **규율 없음** | **전 계·전 온도 2–50 ps 고정** | ✅ **우리가 낫다.** [Kahle20] 의 물질별 custom 이 본문↔SI 불일치를 낳은 선례 |
| **분산 추정법** | **재스케일 채택 / 블록 재규격화 기각** (SI S-II: 블록은 잡음↑·**체계적 과소**) | (해당 없음 — 우리는 분산을 안 낸다) | 🔵 **[Kahle20] 이식 후보 강등**: 우리가 적어둔 *"블록 수 4/8/16 감도 점검"* 은 **애초에 열등한 추정기의 감도**를 재는 일 |
| **복제 궤적 합치기** | `dtype='identical'` → **N′ᵢ 합산** | 시드별 개별 적합 후 산포 | 🔵 **둘 다 내라.** 합산 = 정밀도, 산포 = 통계오차 추정. **서로 다른 것** |
| **Arrhenius** | `kinisi.arrhenius` — **D 분포 → Ea 분포**, `extrapolate(T)`, Arrhenius vs super-Arrhenius **베이지안 evidence** | 600/800/1000 K **3점 선형회귀** | 🔵 **이식 후보 1순위.** [Kahle20] 의 *"Bayesian Ea 오차"* 와 같은 방향이고 **여기엔 코드가 있다** |
| **σ(이온전도도)** | **안 한다** (D\* 만) | NE(Haven=1), **절대값 비인용** | ✅ **정신 일치.** ⚠ σ 로 넘어가면 Haven 계통오차가 통계오차를 압도 → **비인용 규율 그대로 유효** |
| **비(ratio) 전파** | 🔴 **안 다룬다** (*"ratio"* 는 `Fig. 3` 캡션 1회) | **보고량이 `D_rel`** | 🔴 **우리가 붙여야 한다.** ↓ 아래 별도 블록 |
| **불확실도 축** | [Gra25UQ] 분류의 **④ 표집/통계만** | `D_rel` 오차막대 | ⚠ **축 명시 필수.** ⛔ *"kinisi 썼으니 우리 D 가 믿을 만하다"* 는 오용 — **궤적이 옳다는 전제 위의 통계**다 |
| **이식 가능성** | MIT · pip · **from_ase** · numpy<2 · 5.2 s/궤적 | 기존 궤적 파일 존재 | ✅ **MD 0 스텝으로 즉시 가능.** 차단요소 2건은 회피법 확인됨 |

**★ 비(ratio) 전파 — 논문이 안 주므로 우리가 정의한다 (digest 계산으로 검증)**

design 과 host 는 **다른 궤적 = 독립** ⇒ 1차 전파는 **상대 표준편차의 제곱합**:
> **(σ[D_rel]/D_rel)² = (σ[D\*_des]/D\*_des)² + (σ[D\*_host]/D\*_host)²**

더 나은 방법 = **사후표본 나눗셈**(kinisi 가 D 를 3200 표본으로 준다. 각각 무작위 치환 후
원소별 나눗셈 → 비의 사후분포. 정규근사 불필요, 비대칭 꼬리 보존).

검증 (참 비 1.60, 독립 궤적쌍 12회, digest 계산):

| 항목 | 값 |
|---|---|
| 평균 r̂ | 1.6091 (편향 **+0.57 %**) |
| 진짜 산포 sd(r̂) | **0.0449 (2.79 %)** |
| 표본나눗셈 사후 sd | 0.0580 (3.6 %) → 보고/진짜 **1.29**(보수적, ±0.27) |
| 제곱합 검산 | 1.88 % ⊕ 2.28 % = **2.96 %** vs 관측 **2.79 %** ✅ |

**우리가 추가로 붙여야 할 것**
1. **`P(D_rel > 1)` 을 사후분포에서 직접 보고** — 비준 판정이 "1보다 큰가"이므로 이게 가장 정직한 보고량
2. **cell-conditioned 유지** — 같은 무질서 배열 안에서만 비를 만든다
3. **모델오차 축은 분리 표기** — `force_contrast` 를 이 σ 와 **합치지 마라**(다른 축, 상관 구조 미지)
4. **Arrhenius 는 `StandardArrhenius` 에 D 분포를 넘긴다**
5. ⚠ **σ(NE) 로 가면 이 오차막대는 무의미** — Haven=1 계통오차 지배

**⛔ [McC25D] 에서 인용하면 안 되는 것**
1. **LLZO D\* ≈0.9×10⁻⁵ cm²/s 를 우리 값과 나란히** — 다른 물질·다른 T(700 K)·**고전 힘장**(DIPPIM)이다.
2. **"부트스트랩"** — 논문에 그 단어가 0회. `MSDBootstrap` 은 레거시 작명이고 기본값은 리샘플링 없음.
3. **"AIMD/DFT"** — LLZO 는 **고전 MD**(METALWALLS+DIPPIM). 이 논문에 DFT 는 한 줄도 없다.
4. **`Fig. 6` 의 WLS/GLS 선을 "실무 성능"으로** — 512회 반복의 **수치 분산/공분산**을 쓴 **이상적 참조선**이다.
   실무 비교는 **OLS vs kinisi(초록)** 만 정당하다.
5. **σ̂/σ ≈1 을 우리 계에 그대로** — 검증계 2개가 **둘 다 Σ′ 가정에 유리**(격자 RW=가정 그 자체,
   LLZO=700 K 얕은 cage). **caged·느린 계 미검증.**
6. **digest 계산의 87× 를 "우리 실측"으로** — **합성 브라운 걸음** 값이다. 실제 cage 상관에서는
   multi-origin 이득(8.7×)이 줄 수 있다. **"수십 배"가 안전한 서술.**

---

## ③ 병합자에게 남기는 메모

- **PDF 를 `litdb/inbox/` 로 옮기지 못했다** (쓰기 범위 제한). 원본:
  - 본문 `/root/.claude/uploads/82ea256b-12bc-5a75-994e-7718d79c71ba/a21a6645-84._Accurate_Estimation_of_Diffusion_Coefficients_and_their_Uncertainties_from_Computer_Simulation.pdf`
  - SI `/root/.claude/uploads/82ea256b-12bc-5a75-994e-7718d79c71ba/2219d416-84._Sup_…pdf`
  - ⚠ `f5da9ebf-84._Sup2_…pdf` 는 **위 SI 와 같은 문서**(ACS 워터마크만 다름) — 등록 불필요.
  → 그림 재추출을 하려면 본문+`Sup` 두 개를 `litdb/inbox/` 에 넣고 `pdf_map.tsv` 에 등록.
    (`litdb/figures/_sources.json` 에는 업로드 경로 기준으로 이미 색인됐다.)
- **`litdb/figures/<slug>/` 는 완성**: 본문 `fig_1..6.png` (공용 도구) + SI `fig_S1..S6.png`
  (스크래치 크로핑, `figures.json` 에 `source_si: true` 로 병합).
- **`tools/litdb/extract_figures.py` 를 고치지 않았다** (동시 실행 6개 충돌 회피).
  고칠 것: `CAP_RE` 의 `(?P<label>S?\d+)` → `S?-?\d+` + `S-1 → S1` 정규화. 그러면 REVTeX SI
  (`FIG. S-1.`) 가 자동으로 잡힌다. **이 논문 SI 에서 0장이 나온 게 실측 증거다.**
- **`db/` 는 건드리지 않았다.** §7-C 의 판정(`multi-origin 정본 승격`, `시드 3→5`)은
  **보고량 카드 + `db/governance/decisions.json` proposed** 로 올려야 하는 사안이지
  curator 가 할 일이 아니다.
- **🎤 talk 역링크 없음** — `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` →
  `talks/lee2026_skku_mlip_materials_design.md` 하나뿐이고, 그 대기열에 이 논문은 **없다**.
- **교차참조 2건을 digest §13 에 박아 뒀다**: `kahle2020_ht_aimd_screening`(블록 오차 ↔ 재스케일
  정면 충돌 / 창 검증은 Kahle 이 우위) · `grasselli2025_uncertainty_era_ml_atomistic`
  (**축 분류**: McCluskey 는 ④ 표집/통계만. Grasselli 가 *"수송계수 전파는 rigorous theory
  부재, 멀티궤적 brute-force 뿐"* 이라 한 자리에 McCluskey 가 단일궤적 해법을 놓는다 —
  **단 ④ 안에서만**). 병합 시 그 두 digest 에도 역링크 한 줄씩 넣으면 좋다.
- **재현 자산**(이 세션에서 만든 것, repo 밖):
  - clone `~/msd-errors-check` · venv `/tmp/kinisi_env` (kinisi 1.1.0 + ase)
  - 실험 스크립트 `/tmp/kinisi_run/{rw_bench,ase_path2,ours_vs_kinisi,origin_split,ratio_demo,so_bug}.py`
  - ⚠ 임시 경로다. 이식을 진행하기로 하면 **`tools/ionic/msd_diffusive_check.py` 에 `--kinisi`
    플래그로 흡수**하는 게 코드 규율에 맞다 (새 파일 금지 사다리).

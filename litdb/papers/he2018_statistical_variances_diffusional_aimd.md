# Statistical variances of diffusional properties from ab initio molecular dynamics simulations — He, Zhu, Epstein & Mo (npj Comput. Mater. 2018)

> slug `he2018_statistical_variances_diffusional_aimd` · DOI `10.1038/s41524-018-0074-y` · type `methods (MD 통계·적합절차 원전) + 코드 실물` · PDF `2. npjCompMater_2018_He_Mo_…_MAIN.pdf` (+SI `2. Sup) …_SI.docx`) · digested `2026-09-22` · status ✅
> **저자**: **Xingfeng He**¹, **Yizhou Zhu**¹, **Alexander Epstein**¹, **Yifei Mo\***^{1,2} (¹University of Maryland, College Park — Dept. of Materials Science and Engineering · ²Maryland Energy Innovation Institute) · 교신 `yfmo@umd.edu` · ***npj Computational Materials* 4, 18 (2018)** · **OPEN / CC BY 4.0** · 접수 2017-11-05 / 개정 2018-03-09 / 수락 2018-03-16 · 본문 9 pp (`Fig. 1`–`Fig. 6` + `Table 1`, refs 56) · SI = Supplementary Note 1–3 + `Fig. S1`–`Fig. S5` + `Table S1` · 지원 ONR + NSF 1550423 · 계산 UMD / MARCC / XSEDE DMR150038

> elements: Li, La, Zr, O, Ti, Al, P, Ge, S, Ag, Rb, I
> methods: DFT, AIMD, MD

---

## 0. 이 digest 를 읽는 법 — **우리 MD 규약의 빠진 앵커였다**

우리 `CLAUDE.md` 는 이렇게 못박고 있다: *MSD 창 2–50 ps 고정 · 자유절편 D · 아레니우스 600/800/1000 K
3점 · Nernst–Einstein(Haven=1) · σ 절대값 인용 금지 · Ea 오차막대는 600 K 3-시드.*
그런데 **이 규약들의 외부 근거가 없었다.** `kb/concepts/beta-gate.md` §7-5 가 *"He 2018 원문 확보 ⏳"* 로
81일째 걸려 있었고(`db/external/PENDING.md` **P3**, 프록시 403), `deklerk2018` digest 는
*"저온 D\* 과대평가는 ref 21(He 2018)에 위임"* 이라고만 적었다. **이 digest 가 그 공백을 닫는다.**

이 논문은 물성 논문이 **아니다.** 다루는 물성값은 LATP/LGPS/LLZO 의 Ea·σ 뿐이고,
아르지로다이트는 **0회**다. 판매하는 것은 **절차와 하나의 식**이다:

1. **MSD–Δt 곡선의 어디를 적합할 것인가** — 아래쪽 탄도(ballistic)·위쪽 저통계 구간을 잘라내는 규칙.
2. **D 의 통계 분산은 무엇이 정하는가** — 적합의 R² 가 **아니라** 관측된 **유효 홉 수 N_eff** 다.
   `RSD(D) = 3.43/√N_eff + 0.04`.
3. **AIMD 로 아예 잴 수 없는 재료·온도 영역은 어디인가.**

⭐ **우리에게 제일 큰 소득은 2번이다.** 지금 우리는 **600 K 3-시드에서만** Ea 오차막대가 나오고
나머지는 맨몸이다. 이 식은 **닫힌 형태**라서 시드를 더 안 돌리고도 오차막대를 붙일 수 있다 —
그리고 §7-D 에서 **우리 실데이터로 검증했다** (modelc 62원자 200 ps: He 식 σ(Ea) = 0.0342 eV vs
우리 3-시드 실측 ±0.032 eV — **7 % 안에서 일치**).

> ⚠ **소환값 규율**: 아래 LATP/LGPS/LLZO/RbAg₄I₅ 수치는 전부 이 논문 값이다. 우리
> `db/properties/` 절대값과 같은 표에 놓지 않는다. 이식하는 것은 **숫자가 아니라 절차와 식**이다.
> 내가 우리 데이터에 적용해 얻은 값은 전부 **(우리 유도, 논문 미보고)** 로 표시했다.

> ⭐ **코드 실물 확보** — `github.com/mogroupumd/aimd` commit `6616528cb4cde0a92c3336b2f109a1160e1eb271`
> (2018-07-06, MIT). `aimd/diffusion.py` 582줄 · `aimd/script/analyze_aimd.py` 325줄 · tests 2개.
> **논문의 식과 코드가 어긋나는 곳이 여러 군데 있고**(§6-F), **README 가 테스트 데이터의 계를
> 잘못 적고 있다**(§6-G). 코드에서 읽은 것은 전부 `코드 실측` + 파일:줄번호로 표시했다.

🎤 **관련 발표 없음** — `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 인입 대기열
(6건)에 이 논문은 없다. 역링크 대상 아님.

---

## 1. 한 줄 요약

**AIMD 로 뽑은 확산계수의 오차는 "직선이 얼마나 잘 맞았나"(R²)가 아니라 "이온이 실제로 몇 번
뛰었나"(N_eff = max TMSD/a²)가 정하고, 그 관계는 `RSD = 3.43/√N_eff + 0.04` 라는 한 줄짜리
경험식으로 쓸 수 있다 — 그리고 제대로 창을 잘랐다면 R² 는 항상 1에 가까워서 애초에 아무것도 말해주지 않는다.**

---

## 2. 메타 / 동기 — 저자들이 세운 세 문제

Mo 그룹은 2012년 LGPS AIMD 로 이 분야를 열었고(ref 5 = Mo/Ong/Ceder, *Chem. Mater.* **24**, 15),
그 뒤 AIMD 가 초이온전도체 표준 기법이 됐다. 이 논문은 그 **6년 뒤의 자기점검**이다.
서론이 세는 문제 셋(축자):

> (1) How shall one properly extract diffusional properties from the dynamics of atoms with **minimal error**?
> (2) How shall one **quantify the statistical variances** of diffusional properties extracted from AIMD?
> (3) What are the **accessible ranges** of materials properties and physical conditions for typical AIMD?

배경으로 든 세 가지 관행적 결함:

| # | 관행 | 저자들의 지적 |
|---|---|---|
| ① | **적합 파라미터를 각 연구가 알아서 고른다** | *"every study chooses their own tested parameters, but the choice has not been discussed"* — 그 선택이 D 를 유의하게 바꾼다 |
| ② | **오차막대를 Einstein 적합의 R² 로 준다** | R² 는 **진짜 분산을 담지 않는다.** 창을 제대로 자르면 R² 는 언제나 ≈1 이 된다 (`Fig. 3` 이 근거) |
| ③ | **몇 번의 홉·MSD 수 Å² 로 D 를 낸다** | *"The diffusion properties from such poor sampling of ion hops may have low statistical significance"* |

선행 오차이론(단일입자추적 refs 29–32 · 고전 MD ref 33 Chitra & Yashonath · kMC ref 34 Leetmaa)은
**이벤트 수가 훨씬 많은 계**를 전제해 AIMD 에 그대로 못 쓴다는 것이 이 논문의 틈새다.

**⚠ AIMD vs NEB 에 대한 이 논문의 입장** (서론): NEB 는 *"경로를 입력으로 요구하고 그 경로는 대개
연구자의 추측"* 이라 초이온전도체처럼 이동이온 부격자가 무질서한 계에서는 위험하고, 실제로
thio-LISICON·가넷의 **협동(concerted) 이동**은 AIMD 가 발견했지 NEB 가 아니다(refs 9, 24–26).
⇒ **우리 소셀 NEB 마감(0/9, 2026-09-19)이 MD 로 갈아탄 것과 정확히 같은 논리다.**

---

## 3. 핵심 수치 (전부 소환값)

### 3-A. 최종 산출 — `Table 1` (본문 PDF 텍스트 전사, 표 이미지 미판독)

| Composition | Ea (eV) | σ at 300 K (mS cm⁻¹) | 오차범위 [σ_min, σ_max] (mS cm⁻¹) |
|---|---|---|---|
| Li₁.₃₃Ti₁.₆₇Al₀.₃₃(PO₄)₃ (**LATP**) | **0.25 ± 0.02** | **1.2** | [0.5, 2.5] |
| Li₁₀GeP₂S₁₂ (**LGPS**) | **0.21 ± 0.01** | **14.2** | [8.1, 25.0] |
| Li₇La₃Zr₂O₁₂ (**LLZO**) | **0.26 ± 0.02** | **1.1** | [0.5, 2.1] |

- 세 계 모두 **Ea 표준편차 ≈ 0.02 eV**.
- **300 K 외삽 σ 의 오차범위는 1–2 자릿수** — LATP 는 0.5→2.5 (5배 span).
- ⚠ 외삽은 *"해당 온도에서 상전이 등으로 아레니우스 기울기가 바뀌지 않는다"* 를 가정한다고 본문이 명시.

### 3-B. `Table S1` — **점을 빼면 어떻게 되나** (LGPS, `Fig. S5`)

| 아레니우스 적합 | Ea (eV) | σ(300 K) (mS cm⁻¹) | 오차범위 |
|---|---|---|---|
| (a) `Fig. 6` 과 같은 전체 데이터 | **0.21 ± 0.01** | **14.2** | [8.1, 25.0] |
| (b) **600 K · 650 K 제거** | **0.26 ± 0.02** | **3.7** | [1.7, 7.9] |
| (c) **625 K · 700 K 제거** | **0.20 ± 0.01** | **23.6** | [12.8, 43.6] |

🔴 **같은 궤적에서 점 2개를 빼는 것만으로 Ea 가 0.20 ↔ 0.26 eV (60 meV) 를 오가고
σ(300 K) 는 3.7 ↔ 23.6 mS/cm — 6.4배** 움직인다.
⇒ **우리 3점 아레니우스에 직접 겨눠진 경고다** (§7-F).

### 3-C. `RSD = 3.43/√N_eff + 0.04` 환산표 (a = 3 Å 가정, 본문 축자 + 내 재현)

| N_eff | max(TMSD) (Å²) | RSD(D) = RSD(σ) | 출처 |
|---|---|---|---|
| 50 | 450 | **52 %** | 본문 |
| 100 | 900 | **38 %** | 본문 |
| 150 | 1350 | **32 %** | 본문 |
| 200 | 1800 | **28 %** | 본문 |
| ~460 | ~4150 | **20 %** | 본문 |
| ~3200 | ~30,000 | **10 %** | 본문 |

✅ 여섯 줄 전부 식 (8)(9)로 **재현 확인** (내 계산: 52.5 / 38.3 / 32.0 / 28.3 / 20.0 / 10.1 %).
⚠ **TMSD 와 MSD 를 헷갈리면 안 된다** — 본문이 굳이 경고한다:
*"Neff and TMSD are from **all mobile ions**, while only MSD per ion is often presented in the literature."*

### 3-D. AIMD 가 닿을 수 있는 영역 (§Accessible range)

전제 모델: **t_tot = 1 ns · V = 1000 Å³ · N = 20 이동이온 · a = 3 Å.**

| 목표 | 필요조건 | 환산 |
|---|---|---|
| RSD < **50 %** | N_eff > **55** | σ > **0.025 S/cm @ 600 K** ⇒ D ≈ **4.2×10⁻⁷ cm²/s** |
| RSD ≈ **20 %** | max(TMSD) ≈ **4150 Å²** | D ≳ **3×10⁻⁶ cm²/s** |
| 일반 하한 | N_eff > 50 | **D_min ≈ 10⁻⁷ cm²/s** (1 nm³ · 1 ns 급 AIMD) |
| 더 정확한 D | — | **D ≈ 10⁻⁵ cm²/s** 급이면 좋다 |

RSD ≈ 20 % 를 얻기 위한 **최저 온도** (`Fig. 5` 판독 + 본문):

| Ea | 필요 T |
|---|---|
| **0.2 eV** | **> 450 K** |
| **0.3 eV** | **> 700 K** |
| **0.5 eV** | **> 1150 K** |
| **0.6 eV** (일부 양극재) | **900 K 미만에서는 홉이 모자란다** |
| **≤ 0.20 eV** (초이온전도체) | **300 K 까지도 가능** |

### 3-E. SI Note 3 — **짧은 런이 얼마나 속이나** (LLZO, `Fig. S4`)

같은 LLZO 를 **40 ps 짜리 AIMD** 로만 돌렸을 때 (본문 `Fig. 6` 은 충분히 긴 런):

| 양 | 40 ps 짧은 런 | 긴 런 (`Table 1`) | 차이 |
|---|---|---|---|
| Ea | **0.19 ± 0.07 eV** | 0.26 ± 0.02 eV | **−0.07 eV, 오차막대 3.5배** |
| σ(300 K) | **6.7 mS/cm**, [0.4, **104**] | 1.1 mS/cm, [0.5, 2.1] | **6배 과대**, 상한 **50배** |

원인을 SI 가 명시: *"the large errors in D at low temperatures (<800 K) are expected, since the
**maximum MSD is comparable to the recommended lower fitting bound (~0.5a²)**"* — 즉
**창 아래쪽이 곡선 전체를 먹어버려** D 가 부풀고, 저온이 부풀면 기울기가 눕고 Ea 가 내려가고
300 K 외삽이 폭발한다.
🔴 **`Fig. S5`/`Table S1` 과 합치면 결론은 하나다: 저온 점이 짧으면 Ea 가 내려가고 RT σ 가 뜬다.**

---

## 4. 방법 ★ — 식 (1)–(10) 과 계산 설정

### 4-A. 식 전개

| 식 | 내용 | 주의 |
|---|---|---|
| (1) | `Δr_i(Δt) = r_i(t₂) − r_i(t₁)`, `Δt = t₂ − t₁` | |
| **(2)** | `TMSD(Δt) = Σ_i ⟨\|r_i(Δt)−r_i(0)\|²⟩ = Σ_i (1/N_Δt) Σ_{t=0}^{t_tot−Δt} \|r_i(t+Δt)−r_i(t)\|²` | ★ **여기가 multi-time-origin 의 정본 문장**이다. *"This averaging over different N_Δt time intervals provides **essential ensemble sampling**"* |
| (3) | `MSD(Δt) = TMSD(Δt)/N` | N = 이동 carrier 로 **가정한** 이온 수 |
| **(4)** | `D = MSD(Δt)/(2dΔt) + D_offset`, d = 3 | ★ **절편 D_offset 이 식 자체에 들어 있다 = 자유절편** |
| (5) | `σ = N q² D /(V k T)` — **Nernst–Einstein** | 본문이 스스로 *"assumes dilute, non-interacting mobile ions"* 라 적고, 빠른 전도체는 강상관이라 **Haven 비 ≠ 1** 임을 인정 |
| (6) | `σ = q²/(VkT) · TMSD(Δt)/(2dΔt)` | ★ σ 는 **carrier 수 세기와 무관**하다 — N 이 약분된다 |
| (7) | `D = D₀ exp(−Ea/kT)` | |
| **(8)** | `s_D/D_true = A/√N_eff + B`, **A = 3.43, B = 0.04** | ★ **경험식**. 네 계 + 고전MD 1계에 맞춘 것 |
| **(9)** | `N_eff = max_Δt[TMSD(Δt)] / a²` | a = 이웃 이동이온 자리 간 **평균 거리** |
| (10) | `D = a²ν exp(−Ea/kT)`, ν = 10¹² Hz | `Fig. 5` 지도용 **back-of-the-envelope**. 기하인자·상관인자 **무시** |

**a 값 (본문 축자)**: LLZO **2.4** · LATP **3.2** · LGPS **2.8** · RbAg₄I₅ **3.4** Å.
그 밖의 모든 추정에는 **a = 3 Å 을 가정**한다고 명시.

**★ Haven 비 관련 — 본문이 스스로 한 걸음 물러선 자리**:
점프확산계수 `D_J` (전 이온 질량중심 MSD 로 추정)를 tracer D 로 나눈 것이 Haven 비인데,
*"our analysis found that tracking the displacement of the single center point exhibits **higher
statistical variance**"* ⇒ 이 논문의 분산 체계는 **tracer D 에 대해서만** 세웠고 `D_J` 는
*"similar scheme can be applied and developed"* 로 미뤘다. **즉 이 논문은 Haven 비의 오차를 주지 않는다.**

### 4-B. 아레니우스 적합 — **가중최소제곱** (본문 + SI Note 2)

- log(D) vs 1/T 선형적합. **각 점의 가중치 = 1/Var(log D)**. (본문 ref 46 = Ruppert & Wand)
- SI 식 (3): `σ²_logD = σ²_D / D²` — ⚠ **밑(base)을 안 적었다.** 이 식은 **자연로그**용이고
  실제 코드는 log₁₀ 에 `log₁₀(e)` 야코비안을 곱한다 (§6-D). **코드가 맞고 SI 표기가 헐렁하다.**
- 회귀는 **SciPy**.
- Ea·D₀ 의 오차범위, 그리고 외삽 온도의 D·σ 오차범위는 *"standard error analysis for linear regression"* 으로.

### 4-C. 계산 설정 (METHODS 축자)

| 항목 | 값 |
|---|---|
| 코드 | **VASP** (ref 49) |
| 의사퍼텐셜 | **PAW** |
| 범함수 | **PBE (GGA)** — vdW 보정 **언급 없음** |
| 스핀 | **non-spin-polarized** |
| k-점 | **Γ점 1개** |
| 시간간격 | **2 fs** (AIMD·고전MD 공통) |
| 앙상블 | **NVT**, **Nosé–Hoover** thermostat, **velocity–Verlet** 적분 |
| 근사 | **Born–Oppenheimer** MD |
| 초기구조 | Materials Project 표준 파라미터로 **정적 이완** (refs 51–53) |
| 고전 MD | **LAMMPS**, LLZO **8 f.u.**, 퍼텐셜 = Adams & Rao (ref 55) |
| 구조 출처 | **ICSD** + Materials Project |
| **무질서 처리** | ★ *"The structures with **disordered site occupancy were ordered** using the same method in the previous studies (refs 5, 7)"* — **Ewald 최저에너지 단일배열 1개**. SQS 아님, 앙상블 아님 |
| LATP 만듦 | LiTi₂(PO₄)₃ 에서 Ti→Al **부분치환 + Li 삽입** |

⚠ **ecut · 원자 수 · 슈퍼셀 크기 · 평형화 시간 · 총 런 길이 표가 본문에 없다.**
읽을 수 있는 것은 그림 캡션의 개별 값뿐이다: LATP 1200 K **200 ps**(`Fig. 1`) / LATP 1200 K
**500 ps 를 50 ps × 10 으로 쪼갬**(`Fig. 3`) / LLZO **40 ps**(`Fig. S4`).
⇒ **"He 2018 의 AIMD 설정을 따랐다" 고 쓸 수 있는 수준의 표가 이 논문에 없다.**

---

## 5. Figure set ★ — **6장 전부 실제로 열람** (표 2개는 PDF 텍스트로)

> 크로핑 8장 = `fig_1`–`fig_6` + `tab_1` + `tab_S1`.
> **그림 6장은 전부 PNG 를 열어 읽었다.** 표 2장(`tab_1`, `tab_S1`)은 **일부러 안 봤다** —
> 글자라서 PDF/docx 텍스트가 이미지 판독보다 정확하다 (§3-A·3-B 가 그 텍스트다).

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | LATP 1200 K 200 ps 의 **log–log MSD–Δt**. 파란 파선 `MSD ∝ Δt^1.42`(탄도), 빨간 파선 `MSD ∝ Δt`(확산). **inset = 선형축 0–1.1 ps**. 실독: Δt^1.42 는 **0.012–0.1 ps** 구간에만 붙고, **0.1–1 ps 에 뚜렷한 어깨(케이지)** 가 있어 MSD 가 1.3 → 5 Å² 밖에 안 오른다. inset 은 **≈0.15 ps · MSD ≈1.5 Å² 에서 꺾인다** — 즉 **진짜 탄도 무릎은 0.15 ps 인데 논문이 채택한 컷오프(0.5a² = 5 Å²)는 ≈1 ps** 로 **7배 뒤**다 | **우리 2 ps 하한이 물리적으로 늦지 않다는 근거.** 동시에 *"He 의 규칙은 물리적 필요보다 훨씬 보수적"* 이라는 근거. ⚠ log–log 축이 큰 Δt 의 분산을 **시각적으로 숨긴다** — `Fig. 3a` 와 대조 |
| **2** | 같은 궤적의 **MSD(검정, 왼축 0–25 Å²) + dMSD/dΔt(빨강, 오른축 0–15 Å²/ps) vs Δt 0–6.2 ps**. 검정 점선이 탄도 컷오프 표시 | 실독: 빨간 미분이 Δt→0 에서 **≈15 Å²/ps** → **0.3 ps 에 이미 ≈4** → **1 ps 이후 ≈3.3 Å²/ps 평탄**(본문 "~3" 과 일치, `figure-read ≈ 3.3`). 점선은 **MSD = 5 Å² @ Δt ≈ 1.05 ps**. ⇒ **미분이 평탄해지는 시각(≈0.3–0.7 ps)이 컷오프(1 ps)보다 이르다.** 우리가 창 하한을 정할 때 **dMSD/dΔt 평탄화를 직접 보는 것이 MSD 문턱보다 물리적** |
| **3a** | **같은 LATP 모델 · 같은 1200 K** 의 500 ps 를 **겹치지 않는 50 ps 10조각**으로 쪼갠 MSD–Δt 10개 (선형축, 0–50 ps, 0–210 Å²) | 🔴 **이 논문에서 제일 무서운 그림.** 실독: Δt = 50 ps 에서 10곡선이 **≈50 ~ ≈210 Å² (4.2배)** 로 벌어진다. Δt = 25 ps 에서도 **≈40 ~ ≈95 Å² (2.4배)**, Δt = 10 ps 에서 **≈15 ~ ≈38 Å²** (전부 `figure-read ≈`). **두 곡선(녹색·자홍)은 40 ps 이후 MSD 가 실제로 내려간다** — 원점 수 부족의 지문. ⇒ **"우리 단일 궤적 D" 가 얼마나 흔들릴 수 있는지의 시각적 상한** |
| **3b** | 10 곡선의 **R² vs Δt_upper (t_tot 의 10–100 %)**, 평균 ± 표준편차 | 실독: R² ≈ **1.000**(10–30 %) → **0.996**(40–60 %) → **0.991**(70 %) → **0.983**(80 %) → **0.973**(90 %) → **0.947**(100 %). **오차막대는 ±0.001 → ±0.08 로 80배 커진다** (`figure-read ≈`). 🔴 **무릎이 없다** — 0.7 t_tot 은 매끈한 곡선에 그은 **판단선**이지 데이터가 가리키는 문턱이 아니다. 진짜 신호는 R² 값이 아니라 **R² 의 분산 증가** |
| **4a** | **RSD(D) vs N_eff, x = 0–300** — LLZO 600 K(검정■) · LATP 1200 K(녹색●) · LGPS 900 K(파랑▲) · **RbAg₄I₅ 300/500 K**(청록▼) + 빨간 적합선 `3.43/√N_eff + 0.04` | ★ **식 (8)의 근거 전부.** 실독: **AIMD 점은 N_eff ≈ 10 ~ 265 에만 있다.** N_eff≈10 에서 RSD ≈ **1.15(115 %)**. 산포가 크다 — N_eff ≈ 180 의 파란 점이 **0.19** 인데 선은 **0.30** (상대 −37 %). ⇒ **식 (8)은 법칙이 아니라 구름을 통과하는 적합선**이고 개별 점은 **±30–40 % 상대오차**로 벗어난다 |
| **4b** | 같은 축, **LLZO 600 K 고전 MD**, x = 0–6000, y = 0–0.4 | 🔴🔴 **우리 box331 판정의 핵심 그림.** 실독: 데이터는 N_eff ≈ 150(RSD 0.26) 부터 ≈5800(RSD **0.105**)까지. **N_eff ≳ 1200 부터 점들이 빨간 선 위로 체계적으로 뜨고, RSD 가 ≈0.10–0.11 에서 평탄해진다** (`figure-read ≈`). 선은 계속 내려가 5800 에서 0.088 을 가리키는데 데이터는 0.105 다. ⇒ **이 논문의 어떤 데이터도 RSD 0.10 아래로 간 적이 없다.** B = 0.04 는 (b)가 아니라 **(a)의 적합에서 나온 값**이고, (b) 영역에서는 식이 **낙관적**이다 |
| **5** | **D 의 색지도: x = T 200–2300 K, y = Ea 0.05–1.0 eV**, 등D선 10⁻⁹(빨강 실선) 10⁻⁸(녹점선) 10⁻⁷(주황 dash-dot) 10⁻⁶(파랑 dash-dot-dot) 10⁻⁵(짙은 파선) 10⁻⁴(파랑 실선) | 실독 후 식 (10)으로 **검산 통과**: 10⁻⁷ 선이 (500 K, ≈0.39 eV)·(1000 K, ≈0.78 eV) → 계산 0.392/0.785 ✅. 10⁻⁶ 이 (500, 0.29)·(1000, 0.59) ✅. **우리 운영점 (600 K, Ea ≈ 0.17–0.20 eV)** 은 10⁻⁵ 파선과 10⁻⁴ 실선 사이 **진한 파랑 한복판** ⇒ **He 기준 AIMD 접근영역 안쪽 깊숙이** |
| **6** | **아레니우스 3계**: x = 1000/T **0.6–1.7**(≈590–1670 K), y = log D −6.5 ~ −3.5. LGPS(검정■) · LATP(파랑▲) · LLZO(빨강●), 각 점에 식 (7–9) 기반 오차막대 | 실독: 세 계 모두 **9점 · 600–1500 K**. ⇒ **Δ(1/T) ≈ 1.0×10⁻³ K⁻¹** (우리 600/800/1000 은 **0.667×10⁻³**, **1.5배 짧다**). 오차막대는 고온 **±0.05 dex** → 저온 **±0.12–0.18 dex** 로 **약 2–3배** 커진다(`figure-read ≈`). ⚠ 본문의 *"significantly larger variance at lower temperatures"* 는 **2–3배** 정도이지 극적이지 않다. **LATP 점들의 선 이탈이 가장 크다**(1000/T≈1.25 에서 선 아래 ≈0.2 dex) |
| **Table 1** | Ea·σ(300 K)·오차범위 3계 | §3-A. **PDF 텍스트 전사** (이미지 미판독) |
| **Table S1** | LGPS 점 제거 민감도 3판 | §3-B. **docx 텍스트 전사** (이미지 미판독) |

**SI 그림 (docx 텍스트만 확보, 이미지 없음 — 캡션만 읽었다)**
- `Fig. S1` 조화진동 모형: `x = (A/2)sin(2πt/T)`, A = 2, T = 1000 → max MSD ≈ **0.5A²**,
  0 < Δt < 500 적합이 **Δt^1.42** 를 준다. ⇒ **본문 `Fig. 1` 의 지수 1.42 는 물리가 아니라
  "유한창에서 조화진동을 MSD 로 재면 나오는 수"다.**
- `Fig. S2` 적합된 D 값들의 **히스토그램 + 가우시안 KDE** (Seaborn).
- `Fig. S3` **LGPS·LLZO 900/1200 K** 의 상한 검증 — 0.7 t_tot 규칙의 일반성 근거.
- `Fig. S4` 40 ps 짧은 런 (§3-E).
- `Fig. S5` LGPS 점 제거 3판 (§3-B).

---

## 6. 코드 저장소 실측 ★★ — `github.com/mogroupumd/aimd` @ `6616528`

> 논문이 데이터를 안 주는 대신(*"available from the corresponding author on reasonable request"*)
> **분석 코드는 공개**했다. 여기가 이 digest 의 두 번째 본체다.

### 6-A. 구조

```
aimd/diffusion.py      582줄  DiffusivityAnalyzer · ErrorAnalysisFromDiffusivityAnalyzer
                              · ArreheniusAnalyzer · get_conversion_factor
aimd/script/analyze_aimd.py 325줄  CLI (`analyze_aimd diffusivity|arrhenius`)
aimd/tests/            test_diffusion.py · test_arrhenius.py · test_files/{latp_md, arrhenius}
aimd/tests/AE_sample/  INCAR / INCAR.MD / INCAR.heat / KPOINTS / POSCAR / sub.slurm
setup.py               install_requires pymatgen>=2017.12.30, argparse, PrettyTable
                       classifiers: **Python :: 2 / 2.7 만**
```
`analyze_aimd.py` 첫 줄이 `#!/usr/bin/python2.7` 이다. **2018년 py2 코드다.**

### 6-B. ★ MSD 계산 — **모든 시간원점 평균, FFT 로**

`diffusion.py:81–110` (`코드 실측`):
- `autocorrelation_fft(x)` — FFT 자기상관 후 `res / (N − arange(N))` 로 정규화.
- `one_ion_msd_fft(r, dt_indices)` — 표준 **S1 − 2·S2** 분해.
  `S1` 은 `Q(m) = Q(m−1) − r²[m−1] − r²[N−m]`, `S1(m) = Q(m)/(N−m)` 재귀 (`:100–102`).
- ⇒ **lag m 의 평균에 쓰이는 원점 수는 정확히 (N − m)** = 식 (2)의 `N_Δt`.
  **✅ 코드 ≡ 논문 식 (2). "multi-time-origin 은 He 2018" 이라는 우리 기록은 맞다.**
- `dt_indices = np.arange(1, n_steps, max(int((n_steps−1)/time_intervals_number), 1))` (`:75`) —
  기본 `time_intervals_number = 1000` 이라 **dt 격자를 ~1000 점으로 균일 서브샘플**.

### 6-C. ★★ 적합 창 — **코드가 논문보다 구체적이고 더 엄격하다**

`diffusion.py:48–49` 기본값 (`코드 실측`):
```python
spec_dict = {'lower_bound': 4.5, 'upper_bound': 0.5, 'minimum_msd_diff': 4.5}
```
`:129–130`:
```python
lower_bound_index = len(msd[msd < spec_dict['lower_bound']])      # MSD < 4.5 Å² 인 점의 개수
upper_bound_index = int(len(msd) * spec_dict['upper_bound']) - 1  # dt 격자의 앞 50 %
```

| 경계 | 코드가 실제로 하는 것 | 논문 본문 | 판정 |
|---|---|---|---|
| **Δt_low** | **MSD(per ion) 가 4.5 Å² 를 처음 넘는 시각.** 4.5 = **0.5 × 3.0²** = 기본 `site_distance` 3 Å 의 0.5a² | *"cut-off in MSD using the value of a fraction of a² (e.g., 0.5a²)"* | ✅ **일치.** ★ **고정 시간이 아니라 고정 변위**다 |
| **Δt_up** | **t_tot 의 0.5** (dt 격자 점수의 앞 절반) | *"Δt_up < 0.7 t_tot"* (결론 1) / *"<30–70 % of t_tot"* (Discussion) | ⚠ **코드가 더 보수적.** 논문은 0.7 을 권하고 코드는 0.5 를 기본값으로 박았다 |
| **최소 창 크기** | `msd[up] − msd[low] ≥ 4.5 Å²` 아니면 **적합하지 않는다** | 본문에 **대응 문장 없음** (SI Note 3 이 정신만 암시) | 🔴 **코드에만 있는 게이트** |

CLI(`analyze_aimd.py:61–67`)는 이것을 `a` 로 환산해 받는다 —
`lower_bound = (-l 기본 0.5) × a²`, `minimum_msd_diff = (-min 기본 0.5) × a²`, `upper_bound = (-u 기본 0.5)`.
그리고 **`site_distance` 는 CLI 의 필수 위치인자**(`:237–241`) — *"If there are many different
paths, you can provide an averaged value"*. ⇒ **CLI 는 사용자에게 a 선언을 강제하고, 라이브러리는
몰래 3.0 을 쓴다.** 라이브러리를 직접 import 하면 a 가 조용히 3.0 이 된다.

**절편**: `:153` `stats.linregress(dt[lo:up+1], msd[lo:up+1])` → **자유절편.** `intercept` 를 받아
저장만 하고 D 에는 안 쓴다 (`:192` `diffusivity = slope/(20*dim)`).
**✅ 논문 식 (4)의 `D_offset` = 자유절편. 우리 규약과 같다.**
(단위: `dt` 가 fs 라 `20·d = 2·d·10` 의 10 이 Å²/fs → cm²/s 환산. 검산 통과.)

### 6-D. ★★★ 오차 공식의 본체 — `ErrorAnalysisFromDiffusivityAnalyzer`

`diffusion.py:400–421` **전문** (`코드 실측`):
```python
def __init__(self, diffusivity_analyzer, site_distance=3.0):
    n_jump = len(diffusivity_analyzer.indices) * \
             np.max(diffusivity_analyzer.msd) / (site_distance * site_distance)
    n_jump_component = len(diffusivity_analyzer.indices) * \
             np.max(diffusivity_analyzer.msd_component, axis=1) / (site_distance * site_distance)
    RSD_D = 3.43 / np.sqrt(n_jump) + 0.04
```

**식으로 풀면**

> **N_eff = N_mobile × max_Δt[MSD(Δt)] / a²**
> `= max_Δt[TMSD(Δt)] / a²` **≡ 논문 식 (9)** ✅
> **RSD(D) = 3.43/√N_eff + 0.04** **≡ 논문 식 (8)** ✅

**입력이 정확히 무엇인가 — 이게 §7-D 의 열쇠다**

| 입력 | 출처 | 비고 |
|---|---|---|
| **N_mobile** | `len(analyzer.indices)` = 구조에서 해당 원소 개수 | |
| **max(MSD)** | MSD–Δt **곡선 전체의 최댓값** (적합 상한 **바깥**까지 포함) | ⚠ 적합에서 일부러 잘라낸 **가장 시끄러운 꼬리**를 여기서는 쓴다 |
| **a (`site_distance`)** | **인자. 기본 3.0 Å** | 논문의 *"assumed for all following estimations"* 값. **재료값이 아니다** |
| **온도** | ❌ **안 쓴다** | |
| **궤적 길이 t_tot** | ❌ **직접은 안 쓴다** (max MSD 를 통해서만) | |
| **원자 수 (비이동)** | ❌ **안 쓴다** | |
| **적합 창** | ❌ **안 쓴다** | RSD 는 창과 무관하게 정해진다 |

🔑 **즉 식 (8)의 입력은 실질적으로 스칼라 하나(N_eff)뿐이다.**
`N_eff` 만 알면 궤적을 다시 안 읽어도 RSD 가 나온다. **이것이 우리가 쓸 수 있는 이유다.**

**왜 기본값이 3.0 Å 인가**: 논문이 *"a typical ionic conductor with **assumed site distance a = 3 Å**"*
(`Fig. 5` 캡션)이라고 쓰고 §Accessible range 의 모든 추정에 3 Å 을 쓴다. 실제 재료값은
2.4(LLZO)–3.4(RbAg₄I₅) Å 로 흩어져 있으니 **3.0 은 그 가운데 대표값**이다.
⚠ **N_eff ∝ 1/a² 이므로 a 를 2.4 로 쓰면 N_eff 가 1.56배, 3.4 로 쓰면 0.78배**가 된다.
RSD 는 √N_eff 에 반비례하므로 **a 를 25 % 틀리면 RSD 가 25 % 틀린다.** a 는 선언해야 하는 수다.

**`ArreheniusAnalyzer` 가 `diffusivity_errors` 를 어떻게 쓰나** (`:449–485`, `코드 실측`)

```python
x = 1000/T ;  y = log10(D)
if diffusivity_errors is None:
    [slope, intercept], cov = curve_fit(linear, x, y)                       # ← absolute_sigma=False (기본)
else:
    y_error = [log10(e) * σ_D[i] / D[i] for i ...]                          # = log10(e) · RSD
    [slope, intercept], cov = curve_fit(linear, x, y, sigma=y_error, absolute_sigma=True)
Ea       = (-8.617e-5 * 1000 * ln10) * slope
Ea_error = -1 * (-8.617e-5 * 1000 * ln10) * slope_sigma
```

🔴 **두 갈래가 서로 다른 뜻의 오차막대를 낸다:**
- **오차를 주면** `absolute_sigma=True` ⇒ Ea 오차가 **오직 입력 σ_D 의 전파**. 점들이 직선에서
  벗어나도 **오차막대가 안 커진다.**
- **오차를 안 주면** `absolute_sigma=False` ⇒ 공분산이 **잔차로 재척도**. 3점·2모수면 dof = 1 이라
  그 값은 **극도로 시끄럽다.**
⚠ SI Note 2 는 이 구분을 **한 글자도 적지 않는다.** 논문을 읽고 구현하면 갈라진다.

`log10(e)` 야코비안이 코드에는 있고 SI 식 (3)에는 없다 — **코드가 맞다.**

### 6-E. 🔴 코드가 **조용히 틀리는/죽는** 자리 4건 (우리 §코드 규율의 실사례)

| # | 위치 | 내용 |
|---|---|---|
| **①** | `diffusion.py:131–151` | **예외를 던지는 판이 주석으로 죽어 있고**, 대신 `slope = intercept = -1` 을 넣는다. `:192` 에서 **`diffusivity = −1/60 = −0.0167 cm²/s`** 가 된다. **음수 D 가 예외 없이 리턴된다.** CLI 는 `if da.diffusivity > 0:` 로 걸러 주지만(`analyze_aimd.py:71`), **라이브러리를 직접 쓰면 아무 경고 없이 −0.0167 을 받는다.** ⇒ 우리 규율의 *"조용히 틀린 경로"* 교과서 사례 |
| **②** | `diffusion.py:164–165` | `self.drift = drift` — `drift` 는 `len(framework_indices) > 0` 인 `else` 가지에서만 정의된다. **모든 원자가 이동종이면 `NameError`** |
| **③** | `diffusion.py:435–436` | `d['diffusivity_component_relative_standard_deviation']` 에 **먼저 상대값을 넣고 바로 다음 줄에서 절대값(RSD×D)으로 덮어쓴다.** **키 이름은 "relative" 인데 담긴 값은 절대 σ 다.** 스칼라 쪽은 두 키가 따로 있는데(`:433–434`) **성분 쪽은 상대값이 소실**된다 |
| **④** | `diffusion.py:570` | `el, occu = structure.composition.items()[0]` — **py3 에서 `TypeError: 'dict_items' object is not subscriptable`** (내가 실행해 확인). **`get_conversion_factor` = 전도도 경로 전체가 현대 파이썬에서 죽는다.** 우리가 이 코드를 그대로 쓰려면 **반드시 패치해야 한다** |

부가: `diffusion.py:69` 의 `df = ...get_fractional_coords(dc)` 와 `:71` 의
`displacements_frac_final_diffusion_ions` 는 **어디서도 안 쓰인다** (죽은 코드).
`:411–412` 의 **성분별 n_jump** (축별 MSD 를 **전체 a²** 로 나눔)는 **논문에 대응 식이 없다** —
등방계면 축별 MSD 는 전체의 ~1/3 이라 성분 RSD 가 체계적으로 **√3 ≈ 1.7배 크게** 나온다.

### 6-F. ★ 코드에만 있고 논문에 없는 **두 개의 건강검진**

`analyze_aimd.py:92–104` (`코드 실측`):
- **`max(drift_maximum) > 3 Å`** → *"The entire cell has significant drift, please check the MD data"*
- **`max_framework_displacement > 5 Å`** → *"There are significant movement for framework ions, **may be melt**"*
  (git 커밋 메시지가 `add warning of metl` — 이 경고가 마지막 커밋이다)

그리고 `diffusion.py:66–68` 의 **골격 드리프트 차감**:
```python
framework_disp = displacements[framework_indices]
drift = np.average(framework_disp, axis=0)[None, :, :]
dc = displacements - drift
```
⇒ **비이동 원자들의 평균 변위를 모든 원자에서 뺀다.** 이는 전체 COM 고정과 **다르다** — 이동이온을
뺀 **골격 부격자**의 드리프트를 지운다. 우리 b2o3 의 **음이온 골격 creep** 이 정확히 이 검사에
걸릴 종류다 (§7-G).

### 6-G. 🔴 **README 가 테스트 데이터의 계를 잘못 적고 있다** (내가 확인)

README 4-f: *"You will get the arrhenius relationship of **LATP**. The conductivity at 300 K is
predicted to be ~1.08 mS/cm, Ea is ~0.258 eV ± 0.017 eV."*

그런데 `aimd/tests/test_files/arrhenius/POSCAR` 첫 줄은 **`Li56 La24 Zr16 O96`, a = 12.98 Å 정육면체**
= **입방 LLZO 8 f.u.** 다. 그리고 그 값들을 `Table 1` 과 대면 —

| | 테스트가 내는 값 | `Table 1` LATP | `Table 1` **LLZO** |
|---|---|---|---|
| Ea | **0.2581 ± 0.0168** | 0.25 ± 0.02 | **0.26 ± 0.02** ✅ |
| σ(300 K) | **1.0804** | 1.2 | **1.1** ✅ |
| 범위 | **[0.545, 2.141]** | [0.5, 2.5] | **[0.5, 2.1]** ✅ |

⇒ **테스트 데이터는 LLZO 이고, README 의 "LATP" 가 오기다.**
✅ 동시에 이것은 큰 소득이다 — **`Table 1` 의 LLZO 행이 저장소 안에 원자료로 들어 있다.**
`D_T.csv` 9점: **600 / 650 / 700 / 720 / 800 / 900 / 1050 / 1200 / 1500 K**,
D = 1.24e-6 … 1.83e-5 cm²/s, D_error 로 환산한 **RSD = 27.4 / 26.0 / 26.2 / 20.9 / 19.9 / 14.4 /
16.3 / 10.8 / 14.1 %**. ⇒ **He 자신이 논문에 쓴 D 점들의 RSD 는 11–27 % 대**다.

✅ **내가 scipy 로 `ArreheniusAnalyzer` 를 재구현해 테스트 단언값을 전부 재현했다**
(Ea 0.2581282825 vs 단언 0.258128283 · Ea_err 0.0168320192 vs 0.0168320198 ·
D(300) 6.8075404e-9 vs 6.8075402e-9 · 환산인자 158701249.73192352 **완전일치** ·
σ(300) 1.0803652 / [0.5450969, 2.1412504] **완전일치**). **코드 해석이 맞다는 증명이다.**

### 6-H. 🔴 `predict_diffusivity` 가 **표준 회귀를 안 한다** (외삽 오차가 과대)

`diffusion.py:494–495` (`코드 실측`):
```python
logD_sigma = np.sqrt(np.power(self.slope_sigma * (1000.0/temperature), 2)
                     + np.power(self.intercept_sigma, 2))
```
⇒ **기울기–절편 공분산 항 `2·x·Cov(s,i)` 가 빠졌다.** 아레니우스 적합에서 `Cov(s,i) < 0` 이므로
(x > 0), 코드는 **항상 실제보다 넓은 구간**을 낸다.

**내 검산 (LLZO, 저장소 원자료, 300 K 외삽)**:
| | σ_log10D(300 K) | σ(300 K) 구간 |
|---|---|---|
| **코드/논문** | **0.2971** | **[0.545, 2.141]** (= `Table 1` 의 [0.5, 2.1]) |
| **표준 가중회귀** | **0.1966** | **[0.687, 1.699]** |
⇒ **논문 `Table 1` 의 오차범위는 log 스케일에서 1.51배 넓다.**
*"as large as an order of magnitude"* 라는 논문 서술은 **자기 코드의 근사 때문에 부풀어 있다.**
(우리 유도, 논문 미보고)

### 6-I. ⚠ 샘플 INCAR — thermostat 이 METHODS 와 다르다

`aimd/tests/AE_sample/INCAR.MD` (`코드 실측`):
```
IBRION=0  POTIM=2  NSW=1000  NBLOCK=1  KBLOCK=100
SMASS=-1  TEBEG=1500  TEEND=1500
ISPIN=1  ISYM=0  ISMEAR=0  SIGMA=0.05  PREC=Normal  LREAL=True  EDIFF=1e-5  NELM=500  ALGO=Fast
```
- **`SMASS = -1` 은 VASP 에서 Nosé–Hoover 가 아니라 속도 스케일링**이다 (NH 는 `SMASS ≥ 0`).
  METHODS 는 *"NVT ensemble using a Nose–Hoover thermostat"* 라고 적었다.
- `INCAR.heat` 은 `TEBEG=100 → TEEND=1500` 램프 = 가열용.
- `NSW=1000 × POTIM=2 fs` = **RUN 폴더 하나가 2 ps**. CLI 가 `RUN_10 … RUN_29` 를 이어 붙이는 구조.
⚠ 다만 이 샘플의 POSCAR 는 **`Li48 Al16 N32`** 로 **논문의 어느 계도 아니다.** 사용자용 템플릿일
가능성이 높으므로 *"논문의 실제 INCAR"* 로 단정하지 않는다. **불일치 사실만 기록한다.**
(참고: `diffusion.py:302` 는 온도를 **`TEEND`** 에서 읽는다 — 램프 INCAR 로 분석하면 틀린 T 가 박힌다.)

---

## 7. 우리 대비 ★★ — 지시된 질문 1–7 에 정면으로 답한다

> 대상: `CLAUDE.md` MLIP-MD 규약 · `tools/modelc_v3/disorder_ensemble_diffusion.py` ·
> `tools/ionic/{msd_diffusive_check, msd_refit_window, hops_per_ion, arrhenius_compat}.py` ·
> `db/properties/canonical_registry.json` · `kb/methodology/md_conductivity_protocol.md` ·
> `db/properties/lpscl_smallcell_glass_md_estimand_2026_09_21.json`

### 7-A. 【질문 1】 MSD 적합 창 — 고정 창인가, 비율인가, 수렴판정인가

**답: 둘 다 아니다. 하한은 고정 *변위*, 상한은 궤적 길이의 *비율*이다.**

| | **He 2018 (논문 + `코드 실측`)** | **우리 (`CLAUDE.md`)** | 판정 |
|---|---|---|---|
| **하한 Δt_low** | **MSD/이온이 0.5a² 를 넘는 시각** (기본 4.5 Å²). **온도·계마다 시각이 달라진다** | **2.0 ps 고정** | 🔴 **다른 규약** |
| **상한 Δt_up** | **0.5 t_tot** (코드 기본) / **< 0.7 t_tot** (논문 권고) | **50 ps 고정** | ✅ 우리가 더 보수적 (§아래) |
| **수렴판정** | 없음 | 없음 (β·D_inc plateau 는 우리 것) | — |

**무엇을 가정하는가 — 이게 핵심이다**
- **He 의 하한**은 *"국소 진동은 자리 사이 퍼텐셜 우물 안에 갇히므로 변위가 a 의 일부를 못 넘는다"* 를
  가정한다 ⇒ **변위 문턱.** 저온일수록 그 문턱에 늦게 도달하므로 **창이 자동으로 뒤로 밀린다.**
- **우리 하한**은 *"탄도/진동 구간은 몇 ps 안에 끝난다"* 를 가정한다 ⇒ **시간 문턱.** 온도와 무관하다.
- 둘 다 **자유절편**을 쓰므로 **일정한 케이지 오프셋은 절편이 먹는다.** 남는 위험은 창 안의
  **곡률**(sub-diffusive)이고, 그건 저온에서만 문제다.

**우리 실데이터에 He 의 하한 규칙을 그대로 대 봤다** (`db/properties/msd_3sys_200ps_origin.csv`,
a = 3.0 Å · 0.5a² = 4.5 Å²) — **(우리 유도, 논문 미보고)**

| 계·온도 | MSD(2 ps) | **4.5 Å² 도달 시각 = He 의 Δt_low** | 우리 창 | 판정 |
|---|---|---|---|---|
| modelc 600 K | 2.41 Å² | **6.0 ps** | 2–50 | 🔴 2–6 ps 가 He 기준 **탄도/케이지** |
| modelc 800 K | 5.40 | **2.0 ps** | 2–50 | ✅ 일치 |
| modelc 1000 K | 8.60 | **2.0** | 2–50 | ✅ |
| lpsocl 600 K | 3.42 | **4.0** | 2–50 | 🔴 |
| lpsocl 800 K | 4.44 | **3.0** | 2–50 | ⚠ 경미 |
| lpsocl 1000 K | 8.09 | **1.0** | 2–50 | ✅ |
| b2o3 600 K | 2.36 | **4.0** | 2–50 | 🔴 |
| b2o3 800/1000 K | 4.32 / 7.43 | 3.0 / 1.0 | 2–50 | ⚠ / ✅ |

⇒ **우리 2 ps 하한은 800·1000 K 에서는 He 규칙을 만족하고, 600 K 에서만 2–4 ps 이르다.**

🔴 **그리고 그게 Ea 를 얼마나 바꾸는지 계산했다** — 같은 CSV 에서 창만 He 규칙으로 갈아끼우면
(Δt_low = 4.5 Å² 도달 시각, Δt_up = 0.5 t_tot):

| 계 | 우리 (2,50) Ea | **He 창 Ea** | 차이 |
|---|---|---|---|
| **modelc** | 0.1972 eV | **0.2371 eV** | **+40 meV** |
| **lpsocl** | 0.2839 eV | **0.2414 eV** | **−43 meV** |
| **b2o3** | 0.1995 eV | **0.2251 eV** | **+26 meV** |
| **modelc↔lpsocl 격차** | **+87 meV** | **+4 meV** | 🔴🔴 **효과가 사라진다** |

**우리에게 불리한 결론이므로 그대로 적는다.** 다만 **네 가지 완화 조건**을 같이 적는다 —
① 이 CSV 는 **gen0_pre_gate · 단일 시간원점 · 200 ps** 로 레지스트리가 이미 **superseded** 로
찍어 둔 계보다. ② `lpsocl 600 K` 는 게이트 FAIL(β 0.615)로 **"DO NOT QUOTE"** 딱지가 있다.
③ He 창의 상한 100 ps 는 단일원점 곡선의 가장 시끄러운 구간이다. ④ `msd_refit_window.py` 의
docstring 이 *"20–200 창에서 Ea 가 −242 meV"* 라고 **이미 같은 취약성을 기록**해 뒀다.
⇒ **새로운 것은 "어떤 창이든 흔들린다" 가 아니라 "He 가 처방한 바로 그 창에서도 흔들린다" 이다.**
**gen2 box331 400 ps MTO 자료로 같은 시험을 반드시 다시 돌려야 한다** (§8-3).

**상한은 우리가 이긴다**: 우리 50 ps / t_tot —
200 ps 런 → **0.25 t_tot** · 400 ps 런 → **0.125 t_tot** · 99 ps 고온런 → **0.505 t_tot**.
He 의 0.7 t_tot 상한을 **모든 경우에 만족**하고 코드 기본 0.5 도 만족한다. ✅
그리고 우리 MTO 는 최대 lag 를 t_tot/2 로 자르므로(`disorder_ensemble_diffusion.py:123`)
**구조적으로 0.5 t_tot 을 넘을 수 없다** — He 의 상한 규칙이 우리 코드에 이미 내장돼 있는 셈이다.

### 7-B. 【질문 2】 절편 — 자유인가 0 고정인가

**답: 논문·코드 양쪽 다 자유절편이다. 우리와 같다.** ✅
- 논문 식 (4)가 `+ D_offset` 을 **식 안에** 적는다.
- `diffusion.py:153` `stats.linregress` → 절편 자유, D 는 기울기만 사용.
- 우리 `li_diffusion_from_frames`(`disorder_ensemble_diffusion.py:168`) `np.polyfit(...,1)[0]` → 동일.
⇒ **우리 "자유절편 D" 규약에 외부 근거가 생겼다.** (지금까지 근거는 `mccluskey2025` 뿐이었다.)

### 7-C. 【질문 3】 오차 공식의 본체 — 코드 ↔ 논문 대조

**답: 코드와 논문이 완전히 일치한다.** §6-D 참조.
`n_jump = N_mobile × max(MSD)/a²` = 식 (9)의 `max(TMSD)/a²`, `RSD = 3.43/√n_jump + 0.04` = 식 (8).
저장소 테스트가 `n_jump = 100.48841284`, `RSD = 0.382165427856` 을 단언하고 손계산이 맞는다.

**불일치는 오차식 본체가 아니라 그 주변에 있다**:
① 성분별 RSD 는 논문에 없다 · ② 키 이름과 내용이 어긋난다(§6-E③) ·
③ `max(MSD)` 를 **적합 창 밖**까지 포함해 잡는다(논문 표현 *"over the entire MSD–Δt curve"* 와는
일치하지만, **잘라낸 이유가 시끄럽다는 것이었는데 그 구간의 최댓값을 쓴다**는 모순이 남는다).

**`site_distance = 3.0` 의 정체**: 재료 상수가 아니라 논문의 **범용 가정값**(`Fig. 5` 캡션
*"assumed site distance a = 3 Å"*). 실제 값은 2.4–3.4 Å 로 흩어진다.
🟢 **우리에겐 운이 좋다** — 우리 `tools/ionic/msd_diffusive_check.py` 의 `D_HOP_A = 3.0`
(*"이웃 Li 자리 간격 [Å] — hops_per_ion.py 와 같은 규약"*)과 **값도 의미도 같다.**
그리고 우리 `hops_per_ion.py` 의 `n_hop = MSD/d_hop²` 은 **정확히 `N_eff/N_mobile`** 이다.
⇒ **우리는 이미 He 의 N_eff 를 계산하고 있었고, 그걸 RSD 식에 넣은 적이 없을 뿐이다.**

⚠ **a 의 실측값도 우리에게 있다**: `db/properties/modelc_box331_c2b_hops_2026_09_15.json` 의
`hop_dist_mean_A` = **3.27–3.31 Å (600 K) / 3.62–3.65 (800 K) / 4.00–4.02 (1000 K)**.
**온도에 따라 22 % 움직인다.** 1000 K 에서 a = 3.0 을 쓰면 N_eff 를 **1.78배 과대계상** → RSD 가
**25 % 낙관**이 된다. ⇒ **a 는 계·온도별로 선언하고 그 선택을 적어야 한다.**
(단 `hop_dist_mean` 은 케이지 전이 사이의 순 변위이지 자리–자리 간격의 직접 측정은 아니다.)

### 7-D. 🎯【질문 4】 **우리 런에 오차막대를 붙일 수 있나 — 판정: 가능하다 (조건부)**

#### ① 필요한 입력이 전부 `msd.json` 에 있는가 → **있다.**

`disorder_ensemble_diffusion.py:267–269` 가 쓰는 `msd.json` 스키마 (`코드 실측`):
```json
{"T_K":…, "D_Li_cm2_s":…, "times_ps":[…], "msd_Li_A2":[…], "fit_window_ps":[2,50],
 "times_ps_mto":[…], "msd_Li_A2_mto":[…], "n_origins_mto":[…], "n_Li": 27, "D_Li_cm2_s_mto":…}
```
| He 가 요구하는 것 | 우리 파일의 필드 | 있나 |
|---|---|---|
| `N_mobile` | **`n_Li`** (`extra`, `:158`) | ✅ |
| `max(MSD)` | **`max(msd_Li_A2)`** (단일원점 전 구간) 또는 `max(msd_Li_A2_mto)` | ✅ |
| `a` | ❌ **없다** | 🔴 **선언 필요** |
| 온도·원자수·궤적길이 | 쓰지 않는다 (`run_meta.json` 의 `n_atoms`·`supercell` 은 불필요) | — |

⇒ **한 줄만 추가하면 된다**: `msd.json` 에 **`site_distance_A`** 와, 이왕이면
**`n_eff = n_Li * max(msd)/a²`**, **`rsd_D_he2018`** 를 같이 기록한다.
(⛔ 새 파일 만들지 말 것 — `tools/ionic/msd_diffusive_check.py` 가 이미 `msd.json` 을 읽고
`MSD_MIN_A2`·`D_HOP_A` 를 갖고 있으므로 **플래그 하나(`--rsd`)로 붙이는 것이 맞다.**
우리 §코드 규율 사다리 ③.)

**어느 MSD 를 쓸 것인가 — 주의**: He 의 `max(msd)` 는 **lag ≈ t_tot** 의 값이고 그 lag 에는 원점이
1개뿐이라 **사실상 단일원점 총변위**다. ⇒ 우리 **`msd_Li_A2` 의 마지막 값**이 He 와 같은 뜻이다.
우리 MTO 곡선은 lag 를 t_tot/2 로 자르므로 `max(msd_Li_A2_mto)` 를 쓰면 **N_eff 를 절반쯤 과소평가**
(⇒ RSD 과대 = 보수적)한다. **둘 중 무엇을 썼는지 반드시 적는다.**

#### ② AIMD 전제를 MLIP-MD 에 옮겨도 되는가 → **식은 깨지지 않지만, 검증 범위를 벗어나면 깨진다.**

논문이 직접 허용한다: *"our analyses, schemes, and conclusions are **applicable for diffusional
studies using classical MD**"*, 그리고 `Fig. 4`b 가 실제로 **LLZO 고전 MD** 다.
식 (8)의 유도에는 ab initio 적인 것이 **하나도 안 들어간다** — 전부 홉 통계다. ⇒ **MLIP-MD 에 이식 가능.**

🔴 **그런데 `Fig. 4` 를 직접 보니 검증 범위가 좁다** (§5 실독):
- **(a) AIMD: N_eff ≈ 10–265 만.**
- **(b) 고전 MD: N_eff ≈ 150–5800, 그리고 N_eff ≳ 1200 부터 데이터가 선 위로 뜨면서
  RSD 가 ≈0.10–0.11 에서 평탄해진다.**
⇒ **이 논문 어디에도 RSD < 0.10 인 실측이 없다.** `B = 0.04` 바닥은 **(a) 적합의 외삽**이다.

#### ③ 실제 적용 — **(우리 유도, 논문 미보고)**

**(가) 62원자 · 200/100 ps 사다리** (`db/properties/msd_3sys_200ps_origin.csv`, a = 3.0, n_Li 27/27/58):

| 계 | 600 K | 800 K | 1000 K |
|---|---|---|---|
| modelc | N_eff 409 · **RSD 21 %** | 438 · **20 %** | 806 · **16 %** |
| lpsocl | 302 · **24 %** | 769 · **16 %** | 1759 · **12 %** |
| b2o3 | 784 · **16 %** | 888 · **16 %** | 2011 · **12 %** |

이 RSD 를 식 (7–9) 절차(가중 + `absolute_sigma=True`)로 3점 아레니우스에 넣으면:

| 계 | **He 닫힌형 σ(Ea)** | **우리 멀티시드 실측 ±** | 비 |
|---|---|---|---|
| **modelc** | **0.0342 eV** | **0.032 eV** (3시드, canonical) | ✅ **1.07배 — 사실상 일치** |
| **lpsocl** | **0.0336 eV** | 0.024 eV (4시드, provisional) | ⚠ He 가 1.4배 비관 |
| **b2o3** | **0.0258 eV** | 0.034 eV (3시드, retracted) | ⚠ He 가 0.76배 낙관 |

🎯 **modelc 에서 0.0342 vs 0.032 — 시드를 하나도 더 안 돌리고 우리 3-시드 오차막대를 7 % 안에서
재현했다. 이것이 판정의 근거다.** 세 계 전체로 봐도 He 0.026–0.034 vs 실측 0.024–0.034 로 **같은 띠**다.

**(나) box331 · 558원자 · 400 ps** (n_Li **243**, `lpsocl_box331_c2_mto_2026_09_11.json` 의
`hops_msd_ub` = MSD(200 ps lag)/9 = 15.5 / 37.6 / 66.1 per Li):

| | 600 K | 800 K | 1000 K |
|---|---|---|---|
| N_eff | **3766** | **9137** | **16062** |
| **RSD_He** | **9.6 %** | **7.6 %** | **6.7 %** |
| **modelc 실측 시드 CV** | **1.71 %** (n=3) | **2.54 %** (n=5) | **2.23 %** (n=5) |
| **He / 실측** | **5.6배** | **3.0배** | **3.0배** |

그리고 σ(Ea):

| 추정 방식 | lpsocl box331 | modelc box331 |
|---|---|---|
| **He 가중 · `absolute_sigma=True` · 단일런** | **0.0151 eV** | **0.0151 eV** |
| He 식 σ / √n_seed → CI95 반폭 (n≈3) | **0.0171 eV** | 0.0132 eV (n=5) |
| 무가중 3점 회귀 σ (dof=1) | 0.0063 | 0.0079 |
| 가중 + `absolute_sigma=False` | 0.0069 | 0.0087 |
| **우리 레지스트리 등록 ±** | **0.0018** | **0.003** |

🔴 **우리 box331 ± 는 He 의 단일런 σ(Ea) 보다 5–8배 작고, 같은 3점의 순진한 회귀 σ 보다도
2–4배 작다.** 다만 **레지스트리가 이미 정직하게 적어 놨다** —
`uncertainty_kind: "seed-resampling CI95 half-width … **장시간 극한 오차가 아니다**"`.
⇒ **오표기는 아니다. 그러나 `0.180 ± 0.002 eV` 라는 형태로 나가면 읽는 사람은 그걸 Ea 의
불확실도로 읽는다.** §8-2 의 처방을 따른다.

**두 갈래 해석 — 둘 다 이름을 붙여 둔다 (아직 판정 불가)**
- **(가설 A) He 가 우리 영역에서 비관적이다.** `Fig. 4`b 의 바닥 0.10 은 LLZO 의
  *sparse cyclic excitation*(본문 ref 37 Burbano) 같은 계 고유 구조 이질성일 수 있다.
- **(가설 B) 우리 시드가 덜 흩어져 있다.** He 의 부분런은 **하나의 긴 궤적을 겹치지 않게 자른 것**이라
  블록마다 **느린 자유도(음이온 배열·Li 자리 점유 패턴)가 다르다.** 우리 시드는
  **같은 이완 구조 · 같은 `d0.00_cfg0` 에서 Langevin 난수만 바꾸고 5 ps 평형화**한다 ⇒
  **느린 자유도가 시드 간에 동결돼 있을 수 있다.** 그러면 시드 산포는 진짜 분산의 하한이다.
- 🎯 **가르는 시험이 싸다**: 보관된 box331 400 ps 궤적 **하나**를 겹치지 않는 100 ps 블록 4개로
  쪼개 블록 간 D 산포를 잰다. **계산 0.** 블록 CV ≫ 시드 CV 면 **가설 B**, 비슷하면 **가설 A**.
  (He 가 `Fig. 3a`·`Fig. 4` 를 만든 방법 그 자체다.)

#### ④ **판정**

> ✅ **가능하다.** `msd.json` 의 `n_Li` 와 `msd_Li_A2` 만으로 `N_eff` → `RSD(D)` → (가중적합으로)
> `σ(Ea)` 가 **시드를 더 안 돌리고** 나온다. 필요한 추가 입력은 **`a` 하나**이고, 우리는 그것을
> 이미 `D_HOP_A = 3.0` 으로 갖고 있으며 `hop_dist_mean_A` 로 계·온도별 실측값도 있다.
> 62원자 200 ps 계보에서는 **우리 3-시드 실측과 7 % 안에서 일치**해 검증됐다.
>
> ⚠ **조건 셋 — 이걸 안 지키면 조용히 틀린다**
> 1. **He 값은 "통계 바닥"이지 "총 불확실도"가 아니다.** 모델오차(UMA)·유한크기·무질서 배열·
>    열욕 선택은 **하나도 안 들어간다.** 우리 σ·D 절대값 인용금지는 그대로다.
> 2. **N_eff ≳ 2000 은 `Fig. 4` 의 검증범위 밖**이고, 그 근처에서 논문 자신의 데이터는
>    RSD ≈ 0.10 에서 멈춘다. **box331 급에 붙이는 숫자는 "외삽"이라고 적는다.**
> 3. **시드 평균의 오차로 쓸 때는 √n 을 나누되**, 가설 B 가 살아 있는 동안은
>    **시드 CI 와 He 바닥을 *함께* 보고**한다. 한쪽만 쓰지 않는다.

### 7-E. 【질문 5】 시드 vs 긴 단일 런 — 논문은 어느 쪽인가

**답: 논문은 "더 길게, 그리고 더 크게" 를 권하고, 독립 시드를 권하지 않는다. 그런데 그 이유가
우리와 충돌하지 않는다 — 재는 양이 다르다.**

논문 축자:
> *"one should run **longer MD simulations** that sample more diffusion events, i.e., have larger Neff."*
> *"In addition to running longer MD simulations, running MD simulations on **larger systems with more
> mobile ions** … can achieve more effective ion hops Neff and hence less statistical variance."*

⇒ 식 (8)의 세계관에서 **시간과 이온 수는 등가**다. 둘 다 N_eff 를 사는 통화다.
그리고 σ_D 를 **측정한 방법 자체**가 *"dividing a long MD simulation into several non-overlapping
shorter MD simulations"* — **독립 시드가 아니라 시간 블록**이다. **"독립 시드"라는 말이 논문에 없다.**

| | He 2018 | 우리 (SEMIFINAL 2026-07-09, 단일시드 1.33× 철회) |
|---|---|---|
| 분산의 출처 | **홉 수 하나** | 시드(열욕 난수) + 무질서 배열 + 셀 |
| 측정 방법 | **한 궤적의 시간 블록** | **독립 시드 반복** |
| 처방 | 길게 · 크게 | **멀티시드 판정 필수** |

**판정: 반대가 아니라 직교다. 그리고 He 는 우리 규율을 대체하지 못한다.**
- He 의 모형은 **환원 가능한(N_eff 로 줄일 수 있는) 분산**만 기술한다.
- 우리 무질서 앙상블·유리 담금질 시드는 **N_eff 로 줄지 않는 구조 분산**을 잰다.
- 🟢 **그래서 둘을 합치면 새 도구가 된다**: **He 의 RSD 를 귀무모형(null)으로 놓고, 시드 산포가
  그 위로 넘치면 그 초과분이 구조/모델 분산이다.** 우리 `beta_null_test.py` 의 귀무모형 사고를
  D 에 그대로 옮긴 것이고, `kb/concepts/beta-gate.md` §7-5(b) 가 이미 *"시드 산포를 예측하는 건
  β 가 아니라 홉 수(Spearman −0.78)"* 라고 **우리 데이터에서 He 를 재현**해 놓았다.
- ⚠ 단, §7-D③ 가설 B 가 사실이면 **우리 시드 산포가 He 바닥보다 작게 나오는 비정상**이 되고,
  그건 "우리 계가 깨끗하다" 가 아니라 **"우리 시드가 같은 곳을 본다"** 는 경보다.

### 7-F. 【질문 6】 아레니우스 점 개수·온도 간격 — 우리 3점이 충분한가

**He 가 실제로 한 것** (`Fig. 6` 실독 + `D_T.csv`):
- **9점 · 600–1500 K** · **Δ(1/T) ≈ 1.0×10⁻³ K⁻¹**
- 점마다 식 (8)(9)의 **오차막대**를 붙이고 **1/Var(log D) 로 가중**
- 저온 점이 **덜 신뢰되므로 가중치를 낮춘다** — *"these lower-temperature data points should have
  less weight in the fitting"*
- **점을 늘리는 것이 도움**: *"To minimize the error of Ea and extrapolated σ, **more data points are
  helpful**"* + `Table S1` 이 그 반례를 정량화(§3-B: 2점 빼면 Ea 60 meV·σ 6.4배 변동)

**우리와 나란히 놓으면**

| 항목 | He 2018 | 우리 | 판정 |
|---|---|---|---|
| 점 개수 | **9** | **3** | 🔴 **우리가 적다** |
| 온도 범위 | 600–1500 K | 600–1000 K | 🔴 |
| **Δ(1/T)** | **1.00×10⁻³** | **0.667×10⁻³** | 🔴 **지렛대 1.5배 짧다** |
| 가중 | **1/Var(log D)** | **무가중** (`arrhenius_compat.py` *"3점 무가중 ln D 적합"*) | 🔴 **다르다** |
| 점별 오차막대 | **식 (8)로 항상 붙인다** | **없다** (시드 재표본만) | 🔴 |
| 점 제거 | `Table S1` 로 영향 정량화 | **금지** (C3: *"점을 빼고 다시 적합하지 않는다"*) | ✅ **우리가 낫다** |

**🟢 가중을 도입해도 우리 값은 안 움직인다 — 내가 계산했다 (우리 유도, 논문 미보고)**

| 계 | 현재 무가중 Ea | He 가중 Ea | 이동 |
|---|---|---|---|
| modelc box331 | **0.1690** | 0.1706 | **+1.6 meV** |
| lpsocl box331 | **0.1804** | 0.1817 | +1.3 meV |
| modelc 62원자 | **0.1971** | 0.1959 | −1.2 meV |

⇒ **가중은 점추정을 거의 안 바꾸고 오차막대만 바꾼다.** 채택 비용이 사실상 0 이다.

**⚠ 3점의 구조적 한계 — 내 계산이 드러낸 것**: 같은 RSD 로 **600/1000 K 2점만** 써도
σ(Ea) 가 modelc 0.0342 → **0.0342**, b2o3 0.0258 → **0.0258** 로 **바뀌지 않는다.**
⇒ **우리 800 K 점은 σ(Ea) 를 거의 못 줄인다.** 그 점의 가치는 **정밀도가 아니라 선형성 검증**
(= 우리 C3 구간 Ea 양립성 판정)에 있다. **그 역할로만 말해야 한다.**

**그리고 He 의 오차이론은 `ArreheniusAnalyzer` 의 두 갈래(§6-D) 때문에 구현 의존적이다** —
`absolute_sigma` 한 글자가 box331 에서 **0.0151 vs 0.0087 (1.7배)** 를 가른다.
**우리가 채택한다면 `absolute_sigma=True` 를 명시하고 그 뜻(*"점별 σ 의 전파이지 선 적합도가 아님"*)을
카드에 적는다.**

**저온(400/500 K) 제외 판정과의 관계 — 🔴 우리에게 불리한 부분이 있다.**
`kb/methodology/md_conductivity_protocol.md` §3 의 제외 사유 셋 중 ①(저온 잡음)만 He 가 건드린다.
He 의 `Fig. 5` 기준 **Ea 0.2 eV 는 450 K 까지 RSD 20 % 로 접근 가능**하고, 그건 *20 이온 · 1 ns*
기준이다. 우리 box331 은 **243 Li · 400 ps** 다. 외삽하면 — **(우리 유도, 논문 미보고)**

| T | 추정 D | MSD(200 ps lag) | N_eff | **RSD_He** |
|---|---|---|---|---|
| 500 K | ≈7.2×10⁻⁶ cm²/s | ≈87 Å² | ≈2343 | **≈11 %** |
| 400 K | ≈2.7×10⁻⁶ | ≈33 Å² | ≈878 | **≈16 %** |

⇒ **"홉이 모자라서 400/500 K 를 뺀다" 는 He 기준으로 성립하지 않는다.**
⚠ **다만 He 는 다른 이유를 준다**: 400 K 에서 MSD 가 **4.5 Å² 를 넘는 시각이 ≈15 ps** 로 밀리므로
**(2,50) 창의 앞 1/3 이 He 기준 비확산 구간**이 된다. ⇒ **제외 사유를 "통계 부족"이 아니라
"창 규약 붕괴 + 창 재설계 필요"로 고쳐 적는 것이 정직하다.** (제외 사유 ②③ 은 He 와 무관하게 유효.)

### 7-G. 【질문 7】 소셀 유리 MD 카드 — 지지인가 반박인가

대상: `db/properties/lpscl_smallcell_glass_md_estimand_2026_09_21.json`
(a-Li₄PS₄Cl **120원자** Li₄₈P₁₂S₄₈Cl₁₂ · L = 13.98 Å · **400/465/550 K · 5 구조시드 · 400 ps** ·
보고량 = **N_pass/15 와 Ea 의 시드 간 IQR**).

**🟢 지지하는 것 (4건)**
1. **점별 오차막대를 요구하는 정신 자체.** 결론 3–4 가 *"통계 분산을 보고하라"*, *"각 점의
   불확실도를 아레니우스 적합에 넣어라"* 다. 카드가 Ea 절대값 대신 **산포**를 보고량으로 잡은 것은
   같은 방향이다.
2. **Δ(1/T) = 0.682×10⁻³ 선택 = 정확히 He 가 강조하는 축.** He 는 *"more data points are helpful"*
   과 `Table S1`(점 제거 → Ea 60 meV) 로 **지렛대의 중요성**을 정량화했다. 1저자가
   *"k 가 너무 가까우면 값이 오염된다"* 로 잡아낸 지점이 He 의 축과 같다. ✅
   ⚠ 다만 **He 의 0.682e-3 도 그의 1.0e-3 보다 32 % 짧고 점은 3개 vs 9개**다 — **지지는 방향뿐,
   충분성은 아니다.**
3. **셀 120원자 · 1×1×1 유지.** He 의 통화는 N_eff = N_mobile × MSD/a² 이고 **48 Li 는 그의
   예시 모델(20 이온)의 2.4배**다. 셀을 안 키우는 대신 **400 ps** 로 시간을 사는 설계는
   He 의 *"시간과 이온 수는 등가"* 와 정합한다.
4. **시드 5개.** He 는 시드를 안 권하지만, **유리는 He 의 모형 밖**이다(구조 분산이 N_eff 로 안 준다).
   카드가 *"시드를 풀링해 하나의 MSD 로 합치지 않는다"* 고 못박은 것은 He 가 못 재는 축을
   따로 잡은 것이라 **He 를 보완**한다.

**🔴 반박하는 것 / 경고하는 것 (3건 — 전부 우리에게 불리하다)**
1. 🔴🔴 **C1 게이트(MSD ≥ 3 Å²)가 He 기준 사용불가 영역이다.**
   48 Li · a = 3.0 → **N_eff = 48 × 3/9 = 16** → **RSD(D) ≈ 90 %.**
   He 의 `Fig. 4`a 에서 N_eff ≈ 16 은 RSD ≈ 0.9–1.0 인 **맨 왼쪽 끝**이다.
   ⇒ **C1 을 간신히 통과한 런의 D 는 오차 90 % 다.** 목표 RSD 별 필요 MSD/Li (a=3, 48 Li):

   | 목표 RSD | 필요 N_eff | 필요 **MSD/Li** |
   |---|---|---|
   | 50 % | 56 | **10.4 Å²** |
   | 40 % | 91 | **17.0 Å²** |
   | **30 %** | 174 | **32.6 Å²** |
   | 25 % | 267 | **50.0 Å²** |
   | 20 % | 460 | **86.2 Å²** |

   ⇒ **카드에 "He 기준 RSD 환산" 열을 추가하고, C1 을 통과해도 RSD 가 50 % 를 넘는 런은
   'N_pass' 에 세되 별도로 표시**하는 것이 정직하다. (⛔ **문턱을 결과 보고 바꾸지 않는다** —
   카드 §4 의 봉인 규칙 대로, 이건 **새 보고열 추가**이지 문턱 변경이 아니다.)
2. ⚠ **550 K 상한 근거(감김 한계 (d/2)² = 48.88 Å²)와 He 의 요구가 정면으로 부딪힌다.**
   He 기준 RSD 30 % 에 필요한 MSD/Li 는 **32.6 Å²** 이고, 감김 한계는 **48.88 Å²** 다.
   ⇒ **둘 사이 창이 32.6–48.9 Å² 밖에 안 된다.** 400 ps 안에 그 사이로 들어와야
   *"쓸 만한 D"* + *"감김 없음"* 이 동시에 선다. **매우 좁다.** 파일럿에서 이 값을 꼭 본다.
   (⚠ He 의 max MSD 는 lag ≈ t_tot 의 값이고 감김 한계는 **적합 창 끝(50 ps)** 의 값이라
   **같은 lag 가 아니다** — 두 수를 한 칸에 적을 때 lag 를 반드시 병기한다.)
3. ⚠ **He 의 식은 결정질 초이온전도체 4계 + 결정질 고전MD 1계에서만 적합됐다. 유리는 없다.**
   유리는 (i) a 가 잘 정의되지 않고 (ii) 느린 α-완화 때문에 D 자체가 시간의존적일 수 있다.
   ⇒ **유리에 식 (8)을 쓰면 "참고 바닥"으로만 쓰고, a 를 무엇으로 잡았는지(=3.0 가정) 반드시 적는다.**

**한 절 요약**: **설계의 온도 3점·시드 5·400 ps·120원자는 He 가 지지한다. 반면 C1 문턱은
He 기준 사용불가선(RSD 90 %)이라 "통과"가 "쓸 만함"을 뜻하지 않는다 — 카드에 RSD 환산열을 붙여야
한다. 그리고 550 K 상한과 RSD 30 % 요구 사이의 여유가 32.6–48.9 Å² 로 매우 좁다.**

### 7-H. 그 밖에 직접 부딪히는 것 3건

| 항목 | He 2018 | 우리 | 판정 |
|---|---|---|---|
| **골격 드리프트 차감** | **한다** (`diffusion.py:66–68`, 비이동 원자 평균 변위를 뺀다) + **drift > 3 Å**·**골격변위 > 5 Å(용융 의심)** 경고 | **안 한다.** `li_diffusion_from_frames` 에 드리프트 항이 없다. COM 은 **ASE `Langevin(fixcm=True)` 기본값**에 의존 | ⚠ **숨은 의존성.** `fixcm` 은 **ASE 3.28.0 부터 deprecated, 제거 예정**이고 *"does not strictly sample the correct NVT distributions"* 경고가 붙는다. 내 추정(우리 유도): 62원자 LPSCl 600 K 에서 COM 이 풀리면 `D_com = kT/(Mγ) ≈ 2.0×10⁻⁵ cm²/s` → **MSD_com(50 ps) ≈ 59 Å²** — 우리 Li MSD(50 ps) ≈ 33 Å² **보다 크다.** ⇒ **기계별 ASE 버전을 확인하고, He 식 드리프트 차감을 명시적으로 넣는 편이 안전하다** |
| **"용융/골격 붕괴" 자동 경고** | **있다** (5 Å) | 별도 게이트 C6(골격 census)로 **사후** 판정 | 🔵 우리 C6 가 더 정교하나 **MSD 계산 시점에 경보가 없다.** b2o3 음이온 골격 creep 이 이 경고에 걸릴 종류 |
| **Haven / N 세기** | 식 (6)이 **σ 는 carrier 세기와 무관**함을 보임. Haven 오차는 **미제공** | NE · Haven=1 가정 · 실측 `H_R = 0.84 ± 0.06` (citable:false) | ✅ **"σ 절대값 비인용" 규율에 유리.** He 스스로 tracer↔jump 분리를 인정하면서 `D_J` 분산은 못 줬다 |

---

## 8. 적용 인사이트 — **지금 할 수 있는 것 5가지**

1. **`msd_diffusive_check.py` 에 `--rsd` 플래그를 붙인다** (새 파일 금지 — 우리 사다리 ③).
   `msd.json` 의 `n_Li` × `max(msd_Li_A2)` / `a²` → `N_eff` → `RSD = 3.43/√N_eff + 0.04` 를
   기존 표에 열 두 개(`N_eff`, `RSD_he18`)로 추가. `a` 는 `D_HOP_A = 3.0` 기본 + `--site_distance` 로 덮기.
   **selftest 에 음성경로 포함**: (i) `n_Li` 누락 → 시작하지 않음 (ii) `a ≤ 0` → 거부
   (iii) 저장소 단언값 `n_jump = 100.488 → RSD = 0.382165` 재현.
   ⛔ **판정 게이트로 쓰지 않는다** — 처음엔 **보고열**로만.
2. **레지스트리 표기를 두 칸으로 바꾼다.** `0.180 ± 0.002 eV` 하나로 나가면 안 된다 →
   **`0.180 eV · 시드재표본 CI95 ±0.002 · 통계바닥(He18) ±0.015(단일런)`**.
   `uncertainty_kind` 가 이미 *"장시간 극한 오차가 아니다"* 라고 적어 뒀으니 **화면에 실리게만 하면 된다**
   (우리 §화면·claim 결속 규율: *"규율이 원장에만 있고 화면에 안 실리면 사람은 화면을 인용한다"*).
3. 🎯 **블록 분해 시험 — 계산 0, 판정 2개를 동시에 준다.**
   보관된 box331 400 ps 궤적 하나를 **겹치지 않는 100 ps 4블록**으로 쪼개 블록별 D 를 낸다.
   ① 블록 CV vs 시드 CV → §7-D③ 의 가설 A/B 판정.
   ② 같은 궤적에 **He 창 규칙**을 적용해 Ea 가 §7-A 처럼 흔들리는지 확인 → gen0 에서 본
   ±26–43 meV 가 gen2 에서도 살아 있는지.
   ⛔ **결과를 보고 창을 바꾸지 않는다** — 흔들림의 크기를 **기록**하는 것이 목적이다.
4. **`a` 를 계·온도별로 선언한다.** `hop_dist_mean_A` (3.27 / 3.64 / 4.01 Å @600/800/1000 K)를
   근거로, `a = 3.0` 고정을 계속 쓸지 온도별로 쓸지 **결정하고 적는다.** 고정을 유지한다면
   *"1000 K 에서 RSD 가 ~25 % 낙관"* 이라는 단서를 붙인다.
5. **아레니우스 가중을 도입한다** — 점추정이 ±1.6 meV 밖에 안 움직이므로(§7-F) **기존 값이
   흔들릴 위험 없이** 오차막대만 정직해진다. `arrhenius_compat.py` 에 `--weights he18` 옵션.
   `absolute_sigma=True` 를 **명시**하고 그 뜻을 카드에 적는다.

---

## 9. 인용 가능 문장 (영문 초안)

> The statistical uncertainty of a diffusivity extracted from an MD trajectory is governed by the
> number of diffusion events sampled rather than by the goodness of the Einstein-relation fit; He
> *et al.* quantified this as RSD(D) = 3.43/√N_eff + 0.04, where N_eff = max_Δt[TMSD(Δt)]/a² is the
> total effective number of ion hops.[He2018]

> Following the procedure of He *et al.*, the linear fit to the Einstein relation was restricted to
> the diffusive region of the MSD–Δt curve, excluding the ballistic region (MSD ≲ a²) and the
> poorly-sampled region at large Δt (Δt > 0.7 t_tot), and a free intercept was retained.[He2018]

> He *et al.* showed that for typical fast-ion conductors the statistical error bound on the
> room-temperature conductivity extrapolated from an Arrhenius fit can span one to two orders of
> magnitude even when many temperatures and long trajectories are used.[He2018]

⛔ **쓰면 안 되는 문장**
- *"He et al. validated this error formula for machine-learning potential MD"* — **고전 MD 1계(LLZO)
  뿐이고 MLIP 는 0회.**
- *"…so the RSD of our D is X %"* — **He 식은 통계 바닥이지 총 불확실도가 아니다.** 모델오차·
  유한크기·무질서 배열이 전부 빠져 있다.
- *"He et al. recommend a fixed 2–50 ps fitting window"* — **He 의 하한은 시간이 아니라 변위다.**
- *"…error bars below 10 % are supported by He et al."* — **`Fig. 4` 에 RSD < 0.10 인 실측이 없다.**

---

## 10. 주의 / 한계 — 비판적으로

1. 🔴 **식 (8)은 법칙이 아니라 구름 속 적합선이다.** `Fig. 4`a 실독: N_eff ≈ 180 에서 데이터 0.19 vs
   선 0.30 (**상대 −37 %**). 개별 점이 ±30–40 % 벗어난다. **식이 주는 RSD 자체에 ±35 % 불확실도가 있다.**
   논문은 이 산포를 정량화하지 않고 *"general for ionic conductor materials"* 라고만 쓴다.
2. 🔴🔴 **`B = 0.04` 바닥에 실측 근거가 없다.** 적합은 `Fig. 4`a(N_eff ≤ 265)에서 하고, 거기서는
   `A/√N_eff` 가 0.21 이상이라 **B 가 사실상 안 보인다.** 그런데 정작 큰 N_eff 를 보여주는
   `Fig. 4`b 에서는 데이터가 **0.10–0.11 에서 평탄**해져 선(0.088)을 넘어선다.
   ⇒ **B = 0.04 는 어느 데이터에도 지지되지 않는 외삽값이고, 큰 N_eff 에서 식은 낙관적이다.**
   우리처럼 N_eff 10⁴ 급에서 쓰려면 **반드시 경고를 달아야 한다.**
3. 🔴 **0.7 t_tot 에 무릎이 없다.** `Fig. 3`b 는 R² 가 1.000 → 0.947 로 **매끄럽게** 내려간다.
   0.7 은 *"significantly decrease"* 라는 말로 그어진 선이고, 진짜 신호(오차막대 폭증)는
   정량화되지 않았다. 게다가 **코드 기본값은 0.5** 라 **논문과 구현이 다른 수를 쓴다.**
4. 🔴 **`a` 가 정의되지 않은 계에서 식이 무너진다.** 비정질·다중경로·케이지 내/간 홉이 섞인
   아르지로다이트에서 *"이웃 자리 간 평균 거리"* 는 하나가 아니다. 논문은 네 계의 a 를 **값만 주고
   어떻게 정했는지 안 적는다.** `N_eff ∝ 1/a²` 이므로 이건 큰 자유도다.
5. ⚠ **`max(MSD)` 를 적합에서 잘라낸 구간에서 가져오는 자기모순.** Δt_up 을 두는 이유가
   *"큰 Δt 는 원점이 적어 시끄럽다"* 인데, N_eff 는 그 구간의 **최댓값**을 쓴다.
   잡음이 있는 양의 최댓값은 **위로 치우친 추정량**이라 **N_eff 가 과대 → RSD 가 낙관**이다.
6. ⚠ **가중·비가중 갈래의 의미 차이를 논문이 안 적는다** (§6-D). `absolute_sigma` 한 글자가
   우리 box331 에서 σ(Ea) 를 **1.7배** 가른다. SI Note 2 는 *"weighted linear least squares"* 까지만 말한다.
7. ⚠ **`Table 1` 의 오차범위가 자기 코드 때문에 1.51배 부풀어 있다** (§6-H, 내 검산).
   *"standard error analysis for linear regression"* 이라고 적었지만 **공분산 항을 뺀 비표준 계산**이다.
8. ⚠ **계산 설정 표가 없다.** ecut·원자 수·슈퍼셀·평형화 시간이 본문·SI 어디에도 없다.
   *"AIMD 설정을 He 2018 을 따랐다"* 고 쓸 근거가 이 논문에 없다.
9. ⚠ **무질서를 단일 Ewald-최저 배열로 처리**(refs 5, 7 승계)하고, **그 선택이 D 에 주는 분산은
   이 논문의 분산 체계에 전혀 안 들어간다.** 우리 무질서 앙상블 축과 직접 충돌하지는 않지만,
   *"He 의 RSD 가 총 불확실도"* 로 읽으면 **무질서 분산을 0 으로 세는 것**이 된다.
10. ⚠ **thermostat.** METHODS 는 Nosé–Hoover 라 적는데 저장소 샘플 INCAR 은 **`SMASS=-1`
    (속도 스케일링)** 이다(§6-I). 샘플이 다른 계용일 수 있으나 **재현하려는 사람에게는 모순 신호**다.
11. ⚠ **코드가 py2 전용**이고 전도도 경로는 py3 에서 죽는다(§6-E④). *"코드를 공개했다"* 와
    *"코드가 돈다"* 는 2026년 기준 다른 말이다.
12. ⚠ **`Fig. 6` 의 Arrhenius 는 9점인데 `Table 1` 은 ±만 준다** — 각 점의 D 값 표가 본문에 없다.
    (저장소 `D_T.csv` 가 **LLZO 것만** 준다. LATP·LGPS 원자료는 여전히 없다.)

---

## 11. ⛔ 이 논문이 못 하는 것 / 내가 확인 못 한 것

**논문이 못 하는 것**
- **아르지로다이트 0회.** Li₆PS₅X 는 본문·SI·참고문헌 어디에도 없다.
- **MLIP 0회.** 고전 MD 는 LLZO 1계(Adams–Rao 경험퍼텐셜)뿐.
- **비정질/유리 0회.** 전부 결정질.
- **`D_J`(점프확산)·Haven 비의 분산을 못 준다** — 본문이 스스로 미뤘다.
- **모델(퍼텐셜·범함수) 오차를 한 글자도 다루지 않는다.** 전부 샘플링 통계다.
- **유한크기 효과를 다루지 않는다.** N 을 늘리면 N_eff 가 늘어 좋다고만 하고, 셀 크기가 D 자체를
  바꾸는 문제(우리 box331 t13: 셀이 D 를 1.79배 움직였다)는 논의에 없다.
- **비정상확산(sub-diffusion) 진단이 없다.** β 나 `D_inc` plateau 에 대응하는 것이 없고,
  창을 자르는 것으로 대체한다.

**내가 확인 못 한 것 — 정직하게**
- **SI 그림 `Fig. S1`–`Fig. S5` 의 이미지를 못 봤다.** docx 에서 **캡션과 본문만** 텍스트로 뽑았다
  (`word/media` 를 덤프하지 않았다). 특히 **`Fig. S3`(LGPS·LLZO 의 0.7 t_tot 일반성 근거)** 와
  **`Fig. S2`(D 히스토그램의 모양 — 정규인지 치우쳤는지)** 를 못 봤다.
  ⇒ *"0.7 이 LGPS·LLZO 에서도 확인됐다"* 는 **논문의 주장으로만** 인용한다.
- **`tab_1.png` / `tab_S1.png` 를 이미지로 안 봤다** (의도적 — 텍스트가 정확하다).
- **`Fig. 4` 의 개별 점 좌표는 판독값**이다. 저자가 표로 주지 않았다.
- **저장소 코드를 실행하지 못했다** — 이 컨테이너에 `pymatgen` 이 없다. 대신
  `ArreheniusAnalyzer`·`get_conversion_factor`·`ErrorAnalysis` 를 **scipy/numpy 로 재구현해
  테스트 단언값을 전부 재현**했다(§6-G). `DiffusivityAnalyzer` 의 FFT MSD 경로는
  **코드 독해로만** 확인했고 실행 대조는 못 했다.
- **`aimd/tests/test_files/latp_md/RUN_10…29` 의 vasprun 을 열지 않았다** — 거기서 원자 수·
  슈퍼셀·실제 AIMD 파라미터를 캘 수 있었을 텐데 못 했다. **다음 사람이 할 일로 남긴다.**
- **우리 box331/유리 런의 실제 `msd.json` 을 못 읽었다** — repo 에 없다(원격 기계에 있다).
  §7-D 의 box331 수치는 `db/properties/*.json` 에 전사된 요약값(`hops_msd_ub`·시드별 D)에서 유도했다.

---

## 12. 용어 미니 사전 (우리 팀용)

| 용어 | 뜻 | 우리 대응물 |
|---|---|---|
| **TMSD** | Total MSD — **모든 이동이온의 제곱변위 합** (평균이 아니다). `TMSD = N × MSD` | 우리는 TMSD 를 따로 안 쓴다. `msd_Li_A2 × n_Li` 로 만든다 |
| **N_eff** | 총 **유효** 홉 수 `max(TMSD)/a²`. 되돌아오는 홉은 상쇄돼 안 세진다 | `hops_per_ion.py` 의 `n_hop × n_Li`. **정확히 같은 양** |
| **상관인자 f** | (유효 홉)/(실제 홉). 우리 실측 `f ≈ 0.65–0.74` (box331) | `lpsocl_box331_c2b_hops` vs `hops_msd_ub` 비교로 얻었다. ⇒ **식 (8)에는 실제 홉 수가 아니라 MSD/a² 를 넣어야 한다** |
| **RSD** | Relative Standard Deviation = `s_D/D_true`. D 와 σ 에 대해 **같은 값** (선형 관계라) | 우리 시드 CV 와 같은 자리의 양 |
| **ballistic region** | MSD ∝ Δt^α (α>1) 인 초단시간 구간. 자리 안 진동 | 우리 β 게이트가 보는 것의 반대쪽 끝 |
| **Δt_low / Δt_up** | 선형 적합의 하한/상한 lag | 우리 `fit_window_ps = (2, 50)` |
| **`absolute_sigma`** | scipy `curve_fit` 인자. True = 입력 σ 를 절대값으로 믿고 공분산을 **재척도하지 않는다**. False = 잔차로 재척도 | 우리 `np.polyfit` 은 공분산을 안 쓰므로 해당 없음 — **도입하면 True 로** |
| **weighted LSQ** | 각 점을 `1/σ²` 로 가중 | 우리는 **무가중** (`arrhenius_compat.py`) |
| **block/time-slicing variance** | 긴 궤적 하나를 겹치지 않게 잘라 블록 간 산포를 재는 것 | He 의 σ_D 측정법. **우리 시드 산포와 다른 양** |

---

## 13. 교차 참조 (litdb 내부)

| 관계 | 문서 | 내용 |
|---|---|---|
| **후속·상위호환** | `papers/mccluskey2025_accurate_diffusion_coefficients_uncertainties.md` | 같은 질문의 **2025년 정본**. He 가 **경험식 1줄**로 푼 것을 McCluskey 는 **MSD 공분산 행렬 유도 + 베이지안 회귀**로 푼다. ★ **둘은 배타가 아니다** — He 의 RSD 는 *진짜* σ_D 를 (블록 산포로) **보정한 값**이고, McCluskey 가 *"OLS 가 26배 과소평가한다"* 고 지적한 그 OLS σ̂ 과는 **다른 양**이다. ⇒ **He = 빠른 닫힌형 바닥 / McCluskey = 궤적 하나에서 최대 정보.** 우리는 He 부터 붙이고 kinisi 로 간다 |
| **He 를 인용한 편** | `papers/deklerk2018_diffusion_analysis_md_beta_li3ps4.md` §271 | *"짧은 런이 저온 D\* 를 과대평가한다"* 를 **ref 21 = 이 논문**에 위임. **그 위임이 이제 닫혔다** — 근거는 SI Note 3 (§3-E: LLZO 40 ps → Ea −0.07 eV, σ(300) 6배) |
| **같은 축** | `papers/pranami2015_estimating_error_diffusion_coefficients_md.md` · `papers/maginn2019_best_practices_transport_selfdiffusivity_viscosity.md` · `papers/zaby2026_reliable_conductivity_estimates_md.md` | MD 수송량 오차·모범사례 계열 |
| **우리 쪽 원장** | `kb/concepts/beta-gate.md` §7-3/§7-5 | 🔴 **정정 필요.** §7-3 표가 *"He 2018 은 **원칙만 말하고 창을 고정하지 않는다**"* 라고 적었는데 **틀렸다** — 논문은 `0.5a²` 와 `<0.7 t_tot` 을 주고 코드는 `4.5 Å²`·`0.5 t_tot` 을 **박아 놨다**. §7-5-2 의 *"He 2018 원문 확보 ⏳"* 도 **닫혔다** |
| **우리 쪽 원장** | `db/external/PENDING.md` **P3** | ✅ **해소.** *"구체적 수치 기준을 우리가 못 봤다"* → 이제 봤다: `A=3.43 · B=0.04 · 0.5a² · 0.7 t_tot · site_distance 3.0` |
| **우리 쪽 규약** | `kb/methodology/md_conductivity_protocol.md` §3 | 400/500 K 제외 사유 ① 의 문구를 **"통계 부족"에서 "창 규약 붕괴"로** 고치는 것이 정직하다 (§7-F) |
| **진행 중 캠페인** | `db/properties/lpscl_smallcell_glass_md_estimand_2026_09_21.json` | §7-G — C1 문턱의 RSD 환산 열 추가 제안 |

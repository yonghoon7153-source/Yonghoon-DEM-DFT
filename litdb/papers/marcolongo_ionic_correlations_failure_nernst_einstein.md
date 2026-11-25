<!-- digest 표준 양식 (paper-level STANDALONE).
     2026-09-22 신규. 그림 7장(본문 4 + SI 3) **전부 실제 열람** 후 작성.
     ⚠ 크로핑 사고 1건을 고치고 시작했다 — 최초 `litdb/figures/<slug>/` 에 들어 있던 14장은
       **전부 다른 논문**(`10. ACSAMI_2017_Haruyama_…`)의 그림이었다. inbox 파일명이 둘 다
       `10. ` 로 시작해 추출기가 잘못 짝지었다. `--pdf` 로 원본을 명시해 재추출했다. -->

# Ionic correlations and failure of Nernst–Einstein relation in solid-state electrolytes — Marcolongo & Marzari (*Phys. Rev. Materials* **1**, 025402 (2017))

> slug `marcolongo_ionic_correlations_failure_nernst_einstein` · DOI `10.1103/PhysRevMaterials.1.025402` · type `AIMD (Car–Parrinello FPMD) + 선형응답 이론 — 실험 0 · 정적 DFT 물성 0` · PDF `litdb/inbox/10. Ionic_correlations_failure_Nernst_Einstein_SSE_MAIN.pdf` (본문 **4 pp**) + `10. Sup) Ionic_correlations_failure_NE_SI.pdf` (SI **2 pp**) · digested `2026-09-22` · status ✅ · 태그 **[외부·방법 원전]**

> elements: Li, Ge, P, S
> methods: DFT, AIMD, MD

> 🔴 **이 digest 가 1순위였던 이유**: CLAUDE.md 정본이 *"σ 는 Nernst–Einstein(Haven=1)"* 이다.
> 우리 σ 전부가 이 가정 위에 선다. **이 논문이 그 가정을 깨는 축의 원전이다.**
>
> ⛔ **그런데 이 논문은 아르지로다이트를 한 번도 다루지 않는다.** 계는 끝까지 **LGPS Li₁₀GeP₂S₁₂ 하나**다.
> ⇒ **우리 계에서 H_R 을 가정할 근거는 이 논문 뒤에도 여전히 없다.** 자세한 판정은 §7-3.
>
> 🎤 talk 역링크 **해당 없음** — `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` 로 확인한
> 유일한 대기열(`talks/lee2026_skku_mlip_materials_design.md` §99-10, 9건)에 이 논문은 없다.

---

## 0. 이 digest 를 읽는 법 — 무엇을 답하러 왔나

1저자가 이 편에 던진 질문이 6개다. 답이 어디 있는지 먼저 적는다.

| # | 질문 | 답 | 절 |
|---|---|---|---|
| 1 | **H_R 의 값과 부호** | **z 0.36 / xy 0.61 / xyz 0.42** (속도 재규격화 후). **전부 1 보다 작다** ⇒ σ_NE 는 **과소**. 우리 `md.md` §6 과 **같은 방향** | §3 · §7-1 |
| 2 | **상관의 정체** | **같은 종(Li–Li) 속도 교차상관이 양수**. 1D c축 채널의 **협동·일렬 이동**. 별개로 **Li↔골격 역류**(운동량 보존)가 있고 저자가 Eq. (6) 으로 뺀다 | §4-3 · §7-2 |
| 3 | **우리 계에 옮기나** | **⛔ 못 옮긴다.** 계는 **LGPS 하나**, 아르지로다이트 0회. 옮기는 것은 **부호와 방법**뿐 | §7-3 |
| 4 | **어떻게 쟀나** | **Green–Kubo**(속도 자기상관 적분), Einstein 아님. NVE 생산, 블록 분석 오차. 우리 `--haven` 은 **Einstein 경로**지만 **정규화·기준계는 동일** | §5 · §7-4 |
| 5 | **우리가 H_R 을 언제 믿나** | 조건 5개를 §12-1 에 정리. **이 논문은 우리 도구 docstring 의 경고를 *강화*한다** | §12-1 |
| 6 | **물성 4축 편입** | **⛔ 안 넣는다.** `comparison_vs_ours.md` **§J `🔧 방법 원전`** + **§H 한 줄** | §11 |

**그림 열람 실적**: 크로핑 **7장 중 7장 전부 실제로 봤다** (본문 `Fig. 1`·`2`·`3`·`4` + SI `Fig. S1`·`S2`·`S3`).
표는 이 논문에 **번호 붙은 표가 0개**다 — Haven 값 표는 `Fig. 4` **안에 그려진 표**라 그림으로 읽었다.

---

## 1. 한 줄 요약

**초이온 전도체에서 Li 이온들은 서로 상관되어 움직이므로, tracer 확산계수 `D_tr` 로 세운 Nernst–Einstein 식은 이온전도도를 *과소*평가한다.** LGPS 에서 전하 확산계수 `D_σ` 가 `D_tr` 의 **약 2.5 배**로 나오고(Haven 비 `H = D_tr/D_σ ≈ 0.42`), 이 상관은 **가장 빠른 c축에서 가장 강하다**. 단 **활성화에너지는 두 경로가 0.01 eV 안에서 일치**하므로(0.18±0.02 vs 0.17±0.01 eV), *"tracer 로 Ea 는 내도 되고 σ 는 안 된다"* 가 결론이다.

---

## 2. 메타 / 서지 — ⚠ 1저자 지시로 표지에서 직접 확인

**✅ 우리 기록 `PRM 1, 025402 (2017)` 은 정확했다.** 표지 실독으로 대조 완료.

| 항목 | 표지에서 읽은 값 |
|---|---|
| 저자 | **Aris Marcolongo**, **Nicola Marzari** (2인, 교신 표시 없음) |
| 소속 | Theory and Simulation of Materials (**THEOS**) + National Centre for Computational Design and Discovery of Novel Materials (**MARVEL**), **École Polytechnique Fédérale de Lausanne (EPFL)**, CH-1015 Lausanne, Switzerland — 두 저자 공통 소속 하나 |
| 저널 | **Physical Review Materials 1, 025402 (2017)** |
| DOI | **`10.1103/PhysRevMaterials.1.025402`** |
| 날짜 | **접수 2017-01-16 · 게재 2017-07-05** |
| 식별자 | `2475-9953/2017/1(2)/025402(4)` — **4 쪽짜리 Letter 급** |
| 분량 | 본문 **4 pp** (Fig. 1–4, **번호 붙은 표 0개**), SI **2 pp** (Fig. S1–S3, 표 0개), 본문 refs **24** + SI refs **2** |
| 지원 | NCCR MARVEL (Swiss National Science Foundation) |

> ⚠ **이 편은 계산 논문이지만 "DFT 물성 논문" 이 아니다.** 밴드갭·형성에너지·탄성·ESW 를 **하나도**
> 내지 않는다. 내는 양은 **`D_tr`, `D_σ`, `H`, `Ea`** 넷뿐이고 그중 셋이 수송 통계량이다.

### 2b. 논문이 스스로 세운 문제

> *"All previous works took for granted the relation between the tracer diffusion coefficient and the ionic conductivity provided by the Nernst-Einstein equation [7]. With our contribution we aim at showing that this relation is not valid and its application leads to an **underestimation** of the value of conductivity."* (p.1, 좌단)

세 갈래로 답한다.
1. **이론** — `D_tr` 과 `D_σ` 사이의 **새 부등식** `0 ≤ D_σ ≤ N_eff·D_tr` 을 증명한다 (논문이 스스로 *"the first result of this paper"* 라 부른다).
2. **MD 규율** — 주기경계 + 운동량 보존 때문에 **골격(S/Ge/P)이 반대로 흐른다**. 이것을 빼는 속도 재규격화 Eq. (6) 을 제안하고, 그 통계적 크기를 **해석식** Eq. (5) 로 예측해 검증한다.
3. **수치** — LGPS 에서 500 ps FPMD 로 `H` 를 방향별로 잰다.

---

## 3. 핵심 수치 총정리 ★ (전부 소환값 — 우리 db 와 섞지 않는다)

### 3a. 🎯 Haven 비 — `Fig. 4` 오른쪽 아래 표 (이 논문의 헤드라인)

> **규약 (논문 본문 p.1 우단 명시)**: `H = D_tr / D_σ`.
> **우리 규약(`kb/concepts/md.md` §6, `msd_diffusive_check.py`)과 완전히 같다.** 부호 논쟁 없음.

| 방향 | **H_c** (속도 재규격화 **후**, Eq. 6) | **H** (재규격화 **전**) | 실험 [24] |
|---|---|---|---|
| **z** (= c축, 최속 확산 방향) | **0.36** | 0.46 | – |
| **xy** (면내) | **0.61** | 0.79 | – |
| **xyz** (등방 평균) | **0.42** | 0.53 | **~0.3** |

- 실험 비교값 [24] 는 **LGPS 가 아니라 Li₁₀SnP₂S₁₂** 다 (Bron et al., *J. Am. Chem. Soc.* **135**, 15694 (2013)). 논문 표현도 *"the similar material"* 이다. ⚠ **LGPS 실측 Haven 이 아니다.**
- **전부 `H < 1`** ⇒ `D_σ > D_tr` ⇒ **σ_NE (tracer 기반) 는 참값보다 작다**.
- 본문 서술: *"the charge diffusion coefficient shows a value around **2.5 times larger** than the tracer diffusion coefficient"* (p.3). `1/2.5 = 0.40 ≈ H_c(xyz) = 0.42` ✓ 자기정합.
- **재규격화는 항상 H 를 낮춘다** (0.46→0.36, 0.79→0.61, 0.53→0.42). 즉 골격 역류를 빼면 **상관이 더 커 보인다**.

### 3b. 활성화에너지

| 경로 | Ea (eV) |
|---|---|
| **전하** `D_σ` | **0.18 ± 0.02** |
| **tracer** `D_tr` | **0.17 ± 0.01** |

> ⚠ **원문 문장이 모호하다**: *"…also considering the (faster converging) single-particle diffusion coefficient [our computations provide an activation energy of (0.18 ± 0.02) and (0.17 ± 0.01) eV, respectively]"* — `respectively` 의 선행사가 문장에 명시돼 있지 않다.
> **(우리 판독, 논문 미명시)** `Fig. 4` 좌측 아레니우스의 두 점선 기울기를 직접 재면
> **D_σ → Ea ≈ 0.182 eV**, **D_tr → Ea ≈ 0.175 eV** 다 (figure-read 끝점 (0.85, −3.88)–(1.93, −4.87) 및 (0.85, −4.25)–(1.93, −5.20)).
> 오차막대 크기(전하가 더 잡음이 큼 → ±0.02)와도 맞는다. ⇒ **0.18 = 전하, 0.17 = tracer** 로 읽는다.
> 어느 쪽이든 **결론(두 값이 오차 안에서 같다)은 안 바뀐다.**

### 3c. 확산계수 — `Fig. 4` 좌측 아레니우스에서 (figure-read ≈)

| 1000/T | T (K) | log₁₀ D_σ | log₁₀ D_tr | D_σ/D_tr |
|---|---|---|---|---|
| 0.85 | ≈ 1176 | **≈ −3.88** | **≈ −4.25** | **≈ 2.3** |
| 1.93 | ≈ 518 | **≈ −4.87** | **≈ −5.20** | **≈ 2.1** |

- 단위 cm²/s. **x 범위가 0.8–1.95 다 ⇒ 온도 범위 ≈ 513–1250 K. 300 K 점이 없다.**
  SI 가 이유를 명시한다: *"the finite length of the simulations did not permit to investigate diffusion properties at ambient temperatures (without extrapolation techniques)"*.
- 검은 삼각형 = Mo, Ong & Ceder [4] (*Chem. Mater.* **24**, 15 (2012)) 의 tracer 값. **파란 선(이 논문 D_tr)과 고온에서 잘 겹친다.** 단 `1000/T ≈ 1.65` (≈ 606 K) 의 삼각형은 파란 적합선보다 **약 0.1 decade 아래**에 있다 (figure-read).

### 3d. 정적 집단 요동 — Eq. (5) 검증 (`Fig. 2`)

$$N_s\langle V_{s,a}^2\rangle \;\sim\; \frac{k_BT}{m_s}\Bigl(1-\frac{1}{M_{\rm tot}/M_s}\Bigr)$$

- 세 데카르트 방향 **x·y·z 전부** Li(빨강)·S(파랑, ×20 스케일)의 데이터점이 예측 직선 위에 **오차막대 안에서** 올라앉는다 (figure-read: y축 `N⟨V²⟩` 0–50 Hartree units, T ≈ 150–1100 K, 둘 다 원점 근처를 지나는 직선).
- 의미: **MD 가 집단좌표의 *정적* 통계를 맞게 재현하고 있다는 값싼 건강검진**이다. (동역학적 정확도 보증은 아니다.)
- 단일 원소계(`M_tot = M_s`)면 우변이 **0** 이 된다 — 운동량 보존의 직접 결과.

### 3e. SI — 무시하면 안 되는 두 개

**(i) CPMD 열평형 (`Fig. S1`)** — 종(種)별 온도비 `T(S)/T(Li)`:

| 설정 | T(S)/T(Li) 수렴값 |
|---|---|
| mass preconditioning **ON** + emass **500** amu | **≈ 1.3** (figure-read 1.32–1.34, **수렴에 ~40 ps**) |
| preconditioning **OFF** + emass 500 amu | **≈ 1.1** (figure-read 1.08–1.10) |
| preconditioning **OFF** + emass **300** amu ← **생산 설정** | **≈ 1.05** (figure-read 1.04–1.05) |

> *"This causes a difference of **200 K at a global temperature of 600 K**"* — 즉 나쁜 설정에서는
> **Li 와 S 가 서로 다른 온도에 평형**을 이룬다. 온도비는 **글로벌 온도에 무관**(전 온도 같은 값으로 수렴).

**(ii) ⭐ Einstein/MSD 적합창 인공물 (`Fig. S3`)** — 이게 우리에게 제일 직접적이다.

같은 궤적에서 MSD 를 **200 / 400 / 1000 / 2000 fs** 의 서로 다른 시간규모로 선형적합했다.

| figure-read | 결과 |
|---|---|
| T ≳ 830 K (1000/T ≲ 1.2) | **네 곡선이 겹친다** (log D ≈ −4.25 … −4.65) |
| T = 200 K (1000/T = 5) | **200 fs → log D ≈ −5.42 · 2000 fs → log D ≈ −6.46** = **1.04 decade = 약 11 배 차이** |
| 기울기(겉보기 Ea, **우리 유도**) | 저온 구간 `1000/T = 3.65→5.0`: 200 fs **≈ 0.031 eV** vs 2000 fs **≈ 0.091 eV** — **2.9 배** |

> 저자 결론: *"Considering the slope after **2 ps** we get a reasonable convergence to a linear behavior at the higher temperatures. Lower temperatures seem to be converged from a statistical point of view, but are associated to **intermediate superdiffusing regimes**."*
>
> 🟢 **우리 규약 `MSD 창 2–50 ps` 의 하한이 정확히 이 권고다** — §7-4b 에서 다시 다룬다.

**(iii) 단열 조건 (`Fig. S2`)** — 50–500 ps 구간에서 이온 운동에너지 ≈ **0.25 Ha** (요동 0.19–0.33), 가상 전자 운동에너지 ≈ **0.01 Ha** (450 ps 동안 0.008 → 0.014 로 아주 약한 상승만). **25 배 격차 유지** ⇒ Car–Parrinello 단열면 이탈 없음. **x축이 500 ps 까지 간다 = 생산 궤적 길이의 시각적 확인.**

---

## 4. 이론 — 이 논문의 절반이다 (유도 전부)

### 4-1. 두 확산계수의 정의

**Tracer (단일입자)** — Eq. (1):
$$D_{\rm tr}\equiv\lim_{t\to\infty}\frac{\langle|x|^2\rangle}{6t}=\frac13\int_0^{\infty}\langle v(t)v(0)\rangle\,dt$$
- 좌변 = **Einstein(MSD) 경로**, 우변 = **Green–Kubo(속도 자기상관) 경로**. 같은 양의 두 표현.

**근사 Nernst–Einstein** — Eq. (2):
$$\sigma \sim \frac{Z_c^2e^2C}{k_BT}D_{\rm tr},\qquad C=N_c/V$$
- ⚠ 논문이 `=` 가 아니라 **`∼`** 를 쓴다. 처음부터 근사로 표기한다.

**엄밀 선형응답(Kubo)** — Eq. (3):
$$\sigma=\frac{N_c^2Z_c^2e^2}{3k_BTV}\int_0^{+\infty}\langle V^c(t)V^c(0)\rangle\,dt,\qquad V^c=\frac1{N_c}\sum_{i=1}^{N_c}v_i$$
- **대문자 = 집단변수, 소문자 = 단일입자** (논문 표기 규약).
- Einstein 항등식을 적용하면 **전하 확산계수** `D_σ` 가 정의되고 **엄밀한** NE 식 `σ = Z_c²e²C·D_σ/(k_BT)` 를 얻는다.
- ⇒ **`D_σ` 만이 σ 에 정비례한다.** `D_tr` 은 아니다.

**Haven 비**: `H = D_tr / D_σ`.

### 4-2. 🎯 새 부등식 (논문이 말하는 "first result") — Eq. (4)

단순 전개:
$$D_\sigma = D_{\rm tr} + \frac16\sum_{j\neq0}\int_{-\infty}^{+\infty}\langle v_j(t)v_0(0)\rangle\,dt$$

여기 **둘째 항이 "ionic correlations" 의 정체다** — 태그된 입자 0 과 *다른* 입자 j 의 **속도 교차상관**(distinct term).

Cauchy–Schwartz 로 각 교차항을 `≤ D_tr` 로 묶으면:
$$\boxed{0 \;\leqslant\; D_\sigma \;\leqslant\; N_{\rm eff}\,D_{\rm tr}}$$

- `N_eff` = *"an effective number of particles with whom the tagged carrier can interact in a typical correlation time"*. **세기변수(intensive)** 이고 **상호작용 사거리에 의존**한다.
- **물리적 함의 3개** (논문이 직접 뽑는다):
  1. `D_tr = 0` ⇒ `D_σ = 0`. **단일입자 확산 없이 이온전도 없다.**
  2. 역은 성립하지 않는다 — `D_tr > 0` 인데 `D_σ = 0` 일 수 있다. **극단 예: 순수 분자액체(물)** — 분자내 결합이 안 끊긴다고 가정하면 단일입자는 확산하는데 이온절연체다 ⇒ `H = ∞`, NE 의 **완전한 실패**.
  3. **설계 지침**: *"finding materials where the carrier-carrier interaction is long ranged in order to increase conductivity by exploiting correlations."* ⚠ 단 저자 스스로 **바로 제한**한다 — *"the short range of interactions in materials far from phase transitions forces this effect to be relatively small."*

> ⛔ **부등식의 실효성에 대한 우리 평가**: `N_eff` 를 독립적으로 계산하는 처방이 **이 논문에 없다.**
> 그래서 Eq. (4) 는 **정성적 상한**이고 `H` 의 예측값을 주지 않는다. §10-1 참조.

### 4-3. 🔎 **"ionic correlations" 가 구체적으로 무엇인가** (질문 2 의 답)

논문이 다루는 상관은 **두 종류이고 성격이 다르다.** 섞으면 안 된다.

| | **① Li–Li 교차상관 (진짜 상관)** | **② Li ↔ 골격 역류 (운동량 보존)** |
|---|---|---|
| 수식 | Eq. (4) 유도의 `Σ_{j≠0}∫⟨v_j v_0⟩` | Eq. (5)–(6) |
| 종 | **같은 종끼리 (Li–Li)** | **다른 종과 (Li ↔ S/Ge/P)** |
| 부호 | **양수** ⇒ `D_σ > D_tr` ⇒ `H < 1` | 골격이 **반대로** 흐름 |
| 기전 | 1D c축 채널 안의 **협동·일렬(concerted) 이동** — 한 Li 가 뛰면 이웃이 같은 방향으로 따라간다 | Li 집단이 한쪽으로 흐르면 PBC + 총운동량 0 이라 골격이 반대로 표류 |
| 크기 (LGPS) | 이것이 `H ≈ 0.4–0.6` 의 주범 | `H 0.53 → H_c 0.42` — **약 20 %** |
| 처리 | 물리다. 빼면 안 된다 | **빼야 한다** — Eq. (6) 로 골격 기준계로 옮긴다 |

**② 에 대한 저자의 미묘한 주장** (정확히 옮긴다):
> *"We notice that indeed the signals `Ṽ_Li` and `V_Li` are **not equivalent in the thermodynamic limit** and therefore the proposed correction to the conductivity is **not merely a finite-size effect**. Nevertheless, if the simulation protocol leads to a nondiffusing rigid matrix, then the correction added to the signal does not change the value of the measured ionic conductivity."*

즉 — **골격이 안 움직이면 보정이 무해하고, 골격이 움직이면 보정이 필수다.**
🔴 우리에게 직결된다: 우리는 **b2o3 1200 K 에서 골격 creep 판정**을 이미 냈다 (§7-4c).

**재규격화 속도** — Eq. (6):
$$\tilde V_{\rm Li}=V_{\rm Li}-\frac1{N_r}\sum_{i\in R}v_i,\qquad R=\{{\rm S},{\rm Ge},{\rm P}\}$$
- ⚠ **질량가중이 아니라 개수 평균**이다 (`1/N_r · Σ v_i`). 우리 코드도 개수 평균(`ref.mean(axis=1)`)이다 ✓.

### 4-4. 정적 집단 요동 Eq. (5) — SI 유도 요약

SI §I 가 **정준(canonical) 앙상블 → 등적 미시정준(NVE, 총운동량 0)** 변환으로 유도한다.
- 출발: Lebowitz, Percus & Verlet, *Phys. Rev.* **153**, 250 (1967) 의 앙상블 변환 항등식 (Eq. S1).
- 갈릴레이 불변성으로 `∂⟨S_a⟩/∂w_b|_{βw=0} = δ_ab N_s` (Eq. S2), `∂(βw_a)/∂M_b = −β/M_tot` 를 대입 →
  $$\langle S_a^2|M=0,E\rangle \sim \langle S_a^2|\beta w=0,\beta\rangle - \frac{N_s^2}{M_{\rm tot}\beta}\quad({\rm Eq.\ S3})$$
- `V_{s,a} = S_a/N_s` 와 정준값 `⟨S_a²⟩ = N_s k_BT/m_s` 를 넣으면 본문 Eq. (5).

> **왜 이게 중요한가**: 이 식은 *"주기경계에서 골격이 집단적으로 흐르는 것을 막을 방법이 없다"* 를
> **정량적으로** 말한다. 뺄 수 있는 인공물이 아니라 **앙상블이 강제하는 요동**이다.
> ⇒ 그래서 Eq. (6) 의 기준계 이동이 임시방편이 아니라 **필연**이라는 논증이 된다.

---

## 5. 방법 ★ — 우리가 같은 축을 흉내 낼 때 필요한 조건 전부

| 항목 | 값 | 비고 |
|---|---|---|
| **계** | **Li₁₀GeP₂S₁₂ (LGPS) — 이것 하나뿐** | 아르지로다이트 **0회** |
| 초기 구조 | **실험 결정학 좌표** [3] Kuhn/Köhler/Lotsch *PCCP* **15**, 11620 (2013) + [5] Kamaya *Nat. Mater.* **10**, 682 (2011) — **셀 모양·크기도 실험값 고정** | 완화 없음. **NPT 없음** |
| 셀 | **50 원자 초격자** (= LGPS 통상 단위포, Z=2) ⇒ **Li 20개** (**우리 유도**: 25 atoms/f.u. × 2) | 정성 확인용 **100 원자**(Li 40) 별도 |
| 무질서 처리 | **없음 — 단일 구성(single-config)**. SQS·enumerate **0회** | LGPS 는 Li 자리 부분점유가 있는데 그 앙상블을 안 다룬다 (§10-3) |
| MD 방식 | **Car–Parrinello (CPMD)** [18] — Born–Oppenheimer MD 아님 | `cp.x` |
| 코드 | **Quantum ESPRESSO** `cp.x` [19] | |
| 범함수 | **PBE** · vdW 보정 **없음** | |
| 유사퍼텐셜 | **norm-conserving, SSSP 라이브러리** [20] | PAW 아님 |
| 컷오프 | **ecutwfc 60 Ry** (ecutrho 미보고) | |
| k-점 | **미보고** (50원자 CPMD ⇒ 사실상 Γ 만으로 추정 — **우리 추정, 논문 미명시**) | |
| DFT+U | **없음** | |
| 전자 질량 | **300 amu** (가상질량) | *"needed to guarantee adherence to the Born-Oppenheimer surface"* |
| mass preconditioning | **끔** (Fourier acceleration [21] 사용 불가) | 켜면 Li/S 열평형이 깨진다 (SI §II.A) |
| 시간 간격 | **4.0 a.u.** = **0.0968 fs** (**우리 환산**) | dt 가 매우 작다 — CPMD + 가벼운 Li |
| 평형화 | **Nosé–Hoover** [17] 트랜지언트 | |
| **생산 앙상블** | 🔴 **NVE (미시정준)** | *"we rule out the possibility that the presence of a thermostat or a barostat interferes with the transport process of interest"* |
| 궤적 길이 | **최대 500 ps** ⇒ **약 5.17 M 스텝** (**우리 환산**) | SI 열평형 시험은 ~100 ps × 다수 |
| 온도 | 본문 아레니우스 **≈ 513–1250 K** (`Fig. 4` figure-read). SI `Fig. S3` 은 **200 K 까지** 내려가나 **본문에서 배제** | **300 K 직접 계산 없음** |
| D 추출 | **Green–Kubo** — Eq. (7) 의 적분 자기상관함수 `u(t)`, `c(t)`, `c̃(t)` 의 장시간 평탄값 | Einstein/MSD 는 **SI 에서 비판 대상**으로만 등장 |
| 오차 | **블록 분석**(block analysis), **블록 길이에 대한 수렴을 확인** [22] Jones & Mandadapu *JCP* **136**, 154102 (2012) | |
| 시드/복제 | **보고 없음** — 멀티시드 서술 0회 | §10-2 |

**Eq. (7) — 실제로 그린 세 함수**
$$u(t)\equiv\frac13\int_0^t\langle v(t')v(0)\rangle dt' \;\to\; D_{\rm tr}$$
$$c(t)\equiv\frac{N_{\rm Li}}3\int_0^t\langle V_{\rm Li}(t')V_{\rm Li}(0)\rangle dt' \;\to\; D_\sigma$$
$$\tilde c(t)\equiv\frac{N_{\rm Li}}3\int_0^t\langle \tilde V_{\rm Li}(t')\tilde V_{\rm Li}(0)\rangle dt' \;\to\; \tilde D_\sigma$$

> ⭐ **정규화 대조 (우리 코드와 같은가?)** — `V_Li = (1/N)Σv_i` 이므로
> `c(t) = (1/(3N))∫⟨(Σv)(Σv)⟩`. Einstein 대응물은 `D_σ = ⟨|ΣΔr|²⟩/(6Nt)`.
> 우리 `haven_curves` 는 `MSD_σ(τ) = ⟨|Σ_i Δr_i(τ)|²⟩/N`, `D_σ = slope/6`.
> ⇒ **정규화가 정확히 같다.** ✅ (§7-4a)

---

## 6. 결과 — 섹션별 상세 (그림 실독 포함)

### 6-1. `Fig. 1` — LGPS 의 Li 밀도와 1D 채널 (실독)

FPMD 궤적에서 뽑은 **Li 밀도 등가면**(자홍색)을 그렸고, 실험 Li 결정학 자리(연두 구, **반지름 ∝ 점유율**)와 겹친다.

**figure-read**: 자홍색 등가면이 **긴 축 방향으로 끊김 없는 굵은 관(tube)** 을 이루고, 그 관들 사이를 **가늘고 짧은 횡방향 연결**이 잇는다. 화살표가 두 종류 — 긴 축을 따라 셀 밖까지 뻗는 **긴 화살표 하나**, 그리고 횡방향의 **짧은 화살표들**.

- 본문 서술(*"parallel unidimensional paths connected by transverse connections"*)과 **그림이 일치한다**. ✅
- 굵기 차이가 그대로 §6-4 의 이방성(`H_c`: z 0.36 ≪ xy 0.61)으로 이어진다 — **좁고 막힌 1D 관일수록 일렬 협동 이동이 강제된다.**
- ⚠ 이 그림은 **등가면 임계값이 명시돼 있지 않다.** 관이 얼마나 굵은지는 임계값 선택에 달렸다 (§10-5).

### 6-2. `Fig. 2` — Eq. (5) 검증 (실독)

**figure-read**: 3패널(x / y / z). y축 `N⟨V²_{s,a}⟩` (Hartree units) 0–50, x축 T(K) 눈금 300·700 (데이터는 ≈150–1100 K). 빨강 = Lithium, 파랑 = **Sulfur (×20)**. 검은 사각 데이터점 + 오차막대가 **세 방향 모두** 직선 위에 올라간다.

- S 를 **×20** 스케일한 이유: `⟨V²⟩ ∝ k_BT/m_s` 라 무거운 S 는 훨씬 작다. 같은 축에 보이려는 표시상의 선택.
- ⇒ **MD 의 집단좌표 정적 통계가 이론과 일치**. 방향 이방성 없음(x·y·z 가 같은 모양) — 이건 *정적* 요동이라 당연하다. **동적** 이방성은 `Fig. 4` 에서만 나온다.

### 6-3. `Fig. 3` — 🎯 세 자기상관함수 (실독, **이 논문에서 제일 중요한 그림**)

**figure-read**: y축 cm²/s, `×10⁻⁴` 표기, 0 – 약 1.7×10⁻⁴. x축 time (ps), 0 – 약 2 ps. 세 곡선 + **음영 오차띠**.

| 곡선 | 최댓값 (τ ≈ 0.035 ps, 삽입도에서) | **장시간 평탄값** | 오차띠 |
|---|---|---|---|
| **u(t)** (빨강, → `D_tr`) | ≈ **1.45×10⁻⁴** | ≈ **0.17×10⁻⁴** | **거의 안 보일 만큼 얇다** |
| **c(t)** (초록, → `D_σ`) | ≈ **1.38×10⁻⁴** | ≈ **0.33×10⁻⁴** | **눈에 띄게 넓다** |
| **c̃(t)** (파랑, → `D̃_σ`) | ≈ **1.68×10⁻⁴** | ≈ **0.37×10⁻⁴** | **가장 넓다** |

읽히는 것 넷:

1. **짧은 시간(삽입도, 0–0.1 ps)에서 세 곡선이 비슷하다.** 본문 해석: *"for small time intervals the particles do not have the time to interact and behave as independent entities, apart from the constraint imposed by momentum conservation."* ✅ 그림과 일치.
2. **감쇠 진동**이 보인다 — 0.035 ps 첫 봉우리 → 약 0.12 ps 골 → 약 0.21 ps 둘째 봉우리 → 0.3–0.5 ps 부터 평탄. 이것이 본문이 말하는 **backscattering**(되튕김)이다. 우리(Einstein/MSD)는 이 구조를 **아예 못 본다** — MSD 는 이 진동을 적분해 버린다.
3. **`c̃` > `c` > `u`.** 즉 `D̃_σ > D_σ > D_tr`. ⇒ `H_c < H < 1`. `Fig. 4` 표(0.42 < 0.53)와 **자기정합** ✅.
4. 🔴 **오차띠 폭이 결정적이다.** 빨강(tracer)은 선 두께 수준인데 초록·파랑(집단)은 육안으로 폭이 있다. **같은 500 ps 궤적에서** 그렇다. 본문도 명시한다: *"Long molecular dynamics simulations are necessary to obtain a reasonable statistical error on the charge diffusion coefficient, even if the tracer diffusion coefficient converges much sooner, as expected."*
   ⇒ **우리 `haven_curves` docstring 의 경고와 같은 말이고, 이쪽이 FPMD 500 ps 다.** (§12-1)

### 6-4. `Fig. 4` — 아레니우스 + Haven 표 (실독)

**좌측 패널** (figure-read): y `Log D (cm²/s)` −5.2 … −3.8, x `1000/T (1/K)` 0.8 … 1.95.
빨강 = `Log D_σ`, 파랑 = `Log D_tr`, **검은 삼각형** = `Log D_tr` [4] (Mo/Ong/Ceder 2012).
두 점선 적합이 **거의 평행**하고, 세로 간격이 전 구간 **≈ 0.33–0.37 decade**(= 2.1–2.3 배) 로 유지된다.

> **(우리 유도, 논문 미보고)** 이 "일정한 세로 이동" 이 §3b 의 Ea 일치와 **같은 사실의 두 표현**이다.
> 평행 = 기울기 같음 = Ea 같음. 상관은 **아레니우스 전치인자(attempt frequency)** 에만 들어가고
> **장벽에는 안 들어간다.** 논문 결론부가 정확히 이 말을 한다:
> *"Correlations therefore play a role in determining the attempt frequency, in an Arrhenius-like description, but not the energy barriers."*

**우상 패널** (figure-read): y `H_c` (눈금 0.2 / 0.5 / 0.8), x `T (K)` ≈ 550–1150.
두 계열 — **빨강 ≈ 0.58 근방**(수평 점선 + 음영), **파랑 ≈ 0.33 근방**(수평 점선 + 음영).
표와 대조하면 빨강 = **xy** (0.61), 파랑 = **z** (0.36) 로 읽힌다.
- 🔴 **오차막대가 크다.** 빨강 계열은 한 온도에서 **0.4 ~ 0.85** 까지 뻗는 점이 있다 (figure-read).
- 🟢 **그런데 수평 점선은 평평하다** — `H_c` 에 **체계적 온도 의존이 안 보인다** (≈550–1150 K).
  본문: *"The weak temperature dependence of this correction permits one to safely extract activation energies also considering the (faster converging) single-particle diffusion coefficient."*

**우하 표**: §3a 그대로.

**저자의 이방성 해석** (그대로 옮긴다):
> *"showing a much higher degree of correlation along the c axes, the direction of fastest diffusion. The better compatibility of the out-of-plane Haven ratio with the experimental value is an indication that transport along c axes may still be dominant in experiments and not suppressed by disorder or grain-boundary effects."*

⚠ **이 논증은 순환적이다** — `H_c(z) = 0.36` 이 실험 `~0.3` 에 가깝다는 것에서 *"실험에서도 c축이 지배적"* 을 끌어내는데, 실험값은 **다른 물질(Li₁₀SnP₂S₁₂)의 다결정 값**이다. §10-4.

### 6-5. 결론부가 실제로 주장하는 것

1. 부등식 Eq. (4) 로 두 확산계수의 차이에 물리적 의미를 줬다.
2. MD 에서 **확산 이온의 속도를 재규격화해야 한다**.
3. LGPS 의 Li 운동은 **상관이 크고 방향에 의존**한다.
4. ⇒ **표준 NE 식을 쓸 수 없다. 선형응답 식을 써야 한다.**
5. **그러나 Ea 는 두 방법이 거의 같다.** 상관은 **전치인자**에 들어간다.

---

## 7. 우리 DFT/MD 와의 대조 ★★ (1저자 질문 1–4 의 답)

기준 문서: `../our_dft_baseline.md` · `kb/concepts/md.md` §6 · `db/properties/haven_ratio_measured_2026_09_07.json` · `tools/ionic/msd_diffusive_check.py`

### 7-1. 🎯 **질문 1 — H_R 의 값과 부호. 우리 `md.md` §6 과 같은 방향인가?**

> ## ✅ **같은 방향이다. 우리가 또 틀린 것이 아니다.**

| | 규약 | 값 | σ_NE 는 |
|---|---|---|---|
| **`kb/concepts/md.md` §6** (2026-09-07 정정) | `H_R ≡ D*/D_σ` | — | *"`H_R<1` (상관·협동 이동) 이면 NE 는 **과소**다"* |
| **[Marc17NE] 본문 p.1** | `H = D_tr/D_σ` (**같다**) | `H_c(xyz) = 0.42` | *"its application leads to an **underestimation** of the value of conductivity"* |

**세 겹으로 확인했다** (규약 착오는 이 축에서 반복된 사고라 일부러 세 번 봤다):
1. **정의식이 글자 그대로 같다** — 둘 다 분자가 tracer.
2. **값이 1 보다 작다** — 0.36 / 0.42 / 0.46 / 0.53 / 0.61 / 0.79, **여섯 칸 전부**.
3. **저자가 방향을 산문으로 명시한다** — `underestimation`. 우리가 해석으로 끼워 맞춘 게 아니다.

> 🟢 **판정: `md.md` §6 의 2026-09-07 정정은 이 원전이 지지한다.**
> ⛔ 그리고 **"H_R=1 이라서 상한"** 이라는 옛 서술이 틀렸다는 것도 재확인된다.
> ⛔ 반대로 `[Zaby26σ]` 의 *"NE 가 과대"* (액체 H_R 1.3–2.1)는 **이 논문과 부호가 반대**이고,
> 그 이유가 §7-2 에서 미시적으로 설명된다 — **우리 계로 옮기면 안 된다**는 앞선 판정이 강화된다.

**우리 db 의 Haven 지형에 이 편을 꽂으면** (전부 소환값 · 규약 `H_R = D*/D_σ` 로 통일):

| 출처 | 계 | 상 | H_R | 방법 | 온도 |
|---|---|---|---|---|---|
| **[Adeli]** | Li₆₋ₓPS₅₋ₓCl₁₊ₓ **아르지로다이트** | 고체(펠릿) | **0.23 – 0.30** | 실험 ⁷Li PFG + EIS | 300 K |
| **[Bron13]** (본 편이 인용) | Li₁₀SnP₂S₁₂ | 고체 | **~0.3** | 실험 | 실온 |
| **🆕 [Marc17NE]** | **Li₁₀GeP₂S₁₂ (LGPS)** | 고체 (완전결정) | **0.36 / 0.42 / 0.61** (z/xyz/xy) | **FPMD Green–Kubo** | 513–1250 K |
| **[Fang22PW]** | Li₆POS₄(SH) · Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅ | 고체 (**아르지로다이트족**) | **0.667 / 0.769** | AIMD | — |
| **우리 box331** (예비) | LPSOCl 3×3×1, 243 Li, 400 ps | 고체 | **≈ 0.60** | MLIP-MD Einstein | 600/800/1000 K |
| **우리 gen1** | LPSCl 계열 소셀, 27–58 Li, 200 ps | 고체 | **0.84 ± 0.06** | MLIP-MD Einstein | 600–1200 K |
| **[Lynch26]** | Li₃.₂₅P₀.₇₅Si₀.₂₅O₄ (**산화물**) | 고체 | **0.53 – 1.03** | MLIP full GK | — |
| **[Zaby26σ]** | 이온액체·에테르 전해질 | **액체** | **1.3 – 2.1** | 고전 MD | — |

⇒ **고체 Li 전도체는 지금까지 예외 없이 `H_R < 1`** (Lynch 상단 1.03 이 오차 안 1 접촉). **액체만 > 1.**
⇒ 🔴 **그리고 이 표에서 우리에게 불리한 것이 하나 보인다**: **우리 gen1 의 0.84 가 고체 분포에서 제일 높다.**
   같은 계열 아르지로다이트인 `[Fang22PW]` 0.67–0.77 보다도, 우리 자신의 box331 0.60 보다도 위다.
   §7-4c 에서 원인 후보를 다룬다.

### 7-2. 🔎 **질문 2 — 상관의 정체와 미시 기전**

§4-3 의 표가 답이지만, **왜 고체는 H<1 이고 액체는 H>1 인가**를 이 논문 + `[Zaby26σ]` 로 한 문단에 쓴다:

- **액체 전해질**: 움직이는 것이 **양이온과 음이온 둘 다**다. 이온쌍(Li⁺⋯TFSI⁻)이 **함께** 움직이면 질량은 옮겨지는데 **알짜 전하는 안 옮겨진다** ⇒ 반대부호 교차상관이 `Σ_i z_i v_i` 를 깎는다 ⇒ `D_σ < D_tr` ⇒ **H > 1, NE 과대**.
- **고체 전해질 (이 논문)**: 움직이는 것이 **Li 하나**다. 골격 PS₄/GeS₄ 는 고정. 그러면 남는 이동체–이동체 상관은 **같은 전하끼리(Li–Li)** 뿐이고, 1D 채널이 이들을 **같은 방향으로** 밀어낸다 ⇒ **양의 교차상관** ⇒ `D_σ > D_tr` ⇒ **H < 1, NE 과소**.

⇒ **부호를 가르는 것은 "무엇이 움직이나" 다.** 이동 음이온이 있으면 > 1, Li 단독이면 < 1.
⇒ ⛔ **그래서 액체 결과를 우리 황화물로 옮기는 것은 부호를 뒤집는 오류다.**

**기전을 더 좁히면**: `Fig. 1` 의 **막힌 1D 관**이 핵심이다. 좁은 관 안에서는 앞 Li 가 비켜줘야 뒤 Li 가 간다 = **일렬(single-file) 유사 협동**. 그래서 **z(c축)에서 상관이 가장 세고**(H_c 0.36), 관 사이를 잇는 **횡방향(xy)에서 약하다**(0.61). **그림이 이 해석을 그대로 보여준다.** ✅
⚠ 다만 논문은 **"vehicle 메커니즘" 이라는 말을 쓰지 않는다**. 골격이 고정이므로 vehicle(운반체 동반 이동)이 아니라 **협동 홉핑(concerted hopping)** 으로 읽는 것이 맞다. `[Jeon26]` 의 아르지로다이트 concerted Li motion 과 같은 어휘다.

### 7-3. ⭐ **질문 3 — 우리 계에 옮길 수 있나** (제일 중요한 판정)

**이 논문이 다룬 계 목록 — 전부다:**

| # | 계 | 역할 |
|---|---|---|
| 1 | **Li₁₀GeP₂S₁₂ (LGPS)** | **계산한 유일한 계.** 50원자(Li 20) + 100원자(Li 40) 확인 |
| 2 | Li₁₀SnP₂S₁₂ | **계산 안 함.** 실험 Haven `~0.3` 을 [24] 에서 **인용만** |
| 3 | Na 판 LGPS (Na₁₀SnP₂S₁₂ 계열) | **계산 안 함.** [9] Richards *Nat. Commun.* **7**, 11009 (2016) 를 *"a similar failure"* 로 **언급만** |
| 4 | 물(H₂O) | **계산 안 함.** `D_tr>0, D_σ=0` 의 **개념적 극단 예시** |

> ## ⛔ **아르지로다이트(Li₆PS₅X)는 이 논문에 한 번도 나오지 않는다.**
> `Li6PS5`·`argyrodite`·`Li6PS5Cl` — 본문·SI 전문 검색 **0회**.

**그러므로 우리 계로 옮길 수 있는 것과 없는 것:**

| | 이식 가능? | 근거 |
|---|---|---|
| **부호** (`H_R < 1`, NE 는 과소) | 🟢 **가능 — 단 "정황"으로만** | 황화물 · Li 단독 이동 · 고정 PS₄ 골격 · 1D~3D 채널 — **우리 계와 같은 물리 부류**다. §7-2 의 기전 논증이 아르지로다이트에도 그대로 적용된다 |
| **크기** (`H ≈ 0.42`) | ⛔ **불가** | 다른 결정구조(정방 1D 채널 vs 입방 cage-network), 다른 Li 농도, 다른 무질서(아르지로다이트는 S²⁻/Cl⁻ 자리 무질서가 지배적인데 LGPS 는 그 축이 없다) |
| **이방성** (z ≪ xy) | ⛔ **불가** | LGPS 는 **정방정 1D 채널계**. 아르지로다이트는 **입방(F-43m) 준등방**. 이방성 자체가 우리 계에 없다 |
| **방법·규율** (§7-4) | 🟢 **전면 가능** | Eq. (6) 기준계 · 블록 오차 · MSD 창 · NVE 생산 |

> ## 🔴 **결론 (1저자 요청 문장 그대로 적는다)**
> **우리 계에서 H_R 을 가정할 근거는 여전히 없다.**
> 이 논문은 **부호를 굳혀 주지만 값을 주지 않는다.** `H = 0.42` 는 **LGPS 의 값**이고, 우리 LPSCl 에
> 곱할 수 없다. 그리고 우리에게는 이미 **우리 계에서 직접 잰 값**이 있다 (gen1 0.84 / box331 ≈0.60,
> 둘 다 `citable:false`) — **남의 값을 빌릴 게 아니라 우리 측정을 제대로 닫는 것이 맞는 길**이다 (§12-1).
>
> ⚠ 그나마 가장 가까운 소환값은 이 편이 아니라 **`[Fang22PW]` 의 아르지로다이트족 AIMD 0.667/0.769** 다.
> 우리 box331 ≈0.60 과 같은 대역이다.

### 7-4. **질문 4 — 어떻게 쟀나. 우리 `--haven` 과 같은 정의인가?**

#### 7-4a. 정의·정규화·기준계 대조 (코드를 읽고 한 줄씩 맞췄다)

| 항목 | **[Marc17NE]** | **우리 `tools/ionic/msd_diffusive_check.py`** | 판정 |
|---|---|---|---|
| **추출 경로** | **Green–Kubo** — Eq. (7) 의 적분 VACF 평탄값 | **Einstein** — MSD 선형적합 기울기/6 | 🔴 **다르다** (§7-4b) |
| `D_tr` 정의 | `(1/3)∫⟨v(t)v(0)⟩dt` | `⟨|Δr_i(τ)|²⟩_{i,t0}/(6τ)` | ✅ **수학적으로 같은 양** (Eq. (1) 이 두 표현을 명시적으로 등치) |
| `D_σ` 정의 | `(N_Li/3)∫⟨V_Li V_Li⟩dt`, `V_Li=(1/N)Σv_i` | `⟨|Σ_i Δr_i(τ)|²⟩_{t0}/(6Nτ)` | ✅ **정규화가 정확히 같다** (1/N 계수 일치) |
| **Haven 규약** | `H = D_tr/D_σ` | `H_R ≡ D*/D_σ` | ✅ **동일** |
| **드리프트 기준계** | **비-Li 골격**(S·Ge·P)의 **개수 평균** 속도, Eq. (6) | **비-Li 골격**의 **개수 평균** 위치 (`ref.mean(axis=1)`) | ✅ **동일** — 우연이 아니다. 우리 합성시험 ⑥ 이 *"전 원자 COM 을 쓰면 Li 신호를 갉아먹는다"* 를 독립적으로 잡아냈고, 이 논문이 같은 이유로 골격만 쓴다 |
| **보정 전/후 둘 다 보고** | ✅ `H` 와 `H_c` 둘 다 | ⛔ **보정 후만** | 🟡 **우리가 덜 낸다** — §12-2 |
| **오차** | **블록 분석 + 블록길이 수렴 확인** [22] | R² < 0.5 면 **H_R 보류**(값을 지어내지 않음) + 시드 산포 보고 | 🟡 **성격이 다르다.** 우리는 게이트, 저쪽은 오차막대. **둘 다 있어야 한다** |
| **생산 앙상블** | **NVE** (Nosé–Hoover 는 평형화만) | **Langevin NVT 생산 전 구간** (τ ≈ 0.51 ps) | 🔴 **다르다 — §7-4c** |
| **시드/복제** | 보고 없음 | **다중 시드** (gen1 최대 4.8배 산포를 보고) | 🟢 **우리가 낫다** |
| **전하 담지체** | Li 만 (골격 반대흐름은 기준계로 제거) | Li 만 (`docstring`: *"전하가 Li 만이라고 본다"*) | ✅ 동일 가정, 동일 한계 |

> ✅ **핵심 판정: 우리 `--haven` 은 이 논문과 *같은 양*을 잰다.** 정규화·규약·기준계가 셋 다 일치한다.
> 남은 차이는 **추출 경로(GK vs Einstein)** 와 **앙상블(NVE vs Langevin)** 둘이고, 아래에서 따로 본다.

#### 7-4b. 🟢 GK vs Einstein — 그런데 SI 가 우리 창을 **지지한다**

이 논문은 Einstein 경로를 **쓰지 않고**, SI §II.B 에서 그 경로의 계통오차를 **경고 대상**으로 다룬다.
겉보기에는 우리에게 불리한데, **내용을 읽으면 반대다**:

| SI `Fig. S3` 이 말하는 것 | 우리 규약 | 판정 |
|---|---|---|
| 200 fs 창은 **초확산(superdiffusive) 중간영역**을 확산으로 오독한다 | 우리 창 하한 **2 ps** | 🟢 **우리가 그 함정 밖에 있다** |
| *"Considering the slope after **2 ps** we get a reasonable convergence to a linear behavior at the higher temperatures"* | 우리 창 **2–50 ps** | 🟢 **하한이 저자 권고와 정확히 같다** |
| 저온(≲ 500 K)은 창을 아무리 늘려도 확산영역이 아니다 — 본문 아레니우스에서 **≈513 K 미만을 배제** | 우리 아레니우스 **600/800/1000 K (400/500 K 제외 판정)** | 🟢 **독립적으로 같은 결론에 도달했다** |
| 창 하나 바꾸면 200 K 에서 D 가 **11배**, 겉보기 Ea 가 **2.9배** 흔들린다 (**우리 유도**) | — | 🔴 **창을 기록 안 한 문헌값은 비교 불가**라는 우리 규율의 외부 근거 |

> ⭐ **`convention_check.py` 가 지키는 "MSD 창 2–50 ps 고정" 에 이제 *원전 인용*이 생겼다.**
> 지금까지 그 규약은 우리 내부 결정이었다. 이제 2017 PRM 이 같은 하한을 권고한다고 쓸 수 있다.
> ⛔ 단 **상한 50 ps 는 이 논문이 말하지 않는다** — 저쪽 최대 창은 2000 fs = 2 ps 다.

#### 7-4c. 🔴 **우리에게 불리한 것 — Langevin 이 H_R 을 1 쪽으로 밀 수 있다**

논문이 **일부러** NVE 로 간 이유:
> *"After an equilibration transient via a Nosé-Hoover thermostat, the sampling of dynamical properties is performed in the microcanonical ensemble. In this way **we rule out the possibility that the presence of a thermostat or a barostat interferes with the transport process of interest**."*

우리는 **Langevin NVT 로 생산 전 구간**을 돈다 (`tools/modelc_v3/aimd_mlip.py`, `friction=0.02` 원시 ASE 단위 ⇒ **τ = 1/γ ≈ 0.51 ps**, 우리 환산).

**(우리 추론 — 이 논문이 검증하지 않았다)** 왜 이게 `H_R` 에 특히 위험한가:
1. Langevin 은 **입자마다 독립인** 마찰·잡음을 준다 ⇒ **교차상관 `⟨v_j v_0⟩` 를 만들지는 않지만 감쇠시킨다** (VACF 에 `e^{−γt}` 꼴 인자).
2. `Fig. 3` 을 보면 **자기항은 τ ≈ 0.035 ps 에 몰려 있고, `u(t)` 와 `c(t)` 의 간격(= 교차항)은 τ ≈ 0.05 → 0.3 ps 에서 자란다.** 즉 **교차항이 자기항보다 *늦게* 쌓인다.**
3. 우리 `τ_Langevin ≈ 0.51 ps` 는 **교차항이 쌓이는 그 시간대와 같은 자릿수**다. 늦게 쌓이는 항이 더 많이 감쇠된다.
4. ⇒ **측정된 상관이 실제보다 약해 보이고, `H_R` 이 1 쪽으로 치우친다.**

**정황 증거 (증명 아님)**: 우리 gen1 `H_R = 0.84` 는 §7-1 표의 **고체 8개 중 가장 1 에 가깝다.**
셀을 키운 box331 에서 **0.60 으로 내려갔다** — 셀 크기 효과일 수도, 통계 개선 효과일 수도 있다.

> ## 🔴 **불리한 결론을 그대로 적는다**
> **우리 `H_R = 0.84` 는 그 자체가 열욕에 희석된 값일 수 있다.** 그렇다면 실제 Haven 보정은
> `md.md` §6 에 적힌 **19 % 보다 크다.** box331 의 0.60 을 적용하면 **65 %** 가 된다.
> ⛔ **어느 쪽도 지금 값으로 쓸 수 없다** — 확인 실험(§12-1 ⑤)이 먼저다.
> ⚠ 그리고 이것은 **σ 절대값 금지를 푸는 근거가 아니라 조이는 근거**다:
> 보정의 *크기*가 미정이라는 뜻이니까.

**골격 creep 과의 연결** — §4-3 의 저자 단서가 우리 원장과 바로 맞물린다:
저자: *"if the simulation protocol leads to a **nondiffusing rigid matrix**, then the correction … does not change the value"*.
우리: `b2o3 1200 K` 는 **골격 3/3 creep 판정**이 났고, 그래서 Haven 집계에서 뺐다
(`haven_ratio_measured_2026_09_07.json` → `★_b2o3_1200K_제외_6점`, 사유 *"골격이 흐르면 '무엇에 대한' 상관인지 정의되지 않는다"*).
🟢 **이 논문이 그 제외 판정의 이론적 근거를 준다.** 우리가 직관으로 뺀 것에 원전이 생겼다.

#### 7-4d. 🟢 시뮬레이션 H 가 실험 H 보다 **깨끗하다** (우리에게 유리한 발견)

실험 Haven(`[Adeli]` 0.23, `[Bron13]` ~0.3)은 **PFG 로 `D*`, EIS 로 `σ`** 를 재고 `σ → D_σ` 환산에 **캐리어 수 `N_c` 를 가정**해야 한다. `[Adeli]` digest §3c 가 그 규약(`c = 4/cell` 하한)을 명시하고, `[Zaby26σ]` digest 가 *"c 를 크게 잡으면 H_R 이 커진다"* 고 적었다.

**이 논문의 `H` 에는 그 자유도가 없다.** `D_tr` 과 `D_σ` 가 **같은 궤적의 같은 Li 집합**에서 나오므로 `N_Li` 가 비에서 **상쇄**된다.

> 🟢 ⇒ **우리 `--haven` 도 같은 이유로 규약자유도가 없다.**
> ⇒ **실험 Haven(0.23)을 빌려 오는 것보다 우리 궤적에서 직접 재는 것이 원리적으로 더 정의가 깨끗하다.**
> 이것이 2026-09-07 에 `--haven` 을 만든 결정을 사후적으로 정당화한다.
> ⚠ 단 **정밀도는 반대다** — 정의는 깨끗해도 표본이 하나라 잡음이 크다 (§12-1).

### 7-5. 우리 계산과 직접 비교할 수 있는 것 / 없는 것

| 양 | [Marc17NE] | 우리 | 비교 가능? |
|---|---|---|---|
| `H_R` 부호 | **< 1** (6/6 칸) | **< 1** (gen1 0.84 · box331 0.60) | 🟢 **가능 — 일치** |
| `H_R` 값 | 0.42 (LGPS) | 0.84 / 0.60 (LPSCl·LPSOCl) | ⛔ **불가** — 계가 다르다 |
| `Ea` | **0.17–0.18 eV** (LGPS) | comp1 **0.253** · modelc **0.224** eV | ⛔ **불가** — 계가 다르다. ⚠ 숫자가 가까워 보이지만 **우연이다** |
| `D` 절대값 | `log D_tr(518 K) ≈ −5.20` | `D(600 K)` = comp1 3.09e-6 / modelc 7.90e-6 cm²/s | ⛔ **불가** — 계·온도·힘장 전부 다르다 |
| `H_R` 의 온도의존 | **약함** (550–1150 K 평평) | **약함** (box331 600/800/1000 K 에서 0.60±0.01) | 🟢 **정성 일치** — 독립 확인 |
| `Ea(tracer) ≈ Ea(charge)` | **0.01 eV 차** | 미측정 | 🔵 **우리가 아직 안 했다** — §12-3 |
| 밴드갭·ESW·탄성 | **없음** | 있음 | — **접점 없음** |

---

## 8. DFT/계산 방법 요약 ★ (한눈표)

| | |
|---|---|
| code | Quantum ESPRESSO **`cp.x`** (Car–Parrinello) |
| functional | **PBE**, vdW **없음** |
| pseudo | **norm-conserving (SSSP)** — PAW 아님 |
| ecut | **60 Ry** (ecutrho 미보고) |
| k-points | **미보고** (Γ 추정 — 우리 추정) |
| supercell / nat | **50 원자** (Li 20) · 확인용 100 원자 (Li 40) |
| DFT+U | **없음** |
| AIMD | **CPMD** · emass **300 amu** · precond **OFF** · dt **4 a.u. = 0.0968 fs** · 평형 **Nosé–Hoover** → 생산 **NVE** · **최대 500 ps** (≈5.17M 스텝) |
| MLIP | **없음** (전부 FPMD) |
| 무질서 처리 | **단일 구성** — SQS/enumerate 0회 |
| 후처리 | **Green–Kubo 적분 VACF** (Eq. 7) · **블록 분석 오차** · **아레니우스 선형적합** · **Li 밀도 등가면**(`Fig. 1`) |
| 도구 | 명시 없음 (pymatgen/VESTA/LOBSTER 전부 미언급). `Fig. 1` 렌더러 미명시 |
| NEB / Bader / COHP / DOS / ELF / phonon / 탄성 / ESW | **전부 0회** |

---

## 9. Figure set ★ — 7장 전부 실독

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | LGPS 의 FPMD Li 밀도 등가면(자홍) + 실험 Li 자리(연두, 반지름∝점유율). **c축을 따라 굵고 연속인 1D 관**, 그 사이를 **가는 횡방향 연결**이 잇는다. 화살표가 활성 확산 방향 | 🔵 **이방성 상관(z 0.36 ≪ xy 0.61)의 구조적 근거.** ⛔ 등가면 임계값 미명시라 "관 굵기" 정량 인용 금지. 우리 아르지로다이트는 **입방 준등방**이라 이 그림의 1D 구조는 **이식 안 된다** |
| **2** | `N⟨V²_{s,a}⟩` (Hartree units) vs T, **x·y·z 3패널**. Li(빨강)·S(파랑 ×20). Eq. (5) 예측 직선 위에 데이터가 올라앉음 | 🟢 **값싼 MD 건강검진 레시피.** 우리 궤적에서도 종별 COM 요동을 재 `k_BT/m_s·(1−M_s/M_tot)` 와 대면 **집단좌표 통계가 맞는지 MD 재계산 0 으로** 확인할 수 있다 (§12-4) |
| **3** | 🎯 **적분 자기상관함수 3종** `u(t)`(빨강, tracer) · `c(t)`(초록, 전하) · `c̃(t)`(파랑, 골격기준 보정) + **오차 음영띠**. 0.035 ps 첫 봉우리 → 0.12 ps 골 → 0.21 ps 둘째 봉우리(backscattering) → 0.3–0.5 ps 평탄. 삽입도는 0–0.1 ps 확대 | 🔴 **우리 도구 경고의 시각적 증거**: 같은 500 ps 에서 빨강 오차띠는 선 두께, 초록·파랑은 눈에 띄게 넓다 ⇒ **집단좌표는 원리적으로 훨씬 잡음이 크다.** 🔵 교차항이 **자기항보다 늦게(0.05–0.3 ps) 쌓인다** = §7-4c Langevin 감쇠 우려의 근거 |
| **4** | 🎯 좌: **아레니우스** `Log D_σ`(빨강)·`Log D_tr`(파랑)·Mo/Ong/Ceder tracer(검은 삼각), `1000/T` 0.8–1.95 → **513–1250 K, 300 K 점 없음**. 두 적합선 **평행**, 세로 간격 ≈0.33–0.37 decade. 우상: `H_c` vs T(≈550–1150 K), **온도의존 안 보임**(수평 점선), 오차막대 큼. 우하: **Haven 표** z 0.36/0.46 · xy 0.61/0.79 · xyz 0.42/0.53 · exp ~0.3 | 🔴 **이 논문의 헤드라인 숫자 전부가 여기 있다.** 🟢 *"평행 = Ea 같음 = 상관은 전치인자에만"* 은 우리가 **Ea 는 tracer 로 내도 된다**고 쓸 근거. ⛔ **`~0.3` 은 Li₁₀SnP₂S₁₂ 실험값이지 LGPS 도 아르지로다이트도 아니다** |
| **S1** | CPMD 종별 온도비 `T(S)/T(Li)` vs t(0–90 ps). precond ON+emass500 → **≈1.33**(수렴에 ~40 ps) · OFF+500 → **≈1.09** · OFF+300 → **≈1.05**(생산) | 🔵 **CPMD 고유 문제라 UMA-MD 에 직접 이식 안 된다** (우리는 가상 전자자유도가 없다). 🟢 그러나 **"종별 온도 등분배를 따로 확인한다"** 는 검사 자체는 이식 가능하고, **가벼운 Li 에서 먼저 깨진다**는 경고는 보편적이다 |
| **S2** | 단열조건. 50–500 ps 에서 이온 KE ≈**0.25 Ha**(요동 0.19–0.33), 가상 전자 KE ≈**0.01 Ha**(0.008→0.014 로 미세 상승). **25배 격차 유지** | 🔵 CPMD 전용. 🟢 **x축이 500 ps 까지 간다 = 생산 길이의 시각적 확인**이고, 우리가 "500 ps FPMD" 를 인용할 때 근거가 된다 |
| **S3** | ⭐ **MSD 적합창 인공물.** `Log D` vs `1000/T` 0.5–5.5(**T 2000→200 K**), 창 **200/400/1000/2000 fs** 4곡선. T≳830 K 에서 **겹치고**, T=200 K 에서 **1.04 decade(≈11배)** 로 벌어짐 | 🟢🟢 **우리 `MSD 창 2–50 ps` 하한의 외부 원전.** 🟢 **우리 `400/500 K 제외` 판정의 독립 지지** (저자도 ≈513 K 미만을 본문에서 뺐다). 🔴 **창을 기록 안 한 문헌 D 는 비교 불가**의 근거 |

> 표(`tab_*.png`): **이 논문에 번호 붙은 표가 0개**다. Haven 표는 `Fig. 4` **안에 그려진 표**라 그림으로 읽었다.
> ⚠ **크로핑 사고 기록**: 최초 `figures.json` 에 들어 있던 14장은 전부 `10. ACSAMI_2017_Haruyama_…` 의 그림이었다
> (inbox 파일명이 둘 다 `10. ` 로 시작해 추출기가 오짝). `--pdf` 명시로 재추출했고, 그 14장은
> `litdb/figures/haruyama2017_cation_mixing_co_diffusion_lco_lps/` 에 **정상 사본이 이미 있어** 손실 없다.
> `Fig. S2` 는 추출기 기하검증(벡터 경로 4개)이 오탐 방지로 뺀 것을 **손으로 복구**했다.

---

## 10. 비판 — 이 논문의 약한 곳 ★

### 10-1. 🔴 `N_eff` 가 계산 불가능한 양이라 부등식 Eq. (4) 가 헐겁다

논문이 *"the first result of this paper"* 라 부르는 `0 ≤ D_σ ≤ N_eff D_tr` 에서 `N_eff` 는
*"an effective number of particles with whom the tagged carrier can interact in a typical correlation time"* 으로만 정의된다. **계산 처방이 없다.** LGPS 에서 `N_eff` 가 얼마인지도 안 낸다.
⇒ 상한은 **원리적으로 참이지만 수치적으로 공허**하다. 측정된 `D_σ/D_tr ≈ 2.5` 가 그 상한의 몇 %인지 말할 수 없다.
⚠ 그래서 *"이 논문이 상관 강화의 상한을 정량화했다"* 고 인용하면 **안 된다**.

### 10-2. 🔴 시드·복제가 없다 — 통계 규율이 우리보다 얇다

`Fig. 4` 우상 패널의 `H_c` 오차막대는 한 온도에서 **0.4–0.85** 까지 뻗는다 (figure-read). 그런데:
- **독립 시드/복제 서술이 논문·SI 전체에 0회**다. 오차는 **한 궤적 안의 블록 분석**에서만 나온다.
- 블록 분석은 **그 궤적 안의 상관시간**을 잡을 뿐, **초기조건 앙상블**은 못 잡는다.
- 우리는 같은 계·같은 온도에서 **시드만 달라도 H_R 이 1.0–4.8배 벌어지는 것**을 실측했다 (`haven_ratio_measured_2026_09_07.json`).
⇒ **저쪽 `H_c = 0.42` 의 진짜 불확실도는 보고된 막대보다 클 가능성이 있다.** 🟢 **이 축에서는 우리가 낫다.**

### 10-3. 🔴 LGPS 의 Li 자리 무질서를 앙상블로 다루지 않는다

LGPS 는 Li 자리가 **부분점유**인 물질인데, 이 논문은 **실험 좌표 하나**로 50원자 셀을 만들어 **단일 구성**으로 돌린다. SQS·enumerate·구성 앙상블 **0회**.
- 초이온계라 MD 중에 Li 배치가 스스로 섞인다는 방어는 가능하다 (**고온에서는** 그럴 것이다).
- 그러나 **513 K 최저점**에서도 20 개 Li 가 500 ps 안에 구성공간을 충분히 훑었는지 **확인이 없다**.
⇒ 우리 아르지로다이트 작업에서는 **무질서 앙상블이 제1 변수**다. 이 논문은 그 축을 **안 다룬다**.

### 10-4. 🔴 실험 대조가 순환적이고, 애초에 다른 물질이다

- `Fig. 4` 표의 `exp [24] ~0.3` 은 **Li₁₀SnP₂S₁₂** 값이다. **LGPS 실측이 아니다.**
- 저자는 `H_c(z)=0.36` 이 `~0.3` 에 가깝다는 것에서 *"실험에서도 c축 수송이 지배적일 수 있다"* 를 끌어낸다. 그런데 실험값은 **다결정 시료**의 등방 평균일 가능성이 크다 — 즉 **비교 대상이 `xyz`(0.42) 이지 `z`(0.36) 이 아니다**. 저자 스스로 *"not suppressed by disorder or grain-boundary effects"* 라는 **검증되지 않은 가정**을 얹어 `z` 와 비교한다.
- ⚠ 그리고 **다결정 실험 Haven 은 입계·기공이 `σ` 쪽에만 들어가** `D_σ` 를 낮추고 `H` 를 **높이는** 방향이다. 저자는 이 오염을 논의하지 않는다.
⇒ ⛔ *"계산이 실험 Haven 을 재현했다"* 고 인용하면 안 된다. **자릿수가 같다**까지다.

### 10-5. 🟡 `Fig. 1` 의 등가면 임계값이 없다

Li 밀도 등가면의 isovalue 가 본문·캡션·SI 어디에도 없다. 임계값을 낮추면 관이 굵어지고 횡방향 연결이 더 이어진다. **"1D 채널 + 횡연결" 이라는 정성 그림은 임계값 의존적**이다.
⇒ 우리 BVSE 채널% 규율(*"above-min ≤ iso"* 를 명시)과 대비하면 **저쪽이 덜 엄밀하다**.

### 10-6. 🟡 셀 크기 검증이 정성 수준이다

*"our conclusions are also qualitatively checked for shorter simulations in a 100-atom supercell"* 이 전부다. **100원자 셀의 `H` 값을 안 낸다.**
저자의 방어 논리는 *"온도를 올리면 비조화성이 평균자유행로를 줄여 크기효과가 저절로 눌린다"* 인데, **그 논증이 가장 필요한 곳은 최저온(513 K)** 이고 거기서는 반대로 크기효과가 제일 클 것이다.
🔴 **우리에게 이건 남의 일이 아니다** — 우리도 gen1(소셀) 0.84 → box331(3×3×1) 0.60 으로 **셀을 키우니 값이 바뀌었다**. 이 논문은 그 축을 **닫지 않았다**.

### 10-7. 🟡 300 K 가 없는데 결론은 상온 응용을 향한다

초록·서론이 상용 전지 전해질(LGPS 실험 σ **12 mS/cm @ 상온**)을 겨냥하는데, **계산 최저온이 ≈513 K** 다.
`H` 의 온도의존이 약하다는 것이 방어인데, 그 관측 자체가 **550–1150 K 창 안**의 것이다.
⚠ 그리고 **실험 Haven(~0.3, 상온)이 계산 고온값(0.42–0.53)보다 낮다** — 이것은 **저온으로 갈수록 상관이 더 세진다**는 신호로 읽을 수도 있다. 저자는 이 가능성을 **다루지 않는다**.
⇒ ⛔ *"H 는 온도에 무관하다"* 고 상온까지 확장 인용하면 안 된다.

### 10-8. 🟡 k-점·ecutrho 미보고

`ecutwfc 60 Ry` 만 있고 `ecutrho`, k-격자가 없다. 50원자 CPMD 라 Γ-only 일 가능성이 높지만 **논문이 말하지 않는다**. 재현하려면 저자에게 물어야 한다.

---

## 11. 우리 원장 매핑 — 물성 4축 편입 판정 (질문 6)

### 11-1. 판정: ⛔ **A–D 물성 4축에 넣지 않는다**

| 축 | 이 논문이 주는 값 | 판정 |
|---|---|---|
| **A 이온전도** | `D_tr`·`D_σ`·`H`·`Ea` — **전부 LGPS Li₁₀GeP₂S₁₂** | ⛔ **넣지 않는다.** 우리 A축은 **LPSCl/LPSOCl 아르지로다이트**다. LGPS 값을 그 표에 올리면 다른 물질을 같은 칸에서 비교하게 된다 (선례: `[Alg26FT]` 가 LiF 값 때문에 §J 로 갔다) |
| **B 산화안정 (4축)** | **없음** — ESW·전압창·XPS 0회 | ⛔ |
| **C 기계** | **없음** — 탄성·phonon 0회 | ⛔ |
| **D 전자구조** | **없음** — DOS·밴드갭 0회 | ⛔ |

> ⚠ **특히 `Ea 0.17–0.18 eV` 를 A축 표에 넣지 마라.** 우리 comp1 0.253 / modelc 0.224 eV 와 숫자가
> 가까워 비교하고 싶어지는데, **계가 다르고 힘장이 다르고 창 규약이 다르다.** 우연한 근접이다.

### 11-2. 그래서 어디로 가나

| 위치 | 내용 |
|---|---|
| **`comparison_vs_ours.md` §J-31 `🔧 방법 원전`** (병합 2026-09-22) | **주 등재.** Haven 부호·GK vs Einstein·MSD 창·NVE vs Langevin·골격 기준계 — **방법과 판정만**. 물성 수치 행 없음 |
| **`comparison_vs_ours.md` §H (정직 목록)** | **한 줄**: *"우리 계(아르지로다이트)에서 H_R 을 닫은 적이 없다"* + 보강책 |
| **`kb/concepts/md.md` §6** | 🔵 **한 줄 추가 후보** (사람이 결정): 2026-09-07 정정의 **외부 원전**이 생겼다 |
| **`db/properties/haven_ratio_measured_2026_09_07.json`** | 🔵 **비교 맥락 추가 후보** (사람이 결정): 고체 H_R 분포에 LGPS FPMD 0.42 를 문맥값으로. ⛔ **우리 측정값은 손대지 않는다** |

---

## 12. 적용 인사이트 ★

### 12-1. 🔑 **질문 5 — 우리 H_R 측정을 어떤 조건에서 믿을 수 있나**

> **먼저 1저자가 지목한 판정부터**: 우리 `haven_curves` docstring 은
> *"집단좌표는 표본이 하나라 D* 보다 훨씬 잡음이 크다 — 방향 판별용이지 세 자리 숫자가 아니다"*
> 라고 적고 있다.
>
> ## ⇒ **이 논문은 그 경고를 *강화*한다. 완화하지 않는다.**
>
> 근거 셋, 전부 이 논문 안에 있다:
> 1. 저자가 **같은 말을 본문에 쓴다** — *"Long molecular dynamics simulations are necessary to obtain a reasonable statistical error on the charge diffusion coefficient, even if the tracer diffusion coefficient converges much sooner."*
> 2. **`Fig. 3` 이 그것을 그림으로 보여준다** — 같은 500 ps 궤적에서 tracer 오차띠는 선 두께, 집단 오차띠는 눈에 보이는 폭.
> 3. **그런데도** `Fig. 4` 우상 패널의 `H_c` 오차막대가 한 점에서 **0.4–0.85** 다. **500 ps FPMD 에 전용 블록분석까지 하고도** 그렇다.
>
> ⇒ 우리 200 ps(gen1)·400 ps(box331) MLIP 궤적이 **세 자리 숫자를 낼 리 없다**는 것이 이 논문으로 더 분명해진다.

**그래서 우리 `--haven` 측정을 신뢰하려면 — 조건 5개:**

**① 궤적 길이가 통화(currency)다. 이온 수가 아니다.**
집단좌표는 **런당 표본이 하나**다. 이온을 늘려도 `Σ_i Δr_i` 는 여전히 시계열 하나다.
독립 표본 수 ≈ (궤적 길이)/(상관시간). `Fig. 3` 의 평탄 도달 ≈ 0.3–0.5 ps 를 상관시간으로 잡으면 **(우리 유도)**:

| | 궤적 | Li | 집단좌표 독립표본 ≈ |
|---|---|---|---|
| [Marc17NE] | **500 ps** | 20 | **~1000** |
| 우리 box331 | **400 ps** | 243 | **~800** |
| 우리 gen1 | **200 ps** | 27–58 | **~400** |

⇒ 🟢 **box331 은 저쪽과 같은 등급이다.** 🔴 **gen1 은 절반이다.** ⇒ **H_R 판정은 box331 로 간다.**
⚠ 이온 수 243 은 `D*` 쪽만 좋게 한다 — **`H_R` 의 분모를 안 고친다.**

**② 최소 3시드. 블록 오차만으로는 부족하다.**
저쪽은 시드가 없다(§10-2). 우리는 시드 산포 **1.0–4.8배**를 실측했다. **시드 산포가 진짜 정밀도다.**
⇒ box331 은 지금 `600 K 2시드 · 800/1000 K 1시드` 다. **800/1000 K 를 3시드로 채우기 전에는 값이 아니다** (그 json 의 `금지_서술` 과 일치).

**③ 창은 2–50 ps 를 유지하고, `D_σ` 적합의 R² 를 따로 본다.**
SI `Fig. S3` 이 하한 2 ps 를 지지한다(§7-4b). 그리고 우리 도구는 이미 `R² < 0.5` 면 **H_R 을 보류**한다 — gen1 에서 실제로 1건(`lpsocl/T600_s3`)이 걸렸다. **그 게이트를 끄지 마라.**

**④ 골격이 안 흐르는지 먼저 본다.**
저자 명시(§4-3): 골격이 확산하면 Eq. (6) 보정이 **결과를 바꾼다**. 우리 `b2o3 1200 K` creep 제외가 이 근거로 정당화된다. ⇒ **모든 H_R 런에 골격 creep 점검을 선행**한다.

**⑤ 🔴 열욕 시험 — 이게 새 항목이다.**
우리는 **Langevin 생산**이고 저쪽은 **NVE 생산**이다(§7-4c). 우리 `H_R` 이 1 쪽으로 희석됐는지는 **측정으로만** 답할 수 있다.
> **제안 (MD 재계산 최소)**: box331 평형 구조에서 **NVE 생산 세그먼트 하나**(같은 길이·같은 창)를 띄워 `--haven` 으로 같은 양을 잰다.
> · `H_R(NVE) < H_R(Langevin)` 이면 **열욕 희석이 실재**하고, 우리 0.60 도 상한이다.
> · 차이가 없으면 **τ ≈ 0.51 ps 가 충분히 약하다**는 것이 확인되고, 이 우려는 닫힌다.
> ⚠ **결과를 보기 전에 문턱을 등록한다** (CLAUDE.md 계산 규율). 보고량 카드 먼저.

> ⛔ **그리고 이 다섯을 다 채워도 `H_R` 은 아직 보고량이 아니다.** 우리 도구 docstring 이 적은 그대로
> *"이건 새 보고량이다 — 값으로 쓰려면 estimand 카드·문턱 선등록이 먼저다."*
> 이 논문은 그 요구를 **낮추지 않는다**.

### 12-2. 🔵 우리 도구에 추가할 만한 것 (사람이 결정)

| 제안 | 근거 | 비용 |
|---|---|---|
| **`H` 와 `H_c` 를 둘 다 출력** (골격 기준계 **적용 전/후**) | 저자가 두 값을 다 낸다. 차이(0.53→0.42, ≈20 %)가 **골격 역류의 크기**를 직접 준다 | 낮음 — `haven_curves(cart_ref=None)` 를 한 번 더 부르면 끝 |
| **블록 분석 오차막대** [Jones & Mandadapu] | 지금은 R² 게이트만 있고 **H_R 자체의 오차막대가 없다** | 중간 |
| **Eq. (5) 정적 요동 점검** (`Fig. 2` 레시피) | 종별 COM 요동을 `k_BT/m_s(1−M_s/M_tot)` 와 대조 = **MD 재계산 0 의 건강검진** | 낮음 |
| **종별 온도 등분배 점검** (`Fig. S1` 레시피) | CPMD 고유 문제이긴 하나 **Langevin 에서도 가벼운 원자가 먼저 깨진다**. 우리는 한 번도 확인한 적 없다 | 낮음 |

### 12-3. 🔵 우리가 아직 안 한 것 — `Ea(tracer)` vs `Ea(charge)`

이 논문의 가장 실용적인 결론은 **"Ea 는 tracer 로 내도 된다"** 다 (0.17 vs 0.18 eV).
우리는 `Ea` 를 **전부 tracer(D*) 로만** 내 왔고, **`D_σ` 로 아레니우스를 그려 본 적이 없다.**
> 🟢 **box331 은 600/800/1000 K 3점이 있으므로 MD 재계산 0 으로 `Ea(charge)` 를 낼 수 있다.**
> 두 `Ea` 가 우리 계에서도 겹치면, **`Ea` 축은 Haven 논쟁과 무관하다**를 우리 자료로 말할 수 있다.
> 이게 1저자 인용정책(*"상대차만 쓴다"*)에 **직접 도움이 된다** — `Ea` 가 안전지대임을 우리가 보이게 된다.
> ⚠ 단 `D_σ` 3점 아레니우스는 잡음이 커서 **오차막대가 tracer 보다 훨씬 넓을 것**이다 (`Fig. 4` 우상 참조).

### 12-4. 🟢 `convention_check.py` 규약에 원전이 생겼다

`MSD 창 2–50 ps` 의 **하한 2 ps** 가 지금까지 우리 내부 결정이었는데, SI §II.B 가 같은 하한을 권고한다.
⇒ 원고·SI 에 **인용 가능**: *"a fit window starting at 2 ps, following [Marcolongo & Marzari 2017]"*.
⛔ **상한 50 ps 는 여전히 우리 것**이다 — 저쪽 최대 창이 2 ps 다.

---

## 13. 인용 가능 문장 (영문 초안)

1. *"The Nernst–Einstein relation built on the tracer diffusion coefficient is an approximation; the exact linear-response expression involves the charge (collective) diffusion coefficient `D_σ`, and the two differ whenever carrier–carrier velocity cross-correlations are non-zero [Marcolongo & Marzari, Phys. Rev. Mater. 1, 025402 (2017)]."*
2. *"In the superionic conductor Li₁₀GeP₂S₁₂, first-principles molecular dynamics gives a Haven ratio `H = D_tr/D_σ` of 0.42 (isotropic, after referencing Li velocities to the rigid S/Ge/P sublattice), i.e. the tracer-based Nernst–Einstein estimate **underestimates** the ionic conductivity by roughly a factor of 2.5 [ibid.]."*
3. *"The correlation is strongly anisotropic, being largest along the fast c-axis channels (`H_c` = 0.36) and weakest in-plane (`H_c` = 0.61) [ibid.]."*
4. *"Importantly, the tracer and charge diffusion coefficients yield activation energies that agree within error (0.17 ± 0.01 and 0.18 ± 0.02 eV), so correlations enter the Arrhenius prefactor rather than the barrier [ibid.]."*
5. *"Because periodic boundary conditions with conserved total momentum force a counter-drift of the host matrix, the carrier velocities must be referenced to the non-diffusing sublattice before evaluating the collective correlation function [ibid., Eqs. (5)–(6)]."*
6. *"MSD fit windows shorter than ~2 ps sample an intermediate superdiffusive regime and bias both the diffusion coefficient and the apparent activation energy; we therefore fit over 2–50 ps [cf. ibid., Supplemental Material §II.B]."*

⛔ **쓰면 안 되는 문장**
- ✗ *"…이 논문이 아르지로다이트의 Haven 비를 보고했다"* — **LGPS 뿐이다.**
- ✗ *"…계산이 실험 Haven 을 재현했다"* — 실험값은 **다른 물질**(Li₁₀SnP₂S₁₂)이고 다결정이다 (§10-4).
- ✗ *"…H 는 온도에 무관하다"* 를 **상온까지** — 계산 최저온이 ≈513 K 다 (§10-7).
- ✗ *"…이 논문이 상관 강화의 상한을 정량화했다"* — `N_eff` 를 계산하지 않았다 (§10-1).
- ✗ *"…Haven 보정은 2.5배다"* 를 **우리 σ 에** — LGPS 값이다 (§7-3).

---

## 14. 주의 / 한계 (인용 규율)

1. ⛔ **계는 LGPS 하나다.** 아르지로다이트 0회. **값은 하나도 이식하지 않는다.**
2. ⛔ **`H = 0.42` 를 우리 σ_NE 에 곱하지 않는다.** `[Adeli] 0.23` 을 안 곱하는 것과 **똑같은 이유**다.
3. ⛔ **`Ea 0.17–0.18 eV` 를 우리 comp1/modelc Ea 옆에 나란히 놓지 않는다** (§11-1).
4. ⚠ **`figure-read ≈` 로 표시한 값은 그림에서 눈으로 읽은 것**이다 (§3c·§6-3·§6-4). 본문 명시값이 아니다.
5. ⚠ **`0.18 = 전하 / 0.17 = tracer` 배정은 우리 판독**이다 (§3b). 원문 문장이 모호하다.
6. ⚠ **`(우리 유도)` 표시**: dt 0.0968 fs · 5.17M 스텝 · Li 20/40 개 · 아레니우스 기울기 Ea · 창별 겉보기 Ea · 독립표본 수 · Langevin τ 0.51 ps — **전부 논문 미보고**다.
7. ⛔ **이 논문은 σ 절대값 금지를 풀지 않는다.** 오히려 **보정의 크기가 미정**임을 보여 **조인다** (§7-4c).
8. ⚠ **CPMD 고유 사항(emass·mass preconditioning·단열조건)은 우리 MLIP-MD 에 그대로 옮기지 않는다.** 우리는 가상 전자자유도가 없다.
9. ⛔ **`~0.3` 실험값은 Li₁₀SnP₂S₁₂ 다.** LGPS 실측 Haven 이 아니다.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **Tracer 확산계수 `D_tr` (= `D*`)** | 태그된 **한 입자**의 MSD 기울기/6. 모든 이온에 평균 | Eq. (1). MSD 와 VACF 두 표현이 같음을 명시 |
| **전하(집단) 확산계수 `D_σ`** | **캐리어 질량중심**의 확산계수. `σ` 에 **정비례** | Eq. (3) 의 Einstein 형. 이것만이 엄밀한 NE 의 입력 |
| **Haven 비 `H`** | `D_tr/D_σ`. `H<1` = 협동 이동 = NE 과소 / `H>1` = 이온쌍 = NE 과대 | LGPS `H_c(xyz)=0.42` |
| **Green–Kubo** | 수송계수를 **시간상관함수의 적분**으로 얻는 선형응답 공식 | Eq. (7) 의 `u`,`c`,`c̃` |
| **Einstein 관계** | 수송계수를 **변위 제곱의 장시간 기울기**로 얻는 등가 공식 | 저자는 안 쓰고 SI 에서 **함정**으로 다룸 |
| **VACF (속도 자기상관)** | `⟨v(t)v(0)⟩`. 적분이 `D` | `Fig. 3` 의 적분판 |
| **Backscattering (되튕김)** | 이온이 뛰었다가 되돌아오는 것. VACF 가 **음수**로 갔다 오는 진동으로 나타남 | `Fig. 3` 의 0.12 ps 골 / 0.21 ps 둘째 봉우리 |
| **Distinct term (교차항)** | `Σ_{j≠0}⟨v_j v_0⟩` — **다른 입자**와의 속도 상관. `D_σ − D_tr` 의 정체 | Eq. (4) 유도 |
| **Car–Parrinello MD (CPMD)** | 전자 파동함수에 **가상 질량**을 주고 이온과 함께 굴려 매 스텝 SCF 를 피하는 FPMD | `cp.x`, emass 300 amu |
| **Mass preconditioning (Fourier acceleration)** | 고주파 전자자유도에 **주파수 의존 질량**을 줘 dt 를 키우는 CPMD 기법 | **껐다** — Li/S 열평형을 깨뜨려서 |
| **단열조건 (adiabaticity)** | 가상 전자 운동에너지가 이온 것보다 훨씬 작게 유지되어 Born–Oppenheimer 면에 붙어 있는 상태 | `Fig. S2` (25배 격차) |
| **미시정준 앙상블 (NVE)** | 입자수·부피·**에너지** 고정. 열욕 없음 ⇒ 동역학 왜곡 없음 | **생산 전부 NVE** |
| **블록 분석 (block analysis)** | 시계열을 블록으로 나눠 블록평균의 분산으로 상관된 자료의 오차를 추정. **블록 길이에 수렴해야** 유효 | 이 논문의 유일한 오차원 |
| **초확산 (superdiffusive) 중간영역** | MSD ∝ t^α (α>1) 인 구간. 확산이 아직 아님 | SI `Fig. S3` 의 저온 인공물 원인 |
| **`N_eff`** | 상관시간 안에 태그 캐리어와 상호작용하는 **유효 입자 수**. 세기변수 | Eq. (4) 상한. **계산 처방 없음** |

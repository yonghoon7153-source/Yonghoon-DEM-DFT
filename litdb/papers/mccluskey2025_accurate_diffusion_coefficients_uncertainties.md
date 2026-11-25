# Accurate Estimation of Diffusion Coefficients and their Uncertainties from Computer Simulation — McCluskey, Coles & Morgan (J. Chem. Theory Comput. 2025)

> slug `mccluskey2025_accurate_diffusion_coefficients_uncertainties` · DOI `10.1021/acs.jctc.4c01249` · type `methods (통계추정기) + 고전 MD 검증` · PDF `a21a6645-84.…pdf` (+SI `2219d416-…pdf`) · digested `2026-09-09` · status ✅
> **저자**: Andrew R. McCluskey\* (Bristol Centre for Computational Chemistry · European Spallation Source ERIC DMSC · Diamond Light Source), Samuel W. Coles (Bath + Faraday Institution → 현 Cambridge), Benjamin J. Morgan\* (Bath + Faraday Institution) · *J. Chem. Theory Comput.* **2025**, 21, 79−87 · CC-BY 4.0 · 접수 2024-09-23 / 개정 2024-12-02 / 수리 2024-12-03 / 공개 2024-12-30 · arXiv 2305.18244

> elements: Li, La, Zr, O
> methods: MD

---

## 0. 이 digest 를 읽는 법 — 우리 ②축(MD 통계 불확실도)의 **현재 최선**

이 논문은 물성 논문이 아니다. **"MD 궤적 하나에서 D\* 와 그 오차막대를 어떻게 내야 맞나"** 하나만 판다.
물성값은 LLZO D\* 하나뿐이고, 나머지는 전부 3D 격자 random walk 다.

핵심 주장 세 줄:
1. MSD 의 시간점들은 **서로 강하게 상관**돼 있고 **분산도 시간에 따라 변한다**(heteroscedastic).
   순진한 OLS 는 이 둘 다 무시하므로 **통계적으로 비효율**이고, **자기 오차막대를 크게 과소평가**한다.
2. 올바른 답은 GLS(=공분산 행렬 Σ 를 쓰는 최소제곱)인데 Σ 를 모른다. → **자유확산 입자계의 해석적
   공분산 Σ′ 을 유도**하고, 그 **한 개의 미지수(분산 σ²[xᵢ])만 궤적 자체에서 추정**해 채운다.
3. 그 Σ′ 로 **베이지안 회귀(MCMC)** 를 돌리면 **궤적 하나로** GLS 급 정밀도 + 쓸 만한 오차막대를 얻는다.

우리와의 접점은 §7 에 전부 몰아뒀다. 미리 한 줄로: **우리 `MSD 2–50 ps · 자유절편 OLS` 는
D 값 자체는 안 틀리지만(불편), 오차막대는 20배쯤 낙관적이고, 같은 궤적에서 뽑아낼 수 있는
정밀도의 1/9 밖에 못 쓰고 있다.** 게다가 우리 정본 MSD 는 **단일 시간원점**이라 거기서 또
1/9 를 버린다 (§7-C, digest 계산).

> ⚠ **소환값 규율**: 아래 LLZO 수치는 전부 이 논문의 값이다. 우리 `db/properties/` 절대값과
> 같은 표에 놓지 않는다. 우리가 이식할 것은 **숫자가 아니라 추정 절차**다.

---

## 1. 한 줄 요약

MSD 시간점들의 **상관 구조를 자유확산 입자계의 해석적 공분산 행렬 Σ′ 로 모델링**하고 그 분산만
궤적에서 추정해 넣은 뒤 **베이지안 회귀(emcee MCMC)** 로 직선을 맞추면, **복제 궤적 없이 궤적
한 개만으로** GLS(Cramér–Rao 한계) 급 정밀도의 D\* 와 **믿을 만한 σ²[D̂\*]** 를 얻는다 —
OLS 는 같은 데이터에서 σ 가 4–5배 넓고 자기 오차를 10–26배 과소평가한다.

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 문제 | `D̂* = MSD 기울기/6` 은 **추정량**이다. 그 추정량의 **분포** p(D̂\*) 를 아무도 제대로 안 낸다 |
| 왜 지금 | 복제 궤적 여러 개로 σ 를 재는 건 정직하지만 **비용이 배로 든다**. 궤적 1개로 되게 하고 싶다 |
| 두 가지 결함 | ① **비효율**(σ[p(D̂\*)] 가 필요 이상으로 넓다) ② **오차막대 자체가 틀림**(OLS 교과서 식) |
| 왜 OLS 가 틀리나 | MSD 는 (a) **serially correlated** — x(t) 와 x(t+Δt) 는 같은 변위 이력을 공유 (b) **heteroscedastic** — σ²[xᵢ] 가 t 에 따라 커진다. OLS 의 두 가정이 **둘 다** 깨진다 |
| 해법 | Σ′ 해석해 + 분산 재스케일 + 최소고유값 재조건화 + MCMC 베이지안 회귀 |
| 구현 | **KINISI 1.1.0** (MIT, `github.com/kinisi-dev/kinisi`) |
| 재현 자료 | ESI repo `github.com/arm61/msd-errors` (showyourwork) · LLZO 궤적 Zenodo `10.5281/zenodo.10532134` |
| 검증계 | ① 3D 정육격자 random walk (해석적 정답 D\*=1) ② **cubic Li₇La₃Zr₂O₁₂ (c-LLZO)** 고전 MD |

## 3. 핵심 수치 (전부 소환값)

### 3.1 물성값 — 이 논문에 단 하나

| 물성 | 값 | 조건 | 출처 |
|---|---|---|---|
| D\*(Li) in c-LLZO | **≈ 0.9 × 10⁻⁵ cm² s⁻¹** (`figure-read ≈`) | 700 K, DIPPIM 분극이온 FF | `Fig. 5`a 히스토그램 중심 |
| σ[D̂\*] (192 유효궤적) | **≈ 0.05 × 10⁻⁵ cm² s⁻¹ (≈5–6 % 상대)** (`figure-read ≈`) | 각 유효궤적 = 28 Li × ~500 ps | `Fig. 5`a 분홍 ±1σ 막대 |
| σ, Ea, ESW, gap, 탄성 | **n/a** | — | 이 논문은 안 낸다 |

### 3.2 추정기 성능 — random walk 4096회 (`Fig. 1`, 논문의 핵심 표)

D\*=1 로 규격화된 무차원 단위. 분홍 막대 = 모집단 σ(진짜 퍼짐), 파랑 막대 = 방법이 스스로
보고하는 평균 σ̂. **막대는 ±1σ 라 폭이 2σ 다** (내가 `Fig. 1`c 피크 높이 20 ↔ 정규분포
1/(σ√2π) 로 교차확인).

| 방법 | 진짜 σ[p(D̂\*)] | 스스로 보고하는 σ̂ | σ̂/σ | 판정 |
|---|---|---|---|---|
| **OLS** | ≈ **0.078** (`figure-read ≈`) | ≈ 0.005 (`figure-read ≈`, 막대가 작아 판독 불확실) | ≈ **1/16** | 넓고 + 거짓말한다 |
| **WLS** (1/σ²ᵢ 가중) | ≈ **0.042** (`figure-read ≈`) | ≈ 0.0085 (`figure-read ≈`) | ≈ 1/5 | 좁아졌지만 여전히 거짓말 |
| **GLS** (참 Σ) | ≈ **0.020** (`figure-read ≈`) | ≈ 0.021 (`figure-read ≈`) | ≈ **1.0** | 정답 |

→ **σ_OLS / σ_GLS ≈ 3.9 (분산 15배)**. 같은 궤적에서 OLS 는 15배 더 많은 데이터를 버린다.

> ★ **내가 저장소 코드로 직접 재현했다** (repo 실측 · 256 시드, 논문의 4096 대신):
> kinisi 진짜 σ = 0.0135 / 보고 σ̂ = 0.0172 (**σ̂/σ = 1.27**, 즉 27 % 보수적) ·
> OLS 진짜 σ = 0.0740 / 보고 σ̂ = 0.00288 (**σ̂/σ = 0.039 = 1/26**) ·
> **σ_OLS/σ_kinisi = 5.48 (분산 30배)**. 논문 그림 판독과 같은 방향·같은 자릿수이고,
> OLS 과소평가 배수는 그림 판독(≈16×)보다 내 실측(≈26×)이 크다 — **작은 파랑 막대 판독이
> 부정확한 쪽**이므로 실측을 정본으로 본다.

### 3.3 실제 계(LLZO)에서도 같은가 — `Fig. S6`

512개 유효 시뮬레이션(**~25 ps · 56 Li**)에 OLS/WLS/GLS 를 적용:

| 방법 | 중심 D̂\* | 진짜 σ | 보고 σ̂ | σ̂/σ |
|---|---|---|---|---|
| OLS | ≈ 0.92×10⁻⁵ | ≈ **0.14×10⁻⁵** (`figure-read ≈`) | ≈ 0.015×10⁻⁵ | ≈ **1/9–1/10** |
| WLS | ≈ 0.92×10⁻⁵ | ≈ 0.078×10⁻⁵ (`figure-read ≈`) | ≈ 0.016×10⁻⁵ | ≈ 1/5 |
| GLS | ≈ 0.92×10⁻⁵ | ≈ **0.031×10⁻⁵** (`figure-read ≈`) | ≈ 0.031×10⁻⁵ | ≈ **1.0** |

→ **σ_OLS/σ_GLS ≈ 4.6 (분산 ≈21배)**. 세 방법의 **중심값은 같다** — 즉 **OLS 는 D 자체를
편향시키지 않는다. 편향은 오차막대에만 있다.** 이게 우리에게 제일 중요한 문장이다.

### 3.4 크기·길이 스케일링 — `Fig. 6` (내가 본 그림 중 가장 값진 것)

log₂–log₂. 네 방법(OLS 분홍 / WLS 파랑 / kinisi 초록 / GLS 주황).

| 축 | OLS | WLS | kinisi(Σ′) | GLS(Σ_num) |
|---|---|---|---|---|
| **(a) N_atoms** (16→1024, t_max=128 고정) | 기울기 ≈ **−1** | ≈ −1 | ≈ −1 | ≈ −1 |
| **(b) t_max** (16→1024, N=128 고정) | **≈ 0 — 평평하다** | ≈ **−0.5** | ≈ **−1.1** | ≈ −1.1 |

(전부 `figure-read ≈`. 논문 본문은 *"our method scales better than OLS or WLS as the total
simulation time is increased"* 라고만 쓰고 지수를 안 준다.)

> 🔴 **`Fig. 6`b 의 OLS 평평한 선이 이 논문에서 제일 무서운 그림이다.**
> 입자 수를 늘리면 네 방법 모두 σ² ∝ 1/N 으로 똑같이 좋아진다(패널 a, 평행선).
> 그런데 **궤적을 길게 늘리면 OLS 만 아무것도 안 좋아진다**(패널 b). t_max=1024 에서
> kinisi 의 σ² 는 OLS 보다 **≈2⁸ ≈ 250배** 낮다 (`figure-read ≈`).
> 이유: 긴 lag 의 MSD 점은 분산이 t² 로 폭증하는데 OLS 는 그걸 **똑같은 무게로** 넣는다.
> ⚠ 단, 패널 (b) 의 t_max 는 **총 시뮬 길이**이지 *적합 창의 상한*이 아니다 — 우리 2–50 ps 창
> 논의와 헷갈리면 안 된다 (§7-D 에서 분리해 다룬다).

### 3.5 자기 오차막대의 정확도 — `Fig. 4`d, `Fig. 5`b

| 계 | 진짜 σ²[D̂\*] | 추정 σ̂²[D̂\*] 분포 중심 | 비 |
|---|---|---|---|
| random walk (`Fig. 4`d) | ≈ 2.0×10⁻⁴ (`figure-read ≈`) | ≈ 2.9×10⁻⁴ (`figure-read ≈`) | **≈1.45× 과대**(σ 로 1.2×) |
| LLZO (`Fig. 5`b) | ≈ 0.55×10⁻¹³ cm⁴s⁻² (`figure-read ≈`) | ≈ 1.2×10⁻¹³ (`figure-read ≈`) | **≈2× 과대**(σ 로 1.5×) |

→ **kinisi 는 보수적이다** (과대평가). SI S-III 가 그 원인을 명시: Σ′ 을 **추정 분산**으로 채웠기
때문이다. 참 Σ_num 을 쓰면 이 편향이 사라진다(`Fig. S5`b). 그리고 SI 는 **의도적 선택**임을 밝힌다 —
*"we consider overestimation of σ²[D̂\*] to always be preferable to underestimation"* (과대는 더
돌려서 줄일 수 있지만, 과소는 **틀린 확신**을 만든다).

### 3.6 시뮬레이션 제원

| 항목 | random walk | LLZO |
|---|---|---|
| 계 | 3D 정육격자 무작위 걸음 | cubic Li₇La₃Zr₂O₁₂ |
| 크기 | **128 입자 × 128 스텝** | **2×2×2 슈퍼셀, 1536 원자 (Li 448)** |
| 반복 | **4096회**(기준분포) / **512회**(`Fig. 6` 각 점) | 단일 6 ns 궤적 |
| 코드/힘장 | — (jump = √6 → D\*=1, **repo 실측** `Snakefile` `jump=2.4494897428`) | **METALWALLS** + **DIPPIM 분극이온 FF** (Burbano et al. 파라미터) |
| 앙상블/T | — | **NVT, 700 K**, Nosé–Hoover τ = 121 fs (5000 ℏ/E_h) |
| 시간 | 128 스텝 | **6 ns, dt 0.5 fs** |
| 확산영역 시작 | **t = 2 스텝** | **t = 10 ps** (ballistic·subdiffusive 제거) |
| 유효궤적 분할 | — | **192개** = (6 ns/500 ps=12) × (448 Li 를 28개씩 16조, 비복원 무작위) |

> ⚠ **DFT 는 한 줄도 없다.** functional·PAW·k-point·ecut·DFT+U·무질서 처리 전부 **n/a**.
> 이건 고전 MD + 통계다. "이 논문이 DFT 로 뭘 했다" 는 서술은 전부 틀린 인용이다.

---

## 4. 방법 ★ — 추정기 해부 (이 논문의 본체)

### 4.1 무엇을 추정하는가

관측 MSD 는 벡터 **x**, 원소 xᵢ = (1/N(t)) Σⱼ [Δrⱼ(t)]². 궤적 하나가 주는 **x** 는
"가능한 모든 복제 궤적이 만드는 MSD 모집단" p(**x**) 에서 뽑힌 **한 개의 표본**이다.
거기에 직선을 맞추면 D̂\* 가 나오고, D̂\* 들의 모집단이 p(D̂\*) 다.
**좋은 추정기 = (i) 불편 (ii) p(D̂\*) 가 최대한 좁다(=통계적 효율) (iii) 그 폭을 스스로 맞게 안다.**

### 4.2 OLS → WLS → GLS 사다리

- **OLS**: 독립·등분산 가정. MSD 는 **둘 다 아니다** → 비효율 + 오차 과소.
- **WLS**: 잔차를 1/σ²[xᵢ] 로 가중 → 이분산은 고침. **상관은 여전히 무시** → 아직 비효율·과소.
- **GLS**: β̂ = (Aᵀ Σ⁻¹ A)⁻¹ Aᵀ Σ⁻¹ **x** (식 3). A = [**1** **t**] 모델행렬.
  상관+이분산 둘 다 고침 → **Cramér–Rao 하한 달성**(이론적 최대 효율) + 해석적 오차가 정확.
  **문제: Σ 를 모른다.**

### 4.3 Σ′ — 자유확산 입자계의 해석적 공분산 (SI S-I 유도)

1D 랜덤워크(스텝 ±κ)에서 n 스텝 후:
- ⟨xₙ⟩ = nκ² (식 S-4)
- ⟨xₙ²⟩ = (3n²+n)κ⁴ → n→∞ 에서 3n²κ⁴ (식 S-10, S-11)
- **σ²[xₙ] = 2n²κ⁴** (식 S-12) — **분산이 시간의 제곱으로 커진다**
- 공분산: ⟨xₙ x_{n+m}⟩ 의 4중합에서 **겹치지 않는 구간은 평균 0** 이라 살아남는 항이
  **겹치는 n 스텝에만 의존** → **Σ′[xₙ, x_{n+m}] = 2n²κ⁴** (식 S-27)
  = **σ²[xₙ] 과 똑같다.** 즉 "긴 lag 과 짧은 lag 의 공분산 = 짧은 쪽의 분산".

독립 관측 수 N′ 로 나누고 d 차원으로 확장하면 논문 **식 6**:

> **Σ′[xᵢ, xⱼ] = Σ′[xⱼ, xᵢ] = σ²[xᵢ] · N′ᵢ / N′ⱼ,  ∀ i ≤ j**

t 로 쓰면 식 S-32: Σ′[x(t₁), x(t₂)] = 8d(D\*)² t₁² · N′(t₂)/N′(t₁), ∀t₁≤t₂.

**이 한 줄이 "공분산 행렬을 쓰나?" 의 답이다 — 쓴다. 그것도 데이터에서 추정한 전체
공분산이 아니라, 형태를 해석적으로 고정하고 스케일만 데이터에서 받는다.**

### 4.4 σ²[xᵢ] 를 궤적 하나에서 얻는 법 — **분산 재스케일** (식 7)

> **σ̂²[xᵢ] = σ²[Δrᵢ²] / N′ᵢ**

즉 **관측된 제곱변위들의 분산**을 **수치적으로 독립인 부분궤적 수 N′ᵢ 로만** 나눈다.

★ **핵심은 N′ᵢ 의 정의다**: **겹치지 않는(non-overlapping) 시간창의 개수 × 이동입자 수**
= **N′ᵢ = N_atoms × N_t / i** (Methods 명문). **총 관측 수 N_atoms×(N_t−i) 로 나누면 안 된다** —
겹치는 창에서 나온 제곱변위는 서로 상관돼 있어 독립 관측이 아니다 (`Fig. S1` 도식:
Δr₁ 과 Δr₅ 는 h₅+h₆+h₇+h₈ 을 공유한다).

> 💡 우리에게 직접 꽂히는 함정: `tools/modelc_v3/disorder_ensemble_diffusion.py::msd_multi_origin`
> 이 저장하는 `norig = nt − L` 은 **겹치는 원점 수**다. 그걸 독립수로 쓰면 짧은 lag 에서
> 독립성을 최대 L 배 과대계상한다 (§7-E).

### 4.5 재조건화 — 최소고유값법

식 7 의 σ̂² 는 잡음이 있어 Σ′ 이 특이하거나 조건수가 폭발한다 → **minimum eigenvalue method**
(doi:10.1080/16000870.2019.1696646) 로 조건수를 **사용자 지정 cond_max = 1×10¹⁶** 로 고정.
(repo 실측: 그 뒤에 statsmodels `cov_nearest` 까지 한 번 더 통과시킨다.)

### 4.6 베이지안 회귀 — 이 논문이 "부트스트랩이 아니라 베이지안"인 이유

로그우도 = **다변량 정규**(식 5):
`ln p(x|m) = −½[ ln|Σ| + (x−m)ᵀ Σ⁻¹ (x−m) + k ln 2π ]`, m = 6D\*t + c.

| 항목 | 값 |
|---|---|
| **사전분포** | **improper prior D\* ≥ 0** (그것 하나뿐. 사실상 비정보 균등) |
| 초기값 | OLS 로 기울기·절편 → 그걸 시작점으로 **음의 MAP 최소화** |
| 샘플러 | **emcee** (Goodman–Weare affine-invariant ensemble) |
| 설정 | **32 walkers × 1500 steps, burn-in 500, thin 10 → 3200 표본** |
| 역행렬 | Moore–Penrose 유사역행렬(Hermitian) |
| 절편 | **자유 절편 c 를 같이 적합** (기본값) |

논문은 *"in the absence of additional prior information, [베이지안의 평균] is equal to the
estimate obtained from GLS"* 라고 명시한다 — **베이지안은 GLS 를 감싼 것이고, 얻는 것은
"점추정+해석적 오차" 대신 **완전한 사후분포** p(D\*|x) 다. Arrhenius 같은 하류 분석에
그 분포를 통째로 넘길 수 있다는 게 실질 이득이다.

> ⛔ **"부트스트랩"이 아니다.** 논문 본문에 bootstrap 이라는 단어가 **한 번도 안 나온다**.
> (kinisi 의 클래스 이름이 `MSDBootstrap`, 메서드가 `bootstrap_GLS` 라서 오해하기 쉽다 —
> **레거시 작명**이고 기본값이 `bootstrap=False` 다. repo 실측 §6.3.)

### 4.7 분산 추정: 재스케일 vs 블록 재규격화 (SI S-II)

대안은 **Flyvbjerg–Petersen 블록 재규격화**(인접 2개씩 평균 → 반복 → 평탄역 채택).

| | 분산 재스케일 (식 7) | 블록 재규격화 (pyblock) |
|---|---|---|
| σ̂²[xᵢ] 의 매끄러움 | **매끄럽다** | **잡음이 크다** (`Fig. S3`e 산포) |
| 편향 방향 | **긴 t 에서 과대** | **체계적으로 과소**(하한만 주는 추정기라, 식 S-35) |
| p(D̂\*) 폭 | **더 좁다** | 더 넓다 (Σ′ 이 잡음 → 조건화 실패 → 수치불안정) |
| σ²[D̂\*] | **과대**(안전) | **과소**(위험) |
| 왜 | MSD 의 **상관 길이를 이미 안다**(겹침 구조) → 추정할 필요가 없다 | 상관 길이를 매 lag 마다 **수치로 다시 추정**해야 한다 |
| 판정 | ✅ 채택 | ❌ |

> 이건 우리 [Kahle20] 이 쓰는 **블록 분산 오차**에 대한 정면 반론이다 (§7-F).

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a–c | RW 4096회에서 OLS/WLS/GLS 의 p(D̂\*). 분홍=진짜 σ, 파랑=스스로 보고한 σ̂ | **이 논문의 한 장 요약.** OLS 는 넓고(σ≈0.078) 자기 오차를 1/16 로 말한다. GLS 는 좁고(0.020) 정직하다. **세 중심값이 같다 = OLS 는 D 를 편향시키지 않는다** |
| 2a–c | 4096회의 참 분산(a) vs 단일 궤적 추정 분산(b), 그리고 산포도(c) | 식 7 이 **궤적 하나로** 참 분산을 잡는다는 증거. (c) 는 1:1 선 근처, 큰 σ² 쪽에서 살짝 위(과대) |
| 3 | MSD 공분산 행렬 3종(수치 Σ / 해석 Σ′ / 추정) + 쌍별 비율 패널 | **상관 구조가 어떻게 생겼는지 보는 그림.** 비율 패널이 대부분 0.9–1.25 인데 **i 또는 j ≲ 5–10 인 가장자리만 자홍(≤0.5)** = **짧은 lag 에서 모델이 분산을 2배 이상 과대평가**. 우리 2 ps 하한이 바로 그 구역이다 |
| 4a–d | (a) 단일 궤적 MSD + 사후 직선다발 (b) p(D\*\|x) (c) 4096회 점추정 분포 vs 이론최적 (d) σ̂² 분포 vs 참값 | (a) 에서 **관측 MSD 가 긴 t 에서 사후 직선다발보다 아래로 처지는데도 적합이 안 끌려간다** — 상관을 알기 때문. (c) 우리 방법이 이론최적보다 **≈17 % 넓다**(피크 26 vs 30.5, `figure-read ≈`) (d) σ̂² 가 **1.45배 과대** |
| 5a,b | LLZO 192 유효궤적의 p(D̂\*) 와 σ̂² 분포 | **28 Li × 500 ps 라는 작은 유효궤적에서도 작동**한다는 실제계 증거. 우리 셀(27 Li·200 ps)과 **거의 같은 통계 체급** |
| 6a,b | σ²[D̂\*] 의 N_atoms(a)·t_max(b) 스케일링, 4방법 | 🔴 **(b) 에서 OLS 만 평평하다 — 오래 돌려도 OLS 의 오차는 안 준다.** kinisi/GLS 만 ∝1/t. 우리 "200 ps 로 늘렸으니 좋아졌겠지" 를 정면으로 부순다 |
| S1 | 겹치는 시간창이 왜 상관되는가 도식 (Δr₁·Δr₅ 가 h₅–h₈ 공유) | N′ᵢ 를 **겹치지 않는 창 수**로 세야 하는 이유. 우리 `norig=nt−L` 함정의 근거 |
| S2 | Flyvbjerg–Petersen 블로킹 연산 도식 | 대안 방법의 정의 |
| S3a–e | 분산 재스케일(b,c) vs pyblock 블록 재규격화(d,e) | **c 는 조밀·매끄럽고 1:1 위쪽(과대), e 는 흩어지고 1:1 아래쪽(과소)** — 블록법이 왜 지는지 눈으로 보인다 |
| S4a–d | 두 분산 추정법이 p(D̂\*)·p(σ̂²) 에 주는 차이 | 둘 다 불편이지만 재스케일 쪽이 좁다 |
| S5a,b | 참 Σ_num 을 썼을 때의 p(D̂\*)·p(σ̂²) | σ̂² 의 과대편향이 **Σ′ 근사 탓**임을 격리 증명 |
| S6a–c | LLZO(512 유효 · ~25 ps · 56 Li)에서 OLS/WLS/GLS | **실제계에서도 `Fig. 1` 과 똑같다.** σ_OLS/σ_GLS ≈ 4.6, OLS 는 자기 오차를 1/9–1/10 로 말한다 |

**본 그림 / 안 본 그림** — 크로핑 12장(본문 6 + SI 6) 중 **8장을 실제로 열어 봤다**:
`Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. 6` · `Fig. S3` · `Fig. S6`.
**안 본 것: `Fig. S1`·`Fig. S2`(둘 다 도식이고 SI 본문이 완전히 서술) · `Fig. S4`·`Fig. S5`
(SI 본문 서술로 충분한 보조 검증).** 위 표의 그 4행은 **캡션·SI 본문 기준**이고
`figure-read` 표기를 붙이지 않았다.

> 🔧 **크로핑 도구 결함 1건 (보고)**: `tools/litdb/extract_figures.py` 의 `CAP_RE` 는
> 라벨을 `S?\d+` 로 잡아서 REVTeX 식 **`FIG. S-1.`(하이픈)** 을 못 잡는다 → 이 SI 에서 **0장**이
> 나왔다. 동시 실행 중인 다른 curator 와 충돌할까 봐 **공용 도구를 고치지 않고** 스크래치
> 스크립트로 S1–S6 을 직접 크로핑해 `figures.json` 에 병합했다. 나중에 `S?-?\d+` 로 고치고
> `S-1 → S1` 정규화만 넣으면 된다.

---

## 6. Post-processing / **코드 저장소 실측** ★

### 6.0 clone 결과

**✅ 성공.** `git clone --depth 50 https://github.com/arm61/msd-errors ~/msd-errors-check`
(repo 밖). 파일 55개, `.git` 제외. **네트워크 프록시 문제 없었다.**

- **라이선스**: 코드 **MIT** (`src/code/LICENSE`, `src/scripts/LICENSE`), 원고 **CC BY-SA 4.0**.
  → **우리 파이프라인에 흡수해도 라이선스 문제 없다.**
- 이 저장소는 **논문 재현 워크플로**(showyourwork/Snakemake)이지 **추정기 본체가 아니다.**
  추정기는 **PyPI 패키지 `kinisi`** 에 있다.

### 6.1 ★★ 추정기 구현 위치 (경로 + 함수명)

전부 `kinisi` 1.1.0 패키지 안이다 (`pip install kinisi==1.1.0`, wheel 33.1 MB).

| 역할 | 경로 · 함수 |
|---|---|
| **본체 (GLS+MCMC)** | `kinisi/diffusion.py` → **`Bootstrap.bootstrap_GLS()`** (L305) |
| 공분산 조립 | `kinisi/diffusion.py` → **`Bootstrap.generate_covariance_matrix()`** (L397) |
| 식 6 채우기 | `kinisi/diffusion.py` → **`_populate_covariance_matrix()`** (L838) — `ratio = n_samples[i]/n_samples[j]; value = ratio*variances[i]` = 식 6 그대로 |
| 재조건화 | `kinisi/diffusion.py` → **`minimum_eigenvalue_method()`** (L870) + statsmodels `cov_nearest` |
| 식 7 분산 | `kinisi/diffusion.py` → **`MSDBootstrap.__init__()`** (L552): `self._v = np.var(d_squared, ddof=1)/n_o[i]` |
| **N′ᵢ 계산** | `kinisi/parser.py` → **`Parser.get_disps()`** (L170–221): `n_samples = disp.shape[0] * time_intervals[-1] / time_interval` = **N_atoms × N_t/i** ✅ 식 7 과 일치 |
| 직선 모델 | `kinisi/diffusion.py` → `_straight_line()` (L857) |
| D 변환 | `Bootstrap.diffusion()` (L427): `Distribution(gradient.samples/(2e4*dims))` → Å²/ps → cm²/s |
| **Arrhenius** | `kinisi/arrhenius.py` → `StandardArrhenius` / `SuperArrhenius` (uravu `Relationship`). **D 를 분포로 받아 Ea 를 분포로 준다** + `extrapolate(T)` + 베이지안 evidence 로 Arrhenius vs super-Arrhenius 비교 |
| 논문 기준 OLS | (ESI) `src/code/random_walks/ordinary_rw.py` — `linregress(x,y)`, `slope/6`, `stderr/6` |
| 논문 기준 GLS/WLS/OLS | (ESI) `src/code/random_walks/glswlsols.py`, `src/code/llzo/glswlsols.py` |

> ★ **repo 실측 주의점 1 — `model` 기본값이 `False` 다.**
> `bootstrap_GLS(..., model: bool = False, ...)`. `model=False` 면 식 7 의 **원 재스케일 분산**을
> 그대로 Σ′ 에 넣고, `model=True` 면 거기에 **σ² = a·Δt²/N′ᵢ 를 한 번 더 피팅**해 매끄럽게 한다.
> ESI 의 `kinisi_rw.py` 는 `model` 을 안 넘긴다 → **논문 그림은 `model=False`(원 재스케일)** 이다.
>
> ★ **repo 실측 주의점 2 — 이름이 거짓말한다.**
> `MSDBootstrap(bootstrap=False, block=False)` 가 기본값이다. **리샘플링을 안 한다.**
> `bootstrap=True` 는 옛 kinisi 의 방식, `block=True` 는 SI 가 비교한 pyblock 경로다.
> 논문의 방법 = **기본값**.

### 6.2 ★★ 입력 형식 — 우리 UMA-MD 궤적을 바로 먹일 수 있나

**✅ 먹는다.** `kinisi/diffusion_analyzer.py::DiffusionAnalyzer` 에 진입점이 5개:

| 진입점 | 입력 |
|---|---|
| **`from_ase`** | `list[ase.Atoms]` ← **우리 extxyz 궤적이 여기로 바로 들어간다** |
| `from_pymatgen` | `list[Structure]` |
| `from_Xdatcar` | VASP XDATCAR |
| `from_file` | 파일 경로 |
| `from_universe` | MDAnalysis Universe |

`dtype` 인자로 **복제 궤적 처리**까지 지원한다:
- `dtype=None` — 궤적 1개
- **`dtype='identical'`** — **같은 시작점·다른 시드 = 우리 3-seed**. 각 궤적을 따로 파싱한 뒤
  **변위를 쌓고 N′ᵢ 를 더한다** (`n_o += i._n_o`) ← **이게 우리 시드 합치기의 정답 구현이다**
- `dtype='consecutive'` — 이어붙인 연속 궤적

`ASEParser` 주요 인자: `specie`('Li') · `time_step`(ps) · `step_skip`(덤프 간격, 스텝) ·
`min_dt`/`max_dt`/`n_steps`/`spacing`('linear'|'logarithmic') ·
**`sampling`('multi-origin' 기본 | 'single-origin')** · `framework_indices`(드리프트 보정) ·
`specie_indices`+`masses`(분자 COM) · `dimension`('xyz' 부분집합 → 2D 확산) · `memory_limit`(기본 8 GB).

**내가 실제로 돌렸다** (repo 실측): 합성 extxyz 1001 프레임 / 48 Li / 200 ps / 0.2 ps 덤프 →
`from_ase` → `.diffusion(2.0)` 이 **5.2 초**에 완주, D̂ = 9.74×10⁻⁶ ± 2.66×10⁻⁷ cm²/s
(참값 1.00×10⁻⁵, 1σ 안).

### 6.3 ★ 의존성 — 가볍다

`kinisi` 설치가 끌고 오는 것 전부: `numpy scipy statsmodels scikit-learn pandas matplotlib
emcee uravu dynesty uncertainties tqdm` (+ 잡다). **pymatgen·ASE·MDAnalysis 는 필수가 아니다**
(파서에서 지연 임포트). `emcee` ✅ · `uravu` ✅(저자 자작, Arrhenius 용) · **`kinisi` 자체가
그 "무거운 패키지"가 아니다** — 3천 줄짜리 순수 파이썬이다.
→ **우리 uma env 에 넣어도 부담 없다.**

### 6.4 🔴 이식 차단요소 2건 (내가 직접 밟았다)

**① NumPy 2.x 에서 파서가 죽는다**
```
kinisi/parser.py:193   disp_mem += np.product(...)
AttributeError: module 'numpy' has no attribute 'product'
```
`np.product` 는 **NumPy 2.0 에서 제거**됐다. 저장소 `environment.yml` 은 `numpy=1.26.4` 로 못
박아 뒀지만 **우리 uma env 는 보통 numpy≥2** 다.
→ 해법: (a) `numpy<2` 전용 venv 로 분리 (권장 — UMA 환경을 안 건드린다) 또는
(b) 임포트 전 `np.product = np.prod` 한 줄 심기. **(b) 로 통과하는 것을 확인했다.**

**② 🔴 `sampling='single-origin'` 이 잘못 색인된다 — 우리에게 치명적이다**
```python
# kinisi/parser.py  get_disps()  L202-203
if self.sampling == 'single-origin':
    disp = drift_corrected[self.indices, i:i + 1]     # i = 루프 카운터
```
가로축은 `time_intervals[i]` 로 라벨하는데 변위는 **프레임 `i`** 에서 가져온다.
`n_steps` 가 프레임 수보다 작으면 둘이 어긋난다. **실측**:

| 설정 (합성궤적, 참 D\*=1.00×10⁻⁵, 501 프레임) | 나온 D | 참값 대비 |
|---|---|---|
| multi-origin, n_steps=100 | 9.81×10⁻⁶ | **0.981** ✅ |
| **single-origin, n_steps=100** | **1.60×10⁻⁶** | **0.160** 🔴 |
| single-origin, **n_steps=500**(프레임당 lag 1개) | 8.71×10⁻⁶ | 0.871 ✅(단일원점 잡음 범위) |

`n_steps`=100/500 프레임 → 어긋남 배수 5 ↔ 관측 0.160 ≈ 1/5(+절편). **색인 어긋남으로 확정.**
⚠ **우리 정본 MSD 가 바로 single-origin 이므로**, "우리 규약에 맞추자"고 `sampling='single-origin'`
을 켜면 **D 가 조용히 5배 틀린다.** `n_steps = 프레임 수` 를 같이 주지 않으면 안 된다.
(원 코드의 의도까지 단정하진 않는다 — 내가 확인한 것은 **관측된 배수**다.)

### 6.5 예제·테스트·논문 재현 스크립트

- ESI 저장소 자체가 **곧 사용법**이다: `Snakefile` + `showyourwork.yml` 이 각 그림을
  만드는 규칙을 다 적어 뒀다.
- 그림 생성기: `src/scripts/{msd,diffusion,covariances,true_cov,stat_eff,glswlsols,
  glswlsols_llzo,pyblock,random_walk,msd_blocking}.py`
- 데이터 생성기: `src/code/random_walks/*.py` (`kinisi_rw.py`·`ordinary_rw.py`·`true_ls.py`·
  `truecov_rw.py`·`weighted_rw.py`·`stat_eff.py`), `src/code/llzo/many_runs.py`
- ⛔ **`src/data/` 는 .gitignore 라 clone 에 데이터가 없다.** LLZO 원궤적은
  Zenodo `10.5281/zenodo.10532134` 에서 `traj0..5.out` 로 받아야 한다 (**나는 안 받았다**).
- **`showyourwork build` 는 안 돌렸다** — 데이터 다운로드 + conda 환경 구축이 필요하고,
  그럴 필요가 없었다. 대신 **`kinisi` 를 직접 설치해 저장소의 생성기 코드를 돌렸다**(§3.2 회색상자).
- `kinisi/tests/` 존재(패키지 동봉). **돌리진 않았다.**

---

## 7. 우리 대비 ★★ — `our_dft_baseline.md` · `CLAUDE.md` MLIP-MD 규약

우리 규약: **UMA-s-1p1(omat) · Langevin NVT · dt 2 fs · friction 0.02 · equil 5 ps / prod 200 ps ·
덤프 100 fs · MSD 창 2–50 ps 고정 · 자유절편 OLS · 시드 3 · Arrhenius 600/800/1000 K ·
σ 는 Nernst–Einstein(Haven=1, 절대값 인용 금지)**.
보고량: **`D_rel(design,host) = D*(design)/D*(host)` @600 K** (비준, cell-conditioned).

### 7.0 digest 계산의 성격 (먼저 밝힌다)

아래 §7-B~E 의 수치는 **내가 이 저장소의 kinisi 로 직접 돌린 합성 실험**이다. 표기 **"digest 계산"**.

**설계**: 20 Å 정육 셀 · **48 Li** 브라운 걸음(참 D\*=1.00×10⁻⁵ cm²/s) + 정지 골격(P₄S₄₀Cl₈) ·
**1001 프레임 · 0.2 ps 덤프 · 200 ps** = 우리 생산 궤적과 같은 모양 · **독립 반복 40회**.

⚠ **한계 3개를 먼저 적는다**:
1. **합성 걸음은 kinisi 의 가정(자유확산 입자) 그 자체다.** cage·backscatter 상관이 없다.
   → kinisi 의 **보정 정확도(σ̂/σ)** 는 여기서 실제보다 좋게 나온다. 그 부분의 실제계 증거는
   논문의 LLZO(`Fig. 5`b, `Fig. S6`)뿐이고 거기서도 **1.5–2배 과대** 방향이었다.
2. 우리 실제 셀은 **Li 27개**(b2o3 계는 58원자 셀), 여기선 48개. 다만 `Fig. 6`a 가
   **네 방법의 σ²–N_atoms 기울기가 모두 −1 로 평행**임을 보이므로, **방법 간 비(比)** 는
   N 에 거의 무관하다 → 아래 배수는 N=27 에도 옮겨도 된다. **절대 σ 는 옮기면 안 된다.**
3. 반복 40회 → sd 추정의 상대오차 ≈ 1/√(2·39) = **11 %**. 1.1배 이내 차이는 유의하지 않다.

### 7.A 방법 규약 대조

| 항목 | 이 논문 (kinisi) | 우리 | 판정 |
|---|---|---|---|
| 적합 모델 | 직선 + **자유 절편** | 직선 + **자유 절편** | ✅ **일치** |
| 회귀 | **베이지안(≈GLS), Σ′ 사용** | **OLS** | 🔴 **여기가 전부다** |
| MSD 시간원점 | **multi-origin 기본** | **single-origin**(정본 `msd_per_elem_A2`) | 🔴 §7-C |
| 확산영역 시작 | 사용자 지정 (LLZO **10 ps**) | **2 ps** | ⚠ §7-D |
| 적합 상한 | **없음**(궤적 끝까지) | **50 ps** | ⚠ §7-D |
| 복제 궤적 | `dtype='identical'` 로 N′ᵢ 합산 | **시드 3개를 따로 적합해 산포로** | 🔵 §7-F |
| 오차막대 | 사후분포 σ̂²[D̂\*] | **시드 3개 산포** (Ea 0.197±0.032) | 🔵 상보 |
| Arrhenius | D **분포**를 MCMC 로 전파 → Ea 분포 | 3점 선형회귀 | 🔵 이식 후보 |
| σ 환산 | **안 한다** (D\* 만) | NE(Haven=1), **절대값 비인용** | ✅ 정신 일치 |
| 무질서 처리 | n/a (단일 LLZO 배열) | ensemble | — (이 논문 범위 밖) |

### 7.B ★ 우리 자유절편 OLS 가 얼마나 틀리나 — **방향과 크기**

**답을 두 부분으로 나눠야 한다. 섞으면 틀린다.**

**(i) D 값 자체 — 편향 없다.**
`Fig. 1`·`Fig. S6` 에서 OLS/WLS/GLS 의 **중심값이 같다**. 내 실측에서도
OLS 평균 = 9.976×10⁻⁶ (참 1.00×10⁻⁵, **−0.24 %**), kinisi 평균 = 1.0002×10⁻⁵ (**+0.02 %**).
→ ⛔ **"우리 D 가 과대/과소다" 라고 쓰면 안 된다. 안 틀린다.**

**(ii) 오차막대 — 과소평가다. 방향이 확실하고 크기는 한 자릿수 이상.**

| 근거 | OLS 가 자기 σ 를 몇 배 과소평가하나 |
|---|---|
| 논문 `Fig. 1`a (RW 4096) | ≈ **16×** (`figure-read ≈`, 막대 작아 부정확) |
| 논문 `Fig. S6`a (LLZO 실제계) | ≈ **9–10×** (`figure-read ≈`) |
| **repo 실측** — RW 256 시드 | **26×** |
| **digest 계산** — 우리 궤적 모양, multi-origin MSD + 우리 OLS 2–50 ps | **18×** |
| **digest 계산** — 우리 **실제 파이프라인**(single-origin MSD + OLS 2–50 ps) | **23×** |

> 🔴 **판정: 우리가 OLS `stderr` 로 오차막대를 그린다면 그 막대는 참 산포의 1/20 쯤이다.**
> 다행히 **우리는 그러고 있지 않다** — 우리 오차막대는 **시드 3개의 산포**다.
> 그건 **이 논문이 "정직하지만 비싸다"고 부른 바로 그 방법**이고, 원리적으로 옳다.
> ⇒ **우리 오차막대 관행에는 이 논문이 흠집을 못 낸다. 흠집은 정밀도 쪽에 난다(§7-C).**

**(iii) 그리고 실제 정밀도** — digest 계산, 우리 궤적 모양 · 40회 반복:

| 파이프라인 | 평균 D̂ | 편향 | **진짜 산포 sd** | 보고 sd | 보고/진짜 |
|---|---|---|---|---|---|
| **D. 우리 실제**(single-origin MSD + OLS 2–50 ps) | 1.0274×10⁻⁵ | +2.7 %(유의하지 않음, SE 2.4 %) | **1.53×10⁻⁶ (14.8 %)** | 6.50×10⁻⁸ | **0.04** |
| A. multi-origin MSD + 우리 OLS 2–50 ps | 9.976×10⁻⁶ | −0.2 % | 5.17×10⁻⁷ (5.2 %) | 1.37×10⁻⁸ | 0.03 |
| B. kinisi, multi-origin, **같은 2–50 ps 창** | 1.0000×10⁻⁵ | +0.00 % | **1.63×10⁻⁷ (1.6 %)** | 4.98×10⁻⁷ | 3.05 |
| C. kinisi, multi-origin, 2–200 ps 전체 | 1.0007×10⁻⁵ | +0.07 % | 1.77×10⁻⁷ (1.8 %) | 2.59×10⁻⁷ | 1.46 |

### 7.C ★★ 손실의 분해 — **두 겹이고, 곱해진다**

| 무엇을 바꾸면 | 비교한 두 행 | 분산 개선 배수 |
|---|---|---|
| 시간원점 평균만 (single → multi-origin), **추정기는 우리 OLS 고정** | D → A | **8.7×** |
| 추정기만 (OLS → kinisi), **데이터는 multi-origin 고정** | A → B | **10.0×** |
| **둘 다** (= 우리 현재 → kinisi 표준) | D → B | **87×** (=8.7×10.0 ✅ 일관) |

> ⚠ **"kinisi 를 single-origin 데이터에 그대로 적용" 조합은 측정할 수 없었다** — §6.4② 의
> 색인 버그 때문에 그 경로가 D 를 −65 % 로 뱉는다. 그래서 위 분해는 **우리 OLS 를 고정한 축**과
> **multi-origin 을 고정한 축**으로 짰다. 두 배수의 곱이 전체와 일치하므로 분해는 닫혀 있다.

> 🔴 **우리 파이프라인의 D 한 점은 kinisi 한 점의 1/87 짜리 정보다** (digest 계산, N=48).
> **두 손실이 거의 같은 크기(8.7 vs 10.0, 40회 반복의 ±11 % 안에서 사실상 동급)이고 곱해진다.**
> 그중 **시간원점 쪽은 새 코드도 새 이론도 필요 없다** — `msd_multi_origin` 이 이미 있다.
> **둘 다 MD 를 한 스텝도 더 안 돌리고 회수된다.**

우리 저장소에 이미 근거가 있다 — `tools/modelc_v3/disorder_ensemble_diffusion.py::msd_multi_origin`
docstring: *"With only 27 Li … that is 27 samples per lag — the curve is dominated by whichever few
ions happened to find a fast channel. Measured consequence: modelc 600 K has beta = 0.76 over
2–50 ps but 1.00 over 1–100 ps, and the slope changes 1.75x."*
**1저자가 2026-08-03 에 이미 물었던 그 질문이고, 이 논문이 그 답을 준다.**

### 7.D ★ 2–50 ps 창은 이 논문 기준으로 정당한가

**세 조각으로 갈라야 한다.**

**(1) 하한 2 ps — ⚠ 근거가 약하다. 이 논문은 LLZO 에 10 ps 를 쓴다.**
Methods: *"excluding the first 10 ps of MSD data in each case to remove short-time data
corresponding to the ballistic and subdiffusive regimes"*. 그들의 700 K LLZO 대 우리 600 K
아르지로다이트니 그대로 옮길 순 없다. 다만 **두 갈래로 우리 2 ps 가 위험구역**이다:
- `Fig. 3` 의 비율 패널에서 **i 또는 j ≲ 5–10 인 가장자리만 자홍(≤0.5)** = Σ′ 이 **짧은 lag 의
  분산을 2배 이상 과대평가**한다 (본문도 *"the approximation … that t is large … leads to an
  overestimation of the variance at low t"* 로 인정). 우리 2 ps 하한이 정확히 그 구역이다.
- 우리 실측 절편이 크다 — `db/properties/msd_3sys_200ps_origin.csv`: LPSOCl 600 K 절편
  **4.035 Å² = MSD@50 의 18.2 %**. 이 논문의 모델은 **절편 없는 자유확산**이 전제다.
  ⇒ **2 ps 하한은 "kinisi 가 인정하는 확산영역"이 아니라 "우리가 정한 값"이다.**
  이식할 때 `start_dt` 를 2/5/10 ps 로 스캔해 D̂ 가 평탄해지는 지점을 잡아야 한다.

**(2) 상한 50 ps — ✅ 정당하다. 그리고 이건 새 소득이다.**
논문은 상한을 **안 둔다**(궤적 끝까지 적합). `Fig. 6`b 만 보면 "길게 쓸수록 좋다"로 읽힌다.
**하지만 `Fig. 6`b 의 t_max 는 총 시뮬 길이이지 적합 창 상한이 아니다.**
같은 200 ps 궤적에서 창만 바꾼 digest 계산이 그걸 갈라 준다:
**kinisi 2–50 ps 진짜 sd = 1.63×10⁻⁷ vs 2–200 ps = 1.77×10⁻⁷ — 40회 반복의 ±11 % 해상도
안에서 구별 불가.** ⇒ **200 ps 궤적을 50 ps 까지만 적합해도 정밀도 손실이 없다.**
(직관: 정보는 궤적 길이에 있지, 긴 lag 점을 적합에 더 넣는 데 있지 않다. 긴 lag 점은
분산이 t² 로 크고 앞 점들과 거의 완전히 상관돼 새 정보가 거의 없다.)
⚠ 단, **보고 σ̂ 는 창을 좁히면 더 보수적이 된다** (보고/진짜 3.05 vs 1.46).

**(3) "창을 고정한다"는 규율 자체 — ✅ 유지.**
[Kahle20] 이 창을 물질별 custom 으로 뒀다가 본문↔SI 불일치를 낳은 선례가 있다.
이 논문은 창 선택 자체를 **사용자 판단**으로 넘긴다(*"this threshold is set by the user"*) —
**창 선택 규율을 주지 않는다.** 우리 고정창은 그 공백을 메우는 우리 규율이고, 바꿀 이유 없다.

### 7.E ★ 시드 3개로 충분한가 — **digest 계산**

**"충분"의 정의부터.** 시드 3개는 **두 가지를 동시에** 한다: (i) 궤적 간 통계오차의 **추정**
(ii) D̂ 의 **평균화로 정밀도 향상**. 이 논문이 개선하는 건 (ii) 뿐이다.

**(ii) 정밀도 관점 — 3개로는 한참 모자란다.**
digest 계산: `var(우리 파이프라인)/var(kinisi 1회) = 87`.
시드 K 개를 평균하면 분산이 1/K 이므로,

> **우리 파이프라인이 kinisi 궤적 1개와 같은 정밀도를 내려면 시드 ≈ 87개**
> (같은 200 ps · 같은 셀). 지금 3개면 **kinisi 1회의 1/29 수준**이다.
> 분해하면: **multi-origin 만 켜도 87 → 10** (시드 10개 상당), **거기에 kinisi 까지 쓰면 1**.

⚠ **한 자릿수 정밀도로만 읽어라.** 87 은 N=48 합성 브라운 걸음 값이고, 실제 아르지로다이트의
cage 상관에서는 multi-origin 원점들이 내 합성계보다 **덜 독립적**이라 8.7배 이득이 줄어들 수 있다.
**"수십 배"가 안전한 서술이고, "87배"는 이 합성 조건에서의 값임을 밝혀서만 쓴다.**

**(i) 추정 관점 — 3개는 원리적으로 부족하고, 그건 이 논문이 못 고친다.**
[Gra25UQ](`grasselli2025_uncertainty_era_ml_atomistic`) §2.4 식 (27) 이 **M ≥ 4** 를 요구한다.
그리고 시드 3개의 sd 는 상대오차 **1/√(2·2) = 50 %** 다. ⇒ **시드 산포는 "있다/없다" 신호이지
정량 오차막대가 아니다.** 우리 `Ea 0.197±0.032` 의 `±0.032` 는 **±50 % 의 불확실성을 가진 숫자**다.

> 🔵 **실무 권고 (우선순위대로)**
> **① multi-origin 을 정본으로 승격** — MD 0 스텝, 분산 ~9배 이득. 이미 코드가 있다
>   (`msd_multi_origin`, `msd_refit_window.py --mto`). 정본 교체는 재현성 결정이 필요하다.
> **② kinisi 를 병행 산출** — 시드당 D 사후분포. MD 0 스텝.
> **③ 시드는 3 → 5** 로. (i) 을 위해서다. 정밀도 때문이 아니다.

### 7.F ★★ **비(ratio) 의 불확실도** — 논문은 안 다룬다

**⛔ 이 논문은 비를 한 번도 다루지 않는다.** 본문 전체에서 "ratio" 는 `Fig. 3` 캡션의
"per-element ratios between covariance matrices" 한 번뿐이고, **두 D 의 비도, 그 오차 전파도 없다.**
가장 가까운 문장은 §VI 의 *"they allow for scientifically meaningful comparisons to be made
between estimated diffusion coefficients across different systems or under varying conditions"* —
**가능하게 만든다고만 하고 식을 안 준다.**

**그래서 우리가 붙여야 한다. 붙일 수 있고, 내가 검증했다.**

**(a) 전파식.** design 과 host 는 **서로 다른 궤적**이라 독립이다. 1차 전파:
> **(σ[D_rel]/D_rel)² = (σ[D\*_des]/D\*_des)² + (σ[D\*_host]/D\*_host)²**
> — **상대 표준편차가 제곱합(quadrature)으로 더해진다.**

**(b) 더 나은 방법 — 사후표본 나눗셈.** kinisi 는 D 를 **3200개 표본**으로 준다. 두 계의
표본을 각각 무작위 치환해 원소별로 나누면 **비의 사후분포**가 바로 나온다 (정규근사 불필요,
비대칭 꼬리까지 살아 있다).

**(c) digest 계산으로 검증했다** — 참 비 = 1.60 인 두 계 · 독립 궤적쌍 12회:

| 항목 | 값 |
|---|---|
| 평균 r̂ | **1.6091** (편향 **+0.57 %**) |
| 진짜 산포 sd(r̂) | **0.0449 (2.79 % 상대)** |
| 표본나눗셈 사후 sd | **0.0580 (3.6 % 상대)** → 보고/진짜 = **1.29 (보수적)** |
| 제곱합 검산 | host 1.88 % ⊕ design 2.28 % = **2.96 %** vs 관측 **2.79 %** ✅ |

⇒ **전파식 (a) 가 맞고, 표본나눗셈 (b) 는 그것을 재현하면서 개별 kinisi 와 같은 정도로
보수적이다.** (12쌍 → sd 추정 상대오차 21 %, 1.29 는 ±0.27 로 읽어라.)

**(d) 🔴 그러나 이 σ 는 `D_rel` 불확실도의 전부가 아니다.**

| 성분 | 이 방법이 재나 |
|---|---|
| **④ 표집/통계** (궤적이 짧아서) | ✅ **정확히 이것만 잰다** |
| **① 모델오차** (UMA 가 틀려서) | ❌ **전혀 안 잰다** |
| **cell-conditioned 무질서 배열** | ❌ 안 잰다 (배열 앙상블은 우리 별도 축) |

[Gra25UQ] §2.8(c) 가 지적하듯 **ML 오차는 가까운 배치에서 강하게 상관**되므로 design/host 의
모델오차는 비에서 **부분 상쇄**된다 — 그래서 `D_rel` 설계 자체는 옳다. 하지만 상쇄량은
아무도 안 잰다. ⇒ **"D_rel 의 불확실도 = kinisi σ" 로 쓰면 안 된다. "D_rel 의 통계
불확실도"라고 축을 명시해야 한다.**

**(e) 우리가 추가로 붙여야 할 것 (목록)**
1. **비의 사후분포에서 `P(D_rel > 1)`** 을 직접 보고 — 비준 판정이 "1보다 큰가"이므로
   이게 자연스러운 보고량이다 (점추정+σ 보다 정직하다).
2. **cell-conditioned 정의를 유지** — 같은 무질서 배열 안에서만 비를 만든다.
3. **모델오차 축은 따로 표기** — `force_contrast` 는 이 σ 와 **합치면 안 된다**(다른 축이고
   상관 구조를 모른다).
4. **Arrhenius 로 갈 때는 `kinisi.arrhenius.StandardArrhenius`** 에 D **분포**를 넘겨
   Ea 분포를 받는다. 3점 선형회귀보다 정직하다.
5. ⚠ **σ(Nernst–Einstein) 로 넘어가는 순간 이 오차막대는 무의미해진다** — Haven=1 가정의
   계통오차가 통계오차보다 크다. **σ 절대값 비인용 규율은 그대로 유효하다.**

### 7.G ★ 당장 이식 가능한가 — **단계**

**✅ 가능하다. MD 를 한 스텝도 더 안 돌린다.** 기존 궤적 파일만 있으면 된다.

```
0) 격리 환경  python3 -m venv ~/kinisi_env && ~/kinisi_env/bin/pip install "numpy<2" kinisi==1.1.0 ase
   ⛔ uma env 에 넣지 마라 — numpy<2 가 UMA/fairchem 을 깰 수 있다.
   (또는 kinisi 임포트 직전 `np.product = np.prod` 심기 — 둘 다 통과 확인)

1) 궤적 로드   frames = ase.io.read("<prod>.xyz", index=":")        # 우리 생산 궤적 그대로
2) 파서 파라미터  {'specie':'Li', 'time_step':0.002, 'step_skip':50}
   ★ 우리 dt = 2 fs = 0.002 ps, 덤프 save_fs = 100 fs → step_skip = 50.
     (`time_step*step_skip` = 0.1 ps 가 프레임 간격이 되게 맞춘다)
   ★ `sampling` 은 **건드리지 마라** — 기본 multi-origin 이 정답이고
     single-origin 은 §6.4② 때문에 조용히 틀린다.
   ★ `max_dt=50.0` 을 주면 우리 창과 정렬된다 (§7-D(2): 정밀도 손실 없음)
   ★ 골격 드리프트는 `framework_indices` 로 — 우리 `com_exclude="Li"` 와 같은 목적

3) 시드 3개 합치기   DiffusionAnalyzer.from_ase([f1,f2,f3], parser_params=P, dtype='identical')
   → N′ᵢ 를 시드별로 더한다. ⚠ 이건 "시드 산포"와 **다른 것**이다.
     시드 산포도 계속 봐야 하므로 **양쪽 다** 낸다: 시드별 개별 적합 + identical 합산.

4) 적합        d.diffusion(start_dt)  ; start_dt ∈ {2, 5, 10} ps 스캔 (§7-D(1))
5) 회수        d.D.samples   # 3200 표본. 평균·sd·분위수 전부 여기서
6) 비          r = D_des.samples[perm1] / D_host.samples[perm2]   # §7-F(b)
               보고: median(r), 68 % 구간, P(r>1)
7) Arrhenius   kinisi.arrhenius.StandardArrhenius(T=[600,800,1000], diffusion=[분포들])
               → .activation_energy (분포)  ·  .extrapolate(300)

8) 대조 잡     같은 궤적으로 우리 OLS 2–50 ps 도 계속 낸다.
               두 값이 **중심에서 어긋나면** 그건 창/확산영역 문제이지 추정기 문제가 아니다
               (§7-B(i): 추정기는 D 를 편향시키지 않는다).
```

**막는 것**: (a) numpy≥2 (해결됨, 위) (b) `sampling='single-origin'` 버그 — **쓰지 마라**
(c) `memory_limit` 기본 8 GB — 2000 프레임 × 100 원자는 여유, 큰 셀은 올려라
(d) ⛔ **정본값 교체 결정** — 이건 코드 문제가 아니라 **거버넌스**다. 기존 발표된
`D_Li_cm2_s` 를 바꾸면 재현성이 끊긴다 → **병행 산출 후 `db/governance/decisions.json` 에
보고량 카드로 올려 사람이 ratify** 하는 순서를 지켜야 한다.

**코드 규율 준수**: 새 파일 만들지 말고 **`tools/ionic/msd_diffusive_check.py` 에 `--kinisi`
플래그를 붙이는 게 맞다** (이미 `lin_fit` 2–50 ps 자유절편 규약과 β 게이트가 거기 있다).
`tools/ionic/msd_refit_window.py --mto` 도 이미 multi-origin 을 다룬다.

---

## 8. 적용 인사이트

1. **가장 싼 개선은 추정기 교체가 아니라 시간원점 평균이다** — 이득은 둘이 비슷한데
   (분산 8.7× vs 10.0×, digest 계산) **시간원점 쪽은 새 의존성도 새 환경도 필요 없다**
   (`msd_multi_origin` 이 이미 우리 코드에 있다). 우리 정본 MSD 가 single-origin 인 것은
   **의도적 재현성 선택**이었지 물리적 판단이 아니었다
   (`disorder_ensemble_diffusion.py` docstring 자인).
2. **우리 오차막대(시드 산포)는 원리적으로 옳다.** 이 논문이 "정직하지만 비싸다"고 부른
   그 방법이다. 흠집은 **정밀도**이지 **정직성**이 아니다. ⇒ 발표에서 방어 가능하다.
3. **`Fig. 6`b: OLS 는 오래 돌려도 안 좋아진다.** "200 ps 로 늘렸으니 통계가 좋아졌다" 는
   OLS 에선 성립하지 않는다. 우리가 200 ps 에서 얻은 이득은 **창이 50 ps 로 고정돼 있어서**
   부분적으로만 실현된다.
4. **비의 오차는 제곱합이고, 우리가 직접 붙여야 한다** — 논문은 안 준다.
   `P(D_rel > 1)` 이 우리 비준 판정에 가장 맞는 보고량이다.
5. **[Kahle20] 의 블록 오차보다 이 논문의 재스케일이 낫다** (SI S-II: 블록법은 **과소** 방향).
   우리가 [Kahle20] 에서 이식 후보로 적어둔 "블록 수(4/8/16) 감도 점검"은
   **이 논문 기준으로는 애초에 열등한 추정기의 감도를 재는 일**이다. 우선순위를 내려도 된다.

## 9. 인용 가능 문장

- "Ordinary least-squares regression of MSD data is statistically inefficient and its textbook
  standard error significantly underestimates the true uncertainty in D̂\*, because MSD data are
  serially correlated and heteroscedastic [McCluskey 2025, JCTC 21, 79]."
- "Modelling the MSD covariance with the analytical long-time-limit form for freely diffusing
  particles, parametrised by rescaling the observed variance by the number of non-overlapping
  sub-trajectories, allows near-Cramér–Rao-bound estimation of D\* from a single trajectory
  [McCluskey 2025]."
- "The number of statistically independent observations of the MSD at lag i is
  N′ᵢ = N_atoms × N_t/i — the number of *non-overlapping* time windows, not the total number of
  observed squared displacements [McCluskey 2025, SI S-II]."
- ⚠ 우리 문맥 문장은 **반드시 축을 명시**: "우리 `D_rel` 오차막대는 **통계(표집) 불확실도**이고,
  MLIP 모델오차는 포함하지 않는다."

## 10. 주의 / 한계 (over-claim 방지) — **비판적으로**

**논문 자신이 인정하는 것**
1. **Σ′ 은 근사다.** 긴 t 가정에서 유도돼 **짧은 t 에서 분산을 과대평가**한다(`Fig. 3` 자홍 가장자리).
   그 결과 p(D̂\*) 가 이론최적보다 **≈17 % 넓다**(`Fig. 4`c) 고 **σ̂² 가 ~1.45–2배 과대**하다
   (`Fig. 4`d, `Fig. 5`b). 참 Σ_num 을 쓰면 사라진다(`Fig. S5`).
2. **σ̂² 는 짧은 궤적에서 특히 부정확**하다고 §VI 이 명시.
3. 재조건화의 `cond_max` 는 **사용자 지정 손잡이**다. 값에 따라 답이 움직일 여지가 있는데
   **민감도 분석이 없다** (1×10¹⁶ 을 왜 그 값으로 두는지 논증 없음).

**내가 다는 비판**
4. 🔴 **검증계가 두 개뿐이고 둘 다 "쉬운" 계다.** 격자 random walk 는 **Σ′ 의 가정 그 자체**라
   순환에 가깝다. LLZO 는 **700 K 초이온 전도체**로 확산이 빠르고 cage 가 얕다.
   **느리고 caged 한 계**(우리 LPSOCl 600 K, 절편이 MSD@50 의 18 %)에서 Σ′ 이 성립하는지는
   **이 논문이 답하지 않는다.** ⇒ 우리가 이식할 때 **첫 계산은 대조 잡**이어야 한다.
5. 🔴 **확산영역 시작 `start_dt` 선택 규율이 없다.** *"set by the user to a value appropriate
   for their system"* 으로 끝난다. 그런데 `Fig. 3` 이 보여주듯 **짧은 lag 이 Σ′ 이 가장 틀리는
   구역**이라 `start_dt` 가 결과를 크게 흔들 수 있다. **감도 분석이 없다.**
   ([Kahle20] 은 이걸 `Fig. S3` 에서 t′ 스캔으로 실제로 했다 — **그 점에서는 Kahle 이 낫다.**)
6. 🔴 **적합 상한을 안 다룬다.** 궤적 끝까지 쓴다. 창 상한의 효과는 내 digest 계산이
   메워야 했다(§7-D(2)).
7. 🔴 **비(ratio)·차이 같은 하류 보고량 전파가 없다** — §VI 이 "가능하다"고만 하고 만다.
   우리처럼 **비가 보고량인 캠페인**에는 그대로 못 쓴다.
8. ⚠ **σ(이온전도도) 로 안 간다.** D\* 만 다룬다. Haven 비·전하 상관은 논의 밖.
   `kinisi` 패키지에는 `conductivity_analyzer.py` 가 있지만 **논문이 검증하지 않았다.**
9. ⚠ **MLIP 모델오차와 무관하다.** [Gra25UQ] 분류의 **④ 표집/통계**만 다룬다.
   ⛔ *"kinisi 를 썼으니 우리 D 가 믿을 만하다"* 는 오용이다 — 궤적이 옳다는 전제 위의 통계다.
10. ⚠ **`Fig. 6` 의 WLS/GLS 는 512회 반복에서 얻은 수치 분산/공분산을 쓴다** —
    즉 **실무에서 못 쓰는 이상적 참조선**이다. 실무 비교는 OLS vs kinisi(초록)만이 정당하다.

**용어 함정 (우리가 틀리기 쉬운 것)**
11. ⛔ **"부트스트랩"이라고 부르지 마라.** 논문에 그 단어가 없다. 클래스 이름이 `MSDBootstrap`
    일 뿐 기본값은 리샘플링 없음이다. 올바른 이름: **근사 베이지안 회귀(≈GLS)**.
12. ⛔ **"AIMD"·"DFT"라고 부르지 마라.** LLZO 는 **고전 MD**(METALWALLS + DIPPIM 분극이온 힘장)다.
13. ⚠ **`Fig. 6`b 의 t_max 는 총 시뮬 길이**이지 적합 창 상한이 아니다.

## 11. ⛔ 이 논문이 못 하는 것 / 내가 확인 못 한 것

**이 논문이 못 하는 것**
- 비(ratio)·차이의 오차 전파 — **없다**
- σ(이온전도도), Haven 비, 전하 상관 — **없다**
- `start_dt`(확산영역 시작) 선택 규율·감도 — **없다**
- 적합 창 상한의 효과 — **없다**
- MLIP/힘장 모델오차 — **범위 밖**
- 무질서 배열 앙상블 — **범위 밖**
- caged/느린 계에서의 Σ′ 타당성 — **검증 안 함**
- `cond_max` 민감도 — **없다**

**내가 확인 못 한 것 (정직하게)**
- **LLZO 원궤적을 안 받았다** (Zenodo 10.5281/zenodo.10532134). 논문의 LLZO 숫자를
  **독립 재현하지 않았다** — `Fig. 5`·`Fig. S6` 값은 전부 **내 그림 판독**이다.
- **`showyourwork build` 를 안 돌렸다** (데이터·conda 환경 필요). 저장소가 논문 그림을
  **바이트 단위로 재생성하는지 확인 못 했다.**
- **`kinisi/tests/` 를 안 돌렸다.**
- **`model=True`(2차식 분산 피팅) 경로를 안 시험했다.** 논문 그림은 `model=False` 다.
- **`block=True`(pyblock) 경로를 안 돌렸다.** SI S-II 비교는 **논문 서술 + `Fig. S3` 판독**이다.
- **`kinisi.arrhenius` 를 안 돌렸다.** 코드는 읽었지만 실행 검증은 안 했다.
- **우리 실제 궤적으로 안 돌렸다.** §7 의 digest 계산은 **전부 합성 브라운 걸음**이고,
  그것은 kinisi 의 가정 그 자체다. ⇒ **실제 LPSCl 궤적에서의 배수는 다를 수 있다.**
  특히 **8.7× (multi-origin 이득)** 은 cage 상관이 있으면 줄어든다.
- **그림 12장 중 4장(`Fig. S1` · `Fig. S2` · `Fig. S4` · `Fig. S5`)을 안 봤다.**
- **arXiv 2305.18244 판본과 출판본의 차이를 대조 안 했다.**
- **SI 를 두 개 받았는데 같은 문서다** — 텍스트를 뽑아 비교한 결과 `Sup` 과 `Sup2` 는
  **ACS 다운로드 워터마크 줄 하나만 다르고 내용이 동일**하다(둘 다 8쪽, 같은 S-I~S-IV).
  ⇒ **SI 는 실질 1개다.** 크로핑은 `Sup` 쪽 하나만 썼다.

---

## 12. 용어 미니 사전 (우리 팀용)

| 용어 | 뜻 | 왜 중요한가 |
|---|---|---|
| **statistical efficiency (통계적 효율)** | 같은 데이터로 추정량의 분산이 얼마나 작은가 | "효율적"= 정확한 게 아니라 **덜 흔들린다**. OLS 는 불편이지만 비효율 |
| **Cramér–Rao bound** | 불편추정량 분산의 이론적 하한 | GLS 가 이걸 달성한다 = **더 잘할 수 없다** |
| **heteroscedastic (이분산)** | 점마다 분산이 다름 | MSD 는 σ²∝t² 로 커진다 → OLS 의 등분산 가정 붕괴 |
| **serially correlated (계열상관)** | 이웃 점끼리 상관 | x(t)·x(t+Δ)가 같은 변위 이력 공유 → OLS 의 독립 가정 붕괴 |
| **OLS / WLS / GLS** | 가중 없음 / 1-D 분산 가중 / **전체 공분산 행렬** 가중 | 사다리. GLS 만 상관을 본다 |
| **covariance matrix Σ** | Σ[xᵢ,xⱼ] = 두 lag MSD 의 공분산 | GLS 의 연료. **모르는 게 문제**였고 이 논문이 해석적으로 채운다 |
| **N′ᵢ (독립 관측 수)** | **겹치지 않는** 시간창 수 × 입자 수 = N_atoms·N_t/i | 총 관측 수로 나누면 **독립성 과대계상** |
| **multi-origin MSD** | 모든 시간원점에서 평균 | 공짜 통계. 우리 정본은 **안 쓰고 있다** |
| **improper prior** | 정규화 안 되는 사전분포(여기선 D\*≥0) | 사실상 "제약만 있는 비정보 사전" |
| **MAP** | 사후 최대점 | MCMC 시작점으로 씀 |
| **emcee / affine-invariant ensemble sampler** | 여러 walker 가 서로를 참고해 이동하는 MCMC | 32 walkers × 1500, burn 500, thin 10 → 3200 표본 |
| **minimum eigenvalue method** | 작은 고유값을 바닥값으로 올려 조건수를 고정 | Σ′ 이 특이해지는 걸 막는 수치 처방 |
| **condition number (조건수)** | 최대/최소 고유값 비 | 크면 역행렬이 잡음을 증폭 |
| **Flyvbjerg–Petersen blocking** | 인접 2개씩 평균을 반복해 상관을 지우고 평탄역을 읽음 | 대안. **하한만 주므로 과소** → 이 논문이 기각 |
| **posterior predictive / marginal posterior** | c 를 적분해 없앤 p(D\*\|x) | 우리가 최종적으로 쓰는 것 |
| **showyourwork** | 논문 그림·본문을 Snakemake 로 완전 재현하는 프레임워크 | 이 ESI 의 뼈대 |

---

## 13. 교차 참조 (litdb 내부)

| 문서 | 관계 |
|---|---|
| `papers/kahle2020_ht_aimd_screening.md` | **MD 통계 규율의 선행 원전.** 창 검증(t′ 스캔)·Bayesian Ea 는 **Kahle 이 낫고**, 오차 추정기(블록 vs 재스케일)는 **McCluskey 가 낫다**. 두 편이 상보 |
| `papers/grasselli2025_uncertainty_era_ml_atomistic.md` | **축 분류의 정본.** McCluskey 는 그 분류의 **④ 표집/통계**만 다룬다. Grasselli 가 *"수송계수 전파는 rigorous theory 부재, 멀티궤적 brute-force 뿐"* 이라고 한 자리에 **McCluskey 가 단일궤적 해법을 놓는다** — 단 그것도 **④ 안에서만**이다. 🔴 두 digest 를 같이 읽어야 오해가 안 생긴다 |
| `our_dft_baseline.md` | 우리 D·Ea 정본값. **이 논문 수치와 같은 표에 놓지 않는다** |

# Uncertainty estimation by committee models for molecular dynamics and thermodynamic averages — Imbalzano et al. (preprint, 2020-11-10; 저널 표기 PDF 에 없음)

> slug `imbalzano2021_committee_uq_md_thermodynamic_averages` · DOI `n/a (PDF 에 없음)` · type `MLIP · methods (UQ 이론 + 시연)` · PDF `36dc36f5-78._Uncertainty_estimation_by_committee_models…pdf` · digested `2026-09-09` · status ✅
> **저자**: Giulio Imbalzano¹, Yongbin Zhuang², Venkat Kapil^{1,3}, Kevin Rossi^{1,4}, Edgar A. Engel¹, Federico Grasselli^{1,*}, Michele Ceriotti^{1,*} — ¹ COSMO/Laboratory of Computational Science and Modeling, IMX, **EPFL** Lausanne · ² Xiamen Univ. · ³ Univ. of Cambridge · ⁴ LNE/ISIC EPFL Sion. 교신 `federico.grasselli@epfl.ch` · `michele.ceriotti@epfl.ch`

> elements: H, C, N, O, S, Ga
> methods: MD, MLIP, DFT, DOS

> ⚠ **서지 주의 — 이 PDF 는 저널·DOI·arXiv 도장이 하나도 없다.** pdfTeX-1.40.20 로 2020-11-10 생성된
> **preprint 판**이다(16 pp). 본문·참고문헌 어디에도 자기 게재정보가 없다. 슬러그의 `2021` 은
> 사용자가 지정한 것이고 **PDF 가 확인해 주지 않는다.** 인용할 때는 표지를 따로 대조하라.
> 확인 가능한 것: 저자 7인·소속·교신 2인·본문 §I–VI + Appendix A·Fig 1–9·Table 0개·refs 82개.

---

## 0. 이 digest 를 읽는 법 — 우리는 이 논문을 **왜** 읽나

우리 blocker 는 한 문장이다: **MLIP-MD 로 뽑은 D(확산계수)에 오차막대를 어떻게 붙이나.**
UQ 논문 대부분은 **힘·에너지의 단일점 오차**에서 멈춘다. 이 논문은 거기서 한 걸음 더 가서
**그 오차를 궤적 위의 평균값까지 전파**한다. 우리 D 는 MSD 기울기 = 궤적 위의 양이라 겉보기 구조가 같다.

**그런데 결론부터 — 겉보기만 같다.** 이 논문이 전파하는 것은
**배위평균(configurational average)** `⟨a⟩ = (1/Z)∫a(q)e^{−βV(q)}dq` 뿐이다.
논문 전문에서 `diffusion` · `transport` · `MSD` · `mean square` · `Green–Kubo` ·
`time-correlation` · `conductivity` · `viscosity` 는 **각각 0회 등장한다**(전문 grep, 2026-09-09).
"correlation function" 6회는 전부 **radial/pair** correlation — 정적이다.
제목의 *molecular dynamics* 는 **샘플러**를 가리키지 관측량을 가리키지 않는다.

⇒ 축 판정을 먼저 박고 들어간다:

| 축 | 이 논문이 덮나 |
|---|---|
| **모델 불확실도** — 훈련 참조구조가 유한해서 생기는 보간오차 | ✅ **이게 논문 전부** |
| 모델 불확실도 — 참조방법(범함수) 자체의 오차 | ⛔ 명시적 범위 밖 |
| **관측량이 정적 배위평균**일 때의 전파 | ✅ 완전한 식 + 4계 시연 |
| **관측량이 동역학량**(D, 상관함수, 수송계수)일 때의 전파 | ⛔ **전무. 언급조차 없다** |
| **시드/궤적 통계 불확실도** | ⛔ 형식화 안 됨. "comparable" · "larger than" 같은 정성 언급 3회뿐 |
| 유한크기 | ⛔ 범위 밖 (융점 절에서 직접 인정) |

⇒ 우리 2축 blocker 중 **모델축의 절반(정적 부분)만** 덮고, **시드축 0 · 동역학축 0**.
이 판정이 이 digest 의 뼈대다.

## 1. 한 줄 요약

**보정(calibrate)된 committee** 의 예측 산포를 (i) 단일점 오차, (ii) **MD 궤적을 하나만 돌리고
on-the-fly 재가중으로 얻는 열역학 평균의 오차** 로 쓰는 법을 세운 방법론 논문.
핵심 산출물은 `σ̃² ≈ σ_a² + σ_V²` — **관측량 모델의 오차(σ_a)** 와
**퍼텐셜이 달라져 위상공간 표본이 뒤틀리는 오차(σ_V)** 를 **따로 세서 제곱합**한다.
`σ_V` 는 **선형화(cumulant expansion, CEA)** 로 얻고, 그 형태가
`σ_V ≈ β·std_i[Cov_V̄(a, V^(i)−V̄)]` — **관측량과 모델간 에너지차의 공분산**이다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 연구유형 | 방법론(통계) + MLIP-MD 시연 4계 |
| 계 | ① Phe-Gly-Phe 삼펩타이드(기체상) ② 액체 물 64분자 ③ 메탄술폰산 1 + 페놀 20 ④ 액체 갈륨 384원자 |
| MLIP | Behler–Parrinello NNP (n2p2) 전부 · Ga DOS 관측량모델만 SOAP 스파스 커널 |
| MD 엔진 | **i-PI** + **LAMMPS**(n2p2 플러그인) |
| 참조 전자구조 | 계마다 다름 — GAMESS-US PBE/dDsC/def2-TZVP · CP2K revPBE0-D3 · Quantum ESPRESSO PBE |
| 전신 논문 | committee 교정 = **Musil 2019** (ref 36, JCTC 15, 906) · CEA = **Ceriotti 2012** (ref 50, Proc. R. Soc. A 468, 2) · 재가중 원전 = Torrie–Valleau 1977 umbrella (ref 47) |
| 우리와의 접점 | Ceriotti 그룹 = **PET-MAD 저자군**(`papers/petmad2026_lightweight_universal_interatomic_potential_mad.md`). PET-MAD 의 LLPR 불확실도는 이 계보의 후속이다 |

## 3. 핵심 수치 (전부 소환값 — 우리 db 와 섞지 않는다)

| 양 | 값 | 계 / 조건 |
|---|---|---|
| 교정계수 α (**편향보정**, Eq. 6) | **2.1** | 물, M = 4 |
| 교정계수 α (**편향 있음**, Eq. 5) | **3.75** | 같은 committee |
| 교정계수 α (편향보정) | **4.08** | 메탄술폰산/페놀, M = 5 (원논문 ref 7 은 **5.8** 로 보고했었다) |
| 교정계수 α | **1.0** | Phe-Gly-Phe 삼펩타이드, M = 4 |
| 베이스라인 불확실도 σ_b | **7 × 10⁻³ meV/atom** | DFTB3/3OB+D3BJ vs PBE, Eq. 13 (⚠ §10-c 참조) |
| 융점 T_m | **290 ± 5 K** | 물/Ih, interface pinning, M = 4 |
| 융해엔트로피 Δs_m | **0.16 ± 0.01 meV/K/molecule** | 같은 계 |
| 융해잠열 Δh_m | **46 ± 3 meV/molecule** | 같은 계 |
| 탈양성자화 자유에너지 | **20 (+5 / −2) kJ/mol** | CH₃SO₂OH in 페놀, metadynamics + ITRE, **비대칭 구간** |
| committee 크기 M | 4 (삼펩타이드·물·Ga 퍼텐셜) · 5 (산/페놀) · **64** (Ga DOS 관측량모델 M′) · 16 (부록 α 분석용 M_max) | |
| 최소 M | **4** — `E[1/ς²] = (M−1)/(M−3)` 가 M = 3 에서 발산 | Eq. (A4) |
| 권고 M | **≥ 6** (비선형 조합으로 전파할 때) | 부록 마지막 문단 |

## 4. 이론 — 절별 완전 정리 ★★ (여기가 이 논문의 전부다)

### 4.1 §II A — committee 구성과 단일점 불확실도

**구성 (원칙)**: 전체 훈련셋 N 쌍 `(A, y_ref(A))` 을 **복원 없이(without replacement)**
크기 `N_s < N` 의 **M 개 부분집합**으로 나눠, M 모델을 **독립 학습**한다.
⇒ **부트스트랩(복원추출)이 아니라 sub-sampling** 이다. (bagging 이 아니라 subagging.)

```
ȳ(A)  = (1/M) Σ_i y^(i)(A)                                   … Eq. (1)  committee prediction
σ²(A) = 1/(M−1) Σ_i [ y^(i)(A) − ȳ(A) ]²                     … Eq. (2)  단일점 불확실도
```

**교정 (α)**: 부분표집 때문에 예측분포의 **폭**이 참값 분포와 안 맞는다 —
논문 표현으로 *"may be too broad or **(usually) too narrow**"*.
폭만 틀렸다고 가정하고 **하나의 전역 스칼라 α** 로 늘린다. 가정 3개를 명시한다:

1. 편차는 **폭에만** 영향 (중심은 맞다)
2. **α 는 A 에 무관** (구조마다 다르지 않다)
3. 서로 다른 구조의 참값은 **무상관** — `y_ref(A) ⊥ y_ref(A′)` for `A ≠ A′`

```
P(y_ref|{A},α) = Π_A (2πα²σ²(A))^{−1/2} exp[ −|y_ref(A)−ȳ(A)|² / (2α²σ²(A)) ]   … Eq. (3)
LL(α) = (1/N_val) Σ_{A∈val} log P(...)                                          … Eq. (4)
α² = (1/N_val) Σ_{A∈val} |y_ref(A)−ȳ(A)|² / σ²(A)                              … Eq. (5)  ← 편향 있음
α² = −1/M + [(M−3)/(M−1)] · (1/N_val) Σ_{A∈val} |y_ref−ȳ|²/σ²                  … Eq. (6)  ← 편향보정
```

**재척도 (Eq. 7)** — 여기가 우리한테 제일 실용적이다:
```
y^(i)(A) ← ȳ(A) + α[ y^(i)(A) − ȳ(A) ]
```
평균은 불변, 산포만 α배. 그리고 논문이 명시한다 —
*"The rescaled predictions can be used to compute **arbitrarily-complicated non-linear functions** of y,
and the mean and spread of the transformed predictions are indicative of the distribution of the target quantities."*
⇒ **비선형 유도량의 불확실도 = 멤버별로 변환한 뒤 그 산포를 재라.** (§12 에서 D_rel 에 쓴다.)

**검증셋 만드는 두 방법** (§III 서두):
- (a) 짧은 committee MD 에서 **탈상관된** N_val 구조를 뽑아 참조법으로 힘·에너지 재계산
- (b) 훈련 DB 안에서 **적어도 n 개의 부분집합에 안 들어간** 구조를 골라 검증셋으로 (Ref 36 방식,
  별도 참조계산 불필요 — 사실상 out-of-bag)

### 4.2 §II B — weighted baseline (외삽 폭주 방지)

```
V^(i)(A) = V_b(A) + V_δ^(i)(A)        … Eq. (8)   Δ-learning: NN 은 참조−베이스라인 차이만 배운다
V̄(A)    = V_b(A) + V̄_δ(A)            … Eq. (10)
σ²(A)   = 1/(M−1) Σ_i [V_δ^(i) − V̄_δ]²  … Eq. (11)

U(A) = [1/σ_b² + 1/σ²(A)]^{−1} [ V_b/σ_b² + V̄/σ²(A) ]
     = V_b(A) + [ σ_b² / (σ_b² + σ²(A)) ] · V̄_δ(A)                        … Eq. (12)
```
**가중치 `w(A) = σ_b²/(σ_b²+σ²(A))`** — ML 이 자신 있으면(σ 작으면) w→1 로 ML 보정을 다 쓰고,
외삽 영역에 들어가면(σ 큼) w→0 이라 **베이스라인으로 자동 후퇴**한다.
역분산 가중합이라 결합오차 최소화와 일치. **힘은 `σ²(A)` 의 A-의존성까지 미분해야 한다**(논문 주의).

```
σ_b² = 1/(N−1) [ Σ_A |V_b−V_ref|² − (1/N)(Σ_A V_b−V_ref)² ]                … Eq. (13)
```
⇒ **분산 형태** — 베이스라인과 참조가 큰 상수만큼 어긋나는 것을 일부러 무시한다.

**원자단위 판(Eq. 15)**: ML 에너지가 원자중심 합 `V̄_δ = Σ_k V̄_δ(A_k)` (Eq. 14) 이면
가중치를 **원자마다** 매길 수 있다 — 계 전체가 아니라 **반응하는 몇 원자만** 외삽일 때 유용.
베이스라인에 자연스러운 원자분해가 없어도 되지만, 그럴 땐 σ_b 를 **원자당 오차**로 재정의해야 한다.

### 4.3 §II C — 열역학 평균의 on-the-fly 불확실도 ★★★ (사용자 질문 2의 답)

**표기**: PM = potential model(퍼텐셜 committee, M개) · OM = observable model(관측량 committee, M′개).
둘은 **별개 committee** 다. 관측량이 학습된 것이 아니면(예: g(r), Q6) M′ = 1 이 된다.

**① 순진한 단일궤적 평균 (Eq. 16)** — 이게 보통 사람들이 하는 것
```
ā̄ ≡ ⟨ā⟩_V̄ = (1/M′) Σ_j ⟨a^(j)⟩_V̄
```
V̄ 하나로 궤적을 돌리고 OM 만 평균. **PM 불확실도가 안 들어간다.**

**② 무식한 정답 (Eq. 17)** — 궤적을 M개 돌린다
```
ã ≡ (1/(M M′)) Σ_i Σ_j ⟨a^(j)⟩_{V^(i)}
```
논문 평가: *"trivially parallelizable, this strategy is **inconvenient**"* — 같은 배열에 대해
멤버 여러 개를 한꺼번에 계산할 때 나오는 **상당한 계산 절약을 못 쓰기 때문.**

**③ 재가중으로 우회 (Eq. 18–22)** — 논문의 핵심 트릭
```
⟨a^(j)⟩_{V^(i)} = (1/Z^(i)) ∫ a^(j)(q) e^{−βV^(i)(q)} dq                   … Eq. (18)
w^(i)(q) ≡ exp{ −β[ V^(i)(q) − V̄(q) ] }                                    … Eq. (20)
⟨a^(j)⟩_{V^(i)} = ⟨w^(i) a^(j)⟩_V̄ / ⟨w^(i)⟩_V̄                              … Eq. (22)  ★ 원리적으로 정확
σ̃² = 1/(MM′−1) Σ_i Σ_j ( ⟨a^(j)⟩_{V^(i)} − ã )²                            … Eq. (23)
```
⇒ **에르고딕 가정 아래, V̄ 로 돌린 궤적 하나만 있으면 M 개 앙상블의 평균을 전부 복원한다.**
저장할 것: 궤적의 배열 + **멤버별 퍼텐셜에너지 `V^(i)`** (스칼라 M개/스냅샷). 매우 싸다.

부수효과 하나 — **on-the-fly learning 의 체계오차 치료**: 학습 도중 퍼텐셜이 바뀌면 궤적 구간마다
앙상블이 달라 정준평균에 체계오차가 생기는데, 멤버별 에너지를 저장해 뒀으면
**언제든 가장 최신 퍼텐셜 기준의 가중치를 다시 계산**해 궤적 전체를 일관되게 쓸 수 있다.

**④ 왜 ③을 그대로 못 쓰나 → CEA (Eq. 24)** ★ **여기가 "어떤 근사가 들어가나"의 답**
Eq. (22) 는 정확하지만 **통계효율이 나쁘다**: 오차가
`h^(i) ≡ −ln w^(i) = β(V^(i) − V̄)` 의 **분산에 지수적으로** 커지고, 그 분산은
**계 크기에 따라 필연적으로 증가**한다 (Ceriotti 2012 의 *"curse of system size"*).
그래서 **누율전개 근사(cumulant expansion approximation)** 로 **선형화**한다.

> **가정 (논문 문장 그대로)**: `a^(j)` 와 `h^(i)` 가 **상관된 가우시안 변량**이고,
> 평균은 각각 `⟨a^(j)⟩_V̄` 와 `0`, 공분산은 `⟨a^(j)h^(i)⟩_V̄` 이다 (모두 committee 위상공간 측도 기준).

```
⟨a^(j)⟩_{V^(i)} ≈ ⟨a^(j)⟩_V̄ − β ⟨ a^(j) (V^(i) − V̄) ⟩_V̄                    … Eq. (24)  ★★
```
**⇒ 재가중이 아니라 선형화다.** 지수 가중치를 1차 전개해서
"관측량 × 에너지편차" 의 **공분산 한 항**으로 바꾼 것.
논문은 CEA 를 **직접 추정자보다 권장**한다 — 안정성·통계효율 때문만이 아니라
*"the linearized form emphasizes the different sources of error"* 라는 형식적 이유도 든다.

**⑤ CEA 가 주는 두 가지 형식적 결과**

(a) **평균이 일관된다 (Eq. 25)**
```
ã ≈ ā̄ + β (1/M) Σ_i ⟨ā(V^(i)−V̄)⟩_V̄ = ā̄
```
둘째 항은 `Σ_i (V^(i) − V̄) = 0` 이라 정확히 소멸. ⇒ CEA 를 쓰면 **다중궤적 평균 = 단일궤적 평균**.
(Eq. 17 의 무식한 방법은 일반적으로 Eq. 16 과 **다른 값**을 준다.)

(b) **분산이 두 항으로 깔끔히 쪼개진다 (Eq. 26–28)** ★★★ **← 이 논문의 대표식**
```
σ̃² ≈ [M(M′−1)/(MM′−1)] σ_a²  +  [M′(M−1)/(MM′−1)] σ_V²
    ──(M,M′→∞)──▶  σ_a² + σ_V²                                              … Eq. (26)

σ_a² ≡ 1/(M′−1) Σ_j ( ⟨a^(j)⟩_V̄ − ā̄ )²                                     … Eq. (27)
        = **관측량 모델(OM) 오차** — 샘플링은 고정하고 property model 만 흔든 것

σ_V² ≡ (1/M′) Σ_j σ_V^{2(j)},
σ_V^{2(j)} ≡ 1/(M−1) Σ_i ( ⟨a^(j)⟩_{V^(i)} − mean_i )²
           ≈ **β²/(M−1) Σ_i [ ⟨ a^(j)(V^(i)−V̄) ⟩_V̄ ]²**                     … Eq. (28)
        = **퍼텐셜 모델(PM) 오차** — 서로 다른 PM 이 위상공간을 다르게 표본하는 것
```

> ★ **σ_V 의 물리적 읽기 (우리한테 제일 중요한 한 줄)**
> `σ_V ≈ β × std_i[ Cov_V̄( a , V^(i) − V̄ ) ]`
> — **관측량이 "모델간 에너지 불일치" 와 상관이 없으면 σ_V = 0 이다.**
> 모델이 아무리 서로 달라도, 그 차이가 내 관측량이 사는 좌표와 직교하면 관측량은 안 흔들린다.
> 그리고 **β = 1/k_BT 가 앞에 있다 — 고온일수록 같은 공분산에 대해 σ_V 가 작다.**
> (우리는 600 K 에서 잰다 ⇒ 300 K 대비 β 가 절반.)

### 4.4 §Appendix A — α 의 편향과 M 의존성 ★ (사용자 질문 1의 정량적 답)

M 이 유한하면 Eq. (5) 는 **편향 추정자**다. 유도:
- 검증 참값 `y_n` 이 committee 분포 대비 `α_tr` 배 넓은 정규분포에서 나온다고 두고,
  `y_n ⊥ y^(i)`, 평균 일치(0) 를 가정.
- `1/s_M² ≡ E[σ²]·E[1/σ²]` (Eq. A2), `b_M² = E[ȳ²/σ²] = E[ȳ²]E[1/σ²] = 1/(M s_M²)` (Eq. A3).
  둘째 등식은 **표본평균과 표본분산의 독립성 = Basu 정리** (ref 82).
- M-표본분산이 `(M−1)ς² ~ χ²_{M−1}` 이므로
```
E[1/ς²] = (M−1)/(M−3)                                                       … Eq. (A4)
α_M² = α_tr²/s_M² + b_M²      (⚠ 우리 텍스트추출이 분수를 평평하게 폈다 — 아래 자체검산 참조)
α²   = [(M−3)/(M−1)] α_M² − 1/M                                             … Eq. (A5) = Eq. (6)
```

**논문이 뽑아낸 결론 3개**
1. **M ≥ 4 가 하드 하한** — `(M−1)/(M−3)` 이 M = 3 에서 발산한다. *"at least four models are needed."*
2. **M = 4 의 편향 추정자는 α 를 약 2배 부풀린다** (`√(3/1)` = 1.73).
3. **편향보정 추정자는 M = 4 에서 이미 점근값의 10 % 이내.**
4. 그러나 **비선형 조합으로 전파할 땐 유사 편향이 재발할 수 있으니 M ≥ 6 을 권한다.**
   그리고 **Eq. (A5) 의 무편향성은 가우시안 가정이 성립할 때만** — *"usually only approximately true."*

**편향 배율표** (내가 `√[(M−1)/(M−3)]` 로 계산 — 논문 표 아님)

| M | 4 | 5 | 6 | 8 | 10 | 16 | 64 |
|---|---|---|---|---|---|---|---|
| α_M / α (곱셈 성분) | **1.73** | 1.41 | **1.29** | 1.18 | 1.13 | 1.07 | 1.02 |

**자체검산 (내가 한 것 — 그림과 식이 맞는지)**: `Fig. 9` figure-read 로 M = 16 무편향 α ≈ 2.77 을 참값으로 넣고
M = 4 를 예측하면 `α_M² = 3(2.77²) + 3/4 = 23.8 → α_M = 4.88` (그림 초록 평균 figure-read ≈ 4.6),
역으로 `α² = (1/3)(4.6²) − 1/4 = 6.8 → α = 2.61` (그림 파랑 평균 figure-read ≈ 2.62). **일치.**
⇒ OCR 이 평평하게 편 Eq. (A1) 은 `α_M² = α_tr²/s_M² + b_M²` 가 맞고, 내 눈금 판독도 자기일관적이다.

## 5. 계산 방법 ★ (계별 전체 사양)

| | ① Phe-Gly-Phe | ② 물 | ③ CH₃SO₂OH/페놀 | ④ 액체 Ga |
|---|---|---|---|---|
| **MLIP** | Behler–Parrinello NN **M = 4** | NNP (n2p2) **M = 4** | NN **M = 5** | NNP **M = 4** (PM) + SOAP 스파스커널 **M′ = 64** (OM, DOS) |
| **committee 만드는 법** | **NN 가중치 초기화 + 내부 CV 분할(90 % 학습 / 10 % 시험)만 다름** ⚠ | ref 70 참조 (본문 미기술). 부록용으로 **M_max = 16** 학습 | ref 7 과 동일 | DOS OM: 394 Ga 구조 중 **300 개 무작위 추출** ×64 |
| **참조 전자구조** | **GAMESS-US**, PBE + **dDsC** 분산, **def2-TZVP** | **CP2K**, **revPBE0-D3** | ref 7 | **Quantum ESPRESSO**, PBE, MP k-격자 밀도 ≥ **6.5 k-points·Å** |
| **베이스라인** | **DFTB+**, DFTB3/3OB + **D3BJ** | 없음 (V_b = 0) | 없음 | 없음 |
| **기술자** | (n2p2 대칭함수) | 대칭함수 — H **27개** / O **30개**, cutoff **12.0 a.u.**, ref 69 셋 | ref 7 | SOAP: n = 12, l = 9, g_s = 0.5, **r_c = 6 Å**, c = 1, m = 5, r₀ = 6.0 |
| **NN 구조** | — | 원자당 은닉층 **2층 × 20노드** | — | — |
| **MD** | **REMD 120 ps**, **12 replica 300–2440 K**, Langevin, **dt 0.5 fs** | **NVT 300 K, 2 ns**, 64 H₂O, 큐빅 **23.86 Å** | 363 K, **독립 16런 총 ≈1.6 ns** | **NVT 1800 K, 400 ps, dt 4 fs**, 384원자, **GLE + stochastic velocity rescaling** |
| **엔진** | i-PI | i-PI + LAMMPS/n2p2 | i-PI | i-PI |
| **훈련 데이터** | 26종 아미노산 **1.5 ns REMD**(16 replica, 300–1000 K 로그간격)에서 **farthest-point sampling** + **BioFragment DB 기하최적화 이합체 3,380개** | **1,593** 개 64분자 벌크 물 구조 | ref 7 | 394 구조 (고체+액체) |
| **α** | **1.0** | **2.1** (편향판 3.75) | **4.08** (편향판 5.8) | 본문 미기재 |
| **부가** | σ_b = 7 × 10⁻³ meV/atom | — | metadynamics + **ITRE** 언바이어싱 | 융점계는 **interface pinning**, PLUMED, local **Q6**, a = 165, κ 스프링, **336 H₂O**, 직방정 **15.93 × 13.79 × 52.47 Å³** |

> ⚠⚠ **①의 committee 구성이 §II A 의 정의와 다르다.** §II A 는 *"부분집합으로 나눠 독립 학습"* 인데
> 삼펩타이드는 *"**가중치 초기화와 내부 CV 분할만** 다르다"* — 데이터 분할이 **90/10 이라 거의 전량 공유**한다.
> 이건 **부분표집 committee 가 아니라 시드 앙상블**에 가깝다. 논문은 이 불일치를 언급하지 않는다.
> (§10-a 에서 비판으로 다시 다룬다.)
>
> ⇒ 사용자 질문 1 정리: **부트스트랩 아님.** 원칙은 **복원 없는 부분표집**, 실제로는 계마다 달라서
> **부분표집(Ga DOS: 300/394)·초기화 시드 + CV 분할(삼펩타이드)** 이 섞여 있다.

## 6. 결과 — 절별 상세

### 6.1 §III 서두 + `Fig. 2` — 워크플로

`Fig. 2` 를 실제로 보고 옮긴 순서 (도식 상단 좌→우, 하단 우→좌):
**Database construction → Reference Force-Energy calculations (HΨ=EΨ) → Training database subsampling
→ ML Potential Training → Calibrated Committee Model (박스 안에 Eq. 7 재척도식)
→ MD committee Integration (박스에 오일러–라그랑주식)** 에서 갈라져
- 오른쪽: **Reweighting via CEA** (박스에 `⟨a^(j)⟩_{V^(i)}` 와 `⟨w^(i)a^(j)⟩_V̄/⟨w^(i)⟩_V̄`) → **Uncertainty for thermodynamic observable(s)** (박스에 빨간 밴드 g(r) 축소판)
- 왼쪽: **Weighted Baseline** (박스에 Eq. 12) → **Active / Offline Learning Step** 화살표가 **Database construction 으로 되돌아간다**

⇒ 읽어야 할 것: **재가중과 weighted-baseline 은 같은 committee 를 쓰는 두 개의 독립 가지**다.
하나 없이 다른 하나만 해도 된다. (우리한텐 이게 중요 — §11 참조.)
`Vb = 0` 으로 두면 baseline 없는 순수 committee MD 가 된다고 본문이 명시.

### 6.2 §III A — weighted baseline 실증 (`Fig. 3`, `Fig. 4`)

삼펩타이드 REMD 120 ps, 12 replica 300–2440 K.

**`Fig. 3`** (⚠ **내가 안 본 그림** — §14 참조): 2,000 배열을 SOAP 특징의 PCA 1·2 축(x,y)과
replica 온도(z, 로그)로 뿌리고 **가중치 w 로 색칠**. 주변에 대표 배열 렌더.
SOAP 파라미터는 캡션에 있다 — cutoff **4 Å**, radial **n = 6**, angular **l = 4**, 가우시안 폭 **0.3 Å**.
본문 서술: 저온에선 폴리펩타이드 **형태(conformation)** 만 샘플 → 훈련셋에 잘 대표됨 → w 높음.
**≈500 K 이상에서 분해 시작 — 먼저 CO₂ 방출**, **≈1000 K 이상에서 NH₃·H₂O + 큰 조각**.
이 고에너지 반응은 훈련셋에 **하나도 없다** ⇒ w 급감 ⇒ NN 보정이 꺼지고 DFTB 로 후퇴.

**`Fig. 4`** (**내가 본 그림**): 왼쪽 4패널 = w(0–1) vs time(0–120 ps) @ 300/530/940/1670 K,
오른쪽 = 반로그 히스토그램 p(w), 12개 온도.
- figure-read: 300 K 는 대부분 w ≈ 0.8–1.0, **≈110–120 ps 구간에 w ≈ 0.3–0.45 섬이 잠깐** 나타난다.
  530 K 에서 그 섬이 잦아지고, 940 K 는 0까지 흩어지며, 1670 K 는 0–1 을 거의 균일하게 덮는다.
- figure-read: p(w) 봉우리는 **w ≈ 0.37** (본문은 "w ≈ 0.4" 라고 쓴다). 이 봉우리가 **CO₂ 이탈**에 대응.
- figure-read: `w → 1` 에서 p 는 300 K **≈ 8**, 2440 K **≈ 0.3** → **한 자릿수 이상 감소** (본문 주장과 일치).
  `w = 0` 쪽은 300 K ≲ 10⁻³ 에서 2440 K **≈ 2 × 10¹** 로 약 **4 자릿수** 증가.
- ⚠ **본문과 미세한 어긋남**: 본문은 w ≈ 0.4 봉우리가 *"at intermediate T ... emerges"* 라 했는데,
  그림에선 **300 K 곡선에도 이미 p ≈ 0.04 수준으로 보인다.** 새로 생기는 게 아니라 자라는 것.

**본문의 정직한 단서 2개** (인용가치 있다):
- 가중치 없이 하면 *"typically occur within the first 100 ps of a similar REMD simulation"* — 즉 **비가중이면 100 ps 안에 터진다.**
- 외삽 구간에서 얻은 배열은 *"do not reach the level of accuracy of the high-end electronic structure method,
  but only that afforded by the baseline potential"* — **안정성을 사는 것이지 정확도를 사는 게 아니다.**

### 6.3 §III B — 짝분포함수 g(r) (`Fig. 1`, `Fig. 5`)

**`Fig. 1`** (**내가 본 그림**) — 방법론 검증의 핵심 그림.
3패널, x = Distance 1–4.5 Å.
- 위: committee 궤적의 H–H g(r), 첫 봉우리 figure-read ≈ 4 @ ≈1.55 Å, 둘째 ≈1.5 @ ≈2.4 Å, 셋째 ≈1.25 @ ≈3.8 Å
- 가운데: `Δg^(i)(r) = g^(i)(r) − ḡ̄(r)`, **NNP 1–4 각각을 실제로 따로 돌린 궤적**에서.
  진폭 figure-read **±5 × 10⁻²** (첫 봉우리 근처가 가장 큼). g(r) 봉우리 4 대비 **≈1 %**.
- 아래: **NNP 3 독립궤적(주황, 오차밴드 포함) vs Direct 재가중 Eq. (22)(보라) vs CEA Eq. (24)(초록)**
  → figure-read: **세 곡선이 주황 밴드 안에서 사실상 겹친다.** 유일하게 눈에 띄는 차이는
  ≈1.5 Å 의 음의 골에서 Direct(보라)가 살짝 더 깊다 (figure-read ≈ −5.3 vs −5.0 × 10⁻²).
- ⇒ **재가중(정확판·CEA판) 이 독립궤적을 실제로 재현한다** — 이 논문에서 **전파식이 검증된 유일한 자리**.
  단 이건 **평균의 검증**이지 **폭(불확실도)의 검증이 아니다.** (§10-b)

본문 평가: 이 계는 셀이 작고 committee-평균과 개별 NNP 차이가 작아 정확판/CEA 차이가 없다.
그래도 **CEA 를 권장**한다 (안정성·통계효율 + 오차원 분리가 드러남).

**`Fig. 5`** (**내가 본 그림**) — 3패널, 파란 실선 = committee 값, **빨간 음영 = Eq. (28) 불확실도**.
- **H–H 물** (x 1–4.5, y 0–4): 밴드가 거의 안 보인다. figure-read: 첫 봉우리·첫 골 모두 선 두께 수준.
- **O–O 물** (x 1–6.5, y 0–2.x): 첫 봉우리 ≈2.8 (figure-read ≈2.9), **첫 골 ≈3.3–3.5 Å 과 둘째 봉우리 ≈4.5 Å 에서 밴드가 보이기 시작** (figure-read ≈ ±0.05).
  본문 표현: 첫 봉우리 위치·높이 오차는 *"minuscule"*, 장거리 O–O 특징에서 약간 커짐.
- **CH₃SO₂OH···PhOH** (x 1–7, y 0–3.x): **밴드가 확연히 크다.** figure-read: 첫 봉우리 ≈3.1 에서 ≈2.95–3.2,
  **첫·둘째 배위껍질 사이 골(≈3.5–4 Å)에서 ≈0.55–1.0 (즉 ±0.22)** 로 최대.
- ⇒ 본문 해석과 일치: 불확실도는 **상수가 아니고**, **배위껍질 사이 골에서 최대**.
  첫 배위껍질(수소결합 기하·개수)은 오차가 작다 ⇒ 정성적 해석은 안전하다.
- 산/페놀에서 밴드가 큰 이유를 본문이 두 갈래로 나눈다: (i) ML 퍼텐셜의 시험오차가 더 큼(조성이 복잡),
  (ii) **셀에 산 분자가 하나뿐이라 통계가 나쁨.**
  그리고 **"블록평균으로 낸 통계오차가 committee 재가중 오차와 comparable 하다"** 고 적는다 (수치 없음).

### 6.4 §III C 1 — 융점 (`Fig. 6`) ★ **우리 D 와 구조가 가장 닮은 절**

interface pinning: 고체–액체 계면을 강제로 유지시키는 바이어스
`W(A) = (κ/2)[Q(A) − a]²` (Eq. 29), Q = local Q6, a = 165. 그러면
```
Δμ(T) = −κ( ⟨Q⟩′ − a )                                                     … Eq. (30)
⟨Q⟩′_{V^(i)} = ⟨Q⟩′_V̄ − β⟨Q(V^(i)−V̄)⟩′_V̄                                   … Eq. (31)  ← CEA 적용
```
8개 온도에서 Δμ 를 재고 **선형적합** → `Δμ(T_m) = 0` 의 **절편(근)** 이 T_m,
**기울기**가 Δs_m, `Δh_m = T_m Δs_m`.

**`Fig. 6`** (**내가 본 그림**): y = `μ^Ih − μ^L` [meV], **−5 ~ +2.5**; x = Temperature 260–295 K.
- 위 패널: committee 점 8개 + 적합 직선, **≈290 K 에서 0 교차**.
  figure-read 점: 260 K ≈ −4.3, 265 ≈ −3.7, 270 ≈ −3.3, 275 ≈ −3.2, 280 ≈ −1.6, 285 ≈ −1.7, 290 ≈ +1.0, 295 ≈ +1.2.
- 아래 패널: **모델별 적합 4개** (COMM 1–4) + 각자의 T_m^(i) 를 **0선 위 ✕ 마커**로.
  figure-read T_m^(i): **COMM 4 ≈ 285 K · COMM 2 ≈ 288 · COMM 1 ≈ 289.5 · COMM 3 ≈ 295** → 폭 ≈10 K.
  본문 보고 **290 ± 5 K** 와 정합 (±5 = 표준편차).

**논문이 여기서 명시적으로 던지는 방법론 경고 (우리한테 결정적)**:
> *"in view of the **linear nature of the CEA**, the values of the molar entropy and latent heat of melting
> computed from the mean of the committee estimates **match exactly** those computed directly...
> In principle, the two estimates T_m and T̄_m **differ**, even if in this case they are equal within the
> confidence interval. **Whenever a non-linear procedure is involved in the calculation of the property of
> interest, results may change based on the way the committee estimates are combined.** Comparing different
> approaches is then a useful check to assess the robustness of the error estimation."*

⇒ **Δs_m, Δh_m 은 적합계수의 선형함수라 "평균 후 적합" = "적합 후 평균".
   T_m 은 적합계수의 비(근)라 비선형이므로 두 순서가 다르다.**
   논문이 택한 것은 **"멤버별로 끝까지 계산한 뒤 산포를 재기"** — §4.1 Eq. (7) 뒤 문장과 같은 처방.

**정직한 단서**: 이 T_m·Δs_m·Δh_m 은 ref 70 의 유사 퍼텐셜 값과 다르고, 이유는
*"**substantial finite-size effects**"* 이며, 이 계산은 *"only meant to demonstrate the application of this
uncertainty quantification approach, and **not to provide size and sampling-converged values**"* 라고 밝힌다.

### 6.5 §III C 2 — 탈양성자화 자유에너지 (`Fig. 7`) ★ **비선형 전파의 실측 레시피**

metadynamics + **ITRE**(Iterative Trajectory Reweighting, ref 75) 로 시간의존 바이어스를 언바이어싱.
가중치 `u(A(t)) = e^{β(ṽ(t)−c(t))}`.
```
p̄(s) = ⟨ δ(s_O(A)−s) u(A) ⟩_V̄                                              … Eq. (32)
p^(i)(s) = p̄(s) − Δp^(i)(s),   Δp^(i)(s) = β⟨ δ(s_O−s) u(A) (V^(i)−V̄) ⟩_V̄  … Eq. (33)  ← CEA
Δp = std_i[Δp^(i)]                                                          … Eq. (28) 형태
```
★ **결정적 문장**: *"The **symmetric** uncertainty on the population results in a confidence range on the
free energy which is **asymmetric** about −kT log(p̄), spanning values from −kT log(p̄+Δp) to −kT log(p̄−Δp)."*
⇒ **비선형 변환(−kT log)을 통과시키는 법 = 상·하한을 각각 변환한다.** 표준오차 전파식을 안 쓴다.

**`Fig. 7`** (**내가 본 그림 — 자동추출이 놓쳐서 수동 복구했다**, §14): y = FE [kJ/mol] 0–25, x = s_O 0.43–1.07.
- figure-read: 최소 **s_O ≈ 0.99 에서 FE ≈ 2.6**, 밴드 폭 ≈ ±0.3 (거의 안 보인다) ⇒ 중성 상태는 확실.
- figure-read: **s_O ≈ 0.5 에서 파란 선 ≈ 19.3, 밴드 아래끝 ≈ 17.3, 위끝은 축 상단 25 를 넘어 잘린다.**
  s_O ≈ 0.45 에선 선 ≈ 21.5, 아래끝 ≈ 20.
- ⇒ 본문의 **20 (+5 / −2) kJ/mol** 과 정합하고, **위쪽 +5 가 정확히 축 상단(25)에 닿는다.**
  밴드가 눈으로 봐도 **위가 아래보다 훨씬 두껍다** — 비대칭이 그림에서 직접 읽힌다.
- 본문 해석: 중성 최소 근방은 불확실도가 매우 작고 **탈양성자화 상태에서 급증** —
  ref 7 의 정성적 관찰(해리 배열이 훈련셋에 덜 대표됨)과 일치.

**정직한 단서**: *"other errors, e.g. those due to finite-size effects and reference energetics, are likely to be
**comparable** with that obtained from the spread of the committee members."*
⇒ **committee σ 는 총오차가 아니다.** 유한크기·참조에너지 오차가 같은 크기로 옆에 있다.

### 6.6 §III D — 유한온도 전자 DOS of 액체 Ga (`Fig. 8`) ★ **σ_a 와 σ_V 를 갈라 보여주는 유일한 자리**

```
DOS(E,A) = (2/N_bN_k) Σ_n Σ_k δ(E − E_n(k,A))                               … Eq. (34)
DOS^(j)(E,A) = Σ_{k∈A} LDOS^(j)(E, A_k),  j = 1…M′                          … Eq. (35)  국소환경 분해 학습
```
참조 DOS = Kohn–Sham 고유값을 **가우시안 0.5 eV** 로 컨볼브. 구조 간 비교 위해 **E_F 정렬**;
E_F 는 전하중성 `N_e = Σ_E f(E,E_F,T)·DOS(E,A)`, `N_e = 2`(스핀 겹침) 로 정의.
**M′ = 64 를 쓴 이유를 본문이 밝힌다**: 훈련셋이 작고,
*"commitee predictions for **sparse kernel models add negligible overhead** on top of a single prediction."*

**`Fig. 8`** (**내가 본 그림**): 위 = ⟨DOS(E)⟩_T [eV⁻¹/state] 0–0.6, x = Energy −18…+6 eV, E_F = 0.
아래 = Error [eV⁻¹/state] 0–0.022, **회색 채움 = σ(총) · 파랑 = σ_a · 빨강 = σ_V**.
- figure-read: −15 근처에 **Ga 3d 반심(semicore) 봉우리**가 축을 뚫고 올라간다. E_F 근처 ⟨DOS⟩ ≈ 0.5, +5 eV 에서 ≈ 0.56.
- figure-read 오차: **σ_a(파랑)가 σ(회색)와 거의 포개진다** ⇒ **σ_a 가 지배**.
  σ_V(빨강)는 원자가띠 영역에서 σ_a 의 대략 **1/3–1/2**:
  −5 eV 에서 σ_a ≈ 0.004 / σ_V ≈ 0.0015 · E_F 근처 σ_a ≈ 0.009 / σ_V ≈ 0.002 ·
  +5 eV 에서 σ_a ≈ 0.020 / σ_V ≈ 0.007 · 반심 봉우리에서 σ_V ≈ 0.016 (σ_a 는 축 밖).
- ⇒ 제곱합이므로 σ_V 가 σ_a 의 1/3 이면 **총 σ 에 대한 기여는 ~5 %**. 그래서 회색≈파랑으로 보인다.

**본문 결론 3줄 (그대로 옮길 값어치가 있다)**:
- *"Even though the absolute error on the DOS is small, the ML uncertainty, **which is dominated by σ_a, is larger than the statistical error due to finite sampling**."*
- *"Even though in this case the error on the OM is dominant, **σ_V is sizeable**."*
- *"It would be relatively easy to reduce σ_a by increasing the training of the DOS model.
  In general, **the coupling between the potential energy and the observable property cannot be neglected**."*

### 6.7 §Appendix A / `Fig. 9` — α 의 M 의존

**`Fig. 9`** (**내가 본 그림**): 바이올린, x = M (4 → 16, 로그 눈금), y = α (≈1.7–5.8).
**초록 = 편향판 Eq. (5) · 파랑 = 편향보정판 Eq. (A5)**. 점 = 표본평균.
표본은 **M_max = 16 개 학습 모델 중 M 개를 뽑는 C(16, M) 가지 전부**.
- figure-read 평균: M = 4 초록 **≈ 4.6** / 파랑 **≈ 2.62** · M = 8 초록 ≈ 3.3 / 파랑 ≈ 2.77 ·
  M = 16 초록 **≈ 2.99** / 파랑 **≈ 2.77**.
- figure-read 폭: 파랑 분포가 M = 4 에서 **≈ 1.7–3.4** 로 넓고, M = 16 에서 선 하나로 수렴.
- ⇒ **편향보정판은 M 에 거의 무관**(2.62 → 2.77, +5.7 %; 본문 *"within 10 %"* 와 일치).
  **편향판은 M = 4 에서 65 % 과대**.
- ⚠ **본문과의 긴장 (내가 그림에서 찾은 것)**: §III B 1 이 물에 대해 보고한 **α = 2.1(무편향) / 3.75(편향)** 는
  같은 물 계인 `Fig. 9` 의 M = 4 평균(figure-read 2.62 / 4.6)보다 **양쪽 다 낮고**,
  점근값 2.77 보다 **약 24 % 낮다**. 실제 생산 committee 4개가 M = 4 분포의 **아래쪽 꼬리**에 앉아 있다는 뜻이다.
  ⇒ **§III B 1 의 물 g(r) 오차밴드는 점근 교정 대비 ~25 % 좁을 수 있다.**
  ⚠ 단정 못 하는 이유: 생산 committee 4개가 부록의 16개 부분집합인지 논문이 말하지 않고, 검증셋이 다를 수도 있다.

## 7. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | 물 H–H g(r). 위=committee, 가운데=NNP 1–4 **독립궤적** Δg(r)(±5×10⁻²), 아래=NNP 3 독립궤적 vs Direct 재가중(Eq. 22) vs CEA(Eq. 24) | **이 논문에서 전파식이 검증된 유일한 그림.** 단 검증된 것은 **평균의 재현**이지 **오차폭의 커버리지가 아니다** — 우리가 CEA 를 인용할 때 이 구분을 지켜야 한다 |
| 2 | 전체 워크플로 도식 (DB → 참조계산 → 부분표집 → M모델 학습 → α교정 → committee MD → {CEA 재가중 → 관측량 불확실도} / {weighted baseline → active learning → DB 로 복귀}) | **두 가지가 독립 가지**임이 여기서 보인다. 우리는 재가중 가지를 못 쓰지만(단일모델), baseline 가지는 PET-MAD LLPR 로 대체 가능 |
| 3 | 삼펩타이드 2,000 배열을 SOAP-PCA 2축 + 온도축에 뿌리고 가중치 w 로 색칠. 주변에 대표 배열 (SOAP r_c 4 Å, n=6, l=4, σ 0.3 Å) | ⛔ **내가 안 본 그림.** 정성적 삽화이고 정량은 `Fig. 4` 가 대신한다. 우리 축(이온전도·산화안정)과 무관 |
| 4 | 가중치 w 의 시계열(300/530/940/1670 K) + 12온도 로그 히스토그램 p(w) | **"모델이 언제 모르는지"를 온도로 스캔한 그림.** 우리가 MLIP-MD 온도사다리(600/800/1000 K)에서 그대로 흉내낼 수 있는 진단 형태 — 단 우리는 w 대신 이종 committee 불일치를 축으로 써야 한다 |
| 5 | 3계 g(r) + Eq. (28) 불확실도 밴드 (H–H 물 / O–O 물 / 산···페놀) | **불확실도는 상수가 아니다 — 배위껍질 사이 골에서 최대.** 우리 g(r)·RDF 그림에 밴드를 붙일 때 "봉우리는 안전, 골은 위험" 이라는 구조적 예상 |
| 6 | Ih–액체 화학퍼텐셜차 vs T. 위=committee 적합, 아래=모델별 적합 4개 + T_m^(i) ✕마커 | ★★ **우리 D(MSD 기울기)·Ea(아레니우스 기울기)와 구조가 가장 닮은 그림.** "멤버별로 끝까지 계산 → 유도량 분포" 레시피의 실물. **동시에 §10-b 의 비판 근거** — 점의 통계산포가 눈에 보이는데 ±5 K 에 안 들어갔다 |
| 7 | 산/페놀 탈양성자화 자유에너지 프로파일 + **비대칭** 불확실도 밴드 | ★ **비선형 전파의 실측 레시피** — 대칭 Δp 를 −kT log 로 통과시켜 상·하한을 따로 변환. 우리 D_rel 비·Arrhenius log 기울기에 직접 대응하는 절차 |
| 8 | 액체 Ga 유한온도 DOS + 오차 분해 (σ 총 / σ_a OM / σ_V PM) | ★ **σ_a 와 σ_V 를 갈라 그린 유일한 그림.** 우리 D 에는 σ_a 항이 아예 없다(D 는 학습된 관측량이 아니다) ⇒ 우리 모델 불확실도는 전부 σ_V 형이고, 이 논문은 σ_V 를 **정적 평균에 대해서만** 계산한다 |
| 9 | 교정계수 α 의 바이올린 분포 vs M (초록 편향 / 파랑 무편향), M_max=16 의 C(16,M) 부분집합 전부 | ★ **M ≥ 4 하한 · M = 4 에서 65 % 과대 · 무편향판은 M 무관.** 우리 3종 committee·3시드가 왜 위험한지의 외부 근거. **본문 α=2.1 과의 긴장**도 여기서 나온다 |

## 8. Post-processing

- **committee 통계**: Eq. (1)(2) 평균·분산 → Eq. (5)/(6) 로그우도 최대화로 α → Eq. (7) 재척도.
- **재가중**: 궤적을 따라 **멤버별 퍼텐셜에너지 V^(i)** 를 (탈상관된) 배열들과 함께 저장.
  사후에 Eq. (22)(정확) 또는 Eq. (24)(CEA) 로 멤버별 앙상블 평균을 복원. **MD 재실행 없음.**
- **g(r)**: 최소상 분리 히스토그램. **committee 멤버 간 차이는 오직 가중치를 통해서만 들어온다** —
  본문 명시: *"the calculation of g^(i)(r) ... depends on i **through the weights alone**."*
- **자유에너지**: PLUMED 로 Q6 구속(interface pinning) · metadynamics + **ITRE** 언바이어싱.
- **DOS**: 국소환경 분해 SOAP 커널 학습(ref 46), 가우시안 0.5 eV 스미어, 전하중성으로 E_F 정렬 후 평균.
- **active learning 연결**: 문턱 넘는 σ(A) 배열을 모아 DB 에 추가 (오프라인/온라인 둘 다).
- **도구**: i-PI · LAMMPS + n2p2 · PLUMED · DFTB+ · GAMESS-US · CP2K · Quantum ESPRESSO.

## 9. 우리 DFT/MLIP 대비 → `our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 판정 |
|---|---|---|---|
| 물성값 비교 | **없다** — 물·펩타이드·페놀·Ga | LPSCl 아르지로다이트 | ⛔ **물성 4축(A 이온/B 산화/C 기계/D 전자) 어디에도 안 들어간다.** 이건 **방법 원전**이지 비교 대상이 아니다 |
| MLIP 종류 | 계마다 **전용 학습** Behler–Parrinello NNP (M = 4–5) | **UMA-s-1p1(omat) 단일 파운데이션 모델** | ⇒ **committee 를 만들 수 없다** (§10-d) |
| 불확실도 원천 | 훈련 참조구조 유한성 (보간오차) | 우리 blocker 는 **2축**: 모델 + 시드/궤적 | 이 논문은 **모델축만**, 그것도 정적 평균만 |
| 관측량 | 전부 **정적 배위평균** | **D = MSD 기울기 (동역학량)** | ★ **구조가 다르다.** §11-2 |
| MD 창/통계 규약 | 물 2 ns · Ga 400 ps · 산/페놀 16런 1.6 ns | prod 200 ps, **MSD 창 2–50 ps 고정**, 600/800/1000 K | 논문은 궤적 통계규약을 형식화하지 않는다 |
| 온도 | 300 K(물)·363 K(산)·1800 K(Ga) | **600 K** 기준 | β 가 앞에 붙는 σ_V(Eq. 28)는 **고온에서 작아진다** — 우리 온도가 유리한 방향 |
| 참조 범함수 | revPBE0-D3 / PBE+dDsC / PBE | UMA 는 OMat24 = **VASP PBE**; 우리 DFT 도 PBE | 계열은 같지만 이 논문은 범함수 오차를 **명시적으로 범위 밖**에 둔다 |
| 시드 축 | ⛔ 형식화 없음 | modelc 3시드 Ea **0.197 ± 0.032 eV** · 단일시드 1.33× 철회 선례 | **이 논문은 우리 시드축을 도와주지 않는다** |

## 10. 비판 — 이 논문의 약한 곳 ★ (§10)

**(a) §II A 의 committee 정의와 §III A 의 실제 committee 가 다르다.**
이론은 *"복원 없는 부분표집으로 M 개 훈련셋"* 인데, 삼펩타이드는
*"**초기화 가중치와 내부 CV 분할(90/10)만** 다르다"* — 데이터를 거의 전부 공유한다.
이건 부분표집 committee 가 아니라 **시드 앙상블**이고, 두 종류는 산포의 의미가 다르다
(전자는 데이터 유한성, 후자는 최적화 다중성). 논문은 이 불일치를 언급하지 않는다.
그리고 하필 그 계가 **α = 1.0** — 유일하게 교정이 필요 없었던 계다.
데이터를 덜 흔든 committee 가 왜 더 잘 교정돼 있나? 검증셋이 달라서(삼펩타이드 자체 검증)일 수도 있고
설명이 없다. ⚠ 내 관찰이지 논문의 주장이 아니다.

**(b) 전파식의 "폭"은 검증되지 않았다 — 캘리브레이션 보고가 사실상 없다.**
- `Fig. 1` 하단이 검증하는 것은 **평균의 재현**(재가중 g(r) ≈ 독립궤적 g(r))이다.
  **오차밴드가 실제 오차를 몇 % 포함하는지(coverage) 를 보인 그림·표가 하나도 없다.**
  신뢰도 곡선(reliability diagram)·binned predicted-vs-actual error 도 없다.
- α 는 **단일점 에너지·힘**에 대해 검증셋으로 맞춘 것이고, **전파된 열역학 평균의 폭**이
  그 α 로 잘 교정되는지는 별도 문제인데 시험되지 않았다.
- 통계오차와의 대조는 **전부 정성적**: *"comparable"*(산/페놀 블록평균), *"larger than the statistical
  error"*(Ga DOS). **숫자가 없다.**
- ⇒ 사용자 질문 3 의 답: **과소/과대 방향은 α 를 통해 간접적으로만 말한다** —
  `α = 2.1 / 4.08 > 1` 이므로 **raw committee 산포는 참오차를 2–4배 과소추정**한다는 것이
  이 논문의 실측이다. 이건 강한 정보다. 그러나 **교정 후의 폭이 옳은지는 안 보인다.**

**(c) `Fig. 6` 의 ±5 K 는 통계오차를 안 담고 있다.**
그림에서 개별 점이 각 적합선 주위로 눈에 띄게 흩어진다 (figure-read: 270 K 에서 초록 점 ≈ −1.1 인데
초록 적합선은 ≈ −2.6 → 편차 ≈1.5 meV, Δμ 전체 범위 ≈6 meV 의 25 %). 본문도
*"individual points are somewhat scattered due to statistical errors"* 라고 인정한다.
그런데 보고된 **±5 K 는 모델별 T_m^(i) 의 표준편차뿐**이다. 통계오차를 따로 내서 합치지 않았다.
⇒ **우리 규율("창 4개의 max−min 은 불확도가 아니다" · Q7)과 같은 종류의 문제**를
이 논문도 갖고 있다. 방향만 반대다 — 우리는 창을, 이들은 모델을 유일한 오차원으로 삼았다.

**(d) σ_b = 7 × 10⁻³ meV/atom 은 물리적으로 이상해 보인다.**
DFTB3/3OB+D3BJ 와 PBE/def2-TZVP 의 차이가 **7 µeV/atom** 이라는 뜻인데, 보통 meV–수십 meV/atom 이다.
단위 오타(7 × 10⁻³ **eV**/atom = 7 meV/atom)일 가능성이 있다.
⚠ **PDF 가 적은 그대로 옮겼고 나는 판정하지 않는다.** 다만 스킴 자체는 무해하다 —
Eq. (12) 의 가중치 `w = σ_b²/(σ_b²+σ²)` 는 **비(ratio)** 만 쓰므로 절대 척도가 상쇄된다.
(`Fig. 4` 에서 300 K 의 w 가 1 근처인 것은 σ(A) 도 같은 척도라는 뜻이다.)

**(e) Eq. (3) 의 무상관 가정이 MD 데이터와 안 맞는다.**
*"any two true values y_ref(A) and y_ref(A′) are uncorrelated if A ≠ A′"* —
그런데 훈련·검증 구조는 MD 궤적에서 나오므로 시간상 강하게 상관돼 있다.
논문도 *"training points cannot be considered to be independent identically distributed samples"* 라고 인정하고
**그 효과를 전부 α 하나에 흡수**시킨다. 스칼라 하나로 상관구조를 대신하는 것은 강한 축약이다.

**(f) α 가 A 에 무관하다는 가정은 정확히 우리가 걱정하는 곳에서 깨진다.**
α 는 **전역 스칼라**다. 그런데 외삽 영역에서는 committee 산포의 **모양**까지 달라질 수 있다
(과소추정이 특정 영역에만 몰림). 그러면 스칼라 재척도로는 못 고친다.
논문은 이 가능성을 검사하지 않는다.

**(g) 본문 α = 2.1 과 `Fig. 9` 의 M = 4 분포가 어긋난다** — §6.7 참조. ⚠ 단정 불가(검증셋 미확인).

**(h) `Fig. 4` 의 w ≈ 0.4 봉우리는 "중간 온도에서 나타나는" 것이 아니라 "자라는" 것이다** — §6.2 참조. 사소하다.

**(i) 저자가 스스로 적은 한계** (사용자 질문 6 — 이건 비판이 아니라 논문의 정직한 부분):
1. 직접 재가중은 `Var[β(V^(i)−V̄)]` 에 **지수적으로** 나빠지고, 그 분산은 **계 크기에 따라 증가**한다.
   ⇒ **큰 셀에서 Eq. (22)는 못 쓴다.** CEA 가 우회지만 그건 선형화다.
2. Eq. (A5) 의 무편향성은 **가우시안일 때만** — *"usually only approximately true."*
3. **비선형 조합으로 전파하면 유사 편향이 재발** ⇒ **M ≥ 6 권고.**
4. **M ≥ 4 하드 하한** (`(M−1)/(M−3)` 발산).
5. weighted baseline 은 외삽 구간에서 **베이스라인 정확도밖에 못 준다** —
   짧은 외삽 구간이거나 REMD 저온부만 필요할 때만 유효.
6. weighted baseline 은 **베이스라인이 존재해야** 한다. 원자단위판을 쓰려면 σ_b 를 원자당으로 재정의.
7. 융점 수치는 **유한크기 효과**로 ref 70 과 다르며 **수렴값이 아니다** (명시).
8. 산/페놀에서 **유한크기·참조에너지 오차가 committee σ 와 comparable** ⇒ **committee σ ≠ 총오차.**
9. 프레임워크가 재는 것은 **훈련 참조구조가 유한해서 생기는 오차뿐** — 참조법 자체의 오차는 범위 밖.

## 11. 우리 좌표 ① — **단일 UMA 로 이 논문의 무엇을 쓸 수 있고 무엇을 못 쓰나** ★★

### 11-1. 못 쓰는 것 (구조적으로 불가)

| 논문의 것 | 왜 못 쓰나 |
|---|---|
| **σ_V (Eq. 28)** — 이 논문의 대표 산출물 | 정의상 **서로 다른 `V^(i)` 가 M ≥ 2 개** 필요. 단일 UMA 는 `V^(i) − V̄ ≡ 0` ⇒ **σ_V ≡ 0**. "불확실도가 0" 이 아니라 **측정할 수단이 없다** |
| **α 교정 (Eq. 5/6)** | 교정할 산포 자체가 없다. 게다가 α 를 재려면 **참조 DFT 검증셋**이 필요한데, UMA 의 훈련분포(OMat24)를 우리가 안 갖고 있어 "훈련셋 유한성 오차" 라는 개념이 우리 쪽에서 정의되지 않는다 |
| **on-the-fly 재가중 (Eq. 22/24)** | 재가중해서 갈 **다른 앙상블이 없다**. `w^(i) ≡ 1` |
| **weighted baseline (Eq. 12)** | `σ²(A)` 가 없다 ⇒ 가중치가 상수 1. **단, 대체재가 있다** — PET-MAD 의 `calculate_uncertainty=True`(LLPR)는 **단일 모델 내장 불확실도**라 `σ²(A)` 자리에 꽂힌다. 우리 `comparison_vs_ours.md` §J-5 가 이미 이 처방을 적어 뒀다 |
| **Eq. (26) 의 σ_a 항** | 우리 D 는 **학습된 관측량이 아니다** (궤적의 범함수). OM committee 가 존재하지 않는다 ⇒ σ_a 는 정의되지 않음(0 아님, n/a). **우리 모델 불확실도는 전부 σ_V 형이다** — 그런데 그게 못 재는 항이다 |

### 11-2. 쓸 수 있는 것 (수치가 아니라 **구조·규율**)

1. **★ 분해 규율 자체** — `σ̃² ≈ σ_a² + σ_V²`.
   "관측량 모델 오차" 와 "샘플링(퍼텐셜) 오차" 를 **따로 세고 제곱합하라**.
   우리 D 에 옮기면: **σ_a 없음 · σ_V 못 잼 · 남는 것은 통계(시드/블록) 뿐** —
   ⇒ **우리가 지금 낼 수 있는 D 오차막대는 "통계 오차막대" 이지 "총 불확실도" 가 아니다.**
   이 문장이 이 digest 의 실무 결론이다. 우리 규율 *"σ 절대값 인용 금지, 비율도 멀티시드 판정만"* 은
   이 논문 기준으로 **과한 게 아니라 최소한**이다.
2. **★ M ≥ 4 하한 · M ≥ 6 권고** (Eq. A4, 부록 마지막).
   우리 이종 committee 는 **M = 3** (UMA · MACE-MP-0 · SevenNet-0) ⇒ **하한 미달.**
   우리 modelc Ea 도 **3시드** ⇒ 같은 자리.
   ⚠ **정확히 말한다**: `(M−1)/(M−3)` 발산은 **`1/σ²` 의 기댓값**에 대한 것이라
   *committee 산포로 나누는 절차*(교정·z-score·정규화 문턱)에 걸린다. 우리 3시드 SD 는 그냥 표본SD 라
   **분산 자체는 여전히 무편향**이다 — 다만 **SD 의 상대오차가 `1/√(2(M−1))` = M=3 에서 50 %** 다
   (내 계산, 논문 값 아님). ⇒ **3점으로 낸 ±는 그 자신이 ±50 % 다.**
   PET-MAD 를 4번째 멤버로 넣자는 우리 처방(§J-5)은 이 논문 기준으로 **"권장" 이 아니라 "하한 도달"** 이다.
3. **★ raw 산포는 좁다 (α = 2.1 · 4.08 > 1)**.
   우리가 committee/시드 불일치를 그대로 오차막대로 쓰면 **과소추정 쪽**이 기본 방향이다.
   우리는 α 를 잴 수 없으므로 ⇒ **우리 불일치는 "하한(lower bound)" 으로만 말할 수 있다.**
   `"불일치가 작았으니 안전하다"` 는 결론을 **이 논문이 지지하지 않는다.**
   (우리 `b2o3_committee_2026_09_07.json` 의 허용선 *"모델 간 불일치가 특별히 크지 않았다"* 는
   이 논문과 정확히 양립한다 — 그 이상 나가면 안 된다.)
4. **★ 비선형 유도량의 처리 순서** (Eq. 7 뒤 문장 + §III C 1 경고 + `Fig. 7`):
   **멤버별로 끝까지 계산한 뒤 그 산포를 재라. 평균을 먼저 내고 변환하지 마라.**
   비대칭이 나오면 비대칭으로 보고하라(상·하한을 각각 변환).
   우리 Arrhenius Ea(로그 기울기)·D_rel(비)에 그대로 적용되는 절차 규율이다 — **축만 바꿔서**(§13).
5. **`Fig. 4` 형태의 온도 스캔 진단** — "모델이 언제 모르는지"를 온도축으로 스캔.
   우리는 w 대신 이종 committee 불일치를 축으로 쓴다. 600/800/1000 K 사다리에 그대로 얹힌다.
6. **β 가 앞에 붙는다는 것** (Eq. 28): 같은 공분산이면 **고온일수록 σ_V 가 작다.**
   우리가 600 K 이상에서만 재는 것은 이 방향으로는 유리하다. ⚠ 단 공분산 자체가 고온에서 커질 수 있어
   **순효과는 미정** — 이건 내 관찰이고 논문이 논하지 않는다.

## 12. 우리 좌표 ② — **이종(heterogeneous) committee 에 이 논문의 통계가 적용되나** ★

우선 **우리 도구의 사실관계를 정정한다** (사용자 프롬프트의 표현과 코드가 다르다):

> `tools/ionic/mlip_committee.py` 의 **`force_contrast` 는 이종 committee 가 아니다.**
> 코드(`cmd_force_contrast` / `contrast_from_forces`)는 **한 엔진(기본 UMA)의 예측을 파일 안의
> DFT 라벨과 비교**해 골격 힘오차를 내고, 그것을 **test 계 / control 계 두 계 사이의 비 R** 로 만든다.
> 카드 `db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json` 의 보고량이다.
> **이종 3종 committee 는 `sample` → `predict --engine {uma,mace,sevennet}` → `analyze` 경로**이고,
> 거기서 재는 것은 **엔진 쌍 간 힘 불일치**(`per_pair_force_rms`, `committee_frame_disagreement`)다.
> ⇒ 이 논문과 대응하는 것은 **`analyze`** 쪽이다.

**이 논문의 통계가 서 있는 가정 3개, 그리고 우리 `analyze` 에서 각각 어떻게 되나:**

| 가정 | 논문 | 우리 이종 committee (UMA/OMat24 · MACE-MP-0/MPtrj · SevenNet-0/MPtrj) |
|---|---|---|
| (i) M 모델이 **같은 참조 y_ref** 를 근사 (Eq. 3 이 `\|y_ref−ȳ\|²` 를 씀) | 한 DB, 한 참조법 | ⛔ **깨진다.** 전부 PBE 계열이지만 **훈련셋과 DFT 설정이 다르다**(OMat24 vs MPtrj). 세 모델의 target 이 같은 함수가 아니다 ⇒ 불일치에 **훈련셋 계통차**가 섞이고, 그건 "이 배열이 외삽인가" 와 무관한 성분이다 |
| (ii) 멤버가 **교환가능(exchangeable)** — 같은 절차로 만들어 한 분포에서 뽑은 표본 | 부분표집이라 성립 | ⛔ **깨진다.** MACE-MP-0 과 SevenNet-0 이 **둘 다 MPtrj** 라 강하게 상관. 실질 표본수는 3이 아니라 **≈2 클러스터**. 상관된 멤버는 산포를 **과소평가**한다 (우리 §J-5 가 이미 지적) |
| (iii) 예측분포가 근사 가우시안 (α 보정의 전제) | 검증 안 함(인정) | ⛔ **검증 불가** — 참조 라벨이 없어 α 를 못 잰다 |

⇒ **판정: 이 논문의 `σ²`·`α`·`σ_V` 식을 우리 이종 committee 에 그대로 쓰면 안 된다.**
남는 것은 **순서적(ordinal) 신호**뿐 — *"이 배열은 다른 배열보다 합의 밖이다."*
그리고 그것이 정확히 우리 `analyze` 가 하는 일이고, 우리 도구는 이미
*"교정 모드에서 초과 개수는 정보가 아니다"* 라는 **순환성 경고**를 코드에 달아 뒀다.
⇒ **이 논문은 우리 이종 committee 를 정당화해 주지 않는다.** 오히려 M = 3 · 상관 · 비교환성
**세 가지를 전부 지적하는 쪽**이다.

**한 가지는 오히려 우리 편이다**: 이 논문의 α 논리는
*"committee 산포는 절대 오차가 아니라 **교정이 필요한 대리지표**"* 라고 말한다.
이종 committee 는 교정할 수 없으므로 **문턱을 상대적으로만** 써야 하는데,
우리가 이미 그렇게 한다(select/break 분리 · 기준선은 **별도 평형 벌크 표본**에서 잡고 다른 표본에 적용).
**이 논문 정신과 맞다.**

## 13. 우리 좌표 ③ — **D_rel 비(ratio) 와 분자·분모 상관** ★

**보고량**: `D_rel(design, host) = D*(design) / D*(host)` @ 600 K · MSD 창 2–50 ps (비준).

**논문이 상관된 분자/분모를 직접 다루나 — 아니다.** 두 계를 비교한 예제가 하나도 없다.
그러나 **비(ratio)형 유도량**을 다룬 자리는 있고, 처방이 명확하다:

1. **`Fig. 6` 의 T_m 이 바로 비형이다** — 선형적합의 **근** = (절편)/(기울기).
   논문의 처리: **멤버별로 적합 → 멤버별 T_m^(i) → 그 평균·표준편차.**
   ⇒ **비를 먼저 만들고 그 다음 산포를 잰다.** 이 순서가 공통성분을 자동 상쇄시킨다.
2. **논문의 명시 경고**: *"Whenever a **non-linear procedure** is involved ... results may change based on
   **the way the committee estimates are combined**. Comparing different approaches is then a useful check."*
3. **Eq. (7) 뒤**: 재척도된 예측으로 *"arbitrarily-complicated non-linear functions"* 를 계산하고
   **변환된 예측들의 평균·산포**를 쓰라.
4. **`Fig. 7`**: 대칭 Δp → `−kT log` → **비대칭 구간**. 상·하한을 각각 변환.
5. **부록**: 비선형 조합 시 편향 재발 가능 ⇒ **M ≥ 6.**

**⇒ 이식 가능한 규칙 (논문의 정신이지, 논문의 문장이 아니다)**
> `D_rel` 의 불확실도는 **같은 멤버끼리 짝지어 비를 먼저 만들고**, 그 M 개 비의 산포로 낸다.
> 절대 `D` 의 상대오차를 각각 낸 뒤 `√(rel² + rel²)` 로 합치지 않는다 —
> 그건 **상관을 0 으로 가정**하는 것이고, 공통 모델편향이 있으면 **과대추정**이다.
> 그리고 비는 비선형이므로 **비대칭 구간**을 각오한다.

**⚠ 그런데 우리한테는 이 규칙이 곧바로 안 선다 — 이유 두 가지를 분명히 한다.**

**(A) 우리는 M = 1 이다.** 짝지을 멤버가 없다. 그러니 위 규칙은 **모델축에서 실행 불가**다.

**(B) 시드축으로 옮겨 짝짓는 것은 정당화되지 않는다.** ★ 이게 중요하다.
논문에서 상관이 상쇄되는 이유는 **같은 궤적을 재가중**했기 때문이다 — 분자·분모가 **물리적으로 같은 표본**을 공유한다.
우리 design 과 host 는 **다른 계·다른 궤적**이다. "시드 번호가 같다" 는 것은 **난수열이 같다는 것뿐**이고
물리적 상관이 아니다. ⇒ **시드 짝짓기로 상관을 상쇄한다고 주장할 근거가 이 논문에 없다.**
(우리 규율에 이미 같은 종류의 판정이 있다 — Q7: *"겹친 창은 강상관이라 독립 반복처럼 읽으면 안 된다."*
여기는 반대 방향의 오류다: **상관이 없는 것을 있다고 가정하는 것.**)

**(C) 그래서 D_rel 에서 모델 공통편향이 상쇄되기를 바라는 것은 — 희망이지 측정이 아니다.**
"같은 UMA 가 두 계를 같은 방향으로 틀리게 본다" 는 **모델축의 진술**인데, 우리는 모델이 하나라
**그 진술을 검증할 수 없다.** 비를 쓰는 것이 절대값을 쓰는 것보다 나은 것은 맞지만,
**이 논문이 그 개선폭을 보증해 주지 않는다.** ⇒ 우리 규율 *"비율도 멀티시드 판정만"* 은 유지되고,
거기에 한 줄을 더 붙일 수 있다: **"비를 쓴다고 모델 불확실도가 상쇄된다고 쓰지 않는다."**

## 14. 우리 좌표 ④ — **축 구분 최종 판정** ★ (사용자의 ⚠ 항목)

| 우리 blocker 의 축 | 이 논문 | 근거 |
|---|---|---|
| **① 모델 불확실도 — 훈련 참조구조 유한성** | ✅ **완전히 덮는다** (정적 관측량에 한해) | §II 전체, Eq. (26)–(28) |
| ① 중에서도 **동역학 관측량(D, 상관함수)** | ⛔ **전무** | `diffusion`·`transport`·`MSD`·`Green–Kubo`·`time-correlation`·`conductivity` **전부 0회**(전문 grep) |
| ① 중에서도 **참조법(범함수) 오차** | ⛔ 범위 밖 (명시) | §I 문제설정 |
| **② 시드/궤적 통계 불확실도** | ⛔ **형식화 없음** | 정성 언급 3회뿐: *"comparable"*(§III B 2) · *"larger than the statistical error"*(§III D) · *"somewhat scattered"*(§III C 1). **±5 K 에 통계오차가 안 들어갔다**(§10-c) |
| 유한크기 | ⛔ 범위 밖 (직접 인정) | §III C 1 |

**★ 왜 D 에 이 논문의 σ_V 를 못 쓰나 — 한 문단으로**
Eq. (18)–(24) 는 전부 **배위 q 에 대한 볼츠만 가중치**를 다시 매기는 것이다.
`V` 를 바꾸면 **배열의 확률**이 바뀌고, 그 변화를 `w^(i) = e^{−β(V^(i)−V̄)}` 로 흉내낼 수 있다.
그러나 **D 는 배열의 확률이 아니라 배열들의 시간 순서(궤적)에서 나온다.**
`V` 를 바꾸면 **힘이 바뀌고 궤적 자체가 갈라진다** — 같은 스냅샷 집합에 가중치를 다시 매기는 것으로는
**시간상관을 복원할 수 없다.** 정적 재가중은 *"어떤 배열을 얼마나 자주 보나"* 를 고치지
*"그 배열에서 다음 순간 어디로 가나"* 를 고치지 못한다.
⇒ **이 논문의 핵심 트릭(단일 궤적 → M 앙상블 복원)은 D 에 원리적으로 확장되지 않는다.**
논문은 이 한계를 **주장하지도 부인하지도 않는다** — 동역학량을 아예 언급하지 않기 때문이다.
⚠ 그러므로 *"Imbalzano 를 따라 D 에 committee 불확실도를 붙였다"* 는 문장은 **쓸 수 없다.**

## 15. 적용 인사이트 (우리 다음 수)

1. **★ D 오차막대의 이름을 바꾼다.** 지금 우리가 낼 수 있는 것은 **통계(시드/블록) 오차막대**이고
   **모델 불확실도가 아니다.** 이 논문이 그 구분을 형식화해 준다(σ_a + σ_V vs 통계).
   `db/properties/` 와 원고 캡션에서 *"uncertainty"* 를 **`seed/statistical spread`** 로 명시하면
   리뷰에서 걸릴 자리를 미리 막는다. (우리 Q7 판정과 같은 계열.)
2. **★ committee 를 M ≥ 4 로 올리는 것이 "권장" 이 아니라 "하한 도달" 이다.**
   PET-MAD(§J-5) 또는 UMA-1.2 를 4번째로 넣자는 기존 처방이 이 논문으로 **정량적 근거**를 얻는다
   (`Fig. 9` · Eq. A4). ⚠ 단 §12 대로 **이종이라 α 교정은 여전히 불가** — 문턱은 상대적으로만.
3. **★ `Fig. 7` 레시피를 Ea·D_rel 에 적용한다.** 비대칭 구간을 각오하고, **변환 후 산포**를 낸다.
   지금 우리 Ea 는 `0.197 ± 0.032` 처럼 대칭으로 적혀 있는데, 아레니우스 로그 기울기라
   **원칙적으로 대칭이 아니다.** 3시드에서 비대칭을 논하는 것은 무의미하니(§11-2·2),
   **당장 할 일은 값을 바꾸는 게 아니라 "이 ±는 대칭 가정" 임을 적어 두는 것**이다.
4. **`Fig. 4` 형 온도스캔 진단**을 이종 committee 불일치로 만들어 600/800/1000 K 에 얹는다.
   "고온에서 합의가 무너지나" 는 우리가 400/500 K 를 버린 판정과 짝이 되는 질문이고, 비용이 거의 0 이다
   (기존 궤적 스냅샷 재사용).
5. **weighted-baseline 은 우리한테 당장 쓸모가 없다** — 베이스라인 퍼텐셜이 없고, 우리 MD 는
   폭주하지 않는다. 다만 **PET-MAD LLPR 을 σ²(A) 자리에 꽂으면 Eq. (12) 가 그대로 성립**한다는 것은
   기록해 둘 값어치가 있다 (미래 옵션).

## 16. 인용 가능 문장 (deck / paper 용)

- "Committee-based uncertainty quantification propagates the model error not only to single-point
  predictions but also to **static thermodynamic averages**, decomposing the total variance into a
  property-model term and a **sampling (potential-model) term** (Imbalzano et al.)."
- "The raw spread of a sub-sampled committee **systematically underestimates** the true error and requires
  a calibration factor; reported values are **α = 2.1 for liquid water and α = 4.08 for methanesulfonic
  acid in phenol** — i.e. factors of ~2–4 (Imbalzano et al.)."
- "At least **four** committee members are required for a meaningful calibration constant, and **six or more**
  are recommended whenever the uncertainty is propagated through a **non-linear** combination of members
  (Imbalzano et al., Appendix A)."
- "For quantities derived through a non-linear procedure, **the way the committee estimates are combined
  changes the result**; the recommended practice is to carry each member through the full analysis and take
  the spread of the transformed values (Imbalzano et al.)."
- ⛔ **쓰면 안 되는 문장**: *"이 방법으로 확산계수/이온전도도에 불확실도를 붙일 수 있다."*
  논문에 동역학량이 **한 번도** 나오지 않는다.

## 17. 이 논문이 **못 하는 것** / 내가 **확인 못 한 것** ★ (필수 절)

**이 논문이 못 하는 것**
1. **동역학량 불확실도** — D · 상관함수 · 수송계수. **원리적 확장도 안 된다**(§14).
2. **시드/궤적 통계 불확실도의 형식화** — 정성 언급 3회뿐, 숫자 0.
3. **오차폭의 커버리지 검증** — 신뢰도 곡선·coverage 표 없음. `Fig. 1` 은 **평균**만 검증한다.
4. **참조법(범함수) 오차** — 명시적 범위 밖.
5. **유한크기 오차** — 범위 밖 (융점에서 직접 인정).
6. **큰 셀에서의 정확 재가중** — 계 크기에 지수적으로 나빠진다. CEA(선형화)로만 우회.
7. **단일 모델 UQ** — committee 가 없으면 이 논문의 어떤 식도 값을 못 낸다.
8. **이종 committee** — 가정 (i)(ii)(iii) 이 전부 깨진다(§12).
9. **두 계의 비(ratio)** — 예제 0. `Fig. 6` 의 T_m 이 구조적으로 가장 가깝지만 **한 계 안**이다.
10. **α 의 구조 의존성** — 전역 스칼라로 가정하고 검사 안 함.
11. **비가우시안** — Eq. (A5) 무편향성이 깨진다고 스스로 적음.
12. **아르지로다이트·황화물·Li 이온전도체 근거 0** — 이 논문에 그런 계가 없다. 물성값 이전 **0건**.

**내가 확인 못 한 것**
- **서지**: 저널·권·페이지·DOI·arXiv 번호. PDF 에 도장이 없다. 슬러그의 `2021` 은 **미확인**.
- **`Fig. 3`**: ⛔ **안 봤다.** SOAP-PCA 산점도 + 분자 렌더로 정성적이고, 정량은 `Fig. 4` 가 대신한다고 판단했다.
  ⇒ *"저온에선 conformation 만 샘플한다"*, *"500 K 에서 CO₂, 1000 K 에서 NH₃/H₂O"* 는
  **본문 서술을 그대로 옮긴 것이고 그림으로 대조하지 않았다.**
- **`Fig. 7` 의 위쪽 밴드 상한**: 축 상단 25 에서 **잘려 있어** 실제 상한을 못 읽었다.
  본문 `+5` 와 정합하지만 그림만으로는 확인 불가.
- **σ_b = 7 × 10⁻³ meV/atom 의 단위** — 오타 여부 판정 불가 (§10-d).
- **물 α = 2.1 과 `Fig. 9` 의 M = 4 분포 불일치의 원인** — 생산 committee 가 부록 16개의 부분집합인지,
  검증셋이 같은지 논문이 밝히지 않는다.
- **본문 미기재 사양**: 물 committee 를 어떻게 부분표집했는지(ref 70 으로 넘김) · 산/페놀 committee 구성(ref 7 로 넘김) ·
  Ga 퍼텐셜의 α · 각 계의 N_s/N 비율 · 학습 비용.
- **참고문헌 원문**: ref 36(Musil 2019 교정), ref 46(Ben Mahmoud DOS), ref 50(Ceriotti 2012 재가중 비효율),
  ref 7(Rossi 2020) 을 **읽지 않았다.** 이 digest 의 해당 서술은 전부 이 PDF 안의 인용 문맥 기준이다.
- **SI**: 이 PDF 에 SI 가 없다 (16 pp 단일 파일). 별도 SI 존재 여부 미확인.

## 18. 기법 미니 용어집

- **committee (query-by-committee / ensemble UQ)**: 같은 데이터로 여러 모델을 독립 학습해,
  **예측의 산포**를 불확실도로 쓰는 비-베이지안 방법. 가우시안 과정처럼 정확한 사후분산은 없지만 **훨씬 싸다**.
- **sub-sampling vs bootstrap**: 이 논문은 **복원 없이(without replacement)** 크기 `N_s < N` 부분집합 M 개
  (= subagging). 부트스트랩은 복원추출로 크기 N. **다르다.**
- **out-of-bag 검증**: 훈련셋 안의 구조 중 *"적어도 n 개의 부분집합에 안 들어간"* 것을 검증에 쓰는 것.
  별도 참조계산이 필요 없다. (이 논문의 두 번째 검증셋 전략.)
- **calibration factor α**: committee 산포를 참오차 척도에 맞추는 **전역 스칼라**.
  로그우도 최대화로 얻고, M 이 작을 때 **편향**된다.
- **Basu 정리**: 정규분포에서 **표본평균과 표본분산이 독립**이라는 정리.
  부록에서 `E[ȳ²/σ²] = E[ȳ²]E[1/σ²]` 로 인수분해할 때 쓴다.
- **Δ-learning / baselined model**: `V = V_baseline + V_ML`. ML 은 **차이만** 배운다.
  값싼(부정확한) 물리 모형 위에 얹으므로 데이터가 적게 든다.
- **weighted baseline**: 위 구조에서 ML 보정을 **불확실도 역가중**으로 켜고 끈다.
  외삽하면 자동으로 베이스라인으로 후퇴 ⇒ 궤적이 안 터진다.
- **reweighting (Torrie–Valleau umbrella)**: 앙상블 A 에서 뽑은 표본에 `e^{−β(V_B−V_A)}` 가중치를 곱해
  앙상블 B 의 평균을 얻는 것. **원리적으로 정확**하지만 두 앙상블이 겹치지 않으면 통계효율이 붕괴한다.
- **curse of system size (재가중)**: `Var[β(V_B−V_A)]` 가 원자수에 비례해 커지고,
  재가중 오차는 그 분산에 **지수적**으로 커진다 ⇒ 큰 셀에서 재가중이 죽는다. (Ceriotti 2012)
- **CEA (cumulant expansion approximation)**: 위 지수가중치를 **1차 누율까지 전개**해 선형화한 것.
  `⟨a⟩_B ≈ ⟨a⟩_A − β Cov_A(a, V_B−V_A)`. 통계적으로 안정하고 오차원 분해가 드러난다.
- **PM / OM (potential model / observable model)**: 퍼텐셜 committee 와 관측량 committee.
  **별개**다. 관측량이 학습된 것이 아니면 OM committee 는 존재하지 않는다.
- **interface pinning**: 고체–액체 계면을 order parameter(local Q6)에 스프링을 걸어 유지시키고,
  스프링이 받는 평균 힘에서 `Δμ` 를 읽는 자유에너지 기법. (Pedersen 2013)
- **ITRE (Iterative Trajectory Reweighting)**: metadynamics 처럼 **시간의존 바이어스**가 걸린 궤적에서
  비편향 확률분포를 되찾는 반복 알고리즘. (Giberti 2020)
- **local Q6 / Steinhardt 매개변수**: 결합방향 대칭성으로 결정/액체를 구분하는 order parameter.
- **GLE (generalized Langevin equation) thermostat**: 색잡음 열욕. 표본화를 가속한다. (Ceriotti 2010)
- **farthest-point sampling**: 특징공간에서 서로 가장 먼 구조를 순차로 뽑아 훈련셋 다양성을 확보하는 법.
- **SOAP**: Smooth Overlap of Atomic Positions — 원자환경 기술자. 이 논문에서는 PCA 좌표(`Fig. 3`)와
  Ga DOS 학습 커널에 쓴다.

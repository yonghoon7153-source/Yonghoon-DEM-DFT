# MD (MLIP) / MSD / Arrhenius — 분자동역학 이온수송

> 기계학습 퍼텐셜(MLIP)로 DFT 힘을 대체해 큰 셀을 긴 시간 돌리고, Li 이온의 평균제곱변위(MSD)에서 확산계수 $D$를, 온도별 $D$의 Arrhenius 기울기에서 활성화에너지 $E_a$를, Nernst–Einstein으로 전도도 $\sigma$를 뽑는 방법.

## 목차
1. Langevin NVT 동역학
2. MLIP가 DFT 힘을 대체
3. MSD와 Einstein 관계
4. 시간창 피팅
5. Arrhenius — 활성화에너지
6. Nernst–Einstein 전도도

---
## 1. Langevin NVT 동역학
일정 온도(NVT) 앙상블을 만들려고 Langevin thermostat을 쓴다. 뉴턴 운동방정식에 마찰항과 랜덤힘을 더해 원자가 열욕과 에너지를 주고받게 한다.

$$m_i \ddot{\mathbf{r}}_i = \mathbf{F}_i - m_i \gamma \dot{\mathbf{r}}_i + \sqrt{2 m_i \gamma k_B T}\,\boldsymbol{\xi}_i(t)$$

- $\mathbf{F}_i$: 퍼텐셜에서 온 힘 (MLIP가 제공)
- $\gamma$: 마찰계수 (friction) — 우리는 **0.02**
- $\boldsymbol{\xi}_i$: 백색잡음, $\langle\xi(t)\xi(t')\rangle = \delta(t-t')$
- 시간 간격 $dt$ = **2 fs**

> [!note] 왜 Langevin인가
> 마찰+잡음이 fluctuation–dissipation 정리를 만족해 정확한 온도 $T$의 정준 분포를 샘플링한다. friction이 크면 열평형은 빠르나 동역학이 흐려지고, 작으면 반대 — 0.02는 그 절충값.

---
## 2. MLIP가 DFT 힘을 대체
매 step DFT를 부르면 200 ps(10만 step)는 불가능하다. **MLIP**가 DFT 데이터로 학습된 퍼텐셜 에너지면 $E(\{\mathbf{r}_i\})$을 주고, 그 그래디언트로 힘을 즉석에서 준다.

$$\mathbf{F}_i = -\nabla_{\mathbf{r}_i} E_{\text{MLIP}}(\{\mathbf{r}_j\}) \;\approx\; \mathbf{F}_i^{\text{DFT}}$$

우리는 **UMA-s-1p1 (omat)** 파운데이션 모델을 쓴다. DFT급 정확도를 유지하며 수천 배 빠르다 → 통계적으로 의미 있는 확산 통계를 얻는다.

> [!warning] UMA는 Li₃N에 사용 금지
> UMA는 LPSCl 계열 MD에서 검증된 표준이지만, **Li₃N에는 결정론적 편향**이 확인돼(2026-06 판정) 사용 금지. 모델의 적용 범위를 벗어나면 힘이 계통적으로 틀린다.

---
## 3. MSD와 Einstein 관계
확산은 평균제곱변위(MSD)로 측정한다. 시간 $t$ 동안 각 Li가 얼마나 멀어졌나의 앙상블 평균이다.

$$\text{MSD}(t) = \big\langle |\mathbf{r}_i(t) - \mathbf{r}_i(0)|^2 \big\rangle$$

3차원 확산에서 MSD는 시간에 선형이고, 기울기가 확산계수 $D$를 준다 (Einstein 관계):

$$\text{MSD}(t) = 6 D t \;\Longrightarrow\; D = \frac{1}{6}\frac{d\,\text{MSD}(t)}{dt}$$

계수 6은 3차원(각 축 $2Dt$ × 3). 2D 확산이면 4, 1D면 2로 바뀐다.

---
## 4. 시간창 피팅
MSD 곡선 전체를 다 쓰면 안 된다. 구간마다 성격이 다르다.

- **초기(ballistic, < ~1 ps)**: $\text{MSD}\propto t^2$ — 아직 확산 아님, 진동
- **중간(diffusive)**: $\text{MSD}\propto t$ — 여기 기울기가 진짜 $D$
- **후기(long-time)**: 통계 부족으로 노이즈 급증

그래서 **MSD 피팅 창을 2–50 ps로 고정**한다. 이 창을 조성마다 똑같이 써야 비교가 공정하다.

$$D = \frac{1}{6}\cdot\frac{\text{MSD}(50\,\text{ps}) - \text{MSD}(2\,\text{ps})}{50 - 2\,[\text{ps}]}$$

| 구간 | 거동 | 사용 |
|------|------|------|
| 0–1 ps | ballistic $t^2$ | 제외 |
| **2–50 ps** | diffusive $t^1$ | **피팅** |
| > 50 ps | noisy | 제외 |

Setup: equilibration **5 ps** 버린 뒤 production **200 ps** 생성.

### 피팅 품질 체크
- **선형성**: 2–50 ps 창에서 MSD가 직선인지($R^2$) 확인 — 굽으면 아직 diffusive 아님.
- **평형 확인**: equilibration 뒤 온도·에너지가 평탄한지 본다 (앞 5 ps는 버림).
- **등방성**: $x, y, z$ 성분 MSD가 비슷한지 — 한 축만 크면 통계 부족 또는 1D 채널.
- **시드 평균**: 서로 다른 초기속도 시드로 반복해 블록 평균 — 단일시드는 못 믿는다.

### 4b. 확산영역 게이트 — β (R²로는 못 잡는다)

로그-로그 눈금에서 MSD의 **국소 기울기**가 β다:

$$\text{MSD} \propto t^{\beta}, \qquad \beta = \frac{d(\log \text{MSD})}{d(\log t)}$$

| β | 뜻 | 물리 그림 |
|---|---|---|
| ≈ 2 | 탄도 | 첫 충돌 전 직선 비행 (< ~1 ps) |
| **0.8–1.2** | **확산 (게이트 통과)** | 홉이 충분히 많아 랜덤워크 — MSD = 6Dt 가 성립하는 유일한 구간 |
| < 0.8 | 케이지 | 자리 안 진동 + 드문 홉. 평균이 희귀 점프에 지배됨 |
| → 0 | 갇힘 | MSD 평탄 |

> [!warning] R² 0.97이어도 확산이 아닐 수 있다 (2026-08-04 실측)
> MSD = a + b·t^0.6 같은 곡선도 직선 적합하면 R²가 높게 나온다. **LPSOCl 600 K:
> R² 0.975인데 β 0.61** — "직선처럼 보임"과 "확산임"은 다른 판정이다. 기울기/6을
> D라고 부르려면 그 기울기가 *랜덤워크의* 기울기여야 한다. 판정 도구:
> `tools/ionic/msd_diffusive_check.py` (+ MSD 창끝 ≥ 3 Å² 병행).

### 4c. 적합 규율 3건 (2026-08-04 확립 — 3계 200 ps 재적합에서)

1. **절편 자유**: MSD = 6Dt + c 로 맞춘다. 원점 강제는 케이지 진동 오프셋을 기울기에
   밀어넣어 D 를 부풀린다 (실측: 절편 최대 9.1 Å²).
2. **시드 앙상블 평균이 기본**: 같은 계·같은 T에서 시드에 따라 β 0.98 ↔ 0.52 로
   갈렸다 (LPSOCl 600 K). "대표 시드 1개"는 그 갈림을 숨긴다. 독립 시드는 같은 계의
   다른 초기속도라 MSD 평균이 정당하다.
3. **같은 시드의 재실행은 평균 금지**: licube(밀도 cube용 50 ps 재실행)를 섞으면
   이중계상 + 격자 절단. 독립성이 없는 궤적은 시드가 아니다.

### 4b-2. β 는 시간이 아니라 **홉 수**를 잰다 — 그래서 예측된다

이온당 홉 수로 환산하면 게이트 결과가 **미리 계산된다**:

$$n_{\text{hop}} = \frac{\text{MSD}}{d_{\text{hop}}^2} = \frac{6 D t}{d_{\text{hop}}^2}
\qquad (d_{\text{hop}} \approx 3\,\text{Å} = \text{이웃 Li 자리 간격})$$

| n_hop | 뜻 |
|---|---|
| ≥ 10 | 확산 통계 충분 (β ≈ 1 기대) |
| 3–10 | 경계 — 시드마다 β 가 흔들린다 |
| < 3 | 홉 부족 — **β 가 낮게 나오는 게 정상** (측정 실패이지 물리가 아니다) |

**600 K · 200 ps 예측 vs 실측 (2026-08-04)**

| 계 | 예측 n_hop | 실측 β | |
|---|---|---|---|
| LPSCl1.6 | 13.9 | 0.87 | ✓ |
| **LPSOCl1.6** | **8.4** (경계) | **0.61** | **⛔** |
| B₂O₃@LPSCl1.6 | 13.9 | 0.81 | ✓ |

LPSOCl 만 탈락한 이유가 여기서 닫힌다 — Ea 가 90 meV 높아 같은 온도·시간에서 D 가
0.60배이고 **홉이 40% 적다**. 도구 `tools/ionic/hops_per_ion.py` · 표
`db/properties/hops_per_ion.csv` (전 온도 200 ps 기준).

⚠ n_hop 은 **상한**이다. 되돌아오는 홉(back-correlated)을 안 세는데 실제 SE 는
Haven 비 H_R 0.3–0.7 < 1 = 상관 운동이라(litdb `dyre2004`) 같은 MSD 에 더 많은 홉이 든다.

### 4b-3. 저온 β 저하는 "현실적"인가 — 둘을 갈라야 한다

| | **표집 인공물** (우리 경우) | **진짜 아확산** |
|---|---|---|
| 원인 | 궤적이 짧아 홉이 몇 번 없음 → 희귀 사건이 평균을 지배 | 케이지 진동·되돌아오는 홉·상관 운동이 만드는 **실재하는** 중간시간 거동 |
| 물리인가 | 아니다 (측정 실패) | 그렇다 |
| 시간↑ | 홉이 쌓이며 β → 1 **수렴** | 상관 시간을 넘기면 β → 1 **crossover** |

**핵심: 진짜 아확산도 점근적으로는 β = 1 이다** (아니면 D 자체가 정의되지 않는다).
그러니 저온에서 β 가 낮게 나오는 것 자체는 현실적이지만, **그 β 의 기울기를 D 라고
쓰면 안 된다** — 두 원인이 같은 숫자로 보이기 때문이다.

**판별 실험**: 궤적을 늘렸을 때 β 가 오르는가. comp1 600 K 200 → **1600 ps** 연장이
정확히 이 검사다 (진행 중). 오르면 표집 문제, 안 오르면 그 온도·그 셀에서 확산이
실재하지 않는다는 결론(= D 인용 불가가 답).

### 4d. 게이트 판정 현황 (2026-08-04, 200 ps · 창 2–50 ps)

| 계 | 600 K | 800 K | 1000 K | 시드 근거 |
|---|---|---|---|---|
| LPSCl (comp1) | ⛔ 0.17–0.79 | ⛔ | (0.52) | s2·s3 — **전 판 탈락**, 1600 ps 연장 중 |
| LPSCl1.6 | 0.87 ✓ | 0.93 ✓ | 0.92 ✓ | **3시드 평균** (600 K 200 ps · hiT 100 ps) |
| **LPSOCl1.6** | **0.61 ⛔** | 0.86 ✓ | 1.02 ✓ | **4시드 평균** (최초 게이트 검사) |
| B₂O₃@LPSCl1.6 | 0.81 ✓ | 0.83 ✓ | 0.97 ✓ | **3시드 평균** (600 K 200 ps · hiT 100 ps) |

- **v2 (전 계 멀티시드 평균)에서 유일한 탈락 = LPSOCl 600 K.** modelc·b2o3 의
  단일시드 '아슬' 판정은 3시드 평균으로 해소됐다 (0.82→0.87 / 0.81 유지-통과).
  b2o3 600 K 3시드 D 1.039e-5 = 등록 아레니우스 D_600_mean 1.041e-5 재현 ✓.
- LPSOCl 600 K: MSD 는 97 Å²@200 ps 로 충분 — 크기가 아니라 **홉 통계** 문제
  (시드산포 36%). O 트랩의 홉 희소화와 정합. → **Ea 0.287±0.024 는 이 점을 포함한
  적합이라 재검토 대상**. 처방 = 6점 아레니우스 30런(신규 27 + lpsocl 600 재실행 3, 2026-08-04 결정)과 기존 게이트-통과 점으로 재적합.
- 그림·데이터: `docs/figures/msd_3sys_200ps.png` · `db/properties/msd_3sys_200ps_origin.csv`
  (PROVENANCE/GATE NOTE 블록 포함) · 상세: `kb/reports/paper_first_author_requests_2026_08.md` §4

---
## 5. Arrhenius — 활성화에너지
확산은 열활성 과정이라 온도에 Arrhenius 의존한다.

$$D(T) = D_0 \exp\!\left(-\frac{E_a}{k_B T}\right) \;\Longrightarrow\; \ln D = \ln D_0 - \frac{E_a}{k_B}\cdot\frac{1}{T}$$

$\ln D$ vs $1/T$가 직선이고, **기울기 $= -E_a/k_B$**. 우리는 **600 / 800 / 1000 K 3점**으로 피팅한다.

$$E_a = -k_B \cdot \frac{d(\ln D)}{d(1/T)}$$

> [!important] 400/500 K를 제외하는 이유
> 저온에선 200 ps 안에 hop이 몇 번 안 일어나 MSD 통계가 diffusive 영역에 못 든다 → $D$가 과소·노이즈. 그래서 **400/500 K는 판정에서 제외**하고 600/800/1000 K 3점만 쓴다. $E_a$ 오차막대는 600 K 3-시드로 낸다.

---
## 6. Nernst–Einstein 전도도
확산계수에서 이온 전도도 $\sigma$를 추정한다 (Haven ratio = 1 가정).

$$\sigma = \frac{N q^2}{V k_B T}\, D \qquad (H_R = 1)$$

- $N/V$: Li 수밀도, $q$: Li 전하
- $H_R=1$은 이온 운동 상관을 무시한 상한 근사

> [!warning] 절대값 인용 금지 · 멀티시드 판정만
> UMA-MD의 **$D$·$\sigma$ 절대값은 citeable truth가 아니다.** 조성 간 **비율조차 멀티시드로 판정**해야 하며 단일시드 값은 못 믿는다 — 실제로 단일시드 1.33× 우세 주장이 멀티시드에서 철회된 사례(SEMIFINAL 2026-07-09)가 있다. 인용 가능한 건 다중시드로 재현된 순위/비율과 $E_a$(오차막대 포함)뿐.

```mermaid
graph TD
    A[UMA-s-1p1 MLIP forces] --> B[Langevin NVT dt 2 fs friction 0.02]
    B --> C[Equilibrate 5 ps]
    C --> D[Production 200 ps]
    D --> E[MSD window 2-50 ps]
    E --> F[D = slope / 6]
    F --> G[Repeat at 600 800 1000 K]
    G --> H[Arrhenius ln D vs 1/T]
    H --> I[Ea from slope]
    F --> J[Nernst-Einstein sigma HR=1]
    J -.absolute forbidden multiseed only.-> K[Ratios by multiseed]
    style A fill:#e0ebff,stroke:#2563eb
    style E fill:#fef9c3,stroke:#2563eb
    style I fill:#e2f6ec,stroke:#059669
    style J fill:#fde2e2,stroke:#dc2626
```
**한 문장 요약**: UMA MLIP로 긴 NVT 궤적을 만들어 2–50 ps MSD 기울기에서 $D$를, 600/800/1000 K Arrhenius에서 $E_a$를 뽑되, $D$·$\sigma$ 절대값은 멀티시드로만 판정한다.

---
## 우리 캠페인 적용
UMA-s-1p1(omat), Langevin NVT, dt 2 fs, friction 0.02, equilib 5 ps / prod 200 ps, MSD 창 2–50 ps 고정, Arrhenius 600/800/1000 K 3점 (tools/modelc_v3/, tools/ionic/).

| 조성 | 약칭 | $E_a$ (eV) | 비고 |
|------|------|-----------|------|
| Li₆PS₅Cl | comp1 | **0.253** | 기준 |
| Li₅.₄PS₄.₄Cl₁.₆ | modelc | **0.224** | 가장 낮은 장벽 |
| LPSOCl (+O) | lpsocl | **0.271** | O 도핑, 장벽 상승 |

- $E_a$ 순서: **modelc(0.224) < comp1(0.253) < +O(0.271)**. Cl-rich가 Li 이동에 유리, O 도핑은 장벽을 올린다.
- $E_a$ 오차막대는 **600 K 3-시드**로 산출. Arrhenius는 600/800/1000 K 3점(400/500 K 제외).
- **$D$·$\sigma$ 절대값 인용 금지.** 비율·순위도 **멀티시드 판정만** (단일시드 1.33× 철회 사례).
- **UMA는 Li₃N 금지** — LPSCl 계열에는 검증된 표준.


> [!note] 방법 간 비교
> "BV·NEB·MD 가 주는 $E_a$ 는 서로 다른 양"의 정리는 **[DFT](/concept/dft) §12** 에 있다
> (정의 차이 · BV 결손 물리 4가지 · 부호 뒤섞임 실측 · 신뢰도 순서).

*tags: MLIP-MD · UMA · Langevin NVT · MSD · Einstein relation · Arrhenius · activation energy · Nernst-Einstein · Li diffusion · multiseed*

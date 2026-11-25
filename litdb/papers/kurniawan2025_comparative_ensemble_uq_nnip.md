# Comparative study of ensemble-based uncertainty quantification methods for neural network interatomic potentials — Kurniawan, Wen, Tadmor & Transtrum (*Mach. Learn.: Sci. Technol.* **2026**, in press)

> slug `kurniawan2025_comparative_ensemble_uq_nnip` · DOI `10.1088/2632-2153/ae9fb4` · type `MLIP (방법론 / UQ 벤치마크)` · PDF `3501d83b-80._Comparative_study_of_ensemblebased_uncertainty_quantification_methods_for_neural_network_interatomic_potentials.pdf` · digested `2026-09-09` · status ✅
> **저자**: Yonatan Kurniawan¹ (현 Univ. of Toronto MSE), Mingjian Wen² (UESTC 청두), **Ellad B. Tadmor**³ (교신, Univ. of Minnesota 항공우주·역학), Mark K. Transtrum⁴ (Cross Stream Consulting) — ¹Brigham Young Univ. 물리천문 · 원고 ID `MLST-105722.R1` · Accepted Manuscript, CC BY 4.0 · 본문 17 pp + refs, **SI 는 별도 파일(우리 미보유)**
> **코드/데이터**: `https://github.com/yonatank93/compare_UQ` · 지원 NSF DMR-1834251 / DMR-1834332

> elements: C
> methods: DFT, MLIP, phonon, EOS

> ⚠⚠ **slug 의 `2025` 는 틀렸다.** 표지가 말하는 것은 **2026** 이다 (© 2026 The Author(s), IOP).
> slug 은 동시작업 조율 키라서 그대로 뒀다 — **인용할 때는 2026 을 쓴다.**
> ⚠ 저널도 정정: 사용자 기억의 *"Mach. Learn.: Sci. Technol. 2025"* 중 **저널은 맞고 연도가 틀렸다.**
> 저자 4인 중 **Transtrum 이 기억 목록에서 빠져 있었다**(Kurniawan·Wen·Tadmor → +Transtrum).

---

## 0. 이 digest 를 읽는 법 — 그리고 **먼저 정정할 것 하나**

이 논문은 *"MLIP 의 불확실도(σ)를 정확도(오차)의 대용으로 써도 되는가"* 를 **네 가지 앙상블 구성법**으로
비교해 답한다. 답은 **"ID 에서는 되고, OOD 에서는 안 된다 — 그것도 직관과 반대 방향으로 망가진다"** 다.

> 🔴 **의뢰문의 전제 하나를 먼저 부인한다.**
> *"복잡한 추정기가 단순 committee 를 일관되게 이기지 못했다"* 는 **이 논문의 초록에 없다.**
> 그 문장은 **서론에서 이 논문이 인용한 선행연구** — **Carrete et al. 2023** (*J. Chem. Phys.* **158**, 204801, ref [37]) —
> 의 결론이다. 원문(p3):
> > *"Carrete et al. [37] compared several ensemble constructions in OOD molecular-dynamics and
> > active-learning applications, finding that **more elaborate uncertainty estimators did not
> > consistently outperform simpler committees in identifying difficult configurations**."*
>
> 바로 다음 줄의 **Tan et al. 2023** (ref [26], *npj Comput. Mater.* **9**, 225) 도 같은 결에 있다:
> > *"compared model ensembles with several single-model UQ approaches and found that
> > **no method performed consistently best across all settings**."*
>
> ⇒ **"어려운 표본을 찾는 능력(OOD 탐지·능동학습 선별)" 이라는 의뢰문 §4 의 뉘앙스도 Carrete 편의 것**이다.
> 이 논문은 **능동학습을 하지 않고, OOD 탐지 성능(AUROC·precision@k 같은 것)을 재지 않는다.**
> 그 대신 **"σ 가 외삽 거리를 따라가는가"** 를 직접 재고 — **안 따라간다**는 더 센 음성 결과를 낸다(§5.6, §5.7).
>
> 이 논문 자신의 "복잡 vs 단순" 판정은 §5.3 에 **다른 형태로** 있다:
> **snapshot(훈련 1회) ≈ random initialization(훈련 100회)** 이고, ID 에서 **네 방법의 차이가 애초에 작다**.

**우리에게 중요한 순서**: §5.2–5.3(채점 지표) → §5.6–5.7(σ 가 감소하는 현상) → §11(우리 좌표) → §14(못 하는 것).

---

## 1. 한 줄 요약

탄소 동소체(그래핀·이중층·흑연·다이아몬드) NNIP 에 **bootstrap / MC-dropout / random-initialization /
snapshot** 네 앙상블(각 **100개 모델**)을 붙여, **분포 내(ID)** 에서는 σ 가 오차와 그런대로 상관하지만
**분포 밖(OOD, 여기서는 cold curve·phonon)** 에서는 σ 가 오차를 못 따라가고 **평탄해지거나 심지어 감소**하며,
그 병리는 **네 방법 전부·모든 동소체·심지어 SchNet(GNN)에서도** 나타난다는 것을 보인다.
⇒ **"σ 가 작다 = 믿을 만하다" 는 외삽 영역에서 성립하지 않는다.**

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | Kurniawan, Wen, Tadmor(교신), Transtrum |
| 저널/년 | *Mach. Learn.: Sci. Technol.* **2026** (in press, Accepted Manuscript) |
| DOI | `10.1088/2632-2153/ae9fb4` |
| 대상 계 | **탄소 단일원소**: monolayer graphene · bilayer graphene · graphite · diamond |
| 연구유형 | **순수 계산 방법론** (실험 0 · 새 물질 0 · 새 UQ 기법 제안 0) |
| 자기규정 | *"our goal is **not to propose methods for mitigating** issues regarding uncertainty, but rather to **characterize and analyze** the behavior"* (p4) |
| 인프라 | **OpenKIM** / KIM-API / **KLIFF**(학습·UQ) / ASE(포논·시뮬) / LAMMPS(언급) / Materials Project(기준 격자상수) |
| 기여물 | **KLIFF 에 bootstrap UQ 지원을 추가**했다(구성 단위 재샘플링이 기본값) |

---

## 3. 비교한 추정기 목록과 정의 ★ (의뢰문 §1)

> ⚠ **먼저 범위를 못박는다.** 제목 그대로 **ensemble-based** 만 비교한다.
> **GP · conformal prediction · mean-variance estimation · quantile regression · Bayesian NN · distance-based
> (LTAU-FF 등) 는 서론에서 이름만 언급되고 실험 대상이 아니다.** 의뢰문이 예상한 "GP/conformal 포함 비교표"는
> **이 논문에 없다.**

| # | 추정기 | 변동(randomness)의 출처 | 정의 — 앙상블을 **어떻게** 만드는가 | 필요한 **학습 횟수** | 원전 |
|---|---|---|---|---|---|
| ① | **Bootstrap** | **훈련 데이터** | 원 데이터셋을 **복원추출**해 합성 데이터셋 S개를 만들고 각각에 별도 NNIP 를 학습. ⚠ **구성(configuration) 단위로 재샘플링** — 한 배열 안 원자력들은 상호작용 때문에 상관돼 있어 점 단위 부트스트랩은 i.i.d. 가정을 깬다 | **S = 100회** | [53]; 구현은 **이 논문이 KLIFF 에 추가** |
| ② | **Monte Carlo Dropout** | **모델 구조(함수공간)** | 학습된 **하나의** 망에 **서로 다른 dropout mask** `D_l` 를 **추론 시에도** 걸어 노드 부분집합을 꺼서 S개 예측을 만든다. `y_l = σ_l(W_l(D_l y_{l−1}) + b_l)` | **1회** | Gal & Ghahramani 2016 [56] |
| ③ | **Random initialization** (= deep ensemble = 통상적 "committee") | **초기 파라미터** | 동일 구조·동일 하이퍼파라미터, **초기 weight/bias 만 다르게** 독립 학습. 비볼록 손실면이라 서로 다른 극소로 수렴 | **S = 100회** | Lakshminarayanan 2017 [59] |
| ④ | **Snapshot** | **최적화 과정(SGD 잡음)** | **한 번의 학습 궤적**에서 여러 epoch 의 모델을 저장해 앙상블로 쓴다. burn-in(손실 평탄화 전) 스냅샷은 버리고, **100 epoch 간격**으로 저장해 근사 독립 확보. SGD 궤적이 사후분포 샘플링과 유사하다는 논거(Chaudhari & Soatto [60]) | **1회** | Huang 2017 [61], Izmailov [62] |

**공통 규약 (네 방법 전부)**
- 앙상블 크기 **S = 100** (Wen & Tadmor 2020 [6] 을 따름 — 평균·σ 수렴 확보 목적).
- 예측 = 앙상블 평균 `µ_y = (1/S)Σy_s`, 불확실도 = **앙상블 표준편차** `σ_y² = (1/S)Σ(y_s − µ_y)²`
  (⚠ 원문 Eq. 8 은 `S−1` 표기가 조판에서 깨져 있다 — 분모가 `S` 인지 `S−1` 인지 표지에서 확정 불가).
- ⛔ **사후 보정(post-hoc calibration)을 일부러 하지 않았다.** *"σ_y is used directly as the raw ensemble spread"* —
  보정 절차·보정 데이터셋에 의존성이 생기는 것을 피하려고. **⇒ 이 논문의 σ 는 "날것"이다** (§14 참조).

---

## 4. DFT / 계산 방법 ★

### 4.1 참조 데이터(DFT) — 라벨을 만든 쪽
| 항목 | 값 |
|---|---|
| 코드 | **명시 없음** (n/a — VASP/QE 어느 쪽인지 본문에 없다) |
| functional | **PBE** [49] |
| vdW | **many-body dispersion (MBD)** — **bilayer graphene 과 graphite 에만** 적용 |
| plane-wave cutoff | **500 eV** |
| k-points | **Γ-centered Monkhorst–Pack**, "총에너지 수렴을 보장하도록 선택" (구체 격자 **미기재**) |
| 진공 | monolayer·bilayer 슬랩에 **≈ 30 Å** |
| pseudo/PAW | **n/a** |
| 데이터 출처 | Wen & Tadmor 2020 figshare 데이터셋 [48] — **이 논문의 새 DFT 가 아니다** |
| 샘플링 | **AIMD 300–900 K**(흑연·단층 그래핀은 **1,500 K** 궤적 추가) + 단층 그래핀 **등방 2축 변형 −3 %…+3 %** + 그 위치섭동 |

**Table 1 — 데이터셋 (본문 표, 정확값)**

| 구조 | 훈련 | 테스트 | 구성당 원자수 |
|---|---|---|---|
| Diamond | 759 | 84 | 64 |
| Graphite | 661 | 81 | 72 |
| Monolayer graphene | 2,181 | 185 | **2–32** |
| Bilayer graphene | 743 | 94 | 52–76 |
| **합계** | **4,344** | **444** | 총 **4,788** 구성 (90 / 10 무작위 분할) |

### 4.2 MLIP (본 모델)
| 항목 | 값 |
|---|---|
| 아키텍처 | **NNIP = multilayer perceptron**, `E = Σ_n E_n(ξ_n)` (원자별 에너지 합) |
| 은닉층 | **3층 × 128 노드**, 활성함수 **tanh** (미분가능·매끄러움 목적) |
| 기술자 | **atom-centered symmetry functions (ACSF)**, Behler 2011 [47] — 상세는 SI |
| 정칙화 | **dropout p = 0.1 을 모든 은닉층에** (학습 시). ⚠ **이 dropout 이 곧 ②의 UQ 기반** |
| 힘 | 에너지의 좌표 미분(해석적) |
| 손실 | `L = (1/M)Σ_m [ (r^E_m)² + ‖r^F_m‖² ]`, `r^E_m = (E^DFT − E)/(N_m σ_E)`, `σ_E = 1 eV`; `r^F` 는 성분별, `σ_F = √10 eV/Å` (에너지·힘 항 균형 + 무차원화) |
| 최적화 | **Adam**, batch **100**, lr **10⁻³ (0–5,000 epoch)** → **10⁻⁴ (5,000–40,000 epoch)**, 총 **40,000 epoch** |
| 모델 선택 | 대부분의 방법에서 **테스트셋 손실 최저 epoch** ⚠ (아래 §14-③) |
| 검증셋 | **없음** — 구조를 고정해 하이퍼파라미터 탐색을 없앴다고 명시 |
| 교차검증 | **held-out 단일 분할** (k-fold 아님) |
| 대조 아키텍처 | **SchNet** (GNN), 같은 데이터로 **4,000 epoch** 학습해 ID 오차를 NNIP 수준에 맞춤 → `Fig. 12` |
| 무질서 처리 | **해당 없음** (단일원소 결정 + AIMD 스냅샷) |

### 4.3 OOD 프로브 (large-scale property)
| 프로브 | 정의·설정 |
|---|---|
| **Energy cold curve** | 0 K 에서 `E/atom` vs 격자상수 `a`. MP 평형값 기준 **±10 %** 스캔(§5.7 에서는 **육방정계만 ±20 % 로 확장**). diamond 는 **등방 변형**(입방 대칭 유지); graphene/graphite 는 **면내 등방**(결합각 120° 고정); graphite 는 **c 완화 허용**하나 NNIP 예측에서 c 변화가 무시할 수준이라 `E(a)` 만 보고 |
| **Phonon dispersion** | 힘상수 행렬(에너지 Hessian) → 푸리에 변환 → 동역학 행렬 고유값. **ASE 유한차분** [43,65]. ⚠ **그림·수치가 전부 SI 에 있고 본문에 없다** — 우리는 **본문 서술만** 갖고 있다 |
| **왜 이게 OOD 인가** | 훈련 데이터가 300–1500 K AIMD + ±3 % 변형인데, cold curve 는 **0 K · ±10~20 % 변형** ⇒ 기하·온도 모두 훈련 밖 |

---

## 5. 결과 — 절별 상세

### 5.1 학습 상태 (`Fig. 5`, `Table 2`)
- `Fig. 5` (⚠ **크로핑 실패**, §9 참조): 훈련/테스트 손실 궤적이 거의 겹침 → **과적합 없음**.
- **Table 2 — ID RMSE (본문 표, 정확값)**

| 앙상블 | E 훈련 (meV/atom) | E 테스트 | F 훈련 (meV/Å) | F 테스트 |
|---|---|---|---|---|
| **Bootstrap** | 8.905 | **9.204** ← 최악 | 3.001 | **3.350** ← 최선 |
| **Dropout** | 6.087 | 6.252 | 5.249 | 5.559 |
| **Random init** | 5.910 | **6.164** ← 최선 | 4.631 | 4.948 |
| **Snapshot** | 7.105 | 7.235 | 5.218 | 5.501 |

- 🔎 **주목**: bootstrap 이 **에너지 RMSE 는 제일 나쁘면서 힘 RMSE 는 제일 좋다.** 저자도 *"the origin of
  this behavior is not investigated further"* 라고 **설명을 포기**한다. 네 방법 모두 DFT 기대 정확도 안이고
  서로 비슷하다는 것이 저자의 결론.

### 5.2 ★ ID 채점 지표 ① — 잔차-불확실도 패리티 (`Fig. 6`)
**우리가 이 논문에서 제일 필요로 하는 부분이다.** UQ 를 채점하는 **가장 기본 도식**:

- **축**: x = *weighted uncertainty* (σ, 손실함수와 같은 가중·무차원), y = *mean residual* (가중 절대오차).
  **양축 log**, `10⁻⁶ … 10⁻²` (figure-read).
- **격자**: 열 = 4개 앙상블, 행 = 4개 구조(monolayer / bilayer / graphite / diamond) → **4×4 = 16 패널**.
- **표시**: 반투명 산점(꼬리 보존) + **KDE 등고선**(고밀도 영역), 파랑 = 훈련 / 주황 = 테스트.
- **회색 삼각영역** = `σ > residual` = **underconfident(과소확신, 보수적)** 구역.
  ⇒ **대각선 아래(흰 영역)에 몰리면 overconfident** 다. σ 정의를 2σ 로 바꾸면 이 경계선이 수직 이동한다고 명시.
- **이상적 상태**: 점들이 **대각선 근처**에 — σ ≈ residual, 그리고 서로 상관.

**figure-read (Fig. 6 실제 확인)**
- Bootstrap 열: 구름이 **대각선을 따라 가장 길게 뻗어 있다**(상관 최고) — 그러나 monolayer·bilayer·graphite 에서
  구름 중심이 **회색 밖(흰 쪽)** 에 있다 ⇒ 상관은 좋은데 **과소산출**.
- Dropout / Random init / Snapshot 열: 구름이 **오른쪽으로 밀려** 회색 영역과 더 겹친다(더 보수적) 대신
  **세로로 퍼져** 대각선 상관이 약하다.
- diamond 행(맨 아래): 네 방법 모두 구름이 **거의 수직**(σ 는 좁은데 residual 이 2 decade 퍼짐) ⇒ **상관 붕괴**.
- monolayer 행에 `σ ≈ 10⁻²` 근처의 **떨어져 나온 작은 섬**이 네 방법 모두에 보인다 (원자수 2–32 의 소형 셀 꼬리로 추정 — 논문 미언급).
- 🔴 저자 판정: *"the distinction between sample distributions is **more pronounced across structure types
  than across ensemble models**"* ⇒ **어느 앙상블이냐보다 어느 구조냐가 더 크게 갈린다.**

### 5.3 ★★ ID 채점 지표 ②③ — Pearson 상관 + MAE vs 평균 σ (`Fig. 7`) — **의뢰문 §2 의 실제 수치**
`Fig. 7a` 는 **잔차와 불확실도의 Pearson 상관계수**를 히트맵 숫자로 인쇄한다. **테스트셋 기준.**

**figure-read (히트맵 인쇄 숫자 — 눈대중이 아니라 인쇄된 값)**

| 구조 \ 앙상블 | **Bootstrap** | Dropout | Random init | Snapshot |
|---|---|---|---|---|
| Monolayer | **0.74** | 0.31 | 0.34 | 0.33 |
| Bilayer | **0.81** | 0.47 | 0.63 | 0.62 |
| Graphite | **0.69** | 0.43 | 0.41 | 0.31 |
| Diamond | **0.77** | 0.40 | 0.38 | 0.37 |
| **All data** | **0.76** | 0.40 | 0.32 | 0.30 |

⇒ **Bootstrap 이 상관 지표에서 네 구조 전부·전체 데이터에서 1위** (0.69–0.81 vs 나머지 0.30–0.63).
전체 데이터 기준 **0.76 vs 0.30–0.40 — 약 2배**. 이것이 이 논문에서 **가장 또렷한 방법 간 차이**다.

`Fig. 7b` 는 **MAE(원)와 평균 σ(삼각형)를 같은 축에 겹쳐** 그린다 — 구조별 색(파랑 monolayer / 주황 bilayer /
빨강 graphite / 초록 diamond / 검정 all-data), 점선이 같은 구조의 MAE↔σ 쌍을 잇는다.
**σ 삼각형이 MAE 원보다 아래 = overconfident, 위 = 보수적.**

**figure-read ≈ (6배 확대해 눈금에서 읽음, ±10 % 정도로 보라)**

| 앙상블 | 에너지 MAE (meV/atom) | 에너지 평균 σ | 힘 MAE (meV/Å/atom) | 힘 평균 σ | 판정 |
|---|---|---|---|---|---|
| **Bootstrap** | ≈ 8–10 (all-data ≈ 9) | ≈ **6–7** (MAE 아래) | all-data ≈ **2.05**, monolayer **3.3**, graphite ≈1.85, bilayer ≈1.15 | all-data ≈ **0.65**, monolayer ≈ **1.15**, 나머지 ≈ 0.4–0.5 | 🔴 **힘에서 σ ≈ MAE의 1/3 — 명확한 과소확신(overconfident)** |
| **Dropout** | ≈ 5–8 | ≈ **13–18** (MAE 위) | monolayer **4.9**, diamond **4.4**, all **3.4**, graphite **2.7**, bilayer **1.7** | all ≈ **3.35**, graphite ≈ **2.4**, bilayer ≈ **2.0** | 🟢 **σ 가 MAE 를 넘거나 근접 — 가장 잘 보정됨** |
| **Random init** | ≈ 4–7 | all ≈ 16, monolayer ≈ 11, **diamond ≈ 49** ⚠ | monolayer **4.55**, diamond **3.83**, all **3.07**, graphite **2.5**, bilayer **1.6** | diamond **2.72**, monolayer **2.15**, all **1.75**, graphite **1.25**, bilayer **0.8** | 🟡 σ ≈ MAE 의 절반. **diamond 에너지 σ 만 이상치로 폭주** |
| **Snapshot** | ≈ 4–8 | all ≈ 18, 나머지 ≈ 9–11 | monolayer **4.85**, diamond **4.55**, all **3.4**, graphite **2.7**, bilayer **1.7** | diamond **2.9**, monolayer **2.2**, all **1.8**, graphite **1.2**, bilayer **0.85** | 🟡 **random init 과 거의 판박이** |

**⇒ 이 논문의 "복잡 vs 단순" 판정 — 세 갈래로 갈린다**

1. **상관 지표(Fig. 7a)로 채점하면 bootstrap 압승** (0.76 vs 0.30–0.40, 전 구조 일관).
2. **보정 지표(Fig. 7b)로 채점하면 bootstrap 패배** — *"the bootstrap ensemble often produces
   **overconfident** predictions, particularly for the force quantities"*, 반대로 dropout 은
   *"yields average uncertainties that either exceed or closely match the MAEs, suggesting
   **better-calibrated** uncertainty estimates"* ⇒ 저자는 **"dropout 을 bootstrap 보다 선호할 근거"** 라고 씀.
   🔴 **같은 데이터에서 두 지표가 우승자를 반대로 뽑는다. 이게 §11 로 가져갈 제일 중요한 사실이다.**
3. **비용 대비**: *"the random initialization and snapshot ensembles exhibit **very similar performance** …
   However, the snapshot ensemble is **significantly more computationally efficient because it requires
   training only a single model**."* ⇒ **훈련 100회짜리와 1회짜리가 성능이 같다.**

**그리고 저자 자신의 유보** (p12):
> *"the **overall differences in performance between the ensemble methods remain minimal** within this ID
> domain. Except for the bootstrap case, the correlations … are **generally weak** … **this analysis alone
> does not provide sufficient evidence to definitively identify the best-performing ensemble model.**"*

⇒ **"일관되게 이기지 못했다"의 이 논문판**은 이것이다: **ID 에서는 승자를 가릴 수 없다.**
**"일관되지 않은 구간"** 은 `Fig. 7a` bilayer 열 — dropout 0.47 < random init 0.63 ≈ snapshot 0.62 로
**다른 구조와 순위가 뒤집힌다**(다른 세 구조에서는 dropout ≥ random init).
그리고 `Fig. 7b` random-init **diamond 에너지 σ ≈ 49 meV/atom** 은 같은 열의 다른 구조(≈9–16)보다
**3–5배 튀는 유일한 이상치**다 — 논문 본문이 이 점을 언급하지 않는다.

### 5.4 왜 bootstrap 이 과소확신하는가 (저자 가설)
훈련 데이터가 **MD 궤적의 연속 스냅샷**이라 서로 독립이 아니다 → 특정 영역이 과대표집 →
**복원추출로도 훈련셋이 충분히 달라지지 않는다** → 앙상블 산포 과소 → 과소확신.
반면 dropout 은 **학습·추론 양쪽에서 확률적 마스킹**을 걸어 데이터 비독립성에 덜 민감하다.
⚠ 이건 **검증되지 않은 가설**이다 (저자가 "likely arises" 라고 씀).

### 5.5 ★ OOD 결과 — cold curve (`Fig. 8`)
**figure-read (실제 확인)** — 3행(위 graphene / 가운데 graphite / 아래 diamond) × 4열(앙상블).
검은 곡선 = 앙상블 평균, **회색 띠 = ±1σ**, 빨간 점 = DFT, 빨간 파선 = MP 평형 `a`, 검은 파선 = 예측 평형 `a`
(그 세로 회색 띠 = 평형 `a` 의 σ). y = `E/atom` **−7.4 … ≈ −8.1 eV/atom**.

- **graphene / graphite (x = 2.3–2.7 Å)**: 평형 근처는 DFT 점이 회색 띠 안 또는 곡선 위에 정확히 얹힌다.
  예측 `a_eq ≈ 2.46–2.47 Å` 로 MP 값과 **거의 겹친다**(세로 파선 두 개가 붙어 있음).
  ⚠ 양 끝(±10 %)에서 검은 곡선이 빨간 점을 벗어나기 시작하는데 **회색 띠는 거의 안 넓어진다.**
  특히 **bootstrap 열은 회색 띠가 사실상 보이지 않는다** — §5.3 의 과소확신이 눈으로 확인된다.
- **diamond (x = 3.3–3.9 Å)**: **여기서 전부 무너진다.**
  - **bootstrap**: 포물선 모양은 유지하나 **곡률이 DFT 보다 훨씬 크다**(양쪽에서 급격히 치솟음).
    예측 `a_eq ≈ 3.60 Å` vs MP `≈ 3.567 Å`.
  - **dropout / random init / snapshot**: **인장 쪽(a ≳ 3.65 Å)에서 에너지가 평탄해진다** —
    올라가야 할 곳에서 수평이 된다. **물리적으로 불가능한 모양**. 압축 쪽은 지나치게 가파르다.
    예측 `a_eq ≈ 3.63–3.65 Å` 이고 **평형 `a` 의 세로 회색 띠는 여기서만 뚜렷하게 넓다.**
  - 대부분의 DFT 점이 **회색 띠 밖**에 있다 ⇒ 저자 표현 *"the ensemble models are **confidently making
    incorrect predictions**"*.
- **phonon (SI)**: 본문 서술만 — graphene/graphite 는 *"most branches reproduced within the uncertainty
  bounds"*, **Γ점 근처 flexural optical mode 는 과소평가**. diamond 는 *"large deviations … underestimated
  optical branches and **noisy acoustic modes**"*, 그리고 *"the **wide** uncertainty bounds **fail to capture**
  the true values"*. ⚠ **수치 없음 — 우리가 인용할 숫자가 하나도 없다.**

### 5.6 ★ 왜 diamond 만 무너지나 — 특징공간 분석 (`Fig. 9`) = 이 논문의 OOD 진단
훈련셋 원자환경 기술자에 **PCA** 를 적합하고 상위 2개 주성분에 투영. **두 성분이 분산의 98 %** 를 설명
(특이값 제곱합 비율로 계산).

**figure-read (실제 확인)**
- 축은 `PC1`, `PC2` (**눈금 숫자 없음** — 정성적 그림).
- 훈련 클러스터: **diamond(빨강)가 왼쪽에 완전히 분리된 좁은 띠**, **graphite(파랑)+monolayer(주황)가
  오른쪽에서 겹쳐 있고**, bilayer(보라)는 **그 밑에 완전히 가려 안 보인다**(캡션이 명시).
- cold-curve 표본(삼각형): graphene/graphite 삼각형은 **클러스터 위를 지나가다가** 작은 `a` 쪽에서만
  **왼쪽 위로 튀어나간다**(`Small a` 화살표 2개).
- **diamond 삼각형은 빨간 클러스터의 가장자리를 스치고 지나갈 뿐 대부분 밖에 있다** ⇒ 저자 표현
  *"**minimal overlap** between the training data and the atomic environments involved in the cold curve"*.
- 오른쪽 막대: 특이값 스펙트럼 `10³ … 10⁻⁵` (log). 상위 2개가 나머지를 압도.

⇒ **"diamond 정확도 붕괴 = 외삽" 이라는 인과를 특징공간에서 뒷받침**한다.
⇒ **이 PCA 가 이 논문에서 실제로 작동한 유일한 OOD 탐지기다** (σ 가 아니라).

### 5.7 ★★★ 핵심 음성 결과 — **σ 가 외삽하면 오히려 줄어든다** (`Fig. 11`, `Fig. 13`)
`Fig. 11`: x = `a`, y = **에너지 오차(검은 곡선)와 불확실도(회색 띠)를 같은 축에** 놓았다.
**파란 띠 = `Fig. 9` 로 정한 내삽 영역(interpolation domain)**. 육방정계는 **±20 % 로 확장**(2.0–3.0 Å),
diamond 는 3.3–3.9 Å.

**figure-read (실제 확인)**
- **diamond 행(맨 아래)**: 네 방법 모두 **회색 띠가 전 구간 거의 일정하고 얇다(≈ ±0.02 eV/atom)** 인데
  검은 오차 곡선은 파란 띠 밖에서 **≈ 0.2–0.3 eV/atom** 까지 치솟는다 ⇒ **오차/σ ≈ 10배 이상**.
- **graphene/graphite 행**: 파란 띠 밖으로 나가면 오차가 즉시 축 밖(> 0.1)으로 나가는데,
  회색 띠는 **바로 바깥에서 한 번 부풀었다가 더 멀리 가면 다시 좁아진다** (dropout·snapshot 열에서 뚜렷).
  bootstrap 열은 회색 띠가 전 구간 얇다.

`Fig. 13` 이 이 현상을 **한 장에 정량으로** 보여준다 (bootstrap · graphene · **에너지 σ 절대값**):
- y = `Energy uncertainty (eV)` **0.00–0.05**, x = `a` **2.0–3.0 Å**, 파란 띠 = 내삽 영역 ≈ **2.37–2.61 Å**.
- **figure-read ≈**: 내삽 영역 안 **σ ≈ 0.004 eV** (최소) → 압축 쪽 경계 바로 밖 **`a ≈ 2.29 Å` 에서 σ ≈ 0.030 eV 로 최대**
  → **더 압축하면 도로 떨어져 `a = 2.0 Å` 에서 σ ≈ 0.0145 eV** (최댓값의 **절반 이하**).
  인장 쪽도 같은 모양: `a ≈ 2.74 Å` 에서 σ ≈ 0.0275 → `a = 3.0 Å` 에서 σ ≈ 0.0175 로 감소.
- ⇒ **σ 는 "훈련 경계 근처"에서 최대이고, 진짜 위험한 먼 외삽에서는 오히려 작아진다.**
  **σ 는 외삽 여부의 신호는 되지만 외삽 *거리*의 척도는 아니다.**

저자 표현(p16):
> *"While uncertainty **initially rises modestly** as the model begins to extrapolate … it does so at a
> **lower rate than the prediction error** and **eventually plateaus or even declines**, despite increasing
> inaccuracy."*
> *"models may exhibit **low uncertainty even while operating far beyond their training domain**. This
> situation is **inherently ambiguous**."*

### 5.8 가설 검증 시도와 그 실패 (`Fig. 13` 삽입 히스토그램)
**가설**: `tanh` 는 유계 함수라 먼 외삽에서 출력이 **포화**(±1) → 입력 민감도 상실 → σ 축소.
**검증**: 최종 활성함수 출력 분포를 세 `a` 에서 본다 (삽입 3개, x = −1…+1).
- `a = 2.0 Å`(먼 외삽): **±1 에 이봉으로 완전 포화** ✅ 가설과 일치
- `a = 2.3 Å`(σ 큰 곳): 분포가 **−1…+1 에 퍼져 있다** ✅ 가설과 일치
- `a = 2.5 Å`(**평형·훈련 영역 안**): **여기도 ±1 에 포화돼 있다** ❌ **반례**
⇒ 저자 결론: *"activation function saturation **alone does not fully explain**"*. **가설 기각은 아니고 미해결.**

**두 번째 가설**: 극단 외삽에서 앙상블이 **의미 있는 변동을 만들 정보 자체가 없어** 출력이 붕괴.
**세 번째**: **인식론적(epistemic) vs 우연적(aleatoric) 불확실도의 불일치** — 앙상블은 epistemic 만 잡는데
극단 외삽에서는 그 epistemic 조차 과소표현될 수 있다. **둘 다 검증하지 않았다.**

### 5.9 dropout 비율 스캔 (`Fig. 10`) — 유일한 "고칠 수 있나" 실험
diamond cold curve 를 `p = 0.1 … 0.8` 로 8개 패널. 각 패널 위 = 예측/DFT/σ, 아래 = **오차(파랑) vs σ(회색)**.

**figure-read (실제 확인)**
- `p` 가 커질수록 **회색 σ 띠가 넓어진다**(p=0.1 반폭 ≈ 0.01 → p=0.5–0.7 ≈ 0.03–0.05 eV/atom).
- **인장 쪽(a ≳ 3.6 Å)**: `p = 0.1–0.2` 에서 평탄한 비물리 곡선 → 오차가 **> 0.4 eV/atom** 로 축 밖.
  `p ≥ 0.3` 부터 **곡선이 제대로 올라가고 오차가 ≈ 0.02–0.05 로 급감**.
- **압축 쪽(a ≈ 3.4 Å)**: **`p` 를 아무리 올려도 오차 봉우리가 ≈ 0.20–0.30 eV/atom 로 거의 안 변한다.**
  (p=0.1 ≈0.30 → p=0.7 ≈0.20)
- 🔴 **`p = 0.8`**: 예측이 **완전 수평선**(학습 실패), 오차는 W 자로 양끝 **> 0.45**, 그런데
  **회색 σ 띠가 거의 0 으로 붕괴한다.** ⇒ **"학습 능력을 잃으면 앙상블 다양성도 사라져 σ 가 0 이 된다"** —
  최악의 모델이 최고의 확신을 준다. **이 논문에서 가장 무서운 그림이다.**

저자 결론: dropout 비율 조정은 **정확도 개선 수단이 아니다**(인장 개선은 *"incidental rather than systematic"*,
압축은 반례). **과소확신 완화**에는 효과 있음. **최적 `p` 에 대한 보편 지침은 없다**(선행 연구의 ~50 % 는 경험칙).
향후 과제로 *"큰 dropout 을 견디는 더 넓고/깊은 망"* 을 제안.

### 5.10 아키텍처 일반성 — SchNet (`Fig. 12`)
같은 데이터로 SchNet(GNN)을 4,000 epoch 학습(ID 오차를 NNIP 수준에 맞춤).
**figure-read (실제 확인 · 워터마크가 diamond 패널을 상당히 가린다)**
- `Fig. 12a` PCA(그래프 표현): **diamond(빨강)가 오른쪽에 완전 분리**, graphite/monolayer/**bilayer(보라)가
  왼쪽에서 뭉쳐 있다**(NNIP-ACSF 의 `Fig. 9` 와 클러스터 배치가 다르다 — 표현이 다르니 당연).
  diamond cold-curve 삼각형이 **클러스터 밖 오른쪽 위로 길게 뻗는다** = 외삽.
- `Fig. 12b` graphene: σ 띠가 `a ≈ 2.0` 에서 ≈ ±0.09 로 넓지만 오차는 축 밖(> 0.10) ⇒ **여전히 과소확신**.
  `a ≈ 2.2–2.4` 에서 σ 가 ≈ ±0.01 로 좁아졌다가 인장 쪽에서 다시 넓어짐.
- graphite/diamond: 오차 곡선이 내삽 영역 안에서도 **요동**(diamond 는 파란 띠 안에서도 0.03–0.10 사이 진동).
⇒ 저자: *"**not specific to a particular model architecture**"*. ⚠ 단 *"do not imply a general rule"* 이라고 유보.

---

## 6. 평가 지표 총정리 ★★ (의뢰문 §3 — **우리가 제일 필요로 하는 절**)

**이 논문이 실제로 쓴 지표는 딱 다섯 가지다. 그 이상은 없다.**

| # | 지표 | 무엇을 계산하나 | 필요한 것 | 그림 | 무엇을 잡나 / 못 잡나 |
|---|---|---|---|---|---|
| **M1** | **잔차–σ 패리티 산점 (log-log) + KDE + "underconfident" 삼각 음영** | y = |오차|, x = σ, 대각선 = 완벽 보정 | **DFT 라벨 필요** | `Fig. 6` | 상관·보정을 **동시에** 눈으로. 스칼라가 아니라 요약이 안 된다 |
| **M2** | **Pearson 상관 `corr(residual, σ)`** | 테스트셋 전체 + 구조별 | **DFT 라벨 필요** | `Fig. 7a` | 🟢 **"σ 가 오차를 순서대로 맞추나"**. ⛔ **스케일을 안 본다** — σ 를 10배 부풀려도 상관은 그대로 |
| **M3** | **MAE vs 평균 σ 병렬 플롯** | 같은 축에 `MAE` 와 `⟨σ⟩` 를 겹침 | **DFT 라벨 필요** | `Fig. 7b` | 🟢 **"σ 의 크기가 오차 크기와 맞나"(보정)**. ⛔ **순서를 안 본다** — 평균만 맞으면 통과 |
| **M4** | **OOD 포함 여부** — DFT 참값이 ±1σ 띠 안에 드나 | cold curve·phonon 전 구간 | **DFT/참값 필요** | `Fig. 8`, SI | coverage 의 **정성판**. ⚠ **coverage 확률을 수치화하지 않았다** |
| **M5** | ★ **오차 곡선 vs σ 곡선을 외삽 좌표에 함께 그림** + **PCA 로 정한 내삽 영역 음영** | x = 외삽 좌표(`a`), y = 오차와 σ 동시 | **DFT + 훈련셋 기술자 필요** | `Fig. 11`, `Fig. 13`, `Fig. 12b` | 🟢🟢 **이 논문의 발명품.** "σ 가 외삽 거리를 따라가나" 를 본다. **M2·M3 이 통과해도 여기서 떨어진다** |

**⛔ 이 논문에 *없는* 지표 (전문 검색으로 확인)**
`NLL`/negative log-likelihood **0회** · `sharpness` **0회** · `conformal` **0회** · `calibration curve`/
`reliability diagram` **0회** · `AUROC`/`AUC` **0회** · `expected calibration error`/`ECE` **0회** ·
`miscalibration area` **0회** · `spearman` **0회** · `AUROC`/`AUC` **0회** ·
`coverage` 는 3회뿐이고 **신뢰구간 coverage 가 아니다** — 2회는 *"training data coverage"*(`Fig. 9`·`Fig. 12a`),
1회는 epistemic 불확실도 정의의 *"limited data coverage"*.
(참고로 계 자체도 순수 탄소다: `battery`·`lithium`·`sulfide` **각 0회**, `Li` 는 **참고문헌 저자 성으로만 4회**.)
그리고 **사후 보정을 의도적으로 안 했다** (§3 공통규약).

> 💡 **우리에게 주는 실무 결론**: 지표를 **두 개 이상** 써야 한다.
> **M2(순서) 와 M3(크기) 는 다른 것을 재고, 이 논문에서 실제로 우승자를 반대로 뽑았다.**
> 그리고 우리 용도(외삽 감시)에는 **M5 가 본체**다.

---

## 7. 비용 대비 성능 ★ (의뢰문 §5)

⚠ **먼저 정직하게**: 이 논문은 **벽시계 시간·GPU 시간·FLOP 을 하나도 보고하지 않는다.**
`wall-clock` 0회 · `GPU` 0회 · 시간 단위 벤치마크 표 없음. **비용 논의는 전부 정성적**이다.

| 추정기 | **학습 비용** | **추론 비용** | 성능(§5.3) | 저자의 명시 |
|---|---|---|---|---|
| **Bootstrap** | **× 100** (독립 학습 100회) | × 100 (100모델 평가) | 상관 최고(0.76) / **보정 최악(힘 σ ≈ MAE/3)** | — |
| **Random init** | **× 100** | × 100 | 상관 0.32 / 보정 중간 | *"primary drawback … is **computational cost since each model must be trained independently**"* |
| **Snapshot** | **× 1** ★ | × 100 (스냅샷 100개 평가) | **random init 과 사실상 동일** | *"**significantly more computationally efficient because it requires training only a single model**"* |
| **Dropout** | **× 1** ★ | × 100 (마스크 100개) | 상관 0.40 / **보정 최고** | 저장공간도 1모델분 |

**⇒ 이 논문이 실제로 제공하는 비용 결론 두 줄**
1. **`snapshot ≈ random init` 인데 학습은 100분의 1** ⇒ **훈련 100회짜리를 쓸 이유가 이 데이터에서는 없었다.**
2. **추론 비용은 네 방법이 전부 같다** (S = 100회 평가). ⇒ **MD 에 붙이면 어느 쪽이든 100배**다.
   ⚠ 논문은 **앙상블 크기를 줄였을 때 지표가 얼마나 나빠지는지 (S 스윕) 를 하지 않았다** — 우리에겐 그게 진짜 비용 질문인데 답이 없다.

---

## 8. Post-processing ★

- **무엇**: ① **energy cold curve (EOS 형)** — `E(a)`, 평형 `a` 와 응집에너지, 곡률(탄성 정보).
  ② **phonon dispersion** — 힘상수(Hessian) → 동역학행렬 고유값. ③ **PCA / SVD 특징공간 분석**.
  ④ 앙상블 통계(평균·표준편차) 전파.
- **도구**: **KLIFF**(학습 + UQ 앙상블 생성 · 이 논문이 bootstrap 을 여기에 추가) / **KIM-API** /
  **ASE**(포논 유한차분 `ase.phonons`, cold curve) / **OpenKIM** 검증 파이프라인 / **Materials Project**(기준 격자상수) /
  LAMMPS(호환성 언급). ⚠ **pymatgen·phonopy·LOBSTER 등은 안 쓴다.**
- **수치화·기록**: σ 는 **앙상블 표준편차 그대로**(무보정). 상관은 Pearson. 오차는 MAE(에너지·힘 분리) 와
  RMSE(Table 2). 그림에서 **σ 를 "회색 띠"로, 오차를 "검은/파란 곡선"으로** 같은 축에 놓는 것이 이 논문의
  일관된 표기 관례다.
- **재현성**: 코드+데이터 **GitHub 공개** (`yonatank93/compare_UQ`) — ⚠ 우리가 내려받아 확인하지 않았다.

---

## 9. Figure set ★

> 🖼 크로핑: `litdb/figures/kurniawan2025_comparative_ensemble_uq_nnip/` — **본문 그림 11 + 표 2 = 13장 추출.**
> ⚠ **`Fig. 3`(앙상블 4종 모식도)과 `Fig. 5`(손실 궤적)는 추출 실패** — 도구의 기하검증에서
> `f3 = 영역 없음`, `f5 = 그래픽 없음(img0/draw5)` 로 걸러졌다. 두 그림 다 본문 서술이 충분해 손실은 작다.
> ⚠ SI 그림(포논 전체·육방정계 dropout 스캔)은 **SI PDF 를 우리가 안 갖고 있어 0장**이다.

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | 다트판 비유 — 정확도(과녁 근접) × 정밀도(산포) 2×2. "정밀한데 틀린" 좌하 칸이 이 논문의 표적 | 🟡 개념도. **발표 슬라이드에 그대로 쓸 수 있는 프레이밍** (우리 UQ 절 도입부) |
| 2 | NNIP = MLP 그래프 표현 (입력층/은닉층/출력층, `y_l^α`, `w_l^{α,β}`) | ⛔ 일반 교과서 그림 — 우리 활용 없음 |
| 3 | (⚠ 크로핑 실패) 앙상블 4종 모식도: (a) bootstrap 복원추출 (b) dropout 마스크 (c) 랜덤 초기화 (d) 훈련 궤적 스냅샷 | 🟢 **§3 표의 그림판** — 우리 UQ 설계 문서에 옮길 분류 체계 |
| 4 | 탄소 3종 결정구조 (diamond 사면체, graphene 육방, graphite ABAB + `c/2`) | ⛔ 활용 없음 |
| 5 | (⚠ 크로핑 실패) 훈련/테스트 손실 궤적 — 과적합 없음 | 🟡 "과적합 아님"의 근거일 뿐 |
| 6 | ★ **잔차 vs σ 패리티 4×4 (log-log, KDE 등고, 회색=underconfident)**. 구조 차이 > 방법 차이 | 🟢🟢 **지표 M1. 우리 committee 진단 그림의 템플릿 — 이 도식을 그대로 복제한다** |
| 7a | ★★ **Pearson 상관 히트맵** — bootstrap 0.69–0.81 vs 나머지 0.30–0.63, all-data **0.76 vs 0.30–0.40** | 🟢🟢 **지표 M2 + 의뢰문 §2 의 실제 수치. "복잡 vs 단순" 판정의 정량 근거** |
| 7b | ★★ **MAE(원) vs 평균 σ(삼각) 병렬** — bootstrap 힘 σ ≈ MAE/3(과소확신), dropout σ ≥ MAE(보수적) | 🟢🟢 **지표 M3. M2 와 우승자가 반대로 나온다는 사실 자체가 우리 결론** |
| 8 | ★ cold curve 3구조 × 4방법, ±1σ 회색 띠 + DFT 점 + 예측/참조 평형 `a`. diamond 인장에서 **에너지 평탄화**(비물리) | 🟢 **지표 M4. "OOD 프로브를 값싸게 만드는 법"의 실물 예 — 우리 LPSCl 판은 §11-D** |
| 9 | ★★ **PCA 특징공간** — 훈련 클러스터 vs cold-curve 표본. 상위 2 PC 가 **분산 98 %**. diamond 는 **겹침 최소** | 🟢🟢 **σ 없이 작동한 유일한 OOD 탐지기. 우리가 단일 UMA 로도 할 수 있는 것** |
| 10 | ★ dropout `p = 0.1…0.8` 스캔(diamond). `p↑` → σ 띠 확대·인장 개선, **압축은 무변화**, **`p=0.8` 에서 예측 수평선 + σ 붕괴** | 🟢 **"UQ 하이퍼파라미터를 정확도 개선에 쓰지 말라"의 근거. `p=0.8` 패널은 발표용 경고 그림** |
| 11 | ★★★ **오차 곡선 vs σ 띠를 외삽 좌표에 함께** + **파란 내삽 영역**. diamond 는 오차 0.2–0.3 인데 σ ≈ ±0.02 | 🟢🟢🟢 **지표 M5 = 이 논문의 발명품. 우리 committee 검증의 목표 그림** |
| 12 | SchNet(GNN) 재현 — (a) 그래프 표현 PCA (b) 오차/σ. 같은 병리 반복 | 🟢 **아키텍처 일반성 근거 — UMA(등변 GNN)로의 전이 가능성 논거로 인용 가능(단 §14)** |
| 13 | ★★ bootstrap graphene **σ 절대값 곡선**: 내삽 0.004 → 경계밖 0.030(최대) → 먼 외삽 0.0145 eV. 삽입 = tanh 출력 히스토그램(포화 가설과 그 반례) | 🟢🟢 **"σ 감소"의 유일한 정량 그림. 우리가 인용할 숫자는 여기서 나온다** |
| Table 1 | 데이터셋 구성 수 (총 4,788) | 🟡 규모 감각 — **우리 committee 표본 200프레임과 자릿수 비교** |
| Table 2 | ID RMSE — bootstrap 이 E 최악·F 최선 (미설명) | 🟡 인용 가능. 우리 UMA Li₃PS₄ 힘 MAE 30.0 meV/Å 와 **단위는 같지만 계·라벨이 달라 비교 금지** |

---

## 10. 저자가 적은 한계 ★ (의뢰문 §6)

논문이 **스스로** 인정한 것들 — 원문 위치까지:

1. **아키텍처 범위** (Conclusion): *"while the present analysis focuses on **NNIP architecture**, extending
   this study to a **broader range of MLIP architectures** remains an important direction for future work."*
   (SchNet 확인이 있지만 *"do not imply a general rule"*.)
2. **원인 설명 실패** (§4.3, Conclusion): 활성함수 포화 가설과 epistemic/aleatoric 불일치 가설 **둘 다
   결정적이지 않다**. 포화 가설은 **평형점에서 반례**가 나왔다. *"further investigation … is necessary"*.
3. **이론 부재** (마지막 문단, 가장 센 문장):
   > *"in the **absence of a coherent theory of learning** for NN models, it remains difficult to fully explain
   > or resolve the behavior of uncertainty estimates … their uncertainty estimates should be treated with
   > **skepticism**, especially in high-stakes or extrapolative scenarios."*
4. **bootstrap 의 i.i.d. 가정 위반** (§2.3.1): 구성 단위 재샘플링으로도
   *"does not fully eliminate correlation-related biases if the configurations themselves are not
   independent, for instance, when they are **sequential snapshots from a single MD trajectory**"* ⇒ 과소확신.
5. **dropout 비율에 보편 지침 없음** (§4.2): *"the choice remains **largely empirical**"*; 정확도 개선 효과는
   *"**incidental** rather than systematic"* 이며 압축 영역에서 **반례**가 있다.
6. **내삽/외삽 경계가 모호** (§4.3): *"the boundary … is often **subtle and difficult to delineate** in
   high-dimensional feature spaces"*.
7. **사후 보정으로도 안 풀린다** (§4.3, ref [67] 인용): *"Post-hoc calibration may improve the numerical
   interpretation … but it **does not necessarily resolve this ambiguity under distribution shift**."*
8. **에너지-힘 RMSE 역전 미설명** (§3.1): bootstrap 이 E 최악·F 최선인 이유를
   *"the origin of this behavior is **not investigated further** in the present work"*.
9. **연구 목적 자체의 한정** (§1): *"our goal is **not to propose methods for mitigating**"* — 처방이 없다.

**우리가 추가로 지적하는 한계 → §14.**

---

## 11. ★★ 우리 좌표 — UMA 단일 파운데이션 모델에서 이 논문을 어떻게 쓰나

### 11-A. 단일 모델(훈련 1회)로 가능한 것은 무엇인가 — **의뢰문의 핵심 질문**

> **네 추정기를 "우리가 UMA 로 할 수 있나"로 다시 정렬한다.**

| 추정기 | 필요 학습 | **UMA 단일 모델로 가능?** | 판정 근거 |
|---|---|---|---|
| **Bootstrap** | 100회 | ⛔ **불가** | OMat24 훈련셋을 우리가 갖고 있지 않다. 재샘플링할 원본이 없다 |
| **Random init** | 100회 | ⛔ **불가** | 파운데이션 모델을 100번 처음부터 학습 = 우리 자원 밖 |
| **MC Dropout** | **1회** | 🟡 **원리상 가능하나 이 논문 조건과 다르다** | 이 논문은 **dropout `p=0.1` 로 학습된 망**에 추론 시 마스크를 건다. **UMA 는 dropout 으로 정칙화돼 학습되지 않았다**(우리가 확인한 바 없음 = n/a). 학습 때 안 본 마스크를 추론에 걸면 그건 UQ 가 아니라 **모델 훼손**이다. ⚠ 게다가 `Fig. 10` 이 보여주듯 **`p` 를 잘못 잡으면 σ 가 0 으로 붕괴**한다 |
| **Snapshot** | **1회** ★ | 🟢 **여기가 답이다 — 단, "학습 1회"가 있어야 한다** | UMA 사전학습 궤적은 우리에게 없다. **그러나 우리가 UMA 를 fine-tune 하는 순간(LoRA/bespoke, PET-MAD 편이 그 경로를 이미 보여줬다) 스냅샷 앙상블은 공짜로 딸려 온다** — fine-tune 중 100 step 간격으로 체크포인트를 저장하기만 하면 된다. 그리고 이 논문의 결론이 **snapshot ≈ random init** 이다 ⇒ **싼 쪽이 나쁘지 않다** |
| **(비앙상블) PCA 특징공간** | **0회** ★★ | 🟢🟢 **지금 당장 가능** | `Fig. 9`·`Fig. 12a` 의 방법은 **모델이 하나여도 된다.** 훈련셋 대신 **우리가 정의한 참조 집합**(예: 300 K 평형 궤적)의 UMA 임베딩/기술자에 PCA 를 적합하고, 고온·계면·결함 프레임을 투영해 **"내삽 영역 밖인가"** 를 본다. ⚠ **OMat24 커버리지를 재는 것이 아니다** — 우리 참조 집합 대비 상대적 외삽일 뿐. 이 한계를 명시해야 한다 |

**⇒ 한 줄 답**: **단일 UMA 로 "지금 당장" 되는 것은 PCA 특징공간 외삽 진단(§5.6)이고,
"fine-tune 을 하게 되면" snapshot 앙상블이 사실상 공짜로 붙는다. dropout 은 조건이 안 맞고, bootstrap·
random-init 은 훈련셋이 없어 불가능하다.**

### 11-B. 우리 `mlip_committee.py force_contrast` / `analyze` 는 이 논문의 어느 부류인가

우리 도구는 **두 개의 서로 다른 것**을 잰다. 이 논문의 좌표계에 놓으면 **정확히 두 축으로 갈린다.**

| 우리 도구 | 무엇을 재나 | 이 논문 좌표 | 채점 가능한 지표 |
|---|---|---|---|
| **`analyze`** (UMA / MACE-MP-0 / SevenNet-0 3종, 프레임별 원자당 힘 RMS 불일치의 **쌍별 최댓값**, 평균 힘 크기로 정규화) | **σ (불확실도)** | **`Fig. 6`·`Fig. 7` 의 x축 = weighted uncertainty**. 분류상 **committee disagreement** = ③ random initialization 의 **일반화판**(변동 출처가 seed 가 아니라 **아키텍처 + 훈련셋**). ⚠ **이 논문에 정확히 대응하는 항목은 없다** — 이 논문은 네 방법 모두 **같은 아키텍처·같은 데이터**를 쓴다 | — (혼자서는 채점 불가) |
| **`force_contrast`** (UMA vs **DFT 라벨**, 골격 원자 `dF_frame`, 상대 `dF/F_ref`, `cos θ`) | **잔차 (정확도)** | **`Fig. 6`·`Fig. 7` 의 y축 = residual / MAE** | — (혼자서는 채점 불가) |

> 🟢🟢 **여기가 이 digest 의 실무적 최대 소득이다.**
> **우리는 두 축을 다 갖고 있는데, 한 번도 같은 프레임 위에 겹쳐 놓은 적이 없다.**
> **같은 스냅샷 집합**에 `analyze`(σ)와 `force_contrast`(잔차)를 돌리면 **`Fig. 6` 을 우리 계로 그대로 그릴 수 있고**,
> 거기서 **M1·M2·M3 세 지표가 전부 나온다**:
> - **M1**: 프레임별 `(σ_committee, dF_frame)` 산점 log-log + 대각선 + underconfident 삼각영역
> - **M2**: `Pearson(dF_frame, σ_committee)` — **이 논문의 0.76 / 0.30–0.40 이 우리 값의 눈금이 된다**
> - **M3**: `mean(dF_frame)` vs `mean(σ_committee)` — 우리 committee 가 과소확신인지 보수적인지
> - **M5**: x 를 **온도**(600/800/1000 K) 또는 PCA 외삽 거리로 놓고 두 곡선을 겹침
>   → *"σ 가 온도 상승(=외삽 증가)을 따라가는가"* ⇒ **`Fig. 11` 의 우리 판**
>
> ⚠ **선결 조건**: `force_contrast` 는 **DFT 라벨이 필요**하다. 지금 우리에게 라벨 있는 데이터는
> **PET-MAD 배포 Li₃PS₄ test 243구조(PBEsol)** 와 **b2o3 힘 대조 카드**의 프레임뿐이고,
> **Cl 이 없다**(`comparison_vs_ours.md` §J-1 의 4번째 한계 그대로). ⇒ **아르지로다이트에서 이 그림을
> 그리려면 DFT 라벨을 새로 만들어야 한다.** 그건 새 계산이므로 **보고량 카드가 먼저다.**

**⚠ 우리 committee 에만 있는 함정 — 이 논문이 안 다룬 것**
`mlip_committee.py` docstring 이 이미 경고하는 그것: **MACE-MP-0 과 SevenNet-0 은 둘 다 MPtrj, UMA 만 OMat24** 라
불일치가 *"UMA 가 이상하다"* 가 아니라 *"저 둘이 무르다"* 일 수 있다.
이 논문의 네 앙상블은 **전부 같은 데이터·같은 구조**라 이 편향이 원천적으로 없다.
⇒ **이 논문의 σ 해석을 우리 이종 committee 에 그대로 옮기면 안 된다.** 우리 σ 는 **epistemic 불확실도 +
훈련셋 계통차**의 혼합이다. 이 논문에는 그 항이 없다.

### 11-C. ⚠⚠ **보고량 간극 — 이 논문은 힘·에너지에서 멈춘다** (의뢰문이 지적한 그것, 확인됨)

| 층위 | 이 논문의 보고량 | 우리 보고량 |
|---|---|---|
| ① 원자 단위 | 구성별 **에너지 · 원자력**의 residual/σ (`Fig. 6`, `Fig. 7`) | (있음: `force_contrast`, `analyze`) |
| ② 0 K 유도량 | **cold curve `E(a)`, 평형 `a`, phonon `ω(q)`** — 각 앙상블 멤버가 하나씩 내고 그 산포가 σ (`Fig. 8`, SI) | (없음 — 우리는 이 층위를 안 쓴다) |
| ③ **궤적 시간평균** | ⛔ **없다.** MD 를 한 번도 돌리지 않는다 | ★ **`D` (MSD 2–50 ps 창) → Arrhenius `Ea` → NE `σ_ionic`** |

**⇒ 명시적 간극 선언**:
이 논문은 **σ 를 궤적 평균 관측량으로 전파하는 방법도, 그 전파가 유효한지도 다루지 않는다.**
`Fig. 8`·phonon 은 **결정론적 0 K 유도량**이라 "멤버마다 한 번씩 계산해 산포를 본다"가 자명하지만,
**`D` 는 각 멤버가 *다른 궤적*을 만들고 그 위에서 시간평균을 취해야 하므로 비용·정의가 전혀 다르다.**
(멤버당 200 ps × 3온도 × 3시드 = **앙상블 100개면 900배**. 이 논문은 그 문제를 인지조차 하지 않는다.)
🔗 **그 층위는 `imbalzano2021_committee_uq_md_thermodynamic_averages` 편이 덮는다** — 같은 인입 배치의 자매 논문.
**우리 D·Ea 의 오차막대 논의는 그쪽으로 넘긴다. 이 논문에서 D 에 관한 어떤 수치도 가져오지 않는다.**

⚠ 다만 **부분적 다리 하나**는 있다: **phonon dispersion 은 "여러 원자의 집단 응답"이라 힘보다 한 층 위**이고,
거기서 이미 *"wide uncertainty bounds **fail to capture** the true values"* (diamond) 라는 실패가 나왔다.
⇒ **"힘 수준 σ 가 괜찮아도 유도량 수준에서 깨질 수 있다"** 는 방향은 이 논문이 이미 보여준다.
이건 **우리 D 에 대한 경고로 인용 가능**하다 — **단 "경고"까지이고 "정량"은 아니다.**

### 11-D. 우리 계로 옮길 수 있는 OOD 프로브 설계 (T2 후보, 새 계산 필요)
이 논문의 cold curve 는 **싸고, 훈련 밖이고, 참값을 쉽게 얻을 수 있는** 프로브라는 점에서 영리하다.
LPSCl 판을 만든다면:
- **등방 격자상수 스캔 `E(a)`** — comp1 셀을 ±10 % 스캔, UMA vs DFT(PBE, 우리 표준 설정).
  훈련 밖 여부는 **PCA 로 별도 확인**(§11-A).
- ⚠ **그대로 옮기면 안 되는 이유**: 아르지로다이트는 **무질서계**라 `E(a)` 가 **배열마다 다르다**.
  단일 배열로 그리면 그 곡선이 "모델 오차"인지 "배열 선택"인지 안 갈린다.
  ⇒ **보고량 카드에서 배열 선택·집계 규칙을 먼저 선언해야 한다** (CLAUDE.md 계산규율 그대로).
- ⚠ 그리고 **우리의 진짜 외삽 위험은 부피가 아니다** — 고온 무질서·Li 도약 안장점·계면이다.
  **부피 스캔은 우리 위험을 대표하지 않는다.** 이 논문의 프로브 선택을 그대로 베끼면 안 된다.

---

## 12. 적용 인사이트 (우리 연구에 어떻게)

1. **★ 지표를 두 개 이상 쓴다 — 하나면 우승자가 바뀐다.**
   `Fig. 7a`(순서, Pearson)와 `Fig. 7b`(크기, MAE vs ⟨σ⟩)가 **같은 데이터에서 반대 결론**을 냈다
   (bootstrap 0.76 최고 ↔ 힘 σ ≈ MAE/3 최악). 우리가 committee 를 채점할 때 **Pearson 하나만 보고
   "우리 σ 는 쓸 만하다"고 쓰면 그건 이 논문이 이미 반증한 종류의 주장**이다.
2. **★★ `analyze` × `force_contrast` 를 같은 프레임에 겹쳐 우리 `Fig. 6` 을 만든다.**
   추가 도구 없이(코드규율 사다리 ③: 기존 도구에 플래그) 두 산출 JSON 을 프레임 키로 조인하면 된다.
   **선결 조건은 Cl 포함 DFT 라벨이고, 그건 새 계산 → 보고량 카드부터.**
3. **★★ σ 는 "외삽했다"의 신호일 뿐 "얼마나 외삽했다"의 척도가 아니다** (`Fig. 13`: 0.004 → 0.030 → **0.0145**).
   ⇒ **우리 committee 불일치가 고온에서 안 커진다고 해서 "1000 K 도 안전하다"고 읽으면 안 된다.**
   `comparison_vs_ours.md` §J-2 의 **[Zhang npj] 1050 K 골격 융해 경고**와 **같은 방향**이고, 이 논문은
   *"불일치 지표 자체가 그 위험을 못 잡을 수 있다"* 는 한 겹 더 나쁜 소식을 얹는다.
4. **★ PCA 외삽 진단은 지금 당장, DFT 0회, 단일 UMA 로 된다.** 우리 600/800/1000 K 궤적 프레임을
   300 K 평형 프레임 기준 PCA 에 투영해 **"고온 프레임이 저온 클러스터 밖으로 나가는가"** 를 본다.
   ⚠ **참조 집합이 OMat24 가 아니라 우리 궤적이라는 것을 반드시 밝혀야 한다.**
5. **★ fine-tune 을 하게 되면 체크포인트를 버리지 않는다.** snapshot 앙상블은 **학습 1회로 얻는 UQ** 이고,
   이 논문에서 **훈련 100회짜리와 성능이 같았다**. 지금은 fine-tune 계획이 없지만, 하는 날
   *"100 epoch 간격 체크포인트 저장"* 한 줄이 UQ 를 통째로 준다.
6. **⚠ 유도량에서 깨진다는 방향은 인용하되 수치는 안 가져온다.** diamond phonon 에서 *"wide uncertainty
   bounds fail to capture the true values"* 는 **우리 D 에 대한 정성적 경고**로 쓸 수 있다.
   정량은 imbalzano 편.
7. **⚠ `p = 0.8` 패널(`Fig. 10`)은 발표용으로 값지다**: **모델이 학습에 실패하면 σ 도 0 이 된다.**
   *"UQ 는 모델이 망가진 것을 못 알려준다"* 의 가장 깨끗한 실물 증거.

---

## 13. 인용 가능 문장 (deck / paper 용)

- "Ensemble spread is a usable proxy for error **in-distribution**, but Kurniawan et al. (MLST 2026) show it
  **plateaus or even declines** once a neural-network potential extrapolates, so low uncertainty far from the
  training domain must not be read as reliability."
- "In a controlled comparison of four ensemble constructions (bootstrap / MC-dropout / random-initialization /
  snapshot, 100 members each) on carbon allotropes, **no single method won on both metrics**: bootstrap gave
  the highest residual–uncertainty correlation (**0.76** on all data vs 0.30–0.40 for the others) yet was the
  **most overconfident** on forces, while dropout was the best calibrated but only weakly correlated."
- "**Snapshot ensembles matched random-initialization ensembles** while requiring **training only a single
  model**, indicating that ensemble cost can be reduced by two orders of magnitude without a measured loss in
  UQ quality (Kurniawan et al., MLST 2026)."
- "Feature-space (PCA) analysis, not the ensemble spread, was what actually identified the extrapolative
  regime responsible for the largest errors."
- ⛔ **쓰면 안 되는 문장**: *"이 논문이 committee 가 제일 낫다고 했다"* (아님 — 승자를 못 정했다),
  *"이 논문이 GP/conformal 과 비교했다"* (아님 — 앙상블 4종만),
  *"이 논문이 D/이온전도도 UQ 를 다뤘다"* (아님 — MD 를 안 돌린다).

---

## 14. 주의 / 한계 — **우리 시각의 비판** (over-claim 방지)

1. **🔴 계가 탄소 단일원소다.** 다원소·이온성·무질서계(우리 LPSCl)로의 전이는 **시험된 적 없다.**
   특히 **부분점유 무질서**가 만드는 배열 앙상블은 이 논문의 어떤 축에도 없다.
2. **🔴 훈련셋이 4,788구성으로 작고 좁다.** 파운데이션 모델(OMat24 수천만 구조)의 **내삽 영역은 비교가
   안 되게 넓다** ⇒ **"외삽에 얼마나 자주 들어가는가"는 완전히 다르다.** 이 논문의 메커니즘(외삽하면 σ 가
   먹통)은 전이 가능성이 있지만, **빈도·문턱은 전이되지 않는다.** 우리 계로 옮길 때 이걸 안 밝히면 과장이다.
3. **⚠ "테스트셋 손실 최저 epoch 으로 모델 선택" + "그 테스트셋으로 채점"** — §2.2 가 검증셋을 없앤 대신
   **테스트셋을 모델 선택에 썼다**고 명시한다. ⇒ **`Table 2`·`Fig. 6`·`Fig. 7` 의 테스트 성능은 낙관 편향**이
   들어 있다. 저자는 "구조를 고정해 하이퍼파라미터 탐색이 불필요했다"고 방어하지만 **epoch 선택도 선택이다.**
   ⚠ snapshot 앙상블은 정의상 궤적 전체를 쓰므로 이 편향의 크기가 방법마다 다를 수 있고, **그 비대칭을
   논문이 검토하지 않았다.**
4. **⚠ 사후 보정을 일부러 뺐다.** 설계 의도는 이해되지만, 실무에서는 보정을 하고 쓴다.
   ⇒ **"보정하면 얼마나 나아지는가"에 이 논문은 답을 안 한다** (ref [67] 을 근거로 *"보정으로도 분포이동은
   안 풀린다"* 고 말할 뿐, **직접 실험하지 않았다**).
5. **⚠ 앙상블 크기 S = 100 고정.** `S = 5, 10, 20` 에서 지표가 어떻게 되는지 **스윕이 없다.**
   실무에서 100 멤버 MD 는 불가능하므로 **가장 실용적인 질문에 답이 없다.**
6. **⚠ 통계적 유의성이 없다.** `Fig. 7a` 의 0.31 vs 0.34 vs 0.33 같은 차이에 **오차막대가 없고**,
   앙상블을 **한 번씩만** 만들었다(bootstrap 앙상블을 여러 번 재생성한 산포 없음).
   ⇒ **0.30 과 0.40 의 차이가 실재하는지 이 데이터로는 말할 수 없다.** 반면 **0.76 vs 0.30–0.40 은
   충분히 크다** — 우리가 인용할 때 이 구분을 지켜야 한다.
7. **⚠ OOD 프로브가 사실상 "부피 스캔" 한 축뿐이다.** 등방 변형은 **가장 매끄럽고 저차원인** 외삽 방향이다.
   화학적 OOD(새 원소·결함·계면), 동역학적 OOD(안장점·고온)는 **안 건드렸다.**
   phonon 도 결국 같은 평형 구조 주변의 2차 미분이다.
8. **⚠ `Fig. 12`(SchNet) 는 앙상블이 하나뿐**이다 — 어떤 앙상블 구성인지 캡션·본문에 **명시가 없다**
   (문맥상 bootstrap 또는 random init 추정, **확인 불가**). ⇒ *"GNN 에서도 재현됐다"* 를
   **네 방법 전부에 대해** 주장할 근거는 없다.
9. **⚠ 포논 결과가 전부 SI 에 있고 우리는 SI 를 안 갖고 있다.** 본문 서술만으로 인용하면
   **숫자 없는 인용**이 된다. 필요하면 SI 를 받아야 한다.
10. **⚠ Eq. (8) 의 분모가 조판에서 깨져 있다** (`S−1` 인지 `S` 인지). σ 정의의 편향 보정 여부를
    표지에서 확정할 수 없다 — 100 멤버라 실질 차이는 1 % 미만이므로 결론에는 영향 없다.
11. **⛔ 우리 규율 재확인**: 이 논문의 어떤 수치도 **우리 `db/properties/` 절대값과 같은 표에 놓지 않는다.**
    특히 **힘 RMSE 3.35–5.56 meV/Å** 는 **탄소 · ACSF-MLP · PBE** 값이고, 우리 **UMA Li₃PS₄ 30.0 meV/Å**
    는 **황화물 · 등변 GNN · PBEsol** 값이다. **단위가 같다고 비교 가능한 것이 아니다.**

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 (이 논문 맥락) |
|---|---|
| **ID / OOD** | in-distribution(훈련 분포 안, 여기서는 held-out 테스트셋) / out-of-distribution(밖, 여기서는 cold curve·phonon) |
| **정확도 vs 정밀도** | accuracy = 참값과의 거리(잔차) · precision = 예측의 산포(σ의 역). `Fig. 1` 다트판. **둘은 독립일 수 있다** |
| **epistemic / aleatoric** | 인식론적(데이터 부족·모델 오지정·파라미터 불확실 — **줄일 수 있다**) / 우연적(데이터 자체의 변동성 — **못 줄인다**). **앙상블은 epistemic 만 잡는다** |
| **overconfident / underconfident** | σ < 실제 오차(과소확신·위험) / σ > 실제 오차(보수적·안전하지만 쓸모 감소). `Fig. 6` 의 회색 삼각이 후자 |
| **calibration** | σ 의 **크기**가 실제 오차 크기와 맞는가. **상관(순서)과 다른 개념** |
| **post-hoc calibration** | 검증셋으로 σ 에 배율·변환을 걸어 맞추는 후처리. **이 논문은 안 했다** |
| **bootstrap** | 원 데이터를 **복원추출**해 만든 유사 데이터셋들로 통계 산포를 추정. 여기서는 **구성 단위** 재샘플링 |
| **MC dropout** | 추론 시에도 dropout 을 켜서 확률적 예측을 여러 번 뽑아 앙상블로 삼는 것 (Gal & Ghahramani 2016) |
| **deep ensemble / committee** | 초기값만 다르게 독립 학습한 모델 묶음. 이 논문의 **random initialization** |
| **snapshot ensemble** | **한 번의 학습 궤적**에서 여러 epoch 의 가중치를 저장해 만든 앙상블 ("Train 1, get M for free") |
| **energy cold curve** | 0 K 에서 격자상수에 대한 에너지 곡선. 최소점 = 평형 격자상수·응집에너지, 곡률 = 탄성 정보. (EOS 곡선의 일종) |
| **phonon dispersion** | 힘상수 행렬(에너지 Hessian) → 동역학 행렬 고유값으로 얻는 `ω(q)`. 여기서는 ASE 유한차분 |
| **ACSF** | atom-centered symmetry functions — 회전·병진·치환 불변 원자환경 기술자 (Behler 2011) |
| **KLIFF / KIM-API / OpenKIM** | 퍼텐셜 학습 패키지 / 시뮬레이터-퍼텐셜 표준 인터페이스 / 퍼텐셜 저장소·검증 파이프라인 |
| **Pearson 상관** | 두 변수의 **선형** 상관. **순서·스케일 불변**이라 보정을 못 잰다 (그래서 M3 이 따로 필요) |
| **PCA 특징공간 커버리지** | 훈련 원자환경 기술자에 PCA 를 적합하고 새 구조를 투영해 **클러스터 안/밖**으로 외삽을 판정 |

---

## 16. 관련 문헌 (이 논문이 세운 좌표)

| 참조 | 무엇 | 우리에게 |
|---|---|---|
| **[6] Wen & Tadmor 2020** *npj Comput. Mater.* **6** | 이 논문의 **직계 전신** — NNIP 앙상블 UQ, 데이터셋 원본, S=100 근거 | 🔎 후속 인입 후보 |
| **[37] Carrete et al. 2023** *J. Chem. Phys.* **158**, 204801 | ★ *"정교한 추정기가 단순 committee 를 **일관되게 못 이긴다**"* + **어려운 배열 식별(능동학습)** | 🔴 **의뢰문 §2·§4 가 실제로 가리키는 논문. 이걸 받아야 그 질문의 정본이 생긴다** |
| **[26] Tan et al. 2023** *npj Comput. Mater.* **9**, 225 | 앙상블 vs **단일 모델 UQ** 비교 — *"어떤 방법도 모든 상황에서 최고가 아니다"* | 🔴 **우리 단일-UMA 좌표에 가장 직접적인 편** |
| **[36] Kahle & Zipoli 2022** *Phys. Rev. E* **105**, 015311 | OOD 배열에서 앙상블 σ 가 오차를 반영하는가 — 계·아키텍처 의존 | 🟡 |
| **[38] Wimer et al. 2026** *J. Cheminform.* **18**, 67 | NNIP 의 **epistemic/aleatoric/결합** 불확실도를 **정확도 + 보정 지표**로 벤치마크 | 🔴 **"보정 지표"가 우리에게 없는 그것 — 인입 후보 1순위** |
| **[33] Vita et al. 2024** LTAU-FF (arXiv:2402.00853) | **손실 궤적 기반** 거리형 UQ — **단일 모델** | 🟢 **단일 UMA 좌표의 또 다른 후보** |
| **[34] Hu et al. 2022** *MLST* **3**, 045028 | 거리 기반 OOD 지표 | 🟢 |
| **[67] Dale et al. 2025** arXiv:2511.17760 | *"능동학습이 실패할 때, 원인은 보정 안 된 OOD UQ 일 수 있다"* | 🟡 |
| **[59] Lakshminarayanan 2017** NeurIPS | deep ensemble 원전 | 🔎 |
| **[61] Huang 2017** arXiv:1704.00109 | snapshot ensemble 원전 ("Train 1, get M for free") | 🟢 §11-A 의 근거 |
| **[56] Gal & Ghahramani 2016** ICML | MC dropout 원전 | 🟢 |

---

## 17. ⛔ **못 하는 것 / 확인 못 한 것** (필수 절)

**A. 이 논문이 못 하는 것 (우리가 기대했다가 없는 것)**
1. **GP · conformal prediction · mean-variance · quantile regression · Bayesian NN 비교가 없다.**
   이름만 서론에 나오고 **실험 대상이 아니다.** 의뢰문 §1 이 예상한 "6종 비교표"는 존재하지 않는다.
2. **OOD 탐지 성능을 재지 않는다.** AUROC·precision@k·능동학습 획득 효율 **전부 없음.**
   *"어려운 표본을 찾는 능력"* 은 **Carrete 2023 [37]** 의 것이다.
3. **NLL·sharpness·coverage 확률·ECE·reliability diagram 이 없다.** (전문 검색 0건.)
4. **비용을 수치로 보고하지 않는다** (벽시계·GPU 시간 0). 비용 결론은 **"학습 횟수 100 vs 1"** 뿐.
5. **MD 를 돌리지 않는다** ⇒ **궤적 시간평균 관측량(D, σ_ionic, 열전도)의 UQ 를 다루지 않는다.**
   우리 보고량과의 간극 → §11-C.
6. **앙상블 크기 S 스윕이 없다.**
7. **처방을 주지 않는다** (저자 자신이 명시).

**B. 우리가 확인 못 한 것 (이 digest 의 한계)**
1. **SI 를 갖고 있지 않다.** 포논 그림·수치, 육방정계 dropout 스캔, ACSF 상세 파라미터 — **전부 미확인.**
   본문 서술만으로 정리했고, **포논에 관해 인용할 숫자가 하나도 없다.**
2. **GitHub 코드/데이터(`yonatank93/compare_UQ`)를 내려받아 확인하지 않았다.**
3. **`Fig. 3`·`Fig. 5` 는 크로핑에 실패해 이미지로 보지 못했다** (본문 캡션·서술로 대체).
4. **본 그림 / 안 본 그림**:
   - ✅ **실제로 본 것 (7장)**: `Fig. 6`, `Fig. 7`(+ 6배 확대 부분판 2장), `Fig. 8`, `Fig. 9`, `Fig. 10`,
     `Fig. 11`, `Fig. 12`, `Fig. 13` — **논문 주장을 떠받치는 그림 전부**
   - ⛔ **안 본 것**: `Fig. 1`(다트판 개념도), `Fig. 2`(MLP 그래프), `Fig. 4`(탄소 결정구조) —
     **셋 다 순수 모식도**라 본문 서술로 충분하다고 판단. `Table 1`·`Table 2` 는 관례대로 **PDF 텍스트**로 읽었다
     (이미지보다 정확).
5. **본문 서술과 그림이 어긋난 것**: **없었다.** 본문의 정성 주장(bootstrap 상관 최고·과소확신, dropout 보정 양호,
   snapshot ≈ random init, diamond 붕괴, σ 감소)이 **전부 그림에서 확인됐다.**
   다만 **본문이 언급하지 않은 것**을 두 개 발견했다:
   ① `Fig. 7b` random-init **diamond 에너지 σ ≈ 49 meV/atom** 이상치(같은 열 다른 구조의 3–5배) — 논문 미언급.
   ② `Fig. 6` monolayer 행의 `σ ≈ 10⁻²` 고립 섬(네 방법 공통) — 논문 미언급.
6. **`figure-read ≈` 로 표시한 값은 눈금 판독**이라 ±10 % 정도 오차가 있다.
   **예외**: `Fig. 7a` 의 Pearson 값들은 히트맵에 **숫자가 인쇄돼 있어** 정확하다.
7. **Eq. (8) 의 `S−1`/`S` 분모**를 표지에서 확정 못 했다 (조판 깨짐).
8. **저자 소속 확인**: Transtrum 이 BYU 가 아니라 **Cross Stream Consulting** 으로 적혀 있다 —
   Accepted Manuscript 단계라 최종본에서 바뀔 수 있다.
9. **연도**: 표지가 **2026** 인데 slug 은 `2025` 다. **slug 을 안 바꾼 것은 동시작업 조율 때문**이고,
   **인용 시에는 2026 을 쓴다.**

---

## 18. 🔗 이 digest 의 위치

- **자매편(같은 인입 배치, MLIP 불확실도 축 3편)**: `imbalzano2021_committee_uq_md_thermodynamic_averages`
  ← **궤적 시간평균으로의 전파는 그쪽이 정본이다.**
- **우리 도구**: `tools/ionic/mlip_committee.py` (`analyze` = σ축 · `force_contrast` = 잔차축)
- **우리 좌표 문서**: `litdb/comparison_vs_ours.md` §J (MLIP 방법론 축), 특히 **§J-1**(UMA 힘 정확도 실측),
  **§J-2**(Zhang npj 온도 상한 경고), **§J-7**(방법 원전 블록)
- **관련 talk**: `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 인입 대기열에는
  **이 논문이 올라 있지 않다** (그 대기열은 MTP·SevenNet·GNoME 계열). 다만 그 talk 의
  **MTP `γ`(외삽등급)** 논의와 **주제가 인접**하다 — `γ` 는 **선형 기저 위 D-optimality**,
  이 논문은 **앙상블 산포**로, **둘 다 "외삽 감시" 라는 같은 문제의 다른 해법**이다.
  ⛔ 대기열에 없으므로 **talk 파일은 건드리지 않았다.**

# An AI-Ready Fine-Tuning Framework for Accurate Machine-Learning Interatomic Potentials in Solid–Solid Battery Interfaces

*사전학습 데이터를 섞어 미세조정하면 계면 MLIP 오차가 준다*

- Liu et al. · arXiv 2026, preprint · doi:n/a (preprint) · digest `liu2026_ai_ready_finetuning_solid_solid_interfaces`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 사전학습 데이터를 섞어 미세조정하면 계면 MLIP 오차가 준다

> MACE-MP-0 미세조정에 replay를 넣으면 여섯 계 모두 오차가 줄지만, 물성 검증은 벌크에 그친다. (L45 · 181 · 389)

### 요점

1. MACE-MP-0를 배터리 고체-고체 계 여섯 개에 미세조정하는 FIRE를 제안했고, replay와 SOAP, PCA, K-means 표본추출을 묶었다. (L45–46 · 48–49)
2. FIRE는 여섯 계 모두에서 replay 없는 미세조정보다 RMSE가 낮았지만, 황화물 두 계는 힘 RMSE가 43.02와 54.18 meV/Å로 가장 나빴다. (L167–168 · 175 · 181)
3. 물성 검증은 벌크 세 계에서만 했고 계면 물성은 없어서, 확실히 말할 수 있는 것은 replay가 없는 것보다 낫다는 데까지다. (L183 · 386 · 389–390)

### 문제와 접근

고체-고체 계면은 결함과 이종 화학결합 때문에 구조가 다양하다. 원문은 처음부터 학습하는 MLIP은 데이터가 많이 들고, 범용 MLIP(U-MLIP)은 범용성 대가로 특정 계에서 정확도가 떨어진다고 적었다. 그 대안으로 MACE-MP-0를 계마다 미세조정하는 FIRE(Fine-tuning with Integrated Replay and Efficiency)를 내놓았다. (L45 · 59–62)

FIRE는 두 부품으로 이뤄진다. 첫째 replay는 에폭마다 사전학습 데이터를 부분표집해 계 데이터와 함께 학습시켜 catastrophic forgetting을 막는다. 둘째 효율 표본추출은 20–50개 구조로 만든 임시 모델로 MD를 돌려 ~20,000 구조를 얻고, SOAP 서술자와 PCA, K-means로 대표 구조만 고른다. 불확실도를 쓰는 능동학습은 쓰지 않았다. (L46 · 48 · 103 …)

- 그림 — Fig. 1: B에서 에폭마다 위에서 내려오는 사전학습 sub-sample과 아래에서 올라오는 task mini-batch가 섞이는 부분을 보면 된다. C는 종잣값 모델에서 refined dataset까지 표본추출 순서를 보여 준다. (L102–103 · 116 · 120)

### 여섯 계의 정확도

replay가 있는 FIRE는 replay 없는 미세조정(Vanilla)보다 여섯 계 모두에서 에너지와 힘 오차가 작았다. Li/Li₆PS₅Cl에서 에너지 RMSE는 1.29에서 0.86 meV/atom으로, 힘 RMSE는 55.47에서 43.02 meV/Å로 줄었다. 문헌의 기존 보고값(Reference)보다도 모든 계에서 낮았다. (L162 · 168 · 171 …)

계 사이의 차이는 컸다. 원문은 초록에 에너지 RMSE below 1 meV/atom, 힘 near 20 meV/Å라고 적었다. 그러나 인쇄된 막대값으로는 황화물 두 계가 가장 나빴고, Li₃PS₄/Li₃B₁₁O₁₈은 1.04 meV/atom과 54.18 meV/Å였다. (L167–168 · 174–175 · 177)

- 그림 — Fig. 2: C의 막대에 인쇄된 FIRE, Vanilla, Reference 값을 계별로 나란히 보면 된다. B의 힘 패리티 플롯은 범례가 Train과 Valid 둘뿐이다. (L151 · 160 · 171)

### 데이터 효율과 비용

표본 수를 늘려 가며 FIRE, 무작위 추출, 처음부터 학습, Vanilla를 비교했다. 원문은 FIRE가 모든 데이터 크기에서 가장 낮은 RMSE를 내고 무작위 표본추출보다 크게 낫다고 적었다. 표본추출 시간은 파인튜닝에 비해 작은 부가 비용이라고 적었다. (L199–200 · 214 · 217 …)

최종 학습셋은 최대 4,000 프레임까지 살폈다. 수렴에 필요한 프레임 수는 계에 따라 달랐고, 다상인 LLZTO가 Na/Na₃SbS₄보다 더 많은 프레임을 요구했다. (L330 · 379–380)

- 그림 — Fig. 3: A와 B의 PCA 투영에서 회색 전체 풀 위에 선택된 표본이 얼마나 퍼지는지 보면 된다. C와 D의 오른쪽 패널은 파인튜닝과 표본추출의 시간비용을 로그 축으로 그렸다. (L187 · 192 · 199 …)

### 벌크 물성 검증

미세조정 모델로 세 전해질의 이온 전도도를 계산해 EIS와 비교했다. 대상은 T-Na₃SbS₄, LLZTO, LPSCl이며 셋 다 단일상 벌크다. LPSCl의 D는 4.29×10⁻¹¹ m²/s였고, σ는 MD 0.75 mS/cm, EIS 0.89 mS/cm였다. (L256 · 262 · 389)

Young's modulus는 AFM 나노역학 맵의 공간평균과, Poisson's ratio는 문헌 계산값과 비교했다. 원문은 역학 응답을 비교적 높은 정확도로 잡는다고 적었다. MD 시간은 MACE-MD가 16 원자에서 3456 원자까지 거의 평평했고, VASP-MD는 576 원자 근처가 메모리 한계였다. (L295 · 297–298 · 305–306)

- 그림 — Fig. 4: A의 세 열에서 구조, MSD 곡선, EIS Nyquist와 등가회로 적합을 차례로 보면 된다. C는 원자 수에 따른 s/step을 MACE-MD와 VASP-MD로 나눠 그렸다. (L256 · 264 · 304)

### 어디까지 믿나

검토 측은 계면에서 정확하다는 주장이 아직 증명되지 않았다고 본다. 학습은 계면 구조로 했지만 검증은 벌크 세 계에서 했고, 접착일이나 계면 저항 같은 계면 물성은 없다. 계면층과 벌크층을 나눈 오차 보고도, 독립 테스트셋도 없다. 여섯 계 중 LLZTO는 도핑 벌크라 실질 계면은 네 개라고 본다. (L82 · 156 · 386 …)

검토 측은 초록과 본문 문장 일부가 그림과 어긋난다고 본다. 초록 수치는 황화물 두 계에서 맞지 않고, Fig. 3C에서는 작은 데이터 크기에서 무작위 추출이 FIRE보다 오차가 낮다. 검토 측 검산으로는 LPSCl의 인쇄된 D를 Nernst–Einstein으로 바꾸면 인쇄된 σ의 89배가 나오며, MD 온도는 본문에 없다. 그래도 replay가 Vanilla보다 낫다는 결론은 같은 데이터와 백본의 통제된 비교라 가장 방어 가능하다고 본다. (L174–175 · 182 · 215 …)

### 용어 풀이 (논문에 없는 일반 설명)

- **catastrophic forgetting과 replay**: 새 데이터만 계속 학습하면 이전에 배운 것을 잃는 현상이 catastrophic forgetting이고, 옛 데이터를 학습 중에 다시 섞어 주어 이를 막는 기법이 replay다.
- **SOAP**: 원자 주변 이웃 배치를 회전에 불변인 벡터로 바꿔 두 구조의 유사도를 수치로 비교하게 해 주는 서술자다.
- **Nernst–Einstein 식**: MD에서 얻은 확산계수를 이온 농도와 온도를 써서 이온 전도도로 환산하는 식이며, 이온 간 상관운동은 Haven 비로 보정한다.

### 우리 연구에 주는 뜻

- 여섯 계 중 Li/Li₆PS₅Cl은 우리 comp1과 Li 금속 계면에, Li₃PS₄/Li₃B₁₁O₁₈은 우리 B₂O₃ 축의 화학에 겹치지만, 우리 주축인 황화물 SE와 산화물 양극 계면은 없다. (L76–77 · 426–427)
- 우리는 UMA-s-1p1을 zero-shot으로 쓰는데 이 논문은 MACE-MP-0 미세조정만 다루고 zero-shot 계면 오차를 재지 않았으므로, 우리는 force_contrast를 계면 구조에서 돌려 직접 진단해야 한다. (L374 · 505 · 571–572)
- B2를 W_ad 하나가 아니라 표본 분포로 정의하고 집계 규칙을 미리 선언하는 방향은 이 논문의 주장이 아니라 우리 해석으로 얻은 것이다. (L361 · 364–366)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| Li/Li₆PS₅Cl 힘 RMSE (FIRE) | 43.02 meV/Å | Fig. 2C 인쇄값, 미세조정 후 | L441 |
| Li₃PS₄/Li₃B₁₁O₁₈ 에너지 RMSE (FIRE) | 1.04 | meV/atom, 초록 1 meV/atom 초과 | L174 |
| LPSCl 전도도 MD 대 EIS | σ_MD 0.75 vs σ_EIS 0.89 mS/cm | 벌크 LPSCl, Fig. 4A | L447 |
| LPSCl 확산계수 | 4.29×10⁻¹¹ m²/s | MSD 적합, MD 온도 미기재 | L262 |
| 종잣값 구조 수 | 20–50개 | pre-fine-tuned 모델용 perturbed | L122 |
| MD 후보 풀 크기 | ~20,000 구조 | pre-fine-tuned 모델 MD로 생성 | L125 |

### 읽을 때 조심할 것

- 동료심사를 거치지 않은 preprint이고 SI를 확인하지 못해, DFT 설정과 replay 비율, 동결 층수, MD 조건 없이 본문만으로는 재현할 수 없다. (L17 · 22 · 325–326 …)
- 초록의 near 20 meV/Å를 황화물 계면에 적용하면 안 되고, LPSCl 계면의 실제 보고값은 43 meV/Å다. (L175 · 178–179)
- 인쇄된 D 값은 MD 온도가 적혀 있지 않아 다른 온도의 값과 비교할 수 없다. (L276 · 279)
- Reference 막대는 RMSE와 MAE를 섞었고 MACE-MP-0 zero-shot 값이 아니며, UMA는 다루지 않았다. (L373 · 420 · 494–495)

### 원문에서 먼저 볼 곳

- Fig. 2C: 여섯 계의 FIRE, Vanilla, Reference RMSE가 막대에 인쇄돼 있어 이 논문의 알맹이를 정확값으로 볼 수 있다. (L160 · 162)
- Fig. 4A: LPSCl MSD 적합 창과 σ 대조를 보고 D와 σ의 관계를 직접 따져 볼 수 있다. (L258 · 262 · 281)
- Fig. 3B와 3C: PCA 커버리지와 데이터 크기별 RMSE에서 FIRE 표본추출 이득이 계에 따라 달라지는지 확인할 수 있다. (L192–193 · 215 · 234)

태그: MACE-MP-0 · fine-tuning · replay · SOAP · K-means · Li₆PS₅Cl · RMSE · 고체-고체 계면

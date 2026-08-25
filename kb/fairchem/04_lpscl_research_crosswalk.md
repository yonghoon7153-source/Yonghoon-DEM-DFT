# Fair-Chem capability to our LPSCl research

## 왜 이걸 정리하나

Fair-Chem은 우리 연구에서 “정답을 대신 주는 DB”보다 계산을 싸게 넓혀 주는 엔진에 가까워. 가장 가치 있는 사용처는 구조 relaxation, 여러 configuration의 1차 비교, MD scout, property workflow 자동화야. 반대로 MP thermodynamics, DFT validation, ionic conductivity의 승인 판정은 별도 방법 계약이 필요해.

## 적용 표

| Official capability | Our use | Current project status | Required boundary |
|---|---|---|---|
| UMA `omat` | LPSCl relaxation/screening | conditional | fmax, steps, residual stress, exact structure provenance |
| UMA energy | host-relative comparison | same-method only | model/task/reference를 섞지 않기 |
| ASE MD | Li dynamics scout | project protocol controls claim | distinct seed, raw trajectory, fixed MSD window |
| LAMMPS integration | future large-cell MD | not yet canonical | ASE–LAMMPS equivalence and version pin |
| Elastic workflow | mechanical diagnostics | conditional | relaxed/clamped semantics, nonphysical row reject |
| Phonon workflow | future stability check | not yet canonical | displacement/supercell convergence |
| Formation energy | OMat-relative workflow | blocked for MP mixing | MP hull/ESW와 별도 ledger |
| OC20NEB/CatTSunami | transition workflow pattern | scout-only analogy | bulk Li hop에는 별도 cell/path/DFT contract |
| Batch inference | large roster throughput | engineering-ready | batch row를 농도/반복으로 오해 금지 |
| Fine-tuning | future LPSCl adaptation | after ground truth | DFT energy/force/stress, chemistry-group split |

## 우리 논문에 바로 쓸 수 있는 인사이트

### 1. Universal model도 method identity가 필요해

UMA가 여러 domain을 공유해도 `omat`, `oc20`, `omol`은 서로 다른 DFT convention을 반영해. 그래서 “UMA prediction”만 적는 건 부족해. 모델과 task가 둘 다 Methods의 일부야.

### 2. 계산 수가 아니라 비교 규약이 screening을 결정해

Batch inference로 수천 구조를 계산할 수 있어도 composition, site, seed가 통제되지 않으면 농도축이나 반복실험이 생기지 않아. Fair-Chem의 throughput 기술과 우리의 design audit를 함께 설명하면 이 점이 훨씬 선명해져.

### 3. MLIP energy와 MP thermodynamics는 한 축이 아니야

Official README가 OMat/UMA total energy를 MP correction/reference와 직접 섞지 말라고 경고해. 우리 cascade의 UMA relaxation energy와 MP grand-potential ESW를 분리해 둬야 하는 근거가 여기서도 확인돼.

### 4. Random seed는 provenance야

Official example은 prediction-unit 생성이 global NumPy seed에 영향을 줄 수 있다고 경고해. 서로 다른 directory를 만들었다는 사실만으로 독립 MD seed가 되는 게 아니야. seed, initial velocities, model instance를 run receipt에 남겨야 해.

### 5. Capability와 validation을 분리해

Official code에 elasticity, phonon, MD, LAMMPS가 있다고 해서 LPSCl에서 자동 승인되는 건 아니야. “기능이 있다”, “우리 조건에서 재현됐다”, “논문 주장에 써도 된다”를 별도 status로 둬야 해.

## 우선순위 높은 다음 검증

1. LPSCl representative structure에서 UMA version/task별 energy-force-stress benchmark
2. relaxation fmax/step/stress convergence matrix
3. seed와 model construction을 포함한 MD reproducibility receipt
4. model upgrade 전후 동일 input regression
5. large-cell ASE ↔ LAMMPS energy/force/stress equivalence
6. fine-tuning 전 chemistry/site/composition-family grouped split 설계

## 금지 문장

- “UMA energy로 Materials Project E_hull을 계산했다.”
- “Fair-Chem이 ionic conductivity를 검증했다.”
- “OC20NEB가 있으므로 bulk Li barrier도 검증됐다.”
- “세 batch label은 독립 농도 또는 반복이다.”
- “새 UMA version은 더 정확하므로 기존 DB와 바로 합쳤다.”
- “Inorganic model이므로 Li3N에도 사용 가능하다.”

행 단위 machine record는 [lpscl_crosswalk.json](../../db/knowledge/fairchem/lpscl_crosswalk.json)에 있어.


# Workflows and code architecture

## Official monorepo map

```text
src/fairchem/
├─ core/          inference, training, datasets, models, workflows
├─ data/          oc, odac, omat, omc, omol tooling
├─ applications/  AdsorbML, CatTSunami, FastCSP, OCx
├─ demo/          OCP API client/workflows
└─ lammps/        LAMMPS integration

configs/
├─ uma/
├─ escaip/
└─ allscaip/
```

Pinned tree에는 source 453개, config 128개, test file 187개가 있어. 정적 `def test_` 정의는 840개지만, 이번 bundle build에서는 Fair-Chem dependency/checkpoint를 설치해 upstream test를 실행한 건 아니야.

## 실제 기술 목록

### Inference

- `pretrained_mlip`
- `FAIRChemCalculator`
- batch inference
- `InferenceBatcher`
- Ray/multi-GPU inference
- LAMMPS bridge

### Materials workflows

- single point
- atomic/cell relaxation
- MD and NVE MD
- elasticity
- phonons
- thermal conductivity
- formation-energy references

### Application workflows

- AdsorbML
- CatTSunami / catalytic NEB
- FastCSP
- OCx experiment-linked data
- OCP API demo

### Model development

- Hydra configuration
- training and evaluation runners
- fine-tuning templates
- dataset conversion/readers
- benchmark reducers

## 우리에게 차용할 설계

1. `task-specific reducer`: 서로 다른 물리를 하나의 universal score로 만들지 않아.
2. `recipe + runner + reducer`: 입력 생성, 실행, 수집, 해석을 파일/코드 층에서 분리해.
3. `named checkpoint registry`: 모델 별칭이 실제 remote artifact와 reference file을 가리키게 해.
4. `batch service`: 계산 처리량과 scientific denominator를 분리해.
5. `application package`: LPSCl 전용 workflow도 core를 오염시키지 않는 별도 package가 좋아.

## 그대로 가져오면 안 되는 부분

- Official workflow existence만 보고 우리 chemistry에서 validated라고 쓰면 안 돼.
- Current live formation-energy/phonon/elastic tutorial은 실행 오류가 렌더돼 있어. 예제 availability와 executability가 다르다는 실제 반례야.
- Current `main` 문서의 일부 legacy config 링크는 현재 tree에 없는 경로를 가리켜.
- LAMMPS code license는 root MIT와 별도로 확인해야 해.

전체 기술 record는 [technologies.json](../../db/knowledge/fairchem/technologies.json), 전체 파일은 [repo_files.csv](../../db/knowledge/fairchem/repo_files.csv)에 있어.


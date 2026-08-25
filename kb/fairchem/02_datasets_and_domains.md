# Datasets and application domains

## Domain map

| Domain | Main datasets | What the labels mean |
|---|---|---|
| Organic molecules | OMol25, OMol25 Electronic | molecular energy/force/electronic data with molecular charge/spin context |
| Molecular crystals | OMC25 | periodic PBE+D3 crystal data |
| Inorganic materials | OMat24 | PBE/PBE+U energy, force, stress |
| Heterogeneous catalysis | OC20, mAds, OC22, OC20Dense, OC20NEB, OC25 | surface/interface structures, relaxations, reactions |
| Experimental catalysis | OCx24 | experiment–computation bridge |
| Direct air capture | ODAC23, ODAC25 | CO2/H2O adsorption in MOFs |

OMat24 문서는 1,077,382개 training structure와 1,025,361개 validation subset entry를 따로 보고해. 이 숫자는 서로 다른 표의 분모라 합치거나 “2.1M unique materials”로 바꾸면 안 돼.

OC20은 133M+ DFT calculation 규모고, OMol25와 OMC25도 각각 대규모 domain dataset이야. 하지만 dataset size가 우리 LPSCl에서의 적용성을 보증하지는 않아. composition, phase, defect, temperature, target property가 겹치는지를 별도로 봐야 해.

## 데이터 재사용 규칙

1. `dataset_id`, split, task, reference method를 항상 함께 기록해.
2. literature benchmark와 우리 DB 절대값을 방법 설명 없이 섞지 않아.
3. model training payload는 Git repo에 없으므로 “repo를 전수 조사했다 = 학습 데이터를 전수 읽었다”가 아니야.
4. HF access/gating과 각 dataset license를 별도로 확인해.
5. `energy`, `force`, `stress`, `transition state`, `experiment`를 하나의 generic score로 뭉치지 않아.

## LPSCl에 직접 중요한 dataset insight

- OMat24는 구조·에너지·힘·stress 사전학습의 가장 가까운 official domain이야.
- OC25가 electrolyte interface를 포함한다고 해도, LPSCl bulk/SEI/slab 문제와 동일한 method contract는 아니야.
- OC20NEB/CatTSunami는 transition-state workflow의 좋은 참고지만 bulk Li hopping 데이터가 아니야.
- OMol/OMC/ODAC는 multi-domain representation 연구와 fine-tuning 설계에는 참고가 되지만, task energy를 LPSCl 값과 직접 비교하면 안 돼.

전체 structured records는 [datasets.json](../../db/knowledge/fairchem/datasets.json)에 있어.


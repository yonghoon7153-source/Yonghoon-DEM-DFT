# Models and task identities

## Model inventory

Pinned code의 `pretrained_models.json`에는 13개 이름이 등록돼 있어.

| Family | Registered names | Count |
|---|---|---:|
| UMA | `uma-s-1p2p1`, `uma-s-1p2`, `uma-s-1p1`, `uma-m-1p1` | 4 |
| OMol25 eSEN / AllScAIP | 3 eSEN + 2 AllScAIP | 5 |
| OC25 eSEN | conserving + direct | 2 |
| ODAC25 eSEN | filtered + full | 2 |

실제 weight는 Git repo에 없고 Hugging Face에서 받아. Git 안의 `.pt` 파일은 model algebra 또는 test fixture라 pretrained weight inventory로 세면 안 돼.

문서에서 강조하는 모델 목록과 코드 registry가 완전히 같지는 않아. 예를 들어 registry에는 `uma-s-1p2p1`이 있지만 prose의 대표 표는 더 좁을 수 있어. UI는 `documented`와 `registered_in_code`를 두 필드로 분리해야 해.

## UMA tasks

Task는 응용 분야 이름표가 아니라 “어떤 DFT data convention을 모방하는가”를 고르는 method identity야.

| Task | Domain | Reference convention | Main caution |
|---|---|---|---|
| `omol` | aperiodic molecules | wB97M-V/def2-TZVPD, ORCA 6 | charge/spin required |
| `omc` | molecular crystals | PBE+D3, VASP | charge/spin variation not trained |
| `omat` | inorganic materials | PBE/PBE+U, VASP 5.4 | MP total-energy corrections와 호환 아님 |
| `oc20` | surface catalysis | RPBE, VASP 5.4, no dispersion | oxide/solvent 없음 |
| `odac` | CO2/H2O in MOFs | PBE+D3, VASP 5.4 | chemistry scope 좁음 |
| `oc25` | solid-liquid interfaces | RPBE+D3, VASP 6.4 + dipole | UMA 1.2 only; work function 미출력 |
| `oc22` | oxide catalysis | spin-polarized PBE+U | docs에는 있으나 pinned public enum에는 없음 |

마지막 줄은 permanent product claim이 아니라 pinned commit의 docs/code drift야. 업그레이드할 때 다시 확인해야 해.

## 우리 provenance 최소값

모든 UMA 결과에 아래를 남겨.

```json
{
  "model_id": "uma-s-1p1",
  "checkpoint_revision": "...",
  "task_id": "omat",
  "fairchem_core_version": "...",
  "fairchem_source_commit": "...",
  "calculator_settings": {},
  "random_seed": 0,
  "input_structure_sha256": "..."
}
```

모델 버전만 바뀌어도 새 `method_id`야. `uma-s-1p1`과 `uma-s-1p2`를 같은 column에 조용히 합치면 안 돼.

## Architecture insight

UMA는 equivariant GNN backbone과 Mixture of Linear Experts를 이용해 여러 chemistry task를 한 family 안에서 다뤄. 여기서 얻을 논문용 인사이트는 “universal = method-free”가 아니라 반대야. 공유 backbone이 있어도 task conditioning과 reference convention은 계속 결과의 일부야.

Sources: [UMA docs](https://fair-chem.github.io/uma/), [pinned model registry](https://github.com/facebookresearch/fairchem/blob/93a03d656806a55f08c7cd126cfaa40ef18181fb/src/fairchem/core/calculate/pretrained_models.json), [pinned task enum](https://github.com/facebookresearch/fairchem/blob/93a03d656806a55f08c7cd126cfaa40ef18181fb/src/fairchem/core/units/mlip_unit/api/inference.py).


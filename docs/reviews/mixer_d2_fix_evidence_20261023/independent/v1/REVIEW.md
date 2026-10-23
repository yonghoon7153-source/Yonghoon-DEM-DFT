# MXD2 생성기 diff 독립 사전 공격 리뷰

2026-10-23. 결론: **수정 또는 명시적 한정이 필요한 4건**. 정상 입력 산술이 틀렸다는 판정은 아니다. P2 시험 공백 1건, P3 새 회귀 1건, P3 기존 입력 경계 잔여 1건, P3 시험 공백 1건이다. 반박 세션 GO나 실행 승인을 대신하지 않는다.

## 범위와 재현

- 입력: `input_generator.patch`만 구현 설명으로 사용했다. 저자 설명·저자 보고서는 읽지 않았다. 정본 지침 `AGENTS.md`, `CLAUDE.md` 사전 공격 리뷰, `docs/handoff_codex_nonrint_20261023.md`, MXD2 원장, 벽 유도·기존 등록 문서를 대조했다.
- 기반 HEAD 관찰: `7799a2ff64ba462b42ce05edd3e63b7c2854d557`. 원본 생성기 SHA-256 `6baaa04c13c842c2d8e486cbef83bb5cb6f6e3d5f88c5f0f0d8c0904d3949f30`.
- diff SHA-256 `bf29dc9f26e6bdd8a44713e1e865f2cbc2c2517a6755dd347a20df011adce583`. 적용된 생성기 SHA-256 `dada1ebbf22dfc74a0d47000e1a35493d5e2d30cc2bc8d9e92509984665ef81b`.
- 아래 행 번호는 `evidence/snapshot/scripts/make_mixer_deck.py`에 해당한다. 저장소 tracked 파일을 고치지 않았고 commit/push, 전체 저장소 게이트, LIGGGHTS/GPU/장비 실행은 하지 않았다.
- 산출물: `reproduce.py`, `evidence/results.json`, `reproduce.log`, 실제 발행 덱, 변이별 `selftest.log`.

```bash
source /workspace/.cloud-setup/nonrint/activate.sh
python -I reproduce.py \
  --repo /path/to/original/repo \
  --patch /path/to/input_generator.patch \
  --out /tmp/mxd2-independent-review
```

`--repo`는 읽기 전용으로 사용한다. 임시 사본·덱·변이는 `--out` 아래에만 쓴다. 이미 수정된 저장소를 검사할 때는 `--patch`를 생략할 수 있지만, 이 경우 원본/패치 비교 항목도 같은 소스를 검사하므로 아래 회귀 재현에는 위 원본을 써야 한다.

## R1 — P2: 절대 Bo 검사가 출력 중력을 읽지 않아 D2 전용 중력 오류가 생존

- 위치: **2818행**, `_mxd_bo_tokens`; 검사 호출 2827행.
- 재현: 생산 템플릿의 `gravity 9.81` 한 토큰을 `gravity {1.0 if ARMS[arm].get('rule') == 'geomean' else 9.81}`로 바꾼다. 기존 팔 출력은 그대로이고 D2만 중력이 달라진다.
- 결과: 자체 **154/154 PASS, rc 0**. 실제 덱은 `gravity 1.0`, 입력·메타 Bo는 `0.73`; 덱의 CED·E·ν·반경·밀도·중력으로 독립 계산한 Bo는 **7.16120778729592**다. 약 9.81배 오류다.
- 원인: 새 검사는 템플릿 반경·밀도는 읽지만 무게의 중력에 `9.81`을 직접 쓴다. 전 팔을 바꾸는 중력 변이는 옛 골든 해시가 잡지만, D2 전용 오류는 그 골든 범위 밖이다.
- 영향 한정: 제출된 생산 코드의 중력은 9.81이며 정상 덱 산술은 통과했다. 이 결함은 MXD2-02의 “실제 인쇄 덱으로 절대 Bo를 독립 확인”한다는 보장의 공백이다.
- 보완 방향: 실제 중력 명령도 파싱하여 물리값 9.81 유지와 그 중력으로 계산한 Bo를 각각 확인한다. 새 검사에서 위 변이가 실패해야 한다.
- 증거: `evidence/mutants/gravity_1_d2_only/{make_mixer_deck.py,selftest.log,in.mixer}`, `results.json → mutations.gravity_1_d2_only`.

## R2 — P3: 새 벽 결합 검사가 비활성 AM_S를 요구하여 기존 상 선택 API가 회귀

- 위치: **543–544행**, `gm_arm`.
- 재현:

```python
set_phases(('AM_P', 'SE'))
a = gm_arm({'AM_P': 0.3, 'SE': 1.0},
           gamma_wall=gm_wall_from_ncm(0.3), bo_se=0.73,
           rho_uncoated_ncm=0.3)
register_arm('TWOPHASE', a)
p = plan(100000, cgf=151.4, dens_gen='lab20261014')
deck(p, resolve_rpm(p['R']), 2, arm='TWOPHASE')
```

- 결과: 원본은 실제 덱 **7,861 bytes** 발행. 패치는 `SystemExit: ...비코팅 (ρ,ρ) 또는 코팅 기준 (1,1)...`로 거부한다.
- 원인: `set_phases`와 `gm_arm`은 활성 `TYPES`에 맞춘 입력을 허용한다. 새 검사는 활성 상과 무관하게 `(g.get('AM_P'),g.get('AM_S'))` 두 값을 요구한다. 비활성 AM_S의 `None`은 어떤 허용 튜플에도 들어가지 않는다.
- 영향 한정: 기본 3상 CLI에는 영향이 없다. 기존 라이브러리 경로인 AM_P+SE 부분계가 막힌다. 새로운 상·물리 규칙을 요구하는 것이 아니라 기존 지원 범위를 보존하는 문제다.
- 보완 방향: 활성 NCM 상들에 대해 같은 비코팅/코팅 기준을 검사하거나, D2를 3상 전용으로 한정한다면 그 별도 제약·호환성 변경을 명시한다.
- 증거: `evidence/two_phase_original.in.mixer`, `results.json → observations.active_phases_regression`.

## R3 — P3: 팔 이름은 막았지만 desc 줄바꿈이 실행 명령으로 발행됨

- 위치: **535–538행** `gm_arm`의 설명 수용, **1353행** 덱 삽입. 전자는 이번 diff의 변경 함수, 후자는 기존 출력 위치다.
- 재현: 정상 벽 결합 팔을 `desc='independent review\nprint "DESC_EXECUTES"\n#'`와 함께 만든 뒤 `register_arm → deck → deck_meta`를 호출한다.
- 결과: 모두 성공. 출력 덱 **89행**에 주석이 아닌 `print "DESC_EXECUTES"`가 생긴다. 실제 시뮬레이터는 실행하지 않았다.
- 원인: 이름의 `fullmatch`는 이름 끝 개행을 막지만, 사용자 제공 `desc`는 단일 주석 줄에 그대로 들어간다. 설명의 자연스러운 줄바꿈도 덱 명령/문법 오류로 바뀔 수 있다.
- 영향 한정: CLI는 desc 옵션을 노출하지 않는다. 라이브러리 호출에 국한된 기존 잔여 결함이며, 패치가 새로 도입한 것은 아니다. MXD2-04의 줄바꿈 입력 보장을 넓게 닫을 때에는 남겨둘 수 없다.
- 보완 방향: desc의 줄 경계를 거부하거나 각 설명 줄을 확실한 주석으로 출력한다. 실제 deck 발행 결과에 실행 줄이 없는지 검사한다.
- 증거: `evidence/description_injection.in.mixer`, `results.json → observations.description_injection`.

## R4 — P3: scalar CLI 숫자 검증을 되돌린 두 변이가 154/154 통과

- 위치: **2861–2872행** `_mxd_cli_bad`; 생산 옵션 **2934행·2937행**.
- 재현 A: `--gm-wall-ncm`의 `type=_gm_cli_number`만 `type=float`로 되돌린다. 실제 CLI에 `--gm-gamma AM_P=3,AM_S=3 --gm-wall-ncm 0_3 --gm-bo-se .73`를 준다.
- 재현 B: `--gm-bo-se`의 타입만 `float`로 되돌리고 `--gm-gamma AM_P=.3,AM_S=.3 --gm-wall-ncm .3 --gm-bo-se 0_73`를 준다.
- 결과: 각 변이에서 자체 **154/154 PASS**이고, 실제 CLI도 **rc 0 / in.mixer 발행**. `float()`가 밑줄을 제거해 각각 3.0과 0.73으로 읽는다.
- 원인: 새 CLI 부정 시험은 `--gm-gamma` 문자열만 바꾼다. 같은 보장을 요구하는 벽·Bo scalar 옵션의 연결은 시험하지 않는다.
- 영향 한정: 패치 원본의 두 옵션은 올바른 타입을 사용한다. 현재 잘못된 덱을 쓰는 결함이 아니라 MXD2-04의 회귀 방지 공백이다.
- 보완 방향: 각 scalar 옵션에 밑줄·Unicode·공백·NaN/inf/넘침을 실제 CLI로 전달하여 거부와 산출물 부재를 확인한다.
- 증거: `evidence/mutants/{wall_cli_float,bo_cli_float}/selftest.log` 및 각 `emitted/`, `results.json → mutations`.

## 검증 범위와 통과 증거

| 함수/보장 | 독립 공격 | 결과 |
|---|---|---|
| `_gm_num`, `gm_wall_from_ncm` | NaN/±inf/0/음수/bool/문자열/subnormal/10**1000/None/list/dict를 Bo·ρ로 실제 발행 경로에 넣음 | 24개 모두 통제된 거부 |
| `_gm_cli_number`와 CLI 연결 | gamma 빈·부분·중복·NaN/inf/넘침/밑줄/Unicode/공백/잘못된 SE + scalar 벽·Bo 20개 | **실제 CLI 32개 모두 rc≠0, traceback 없음, in.mixer 없음** |
| `gm_arm`, `register_arm` | 불일치 ρ, 미결합 벽, 이름 개행 변이, 부분 상, desc 개행 | ρ·벽·이름은 확인; R2·R3 잔여 |
| `ced_matrix_geomean` | 밀도 2세대 × CGF 3값 × 강성 2값 × ρ 4값 × 코팅 2값 × Bo 2값 | **192 덱 / 1,728 접촉쌍** 독립 인쇄값 산술 통과 |
| 쌍 규칙·반경·단위 | `F0=(2πR*CED)^3/[(4/3)E*√R*]^2`, 실제 출력 r·ρ·g로 무게, 쌍별 `√γ_iγ_j R*/R*_SS` | Bo 최대 상대오차 **1.28765e-5**, 쌍비 최대 상대오차 **2.58934e-5**; CED 6자리 인쇄 오차 범위 |
| 벽 | 벽 R*=입자 반경·선언된 유한 E/ν, γ_W=.0256ρ, 코팅 전후 같은 세계 | 위 192 덱의 3개 입자–벽 쌍 포함 |
| 겹침 | 9쌍 δ0/min(r), 혼합쌍 제한점 ρ10/Bo800, 천장 검사 삭제 변이 | 정상 표 최대 **0.00160539**; 과천장 입력 거부; 삭제 변이 MXD03에서 실패 |
| `_require_dens_gen` | None 세대, 직접 벽 값, ρ/γ 불일치 | 실제 deck·메타 경로 거부 |
| `deck_meta`, `deck` | 스키마/등록전/입력 Bo/hash, schema·Bo 상수 변이, 벽 문구 | 정상 192개 일치; 해당 변이 실패. 호출 인자↔text 결합의 범위는 아래 한계 |

자체 selftest는 패치에서 **154/154 PASS**. 변이 **10개 중 7개 포착, 3개 생존**이다. 생존은 R1의 D2 전용 중력과 R4의 scalar CLI 두 개다. gen1 밀도 강제·메타 Bo 상수·혼합쌍 검사 삭제·스키마 복귀·이름 정규식 복귀는 각각 관련 MXD 시험에서 실패했다. 전체 중력/반경 변이는 기존 골든도 실패했고, 반경 변이는 새 MXD02도 실패했다. 이 결과를 전체 저장소 게이트나 실행 물리 검증으로 확대하지 않는다.

## 추가 경계와 한정

아래는 패치가 새로 도입한 결함으로 분류하지 않았다. 현재 호출 계약·후속 되읽기 범위에 명시할 내용이다.

1. **메타는 입력 text 신원을 검증하지 않는다.** Bo .73 덱 문자열을 Bo12.5 팔·계획과 `deck_meta`에 주면 `deck_sha256`은 그 실제 문자열과 맞지만 `adhesion_rule.bo_se=12.5`가 된다. 출력 SI Bo는 .7299906001321019다. docstring이 메타를 “생성기 산술”, 독립 확인을 `mixer_deck_readback.py`로 구분하므로, 이번 생성기 패치만으로 인증 결합까지 닫았다고 주장할 수 없다.
2. **밀도 세대 라벨과 호출자 변조 계획의 표를 다시 결합하지 않는다.** `plan(...dens_gen='lab20261014')`의 `dens`를 gen1 표로 바꾸면 deck/meta는 계속 `lab20261014`라고 적으면서 SE 2000 kg/m³/2.0 g/cm³를 발행한다. 정상 `plan()`·CLI에서는 재현되지 않는다. `_require_dens_gen`의 보장은 세대 필드 존재이며, 임의 계획 사전의 무결성 보장이 아니다.
3. **정적 여유는 점착 지배 무하중 δ0 범위다.** ρ1, lab, CGF151.4, soft, Bo1015.4211813368634 덱은 SE–SE δ0/r=0.009999866799323059로 발행된다. 한 SE 중량을 지탱하는 작은 해석 접촉에서 `Aδ^(3/2)−Bδ−mg=0`의 해는 δ/r=0.010019533792156731이다. 실제 SJKR 동역학 결과가 아니며 정본에 이미 있는 “점착 지배·고립 접촉 근사”를 벗어난 추가 하중 반례다. 따라서 생성기 천장 통과를 중력 하중·접촉망·운동 상태 전체의 1% 보장으로 쓰지 않는다. 새로운 안전여유 정책은 여기서 정하지 않았다.
4. **구조 오류의 일부는 traceback형 예외다.** 혼합형 gamma 키는 `sorted(keys)`에서 TypeError, `register_arm`의 list/None은 AttributeError, 빈 팔은 이후 KeyError를 낸다. 실제 덱은 발행되지 않아 조용한 수용은 아니지만, 모든 잘못된 라이브러리 입력이 SystemExit라는 전칭은 성립하지 않는다. 기본 CLI에는 해당 사전 구조가 없다.

MXD2-01의 되읽기·덱 비교·스모크 구현, MXD2-06 웹앱 이력, MXD2-07 D3 문서는 이 generator diff의 변경 범위 밖이다. 이 보고서는 이들을 닫는 판정이 아니다.

# MXD2 소비자 독립 공격 리뷰 — 2026-10-24 KST

**판정: frozen v3의 개발용 소비자 수정은 검토 범위 안에서 GO.** 현재 D2 설계·정책에 대한 사용자의 비준은 주어졌다. 이 판정은 새 코호트 등록, D3 보정 수치, WSL/DEM 실행 증거나 외부 실행 GO를 대신하지 않는다. 전체 게이트·통합 커밋·push는 이 리뷰 범위 밖이다.

기준은 `486a57cf58d3e0d93ef79be6aae50968929099c0`의 [논지](../hetero_thesis.md), [D2 설계](../mixer_paper_pipeline_draft_20261013.md), [벽 결합 유도](../mixer_d2_wall_gamma_derivation_20261014.md), [밀도 세대](../density_generations_20261014.md)와 실제 코드다. 구현자의 완료 주장으로 판정하지 않았다. 리뷰어는 구현 소스를 수정하지 않았고, 별도 사본에서 합성 덱과 메모리 내 검증 조건 변이만 실행했다.

## 검토한 코드

| 파일 | 최종 SHA256 |
| --- | --- |
| `scripts/mixer_deck_readback.py` | `bfeaf8497048360ba328cb1a01575f2c2f7573d93e7627f53e535da73b8874d3` |
| `scripts/mixer_deck_diff.py` | `9a86950434b4abe852a6e3411fa809e78eef3d5ef6d7c8e125fb694cc1582877` |
| `scripts/mixer_smoke_blind.py` | `83760d9d81e4b2b6cf2d4ae7eda7f140dbec87cadc836b82079b1fd64f15dd4a` |
| `scripts/test_mixer_d2_consumers.py` | `a5014bf3f5349b6f6569586141d3f4e4447b1c0cc767343a5a487d3ce822c5a9` |

기준 생성기 SHA256은 `661936b78c3d60794714a63102f5461f7f42f581a5ad7da466c7c6fe0465bc27`이다. v3는 v2 소비자 코드 그대로이며 천장 검사 회귀만 추가했다. 단계별 diff·의존 파일·기준 설계 blob 해시는 [source manifest](codex_mxd2_consumers_independent_evidence_20261024/source_manifest.json)에 있다.

## 발견과 재검증

### 1. v1의 명령 생명주기 누락 — v2에서 해소 확인

두 덱에 같은 변경을 가하고 SHA256·바이트 수를 실제 덱에 맞춰 갱신했을 때 다음 네 반례가 v1의 readback, pair diff, planned-count 소비자에서 모두 PASS였다.

| 실제 덱 변경 | 의미 | 최종 코드 근거 |
| --- | --- | --- |
| `unfix insA`를 첫 `run 1` 앞으로 이동 | 입자 삽입 전에 해당 fix 제거 | `mixer_deck_readback.py:1171` |
| `nve/sphere` fix 삭제 | 평구 적분기가 없는 계획 | `mixer_deck_readback.py:1132` |
| `move/mesh` 셋을 첫 run 앞으로 이동 | 정착 전 회전인데 정착→회전 계획으로 판독 | `mixer_deck_readback.py:1157` |
| 삽입 region 참조를 `no_such_region`으로 변경 | 존재하지 않는 구역 참조 | `mixer_deck_readback.py:1165` |

v2의 `_d2_lifecycle`은 지원하는 명령의 정의·참조·순서를 검사한다(`mixer_deck_readback.py:1104`, 호출 `:1257`). 독립 재현에서 네 반례가 세 소비자 모두 FAIL로 바뀌었다. 정상 대조는 PASS, 벽 mesh 삭제 대조는 계속 FAIL였다. **6사례·18호출 기대 일치**다. [v1 red](codex_mxd2_consumers_independent_evidence_20261024/results/lifecycle-v1-red.json), [v2 green](codex_mxd2_consumers_independent_evidence_20261024/results/lifecycle-v2-green.json).

실행 권한 필드는 반례가 통과하던 v1에서도 False였다. 실제 시뮬레이터를 실행해 관측한 결과가 아니라, 지원한다고 선언한 개발용 덱의 구조 검증 결함을 확인한 것이다.

### 2. 겹침 천장 검사의 회귀 공백 — v3에서 해소 확인

v2에서 CED 전체를 ×100, metadata의 Bo를 ×100³으로 바꾸고 해시도 갱신하면, 정상 소비자는 정확히 `static pair overlap exceeds 1%`로 거부했다. 이 조건 하나만 메모리에서 제거하면 같은 덱이 PASS인데 기존 13개 시험 방법은 모두 통과했다. 종전 CED 변형은 절대 Bo 불일치에서 먼저 거부되어 천장 검사를 보호하지 못했다.

v3의 `test_mixer_d2_consumers.py:140`은 일관된 CED/Bo 변형과 실제 천장 실패 사유를 검사한다. 동일한 독립 변이를 다시 적용했을 때 시험이 실패했다. 생산 코드의 천장 계산을 바꾼 것은 아니다. [v2 공백](codex_mxd2_consumers_independent_evidence_20261024/results/mutations-v2-ceiling-gap.json), [v3 검출](codex_mxd2_consumers_independent_evidence_20261024/results/mutations-v3-portable.json).

중력 벡터 검사 제거가 v1 시험에서 살아남는 공백도 독립 확인했다. v2에 추가된 벡터 반전 회귀는 이 변이를 잡았다. [v1 결과](codex_mxd2_consumers_independent_evidence_20261024/results/mutations-v1-gravity-gap.json).

## 실제 실행한 확인 범위

| 확인 | 결과와 범위 |
| --- | --- |
| 독립 합성 덱 행렬 | 90사례·249호출, 기대와 다른 판정 0. 이 중 2사례·6호출은 아래 한정 사항의 관찰이며 PASS/FAIL 정답을 부여하지 않았다. |
| 정상 조합 | 48조합: AM_P+AM_S+SE / AM_P+SE, gen1 / lab20261014, 강성 1 / 20, ρ=.25 / 1 / 3, 층상 / 균일. 구현자의 기본 N·CGF·seed·Bo와 다른 N=100003, CGF=125, seed=49979687, Bo=1.125 사용. |
| 실제 공통 덱 변형 | 두 덱의 잘못된 밀도, 중력 크기·벡터·group, 수량, 반지름, CED, 중복 명령, Unicode·underscore 숫자, NaN·Infinity, 끊어진 해시/metadata를 거부. 한쪽 기하 변경도 pair diff에서 거부. |
| 기존 계약 | 기존 gen1 LC→LH의 B 비교는 PASS. D2 덱을 A/B/U/E/EB로 보내면 FAIL. |
| 최종 소비자 시험 | frozen v3의 `python -I scripts/test_mixer_d2_consumers.py`: 13개 unittest 방법 PASS. 하위 반복을 13개의 독립 물리 실험으로 세지 않았다. |
| 최종 기존 자체시험 | frozen v3: readback 24/24, diff 55/55, smoke 전체 PASS. 네 명령 모두 rc 0. [명령·시각·rc](codex_mxd2_consumers_independent_evidence_20261024/logs/results.json). |
| 유효 검증 조건 변이 | 9/9 검출: 해시, 절대 Bo, 중력 벡터, 비CED 동일성, ASCII 어휘, 겹침 천장, 실제 수량, 실제 밀도 세대, 명령 생명주기. 각각 정상 조건에서는 독립 반례 FAIL, 그 조건을 제거하면 PASS임을 먼저 확인했다. 시험 실패로 검출했고 예외 오류는 0. 디스크 소스 바이트는 전후 동일. |

독립 행렬·생명주기 시험은 v2에서 실행했으며 v3의 세 소비자 SHA256이 같음을 대조했다. v3에서는 회귀·자체시험·변이 시험을 직접 실행했다. 이 둘을 소급해 같은 실행으로 표기하지 않았다.

초기 사본에는 기존 자체시험이 요구하는 STL과 커밋된 DEV 덱들이 빠져 diff/smoke가 실패했다. 이는 소스 결함으로 세지 않았다. 기준 핀의 정확한 fixture를 보충한 뒤 재실행했고, 최초 실패 로그도 [historical](codex_mxd2_consumers_independent_evidence_20261024/historical/)에 보존했다. 최초 변이 도구의 해시 메시지 오기 역시 수정 전 결과를 버리지 않고, 효과가 입증된 재실행만 최종 수에 포함했다.

## 남은 경계

- `registered=None`, `execution_authorized=False`가 유지된다. planned counts는 덱에서 해석한 계획이며 실제 삽입 성공, 관측 입자 수, 접촉·혼합·유동성 결과가 아니다.
- 두 덱의 동일한 임의 기하 변경은 현재 미등록 개발 입력으로 수용된다. 구역 문법·참조·순서와 두 덱 간 동일성은 검사하지만 실제 STL 형상이나 특정 등록 기하 수치는 인증하지 않는다.
- `meta.seed`는 첫 삽입 seed와 대조된다(`mixer_deck_readback.py:1066`). 두 번째 삽입 seed를 두 덱에서 같이 바꾸면 PASS다. 이를 전체 등록 seed signature 검증으로 부를 수 없다. 현 미등록 경로의 명시 한정으로 남겼으며 기존 등록 코호트의 seed 검증을 완화한 것은 아니다.
- 현재 설계·정책 비준과 별도로, 새 코호트의 구체적 이름·수치·기계 입력 및 필요한 실제 실행 자료는 아직 제공되지 않았다. 이 리뷰로 MXD2 전체 원장이나 D3 수치 정책을 닫지 않는다.

재현 명령과 결과 파일 설명은 [증거 README](codex_mxd2_consumers_independent_evidence_20261024/README.md)를 따른다.

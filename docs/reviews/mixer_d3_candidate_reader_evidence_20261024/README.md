# [믹서 D3] 유한 후보 판독기 구현 증거 — 2026-10-24 KST

> 현재 canonical 전체 gate: **PASS, 155/0, rc 0**. [완료 기록](completion.md)을 따른다. 아래 작성자/초기 반입 시점의 예정·대기 문구는 원 스냅샷의 범위이며 현재 상태를 대신하지 않는다.


사용자 “계속 진행”·“다 비준이야”로 제시된 V2-Q1–Q4 정책을 비준한 뒤 작성한 실제 결정 판독기다. 입력 숫자는 모두 합성이며 실제 DEM·실험 런은 0건이다. 사전등록·물리적 적격성·통계 추정·실제 seed 미사용을 새로 인증하지 않는다.

## 소스와 실행

| 파일 | SHA-256 |
|---|---|
| `scripts/mixer_d3_candidates.py` | `ea4528156e8eb9762999fef0643985bebf0b0735691202fddb4a2c17814ee7f8` |
| `scripts/test_mixer_d3_candidates.py` | `12155f4e420ea3b15529501562b9fd6758c2767cbfcf4e1c79d6cdd7f4034d4c` |

후속 독립 지적에 의해 바뀌면 원 보고서와 당시 소스를 보존하고 최종 지문을 갱신한다. 다음은 저장소 루트에서 실행한다. 출력은 새 scratch 경로를 사용한다.

```bash
python3 -I scripts/test_mixer_d3_candidates.py
python3 -I scripts/mixer_d3_candidates.py \
  --contract docs/reviews/mixer_d3_candidate_reader_evidence_20261024/author/synthetic_example/contract.json \
  --observations docs/reviews/mixer_d3_candidate_reader_evidence_20261024/author/synthetic_example/observations.json \
  --out /absolute/new/scratch/result.json
python3 -I docs/reviews/mixer_d3_candidate_reader_evidence_20261024/author/run_mutation_probe.py \
  --reader scripts/mixer_d3_candidates.py \
  --tests scripts/test_mixer_d3_candidates.py \
  --out /absolute/new/scratch/mutations
```

## 실제 관찰과 범위

| 단계 | 실제 결과 | 원 로그/증거 |
|---|---|---|
| 첫 시험 작성 | SyntaxError 1. 시험 파일 괄호 오류 수정; 기능 red로 세지 않음 | `author/history/test-authoring-syntax-error.log` |
| 신규 기능 전 red | reader 파일 부재로 import 실패. 기존 구현의 의미 결함이라고 주장하지 않음 | `author/history/tests-first.log` |
| 최초 구현 | system Python 3.12, 23 unittest PASS; 크기 제한 뒤 24 PASS | `author/history/green-initial.log`, `author/history/green-bounded.log` |
| 독립 D3IR-01 red | 극단 JSON 지수에서 Decimal 예외가 계약오류로 처리되지 않음. 회귀 추가 후 27개 중 1 failure·1 error | `author/independent-r1-red.log`, `author/independent-r1-red-source/` |
| D3IR-01 수정 | Python 3.11.17, 27/27 PASS | `author/independent-r1-green-py311.log` |
| 작성자 추가 reason 회귀 | 선택 reason의 타입/내용을 무시하지 않도록 신규 시험, 수정 전 KeyError | `author/author-reason-red.log` |
| **현재 직접 회귀** | **Python 3.11.17, 28/28 PASS**. 그 안의 보정 상태 81조합·검증 상태 81조합은 서로 다른 집합 | `author/green-v2-py311.log` |
| **작성자 변이** | **12/12를 해당 assertion에서 검출**, 문법 유효·예외 error로 죽은 변이 0 | `author/mutation-v2/mutation-results.json`, 각 `mutants/*/test.log` |
| **실제 CLI** | rc0, 합성 후보 2개·all-compatible, `execution_ready=false`, 입력/reader SHA 기록 | `author/synthetic_example/receipt.json`, `result.json`, `cli.log` |
| **독립 코드 후속** | **입력 조건부 계산기 범위 PASS**. 독립 명명 검사 19/19(그중 세 점×두 보정 시험의 729조합), 독립 변이 10/10을 관련 assertion에서 검출 | `independent/RECHECK-v3.md`, `independent/recheck-v3-receipt.json` |
| 저장소 전체 gate | **PASS — 155/0, rc 0; 현재 완료 기록 참조** | `full_gate_receipt.json` |

검증 81조합의 집계 분포는 all-compatible 1, mixed 6, none-compatible 9, incomplete 65다. 이는 후보 2개×필수항목 2개의 세 상태를 전수 열거한 합성 의미 시험이며 전체 과학 입력 공간의 완전성을 뜻하지 않는다.

12 변이는 strict boundary, 교집합→합집합, 미평가 무시, 검증 뒤 S 축소, 알 수 없는 후보 허용, 출처 digest 신뢰, 예약 seed 허용, 미평가 간극 연결, 빈 집합 성공, 단위 불일치 무시, 평탄 응답 자동 미평가, 이진 float 경계다. 각 변이는 고정 소스를 한 군데 바꾸고 특정 실제 회귀를 실행했다. 작성자 검사이며 독립 공격 결과와 합산하지 않는다.

초기 v1 명령/결과와 작성 중 오류는 `author/history/`에 그대로 보존한다. 현재 소스 검증은 위 최종 지문과 연결된 py3.11 회귀·mutation-v2·synthetic_example을 사용한다. 전체 gate는 기존 게이트 단계 수를 그대로 쓰며 새 reader 시험을 자동 포함한다고 주장하지 않는다.

독립 최종 재확인은 위 두 소스 지문과 계약 문서 지문에 결합한다. 유효한 D3IR-01 극단 지수 오류는 해소됐다. D3IR-02(Bo_po 누락)는 검토 시점/필드명 혼동으로 **검토자가 철회한 오탐**이며 수정 완료 건수에 넣지 않는다. 최초 `REVIEW-v1.md`, 오류가 있던 probe/출력, `ERRATUM-D3IR-02.md`, 정정 출력, 최종 `RECHECK-v3.md`를 바이트 그대로 보존했다. 독립 manifest의 92개 파일을 복사 뒤 다시 확인했다.

독립 결과의 한정도 유지한다. 실제 원자료 수치 추출 일치·물리적 적격성·불확도 추정·실제 사전등록·맹검·외부 GO는 이 계산기 검토가 인증하지 않는다. 전체 gate와 웹앱 실제 반입 검사는 root 통합 단계에서 별도 기록한다.

현재 전체 게이트 PASS는 같은 후보의 **순차 재검증** 결과다. 이전 병렬 시도는 **154 PASS / 1 FAIL, rc 1**(기존 300초 시간 초과)이었으며 원본을 보존했다. [실패 이력과 현재 완료 기록](completion.md)을 함께 읽는다.

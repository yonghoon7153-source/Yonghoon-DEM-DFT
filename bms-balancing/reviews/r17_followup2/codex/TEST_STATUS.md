# 독립 시험 상태 — a4c311ef

## 실제 실행 결과

| 시험 | 결과 | 근거 |
|---|---|---|
| 전체 `python -m pytest tests/ -q` | **344 passed, 108 failed, 4 warnings**, 980.88초 | full_scoped.log/xml/json |
| R17 followup + R17 + R16 receipt + chain-rule | **68 passed, 3 failed**, 65.99초 | focused_scoped.log/xml/json |
| 신규 followup 파일만(위 집중 실행의 집계) | **25 passed, 1 failed** | test_fu_03이 fcntl 부재 |
| chain-rule 파일만(위 집중 실행의 집계) | **9 passed** | focused_scoped.xml |
| 원래 반례·인접 입력 독립 재현 | **47 case** 실행, 관측 checker **63/63** | REPRO_RESULTS.json / OBSERVATION_CHECK.json |
| 실제 fit_cycles API → reader, 합성 2사이클 | measured 2행, 일반 schema 문제 0, **reader rc 2** | PRODUCER_READER_RESULTS.json |
| 같은 값에서 row receipt cycle만 제거한 축 분리 대조군 | **reader rc 0** | 위 JSON의 control_without_row_cycle |
| 현행 out schema-only | **rc 0**, promotion_eligible=false | current_schema.log/json |
| legacy out schema-only | **rc 2**, 52/25/10/1 | legacy_schema.log/json |

pytest 실제 인자는 `-p no:cacheprovider`, JUnit 경로, 고유 검토 전용 `--basetemp`를 추가했다. 실행 명령 전체는 각 command JSON에 있다. 발신 측 Linux 전수 결과를 Windows 재현 성공으로 대체하지 않았다.

## 108 실패의 분리

이는 trace에 근거한 분류이며, 해당 원인 뒤에 있을 다른 결함이 없다는 증명은 아니다.

| 범주 | 수 |
|---|---:|
| 실패 trace의 ModuleNotFoundError: fcntl | 80 |
| bash/Unix shell 실행 파일 부재 | 16 |
| symlink 생성 권한 | 1 |
| Windows에서 불가능한 `a -> b.csv` 파일명 | 1 |
| `/` vs `\\` 경로 문자열 assertion | 2 |
| 원인 미확정 — 환경 문제로 단정하지 않음 | 8 |

집중 시험의 세 실패는 `test_fu_03`, `test_r17_01`, `test_r17_02`이며 모두 생산자 `record_partial`의 fcntl import에서 멈췄다. 독립 GC 재현은 합성 index를 직접 작성해 **실제 gc_partial CLI**를 호출했으므로 그 장애와 분리된다. Linux 동시 게시 잠금을 시험했다고 주장하지 않는다.

이전 Windows 318 passed/108 failed와 비교하면 이번은 344 passed/108 failed다. 수가 같다고 같은 실패 집합은 아니다.

- 신규 `test_fu_03` 1건이 fcntl에서 실패했다.
- 이전 미확정 `test_e11_10`은 **이번 실행에서는 통과**했다. 원인이 밝혀졌거나 코드 수정으로 닫혔다는 판정은 아니다.
- 나머지 기존 실패 107건은 남았다. 비교 근거는 `FULL_TEST_DELTA.json`이다.

미확정 8건:

1. test_d10_12_closure_runners_fail_closed_when_assertions_are_off
2. test_d10_13_closure_runners_seal_the_bytes_they_execute
3. test_d10_14_package_byte_corruption_stops_the_runner_and_the_regression_sees_it
4. test_e11_17_skip_worktree_is_detected
5. test_e11_18_expected_head_must_be_the_full_object_id
6. test_d8_07_r7_closure_runner_records_whether_each_probe_reached_its_counterexample_assertion
7. test_d9_08_r7_runner_rejects_unknown_empty_or_duplicate_probes_and_wrong_head
8. test_r4_06_concurrent_profiles_publish_their_own_rows_with_run_ids

반환 rc 0/빈 출력, JSON 미수신, index flag 관측 실패, barrier 대기 실패 등을 그대로 보존했다. full 로그에는 subprocess pipe UnicodeDecodeError 관련 thread 경고도 4건 있다. 이 경고만으로 위 모든 실패의 원인을 확정하지 않는다. Linux 실행 로그가 Windows의 이 실패를 설명한다는 주장도 하지 않는다.

## 환경·식별·범위

- Windows / Python 3.12.14 / numpy 2.5.3 / scipy 1.18.1 / pandas 3.0.6 / openpyxl 3.1.5 / pytest 9.1.1.
- HEAD `a4c311eff898615932ae6f333bbb26b605abf762`; tree `a5bf03ae4c98a0a6c871b041f3e596ef8b21715d`.
- 독립 재현 두 스크립트는 전체 pytest가 종료된 뒤 다시 실행했다. 최종 소스 식별/깨끗한 git status는 REVIEW_IDENTITY.json에 있다.
- checkout raw SHA와 git blob SHA, CRLF→LF 정규화 동일 여부를 별도로 남겼다. 정규화 동일을 원문 바이트 동일로 바꾸지 않는다.
- 최초 기본 임시 디렉터리 정리 실패/중단·검토 스크립트의 콘솔 인코딩 오류는 EXECUTION_NOTES.md에 기록했다. 이를 제품 결함이나 전수 완료 수치로 합산하지 않는다.
- 전수의 기존 환경 실패와 독립 반례 F2-01~06은 다른 집합이다. NO-GO 근거는 재현된 여섯 조건이며, 108개를 새 결함 108건으로 세지 않는다.

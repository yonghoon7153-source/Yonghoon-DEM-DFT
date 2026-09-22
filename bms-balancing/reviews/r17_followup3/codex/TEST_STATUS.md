# 독립 실행 결과 — e834b01e

## 실측

| 명령/범위 | 결과 | 근거 |
|---|---|---|
| 전체 `python -m pytest tests/ -q` | **357 passed · 110 failed · 26 errors · 4 warnings**, 1048.63초, rc 1 | full.xml / full.stdout.bin / full.stderr.bin / full.json |
| 위 실행 중 `tests/test_r17_followup2.py` | **13 passed · 2 failed · 26 errors**, 합계 41 | TEST_RESULTS.json |
| 원래 반례 재현기 | **47 case 실행 완료** | REPRO_RESULTS.json / old-repros.json |
| 원래 실제 producer 재현 | 합성 2사이클 measured, check_rows 문제 없음, **reader rc 0** | PRODUCER_READER_RESULTS.json / producer.json |
| row receipt에서 cycle 제거한 대조군 | **rc 2** | 위 JSON |
| 새 GC 반례 | 변경된 바이트 삭제 rc 0, 없는 최신 결과를 남기면서 이전 유일 payload 삭제 rc 0 | NEW_FAST_RESULTS.json |
| 새 정상 starts 비교 | 실제 API starts 1/2 각각 reader rc 0, `--axis starts`와 `--axis n_multistart` 각각 rc 2 | NEW_PRODUCER_RESULTS.json |
| 새 typed receipt 반례 | code=null / instrument=list 각각 AttributeError·rc 1·구조화 판정 없음 | NEW_FAST_RESULTS.json |
| 저장된 주요 관측 재검산 | **59/59**. 제품 GO가 아니라 관측 일치 검사 | OBSERVATION_CHECK.json |
| 현행 out schema-only | **rc 0**, promotion_eligible=false, env_contract_legacy=13, baseline_absent=1 | schema.json / schema.stdout.bin |
| legacy schema-only | **rc 2**, schema/provenance_cols/content/provenance = **52/25/10/1** | legacy.json / legacy.stdout.bin |

전체 pytest의 추가 인자는 `-p no:cacheprovider`와 JUnit 출력 경로다. 실행별 전체 argv·cwd·환경은 command JSON에 있다. pytest 임시 부모를 이번 검토 전용 새 디렉터리로 두었다. 전체 시험과 독립 재현이 일부 동시에 돌았으므로 실행 시간을 단일작업 성능 benchmark로 사용하지 않는다.

발신 측 **Linux 493 passed**를 이번 Windows 결과로 재현했다고 쓰지 않는다. 이번 수집 합계는 493이다. 최초 wrapper 콘솔 출력의 인코딩 오류와 리뷰어 probe 인자 실수는 EXECUTION_NOTES.md에 따로 기록했다.

## 136개 비통과 결과의 trace 분류

| 직접 관측한 범주 | 수 |
|---|---:|
| ModuleNotFoundError: fcntl | 108 |
| bash/Unix shell 실행 파일 부재 | 16 |
| symlink 생성 권한 | 1 |
| Windows에서 불가능한 파일명 | 1 |
| `/`와 `\\` 경로 문자열 assertion | 2 |
| 원인 미확정 — 환경 문제로 단정하지 않음 | 8 |

직전 a4c311ef의 108개 실패가 **모두 그대로** 남았다. 새로 비통과한 28개는 전부 새 `test_r17_followup2.py`에 속하며 fcntl에서 막힌다. 그중 producer fixture 준비가 실패해 **26 errors**, GC 테스트의 부분 게시 helper가 실패해 **2 failures**다. 이는 새 validator의 해당 분기까지 실행했다는 증거가 아니다. 그 축은 원래 독립 재현기·이번 합성 index/실제 API 재현으로 따로 확인했다. fcntl을 mock하여 전체 게시가 성공한 것처럼 만들지 않았다.

직전 344 passed/108 failed → 이번 357 passed/110 failed/26 errors. pass 증가는 새 파일의 13개다. 기존 실패가 해결됐거나 새로 악화됐다는 숫자 해석은 하지 않는다. 비교한 이전 evidence SHA 및 개별 nodeid는 TEST_RESULTS.json의 delta에 있다.

미확정 여덟 건은 직전과 같다:

1. test_d10_12_closure_runners_fail_closed_when_assertions_are_off
2. test_d10_13_closure_runners_seal_the_bytes_they_execute
3. test_d10_14_package_byte_corruption_stops_the_runner_and_the_regression_sees_it
4. test_e11_17_skip_worktree_is_detected
5. test_e11_18_expected_head_must_be_the_full_object_id
6. test_d8_07_r7_closure_runner_records_whether_each_probe_reached_its_counterexample_assertion
7. test_d9_08_r7_runner_rejects_unknown_empty_or_duplicate_probes_and_wrong_head
8. test_r4_06_concurrent_profiles_publish_their_own_rows_with_run_ids

전체 log의 subprocess pipe UnicodeDecodeError 관련 경고 4건도 보존했다. 이것만으로 미확정 여덟 건의 원인을 전부 설명했다고 쓰지 않는다. 분류는 trace에 나타난 첫 원인일 뿐, 그 뒤에 다른 코드 문제가 없다는 증명이 아니다.

## 대상·환경·범위

- HEAD `e834b01e4066c5e78c06b6ed1f77878e5a27a481`, BMS fix `7f09804fdc6be2892746dece201b98da48aac6cd`.
- Windows / Python 3.12.14 / NumPy 2.5.3 / SciPy 1.18.1 / pandas 3.0.6 / openpyxl 3.1.5 / pytest 9.1.1.
- 마지막 git status는 clean, 최초 식별한 검토 소스의 변경 0. 실제 checkout bytes와 git blob bytes 및 LF 정규화 대조는 FINAL_IDENTITY.json.
- 기존 재현기 둘의 바이트는 이전 검토와 같다. 실제 producer API는 합성 workbook만 썼고, CSV 게시 직렬화는 리뷰어 소유 코드였다. Linux 잠금/게시 전체 성공 주장은 없음.
- 이번 NO-GO의 세 독립 결함과 전수의 Windows 환경/미확정 실패 집합은 다르다. 원자료 재적합·생산 코드 수정·commit/push·COMSOL 실행 없음.

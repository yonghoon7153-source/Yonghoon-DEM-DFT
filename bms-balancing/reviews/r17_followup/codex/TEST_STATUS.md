# 실행 상태 — R17 후속 7c8f61f9

2026-09-22. Windows / Python 3.12.14에서 직접 실행했다. 대상은 `7c8f61f943199c3782bf3c3d81f6b573aa0a1b79`의 `bms-balancing/`이다. 작성자 환경의 **426 passed를 이 기계에서 재현하지 못했다.** 아래 실패를 PASS나 skip으로 바꾸지 않았다.

## 결과

| 검사 | 직접 관측 | 근거 |
|---|---|---|
| 전체 `python -m pytest tests/ -q` | **318 passed, 108 failed, 4 warnings, 952.84초**, rc 1 | full.log / full.xml / full.json |
| R17 + chain-rule + widths 표적 3파일 | **56 passed, 3 failed, 151.09초**, rc 1 | targeted.log / targeted.xml / targeted.json |
| chain-rule 9회귀 | 위 표적·전체 실행에서 9개 모두 통과 | JUnit testcase 결과 |
| 독립 유한차분 대조 | legacy 최대 오차 0.37083333345545677, v2 4.0270053958124663e-10, rc 0 | derivative_independent.log / .json |
| `check_u14 --new out --schema-only` | rc 0, promotion=false | current_schema_recheck.log / .json |
| `check_u14 --new out/archive/legacy_r6_u14 --schema-only` | rc 2, schema 52 / provenance_columns 25 / content 10 / provenance 1 | legacy_schema.log / .json |
| `check_u14 --new out --old-rev 42314198e0beee59834d394cdba2757183503b59` | rc 4, legacy_transition_approved=true, promotion=false | old_revision.log / .json |
| 리뷰 합성 반례 및 양성·음성 대조군 | 스크립트 정상 종료, 잘못된 수용/삭제/폭 계산을 실제 관측 | REPRO_RESULTS.json 및 case별 로그 |

표적 시험은 전체 시험의 부분집합이므로 통과 수를 합산하지 않는다. pytest 시간과 바깥 runner가 재는 프로세스 시간은 범위가 다르다. 정확한 argv/cwd/rc/시각은 각 JSON에 있다. 캐시 비활성화와 리뷰 폴더의 basetemp/JUnit 경로만 pytest 실행 옵션에 추가했다.

구형 archive의 52/25/10/1은 과거 회차의 40/25/6/1과 다르다. 현재 코드에서 관측한 값으로 남기며 과거 숫자로 덮지 않는다. canonical out의 tree는 `1da2e9f5600dc5f91dd0a989188ef7b0ecb19437`로 보존돼 있다. schema-only rc 0은 승격 또는 실데이터 수치의 과학적 정답 판정이 아니다.

## 실패 108건의 분류와 미확정 범위

`FULL_TEST_TRIAGE.json`은 실패 trace를 다음과 같이 분류했다. 이는 모든 실패의 독립 원인 규명 결과가 아니다.

| trace에서 관측한 분류 | 건수 | 주장 가능한 범위 |
|---|---:|---|
| fcntl 부재가 직접 또는 subprocess trace에 나타남 | 79 | 해당 실패에서 POSIX 모듈 부재를 관측. 이를 해결하면 모두 통과한다고 입증하지 않음 |
| bash 호출 WinError 2 | 16 | 이 실행 환경에서 해당 명령을 찾지 못함 |
| symlink 생성 WinError 1314 | 1 | 해당 링크 생성에 필요한 권한 부재 |
| Windows에서 만들 수 없는 `a -> b.csv` 이름 | 1 | fixture 파일 생성 실패 |
| POSIX/Windows 경로 구분자 assertion | 2 | 기대 문자열과 실제 경로 표기 불일치 |
| **원인 미확정** | **9** | 환경 탓으로 확정하지 않으며 여전히 실패 |

원인 미확정 9건은 다음과 같다. 전체 traceback은 `full_failures.json`에 보존했다.

1. `test_d10_12_closure_runners_fail_closed_when_assertions_are_off`: 기대한 실패 대신 rc 0/빈 stdout.
2. `test_d10_13_closure_runners_seal_the_bytes_they_execute`: 기대 출력이 없어 NoneType 오류.
3. `test_d10_14_package_byte_corruption_stops_the_runner_and_the_regression_sees_it`: 기대한 실패 대신 rc 0/빈 stdout.
4. `test_e11_10_the_gate_is_isolated_before_it_is_imported_and_the_snapshot_bytes_are_checked`: forged pyc marker가 실제 존재하여 assertion 실패.
5. `test_e11_17_skip_worktree_is_detected`: 기대 index flag 검출 결과가 빈 목록.
6. `test_e11_18_expected_head_must_be_the_full_object_id`: 기대한 실패 대신 rc 0/빈 stdout.
7. `test_d8_07_r7_closure_runner_records_whether_each_probe_reached_its_counterexample_assertion`: 빈 출력의 JSON 해석 실패.
8. `test_d9_08_r7_runner_rejects_unknown_empty_or_duplicate_probes_and_wrong_head`: 기대 출력이 없어 NoneType 오류.
9. `test_r4_06_concurrent_profiles_publish_their_own_rows_with_run_ids`: 동시 실행 barrier 대기 실패.

이 중 runner 격리·index flag 검출 실패는 단순 계산 의존성 누락으로 축소할 수 없다. Windows의 process 재실행·경로 차이 또는 별도 코드 결함인지 이 리뷰에서 분리 확정하지 못했다. **지원 Linux 환경의 동일 SHA 전수 로그와 위 9개 항목별 설명/재현이 추가로 필요하다.** 상세 보고서의 새 P1 3건·P2 2건은 별도 합성 반례로 확인한 것이며 이 9건을 섞어 발견 수를 부풀리지 않았다.

표적 시험 실패 3건은 `test_r17_01`, `test_r17_02`, `test_w14`의 fcntl 부재다. GC 원 반례는 fcntl을 대체하거나 production을 고치지 않고, 동일 index 구조를 직접 만드는 별도 합성 fixture로 실행했다.

## 검토 환경과 검토 도구 자체의 이력

- Python 3.12.14, numpy 2.5.3, scipy 1.18.1, pandas 3.0.6, openpyxl 3.1.5, pytest 9.1.1. Linux와 의존성/OS가 같다고 주장하지 않는다.
- 첫 current_schema 실행은 대상 rc 0을 로그/JSON에 저장한 뒤 리뷰 runner가 Unicode 출력을 CP949 터미널로 재출력하는 단계에서 실패했다. 리뷰 runner의 stdout을 UTF-8로 고친 뒤 같은 대상 명령을 재실행해 `current_schema_recheck` rc 0을 얻었다. 이 wrapper 오류는 제품 결함으로 세지 않았다.
- 대상은 별도 checkout이며 production 수정·실데이터 재적합·실제 산출 재생성·COMSOL 호출·push는 없다. 시험이 만든 합성 데이터와 적합은 실데이터 작업과 구분했다.
- checkout HEAD/status와 주요 소스 hash는 `REVIEW_IDENTITY.json`에 기록했다. 제공 ZIP은 리뷰 문서·재현 코드·실행 증거만 포함하며 소스 checkout/합성 scratch/실데이터/MPH는 포함하지 않는다. 재현에는 고정 SHA checkout과 의존성이 별도로 필요하다.

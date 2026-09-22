# R17 시험 상태 — 2026-09-22

대상 dfc1fc78b3396c95709650860f1502c0e83ead40. 작성자 390 passed는 재인증하지 않았다.

| 실행 | rc / 결과 | 범위 |
|---|---|---|
| pytest_full | 1 / 904.938초 | 전체 tests/를 실행했지만 종료 정리에서 공용 pytest-current 접근 거부. 진행 출력에 F도 다수 있으며 최종 per-test 실패 내역/집계가 남지 않아 각각의 원인은 미분류. 이를 전부 환경 탓이라고 단정하지 않는다 |
| pytest_r15_r16 | 1 / 36.500초 | 첫 표적 시도도 같은 종료 정리 오류. 최종 집계로 사용하지 않음 |
| pytest_r15_r16_local | 1 / 61 passed, 3 failed / pytest 37.10초 | 전용 basetemp 사용. 실패 1개 Bash 없음, 2개 fcntl 없음. 정확한 이름은 로그/XML에 있음 |
| pytest_width_contract | 0 / 9 passed, 14 deselected / pytest 3.88초 | 빈값/폭 상태/비교 설정 관련 선택 회귀 |
| check_u14_current | 0 | schema-only. 승격 false |
| check_u14_oldrev | 4 | 승인된 과거 revision 정상 대조군. legacy true, 승격 false |
| check_u14_legacy_archive | 2 | 현재 계약에서 52·25·10·1. 과거 라운드와 계약 세대가 다름 |
| repro_r17.py | 0 | BAD 관측들이 예상대로 재현됐다는 assert. target이 올바르다는 PASS가 아님 |
| science_repro.py | 0 | 합성 논리 반례 및 알려진 chain rule 독립 확인 |

표적 회귀와 전체 시도가 겹친다. 61+9를 전수 통과 수에 합산하거나 중복 실행을 독립 시험 개수로 세지 않는다.
관련 로그·JSON·JUnit은 이 폴더에 보존했다. 전체 재실행은 Linux 지원 환경에서 필요하다. WSL/프로세스 조회의 접근 제한을 풀거나 fcntl을 stub으로 바꾸지 않았다.
pip은 격리 venv에만 설치했고 캐시 접근 지연 후 --no-cache-dir로 설치했다. 전역 Python·COMSOL·원격 PC 설정은 변경하지 않았다.


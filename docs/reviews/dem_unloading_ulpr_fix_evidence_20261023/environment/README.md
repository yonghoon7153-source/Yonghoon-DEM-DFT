# 환경 검증 이력

최초 전체 게이트는 venv Python의 realpath 실행에서 의존성을 잃고, 일부 launcher 교체 과정에서도 실패했다. `check-all-initial.log`는 그 실패를 보존하며 통과 증거가 아니다.

설치 스크립트는 venv의 python·python3·python3.11을 모두 실제 실행 파일로 설치하도록 수정했다. 해당 경로의 ca_ext_runner 재검증은 128 PASS이며 새 전체 게이트는 상위 `../full_gate_receipt.json`으로 별도 판정한다. 브라우저 결과는 당시 로컬 기본 웹앱 3페이지의 스모크이며 연구 실행 검증이 아니다.

미커밋 수정 상태의 다음 전체 게이트는 `check-all-uncommitted.log`에 보존한다(rc1). 키트 13명령과 별개로 저장소 전체 검사에서 legacy summary 핀, 임시 출력 경로, 추적 파일 clean 검사가 실패했다. 원인은 별도 재현으로 구분하고 최종 판정은 상위 receipt로 확인한다.

`wsl_network_smoke.py` 자체시험은 시험 전후 변경 비교가 아니라 `git status --porcelain --untracked-files=no` 전체가 비어 있어야 통과한다. 따라서 인계서 §2의 트랙별 게이트 계약(커밋마다 문서/원장 검사, 넘기기 전 전체 게이트)에 따라 검토된 수정안을 로컬 커밋한 뒤 깨끗한 상태에서 전체 검사를 수행한다. 전체 PASS 전에는 push하지 않는다. 게이트 구현·Git 상태·봉인·샌드박스의 .git 표지는 바꾸지 않는다.

임시 출력 경로 실패의 독립 재현은 `sigmae-triage-selftest.log`(32/58·rc1), 교정 재검증은 `sigmae-triage-tmpdir-selftest.log`(58/58·rc0)다. `/tmp`와 `/workspace`의 환경용 .git 표지 때문에 저장소 안 출력 금지에 걸렸다. 표지를 보존하고 승인된 작업 전용 `/var/tmp/codex-nonrint-20261023`를 TMPDIR로 사용했다. 현재 제한 샌드박스에서는 해당 경로 쓰기에 도구 실행 승인이 필요하다.

`coverage-pandas-compat/README.md` 및 원시 자료는 독립 환경 진단이다. pandas 3.1.0의 CSV 파싱에서 contacts.csv 10개 셀이 다르게 읽혀 반환 요약 2필드의 마지막 자릿수·SHA가 달라졌다. 현재/옛 코드 모두 같은 환경에서는 동일했고 full_metrics·per-AM CSV 핀은 원래부터 같았다. pandas 2.3.3+pytz 2026.5로만 바꾸고 NumPy 2.4.6을 유지하면 세 핀과 자체시험 16/16이 복원됐다. 이는 물리 수치의 참/거짓 판정이 아니라 기존 바이트 계약을 재현하는 환경 선택이다. root는 설치 스크립트에 이 버전을 고정하고 공유 venv 설치·필수 import·pip check를 재검증했다(`install-final-env-retest.log`, rc0). 이전 키트/독립 로그의 환경을 소급해 바꾸지 않는다.

최종 설치 환경의 키트 전체 재검증은 `final-env-suite/summary.json` 및 13개 로그에 보존했다. 13명령 모두 rc0이며 reader 214/gates 202 등 앞선 최종 키트 수와 같다. `final-constraints.txt`는 이 실행 및 다음 전체 게이트의 설치 버전 핀이다.

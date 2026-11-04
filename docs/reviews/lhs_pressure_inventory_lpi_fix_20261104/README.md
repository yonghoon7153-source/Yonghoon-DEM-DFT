# LHS 압력 재고 LPI-01/02 보강 후보 — 짧은 재확인 (2026-11-04)

**이번 수정 범위:** LPI-01의 출력 오류 재시도·flush·종료·shell fallback 경계, LPI-02의 시간 상한 부재 설명과 반례 보존.
**이번에 승인/종결하지 않는 것:** 실제 ibb/WSL 재고 실행·POSIX/Lustre 현장 자격·압력 적격성·단계 A·배포·전체 게이트 HOLD 해제. 외부 재확인 대기이며 자체 CLOSED가 아니다.

## 근거와 결정

외부 판정은 `docs/reviews/lhs_pressure_inventory_review_intake_20261104/external_verdict.md`이며 준비 핵심 수용·새 P1/P2 없음·P3 두 건이다. 원본 ZIP과 수령 때 재현 기록은 같은 수령 폴더에 보존했다. 그 폴더의 Q2 대기 표시는 당시 시점 기록이다. 이후 1저자가 “권고대로 고쳐”로 출력 경계 코드/문구와 시간 상한 한정만 비준했다. 이번 코드 수정의 입력은 수령 핀 `d3a8abc09dbd77ea4b19b2edbc60f7181322e595`; 처음 검토된 명령은 `c8a55c8ae1021ec80634ee8c6533deeebc67ce61`의 바이트다. 그 명령·README·해시 목록을 `before/`에 보존했다. `SHA256SUMS.before.txt`는 당시 전체 폴더의 목록 원문이며, 이 before 폴더의 부분 사본을 위한 검사 목록이 아니다. 현재 증거의 검사 목록은 이 폴더의 `SHA256SUMS`다.

## 변화

| 항목 | 고친 뒤 동작 | 남은 한계 |
|---|---|---|
| LPI-01 계산/직렬화 | stdout을 건드리기 전에 성공/고정 실패 payload를 확정 | 치명적인 런타임 실패는 JSON이 없을 수 있음 |
| LPI-01 출력 | JSON+개행 한 번 쓰기, short write 검사, 명시적 flush; 실패하면 rc2, JSON 재시도 없음 | 쓰기는 원자적이지 않음; 부분/완전 JSON이 이미 나간 뒤 실패할 수 있음 |
| LPI-01 종료 | CLI에서 명시적 flush 후 즉시 종료; 실패 버퍼의 interpreter finalization 재flush 방지 | import한 main만 별도 호출하는 외부 프로그램의 종료는 이 CLI 보장 범위가 아님 |
| LPI-01 shell | exec로 해석기를 실행, 비정상 종료 상태 전달, fallback JSON 제거 | 시작 실패·신호 종료 rc는 2 외의 비0도 가능 |
| LPI-02 | 크기 제한은 시간 제한이 아님을 README에 명시; 합성 느린 줄 반례 보존 | B7 regex·계수·등록 규칙 유지; 시간 상한을 추가한 수정이 아님 |

수신자는 **프로세스 rc0 + 완전한 JSON 한 개 + 최상위 INVENTORY_COMPLETE/rc0**를 모두 확인해야 한다. 실제 CLI의 Python stderr는 `/dev/null`로 보낸다. 외부 shell 자체 실행 실패·단말/OS 장애까지 일률적인 stdout/stderr 꼴을 보장하지 않는다.

## 시험 먼저와 검증

- `output_before.log`: 기존 명령에서 새 출력 시험 13개 실행·6 FAIL·rc1. 최초/부분 write 뒤 두 번째 JSON, short write의 거짓 성공, shell의 시작/부분/신호 실패 후 fallback을 잡았다. `before_source.json`에 소스·시험 해시를 보존했다.
- `direct_runs.json`: 수정 후 기존 재고 20개와 새 출력 13개를 **각각 실제 Python 3.11.17 및 3.8.20**에서 실행했다. 개별 결과·소스 SHA·로그는 그 JSON에 있다. 이들은 공용 게이트에 새로 연결하지 않았고 공용 검사 수에 합산하지 않는다.
- 초기 병렬 검사의 Python 3.11 기존 시험 중 `test_17_no_explicit_writes_or_external_processes`에서 expected rc0 / observed rc2가 한 번 나왔다. 원래 assertion에 파일별 사유가 없어 원인은 미확정이다. 소스·시험 변경 없이 해당 시험을 진단 실행하고 전체 20개를 순차 실행했을 때 통과했다. 초기 실패 로그와 `direct_runs_initial.json`, `audit_failure_diagnostic.log`를 보존하며 부하 탓이라고 단정하지 않는다.
- `mutations.json`: 출력 재시도 복원, flush 제거, 일반 종료 복원, short-write 검사 제거, shell fallback 복원의 다섯 변이를 동일 출력 시험으로 검출한다. 각 변이의 patch·해시·실패 로그는 `mutations/`에 있다. 변이본은 실제 연구 경로를 열지 않는 합성 child/fake interpreter에서만 실행한다.
- `scope_comparison.json`: main/CLI entry/shell을 제외한 원래 Python AST 및 B7 파일 바이트가 그대로인지 대조한다. LPI-02의 느린 입력은 고쳐진 척하지 않는다. 수령 때 실행한 120,019자/탐침 5초 제한 반례와 원본 파서 탐침은 수령 폴더에 있고, 이번 시간 측정을 새로 수행했다고 세지 않는다.
- 내부 좁은 읽기 검토는 코드·출력 시험에서 추가 필수 수정 없음. 외부 독립 종결과 구분한다.

임시 합성 파일·OS/IO 모의·실제 child 종료·fake interpreter shell만 검사했다. 기존 CLI 시험의 실제 cloud 신원은 거부되어 연구 root를 열지 않는다. 연구 ibb/WSL 접속·실제 로그 읽기·작업 제출·복사·전송은 하지 않았다.

## 재현과 전달

현재 명령과 두 시험 = `docs/reviews/lhs_pressure_inventory_20261104/`.
그 폴더에서 `python3 -I -B test_pressure_inventory.py`와 `python3 -I -B test_output_contract.py`를 실행한다. 출력 시험은 synthetic child에서 identity/inventory/stdout만 바꾸고 실제 entry 종료를 검증한다. `LPI_COMMAND`는 **시험 전용** 대상 선택이며 실제 재고 명령에는 가드 해제 옵션이 없다. 변이 재현은 같은 증거 폴더의 도구에 아직 없는 임시 출력 폴더를 지정한다: `python3 -I -B replay_mutations.py /tmp/lpi-synthetic-replay-new`. 기존 폴더면 거부하며 변이 코드·로그를 그 임시 폴더에만 쓴다. 이 검토의 명령은 실제 연구 실행 승인서가 아니다.

새 재확인 요청은 `review_request.md`; 전달 ZIP의 `PIN.txt`는 push된 이 수정 커밋이다. 과거 준비 ZIP/판정 원본은 보존한다. 실제 수령·판정은 별도 반박 리뷰 창, 발송은 1저자다.

공용 전체 게이트 **HOLD 유지**. 이번에는 관련 직접 검사·문서 참조·원장·변경 경로 검사를 수행한다. 기존 전체 게이트의 실패·중단을 재실행으로 지우지 않으며, Rint 구현이나 다른 트랙으로 확대하지 않는다. 통합 전체 게이트는 Claude 통합 때 별도다. Q1 기록·MXD2R 외부 판정은 별도 대기다.

# RTR-01 — 최종 폴더 audit 퇴역 보완

전체 HOLD. RTA-02 잔여 RTR-01(P3)은 648bb499015764f5aed74d4ca41f31a9d7c83f0d 독립 재확인에서 코드 범위 종결 가능으로 수령했다. 연구 결과 0건. RTRR-01 비차단 P3에 따라 아래 이동 오류 문구만 좁혔다. verified/closed로 자동 승격하지 않는다. 새 수령 정본은 docs/reviews/rint2_rtr01_closure_20261113/README.md다.

## 1. 수령과 처분

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 독립 회신 ZIP | 1: 145파일·외부 해시144/144·CRC/경로/중복/링크 검사 통과 | receipt.json, intake_verification.json | 원본은 전달 ZIP에만 보존 |
| 고정 소스 | 1: candidate/scripts 38파일 = 검토 핀 blob 38/38 | 97d8831a858fab5f92ed3e580817eea2eaa85f5f | 변조 없이 수령 |
| RCPX-01–06·RTA-01 | 1: 외부 판정 = 코드·문서 범위 종결 가능 | 수령 판정 요약 received_verdict.md §1 | 기존 한정 보존; 공유 원장 반영은 Claude |
| RTA-02 | 0: 부분 수용; RTR-01(P3) 잔여 | received_verdict.md §2 | 이 후보 한정 재확인 |
| 새 P1/P2 | 0: 수령 판정의 새 지적 없음 | 원 회신 판정 | 범위를 연구 자격으로 확대하지 않음 |

## 2. 원 반례와 수정

run 폴더의 audit 퇴역과 최종 OUTDIR의 audit 퇴역은 별개다. 기존 후보는 새 팔을 OUTDIR에 올린 뒤 새 audit이 있으면 이동했다. 새 audit 생성/이동 실패 때 OUTDIR에 남은 옛 `hit` 기록을 소비자가 새 팔의 기록처럼 읽을 수 있었다.

이번 수정은 `scripts/sdcp_gain_vox015_8arm.sh`의 정상 팔 게시 직전에만 들어간다. 저장본 켬이고 최종 audit이 있으면 같은 부모에 `mktemp -d`로 새 보존 폴더를 만들고 옛 파일을 그 안의 `audit`으로 옮긴다. 보존 폴더 할당 또는 퇴역 이동이 실패하면 새 팔을 게시하지 않는다. 퇴역을 마친 뒤 기존 팔 이동과 새 audit 이동을 수행한다. 최종 audit가 없으면 `missing`, 읽을 수 없으면 `unreadable`이며 이동 오류 뒤 source·destination 상태를 일률적으로 보장하지 않는다. audit 자체는 자기 기록이며 새로운 팔 hash/attempt 인증 계약을 도입하지 않는다.

| 조건 | 상태 | 결과 |
|---|---|---|
| 새 audit 없음·생성 실패 | 1 | 새 팔은 기존 자격 검사 뒤 게시; audit 소비자는 `missing`; 옛 바이트 별도 보존 |
| 새 audit 이동 실패 | 1 | 경고; 이동 전 실패면 `missing`·source 보존, 목적지 변경 뒤 실패면 새 audit 또는 `unreadable` 가능; source 잔존 일률 보장 없음; 옛 `hit` 재사용 차단 |
| 옛 audit 퇴역 실패 | 1 | 반환값 비0; 새 팔 게시 중단; 옛 기록 보존 |
| 정상 새 audit | 1 | 새 audit 바이트 그대로 소비; 옛 바이트 별도 보존 |
| 유효한 기존 팔 SKIP | 1 | 원 위치의 팔·audit 그대로; 퇴역 코드에 도달하지 않음 |
| 저장본 끔 | 1 | 기존 곁 파일 이동/집계 안 함; 기존 정책 그대로 |
| 팔 이동 자체 실패 | 1 | 비0; 새 audit을 게시하지 않음; 옛 audit은 이미 보존됐을 수 있음 |

불완전한 기존 팔을 지우는 앞선 동작, 조립만(CJGO) 경로, 과학 payload·소비자·audit writer는 고치지 않았다. 단일 작성자·고정 폴더 전제다. 동시 작성, 외부의 경로 바꿔치기, POSIX/Lustre 내구성·중단 복구를 이번 작은 시험으로 인증하지 않는다. audit 누락은 과학 결과의 실패로 자동 바꾸지 않지만 옛 성공 기록으로 채우지도 않는다.

시험의 실패 시 옛 팔 바이트 보존 assertion은 **게시 조각 진입 시 남아 있는 팔**에 한정한다. 전체 러너는 그보다 앞에서 불완전한 옛 팔을 지울 수 있다. 옛 audit 바이트 보존과 전체 러너의 옛 과학 팔 보존을 같은 보장으로 적지 않는다.

## 3. 시험

| 검사 | 상태 | 범위 |
|---|---|---|
| 원 독립 반례 원코드 | 1: 원 핀의 3시나리오 재현 | 새 audit 없음·이동 실패에서 옛 `hit`, 정상은 새 `built_written`; 상위 rc0은 반례 재현 성공 |
| 동일 새 회귀 | 1: 10메서드, 수정 전 8실패·오류0 → 수정 후 10/10 | 실제 Bash 게시 조각·SKIP 조각, 원 AST writer/consumer/store-off 메서드 |
| 기존 직접 회귀 | 1: 13/13 | 기존 시험 바이트 보존; 10과 중첩되는 경계가 있어 합산하지 않음 |
| Bash 구문 | 1: `bash -n` rc0 | 전체 러너 본문 실행 없음 |
| 내부 사전 공격 | 별도 기록 | internal_attack.md 및 evidence; 외부 독립 판정 아님 |
| 참조·원장 검사 | 별도 기록 | check_results.json; native 실패를 성공으로 바꾸지 않음 |

실행 환경은 Windows Python3.12.14와 Git Bash다. 새 시험은 표준 라이브러리만 사용한다. 기존13은 NumPy2.3.5·SciPy1.17.1이다. 원 외부 판정의 NumPy2.4.6과 구분한다. 새 팔의 `--check-arm` 통과는 합성 fixture의 명시 전제이며 실제 자격 검사·엔진·σ·현장 입력을 호출하지 않는다. 원 독립 회신의 13/13·조립7/7은 수령 기록이며 이번 새 고유 시험 수로 더하지 않는다.

재현: Bash를 사용할 수 있는 환경에서 `python -I -X utf8 -B scripts/test_rint_destination_audit.py`. 필요하면 `RINT_AUDIT_BASH`에 Bash 실행 파일을 지정한다. `RINT_AUDIT_SOURCE_ROOT`로 before 소스 사본을 지정해 같은 expected-correct 회귀를 적용할 수 있다. 원 반례 탐침의 실패 기대를 수정 성공 근거로 재사용하지 않는다.

## 4. 다음과 경계

review_request.md Q1–Q3와 이 폴더의 기존 수령·제안·시험 기록은 648bb499015764f5aed74d4ca41f31a9d7c83f0d 발송 때의 역사 기록이다. 재확인 결과는 새 closure 폴더에 수령했다. 원장 반영은 새 ledger_proposal.json을 함께 보며 Claude가 기존 Rint 사슬 뒤에 cherry-pick -x 한다. 기존 요청·쪽지의 단정적 `missing` 표현은 RTRR-01 정정으로 대체한다.

⑥ 시도3·4 블록은 코드 잔여 종결 가능 판정 수령 뒤 최종 핀으로 준비한다. 시도3은 빈 저장본 폴더, 시도4는 시도3 저장본 보존이라는 기존 비준을 유지한다. 실제 현장·GPU·연구 실행·운영 봉인·R 런은 별도 GO다. RCPX 전체나 Q11 소비·수치 자격을 다시 인증한 묶음이 아니다.

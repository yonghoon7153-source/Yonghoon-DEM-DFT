# BMIN150 배치와 사전 관측 검토

2026-10-06. **제출된 고정 R2 배치·사전 관측 완료를 한정 수용한다. 새 차단사항은 없다. 실제 native150 계산과 승인 파일 생성은 아직 미승인이다.** 준비·검증을 반복하거나 생산 코드를 수정할 필요는 없으며, 다음은 사용자의 최종 실행 승인이다.

이번 계산의 목적은 시간 연장이 아니라 **입자 반경 메시 320/320과 640/640의 한 축 민감도 비교**다. fresh 0→150초를 한 번 계산해 NORMAL480의 120–150초 구간과 비교한다. 작은 차이가 나와도 전체 공간 수렴·480초 후반 정확도·실험 타당성까지 수용하는 것은 아니다.

## 수신 식별과 무결성

수신 파일 BMIN150_DEPLOYMENT_PREFLIGHT_FOR_REVIEW_20261006.zip은 33,990 bytes / SHA-256 `8800035eb5ed427ea66d98d8dab8406fff189edceb9d86732706fbd323e70640`다.

- PACKAGE_MANIFEST의 payload 21개와 manifest 1개의 정확한 집합, 각 크기/SHA, 중복·대소문자 충돌·경로 이탈·링크 속성을 대조했다.
- records/MANIFEST.json의 17개 멤버와 이후 MANIFEST·CLOSEOUT을 포함한 기록 19개가 맞는다. 합계 78,470 bytes가 마지막 반환과 일치한다.
- 원 retry3 ZIP도 수신 PC에서 다시 해시하고 fixed_received/candidate의 8개 멤버를 읽어 제출된 배치 전후 식별과 대조했다. 1,619,237 bytes / SHA `ed0138b90cf2dc4e42f22ec18d8719ff56906780f74b4139850d604b096bb470`다.
- 데이터 대조 16항목 모두 일치했다. 기능 시험 16개를 새로 실행한 뜻이 아니다. CRC는 별도로 검증했다고 주장하지 않는다.

수신 패키지에는 생산 코드·CSV·MPH·prefs 전체가 없다. 따라서 배치 후 BML PC 파일을 직접 열어 해시한 것은 아니다. 원본 ZIP의 수신 측 바이트와 BML 측 배치·관측 기록 사이의 일치를 수용한다.

## 배치와 관측 수용

| 구분 | 확인된 기록 | 판정과 경계 |
| --- | --- | --- |
| R2 배치 | 8개, 212,467 bytes, 배치 전후 SHA 동일 | 원 retry3 멤버와 일치 |
| 후보 manifest | 1,050 bytes, 4cdca2e6… | 과거 비활성 상태 문자열 유지 |
| 기준 자료 | NORMAL480 run/tables 9개 | 고정 계약의 경로·크기·SHA와 일치 |
| 외부 의존 | 16개 | 같은 계약의 목록·크기·SHA와 일치 |
| 실행파일 | compile·batch·Python·PowerShell 4개 | 파일 식별 관측이며 프로그램 실행 아님 |
| future 경로 | 지정 5개 부재 | 당시 관측; 현재 또는 미래 부재 보장 아님 |
| prefs | 22,252 bytes, 064d1900…; security 16줄 | enable=on, filepermission=limited, 중복 없음 |
| cwd·자원·프로세스 | 각 1건, 합계 4건 | 아래 한계 유지 |

관측 합계는 5+9+16+1+4+1+1+1+1=39건이다. 관측의 expected만 신뢰한 것이 아니라, 이전 고정 커밋 e4e06889338f22df53e4d4ece9e29e1131570fad의 보존된 계약·COMMAND_MAP과 observed 경로/크기/SHA를 다시 대조했다. INACTIVE_STAGE2_BINDINGS의 명령 배열·cwd·예산도 그 고정 자료와 같다.

CODE_MANIFEST 전체 SHA는 `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`다. manifest의 OFFLINE_CANDIDATE_NOT_VALIDATED·approved=false·usable=false는 변경하지 않는다. 기존 검증 수용은 별도 VALIDATION_RELEASE에서 근거와 연결해야 한다.

prefs 전체 SHA는 `064d190077d7533f9fff22b61460d377cb53fb314e5c0f32a0bd02e3fa28b651`다. 이 파일의 동일성과 보안 문자열을 COMSOL 내부 실효 정책 PASS로 바꾸지 않는다.

디스크 121,785,380,864 bytes는 관측 당시 15 GiB 시작조건을 만족한다. RAM 7,093,915,648 bytes는 관측값일 뿐, 하한·peak·향후 충분성 보증이 아니다. Get-Process 이름/ID에서 comsol·java/javaw 일치 0개는 해당 조회 범위만 의미한다. 전체 명령줄·원격 작업·모든 내부 프로세스의 부재를 입증하지 않는다.

## 시간과 종료 기록

START의 원점은 2026-10-06T11:52:42.9862179+00:00이다. 관측 39건은 11:54:38.0560940–11:54:40.5737121+00:00 구간에 있다.

CLOSEOUT 쓰기 전 298.8750041초, 마지막 쓰기·재읽기·해시 뒤 298.9079295초이며 1,800초 이내다. 기록 78,470 bytes도 50,000,000 bytes 한도 이내다.

FINAL_PREFLIGHT_TOOL_RETURN의 ed90f4 / rc0 / wall 0.9614202초는 후속 전사다. CLOSEOUT SHA `67aab5f65d316413589e856dcef039bb13726764e38af121417f2f248410f310`와 records manifest SHA `8258b3c1826b585467e672deb07d54a38db729c71b575b663c2ef152e0b61f0e`가 실제 ZIP 멤버와 일치한다.

298.9079295초는 반환 전 snapshot이며 도구 wall time을 더해 새로운 전체시간을 만들지 않는다. 이 파일은 원시 stdout 문자열 그대로가 아니라 반환의 필드를 후속 직렬화한 기록이다. READ_OPERATIONS_INDEX 일부도 원출력 요약임을 표시하고 있다. 독립 원격 OS 감사나 모든 명령의 완전한 터미널 캡처로 확대하지 않는다.

이번 검토용 ZIP 포장은 관측 종료 뒤의 별도 전달 작업이다. 관측 당시 zip_created=false와 현재 ZIP의 존재는 모순이 아니다. 현재 포장 활동의 예산을 과거 298.9초에 소급 포함하지 않는다.

## 최종 승인 요청문 판정

INACTIVE_NATIVE150_FINAL_REQUEST_KO.txt는 수용된 고정 계약과 정합적이다. 앞서 정정한 PowerShell 실행파일 식별과 부모 시간 원점도 반영됐다. 변경·재봉인·한정 시험 재실행을 요구하지 않는다.

사용자의 별도 명시 승인에는 다음 조건을 유지한다.

1. 고정 실행본으로 fresh 0→150초, compile/batch/solve 각 최대 1회, control·retry 0회. 물리300, 입자640/640, 0.1C, sigma1e-20, threshold0, rtol1e-6 및 기존 보호식·허용치 유지.
2. 현재 관측은 예약이 아니다. 부모/entry의 기존 해시·경로·승인·정책·디스크 검사를 그대로 거친다. 불일치·동시 작업·충돌·정책/도구 거부는 중지하며 과거값·다른 경로·관리자 권한으로 대체하지 않는다.
3. 사용자의 실제 승인 원문을 USER_DECISION에 식별하고, 수용된 검증·이번 사전 관측·고정 manifest를 VALIDATION_RELEASE에 결속한 뒤 bmin640_001.json에 연결한다. 필요한 근거가 없으면 만들어 채우지 않고 중지한다. 검토 문서의 생성·수신만으로 이를 만들지 않는다.
4. 일반 PS5.1 NoProfile/NoExit 경로와 고정 COMMAND_MAP을 유지한다. 같은 Python 세션의 새 두 challenge는 사용자가 직접 입력한다. 자동 응답·check-only 반복은 없다.
5. 부모 전체 10,500초는 4행 Stopwatch 원점에서 시작한다. 단계 180/9000/120/900/300초를 유지하며 자동 연장·전용은 없다. 마지막 POST_WRITE는 FINAL_BOUNDARY 쓰기·재읽기·해시 뒤의 snapshot이다. Stop-Transcript 뒤에 나오므로 사용자 화면 원문과 프롬프트 복귀를 따로 보존한다. NoExit 외부 OS rc는 null이다.
6. 결과 포장은 부모와 별도 1,800초·1회로 최종 승인에 명시한다. 실패·초과 시 원 산출과 판정 필드를 그대로 보존하고 중지한다. 결과 MPH는 크기/SHA만 전달하고 수신 검토 종료까지 삭제하지 않는다.
7. native_completion·evidence_validity·mesh_comparison을 구분한다. 비교 초과는 EXCEEDS_LIMITS이며 native 오류와 다르다. 다음 시간·메시·물리조건 계산을 자동 시작하지 않는다.

기존 LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE, PS01-16 내부 분기 UNOBSERVED, 실효 정책·실제 코어 UNVERIFIED, 전체/정상 gate INCOMPLETE를 유지한다. 처음 root 부재 중지와 Python 1회 절차 이탈 기록도 소급 PASS 처리하지 않는다.

## 이번 검토의 범위

PowerShell/.NET으로 ZIP과 텍스트·JSON·SHA를 읽고 데이터만 대조했다. 동봉 스크립트·후보·부모를 실행하거나 import하지 않았고, Python·기능 시험·COMSOL·설정 변경·BML 경로 배치·실제 승인 파일 생성은 하지 않았다. 외부 발송도 하지 않았다.

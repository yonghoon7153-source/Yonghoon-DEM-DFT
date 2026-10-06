# BMIN640 r2 native150 승인 요청 검토

2026-10-06. **1단계 사전 관측 승인안은 문구 두 곳을 정정하는 조건으로 수용한다. 실제 사전 관측과 native 150초 계산은 모두 미승인이다.** 고정 생산 코드 수정이나 한정 검증 재시험은 요구하지 않는다.

이 작업의 목적은 시간을 더 늘리는 것이 아니라, 같은 모델의 입자 반경 메시를 두 전극 모두 320에서 640으로 바꿨을 때 120–150초의 선언 표본에서 전압·표면 조성이 얼마나 달라지는지 확인하는 것이다. 150초 계산을 완료하거나 차이가 작아도 전체 공간 수렴·480초 후반 정확도·실험 타당성을 증명하지 않는다.

## 검토 대상과 유지되는 수용

- 최초 첨부는 요청 커밋 `b67fed84646e5b783a1046280df73dec0727f6dc`의 문서와 바이트가 같다. 13,541 bytes / SHA `8e87252e208adfdc065ca5e08b00b406224a4137601e42cc44e19483681ddfe9`다.
- 질의 뒤 정정본은 `9c6f58200eb67a68f063e5399c454d6fc6883e5d`의 같은 문서다. 17,060 bytes / SHA `758baf7b0d44981f727a417cd2f56b55431186469debba1baa915a5e76812795`다. 이 판정은 두 정정 절을 포함한 버전에 대한 것이다.
- 후보 CODE_MANIFEST SHA는 `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`다. manifest의 5개 파일 크기·SHA, manifest 자체 및 봉인 밖 COMMAND_MAP과 승인 필드 명세를 확인했다. 후보 8개 파일의 Git blob은 `939b544b8bb77dbf20a56520af9f74a82acd0a94`와 최초 요청 커밋에서 동일하며, 정정 커밋까지의 diff에도 후보 변경이 없다.
- 이전 `LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE`를 유지한다. 62개 ID·77개 입력의 한정 수용을 새 기능 시험 결과로 세지 않는다. PS01-16의 내부 TryParse 분기는 계속 UNOBSERVED이고 외부 fail-closed 결과에 한정한 수용이다.
- 1,637개 요청시각, 120–150초의 정확한 301개 주 비교시각, 전극별 241좌표, NORMAL480 `run/tables` 9개 봉인 참조, 외부 의존 16개와 명령·승인·예산 연결이 정적으로 일치한다. **실행 기계에 그 파일들이 현재 존재하고 같은 바이트인지는 아직 관측하지 않았다.**

## 질의로 해소된 경계

사용자 답변 및 요청문 §6-1·§9-1을 함께 수용한다.

| 단계 | 경계와 한도 | 현재 상태 |
| --- | --- | --- |
| 1단계 사전 관측 | 새 `bmin640_native150_preexec_20261006/`만 기록 허용, 50 MB·1,800초·1회. 이미 있으면 중지. 기존 root·기준·prefs·설치·runtime은 변경 금지 | 별도 사용자 승인 대기 |
| 향후 부모 실행 | 기존 계약 그대로 전체 10,500초, 그 안의 로컬 전달 300초. 정확한 계측 시작·끝은 아래 N150-N2 문구 적용 | 최종 2단계 승인 대기 |
| 향후 결과 포장 | 사용자 프롬프트 복귀 뒤 별도 1,800초·1회. 원 산출과 세 판정 필드는 불변. 실패·초과는 별도 포장 미완으로 보존 | 최종 승인 범위에 포함할 제안 |

사전 관측에서 r2 root가 없거나 v1/r1과 충돌하면 고치지 않고 기록한다. 배치가 필요할 경우 대상·보존 방법·배치 후 해시 대조를 최종 승인 요청에 별도로 적는다. 사전 관측 승인만으로 배치하거나 실제 승인·release·USER_DECISION을 만들지 않는다.

## 문구 정정 두 곳

### N150-N1 P2 PowerShell 실행파일 식별을 사전 관측 목록에 추가

요청문 §9 표 2에는 COMSOL 실행파일 둘과 Python의 현재 해시가 있지만 PowerShell 실행파일은 빠져 있다. 부모는 `PARENT_COMMAND.ps1:189`에서 다른 검사와 transcript 생성보다 먼저 아래 SHA를 요구하며 다르면 `POWERSHELL_IDENTITY`로 중지한다.

- 경로: `C:/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe`
- 요구 SHA: `8bb6fa8c283b4d92120b1ef249a9b311b0f804d4cabbe9981159976c8be76a5e`

**수정:** §9 표 2에 해당 파일의 현재 경로·크기·SHA와 봉인 부모 요구값 대조를 추가한다. 이는 파일을 읽는 관측이지 해당 엔진이나 부모의 시험 실행이 아니다. 불일치 시 값을 고쳐 맞추거나 다른 PowerShell을 선택하지 않고 중지한다. 업데이트·관리자 실행·모듈 정책 변경도 포함하지 않는다.

첫 BHash 오류는 `future_parent_001`과 transcript를 만들기 전에 날 수 있다. 해당 오류가 생기면 화면의 원문과 사용자 관측을 후속 증거로 보존하고, 존재하지 않는 부모 기록·외부 rc를 만들어 넣지 않는다는 절차를 명시한다. PS 5.1의 모듈 자동 로딩 미관측은 유지하며 이를 닫기 위한 별도 probe는 요구하지 않는다.

### N150-N2 P2 예산 시계의 시작과 마지막 관측을 코드대로 표기

정정된 §6-1은 원점을 207행 `PARENT_START`로 설명하지만 `$bClock`은 **4행 `Stopwatch.StartNew()`**에서 시작한다. 207행은 이미 진행 중인 시계의 기록이다. 전체 계측을 여기서 다시 시작하면 앞선 실행파일·manifest·승인·경로 검사의 비용을 빼게 된다.

끝 경계도 구분해야 한다. `FINAL_BOUNDARY.json`의 쓰기·재읽기·해시 뒤 **239행에서 POST_WRITE snapshot**을 취하고, 241행에서 예산을 판정하며, 246행에서 그 값을 출력한다. snapshot은 최종 줄 출력·STOP 출력·사용자 프롬프트 복귀 이후의 측정값이 아니다. 부모 transcript는 232행에서 이미 닫히므로 POST_WRITE 줄은 사용자가 별도로 원문을 제공해야 한다.

**권장 대체 문장:**

> 부모 전체 10,500초의 원점은 PARENT_COMMAND.ps1 4행의 Stopwatch.StartNew()이며, PARENT_START는 그 뒤의 기록이다. 정상 경로의 로컬 전달 300초는 분석 반환 뒤 216행부터 센다. 마지막 예산 관측은 FINAL_BOUNDARY 쓰기·재읽기·해시 후 239행의 POST_WRITE snapshot이고, 246행은 이 관측을 출력한다. 출력·프롬프트 복귀 이후 시간을 실측했다고 주장하지 않는다. 결과 수집·포장은 별도 1,800초·1회다.

기존 부모와 entry가 사용하는 단계별 시계·반환 후 예산 검사도 그대로 둔다. 이 문구 정정은 동기 I/O나 분석 본문을 예산 도달 즉시 강제 중단하는 새 watchdog을 의미하지 않는다. 코드 수정·재봉인·재시험 없이 문서를 실제 계측 범위에 맞추면 된다.

## 최종 승인에 남길 운영 조건

1. 1단계 새 폴더 기록에는 명령·원문·시각·파일 식별·security 줄·가용 디스크/RAM·프로세스 목록을 남긴다. 원본 CSV·MPH·소스 사본은 넣지 않는다. 시작과 종료, 총 크기 및 한도 판정도 같은 폴더에 기록한다. 관측 실패·시간 초과는 누락을 추정으로 채우지 않고 중지한다.
2. 미래 실제 실행은 보이는 PS 5.1의 동일 Python에서 새 두 challenge를 사용자가 직접 입력한다. check-only나 AI 입력을 재사용하지 않는다. 사전 관측 이후 상태가 계속 같다는 보장은 없으며 실제 진입점의 재검사는 유지한다.
3. NORMAL480 기준은 계약의 `run/tables` 9개다. 과거 ZIP의 더 짧은 `baseline/`으로 대체하지 않는다. 기본 prefs의 현재 식별은 관측값을 쓰고, 정책 무변경과 실효 정책 UNVERIFIED의 명시 수용을 최종 사용자 결정에 남긴다.
4. 봉인 manifest의 과거 `OFFLINE_CANDIDATE_NOT_VALIDATED` 같은 상태 문자열은 고치지 않는다. 별도 release가 수용된 검증 근거와 동일 manifest를 연결하고, 실제 사용자 결정이 승인 파일에 연결되어야 한다. 관측·검증 완료만으로 승인 boolean을 true로 만들지 않는다.
5. `native_completion`, `evidence_validity`, `mesh_comparison`은 별도 필드다. 한도 초과 EXCEEDS_LIMITS도 유효한 비교 결과일 수 있다. 비교 성공을 정상 gate PASS로 올리지 않으며 NoExit 부모의 OS rc도 null로 유지한다.

차단하지 않는 문구 정리: §5의 “2단계 사전 관측”은 “1단계 관측값을 2단계 승인에 결속”으로, 승인 문구의 “§9-2”는 “§9 표의 2번 및 §9-1”로 명확히 하면 된다. 1단계 1,800초·50 MB와 별도 포장 1,800초도 승인 원문에 직접 적는 편이 좋다.

## 결론과 다음 한 건

**정정 두 곳을 반영한 1단계 사전 관측안에 대한 사용자 승인을 받는 것이 다음이다.** 동일 문구만 반영하는 데 생산 변경이나 전체 재검토·기존 suite 반복은 필요 없다. 1단계가 승인되면 실행 기계에서 허용된 관측과 최종 2단계 요청문 작성까지만 하고 멈춘다. native 150초는 그 이후 별도 승인이다.

이번 검토는 GitHub에서 고정 텍스트를 읽고 로컬 첨부 및 해시·JSON·정확 산술을 대조했다. 받은 소스의 import·컴파일·함수 실행·시험·COMSOL 호출, 실행 기계 사전 관측, 실제 approval/runtime/token 생성은 모두 0회다. 결과 문서에는 write-page 스킬의 출처·판정·승인 구분을 적용했다.

독립 데이터 대조 51건은 최종 일치했다. 검토자 도구의 첫 대조에서는 문자열 `"150"`을 정수 150과 직접 비교한 오류 한 건이 있었고, Decimal 대조로 바로잡았다. 첫 50/1 결과는 `STATIC_CHECKS.json`, 최종 결과는 `STATIC_CHECKS_FINAL.json`, 정정 사유는 `REVIEWER_CHECK_HISTORY.json`에 보존했다. 후보 실패나 기능 재시험이 아니다.

## 고정 근거

- [정정된 승인 요청](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9c6f58200eb67a68f063e5399c454d6fc6883e5d/bms-balancing/docs/COMSOL_BMIN640_R2_NATIVE150_APPROVAL_REQUEST_20261006.md)
- [봉인 부모 코드](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/939b544b8bb77dbf20a56520af9f74a82acd0a94/bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/candidate/PARENT_COMMAND.ps1#L188)
- [승인 검사와 실행 진입점](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/939b544b8bb77dbf20a56520af9f74a82acd0a94/bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/candidate/src/candidate_entry.py#L45)
- 받은 텍스트와 commit 비교 메타데이터: `RECEIVED_SNAPSHOT.json`. 이전 한정 검증 판정은 `PRIOR_VALIDATION_DECISION.json`의 별도 보존 사본을 참조한다.

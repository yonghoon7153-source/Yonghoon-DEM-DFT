# 전해질 후처리 복구 — 파일 읽기 차단으로 미완

**INCOMPLETE_RECOVERY / BLOCKED_COMSOL_FILE_READ_SECURITY. 후처리 제출 1건, 새 solve 0회, 발동 시험 0회. 추가 실행 중지.**

사용자가 승인한 Astra High 작업은 기존 실패 MPH 복사본의 후처리 전용 복구다. 이번에는 COMSOL 파일 접근 보안 설정에 막혀 모델을 열거나 수치를 회수하지 못했다. 정상 시험의 최초 미완과 worker failed를 유지한다. 전체 수렴 미완·장시간 운전 보류도 유지한다.

## 실행과 원인

| 항목 | 기록 |
|---|---|
| 원래 정상 job | `56ef13bee5a448c5a029b02656ebf6bb` — failed, 변경 없음 |
| 복구 후처리 job | `28f40815e3a3410aab411ec93cd36fe1` — failed |
| 복구 소스 | ElectrolyteRecovery300R320C16.java |
| 제출 소스 SHA-256 | `610b7d7ebea32fdd6fc2d36dc9b7142e265338f3f99eca25dae80de48dddfd51` |
| 제출 자원 | 16코어, compile/batch 공유 1800초 한도 |
| 반환 코드 | compile 0, batch 0; native fatal error로 worker failed |
| 실제 수행 범위 | 컴파일 및 Java batch 진입; 입력 읽기에서 차단 |
| 새 산출물 | 소스·class·로그·상태·검토 기록. 새 수치 CSV/MPH 없음 |

native batch의 원문 진단은 다음이다.

> Security preference 'File system access' does not allow 'read' access

복구 코드의 첫 단계 `inputCheck("before") → hashInput() → Files.newInputStream`은 지정 복사본을 해시하는 읽기다. 이 단계의 성공 marker가 나오지 않았고 console.log는 0 bytes다. `ModelUtil.loadCopy`는 그 뒤에 있으므로 **loadCopy 성공이나 실패를 시험한 것으로 기록하지 않는다.** 직접 COMSOL API를 통한 해·987시각·필드 확인과 결과 평가에 도달하지 못했다. 이 실행 순서와 native 파일 읽기 거부를 원인 근거로 기록한다.

이것은 COMSOL 애플리케이션 보안 설정의 거부이며 Codex 자동 승인 심사의 거부가 아니다. 운영체제 파일 손상·MPH 데이터 손상·좌표 표현식 오류로 분류하지 않는다. 보안 설정을 바꾸거나 파일 읽기 방법을 교체해 재호출하지 않았다. native 로그의 경로 표기는 그대로 보존했으며, 실제 제출 소스의 경로와 입력 식별은 INPUT.json에서 확인할 수 있다.

16코어는 제출 옵션으로 확인했다. 모델 평가에 도달하지 않아 실제 평가 병렬성·메모리 사용이나 성능을 검증한 것은 아니다. 1800초는 응답 대기시간이 아니라 worker의 compile/batch 공유 예산이며 이번 오류는 timeout이 아니다.

## 준비한 코드와 미완 범위

복구 코드는 원래 모델의 build/main/preflightAudit를 호출하지 않는다. 별도 클래스의 호출 경로를 검사했고 study/solver 실행·초기화·메시 재생성·해 삭제·물성/threshold/보호 변경 호출은 없다. 필수 guard/전압/표면/Li/OCP 출력 뒤 별도 좌표 평가를 두었다. 제출 전 정적 검토에서 중복 helper를 제거했으며, 최종 제출/정본 소스 SHA는 같다.

그러나 **그 복구 경로의 정상 동작은 아직 검증하지 못했다.** 기존 x의 문맥 확인, 최소값/단위/domain 비교, 원래 기준 대비 요청187시각·전극별241좌표 및 정확 공통 저장시각 비교, 실제 설정과 저장벡터 전후 대조는 모두 미실행이다. 보조 좌표 식의 성공도 확인하지 않았다.

work/electrolyte_recovery의 analyze.py/common.py는 별도 복구 자료용으로 준비했지만 수치 분석은 실행하지 않았다. 원래 analyze.py의 completed 조건을 우회하려 status를 수정하거나 기존 audit/gate에 데이터를 덮어쓰지 않았다. 없는 CSV나 이후 데이터를 보간·대체하지 않았다.

## 입력과 보존

원래 실패 MPH와 별도 입력 복사본은 모두 1,266,539,803 bytes, SHA-256
`7fefc0cfdf6910d40f2fec8021d6efbc72250c4e8ff79ba4a9442233bc581658`이다.
COMSOL 밖의 파일 검사로 전후 크기·SHA 동일을 확인했다. 이는 실패한 Java 내부 해시 검사 성공과 구분한다.

선택한 기존 33개 파일을 계획서 갱신 직전까지 전후 대조했다. 기존 34개 job 폴더를 보존하고 이번 후처리 job 1개만 추가됐다. 이 범위는 현지 선택 파일·job 목록의 기록이며 원격 현재 파일 전체 검증이나 모든 프로세스의 실행 부재 증명이 아니다. 변경 전 NEXT_RUN_PLAN은 별도 사본으로 보존했다.

수신 측이 확인한 기존 ZIP 555,102,474 bytes / 76 payload+manifest / SHA `8a72d6a7fe7649aae94fbb3f921c297b9cdf39bec24fb5537b64b585ea11ad14`는 별도 수신 기록에 추가했다. 생성 당시 영수증과 원래 ZIP은 수정하지 않았다. 수신 측의 MPH 내부 987시각 및 저장 리소스 확인을 이번 API 복구 성공으로 확대하지 않는다. 역사적333개 전체는 이번에 다시 검증하지 않았다.

## 다음 결정

이번 승인 범위의 후처리 1건은 접근 차단으로 미완 종료한다. 자동 재시도, Java 파일 읽기 경로 교체, COMSOL 보안 설정 변경, 정상 solve 재실행 및 발동1198 제출은 하지 않는다.

다음 후보는 **COMSOL의 파일 접근 정책과 허용 가능한 MPH 로드 경로를 읽기 전용으로 검토하는 작업 1건**이다. 목적은 이번 차단을 해소할 최소 변경을 구체화하는 것이다. 기준은 동일 실패 MPH SHA이며 Astra High, 새 solve0·COMSOL 복구 재제출0·보안 설정 변경0으로 제안한다. 실제 설정 변경 또는 후처리 재호출은 검토 결과를 제시한 뒤 별도 승인을 받는다. 이 검토만으로 정상 기능 PASS나 발동 기능 검증을 해소할 수는 없다.

기존 기준 모델의 전해질 양수 확인은 후처리다. 실패 정상 복제본에는 solver 최소값 조건이 추가됐지만 필수 정상검사와 발동검사는 여전히 미완이다. OCP 외삽 금지, 기존 failed/INCOMPLETE_RANGE_STOP, 원본·초기조성·Li 재고를 유지한다. TIME_CAPS raw ZIP 차이 원인은 미확인이다. 후보C·추가 시간/메시 시험·전체 프로토콜·12시간 휴지·유한sigma·sweep은 계속 보류한다. 연속 시공간 양수성은 입증하지 않았다.

참고 API 의미: [ModelUtil loadCopy](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_general.47.15.html), [저장 해 조회](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.09.html). API 존재는 현재 보안 설정에서 호출 성공을 보장하지 않는다.

[복구 판정](results/RECOVERY_GATE.json), [전후 보존](results/INPUT_AND_PRESERVATION_AFTER.json), [소스 호출 경로 검토](SOURCE_REVIEW.json), [변경 전 계획](NEXT_RUN_PLAN_before_recovery.md).

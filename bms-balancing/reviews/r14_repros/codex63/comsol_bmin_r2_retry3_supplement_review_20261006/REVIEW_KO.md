# BMIN retry3 기록 보완 종결 검토

2026-10-06. 고정 커밋 `10525ae1e30cf2d0f5e6e232e92897f08db3030f`의 집계 정정표와 PS01-16 범위 정리를 이전 retry3 원 ZIP에 대조했다. 게이트 및 REIL 검토와 분리한다.

## 결론

**BMIN-R3-C1 기록 보완을 수용하고, PS01-16을 외부 fail-closed 결과에 한정한 B-min r2 한정 검증 계획을 종결한다.** 판정은 `LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE`다. 기존 62개 ID·77개 입력의 기대 결과 수용을 유지한다. 원안의 모든 요구가 변경 없이 충족됐다는 뜻은 아니다.

새 차단 항목은 없다. 생산 수정·전체 suite 반복·TryParse 내부 분기 추가 관측을 요구하지 않는다. **native 150초 계산은 미승인**이며, 다음은 고정 실행본의 별도 승인 요청문 준비다. 이번 종결을 실제 approval/token/runtime 생성이나 COMSOL 호출 권한으로 사용하면 안 된다.

## 1 확인한 식별과 행별 근거

| 대상 | 직접 대조 결과 |
| --- | --- |
| 원 retry3 ZIP | 1,619,237 bytes, SHA `ed0138b90cf2dc4e42f22ec18d8719ff56906780f74b4139850d604b096bb470` |
| 원 PACKAGE_MANIFEST | SHA `97f51112bd6c4e0ae502e56db99eba5fb56026c7b7c79d0639661cf44727b91a`; 244 payload와 manifest의 정확 집합·크기·SHA·CRC 일치 |
| 새 집계 정정표 | 138,108 bytes, SHA `16876bb01afe549f9f78ef1c5b32569a85f8e8e3dde0c1daef65bf56305c4414`; Git blob도 수신 메타데이터와 일치 |
| 입력 집합 | 77개의 고유 (ID, input_index), 고유 ID 62개. Python 42·Java helper 2·Windows PowerShell 33 |
| 근거 참조 | 396개 참조 위치, 고유 ZIP 멤버 140개. 모두 실제 멤버 바이트의 SHA와 일치 |
| 원본 보존 | 이번 검토 전후 원 ZIP의 SHA 동일 |

각 행의 `final_accounting_row`가 가리키는 ID·입력 번호·엔진 및 세 원래 필드가 일치한다. 준비 단계 `INPUT_CASE_MAP.json`의 같은 행은 `status=NOT_RUN`과 두 false를 담고, 최종 원 집계는 `status=PASS`와 동일한 두 false를 담는다. 정정표는 두 false를 최종 판정 근거로 사용하지 않도록 명시하며 근거 없이 true로 바꾸지 않았다.

Python 42행은 준비 입력 키·fixture 경로와 멤버 집합·INPUT_EXPECTATION·개별 candidate_entry 산출 경로·harness stdout 줄·PYTHON_RESULTS·최종 observed를 구분하여 연결한다. 개별 entry 산출 객체와 harness 판정 객체가 같다고 취급하지 않는다. PowerShell 33행은 입력 키 및 결과 배열 인덱스를 함께 사용하므로 한 ID의 복수 입력을 혼동하지 않는다. Java 2행은 해당 stdout 줄과 helper 안의 추출 checkShape/TIMES 바이트로 연결된다. 세 실행 엔진의 stdout은 반환 기록의 크기·SHA와 일치하고 기록된 rc0·예산 이내 상태도 맞는다.

독립 자료 대조 상세는 `REVIEW_CHECKS.json`에 있다. 그 파일의 검사 수는 JSON·해시·집합·문자열 대조 횟수이며 새 기능 시험 수가 아니다. 정정표 생성기와 받은 후보 코드는 실행하지 않았다.

## 2 BMIN-R3-C1 수용

이전 지적은 실제 시험 부재가 아니라 최종 집계에 남은 준비 단계 boolean의 의미 충돌이었다. 별도 정정표가 원 ZIP·manifest·원 집계 및 준비 템플릿을 해시로 고정하고, 전 행을 실제 입력·산출·판정·엔진 반환에 연결하므로 요청했던 기록 보완 조건을 충족한다.

원 ZIP·원 집계·기존 영수증을 고쳐 과거를 다시 쓰지 않는다. 정정표와 이번 판정을 원본과 함께 소비해야 한다. 대형 fixture CSV 전량을 이번에 재검산했다거나 원격 파일 전체를 직접 재해시했다는 의미는 아니다.

## 3 PS01-16 범위 정리 수용

실제 `PS51_stdout.txt` 19번째 줄과 `PS_RESULTS.json`의 인덱스 18은 최종 observed와 같으며 다음 값을 담는다.

- GDecision: `INCOMPLETE`
- GFields evidence_validity: `INVALID`
- GFields mesh_comparison: `INCONCLUSIVE`

이는 입력이 외부 완료 판정으로 승격되지 않는다는 증거다. TryParse가 반올림했는지 실패했는지, 어느 내부 거부 분기를 통과했는지는 계속 `UNOBSERVED`다. 이 합성 행의 `NORMAL_150S_COMPLETED` 필드도 실제 COMSOL 150초 실행 증거가 아니다.

범위 정리 문서와 `COMSOL_REBUILD_SPEC.md` §61은 사용자 선택 (가)를 기록하고, 원안의 내부 actual path 확인은 미충족으로 남기면서 외부 결과 범위에서 종결한다고 명시한다. 이 제출된 결정 기록을 문서상 범위 정리의 근거로 수용한다. 다른 대화의 사용자 발언 자체를 독립 인증한 것은 아니며, 이번 기록을 새 실행 승인으로 확장하지 않는다.

## 4 차단하지 않는 문구 잔재

정정표의 `not_claimed[0]`에는 `승인권자 결정 대기`가 남아 있다. 이는 §60 단계의 설명이며, 같은 고정 커밋에 포함된 후속 범위 정리 문서와 §61에는 결정 (가)가 기록돼 있다. 내부 분기 UNOBSERVED라는 실질 한계는 두 자료에서 동일하다.

**P3 문서 권고:** 접수 기록에 “정정표의 결정 대기는 작성 당시 상태이고, 현재 범위 결정은 §61 및 PS01-16 범위 정리 문서를 따른다”는 한 문장을 추가하면 충분하다. 원 정정표를 바꾸거나 재해시·재시험할 필요가 없고 종결을 차단하지 않는다.

## 5 유지되는 수용 한계

- PY04-02는 내용 파싱 전 baseline identity 거부의 대체 증거다. 실제 NORMAL240 교체 시험으로 바꾸어 부르지 않는다.
- PY05-03은 runtime tlist만 변조한 RUNTIME_TLIST 거부와 정적 순서 근거다. tlist와 tables 동시 변조를 실행한 증거가 아니다.
- profile 기록은 원 reader 성공 14회와 같은 바이트 재사용 39회이며 53회 재파싱이 아니다.
- 제출된 Java helper 컴파일·JVM 실행은 COMSOL 모델 실행과 구분한다. 이번 검토는 받은 소스 import·함수 호출·컴파일·suite·COMSOL 모두 0회다.
- 과거 실패·pending·원복·생성 영수증 recipient=null·정상 gate INCOMPLETE를 유지한다. 포장 반환의 후속 전사를 원시 OS 감사나 수신자의 당시 직접 관측으로 바꾸지 않는다.

## 6 다음 최소 행동

검토 접수를 기록한 뒤, 사용자가 요청하면 **같은 고정 실행본의 native 150초 별도 승인 요청문**을 준비한다. 생산 CODE_MANIFEST `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`, 정확 source/run/cwd/argv, NORMAL480 비교 기준, 정책·자원·시간·정리·보존 범위와 실패 중단 조건을 연결해야 한다. 준비와 실제 계산은 구분한다.

이 회신은 native 실행 GO가 아니다. 승인 전 실제 approval/token/runtime을 만들지 않으며 COMSOL 실행·설정 완화·960초 자동 연장·기존 시험 반복도 하지 않는다. 전체 수렴·공간 수렴·실험 타당성은 이번 검증 종결로 확정되지 않는다.

## 근거와 검토 범위

- [고정 커밋의 요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/10525ae1e30cf2d0f5e6e232e92897f08db3030f/bms-balancing/docs/COMSOL_BMIN_R2_RETRY3_SUPPLEMENT_REVIEW_REQUEST_20261006.md)
- [집계 정정표](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/10525ae1e30cf2d0f5e6e232e92897f08db3030f/bms-balancing/docs/BMIN_R2_RETRY3_ACCOUNTING_CORRECTION_20261006.json)
- [PS01-16 범위 정리](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/10525ae1e30cf2d0f5e6e232e92897f08db3030f/bms-balancing/docs/COMSOL_BMIN_R2_RETRY3_PS01_16_SCOPE_DISPOSITION_20261006.md)
- [원장 §61](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/10525ae1e30cf2d0f5e6e232e92897f08db3030f/bms-balancing/docs/COMSOL_REBUILD_SPEC.md#L4031)

받은 원격 텍스트는 `RECEIVED_SNAPSHOT.json`, 독립 대조 로직은 `reviewer_checks.py`로 보존한다. 기존 원 ZIP은 별도 원자료이며 이 회신 묶음에 중복 동봉하지 않는다. 문서 작성 스킬에 따라 원안·관측·범위 정정·승인 상태를 구분했다. 검토 중 무관한 과거 work 하위 폴더의 AGENTS 탐색은 접근 거부를 반환했으며 권한 변경 없이 중지했다. 해당 경로는 이번 근거가 아니고 본 검토의 자료 대조에는 영향을 주지 않는다.

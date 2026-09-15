# 전해질 농도 중단 기능 결과

**필수 검사 미완/실패 — 추가 실행 중지. 전체 수렴 미완·장시간 운전 보류.**

목적은 provisional 모델의 기능 진단이다. 실제 셀 정량 대응·장시간 GO·연속 시공간 양수성을 입증하지 않는다. 기존 기준 해는 재사용했고 원본을 덮어쓰지 않았다.

기준: Caps300R320H0125C16 / job `5d1a87652ed54e6a945d4f2af4aeda70` / SHA `4db47e27dcf0d8d2977dc786dab2c3ba40e98a6adf42d7201bf1c66ab802537e`.

## 구현과 실행 범위

solver에서 평가되는 Minimum coupling을 전체 domain[1,2,3]과 각 domain별로 만들었다. 기하차원1, Lagrange점5차, selection·차수·활성조건을 되읽었다. `comp1.minguardall(comp1.cl)<=ce_stop_threshold`를 True 모드의 세번째 활성 StopCondition으로 넣고 기존 두 guard 및 stepbefore_stepafter를 유지했다. 정지 증거는 같은 operator 식으로 출력하도록 구현했으나 실제 값/단위 내보내기 완료 여부는 아래 시험 상태와 구분한다.

물리300(120/60/120)·입자320/320·16코어·0.1C·sigma1e−20S/m·초기 재고/조성·OCP/물성·scale·초기화·rtol1e−6·초기step1e−5를 유지했다. cap은 `if(t<0.1[s],0.000125[s],0.1[s])`, 요청187시각/전극별241입력좌표도 동일하다. 새 두 소스 간 차이는 식별 이름2곳과 threshold 0/1198 한 곳뿐이다.

| 시험 | job | 임계값(mol/m³) | 소스 SHA-256 | 원래 worker 상태 | 이번 판정 |
|---|---|---:|---|---|---|
| ElectrolyteGuard300R320C16Normal | 56ef13bee5a448c5a029b02656ebf6bb | 0 | 40063efedfc95fae00b1d5df22636b3a7acddf40420074df98985d2027e810ce | failed | INCOMPLETE_POSTPROCESSING_UNDEFINED_COORDINATE |
| ElectrolyteGuard300R320C16Trigger | 미제출 | 1198 | f183d5dcdba4e23bd8fbc3b0666d5f3f5d49f0805a7bc3c30567c2e3009a6e6b | 미제출 | 미실행 |

각 job1800초는 컴파일·배치 공유 worker 예산이며 단순 응답 대기시간이 아니다. 제한 초과의 런처 정지는 하위 프로세스 전체 종료를 보장하지 않는다. 사전 버전 명령은20초 timeout이었고 파일 버전6.3.0.290을 읽어 구분 기록했다. solve 자동 재시도는 하지 않았다. 상세 자원/도구 한계는 RESOURCE_AND_TIMEOUT.json에 있다.

## 실제 설정·시간 이력·guard 증거


## 실패·미완

```json
{
  "normal": {
    "status": "INCOMPLETE",
    "classification": "INCOMPLETE_POSTPROCESSING_UNDEFINED_COORDINATE",
    "job_id": "56ef13bee5a448c5a029b02656ebf6bb",
    "all_required_checks_complete": false,
    "next_trigger_allowed": false,
    "error": "New optional domain argmin coordinate evidence uses comp1.x; COMSOL reports Undefined variable comp1.x in comp1.minguard1(comp1.cl,comp1.x), Global Evaluation after Time solver returned."
  }
}
```

기대하지 않은 실패/필수 검사 미완으로 추가 제출을 중지했다. 범위 실패로 자동 분류하거나 설정을 바꾸어 재실행하지 않았다.

**제가 추가한 좌표 증거 출력식의 오류다.** Global Evaluation에서 `comp1.x`가 Undefined variable로 보고됐으며 문제 식은 `comp1.minguard1(comp1.cl,comp1.x)`다. 기존 기준의 물성·초기재고·OCP 오류로 분류하지 않는다.

native Time solver는5초까지 적분을 완료했고 로그에0번부터986번까지987시각이 있다. 이는 **반올림된 native 로그**의986개 accepted 구간 근거다. 새 정확한 저장시간 CSV는 없으므로 기존 해와 정확 공통 저장시각/전압/표면x 비교를 완료하지 못했다. `axes_runtime_settings.csv` 한 개만 새 raw CSV로 남았다. 전해질 전체/영역별 최소값·자동추론 단위·비간섭·미발동의 필수 수치 검사는 미완이다.

임계값0[mol/m³]의 식/숫자와 선택[1,2,3]·각영역·Lagrange5차, Time/Variables1,143개의 의도한 네 배열 차이는 확인했다. 그러나 이것과5초 적분 완료만으로 정상 guard 기능PASS를 만들지 않는다. native 전해질 중단 경고는 없지만 최소값 시계열을 대신하는 검증은 아니다.

실패 MPH는 1,266,539,803 bytes / SHA `7fefc0cfdf6910d40f2fec8021d6efbc72250c4e8ff79ba4a9442233bc581658`이며 검증된 정상 해가 아니라 실패 산출물로 제공한다. worker 원래 상태failed·batch rc0·오류로그를 그대로 보존했다. 분류는 INCOMPLETE_POSTPROCESSING_UNDEFINED_COORDINATE이며 기존 INCOMPLETE_RANGE_STOP과 다르다.

발동1198 소스는 준비만 됐고 제출/solve0회다. source 수정·재시도·후처리용 COMSOL 재실행도 하지 않았다. 다음에 승인받을 후보는 좌표식/내보내기 오류를 검토하고 기존 실패 MPH 복사본에서 solve 없이 후처리만 복구할 수 있는지 확인하는 것이다. 이는 현재 미승인이며, 새 정상 solve가 반드시 필요한 것으로 단정하지 않는다. 정상 필수검사 복구 없이 발동 시험을 진행하지 않는다.

[실패 상세](results/NORMAL_FAILURE_DETAILS.json), [반올림 native 로그 시각만 추출한 CSV](results/normal_NATIVE_LOG_STEPS_ONLY.csv).

## 한계·보존·다음 상태

기존 기준 파일의 전해질 양수 검사는 여전히 후처리다. 새 복제본에만 step 뒤의 solver 최소값 조건을 추가했다. Lagrange 평가점의 최소이며 연속공간 참 최소나 모든 Newton trial의 양수성을 보장하지 않는다. 1198은 시험용 양수 임계값으로 실제 고갈점/생산 한계가 아니다. 모든 domain 개별발동, 실제0접근에서의 solver 안정성, 입자 내부 보호·CDC/장기제어 통합은 이번 두 시험 범위 밖이다.

OCP 외삽none·기존 failed/INCOMPLETE_RANGE_STOP·원본은 유지한다. 다른 원인 실패를 범위 중단으로 자동 재분류하지 않는다. TIME_CAPS raw ZIP 차이 원인은 미확인이다. 후보 C·추가 시간/메시 계산·전체 프로토콜·12시간휴지·유한sigma·sweep은 보류한다.

선택한 기존 45개 파일을 변경 전/후 크기·SHA로 대조했다. 전체 현지 파일의 원격 검증을 주장하지 않는다. 이전 33개 job 폴더를 유지하고 이번 1개만 추가됐다. 다음 계획서를 바꾸기 전 원문은 NEXT_RUN_PLAN_before_guard.md에 보존했다. 이번 원격 수신 검증은 아직 없으며 생성 영수증과 구분한다.

공식 의미: [Minimum](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_definitions.21.098.html), [Stop Condition](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_solver.36.208.html). [비교 계약](comparison_contract.json), [소스 검토](source_review.json), [판정과 원시 비교](results/), [다음 계획](../NEXT_RUN_PLAN.md).

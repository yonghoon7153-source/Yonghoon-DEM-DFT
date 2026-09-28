# 비활성 — 정상조건 fresh 0→30초 단발 승인 초안

**approved=false / usable=false. 지금은 실행 승인 요청 단계가 아니다.** 새 변경부 한정 검증 결과를 수용하고 최종 식별을 확인한 뒤 사용자가 채택할 문안이다.

> manifest `28dd6da5cc76885263c17b2671548a00692064807e02e77ceb6f3edbdd946fa5`, run_id `normal30_candidate_001`에 결속된 정상조건 fresh t=0→30초 진단 최대1회를 승인합니다. 저장 MPH restart가 아니며 compile≤1/batch≤1/solve≤1, 추가control0/자동재시도0입니다. 시험용1198이 아닌 기존 정상 threshold0, 기존 OCP/표면 보호식과 stepbefore_stepafter를 유지합니다. physical300/particle320·320/0.1C/sigma1e−20 및 물성·초기화·OCP·수치 허용치를 변경하지 않습니다.
>
> 일반 사용자 PowerShell5.1 NoProfile 전경 경로, 고정 Python과 같은 프로세스의 fresh 두 직접 입력을 사용합니다. 설정 변경0이며, 승인된 현재 prefs 식별이 다르거나 정책이 거부하면 중지합니다. All files 전환·권한 상승·다른 셸·우회·자동입력은 포함하지 않습니다.
>
> 요청16코어, 시작 디스크20GiB, 시작RAM 관측을 수용합니다. 새8GiB RAM 문턱/working-set 감시는 없으며 실제 메모리 부담은 미확인입니다. 사전/입력180초, compile+batch3600초, 소유정리합계120초, 분석900초, 로컬증거확보300초, 부모전체5100초의 제안 상한을 승인합니다.300초 끝은 로컬 최종증거 확보이며 이후 사용자 업로드 대기는 제외합니다. 각 원점/소비는 CONTRACT 및 RESOURCE_BUDGET에 따르고, 미사용분 전용·실패 후 자동 재시도는 없습니다.
>
> 정확30초 정상 도달·필수 수치/저장/반환/보존/정리/정책/예산이 모두 충족된 경우에만 한정30초 진단 완료로 판정합니다. 보호중단은30초 미완으로 별도 기록합니다. 첫 오류·fatal·식별/시간/정책/소유 귀속 불명확 시 다음 native 단계로 넘어가지 않습니다. 원본과 기존 실패·pending·원복·영수증은 보존합니다.
>
> native/analysis 자식 rc와 부모의 스크립트 완료 경계를 구분합니다. `-NoExit` PowerShell의 외부 OS 종료코드는 미포착/null로 두며 최종 local decision/FINAL_BOUNDARY/실제 반환문/프롬프트 복귀를 대조합니다. 오류 뒤 성공처럼 보이는 문구만으로 수용하지 않습니다.
>
> 전체/정상 gate INCOMPLETE와 내부 실효정책 UNVERIFIED는 유지합니다.30초 완료는 장시간·12시간 운전/수렴/실험 타당성/후보C/다음 연장의 승인이 아닙니다. 결과를 제출한 뒤 정지합니다.

현재 검증 release/사용자 결정/실제 승인/runtime/token은 생성하지 않았다. `NATIVE_APPROVAL_FIELD_SPEC.json`은 필요한 필드의 명세이며 사용 가능한 승인 파일이 아니다.

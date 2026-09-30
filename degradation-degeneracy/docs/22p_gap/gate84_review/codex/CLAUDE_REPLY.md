# 84차 검토 회신 — 2a/2b 분리 수용, 사전 고정은 수정 조건부 적합

고정 HEAD `7fed4594c74b16f4a53402699eb2a8427805cdf5`를 검토했습니다. 코드 기준 `ea2af59e`와 RUN_SCOPE 58개 파일 식별이 같고, source_digest는 독립 재계산해 `7187bd31740514d4`로 일치했습니다. 76차 및 83차 라운드 1 종결을 유지합니다. 수신 코드·시험·COMSOL 실행이나 영수증 재생성은 하지 않았습니다.

**2a=e/f/g+b, 2b=a/c의 분리 방향은 수용합니다. 다만 구현 전 고정 표에 아래 네 조건을 반영해 주세요.**

1. **G84-N1 P1 / 2a:** 기존 `_config_closure_digest()`는 hex16인데 planned-leg/v4의 `inputs.base_config_digest`는 hex64/null입니다. 기존 반환값을 그대로 비교하면 정상 non-null 계획도 거부됩니다. closure preimage 정의를 공유하되 v6은 전체 SHA-256, v5 승인 축은 기존 hex16을 유지하는 방식을 권고합니다. 실제 staged extends 전체에 결속하고 leaf SHA/16자 padding으로 대신하지 마세요. parent 변경·null·정상 non-null·staging 경로 대조를 고정하세요.
2. **G84-N2 P1 / 2b:** v5 sealed spec에 `stage3:null`을 추가하면 canonical 바이트와 digest가 변합니다. v5 기존 key set/preimage를 보존하고 v6 spec을 명시적으로 버전 분기하세요. v6 stage3 누락의 legacy fallback은 거부합니다. **이 문제를 2a에 끌어오지 마세요.**
3. **G84-N3 P1 / 2a:** `_run_fit_locked`의 halfcell `_fit_one`(1955)이 `_prepare_stage3` 호출(1970)보다 먼저입니다. 그 helper 안에만 새 검사를 넣으면 “시작 전 거부”가 부족합니다. v6 unsupported reference/p_ini 및 source/staged-config 결속을 첫 수치 작업/worker보다 앞선 공통 경계에서 검사하고, 거부 때 inert sentinel 도달 0을 확인하세요. 이는 R2-b의 배선 보완이지 p_ini 지원 구현이 아닙니다. 기존 lock/승인 및 legacy 동작은 유지하세요.
4. **G84-N4 P2 / 2a:** `returned`는 objective별 `restarts_json` 원소 수 합입니다. `finite`는 저장 J 유한 수, `converged`는 legacy true 수로 명시하고 정상 종료/primary complete-pair와 분리하세요. legacy는 80차 정정의 “마지막 유한 fun round success”입니다. finite 성공 뒤 nonfinite 종료도 두 수에 들어갈 수 있습니다. `execution-record/v2`는 수용하되 writer/재계산 consumer 모두 버전 분기하여 v1의 닫힌 키·원문 읽기를 유지하고 v2 필수 키 누락의 하향 해석은 거부하세요.

네 정책 결정은 p_ini 거부 유지 / protocol `v6` 하나 / 기존 run.sh 경로 통합 / record v2를 위 조건으로 수용합니다. CLI 표기는 현재 문법에 맞게 **`./run.sh --mode fit --stage3-plan <leg_id> ...` 후보**로 정정하세요. 정확 argv와 기존 leg/env 충돌 규칙은 2b 전에 고정하며 지금 실행하지 않습니다.

추가 문구만 바로잡아 주세요: 내부 `stage3=` 전달 호출은 이미 있으므로 “외부 production 진입점이 없다”로 좁힙니다. R2-f는 계약 §1이며, legacy 의미는 보존하되 dead 정의 삭제로 이동한 코드 인용 줄번호는 갱신할 수 있습니다.

2a 생산 파일은 제안한 네 파일 안으로 한정하고, 관련 시험/문서/변이 및 기존 leg별 영수증 1회·history 보존을 별도 사용자 승인에 명시하세요. validator만 바뀐 digest에 가상 연구 leg를 등록하지 않습니다. 2b 구현 자체도 실물 v6 실행/등록 완료가 아닙니다.

**다음은 이 정정을 고정 표에 반영하고 사용자에게 2a 제한 구현 승인을 받는 단계입니다.** 같은 계획을 처음부터 다시 만들 필요는 없습니다. 이 회신 자체는 구현 착수·실행 GO·새 연구 leg·라운드 2b·복원·class/투영 승인이 아닙니다. grid_fit_v5는 진단 전용으로 유지합니다.

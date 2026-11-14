# 믹서·LHS 준비 확인

## 1. 믹서 시계 적용 범위

고정 후보 087ba5eb9a8d1d2c363d265bacfe064116361c80의 wrapper와 런처 텍스트만 읽었다. `mixer_clock_map.json`은 Git blob·SHA 및 AST 위치를 담는다. 소스 import·자식 프로세스·셸·현장 실행0이다.

| 직접 시계 호출 함수 | 행 | 고정 overlay의 정적 적용 대상 |
|---|---:|---|
| run_blind | 149 | wrapper의 datetime 이름 |
| _vault | 216 | 같은 이름 |
| run_contract_cert | 343 | 같은 이름 |
| e0_diag | 473 | 같은 이름 |
| _now | 549 | 같은 이름; 이 함수를 부르는 경로는 별도 |

기존 overlay는 wrapper의 datetime 바인딩만 바꾼다. Python 전체 datetime 모듈·다른 모듈의 import·OS 시계를 교체하는 코드가 아니다. 위5행은 정적 위치 수이며 해당 selftest가 전부 실행했다는 결과나 새 전수 실행 요건이 아니다. 실제 도달·비적용·미확인을 기존 네 칸 수령 기록에서 구분한다.

`mixer_gate_reader_diff._gate_code`와 같은 선택 규칙으로 rest Python 블록1개를 텍스트에서 찾았다. 그 블록 안에는 검사한 직접 시계 호출이0개다. 다른 함수 호출과 import가 있으므로 transitive 시계 무관을 증명하지 않는다. 전체 런처에는 다른 영수증 블록의 시계 사용이 있으며 이번 범위에서 제외한다. 런처 셸을 실행하거나 rest 외 블록을 평가하지 않았다.

앞 두 subprocess 위치(기존 `docs/reviews/dem_memory_preparation_20261114/mixer_selected_process_sites.json`)와 이번 범위를 연결해, Linux 수령 때 같은 wrapper 사본·자식 파일 신원·추출 관문 SHA를 별도로 확인한다. 실제 parent/child 시계 전달은 아직 미확인이다. SELF-170 네 칸·POSIX 권한·환경 자격·E0-R1·재봉인 A/B·host/wave·first8 GO는 그대로다.

## 2. LHS

실제 O1 출력은 아직 없다. 기존 `docs/reviews/nonrint_offline_casebooks_20261114/lhs_o1_receipt_plan.md`의11키+별도 실제rc, 기존10수령 사례를 유지한다. 현재 덱의 관측을 과거 실행 신원으로 올리지 않으며 `NOT_ESTABLISHED`·값GO NONE·전체 HOLD다.

원 명령 SHA256 `2026d61bb920599ca95870b62b8aee9ed3345f288da21ed4ff090a0064e0b8a3`와 기존 양식을 보존한다. 중복 parser나 새 현장 명령을 만들지 않았다. 수령 전 빈 값을 채우거나 Q2–Q4를 재질문하지 않는다. 이번 LHS 기록은 보존 확인이며 새 현장 관측이 아니다.

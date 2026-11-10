# D-3/LIVE·R-a — 동시 관측 채널·독립 이완 진단

| 1저자 결정 칸 | 권고 한 줄 | 준비 중 적용 |
|---|---|---|
| Q-LIVE-1: 필수 채널의 결속 | 반력·에너지·힘/토크 수지·판·접촉·재고를 같은 source/frame에 묶어 결손과 불일치를 보존 | **권고안 전제(Q-LIVE-1)**; 실제 수집/단위 자격 아님 |
| Q-LIVE-2: 독립 R-a 끝 | servo 진단 뒤 고정판·같은 이력의 별도 완전 R-a 창을 요구 | **권고안 전제(Q-LIVE-2)**; 실제 단계 전이·S0 생성 권한 없음 |

## 1. 바탕·산출물

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 바탕·새 가지 | T11 `ea5f22b6ae807dda3decf1928ec310d459996cb9` → `codex/dem-live-ra-contract-1110` | 상시 요청서 D-3 | 앞 판정/반입을 기다리지 않는 새 준비 |
| 순수 진단 API | `diagnose_live_ra(plan, servo_frames, ra_frames)` 1개 | `scripts/dem_gen2_live_contract.py`; `docs/reviews/dem_live_ra_contract_20261110/README.md` | 독립 확인 PENDING |
| 관측 채널 | 명시 7종, 동일 frame·source·unit·완전 재고 대조 | 같은 README의 입력/필수 채널·boundary 계약 | residual/gravity/damping/inertia는 입력 선언 채널. 입자에서 물리 수지를 재계산하지 않음 |
| R-a 경계 | 기존 servo bridge 뒤 별도 완전 예산·고정판·이력·terminal 창 | `contract_draft.json`; `verification_summary.json` | 끝 step·계획/trace·재고에 결속된 합성 후보만 반환 |
| 기존 함수 | q/T0/T11 source 바이트 3/3 보존 | 부모 Git blob·작성 측 영수증 대조 | 기존 전체 suite 재실행 0 |

전체 HOLD. 실제 원천 진위·단위·hidden history·T0/T11/T12·R-a/S0는 미확인/NOT_RUN이다. `source_authenticated/registration_complete/physical_ready/execution_go/transition_authorized/gate_write=false`를 유지한다. 실제 reader·엔진·운영 봉인은 구현하거나 변경하지 않았다.

## 2. 작성 순서·합성 증거

| 단계 | 결과 | 한계 |
|---|---|---|
| 사전 구현 초안 | red 전에 존재, 원본 보존 | root의 병렬 staging 요청에 따른 순서 한계. 엄격한 구현 작성 전 TDD 주장 없음 |
| 스텁 red | 25메서드, assertion/subtest 실패 67·오류 0·rc1 | 새 feature 미구현 대조, 과거 producer 결함 아님 |
| 보존 초안 첫 실행 | 25메서드, 실패 1·오류 0·rc1 | 누락 balance 구성요소가 REJECTED로 분류됨 |
| 최소 보완 뒤 | 25/25·오류 0·rc0 | 누락 구성요소는 NOT_COMPUTED. 잘못된 정상 부분자료로 대체하지 않음 |
| 보호 조건 제거 | 7/7 검출·모두 오류 0 | same-frame·source·전체 재고·고정판·R-a 예산·추가 채널·정확 bool 표지. 반복/내부 실패를 시험 수에 더하지 않음 |
| 최종 문구 정정 | source 첫 docstring만 수정 뒤 같은 시험 25/25 | 앞 변이 소스와 이 한 줄 외 바이트 및 docstring 제외 AST 동일. 7변이를 최종 소스에서 재실행했다고 쓰지 않음 |

최종 source SHA256=`a4e4d1c9e6574bac2c338d68e093dd999afc2c42c82c9f84f5011abd437d189c`, 고정 시험 SHA256=`78bb9922813c208b514c7ced4525d58e8b828c4d90cebb83655b5791bf42421a`. 이전 green·변이 기준은 `verification_summary.json`에 별도 보존했다. 각 합성 호출의 process/network 시도·engine·원자료/원로그 접근은 0, 연구 결과 0이다. 전체 gate/CI는 NOT_RUN. 앞 쪽지 `20261110-0121_dem-t5-contract.md` §3의 문서 노출 예외를 전체 턴 통계에서 지우지 않는다.

## 3. 반입·다음

반입할 커밋=`<<sha:Prepare synthetic live and R-a channel contract>>`. 같은 폴더 `review_request.md`를 11-10 하루 검토 ZIP에 고정 source·원 증거와 함께 넣는다. 발송=1저자, cherry-pick -x 반입·처분=Claude. 원장·공유 기록·Rint·봉인 32 수정 0.

다음은 D-3 **정확 S0 기록·순수 bytes 직렬화**다. 원 LIVE 입력을 재검증하고 같은 R-a 끝의 atom/pair/wall/mesh/restart/state를 결속한다. 숨은 이력·물리 복원 자격을 파일 hash만으로 승인하지 않으며 실제 파일/운영 source seal은 쓰지 않는다.

# 상시 요청 1회차 — 준비 인계와 일일 검토 묶음

| 남은 결정 | 권고 | 계속 준비한 전제 |
|---|---|---|
| DEM 정량/실제 자격·Q3 메타 | 단위별 고정 계약과 비결과 신원을 먼저 확정 | **권고안 전제(Q-DEM)**; 개별 쪽지 Q의 묶음 표기 |
| LHS 정본·동결·값 GO | 부족한 사실은 null/NOT_ESTABLISHED 유지 | **권고안 전제(Q-LHS)**; 현재 SHA로 당시 실행을 대체하지 않음 |
| 믹서 현장·전환·wave | 해당 범위 반박 GO와 1저자 GO를 모두 결속 | **권고안 전제(Q-MIXER)**; 기존 정책을 실제 실행 승인으로 확대하지 않음 |
| Q-LPI-1: 진단 시도에서 무엇을 보존할까 | 고정 명령 신원·원 rc/전체 출력·비결과 메타·상한/회수 영수증을 보존하고 원인은 UNKNOWN 유지 | **권고안 전제(Q-LPI-1)**; 진단 실행0 |
| Q-M1-2: S1/cohort의 등록 칸은 | 셀·팔·분모·관측 단계·실행 출처를 관측 전에 고정 | **권고안 전제(Q-M1-2)**; 새 등록 승인 아님 |
| Q-M1-3: D3 역할을 어떻게 나눌까 | 개발 탐색·보정·검증의 등록과 노출을 분리 | **권고안 전제(Q-M1-3)**; 물성/정량 선택 없음 |
| Q-M1-4: MIX-11의 다음 증거는 | 가상 호출별 rc·전체 출력·hash·scratch를 결속 | **권고안 전제(Q-M1-4)**; 이번 문서 계획만 |
| Q-M2-1: 현장 자격의 최소 범위는 | ibb 한 설치의 링크·권한/변경 통제·binary/MPI·자원/회수로 고정 | **권고안 전제(Q-M2-1)**; 현장 실행0 |
| Q-M2-2: 전환/발사 검토 단위는 | exact source/environment/승인 묶음에 두 GO를 결속 | **권고안 전제(Q-M2-2)**; 기준 완화 없음 |
| Q-M2-3: 런 실패 이후 처분은 | 운영자가 후속 wave 중단·증거 보존·수동 판단, 승인 없는 예약 해제 금지 | **권고안 전제(Q-M2-3)**; 자동 전파 기능 추가 아님 |

바탕 `96376652f9c6591feaacfbfb9a53264cd0dcb6d2`, 새 가지 `codex/nonrint-standing-handoff-1110`, 인계 커밋 `<<sha:Summarize non-Rint standing preparation batch>>`.
기준 B는 `13eb293cd9ac44502517c81e8f5e9b7ae02d817f`이며 자기 앞 가지 위로 순서대로 준비했다. 본 세션 복귀 쪽지는 미수령이다.

상시 목록의 D2–D5·L1–L3·M1–M2·C1의 현재 허용 범위를 마쳤다. D1 외부 판정은 미수령이다. 상태·시험 수·닫지 않는 범위는 `docs/reviews/nonrint_standing_handoff_20261110/README.md` §1, 절차 예외는 §3, 반입 규칙은 §4에 있다. 이번 인계 자체는 문서3파일·새 시험0이다.

| 순서 | 단위 | 고정 준비 커밋 |
|---:|---|---|
| 1 | d2 | `3f81b6162838c3453f3df806a2b0d176ae2c887b` |
| 2 | d3_t0 | `c5ebaa71298691020313e272b39c0a80b51cdc4d` |
| 3 | d3_t5 | `d11b60d2bc75948b0bc8a2c33f84e3b0b65869d4` |
| 4 | d3_t11 | `ea5f22b6ae807dda3decf1928ec310d459996cb9` |
| 5 | d3_live_ra | `63a513560c2770990920065be94ef966a8be018b` |
| 6 | d3_s0 | `f4647f2b7c218a6df7def3292c092273f9d4e35f` |
| 7 | d3_p2 | `c571a27119ace92ca34d3d6f2b61135219a3f1b4` |
| 8 | d3_qualification_matrix | `b7fbe749ea8ffa3151b3e768de445c572940c43d` |
| 9 | d3_demp | `fa073370edd483bc425c58311d010fd1ac211c04` |
| 10 | d4_gate_draft | `77eda58211459e5c14354e200adaaca81e4e2d2d` |
| 11 | d5_findings_proposals | `edc9fc83a22ee3d71bcbbf97fc03d28cda199a1d` |
| 12 | l1_document_cells | `6add88f264d2c651b467f3906e755824ed6e40ad` |
| 13 | l2_boundary_fixes | `ace5912fbaf2a892b52e32c7bdb0b89a490cdc3f` |
| 14 | l3_lpi_diagnostic_plan | `02a2087803d737290822964807e197133224029a` |
| 15 | m1_mixer_scope_followup | `b3ad4d4f66bc8133cc419e89071bb171ed976655` |
| 16 | m2_mixer_qualification_plan | `0c56deba6f2fb824996d770163a19c8e7dbd8abe` |
| 17 | c1_source | `084c978afc363078781dba37a318dc37e8edc084` |
| 18 | c1_web_cap_radius | `96376652f9c6591feaacfbfb9a53264cd0dcb6d2` |
| 19 | 이 인계 | `<<sha:Summarize non-Rint standing preparation batch>>` |

작성측 검증은 독립 반박 판정이 아니다. C1 첫 커밋의 sparse staging 누락을 후속 커밋으로 보완했으므로 준비18커밋은 논리17단위다. C1은 두 커밋을 순서대로 반입하며 완결 핀 `96376652f9c6591feaacfbfb9a53264cd0dcb6d2`만 독립 검토 대상으로 삼는다. 첫 커밋 단독 검토는 요청하지 않는다. 새 코드 후보는 각 고정 핀의 요청서와 일일 ZIP으로 검토를 요청하며, 문서만의 제안·기존 방어 유지와 구분한다. 하루 한 번의 ZIP은 1저자가 발송하고 Claude가 해당 수용 범위 뒤 `cherry-pick -x`한다. 원시 로그/ZIP 전체는 리포에 반입하지 않는다. 믹서 최종 발사 ZIP은 이번 준비 검토 ZIP과 별개로 미수령 처분을 유지한다.

T11/LIVE/S0의 엄격한 시험 선행 순서 미충족, 초기 시험/준비 오류, 역사 문서의 수치 서술 노출을 숨기지 않았다. 원시 증거와 고정 요약을 함께 전달한다. 실제 원로그·연구 값 접근, 연구 실행, 현장 접근, 운영 재봉인, 전체 gate/CI 실행은 하지 않았다. 봉인32·Rint·litdb 정본·원장/공유 기록 수정0. 전체 HOLD.

다음 외부 입력이 오면 D1 또는 이번 고정 후보의 지적부터 반영한다. 실제 승인 없이 연구/현장 단계로 넘어가지 않는다.

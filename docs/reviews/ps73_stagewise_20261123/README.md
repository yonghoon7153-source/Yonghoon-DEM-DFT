# 7:3 UB 이후 팔별 승인

11월 21일 1저자가 실행한 `GO_PS73_SEQUENCE_ONCE`는 UB부터 설정 선택까지 순차 제출하도록 승인한 모드다. 11월 22일 마지막 화면에서 UB 368469가 실행 중이었다. 11월 23일 인수 시점의 잡은 STATUS로 확인한다. 새 규칙을 적용하는 시점은 아래의 인수 성공 응답이다. 그 전까지 기존 감시기는 다음 팔을 제출할 수 있다.

| 차례 | 1저자 명령 인자 | 성공 출력과 다음 |
|---|---|---|
| 현황 | `STATUS` | 기존 UB 번호·팔별 job ID·감시기 상태를 읽는다. |
| UB 진행 중 인수 | `GO_TAKEOVER_BEFORE_UT` | `BOUNDARY_RESERVED`. 구 감시기의 UT 제출 자리를 먼저 확보한다. 실행 중인 잡은 마친다. |
| 인수 전 이미 진행 | `STATUS` | UT까지 접수됐으면 `GO_TAKEOVER_BEFORE_UC`, UC까지 접수됐으면 `GO_TAKEOVER_BEFORE_UV`, UV 한 팔까지 접수됐으면 `GO_TAKEOVER_BEFORE_UTc`로 그다음 경계의 인수를 선택할 수 있다. 마지막 명령은 연장을 제출하지 않는다. t3 여부는 원 선택기가 점검한다. |
| 후속 팔 선택 확인 | `RECORD_ONLY` | 구 감시기가 디렉터리 잠금을 놓은 뒤 기존 기술 영수증을 완성하고 고정 판독기로 `next_arm`을 출력한다. 상태 기록이 추가되며 제출은 0건이다. 종료 회계나 잠금 반납을 기다리는 경우 그 자리에서 끝난다. |
| UT | `GO_UT_ONCE` | 기본 속도, 절반 시간 간격. 일치하는 `next_arm=UT`와 해당 팔의 1저자 GO가 필요하다. |
| UC | `GO_UC_ONCE` | 판 고정 50,000스텝. UT의 정상 종료·원위치 수치 판독 다음이다. |
| UV | `GO_UVa_ONCE` 또는 `GO_UVb_ONCE` | UB·UT의 1 MPa 회복률 차이가 0.10%p 이하이면 UVa, 초과이면 UVb. UC까지 검증한 후 고정 선택기가 고른 한 팔에만 별도 GO를 준다. |
| 연장 | `GO_UTc_ONCE` | t3이고 UT의 고정 재시작 쌍이 확인된 경우에만. 회복률은 UT, 분리 보조 관측은 UTc에 귀속한다. |
| 완료 회수 | `RECORD_ONLY`, 원 블록 `RETURN` | `REVIEW`와 선택 행을 확인하고 종전 RETURN으로 전용 ZIP·해시·개발 판독을 받는다. 중간 회수에서는 `PARTIAL_RETURN`이 가능하다. |

## 인수와 경합 처리

고정 구현은 제출마다 새 팔 디렉터리를 배타 생성한다. 인수할 때는 원 GO 영수증·원 UB 368469·고정 소스·원 감시기 PID/부팅 식별자/명령행·이전 잡의 제출 응답을 확인한다. 원 감시기의 다음 반복 진입을 막는 공유 표식을 먼저 등록하고, 남은 팔 이름에 같은 파일의 하드링크를 배타 생성한다. UVa와 UVb 양쪽을 보호하며 실제 선택은 기존 판독기에 맡긴다. 이미 구 감시기가 반복 안에 있다면 한 팔이 이름 경합에서 먼저 접수될 수 있다. 이때 `STAGEWISE_AFTER_EXISTING_CLAIM`의 `previously_claimed`가 보존한 팔과 잡 번호를 준다. 출력이 `BOUNDARY_RESERVED`이면 경합에서 선점한 후속 잡이 없다.

영수증이 없는 디렉터리나 모르는 파일은 보존하며 새 팔을 차단한다. 조작 중 연결이 끊기면 `STATUS`로 표식과 접수 여부를 확인한다. 미완료 인수는 같은 경계의 인수 명령으로 이미 만든 링크를 대조하고 완성한다. 새 팔 GO로 복구하지 않는다. 실행 중인 잡에는 취소·신호·재제출을 보내지 않는다.

영구 표식을 만나면 원 감시기가 후속 제출 전에 끝난다. 기존 STATUS가 `HOLD_OR_RECONCILE`을 표시하거나 예약한 팔을 `SUBMIT_STATE_UNCERTAIN`으로 표시할 수 있다. 새 STATUS의 `stage_control=AUTHOR_GO_PER_ARM`과 실제 잡의 응답 영수증을 함께 본다. 새 경로는 고정 디렉터리 잠금을 얻은 뒤에만 한 팔을 진행한다. 퇴장한 구 감시기의 실제 오류 사유는 `controller`에 보존된다.

새 GO는 고정 현장 코드의 정상 종료 회계, 실행·덱 신원, 저장 보고/원위치 판독, 선택·저장 공간 관문을 재사용한다. 각 팔은 기존과 같이 ibb 한 노드, NP6, 팔당 최대 5일이다. 한 명령에 한 팔만 제출하며 명령의 응답은 새 잡 번호다. 응답이 끊기면 STATUS로 먼저 확인한다. 제출 의도와 응답이 일치하지 않으면 수동 판독을 기다린다. 다음 팔마다 별도 1저자 GO가 필요하다.

고정 근거는 `docs/reviews/ps73_development_sequence_20261121/controller/phase_controller.py`, `docs/reviews/ps73_development_sequence_20261121/sequence/ps73_sequence.py`, `docs/reviews/ps73_development_sequence_20261121/release/collect_ps73.py` 및 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §12–15다. 원 고정 핀은 2f4c42a3b205다.

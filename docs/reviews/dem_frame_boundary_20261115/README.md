# DEM 우선 — 프레임 제어 상태와 출력 경계 준비

## 1. 이번에 확인한 것

바탕 36054ada01fd9092ec38dbe32a7a27e9802863ac. 기존 합성 복구 모델을 실제 `scripts/mpm3d_compaction.py`의 프레임 제어부와 정적으로 대조했다. **초기화 구간과 프레임 변경 이름의 교집합 38개, 프레임 안 print 8곳, raise 1곳·break 2곳**이다. 이는 실행 횟수나 완전한 rollback 상태 수가 아니다. 소스 import·엔진·실제 입력·값 열람·물리 자격 수행0, 전체 HOLD.

정적 목록은 `frame_map.json`. `inspect_boundaries.py`는 고정 Git blob의 SHA256을 확인하고 AST만 읽는다. 기존 소스 SHA256은 `b8bb85278b09e4232c933a868d332eb544b981b75e7367c82ce98b54cce17bdd`로 보존됐다. 이번에는 solver·생성기·시험·공유 원장·운영 봉인을 고치지 않았다.

## 2. 실제 호출 순서와 복구 단위

| 순서 | 고정 소스 위치 | 현재 동작 | 다음 연결에서 필요한 구분 |
|---|---|---|---|
| 1 | 3229–3232 | 프레임 시작, profile 4개 초기화 | 프레임 전 상태와 substep 전 상태는 서로 다름 |
| 2 | 3233–3243 | substep → 선택 rod_pass 반복 → rod_setv → sacc/wacc/amdn/amup 누적 | 실패 지점에 따라 입자·rod·누적 profile·프레임 합계가 함께 걸림 |
| 3 | 3244–3281 | 판독·profile 축약, por0와 최근창 _p_tail 갱신 | kernel 사본만 복구해도 host 최근창은 자동 복구되지 않음 |
| 4 | 3282–3615 | 정착·제하·하강·hold·servo 분기, 창/카운터/판 위치·속도 변경 | 분기별 제어 상태와 장치 wall 필드를 같은 완료 상태로 연결해야 함 |
| 5 | 3616–3641 | 끝값 갱신, 프레임 출력, 수렴 break | 3552의 hold break는 이 끝값 갱신 앞에서 루프를 나감 |
| 6 | 3642–3735 | FINAL 등 출력 뒤 제하·servo 결과 반출 가드 | 앞서 인쇄된 문장을 승인된 완료 기록으로 소비하지 않음 |
| 7 | 4047–4174 | 선택한 metrics·배열·state 파일을 차례로 기록 | 파일 묶음의 원자적 반출 계약은 현재 정적 순서만으로 입증되지 않음 |

위 줄은 소스 제어 흐름의 관찰이다. 실제 실패가 발생했다거나 해당 과거 결과가 틀렸다고 판정한 것이 아니다. 호출된 helper의 전체 별칭·전역 상태·예외 효과까지 닫힌 분석도 아니다.

**권고 준비 범위:** 우선 substep+선택 rod와 그 누적값을 한 시도의 경계로 명시한다. 그 구현이 성공해도 프레임 전체 rollback/retry를 보장했다고 쓰지 않는다. 제어부에서 실패한 뒤 이미 끝난 substep을 되돌려 자동 재시도하는 정책은 아직 선택·구현하지 않았다. 통합 전에 복구 단위·완료 장벽·host/device 소유권을 고정하고 해당 변경을 독립 검토한다.

기존 `docs/reviews/dem_trial_isolation_20261114/trial_model.py`의 host 표지는 작은 합성 상태일 뿐, 아래 38개 또는 실제 frame 상태를 전부 담는 구현이 아니다. `docs/reviews/dem_copy_budget_20261114/README.md`의 세 사본 관측도 이 실제 프레임의 크기·복사 비용으로 전용하지 않는다.

## 3. host 상태 후보 명부

AST가 3169–3228에서 초기화된 이름 중 프레임 안 대입 또는 선택한 가변 메서드 호출이 있는 것을 뽑았다. 같은 이름의 여러 대입을 하나로 센다.

| 묶음 | 이름 | 수 |
|---|---|---:|
| 공통 끝값·도달 | reached, conv, por_end, p_end, por_at_target, por0, relax, am_skel, reach_cnt | 9 |
| 제하·정착·탐침 | _unload, _unload_status, _p_settle, _p_tail, _probe_left, _unload_cnt, _unload_probes, _z_lo, _z_hi, _settle_quasistatic, _settle_spread_rel, _probe_win, _probe_extended, _probe_win_max, _restart_floor_hit | 15 |
| 하강 동결 탐침 | _dsc_left, _dsc_win, _dsc_probes, _dsc_spread, _dsc_tgt, _dsc_armed, _dsc_qs_last, _dsc_qs_n, _geom_stop, _dsc_resumes | 10 |
| servo | _srv_left, _srv_win, _srv_probes, _srv_spread | 4 |

38개는 **필요 상태 후보**다. wall_z/wall_vel는 Taichi 필드여서 이 host 이름 교집합에 없고, frame 인덱스·프레임 합계·초기화 범위 밖 변수·다른 helper의 숨은 변경·출력은 별도다. 완전성·불변성·동시 실행 자격을 주장하지 않는다. 목록 안에도 재계산 가능한 값이 있지만, 제거하려면 같은 상태에서 재계산된다는 근거가 필요하다.

원소 추가·삭제뿐 아니라 창을 새 리스트로 재바인딩하는 경우도 있다. 창 내용만 복사하거나 얕은 dict 사본만 만드는 방식이 충분하다고 가정하지 않는다. 전체 사본을 택하면 기존 메모리 명부에 이 host 상태·window 수명·장치 완료 장벽 및 반환 사본을 추가해야 한다. 실제 크기·장비 예산은 미측정이다.

## 4. 출력과 중단의 별도 경계

프레임 안 print 8곳은 선택한 실행 경로의 진단 출력이다. 외부에 나간 stdout은 메모리 복구로 회수되지 않는다. 새 연결에서 시도 ID와 잠정/완료 구분을 정할 경우 기존 문장의 지위를 자동으로 올리지 않는다.

프레임 이후 선택한 파일 쓰기는 10곳이다: metrics 1, np.save 8, write_state_npz 1. 실제 옵션에 따라 실행 여부가 다르며, 관련 helper까지 포함한 파일 I/O 전수 목록은 아니다.

- 제하·servo 반출 가드(3697, 3723)는 위 파일 쓰기보다 앞이다.
- save-state 유한성 가드(4122)는 metrics·여러 np.save보다 뒤다. 그 가드가 거부하면 앞 산출물이 존재할 가능성을 계획에서 배제할 수 없다.
- 상태 저장은 `write_state_npz`(535행 정의, 549행 np.savez 계열 호출)로 이어진다. 이번에는 파일 저장 실패·전원 손실·다중 파일 반출을 실행 검증하지 않았다.
- 기존 restart가 v/C를 0으로 돌리는 규약은 유지한다. 저장 파일을 같은 시도의 정확한 rollback snapshot이라고 대체하지 않는다.

새 구현에 필요한 것은 성공 파일의 존재 확인만이 아니라 **시도에 귀속된 완결 집합과 거부/부분 집합의 구분**이다. 운영 저장 방식 변경과 재봉인은 이번 범위가 아니다.

## 5. 다음 합성 시험의 구체적 준비표

전부 **계획·미실행**이다. 기존 시험 통과 수에 합산하지 않는다. 실패 주입과 기대 관찰을 먼저 고정한 뒤 구현 연결별로 시험한다.

| ID | 주입 위치 / 작은 입력 | 기대 관찰 |
|---|---|---|
| FB01 | 두 substep 중 둘째의 profile 갱신 뒤 실패 | 복구 단위에 포함된 입자/rod/profile/합계가 그 시도 전과 같음. 앞 완료 substep까지 되돌렸다는 주장은 별도 |
| FB02 | rod_pass 반복 중 실패 | x·rod_dx·v 및 소유/ID 관계의 등록 상태 보존. rod 없는 경로도 보존 |
| FB03 | _p_tail append/pop 또는 probe 창 재바인딩 뒤 제어부 실패 | host 변경과 장치 변경을 나누어 탐지. substep 복구만 성공해도 frame 복구 PASS로 올리지 않음 |
| FB04 | wall_z 변경 뒤 기록 실패 | 물리 상태 완료와 외부 기록 완료를 구분. 기존 시도를 무조건 재실행하지 않음 |
| FB05 | hold break와 일반 종료 각각의 작은 상태 표지 | 종료 위치·마지막 끝값 갱신 여부를 관측. 두 경로를 같은 완료 사건으로 덮지 않음 |
| FB06 | FINAL 출력 뒤 제하/servo 가드 거부 | 진단 출력이 있어도 완료 산출물·승인 기록으로 승격되지 않음 |
| FB07 | metrics/배열 기록 뒤 state 유한성 거부 또는 저장 실패 | 부분 집합을 완료 집합으로 받지 않음. 기존 성공 산출물을 새 시도로 오인하지 않음 |
| FB08 | 같은 상태의 정상 경로·명시적 새 시도 | 승인된 원래 순서와 정상 상태를 보존. 중복 출력/카운터 증가·자동 재시도 없음 |

소스의 물리 알고리즘을 바꾸거나 실행 가능한 frame transaction을 넣지 않았다. P1 A/B 독립 설계 판정, 실측 자격, 1저자 수치·운영 결정은 그대로 대기한다.

## 6. 검산

리포 루트에서 `python -I -X utf8 -B docs/reviews/dem_frame_boundary_20261115/inspect_boundaries.py`는 원본 Git 소스의 정적 목록을 다시 만들어 두 JSON과 바이트 비교한다. Python3.12.14/stdlib와 Git 읽기만 사용한다. 대상 모듈 import·연구 입력 읽기·엔진 실행이 없다.

저장소 참조·원장 검사 결과는 `check_results.json`, 바뀐 범위와 원본 보존은 `scope_check.json`. 전체 게이트는 실행하지 않는다. 별도 전달문·인계 ZIP은 만들지 않는다.

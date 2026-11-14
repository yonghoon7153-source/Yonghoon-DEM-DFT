# DEM 수영 — 기존 MPM 소스의 상태·복원 경계 지도

## 1. 확인 범위

기준은 c438673b8dac3ce0a54dfcb0de00562a98e1ddf3의 `scripts/mpm3d_compaction.py`다. Git blob `fb1bf65535135ecdb7acb87833b7acdb389e54db`, 335832 B, SHA256 `b8bb85278b09e4232c933a868d332eb544b981b75e7367c82ce98b54cce17bdd`. 소스 바이트와 AST만 읽었다. 모듈 import, Taichi 초기화, 연구 입력·결과 열람은 하지 않았다.

앞 준비 `docs/reviews/nonrint_contract_preparation_20261114/dem_p2g_transaction_contract.md` §2–5와 `docs/reviews/dem_memory_preparation_20261114/README.md` §2를 실제 변수에 연결한다. 현재 소스의 restart 의미와 새 rollback 제안을 구분한다. 이번 기록은 기존 restart의 새 결함 판정이나 rollback 구현·자격이 아니다. 전체 HOLD.

## 2. 선언된 메모리

`source_state_inventory.json`은 main 안의 Taichi field 선언 33개, 선택한 네 kernel의 직접 대입 위치, field의 fill/from_numpy/to_numpy 위치를 담는다. 아래 계수는 f32/i32의 스칼라 성분을 4 B로 센 선언 payload다.

| 그룹 | 변수 | 선언 payload | 소스 위치 |
|---|---|---:|---|
| 물질점 상태·상수, 11개 | x, v, C, F, mu_p, la_p, yld_p, pvol_p, coh_p, dg_acc, eps_acc | 124n | 2801–2807행 |
| grid, 2개 | grid_v, grid_m | 16G | 2808행 |
| scalar, 6개 | wall_z, wall_vel, szz, wallf, amf_dn, amf_up | 24 | 2809–2810·2825–2826행 |
| z profile, 4개 | amf_zdn, amf_zup, szz_zs, szz_zn | 16nz | 2841–2844행 |
| AM mask, 2개 | am_mask, am_near | 8A | 2847–2848행 |
| rod, 8개 | rod_prev, rod_next, rod_rl, rod_kfac, rod_is, rod_b0, rod_dx, x_pre | 56R | 2903–2906행 |

G = n_grid × n_grid × nz. A = scaffold_on이면 G, 아니면 1. R = FIBRE_ROD이면 n, 아니면 1. 따라서 선언 payload 합은 **124n + 16G + 8A + 16nz + 56R + 24 B**다. 실제 n·격자 크기·가용 메모리를 받거나 대입하지 않았다.

이 식은 실제 할당량이나 peak가 아니다. Taichi layout/alignment·allocator·runtime/JIT, NumPy host 배열, host/device 복사, 저장·복원 사본, 임시 버퍼가 빠져 있다. F 방식의 입자별 장·색 계획도 현 소스의 이 식에 자동 포함되지 않는다. 실제 메모리 명부를 만들 때 이 식은 출발점이며, 누락 비용을 0으로 고정하지 않는다.

## 3. 쓰기와 완료 경계

| 단계 | 직접 쓰기 | 확인된 동작 | 새 복원 설계에 반영할 것 |
|---|---|---|---|
| load, 2936–2941행 | 9 field | x·상수 적재, v/C=0, F=I | 프로토콜 시작용 초기화와 같은 걸음의 정확 복원을 분리 |
| substep, 2944–3033행 | 17 field | grid·단일 걸음 scalar 초기화, P2G, 경계 처리, G2P, F·변형 이력·위치 변경 | 실패 지점 이후 일부 배열만 비워 재사용하지 않음 |
| rod_pass, 3036–3054행 | rod_dx, x | 각 pass의 변위 버퍼 초기화 후 rod 위치 보정 | rod가 켜진 구성은 모든 pass까지 시도 안에 포함 |
| rod_setv, 3057–3060행 | v | x와 x_pre로 rod 속도 갱신 | 위치 보정 뒤 속도 갱신까지 끝난 뒤 성공 처리 |
| frame loop, 3229–3242행 | profile fill 및 host 누적 | profile은 frame 시작에 한 번 초기화. substep과 rod 뒤 sacc/wacc/amdn/amup 누적 | 성공한 앞 substep의 누적분을 보존하고 실패 시도 기여만 폐기 |

17개라는 수는 AST에 보이는 서로 다른 field 이름 수다. 조건 분기별 실제 쓰기 횟수·커널 완료 보장·전체 호출 그래프를 뜻하지 않는다. fill/from_numpy/to_numpy 목록에는 읽기인 to_numpy도 포함한다.

### 3.1 다시 시도할 때 보존할 것

현재 substep의 지속적 물질점 쓰기는 x, v, C, F, dg_acc, eps_acc다. 이 여섯 field의 선언 payload는 104n B지만, 이것만 복사하면 충분하다는 결론은 아니다. 선택적 rod의 x_pre·rod_dx는 완전 재작성 순서와 실패 지점을 확인해야 하고, frame profile·host 누적·경계 상태도 별도로 다뤄야 한다.

profile 네 개는 substep 안에서 누적되지만 frame 시작에만 0이 된다. 따라서 grid만 비우면 실패 기여가 남고, profile 전체를 0으로 만들면 앞서 성공한 substep 기여까지 잃는다. 권고 구조는 **성공한 앞부분을 보존한 채 시도별 증가분을 임시 저장하고, substep 및 필요한 rod 단계가 모두 끝난 뒤 한 번 반영**하는 것이다. 기존 배열을 직접 수정하는 방식이면 시도 전 profile과 point 상태를 복원하는 별도 증명이 필요하다.

`accumulator_example.json`은 이 구분만 설명하는 정수 산술이다. 성공한 앞부분 2, 실패 시도 3, 재시도 3에서 무복원은 8, frame 전체 초기화는 3, 앞부분 복원은 기준 5가 된다. 이는 3개 물리 시험이나 solver 회귀 결과가 아니다.

### 3.2 host 상태는 아직 전수 목록이 아님

3170–3228행에는 reached/conv, reach_cnt, _settle/_unload, _probe_win, _dsc_* 및 _srv_* 같은 제어 상태가 있다. 현재 제안은 한 substep의 완료 경계를 먼저 잡고 frame 판독·제어 갱신 전에 성공을 확정하는 것이다. frame 전체 rollback 또는 frame 제어 이후 재시도까지 확장하려면 해당 분기·host 상태·출력 부작용을 전수 추적해야 한다. 이번 AST 목록은 그 전수 추적을 대신하지 않는다.

## 4. 저장본 재개와 rollback은 다른 계약

3140–3157행의 load-state는 F·dg_acc·eps_acc를 복원하지만 v/C는 의도적으로 0에 둔다. wall_z도 이번 실행의 이동 범위로 제한한다. 4096–4100행에서 v/C를 저장하는 목적은 감사이며 로드 때 재주입하지 않는다는 주석이 있다. 앞 초기화와 제어 상태 재설정도 그대로다.

따라서 현재 save/load 경로를 실패한 한 걸음의 정확한 되돌리기에 그대로 쓰지 않는다. 기존 프로토콜 전환용 재개는 보존하고, 새 rollback은 부모 상태·시간·시도번호·누적값을 별도로 보존하는 경로로 설계한다. 이 구분으로 기존 연구 결과나 재개 기능의 물리 적합성을 새로 판정하지 않는다.

## 5. 입자 신원 연결

소스에 se_id_base가 있고 저장 시 se_id를 내보내는 경로도 있다(4110–4112행). 그러나 확인한 33개 Taichi field에는 se_id field가 없으며 substep AST는 se_id_base를 참조하지 않는다. 현 kernel의 point index를 원 SE 입자 ID와 동일하다고 해석하지 않는다.

향후 F 또는 색칠 장 설계에는 point→원 입자→field와 주기 node 신원을 명시적으로 연결해야 한다. host의 ID 저장 기능이 있다는 사실만으로 P2G가 입자 소속을 분리한다는 보장이 생기지 않는다. 이 기록은 모든 다른 함수에 ID가 없다는 전칭이 아니다.

## 6. 다음 구현 전에 고정할 작은 사례 — 이번에는 미실행

| 사례 | 준비할 실패 주입 | 기대 |
|---|---|---|
| S1 | P2G profile 누적 뒤 중단 | 부모 point 상태와 이미 성공한 profile 앞부분 보존 |
| S2 | G2P 일부 point만 갱신한 뒤 중단 | x/v/C/F/dg_acc/eps_acc의 부분 결과를 완료로 공개하지 않음 |
| S3 | rod_pass 도중 또는 rod_setv 전 중단 | rod 보정 포함 전체 시도 폐기, 앞 성공 걸음 보존 |
| S4 | host 누적 일부만 반영한 뒤 중단 | 재시도에서도 누적 기여가 정확히 한 번만 반영 |
| S5 | protocol load-state로 rollback 대체 | 비영 v/C 및 이전 wall_z 보존 기대와 충돌함을 검출 |
| S6 | point index를 원 입자 ID로 사용 | 같은 원 입자의 복수 point와 다른 입자의 동일 좌표를 구분 |

수치 문턱·장 수·재시도 한도·실제 입력은 여기서 선택하지 않는다. P1 A/B 독립 판정과 내부 5회차 병합 대기는 그대로이며, 새 생산 구현·현장 실행·운영 봉인·원장 종결 권한을 만들지 않는다.

## 7. 확인 방법

같은 폴더의 `inspect_source.py`를 리포 루트에서 `python -I -X utf8 -B docs/reviews/dem_source_state_map_20261114/inspect_source.py --check`로 실행한다. 고정 Git blob을 읽고 길이·SHA256을 확인한 뒤 AST 목록을 재생성해 보존 JSON과 대조한다. Python 표준 라이브러리와 로컬 Git 읽기만 사용하며 solver를 import하지 않는다. 현재 HEAD의 물리 구현을 실행하거나 최신판에 자동 적용하는 도구가 아니다.

기존 필수 저장소 점검 결과는 `check_results.json`, 변경 범위 확인은 `scope_check.json`에 기록한다. 생산 소스·공유 원장·봉인·Rint 실행 핀은 이번 변경 대상이 아니다.

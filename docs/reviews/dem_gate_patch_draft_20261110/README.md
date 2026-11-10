# D-4 — DEM 세대 2 시험의 게이트 연결 패치 초안

**패치는 적용하지 않았다. 실제 gate/CI 실행0·시간 영수증0이다.** 반입/적용은 Claude가 담당하며, 고정 후보 검토·의존 반입과 CI/규율 K 대조 뒤에 수행한다. 기존 gate가 통과했다거나 이 초안의 새단계가 이미공유게이트에 들어갔다고 쓰지 않는다.

## 1. 고정 범위

바탕=`fa073370edd483bc425c58311d010fd1ac211c04`. `check_all_dem_gen2.patch`는 이 핀의 `scripts/check_all.sh`에 대한 **미적용 text diff**다. 원 파일의 Git blob/SHA와 제안 파일SHA, 기존 run 호출/순서 보존·run() 함수본문 보존은 `patch_draft_verification.json`에 결속한다. 실제 scripts/check_all.sh·CI·Rint·봉인32·공유진행/원장은 변경0이다.

## 2. 추가할 11개 호출

| 분류 | 시험 경로 | 경계 |
|---|---|---|
| 생산기/기존 자격 | `scripts/test_make_dem_gen2_decks.py`, `scripts/test_dem_gen2_qualification.py` | 정적덱·작은합성함수, 실제binary자격 아님 |
| 첫 연결 | `scripts/test_dem_gen2_observation_bridge.py` | 고정 원 bridge; D-1 외부 판정은 별도 |
| T0/T5/T11 | `scripts/test_dem_gen2_t0_contract.py`, `scripts/test_dem_gen2_t5_contract.py`, `scripts/test_dem_gen2_t11_contract.py` | 선언·toy통계/이산시간 계약 |
| LIVE/S0/P2 | `scripts/test_dem_gen2_live_contract.py`, `scripts/test_dem_gen2_s0_contract.py`, `scripts/test_dem_gen2_p2_contract.py` | typed원입력·바이트·진단순서만 |
| 통합/DEMP | `scripts/test_dem_gen2_qualification_matrix.py`, `scripts/test_dem_gen2_demp_contract.py` | 고정분모/단계·메타계약, 실제T12/DEMP종결아님 |

각 호출은 기존 `run 'label' python3 scripts/test_....py` 형식이다. 기존 단계는 삭제·재배열하지 않고 마지막 run 뒤에 새호출을 추가한다. 기존 `CHECK_ALL_RANGE`·`CHECK_ALL_LIST`·`CHECK_ALL_TIMES` 로직을 그대로 사용한다. 별도시간기록기를 중복추가하지 않는다.

## 3. 단계별 시간과 적용시 확인

현재 run()은 시작SECONDS·종료상태를 얻고 `CHECK_ALL_TIMES`에 단계번호/초/ok-or-fail/이름을 기록한다. 새호출도 이경로를 통과하므로 **실제실행시** 같은 형식으로 기록된다. 아직초값이나성공영수증은없다. 정적으로센 run 행 수는 실제전체단계/성공수와같은증거가아니다. LIST모드도preflight가있으므로이번에실행하지않았다.

**권고안 전제(Q-GATE-1)**: Claude가현재통합HEAD에후보를반입하고 exactpatch/의존을다시대조한뒤 CI동일시험경로·규율K를함께정렬한다. 실제공유게이트 수행은그담당절차로한다. 나눠수행하면같은HEAD/깨끗한트리에서전체범위가누락·중복없이이어지고모두fail0인지확인하며, 각실패의전체출력·rc·시도/소스·시간기록을보존한다. 중간통과나이번작성측suite를전체gatePASS로옮기지않는다.

이번검증은Git원blob·text diff·기존run본문/호출보존·새test경로존재의정적대조와읽기전용patch적용가능성확인뿐이다. 단위시험신규실행0·gate/CI/연구/현장0·운영봉인변경0. 실제발사/배포기준과반박창GO를낮추지않으며전체HOLD다.

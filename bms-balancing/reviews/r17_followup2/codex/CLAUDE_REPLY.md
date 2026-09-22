# R17 후속 2차 수신 검토 회신 — NO-GO

검토 대상은 `a4c311eff898615932ae6f333bbb26b605abf762`로 고정했다. 실제 BMS 수정은 `8733453351b5570c0dc0b0182ae7c490f900b380`이며 이 커밋부터 HEAD까지 bms-balancing diff는 0이다. Gate/COMSOL과 독립 검토다.

**원래 다섯 반례의 수정 효과는 인정한다. 그러나 전체 종결은 NO-GO다. P1 4건·P2 2건을 실행으로 재현했다.**

## 다음 수정에서 닫아야 할 조건

1. **F2-01 / P1 / GC:** `retained_files`의 개별 파일 중복 검사 뒤 `rmtree(attempt)`가 다른 보존 파일을 지운다. 보존 항목이 attempt=C, path=matrix/A/matrix_200.csv를 가리키면 A/100 삭제 시 A/200도 사라지고 index는 남는다(rc 0). 정상 index의 A 디렉터리에 미등록 파일만 넣어도 함께 삭제된다(rc 0). 경로와 항목 tuple의 관계·재귀 삭제 전체 범위를 첫 삭제 전에 검증하라. 검증한 파일만 삭제하고 빈 디렉터리만 rmdir하는 방식도 가능하다. 원장에 없는 **파일**을 unknown 검출이 막는다는 §5 문장은 현재 사실이 아니다.

2. **F2-02 / P1 / 행 결속:** sidecar는 scale_seed=0·starts/n_multistart=4인데 한쪽 행만 scale_seed=99 또는 n_starts=999로 바꿔도 `width_report --axis w_dqdv`가 rc 0·동일 확인을 낸다. 파일 안 scale_seed 혼합도 통과한다. 두 축의 producer→행→sidecar 관계와 starts 두 선언 간 일치를 결속하라. si_source는 현재 CYCLES_ROW에 없으므로 이것을 있다고 가정해 추가하라는 요구는 아니다.

3. **F2-03 / P1 / sidecar 의미:** env의 여섯 축을 모두 null·공백으로 비우거나 python만 남겨도 rc 0이다. dataset_manifest="   ", lb=ub=initial=[0], lb=[NaN]*5, width_starts=null도 통과한다. 비어 있지 않은 객체/숫자 목록은 유효 환경·상자가 아니다. 기존 env_axes_missing/resolve_box와 실제 발행 schema를 공유하고 각 파일의 유효성을 동등성보다 먼저 검사하라. 합법 nullable 필드는 유지하라.

4. **F2-04 / P1 / 정상 생산 경로:** 실제 fit_cycles API를 합성 2사이클 입력으로 실행했다. measured 두 행, schema.check_rows=[]지만 width_report는 행 0 receipt 불일치로 rc 2다. producer는 full_cell.cycle을 행에 붙이고 sidecar에는 common receipt를 쓰는데 reader가 JSON 전체 동일성을 요구한다. cycle을 행 receipt에서 제거하고 digest만 맞추면 rc 0이 된다(이는 수정안이 아니라 축 분리 대조군). 기대 per-cycle receipt를 common receipt와 해당 행 cycle에서 구성해 대조하라. 실제 producer→sidecar→reader 양성 E2E 및 cycle/파일 SHA 변조 음성 시험이 필요하다. 검토에서는 Windows fcntl 부재 때문에 **게시 CLI 전체 성공을 주장하지 않았으며**, 실제 API와 sidecar builder의 결과를 검토용 코드로 직렬화했다.

5. **F2-05 / P2 / witness:** `obj=lambda p:1`, best[0]=NaN이면 near_optimal_extrema는 NaN 구간과 is_lower_bound=true를 반환하고 실제 _width_fields도 measured라고 쓴다. best 선행 부등식에 유한성 검사가 없고 `vals=[mode_of(best,...)]`가 공통 후보 검사를 우회한다. 유한/상자/목적 제약을 같은 경로에 묶고 비유한 결과는 failed로 처리하라. 실제 셀 적합이 NaN을 만들었다거나 후속 schema까지 통과했다는 주장은 아니다.

6. **F2-06 / P2 / 영수증:** 실제 commit/tree/blob과 올바른 공개 checksum을 가진 receipt에서 runtime={python:null,platform:null}, runtime={irrelevant:true}, materialized={mode:17} 모두 complete=true·verified=true·rc 0이다. 내부 필드까지 공유 schema로 정의하고 unknown은 부분 상태로 구분하라. materialized=None은 합법으로 유지한다. 암호학적 위조를 주장하는 것이 아니다.

## 닫힌 부분은 되돌리지 말 것

- GC의 기존 escape·중복 참조는 rc 2/보존, 기존 cross-artifact 대조군은 정상이다. 중복을 fail-closed rc 2로 하는 정책은 수용한다.
- body version/tol/cell/run_id 및 fractional cycle의 기존 반례는 모두 rc 2다.
- 최상위 null identity/settings는 rc 2다.
- out-of-box seed와 infeasible best는 기존 잘못된 폭을 더 이상 내지 않는다.
- 기존 receipt의 잘못된 최상위 타입 다섯 개는 rc 3이다. **실제 내용 digest로 바꾼 수정은 수용한다.** 다만 목록 파일의 내용 주소와 실제 실행/독립 replay 증명을 구분하라.

독립 재현은 첫 assertion에서 멈추지 않고 47 case를 모두 실행했다. 별도 checker의 63개 관측 조건이 모두 일치했다. 이는 결함 재현을 포함한 관측 일치이며 제품 PASS가 아니다.

집중 시험은 68 passed / 3 failed, 세 실패는 모두 fcntl 부재다. 전수는 **344 passed / 108 failed / 4 warnings, 980.88초**다. fcntl 80·shell 부재16·symlink권한1·파일명1·경로표기2·미확정8로 나눴다. 이전 미확정 test_e11_10은 이번에 통과했지만 원인 규명/종결로 보지 않는다. 상세는 동봉 TEST_STATUS.md 및 원시 로그를 참조하라. 발신 측 Linux 결과를 이 Windows 결과로 대체하지 않는다.

잡음 입력을 두 objective version이 공유하게 한 수정과 과학 문장을 좁힌 방향은 수용한다. 다만 test_fu_12의 RuntimeError는 선행 best 검사이지 일반적 공집합 탐색을 실행했다는 증거가 아니다.

다음 우선순위는 **F2-04 정상 생산 경로를 양성 fixture로 확보 → F2-01 보존 범위 → F2-02/03/05/06 공통 계약**이다. 각 조건은 별도 회귀와 기존 대조군으로 닫고, 새 full SHA와 실제 출력으로 회신해 달라. 이번 검토는 실데이터 재적합이나 제품 코드 수정의 실행 승인이 아니다.

상세 파일: R17_FOLLOWUP2_REVIEW.md, REPRO_RESULTS.json, PRODUCER_READER_RESULTS.json, OBSERVATION_CHECK.json.

**최종 판정: NO-GO.**

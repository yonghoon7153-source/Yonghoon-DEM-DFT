# Gate74 — 완주·보존 증거 수용 / 주장 편입·전체 절차 종결은 보류

2026-09-26. 대상 HEAD `a49a021833282e0bd04c4565591668dc323e9630`. 새 실행 GO를 요청한 건이 아니므로 새 계산 허가를 내리지 않는다. Gate73의 E1/E2/E4 한계는 유지한다.

## 1. 결론과 질문별 답

**Gabia 판 3의 저장 결과와 보존 묶음은 제한적으로 수용한다. 전체 실행 이력을 “73차 조건 1~5 전부 충족”으로 종결하지는 않는다.** 계산 결과가 무효라는 판정도, 전체 suite가 PASS라는 판정도 아니다.

| 요청 §5 | 답 |
| --- | --- |
| ① 판 3 실행 / 이전 재승인 | 판 3의 코드·계획·산출·보존 연결은 확인했다. 다만 역할/투영 편입 단계가 미완이고, 판 1의 두 번째 `--resume` 사전 승인은 제출 자료로 확인되지 않는다. 전체 이력의 무조건 준수 판정은 **아니오**다. |
| ② G74-3 분류 | **(c) 진단용·활성 주장 비사용을 유지하되, 이를 표현할 최소 명시 계약 (b)을 함께 마련**하는 방향을 권고한다. 새 투영·세대·active claim을 한꺼번에 만들지 않는다. 현재 적색은 알려진 미완 상태로 보존할 수 있지만 정상 기준선/다음 실행 GO로 인정하지 않는다. |
| ③ G74-1·G74-4 시점 | 이번 결과를 버리고 재계산할 이유는 발견하지 않았다. 그러나 **다음 grid/resume 및 다음 archive 게시 전에** 해당 결함을 닫아야 한다. 다음 보완 묶음에서 처리하는 것을 권고한다. 이번 리뷰 자체는 수정·실행 승인 아님. |
| ④ G74-2 | 삭제·운영 등록부 편입·class 재작성 없이 과거 실패 증거로 보존하는 방향은 수용한다. 현재 전달본에는 고아 JSON 원문이 없으므로 그 내용/해시는 독립 확인하지 못했다. WSL 재사용 전 영향 범위를 확인해야 한다. |

이번에 독립 확인한 것은 **기존 자료의 바이트·구조·저장 행/조건 집합**이다. 새 grid/fit/scoring, pytest/smoke, projection 게시, archive/restore/make_receipt/attach, COMSOL/Java 실행은 하지 않았다.

## 2. 독립 확인한 결과

### 식별·계획

- 마지막 RUN_SCOPE 코드: `7a7945564e6a94803b4d3bc72e8202534189ccdb`.
- 실행 HEAD: `e34eea8455d87f8e33c6ae7113fe3d16ddb600e3`.
- 57개 RUN_SCOPE 파일의 경로+바이트로 계산한 source digest: `c2ef1a811e70bb4c`.
- 코드→실행 HEAD, 코드→Gate74 HEAD의 RUN_SCOPE diff 모두 **0 bytes**.
- 세 계획의 run_spec digest를 JSON 규칙으로 독립 재계산했다. `951b6136` → `69c3c826` → `e34eea84`에서 run_spec의 차이는 discharged cache SHA뿐이다. 그 밖의 grid/fit 축은 같다. 계획의 근거 문장은 별도 변경이다.
- WSL 보관 캐시 3개는 모두 1,035 bytes / SHA `5ab61b3799d4e18e0233038d6c9dccfb53882a027d36a8721af3796f4c33a064`다. Gabia 원래 캐시 파일 자체는 이 창 자료에 없으며, 그 식별은 계획·실행 기록으로 연결한다.

### 저장 데이터의 완전성

| 확인 항목 | 수신 독립 확인 |
| --- | --- |
| fits.parquet | 12,276행, 조건 3,069개. `(cond_id, objective)` 중복 없음. 각 조건에 네 목적함수 정확히 1개씩. |
| curves.parquet | 920,700행의 저장 시계열, 고유 조건 3,069개. fits 조건 집합과 같음. |
| failed.csv | 924행·924개 고유 조건, 전부 `infeasible:` 사전 제외 사유. 곡선 조건과 겹치지 않음. |
| 전체 조건 | 3,069+924=3,993개. 정렬 ID digest `7b08e97e129d0bf4`로 계획과 일치. fit 대상 digest `f4e633ebe62924a6`도 일치. |
| WSL 부분 기록 | 세 보관 디렉터리의 completed 924개가 모두 사전 infeasible ID와 일치. 완료된 feasible 조건은 확인되지 않음. |

따라서 **전달 데이터 기준으로 누락/중복 조건이나 failed.csv의 solver 실패 행은 발견하지 않았다.** 이는 모든 내부 solver 호출이 한 번도 실패하지 않았다는 전역 추적도, 저장 값의 물리적 참값 검증도 아니다. multistart 저장 파일의 행 수도 별도 기록했으며 이를 모든 내부 최적화 평가 횟수로 해석하지 않았다.

### 묶음·영수증·등록부

- `artifacts/grid_fit_v5`: payload index 포함 **29파일 / 27,313,017 bytes**. 정확 집합과 각 payload SHA 모두 일치.
- payload index SHA `4cd2c0f89a07da834680e4a69d75391241a0930819174fc98cf52045f7519c42`.
- receipt core는 실제 YAML 직렬화 규칙으로 재해시하여 `2aadd24b1de88b070e48bdda428050e6475fa7a245c4571df4771ca04ffde83a`와 일치했다.
- receipt의 fits/source hash, sealed summary 바이트, 원장 `evidence.out`과 restore_map/receipt의 실행 자리, validator 소스 파일 식별이 맞는다. sealed summary의 semantic SHA도 독립 계산해 일치했다.
- **33개 provenance 검사·empty-root restore·재채점은 송신 측 실행 기록**이다. 수신자는 이 실행을 반복하지 않았다. 임시 `_rescored_summary.yaml` 실물은 전달 묶음에 없으므로 재채점 쪽 출력의 원문 바이트까지 독립 재검산했다고 쓰지 않는다.
- 실행 전후 등록부 snapshot은 실제 저장소 파일 해시와 일치한다. **367→369**, 기존 367개 바이트 불변, 신규 두 기록은 grid/fit의 canonical·sealed 등록이다. 이 class는 추론상의 canonical claim과 다르다.
- `validator_tree_dirty: true`는 그대로 유지한다. 실행 산출물/원장 등이 생긴 뒤의 validator stamp와 시작 코드 식별은 다른 주장이다. 현재 code digest가 같다는 이유로 dirty 기록을 false로 바꾸지 않는다.

전체 pytest `20 failed / 1859 passed / 2 xfailed`, smoke rc0, docs-lint `20 failed / 336 passed` 및 실패 목록 일치는 **송신 보고**다. 수신자가 전체 suite를 다시 돌린 수치가 아니다. 현재 cohort 모순·누락 항목은 소스와 자료에서 직접 확인했다.

## 3. Gate73 조건별 재판정

| Gate73 §6 | 판 3 / 전체 이력 판정 |
| --- | --- |
| 1. 실행 기계에서 계획 생성·커밋, cohort 연결 | 세 판의 commit/spec 결속은 확인. 판 3은 실행 전에 계획을 포함한다. 다만 계획 때의 prospective 연결이 완료 후 유효한 projection membership까지 보장하지 못했다. E9와 기존 cohort 계약의 공백이다. |
| 2. 최종 승인 HEAD, 코드 불변, clean 시작·입력 | 판 3의 고정 HEAD/코드/입력·산출 식별은 정합적이다. `status_before.txt`는 빈 파일이고 실행 manifest는 RUN_SCOPE clean을 기록한다. 이는 전체 세션 모든 파일 불변 증명이 아니다. WSL `status_before2.txt`에는 미추적 항목이 있으므로 이전 판까지 “모두 clean 시작”이라고 합치지 않는다. |
| 3. E6 창·등록부 보존 | +2/기존 367 불변은 독립 확인. 중간에 다른 publisher/pytest/commit이 없었다는 것은 송신 운영 기록의 범위이며 전역 process audit가 아니다. 병행 QE 프로세스는 기록대로 별도 작업이다. |
| 4. 정확 범위·후속 절차·실패 처리 | 판 3은 grid→fit→finalize→report 및 archive→receipt→attach 기록과 산출이 연결된다. 사람의 역할 문구/주장 체계 편입은 미완. 판 1의 추가 resume는 아래 R1 때문에 준수 종결 불가. |
| 5. 한계·역할 비승격 | `diagnostic`, E1/E2/E4 한계 유지와 활성 주장 미사용은 수용한다. 아래 R2의 과도한 원인/“0회” 문구는 좁혀야 한다. |

이전 리뷰가 E9의 cohort 연결을 요구하면서 **실행 완료 roster와 projection roster의 동일시**를 놓친 점도 인정한다. 그 공백을 송신자만의 잘못으로 돌리거나, 이제 와서 기존 미검증 E1을 전면 해결해야 한다고 조건을 확대하지 않는다.

### R1 — `--resume` 한도·재승인 증거를 분리할 것

`docs/08_REVIEW_RESPONSE.md:8138~8143` 및 두 원시 로그는 다음을 보여 준다.

1. 18:18 `resume_20260926T091848Z.log`: attempt `591c0939…`, cache/spec 불일치로 거부.
2. 18:20 `resume2_20260926T092009Z.log`: **같은 attempt로 다시 resume**, 캐시를 옮긴 뒤 gate 통과, baseline 재계산·캐시 저장, 이후 종료.
3. 그 뒤 release/new attempt 및 별도 계획 교체 기록이 이어진다.

따라서 “명시 resume 1회”로 전체를 요약할 수 없다. 첫 거부가 compute 이전이었다고 해서 호출 횟수에서 자동 제외되지는 않는다. 완료 조건 0개도 재시도 허가가 아니다. 18:20 전에 해당 추가 호출과 캐시 이동을 승인한 원문이 있으면 그 출처·시점·범위를 덧붙일 수 있다. **없으면 ‘원 승인 한도 밖 추가 호출, 사전 재승인 확인 불가’로 기록**한다. 뒤의 `69c3c826/e34eea84`가 앞선 추가 호출을 소급 승인하지 않는다.

두 계획 교체의 기술적 식별·캐시 결속 자체는 확인했다. 원장에 기록한 사용자 결정/release 수행은 그 출처대로 보존한다. 현재 증거로 무단 행위를 확정하는 것도, 모든 재승인이 증명됐다고 닫는 것도 하지 않는다. 이 공백이 별도로 봉인된 Gabia 결과를 자동 무효로 만들지는 않는다.

### R2 — 완료 수·원인·호출 주체 문구 정정

- **“조건 계산 0” → “저장 기록에서 완료된 feasible 조건 0”**. 워커가 시작되지 않았거나 solver 작업이 전혀 없었다는 뜻은 아니다. baseline 계산·캐시 쓰기는 로그에 있다.
- **VM 재부팅 관측과 OOM 확정은 다르다.** 전달된 설명의 uptime 보고는 보존하되, 메모리 한도 초과/idle/tmux 원인을 독립 확정한 것으로 쓰지 않는다. 원장 자체도 판별이 바뀌므로 시간순 설명과 가설을 구분한다.
- **“null이면 어떤 resume도 불가능/항상 거부”**는 너무 넓다. 정확히는 cache=true에서 계산으로 생성된 캐시를 그대로 둔 다음 live 축이 바뀌어 거부된다. 실제 두 번째 호출은 캐시를 옮긴 뒤 통과했다. 이것을 향후 권장 우회로 삼지는 않는다.
- **cohort 이동은 attach가 아니라 `finalize_leg()`**가 한다 (`tools/preserve.py:8383~8386`). attach는 이후 bundle 검증 상태를 바꾸는 단계다.
- JAX 로그에는 CPU fallback이 명시돼 있고 최종 조건 집합은 완전하다. 하지만 “loky 경고는 반드시 메모리 교체이며 유실은 반드시 특정 예외로 나타난다”까지는 이번 자료로 확정하지 않는다. 관측된 결과와 추정 원인을 나눈다.

## 4. G74-3: 권고는 진단 전용 + 명시적 비주장 계약

현재 g18 원장은 `legs=[grid_fit_v5, paired_fixed5_v4]`인데 `cross_leg_comparison=not_applicable_single_leg`다. 실제 `proj_g18/CURRENT`에는 paired_fixed5_v4의 projection만 있다. `claim_roles`와 `regeneration_capability`도 새 leg에 없다.

핵심 원인은 세 계약의 충돌이다.

- `tools/preserve.py:5836~5848`: 완료된 prospective 계획은 cohort `legs`에 있어야 한다.
- `tools/preserve.py:8383~8386`: finalize가 그 명부에 실제로 추가한다.
- `row_projection.py:4922~4929`, `tests/test_docs_lint.py:2432~2435, 2984~2993, 3007~3017`: 명부의 각 leg를 투영/주장 계약에 넣어 해석한다.

그러므로 **원장에서 grid_fit_v5 한 줄만 빼거나 lint에서 이 이름을 skip하는 해결은 불충분**하다. planned_index의 executed 결속이 깨지거나, 미래 같은 종류의 leg가 검증을 우회한다. `not_applicable_single_leg`를 `allowed_within_cohort`로만 바꿔도 없는 projection과 CURRENT 결속 문제가 남는다.

### 최소 수용 계약 — 필드 철자는 구현자가 확정하되 의미는 고정

1. **실행 이력과 투영 membership을 분리한다.** 원래 승인 cohort ID·planned/spec·attempt·영수증은 역사적 사실로 보존하고, “그 cohort에서 실행 승인받음”을 “그 cohort의 투영 파일을 보유함”으로 읽지 않게 한다. 현재 9개 executed leg를 조용히 삭제하거나 옛 계획을 재작성하지 않는다.
2. **명시된 `no_active_claim` 종류만 claim_roles가 비어 있을 수 있게 한다.** diagnostic라는 라벨만으로 모든 검사를 면제하지 않는다. 이 종류는 활성 claim에서 참조되면 거부해야 하며, 없는/알 수 없는 종류는 fail-closed다.
3. **full_bundle 증거 계약은 그대로 적용한다.** payload·receipt·실행 자리·소스·상태 일치를 요구한다. 원자료가 실제 있는 경우의 regeneration capability는 사실대로 기록하되 projection 생성/검증 완료와 구분한다.
4. **기존 projection cohort/claim 보호는 그대로 유지한다.** g18의 기존 paired 자료, frozen cohort, generation/role compatibility, 투영 seal/명부 검사는 약화하지 않는다. 새 실행이 projection을 만들지 않았다는 이유로 기존 자료를 다시 계산할 필요는 없다.
5. **생산 경로와 consumer를 함께 맞춘다.** planner/planned_index/finalize 및 원장/claim/projection 소비자가 같은 분류를 읽어야 한다. 이는 단순 lint 이름 예외가 아니며, 생산 함수 수정 시 RUN_SCOPE/validator 식별도 다시 확인한다.

선택 (a)의 “투영 생성”, “세대 등록”, “새 active claim 추가”는 원래 별개 결정이다. 투영을 만들었다는 이유만으로 E1 독립 producer 검증이 생기거나 새 과학 주장이 성립하지 않는다. 지금 요구한 진단 결과 수용을 위해 세 단계를 강제로 수행할 필요는 없다.

### 한정 회귀 종결 목록

새 전체 체계를 무한 재설계하지 않는다. 최소한 다음을 고정한 회귀면 이번 분류 경계의 수용 여부를 판단할 수 있다.

1. 현 grid_fit_v5 자료로 **진단 전용 양성**: 실행/영수증 결속 유지, projection membership 아님, active claim 없음.
2. 같은 자료에 active claim 참조를 붙이면 거부.
3. 같은 종류에 out/receipt/hash/필수 상태를 빼거나 바꾸면 거부.
4. 분류 누락·알 수 없는 분류·원장/소비자 간 분류 모순 거부.
5. 기존 g18/frozen/claim 양성 및 변조 거부는 유지.
6. 신규 prospective→finalize→archive receipt 연결의 **inert/fixture 통합**이 자기 lint와 정합적이고, 실패 시 원장이 불변.

현재 실패 20개는 알려진 미완으로 보고서에 남겨도 된다. 그러나 xfail/skip/광범위 필터로 덮고 green이라 부르지 않는다. 분류 보완 뒤 실제 실패 목록을 다시 보고해야 하며, 현재 20개가 공유 선행 오류 뒤의 모든 잠재 오류를 이미 보여 준다고 보증하지 않는다. 이번 리뷰는 그 재시험의 실행 승인이 아니다.

## 5. G74-1·G74-4: 재계산 없이 닫되 다음 사용 전 필수

### G74-1 — null 캐시 실행이 자기 재개 축을 바꾸는 문제

`src/grid.py:465~467`은 null 계획을 force 계산으로 보내고, `src/baseline.py:229~241`은 cache=true일 때 결과를 저장한다. 다음 `live_grid_axis()`(:519~529)가 그 파일 SHA를 읽고, `tools/preserve.py:3800~3805`가 원래 spec과의 불일치를 거부한다. 거부 자체는 올바른 결속 검사다.

현재 최소 권고는 **(ii) 캐시를 미리 고정한 계획만 허용하는 제한을 명시**하는 쪽이다. 이를 정책으로 택한다면 계획 도구만 막아 수기/직접 경로가 남지 않도록 실제 새 실행 진입에서도 일관되게 검사한다. cache=false 등 적용 밖 모드를 함께 금지할지는 별도 명시하고 암묵적으로 바꾸지 않는다. `plan_leg.py` 자체는 docs 아래 RUN_SCOPE 밖이므로, 그 파일만 바꾸면 자동으로 source_digest가 바뀐다는 설명도 정확하지 않다.

null 지원을 계속하려면 (i)의 비저장 계산과 재개·서명 일관성까지 검증해야 한다. (iii)에서 **live 축을 claim 값으로 단순 덮어써 비교를 없애는 방식은 받지 않는다.** 승인된 입력과 실제 소비 바이트의 결속을 유지해야 한다.

최소 반례는 null/캐시 부재 초기 상태, 실행 뒤 캐시 생성 상태, 고정 SHA 양성, 캐시 변조/부재 거부다. 기존 3,069조건을 다시 계산해 회귀를 만들 필요는 없다.

### G74-4 — 단일 archive가 다른 index 항목을 지우는 문제

`scripts/archive_results.sh:248`의 `runs={}`와 :322~330의 전체 index 쓰기를 확인했다. d9f8791c에서 v4 네 entry가 사라졌고, 현재는 **각 entry의 YAML 블록 원문 바이트가 e34eea84와 같게 복원**됐다. 새 grid_fit_v5 entry도 d9f8791c 원문과 같다. v4 네 묶음 파일의 commit diff는 0이다.

현재 손상 복구는 수용하지만 **버그는 여전히 열린 상태**다. 다음 단일/부분 archive 호출 전에 고쳐야 한다. 우선은 검증된 신규 entry와 기존 검증 가능한 index의 병합을 권고한다. 기존 entry를 새로 검증한 것처럼 stamp를 갱신하지 않고, 무관한 항목 보존·동명 충돌 명시 거부·검증/쓰기 실패 시 기존 index 불변·원자적 최종 교체를 요구한다. 기존 index가 불명확하면 비우고 쓰지 말고 중지한다. 단일 호출 자체를 게시 전에 거부하는 보수적 대안도 가능하다.

최소 회귀: 기존4+신규1, 동일 entry 재호출, 같은 이름/다른 identity, 신규 검증 실패, index 쓰기 실패의 보존이다. 이는 향후 보완 승인 범위의 제안이지 지금 실행하라는 지시가 아니다.

코드 변경 후 validator identity는 새 버전으로 별도 기록한다. 기존 producer source를 새 digest로 덮어쓰지 않는다. 두 실물 receipt 재검증이 필요하다면 **기존 묶음의 별도 복사본/승인된 검증 작업**으로 다루고, 이번 검토가 restore/재채점 허가였다고 해석하지 않는다. 현재 두 receipt 원본도 보존한다.

## 6. G74-2와 다음 작업의 유한 경계

WSL `status_before2.txt`와 snapshot에는 `f3f50901…json`이 추가돼 있다. 코드상 canonical 등록은 실행 출처/권한의 종류이지 완료/과학 claim의 승인 표지가 아니다. 부분 산출물에 붙었다는 이유만으로 임의 삭제·class 교체를 요청하지 않는다. 지금 Gabia/저장소 369개와 이 WSL 레코드를 합치지도 않는다.

가능한 최소 기록 보충은 **이미 존재하는** 고아 JSON 원문/크기/SHA, 해당 partial manifest 식별, 최초/최종 snapshot 및 현재 소비 대상 여부다. 새 registry 측정/복원/이관을 이번 승인으로 수행하지 않는다. 원문을 확보하지 못하면 “송신 보고·원문 미전달”로 유지한다. WSL을 다음 운영 환경으로 쓰려면 그때 authoritative registry 위치와 미추적 영향부터 별도 확인한다.

다음 회신은 다음 여섯 항목으로 한정하면 된다.

1. R1의 추가 resume 승인 출처 또는 확인 불가/편차 인정 기록.
2. R2의 완료 수·원인·finalize 주체 문구 정정.
3. 진단 전용 분류의 구체 계약·최소 생산/소비 변경 및 여섯 회귀.
4. G74-1의 선택 정책과 경계 회귀.
5. G74-4의 index 보존 회귀 및 기존 복원 바이트 유지.
6. 기존 결과/등록부/영수증 보존과 새 validator 기록의 범위 구분.

**새 grid/fit 본 실행은 필요하지 않다.** 과거 승인 공백을 새 실행으로 덮지도 않는다. 20개 적색을 보존한 채 제한 보완을 계획할 수 있지만, 실제 변경·시험·receipt 재검증은 사용자가 그 범위를 별도로 승인해야 한다. 검토자는 원장, class, 결과, 설정을 변경하지 않았다.

## 7. 근거와 검증 한계

`IDENTITY.json`, `PLAN_HISTORY.json`, `DATA_AUDIT.json`, `PARQUET_DATA_AUDIT.json`, `SUPPLEMENT_AUDIT.json` 및 diff와 `reference/`의 고정 원문을 함께 제공한다. 검토 checkout tracked DD 2,681개는 포장 전 다시 크기/SHA를 대조한다. 이는 해당 checkout의 보존 확인이며 원격 서버 전체 파일/프로세스 보존을 뜻하지 않는다.

검토자 도구의 중간 오류와 정정은 `REVIEW_ACTIVITY.md`에 분리 기록했다. 송신 suite 횟수/실패에 합산하지 않았다. 이 패키지에는 대형 Parquet 원본 전체를 재포장하지 않고, 고정 Git 좌표·바이트 식별·독립 데이터 검사 결과와 필요한 텍스트 증거를 담았다. 원래 결과 묶음의 대체 백업이 아니다.

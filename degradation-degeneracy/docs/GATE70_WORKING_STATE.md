# 70차 게이트 리뷰 작업 상태 (정본)

판정: **현재 본 실행 NO-GO · 유한 종결 조건 E1~E10 고정** — 2026-09-24 접수. 리뷰어 고정 검토 HEAD `8568f782db3acbf00d872ce5527147258c00bec7`
(= 요청문 커밋, 발송문의 두 SHA 가 같았다), 판정 대상 코드 `f0dfaff3` · `source_digest 5e660a8c73d5663a` (리뷰어 직접 계산 rc 0),
코드 대상→HEAD RUN_SCOPE diff 0 bytes. **새 P1 1건 (G70-N1) · F50b(E7) 수용 · E8 종결 유지 · 본실행 GO 없음 · 기한 경과가 GO 를 자동 발행하지 않는다.**
상세는 원장 §90(접수)·§91(대응), 패키지 원본 `docs/22p_gap/gate70_review/` (zip `7d49836e…`, MANIFEST 78 payload · 커밋 뒤 blob 대조 78/78,
`-text !eol` 규칙 `05a8026b` 먼저 → 패키지 `4ed1a540`).

62차 이후 첫 **GO 요청**이었고, 리뷰어의 답은 "끝없는 게이트를 요구하지 않는다 — 종결 목록을 E1–E10 으로 고정한다. 조건이 닫힌
**최종 코드와 실행 명세를 확인한 뒤** GO 또는 명시적 조건부 GO 를 판단한다." 이 문서는 그 목록을 하나씩 닫는 작업의 좌표다.

## 발견 원장

| ID | 등급 | 무엇 | 상태 |
|---|---|---|---|
| G70-N1 | **P1** | `run.sh --mode all` 이 grid/fit 하위 argv 에 `--may-open` 을 붙이고(`:526` `:541`) 그 argv 를 `"$0"` 로 넘긴다(`:558–559`). 셸 parser(`:165–211`)에는 그 옵션이 없어 `:209` 에서 `알 수 없는 인자: --may-open` rc 1. 57차 P0-1 부터 있던 결함 — **F50b 회귀가 아니다.** dry(`_dry_all`)는 출력에서 멈추고 strict smoke 는 개별 모드라 아무도 안 봤다 | **닫음 (`ae3d3152`)** — RED `tests/test_runner.py::test_g70_n1_mode_all_child_argv_is_accepted_by_the_shell_parser[grid|fit]` (두 파라미터 모두 `알 수 없는 인자: --may-open` 실패를 본 뒤) → `all` 의 두 줄 삭제 · grid 분기에 `RUN_SH_DRY` 경로(plan_gate 앞) · grid/fit 의 `--may-open` 추가를 dry 출력 앞으로 → GREEN. 변이 `mode-all-does-not-pass-may-open-to-the-shell-g70` 등록([grid] 만 빨개짐, `--emit-expect` 관측 그대로). planned leg/소유권 전달/finalize/archive 단계는 건드리지 않았다 |

## 종결 조건 표 E1~E10 (리뷰어 §5 를 그대로 옮기고 우리 상태를 붙인다)

| ID | 리뷰어 분류 | 필요한 종결 증거 (리뷰어 문장) | 우리 상태 (2026-09-24) |
|---|---|---|---|
| E1 | 미완 · 한정 실행에서 결과·출처 보증 한계 허용 | 강한 producer 주장을 쓰면 **`row_projection.py`** 의 projection/restart 두 압축 payload 소비 경로의 typed manifest·압축해제 hash·producer receipt (49차 원조건 — `archive_bundle.py` 의 fit 묶음만으로는 못 닫는다 · 내용 identity 와 운송 바이트 identity 구분 · 무조건 거부 회귀 아님). 쓰지 않으면 미검증 범위 명시 + 주장 제외 | **한계 라벨** (사용자 결정 2026-09-24 ("ㅇㅇ 그렇게 하고 71차 md 받자")) — GATE71 §1 문구 |
| E2 | 미완 · 독립 실행 코드 보증 한계 허용 | 독립 launcher 주장을 쓰면 실제 시작/import bytes 와 소비 receipt. 아니면 "자기 측정" 명시 (`source_digest` 는 디스크 자기 측정이다) | **한계 라벨** (사용자 결정 2026-09-24) |
| E3 | **기존 실행/보존 계약 차단 유지** | lifecycle finalize 가 typed receipt(`execution-receipt/v1`, `tools/preserve.py:2979` `:3245` 검사기는 있다)를 실제로 소비 · 상태·bundle 식별 결속 · `_declared_index_members` 가 None 을 돌려주면 대조를 건너뛰는 경로(`:7492–7523`) fail-closed · 정상/부정/부분 회귀 | **닫음 (`876429562f6a69b59793c70700cb5b375391ab67`, 원장 §92)** — index fail-closed·YAML·구성원 sha · `attach_bundle_evidence` typed 영수증 소비 |
| E4 | 미완 · 독립 변이 replay 보증 한계 허용 | 미재생 또는 명시적 **표본** 범위(선택·seed·분모·미수행)로 한정. 전수 독립 replay 완료라 표시하지 않음 | **한계 라벨** (사용자 결정 2026-09-24) |
| E5 | **부분 구현 · class 소비 계약 차단 유지** | `_read_exec_class_at`(`:4950–4974`) 이 class enum + content_id 만 본다 — 두 키만 있는 레코드, `sealed=[]`·`evidence=17`·`recorded_at=false` 레코드를 수용했다(리뷰어 fixture). `resolve_execution_class` 는 `sealed` truthiness(`:5097–5111`). typed modern/legacy variant · content/seal 결속 · writer→reader→promotion 회귀. 과거 class 임의 재작성 금지. (요청문의 "미착수" 는 **부정확** — identity·seal·capability·lock·read-back·충돌 거부는 있다) | **닫음 (`876429562f6a69b59793c70700cb5b375391ab67`, §92)** — typed variant 둘 · 손상은 오류 · `sealed is True` · tracked 367 재작성 0 |
| E6 | **새 실행의 운영 전제** · 전체 과거 이관과 분리 | 읽기 전용 영향 지도 `docs/22p_gap/registry_impact.md`(약속했으나 HEAD 에 없음) + 새 실행 권한 영역의 격리/배타 사용 및 전후·delta 보존. 현재 `tests/test_compare.py:940–950` 는 운영 등록부에 synthetic canonical 을 만들 수 있고 `tests/conftest.py:154–188` 은 시작 때 없던 JSON 을 소유권 구분 없이 지운다 — 다른 실행의 합법 기록도 삭제 대상. 한계 라벨로 대체 불가 | **닫음 (`876429562f6a69b59793c70700cb5b375391ab67`, §92)** — `registry_impact.md` · 시험 authority 격리 · 운영 불변 검사 · 배타 운영 창(§93) |
| E7 | **F50b 제한 수용** | 비교 규칙 유지 · 최종 식별에서 통합 회귀 확인 · `git_dirty` 제거 불요 (Q6: "범위 밖 문서 수정도 무조건 dirty" 라는 요청문 전제가 틀렸다 — git_info 는 RUN_SCOPE 기준) | ✔ |
| E8 | 69차 한정 종결 유지 | 관련 변경 없으면 반복 심사 안 함 | ✔ |
| E9 | **실행 명세 미완 + G70-N1** | 정확한 argv/config/입력/출력/leg/cohort/run_spec · 새 prospective 승인 · archive/검증 순서 · 실패 처리. Gate63 §0 적용성 표 1회 (immutable publication · class/삭제 절차 · 비-grid 진입점 · retention/power-loss · publisher principal · truth_provenance 를 `이번에 사용/완료 근거`·`범위 제외`·`명시적으로 보증하지 않음` 으로). 과학 목적 고정(`synthetic grid/fit 재실행` vs `Stage3 primary 비교`). 당장 빠진 것: `./run.sh` 는 `--mode` 필수 rc 1 · 기본 OUT 은 timestamp(≠ `results/grid_fit_v4/`) · planned index 8 = 과거 executed, `grid_fit_v4` prospective 항목 없음 · `all` 체인은 archive 를 안 부르고 finalize 는 `preservation_pending` | G70-N1 닫음 · **명세 §93 / GATE71 §2** · 과학 목적 = synthetic grid/fit 재실행 (사용자 결정 2026-09-24) |
| E10 | **최종 통합/환경 증거 미완** | 실제 대상 Linux 에서 **최종 식별**의 전체 회귀 + 작은 전 과정 smoke · positive-control 공백 해소(`test_a_smoke_run_cannot_be_promoted_to_a_canonical_report` 의 `results/grid_fit_v4` 양성 경로 — skip 이나 가짜 class 레코드로 녹색 만들지 않음) · "1 failed/1804 passed rc 1" 과 "smoke rc 0" 은 다른 결과 — full suite 전부 통과라 적지 않음. 문서만 바뀐 커밋은 바이트 동일 근거로 기존 증거 재사용 가능 | **닫음 (`876429562f6a69b59793c70700cb5b375391ab67`, §92)** — 양성 fixture · 최종 식별 `0e6348be9ec80919e0f84ae246294cb6336e9545` 회귀 0 failed · 1855 passed · 2 xfailed (43:10) · smoke EXIT 0 |

## 여섯 질문의 답 (요약 — 원문은 리뷰 §6)

Q1 **아니오** (E9/E10 + Gate63 §0 적용성 빠짐, 대상은 최종 수정 commit) · Q2 **부분 동의** (E1/E2/E4 는 주장 축소로 가능, E6 은 실행별 운영 조건 필요) ·
Q3 **그 셋만으로는 아니오** (E6·E9·E10 을 더 닫으면 E1/E2/E4 를 명시한 한정 실행 GO 경로 있음) · Q4 **동의** · Q5 **아니오** (실제 통과/실패/미수행과
미닫힌 ID·영향을 적는다, `N/M` 은 보조) · Q6 **유지**.

## 이 라운드가 하지 않은 것 / 유지되는 경계

- 리뷰어: 제품 수정 0 · 본 grid/fit·COMSOL·보관 복원·class migration 0회 · 전체 pytest/strict smoke/mutation replay 는 수신 환경(Windows/3.12.14)에서 미실행 · `make_receipt.py` 미실행(실제 복원/검증 수반). 부수효과 1: 부검토자가 `precheck_leg_run` 을 불러 **빈 `docs/22p_gap/_claims/` 폴더 하나**가 리뷰 worktree 에 생겼고 Windows mount 검사 `BoundaryUnknown` 으로 중지 — claim/token/ledger/class 파일 변경 없음.
- 동봉 스크립트는 증거다. `agents/preservation_class/probe.py` 는 실패한 precheck 호출을 담고 있어 **원래 checkout 에서 재실행하지 않는다.**
- 우리: 리뷰어 스크립트 미실행 · 복원/class 변경 없음 · 본실행 시작 안 함.

## 배운 것

- **"dry 출력이 있다" ≠ "그 argv 가 실행된다".** 57차부터 `all` 의 하위 argv 가 셸 parser 를 못 넘었는데 dry 회귀는 문자열만, strict smoke 는 개별 모드만 봐서 13 라운드 동안 아무도 보지 못했다. 회귀는 이제 dry 출력을 **실제 하위 셸에 넣어** rc 와 Python argv 까지 본다.
- RUN_SCOPE(`run.sh`)를 고치면 보존 영수증의 검증기 identity 가 낡는다 — F50b 때와 같은 절차(clean 트리에서 `make_receipt.py`, 원장은 검증기 digest·core sha 두 값만)로 닫는다. 산출물의 실행 digest(`d50295f9…`)는 안 움직인다.
- 라벨은 `N/M` 이 아니라 **미닫힌 ID 와 실제 명령·rc·실패/skip/xfail** 을 적는다.

## 71차 회신 (2026-09-25) — 한정 GO 보류 · 잔여 E3-R(P1)·E9-R(P2) → 둘 다 닫음 (원장 §94·§95)

E3-R: 소비자가 짝·실제 일치·source fits·복원 자리·봉인 summary 를 다시 대조 (`82854571`, `tests/test_gate71_defensive.py` 14, 변이 3). E9-R: 실패 즉시 정지 → 명시적 `--resume` 1회 → 재승인 (D6). D7 승인 HEAD · D8 `unset CANONICAL_RUN LEG` · D9 E4 = 11 · E6 requirements 복사. 판정 대상 `82854571` · `source_digest 518d4f63076b77e3`.

## 72차 회신 (2026-09-25) — 한정 GO 보류 · 잔여 E3-R 원장 `evidence.out` 결속(P1) → 닫음 (원장 §96·§97) · E9-R 수용

`_assert_ledger_run_bound`: out 필수(부재 = 미결속 거부) · full_bundle 멱등 반환보다 먼저 (`7a794556`, `tests/test_gate72_defensive.py` 10, 변이 g72 1 + g71 재조준). 실물 `paired_fixed5_v4` 는 out 없는 소급 다리 — 소급 채우지 않고 미결속 거부. 판정 대상 `7a794556` · `source_digest c2ef1a811e70bb4c`.

## 73차 회신 (2026-09-25) — **E3-R 종결 수용 · 조건부 한정 실행 GO** (원장 §98)

코드 `7a794556` · `source_digest c2ef1a811e70bb4c` 유지 + 사람이 실행 기계에서 생성·확인한 `grid_fit_v5` prospective 항목을 커밋한 최종 승인 HEAD + E6/E9 조건. 새 차단 없음. 현재 prospective 없음 = 아직 실행 가능 상태 아님.

## 한정 실행 1~3차 시도 (2026-09-26, WSL) — 전부 외부 종료 · **G74-1 null 캐시 계획은 재개 불능** · 재승인 (원장 §99)

1차 승인 HEAD `951b6136`(null 캐시 항목). 시도 1 WSL idle 종료 · `--resume` 1회 거부(`97585418 ≠ e7cc8713`) · 시도 2 VM 재시작(18:27 부팅) · 시도 3 tmux 세션 종료(내 명령 블록의 줄 갈림) + 중복 호출 거부. 조건 계산 0. 기제: null 계획 → `force=True` 재계산이 캐시를 **저장** → 다음 프로세스의 `live_grid_axis` 가 그 sha 를 넣어 봉인 spec 과 어긋남 (RUN_SCOPE 수정 대상, 지금 안 고침). 고아 등록 레코드 `f3f509…` (지우지도 커밋하지도 않음). 재승인: 항목 교체 — 캐시 `5ab61b37…` 결속, `run_spec_digest e7cc8713bb88d941…`. 74차 요청문에 G74-1·G74-2·편차 3건을 싣는다.

## 4차 (WSL) VM 재시작 · 재개 성립 실측 · Gabia 이전 · 재승인 2 (원장 §100)

4차도 `grid 0/3069` 에서 소멸 — VM 부팅 시각 관측(19:21 시작 → 19:24 부팅), ~~메모리~~ 원인 미확정 (74차 R2). 캐시 결속 계획에서는 `precheck` 가 `resume` — G74-1 의 반대편 증거. 사용자 결정으로 Gabia(`kserver116-27`, 20 proc, 62 GB)로 이전, 캐시 `66d84e76…`, `run_spec_digest 0838df84…`. 승인 HEAD = 이 커밋.

## 한정 실행 완주 (2026-09-26, Gabia) — full_bundle · current_validated (원장 §101)

grid 3069 (solver 실패 0) → fit 12276 행 → finalize → report → archive → 영수증(core `2aadd24b…`) → attach. 등록부 367 → 369. 데이터 커밋 `d9f8791c`. 실행 뒤 발견: **G74-3** cohort/투영/주장 lint 가 투영 없는 다리를 받지 못함 (docs-lint 적색, 사람 결정 대기) · **G74-4** `archive_results.sh <run>` 이 인덱스를 그 묶음만으로 덮어씀 (v4 네 항목 복원). 그 전 발견: G74-1 null 캐시 재개 불능 · G74-2 WSL 고아 레코드.

## 74차 회신 (2026-09-26) — **완주·보존 증거 제한 수용 · 주장 편입·전체 종결 보류** (원장 §102)

수신 독립 확인: fits 12,276 = 3,069 × 4 · 곡선/failed 집합 일치 · 묶음 29/27,313,017 · receipt core 일치 · 등록부 +2/367 불변 · v4 index 복원 확인. R1: 판 1 의 18:20 호출은 같은 attempt 의 `--resume` 2회째 — 한도 밖, 사전 재승인 없음 (대화 기록으로 확인, 편차 인정). R2: 문구 5건 취소선 정정. G74-3 권고 = (c)+(b) 진단 전용 명시 계약 (여섯 회귀). G74-1·4 는 다음 사용 전 수정 필수, 재계산 불필요. 항목 3~6 은 **사용자 범위 승인 대기** — 그 전에는 코드·시험·receipt 재생성 없음.

## 74차 대응 (2026-09-26) — 항목 3~6 전부 (사용자 범위 승인) · 원장 §103

G74-3 (c)+(b): `claim_scope` 다리마다 명시 · cohort `executed_legs` ≠ `legs` · finalize 라우팅 · planned_index/lint 동일 분류 · `row_projection.py` 불변(봉인 불변). G74-1: 고정 캐시 SHA 계획만 진입 (`_assert_prospective_plan_is_startable`). G74-4: index 병합·동명 충돌 거부·원자 교체. 코드 `ebfb853d` · `source_digest 27390883eb132941`. 영수증 원본 history/ 보존 후 재생성(`8765068a`; 차이 = validator 식별·core·stamp 뿐). `tests/test_gate74_defensive.py` 41 node (RED 36) · 변이 6/6. 전체 회귀 `7ec4e234`: 0 failed · 1922 passed · 2 xfailed · smoke rc 0 · docs-lint 적색 20 → 0.

## 75차 회신 (2026-09-27) — 부분 수용 · 종결 보류 (원장 §104)

1/2/4/6 수용 · 3 은 **G75-N3**(진단 소비자 out 결속) · 5 는 **G75-N1**(index 실패 rc 소실, P1) · **N2**(중복 YAML 키). row_projection 불변 수용 · current_validated 유지 가능 · 새 본 실행 불필요. 문구 정정 반영. 다음 범위 N1/N2/N3 — 사용자 승인 대기.

## 75차 대응 (2026-09-27) — N1·N2·N3 전부 (사용자 범위 승인) · 원장 §105

G75-N1: index 최종화 실패 → 즉시 nonzero · 명시적 미완(승격된 묶음 표기) · 안내 차단 · tmp 삭제. G75-N2: `tools/index_yaml.py::load_index_strict` 한 함수(중복 키·merge key `<<` 거부·형식)를 archive 세 reader 가 전부 사용. G75-N3: 진단 소비자가 생산자와 같은 함수로 `out` 결속 대조. 코드 `23c361ed` · `source_digest 1c67a748598baadb` (두 번 이동: `10be3a69` cd2408… → `23c361ed`). 영수증 원본 매번 history/ 보존 후 재생성(현행 `baf109b5`). `tests/test_gate75_defensive.py` 22 node (첫 판 RED 11/~~19~~18 (76차 정정)) · 변이 4/4. 전체 회귀 `4d8dfc52` 1 failed(패키지 사본 claim 관할 — `cd272a89` 부터) → `5b10a79f` 에서 제외 규칙 추가 후 **0 failed · 1944 passed · 2 xfailed · smoke rc 0**.

## 76차 회신 (2026-09-27) — **N1·N2·N3 종결 수용 · 74차 1–6 + 75차 잔여 전체 종결 · 새 실행 GO 없음** (원장 §106)

독립 격리 검사 44건 · 2,868 파일 보존 · 패키지 87/87. 비차단 정정 3건(등록부 369 · history 3+현행 1 · 첫 RED 18 node) 취소선 반영. 남는 한계는 리뷰어 문장대로: replace 뒤 출력 오류는 rc 만으로 확정 불가, E1/E2/E4·WSL 고아·과학적 수렴 미검증은 해소되지 않음.

## 다음 단계 결정 (2026-09-27) — 사용자 위임 → **단계 3 계약 v4 구현 전 재심사 (77차)** · 원장 §107

grid_fine 재실행은 권고하지 않았다 (grid_fit_v5 와 산출이 같고 지지할 v6 주장이 없다). `docs/22p_gap/GATE77_REQUEST.md`: §13.1 묶음 상태 갱신 초안 · §11 위치(12 완주 → 13 미착수) · 13 앞 여섯 결정 제안 · 질문 5. 실행 GO 아님 · RUN_SCOPE 불변.

## 77차 회신 (2026-09-27) — 방향 수용 · 12 전체 완료→13 일괄 착수 불수용 · 설계 정정 3건 (원장 §108)

G77-N1(P1): 로컬 완주 ≠ retention provider 증거 → 단계 12 를 12-L(실물)/12-P(부분)로 분리. G77-N2(P1): primary 는 §7 그대로 grid·no-warm·같은 base·bank·B, Δ 하나 + 네 칸 분해; base-retained 는 secondary. G77-N3(P2): 미정은 최종 B 뿐, ladder/max/중단/floor/tolerance/stratum/자원 사전 고정, §9.4 필드는 의존 순서대로. → `GATE78_REQUEST.md`. 제한 오프라인 구현 = §3.2 단계 1+2 — **사용자 승인 (2026-09-27): 78차 회신 뒤 착수 · 보존 profile 선택 1 유지.**

## 78차 회신 (2026-09-27) — G77-N1·N3 종결 · G77-N2 잔여 G78-N1/N2 · 단계 1+2 수정 조건부 적합 (원장 §109)

단계 1: GATE78 §2.1 관측 쌍 key(obs_key) · N/n/m + inclusion mask · Δ_cc vs 전체 집합 bound · 5% 는 gate 완화 아님 (`3e995c4f`). 단계 2: `src/fitting.py` restart 행 converged·n_eval·termination_status(native last/best·outer) · restart_errors_json · `src/io.py` 깨진 parquet 발견 (`3dc269d8`, RED 9/13). 영수증 재생성 `194b1a55` (validator c78d7969ef49fd07 · 재채점 = 봉인 summary → 수치 불변 실물 증거). 변이 5/5.

## 79차 요청 (2026-09-27) — 원장 §110

전체 회귀 `f90a9c89` 1 failed(계약 줄번호 인용) → `c77674f6` **0 failed · 1958 passed · 1 xfailed · smoke rc 0**. 25차 발견 9(깨진 parquet ArrowInvalid) xfail → PASS. `GATE79_REQUEST.md` 발송.

## 79차 회신 (2026-09-28) — G78-N1·N2 종결 · 단계 1 종결 · 단계 2 는 G79-N1(P2) 정정 뒤 종결 (원장 §111)

G79-N1: legacy `converged` = 마지막 **유한** round 에서 갱신한 success (없으면 False) — 설명만 틀렸고 계산 경로 불변. docstring·주석 정정 · `g79_03c`/`03d` 동작 고정 · 변이 1 (`6ffa98d4` · digest eda3feb8f4536511). 영수증 `184d34dd`. 전체 회귀 `184d34dd` 2 failed(계약 줄번호 · fixture timestamp 충돌) → `517f25ff` **0 failed · 1960 passed · 1 xfailed · smoke rc 0**.

## 80차 회신 (2026-09-28) — **G79-N1 종결 수용 · 단계 1+2 한정 범위 종결 · 잔여 P1/P2 0 · 실행 GO 아님 · 단계 3 착수 승인 아님** (원장 §112)

패키지 `docs/22p_gap/gate80_review/` (zip sha256 `17e5b50b…` · MANIFEST 28 · 규칙 먼저 `bf6fa29e` → 풀기 `ac674aab` → 커밋 blob 28/28). 리뷰어: docstring 제외 실행 AST 79차와 동일 · `g79_03c`/`g79_03d` 가 요청한 두 비유한 경로를 정확히 검사 · 영수증 history 보존·허용 네 필드만 변경·원장 참조 일치 · 전체 시험 재실행 없음(발신 기록으로 소비). 비차단 이월(`normalize_restart_record` 혼합 키 행 정책) 그대로. 이 세션은 대피 서브 `claude/gate80-standby-9a26dd5f` (본진 `9a26dd5f` 동결).

## 81차 요청 (2026-09-28) — **단계 3 제한 구현 범위·사전 고정 사항 확인** 요청 발송 (구현 착수 아님 · 실행 GO 아님) (원장 §113)

사용자 "승인" = 범위 확인 요청의 발송 승인. 요청문 `docs/22p_gap/GATE81_REQUEST.md` — 범위 = GATE78 §3.2 단계 3 을 3-A 결속 · 3-B provider DAG · 3-C 행·검증으로 · 갈림 Q1–Q4 · 사전 고정 표 재확인 · 실행 경계 78차 §4 규칙. 코드 변경 0 (`source_digest eda3feb8f4536511` · RUN_SCOPE diff 0). **발송 SHA `88ac144a`** — 그 SHA 에서 clean 실측: docs-lint 358 passed · 전체 pytest 0 failed · 1960 passed · 1 xfailed (49:11) · smoke rc 0. 첫 실행은 환경(얕은 클론 · 의존성 미설치)으로 실패 → 설치·unshallow 뒤 같은 SHA 재실행 (원장 §113 신고). 서브 `claude/gate80-standby-9a26dd5f` 에서 발송 · 본진 `9a26dd5f` 동결.

## 81차 회신 (2026-09-28) — **수정 조건부 적합 · G81-N1·N2·N3 (P1 각) · 3-A/B/C 한 라운드 권고 · Q1·Q4 수용 · Q2·Q3 조건부 · 구현 착수 승인 아님** (원장 §114)

패키지 `docs/22p_gap/gate81_review/` (zip sha256 `e9def6bc…` · MANIFEST 34 · 규칙 먼저 `58980d60` → 풀기 `3dd4282a` → 커밋 blob **34/34** (zip blob sha 도 업로드본 `e9def6bc…` 과 동일)). 리뷰어: 요청 원문 = 저장소 blob 바이트 동일 · 80차 HEAD→요청 HEAD RUN_SCOPE 0 · 발송문 최종 실측은 발신 보고로 소비 (첫 실행 미확인 3 건 유지, 재시험 요구 없음). **N1** planned(사전 봉인) ↔ realized(별도 execution record, `planned_id` 참조) 분리 + 79차 `obs_key`/roster 결속 · **N2** 세대는 키 개수/mode 이름이 아니라 봉인 문맥으로 dispatch (정상 8 키 prep 보존 · v6 downgrade 거부) · **N3** provider 세 sha 를 지정 row·objective·실제 x0 까지 결속 (no-warm 전환 거부). 승인 초안 `codex/NEXT_APPROVAL_SCOPE_DRAFT.md` (미승인).

## 82차 요청 (2026-09-28) — **단계 3 라운드 1 구현 결과 + 발송 전 자체 점검 보강** 발송 (G81-N1·N2·N3 반영 · 실행 GO 아님 · 본진 복귀 아님) (원장 §115)

`docs/22p_gap/GATE82_REQUEST.md` — 판정 대상 HEAD `c82231c4` (RUN_SCOPE 변경 `20ab9655` → `f3de7e02` · `source_digest eda3feb8f4536511 → eea5977f4faf9685 → 02a776a7a0a3f4ba`). 커밋 사슬: 고정 표 `90a1f419` → RED `6473d1fb` → 구현 `20ab9655` → 영수증 보존 `5d659d06` · 1차 `03f907cc` → 전체 검증 `3b008357` **red** (원장 앵커 누락, F8) → 자체 점검 F1~F12 → 사용자 결정 "지금 고치고 영수증 한 번 더" → RED `315f5028` → GREEN `f3de7e02` → 1차 보존 `23670e58` · 2차 + 앵커 `9b52eb2a` → 변이 EXPECT `2d2f5d8b` → 전체 검증 `9d5d8d1c` **red** (증인 규칙 G67-T1-b 1 건) → 증인 정정 `d76b3eda`. 시험 59 passed (g81 44 + g79 15) · 변이 `-k g81` 20/20 · 전체 검증 `c82231c4` — docs-lint 358 passed · pytest 0 failed · 2004 passed, 1 xfailed · smoke rc 0. 영수증: validator 항 둘 + 검사 `세대_선언_일치` 하나만 변화, 검증·복원·재채점 결과 세 세대 동일. 자기 신고 13 건(요청문 §8 a~m — 영수증 2회째 · 두 번의 첫 전체 검증 red · 순서 · 질문 뒤 범위 변화 포함) · 질문 9 (§9). 발송 SHA = 이 절을 담은 커밋 (값은 발송문) · `FF_OK`.

## 82차 회신 (2026-09-30) — **부분 수용 · 라운드 1 종결 보류** · G82-N1 (P1) · G82-N2 (P1) · G82-N3 (P2) · 영수증 2차본 수용 (원장 §116)

발송 HEAD `8f54427c` (본진 ff 복귀 뒤) · 패키지 `docs/22p_gap/gate82_review/` (blob 105/105). **N1** 관측 roster 를 출력에서 재구성하지 않는다 (시작 전 SHA 복사 · record ↔ 계획만 비교 · noise realization 결속 없음) · **N2** bank 선언 (envelope · 설계 generator/version/seed rule/dtype/endian) 이 고정 구현 (bank-seed/v1 · PCG64 · float64 · little) 과 대조되지 않는다 · **N3** 계획/record protocol_generation 이 sig 6 · 행 v6 와 연결되지 않는다. 좌표: `src/io.py:1528 · 1569 · 1727 · 1801` · `src/fitting.py:1286–1391 · 1394 · 1881 · 1992` · `tools/design_wire.py:404–412 · 563–597` · `tools/preserve.py:3183 · 3230 · 3305`. 요청문 F3 · §3 map 문장 정정 (취소선). Q6 2차 영수증 수용 · Q7 returned 유지 · Q1 dead 정의는 다음 승인 코드 라운드.

## 83차 요청 (2026-09-30) — G82-N1·N2·N3 제한 보완 결과 · 라운드 1 종결 판정 요청 (원장 §117)

`docs/22p_gap/GATE83_REQUEST.md` — 판정 대상 HEAD `ea2af59e` (RUN_SCOPE 변경 `7d291fbc` · `source_digest 02a776a7a0a3f4ba → 7187bd31740514d4`). 고정 표 §10 `dfdd91a9` → RED `6bc46caf` (18/19) → GREEN `7d291fbc` → 변이 12 `8e18ae83` · 증인 정정 `6723b2ad` → 2차 영수증 보존 `5313731c` → 새 세대 `4307b6f8` → 계약 줄번호 `ea2af59e`. 실측 `ea2af59e`: pytest 0 failed · 2023 passed · 1 xfailed · smoke rc 0 · 변이 12/12. 새 검사 `관측_roster_재구성` · `세대_연결` · bank profile (`check_bank_profile`) — 좌표 `src/io.py:1573 · 1628 · 1660 · 1834 · 1919` · `src/fitting.py:1300 · 1317 · 1402` · `tools/design_wire.py:560–600` · `tools/preserve.py:3235`.

## 83차 회신 (2026-09-30) — **G82-N1·N2·N3 종결 · 승인된 단계 3 라운드 1 종결 · 새 차단 0 · 새 세대 영수증 수용** (원장 §118)

패키지 `docs/22p_gap/gate83_review/` (blob 169/169). 비차단 정정 하나 (`check_design` → `pairing_design_sha256` → `_check_design_nested`) 는 문서에서 닫음. 실행 GO · 라운드 2 · 단계 3 전체 완료 아님.

## 84차 요청 (2026-09-30) — 라운드 2 범위 확인 (원장 §119)

`docs/22p_gap/GATE84_REQUEST.md` — 문서만 · RUN_SCOPE 0. 좌표: 진입점 없음 (`stage3=` 는 시험뿐) · `tools/preserve.py` `LEG_SPEC_FIT_KEYS` :6402 · `leg_run_spec` :6418 · `planned_index` :6046 · `src/fitting.py` `_prepare_stage3` :1286 (curves :1335 · reference :1307) · dead 정의 :350 · `src/io.py` `realized_from_fits` :1528.

## 84차 회신 (2026-09-30) — 2a/2b 분리 수용 · 사전 고정 수정 조건부 적합 (원장 §120 · 고정 표 §11)

G84-N1 (hex16 ↔ hex64 · `src/fitting.py:903–925` · `tools/preserve.py:3250`) · N2 (2b · v5 spec 키 불변 · `:6468`) · N3 (halfcell `_fit_one` :1955 < `_prepare_stage3` :1970 — 공통 시작 전 경계) · N4 (`returned` :1549 · `finite`/`converged` · record v2 분기 · `:1879–1887`). 패키지 `gate84_review/` blob 88/88.

## 라운드 2a 구현 (2026-09-30) — 원장 §121 · GATE85 요청

승인 기록 `2bceaf9e` → RED `d81fdc01` (`tests/test_gate84_round2a.py` 15 node · 15 failed — 무관 예외 11 · 실제 4 + 패치 전 탐침 5 `scratchpad/g84_probe_real_reasons.txt`) → GREEN `eaa8888d` (3 파일: `src/fitting.py` +124/−, `src/io.py` +63, `tools/preserve.py` +20 · 167/40) → history `b740db16` → 영수증 + 앵커 `91f00a72` (validator `ba51cd20caa10b7b` · paired `4d6cdc7b…` 35 · grid `3f706067…` 34). 좌표 (`91f00a72`): `_config_closure_digest` :885 (= hex64[:16]) · `_config_closure_parts` :901 · `closure_sha256_from_parts` :919 · `config_closure_sha256` :926 · `_stage3_preflight` :1288 · `_prepare_stage3` :1333 (`preflight=`) · `write_execution_record` :1454 (v2) · `normalize_restart_record` :395 (dispatch 판 하나 · dead 삭제) · 호출 `_pf = _stage3_preflight` :1982 < `if reference == "halfcell"` :1985 < self-fit `_fit_one` :2015 · seed :1965 · 연쇄 725-749. `src/io.py` `_RECORD_SCHEMAS` :1531 · `realized_from_fits(schema=)` :1534 · `_stage3_checks` :1803 · `base_config_결속` :1974. `tools/preserve.py` `_REALIZED_OBJ_KEYS_V2` :3066 · `_RECORD_SCHEMA_KEYS` :3067 · `check_execution_record` :3287 (분기 :3301). 변이 `-g84` 12 (생존 1 → n3_04 추가 → 12/12) + 기존 2 재정박 (`absent-restart-fields-are-unrecorded-g79` — 81차부터 dead 정의를 변이하던 것 · `the-v6-path-refuses-another-plan-generation-g82` → MULTI). 계약 §1 v6 열 · 인용 2015 · 1965 · 725-749. 최종 실측: 전체 pytest (clean `91f00a72`) 0 failed · 2039 passed · 1 xfailed (56:56) · smoke rc 0 · **등록부 전체 변이 재생** (clean `28d0effe`, 단독) 345 중 344 물었다 · 예외 1 (g61) → `f89b1401` 정정. 전체 재생 자체 발견 5 (g79 dead 자리 · 54차 fixture 2 변이 · 59차 M3/M8 · 61차 영수증 — 전부 시험 층, 65·70·74차 방어층 추가 뒤 전체 재생 부재) → 정정 `eaa8888d` · `3eab51f9` · `28d0effe` · `f89b1401`. 판정 대상 HEAD `f89b1401` (RUN_SCOPE = `eaa8888d`). 요청문 `docs/22p_gap/GATE85_REQUEST.md`.

## G85-N1 한정 보완 (2026-09-30) — 원장 §124 · GATE86 요청

승인 · 고정 표 §12 `b9bc46c1` → RED `9255377a` (자기일관 위조 넷이 패치 전 validator 전체 통과 · 실패 목록 []) → GREEN `19bf1c15` (`src/io.py` `base_config_closure_members` + `base_config_결속` 정확·유일 대조 · source_digest f1f4378f46610f08) → 변이 -g85 7/7 `3dc20c2d` → 영수증 history `c2f37648` · 새 세대 `0be169b1` (35 · 34 불변) → 최종 `0be169b1`: pytest 1 failed (증인 형식) · smoke rc 0 · **등록부 전체 변이 재생 352/352** → 증인 정정 `b4876b0b`. 탐침이 운영 `_exec_class/` 에 기록 1 개를 남겨 지웠다 (요청문 §6-b).

## 87차 회신 (2026-10-03) — 2b 종결 보류 · G87-N1 (P1) (원장 §128)

패키지 `docs/22p_gap/gate87_review/` (zip `8c46223d…` · payload 152 · index blob = 패키지 바이트 154/154 · 규칙 `f7ff978d` → 보존 `89651dec`). 수용: v5 골든 · v3 builder/index · 진입점 배선 (완료 제외) · `v6` 이름 · 원문 로그 13 · 영수증 보존. G87-N1 좌표 (`b8d4b693` = 현재 RUN_SCOPE): `run.sh:222–232` (fit 전용) · `src/fitting.py` `_record_phase` :849 (claim None → :856 반환) · `_assert_fit_input_is_authorized` :1184 (hex64 → 묶음 digest :1215 · null → `assert_phase_input_binding` :1208) · `_assert_fit_authorized` :1243 (v2 :1278 · v3 :1284 · claim :1306) · `commit_run_outputs` :1735 → `_record_phase(claim, "fit")` :1740. `tools/preserve.py` `CLAIM_PHASES` :3997 · `CLAIM_KEYS` :4010 · `PHASE_INPUT_KEYS` :6652 · `assert_phase_input_binding` :6656 · `phases_done` :6795 · `phase_done` :6804 (순서 :6895–6906 · consumed :6907) · claim 생성 :7377–7382 (`phases: {}`) · 상태 view :7828 · `finalize_leg` :8820 (missing :8938 · consumed 대조 :8955–8984 · 기록 :9044). `src/grid.py` `_assert_grid_authorized` :393 (v2 spec :436). 시험 `tests/test_gate87_round2b.py` s02_04 :348 (발급까지 · `in_digest` = 곡선 단독 sha :271) · s04_01 :486 (smoke 완주).

## G87-N1 한정 보완 (2026-10-03) — 원장 §129 · §130 · GATE88 요청

승인 · 고정 표 §14 `00ed85b44` → RED `9e53a7edb` (16 node · 9 failed / 7 passed — f01_01 traceback = G87-N1 실행 재현) → 증인 고정
`5cdf22bea` → GREEN `e462a3d19` (source_digest `7dd546baaee9e823`) → history `8adb3bb41` → 변이 16 `12a2c27be` → 영수증 `38522285f`
(35 · 34) → 자체 점검 고정 `07aefea11` (node 8 · 변이 5 · 21/21) → 최종 `07aefea11`: pytest **2133 passed / 1 xfailed / rc 0** (54:14) · smoke **rc 0** (2:30) · 전체 재생
**395/395 call 단계에서 물었다 · rc 0** (scenario 406 · site 444 · 2:30:49). 좌표 (`e462a3d19` = 현재 RUN_SCOPE): `tools/preserve.py` `claim_phases_for_spec` :4035 · `_claim_required_phases` :4024 ·
`_claim_record_keys_ok` :4019 · `input_package_digest` :6705 · `_assert_external_input_binding` :6721 · `phase_done` :6897 (집합 :6944 ·
결속 :6950 · 순서 :6997 · consumed :7016) · `_claim_planned_leg` 봉인 :7491 · `finalize_leg` :8929 (missing :9048 · 재유도 :9125 · 계획
in_digest :9133–9141 · 기록 :9177) · `src/fitting.py` `_record_phase` :849 · `_fit_input_binding` :871 · `fit_input_package_digest` :1181
→ preserve 위임 · staged 결속 :1701 · 완료 기록 :1753. 시험 `tests/test_gate88_fit_only_lifecycle.py` 24 node.

## 88차 회신 (2026-10-04) — 2b 종결 보류 · G88-N1 (P1) (원장 §131)

패키지 `docs/22p_gap/gate88_review/` (zip `3f299425…` · codex/ payload 12 + manifest · index blob = 패키지 바이트 14/14 · 규칙
`be6358fd1` → 보존 `0e0a1975c`). 검토자 실행 0 (정적 호출 · 데이터 흐름 판정). 수용: G87-N1 정상 경로 (v3 밖 입력 = fit-only · v3 null
= index 거부 · 비-smoke 완료 · 최종화 양성) · 입력 생산자 의미 · v2 불변 (한정) · 87차 수용 부분 유지 · 재개 / 상태 view (정상 도달
상태 한정) · 새 영수증 (한정) · 원문 로그 16 (보존 기록 대조 — 재실행 아님). G88-N1 좌표 (`e462a3d19` = 현재 RUN_SCOPE):
`tools/preserve.py` `_assert_external_input_binding` :6721 (정의 1 · 호출 1 = `phase_done` :6950) · `_read_claim_record` :7548 (키
집합만 :7553) · `resume_claim` :7559 (token · 계획 · cohort · run_spec :7577–7599) · `finalize_leg` :8929 (`_lifecycle_locks` :9010 ·
snap :9042 · missing :9049 · 선행 소비 :9067–9073 — fit 은 첫 phase 라 건너뜀 · `_ledger_lock` :9098 · 재유도 :9125 · fit 전용 분기
:9130–9142 = 세 문자열 비교뿐 · `inputs` 안 읽음 · 기록 :9176–9177 · 원장 write :9206). 반례 (정적): `phase_done` 뒤 저장 claim 의
`phases.fit.receipt.inputs` 삭제 · 값 하나를 다른 hex64 로 · 키 추가 · 비hex → 세 문자열 그대로라 `executed`. 보완 자리 = :9130
분기 안 기존 비교 뒤 (두 lock 안 · 원장 · claim · token 변경 전). 시험 사각: f03_02 · f03_06 inputs 둘 = `phase_done` 에 처음 주는
입력 · f03_03 · f03_06 `receipt_package_tampered` = 문자열 대조만.

## G88-N1 한정 보완 (2026-10-04) — 원장 §132 · §133 · GATE89 요청

승인 · 고정 표 §15 `abf857752` → RED `76a5da16e` (6 node · 4 failed / 2 passed — d02 넷 `DID NOT RAISE` = G88-N1 실행 재현) → GREEN
`26c11d6fc` (`tools/preserve.py` +4 · source_digest `803e2b7781cbc9cd`) → history `14978adb0` → 변이 `-g89` 2 + `-g88` 증인 한 건
`134f26f48` → 영수증 `66129fc6a` (35 · 34) → 최종 `66129fc6a`: pytest **2139 passed / 1 xfailed / rc 0** (0:52:30) · smoke **rc 0** (2:25) · 전체 재생 **397/397 call 단계에서 물었다 · rc 0** (scenario 408 · executable 397 · site 446 · 2:26:43).
좌표 (`26c11d6fc` = 현재 RUN_SCOPE): `tools/preserve.py` `_assert_external_input_binding` :6721 (호출 둘 = `phase_done` :6950 ·
`finalize_leg` :9146) · `finalize_leg` :8929 (`_lifecycle_locks` :9010 · snap :9042 · `_ledger_lock` :9098 · fit 전용 분기 :9130 ·
세 비교 :9136–9142 · 새 검사 :9143–9146 · 기록 :9180 · 원장 write :9210). 시험 `tests/test_gate89_finalize_input_binding.py` 6 node.

## 89차 회신 (2026-10-04) — G88-N1 종결 · 라운드 2b 종결 (원장 §134)

패키지 `docs/22p_gap/gate89_review/` (zip `ce9fbe39…` · codex/ payload 12 + manifest · index blob = 패키지 바이트 14/14 · 규칙
`992ea2a63` → 보존 `023876a66`). 판정 `ACCEPT_G88_N1_AND_CLOSE_STAGE3_ROUND2B` — G88-N1 종결 (`finalize_leg` :9146 의 공통 결속
검사가 원장에 옮길 같은 snap 의 fit receipt 에 · 두 lock 안 · 세 비교 뒤 · executed 전환 · 원장 쓰기 · claim 삭제 전 · 새 호출 하나를
뺀 AST = 88차) · 회귀 d01–d03 · 변이 `-g89` 2 + `-g88` 증인 갱신 · 원문 로그 (제출 원문 확인 수준 — 검토자 재실행 아님) · 새 영수증
세대 수용 · 87 · 88차 수용 · 2a 종결 유지 · **2b 종결**. 검토자 쪽 import · pytest · smoke · 변이 · COMSOL 0 (정적 도구만). 한계:
일반 손상 durable 자료형 · 동시 실행의 새 검증 없음 · 같은 치환 지점의 변이 둘을 독립 커버리지로 세지 않음 · YAML core 해시 독립
재계산 없음. 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class · 투영 게시 · requirements · COMSOL 미승인 —
`grid_fit_v5` 진단 전용 지위 유지.

## 다음

**89차 회신 접수 (원장 §134) — G88-N1 종결 · 단계 3 라운드 2b 종결 · 새 차단 0 · 실행 GO 아님.** 다음은 사용자가 정한 순서대로 **PyBaMM 고정의 별도 범위 · 승인 라운드** (출발점 `docs/22p_gap/PYBAMM_PIN_PREREVIEW_REPLY_20261003.md`) — 승인 전 착수 없음 · 이 종결은 requirements 변경 · 새 계산의 승인이 아니다. 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class · 투영 게시는 밖. ~~**`docs/22p_gap/GATE89_REQUEST.md` (G88-N1 보완 결과 · 2b 종결 재요청) 발송 → 89차 회신 대기** (원장 §132 승인 · §133 요청). 판정 대상 `26c11d6fc` · 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini 는 밖.~~ REIL 은 게이트 차수 밖으로 따로: **부속 B 재검토 수용** (RV2A-N1–N3 종결 · 문서 수용 조건 C2 종결 · 묶음 `bms-balancing/reviews/prereview_reil_v2_annexB_20261004/` · 기록 `wiki/entities/isu-uconn-lfp-gr-emulated-degradation.md`) → 다음은 C1-core 명세 확보 · 환경 고정 · P0 / 비용 측정 / 실행 각각의 별도 승인 (자동 시작 없음). ~~REIL 은 게이트 차수 밖으로 따로: 부속 A 재검토 회신 접수 (RV2-N1 종결 · RV2A-N1–N3) → 부속 B `bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md` · 재검토 요청문 준비 (발송은 사용자 결정).~~ ~~**G88-N1 한정 보완 착수 (원장 §132 승인 · 고정 표 §15 · 2026-10-04).** RED (`tests/test_gate89_finalize_input_binding.py`) → `tools/preserve.py` 최소 GREEN → 변이 `-g89` (+ `-g88` 증인 한 건) → 영수증 history + 1 회 → 전체 회귀 · smoke · 등록부 전체 변이 재생 → GATE89. 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class/투영 · requirements 는 밖.~~ ~~**88차 회신 접수 (원장 §131) — 2b 종결 보류 · G88-N1 (P1) → 사용자에게 G88-N1 한정 보완 승인 요청.** 승인이 오면 고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` §15 (최종화가 원장에 옮길 같은 snapshot 의 fit receipt 에 기존 `_assert_external_input_binding` — 코드 변경 전 커밋) → RED (실제 `finalize_leg` · 정상 durable 양성 + `phase_done` 뒤 inputs 삭제 / 유효 hex64 교체 / 키 추가 / 비hex 음성 · 결속 이유 · 원장 바이트 불변) → 최소 GREEN (`tools/preserve.py` 안 — 넘으면 차이만 먼저 승인) → 변이 `-g89` (새 호출 제거 포함) → 영수증 history + 1 회 → 전체 회귀 · smoke · 등록부 전체 변이 재생 → GATE89. 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class/투영 · requirements 는 밖.~~ ~~**`docs/22p_gap/GATE88_REQUEST.md` (G87-N1 보완 결과 · 2b 종결 재요청) 발송 → 88차 회신 대기** (원장 §129 승인 · §130 요청). 판정 대상 `e462a3d19` · 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini 는 밖.~~ pybamm 고정 = 게이트 차수 밖 사전 검토 회신 접수 (`docs/22p_gap/PYBAMM_PIN_PREREVIEW_REPLY_20261003.md` — 목적별 프로필 C · B · D 권고) · G87-N1 종결 뒤 별도 라운드 (사용자 결정). REIL = 프로토콜 v2 정정본 (`bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md`) · 확인적 맞춤은 논문 선행. ~~**G87-N1 한정 보완 착수 (원장 §129 승인 · 고정 표 §14 · 2026-10-03).** RED (`tests/test_gate88_fit_only_lifecycle.py`) → `tools/preserve.py` · `src/fitting.py` 최소 GREEN → 변이 `-g88` → 영수증 history + 1 회 → 전체 회귀 · smoke · 등록부 전체 변이 재생 → GATE88. 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · requirements 상한은 밖 (pybamm 상한 · REIL 은 Codex 사전 검토 요청문 별도).~~ ~~**87차 회신 접수 (원장 §128) — 2b 종결 보류 · G87-N1 (P1) → 사용자에게 G87-N1 한정 보완 승인 요청.** 승인이 오면 고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` §14 (외부 producer 입력의 결속 · v6 fit-only 의 완료 · 재개 · 최종화 계약 — 코드 변경 전 커밋) → RED (격리 원장 · 비-smoke 출력 · 실제 `fit_input_package_digest(_fit_input_digests(…))` · 수치 본체만 inert · lifecycle 대체 금지 · 양성 1 + 입력 / attempt / 순서 음성) → 최소 GREEN (`tools/preserve.py` · `src/fitting.py` 안 — 넘으면 차이만 먼저 승인) → 변이 `-g88` → 영수증 history + 1 회 → 전체 회귀 · smoke · 등록부 전체 변이 재생 → GATE88. 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · requirements 상한은 밖.~~ ~~**`docs/22p_gap/GATE87_REQUEST.md` (라운드 2b 결과 · 2b 종결 판정 요청) 발송 → 87차 회신 대기** (원장 §126 승인 · §127 요청). 코드 `b8d4b693` (source_digest `864edfb73b9695a1`) · 고정 표 §13 · 시험 `tests/test_gate87_round2b.py` 63 · 변이 `-g87` 22 · 영수증 `7fbaa45b` · 전체 pytest 2109/1 xfailed · smoke rc 0 · 전체 재생 374/374. 실행 GO · 운영 원장 v6 계획 항목 · requirements 상한 (§13-7) 은 사용자 별도 결정.~~ ~~**86차 회신 접수 (원장 §125) — 라운드 2a 종결 수용 · G85-N1 종결.** 다음은 **2b 범위 (R2-a · R2-c · G84-N2 조건) 의 사용자 별도 승인 요청** — 승인 전 착수 없음. 실행 GO · 새 연구 leg 없음 · grid_fit_v5 진단 전용 유지.~~ ~~**`docs/22p_gap/GATE86_REQUEST.md` (G85-N1 보완 결과 · 2a 종결 재요청) 발송 → 86차 회신 대기** (원장 §124). 회신 뒤 2b 는 사용자 별도 승인. 실행 GO · 새 연구 leg 없음.~~ ~~**85차 회신 접수 (원장 §122 보충 · §123 본 회신) — 2a 종결 보류 · G85-N1 P1 → 사용자에게 G85-N1 한정 보완 승인 요청.** 승인이 오면 고정 표 (STAGE3_IMPL_ROUND1_SPEC §12) → RED (구성원 누락 · 추가 · 중복 · 순환 · 자기일관 위조) → `src/io.py` `base_config_결속` 최소 diff (run_spec.base_config 스냅샷에서 extends 연쇄 독립 유도 · 정확 · 유일 집합 대조) → 변이 → 영수증 history + 1 회 → 전체 회귀 · smoke · 등록부 전체 변이 재생 → GATE86. 2b · p_ini · 실행 GO 는 밖.~~ ~~**`docs/22p_gap/GATE85_REQUEST.md` (라운드 2a 결과 · 2a 종결 판정 요청) 발송 → 85차 회신 대기** (원장 §121). 회신 뒤 2b (R2-a · R2-c · G84-N2 조건) 는 사용자 별도 승인. 실행 GO · 새 연구 leg 없음.~~ ~~**84차 회신 접수 (원장 §120 · 고정 표 §11) → 사용자에게 라운드 2a 제한 구현 승인 요청.** 승인이 오면 RED (`tests/test_gate84_round2a.py`) → 4 파일 안 최소 diff (§11-2 hex64 결속 · §11-3 공통 시작 전 경계 · dead 정의 삭제 · §11-4 record v2 · 계약 §1 v6 열) → 변이 `-g84` → 영수증 `7187bd31740514d4` history 보존 → 두 leg 1 회 → 전체 회귀 · smoke → GATE85. 2b (G84-N2 조건) · p_ini 구현 · 세대표 등록 · 실행 GO 는 밖.~~ ~~**`docs/22p_gap/GATE84_REQUEST.md` (라운드 2 범위 확인 · 사용자 결정 "84차 범위 확인 요청부터") 발송 → 84차 회신 대기** (원장 §119). 회신 뒤 구현은 사용자 별도 승인 (라운드 2a = R2-b · e · f · g / 2b = R2-a · c 제안).~~ ~~**라운드 2 범위 사용자 승인 대기** (원장 §118 끝 R2-a … R2-g — 항목별로 나눠 승인). 승인 전 코드 · 시험 없음. 승인이 오면 시작 전 고정 표 → RED 먼저 → 최소 diff → 변이 → 83차 영수증 (`7187bd31740514d4`) history 보존 → 새 세대 1 회 → 전체 회귀 · smoke → GATE84.~~ ~~**`docs/22p_gap/GATE83_REQUEST.md` 발송 (SHA 는 발송문) → 83차 회신 대기.** 라운드 1 종결이어도 라운드 2 (실물 v6 leg gate 배선 · 세대표 등록 · p_ini · dead 정의 · 계약 §0 · §6-c/e) 는 사용자 별도 승인 뒤.~~ ~~**82차 회신 접수 (원장 §116) → 사용자 승인 대기: G82-N1·N2·N3 제한 보완 + 이유별 회귀만** (검토자 `docs/22p_gap/gate82_review/codex/NEXT_SCOPE_DRAFT.md` — 비활성 초안). 승인이 오면 RED 먼저 (N1 양성 1 · 음성 3 / N2 양성 1 · 음성 4+ / N3 양성 1 · 음성 2 — 소비자와 validator 양쪽 도달 단계 · 정확 이유) → 같은 4 파일 최소 수정 → 변이 → 2차 영수증 보존 → 새 세대 영수증 1회 → 전체 회귀 · smoke → GATE83. 승인 전에는 코드 · 시험을 만들지 않는다. 라운드 2 · p_ini · 새 연구 계산 · 실행 GO 는 이 승인 밖.~~ ~~**`docs/22p_gap/GATE82_REQUEST.md` 발송 (SHA 는 발송문) → 82차 회신 대기.** 회신이 오면 §116 접수 → 라운드 2 (실물 v6 leg gate 배선 · 세대표 등록 · `p_ini` 정책 · dead 정의 삭제 · 계약 §0 정정 · 비유한 J count 규칙)는 **사용자 별도 승인 뒤에만**. 실행 GO · 본진 ff 복귀는 여전히 아님.~~ ~~**승인됨 (2026-09-28 "비준", 원장 §114 끝).** 단계 3 한정 구현 라운드 1 진행: 시작 전 세 표 고정 `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` → RED 먼저 (`tests/test_gate81_stage3_wire.py`) → 3-A → 3-B → 3-C → 변이 → 전체 회귀·smoke (clean 커밋) → 원본 영수증 `history/<leg>.validate.eda3feb8f4536511.yaml` 보존 → 두 leg 영수증 1회 → GATE82. RUN_SCOPE 4 파일 밖이 필요하면 멈추고 별도 승인.~~ ~~**단계 3 한정 구현은 사용자가 `docs/22p_gap/gate81_review/codex/NEXT_APPROVAL_SCOPE_DRAFT.md` 의 범위(G81-N1~N3 반영 · 4 파일 · 지정 두 leg 영수증 1회)를 명시 승인한 뒤에만.** 승인이 오면 시작 전 세 표(계획/실현 필드 시점 · legacy/prep/v6 dispatch · provider edge·좌표 결속) 고정 → RED 먼저 (`tests/test_gate81_stage3_wire.py`) → 3-A → 3-B → 3-C → 변이 → 전체 회귀·smoke → 영수증 1회 → GATE82. 승인 전에는 코드를 만들지 않는다.~~ ~~**`docs/22p_gap/GATE81_REQUEST.md` 발송 (SHA `88ac144a`) → 81차 회신 대기.** 회신이 단계 3 범위(3-A 결속 · 3-B provider DAG · 3-C 행·검증 · 갈림 Q1–Q4)를 확정해도 **구현 착수는 사용자 별도 승인 뒤** — 그때 RED 먼저 (`tests/test_gate81_stage3_wire.py`) → 3-A → 3-B → 3-C → 변이 → 전체 회귀·smoke → 라운드 끝 영수증 1회 → GATE82.~~ ~~**단계 3 은 사용자가 제한 범위·사전 고정 사항을 승인한 뒤에만.** 승인이 오면 `docs/22p_gap/GATE81_REQUEST.md` 로 범위 확인 요청부터 (구현 착수 아님). 그 전에는 코드·문서를 더 만들지 않는다 — 회신이 종결이라고 시작하지 않는다.~~ ~~`docs/22p_gap/GATE80_REQUEST.md` 발송 → 회신 대기. 단계 2 종결이면 단계 3 은 새 사용자 승인 뒤.~~ ~~`docs/22p_gap/GATE79_REQUEST.md` 발송 → 회신 대기.~~ 종결이면 단계 3(묶음 1·2 schema · ID preimage · provider DAG)은 새 사용자 승인 뒤. ~~전체 회귀 + strict smoke (clean 커밋) → 원장 §110 · `GATE79_REQUEST.md` → docs-lint → 발송.~~ ~~`docs/22p_gap/GATE78_REQUEST.md` 발송 → 회신 대기.~~ 사용자 승인이 오면 코드 라운드(단계 2: restart 행 `converged`·`termination_status`·`n_eval` · parquet 읽기 실패 구조화, RED 먼저, RUN_SCOPE 이동 → 라운드 끝 영수증 1회). ~~`docs/22p_gap/GATE77_REQUEST.md` 발송 → 회신 대기.~~ 회신이 13 착수를 승인하면 코드 라운드는 (a) §9.4 restart 행 필드 → (b) 묶음 6 → (c) 묶음 4 → (d) 묶음 3 → (e) 묶음 5 → (f) 고유 leg 목록·비용 → pilot 요청 순 (리뷰가 고치면 그대로). ~~**게이트 루프 종결.** 다음 일(본 실행 계획 `plan_leg.py --claim-scope active_claims` · 투영 게시 · class 변경)은 전부 사용자 승인 뒤 새 요청문으로.~~ (§107 정정: '본 실행' 은 grid 재실행이 아니라 단계 3 pilot 이다) ~~`docs/22p_gap/GATE76_REQUEST.md` — 75차 잔여 N1·N2·N3 종결 판정 요청 (새 실행 GO 아님).~~ 회신 전까지 `grid_fit_v5` 의 claim_roles·세대·cohort 명부는 쓰지 않는다. 종결되면 본 실행 계획(`plan_leg.py --claim-scope active_claims`)은 사용자 승인 뒤.

~~`docs/22p_gap/GATE75_REQUEST.md` — 74차 항목 1~6 종결 판정 요청 (새 실행 GO 아님). ~~`docs/22p_gap/GATE74_REQUEST.md` — 결과 보고 + G74-1~4 신고 + G74-3 분류 질문 (새 실행 GO 요청 아님).~~ 74차 회신 항목 3~6 의 범위를 사용자가 정하면 `/finding` (RED 먼저) 로 시작. 현지 검증 `e84d670d`: 20 failed (전부 G74-3) · 1859 passed · 2 xfailed · smoke rc 0. 회신 전까지 `grid_fit_v5` 의 claim_roles·세대·cohort 명부는 쓰지 않는다.

~~**사람의 단계** — 실행 기계에서 `plan_leg.py` 출력 확인 → 원장 `planned:` + cohort `prospective_legs` 커밋(승인 행위) → 승인 HEAD 에서 E9-3 순서로 한정 실행. 요청문 이력: ~~`GATE73_REQUEST.md`~~ (한정 실행 GO 재요청) · ~~`docs/22p_gap/GATE72_REQUEST.md`~~ (한정 실행 GO 재요청) · ~~`docs/22p_gap/GATE71_REQUEST.md`~~ — 판정 대상 `876429562f6a69b59793c70700cb5b375391ab67` · `source_digest b705a21a1237ec73` 로 **한정 실행 GO** 를 묻는다 (원장 §92·§93). 발송문은 요청문 SHA + 브랜치 head SHA, 커밋 뒤 실측.~~
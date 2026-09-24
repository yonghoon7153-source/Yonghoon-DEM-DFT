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
| E1 | 미완 · 한정 실행에서 결과·출처 보증 한계 허용 | 강한 producer 주장을 쓰면 **`row_projection.py`** 의 projection/restart 두 압축 payload 소비 경로의 typed manifest·압축해제 hash·producer receipt (49차 원조건 — `archive_bundle.py` 의 fit 묶음만으로는 못 닫는다 · 내용 identity 와 운송 바이트 identity 구분 · 무조건 거부 회귀 아님). 쓰지 않으면 미검증 범위 명시 + 주장 제외 | **사용자 결정 대기** — 구현 vs 주장 축소 |
| E2 | 미완 · 독립 실행 코드 보증 한계 허용 | 독립 launcher 주장을 쓰면 실제 시작/import bytes 와 소비 receipt. 아니면 "자기 측정" 명시 (`source_digest` 는 디스크 자기 측정이다) | **사용자 결정 대기** |
| E3 | **기존 실행/보존 계약 차단 유지** | lifecycle finalize 가 typed receipt(`execution-receipt/v1`, `tools/preserve.py:2979` `:3245` 검사기는 있다)를 실제로 소비 · 상태·bundle 식별 결속 · `_declared_index_members` 가 None 을 돌려주면 대조를 건너뛰는 경로(`:7492–7523`) fail-closed · 정상/부정/부분 회귀 | 미착수 (다음) |
| E4 | 미완 · 독립 변이 replay 보증 한계 허용 | 미재생 또는 명시적 **표본** 범위(선택·seed·분모·미수행)로 한정. 전수 독립 replay 완료라 표시하지 않음 | **사용자 결정 대기** |
| E5 | **부분 구현 · class 소비 계약 차단 유지** | `_read_exec_class_at`(`:4950–4974`) 이 class enum + content_id 만 본다 — 두 키만 있는 레코드, `sealed=[]`·`evidence=17`·`recorded_at=false` 레코드를 수용했다(리뷰어 fixture). `resolve_execution_class` 는 `sealed` truthiness(`:5097–5111`). typed modern/legacy variant · content/seal 결속 · writer→reader→promotion 회귀. 과거 class 임의 재작성 금지. (요청문의 "미착수" 는 **부정확** — identity·seal·capability·lock·read-back·충돌 거부는 있다) | 미착수 (다음) |
| E6 | **새 실행의 운영 전제** · 전체 과거 이관과 분리 | 읽기 전용 영향 지도 `docs/22p_gap/registry_impact.md`(약속했으나 HEAD 에 없음) + 새 실행 권한 영역의 격리/배타 사용 및 전후·delta 보존. 현재 `tests/test_compare.py:940–950` 는 운영 등록부에 synthetic canonical 을 만들 수 있고 `tests/conftest.py:154–188` 은 시작 때 없던 JSON 을 소유권 구분 없이 지운다 — 다른 실행의 합법 기록도 삭제 대상. 한계 라벨로 대체 불가 | 미착수 (다음) |
| E7 | **F50b 제한 수용** | 비교 규칙 유지 · 최종 식별에서 통합 회귀 확인 · `git_dirty` 제거 불요 (Q6: "범위 밖 문서 수정도 무조건 dirty" 라는 요청문 전제가 틀렸다 — git_info 는 RUN_SCOPE 기준) | ✔ |
| E8 | 69차 한정 종결 유지 | 관련 변경 없으면 반복 심사 안 함 | ✔ |
| E9 | **실행 명세 미완 + G70-N1** | 정확한 argv/config/입력/출력/leg/cohort/run_spec · 새 prospective 승인 · archive/검증 순서 · 실패 처리. Gate63 §0 적용성 표 1회 (immutable publication · class/삭제 절차 · 비-grid 진입점 · retention/power-loss · publisher principal · truth_provenance 를 `이번에 사용/완료 근거`·`범위 제외`·`명시적으로 보증하지 않음` 으로). 과학 목적 고정(`synthetic grid/fit 재실행` vs `Stage3 primary 비교`). 당장 빠진 것: `./run.sh` 는 `--mode` 필수 rc 1 · 기본 OUT 은 timestamp(≠ `results/grid_fit_v4/`) · planned index 8 = 과거 executed, `grid_fit_v4` prospective 항목 없음 · `all` 체인은 archive 를 안 부르고 finalize 는 `preservation_pending` | G70-N1 닫음 · 명세 미착수 · **과학 목적 사용자 결정 대기** |
| E10 | **최종 통합/환경 증거 미완** | 실제 대상 Linux 에서 **최종 식별**의 전체 회귀 + 작은 전 과정 smoke · positive-control 공백 해소(`test_a_smoke_run_cannot_be_promoted_to_a_canonical_report` 의 `results/grid_fit_v4` 양성 경로 — skip 이나 가짜 class 레코드로 녹색 만들지 않음) · "1 failed/1804 passed rc 1" 과 "smoke rc 0" 은 다른 결과 — full suite 전부 통과라 적지 않음. 문서만 바뀐 커밋은 바이트 동일 근거로 기존 증거 재사용 가능 | 미착수 |

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

## 다음

E3 → E5 → E6 → E9(명세·적용성 표) → E10 순으로 닫고, E1/E2/E4 와 과학 목적은 사용자 결정을 받아 `docs/22p_gap/GATE71_REQUEST.md` 에
최종 commit/`source_digest` 로 제출한다 (미래 수정을 `f0dfaff3` 에 소급 적용하지 않는다). 발송문은 요청문 SHA + 브랜치 head SHA, 커밋 뒤 실측.

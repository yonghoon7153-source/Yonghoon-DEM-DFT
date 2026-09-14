# 적대적 리뷰 요청 — 13차 · α·β 검증 하네스 (`bms-balancing/`)

11차(대상 `2add074`)는 **NO-GO** (P1 12 · P2 6). 열여덟 건을 닫고 `reviews/R12_REQUEST.md` 를 썼으나
**보내지 못했다** (Codex 토큰 소진). 대신 `/self-review` 6 렌즈를 내부에서 돌려 **35 건**을 찾아 닫았다.
그 라운드가 드러낸 것이 이 요청의 이유다:

> **R11 이 "닫았다" 고 적은 것의 절반이 반쪽이었다.** (§2 표)

목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가."**
GO 기준: R3 §5 + R5 §4 + R6 출처 결속 + R7 §6 + R8 §6 + R9 6항 + R10 7항 + R11 5항.

**리뷰어에게 최우선 요청**: 자체 리뷰는 **우리가 우리를 턴 것**이라 같은 맹점을 공유한다.
§2 의 "반쪽으로 닫음" 패턴이 **이번 35 건에도 반복되는지**를 먼저 봐 달라.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`) |
| 코드 정본 | `c7217c0` — 증거는 이 커밋에서 만들었다 |
| 증거 커밋 | `85038ee` (`reviews/r12_repros/replay_ours_after_selfreview/`) |
| 이후 커밋 | `26c477c` — **`.md` 하나만**. `git diff c7217c0 HEAD --name-only -- '*.py' '*.sh'` → **0 개** (실측, §1) |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 소유 |
| 직전 대상 | `2add074` (R11) |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). **현행 `out/` 13 개는 provenance-incomplete** (§4) |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 회귀 | `tests/test_r12_selfreview.py` (`f01`~`f28`) 신설. 전체 **236** (직전 202) |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                # 236 passed 기대. 원자료 불필요
bash matlab/tests/run_all.sh               # Octave 없으면 4·5 단계만

HEAD=$(git rev-parse HEAD)                 # ⚠ 러너는 **40 자 full object id** 만 받는다 (R11 P2-6)

python3 reviews/r6_repros/codex_r6_mutation_audit.py                              # 8/8 CAUGHT · MISSED 0
python3 reviews/r6_repros/codex/mutation_adapted.py                               # 5/5 CAUGHT
python3 reviews/r7_repros/replay_codex_r7.py   --target . --expected-head "$HEAD" # 6 슬롯 (5 소멸 + 1 전제 변경)
python3 reviews/r9_repros/replay_codex_r9.py   --target . --expected-head "$HEAD" # 12/12
python3 reviews/r10_repros/replay_codex_r10.py --target . --expected-head "$HEAD" # 22 슬롯
python3 reviews/r11_repros/replay_codex_r11.py --target . --expected-head "$HEAD" # 35 슬롯
python3 scripts/check_u14.py --new out --schema-only                              # rc 2 (§4)
```

> ⚠ **`expected_tree` 는 커밋마다 다르다.** 보관 증거(`85038ee` 시점)는 `ae9e48479805…`,
> `26c477c` 에서 재실행하면 `16d449467101…` 다. **불일치가 아니라 트리 해시가 커밋을 따라간 것**이다.
> 러너가 봉인하는 것은 도구 blob 과 `dirty_paths` 이고, 그 둘은 안 변했다 (§1).

> ⚠ **이번 라운드가 러너 계약을 둘 바꿨다** — 리뷰어가 옛 기대치로 읽으면 오판한다.
> · 러너 rc 가 `evidence_eligible` 을 반영한다 (증거 아닌 실행은 0 이 아니라 **3**) — C19
> · `-O`/`PYTHONOPTIMIZE` 는 재실행 **전에** 거부(`SystemExit(2)`) — `-E` 가 그 환경값을 무시하므로
>   R10 P2-4 를 지키려면 거부가 앞에 와야 한다 — C08

## 1. 검증 — 방금 실행 (2026-09-13, `26c477c`)

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 회귀 | `python3 -m pytest tests/ -q` | **`236 passed in 200.29s`** |
| 코드 무변경 | `git diff c7217c0 HEAD --name-only -- '*.py' '*.sh'` | **0 개** |
| 증거 이후 변경 | `git diff c7217c0 HEAD --name-only` | `docs/MICROSHORT_MPH_REVIEW.md` + `reviews/r12_repros/…` 21 개 (증거 자체) |
| R7 재생 @ 현 HEAD | `replay_codex_r7.py --expected-head 26c477c…` | rc **0** · `evidence_eligible: true` · `instrument_sealed: true` · `package_digest_ok: true` · `dirty_paths: []` · `ran_in: 격리 snapshot` · `closed: true` · 6/6 probe 자기 assertion 정지 |
| 현행 정본 점검 | `check_u14.py --new out --schema-only` | rc **2** · `promotion_eligible: false` · `blocked_by {schema 59, provenance_cols 27, content 5, provenance 1, baseline_absent 1}` — 보관 증거와 **일치** |

보관 증거(`85038ee` 시점, `reviews/r12_repros/replay_ours_after_selfreview/`):

| 파일 | 결과 |
|---|---|
| `pytest_full.txt` | `236 passed in 195.33s` (rc 0) |
| `matlab_smoke.txt` | `전부 통과` (rc 0) |
| `codex_r6_mutation_audit.txt` | 8/8 CAUGHT · MISSED 0 |
| `mutation_adapted.txt` | 5/5 CAUGHT · MISSED 0 (`R6_OLD_OUT = bfc4623^` 의 `out`) |
| `replay_codex_r6_adapted.json` | `"mode": "full"` 6/6 |
| `replay_codex_r7.json` | 반례 소멸 5 · 전제 변경 1 (R7-03) |
| `replay_codex_r9.json` | 반례 소멸 12 |
| `replay_codex_r10.json` | 반례 소멸 20 · 우리 코드 밖 1 (`snapshot:argv`) · 전제 변경 1 (`u18:shape_duplicates`) |
| `replay_codex_r11.json` | 반례 소멸 32 · 전제 변경 2 (`publish:*` · `root:profile_grid`) · **환경상 불가 1** (`data:shape_wrapper` — 원본이 `wsl.exe` 를 부른다) |
| `check_u14_out_schema_only.txt` | rc 2 (§4) |

"전제 변경"·"환경상 불가"는 **닫힘으로 세지 않았고** 각각 fingerprint 를 봉인해 두었다.
각 파일 옆 `*.rc.txt` 가 종료 코드다 (전 판은 rc 를 `.json` 꼬리에 붙여 유효 JSON 이 아니었다 — C24).

## 2. 이 라운드가 드러낸 것 — R11 답변의 절반이 반쪽이었다

**이 표가 이 요청의 핵심이다.** 우리가 R11 요청문에 "닫았다"고 적은 것과 실제:

| R11 에 적은 것 | 실제 | 자체 리뷰 ID |
|---|---|---|
| P1-1 두 실행 사이 입력 identity 비교 | 파일당 receipt 한 벌만 만들어 **마지막 행만** 비교 | C01 (3 렌즈) |
| P1-3 정본 γ 격자 21 | `authority` 칸만 봄 — 행 수·`requested` 와 안 댐 | C04 (3 렌즈) |
| P1-5 hardlink alias 차단 | inode 만 봐서 `cp -a` 사본은 통과 | C02 (2 렌즈) |
| P1-8 유한성 | JSON 쪽은 문자열 `"1e999"` 통과 | C06 |
| P1-9 "신고된 위험을 값으로 소비" | 실은 "**키가 있을 때만** 값으로" — 지우면 통과 | C03 (2 렌즈) |
| P1-10 A import 전 격리 | pyc 만. gate 앞에 106 모듈이 저장소에서 해결 | C08 |
| P1-10 B snapshot bytes 재대조 | `instrument_sealed` 은 `--no-filters` 를 **안** 씀 (한쪽만 닫은 비대칭) | C07 |
| P2-2 "네 축 대조" | `run_id` 축은 항진명제 | C29 |

**같은 축을 여러 렌즈가 독립으로 친 것이 셋** (C01·C04·C11, 각 3회) — 10차에서도 그것이 진짜 구멍의 신호였다.

## 3. 발견별 대응 — `결론이_바뀜` 14 건

| ID | 반례 (실행 확인) | 수정 (`파일:대상`) | 회귀 |
|---|---|---|---|
| **C01** (3) | `_receipts_of` 가 행별 receipt 를 `dict.update()` 로 뭉쳐 마지막 행만 비교. production 은 행마다 입력이 다르다 (`verify.build` 가 반쪽전지 소스별 `hb.identity()` + Si 소스별 `lit_id` → state 100 의 32 행에 half_cell sha 2 종 · literature.si 8 종). **양방향**: 앞 31 행이 달라도 rc 0 promotion true / 순서만 뒤집힌 정당한 재실행은 거짓 rc 2 | `scripts/check_u14.py:_receipts_of` — 행 key(`S.matrix_key`/`S.profile_key`)별 `{역할: sha}` 를 만들어 key 끼리 댄다 (순서 무관). `_compare_roles` helper | `test_f01` |
| **C02** (2) | alias 가 inode 만 봐서 `cp -a` 바이트 동일 사본이 rc 0 · promotion true — 계산을 한 번도 안 하고 승격 증명서. `run_id` 는 `ROW_SKIP` 에 있고 `META_CONTROLS` 에도 없어 아무도 안 봤다 | `check_u14.py` — `run_id` 가 같으면 alias (독립 실행이면 시도마다 uuid4) | `test_f04` |
| **C03** (2) | `if k in meta and …` + `META_KEYS` 에 `git_dirty`/`git_modified_code` 없음 → 위험 필드를 **지우면** 검사가 안 돌았다. 정직하게 신고한 실행 rc 2 / 침묵한 실행 rc 0 — 게이트가 침묵에 보상 | `check_u14.py` — `meta.get(k, "(없음)") != want`. `_ABSENT = "(없음)"` | `test_f05` |
| **C04** (3) | `check_gamma_roster` 가 본문과 한 번도 안 댔다 — 3 행 산출이 "21/21" 로, 21 행이 "성공 1" 로, "γ=0.5 실패"인데 그 행이 있어도 통과. `isinstance(True, int)` 라 bool 도 개수로 셌다 | `bms_balancing/schema.py:check_gamma_roster` — `succeeded == len(rows)` · `requested == authority` · `missing ∩ 본문 γ == ∅` · bool 배제 | `test_f09` |
| **C05** (2) | matrix 의 모집단이 stdout `SUMMARY` 전용 — 소비자 0, 2/32 행 묶음이 "전부 갖췄다". `MATRIX_ROW` 에 모집단 열 0 개 · meta 에 status 키 0 개 · `check_u14` 안 `'status'` 0 회 | `verify.py:cmd_matrix` 가 `combo_roster` 를 **행마다** 봉인 (`absent` 는 `D.HALF_CELL_ABSENT`), `schema.py:check_combo_roster` 가 본문과 대조. `MATRIX_ROW`/`MATRIX_NON_NUMERIC` 확장 | `test_f10` |
| **C06** (1) | `_finite_problems` 가 `str` 통과 → degeneracy `best_obj="1e999"`/`"Infinity"`/`"nan"` 문제 0. `_num_diff` 도 `float()` 라 양쪽 `"1e999"` 면 `inf == inf` 로 숫자 차이 0. **P1-8 이 닫았다는 부류가 다시 들어왔다** | `schema.py:_finite_problems` — 문자열도 파싱해 CSV 와 같은 규칙 | `test_f11` |
| **C07** (1) | `evidence_gate.py:instrument_sealed` 이 `--no-filters` 없이 `hash-object` (같은 파일 `verify_snapshot_bytes` 는 쓴다) → committed `.gitattributes` + clean 드라이버로 **주입 코드가 든 러너**가 ok 봉인 + 실제 실행 | `evidence_gate.py:instrument_sealed` — 같은 플래그 | `test_f12` |
| **C08** (1) | 네 러너 전부 gate import **전에** 106 모듈이 `sys.path[0]`(저장소 안)에서 해결 — untracked `traceback.py` 하나가 gate 보다 먼저, `INSTRUMENT` 밖. shim 이 gate 를 `sys.modules` 에 선주입하면 tracked 러너가 수정된 채로도 `dirty_paths: []` · `instrument: ok` · eligible true | 네 러너 — `__name__ == "__main__"` 이고 `not sys.flags.safe_path` 일 때 `os.execv(… -P -E -B …)` 로 한 번 재실행. `-O` 거부는 재실행 **앞** | `test_f13` |
| **C09** (1) | 같은 구멍이 production `write_meta` 에도 — heredoc 의 `sys.path[0]` 이 `''`(cwd) 라 저장소 루트 untracked `hashlib.py` 가 `from provenance import` 보다 먼저 실행. **실측으로 meta 에 `git_dirty: false` 를 받아냈다** (P1-9 반례 재개방) | `scripts/run_states.sh` — 세 heredoc 을 `python3 -I -P -` 로 | `test_f14` |
| **C10** (1) | `.gitattributes` 가 `*.sh/*.py/*.csv/*.json` 만 `eol=lf` → `core.autocrlf=true`(Windows 기본값)에서 **121/415 파일** CRLF 드리프트 → `verify_snapshot_bytes` 가 네 러너를 전부 rc 2 로. **리뷰어가 절차대로 clone 하면 증거가 하나도 안 나온다** | `.gitattributes` 맨 앞에 `* text=auto eol=lf` (보관 패키지의 `-text` 는 뒤라 그대로 이긴다) | `test_f17` |
| **C11** (3) | `rc 0` 인데 `promotion_eligible: false` 인 경로가 둘 생겼는데 `WORKING_STATE.md` 런북은 **"0 이었을 때만 정본 교체"** — 실제 `out/` baseline 12/12 대조가 정확히 그 상태 (`inputs_uncomparable: 16`). **오늘 U18 승격 경로가 전부 여기로 온다** | `check_u14.py` — 승격 자격 없음에 전용 **rc 4** (`not_promotable = bool(inputs_unk)`). `--schema-only` 는 승격을 **묻지 않은** 진단이라 0 유지 + `promotion_eligible`·`baseline_absent` 가 말한다. 런북·docstring 수정 | `test_f18` |
| **C12** (1) | 후보 디렉터리의 `_vN` 이 명부에서 조용히 빠지고 `blocked_by` 에 `stale` 없음 → 진짜 재실행(LLI 99.0)을 무시하고 옛 사본만 대조해 rc 0 promotion true | `check_u14.py` — `stale_new` 를 blocker 로 (정본 쪽 `_vN` 은 경고 유지) | `test_f06` |
| **C13** (1) | degeneracy receipt 가 **JSON 문자열**이면 `receipt_map` 이 `{}` → 양쪽 `{}` 라 `if not x and not y: continue` 로 잠들고 `inputs_uncomparable` 조차 안 찍힘. `check_degeneracy` 도 `[]`. **서로 다른 반쪽전지인데 promotion true** (CSV 셀 쪽은 `validate_receipt` 가 막는다 — JSON 산출만 비대칭) | `schema.py:receipt_text` 로 정규화를 한 자리에 (`validate_receipt` 와 같은 규칙). `receipt_map`/`receipt_paths` 가 그것을 쓴다 | `test_f02` |
| **C14** (2) | `canonical_names` 가 3종 glob 만 → 서명된 13 개 중 **12 개만** 명부. 실측: `out/*.meta.json` 13 vs 명부 12, `ne_shape_GITT_Li.csv` 가 게이트 밖 | `check_u14.py` — 허용목록 → **배제목록** (`ARTIFACT_SUFFIXES`, `d.glob("*")` 에서 `.meta.json`·dotfile·비산출 확장자 제외). **"사이드카 있는 것만" 으로 좁히지 않았다** — 서명 없는 산출이 조용히 빠지는 것은 같은 부류의 버그다 | `test_f07` |

### `숫자가_바뀜` 6 건 · `서술만_바뀜`/사소 15 건

| ID | 요지 → 수정 |
|---|---|
| C15 | `shape_step` 만 묶음 검사·`BMS_RUN_ID` 없음 (R8-02 축) → `run` 과 같게 (`rid` 생성 · `verify_unit_or_say`) |
| C16 | candidate 쪽 receipt 누락도 "정본이 옛 스키마" 사면 → rc 0 (`schema.py:322` 빈 dict falsy) → 그쪽은 계약 위반 |
| C17 | P1-7 이 현행 `out/matrix_*.csv` 4 개를 `ne_shape` 가 못 읽게 만든 사실이 산출에 안 남음 → `pairing.rejected_matrix` 로 남기고 짝 없음으로 센다 |
| C18 | `ENV_KEYS` 에 `pandas` 없음 (서명엔 적으면서). 모든 과학 입력이 `pd.read_excel` → `ENV_KEYS` 에 추가 |
| C19 | 러너 rc 가 `evidence_eligible` 미반영 (`--allow-dirty` 가 rc 0) → 아니면 **3** |
| C20 | `R12_REQUEST.md:82-83` namespace 분해가 실측과 반대(root 6·data 5 → 실측 5·6), 같은 문서 `:88-89` 과 모순 |
| C21 | `check_u14.py` docstring 의 rc 계약 자기모순 |
| C22 | `blocked_by.schema` 가 사람용 출력에 없는 합계 → `schema` + `provenance_cols` 로 분리 |
| C23 | 보고 블록 13 개 중 8 개가 `--max-show` 에서 표시 없이 잘림 (stale 은 `[:6]` 하드코딩) → `_show` helper 한 자리 |
| C24 | 증거 `.json` 5 개가 유효 JSON 아님 (rc 꼬리) → `.rc.txt` 로 분리 |
| C25 | before-evidence 2 개에 40-hex 커밋 id 없음 → **닫지 않음** (§5) |
| C26 | `R12_REQUEST` `:30,32` (6/6) vs `:57` (5+1) 불일치 |
| C27 | 패키지 파일 수 13 vs 14 불일치 |
| C28 | `test_d10_15` 의 none 케이스가 모순 감지 가지를 잼 (`label[1]` 을 지워도 통과) |
| C29 | `shape_step` 의 run_id 대조가 항진명제 (producer 가 같은 meta 에서 읽어 보고) → 프로세스의 id 로 |
| C30 | `verify_snapshot_bytes` 1 회성 + untracked 에 눈 없음; `ev_env` 가 prefix 를 벗겨 snapshot 에 `__pycache__` 7 개 잔류 → `NEEDS_DEFAULT_PYCACHE = {"early-gate-pyc"}` 만 기본 자리, 나머지는 별도 prefix |
| C31 | `gate.bootstrap_pycache()` 호출자 0 (죽은 코드) + `/tmp` 누수 (pycache 718 · snap 94) → 삭제 |
| C32 | `check_u14.py:166` 오류 분기가 list 를 반환하는데 `:313` 이 2-tuple 로 푼다 → BOM JSON 에서 `ValueError`, rc 1 → 모든 경로가 `(problems, uncomparable)` |
| C33 | `scale_audit_*` 가 `MAY_BE_EMPTY` 와 `ROW_SKIP` **양쪽**에 → 정본에 있고 재실행에 없어도 통과 → carve-out 제거 (`MAY_BE_EMPTY = frozenset()`) |
| C34 | `receipt_paths` 에 production 소비자 0 → **닫지 않음** (§5) |
| C35 | `replay_codex_r11.py` 가 SIGTERM 이면 symlink 잔존 + `.gitignore` 가 그것을 dirty 게이트에서 감춤 → workspace 를 `tempfile.mkdtemp` 로 |

## 4. 현행 정본 상태 — `check_u14 --new out --schema-only` rc 2

```
blocked_by {schema 59, provenance_cols 27, content 5, unit 0, controls 0, env 0,
            numbers 0, alias 0, provenance 1, inputs 0, inputs_uncomparable 0,
            stale 0, baseline_absent 1}
roster {old 0, new 13, compared 0}
promotion_eligible false
```

⚠ **R11 라운드(28 · 24 · 4)보다 커진 것은 요구 축이 늘었기 때문이다** — matrix 행의 `combo_roster`(C05),
명부가 `ne_shape_*.csv` 까지 세는 것(C14), provenance 부재를 unsafe 로 세는 것(C03).
**산출 숫자는 하나도 안 움직였다.** 내용 5 중 4 는 degeneracy 의 aggregate digest 불일치, 1 은
`ne_shape_GITT_Li.csv` 가 producer 스키마에 없는 열 19 개를 갖고 있는 것 (C14 로 이제야 게이트 안에 들어왔다).

## 5. 닫지 않은 것

| 항목 | 왜 |
|---|---|
| **C34** `receipt_paths` production 소비자 0 | 원장·요청문이 "역할별 path 를 드러낸다" 고 적은 것보다 실제 범위가 좁다. 경로를 identity 에 넣는 것은 R6 F1/F4 의 **의도된** 결정이라 digest 에 넣는 것이 답이 아니다. 소비자를 붙이는 것(locator 변화를 정보 줄로)이 다음 라운드 작업 |
| **C25** before-evidence 2/4 에 40-hex 커밋 id 없음 | 그 스크립트들이 안 적는다. **보관 패키지라 안 고친다** (고치면 그 패키지의 digest 가 바뀐다) |
| R11 답변이 지목한 5 축 | export 공통 snapshot · dataset manifest · run receipt · partial 수명 · locator 무결성 — 그대로 열려 있다 |
| `data:shape_wrapper` (R11) | 원본 반례가 `wsl.exe` 를 부른다 — 리눅스 컨테이너에서 **환경상 불가**. 닫힘으로 세지 않았다 |
| 전제 변경 4 건 | R7-03 · `u18:shape_duplicates` · `publish:*` · `root:profile_grid`. 각각 fingerprint 봉인 — 아무 예외나 그렇게 읽히지 않는다 |

## 6. fixture 감사 — 일곱 번째

`combo_roster` 추가 · `run_id` alias 검사 · `scale_audit` carve-out 제거 · `ENV_KEYS` 확장으로
**기존 fixture 20 곳 가까이가 깨졌다.** 전부 "이제야 실제 invariant 를 만족하게" 고쳤다.

반복된 패턴 하나를 남긴다:

> 정본과 재실행 fixture 가 **같은 `run_id`** 를 쓰고 있었다
> (`_matrix_unit` · `_u14_dirs` · `_deg` · `d7_04` · `d8_02` · `d10_09`).
> C02 를 닫기 전에는 그것이 아무 의미도 없었으므로 아무도 안 봤다.

C01 을 R11 회귀가 못 잡은 이유도 같은 종류다 — `_matrix_unit` 이 `_full_matrix_rows` 를 만든 뒤
**모든 행에 같은 receipt 를 덮어썼다**. 행별 분기를 구조적으로 만들 수 없는 fixture 였다.
그래서 `test_r12_selfreview.py` 에 `_rows_per_si(tag_half, tag_si, n=4)` 를 두어 production 모양의
행별 receipt 를 만든다.

## 7. 리뷰어에게 묻는 것

| Q | 내용 |
|---|---|
| Q1 | **§2 의 "반쪽으로 닫음" 패턴이 이번 35 건에도 있는가.** 자체 리뷰는 우리가 우리를 턴 것이라 같은 맹점을 공유한다. 특히 C01(행별 비교)·C04(명부 결속)·C14(명부 범위) 는 "이번엔 진짜 다 봤나"를 의심할 축이다 |
| Q2 | C11 의 **rc 4** 설계 — `--schema-only` 만 0 을 유지하게 한 것이 옳은가. 우리 논리는 "승격을 묻지 않은 진단"인데, 그 예외가 새 우회로일 수 있다 |
| Q3 | C08 의 `os.execv` 재실행 — 봉인을 import 앞에 두는 방법으로 맞는가. `__name__ == "__main__"` 가드는 회귀가 `exec` 로 부르기 때문인데, 그 가드 자체가 우회로가 되는가 |
| Q4 | C14 에서 **허용목록 → 배제목록**으로 뒤집었다. 처음엔 "사이드카 있는 것만"으로 좁혔다가 legacy meta-less baseline 이 조용히 빠지는 걸 보고 되돌렸다 (같은 부류의 버그). 배제목록(`ARTIFACT_SUFFIXES`)이 새 확장자에 대해 fail-open 인데, 이 방향이 맞는가 |
| Q5 | C34 를 닫지 않은 판단 — `receipt_paths` 에 소비자를 붙이는 것이 R6 F1/F4(경로를 identity 에서 뺀 결정)와 충돌하지 않는가 |
| Q6 | `check_u14` 의 blocked_by 59·27·5·1 중 **content 5** 는 정본 자체의 결함이다 (degeneracy aggregate digest 4 + `ne_shape` 미등록 열 19). 이걸 정본을 다시 만들어 닫아야 하는가, 아니면 스키마를 넓혀야 하는가. 우리는 아직 정하지 않았다 |

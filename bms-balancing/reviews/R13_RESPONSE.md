# R13 회신 — Codex 13차 (대상 `94add7b`) NO-GO P1 4 · P2 5 + §5 Q6 — 전부 닫음

> 기계용 회신. 리뷰 원본은 `reviews/r13_repros/codex/pkg/HARNESS_R13_94ADD7B5_CODEX_REVIEW.md`
> (zip sha256 `c4d51fcff1e6843d69302d870784ce6d80181e9454a5ca5664de8832055f6f60`, manifest 163/163 일치 실측).
> 리뷰어 스크립트는 그대로 두고 우리 트리에서 돌려 RED 를 재현한 뒤 고쳤다 — 회귀는 그 반례를 옮긴 것이다.

| 항목 | 값 |
|---|---|
| 코드 정본 | `ef8e8f681050ee649783a8d85a9d584880c8aa80` |
| 증거 커밋 | `84ab3b3e40d771b044ccc4310ae4ecf59487d8ce` (`reviews/r13_repros/replay_ours_after_fixes/`, 코드 diff 0 — `git diff ef8e8f681050ee649783a8d85a9d584880c8aa80 84ab3b3e40d771b044ccc4310ae4ecf59487d8ce -- '*.py' '*.sh'`) |
| 회귀 | `python3 -m pytest tests/ -q` → **262 passed** (리뷰 대상 시점 236) |
| 브랜치 | `claude/bms-alpha-beta-verify` |
| 회신 이후 코드 | `df6413d649ef51ace16d634c3856f857d598c79d` — 조건 7 의 **실데이터 재실행이 끝났고**(U18b 승격 `37a889b`) 그 과정에서 발견 넷이 나왔다 (§8). **§4 증거는 이 커밋에서 다시 뽑았다** |

## 1. 발견별 — 재현 · 원인 · 수정 · 회귀

| # | 리뷰어 관측 (재현) | 원인 | 수정 | 회귀 | 커밋 |
|---|---|---|---|---|---|
| **P1-1** C04/C05 | 리뷰어 스크립트 6 case 를 우리 트리에서: `profile_wrong_grid`(γ 21 점 0~0.4)·`profile_twenty_duplicate_missing`·`matrix_self_declared_one_row_authority`·`matrix_wrong_member`(미등록 Li2) 전부 **rc 0 / promotion true** | 검사가 roster 의 **개수**만 봤고 구성원을 독립적으로 정하지 않았다 — 모집단 주장이 산출 안에서 닫혀 있었다 | `schema.canonical_gamma_grid()`(값, producer 의 `np.linspace(LB5[4],UB5[4],21)` 과 비트 동일) · `canonical_combo_keys(state)`(`data.HALF_FILE`−`HALF_CELL_ABSENT`, 상태 모르면 ValueError) · `state_of(name)` · `check_gamma_roster`(missing 중복 금지 + canonical 이면 본문 ∪ missing == 정본 격자) · `check_combo_roster(rows, state)`(구성원 유효성 + canonical 이면 exact set) · `verify.cmd_matrix/cmd_profile` 이 같은 함수 · 자리 규칙은 `CANONICAL_SLOT_PREFIX` 로 내용과 분리 | 4 case 전부 rc 2/false, 대조군 2 rc 0 유지. `test_g01~g05` | `ce9b5bf` |
| **P1-2** C13/C16 | `ref_consumed_inputs: {}` 가 필수 키 검사·truthy 가지 둘 다 통과; 같은 불완전 reference 가 dict 면 보고, JSON 문자열이면 침묵 | `in (None, "")` 이 빈 컨테이너를 "있음" 으로 셌고, reference 검증이 truthy·dict 일 때만 돌았다 | `check_degeneracy`: 빈 컨테이너 = 없음 · reference 는 키가 있으면 언제나 `receipt_text` 로 정규화해 검증 (candidate 혼자 지키는 계약) | `test_g06~g07` | `5f180df` |
| **P1-3** 보관 증거 | 전제 변경·환경상 불가·우리 코드 밖을 unresolved 에서 빼고 `closed: true` · "모든 case 가 닫혔다" | 러너 넷이 집계를 각자 가졌다 | `evidence_gate.summarize_verdicts()` 한 자리: `report_complete`(rc 0 의 뜻) · `closed`(요청 leaf 전부 반례 소멸) · `closed_with_substitutes`(제외마다 대체 증거 **이름**) · `excluded` · `leaf_cases` · `rc_reason` 문자 그대로. GO 소비자는 `closed` 를 읽는다 | `test_g13~g14` | `d5d143f` |
| **P1-4** C08 | 격리 재실행이 앱 의존성 import **뒤** | `import argparse, …, traceback` 가 먼저 돌아 untracked 모듈이 봉인 앞에서 실행될 수 있었다 | 네 러너의 재실행 블록을 `from __future__` 직후, `import os, sys` 만 앞에 (인터프리터 시작 때 이미 로드된 둘) | `test_g10` — AST 로 **순서**를 잰다 | `752df9a` |
| **P2-1** C06 | `best_obj=true`(float(True)==1.0) · `best_p=[]` · `LLI_percent={}` 가 문제 0 | 유한성 앞에 타입·모양 계약이 없었다 | `check_degeneracy_shape()`: NUMERIC 8 은 bool·비수치·비유한 거부(`_is_num` 이 bool 을 뺀다) · `best_p/ref_p` 는 유한 5 개 · 세 통계는 min/max 객체 · `best_modes_percent` 비지 않은 유한 객체 | `test_g08` | `5f180df` |
| **P2-2** C33 | `scale_audit_*="{}"` 가 감사로 인정 | 빈 문자열만 막았다 | `check_scale_audit()`: pocv·dvdq·dqdv 존재 · 7 칸 · 유한 · 표본 산술 · **열 결속**(`audit[m].scale == scale_{m}_{side}`). 실제 `out/` 에서 결속 성립을 먼저 확인하고 계약으로 | `test_g11` | `752df9a` |
| **P2-3** C32 | BOM JSON 에 CLI 가 `JSONDecodeError` 로 죽고 `PROMOTION` 도 없음 | JSON 읽기 네 자리가 전부 `decode("utf-8")` (CSV 는 이미 utf-8-sig) | `schema.json_bytes()` 한 자리 · 네 곳 적용 · 파싱 실패는 구조화된 스키마 오류 | `test_g12` (온전한 묶음으로 고치자 RED — 열 번째 fixture 감사) | `752df9a` |
| **P2-4** | schema-only 가 필수 env 축 누락을 안 봤다 | 비어 있지 않은 dict 인지만 | `check_degeneracy_shape`: `ENV_KEYS` 전수 존재 (baseline 없이 candidate 혼자) | `test_g09` | `5f180df` |
| **P2-5** | r10 이 아무 예외나 전제 변경으로 · r11 `ENVIRONMENT_LIMITED[key][0]` 이 "원" 한 글자 · `publish:*` 가 3 leaf 를 1 record 로 | fingerprint 없음 · 값이 문자열 · 그룹 중단을 하나로 접음 | r10 `PREMISE_FINGERPRINT`(보관 증거의 실제 멈춘_곳에서 봉인) · `EXPECTED_LEAVES` 22 · r11 `ENVIRONMENT_LIMITED` 를 `{why, substitute, fingerprint}` dict 로(`wsl.exe` 일치만) · `EXPECTED_LEAVES` 37 · 그룹 중단은 첫 leaf 만 fingerprint 로 전제 변경, 나머지는 `미실행 (그룹 중단)` 각각 | `test_g15~g16` | `d5d143f` |
| **§5 Q6** shape | 리뷰어 `fresh_shape_producer`: 실제 writer → `--schema-only` **rc 2 · schema 27 · provenance_cols 3 · content 1 · provenance 1**. 우리 재현(`test_g25` RED, 실제 producer→`shape_step`→U14): **schema 27 · provenance_cols 3 · content 1** 그대로 | `check_u14._kind` 와 `schema.body_roster` 가 각자 "matrix 아니면 profile" — `ne_shape_*.csv` 도 모르는 이름도 profile | 아래 §2 | `test_g18~g25` | `ef8e8f681050ee649783a8d85a9d584880c8aa80` |

## 2. Q6 — shape 전용 계약 (PROFILE_ROW 확대가 아니다)

| 축 | 어디 | 계약 |
|---|---|---|
| kind | `schema.kind_of(name)` | 이름 → 종류 **한 함수**. `matrix_*.csv` · `profile_gamma_*.csv` · `degeneracy_*.json` · `ne_shape_*.csv` 만; 그 밖은 `ValueError`. `check_u14._kind` 와 `body_roster` 는 이것만 부른다; gate 는 모르는 이름을 `"<name>: 모르는 산출 종류"` content 로 세고(`test_g19`), production `write_meta` 는 등록되지 않은 이름에 meta 를 쓰지 않는다 (`test_g26`) |
| 열 | `schema.SHAPE_ROW` 22 | 기존 20 + `inputs_sha` · `consumed_inputs`. producer 의 header 가 이 tuple 에서 나온다 (`ne_shape._write_csv`) · `SHAPE_NUMERIC` 은 state/run_id/receipt 둘을 뺀 전부(유한 필수) |
| 행 key | `schema.shape_key` = `state` · `row_key(kind)` | reader·checker 같은 함수. 중복 상태 = 중복 key |
| receipt | 행마다, 역할 `SHAPE_ROLES` = `matrix` · `half_cell` · `half_cell_pristine` · `literature.gr` · `literature.si` | `ne_shape._row_receipt` 가 sidecar 의 상태별 dict 를 역할 모양으로 (matrix leaf 의 `file` → `path`). `validate_receipt(..., roles=receipt_roles(kind))`. 짝 없는 행은 빈 칸 — receipt 를 지어내지 않는다 (partial 은 success 가 아니다). `check_u14` 의 입력 identity 대조(R11 P1-1)가 shape 에도 행 key 별로 돈다 |
| 빈 칸 | `SHAPE_MAY_BE_EMPTY` = `gamma_witness` · `gamma_witness_delta` | R3-03 의 "격자에서 증인 없음" 은 값이다 — 둘이 **함께** 비어야 한다 (`test_g24`) |
| coverage | `check_shape_coverage(rows, name)` | 본문 상태 집합 ↔ `canonical_shape_states(source)` (= `data.declared_states`; producer `ne_shape.main` 의 authority 도 같은 함수). 선언 밖 상태 = content · 정본의 부분집합 = 자리 규칙(`CANONICAL_SLOT_PREFIX`, reader 는 소비 가능 · 승격 gate 만 막음) |
| sidecar 내용 | `check_shape_meta(meta, rows, name)` (`check_u14` 가 shape 마다 부른다) | typed `status` ∈ {complete, partial, none, subset} · `pairing` 여섯 목록 · 중복 없음 · `authority` == 정본 · `requested ⊆ authority` · `available ⊎ missing_input = requested` · `paired ⊎ missing = available` · 본문 상태 == available · 본문의 γ 짝 있는 행 == paired · status == producer 판정식(none → subset → complete → partial) (`test_g22`) |
| sidecar 계약 | `_write_csv` | `env` · `started_utc` · `git_commit_at_start` · `git_dirty_at_start` · `git_modified_code_at_start` · `git_state_changed_during_run`(pre/post 대조, `write_meta` 와 같은 식) · `argv` · `roster`(잠금 안에서 sha256 과 **같은 bytes** 로 `body_roster`) — U14 `META_KEYS`·`META_REQUIRED` 전부 (`test_g23`) |
| 실행 조건 | `meta_controls("shape")` = `half_cell_source` · `si_source` · `grid_n` · `grid_range` · `gamma_grid` | solver 가 없으니 starts/seed 가 아니고, 상태는 본문에 여럿이라 조건이 아니다. 다른 세 종류는 `META_CONTROLS` 그대로 |
| 시작점 | `ne_shape.run_started()` | `main` 이 입력을 읽기 **전** 시각·git 상태 (R6 내부 F04). 직접 호출(리뷰 repro)은 writer 진입 시점 |

완주 (`test_g25`, 합성 원자료 `matlab/tests/gen_synth_xlsx.py` + fixture matrix, **실제** `ne_shape.py` → **실제** `shape_step` → **실제** `check_u14`):
schema-only 에서 schema 0 · provenance_cols 0 · content 0 · unit 0 · stale 0 (provenance 는 그 트리의 dirty 여부 그대로);
두 번째 독립 실행을 `--new B --old A` 로 대조하면 numbers 0 · controls 0 · env 0 · inputs 0 · alias 0 · inputs_uncomparable 0,
clean 트리에서 `promotion_eligible: true`.

리뷰어 스크립트의 `consumed={"synthetic": True}` 는 receipt 가 아니다 — 그 호출은 **receipt 축에서만** 막힌다
(schema 0 · provenance_cols 0 · provenance 0, content 는 전부 `consumed_inputs`/`inputs_sha`/출처 줄, `test_g21`).
스크립트를 다시 돌리면 그렇게 보일 것이고, 그것이 맞는 결과다.

정본 `out/ne_shape_GITT_Li.csv` 는 **소급 보수하지 않았다** (리뷰어 §Q6 답 그대로). `check_u14 --new out --schema-only`
는 59·27·5·1 → **40·25·6·1**: 옛 shape 가 제 종류로 읽혀 "모르는 열 19 + profile 열 21 누락" 이 사라지고 대신
`inputs_sha`(schema)·`consumed_inputs`(provenance_cols) 누락과 `status`·`pairing` 없음(content 2) 으로 잡힌다.
산출 숫자는 하나도 안 움직였다. 실데이터 재생성은 원자료가 있는 사용자 기계에서 `WORKING_STATE.md` U18 4 단계
(`scripts/ne_shape.py` → `check_u14 --schema-only` 에 shape 줄 0) — 이 컨테이너에는 규진팀 원자료가 없다.

## 3. GO 최소 조건 1~8 대응

| # | 조건 | 상태 |
|---|---|---|
| 1 | γ/조합 exact membership, producer 공유 · P1-1 세 case 거부 | 닫음 (P1-1 표: 4 case rc 2, 대조군 rc 0) |
| 2 | candidate reference receipt 독립 정규화·검증 · legacy baseline-only 는 정직한 비승격 | 닫음 (P1-2; legacy 는 `inputs_uncomparable` → rc 4 / schema-only 는 `promotion_eligible: false`) |
| 3 | 과학 JSON 타입·shape · scale audit 내용·결속 · 필수 env 축 | 닫음 (P2-1 · P2-2 · P2-4) |
| 4 | BOM/파싱 실패의 구조화된 CLI 결과 · helper 와 CLI 둘 다 회귀 | 닫음 (P2-3, `test_g12` 는 CLI 경로) |
| 5 | 증거 유효성/도달/개별/종결 분리 · 정확한 개별 명부 | 닫음 (P1-3 · P2-5; r11 은 `closed: false` · `closed_with_substitutes: false` 로 **정직하게** 남는다 — `publish:profile_partial_stdout` 에 대체 증거가 없다) |
| 6 | 초기화 경계 재설계 · 동적 검증 | 코드 순서는 닫음 (P1-4). **동적 인증은 하지 않았다** — `test_g10` 은 AST 순서 검사이지 우회 재현이 아니다. 열린 항목으로 남긴다 |
| 7 | shape 전용 계약 → producer→wrapper→U14 완주 · 기존 `out/` 보존, 별도 출력에 실제 재실행 | **닫음** — 실데이터 재실행 2 차(U18b)가 `numbers 0` · 명부 13/13/13 · 계약 축 전부 0 으로 승격됐고(`37a889b`), 기존 `out/` 은 `out/archive/legacy_r6_u14/` 에 **얼려 보존**했다 (그 경로가 옛 40·25·6·1 을 그대로 낸다). 승격 뒤 `--schema-only` 는 사용자 기계와 fresh clone 둘 다 **rc 0** (§8) |
| 8 | 기존 GO 전제(공통 snapshot · dataset manifest · run receipt · partial 수명 · locator 무결성)에 대한 명시적 판단 | **열림** — 이번 라운드는 신규 9 건 + Q6 만 닫았다. 전체 GO 로 바꾸지 않는다 (아래 §5) |

## 4. 증거 (`reviews/r13_repros/replay_ours_after_fixes/`, **U18b 승격 뒤 재생성**)

전부 clean 트리의 `df6413d649ef51ace16d634c3856f857d598c79d` 에서 (직전 판은 `ef8e8f6…`; 러너 넷의 leaf 별 판정은 **동일**하고,
바뀐 것은 정본 `out/` 의 상태다 — 아래 `check_u14` 행). 러너 넷 `evidence_eligible: true` · `instrument_sealed: true` · `package_digest_ok: true`.
새 종결 계약으로 읽는다 (rc 0 = `report_complete`, GO 소비자는 `closed`/`closed_with_substitutes`):

| 파일 | 결과 |
|---|---|
| `replay_codex_r7.json` | 반례 소멸 5/6 · 제외 1 (R7-03 전제 변경, 대체 `test_d7_03`) · report_complete true · closed false · closed_with_substitutes true |
| `replay_codex_r9.json` | 반례 소멸 12/12 · closed **true** |
| `replay_codex_r10.json` | 반례 소멸 20/22 · 제외 2 (`snapshot:argv` 우리 코드 밖 → `adapted:argv-vector` · `u18:shape_duplicates` 전제 변경, fingerprint `TypeError: 'NoneType' object is not subscriptable` → `adapted:duplicate-states`) · closed false · closed_with_substitutes true |
| `replay_codex_r11.json` | leaf 37 · 반례 소멸 32/37 · 제외 5 (`root:profile_grid` 전제 변경 · `data:shape_wrapper` 환경상 불가 `wsl.exe` → `publish:shape_step` · `publish:matrix_filtered_canonical` 전제 변경 → `data:matrix_subset` · `publish:profile_grid1_canonical` 미실행(그룹 중단) → `data:profile_grid` · `publish:profile_partial_stdout` 미실행(그룹 중단) **대체 없음**) · closed false · closed_with_substitutes **false** |
| `replay_codex_r6_adapted.json` | mode full 6/6 닫힘 (R6_OLD_OUT = `git archive bfc4623^ out`, 26 파일) |
| `codex_r6_mutation_audit.txt` · `mutation_adapted.txt` | 8/8 · 5/5 CAUGHT, MISSED 0 |
| `check_u14_out_schema_only.txt` | **rc 0** · blocked_by 전부 0 (`baseline_absent` 1 만) — U18b 가 정본을 새 계약으로 다시 서명했다. 옛 40·25·6·1 은 사라진 것이 아니라 `out/archive/legacy_r6_u14/` 로 **옮겨가 그대로 재현**된다 |
| `pytest_full.txt` | 277 passed |
| `matlab_smoke.txt` | Octave 전 단계 전부 통과 |

leaf 별 판정은 `ef8e8f6` 판과 동일하다 — Q6 이후의 코드 변경도, U18b 승격도 러너 결과를 움직이지 않았다.
⚠ 재생성할 때 `tests/` 전체 실행과 러너를 동시에 돌리지 않는다 (`test_d8_07` 이 같은 `replay_codex_r7.py` 를 부른다 — §8 U18-04).

## 5. Q1~Q6 리뷰어 답에 대한 우리 답

| Q | 리뷰어 | 우리 |
|---|---|---|
| Q1 반쪽 수정 반복 | 그렇다 — C04/C05·C13/C16·C14·C32·C33 | 수용. 다섯 자리 전부 이번에 나머지 반쪽을 닫았다 (P1-1 · P1-2 · Q6 · P2-3 · P2-2). fixture 가 잘못된 모집단·`{}` 감사를 정상으로 인정한 것도 여덟~열한 번째 감사로 고쳤다 (§6) |
| Q2 schema-only rc 0 | 가능하되 P1-2/P2-1/P2-4 의 candidate 검사가 전제 | 그 셋을 닫았다. schema-only 는 여전히 `promotion_eligible: false` + `baseline_absent` |
| Q3 execv 재실행 | 위치 부족, 정적 판단 | 위치는 옮겼다 (P1-4). 동적 우회 재현은 **안 했다** — 열린 항목 |
| Q4 배제목록 | `ARTIFACT_SUFFIXES` 는 여전히 확장자 허용목록; kind 등록부가 답 | 반은 수용: `kind_of` 가 **이름 등록부**다 — 등록되지 않은 산출은 이제 조용히 생략되지 않고 content 로 잡힌다 (`test_g19`). 확장자 목록은 그대로다 (`.log`·`.lock`·`.part` 를 산출로 세지 않기 위한 것). manifest 는 §5 의 열린 축 |
| Q5 locator | 충돌 안 함, 정보로 표시 | 수용. C34 는 아직 열림 (소비자 미부착) |
| Q6 | shape 는 전용 배선 뒤 재생성 · degeneracy digest 는 새 provenance 실행으로 분리 · 소급 보수 금지 | 수용 그대로 (§2). degeneracy digest 4 는 손대지 않았다 — 새 실행(U18)이 새 provenance 로 만든다 |

## 6. fixture 감사 — 여덟~열세 번째

| 회 | 무엇이 거짓이었나 |
|---|---|
| 8 (P1-1) | `_full_matrix_rows` 2/32 행이 "정상 전수 대조군" · `_u14_dirs` 1 행 authority 1 · `test_f09`/`e11_16` γ 0~1 · `matrix_row()/seal_combo()` 기본값이 canonical 주장 · d9_10 손으로 적은 roster 기대 · d8_05 방향이 모집단 크기 의존 |
| 9 (P1-2·P2-1·P2-4) | `_deg()` 등 degeneracy fixture 의 `best_p` 길이 2 · `env={"numpy"}` 만 |
| 10 (P2-2·P2-3) | g12 가 meta 없이 데이터만 둬 "묶음 미완" 으로 먼저 거부돼 BOM 경로에 닿지 않았다 · `matrix_row()/_full_matrix_rows/_u14_dirs` 의 `scale_audit_*="{}"` |
| 11 (P2-5) | 러너 안 inline fixture (`r9._full_row` · `r6_adapted._full_matrix` · `r9_05_adapted`) 가 `"{}"` 감사 + authority 1/2 — 새 검사에 먼저 거부돼 R7-05·R9-05 가 `오류` 가 됐다 |
| 13 (U18-03) | `test_g29` 의 첫 fixture 가 3 행짜리 matrix 를 canonical 이름에 뒀다 — P1-1 의 자리 규칙(좁힌 실행은 정본이 아니다)에 걸려 env 축에 닿기 전에 content 로 먼저 막혔다. 정본 자리에는 정본 모집단(`_canonical_combo_rows`)을 둔다 |
| 12 (Q6) | `kind_of` 가 fail-closed 가 되자 `test_review_findings` 의 세 fixture(`r4_06` · `r4_07` · `r5_04`)가 깨졌다 — production `write_meta` 를 `out/100.csv` · `out/old.csv` · `out/profile.csv` 로 부르고 있었고, `body_roster` 가 그 이름을 조용히 profile 로 읽어 통과했다. 등록된 이름으로 고쳤고 `write_meta` 는 이제 등록되지 않은 이름에 meta 를 쓰지 않는다 (`test_g26`). shape 축 자체는 검사하는 회귀가 없었으므로, 새 축을 위반하는 fixture 를 일부러 만들어 걸리는지 확인했다 (`g19` 모르는 이름 · `g21` receipt 없음 · `g22` 자기 authority/선언 밖 상태/pairing 위조 · `g23` roster 위조 · `g24` 증인 한쪽만 빈 칸/nan/중복) |

## 7. 열린 것 (이번 라운드가 닫지 않은 것 — GO 로 바꾸지 않는다)

| 항목 | 상태 |
|---|---|
| ~~조건 7 의 실데이터 재실행~~ | **닫음** (U18b 승격 `37a889b` · §8) |
| ~~§4 증거의 현행 커밋 재생성~~ | **닫음** — `df6413d…` 에서 전부 재생성, 러너 넷의 leaf 별 판정은 그대로 |
| 조건 6 의 동적 인증 · 조건 8 의 다섯 축 (snapshot · manifest · run receipt · partial 수명 · locator) | 열림 |
| C34 `receipt_paths` 소비자 · C25 before-evidence 40-hex | 열림 (C25 는 보관 패키지라 안 고친다) |
| `openpyxl` 이 `env_signature`/`ENV_KEYS` 에 없음 (리뷰어 정적 지적) | 열림 — 넣으면 세 종류의 sidecar 계약과 fixture 가 같이 바뀌므로 별도 라운드로 |
| C28 none 회귀가 rc 1 만 봄 · C31 | 열림 |
| r11 `publish:profile_partial_stdout` 미실행(그룹 중단) 대체 증거 없음 | 열림 — `closed_with_substitutes: false` 로 그대로 적혀 있다 |

---

## 8. 조건 7 의 실데이터 재실행 — 1 차(U18) · 2 차(U18b) · 승격, 그리고 드러난 것 넷 (2026-09-13/14, 회신 이후)

> 이 절은 위 표의 코드 정본(`ef8e8f6…`) **이후**다. 조건 7 은 **닫혔고**, §4 증거는 승격 뒤 `df6413d…` 에서 다시 뽑았다.

원자료가 있는 기계에서 `OUT=out_u18 STATES='100 200 300_0009 300_0147' STARTS=24 ./scripts/run_states.sh`
(2026-09-13 20:02–22:39 KST, 13/13 게시, 반쪽전지 소스 100·200·300_0009=GITT · 300_0147=step_005C).
기존 `out/` 은 손대지 않았다 (조건 7 의 보존 요구).

**숫자는 하나도 안 움직였다** — `check_u14 --new out_u18 --old out` 이 `numbers 0`, 명부 13/13 · 대조 13.
바뀐 것은 서명 축뿐이다. 그런데 승격은 못 했고 발견 셋이 나왔다.

| # | 실측 | 원인 | 수정 | 회귀 |
|---|---|---|---|---|
| U18-01 | shape 가 `ne_shape_step_005C_Li.csv` 로 게시됐다 (정본 이름은 `ne_shape_GITT_Li.csv`) | main 의 `--source "${SHAPE_SRC:-${SRC:-GITT}}"` — `SRC` 는 상태 loop 의 변수라 **마지막 상태**(300_0147, step_005C 전용)의 소스가 샜다. `test_g25` 는 `shape_step` 을 `--source GITT` 로 직접 불러 이 줄을 지나지 않는다 | shape 소스는 loop 와 무관하게 `SHAPE_SRC` 아니면 GITT, 요약 줄에 찍는다 | `test_g27` — production 스크립트를 **통째로** 돈다 (적합 세 명령은 PATH shim 이 rc 7 로 즉시 실패, `ne_shape` 호출은 argv 만 기록) |
| U18-02 | 13 중 **11** 이 `git_state_changed_during_run: true`. 트리는 깨끗했다 | `run` 의 시작 provenance 가 `provenance.py "$art"` 라 CLI 기본값 `output_roots=("out",)` 을 썼다 → `OUT=out_u18` 은 그 밖의 untracked 디렉터리라 **코드 변경**으로 분류 → `git_dirty_at_start: true`. 끝 상태는 `write_meta` 가 `output_roots=(out_dir,"out")` 로 물어 false → "실행 중 변경". 첫 산출만 clean (그때는 디렉터리가 비어 git 이 아무것도 보고하지 않는다) | CLI 가 둘째 인자부터를 산출 root 로 받고(`out` 은 늘 포함), `run` 이 `"${OUT:-out}"` 을 넘긴다 | `test_g28` — 산출 둘을 연달아 게시해 둘째의 `git_modified_code_at_start == ['out_alt/']` 를 재현 |
| U18-03 | 대조가 rc **2**(계약 위반)를 냈고 근거는 정본 `ne_shape_GITT_Li.csv.meta` 에 `env` 가 없다는 것 **하나** | 옛 정본의 **나이**를 새 산출의 위반으로 청구했다 — 자체 리뷰 C16 이 입력 identity 축에서 닫은 것과 같은 비대칭 (`env` 계약은 R10 P1-7 뒤에 생겼다) | `env_uncomparable` 버킷: 정본이 안 적었으면 **대조 불가**(rc 는 안 바꾸고 승격만 불가), **새 산출**이 안 적으면 그대로 계약 위반 | `test_g29` + 대조군 (새 산출에서 `env` 를 지우면 rc 2 · `schema` blocker) |

U18-02 는 위조 방향이 아니라 **거짓 양성**이다. 다만 `provenance.py` 머리말이 경고하는 고장 — "플래그가 늘 켜져
정보가 사라진다" — 을 wrapper 쪽에서 재현한 것이라, 그 축의 신호는 죽어 있었다.

**1 차 산출은 승격하지 않는다.** 고침은 다음 실행의 서명을 고칠 뿐 이미 적힌 sidecar 의 `true` 를 바꾸지 않고,
`matrix_100` 은 그 위에 **실제로** 실행 중 커밋이 바뀌었다 (`d07a77a` → `c9dd822` — 그 시간에 `git pull` 이 돌았다).
사면 규칙을 만들지 않고 깨끗한 트리에서 2 차(U18b)를 돈다. 승격 조건은 `numbers 0` · 계약 축 전부 0 ·
`provenance 0` 이고 **`inputs_uncomparable` 과 `env_uncomparable` 만 > 0** (둘 다 옛 정본의 나이 — 1 차 실측 17 · 1).

### 8-1. 2 차(U18b)와 승격 — 조건 7 닫음

고친 wrapper·checker 로 깨끗한 트리에서 다시 돌렸다 (사용자 기계, 같은 설정 `STATES='100 200 300_0009 300_0147'` ·
`STARTS=24` · `SI=Li`). 도중에 저장소에서 git 명령이 한 번 돌아 `matrix_300_0147` 하나가 또 `git_state_changed_during_run:
true` 가 됐고 **그 상태만 다시 게시**해 닫았다 (산출마다 독립 서명이라 전체 재실행이 필요 없다). 나머지 12 개는
`out_u18b/` 가 untracked 인데도 전부 clean — **U18-02 고침이 실데이터에서 확인된 지점**이다.

| 검사 | 결과 |
|---|---|
| `check_u14 --new out_u18b --old out` | **rc 4** · `numbers 0` · 명부 13/13/13 (missing·extra 없음) · 계약 축(schema·provenance_cols·content·unit·controls·env·alias·inputs·provenance·stale) **전부 0** · 남은 것은 `inputs_uncomparable 17` · `env_uncomparable 1` **뿐** — 둘 다 옛 정본의 나이다 |
| 승격 (`37a889b`) | 옛 정본 26 파일을 `out/archive/legacy_r6_u14/` 로 **얼려 보존**(조건 7 의 요구), 새 묶음이 `out/` 이 됐다. archive 는 자기 문서(`out/archive/README.md`)에 그 사실을 적는다 |
| 승격 뒤 `check_u14 --new out --schema-only` | **rc 0** — 사용자 기계와 **fresh clone(다른 기계)** 둘 다. 서명이 git 왕복(줄끝 정규화)을 견딘다는 뜻이고 U14-01 축을 실데이터로 다시 건 것이다 |
| 승격 뒤 `--old-rev <승격 직전 커밋>` | **`--old-rev 42314198e0beee59834d394cdba2757183503b59`** (= `37a889b^`) → rc 4 · 13/13 · `numbers 0` · `inputs_uncomparable 17` · `env_uncomparable 1` — 3 단계와 같은 판정. ⚠ **승격 커밋 뒤에는 `--old-rev HEAD` 를 쓰면 안 된다**: 그때 HEAD 의 `out/` 은 이미 새 정본이라 같은 run_id 13 개와 자기대조가 되고 도구가 `alias 13` 으로 **거부(rc 2)** 한다 — 맞는 동작이다 (Codex R14 P2-3, 실측 재현) |
| `compare_states.py out` | degeneracy 4/4 사용 · 제외 0 · "A 축에서 LLI 가 항상 가장 좁은가: **예**" · 묶음 불일치 경고 없음 |
| 옛 묶음(`out/archive/legacy_r6_u14/`) | `--schema-only` 가 **40 · 25 · 6 · 1** 을 그대로 낸다 — 표본이 바이트 단위로 살아 있다 |

**숫자는 이 라운드 내내 한 번도 안 움직였다.** 바뀐 것은 게시·서명 계약뿐이다.

### 8-2. U18-04 — 승격이 깨뜨린 것 (테스트 7 건, 닫음)

승격 직후 전체 테스트가 7 건 빨갰다. 원인은 셋으로 갈린다.

| 무엇 | 왜 | 고침 |
|---|---|---|
| `_ne_shape_csv` 가 `inputs_sha` 를 `float()` 로 읽어 ValueError (FINDINGS §1-12·§5-2·R3-03 표 대조 셋) | 헬퍼의 텍스트 열 목록이 `schema` 와 **별개의 사본**이었다. 정본이 22 열 계약이 되자 모르는 열을 숫자로 읽었다 — `test_i6w_07` 이 2026-09-12 에 "커밋된 산출이 아직 옛 스키마라 fixture 가 진실을 가린다" 고 적어 둔 바로 그 고장이 실제로 터졌다 | 목록을 `schema.SHAPE_NON_NUMERIC` 에서 **유도**한다 |
| `test_f26`(reader 가 정본 matrix 를 거부한다) · `test_d8_02`(`out/` schema-only rc 2) 의 전제 소멸 | 승격으로 정본이 새 계약이 됐다 — **그것이 승격의 뜻**이다 | 표본을 `out/archive/legacy_r6_u14/` 로. `d8_02` 에는 "현행 정본은 rc 0" 도 같이 고정해 이 검사가 "늘 rc 2" 를 재는 것이 아님을 못박았다 |
| `test_d8_07` 이 **전체 실행에서만** 실패 | 증거 재생성으로 같은 `replay_codex_r7.py` 를 동시에 돌린 탓. 단독 통과, 직렬 전체 실행 277 passed | 코드 변경 없음. 증거 재생성과 테스트를 겹쳐 돌리지 않는다 (§4 경고) |

교훈은 U14-05 와 같은 축이다 — **살아 있는 파이프라인 경로에 표본이나 역사 자료를 두면 재실행 한 번에 전제가
사라진다.** archive 는 그래서 있다.

회귀 전체: **277 passed** (승격 뒤 직렬 재실행). 증거는 `df6413d…` 에서 전부 재생성했고 러너 넷의 leaf 별 판정은
`ef8e8f6` 판과 같다.

# MXD2R-01 · 02 · 03 수정 증거 (2026-11-03) — 믹서 D2 개발 소비자

- 근거: Codex 10-27 독립 재검토 `docs/reviews/codex_mixer_d2_review_20261027/codex_review_mixer_d2_20261027.md` (HOLD · 새 P1 둘 · P2 하나) · 수정 계획 `docs/reviews/mxd2r_fix_plan_20261030.md` · **1저자 11-02 비준 Q1–Q3 = 전부 (가)** (생성기 자신의 문법만 · 접촉 제외 거부 + 재료 fix 완비성 · 적용 전 순서 · 실제 파일 바이트를 먼저 해시 · CRLF 는 구체 사유로 거부).
- 대상: `scripts/mixer_deck_readback.py` (`--d2` · `read_d2`) · `scripts/mixer_deck_diff.py` (`--allow D2` · `diff_d2_decks`) · `scripts/mixer_smoke_blind.py` (`--d2-plan` · `d2_plan_check`) · 회귀 `scripts/test_mixer_d2_consumers.py` · 웹앱 `/mixer` 개발 이력 `docs/mixer_devlog/v20_20261103.md`.
- 환경: 이 컨테이너 · Linux · Python 3.11.15 · `python3 -I -X utf8 -B`.  LIGGGHTS · DEM · 스케줄러 · 믹서 실행 0 회.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (claimed_fixed · Codex 재확인 전) | 닫지 않는 것 |
|---|---|
| MXD2R-01 시간 · 삽입 · 회전 = 생성기 문법만 | MXD2-01 전체 — 개발 소비자 하위 범위 종결은 Codex 재확인 GO 전에 주장하지 않는다 (수정 계획 §3 단계 6) |
| MXD2R-02 접촉 제외 거부 · pair 꼴 · 재료 fix 완비성 · 순서 · 생성기 상수 | 새 S1 셀 · 코호트 · 정책 · 등록 · 실물 입력 · 실제 DEM · 믹서 실행 (계획 §3 끝) |
| MXD2R-03 실제 파일 바이트 해시 · CR 거부 · 바이트를 디코딩해 파싱 | 범위 밖 공통 변조 17 (전역 설정 · 템플릿 옵션 · RNG 시드 · 기하 · 출력) — 여전히 PASS (§5-3) |
| | LIGGGHTS 토큰화 · 실행 의미의 실측 (소스 판독 인용만 · 실행 안 함) · 등록 표 · 코호트 경로의 텍스트 읽기 (D2 밖 · 그대로) |

## 1. 커밋 (이 작업 가지 — 본 가지로 cherry-pick 하면 SHA 가 바뀐다 · check_doc_refs 가 남은 옛 SHA 를 잡는다)

| 커밋 | 무엇 |
|---|---|
| `a9e82e019` | 시험 먼저 — Codex 공통 변조 여섯 · CRLF 두 방향 · 같은 부류 · 양성 48 (고치기 전 소비자) |
| `e77dc379a` | MXD2R-01 수정 (`_d2_time_grammar` · `_d2_lifecycle` 삽입 꼴 · 공동 회전 주기) |
| `8d4f9a94a` | MXD2R-02 수정 (`_d2_contact_grammar` · `D2_MATERIAL` 생성기 사본) |
| `6016d20ef` | MXD2R-03 수정 (`read_d2` 바이트 입력 · CR 거부 · 세 CLI 바이트 읽기 · `d2_text`) |
| `5ef8bb780` | 사전 공격 후속 — 같은 값 중복 재료 fix 시험 (변이 M11) · 삽입 꼴 사유에 첫 어긋난 토큰 |

## 2. 발견별 — 고치기 전 실패 · 고친 뒤 통과 · 바뀐 파일

커밋마다 그 커밋의 `scripts/` (git archive) 로 그 커밋의 `test_mixer_d2_consumers.py` 를 돌렸다 (`tools/per_commit_replay.py` → `per_commit/per_commit_replay.json` · 로그 `per_commit/replay_<커밋>.log` · 경로는 `<replay>` 로 가림).  칸 = 실패 subTest 수 F · 오류 E (ok = 통과).

| 시험 메서드 \ 커밋 | `a9e82e019` 시험 먼저 | `e77dc379a` 01 | `8d4f9a94a` 02 | `6016d20ef` 03 | `5ef8bb780` 후속 |
|---|---|---|---|---|---|
| 기존 13 메서드 | ok ×13 | ok ×13 | ok ×13 | ok ×13 | ok ×13 |
| test_mxd2r01_codex_time_insert_rotation | F24 | ok | ok | ok | ok |
| test_mxd2r01_same_class_generator_grammar | F24 | ok | ok | ok | ok |
| test_mxd2r02_codex_contact_exclusion_and_friction | F12 | F12 | ok | ok | ok |
| test_mxd2r02_same_class_contact_and_materials | F39 | F39 | ok | ok | ok |
| test_mxd2r02_material_copies_match_generator | E1 | E1 | ok | ok | ok |
| test_mxd2r03_physical_bytes_api | F11 | F11 | F11 | ok | ok |
| test_mxd2r03_physical_bytes_cli_both_directions | F6 | F6 | F6 | ok | ok |
| test_mxd2r_positive_codex_independent_48 (양성 보존) | ok | ok | ok | ok | ok |
| 합 (21 시험) | FAILED (failures=116, errors=1) | FAILED (failures=68, errors=1) | FAILED (failures=17) | OK | OK |

- 고치기 전 실패 116 의 단언 문구 (전부 '옳은 이유' — 반례를 소비자가 받았거나 바이트를 못 받음): API `AssertionError: 'PASS' != 'FAIL'` 83 · CLI `AssertionError: 0 != 1 : D2 개발 덱 계약 PASS — 실제 런/코호트/발사 인증 아님` 21 · 바이트 API `deck text must be a string` 6 · LF 바이트 양성 `'FAIL' != 'PASS'` 3 · CRLF+CRLF 메타 CLI `'LF-only' not found in '… metadata SHA256 != actual deck'` 3 (정규화 텍스트의 해시로 거부 = 결함 그대로) · 오류 1 = `module 'mixer_deck_readback' has no attribute 'D2_MATERIAL'`.
- 5ef8bb780 의 same_class 는 사례 14 (같은 값 중복 추가) — 앞 커밋들의 시험 파일은 13.  subTest 실측 (`tools/count_subtests.py` → `after/subtest_counts_5ef8bb780.json` · 중첩 subTest 는 바깥 사례도 하나로 센다): 01 Codex 28 (= 사례 4 + 안쪽 24) · 01 같은 부류 32 (8 + 24) · 02 Codex 14 (2 + 12) · 02 같은 부류 56 (14 + 42) · 03 API 11 · 03 CLI 9 · 양성 48.

고친 뒤 거부 사유 — CLI 화면 그대로 (`after/codex_cases_cli/cli_logs_after.txt` · Codex 받은 사례 파일):

- **MXD2R-01** (고치기 전 = 네 공통 변조 세 소비자 PASS · CLI rc 0) — 바뀐 파일 `scripts/mixer_deck_readback.py`
  - run_upto: «D2 time contract: only two-token \`run <integer>\` (generator grammar) — run options such as upto · start · stop · pre · post · every change the executed step program: \`run 1 upto\`»
  - late_timestep: «D2 time contract: exactly one two-token \`timestep <dt>\` before the first run (dt set once, unchanged after) — found 1 at command index [53] · first run at [40]»
  - insert_start_late: «D2 insertion contract: insert/pack must be the generator form (…) — start · repeat (insert_every N) · other options rejected: fix insA token 12 \`start\` (generator \`overlapcheck\`)»
  - front_period: «D2 rotation contract: every wall mesh must rotate with the Drum period (common rotation) — Back 0.782508 s · Drum 0.782508 s · Front 0.1 s»
- **MXD2R-02** (고치기 전 = `neigh_modify exclude type 3 3` · coefficientFriction 삭제 PASS · rc 0) — 바뀐 파일 `scripts/mixer_deck_readback.py`
  - exclude_SE_SE: «D2 contact contract: exactly one \`neigh_modify delay 0\` after create_box and before the first run — exclude and other neighbor options change which contacts are computed: \`neigh_modify delay 0\` | \`neigh_modify exclude type 3 3\`»
  - friction_missing: «D2 contact contract: material fix missing for the supported hertz/sjkr/rolling_friction pair and wall model: coefficientFriction»
- **MXD2R-03** (고치기 전 = CRLF 덱 + LF 메타 rc 0/0/0 · CRLF 덱 + CRLF 메타 rc 1/1/1 이지만 사유 = LF 로 정규화한 텍스트의 해시) — 바뀐 파일 `scripts/mixer_deck_readback.py` · `scripts/mixer_deck_diff.py` · `scripts/mixer_smoke_blind.py`
  - crlf_lf_metadata: «metadata SHA256 != actual deck file bytes»
  - crlf_crlf_metadata: «deck contains 179 CR (0x0D) byte(s) — CRLF/CR line endings are rejected: D2 development decks are LF-only generator output (never normalized before hashing or parsing)»
- (공통) `scripts/test_mixer_d2_consumers.py` — 새 8 메서드 · 기존 CLI 시험의 덱 쓰기를 바이트로 (Linux 동작 같음 · Windows 개행 무관) · `docs/mixer_devlog/v20_20261103.md` — 웹앱 `/mixer` 개발 이력 v2.0 (코드 → 웹앱 같은 묶음).

## 3. 기존 시험 전 · 후 (같은 명령 · 이 컨테이너)

| 시험 | 전 (커밋 `57f1b2baf` 기반) | 후 (커밋 `5ef8bb780`) | 로그 |
|---|---|---|---|
| `scripts/test_mixer_d2_consumers.py` | 13/13 OK | 21/21 OK (기존 13 그대로 + 새 8) | `before/test_mixer_d2_consumers_13_base_57f1b2baf.log` · `per_commit/replay_5ef8bb780.log` |
| `scripts/mixer_deck_readback.py --selftest` | 24/24 PASS | 24/24 PASS | `before/readback_selftest_before.log` · `after/readback_selftest_after.log` |
| `scripts/mixer_deck_diff.py --selftest` | 55/55 PASS | 55/55 PASS | `before/diff_selftest_before.log` · `after/diff_selftest_after.log` |
| `scripts/mixer_smoke_blind.py --selftest` | rc 0 · ✓ 31 줄 (항목 30 + "전부 통과") · ✗ 0 | rc 0 · ✓ 31 · ✗ 0 | `before/smoke_selftest_before.log` · `after/smoke_selftest_after.log` |
| `webapp/test_mixer_devlog_page.py` | 9/9 PASS | 9/9 PASS (v2.0 항목 포함) | `before/devlog_page_before.log` · `after/devlog_page_after.log` |

- 다른 해석기: 3.10 · 3.12 · 3.13 은 numpy 가 없어 실행 못 함 (설치 금지).  Python 3.8 은 `ast.parse(feature_version=(3, 8))` 문법 검사만 (네 파일 OK) — kgy 3.8 실행 아님.
- 시험 로그의 `ResourceWarning: unclosed file … make_mixer_deck.py:1122` 은 생성기의 기존 경고 (이번 변경 밖).

## 4. Codex 가 보낸 사례 파일 — 판정문 명령 그대로 (세 CLI rc · `--json` 없이)

도구 = 10-30 재현 도구 그대로 `docs/reviews/codex_mixer_d2_review_20261027/_repro_ours_20261030/tools/run_d2_cli_cases.py` · 입력 = `docs/reviews/codex_mixer_d2_review_20261027/d2/evidence/cases/` (바이트 그대로 · CRLF 덱 13833 B).  readback / pair / plan.

| 사례 | 전 (커밋 `57f1b2baf`) | 후 (커밋 `5ef8bb780`) |
|---|---|---|
| run_upto · late_timestep · insert_start_late · front_period | 0/0/0 | 1/1/1 |
| exclude_SE_SE | 0/0/0 | 1/1/1 |
| crlf_lf_metadata | 0/0/0 | 1/1/1 (SHA 사유) |
| crlf_crlf_metadata | 1/1/1 (정규화 텍스트 SHA 사유) | 1/1/1 (CR 179 개 · LF-only 사유) |
| (대조) normal | 0/0/0 | 0/0/0 |
| (대조) friction_missing | 0/0/0 | 1/1/1 |
| (음성 대조) bad_gravity · remove_integrator | 1/1/1 | 1/1/1 |

Traceback 0 (전 · 후).  JSON = `before/codex_cases_cli/cli_rc_codex_cases_before.json` · `after/codex_cases_cli/cli_rc_codex_cases_after.json` · 화면 = 같은 폴더 `cli_logs_*.txt` (`tools/concat_cli_logs.py` 로 사례 33 개를 한 파일로).

## 5. 사전 공격 (CLAUDE.md "Codex 요청 전 사전 공격 리뷰" ② ③)

### 5-1. 바뀐 함수마다 NaN · inf · 빈 · 중복 · 공백 · Unicode 숫자 · 바이트 꼴 — 72/72 보장대로

`tools/preattack_probe.py` → `preattack/preattack_probe.json` (두 덱에 같이 · 메타 재결합 · 세 API — 바이트 꼴은 readback API).  FAIL 사례의 첫 사유는 모두 명시 사유 (우연한 TypeError · KeyError 0 · str 서러게이트 = UnicodeEncodeError 로 FAIL).

| 함수 | 사례 | 결과 |
|---|---|---|
| `_d2_time_grammar` | run nan · inf · 빈 · 앞자리 0 · + 부호 · 소수 · Unicode 숫자 · upto 두 번 · `&` 이어 쓴 upto · NBSP 로 붙인 upto · timestep nan · inf · 빈 · 같은 값 두 번 · Unicode 숫자 | 전부 FAIL |
| (같은 뜻 꼴) | run 탭 구분 · run 뒤 주석 `# upto` · 줄 끝 공백 | PASS (같은 명령) |
| `_d2_lifecycle` | insert_every nan · 0 · once 두 번 · ntry Unicode · 속도 -inf · 속도 같은 값 다른 표기 · Front 주기 nan · inf · 음수 · 0 · 끝자리 1e-6 · Unicode 숫자 · Front 두 번 회전 | 전부 FAIL |
| (같은 뜻 꼴) | Front 주기 `7.82508e-1` (Drum 과 같은 float) | PASS |
| `_d2_contact_grammar` | neigh delay nan · Unicode · 같은 줄 두 번 · NBSP 로 붙인 exclude · pair_coeff 두 번 · 마찰 nan · inf · Unicode · 행렬 크기 Unicode · 빈 행렬 · 17 값 · charVel nan · 이름 없는 property/global · CED fix 둘 | 전부 FAIL |
| (같은 뜻 꼴) | neigh 탭 구분 · 마찰 `9e-1` (= 0.9) · 폼 피드 구분 | PASS |
| `read_d2` 바이트 | LF 바이트 PASS · 주석 안 CR 하나 · CR 만 줄바꿈 · CRLF · 잘못된 UTF-8 · UTF-16 (BOM · 무 BOM) · 빈 바이트 · 끝 NUL · bytearray · memoryview · None · 서러게이트 str · 메타 길이 +1 · 길이 bool · 대문자 SHA · BOM 머리 | PASS 1 · 나머지 FAIL |
| 따옴표 `"#"` (고정된 줄) | run · neigh_modify · insert/pack · Front move/mesh · Front mesh/surface 뒤에 `"#" …` | 전부 FAIL (남은 `"` 토큰) |

- 일부러 엄격하게 둔 것 (생성기 표기 그대로): run 정수 (앞자리 0 · + 거부) · insert/pack 토큰 (`0.0 0.0 -0.20` 도 거부) · `neigh_modify delay 0` · `pair_coeff * *` 은 **토큰 그대로**.  회전 주기 · 재료 계수는 **float 같음** (같은 double 이면 받음).
- NUL 이 **주석 안**에 있는 덱은 PASS (주석은 판정 밖).  UTF-16 은 CR 규칙으로 먼저 거부된다 (인코딩 바이트에 0x0D) — 거부 사유가 인코딩이 아니라 CR 이다.
- LIGGGHTS 쪽 토큰 구분자 (NBSP · 폼 피드) 는 대조하지 않았다 — 표의 '같은 뜻' 은 Python 쪽 판정과 생성기 문법 기준이다.

### 5-2. 변이 시험 — 가드를 하나씩 끄면 새 시험이 잡는가

`tools/mutation_check.py` (커밋의 `scripts/` 사본에서 가드 하나를 정확한 문자열 치환으로 끄고 시험 → 되돌림).

- 1 회차 (커밋 `6016d20ef`): **18/19 죽음 · M11 '재료 fix 중복 허용' 생존** — 시험의 중복 덱은 값이 0.1 이라 상수 검사가 먼저 거부해 중복 규칙이 묶이지 않았다 (`preattack/mutation_check_v1_6016d20ef_console.txt` · 화면 그대로 · 이 회차 JSON 은 2 회차가 덮어썼다).
- 고침 (커밋 `5ef8bb780`): 같은 값 (0.9) 중복 사례 `friction_duplicate_same_values` (사유 = defined more than once).
- 2 회차 (커밋 `5ef8bb780`): **19/19 죽음** · 변이 없는 판 rc 0 (`preattack/mutation_check_v2_5ef8bb780.json`).  가드 = run 옵션 · timestep 위치 · timestep 토큰 수 · 삽입 꼴 · 공동 주기 · neigh 인자 · neigh 개수 · pair 위치 · pair_coeff 인자 · 재료 결손 · 중복 · 상수 · 순서 · 모르는 이름 · CR · 정규화 해시 · 세 CLI 의 바이트 읽기.

### 5-3. 범위 밖 공통 변조 — 여전히 PASS (닫지 않음 · 1저자 11-02 비준 범위 밖)

`tools/preattack_outside_scope.py` → `preattack/preattack_outside_scope.json` — 17/17 세 소비자 PASS.

| 부류 | 사례 | 메모 (LIGGGHTS 실행 · 소스 대조 안 함) |
|---|---|---|
| 전역 설정 | `boundary p p p` · `newton on` · `atom_style sphere` · `communicate … cutoff` · `hard_particles no` · `atom_modify sort` | 생성기는 고정 문구를 쓴다 · 개발 소비자는 값 의미를 보지 않는다 |
| 템플릿 옵션 | `particletemplate/sphere … volume_limit 1e-30` · 같은 줄 `… "#" volume_limit 1e-30` | 뒤 토큰을 보지 않는다 (줄 길이 미고정) |
| RNG 시드 | 분포 시드 · 둘째 삽입 시드 | v1.8 한정 그대로 — "모든 난수열의 생성기 서명은 별도 검증 대상" |
| 기하 | 삽입 영역 반지름 · 메시 scale | `_d2_lifecycle` 한정 그대로 — "Geometry remains supplied input" |
| 출력 · 체크포인트 | `dump_modify` 추가 · `thermo` 간격 · `write_restart` 삭제 | 물리 밖 |

- 같은 부류의 표기 차이: 소비자 파서는 줄의 첫 `#` 부터 주석으로 버린다 (`_logical`) — 따옴표 안 `#` 를 LIGGGHTS 가 어떻게 읽는지는 대조하지 않았다.  토큰 수 · 꼴이 고정된 줄 (run · timestep · insert/pack · neigh_modify · pair_coeff · 재료 fix · region · create_box · 메시 · 벽 · 중력 · 적분기 · move/mesh · 분포) 은 `"` 토큰이 남아 거부되고, 고정되지 않은 줄 (템플릿 · 전역 설정 · 출력) 에만 이 차이가 남는다.
- ⬜ **1저자 결정 후보 (권고 = 고정)**: 전역 설정 · 템플릿 줄도 같은 (가) 원리로 생성기 꼴 고정할지 — 이번 비준 범위 (시간 · 삽입 · 회전 · 접촉 제외 · 재료 fix · 바이트) 밖이라 구현하지 않았다.  Codex 재확인에서 같은 부류로 지적될 수 있다.

## 6. 한정

- 의미는 계산하지 않는다 — `run upto` · 늦은 dt · 삽입 스케줄 · 메시별 주기 · 접촉 제외의 실제 효과는 Codex 판정문의 LIGGGHTS 3d5c00f 소스 판독 인용이고, 우리는 생성기 꼴 밖을 거부할 뿐이다.
- 생성기 꼴 · 상수는 사본이다 (생성기를 import 하지 않는다) — 생성기가 바꾸면 개발 소비자가 거부해 드러난다 (fail-closed · `test_mxd2r02_material_copies_match_generator` · 양성 시험).
- 재료 fix 순서 = 생성기 순서 (create_box 뒤 · pair_style · wall/gran 앞) — LIGGGHTS 가 요구하는 '첫 run 전' 보다 엄격해 의미가 같은 재배치도 거부한다.
- API 의 str 입력 = 그 UTF-8 이 파일 바이트라고 본다 (메모리 텍스트).  실제 파일 바이트는 세 CLI 만 읽는다.  `diff --allow D2` 의 못 읽는 파일은 옛 `_read` 와 같이 None → 소비자 거부 rc 1 (readback · smoke 는 argparse rc 2 그대로).
- 실행 OS = Linux 하나.  기존 CLI 시험의 덱 쓰기를 바이트로 바꿔 Windows (Codex 환경) 의 개행 변환에도 같은 바이트가 되게 했다 — Windows 실행 확인은 하지 않았다.
- 판정문 §7 최소 해제 증거 (1) 공통 명령 변조 거부 (2) 접촉 제외 거부 (3) 실제 바이트 결합 (4) 양성 보존 (정상 2 상/3 상 · 밀도 두 세대 · 층상/균일 · ρ = 1 퇴화 · Codex 독립 48 조합 · `registered=null` · `execution_authorized=false`) — (1)–(3) 은 §2 · §4 · (4) 는 기존 시험 + `test_mxd2r_positive_codex_independent_48`.
- 원장: MXD2R-01 · 02 · 03 = claimed_fixed (Codex 재확인 전 · verified 아님).  MXD2-01 은 손대지 않았다 (open 그대로).

## 7. 재현

```bash
python3 -I -X utf8 -B scripts/test_mixer_d2_consumers.py                         # 21/21
python3 scripts/mixer_deck_readback.py --selftest                                # 24/24
python3 scripts/mixer_deck_diff.py --selftest                                    # 55/55
python3 scripts/mixer_smoke_blind.py --selftest                                  # rc 0
python3 webapp/test_mixer_devlog_page.py                                         # 9/9
python3 -I docs/reviews/codex_mixer_d2_review_20261027/_repro_ours_20261030/tools/run_d2_cli_cases.py \
  "$PWD/scripts" "$PWD/docs/reviews/codex_mixer_d2_review_20261027/d2/evidence/cases" codex_cases_after <OUT>
python3 -I -X utf8 -B docs/reviews/mxd2r_fix_evidence_20261103/tools/preattack_probe.py "$PWD/scripts" <OUT>.json
python3 -I -X utf8 -B docs/reviews/mxd2r_fix_evidence_20261103/tools/preattack_outside_scope.py "$PWD/scripts" <OUT>.json
# 커밋별 · 변이: git archive <커밋> scripts | tar -x -C <ROOT>/<커밋> 뒤
python3 -I docs/reviews/mxd2r_fix_evidence_20261103/tools/per_commit_replay.py <ROOT> <OUT>.json <커밋> …
python3 -I docs/reviews/mxd2r_fix_evidence_20261103/tools/mutation_check.py <ROOT>/<커밋>/scripts <OUT>.json
```

## 8. 파일

`SHA256SUMS` = 이 폴더의 파일 전부 (자신 제외 · `sha256sum -c SHA256SUMS` 로 대조).

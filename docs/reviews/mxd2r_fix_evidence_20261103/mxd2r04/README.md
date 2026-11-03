# MXD2R-04 수정 증거 (2026-11-03) — 믹서 D2 개발 소비자: 명령 전부 = 생성기 꼴

- 근거: 11-03 사전 공격 (상위 `../README.md` §5-3 — MXD2R-01–03 범위 밖 공통 변조 17 이 세 소비자 PASS) · **1저자 11-03 비준 Q1 = 권고대로** (공통 변조 17 도 생성기 꼴로 고정 · 원리 = MXD2R-01–03 의 (가) — 생성기 자신의 꼴만 받고 모르는 뜻은 계산하지 않고 거부).
- 대상: `scripts/mixer_deck_readback.py` — 새 `_d2_text_form` · `_d2_generator_form` (read_d2 끝 · 세 소비자 공통: `readback --d2` · `diff --allow D2` (`diff_d2_decks` → read_d2 둘) · `smoke --d2-plan` (`d2_plan_check` → read_d2)) · 회귀 `scripts/test_mixer_d2_consumers.py` · 웹앱 `/mixer` 개발 이력 `docs/mixer_devlog/v21_20261103.md` · 수정 계획 상태 줄 `docs/reviews/mxd2r_fix_plan_20261030.md`.
- 환경: 이 컨테이너 · Linux · Python 3.11.15 · `python3 -I -X utf8 -B`.  LIGGGHTS · DEM · 스케줄러 · 믹서 실행 0 회.

## 한정 (1저자 지시 문구 그대로 — 아래 §6 이 자세히)

- **뜻이 같아도 표기가 다르면 거부한다 (생성기 꼴 엄격).**
- **LIGGGHTS 실행 · Windows · Python 3.8 실행은 확인하지 않았다.**

> ★ 11-03 밤 범위 넓힘 (1저자 Q4 = 권고대로) — 첫 판의 유일한 자유 칸 **neighbor skin 값**도 생성기 꼴로 고정했다 (자유 칸 없음 · 기존 시험 `test_actual_command_scope` 의 기대를 바꿈) → **§9**.  §0 – §8 은 첫 판 (커밋 `42dcdc7f9` 까지) 기록이고, skin 을 자유 칸으로 적은 줄에는 §9 표지를 달았다.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (claimed_fixed · Codex 재확인 전) | 닫지 않는 것 |
|---|---|
| MXD2R-04 — 사전 공격 17 (전역 설정 · 템플릿 뒤 옵션 · 따옴표 `#` · RNG 시드 · 기하 · 출력 · 체크포인트) | MXD2-01 전체 · MXD2R-01–03 의 Codex 재확인 (상태 그대로) |
| 같은 부류 47 (같은 값 다른 표기 · 생성기 이름 · 순서 · 중복 · 결손 · 배플 · 마지막 run 뒤 명령 · skin 토큰 꼴) | neighbor skin **값** (자유 칸 — 기존 시험 `test_actual_command_scope` 가 단일 덱 PASS 를 요구 · 두 덱에 같이 바꾸면 세 소비자 PASS = 남은 같은 부류 · §6) → **11-03 밤 Q4 로 닫음 (§9)** |
| 글자 꼴 14 (탭 · 제어 문자 · 비 ASCII · 따옴표 · `$` · 이음 꼴 · 끝 줄바꿈 · 주석 끝 `&`+유니코드 공백) | LIGGGHTS 가 그 글자들을 실제로 어떻게 읽는지의 실측 (소스 규약 판독 · 실행 안 함) |
| 메타까지 같이 바꾼 덱 6 + timestep 표기 3 (메타 결합으로는 못 잡는 표기 · 규칙) | 새 S1 셀 · 코호트 · 정책 · 등록 · 실물 입력 · 실제 DEM · 믹서 실행 |

## 1. 커밋 (이 작업 가지 — 본 가지로 cherry-pick 하면 SHA 가 바뀐다 · check_doc_refs 가 남은 옛 SHA 를 잡는다)

| 커밋 | 무엇 |
|---|---|
| `85e2d66d8` | 시험 먼저 — 범위 밖 17 · 같은 부류 46 · 글자 꼴 13 · timestep 표기+메타 · 양성 보존 · 사본 대조 (고치기 전 소비자) |
| `49608570a` | MXD2R-04 수정 (`_d2_text_form` · `_d2_generator_form` · 사본 상수 · read_d2 끝에서 호출) |
| `52d84d9eb` | 사전 공격 후속 — 변이 1 회차 생존 7 을 시험에 묶음 (새 사례 8 · 소비자 코드 무변경) |
| (이 폴더를 넣은 커밋) | 증거 · 원장 MXD2R-04 · `/mixer` v2.1 · 수정 계획 상태 줄 · 상위 README 표지 · `scripts/mixer_deck_readback.py` **주석 두 줄만** (skin 자유 칸 서술 정정 — 동작 무변경 · 시험 28/28 그대로 · 변이 문자열에 안 걸림) |

## 2. 고치기 전 → 뒤

커밋마다 그 커밋의 `scripts/` (git archive) 로 그 커밋의 `test_mixer_d2_consumers.py` 를 돌렸다 (`../tools/per_commit_replay.py` → `per_commit/per_commit_replay.json` · 로그 `per_commit/replay_<커밋>.log`).  칸 = 실패 subTest 수 F · 오류 E · ok · `-` = 그 판에 없는 시험.

| 시험 메서드 \ 커밋 | `fe103fc01` 기반 | `85e2d66d8` 시험 먼저 | `49608570a` 수정 | `52d84d9eb` 후속 |
|---|---|---|---|---|
| 기존 21 메서드 (MXD2R-01–03 · 양성 48 포함) | ok ×21 | ok ×21 | ok ×21 | ok ×21 |
| test_mxd2r04_outside_scope_17_api_and_cli | - | F102 | ok | ok |
| test_mxd2r04_same_class_spelling_identity_order | - | F138 | ok | ok |
| test_mxd2r04_parser_equivalence_characters | - | F51 | ok | ok |
| test_mxd2r04_timestep_spelling_with_metadata | - | F9 | ok | ok |
| test_mxd2r04_copies_match_generator | - | E1 | ok | ok |
| test_mxd2r04_positive_generator_options (양성 보존) | - | ok | ok | ok |
| test_mxd2r04_metadata_coordinated_rules (후속) | - | - | - | ok |
| 합 | 21 OK | 27 FAILED (failures=300, errors=1) | 27 OK | 28 OK |

- 고치기 전 실패 300 은 전부 '옳은 이유' — 소비자가 변조 덱을 **받았다**: API `AssertionError: 'PASS' != 'FAIL'` 237 · CLI `AssertionError: 0 != 1 : D2 개발 덱 계약 PASS …` 63 · 오류 1 = `module 'mixer_deck_readback' has no attribute 'D2_GLOBAL_FORM'` (사본 상수 없음).
- 후속 커밋의 새 사례 8 (메타 동반 6 · 같은 부류 `command_appended_at_end` · 글자 꼴 `comment_continuation_ascii`) 을 고치기 전 소비자 (커밋 `fe103fc01` 의 scripts + 후속 시험 파일) 에서 돌림 = 8 사례 × API 3 = **24/24 PASS (결함)** · `before/followup_cases_on_prefix_c3bf134b9.log` (scratch 경로 = `<scratch>`).
- subTest 실측 (커밋 `52d84d9eb` · `../tools/count_subtests.py` → `after/subtest_counts_89315d8d2.json` · 바깥 사례도 하나로 센다): 범위 밖 17 = 119 (17 + 17×6 = API 3 + CLI 3) · 같은 부류 188 (47 + 47×3) · 글자 꼴 68 (14 + 14×3 + CLI 4×3) · timestep 12 (3 + 9) · 메타 동반 24 (6 + 18) · 양성 10.

고친 뒤 거부 사유 — 범위 밖 17 (readback API 첫 사유 · 꼬리 설명 생략 · 같은 사유가 세 CLI 화면에 그대로 나온다 — 시험이 rc 1 · 사유를 확인):

| 사례 | 사유 |
|---|---|
| boundary_periodic | D2 generator form: command 4 `boundary p …` token 1 `p` (generator `f`) |
| newton_on | D2 generator form: command 5 `newton on …` token 1 `on` (generator `off`) |
| atom_style_sphere | D2 generator form: command 1 `atom_style sphere …` token 1 `sphere` (generator `granular`) |
| communicate_cutoff | D2 generator form: command 6 `communicate single …` token 2 `cutoff` (generator `vel`) |
| hard_particles_no | D2 generator form: command 3 `hard_particles no …` token 1 `no` (generator `yes`) |
| atom_modify_sort | D2 generator form: command 2 `atom_modify map …` token 4 `1000` (generator `0`) |
| thermo_lost_error | D2 generator form: command 38 `thermo_modify lost …` token 2 `error` (generator `ignore`) |
| neighbor_nsq | D2 generator form: command 10 `neighbor 7.57e-05 …` token 2 `nsq` (generator `bin`) |
| template_extra_option | D2 generator form: command 27 `fix pt1 …` token 13 `volume_limit` (generator `(end)`) |
| template_quote_hash | D2 generator form: line 111: command text must be printable ASCII without quotes or $ — 'fix pt1 all particletemplate/sphere 1048' |
| pdd_seed | D2 generator form: command 30 `fix pddA …` token 4 `15485863` (generator `32452867`) |
| insert_b_seed | D2 generator form: command 47 `fix insB …` token 5 `15485867` (generator `32452867`) |
| insert_region_geometry | D2 generator form: command 32 `region ins_reg …` token 6 `0.0100000` (generator `0.0113249`) |
| mesh_scale | D2 generator form: command 23 `fix Drum …` token 9 `0.0250000` (generator `0.0251665`) |
| dump_modify_added | D2 generator form: command 44 `dump_modify dmp …` token 0 `dump_modify` (generator `run`) |
| thermo_every | D2 generator form: command 37 `thermo 1000 …` token 1 `1000` (generator `5000`) |
| write_restart_removed | D2 generator form: command 50 `fix mvD …` token 0 `fix` (generator `write_restart`) |

- 바뀐 파일: `scripts/mixer_deck_readback.py` (사본 상수 `D2_GLOBAL_FORM` · `D2_DRUM` · `D2_DIST_SEED` · `D2_MESHES` · `D2_DUMP_COLUMNS` · `D2_DUMP_FORMAT` · `D2_SEED_MAX` · 함수 `_d2_next_prime` · `_d2_text_form` · `_d2_generator_form` · read_d2 끝 호출 · 결과에 `generator_form` 설명 칸) · `scripts/test_mixer_d2_consumers.py` (새 7 메서드 · `fixture` 에 선택 인자 `dump_full_precision` · `fr` — 기본값 = 옛 동작) · `docs/mixer_devlog/v21_20261103.md` · `docs/reviews/mxd2r_fix_plan_20261030.md` (상태 줄) · `docs/reviews/findings.json` (MXD2R-04 · MXD2R-02 메모 한 줄) · `../README.md` (표지 · §0 · §5-3 · §7 한 줄씩).  `scripts/mixer_deck_diff.py` · `scripts/mixer_smoke_blind.py` 는 바꾸지 않았다 (read_d2 를 부른다).

## 3. 기존 시험 · 대조 전 · 후 (같은 명령 · 이 컨테이너)

| 시험 | 전 (소비자 = 커밋 `f2f63e7cd` · `fe103fc01` 같음) | 후 (커밋 `52d84d9eb` · 소비자 = 커밋 `49608570a`) | 로그 |
|---|---|---|---|
| `scripts/test_mixer_d2_consumers.py` | 21/21 OK | 28/28 OK (기존 21 그대로 + 새 7) | `per_commit/replay_c3bf134b9.log` · `per_commit/replay_89315d8d2.log` |
| Codex 독립 정상 48 조합 (`test_mxd2r_positive_codex_independent_48`) | 48 PASS | 48 PASS | 같은 로그 |
| `scripts/mixer_deck_readback.py --selftest` | 24/24 PASS | 24/24 PASS | `../after/readback_selftest_after.log` · `after/readback_selftest_after.log` |
| `scripts/mixer_deck_diff.py --selftest` | 55/55 PASS | 55/55 PASS | `../after/diff_selftest_after.log` · `after/diff_selftest_after.log` |
| `scripts/mixer_smoke_blind.py --selftest` | rc 0 · ✓ 31 · ✗ 0 | rc 0 · ✓ 31 · ✗ 0 (화면 같음) | `../after/smoke_selftest_after.log` · `after/smoke_selftest_after.log` |
| `webapp/test_mixer_devlog_page.py` | 9/9 PASS | 9/9 PASS (v2.1 이 맨 앞) | `../after/devlog_page_after.log` · `after/devlog_page_after.log` |
| Codex 받은 사례 (판정문 명령 그대로 · 세 CLI) | 반례 7 = 1/1/1 · normal 0/0/0 · friction_missing 1/1/1 · 음성 대조 둘 1/1/1 | rc · 입력 지문 · 첫 줄 · 화면 (경로 가림) **전부 같음** | `../after/codex_cases_cli/` · `after/codex_cases_cli/` |

- 새 검사는 read_d2 **끝** (기존 검사 뒤) 에 둔다 — 기존 반례의 사유가 먼저 나와 MXD2R-01–03 시험의 사유 단언 · Codex 사례 화면이 바뀌지 않는다.
- 다른 해석기: 3.10 · 3.12 · 3.13 은 numpy 가 없어 실행 못 함 (설치 금지).  Python 3.8 = `ast.parse(feature_version=(3, 8))` 문법 검사만 (readback · 시험 파일 OK · `math.isqrt` = 3.8+) — kgy 3.8 실행 아님.

## 4. 사전 공격 (CLAUDE.md "Codex 요청 전 사전 공격 리뷰" ② ③)

### 4-1. 바뀐 함수마다 — 85/85 보장대로

`tools/preattack_probe_v2.py` → `preattack/preattack_probe_v2.json` (두 덱에 같이 · 메타 해시 · 길이 재결합 (+ 적힌 메타 고침) · 세 API · 바이트 행 = readback API 바이트).  FAIL 행은 사유 조각까지 확인 (우연한 다른 사유가 아님).

| 공격 대상 | 사례 (기대) | 결과 |
|---|---|---|
| `_d2_text_form` 제어 문자 | 탭 (코드 · 주석) · 폼 피드 · NUL (코드 · 주석) · DEL · NEL (U+0085) · ESC (FAIL 8) | 전부 FAIL (control character) |
| `_d2_text_form` 명령 글자 | NBSP · U+3000 · U+2028 · 폭 없는 공백 · 전각 이름 · 키릴 동형 글자 · 결합 부호 · 전각 숫자 · 작은따옴표 · 따옴표 `#` · `${…}` · `$(…)` (FAIL 12) | 전부 FAIL — 전각 이름은 앞 검사 (모르는 명령) 가 먼저 |
| `_d2_text_form` 이음 | 주석 끝 `&`+NBSP · +U+3000 · ASCII `&` · 명령 `&` 뒤 주석 · `4&` · `& ` · `&`+NBSP · `&&` · 이음 뒤 빈 줄 · `&` 만인 줄 · 끝 줄바꿈 없음 · 끝 NUL (FAIL 12) | 전부 FAIL — `&&` (행렬 17 값) · 끝 NUL (모르는 명령) · `&`+NBSP (ASCII 규칙) 은 앞 검사가 먼저 |
| 배치 (자유 · PASS 9) | 빈 줄 · 주석 줄 (한글 포함) · 주석 안 NBSP · 주석 안 U+2028 · 명령 앞 공백 · 한 칸 공백 배치 · 명령 뒤 ASCII 공백 · 명령 뒤 주석 · 끝 빈 줄 | 전부 PASS |
| `_d2_generator_form` skin 자유 칸 | nan · inf · 빈 · 0 · 음수 · 뒤 토큰 (FAIL 6) · `0.0000757` · ×1.1 (PASS 2 — 두 덱에 같이 바꾼 공통 변조가 세 소비자 PASS = **자유 칸 기록** · §6) | 보장대로 |
| `_d2_generator_form` 고정 칸 | 상자 nan · scale inf · CED `.0` 표기 · 마찰 전각 · `9e-1` · 분포 B 시드 = A · 둘째 삽입 시드 = 첫 · compute 중복 · thermo_modify 결손 · 마지막 run 뒤 명령 · Front 주기 `7.82508e-1` · 원점 `0.0` (FAIL 12) | 전부 FAIL |
| 메타 동반 (해시 재결합 + 메타 고침) | 합성수 시드 · 2^31−1 넘는 소수 · dt `e-7` · `+` 부호 · k = 2 · 3 표기 · k 배 아닌 정착 step · 규칙 밖 dump · restart 간격 (FAIL 9) | 전부 FAIL |
| 전 정밀도 dump 줄 | 정확한 줄 (PASS) · 두 칸 · 뒤 주석 · 메타만 다른 형식 · 메타+줄 같이 · 줄 결손 · 중복 · 메타 선언 없음 (FAIL 7) | 보장대로 |
| `read_d2` 바이트 | LF (PASS) · `&`+C2 A0 · 주석 안 NUL · 겹친 NUL (C0 80 · 잘못된 UTF-8) · CRLF · BOM · 탭 (FAIL 6) | 보장대로 |

### 4-2. 1 회차 사전 공격 도구 다시 (`../tools/preattack_probe.py` → `preattack/preattack_probe_v1_rerun.json`) — 66/72

바뀐 6 행 = **의도한 엄격화** (MXD2R-04 전에는 '같은 뜻 꼴 PASS' 로 적었던 것): `run_tab_separator` · `neigh_tab` · `form_feed_in_code` (탭 · 폼 피드 = 제어 문자) · `front_period_exp_spelling` (`7.82508e-1` ≠ 생성기 `0.782508`) · `friction_same_value_spellings` (`9e-1` ≠ `0.9`) · `nul_in_comment` (주석 안 NUL — C 문자열로 읽으면 줄이 거기서 끝난다).  나머지 66 행은 1 회차와 같다 (`run_comment_upto` · `trailing_spaces` · `bytes_lf` 는 여전히 PASS).

### 4-3. 범위 밖 17 다시 (`../tools/preattack_outside_scope.py` → `preattack/preattack_outside_scope_rerun.json`) — 17/17 세 소비자 FAIL

### 4-4. 생성기 옵션 양성 더 (`tools/positive_extra.py` → `preattack/positive_extra.txt`) — 18/18 PASS × 4 (API 셋 + 바이트)

회전 0 바퀴 (층상 · 균일 + dt/2) · 정착 시간 지정 (0.37 · 1.9 s + dt/4) · rpm 지정 (70 · 72.5 · 앵커 밴드 안) · SE 경화 14 · 28 (2 상) · 반발 0.5 (정착 시간만) · dt/4 2 상 · 시드 2147483647 · 2147483629 · 원자 2 만 · 30 만 (gen1) · 8 바퀴 + 전 정밀도 dump · ρ = 1 · Bo 3 · ρ 0.03 · dt/3 균일 0 바퀴.  rpm 60 은 생성기가 스스로 거부 (Fr 밴드 밖) — 소비자 문제 아님.

## 5. 변이 시험 — 가드를 하나씩 끄면 새 시험이 옳은 이유로 실패하는가

`tools/mutation_check_v3.py` (커밋 scripts 사본에서 가드 하나를 정확한 문자열 치환으로 바꾸고 시험 → 되돌림 · M01–M19 = 1 회차 도구 그대로 import · M20–M54 = MXD2R-04).  **weaken** 29 (자리 값을 덱 자신에서 복사 · 검사 끔 — 반례 시험이 잡아야 함) · **tighten** 6 (M27 · M50–M54 사본 상수 바꿈 — 양성 시험이 잡아야 함).

- 1 회차 (커밋 `49608570a`): M01–M19 **19/19** · M20–M54 **28/35** — 생존 7 = M25 (주석 줄 이음) · M28 (메타 dump 형식) · M30 (명령 개수) · M32 (시드 소수 · 상한) · M33 (정착 step k 배) · M34 (dump 간격 규칙) · M35 (restart 간격 규칙).  원인 = 해시 재결합만 하는 공통 변조 시험으로는 메타가 막는 칸 · 마지막 run 뒤 명령 · ASCII 주석 이음에 닿지 않았다 (가드는 동작 — 사전 공격 4-1 이 같은 사례로 확인).  `preattack/mutation_v3_round1_49608570a_*.json`.
- 후속 (커밋 `52d84d9eb`): 새 사례 8 — 고치기 전 소비자에서 24/24 PASS (결함) 확인 뒤 넣음 (§2).
- 2 회차 (커밋 `52d84d9eb`): **54/54 죽음** (19 + 35) · 변이 없는 판 rc 0 — weaken 29 은 MXD2R-04 반례 시험이 · tighten 6 은 양성 시험 (생성기 출력 · 정상 48 · dpf) 이 잡는다.  `preattack/mutation_v3_round2_52d84d9eb_*.json`.

## 6. 한정

- **뜻이 같아도 표기가 다르면 거부한다 (생성기 꼴 엄격)** — 예: `0.01447070` · `5e3` · `1.037e9` · `0.3` ↔ `0.30` · `9e-1` · `7.82508e-1` · `04` · `+2.373e-07` · 탭 · 폼 피드.  LIGGGHTS 가 같은 값으로 읽어도 거부한다.
- **LIGGGHTS 실행 · Windows · Python 3.8 실행은 확인하지 않았다.**  LIGGGHTS 쪽 읽기 (ASCII 공백만 구분 · 따옴표 안 `#` 는 주석 아님 · `$` 치환 · 줄 = C 문자열 (NUL 에서 끝) · `&` 앞 ASCII 공백만 건너뜀) 는 소스 규약 판독이고 실행으로 확인하지 않았다 — 생성기가 그 글자들을 쓰지 않으므로 무엇으로 읽히든 거부한다.  주석 끝 `&`+NBSP 로 다음 줄을 숨기는 사례는 '우리 파서가 그 줄을 못 본다' 는 것만 확인했고 LIGGGHTS 가 그 줄을 실행한다는 것은 추정이다.
- (첫 판 기록 — **11-03 밤 Q4 로 없앰 · §9**) **예외 (자유 칸 하나) = neighbor skin 값** — 양의 ASCII 수만 받는다 (nan · inf · 0 · 음수 · 빈 · 문자 = 거부).  값과 표기 (`0.0000757`) 는 고정하지 않았다: 기존 시험 `test_actual_command_scope` 가 skin ×1.1 덱의 **단일 덱 PASS** 와 **짝 대조 FAIL** (한쪽 덱만 바꾼 짝) 을 요구한다 (그 시험은 고치지 않았다).  ⚠ 짝 대조는 두 덱의 skin 이 **다를 때만** 잡는다 — 두 덱에 **같이** 바꾼 skin (공통 변조) 은 세 소비자 PASS 다 = 남은 같은 부류 (이웃 목록 갱신 간격 · 성능 쪽 값이라는 판단은 추정 · 실행 확인 안 함).  고정하려면 그 기존 시험을 바꿔야 한다 — ⬜ 1저자 결정 후보.
- **토큰 단위 엄격 · 배치 자유**: 토큰 사이 공백 수 · 빈 줄 · 주석 글 · 명령 줄 앞뒤 ASCII 공백은 고정하지 않는다 (두 파서가 같은 토큰을 읽는 범위 — 4-1 배치 PASS 9).  명령 부분 = 인쇄 가능 ASCII (공백 = 0x20 만) · 따옴표 · `$` 금지 (메타가 선언한 전 정밀도 dump 한 줄만 문자열 그대로) · 이음 = 명령 줄 끝 ` &` 만 · 제어 문자 (C0 · DEL · C1) 는 주석 안에서도 거부.
- **값 묶음의 갈래**: 드럼 기하 (상자 1.15R · 메시 scale 2R · 삽입 영역 0.9R · ±0.45L · 층상 위 블록) · 템플릿 (id · 시드 · 밀도 · 반지름) · 분포 (시드 · 분율) · 영률 · ν · 재료 상수 · 시드 · dump / restart 간격 규칙 · 회전 주기 (= 메타) = **정확한 생성기 문자열**.  CED 값 · 삽입 총수 · run step 수 · dt 값 = 기존 검사 (힘 규칙 허용폭 · 계획수 · 메타) 가 묶고 여기서는 **생성기 표기**만 본다 (예: CED 를 허용폭 안에서 바꾼 같은 표기 꼴의 값은 기존 규칙 그대로).
- **생성기보다 엄격한 곳**: 배플 덱 (`--baffles`) 거부 (D2 메타에 배플 칸이 없다) · 시드 2^31−1 초과 거부 (생성기는 상한 없음 · LIGGGHTS 시드 = C int — 추정).
- **사본**: plan() · deck() 의 식 · 상수를 사본으로 둔다 (생성기를 import 하지 않는다 — 시험이 사본 ↔ 생성기 대조 · 양성 시험이 식 사본을 지킨다 · 변이 M50–M54).  연산 순서까지 같게 옮겼다 — 생성기와 다른 Python 판 (3.12+ 의 `sum()` 보정 합) 에서 끝자리가 갈려 `.6g` 반올림 경계에 걸리면 거짓 거부가 날 수 있다 (확률 극소 · fail-closed · 확인 안 함).
- **기존 사유 우선**: 새 검사는 read_d2 끝 — 이미 다른 규칙이 거부하는 덱은 그 사유가 먼저 나온다 (4-1 의 4 행).
- 원장: MXD2R-04 = claimed_fixed (Codex 재확인 전 · verified 아님).  MXD2-01 · MXD2R-01–03 상태 그대로.

## 7. 재현

```bash
python3 -I -X utf8 -B scripts/test_mixer_d2_consumers.py                         # 28/28 (§9 skin 판 뒤 29/29)
python3 scripts/mixer_deck_readback.py --selftest                                # 24/24
python3 scripts/mixer_deck_diff.py --selftest                                    # 55/55
python3 scripts/mixer_smoke_blind.py --selftest                                  # rc 0
python3 webapp/test_mixer_devlog_page.py                                         # 9/9
python3 -I docs/reviews/codex_mixer_d2_review_20261027/_repro_ours_20261030/tools/run_d2_cli_cases.py \
  "$PWD/scripts" "$PWD/docs/reviews/codex_mixer_d2_review_20261027/d2/evidence/cases" codex_cases_after <OUT>
E=docs/reviews/mxd2r_fix_evidence_20261103
python3 -I -X utf8 -B $E/mxd2r04/tools/preattack_probe_v2.py "$PWD/scripts" <OUT>.json            # 85/85
python3 -I -X utf8 -B $E/tools/preattack_probe.py "$PWD/scripts" <OUT>.json                       # 66/72 (6 = 의도한 엄격화)
python3 -I -X utf8 -B $E/tools/preattack_outside_scope.py "$PWD/scripts" <OUT>.json               # 17/17 FAIL
python3 -I -X utf8 -B $E/mxd2r04/tools/positive_extra.py "$PWD/scripts"                           # bad 0
# 커밋별 · 변이: git archive <커밋> scripts | tar -x -C <ROOT>/<커밋> 뒤
python3 -I $E/tools/per_commit_replay.py <ROOT> <OUT>.json fe103fc01 85e2d66d8 49608570a 52d84d9eb   # 커밋 넷 (§2)
python3 -I $E/mxd2r04/tools/mutation_check_v3.py <ROOT>/<커밋>/scripts <OUT>.json [M0 M1 | M2 M3 | M4 M5]
```

## 8. 파일

`SHA256SUMS` = 이 폴더의 파일 전부 (자신 제외 · 하위 `q4_skin/` 포함 · `sha256sum -c SHA256SUMS` 로 대조).  상위 `../SHA256SUMS` 도 이 폴더를 포함해 다시 만들었다.

## 9. 11-03 밤 범위 넓힘 — neighbor skin 도 생성기 꼴 (1저자 Q4 = 권고대로)

- 근거: 첫 판의 남은 같은 부류 (§0 · §6 — skin 값 = 자유 칸이라 두 덱에 같이 바꾼 skin 을 세 소비자가 받음) · **1저자 11-03 밤 Q4 = 권고대로** (skin 값도 고정 · 기존 시험 기대 바꿈).
- 바뀐 것: `_d2_generator_form` 의 neighbor 줄 기대 = `['neighbor', f6(min(d)·0.5), 'bin']` (deck() 의 `{min(d.values())*0.5:.6g}` 사본 · 같은 연산 · d = 활성 상 지름 = REG_D_UM × 1e-6 × CGF) · 자유 칸 분기 · `<skin>` 사유 문구 삭제 · 결과 설명 칸 · 주석.  **자유 칸 없음.**
- 증거 폴더 `q4_skin/` (before · after · per_commit · preattack) · 도구 `tools/preattack_probe_v3.py` · `tools/mutation_check_v4.py` (v2 · v3 와 그 결과는 첫 판 기록 그대로).

### 9-1. 커밋

| 커밋 | 무엇 |
|---|---|
| `83ad3ba4e` | 시험 먼저 — skin 공통 변조 7 (×1.1 repr · ×1.1 .6g · ×2 · AM 반지름 · 1e-9 · 같은 값 `0.0000757` · `7.570e-05` · 둘은 CLI 셋) · 기존 시험 기대 바꿈 · garbage skin 사유 |
| `b74fc9b75` | 수정 (skin = 생성기 값 · 자유 칸 없앰) |
| (이 절을 넣은 커밋) | 증거 · 원장 MXD2R-04 범위 넓힘 메모 · `/mixer` v2.1 한 줄 · 수정 계획 상태 줄 |

### 9-2. 옛 기대 → 새 기대 (이유 = (가) 원리 — 생성기 자신의 꼴만 · 같은 부류 예외 제거)

| 시험 · 사례 | 옛 기대 (커밋 `42dcdc7f9` 까지) | 새 기대 (커밋 `b74fc9b75` 부터) |
|---|---|---|
| `test_actual_command_scope` — 한쪽 덱만 skin ×1.1 (`8.327000000000001e-05`) · **단일 덱 readback** | **PASS** (skin = 단일 덱 계약 밖 · 짝 대조만 FAIL) | **FAIL** — token 1 `8.327000000000001e-05` (generator `7.57e-05`) (시험이 사유까지 확인) |
| 같은 시험 — 그 덱과 정상 덱의 **짝 대조** (diff) | FAIL | FAIL (그대로) |
| `test_mxd2r04_same_class…` `neighbor_garbage_skin` (`7.57e-05x`) — 사유 | `neighbor skin: ASCII decimal token required …` (자유 칸 수 검사) | token 1 `7.57e-05x` (generator `7.57e-05`) — 거부는 전과 같고 사유 문구만 바뀜 |
| 사전 공격 v2 `skin_nan` · `skin_inf` · `skin_empty` · `skin_zero` · `skin_negative` — 사유 | `neighbor skin` (자유 칸 수 검사) | 생성기 토큰 대조 사유 (v3 · 거부 그대로) |
| 사전 공격 v2 `skin_same_value_spelling` (`0.0000757`) · `skin_value_x1.1` — 두 덱 같이 | **PASS** (자유 칸 기록) | **FAIL** (v3) |

- 시험 주석 = `scripts/test_mixer_d2_consumers.py` `test_actual_command_scope` (같은 이유 · 이 표 가리킴).

### 9-3. 고치기 전 → 뒤 (`../tools/per_commit_replay.py` → `q4_skin/per_commit/per_commit_replay.json` · 바뀐 메서드만 · 나머지 26 은 세 판 모두 ok)

| 시험 메서드 \ 커밋 | `42dcdc7f9` 첫 판 | `83ad3ba4e` 시험 먼저 | `b74fc9b75` 수정 |
|---|---|---|---|
| test_actual_command_scope | ok (옛 기대) | F1 | ok |
| test_mxd2r04_neighbor_skin_generator_form | - | F27 | ok |
| test_mxd2r04_same_class_spelling_identity_order | ok | F3 | ok |
| 합 | 28 OK | 29 FAILED (failures=31) | 29 OK |

- 고치기 전 실패 31 = skin 7 사례 API 21 + CLI 6 (세 소비자가 받음: `'PASS' != 'FAIL'` · rc 0) · 단일 덱 skin ×1.1 PASS 1 (옛 기대의 동작) · garbage skin 사유 3 (거부는 같고 사유 문구만 다름) — `q4_skin/before/tests_on_4e761d674_before_skin_fix.log` (리포 경로 = `<repo>`).
- subTest (커밋 `b74fc9b75` · `q4_skin/after/subtest_counts_02ad3f7b8.json`): skin 34 (7 + API 21 + CLI 6).

### 9-4. 다시 돌린 것 (커밋 `b74fc9b75` 소비자)

| 시험 | 결과 | 로그 |
|---|---|---|
| D2 소비자 (`scripts/test_mixer_d2_consumers.py`) | 29/29 OK (첫 판 28 + skin 1) | `q4_skin/per_commit/replay_02ad3f7b8.log` |
| Codex 독립 정상 48 조합 | 48 PASS | 같은 로그 |
| readback `--selftest` · diff `--selftest` · smoke `--selftest` · `/mixer` 개발 이력 | 24/24 · 55/55 · rc 0 (✓ 31 · ✗ 0) · 9/9 | `q4_skin/after/` |
| Codex 받은 사례 (세 CLI) | rc · 입력 지문 · 첫 줄 · 화면 (경로 가림) 첫 판과 전부 같음 (normal 0/0/0 · 반례 · 음성 대조 1/1/1) | `q4_skin/after/codex_cases_cli/` |
| 생성기 옵션 양성 (`tools/positive_extra.py`) | 18/18 PASS × 4 (rpm 60 = 생성기 스스로 거부) | `q4_skin/preattack/positive_extra.txt` |
| 사전 공격 v3 (`tools/preattack_probe_v3.py`) | **93/93** (v2 85 사례의 skin 행 기대 바꿈 + skin 8 더함: 대문자 E · + 부호 · 앞자리 0 · 전각 숫자 · 탭 · NBSP · 다른 CGF 생성기 덱 PASS · 다른 계획의 skin 값 FAIL) | `q4_skin/preattack/preattack_probe_v3.json` |
| 1 회차 사전 공격 도구 · 범위 밖 17 | 66/72 (첫 판과 같음 · 6 = 의도한 엄격화) · 17/17 세 소비자 FAIL | `q4_skin/preattack/` |
| 변이 v4 (`tools/mutation_check_v4.py` · 커밋 `b74fc9b75` 사본) | **55/55 죽음** · 변이 없는 판 rc 0 — M31 (바꿈) = skin 기대 토큰을 덱 자신에서 복사 → `test_actual_command_scope` · skin 시험 · garbage skin 이 잡음 · M55 (더함 · tighten) = skin 계수 0.5 → 0.6 → 양성 시험이 잡음 | `q4_skin/preattack/mutation_v4_b74fc9b75_*.json` |

- 한정은 §6 그대로 (자유 칸 줄만 없어짐): **뜻이 같아도 표기가 다르면 거부한다 (생성기 꼴 엄격)** · **LIGGGHTS 실행 · Windows · Python 3.8 실행은 확인하지 않았다** (3.8 = 문법 검사만).  skin 이 성능 쪽 값이라는 판단은 고정 근거가 아니다 — 근거는 (가) 원리다.
- 원장: MXD2R-04 범위 넓힘 메모 · claimed_fixed_sha = 이 수정 커밋 · 회귀에 skin 시험 · `test_actual_command_scope` 를 더함 (Codex 재확인 전).

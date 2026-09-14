# R6 라운드 원장 — **내부 자체 리뷰** (Codex 토큰 소진) · 대상 `1049894` · 2026-09-11

> **다음 세션은 이 파일부터 읽는다.** 6차는 외부(Codex) 대신 `/self-review` 로 돌렸다: 네 렌즈 subagent 가
> 1049894 에서 발견을 내고(`reviews/r6_repros/<렌즈>/REPORT.md` + `repro_*.py`), 발견마다 격리 worktree 의
> 적대적 검증 subagent 가 반박을 시도해 재현된 것만 CONFIRMED (`reviews/r6_repros/<렌즈>/VERDICT.md`).
> 렌즈 재현 스크립트 넷은 본인이 1049894 트리에서 다시 돌려 전부 재현을 확인했다 (validator 9/9 · toctou 10/10 ·
> derived 8 FINDING · sig_port 11/11). 닫은 뒤 트리에서는 그 스크립트의 '재현' assertion 이 실패해야 한다.

판정: **CONFIRMED 30 · 부분 5 · 제외 2** (37 건). 전부 RED → 수정 → GREEN 으로 닫았다 —
`tests/test_r6_internal.py` (35 개; V 8 · D 10 · T 8 · P 7 · 매개변수 2). 네 커밋: `509a0cc`(V) · `eb95ac1`(D) ·
`601f8a9`(T) · `a121e2d`(P). 수정 뒤 `python -m pytest tests/ -q` → **122 passed**.

## 렌즈별 통합 발견 (심각도 = 검증자의 독립 판정)

### V · validator 우회 (`reviews/r6_repros/validator/`) — 9 → CONFIRMED 8 · 제외 1

공통 반례: MATLAB rmse 가 Python 과 상대차 1e-3~1e-2 (`MODEL_REL` 의 10⁶ 배) 인데 `%.2g` 로는 같은 문자열.

| ID | 무엇 | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| V6-01 | 헤더가 데이터 행 **뒤**면 행별 검사(R4-04·R5-01)가 안 돌아 complete·0 | 결론이_바뀜 | 닫힘 (코드) — 헤더 앞의 데이터 행 = malformed | `test_i6v_01` |
| V6-02 | `--precision` 옵션이 토큰과 대조되지 않아 선언 없는/해석 불가 파일이 선언된 파일보다 관대 (sig:2 로 17 자리 토큰 → 0) | 결론이_바뀜 (옵션 시) | 닫힘 (코드) — 선언 없으면 옵션 형식으로 재출력 검사 | `test_i6v_02` ×3 |
| V6-03 | 헤더 없는 파일 = 존재한 적 없는 스키마(56a35a8 부터 헤더) 인데 partial → `--allow-partial` 로 0 | 결론이_바뀜 (플래그 시) | 닫힘 (코드) — 헤더 없음 = malformed | `test_i6v_03` |
| V6-04 | 스키마 누락에 하한 없음 — rmse 열 0·앵커 0 이어도 "전부 일치" 0 | 결론이_바뀜 (플래그 시) | 닫힘 (코드) — `OLD_SCHEMA_MIN_COLS` (rmse_pocv·rmse_dvdq) 없으면 invalid | `test_i6v_04` |
| V6-05 | `verify_unit` 이 meta 의 `artifact` 이름을 안 봐 다른 상태 이름으로 복사해도 '일치' | 숫자가_바뀜 (사후 rename) | 닫힘 (코드) | `test_i6v_05` |
| V6-06 | `# printed_format,17` 이 '선언 없음' 으로 흘러 invalid 가 아니었다 | 서술만_바뀜 | 닫힘 (코드) — 이름으로 역할 (R5-02 를 meta 리더에도) | `test_i6v_06` |
| V6-07 | 못 읽는 `--compare` 경로가 traceback rc 1 = "갈림" | 서술만_바뀜 | 닫힘 (코드) — OSError → invalid(2) | `test_i6v_07` |
| V6-08 | `run_id` 열 중복 시 DictReader 마지막 열만 | 사소 | 닫힘 (코드) | `test_i6v_08` |
| V6-09 | `%f` ±0 토큰이 부호 경계에서 거짓 거절 | 사소 | **제외** — rmse = sqrt(mean(r²)) 라 음수·-0 은 양쪽 다 생산 불가 (도달 불가, fail-closed) | — |

~~검증 못 한 전제~~ → **닫힘 (U15, 2026-09-11 사용자 기계 실측)**: R5-01 의 "Python format = MATLAB sprintf" 에서
우리가 못 재던 두 축이 둘 다 일치했다 — 반올림 타이 `sprintf('%.2f',0.125)` = `'0.12'` (half-to-even, Python 과 같다;
half-away 였다면 멀쩡한 `0.12` 산출을 audit 이 invalid 로 거절했을 것), 지수 자릿수 `sprintf('%.17g',1e-5)` =
`'1.0000000000000001e-05'` (2 자리 — Windows 식 `e-005` 가 아니고, 원래 double 로 되돌아온다). 기준선을
`tests/test_r6_internal.py::test_i6u_15_*` 에 `MATLAB_SPRINTF` 로 고정했다 (`token_format` 을 바꾸거나 지수 자릿수가
갈리면 걸린다). 남는 한계: 두 표본이고 MATLAB 판·플랫폼 하나다 — 다른 기계의 산출을 댈 때는 다시 재는 편이 맞다.

### D · 파생 보고서 · 공정성 (`reviews/r6_repros/derived/`) — 10 → CONFIRMED 8 · 부분 2

| ID | 무엇 | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| DF-01 | §3-4 "두 독립 방법이 수렴" — 힌트 격자(pad=폭/2·21 점)의 grid[5]·grid[15] 가 제약 최적화 min·max 그 자체 → LLI '정확히 일치' 는 같은 격자점 | 서술만_바뀜(상) — 폭 1.0832·`is_lower_bound` 불변 | 닫힘 (문서) — §3-4·§7-3 "끝점 재확인, 독립 수렴 아님" | `test_i6d_01` (artifact 로 grid 재구성) |
| DF-02 | HANDOFF §5·INTRO §6-2 에 §0-2 철회 결론 7 곳 잔존 | 결론이_바뀜 (그 문서 독자) | 닫힘 (문서) | `test_i6d_02` |
| DF-03 | "raw 로 5~10 배" — 어느 통계량도 아님 (max/max 10.52 · min/min 9.66 · med 10.04 · 상태별 쌍 5.1~18.3) | 부분 → 서술만_바뀜 | 닫힘 (문서) — "max/max 10.5 배" 로 통일 | `test_i6d_03` |
| DF-04 | "86 passed 기대" 잔존 (Codex R5 §1 이 짚은 종류) | 숫자가_바뀜 | 닫힘 — 수집 수와 같아야 하는 테스트 | `test_i6d_04` |
| DF-05 | U13 을 "192 값의 조건" 에 묶음 — 192 값은 raw rmse 라 scale 을 소비하지 않는다 | 서술만_바뀜 | 닫힘 (문서) — 대상은 목적함수 build; R5-09 의 build 범위 문장은 유지 | `test_i6d_05` |
| DF-06 | §4-0 6·17·"전부 w=1" 은 상대 1e-9 문턱에서만 (부호만 10·22·0) | 서술만_바뀜 | 닫힘 (문서) | `test_i6d_06` |
| DF-07 | §1-10 에 탐색 하한 한정어 없음 | 서술만_바뀜 | 닫힘 (문서) | `test_i6d_07` |
| DF-08 | §4-1 2.11 → 원값 폭 2.1016 | 사소 | 닫힘 (문서) | `test_i6d_08` |
| DF-09 | §3-3 best 행 인용이 v1 (비트 일치는 v2) | 부분 → 사소 | 닫힘 (문서) | `test_i6d_09` |
| DF-10 | INTRO §6-3 "n=1 … 산수다" 는 §7-3 이 철회 | 사소 | 닫힘 (문서) | `test_i6d_10` |

공정성 검사에서 통과한 것: seed 는 U13 18 줄 전부 0 이고 eps_rel 최대 1.7e-15 vs 문턱 1e-9 (여유 5.8e5 배) 라 seed 는
verdict 에 무관; 1e-9 의 근거는 `model.py` 의 "MODEL_REL 과 같은 크기" 뿐 (문서는 seed-독립을 주장하지 않는다);
MATLAB(30 sqp) vs 우리(24 L-BFGS-B) 예산 차이는 §1-4 가 밝히고 §1-9 는 "관측 상한" 만 말한다.

### T · 순서/TOCTOU (`reviews/r6_repros/toctou/`) — 9 → CONFIRMED 8 · 부분 1

| ID | 무엇 | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| F01 | degeneracy `.part` 가 고정 이름 + producer 의 stdout fd — 느린 시도가 게시된 inode 를 잠금 밖에서 덮음 (JSON=B, meta=A, 두 wrapper "통과"); R5-04 "마지막 온전한 묶음" 이 이 경로에서 거짓 | **결론이_바뀜** | 닫힘 (코드) — `cmd_degeneracy --out` + `atomic_write_json`(잠금 안 교체), shell 은 matrix 와 같은 형태 | `test_i6t_01` (실제 두 process) |
| F02 | `ne_shape._write_csv` 비원자·잠금·run_id·sha256 없음 → CSV=B·meta=A, 검출 불가 | 서술만_바뀜 | 닫힘 (코드) — 같은 게시 규약, 행 `run_id` | `test_i6t_02` |
| F03 | `fitted_pair_info` 파싱↔해시 두 번 읽기 | 사소 (창 sub-ms) | 닫힘 (코드) — bytes 한 번 | `test_i6t_03` |
| F04 | git 상태가 계산 뒤 한 번 샘플 | 서술만_바뀜 | 닫힘 (코드) — `git_*_at_start`·`started_utc`·`git_state_changed_during_run` | `test_i6t_04` |
| F05a | `--verify-unit` 이 이 시도의 id 를 안 받음 | 사소 | 닫힘 (코드) — `verify_unit(path, rid)` | `test_i6t_05a` |
| F05b | 실패 이유 `>/dev/null` | 사소 | 닫힘 (shell) — `verify_unit_or_say` | `test_i6t_05b` |
| F06 | `.lock`·`.part` 가 ignore 밖 | 사소 | 닫힘 (`.gitignore`) | `test_i6t_06` |
| F07 | reader 가 묶음을 안 봄 (Codex R5-04 reader 절 미구현) | 서술만_바뀜 | 닫힘 (코드) — `compare_states` 경고+제외, `fitted_pair_info` RuntimeError | `test_i6t_07` |
| F08 | run_id 는 공개 열 — 복사한 producer 는 모든 검사 통과 | 부분 → 사소 | **신뢰 경계** — 문서의 위협 모델(각자 uuid 의 "다른 시도") 밖; 소유 증명은 주장한 적 없음. 원할 때: producer 가 자기 bytes 의 sha256 을 stdout 에 내고 write_meta 가 그것과 대조 | — |

### P · sig-완전성 · 이식성 (`reviews/r6_repros/sig_port/`) — 11 → CONFIRMED 8 · 부분 3

| ID | 무엇 | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| F1 | `root=` 라벨이 공백·같은 basename·`.` 에서 식별자가 아님 | 사소 | 닫힘 (코드) — URL 인코딩 + `inputs=<digest>` | `test_i6p_01` |
| F2 | `test_u13` 이 네 루트를 증거 못 함 (위조 사본 통과) | 부분 → 사소 | **한계로 기록** — §1-13 은 이미 "루트는 보고 순서" 라 적음; identity 붙은 다음 실측(U14)부터 루트 집합을 센다 | — |
| F3 | 라이브러리 버전 미기록 (scipy 1.11↔1.17: savgol ULP → 최적점 nit 25↔27, a_NE 1.5e-5) | 숫자가_바뀜 (끝자리) | 닫힘 (코드) — `env_signature` 를 meta·JSON·eval 헤더에 | `test_i6p_03` |
| F4 | 풀셀 워크북(이름순 첫 xlsx) identity 미기록 | 서술만_바뀜 (stderr 경고는 있음) | 닫힘 (코드) — `consumed_inputs`·`inputs_sha` 를 산출마다 | `test_i6p_04` |
| F5 | `--profile-scale`·`--samples/--grid` 가 산출에 없음 | 부분 → 사소 | 닫힘 (코드) — 행 `profile_scale`, JSON `n_grid`·`n_samples` ((c) starts 는 meta 에, (d) seed 는 `--seed 0` 과 쌍 — 반증) | `test_i6p_05` |
| F6 | `eol=lf` 비소급 — autocrlf 사본을 pull 로 올리면 안 바뀐 `run_all.sh` 가 CRLF | 서술만_바뀜 | 닫힘 (요청문 §0 "fresh clone"; `add --renormalize` 는 실측 무효) | — |
| F7 | `git_provenance` 가 cwd 기준 | 사소 | 닫힘 (코드) — 기본 base = 스크립트의 저장소 | `test_i6p_07` |
| F8 | `flock` 명령 부재 시 degeneracy 고아·오진 | 사소 | 닫힘 — F01 수정으로 shell 의 `flock` 사용이 사라짐 | (`test_i6t_01`) |
| F9 | 비-UTF-8 기본에서 check_artifact·CLI 크래시 | 부분 → 사소 | 닫힘 (코드) — `encoding="utf-8"`, stdout backslashreplace | `test_i6p_09` |
| F10 | ENOLCK 면 계산 행 소실 | 사소 | 닫힘 (코드) — `.part` 보존 + 경로를 예외에 | `test_i6p_10` |
| F11 | "86 passed"·`.lock` ignore | 사소 | 닫힘 — DF-04·F06 | — |

## 스키마 변경 (다음 실측 U14 에서 처음 채워진다)

- degeneracy: `--out` 로 게시 (stdout 은 로그); JSON 에 `n_grid`·`n_samples`·`env`·`consumed_inputs`·`ref_consumed_inputs`·`inputs_sha`.
- matrix 행 `inputs_sha`; profile 행 `profile_scale`·`inputs_sha`; ne_shape 행 `run_id`, meta `run_id`·`sha256`.
- meta: `env`, `git_commit_at_start`·`git_dirty_at_start`·`git_modified_code_at_start`·`git_state_changed_during_run`·`started_utc`.
- eval 헤더: `# env,…`·`# inputs,sha=… full_cell=<이름>:<sha12> …`; `# scale_audit,root=<URL 인코딩> … inputs=<digest>; …`.
- 기존 `out/` 은 전부 pre-R5 meta 라 새 검사의 대상이 아니다 (reader 는 옛 meta 를 전과 같이 읽는다).

## U14 실행이 드러낸 것 (2026-09-12, 사용자 기계 네 상태 재실행 — `STARTS=24`, 12 산출, 전부 통과)

재실행 자체는 깨끗했다 (배관 확인 3/3 · 본 실행 12/12 · 새 스키마 전부 갖춤). 그 과정이 두 건을 드러냈다.

| ID | 무엇 | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| U14-01 | `atomic_write_csv` 가 `csv` 기본 lineterminator 라 **CRLF** 를 쓰는데 `.gitattributes` 가 csv 를 안 덮어 git 이 LF 로 정규화해 저장한다 → 디스크 bytes ≠ 커밋 bytes → **fresh clone 에서 meta 의 sha256 이 안 맞고**, R6 내부 F07 이 넣은 reader 검사가 그 상태를 §1-10 표에서 뺀다. 저장소를 새로 받은 리뷰어에게는 상태가 사라진 표가 간다 | **결론이_바뀜** (fresh clone 한정) | 닫힘 (코드) — writer 는 LF, `.gitattributes` 에 `*.csv`·`*.json text eol=lf`, `verify_unit` 이 "줄끝만 다르다" 를 짚는다. 이미 게시된 것은 `check_u14.py --renormalize` (파싱한 셀이 같을 때만 다시 서명, meta 에 기록) | `test_i6w_01`·`02`·`04` |
| U14-02 | `check_u14.py` 가 정본을 **파일 이름**으로만 골라 `degeneracy_300_0009_Li.json`(v1, 힌트 격자 이전)과 댔다 — 정본은 `_v2` 다. 또 정본에 없던 필드(스키마 추가분)를 `None → [값]` 으로 전부 diff 에 세었다. 둘이 겹쳐 "다른 숫자 618" 이 나왔는데 대부분 거짓 경보다 | 숫자가_바뀜 (도구) | 닫힘 (코드) — `baseline_for` 가 가장 높은 판을 고르고(`compare_states._keep_latest` 와 같은 규칙), 새 필드는 "정본에 없던 필드" 로 따로 센다 | `test_i6w_03` |

곁: `scale_audit_line` docstring 의 `\S` 가 SyntaxWarning 을 냈다 (raw string 으로).

**아직 판정 안 난 것**: U14 재실행의 숫자가 정본과 같은가. 위 두 거짓 경보를 걷어내야 답이 나온다 —
사용자가 `4de17ee` 를 push 하면 고친 `check_u14.py` 로 `git show` 기반 대조를 돌려 닫는다.

## 순서 (진행 기록)

1. ~~탐색 4 렌즈~~ → 2. ~~선별·본인 재현~~ → 3. ~~적대적 검증 4~~ → 4. ~~V·D·T·P 닫기~~ → 5. 원장·§0-2·요청문 (이 커밋) →
6. Codex 토큰 복귀 시 `R6_REQUEST.md` 송부 → 7. U14 (사용자 기계 `run_states.sh` 재실행으로 새 스키마 산출) → 8. 새 모델 요구서.

## 이력 정정 (2026-09-12)

`4762dcb` 의 커밋 메시지는 "옛 blob 둘(`out/matrix_300_0009.csv`·`out/profile_gamma_300_0009_Li.csv`)은 이 커밋에서
건드리지 않는다" 고 적었으나 **실제로는 그 둘의 CRLF→LF 변환이 같이 들어갔다** (그 전에 시험 삼아 돌린
`git add --renormalize .` 가 남긴 스테이징). 되돌리려 했으나 `.gitattributes` 의 `*.csv text eol=lf` 가 켜진 뒤로는
git 이 add 때마다 LF 로 정규화하므로 CRLF blob 으로 되돌릴 수 없다 — 그것이 그 규칙의 목적이다. 그래서 기록을
사실에 맞춘다: **그 두 파일은 `4762dcb` 에서 LF 로 정규화됐다.**

깨진 것은 없다 — 두 파일 모두 파싱한 셀이 완전히 같고(줄끝만 바뀌었다), 서명(`sha256`)이 없는 R5 이전 산출이라
다시 서명할 대상도 아니었다. 다만 **사용자 트리에서 U14 커밋을 rebase 할 때 이 두 파일이 충돌한다** (그쪽 patch 는
CRLF 판을 base 로 만들어졌다). 해결은 U14 판을 그대로 취하는 것이다 — 재실행 산출이 정본이다.

## U14-03 · U14-04 (2026-09-12, 사용자 기계 rebase 중 드러남)

| ID | 무엇 | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| U14-03 | R6 내부 F02 가 `ne_shape` 행에 `run_id` 를 붙였는데 소비 helper `_ne_shape_csv` 는 모든 열을 `float()` 로 읽어 세 테스트가 `ValueError: could not convert string to float` 로 깨졌다. **이 트리에서 안 깨진 이유**가 요점이다 — 커밋된 `out/ne_shape_GITT_Li.csv` 가 아직 옛 스키마라 fixture 가 진실을 가렸다 (이 저장소에서 다섯 번째로 실측된 패턴) | 숫자가_바뀜 (테스트가 새 산출을 못 읽는다) | 닫힘 (코드) — `NE_SHAPE_TEXT_COLS` 에 `run_id`; helper 를 경로 인자로 열어 **새 스키마 파일**로 직접 건다 (커밋된 산출이 재생성되기 전에도 회귀가 잡히게) | `test_i6w_07` |
| U14-04 | rebase 충돌이 해결되지 않은 채 `out/matrix_300_0009.csv` 에 `<<<<<<< HEAD` 가 박혔고, 그것이 여덟 개의 `KeyError: 'half_cell'`·`'w_dqdv'`·`'obj_ratio_to_best'` 로 나왔다 — 원인에서 먼 오류라 진단이 늦는다 | 사소 (진단) | 닫힘 (테스트) — 산출을 훑어 충돌 표식을 바로 말한다; 탐지기 자체 증명 포함 | `test_i6w_08` |

**교훈 (스키마를 바꿀 때)**: 산출 스키마에 열을 더하면 그것을 **읽는 쪽**을 같이 고쳐야 하는데, 커밋된 산출이
옛 판이면 테스트가 통과해 버려 그 사실이 안 보인다. R6 내부 F02·F04·F05 가 더한 열(`run_id`·`inputs_sha`·
`profile_scale`)의 소비자를 전수로 확인한 것은 아니다 — U14 산출이 들어오면 전체 테스트가 그 감사다.

## U14 판정 (2026-09-12) — **결론 숫자는 전부 재현됐다. 움직인 것은 γ 프로파일의 개별 행이다**

사용자 기계 네 상태 재실행(`STARTS=24`, 12 산출) 을 커밋 `bfc4623^` 의 정본과 셀 단위로 댔다
(`python3 scripts/check_u14.py --new out --old-rev bfc4623^`; 환경은 python 3.12.3 · numpy 2.5.3 · scipy 1.18.1 ·
pandas 3.0.5 · WSL2 — 정본을 만든 조합은 meta 에 없어 모른다, 그것이 F3 의 요지였다).

| 무엇 | 최대 상대차 | 뜻 |
|---|---|---|
| `matrix_100·200·300_0147.csv` (전 셀) | **0.00e+00** | B축 산출은 비트 단위로 같다 |
| `matrix_300_0009.csv` ↔ 옛 `_v2` | **0.00e+00** | 재실행이 v2 를 그대로 재현 (U14-05 참조) |
| `degeneracy_*` 의 세 mode `span` | **0.00e+00** | §1-10 A축 폭 — 결론 숫자가 그대로다 |
| `profile_gamma_*.csv` 개별 행 | LAM_NE 2.8e-2 · b_NE 3.6e-1 · rmse_pocv 2.1e-2 | 국소 최적점이 갈린 행이 있다 |
| §5-1 문턱 표 (8·10·11·12 mV) | n 6/10/12/13 **동일**, 폭 13.5860 → 13.5859, 최악 비 동일 | 문서 숫자(소수 3자리)는 그대로 |

**읽는 법** (Codex R6-06 정정판 · R7 §5 로 다시 좁힘): degeneracy·matrix 는 5변수 multistart(24 시작 + 힌트) 이고,
`profile` 은 γ 를 고정한 4변수 L-BFGS-B 를 **γ당 25 회**(`best[:4]` + 무작위 24, `cmd_profile`; 산출 `n_tried` 25)
돈다. ~~적은 시작으로 푸는 구조라~~ 는 SLSQP 등식 프로파일(`_profile_mode`, 3 시작)과 섞은 오기였다.

여기까지가 사실이고, **원인은 여기서 멈춘다**: 두 산출의 γ profile 은 둘 다 25 회 시작을 썼다. 같은 예산 아래 일부
행이 달랐고 **원인은 U16 미확정**이다 — "25 회였으니 예산은 충분했다" 도, "차이는 ULP 때문" 도 이 관측만으로는
말할 수 없다 (F3 는 scipy 판에서 `savgol_filter` 가 ULP 로 갈리는 것을 보인 **가설의 근거**지 이 차이의 확인된
원인이 아니다). 보존된 두 실행에서 본문 인쇄 정밀도의 해당 집계는 유지됐다: §5-1 이 세는 n 과 최악 비는 그대로고
폭은 넷째 자리에서만 움직인다. **어떤 결론도 뒤집히지 않았다.**

**남는 한계**: 정본을 만든 라이브러리 조합을 모른다 (그 산출에는 `env` 가 없다). 그래서 "이 차이가 scipy 판 때문" 은
**가설**이고, 닫으려면 같은 기계에서 옛 조합으로 한 번 더 돌려야 한다 (U16 후보). 지금부터의 산출에는 `env` 가 붙는다.

| ID | 무엇 | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| U14-05 | U14 재실행이 `out/matrix_300_0009.csv` 를 덮었는데 그 자리에 있던 것이 §4-0 이 "고치기 **전**" 으로 인용하는 v1 이었다 (재실행은 수정된 코드라 `_v2` 를 재현 — 새 파일 ↔ 옛 v1 최대 상대차 4.17e-01). 파이프라인이 덮어쓰는 이름에 역사 자료가 놓여 있었다 | 숫자가_바뀜 (§4-0 의 근거가 사라졌다) | 닫힘 — `out/archive/matrix_300_0009_premultistart.csv` 로 보존(+`out/archive/README.md`), §4-0·§3-3 인용과 테스트 둘을 그쪽으로. archive 는 `out/*.csv` 비재귀 glob 에 안 걸려 소비자와 섞이지 않는다 | `test_i6d_06`·`test_i6d_09` |

---

## Codex R6 (2026-09-12, 대상 `d431404`) — **NO-GO (P1 3 · P2 3) → 여섯 건 전부 재현·닫음** (`reviews/R6_CODEX.md`)

토큰이 돌아와 6차 요청문(`R6_REQUEST.md`)을 Codex 에 보냈다. 판정은 NO-GO — "출처 결속 세 조건을 먼저 닫는다".
절차는 그대로: 원문 보존 → 우리 트리에서 재현(RED) → 수정 → GREEN → 변이 감사 → 원장. 회귀는
`tests/test_r6_internal.py` **C 절** (`test_c6_01`~`06` + `test_c6_q3`, 전부 수정 전 트리에서 RED 확인).

| ID | 무엇 (Codex 반례) | 심각도 | 상태 | 테스트 |
|---|---|---|---|---|
| **R6-01** (P1) | 독자가 A 의 bytes 를 읽은 뒤 경로를 다시 검사 → 그 사이 게시된 정상 시도 B 가 검사를 통과해 **A 데이터에 B meta**; matrix 는 반대 순서로 A/A 검증 뒤 B 행 소비 | 결론이_바뀜 (동시 게시 시) | 닫힘 (코드) — `provenance.read_unit(path, rid) → (ok, why, data, meta)` 가 bytes 와 meta 를 **한 번씩** 읽어 서로 대조한 snapshot 을 돌려주고, `compare_states.load_degeneracy`·`load_matrix_axis`·`ne_shape.fitted_pair_info` 는 **그 data 만** 파싱한다. `verify_unit` 은 `read_unit(...)[:2]` | `test_c6_01` (훅으로 어느 읽기 경계에 게시가 끼든 A/A · B/B · 미완만) |
| **R6-02** (P1) | `run_id` 가 있는 현행 산출에 meta 가 없거나 옛 meta 면 `verify_unit` 이 None(옛 산출 호환) → 미완 묶음이 표에 실린다 | 결론이_바뀜 (중단된 게시) | 닫힘 (코드) — `is_modern_bytes` 로 산출 안의 `run_id` 를 보고, 현행이면 meta 없음/옛 meta = **False (미완)**; 옛 산출(run_id 없음)만 None | `test_c6_02` |
| **R6-03** (P1) | `build` 가 풀셀 워크북을 파싱한 **뒤** 경로를 다시 열어 해시 → 그 사이 재-export 된 B 를 서명 (A 로 계산, B 서명). `ne_shape.main` 은 반쪽전지를 세 번 열었다 (HalfCell · raw_ne_capacity · identity) | 결론이_바뀜 (입력 재-export 시) | 닫힘 (코드) — `data.read_input(path) → InputBytes` (bytes · sha256 · `.stream()` · `.identity()`); `load_full_cell`·`load_literature`·`HalfCell`·`raw_ne_capacity` 가 **같은 bytes** 로 파싱하고 `consumed_inputs`·`inputs_sha` 는 그 bytes 의 해시 | `test_c6_03` (워크북 1·2·3 번째 open · 반쪽전지 2·3 번째 open 직전 재-export — A값/A서명 · B값/B서명만 허용) |
| **R6-04** (P2) | "가장 높은 `_vN`" 규칙 때문에 U14 가 정본을 다시 만든 뒤에도 독자는 옛 `_v2`(meta 없음)를 골랐다 — 새 서명·환경 필드가 소비 경로에 안 실렸다 | 숫자가_바뀜 (같은 값이었지만 검증 경로가 빠짐) | 닫힘 (코드+자료) — 정본은 **unversioned 이름 하나**. `_vN` 이 out/ 에 남으면 시끄럽게 건너뛴다 (`_canon_files`, ne_shape 도 같은 경고). `degeneracy_300_0009_Li_v2.json`·`matrix_300_0009_v2.csv` 는 `out/archive/` 로 (README 행 추가). FINDINGS §1-8·§3-3·§3-4·§4-1 · README · HANDOFF · matlab/README 의 `_v2` 인용을 정본 이름으로 | `test_c6_04` · `test_compare_states_reads_the_unversioned_canon_*` (옛 "최신 판" 테스트를 규칙째 뒤집음) · `test_r5_05_*` (같은 이름 재게시로) |
| **R6-05** (P2) | `git_provenance` 가 `-z` 레코드 경로를 `" -> "` 로 쪼개고 strip → `out/a -> b.csv` 가 `b.csv`(코드) 로 분류 | 서술만_바뀜 | 닫힘 (코드) — `rel = ln[3:]` 그대로 | `test_c6_05` |
| **R6-06** (P2) | U14 판정문 "γ profile 은 적은 시작으로 풀어서 움직였다" — 실제 경로는 `best[:4]` + 무작위 24 = **γ당 25 회** 4변수 L-BFGS-B (`n_tried` 25). SLSQP 등식 프로파일(3 시작)과 섞은 오기 | 서술만_바뀜 | 닫힘 (문서) — 위 "U14 판정" 읽는 법 정정판 · `R6_REQUEST.md` §3 취소선 · FINDINGS §0-2 행 | `test_c6_06` (코드·산출 `n_tried`·문서 셋 동시에) |
| Q3 | "충돌이면 항상 partial" 문구 ≠ 코드 — `.125`/`.125` 는 conflict 지만 complete, `.125`/`.126` 은 partial | 서술만_바뀜 | 닫힘 (문서) — §1-8: "옵션이 선언은 못 흡수하는 차이를 흡수한 셀이 있을 때만 partial(3)" | `test_c6_q3` (코드 두 경우 + 문구) |

**변이 감사** (`reviews/r6_repros/codex_r6_mutation_audit.py`, 출력 `…_audit.txt`): 수정 여덟 조각을 하나씩
되돌리면 각각의 테스트가 실패한다 — **8/8 CAUGHT · 0 MISSED**, 되돌린 뒤 7 passed. 이 감사가 없었으면 c6_03 의
ne_shape 절반은 3 번째 open 만 걸어 "파싱 뒤 다시 열어 해시" 류(2 번 open)를 놓쳤을 것이다 → 2·3 번째를 다 건다.

**규약이 바뀐 것 (소비자 전부)**
- 독자: `read_unit` 의 (data, meta) snapshot 만 소비. 경로 재검사·재읽기 금지. False 면 표에서 빼고 이유를 찍는다.
- 산출 판정: `run_id` 있음 + meta 없음/옛 meta = **미완**. 옛 산출(run_id 없음)만 호환 경로 (None).
- 입력: `read_input` 의 bytes 로 파싱과 해시를 같이. `HalfCell`·`raw_ne_capacity` 는 스트림을 받는다.
- 정본 이름: unversioned 하나. `_vN` 은 `out/archive/` 의 역사 자료 (`check_u14.baseline_for` 의 "가장 높은 판" 은
  **옛 리비전**을 읽을 때만 뜻이 있다 — docstring 에 못 박음).

**Codex 의 질문에 대한 답 (R7 요청문 §6 에 다시 싣는다)**
- Q1 동시 실행: R6-01·02 를 닫았으니 "독자는 검증한 snapshot 만 소비" 가 성립한다. 남는 것은 Codex 가 짚은 대로
  crash 뒤 "마지막 온전한 묶음 유지" 인데, 지금 게시는 `.part` → rename 두 단계라 data 는 갔고 meta 가 안 간 순간이
  있다 — 그 순간은 이제 **미완(False)** 으로 읽히지 옛 묶음으로 오인되지 않는다. 시도별 불변 묶음 + 단일 선택 지점은
  안 만들었다 (신뢰 경계 F01b 로 등록).
- Q2 producer 의 id 복사: GO 전제로 삼지 않는다 (Codex 동의). F08 그대로.
- Q3: 문서를 실제 의미로 고쳤다 (위 표).
- Q4 1.0832 인용: 탐색 하한으로만. endpoint 의 parameter·J·limit·제약 잔차 보존은 안 했다 — U17 로 등록.
- Q5 §5·§5-1 인용: 인쇄 정밀도의 기술 집계로 가능. "multistart 가 없어서" 는 쓰지 않는다 (R6-06). U16 유지.
- Q6 다섯 관측: Codex 의 한정어 다섯 줄을 요구서 초안의 관측 열 규격으로 받는다 (R7 §5).

**부수 정정**: 2026-09-10 의 `test_compare_states_reads_the_latest_version` 은 "가장 높은 `_vN` 을 읽어라" 였고 그
규칙이 R6-04 의 원인이다 — 삭제하지 않고 **규칙을 뒤집어** 같은 이름 자리에 둔다 (역사를 docstring 에 남김).
`test_quoted_spreads_*`·`test_dump_table_*` 는 `_v2` 가 없으면 조용히 `return` 하던 것을 **assert** 로 바꿨다 —
정본을 옮기자 두 테스트가 통째로 비었을 것이다 (fixture 가 진실을 가리는 통로).

### Codex 재현 패키지 도착 — **우리 트리에서 다시 돌렸다** (2026-09-12 늦게, `reviews/r6_repros/codex/`)

위 여섯 건은 처음에 **리뷰 본문만** 보고 닫았다. 그 뒤 사용자가 Codex 의 재현 패키지(10 파일, `HARNESS_R6_D431404_*`)
를 줬다 — 절차대로라면 **먼저** 있었어야 할 것이다. 받은 그대로 보존하고(`sha256sum -c` 10/10 OK) 두 트리에서 돌렸다.

**① 대상 커밋 `d431404` 에서 — 일곱 probe 전부 재현** (`replay_ours_d431404.json`, 격리 worktree)

| probe | 관측 |
|---|---|
| `snapshot_metadata_mix` (R6-01) | 독자가 **A 데이터 + B meta** 를 소비 (`loaded_data_run_id` attempt-A · `loaded_meta_run_id` attempt-B), 디스크는 B/B 로 온전 |
| `matrix_after_verification` (R6-01) | A 를 검증(폭 3.0)한 뒤 **B 의 폭 79.0** 을 표에 넣음, 그 순간 디스크 묶음은 false |
| `missing_modern_metadata` (R6-02) | meta 가 한 번도 없던 현행 산출이 `None`(옛 산출)로 통과해 degeneracy·matrix·`fitted_pair` 전부 소비 |
| `old_version_selected` (R6-04) | 독자가 `_v2`(meta 없음) 를 골랐고 그 옆의 서명된 정본은 `True` 인데 안 쓰임 |
| `shape_and_matrix` (R6-03) | 반쪽전지를 늦게 해시 — 값은 A(PE 변화 0 mV), 서명은 B, 그리고 B 의 정상 실행과 meta 가 **동일** |
| `fullcell_build_signature` (R6-03) | `raced.voltage == original.voltage` 인데 `inputs_sha` 는 B 와 같다 (rmse_pocv 8 점 차 > 1e-6) |
| `role_checks` (R6-05) | `out/a -> b.csv` 가 `git_modified_code` 로, `git_dirty` true |

Codex 가 첨부한 `harness_r6_final_replay_results.json` 과 같은 관측이다 — **보고서를 믿고 닫은 것이 아니라 우리
기계에서 같은 반례를 봤다**는 기록이 이제 있다.

**② 우리 HEAD `4396a54` 에서 — 원본 probe 는 전부 '안 재현'** (`replay_ours_4396a54.json`). 다만 **그중 넷은 닫혀서가
아니라 hook 이 빗나가서**다: `Path.read_text` 가 아니라 `read_bytes` 를 쓰고(01a), `_unit_ok` 가 사라졌고(01b),
mock 이 새 `identity=` 를 못 받고(03b), `_v2` 가 archive 로 갔다(inference). **hook 이 안 걸린 것을 닫힘으로 읽으면
안 된다** — 그래서 세 번째 판을 만들었다.

**③ 적응판 — hook 만 현행 코드에 맞추고 판정을 뒤집어서** (`replay_codex_r6_adapted.py`, 결과
`replay_adapted_4396a54.json`). probe 의 fixture·경쟁 순서·입력은 원본 그대로다.

| 적응 probe | HEAD 에서의 실측 |
|---|---|
| R6-01a (두 순서) | 검증 **중** 게시 → 묶음 불일치로 표에서 뺌 · 검증 **후** 게시 → A/A 그대로 소비 (값 1.0) |
| R6-01b | A 를 검증한 폭 3.0 을 그대로 소비 (B 의 79.0 아님), 디스크는 false |
| R6-02 | 현행 산출 + meta 없음 = `False`(미완), 두 독자 모두 제외, `ne_shape` 는 RuntimeError. **옛 산출(run_id 없음)은 그대로 읽힌다** (대조군) |
| R6-03a | 값이 A(PE 0 mV)면 서명도 A (`recorded_sha_is_A`), 디스크의 B 해시와 다름 |
| R6-03b | `raced.voltage == original.voltage` 이고 `inputs_sha` 도 **A 와 같다** (B 와 다름) |
| R6-04 | Codex `inference` 스크립트를 정본 이름으로 한 줄 적응해 완주 (rc 0) — `DF01_AND_DERIVED_CLOSURE` · `U14_SECTION_5_1_THRESHOLDS` · `U14_12_ARTIFACT_NUMERIC_COMPARISON` · `U14_PROFILE_BUDGET_FACT` · `CURRENT_SECTION_5_PRINTED_TABLE` 전부 통과 |

**④ 적응판이 실제로 무언가를 재는가** (`mutation_adapted.py`, 출력 `mutation_adapted.txt`): 수정을 하나씩 되돌리면
해당 적응 probe 가 **열림** 으로 돌아와야 한다 → **5/5 CAUGHT · MISSED 0**, 되돌린 뒤 전부 닫힘.

이 감사가 두 번 고쳐 준 것 (처음엔 둘 다 MISSED 였다):
- **R6-01a 는 한 순서만 재고 있었다.** 검증 *중* 게시만 걸면 검사가 먼저 깨져 어차피 제외되므로, "검증 뒤 다시
  읽는다" 를 못 잰다. 검증이 끝난 **뒤** 게시하는 순서를 더해서야 그 변이가 잡혔다.
- **R6-03b 의 변이를 내가 엉뚱한 자리에 넣고 있었다.** 해시를 `load_full_cell` 안으로 옮기는 변이는 mock 이
  로더를 감싸는 순서 때문에 아무 일도 안 일으킨다. 원래 결함 자리(`build` 가 로더 뒤에 경로로 해시)로 바꿔야 잡힌다.

**남긴 한계**: 원본 probe 는 d431404 전용(커밋 SHA·옛 API 에 묶여 있다)이라 HEAD 에서는 적응판이 정본이다. 적응은
hook 지점·mock 서명·`_vN` 이름 세 가지뿐이고 diff 는 `replay_codex_r6_adapted.py` 머리말에 적었다.

---

## Codex R7 (2026-09-12, 대상 `521be85`) — **NO-GO (P1 3 · P2 3)**, 여섯 건 전부 재현·닫음

이번에는 **재현 패키지가 리뷰와 같이 왔다** (`reviews/r7_repros/codex/`, sha256 10/10 OK) — R6 때 뒤집혔던 순서가
제자리로 왔다. 그래서 절차가 그대로 돌았다: 원문 보존 → 패키지 probe 를 **우리 HEAD 에서 실행**(전부 재현) →
RED 회귀(`tests/test_r7_codex.py`) → 수정 → GREEN → 변이 감사 → 원장.

Codex 의 판정 요지: **R6 의 반례는 닫혔다. 그러나 개별 snapshot 을 올바르게 읽은 *다음 단계* 가 안 이어진다** —
집계 결론(R7-01) · 잡음 진단의 입력 결속(R7-02) · 기준 입력의 출처(R7-03).

### 우리 HEAD `521be85` 에서의 재현 (수정 전)

| probe | 관측 |
|---|---|
| `aggregate_incomplete_counterexample` (R7-01) | 두 상태 정상 → "LLI 가 항상 가장 좁은가: **아니오**" rc 0. 반례 상태(200)가 data 만 게시된 미완이 되면 독자는 정확히 거부하는데 집계는 **"예" rc 0**. meta 를 채우면 다시 "아니오". **빈 디렉터리도 "예" rc 0** |
| `noise_reopen` (R7-02) | A 적합 뒤 정상 재-export B → misfit 0.02887622(A) ÷ σ 0.01819577(B) = **1.59** (A/A 는 2163). 진단 문장이 "거짓으로 좁은 구간" → "likelihood 를 논의할 여지" 로 바뀐다 |
| `matrix_reference` (R7-03) | 기준 전용 입력(pristine 반쪽전지)만 바꾸면 LAM_NE 2.8497 → 3.8477 %p 인데 행의 `inputs_sha` 는 **같다**(`15607a668c80`). 실제 기준 소비 입력은 `55a99b55ae92` → `241a9b77f7e1` 로 달랐고 행에는 그 열이 없다 |
| `--case baseline` (R7-04) | 현행 디렉터리를 `--old` 로 줬는데 역사 규칙이 걸려 `_v2`(B) 를 골라 "정본과 전부 같다" rc 0. `_v2` 를 지우면 같은 대조가 차이 2 건 rc 1 |
| `--case adapted` (R7-05) | `R6_OLD_OUT` 없이 부르면 `Path("")` = `.` 이라 **현재 트리를 과거 baseline 으로** 삼아 full 재생 → 5/6 rc 1 |
| `--case controls` (R7-06) | 변이 감사가 `MISSED: 1` 을 찍고도 **rc 0** |

### 수정

| ID | 무엇 | 수정 | 테스트 |
|---|---|---|---|
| **R7-01** (P1) | 미완으로 제외된 상태가 반례일 때 전체 판정이 "아니오"→"예" 로 뒤집힌다 (빈 집합도 "예") | `load_degeneracy`·`load_matrix_axis` 가 `excluded=` 로 뺀 것을 보고하고, `main` 이 **후보/검증/제외**를 세어 찍는다. 제외가 있거나 관측이 0 이면 전체 판정 대신 **미완**(부분집합에서 본 것은 "관측한 n 개 안에서는" 으로 범위를 붙여 따로) 과 **rc 2** | `test_d7_01` (아니오 → 미완 → 아니오 · 빈 디렉터리) |
| **R7-02** (P1) | `cmd_noise` 가 `build` 뒤 풀셀 경로를 **다시 열어** σ 를 재 A 분자 ÷ B 분모 | `build` 가 소비한 **원시 배열**을 `obj.full_cell_raw` 로 들려 보내고 `cmd_noise` 는 그것만 쓴다 (평활·재표본 배열로 바꾸지 않는다 — 정의 그대로). 산출에 `consumed_inputs`·`inputs_sha` 추가 | `test_d7_02` (잡음 있는 정상 재-export 로 σ 를 실제로 움직인다) |
| **R7-03** (P1) | matrix/profile 행이 **기준** 적합의 입력 출처를 안 남긴다 | matrix 행에 `ref_inputs_sha`·`ref_consumed_inputs`(+대상 `consumed_inputs`), profile 행에 `ref_inputs_sha` 와 summary 에 양쪽 `consumed_inputs` | `test_d7_03` (기준 전용 입력만 바꿔 서명이 갈리는지) |
| **R7-04** (P2) | `--old` 가 현행 디렉터리여도 역사 규칙(최고 `_vN`) | `baseline_for(..., policy)` + `--baseline-policy {auto,current,historical}` (auto = `--old-rev` 면 historical). 어느 정책으로 골랐는지·건너뛴 형제를 출력 | `test_d7_04` (두 정책 다) · `test_i6w_03` 은 historical 을 명시 |
| **R7-05** (P2) | `R6_OLD_OUT` 부재가 `.` 로 떨어져 현재 트리를 baseline 으로 | `baseline_from_env()` 가 빈 문자열·공백·없는 디렉터리를 **None** 으로. baseline 없는 재생은 상태 `부분` + `mode: 부분` 으로 full 과 구분 | `test_d7_05` |
| **R7-06** (P2) | 변이 감사가 `MISSED` 에도 rc 0 | `main()` 이 `1 if (bad or 복구실패)`; 스크립트를 import 해도 감사가 돌지 않게 함수로 분리 | `test_d7_06` (놓친 변이를 주입해 rc 확인) |

### Codex 가 짚은 우리 증거의 두 한정 — 같이 고쳤다

- **`test_c6_01` 은 주입을 꺼도 통과했다.** 실제로 재보니 더 나빴다: degeneracy 데이터는 **한 번만** 열리는데
  k 를 1~4 로 가정해서 k≥2 인 건들은 훅이 아예 안 걸린 채 통과하고 있었다. 이제 경계 수를 **먼저 세고**(probe 실행)
  그 수만큼만 돌며, 건마다 `fired["v"] >= k` 로 주입을 확인한다. 관측 결과도 정직하게 적었다 — 읽기 직전 주입에서
  살아남는 것은 B/B 와 명시적 미완뿐이고, A/A 는 대조군과 적응판의 `검증_후_게시` 순서에서 나온다.
- **c6_04 변이가 `KeyError` 로 잡히고 있었다** (파일명 때문에 state 가 사라져서). "옛 값을 실제로 소비했다" 는
  반례가 아니었다 — 변이를 옛 `_keep_latest` 규칙 그대로(판 번호를 떼고 최고판 선택)로 바꿔 값으로 잡히게 했다.

### Q2 전제 정정 (Codex)

R7 요청문 §6 의 "`run_states.sh` 의 실행 직전 `inputs_sha`" 는 **존재하지 않는다** — 그 문자열은 `run_states.sh` 에
0 회고, 실행 전에는 `LAST_PRE_PV` 의 git 상태·시각만 모은다. 입력 서명은 각 `build()` 가 소비 snapshot 으로 만든다.
없는 두 해시의 충돌을 물은 질문이었다. `test_d7_07` 이 이 사실을 고정한다 (`inputs_sha` 가 `run_states.sh` 에
생기면 그 테스트가 깨지고 문장을 다시 써야 한다).

---

## Codex R8 (2026-09-12, 대상 `a22da33`) — **NO-GO (P1 4 · P2 4)**, 여덟 건 전부 재현·닫음 (`reviews/R8_CODEX.md`)

패키지(`reviews/r8_repros/codex/`, sha256 10/10 OK)의 세 스크립트를 **수정 전 HEAD 에서 그대로 돌려 전부 재현**했다
(`reviews/r8_repros/replay_ours_a22da33_before/`). Codex 의 판정 요지: R7 의 반례는 닫혔지만 **"검증된 개별 묶음 →
완전한 모집단 → 전체 결론" 의 합성**이 안 이어진다. 절차: RED(`tests/test_r8_codex.py` d8_01~09) → 수정 → GREEN.

### 수정 전 재현 (우리 HEAD `a22da33`)

| probe | 관측 |
|---|---|
| `aggregate` (R8-01) | state 100 에 Kunz(LLI 폭 9)·Li(폭 1) 둘 다 정상인데 `out[state]` 에서 Li 가 Kunz 를 덮어 **1/1 · 예 rc 0** (Kunz 만이면 아니오). `good=<정상> empty=<빈>`·존재하지 않는 root 를 명시해도 **1/1 · 예 rc 0** |
| `unit` (R8-02) | 다른 정상 시도 B 가 data 만 게시(`read_unit` False)한 상태를 `check_u14` 가 "스키마 전부 갖춤 · 숫자 전부 같다 · rc 0". 또 `MATRIX_COLS`/`PROFILE_COLS` 가 R7-03 의 출처 열을 요구하지 않아 현행 out/(그 열 없음)이 "전부 갖췄다" |
| `shape` (R8-03) | state100 10 mV(짝 있음) · state200 100 mV(matrix 없음) → CSV 는 100 을 남기는데 요약은 "측정된 음극 모양 변화 최대 **10.00** mV", rc 0 |
| `profile` (R8-04) | profile 의 target/ref 전체 identity 는 stdout `SUMMARY` → `.csv.log` 뿐; 다음 정상 재시도가 입력 root 부재로 실패하면 redirect 가 먼저 log 를 잘라 이전 정상 묶음(`read_unit` True)의 출처가 사라진다 |
| `rows` (R8-05) | 같은 key 의 중복행(먼저 오는 쪽 LLI +3 %p)을 넣어도 dict comprehension 이 앞 행을 지워 "전부 같다" rc 0 (`compare_states` 폭은 1.27 → 3.69 로 움직였는데) |
| `controls` (R8-06) | selector `c6_DOES_NOT_EXIST` → pytest rc 5 ("52 deselected") 를 **CAUGHT** 로 세고 MISSED 0 rc 0 |
| R8-07 | 보관한 R7 probe 는 SHA pin 으로 rc 1 (옳다) — 그러나 "수정 뒤 자기 반례 assertion 에서 실패한다" 를 재생할 명령이 없었다 |
| R8-08 | `_hook_open` 의 `fired["v"]` 는 읽기 수라 metadata 경계 callback 만 꺼도 `test_c6_01` 통과 (다른 schedule 의 B/B·미완이 합집합을 채운다) |

### 수정

| ID | 수정 | 테스트 |
|---|---|---|
| **R8-01** (P1) | `load_degeneracy` 가 inventory 를 **먼저** 만들고 같은 state 에 Si 가 둘 이상이면 `state\|si` 로 전부 남긴다(하나면 옛 key 그대로; 같은 (state, si) 둘은 RuntimeError). `main` 이 요청한 root 마다 **roster**(있음/후보/검증/제외)를 찍고, 없거나 관측 0 인 root 가 있으면 전체 판정 대신 미완 + rc 2 | `test_d8_01` (Kunz+Li → 2/2 · 아니오; good+empty · good+absent → 미완 rc 2) |
| **R8-02** (P1) | `check_u14` 가 `read_unit` 의 검증 snapshot 만 검사(`_unit`) — 묶음 불일치는 **broken** 으로 따로 세어 rc 2, "전부 같다" 를 찍지 않는다. `PROVENANCE_COLS = (ref_inputs_sha, consumed_inputs, ref_consumed_inputs)` 를 matrix/profile 필수 스키마에 넣고, 그 열이 없으면 "**provenance-incomplete** — 재실행(U18)으로 보강, pathname 해시로 소급 채우지 않는다" 로 이름 짓는다. **현행 out/ 12 개는 이 상태다** (아래 "정본 범위") | `test_d8_02` |
| **R8-03** (P1) | `ne_shape` 측정 통계는 requested 전부에서, γ 통계는 paired 에서; `pairing{requested, paired, missing}` 을 stdout·meta 에; missing 이 있으면 **rc 3(부분)** | `test_d8_03` |
| **R8-04** (P1) | profile 행마다 `consumed_inputs`·`ref_consumed_inputs`(JSON) — 검증되는 CSV 자체에 (matrix 행과 같은 모양). 실행 log 는 receipt 가 아니다 | `test_d8_04` (log 를 비워도 CSV 에서 회수) |
| **R8-05** (P2) | `_rows_from` 이 dict 변환 전에 중복 key·행 수를 세고 diff 로 보고 | `test_d8_05` |
| **R8-06** (P2) | `classify(rc, last)`: rc 5·선택 0·수집 오류 = **오류**(CAUGHT 아님) → rc 1 | `test_d8_06` |
| **R8-07** (P2) | `reviews/r7_repros/replay_codex_r7.py` — 원본 R7 probe 를 pin 우회로 직접 불러 **도달·상태(재현/반례 소멸/오류)·멈춘_곳**을 따로 기록; R7-05·06 은 현행 API 로 적응한 positive-closure 검사 | `test_d8_07` (R7-01·06: 도달 True · 반례 소멸) |
| **R8-08** (P2) | `_hook_open` 이 `published`(callback 수)를 따로 세고 `test_c6_01` 이 건마다 `published == 1` 과 schedule 별 (기대 게시 id, 관측) 을 assert | `test_d8_08` |

**c6_04 정정 (R7·R8 이 두 번 짚음)**: "이제 값으로 잡힌다" 는 R8 요청문의 주장은 **틀렸다** — 변이는 여전히 `_v2` 파일명
때문에 state 가 사라져 `KeyError` 로 잡히고 있었다. 이번엔 옛 `_keep_latest` 규칙을 **두 자리**(최고판 선택 + 판 번호를
뗀 이름으로 파싱)에 되살려, 독자가 key "100" 아래 `_v2` 의 222 를 돌려주고 값 assertion 이 잡는다 (`test_d8_08` 이 변이를
사본에 적용해 222 소비를 직접 확인한다; `apply()` 가 두 자리 변이를 지원).

### 정본 범위 — 현행 `out/` 12 개는 provenance-incomplete 다

숫자(matrix 2,240 칸 · degeneracy 12 span · §5 표 35 칸)는 R7 과 바이트 동일하고 data/meta 묶음도 전부 True 다. 그러나
matrix 4 개에는 `ref_inputs_sha`·`consumed_inputs`·`ref_consumed_inputs` 가, profile 4 개에는 `ref_inputs_sha`·
`consumed_inputs`·`ref_consumed_inputs` 가 없다 — **기준 입력의 출처는 그 묶음에서 회수되지 않는다**. `check_u14 --new
out --schema-only` 가 이제 그것을 rc 2 로 말한다. 보강은 실제 재실행 **U18**(사용자 기계, 별도 destination 에 만들어
비교·승격 — 현재 pathname 해시로 소급 채우지 않는다)이다. 그때까지 정본 인용은 "수치는 그대로, 기준 입력 출처는 미기록" 으로
범위를 붙인다.

### Codex 질문에 대한 답 (R9 요청문 §3 에 다시 싣는다)

1. 미완 전파가 빠진 소비자 — `compare_states` roster(R8-01) · `ne_shape` paired subset(R8-03) · `check_u14` 묶음/스키마/
   중복(R8-02·05) 을 닫았다. 정적 문서 표는 생성 경로가 모집단 receipt 를 소비하지 않는 한 코드 회귀만으로 완전성이
   증명되지 않는다 — 요구서는 관측마다 모집단/roster 를 적는다 (Q6).
2. 두 번 읽기 — 남은 것은 receipt 내구성(R8-04) 이었고 닫았다. `ne_shape` 가 옛 matrix γ 를 현재 문헌 export 에 대입하는
   것은 재적합이 아니라 **sensitivity 경계** — 양쪽 직접 입력을 기록하되 "같은 export" 계약은 걸지 않았다 (R9 Q).
3. target/reference export 정책 — 공통 snapshot 강제는 아직 안 했다 (R9 미결로 올린다).
4. `--baseline-policy auto` — 손으로 푼 옛 out/ 은 explicit historical 을 요구하는 편이 안전하다: 남긴다.
5. U16·U17 순서 — U16(옛 조합 재실행, receipt 보존) 먼저, U17 스키마는 다음 계획 실행에. 여기에 **U18**(출처 열 보강
   재실행)이 더해졌다 — 셋 다 사용자 기계, 어느 것도 current canonical 을 바로 덮지 않는다.
6. 다섯 관측 → 요구서 — 행마다 모집단/roster·completeness·입력 receipt·관측 범위·후보 변경·대안 가설·구분 실험·임계값·
   실패/미계산 의미·evidence version 을 둔다.

## Codex R9 (2026-09-12, 대상 `29ef505`) — **NO-GO (P1 7 · P2 5)**, 열두 건 전부 재현·닫음 (`reviews/R9_CODEX.md`)

패키지(`reviews/r9_repros/codex/`, sha256 11/11 OK)의 세 스크립트와 classify probe 를 **수정 전 HEAD 에서 그대로 돌려 전부
재현**했다 (`reviews/r9_repros/replay_ours_29ef505_before/` — `r9_root_repros.py` 다섯 묶음 assertion 전부 통과
`R9_ROOT_REPROS_PASSED` · `r9_aggregation_repros.py` 12 case 기록 · `r9_provenance_repro.py` `raced_status: complete`,
`read_count: 3`, U18 gate 세 case 전부 rc 0). Codex 의 판정 요지: R8 의 여덟 수정은 허상이 아니지만 **"모집단을 먼저 세고,
검증 snapshot 만 검사하고, 부분은 부분이라 말한다" 가 아직 production 전체의 불변식이 아니다** — 인자 파싱·U18 승격·
`ne_shape` 입력/게시·`dd_eval` 검증에서 각각 우회된다. 절차: RED(`tests/test_r9_codex.py` d9_01~12, 12 failed 로 시작) →
수정 → GREEN.

### 수정 전 재현 (우리 HEAD `29ef505`)

| probe | 관측 |
|---|---|
| `root_alias` (R9-01) | `same=<빈> same=<정상>` → "요청한 root 1 개 · 검증 1 · 예" rc 0; label 없는 `<빈> <정상>` 도 둘 다 `out` 이 되어 뒤가 앞을 지운다 (반대 순서만 rc 2) |
| `u18_gate.one_of_twelve` (R9-02) | 정본 12 개 중 `degeneracy_100_Li.json` 한 묶음만 new 에 두고 대조 → "산출 1 개 · 전부 갖췄다 · 전부 같다" rc 0 |
| `blank_provenance` · `u18_gate.blank_receipts` · `config_mismatch` · `u14_dropped_numeric_column` · `u14_duplicate_schema_only` (R9-03) | 출처 열 값을 전부 비워도 `read_unit` True + "전부 갖췄다" rc 0; `ref_inputs_sha="f"*64`·`consumed_inputs="{}"` 도 "전부 같다" rc 0; `LLI_pct` 를 지워도 rc 0; 실행 조건 `{24,0,21,400,1%}→{1,731,999,1,50%}` 도 "게시·서명만 바뀌었다" rc 0; `--schema-only` 는 중복 key 를 안 본다 rc 0 |
| `shape_missing_halfcell` (R9-04) | 선언 pristine·100·200 에서 200 반쪽전지만 없으면 `{requested:[100], paired:[100], missing:[]}` · rc 0 — 200 은 모집단에 들기 전에 사라진다 |
| `shape_duplicate_matrix_rows(+reversed)` (R9-05) | 서명된 matrix 에 (GITT, Li, 0) 두 행(γ 0.10 / 0.40) → 행 순서가 γ 를 정하고 둘 다 paired 1/1 rc 0 |
| `shape_partial_overwrites_complete` (R9-06) | 완전 실행(100·200) 게시 뒤 200 짝을 없애고 다시 돌리면 rc 3 인데 canonical CSV/meta 가 부분 묶음으로 **교체**됐고 그 묶음도 `read_unit` True |
| `eval_verified_bytes_race` (R9-07) | `_compare_dd_eval` 이 경로를 **3 번** 읽는다 — 첫 read 가 malformed A(중복 헤더), 직후 정상 B 로 교체되면 단독 A 는 invalid 인데 race 는 32/32 `complete` |
| `replay_vacuity` (P2-1) | `replay_codex_r7.py --probes DOES_NOT_EXIST` → `probes: {}` rc 0 |
| P2-2 | 러너가 expected SHA·clean·패키지 bytes 를 대조하지 않는다 (임의 HEAD 에서도 rc 0) |
| `r9_evidence_classify_probe` (P2-3) | 같은 `1 failed` summary 에 rc 2·3·4 도 CAUGHT (5 만 오류) |
| P2-4 | `run_states.sh` sidecar 가 matrix 에도 singular `si_source: Li` 를 적는데 본문은 2 반쪽전지 × 8 Si × 2 가중 = 32 행 |
| P2-5 | 짝이 전부 없으면 rc 1 이 rc 3 보다 먼저 — 요청문의 "missing pair 면 rc 3" 계약과 wrapper 가 1/3 을 구분하지 않았다 |

### 수정

| ID | 수정 | 테스트 |
|---|---|---|
| **R9-01** (P1) | `compare_states.main` 이 인자를 **순서 있는 목록**으로 들고 중복 label(암묵적 `out` 포함)을 **판정 전에** 거부한다 (rc 2, 판정 줄 없음) | `test_d9_01` |
| **R9-02** (P1) | `check_u14` 의 명부(roster) = 정본 ∪ 새 산출의 canonical basename (`canonical_names`; historical 은 `_vN` 을 뗀 이름). 정본에 있는데 새 산출에 없으면 "명부 불일치" rc 2; 부분 재실행은 `--subset` 으로 계약을 명시해야 하고 그때도 `k/N` 을 찍으며 "승격 근거가 아니다" | `test_d9_02` |
| **R9-03** (P1) | 스키마의 **한 정본** `bms_balancing/schema.py` (아래). checker 가 열 이름 다음에 **값**을 본다 — 필수 셀 nonempty·숫자 파싱·receipt(역할·path·64-hex·재계산 aggregate digest)·중복 key — `--schema-only` 에서도; degeneracy 는 `DEGENERACY_CONTROLS` 와 meta `state/half_cell_source/si_source/starts/seed` 를 정본과 대조해 다르면 "실행 조건 불일치" rc 2 | `test_d9_03` (A 열 삭제 · B 빈/가짜 receipt · 진짜 receipt 대조군 · C 조건 · D schema-only 중복) |
| **R9-04** (P1) | `ne_shape` 의 requested 명부는 **파일 존재를 보기 전에** 고정 (`D.HALF_FILE[source] ∩ D.STATES`, 또는 `--states`); `pairing{requested, requested_from, available, missing_input, paired, missing}` 을 meta·stdout 에 | `test_d9_04` |
| **R9-05** (P1) | `fitted_pair_info` 가 checker 와 같은 typed validator(`schema.unique_rows` · `matrix_key`: w_dqdv 는 숫자)로 파일 전체 key 유일성을 강제 — 중복이면 `RuntimeError(중복)`, 첫 행을 고르지 않는다 | `test_d9_05` |
| **R9-06** (P1) | 완전성 판정이 **게시보다 먼저**: typed `status` complete/partial/none. complete 만 canonical `<write>/`; partial·none 은 `<write>/partial/` 에만 (canonical bytes 불변, `read_unit` True 유지) | `test_d9_06` |
| **R9-07** (P1) | `load_dd_eval` 이 경로를 **정확히 한 번** 읽어 `DdEvalText(path, text, sha256)` 를 만들고 parse·precision·audit·compare 가 전부 그 snapshot 을 소비한다 (`_dd_eval_lines`); 결과에 `matlab_sha256` | `test_d9_07` (`Path.read_text` 1 회 · race 판정 invalid) |
| **P2-1** (P2) | `replay_codex_r7.py`: `--probes` 빈/오타/중복/valid+unknown 거부 rc 2, JSON 없음; 출력 key == 요청 집합 | `test_d9_08` |
| **P2-2** (P2) | 같은 러너: `--expected-head` 필수(불일치 rc 2), dirty 트리는 기본 거부(`--allow-dirty` 는 목록 기록), 패키지 bytes 를 `HARNESS_R7_521BE85_SHA256SUMS.txt` 와 대조(`package_digest_ok`), 재현/오류/mismatch 면 rc ≠ 0 | `test_d9_08` |
| **P2-3** (P2) | `classify`: CAUGHT 는 rc 1 ∧ `N failed` 일 때만, MISSED 는 rc 0 ∧ `N passed`(failed 없음) 일 때만, 나머지 전부 오류 | `test_d9_09` |
| **P2-4** (P2) | `run_states.sh`: `run` 이 `LAST_ARGV="$*"` 를 남기고 `write_meta` 가 잠금 안 **한 번 읽은 bytes** 로 id 재확인·sha256·`roster`(본문에서 유도: 행 수·half_cell·si·w_dqdv·γ 범위)·`argv` 를 sidecar 에 봉인 (`si_source` 는 wrapper 환경값이라는 note) | `test_d9_10` |
| **P2-5** (P2) | 종료 코드 계약을 코드에 적었다 (`EXIT_BY_STATUS = {complete: 0, none: 1, partial: 3}`): 짝 0 은 rc 1 + typed `status: none` (partial/ 에), 일부는 rc 3 + `partial`; wrapper 가 meta 의 status 로 가른다 | `test_d9_11` |

### 스키마의 정본 — `bms_balancing/schema.py`

producer(`cmd_matrix`·`cmd_profile`·`cmd_degeneracy`)가 쓰는 키와 checker(`check_u14`)·reader(`ne_shape`)가 요구하는 키가
한 파일에서 나온다: `MATRIX_ROW` 39 열 · `PROFILE_ROW` 20 열 · `DEGENERACY_KEYS` 22 키 · `DEGENERACY_CONTROLS` · `PROVENANCE_COLS`
· `MAY_BE_EMPTY`(scale_audit_*) · `inputs_digest`(verify 는 여기서 빌린다) · `matrix_key`/`profile_key`/`unique_rows` ·
`validate_receipt` · `check_rows` · `check_degeneracy`. producer 는 행/키 집합을 `assert tuple(row) == MATRIX_ROW` 처럼 **쓰기
직전에** 대조한다 (degeneracy 는 `--out` 게시 경계에서; stdout 모드는 경고만 — 시험용 objective 가 거기서 돈다).

**fixture 가 진실을 가리고 있었다 (네 번째 실측)**: `_full_matrix_rows`(R8)·`_deg(schema=True)`(R7)·`_u14_dirs`(R6)·i6w_03 의
inline JSON 은 전부 **열 이름의 부분집합 + 가짜 receipt**(`sha256: "x"`, `inputs_sha: "a"*12`)였다 — checker 가 내용을 안 본다는
사실을 fixture 가 가려 주고 있었다. 전부 producer 스키마 + 진짜 receipt(64-hex·재계산 digest)로 다시 썼고, 그 뒤에야 d9_03
의 대조군(진짜 receipt 는 rc 0)이 의미를 가진다. c6_03·d8_03 은 짝 없는/부분 실행의 산출을 `partial/` 에서 읽도록 옮겼다
(R9-06 의 결과). 현행 `out/` 12 개는 이 검사에서 **출처 열 24 건만** 빠지고(provenance-incomplete, 전과 같은 판정) 내용·조건·
숫자(자기 대조)는 전부 통과한다.

### 수정 뒤 패키지 재실행 (`reviews/r9_repros/replay_ours_after_fixes/`)

| 스크립트 | 결과 |
|---|---|
| `r9_root_repros.py --case roots / provenance / shape-overwrite` | 각각 **자기 반례 assertion** 에서 rc 1 (`assert missing_first.returncode == 0` · `assert checked.returncode == 0 and "전부 갖췄다"` · `assert rc2 == 3 and meta2["pairing"]["missing"] == ["200"]` — 세 번째는 canonical meta 가 완전 묶음 그대로라 깨진다) |
| `--case shape-roster` · `--case replay-vacuity` | 반례 assertion **앞에서** 죽는다 — 전제가 바뀌었다 (partial 은 `<write>/partial/` 에 있고, 러너는 거부 rc 2 에 JSON 을 내지 않는다) → 적응 probe 로 positive closure |
| `r9_aggregation_repros.py` | compare/u14 다섯 case 뒤 `shape_missing_input_state` 에서 canonical 부재로 죽는다 (같은 이유) → helper 그대로 적응 |
| `r9_provenance_repro.py` | rc 0 (기록형): `dd_eval_reread.read_count` 3 → **1**, `raced_status` complete → **invalid**, `raced_compared` 32 → 0; `u18_gate.one_of_twelve`·`blank_receipts`·`config_mismatch` rc 0 → **2** (셋 다); `production_paths.shared_full_cell_mismatch_accepted` 는 **true 그대로** (export 계약, 아래 "열어 둔 것") |
| `r9_evidence_classify_probe.py .` | rc=1 CAUGHT · rc=2·3·4·5 오류 |
| R6 적응판 `replay_codex_r6_adapted.py` (R6-03a) · R7 러너의 R7-05 · `mutation_adapted.py` baseline | R9-04 뒤 requested 명부가 **선언**에서 오므로 pristine·100 만 있는 합성 소스에서 200·300_* 이 missing_input → status partial(rc 3) → 산출이 `out/partial/` 로 가서 원본 helper(`cl.run_shape`: rc 0 + canonical)의 전제가 깨졌다 (`R6-03a: 열림`, mode 실패, R7-05 재현). 적응판 a4 가 `D.STATES=[pristine, 100]` 을 명시하도록 hook 만 고쳤다 — 판정은 그대로 (A 값이면 A 서명) |
| `reviews/r9_repros/replay_codex_r9.py` (닫힘 재생기, R7 러너와 같은 계약) | 12 probe **전부 도달 True · 반례 소멸** — 원본 함수 직접 호출 5(R9-01·03·06 은 자기 반례 assertion 에서, R9-05·R9-07 은 패키지 함수/helper 그대로 판정만 뒤집어) + 적응 7. clean 트리 실행은 `replay_codex_r9_after_fixes.json` (expected-head 는 그 파일의 값) |

### 열어 둔 것

- **export 계약 (Codex Q3)**: `shared_full_cell_mismatch_accepted: true` 그대로다 — 기준(pristine)과 대상이 같은 workbook 을 각자
  읽어 두 identity 를 기록만 한다. Codex 의 위치 제안(command/build 경계에서 한 번 읽은 typed snapshot 을 양쪽에 전달, 다른
  export 는 명시적 sensitivity 모드 + A/B digest)을 채택하되 이번 라운드에는 넣지 않았다 — R10 §6.
- **typed (root, state, si) identity (Codex Q1)**: 아직 문자열 `state|si` 다. 중복 label 은 이제 그 전에 거부된다.
- **U18 승격 규칙 (Codex Q5)**: exact 명부 + 스키마 내용 + 조건/env + 수치 exact equality 는 `check_u14` 가 강제한다. profile 행이
  움직이면 rc 1 로 승격되지 않는다; "후보 evidence version 보존 + pinned 옛 환경 재현 + U16 attribution" 은 절차(문서)다.

### Codex 질문에 대한 답 (R10 요청문 §3 에 다시 싣는다)

1. `state|si` 는 유지하되 중복 label 을 사전에 거부한다 (R9-01). typed 3-tuple identity 는 다음 라운드.
2. 다섯 관측은 "provenance-incomplete 탐색적·잠정" 으로만 요구서 초안에 옮긴다 — GO·승격·원인·출처 주장의 근거로 쓰지 않는다.
3. 공통 snapshot 강제 위치 동의 (build 경계) — 미구현, 열어 둔다.
4. rc 3 은 typed `PARTIAL`(meta `status`) 로 보존하고 canonical 을 덮지 않는다 (R9-06); zero-pair 는 rc 1 + `none` (P2-5).
5. U18: 명부·receipt·조건·env 를 먼저 강제하고 exact equality — `check_u14` 가 그 순서로 실패한다; 움직인 profile 행은 승격 안 함.

## Codex R10 (2026-09-13, 대상 `bd6ba47` · 코드 정본 `554dad6`) — **NO-GO (P1 8 · P2 7)**, 열다섯 건 전부 재현·닫음 (`reviews/R10_CODEX.md`)

패키지(`reviews/r10_repros/codex/`, sha256 10/10 OK)의 세 스크립트를 **수정 전 clean 트리에서 그대로 돌려 전부 재현**했다
(`reviews/r10_repros/replay_ours_bd6ba47_before/` — 세 스크립트 rc 0 = bad-state assertion 전부 통과). Codex 의 판정 요지:
R9 의 열두 수정은 허상이 아니지만 **"모집단을 먼저 세고, 검증 snapshot 만 검사하고, 부분은 부분이라 말한다" 가 게시
경계·승격 gate·증거 기계에서는 아직 참이 아니다** — 출력이 비교 근거를 덮고, caller 가 roster 를 줄여 complete 를
참칭하고, `error` 한 칸이 검증을 끄고, 러너가 자기가 실행한 bytes 를 봉인하지 않는다. 절차: RED(`tests/test_r10_codex.py`
d10_01~16) → 수정 → GREEN.

### 수정 전 재현 (우리 HEAD `bd6ba47`, clean)

| probe | 관측 |
|---|---|
| `eval-self-overwrite` (P1-1) | `--out X --compare X` 에서 X 가 `c3dabc9d…` → `3d18405e…` 로 **교체된 뒤** comparator 가 처음 읽는다 → 16/16 앵커·32/32 RMSE `complete` rc 0 (자기대조) |
| `shape_subset` · `shape_duplicates` (P1-2) | 선언 100·200 의 2 행 complete canonical 을 `--states 100` 이 **1 행으로 교체**하며 rc 0 · status `complete`; `--states 100,100` 은 requested/paired 2/2 · 중복 2 행 · rc 0 |
| `profile-partial` (P1-3) | γ 2 중 1 실패 → 1 행이 canonical 교체, rc 0, `check_rows` 문제 0, 실제 `write_meta` 서명 + `provenance --verify-unit` 까지 **일치** |
| `matrix-errors` (P1-4) | 전 조합 실패 → 4 열 error 행 16 개가 canonical 교체, 스키마 문제 36 건, 함수 `None` → process rc 0 |
| `error-skip` · `error_bypass` (P1-5) | 정상 수치 행에 `error=skip` + receipt 4 칸 공백 → `check_rows` 문제 0, gate "전부 갖췄다 · 전부 같다" rc 0 |
| `receipt-roles` · `receipt_roles` (P1-6) | half_cell↔full_cell 을 바꿔도 digest 같음(`76be1dcab00e`); `{"decoy":…}` 하나만 든 receipt 도 validator 문제 0 · gate rc 0 |
| `controls` (P1-7) | candidate meta 의 env 를 alien 으로 바꿔도, `state`·`starts` 를 지워도 rc 0 "전부 같다" · 조건 불일치 0 |
| `same_root` (P1-8) | 같은 signed 디렉터리를 `--new`/`--old` 에 함께 주면 rc 0 · roster 1/1 · "전부 같다" |
| `--subset` (P2-1) | "부분 · 승격 아님" 을 찍고도 rc 0 — 자동 소비자는 full equality 와 구분 불가 |
| `stdout-invalid` (P2-2) | receipt·`inputs_sha` 없는 degeneracy JSON 을 stdout 으로 흘리고 stderr 경고 뒤 rc 0 |
| `argv` · `argv-flatten-collision` (P2-3) | `['cmd','a b','c']` 와 `['cmd','a','b c']` 가 같은 `cmd a b c` 로 기록 · `argv-binding-mutant`: `LAST_ARGV="FORGED-BY-MUTANT"` 변이가 `test_d9_10` 을 통과 |
| `optimized-assertions` (P2-4) | `PYTHONOPTIMIZE=1` + 잘못된 `PYTEST_ADDOPTS` → delegated pytest 는 usage error 인데 runner rc 0 · `closed: true` · P2-4 `반례 소멸` |
| `git-status-error` · `assume-unchanged` · `ignored-pyc` (P2-5) | `GIT_INDEX_FILE=<dir>` 로 status rc 128 인데 `dirty: false · closed: true` · `assume-unchanged` 로 고친 `verify.py` 가 **실행되고**(marker 생성) clean · ignored `__pycache__` 의 위조 bytecode 가 실행되고 clean |
| `package-enforcement-mutant` (P2-6) | `package_digest()` 를 항상 True 로 만드는 변이가 `test_d9_08` 을 통과(`1 passed`), 실제 파일을 손상시켜도 `package_digest_ok: true · closed: true · rc 0` |
| `wrapper-coverage` (P2-7) | `ne_shape` 의 rc 1/3·meta status 를 소비하는 production wrapper **0 개** |

### 수정

| ID | 수정 | 테스트 |
|---|---|---|
| **P1-1** | `cmd_eval` 이 `--compare` snapshot 을 **모든 쓰기 전에** 한 번 읽고 그 `DdEvalText` 만 comparator 에 넘긴다. `--out` 과 `--compare` 가 **같은 object**(realpath/samefile — symlink·hardlink 포함)면 거부 rc 2 | `test_d10_01` |
| **P1-2** | `ne_shape` 의 정본 roster(authority) = `D.declared_states(source)` (선언 − **알려진 부재** `D.HALF_CELL_ABSENT`). `--states` 는 그 부분집합만 고를 수 있고 축소 실행은 status `subset` · rc 3 · canonical 금지; 중복·미선언은 rc 2 | `test_d10_02` |
| **P1-3** | `cmd_profile` 이 γ roster 를 계산 전에 고정하고 `gamma_roster`(요청·성공·누락)를 **행마다 봉인**; complete 만 canonical, 부분은 `partial/` + rc 3 | `test_d10_03` |
| **P1-4** | `cmd_matrix` 가 기대 조합 roster 를 돌기 전에 정하고(알려진 부재만 제외) typed status 로 게시 — complete 만 canonical, 나머지는 `partial/`; 종료 코드 0/3/1 | `test_d10_04` |
| **P1-5** | `schema.check_rows` 가 success/error **exact tagged union** — success 행에 `error` 금지, error 행이 하나라도 있으면 그 묶음은 승격 대상 아님, 모르는 열도 문제 | `test_d10_05` |
| **P1-6** | receipt 에 **역할**을 묶는다: `REQUIRED_ROLES = (full_cell, half_cell, literature.gr, literature.si)` exact, `inputs_digest` 는 `(역할, sha256)` 을 버전 태그와 함께 해시 (역할 swap → 다른 digest) | `test_d10_06` |
| **P1-7** | `check_u14` 가 `env` 를 **값으로** 대고(`schema.env_problems`, python·numpy·scipy·platform) 필수 control 은 **양쪽에 있어야** 한다 — 지우면 잠들던 검사가 이제 불일치로 잡힌다 | `test_d10_07` |
| **P1-8** | candidate 와 baseline 이 같은 object 면 rc 2 (자기대조 거부; `--old-rev` 의 immutable bytes 는 별도 경로) | `test_d10_08` |
| **P2-1** | `--subset` 은 rc 3 이고, 마지막 줄 `PROMOTION {…}` 이 `promotion_eligible`·roster·`blocked_by` 를 machine-readable 로 낸다 | `test_d10_09` |
| **P2-2** | degeneracy 가 schema 를 어기면 **sink 와 무관하게** rc 2 이고 bare artifact 대신 typed diagnostic(`status: invalid`)을 낸다 | `test_d10_10` |
| **P2-3** | `run_states.sh` 의 `run()` 이 `"$@"` 를 JSON array 로 직렬화(`LAST_ARGV_JSON`)하고 meta 의 `argv` 는 vector 다; 회귀가 **실제 `run()`** 을 shim producer 로 통과한다 | `test_d10_11` |
| **P2-4** | 두 러너가 `python -O` 에서 증거를 만들지 않고(`gate.require_assertions`), 자체 판정은 `assert` 가 아니라 `gate.need` 의 명시적 분기; delegated pytest 의 rc 를 **값으로** 최종 술어에 묶는다 | `test_d10_12` |
| **P2-5** | 증거 gate 를 `reviews/evidence_gate.py` 한 자리로: `git` 의 rc 를 보고, index skip flag 를 거부하고, `__pycache__` 를 읽지 않게 캐시 prefix 를 돌리고, **expected commit 의 sparse detached worktree** 에서 대상 bytes 를 실행한다. 도구 자신도 그 커밋의 blob 과 같아야 `evidence_eligible` 이 true (`instrument_sealed`) | `test_d10_13` |
| **P2-6** | 회귀가 **실제 패키지 byte 를 손상시켜** 러너가 probe 를 안 돌리는지 본다 (전 판은 source 문자열만 봤다). 행동 자체는 이미 옳았고 빠진 것은 회귀였다 — 변이 감사가 그것을 증명한다 | `test_d10_14` |
| **P2-7** | `run_states.sh` 에 `shape_step` — `ne_shape` 의 rc 0/1/3 과 meta `status` 를 읽어 typed 로 보고하고 그대로 전파하는 **production caller**; 회귀가 그 함수를 직접 돌린다 | `test_d10_15` |

### 의도적으로 다르게 간 곳 — receipt digest 에 **경로를 넣지 않는다**

Codex 의 P1-6 최소 조건은 "`(role, object identity/path, sha256)` canonical manifest 전체를 hash" 다. 우리는 `(역할, sha256)`
만 해시하고 **경로는 receipt 안에 남기되 digest 에서 뺐다**. 이유: R6 내부 F4 가 "같은 bytes 면 같은 실행" 을 고정했고
(`test_i6p_04`: 풀셀 워크북을 이름만 다른 사본으로 바꿔도 digest 가 같아야 한다 — 그 시험이 지금도 돈다), 경로를 넣으면
byte 가 같은 재-export 가 다른 실행으로 읽힌다. 우리 입력의 object identity 는 bytes 이고 경로는 라벨이다 (R6 내부 F1 의
결론과 같다). 역할 결속이라는 **결함의 본체**는 닫혔다 — 역할을 바꾸면 digest 가 달라진다. 경로까지 묶어야 한다면 한 줄
변경이고, R11 §6 Q1 에서 묻는다.

### 알려진 부재 allowlist — `data.HALF_CELL_ABSENT`

P1-2·P1-4 의 "축소된 roster" 를 닫으려면 **없는 것이 요청 밖인지(알려진 부재) 아니면 빠진 것인지(missing_input)** 를
코드가 갈라야 한다. `HALF_CELL_ABSENT = {("GITT", "300_0147")}` 는 실측에서 왔다: `out/matrix_300_0147.csv` 는 step_005C
16 행뿐이고 GITT 행이 없다 · `out/degeneracy_300_0147_Li.json` 의 half_cell 은 step_005C · 나머지 세 상태의 matrix 는 두
소스 32 행 · `run_states.sh` 의 `pick_src` 주석(2026-09-10 실측). `D.declared_states("GITT")` 가 `[100, 200, 300_0009]` 를
주는데 이는 커밋된 `out/ne_shape_GITT_Li.csv` 의 행 집합과 **정확히 같다**.

### digest 규칙이 바뀌어 **정본의 옛 `inputs_sha` 는 새 규칙으로 재계산되지 않는다** (실측)

`inputs_digest` 를 역할 결속으로 바꾸면서 값이 달라졌다 (그래서 `RECEIPT_SCHEMA_VERSION = "r10.1"` 을 payload 에 넣었다).
그 결과 커밋된 `out/degeneracy_*.json` 네 개는 receipt(역할 넷 다 있다)는 통과하지만 기록된 `inputs_sha` 가 옛 규칙의
값이라 재계산과 안 맞는다 — `check_u14 --new out --schema-only` 가 이제 그것을 "내용 검사 실패 4" 로 말한다
(`replay_ours_after_fixes/check_u14_out_schema_only.txt`, 출처 열 누락 24 + profile `gamma_roster` 4 는 그대로).

**숫자는 하나도 안 움직였다** — 바뀐 것은 digest 규칙이고, 옛 값은 옛 규칙의 값이다. 이것도 U18 재실행이 채운다
(재실행 산출은 새 규칙으로 서명되고 gate 가 재계산과 대조한다). 소급해서 값을 고쳐 넣지 않는다 — 그러면 그 digest 가
무엇을 증명하는지 사라진다.

### 계약이 바뀐 곳 (이전 라운드 회귀를 같이 고쳤다)

| 전 | 후 | 왜 |
|---|---|---|
| `check_u14 --subset` rc 0 | **rc 3** + `PROMOTION` 줄 | P2-1 — 글자로만 "승격 아님" 이면 자동 소비자가 못 읽는다 (`test_d9_02` 갱신) |
| 러너: dirty 트리 **거부** | dirty 여도 **격리 snapshot 에서** 실행하고 dirty 를 기록 | P2-5 — 실행 bytes 를 commit 에서 가져오면 worktree 상태는 오염원이 아니다 (`test_d9_08` 갱신) |
| sidecar `argv` = `$*` 문자열 | **JSON array** | P2-3 (`test_d9_10` 갱신, production 결속은 `test_d10_11`) |
| `check_u14 --new out --old out` (자기 점검) | rc 2 로 **거부** | P1-8 — 자기대조는 승격 근거가 아니다. 현행 정본 점검은 `--schema-only` 로 |

### fixture 가 또 가리고 있었다 (다섯 번째)

`_Ridge`(합성 objective)가 receipt 를 안 들어서 "stdout 이면 스키마를 봐준다" 는 우회로를 가려 주고 있었고,
`_u14_sign`·`_sign(full=True)`·`i6w_03` 의 inline meta 는 실행 조건(`half_cell_source`·`si_source`·`seed`)이 없어 control
비교가 **양쪽에 없으면 잠드는** 구조를 가려 줬다. 전부 production 이 실제로 쓰는 모양으로 다시 썼다.

### 열어 둔 것

- **export 계약 (R9 Q3 · R10 Q5)**: 여전히 미구현. 공유 workdbook·문헌을 command/build 경계에서 한 번 읽어 role-keyed
  typed snapshot 으로 ref/target 양쪽에 주입하는 설계에 합의했고, 다음 라운드 작업이다.
- **typed `(root, state, si)` identity (R9 Q1)**: 문자열 `state|si` 그대로.
- **U16 · U17 · U18**: 사용자 기계 실측. U18 승격 gate 는 이번에 명부·내용·역할·조건·환경·독립성까지 강제한다.

## Codex R11 (2026-09-13, 대상 `2add074`) — **NO-GO (P1 12 · P2 6)**, 열여덟 건 전부 재현·닫음 (`reviews/R11_CODEX.md`)

패키지(`reviews/r11_repros/codex/`, sha256 13/13 OK)의 네 스크립트를 **수정 전 clean 트리에서 그대로 돌려 전부 재현**
했다 (`reviews/r11_repros/replay_ours_2add074_before/` — sparse worktree at `2add074`, dirty 0). Codex 의 판정 요지:
R10 의 열다섯 수정은 **각 산출 안에서는** 참이 됐지만, (a) 두 실행 **사이**의 입력 identity 를 아무도 대지 않고,
(b) caller 옵션이 권위 명부 자체를 줄이며, (c) 증거 기계가 자기 startup(bytecode·checkout filter·자식 rc·분류기)을
봉인하지 않는다. 절차: RED(`tests/test_r11_codex.py` e11_01~e11_19) → 수정 → GREEN.

### 수정 전 재현 (우리 HEAD `2add074`, clean · 네 스크립트)

| probe | 관측 |
|---|---|
| `receipt_identity` (P1-1) | old/new 의 target `9d6ace08c3d4→48cf03a6b6b8` · ref `d789ce826bcd→e9a7ac3dea7c` — 네 digest 가 전부 다른데 rc 0 · `blocked_by` 전부 0 · `promotion_eligible: true` |
| `matrix_subset` (P1-2) | `--only-source --only-wdqdv` 로 8/32 행만 돌고 status `complete` · canonical 게시 |
| `profile_grid` (P1-3) | `--grid 1` 이 1 행 · `gamma_roster {requested 1, succeeded 1, missing []}` · status `complete` · canonical 게시 (wrapper 기본은 21) |
| `allowlist` (P1-4) | `HALF_CELL_ABSENT` 의 `(GITT, 300_0147)` 이 **파일이 실제로 있는데도** 요청에서 빠지고 16 행이 complete canonical |
| `per_file_alias_self_comparison` (P1-5) | 디렉터리는 다른데 data·meta 가 **hardlink 로 같은 object** — rc 0 · "전부 같다" · 승격 가능 |
| `schema_only_no_baseline` (P1-6) | `--schema-only` 가 baseline 0 · 대조 0 인데 `promotion_eligible: true` (승격 증명서로 인용 가능) |
| `shape_reader` (P1-7) | `error="optimizer failed"` 행을 `S.check_rows` 는 거부하는데 `fitted_pair_info` 는 그 행의 (0.4, 0.2) 를 과학 입력으로 반환 |
| `matrix_inf` · `degeneracy_infinity` · `a_NE="not-a-number"` (P1-8) | 비유한·비숫자 값이 스키마 문제 0 으로 통과하고 승격 가능 |
| `u18-dirty-meta` · `untracked-sitecustomize` (P1-9) | `git_dirty: true`·`git_state_changed_during_run: true` meta 가 rc 0 승격; 저장소 안 untracked `sitecustomize.py` 가 **실제로 실행되는데**(marker 생성) provenance 는 `git_dirty: false` |
| `early-gate-pyc` · `materialize-smudge` (P1-10) | timestamp/size 를 맞춘 ignored `reviews/__pycache__/evidence_gate…pyc` 가 gate 보다 **먼저** load 돼 marker 실행 — `instrument_sealed`·`evidence_eligible`·`closed` 전부 true; committed `.gitattributes` + smudge driver 로 materialize 된 `verify.py` bytes 가 blob 과 달라도 같음 |
| `r10-child-rc` (P1-11) | evidence 자식 일곱 개가 전부 rc 7 인데 parent 가 기대 boolean 만 읽고 rc 0 · 22-case `closed: true` |
| `r10-assertion-alias` (P1-12) | `schema.inputs_digest` 가 `AssertionError("UNRELATED production invariant")` 를 내게 하자 parent 가 `도달: true · 반례 소멸` 로 기록 |
| `profile_partial_stdout` (P2-1) | sink 가 stdout 이면 부분 실행(`missing [0.5]`)도 rc 0 |
| `shape_step` (P2-2) | stale canonical 과 fresh partial 이 함께 있으면 `ls | head -1` 이 **stale** 의 status 를 읽어 rc 0 shim 에 "**complete** (meta status partial)" 를 찍고 `SHAPE_STEP_RC=0` |
| `receipt_shape` · `duplicate_receipt_direct` (P2-3) | nested `literature.gr` 과 top-level dotted `"literature.gr"` 를 **다른 SHA 로** 함께 둬도 validator 문제 0; path 만 뒤바꾼 receipt 도 digest 동일 |
| `profile_gamma_roster_not_validated` (P2-4) | 유효한 profile 행의 `gamma_roster="not-json"` 이 문제 0 |
| `skip-worktree` (P2-5) | git 은 `S reviews/evidence_gate.py` 를 찍는데 `index_skip_flags()` 는 빈 목록 (소문자만 봤다) — 러너 rc 0 · eligible/closed true |
| `abbreviated-head` (P2-6) | 7 자 prefix `2add074` 만 넘겨도 rc 0 이고 그 짧은 값이 expected head 로 기록 |

### 수정

| ID | 수정 | 테스트 |
|---|---|---|
| **P1-1** | `check_u14` 가 baseline↔candidate 의 `{역할: full sha256}` map 을 target·ref 양쪽으로 **정규화해 비교**한다 (`_input_identity_problems`). 다르면 `blocked_by.inputs` 로 rc 2. 한쪽이 입력을 아예 안 적었으면(정본이 옛 스키마) 역할별 소음 대신 **"대조 불가"** 한 줄이고 rc 는 안 바꾸되 승격 자격은 없다 (`inputs_uncomparable`) | `test_e11_01` · `test_i6u_14` |
| **P1-2** | `cmd_matrix` 가 권위 명부(`HALF_FILE × SI_SOURCES × w_dqdv`, 알려진 부재 제외)를 먼저 세고 `--only-*`·`--state` 로 좁힌 실행은 status `subset` · rc 3 · `partial/` — canonical 금지. 명부에 `authority` 를 봉인 | `test_e11_02` |
| **P1-3** | `S.CANONICAL_GAMMA_GRID_N = 21` 을 정본 격자로 두고 `--grid` 가 그와 다르면 `grid_subset` → status `subset` · rc 3 · `partial/` | `test_e11_03` |
| **P1-4** | 부재 allowlist 와 **실제 파일이 모순되면 hard-fail rc 2** — 있는 것을 없다고 선언한 채로 complete 를 찍지 않는다 | `test_e11_04` |
| **P1-5** | `check_u14` 가 디렉터리뿐 아니라 **파일 단위로** `samefile` 을 본다 (data·meta 각각) — hardlink 자기대조는 `blocked_by.alias` | `test_e11_05` |
| **P1-6** | `--schema-only` 는 **구조상 언제나** `promotion_eligible: false` (`baseline_absent`); `META_REQUIRED = ("argv","roster")` 로 sidecar 의 argv·명부를 필수로 하고 명부는 본문에서 유도한 `S.body_roster` 와 대조 | `test_e11_06` · `test_e11_07` |
| **P1-7** | `ne_shape.fitted_pair_info` 가 **checker 와 같은** `S.check_rows("matrix", …)` 를 exact header 로 돌리고 문제가 있으면 RuntimeError — error 행을 과학 입력으로 쓰지 않는다 | `test_e11_08` |
| **P1-8** | 숫자 열을 **제외로** 유도(`MATRIX_NON_NUMERIC`·`PROFILE_NON_NUMERIC`)해 전부 `math.isfinite` 로 보고, degeneracy JSON 은 `_finite_problems`, 게시는 `allow_nan=False` | `test_e11_09` |
| **P1-9** | provenance 가 `--untracked-files=normal` 로 보고 **산출 root 밖 untracked 는 코드로** 센다 (안쪽은 무시 — 산출은 늘 untracked 다). `check_u14` 는 `SAFE_PROVENANCE` 값 자체를 요구 | `test_git_state_ignores_untracked_artifacts` · `test_e11_09` |
| **P1-10** | 세 러너가 gate 를 **import 하기 전에** `sys.pycache_prefix` 를 돌리고, materialize 뒤 `gate.verify_snapshot_bytes` 로 풀린 tracked bytes 를 blob object id 와 재대조(`hash-object --no-filters`) | `test_e11_10` |
| **P1-11** | R10 러너에 `child_ok(proc)` — payload 를 **읽기 전에** 자식 rc 0 을 강제 | `test_e11_11` |
| **P1-12** | R10 러너에 `COUNTEREXAMPLE_LINES` 를 두고 `_classify(fn, pkg, case_key)` 가 **그 case 의 반례 assertion 줄**에서 멈췄을 때만 "반례 소멸" — 그 밖의 AssertionError 는 오류 | `test_e11_12` |
| **P2-1** | profile 의 status→rc 계산을 sink 와 분리 — stdout 이어도 부분은 rc 3 | `test_e11_13` |
| **P2-2** | producer 가 `SHAPE_RESULT {json}` 로 **자기가 쓴 경로·run_id·status** 를 말하고 `shape_step` 이 rc ↔ status ↔ namespace ↔ run_id 를 대조한다 (못 대조하면 실패). 바깥 wrapper 는 partial 을 따로 세고 종료 코드 3 | `test_e11_14` · `test_d10_15` |
| **P2-3** | `receipt_leaves` 가 dotted top-level 역할과 **중복 논리 역할**을 거부하고, `receipt_map`·`receipt_paths` 로 역할별 path 를 따로 드러낸다 | `test_e11_15` |
| **P2-4** | `check_gamma_roster` 가 roster 를 exact JSON schema 로 parse 하고 행마다 같은지·산술이 맞는지 본다 | `test_e11_16` |
| **P2-5** | `index_skip_flags` 가 소문자와 **대문자 `S`**(skip-worktree) 를 둘 다 본다 | `test_e11_17` |
| **P2-6** | `gate.full_head` 가 **40 자 full object id 만** 받고 exact 로 대며, 증거에 `expected_tree` 를 같이 적는다 | `test_e11_18` |

### 닫힘 재생 (`reviews/r11_repros/replay_codex_r11.py`)

네 스크립트를 계약 그대로 돌리되 case 마다 **봉인한 술어**로 판정한다 — 표에 없는 case 는 닫힘으로 세지 않는다
(P1-12 가 R10 러너에서 지적한 규율을 R11 러너에 처음부터 적용). 결과: **반례 소멸 32 · 전제 변경 2 · 환경상 불가 1**.

- `publish:*` (전제 변경): 좁힌 matrix 를 canonical 자리에 안 쓰므로 원본 probe 가 그 파일을 열다 죽는다. 같은 축은
  `data:matrix_subset`·`data:profile_grid`·`root:matrix_authority` 가 따로 본다. **fingerprint 를 봉인**해 두어
  아무 예외나 전제 변경으로 읽히지 않는다.
- `root:profile_grid` (전제 변경): 원본의 "완전" 대조군이 `--grid 3` 이다 — 정본 격자가 아니면 그것도 subset 이라
  canonical 자리에 파일이 없다. 같은 축은 `data:profile_grid` 와 회귀 `test_d10_03`.
- `data:shape_wrapper` (환경상 불가): 원본이 `wsl.exe` 로 wrapper 를 부른다 (리뷰어는 Windows). 같은 축은
  `publish:shape_step` 이 native 로 재생하고 회귀 `test_e11_14` 가 고정한다.

### 이전 라운드 재생기도 같이 고쳤다 (수정이 그 probe 들의 전제를 바꿨다)

P1-2(좁힌 matrix 는 canonical 아님)와 P1-7(reader 가 공용 validator 를 쓴다)이 **우리 재생기의 적응 probe** 들을
깨뜨렸다. 셋 다 "발견이 다시 열렸다" 가 아니라 "이 fixture·자리로는 더 못 잰다" 이므로, 무엇이 대신 그 축을 보는지
같이 적고 fingerprint 를 봉인했다.

| 자리 | 무엇이 깨졌나 | 어떻게 했나 |
|---|---|---|
| `replay_codex_r7.py` R7-03 | 원본 probe 가 한 조합만 도는 matrix 를 canonical(`A.csv`)에서 읽는다 → subset 이라 파일이 없다 | `PREMISE_CHANGED` 표에 **fingerprint 와 함께** 등록 (`A.csv` + `No such file or directory` 둘 다 맞아야). 같은 축은 회귀 `test_d7_03` 이 `publish_target` 로 자리를 맞춰 본다 |
| `replay_codex_r6_adapted.py` R6-03a | `cl.matrix` 가 여섯 열짜리라 reader 가 스키마에서 먼저 멈춘다 | 값(γ 0.16 / ref 0.15)은 그대로 두고 `_full_matrix` 로 전 열을 채운다 |
| `replay_codex_r6_adapted.py` R6-04 | 원본 `matrix_independent_axes` 가 좁힌 실행을 canonical 에서 읽는다 | 이미 있던 두 개의 한 줄 적응에 **적응 ③** 을 더해 읽는 자리만 `publish_target(out, "subset")` 로 맞춘다 (관측은 그대로) |
| `replay_codex_r9.py` R9-05 | `agg.matrix_row` 가 열의 부분집합이라 중복 판정 전에 스키마에서 멈춘다 | 중복 key(γ 0.10 ↔ 0.40)는 그대로, `_full_row` 로 전 열을 채운다 |

### 수정 뒤 실측 (코드 커밋 `4185955`, 격리 snapshot)

`python3 -m pytest tests/ -q` → **202 passed** · Octave 스모크 전 단계 통과 · 변이 감사 8/8 · 적응판 5/5 ·
R6 적응판 `"mode": "full"` 6/6 · R7 5+1(전제 변경) · R9 12/12 · R10 20+1+1 · R11 32+2+1. 네 재생기 전부
`evidence_eligible: true` · `instrument_sealed: true` · `package_digest_ok: true` · `expected_tree efa727fac821…`.
`check_u14 --new out --schema-only` rc 2 — 새 스키마 누락 28(sidecar `argv` 12 + `roster` 12 + profile
`gamma_roster` 4) · 출처 열 24 · 내용 4. 전문은 `reviews/r11_repros/replay_ours_after_fixes/`.

### 계약이 바뀐 곳 (이전 라운드 회귀·fixture 를 같이 고쳤다)

| 전 | 후 | 왜 |
|---|---|---|
| `--grid N` 아무 값이나 canonical | **21 만** canonical, 나머지는 `partial/` rc 3 | P1-3 — 시험들이 속도 때문에 쓰던 `--grid 2/3` 은 정본 격자로 바꿨다 (`_args`·`_prof_args` 기본값) |
| `--only-source`·`--only-wdqdv` matrix 가 canonical | **subset** → `partial/` rc 3 | P1-2 (`_matrix_rows`·`test_r5_07` 갱신) |
| `fitted_pair_info` 가 열 몇 개만 봄 | **공용 validator 전체** | P1-7 — 부분집합 matrix fixture 가 전부 깨졌다 (`matrix_row()` 공용 helper 로 다시 씀 — **fixture 가 가리고 있던 여섯 번째**) |
| provenance `--untracked-files=no` | **normal**, 산출 root 밖은 코드 | P1-9 (`_fixture_repo` 에 production 과 같은 ignore 정책을 준다) |
| `write_meta` 가 자기 안에서 명부 유도 | `bms_balancing.schema.body_roster` **한 자리** | P1-6 — 패키지가 없는 합성 fixture 에서는 `roster: null` + `roster_error` 를 적고 승격 gate 가 막는다 (명부를 지어내지 않는다) |

### 열어 둔 것 (R11 답변이 지목한 다음 축)

- **export 계약**: full-cell + 문헌 gr/si 는 **공통 snapshot** 한 번, half-cell 은 `(source, state, sha)` 별. 아직 미구현.
- **부재 allowlist**: 코드 상수는 과도기다. versioned dataset-side manifest 로 옮겨야 한다 (모순 hard-fail 은 이번에 넣었다).
- **`evidence_eligible` 의 run receipt**: 코드 commit/tree + 러너·gate digest + 패키지 + 런타임을 한 receipt 로 묶는 것은 다음 라운드.
- **partial 수명**: `partial/<producer>/<attempt-id>/` 불변 단위 + 보존/GC 정책. 지금은 이름이 겹치면 덮인다.

## 자체 적대적 리뷰 (2026-09-13, 대상 `fbc52bb` · 코드 정본 `4185955`) — **Codex 토큰 소진 뒤 내부 6 렌즈**, 35 건

Codex 를 더 못 쓰게 되어 `/self-review` 로 6 렌즈(sig-완전성 · validator-우회 · 순서-TOCTOU · 파생-보고서 ·
archive-이식성 · 공정성-의미)를 병렬로 돌렸다. 원시 45 건 → 중복 합쳐 **35 건**, 그중 `결론이_바뀜` **14 건**.
**같은 축을 여러 렌즈가 독립으로 친 것이 셋**이다 (C01 3회 · C04 3회 · C11 3회) — 10 차에서도 그것이 진짜
구멍의 신호였다. 전부 실행된 반례가 붙어 있고, 회귀는 `tests/test_r12_selfreview.py` (f01~f28).

### 이 라운드가 드러낸 것: **직전 라운드(R11)가 "닫았다" 고 적은 것의 절반이 반쪽이었다**

| R11 에 적은 것 | 실제 |
|---|---|
| P1-1 입력 identity 비교 | 파일당 한 벌만 만들어 **마지막 행만** 비교 (C01) |
| P1-3 정본 격자 21 | `authority` 칸만 봄 — 행 수·requested 와 안 댐 (C04) |
| P1-5 hardlink alias 차단 | inode 만 봐서 `cp` 사본은 통과 (C02) |
| P1-8 유한성 | JSON 쪽은 문자열 `"1e999"` 통과 (C06) |
| P1-9 "신고된 위험을 값으로 소비" | 실은 "**키가 있을 때만** 값으로" — 지우면 통과 (C03) |
| P1-10 A import 전 격리 | pyc 만. gate 앞에 106 모듈이 저장소에서 해결 (C08) |
| P1-10 B snapshot bytes 재대조 | `instrument_sealed` 은 `--no-filters` 를 안 씀 (C07) |
| P2-2 "네 축 대조" | run_id 축은 항진명제 (C29) |

### 결론이_바뀜 14 건 — 수정

| ID | 발견 (괄호 = 독립 재현 렌즈 수) | 수정 | 테스트 |
|---|---|---|---|
| **C01** (3) | `_receipts_of` 가 행별 receipt 를 `dict.update()` 로 뭉쳐 마지막 행만 비교. production 은 행마다 입력이 다르다 (`verify.build` 가 반쪽전지 소스별 `hb.identity()` + Si 소스별 `lit_id` 를 담는다 → state 100 의 32 행에 half_cell sha 2 종 · literature.si 8 종). 양방향으로 틀렸다 — 앞 31 행이 달라도 통과하고, 순서만 뒤집힌 정당한 재실행은 거짓 불일치로 막혔다 | 행 key(`S.matrix_key`/`profile_key`) 별 `{역할: sha}` 를 만들어 key 끼리 댄다 (순서 무관) | `test_f01` |
| **C02** (2) | alias 가 inode 만 봐서 `cp -a` 바이트 동일 사본이 rc 0 · promotion true — 계산을 한 번도 안 하고 승격 증명서 | `run_id` 가 같으면 alias (독립 실행이면 시도마다 uuid4 라 같을 수 없다) | `test_f04` |
| **C03** (2) | `if k in meta` 라 위험 필드를 **지우면** 검사가 안 돌았다 — 정직하게 신고한 실행만 rc 2, 침묵한 실행은 rc 0 (게이트가 침묵에 보상) | `meta.get(k, "(없음)") != want` — 부재를 안전값으로 읽지 않는다 | `test_f05` |
| **C04** (3) | `check_gamma_roster` 가 본문과 한 번도 안 댔다 — 3 행이 "21/21" 로, 21 행이 "성공 1" 로, "γ=0.5 실패" 인데 그 행이 있어도 통과. `isinstance(True, int)` 라 bool 도 개수로 셌다 | `succeeded == len(rows)` · `requested == authority` · `missing ∩ 본문 γ == ∅` · bool 배제 | `test_f09` |
| **C05** (2) | matrix 의 모집단(`combo_roster`)이 stdout `SUMMARY` 전용 — 소비자 0, 2/32 행 묶음이 "전부 갖췄다". `out/matrix_300_0147.csv` 의 분모가 16 인 이유가 산출에 없다 | `combo_roster` 를 `MATRIX_ROW` 에 추가해 **행마다** 봉인하고 `check_combo_roster` 로 본문과 대조 (뺀 조합은 `absent` 로 명시) | `test_f10` |
| **C06** (1) | `_finite_problems` 가 `str` 을 통과 — degeneracy 의 `"1e999"`·`"Infinity"`·`"nan"` 이 문제 0. `_num_diff` 도 `float()` 라 양쪽 같으면 `inf == inf` 로 숫자 차이도 0 | 문자열도 CSV 와 같은 규칙 (파싱되면 유한해야 한다) | `test_f11` |
| **C07** (1) | `instrument_sealed` 이 `--no-filters` 없이 해싱 — committed `.gitattributes` + clean 드라이버로 **주입 코드가 든 러너**가 ok 로 봉인되고 실제로 돌았다 (`verify_snapshot_bytes` 는 이미 쓰고 있었다 = 한쪽만 닫은 비대칭) | 같은 플래그로 | `test_f12` |
| **C08** (1) | 네 러너가 gate import **전에** 106 모듈을 `sys.path[0]`(저장소 안)에서 해결 — untracked `traceback.py` 하나가 gate 보다 먼저 돌고 `INSTRUMENT` 밖. shim 이 gate 를 선주입하면 tracked 러너가 수정된 채로도 `dirty_paths: []` · `instrument: ok` · eligible true | `-P -E -B` 로 한 번 재실행 (봉인을 import 앞에). `-E` 가 `PYTHONOPTIMIZE` 를 무시하므로 재실행 **전에** `-O` 요청을 거부해 R10 P2-4 를 지킨다. 재실행은 `__main__` 일 때만 (회귀가 `exec` 로 부른다) | `test_f13` |
| **C09** (1) | 같은 구멍이 production `write_meta` 에도 — heredoc 의 `sys.path[0]` 이 `''`(cwd) 라 저장소 루트 untracked `hashlib.py` 가 `from provenance import` 보다 먼저 실행되고, 그러면 meta 에 `git_dirty: false` 가 찍힌다 (P1-9 반례 재개방) | 세 heredoc 을 `python3 -I -P -` 로 | `test_f14` |
| **C10** (1) | `.gitattributes` 가 확장자별이라 `core.autocrlf=true`(Windows 기본값)에서 **121/415 파일**이 CRLF 로 풀리고 `verify_snapshot_bytes` 가 재생기 넷을 전부 rc 2 로 — 리뷰어가 절차대로 clone 하면 증거가 하나도 안 나온다 | 맨 앞에 `* text=auto eol=lf` (보관 패키지의 `-text` 는 뒤라 그대로 이긴다) | `test_f17` |
| **C11** (3) | `rc 0` 인데 `promotion_eligible: false` 인 경로가 둘 생겼는데 `WORKING_STATE.md` 의 U18 런북은 **"0 이었을 때만 정본 교체"** — 실제 `out/` baseline 12/12 대조가 정확히 그 상태다 (`inputs_uncomparable: 16`). 오늘 U18 을 돌리면 승격 경로가 전부 여기로 온다 | 승격 자격 없음에 전용 rc **4**. 단 `--schema-only` 는 승격을 **묻지 않은** 진단이므로 0 을 유지하고 `promotion_eligible`·`baseline_absent` 가 말한다. 런북과 docstring 을 고쳤다 | `test_f18` |
| **C12** (1) | 후보 디렉터리의 `_vN` 이 명부에서 조용히 빠지고 `blocked_by` 에 `stale` 이 없었다 — 진짜 재실행(LLI 99.0)을 무시하고 옛 사본만 대조해 rc 0 · promotion true | `stale_new` 를 blocker 로 (정본 쪽 `_vN` 은 경고 그대로) | `test_f06` |
| **C13** (1) | degeneracy receipt 가 **JSON 문자열**이면 `receipt_map` 이 `{}` — 양쪽 `{}` 라 비교가 조용히 잠들고 `inputs_uncomparable` 조차 안 찍혔다 (`check_degeneracy` 도 `[]`) | `receipt_text` 로 정규화를 한 자리에 (`validate_receipt` 와 같은 규칙) | `test_f02` |
| **C14** (2) | 명부가 세 glob 만 써서 서명된 13 개 중 12 개만 셌다 — `ne_shape_*.csv` 가 게이트 밖 | 허용목록 → **배제목록** (`ARTIFACT_SUFFIXES`). "사이드카 있는 것만" 으로 좁히지 **않는다** — 서명 없는 산출이 조용히 빠지는 것은 같은 부류의 버그다 | `test_f07` |

### 숫자가_바뀜 6 건 · 서술만_바뀜 15 건 (요지)

`shape_step` 만 묶음 검사·`BMS_RUN_ID` 가 없었다(C15 → `run` 과 같게) · candidate 쪽 receipt 누락이 "정본이 옛
스키마" 사면을 받았다(C16 → 그쪽은 계약 위반) · P1-7 이 현행 정본을 reader 가 못 읽게 만든 것이 산출에 안 남았다
(C17 → `rejected_matrix` 로 남기고 짝 없음으로 센다) · `env.pandas` 를 서명에만 적고 안 댔다(C18 → `ENV_KEYS` 에)
· 러너 rc 가 `evidence_eligible` 을 안 봤다(C19 → 아니면 3) · 문서 숫자 셋이 어긋났다(C20·C26·C27) ·
docstring 의 rc 계약(C21) · `blocked_by.schema` 가 사람용에 없는 합계였다(C22 → `schema`+`provenance_cols` 로 분리)
· 보고 블록 8 개가 표시 없이 잘렸다(C23 → `_show` helper 한 자리) · 증거 `.json` 다섯 개가 유효 JSON 이 아니었다
(C24 → rc 를 `.rc.txt` 로) · `test_d10_15` 의 none 이 모순 감지 가지를 쟀다(C28) · SHAPE_RESULT 의 run_id 가
항진명제였다(C29 → 프로세스의 id) · evidence 자식이 snapshot 에 `__pycache__` 를 남겼다(C30 → 기법이 기본 자리를
요구하는 case 만 벗기고 나머지는 별도 prefix) · `bootstrap_pycache` 가 호출자 0 이었다(C31 → 삭제) ·
오류 분기가 선언한 모양을 안 지켰다(C32) · `scale_audit_*` 가 두 carve-out 에 동시에 있었다(C33) ·
재생기 workspace 가 트리 안이었다(C35 → `mkdtemp`).

### fixture 감사 — **일곱 번째**

`combo_roster` 추가와 `run_id` alias 검사, `scale_audit` carve-out 제거, `ENV_KEYS` 확장으로 **기존 fixture 20 곳
가까이가 깨졌다.** 전부 "이제야 실제 invariant 를 만족하게" 고쳤다. 특히 반복된 패턴 하나:

> 정본과 재실행 fixture 가 **같은 `run_id`** 를 쓰고 있었다 (`_matrix_unit`·`_u14_dirs`·`_deg`·d7_04·d8_02·d10_09).
> C02 를 닫기 전에는 그것이 아무 의미도 없었으므로 아무도 안 봤다. 독립 실행이면 run id 가 달라야 한다.

C01 을 R11 의 회귀가 못 잡은 이유도 같은 종류다 — `_matrix_unit` 이 `_full_matrix_rows` 를 만든 뒤 **모든 행에
같은 receipt 를 덮어썼다**. 행별 분기를 구조적으로 만들 수 없는 fixture 였다.

### 닫지 않은 것

- **C34** `receipt_paths` 에 production 소비자가 0 이다 — 원장·요청문이 "역할별 path 를 드러낸다" 고 적은 것보다
  실제 범위가 좁다. 경로를 identity 에서 빼는 것은 R6 F1/F4 의 **의도된** 결정이므로 digest 에 넣는 것이 답이
  아니고, 소비자를 붙이는 것(locator 변화를 정보 줄로)이 다음 라운드 작업이다.
- **C25** 수정 전 증거 넷 중 둘에 40-hex 커밋 id 가 없다 (그 스크립트들이 안 적는다 — 보관 패키지라 안 고친다).
- R11 답변이 지목한 다섯 축(export 공통 snapshot · dataset manifest · run receipt · partial 수명 · locator 무결성)은
  그대로 열려 있다.

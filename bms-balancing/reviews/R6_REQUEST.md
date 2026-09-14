# 적대적 리뷰 요청 — 6차 · α·β 검증 하네스 (`bms-balancing/`)

5차(대상 `0cb7b7a`)는 **NO-GO** (P1 7 · P2 4, `reviews/R5_CODEX.md`). 열한 건 전부 재현·닫음(`R5_LEDGER.md`).
그 뒤 Codex 토큰이 끊겨 6차 전반부는 **내부 자체 리뷰**로 돌렸다 (`/self-review` 4 렌즈 → 발견별 적대적 검증;
`reviews/R6_LEDGER.md`, 원본 보고·재현·판정은 `reviews/r6_repros/`). 이 요청문은 그 위에서 시작한다.
목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**. GO 기준은 R3 §5 다섯 조건 + R5 §4 재판정.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 직전 실측 커밋 `8c36e43` (U14 산출) |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). 이 요청문의 숫자는 사본 |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 5차 대비 새것 | 내부 리뷰 30 건 · U13(scale 동치) · U14(네 상태 재실행) · U15(MATLAB `sprintf` 기준선) |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
# ⚠ fresh clone 으로. autocrlf 사본을 pull 로 올리면 안 바뀐 .sh 가 CRLF 로 남아 죽는다 (R6 F6; `add --renormalize` 로는 안 고쳐진다)
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q          # 132 passed 기대. 원자료 불필요; 동시 실행 시험은 subprocess+fcntl.flock (Linux/WSL)
bash matlab/tests/run_all.sh         # Octave 없으면 4·5 단계
```

## 1. 검증 — 방금 실행, 작업트리 clean

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 테스트 | `python3 -m pytest tests/ -q` | `132 passed in 71.05s` |
| MATLAB 스모크 | `bash matlab/tests/run_all.sh` | `PASS — 실패 0: []` · `전부 통과` |
| R5 반례 | `reviews/r5_repros/*` | 전부 수정 뒤 assertion 실패 (닫힘) |
| R6 내부 반례 | `reviews/r6_repros/validator/repro_validator.py` | 9 중 **1 만 재현** = `v09`(도달 불가로 제외한 건). V6-01~08 은 안 재현 |

`reviews/r6_repros/{derived,sig_port}/repro_*.py` 는 **탐색 검사기**(성질을 찍는다)이지 회귀 assertion 이 아니다 —
문서를 고쳐도 같은 줄을 찍는다. 회귀는 `tests/test_r6_internal.py` (46 개) 가 건다.

## 2. 내부 리뷰 30 건 — 대응

### 2a. validator 우회 (`r6_repros/validator/`) — 9 → CONFIRMED 8

공통 반례: MATLAB rmse 가 Python 과 상대차 1e-3~1e-2 (`MODEL_REL` 의 10⁶ 배) 인데 `%.2g` 로는 같은 문자열.

| ID | 무엇 | 수정 | 테스트 |
|---|---|---|---|
| V6-01 | 헤더가 데이터 행 **뒤**면 행별 검사(R4-04·R5-01)가 한 번도 안 돌아 complete·0 | `dd_eval_csv_audit`: 헤더 앞 데이터 행 = malformed | `test_i6v_01` |
| V6-02 | `--precision` 옵션이 토큰과 대조되지 않아 **선언 없는 파일이 선언된 파일보다 관대** (`sig:2` + 17 자리 → 0; 선언 `%.17g` 면 같은 옵션이 3) | 선언 없으면 옵션 형식으로 재출력 검사 (`spec_label="옵션 형식"`) | `test_i6v_02`×3 |
| V6-03 | 헤더 없는 파일 = `dd_eval.m` 첫 판(`56a35a8:118`)부터 존재한 적 없는 스키마인데 partial → `--allow-partial` 로 0 | 헤더 없음 = malformed | `test_i6v_03` |
| V6-04 | "스키마 누락" 에 하한 없음 — rmse 열 0·앵커 0 이어도 "전부 일치" 0 (`compared=0/0`) | `OLD_SCHEMA_MIN_COLS=(rmse_pocv, rmse_dvdq)` 없으면 invalid | `test_i6v_04` |
| V6-05 | `verify_unit` 이 meta 의 `artifact` 이름을 안 봐 다른 상태 이름으로 복사해도 '일치' | 이름 결속 | `test_i6v_05` |
| V6-06 | `# printed_format,17` 이 '선언 없음(추정)' 으로 흘러 invalid 가 아니었다 | `read_dd_eval_meta` 가 값과 무관하게 선언으로 읽음 (R5-02 를 meta 리더에도) | `test_i6v_06` |
| V6-07 | 못 읽는 `--compare` 경로가 traceback rc 1 = README 의 "갈림" | OSError → invalid(2) | `test_i6v_07` |
| V6-08 | `run_id` 열 중복 시 `DictReader` 마지막 열만 | 헤더의 `run_id` 가 정확히 하나 | `test_i6v_08` |
| V6-09 | `%f` ±0 토큰 경계 | **제외** — rmse=`sqrt(mean(r²))` 라 음수·-0 생산 불가 (도달 불가) | — |

### 2b. 순서/TOCTOU (`r6_repros/toctou/`) — 9 → CONFIRMED 8

| ID | 무엇 | 수정 | 테스트 |
|---|---|---|---|
| **F01** | degeneracy `.part` 가 고정 이름 **이자 producer 의 stdout fd** — 빠른 A 가 게시·meta·verify-unit 을 전부 통과한 뒤 느린 B 가 rename 된 inode(=게시 파일)에 잠금 밖에서 쓴다 → JSON=B·meta=A, 두 wrapper 다 "통과". **R5-04 의 "마지막 온전한 묶음만 남는다" 가 이 경로에서 거짓** | `cmd_degeneracy --out` + `atomic_write_json`(고유 임시·`publish_lock` 안 교체); shell 은 matrix 와 같은 형태, `flock` 사용 소멸 | `test_i6t_01` (실제 두 process, `run_states.sh` 블록 원문) |
| F02 | `ne_shape._write_csv` 비원자·잠금·run_id·sha256 없음 → CSV=B·meta=A, `verify_unit` 이 '옛 meta' 라 검출 불가 | 같은 게시 규약 + 행 `run_id` | `test_i6t_02` |
| F03 | `fitted_pair_info` 가 파싱 뒤 해시를 위해 다시 연다 | bytes 한 번 읽어 그것을 파싱·해시 | `test_i6t_03` |
| F04 | git 상태가 계산 **뒤** 한 번 샘플 (10 시간 실행 중 checkout/커밋이면 거짓) | `git_*_at_start`·`started_utc`·`git_state_changed_during_run` | `test_i6t_04` |
| F05a/b | `--verify-unit` 이 이 시도의 id 를 안 받음 / 실패 이유를 `>/dev/null` 로 버림 | `verify_unit(path, rid)`·CLI 인자 / `verify_unit_or_say` | `test_i6t_05a`·`05b` |
| F06 | `.lock`·시도별 `.part` 가 `.gitignore` 밖 (`git clean -fd` 가 보유 중 잠금을 지우면 배타 소멸) | `out/**/*.lock`·`out/**/*.part` | `test_i6t_06` |
| F07 | reader 가 묶음을 안 봄 — **R5-04 최소 조건의 reader 절 미구현** | `compare_states` 는 경고+제외, `fitted_pair_info` 는 RuntimeError | `test_i6t_07` |
| F08 | `run_id` 가 공개 열이라 복사한 producer 는 모든 검사 통과 | **신뢰 경계** (§4) | — |

### 2c. 파생 보고서·공정성 (`r6_repros/derived/`) — 10 → CONFIRMED 8 · 부분 2 (전부 문서 정정)

| ID | 무엇 | 테스트 |
|---|---|---|
| **DF-01** | §3-4 "두 독립 방법이 수렴" — 힌트 격자(`pad=폭/2`, 21 점)의 `grid[5]`·`grid[15]` 가 제약 최적화의 min·max **그 자체**. LLI 의 '정확히 일치' 는 같은 격자점 반환이고 세 mode 모두 `profile.max == ext.max` 가 비트 일치 → "끝점 재확인, 독립 수렴 아님" 으로 정정. 폭 1.0832·`is_lower_bound` 는 불변 | `test_i6d_01` (artifact 로 격자 재구성) |
| DF-02 | HANDOFF §5·INTRO §6-2 에 §0-2 철회 결론 7 곳 잔존 (같은 문서의 정정판과 모순) | `test_i6d_02` |
| DF-03 | "raw 로 5~10 배" — 어느 통계량도 아님 (max/max 10.52·min/min 9.66·med 10.04; 상태별 쌍 5.1~18.3) | `test_i6d_03` |
| DF-04 | 문서의 "N passed 기대" 가 트리와 어긋남 | `test_i6d_04` (수집 수와 대조) |
| DF-05 | U13 을 "192 값의 조건" 에 묶음 — 192 값은 raw rmse 라 `scales` 를 소비하지 않는다 (`__call__` 만) | `test_i6d_05` |
| DF-06 | §4-0 "6·17·전부 w=1" 은 상대 1e-9 문턱에서만 (부호만 보면 10·22·0) | `test_i6d_06` |
| DF-07 | §1-10 에 탐색 하한 한정어 없음 (네 JSON 모두 `is_lower_bound: true`) | `test_i6d_07` |
| DF-08·09·10 | §4-1 2.11→2.10 · §3-3 인용을 `_v2` 로 · INTRO §6-3 "n=1 …산수다" 는 §7-3 이 철회 | `test_i6d_08`~`10` |

### 2d. sig-완전성·이식성 (`r6_repros/sig_port/`) — 11 → CONFIRMED 8 · 부분 3

| ID | 무엇 | 수정 | 테스트 |
|---|---|---|---|
| F4 | `build` 가 읽는 **풀셀 워크북**은 폴더의 이름순 첫 xlsx 인데 이름·sha256 이 어디에도 없다 (사본 하나로 scale 이 바뀌어도 `data_root`·run_id·commit 은 그대로) | `Objective.consumed_inputs`(반쪽전지·풀셀·문헌 Si/Gr 경로+sha256) + `inputs_sha`; JSON·matrix/profile 행·eval 헤더에 | `test_i6p_04` |
| F3 | 라이브러리 버전 미기록 — scipy 1.11↔1.17 에서 `savgol_filter` 13/500 ULP → L-BFGS-B 최적점 다름 | `provenance.env_signature()` 를 meta·JSON·eval 헤더 `# env,…` 에 | `test_i6p_03` |
| F1 | `root=<basename>` 이 공백에서 사본 파서(`\S+`)를 깨고 같은 basename 을 못 가름 | `scale_audit_line`: URL 인코딩 + `inputs=<digest>` | `test_i6p_01` |
| F5 | `--profile-scale`·`--samples/--grid` 가 산출에 없음 (같은 run_id·같은 스키마에 obj 0.8895↔1.2542) | 행 `profile_scale`, JSON `n_grid`·`n_samples` | `test_i6p_05` |
| F7 | `git_provenance` 가 호출자 cwd 기준 (같은 산출이 False/True/None) | 기본 base = 스크립트의 저장소 | `test_i6p_07` |
| F9 | 비-UTF-8 기본에서 `check_artifact`·CLI 크래시 | `encoding="utf-8"`, stdout `backslashreplace` | `test_i6p_09` |
| F10 | ENOLCK 면 계산 행 전부 소실 | `_publish_or_keep`: `.part` 보존 + 경로를 예외에 | `test_i6p_10` |
| F8·F2·F6·F11 | flock 부재 / 루트 차원 / autocrlf 사본 / 옛 수치 | F01 수정으로 소멸 · §4 신뢰 경계 · 요청문 §0 · DF-04·F06 | — |

## 3. 사용자 기계 실측 (U13 · U15 · U14)

| # | 무엇 | 결과 |
|---|---|---|
| U13 | scale 동치 조건 (`eval` 감사 줄 18 build) | 전부 유한·예외 0·`eps_rel` 4.7e-16~1.7e-15 ≪ 1e-9 → `equiv=1`. 사본 `out/scale_audit_eval_u13.txt` |
| U15 | R5-01 의 미검증 전제 (MATLAB `sprintf` ↔ Python `format`) | `sprintf('%.2f',0.125)`=`'0.12'`(half-to-even, 일치) · `sprintf('%.17g',1e-5)`=`'1.0000000000000001e-05'`(2 자리 지수, 일치). 기준선 `MATLAB_SPRINTF` 로 고정 (`test_i6u_15`). **범위**: 표본 둘·MATLAB 판 하나 |
| **U14** | 새 게시·서명 스키마로 **네 상태 재실행** (`STARTS=24`, 12 산출) | 아래 |

### U14 판정 — 결론 숫자는 전부 재현됐다

`python3 scripts/check_u14.py --new out --old-rev bfc4623^` (환경: python 3.12.3 · numpy 2.5.3 · scipy 1.18.1 ·
pandas 3.0.5 · WSL2. 정본을 만든 조합은 그 산출에 `env` 가 없어 **모른다** — F3 의 요지가 그것이다).

| 대상 | 최대 상대차 |
|---|---|
| `matrix_100·200·300_0147.csv` 전 셀 | **0.00e+00** |
| `matrix_300_0009.csv` ↔ 옛 `_v2` | **0.00e+00** (재실행이 v2 를 재현) |
| `degeneracy_*` 세 mode `span` (§1-10 A축) | **0.00e+00** |
| `profile_gamma_*.csv` 개별 행 | LAM_NE 2.8e-2 · b_NE 3.6e-1 · rmse_pocv 2.1e-2 |
| §5-1 문턱 표 (8·10·11·12 mV) | n 6/10/12/13 **동일** · 최악 비 동일 · 폭 13.5860→13.5859 |

~~`degeneracy`·`matrix` 는 multistart 24 시작이라 국소 해가 안정적이고, `profile` 은 γ 마다 등식 제약을 적은 시작으로
푸는 구조라 입력의 ULP 차이가 다른 국소 최적점으로 간다~~ — **Codex R6-06 정정**: `profile` 은 γ당 25 회(`best[:4]` +
무작위 24) 4변수 L-BFGS-B 다; 움직임은 같은 예산 안의 국소 해 갈림이다 (`reviews/R6_LEDGER.md` U14 판정).
**F3 가 야생에서 확인됐고 영향은 갇혀 있다.** 어떤 결론도 뒤집히지 않았다.

U14 실행이 드러낸 다섯 건 (전부 닫음):

| ID | 무엇 | 수정 | 테스트 |
|---|---|---|---|
| **U14-01** | `atomic_write_csv` 가 CRLF 를 쓰고 `.gitattributes` 가 csv 를 안 덮어 git 은 LF 로 저장 → **fresh clone 에서 meta 의 sha256 이 안 맞고 F07 의 reader 검사가 그 상태를 §1-10 표에서 뺀다** | writer LF · `*.csv`/`*.json text eol=lf` · `verify_unit` 이 "줄끝만 다르다" 를 짚음 · 게시된 것은 `check_u14.py --renormalize`(줄끝 변형과 맞을 때만 재서명) | `test_i6w_01`·`02`·`04`·`05` |
| U14-02 | `check_u14` 가 정본을 이름으로만 골라 v1 과 댐 + 새 필드를 diff 로 셈 → 거짓 "618 건" | `baseline_for`(가장 높은 판) · "정본에 없던 필드" 분리 · `--old-rev` | `test_i6w_03`·`06` |
| U14-03 | F02 가 더한 `run_id` 열을 소비 helper 가 `float()` 로 읽어 깨짐. **이 트리에서 안 깨진 이유**: 커밋된 산출이 옛 스키마라 fixture 가 가림 | `NE_SHAPE_TEXT_COLS` + helper 를 경로 인자로 | `test_i6w_07` |
| U14-04 | rebase 충돌 표식이 CSV 에 박혀 `KeyError` 여덟 개로 나옴 | 산출의 충돌 표식 감지 | `test_i6w_08` |
| U14-05 | 재실행이 `out/matrix_300_0009.csv` 를 덮었는데 그 자리가 §4-0 이 "고치기 **전**" 으로 인용하는 v1 (새 파일 ↔ 옛 v1 4.17e-01) | `out/archive/matrix_300_0009_premultistart.csv` 로 보존(+README); §4-0·§3-3 인용·테스트 둘을 그쪽으로. archive 는 비재귀 glob 에 안 걸림 | `test_i6d_06`·`09` |

## 4. 닫지 않은 것 — 신뢰 경계

| # | 무엇 | 왜 열어 두나 |
|---|---|---|
| F08 | `run_id` 는 게시 파일의 공개 열 — 복사해 게시하는 producer 는 모든 검사를 통과 | 문서의 위협 모델은 "각자 uuid 인 다른 시도" 이고 소유 증명을 주장한 적 없다. 닫으려면 producer 가 자기 bytes 의 sha256 을 stdout 으로 넘겨 write_meta 가 대조 |
| F2 | U13/U14 의 **루트 차원**은 사본으로 검증 불가 (위조 사본이 테스트 통과) | §1-13 이 이미 "보고 순서" 로 한정. `inputs_sha` 가 붙은 다음 실측부터 루트 집합을 센다 |
| V6-09 | `%f` ±0 토큰 경계 | rmse=`sqrt(mean(r²))` 라 도달 불가 |
| U16 | U14 의 프로파일 차이가 **scipy 판 때문인가** | 가설이다. 정본 조합을 모르므로(그 산출에 `env` 없음) 같은 기계에서 옛 조합으로 한 번 더 돌려야 닫힌다 |
| U2~U10 | 전과 같음 | — |

## 5. 지금 정본이 말하는 것 — 범위를 붙인 다섯 관측 (R5 Q5 반영, 변동 없음)

| 관측 | 붙인 범위 |
|---|---|
| 포팅 일치 | 보존된 네 조합 **192 출력값**의 경험적 일치. scale 동치는 유한·예외 없음·`eps_rel ≤ 1e-9` 의 상대 근사(U13) — **적합 산출의 목적함수** 조건이고 192 값(raw rmse)의 조건이 아니다 (DF-05). 형식 대조 전제는 U15 |
| 음수 LAM_NE | 공개 5 행·고정 기준의 부호 산술, 행별 임계. 경계 변경 재적합의 인과 미확립 |
| 파우치 폭 순위 | 네 상태·소스·설정의 **탐색 하한** 순위 4/4 (DF-07). 식별성·정확도 보장 아님 |
| 원통형/PE 대조·재척도화 | 명시한 소스 집합·분모·통계량의 기술값 (raw max/max 10.5 배, DF-03). 원인 배제·공유 가능값 증명 아님 |
| 잔차·γ 변화 | 상태별 RMSE 증가·선택된 쌍의 진폭비·γ_ref 고정 격자 여유(진폭 증인). 원인·보상 경로는 가설. §3-4 의 두 방법은 **독립 수렴이 아니라 끝점 재확인** (DF-01) |

## 6. 질문

1. **F01 이후의 게시 규약**: degeneracy 를 stdout 에서 떼어 `--out`+`publish_lock` 으로 옮겼다. 산출·meta·`--verify-unit`(시도 id 포함)·reader 검사(F07)까지 걸었을 때 남는 창이 있는가. 동시 실행을 **거부하지 않고** "마지막 온전한 묶음" 을 유지하는 선택이 맞는가 — 거부로 바꾸면 되돌릴 수 있다.
2. **F08 의 위협 모델**: 게시 파일에서 읽은 id 로 만든 묶음까지 가려야 하는가. 가린다면 producer 의 bytes 해시를 stdout 으로 넘기는 설계로 충분한가.
3. **V6-02 의 규칙**: "선언 없으면 옵션 형식으로 토큰 재출력 검사, 선언 있으면 선언으로 검사하고 충돌은 partial" 에 남는 역전이 있는가.
4. **DF-01 정정문**: 힌트 격자가 제약 최적화의 끝점을 격자점으로 포함하므로 "독립 수렴" 을 "끝점 재확인" 으로 낮췄다. §3-3 의 폭 1.0832 를 믿을 근거로 이것이 충분한가, 힌트 없는 격자 재실행이 필요한가.
5. **U14 의 프로파일 차이**: 결론 숫자는 0.00e+00 인데 γ 프로파일 개별 행이 최대 2.8e-2 움직였다. 이 상태에서 §5·§5-1 을 인용해도 되는가, 아니면 profile 도 multistart 예산을 올려 안정화해야 하는가 (U16 과 묶어).
6. **§5 의 다섯 관측**을 새 모델 요구서의 관측 열로 옮기는 데 남은 문제.

## 7. 실측 첨부

- `reviews/r6_repros/{validator,toctou,derived,sig_port}/` — 렌즈 보고(`REPORT.md`)·재현(`repro_*.py`)·적대적 검증 판정(`VERDICT.md`)·검증 스크립트.
- `out/scale_audit_eval_u13.txt` (U13 18 줄) · `out/archive/` (U14-05 로 보존한 수정 전 산출 + README).
- U14 산출 12 개는 `out/` 에 새 스키마(`run_id`·`sha256`·`env`·`inputs_sha`·시작 시점 git)로 들어 있다.

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안 — §5 의 다섯 행을 관측 열로. 문헌 입력은
`docs/LIT_19_20_FOR_NEW_MODEL.md` (논문 19 무율 도금 · 20 LFP 직접 진단의 관측·구분 시험·라벨 출처).

# KG50R-F01 고침 증거 — 준비 구간 그 자리 치환 값 (10-30 · Codex KG50RF-01 · P1 · 1저자 Q1 "권고대로")

> ⚠ 10-30 정정 2 건 (독립 사전 공격이 찾은 서술 어긋남) = 맨 끝 §13 · 2 판 (사전 공격 R1–R8 고침 · F02 통합) 증거 = [`r2/`](r2/README.md).  아래 본문은 첫 판 기록 그대로다.

## 0. 판 · 커밋 · 범위

| 무엇 | 값 |
|---|---|
| 고치기 전 판 | `scripts/resume_ckpt.sh` sha256 `77c242375c4093023e609703ef471c64c2370d374e7533824412d96da5b1b9f8` (= 기준 커밋 `bf8cf21c6` · Codex 검토 묶음 `PIN.txt` 의 리뷰 핀 `bf8cf21c6466…` 과 같은 커밋 · 같은 sha256) |
| 시험 먼저 커밋 | `f3cbdc6f3` — `scripts/test_resume_ckpt.py` 에 V 묶음 76 만 더함 (221 줄 더함 · 지운 줄 0 · 기존 시험 · 기대 안 바꿈 · 묶음은 `main()` 끝 요약 줄 바로 앞).  ⚠ 작업 순서: V34–V40 · V9 의 글 조각 하나는 고친 판의 첫 판이 있은 뒤 더했다 (내 첫 고침의 빈틈 · 변이 생존을 잡으려고 — §8) · 커밋은 로컬에서 시험 → 고침 → 증거 순으로 다시 묶었다 (push 없음).  76 개 전부가 고치기 전 판에서 FAIL (V1e · V1f · V1g 대조군 셋 빼고) 인 것 = §5 · §7 |
| 고침 커밋 | `f4346cf69` — 고친 판 sha256 `38e1eff54d396c6607eb9c1f04d3b048862e23e31a604f34fedc59b6d90e2992` (430 줄 더함 · 41 줄 지움 · 이 파일만) |
| 고친 곳 | 내장 Python 정적 대조 (`deckcheck(){ python3 - … <<'PY'` ~ `PY` 사이) 만 — `words`/`wpos` · `run_state` (src) · `setup_order` (짝을 돌려줌) · `state_cmp` · 새 함수 (`isubs` · `show` · `xfmt` · `mark_end` · `word_end` · `bare` · `fwhy` · `expand` · `sub_text` · `nested` · `var_env` · `xline` · `xstate` · `setup_values`) · `check()` 의 부르는 자리 · 머리 주석 두 줄.  바뀐 줄은 전부 그 heredoc 안 (옛 판 57–1033 행 · 새 판 57–1422 행) — 셸 러너 · 시도 폴더 · 영수증 · 본 제출 구역 (다른 작업 트리가 고치는 곳) 은 안 건드림 |
| 환경 | 이 리포의 클라우드 컨테이너 (Linux · GNU bash 5.2.21) · 가짜 SLURM · 가짜 `dem_restart.py` (시험 안 stub) — 실제 ibb SLURM · LIGGGHTS 실행 없음 |

## 1. 결함 (Codex 판정문 §1 · 원장 KG50R-F01)

정적 대조 (`-C` · 본 흐름의 시험 전 대조) 가 준비 구간을 **순서 보존 부분열 (`setup_order`) + 끝 상태 글자 (`state_cmp`)** 로만 봤다.  LIGGGHTS 는 따옴표 밖 `${x}` · `$x` 를 **그 줄을 읽는 순간** x 의 그때 값으로 바꾸고 (equal = 그때 계산한 수를 `%.15g` · string = 글), equal 수식 안 `v_y` 는 쓸 때 계산한다 (고정판 `3d5c00f` 의 `doc/variable.txt` · `src/input.cpp` `Input::substitute` · `src/variable.cpp` `Variable::retrieve` — 의미 확인용으로만 읽음).  그래서 다음 둘이 통과했다 (rc 0 · 문제 0).

1. **중간 정의를 뺀 재개 덱** — 본 덱 `g_probe 98.1 → 196.2 → fix gravi … ${g_probe} → 98.1` · 재개 덱은 `196.2` 줄만 뺌 → fix 가 받는 중력 196.2 ↔ 98.1 (끝 상태 글자는 같다)
2. **실행 상태에 따라 바뀌는 즉시 치환** — 두 덱 같은 `variable g_probe equal 98.1*(step+1)` · `fix … ${g_probe}` → 본 덱 step 1 ↔ 재개 덱 step 20001 에서 계산

같은 뿌리: `state_cmp` 가 변수 정의를 원 글자로 대조해 `variable b equal ${a}*2` 의 a 가 정의 때 달라도 같다고 봤다.

## 2. 고친 것 — 1저자 10-30 Q1 규칙 (1)–(5) ↔ 코드

| 규칙 | 코드 | 한 일 |
|---|---|---|
| (1) 준비 구간 명령의 그 자리 치환 | `setup_values` · `setup_order` · `check()` 의 템플릿 짝 | 재개 덱 준비 구간 (`setup_check` · `setup_order` 가 보는 같은 구간 · 템플릿 fix · `variable` 포함) 명령마다 따옴표 밖 `${x}` · `$c` 를 두 덱에서 펼친다 — 본 덱 = `setup_order` 가 맞춘 체크포인트 앞 명령 자리 · 재개 덱 = 그 명령 자리.  펼침 = 그 자리의 정의 (정의 안 `${}` · `$c` = 정의 줄 자리 값 · equal 수식의 `v_y` = 쓰는 자리 정의).  두 펼침의 글자가 같고 상수일 때만 통과 · 통과하면 기록 줄 `그 자리 치환 대조 (10-30 KG50R-F01): 명령 N 개 · 치환 M 곳 = 두 덱 같은 상수 값` |
| (2) 상수 | `fwhy` · `expand` | 수 · `+ - * / % ^` · `== != < <= > >=` · 괄호 · 쉼표 · 공백 · `sqrt exp ln log abs sin cos tan asin acos atan atan2 ceil floor round` (고정판 doc 의 math functions 중 결정형 · 고정판 doc 대조) · 상수 변수 · string 글.  그 밖 = 거부: thermo 낱말 (`step` · `time` · `dt` · `atoms` · `ke` …) · group · region · special 함수 (`count()` · `bound()` …) · 원자 값 · `c_` · `f_` · 상수 아닌 변수의 `v_` · `random normal ramp stagger logfreq stride vdisplace swiggle cwiggle` · `PI` · `&& \|\| !` |
| (3) 끝 상태 = 펼친 정의 | `xstate` · `state_cmp` · `run_state(src)` | 끝 상태 표 (변수만이 아니라 fix · timestep · region · neigh_modify … 전부) 를 **정의 자리의 그 자리 치환으로 펼친 줄**로 대조 — 원 글자가 같아도 펼친 줄이 다르면 거부.  끝 자리 앞에 흐름 · 변수 바꾸는 줄 (아래 (4)) 이 있으면 끝 상태 변수 표 = 못 정함 (재개 덱이 다시 선언한 변수 = 거부).  판 메시 file 이름만 다름 허용 = 펼친 줄도 file 이름만 다를 때 |
| (4) 못 펼침 = 거부 (닫힌 실패) | `isubs` · `sub_text` · `var_env` · `nested` | `$(...)` · `}` 없는 `${` · `$` 뒤 이름 글자 아님 · equal · string 밖 변수 꼴 (atom · index …) · 정의 없음 · 순환 · string 값에 공백 · 따옴표 · `v_` 로 쓰는 string 이 수 글 아님 · 그 자리 앞의 흐름 · 변수 바꾸는 줄 (`label` · `jump` · `next` · `python` · `partition` · `if` · `run … every` 안 (겹친 것까지) 그런 줄 · `variable` · `variable` 이름 · 꼴 자리 치환 · 못 읽는 `variable` 줄).  문제 줄 머리 `준비 구간 그 자리 치환을 펼칠 수 없음 (10-30 KG50R-F01 · 닫힌 실패)` |
| (5) 값 대조 밖 | `setup_values` 앞머리 | `print` · `if` (print · quit 만) · `shell mkdir` — 실제 덱의 삽입 수 검사 (`variable n_ins equal count(all)` + `print` · `if` 의 `${n_ins}`) 그대로 통과 (V1) |

문제 줄 표기: `⟦…⟧` = equal 값 (그 수식) · `⟨…⟩` = 정의 때 실행 상태 값 · 못 펼침 (덱 · 자리를 담아 두 덱에서 늘 다르다).

## 3. 해석 선택 (보고 · 1저자 확인 거리)

1. **상수 목록 = 엄격** — `PI` · `&& || !` 는 결정형이지만 등록 목록에 없어 거부 (V23 · V24) · `%` (나머지 · 고정판 `variable.cpp` 1514 행 `MODULO` 에 있음 · `doc/variable.txt` 343 행 연산자 표에는 없음) 는 산술로 받음 · 비교 6 개 받음 (V19).  수학 함수 목록 = 고정판 doc 344 행의 24 개 중 결정형 15 개 (나머지 9 = `random` · `normal` · `ramp` · `stagger` · `logfreq` · `stride` · `vdisplace` · `swiggle` · `cwiggle` = 거부).
2. **"글자 같음"** = `deck()` 정리 뒤 글 (공백 하나) — 같은 수를 내는 다른 글 (`2*3` ↔ `6`) 은 거부 (보수 쪽).
3. **그 자리 치환 판별** = 고정판 `Input::substitute` 와 같게 (`input.cpp` 457–531 행 — `"` · `'` 를 따로 뒤집어 둘 다 밖일 때의 `$` 만 · 치환한 글은 다시 읽지 않음 · 치환은 낱말 나누기 앞 = 369 · 374 행) — 따옴표 안 `${}` 는 그 자리 치환 아님 (V18) · 따옴표 안 다른 따옴표도 LIGGGHTS 처럼 따로 뒤집는다 (자기 공격 A37–A40: 하나면 그 뒤 `${x}` 를 치환 안 함 = 받음 · 둘이면 치환 = 값 다름 거부).  따옴표 안에 `$` 가 남은 equal 을 `${}` 로 쓰면 = 상수 아님으로 거부 (`모르는 글자 '$'` · LIGGGHTS 도 계산 때 `Invalid syntax in variable formula` = `variable.cpp` 1647 행 · 자기 공격 A5).
4. **템플릿 fix 의 본 덱 자리** = 본 덱 끝 상태의 그 fix 줄 (글자 같을 때) — `setup_order` 는 템플릿을 빼고 맞추므로 규칙 (1) 의 "같은 짝" 이 없는 자리.  체크포인트에 남는 정의가 그 줄이다 (V8).
5. **규칙 (3) 을 상태 표 전부에** (변수만이 아니라 fix · timestep · neigh_modify · region … — 자기 공격 A33 · A34 의 `재개 지점 neigh_modify` · `region rb` 줄) — 같은 글자 줄이 본 덱에 둘이면 규칙 (1) 은 앞 것 자리에 맞춰지고 끝 상태 = 뒤 것이라 규칙 (3) 만 잡는다 (V12 fix · V13 변수 · V26 판 메시 · 자기 공격 A7 timestep · A17 unfix 뒤 다시 fix).
6. **흐름 · 변수 바꾸는 줄 = 그 자리 뒤 펼침 거부** — 쓰이지 않는 `label` 도 (보수 쪽).  "모든 자리" (뒤의 흐름 줄이 앞 자리까지) 는 두지 않음: 어떤 자리의 값을 바꾸는 반복은 그 자리 앞에 `label`, 앞으로 건너뛰기는 그 자리 앞에 `jump` 가 있다.  끝 상태 변수 표는 끝 자리라 그 앞 어디든 그런 줄이 있으면 못 정함 (V36).
7. **string** — 따옴표 밖에 넣는 string 에 공백 · 따옴표 = 거부 (V20 · LIGGGHTS 는 치환한 뒤 낱말을 나누므로 `fix … gravity ${g_s}` 가 `98.1 vector 0.0 0.0 -1.0` 네 낱말로 갈라져 돌 수도 있다 = 닫힌 쪽) · `v_` 로 쓰는 string = 수 글 (V30) 이나 정의 때 넣은 equal 값 하나 (V31) 만 (LIGGGHTS `atof`).
8. **예외 안 둠** — §4.
9. **문제 줄이 둘 이상 나올 수 있음** — 같은 결함을 규칙 (1) (명령 자리) 과 (3) (끝 상태) 이 같이 본다.  기존 시험의 문제 수 (C1 `(문제 2)` · Y16 `(문제 1)`) 와 Q5 등록 §12-4 기대 문제 줄 (W1 넷 · W2 넷 = `kg50_q5_branches.py` 의 `EXPECTED_STATIC_W1` · `_W2` · 글자 · 순서 대조) 은 그대로 (§9).

## 4. after_settling 예외 — 넣지 않음 (근거 = 실측)

규칙 (2) 의 예외 (체크포인트 step 에서 돈 본 덱 명령의 실행 상태 값) 는 "보관 after_settling 기준선이 실제로 필요하면" 이었다.  필요 없다:

- 기준선 = Codex `archived_after_settling_baseline` = 리포 `docs/reviews/codex_kg50_resume_recheck_20261028/independent/deck/after_settling_baseline.liggghts` + v2 본 덱 (`docs/data/kg50_decks_20261026_v2/kg50_d07_b40/input_kg50_d07_b40.liggghts`) — Codex 사례 폴더의 두 덱과 줄 끝 (CRLF) 만 다르다 (`\r` 뺀 diff = 없음).
- write_restart 체크포인트의 뒤 구간 = 본 덱 `write_restart … after_settling.bin` 다음 명령부터 (`pM = ia + 1`) — 판 높이 블록 (`run 1` · `variable z_max equal c_zmax` · `variable plate_z equal ${z_max}+${r_AM_P}+${plate_margin}` · 판 STL `print`) 이 여기 있어 `seq_cmp` 가 명령 하나하나 대조한다 (두 덱 같은 step 200001 → 200002 에서 실행).  준비 구간 (`R[:q]`) 이 아니다.
- 그 기준선의 준비 구간 그 자리 치환 = `timestep ${dt}` · 템플릿 셋 (`${r_AM_P}` · `${r_AM_S}` · `${r_SE}`) — 전부 상수.  고친 판 `-C` = rc 0 · `통과 (문제 0)` · 기록 줄 `명령 4 개 · 치환 4 곳` (V1b · Codex 사례 폴더 그대로도 rc 0 · §6).
- v3 50×50 after_settling (V1c · 본 흐름 V1g) · 받은 D2 (V1 · V1e) 도 예외 없이 통과 · Q5 W1 · W2 가지의 기대 문제 줄 (등록 §12-4) 그대로 (§9).

## 5. 결과 — 환경별 (로그 끝 줄 그대로)

| 환경 | 고치기 전 판 + 최종 시험 (`--script <옛 판>`) | 고친 판 |
|---|---|---|
| Python 3.11.15 · awk = mawk 1.3.4 20240123 (시스템) | `219 PASS · 73 FAIL` (rc 1) | `292 PASS · 0 FAIL` (rc 0) |
| Python 3.11.15 · awk = GNU Awk 5.2.1 (스크래치 .deb 의 gawk 를 `awk` 이름으로 PATH 앞 · 시스템 awk 그대로) | `219 PASS · 73 FAIL` (rc 1) | `292 PASS · 0 FAIL` (rc 0) |
| 지시받은 명령 `python3.8 -I scripts/test_resume_ckpt.py` (시험 틀 3.8.20 · 도구 내장 Python = PATH 의 `python3` 3.11.15) · mawk | `219 PASS · 73 FAIL` (rc 1) | `292 PASS · 0 FAIL` (rc 0) |
| 시험 틀 3.8.20 + 도구 내장 Python 도 3.8.20 (`python3` → `python3.8` 고리를 둔 폴더를 PATH 앞 · `python3 --version` = 3.8.20) · mawk | `219 PASS · 73 FAIL` (rc 1) | `292 PASS · 0 FAIL` (rc 0) |

- 고치기 전 73 FAIL = 전부 V (기존 216 = 네 환경 모두 통과) · V 통과 3 = 본 흐름 대조군 (V1e · V1f · V1g).
- 고친 판 로그 넷 = 바이트 같음 (sha256 `b07f90948cc7e27b…`) · 고치기 전 로그 넷은 FAIL 줄의 임시 폴더 이름만 다르다.
- 디스크 가득 (`No space left` · `Errno 28`) 줄 = 0 (이 폴더의 로그 전부).  작업 중 컨테이너 디스크가 가득 찼던 때 (컨테이너 시계 10-29 22:33 UTC 무렵) 돈 판은 버렸다 — 이 표의 판은 그 뒤에 돌렸고, 러너 `run_envs.sh` 는 로그에 그 줄이 있으면 다시 돈다 (다시 돈 횟수 0 · `run_summary.txt`).
- 이 표의 판 = 커밋된 시험 · 도구 그대로 (시험 마지막 고침 23:21 UTC · 도구 마지막 고침 22:47 UTC 뒤에 돌림 · 지금 작업 트리 `scripts/` 변경 없음).

## 6. Codex 사례 여섯 (`-C` · Codex `independent/program/cases/` 고정물 읽기만 · 작업 폴더 = 내 스크래치)

| 사례 | 체크포인트 · S0 | 고치기 전 | 고친 판 |
|---|---|---|---|
| `d2_drop_intermediate_variable_definition` | `restart_kg50_d2_b50/restart_settling_20001.bin` · 20001 | rc 0 · 통과 (문제 0) | rc 1 · 실패 (문제 2) |
| `d2_runtime_dependent_eager_variable` | 같음 | rc 0 · 통과 (문제 0) | rc 1 · 실패 (문제 2) |
| `drop_intermediate_variable_definition` | `restart_settling_50.bin` · 50 | rc 0 · 통과 (문제 0) | rc 1 · 실패 (문제 2) |
| `runtime_dependent_eager_variable` | 같음 | rc 0 · 통과 (문제 0) | rc 1 · 실패 (문제 2) |
| `d2_received_baseline` | D2 · 20001 | rc 0 · 통과 (문제 0) | rc 0 · 통과 (문제 0) · `명령 4 개 · 치환 4 곳` |
| `archived_after_settling_baseline` | `restart_kg50_d07_b40/restart_after_settling.bin` · 200001 | rc 0 · 통과 (문제 0) | rc 0 · 통과 (문제 0) · `명령 4 개 · 치환 4 곳` |

첫 사례의 문제 줄 (고친 판 · `codex_cases_after.log`):

```text
✗ 준비 구간 그 자리 치환 값이 본 덱과 다름 (10-30 KG50R-F01 · LIGGGHTS 는 ${x} · $x 를 그 줄을 읽을 때 치환): [fix gravi all gravity ${g_probe} vector 0.0 0.0 -1.0] 의 ${g_probe} — 본 덱 (62 번째 명령 자리) ⟦196.2⟧ ↔ 재개 덱 (55 번째 명령 자리) ⟦98.1⟧
✗ 재개 지점 fix gravi 다름 — 그 자리 치환을 펼치면 (10-30 KG50R-F01 · 정의 때 값 · LIGGGHTS 는 ${x} · $x 를 그 줄을 읽을 때 치환): 본 덱 [fix gravi all gravity ⟦196.2⟧ vector 0.0 0.0 -1.0] ↔ 재개 덱 [fix gravi all gravity ⟦98.1⟧ vector 0.0 0.0 -1.0]
```

시험 안 V2 · V3 (와 V1) = D2 사례를 리포 덱 (`docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/`) 에서 다시 만든 것 (Codex 덱과 `\r` 뺀 글 같음 · 줄 끝만 다름) · V4 · V5 = 합성 둘 (Codex 파일과 바이트 같은 CRLF 글 · sha256 앞 16 자 main `40e30bc80d851b3d` · resume `4d4759b5240e418c` / main `af6c7ca303a0790f` · resume `427fbd5172138885`) — `cmp_codex_decks.py` · `cmp_codex_decks.log`.

## 7. V 장면 표 — 장면마다 고치기 전 ↔ 고친 판 (`v_scenes_before.log` · `v_scenes_after.log`)

`-C` = rc · 판정 줄 (문제 수) · KG50R-F01 문제 줄 수 · 본 흐름 (`-T`) = 이번 호출의 시험 sbatch · 본 sbatch 수 · 정적 대조 판정.  음성의 고치기 전 = `-C` rc 0 · 본 흐름 시험 1 (반례가 열려 있음).  양성 `-C` 의 고치기 전 FAIL = 기록 줄 (`그 자리 치환 대조`) 이 없어서 — rc 0 (받음) 은 같다.  V37 은 고치기 전에도 거부였다 (기존 `var_refs` 가 자기 참조를 "정의 전 변수" 로 · 다른 까닭) — 시험이 보는 것은 KG50R-F01 닫힌 실패 줄.

| 장면 | 대조 | 내용 | 고치기 전 판 (77c24237) | 판정 | 고친 판 | 판정 |
|---|---|---|---|---|---|---|
| V2 | -C | Codex d2_drop_intermediate_variable_definition (g 98.1 → 196.2 → fix ${g_probe} → 98.1 · 재개 덱이 196.2 만 뺌) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V2 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V3 | -C | Codex d2_runtime_dependent_eager_variable (두 덱 같은 g = 98.1*(step+1) · fix ${g_probe}) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V3 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V4 | -C | Codex 합성 drop_intermediate_variable_definition (dt 1e-6 → 2e-6 → timestep ${dt} → 1e-6) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V4 | 본 흐름 | 같음 (LF 사본) | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V5 | -C | Codex 합성 runtime_dependent_eager_variable (두 덱 같은 dt = 1e-6*(step+1)) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V5 | 본 흐름 | 같음 (LF 사본) | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V6 | -C | 사슬 — b = ${a}*2 정의 앞 a 중간 정의 (98.1) 를 뺌 · fix 가 v_b 로 씀 | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V6 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V7 | -C | 한 글자 $g — g 98.1 → 196.2 → fix $g → 98.1 · 196.2 만 뺌 | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V7 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V8 | -C | 템플릿 fix 반지름 ${r_AM_S} = 실행 상태 수식 2.0e-3*(1+step) (두 덱 같은 글자) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V8 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 3 | PASS |
| V9 | -C | $(...) 그 자리 식 — timestep $(v_dt) (두 덱 같은 글자) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V9 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V12 | -C | 같은 글자 fix 가 본 덱에 둘 — 재개 덱 fix 는 앞 것 자리 (g 98.1) · 본 덱 끝 상태 = 뒤 것 (g 196.2) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 1 · F01 1 | PASS |
| V12 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 1 | PASS |
| V13 | -C | 같은 글자 b = ${a}*2 정의가 본 덱에 둘 — 끝 상태 b = 뒤 것 (a 98.1) ↔ 재개 덱 (a 49.05) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 1 · F01 1 | PASS |
| V13 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 1 | PASS |
| V14 | -C | v3 after_settling — 본 덱 체크포인트 앞에 반복 (label · if jump · 본 덱 timestep = 2e-6) · 준비 구간 timestep ${dt} | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 14 · F01 14 | PASS |
| V14 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 17 | PASS |
| V15 | -C | ${ 닫는 } 없음 — timestep ${dt (두 덱 같은 글자) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V15 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V16 | -C | string 변수 = 정의 때 실행 상태 값 (variable s_ins string ${n_ins} · n_ins = count(all)) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V16 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V20 | -C | string 값에 공백 (g_s string "98.1 vector 0.0 0.0 -1.0" · fix gravity ${g_s}) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V20 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V21 | -C | v_ 로 쓰는 string 값이 수 글 아님 (g_s string abc · g = v_g_s*2) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V21 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V22 | -C | atom 변수를 ${} 로 씀 | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V22 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V23 | -C | PI (등록 상수 목록 밖) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V23 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V24 | -C | 논리 연산자 \|\| (등록 상수 목록 밖) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V24 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V25 | -C | 본 덱 체크포인트 앞 run every 안 variable (삽입 run 1 끝에 g = 196.2 · 재개 덱에는 그 run 이 없다) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 12 · F01 12 | PASS |
| V25 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 12 | PASS |
| V26 | -C | 판 메시 fix (file 이름만 다름 허용) 가 본 덱에 둘 · 끝 상태 = 뒤 것 (scale ${msc} = 2.0) ↔ 재개 덱 (1.0) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 1 · F01 1 | PASS |
| V26 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 1 | PASS |
| V28 | -C | v3 after_settling — 본 덱 체크포인트 앞 python 줄 · 준비 구간 timestep ${dt} | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 14 · F01 14 | PASS |
| V28 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 17 | PASS |
| V29 | -C | 본 덱 체크포인트 앞 variable ${vn} equal 196.2 (이름 자리 치환 = g_probe 를 바꿈 · 재개 덱에는 없음) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 21 · F01 21 | PASS |
| V29 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 24 | PASS |
| V32 | -C | $ 뒤 이름 글자 아님 — fix gravity 98.1$- | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V32 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V34 | -C | v3 after_settling — 본 덱 체크포인트 앞 partition yes 1 variable dt equal 2.0e-6 | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 14 · F01 14 | PASS |
| V34 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 17 | PASS |
| V35 | -C | 본 덱 삽입 run 1 every 1 안 if 안 variable g_probe 196.2 (겹친 명령) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 12 · F01 12 | PASS |
| V35 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 12 | PASS |
| V36 | -C | 본 덱 삽입 run 1 every 1 "variable dt equal 2.0e-6" (마지막 쓰는 자리 뒤 · 끝 상태 dt = 2e-6 ↔ 재개 덱 1e-6) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 9 · F01 9 | PASS |
| V36 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 9 | PASS |
| V37 | -C | 순환 참조 (g = v_g+1 · fix ${g_probe}) | rc 1 · 실패 1 · F01 0 | FAIL | rc 1 · 실패 3 · F01 2 | PASS |
| V37 | 본 흐름 | 같음 | 시험 0 · 본 0 · 정적 실패 1 | FAIL | 시험 0 · 본 0 · 정적 실패 3 | PASS |
| V38 | -C | v_x[i] (atom 변수 원자 하나 값 · g = v_a_v[1]) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V38 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V39 | -C | string 을 equal 로 다시 정의 (LIGGGHTS 오류 꼴) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V39 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V40 | -C | equal 정의 인자 둘 (variable g_probe equal 98.1 2 · LIGGGHTS 오류 꼴) | rc 0 · 통과 0 · F01 0 | FAIL | rc 1 · 실패 2 · F01 2 | PASS |
| V40 | 본 흐름 | 같음 | 시험 1 · 본 0 · 정적 통과 0 | FAIL | 시험 0 · 본 0 · 정적 실패 2 | PASS |
| V1 | -C | 받은 D2 덱 그대로 (timestep ${dt} · 템플릿 반지름 셋 = 상수 · print · if 의 ${n_ins} = 값 대조 밖) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V1b | -C | 보관 after_settling 기준선 (§4) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V1c | -C | v3 50×50 after_settling (템플릿 줄 포함) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V1d | -C | Codex 합성 대조군 (dt 1e-6 한 번 · timestep ${dt}) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V10 | -C | 안전한 생략 (쓰기 전에 덮인 정의 196.2 만 뺌) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V11 | -C | 상수 사슬 (a 49.05 · b = ${a}*2 · fix v_b · 두 덱 같음) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V17 | -C | string 상수 글 (variable g_s string 98.1 · fix ${g_s}) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V18 | -C | 따옴표 안 ${dt} (그 자리 치환 아님 · 쓰지 않음) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V19 | -C | 정해진 수학 함수 · 비교 연산자 (g = sqrt(9623.61)*(2>=1) · fix ${g_probe}) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V30 | -C | v_ 로 쓰는 string 수 글 (g_s string 98.1 · g = v_g_s*1) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V31 | -C | v_ 로 쓰는 string = 정의 때 넣은 equal 값 (a 98.1 · s = ${a} · g = v_s*1) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V33 | -C | string = 띄어 쓴 equal 값 (a "49.05 * 2" · s = ${a} · fix ${g_s}) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V27 | -C | 판 메시 fix 하나 (scale ${msc} = 1.0 상수 · 재개 덱 file 이름만 다름 · 파일 있음) | rc 0 · 통과 0 · F01 0 | FAIL | rc 0 · 통과 0 · F01 0 | PASS |
| V1e | 본 흐름 | 받은 D2 덱 그대로 | 시험 1 · 본 0 · 정적 통과 0 | PASS | 시험 1 · 본 0 · 정적 통과 0 | PASS |
| V1f | 본 흐름 | Codex 합성 대조군 (LF 사본) | 시험 1 · 본 0 · 정적 통과 0 | PASS | 시험 1 · 본 0 · 정적 통과 0 | PASS |
| V1g | 본 흐름 | v3 after_settling 그대로 | 시험 1 · 본 0 · 정적 통과 0 | PASS | 시험 1 · 본 0 · 정적 통과 0 | PASS |

V 묶음만 (스크래치 사본 = 커밋된 시험에서 `make_vonly.py` · `make_verbose.py` 로 다시 만든 것과 바이트 같음): 고치기 전 `3 PASS · 73 FAIL` · 고친 판 `76 PASS · 0 FAIL`.

본 흐름 장면의 문제 수가 `-C` 보다 큰 것 (V8 +1 · V14 · V28 · V29 · V34 +3) = 본 흐름에서 도구가 본 덱의 템플릿 줄 넷 (`fix pts1`–`pts3` · `fix pdd_mix`) 을 재개 덱 `read_restart` 바로 뒤에 넣기 때문이다 (지금 판 러너 1518–1520 행 · 시험의 재개 덱 글에도 템플릿 넷이 있어 본 흐름 덱에는 둘씩 있다 — 대조군 V1e · V1g 도 같은 꼴로 통과).  V8 = 바뀌는 `${r_AM_S}` 를 쓰는 `pts2` 두 줄 (넣은 것 · 원래 것) 이 각각 "상수 아님" (+1) · V14 = 흐름 줄 뒤라 템플릿 치환 셋 (`${r_AM_P}` · `${r_AM_S}` · `${r_SE}`) 의 "펼칠 수 없음" 줄이 두 번씩 (+3) — 둘 다 문제 줄로 직접 봄 (`flow_vs_static.py` · `flow_vs_static.log`) · V28 · V29 · V34 = 수만 같은 꼴.

## 8. 변이 시험 — 새 관문 하나씩 끈 사본 36 → V 묶음 (`mutation_summary.log`)

결과: **변이 36 · 잡힘 33 · 생존 3**.  잡힘 = V 시험 하나라도 FAIL (줄 끝 = 잡은 시험).  변이 사본 36 개 = 커밋된 도구 (`38e1eff5…`) 에서 한 곳씩 바꾼 것 (되돌리면 도구와 바이트 같음 36/36 · `check_mutants_base.py` · `check_mutants_base.log` · 사본 자체는 스크래치) · 돌린 V 만 사본 = 커밋된 시험에서 `make_vonly.py` 로 다시 만든 것과 바이트 같음.

| 생존 | 끈 관문 | 까닭 |
|---|---|---|
| F01-28 | `var_env` 못 펼치는 변수는 `delete` 전까지 그대로 | 끄면 다음 `elif` (다른 꼴 다시 정의) 가 같은 거부를 낸다 — 바뀌는 것은 문제 줄 글뿐 (원래 까닭 → "다른 꼴") |
| F01-31 | `var_env` 따옴표 낱말 안 치환 자리 | 그 길에 닿으려면 변수 이름에 따옴표가 있어야 한다 (`variable x" equal "${a}"` 꼴 — 이름의 `"` 가 뒤집기를 바꿔 따옴표 낱말 안 `$` 가 밖이 된다) · LIGGGHTS 는 그런 이름을 오류로 끝낸다 (고정판 `variable.cpp` 430 행 · doc 111 행) — V 시험에 그런 덱 없음 |
| F01-32 | `var_env` 못 읽는 `variable` 줄 | 따옴표를 못 읽는 줄은 `unsupported()` 가 먼저 덱 전체를 거부 (`따옴표를 못 읽음`) |

처음 돌림 (V 68 · 284 PASS 때 · V37–V40 을 더하기 전) 에서는 변이 36 · 잡힘 28 · 생존 8 이었다 (위 셋 + F01-13 `$(...)` 판별 — `x` 꼴로 떨어져도 거부라 V9 글 조각이 둘 다에 맞음 · F01-26 순환 · F01-27 `v_x[…]` · F01-29 다른 꼴 다시 정의 · F01-30 인자 수).  V9 에 `그 자리 식 = 지원 안 함` 조각 · V37–V40 을 더해 다섯을 잡았다 (시험 먼저 커밋에 함께 들어감).  그 첫 판 변이 로그는 덮어써져 이 폴더에 없다 (작업 기록의 요약 줄만).  또 첫 고침 판에서 V34–V36 (내가 찾은 빈틈 = `partition` · 겹친 `run every` → `if` → `variable` · 끝 상태 변수 표) 이 FAIL 6 이었고 고친 뒤 통과했다 — 그 중간 판 도구는 남기지 않아 재현할 수 없다 (이 폴더의 증거 = 최종 판 기준 §5–§9).

## 9. Q5 selftest · `--compare-old` · 자기 공격

- Q5 (실제 도구 `-C` 의 문제 줄을 등록 §12-4 와 글자 · 순서로 대조): `kg50_q5_branches selftest: PASS (151/151)` · `kg50_q5_verdict selftest: PASS (98/98)` (커밋된 고친 판으로 다시 돌린 것 · `q5_*_after.log`).
- `python3 -I scripts/test_resume_ckpt.py --compare-old <옛 판>` (`compare_old_311.log`): `292 PASS · 0 FAIL` · `둘 다 정상인 장면 (시험 · G0–G3 통과 / -C 통과) 47 — 예전 묶음에서 다름 0 · 새 묶음에서 다름 0` · `옛 판 정상 · 새 판 거부 53` (53 개 전부 V) · `새 판만 정상` 0.
- V 밖에서 "다름" 인 장면 12 (P 2 · W 1 · G 1 · I 3 · Y 5) = 전부 두 판 다 거부한 장면 — 장면마다 옛 판 ↔ 새 판 출력 차이 줄을 찍어 봤다 (`make_cmpdiff.py` · `compare_old_scene_diffs.log` · 표지 `KG50R` 든 줄은 대조 틀이 원래 뺀다): 판정 줄의 문제 수 (P `p_jump` 3 → 9 · W9 1 → 7 · G `duplicate_loop_label` 2 → 8 · Y 넷 2 → 3 · 2 → 4 · 2 → 3 · 1 → 2 · Y 본 흐름 2 → 4 — 차이 줄이 문제 수 줄뿐 = 늘어난 줄은 다 표지 든 줄 · W9 · G · Y1 ya 셋은 "옛 문제 줄 그대로 + KG50R-F01 줄" 로 직접 셈 = `count_f01.py` · `count_f01.log` · 나머지는 수만) · I1 셋 = 찍는 도구 sha256 (`77c24237…` → `38e1eff5…` · 승인 안내 줄 하나 포함) · P `p_rr2` = 기존 bash 줄 `[: … binary operator expected` 의 스크립트 경로 · 줄 번호 (1149 → 1538 행).  두 판 다 정상인 장면 47 의 출력 · 보고 · 작업 폴더 (`.txt` 는 내용 sha256) 는 표지 `KG50R` 든 줄 말고 한 줄도 안 바뀌었다 — 고친 코드가 정상 장면에 더하는 줄은 기록 줄 `그 자리 치환 대조 (10-30 KG50R-F01): …` 하나뿐이다 (준비 구간에 치환이 있을 때 · 표지 든 줄).
- 자기 공격 (`attack_f01.py` · 합성 17 · 시험 밖 · 커밋된 고친 판 · `attack_final.log`): 기대와 다름 1 = A4 — 기대를 잘못 세웠다 (기존 `var_refs` 가 `v_c` 를 c 정의 앞에서 거부 · KG50R-F01 문제 0).  나머지 16 = 기대대로 — 중간 정의 뺌 (A1) · `v_` 사슬 (A3) · 따옴표 안 `$` (A5) · timestep 둘 (A7) · unfix 뒤 다시 fix (A17) · delete (A27) · fix 이름 자리 치환 (A31) · 대조군 (A32) · neigh_modify (A33) · region (A34) · group (A35) · 정의 없음 (A36) · 따옴표 뒤집기 넷 (A37 · A39 받음 / A38 · A40 거부).  ⚠ 첫 판 기록의 A32 이름표 ("단일 따옴표 안 겹따옴표 · 그 뒤 $") 는 덱 내용 (따옴표 없음) 과 달랐다 — 이름표를 "대조군" 으로 고치고, 따옴표 뒤집기는 A37–A40 으로 새로 쟀다.

## 10. 한계 · 닫지 못한 것

1. **`print … file | append` 로 쓴 파일** (판 STL 같은) 을 뒤에서 입력으로 쓰는 꼴 — 규칙 (5) 대로 값 대조 밖이다 (근거 "효과 = 출력" 이 이 꼴에서는 서지 않는다).  받은 덱 (D2 · v2 · v3 · after_settling) 은 판 STL `print` 가 체크포인트 뒤 구간 (명령 하나하나 대조 · 두 덱 같은 step) 에 있어 준비 구간에 없다.  준비 구간에 넣으면 지금 판은 받는다 → **1저자 결정 거리** (그 `print` 의 그 자리 치환도 값 대조로 넣을지).
2. **본 덱 체크포인트 앞 `run … every` · `partition` 안 상태 명령** (`fix` · `unfix` … · 변수 아님) — `run_state` 가 못 보고 `mprefix_check` 는 맨 위 `if` 만 본다 (기존 KG50R-03 계열 · 이번 범위 밖).  변수를 바꾸는 꼴만 이번에 닫았다 (V25 · V34 · V35 · V36).  제안: `mprefix_check` 가 `run every` 의 명령 · `partition` 도 같은 규칙 (print · quit · jump 만) 으로.
3. **CRLF 덱** — 셸 쪽 `awk` (`read_restart` 경로 · `S0`) 가 `\r` 을 남겨 본 흐름이 체크포인트를 못 찾는다 (`-C` 는 CRLF 를 읽는다 · Codex 합성 둘 = CRLF).  러너 구역 (다른 작업 트리) · 이번 범위 밖 — 시험의 본 흐름 장면은 LF 사본으로 돈다.
4. **엄격한 상수 목록** (PI · `&& || !` 거부) · **같은 수 다른 글 = 거부** · **쓰이지 않는 label 도 거부** — 모두 닫힌 쪽.  넓힐지는 1저자.
5. **변이 생존 셋** (§8).
6. **한 원인에 문제 줄이 여럿** — 흐름 줄 하나가 그 뒤 치환 · 끝 상태 변수마다 줄을 낸다 (V14 · V25 · V28 · V29 · V34 · V35 · V36 = 9–24 줄).  첫 줄이 원인을 적는다.
7. **실행 증거 없음** — 실제 LIGGGHTS · ibb SLURM 실행 없이 합성 덱 · 가짜 SLURM · 정적 대조만.  LIGGGHTS 의미 = 고정판 소스 · doc 을 읽은 것 — ibb 바이너리 신원 인증이 아니다.
8. **`deck()` ↔ LIGGGHTS 줄 읽기 차이** (공백 정리 · `&` 이음 · 주석 따옴표 규칙) — 기존 (Codex P09 · P10) 그대로.
9. **상태 표 밖 명령 (group 같은) 의 빠짐** 은 규칙 (1) 이 보지 않는다 (부분열 허용 · 기존 판 그대로) — 재개 덱에 있는 group 줄의 그 자리 치환 값은 본다 (자기 공격 A35).
10. **합칠 때** — V 의 본 흐름 장면은 러너 구역 글자 (`✗ 재개 덱 정적 대조 실패` · `재개 덱 정적 대조: 통과`) · 템플릿 넣기 (위 §7) 와 가짜 SLURM 틀 (`run_case` 의 `main_bytes` · `more_decks` · `ckpt` · `mode` · `orig_log`) 에 기댄다 — 다른 작업 트리의 러너 · 가짜 sbatch 고침과 합친 뒤 다시 돌린다.
11. **`var_refs` (기존)** 는 `v_` 도 정의 앞을 요구한다 (LIGGGHTS 보다 엄격) — 자기 공격 A4 · V37 의 고치기 전 거부 까닭.
12. **V 본 흐름 장면의 재개 덱에 템플릿이 둘씩** (§7) — 시험의 재개 덱 글이 이미 템플릿을 담은 채로 도구가 또 넣는다 (V 의 덱 = 받은 D2 · `res_after(tmpl=True)`).  템플릿 없는 재개 덱 (실제 `dem_restart.py` 꼴) + 도구가 넣은 템플릿 하나 꼴은 기존 묶음이 본다 (`res_variant` · `res_after` 기본 = 템플릿 0 · 예 K1 정상 본 제출) — 두 판 다 정상인 장면 47 의 출력 · 보고 · 작업 폴더가 그대로 (§9).
13. **관찰 (범위 밖 · 고치지 않음)** — Q5 selftest 이름표 셋 (`kg50_q5_branches.py` 1658 · 1753 · 2050 행 `G1c` · `G4c` · `H1d`) 이 "문제 셋 · W1 셋" 이라 적는데 대조하는 기대 목록 `EXPECTED_STATIC_W1` 은 넷이다 (판정은 목록 전체와 같은지 = 넷 · 이름표만 옛 글).

## 11. 다시 돌리기 (리포 뿌리)

- 시험: `python3 -I scripts/test_resume_ckpt.py` (mawk) · gawk = `PATH=<gawk 를 awk 이름으로 둔 폴더>:$PATH python3 -I scripts/test_resume_ckpt.py` · `<python3.8> -I scripts/test_resume_ckpt.py` (지시받은 명령) · 도구 내장 Python 까지 3.8 = `PATH=<python3 → python3.8 고리를 둔 폴더>:$PATH <python3.8> -I scripts/test_resume_ckpt.py` — 넷을 차례로 = `run_envs.sh <꼬리표> py311_mawk,py311_gawk,py38_mawk,py38all_mawk [--script <판>]` (스크립트 안 경로 = 이 작업 트리 · 스크래치)
- 고치기 전 판: `git show bf8cf21c6:scripts/resume_ckpt.sh > <옛 판>` 뒤 위 명령에 `--script <옛 판>` · 대조 = `--compare-old <옛 판>` · 장면마다 차이 줄 = `python3 -I make_cmpdiff.py scripts/test_resume_ckpt.py <사본> <리포 뿌리>` 뒤 `python3 -I <사본> --compare-old <옛 판>`
- Q5: `python3 scripts/kg50_q5_branches.py --selftest` · `python3 scripts/kg50_q5_verdict.py --selftest`
- Codex 사례: `python3 -I run_codex_cases.py <도구> <Codex ZIP 의 independent/program/cases> <빈 작업 폴더>` · 시험 덱 ↔ Codex 덱 = `python3 -I cmp_codex_decks.py <리포 뿌리> <같은 cases>` (Codex 고정물 = 리포 밖 · 읽기만)
- 장면 표: `python3 -I make_vonly.py scripts/test_resume_ckpt.py <V 만 사본> <리포 뿌리>` → `python3 -I make_verbose.py <V 만 사본> <verbose 사본>` → `python3 -I <verbose 사본> --script <판>` 을 두 판에 → `python3 -I vtable.py <옛 로그> <새 로그>` · 본 흐름 ↔ `-C` 문제 수 = `python3 -I flow_vs_static.py <리포 뿌리> <임시 폴더 위>`
- 변이: `python3 -I mutate_f01.py scripts/resume_ckpt.sh <V 만 사본> <빈 출력 폴더> [이름,…]` · 사본이 도구에서 나왔는지 = `python3 -I check_mutants_base.py mutate_f01.py <출력 폴더> scripts/resume_ckpt.sh`
- 자기 공격: `python3 -I attack_f01.py scripts/resume_ckpt.sh <빈 작업 폴더>`

## 12. 이 폴더

| 파일 | 무엇 |
|---|---|
| `before_<환경>.log` (넷) | 최종 시험 + 고치기 전 판 (`--script <옛 판>`) |
| `after_<환경>.log` (넷) | 최종 시험 + 고친 판 (넷 바이트 같음) |
| `run_envs.sh` · `run_summary.txt` | 네 환경 러너 (디스크 가득 줄이 있으면 다시) · 돌린 판의 끝 줄 요약 (§5 · §7 · §8) |
| `v_scenes_before.log` · `v_scenes_after.log` | V 묶음만 · 장면마다 `[-C]` · `[흐름]` 결과 줄 (§7 표의 원본) |
| `flow_vs_static.py` · `flow_vs_static.log` | V8 · V14 의 본 흐름 ↔ `-C` 문제 줄 (§7) |
| `codex_cases_before.log` · `codex_cases_after.log` · `run_codex_cases.py` | Codex 사례 여섯 `-C` (§6) |
| `cmp_codex_decks.py` · `cmp_codex_decks.log` | 시험 V1–V5 덱 ↔ Codex 사례 덱 (§6) |
| `q5_branches_after.log` · `q5_verdict_after.log` | Q5 selftest (커밋된 고친 판) |
| `compare_old_311.log` · `compare_old_scene_diffs.log` · `make_cmpdiff.py` · `count_f01.py` · `count_f01.log` | `--compare-old` · V 밖 "다름" 장면 12 의 옛 ↔ 새 차이 줄 · 그 중 셋의 KG50R-F01 줄 셈 (§9) |
| `mutation_summary.log` · `mutate_f01.py` · `check_mutants_base.py` · `check_mutants_base.log` · `make_vonly.py` · `make_verbose.py` · `vtable.py` | 변이 시험 · 사본 출처 대조 · 표 만들기 (§7 · §8) |
| `attack_f01.py` · `attack_final.log` | 자기 공격 17 (§9) |

## 13. 정정 (10-30 · 2 판 · 독립 사전 공격 리뷰가 찾은 서술 어긋남 둘 — 위 본문 · 커밋 메시지는 고치지 않는다)

1. **"V 음성 30 = 고치기 전 -C 통과"** (시험 먼저 커밋 `f3cbdc6f3` 메시지 *"V 의 음성은 -C 통과 (문제 0)"*) → **30 중 29**.  V37 (순환 참조) 은 고치기 전 판
   (도구 sha256 77c24237…) 에서도 `-C` rc 1 (문제 1 · 기존 `var_refs` 의 "정의 전 변수" · 다른 까닭) 이었다 — §7 표 V37 줄 (`rc 1 · 실패 1 · F01 0`) 이 맞고
   그 메시지의 전칭이 틀렸다.  V37 시험이 고치기 전에 FAIL 인 까닭 = KG50R-F01 닫힌 실패 줄이 없어서 (§7 본문 그대로).  "V 76 중 대조군 셋 빼고 FAIL" (§0) 은 맞다.
2. **"끝 상태 표 전부를 펼친 줄로 대조"** (§2 규칙 (3) · §3-5 · 고침 커밋 `f4346cf69` 메시지 ②) → **펼친 것은 줄 (값) 이고 표의 키는 아니다**.  키 (fix · compute ·
   dump · region ID · unfix 대상 · pair_coeff 형) 는 치환 전 글자로 만들었다 — `fix gx${n}` 둘이 한 키로 접히고 본 덱에만 있는 `unfix ${u}` 가 아무것도 안 지워
   감쇠 fix 를 뺀 덱이 통과했다 (사전 공격 R1 · P1).  2 판 = 키 · 분류 자리에 `$` 가 있으면 닫힌 실패 (키를 펼치지 않음) — [`r2/README.md`](r2/README.md) §1.

# 사전 공격 리뷰 — 재개 도구 고친 판 (10-28 밤 · 독립 에이전트 · diff 만)

- 대상: 고친 판 `scripts/resume_ckpt.sh` sha256 `fb334928…` (작업 트리 판 = 통합 커밋 `0ec4c1c16` 과 같은 바이트) · 시험 `scripts/test_resume_ckpt.py` 179 · 명세 = Codex 판정문 (`docs/reviews/codex_kg50_resume_recheck_20261028/codex_review_kg50_resume_recheck_20261028.md`) · 수정 계획 `docs/50kg/kg50_resume_recheck_fix_plan_20261028.md`.
- 리뷰어는 고친 사람의 설명 없이 diff · 명세만 받았다 (CLAUDE.md 사전 공격 규칙 ③).  설치 · SLURM · LIGGGHTS · push 없음 · 작업 트리 무변경.
- 리뷰어 확인: Codex 원 반례 (KG50R-01–05 · 07) 는 모두 막힌다 · 시험 179 PASS · 0 FAIL (mawk 1.3.4 · gawk 5.2.1 · Python 3.8.20 셋 다 리뷰어가 직접) · 고치기 전 판 97 PASS · 82 FAIL.

## 찾은 것 (원장 `KG50P-01`–`10`)

| 원장 | # | 등급 | 무엇 | 고친 판 | 고치기 전 판 |
|---|---|---|---|---|---|
| `KG50P-01` | A | **P1** (회귀 · KG50R-03 부류) | 준비 구간에서 변수를 바꿨다 되돌리면 통과 — 실제 D2 r4 덱에서 두 줄만 바꿈 (47 줄 `variable dt equal 2.0e-6` · `timestep ${dt}` 바로 뒤 `variable dt equal 1.0e-6`) · 상태 대조가 끝 값만 본다 · LIGGGHTS 는 `${dt}` 를 읽을 때 치환 (리뷰어 판독: input.cpp · restart 머리에 dt 없음) ⇒ 재개 dt 2 배 (`d2/A_dt_redef_r4.liggghts`) | `-C` rc 0 통과 · 가짜 SLURM 사슬 시험 1 · 본 1 · after_settling 꼴도 통과 | rc 1 (`본 덱에 없는 줄` — 지운 옛 검사가 막던 꼴) |
| `KG50P-02` | B | P2 | restart 체크포인트에서 본 덱 그 run 의 꼬리 (`every` · `start`/`stop` · `pre`/`post`) 를 대조하지 않음 — 본 덱 `run 200000 every 1000 "velocity all set 0 0 0"` + 재개 덱 `run 180000` 통과 · every 안 `include` 도 못 봄 (`d2/B_main_every.liggghts`) | rc 0 · 시험 1 · 본 1 | rc 0 (같음) |
| `KG50P-03` | C | P3 | 시도 폴더 묶음은 기록일 뿐 — 본 제출은 작업 폴더의 러너 · 덱을 sha 대조 없이 그대로 · 시험 뒤 덱 · 러너를 바꿔도 본 제출 · tool.txt 에 체크포인트 sha · lmp_mpi 신원 없음 (Codex §10-5 일부만) (`probe_e2e2.py deck_changed_after_trial runner_changed_after_trial`) | 둘 다 시험 1 · 본 1 | — |
| `KG50P-04` | D | P3 | 본 sbatch 출력을 검사하지 않음 (시험 쪽 Q9d 와 다름) — 오류 글 + rc 1 이면 `✅ 본 제출 job sbatch: error: …` (`probe_e2e.py MAIN_SBATCH_TEXT`) | 그대로 | 같음 |
| `KG50P-05` | E | P3 · awk 차이 | G3 `sane()` 에 유한 검사 없음 (G1 `same()` 에는 있음) — 비교 줄 KE `nan` 이면 mawk 본 제출 · gawk 거부 · gawk 도 `-nan` · `+nan` 통과 · G0 마지막 줄 검사 때문에 실제로 닿기 어려움 (`probe_e2e.py NaN_G3`) | mawk 본 1 · gawk 본 0 | 같음 |
| `KG50P-06` | F | P3 | 둘째 고리가 `read … < mode.txt` 실패를 보지 않음 · `C ./C` 두 철자 → 둘째가 첫 케이스 작업 폴더를 prev 로 밈 (`probe_e2e2.py two_spellings`) | 본 0 (우연) | — |
| `KG50P-07` | G | P3 | 큐 이름 검사가 C · C_ins · C_<이번 SFX>[t] · C_r<N>[t] 만 — 앞 호출이 `-x foo` 였으면 C_foo 본 런을 못 봄 (`probe_e2e2.py custom_suffix_busy`) | 시험 1 · 본 1 | 같음 |
| `KG50P-08` | H | P3 | 체크포인트 대조가 파일 이름 (basename) 만 — 다른 케이스 폴더의 같은 이름 체크포인트도 `-C` 통과 · 본 흐름은 G1 이 잡을 것 (`d2/other_ckpt_r4.liggghts`) | 통과 | 통과 |
| `KG50P-09` | I | P3 | 낱말 나누기가 LIGGGHTS 와 다름 (`&` 이음 · NBSP · CR 만 쓴 덱) — `-C` 통과 · LIGGGHTS 는 오류로 멈추거나 아무것도 안 함 → cut · G0 가 막음 (닫힌 실패) (`probe_static.py` G_ · H_) | `-C` 통과 | 같음 |
| `KG50P-10` | J | P3 | 허용 차이 ② (판 메시 file 이름) 는 파일이 있는지만 · 내용 (판 높이) 안 봄 · 준비 구간 fix 순서 바꿈도 통과 (`probe_static.py` C_ · D_) | 통과 | 통과 |

## 깨진 보장 문장 (리뷰어)

- `scripts/resume_ckpt.sh` 머리 주석 · 절차 문서 개정 4 절의 *"준비 구간이 만든 상태 = 본 덱 체크포인트 시점 상태"* → A · *"그 밖의 더함 · 빠짐 · 바뀜 = 거부"* → A · J · *"본 덱 그 run (남은 step 만 다름)"* → B · *"include … = 거부 (어디서든)"* → B 의 every 안 include.

## 변이 (리뷰어 · 관문 하나씩 끈 사본 59)

- 잡힘 40 · 생존 19 = **시험 빈틈 3** (`py_reinsert` = 본 덱이 ins_mix 를 unfix 하지 않고 재개 덱이 다시 선언 · `sh_g1` = 시험 setup 줄 KE 0.1000 → 0.1003 이면 변이가 본 제출 (G1 단독 시험 없음) · `sh_miss` = 22000 줄 하나만 빠진 시험 로그) + **이중 방어 16** (옆 관문이 같은 꼴을 막음).
- 옛 동작을 되살린 변이 `sh_stale_loop` = 시험 8 개 (R1 둘 · R2–R6 · R10) 가 잡음.
- 고친 사람 기록 (28 중 26 잡힘) 과는 변이 집합이 다르다.

## mawk ↔ gawk (리뷰어)

- 시험 179/179 둘 다 같음 · A · B · C · D · G 판정 같음 · 갈린 것 = E 하나 · 새 `lastrun()` 은 nan · inf · 1e5 · 2^31 넘는 step 에서 둘 다 같음.

## 실제 D2 덱 (고친 판 `-C` · Python 3.11 · 3.8 같음)

- 받은 재개 덱 (`run 180000`) = rc 0 · 문제 0 (끝 200001 · 첫 긴 run 뒤 명령 64 개 같음).
- 157 줄을 `run 179999` 로 한 글자 바꾼 사본 (`d2/input_kg50_d2_b50_r4_orig179999.liggghts`) = rc 1 · 문제 하나 `남은 step 다름` · `--fix-run` → 받은 r4 와 바이트 같음 · `--cut-trial` → 받은 r4t 와 바이트 같음 · 시험 run 합 2000.
- ⇒ 지금 도는 D2 는 A · B · C 꼴이 아니다 (이 덱 한정).

## 찾지 못함 (시도한 부류)

- lastrun 의 NaN · inf · 넘침 · 빈 mode 파일 · 같은 케이스 · 같은 label · read_restart 둘 · 주석 · 따옴표 안 명령 · 전각 숫자 · 재개 쪽 run 꼬리 · 옛 job/mode/log · squeue 실패 · `id;cluster` 꼴 sbatch 출력 · 시험 예산 넘기기 · 압축 체크포인트 — 모두 거부 또는 닫힌 실패.

## 파일

- 반례 덱 `d2/` · 탐침 `probe_*.py` (`probe_static.out` · `probe_as.out` = 출력) · 변이 `mutants.py` · `mut_results.txt`.  탐침 안 경로는 리뷰 때 스크래치 경로다 (돌리려면 인자로 도구 경로를 준다).

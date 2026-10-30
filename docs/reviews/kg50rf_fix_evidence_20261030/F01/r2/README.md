# KG50R-F01 2 판 — 독립 사전 공격 R1–R8 고침 + KG50R-F02 통합 (10-30 · 1저자 "권고대로")

## 0. 판 · 커밋 (가지 `kg50-f01r2-int` · push 없음)

| 단계 | 커밋 · 도구 sha256 |
|---|---|
| 시작 = F01 끝 | `c24fef721` · 도구 `38e1eff5…` |
| F02 통합 (cherry-pick 6 · 작업 가지 원래 번호 c3c67fb37 · 2107f144f · a0680e8f8 · 34b3e2cdb · 6057a6514 · d23a865a3 = 원격에 없음) | → 이 가지 `8bc406a2a` · `0b710c85d` · `aee27ba0b` · `debd23ad0` · `7920e9be8` · `4865ba895` (같은 차례) — 충돌 = 시험 파일 `main()` 끝 묶음 자리 하나 (V · RB 둘 다 둠) · 통합 도구 `12bc95ce030fbc9b…` = F01 정적 대조 heredoc + F02 그 밖 (둘 다 바이트 같음 · `compose_check.log`) · 통합 시험 383 PASS · 0 FAIL (Python 3.11 · mawk · `integrated_12bc95ce_py311_mawk.log`) |
| 시험 먼저 | `f4142506e` — VP 묶음 50 (`--only VP`) |
| 고침 | `65c5d6d37` — 도구 **`2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8`** (메인 세션에 알림 → ibb `-T` 에 씀 · 이 뒤 도구 안 바꿈) |
| 증거 | 이 폴더 · F01 README 정정 §13 |

## 1. R1–R8 ↔ 고친 것 ↔ 시험

| R | 결함 (사전 공격) | 고친 것 (도구 2dc7f693) | VP 시험 |
|---|---|---|---|
| R1 (P1) | 끝 상태 표의 키 = 치환 전 글자 (`fix gx${n}` 둘이 한 키 · 본 덱만 `unfix ${u}` = 아무것도 안 지움 → 감쇠 뺀 덱 통과) | `run_state`: 키 · 분류 자리 (fix ID · 스타일 · unfix · compute · uncompute · dump · undump · `*_modify` · region ID · 꼴 · pair_coeff 형 · variable 이름) 에 `$` = 닫힌 실패 (키를 펼치지 않음) — 실제 덱에서 `$` 는 값 자리뿐 (`scan_keys.log`) | VP1a–h (리뷰어 A1 · A2 · A2p · A1as · A2as + 스타일 · region · pair_coeff) |
| R2 (P2) | 본 덱 체크포인트 앞 `run … every "…"` 안 fix · unfix · timestep 을 안 봄 (if 안 같은 명령은 거부) | `mprefix_check`: run every · partition 안 명령 = print · quit 만 (if 와 같은 규칙 · 둘 안 jump 도 거부 — restart 체크포인트 남은 step 셈이 못 보는 자리) · `unsupported()` 가 partition 안 명령도 (include · next) | VP2a–f (A3 · A4 · A5 + partition · jump · 뒤 구간 partition include) · 대조군 VP2z |
| R3 (P2) | 줄 읽기 ≠ LIGGGHTS (`#\r…` · `&`+NBSP · `variab&`↵`le`) | `deck_lines()`: 고정판 `Input::file()`/`parse()` 그대로 — 바이트 · `\n` 에서만 · 줄 끝 C 공백 · `&` 이음 사이 공백 없음 · 파일 끝 `&` = 글자 · 주석 따옴표 규칙 (다른 따옴표로 바뀜) · 제어 글자 (탭 · 원 줄 끝 `\r` 말고 · 주석 안이어도) · 주석 밖 비 ASCII = 거부 (주석 안 한글 받음) · `deck_spans` 같은 함수 | VP3a–g (A9 · A10 · A11 + NBSP · `\f` · NUL · 주석 따옴표) · 대조군 VP3z |
| R4 (P2 · 1저자 결정 대기) | 준비 구간 `print … file/append` 로 쓴 STL 을 mesh fix 가 읽음 (print 값은 대조 밖) | 재개 덱 준비 구간 print file/append 의 파일을 뒤 명령 (print 말고) 이 읽음 · 이름에 `$` = 닫힌 실패 (본 덱은 안 봄 — §5-1) | VP4a–c (A8 + 판 STL · 이름 `${pf}`) · 대조군 VP4z |
| R5 (P3) | write_restart 체크포인트 앞 jump · label · clear → 줄 순서 상태 표가 틀림 (변수 없는 덱은 통과) | write_restart 체크포인트 앞 label · jump · clear · python (맨 위 · if · run every 안) = 닫힌 실패 (restart 체크포인트는 남은 step 셈이 이미 거부) | VP5a–f (A7s · C1 · A7 + label · if 안 jump · python) · 대조군 VP5z |
| R6 (P3) | 판 메시 "file 이름만 다름" 허용이 치환 전 이름으로 있는지 봄 | 준비 구간 상태 = 펼친 이름으로 있는지 · 펼친 이름에 equal 값 · 실행 상태 값 = 거부 · 뒤 구간 file 이름에 `$` = 거부 (안 펼침) · `mesh_file` 낱말 = 공백 · 탭만 | VP6a (A12a · 고치기 전 = 거짓 거부) · VP6b (A12b) · VP6c · VP6d |
| R7 (P3) | 펼친 글이 깊이에 지수 (20 단 = 316 s) | `expand` · `var_env` 펼친 글 4096 자 상한 → 못 펼침 = 닫힌 실패 (실제 24 쌍 최대 = 15 자 · `measure_xlen.log`) | VP7 (`${}` 20 단 · `v_` 24 단 · string 20 단 — 60 초 안 거부) · 대조군 VP7z (6 단) |
| R8 (P3) | group 값 대조에 시험 없음 (변이 M16 생존) | 시험만 | VP8 (본 덱 t 1→3→group→1 · 재개 덱 3 뺌) · 대조군 VP8z |

## 2. 결과 — 환경별 (로그 끝 줄)

| 환경 | 고치기 전 = 통합 12bc95ce + 최종 시험 (`--script`) | 고친 판 2dc7f693 |
|---|---|---|
| Python 3.11.15 · mawk 1.3.4 | `390 PASS · 43 FAIL` | `433 PASS · 0 FAIL` |
| Python 3.11.15 · GNU Awk 5.2.1 | `390 PASS · 43 FAIL` | `433 PASS · 0 FAIL` |
| 시험 틀 3.8.20 · 도구 python3 3.11 · mawk | `390 PASS · 43 FAIL` | `433 PASS · 0 FAIL` |
| 시험 틀 · 도구 둘 다 3.8.20 · mawk | `390 PASS · 43 FAIL` | `433 PASS · 0 FAIL` |

- 433 = 기존 383 (216 + V 76 + RB 91) + VP 50.  고친 판 로그 넷 = 바이트 같음 (sha256 `032e6239…`).  디스크 가득 줄 0.
- 고치기 전 43 FAIL = 전부 VP (기존 383 통과) — 까닭 (`why_before.log`): `-C` 통과 = 반례 열림 29 · 본 흐름 시험 냄 · G0–G3 통과 5 · 다른 까닭으로 이미 거부 (새 문제 줄 없음) 5 (VP2d · VP2e · VP5f = F01 끝 상태 변수 표 "못 정함" · VP6a = 치환 전 이름 `${mf}_r4` 로 찾아 거짓 거부 · VP6c = F01 판 메시 펼친 줄 대조 — `str.split()` 이 값 표지에서 file 낱말을 갈라 "file 이름 말고도 다름" 으로 거부) · VP3a 본 흐름 = F02 러너 대조가 먼저 막음 1 · R7 = 60 초 초과 2 · string 사슬 통과 1.  통과 7 = 대조군 6 + VP8 (group 값 대조는 이미 있음 — M16 잡이).
- Q5 selftest (고친 판): `kg50_q5_branches selftest: PASS (151/151)` · `kg50_q5_verdict selftest: PASS (98/98)`.
- `--compare-old` (Python 3.11 · mawk · 판정은 지금 판으로만): 옛 판 `77c24237` (= `bf8cf21c6`) · `5f4ffb46` (F02 1 판) 둘 다 rc 0 · `433 PASS · 0 FAIL` ·
  둘 다 정상인 장면 53 — 예전 묶음 · 새 묶음 다름 0 · 옛 판 정상 · 새 판 거부 91 = V 53 + VP 38 (전부 반례 장면) · V · VP 밖 "다름" 12 (P 2 · W 1 ·
  G 1 · I 3 · Y 5) = F01 증거 §9 와 같은 장면 (두 판 다 거부 · 문제 수 · 찍는 도구 sha256) · C 묶음 4/4 같음 (§5-1).

## 3. 실제 덱 · 반례 · 줄 읽기 대조

- **실제 kg50 본 덱 12 × (settling · after_settling) = 24 쌍 → rc 0 24** (고친 판 `real24_final.log` · 통합 판 `real24_before.log`) — 리뷰어 `a04_regress.py` 와 같은 재개 덱.
- **리뷰어 반례 덱 15** (`f01rev/*_main|_resume.liggghts` · `repro_all_r2.py`): 통합 판 rc 0 14 (A7 = F01 변수 표로 rc 1 · `repro_before.log`) → 고친 판 **rc 1 15** (`repro_final.log`).
- 줄 읽기 (`reader_diff.log`): 리포 kg50 덱 151 + 리뷰어 A9 · A10 · A11 — 새 `deck()` = 리뷰어 LIGGGHTS 흉내 (`a12_ligread.py` · 고정판 `file()`/`parse()`) 153/153 (A9 = 제어 글자 거부) · 새 = 옛 `deck()` 151/151 (리포 덱) · 옛 ≠ LIGGGHTS 3 (반례 셋).
- 실제 덱 조사 (`scan_decks.log`): 151 덱 · 비 ASCII 줄 5,572 = 전부 주석 안 · 제어 글자 (탭 · `\r` 말고) 0 · `\r` 844 = Codex CRLF 고정물 (전부 원 줄 끝 — 새 읽기가 151 덱을 다 받음 = `reader_diff.log`) · `&` 이음 1,282 = 전부 앞에 공백 · 주석 밖.  흐름 줄 (`scan_flow.log` · 명령 번호 0 부터): 12 본 덱의 label · jump = 압축 루프 (108 · 112) = 두 체크포인트 (restart 63 · write_restart 65) 뒤.

## 4. 변이 시험 — 새 관문 하나씩 약하게 (`mutation_r2.txt` · VP 먼저 · VP 에서 살아남으면 전체)

사본 38 = 고친 도구에서 한 곳씩 (바꿀 글이 정확히 한 번 · 같은 자리에서 되돌리면 도구와 바이트 같음 = `mut_dry.py` 38/38).  **잡힘 31 · 생존 7.**

| R | 잡힘 / 변이 | 잡은 시험 | 생존 · 까닭 |
|---|---|---|---|
| R1 | 5 / 10 | VP1a–h | R1f compute · R1g dump · R1h `*_modify` 셋 · R1i uncompute · undump = 시험이 없는 키 표 줄 (같은 KEYPOS 조회 길 — fix · unfix · region · pair_coeff 줄은 잡힘) — **동등 아님** · R1j variable 이름 = 판정 동등 (F01 변수 표가 이름 자리 치환을 이미 "못 정함" → 거부 · V29) |
| R2 | 4 / 4 | VP2a–f | — |
| R3 | 7 / 7 | VP3a–g | — |
| R4 | 3 / 3 | VP4a–c | — |
| R5 | 5 / 5 | VP5a–f | — |
| R6 | 4 / 4 | VP6a–d | — |
| R7 | 2 / 4 | VP7 (R7c = string 사슬 · R7d = v_ 사슬 60 초 초과) | R7a 고리 안 상한 · R7b 끝 상한 = 하나만 끄면 판정 동등 (다른 하나가 한 단 뒤에 끊는다) · 둘 다 끈 R7d = 잡힘 (v_ 24 단 60 초 초과) |
| R8 | 1 / 1 (리뷰어 M16) | VP8 | — |

## 5. 한정 · 닫지 않은 것

1. **R4 = 1저자 결정 대기** — 지금 규칙 = 재개 덱 준비 구간 print file/append 를 뒤 명령이 읽으면 닫힌 실패.  본 덱은 보지 않는다: 본 덱 쪽도 보면 기존 시험 C1 (실제 09-27 압축 재개 본 덱이 체크포인트 앞에서 제 판 STL 을 쓰고 읽음 · 이미 Q3 로 거부) 의 문제 수가 2 → 3 으로 바뀌었다 — 본 덱이 제 준비 구간에서 쓰고 읽는 파일은 본 덱 자신의 이력이다.
2. **R6 뒤 구간** = 펼치지 않고 `$` 면 거부 (펼친 이름 대조는 준비 구간 상태 표만).
3. **R1 = 키를 펼치지 않는다** (닫힌 실패) — `$` 를 ID 자리에 쓰는 덱은 받지 않는다 (실제 덱 0).
4. **R7 상한 4096 자** — 넘는 정상 덱도 거부 (닫힌 쪽 · 실제 최대 15 자).
5. **R2 run every · partition 안 jump 도 거부** — if 안 jump 는 예전처럼 받음 (restart = 남은 step 셈이 거부 · write_restart = R5 가 거부).
6. 리뷰어의 다른 생존 변이 M20 · M23 · M28 · M35 (F01 첫 판 관문) = 이번 범위 밖 · 고치지 않음.  이번 변이 생존 중 동등 아닌 넷 (R1f–R1i · 시험 없는 키 표 줄) 도 열린 채 — 시험을 더하면 닫힌다 (도구 안 바꿈).
7. 셸 쪽 `awk` 의 덱 읽기 (read_restart 경로 · S0 · CRLF) = F01 §10-3 그대로 (범위 밖).
8. 실행 증거 없음 — 가짜 SLURM · 정적 대조 · LIGGGHTS 의미 = 고정판 `src/input.cpp` (`file()` 183–265 · `parse()` 343–393 · `nextword()` 407–426) 를 읽은 것.

## 6. 이 폴더

| 파일 | 무엇 |
|---|---|
| `compose_check.py` · `compose_check.log` · `integrated_12bc95ce_py311_mawk.log` | F02 통합 (§0) |
| `before_<환경>.log` · `after_<환경>.log` (넷씩) · `*_summary.txt` | 전체 시험 (§2) |
| `why_before.log` · `why_before.py` | 고치기 전 VP FAIL 까닭 (§2) |
| `real24_final.log` · `real24_before.log` · `real24.py` | 실제 24 쌍 (§3) |
| `repro_final.log` · `repro_before.log` · `repro_all_r2.py` | 리뷰어 반례 15 (§3) |
| `reader_diff.log` · `reader_diff.py` · `scan_*.log` · `scan_*.py` · `measure_xlen.*` | 줄 읽기 대조 · 실제 덱 조사 · 펼친 글 길이 (§3 · §1 R7) |
| `q5_*_selftest.log` · `compare_old_*.log` | Q5 · `--compare-old` (§2) |
| `mutation_r2.txt` · `mutate_r2.py` · `mut_dry.py` | 변이 (§4) |
| `run_one.sh` · `run_envs.sh` · `run_q5.sh` · `run_cmpold.sh` · `run_scans.sh` | 돌린 명령 (경로 = 이 작업 트리 · 스크래치) |

변이 사본 · 장면별 로그 (`mut/logs/` · 864 KB) 는 스크래치에만 둔다 (요약 = `mutation_r2.txt` 에 잡은 시험 이름).

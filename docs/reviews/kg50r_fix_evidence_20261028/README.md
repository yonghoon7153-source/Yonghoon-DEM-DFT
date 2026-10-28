# 50kg 재개 도구 고침 증거 (10-28 밤 · KG50R-01–05 · 07 · Q5 §12-4)

- 대상: `scripts/resume_ckpt.sh` 고친 판 sha256 `fb334928ff0c524e240f3166fea40245d298a40b9245a26fd720352e7b106f07` (고치기 전 판 `e59c43e688b2b9a6c23a337ceee2b28214ed3f6c76bd69b7f2402f926336dae8` = 리뷰 핀 `f118c1fd1` 의 판) · 시험 `scripts/test_resume_ckpt.py` (179 개 = 옛 87 + 새 92) · Q5 생성기 `scripts/kg50_q5_branches.py` · 판독기 `scripts/kg50_q5_verdict.py`.
- 환경: 이 리포의 클라우드 컨테이너 (Linux · GNU bash 5.2.21) · 가짜 SLURM · 가짜 `dem_restart.py` (시험 안 stub) — 실제 ibb SLURM · LIGGGHTS 없음.
- 다시 돌린 사람 = 메인 세션 (10-28 밤 · 아래 "메인 재실행" 줄).  고친 사람 (작업 트리 에이전트) 의 기록은 그렇다고 적었다.

| 파일 | 무엇 | 결과 (파일 끝 줄) | 누가 |
|---|---|---|---|
| `test_311_mawk.log` | 고친 판 · Python 3.11.15 · awk = mawk 1.3.4 | `179 PASS · 0 FAIL` · rc 0 | 메인 재실행 |
| `test_311_gawk.log` | 고친 판 · Python 3.11.15 · awk = GNU Awk 5.2.1 (아래 출처) | `179 PASS · 0 FAIL` · rc 0 | 메인 재실행 |
| `test_38_mawk.log` | 고친 판 · Python 3.8.20 (kgy 판과 같은 판) · mawk | `179 PASS · 0 FAIL` · rc 0 | 메인 재실행 |
| `test_311_oldtool.log` | 같은 시험 179 + 고치기 전 판 (`e59c43e6…` · `git show b80f98f98:scripts/resume_ckpt.sh`) | `97 PASS · 82 FAIL` · rc 1 | 메인 재실행 |
| `compare_old_311.log` | `--compare-old <고치기 전 판>` — 둘 다 정상인 장면의 출력 대조 | 둘 다 정상 30 = 예전 묶음 다름 0 · 새 묶음 다름 3 (보고만) · 옛 판 정상 · 새 판 거부 43 · rc 0 | 메인 재실행 |
| `q5_branches_selftest_before.log` · `q5_verdict_selftest_before.log` | 고친 재개 도구 + Q5 시험 먼저 커밋 (등록 §12-4 를 읽는 selftest · 생성기 상수는 옛 판) | `FAIL (62/85)` · `FAIL (6/21)` — 가지 만들기 거부 (기대 ≠ 도구 출력) | 메인 |
| `q5_branches_selftest_after.log` · `q5_verdict_selftest_after.log` | Q5 생성기 고침 뒤 | `PASS (151/151)` · `PASS (98/98)` | 메인 |
| `q5_static_new_tool_capture.json` | 고친 도구가 Q5 가지 덱에 낸 `-C` 문제 줄 전부 (selftest 중 `static_check` 감싸 기록) | W1 셋 · W2 넷 = 등록 §12-4 | 메인 |
| `mutants_fixer.py` · `mutants_fixer_log.txt` | 관문 28 개를 하나씩 끈 사본으로 시험 179 | 26 잡힘 · 생존 2 (자른 시험 덱 다시 읽기 대조 · 셸 시험 예산 대조 = 같은 꼴을 막는 이중 방어) | 고친 사람 기록 (메인 재실행 안 함) |

- gawk 출처: Ubuntu noble `gawk` `1:5.2.1-2ubuntu0.1` amd64 .deb (sha256 `baaf6853bea746485bff4ae0e506599b3c5093ebe6ec9b9584e4272f94f75b93`) 를 스크래치 폴더에 풀어 (`dpkg-deb -x`) 그 `gawk` 를 `awk` 이름으로 PATH 앞에만 놓았다 — 시스템 `awk` (mawk · update-alternatives) 는 바꾸지 않았다.
- 다시 돌리기 (리포 뿌리): `python3 -I scripts/test_resume_ckpt.py` · gawk = `PATH=<gawk 를 awk 로 둔 폴더>:$PATH python3 -I scripts/test_resume_ckpt.py` · 옛 판 = 리포 사본에서 `scripts/resume_ckpt.sh` 를 `git show b80f98f98:scripts/resume_ckpt.sh` 로 바꾼 뒤 같은 명령 · 대조 = `python3 -I scripts/test_resume_ckpt.py --compare-old <옛 판 경로>` · Q5 = `python3 scripts/kg50_q5_branches.py --selftest` · `python3 scripts/kg50_q5_verdict.py --selftest`.
- `test_311_oldtool.log` 의 PASS 97 = 옛 시험 79 + 새 시험 18 (새 시험 중 예전 판도 거부하던 꼴 = 대조군) · FAIL 82 = 기대를 바꾼 옛 시험 8 + 새 시험 74 — 옛 · 새 나눔은 고친 사람 기록 (`docs/resume_ckpt_procedure_20260927.md` 개정 4 절) 이다.

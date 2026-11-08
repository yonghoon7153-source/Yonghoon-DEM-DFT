# 우리 트리 재현 — Codex Rint ② 재검토 회차 ③ (11-08)

- 무엇을: 판정문 (`docs/reviews/codex_review_rint2_rr_round3_20261108.md`) §2 · §3 · §4 · §6 이 든 탐침 6 개 (pc12_attack 1 · contracts 2 · s0_memory 3) 를 **고치지 않고** 다시 돌렸다 + 옛 회차 ② 탐침 재생 (`run_old_probe.py`) 하나 (요청 밖 · 1 초대).  탐침 = 반입 ZIP 을 리포 밖 빈 폴더에 푼 원본을 다 읽은 뒤 스크래치 실행 폴더로 복사한 것 (복사본 sha256 = 원본과 같음 · `docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/build_record.json`) · cwd = 리포 밖 빈 폴더 · `python3 -I -B -X utf8`.
- 우리 트리: `RINT_REVIEW_REPO` (s0_memory 셋은 인자) = **우리 git 의 핀 `17d45fb9cdfc7033bdfd41509527cea23ba1654c`** 를 리포 밖 임시 분리 작업 트리로 꺼낸 것 (`git worktree add --detach` · tree `6989fd20dca6fba46fcf5eb6955dc8e9f12f2586` · 깨끗함 · 실행 뒤 지움).  ZIP 의 package/repo 사본은 쓰지 않았다 (그 660 파일 = 핀 blob 과 같음 · 반입 README).  옛 기준 모듈 둘 = ZIP 사본이 아니라 우리 git 객체 (`3b12fbe2d:scripts/carbon_junction.py` sha256 5460dad1… · `39104710a:scripts/ca_s0_census.py` sha256 6e527e6c… = ZIP 사본과 같음).
- 환경 (우리) = Linux 6.18 · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · git 2.43.0 · 스레드 환경 변수 미설정.  환경 (Codex) = Windows 11 · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3.
- 탐침이 만드는 scratch Git · 임시 폴더 = 스크래치 실행 폴더 안 (리포 밖).
- ⚠ 프로세스 그룹 반환 (`run_in_group`) · 잠금 · 호스트 신원 · 그룹 정리 = 탐침 자신이 모의한다 — Linux 에서 돌렸어도 실제 SIGKILL · flock 경쟁 · `/proc` 권한 · FIFO · NFS · kgy 동작을 시험한 것이 **아니다**.  우리 Linux 에는 `os.O_NONBLOCK` 이 있어 탐침의 Windows 0 대체는 쓰이지 않았다.

## 결과 (탐침 · Codex 기록 · 우리 · 판정값 차이)

잎 대조 = 같은 JSON 의 잎마다 형 · 값 비교 (`docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/comparison.json` · 다른 잎마다 분류 · 분류 "OTHER" (판정값 후보) = **0**).  글 기록 = CRLF → LF 뒤 바이트 대조.  우리 산출물 = 이 폴더 (같은 상대 자리 · 실행 기록 `logs/<탐침>.stdout.log` · `.stderr.log` · `.rc.json`).

| 탐침 | Codex 기록 | 우리 | 판정값 차이 |
|---|---|---|---|
| `docs/reviews/codex_rint2_rr_round3_evidence_20261108/pc12_attack/probe_pc12_independent.py` (RR3-01 · PC11 · PC12) | rc 0 (= RR3-01 반례 존재 assert 통과) · 요청 255 수용 / 21 거부 · 끝 기록 175 행 (정직 25 · 변이 150) · ARM_JSON_COUNT 실패 런 → 요약 두 칸 편집 → cause check → timeout · resume_ok false → true · stop_record_problem None · 원장 resume_ok false → true · attempt_order_problem RESUME_NOT_ALLOWED → None · result_line_problem None / None · `_copy` 재판독 = ARM_JSON_COUNT | rc 0 · 같은 표 전부 | **0** — results.json 161 잎 중 154 같음 · 다른 7 = 환경 판 1 · 시각 / 초 3 · 시도 폴더 지문 2 · 합성 팔 파일 sha256 1 (Codex = Windows 글 쓰기라 `{}` 뒤 CRLF · 우리 = LF — 두 바이트의 sha256 을 다시 셈 = e3566b3a… · ca3d163b… = 각자 기록값) · chain_side_rows.json 1,225 / 1,225 · 요약 둘 22 잎 중 20 (초 · 팔 파일 sha256) · 원장 둘 37 잎 중 34 (임시 폴더 경로 · 폴더 지문 · 시각) |
| `docs/reviews/codex_rint2_rr_round3_evidence_20261108/contracts_probe.py` (RR2 · PC9 · PC10) | 105 / 105 | rc 0 · 105 / 105 | **0** — 524 잎 중 522 같음 · 다른 2 = 환경 판 |
| contracts_p2p4_git.py (원 PC12 p2 / p4 입력 → 실제 Git recover → 다음 자격 · 반입에서 뺀 ZIP 안 이름 · 우리 실행 사본 sha256 = 원본) | 12 / 12 (p2_1a–1c · 2a–2c · p4 셋 = RESUME_NOT_ALLOWED · 정직 timeout · signal · GU rc0 = 허용) | rc 0 · 12 / 12 · 같은 원인 · 자격 | **0** — 720 잎 중 677 같음 · 다른 43 = 결과 줄 시각 12 · 시도 폴더 지문 12 · 합성 fixture 커밋 번호 12 · 그룹 끝 시각 4 · 환경 판 2 · scratch 경로 1 · 사례 로그 12 / 12 = LF 뒤 바이트 같음 |
| `docs/reviews/codex_rint2_rr_round3_evidence_20261108/s0_memory/probe_s0_memory.py` (SELF-155 후보 완전성 · 경계 예외 · 동률) | 575 / 575 | rc 0 · 575 / 575 | **0** — 2,297 잎 중 2,294 같음 · 다른 3 = 파이썬 · numpy · scipy 판 (경계 예외 거리 0.19999999999999996 · 옛 반지름 · 후보 수 같음) |
| `docs/reviews/codex_rint2_rr_round3_evidence_20261108/s0_memory/probe_plan_binding.py` (도구 sha 만 바뀌면 계획 sha 바뀜 · 옛 carbon 지문 거부) | passed True | rc 0 · True | **0** — 18 / 18 잎 같음 |
| `docs/reviews/codex_rint2_rr_round3_evidence_20261108/s0_memory/run_targeted_memory.py` (상주 carbon 9 묶음 · S0 M) | carbon 55 / 55 · S0 19 / 19 | rc 0 · 55 / 55 · 19 / 19 (50.2 초) | **0** — 두 로그 = LF 뒤 바이트 같음 · 요약 20 잎 중 16 같음 · 다른 4 = 기준 파일 경로 2 + 기준 사본 sha256 2 (Codex 첫 실행 사본 = 고정 원문 + 끝 LF 하나 · REPRODUCE.md 가 공개 · 그 바이트를 다시 만들면 a387402c… · aa386bfe… = Codex 기록값 · 우리 = 고정 원문 그대로) |
| `docs/reviews/codex_rint2_rr_round3_evidence_20261108/run_old_probe.py` (회차 ② 탐침 기대 그대로 · 역사 report_c 두 검사 빼기 · 요청 밖) | rc 1 · 301 / 309 · 다른 8 = 판정문 §4 기대 변경 8 | rc 1 · 301 / 309 · 같은 8 FAIL 줄 | **0** — 로그 = 마지막 환경 줄만 다름 · results.json 1,401 잎 중 1,397 같음 (다른 2 = 환경 판 · 원천 sha256 칸 이름의 경로 구분자 2 = 값 같음) · residual_rc 66 / 66 · candidate_fix 42 / 42 · residual_rc_integration 57 잎 중 45 (다른 12 = 결과 줄 시각 3 · 폴더 지문 3 · 원장 · 시도 경로 6) · 적응 사본 sha256 다름 (REPO 경로 글 · Windows 한 줄) |

## 돌리지 않은 것

- `docs/reviews/codex_rint2_rr_round3_evidence_20261108/replay_preattack12.py` (사전 공격 12 원 탐침 전체 fixture 재생 · Codex = Windows symlink 권한으로 p2 / p4 중단) — 요청 범위 밖 · 같은 원 탐침의 우리 쪽 재실행 = `docs/reviews/rint2_rr2_fix_evidence_20261105/pc12_fix/probe_rerun/` (고침 반입 때).
- ZIP 안 `docs/reviews/codex_rint2_rr_round3_evidence_20261108/verify_evidence.py` · `docs/reviews/codex_rint2_rr_round3_evidence_20261108/package_evidence.py` — 실행하지 않았다 (매니페스트 735 줄 · package/ 대조는 우리 스크립트 · 반입 README).
- 실제 SIGKILL · flock 경쟁 · `/proc` 권한 · FIFO · NFS · GPU · kgy 3.8.10 · 실침대 S0 · 등록 R · 전체 게이트.

⇒ **판정값 차이 0** — RR3-01 (실제 `read_run` 실패 기록 + 요약 두 칸 편집 → resume_ok true · 다음 원장 항목 허용 · 실제 `_copy` 재판독 = 거부) 이 우리 핀 · 우리 Linux 에서도 같다 · PC12-01 · 02 · 04 · 05 · PC11-01–04 · RR2 · PC9 · PC10 계약 105 · 원 p2 / p4 Git 12 · S0 575 · 55 · 19 · 계획 결속 · 옛 탐침 301 / 309 도 같다.

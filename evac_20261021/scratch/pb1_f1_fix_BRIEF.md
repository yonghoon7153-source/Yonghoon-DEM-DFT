# PB1 F1 — scaffold step 선언의 숫자 뒤 꼬리 (시험 먼저 → 수정 · 작업 트리 · push 안 함 · 10-20)

## 기반
- 너의 작업 트리에서 `git reset --hard 952ad1a25` → `git log -1` 확인.  `git fetch` 하지 않는다.
- 봉인 확인: `scripts/rint_iface_join.py` 는 `scripts/run_network_194_parallel.py` 의 `CODE_FILES` 32 · `scripts/seal_s3_prerun.py` 의 `NUMERIC_MODULES` 6 에 없다 (확인만 · 있으면 멈추고 보고).
- 고칠 파일 = `scripts/rint_iface_join.py` · 시험 = `scripts/test_rint_g2_join.py` 뿐.

## 결함 (사전 공격 리뷰 · 재현 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prerev_pb1/repro_min.py` · 결과 `repro_min.out` — 읽기만 · 그 스크립트는 지워진 작업 트리 경로를 기대하니 실행하지 말고 입력 꼴만 가져온다)
- v5 (`263c9502b`) 의 scaffold step 선언 읽기가 숫자 뒤 꼬리를 버린다: 머리줄 `# step 2060000.9` (덤프 2060000) · `# step 100_000` · `# step 1e6` (덤프 1) · `# step 100²` · `# step 100x` = **PASS · 주장 "G-frame 까지" · 계획 · 정량 관문 ACCEPT** (v4 도 같음).  대조: `# step 100١` = REJECT (v5 J18 ④).  같은 부류 = RIMPR-03 · RIMP-02 e3 (`2060000.9` 를 거부하는 원칙).
- 권고 수정 (공격 리뷰): `_STEP_DECL_RE = r'(?:time)?step\s*[=:]?\s*(\d\w*(?:\.\w+)*)'` (re.I) — 선언 토큰을 숫자 뒤 글자 · 안쪽 점까지 넓혀 엄격 fullmatch (ASCII 정수 · int64) 가 실패하게.  실제 생산 꼴은 그대로 통과해야: heckel LOOSE 머리줄 `step 405000 = …` · 문장 끝 `.` (`# compacted at step 100.`) · `,`.  (선택 · 같은 커밋: 왼쪽 경계 — `# laststep 100` 을 step 100 으로 읽지 않게.)  권고는 출발점일 뿐 — 지금 코드를 읽고 같은 뜻으로 가장 작게 고친다.
- 비차단 관찰 (고치지 않음 · 보고만): 같은 정규식의 긴 공백 2 차 백트래킹 (공백 8,000 칸 0.9 s · v4 부터).

## 커밋 1 — 시험 먼저 (`scripts/test_rint_g2_join.py` 만)
- J18 에: `# step 2060000.9` · `# step 100_000` · `# step 1e6` · `# step 100²` · `# step 100x` → `int_token` (`scaffold_step`) 거부 + 소비자 차단 · (왼쪽 경계를 고치면) `# laststep 100` → 선언 아님 · 양성: `# compacted at step 100.` · `# step 100,` · LOOSE 머리줄 원문 (리포 heckel scaffold 의 실제 줄 — 찾아서) → PASS · 기존 J18 양성 그대로.
- **고치기 전 코드 (v5) 에서 돌려** 새 반례가 실패하는 것을 확인 → 커밋 메시지에 "pre-fix N/M (fails = K checks from the J new counterexamples, each = entrance + consumer)" — 반례 수와 검사 수를 따로 적는다 (`SELF-124` 부류 · 지난 커밋 메시지의 "fails = the 39 new counterexamples" 는 실패 검사 78 = 39 × 2 였다).

## 커밋 2 — 수정 (`scripts/rint_iface_join.py` 만)
- 위 정규식 · `JOIN_VERSION` v5 → **v6** (행동이 바뀐다 · 기록 판 = 행동 판).
- ⚠ **본 트리 게이트가 끝나기 전 (≈ 14:30 UTC) 무거운 시험 금지** — 그 전엔 코드 · 시험 작성 · 작은 확인만.  그 뒤: `scripts/test_rint_g2_join.py` 전부 (N/N) · 옛 138 판 (`git show 2b9efa253:scripts/test_rint_g2_join.py`) 을 고친 모듈에 · `scripts/test_rint_g2_am_iface.py` · `scripts/test_rint_g2_rrm.py` · `scripts/test_rint_t4_census.py` · `scripts/test_rint_t43_order.py` · `scripts/test_rint_t2_dev.py` · `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `python3 scripts/rint_t41_census.py --selftest` · real14 · case15 조인 = v5 와 배열 (particles 3 · atom_id_of_row · dem_am_am 6) · `delta_bound_um` 바이트 같음 · 리포 scaffold 중 조인이 읽는 36 개 = v5 와 값 같음 (heckel LOOSE 포함 — step 값 같음).
- Codex 탐침 넷 (`docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/`) — 먼저 전부 읽고 · 네트워크 · 묶음 밖 쓰기 · 삭제 · 임의 subprocess 없을 때만 스크래치 `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/pb1_f1/` 로 복사 · 경로 상수만 바꿔 `python3 -I -X utf8 -B` — v5 대비 판정 차이 0 이어야 (scaffold step 꼬리 꼴이 탐침에 없으면 그대로).

## 규칙
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 문서 · 원장 · CLAUDE.md · 진행 기록은 고치지 않는다 (메인이 한다) · 디스크 적게 (임시 = 위 스크래치 · 쓰고 지움 · 큰 사본 금지).
- 커밋 메시지 영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 1 · 2 SHA · 고치기 전 → 뒤 (반례 수 · 검사 수 · 실패 집합) · 회귀 표 · real14 · case15 · scaffold 36 · 탐침 넷 · 새 사유 칸 (있으면) · 남은 것.

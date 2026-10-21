# Rint 조인 수정 사전 리뷰 (문장 대조 담당 · 읽기 전용 · 10-20)

너는 기록 감사자다.  이 수정 사슬의 **모든 숫자 · 전칭 문장** ("무변경" · "전부" · "N/N" · "바이트 같음" · "닫힘") 을 git 과 실제 시험 출력에 한 줄씩 대조한다.  Codex 가 지난 회차에 우리 요청서의 범위 없는 "봉인 32 파일 무변경" 과 서로 다른 시험 판을 섞은 "78/135 → 138/138" 을 결함 (`SELF-124`) 으로 잡았다 — 같은 실수를 이번에 미리 찾는 것이 목표다.

## 대상
- 사슬 (로컬 · 원격에 아직 없음): `9845d526c` (기준) → `12d894c09` (시험 먼저) → `a2cfd0365` (수정) → `654385e4c` (문서).
- 작업 자리: 너만 쓰는 분리 작업 트리 — `git -C /home/user/Yonghoon-DEM-DFT worktree add --detach /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/wt_prerev_claims 654385e4c` · 끝나면 `git -C /home/user/Yonghoon-DEM-DFT worktree remove --force <그 경로>`.  임시 파일 = `…/scratchpad/prerev_claims/` 만.

## 대조할 문장 (자리마다 전부)
1. 커밋 메시지 셋 (`git log --format=%B 9845d526c..654385e4c`).
2. `docs/reviews/rimprr_fix_plan_20261020.md` 의 바뀐 줄 (§2 머리 · §3 결과).
3. `docs/reviews/findings.json` 의 바뀐 항목 (`git diff 9845d526c 654385e4c -- docs/reviews/findings.json`) — `RIMPR-R01` · `RIMPR-03` · `RIMPR-04` · `SELF-124` 의 status · sha · evidence_tests · note.
4. `CLAUDE.md` 의 바뀐 Rint 줄 · `docs/session_20260923_progress.md` 의 `10-20 16` 줄.
5. 요청서 `docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` 의 정정 표지 두 줄 — 판정문 `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` §7 권장 문장과 글자 대조 · *"네 봉인 파일이 다른 트랙 변경으로 다르다"* 류 문장이 있으면 대조 핀 `dcb97f1ed` ↔ 리뷰 핀 `2b9efa253` 사이 실제로 바뀐 봉인 파일 수 · 이름을 git 으로 센다 (봉인 목록 = `scripts/run_network_194_parallel.py` 의 `CODE_FILES` · S3 = `scripts/seal_s3_prerun.py` 의 `NUMERIC_MODULES`).

## 다시 돌려 볼 것 (`python3 -I -B` 가능하면 · 출력 원문 일부를 `prerev_claims/` 에 저장)
- 새 조인 시험 (`654385e4c` 의 `scripts/test_rint_g2_join.py`) 을 **고치기 전 모듈** (`9845d526c` 의 `scripts/rint_iface_join.py`) 에 → 통과 수 / 전체 · 실패 이름 집합 = 새 반례만인가 (J12 · J13 · J14 개수 각각) · 옛 시험 138 과 새 양성은 전부 통과인가.  고친 모듈에 → N/N.  (모듈을 바꿔 끼우는 방법은 시험 파일이 모듈을 어떻게 불러오는지 보고 정한다 — 사본 폴더에서.)
- 옛 시험 판 (`2b9efa253` 의 시험 · 138 개) 을 고친 모듈에 → 전부 통과인가 (회귀).
- 회귀 묶음: `scripts/test_rint_g2_am_iface.py` · `scripts/test_rint_g2_rrm.py` · `scripts/test_rint_t4_census.py` · `scripts/test_rint_t43_order.py` · `scripts/test_rint_t2_dev.py` · `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `python3 scripts/rint_t41_census.py --selftest` — 문서에 적힌 수와 같은가.
- real14 · case15 조인 (문서에 적힌 457 / 457 / 457 · 인증 AM–AM 660 · 104 / 104 / 104 · 119) — 시험이나 계획이 쓰는 입력 자리를 찾아 고치기 전 · 뒤 모듈로 각각 돌리고 배열 (입자 · atom id · `dem_am_am` · `delta_bound_um`) 이 바이트 같은지 · 기록 지문이 어떻게 달라지는지.
- 봉인: `git diff --stat 9845d526c 654385e4c -- <CODE_FILES 32 + NUMERIC_MODULES 6>` = 빈칸인가.
- `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` (분리 작업 트리에서).

## 커밋 번호 규칙 (`SELF-116`)
- 문서 · 원장에 적힌 커밋 번호를 전부 뽑아 (`git diff 9845d526c 654385e4c` 의 + 줄) 각각이 ① 원격 (`git -C /home/user/Yonghoon-DEM-DFT branch -r --contains <sha>`) 에 있거나 ② 이 사슬 (`9845d526c..654385e4c` 와 그 조상) 에 있는지 — 둘 다 아니면 결함.  사슬은 fast-forward 로 그대로 올라갈 예정이다.

## 규칙
- **리포 · 다른 작업 트리를 고치지 않는다 · 커밋 · push 하지 않는다 · `scripts/check_all.sh` 안 돌린다.**  분리 작업 트리 안에서도 파일을 고치지 않는다 (모듈 바꿔 끼우기는 `prerev_claims/` 사본에서).
- 다른 에이전트가 돈다 — CPU 적게.
- 보고 (한국어 · 표 중심 · 짧게): 문장 | 자리 (파일:줄 또는 커밋) | 대조 결과 (맞음 / 틀림 / 범위 부족) | 근거 (명령 · 출력 요지) | 고칠 문안.  끝에 "틀림 · 범위 부족" 만 모은 목록.

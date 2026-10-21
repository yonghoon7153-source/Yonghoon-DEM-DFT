# PB1 조인 같은 부류 보강 (시험 먼저 → 수정) + 기록 · 결정 표지 (1저자 10-20 *"다 권고대로 해"*) — 작업 트리 · push 안 함

## 기반
- `git reset --hard tmp-rq7-int` (로컬 가지 = `d1768cf0c` · 부모 `b694369b5` → `f507bdc74` (원격)) → `git log -3 --oneline` 확인.  `git fetch` 하지 않는다.
- 1저자 10-20 *"다 권고대로 해"* = Rint ② 설계 §10 의 **N1–N18 전부 권고대로 + PB1 (조인 같은 부류 보강 다섯 = 지금 고침)**.  (앞서 *"ㅇㅇ 권고대로 해"* = 통합 계획 Q1–Q12 · *"권고대로해"* = 조인 수정 계획 Q1–Q6.)
- 사전 리뷰 요지 (먼저 전부 읽는다): `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prerev_join_findings_summary.md` (PB1 다섯 · 한정 목록 · 문장 정정 A–K).  반례 입력 · 검증된 수정 사본 (참고만 · 그대로 베끼지 말고 시험 먼저 순서를 지킨다): `…/scratchpad/prerev_attack/attack_header.py` · `attack_numeric.py` · `attack_misc.py` · `attack_gaps.py` · `attack_lib.py` · `fix_variants/F2.diff` · `F2_full_suite.json`.  ⚠ 그 스크립트들은 지워진 작업 트리 경로 (`wt_prerev_attack`) 를 박고 있다 — 입력 꼴만 읽고 실행하지 않는다.
- ⛔ 먼저 봉인 확인: `scripts/rint_iface_join.py` 가 `scripts/run_network_194_parallel.py` 의 `CODE_FILES` · `scripts/seal_s3_prerun.py` 의 `NUMERIC_MODULES` 에 없는지 — 있으면 멈추고 보고.

## 커밋 1 — 시험 먼저 (`scripts/test_rint_g2_join.py` 만)
- 새 묶음 (이름은 기존 J 번호 다음): ① 표지 경계 — `ITEM: ATOMS` · `BOX BOUNDS` · `ENTRIES` 바로 뒤 · `ITEM: TIMESTEP` 끝에 U+00A0 · U+3000 · U+2003 · U+001F (4 × 4 = 16) → 거부 (`frame_layout`) ② 어휘 — 머리 열 사이 · 행 · 상자 줄 · step/count 값의 NBSP · U+3000 · U+001F · 줄 끝 FF · VT · NEL · U+2028 (13) → 거부 ③ scaffold 실수 열 x · y · z · r 에 전각 · 아라비아-인도 숫자 · 밑줄 · 유니코드 공백 덧붙임 (5) → 거부 + 양성: 주석 줄의 U+2014 는 그대로 통과 (case15 scaffold 꼴) ④ `_STEP_RE` — scaffold 머리줄 `# step １００` 꼴 → 거부 · 긴 ASCII step 은 정상 처리 ⑤ J13 에 f6 `wd` 만 넘치는 꼴 한 줄 (같은 x 의 두 SE 구 · δ 틀림 — 사전 리뷰 ② 7번).
- 기존 J13 머리 출력 문구 정정 (H): *"고치기 전 = 조인 PASS (① 정량 ACCEPT · ③④ 는 계획이 이미 join_particles_mismatch) · 1e150 대조 = REJECT"*.
- 양성 그대로 (거짓 거부 방지): real14 · case15 원 gz · LIGGGHTS 꼴 머리 (`… ix iy iz vx … omegaz radius ` 끝 공백) · `1e-05` · `-0` · `5` · 추가 열 · 탭 · 겹 공백 · CR 만 · CRLF/LF 섞임 · gzip 두 멤버 · `mm` · `fs` · `sm` 플래그.
- **고치기 전 코드에서 돌려** 새 반례가 실패하는 것을 확인 → 커밋 메시지에 "pre-fix N/M (fails = the K new counterexamples)" — 판 · 시험 수 · 실패 집합을 한 판으로 적는다 (`SELF-124`).

## 커밋 2 — 수정 (`scripts/rint_iface_join.py` 만)
- 표지 경계 = 줄 끝 · 공백 · 탭만 (`isspace()` 금지) · 덤프 글자 어휘 관문 (TAB · LF · CR · 0x20–0x7E 밖 = `frame_layout` · 새 셈 칸 예 `lexical` · 기록 · `join_gate_failed` 전파) · scaffold 주석 아닌 줄 = 어휘 관문 + 실수 열 ASCII 고정소수 문법 (`[+-]?[0-9]+(\.[0-9]+)?` 꼴 — 실제 생산 scaffold 값 꼴 (지수 표기 있나) 을 먼저 확인해 거짓 거부 없게) · `_STEP_RE` ASCII · `JOIN_VERSION` v4 → v5.
- 회귀 전부: `test_rint_g2_join.py` (새 시험 포함 전부 · N/N) · 옛 138 판 (`git show 2b9efa253:scripts/test_rint_g2_join.py`) 을 고친 모듈에 · `test_rint_g2_am_iface.py` · `test_rint_g2_rrm.py` · `test_rint_t4_census.py` · `test_rint_t43_order.py` · `test_rint_t2_dev.py` · `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `python3 scripts/rint_t41_census.py --selftest` · real14 · case15 조인 = 고치기 전과 배열 (입자 · atom id · `dem_am_am` · `delta_bound_um`) 바이트 같음 · iface 끔 무영향.
- Codex 탐침 넷 재실행 (`docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/` 의 `structure_probe.py` · `structure_minimal_replay.py` · `numeric_review.py` · `numeric_overflow_replay.py` — 먼저 전부 읽고 · 네트워크 · 묶음 밖 쓰기 · 삭제 · 임의 subprocess 없을 때만 · 스크래치로 복사 · 경로 상수만 · `python3 -I -X utf8 -B`) → 기대: 헤더 10 거부 · 1e160 거부 · 전각 정수 거부 · 그 밖 판정 그대로 (바뀐 것이 있으면 이유를 표로).
- 웹앱 화면 없음 (확인만).
- ⚠ 임시 폴더 (real14 사본 등) 는 쓰고 바로 지운다 — 디스크 여유가 작다 (지난번 600 MB 사본으로 ENOSPC).

## 커밋 3 — 기록 · 결정 표지
1. 원장 `docs/reviews/findings.json` (`json.dumps(d, ensure_ascii=False, indent=2) + '\n'`): `RIMPR-R01` · `RIMPR-03` note = 같은 부류 보강 (커밋 2) · sha 를 커밋 2 로 · `RIMPR-04` open 유지 + note 에 한정 목록 (요지 파일) · `SELF-124` note 정정 (A · B · E · D 의 처리) · 새 `SELF-125` (P3 · claimed_fixed = 커밋 3) = *"내부 사전 리뷰 (10-20) 가 찾은 우리 기록의 과장 · 범위 부족 11 곳 (A–K)"* — 항목 · 자리 · 정정 한 줄씩 (G 는 커밋 메시지라 못 고침 = 기록만).  `python3 scripts/check_review_findings.py` ✓.
2. 조인 요청서 `docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` — B · C · D · E 정정 표지 (원문 지우지 않음).
3. 조인 수정 계획 `docs/reviews/rimprr_fix_plan_20261020.md` — 제목 (I) · §3 끝에 PB1 결과 몇 줄 (커밋 1 · 2 SHA · 고치기 전 → 뒤 · 회귀 · 탐침).
4. Rint ② 문서 셋 (`docs/reviews/rint_carbon_additive_design_v1_20261020.md` · `…_registration_R_draft_20261020.md` · `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md`) — `⬜ 1저자 (권고)` 표지를 전부 `✅ 1저자 10-20 *"다 권고대로 해"*` 로 (권고안 본문은 그대로 · 바뀐 줄 수 기록) · 설계 §10 머리에 한 줄 · 요청서 Part B 의 보강 커밋 자리 = 커밋 1 · 2 SHA · 결과 수 · 탐침 결과 · 리뷰 핀 자리는 *"⬜ push 뒤 메인이 기록 (이 요청서가 들어간 커밋)"* 로 남긴다.
5. 통합 계획 `docs/reviews/rint_carbon_additive_plan_20261020.md` — N8 의 정정 표지 넷 (설계 §10 N8 이 가리키는 자리 그대로 · 원문 지우지 않음).
6. `CLAUDE.md` Rint 줄 — (J) 문구 정정 + PB1 + Rint ② N1–N18 ✅ + 설계 요청서 (사전 리뷰 두 회차 · 발송 = 1저자) 를 한 번만 나오는 문자열 자리에.
7. 진행 기록 `docs/session_20260923_progress.md` — 1138 행 (K) 정정 + 끝에 `- **10-20 19 (PB1 조인 보강 · Rint ② N1–N18 결정)**: …` 한 줄.
8. `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` 통과.

## 규칙
- push 안 함 · `scripts/check_all.sh` 안 돌림 (메인에서 게이트가 돈다 — CPU · 디스크 적게) · 고치는 코드 = `scripts/rint_iface_join.py` · 시험 = `scripts/test_rint_g2_join.py` 뿐 (다른 코드가 필요하면 멈추고 보고) · 커밋 메시지 영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 원격에 없는 커밋 번호를 문서에 쓰지 않는다 (`SELF-116`) — 이 사슬 (`d1768cf0c` 와 조상 · 네 커밋 1 · 2) 은 fast-forward 로 올라간다 · 커밋 3 이 자기 SHA 를 쓰지 않는다.
- 보고 (한국어 · 짧게 · 표): 커밋 1 · 2 · 3 SHA · 봉인 확인 · 고치기 전 → 뒤 시험 수 (실패 집합) · 회귀 표 · real14 · case15 · 탐침 넷 · 새 사유 칸 · 원장 변화 · 결정 표지 바꾼 수 · 남은 ⬜.

# Rint 조인 RIMPR-R01 · RIMPR-03 · RIMPR-04 수정 (1저자 10-20 *"권고대로해"* = Q1 (가) · Q2 (가) · Q3 (가) · Q4 (가) · Q5 반영 · Q6 (나)) — 작업 트리 · 시험 먼저 · push 안 함

## 기반 · 먼저 읽을 것
- `git reset --hard tmp-rq7-int` (로컬 가지 · `9845d526c` = 병합 HEAD `10173a053` + Codex Rint 재확인 반입) → `git log -2 --oneline` 확인.  `git fetch` 하지 않는다.
- 계획 `docs/reviews/rimprr_fix_plan_20261020.md` (§1 · §2 · §3 전부) · 판정문 `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` §3 · §4 · 증거 `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/` (`evidence/structure_results.json` 의 헤더 false-PASS 10 건 입력 · 기대, `probes/structure_minimal_replay.py` · `probes/numeric_overflow_replay.py` 의 반례 꼴) · 원장 `RIMPR-R01` · `RIMPR-03` · `RIMPR-04` · `SELF-124`.
- ⛔ 먼저 봉인 확인: `scripts/run_network_194_parallel.py` 의 `CODE_FILES` (32) 와 S3 `NUMERIC_MODULES` 에 `scripts/rint_iface_join.py` 가 **없는지** 확인 — 있으면 아무것도 고치지 말고 멈추고 보고.

## 커밋 A — 시험 먼저 (`scripts/test_rint_g2_join.py` 만)
- Q2 (가): Codex 헤더 반례 10 건 전부 (ATOMS · ENTRIES 이름과 첫 열 붙임 · BOX BOUNDS 와 첫 플래그 붙임 · 표지 반복 · 후첨 · 판정문 §3 최소 반례 둘 문자열 그대로 · contact `ENTRIES` 대응) → 기대 = 구조화 거부 (계획 Q1 의 예상 사유: `frame_layout` · `box_format` · `row_width` 등 — 실제 고친 코드가 내는 사유로 맞추되 **PASS 가 아니어야** 한다) · `join_gate_failed` 가 계획 · 정량 관문까지 전파.
- Q3: 1e160 반례 (정상 AM 둘 + SE 둘 x = 1e160 · 2e160 sim · r 0.001 · 상자 0 … 3e160 · 접촉 δ 0.0005 — 판정문 §4 표) → 기대 = 구조화 거부 (새 사유 코드) · 1e150 대조 = 지금처럼 거부 (n_delta_pos_mismatch) 유지.
- Q4: 전각 숫자 (원자 ID · type · step · count · 접촉 ID · scaffold type) → 기대 = `int_token` 거부.
- 정상 양성 그대로 (real14 · case15 · 접촉 0 행 · gzip · CRLF · 기존 빈 줄 규약 · D19 · 쓰지 않는 진단 열 · 공백 · 탭).
- **고치기 전 코드에서 돌려** 새 반례가 실패하는 것을 확인 → 판 · 시험 수 · 실패 집합을 그대로 적는다 (`SELF-124` 교훈 — 시험 집합을 섞어 적지 않는다).  커밋 메시지에 "pre-fix N/M (실패 = 새 반례 K 건)".

## 커밋 B — 수정 + 요청서 정정
- `scripts/rint_iface_join.py`:
  - Q1 (가): 머리 줄을 `ITEM:` 뒤 낱말로 토큰화 → 구역 이름 (`TIMESTEP` · `NUMBER OF …` · `BOX BOUNDS` · `ATOMS` · `ENTRIES`) 을 **정확한 단어 경계**로 대조 → 표지 하나만 앞에서 제거 → 나머지 토큰은 기존 열 · 상자 검사로 (공백 · 탭 · 쓰지 않는 진단 열 허용 그대로).
  - Q3 (가): `:641–645` 의 거리 · 허용폭 (와 같은 부류 `:767` 반올림 폭 · `:799` 면적 — 계획 표) 이 유한이 아니면 구조화 거부 (새 사유 코드 · 기록 · `join_gate_failed` 전파).  안정한 `hypot` 재작성은 **하지 않는다** (정량 채택 전 몫).
  - Q4 (가): `_INT_RE` 의 `\d` → `[0-9]`.
- 회귀 전부: `test_rint_g2_join.py` (새 시험 포함 전부) · `test_rint_g2_am_iface.py` 136/136 · `test_rint_g2_rrm.py` 55/55 · `test_rint_t4_census.py` 8/8 · `test_rint_t43_order.py` 6/6 · `test_rint_t2_dev.py` 23/23 · `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `python3 scripts/rint_t41_census.py --selftest` · real14 · case15 조인 결과 그대로 (457 / 457 / 457 · 104 / 104 / 104 · 인증 AM–AM 660 · 119) · iface 끔 무영향.
- 웹앱: 이 조인을 보여 주는 화면이 있는지 확인 — 없으면 보고에 "웹앱 화면 없음".
- Q5 (같은 커밋 B 에 문서 정정): 요청서 `docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` 의 *"봉인 32 파일 무변경"* 줄 · *"78/135 → 138/138"* 줄 — 원문은 지우지 않고 정정 표지 (예: `⛔ 정정 10-20 (SELF-124 · Codex §7): …`) 로 판정문 §7 권장 문장 (*"이번 Rint 수정 두 커밋은 봉인 32 개를 변경하지 않았다. 대조 핀 이후의 다른 트랙 변경까지 포함한 전체 스냅샷의 동일성은 별도다."*) 과 *"78/135 = 시험 작성 중간 시점 135 개 · 현재 시험 138 개를 옛 코드에 = 81/138"* 구분.

## 커밋 C — 원장 · 계획 · 기록
- 원장 (`json.dumps(d, ensure_ascii=False, indent=2) + '\n'`): `RIMPR-R01` open → claimed_fixed (sha = B) · `RIMPR-03` open → claimed_fixed (B) · `RIMPR-04` **open 유지** + note "★ 10-20 부분 수정 (B): 파생 거리 · 허용폭 · 반올림 폭 · 면적 비유한 = 거부 (1e160 반례 상주) · 안정한 hypot · 결과 유한성 전반 = 정량 채택 전 (Codex 연기 조건 ④)" · `SELF-124` open → claimed_fixed (B) · `check_review_findings.py` ✓.
- 계획 문서 §2 머리에 `✅ 1저자 10-20 *"권고대로해"* — Q1 (가) · Q2 (가) · Q3 (가) · Q4 (가) · Q5 반영 · Q6 (나)` + §3 아래 결과 몇 줄 (A · B SHA · 고치기 전 → 뒤 시험 수 · 회귀 표).
- `CLAUDE.md` Rint 줄: 문자열 `→ ⬜ 수정 계획 \`docs/reviews/rimprr_fix_plan_20261020.md\` Q1–Q6 = 1저자 →` (정확히 한 번) 을 `→ ✅ 수정 계획 \`docs/reviews/rimprr_fix_plan_20261020.md\` Q1–Q6 = 1저자 10-20 권고대로 → ✅ **수정 10-20 (시험 먼저 \`A\` · 수정 \`B\` — RIMPR-R01 정확한 구역 이름 · 표지 한 번 · RIMPR-03 \`[0-9]\` · RIMPR-04 파생값 비유한 = 거부 (안정한 hypot = 정량 채택 전 · open 유지) · 조인 시험 고치기 전 → 뒤 · 회귀 전부 · 원장 claimed_fixed)** → Codex 재확인 = Rint ② 설계 리뷰 회차 (Q6 (나)) →` 로 (A · B 는 실제 짧은 SHA).
- 진행 기록 `docs/session_20260923_progress.md` 끝에 `- **10-20 16 (Rint RIMPR-R01 · 03 · 04 수정)**: …` 한 줄.
- `python3 scripts/check_doc_refs.py` · `check_review_findings.py` 통과.

## 규칙
- push 안 함 · `scripts/check_all.sh` 안 돌림 · 고치는 코드 = `scripts/rint_iface_join.py` · 시험 = `scripts/test_rint_g2_join.py` 뿐 (다른 코드가 필요하면 멈추고 보고) · 커밋 메시지 영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 메인에서 게이트와 다른 반입 에이전트가 돈다 — CPU 적게, 시험은 필요한 것만.
- 보고 (한국어 · 짧게 · 표): 커밋 A · B · C SHA · 봉인 확인 · 고치기 전 → 뒤 시험 수 (실패 집합) · 회귀 표 · real14 · case15 · 새 사유 코드 · 웹앱 · 원장 변화.

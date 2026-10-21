# Codex Rint 조인 재확인 판정 반입 (검토 핀 `2b9efa253` · 대조 핀 `dcb97f1ed` · 10-20) — 작업 트리에서 커밋 하나 (push 안 함)

## 받은 것
- 묶음 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/import_rq7/raw/2368c040-codex_rint_join_rimpr_q7_recheck_20261020_review.zip`
  (sha256 `970690f42865dc74d164866f02b68953e532d099561c83e1c0d60d7f6b762cc2` · 2,231,651 B · 1,307 항목 · 위험 경로 0 · Codex "전달용 증거 ZIP".  소스 포함 전체 묶음 83.7 MB 는 받지 않았다).
- 뿌리: `PACKAGE_MANIFEST.json` · `rint_join_q7_recheck_20261020/` (판정문 `codex_review_rint_join_rimpr_q7_recheck_20261020.md` · README_COMPACT · README_REVIEW · notes/ · probes/ · evidence/ · submitted/) · `rint_g2_impl_reverify_20261015/` (이전 10-15 검토 폴더 사본 = 옛 반례 원본 바이트).
- ⚠ 외부 자료 — 풀기는 새 빈 폴더 (`…/scratchpad/import_rq7/x/`) · 읽기는 `python3 -I` · 절대 경로 · `..` · 링크 = 거부.

## 판정 요지 (정본 = 묶음 안 판정문)
- RIMPR-01 · 02 = 이전 최소 해결 조건 **범위 한정 닫힘** · Q7 (일반 관문 r_face 유한·비음수) **닫힘** · 새 P1 · P2 없음 · ①′ 정량 채택 · 생산 HOLD 그대로.
- 새 **P3 `RIMPRR-01`** (§3): `scripts/rint_iface_join.py:278–279` · `:298` · `:302` — 구역 분류 `startswith()` + 헤더에서 표지를 `replace()` 로 전부 지움 → `ITEM: ATOMSid …` · `ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS` 가 PASS / 정량 ACCEPT (소비 배열은 정상과 같음 · σ 오염 증거 아님 · 대조 핀에서도 발생 = 회귀 아님) · 최소 해결 = 정확한 단어 경계 검사 + 표지 한 번만 앞에서 제거 + 두 사례 + contact 대응 사례 상주.
- `RIMPR-04` 범위 보강 (§4): 비-AM (SE 두 구 x 1e160) 거리·허용폭 norm = inf → `dd > wd` 가 `inf > inf` 거짓 → 조인 PASS / 정량 ACCEPT (`rint_iface_join.py:641–645`) · *"후단이 반드시 거부하므로 무해"* 설명 철회 · 새 ID 아님 · 연기 조건 네 개 (§4 끝).
- `RIMPR-03` (전각 숫자) = ASCII 생산 덤프 범위 명시 + open 유지면 연기 가능.
- §1 시험 수: 현재 시험 138 개를 옛 코드에 = 81/138 (57 실패) — 요청서의 78/135 와 같은 집합처럼 혼용 금지.  §7 *"봉인 32 무변경"* = 두 Rint 커밋 (`3b9d51789` · `2b9efa253`) 한정 — 대조 핀 → 검토 핀 전체 구간에서는 네 파일이 다름 (`scripts/network_conductivity.py` · `scripts/tau_flux.py` · `webapp/app.py` · `webapp/pipeline_service.py`) · 권장 문장 = §7 인용문.

## 할 일 (작업 트리 · 커밋 하나)
0. `git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8` → `git reset --hard origin/claude/sdcp-dem-manuscript-si-pqwtv8` (= `d8808c164` 인지 확인 · 원장 769 건) — 이 가지 위에서 작업한다.
1. 묶음 목록 (sha256 · 크기 · 위험 경로) → 새 빈 폴더에 풀기 → `_members_mini.tsv` (sha256 · bytes · status keep/verdict/meta/dup-repo · path).
2. 판정문 → `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` (**바이트 그대로** · `cmp`).
3. 증거 폴더 `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/` = `rint_join_q7_recheck_20261020/` 내용 (판정문 제외) + `PACKAGE_MANIFEST.json` + `_members_mini.tsv` + `_README_import.md` (앞선 반입 `docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/_README_import.md` 꼴: 판정문 sha256 · 받은 것 · 뺀 것 · 처리 · 우리 트리 재현 · 폴더 꼴 · 참조 예외 · 원장).
   - `rint_g2_impl_reverify_20261015/` 파일은 리포의 10-15 판정문 · 증거 폴더와 바이트 대조 → 같으면 `dup-repo` (넣지 않음 · 리포 경로 기록) · 다르면 증거 폴더 아래 `baseline_20261015/` 로 넣고 이유.
   - `submitted/` 요청서 사본 = 리포 요청서와 바이트 대조 (같음 / 다름 기록).
4. **우리 트리 재현** (Codex 탐침):
   - probes/*.py 를 **전부 먼저 읽는다** — 네트워크 · 리포 밖 쓰기 · 삭제 · 임의 subprocess 가 없을 때만 돌린다 (있으면 돌리지 말고 보고).
   - 탐침을 묶음 밖 새 폴더로 복사 → 경로 상수만 우리 트리 (이 작업 트리 = 검토 핀 코드) 와 대조 핀 (`git worktree add` 또는 `git archive dcb97f1ed` 를 스크래치에) 으로 바꾼다 · `python3 -I -X utf8 -B` 로 실행.
   - 판정문 숫자와 대조: 시험 138/138 · 136/136 · 55/55 · 8/8 · 6/6 · 23/23 (옛 코드 81/138 · 133/136 · 54/55) · 구조 탐침 144 = 정상 14 · 거부 112 · ValueError 8 · 헤더 false-PASS 10 · 수치 탐침 113 = REJECT 98 · PASS 15 · 넘침 반례 (1e150 대조 거부 · 1e160 PASS/ACCEPT) · Q7 36/36 · σ 표 여섯 값 · N9b φ SHA256 `c62f2830…`.  같음 / 다름을 README 표로 (numpy · scipy 판도 적기).  무거우면 (각 수 분 넘게) 그 탐침은 건너뛰고 "미재현 (시간)" 으로 적는다.  CPU 적게.
5. `python3 scripts/check_doc_refs.py` → 깨진 참조가 묶음 루트 기준 상대 경로면 `docs/reviews/doc_refs_allowlist.tsv` 에 줄 추가 (꼴 = `<경로>\texternal\tsha256:<64hex>\tCodex Rint 조인 재확인 (검토 핀 2b9efa253 · 10-20) 묶음 루트 기준 상대 경로 (리포 사본 = <리포 경로> · 실행하지 않음)` · Windows 절대 경로 링크도 같은 방식 · 같은 경로 키가 있으면 그 줄 이유에 덧붙임) · 다른 저장소 커밋 = `docs/reviews/doc_refs_sha_exceptions.tsv` 기존 꼴.  끝에 `✓ 깨진 참조 없음`.
6. 원장 `docs/reviews/findings.json` (`json.dumps(d, ensure_ascii=False, indent=2) + '\n'` 그대로 · 쓰기 전 왕복 확인):
   - `RIMPR-01` · `RIMPR-02`: `claimed_fixed` → `verified` (verified_by codex · verified_in = 판정문 경로 · verified_sha `2b9efa253` · verified_scope = 판정문 §0 · §2 · §4 표현 그대로 한정 (01 = 불량 폭 행 · 중복 필수 열 · scalar 뒤 토큰 입구 거부 + `join_gate_failed` 전파 · 확대된 헤더 토큰 주장은 `RIMPRR-01` · 02 = Decimal + float64 + scaffold µm 변환 유한 · int64 범위 밖 구조화 거부 · 계산 결과 유한성은 `RIMPR-04`) · verification_note · evidence_tests 에 판정문 §).  기존 verified 항목 (예 `SELF-118`) 의 필드 꼴.
   - Q7 (일반 관문 r_face 유한·비음수 · 커밋 `2b9efa253`) 에 해당하는 원장 항목이 있으면 같은 방식으로 verified (범위 = §5: 기존 planner 의 float64 실수 행 계약 · r=0 · 절단 tombstone 유지 · 원장 완전성 · 임의 객체 schema 인증 아님 · RRM wrapper 유지).  **없으면 새로 만들지 말고 보고.**
   - `RIMPR-03` · `RIMPR-04`: open 유지 · note 끝에 "★ 10-20 Codex 재확인 (핀 2b9efa253) §4: …" (04 = 비-AM 거리 넘침 1e160 반례로 범위 보강 · "후단이 반드시 거부" 설명 철회 · 연기 조건 네 개 · 03 = ASCII 생산 덤프 범위 명시면 연기 가능).
   - 새 `RIMPRR-01` (P3 · open · owner claude · found_by "codex 10-20 Rint 조인 재확인 (검토 핀 2b9efa253 · 대조 핀 dcb97f1ed · 실제 조인 → 계획 → 정량 관문 · 구조 탐침 144 · 생산 실행 없음)" · opened_in = 판정문 경로 · title 한 문장 · note (자리 · 반례 둘 · 한정 = σ 오염 증거 아님 · 대조 핀에도 있음 · 최소 해결 · "⬜ 수정 계획 = docs/reviews/rimprr_fix_plan_20261020.md (1저자 비준 대기)") · evidence_tests).  `RIMPR-04` 바로 뒤.
   - SELF: 우리 요청서 (`docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` 또는 묶음 submitted 의 원본) 에 *"봉인 32 무변경"* 이 범위 한정 없이 전체 스냅샷처럼 적혔거나 78/135 를 현재 시험 집합처럼 적었으면 새 `SELF-NNN` (P3 · 다음 빈 번호 · claimed_fixed 아님 open → 이 커밋에서 문장 정정하면 claimed_fixed 는 다음 커밋 몫이니 open 으로 두고 정정 문안만 note) — 범위가 이미 한정돼 있었으면 만들지 말고 보고.
   - `RIMP-02` 는 건드리지 않는다 (원장 note 의 닫는 조건이 이번에 충족됐는지만 보고).
   - `python3 scripts/check_review_findings.py` = `원장 자기일관 ✓`.
7. 요청서 (`docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` — 이름이 다르면 리포에 있는 실제 요청서) 제목 줄 바로 뒤에 빈 줄 + `> ✅ **Codex 재확인 (10-20 · 핀 2b9efa253) = RIMPR-01 · 02 · Q7 닫힘 (범위 한정)** — 새 P3 `RIMPRR-01` (구역 헤더 정상화 false-PASS) · `RIMPR-04` 범위 보강 · ①′ 정량 채택 · 생산 HOLD · 판정문 docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md (증거 docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/).`
8. 수정 계획 초안 `docs/reviews/rimprr_fix_plan_20261020.md` (앞선 계획 `docs/reviews/rint_g2_impl_fix_plan_20261014.md` 꼴 · 짧게 · 결과 0 건 · 코드 고치지 않음) — Q 마다 선택지 + **권고 한 줄**:
   - Q1 RIMPRR-01 고침 방식 (정확한 구역 이름 · 단어 경계 · 표지 한 번만 제거 · 나머지 토큰은 기존 열 · 상자 검사로 · 공백 · 탭 · 쓰지 않는 진단 열은 그대로 허용) — 권고 (가).
   - Q2 시험 먼저 범위 (최소 반례 둘 + contact ENTRIES 대응 + 반복 · 후첨 표지 + 정상 양성 그대로) — 권고.
   - Q3 RIMPR-04 지금 범위: (가) 비유한 거리 · 허용폭 = 거부 (fail-closed 한 줄) + 1e160 반례 상주 · 안정한 hypot 재작성은 정량 채택 전 / (나) 그대로 연기 (조건 네 개 기록) — 권고 한 줄.
   - Q4 RIMPR-03 지금 (ASCII `[0-9]` 정규식) / 연기 (ASCII 범위 명시) — 권고 한 줄.
   - Q5 문서 정정 (요청서 · 원장의 "봉인 32 무변경" → §7 권장 문장 · 시험 수 81/138 구분) — 권고 = 그대로 반영.
   - Q6 Codex 재확인 시점 (단독 짧은 재확인 / Rint ② 설계 리뷰 요청과 함께) — 권고 한 줄.
9. `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` 다시 → 커밋 하나 (영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`).

## 규칙
- push 안 함 · `scripts/check_all.sh` 안 돌림 · **코드 파일은 하나도 고치지 않는다** (문서 · 원장 · 예외 목록 · 증거 · 계획만) · `CLAUDE.md` 와 진행 기록은 **건드리지 않는다** (메인이 병합 뒤에 넣는다).
- 원격에 없는 커밋 번호를 문서에 쓰지 않는다 (`SELF-116`) — `2b9efa253` · `3b9d51789` · `dcb97f1ed` · `d8808c164` 는 원격 pqwtv8 에 있다.
- 묶음 안 스크립트는 4 의 절차 (전부 읽고 · 묶음 밖 복사 · 경로만 바꿈) 로만 돌린다.
- 보고 (한국어 · 짧게 · 표): 커밋 SHA · 증거 파일 수 · 뺀 것 · dup 수 · 재현 표 (같음 / 다름 / 미재현) · 예외 줄 수 · 원장 변화 · SELF 여부 · RIMP-02 닫는 조건 · 두 검사 결과 · 계획 Q1–Q6 권고 요약.

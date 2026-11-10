# Codex Rint ② 재확인 회차 ⑥ (11-10) — 반입 기록

- 판정문 = `docs/reviews/codex_review_rint2_rr_round6_20261110.md` — 받은 묶음 안 원본 17514 B · sha256 0facda3104bb96873031c7e0190890d8a3f7b6abed27d717e390938be9219d3a · CR 0 · 주소 꼴 0 → 리포 사본 = 원본과 바이트 같음.
- 리뷰 핀 = `aec8ca2f6` (aec8ca2f6cbc24d43e2ed447c61ce6b62dd19f1e · 가지 B) · 우리가 보낸 ZIP = codex_rint2_rr_round6_aec8ca2f6cbc.zip (1410435 B · sha256 0945ae19… · Codex 입력 대조 = 전달값과 같음) · 현장 관측의 실행 핀 = db86ce9b9.
- 받은 것 = 1저자가 대화에 올린 증거 ZIP (2472268 B · sha256 9e9d9f72745257fa9f097173cb9ad9c2ee57da16fd30ebfb8aad56c27e4a1f1b · 항목 241) · 빈 폴더에 `python3 -I` 로 풀어 검사 (위험 경로 0 · 중복 0 · CRC 이상 0).
- 넣은 것 = **33 파일** (이 폴더 · ZIP 과 같은 상대 경로 · 바이트 그대로 · 목록 = `IMPORT_SHA256SUMS` · `_import_manifest.json`) · 뺀 것 = **208** — 우리 blob 사본 197 (`package/repo/` · `codekey_sources/`) · 우리가 보낸 ZIP 의 봉인 파일 2 (package/PIN.txt · package/SHA256SUMS) · 주소 꼴 4 (Windows 사용자 폴더 경로 · git 신원 메일 → 이름 · sha256 만 · 회차 ④ · ⑤ 와 같은 규칙) · GitHub API 응답 4 · 판정문 1 (위 자리에 따로).  뺀 파일의 이름 · 크기 · sha256 = `_import_manifest.json` 의 `excluded`.
- ⚠ 뺀 주소 꼴 파일 가운데 rr6_siteq_semantics/REPORT.md 는 RR6-01 세부 보고다 (Windows 실행 경로 한 줄 때문에 뺐다) · 같은 내용의 판정은 판정문 §4 · 탐침 결과 = `rr6_siteq_semantics/probe_siteq_predicates.json` (넣음).

## 우리 트리 재현 (메인 세션 · `_repro_ours_20261110/`)

- 고정 트리 = 가지 B HEAD `13eb293cd` 의 git archive (siteq 관련 파일은 리뷰 핀 `aec8ca2f6` 과 같다) · 탐침 사본 = 받은 원본과 sha256 같음 · 빈 작업 폴더 · `python3 -I -B`.
- RR6-01: `probe_siteq_predicates.py` → C02b 네 사례 = Codex JSON 과 같음 (경로 칸 제외 · 같은 단위 + rc 1 = PASS · rc 미보존).  고친 트리 (작업 트리 `siteq_probe.py`) 에 무수정 탐침 = 61 행 AssertionError (옛 동작을 단언 · 기대된 실패) · 기대 한 줄만 바꾼 사본 (`probe_siteq_predicates_expect_fixed.py` · 차이 = `probe_expect_fixed.diff`) = rc 0 · rc 1 사례 FAIL · rc 기록 0/1/0/0.
- RR6-02: `audit_siteq_evidence.py` → prep 목록 README 한 행만 불일치 (기록 6401d4f9… ↔ 실제 c9a11392… · 56403 B) · data 4 행 · 바깥 부분집합 12 행 정상 = Codex 결과와 같음 (경로 칸 제외).
- 고침 시험 = `docs/reviews/rint2_siteq_prep_20261109/tools/test_siteq_c02b.py` 고치기 전 5/10 (`c02b_before.txt`) → 뒤 10/10 (`c02b_after.txt`).

## 처분

`docs/reviews/rint2_rr6_fix_plan_20261110.md` — 원장 RR5-01 verified · RR6-01 · RR6-02 open (고침 = 같은 커밋 · claimed_fixed = 다음 커밋) · Q5 순서 문안 · §7④ 문장 · 1저자 질문 Q1–Q4 (본 세션).  전체 HOLD.

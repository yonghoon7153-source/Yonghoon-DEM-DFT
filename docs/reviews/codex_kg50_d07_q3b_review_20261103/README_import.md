# 반입 — Codex 확인 D0.7-50 압축 체크포인트 재개 한 건 (11-03)

- 받은 것: 1저자 업로드 `codex_kg50_d07_q3b_review_evidence_20261103.zip` · 2305979 B · sha256 `8ed0e4cf2227c401583e6af5bbbd08775f4016bea4f2da4d79bc1a6b73ee1dcc` → 이 폴더에 그대로 풂 (파일 바꾸지 않음).
- 정본 판정문 = `codex_review_kg50_d07_compress_resume_20261103.md` — **한 건 조건부 GO · 새 P1 없음 · P2 `KG50Q-01` (Codex 표기 KG50Q3B-01) (영수증 첫 대조가 본 제출 뒤) · P3 `KG50Q-02` (Codex 표기 KG50Q3B-02) (600,000 step = 첫 접촉 단정 · 중심 ↔ 표면 거리 혼동)** · 독립 탐침 40/40 · 받은 ZIP 해시 198/198.
- 대상 ZIP = 핀 `4d2b8fc42` · sha256 `564e72ec…`.  ZIP 의 `received_zip/` (= 그 ZIP 사본 = `git archive 4d2b8fc42`) · `source/repo/` (= 후보 커밋 `50b5fb4b7` 부분 사본) 는 **반입에서 뺐다** — 우리 파일 사본이고 그 안 상대 경로가 이 자리에서 깨진 참조가 된다 (`check_doc_refs` 3 건).  그래서 `PACKAGE_MANIFEST.sha256` 은 이 폴더만으로 전부 맞지 않는다 (뺀 두 폴더 몫) · 원 ZIP sha256 = 위 값.
- 반영: 실행 절차 `docs/50kg/d07_guard/compress_resume_exec_20261103.md` (판정문 §6 순서 = 새 시험 중 · 본 제출 전 영수증 대조) · 요청서 머리 배너 · 원장 KG50Q-01 · 02 (Codex 표기 KG50Q3B-01 · 02).
- 우리 트리 재현 = 안 함 (판정이 실행 순서 · 문구만 고치라 함 · 코드 변경 없음).

# Codex LHS214 사전 점검 SHA 형식 수정 재확인 (S1 · 10-28) — 반입

- 판정문 `codex_review_lhs214_pin_syntax_20261028.md` (Codex 원문 그대로): **LHS214-PRE-01 (원장 `L214P-01`) 닫힘 · P7 / P10 두 줄 수정 GO · 새 P1/P2 없음 · 실제 214 발사 GO 아님**.  남은 것 = E1 (자체시험 다섯의 실제 종료코드 기록) · E2 (수령표 ↔ 독립 대조 · WSL 기록 연결) · Q5 잔존 P3 (`launch_eligibility` 1140 행 LF · 원장 `L214P-02`).
- 받은 ZIP = `received_codex_lhs214_pin_syntax_review_20261028.zip` (4,454,350 B · sha256 `6b2e09c995834cb36a2b3c79bd431eab7cfbb03d12ccfb061d646d6eab35e46c` · 1저자 10-28 18:4x KST 업로드) · 365 항목 · `MANIFEST.sha256` 364/364 일치 (받은 직후).
- 풀지 않은 것: `repo/` (287 · 리뷰 핀 git blob 사본) · `input/` (4 · 우리 요청서 둘 · 단계 0–6 안내 · WSL 묶음 tgz sha256 `9c05aef7…` = 우리 반입본과 같음).  CRLF 파일은 리포 `.gitattributes` 로 LF — 바이트 원본 = 받은 ZIP.
- 우리 확인 (10-28): `git diff 1baa0d9b7 09bf1813c -- scripts/run_network_194_parallel.py` = `_HEX40.match(gsha)` → `.fullmatch(gsha)` 두 줄뿐 · 우리 HEAD 의 1140 행 `_HEX40.match(g['sha'])` 그대로 (Q5 잔존) · Codex 탐침 넷은 우리 쪽에서 다시 돌리지 않았다 (NumPy · SciPy · networkx + 핀 blob 필요).
- E1 회수: 1저자 10-28 17:36 KST 단계 2 화면 붙여 넣기 원문 = `docs/reviews/lhs214_wsl_preflight_35f032737_1028/step2_screen_paste_1028_1736.txt` (fast16 · real4 · reread · runner · receipt 다섯 다 `rc=0` 줄 · dirty 0) — Codex §5 *"기존 화면 기록을 회수할 수 있으면 재실행할 필요가 없다"*.

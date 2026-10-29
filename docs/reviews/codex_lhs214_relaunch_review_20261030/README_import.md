# 반입 — Codex LHS214 다시 발사 확인 S2 (10-30 · 발사 확인 범위 GO)

- 받은 것: 1저자 10-30 업로드 `codex_lhs214_relaunch_review_bf8cf21c_20261030.zip` → `received_codex_lhs214_relaunch_review_bf8cf21c_20261030.zip` (9,965,711 B · sha256 `d943fa7e7c97ac76e125b1f4a058b680271e0f5e9b31b99dde2e5d3b3e589a28` · 항목 468 · 중복 0 · 대소문자 중복 0 · 경로 이탈 · 링크 0).
- 이 폴더에 푼 것: 판정문 `codex_review_lhs214_relaunch_20261030.md` · `VERDICT.json` · `REPRODUCE.md` · MANIFEST · `independent/identity` (REPORT · 요약 JSON · 대조 스크립트) · `independent/evidence` (REPORT · 재검증 JSON · 스크립트) · `independent/launch` (REPORT · SHA 경계 JSON 10 + 결과 · 스크립트).  뺀 것 (ZIP 안에 그대로): `repo/` (70 파일 = 우리 요청 ZIP) · `input/` (우리 요청 ZIP · 원 WSL tgz · PIN · intake) · `support/s1/` (S1 때 입력 232) · `independent/identity/sources` 등 사본.
- 판정: **GO — 승인 핀 B7 `35f0327377a4213774010a090df4d224e50d29e1` 에서 등록된 수동 순서 (⑤ 승인 → B7 · 환경 · ROOT 현장 확인 → 194 → 실제 완료 · audit · 재시도 예외 확인 → 보충 20 → 두 실제 manifest 와 전체 40 자리 승인 SHA 영수증) 의 발사 확인 범위** · Q1 ①–④ 닫힘 (③ = 명시적 개정 기준 · 원 B15 충족 아님) · 새 P1 · P2 없음 · `L214P-02` (P3) 열림 유지 = 전체 40 자리 `--approved-sha` 필수 · 끝 블록 = 자동 스크립트 아님 (단계마다 따로 · 기준 불충족이면 멈춤) · ⑤ 1저자 발사 승인 · 실행 직전 확인 = 별도.
- 원장: `SUPR-03` → verified (판정문 §1-1 범위) · `L214P-02` note 보강 (열림 그대로).

## 우리 트리 재현 (`_repro_ours_20261030/` · 이 컨테이너 Python 3.11.15 · ZIP 을 새 폴더에 푼 사본에서)

| Codex REPRODUCE 명령 | 결과 |
|---|---|
| `independent/identity/audit_identity.py` | rc 0 · tree 해시 15 · core · closure · input16 같음 · missing 0 · code_fp `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` · 게이트 +25/0 · 등재 +2/0 · LHS 7 행 같음 |
| `independent/evidence/verify_evidence.py` | rc 0 · 보충 24 칸 · S0b 12 경우 · 파서 7 · 변이 4 잡힘 · 결과 JSON = Codex 판과 판정값 차이 0 (목록 순서 · 경로 · 해석기 판만 다름 = 파일 열거 순서가 Windows ↔ Linux 에서 다름) |
| `independent/launch/check_launch_validators.py` | rc 0 · 결과 JSON = Codex 판과 같음 (경로만 정규화) |

- 한정: 보존 자료 · 고정 코드의 읽기 전용 검사뿐 — 생산 실행 · WSL · 실제 발사 아님 (Codex 와 같은 범위).
- 개행: 이 폴더의 JSON · 일부 스크립트는 커밋 때 CRLF → LF 로 정규화됐다 (git 속성) — 바이트 원본 = 같은 폴더의 received_*.zip · Codex MANIFEST.sha256 은 ZIP 안 원본 바이트 기준.

# Rint ② Codex 2/2 요청 기록 (11-17 · 봉인 후보 v2 · v2.1 · 내부 반박 리뷰 · ZIP 도구)

- 요청서 = `docs/reviews/codex_rint2_seal_round2_request_20261117.md` (리뷰 핀 = 이 폴더가 든 커밋 · 발송 = 1저자).
- 지위 = 결과 0 건 · σ 열람 0 · 봉인 전 · R 런 0 · 내부 반박 리뷰 = 독립 조수 · **Codex 아님** (Codex verified 로 올리지 않는다).

## 이 폴더

| 파일 | 무엇 |
|---|---|
| `seal_round2_records_20261117.tgz` | 기록 묶음 (sha256 `e726b55f105b519d0c7d7721b5cdde889b7e687b3874f8149cd8cc638d2c39dd` · 518 항목 · `tar --sort=name` · 고정 시각 · `gzip -n`) — `seal_candidate_v2/` (168 파일 · 봉인 꼴 묶음 seal_form_Gprime_20261117.bundle = 커밋 bea3cb33a · 부모 = 코드 핀) · `seal_candidate_v2_1/` (200 파일 · 내부 리뷰 고침 판 · 봉인 꼴 묶음 seal_form_G2_20261117.bundle = 커밋 c80d700bd · sha256 6e8e1e2d5b104557d6701cf0ebfd53b80492e749652b4cca04c7a696d7af4313) · `seal_candidate_v2_review/` (85 파일 · REVIEW.md · repro/) · `seal_v2_brief.md` (조수 지시서 · 1저자 결정 Q1–Q8) |
| `build_zip.py` | 요청 ZIP 도구 (repo/ = 리뷰 핀 blob 그대로 · git blob sha1 다시 대조 · extra/ · PIN.txt · ZIP_MANIFEST.tsv · 같은 입력 = 같은 바이트 · git 쓰기 없음) |
| `zip_paths.txt` | ZIP repo/ 경로 목록 |

- 봉인 꼴 커밋 둘 (bea3cb33a · c80d700bd) 은 scratch 커밋이다 — 원격에 없고 묶음으로만 있다 (봉인 때 같은 도구로 다시 만든다).
- 묶음 안 증거의 원 출력 (`evidence/raw/`) 은 scratch 경로를 담는다 (주소 · 계정 · 실제 홈 경로 낱말 훑음 0 건 · 11-17).

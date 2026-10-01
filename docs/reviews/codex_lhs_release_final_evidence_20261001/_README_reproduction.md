# Codex 최종 리뷰 — LHS 배포 v1.1 (2026-10-01) · 증거 반입

- 판정문: `docs/reviews/codex_lhs_release_final_verdict_20261001.md` (받은 그대로).  판정 = **고정 v1.1 계산값 전달 GO · 실제 전극 물리 타깃 인증 HOLD** · 새 P1 없음 · P2 다섯 (`LHSREL-01`~`05`) · P3 하나 (`LHSREL-06`).
- 받은 묶음: `codex_lhs_release_final_review_20261001.zip` sha256 `b89f50be903e67db63f63ab16d4a0a7b73a174afc2d2344a5e3e14df0f880ef7` (1저자 경유).
- 고정 대상: 요청 · 원장 스냅샷 `8b3bc3d9c` · 데이터 · 배포 커밋 `c981d77f0`.
- 반입한 것: 검토 스크립트 (`audit_release.py` · `supplemental_probes.py` · `final_evidence.py` · `run_baseline.py` · `package_review.py` · `bootstrap.py` · `probe_*.py` · `restore_source_bytes.py`) · `README_REVIEW.md` · `reused.json` · `evidence/` (판정 근거 JSON · 열별 검토표 · selftest 로그).
- **반입하지 않은 것**:
  - `snapshot/` (고정 커밋의 리포 파일 사본 — git 이력에 있다)
  - `evidence/regenerated_{lhs,lhsx}.csv` · `_columns.tsv` — 커밋된 인계표와 **바이트 동일**이라 해시만 남긴다:
    130 csv `4df9c1f580bc1ae6…` · tsv `c32137b9dbd1210c…` / 64 csv `769cb26972c42783…` · tsv `70e398c02b482b80…` (= `docs/data/{lhs,lhsx}_handover_20261001{.csv,_columns.tsv}`).
- 재현: `c981d77f0` 를 별도 worktree 로 꺼내 그 루트에서 `python audit_release.py` · `python supplemental_probes.py` · `python final_evidence.py` (numpy · scipy · networkx · pandas).  스크립트는 증거 루트 기준 경로를 쓴다 — `snapshot/` 대신 worktree 를 가리키게 바꿔야 한다.
- 검토 환경 한계 (판정문 §1 그대로): Windows · WSL 접근 불가 · `check_all.sh` 전체 미실행 · 수확기 selftest 원본 167/168 (LF 픽스처 진단 168/168) · 웹앱 배치 selftest 는 symlink 권한 오류 (복사 진단 29/29).
- 판정문 반입 때 바꾼 것 (문서 참조 검사기 통과용 · 뜻 불변): `evidence/<파일>.json|tsv` 8 곳을 리포 경로 `docs/reviews/codex_lhs_release_final_evidence_20261001/evidence/<파일>` 로 — 그 밖의 글자는 받은 그대로.

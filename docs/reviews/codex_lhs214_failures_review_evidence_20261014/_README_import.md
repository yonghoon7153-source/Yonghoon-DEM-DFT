# 반입 기록 — Codex LHS 214 실패 14 건 · 분류 수정 (가) 설계 검토 (2026-10-14)

- 판정문 = `docs/reviews/codex_review_lhs214_failures_20261014.md` (묶음 안 원본 바이트 그대로 · sha256 `cc3f18cbb0ff2e66b993fdb6355522d51c4a14575feadbc9bb052d10bbbffe01`) · 검토 핀 `1087a9b2f` (발사 핀).
- 요청서 = `docs/reviews/codex_lhs_run214_failures_request_20261014.md` — 보낸 바이트 = 이 폴더 `submitted/codex_lhs_run214_failures_request_20261014.md` (sha256 `bba26adbcea8dc7d2b07c40ad2044623cba54593a345edf711682805bd5e3a69` · 우리 작성본과 같음).  리포 사본에는 끝에 상태 줄만 더했다.
- 원 ZIP = Codex 작업 공간 `codex_lhs214_failures_review_1087a9b2f_20261014.zip` (1저자 PC) — 원 ZIP sha256 은 받지 못했다 [미확인].
  1저자가 미니 ZIP 으로 다시 묶어 올림: `codex_lhs214_failures_mini_20261014.zip` (654,726 B · sha256 `61026156c0976345940cc23a8d33760f27cde68382f05536a885024d53df6ef9` · 원 ZIP 멤버 1,056 전부의 sha256 · 크기 목록).
- `_members.tsv` 열 = sha256 · 크기 · 상태 · 원 경로.  상태 = `keep` (이 폴더에 그대로 23) · `verdict` (판정문 자리로 1) · `tgz` (아래 원 tgz 안 60) · `drop` (넣지 않음 972).
- 넣지 않은 것 (`drop`): `source/` 972 파일 = 검토 핀 `1087a9b2f` 의 git blob 과 sha256 · 크기 **972 / 972 같음** (반입 때 `git cat-file` 로 대조).  Codex `source_manifest.json` · `final_verification.json` 은 974 를 적는다 — ZIP 의 `source/` 에 없는 둘 = `docs/reviews/codex_rint_g1_lhs_network_review_evidence_20261005/package_manifest.json` · `docs/reviews/codex_rint_g2_v3_review_evidence_20261007/package_manifest.json` (옛 증거 폴더의 같은 이름 파일 · 묶음 포장에서 빠진 것으로 보임 [추정] · 둘 다 핀에 있는 파일).
- 묶은 것 (`tgz`): `submitted/lhs214_run_evidence_1014_1520/` 60 파일 = 1저자가 Codex 에 보낸 **원 tgz** `submitted/lhs214_run_evidence_1014_1520.tgz` (166,670 B · sha256 `250e7a9ddf180192f724c827431b9ef3f56e3bdc485d709c0f3a7c1234d7f4b4` · 멤버 80 = 파일 60 + 폴더 20 · 위험 경로 0) 의 멤버와 바이트 **60 / 60 같음** → 원 tgz 만 둔다.
  ⇒ 10-14 실행 증거 (194 · 보충 20 의 manifest · progress · 감사 · 다시 읽기 · 실패 14 건 worker · log · network_attempt · 보충 20 사후 영수증 · lhsx_054 단독 진단) 의 리포 보관본이 이 tgz 다.
- 묶음 안 스크립트 (`probes/` · `build_package.py` · `complete_source.py` · `prepare_review.py`) 는 **실행하지 않았다** (반입 규칙 — 읽기만).  Codex 반례는 우리 시험으로 옮겨 상주시킨다 (수정 계획 §3).
- 판정문 · `README.md` · `notes/` 의 상대 경로 (`source/` · `evidence/` · `probes/` · `submitted/` · `notes/`) 는 Codex 묶음 루트 기준이다.

## 판정 요지 (원장에 옮긴 것)

- **분류 분리안 (가) 조건부 지지 · 보완 셋을 포함한 구현 · 시험 착수 가능 · 새 214 발사와 v1.3 배포 = HOLD.**  이번 판정은 코드 수정 · 원장 종결 · 재발사 승인이 아니다.
- 새 결함 (open · P2): `L214-01` (사유 이름만으로 유효한 모형 한계를 식별하지 못함 — 같은 회로에 plate_z = +∞ 도 같은 `over_conduction_guard`) · `L214-02` (게시되지 않는 실패 레코드의 검사 면제를 새 범주가 상속하면 증서 · 세대 보장이 사라짐) · `L214-03` (웹앱 표가 없는 Physics 값을 Hertz 로 채우고 차이 0 % 표시).
- 내 오기 (`SELF-113`): 요청서 §1 의 "망 솔버 rc 1" (실제 = 망 솔버 rc 0 · ok=false → 병합 rc 1 → 워커 rc 1) · "최대 RSS 0.88–1.94 GB (메모리 아님)" (실제 527.8–1937.9 MiB · `ru_maxrss` 는 트리 합이 아님 · RSS 하나로 메모리 원인 배제를 확정하지 않는다) · "통과 침대 Physics σ_ratio 1.04–1.48 (`MODEL_BELOW_CONTINUUM_BOUND`)" (그 상태는 τ² < 1 판정이지 q > 1 의 동의어가 아님 · q < 1 사례도 있다) · "≈ 40 분" (계획 추정 · 실측 = 30 분 33 초 + 5 분 23 초).
- 확인된 사실 (판정문 §1): 두 배치 집계 · 봉인 32 · `code_fp e8b2496b…` · ID 집합 해시가 등록과 같음 · `lhsx_054` 단독 진단 = 수치 인증 통과 뒤 q = 1.5370331988867802 로 FULL 가드 거부 (Hertz FULL q 0.66147876) — 단 진단 입력 digest · 실행 provenance 없음 · **나머지 13 건 원인 미확정**.
- 수정 계획 = `docs/reviews/lhs214_fix_plan_20261014.md` (Codex 최소 해제 목록 A · B · C 를 그대로 단계로 · Q1–Q4 = 1저자).

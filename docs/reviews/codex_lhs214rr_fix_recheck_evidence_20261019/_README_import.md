# 반입 기록 — Codex LHS214RR 재확인 (L214R-R01–R04 · WEB-09 · 리뷰 핀 `77d8fd445` · 비교 `60ba39e22` · 2026-10-19)

- 판정문 (리포 사본) = `docs/reviews/codex_review_lhs214rr_fix_recheck_20261019.md` (묶음 `verdicts/` 사본 · 묶음 뿌리 사본과 바이트 같음 · sha256
  `809e47182d3f963f4273efaa80dfa2ce2d9a0847ddd3dd48217afc55f0719c93` · 20,511 B).
- 판정 = **수치 인계 코드 HOLD 해제 가능 · 새 P1/P2 없음 · 전체 종결 부분 · 새 214 발사 HOLD** — R01 (= L214RR-01) 닫힘 · R02 닫힘 · R03 원 반례 닫힘 (공백 잔여 = 새 P3 L214RR2-01) ·
  R04 명시 범위 닫힘 · WEB-09 갱신 · Δ 규약 닫힘 · 새 P3 넷 (L214RR2-01 등록 파서 공백 · 02 R01 경계 시험 환경 의존 · 03 이온 채널 요약 표지 ↔ FULL 미결합 · 04 과거 sigma_ratio null → /single 500) ·
  대기 지문 설명 오기 (요청서 · 증거 README 의 `755325e1…` = R04 이전 설명 · 실제 대기 선언 · 영수증 S0b = `2149f873…` 올바름) · 무영향 A4 36/36 (91.6 s · Codex 환경) ·
  제출 R01 시험 = Codex 환경 (Windows · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3) 23/26 rc 1 (E 경계 입력의 raw q 가 환경에 따라 다름 · 별도 정확 경계 입력으로 다섯 단언 통과).
- 받은 것 = 1저자가 WSL 에서 만든 **미니 묶음** `codex_lhs214rr_recheck_20261019_mini.zip` · sha256 `6536f4b2283bbd230e90b9382c911ca7e93d385c27720e623ea176c38774bf78` · 5,396,396 B ·
  원 Codex ZIP `codex_lhs214rr_fix_recheck_20261019.zip` (55,533,008 B · sha256 `7603fcf212a7c63d8b2adebc9940d7d3c83219b35a20a7c68b7df4a2b30e5bd8`) · 미니 = 남김 1,728 (20,123,990 B) ·
  뺌 2,037 (git 사본 2,028 · 2 MB 초과 9) · `MINI_MANIFEST.json` 해시 1,728/1,728 같음.
- 반입 처리: 새 빈 폴더에 복사 → sha256 → 멤버 목록 (절대 경로 · `..` · 역슬래시 0) → `python3 -I` 로 읽기만 (안의 스크립트 실행 없음).
- 우리 쪽 대조 (git · 10-19): 뺀 git 사본 2,028 중 **2,025 = 핀 `77d8fd445` 의 blob 과 sha256 같음** · 3 = `docs/db/` 실행 때 생긴 웹앱 DB 초기 파일 (`.mtime_cache.json` ·
  `metrics_master.csv` · `metrics_master.sqlite` — 10-18 반입과 같은 부류 · git 밖).
- 넣은 것 = 281 파일 (6,589,902 B) — `README.md` · `notes/` 셋 · `probes/` · `prior_reference/` · `evidence/` 의 요약 JSON · 로그 · 등록 파서 반례 입력 `evidence/receipt_fence_cases/` (114).
- 넣지 않은 것 (해시 = `_members_mini.tsv` 의 status · note 열): `verdict` 1 (→ `docs/reviews/`) · `verdict-copy` 1 · `dup-git` 2,025 · `dup-git?` 3 (위 DB) · `big-hash-only` 9
  (화면 대조 JSON 셋 · 트리 목록 둘 · source 사본 넷 (덤프 gz 셋 · findings.json)) · `hash-only` 1,446 (실행 작업 폴더 `evidence/rr_display_*work/` · `evidence/rr_consumers/consumer_adversarial_*/` ·
  다시 만들 수 있는 생산자 fixture `evidence/rr_consumers/consumers_fixtures/` · 렌더 `*.html` · 트리 대조 `evidence/commit.json` · `evidence/compare_60ba.json`).
- 참조 검사 예외 = `docs/reviews/doc_refs_allowlist.tsv` (이 묶음 루트 기준 상대 경로 · 리포 사본 sha256).
- 정정 기록 (원장 `SELF-121`): 요청서 `docs/reviews/codex_lhs214rr_fix_recheck_request_20261018.md` 머리 (대기 지문 문장) 와 10-18 증거 README
  (`docs/reviews/lhs214rr_fix_evidence_20261018/README.md` · SHA256SUMS 봉인 — 덮어쓰지 않는다) 의 `755325e1…` = R04 이전 설명 · R04 뒤 실제 대기 지문 = `2149f8738bb20b6a…`
  (194 §9-8 · 보충 §9-3 · 영수증 S0b 접두 = 올바름 · 영수증 D1 실패는 승인 전 정상 상태).
- 원장: L214R-R01 · R02 · R03 (원 반례 범위) · R04 (이온 FULL · CF · 협착-only 가지 · 증서 쌍) · WEB-09 (채택 값 갱신 · Δ freshness) → verified (verified_sha `77d8fd445`) ·
  신설 `L214R-S01` (= L214RR2-01) · `L214R-S02` (= 02) · `L214R-S03` (= 03) · `L214R-S04` (= 04) P3 open · `SELF-121` open · ⬜ 우리 트리 재현 · 수정 계획 = 1저자 비준.
- 우리 트리 재현 (10-19 · `298a73197` · 이 폴더 `_repro_ours_20261019/` · Codex 탐침 파일은 실행하지 않고 같은 절차의 파생 스크립트로 Codex 입력을 읽기만): S01 · S02 · S03 · S04 넷 다 Codex 와 같은 판정 (S01 · S03 판정값 차이 0 · S02 = 실 사슬 raw q 끝자리 환경 차 양방향 · S04 = 500 / 200 같음) · 수정 계획 = `docs/reviews/lhs214s_fix_plan_20261019.md` (⬜ 1저자 비준).

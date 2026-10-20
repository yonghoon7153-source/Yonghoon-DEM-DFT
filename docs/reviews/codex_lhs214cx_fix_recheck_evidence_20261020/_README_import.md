# 반입 기록 — Codex LHS214 S06 · S02 수정 재확인 (검토 핀 `34713ac96` · 대조 핀 `685c2bbdb` · 2026-10-20)

- 판정문 (리포 사본) = `docs/reviews/codex_review_lhs214cx_fix_recheck_20261020.md` (묶음 뿌리의 같은 이름 · 바이트 그대로 · `cmp` 같음 ·
  sha256 `f5da326d4b05b2af1f3ab318e27ced9274ef7346272cc3db7ef32ba6f2f3b35e` · 19,049 B).
- 판정 = **요청한 두 수정 닫힘 · 새 P1 · P2 · P3 없음** — `L214R-S06` (Codex 표기 L214S-CX01) CLOSED · `L214R-R03` CLOSED **합의한 지원 문법 (울타리 코드 블록 + 0 열 ATX 제목) 범위 한정**
  (들여쓴 제목 · setext · HTML · 목록 · 인용 · 들여쓴 코드 블록을 지원하거나 전부 거부한다는 인증 아님 · §3-2) · `L214R-S02` (Codex 표기 L214RR2-02) CLOSED **실제 Windows 원본 40/40**
  (대조 핀 원본 23/29 rc 1 · 같은 환경 · 시험 파일 무변경 · §4-1) · 새 214 발사 = 기존 다섯 선행 조건 (§5 — 등록 비준 · 재결합 · B7 승인 핀 · 새 ROOT 사전 점검 · 1저자 발사 승인) 전 **HOLD** ·
  S03 · S05 open 유지 · S3 별도 실행 봉인 · v1.3 주 학습 인계 HOLD 그대로 (§5).
- 판정문의 정정 · 한정 둘 (우리 문장에 옮길 때): §2 *"실행 코드 두 파일만 바뀌었다"* 는 맞지만 *"커밋 전체에서 두 파일과 재고 한 줄만 바뀌었다"* 는 아니다 (전체 tree 수정 8 · 추가 155 · 삭제 0 —
  원장 · 기록 · 요청서 · 증거 · 별건 SDCP 등록 문서) · §3-3 영수증 자체시험 원본 = 105/118 (대조) · 109/122 (검토) rc 1 (실패 13 같음 · 하위 `python -I` 세대 탐침이 따로 준 의존성 경로를 못 봄 =
  Windows 런타임 · S06 회귀 · git 탓 아님) · 어댑터 보조 실행 122/122 — *"무어댑터 원본 Windows 122/122"* 라 쓰지 않는다 · 실제 발사 환경 검증을 대신하지 않는다.
- 받은 것 = Codex "판정문 + 증거 ZIP" `042354ec-codex_lhs214cx_fix_recheck_20261020.zip` · sha256 `8935a3af47be0835f6db2cc2584620b966715e0b2ec83e1d5fb4e22bd8fc17d6` · 1,901,737 B ·
  항목 142 (모두 파일 · 폴더 항목 0) · 풀면 9,345,368 B · 위험 경로 0 (절대 경로 · `..` · 역슬래시 · 드라이브 · 링크) · 이름 중복 0 · `CONTENTS_SHA256.json` 141 항목 sha256 · 크기 =
  풀린 파일 전수 같음 (141/141 · 목록 밖 = 그 파일 자신).
- 반입 처리: 새 빈 폴더에 복사 → 위 검사 → 새 빈 폴더에 풀기 (각 항목이 대상 폴더 안에 머무는지 다시 검사) → 읽기는 `python3 -I` · 묶음 안 스크립트는 **전부 먼저 읽고**
  실행은 `probes/s02/adversary.py` 하나 (묶음 밖 복사본 · 경로 상수만 바꿈 = `_repro_ours_20261020/` 의 probe_path_changes.diff · 그 밖 한 글자도 안 바꿈 · 쓰기 = 복사본 폴더 안 · 변이는 메모리 안만).
  실행하지 않은 것 = `intake.py` (GitHub 네트워크 `urllib` · `C:/Users/…` 에서 요청서 복사) · `package_review.py` (ZIP · 영수증 쓰기) · `probes/run_original.py` (우리 두 시험의 하위 프로세스 래퍼 →
  같은 두 시험을 우리 트리에서 직접 돌렸다) · `probes/s06/parser_audit.py` · `probes/s06/supplementary.py` · `probes/s06/generation_environment.py` (셋 다 markdown-it-py 필요 — 이 컨테이너에 없음 ·
  설치하지 않음) · `probes/scope/cx_scope_audit.py` (Codex 작업 공간의 `source/` 스냅샷 필요 → 같은 대조를 git 으로 직접).
- 우리 쪽 대조 (git · 10-20): Codex `source_manifest.json` 2,135 항목 = git `34713ac96` blob **2,135 / 2,135 같음** · 묶음 baseline_review/source_manifest.json 2,076 = git `685c2bbdb` blob
  **2,076 / 2,076 같음** · 묶음 evidence/tree.json = `git ls-tree -r 34713ac96` blob 11,443 (경로 · sha · 모드 전수 같음 · tree 항목 1,513) · `evidence/commit.json` = 커밋 `34713ac96` (부모 `406cec59f`) ·
  이 작업 트리와 2,126 / 2,135 같음 (다른 9 = 그 뒤 바뀐 문서 넷 `CLAUDE.md` · `docs/reviews/findings.json` · `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` ·
  `docs/session_20260923_progress.md` + Rint 파일 다섯 `scripts/rint_iface_join.py` · `scripts/step3_sigma.py` · `scripts/test_rint_g2_am_iface.py` · `scripts/test_rint_g2_join.py` · `scripts/test_rint_g2_rrm.py`)
  ⇒ **작업 트리 LHS214 코드 = 검토 핀 코드** (영수증 도구 · 경계 시험 · 생산 · 소비 · 실행기 · 배포 빌더).
- 넣은 것 = 묶음 파일 121 (keep 120 + 묶음 매니페스트 `CONTENTS_SHA256.json`) + 반입 파일 (`_members_mini.tsv` · 이 README · `_repro_ours_20261020/` 40 = 그 README · 우리 출력 · `_repro_ours_20261020/results_ours.json` ·
  탐침 경로 diff · tools 13).  증거 폴더는 `.gitattributes` 의 `codex_*_evidence_*/** -text` 라 CRLF (evidence/s06/new_cases 12 = Codex Windows `write_text`) · CR · CRLF
  (evidence/s06/newline_cases 12) fixture 도 바이트 그대로 커밋된다.  `.gitignore` 에 걸리는 이름 없음 (폴더 이름 바꾼 것 0).
- 넣지 않은 것 (해시 = `_members_mini.tsv` 의 status · note 열): verdict 1 (→ `docs/reviews/`) · `big-hash-only` 1 = evidence/tree.json (3,989,838 B · 2 MB 초과 · 내용 = 위 git 대조로 같음) ·
  `dup-repo` 19 = source_review/ 15 (리포의 같은 경로 · 같은 바이트 = `34713ac96` blob — 요청서 사본은 이 반입 커밋이 머리에 Codex 회신 한 줄을 붙이기 **전** 바이트) +
  baseline_review/ 4 (이전 판정문 = `docs/reviews/codex_review_lhs214s_fix_recheck_20261019.md` · 기준 manifest =
  `docs/reviews/codex_lhs214s_fix_recheck_evidence_20261019/lhs214s_recheck_20261019/source_manifest.json` · 시험 · 영수증 도구 두 파일 = git `685c2bbdb` blob — 작업 트리 판은 `34713ac96` 에서 바뀜).
- keep 인데 같은 바이트가 리포에 이미 있는 것 1 = evidence/original_baseline_boundary.log (= 10-19 반입 lhs214s_recheck_20261019/evidence/s02_new_full.log · 같은 Windows 원본 시험의 같은 출력) —
  판정문 §4-1 · Codex README 의 핵심 증거라 이 폴더에도 둔다.  빈 로그 둘 (evidence/s02/axis.log · sweep.log · 0 B) 은 Codex 탐침의 로그 자리 그대로.
- 요청서 사본: `submitted/codex_lhs214cx_fix_recheck_request_20261019_send.md` ↔ 리포 `docs/reviews/codex_lhs214cx_fix_recheck_request_20261019.md` (`34713ac96` 판) = **다름 — 7 행 하나뿐**
  (리포 = 리뷰 핀 자리 표시 *"SHA 는 발송 때 1저자가 적는다"* · 발송본 = 실제 `34713ac9650ece7c8d59b7c4d9a2aefccee693ea` 와 가지 이름) · 그 밖 바이트 같음 = 발송본 · source_review/ 사본 = 리포 판과 같은 바이트.

## 우리 트리 재현 (10-20 · 가볍게 — 메인 게이트와 겹쳐 CPU 하나씩 · 합 약 2 분)

- 우리 = 이 컨테이너 (Linux · 4 vCPU · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · markdown-it-py 없음 · 스레드 1) · 코드 = 이 작업 트리 (= 검토 핀 LHS214 코드) ·
  대조 핀 코드 = `git show 685c2bbdb:` (경계 시험 · 영수증 도구 · 생산 · 소비 두 파일) · 시험 · 영수증은 트리를 건드리기 전 (깨끗한 트리) 에 돌렸다.
  Codex = Windows 11 build 26200 · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3 · markdown-it-py 3.0.0.  출력 · 도구 = `_repro_ours_20261020/` (`_repro_ours_20261020/README.md`).

| 항목 | Codex (판정문 · 증거) | 우리 트리 | 판정 |
|---|---|---|---|
| 경계 시험 원본 — 검토 핀 (`scripts/test_l214r_r01_restored_full.py` 무변경) | Windows **40/40 rc 0** (9.33 s) | 40/40 rc 0 (10.1 s) | 같음 |
| 경계 시험 원본 — 대조 핀 판 (sha256 `eaff4ba4…`) | Windows **23/29 rc 1** (E0–E4 · E′ FAIL · E5 PASS) | 30/30 rc 0 (그 판을 우리 트리 자리로 실행 · E′ 가 ±18 두 칸이라 30) | 다름 (환경 — 등록 면적의 box_y 한 축 걸음이 이 기계에서는 경계를 안 건너뛴다 · §4-1 결손 = Windows 관측) |
| 영수증 자체시험 (`scripts/supp20_input_receipt.py --selftest`) | 원본 105/118 (대조) · 109/122 rc 1 (검토) · 명시 어댑터 122/122 | 검토 핀 판 **122/122 rc 0 · 어댑터 없음** (33 s) · Windows 실패 13 (S7 · S7u · S7a · S7a-t · S7a2 · S7d-t · S7j · S7k1 · S7k2 · S11d2 · S11f2 · S12a2 · S12c2) 전부 PASS · S12k–S12k4 PASS | 다름 (환경 — §3-3 원인과 맞음: 이 컨테이너 SciPy 는 system dist-packages 라 `python -I` 세대 탐침 자식도 본다 · Codex 는 의존성을 따로 준 경로라 자식이 못 봄) |
| 실제 보충 20 등록 영수증 (인자 없음) | rc 1 · 실패 D1 하나 · 옛/새 도구 값 · 칸 같음 | rc 1 · [D1] · 11 칸 · 등록 값 = Codex 영수증 넷 (`evidence/s06/actual_receipt_new.json` · `evidence/s06/actual_receipt_old.json` · `evidence/scope/receipt_new_raw.json` · `evidence/scope/receipt_old_raw.json`) 과 같음 (code_fp `e8b2496b…` · pending `2149f873…`) | 같음 |
| 이전 제목 19 문서 · 전체 `receipt()` | oracle 불일치 **14 → 0** · rc 0 14 → 4 | 14 → 0 · rc 0 14 → 4 · 판정 · 영수증 19/19 Codex 기록과 같음 · 입력 sha256 19/19 같음 | 같음 (oracle = Codex 기록값) |
| 이전 울타리 114 문서 · 전체 `receipt()` | **0 → 0** · 수용 57 · 거부 57 | 0 → 0 · rc 0 57 · 57 · 114/114 같음 | 같음 (oracle = Codex 기록값) |
| 새 경계 · 울타리 · 역사값 조합 8,736 문서 | oracle 불일치 **608 → 0** | 옛 ↔ 새 도구 판정이 다른 문서 **608** (새 도구 = oracle 이면 반드시 608) · 1.6 s | 일관 (필요조건 · oracle 미재현 = 의존성) |
| 전이 30,000 문서 (seed 20261020) | 2,212 → 0 | 옛 ↔ 새 다른 문서 **2,212** · 1.6 s | 일관 (같은 한정) |
| 대표 12 문서 전체 영수증 | 12/12 기대 판정 | 12/12 · Codex 기록과 같음 · 문서 = 묶음 new_cases 12/12 (CRLF → LF 뒤 같음) | 같음 |
| LF · CRLF · CR 실제 파일 18 | 18/18 | 18/18 · Codex 기록과 같음 · 문서 바이트 = 묶음 newline_cases 18/18 | 같음 |
| 지원 밖 대조 6 (들여쓴 제목 · setext · HTML 둘 · 들여쓴 코드 · 인용) | 옛/새 판정 기록 (§3-2 한정) | 6/6 같음 | 같음 |
| 실제 등록 문서 §3 절 (옛/새) | 같음 | 같음 (Codex 기록과도) | 같음 |
| S02 탐침 core | 9/9 | 8/9 — 빠진 1 = *"Windows 등록 면적 한 축 건너뜀 재현"* (이 기계는 등록 면적 k = 0 에서 세 경계를 다 낸다) | 다름 (환경) |
| S02 탐침 axis | 5/5 | 2/5 — 같음 = 상자 여섯 전류 비트 같음 · q 식 비트 같음 · 곱 증가 0/1 ULP · 빠진 3 = 등록 면적 prev 결손 셋 (129 실 기록 · 분모 열거 · box_x 401) — 이 기계 등록 면적 전류 `0.03976778104389289` (Windows `…278`) 에서는 prev 가 나온다 | 다름 (환경 — §4-3 의 *"등록 사슬 · 주변 binade · 이 환경"* 한정과 같은 방향) |
| S02 탐침 mutants · 변이 6 종 | 11/11 · 실패 단언 E2·E4 / E1·E3·E4 / E1–E4 / E2·E5 / E4·E5 / E4·E5 | 11/11 · 같은 단언 집합 6/6 | 같음 |
| S02 탐침 failclosed | 3/3 | 2/3 — 129 면적 소진 · 예외 주입 같음 · 빠진 1 = kmax 0 에서 등록 면적이 실패해야 한다는 전제 (이 기계는 k = 0 에서 찾아 E4 가 복원을 정상 호출) | 다름 (환경) |
| S02 탐침 sweep (출발 면적 ±200 ULP 401) | 401/401 · 둘째 축 251 · 최대 9 ULP · 최대 19 회 | 안 돌림 | 미재현 (시간 — 브리프 지시) · 리눅스 컨테이너 값 = 10-19 S02 수정 증거 401/401 · 278 · 14 ULP |
| 세 경계 raw q · 생산자 판정 | 1.5000000000000002 보류 · 1.5 게시 · 1.4999999999999998 게시 · 저장 q 1.5 · 1.5 | 같음 (등록 · E″a = box_y …881 / …882 / …883 · E″b = …820 / …821 / …823 · 셋 다 같은 q · 상태 · 저장값) | 같음 |
| 경계 입력 찾기 (등록 · E″a · E″b) | 등록 = prev 건너뜀 → −5 ULP · 11 회 / E″a = next → +2 · 4 회 / E″b = next → +1 · 2 회 · 성공 면적 I_bottom 셋 다 `0.03976778104389289` | 등록 = 건너뜀 없음 (k 0 · 1 회) / E″a = **prev** → +2 · 4 회 (같은 면적 0.5000000010000007) / E″b = next → −4 · 9 회 (0.5000000009999985 · I_bottom `…256`) | 다름 (환경 — §4-2 *"E″a 누락 = 저자 Linux prev · 이번 Windows next"* 와 같다 · 계약 = 이 환경에서 세 경계 정확 재현) |
| 독립 단언 합 | **29/29** (원본 40/40 과 다른 묶음) | 23/28 (sweep 빼고 · 빠진 5 = 모두 Windows 등록 면적 전제) | 다름 (환경) |
| 범위 (git 직접) | 봉인 32 · HANDOVER 2 · 등록 문서 둘 · 배포 빌더 · 생산 · 소비 바이트 같음 · `E_AREA` · `E_BX` · `E_BY` 같음 · FULL 1.5 · 엄격 `>` (`network_conductivity.py:1471` · `tau_flux.py:807`) · 재계산 지문 `2149f873…` · 활성 §3 `e8b2496b…` · tree 수정 8 · 추가 155 · 삭제 0 · 실행 코드 2 | `685c2bbdb` · `34713ac96` · 작업 트리 셋 다 32/32 · 2/2 같음 · 같은 값 · 같은 줄 · 지문 같음 · `git diff --name-status 685c2bbdb 34713ac96` = M 8 · A 155 · D 0 (실행 코드 = `scripts/supp20_input_receipt.py` · `scripts/test_l214r_r01_restored_full.py`) | 같음 |

- 미재현 = S06 oracle 자체 (markdown-it-py 3.0.0 토큰 · 의존성) · S02 sweep (시간 · 브리프 지시).  다름 (환경) 은 모두 Windows 등록 면적 전제 또는 Windows 런타임의 격리 의존성에서 나온다 —
  판정문이 그 둘을 환경 관측으로 한정했으므로 (§3-3 · §4-2 · §4-3) 닫힘 판정과 충돌하지 않는다.
- 한정: 판정값 재현이다 — `check_all.sh` 전체 · WSL · 새 214 · 생산 σ 재계산 · A4 재수행 아님 (판정문 §6 *"하지 않은 것"* 과 같은 범위).

## 폴더 꼴 · 참조 예외 · 원장

- 폴더 꼴: 이 폴더 = 묶음 뿌리 (판정문 · Codex README 의 상대 경로 `evidence/…` · `probes/…` · `submitted/…` 의 루트) − 판정문 − evidence/tree.json − source_review/ · baseline_review/ 사본 + 반입 파일.
  판정문 · Codex README 의 `source/…` · `lhs214cx_recheck_20261020/…` · `lhs214s_recheck_20261019/…` 경로 = Codex 작업 공간 (Windows) 의 고정 핀 사본 · 폴더 (리포의 `34713ac96` · `685c2bbdb` 같은 경로).
- 참조 검사 예외 = `docs/reviews/doc_refs_allowlist.tsv` (이 묶음 루트 기준 상대 경로 · `external` · 리포 사본 sha256 · 실행하지 않음 표지).
- 원장 (`docs/reviews/findings.json`): `L214R-S06` · `L214R-S02` claimed_fixed → **verified** (verified_sha `34713ac96` · 범위 = 판정문 §1 · §3 · §4 한정) ·
  `L214R-R03` = 이미 verified (10-19 · `77d8fd445` · 원 반례 범위) 라 상태 · verified 칸은 그대로 두고 note 에 이번 전체 종결 (합의 문법 범위 한정 · §3-2) 한 문장만 붙였다 ·
  `L214R-S01` · `S04` (verified) · `S03` · `S05` (open) 손대지 않음 · 새 SELF 없음 (요청서 §0 의 *"코드 diff = git diff … -- 두 파일 (+ 재고 한 줄)"* 은 경로를 박은 코드 diff 범위로 적혔고 · 122/122 는
  S06 증거 README 가 *"이 컨테이너 (Linux · Python 3.11.17)"* 로 적었다 — 판정문 §2 · §3-3 은 그 범위를 넘겨 읽지 말라는 한정으로 받는다).

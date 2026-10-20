# 반입 기록 — Codex Rint 조인 RIMPR-01 · 02 + Q7 재확인 (검토 핀 `2b9efa253` · 대조 핀 `dcb97f1ed` · 2026-10-20)

- 판정문 (리포 사본) = `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` (묶음 `rint_join_q7_recheck_20261020/` 의 같은 이름 파일 · 바이트 그대로 · `cmp` 같음 ·
  sha256 `766eecd00ec8038f890be4ec144321b07fcfc762e2f234dd637beb4dae605e7c` · 19,944 B).
- 판정 = **RIMPR-01 · 02 이전 최소 해결 조건 범위 한정 닫힘 · Q7 (일반 관문 r_face 유한 · 비음수) 닫힘 · 새 P1 · P2 없음 · ①′ 정량 채택 · 생산 HOLD 그대로** —
  새 P3 `RIMPRR-01` (원장 `RIMPR-R01` · §3 · 구역 분류 `startswith()` + 헤더 표지 전역 `replace()` → `ITEM: ATOMSid …` · `ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS` 가 조인 PASS / 정량 ACCEPT ·
  소비 배열은 정상과 같음 · σ 오염 증거 아님 · 대조 핀에도 있음 = 회귀 아님) · `RIMPR-04` 범위 보강 (§4 · 비-AM 두 구 x 1e160 → 거리 · 허용폭 norm inf → `inf > inf` 거짓 → 조인 PASS / 정량 ACCEPT ·
  *"후단이 반드시 거부하므로 무해"* 설명 철회 · 연기 조건 넷 · 새 ID 아님) · `RIMPR-03` = ASCII 생산 덤프 범위 명시 + open 유지면 연기 가능 ·
  §1 시험 수 = 현재 시험 138 을 옛 코드에 81/138 (57 FAIL) — 요청서의 78/135 (시험 작성 중간 시점) 와 같은 집합처럼 혼용 금지 · §7 *"봉인 32 무변경"* = 두 Rint 커밋 (`3b9d51789` · `2b9efa253`) 한정 ·
  대조 핀 → 검토 핀 전체 구간에서는 봉인 네 파일이 다름 (`scripts/network_conductivity.py` · `scripts/tau_flux.py` · `webapp/app.py` · `webapp/pipeline_service.py`).
- 받은 것 = Codex 간편 전달 묶음 (소스 폴더 뺀 `_review.zip`) `2368c040-codex_rint_join_rimpr_q7_recheck_20261020_review.zip` ·
  sha256 `970690f42865dc74d164866f02b68953e532d099561c83e1c0d60d7f6b762cc2` · 2,231,651 B · 항목 1,307 (뿌리 `PACKAGE_MANIFEST.json` + 검토 폴더 `rint_join_q7_recheck_20261020/` 1,127 +
  이전 10-15 검토 폴더 사본 `rint_g2_impl_reverify_20261015/` 179) · 위험 경로 0 (절대 경로 · `..` · 역슬래시 · 드라이브 · 링크) · CRC 정상 ·
  `PACKAGE_MANIFEST.json` 1,306 항목 sha256 · 크기 = 풀린 파일 전수 같음.  소스 포함 전체 묶음 (83.7 MB · sha256 `2588ff6f0185e8cd64e5d1e2e03a19c901da7d575d95485e5b50439161895127`) 은 받지 않았다.
- 반입 처리: 새 빈 폴더에 풀기 (각 항목이 대상 폴더 안에 머무는지 다시 검사) → 읽기는 `python3 -I` · 절대 경로 → 묶음 안 탐침은 **전부 먼저 읽고** 묶음 밖 새 폴더로 복사 ·
  경로 상수만 바꿔 (`_repro_ours_20261020/probe_path_changes.diff` · 그 밖 한 글자도 안 바꿈) `python3 -I -X utf8 -B` 로 실행 (아래 재현).
  실행하지 않은 것 = `probes/root_metadata.py` · `intake.py` (GitHub 네트워크 `urllib`) · `probes/package_review.py` (검토 폴더 밖에 ZIP 을 쓰는 포장 도구) — §7 은 git 으로 직접 재현했다.
- 우리 쪽 대조 (git · 10-20): Codex `source_manifest.json` 1,105 항목 = `2b9efa253` 의 blob 과 **1,105 / 1,105 같음** · 이전 폴더 `source_manifest.json` 851 = `dcb97f1ed` 의 blob 과 **851 / 851 같음** ·
  이 작업 트리 (`d8808c164`) 와 1,104 / 1,105 같음 (다른 하나 = `CLAUDE.md` · `2b9efa253` → `d8808c164` 사이에는 문서 셋만 바뀜) ⇒ **작업 트리 코드 = 검토 핀 코드**.
- 넣은 것 = 1,125 파일 (3,783,073 B) — 검토 폴더에서 판정문 · tree 목록 둘을 뺀 1,124 (README 둘 · `intake.py` · `source_manifest.json` · `notes/` 3 · `probes/` 8 · `evidence/` 31 ·
  `submitted/` 1 · `support/` 1 · 묶음 tmp 폴더 1,076 → 이 폴더 `fixtures/` (리포 `.gitignore` 의 tmp 규칙 때문에 폴더 이름만 바꿈 · 안의 이름 · 바이트 그대로)) + 뿌리 `PACKAGE_MANIFEST.json`
  + 반입 파일 (`_members_mini.tsv` · 이 README · `_repro_ours_20261020/` 29 = 그 README · 우리 출력 6 · `results_ours.json` · 경로 diff · `tools/` 20).  증거 폴더는 `.gitattributes` 의 `codex_*_evidence_*/** -text` 라 CRLF fixture 도 바이트 그대로 커밋된다.
- 넣지 않은 것 (해시 = `_members_mini.tsv` 의 status · note 열): verdict 1 (→ `docs/reviews/`) ·
  `big-hash-only` 2 = 검토 폴더 evidence 의 tree.json (3,990,688 B) · base_tree.json (3,345,839 B) — 두 핀의 GitHub tree 응답 · 내용 = `git ls-tree -r 2b9efa253` (blob 11,446) ·
  `git ls-tree -r dcb97f1ed` (blob 9,768) 와 경로 · sha · 모드 전수 같음 (10-20 확인) · 2 MB 초과 (앞선 반입과 같은 처리) ·
  `dup-repo` 179 = 이전 폴더 사본 전부 **같은 이름 · 같은 바이트**: 판정문 = `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md` ·
  `source_manifest.json` = `docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/source_manifest.json` · 원 반례 fixture 177 (그 폴더 tmp/join_independent) =
  `docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/evidence/join_fixtures/` 177 ⇒ `baseline_20261015/` 폴더는 만들지 않았다 (다른 바이트 0).
- 요청서 사본 `submitted/codex_rint_join_rimpr_q7_recheck_request_20261020_send.md` ↔ 리포 `docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` (`2b9efa253` 판 = `d8808c164` 판) =
  **다름 — 7 행 하나뿐** (리포 = 리뷰 핀 자리 표시 *"SHA 는 발송 때 1저자가 적는다"* · 발송본 = 실제 `2b9efa253edbf455c2e1abfef1d60e51818e01f8` 와 가지 이름) · 그 밖 바이트 같음 = 발송본.

## 우리 트리 재현 (10-20 · Codex 탐침 6 종 · 경로 상수만 바꿈)

- 우리 = 이 컨테이너 (Linux · 4 vCPU · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · BLAS · OpenMP 스레드 1) · 현재 코드 = 이 작업 트리 (`2b9efa253` 코드) · 대조 코드 = `git archive dcb97f1ed`
  (scripts · webapp · 탐침 · 시험이 읽는 docs/data 일곱 경로 · AGENTS.md · CLAUDE.md — 이전 manifest 851 중 꺼낸 634 가 manifest sha256 과 전부 같음 · 나머지 217 = 꺼내지 않은 리뷰 문서) ·
  옛 10-15 반례 = 묶음의 원본 바이트 (읽기만).
  Codex = Windows · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3.  우리 쪽 출력 · 대조 도구 = `_repro_ours_20261020/` (`results_ours.json` · `tools/`).
- 판정 대조는 거부 / 허용 상태 · 사유 코드 · 개수 · 수치 (경로 · 시각 · 환경 칸 제외) 전수다.  시간: 탐침 다섯 (일곱 번 실행) 합 약 70 초 · 제출 시험 new 약 4 분 (join 218 초) · old 약 3.5 분 (CPU 4 개 중 1 개씩).

| 항목 | Codex (판정문 · 증거) | 우리 트리 | 판정 |
|---|---|---|---|
| 제출 시험 (현재 코드 · `probes/run_submitted.py new`) | join 138/138 · am_iface 136/136 · rrm 55/55 · t4_census 8/8 · t43_order 6/6 · t2_dev 23/23 · `step3_sigma --selftest` · `--selftest-rint` · `rint_t41_census --selftest` PASS | 아홉 child 모두 rc 0 · 같은 수 · PASS 항목 집합 같음 | 같음 |
| 현재 시험을 옛 코드에 (`old`) | join 81/138 (57 FAIL) · am_iface 133/136 · rrm 54/55 | 같은 수 · 실패 목록 집합 같음 (FAIL 상세 줄 4 = OverflowError 문구 · 옛 NaN 계획 σ 끝자리 — 플랫폼) | 같음 |
| 구조 탐침 144 (`structure_probe.py`) | 정상 14 · 구조화 거부 112 · ValueError 8 · 헤더 false-PASS 10 (10 모두 대조 핀에서도 PASS) | 같은 분류 · 결과 JSON 잎 10,915 차이 0 | 같음 |
| 최소 반례 둘 (`structure_minimal_replay.py`) | `ITEM: ATOMSid …` · `ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS` = 조인 PASS · 정량 ACCEPT · 소비 배열 8 칸 같음 | 잎 50 차이 0 | 같음 |
| real14 · case15 정상 (구조 탐침 안) | 457/457/457 · AM–AM 660/660 인증 · 물리 행 33,289 / 106,563 · case15 104/104/104 · 119/119 · AM–SE 음수 2 = 범위 밖 | 같음 | 같음 |
| 수치 탐침 현재 113 (`numeric_review.py`) | REJECT 98 · PASS 15 · 예외 0 | 잎 7,600 차이 0 | 같음 |
| 수치 탐침 대조 핀 113 (`--baseline`) | PASS 19 · REJECT 56 · 예외 38 | 같은 수 · 차이 10 = int64 넘침 OverflowError 문구 (Windows *int too big to convert* ↔ Linux *Python int too large to convert to C long*) | 같음 (문구만) |
| 넘침 반례 (`numeric_overflow_replay.py` · 두 핀) | 1e150 대조 = REJECT / ValueError (n_delta_pos_mismatch 1 · 비 99,999.99998223643) · 1e160 = PASS / ACCEPT (거리 · 허용폭 norm inf · inf · n 0 · 비 NaN) | 잎 48 · 48 차이 0 | 같음 |
| Q7 음성 36 (`q7_independent.py`) | x · y · z × CNC · RRM 막 행 × NaN · +inf · −inf · 음수 (24) + RRM 절단 tombstone (12) → 관문 · 솔버 ValueError · CG 호출 0 | 36/36 같음 | 같음 |
| Q7 양성 여섯 σ (직접해법 `spsolve`) | CNC 0.0038116099134384756 · r0 = OFF 0.004141925781633665 · ×2 0.0035313954366456347 · RRM 0.003334457143882423 · r0 0.0037299595666211234 · ×2 0.0030984308118989293 | 끝자리만 다름 — 상대 4.6e-16 ~ 1.6e-15 (예: RRM r0 …1278) · 조립 행렬 · 우변 해시는 Codex 와 **같음** · 같은 기계 안 옛/새 전체 반환 같음 · CNC r0 = OFF (σ hex · φ 바이트) 같음 | 다름 (반올림 · 판정 같음) |
| N9b 옛 NaN 계획 ≡ 등록 r0 | σ hex · φ 바이트 · n_dof · 잔차 hex · 행렬/우변 다섯 항목 같음 | 우리 기계에서도 다섯 항목 같음 | 같음 |
| N9b φ SHA256 | `c62f2830…` (σ hex `0x1.e8e4acb544bd1p-9`) | `fe37433c…` (σ hex `0x1.e8e4acb544bdbp-9`) · 최대 φ 차 1.8e-15 (φ 범위 0.98) · 원인 = 위 직접해법 끝자리 | 다름 (같은 원인) |
| N9b 절단 85 삭제 | 일반 관문 통과 · σ 0.0040840140889134725 · RRM wrapper = CG 전 거부 · 독립 원장 `film_off_outside` (n=85) | σ 0.004084014088913466 (상대 1.5e-15) · 나머지 같음 | 같음 (σ 끝자리만) |
| OFF 16 쌍 · 원래 CG 4 쌍 · schema 경계 10 | 옛/새 전체 반환 같음 · CG 수렴 (잔차 8.6–9.2e-9) · 경계 허용/거부 · 예외 종류 | 같음 (값 끝자리 ≤ 7e-15 · CG 잔차 상대 2.4e-8) | 같음 |
| §7 봉인 32 범위 (git 직접) | 두 Rint 커밋이 건드린 봉인 파일 0 · `dcb97f1ed` → `2b9efa253` 봉인 네 파일 다름 · S3 `NUMERIC_MODULES` 6 무변경 | `git diff --name-only` · `git show --name-only` 로 같음 | 같음 |
| 다시 만든 fixture 바이트 | (Codex Windows) | numeric 678 = 줄 끝 CRLF ↔ LF 만 (Codex `write_text`) · structure 396 = 393 바이트 같음 + gz 3 풀면 같음 · minimal 2 = CRLF 만 | 같음 (내용) |

- 미재현 = 없음 (돌린 탐침 6 종 전부 끝남 · 각 수 분 안).  실행하지 않은 셋 (네트워크 · 포장) 은 위 처리 절.
- 한정: 우리 재현은 같은 탐침 · 같은 입력의 **판정값** 재현이다 — `check_all.sh` 전체 · WSL · 생산 σ 재계산 아님 (판정문 §1 과 같은 범위).

## 폴더 꼴 · 참조 예외 · 원장

- 폴더 꼴: 이 폴더 = 묶음의 `rint_join_q7_recheck_20261020/` (판정문 · notes · README 의 상대 경로 `evidence/…` · `probes/…` · `notes/…` · `tmp/…` 의 루트) − 판정문 − tree 목록 둘 + 묶음 tmp → `fixtures/` +
  뿌리 `PACKAGE_MANIFEST.json` + 반입 파일.  판정문 · notes 의 `source/…` 경로 = Codex 작업 공간의 고정 핀 사본 (= 리포 `2b9efa253` 의 같은 경로 · 간편 묶음에 없음) ·
  `C:/Users/…` = Codex 작업 공간 (Windows).
- 참조 검사 예외 = `docs/reviews/doc_refs_allowlist.tsv` (이 묶음 루트 기준 상대 경로 · `external` · 리포 사본 sha256 · 실행하지 않음 표지).
- 원장 (`docs/reviews/findings.json`): `RIMPR-01` · `RIMPR-02` → verified (verified_sha `2b9efa253` · 범위 = 판정문 §0 · §2 · §4) · `RIMPR-03` · `RIMPR-04` = open 유지 (note 에 §4 보강) ·
  신설 `RIMPR-R01` (= Codex 표기 `RIMPRR-01` · 원장 ID 규칙이 접두 5 글자까지라 선례 `L214RR-01` → `L214R-R01` 와 같은 꼴 · P3 · open · 수정 계획 `docs/reviews/rimprr_fix_plan_20261020.md` ⬜ 1저자 비준) ·
  신설 `SELF-124` (P3 · open · 요청서의 범위 한정 없는 *"봉인 32 무변경"* · 78/135 → 138/138 표기) ·
  Q7 전용 원장 항목은 없다 (권고는 `RIMPR-01` note 에만 · 새로 만들지 않음) · `RIMP-02` 는 손대지 않음 (note 의 닫는 조건 = *"RIMPR-01 · 02 수정 + 짧은 재확인"* → 이번 판정으로 충족).

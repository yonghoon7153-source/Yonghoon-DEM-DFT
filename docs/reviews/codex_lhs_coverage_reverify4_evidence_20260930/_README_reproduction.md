# Codex 재검증 4 (LHSC-03-R4 · LHSC-04-R4-PIN · R4-DOMAIN · 패치 0016 · 0017) — 반입 + 우리 트리 재현 (2026-09-30 밤)

- 판정문: `docs/reviews/codex_lhs_coverage_reverify4_verdict_20260930.md` (**HOLD · 새 P1 없음 · 이전 P2 둘 (LHSC-03-R4 · LHSC-04-R4-PIN) 닫힘 · 새 P2 한 계열 LHSC-03-R5 · P3 둘 (LHSC-04-R5-PIN-TYPE · R5-DOMAIN)** · 155 행 · sha256 `d0939f8bb289039c0a355fb692d40594aab0cbea0cf98967fa4bcc0a119b36ba` · `PACKAGE_SHA256SUMS.json` 과 일치).
- 반입 원본: 사용자 전달 zip `codex_lhs_coverage_reverify4_20260930.zip` (Codex 전달용 결과 묶음 — 우리가 보낸 요청 zip 과 이름이 같다) — 652,831 B · sha256 `9d38219b736f69d0391704380988e0dff960cff073699526f106d79907c4a4ae` · 172 파일 · `PACKAGE_SHA256SUMS.json` 171/171 일치.
  이 폴더 = zip 의 `lhs_coverage_reverify4_20260930/evidence/` 의 파일 전부 (스크립트 10 · 결과 JSON 9 · 로그 8 · README · run_selftests) + `codex_source_manifest.json` (zip 의 `source_manifest.json`) + `PACKAGE_SHA256SUMS.json`.
  ⚠ 뺀 것: `evidence/r4_fixtures/` 19 · `evidence/r5_fixtures/` 25 · `evidence/schema_fixtures/` 69 (감사 스크립트가 실행 때 다시 만든다) · `candidate/` 10 (아래 대조로 우리 트리와 같음) · `submitted/` 11 (우리가 보낸 묶음 사본) · `prepare.py` · 앞 라운드 사본 셋 (재검증 3 의 source manifest · 재검증 1 증거 README · 첫 리뷰 README).
- Codex 가 본 트리: 재검증 3 후보 사본에 패치 0016 → 0017 (`git apply --check` 뒤) = 우리 검토 브랜치 `review-coverage-20260930` tip **`9ab4bc320`**.  **후보 10 파일 ↔ 우리 worktree: LF 정규화 뒤 10/10 동일.**

## 우리 재현 — Codex 스크립트를 **무변경**으로 우리 worktree 에 (Linux · Python 3.11 · `candidate` → worktree 심볼릭 링크 · `SUPABASE_*` 비움)

| 스크립트 | 우리 결과 파일 | Codex 결과와의 차이 |
|---|---|---|
| `audit_r5.py` | `_reproduction_r5_results_wtcov_9ab4bc320.json` | **판정값 0** — 생산자 대조 (0 접촉 · 부분 · 전체 클립) 3/3 True · 변이 `below_clip_lower_bound` False / failed · **`all_clipped_but_phase_mean_zero` · `all_clipped_but_phase_std_40` True / done** (= 새 R5) · `unverified_phase_weight_example` True / done · pin 8 종 (claim · 로컬 대조 · installed False) 같음 · `bad_hosts_type` TypeError 같음 · domain: 1e-100 E = ∞ 미인증 · **1e160 `contact_area_check` OverflowError** 같음 · normal · 1e-60 같음.  다른 것 = 경로 문자열 (Windows ↔ Linux) · 픽스처 `source.txt` 의 sha256 (Windows 줄끝) · OverflowError 문구 (`Result too large` ↔ `Numerical result out of range`) 뿐 |
| `audit_r4.py` · `audit_schema.py` · `audit_numeric_domain.py` · `audit_producer.py` | (수정 전 트리에서는 재실행 안 함 — 재검증 3 반입 때 같은 트리 상태로 재현했다) · **고친 트리 (6e4ef6925) 실행 = `docs/reviews/codex_lhs_coverage_reverify5_request_20260930/fixed_tree_reproduction/`** | — |
| `audit_error_3d.py` · `audit_geometry.py` · `audit_power_boundary.py` · `audit_regression.py` · `run_selftests.py` | 재실행 안 함 (이번 수정 (검증기 · pin hosts 형식) 과 무관한 수치 검산 · Windows 환경 대조) — Codex 결과를 그대로 둔다 | — |

⇒ **Codex 의 새 잔여 (LHSC-03-R5 P2 · LHSC-04-R5-PIN-TYPE P3 · R5-DOMAIN P3) 는 우리 트리에서 그대로 재현된다.**  수정 (R5 · PIN-TYPE) 은 Codex 최소 해제 그대로 · 반례를 셀프테스트로 먼저 → `docs/reviews/codex_lhs_coverage_reverify5_request_20260930.md`.  R5-DOMAIN 은 열어 둔다 (비차단).

## 한정

- 격리 사본의 CPU 합성 시험 — DEM · 실 130/64 · 설치 엔진 실행 없음 (Codex 도 같은 한정).  Codex 의 `harvest` · `batch` 원본 selftest rc 1 은 Windows 원형 (CRLF fixture hash · τ median 1 ULP · symlink WinError 1314) — Linux 에는 없다 (우리 로그 = 요청 묶음 `selftests_*.log`).
- 판정문 안의 `C:/Users/Administrator/Documents/Codex/…` 링크는 Codex 작업 폴더 경로다 (이 리포에 없다).

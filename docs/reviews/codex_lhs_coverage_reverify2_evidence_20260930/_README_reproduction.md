# Codex 재검증 2 (LHS 피복률 · LHSC-03 R2 · LHSC-04 R2 수정) — 반입 + 우리 트리 재현 (2026-09-30 밤)

- 판정문: `docs/reviews/codex_lhs_coverage_reverify2_verdict_20260930.md` (**HOLD · 새 P1 없음 · P2 R3 셋** — sha256 `f95319582336a0fb5ea40c902b3eb36b87ea5460582a5bd6f1ad58c8d0c6470d` · 191 행 · `PACKAGE_SHA256SUMS.json` 과 일치).
- 반입 원본: 사용자 전달 zip `codex_lhs_coverage_reverify2_20260930.zip` — 568,677 B · sha256 `647e5b9704510b47c8431047c2f02db67b1f7e4227a2ecd81a236586a49b4a84` · 117 파일.
  이 폴더 = zip 의 `lhs_coverage_reverify2_20260930/evidence/` 전부 (스크립트 6 · 결과 JSON 6 · 로그 8 · README · package_review) + `PACKAGE_SHA256SUMS.json`.
  ⚠ 뺀 것: `evidence/schema_fixtures/` 69 파일 (양성 8 케이스의 atoms/contacts/coverage_per_am/full_metrics/meta/se_clusters + 변이 22 의 full_metrics) — 전부 `audit_schema.py` 가 실행 때 `_selftest_fixture` 로 **다시 만든다** (재현 파일이 같은 내용을 담는다).  zip 의 `candidate/` (후보 소스 9 파일 + AGENTS.md) 도 뺐다 — 아래 대조로 우리 검토 worktree 와 같음을 확인했다.
- Codex 가 본 트리: 이전 후보 (`002cc2881` 사본) 에 패치 0012 → 0013 적용 (`git apply --check` 뒤) = 우리 검토 브랜치 `review-coverage-20260930` tip **`ca0471d19`**.  **후보 10 파일 ↔ 우리 worktree: CRLF 정규화 뒤 sha256 10/10 동일** (raw 는 Windows 줄끝으로 8 파일 다름 · `pipeline_service.py` · `AGENTS.md` 는 raw 도 같음).

## 우리 재현 — Codex 스크립트를 **한 글자도 안 바꾸고** 우리 worktree 에 (Linux · Python 3.11 · `candidate` → worktree 심볼릭 링크 · `SUPABASE_*` 비움)

| 스크립트 | 우리 결과 파일 | Codex 결과와의 차이 (경로 · 플랫폼 문자열 제외 · 실수는 상대 1e-12) |
|---|---|---|
| `audit_schema.py` | `_reproduction_schema_results_wtcov_ca0471d19.json` | **0** — 양성 8 전부 accepted · 옛 변이 10 전부 거부 · 추가 변이 12: `missing_fractions` · `none_fractions` (필수 단계 **done**) · `wrong_fractions` · `empty_count_dicts` (**done**) · `unknown_binding_keys` · `contradictory_count_totals` · `n_am_zero_positive_area` (**done**) · `zero_contacts_positive_area` · `blank_bad_film` · `blank_none_rule` · `blank_missing_film` 전부 accepted · `huge_integer_area` = helper OverflowError · 필수 단계 failed |
| `audit_power.py` | `_reproduction_power_results_wtcov_ca0471d19.json` | **0** — seed 4813 · 431 번째 상자 · 정상 토큰 beyond 0 · wide 1 · power 0 / +1 % 토큰 beyond 0 · wide 0 · **power 1** |
| `audit_producer.py` | `_reproduction_producer_results_wtcov_ca0471d19.json` | **0** — normal beyond 0 · `equal_deep_1e-12` **beyond 1** (생산 식 A 3.142020451916476e-6 > π r² · 구간 [0, 3.1416240695948997e-6]) · `equal_deep_1e-13` beyond 0 (하한 0 가지) · `contained` 생산 식 −1.5088371383490986e-6 (beyond 1) · `no_contact` −3.2201324699295325e-7 (beyond 1) |
| `audit_geometry.py` | `_reproduction_geometry_results_wtcov_ca0471d19.json` | **0** — 12,000 상자 × 24 점 = 288,000 점 · corner 6,489 · zero 4,099 · interval 429 · boundary 983 · Decimal 80 / 실제 함수 이탈 **0 / 0** · 옛 R2 반례 구간 [2.660084532696906e-6, 4.7882607651360736e-6] 초과 0 · 옛 rounding 0 · Hertz 0 · 3e-5 치환 1 · 경계 대조 (비접촉 0 면적 허용 · δ = 0 양수 면적 검출) 동일 · lo = 0 인데 `lower_bound_flag` False 인 예 8 (P3 라벨) · 깨끗한 import 에 plastic_coverage 없음 · 6.6 s |
| `run_selftests.py` | (재실행 안 함) | 우리 트리의 같은 6 셀프테스트 로그 = `docs/reviews/codex_lhs_coverage_reverify2_request_20260930/selftests_ca0471d19.log` (수확기 149 · lens 7 · plastic 28 · coverage 16 · 배치 30 · 파이프라인 209 · rc 전부 0).  Codex 의 Windows 원형 실패 (fixture CRLF 해시 · τ 중앙값 1 ULP · symlink WinError 1314) 는 Linux 에 없다 (앞 라운드와 같음) |
| `audit_regression.py` | (재실행 안 함) | 이전 후보 `baseline` 사본이 필요한 Windows 통제 — legacy 36 키 × 16 호출 불일치 0 은 Codex 결과 (`regression_results.json`) 로 둔다 |

⇒ **Codex 의 세 잔여 (LHSC-03 R3 · LHSC-04 R3a · R3b) 와 P3 둘은 우리 트리에서 그대로 재현된다.**  수정은 1저자 비준 뒤 · 반례를 셀프테스트로 먼저.

## 한정

- 이것은 격리 사본의 CPU 합성 시험이다 — DEM · 실 130/64 재수확 · coverage 배치 · 설치된 LIGGGHTS 빌드 인증이 아니다 (Codex 도 같은 한정).
- R3a 의 생산자 식은 **공개 PUBLIC master `compute_pair_gran_local.cpp add_pair`** 를 연산 순서대로 옮긴 스칼라 계산이다 — 사용자 WSL · ibb 의 설치 빌드가 같은 소스인지는 **미확인** (해제 항목).
- `docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md` (앞 라운드 판정문) 도 zip 에 들어 있었다 — 우리 커밋본과 대조하지 않고 그대로 둔다 (앞 라운드 반입분이 정본).

# Codex 재검증 3 (LHSC-03 R3 · LHSC-04 R3a · R3b · 패치 0014 · 0015) — 반입 + 우리 트리 재현 (2026-09-30 밤)

- 판정문: `docs/reviews/codex_lhs_coverage_reverify3_verdict_20260930.md` (**HOLD 유지 · 새 P1 없음 · P2 둘 (LHSC-03-R4 · LHSC-04-R4-PIN) · P3 하나 (LHSC-04-R4-DOMAIN)** · 190 행).
- 반입 원본: 사용자 전달 zip `codex_lhs_coverage_reverify3_20260930.zip` — 647,715 B · sha256 `393ffbff891316e4bd953f4de299249159d1617a23023c2561d64a785187e40a` · 153 파일.
  이 폴더 = zip 의 `lhs_coverage_reverify3_20260930/evidence/` 의 파일 전부 (스크립트 · 결과 JSON · 로그 · README) + `codex_source_manifest.json` (zip 의 `source_manifest.json`).
  ⚠ 뺀 것: `evidence/r4_fixtures/` · `evidence/schema_fixtures/` (89 파일 — 감사 스크립트가 실행 때 다시 만든다) · `candidate/` (아래 대조로 우리 트리와 같음) · `submitted/` (우리가 보낸 묶음 사본) · `lhs_coverage_reverify2_20260930/` (앞 라운드 사본).
- Codex 가 본 트리: 앞 후보 사본에 패치 0014 → 0015 (`git apply --check` 뒤) = 우리 검토 브랜치 `review-coverage-20260930` tip **`220b1426e`**.  **후보 10 파일 ↔ 우리 worktree: LF 정규화 뒤 10/10 동일.**

## 우리 재현 — Codex 스크립트를 **무변경**으로 우리 worktree 에 (Linux · Python 3.11 · `candidate` → worktree 심볼릭 링크)

| 스크립트 | 우리 결과 파일 | Codex 결과와의 차이 (경로 · 시각 제외 · 실수 상대 1e-12) |
|---|---|---|
| `audit_r4.py` | `_reproduction_r4_results_wtcov_220b1426e.json` | **0** — 가짜 pin 둘 (없는 소스 · build 없음 / add_pair 없는 파일 · 0×64 해시) 모두 `pinned=True` · `installed_build_pinned=True` · 장부 모순 넷 (접촉 0 인데 피복률 50 % · 전 AM 클립인데 평균 1.218 % · std 75 %p · cap 11 = elastic · none 포함) 모두 검증기 True · 필수 단계 **done** |
| `audit_numeric_domain.py` | `_reproduction_numeric_domain_results_wtcov_220b1426e.json` | **0** — r1 = r2 = 1e-100 · d 1.9e-100: 생산 면적 0 (언더플로) · E 0 · \|오차\| > E |
| `audit_producer.py` | `_reproduction_producer_results_wtcov_220b1426e.json` | **0** — 동심 둘 미인증 · 음수 둘 따로 |
| `audit_schema.py` | `_reproduction_schema_results_wtcov_220b1426e.json` | **0** — 양성 8 허용 · 옛 변이 20 거부 · 정당한 blank 허용 |
| `audit_error_3d.py` | `_reproduction_error_3d_results_wtcov_220b1426e.json` | **0** — 17,926 점 \|A_p − A_e\| > E 0 · 최대 비 0.2131 · 인증 행 8,170 거짓 초과 0 · detect 5,928 행 ±1 % 누락 0 |
| `audit_power_boundary.py` | `_reproduction_power_boundary_results_wtcov_220b1426e.json` | **0** — 500,000 구간 · 보증 263,988 · 치환 1,980,567 누락 0 |

⇒ **Codex 의 새 잔여 (LHSC-03-R4 · LHSC-04-R4-PIN · R4-DOMAIN) 는 우리 트리에서 그대로 재현된다.**  수정은 1저자 비준 뒤 · 반례를 셀프테스트로 먼저.

## 한정

- 격리 사본의 CPU 합성 시험 — DEM · 실 130/64 · 설치 엔진 실행 없음 (Codex 도 같은 한정).
- `audit_regression.py` · `run_selftests.py` 는 재실행하지 않았다 (Windows 환경 대조 · 우리 Linux 셀프테스트 로그는 재검증 3 요청 묶음에 있다).

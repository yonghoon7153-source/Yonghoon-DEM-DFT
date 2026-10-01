# Codex ps45 공극률 검토 — 반입 · 재현 (2026-10-01 밤)

- 판정문: `docs/reviews/codex_ps45_porosity_verdict_20261001.md` — **수치 산술 재현 / 정확도 검증 · 인과 귀속 HOLD** (P1 셋 = 주장 · 사용 차단 조건 · 코드 수정 요청 아님).
- 받은 zip `codex_ps45_porosity_review_20261001.zip` sha256 `a6533ba9ddfac826ebac7623533d09851ec4d337fb76dfd5d83402b7ec5b23b8` (1저자 전달) · 요청 zip sha256 `3bdee6ba…` (판정문 §1).
- 이 폴더 = 받은 그대로 (`audit_porosity.py` · `package_review.py` · `unpack.py` · 매니페스트 셋 · `evidence/` · `inputs/` · `reference/dem_scripts/` · `reference/normal_model_hooke_hysteresis.h` — LIGGGHTS-PUBLIC 공개 소스 사본).
- 넣지 않은 사본 (리포에 원본이 있다 — 해시만):
```
abee9d77ab2589ec511b978a98c0a548c4f6b06c56dcd29f8781899e7d75ad74  CLAUDE.md
38b8708ba8a50c8a08819c7c4138763bce02b6dc6c5b8112f4c8aa386fb17ec3  AGENTS.md
839129f36f5f7bc3dae2b1a0be8a12dcfc8bf5b9c7c8653aea68480551cd9747  docs/se_curve_transfer_verdict_20260806.md
```
- 판정문 바이트 변경 1 곳: `evidence/deck_provenance.csv` → 리포 경로 (문서 참조 게이트 `check_doc_refs.py` 가 판정문 위치 기준으로 풀어 깨진 참조로 잡음).  원본 바이트 sha256 은 `DELIVERY_MANIFEST.json` 에 있다.

## 우리 쪽 재현 (10-01 밤 · 컨테이너)
```
cd docs/reviews/codex_ps45_porosity_evidence_20261001 && python3 audit_porosity.py
```
- **94/94 통과** · `evidence/` 다섯 CSV · JSON 중 `recomputed_5beds.csv` · `density_springback_sensitivity.csv` · `descriptive_comparisons.csv` · `deck_provenance.csv` 는 바이트 동일.
- 다른 둘 = `CI_planning_examples.csv` · `audit_result.json` 의 t-신뢰구간 반폭 두 값의 **소수 14 자리 이후** (0.46242287415902045 → 0.4624228741590222 · 0.4972883007129521 → 0.4972883007129839) — scipy 버전 차 (우리 1.17.1).  판정 내용 무관.  ⚠ 재실행은 `evidence/` 를 덮어쓴다 — 커밋된 바이트는 받은 원본이다.

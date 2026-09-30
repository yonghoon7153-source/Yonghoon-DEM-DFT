# Codex 재검증 5 (LHSC-03-R5 · LHSC-04-R5-PIN-TYPE · 패치 0018 · 0019) = **GO** — 반입 + 병합 트리 재현 (2026-09-30 밤)

- 판정문: `docs/reviews/codex_lhs_coverage_reverify5_verdict_20260930.md` (**GO · 새 P1 · P2 없음 · LHSC-03-R5 (P2) · LHSC-04-R5-PIN-TYPE (P3) 닫힘 · LHSC-04-R5-DOMAIN (P3) 비차단 열림 · 병합 순서 0001 → … → 0019 → 게이트 → 트리 해시 → 새 디렉터리 동의** · 159 행 · sha256 `1d0b825ed36e590b2d49235c927c11cb5ceffa54d0c04099cbfa2b61c9da3682` · `PACKAGE_SHA256SUMS.json` 과 일치).
- 반입 원본: 사용자 전달 zip `codex_lhs_coverage_reverify5_result_20260930.zip` — 886,625 B · sha256 `e40910eb3ca685650a5b48407e2662b4c825dbb3c4b6e1daa6d979e753d21995` · 227 파일 · `PACKAGE_SHA256SUMS.json` **226/226 일치**.
  이 폴더 = zip 의 `lhs_coverage_reverify5_20260930/evidence/` 파일 전부 33 (스크립트 12 · 결과 JSON 11 · 로그 9 · README) + `codex_source_manifest.json` (zip 의 `source_manifest.json`) + `PACKAGE_SHA256SUMS.json` + 우리 재현 셋 (`_reproduction_*`).
  ⚠ 뺀 것: 픽스처 네 폴더 (`r4_fixtures` · `r5_fixtures` · `r6_fixtures` · `schema_fixtures` = 161 파일 — 감사 스크립트가 실행 때 다시 만든다) · `candidate/` (아래 대조로 우리 트리와 같음) · `submitted/` (우리가 보낸 요청 묶음 사본) · `prepare.py` · 앞 라운드 사본 (재검증 4 판정문 = 리포 사본과 **바이트 동일** · 재검증 4 후보 `app.py` · manifest · 재검증 1 증거 · 첫 리뷰 baseline 수확기).

## 소스 세대 대조 — Codex §5 ① (검증한 바이트 ↔ 실제 통합 결과)

| 대조 | 결과 |
|---|---|
| Codex 후보 3 파일 (`lhs_descriptor_harvest.py` · `webapp/app.py` · `webapp/test_pipeline_provenance.py`) git blob ↔ 검토 브랜치 tip `6e4ef6925` | **3/3 같음** (`ce0fdf14` · `26a13ca8` · `5fbaee0f`) |
| 병합 방법 | 본 브랜치 `c1233581a` 위에 검토 브랜치 19 커밋 (`da4670594..6e4ef6925`) 을 **0001 → 0019 순서대로** `cherry-pick -x` → `15ecbbc9a` … `9514b851a` |
| 본 브랜치가 안 건드린 7 파일 (`area_contract` · `coverage_physics_vs_hertzian` · `lens_geometry` · `lhs_descriptor_harvest` · `lhs_webapp_batch` · `plastic_coverage` · `test_pipeline_provenance`) | 병합 결과 = 검토 tip blob **7/7 동일** |
| `webapp/app.py` (양쪽이 고침) | 자동 병합 (충돌 0) · 병합 결과 − 검토 tip 의 변경 줄 **19 = 본 브랜치 자신의 `app.py` 변경 (7a · `da4670594` → `8e8474a68`) 19 줄과 바이트 동일** ⇒ 통합이 더한 것 = 본 브랜치 변경뿐 |
| `docs/reviews/selftest_inventory.tsv` | 충돌 2 번 (0010 · 0012 적용 때) — 줄 단위 해결: 검토 커밋의 줄 (`lens_geometry` · `lhs_descriptor_harvest`) + 본 브랜치의 `lhs_design_dataset` 줄 (7b · 137 건) · 코드 아님 |

## 병합 트리 재현 — Codex 스크립트 **무변경** (Linux · Python 3.11.15 · `candidate` → 병합 worktree 심볼릭 링크 · `SUPABASE_*` 비움)

| 스크립트 | 우리 결과 파일 | Codex 결과와의 차이 |
|---|---|---|
| `audit_r5.py` | `_reproduction_r5_results_merged.json` | rc 0 · 잎 629 = 629 · **판정값 차이 0** — 다른 것 = 경로 44 · 픽스처 바이트 sha 20 (Windows 줄끝) · OverflowError 문구 1 (`Result too large` ↔ `Numerical result out of range` — R5-DOMAIN 반례가 그대로 재현된다) |
| `audit_r6.py` | `_reproduction_r6_results_merged.json` · `_reproduction_resident_rollback_merged.log` | rc 0 (스크립트 안 `assert` 전부 통과) · 잎 839 = 839 · **판정값 차이 0** (경로 91 · 픽스처 sha 48) — 생산자 대조 5 종 허용 · 끝점 변이 5 종 거부 · pin 15 종 기대대로 · **상주 회귀 롤백 214/216 · 실패 = T11s · T11t 만** (Codex 와 같다) |
| 영향 selftest 6 (병합 트리) | — | `lens_geometry` · `plastic_coverage` · `coverage_physics_vs_hertzian` · `lhs_descriptor_harvest` · `lhs_webapp_batch` · `webapp/test_pipeline_provenance.py` **216/216** — 전부 rc 0 |

우리 재현 JSON 안의 로컬 작업 경로 (scratchpad) 는 `<SCRATCH>/` 로 바꿔 실었다 (값 비교 뒤 · 판정값 무관).

## 원장 (같은 커밋)

- `LHSC-01` · `02` · `05` · `06` → **verified** (Codex 재검증 1 에서 닫힘 · 병합 SHA) · `LHSC-03` · `04` → **verified** (재검증 5 · 병합 SHA `5a77d6e90` · `9514b851a`).
- `LHSC-11` 새로 (P3 · 열림 · 비차단) = R5-DOMAIN (1e160 sim OverflowError).
- `LHSC-07` · `08` · `09` · `10` (P3) 은 **열림 그대로** — 08 · 09 · 10 은 5번 재수확 보고 항목 (근접 접선 수 · 단일 영상 확인 · v2 코퍼스 비율 · 라벨).

## 한정 (Codex §5 ③ ④ 그대로)

- `installed_build_pinned` = **False** 그대로 (pin = 소스 · 식 **자기 신고**) · R5-DOMAIN 열림 — 모든 유한 입력이 예외 없이 미인증 기록으로 돌아온다는 전역 주장 금지.
- 이 재현은 CPU 합성 시험이다 — DEM · 실 130/64 재수확 · 설치 엔진 실행 없음.  실제 값은 **새 디렉터리** 재수확 · coverage 배치 뒤 (5번) · 기존 결과를 덮어쓰거나 다른 세대와 섞지 않는다.
- v2 (`*_physics_v2`) = **미검증 후보 연산자** (`LHSC-10`) · `OK` = 계산 상태 ≠ 물리 적격성.
- 판정문 안의 `C:/Users/Administrator/Documents/Codex/…` 링크는 Codex 작업 폴더 경로다 (이 리포에 없다).

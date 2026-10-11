# DEM 언로딩 등록 Codex 검토 — 증거 반입 (10-11) · 우리 트리 재확인

정본 판정 = `docs/reviews/codex_review_dem_unloading_prereg_20261011.md` (검토 핀 `a20fc1875` · LIGGGHTS 고정 `3d5c00f` · **HOLD** — 계단식 언로딩 · 1 MPa 주 값 · 선택된 실험 자료를 독립 검증으로 쓰지 않는 제한은 유지 가능 · 새 finding UL-01 ~ 10).
Codex 묶음 설명 = 이 폴더 `README_REVIEW.md` (묶음의 `README.md` 를 이름만 바꿨다).

## 1. 받은 것 · 넣은 것

| 묶음 | 크기 · 파일 | sha256 | 리포 |
|---|---|---|---|
| `codex_dem_unloading_prereg_review_20261011.zip` (1저자 첨부) | 1,062,322 B · 160 파일 (풀면 3.0 MB) | `848afcc42838e5c76a9c5fe36ef28b94c2b0b378464702edabf2d54b46fb54ca` | 아래 표만 |

- 묶음 sha256 표 (`review_bundle_manifest.json` · 159 행 · 자기 제외) 대조 = **159 / 159 같음** (풀어 놓은 전부) · 반입한 20 파일 + 판정문도 같음.
- 첨부된 요청서 (`submitted_request.md`) = 리포 `docs/reviews/codex_dem_unloading_prereg_request_20261009.md` 와 sha256 `972aafa6…` 같음 (판정문 §0 · `evidence/pin_receipt.json`) → 사본은 넣지 않았다.
- ibb 주소 · 포트 없음 (검색).  `home/yonghoon/…` = 로그 묶음 안 경로 (사용자 이름 · 리포에 이미 있는 꼴).

| 무엇 | 반입 | 빠진 것 |
|---|---|---|
| 판정문 | `docs/reviews/codex_review_dem_unloading_prereg_20261011.md` | — |
| 묶음 README · `review_bundle_manifest.json` · `source_manifest.json` · `upstream_manifest.json` · `prepare_sources.py` | 전부 | — |
| `evidence/` JSON 7 (`counterexamples` · `design_arithmetic` · `original_log_recheck` · `physics_arithmetic` · `pin_receipt` · `ps73_archive_inventory` · `reproduction_receipt`) | 전부 | — |
| `evidence/ps73_logs/` (r8 원 로그 · 덱 · 러너 12 파일) | — | 리포 `docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz` 를 푼 것 (목록 = `evidence/ps73_archive_inventory.json`) |
| `notes/` 셋 (이력 · 물리 · 설계 상세) · `probes/` 여섯 | 전부 | — |
| `source/` 94 파일 (2.1 MB) | — | 핀 `a20fc1875` 의 리포 파일 사본 — `source_manifest.json` 의 blob · sha256 으로 리포에서 다시 만든다 |
| `upstream/` 27 · `notes/source_extra/` 5 (LIGGGHTS-PUBLIC 원문) | — | 고정 `3d5c00f` 공개 저장소 원문 (`upstream_manifest.json` · 묶음 표에 sha256) — 판정문의 줄 번호 링크가 같은 커밋을 가리킨다 |

## 2. 우리 트리 재확인 (10-11 · HEAD `77e0594c3` 의 파일 · 컨테이너 Linux · Python 3.11 · DEM 실행 없음)

`_repro_ours_20261011/ul_checks_ours.py` → `ul_checks_ours.json` (우리 코드 · Codex 탐침을 돌리지 않고 같은 입력을 다시 썼다):

| 항목 | 판정문 | 우리 |
|---|---|---|
| UL-02 — 중력과 정확히 평형인 5 구 사슬을 우리 `scripts/plane_load_share.py` (sha256 `a1d95cb9…` = Codex 사본과 같음) `compute()` 에 | `balance_residual` 0.0400 > 0.001 · 총힘 최대 2.2e-20 N | **같다** (0.040000000000000015 · 2.202285662861181e-20 N · S3 FAIL) |
| UL-03 — 첫 교차 A 괄호 0.20 µm vs 등록 B 0.05 µm (7:3 h0 111.052 µm) | 0.180096 vs 0.045024 %p | **같다** |
| Q3 축척 — 덱 머리 명목 개수 282 · 1,375 · 158,765 · 덱 면적 0.0025 m² | 0.90410 kg · 보고 자중 3.5477 MPa · 보조 g 9.81e-6 | **같다** |
| Q6 δ_lim 표 — 덱 `coefficientMaxElasticStiffness` · `coefficientPlasticityDepth` (m6 · m8) · 반지름 | 0.003125 · 0.012 · 0.0135 · 0.015 · 0.300 · 0.41538 · 0.675 µm | **같다** (덱 원문 `docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` 의 m6 · m7 · m8 대조) |

- 한정: 합성 반례 · 명목 산술의 재확인이다 — 언로딩 결과가 아니다 · 실제 침대의 S3 실패율 · 포화율 · 회복량은 미측정.
- 재현 명령: `python3 -I -B docs/reviews/codex_dem_unloading_prereg_review_evidence_20261011/_repro_ours_20261011/ul_checks_ours.py <리포> out.json`.

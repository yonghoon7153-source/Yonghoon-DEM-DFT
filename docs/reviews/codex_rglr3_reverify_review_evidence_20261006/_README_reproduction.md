# Codex 5차 재검증 (RGLR3 · 194 인계 v1.2) — 반입 · 우리 트리 재현 (2026-10-06)

- 판정문: `docs/reviews/codex_review_rglr3_reverify_20261006.md` (핀 `92b6ebde1` · 바이트 그대로).
- 받은 묶음: `codex_rglr3_reverify_review_20261006.zip` · sha256 `b961452942b12091311a35a6e29ae0c4cca82fadf98435fe0b832869cfd85043` · 1,529 항목 · 루트 `rglr3_reverify_20261006/` (1저자 전달 10-06 04시 KST).
- 반입한 것: manifest 7 · 실행기 4 (`verify_final_acquisition.py` · `run_tests.py` · `run_probes.py` · `record_environment.py`) · `probes/` 16 · `evidence/` 205.
- 반입하지 않은 것 (`_reproduction_compare_linux.json` `excluded_from_repo` 에 sha256 · 대조 결과):
  - `source/` 688 파일 — **전부 우리 HEAD (`92b6ebde1`) 의 같은 경로 blob 과 같다** (manifest 458 · 획득 207 · 우리 증거 ZIP 26 · 겹침은 한 번만 셈).  `source_manifest.json` · `final_acquisition.json` · `incoming_manifest.json` 으로 복원한다.
  - `tau_sources/` 582 파일 — 커밋된 `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz` 의 582 파일과 바이트 동일.
  - `diffs/` 24 (핀 사이 diff · 4차 반입과 같은 처리) · `inputs/` 2 (우리 요청서 표시용 사본 · 4차 판정문과 바이트 동일한 사본).

## 우리 트리 재현 (Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · pandas 3.0.6)

묶음을 그대로 풀고 (`source/` = 우리 HEAD 라서 그 묶음을 돌리면 우리 트리를 돈 것이다) 실행기를 **무변경**으로 돌렸다.

| 실행 | rc | Codex 증거와 대조 |
|---|---|---|
| `verify_final_acquisition.py` | 0 | `final_integrity.json` 차이 0 (624 키 · ZIP 26 · 획득 207) |
| `probes/delivery_audit.py` | 0 | `delivery_independent.json` 차이 0 (190 키) · `reread_mutants.json` 차이 0 — **두 변조 모두 PASS · rc 0 이 우리 트리에서도 재현** (RGLR4-01 · 02) |
| `probes/execution_and_567.py` | 0 | `execution_and_567.json` 차이 0 (791 키 · worker 194 · `_judge_legacy` 194 SEALED_LEGACY · ⑤⑥⑦ 대조) |
| `probes/bulk_counterexample.py` | 0 | nz 40 의 G · q · T 만 상대 ~2.5e-12 (CG 수치) · T = 0.633 · 0.650 · 0.658 (< 1) 같음 |
| `run_tests.py lhs` · `lhs chain tau pipeline` | 0 · 0 | 326/326 · 19/19 · 55/55 · 284/284 (Codex 4 묶음 실행의 lhs 325/326 = 그쪽 부분 스냅샷의 옛 웹 템플릿 · 판정문 §2) |
| `run_probes.py` (옛 탐침 7) | 0 | 7/7 rc 0 · lw · vm · handover 둘 차이 0 · precision = 버전 문자열뿐 · raw18 = 출력 끝자리 상대 2.2e-11 (솔버 수치) · network = 시각 · run id · 합성 digest · 백업 파일 이름뿐 (판정 키 138 중 다른 것 = 그 이름을 담은 사유 문자열 1) |
| `source/` 에서 `../probes/new_probes_after_fix.py` | 0 | 경로 · 시각 · τ² 1 ULP · 곱셈 ↔ pow 비트 1 ↔ 0 (libm) — 4차 반입과 같은 부류 |

⇒ 판정에 쓰인 값 · 상태는 우리 트리에서 같다.  차이는 환경 (경로 · 시각 · 무작위 접미사 · 반복 솔버 수치 끝자리) 뿐이다.

## 한정

- 이 재현은 Codex 묶음의 실행기를 우리 트리에서 다시 돈 것이다 — 원 194 의 atoms · contacts 로 망을 다시 푼 것이 아니다 (판정문 §2 의 검증 한계 그대로).
- 숫자의 출처: `_reproduction_compare_linux.json`.

# SUP20-01 · SUP20-02 수정 — Codex 탐침 고친 트리 재실행 + 입력 지문 영수증 (컨테이너 범위) (2026-10-12)

- 기준 판정: `docs/reviews/codex_review_supp20_support_20261012.md` (리뷰 핀 `b429c3c1d` · **HOLD** · P2 `SUP20-01` 배포 대조의 배치 신원 두 벌 · P3 `SUP20-02` 원천 슬롯 열 사전 문구) ·
  수정 계획 `docs/reviews/sup20_fix_plan_20261012.md` (1저자 10-12 Q1–Q4 = (가) 권고대로).
- 고친 커밋: `4cae3a464` (SUP20-01 · 시험 V22) · `dd87e069c` (SUP20-02 · selftest ㉛j · ㉛j2) · `dfee89184` (입력 지문 영수증 `scripts/supp20_input_receipt.py`).
  재실행 트리 = `dfee89184` (깨끗한 트리 · 컨테이너 Linux · Python 3.11.15).
- 방법: 반입된 Codex 묶음 `docs/reviews/codex_supp20_support_review_evidence_20261012/` 의 `run_checks.py` · `probes/` 를 리포 밖 새 폴더에 복사 · 그 폴더의 source = 이 트리 (심볼릭 링크) ·
  `python3 -B run_checks.py design_probe release_probe` (탐침 **무변경**) → 반입 때 만든 대조기
  `docs/reviews/codex_supp20_support_review_evidence_20261012/_repro_ours_20261012/compare_probe_outputs.py` 로 Codex 증거와 평탄화 키별 대조 (`compare_fixed.json`).
  두 탐침 rc 0 (`run_checks_fixed.log` · `run_release_probe.json` · `run_design_probe.json`).

## 1. 결과 — Codex 탐침 (`release_probe.json` · `design_probe.json`)

| 탐침 칸 | Codex (핀 `b429c3c1d`) | 고친 트리 (`dfee89184`) |
|---|---|---|
| baseline_build · baseline_check (정상 214) | 생성 · 문제 0 | 같음 |
| normal_build_different_fp (다른 code_fp 보충 뿌리 build) | ReleaseError (교차 code_fp) | 같음 (메시지 안 합성 지문만 다름 — 아래) |
| **missing_cross_root** (사본 batches.supp20.root = 없는 경로) | **문제 0** | 문제 1 (사본 뿌리 ≠ 관문 뿌리) |
| **missing_supp_code_identity** | **문제 0** | 문제 1 (보충 배치 — code_identity 없음) |
| missing_primary_code_identity (대조) | 문제 1 | 문제 1 (같음) |
| **unauthorized_supp_code_change** (sealed_changed webapp/app.py · allowed []) | **문제 0** | 문제 1 (명시 승인 목록에 없다) |
| **different_fp_gate_original_cross_roots** (supp_batch 만 다른 유효 뿌리 증거로 교체) | **문제 0** | 문제 4 (사본 뿌리 · 교차 code_fp · cross_batch.code_fp · cross_batch.roots) |
| different_fp_gate_matching_cross_root (교체 + 사본도 교체) | 문제 2 | 문제 3 (+ cross_batch.roots) |
| **different_fp_gate_missing_cross_root** (교체 + 사본 없는 경로) | **문제 0** | 문제 4 |
| other_supp_gate (교체에 쓴 뿌리 자신의 관문 — 대조) | 문제 0 | 문제 0 |
| 판정문이 기존 경계로 남긴 칸 (§3 Q3 · §6 — 이번에 바꾸지 않음): 인계표 출처 열만 바꿈 · τ 출처 부록 check · 하중 99 (lhss · lhs) build · check | 문제 0 · 생성 | 같음 |
| changed_tau_provenance_build · restored_check | ReleaseError · 문제 0 | 같음 |
| design_probe `new_dictionary_claims` lhss_w_AM_P · lhss_w_AM_S | 옛 문구 ("AM_P 질량분율 — ps_frac = …") | 새 문구 (P · S 슬롯 · mono = 단일 AM 자리 · 비율 식은 bimodal 에만 · mono_AM_P → 1 · mono_AM_S → 0) |
| design_probe 나머지 (설계 800 칸 독립 재계산 · mono 반례 네 행 = 데이터 · 정의 교차 · 하중 빈칸 · r2 묶음 · 재적합) | — | 같음 (재적합 실수 끝자리 14 키 ≤ 1e-12) |

- 키별 대조 (`compare_fixed.json`): release 97 ↔ 104 키 · 같음 82 · 경로 문자열만 6 (임시 폴더) · Codex 에만 5 = 빈 목록이던 `returned` 칸 다섯 · 우리에만 12 = 그 칸들의 새 문제 ·
  판정값 문자열 차이 4 = 합성 교체 뿌리 지문 하나와 그 지문이 든 메시지 셋 — 탐침의 시험용 축소 봉인 지도에 `scripts/lhs_release_build.py` 의 sha256 을 싣는 구성이라
  그 파일을 고치면 지문이 바뀐다 (`3b0ef9f1…` → `60252564…` · 생산 지문 아님 · 판정은 같다 = build 거부).  design 914 키 · 같음 898 · 실수 14 · 판정값 차이 2 = 고친 문구 둘.
- 우리 시험: `scripts/test_lhs_release_v13.py` 고치기 전 239 PASS · 17 FAIL (V22 반례 17 오수용) → 256/256 · `scripts/lhs_release_build.py --selftest` 31/31 ·
  `scripts/lhs_design_dataset.py --selftest` 389/389 → 390/391 (㉛j 만 FAIL) → 391/391.

## 2. 입력 지문 영수증 — 컨테이너 범위 (`supp20_receipt_container.json`)

`python3 scripts/supp20_input_receipt.py --json docs/reviews/codex_sup20_fix_probe_rerun_20261012/supp20_receipt_container.json` (트리 `dfee89184` · 깨끗함) = **rc 0 · 11 칸 같음** —
R0 (등록 문서 §2 · §3 · README 값) · A1 (실행기 등록 표 = 등록 §2) · A2 (등록 집합 supp20 성립) · B1 (계획 = 등록 생산 집합) · B2 (후속 다시 읽기 = `--expect-set supp20`) ·
B3 (입력 지문 다시 계산 = 등록 §2 — 케이스 20 · ids `991cf115…` · raw 표 `a7aaa3c8…` · 원자료 결손 0 · 코호트 TSV `69d3f913…`) · C1 (r3 묶음 sha256 = README · harvest_head `1e09f661d…`) ·
C2 (반입 파일 = r3 묶음 바이트) · C3 (설계 · 어댑터 CSV sha256 = 등록 §2) · C4 (r2 ↔ r3 키별 대조 = README 끝) · D1 (봉인 32 code_fp `e8b2496b…` = 등록 §3).
⚠ **발사 승인이 아니다** — 발사 dry-run (`--dry-run-log`) · 실제 manifest (`--manifest` · `--primary-manifest`) 칸은 WSL 사전 점검에서 · 사전 점검 결과 · 저자 발사 승인 = 수동 칸.

## 3. 한정

- 합성 214 관문 시험이다 (τ 실제 원천 재독해 = 대역 — Codex 와 같은 한정 · check · 배치 관문 · 교차 = 대역 없음) — 생산 194 · 보충 20 · WSL dry-run · fast16 + real4 는 돌리지 않았다.
- `release_probe.json` 의 경로 문자열은 이 재실행의 임시 폴더 · 이 worktree 경로다.
- 봉인 32 무변경 (code_fp `e8b2496b…`) · 배포 도구 (`scripts/lhs_release_build.py`) · 인계 도구 (`scripts/lhs_design_dataset.py` = HANDOVER 파일) 지문은 바뀐다 (발사 manifest 에 기록).

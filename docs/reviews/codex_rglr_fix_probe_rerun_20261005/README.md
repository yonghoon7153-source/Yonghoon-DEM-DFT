# RGLR 수정 뒤 Codex 탐침 재실행 (2026-10-05 밤)

- 탐침 = Codex RGL 재검증 판정 묶음 (zip `04e45fe0-codex_rgl_reverify_review_20261005.zip` · sha256 `748ebabd5dbfaa1d8f38376525201c207db0e1cb1e8937f88f04b3e71d791cbf` ·
  반입 기록 `docs/reviews/codex_rgl_reverify_review_evidence_20261005/_README_reproduction.md`) 의 `docs/reviews/codex_rgl_reverify_review_evidence_20261005/probes/network_adversarial.py` · `docs/reviews/codex_rgl_reverify_review_evidence_20261005/probes/lw_replay.py` — **무변경**.
  단 두 파일 끝의 `assert` 는 **수정 전 결함 결과**를 단언한다 (예: `band_ratio_nan` 이 done) → `rglr_after.py` 가 AST 로 `assert` 를 **기록**으로 바꾼다 (`*.soft_asserts.json` · held true/false).
- 소스 = 우리 트리 — 탐침이 가리키는 `source/` 를 판정 묶음 매니페스트의 432 경로 + `scripts/*.py` · `webapp/*.py|json` 로 채운다.
- **전** = `fde4a812c` (재검증 반입 커밋 · 수정 전 생산 코드 = 판정 핀 `bf4fb6aee` 와 같은 blob) · **후** = 통합 트리 (`a6f950227` 위 `af9e6b15f` RGLR-03 · LHS-33 · `9fe8ba0bf` 194 인계 LW 제외 · `e03c0a84b` RGLR-01 · 02 · WEB-03).
- 재현 (Linux · 리포 뿌리): zip 을 풀고
  `CODEX_RGLR_PKG=<풀린 폴더> python3 docs/reviews/codex_rglr_fix_probe_rerun_20261005/rglr_after.py . <출력 폴더> new_network independent_lw`
  → `<출력>/evidence/network_adversarial.json` · `lw_replay.json` · `<출력>/probes/*.soft_asserts.json`.

## 망 — `new_network` (실 network CLI · 실 app helper · Stage E 는 탐침의 대역)

| 경우 | 전 (`fde4a812c`) | 후 | 판정문 |
|---|---|---|---|
| positive (L0 관통) | done · τ² 10.984918916215547 | done · τ² 10.984918916215547 | 양성 |
| no_through (정상 비관통) | done | done | 양성 |
| legitimate_band (정상 L1) | done | done | 양성 |
| solver_failed_stop | failed (정지 계약) | failed (망 솔버 내용 검증 — 한 단계 앞) | — |
| solver_failed_general | **done** | **failed** | Q1 · WEB-03 |
| ratio_times4 (무차원 σ 만 ×4) | **done** · τ² 2.7462297290538866 | **failed** | RGLR-02 |
| band_ratio_missing (L1 · σ_ratio None) | **done** | **failed** | RGLR-01 |
| band_ratio_nan | **done** | **failed** | RGLR-01 |
| band_ratio_negative | **done** | **failed** | RGLR-01 |
| band_fraction_above1 (관통 분율 2) | **done** | **failed** | RGLR-01 |
| rejected_retry_preserves_generation | failed · 옛 세대 동일 | failed · 옛 세대 동일 | 양성 (RGL-04) |
| write_failure_after_stamp (full_metrics 쓰기 OSError) | **EXCEPTION · 옛 세대 다름** (provenance ↔ full_metrics run id 섞임) | **failed · 옛 세대 동일** | Q2 · WEB-03 |

기록된 단언: 전 7/7 성립 (결함 재현) → 후 4/7 — 성립하지 않는 셋 = 결함 단언 (줄 75 ratio_times4 의 τ/4 · 76 band_nan · negative done · 77 write_failure EXCEPTION) ·
양성 단언 넷 (positive · no_through done · solver_failed_stop failed · retry 옛 세대 동일) 은 그대로 성립.

## LW — `independent_lw` (실 CSV → 실 `load_atoms_raw` → 실 `calc_love_weber_stress`)

| 경우 | 전 | 후 |
|---|---|---|
| normal | OK | OK |
| nan_plate · isolated_nan_radius | FAILED (invalid_input) | FAILED (invalid_input) |
| true_zero_load | UNDEFINED (zero_load) | UNDEFINED (zero_load) |
| false_zero_force | FAILED (force_columns) | FAILED (force_columns) |
| two_dimers_correct · swapped · finite_cstr | OK | OK |
| **nan_cstr_first** | **OK** (virial unavailable · 파서가 세 키를 안 씀) | **FAILED (invalid_input · 파서 c_strs 손상)** |
| **text_cstr_first** | **OK** | **FAILED (invalid_input)** |
| inf_cstr_first | FAILED (invalid_input) | FAILED (invalid_input) |
| finite_wrong_virial | FAILED (virial_mismatch 0.667) | FAILED (virial_mismatch 0.667) |
| **nan_hides_wrong_virial** | **OK** | **FAILED (invalid_input)** |
| all_cstr_absent (세 열 전무 · 옛 규약) | OK (unavailable) | OK (unavailable) |
| **partial_cstr_tuple** (직접 dict · sigma_xx 만 없음) | **OK** (unavailable) | **FAILED (invalid_input · 세 성분 일부 결측)** |

기록된 단언: 전 8/8 → 후 6/8 — 성립하지 않는 둘 = 결함 단언 (줄 46 nan_cstr_first OK · 48 nan_hides_wrong_virial OK).

## 한정 (Codex 와 같다)

- 합성 fixture · 소형 CLI 검산이다 — 운영 코퍼스에 이 손상이 있다는 증거가 아니다.
- 일반 경로 반례의 Stage E 는 탐침의 대역 — 실 Stage E 수치 재현이 아니다.
- 탐침 임시 폴더 (`band_*` · `lw_parser_*` 등) 는 반입하지 않았다 — 재실행이 다시 만든다.

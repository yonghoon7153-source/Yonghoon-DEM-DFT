# Codex 3차 재검증 탐침 — 고친 트리 재실행 (RGLR2-01 · 02 · 03 · 2026-10-05 밤)

- 기준 판정: `docs/reviews/codex_review_rglr_reverify_20261005.md` (핀 `dbe0f076d` · P2 셋 = `RGLR2-01` 일반 게시 경로 기술 검사 · `RGLR2-02` 되돌림 실패 표지 · `RGLR2-03` 옛 σ_VM clamp).
- 고친 커밋: `5d0f30984` (RGLR2-01 · 02) · `b2d8f80dc` (RGLR2-03 · 문턱 K = 2^20 = 1저자 *"권고하는대로 가"*).
- 방법: 판정 묶음 (`codex_rglr_reverify_review_20261005.zip`) 을 풀고 `source/` 를 고친 트리의 `git archive HEAD` 로 바꾼 뒤 `source/` 에서 실행.
  탐침 원본은 **결함이 있음을 단언**한다 (고친 트리에서는 AssertionError 가 정상) — 그래서 결함 단언만 수정 뒤 기대로 뒤집은 사본을 둔다.
  - `network_adversarial_after_fix.py` = Codex 탐침 network_adversarial.py (판정 묶음의 probes 폴더) 와 1–104 행 동일 · 105 행 (일반 경로 두 변이 `done` → `failed`) · 110 행 (`previous_generation_kept` True · `active_status` success → 그 반대) · 출력 파일 이름만 다름.
  - `vm_boundary_after_fix.py` = Codex 탐침 vm_boundary.py (판정 묶음의 probes 폴더) 의 `vm_cv == 100.0` 단언을 `|vm_cv| < 1e-6` (Python float · NumPy float64 둘 다) 로 · 출력 파일 이름만 다름.

## 결과 (Linux · Python 3.11 · rc 0)

| 사례 | 고치기 전 (Codex · 우리 재현) | 고친 뒤 |
|---|---|---|
| `general_ratio_times4` (RGLR2-01) | done (×4 게시) | **failed** (candidate_rejected · 승격 전 기록 검사) |
| `general_band_ratio_missing` (RGLR2-01) | done | **failed** |
| `rollback_destination_failure` (RGLR2-02) | failed · kept **True** · active **success** · 화면 "이전 성공 세대 그대로" | failed · `failure_kind` **rollback_failed** · kept **False** · active **invalid** (사유 = 중단된 게시 흔적 · full_metrics ↔ 도장 불일치) |
| 양성 `positive` · `no_through` · `legitimate_band` | done | done (그대로) |
| 나머지 실패 사례 (`solver_failed_*` · `ratio_times4` · `band_ratio_*` · `band_fraction_above1` · 재시도 보존 · 쓰기 실패 둘) | failed · 6 파일 보존 | 그대로 |
| VM 거의 정수압 쌍 (RGLR2-03) | vm_cv **100.0** · computed (계약 v2) | vm_cv **0.0** · vm_mean `1.0730991562013514e-07` (= 정확 VM) · computed · 계약 v3 · 다시 계산 1 (Python · NumPy) |
| VM 양성 대조 | CV 0.0 | 그대로 (다시 계산 0) |

- 한정: 탐침의 `grade_tau2` (되돌림 실패 사례 15.07) 는 탐침이 **가드 없이** full_metrics 를 직접 읽은 값이다 — 케이스 화면 · 등급 경로는 `_network_generation_guard` 로 None (시험 T22e).
- `wsl_smoke_prefix_05fbf15aa.md` = 1저자 WSL 소형 통합 시험 (고치기 전 코드 `05fbf15aa`) — 실데이터 검사 22/22 통과 · 음성 대조 C1 · C1b · C2 · C3 가 Codex 증상 그대로 FAIL (rc 2 = 고치기 전 정상).  고친 코드 재실행은 따로 기록한다.

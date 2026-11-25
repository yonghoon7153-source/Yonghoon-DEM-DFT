# 7:3 탈압 UB (368469) 회수 · 개발 판독 — 개발 자료

2026-11-25 · Codex 실무 창 사용 한도 (11-28 까지) → 1저자 *"codex 실무에서 하던거 여기서 해야될듯"* → 본 세션이 회수 · 판독.

| 항목 | 값 |
|---|---|
| 잡 | UB 368469 · COMPLETED 0:0 · 러너 rc 0 · 기술 영수증 일치 (`TECHNICAL_RECEIPT_MATCH`) |
| 회수 | ibb 현장 도구를 직접 부름 (WSL 실행 TXT 를 찾지 못함) · `collect_ps73.py` sha256 `65d7ef5f…` · `phase_controller.py` `4cbd94d5…` = 발사 핀 `2f4c42a3b205` 판과 같음 · 반환 ZIP sha256 `cdc24df72e41aad482955a83dc38f4bc6ff67baab3be3e85f9c34a19e6e14f3b` (리포 밖 · 저자 전용) |
| 요약 판독 | 같은 핀의 `local_summary.py` → `development_readback.json` (sha256 `15a5b0005c1435bf…`) · `PARTIAL_RETURN` |
| UB 1 MPa 회복률 ρ | **14.1197 %** · 괄호 14.0925 – 14.1375 % · `primary_status` OK · 궤적 `LIFT_CAP` · 자유 표면 높이 없음 |
| 원 감시기 | `HOLD_OR_RECONCILE` (05:14 UTC) — UB 끝난 뒤 UT 를 내려다 `state/jobs/UT` 가 이미 있어 멈춤 (UT 373358 은 11-24 병렬 블록으로 접수) = 설계대로 · 이중 제출 0 |
| 남은 팔 | UT 373358 · UVa 373686 진행 · UC 373359 = 11-25 수령 (`docs/reviews/ps73_uva_early_20261125/README.md`) |

- ρ = (h(1 MPa) − h₀)/h₀ (`docs/reviews/dem_unloading_ps45_prereg_20261009.md` 머리 용어).  **모델 안 개발 값 · 실험 대조 없음** (`validation_against_experiment` = NOT_ESTABLISHED) · 중력 자격 = GT1 · GT2 개정 대기.
- 다음 = UT 정상 종료 · 판독 → UB ↔ UT 유효 끝점 차 ≤ 0.10 %p 이면 UVa = 속도 대조 · 넘으면 보조 (`docs/reviews/ps73_stagewise_20261123/README.md`).

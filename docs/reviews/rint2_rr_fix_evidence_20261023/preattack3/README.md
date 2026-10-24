# 사전 공격 리뷰 3 회차 — Q9 설계 개정 2 (Rint ② RR · 2026-10-24)

- 보고 = `PREATTACK_Q9R2.md` (옮겨 적음 머리 · 메인 메모 = 맨 끝 절) · 탐침 = `probes/` · 출력 = `logs/`.
- 대상 = `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` 개정 2 (`9a72d65c6`) · 비교 기준 개정 1 (`919906a3e`) · 문서만.
- 결론 = P1 0 · P2 5 · P3 15 · 질문 6 · 개정 1 발견 7 = 닫힘 3 · 부분 4.
- 처분 = 1저자 10-24 *"권고대로 해"* — 개정 3 (P2 다섯 + 질문 6 결정 · 문서만) 뒤 Codex 회차 ① 요청서 (메인 메모).
- 다시 돌리기: 트리 = `git archive 9a72d65c6 scripts docs/reviews/rint2_rr_fix_evidence_20261023` 를 푼 폴더 →
  `OPENBLAS_NUM_THREADS=1 nice -n 19 python3 -I probes/<탐침>.py <트리>/scripts [<이 폴더>/probes]`.

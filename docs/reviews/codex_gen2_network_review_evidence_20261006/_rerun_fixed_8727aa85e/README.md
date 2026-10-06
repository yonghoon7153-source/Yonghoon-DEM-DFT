# 고친 트리 재실행 (8727aa85e · 2026-10-06 밤)

Codex 판정 `docs/reviews/codex_review_gen2_network_20261006.md` 의 probes 를 **무변경**으로 고친 트리에서 다시 돌린 출력이다
(`source/` = `git archive 8727aa85e scripts webapp docs/data/real14_reference_20260928 docs/data/case15_corner_20261001 docs/data/gen2_design_20261006`).
고친 커밋: 계약 `05c60ae2d` (G2R-01 · 02) · 증서 · 사다리 · GEN2-01 `05977e94a` · 통합 `5627a74a6` (증서 → 계약 · G2R-04 문구).

| probe | 우리 트리 (7a5976602 · 고치기 전) | 고친 트리 (8727aa85e) |
|---|---|---|
| `publication.py` | 다섯 다 `done (True, 'ok')` · h12_as_primary σ 0.00513502 | baseline 만 `done (True, 'ok')` · h12_as_primary · bad_psi · bad_electrode · partial_missing_g2 = **`failed (False, …)` — 게시 전 거부** (후보가 활성 세대가 되지 않아 정지 판정은 "모드 파일 없음" 으로 읽힌다 · 거부 사유 = 세대 계약은 `webapp/test_gen2_publication_handover.py` ①c 가 실 생산자 사슬로 확인) |
| `handover.py` | 다섯 단독 + 섞음 둘 전부 인계 통과 | baseline 통과 · 변이 넷은 **게시되지 않아 run id 가 없다** → probe 가 `KeyError: 'network_run_id'` 로 멈춘다 (probe 의 가정 = 게시 성공).  강제로 디스크에 둔 변이 폴더의 인계 거부 = `webapp/test_gen2_publication_handover.py` · `scripts/test_gen2_role_contract.py` |
| `adversarial.py` | CG 막다른 간선 1e14 → G 30001 (참 15000.5) · zero_Rc → 0.1 S computed | zero_Rc 가 **G = None (not_computed · zero_resistance_requires_contraction)** 이라 probe 의 `G/1.1` 산술이 TypeError (probe 가정 = 숫자) |
| `adversarial_none_ok.py` (위 probe 에서 `rel_error` 한 줄만 None 허용 — 이 폴더에 사본) | — | CG 막다른 간선 다섯 대비 전부 **15000.5** (1e14 = `spsolve_fallback` · 나머지 `cg`) · zero_Rc = not_computed (사유 zero_resistance_requires_contraction) |

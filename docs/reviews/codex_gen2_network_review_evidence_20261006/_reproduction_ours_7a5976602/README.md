# 우리 트리 재현 (7a5976602 · 2026-10-06 밤)

Codex 판정 `docs/reviews/codex_review_gen2_network_20261006.md` 의 반례 probes 를 **무변경**으로 우리 트리에서 다시 돌린 출력이다.
`source/` = `git archive 7a5976602 scripts webapp docs/data/real14_reference_20260928 docs/data/case15_corner_20261001 docs/data/gen2_design_20261006`
(핀 c13da95a3 + 3B 피복 · 3A 인계 관문 커밋 — 망 · τ · 게시 코드는 핀과 같다).

| probe | 결과 (우리 트리) | Codex 판정문 |
|---|---|---|
| `adversarial.py` | CG 막다른 간선 다섯째 대비 G 30001.0 vs 참 15000.5 (+100 %) · zero_Rc G 0.1 vs 수축 1.1 (−90.9 %) · 세대 오타 · 결손이 정지 ⑨ 와 섞음 검사를 빠져나감 | G2R-03 · GEN2-01 · G2R-02 같은 값 |
| `publication.py` | baseline · h12_as_primary · bad_psi · bad_electrode · partial_missing_g2 다섯 다 `done (True, 'ok')` · h12_as_primary σ 0.00513502 (baseline 0.00400538) | G2R-01 · G2R-02 같은 값 |
| `handover.py` | 다섯 단독 + [baseline, h12_as_primary] · [baseline, bad_psi] 전부 인계 통과 (True) | 같은 판정 |

`publication.py` · `handover.py` 는 웹앱 의존 (requests) 때문에 `python3 -I` 가 아니라 `python3` 로 돌렸다 (probes 폴더에는 probe 6 개뿐).

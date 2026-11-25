# 여기 있는 그림은 **배포 경로에서 내린 것**이다 (지우지는 않는다)

틀린 그림도 "무엇이 왜 틀렸나"의 증거라 파일은 남긴다. 다만 `docs/figures/<계>/` 는
배포 경로라 거기 있으면 인용된다 — 그래서 이 폴더로 옮기고 이름에 `RETRACTED_` 를 붙인다.

| 파일 | 언제·어디서 왔나 | 왜 내렸나 |
|---|---|---|
| `RETRACTED_cascade_conc_trends_2026_06_15.png` | `tools/figures/plot_cascade3.py` (2026-06-15, 옛 저장 경로 `docs/figures/cascade/cascade_conc_trends.png`) | **존재하지 않는 농도축**으로 그렸다. `x002/x005/x010` 은 x=0.02/0.05/0.10 이 아니라 **전부 x=0.25 인 배치 반복(placement replicate)** 이다 — 슈퍼셀 버그. 근거: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:350,409,656` · 같은 폴더 `tools/figures/plot_cascade_v23.py:12-14` 가 그 사실을 스스로 적어 놨다. 세 패널 전부 해당. |

농도 응답이 필요하면 `dualx_v23`(actual_x 0.0625 / 0.25 실측)로 다시 그린다.
스크립트(`plot_cascade3.py`)는 철회 배너를 달고 남아 있다 — 실행하면 이 폴더로만 저장된다.

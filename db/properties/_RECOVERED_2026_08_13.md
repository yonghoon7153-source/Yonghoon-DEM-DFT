# 2026-08-13 회수분 — 출처 기록

이 파일들은 `/data/work/repo` (브랜치 `claude/configure-spawn-halogen-lithium-TjDCB`,
마지막 커밋 2026-06-29, **원격 미푸시**) 에서 회수했다. 그 브랜치가 6/29 에 버려지면서
정본으로 흘러오지 못한 산출물이다. 미푸시 커밋은
`/data/work/cascade_registration_2026_06_29.bundle` (399 MB) 로 보존.

| 파일 | 원 위치 | 계산일 | 비고 |
|---|---|---|---|
| `oxidation_stability_cascade.json` | repo/db/properties | 2026-06-25 | **분해 반응식 포함** (기존 .csv 2.8 KB 는 숫자 4개만 남긴 축약본) |
| `oxidation_stability_cascade_v2.json` | 동 | 2026-08-13 | 90종 270 champion 회수 재계산. 옛 141건과 ox_V 차이 0 |
| `cascade_v23_all.csv` | 동 | 2026-08-13 | = `unified_dataset_273.csv` (90종 3615행) |
| `cascade_v23_all_20260629_47species.csv` | 동 git object | 2026-06-29 | 옛 47종 판 (2025행). 풀의 정의였던 파일 |
| `doping_cascade.json` | 동 | 2026-06-29 | `_verified`/`_trivalent_M3` 의 원본 |
| `esw_lpscl_{hull,profile}.json` · `esw_comp1_mp.json` · `esw_lis4excluded.json` | repo 루트 | 2026-06 | host ESW 분석 |
| `constrained_esw_{results,cl_scan,cl_scan_relax,cl_scan_hybrid}.json` | repo 루트 | 2026-06-09 | 해설 문서는 `docs/oxidation/constrained_esw_*.md` 로 이미 있었는데 **데이터만 없었다** |
| `interface_reactivity_results.json` | repo 루트 | 2026-06 | |
| `tools/oxidation/{esw_nd_doped,interface_reactivity_nd,sei_product_gaps}.json` | 동 | 2026-06 | |

⚠ 값 검증은 아직 안 했다. 회수 = 등록이지 승인이 아니다.
근거: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md`

# 이종기술 코팅 프리셋 (webapp v3, #33)

litdb 적용표 B-2위: 코팅(이종기술)이 현재 **3경로로 흩어져** 있음 → 통합 "코팅 프리셋 셀렉터".
frame[5]: **코팅 = 화학 CEI 축**(Stage-E 기계 coverage와 별개).

## 통합된 3경로
| 경로 | 위치 | 프리셋 필드 |
|---|---|---|
| (a) 화학 CEI 억제 | STEP5 `b1_chem_fade --chem-x` | `cei_suppress`, `r_ct_factor` |
| (b) 계면 전도 | Stage-E/STEP3 (Han2025 t/σ_b) | `sigma_ion_mod`, `sigma_e_mod` |
| (c) 구조 seeding | STEP2 `additives.seed_*` | `seed_morph` (shell/coat/sheath) |

## `scripts/coating_presets.py` (기본 OFF = none)

프리셋 표 (★크기=앵커, shape=√N ASSUMED, 앵커 없으면 None=스윕전용·날조금지):

| coating | cei_suppress | r_ct× | σ_ion× | σ_e× | morph | 앵커 |
|---|---|---|---|---|---|---|
| none | 1.0 | 1.0 | 1.0 | 1.0 | — | baseline |
| **LNO** | 15 | 0.05 | 1.0 | 1.0 | shell | Kim2025 R_ct 20×·CEI 13–20× / Payandeh 93%@200 |
| **LZO** | 8 | 1/6 | 1.0 | 1.0 | shell | Kang&Shin 6–8nm (배수=LNO 하한 보수) |
| Li₃PO₄ | None | None | 1.0 | 1.0 | shell | ⛔ 정량앵커 없음 → 스윕전용 |
| carbon | 1.0 | None | 1.0 | None | shell | Reisacher p_c 4wt%·So2022 (CEI 억제 아님; 열화=#30 촉매) |
| SDCP | None | None | 0.80 | 5.1 | coat | A4′ (σ_e×5.1·σ_ion×0.80·E23.6) |
| SWCNT | None | None | 1.0 | None | sheath | A14 (seed_sheath sid8) |

`coated_chem_x(coating, bare_chem_x)` = 1 + (bare−1)/cei_suppress (증분만 억제).  앵커 없으면 bare 유지.

**추가 API (앵커-안전):**
- `coated_rint0(coating, rint0, rct_frac)` — 계면 R_ct 억제(r_ct_factor, LNO 1/20)를 pristine R_int0에.
  ★R_ct는 R_int **한 성분** → 성분 분율(rct_frac, EIS-TLM 앵커)을 **줄 때만** 적용, 미상=미적용(날조금지).
  R_int0_coated = R_int0·[(1−f)+f·r_ct_factor].
- `coating_effect(coating, bare_chem_x)` — 코팅 전체 효과 1-dict(webapp 단일소스): chem_x(앵커 계산)·
  r_ct/σ_mod(앵커 계수, 적용은 성분분율/STEP3 필요)·anchor·note.

## STEP5 배선 (`b1_chem_fade --coating`)
`--coating LNO --chem-x 1.30`(bare) → 화학성장 1.30 → **1.02** (CEI 15× 억제).  검증(6.1× 총성장,
ledger 1.1): 화학몫 5.9% → **0.4%**.  selftest 8/8(coating) + b1 20/20.

## ★ 정직 규약 (중요 — 오용 방지)
- **코팅은 화학 *채널*만 억제** — 총 R_int 끝점(`rint_exp_x`)은 **별도 실험 입력**.  코팅셀 예측 시
  그 셀의 (낮은) 측정 끝점을 넣어야 함.  bare 끝점(6.1×)에 코팅을 걸면 억제된 화학몫이 **OTHER로 이동**
  (= "코팅이 화학을 15× 줄였는데 총이 6.1× 그대로면 나머지는 비-화학 OTHER" = 유용한 진단, 날조 아님).
- **크기만 앵커, shape(√N)는 ASSUMED** — `fit_rint_curve.py`가 ≥4 N점 실측으로 게이트.
- **앵커 없는 프리셋(Li₃PO₄/SDCP/SWCNT/carbon-σ)은 chem_x 미변경**(스윕 전용) — 화학억제 배수를 날조하지 않음.

## 잔여 (v3 후속)
- **webapp /step5 코팅 셀렉터 UI** (드롭다운 + /api/step5/fade coating 파라미터) = 즉시 후속.
- (b) 계면전도 `--coat-sigma-b`·(c) So2022 core-shell `# A4 HOOK` 구조 seeding = GPU/STEP3 후속.
- LZO 배수·Li₃PO₄ 앵커 = 신규 digitize 대기.

# 📚 LITDB — DEM+MPM ASSB 압밀·전달 문헌 인덱스

> 갱신: 2026-06-23. 각 논문 상세는 `papers/<slug>.md` (digest), 우리 대비는 `comparison_vs_ours.md`,
> 기준값은 `our_dem_baseline.md`. 수치 CSV는 `docs/data/<slug>_*.csv`.

Status 범례: ✅ digest 완료 · ⬜ PDF만(미digest) · 📄 메타만

## DEM/MPM 압밀 · 전달 (composite ASSB)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Bazzoun 2026** | J. Power Sources 661, 238682 | **LPSCl + NMC811** | DEM+FEM+RNM σ_eff,ion; 실험 0.137/0.101/0.065 mS/cm @f_CAM 70/75/80; RNM=Holm/Kirchhoff; E_SE=22.1 | DEM+FEM+RNM | ✅ | `bazzoun2026_dem_fem_rnm_ionic` |
| **Varkey 2026** | Adv. Powder Tech. 37, 105338 | halide Li₃YBrCl₆ + NMC811 | multi-contact 탄소성 DEM; separator floor 21% / cathode 37% @350MPa; E_SE=10.58; CONTACT-소성만(구) | DEM | ✅ | `varkey2026_multicontact_elastoplastic_dem` |
| So 2021 | J. Power Sources | (sulfide) ASSB | DEM mold-pressure cold-pressing | DEM | ⬜ | — |
| Martin & Bouvard 2003 | Acta Mater. | composite powders | DEM cold compaction of composite powders | DEM | ⬜ | — |
| Bouvard 2000 | Powder Tech. | hard+soft mix | densification of hard & soft powder mixtures | exp/theory | ⬜ | — |

## 패킹 기하 (geometric packing — Furnas dip 근거)

| 논문 (제1저자 년) | 저널 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|
| McGeary 1961 | J. Am. Ceram. Soc. | mechanical packing of spherical particles (bimodal 패킹 한계) | exp | ⬜ | — |

## 통합된 기존 노트 (→ papers/ digest로 흡수)
- `docs/lit_varkey2026_multicontact_dem.md` (한국어 노트) → `papers/varkey2026_*` ✅ + `docs/data/{densification_porosity_db,varkey2026_ionic_vs_pressure}.csv`
- `docs/lit_bazzoun2026_dem_fem_rnm.md` (한국어 노트) → `papers/bazzoun2026_*` ✅ + `docs/data/bazzoun2026_sigma_ionic.csv`
- `docs/literature_coverage/` json DB: contact_mechanics_db, coverage_db, packing_regime_db (수치 참조용 유지)

## 다음에 먹일 후보 (PDF 있음, 미digest)
So2021 / Martin-Bouvard2003 / Bouvard2000 / McGeary1961 — "논문 에이전트 실행해줘"로 순차 digest.

# B₂O₃-doped 챔피언 — Voronoi 부피 disorder 분석 (slide 9/17의 b2o3 판)

**날짜** 2026-07-02 · **구조** `db/structures/b2o3_relaxV0.cif` (DFT V₀, 128 atom) · **방법** scipy Voronoi (3×3×3 PBC 복제 + ConvexHull 부피), pymatgen 불필요
**데이터** `db/properties/b2o3_voronoi_disorder.csv` · **그림** `docs/figures/cascade/b2o3_voronoi_disorder.png` · **툴** `tools/comp1_v3/voronoi_volume_disorder.py`

> **한 줄.** per-atom Voronoi 부피의 **표준편차 = site-disorder 지표**. **B₂O₃ 도핑이 모든 골격 종의 disorder를 올림**(P 0.37→**1.47** ×4[O@PS₄→PS₃O], Cl 0.74→**1.63**, Li 1.15→**1.71**, S 2.05→**2.62**) + 새 도판트 **B(mean 12.7)·O(16.2)** = 작고 단단. "disorder↑ → 전도↑" 서사와 정합.

## 검증 (방법 신뢰성)
- **modelc(LPSCl1.6) 재현이 슬라이드와 정확 일치**: std P 0.370/Cl 0.736/Li 1.150/S 2.047 = 슬라이드 9 (0.37/0.74/1.15/2.05). Cl mean 20.31 = 슬라이드 17. → 방법 검증됨.
- `sum(Voronoi) == cell V` 정확(2436.3 ų) = 테셀레이션 완전.
- ⚠ comp1(LPSCl) 구조(`comp1_V0_k444`)는 Li/S std가 슬라이드(0.21/3.41)와 다름(내 1.61/2.75) — 슬라이드 LPSCl은 더 ordered한 셀. b2o3 비교엔 무관(b2o3↔modelc 둘 다 일관 계산).

## 결과 (b2o3 vs modelc)
| 종 | modelc std | **b2o3 std** | 배수 | mean(modelc→b2o3) |
|---|---|---|---|---|
| P | 0.37 | **1.47** | ×4.0 | 13.99→13.14 |
| Cl | 0.74 | **1.63** | ×2.2 | 20.31→20.77 |
| Li | 1.15 | **1.71** | ×1.5 | 20.51→20.00 |
| S | 2.05 | **2.62** | ×1.3 | 19.55→18.66 |
| **B** | — | **1.06** | NEW | 12.65 (작은 BS₃) |
| **O** | — | **1.19** | NEW | 16.18 (단단 O²⁻) |

## 해석
- **P disorder ×4**가 가장 큼: O가 PS₄ 일부를 PS₃O로 바꿔 P 국소환경을 크게 흔듦(결합길이 P–O 1.556 지문과 정합).
- **B(12.7)·O(16.2) mean 부피가 S(18.7)보다 작음** = 작고 hard한 도판트 → 국소 자유부피 축소 + 주변 격자 변형(→ 이웃 disorder↑).
- 전 종 disorder 상승은 **결합길이 노트의 4d Cl anti-site 25%(>modelc 10%)** 와 같은 그림 = **site-disorder 강화**. Minafra/Kraft "disorder가 Ea 낮춤" 서사와 방향 일치(단, MD는 b2o3=modelc 동일 Ea, 이득은 D₀).

## 연결
- `b2o3_bond_lengths_2026_06_29.md`(BS₃·P–O 지문, 4a/4d Cl), `b2o3_phonon_stability_2026_06_30.md`(soft 격자), `b2o3_vs_lpscl16_md_2026_07_02.md`(disorder↔전도).
- 남은 b2o3 분석: ICOHP(LOBSTER), ELF(kgy 진행중), CDD, ε∞(kgy 진행중). (Voronoi = 이번 완료)

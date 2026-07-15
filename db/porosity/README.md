# 건식 Bimodal 복합양극 Porosity — 실험값 (★ Furnas dip)

> 데이터: `bimodal_porosity_dry_raw.csv` (개별 펠렛), `bimodal_porosity_dry_summary.csv` (구성별 평균±표준편차)
> 측정: 건식 복합양극 펠렛의 기하 부피 vs 진밀도 기반 고체 부피로 porosity 산출.

## 산출식
```
porosity = 1 − (고체 부피 합 / 전체 부피)
전체 부피 = 면적 × 높이,  면적 = 0.8494864768 cm² (≈ ⌀10.4 mm)
고체 부피 합 = Σ (성분 질량 / 성분 진밀도)
진밀도(g/cm³): NCM(P,S) 4.8 · LPSCl(SE) 2.0 · VGCF 2.1 · PTFE 2.2
조성: AM:SE:VGCF:PTFE = 80:18:1:1  (P=대립 다결정, S=소립 단결정)
```

## 결과 (구성별 평균)
| P:S 구성 | n | porosity 평균 | 표준편차 |
|---|---|---|---|
| **S only (0:10)** | 6 | **23.9 %** | 3.7 % |
| 3:7 | 5 | 21.2 % | 3.4 % |
| 5:5 | 4 | 20.2 % | 2.5 % |
| **7:3 (최소)** | 5 | **19.7 %** | 3.1 % |
| **P only (10:0)** | 5 | **25.3 %** | 1.8 % |

## 핵심 해석
- **Bimodal Furnas dip 실험 확증.** 순수 단결정(S only, 23.9%)·순수 다결정(P only, 25.3%)보다
  **혼합(bimodal)에서 porosity가 낮아지고, 7:3(대립:소립=7:3)에서 최소 19.7%**.
  소립(단결정)이 대립(다결정) 간극을 채우는 geometric packing 효과.
- **방향성:** porosity 최소화(=catholyte 연속성·전달 최적, 에너지밀도↑) 관점에서 **P:S ≈ 7:3 부근이 최적 packing**.
  단, 대립(Poly) 비율↑ → grain boundary 저항·입자내 확산 저항↑ (연차보고서 모델). 따라서
  **packing 최적(7:3) ↔ 입자내 전달 최적(소립↑)** 사이의 trade-off → 2차년도 설계 최적점 탐색 대상.
- 연차보고서 모델은 "대립 비율↑ → 기공↑"로 기술(단조 증가). **그러나 실험은 bimodal dip을 보임**
  → 모델의 packing 가정 보정 필요 (`docs/project/05_ISSUES_AND_FIXES.md` #8).

## DEM 브랜치 연계
- DEM/MPM 브랜치(`claude/stoic-knuth-NObVQ`)의 bimodal packing 문헌과 직접 대응:
  - `litdb/papers/mcgeary1961_bimodal_sphere_packing.md` (강체 구 bimodal 충전, Furnas dip 원전)
  - `litdb/papers/bouvard2000_hard_soft_powder_densification.md` (SE+AM dip)
  - DEM v4 porosity-vs-AM% dip (CLAUDE.md [3])
- **이 실험 dip(7:3 최소, 19.7%)은 DEM bimodal porosity 예측의 실험 앵커로 사용 가능.**
  DEM은 무차원 packing(크기비·부피분율)을 주고, 실험은 절대 porosity를 줌 → cross-validation.
- 비교: Doux2020 LPSCl 펠렛 18 %@370 MPa(강체구 floor), Minnmann2021 복합 14 %@380 MPa.
  본 건식 복합양극(19.7–25.3 %)은 제작압·도전재/바인더 포함 조건이 달라 절대값 직접비교는 주의.

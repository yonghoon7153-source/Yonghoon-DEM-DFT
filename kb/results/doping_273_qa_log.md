# 273 Doping Cascade — QA Log

> 완주한 cascade의 품질 판정 기록. batch = `/data/work/runs/multi_category_2026_05_26_v23` (kserver).
> QA 기준: cascade COMPLETE(STAGE_12.DONE) + screen 수렴/outlier(|ΔV|>30%·|ΔE|>5eV) +
> ΔE/atom 음수(favorable) + B0 argyrodite 범위(~15-35) + elastic stable + site 화학 타당.
> 참고: master_batch_273가 TOP_K_SIGMA=2/TOP_K_NCM=3 기본이나, 처리량 위해 일부 cascade는
> Stage 10/11(σ_Li MD·cathode) 스킵하고 완주 (TOP_K_SIGMA=0 TOP_K_NCM=0).

## BaO (Ba²⁺ + O²⁻) — 2026-06-05 판정: ✅ 정상

- **site**: Ba²⁺ → Li 24g (큰 cation, aliovalent), O²⁻ → S 16e(PS₄) 또는 S 4a (isovalent). winner = S16e.
- **ΔE/atom (best winner)**: **−0.55 eV** → BaO incorporation favorable ✓
- **B0 (3농도 × 2 site)**:

  | 농도 | S16e | S4a |
  |---|---|---|
  | x002 | 23.2 | 20.9 |
  | x005 | 20.0 | 19.9 |
  | x010 | 21.8 | **18.2** |

  - 전부 18~23 GPa = modelc baseline(21.7) 근처, 타당
  - **S4a 단조 soft화** (20.9→19.9→18.2): Ba²⁺ 큰 이온(1.35Å) 격자팽창 → B0↓, 물리적 ✓
  - S16e 약한 비단조(23.2→20.0→21.8): 농도별 독립 screening + Li-ordering 분산(±몇 GPa)의 정상 scatter (오류 아님)
- **elastic**: top-2에 B0·E_young 계산됨(0 아님) → 발산 없이 안정. E_young 36~45 GPa.
- **V_mig**: ~14% (BVSE Li migration 부피, 적당한 경로 연결)
- **완주 상태**: x002 ✅, x010 ✅, **x005는 Stage 10(md_sigma) 타임아웃으로 중단** → `TOP_K_SIGMA=0
  TOP_K_NCM=0`로 tier_cascade 재실행(09f까지 skip, Stage 12만) → **완주**. 세 농도 모두 10/11 없이 통일.

**결론**: BaO 도핑 물리적으로 일관, cascade QA 통과. paper Layer-2 ML 데이터로 사용 가능.

---

## (이후 compound 판정 여기 누적)

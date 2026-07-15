# 실험 데이터베이스 (데이터 사전)

> 건식 후막 bimodal 전고체 복합양극 실험 데이터. 출처는 `../docs/project/sources/`.
> 명명: **No.1=NCM_2(매끈), No.2=NCM_3(satellite), Poly=대립 다결정**. P=Poly, S=Single.

## 폴더
| 경로 | 내용 |
|---|---|
| `materials/` | CAM(양극활물질), SE(고체전해질), 복합양극 조성 |
| `electrochemistry/` | formation, PTFE별 전도도, 건식셀 용량, 율속, bimodal 블렌드, 임피던스 TLM |
| `porosity/` | ★ bimodal 건식 porosity 실험값 (Furnas dip) |
| `loading/` | 디스크별·면용량별 로딩 계산 |
| `model/` | P2D/전기화학-기계 모델 파라미터 |
| `sem/` | SEM 이미지 카탈로그 |

## 파일별 핵심
| 파일 | 핵심 |
|---|---|
| `materials/cathode_active_materials.csv` | No.1/No.2/Poly/(NCM_1) 조성·입도·비용량·진밀도 |
| `materials/solid_electrolyte.csv` | LPSCl ~1µm, σ_ion 2.0 mS/cm |
| `materials/composite_recipe.csv` | AM:SE:VGCF:PTFE = 80:18:1:1, 진밀도 |
| `electrochemistry/formation_coincell.csv` | half-cell: No.1 DC205.9/91.5%, No.2 DC213/89.8% |
| `electrochemistry/ptfe_conductivity.csv` | σ_ion 0.062/0.057/0.019 (PTFE 0.5/1/2%), σ_e 0.04–0.05 |
| `electrochemistry/capacity_drycell_0p1C.csv` | 건식 ASSB 0.1C 용량 (PTFE별) |
| `electrochemistry/rate_capability.csv` | 1C: No.1 150 > No.2 135 mAh/g |
| `electrochemistry/bimodal_blends.csv` | P:S별 가중 비용량 200–205.9 |
| `electrochemistry/impedance_tlm.csv` | Rion/Rint: No.1 0.61/4.42, No.2 0.87/23.37 Ω·cm² |
| `porosity/bimodal_porosity_dry_*.csv` | ★ S only 23.9 → 7:3 19.7(최소) → P only 25.3 % |
| `loading/loading_table.csv` | 13pi/10pi, 3.2 & 6 mAh/cm² 로딩 |
| `model/p2d_parameters.csv` | i0, D_Li, σ, E, 압력, 설계변수 레벨 |

## 단위 규약
- 전도도 σ: **mS/cm** (= mS·cm⁻¹). ⚠ 킥오프 원본의 "mS cm⁻²" 표기는 오타 (→ `../docs/project/05_ISSUES_AND_FIXES.md`).
- 비용량 mAh/g, 면용량 mAh/cm², 로딩 mg/cm², 압력 MPa, 저항 Ω 또는 Ω·cm².

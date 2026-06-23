<!-- digest 표준 양식. 복사해서 papers/<slug>.md 로. ★ = 사용자가 특히 원한 항목 -->
# <제목> — <제1저자> (<저널> <년>)

> slug `<slug>` · DOI `<doi>` · type `DEM|MPM|FEM|RNM|continuum|exp|mixed` · PDF `<파일명>.pdf` · digested `<날짜>` · status ✅

## 1. 한 줄 요약
<핵심 메시지 1–2문장 (무엇을·왜 중요한가)>

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
|  |  |  |  |  |

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| porosity / 상대밀도 |  | @P |  |  |
| σ_ionic |  | @P, 조성 |  |  |
| σ_electronic |  |  |  |  |
| σ_thermal |  |  |  |  |
| coverage / 접촉면적% |  |  |  |  |
| coordination Z |  |  |  |  |
| E_SE / σ_y / ν |  | 소재 |  |  |
| Heckel P_y / knee |  |  |  |  |
| PSD (D10/D50/D90) |  | SE / CAM |  |  |

## 4. 시뮬레이션 방법 ★
- **code / version** (LIGGGHTS / Rocky / LAMMPS / Taichi-MPM / COMSOL / in-house):
- **DEM 접촉법칙** (Hertz / Thornton–Ning / EEPA / hooke-hysteresis / multi-contact) + 항복·제하:
- **재료 파라미터**: E_SE, E_CAM, ν, 마찰 μ, COR, σ_y, 경화:
- **bond/binder 모델** (SBR/CB/PTFE, 강성·반경):
- **MPM/continuum** (있으면): 구성식 J2/DPC/cap, grid/dx, readout(wallP/σzz), protocol(servo/hold):
- **전달 솔버** (있으면): RNM/Kirchhoff, 접촉저항 R=1/(2σr_c), FEM continuum, σ 정규화:
- **입자 처리** ★ (DEM판 "무질서 처리"): 구 vs 형상; mono/bi/poly-PSD; **rigid vs CONTACT-소성 vs
  진짜 SHAPE-소성** (어느 쪽인지 명시 — δ-overlap 프록시 ≠ 흐름):
- **도메인/RVE / servo / seeds / 압력범위**:
- **특이사항/튜닝**:

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 |  |  |
| 2 |  |  |

## 6. Post-processing ★
- **무엇** (Heckel fit / percolation / coordination / coverage(Hertz·Tabor) / tortuosity / porosity
  convention(union vs sphere-sum) / EIS-TLM / 네트워크 지표 θ·Z·R̄ …):
- **도구** (pymatgen / OVITO / 자체 스크립트 / RELAXIS / COMSOL …):
- **수치화·플롯·기록 방식**:

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 (rigid·plastic / halide·LPSCl / 2D·3D / mean-field·continuum) |
|---|---|---|---|
|  |  |  |  |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ①
- ②

## 9. 인용 가능 문장 (deck/paper용)
- "<defensible 1-liner>"

## 10. 주의/한계 (over-claim 방지)
- <rigid-sphere? CONTACT-plasticity만? halide라 절대값 전이 불가? 2D? 단일압력? digitized?>

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

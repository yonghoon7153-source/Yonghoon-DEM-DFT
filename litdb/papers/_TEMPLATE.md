<!-- digest 표준 양식. 복사해서 papers/<slug>.md 로. ★ = 사용자가 특히 원한 항목 -->
# <제목> — <제1저자> (<저널> <년>)

> slug `<slug>` · DOI `<doi>` · type `exp|DFT|AIMD|MLIP|mixed` · PDF `<upload-id>.pdf` · digested `<날짜>` · status ✅

## 1. 한 줄 요약
<핵심 메시지 1–2문장 (무엇을·왜 중요한가)>

## 2. 메타
| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
|  |  |  |  |  |

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| 이온전도도 σ |  | RT / T |  |
| 활성화E Ea |  |  |  |
| 산화 onset / ESW |  |  |  |
| 기계적 (E/B/G, C_ij) |  |  |  |
| 전자구조 (gap, VBM/CBM) |  | functional |  |

## 4. DFT/계산 방법 ★
- **code / version**:
- **functional** (PBE/PBEsol/SCAN/HSE06) + **vdW**(D3?):
- **pseudo / PAW**:
- **k-points / ecut(wfc,rho) / supercell / nat**:
- **DFT+U** (원소·값):
- **AIMD**: ensemble, T, time/step, thermostat
- **MLIP**: model, training set
- **무질서 처리**: SQS / enumerate / 단일 배열 / 실험 점유 decorate
- **특이사항/튜닝**:

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 |  |  |
| 2 |  |  |

## 6. Post-processing ★
- **무엇** (BVSE / NEB / Bader / COHP-ICOHP / DOS-PDOS / grand-potential ESW / ELF …):
- **도구** (pymatgen / VESTA / LOBSTER / VASPKIT …):
- **수치화·플롯·기록 방식**:

## 7. 우리 DFT 대비 (comp1 / modelc)  →  `our_dft_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
|  |  |  |  |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ①
- ②

## 9. 인용 가능 문장 (deck/paper용)
- "<defensible 1-liner>"

## 10. 주의/한계 (over-claim 방지)
- 

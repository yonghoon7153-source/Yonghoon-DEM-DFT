# 대칭셀 EIS (임피던스) — 2026-06-18 초기 측정

> 사용자: "초반 나온 임피던스 프로파일". No.1/No.2/Poly 대칭셀 EIS.
> `raw_mps/`에 EC-Lab **설정파일(.mps)** 보관. ⚠ .mps = 측정 프로토콜만 — **실제 Nyquist 스펙트럼
> (.mpr/.txt)은 아직 미확보**. 스펙트럼 확보 시 `raw_mpr/` 또는 `nyquist_*.csv`로 추가 후 피팅값 기록.

## 측정 조건 (PEIS, 6개 파일 동일)
| 항목 | 값 |
|---|---|
| 장비 | BioLogic **VSP-300** (EC-Lab v11.63) |
| 기법 | Potentio EIS (PEIS), single sine |
| 전위 | E = 0 V vs E_oc |
| 주파수 | **7 MHz → 10 mHz**, 10 points/decade, log spacing |
| 진폭 V_a | 5.0 mV |
| 평균 N_a | 2 |
| (헤더 표면적/질량은 0.001 기본값 — 실제값으로 보정 필요) |

## 파일 목록 (`raw_mps/`)
| 파일 | 샘플 | 셀 | 비고 |
|---|---|---|---|
| 260618_No1_sym_1.mps | No.1 (NCM_2) | 대칭셀 #1 | |
| 260618_No1_sym_2.mps | No.1 (NCM_2) | 대칭셀 #2 | 반복/2차 |
| 260618_No2_sym_1.mps | No.2 (NCM_3) | 대칭셀 #1 | |
| 260618_No2_sym_2.mps | No.2 (NCM_3) | 대칭셀 #2 | 반복/2차 |
| 260618_poly_sym_1.mps | Poly (대립) | 대칭셀 #1 | |
| 260618_poly_sym_2.mps | Poly (대립) | 대칭셀 #2 | 반복/2차 |

## 맥락 / 다음 단계
- 6/25 미팅 계획의 "3:7/5:5/7:3 대칭셀 데이터(이온전도도)"와 동일 측정 라인 (여기는 단일 소재 No.1/No.2/Poly).
- 대칭셀(전극/SE/전극) → **TLM 피팅으로 전극 R_ion·R_int 추출** (cf. powder 풀셀 TLM:
  No.1 R_ion 0.61/R_int 4.42, No.2 0.87/23.37 Ω·cm² — `../impedance_tlm.csv`).
- 스펙트럼(.mpr) 확보 → Nyquist → R_ion/R_int/Warburg 피팅값을 `eis_fit_results.csv`로 추가 예정.

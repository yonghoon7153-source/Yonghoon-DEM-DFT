<!-- 🌱 research-agent 가 만든 **뼈대**다.  실물(PDF·SI)을 읽고 채워야 digest 가 된다.
     깊이 기준 = litdb/papers/_TEMPLATE.md · 실제 사례 = bazzoun2026_dem_fem_rnm_ionic.md.
     ⛔ `⏳ 문서 대기` 가 하나라도 남아 있으면 이 카드를 **인용하지 않는다**. -->
# Domain oriented universal machine learning potential enables fast exploration of chemical space of battery electrolytes — Feng Wang (Nature Communications 2026)

> slug `wang2026_domain_oriented_universal_machine_learning_potential` · DOI `10.1038/s41467-025-67982-0` · type `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)`
> · PDF `⏳ 미확보` · digested `2026-09-03` · status `🌱 skeleton (문서 대기)`
> · evidence_level `fulltext`
> · IF `15.7` · tier `B` · relevance `0.45`

## 0. 왜 이 카드가 열렸나 (research-agent 판정)
Nature Communications(IF 15.7)이고 키워드 'dft battery'에 잡혔지만 대상이 액체 전해질이라 내 황화물 SE 연구와 직접 연결되지는 않는다. 그래도 내 파이프라인의 DFT → MLIP(UMA/MACE) 단계에서 '학습 데이터를 어떻게 구성해 transferability를 확보하는가'라는 방법론적 질문에 좋은 참고가 돼 Tier를 유지하되 관련도는 낮게 둔다.

## 1. 한 줄 요약
Wang et al.(Xiamen Univ., Jun Cheng)은 2,300여 용매·20종 Li 염을 무작위 조합한 ~16만 구성의 DeePMD 기반 범용 MLIP(PBE-D3 라벨, 힘 RMSE ≈160 meV Å⁻¹)를 만들어 액체 전해질의 밀도(<5 % 오차)·이온 전도도·점도를 ns 규모 MD로 예측하고, Li⁺ 배위 수명(τ)을 용매화 세기의 정량 지표로 제안했다.

## 2. 메타
| 저자 | 저널/년 | DOI | 조성·계 | 연구유형 |
|---|---|---|---|---|
| Feng Wang, Yu-Hang Tang, Ze-Bing Ma, Yu-Cheng Jin, Jun Cheng | Nature Communications 2026 | 10.1038/s41467-025-67982-0 | ⏳ 문서 대기 | ⏳ 문서 대기 |

## 3. 핵심 물성 (수치) ★ 실물 필요
> ⛔ 초록만으로 채우지 말 것.  단위·조건 없는 값은 우리 db 와 **같은 표에 놓을 수 없다**.
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| ⏳ 문서 대기 |  |  |  |

## 4. 방법 ★ 실물 필요
- **code / version**: ⏳ 문서 대기
- **축 A(DEM/MPM/복셀)**: 접촉모델·강성·마찰·압축압력·입경분포·셀·복셀 크기 —
- **축 B(DFT/MLIP)**: functional·vdW·pseudo/PAW·k-points·ecut·supercell·U·MLIP 학습셋 —
- **축 C(실험)**: 셀 구성·면적용량·온도·율·EIS 조건·등가회로 —
- **무질서·상태 선택 규칙**(있으면):
- **특이사항**:

## 5. Figure set ★ 실물 필요
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| ⏳ 문서 대기 |  |  |

## 6. Post-processing ★ 실물 필요
- **무엇**: (NEB / BVSE / COHP / TauFactor / Kirchhoff / Heckel / CNLS fit …)
- **도구**:
- **수치화·플롯 방식**:

## 7. 우리 대비 ★ 실물 필요 — 이 카드의 값어치는 여기서 나온다
- **어느 축인가**: (A: DEM/MPM/복셀 · B: DFT/MLIP · C: 실험 EIS · none)
- **우리 확보값과의 일치/충돌**: → `db/properties/canonical_registry.json`(축 B) ·
  `docs/db/section7_10case_sweep.csv`(축 A) 와 대조
- **인용 포인트**: (축 A = `main.tex` 절 이름 / 축 B = `kb/` 카드 또는 `db/properties/` 항목)
- **비판 포인트**: (보고량 정의가 있는가 · 상태 선택 규칙이 있는가 · 수렴을 보였는가 ·
  DEM↔MPM 을 서로 보정했는가[frame[4] 위반] · DOS-threshold 갭 · 단일시드 σ 비)

## 8. research-agent 초록 판정 (실물 판독으로 대체될 것)
- 전해질 생성기로 >2,300 용매 × 20 Li 염 조합에서 ~100만 계를 만들고, concurrent learning 91회 반복으로 ~160,000 구성을 PBE-D3로 라벨링해 DeepPot-SE 모델을 학습했다(원소: C, H, O, N, B, S, F, Cl, Br, I, P, Si).
- 에너지 RMSE ≈0.005 eV atom⁻¹, 힘 RMSE ≈160 meV Å⁻¹, virial ≈5 meV atom⁻¹; 밀도 오차 <5 %, 전도도 최대 농도 위치와 온도 의존성을 재현했다.
- Li⁺ 배위 수명 τ가 짧으면(<15 ps) 약한 용매화·높은 전도도, 길면(200~1,000 ps, 저온) 강한 용매화로 대응돼 τ가 용매화 세기의 직접 지표가 된다.
- LiTFSI/FAN, LiFSI/DMC, LiPF₆/EC-EMC 등 대표 전해질과 이온성 액체, 다가 양이온(Na⁺, K⁺, Mg²⁺, Ca²⁺, Zn²⁺)까지 재학습 없이 적용했다.

## 9. 남은 일
- [ ] PDF·SI 확보 → §3–§7 채우기
- [ ] `status` 를 `✅` 로, `evidence_level` 을 `fulltext` 로
- [ ] `INDEX.md`(argyrodite SE 축) 또는 `INDEX_DEM.md`(DEM 축)에 **손으로** 등재

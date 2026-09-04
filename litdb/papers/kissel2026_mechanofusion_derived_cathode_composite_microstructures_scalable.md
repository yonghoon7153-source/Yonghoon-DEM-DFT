<!-- 🌱 research-agent 가 만든 **뼈대**다.  실물(PDF·SI)을 읽고 채워야 digest 가 된다.
     깊이 기준 = litdb/papers/_TEMPLATE.md · 실제 사례 = bazzoun2026_dem_fem_rnm_ionic.md.
     ⛔ `⏳ 문서 대기` 가 하나라도 남아 있으면 이 카드를 **인용하지 않는다**. -->
# Mechanofusion-derived cathode composite microstructures with scalable mixed conducting matrix coatings for solid state batteries — Maximilian Kissel (Nature Communications 2026)

> slug `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` · DOI `10.1038/s41467-026-71305-2` · type `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)`
> · PDF `⏳ 미확보` · digested `2026-09-03` · status `🌱 skeleton (문서 대기)`
> · evidence_level `fulltext`
> · IF `15.7` · tier `A` · relevance `0.9`

## 0. 왜 이 카드가 열렸나 (research-agent 판정)
Nature Communications(IF 15.7)에 실린 2026년 논문이면서, 내 주축인 'DEM으로 composite cathode 미세구조를 설계한다'는 문제의식을 공정(혼합) 단계에서 다룬다. 내 DEM은 압축(compaction) 단계, 이 논문은 혼합 단계라 서로 보완적이고, DEM 결과를 실험 지표(피복률, 입도, 공극률)로 검증한 사례라서 내 porosity 보정·검증 논리의 근거로 바로 쓸 수 있다.

## 1. 한 줄 요약
Kissel et al.(Janek group)은 mechanofusion 고강도 건식 혼합으로 single-crystal NCM82 위에 Li₃InCl₆ 코팅(5 nm~100 nm)을 만들고, DEM으로 계산한 stress intensity(SI ∝ n²)와 코팅 피복률·공극률을 연결해 80:20:0.5(NCM:LIC:CB) 조성에서 1 C에서 100 mAh g⁻¹(복합전극 질량 기준)을 얻었다.

## 2. 메타
| 저자 | 저널/년 | DOI | 조성·계 | 연구유형 |
|---|---|---|---|---|
| Maximilian Kissel, Finn Frankenberg, Thomas Demuth, Anton Lai, Niklas Laser | Nature Communications 2026 | 10.1038/s41467-026-71305-2 | ⏳ 문서 대기 | ⏳ 문서 대기 |

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
- 코팅 함량 1~20 wt%, 회전속도 1,000~10,000 rpm, 혼합 5~60 min 조건에서 균일 코팅을 얻었고, XPS 피복률은 최고 함량에서 1.0에 근접했다(≥5,000 rpm, 5~10 min이면 97~100 %).
- DEM(coarse-graining)으로 계산한 stress intensity는 회전속도의 제곱에 비례(SI ∝ n²)했고, specific energy input이 커질수록 코팅이 두꺼워지고 피복률이 올라갔다.
- 복합전극 공극률은 코팅 함량과 혼합 강도가 커질수록 약 40 %에서 약 25 %로 떨어졌다(압축 후 기준).
- LIC 매트릭스에 carbon black을 넣으면 전자 percolation threshold가 2~5 wt% 사이에서 나타났고, 전자 부분 전도도는 <0.01 → ~1,000 mS cm⁻¹(0 → 15 % CB)로 올라간 반면 이온 부분 전도도는 ~0.7 → ~0.03 mS cm⁻¹로 떨어졌다.
- 80:20:0.5 조성에서 1 C에 100 mAh g⁻¹(복합전극 질량 기준), CB 과다(3 %)에서는 1 C 용량이 <10 mAh g⁻¹로 급락해 kinetics·chemo-mechanics 악화를 보였다(CAM 이용률은 65 → 90 %로 올라감).

## 9. 남은 일
- [ ] PDF·SI 확보 → §3–§7 채우기
- [ ] `status` 를 `✅` 로, `evidence_level` 을 `fulltext` 로
- [ ] `INDEX.md`(argyrodite SE 축) 또는 `INDEX_DEM.md`(DEM 축)에 **손으로** 등재

<!-- 🌱 research-agent 가 만든 **뼈대**다.  실물(PDF·SI)을 읽고 채워야 digest 가 된다.
     깊이 기준 = litdb/papers/_TEMPLATE.md · 실제 사례 = bazzoun2026_dem_fem_rnm_ionic.md.
     ⛔ `⏳ 문서 대기` 가 하나라도 남아 있으면 이 카드를 **인용하지 않는다**. -->
# Using resistor network models to predict the transport properties of solid-state battery composites — Lukas Ketter (Nature Communications 2025)

> slug `ketter2025_resistor_network_models_predict_transport_properties` · DOI `10.1038/s41467-025-56514-5` · type `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)`
> · PDF `⏳ 미확보` · digested `2026-09-03` · status `🌱 skeleton (문서 대기)`
> · evidence_level `fulltext`
> · IF `15.7` · tier `A` · relevance `0.95`

## 0. 왜 이 카드가 열렸나 (research-agent 판정)
2025년 2월 논문이라 '최신'은 아니지만, 내가 만들고 있는 DEM-native resistor-network solver의 가장 직접적인 선행연구다. 같은 재료계(NCM8x + LPSCl), 같은 목표(유효 전도도 예측), 다른 표현 방식(voxel vs 입자 접촉)이라 방법론 비교와 검증 데이터 확보에 필수라 bootstrap에 넣었다. Nature Communications(IF 15.7).

## 1. 한 줄 요약
Ketter et al.(Zeier group)은 300³ voxel(2 µm/voxel) resistor network로 NCM83–Li₆PS₅Cl 복합양극의 유효 전자·이온·열 전도도를 계산해 EIS/DC 분극 실험과 맞췄고, 복합전극 열전도도가 조성과 무관하게 1 W m⁻¹ K⁻¹ 아래에 머문다는 점을 보였다.

## 2. 메타
| 저자 | 저널/년 | DOI | 조성·계 | 연구유형 |
|---|---|---|---|---|
| Lukas Ketter, Niklas Greb, Tim Bernges, Wolfgang G. Zeier | Nature Communications 2025 | 10.1038/s41467-025-56514-5 | ⏳ 문서 대기 | ⏳ 문서 대기 |

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
- 300×300×300 voxel(각 2 µm) 미세구조에 LPSCl(~20 µm 입자 → voxel clustering)과 NCM83(~2 µm)을 배정하고, 양면에 전위/온도 구배·나머지 면은 zero-flux 조건을 걸어 정상상태 flux로 유효 전도도를 구했다.
- NCM83 부피분율에 따라 유효 전자 전도도는 10¹~10⁻² mS cm⁻¹, 유효 이온 전도도는 10¹~10⁻⁵ mS cm⁻¹ 범위를 보였고, 두 전도도가 가장 균형을 이루는 조성은 NCM83 약 40 %였다.
- 열전도도는 LPSCl 0.32 ± 0.02, NCM83 0.71 ± 0.04 W m⁻¹ K⁻¹였고, 복합전극은 계면 열저항(2×10⁻⁶ m² K W⁻¹) 때문에 조성에 거의 무관하게 낮은 값(<1 W m⁻¹ K⁻¹)에 머물렀다.
- VGCF <2 wt% 첨가로 전자 전도도는 두 자릿수 이상 올랐지만 열전도도는 거의 변하지 않았다.
- LiMn₂O₄–Li₃InCl₆, 다공성 LPSCl, PEO:LiTFSI:SiO₂ 문헌 데이터에도 같은 모델을 적용해 일반성을 보였다.

## 9. 남은 일
- [ ] PDF·SI 확보 → §3–§7 채우기
- [ ] `status` 를 `✅` 로, `evidence_level` 을 `fulltext` 로
- [ ] `INDEX.md`(argyrodite SE 축) 또는 `INDEX_DEM.md`(DEM 축)에 **손으로** 등재

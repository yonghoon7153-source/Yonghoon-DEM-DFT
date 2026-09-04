<!-- 🌱 research-agent 가 만든 **뼈대**다.  실물(PDF·SI)을 읽고 채워야 digest 가 된다.
     깊이 기준 = litdb/papers/_TEMPLATE.md · 실제 사례 = bazzoun2026_dem_fem_rnm_ionic.md.
     ⛔ `⏳ 문서 대기` 가 하나라도 남아 있으면 이 카드를 **인용하지 않는다**. -->
# Planar Li deposition and dissolution enable practical anode-free pouch cells — Lei Liu (Nature 2026)

> slug `liu2026_planar_li_deposition_dissolution_enable_practical` · DOI `10.1038/s41586-026-10402-0` · type `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)`
> · PDF `⏳ 미확보` · digested `2026-09-03` · status `🌱 skeleton (문서 대기)`
> · evidence_level `fulltext`
> · IF `48.5` · tier `A` · relevance `0.55`

## 0. 왜 이 카드가 열렸나 (research-agent 판정)
Nature(IF 48.5)라 IF 순위 최상위지만, 액체 전해질 anode-free 논문이라 내 키워드 'anode-less assb'와는 시스템이 다르다. 그래도 '평면 석출을 만드는 계면 조건(SEI 균질성·기계적 유연성)'은 전고체 anode-free에서도 같은 설계 변수이므로, 배경·논리 인용용 Tier A로 유지하되 관련도는 0.55로 낮춰 잡는다.

## 1. 한 줄 요약
Liu et al.(Westlake Univ.)은 LiDFOB/NDFA 기반 'crossover-coupled' 전해질로 8 nm 두께의 균질한 B–F 고분자계 SEI를 만들어 Cu‖NCM811 anode-free 파우치셀(5.6 mAh cm⁻², 2.7 Ah)에서 Li의 2차원 평면 석출·용해를 구현했고 508 Wh kg⁻¹·100 % DOD 100 사이클(80 % 유지)을 보고했다.

## 2. 메타
| 저자 | 저널/년 | DOI | 조성·계 | 연구유형 |
|---|---|---|---|---|
| Lei Liu, Yuxuan Xiang, Xingyu Lu, Jianhui Wang | Nature 2026 | 10.1038/s41586-026-10402-0 | ⏳ 문서 대기 | ⏳ 문서 대기 |

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
- SEI의 micro-heterogeneity와 기계적 취약성이 Li 석출·용해 불균일의 근원이라는 진단에서 출발해, 전해질 설계로 SEI 자체를 균질화했다.
- 1.6 M LiDFOB in NDFA 전해질에서 라디칼 종이 음극(3.9 V)에서 양극(4.2 V)보다 먼저 생성되는 위치 의존 계면 반응이 일어나, B–F 기반 고분자가 풍부한 'self-adaptive mesh-film' SEI(두께 8 nm, sub-nm 균질도)가 형성됐다.
- Cu‖NCM811 anode-free 파우치셀에서 5.6 mAh cm⁻², 2.7 Ah, 508 Wh kg⁻¹(1,668 Wh L⁻¹); 100 % DOD 100 사이클, 80 % DOD 250 사이클에서 80 % 용량 유지.
- 출력 2,650 W kg⁻¹(96 Wh kg⁻¹ 기준), 작동 온도 −40~100 °C.
- cryo-FIB-SEM/cryo-TEM, in situ EPR, 고체/액체 NMR로 SEI 구조와 라디칼 형성을 추적했다 — 계산(DFT/MD)은 사용하지 않았다.

## 9. 남은 일
- [ ] PDF·SI 확보 → §3–§7 채우기
- [ ] `status` 를 `✅` 로, `evidence_level` 을 `fulltext` 로
- [ ] `INDEX.md`(argyrodite SE 축) 또는 `INDEX_DEM.md`(DEM 축)에 **손으로** 등재

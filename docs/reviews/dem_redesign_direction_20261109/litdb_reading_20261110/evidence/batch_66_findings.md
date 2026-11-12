# 배치 66 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode` (404 줄 · 원문 = Extreme Mech. Lett. 본문 8 쪽 · SI 없음 ·
그림 크롭 40 장 = 도구 8 (전부 다시 자름) + 패널 18 + 식 3 + 근거 문단 11 · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 287 행 — 그림 3b · 3c · 4 · 6 · 3a 삽입도는 벡터 경로 좌표로 읽음).
서지 (k · l 인용용) = de Vasconcelos L. S., Xu R., Li J., Zhao K., *Grid indentation analysis of mechanical properties of composite electrodes in Li-ion batteries*,
Extreme Mech. Lett. 9 (2016) 495–502, DOI 10.1016/j.eml.2016.03.002.
⚠ 재료 = NMC532 · PVDF · CB (90 : 5 : 5 wt%) **액체계 LIB 양극 · 캘린더링 안 함 · 기공 56 %** + 별도 CB/PVDF 50/50 필름 (61 %) · 고체전해질 없음 · 압력 이력 없음 · 계산 없음 — 아래 값을 LPSCl · NCM811 값처럼 쓰지 않는다.
쪽 = PDF p.1–8 (학술지 p.495–502 = 494 + PDF 쪽).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- 이 배치에 없음 — 고체전해질이 없다.  (전극 · CB/PVDF 필름의 질량-두께 기공은 질문 i 에.)

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | 전극 수준 탈압 **없음** — 압입 제하 곡선 하나뿐: NMC532 단일 입자 · Berkovich · 하중 최대 ≈20.4 mN (변위 ≈397 nm) → 5 s 유지 중 ≈406 nm (≈10 nm 더 들어감) → 하중 0 에서 ≈201 nm ⇒ h_f/h_max ≈0.49 | 카드 §3-3 · 그림 3a 삽입도 (p.5) | [판독 · 벡터] · [카드 산술] | AM (NMC532) 이 눌린 쪽 · SE 아님 · 압입 (국소) 되돌아옴이지 전극 두께 회복이 아님 · 원문은 이 곡선의 수치를 보고하지 않음 (*"a set of 400 nm maximum displacement"* p.4 만)

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | ★ NMC532 이차입자 압입 경도 **H 8.89 ± 1.86 GPa** (targeted · 깊이 창 75–150 nm) · 격자 분해 입자 **7.78 ± 1.40** · 깊이별 9.54 (52 nm) → 5.36 GPa (420 nm) · 탄성률 **E 138.73 ± 18.78** (targeted) · **123.02 ± 20** (격자) · 151.6 → 73.4 GPa (깊이) | 카드 §3-3 · §3-6 · p.4 · 표 2 · 그림 3c | [인쇄] (창 · 표 2) · [판독 · 벡터] (깊이별) | 정의 = Oliver–Pharr 압입 경도 · E 는 ν 0.3 가정 · NMC532 · 국소 (입자 전체 아님) · **일축 항복 환산 없음** · 크리프 값 없음 (5 s 유지만)
- [c] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | 별도 CB/PVDF 50/50 wt% 필름 (기공 61 %): **E 1.78 ± 0.35 · H 0.043 ± 0.01 GPa** (350 회 · 깊이 200–2200 nm 일곱 깊이 평균 · 깊이별 E 1.47 → 2.22 GPa) · 전극 속 기지 (격자) **4.40 ± 2 · 0.13 ± 0.01** (2–3 배) | 카드 §3-4 · §3-6 · p.4 · p.7 · 표 2 · 그림 4 | [인쇄] · [판독 · 벡터] | 다공 PVDF + CB 복합 — PTFE · SE 기지가 아님 · 저자: 덜 다공이면 더 큼
- [c] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | 우리와 견줌: H_AM 4.0 (`am_load_balance_jam.py --h-am` 기본) · 6.0 (fracture_model.py) 은 원전 8.89 · 7.78 의 0.45–0.67 배 → 우리 "3–6 GPa" 밴드 밖 · Tabor H/3 ≈3.0 GPa 는 원문에 없는 환산 (취성 세라믹의 항복 아님) | 카드 §7-1 · §14 D15 · D18 | [카드 산술] · [우리] | 압입 경도 ↔ 우리 H_AM (입자 크라운 지지압) 은 이름만 같은 다른 양 ([Sedl26] §7.5)

## d — 단단한 입자 + 무른 입자 혼합 압밀의 하중 몫 · 재밍

- 이 배치에 없음 — 압밀 · 하중 분담 실험이 아니다.  곁가지: 연한 상 (CB/PVDF) 을 복합 안에서 누르면 밑에 묻힌 단단한 NMC 가 겉보기 E · H 를 **2–3 배** 올린다 (*"NMC particles are likely buried underneath the surface of CB/PVDF coating"* p.7) — 하중 분담이 아니라 압입 기판 효과 (카드 §3-6).

## e — 점접촉 법칙의 큰 변형 한계 · 대안

- 이 배치에 없음 (접촉 모델 없음).  곁가지 입력값: NMC532 의 (E, H) 쌍 · H/E 0.064 [카드 산술] — MDR · Thornton–Ning 류 AM 쪽 항복 입력을 경도에서 잡을 때의 자릿수 (카드 §8 후보 C · C′).

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙

- 이 배치에 없음 (MPM 없음).  곁가지 유비: 격자 압입 규칙 *"the indentation depth (typically 100 nm) is much smaller than the characteristic size of the constituent phases, and the spacing between the indents (3–5 µm) is larger than the size of individual impression"* (p.4) = 탐침 부피 ≪ 상 크기 — 우리 '지름당 셀 수' · d_h/dx 규칙과 같은 꼴 [카드 해석] (카드 §8 U0–U6).

## g — 2D 결과를 3D 로 옮길 때의 경고 · 증거

- [g] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | 연마면 (2D) 의 상 분율 ≠ 부피 분율: *"The surface fraction of individual components in the selected indentation area may deviate from the overall volume fraction in the samples."* · 카드 산술: 입자 표면 분율 38.40 % ↔ 이론 밀도로 계산한 NMC 부피 분율 ≈34 % (33.2–34.6) | 카드 §3-1 · §4-3 (iii) · p.4 | [인쇄] · [카드 산술] | 33 × 33 µm 한 구역 · 액체계 전극

## h — DEM 에서 FE · MPM 으로 넘긴 선례 · 넘긴 시점

- 이 배치에 없음 (모델 없음).  이 논문 값을 FE 입력으로 쓴 사용례는 `wang2027_…` (NCM811 복셀 FE · E 140 · CBD 1.8 GPa) — 카드 §7-3.

## i — 복합 양극 (AM + SE) 압력별 기공

- [i] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | **압력별 아님 · SE 없음** — 캘린더링 안 한 NMC532 · PVDF · CB 액체계 양극의 질량-두께 기공 (식 1) **55.32 · 55.86 · 57.15 % (평균 56 %)** · CB/PVDF 필름 61.39 · 63.71 · 57.95 % (평균 61 %) · 이론 밀도 NMC 4.77 · CB 1.90 · PVDF 1.76 · Al 2.70 mg/mm³ | 카드 §3-1 · 표 1 · p.3 | [인쇄] | ⚠ 표 1 양극 h_Al "0.015 µm" = 실제 0.015 mm (그래야 재현 55.31 · 55.85 · 57.13 %; 글자대로면 38 %) · CB/PVDF 열은 식 1 로 재현 불가 (Al 질량 > 시료 무게) [카드 산술]

## j — 카드가 스스로 적은 한계 중 가압 · 탈압과 닿는 것

- [j] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | 저자 한계: 기지 값은 기공에 크게 좌우 (*"One may expect to obtain higher values of modulus and hardness for samples of low porosity"* p.4) — 압밀로 기공이 줄면 CBD 강성이 바뀐다는 정성 진술 · 복합 전극 물성은 *"packing density of the active material … and tortuosity of the surrounding medium"* 에 크게 의존 (p.2) · SOC · 사이클 의존 = 다음 연구 (p.7) | 카드 §3-7 · §4-3 | [인쇄] | 캘린더링 · 압밀 실험 자체는 없음

## k — DEM 의 한계 (인용 서지 = de Vasconcelos L. S. et al., Extreme Mech. Lett. 9 (2016) 495–502)

- [k] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode (de Vasconcelos et al. 2016, Extreme Mech. Lett. 9, 495–502) | **말 없음** — DEM · 입자 모델을 쓰지 않는다.  모델 일반에 대한 문장만: *"The mechanical properties of electrodes are prerequisite parameters for the mechanics models. Nevertheless, elastic modulus, hardness, and fracture strength of most emerging electrode materials are unknown a priori that makes theoretical predictions questionable."* | p.1–2 (카드 §4-3 (i) · `txt_p1_p2_prerequisite_parameters_twofold.png`) | [인쇄] | DEM 한계의 근거로는 쓸 수 없다 — "입력 물성이 모르는 값이면 예측이 의심스럽다" 는 일반 진술

## l — 소성변형이 왜 어려운가 (인용 서지 = de Vasconcelos L. S. et al., Extreme Mech. Lett. 9 (2016) 495–502)

- [l] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode (de Vasconcelos et al. 2016, Extreme Mech. Lett. 9, 495–502) | **모델 관점 말 없음** — 측정 쪽 어려움 두 가지: *"First, electrodes in commercial batteries are heterogeneous materials … The constituent components have large difference in their mechanical properties—the elastic modulus changes by 2–3 orders of magnitude for instance. In addition, the mechanical properties of composite electrodes are highly dependent on the packing density of the active material from the elementary powders and tortuosity of the surrounding medium"* · *"Second, the mechanical properties of active materials may vary significantly with the state of charge"* (Si 취성 → 연성) · 우회 = 많은 얕은 압입 + 통계 분해 (맞춘 값: 상마다 µ_E · σ_E · µ_H · σ_H 4 개 × 3 상 + 공유 f_i 3 개 = 15 개 (Σ f_i = 1 이라 독립 14 개) · 맞춘 대상 = E · H 의 경험 CDF · 검증 = targeted 압입 · 비용 = 121 회 (지도) / 분해 표본 ≈243 [카드 판독]) | p.2 · p.4–7 (카드 §3-6 · §4-3 (ii)) | [인쇄] · [카드 판독] · [카드 산술] (맞춘 값 수) | 입자 소성 · 큰 변형을 계산에 넣는 어려움은 다루지 않는다 — 경도 (소성 저항) 를 잴 뿐

## m — 받아들일 통찰

- [m] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | ★ 판독 창을 결과 전에: 같은 입자에서 압입 깊이 창만 바꿔도 E 가 151.6 → 73.4 GPa (×0.48) · 창 75–150 nm 은 데이터를 보고 정했다 → 우리 압입 · 응력 · 기공 판독 창 (깊이 · 프레임 · 구간) 을 결과 전에 적고 인용 값마다 창을 꼬리표로 | 자리: 단계 0 · 결과 전 대조 항목 | 근거 p.4 · 그림 3c · 카드 §3-3
- [m] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | ★ 연한 상의 복합 내 측정은 밑의 단단한 상 때문에 2–3 배 부푼다 (CB/PVDF 4.40 ↔ 1.78) → SE 물성 앵커 (E · H · σ_y) 는 순수 SE 펠릿 측정에서 · 복합 단면 압입 값을 SE 물성으로 쓰지 않는다 | 자리: 단계 4 · 흐름 밖: SE 물성 앵커 고르기 | 근거 p.7 · 표 2 · 카드 §3-6
- [m] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | ★ 함정 (숫자 겹침): 우리 MPM `ADD_E_NU` 의 PTFE E 1.80 GPa (사용자 지정 · 출처 미기재) 가 이 논문 CB/PVDF 1.78 GPa 와 반올림해 같다 → 출처를 채울 때 이 논문을 쓰지 않는다 (61 % 다공 PVDF + CB 필름 · 다른 재료) | 자리: 흐름 밖: 첨가제 상 E 의 출처 정리 (단계 5 의 첨가제 입력) | 근거 p.4 · 작업 트리 `scripts/mpm3d_compaction.py` L155–162 · 카드 §7-1
- [m] devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode | 보고 방식: 통계 분해 값을 낼 때 표본 수 · 분모 규약을 적는다 — 이 논문은 지도 121 회만 적고 분해 표본은 미기재 (경험 CDF 분모 243 [카드 판독]) · 표 2 의 H 값이 그린 H 맞춤을 재현 못 함 (RMS 0.046) → 우리 분포 맞춤 · 지표 보고에 N · 분모 · 재현 검산 (그린 곡선 ↔ 표 값) 을 함께 | 자리: 흐름 밖: 통계 지표 보고 · 결과 전 대조 항목 | 근거 그림 5 · 6 · 표 2 · 카드 §3-6

## n — 논문 에이전트 후보 (이 논문이 인용 · 정본에 카드 없음)

- [n] G. Constantinides, K.R. Chandran, F.-J. Ulm, K. Van Vliet, Grid indentation analysis of composite microstructure and mechanics: principles and validation, Mater. Sci. Eng.: A 430 (2006) 189–202. | c · m — 격자 압입 원리 · 검증 규칙 (깊이 ≪ 상 크기 · 간격 > 압흔 · 통계 분해) 의 원전 · 카드 §12 [34] | litdb 확인: `git ls-tree … litdb/papers/` 에 constantinides* 없음 · "Constantinides" · "Grid indentation analysis of composite microstructure" grep 0 건 → 카드 없음
- [n] W.C. Oliver, G.M. Pharr, An improved technique for determining hardness and elastic modulus using load and displacement sensing indentation experiments, J. Mater. Res. 7 (1992) 1564–1583. | c — 우리 모든 압입 앵커 (H_AM · LPSCl H 1.41 · NMC E) 의 H · reduced modulus 정의 원전 (ν 가정이 필요한 이유) · 카드 §12 [42] | litdb 확인: oliver* · pharr* 파일 없음 · 제목 grep = papakyriakou2021 · stallard2022 (인용만) → 카드 없음
- [n] F.J. Ulm, M. Vandamme, C. Bobko, J. Alberto Ortega, K. Tai, C. Ortiz, Statistical indentation techniques for hydrated nanocomposites: concrete, bone, and shale, J. Am. Ceram. Soc. 90 (2007) 2677–2692. | c — 다공 복합체 통계 압입 · 상 물성의 다짐 (packing density) 의존 — 다공 SE 펠릿 · 압밀체 압입 해석의 틀 · 카드 §12 [35] | litdb 확인: ulm* 파일 없음 · "Statistical indentation techniques" grep 0 건 → 카드 없음
- [n] B. Vijayaraghavan, D.R. Ely, Y.-M. Chiang, R. García-García, R.E. García, An analytical method to determine tortuosity in rechargeable battery electrodes, J. Electrochem. Soc. 159 (2012) A548–A552. | 단계 7 · m — tortuosity 해석식 (정본 J 절 명명 규약과 대조할 원전) · 이 논문의 *"packing density … tortuosity"* 근거 [29] · 카드 §12 | litdb 확인: vijayaraghavan* 없음 (vijay2025 는 다른 논문) · 제목 grep = froboese2019 · tjaden2018 (인용만) → 카드 없음

## 카드 문제

- `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn` L316 · comparison_vs_ours_DEM.md L4400: *"138.73 은 NMC532 **grid** 압입값으로 보인다"* — 원문은 **targeted** (단일 입자 · 75–150 nm 창) · 격자 입자 값은 123.02 ± 20 (조성 NMC532 는 맞음).  고치지 않았다 (새 카드 · 비교 문서 새 항목 [deVasc16] 에 정정 사실만 적음).
- `shi2019_high_am_loading_particle_size_assb` L120 · L176 · L435: Shi 2019 SI 가 `[2]` (이 논문) 에 단 **E_AM 177.5 · σ_y 12.6 · ρ 4.85** 는 원문에 **없다** (ν 0.3 만 해석 가정 · ρ_NMC = 4.77) — 카드의 "귀속 오류 공산" 이 확정됨 (카드 내용은 맞음 · 원 논문의 오귀속).
- `xu2023_realistic_am_shape_cgmd_calendering` L110 · L361: E_AM **135 GPa** 의 출처 묶음 refs [39–41] 에 *"grid indentation"* 이 들었다고 적었으나 이 논문에 135 는 없다 (138.73 · 123.02) — [39–41] 에 이 논문이 포함되는지는 이 카드로 판정 불가.
- `so2021_dem_mold_pressure_assb_coldpress` L40: *"H_AM (Si hardness) 10.6 GPa — de Vasconcelos [38]"* — 이 논문은 Si 를 재지 않았다 · so2021 카드에 [38] 서지가 없어 어느 de Vasconcelos 논문인지 판정 불가.
- `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` L140: Xu 2017 그림 4b 의 CB+PVDF 기지 1.78 ± 0.35 · 0.043 ± 0.01 은 이 논문 targeted 값과 같다 (재측정인지 재사용인지는 판정 불가) — 카드 문제는 아니고 출처 사슬 메모.
- 원문 안 어긋남 (카드 §3-7): 표 1 h_Al 단위 · CB/PVDF 열 재현 불가 · 적재 12.5 ↔ 표 1 10.0–10.5 mg/cm² · 식 2 하한 0 ↔ 그림 6a 는 보통 CDF · 표 2 H 값 ↔ 그림 6c 불일치 · 분해 표본 수 미기재 (분모 243).

---
title: "Using resistor network models to predict the transport properties of solid-state battery composites"
aliases: ["Using resistor network models to predict the transport"]
authors: ["Lukas Ketter", "Niklas Greb", "Tim Bernges", "Wolfgang G. Zeier"]
journal: "Nature Communications"
year: 2025
doi: "10.1038/s41467-025-56514-5"
url: "https://www.nature.com/articles/s41467-025-56514-5"
if: 15.7
tier: "A"
relevance: 0.95
status: digested
keywords: ["dem battery"]
tags: ["paper/dem", "tier/A", "topic/resistor-network", "topic/effective-conductivity", "material/LPSCl", "material/NCM83"]
source: bootstrap
date_added: 2026-09-03
analyzed_at: 2026-09-03
evidence_level: fulltext
ra_id: "doi:10.1038/s41467-025-56514-5"
---

# Using resistor network models to predict the transport properties of solid-state battery composites

**Lukas Ketter, Niklas Greb, Tim Bernges, Wolfgang G. Zeier** — *Nature Communications* (2025) · IF 15.7 · Tier A · 관련도 0.95
DOI: [10.1038/s41467-025-56514-5](https://doi.org/10.1038/s41467-025-56514-5)
키워드: [[dem battery]]

> [!abstract] 한 줄 요약
> Ketter et al.(Zeier group)은 300³ voxel(2 µm/voxel) resistor network로 NCM83–Li₆PS₅Cl 복합양극의 유효 전자·이온·열 전도도를 계산해 EIS/DC 분극 실험과 맞췄고, 복합전극 열전도도가 조성과 무관하게 1 W m⁻¹ K⁻¹ 아래에 머문다는 점을 보였다.

## 선정 이유
2025년 2월 논문이라 '최신'은 아니지만, 내가 만들고 있는 DEM-native resistor-network solver의 가장 직접적인 선행연구다. 같은 재료계(NCM8x + LPSCl), 같은 목표(유효 전도도 예측), 다른 표현 방식(voxel vs 입자 접촉)이라 방법론 비교와 검증 데이터 확보에 필수라 bootstrap에 넣었다. Nature Communications(IF 15.7).

## 핵심 내용
- 300×300×300 voxel(각 2 µm) 미세구조에 LPSCl(~20 µm 입자 → voxel clustering)과 NCM83(~2 µm)을 배정하고, 양면에 전위/온도 구배·나머지 면은 zero-flux 조건을 걸어 정상상태 flux로 유효 전도도를 구했다.
- NCM83 부피분율에 따라 유효 전자 전도도는 10¹~10⁻² mS cm⁻¹, 유효 이온 전도도는 10¹~10⁻⁵ mS cm⁻¹ 범위를 보였고, 두 전도도가 가장 균형을 이루는 조성은 NCM83 약 40 %였다.
- 열전도도는 LPSCl 0.32 ± 0.02, NCM83 0.71 ± 0.04 W m⁻¹ K⁻¹였고, 복합전극은 계면 열저항(2×10⁻⁶ m² K W⁻¹) 때문에 조성에 거의 무관하게 낮은 값(<1 W m⁻¹ K⁻¹)에 머물렀다.
- VGCF <2 wt% 첨가로 전자 전도도는 두 자릿수 이상 올랐지만 열전도도는 거의 변하지 않았다.
- LiMn₂O₄–Li₃InCl₆, 다공성 LPSCl, PEO:LiTFSI:SiO₂ 문헌 데이터에도 같은 모델을 적용해 일반성을 보였다.

## 방법
- **시스템**: LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂ (≈2 µm) + Li₆PS₅Cl (≈20 µm) [+ VGCF]
- **기법**: voxel 기반 resistor network(300³, 2 µm/voxel), 반복 해법으로 정상상태 노드 전위/온도 계산, 계면 열저항 포함; 검증은 EIS·DC 분극(ion-/electron-blocking)
- **파라미터**: voxel 2 µm, 격자 300³, LPSCl voxel clustering(≈20 µm), 계면 열저항 2×10⁻⁶ m² K W⁻¹, NCM83 부피분율 스캔, VGCF 0~2 wt%
- **검증**: 자체 NCM83–LPSCl 실험(EIS, DC polarization) + 문헌 3건

> [!tip] 내 연구와의 연결
> **DEM** — 내 solver는 DEM 접촉 네트워크(입자–입자 접촉 면적·중첩)를 저항으로 바꾸는 방식이라, 이 논문의 voxel 방식과 '같은 조성에서 같은 유효 전도도를 주는가'를 비교하면 내 접근의 장점(접촉 물리 반영, 압력 의존성)을 정량적으로 주장할 수 있다. 특히 NCM 40 vol%에서 전자·이온 균형이라는 결과는 내 AM:SE 62:38/72:28/82:18 percolation 연구와 직접 맞닿는다.
> **DFT/MLIP** — 간접 연결. 계면 저항 개념을 내 W_ad(NCM/SE adhesion energy)와 연결해 '계면 접촉 품질 → 저항' 서사를 만들 수 있다.
> **Anode-free** — -

### 비교할 수치
- 유효 이온 전도도 10¹~10⁻⁵ mS cm⁻¹ (NCM83 부피분율 스캔) vs 내 resistor-network proxy (같은 AM:SE 비율로 환산)
- 전자·이온 균형 조성 NCM 40 vol% vs 내 percolation threshold (AM:SE 62:38~82:18, D_SE 0.5~3 µm)
- LPSCl 벌크 이온 전도도 입력값 vs 내 시뮬레이션에서 쓰는 SE 전도도 파라미터
- voxel 2 µm 해상도 vs 내 DEM 입자 0.5~3 µm — 해상도가 SE 네트워크 연결성 판정에 주는 영향

## 논문 작성에 쓸 곳
- **Introduction**: '복합전극 유효 전도도는 조성 공간이 넓어 실험만으로 최적화하기 어렵고, 저비용 네트워크 모델이 대안으로 제시됐다'는 문장의 근거. 이어서 'voxel 모델은 입자 접촉 물리와 압력 의존성을 담지 못한다'는 갭을 제시하며 내 DEM-native 접근을 도입.
- **Methods**: resistor network의 경계조건(양면 구배 + zero-flux)과 정상상태 해법을 동일하게 채택했음을 밝히고 인용. 계면 열저항 값은 향후 열 확장 시 초기값으로 사용.
- **Discussion**: NCM 40 vol% 균형점과 내 percolation threshold를 같은 그림에 놓고 '입자 크기비(NCM 2 µm vs SE 20 µm)가 바뀌면 균형점이 이동한다'는 점을 내 D_SE 스캔으로 보여준다.

> [!quote] 인용 문장 초안
> Resistor-network models built on voxelized microstructures reproduce the measured electronic, ionic and thermal conductivities of NCM83–Li6PS5Cl composites without heavy computation [ref], but they do not resolve particle-level contact mechanics, which the present DEM-based network addresses.

> [!warning] 비판 포인트 / 세미나 질문
> - voxel 배정이 확률적이라 실제 압축 후 미세구조(입자 변형, 접촉 면적)를 반영하지 못한다 — 압력 의존성이 없다.
> - LPSCl 입자를 voxel clustering으로 근사했는데 clustering 규칙이 결과(percolation)에 얼마나 민감한지에 대한 통계(반복 수)가 충분한지 확인 필요.
> - 실험 검증이 한 조성 계열(NCM83–LPSCl)에 집중돼 있고, 압력·온도 변화에 대한 검증은 없다.
> - 세미나 질문: '입자 크기비를 바꾸면 균형 조성(40 vol%)이 어떻게 움직이는가? 실험으로 확인했는가?'

## Follow-up
- [ ] 같은 조성(NCM 40~80 vol%)으로 내 solver를 돌려 유효 전도도–조성 곡선을 겹쳐 그리기
- [ ] SI에서 입력 전도도(σ_ion LPSCl, σ_e NCM83)와 격자 수렴성 확인
- [ ] 계면 열저항 2×10⁻⁶ m² K W⁻¹를 내 COMSOL 열 모델 초기값으로 등록

## 원문 초록
> Solid-state batteries use composites of solid ion conductors and active materials as electrode materials. The effective transport of charge carriers and heat thereby strongly determines the overall solid-state battery performance and safety. However, the phase space for optimization of the composition of solid electrolyte, active material, additive is too large to cover experimentally. In this work, a resistor network model is presented that successfully describes the transport phenomena in solid-state battery composites, when benchmarked against experimental data of the electronic, ionic, and thermal conductivity of LiNi0.83Co0.11Mn0.06O2-Li6PS5Cl positive electrode composites. To highlight the broadness of the approach, literature data are examined using the proposed model. As the model is easily accessible and expandable, without the need for high computing power, it offers valuable guidance for experimentalists helping to streamline the tedious process of performing a multitude of experiments to understand and optimize the effective transport of composite electrodes.

---
*related:* [[dem battery]], [[2026 - Kissel - Mechanofusion-derived cathode composite microstructures with scalable mixed]] · *digest:* [[2026-09-04]]

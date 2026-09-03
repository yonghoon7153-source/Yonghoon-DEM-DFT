---
title: "Mechanofusion-derived cathode composite microstructures with scalable mixed conducting matrix coatings for solid state batteries"
aliases: ["Mechanofusion-derived cathode composite microstructures"]
authors: ["Maximilian Kissel", "Finn Frankenberg", "Thomas Demuth", "Anton Lai", "Niklas Laser"]
journal: "Nature Communications"
year: 2026
doi: "10.1038/s41467-026-71305-2"
url: "https://www.nature.com/articles/s41467-026-71305-2"
if: 15.7
tier: "A"
relevance: 0.9
status: digested
keywords: ["dem battery"]
tags: ["paper/dem", "tier/A", "topic/mixing-process", "topic/percolation", "topic/coating", "material/halide-SE"]
source: bootstrap
date_added: 2026-09-03
analyzed_at: 2026-09-03
evidence_level: fulltext
ra_id: "doi:10.1038/s41467-026-71305-2"
---

# Mechanofusion-derived cathode composite microstructures with scalable mixed conducting matrix coatings for solid state batteries

**Maximilian Kissel, Finn Frankenberg, Thomas Demuth, Anton Lai, Niklas Laser** — *Nature Communications* (2026) · IF 15.7 · Tier A · 관련도 0.9
DOI: [10.1038/s41467-026-71305-2](https://doi.org/10.1038/s41467-026-71305-2)
키워드: [[dem battery]]

> [!abstract] 한 줄 요약
> Kissel et al.(Janek group)은 mechanofusion 고강도 건식 혼합으로 single-crystal NCM82 위에 Li₃InCl₆ 코팅(5 nm~100 nm)을 만들고, DEM으로 계산한 stress intensity(SI ∝ n²)와 코팅 피복률·공극률을 연결해 80:20:0.5(NCM:LIC:CB) 조성에서 1 C에서 100 mAh g⁻¹(복합전극 질량 기준)을 얻었다.

## 선정 이유
Nature Communications(IF 15.7)에 실린 2026년 논문이면서, 내 주축인 'DEM으로 composite cathode 미세구조를 설계한다'는 문제의식을 공정(혼합) 단계에서 다룬다. 내 DEM은 압축(compaction) 단계, 이 논문은 혼합 단계라 서로 보완적이고, DEM 결과를 실험 지표(피복률, 입도, 공극률)로 검증한 사례라서 내 porosity 보정·검증 논리의 근거로 바로 쓸 수 있다.

## 핵심 내용
- 코팅 함량 1~20 wt%, 회전속도 1,000~10,000 rpm, 혼합 5~60 min 조건에서 균일 코팅을 얻었고, XPS 피복률은 최고 함량에서 1.0에 근접했다(≥5,000 rpm, 5~10 min이면 97~100 %).
- DEM(coarse-graining)으로 계산한 stress intensity는 회전속도의 제곱에 비례(SI ∝ n²)했고, specific energy input이 커질수록 코팅이 두꺼워지고 피복률이 올라갔다.
- 복합전극 공극률은 코팅 함량과 혼합 강도가 커질수록 약 40 %에서 약 25 %로 떨어졌다(압축 후 기준).
- LIC 매트릭스에 carbon black을 넣으면 전자 percolation threshold가 2~5 wt% 사이에서 나타났고, 전자 부분 전도도는 <0.01 → ~1,000 mS cm⁻¹(0 → 15 % CB)로 올라간 반면 이온 부분 전도도는 ~0.7 → ~0.03 mS cm⁻¹로 떨어졌다.
- 80:20:0.5 조성에서 1 C에 100 mAh g⁻¹(복합전극 질량 기준), CB 과다(3 %)에서는 1 C 용량이 <10 mAh g⁻¹로 급락해 kinetics·chemo-mechanics 악화를 보였다(CAM 이용률은 65 → 90 %로 올라감).

## 방법
- **시스템**: single-crystalline LiNi₀.₈₂Mn₀.₀₇Co₀.₁₁O₂ (d₅₀ 3.3 µm) + Li₃InCl₆ (100 nm~100 µm) + carbon black (aggregate d₅₀ ≈ 250 nm)
- **기법**: Mechanofusion(고강도 건식 혼합, dry room −60 °C) + DEM coarse-graining으로 stress intensity(SI)·stress number(SN) 산출 + SEM/EDX, TEM/STEM, XPS 피복률, XRD Rietveld, SPED, 나노압입, DC 분극(ion/electron-blocking), CCCV 반쪽전지
- **파라미터**: 회전속도 1,000~10,000 rpm, 혼합 시간 5~60 min, 충전율 10 % (~20 g batch), 코팅 함량 1~20 wt%, CB 0~15 wt%, 조성 80:20:x (NCM:LIC:CB)
- **검증**: DEM 파라미터(SI, SN, energy input)를 실험 형태학(피복률, 입도분포, 공극률)과 상관시켜 검증; 전기화학 성능은 half-cell CCCV

> [!tip] 내 연구와의 연결
> **DEM** — 내 LIGGGHTS 압축 시뮬레이션은 '혼합이 끝난 분말'을 초기조건으로 가정한다. 이 논문은 그 초기조건(코팅 두께·피복률·응집)이 혼합 공정 변수에 따라 어떻게 달라지는지를 DEM으로 보여주므로, 내 bimodal AM/SE 초기 packing 생성 논리의 앞단 근거로 삼을 수 있다. coarse-graining DEM에서 SI ∝ n² 스케일링은 내 press_speed·E_eff 스케일 규약과 비교할 만한 무차원 접근이다.
> **DFT/MLIP** — 직접 연결은 약함. 다만 LIC(할라이드)의 malleability를 근거로 코팅이 형성되는데, 내 argyrodite B₀·G 계산 결과를 '황화물은 LIC보다 어떤 변형 거동을 보이는가'로 대비시켜 Discussion에 쓸 수 있다.
> **Anode-free** — -

### 비교할 수치
- 복합전극 공극률 40 → 25 % (코팅 함량·혼합 강도 증가) vs 내 RVE50/SE0.5 압축 케이스의 porosity–압력 곡선
- 전자 percolation threshold 2~5 wt% CB (LIC 매트릭스) vs 내 monomodal 연구의 AM:SE·D_SE 기반 percolation threshold (전도상 부피분율로 환산 필요)
- 이온 부분 전도도 0.7 → 0.03 mS cm⁻¹ (CB 0 → 15 %) vs 내 resistor-network solver의 유효 이온 전도도 proxy
- CAM 이용률 65~90 % vs 내 contact number 기반 활물질 접근성 지표

## 논문 작성에 쓸 곳
- **Introduction**: 'composite cathode 미세구조 최적화는 공정–구조–성능 연결이 핵심이며 DEM이 그 연결고리로 쓰이기 시작했다'는 문제 정의에 인용. 특히 '혼합 단계 DEM은 있으나 압축 단계의 percolation·porosity 정량은 부족하다'는 갭 서술에 활용.
- **Methods**: coarse-graining DEM과 stress intensity 개념을 언급하며, 내 시뮬레이션의 스케일 규약(radius ×1000, E ×0.001)이 무차원 응력 관점에서 정당함을 뒷받침하는 참고문헌.
- **Discussion**: porosity 25 % 근처에서 성능이 좋아졌다는 결과를 내 porosity–percolation 회귀 결과와 대비. CB 과다 시 chemo-mechanics 악화는 내 force chain/Von Mises 분석과 연결해 '전도 첨가제가 응력 전달 경로를 바꾼다'는 해석에 사용.

> [!quote] 인용 문장 초안
> Recent work has linked discrete element method (DEM)-derived stress intensities during high-intensity dry mixing to the resulting coating coverage and composite porosity of NCM/Li3InCl6 cathodes, underscoring that microstructure descriptors must be traced back to processing parameters [ref].

> [!warning] 비판 포인트 / 세미나 질문
> - DEM은 혼합 장치 내 응력 조건(SI, SN)만 계산하고 입자 단위 코팅 형성 자체는 모델링하지 않는다 — 코팅 두께는 실험 상관에 의존한다.
> - SE가 Li₃InCl₆(할라이드)라 황화물(LPSCl)보다 훨씬 무르고 산화 안정성이 높다. 같은 공정을 argyrodite에 적용하면 입자 파쇄와 계면 반응이 달라질 텐데 이 점은 다루지 않는다.
> - 용량은 복합전극 질량 기준 100 mAh g⁻¹(1 C)로, CAM 기준으로 환산하면 조성별 비교가 달라진다 — 세미나 질문: 'CAM 기준 이용률과 rate 성능의 trade-off를 어떻게 정량화했는가?'
> - 공극률은 압축 후 값인데 압축 압력·조건이 본문 요약에 명확히 드러나지 않는다 — SI/Methods 확인 필요.

## Follow-up
- [ ] SI에서 DEM 접촉 모델·입자 크기·coarse-graining 비율 확인 후 내 LIGGGHTS 설정과 비교표 작성
- [ ] 공극률 25~40 % 범위를 내 porosity regression 데이터(30-cell factorial)와 같은 축에 그려 보기
- [ ] LIC vs LPSCl 기계적 물성(내 DFT B₀, G) 비교 문단 초안 작성

## 원문 초록
> The successful implementation of solid state batteries not only requires the use of high-capacity anodes, but also high-performance composite cathodes. However, the production of solid state battery cathode composites with optimized microstructures remains a significant challenge, especially for large-scale fabrication. Here, we present a scalable high-intensity dry mixing process to create tailored functional coatings on single-crystalline LiNi0.82Mn0.07Co0.11O2 via mechanofusion. We investigate the coating of LiNi0.82Mn0.07Co0.11O2 with the malleable halide solid electrolyte Li3InCl6 under various process conditions, linking process parameters obtained from discrete element method simulations with experimentally accessible morphological properties to offer guidelines for further optimization. In this way nanometer-thin covering coatings as well as thick matrix coatings are successfully produced. Incorporating carbon black into the thick matrix coating results in well-performing mixed conducting matrices that can be used directly as composite cathodes without further treatment. The compositions investigated enable stable cycling with a specific capacity of up to qcomp = 100 mAh g−1 (based on the total mass of the composite cathode) at a C-rate of 1 C (60 min). While higher carbon black content is observed to improve CAM utilization, excessive amounts are detrimental for cell kinetics and chemo-mechanics, emphasizing the importance of the cathode mixing process and composition on overall cell performance.

---
*related:* [[dem battery]], [[2025 - Ketter - Using resistor network models to predict the transport properties of solid-state]] · *digest:* [[2026-09-04]]

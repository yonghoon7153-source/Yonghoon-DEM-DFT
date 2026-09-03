---
title: "Domain oriented universal machine learning potential enables fast exploration of chemical space of battery electrolytes"
aliases: ["Domain oriented universal machine learning potential"]
authors: ["Feng Wang", "Yu-Hang Tang", "Ze-Bing Ma", "Yu-Cheng Jin", "Jun Cheng"]
journal: "Nature Communications"
year: 2026
doi: "10.1038/s41467-025-67982-0"
url: "https://www.nature.com/articles/s41467-025-67982-0"
if: 15.7
tier: "B"
relevance: 0.45
status: digested
keywords: ["dft battery"]
tags: ["paper/dft", "tier/B", "topic/MLIP", "topic/transferability", "system/liquid-electrolyte"]
source: bootstrap
date_added: 2026-09-03
analyzed_at: 2026-09-03
evidence_level: fulltext
ra_id: "doi:10.1038/s41467-025-67982-0"
---

# Domain oriented universal machine learning potential enables fast exploration of chemical space of battery electrolytes

**Feng Wang, Yu-Hang Tang, Ze-Bing Ma, Yu-Cheng Jin, Jun Cheng** — *Nature Communications* (2026) · IF 15.7 · Tier B · 관련도 0.45
DOI: [10.1038/s41467-025-67982-0](https://doi.org/10.1038/s41467-025-67982-0)
키워드: [[dft battery]]

> [!abstract] 한 줄 요약
> Wang et al.(Xiamen Univ., Jun Cheng)은 2,300여 용매·20종 Li 염을 무작위 조합한 ~16만 구성의 DeePMD 기반 범용 MLIP(PBE-D3 라벨, 힘 RMSE ≈160 meV Å⁻¹)를 만들어 액체 전해질의 밀도(<5 % 오차)·이온 전도도·점도를 ns 규모 MD로 예측하고, Li⁺ 배위 수명(τ)을 용매화 세기의 정량 지표로 제안했다.

## 선정 이유
Nature Communications(IF 15.7)이고 키워드 'dft battery'에 잡혔지만 대상이 액체 전해질이라 내 황화물 SE 연구와 직접 연결되지는 않는다. 그래도 내 파이프라인의 DFT → MLIP(UMA/MACE) 단계에서 '학습 데이터를 어떻게 구성해 transferability를 확보하는가'라는 방법론적 질문에 좋은 참고가 돼 Tier를 유지하되 관련도는 낮게 둔다.

## 핵심 내용
- 전해질 생성기로 >2,300 용매 × 20 Li 염 조합에서 ~100만 계를 만들고, concurrent learning 91회 반복으로 ~160,000 구성을 PBE-D3로 라벨링해 DeepPot-SE 모델을 학습했다(원소: C, H, O, N, B, S, F, Cl, Br, I, P, Si).
- 에너지 RMSE ≈0.005 eV atom⁻¹, 힘 RMSE ≈160 meV Å⁻¹, virial ≈5 meV atom⁻¹; 밀도 오차 <5 %, 전도도 최대 농도 위치와 온도 의존성을 재현했다.
- Li⁺ 배위 수명 τ가 짧으면(<15 ps) 약한 용매화·높은 전도도, 길면(200~1,000 ps, 저온) 강한 용매화로 대응돼 τ가 용매화 세기의 직접 지표가 된다.
- LiTFSI/FAN, LiFSI/DMC, LiPF₆/EC-EMC 등 대표 전해질과 이온성 액체, 다가 양이온(Na⁺, K⁺, Mg²⁺, Ca²⁺, Zn²⁺)까지 재학습 없이 적용했다.

## 방법
- **시스템**: 액체 유기 전해질(카보네이트·에테르·나이트릴·헤테로고리·설폰 용매 + Li 염); 황화물/고체 전해질 없음
- **기법**: DeePMD(DeepPot-SE) 범용 MLIP, ai2-kit concurrent learning, PBE-D3 라벨, cutoff 6.0 Å; MD로 RDF·용매화 구조·확산계수(Nernst–Einstein 전도도)·Green–Kubo 점도·배위 수명 계산
- **파라미터**: ~160k 구성 / 91 iteration, cutoff 6.0 Å, PBE-D3, ns 규모 MD
- **검증**: 실험 밀도·전도도·점도와 비교

> [!tip] 내 연구와의 연결
> **DEM** — -
> **DFT/MLIP** — 내 MLIP 단계(UMA/MACE fine-tuning)에서 학습 데이터 편향 문제를 다룰 때, '무작위 조성 + concurrent learning'으로 transferability를 확보한 사례로 인용할 수 있다. 특히 argyrodite 할로겐 치환 계열(Cl/Br 비율, Li 결손)을 스캔할 때 조성 공간을 무작위로 샘플링해 학습하는 전략을 그대로 적용해 볼 수 있다. 힘 RMSE 160 meV Å⁻¹는 액체계 기준이라 내 고체계 목표(수십 meV Å⁻¹)와 비교해 오차 허용 범위를 정하는 참고치가 된다.
> **Anode-free** — -

### 비교할 수치
- 힘 RMSE ≈160 meV Å⁻¹, 에너지 RMSE 0.005 eV atom⁻¹ vs 내 UMA/MACE fine-tuning 검증 오차(argyrodite EOS·탄성상수 재현 기준)
- 학습 구성 수 ~160k vs 내 MLIP screening에 쓴 DFT 구성 수

## 논문 작성에 쓸 곳
- **Introduction**: 'MLIP의 transferability 한계와 이를 데이터 구성 전략으로 극복하려는 흐름'을 소개하는 문장에 인용.
- **Methods**: MLIP 검증 지표(에너지/힘/virial RMSE)를 보고하는 방식의 참고.
- **Discussion**: 

> [!quote] 인용 문장 초안
> Universal machine-learning potentials trained on randomly composed chemical spaces have recently reached ab initio accuracy across broad electrolyte families [ref], motivating a similar data-diversity strategy for sulfide solid electrolytes.

> [!warning] 비판 포인트 / 세미나 질문
> - 고체 전해질·계면은 학습 범위 밖이라 내 시스템에 바로 쓸 수 없다 — 'universal'의 범위가 액체 유기 전해질에 한정된다.
> - 힘 RMSE 160 meV Å⁻¹는 고체 탄성상수·포논 계산에는 부족한 정확도다.
> - PBE-D3 라벨의 한계(용매화 에너지 과대/과소)가 그대로 MLIP에 전파된다 — 세미나 질문: 'functional 선택이 τ 같은 동역학 지표에 주는 영향은?'

## Follow-up
- [ ] 내 MLIP 학습 데이터 구성 문서에 '무작위 조성 샘플링 + concurrent learning' 항목 추가 검토
- [ ] MLIP 검증 오차 표(에너지/힘/virial)를 내 논문 SI 양식으로 정리

## 원문 초록
> Li-ion batteries, widely used in electronic devices, electric vehicles, and aviation, demand high energy density, fast charging capabilities, and broad operating temperature ranges. Computations combined with experiments have gained increasing attention for electrolyte development. However, the inherent complexity of electrolytes poses a significant challenge. Classical molecular dynamics often fails due to inaccuracies in force field parameters, while ab initio calculations are limited by high computational costs. Recently, machine learning molecular dynamics has emerged as an efficient and accurate alternative. However, its application is hindered by limited transferability of machine learning potentials. In this work, we developed a universal machine learning potential for electrolytes using an iterative training approach on randomly composed datasets, enabling the accurate computation of key properties for a broad range of electrolytes via molecular dynamics. Furthermore, coordination dynamics analysis of Li ion, by quantifying the coordination lifetime, provides a direct, quantitative measure of solvation strength. The universal machine learning potential for electrolytes facilitates the prediction and optimization of electrolyte properties, offering a powerful tool for electrolyte design.

---
*related:* [[dft battery]] · *digest:* [[2026-09-04]]

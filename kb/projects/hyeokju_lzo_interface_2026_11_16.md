---
title: "[혁주] LZO 코팅 양극 계면 — 요청 요약과 계산 계획"
date: 2026-11-16
updated: 2026-11-17
tags: [hyeokju, LZO, Li2ZrO3, NCA, LPSCl, interface-reactivity, band-gap, MLIP-MD]
status: 진행 — 1 단계 · 2a active (사용자 승인 11-16) · MD proposed (문턱 승인 대기) · 혁주 자료 대기 (조성 · 전압 기준 · 충전 용량)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: single-source
---

# [혁주] LZO 코팅 양극 계면 — 요청 요약과 계산 계획

## 트랙

- 이름: **[혁주]** (용훈 포메이션의 절 이름 · 사용자 2026-11-16 *"이것도 [혁주] section으로 정의하고 관련해서 dft, md 관련해서 진행해보자"*).
- 요청자 = 혁주 (실험 · 원고 쪽) · 사용자 = 계산 담당.
- 1저자: **혁주** (사용자 확인 2026-11-16). 계산 쪽 결정은 '사용자' 로 적는다 (CEI 와 같은 꼴).
- 원본: Google Docs 'LZO_계면_DFT_계산_협의_그림추가' 인쇄본 사진 3 장 (1–3/4 쪽 · **4 쪽은 못 봤다**) · 사용자 2026-11-16 전달.

## 요청 요지 (1–3 쪽)

- **계**: LZO 코팅 NCA721 · NCA811 양극 | Li₆PS₅Cl. 상대전극 Li–In · 45 °C · 100 MPa. 화성은 0.1C 2 회이고 상한 전압을 바꾼다. 뒤 사이클은 0.5C · 2.5–4.4 V. 전압의 Li/Li⁺ 환산 여부는 혁주가 확인한다.
- **목표**: 화성 중 충전 상태가 달라질 때 코팅 양쪽에서 가능한 반응을 보고, XPS 해석 근거를 얻는다. 단일 셀 결과와 dQ/dV 만으로는 계면 열화 원인을 확정하기 어렵다.
- **1 단계 부탁**:
  - ① NCA–LZO ② LZO–Li₆PS₅Cl 의 열역학적 반응에너지와 생성물. 기존 NCA–Li₆PS₅Cl 직접 접촉 계산을 대조군으로.
  - 초기 NCA 와 화성 상한 3.8 · 4.4 V 에 해당하는 Li 함량을 비교. Mid-Ni 먼저, 계산량이 허용되면 High-Ni.
  - 벌크 에너지 기반 반응성 평가가 먼저. 명시적 계면 모델과 AIMD 는 필요성과 비용을 본 뒤.
- **받고 싶은 최소 결과**: 혼합 비율별 반응에너지 곡선 · 주요 반응식 · 생성물 (같은 에너지 기준 · 정규화) · Li 함량 또는 μ_Li 조건별 경향의 짧은 해석 (조성 · 전압 · 평형 가정 명시) · 2 단계 대표 물질 1–2 개 추천 (XPS 관련성).
- **참고 그림**: Banerjee 2019 *ACS Appl. Mater. Interfaces* Fig. 4 (LPSCl–NCA · LPSCl–LNO 혼합 반응에너지 · AIMD) 와 Fig. 8 (코팅 물질 표). 문헌의 코팅은 LiNbO₃ 라 LZO 와 다르다. **우리 litdb 에 없다.** ⏩ **11-17 확인** (litdb `banerjee2020_interfaces_interphases_assb_review` · 그림 직접 봄): 두 그림은 원전 Banerjee 2019 *ACS AMI* 11, 43138 (= Banerjee 2020 *Chem. Rev.* 리뷰의 ref 51) 의 것이고, 리뷰에 **Fig. 18a** (NCA–LPSCl · LiNbO₃–LPSCl pseudo-binary · 세로축 **eV/f.u.** — 원자당이 아니라 우리 meV/atom 곡선과 깊이를 견주지 않는다) 와 **Fig. 17** (코팅 선별 다섯 기준 · Li₂ZrO₃ 는 이온전도도 10⁻⁴ S/cm (598 K) · 띠틈 3.99 eV 칸에만 있고 반응에너지 · 창 칸에는 없다) 로 다시 실렸다. 요청서의 'Fig. 4 · 8' 은 원전의 그림 번호로 보인다 (원전 PDF 없음 · 추정). AIMD 는 리뷰 본문 한 줄뿐이다 (그림 없음). 원전은 여전히 litdb 에 없다 (리뷰 참고문헌 지도의 다음 인입 1 순위 · 위시리스트에 올릴지는 사용자).
- **2 단계**: LZO 와 생성물 1–2 개의 band gap · DOS/PDOS · 계산 조건 · 정량값의 한계. 계산법과 보정 필요성은 상의. Li⁺ 이동성은 별도 질문.
- **혁주가 줄 자료**: 정확한 NCA · LZO 조성 · 코팅 두께 · 함량 · 결정성 · 전압 기준 · 화성 충전 용량 · 기존 계산 파일. 충전 용량에 부반응이 섞일 수 있어 Li 함량 환산 오차도 같이 검토해 달라고 했다.
- **혁주 문서가 스스로 그은 선** (그대로 지킨다): 계산은 열역학적 가능성과 생성물 후보까지다. 속도 · 생성량 · LZO 보호 효과는 실험과 함께 판단한다. 두 계면을 따로 계산한 결과로 코팅 전체의 차단 효과를 증명할 수 없다. Band gap 은 산화 안정 전압과 같지 않고 전도도 · 누설전류 · 보호 효과를 단독으로 정하지 않는다.

## 계산 계획

| 단계 | 카드 · 결정 | 무엇 | 어디서 |
|---|---|---|---|
| 1 열역학 | `db/properties/hyeokju_lzo_stage1_reactivity_card_2026_11_16.json` · `D-2026-11-16-hyeokju-lzo-stage1-reactivity` (**active** 11-16) | 닫힌계 혼합 곡선 (양극 Li 함량 y = 1.0 … 0.1) + Li 열린계 (2.5–5.0 V) · 대조 NCA–LPSCl · 앵커 LPSCl×LCO | gabia CPU · MP 조회 |
| 2a 전자구조 | `db/properties/hyeokju_lzo_stage2a_li2zro3_gap_card_2026_11_16.json` · `D-2026-11-16-hyeokju-lzo-stage2a-li2zro3-gap` (**active** 11-16 · vc-relax 허락) | Li₂ZrO₃ fixed-occ nscf 띠틈 + DOS/PDOS · CEI 생성물 띠틈 체인 | kgy GPU · 작은 셀 |
| MD | `db/properties/hyeokju_lzo_md_card_2026_11_16.json` · `D-2026-11-16-hyeokju-lzo-md` (proposed · G1 · G2 문턱 승인 대기) | UMA 검증 (DFT 단일점 대조) → 1 단계가 고른 계면 MD | kgy GPU |

### 혁주 자료가 오기 전과 뒤

- **전**: 이름 그대로의 조성 (NCA721 = LiNi0.7Co0.2Al0.1O2 · NCA811 = LiNi0.8Co0.1Al0.1O2 — 추정) 과 Li₂ZrO₃ 로 y 격자 · 전압 격자 전체를 미리 낸다. 3.8 · 4.4 V 라벨은 붙이지 않는다.
- **뒤**: 조성이 추정과 다르면 (전이금속 분율 0.02 초과) 다시 돈다. 3.8 · 4.4 V → y 는 y = 1 − Q_ch / Q_theo 로 바꾸고, 부반응 몫은 혁주 오차 (없으면 ±0.05) 로 띠를 그린다. 전압 기준이 Li–In 이면 +0.62 V 로 Li/Li⁺ 로 옮긴다 (혁주 값이 있으면 그것). ⏩ **11-17**: 전압은 Li/Li⁺ 기준 (사용자 확인) — Li–In 환산 없음.

## 우리 쪽에 이미 있는 것 (규약 대조)

- 같은 계산틀: cascade M6 (코팅 × LCO/LNO 만충 · 반충 · Xiao 2019 F4 정의) · `db/properties/cathode_reactivity_cascade.csv` · LPSCl×LCO 앵커 (`cathode_reactivity_verdict.json`).
- cascade NCM 축 카드 `db/properties/cascade_axis_ncm_interface_estimand_2026_11_04.json` — 도핑 조성 · 반충 대리 조성을 hull 에너지로 처리하는 관례와 MP 띠틈 등급 규칙.
- 계보 `kb/syntheses/cathode_coating_computational_lineage.md` — #4 Nolan 2019 의 E_d 가 우리 닫힌계 값과 같은 양 · 같은 구현.
- 띠틈 체인: `db/properties/cei_product_gap_card_2026_10_27.json` (+ 개정 1) — fixed-occ nscf · 60/480 Ry · PP 세트. Zr PP 는 이 세트에 없다 (2a 에서 정한다). 비-argyrodite 결정의 vc-relax 는 사용자 허락으로만 (CLAUDE.md 이완 규칙).
- MD: LPSCl 계열 UMA 는 검증된 표준이다. Li₂ZrO₃ 와 NCA (Ni · Co) 는 우리 검증이 없다.
- '기존 NCA–Li₆PS₅Cl 직접 접촉 계산' 은 혁주가 말한 '기존 preview' 일 수 있다 — 혁주가 파일을 주면 같은 실행 값과 대조한다.

## 열린 질문

- 4 쪽 내용 (사진에 없음).
- NCA721 · NCA811 의 실제 Ni:Co:Al.
- ~~3.8 · 4.4 V 와 2.5–4.4 V 가 Li–In 기준인지 Li/Li⁺ 기준인지.~~ → ✅ **Li/Li⁺ 기준** (사용자 2026-11-17 *'Li/Li+ 기준이얌'*) — Li–In +0.62 V 환산을 하지 않는다. 열린계 전위 격자 (2.5–5.0 V vs Li/Li⁺) 와 같은 축이다. y 에 3.8 · 4.4 V 라벨을 붙이는 건 여전히 화성 충전 용량 대기 (G5).

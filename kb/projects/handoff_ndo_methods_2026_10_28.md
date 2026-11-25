---
title: "NdO-LPSCl₁.₆ 원고 계산 부분 인계 — Methods 두 판 · Fig. 3h · Fig. 5e,f · Fig. SX (2026-10-28)"
date: 2026-10-28
updated: 2026-10-28
tags: [handoff, ndo, cei, manuscript, methods, band-gap, interface]
status: 발송 대기 — 사용자가 Word 둘 · CSV 둘과 같이 전달한다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-28
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---


# NdO-LPSCl₁.₆ 원고 — 계산 부분 인계 (2026-10-28)

> 이 카드는 원고를 받는 쪽 (실험 쪽 1저자) 을 위한 거예요. 계산 담당이 쓴 4.5 절 Methods 두 판과 그림 값 두 묶음을 같이 보내요.
> 숫자는 전부 계산 쪽 원장에서 옮겼고, 아래 **'쓸 때 지킬 것'** 은 그 원장의 인용 규칙이에요.
> 기준: 브랜치 `claude/friendly-meitner-lldvar` · 이 카드가 들어간 커밋.

## 0. 한 줄 요약

4.5 절 DFT calculations 를 본문용 (짧은 판) 과 SI 용 (전체 판) 으로 썼어요. 원고에서 손댈 곳은 셋이에요 —
**Fig. 3h** 막대 · 숫자를 우리 QE 값으로 바꾸고, 빈칸인 **Fig. 5e,f** 와 **Fig. SX** 를 아래 값과 단서로 채우면 돼요.
Methods 에는 결과 값이 없어요 (계산 설정만).

## 1. 보내는 파일

| 파일 | 무엇 | 어디에 |
|---|---|---|
| `ndo_lpscl16_methods_main_2026_10_28.docx` | 4.5 절 본문판 (약 450 단어 · 참고문헌 14) | 원고 4.5 절 자리 |
| `ndo_lpscl16_methods_SI_2026_10_28.docx` | SI Computational details (약 800 단어 · 식 S1–S3 · 참고문헌 15) | SI |
| `ndo_fig3h_sei_gaps_qe_origin.csv` | Fig. 3h 막대 값 다섯 (우리 QE · 원고 막대 순서) | Fig. 3h · 결과 문단 숫자 |
| `ndo_fig5ef_reaction_energy_origin.csv` | Fig. 5e,f 값 (NCM811 × 두 SE · 여섯 전압 · 최소 반응식 · Nd 산물) | Fig. 5e,f |
| 이 카드 | 할 일 · 단서 | — |

CSV 는 Origin 에 바로 넣을 수 있게 열 이름을 적었어요 (`*_origin_label` 열 = Origin 아래첨자 표기). 첫 줄 (`#`) 에 출처와 읽는 법이 있어요.

## 2. 원고에서 바꾸거나 채울 곳

### 2-1. Fig. 3h — SEI 성분 띠틈 (값 바꿈)

- 지금 원고의 막대와 결과 문단 숫자는 Materials Project 데이터베이스 값이에요. Methods 는 우리 QE 계산 (PBE · 고정 점유 nscf 고유값) 으로 썼으니,
  **막대와 결과 문단 숫자를 CSV 값으로** 바꿔 주세요: Li₂S 3.44 · Li₃P 0.71 · Li₂O 4.99 · β-Li₃PO₄ 5.91 · LiCl 6.26 eV.
- 역할 구분 (넓은 띠틈 · 중간 · 전도성) 은 MP 값일 때와 같아서 문장 흐름은 안 바뀌어요.
- PBE 는 띠틈을 작게 잡아요. 그래서 이 값은 **상끼리 비교**에 쓰고 실험 띠틈 값과 나란히 두지 않아요 (Methods 에도 한 줄 있어요).

### 2-2. Fig. 5e,f — 계면 반응에너지 대 전압 (빈칸 → CSV)

- Methods 는 NCM811 × LPSCl₁.₆ · NdO-LPSCl₁.₆ (원고 조성 Li₅.₄₄Nd₀.₀₂P₀.₉₈S₄.₃₇O₀.₀₃Cl₁.₆) 를 2.5 · 3.0 · 3.5 · 4.0 · 4.3 · 4.5 V 에서 잰 걸로 썼어요.
  다른 양극이나 조성을 그리면 Methods 문장을 넓혀야 하니 알려 주세요.
- 값은 Materials Project 에너지 (MP2020 보정 포함) 로 낸 거예요 — 우리 QE 계산이 아니에요. 단위는 Li 를 뺀 원자당 eV 예요.
- **쓸 때 지킬 것** (계산 쪽 원장):
  - 두 SE 의 반응에너지 차이는 x = 0.02 에서 이 방법의 구분폭 (±0.010 eV/atom · 양극 · 전압 전 칸 평균) 안이에요.
    그래서 차이의 **크기를 인용하지 않고**, 부호도 *'NdO-LPSCl₁.₆ 가 덜/더 반응한다'* 나 순위로 읽지 않아요.
  - 말할 수 있는 건 **산물**이에요. NdO-LPSCl₁.₆ 에서는 Nd 가 인산염으로 가요 — 전압이 오를수록
    NdPO₄ (2.5 · 3.0 V) → LiNd(PO₃)₄ (3.5 V) → Nd(PO₃)₃ (4.0 V) → NdP₅O₁₄ (4.3 · 4.5 V).
    결과 문단의 *'formation of an Nd-containing CEI is thermodynamically favorable in the high-voltage region'* 과 맞아요.
  - Nd 가 가져가는 P 는 최대 1 할 (4.3 · 4.5 V 의 NdP₅O₁₄) 이에요. 고전압에서 나머지는 무도핑처럼 양극 전이금속 인산염으로 가요.
  - 반응에너지는 반응 전 SE 와 NCM 을 기준으로 재서, 각자 그 전압에서 혼자 분해되는 몫도 들어 있어요. 여섯 점 모두 최소가 중간 혼합비라 SE–NCM 이 같이 반응한 값이에요.
  - 0 K 열역학이라 최종 평형 산물이지 순서 · 속도가 아니에요.

### 2-3. Fig. SX — Nd 함유 CEI 성분 띠틈 (빈칸)

- 결과 문단 빈칸 *'The Nd-containing CEI component [ ] exhibited a calculated band gap of [ ] eV (Fig. SX)'* →
  **NdP₅O₁₄ · 5.39 eV** (우리 QE · PBE · *Pmna* mp-560681). Fig. 5e,f 의 고전압 Nd 산물과 같은 상이에요.
- 이 값을 쓰면 캡션이나 SI 에 아래 한 줄을 같이 넣어 주세요 (계산 쪽 원장 규칙):
  *"The Materials Project band gap of this entry (6.34 eV) was obtained with r2SCAN and is therefore not directly comparable with our PBE value; the GGA band gap of a related P2₁/c entry (mp-4736), 5.39 eV, provides only an auxiliary comparison."*
- 그림 값은 9 월에 보낸 CEI 화면 묶음의 `cei_gap_briefing_origin_2026_09_28.csv` 에도 같은 값으로 있어요.
- 요청하신 **CEI 생성물 11 종 띠틈** (이 그림 아래) 은 지금 계산 중이에요 (12 개 중 6 개 끝). 끝나면 값과 함께 Methods 문단
  (전이금속 화합물의 스핀 · U 설정) 을 더해 보낼게요. 그때 Fig. SX 문장도 여러 상으로 넓혀요.

### 2-4. Fig. 3f,g — Li 이동 장벽 (바꿀 것 없음)

- Methods 는 실제 계산 설정대로 썼어요 (Li₂S 3 × 3 × 3 · 음전하 Li 공공 / Li₃Nd 2 × 2 × 2 · 중성 Li 공공 · CI-NEB).
- SI 3 문단의 Li₃Nd 모델 설명 (가상의 정렬 구조 · 끝점 재배열 · 셀 크기에 수렴 안 됨) 은 계산 쪽 필수 문장이라 그대로 둬 주세요.

## 3. 참고문헌 · 형식

- 원고 [1] 과 같은 Elsevier 꼴이에요 — 문장부호 앞 [n] · *저자, 제목, 저널 권 (연도) 쪽. DOI.*
- 번호는 파일마다 처음 인용 순서예요 (본문판 1–14 · SI 판 1–15). 원고 목록에 합칠 때 다시 매겨 주세요. 본문판에는 SI 에서만 쓰는 Marzari–Vanderbilt 문헌이 없어요.
- *'Fig. SX'* · *'Supplementary Material'* 은 원고 자리표시 그대로 뒀어요. NCM · SEs · CEI 는 원고 앞에서 정의한 약어를 그대로 썼어요.
- 붙여 넣은 뒤 아래첨자 · 이탤릭 · 마이너스 기호를 한 번 봐 주세요.

## 4. 계산 쪽 기록 (참고)

- Methods 원문 · 문장별 근거 · 독립 검토 반영 표: `kb/papers/ndo_lpscl16_methods_2026_10_28.md`
- 실행 입력 대조 (gabia · 10-28): `db/raw/ndo_methods_2026_10_28/gabia_check_1_2026_10_28.log`
- 원장: Fig. 3h `db/properties/sei_electronic.json` · Fig. 5e,f `db/properties/cei_interface_V_x002_2026_09_28.json` (읽는 법 `cei_x002_result_2026_09_28.json`) · NdP₅O₁₄ `db/properties/cei_gap_results_2026_09_19.json`
- 이전 CEI 인계 카드 (09-30): `kb/projects/handoff_cei_2026_09_30.md`

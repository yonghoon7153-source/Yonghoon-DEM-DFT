---
title: "산화 · 환원은 어디서 먼저 일어나나 — free S²⁻ (VBM) · P–S σ* (CBM) · Li₃PO₄ 두 경로"
date: 2026-11-09
updated: 2026-11-09
tags: [oxidation, reduction, vbm, cbm, free-s, ps3o, antibonding, sigma-star, cohp, site-pdos, li3po4, grand-potential, li-metal, kang2026, reading-guide]
status: 확정 (개념 카드)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-mixed
---

# 산화 · 환원은 어디서 먼저 일어나나 — free S²⁻ · P–S σ\* · Li₃PO₄

> [!info] 이 카드가 답하는 질문 (사용자, 2026-11-09)
> [Kang 2026](/paper/kang2026_site_specific_customized_se_dendrite_tolerant_li_metal) (*site-specific customized SE*) 의 문장 17 — *"this contraction … stabilizes the anion framework through the formation of more stable PS₃O tetrahedra, thereby enhancing the electrochemical stability"* — 을 같이 읽다가 나온 질문 셋이에요.
> ① **"4c·4d 에 있는 S 가 먼저 반응할 거 같은데 DOS 도 그렇고 — 이런 문장이 어떻게 성립하나? 시뮬레이션으로 설명해줘"**
> ② **"CBM 이 P–S 반결합 궤도라 전자가 들어오면 P–S 가 끊긴다 — 더 설명해줄 수 있나? Li metal ASSB 면 중요할 것 같은데"**
> ③ **"산화돼서 Li₃PO₄ 가 나오는 거랑 환원돼서 Li₃PO₄ 가 생기는 거랑 화학식 · 메커니즘이 어떻게 다른가"**

세 질문은 한 그림으로 풀려요. 산화는 전자를 **빼는** 일이라 채워진 띠의 맨 위 (VBM) 에서, 환원은 전자를 **넣는** 일이라 빈 띠의 맨 아래 (CBM) 에서 시작해요.
그 두 자리에 누가 앉아 있는지가 답이에요.

그림 안 글자는 하우스 규약대로 영어예요. 그림은 `tools/figures/build_se_redox_frontier_figures.py` 가 만들어요 (`docs/figures/se_redox_frontier/` · `--selftest` 음성 5 경우).
데이터 그림 둘의 Origin CSV 는 `db/properties/se_redox_frontier_cohp_per_bond_origin.csv` · `db/properties/se_redox_frontier_o_only_profile_origin.csv` 예요.

---

## 1. 출발점 — 위에서 빼고, 아래에 넣어요

![Where oxidation and reduction start](/api/file/docs/figures/se_redox_frontier/rf_01_frontier_map.svg)

- **산화**: 채워진 전자 중 가장 얕은 (에너지가 높은) 것부터 빠져요. 그래서 VBM 에 앉은 원자가 먼저 반응해요.
- **환원**: 들어온 전자는 빈 상태 중 가장 낮은 곳 (CBM) 으로 가요. 그래서 CBM 을 이루는 결합이 먼저 반응해요.
- ⚠ 이 그림은 **어느 자리가 먼저인지**를 보는 그림이에요. 몇 V 에서 일어나는지는 열역학 (grand-potential) 이 정해요 — 띠틈이 곧 전기화학 창은 아니에요 ([띠틈 카드](/concept/bandgap)).

---

## 2. 산화 — free S²⁻ 가 먼저예요 (질문 ①)

### ① 자리별 PDOS 로 보면

P 에 안 붙은 S²⁻ (4a·4d 자리 — 논문마다 4c·4d 로 이름이 갈려요) 는 결합에 안 묶인 고립 전자쌍이라 얕아요.
PS₄ 안의 S 는 P–S 결합에 묶여서 1 eV 넘게 깊어요.

![Site-resolved p-states of the B2O3-doped model](/api/file/docs/figures/se_redox_frontier/rf_02_site_pdos.svg)

자리별 p 상태의 평균 에너지 (VBM 기준 · −8..0 eV 창 · 그림 창과 같은 창) 는 이래요. 출처는 `db/properties/site_pdos_mean3p_summary.csv` 예요.

| 전자 | B₂O₃ 도핑 모델 | 무도핑 LPSCl1.6 | 뜻 |
|---|---|---|---|
| free S²⁻ 고립쌍 | −1.14 eV | −0.90 eV | 가장 얕음 = 산화 시작 자리 |
| BS₃ 안의 S | −2.15 eV | — | 도핑이 만든 결합 |
| PS₄ 안의 S | −2.23 eV | −2.25 eV | 호스트 · 도핑 전후 같음 |
| Cl | −2.99 eV | −2.83 eV | 깊음 |
| O (P 에 붙은 O) | −3.64 eV | — | 가장 깊음 |

B₂O₃ 도핑 모델에서 O 는 P 에 붙어 있어요 (P–O 결합). 그래서 PS₃O 류 사면체의 O 가 어디에 놓이는지 보는 데 쓸 수 있어요.
O 가 만드는 전자 (P–O 결합 · O 고립쌍) 는 전부 free S 보다 깊어요. **새 약점을 안 만드니까 첫 산화도 안 바뀌어요.**

### ② grand-potential 도 같은 말을 해요

- O 만 넣은 대조 조성 (Li₅.₄PS₄.₁O₀.₃Cl₁.₆) 의 산화 개시가 같은 상 집합의 무도핑 (comp1 · modelc) 과 **같았어요** (차이 0 · 한 점 · `db/properties/cei_esw_Li_controls_2026_09_16.json`).
  규약: 이 값들은 grand-potential 경계의 Li-rich facet 값이에요. 문헌 값과 견줄 때는 다음 breakpoint 를 같이 적어요 (`HZ-esw-reduction-limit-facet-convention`).
- B₂O₃ 도핑도 산화 개시가 거의 그대로였어요 (−0.1 V 남짓 · [전자 국소화 틀](/kb?path=kb/methodology/electron_localization_framework_2026_07_08.md) §4).
- Kang 의 CV 겉보기 개시도 LPSC → LPSOC 에서 0.1 V 쯤만 움직여요 (`figure-read ≈` · Kang 정리본 §7b ⑤).
- 그리고 이 개시 전압은 **우리 셀 작동창 (2.5–4.25 V vs Li) 아래**예요. 셀이 도는 동안 SE 는 늘 열역학적 산화 구간에 있어요 (4 장 ④).

### ③ 그럼 문장 17 은 무엇에 기대나

Kang 2026 은 원자 단위 계산을 하지 않았어요. "PS₄₋ₙOₙ 강화" 의 근거는 인용 [29,30] 이 전부예요 (정리본 §4e).
이런 문장이 흔히 쓰이는 근거는 셋인데, 셋 다 **첫 산화와는 다른 양**이에요.

- **(a) 결합 세기** — P–O 가 P–S 보다 훨씬 강해요 (결합당 ICOHP P–O −8.6 · P–S −6.0 eV · `docs/figures/icohp/b2o3_icohp_summary.csv`). "더 안정한 사면체" 는 이 뜻이에요. 결합이 강한 것과 그 사면체가 먼저 산화되느냐는 다른 질문이에요.
- **(b) 분해 산물** — O 가 있으면 산화 산물에 Li₃PO₄ 가 섞여요 (4 장). Li₃PO₄ 는 띠틈이 넓은 절연체라 분해층이 전자를 막고, 분해가 스스로 멈춰요. 실험 CV 에서 창이 넓어 보이는 건 대개 이 효과예요 — 열역학 개시가 아니라 동역학이에요.
- **(c) 평균으로 낸 지표** — S 의 p-band center 를 '모든 S 평균' 이나 '사면체 S 만' 으로 내면 O 치환이 값을 바꿔요. 그런데 첫 산화를 정하는 free S 는 그 평균에 묻혀요. 예: Liu 2024 (*Adv. Funct. Mater.*) 는 사면체 S 만 계산했고 free S 와 PS₄ 안의 S 를 나누지 않았어요.

> [!note] 방어할 수 있는 읽기
> *"강한 P–O 결합이 골격 (P 에 묶인 부분) 의 분해 경로와 산물을 바꾸고, 그 산물 (Li₃PO₄) 이 계면을 막아 겉보기 안정성이 좋아진다."*
> **"산화 개시가 늦춰진다" 는 뜻은 아니에요.** 덧붙여 이 논문의 '격자 수축' 도 근거가 약해요 — XRD 봉우리 이동이 Rietveld 격자 상수 변화의 약 5 배라서 정리본에서 수축의 정량 근거로 쓰지 않았어요.

### ④ 계산으로 이 문장을 제대로 세우려면

1. **정공 국재 계산** — 전자를 하나 뺀 셀에서 빈자리 (정공) 가 어느 원자에 모이는지 봐요. PBE 는 정공을 넓게 퍼뜨려서 hybrid 가 필요해요. free S 에 앉으면 O 효과는 없는 거예요.
2. **자리별 산화 에너지** — PS₃O 옆 free S 와 먼 free S 에서 S⁰ (또는 S–S) 를 만드는 에너지를 비교해요. 격자 수축 효과가 있다면 여기서 보여요.
3. **O 함량을 바꾼 grand-potential** — 개시 전압 · 두 번째 단계 · 산물을 같이 봐요.
4. **산물의 띠틈과 계면 잔류** — Li₃PO₄ 가 계면에 남아 전자를 막는지 봐요.

문헌은 보통 (a) 나 (c) 만 하고 끝내요. 그래서 이 문장이 '통상' 이 됐어요. 사이트 수준에서 free S 와 PS₄ 의 S 를 가르는 건 hull 계산이 원리적으로 못 하는 일이기도 해요 ([산화 vs 기계 카드](/concept/oxidation_vs_mechanical)).

---

## 3. 환원 — 반결합 궤도가 차면 결합이 끊겨요 (질문 ②)

### ① 결합 궤도와 반결합 궤도

깨지는 건 반결합 궤도가 아니에요. **반결합 궤도에 전자가 차서 결합이 깨지는 거예요.**

![Filling an antibonding orbital breaks the bond](/api/file/docs/figures/se_redox_frontier/rf_03_bond_order.svg)

- 두 원자가 결합하면 궤도가 둘로 갈라져요. 아래쪽 **결합 궤도 σ** 는 전자가 두 원자 사이에 모여 둘을 붙여요. 위쪽 **반결합 궤도 σ\*** 는 두 원자 사이에 마디가 있어서, 전자가 들어가면 오히려 둘을 밀어내요.
- **결합 차수 = (σ 전자 − σ\* 전자) / 2.** P–S 결합은 σ 에 전자 2 개, σ\* 는 비어 있어서 차수 1 이에요.
- σ\* 에 전자 2 개가 들어가면 차수가 (2 − 2)/2 = 0 이 되고 결합이 끊겨요. S 는 S²⁻ 로 떨어져 나가 Li₂S 가 되고, P 는 전자를 받아 산화수가 내려가요.
- 끝까지 가면 **Li₃PS₄ + 8 Li → Li₃P + 4 Li₂S** 예요. P 가 +5 에서 −3 이 되니까 전자 8 개가 들어간 거예요.
- 겹침이 강한 결합일수록 σ 는 더 깊고 σ\* 는 더 높아요. 그래서 강한 결합은 **두 번** 보호돼요 — 전자를 빼기도 어렵고 (산화), 넣기도 어려워요 (환원).

### ② 우리 계에서 CBM 은 P–S σ\* 예요

COHP 는 원자 쌍마다 상태를 결합 (+) · 반결합 (−) 으로 나눠 보는 분석이에요 ([COHP 카드](/concept/cohp)). 그 빈 쪽을 보면 누가 환원 전자를 받는지 보여요.

![Per-bond COHP on the empty side](/api/file/docs/figures/se_redox_frontier/rf_04_cohp_unoccupied.svg)

- 띠 가장자리 바로 위의 빈 상태는 **P–S 반결합**이 차지해요. CBM 바닥의 조성도 S 와 P 가 대부분이에요 (LPSCl1.6 S 51 % + P 34 % · B₂O₃ 도핑 S 46 % + P 27 % + B 10 % · O 0 %).
- 오른쪽은 띠 가장자리부터 쌓은 결합당 반결합 무게예요. 2.5 eV 안에서 **P–S 가 B–S 의 3.4 배, P–O 의 7.2 배**예요 (이 그림의 가장자리 정의 · 07-08 분석은 3.7 배 · 5.8 배).
- 07-08 분석은 σ\* 시작점을 P–S +0.10 · B–S +0.75 · P–O +1.61 eV (CBM 기준) 로 적었어요 ([σ\* 궤도 제어 (07-08)](/kb?path=kb/results/redox_orbital_control_PS4_vs_BS3_2026_07_08.md)).
  ⚠ 그 시작점 정의는 도구로 남아 있지 않아요. 다시 내 보면 **P–S 가 맨 앞인 것은 문턱과 상관없이 같지만**, B–S 와 P–O 의 앞뒤는 문턱에 따라 바뀌어요 (P–O 는 가장자리 근처에 아주 작은 꼬리가 있어요). 그래서 그림에는 시작점 숫자를 찍지 않았어요.
- 결론은 같아요: **Li 가 준 전자는 P–S σ\* 가 먼저 다 받아요.** P–O 는 가장자리 근처에서 받을 자리가 거의 없어요.

### ③ 계면 MD 가 본 것 — 안쪽과 접촉면은 달라요

![Buried vs direct Li contact](/api/file/docs/figures/se_redox_frontier/rf_06_buried_vs_contact.svg)

- **안쪽 (매몰)** — 전자가 SE 를 지나 조금씩 오는 곳이에요. P–S 만 끊기고 B–S · P–O 는 그대로였어요 (B–S 9/9 · O–P 3/3 유지). P 둘레의 Li 수가 0.8 → 4.2 로 늘었어요 — P 가 단계적으로 환원된 흔적이에요.
- **Li 금속에 직접 닿은 면** — 전자가 넘치게 들어와서 높은 σ\* 도 채워져요. B–S 는 끊겼고, P–O 는 시드 2 개 중 1 개에서 끊겼어요.
- O 가 두 개 달린 사면체 (PS₂O₂) 는 접촉면에서 오히려 **PS₄ 보다 빨리** 무너졌어요 (PS₄ 결합 손실 34 % 대 22 % · MLIP · 시드 2).
- 반대로 B 가 노출된 면은 호스트 손실이 크게 줄었어요 (8 % 대 22 %) — B 의 환원 산물이 계면에 남아 **벽**이 됐어요.

### ④ Li 금속 ASSB 에 주는 뜻

- σ\* '문' 은 **안쪽 (매몰 · 입계) 의 규칙**이에요. 그곳에서는 강한 결합의 단위가 살아남아요.
- 접촉면에서는 열역학 순서대로 무너져요. 그래서 갈리는 건 **산물**이에요:
  - **산물이 전자를 막느냐** — Li₂S · LiCl 은 띠틈이 넓고, Li₃P 는 띠틈이 작아 약점이에요 (`db/properties/cascade_product_gaps.json`).
  - **산물이 계면에 남느냐** — 남아서 벽이 되면 분해가 번지지 않아요 (B 선례).
- bulk 계산에서 뽑는 설계 지표 후보 (07-08 §5): ① 그 결합의 σ\* 가 CBM 보다 충분히 위 ② 중심 양이온에 낮은 환원 상태가 없음.

---

## 4. Li₃PO₄ — 산화로 생길 때 vs 환원으로 생길 때 (질문 ③)

### ① 공통점 — Li₃PO₄ 자체는 산화환원 산물이 아니에요

- Li₃PO₄ 안에서 P 는 +5, O 는 −2 예요. SE 안에서도 원래 그랬어요.
- O 가 사면체끼리 S 와 자리를 바꿔 한 P 에 네 개 모인 것뿐이에요: **4 PS₃O³⁻ → 3 PS₄³⁻ + PO₄³⁻** (전자 이동 없음).
- 실제로 우리 원장에서 Li 를 주고받지 않는 중립 분해 (1.72–2.14 V) 에서도 Li₃PO₄ 가 나와요 — P–O 가 워낙 강해서 O 가 가장 안정하게 있는 곳이 Li₃PO₄ 예요.

### ② 차이는 옆에서 누가 전자를 내놓거나 받느냐예요

![Where O ends up vs voltage](/api/file/docs/figures/se_redox_frontier/rf_05_o_host_vs_voltage.svg)

숫자는 O 단독 대조 Li₅.₄PS₄.₁O₀.₃Cl₁.₆ 의 grand-potential (`db/properties/cei_esw_Li_controls_2026_09_16.json` · `o_only_03`) 이에요.
원장 행의 전압은 그 반응이 성립하는 구간의 **아래 끝**이에요 (`HZ-esw-reduction-limit-label`). 그래서 Li 흡수는 1.72 V 아래에서 시작해요.

**산화 쪽 (양극 · Li 가 빠짐)** — 전자를 내놓는 건 **S** 예요 (S²⁻ → S⁰ · free S 부터).

- **첫 반응 (2.14 V 부터)**: Li₅.₄PS₄.₁O₀.₃Cl₁.₆ → 0.925 Li₃PS₄ + 0.1 LiS₄ + **0.075 Li₃PO₄** + 1.6 LiCl + 0.7 Li⁺ + 0.7 e⁻
- **그다음**: Li 가 더 빠지며 인산염끼리 O 다리로 이어져요 — 2.70 V Li₄P₂O₇ → 2.91 V LiPO₃ → 3.69 V P₂O₅. O 는 끝까지 −2 예요 (O 가 산화되는 게 아니에요).
- **Li₃PO₄ 의 끝**: 이 혼합물에서는 2.70 V 부터 더 응축된 인산염으로 바뀌어요. Li₃PO₄ 단독의 상한 (약 4.2 V · Zhu 2015) 보다 낮은데, 옆 상에서 P 를 끌어와 응축하기 때문이에요.

**환원 쪽 (Li 쪽 · Li 가 들어옴)** — 전자를 받는 건 **P** 예요 (P⁵⁺ → P⁰ → P³⁻ · P–S σ\*).

- **첫 구간 (1.72 V 아래)**: + 4.625 Li → 4.1 Li₂S + **0.075 Li₃PO₄** + 1.6 LiCl + 0.925 P (원소 P)
- **그다음**: P 가 Li–P 화합물을 거쳐 Li₃P 가 돼요 — 0.69 V 위: + 7.4 Li → 0.925 Li₃P + 4.1 Li₂S + 0.075 Li₃PO₄ + 1.6 LiCl. O 를 문 P 만 +5 로 버텨요.
- **Li₃PO₄ 의 끝**: 0.69 V 아래 (Li 금속 0 V) 에서 **Li₃PO₄ + 8 Li → Li₃P + 4 Li₂O** — P⁵⁺ 까지 환원되고 O 는 Li₂O 로 가요.

정리하면 이래요.

- **산화 쪽 Li₃PO₄** — S 가 산화되는 동안 P⁵⁺–O 가 모인 것이에요. 전위를 더 올리면 Li 를 잃으며 응축돼요.
- **환원 쪽 Li₃PO₄** — PS₄ 의 P 가 환원되는 동안 O 를 문 P 만 +5 로 버틴 것이에요. 0.69 V 아래에서는 그것마저 환원돼요.

### ③ 실험에서 Li 쪽에 Li₃PO₄ 가 보인다면

열역학은 0 V 에서 Li₂O + Li₃P 라고 해요. 그런데도 Li 금속 쪽에서 Li₃PO₄ 가 보인다면 가능성은 셋이에요 (Kang 정리본 §7b ⑦).

1. **동역학적으로 버틴다** — P–O σ\* 가 높아서 전자를 늦게 받아요 (3 장과 같은 말 · 가설 · LiPON 류).
2. **전위가 0.69 V 보다 높은 자리다** — 접촉면에서 떨어진 곳이에요.
3. **남은 전구체다.**

이 논문 데이터로는 셋을 못 가려요.

### ④ 우리 셀 작동창 (2.5–4.25 V vs Li) 에서 읽으면

우리 셀은 2.5–4.25 V (vs Li/Li⁺) 로 돌아요. 그래서 양극 쪽 판단은 이 창에서 해요 (사용자 2026-11-09). Li 금속 쪽은 0 V 로 봐요.

- **창 전체가 열역학적으로는 산화 구간이에요.** SE 의 산화 개시 (2.14 V · 다음 breakpoint 2.36 V) 가 창 아래 끝 2.5 V 보다 낮아요.
  그래서 이 창에서 '안정성' 은 분해가 안 일어나는 게 아니라 **분해 산물이 막아서 멈추느냐**의 문제예요. 문장 17 의 *electrochemical stability* 도 이렇게 읽어야 해요.
- 창 안에서 O 단독 대조의 평형 산물이에요 (원장 `o_only_03` · 그림 위 파란 칸):

| 구간 (V vs Li) | O 의 집 | 나머지 산물 |
|---|---|---|
| 2.50–2.70 | Li₃PO₄ | P₂S₇ · LiS₄ · LiCl |
| 2.70–2.91 | Li₄P₂O₇ | P₂S₇ · LiS₄ · LiCl |
| 2.91–3.69 | LiPO₃ | P₂S₇ · LiS₄ → S → SCl · PCl₅ |
| 3.69–4.25 | P₂O₅ | P₂S₇ · SCl · PCl₅ |

- 그래서 **이 창에서 Li₃PO₄ 가 평형 산물인 건 맨 아래 0.2 V (2.50–2.70 V) 뿐이에요.** 그 위에서는 Li 가 빠지며 인산염끼리 O 다리로 이어진 응축 인산염 (Li₄P₂O₇ → LiPO₃ → P₂O₅) 이 O 의 집이에요. O 는 그대로 −2 예요.
- 3.33 V 부터는 Cl⁻ 도 산화돼요 (SCl · 3.39 V 부터 PCl₅). 4.25 V 충전 끝에서는 Li 가 다 빠진 산물만 남아요.
- Kang 의 XPS 가 본 'PO₄³⁻' 는 P–O 인산염 성분이에요. 그게 Li₃PO₄ 인지 응축 인산염인지는 따로 확인해야 해요 — 그래서 'Li₃PO₄ 계 CEI' 는 **'인산염 계 CEI'** 로 읽는 게 안전해요.
- 방전 끝 (2.5 V) 에서는 평형이 다시 Li₃PO₄ 쪽이에요. 하지만 분해 산물이 Li 를 다시 받아 되돌아가는지 (가역성) 는 이 계산이 말해 주지 않아요 (0 K 평형 · 동역학 없음).

### ⑤ 양극 쪽은 길이 하나 더 있어요

실제 산화물 양극에서는 양극의 O 가 황화물과 화학 반응해서 PO₄³⁻ (와 SO₄²⁻) 를 만드는 길도 있어요. 이건 SE 자신의 O 가 아니라 **양극에서 온 O** 예요.
우리 쪽은 O 를 열어 둔 grand-potential (`db/properties/cei_esw_O_2026_09_16.json`) 이 그 축이에요.

---

## 5. 우리 계산과의 관계 (원장)

- **산화는 free S²⁻ 가 먼저** — 자리별 p 상태 평균: free S 가 가장 얕고 O 가 가장 깊어요 (두 계). `db/properties/site_pdos_mean3p_summary.csv` · `db/properties/b2o3_pdos_site_smooth.csv`
- **O 치환은 산화 개시를 거의 안 움직인다** — O 단독 대조의 개시 = 무도핑 (같은 상 집합 · 한 점). `db/properties/cei_esw_Li_controls_2026_09_16.json` (`o_only_03`) · `HZ-esw-reduction-limit-facet-convention`
- **P–O 가 P–S 보다 강하다** — 결합당 ICOHP P–O −8.6 · P–S −6.0 eV (B₂O₃ 도핑 모델). `docs/figures/icohp/b2o3_icohp_summary.csv`
- **CBM 은 P–S σ\*** — COHP 빈 쪽 · CBM 바닥 조성. `docs/figures/icohp/b2o3_COHP_ext.csv` · [σ\* 궤도 제어 (07-08)](/kb?path=kb/results/redox_orbital_control_PS4_vs_BS3_2026_07_08.md)
- **안쪽에선 P–S 만 끊긴다 · 접촉면에선 높은 σ\* 도** — 계면 MD (MLIP · 시드 2). [σ\* 궤도 제어 (07-08)](/kb?path=kb/results/redox_orbital_control_PS4_vs_BS3_2026_07_08.md) §4.1
- **Li₃PO₄ 는 0.69–2.70 V 에서 O 의 집** — grand-potential 단계별 산물. `db/properties/se_redox_frontier_o_only_profile_origin.csv` (원장에서 다시 냄)

---

## 6. 이 카드가 못 하는 것

- **정공 국재 계산은 없어요.** "산화는 free S 부터" 는 자리별 PDOS 와 grand-potential 에서 온 말이에요 — 정공이 실제로 어디 앉는지 hybrid 로 본 적은 없어요.
- **σ\* 위치는 bulk PBE 값이에요.** 절대 위치는 hybrid 에서 움직일 수 있어요. 순서는 결합 세기에 묶여 있지만, B–S 와 P–O 의 앞뒤는 시작점 정의에 따라 바뀌어요 (3 장 ②).
- **COHP 그림의 에너지 0 은 LOBSTER 의 E_F 이고, 띠 가장자리는 0.1 eV 가우시안으로 번져 있어요.** 띠틈 숫자를 여기서 읽지 않아요 (띠틈 정본은 fixed-occupation nscf).
- **grand-potential 은 0 K MP hull · Li 열림 · 한 조성이에요.** 동역학이 없고, Kang 의 LPSOC (Li₆PS₄OCl) 와 조성이 달라요 (우리 대조는 O 0.3). 작동창 (2.5–4.25 V) 의 산물 표도 SE 자신의 O 만 본 평형이에요 — 실제 양극 계면에서는 양극의 O · 전이금속 · 동역학이 섞여요.
- **계면 MD 는 MLIP (UMA) · 시드 2 · B₂O₃ 도핑 모델의 PS₂O₂ 사면체예요.** PS₃O 를 직접 본 게 아니에요.
- **자리별 PDOS 그림은 같은 CSV 를 다시 계산해 PS₄ S 를 −2.22 eV 로 찍어요** (원장 요약 −2.23 과 반올림 차 · selftest 문턱 0.01 eV 안).

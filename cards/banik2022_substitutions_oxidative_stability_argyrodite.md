# Can substitutions affect the oxidative stability of lithium argyrodite solid electrolytes?

*치환해도 황이 가전자대 끝을 잡아 산화 안정성은 그대로다*

- Banik et al. · Zeier & Mo groups; manuscript / ACS-class, ~2022 · doi:n/a · digest `banik2022_substitutions_oxidative_stability_argyrodite`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 치환해도 황이 가전자대 끝을 잡아 산화 안정성은 그대로다

> P를 Si/Ge로, Cl을 I로 바꾸는 치환은 VBM을 황 상태가 차지하는 구조를 바꾸지 못해 아지로다이트의 산화 안정성을 거의 바꾸지 못한다. (L20 · 87 · 90)

### 요점

1. Li₆PS₅Cl과 Si·Ge 치환 Li₆PS₅I를 stepwise CV, 광학 흡수, HAXPES, DFT pDOS·COHP, grand-potential 계산으로 함께 비교했다. (L25–26 · 46 · 54)
2. 모든 조성에서 VBM 위치와 실효 산화 onset이 비슷했고, VBM은 자유 S²⁻와 PS₄³⁻의 비결합 S 3p 상태가 지배했다. (L67 · 71 · 81 …)
3. 원문은 S가 조성에 있는 한 단순 치환으로는 산화 안정성을 올릴 수 없고 양극 코팅이나 다른 물질군이 필요하다고 결론지었다. (L90–91)

### 무엇을 물었나

치환은 이온전도도를 올리려고 흔히 쓰지만, 산화 안정성도 함께 바뀌는지는 알려져 있지 않았다. 원문은 Li₆PS₅Cl의 산화가 2.5 V vs In/InLi에서 시작한다고 적었다. 이 값은 황 양극의 작동 범위 안이지만 산화물 삽입형 양극의 범위 밖이어서, 개선이 가능한지가 논문의 동기가 되었다. (L28–29 · 61–62)

원문은 전기화학 창을 보는 접근을 band-edge, stoichiometry, phase-stability 세 가지로 나눴다. band-edge 접근은 어느 원소가 분해를 주도하는지와 상한을 알려 주고, phase-stability 접근은 분해 반응의 Gibbs 자유에너지로 실제 분해 전압을 정한다. 계산 창이 실측 창보다 좁다는 점도 원문은 계면 kinetics와 준안정 중간상으로 설명했다. (L30 · 60–61)

- 그림 — Fig. 1: Fig. 1b에서 band-edge 창과 phase-stability 창의 차이를, Fig. 1c에서 Li₆PS₅Cl의 실측 창과 계산 창을 비교하면 된다. (L120–121)

### CV의 산화 onset

실험 시료는 Li₆PS₅Cl과 Ge-Li₆PS₅I, Si-Li₆PS₅I 세 가지다. Si와 Ge 조성은 전도도가 Li₆PS₅Cl과 비슷하도록 골라 물질 수송의 영향을 배제했다. 측정은 탄소와 전해질을 섞은 복합체로 계면적을 늘리고, reversal 전위를 0.1 V씩 3 V까지 올리는 stepwise CV로 했다. (L25 · 46 · 65)

1.8 V vs In/InLi 아래에서는 용량성 전류만 흘렀고, 그 위에서 전류가 급증하며 분해산물의 redox 피크가 나타났다. 낮은 reversal에서 안정해 보이던 전위에서도 높은 reversal 뒤에는 분해 피크가 자랐다. 몰 정규화한 산화 전류의 onset은 세 조성이 모두 비슷했고, 원문은 음이온도 양이온도 실효 산화 안정성을 바꾸지 않는다고 적었다. (L66–67)

- 그림 — Fig. 2: Fig. 2d에서 세 조성의 몰 정규화 산화 전류가 거의 같은 전위에서 오르는지를 보면 된다. (L123)

### 밴드엣지와 분해창

밴드엣지 측정도 치환에 따른 VBM 변화를 보이지 않았다. 광학 gap은 모든 조성에서 direct로 >3 eV였고 치환 때 약간만 이동했다. 6 keV HAXPES에서 모든 조성의 첫 피크가 같은 에너지에 나타나 VBM이 거의 같았고, I 조성은 밴드엣지 강도만 커졌다. Li₆PS₅I는 강한 sample charging으로 HAXPES 측정에 실패했다. (L46 · 70–71)

grand-potential 계산은 Lithium-evolution number를 전위에 대해 구해 열역학 창과 분해산물을 얻었다. 실험 창은 계산 창과 비슷하되 약간 더 넓었다. 분해산물은 S, 폴리설파이드, (P–S)ₓ와 LiX였고, Li₆PS₅I가 약간 더 안정해 Ge-Li₆PS₅I 분해의 중간 산물이 되었다. (L75–78)

- 그림 — Fig. 3: Fig. 3b에서 조성별 첫 피크 위치가 같은지를 보고, Fig. 3c의 계산 창과 Fig. 3d의 실험 한계를 나란히 비교하면 된다. (L125–127)

### 황이 VBM을 잡는다

pDOS에서 가전자대는 음이온 상태가, 그중 VBM은 S 상태가 지배했다. Cl 3p는 전기음성도가 커서 가전자대 깊이 있었다. I 5p는 밴드엣지에 일부 기여했지만, Table S3의 상평형에서 I⁻/I₂ redox는 창에 영향을 주지 않았다. (L81–84)

COHP에서 전도대 끝은 P–S 반결합 상태였고, P–S 결합 상태는 VBM보다 훨씬 아래에 있었다. 그래서 채워진 비결합 S 궤도가 VBM을 이룬다. 원문은 치환이 band gap의 크기만 바꾸고 S 상태가 산화 안정성 창을 고정한다고 적었으며, 황을 황화물 전해질 산화 안정성의 약점으로 불렀다. (L85–87 · 90)

- 그림 — Fig. 4: Fig. 4a의 개념도에서 비결합 S 상태가 VBM을 이루는 배치를, Fig. 4c의 COHP에서 P–S 결합 상태가 VBM보다 깊이 있는 것을 보면 된다. (L128 · 130)

### 어디까지 믿나

검토 측은 계산의 functional, k 점, U, supercell, 무질서 처리가 원문에 명시되지 않아 절대 gap과 절대 onset의 수치 재현을 확인할 수 없다고 본다. 계산 조성도 실험에 가까운 단일 모델 하나로 택했다. (L48–49 · 51 · 149)

검토 측은 결론이 P를 Si/Ge로, Cl을 I로 바꾸는 치환에 대한 것이고 할라이드 증량이나 산화물 도판트는 다루지 않았다고 본다. 또한 원문은 intrinsic 창만 다루며 kinetics, 계면, calendar 거동은 포함하지 않는다고 본다. (L110–111 · 151 · 154)

### 용어 풀이 (논문에 없는 일반 설명)

- **HAXPES**: 고에너지 X선으로 광전자를 떼어내 표면보다 깊은 bulk의 가전자대 끝을 측정하는 광전자 분광법이다.
- **COHP**: 원자쌍 사이 전자 상태를 에너지별로 결합과 반결합 기여로 나누어 보여 주는 분석이다.
- **phase-stability(grand-potential) 접근**: Li 화학퍼텐셜을 전압으로 바꿔 가며 전해질이 어떤 상들로 분해될 때 자유에너지가 낮아지는지 계산해 분해 전압과 산물을 정하는 방법이다.

### 우리 연구에 주는 뜻

- 우리 grand-potential 계산에서 comp1과 modelc는 VBM이 +0.32 eV 다른데도 산화 onset이 둘 다 2.14 V로 같아, 원문의 결론과 메커니즘에 맞는다. (L15 · 101–102)
- 원문이 쓴 phase-stability 방법은 우리가 쓰는 get_element_profile 기반 grand-potential 방법과 같은 산출물을 내며, 교신저자 Yifei Mo는 그 방법의 원저자다. (L5 · 103 · 141)
- 산화물 도판트가 onset을 옮긴다는 우리 쪽 주장은 철회되었고, 지금은 대부분 2.140 V에 고정된다는 호응까지만 말할 수 있다. (L111 · 167–168)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 광학 band gap | >3 eV | 모든 조성, direct, Tauc | L70 |
| HAXPES X선 에너지 | 6 keV | bulk VBM 측정 | L71 |
| 용량성 전류만 흐르는 상한 | 1.8 V vs In/InLi | stepwise CV, C–SE 복합 | L66 |
| Li₆PS₅Cl 산화 시작 전위 | 2.5 V vs In/InLi | 선행 실측 창, Fig 1c | L61 |
| Li₆PS₅Cl 환원 한계 | 0.6 V vs In/InLi | 선행 실측 창, Fig 1c | L61 |

### 읽을 때 조심할 것

- 본문과 그림이 In/InLi와 Li⁺/Li 두 전압 기준을 섞어 쓰므로, 2.5 V vs In/InLi 같은 값은 실험상 겉보기 onset이며 기준을 맞추기 전에는 열역학 계산값과 등치할 수 없다. (L17 · 150)
- 계산의 functional, k 점, U, 무질서 처리가 명시되지 않아 절대 gap과 절대 onset을 다른 계산과 1:1로 비교하면 안 된다. (L48–49 · 51 · 149)
- 미치환 Li₆PS₅I의 VBM은 charging으로 실측되지 않았고, I의 효과는 Si·Ge 치환 조성으로만 확인되었다. (L46 · 153)
- 결론은 MS₄와 할라이드 교환 치환의 intrinsic 창에 한정되며, 할라이드 증량, 산화물 도판트, kinetics나 calendar 거동까지 넓히면 부정확하다. (L151 · 154)

### 원문에서 먼저 볼 곳

- Fig. 2d에서 세 조성의 산화 전류 onset이 겹치는지를 먼저 본다. 치환이 실효 산화 안정성을 바꾸지 않는다는 실험 근거다. (L67 · 123)
- Fig. 4의 pDOS와 COHP를 본다. 비결합 S가 VBM을 이루어 산화 창을 고정한다는 논문의 핵심 설명이 여기 있다. (L86–87 · 128 · 130)
- Table S3와 Fig. 3c, 3d를 함께 본다. I⁻/I₂ redox가 창에 영향이 없다는 근거와 계산 창과 실험 창의 차이를 확인할 수 있다. (L83 · 126–127 · 138)

태그: Li₆PS₅Cl · Li₆PS₅I · argyrodite · 산화 안정성 · grand-potential · HAXPES · COHP · stepwise CV

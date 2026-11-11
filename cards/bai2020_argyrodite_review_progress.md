# Research progress in Li-argyrodite-based solid-state electrolytes

*다중 치환과 공도핑이 아지로다이트의 약점을 함께 푼다*

- Bai et al. · J. Mater. Chem. A 8, 25663-25686 (2020) · doi:10.1039/d0ta08472g · digest `bai2020_argyrodite_review_progress`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 다중 치환과 공도핑이 아지로다이트의 약점을 함께 푼다

> Li₆PS₅X는 전도도와 연성의 균형이 좋지만, 수분, 고전압 산화, 합성 편차의 약점은 다중 치환과 공정 최적화로 함께 풀어야 한다. (L19 · 21 · 35)

### 요점

1. Li-argyrodite Li₆PS₅X(X=Cl/Br/I) 한 계열을 결정구조, 치환과 도핑, 합성, 계면, 대기안정, 셀 통합의 여섯 토픽으로 종설했다. (L16 · 35)
2. anion site disorder가 inter-cage 점프 장벽을 낮춰 전도도를 켜고, Cl-rich 조성은 10 mS/cm에 이르며, Sn과 O 공도핑은 대기안정을 높인다고 정리했다. (L20 · 85 · 122 …)
3. 자체 계산이나 실험이 없는 2020년 문헌 종설이라 수치는 인용값이고, 방법의 세부는 원전에서 확인해야 한다. (L46 · 241 · 298–299)

### 세 가지 약점

원문은 Li-argyrodite Li₆PS₅X를 황화물 고체전해질 중 가장 유망한 계열로 본다. 근거는 10⁻³–10⁻² S/cm 수준의 이온전도도, 냉간가압이 가능한 연성, 전기화학 안정성의 균형이다. 그러나 수분에 취약해 H₂S가 나오고, 양극 고전압에서 산화 분해되며, 합성 공정의 편차가 크다는 세 약점이 상용화를 막는다고 적었다. (L19 · 35)

연성은 Young's modulus로 정량된다. 원문의 Table 1에서 argyrodite LPSX는 22.1–30.0 GPa이고 산화물 LLTO는 200 GPa다. 원문은 이 낮은 탄성률이 냉간가압과 밀착 접촉을 가능하게 한다고 적었다. (L93 · 98 · 100)

- 그림 — Table 1: oxide, sulfide, organic 세 군의 E를 나란히 보면 된다. sulfide 줄의 LPSX 값이 argyrodite의 연성을 보여 준다. (L221)

### 구조와 Li 점프

원문은 Li₆PS₅X를 공간군 F-43m의 입방 구조로 설명한다. X⁻는 Wyckoff 4a, PS₄의 P는 4b, free S²⁻는 4d에 놓이고, Li⁺는 24g와 48h가 만드는 cage에 있다. Li 이동은 doublet(48h–24g–48h), intra-cage, inter-cage 세 가지이며 inter-cage 점프가 율속이다. (L72–76 · 80)

전도도를 지배하는 것은 halide와 free S²⁻ 자리가 섞이는 anion site disorder다. Cl과 Br은 섞임이 커서 10⁻³–10⁻² S/cm를 보인다. I⁻는 이온반경 2.20 Å가 S²⁻의 1.84 Å보다 커서 섞이지 않고 σ가 ~10⁻⁷ S/cm에 그친다. 원문은 이 disorder가 inter-cage 점프의 활성화에너지를 낮춰 superionic 전도를 켠다고 적었다. (L83–85)

- 그림 — Fig. 1: Fig 1b에서 cage 안과 cage 사이의 세 가지 점프 경로를 구분해 보면 된다. (L77 · 220)

### 치환으로 높인 전도도

치환 자리는 halide 4a, PS₄³⁻ 단위, free S²⁻ 4d의 세 곳이다. halogen과 Li 함량을 늘리면 전도도가 오른다는 DFT-MD 예측은 Li₅.₅PS₄.₅Cl₁.₅에서 σ = 10 mS/cm로 확인되었다. 다만 Cl 계수를 1.7–1.9로 올리면 순상을 얻는 데 500 ℃의 합성온도가 필요하다고 원문은 적었다. (L117–119 · 122 · 124)

aliovalent 양이온 치환은 격자, vacancy, disorder를 함께 바꾼다. Si 치환 Li₆₊ₓP₁₋ₓSiₓS₅Br은 x=0.3에서 격자상수가 포화되고 σ가 0.7에서 2.4 mS/cm로 올랐다. Nazar 그룹의 Sb/Si 계는 concerted ion migration을 활성화해 Li₆.₆Sb₀.₆Si₀.₄S₅I에서 14.8 mS/cm를 보였다. (L129–130)

- 그림 — Fig. 4: Fig 4에서 새로 나타난 inter-cage Li3(48h–48h) 점프 경로를 보면 된다. (L224)

### 대기와 계면 안정

H₂S는 P⁵⁺의 높은 oxophilicity 때문에 생긴다. 원문은 HSAB 원리에 따라 soft acid인 Sn이 S를 선호해 대기안정을 준다고 적었다. Li₆PS₅I–20Sn은 O₂ 10 h 노출 뒤 질량 증가가 0.28%로, pure Li₆PS₅I의 1.12%보다 작았다. 원문은 단일 원소 치환은 한 측면만 개선하고, metal과 O의 다중 치환이 종합 개선을 준다고 정리했다. (L142 · 144–145 · 150)

양극 쪽에서 Li₆PS₅Cl은 CV상 2.2 V 이상에서 불안정하고, 인용된 이론값으로 S/S²⁻ 산화가 2.24 V에서 일어나 Li₃PS₄, S, LiCl을 만든다. 음극 쪽에서는 Li 금속과 호환되지 않으며 환원전위가 1.7 V 부근이다. 원문은 분해산물이 만드는 passivation interphase가 실효 안정창을 넓힌다고 적었다. (L161–163 · 168)

- 그림 — Fig. 2: Fig 2a의 질량 변화로 Sn 치환 효과를 보고, Fig 2e에서 PS₄와 (P/Sn)S₄의 H₂O 산화 난이도를 비교하면 된다. (L222)

### 어디까지 믿나

검토 측은 원문을 자체 계산이나 실험 없이 인용 문헌을 엮은 종설로 본다. 인용된 DFT의 functional, k점, supercell, 무질서 처리는 원문에 없어 원전을 봐야 한다. (L236 · 241 · 298)

검토 측은 2020년 시점의 한계도 지적한다. grand-potential 방법의 절차는 기술되지 않고 결과만 인용되었다. 원문이 든 치환 예시는 모두 전도도를 높이는 방향이라고 검토 측은 본다. (L134 · 238 · 299)

### 용어 풀이 (논문에 없는 일반 설명)

- **anion site disorder**: 결정 안에서 서로 다른 음이온이 정해진 자리를 바꿔 차지하는 무질서로, argyrodite에서는 halide와 S²⁻ 자리의 섞임을 말한다.
- **HSAB**: 단단한 산은 단단한 염기와, 무른 산은 무른 염기와 잘 결합한다는 화학 결합 경향의 원리다.
- **passivation interphase**: 전해질의 분해산물이 계면에 층을 이루어 더 이상의 분해를 막는 보호층이다.

### 우리 연구에 주는 뜻

- 우리 grand-potential 산화 onset 2.14/2.256 V는 원문이 인용한 S/S²⁻ 2.24 V와 CV 2.2 V에 0.1 V 안에서 맞고, 분해산물 Li₃PS₄, S, LiCl도 같다. (L175–176)
- 우리 comp1의 relaxed-ion E_VRH 22.06 GPa는 원문 Table 1의 LPSX 22.1–30.0 GPa 줄에 놓이지만, 원문은 relaxed와 clamped-ion을 구분하지 않는다. (L108)
- 우리 Nd와 O cascade는 원문의 metal과 O 공도핑 틀에 들어맞지만, 원문 예시는 대기 질량 변화를 재고 우리는 전자절연 interphase를 보므로 관측량이 다르다. (L152 · 303)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| Cl-rich 조성 이온전도도 | 10 mS/cm | Li₅.₅PS₄.₅Cl₁.₅, 실험 | L122 |
| Li₆PS₅I 이온전도도 | ~10⁻⁷ S/cm | anion disorder 없는 I 계 | L84 |
| Sb/Si 치환 최고 전도도 | 14.8 mS/cm | Li₆.₆Sb₀.₆Si₀.₄S₅I, RT | L130 |
| argyrodite Young's modulus | 22.1–30.0 GPa | LPSX, Table 1 | L108 |
| 이론 산화 전위 | 2.24 V | Li₆PS₅Cl S/S²⁻ redox, 인용 | L162 |
| Li/SE 계면 환원전위 | 1.7 V | argyrodite와 Li 금속 | L168 |

### 읽을 때 조심할 것

- 원문의 1.7 V는 Li/SE 계면 환원전위이고 함께 인용된 이론 P/P⁵⁺ 1.08 V와 정의가 달라, 검토 측은 두 값을 등치하지 말라고 본다. (L162 · 168 · 302)
- Cl-rich 예시는 Cl 1.5 조성이며, 그보다 Cl이 많으면 용해한계 때문에 순상 합성이 어렵고 2차상 위험이 커진다. (L124 · 190 · 300)
- 원문의 수치는 모두 인용된 문헌값이므로 원문이 계산하거나 측정한 값으로 인용하면 안 된다고 검토 측은 본다. (L261 · 298)
- 원문은 halide가 고전압 계에서 Al 집전체 부식을 일으킨다고 경고해, Cl-rich 조성의 대가를 함께 적었다. (L126)

### 원문에서 먼저 볼 곳

- Fig 1은 결정구조의 자리 배치와 세 가지 Li 점프를 한 그림에 담고 있어 이후 내용을 읽는 기준이 된다. (L48 · 220)
- 원문 p.25669의 공도핑 문단은 단일 치환과 다중 치환을 비교한 결론을 담고 있어 리뷰의 핵심 처방이 무엇인지 확인할 수 있다. (L21 · 150)
- Table 5는 LCO, NCM, LMO와 Li₆PS₅Cl의 half-cell을 비교해 양극별 반응성 차이를 보여 준다. (L164 · 230)

태그: Li₆PS₅X · argyrodite · anion site disorder · aliovalent substitution · HSAB · O 공도핑 · ESW · review

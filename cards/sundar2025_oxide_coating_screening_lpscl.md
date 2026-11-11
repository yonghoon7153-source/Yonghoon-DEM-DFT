# Computationally‐Guided Development of Sulfide Solid Electrolyte Powder Coatings for Enhanced Stability and Performance of Solid‐State Batteries

*코팅 자체보다 계면 분해산물의 전도도가 성능을 가른다*

- Sundar et al. · Advanced Science 12, e13191 (2025) · doi:10.1002/advs.202513191 · digest `sundar2025_oxide_coating_screening_lpscl`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 코팅 자체보다 계면 분해산물의 전도도가 성능을 가른다

> LPSCl 산화물 코팅의 성능은 분해산물의 이온·전자 전도도로 가장 잘 예측되며, MgO가 여러 면에서 가장 좋았다. (L49 · 215–216)

### 요점

1. DFT 두 단계 스크리닝으로 Li₆PS₅Cl 입자에 입힐 바이너리 산화물을 고르고, MgO·ZrO₂·ZnO를 ALD로 실제 입혀 검증했다. (L49 · 57 · 213–214)
2. ZrO₂는 Li 절연성 산물 때문에 이온전도도가 한 자릿수 줄었고, MgO는 전자전도도를 크게 낮추면서 CCD를 0.9 mA/cm²까지 올렸다. (L202–203 · 209)
3. 결론은 Li 대칭셀과 전도도 비까지만 받쳐지며, full-cell 데이터와 DFT+U, 3상 반응 검토는 빠져 있다. (L249 · 253 · 255–256)

### 무엇이 빠져 있었나

같은 그룹의 선행 연구는 LPSCl에 Al₂O₃를 ALD(원자층 증착)로 입혀 이온전도도를 올리고 전자전도도를 낮췄다. 원문은 이보다 다면적인 이득을 주는 코팅을 계산으로 찾는 길을 묻는다. (L59 · 61)

원문은 기존 코팅 스크린이 양극에만 집중하고 반응 에너지만 봤다고 적었다. 그래서 전해질, 양극, 음극 세 계면을 모두 보고 분해산물의 전도도까지 따지는 스크린을 세웠다. (L60 · 178 · 188)

- 그림 — Fig. 1: 오른쪽 세 개의 확대 모식도가 Li 음극║코팅, LPSCl║코팅, 양극║코팅 계면을 나타낸다. (L178)

### 세 계면 반응성

첫 단계는 계면 분해 driving force ΔE를 Materials Project Interface Reactions로 구하는 일이다. 가능한 모든 반응 가운데 가장 음의 ΔE를 골라 heatmap으로 만들었고, 에너지는 PBE 0 K 값이다. (L148–149)

LPSCl 계면에서는 SiO₂가 반응하지 않았고 ZnO가 −0.372로 가장 반응성이 컸다. Li 계면에서 MgO는 −0.040으로 안정했고, MgO·ZrO₂·Al₂O₃가 양쪽 모두 비교적 안정한 핵심 후보로 남았다. (L179–180)

- 그림 — Fig. 2: heatmap에서 짙은 녹색일수록 반응성이 낮은 계면이다. LPSCl 패널과 Li 음극 패널을 비교하면 된다. (L178–180)

### 밴드갭과 분해산물

전자전도를 가늠하려고 HSE06(mixing 0.32)으로 bulk와 약 1 nm slab의 밴드갭을 계산했다. LPSCl 기준선은 3.92 eV였고, ZnO는 1 nm slab에서 0.4 eV로 급감해 bulk 밴드갭만으로는 부족함을 보였다. (L146 · 151 · 184–185)

둘째 단계는 분해산물의 Li 이동 장벽을 CI-NEB로, 밴드갭을 함께 보는 것이다. Li₃PO₄(0.25)와 Li₃PS₄(0.34–0.41)는 Li⁺ 전도체이고 밴드갭이 커서 이온 통로를 지키며 전자를 막는다. (L188–189)

- 그림 — Fig. 4: a 패널은 LPSCl║산화물, b 패널은 Li║산화물 계면 산물의 Li 이동 장벽이다. 왼쪽 화살표는 계면 반응성이 커지는 방향이다. (L188 · 191)

### ALD 실측 검증

MgO·ZrO₂·ZnO를 약 1 nm 두께로 입혔고, XPS에서 DFT가 예측한 LiMgO, Li₆Zr₂O₇·Zr₃O 같은 산물이 보였다. ZnO는 LPSCl 위 직접 증착에 실패해 Al₂O₃ seed를 먼저 입혔다. (L195–198)

전도도 비는 계산 예측과 맞았다. ZrO₂는 이온전도도가 0.1×로 줄고 전자전도도는 2×로 늘었으며, MgO는 전자전도도 비가 0.11이었다. (L202–203)

- 그림 — Fig. 6: y값 1의 점선이 uncoated 기준이다. ZrO₂만 이온전도도가 아래로, 전자전도도가 위로 벗어난다. (L202–203)

### MgO와 그 한계

MgO 코팅은 Li 금속과 만났을 때 Li₂S 생성이 적었고 LiMgO·LiMg alloy·Li₂O가 생겼다. 대칭셀에서 uncoated는 0.6 mA/cm²에서 soft short가 났지만 MgO 코팅은 0.9 mA/cm²까지 대체로 안정했다. (L207–209)

검토 측은 DFT+U 언급이 없어 전이금속 산화물의 ΔE와 밴드갭 신뢰도가 의문이라고 본다. 또 mixing 0.32가 비표준이라 밴드갭 절대값이 이 선택에 좌우되고, 3상 반응과 full-cell 사이클은 검토되지 않았다고 지적한다. (L249 · 251 · 253 …)

- 그림 — Fig. 8: B와 D의 ASR을 비교하면 uncoated에서만 0.6 mA cm⁻² 부근의 급락이 보인다. (L130–131 · 209)

### 용어 풀이 (논문에 없는 일반 설명)

- **Interface Reactions**: 두 상의 혼합비를 훑으며 convex hull 위에서 가능한 분해반응의 에너지를 구하고 가장 음의 값을 계면 반응성으로 삼는 계산법이다.
- **CI-NEB**: 초기와 최종 구조 사이 이미지 띠를 최적화하되 가장 높은 이미지를 안장점으로 끌어올려 이동 장벽을 구하는 방법이다.
- **CCD**: Li 대칭셀에서 단락이 나기 직전까지 버티는 최대 전류밀도다.

### 우리 연구에 주는 뜻

- 계면 분해 ΔE 계산은 우리 interface_reactivity, GrandPotentialInterfacialReactivity와 같은 pymatgen 알고리즘이며, 우리는 전압별 grand potential까지 확장했다는 차이가 있다. (L150 · 224)
- LPSCl 밴드갭은 이들이 HSE06으로 3.92 eV, 우리가 PBE로 comp1 2.066 eV라 절대 비교하지 않고 wide-gap insulator라는 판정에만 쓴다. (L223)
- 우리 도핑 cascade와는 레버가 달라 랭킹이나 descriptor를 대조하지 않고, 분해산물 전도도가 진짜 레버라는 생각만 공유한다. (L17 · 236)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| LPSCl 밴드갭 (HSE06) | 3.92 eV | bulk LPSCl, mixing 0.32 | L68 |
| ZnO 1 nm slab 밴드갭 | 0.4 eV | HSE06 slab 계산 | L185 |
| Zr₃O Li 이동 장벽 | 1.4 eV | ZrO₂ 분해산물, CI-NEB | L190 |
| 양극 계면 ΔE 예시 | −0.024 eV/atom | LiMn₂O₄ + Al₂O₃ 반응 | L181 |
| MgO 코팅 전자전도도 비 | 0.11 |  | L120 |
| MgO 코팅 대칭셀 안정 한계 | 0.9 mA/cm² | Li 대칭셀 CCD | L209 |

### 읽을 때 조심할 것

- 검토 측은 DFT+U가 명시되지 않아 전이금속 산화물과 양극 계면의 ΔE·밴드갭 순위는 조심해야 한다고 본다. (L249 · 252)
- 전도도는 절대값 없이 uncoated 대비 비로만 보고되어 다른 연구의 절대 성능과 비교할 수 없다. (L256)
- ZnO 실측은 Al₂O₃ seed 위에 입힌 이중층이라 순수 ZnO 효과가 완전히 분리되지 않았다. (L254)
- 반응 ΔE는 PBE 0 K 2상 반응이고 3상 반응은 대표 하나만 검토되었으며 full-cell 성능은 검증되지 않았다. (L248 · 253 · 255)

### 원문에서 먼저 볼 곳

- Fig. 4를 먼저 보면 어떤 분해산물이 Li 전도체이고 어떤 것이 절연체인지, 즉 논문의 핵심 논리축을 한눈에 볼 수 있다. (L187–188)
- Fig. 6은 계산 예측이 전도도 실측으로 확인되는 자리이며 ZnO 역설도 여기서 드러난다. (L201 · 204)
- Table 1과 Table 2는 LPSCl 계면과 Li 계면의 ΔE 순위와 분해산물을 정리한 표다. (L71 · 179–180)

태그: Li₆PS₅Cl · ALD · MgO · InterfaceReactions · HSE06 · CI-NEB · CCD

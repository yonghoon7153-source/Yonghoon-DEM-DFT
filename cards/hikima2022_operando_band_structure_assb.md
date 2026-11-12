# Operando analysis of electronic band structure in an all-solid-state thin-film battery

*충전하면 양극 Fermi level이 내려가 집전체 계면이 정류한다*

- Hikima et al. · Commun Chem 5, 52 (2022) · doi:10.1038/s42004-022-00664-w · digest `hikima2022_operando_band_structure_assb`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 충전하면 양극 Fermi level이 내려가 집전체 계면이 정류한다

> 박막 전고체전지를 반도체 소자로 보고 operando HAXPES로 재면, 충전 중 Li₂₋ₓMnO₃가 n형에서 p형으로 바뀌어 고전압 충전이 막힌다. (L22 · 61 · 102)

### 요점

1. Al|Li₂MnO₃|LASGTP|Li₃PO₄|Li 박막셀의 각 층 밴드를 UPS와 LEIPS로 진공준위에 정렬하고, 충전 중 코어레벨 결합에너지 이동을 operando HAXPES로 추적했다. (L15 · 27 · 33)
2. 원문은 충전 중 Li₂₋ₓMnO₃의 Fermi level이 총 ~1.1 eV 내려가 n형에서 p형으로 바뀌고, Al 계면이 Ohmic에서 Schottky로 바뀌며 inversion layer가 생긴다고 적었다. (L61 · 89 · 96)
3. 검토 측은 재료가 산화물 양극과 NASICON 전해질이고 박막 모델셀이며 capacitor 기전은 간접 추론이라, 결론을 다른 재료나 실셀로 옮기는 데 한계가 있다고 본다. (L150 · 155–156)

### 전지를 소자로 보기

충방전, 임피던스, XPS 같은 기존 배터리 특성화는 밴드구조를 고려하지 않는다. 액체전해질 셀은 분해와 복잡성 때문에 작동 중 밴드구조를 잴 수 없다. 원문은 전고체전지의 모든 계면이 고체 정션이므로 반도체 헤테로접합 소자처럼 다룰 수 있다고 적었다. (L31)

모델셀은 Al 집전체, Li₂MnO₃ 양극, LASGTP 고체전해질 기판, Li₃PO₄ buffer, Li 음극의 다섯 층으로 된 박막이다. UPS로 VBM과 일함수를, LEIPS(저에너지 역광전자분광)로 CBM과 전자친화도를 얻고, operando HAXPES(경X선 광전자분광)로 깊이 묻힌 계면의 결합에너지 이동을 충전 중에 따라갔다. (L27 · 33 · 76–77)

- 그림 — Fig. 1: c에서 박막 모델셀 구성을, d에서 potentiogalvanostat와 빔라인으로 된 operando HAXPES 장치를 보면 된다. (L84)

### 층별 밴드 정렬

다섯 층을 진공준위 기준으로 정렬하면 양극에서 buffer로 갈수록 밴드갭이 넓어진다. 원문의 밴드갭은 Li₂MnO₃ 2.83, LASGTP 4.09, Li₃PO₄ 5.77 eV다. Al과 Li의 Fermi level 차는 2.6 eV로, 원문은 이것이 셀 전압의 밴드 기원이라고 적었다. (L42–44 · 53 · 85)

pristine 상태에서 Li₂MnO₃/LASGTP 계면은 staggered(Type II) 정렬이다. Li₂MnO₃의 VBM이 LASGTP보다 1.46 eV 위에 있다. (L52 · 88)

- 그림 — Fig. 2: 파란 숫자가 일함수, 빨간 숫자가 밴드갭, 검은 숫자가 전자친화도와 이온화퍼텐셜이다. (L85)

### 충전 중 네 단계

operando HAXPES는 충전 구간을 전자구조 변화에 따라 네 단계로 나눴다. 첫째 단계에서는 x<0.04의 미량 Li 추출만으로 Li₂₋ₓMnO₃의 Fermi level이 ~0.45 eV 내려간다. 원문은 이것을 operando HAXPES로 처음 관측했다고 적었다. (L60 · 94–95)

둘째 단계에서 Fermi level은 VBM 수준까지 총 ~1.1 eV 내려가 n형에서 p형으로 바뀐다. 셋째 단계는 ~4.6 V plateau로, 결합에너지는 변하지 않고 새 O 1s peak만 커져 원문은 이를 progressive oxygen redox로 해석했다. 넷째 단계에서는 Li 1s와 O 1s가 Al의 Fermi level과 나란히 움직인다. (L61–63 · 96–98)

- 그림 — Fig. 4: b-1 Li 1s와 b-2 O 1s의 ΔBE에서 네 단계를 읽고, a-2 P 1s가 거의 변하지 않는 것을 기준으로 삼으면 된다. (L136–137)

### 셀 거동의 해석

원문은 고전압에서 충전이 더 진행되지 않는 원인을 계면 정류로 설명했다. 둘째 단계의 p형 전이와 inversion layer로 Al/Li₂₋ₓMnO₃ 계면이 정류성이 되어 전류가 방전 방향으로만 흐른다. 이것이 이론용량 459 mAh/g에 못 미치는 전자구조적 원인 중 하나라고 적었다. (L28 · 66 · 102)

방전 2.0 V에서는 LASGTP가 전위창 밖으로 0.53 eV 벗어나 Li₂₋ₓMnO₃에 의해 환원될 위험이 있다. 5.0 V에서 OCV로 이완할 때 ΔBE가 바로 풀리지 않아, 원문은 5.0 V 상태가 열역학 평형이 아니고 과전압이 있다고 보았다. 그 기전으로 bulk 활성화장벽과 Li₂₋ₓMnO₃/LASGTP 계면의 가역 capacitor 형성을 제시했다. (L55 · 90 · 99 …)

- 그림 — Fig. 3: a에서 c까지 pristine, 충전 5.0 V, 방전 2.0 V의 정렬 타입 변화를, d에서 f까지 같은 조건의 band bending을 비교하면 된다. (L134–135)

### 어디까지 믿나

검토 측은 둘째 단계의 ~1.1 eV가 밴드갭이 일정하다는 가정으로 환산한 값이라고 본다. Mn 산화상태 변화로 gap이 바뀌면 이 값은 흔들린다. HAXPES 신호는 Al 집전체를 통과하므로 Al 기여를 빼야 하고, grounding 선택이 결합에너지 기준을 바꾼다. (L153–154)

검토 측은 계면 capacitor 기전이 depth profiling과 선형 V-Q 관계에서 나온 추론이지 직접 증명이 아니라고 본다. 원문도 두꺼운 전극을 쓴 실셀에는 추가 고려가 필요하다고 적었다. 검토 측은 n형에서 p형으로의 전이가 Li₂MnO₃ 특유일 수 있어 다른 양극으로 일반화하기 어렵다고 본다. (L155–157)

### 용어 풀이 (논문에 없는 일반 설명)

- **band bending**: 계면에서 전하 운반자가 재분포하면서 Fermi level을 기준으로 밴드 가장자리가 휘는 현상이다.
- **staggered(Type II)와 straddling(Type I)**: 두 반도체의 VBM과 CBM이 서로 엇갈리는지, 한쪽이 다른 쪽 밴드갭 안에 들어가는지에 따른 헤테로접합 정렬 분류다.
- **Schottky 접촉과 inversion layer**: 금속과 반도체 계면이 한 방향으로만 전류를 흘리는 정류 접촉이 Schottky 접촉이고, 반도체 표면의 다수 운반자 종류가 뒤집힌 층이 inversion layer다.

### 우리 연구에 주는 뜻

- 원문이 UPS로 잰 Li₃PO₄ 밴드갭 5.77 eV는 우리 sei_products.json의 Li₃PO₄ 5.73 eV와 거의 같아, 우리 전자절연 SEI 산물 계산의 외부 실측 앵커가 된다. (L118 · 161)
- 우리 DFT의 절대 VBM은 셀 간 정렬이 보정되지 않았고 slab 일함수도 포기했는데, 이 진공준위 절대 정렬법이 외부 절대기준을 준다. (L115 · 162)
- 우리 ORCA ΔSCF XPS가 정적 코어레벨 계산이라면, 이 operando HAXPES는 작동 중 코어레벨 이동의 실측이라 서로 짝이 된다. (L122 · 165)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 충전 중 Li₂₋ₓMnO₃ Fermi level 총 하강 | ~1.1 eV | stage 2, 일정 밴드갭 가정 | L61 |
| 미량 Li 추출 시 Fermi level 하강 | ~0.45 eV | stage 1, 0 ≤ x < 0.04 | L60 |
| LASGTP가 전위창을 벗어난 양 | 0.53 eV | 방전 2.0 V, band bending 무시 | L55 |
| Li₃PO₄ 밴드갭 | 5.77 eV | UPS 실측, buffer층 | L118 |
| LASGTP 밴드갭 | 4.09 eV | NASICON 산화물 고체전해질 | L119 |
| Li₂MnO₃ 이론용량 | 459 mAh/g | 2Li 추출 기준 | L28 |

### 읽을 때 조심할 것

- 재료가 Li₂MnO₃ 양극과 LASGTP 산화물 전해질이라 argyrodite의 VBM, CBM, 밴드갭, 일함수와 절대값을 1:1로 비교할 수 없다. (L150)
- LASGTP의 potential window는 밴드 가장자리로 정한 전자적 창이지 grand-potential 분해창이 아니다. (L152)
- Fermi level 하강 ~1.1 eV는 Li₁.₉₆MnO₃의 밴드갭이 일정하다는 가정에 기댄 값이다. (L154)
- 35 nm Li₂MnO₃ 박막 모델셀의 결과라 두꺼운 복합전극 실셀에는 그대로 옮길 수 없다. (L155)

### 원문에서 먼저 볼 곳

- Fig. 4b의 Li 1s와 O 1s ΔBE를 먼저 본다. 충전 네 단계의 정량 근거가 모두 여기에 있다. (L137)
- Fig. 3a에서 f까지를 본다. 충전과 방전에 따른 정렬 타입 전이와 band bending 크기가 나온다. (L134–135)
- Fig. 2의 밴드도를 본다. 다섯 층의 일함수, 전자친화도, 이온화퍼텐셜, 밴드갭이 진공준위 기준으로 한 장에 있다. (L133)

태그: Li₂MnO₃ · LASGTP · Li₃PO₄ · operando HAXPES · UPS · LEIPS · band bending

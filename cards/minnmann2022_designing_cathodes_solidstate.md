# Designing Cathodes and Cathode Active Materials for Solid‐State Batteries

*고체전지 양극은 CAM과 SE를 함께 설계해야 한다*

- Minnmann et al. · Advanced Energy Materials 12, 2201425 (2022) · doi:10.1002/aenm.202201425 · digest `minnmann2022_designing_cathodes_solidstate`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 고체전지 양극은 CAM과 SE를 함께 설계해야 한다

> 고체전지 복합양극은 CAM과 SE의 함량, 입자 크기, 분포, 계면을 함께 맞춰야 한다는 정성 설계 지침을 제시한다. (L116 · 219–220 · 235)

### 요점

1. 무기 CAM과 sulfide, halide SE로 된 복합양극의 설계 과제를 미세구조, 화학-기계, 계면의 세 층위로 나누어 타 문헌의 결론을 종합했다. (L21–23 · 113–114)
2. CAM 60–70 vol%, 2차입자 3–5 µm, 작은 SE와 tailored PSD, 명시적 tortuosity 고려 같은 설계 임계와 권고가 나왔다. (L89 · 101 · 175 …)
3. 측정값도 시뮬레이션도 없는 Perspective여서 범위 권고까지만 말할 수 있고, 정량 앵커의 출처로는 쓸 수 없다. (L259 · 365 · 370)

### SSB 양극의 과제

액체전해질 전지에서 성숙한 CAM 요구조건은 고체전해질로 바꾸면 달라진다. SE의 전기화학 안정성과 기계적 강성이 LE와 다르기 때문이다. CAM은 셀의 유일한 에너지 저장 성분이어서 그 함량을 최대화하는 것이 비에너지를 결정한다고 원문은 적었다. (L108–111)

원문의 질문은 미세구조와 전하수송, (chemo-)역학, 계면화학의 세 층위에서 무엇을 설계해야 하는가이다. CAM 종류별(intercalation, insertion, conversion) 전략도 함께 묻는다. 핵심 프레이밍은 CAM과 SE를 상보적으로 함께 설계해야 한다는 것이다. (L113–114 · 116)

- 그림 — Fig. 1: cell, cathode 미세구조, interface 나노구조로 길이척도를 나누고 각 층위의 도전과제를 배치한 모식도다. (L125–126)

### 미세구조와 전하수송

CAM 함량을 늘리면 에너지는 늘지만 SE가 줄어 이온경로의 tortuosity가 커지고 출력이 준다. 원문은 실험에서는 ~50 vol% CAM으로 이온 percolation을 확보했고, 기하모델에서는 60–70 vol% CAM이 최적이며, 상업셀은 ~70 vol% CAM을 목표로 한다고 적었다. (L129–131)

SE 양극에서는 잔류 기공과 grain boundary가 남아 경로가 LE보다 훨씬 우회한다. 그래서 apparent tortuosity가 기하 tortuosity보다 크다. 기공은 전자와 이온을 모두 막으므로 최소화 대상이고, 부분전도도(partial conductivity)가 percolation의 적절한 descriptor라고 원문은 명시했다. (L135–137 · 141 · 146)

- 그림 — Fig. 2: (a) LE 양극의 짧은 빨간 경로와 (b) SE 양극의 길게 우회하는 빨간 경로를 비교하면 된다. (L134–136)

### 화학-기계와 계면

모든 성분이 고체이고 부피가 구속되어 있어 (de)lithiation 부피변화가 성능에 직접 영향을 준다. CAM 입자에 균열이 생기면 LE는 새 기공에 침투하지만 rigid한 SE는 침투하지 못해 수송경로가 길어진다. 큰 부피변화는 CAM-SE 접촉상실과 계면저항 증가로 이어진다. (L151–152 · 154)

실험실은 수~수십 MPa 외압으로 이를 보상하지만 원문은 이런 고압이 상업화에 부적합하다고 적었다. 계면에서는 CAM의 낮은 Li 화학퍼텐셜이 SE 산화분해를 일으킨다. LiNbO₃ 같은 보호 코팅이나 산화안정성이 높은 halide(Li₃InCl₆/Li₃YCl₆)가 완화책으로 제시된다. (L92 · 159 · 165–167)

- 그림 — Fig. 3: (a) 균열, (b) 접촉상실, (c) LE의 wetting과 SE의 점접촉을 액체와 고체 경우로 나란히 비교한 패널을 보면 된다. (L152 · 154–156)

### 입자 크기 설계

CAM 입자 안의 전자와 이온 수송 중 느린 쪽이 율속이므로 입자 크기에 상한이 있다. 원문은 이론용량 83 % 기준으로 L ≤ √(3·D̃_Li / C-rate)라는 해석식 Eq (1)을 제시했다. 작은 입자는 확산경로가 짧지만 SE-CAM 계면이 늘어 열화가 커지므로 최적 크기가 존재한다. (L183–184 · 187)

양극 수준에서는 SE와 CAM의 PSD를 서로 맞춰 packing density를 높이고 기공을 줄이라고 권고한다. 작은 SE와 구형 CAM이 packing에 유리하고, NCM 2차입자 3–5 µm이 입자 간 연결성에 유리하다고 원문은 적었다. CAM과 SE 크기의 네 조합 중 어느 것도 모든 축에서 좋지 않고, tailored PSD가 모든 축에서 최적이라는 것이 Fig 6의 정리다. (L173–175 · 198–199 · 202)

- 그림 — Fig. 6: Large/Small CAM과 Large/Small SE 네 칸의 장단점과 하단 tailored PSD 칸을 비교하면 된다. 어느 조성이 최적인지의 정량 위치는 그림에 없다. (L196 · 200 · 203)

### 어디까지 믿나

검토 측은 원문이 porosity, 밀도-압력 곡선, σ 측정값을 하나도 싣지 않은 정성 Perspective라고 본다. 시뮬레이션도 수행하지 않았고 Fig 4와 Fig 5는 계산식 곡선, Fig 7은 타 문헌 재인용이다. 그래서 원문이 직접 적은 수치는 설계 임계와 범위뿐이다. (L41 · 84 · 252 …)

검토 측은 연구실 문서가 이 논문에 귀속한 porosity 14 %, τ_ion 2.07 같은 값의 실제 출처를 Minnmann 2021 JES와 Sakuda 2013으로 정정했다. 이후 정정에서 순수 SE 기공 10 %는 2021 JES에도 없어 출처 미확인, 외부 앵커 없음으로 판정했다. (L40 · 44 · 49 …)

### 용어 풀이 (논문에 없는 일반 설명)

- **tortuosity**: 전하가 전극을 가로지를 때 실제로 지나는 경로가 직선 거리보다 얼마나 우회하는지를 나타내는 비율이다.
- **percolation**: 전도상이 전극 전체를 잇는 연결망을 이루어 전하가 끊김 없이 이동할 수 있게 되는 상태다.
- **PSD**: 입자 크기 분포(particle size distribution)로, 분말 입자들의 크기가 어떻게 퍼져 있는지를 나타낸다.

### 우리 연구에 주는 뜻

- Fig 2의 SE 고 tortuosity 설명은 우리 σ_ionic 식에서 C(τ) 항이 Bruggeman 너머로 필요한 이유의 정성 근거로 쓰인다. (L138–139)
- CAM 60–70 vol%, 작은 SE, tailored PSD 권고는 우리 production core(AM 70–85 wt%)와 bimodal Furnas dip 결론과 방향이 맞고, 우리는 그 dip의 정량 위치를 더한다. (L308–309 · 341)
- §5.4의 결합 mechanical-electrochemical-thermal 미세구조 모델 요구에 우리 DEM(transport)과 MPM(mechanics) 분업이 한 구현으로 응답한다고 본다. (L228–232)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| CAM 2차입자 권장 지름 | 3–5 µm | NCM 2차입자, 입자 간 연결성 | L88 |
| 기하모델 최적 CAM 분율 | 60–70 vol% | 기공, 균질도에 따라 | L131 |
| 이온 percolation용 CAM 분율(실험) | ~50 vol% | 실험 복합양극 | L130 |
| 상업셀 목표 CAM 분율 | ~70 vol% | 미래 상업셀 | L131 |
| sulfide SE σ_ion 상한 | ~25 mS/cm | LPS 계열, 상온 | L93 |
| LFP 본질 전자전도도 | ~10⁻⁹ S/cm | LFP, 도핑 없음 | L95 |

### 읽을 때 조심할 것

- 원문에는 porosity, σ, coverage 측정값이 없으므로 정량 앵커의 출처로 인용하면 오귀속이 된다고 검토 측은 지적한다. (L365–366)
- 60–70 vol% 같은 값은 범위 권고이지 측정값이 아니며, 원문이 dip을 측정했다고 말하면 과장이다. (L370–371)
- 원문의 수~수십 MPa는 작동 스택압이고 300 MPa나 380 MPa 같은 제조 cold-press 압력과 같은 숫자가 아니다. (L372–373)
- LFP, LMO, CuS의 σ_e 값은 NCM의 값이 아니므로 NCM 전자전도 식에 그대로 옮기면 안 된다. (L375–376)

### 원문에서 먼저 볼 곳

- Fig 6을 먼저 본다. CAM과 SE 크기 조합별 장단점과 tailored PSD 권고가 한 장에 정리되어 있다. (L194 · 202)
- §2.1과 Fig 2를 본다. CAM 분율 trade-off와 SE 양극의 tortuosity, 부분전도도 descriptor 논리가 여기 있다. (L129 · 133 · 146)
- §5.4 Modeling을 본다. 결합 미세구조 모델과 CAM 형상, 크기 재고를 요구하는 대목이다. (L228–230)

태그: NCM · LPSCl · halide SE · composite cathode · tortuosity · percolation · PSD · chemo-mechanics

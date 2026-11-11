# High-voltage stability of sulfide-based all-solid-state batteries: benefit of the parasitic reaction

*SE 코팅이 기생반응을 균일하게 만들어 Ni-rich 양극을 지킨다*

- Kang et al. · Chem. Commun 61, 16850-16853 (2025) · doi:10.1039/d5cc04349b · digest `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## SE 코팅이 기생반응을 균일하게 만들어 Ni-rich 양극을 지킨다

> LPSCl 건식 코팅은 고전압 기생반응을 막지 않고 고르게 퍼뜨린다. 그 결과 NCM811의 SOC가 균일하게 낮아져 구조 붕괴가 늦춰진다. (L24 · 32)

### 요점

1. NCM811 입자에 Li₆PS₅Cl을 건식 코팅했다. 4.25 V 충전 후 SOC 100 %로 저장하며 bare NCM과 OCV, 임피던스, 구조 변화, 사이클 수명을 비교했다. (L32 · 38 · 78)
2. SE-coated 쪽에서 기생반응은 더 많았지만 더 균일했고, 계면 저항은 낮았다. 200 사이클 용량유지율도 15.0 % 더 높았다. (L101 · 107 · 113 …)
3. 이로움은 분해산물의 보호막 때문이 아니라 균일한 SOC 강하에서 온다. 분해산물은 화학량론으로만 제시되었고 분광학으로 확인되지 않았다. (L16 · 251 · 254)

### 문제와 가설

Ni-rich 양극과 황화물 전해질의 계면에서는 고전압 기생반응을 피하기 어렵다. 원문은 LiNi₀.₈Co₀.₁Mn₀.₁O₂(NCM811)가 고-SOC(state of charge, 충전 상태)에서 격자 O를 내놓아 구조가 불안정해진다고 적었다. 짝을 이루는 Li₆PS₅Cl(LPSCl)은 산화 안정성이 낮다. 핵심 질문은 이 불가피한 반응을 어떻게 관리해야 고전압 수명을 얻느냐다. (L39–40 · 42 · 137)

원문의 답은 반응을 없애는 것이 아니라 균일하게 만드는 것이다. 고전압에서 LPSCl이 산화분해되면 Li⁺가 나오고, 이 Li⁺가 탈리튬된 NCM에 다시 들어가 SOC를 낮춘다. 원문은 bare NCM에서는 이 화학적 리튬화가 불균일해 해롭다고 적었다. 반면 conformal SE 코팅이 있으면 리튬화가 표면 전체에서 고르게 일어난다. (L20 · 22 · 131 …)

- 그림 — Fig. 4: bare와 SE-coated를 나란히 놓은 모식도다. 전극 수준의 void와 접촉 차이, 입자 수준의 불균일한 chemical lithiation과 균일한 chemical lithiation을 비교한다. (L135–136)

### 건식 코팅과 전극

SE-coated NCM은 무용매, 무바인더 건식 코팅으로 만들었다. NCM과 LPSCl을 100:2 wt% 비율로 planetary centrifugal mixer에 넣으면, 무른 LPSCl이 충돌 때 소성변형하며 입자를 덮는다. SEM/EDS에서 P와 Cl이 고르게 분포했다. XRD에서는 LPSCl 피크가 보이지 않아 원문은 전량이 conformal 코팅된 것으로 해석했다. (L76 · 92–93)

코팅은 복합 양극의 미세구조도 바꿨다. 단면 SEM에서 SE-coated 쪽 void가 더 작고 적었다. 원문은 LPSCl의 탄성계수 22.1 GPa가 NCM의 175 GPa보다 훨씬 낮아서 압연 때 void를 채운다고 설명했다. 공정한 비교를 위해 코팅분만큼 추가 SE를 줄여 총 SE량을 bare와 맞췄다. (L57 · 77 · 96)

- 그림 — Fig. 1: (d)와 (e)의 단면 SEM에서 void 크기와 SE/CAM 접촉을 비교한다. (a), (b)의 EDS 맵은 P와 Cl 분포로 코팅 균일성을 보여 준다. (L92 · 96)

### 저장 중 반응과 수명

4.25 V vs Li/Li⁺까지 충전해 SOC 100 %로 저장하자 SE-coated 셀의 OCV가 더 빨리 떨어졌다. 200 h에서 강하폭은 10.1 mV 더 컸다. Li–In 음극의 전위는 0.62 V로 고정되어 있다. 그래서 원문은 이 강하를 양극 쪽 self-discharge, 곧 기생반응이 더 많이 일어난 결과로 해석했다. (L78 · 101–102)

반응이 더 많았는데도 계면 저항과 수명은 SE-coated가 나았다. 수정 TLM(transmission-line model)으로 분리한 계면 저항은 200 h 시점에 SE-coated가 4.3 Ω cm²로 bare보다 낮았다. 저장 뒤 용량 강하는 bare가 26.4, SE-coated가 24.4 mAh/g였다. 200 사이클 용량유지율은 SE-coated가 15.0 % 더 높았다. (L106–107 · 112–113)

- 그림 — Fig. 2: (b)의 저장 중 OCV 곡선과 (g)의 사이클 유지율을 함께 본다. (d)와 (e)는 저장 시점별 R_int와 R_w의 추이를 보여 준다. (L197 · 199 · 201)

### 균일화의 구조 증거

저장 후 XRD는 chemical lithiation이 실제로 일어났고 코팅이 그것을 고르게 만들었음을 보여 준다. 두 시료 모두 피크가 저각으로 이동해 Li 농도가 늘었고, 이동폭은 SE-coated가 더 컸다. bare는 (003) 피크 분리가 뚜렷해 입자마다 Li 농도가 달랐다. SE-coated는 균일했다. (L117–118)

TEM/FFT는 상전이가 얼마나 깊이 들어갔는지를 보여 준다. bare NCM은 표면의 layered 구조가 rock-salt(Fm-3m)로 바뀌었고, 이 변화가 깊이 침투했다. SE-coated NCM은 최외곽만 rock-salt이고 내부는 layered가 남았다. 원문은 rock-salt 형성이 격자 O 손실을 뜻하며, 이것이 LPSCl 분해를 가속해 저항을 키운다고 적었다. (L122–124)

- 그림 — Fig. 3: (a), (b)에서 저장 전후의 피크 이동과 bare의 (003) 분리를 본다. (c), (d)에서는 rock-salt 층의 두께 차이를 본다. (L202–203)

### 해석의 한계

검토 측은 이로움의 핵심이 passivating CEI가 아니라 균일한 SOC 강하라고 본다. 식 (1)의 산물 가운데 절연성은 LiCl뿐이고 P₂S₅와 S는 전도성이다. 그래서 분해산물이 보호막을 만든다는 흔한 설명은 이 논문에 맞지 않는다는 판단이다. (L16 · 251)

검토 측은 측정 범위의 한계도 지적한다. P₂S₅, S, LiCl은 식 (1)의 화학량론상 산물이며 XPS로 검출한 것이 아니다. 논문에는 DFT 계산이 없고 이온전도도와 band gap 값도 없다. 검토 측은 이 효과가 격자 O를 내놓는 Ni-rich 양극에 특유한 것이어서, LCO 같은 안정한 양극에서는 이득이 작을 수 있다고 본다. (L71–72 · 253–254 · 256)

### 용어 풀이 (논문에 없는 일반 설명)

- **chemical lithiation**: 외부 전류 없이 화학 반응으로 생긴 Li⁺가 양극 격자에 들어가 충전 상태를 낮추는 현상이다.
- **(003) peak splitting**: 층상 양극의 XRD (003) 반사가 둘 이상으로 갈라지는 것으로, 입자마다 Li 농도가 다르다는 신호다.
- **TLM**: 다공성 복합전극의 임피던스를 계면 저항, 확산 저항, 이온과 전자 경로로 나누어 해석하는 등가회로 모형이다.

### 우리 연구에 주는 뜻

- 우리 grand-potential 계산에서 comp1의 고전압 산화분해 종착산물은 P₂S₇/P₂S₅계, 원소 S, LiCl이다. 이는 식 (1)의 우변과 같은 화학 패밀리다. (L167 · 176)
- 우리가 계산한 산물별 band gap에서 절연체는 6.65 eV의 LiCl뿐이고 나머지는 전도성이다. 이 결과는 이로움이 passivation이 아니라 SOC 강하에서 온다는 해석을 뒷받침한다. (L170 · 182)
- 우리 Nd 도핑의 wide-gap CEI와는 보호 경로가 다르다. 따라서 이 논문을 Nd passivation의 실험 증거로 쓰지 않고, 코팅과 도핑이라는 상보적인 두 레버로 함께 다룬다. (L172 · 239)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 200 사이클 용량유지율 격차 | 15.0 % | SE-coated 대 bare, 고-SOC 저장 후 | L113 |
| 계면 저항 R_int | 4.3 Ω cm² | SE-coated, 200 h 저장 시점 | L107 |
| 추가 OCV 강하 | 10.1 mV | SE-coated, SOC 100 % 저장 200 h | L101 |
| 저장 후 용량 강하 | 24.4 mAh/g | SE-coated, aged 후 0.5C | L63 |
| 평균 쿨롱효율 | 94.2 % | bare, aged 후 초기 70 사이클 | L113 |
| 코팅 비율 NCM:LPSCl | 100:2 wt% | 건식 코팅 공정 | L76 |

### 읽을 때 조심할 것

- 이로움은 균일한 chemical lithiation에서 온다. 전도성 분해산물이 대부분이므로 이 논문을 passivating CEI 사례로 인용하면 안 된다. (L251)
- P₂S₅, S, LiCl은 식 (1)의 화학량론상 산물이며 XRD, TEM, EIS만 측정되었다. (L72 · 254)
- self-discharge 해석은 Li–In 음극의 전위가 0.62 V로 고정되어 있다는 가정에 기대고 있다. (L255)
- 효과는 NCM811 같은 Ni-rich 양극에 특유할 수 있으며, 원문에는 이온전도도, band gap, XPS 값이 없다. (L253 · 256)

### 원문에서 먼저 볼 곳

- Fig. 2b와 2g. 기생반응이 더 많았다는 OCV 근거와 수명 격차가 한 그림에 있다. (L197 · 201)
- Fig. 3a,b. 저각 이동과 (003) 분리로 리튬화의 균일성을 판단한 직접 증거다. (L202)
- 식 (1)과 이를 설명하는 본문 부분. Li⁺ 이동이 접촉 영역에 국한된다는 주장이 코팅이 필요한 이유를 설명한다. (L128 · 131)

태그: Li₆PS₅Cl · NCM811 · dry coating · chemical lithiation · calendar aging · TLM · rock-salt

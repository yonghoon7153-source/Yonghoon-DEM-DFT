# Dry‐Crafted Charge‐Conductive ZrO₂ − x Cathode Shell Coating for High‐Performance Sulfide‐Based Solid‐State Batteries

*산소결핍 ZrO₂₋ₓ 코팅은 전도를 지키며 황화물 계면 부반응을 줄인다*

- Choi et al. · Small 22, e73805 (2026) · doi:10.1002/smll.73805 · digest `choi2026_bzox_dry_zro2x_nmc_shell_coating`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 산소결핍 ZrO₂₋ₓ 코팅은 전도를 지키며 황화물 계면 부반응을 줄인다

> 건식 코팅한 black ZrO₂₋ₓ 셸은 NMC811의 전하 수송을 보존하면서 LPSCl 계면 부반응을 억제해 초기 CE를 69.6에서 77.5 %로 올렸다. (L19 · 42 · 44)

### 요점

1. 산소결핍 black ZrO₂₋ₓ(BZOx)와 화학양론 white ZrO₂(WZO)를 무용매 mechanofusion으로 단결정 NMC811에 입히고, Li₆PS₅Cl(LPSCl) 전고체 셀에서 전기화학 시험과 DFT+U 계면 슬랩 계산으로 비교했다. (L19 · 26 · 33 …)
2. WZO는 전자 절연 장벽이 되어 계면 저항이 192.9 Ω까지 컸지만, BZOx는 55.2 Ω로 bare급 저항을 유지하면서 초기 CE와 100 cycle 방전용량을 가장 높였다. (L19 · 44 · 52 …)
3. 용량 유지율 자체는 WZO가 가장 높고, DFT는 분해 열역학 없이 정적 pDOS와 결합길이만 보았으므로 BZOx의 계면 안정성은 시사 수준으로 읽어야 한다. (L53 · 166 · 169)

### 절연 코팅의 딜레마

황화물 고체전해질과 산화물 양극이 만나면 POₓ, SOₓ, 폴리설파이드 같은 부반응 산물이 생긴다. 원문은 첫 사이클 비가역 손실을 SE 분해와 양극 표면 O와 SE의 P, S 반응으로 설명한다. 절연성 산화물 코팅은 이 반응을 막지만 전하 수송도 함께 막는다. (L19 · 45)

원문은 밴드갭이 0.5 eV보다 작은 코팅은 전자전도가 지나쳐 SE 표면 분해를 부추기고, 절연 코팅은 rate에서 손해를 본다고 적었다. 그래서 그 사이의 mixed ionic-electronic 창에 드는 BZOx를 골랐다. BZOx의 밴드갭은 선행논문 인용값으로 0.5–2.25 eV다. (L37)

- 그림 — Fig. 1: mechanofusion 세 단계와, 비코팅 계면의 space-charge layer와 BZOx 계면의 O 공공 경유 전하수송을 대비한 만화를 보면 된다. space-charge 완화 주장은 이 모식도로만 제시된다. (L111)

### 무용매 건식 셸

BZOx는 PVP 보조 졸을 공기 중 하소한 뒤 H₂/Ar에서 환원 어닐해 만들었다. 코팅은 Hosokawa Nob-Mini로 코팅재와 NMC를 3:97 wt로 섞어 두 단계 회전으로 입혔다. (L32–33)

HR-TEM에서 셸 두께는 WZO가 ~9.7 nm, BZOx가 ~8.1 nm였고 EDS에서 Ni, Zr, O가 고르게 분포했다. Zr 3d XPS에서 BZOx에만 180.68 eV 환원 Zr 성분이 나타나, 원문은 이를 산소공공 형성의 증거로 제시했다. (L34–35)

- 그림 — Fig. 2: a, b의 HR-TEM 셸 두께와 k, l의 Zr 3d XPS에서 BZOx에만 있는 낮은 결합에너지 shoulder를 보면 된다. (L34–35 · 112)

### 첫 사이클과 수명

BZOx 코팅은 첫 사이클 손실과 분극을 함께 줄였다. 초기 CE는 pristine NMC 69.6 %에서 77.5 %로 올랐고, 비가역 손실은 45.84 mAh g⁻¹로 가장 작았다. WZO는 hysteresis가 0.73 V로 커지고 초기 CE가 62.3 %로 떨어졌다. (L42–45)

100 cycle 뒤 방전용량은 BZOx가 126.69 mAh g⁻¹로 pristine보다 높았다. 다만 유지율만 보면 WZO가 85.8 %로 가장 높고 BZOx는 80.4 %다. WZO의 높은 유지율은 절대용량이 낮아서 생긴 결과이고, BZOx의 우위는 절대용량, CE, hysteresis의 조합이다. (L50–53)

- 그림 — Fig. 3: a에서 c까지 첫 사이클 전압곡선의 충방전 간격과 d의 초기 CE 막대, e의 100 cycle 용량과 CE를 함께 보면 된다. (L113)

### 병목은 전자전도

WZO의 손해는 양극과 SE 사이 저항에서 드러난다. 첫 사이클 후 R_CA-SE는 NMC 44.5 Ω, WZO 192.9 Ω, BZOx 55.2 Ω였다. DC 분극으로 잰 코팅 NMC 펠릿의 σ_e는 WZO에서 pristine의 25.5분의 1, BZOx에서 3.8분의 1로 줄었다. (L60 · 67–68)

GITT 과전압은 WZO가 97.7 mV로 BZOx의 46.2 mV보다 두 배가량 컸다. 정규화 확산계수는 방전 시 세 시료가 비슷해, 원문은 WZO의 병목이 이온이 아니라 전자전도라고 해석했다. (L72–73)

- 그림 — Fig. 4: b의 CA-SE 저항 막대에서 WZO만 튀는 것과 d의 과전압 비교를 보면 된다. (L114)

### 계면 화학과 한계

50 cycle 뒤 XPS에서 POₓ 성분은 pristine NMC에만 나타나, 두 코팅 모두 SE 분해를 완화했다. DFT에서 LNO-LPSCl 계면 S의 pDOS 피크는 E_F 바로 아래에 있었고, Zr 산화물과 접촉하면 더 낮은 에너지로 내려갔다. 원문은 BZOx-LPSCl에서 Zr–S와 P–Cl 상호작용이 생겨 SO₂ 발생이 억제된다고 적었다. (L84 · 104–105)

검토 측은 DFT가 정적 슬랩의 pDOS와 결합길이뿐이고 분해 열역학이 없어 BZOx 안정성을 증명했다고 보기는 어렵다고 본다. Zr–S 결합 형성은 계면이 화학적으로 활성이라는 뜻일 수도 있고, DFT 모델 ZrO₁.₃₃은 실험 지문 ZrO₁.₈보다 공공이 훨씬 많다. 또 본문의 1C rate 값은 SI 그래프와 어긋나, 검토 측은 BZOx가 WZO보다 낫다는 것까지만 인용한다. (L151 · 165 · 167 …)

- 그림 — Fig. 5: a, b의 S 2p와 P 2p에서 산화종과 POₓ 성분을, c, d에서 계면 S와 격자 S의 pDOS 위치 차이를 보면 된다. (L83–84 · 115)

### 용어 풀이 (논문에 없는 일반 설명)

- **mechanofusion**: 고속 회전 챔버의 전단과 압축으로 나노입자를 호스트 입자 표면에 용매 없이 융착시키는 건식 코팅법이다.
- **DC 분극법**: 이온을 차단한 전극 사이에 정전압을 걸어 정상상태 전류에서 전자전도도만 분리해 내는 측정이다.
- **pDOS**: 전자 상태밀도를 원자나 궤도별로 나눠 본 것으로, 특정 원자의 전자 준위가 페르미 준위에 얼마나 가까운지 보는 데 쓴다.

### 우리 연구에 주는 뜻

- 원문의 계면 S pDOS 하강은 우리가 벌크에서 정량화한 free-S site-PDOS ⟨3p⟩ 지표가 −1.1 eV에서 B–S 결합 시 −2.15 eV로 내려가는 것과 같은 관측량 계열이며, 원문은 창과 수치 없이 음영으로만 보였다. (L139 · 161)
- 원문의 S 2p 자리분해 XPS는 우리 free-S와 PS₄-S site-PDOS 예측을 실험과 짝지어 검증할 표준 포맷이 된다. (L140 · 156)
- BZOx와 LPSCl이 화학 분해를 일으키는지는 우리 interface_reactivity에 Zr hull을 추가하면 계산으로 판정할 수 있는 열린 질문이다. (L151)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 초기 쿨롱 효율 | 77.5 % |  | L44 |
| 첫 사이클 hysteresis | 0.18 V |  | L44 |
| 100 cycle 방전용량 | 126.69 mAh g⁻¹ |  | L52 |
| 양극-SE 계면저항 R_CA-SE | 192.9 Ω | NMC-WZO, 첫 사이클 후 EIS | L60 |
| 양극-SE 계면저항 R_CA-SE | 55.2 Ω | NMC-BZOx, 첫 사이클 후 EIS | L60 |
| 전자전도도 σ_e | 3.88×10⁻⁵ S/cm |  | L68 |

### 읽을 때 조심할 것

- 최고 유지율은 WZO의 85.8 %이므로 BZOx가 유지율 최고라고 인용하면 틀리며, 결론부의 80.4 % 개선 문구도 오독을 부른다. (L53 · 166)
- 본문의 1C rate 값은 SI Fig S5와 크게 어긋나고 pristine과의 비교가 빠져 있어, rate는 BZOx가 WZO보다 낫다는 데까지만 쓸 수 있다. (L165)
- σ_e 값은 코팅 NMC 펠릿의 값이라 SE bulk 전자전도도와 섞어 쓰면 안 된다. (L69 · 174)
- DFT의 BZOx 모델은 ZrO₁.₃₃이고 LPSCl은 단일 ordered 배열이라, pDOS 결론은 정성 인용까지만 가능하다고 검토 측은 본다. (L167 · 175)

### 원문에서 먼저 볼 곳

- Fig 3: 초기 CE, hysteresis, 100 cycle 거동 등 핵심 성능이 모두 여기서 나온다. (L113)
- Fig 4와 Fig S6: EIS, GITT, DC 분극으로 WZO의 병목이 전자전도라고 판정한 논리를 확인할 수 있다. (L114 · 124)
- Fig S5와 본문 rate 문장: 1C 용량 값이 서로 맞지 않으므로 인용 전에 직접 대조해야 한다. (L76–77 · 123)

태그: LPSCl · NMC811 · ZrO₂₋ₓ · mechanofusion · DFT+U · pDOS · EIS

# Density Functional Theory for Battery Materials

*배터리 재료 DFT는 functional부터 검증해야 한다*

- He et al. · Energy & Environmental Materials 2019 · doi:10.1002/eem.12056 · digest `he2019_dft_for_battery_materials_review`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 배터리 재료 DFT는 functional부터 검증해야 한다

> 배터리 재료 DFT를 다섯 축으로 정리하고, 에너지 계산에는 PBE보다 SCAN이나 HSE06을 권한다. (L22 · 118)

### 요점

1. 구조안정성, 반응전압과 용량, 전자구조, 이온수송, 흡착의 다섯 축으로 배터리 재료 DFT의 용법을 정리하고 functional을 비교했다. (L22 · 29)
2. 원문은 PBE가 전압을 수 십 분의 1 V, band gap을 약 1 eV 과소평가하며, SCAN이 gap, 전압, DOS를 가장 균형 있게 준다고 적었다. (L22 · 110 · 116)
3. 검토 측은 이 리뷰가 정적 DFT 관행의 근거는 되지만 고체전해질의 grand-potential 분해창이나 MLIP은 다루지 않는다고 본다. (L17 · 19 · 203)

### functional이 핵심

원문은 DFT의 정확도가 교환상관(XC) functional의 품질에 좌우된다고 적었다. LSDA는 격자상수는 잘 맞히지만 반응 장벽을 과소평가하고 결합을 과결합한다. GGA의 대표인 PBE는 결합에너지에 더 유용하지만 band gap과 장벽 높이를 여전히 과소평가한다. (L37–39)

다음 세대는 운동에너지 밀도를 넣은 meta-GGA인 SCAN과 HF 교환을 섞은 hybrid인 HSE다. 원문은 배터리 재료 계산의 주류가 GGA, 특히 PBE라고 적었다. (L40–41)

### 안정성과 전압

구조안정성은 cohesive energy, formation energy, Gibbs 자유에너지, phonon의 네 지표로 본다. 원문은 0 K 안정성에는 원소 표준상태를 기준으로 한 formation energy가 cohesive energy보다 나은 기술자라고 적었다. phonon에서 허수 진동수가 나오면 동역학적으로 불안정하다고 판정하지만 계산비용이 크다. (L46 · 52 · 54 …)

반응전압은 Δ_rG = −nFE에서 얻고, 고체상에서는 Δ_rG를 DFT 총에너지 차로 근사한다. 전압 프로파일은 formation energy convex hull과 직결된다. 고용체는 전압이 연속으로 줄고, 2상 공존은 plateau를, 중간 안정상은 다단 plateau를 만든다. (L65–66 · 69–72)

- 그림 — Fig. 3: 위쪽 자유에너지 곡선과 아래쪽 전압 프로파일을 짝지어 보면 고용체, 2상 전이, 중간상의 세 경우가 구별된다. (L70–72)

### 전자구조와 수송

band gap은 PBE로 구하면 작게 나오고 hybrid로 보정한다. 원문의 예에서 Mg₃N₂의 PBE gap은 0.91 eV였고 HSE06으로 다시 계산하면 1.92 eV였다. DOS 비교에서도 PBE는 E_F 근처 금속 d 상태를 과소평가하고 PBE+U는 O 2p를 과대평가하며 SCAN이 더 정확하다고 적었다. (L84 · 87)

이온수송은 NEB로 한 경로의 활성화 장벽을 구하거나 AIMD로 확산계수와 전도도를 구한다. LiMn₂O₄에서는 bulk E_a 0.33 eV가 나노입자에서 0.59 / 0.72 eV로 올라 작은 입자가 확산을 방해함을 보였다. 원문은 AIMD가 실험과 비교할 수 있는 값을 주지만 계산비용이 크다고 적었다. (L94–96)

- 그림 — Fig. 8: Mg₃N₂의 DOS와 밴드 구조에서 PBE와 HSE06의 gap 차이를 확인한다. (L138)

### functional 비교

결론절은 production 계산 전에 functional을 반드시 검증하라고 권한다. LDA와 GGA는 전이금속 d 전자의 self-interaction 때문에 반응전압을 수 십 분의 1 V 과소평가한다. GGA+U는 리튬화 전압을 훨씬 정확히 주지만 U가 계마다 다르고, 산화물 formation energy에는 GGA가 낫다고 적었다. (L108 · 110 · 112)

HSE06은 formation energy, 부피, 삽입전압에서 GGA+U급 정확도를 보이지만 비용이 훨씬 크다. SCAN은 gap과 절대전압을 PBE보다, DOS와 반응전압을 PBE+U보다 잘 준다. 다만 약결합 intermetallic의 formation energy 오차는 PBE보다 크다. 원문은 전압 같은 에너지 계산에 SCAN이나 HSE06을 권한다. (L114 · 116 · 118)

- 그림 — Fig. 11: LiNiO₂, LiCoO₂, LiMnO₂의 DOS를 PBE, PBE+U, SCAN으로 나란히 비교하며 d와 O 2p 위치 차이를 본다. (L87 · 141)

### 어디까지 믿나

검토 측은 2019년 리뷰라서 r²SCAN, foundation MLIP, 최신 grand-potential 계면 도구를 다루지 않는다고 본다. 예시도 대부분 전극, 음극, 2D 재료이고 argyrodite나 황화물 고체전해질 예시는 없다. (L17 · 19 · 202)

원문은 전해질의 전기화학창을 Goodenough의 HOMO/LUMO band-edge 그림으로만 다룬다. 검토 측은 고체전해질의 산화가 전자 하나의 제거가 아니라 상 분해이므로 band-edge 창이 실제 분해창을 2–3배 과대평가한다는 Schwietert 2020의 논증을 든다. 따라서 이 그림은 band alignment 용도로만 써야 한다고 본다. (L19 · 81–82 · 204)

- 그림 — Fig. 7: 전해질 gap과 양극, 음극 전기화학 퍼텐셜의 상대 위치로 안정창을 정의하는 방식을 본다. (L81 · 137)

### 용어 풀이 (논문에 없는 일반 설명)

- **교환상관(XC) functional**: Kohn–Sham DFT에서 전자 사이의 교환과 상관 에너지를 근사하는 식으로, 그 형태가 계산 정확도를 좌우한다.
- **convex hull**: 조성에 따른 formation energy의 아래쪽 볼록 포락선으로, 그 위에 놓인 상이 열역학적으로 안정하다.
- **NEB**: 두 안정 위치 사이의 최소 에너지 경로를 이미지 사슬로 찾아 이동 장벽을 구하는 방법이다.

### 우리 연구에 주는 뜻

- 우리 정적 DFT 백본은 PBE와 MP의 GGA/GGA+U hull이어서, 원문의 배터리 계산은 PBE가 주류라는 서술이 functional 선택의 표준 근거가 된다. (L43 · 121)
- 우리 grand-potential ESW는 원문 §3의 닫힌계 평균전압을 Li 화학퍼텐셜을 연 계로 확장한 것이지만, 그 절차의 출처는 이 리뷰가 아니라 Mo2012다. (L74–76)
- 우리 주재료는 전이금속이 없는 황화물이라 U가 필요 없고, Nd 도핑만 4f에 +U를 쓰며, 리뷰의 1순위 추천인 SCAN은 MP 정합과 mixing noise 회피 때문에 쓰지 않았다. (L122 · 124)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| Mg₃N₂ PBE band gap | 0.91 eV | Mg₃N₂ LIB 음극, PBE | L84 |
| Mg₃N₂ HSE06 band gap | 1.92 eV | Mg₃N₂, HSE06 재계산 | L84 |
| LiMn₂O₄ bulk Li 이동 장벽 | 0.33 eV | bulk LMO, DFT+NEB | L95 |
| LiMn₂O₄ 나노입자 Li 이동 장벽 | 0.59 / 0.72 eV | 나노입자 LMO, DFT+NEB | L95 |
| Nb₂O₅ 경로별 Li 이동 장벽 | 0.33 / 0.25 eV | Nb₂O₅ path A/B, NEB | L95 |
| COF 음극 cohesive energy | 4.6 eV/atom | NUS-2, Li 흡착 후 | L49 |

### 읽을 때 조심할 것

- 방법 리뷰이므로 argyrodite나 황화물 고체전해질의 물성값 출처로 쓸 수 없다. (L202)
- 이 리뷰가 grand-potential 분해창을 정당화한다고 인용하면 부정확하며, 리뷰가 주는 것은 Δ_rG = −nFE 평균전압의 근간뿐이다. (L204)
- r²SCAN과 foundation MLIP 이후의 방법은 다루지 않으므로 그 표준성은 후속 문헌에서 찾아야 한다. (L203)
- Fig 7의 band-edge 안정창은 검토 측이 고체전해질 분해창을 과대평가한다고 보므로 분해 전압 근거로 쓰지 않는다. (L82 · 137)

### 원문에서 먼저 볼 곳

- §7과 Fig 21, Fig 11: GGA, GGA+U, HSE06, SCAN의 전압 오차와 DOS 차이를 정량 비교한 결론절이다. (L107 · 141 · 146)
- Fig 8과 §4.2: PBE gap 과소평가와 HSE06 보정을 수치로 보여 주는 예다. (L84 · 138)
- Fig 3과 §3.2: convex hull과 전압 plateau의 관계를 보여 주는 기본 그림이다. (L69 · 72 · 133)

태그: DFT · GGA+U · HSE06 · SCAN · convex hull · NEB · AIMD · band gap

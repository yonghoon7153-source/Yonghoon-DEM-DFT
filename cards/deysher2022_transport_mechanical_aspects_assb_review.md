# Transport and mechanical aspects of all-solid-state lithium batteries

*전고체전지의 병목은 복합 양극의 전달과 역학이다*

- Deysher et al. · Materials Today Physics 24, 100679 (2022) · doi:10.1016/j.mtphys.2022.100679 · digest `deysher2022_transport_mechanical_aspects_assb_review`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 전고체전지의 병목은 복합 양극의 전달과 역학이다

> SE 벌크 전도도는 충분해졌으므로 이제 복합 양극 내부의 전달과 부피변화 역학이 전고체전지의 율속 병목이라고 정리한 리뷰다. (L53–56)

### 요점

1. 복합 양극의 이온·전자 전달 한계와 부피변화에서 오는 역학 한계를 현상과 실험 특성화 방법 중심으로 종합한 리뷰다. (L8–10 · 53)
2. 원문은 연구 초점을 복합 양극 내부로 옮겨야 하고, 그 전달을 이해하려면 EIS, CV, DC 분극 같은 올바른 전기화학 측정이 필요하다고 적었다. (L20 · 54–56)
3. 자체 측정이나 시뮬레이션이 없어 모든 수치는 인용값이므로, 값을 쓸 때는 원 출처를 함께 밝혀야 한다. (L65 · 68 · 291–292)

### 병목의 이동

원문은 SE의 벌크 이온전도도가 이미 충분히 높아졌다고 본다. 그 예로 LGPS가 RT에서 12 mS/cm에 이른다는 인용을 든다. 그런데도 문헌 대부분의 areal capacity는 < 2 mAh/cm²에 머물고, RT Li-metal 셀의 current density도 < 2 mA/cm²에 그친다. (L55 · 73 · 76 …)

원문은 그래서 연구 초점이 복합 양극 내부의 전달, 역학, 계면으로 이동해야 한다고 적었다. 소재계는 NMC 양극, Li₆PS₅Cl(LPSCl) 전해질, Si와 Li 음극이다. (L7 · 55–56 · 61)

- 그림 — Fig. 1: current density를 발표연도에 대해 찍은 문헌 조사 그림이며 점 크기가 areal loading이다. 녹색 점선이 ARPA-E 목표 3 mA/cm²이고, Tan의 5 mA/cm²와 Lee의 6.8 mAh/cm² 결과가 상단에 있다. (L77 · 125)

### 양극 안의 전달

원문은 전도도를 σ = t/(R·A)로 쓰고, SE를 얇게 코팅해 두께 t를 줄이는 것을 핵심 논리로 삼는다. 인용된 이온수송망 모델은 SSE 입자가 작고 CAM 로딩이 낮을수록 이용률이 오른다고 보였다. 또 다른 인용 모델은 고-CAM 조성에서 full 이용률을 얻으려면 < 20 % porosity가 필요하다고 했다. (L82 · 111–112 · 115 …)

전자 경로도 필요해서 carbon이 없으면 이용률이 떨어지고, SSE:carbon 비에는 최적점이 있다. 다만 비표면적이 큰 carbon black은 SE 분해를 키우고 VGCF는 분해가 적다고 원문은 적었다. LPSCl의 산화 한계는 2.1 V vs Li/Li⁺로 인용되었다. (L100 · 127–128 · 130)

- 그림 — Fig. 2: a와 b에서 SSE-to-CAM 크기비에 따른 이용률 맵을, c에서 SSE:carbon 비의 최적점을 본다. f는 carbon 종류별 분해 kinetics 차이를 보여 준다. (L126–127 · 130)

### 부피변화와 접촉

원문의 중심 메커니즘은 반복된 팽창과 수축이 입자 사이 void를 만들고, 접촉 손실이 이온수송을 막는다는 것이다. NMC의 부피변화는 1–3 %로 인용되었다. Li₃PS₄+NMC 셀을 370 MPa로 다시 누르면 잃은 용량이 상당히 돌아왔다는 결과도 인용되었다. (L79 · 81 · 133 …)

완화책으로는 방사상 결정립 설계와, 부피변화 추세가 반대인 LiCoO₂와 NMC를 섞어 net-zero를 노리는 방법이 소개된다. Li 음극 쪽에서는 Li creep yield가 ~0.8 MPa이고, Li₆PS₅Cl 대칭셀의 critical stripping 전류가 3 MPa에서 0.2, 7 MPa에서 1.0 mA/cm²로 인용되었다. 원문은 SE와 그 복합체의 역학 물성에 지식 공백이 크다고 명시했다. (L93–94 · 118–119 · 134–135)

- 그림 — Fig. 3: a에서 pristine과 cycled 양극의 cathode|SSE 계면 void를 비교한다. c에서 LiCoO₂와 NMC의 부피변화가 반대 방향인 점을 본다. (L133 · 135)

### 측정법 처방

원문은 이온과 전자 기여를 가르려면 EIS와 저bias DC 분극을 함께 써야 한다고 적었다. 혼합전도체(MIEC)에서는 전자 누설로 capacitive tail이 사라지므로 electron-blocking layer와 composite carbon electrode가 필요하다. (L147–149)

CV로 안정성창을 잴 때 semi-blocking planar 전극은 분해전류를 과소평가한다고 원문은 지적한다. 그 예로 LGPS의 겉보기 안정성창은 0–5 V였지만 실제로는 환원 1.71, 산화 2.15 V였다. 그래서 carbon-composite 전극으로 측정해야 한다고 적었다. (L99 · 150–151)

- 그림 — Fig. 6: a의 planar 전극과 b의 carbon-composite 전극에서 분해 전류 크기를 비교한다. c부터 e에서 MIEC 측정 구성과 두 semicircle EIS, DC 분극을 본다. (L140–142)

### 어디까지 믿나

검토 측은 이 리뷰에 자체 측정이 없으므로 수치를 리뷰가 아니라 원전으로 인용해야 한다고 본다. 예를 들어 porosity 임계는 Bielefeld, 6.8 mAh/cm²는 Lee, 370 MPa는 Koerver의 값이다. (L65 · 291–292)

검토 측은 Li-metal과 anode-less 셀의 부피팽창이 Li 상의 물리이므로 SE와 양극 미세구조에 그대로 옮기면 안 된다고 본다. multilayer 팽창 값은 그림 곡선에서 읽은 추세라 정밀값이 아니라고 덧붙였다. (L251–252 · 293–294 · 301)

- 그림 — Fig. 5: 층 수가 늘수록 셀 팽창이 선형으로 커지는 경향만 읽는다. 검토 측은 그림의 값이 판독 추세라고 본다. (L139 · 301)

### 용어 풀이 (논문에 없는 일반 설명)

- **복합 양극**: 활물질, 고체전해질, 도전재를 섞어 이온과 전자가 모두 활물질에 닿도록 만든 전고체전지 양극층이다.
- **MIEC**: 이온과 전자를 함께 전도하는 혼합전도체로, 두 기여를 측정에서 분리해야 하는 물질이다.
- **stack pressure**: 셀을 작동하는 동안 적층 방향으로 가해 계면 접촉을 유지시키는 외부 압력이다.

### 우리 연구에 주는 뜻

- 리뷰가 말로 묶은 부피변화, void, 접촉 손실, 전달 저하의 결합은 우리 DEM 접촉망 σ 계산과 MPM void-fill 분업이 계산으로 다루는 현상이다. (L13–15 · 168)
- 우리 DEM porosity ~10–15.6 %는 인용된 < 20 % 임계 영역에 들지만, 그쪽은 입력 porosity이고 우리는 압밀로 예측한 값이라 결론 방향만 비교한다. (L177 · 200 · 297–298)
- 리뷰가 future-direction으로 남긴 cycling과 operando 시간축은 우리 정적 RVE 모델도 갖지 못한 공유 gap이다. (L215–216 · 249)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| best-case areal capacity | 6.8 mAh/cm² | 60 ℃, Ag–C pouch, NMC+LPSCl | L74 |
| best full cell current density | 5 mA/cm² | NCM811+LPSCl μSi full cell | L75 |
| 대표 SE 벌크 이온전도도 | 12 mS/cm | LGPS, RT | L78 |
| NMC 부피변화 | 1–3 % | layered oxide de/lithiation | L79 |
| void-fill 회복 재가압 압력 | 370 MPa | Li₃PS₄+NMC, 첫 수십 cyc 후 | L81 |
| full 이용률 porosity 조건 | < 20 % porosity | 고-CAM wt%, 미세구조 모델 | L82 |

### 읽을 때 조심할 것

- 모든 수치가 다른 논문에서 인용한 값이므로 리뷰를 1차 출처로 쓰지 말고 원전 ref 번호를 함께 적어야 한다. (L65 · 68 · 291–292)
- Li-metal과 anode-less 셀의 부피팽창 값은 Li 상의 물리라서 SE나 양극 미세구조 값으로 옮기면 안 된다. (L251–252 · 293–294)
- LGPS 12 mS/cm 같은 벌크 σ는 LPSCl과 소재가 달라 LPSCl 앵커로 쓸 수 없다. (L204 · 295–296)
- Fig 5의 multilayer 팽창 값은 곡선에서 읽은 추세라 정밀값이 아니다. (L91 · 301)

### 원문에서 먼저 볼 곳

- Fig 3a에서 부피변화 반복이 계면 void와 접촉 손실로 이어지는 SEM 증거를 먼저 본다. (L133 · 170–171)
- Fig 2a–c에서 SSE 입경비와 SSE:carbon 비가 이용률을 어떻게 바꾸는지 본다. (L126–127)
- 전기화학 특성화 절과 Fig 6에서 EIS, DC 분극, carbon-composite CV 측정 처방을 본다. (L145 · 147 · 150–151)

태그: Li₆PS₅Cl · NMC · 복합 양극 · void formation · stack pressure · EIS · porosity · 리뷰

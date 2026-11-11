# Robust interface and reduced operation pressure enabled by co-rolling dry-process for stable all-solid-state batteries

*co-rolling 건식 박막 SSE는 2 MPa 저압에서도 작동한다*

- Lee et al. · Nat Commun 16, 4200 (2025) · doi:10.1038/s41467-025-59363-4 · digest `lee2025_corolling_dryprocess_lpscl_ptfe`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## co-rolling 건식 박막 SSE는 2 MPa 저압에서도 작동한다

> 박막 LPSCl 층과 양극을 함께 압연하면 바인더-VGCF 섬유망이 계면을 묶어 저압 사이클이 안정해진다. (L45 · 78 · 91)

### 요점

1. LPSCl SSE 막과 NCM 양극 막을 건식 co-rolling으로 함께 압연하고, 공정 변수, 계면 강도, 전달, 저압 사이클을 실험으로 평가했다. (L20 · 62 · 80)
2. co-rolled 셀은 2 MPa에서 500 사이클 동안 용량을 >80% 유지했고, 양극의 PTFE 함량을 늘리면 이온·전자 전도도가 함께 떨어졌다. (L32–33 · 45)
3. 시뮬레이션과 압밀 porosity 측정은 없고 void 분석은 사이클 후 계면의 상대비라서, 값은 측정 조건과 함께 써야 한다. (L146–147)

### 문제와 설계

SSE 층을 얇게 만들수록 막이 기계적으로 파손될 위험이 커진다. 원문은 SSE 막과 양극 막을 겹쳐 함께 압연하는 건식 co-rolling으로 이 문제를 다뤘다. (L20 · 71)

재료는 Li₆PS₅Cl(LPSCl) 고체전해질, 다결정 NCM811(PC-NCM) 또는 단결정 NCM82(SC-NCM), 도전제 VGCF, 바인더 PTFE다. 양극은 CAM:SSE:VGCF:PTFE = 80:17:3:0.5 wt%이고, SSE 층은 LPSCl:PTFE = 100:0.1 wt%에 두께 50 µm다. 시뮬레이션은 없고 막 제조, 전달 측정, 셀 사이클로 이루어진 실험 연구다. (L20 · 23–24)

- 그림 — Fig. 1: Fig. 1b의 co-rolling 모식과 Fig. 1c의 SSE 두께와 파손 위험의 관계를 본다. (L71)

### 세 공정 변수

공정 변수는 활물질 입자, 압연 온도, 두께 감소량 세 가지다. 작은 SC-NCM은 가압 전부터 치밀하게 접촉했고 가압 뒤에도 무손상이었다. 큰 PC-NCM은 거친 표면과 큰 void 때문에 가압 시 심하게 균열했다. (L46 · 63–64)

압연 온도는 30 °C에서 비균일 층을, 120 °C에서 균일 층을 만들었다. 원문은 이를 PTFE storage modulus가 30에서 120 °C 사이에 67% 감소한 바인더 연화로 설명했다. 두께 감소량이 100 µm이면 전극이 SSE로 침투했고, 20 µm이면 두 층이 구분되어 120 °C와 20 µm 조건을 채택했다. (L42 · 65–66)

- 그림 — Fig. 2: Fig. 2b,c에서 PC-NCM의 균열과 SC-NCM의 무손상을, Fig. 2d,e에서 온도에 따른 단면 균일도 차이를 본다. (L73–74)

### 결합된 계면

co-rolled 막에서는 두 막이 하중을 함께 나눠 졌다. 인장강도는 SSE 0.049, 전극 0.441, co-rolled 0.510 N cm⁻¹였다. peel-off 시험에서 freestanding 막은 한 번 만에 분리됐지만 co-rolled 막은 열 번에도 떨어지지 않았다. (L43 · 77–78)

원문은 결합의 원인을 계면을 가로지르는 바인더-VGCF 섬유망으로 보았다. 압연 shear가 바인더를 늘려 섬유화하고 새 접촉을 만든다. 그 결과 freestanding은 불균질한 계면을, co-rolled는 융합된 계면을 이룬다고 원문은 적었다. (L53–55 · 79 · 91–92)

- 그림 — Fig. 3: Fig. 3b의 인장강도 비교와 Fig. 3h 측면 SEM, Fig. 3i의 바인더-VGCF 네트워크 모식을 본다. (L77–78)

### 전달과 PTFE 함량

PTFE 함량을 늘리면 양극의 이온 전도도와 전자 전도도가 함께 떨어졌다. CAM:SSE:VGCF를 80:17:3으로 고정하고 PTFE를 0.5, 2, 5 wt%로 늘렸다. 이때 σ_ionic은 0.069, 0.024, 0.007 mS/cm였고 σ_e는 34, 4.5, 0.011 mS/cm였다. (L32–33)

PTFE 0.5 wt% 양극에서는 co-rolled와 freestanding의 전달이 거의 같았다. SSE 층의 σ_ionic은 co-rolled가 1.04, freestanding이 1.29 mS/cm였다. 원문은 이 차이가 freestanding SSE의 500 µm 두께로 측정 형상이 달라서 생긴 것이라고 적었다. (L34 · 36 · 150–151)

- 그림 — Fig. 4: Fig. 4c,d에서 SSE 층, Fig. 4e,f에서 양극 층의 Li⁺와 e⁻ 전도도를 co-rolled와 freestanding으로 비교한다. (L80)

### 저압 작동과 한계

견고한 계면의 효과는 낮은 stack pressure에서 크게 드러났다. co-rolled 셀은 2 MPa에서 500 사이클 동안 용량을 >80% 유지했고, 75 MPa에서는 >95%를 유지했다. 압력을 75에서 2 MPa로 낮추자 사이클 후 void ratio는 freestanding에서 4.0에서 15.5로, co-rolled에서 1.9에서 3.5로 늘었다. (L45 · 83)

검토 측은 void 분석이 사이클 후 계면 void의 상대비일 뿐 압밀 porosity가 아니라고 본다. 정량 porosity, 접촉면적, 탄성계수 같은 압밀 물성은 측정되지 않았다고 지적한다. SSE 층 전도도의 co-rolled와 freestanding 비교도 측정 형상이 달라 조심해야 한다고 본다. (L146–147 · 150–151)

- 그림 — Fig. 5: Fig. 5a와 5b에서 75 MPa와 2 MPa 장기 사이클의 co-rolled와 freestanding 차이를 본다. (L82)

### 용어 풀이 (논문에 없는 일반 설명)

- **co-rolling**: 두 막을 겹쳐 롤 사이로 함께 압연해 한 번에 접합하는 건식 공정이다.
- **DCP**: 직류 전압을 걸고 정상 전류로 저항을 구해 전자 전도도를 재는 직류분극 측정법이다.
- **PTFE 섬유화**: 전단을 받은 PTFE 입자가 가는 섬유로 늘어나 주변 입자를 그물처럼 묶는 현상이다.

### 우리 연구에 주는 뜻

- 우리 σ_e, σ_ionic 폼은 도전제 추가만 반영하고 PTFE의 절연과 접촉 차단 페널티가 없어서, Supp Fig 5의 PTFE 함량 곡선을 보정 1순위로 흡수한다. (L112 · 120–122)
- PC-NCM 균열과 SC-NCM 무손상은 우리 DEM이 AM_P만 파괴하고 AM_S를 rigid로 두는 처리의 실험 근거가 된다. (L114 · 128–130)
- 바인더-VGCF 섬유망 SEM은 우리 CBD 시드 모델의 개념적 검증으로 쓰고, 정량 porosity와 명시적 접촉망 전달은 우리가 더하는 부분이다. (L113 · 115–116 · 155 …)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 양극 σ_ionic (PTFE 함량별) | 0.069 / 0.024 / 0.007 mS/cm | PTFE 0.5/2/5 wt%, 75 MPa | L32 |
| 양극 σ_e (PTFE 함량별) | 34 / 4.5 / 0.011 mS/cm | PTFE 0.5/2/5 wt%, VGCF망 | L33 |
| SSE 층 σ_ionic | 1.04 (co-rolled) / 1.29 (freestanding) mS/cm | LPSCl:PTFE 100:0.1 | L36 |
| 저압 사이클 용량 유지 | 2 MPa서 >80% 유지 500 cyc | LiIn‖LPSCl‖NCM, 0.5 C | L45 |
| stack 비에너지 | 310 Wh kg⁻¹ | pouch, 5 mAh cm⁻², 5 MPa | L44 |
| PTFE storage modulus 감소 | 67% 감소 | DMA 1 Hz, 30에서 120 °C | L42 |

### 읽을 때 조심할 것

- 검토 측은 void 분석이 사이클 후 계면 void의 상대비라서 압밀 porosity와 직접 비교할 수 없다고 본다. (L98 · 147)
- 양극 레시피가 VGCF 3 wt%, PTFE 0.5 wt%이므로, 검토 측은 함량이 다른 전극에 σ_e 절대값을 옮기지 말고 추세로만 써야 한다고 본다. (L148–149)
- bulk LPSCl σ_ionic 2.19 mS/cm는 측정, 입자, 입계 조건이 다른 문헌 값과 달라 절대 대조를 피해야 한다고 검토 측은 본다. (L38 · 152–153)
- Supp Table 2, 3의 EIS 피팅 R, CPE 값은 회로 파라미터이지 직접 물성이 아니라고 검토 측은 지적한다. (L156)

### 원문에서 먼저 볼 곳

- Supp Fig 5: PTFE 함량에 따라 양극 σ_ionic과 σ_e가 함께 떨어지는 정량 곡선이 있다. (L86)
- Fig. 2b,c와 Supp Fig 6–8: PC-NCM 균열과 SC-NCM 무손상, 압력에 따른 균열 증가를 SEM으로 보여 준다. (L73 · 87–89)
- Fig. 3h,i와 Supp Fig 17, 18: 계면의 바인더-VGCF 섬유망 SEM과 5단계 섬유화 메커니즘 모식이 있다. (L78 · 91–92)

태그: LPSCl · NCM811 · PTFE · VGCF · co-rolling · EIS · stack pressure

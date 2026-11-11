# Modeling of the Calendering Process for Lithium-Ion Batteries with DEM Simulation

*EEPA와 Bonding DEM으로 캘린더링 공정 파라미터를 역추천한다*

- Schreiner et al. · Procedia CIRP 93, 149-155 (2020) · doi:10.1016/j.procir.2020.05.158 · digest `schreiner2020_dem_calendering_lib`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## EEPA와 Bonding DEM으로 캘린더링 공정 파라미터를 역추천한다

> 상용 DEM으로 NMC622 양극 압연을 모사하고, 목표 전극물성을 넣으면 캘린더링 파라미터를 추천하는 세 모듈 도구 구조를 제안했다. (L23 · 55 · 110)

### 요점

1. NMC622 양극의 캘린더링을 EDEM에서 EEPA 탄소성 접촉과 Bonding으로 모델하고, 나노압입 load-displacement 곡선으로 접촉 파라미터를 보정했다. (L23 · 62 · 82)
2. 결과의 중심은 목표 전극물성을 압력, 온도, 압연속도, calender 사양으로 되돌려 추천하는 USER TOOL 구조이며, 정량값은 압연 전 porosity 43 % 하나에 그친다. (L6 · 35 · 55)
3. porosity 대 압력 자료, 전도도, Young's modulus 확정값이 없어 도구 구조와 파라미터 경향까지만 말할 수 있다. (L37 · 46–47)

### 전극 모델 구성

출발점은 캘린더링을 생산공정으로 보고 공정 파라미터를 예측하는 방법론이다. 원문은 ramp-up 비용 절감을 목표로 적었고 전체 구조를 세 모듈로 나누었다. 첫 모듈은 소재, 밀도, 질량분율을 받아 전극 모델을 만들고 전극밀도와 입자분포로 검증한다. (L30 · 53 · 96)

전극은 활물질 NMC622 95.5 wt%에 PVDF, carbon black, 도전성 흑연을 섞은 양극이다. NMC622는 강체 구로 두고, 바인더와 도전제는 conductive additive-binder matrix(CABM)로 묶어 개별 입자로 그리지 않았다. 입자는 한 변 250 µm의 control volume에 생성한 뒤 56 µm 두께로 잘라 냈다. (L28 · 39 · 74–75 …)

- 그림 — Fig. 2: a와 c의 SEM 사진에서 NMC 입자가 바인더와 carbon black matrix에 박힌 모습을 보면 된다. 원문은 이 사진으로 구형 가정을 정성적으로 뒷받침했다. (L74 · 106)

### EEPA와 Bonding

입자 사이 접촉은 두 모델을 따로 보정한 뒤 결합했다. EEPA(Edinburgh Elasto-Plastic Adhesion)는 탄소성과 하중의존 점착을 맡고, Bonding(Potyondy–Cundall)은 CABM을 입자 사이의 가상 접촉으로 표현한다. bond는 첫 timestep에 생기고, 법선과 전단 임계응력을 넘으면 끊긴 뒤 다시 생기지 않는다. (L63–64 · 67–68)

EEPA의 소성 정도는 contact plasticity ratio λ_P로 조절한다. λ_P는 초기강성에 대한 제하강성의 비로, 0이면 완전탄성이고 1이면 완전소성이다. 원문은 PVDF-NMC에 0.9, NMC-NMC에 0.8, PVDF-PVDF에 0.975를 주고 모두 0.985로 점증시켰으며, 접촉면적이 가장 큰 NMC-NMC 쌍의 영향이 가장 컸다고 적었다. (L41 · 65)

- 그림 — Fig. 4: PVDF-PVDF, NMC-NMC, PVDF-NMC 상호작용별로 압밀압력 대 압밀경로 곡선이 어떻게 달라지는지 보면 된다. NMC-NMC 상호작용의 영향이 가장 크다. (L108)

### 나노압입 보정

접촉 모델은 나노압입 load-displacement 곡선에 맞춰 보정했다. 압입은 ⌀100 µm flat punch를 0.15 µm s⁻¹로 누르고 같은 속도로 뺐다. Young's modulus는 영향이 가장 커서 먼저 맞췄지만, 원문은 이를 높이면 timestep이 줄어 계산비가 는다고 적었다. (L40 · 82)

곡선의 부분마다 지배하는 파라미터가 다르다. 초기 shift는 임계 전단·법선 응력과 surface energy가, 압력의 크기는 Young's modulus가, 탄성 회복은 λ_P가 주로 정한다. surface energy를 올리면 필요한 압축력이 급증하므로 원문은 약간만 올리라고 권한다. (L66 · 92 · 109)

- 그림 — Fig. 5: 빨강 시뮬레이션과 주황 실험의 압밀압력 곡선, 그리고 초록 broken bonds 곡선을 함께 보면 된다. a, b, c 표시가 각각 어느 파라미터의 몫인지 캡션에 적혀 있다. (L109)

### USER TOOL

세 번째 모듈인 USER TOOL이 원문의 중심이다. 압연 전후의 두께와 밀도 같은 목표 전극물성을 넣으면 압력, 온도, 압연속도, calender 사양 공간에서 적절한 calendering 파라미터를 추천한다. 둘째 모듈은 compaction resistance, initial cohesion, elastic spring-back 같은 시뮬레이션 파라미터를 현미경 분석이나 예비 시뮬레이션으로 정한다. (L54–55 · 110)

calender는 roll 전체가 아니라 roll section으로 모델했다. roll 직경이 약 400 mm라 입자 크기와 차이가 커서 전체를 모델하면 계산비가 폭증하기 때문이다. 원문은 roll의 탄성변형을 무시해 이론적 roll gap을 최소 전극두께로 두고, roll 직경이 크고 압연속도가 느릴수록 공기가 잘 빠져 spring-back이 준다고 적었다. (L45 · 81)

- 그림 — Fig. 6: 압연 전후의 두께와 밀도 같은 입력이 USER TOOL을 거쳐 calendering 파라미터로 나가는 입출력 구조를 보면 된다. (L110)

### 믿을 수 있는 범위

검토 측은 정량 결과가 빈약하다고 본다. 하드 porosity 값은 압연 전 43 %(ρ 2.53 g/cm³) 하나뿐이고, porosity-vs-line-load 표나 곡선은 없다. Young's modulus도 먼저 보정했다고만 하고 확정값을 본문에 주지 않았다. (L6 · 35 · 37 …)

다루지 않은 물리도 있다. 전도도는 풀지 않았고 이온 전도와 전자 전도의 trade-off를 서술로만 언급했으며, 입자 형상 변화와 파쇄는 모델하지 않았다. 검토 측은 EEPA를 항복압 캡이 없는 이력 법칙으로 분류해, 같은 탄소성 접촉이라도 Thornton–Ning류 항복캡 모델과 다른 계열로 본다. (L46 · 71 · 74 …)

- 그림 — Fig. 3: 세로축이 압밀압력, 가로축이 압밀경로인 load-displacement 곡선이라는 점을 보면 된다. porosity 대 압력 곡선이 아니며, c 구간에서 제하 후 잔류변위와 spring-back이 보인다. (L107)

### 용어 풀이 (논문에 없는 일반 설명)

- **캘린더링**: 코팅된 전극을 두 롤 사이로 통과시켜 눌러 두께와 공극률을 줄이는 압연 공정이다.
- **spring-back**: 압축을 풀었을 때 탄성 회복 등으로 전극 두께가 일부 되돌아오는 현상이다.
- **bonded-particle model**: 입자 쌍 사이에 가상의 결합을 두고 그 결합이 임계 응력을 넘으면 끊어지게 하는 DEM 접촉 기법이다.

### 우리 연구에 주는 뜻

- 검토 측은 EEPA의 λ_P와 Δ_Y가 우리 LIGGGHTS hooke/hysteresis의 언로딩 강성비와 점착 항과 기능이 같은 캡 없는 이력 계열이라고 보며, 우리 접촉 법칙 선택을 상용 코드 사례로 뒷받침한다. (L151 · 186–187)
- CABM을 입자상 없이 bond로만 표현한 방식은 우리 CBD 표현을 입자 수 증가 없이 확장하는 최소 구현 청사진이 된다. (L199)
- 목표 물성에서 공정을 역산하는 USER TOOL은 우리 설계에서 물성으로 가는 forward predictor에 inverse-design 모드를 넣을 때의 구조 선례다. (L203)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 압연 전 코팅 porosity | 43 % | 압연 전 NMC622 코팅, eq (1) | L35 |
| 단면 코팅 두께 | 56 µm | 압연 전 single-sided | L36 |
| NMC622 평균 입경 d₅₀ | 7.19 µm | SLS 실측, log-normal | L38 |
| EEPA λ_P 최종값 | 0.985 | 모든 접촉 쌍, 점증 보정 | L41 |
| PVDF-PVDF surface energy | 60 J m⁻² | EEPA 하중의존 점착 | L42 |
| 나노압입 속도 | 0.15 µm s⁻¹ | ⌀100 µm flat punch 보정 | L40 |

### 읽을 때 조심할 것

- porosity 대 line-load 자료가 없고 Fig 3과 Fig 5는 load-displacement 곡선이라 압력별 치밀화 비교에는 쓸 수 없다. (L37 · 174 · 270)
- 전도도는 어떤 형태로도 계산하지 않았으므로 전달 물성을 이 논문에서 끌어오면 안 된다. (L87 · 271)
- Young's modulus 확정값이 공개되지 않았고 broken bonds 수는 그림에서 읽은 추세에 불과하다. (L47 · 281)
- λ_P, Δ_Y, 임계응력은 액체전해질 LIB의 NMC622-CABM에 맞춘 보정값이라 다른 전극계로 절대값을 옮길 수 없다. (L273 · 277)

### 원문에서 먼저 볼 곳

- Fig 5에서 시뮬레이션과 실험 곡선을 비교하며 어느 파라미터가 곡선의 어느 구간을 지배하는지 확인한다. (L109)
- Fig 1과 Fig 6에서 세 모듈 구조와 USER TOOL의 입출력을 보고 논문의 무게중심이 도구 구조임을 확인한다. (L105 · 110)
- Table 1에서 시뮬레이션에 쓴 성분별 질량분율과 밀도를 확인한다. (L28 · 261)

태그: NMC622 · DEM · EDEM · EEPA · Bonding · calendering · 나노압입 · spring-back

# Formulating Interfacial Impedances for Designing High-Energy and High-Power All-Solid-State Battery Cathodes

*bimodal 양극 입자가 입계 저항과 전하전달 저항을 함께 낮춘다*

- Choi et al. · ACS Appl. Mater. Interfaces 16, 26066-26078 (2024) · doi:10.1021/acsami.4c01322 · digest `interfacial_impedance_formulation_assb_cathode`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## bimodal 양극 입자가 입계 저항과 전하전달 저항을 함께 낮춘다

> 복합 양극의 낮은 이온전도는 SE 입계 저항 때문이고, 입경에 따른 입계 저항과 전하전달 저항의 trade-off는 bimodal CAM으로 풀린다. (L52 · 235–236)

### 요점

1. NCM/NCA와 LPSC로 만든 복합 양극의 임피던스를 전송선 모형(TLM) 등가회로로 정식화하고, 대칭셀과 full cell EIS로 입계 저항 r_i,gb와 전하전달 저항 r_i/e를 따로 뽑았다. (L52 · 138 · 143 …)
2. 원문은 작은 CAM이 r_i/e를 낮추지만 공극을 늘려 r_i,gb를 키운다고 적었고, 작은 입자와 큰 입자를 섞은 bimodal 양극이 R_cathode 14 Ω·cm²로 가장 낮았다. (L180–181 · 228)
3. r_i,gb와 r_i/e는 측정값에 회로를 맞춘 lumped 값이고 전해질과 양극 조성이 특정되어 있어, 검토 측은 추세와 방법은 옮기되 절대값 전이는 피해야 한다고 본다. (L378–380)

### 두 레일 회로

황화물 전고체 전지 복합 양극은 계면 임피던스가 높지만, 그 원인을 항별로 나누는 정량 틀이 필요했다. 원문은 이온이 SE 입자망(z_i)을, 전자가 CAM과 탄소섬유망(z_e)을 따로 흐르고 계면 crossrail(z_i/e)에서 전하전달로 이어지는 TLM 사다리 회로를 세웠다. 이온 레일은 입내 저항 r_i,bulk와, 입계 저항 r_i,gb와 용량 c_i,gb의 병렬 묶음을 직렬로 이은 형태다. (L129–132)

경계조건을 바꿔 서로 다른 과정을 고립시켰다. 이온을 막는 SUS 대칭셀에서는 전하전달이 사라져 r_i,gb를 정량하고, In 음극 full cell에서는 전하전달 r_i/e와 저주파 고상 확산 Z_low가 살아남는다. (L139 · 141 · 144 …)

### 병목은 입계다

순수 SE 펠릿에서도 입계가 이온 저항의 대부분을 차지했다. 300 MPa 펠릿의 r_i,bulk는 178 Ω·cm, r_i,gb는 631 Ω·cm였다. 복합셀에서 r_i,gb 항이 없는 회로는 EIS에서 벗어났고, 입계 항을 넣은 Fig 1d 회로가 일관되게 맞았다. (L83–84 · 141 · 200)

SE 부피분율 ε_i를 줄이면 입계 저항이 폭증했다. ε_i=0.54에서 r_i,bulk는 610 Ω·cm였지만 r_i,gb는 17 700 Ω·cm였다. Bruggeman 지수 α는 입내 항이 0.52로 이상값에 가까웠으나 입계 항은 4.3이어서, 원문은 저항 증가의 주역이 경로 신장이 아니라 입계 성장이라고 적었다. (L89–90 · 92 · 206–207)

### 압력과 등방가압

압밀 압력을 높이고 등방가압을 쓰면 r_i,gb가 크게 줄었고 r_i,bulk는 거의 변하지 않았다. 등방가압 펠릿(IP-P) 500 MPa에서 eps_pore는 0.046이었다. 500 MPa 85°C 조건의 tau_eff²는 1.46으로 이상 Bruggeman 값 1.41에 가까웠고, 원문은 낮은 모듈러스 SE가 pristine 펠릿 수준까지 치밀화된 것으로 해석했다. (L99 · 101 · 185–186)

일축가압은 SUS 평판이 단단한 CAM에 응력을 모아 SE 변형이 적었다. 대신 전자저항 r_e는 SUS 셀 쪽이 더 낮았다. (L187 · 217)

### 입경 trade-off

CAM 입경은 두 계면 저항을 반대 방향으로 움직였다. r_i/e는 CAM 표면적의 역수에 비례했고 기울기는 0.082 Ω·cm⁵였다. 반면 작은 CAM은 비균질 응집으로 더 다공해져 r_i,gb가 커졌고, r_i,gb는 eps_pore에 비례했다. (L178–180 · 225)

4 µm와 15 µm NCA를 섞은 bimodal 양극이 이 trade-off를 풀었다. 작은 입자가 큰 입자 사이 공극을 채워 eps_pore가 0.11, r_i,gb가 3 240 Ω·cm로 가장 낮았고, R_cathode는 unimodal의 20–25 대비 14 Ω·cm²였다. 2C 방전 용량은 NCA-b-12가 2.1, NCM-7이 0.3 mAh/cm²였다. (L108 · 181 · 228 …)

### 믿을 수 있는 범위

검토 측은 미세구조가 생성되지 않고 r_i,gb, r_i/e, eps_pore 같은 fitted lumped 파라미터로만 들어온다는 점을 한계로 본다. SE가 Cl-rich인 Li₅.₇₅PS₄.₇₅Cl₁.₂₅이고 CAM이 NCM90/NCA94여서, 검토 측은 절대값 전이를 금하고 추세와 방법만 비교하라고 적었다. (L378–380)

검토 측은 α_gb=4.3이 자유 지수를 둔 경험 fit이라 기하 굴곡 외에 constriction까지 흡수한 값이라고 본다. 0.082 Ω·cm⁵ 기울기는 NCA 계 값이고 NCM-7의 r_i/e는 훨씬 컸다. 제조 압력 300–500 MPa와 작동 stack 압력 4 MPa도 구분해야 한다. (L384–386)

### 용어 풀이 (논문에 없는 일반 설명)

- **TLM(transmission line model)**: 다공성이나 복합 전극을 이온 레일과 전자 레일, 그 사이 계면 요소로 이루어진 분포 RC 사다리로 보고 임피던스를 해석적으로 푸는 de Levie 계열 모형이다.
- **Bruggeman 지수**: 유효 굴곡도 인자를 전도상 부피분율의 거듭제곱으로 쓸 때의 지수로, 구형 절연 입자가 흩어진 이상적인 경우를 기준값으로 삼는다.
- **전하전달 저항**: 전해질과 활물질 계면에서 Li 이온이 전자와 만나 활물질 격자로 들어가는 반응이 일으키는 저항이다.

### 우리 연구에 주는 뜻

- 우리 Kirchhoff/Holm 솔버가 계산하는 σ_ionic은 원문의 r_i=r_i,bulk+r_i,gb에서 얻는 σ_i,eff=1/r_i와 같은 양이어서, 측정과 구조 계산을 맞대는 방법론 대조가 된다. (L41 · 297 · 326)
- 우리 솔버에는 전하전달 r_i/e와 Warburg 확산 Z_low가 없으며, r_i/e가 CAM 표면적에 반비례한다는 관계는 우리가 이미 계산하는 AM-SE 접촉 면적 위에 R_ct를 얹는 경로가 된다. (L43–44 · 333)
- 원문의 bimodal 최적은 임피던스에서, 우리 Furnas dip은 packing에서 나와 이유는 다르지만 같은 결론이며, 모달리티 주체가 CAM과 AM:SE로 달라 교차검증 시 구분이 필요하다. (L340 · 383)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 순수 SE 입계 이온저항 r_i,gb | 631 Ω·cm |  | L84 |
| 입계 항 Bruggeman 지수 α | 4.3 | 복합 대칭셀 eq 5 fit | L92 |
| r_i/e 대 1/A_CAM 기울기 | 0.082 Ω·cm⁵ | NCA full cell | L102 |
| R_cathode (NCA-15/NCA-4/NCM-7/NCA-b-12) | 20 / 24 / 25 / 14 Ω·cm² | full cell, 500 MPa | L105 |
| 2C 방전 용량 (NCA-b-12 / NCM-7) | 2.1 / 0.3 mAh/cm² | full cell, 2C | L111 |
| 등방가압 후 tau_eff² | 1.46 | IP-P 500 MPa 85°C, ε_i=0.58 | L101 |

### 읽을 때 조심할 것

- SE가 Cl-rich Li₅.₇₅PS₄.₇₅Cl₁.₂₅이고 CAM이 NCM90/NCA94라서, 검토 측은 σ, r_i,gb, r_i/e의 절대값을 다른 조성으로 옮기지 말라고 지적한다. (L64–65 · 379)
- r_i/e 기울기 0.082 Ω·cm⁵는 LPSC/NCA 계면 값이고 NCM-7의 r_i/e는 훨씬 커서 재료에 따라 달라진다. (L224 · 384)
- 검토 측은 α_gb와 tau_eff²가 자유 지수를 둔 경험 fit이라 constriction까지 섞여 있으므로 다른 굴곡도 정의와 절대값을 비교하지 말라고 본다. (L386)
- eps_pore는 800 µm 복합셀 펠릿 값이고 압력은 제조 300–500 MPa와 작동 4 MPa가 다르므로 조건을 맞춰 써야 한다. (L69 · 114 · 382 …)

### 원문에서 먼저 볼 곳

- Fig 2e–h에서 z_e 기준 회로와 z_i 기준 회로의 피팅 차이를 보면 낮은 이온전도가 입계 때문이라는 핵심 주장의 근거가 드러난다. (L200 · 249)
- Fig 3c,d에서 ε_i에 따른 r_i,bulk와 r_i,gb, Bruggeman 지수 fit을 확인한다. (L206–207 · 253)
- Fig 6b–f에서 입경에 따른 r_i,gb와 r_i/e의 반대 움직임과 bimodal 양극의 위치를 본다. (L223–225 · 227)

태그: LPSC argyrodite · EIS · TLM 등가회로 · grain-boundary resistance · charge-transfer resistance · bimodal CAM · isostatic press

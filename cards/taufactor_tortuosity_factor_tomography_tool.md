# TauFactor: An open-source application for calculating tortuosity factors from tomographic data

*voxel 위에서 확산을 직접 풀어 굴곡도 인자를 일관되게 구한다*

- Cooper et al. · SoftwareX 5, 203-210 (2016) · doi:10.1016/j.softx.2016.09.002 · digest `taufactor_tortuosity_factor_tomography_tool`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## voxel 위에서 확산을 직접 풀어 굴곡도 인자를 일관되게 구한다

> TauFactor는 분할된 voxel 미세구조에서 ∇²C=0을 직접 풀어 τ = ε·D/D_eff를 빠르고 재현성 있게 계산하는 오픈소스 툴이다. (L15 · 32 · 51)

### 요점

1. 단층촬영으로 얻어 분할한 voxel 미세구조를 그대로 격자로 삼아 정상상태 확산을 over-relaxation 반복법으로 푸는 MATLAB 툴을 공개했다. (L15 · 51 · 61)
2. 원문은 10⁶ voxel을 단일 코어에서 30 s 안에 풀고, 8가지 방법 비교에서 TauFactor의 τ가 Avizo XLab과 일치했다고 적었다. (L34 · 41 · 89)
3. 검토 측은 이 τ가 점접촉 구속저항이 없는 기하적 상한 굴곡도이고, voxel 해상도와 SA·TPB 근사에 묶인다고 본다. (L77 · 132–134)

### 왜 직접 계산인가

원문은 Bruggeman 같은 상관식이 등방·단순 기하를 가정해 복잡한 망에서 부정확하다고 보았다. 그래서 3D 이미지가 있으면 τ를 미세구조에서 직접 계산하라고 주장한다. (L99)

또 하나의 문제는 명목상 같은 방법들 사이의 불일치였다. 원문은 meshing이 smoothing과 기하 왜곡을 낳는다고 보고, remesh나 resample 없이 voxel을 그대로 mesh 요소로 쓴다. 고가 독점 소프트웨어나 비공개 코드 대신 FreeBSD 라이선스로 공개해 연구 간 비교 가능성을 높이는 것이 기대 효과로 적혀 있다. (L23 · 51 · 98)

- 그림 — Fig. 1: 회색조 단층촬영에서 분할된 2상 부피를 거쳐 확산 시뮬레이션으로 가는 흐름을 왼쪽에서 오른쪽으로 본다. 빨간 영역이 flux가 높은 병목이다. (L72 · 82)

### 어떻게 푸는가

전도상 안에서 ∇²C=0을 풀고, 위 면에 C=0, 아래 면에 C=1을 고정하며 비전도상 계면은 no-flux로 둔다. 다공체 flux를 같은 크기의 완전 치밀 대조체적 flux로 나누면 τ = ε·D/D_eff가 나온다. 원문은 τ=1이 직선 경로이고 τ는 항상 1 이상이라고 적었다. (L32 · 55–58)

이산화는 각 voxel 농도를 면으로 맞닿은 여섯 이웃 전도 voxel의 평균으로 두는 유한차분이다. 경계는 ghost-node 기법으로 강제한다. Jacobi에 선형 외삽을 더한 over-relaxation으로 반복 수를 약 세 자릿수 줄였고, checkerboard 벡터화와 합쳐 최소 4배를 더 빠르게 했다. (L35 · 59–61)

- 그림 — Fig. 3: 3D 전도상 voxel을 RED와 GREEN 두 벡터로 나누는 checkerboard 변환을 본다. 캡션은 두 최적화를 합쳐 속도가 최소 4배 올랐다고 적었다. (L61 · 84)

### 무엇을 내놓나

τ 외에 부피분율 ε, 표면적 SA, triple-phase-boundary(TPB) 밀도, percolation 분율, flux map을 함께 낸다. SA는 voxel 면을, TPB는 세 상이 만나는 voxel 모서리를 그대로 센다. representative volume analysis(RVA)는 부피를 키워 가며 지표의 안정성을 그려 대표 체적이 충분한지 본다. (L66 · 69–70 · 72–73)

원문은 고성능 컴퓨팅 없이 10⁸ voxel 넘는 데이터를 단일 코어에서 몇 시간에 처리한다고 적었다. 예시 3상 구조에서 White 상의 τ는 2.26으로 보고됐다. 전도 방향으로 연결되지 않은 상은 τ를 잴 수 없다. (L36–37 · 67)

- 그림 — Fig. 6: 왼쪽 리포트에서 농도장, flux, τ-반복 곡선과 τ=2.26을, 오른쪽에서 ε·SA·TPB의 RVA 변화를 본다. (L87)

### 검증과 오차 한계

원문은 SOFC LSCF cathode 시료에서 8가지 방법으로 τ를 비교했다. TauFactor는 Avizo XLab과 일치했고 random walk, mean path, pore centroid 같은 다른 방법은 크게 흩어졌다. 검토 측은 두 툴이 모두 voxel을 직접 푸는 솔버라 일치가 당연하다고 본다. (L41 · 89 · 161)

원문은 voxel 면을 그대로 쓰는 SA가 체계적으로 틀릴 수 있다고 스스로 경고한다. 한 voxel짜리 구는 SA가 약 2배, 여러 voxel 구도 최소 1.5배 과대추정되고, sub-voxel 복잡 구조는 임의로 크게 과소추정된다. Marching Cubes 같은 smoothing은 일관성을 위해 일부러 쓰지 않았다. (L39 · 88 · 133)

- 그림 — Fig. 8: ε에 대한 τ를 8가지 방법으로 그린 비교에서 TauFactor와 Avizo XLab이 겹치는지, 나머지 방법과 Bruggeman이 얼마나 벌어지는지 본다. (L89)

### 검토 측 판단

검토 측은 TauFactor가 전도상을 연속 매질로 다루므로 고체 전해질 입자 사이 점접촉의 Holm 구속저항이 들어가지 않는다고 본다. 그래서 이 τ는 기하적 상한 굴곡도에 해당하며, 구속을 포함한 유효 굴곡도를 대신하지 못한다. 0.5 µm 입자를 1 µm 격자로 voxel화하면 목 부분이 뭉개져 τ가 낮게 나온다는 점도 지적한다. (L77 · 132 · 134 …)

검토 측이 1.424.0 판 MATLAB 소스를 정적으로 읽은 결과, τ 정의는 원문과 같았다. 다만 ε는 관통하지 않는 고립 부피까지 포함해 세고, D_eff는 상자 전체 단면으로 정규화하며, 보고 τ는 위·아래 면 추정의 평균이다. 검토 측은 이 conventional τ를 P2D 입력으로 쓸 때 Nguyen 2020이 권하는 τ_e와 다른 양임을 밝혀야 한다고 본다. (L236–239 · 308–309)

### 용어 풀이 (논문에 없는 일반 설명)

- **tortuosity factor**: 다공 구조 때문에 유효 확산도나 전도도가 부피분율만으로 기대되는 값보다 얼마나 더 줄어드는지를 나타내는 무차원 인자다.
- **over-relaxation**: 반복 풀이에서 매 갱신량을 1보다 큰 계수로 키워 수렴에 필요한 반복 수를 줄이는 기법이다.
- **RVE와 RVA**: 대표 체적요소(RVE)는 지표가 시료 크기에 더 이상 흔들리지 않는 최소 부피이고, RVA는 부피를 키워 가며 그 안정성을 확인하는 분석이다.

### 우리 연구에 주는 뜻

- 우리 voxel_conductivity.py의 Laplace τ는 TauFactor와 같은 종류의 계산이라, 같은 voxel 입력에서 τ_Laplace,bulk를 표준 툴로 교차검증할 수 있다. (L109 · 119 · 176)
- TauFactor τ는 상한이므로 Holm 구속을 넣은 우리 σ_ionic이 TauFactor bulk 값보다 높게 나오면 버그 신호로 본다. (L177)
- 실제 비교에서는 DEM 접촉망은 측면 주기 조건인 mode 2와, MPM STEP3 복셀 σ는 측면 거울 조건인 mode 1과 맞추고, 접촉 구속이 없는 τ_Lap,geom과 대조한다. (L288–289 · 292)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 솔버 속도 | <30 s | 10⁶ voxel, 단일 i7 코어 | L34 |
| 반복 수 절감 | ~3 orders of magnitude(약 1000×) | OR 대 Jacobi | L35 |
| 처리 가능 크기 | >10⁸ voxel | 단일 코어 수 시간 | L36 |
| 예시 tortuosity factor | τ = 2.26 | ThreePhase.tif White 상, Dir 1 | L37 |
| 예시 TPB 밀도 | 30.2 µm⁻² | ThreePhase.tif RVA 리포트 | L38 |
| SA 과대추정 하한 | ×1.5 | 여러 voxel로 그린 구 | L39 |

### 읽을 때 조심할 것

- TauFactor τ는 점접촉 구속저항이 없는 기하적 상한이어서 구속을 포함한 유효 τ나 σ_ionic으로 읽으면 틀린다. (L132 · 157)
- τ는 입력 voxel 해상도에 민감하며, 미해상 voxel에서는 툴이 정확해도 결과가 틀릴 수 있다고 검토 측은 Duquesnoy 사례로 지적한다. (L134 · 223–224)
- voxel 면과 모서리로 센 SA와 TPB는 근사이며 구조에 따라 과대 또는 과소 추정된다. (L39 · 133)
- conventional τ는 dead-end 기공을 부피로만 세고 비관통이면 무한대가 되므로, P2D 입력에는 Nguyen 2020의 τ_e와 구분해야 한다. (L237 · 255 · 308–309)

### 원문에서 먼저 볼 곳

- Fig. 8에서 8가지 방법의 τ가 얼마나 흩어지는지와 voxel 직접 솔버끼리의 일치를 먼저 본다. (L89 · 123)
- 지배식과 Eq 1–3, ghost-node Eq 5–7을 다룬 솔버 절에서 τ 정의와 경계 처리 방식을 확인한다. (L54 · 58 · 60)
- Fig. 7에서 voxel 표현이 SA와 TPB에 주는 오차 시나리오를 확인한다. (L88)

태그: TauFactor · tortuosity factor · voxel Laplace · tomography · over-relaxation · RVA · TPB · SOFC LSCF cathode

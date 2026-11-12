# Effect of mold pressure on compaction and ion conductivity of all-solid-state batteries revealed by the discrete element method

*응집체 SE는 percolation 임계를 가져 Bruggeman 식을 벗어난다*

- So et al. · Journal of Power Sources 508, 230344 (2021) · doi:10.1016/j.jpowsour.2021.230344 · digest `so2021_dem_mold_pressure_assb_coldpress`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## 응집체 SE는 percolation 임계를 가져 Bruggeman 식을 벗어난다

> 접촉 소성을 넣은 3D DEM이 압밀을 재현했고, 응집체 SE의 이온전도는 φ_SE^crit = 0.13의 percolation식을 따른다. (L11 · 13 · 27 …)

### 요점

1. 소성변형을 접촉 단위로 넣은 3D cold-press DEM으로 LPS SE와 Si AM 전극의 압밀과 SE 상대 이온전도를 몰드압력과 AM 비율에 따라 계산했다. (L11–12 · 66)
2. 상대밀도는 Sakuda 실험과 맞았고, 볼밀 응집체가 만든 percolation 임계 φ_SE^crit = 0.13 때문에 이온전도가 Bruggeman 식을 따르지 않았다. (L13–14 · 27 · 61)
3. 입자는 구로만 다뤘고 소재가 LPS와 Si이며 임계값은 200–400 MPa 범위의 fit이라, 추세와 방법을 가져다 쓰는 데 그친다. (L63 · 112 · 115)

### 무엇을 묻나

몰드압력과 활물질 비율이 전극의 압밀과 고체전해질(SE) 이온전도도를 어떻게 바꾸는지가 질문이다. 대상은 LPS(Li₂S–P₂S₅) SE와 Si 음극활물질(AM)로 된 전극이다. 같은 그룹의 2D 모델을 3D로 확장한 작업이다. (L12 · 15 · 20)

유효 이온전도도는 흔히 Bruggeman 식으로 다룬다. 원문은 이상적 지수가 α=1.5인데 실험은 2.2<α<3.6을 보인다고 인용했다. 원문의 결론은 수정 Bruggeman 식도 부정확하므로 percolation 기반 식이 필요하다는 것이다. (L35 · 61)

### 접촉 소성 모델

in-house MATLAB DEM에 비선형 Hertz 스프링과 hysteresis 소성 모델을 넣었다. cold-press 단계에서는 소성으로 눌린 접촉점의 새 위치인 평형 overlap h_eq를 도입했다. 항복은 두 입자 중 작은 경도 H와 접촉면적으로 정한 임계력 F_th로 결정했다. (L51–52 · 55)

시뮬레이션은 응집체를 만드는 annealing, 중력 settling, PI 제어 상단벽으로 가압하는 cold-press의 세 단계로 나눴다. 경도는 Si가 10.6 GPa, LPS가 1.9 GPa로 주어졌다. 입자는 AM과 SE 모두 구이고 형상은 변하지 않는다. (L57 · 63 · 67)

- 그림 — Fig. 1: (b)의 가압 중 overlap h_ov와 (c)의 가압 후 평형 overlap h_eq를 비교하면 소성이 접촉점 잔류 overlap으로 표현되는 방식이 보인다. (L72)

### 압밀과 응력

압력이 높을수록 전극이 더 얇게 압축됐다. pure-SE층은 초기 80.0 µm에서 100 MPa에서 33.6 µm, 400 MPa에서 26.5 µm가 됐다. 원문은 상대밀도 곡선이 Sakuda 실험과 잘 맞는다고 적었고, AM 비율이 높을수록 최종 밀도는 낮았다. 압력을 풀면 전극이 약간 팽창했다. (L27–29 · 67)

입자 사이 응력은 단단한 Si끼리의 AM-AM 접촉에 몰렸다. SE-SE 응력은 H_SE 근처에서 막혔고, AM-AM 접촉은 소성변형을 거의 하지 않았다. 원문은 이를 AM cracking 위험으로 해석했다. (L36–37 · 76–77 · 104)

- 그림 — Fig. 4: (b)에서 시뮬레이션 상대밀도와 Sakuda 실험점의 겹침을, (c)에서 AM 비율에 따라 밀도가 낮아지는 것을 본다. (L27 · 75)

### percolation 보정식

이온전달은 Kirchhoff 망이 아니라 3D grid 위의 확산 풀이로 계산했다. 가압 후 입자를 grid에 옮겨 φ_SE를 얻고 TauFactor로 굴곡도 τ_SE를 구해 σ_SE^rel = φ_SE/τ_SE로 정의했다. 소성 때문에 단순 반경탐색은 부피분율을 과소평가하므로 0.1% 허용오차로 threshold distance를 반복 보정했다. (L60 · 82)

log-log 그림에서 σ_SE^rel은 Bruggeman 직선을 벗어났다. 원문은 φ_SE^crit = 0.13인 percolation 식(eq 16)을 200–400 MPa 결과에 맞췄고, 임계 이하에서는 전도가 0이다. 원문은 볼밀 응집체가 SE-SE 연결을 부족하게 만든 것을 그 원인으로 들었고, 이 식을 Sakuda와 Nakamura 실험에 비교했다. (L61 · 79 · 84 …)

- 그림 — Fig. 8: (a)는 Bruggeman 이탈을, (b)는 φ_SE^crit를 바꾼 곡선들 가운데 0.13이 실험과 가장 잘 맞는 것을 보여 준다. (L79)

### 어디까지 믿나

원문 스스로 AM을 구로 둔 점을 한계로 들고 비구형 입자와 입자 내부 균열을 future work로 남겼다. 검토 측은 h_eq가 접촉 함몰의 proxy일 뿐 공극을 메우는 형상 흐름은 없다고 본다. (L63 · 113)

검토 측은 σ_SE^rel이 τ 기반 상대값이고 접촉저항을 포함하지 않는다고 지적한다. 또한 φ_SE^crit는 LPS 응집체와 200–400 MPa의 fit값이며, 다중 seed 통계가 없어 단일 실현으로 보인다고 적었다. (L114–115 · 117)

### 용어 풀이 (논문에 없는 일반 설명)

- **percolation threshold**: 전도 상의 부피분율이 이 값 아래로 내려가면 끝에서 끝으로 이어진 경로가 끊겨 유효 전도도가 0이 되는 임계 분율이다.
- **tortuosity factor**: 다공 구조 안의 이온 경로가 직선 경로에 비해 얼마나 구불구불하고 좁은지를 나타내어 유효 전달을 깎는 계수다.
- **Bruggeman 식**: 유효 전도도를 전도 상 부피분율의 거듭제곱으로 근사하는 경험식이다.

### 우리 연구에 주는 뜻

- 검토 측은 So가 real E_SE=24 GPa를 그대로 쓰고도 경도 기반 항복으로 압밀을 재현한 점이, 항복 cap 없이 18× 연화로 보상하는 우리 DEM의 물리적 대안이 된다고 본다. (L93 · 102)
- 우리 σ_ionic 폼의 φc 0.195–0.20이 So의 0.13보다 높은 것은 응집 SE와 mono-disperse SE의 분산도 차이일 수 있다. (L97 · 103)
- AM-AM에 응력이 몰리고 SE만 소성하는 결과는 우리 Stage-E의 AM/SE 하중분배와 정성적으로 일치한다. (L104)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| SE percolation 임계 부피분율 | φ_SE^crit = 0.13 | LPS 응집체, 200–400 MPa fit | L61 |
| LPS 경도 H_SE | 1.9 GPa | Table 1, McGrogan 인용 | L41 |
| Si 경도 H_AM | 10.6 GPa | Table 1, de Vasconcelos 인용 | L40 |
| LPS 영률 E_SE | 24 GPa | Table 1, Sakuda 인용 | L38 |
| pure-SE층 가압 후 두께 | 26.5 µm | 초기 80.0 µm, 400 MPa | L29 |
| 시뮬레이션 입자 수 | ~45,000 | aggregate 크기 20 µm | L45 |

### 읽을 때 조심할 것

- SE는 argyrodite가 아닌 LPS이고 AM은 NMC 양극이 아닌 Si 음극이므로 절대 밀도와 전도도 값은 옮기지 않고 추세와 방법만 가져온다. (L22 · 112)
- φ_SE^crit = 0.13은 LPS 응집체와 200–400 MPa의 fit값이라 응집 정도가 다른 계에 그대로 대입할 수 없다. (L115)
- σ_SE^rel은 TauFactor의 φ/τ로 얻은 상대값이며 접촉저항을 포함하지 않아 절대 σ는 σ_SE^bulk를 곱해 추정할 수밖에 없다. (L114)
- 상대밀도, 응력, overlap, τ 곡선의 값은 그림에서 읽은 근삿값이고 다중 seed 통계가 없어 단일 실현으로 보인다. (L116–117)

### 원문에서 먼저 볼 곳

- Fig. 8에서 Bruggeman 이탈과 φ_SE^crit 곡선 비교를 보면 핵심 결론을 바로 확인할 수 있다. (L79)
- 방법 절의 eq 12–16에서 h_eq, 경도 기반 임계력, percolation 식의 정의를 확인한다. (L55 · 61)
- Fig. 5(d)와 Fig. 6(b)에서 입자쌍 종류별 응력과 평형 overlap 차이를 보면 phase별 소성 비대칭을 볼 수 있다. (L76–77)

태그: LPS · Si · DEM · cold-press · 소성변형 · percolation · tortuosity · TauFactor

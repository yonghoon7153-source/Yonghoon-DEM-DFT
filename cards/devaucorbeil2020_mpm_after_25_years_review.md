# Material point method after 25 years: Theory, implementation, and applications

*MPM은 격자를 매번 되돌려 대변형을 다루지만 수렴은 최적이 아니다*

- de Vaucorbeil, Nguyen, Sinaie, Wu · Advances in Applied Mechanics, 185-398 (2020) · doi:10.1016/bs.aams.2019.11.001 · digest `devaucorbeil2020_mpm_after_25_years_review`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## MPM은 격자를 매번 되돌려 대변형을 다루지만 수렴은 최적이 아니다

> MPM 25년을 정리한 첫 종합 리뷰로, 변종, 접촉, 파괴, 응용, 코드, 타 방법과의 비교를 한 틀에 묶었다. (L14 · 32 · 43 …)

### 요점

1. Sulsky 1994 이래 물질점법(MPM)의 이론, 구현, 응용을 339편의 참고문헌으로 정리한 리뷰다. (L14 · 22)
2. 원문은 고정 배경격자를 매 단계 초기화해 mesh distortion이 없다는 점을 MPM의 강점으로 들고, 변종, 접촉, 파괴 접근, 응용, 코드, FEM, SPH, DEM과의 비교를 정리했다. (L28 · 35 · 44 …)
3. 한계로 비최적 수렴, 경계조건 부여의 어려움, null-space 문제, 큰 메모리를 원문이 적었고, 검토 측이 본 범위는 초록과 서론뿐이라 수식과 수렴 수치는 이 기록으로 확인할 수 없다. (L5–6 · 68–69 · 96)

### 입자와 고정격자

MPM은 Lagrangian 입자와 고정된 Eulerian 배경격자를 함께 쓰는 하이브리드 방법이다. PIC/FLIP 계보에 속하며, Sulsky 1994가 FLIP을 고체역학으로 옮긴 것이 출발점이다. 입자가 위치, 질량, 속도, 부피, 변형구배, Cauchy 응력 같은 물리상태 전부를 운반하므로 질량 보존이 저절로 지켜진다. (L25–27)

한 계산 주기는 입자에서 격자로 옮기는 P2G, 격자 위 운동량 약형 풀이, 격자에서 입자로 되돌리는 G2P, 격자 초기화의 순서다. 격자를 매번 초기화하므로 mesh distortion이 없고, 원문은 이것을 FEM의 한계를 넘는 대변형 해석의 강점으로 적었다. 분류로는 Galerkin meshfree 계열이지만 shape function이 고정격자 위 단순 다항식이라 다른 meshfree보다 구현이 쉽다고 했다. (L27–30)

### 변종의 갈래

MPM 변종은 주로 shape function을 어떻게 고르느냐로 갈린다. 원조인 standard MPM은 선형 hat 함수를 써서 cell-crossing 불안정이 생긴다. GIMP는 유한한 입자영역을 둔 C¹ smooth 함수로 이를 완화하고, B-spline MPM은 현재 널리 쓰인다. (L33 · 35–37)

CPDI는 사변형이나 사면체 입자영역을 써서 극단적 인장에서도 수치적 파괴가 생기지 않는다. TLMPM은 total-Lagrangian 방식으로 격자가 초기형상만 덮어 메모리가 준다. Sulsky-Gong 2016의 iMPM/MLS는 속도만 MLS로 다뤄 중간 크기 격자에서 2차 수렴을 보이고 cell-crossing을 없앤다. (L38–40)

### 접촉과 파괴

원문은 no-slip과 no-penetration 접촉이 MPM에 내재한다고 적었다. 속도장이 단일값이라 추가 비용이 들지 않는다. 마찰과 다물체의 분리, 슬라이딩은 Bardenhagen 다물체 알고리즘이 표준이며, Nairn 2018이 점착을 포함한 임의 마찰법칙으로 일반화했다. (L44–46)

파괴는 세 갈래로 나뉜다. discontinuous 접근은 다중 속도장으로 명시적 균열을 다루고, continuous 접근은 damage 변수로 응력을 낮추며 particle erosion을 쓴다. mixed 접근으로는 continuum damage와 self-contact를 합친 Homel-Herbold 2017 CPDI가 소개됐다. (L49–51)

### 응용과 비교

응용은 지반공학, 유체-구조 연성, 영상 기반 해석, 컴퓨터 그래픽스, 해빙, 눈사태, 폭발까지 걸쳐 있다. 영상 기반 해석의 예로 foam 치밀화, 목재, 저밀도 눈, 고충전 복합재가 들렸고, Gritton 2017의 Si 음극 화학-기계 MPM도 언급된다. 공개 코드로는 저자의 Karamelo(C++, LAMMPS 구조), Uintah, NairnMPM, CB-Geo, MPM3D가 소개됐다. (L56–58 · 60–61)

원문은 대변형에서 MPM이 FEM보다 유리하고, SPH보다 빠르고 정확하다고 적었다. DEM과의 비교에서는 적절한 구성식을 쓰면 MPM이 DEM의 정확도를 재현할 수 있고 DEM에서 유도한 구성식으로 MPM을 대규모로 돌릴 수 있다는 논의를 소개했다. (L63–65)

### 믿을 수 있는 범위

원문이 직접 밝힌 한계는 네 가지다. 수렴이 비최적이라 1D에서도 FEM에 못 미치고 매우 고운 격자에서는 수렴하지 않는다. 경계조건 부여가 어렵고, null-space 문제가 있으며, updated-Lagrangian MPM은 메모리를 많이 쓴다. (L68–69)

검토 측은 초록과 서론, 절 일부만 보고 기록했으므로 본문의 수식과 알고리즘은 확인하지 못했다고 밝혔다. 또 Bardenhagen 2005 원문을 확인한 결과, 그 계산은 이상화 단위 셀 두 종에 붙는 접촉만 쓴 것이라 영상 기반, 다물체 접촉의 선례라는 서술은 그 논문으로 받쳐지지 않는다고 본다. 리뷰가 가리킨 것이 다른 논문인지는 확인되지 않았다. (L5–6 · 79–82)

### 용어 풀이 (논문에 없는 일반 설명)

- **cell-crossing 불안정**: 입자가 배경격자의 셀 경계를 넘을 때 shape function 기울기가 불연속이라 내력에 잡음이 생기는 현상이다.
- **updated-Lagrangian과 total-Lagrangian**: 변형을 현재 형상 기준으로 갱신하며 계산하느냐, 초기 형상 기준으로 계산하느냐의 차이다.
- **P2G/G2P**: 입자의 질량과 운동량을 격자 절점으로 옮기는 단계와 격자에서 구한 속도를 입자로 되돌리는 단계다.

### 우리 연구에 주는 뜻

- 우리 MPM은 Taichi 기반 MLS/B-spline 평활화 updated-Lagrangian 변종으로, 리뷰의 BSMPM과 iMPM 가지에 놓인다. (L15 · 41)
- 우리 scaffold MPM이 AM을 속도 0인 고정 장애물로 둔 것은 MPM에 내재한 no-penetration 접촉의 가장 단순한 활용이고, 더 복잡한 AM-SE 접촉은 Bardenhagen 알고리즘이 경로가 된다. (L46–48)
- 우리 MPM에는 파괴가 구현돼 있지 않아, SE 취성균열을 넣으려면 J2 소성과 별도로 continuous damage나 cohesive 접근을 더해야 한다. (L51–52 · 84–85)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 참고문헌 수 | 339 ref | 약 2019년까지의 MPM 문헌 | L14 |
| 리뷰가 다룬 기간 | 25년 | Sulsky 1994 이래 | L14 |
| 수록 쪽 | 185–398 | Adv. Appl. Mech. 53권 | L22 |
| Bardenhagen 2005의 압축 정도 | 공칭 90 % | 붙는 접촉, 이상화 단위 셀 | L83 |

### 읽을 때 조심할 것

- 기록은 초록과 서론, 절 일부에 근거하므로 MPM 수식, 알고리즘, 수렴 수치는 이 리뷰에서 가져올 수 없다. (L5–6 · 96)
- 리뷰라 LPSCl 물성, 공극률, 응력 같은 1차 데이터가 없다. (L87 · 97)
- 영상 기반 foam 치밀화를 Bardenhagen 2005의 직접 선례로 인용하면 안 되며, 그 논문은 이상화 단위 셀과 붙는 접촉만 다뤘다. (L79–81)
- MPM의 수렴이 비최적이고 매우 고운 격자에서 수렴하지 않는다는 점을 원문이 한계로 적었다. (L68)

### 원문에서 먼저 볼 곳

- 서론의 변종 분류 부분에서 standard MPM, GIMP, BSMPM, CPDI, TLMPM, iMPM의 차이를 먼저 본다. (L32–33)
- Bardenhagen 2005 인용 위치를 원문에서 다시 확인해 영상 기반 선례가 어느 논문을 가리키는지 본다. (L82)
- 본문 §2 일반 MPM, §5 contact/locking/fluid, 부록 B 구성식은 기록에 없으므로 원문에서 직접 읽는다. (L98)

태그: MPM · MLS-MPM · B-spline MPM · GIMP · CPDI · contact · fracture · large-deformation

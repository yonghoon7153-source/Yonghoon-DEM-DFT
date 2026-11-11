# Material point method after 25 years: Theory, implementation, and applications

*MPM 25년의 이론, 구현, 응용을 한 편에 정리했다*

- de Vaucorbeil, Nguyen, Sinaie, Wu · Advances in Applied Mechanics, 185-398 (2020) · doi:10.1016/bs.aams.2019.11.001 · digest `devaucorbeil2020_mpm_after_25_years_review`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## MPM 25년의 이론, 구현, 응용을 한 편에 정리했다

> MPM은 격자를 매번 되돌려 mesh distortion 없이 대변형, 접촉, 파괴를 다루고, 25년 동안 여러 변종과 응용으로 갈라졌다. (L14 · 28 · 44 …)

### 요점

1. Sulsky 1994 이래 물질점법(MPM)의 이론, 구현, 응용을 339편의 참고문헌으로 정리한 첫 종합 리뷰다. (L14 · 22)
2. 원문은 MPM의 변종 계보와 접촉, 파괴 처리법을 정리하고, FEM, SPH, DEM과 비교해 MPM이 유리한 조건을 적었다. (L35 · 40 · 44 …)
3. 검토 측이 본 것은 초록과 서론, 일부 절 스니펫뿐이라 수식, 알고리즘, 수렴 수치는 이 기록으로 확인할 수 없다. (L5–6 · 90)

### 범위와 기본 구조

원문은 Sulsky 1994 이후 25년 동안의 MPM을 이론, 구현, 응용으로 나눠 정리한 첫 종합 리뷰다. 참고문헌은 339편이고 2019년 무렵까지를 다룬다. (L14 · 22)

MPM은 Lagrangian 입자와 고정된 Eulerian 배경격자를 함께 쓰는 하이브리드 방법이다. 입자가 위치, 질량, 속도, 변형구배, 응력 같은 물리상태를 모두 들고 다니므로 질량 보존이 저절로 된다. 한 계산 주기는 입자에서 격자로 옮기기(P2G), 격자에서 운동량 약형 풀기, 격자에서 입자로 되돌리기(G2P), 격자 재설정으로 이어진다. 격자를 매번 재설정하므로 mesh distortion이 생기지 않고, 이것이 FEM과 달리 대변형에 강한 이유다. (L25–28)

### 변종의 갈래

MPM 변종은 주로 shape function을 어떻게 고르느냐로 갈린다. 원조인 standard MPM은 선형 hat 함수(C⁰)를 써서 입자가 격자 경계를 넘을 때 불안정해진다. GIMP는 C¹ smooth 함수로 이 cell-crossing 문제를 줄였고, B-spline MPM은 매끄러운 함수로 현재 널리 쓰인다. (L35–37)

다른 변종은 각기 다른 약점을 겨냥한다. CPDI는 사변형과 사면체 입자영역으로 극단적 인장에서도 수치적 파괴가 생기지 않게 했다. TLMPM은 격자가 초기 형상만 덮게 해 메모리를 줄였다. iMPM/MLS는 속도에만 MLS를 적용해 중간 격자에서 2차 수렴을 얻고 cell-crossing을 없앴다. (L38–40)

### 접촉과 파괴

원문은 no-slip, no-penetration 접촉이 MPM에 내재한다고 적었다. 속도장이 하나의 값만 가지므로 추가 비용이 들지 않는다. 마찰과 다물체 분리, 미끄럼에는 Bardenhagen 다물체 알고리즘이 표준이고, Nairn(2018)이 이를 점착을 포함한 임의 마찰법칙으로 일반화했다. (L44–46)

파괴는 세 가지 접근으로 나뉜다. 첫째는 균열을 명시적으로 두고 속도장을 여러 개 쓰는 discontinuous 방식이다. 둘째는 damage 변수로 응력을 떨어뜨리는 continuous 방식으로, 항복한 입자의 deviatoric 응력을 0으로 두는 particle erosion을 포함한다. 셋째는 continuum damage와 self-contact를 함께 쓰는 mixed 방식이다. (L49–51)

### 응용과 비교

응용은 지반공학, 유체-구조 상호작용, image-based 해석, 컴퓨터 그래픽스, 해빙, 눈사태, 폭발까지 넓다. image-based 해석은 voxel을 입자로 바꾸는 방식으로, foam 치밀화(Bardenhagen 2005)와 저밀도 눈, 고충전 복합재에 쓰였다. 배터리 쪽으로는 Si 음극의 chemo-mechanical MPM(Gritton 2017)이 있다. 오픈소스 코드로는 저자의 Karamelo(C++, LAMMPS 구조)와 Uintah, NairnMPM, CB-Geo, MPM3D가 소개된다. (L56–58 · 60–61)

원문은 다른 방법과의 비교도 정리했다. 대변형에서는 mesh distortion이 없어 FEM보다 유리하고, Taylor impact에서 LS-DYNA FEM보다 빨랐다. SPH보다는 neighbor search가 없어 빠르고 정확하다. DEM과 비교한 연구들은 적절한 구성식을 쓰면 MPM이 DEM 정확도를 재현할 수 있고, DEM에서 유도한 구성식으로 MPM을 대규모로 돌릴 수 있다고 보았다. (L63–65)

### 한계와 출처

원문은 MPM의 한계도 적었다. 수렴이 최적이 아니어서 1D에서도 FEM에 못 미치고, 매우 고운 격자에서는 수렴하지 않는다. 경계조건을 주기 어렵고, null-space 문제가 있으며, updated-Lagrangian MPM은 메모리를 많이 쓴다. (L68–69)

검토 측은 PDF 없이 초록, 서론, 일부 절 스니펫만 보고 정리했다고 밝혔다. 그래서 본문의 수식과 알고리즘, 수렴 수치는 담기지 않았다. 검토 측은 리뷰라서 1차 데이터가 없고, 이 문헌의 가치는 방법론의 지도와 계보에 있다고 본다. (L5–6 · 90–91)

### 용어 풀이 (논문에 없는 일반 설명)

- **PIC/FLIP**: 입자와 격자 사이에서 물리량을 주고받으며 유동을 계산하는 입자-격자 혼합 기법의 계보로, MPM이 여기서 나왔다.
- **cell-crossing 불안정**: 입자가 배경격자의 셀 경계를 넘을 때 shape function의 기울기가 불연속이라 힘 계산에 잡음이 생기는 현상이다.
- **updated-Lagrangian과 total-Lagrangian**: 변형된 현재 형상을 기준으로 계산하느냐, 초기 형상을 기준으로 계산하느냐의 차이다.

### 우리 연구에 주는 뜻

- 우리 MPM(Taichi MLS-MPM과 von Mises J2)은 MLS/B-spline 평활화를 쓰는 updated-Lagrangian 변종으로, 리뷰의 BSMPM과 iMPM 가지에 속한다. (L15 · 41)
- 우리 scaffold MPM에서 AM을 움직이지 않는 장애물로 둔 것은 MPM에 내재한 no-penetration 접촉을 가장 단순하게 쓴 것이고, 마찰이나 분리가 필요하면 Bardenhagen 알고리즘이 경로다. (L46–48)
- 우리 MPM에는 fracture가 없어서, SE 취성균열을 넣으려면 continuous damage나 cohesive 방식이 필요하며 Bardenhagen 2005의 image-based foam 치밀화는 DEM dump를 MPM 입자로 옮기는 우리 방식의 선례다. (L51–52 · 59 · 76 …)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| 참고문헌 수 | 339 ref | 리뷰 전체, 2019년 무렵까지 | L14 |
| 정리한 기간 | 25년 | Sulsky 1994 이후 MPM | L14 |
| 게재 쪽 | 185–398 | Advances in Applied Mechanics 53권 | L22 |
| 본문 수식·알고리즘 수 | 11개 | 본문 2–6절, 검토 측 미열람 | L6 |

### 읽을 때 조심할 것

- 검토 측은 초록, 서론, 일부 스니펫만 보았으므로 수식, 알고리즘, 수렴 수치를 이 기록에서 인용하면 안 된다. (L5–6 · 90)
- 리뷰라서 LPSCl 물성, 공극률, 응력 같은 1차 데이터가 없다. (L81 · 91)
- 원문은 MPM이 고운 격자에서 수렴하지 않고 경계조건 부여가 어렵다고 적었으므로, MPM 결과의 수치 정확도를 주장할 때는 이 한계를 함께 적어야 한다. (L68–69)
- 방법의 세부는 원전 알고리즘(Stomakhin 2013)이나 실제 코드로 따로 확인해야 한다. (L6 · 81)

### 원문에서 먼저 볼 곳

- 서론 1.1–1.6절은 변종 분류, 접촉, 파괴, 응용, 코드, 비교를 한 번에 정리한 곳이다. (L5 · 7)
- 2절 일반 MPM은 이 기록에 빠진 수식과 계산 주기의 세부를 담고 있다. (L6 · 92)
- 5절 contact, locking, fluid와 부록 B 구성식(Johnson-Cook 등)은 접촉 처리와 재료 모형을 고를 때 필요하다. (L92)

태그: MPM · MLS-MPM · B-spline MPM · GIMP · contact · fracture · MPM vs DEM · review

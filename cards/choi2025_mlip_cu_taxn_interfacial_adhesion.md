# Atomistic Insights into Cu/Amorphous-Ta x N Interfacial Adhesion via Machine Learning Interatomic Potentials: Effects of Stoichiometry and Interface Construction

*Ta 함량과 계면 제작법이 Cu/비정질 TaₓN 접착을 좌우한다*

- Choi et al. · ACS Appl. Electron. Mater 7, 11165-11179 (2025) · doi:10.1021/acsaelm.5c02157 · digest `choi2025_mlip_cu_taxn_interfacial_adhesion`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## Ta 함량과 계면 제작법이 Cu/비정질 TaₓN 접착을 좌우한다

> MLIP 기반 SMD와 Jarzynski 환산으로 Ta가 많고 섞임이 큰 계면일수록 Cu 접착이 강해짐을 보였다. (L22 · 40 · 88)

### 요점

1. VASP PBE 참조로 학습한 SevenNet MLIP로 Cu/비정질 TaₓN 계면을 세 가지 방법으로 만들고, steered MD(SMD) 분리일을 Jarzynski 등식으로 PMF로 환산해 work of adhesion을 구했다. (L22 · 66 · 75)
2. 원문은 Ta 함량이 늘수록 Cu–Ta 결합과 접착이 커지고, 계면 제작법은 relaxed, annealed, deposited 순으로 접착을 키운다고 적었다. (L40 · 89)
3. 검토 측은 큰 효과에 대한 결론은 믿을 만하나, SMD 파라미터 의존과 적은 반복 수 때문에 절대값과 미세한 차이는 조심해야 한다고 본다. (L137 · 139–140)

### 약한 Cu 접착

반도체 Cu 배선의 확산방지막인 비정질 TaₓN은 Cu 접착이 약하다는 문제가 있다. 비정질이라 grain boundary가 없어 확산 방지에는 유리하다. 그러나 접착이 약해 Ta, Co, Ru 같은 liner를 없애는 liner-free 배선이 막혀 있다. (L15 · 28)

원문은 Ta 조성과 계면 제작법이 접착을 어떻게 바꾸는지를 함께 묻는다. 기존 계산은 계면 제작을 짧은 상온 어닐로 단순화했고 두 변수를 따로 다뤘다. DFT는 계면 파괴를 보기에 셀이 작고, 고전 MD는 Cu, Ta, N이 섞인 결합에서 부정확하다는 것이 MLIP를 쓴 이유다. (L29–31)

- 그림 — Fig. 1: DFT 학습셋에서 기준 MLIP를 만들고, 계면 어닐, 증착, SMD 구성을 더해 다듬은 뒤 작은 셀로 검증하고 큰 셀로 분석하는 흐름을 본다. (L82)

### MLIP 학습과 검증

SevenNet은 두 단계로 학습했다. 첫 단계는 결정 다형체, 비정질 벌크, 표면으로 기준 모델을 만들었다. 둘째 단계는 기준 모델로 돌린 계면 어닐, SMD, 증착 구성을 DFT로 다시 계산해 학습셋에 더했다. (L56 · 58–59)

검증은 여러 물성에 걸쳐 했다. 원문은 검증 RMSE를 에너지 4.5 meV/atom, 힘 0.3 eV/Å, 응력 7.1 kbar로 적었다. 벌크 탄성률은 DFT 대비 5% 이내였다. 계면 MD 궤적에서는 에너지에 일정한 offset이 있었지만 힘은 DFT와 맞았다. (L43–45 · 85)

- 그림 — Fig. 3: 어닐, SMD, 증착 궤적에서 DFT 에너지와 MLIP 에너지가 일정한 간격을 두고 나란히 움직이는지를 본다. (L85)

### 계면 제작과 W_ad

계면은 세 가지 방법으로 만들었다. relaxed는 TaₓN slab과 Cu층을 2 Å 간격으로 붙인 뒤 정적 완화만 했다. annealed는 같은 접합을 1000 K에서 1 ns 동안 가열한 뒤 식혔다. deposited는 Cu 원자를 하나씩 쏘아 PVD 증착을 흉내 냈다. (L68–70)

work of adhesion(W_ad)은 SMD로 구했다. 가상 스프링으로 Cu slab 위쪽을 일정한 속도로 당겨 계면을 떼고 그 비평형일을 쟀다. 조건마다 세 번의 독립 SMD에서 얻은 일을 Jarzynski 등식으로 지수평균해 PMF를 복원하고, 완전 분리 plateau 높이를 W_ad로 삼았다. (L73–76)

- 그림 — Fig. 4: slab 생성, 세 가지 계면 제작, SMD 분리로 이어지는 W_ad 계산 순서를 본다. (L86)

### Ta와 섞임의 효과

원문은 Ta가 많을수록, 제작 과정에서 섞임이 클수록 접착이 강하다고 적었다. W_ad는 x가 1에서 4로 가며 커졌고 relaxed, annealed, deposited 순으로 컸다. 제작법 사이 차이는 Ta가 적은 계면에서 가장 컸다. 섞임 두께도 relaxed 6.16 Å, annealed 7.18, deposited 9.06 Å로 같은 순서였다. (L38–40 · 88 · 123)

기전은 계면 결합을 종류별로 세어 설명했다. Ta가 늘면 Cu–Ta 결합은 늘고 Cu–N 결합은 줄었다. deposited 계면에서는 Ta가 Cu 첫 층까지 들어가 cohesive strength를 키웠고, Cu 첫 층의 10%를 Ta로 바꾸면 모든 계면에서 W_ad가 더 올랐다. (L41 · 89 · 94–95)

- 그림 — Fig. 8: 세 조성과 세 제작법의 force-separation 곡선과 inset의 W_ad 막대를 비교한다. 단면적은 모든 경우 14.5 nm²다. (L42 · 90)

### 어디까지 믿나

검토 측은 W_ad가 당김 속도, 스프링 상수, 반복 수에 의존한다고 지적한다. Jarzynski 환산은 느린 당김과 충분한 반복에서만 수렴한다. 그런데 SMD는 조건당 세 번뿐이어서 W_ad 분산을 보기에는 적을 수 있다고 본다. (L139–140)

검토 측은 force 오차 수준이 x나 제작법 같은 큰 효과에는 충분하지만 미세한 조성 차에는 부족하다고 본다. MLIP는 PBE만큼만 정확하다는 한계도 그대로 물려받는다. (L137–138)

### 용어 풀이 (논문에 없는 일반 설명)

- **SMD (steered MD)**: 가상 스프링으로 원자 무리를 일정한 속도나 힘으로 끌어 원하는 경로를 강제로 진행시키는 비평형 분자동역학이다.
- **Jarzynski 등식**: 비평형 과정에서 한 일의 지수평균으로 평형 자유에너지 차를 구하게 해 주는 관계식이다.
- **PMF (potential of mean force)**: 한 반응 좌표를 따라 나머지 자유도를 평균한 유효 자유에너지 곡선이다.

### 우리 연구에 주는 뜻

- 우리 Stage11 rigid 분리법은 dangling-bond 인공일 때문에 W_ad 절대값이 100–1000× 과대인데, 검토 측은 이 논문의 SMD와 PMF 방식을 그 처방으로 본다. (L113 · 121)
- 이 논문의 벌크 탄성률 DFT 대비 5% 이내 검증은 우리 Nd₂O₃ B0 UMA 18.9 vs DFT 19.9 GPa 검증과 같은 종류여서 UMA 신뢰의 외부 근거가 된다. (L116 · 122)
- Cu–Ta와 Cu–N 결합 카운트는 우리 v14 Li–O, Cl–O 결합밀도 기술자와 같은 발상이다. (L118 · 124)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| MLIP 검증 에너지 RMSE | 4.5 meV/atom | refined SevenNet, 검증셋 | L43 |
| MLIP 검증 힘 RMSE | 0.3 eV/Å | refined SevenNet, 검증셋 | L43 |
| 벌크 탄성률 오차 | 5% 이내 | FCC Cu와 a-TaₓN, DFT 대비 | L45 |
| 섞임 두께 | relaxed 6.16 Å < annealed 7.18 < deposited 9.06 Å | Cu/a-Ta₂N, 제작법별 | L88 |
| SMD 스프링 상수와 속도 | k=0.01 eV/Å²/atom, v=0.01 Å/ps | 모든 SMD 공통 | L76 |
| 학습 데이터 크기 | 843,910 training points | 7984 구조, train:test 9:1 | L57 |

### 읽을 때 조심할 것

- Cu/a-TaₓN의 W_ad는 이온성 고체전해질 계면과 물리적으로 무관하므로 값을 직접 비교하지 않는다. (L135)
- 검토 측은 W_ad가 당김 속도, 스프링 상수, 반복 수에 의존하므로 같은 방법을 쓸 때 수렴 테스트가 필요하다고 본다. (L139)
- SevenNet은 이 계에 맞춰 자체 학습한 모델이라, 검토 측은 UMA로 SMD를 돌리면 큰 vacuum이 학습 분포 밖일 위험이 있다고 본다. (L136)
- 계면 궤적에서 MLIP 에너지에는 DFT 대비 일정한 offset이 있어 절대 에너지보다 힘과 거동을 믿는 편이 맞다. (L44 · 85)

### 원문에서 먼저 볼 곳

- Fig. 8은 세 조성과 세 제작법의 force-separation 곡선과 W_ad를 한 번에 보여 주는 결과의 중심이다. (L90)
- Fig. 3은 에너지 offset이 있어도 힘이 맞는다는 검증 근거라 MLIP를 분리 동역학에 쓴 이유를 판단할 수 있다. (L85)
- Fig. S5는 당김 속도와 스프링 상수에 대한 수렴 테스트라 W_ad 값의 신뢰 범위를 확인할 수 있다. (L139)

태그: Cu/a-TaₓN · SevenNet · MLIP · SMD · Jarzynski · work of adhesion · intermixing · melt-quench-anneal

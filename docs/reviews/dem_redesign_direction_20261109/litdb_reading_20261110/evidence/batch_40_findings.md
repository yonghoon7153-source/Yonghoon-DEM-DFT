# 배치 40 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-11)

읽은 카드 = 1/1: `gritton2017_mpm_chemomechanical_coupling_silicon_anode` (707 줄 · 논문 에이전트가 원문 PDF 23 쪽 = 표지 1 + 논문 22 쪽을 읽고 만든 카드 · 그림 10 + 식 56 장을 전부 열어 봄).  형식 = `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계`.
서지 (k · l 인용용) = Gritton C, Guilkey J, Hooper J, Bedrov D, Kirby R M, Berzins M, *Using the material point method to model chemical/mechanical coupling in the deformation of a silicon anode*, Modelling Simul. Mater. Sci. Eng. 25 (2017) 045005, DOI 10.1088/1361-651X/aa6830.  쪽 = 논문 쪽 (PDF 쪽 − 1).
카드의 성격: **규소 음극 나노기둥** (기둥 하나 + 기판) 의 리튬화 / 탈리튬화를 CPDI-MPM (Uintah) 으로 푼 방법 논문.  **압력 하중 · 압밀 · 기공 · 분말 · 물체 사이 접촉 · DEM 이 없다** → a · d · e · h · i 는 없음.  쓸 것은 f (MPM 수치 장치) · g · j · l · m 과 흐름 밖 (화학–역학 결합) 이다.  표지는 카드에 적힌 그대로다 (`인쇄` · `[판독]` · `[카드 산술]` · `[카드 판독]` · `[카드 추론]` · `[우리 코드 판독]` · `[우리 기록]` · `[미확인]`).

---

## a — 순수 SE 압력별 기공 곡선

이 배치에 없음 (황화물 · 기공 · 압력 하중이 논문에 없음).

## b — 탈압 때 되돌아오는 양 · 잰 방법

압력 하중은 없음.  대응하는 것 (자유 변형률을 넣었다 뺌) 만:
- [b] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 리튬화 → 탈리튬화 한 바퀴 뒤 끝 상태 (처음 대비): 높이 ×1.35 · 최대 폭 ×0.98 · 회전체 부피 ≈ ×1.1; 완전 리튬화 때는 폭 ×1.45 · 가운데 높이 ×3.40 · 부피 ≈ ×5.0 — "부피는 거의 돌아오고 모양은 안 돌아온다" | 카드 §3-5 · §0-2 (iv) · 논문 Fig. 10 · §4.7 p.19 | [판독] (내장 래스터의 윤곽 화소 계수 · 회전체 적분은 [카드 산술]) | 논문에 인쇄된 잔류 변형 값은 없음 (*"shows the amount of plastic deformation"* 한 문장) · 압력이 아니라 농도 유도 팽창 · 규소 · 계면은 붙은 채 (열림 없음) · 되돌아오는 탄성량 · 응력 값 없음

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 비정질 규소: 항복 응력 σ_Y 1.4 GPa (von Mises 항복면 √(3/2 σ_dev:σ_dev) − σ_Y = 0 · 완전 소성 또는 선형 등방 경화 · 소성 계수 1.15 GPa) · K 67 · G 31 GPa → E 80.6 GPa · ν 0.300 · E/σ_Y ≈ 58; 기판 σ_Y 0.7 GPa · K 180.4 · G 76 GPa → E 199.9 GPa · ν 0.315 | 카드 §3-1 · §4-5 · 논문 식 (34)(35) p.10 · p.11 · 13–19 | σ_Y · K · G · 소성 계수 = 인쇄 (출처 미인쇄 — *"reasonable values"*) · E · ν · E/σ_Y = [카드 산술] | **규소 · 이름 없는 기판 — LPSCl · NCM 값으로 쓰지 않는다** · von Mises 꼴이라 σ_Y 는 일축 항복 세기와 같은 정의이나 카드에 환산 서술은 따로 없음 · 경도 · 크리프 없음 · 탄성 계수는 농도와 무관하게 고정

## d — 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (입자 혼합이 없음).  관련만:
- [d] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 변형하는 기판은 기둥 팽창의 변형을 *"shared between both the pillar and the substrate"* — 단단한 (변형 않는) 기판에서는 바닥 모서리에 변형이 몰린다 | 카드 §5-6 · 논문 §4.6 p.18–19 · Fig. 9 | 인쇄 (정성) | 하중 몫의 값 없음 · 입자 층이 아니라 기둥 + 기판 · 계면 붙음

## e — 점접촉 법칙이 깨지는 범위 · 대안 · 맞춘 값 수

이 배치에 없음 (접촉 법칙 · DEM 이 논문에 없음).

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차

- [f] gritton2017_mpm_chemomechanical_coupling_silicon_anode | **접촉 알고리즘 없음** — 본문 · 참고문헌에 'contact' 0 회 · 기둥은 기판에 *affixed* (한 속도장으로 붙음 · 미끄럼 · 분리 없음) · 기판으로의 확산 없음 (거는 방법 미인쇄) | 카드 §4-7 · 머리 ③ · 논문 §4.6 p.17 · §4.7 p.19 | 인쇄 + [카드 전문 검색] · "한 속도장" 은 [카드 판독] | 다물체 · 마찰 · 강체 결합의 방법을 주지 않음
- [f] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 이산화 = CPDI 변종 (ref. [38]) · Uintah · 시간 간격 dt = min(dx/(c_s + v), dx²/2D) 를 매 걸음 다시 계산 (식 43–45 · 안전계수 미인쇄) · 1D 검증은 셀당 입자 2 · 3D 는 격자 간격 · 셀당 입자 수 · 입자 수 미인쇄 (작은 기둥의 입자 영역 ≈ 40 개/지름 · 간격 ≈ 2.5 nm) | 카드 §3-2 · §4-1 · §4-6 · 논문 p.3 · 5 · 12 | 인쇄 · 3D 입자 영역 수는 [판독] | **지름당 셀 수 같은 해상도 규칙은 없다** · 'explicit' 낱말도 본문에 없음 ([카드 판독])
- [f] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 수치 오차 추정 = 1D 확산 해석해 대비 입자별 상대오차의 노름 (식 14 · 15): 오차 0.56 · 0.049 · 0.0123 · 0.0068 · 0.0037 · 0.0016 · 0.00079 (h 0.1 → 0.001) · 저자 판정 O(h) · 인쇄된 노름 √(Σe²)/N 을 RMS 로 되돌리면 0.123 → 0.035 (h 0.02 → 0.001 · 기울기 ≈ 0.42) | 카드 §3-3 · 논문 §2.2 p.5–6 · Fig. 1 | 오차 값 = [판독] · O(h) = 인쇄 · RMS 환산 = [카드 산술] | 순수 확산 1D 뿐 — 역학 · 결합 · 3D 의 수렴 시험 없음 · 식 (13) 지수에 t 누락 (인쇄 어긋남)
- [f] gritton2017_mpm_chemomechanical_coupling_silicon_anode | **질량 (밀도) 스케일링**: 탄성파 시간 간격 (인쇄 6.8 × 10⁻¹¹ s · 산술 1.47 × 10⁻¹² s) ≪ 확산 시간 간격 0.05 s → 밀도를 인위로 올림 · 근거 = 준정적 ∇·σ = 0 (식 42) · a = (2G/ρ)∇·ε_dev + (3K/ρ)∇·ε_vol (식 49) · 시험 = 밀도 10⁵ 배 · 10⁶ 배 차 두 쌍 (2.33e3 ↔ 2.33e8 · 2.33e18 ↔ 2.33e24 kg/m³ — 본문은 둘 다 *five orders*) 이 *qualitatively* 같음 · 윤곽 높이 차 ≤ 1 % · 겉면 속도 ÷ 종파속 ≈ 5e-5 ↔ 1.6e-2 · 6e-6 ↔ 6e-3 | 카드 §3-4 · §4-6 · §8-2 · 논문 §4.1–4.2.1 p.11–14 · Fig. 3 · 4 | 식 · 밀도 · 저자 판정 = 인쇄 · 높이 차 = [판독] · 속도 비 = [판독 · 카드 산술] | 판정이 눈 대조 (응력 · 에너지 비교 없음) · 본 계산에 쓴 밀도 미인쇄 · 자유 팽창 문제 (가압 아님)

## g — 2D → 3D 경고 · 증거

- [g] gritton2017_mpm_chemomechanical_coupling_silicon_anode | *"while the pillar geometry lends itself to a 2D axisymmetric numerical solution for the purposes of this paper full 3D simulations will be performed"* — 축대칭 2D 로 줄일 수 있는 문제를 3D 로 풀었고 2D 해와 견주지 않음 | 카드 §0-2 (iii) · 논문 §4 p.11 | 인쇄 | 3D 를 택한 까닭 · 2D ↔ 3D 값의 차이는 없음
- [g] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 차원 축소 (구 대칭 1D 모형 [22, 23]) 에 대해: *"While the reduction of dimensionality can lead to insights … without the higher computational costs of higher dimensional simulations, key features associated with anode geometries will be lost."* | 카드 §0-2 (iii) · 논문 §1 p.3 | 인쇄 | 남의 모형에 대한 일반 문장 · 증거 수치 없음
- [g] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 2D 벤치마크에 **축대칭 MPM** (논문 ref. [41]) 을 쓰면 입자 하나 압축 · 구–블록 누르기가 그대로 3D 문제가 된다 | 카드 §9 ⑩ · §10 행동 4 | [카드 추론] | 논문 주장 아님

## h — DEM 에서 FE · MPM 으로 넘긴 선례

이 배치에 없음 (DEM 이 논문에 없음 · 초기 상태는 원기둥 기하).

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음.

## j — 카드가 스스로 적은 한계 (가압 · 탈압과 닿는 것)

- [j] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 계면이 붙어 있어 실험의 바닥 반경 팽창 ∼20 % 가 미끄럼 때문인지 기판 변형 때문인지 가를 수 없다 (*"It is unknown if …"*) | 카드 §0 · §11 #7 · 논문 §4.6 p.17 | 인쇄 | 판이 물러날 때 (탈압) 계면이 열리는지를 한 속도장으로는 물을 수 없다는 것과 같은 부류 ([카드 추론])
- [j] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 밀도 스케일링의 확인은 정성 (*"qualitatively the variations … are small"*) | 카드 §11 #5 · 논문 p.13–14 | 인쇄 | 응력 · 반력의 재하율 민감도는 재지 않음
- [j] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 입자 표면 넓이를 처음 값으로 고정 — *"not a valid assumption"* · 향후 변형 구배로 갱신 | 카드 §11 #1 · 논문 §2.3 p.7 | 인쇄 | 큰 변형에서 표면 · 계면에 걸리는 양 (피복 넓이 등) 에 같은 주의
- [j] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 변형률 속도는 Hencky 변형률 속도의 근사 (주축 회전이 작을 때) | 카드 §11 #4 · §4-5 · 논문 §3.2 p.9 | 인쇄 | 큰 전단 회전이 있는 압밀 유동에서의 오차는 다루지 않음
- [j] gritton2017_mpm_chemomechanical_coupling_silicon_anode | 손잡이 (α · β · p_max) 에 따라 변형 거동이 달라진다 · 파괴 없음 · 전기화학 없음 | 카드 §11 #6 · #9 · #10 · 논문 p.16 · 20 | 인쇄 | 가압 계산과는 간접

## k — DEM 의 한계 (서지 병기)

- [k] gritton2017_mpm_chemomechanical_coupling_silicon_anode (Gritton 외 · Modelling Simul. Mater. Sci. Eng. 25, 045005, 2017) | **말 없음** — DEM 을 쓰지도 언급하지도 않는다 ('DEM' · 'discrete element' 0 회 · 참고문헌 52 건에도 없음).  다른 방법에 대한 문장은 성공을 적는다: *"Mesh based methdods such as FEM [27] and XFEM [28] have found success along with meshless methods such as SPH [29] and RPKM [30].  An alternative to these approaches that has been found to be successful in modeling large deformations is the material point method (MPM) [31]."* | 카드 §0-2 (i) · 논문 §1 p.3 | 인쇄 + [카드 전문 검색] | DEM 한계의 인용처로 쓸 수 없음

## l — 소성변형이 왜 어려운가 (서지 병기)

- [l] gritton2017_mpm_chemomechanical_coupling_silicon_anode (Gritton 외 · Modelling Simul. Mater. Sci. Eng. 25, 045005, 2017) | 어려움 ① 결합 + 큰 변형: *"The main challenges in modeling this process using the MPM is to simulate stress dependent diffusion coupled with concentration dependent stress within a material that undergoes large deformations.  MPM is chosen as the numerical method of choice because of its ability to handle large deformations."* | 카드 §0 · §0-2 (ii) · 논문 초록 p.1 | 인쇄 | 큰 변형 계산의 정확도 시험은 없음 (1D 확산뿐)
- [l] gritton2017_mpm_chemomechanical_coupling_silicon_anode (같은 서지) | 어려움 ② 시간 척도: 명시 풀이의 탄성파 시간 간격으로는 *"10¹¹ time step integrations would be needed to reach 6.8 s of simulation time.  The number of time steps for this calculation would be intractable."* → 우회 = **밀도 인위 증가** (*"the density of silicon is artificially raised to a value such that the limiting time step criteria is dependent upon the numerical solution of the diffusion equation"*) · 시험 밀도 최대 2.33 × 10²⁴ kg m⁻³ | 카드 §0 · §3-4 · §4-6 · 논문 §4.2.1 p.12–14 | 인쇄 (식 46 의 값은 인쇄 어긋남 — 카드 §12 #5) | 준정적 문제에만 · 판정은 눈 대조
- [l] gritton2017_mpm_chemomechanical_coupling_silicon_anode (같은 서지) | 어려움 ③ 이력 의존: *"Both the perfectly plastic and the linear strain hardening constitutive models are dependent upon the prior history of the material.  Because of this history dependent behavior the choice of flux boundary conditions affects the shape of the pillars."* — 유속 10 배 차이가 완전 리튬화 뒤의 모양에도 남는다 (Fig. 6 · 7) | 카드 §5-4 · §9 ⑦ · 논문 §4.4 p.15 | 인쇄 | 규소 기둥 사례
- [l] gritton2017_mpm_chemomechanical_coupling_silicon_anode (같은 서지) | 택한 우회와 값: hypoelastic–plastic (변형률 속도 덧셈 분해 d = d^e + d^p + d^c · 회전 전 자리 · J2) + CPDI + 밀도 스케일링.  **맞춘 값**: 실험에 정량으로 맞춘 것 없음 — 손잡이 α 6.0 · β 0.5 (0 · 1 도 시험) · p_max 3 GPa · η 0.56 · 유속 10⁻⁹ / 10⁻⁸ 을 정하고 눈으로 견줌 (전선 뒤 농도 0.5–0.6 / > 0.7 ↔ 실험 ∼0.67).  **검증**: 1D 확산 해석해 (O(h)).  **비용**: 큰 기둥 + 기판 한 바퀴 9 코어 · 27,472 걸음 · 48.57 h (6.36 s/걸음 · 437 코어·시간) · 입자 수 미인쇄 | 카드 §0-2 (ii) · §3-1 · §3-6 · 논문 p.9 · 14–16 · 19 | 인쇄 · 걸음당 시간 = [카드 산술] | 연화 영률 같은 우회는 없음 (실제 계수 그대로 · 물체 하나라 재배열이 없음)

## m — 받아들일 통찰 (무엇을 · 우리 쪽 어디에 · 근거)

- [m] gritton2017_mpm_chemomechanical_coupling_silicon_anode | **준정적 사다리의 통과 기준에 응력 (판 반력 · 정착 응력) 을 넣는다** — 이 논문의 질량 스케일링 시험은 형상만 견줬고 (윤곽 높이 차 ≤ 1 % · 겉면 속도 ÷ 종파속 ≈ 6e-3–1.6e-2 까지), 우리 실측은 같은 스트로크에서 기하는 같고 응력만 달랐다 → 재하율의 흔적은 형상보다 응력에 먼저 난다 | 단계 2 (U0 · U6) ; 단계 4 ; 단계 5 | 카드 §3-4 · §8-2 · §9 ② · 논문 Fig. 3 · 4 · p.13–14 ([판독] · [카드 산술] · [우리 기록])
- [m] gritton2017_mpm_chemomechanical_coupling_silicon_anode | **'한 속도장으로 눌렀다 떼기' 를 기준선 팔로 먼저 기록** — 붙은 계면은 수축 (하중 제거) 때 열리지 않고 상대를 끌고 온다 (Fig. 9 · 10 의 턱 · 자국) · 저자 스스로 미끄럼 ↔ 상대 변형을 가를 수 없다고 적음 → 분리 규칙을 넣은 팔과 겹쳐야 차이가 보인다 | U3 ; U4 ; 단계 6 ; 후보 A′-0 | 카드 §0 (2) · §9 ④ ⑤ · §10 행동 3 · 논문 §4.6 p.17 · Fig. 9 · 10 (인쇄 + [판독])
- [m] gritton2017_mpm_chemomechanical_coupling_silicon_anode | **늘어나는 구역의 물질점 간격 ÷ dx 를 산출물에 적는다** — 이 논문은 높이 ×3.4 까지 늘어나는 변형 때문에 입자 영역을 추적하는 CPDI 를 골랐다; 우리 MLS-MPM (2차 B-spline) 은 영역을 추적하지 않으므로 SE 가 틈으로 밀려 들어가는 자리에서 물질점이 셀보다 멀어지면 수치적으로 끊긴다 | U1 ; 단계 4 ; 단계 5 ; 조건 R6 | 카드 §9 ⑨ · §10 행동 2 · 논문 초록 · p.3 · Fig. 10 ([판독] · [카드 추론] · [우리 코드 판독])
- [m] gritton2017_mpm_chemomechanical_coupling_silicon_anode | **자유 변형률 (열 · 화학 팽창) 을 속도 꼴로 넣을 때 계수는 로그 변형률 기준** — η 0.56 은 1.56³ = 3.80 (+280 %) 로 고른 값인데 d̄^c = η ċ I 를 적분하면 exp(3η) = 5.37, 그림 판독은 ×4.0–5.0; 첫 단위 시험 = 구속 없는 균일 팽창의 부피비 | 흐름 밖: 충방전에 따른 AM 부피 변화 (사이클 화학–역학) 를 MPM 에 넣을 때 · 변형과 함께 푸는 수송 (확산 5 단계 식 4–8 + 1D 해석해 시험) | 카드 §3-5 · §9 ⑥ · §10 행동 5 · 6 · 논문 식 (32)(33) p.10 · η p.14 ([카드 산술 · 카드 판독 · 논문 밖])

## n — 논문 에이전트 후보 (litdb 에 카드 없음 · 많아야 다섯)

(서지는 이 논문 참고문헌 목록에 적힌 그대로 · litdb 확인 = 정본 `papers/` 파일 목록에서 제1 저자 성 · 제목 낱말을 찾음 — 파일 없음.  괄호 안은 그 논문을 언급만 하는 기존 카드.)

- [n] [38] Sadeghirad A, Brannon R M and Burghardt J 2011 A convected particle domain interpolation technique to extend applicability of the material point method for problems involving massive deformations Int. J. Numer. Methods Eng. 86 1435–56 | f · l · m — 큰 신장에서 MPM 이 수치적으로 끊기는 문제와 입자 영역 추적 (CPDI) 의 원전.  이 카드 (§4-1 · §9 ⑨) 와 `homel2017_…` 카드가 둘 다 CPDI 로 계산했는데 원전 카드가 없다 → "우리 B-spline MLS-MPM 은 어디까지 늘어나도 되는가" 의 기준 | 카드 없음 (언급만: devaucorbeil2020 · homel2017)
- [n] [41] Nairn J A and Guilkey J E 2015 Axisymmetric form of the generalized interpolation material point method Int. J. Numer. Methods Eng. 101 127–47 | g · f — 축대칭 MPM: 2D 벤치마크 (입자 하나 압축 U1 · 구–블록 누르기 U3) 를 3D 와 같은 문제로 푸는 길 (카드 §9 ⑩ · §10 행동 4) | 카드 없음 (Nairn 언급만: devaucorbeil2020 · homel2017 — 다른 논문)
- [n] [34] Steffen M, Wallstedt P C, Guilkey J E, Kirby R M and Berzins M 2008 Examination and analysis of implementation choices within the material point method (MPM) Comput. Modeling Eng. Sci. 31 107–27 | f — MPM 구현 선택 (갱신 순서 · 기저 함수) 의 오차 분석.  이 논문이 "MPM 알고리즘은 [34, 38] 대로" 라고 넘긴 자리 (카드 §4-1) — 수치 오차를 어떻게 추정했는가의 원전 후보 | 카드 없음 (Steffen 언급만: stomakhin2013)
- [n] [36] Steffen M, Kirby R M and Berzins M 2010 Decoupling and balancing of space and time errors in the material point method (mpm) Int. J. Numer. Methods Eng. 82 1207–43 | f — 공간 · 시간 오차를 갈라 균형 맞추는 법 → 격자 간격 · 시간 간격 규칙 (U1 · U6 의 수렴 판정) | 카드 없음
- [n] [37] Bardenhagen S G and Kober E M 2004 The generalized interpolation material point method Comput. Modeling Eng. Sci. 5 477–96 | f — GIMP 원전 (물질점이 셀을 넘을 때의 잡음 · 가중 함수의 일반 꼴) — CPDI · 우리 B-spline 가중의 비교 기준 | 카드 없음 (언급만: devaucorbeil2020)

덧붙임: 이 논문 ref. [31] Bardenhagen S G, Brydon A D and Guilkey J E 2005 Insight into the physics of foam densification via numerical simulation J. Mech. Phys. Solids 53 597–617 도 카드가 없으나, 같은 날 inbox 에 PDF 가 있어 (`78ceea61-19._Insight_into_the_physics_of_foam_densification_…pdf`) 따로 반입 중으로 보여 후보에 넣지 않았다.

## 카드 문제

- 카드 자체의 모순은 찾지 못함 (새로 만든 카드 — 숫자는 `[판독]` · `[카드 산술]` 로 표지).  읽을 때의 주의 셋:
  1. 카드의 부피 · 높이 · 폭 배수 (§3-4 · §3-5) 는 전부 그림 윤곽의 화소 계수다 — 논문에 인쇄된 값이 아니며 방법 오차 ± 10 % 안팎 (카드가 끝 상태 ≈ ×1.1 로 미루어 적음).  값으로 인용하지 않는다.
  2. "겉면 속도 ÷ 종파속" (§3-4 · §8-2) 과 dt_mb 표는 dx_cell = 10⁻⁸ m (논문의 예시 값) 와 고정 바닥 폭 = 0.1 µm 를 가정한 카드 산술이다 — 3D 계산의 실제 격자 간격은 논문에 없다.
  3. 논문 쪽 인쇄 어긋남 15 곳 (카드 §12): 식 (13) 지수의 t · 식 (15) 의 ÷ N · 식 (18) 의 번호 칸 "(18rate of change of the elastic)" · 식 (21) 의 γ · 식 (46) 의 6.8 × 10⁻¹¹ s (산술 1.47 × 10⁻¹² s) · Fig. 3 · 4 캡션 · *five orders* ↔ 인쇄된 밀도 10⁶ 배 차 등.  식 그림은 인쇄 그대로 잘랐다.

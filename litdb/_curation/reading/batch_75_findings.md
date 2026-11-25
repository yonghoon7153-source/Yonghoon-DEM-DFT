# batch_75 — 질문 a–n 근거 (카드 1 편: `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` · 2026-11-12)

서지 (카드 머리): John Paul Morrissey, *Discrete Element Modelling of Iron Ore Pellets to Include the Effects of Moisture and Fines*, PhD thesis, Institute for Infrastructure and Environment, School of Engineering, University of Edinburgh (2013) · DOI 없음 [미확인].
쪽 = 학위논문 인쇄 쪽 (p.N).  재료 = 철광석 미분 (수분 접착) · DEM 입자 = 응집체 대리 (meso) · 3D · 응력 ≤ 120 kPa — 전지 재료 · 300 MPa 와 다르다.

## a — 순수 SE 의 압력별 기공 곡선 (진밀도 · 질량 기준 · 누른 채/뺀 뒤)
- [a] morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis | 순수 SE (황화물) 값 없음 — 같은 꼴의 단일 재료 곡선만 (철광석 미분 DEM): Δγ 8 J/m² 에서 시작 0.571 → 100 kPa 누른 채 0.3336 → 뺀 뒤 0.3447 (다공도) · 밀도 2758 → 2718 kg/m³ | 카드 §3-5 · 그림 7.23 · 7.15 (p.203 · p.197) | [판독-벡터] | 철광석 meso 응집체 · ≤ 100 kPa · 기공 = 1 − ρ_bulk/ρ_particle (식 2.5 · 고체 보존) · a 질문에는 해당 없음 (참고 꼴만)
- [a] 같은 카드 | ⚠ 표 6.2 · 6.10 · 6.11 의 *"Consolidated Porosity"* 는 그림의 '뺀 뒤 (몰드 안)' 다공도와 0.001–0.007 안에서 같다 → 표 값은 누른 채가 아님 | 카드 §3-3 (a) · 원문 대조 기록 | [판독-벡터 대조] · 원문은 정의 없음 | 상태 표기가 없는 문헌 표를 읽을 때의 함정 (철광석)

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] morrissey2013_… | DEM (보정 KPRS · 판을 25 mm/s 로 들어 0 까지 · 몰드 벽 마찰 0): 100 kPa 정점 변형률 0.3635 → 뺀 뒤 0.3505 · Δε 0.0130 = 정점의 3.6 % = 압축된 높이의 2.05 % (Δγ 8) · Δγ 23.5 는 0.0170 (4.6 % · 2.70 %) | 카드 §3-5 표 · 그림 7.14a · b (p.196) | [판독-벡터] · 높이 기준 비 = [카드 산술] | 철광석 meso · ≤ 100 kPa · 단일 시드
- [b] 같은 카드 | 회복의 40–85 % 가 5 kPa 아래 (압밀 응력이 클수록 몫이 작다 · 100 kPa 에서 40–42 %) — 저자 해석 = 몰드 벽 마찰 0 이라 탄성 되돌아옴이 큼 · 줄이려면 k₂ 를 10 배 이상 (시간 간격 ↓) | 카드 §3-5 · p.196 | [판독-벡터] · 해석 = [인쇄] | 같음
- [b] 같은 카드 | 손잡이별 Δε (100 kPa · 몰드 안): k₂/k₁ 10 · 25 · 50 → 0.0087 · 0.0068 · 0.0053 · k₁ (G 2.5 · 5 · 7.5 MPa) → 0.0306 · 0.0202 · 0.0163 · 접선 강성 배수 κ_tm 1 → 0.1 (구) → 0.0177 → 0.0504 · 전역 감쇠 없음 → 0.75 에서 뺀 뒤 다공도 증가 0.0177 → 0.0106 · 반발 계수 무관 | 카드 §3-5 · 그림 6.4 · 6.7 · 6.12 · 6.37–6.38 · 6.43 | [판독-벡터] | 6 장 매개변수 연구 (같은 충전에서 갈라 쓴 비교 · 단일 시드)
- [b] 같은 카드 | 탄성 접착 (JKR) DEM: 100 · ~250 ('200' 범례) · 500 kPa 정점 변형률의 49 · 52 · 55 % 가 돌아옴 (0.0545 → 0.0278 등) | 카드 §3-5 · 그림 3.16a (p.60–61) | [판독-벡터] | JKR 시험의 입자 강성 · 크기 · 충전 미인쇄 → EEPA 와 같은 조건 비교 아님
- [b] 같은 카드 | 실험 (EPT 몰드 안 · ≈ 115 kPa → 0): 되돌아옴 ≤ 0.1 mm (≤ 0.2 % · 분해능 0.1 mm) — *"the unloading curves are almost vertical"* · 몰드 · 하중을 뺀 뒤 높이 (부록 E 두 칸) KPRS +2.1–5.3 % (표 E.6–E.8 · 1–3 % MC · 20–100 kPa) · KPBO +2.9–7.0 % (표 E.1–E.5) | 카드 §3-5 · 부록 C · E · p.118 | [인쇄] · 비 = [카드 산술] · 부록 E 칸 정의 [미확인] | 철광석 미분 실험 · 측정 시점 미확인
- [b] 같은 카드 | 뺄 때 K0 (수평/수직 응력비) 가 100 kPa 의 ≈ 0.30–0.36 에서 뺀 끝 ≈ 0.69 까지 오름 = *"locked-in"* 수평 응력 (실험도 같은 방향 · 그림 5.49) | 카드 §3-5 · p.149 · 그림 6.6 | [판독-벡터] · [인쇄] | 몰드 벽 힘으로 잼

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기 환산
- [c] morrissey2013_… | EEPA 에는 항복점이 없다 — *"For simplification purposes, the EEPA model omits the yield point"*; 소성 = 강성비 C_p = 1 − k₁/k₂ (보정 0.98 · k₂ : k₁ = 40) | 카드 §0 · §4-2 · 식 (6.1) · p.77 · p.150 | [인쇄] | 접촉 법칙 수준 · 경도 · σ_y 없음
- [c] 같은 카드 | 실험 벌크 강도 (일축 항복 = 무구속 강도 σu vs 압밀 σ₁): KPRS 1 % MC 17.75 · 37.75 · 57.85 · 77.27 · 96.27 kPa → 2.00 · 3.75 · 6.63 · 8.46 · 11.38 kPa (부록 표 E.6) · Jenike φ 44° (KPRS) · 45° (KPBO) · 7.5–8.5 % 물에서 c 1.36–2.18 kPa (표 5.15) | 카드 §3-4 · §3-6 | [인쇄] | 철광석 · kPa 범위 · 입자 항복 세기로 환산하는 식은 카드에 없음
- [c] 같은 카드 | 크리프 · 시간 압밀 (caking) 은 모델에 없음 (저자 권고 항목) · KPRS 가 건조 뒤 단단한 응집체 (그림 5.39–5.40) | 카드 §3-6 · §9.2 (p.261–262) | [인쇄] | 값 없음

## d — 단단한 입자와 무른 입자를 섞을 때 하중 몫 · 재밍
- 이 배치에 없음 (한 재료 · 이종 접촉 규칙 없음 — 카드 §0-1).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값 수
- [e] morrissey2013_… | EEPA = 탄성 접착 (JKR · DMT · EDEM linear cohesion · 모세관) 의 대안 (응력 이력을 내기 위해) — 그러나 '큰 변형 고치기' 는 아니다: 겹침 *"typically less than 1% of the particle diameter"* 전제 · 항복점 생략 | 카드 §0-1 · §4-2 · p.39 · p.77 | [인쇄] | 저응력 · 철광석
- [e] 같은 카드 | 맞춘 값 (7 장): k₁ (G 2.5 × 10⁶ Pa · 2.5 · 7.5 · 50 MPa 시행으로 고름) · k₂ : k₁ = 40 · μs 0.5 (Härtl–Ooi 형상–마찰 지도로 미리 고정) · 함수율마다 Δγ 1 개 (8 · 12.5 · 18.5 · 23.5 J/m²) + 고정 선택 (μr 0.005 · ν 0.225 · e 0.5 · 전역 감쇠 0.5 · 쌍구 AR 1.5) · 보정 대상 = 실험 5 점 | 카드 §3-4 · 표 7.1–7.3 | [인쇄] | 철광석 유동 함수
- [e] 같은 카드 | 저자의 다른 대안 평가: Thornton (1997) 탄성–완전소성은 FEA 대비 *"too soft"* (Vu-Quoc–Zhang 1999b) · 소성 모델은 *"difficult to establish the model parameters"* · Tomas 는 계산 무거움 · Luding 접착 정의는 벌크 값과 잇기 어렵다 · *"these linear models maybe too soft at higher stresses"* | 카드 §4-8 · p.48 · p.54 · p.62 · p.77 | [인쇄] | 문헌 평가 (원문 2 차)

## f — MPM 의 접촉 · 다물체 · 해상도 규칙
- 이 배치에 없음 (MPM 없음 · 거친 평균 반지름 2.5–3R 은 DEM 후처리 규칙 — 카드 §6).

## g — 2D 결과를 3D 로 옮길 때의 경고 · 증거
- [g] morrissey2013_… | 한 겹 평면에서만 전단띠가 또렷: *"Even in an assembly of particles that is just a few particles thick the dilation that is occurring during shearing can be lost through interactions with particles in three dimensions"* · 3D 원통은 *"no shear zone will exist, or that it may not be possible to detect it"* · 평면 시험 띠 안 고체 분율 20–30 % 낮음 | 카드 §0 ⑪ · §3-4 · §4-10 (iii) · p.209 · p.210 · p.212 | [인쇄] | 철광석 평면 6000 구 · 3D 원통 · 2D → 3D 값 전이 문장은 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례 · 시점
- 이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
- 이 배치에 없음.

## j — 카드가 '아직 못 한다 · 한계' 라 적은 것 (가압 · 탈압 관련)
- [j] morrissey2013_… | 과압밀 (취성) 피크는 다공도 < ≈ 40–45 % 에서만 · 무구속 정점 변형률 DEM 1.5–3 % ↔ 실험 3–6 % · 무구속 강성 못 맞춤 | 카드 §3-4 · §11 · p.199–201 · p.216 | [인쇄] | 철광석 · 단분산 · 한 모양이 원인일 수 있다 (저자)
- [j] 같은 카드 | 실제 벌크 강성 (G ~10⁸ Pa) 포기 — 유동 함수에 맞춘 G 2.5 × 10⁶ Pa 로 *"the compromise of only predicting the experimental bulk stiffness for moisture contents greater than 1%"* | 카드 §3-4 · §7-3 · p.189 · p.191 | [인쇄] · 40 배 = [카드 산술] | 같음
- [j] 같은 카드 | 5 kPa 아래 제하 탄성 과대 (벽 마찰 0) · 1 % MC 는 60 kPa 아래 유동 함수 과대 (≈ 1.4–1.6 배) · K0 0.32–0.34 ↔ 실험 0.24 (Mylar 보정 0.29) · 시간 압밀 · 온도 · 사일로 실험 검증 없음 | 카드 §3-4 · §3-5 · §9 · p.196 · p.201–202 · p.261–262 | [인쇄] · 배수 = [카드 산술] | 같음

## k — DEM 의 한계 (인용 가능 서지 + 원문 문장)
- [k] morrissey2013_… (Morrissey 2013 · PhD thesis · University of Edinburgh) | *"The particles are rigid but are subject to local deformation in places of contact and the resulting forces from particle overlap are calculated"* | 카드 §4-10 (i) · L285 · p.37 | [인쇄] | 일반 서술
- [k] 같은 서지 | 겹침 *"typically less than 1% of the particle diameter"* — 믿을 겹침의 상한 서술 | 카드 §4-10 (i) · p.39 | [인쇄] | 일반 서술 (수치 시험 없음)
- [k] 같은 서지 | *"DEM's major flaw is its computational requirement … It is also difficult to incorporate crushing and pore-pressure"* · *"Contact models tend to be relatively simplistic in the way they describe the material behaviour in an attempt to keep the computational costs down"* · *"The effect of asperities and surface roughness is not explicitly considered in any of the commonly used contact models"* | 카드 §4-10 (i) · p.27 · p.44 · p.62 | [인쇄] | 같음
- [k] 같은 서지 | 보정값은 물성이 아님 — 매개변수는 *"phenomenologically based"* (p.64) · E 6.13 MPa = *"the stiffness of the agglomerate"* (p.148) · 실제 벌크 강성에는 G ~10⁸ Pa 가 필요했다 (p.189) | 카드 §0 · §4-1 · §3-4 | [인쇄] | 철광석 meso
- [k] 같은 서지 | 구는 큰 회전 · 벌크 마찰 ≈ 30° 에서 포화 (Härtl–Ooi 2011 외 인용) · 단분산 · 한 모양이 과압밀 거동을 못 내는 원인일 수 있다 | 카드 §4-10 (i) · p.27 · p.201 · p.216 | [인쇄] | 2 차 인용 포함

## l — 소성변형이 왜 어려운가 · 택한 우회와 값
- [l] morrissey2013_… (Morrissey 2013 · PhD thesis · University of Edinburgh) | 이유: 소성 접촉 모델 (Thornton 1997 · Vu-Quoc 2001) 은 *"it is difficult to establish the model parameters for various materials from laboratory experiments"* · Tomas 는 계산이 무거움 · Luding 의 접착 정의는 *"difficult to relate to bulk material properties"* · AFM 미시 보정은 산포가 크다 | 카드 §4-8 · §4-1 · p.48 · p.54 · p.62 · p.64–65 | [인쇄] | 문헌 평가
- [l] 같은 서지 | 우회: 항복점을 뺀 강성비 이력 (k₂ : k₁) + 접촉 크기에 따라 자라는 접착 + 응집체 (meso) 입자 + 벌크 시험 보정 — 맞춘 값 = k₁ (G) · k₂ : k₁ · Δγ (함수율마다) + μs (문헌 지도) · 검증 = 해석해 (≤ 0.08 %) · 실험 5 점 보정 뒤 나머지 예측 (대부분 실험 표준편차 안) | 카드 §0 · §3-2 · §3-4 · p.77 · p.183–198 | [인쇄] | 철광석 · ≤ 120 kPa
- [l] 같은 서지 | 비용: 강성 ↑ → 시간 간격 ↓ (*"Increasing contact stiffness leads to decreasing simulation time-steps"* p.143 · 사일로 *"Reduced particle stiffness has been utilised to reduce the computational timestep"* p.218) · 제하 탄성을 줄이려면 k₂ 를 한 자릿수 키워야 하나 시간 간격이 준다 (p.196) · 입자 3,000–61,000 · Δt 1 × 10⁻⁷–5 × 10⁻⁶ s · 실행 시간 미기재 | 카드 §3-1 · §4-10 (ii) | [인쇄] · 실행 시간 [미확인] | 같음

## m — 받아들일 통찰 (가져다 쓸 것)
- [m] morrissey2013_… | 되돌아옴 결과에 손잡이 목록을 같이 등록한다 (k₂/k₁ · k₁ 연화 · 접선 강성 규칙 · 감쇠 · 벽 마찰 · 판 속도) — 같은 100 kPa 에서 이것들만으로 Δε 가 0.016 ↔ 0.050 (3 배) | 단계 6; 조건 R4; 후보 D0 | 카드 §3-5 · §9-1 | [판독-벡터] | 철광석 · 저응력 (크기 감각만)
- [m] 같은 카드 | 기공 · 다공도 칸에 상태를 따로 둔다 (누른 채 · 판 정지 · 판 뺀 뒤 · 측면 구속 해제 뒤) — 이 학위논문 표 '압밀 다공도' 는 그림과 대조해야 '뺀 뒤' 임이 드러났고 상태 차가 0.010–0.045 | 단계 0; 결과 전 대조 항목 | 카드 §3-3 · §8 단계 0 | [판독-벡터 대조] | 같음
- [m] 같은 카드 | 접촉 법칙 단위 시험 꼴: 두 입자 반복 하중 (δp · f_min · δ_min 해석해와 칸마다 대조 · k₂ : k₁ 1–40) + 7 개 반발 계수 충돌 + 탄성 충돌 에너지 보존 | U3; U5 | 카드 §3-2 · 표 4.1–4.5 · 그림 4.12–4.21 | [인쇄] | 두 입자 · 선형/비선형 EEPA
- [m] 같은 카드 | 함정: 제하 · 재하 가지가 따로 있는 접촉에 감쇠를 걸면 힘이 가지를 따라 진동 → *"premature separation of the particle contacts"* — 언로딩에서 접촉 수가 갑자기 줄면 판 속도 · 감쇠를 바꿔 물리인지 인공물인지 먼저 가른다 | 단계 6; 후보 D0 | 카드 §3-5 · p.176 | [인쇄] | EDEM EEPA (같은 꼴의 hooke/hysteresis 에도 해당할 수 있음 = 추정)

## n — 논문 에이전트 후보 (카드가 인용 · litdb 카드 없음)
- [n] Thakur, S.C., Morrissey, J.P., Sun, J., Chen, J.F., and Ooi, J.Y. (2011). A DEM study of cohesive particulate solids: plasticity and stress- history dependency. In: 11th Particulate Systems Analysis Conference: PSA2011, Edinburgh, UK, pp. 1–5. | C_p = 1 − k₁/k₂ (식 6.1) 의 인용처 · k₂ : k₁ = 40 의 근거 · 'EEPA' 이름이 처음 나왔는지 (카드 [미확인] 목록) — 질문 c · e | litdb 확인: papers/ 에 thakur2011 없음 (thakur2014 만) · 'PSA2011' grep = 이 카드뿐
- [n] Vu-Quoc, L. and Zhang, X. (1999b). An elastoplastic contact force-displacement model in the normal direction: displacement-driven version. Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences, 455(1991): pp. 4013–4044, doi:10.1098/rspa.1999.0488. | FEA 로 '선형 · Thornton 탄소성 접촉은 고응력에서 너무 무르다' (그림 3.7 · p.48 · p.77) — 점접촉 법칙이 깨지는 범위 (질문 e · k · l) · 후보 C′ | litdb 확인: vuquoc 카드 없음 (demirtas2021 · 이 카드가 언급만)
- [n] Walton, O.R. and Johnson, S.M. (2009). Simulating the Effects of Interparticle Cohesion in Micron-Scale Powders. In: AIP Conference Proceedings - Powders And Grains 2009 … pp. 897–900, doi:10.1063/1.3180075. (서지 일부만 — 편집자 · 장소는 카드 §12) | 떼는 힘 증가율을 끌어당김 기울기와 분리 (EEPA 의 X 와 같은 생각) · 비틀림 · 굽힘 · 이력 변수 δ₀ (카드 §4-8) — 질문 e · 믹서 접착 | litdb 확인: walton 카드 없음 (pasha2014 · 이 카드가 언급만)
- [n] Tykhoniuk, R., Tomas, J., Luding, S., Kappl, M., Heim, L.O., and Butt, H.J. (2007). Ultrafine cohesive powders: From interparticle contacts to continuum behaviour. Chemical Engineering Science, 62(11): pp. 2843–2864, doi:10.1016/j.ces.2007.02.027. | 단순 선형 접착 모델로도 Tomas 모델의 핵심 거동이 나온다 (meso 보정의 근거 · p.54 · p.64) — 질문 e · l · 후보 M0 | litdb 확인: tykhoniuk 카드 없음 (이 카드만 언급)
- [n] Chung, Y.C. and Ooi, J.Y. (2007). Influence of Discrete Element Model Parameters on Bulk Behavior of a Granular Solid under Confined Compression. Particulate Science and Technology, 26(1): pp. 83–96, doi:10.1080/02726350701759381. | 구속 압축 DEM 의 매개변수 민감도 · 충전 의존 (p.94 · p.152 · p.203) — 단계 4 · 단계 6 (구속 압축 · K0) · 질문 b | litdb 확인: chung 카드 없음 (coetzee2017 · 이 카드가 언급만)

## 카드 문제
- `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L239 *"EEPA — 카드 없음"* → 이 카드로 낡았다 (그 줄은 고치지 않음).  같은 카드 L29 · L61 의 EEPA 계산비 (1/2 · +100 %) 는 Klama 2017 의 값 — 이 학위논문에는 계산 시간이 없다.
- `thakur2014_eepa_adhesive_elastoplastic_dem` L38 · L65 · L90–97 (*'5 개 매개변수 · −k_adh·δⁿ'*) · L131 (*k_t = 2/7·k₁*) = 학술지 판의 꼴 — 학위논문은 Δγ 입력으로 f_min = (3/2)πΔγa 를 정하고 k_adh 를 유도 (식 4.16) · 끌어당김 가지 지수 X 를 n 과 따로 · 접선 강성 = 배수 κ_tm 변수 (p.81).  두 판을 같은 식으로 쓰면 안 된다 (틀렸다는 뜻은 아님).  같은 카드 L6 · L245 의 '소성 접촉면적과 함께 성장' 은 학위논문 본문 문장 (p.74 'surface area') 과 같으나 학위논문 식은 반지름 a 에 비례.
- `yano2026_se_psd_width_ionic_tortuosity_dem` L186 · L192: λp 정의는 학위논문의 C_p 와 같은 꼴 · 0.619 는 학위논문에 없다 (Yano 2024 의 값 — 맞게 적혀 있음).
- 원문 (학위논문) 자체의 인쇄 어긋남 19 개 = 이 카드 §3-9 (특히 표 5.14 'KPRS 1 %' = 부록 E.1 KPBO 1 % 숫자 · 부록 E.9 · E.10 = E.4 · E.5 복사 · 흐름도 그림 4.6 판정 기호 · 식 (4.13) γ ↔ λ · 식 (6.1) 은 n = 1 에서만 정확).
- 도구: 웹앱 그림 참조 정규식이 'Fig 4.4' 를 f4 로 읽어 이 카드의 장 번호 키 (f4_4 …) 에 자동 연결되지 않는다 (figures.json key_note).

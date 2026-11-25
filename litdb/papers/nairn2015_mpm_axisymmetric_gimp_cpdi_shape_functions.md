# 축대칭 GIMP — MPM 을 r–z 평면의 회전체 계산으로 다시 유도 (r 가중 형상 함수 S_ip · 기울기 G_ip + 새 함수 T_ip 로 후프 응력 · 후프 변형률 · 라디안당 질량 · 축 r = 0 에서 입자 영역 자르기) · uGIMP 와 CPDI 의 닫힌 꼴 · 확장 넷 (견인력 경계 · 명시 균열 · 다물질 접촉 법선 = 면적 기울기 · 열 전도 / 확산) · 시험 셋 (원판 균일 반지름 압축 J 16 % 정확해 · 원기둥 끝 견인 1000 MPa · 텅스텐 봉 1.70 km/s 관통 실험 대조) · 코드 변환 체크리스트 9 항 ★★ 3D 대조 · 계산 비용 · 구 · 누르기 · 탈압 · 접촉 계산 예 없음 — Neo-Hookean 가상 재료 (E 2300 MPa) · Johnson–Cook 금속 — Nairn, Guilkey (Int. J. Numer. Meth. Engng 2015)

> slug `nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions` · DOI `10.1002/nme.4792` · type `MPM (축대칭 GIMP 정식화 — 원통 부피 적분으로 형상 함수 S_ip · 기울기 G_ip (r 가중 · 식 6–7) + 후프 항 함수 T_ip (식 8) · 라디안당 질량 m_p = ρA_p⟨r_p⟩ · 후프 변형률 du_r/r_p · uGIMP 닫힌 꼴 (식 15–29 · 축 r = 0 에서 입자 영역을 자름) · CPDI 닫힌 꼴 (식 30–39 · 모서리가 축을 넘으면 평행사변형을 줄임) · 확장 = 견인력 경계 (식 40–53) · 명시 균열 (CRAMP · 점착대) · 다물질 접촉 (multimaterial contact) 법선 = 면적 기울기 (식 55) · 열 전도 · 확산 (식 56–62) · 시험 = 원판 균일 반지름 압축 Neo-Hookean (정확해 식 66–67) · 원기둥 끝 견인 · 텅스텐 봉 1.70 km/s 관통 (Johnson–Cook + Mie–Grüneisen · 남의 실험 대조) · 코드 변환 체크리스트 9 항 · 3D 계산 · 비용 · 하중 제거 없음)` · PDF `65b015d3-35._Axisymmetric_form_of_the_generalized_interpolation_material_point_method.pdf` (21 쪽 = 학술지 127–147 · 글자 층 온전 — 단 그리스 문자 · 빼기 · 적분 기호 · 꺾쇠 ⟨ ⟩ 는 글자 층에서 빠지거나 다른 글자로 나온다 → 식 · 기호는 렌더로 확인 · 보충 자료 없음) · digested `2026-11-12` · status ✅
>
> ⚠ **먼저 읽을 것** — ① 재료는 **이름 없는 Neo-Hookean 가상 재료** (E 2300 MPa · ν 0.33 · K 2254.9 · G 864.662 MPa · 시험 둘) 와 **텅스텐 합금 → 고경도 장갑강** (Johnson–Cook 흐름 + Mie–Grüneisen 압력 · 상수는 Anderson 외 [21] 의 값 그대로 · Table I) 이다 — **LPSCl · NCM 이 아니고 분말 · 입자 층 · 압밀도 아니다.  절대값 전이 0 건.**  가져오는 것은 **축대칭 MPM 의 식 (r 가중 형상 함수 · 후프 항 · 축 처리) · 확장마다 고칠 곳 · 시험 꼴 (정확해 있는 균일 압축 · 축 근처 입자의 J 균일성 · 견인 대 입자 힘) · 체크리스트 9 항 · 저자 한계**뿐이다.
> ② **축대칭 = 회전체 + 축대칭 하중인 3D 문제를 r–z 2D 로 푼다.**  이 논문에 **3D 계산 · 3D 와의 대조 · 계산 시간 · 메모리 수치가 없다.**  3D 에 대한 말은 셋뿐 — 견인력 (*"Further extension to 3D is straightforward by integrating over the six faces of the deformed particle domain."* p.137) · 축 바깥 노드의 거울 경계 (*"This last option is meant to mimic the value that node would have in a full three-dimensional simulation."* p.142) · 체크리스트의 *"store T_ip in the unused third component of a 3D gradient vector"* (p.145).  평면 2D 와의 대조는 **축 근처 입자의 J** 하나 (Fig. 6) 뿐이다.
> ③ **구 · 누르기 · 분말 · 탈압이 없다** — 'sphere' 0 회 · 'indent' 0 회 · 'unload' 0 회 · DEM 0 회 · 'granular' 는 참고문헌 제목 둘 ([4] · [5]) · 'plastic' 은 관통 예의 *"elastic-plastic"* 과 참고문헌 [6] 제목 둘 [카드 전문 검색].  **접촉은 정식화만** (§3.3 · 식 55 · 체크리스트 4) — 접촉 계산 예가 없다.  관통 예 (§4.3) 가 두 물체 계산인데 두 물체 사이를 어떻게 다뤘는지 (다물질 · 마찰 · 법선) 는 인쇄돼 있지 않다 [미확인].
> ④ 검증은 셋 — 원판 균일 반지름 압축 (정확해 식 66–67 · Fig. 5–7) · 원기둥 끝 견인 (지정 응력 1000 MPa 대조 · Fig. 8) · 텅스텐 봉 관통 (Anderson 외 [21] 의 flash x-ray 코 · 꼬리 위치 · Fig. 10).  **격자 수렴은 한 문장** (*"Simulations done at higher and lower resolutions (not shown) confirm that the results are convergent with grid refinement."* p.145) — 수치 · 오차 노름 · 수렴 차수 없음.
> ⑤ 그림 값은 화소가 아니라 **PDF 그리기 명령의 경로 좌표**에서 읽었다 (Fig. 2 · 3 · 5 · 6 · 7 · 8 · 10 은 벡터 · 축 = 틀 모서리와 눈금 · Fig. 9 만 래스터 920 × 809 px · 색 막대 없음 → 응력 값은 못 읽는다) — 원자료가 아니라 그림이므로 표지는 `[판독]`.  **판독 원자료** = `litdb/figures/nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions/digitized.csv` (113 행).
> ⑥ 인쇄 어긋남이 여럿 있다 (식 25 의 적분 아래 끝 · p.132 윗첨자 · 식 28 의 x_p · 식 31 의 Δr ↔ Δz · 식 54/55 의 부호 · 식 57 의 부호 · 식 66/67 의 G₁ · 식 A.2 의 조건 · Fig. 1 의 '−2' · 캡션의 'red' · Fig. 7 범위 ↔ 본문 84 % · 바닥글 연도) — §12 에 모았다.  식 그림은 **인쇄된 그대로** 잘랐다.
> ⑦ 표지: `인쇄` = 본문 · 캡션 · 표 · 그림 글자 · `[판독]` = 그림 경로 좌표에서 읽은 값 · `[카드 산술]` = 인쇄값 · 판독값에서 산술로만 (식 병기 · 식 확인은 scratchpad 의 수치 적분) · `[미확인]` = 논문에 없음 · `[카드 판독]` · `[카드 추론]` = 논문 밖 판단 · `[다른 카드]` = 정본의 다른 카드에 적힌 것 (slug 병기) · `[우리 기록]` = CLAUDE.md · 정본 카드에 적힌 우리 쪽 값.  쪽 = **학술지 쪽 (p.127–147) = PDF 쪽 + 126**.
>
> 짝 카드: `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` — GIMP 원전 = 이 논문 ref. [11] · 이 논문의 출발점 (*"we started from the cartesian formulation of GIMP [11]"* p.128) · 그 카드 §4-8 의 '셀당 1 · 폭 고정 GIMP = 2차 B-spline' 이 이 논문 식 (A.1) 에서도 선다 (§4-10).  `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` — CPDI 원전 = ref. [3] · 이 논문 §2.2 가 그 식을 축대칭으로 옮긴다.  `gritton2017_mpm_chemomechanical_coupling_silicon_anode` — 이 논문을 ref. [41] 로 · 열 확산 선례 [41–43] 로 인용 · 기둥을 축대칭 대신 3D 로 푼 카드 (고른 의도의 출처 · §0-1).  `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 이 논문 ref. [5] (다물질 마찰 접촉 · 접촉 법선) · `bardenhagen2000_mpm_granular_multibody_frictional_contact` — 같은 계열 다물체 접촉.  `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — 명시 균열 MPM (Nairn 계열) 을 견준 카드.  `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MLS-MPM 이산화의 원전.  `devaucorbeil2020_mpm_after_25_years_review` — MPM 리뷰 (NairnMPM 이름 · 이 논문은 코드 이름을 인쇄하지 않는다).  `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` — 입자 압밀 MPM 이지만 **평면 2D 원판** (축대칭 아님).

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

[DEM 우선 (수영)] 의 방향 메모 3.1 은 **2D 벤치마크를 먼저** (단계 2 · 3) 하고 3D 는 뒤로 미룬다 [우리 기록 · CLAUDE.md 11-09 · 11-10 줄 (*"2D 벤치마크로 한 속도장 ↔ 입자별 장을 먼저 가름"* · GPU 없이 단계 0–3)].  그 2D 벤치마크 가운데 단위 시험 U1 (입자 하나를 두 판 사이에 누름 · 지름당 셀 수) 과 U3 (단단한 구를 소성 블록에 눌렀다 뗌) 은 **하중 축이 대칭축인 문제**다 — 평면 변형 2D 로 풀면 '원판 · 원기둥 홈' 을 푸는 셈이고, 축대칭 r–z 로 풀면 같은 2D 비용으로 **구 · 구–블록 그 자체** (3D 회전체) 를 푼다 [카드 추론].  이 논문은 그 축대칭 MPM 을 **GIMP 위에서 처음 유도한 원전**이다.  읽을 까닭이 넷이다.

**(1) 축대칭 GIMP 의 형상 함수 · 기울기 · 후프 항을 식 번호마다 다 준다.**

> *"The main differences between planar GIMP [11] and axisymmetric GIMP are the σ^(s)_θθ,p term in f_i^(int), particle masses are per radian (m_p = ρA_p⟨r_p⟩) and vary with position, and the incremental deformation gradient has du_r/r_p for hoop direction strain.  Furthermore, the r in the integrands causes S_ip and G_ip to differ from the corresponding planar GIMP functions, and axisymmetry requires a new GIMP shape function denoted here as T_ip."* (p.129–130 · `txt_p3_p4_classic_recovered_main_differences.png`)

> *"In “classic” MPM, it turned out that axisymmetric MPM could re-use the planar shape functions, but when axisymmetric MPM is extended to GIMP, new shape functions are required and those shape function are not available in the literature."* (p.130 · 같은 크롭)

**(2) 축 r = 0 의 처리가 결과를 가른다는 숫자가 있다** — 평면 형상 함수를 그대로 쓰면 축에서 첫 입자의 상대 부피 J 가 **23.33 %** (목표 16 %) · 축대칭 형상 함수를 자르지 않으면 uGIMP **6.52 %** · CPDI **20.12 %** ↔ 자르면 **16.31 · 16.48 %** [판독 · Fig. 5 · 6].

> *"Thus, simply using planar shape function instead of the axisymmetric shape function derived here in axisymmetric problems can cause large errors at the origin (see “uGIMP (planar, No Extra Node BC)” curve in Figure 6)."* (p.142 · `txt_p16_planar_shape_functions_extra_nodes_mirror.png`)

U1 · U3 에서 하중이 걸리는 자리 (구 꼭대기 · 누르는 꼭지) 가 바로 축 위다 [카드 추론].

**(3) 코드를 축대칭으로 바꿀 때 고칠 곳의 체크리스트 9 항** (p.145 · `txt_p19_conclusion_checklist.png`) — 질량 · 축 경계 · 형상 함수 · 접촉 법선 · 후프 변형률 · 구성식 · 견인 · 내부력 후프 항 · 축 넘김 정지.  우리 2D MLS-MPM 에 축대칭 판을 둔다면 '무엇이 필요한가' 의 목록이 된다 (구현 판단은 하지 않는다 · §10).

**(4) 축대칭으로 옮길 때 확장마다 바뀌는 곳** — 접촉 법선은 부피 기울기로 구하면 틀리고 (V_p 가 r 에 달림) **면적 기울기**로 · 축 노드의 법선 r 성분 = 0 · 접촉 판정의 노드 면적은 축에서 두 배 (p.139) · 견인력은 두께 B 대신 반지름 가중 (p.137) · 입자 힘은 라디안당 + r 의존 (p.138) · 열 · 확산은 형상 함수와 라디안당 양만 바꾼다 (p.140).

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| U1 · U3 를 2D 비용으로 3D 문제처럼 (단계 2 · 3) | 축대칭 GIMP (uGIMP · CPDI) 정식화 전부 (식 1–39) + 체크리스트 9 항.  **U1 · U3 같은 예제 · 3D 대조 · 비용은 없음** |
| 축 근처에서 믿을 만한가 | 축 근처 입자 J 시험 (Fig. 5 · 6) — 자름 / 안 자름 · 평면 형상 함수 + 경계 처리 셋.  자른 축대칭 형상 함수가 J 를 고르게 (16.31–16.78 % · 평균선 16.41 % [판독]) |
| 큰 변형에서 언제 깨지나 | 압축 84 % 까지 그림 · uGIMP 88 % 에서 붕괴 · CPDI 약 93 % 에서 붕괴 시작 (p.143 · 인쇄) · uGIMP 인장 약 50 % 한계 (p.134 · p.144) |
| 판 · 하중 경계를 어떻게 거나 | 견인 (변 적분 · CPDI) 이면 입자 응력 991.8–1004.1 MPa (지정 1000) ↔ 입자 힘이면 가장자리 574.5 · 안쪽 1149.5–1203.1 MPa [판독 · Fig. 8] |
| 접촉 · 다물체 (후보 A′ · A′-0) 를 축대칭으로 | 면적 기울기 법선 (식 55) · 축 성분 0 · 노드 면적 두 배 (§3.3) — **정식화만 · 계산 예 없음** |
| 정확해 단위 시험 | 균일 반지름 압축 (z 구속) Neo-Hookean 정확해 (식 63–67) — J 16 % 에서 σ_rr = σ_θθ −12.0 GPa · σ_zz +3.40 GPa [카드 산술] |
| 탈압 · 되돌아옴 · 잔류 압흔 · 분말 · LPSCl | **없음** |

### 0-1. ★ 고른 의도 대조 (후보 표 N-35 의 '왜' 칸)

의도 원문: *"g · f — 축대칭 MPM: 2D 벤치마크 (입자 하나 압축 U1 · 구–블록 누르기 U3) 를 3D 와 같은 문제로 푸는 길 (카드 §9 ⑩ · §10 행동 4) · gritton2017 은 축대칭으로 줄일 수 있는 문제를 3D 로 풀고 2D 와 견주지 않음"* (가리킨 카드 = `gritton2017_mpm_chemomechanical_coupling_silicon_anode` · §9 ⑩ · §10 행동 4 · 정본 L597 · L624 · L58)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "g" — 2D 결과를 3D 로 옮길 때의 경고나 증거 | **일부** | **경고 = 채움 (평면 → 축대칭)**: 평면 형상 함수를 축대칭 계산에 쓰면 축 근처에서 큰 오차 — 첫 입자 J 23.33 % ↔ 목표 16 % · 축대칭 자름 16.31 % [판독 · Fig. 6 · p.142] · 경계 처리로 줄어듦 (축 바깥 노드 BC 0 → 17.48 % · 거울 → 16.02 % [판독]) · 평면 ↔ 축대칭 형상 함수의 차이는 축 근처에 몰림 (Fig. 2 · 3 · p.131 · p.133) · 견인 두께 B ↔ 반지름 (p.137) · 입자 힘 라디안당 (p.138) · 부피 기울기 법선 실패 (p.139).  조건: 원판 균일 반지름 압축 · z 구속 · Neo-Hookean · J 16 %.  **증거 = 없음 (평면 2D ↔ 3D)**: 같은 문제를 3D 로 풀어 견준 값 · 계산 비용 없음 |
| "f" — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정 | **일부** | **접촉 = 정식화만**: 다물질 모드 (물질마다 속도장) 에서 축대칭으로 바꿀 곳은 법선뿐 (*"Most planar 2D contact tasks can be applied directly to axisymmetric MPM.  The only exception is determination of the normal vector"* p.138) → 면적 기울기 (식 55) · 축 노드 r 성분 0 · 노드 면적 두 배 (p.139) · 계산 예 0.  **강체**: 원판 압축을 *"rigid particles"* 로 일정 속도 (p.141) — 강체 결합 식은 없음.  **해상도**: 셀 2.5 × 2.5 · 2 × 2 · 0.25 × 0.25 mm · 셀당 입자 = 관통 *"four particles/cell"* (p.145 인쇄) · 압축 · 견인은 방향당 2 [판독 — 입자 위치 간격 = 셀 절반].  **오차**: 정확해 · 지정 응력 · 실험 대조 · 수렴은 *"not shown"* — 노름 · 차수 없음 |
| "축대칭 MPM" | **채움** | §2 (식 1–14 · p.128–130) · §2.1 uGIMP (식 15–29 · p.130–133) · §2.2 CPDI (식 30–39 · p.134–136) · §3 확장 넷 (p.136–140) · §5 체크리스트 9 항 (p.145) |
| "2D 벤치마크 … 를 3D 와 같은 문제로 푸는 길" | **채움 (방법) · 없음 (대조)** | 방법: 원통 부피 적분으로 회전체를 r–z 단면에서 푼다 (*"The key changes were to replace volume integration by cylindrical volume integration and to account for cylindrical coordinates in gradient evaluations"* p.128) · 질량 · 힘 · 부피는 라디안당.  원문은 같은 문제를 3D 로 풀어 견주지 않고 비용도 적지 않는다 — '같은 문제' 는 기하 · 하중 · 경계 · 접촉이 다 축대칭일 때만 [카드 추론] |
| "입자 하나 압축 U1" | **없음 (예제) · 일부 (닮은 시험)** | 구 · 입자 압축 예제 없음 ('sphere' 0 회).  닮은 것: 원판 (R₀ 50 mm · 두께 10 mm · 셀 2.5 mm) 의 균일 반지름 압축 J 16 % — 축 근처 입자 J (Fig. 5 · 6) · 평균 응력 ↔ 정확해 (Fig. 7).  U1 의 '지름당 셀 수' 규칙 없음 (원판 반지름 = 셀 20 · 두께 = 셀 4 [카드 산술]) |
| "구–블록 누르기 U3" | **없음 (예제) · 일부 (닮은 문제)** | 텅스텐 봉 (∅ 0.4 cm · 길이 5.0 cm · 뭉툭한 코) 이 강 원기둥 (∅ 4.0 cm · 4.95 cm) 에 1.70 km/s 로 들어가는 관통 (§4.3 · p.144–145) — 축 위 물체가 소성 표적에 들어가는 축대칭 문제지만 **동적 · 둘 다 변형 (Johnson–Cook) · 준정적 누르기 · 떼기 · 잔류 압흔 · 되돌아옴 없음** · 두 물체 사이 처리 [미확인] · 결과 = 코 · 꼬리 위치뿐 (Fig. 10) |
| "(카드 §9 ⑩ · §10 행동 4)" · "gritton2017 은 … 3D 로 풀고 2D 와 견주지 않음" | **원문 밖 (가리킨 카드에서 확인)** | gritton 의 문장 (*"while the pillar geometry lends itself to a 2D axisymmetric numerical solution for the purposes of this paper full 3D simulations will be performed"*) 은 gritton 카드 L58 이 옮긴 것 — 이 논문은 2015 (gritton 2017 보다 앞) 라 gritton 을 말하지 않는다.  이 논문도 3D 와 견주지 않는다 |

**가리킨 카드 · 같은 저자를 언급한 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 정독 출력의 카드 문제 절에):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `gritton2017_…` L58 (§0-2 (iii)) | gritton 원문 *"lends itself to a 2D axisymmetric numerical solution … full 3D simulations will be performed"* · *"축대칭 해와의 대조는 없다"* | (gritton 원문 — 이 논문과 무관) | **같음** (gritton 쪽 사실 · 이 논문으로 대조할 것 아님) |
| `gritton2017_…` L254 (§4-2 출처) | *"This method of modeling concentration diffusion within MPM is similar to methods used previously in modeling heat diffusion [41–43]"* — [41] = 이 논문 (후보 표 N-35) | §3.4 (p.139–140 · 식 56–62) 축대칭 GIMP 열 전도 + 확산 치환 (k → D · T → μ · *"An axisymmetric GIMP analysis for diffusion is recovered by replacing k with the diffusion tensor"*) — **계산 예는 없다** | **같음 (내용 수준)** — '열 확산 선례' 로서 알고리즘은 있고 결과는 없다 |
| `gritton2017_…` L597 (§9 ⑩) | *"평면 변형 대신 축대칭 MPM (이 논문 ref. [41]) 을 쓰면 2D 값을 3D 로 옮기는 문제의 일부가 사라진다 [카드 추론]"* | 축대칭 정식화 (§2) · 단 축 처리 (자름 · 축 노드 · r 속도 0) 가 필요하고 (p.131 · 체크리스트 2–3) 입자가 r = 0 을 넘으면 계산을 멈춘다 (체크리스트 9).  3D 대조 · U1 · U3 같은 예제 없음 | **같음 (방법 수준) · 한정어 필요** — '사라진다' 는 기하 · 하중 · 경계 · 접촉이 모두 축대칭일 때만 · 축 근처 처리를 잘못하면 오히려 축 근처 오차가 생긴다 (Fig. 6) |
| `gritton2017_…` L624 (§10 행동 4) | *"축대칭이면 구 하나 · 구–블록 문제가 그대로 3D 문제다"* | 원문은 구 · 구–블록을 다루지 않는다 · 회전체 r–z 단면 계산 (라디안당) | **같음 (원리) · 한정어 필요** — 구는 r–z 반원 단면 · 축 위 입자 영역 자름 (식 20–21 · 25–26 · 28–29) · 접촉 법선 수정 (식 55) 이 따라와야 '그대로' 가 된다 [카드 추론] |
| 후보 표 N-35 서지 (b40) | *"Nairn J A and Guilkey J E 2015 Axisymmetric form of the generalized interpolation material point method Int. J. Numer. Methods Eng. 101 127–47"* | 첫 쪽 머리글 *"Int. J. Numer. Meth. Engng 2015; 101:127–147"* · *"Published online 1 October 2014"* · DOI 10.1002/nme.4792 · 쪽마다 바닥글 *"Int. J. Numer. Meth. Engng 2014; 101:127–147"* | **같음** (권 · 쪽 · 연도) — 원문 안에서 연도 표기가 둘 (머리 2015 ↔ 바닥글 2014 · §12) |
| `devaucorbeil2020_…` L46 · L56 · L61 | *"Nairn(2018)이 임의 마찰법칙"* · *"wood Nairn"* · *"NairnMPM"* | 다른 Nairn 문헌 · 코드 이름 — 이 논문은 코드 이름을 인쇄하지 않는다 ('NairnMPM' 0 회 [카드 전문 검색]) | **이 논문을 가리키지 않음** |
| `homel2017_…` L267 · L458 · L617 | 명시 균열 MPM (Nairn · ref 34 · 35 · 69) | 이 논문 §3.2 의 CRAMP = ref. [9] (Nairn 2003) · J 적분 [7, 8] (Guo · Nairn) — 그 카드의 ref 번호 서지는 그 카드에 [미확인] | **이 논문을 가리키지 않음** (같은 균열 계열일 수 있으나 서지 대조 불가) |

⇒ **의도 대조 결과: 채움 (축대칭 MPM 정식화 · 축 r = 0 처리 · 확장마다 고칠 곳 · 체크리스트) / 일부 (g = 평면 → 축대칭 경고만 · f = 접촉 정식화 + 해상도 기록만 · U1 · U3 와 닮은 시험) / 없음 (3D 대조 · 계산 비용 · 구 · 준정적 누르기 · 떼기 · 탈압 · 접촉 계산 예)**.

### 0-2. 이 묶음의 네 질문 (DEM 한계 · 소성 · 2D/3D · 탈압)

| 질문 | 이 논문의 답 (원문 위치) |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | **말 없음** — DEM · 'discrete' 0 회 · 'granular' 는 참고문헌 제목 둘 [카드 전문 검색].  한계를 적은 대상은 **옛 MPM** 이다: *"It has long been recognized that this original MPM (i.e., particles represented spatially as Dirac delta functions) has serious element crossing artifacts and should not be used."* (p.127 · `txt_p1_p2_only_axisym_mpm_dirac_artifacts.png`) · 원판 압축에서 *"No results for classic axisymmetric MPM shape functions are given, because they became unstable as many particles crossed element boundaries."* (p.141) |
| (ii) 입자의 소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용 | 어려움 = **변형한 입자 영역 위의 적분** — *"Although uGIMP explicitly evaluates S_ip, G_ip, and T_ip, it will lose accuracy as the actual particle domain deforms.  For example, large-deformation tension tests are limited to about 50% strain when using uGIMP.  The solution is to evaluate the integrals over the deformed particle domain.  Although this task is easy in 1D [11], it is very difficult in 2D or 3D."* (p.134 · `txt_p8_ugimp_50pct_strain_cpdi_deformed_domain.png`).  우회 = **CPDI** (N_i 를 평행사변형 네 모서리 값의 보간으로 바꿔 닫힌 꼴 · 식 30–39) · 축에서 영역이 r = 0 을 넘으면 자름 (uGIMP) · 줄임 (CPDI).  한계 = 압축 uGIMP 88 % · CPDI 약 93 % 에서 붕괴 (p.143) · 인장 50 % 에서 uGIMP 불안정 (p.144).  소성 계산은 관통 하나 (Johnson–Cook · 상수 = Anderson 외 [21] 의 값 · **맞춘 값 0**).  **계산 비용 미인쇄** |
| (iii) 2D 인가 3D 인가 · 2D → 3D 전이 | **축대칭 (r–z 2D 계산 = 3D 회전체)**.  3D 계산 · 대조 없음 (② 의 세 문장뿐).  요약: *"Finally, a check list for software development describes all tasks needed to convert 2D planar or 3D codes to include an option for axisymmetric MPM."* (p.127).  평면 ↔ 축대칭 차이: 형상 함수 (축 근처) · 후프 항 · 라디안당 질량 · 견인 · 입자 힘 · 접촉 법선 · 열 유속 (§2–§3) |
| (iv) 압력을 뺄 때의 거동 | **다루지 않는다** — 'unload' 0 회 · 원판은 끝까지 압축 · 견인은 선형 증가 · 관통은 한 번의 충돌 (100 µs) |

---

## 1. 한 줄 요약

**KR:** 물질점 방법 (MPM) 의 일반화 판인 GIMP 를 원통 좌표로 다시 유도해, 회전체 + 축대칭 하중 문제를 r–z 단면 하나로 푸는 축대칭 MPM 을 만든다.  부피 적분이 원통 부피 적분이 되면서 형상 함수와 기울기에 반지름 r 이 가중으로 들어가고 (S_ip · G_ip · 식 6–7), 후프 응력 · 후프 변형률을 위한 새 함수 T_ip (r 가중 없음 · 식 8) 가 생기며, 입자 질량은 라디안당 m_p = ρA_p⟨r_p⟩ 가 된다.  옛 축대칭 MPM (Sulsky–Schreyer 1996 · 점 질량) 은 평면 형상 함수를 그대로 쓸 수 있었지만 GIMP 에서는 새 함수가 필요하다.  영역을 고정하는 uGIMP 에서는 반지름 몫 S_r 의 닫힌 꼴 (평면 uGIMP + 1/(2n_i + ξ_p) 항 · 식 19 · 24 · 27) 을, 영역을 변형 경사로 평행사변형으로 실어 나르는 CPDI 에서는 모서리 넷 보간의 닫힌 꼴 (식 35 · 37 · 39) 을 낸다.  입자 영역이 축 r = 0 을 넘으면 형상 함수가 특이해지므로 uGIMP 는 영역을 r = 0 에서 자르고 (축 노드 · 첫 노드만 특수 꼴 · 식 20–21 · 25–26 · 28–29), CPDI 는 평행사변형을 줄인다.  확장 넷 — 견인력 경계 (변형한 변 위의 선적분 · 식 40–48 · 평면 판 식 49–53) · 명시 균열 (기하라 그대로 · 점착력은 라디안당 · 축대칭 J 적분은 미개발) · 다물질 접촉 (법선 = r–z 면적 기울기 · 축 노드 r 성분 0 · 노드 면적 두 배) · 열 전도 / 확산 (형상 함수와 라디안당 양만 바꿈 · 입자 온도는 노드 비율로 갱신) — 을 점검한다.  시험: Neo-Hookean 원판을 z 를 막고 반지름 방향으로 J 16 % 까지 누르면 자른 축대칭 형상 함수만 축 근처 입자의 J 를 고르게 내고 (자르지 않은 uGIMP 첫 입자 6.5 % · 평면 형상 함수 23.3 % [판독]), 평균 응력은 정확해와 겹치며 (84 % 압축까지 그림 · uGIMP 88 % · CPDI 약 93 % 에서 붕괴), 원기둥 끝 견인 1000 MPa 에서 견인 경계는 입자 응력을 지정값에 묶고 입자 힘은 가장자리를 낮게 · 안쪽을 높게 (+15–20 % [판독]) 내며, 텅스텐 봉 1.70 km/s 관통의 코 · 꼬리 위치는 남의 실험과 맞는다.  결론은 축대칭 MPM 으로 바꾸는 코드 체크리스트 9 항.

**EN:** Nairn and Guilkey re-derive GIMP in cylindrical coordinates so that bodies of revolution under axisymmetric loading are solved on a single r–z section.  Cylindrical volume integration puts the radius into the shape-function and gradient weights (S_ip, G_ip), adds a new function T_ip for hoop stress and hoop strain, and makes particle mass per radian (m_p = ρA_p⟨r_p⟩).  Unlike classic point-mass axisymmetric MPM, which could reuse planar shape functions, GIMP needs new ones: closed forms are given for uniform GIMP (planar uGIMP plus terms in 1/(2n_i + ξ_p)) and for CPDI (corner interpolation over the convected parallelogram).  Particle domains crossing r = 0 make shape functions singular, so uGIMP domains are truncated at r = 0 (special forms for the axis node and the first node only) and CPDI parallelograms are shrunk to touch the axis.  Extensions are re-examined: traction boundary conditions as edge line integrals (with the previously unpublished planar forms), explicit cracks (unchanged except per-radian cohesive forces; axisymmetric J integral still undeveloped), multimaterial contact (normals from the r–z area gradient, zero radial component on the axis, doubled nodal area), and conduction/diffusion (per-radian quantities, rate-based particle update).  In uniform radial compression of a Neo-Hookean disk to J = 16 %, only truncated axisymmetric shape functions keep J uniform near the axis; mean stresses match the exact solution up to 84 % compression (uGIMP fails at 88 %, CPDI begins to fail near 93 %).  End tractions keep particle stresses at the 1000 MPa target while particle forces give low edge and drifting interior stresses; a 1.70 km/s tungsten-rod penetration matches flash x-ray nose/tail data.  A nine-item conversion checklist closes the paper.  No 3D comparison, cost data, contact example, spheres, indentation or unloading.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **Axisymmetric form of the generalized interpolation material point method** |
| 저자 | **John A. Nairn** (¹ · 교신) · **James E. Guilkey** (²) |
| 소속 (인쇄 그대로) | ¹ Wood Science and Engineering, Oregon State University, Corvallis, OR, USA · ² Schlumberger Technology Corporation, Rasharon, TX, USA |
| 저널 | **International Journal for Numerical Methods in Engineering 101, 127–147 (2015)** — 첫 쪽 머리글 *"Int. J. Numer. Meth. Engng 2015; 101:127–147"* · *"Published online 1 October 2014 in Wiley Online Library"* · *"Copyright © 2014 John Wiley & Sons, Ltd."* · 쪽마다 바닥글 *"Int. J. Numer. Meth. Engng 2014; 101:127–147"* (연도 표기 둘 · §12) · 호 = 2 [카드 판독 — 내려받기 표지 *"10970207, 2015, 2"*] |
| DOI | **10.1002/nme.4792** (첫 쪽 인쇄) |
| 접수 · 게재 | Received 10 January 2013 · Revised 20 December 2013 · Accepted 18 August 2014 (첫 쪽 인쇄) |
| 키워드 (인쇄) | material point method; axisymmetry; penetration; MPM; GIMP; CPDI |
| 분량 | 21 쪽 (p.127–147 · **PDF 쪽 = 학술지 쪽 − 126**) · Fig. 1–10 · Table I · 번호 식 (1)–(67) + (A.1) · (A.2) · 참고문헌 21 건 · 보충 자료 없음 |
| 절 구성 | 1 Introduction (p.127–128) · 2 Generalized material point method (p.128–136: 2.1 Uniform GIMP p.130–133 · 2.2 Convected particle domain integration p.134–136) · 3 Generalized material point method extensions (p.136–140: 3.1 Traction boundary conditions · 3.2 Explicit cracks · 3.3 Multimaterial contact calculations and imperfect interfaces · 3.4 Conduction and diffusion) · 4 Examples (p.140–145: 4.1 Uniform radial compression · 4.2 Traction boundary conditions · 4.3 Impact penetration example) · 5 Conclusion (p.145 · 체크리스트) · Appendix A (p.146) · Acknowledgments · References (p.146–147) |
| 연구 유형 | 수치 방법 (정식화 + 코드 시험) + 남의 실험 대조 1 건 (Anderson 외 1995 · flash x-ray) |
| 자금 (인쇄) | Nairn: Office of Naval Research SBIR (Wasatch Molecular, Inc. 하도급 · contract N00014-13-M-0018) · National Science Foundation (award 1161305) |
| 코드 | 이름 · 언어 · 병렬 미인쇄 [미확인] ('NairnMPM' · 'Uintah' 0 회) — 서론은 MPM 이 Sandia 의 CTH 에 구현됐다는 사실만 ([10]) |
| PDF 상태 | Wiley 조판 · 글자 층 온전 (빼기 · 그리스 문자 · 적분 · 꺾쇠가 빠짐 → 렌더로 확인 · 식 크롭 69 장) · 그림: Fig. 1–8 · 10 벡터 · Fig. 9 래스터 (920 × 809 px) · 쪽마다 오른쪽 여백에 내려받기 표지 (크롭에서 뺌) |

**자기 위치 (저자 원문)**
> *"Sulsky and Schreyer presented the first, and thus far, only, formulation for axisymmetric MPM [12].  Unfortunately, this prior axisymmetric MPM was based on early MPM methods that treated particles as point masses.  It has long been recognized that this original MPM (i.e., particles represented spatially as Dirac delta functions) has serious element crossing artifacts and should not be used.  They have been replaced by GIMP methods [11], which have been developed for cartesian coordinates but are not available for axisymmetric calculations.  In addition to reformulation of axisymmetry using GIMP methods, numerous other extensions to MPM have developed since the original work on axisymmetric MPM [12].  Because none of these extensions considered axisymmetry, each one needs to be re-examined for use in axisymmetric code."* (p.127–128 · `txt_p1_p2_only_axisym_mpm_dirac_artifacts.png`)

---

## 3. 핵심 수치

> **표지** · `인쇄` = 본문 · 캡션 · 표 · 그림 글자 · `[판독]` = 그림 경로 좌표 (`digitized.csv`) · `[카드 산술]` = 산술 · 수치 적분으로만 · `[미확인]` = 논문에 없음.  판독값은 추세 · 자릿수 확인용이다 — 논문이 인쇄한 값처럼 쓰지 않는다.  ⚠ 재료값은 Neo-Hookean 가상 재료와 금속의 값이다 — **우리 재료 값으로 쓰지 않는다.**

### 3-1. 정식화가 정하는 수 · 규칙 (§2 · 식 1–39)

| 무엇 | 값 · 규칙 | 위치 | 표지 |
|---|---|---|---|
| 무차원 좌표 | ξ = 2(r − r_i)/Δr · η = 2(z − z_i)/Δz → 노드 i 가 (0, 0) · 셀 = 2 × 2 · n_i = r_i/Δr · 입자 영역 폭 = 2l_p (무차원) = l_pΔr (실제) | 식 15 · p.130 | 인쇄 · 폭 환산 [카드 산술] |
| uGIMP S_r 의 지지 | ±(2 + l_p) (무차원) = 노드 양쪽 (1 + l_p/2) 셀 · *"it extends to the second neighbor grid cells"* | Fig. 1 캡션 · p.131 | 인쇄 |
| 평면 극한 | n_i → ∞ 에서 S_r → 평면 uGIMP · 카드 수치: 차 2.1 × 10⁻⁴ (n = 100) · 2.1 × 10⁻⁵ (n = 1000) · l_p = 1/2 | p.131 | 인쇄 · [카드 산술] |
| 축에서 자르는 조건 | n_i < 1 + l_p/2 이고 r_p < l_pΔr/2 (ξ_p < −2n_i + l_p) 일 때만 · 그런 노드가 있으면 격자는 r = 0 에 노드를 둔다 → n_i 는 정수 → 특수 꼴은 n_i = −1 · 0 · 1 뿐 | p.131 | 인쇄 |
| 자른 S_r | S_r^(−1) = 0 · S_r^(0) = (3 − l_p − ξ_p)/3 (0 ≤ ξ_p < l_p) · S_r^(1) = (2 + l_p + ξ_p)/3 (−2 ≤ ξ_p < −2 + l_p) · 정의 적분과 차 4.2 × 10⁻¹² | 식 20–21 · p.131 | 인쇄 · 확인 [카드 산술] |
| 축 위 입자 (r_p → 0) | S_r(n = 0) → 5/6 · S_r(n = 1) → 1/6 (l_p = 1/2) · 2/3 · 1/3 (l_p = 1) | 식 20–21 | [카드 산술] |
| 자르지 않은 S_r 의 특이 | ξ_p = −2n_i 에서 특이 · 예: 2r_p/Δr = 0.05 에서 S_r(n = −1, 0, 1) = −0.304 · 0.749 · 0.555 (합은 1 · l_p = 1/2) — *"the singularities cancel to retain partition of unity"* | p.131 · 식 17 | 인쇄 · 값 [카드 산술] |
| 자른 dS_r | dS_r^(−1) = 0 (인쇄 윗첨자 '(0)' · §12) · dS_r^(0) = −1/2 · dS_r^(1) = +1/2 — *"extends dS_r(ξ_p, 0) and dS_r(ξ_p, 1) to the origin at constant ±1/2"* | 식 25–26 · p.132–133 | 인쇄 |
| T_ip (uGIMP) | 평면 uGIMP 형상 함수 ÷ r_p (식 27) · 자른 꼴 T^(0) = (1/Δr)(4/(l_p + ξ_p) − 1)S_z(η_p) → ξ_p → 0 에서 (1/Δr)(4/l_p − 1) = 7/Δr (l_p = 1/2) · T^(1) = S_z(η_p)/Δr — 자르면 1/r_p 특이가 사라진다 | 식 27–29 | 인쇄 · 극한 [카드 산술] |
| CPDI 영역 | 평행사변형 반 벡터 d_1 · d_2 (식 31) · \|J\| = d_1r d_2z − d_2r d_1z = A_p/4 · r_p → ∞ 에서 평면 CPDI | 식 31–35 · p.134–135 | 인쇄 |
| CPDI 축 넘김 | r_p − \|d_1r + d_2r\| < 0 이면 모서리 하나가 r < 0 → s = r_p/\|d_1r + d_2r\| 로 d_1 · d_2 를 줄여 원점에 닿게 · *"(and they do in some sample calculations)"* | p.135–136 | 인쇄 |
| dF 갱신 | dF = exp(Δt∇v) = I + ∇u + Σ_{k≥2}(∇u)^k/k! · 충분한 해상도면 처음 두 항 · 회전 (관통) 이면 k ≥ 2 필요 · 축대칭은 Cayley–Hamilton 으로 행렬 곱 없이 | 식 9 · p.129 | 인쇄 |
| 질량 | m_p = ρA_p⟨r_p⟩ (라디안당 · 위치에 따라 변함) · 체크리스트 (1) 은 ρA_p r_p | p.129 · p.145 | 인쇄 |

### 3-2. 균일 반지름 압축 (§4.1 · 식 63–67 · Fig. 5–7 · `txt_p15_radial_compression_setup_classic_unstable.png`)

| 설정 | 값 | 표지 |
|---|---|---|
| 원판 | 반지름 R₀ 50 mm · 두께 10 mm · z 구속 → F = diag(1 + ε_rr, 1, 1 + ε_rr) (식 63) · ε_rr = −ΔR/R₀ | 인쇄 |
| 격자 | 2.5 × 2.5 mm (반지름 = 셀 20 · 두께 = 셀 4 [카드 산술]) | 인쇄 |
| 입자 | 첫 입자 0.625 mm · 간격 1.25 mm = 셀 절반 (방향당 2) → 원판을 다 채웠다면 40 × 8 = 320 개 | [판독] · [카드 산술 — 채움 가정] |
| 재료 | Neo-Hookean (식 64–65) · E 2300 MPa · ν 0.33 · K 2254.9 · G 864.662 MPa (= E/(3(1 − 2ν)) · E/(2(1 + ν)) [카드 산술]) | 인쇄 |
| 하중 | *"compressed slowly (compared to wave speed of the material) until ε_rr = −0.6 resulting in final relative volume of J = 16%"* · *"Compression was done at fixed velocity using rigid particles."* — 속도 값 · Δt · 걸음 수 미인쇄 | 인쇄 · [미확인] |
| 비교 | 형상 함수 다섯 — uGIMP · CPDI × (자름 · 안 자름) + classic | 인쇄 |
| classic | *"became unstable as many particles crossed element boundaries"* — 결과 그림 없음 | 인쇄 |

**Fig. 5 — 축 근처 입자의 J (%) [판독 · 처음 위치별]** (가는 가로선 = 평균 J = **16.41 %** [판독] · 목표 16 %)

| 처음 위치 (mm) | 0.625 | 1.875 | 3.125 | 4.375 | 5.625 | 6.875 |
|---|---|---|---|---|---|---|
| uGIMP (자름) | 16.31 | 16.31 | 16.33 | 16.36 | 16.78 | 16.67 |
| CPDI (자름) | 16.48 | 16.48 | 16.42 | 16.34 | 16.50 | 16.61 |
| uGIMP (안 자름) | **6.52** | 20.45 | 20.33 | 18.63 | 14.77 | 14.77 |
| CPDI (안 자름) | **20.12** | 16.58 | 16.52 | 16.41 | 16.49 | 16.56 |

- 저자: *"The only axisymmetric shape functions to correctly give J constant for all particles (the thin line is the mean J) are the truncated uGIMP and CPDI shape functions.  If uGIMP shape functions are not truncated, the results are poor.  Because CPDI approximately tracks deformed particle domain, the effects of truncation are smaller.  Nevertheless, CPDI without truncation loses accuracy for the particle closest to the origin."* (p.141)
- 안 자른 uGIMP 의 오차는 첫 입자만이 아니다 — 1.9–4.4 mm (첫 · 둘째 셀) 에서 +2.6–4.4 %p · 셋째 셀 (5.6 · 6.9 mm) 에서 −1.2 %p [판독 · 카드 산술 (16 % 기준)].

**Fig. 6 — 평면 형상 함수 + 축 처리 셋 (축 노드는 모두 r 속도 0 · 축 바깥 'extra node' 처리만 다름) · J (%) [판독]**

| 처음 위치 (mm) | 0.625 | 1.875 | 3.125 | 4.375 | 5.625 | 6.875 |
|---|---|---|---|---|---|---|
| uGIMP (자름 · 축대칭) | 16.31 | 16.31 | 16.32 | 16.35 | 16.57 | 16.53 |
| 평면 · extra node 처리 없음 | **23.33** | 15.63 | 15.96 | 16.07 | 16.20 | 16.12 |
| 평면 · extra node BC 0 | **17.48** | 16.00 | 15.98 | 16.02 | 16.20 | 16.13 |
| 평면 · extra node 거울 | 16.02 | 16.02 | 15.99 | 16.01 | 16.20 | 16.13 |

- 저자: *"What we observe is that in the last option, which tends to keep the particle pushed farther away from r = 0, the use of planar shape functions gave an acceptable result with constant level of compression.  Note that because the axisymmetric formulation presented here truncates the GIMP domains at r = 0, the extra nodes do not participate in the calculation; therefore, the way boundary conditions are treated on those nodes is inconsequential; the results are always correct."* (p.142)
- 카드 관찰 (판정 아님): 거울 판의 처음 네 입자 (16.0 %) 가 축대칭 자름 판 (16.3 %) 보다 공칭 16 % 에 가깝다 [판독] — 원문은 '고른가' 만 판정한다.  또 같은 이름 'uGIMP (truncated)' 의 5 · 6 번째 입자가 Fig. 5 (16.78 · 16.67) 와 Fig. 6 (16.57 · 16.53) 에서 다르다 [판독 · 처음 넷은 차 ≤ 0.013] — 같은 런인지 [미확인] (§12).

**Fig. 7 · 붕괴 (p.142–143 · `txt_p16_p17_fig7_84_88_93pct_four_reasons.png`)**

| 무엇 | 값 | 표지 |
|---|---|---|
| 그림 범위 (본문) | *"plotted up to 84% compression"* (= J 16 %) | 인쇄 |
| 그림 범위 (선) | 실선이 V/V0 ≈ 9.3 % (≈ 90.7 % 압축) 까지 · 끝 응력 σ_rr = σ_θθ ≈ −25.5 GPa · σ_zz ≈ +15.2 GPa | [판독] |
| 정확해 (식 66–67) | J 16 %: σ_rr = σ_θθ = −12.0 GPa · σ_zz = +3.40 GPa / J 12 %: −17.9 · +8.1 GPa / J 9.3 %: −25.7 · +15.4 GPa / J 7 %: −38.6 · +29.1 GPa | [카드 산술] |
| 겹침 | 실선 (평균 응력) 이 파선 (정확해) 과 선 굵기 안 | [판독] |
| 붕괴 | *"The uGIMP method broke down when compression reached 88%.  The CPDI method began to break down at about 93% compression."* | 인쇄 |
| σ_zz 부호 | z 를 막고 반지름으로 누르면 σ_zz 는 **인장** (편차 항이 이김: J 16 % 에서 부피 항 −6.87 GPa · 편차 zz +10.27 GPa) | [카드 산술] |

- 저자의 권고 네 까닭 (p.143): ① GIMP 를 축대칭에서 다시 유도한 자연스러운 결과 — 더 정확 · 수렴이 낫다고 *"reasonably presumed"* · 복잡한 응력 상태에서 효과가 클 수 있다 ② 자름이 r = 0 효과를 잘 다뤄 *"ghost nodes"* 처리 없이 보통 r 속도 0 경계로 된다 ③ *"this extension of the method to GIMP methods is essential when modeling large deformation because classic axisymmetric MPM methods are not robust"* ④ 평면 GIMP 코드에 쉽게 더할 수 있다.
- 그 앞 문장: *"In summary, acceptable results in uniform compression are possible without using new shape functions, but only if great care is used in setting boundary conditions."* (p.143)

### 3-3. 원기둥 끝 견인 (§4.2 · 식 43 · Fig. 8 · `txt_p18_traction_test_setup_cpdi_required.png`)

| 설정 | 값 | 표지 |
|---|---|---|
| 원기둥 | 길이 40 mm · 반지름 10 mm · 격자 2 × 2 mm · r = 0 면 r 변위 0 · 바닥 z 변위 0 | 인쇄 |
| 입자 | 간격 1 mm = 셀 절반 (Fig. 8 의 0.5 · 1.5 … 9.5 mm) → 다 채웠다면 10 × 40 = 400 개 | [판독] · [카드 산술] |
| 하중 | 위쪽 입자를 인장 · 응력 선형 증가 → 최종 1000 MPa · 변위 속도 *"(∼ 1%)"* of wave speed · 최종 변형률 약 50 % | 인쇄 |
| 두 방법 | 견인 = 변 3 (식 43 · CPDI) / 입자 힘 = 라디안당 F_p(t) = σ̇ r_p l_p Δr t (처음 치수 기준) | 인쇄 |
| 재료 | 3-2 와 같은 Neo-Hookean | 인쇄 |
| uGIMP | *"not stable for the simulated 50% tensile strain"* → 결과 없음 | 인쇄 |

**Fig. 8 — 하중 변에서의 처음 거리별 입자 σ_zz (MPa) [판독]** (그림의 점선 1000 은 997.9 로 읽힘 → 판독 치우침 약 −2 MPa)

| 처음 거리 (mm) | 0.5 | 1.5 | 2.5 | 3.5 | 4.5 | 5.5 | 6.5 | 7.5 | 8.5 | 9.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| 견인 (○) | 999.8 | 1004.1 | 1000.2 | 1000.4 | 999.2 | 997.5 | 991.8 | 998.6 | 998.6 | 992.7 |
| 입자 힘 (□) | **574.5** | 1149.5 | 1174.7 | 1182.7 | 1203.1 | 1200.8 | 1201.9 | 1193.8 | 1193.8 | 1182.4 |

- 입자 힘: 가장자리 입자 = 지정의 0.57 · 안쪽 평균 (1.5–9.5 mm) 1187 의 0.48 [카드 산술] · 안쪽 +15–20 % — 저자: *"particle force boundary conditions always have an artifact of low stress for the loaded particles"* · *"the cylinder contracted in the radial direction due to Poisson effects, and therefore, the applied forces, which were based on initial dimensions, caused higher stresses"* (p.144).
- 저자: *"The ability of traction boundary conditions to maintain a specified stress requires CPDI because it evaluates surface forces on deformed edges.  In contrast, uGIMP calculates surface forces using undeformed edges."* · *"CPDI is required for large strain calculations and for constant stress boundary conditions."* (p.144)

### 3-4. 관통 (§4.3 · Table I · Fig. 9 · 10 · `txt_p18_p19_penetration_setup_convergence_not_shown.png`)

| 설정 | 값 | 표지 |
|---|---|---|
| 봉 | 텅스텐 합금 · 뭉툭한 코 · 지름 0.4 cm · 길이 5.0 cm | 인쇄 |
| 표적 | 고경도 장갑강 원기둥 · 지름 4.0 cm · 길이 4.95 cm | 인쇄 |
| 충돌 속도 | 1.70 km/s | 인쇄 |
| 재료 | 둘 다 *"elastic-plastic"* · Johnson–Cook 흐름 [19] + Mie–Grüneisen 압력 [20] · 상수 = Table I (*"as reported by Anderson et al. [21]"*) — JC · MG 식은 인쇄 안 함 | 인쇄 |
| 격자 | Δr = Δz = 0.25 mm · *"four particles/cell"* | 인쇄 |
| 입자 수 | 봉 (반지름 셀 8 × 길이 셀 200) × 4 = 6,400 · 표적 (셀 80 × 198) × 4 = 63,360 → ≈ 7 만 | [카드 산술 — 셀을 다 채운다고 가정] |
| 격자 수렴 | *"Simulations done at higher and lower resolutions (not shown) confirm that the results are convergent with grid refinement."* | 인쇄 (수치 없음) |
| 두 물체 사이 | 접촉 방법 · 마찰 · 침식 (erosion) 여부 미인쇄 | [미확인] |
| 결과 | Fig. 9 = 10 · 30 · 60 µs 등가 응력 색 (색 막대 없음) · Fig. 10 = 코 · 꼬리 위치 | 인쇄 |

**Table I (인쇄 · Anderson 외 [21] 의 값)**

| 성질 | 텅스텐 | 강 |
|---|---|---|
| A (GPa) | 1.50696 | 1.50 |
| B (GPa) | 0.17664 | 0.569 |
| C | 0.016 | 0.003 |
| n | 0.12 | 0.22 |
| m | 1.0 | 1.17 |
| T_m (K) | 1723 | 1777 |
| C₀ (m/s) | 3980 | 3574 |
| S | 1.24 | 1.92 |
| γ₀ | 1.54 | 1.69 |
| 밀도 (g/cc) | 17.6 | 7.85 |
| 전단 계수 (GPa) | 124.0 | 77.3 |

**Fig. 10 — 코 · 꼬리 위치 (cm) [판독]** (0 = 처음 코 자리 · 꼬리 처음 −5.00)

| 시각 (µs) | 0 | 10.4 | 15.3 | 20.5 | 20.7 | 25.3 | 28.3 | 30.5 | 40.4 | 40.6 | 60.3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 코 실험 (○) | 0.00 | 0.92 | 1.34 | 1.75 | 1.72 | 2.16 | 2.38 | 2.62 | 3.24 | 3.33 | 4.56 |
| 코 MPM | −0.01 | 0.93 | 1.34 | 1.76 | 1.77 | 2.14 | 2.37 | 2.54 | 3.27 | 3.28 | 4.51 |
| 꼬리 실험 (□) | −5.00 | −3.32 | −2.41 | −1.54 | −1.64 | −0.82 | −0.31 | 0.20 | 1.64 | — | — |
| 꼬리 MPM | −4.99 | −3.23 | −2.41 | −1.54 | −1.51 | −0.75 | −0.26 | 0.09 | 1.65 | — | — |

- MPM − 실험 = 코 −0.08 … +0.05 cm · 꼬리 −0.11 … +0.13 cm [판독] · 거의 같은 시각의 두 실험점끼리 차 = 코 0.03 (20.5 ↔ 20.7 µs) · 0.09 (40.4 ↔ 40.6 µs) · 꼬리 0.10 cm (20.5 ↔ 20.7 µs) [판독 · 카드 산술] → MPM 과 실험의 차가 실험점 사이의 흩어짐과 같은 자릿수다.
- 처음 10.4 µs 평균 속도: 코 0.88 km/s · 꼬리 1.62 km/s [판독 · 카드 산술] (충돌 1.70 km/s).  MPM 선은 100 µs 에서 끝: 코 4.76 · 꼬리 4.42 cm → 남은 봉 0.34 cm (처음 5.0 cm) [판독 · 카드 산술].
- 저자: *"The simulation results have good agreement with experimental results from Anderson et al. [21], which are plotted as symbols."* (p.145) — 정량 지표 · 오차 막대 없음.

### 3-5. 계산 비용

- **인쇄된 값 없음** — 실행 시간 · 메모리 · 프로세서 · Δt · 걸음 수 · 입자 수 모두 미인쇄 [미확인].
- [카드 산술 · 논문 밖] 축대칭이 3D 를 대신할 때 격자 셀 수의 비 = 반지름 방향 셀 N_r 에 대해 3D 전체 (2N_r)² N_z ↔ 축대칭 N_r N_z → **4N_r 배** (3D ¼ 대칭이면 N_r 배).  관통 표적 (N_r 80 · N_z 198) 이면 3D 전체 5.07 × 10⁶ 셀 ↔ 축대칭 1.58 × 10⁴ 셀 = **320 배** (¼ 대칭 80 배).  같은 셀 수 M 으로 구 하나를 풀면 지름당 셀 수 = 3D 정육면체 M^{1/3} ↔ 축대칭 반원 단면 √(2M) (M = 10⁶ → 100 ↔ 1414).  ⚠ 명시적 Δt 가 셀 크기에 비례해 시간 걸음 수는 해상도를 따라 는다 — 비용 비는 셀 수 비가 아니다.

### 3-6. ★ 이 논문에 **없는** 값 (정직 목록)

- 3D 계산 · 3D 와의 대조 · 평면 2D 와 축대칭의 같은 문제 값 (Fig. 6 의 축 근처 J 뿐).
- 계산 비용 (3-5) · 코드 이름 · Δt · CFL 값 · 압축 속도 (§4.1) · 걸음 수 · 입자 수 (인쇄).
- 격자 수렴 수치 (§4.3 *"not shown"*) · 오차 노름 · 수렴 차수.
- 접촉 계산 예 (§3.3 정식화만) · 관통에서의 두 물체 처리 · 마찰 계수 · 침식.
- 균열 · 점착대 · J 적분 · 열 · 확산 계산 예 (§3.2 · §3.4 정식화만).
- 구 · 입자 · 분말 · 누르기 · 하중 제거 · 되돌아옴 · 잔류 변형.
- classic MPM 의 원판 결과 (불안정이라 그리지 않음) · uGIMP 의 견인 결과 (50 % 에서 불안정).
- Johnson–Cook · Mie–Grüneisen 의 식 (참고문헌으로 넘김) · 관통의 응력 값 (Fig. 9 색 막대 없음).
- ν 0.33 밖 (예: 거의 비압축 ν 0.49) 의 축 근처 거동.

---

## 4. 방법 ★

### 4-1. 축대칭 GIMP 의 기본 식 (§2 · 식 1–14 · `txt_p2_key_changes_cylindrical_integration.png`)

> *"Instead, we started from the cartesian formulation of GIMP [11] and modified it for axisymmetry.  The key changes were to replace volume integration by cylindrical volume integration and to account for cylindrical coordinates in gradient evaluations."* (p.128)

- 노드 운동량: **dp_i/dt = f_i^(int) + f_i^(ext) + f_i^(b) + f_i^(s)** (1) · **p_i = Σ_p p_p S_ip** (2)
- 내부력 (비응력 σ^(s) = σ/ρ): **f_i^(int) = −Σ_p m_p [σ^(s)_rr,p σ^(s)_rz,p ; σ^(s)_rz,p σ^(s)_zz,p] G_ip − Σ_p m_p (σ^(s)_θθ,p, 0) T_ip** (3) — 둘째 항이 **후프 응력 항** (체크리스트 8)
- 외력 · 체적력: f_i^(ext) = Σ_p F_p S_ip · f_i^(b) = Σ_p m_p b_p S_ip (4) · 견인: **f_i^(s) = (1/2π)∫ T N_i(r, z) dS** (5) (라디안당 · N_i = 보통 격자 형상 함수)
- ★ 형상 함수 (Ω_p = r–z 평면의 변형한 입자 영역 · χ_p = 입자 가중 함수 (그 선택이 'generalized') · A_p = 영역 넓이 · ⟨r_p⟩ = 영역의 평균 반지름):
  - **S_ip = (1/(A_p⟨r_p⟩)) ∫_Ωp r χ_p(r, z) N_i(r, z) dr dz** (6)
  - **G_ip = (1/(A_p⟨r_p⟩)) ∫_Ωp r χ_p(r, z) ∇N_i(r, z) dr dz** (7)
  - **T_ip = (1/(A_p⟨r_p⟩)) ∫_Ωp χ_p(r, z) N_i(r, z) dr dz** (8) — r 가중 없음
  - [카드 산술] χ_p = 1 (영역 안) 이면 ∫ r χ_p dr dz = A_p⟨r_p⟩ → Σ_i N_i = 1 에서 Σ_i S_ip = 1 (분할의 합).
- 변형: F^(n+1) = dF F^(n) · **dF = exp(Δt∇v) = I + ∇u + Σ_{k=2}^∞ (∇u)^k/k!** (9) · **∇u = [[∂u_r/∂r, ∂u_r/∂z, 0], [∂u_z/∂r, ∂u_z/∂z, 0], [0, 0, du_r/r_p]]** (10) · v_i = p_i/Σ_p m_p S_ip (11) · (∂u_r/∂r, ∂u_r/∂z) = Δt Σ_i v_i,r G_ip (12) · (∂u_z/∂r, ∂u_z/∂z) = Δt Σ_i v_i,z G_ip (13) · **du_r/r_p = Δt Σ_i v_i,r T_ip** (14)
- 옛 판 회복: χ = A_p δ(r_p) → S_ip = N_i(r_p, z_p) · G_ip = ∇N_i(r_p, z_p) · T_ip = N_i(r_p, z_p)/r_p (p.129).

### 4-2. uGIMP (§2.1 · 식 15–29 · Fig. 1–3 · `txt_p4_ugimp_undeformed_domain_regular_grid.png` · `txt_p5_partition_of_unity_origin_truncation_fig2.png`)

- 정의: *"In uGIMP, the particle domain is assumed to remain undeformed at the size of the initial domain but translates along with the particle and χ_p(r, z) = 1 within the domain and zero elsewhere.  This approach is commonly used because of numerical difficulty evaluating GIMP integrals for arbitrarily deformed particle domains.  For simpler explicit calculations, uGIMP is restricted to a regular grid with all elements having size Δr × Δz."* (p.130)
- 나눔: **S_ip = S_r(ξ_p, r_i) S_z(η_p)** (16) — S_z = 평면 uGIMP (식 A.1) · **S_r(ξ_p, r_i) = (1/(W_p⟨r_p⟩)) ∫_{r_min}^{r_max} r N_i(r) dr = (1/(2l_p(ξ_p + 2n_i))) ∫_{ξ_p−l_p}^{ξ_p+l_p} (ξ + 2n_i) N_i(ξ) dξ** (17) · N_i(ξ) = (2 + ξ)/2 (−2 < ξ < 0) · (2 − ξ)/2 (0 ≤ ξ < 2) (18).
- 닫힌 꼴 (19): 다섯 구간 (−2 − l_p < ξ_p < −2 + l_p · −2 + l_p ≤ ξ_p < −l_p · −l_p ≤ ξ_p < l_p · l_p ≤ ξ_p < 2 − l_p · 2 − l_p ≤ ξ_p < 2 + l_p) 각각 = 평면 uGIMP + 1/(2n_i + ξ_p) 에 비례하는 항 (`eq_19_ugimp_axisym_Sr_piecewise.png`).  [카드 산술] 식 (19) ↔ 정의 적분 (17) 의 차 최대 3.9 × 10⁻¹² (l_p = 1/2 · n_i = 1–10 · r > 0).
- 기울기: **G_ip = ((2/Δr) dS_r(ξ_p, r_i) S_z(η_p), (2/Δz) S_r(ξ_p, r_i) dS_z(η_p))** (22) · dS_r = (Δr/(2W_p⟨r_p⟩))∫ r dN_i/dr dr = (1/(2l_p(ξ_p + 2n_i)))∫ (ξ + 2n_i) dN_i/dξ dξ (23) · 닫힌 꼴 (24) = 평면 + 1/(2n_i + ξ_p) 항 · [카드 산술] (24) ↔ (23) 차 최대 3.3 × 10⁻⁶ (수치 적분 한계).
- 후프: **T_ip = (2/(Δr(2n + ξ_p))) S_z(ξ_p) S_z(η_p)** (27) = 평면 uGIMP ÷ r_p (r_p = (2n_i + ξ_p)Δr/2 [카드 산술]).
- ★ 축 처리 (p.131): *"The above integration satisfies partition of unity (Σ_i S_r(ξ_p, r_i) = 1), but when particles are within l_pΔr/2 of the origin, the particle domain crosses r = 0.  As r_p approaches zero, some shape functions will have singularities at ξ_p = −2n_i.  We show below that this non-physical extension of the domain and shape function singularities can lead to loss of accuracy for particles near the origin.  The results are improved by truncating the particle domain, which is only needed when n_i < (1 + l_p/2) and r_p < l_pΔr/2 (or ξ_p < −2n_i + l_p).  For simplicity, if the grid includes any nodes with n_i < (1 + l_p/2), the grid is required have nodes at r = 0 and therefore all n_i in a regular grid will be integers.  In such a grid, special case evaluations are needed only for n_i = −1, 0, and 1."* · *"The simplest approach in uGIMP is to truncate the particle domain at r = 0 and to disallow particle positions less than r = 0."*
  - n_i = −1: S_r^(−1) = 0 · dS_r = 0 · T = 0.
  - n_i = 0 (축 노드 · 0 ≤ ξ_p < l_p): 자른 영역 폭 ξ_p + l_p · 중심 (ξ_p + l_p)/2 → **S_r^(0) = (2/(ξ_p + l_p)²)∫_0^{ξ_p+l_p} ξ N_i dξ = (3 − l_p − ξ_p)/3** (20) · **dS_r^(0) = −1/2** (25) · **T^(0) = (1/Δr)(4/(l_p + ξ_p) − 1)S_z(η_p)** (28).
  - n_i = 1 (첫 노드 · −2 ≤ ξ_p < −2 + l_p): 폭 ξ_p + l_p + 2 · 중심 (ξ_p + l_p − 2)/2 → **S_r^(1) = (2 + l_p + ξ_p)/3** (21) · **dS_r^(1) = +1/2** (26) · **T^(1) = (1/Δr)S_z(η_p)** (29).
  - [카드 산술] 자른 꼴의 분할의 합 = 1 (r_p 0 … 2.95Δr · 차 2.2 × 10⁻¹⁶) · 축 근처 기울기는 축 노드 −1/2 · 첫 노드 +1/2 의 평평한 선형 (합 0) · T 는 유한 (r_p → 0 에서 7/Δr · l_p = 1/2).
- Fig. 2 · 3 (l_p = 1/2): 실선 = 축대칭 (n_i = 0 · 1 · 2) · 파선 = 평면 (n_i = −1 … 2) · 점선 = 안 자른 n_i = −1 · 0 · 1 — *"Both S_r(ξ_p, −1) and S_r(ξ_p, 1) are singular, although the singularities cancel to retain partition of unity.  Some calculations below show these singularities can reduce accuracy."* (p.131).  [판독] Fig. 2 의 실선은 식 (19)–(21) 과 0.003 안.

### 4-3. CPDI (§2.2 · 식 30–39 · Fig. 4 · `txt_p8_ugimp_50pct_strain_cpdi_deformed_domain.png` · `txt_p9_p10_cpdi_corner_cross_origin_shrink.png`)

- 근사: **S_ip = (1/(A_p⟨r_p⟩)) ∫_Ωp r (Σ_{α=1}^4 M_α(r, z) N_i(r_p^(α))) dr dz** (30) — 격자 함수 N_i 를 평행사변형 네 모서리 r_p^(α) 의 값으로 보간 (M_α = 영역의 모양 함수).
- 영역: **d_1 = (F_rr Δr, F_zr Δz)/4 · d_2 = (F_rz Δr, F_zz Δz)/4** (31) (인쇄 그대로 · §12) · (r, z) = r_p + ρd_1 + ζd_2 = (Σ r_α M_α(ρ, ζ), Σ z_α M_α(ρ, ζ)) (32) · ρ, ζ ∈ [−1, 1] · M_1 = (1 − ρ)(1 − ζ)/4 등 반시계 · 부모 좌표 적분 (33) · J = [[d_1r, d_1z], [d_2r, d_2z]] (34) · \|J\| = A_p/4.
- ★ 닫힌 꼴: **S_ip = ¼[(1 − (d_1r + d_2r)/(3r_p))N_i(r_p^(1)) + (1 + (d_1r − d_2r)/(3r_p))N_i(r_p^(2)) + (1 + (d_1r + d_2r)/(3r_p))N_i(r_p^(3)) + (1 − (d_1r − d_2r)/(3r_p))N_i(r_p^(4))]** (35) · G_ip (36) → (37) (r 성분 = (1/A_p)[(d_1z − d_2z − β/(3r_p))N_1 + (d_1z + d_2z + β/(3r_p))N_2 − (d_1z − d_2z + β/(3r_p))N_3 − (d_1z + d_2z − β/(3r_p))N_4] · z 성분 = (1/A_p)[−(d_1r − d_2r)(1 − (d_1r + d_2r)/(3r_p))N_1 − (d_1r + d_2r)(1 + (d_1r − d_2r)/(3r_p))N_2 + (d_1r − d_2r)(1 + (d_1r + d_2r)/(3r_p))N_3 + (d_1r + d_2r)(1 − (d_1r − d_2r)/(3r_p))N_4]) · β = d_1r d_1z − d_2r d_2z (38) · **T_ip = (1/(4r_p))[N_i(r_p^(1)) + N_i(r_p^(2)) + N_i(r_p^(3)) + N_i(r_p^(4))]** (39) = 평면 CPDI ÷ r_p.
- [카드 산술] 기울어진 평행사변형 (셀 = 1 · r_p = (1.3, 0.7) · d_1 = (0.31, 0.06) · d_2 = (−0.04, 0.27) · 선형 격자 노드 다섯) 에서 (35) · (37) · (39) 를 식 (33) · (36) 의 수치 적분 (Gauss–Legendre 8 × 8) 과 견주면 차 최대 5.6 × 10⁻¹⁷ · 3.3 × 10⁻¹⁶ · 8.3 × 10⁻¹⁷ — 인쇄된 닫힌 꼴 셋은 옳다.
- ★ 축 넘김: *"In accurate simulations, the deformed domain should naturally stay within valid territory, but cruder calculations or round-off error might cause some corners to pass r = 0 (and they do in some sample calculations).  Truncating as done in uGIMP cannot be used because it would leave a non-quadrilateral particle domain that is difficult to integrate.  The option proposed here is simply to shrink the domain to fit."* → r_p − \|d_1r + d_2r\| < 0 이면 s = r_p/\|d_1r + d_2r\| 로 d_1 · d_2 를 곱해 *"a truncated parallelogram that just touches the origin but is entirely within r > 0"* (p.135–136).

### 4-4. 견인력 경계 (§3.1 · 식 40–53 · `txt_p10_evaluate_all_extensions_traction_rarely_done.png` · `txt_p11_planar_thickness_3d_six_faces.png`)

- *"The most accurate method in MPM for applying tractions is to use the surface force term in Equation (5), but it is rarely done.  Its problem is the challenge of integrating over the deformed surface of the object, much like uGIMP is used to avoid integrating over the deformed particle domain.  But, this challenge can be solved by exploiting CPDI methods [3]."* (p.136) — 견인이 걸리는 변은 시뮬레이션 경계 조건으로 미리 고른다.
- 변 1: g(ρ) = r_p + ρd_1 − d_2 · dS = 2πr(ρ)\|d_1\|dρ → **f_ip,1^(s) = (1/2π)∫ T N_i dS = T\|d_1\|∫_{−1}^{1} (g(ρ)·(1, 0))(Σ_α M_α(ρ, −1)N_i(r_p^(α))) dρ** (40) → **f_ip,1^(s) = \|d_1\|[(r_px − d_2x − d_1x/3)N_i(r_p^(1)) + (r_px − d_2x + d_1x/3)N_i(r_p^(2))]T** (41) · 변 2–4 (42)–(44).  [카드 산술] 변 1 에서 M_1 = (1 − ρ)/2 · M_2 = (1 + ρ)/2 · r(ρ) = r_px − d_2x + ρd_1x 를 적분하면 (41) 의 두 계수가 그대로 나온다.
- uGIMP: d_1 = (l_pΔr/2, 0) · d_2 = (0, l_pΔz/2) 로 (45)–(48) · 축을 넘으면 먼저 자름 (CPDI = 줄임 · uGIMP = r_px − d_1x < 0 이면 r′_px = d′_1x = (r_px + d_1x)/2).
- 평면 판 (처음 공개 · *"We are not aware of corresponding planar MPM results for traction forces in the literature"*): dS = B\|g′(ρ)\|dρ → (49) · **f_ip,1^(s) = \|d_1\|B[N_i(r_p^(1)) + N_i(r_p^(2))]T** (50) · (51)–(53).  *"The difference between the planar results and the axisymmetric results is that thickness, B, replaces all the coefficients in the axisymmetric results, which are radial positions along the traction edge.  Further extension to 3D is straightforward by integrating over the six faces of the deformed particle domain."* (p.137)
- T 는 한 걸음 동안 변 위에서 일정 · 두 선택: 전체 좌표에 묶음 (단단한 하중 장치의 거시 응력) / 변 방향에 묶음 (돌아가는 물체에 일정 압력 · d_1 · d_2 로 걸음마다 다시 계산) (p.137).
- 입자 힘의 문제 (p.138 · `txt_p12_particle_forces_explicit_cracks_jintegral.png`): *"Use of such forces, which are applied at the particle centroids, results in that force effectively being a distributed load over the particle domain.  This approach leads to unphysical stress fluctuations in the region of the applied load."* · 축대칭에서는 라디안당 힘이라 r 이 일정하지 않은 경계에서 위치에 달려야 한다.

### 4-5. 명시 균열 (§3.2 · p.138)

- CRAMP [9] (노드–입자 선이 균열면을 넘는지로 속도장을 위 · 아래로 나눔) 는 기하라 *"works in axisymmetric MPM without any modification from planar MPM"*.
- 점착대 [13]: 힘 = 견인 법칙 응력 × 국소 균열면 넓이 → 평면 (균열 조각 길이 × 두께) ↔ 축대칭 (균열 조각 길이 × 노드의 반지름 · 라디안당).
- J 적분 [7, 8, 14]: *"Our literature search, however, did not find any fully developed results for axisymmetric J integral."* · Bergkvist–Huong [15] · Broberg [16] 두 이론은 반지름 방향 균열만 · *"The full implementation of J integral calculations for arbitrary crack orientation in axisymmetric problem for both MPM and finite element analysis is in need of additional development."*

### 4-6. 다물질 접촉 · 불완전 계면 (§3.3 · 식 54–55 · `txt_p12_p13_contact_normal_area_gradient_r0.png`)

- 틀: *"contact is handled by using multimaterial mode MPM where each material extrapolates to its own velocity field.  Nodes interacting with a single material proceed by normal MPM methods, but nodes with more than one material use contact physics to adjust the nodal momenta and/or to add internal forces.  Available methods can implement stick contact, frictional contact [4–6], or imperfect interface traction laws [17]."* (p.138)
- 바꿀 곳은 법선 하나: *"Most planar 2D contact tasks can be applied directly to axisymmetric MPM.  The only exception is determination of the normal vector between two contacting surfaces, and experience has shown that accurate determination of the normal is crucial to accurate contact simulations [6]."* (p.138)
- 옛 법선 (질량 · 부피 기울기 · 밀도가 다른 물질끼리면 부피 쪽): **‖n_i,a‖n_i,a = −∇V_a(x_i) = Σ_{p∈a} V_p G_ip** (54) — *"This method does not work in axisymmetric MPM because V_p depends on radial position, which causes ∇V_a(x_i) to lose is connection to r-z plane surface normal."* (p.139)
- ★ 축대칭 법선: **‖n_i,a‖n_i,a = −∇A_a(x_i) = Σ_{p∈a} A_p G_ip** (55) (A_p = r–z 평면의 변형한 영역 넓이).
- 다듬기 둘 (p.139): ① 대칭이면 축에서 면적 기울기의 r 성분 = 0 이어야 하지만 외삽으로는 늘 0 이 아님 → **r_i = 0 노드에서 n 의 r 성분을 0 으로** ② 노드 부피가 셀 부피에 가까울 때만 접촉으로 보는 방법은 **부피 대신 면적**을 견주고, **r_i = 0 노드의 면적을 두 배로** (*"to account for the fact it is the middle of a solid object and not on an edge.  This same modification should be made in planar contact problems when they involve symmetry planes; the only difference is that axisymmetry always has a symmetry plane at r = 0."*).
- 불완전 계면 [17 · 18]: 총 계면 접촉 넓이 계산을 축대칭으로 따로 고쳐야 한다 — 그 유도는 [17] 에 있다 (이 논문에는 없음).

### 4-7. 열 전도 · 확산 (§3.4 · 식 56–62 · `txt_p14_conduction_no_extrapolation_diffusion.png`)

- 약형 (56) → 발산 정리 (57) → **M_i dT_i/dt = f_i^(g) + f_i^(s) + f_i^(e)** (58) · M_i = Σ m_p C_p^(p) S_ip · T_i = (1/M_i)Σ m_p C_p^(p) T_p S_ip (59) · f^(g) = −Σ V_p k∇T_p · G_ip · f^(s) = Σ V_p q_p S_ip · f^(e) = ∫ N_i Φ dS (60) · ∇T_p = Σ_i T_i G_ip (61).
- ★ 입자 갱신: **T_p^(k+1) = T_p^(k) + Δt Σ_i (dT_i/dt) S_ip** (62) — *"and importantly not by extrapolating T_i, because that causes numerical conduction.  However, when using temperature in constitutive laws on particles, it is preferable to use an extrapolated T_i instead of T_p.  T_i is a better representation of the temperature field, whereas T_p is prone to local fluctuations within grid cells."* (p.140)
- 축대칭에서 바꿀 것: 축대칭 S_ip · G_ip · 라디안당 m_p · V_p · 원통 면 위 라디안당 유속 (견인 방법에서 T → Φ).  확산 = k → D · q → 농도 원천 · m_pC_p → V_p · T → 화학 퍼텐셜 μ (p.140).

### 4-8. ★ 체크리스트 9 항 (§5 · p.145 · `txt_p19_conclusion_checklist.png` · 원문 그대로)

> *"(1) Particle mass is mass per radian (m_p = ρA_p r_p).  (2) If the grid has any nodes at r = 0, apply zero velocity boundary conditions in the r direction.  (3) Whenever shape functions or gradients are needed, find the axisymmetric shape functions (for uGIMP or CPDI) with domain truncation.  Some results that depend on shape function gradients will also need T_ip.  A convenient method in some codes is to store T_ip in the unused third component of a 3D gradient vector.  (4) If including multimaterial contact, extrapolate the r-z plane area gradient to nodes and for nodes at r = 0 set the r component of that gradient to zero.  This gradient is used to find contact normals.  If contact methods use nodal areas for detecting contact, double the nodal area on r = 0 nodes.  (5) On strain updates, find the hoop component of the deformation gradient using du_r/r in Equation (14).  (6) Each material used in simulations must support axisymmetric deformation gradients in their constitutive laws including updates for hoop stresses and strains.  (7) When applying traction boundary conditions, calculate the axisymmetric form of the surface forces.  When applying forces directly to particles, make sure the input is in force per radian and the forces correctly depend on position, if needed, to obtain desired stress along the edge.  (8) When finding f_i^(int), include the hoop stress term in Equation (3).  (9) When updating particle positions, if any particle crosses r = 0, stop the calculations (or attempt a fix, such as to move to r ⩾ 0)."*

### 4-9. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

- 이 논문의 '입자' 는 **연속체의 물질점** 이다 — 알갱이 · 구가 아니다.  처음 영역 = 사각형 (uGIMP · 크기 고정 · 같이 이동) / 평행사변형 (CPDI · F 로 실어 나름).  초기 배치는 셀을 고르게 채움 (방향당 2 · 관통 셀당 4).
- 무질서 · 랜덤 배치 · 입자 크기 분포 · 알갱이 사이 접촉망은 없다.  우리 쪽에서 축대칭으로 구 하나를 풀면 구 = r–z 반원 단면을 물질점으로 채운 것이 된다 [카드 추론].
- 축 r = 0 을 넘는 물질점은 허용하지 않는다 (uGIMP · 체크리스트 9) — CPDI 는 영역 모서리만 줄인다.

### 4-10. ★ 우리 2차 B-spline 과의 관계 (원문 식으로 · 판정 없이 · 전부 [카드 산술] / [다른 카드])

1. 평면 uGIMP (식 A.1) 에 **l_p = 1** (셀당 방향마다 입자 1 · 영역 폭 = 셀 Δ) 을 넣고 x = η/2 (셀 단위) 로 쓰면 \|x\| < 1/2 에서 3/4 − x² · 1/2 ≤ \|x\| < 3/2 에서 ½(3/2 − \|x\|)² = **2차 B-spline** — `bardenhagen2004_…` §4-8 (l_p = L/2) 과 같은 결과 [다른 카드].
2. 같은 l_p = 1 을 축대칭 식 (19)–(21) 에 넣으면 r 가중 판이 된다: (19) ↔ 정의 (17) 차 8.2 × 10⁻¹² · 자른 꼴의 분할의 합 차 2.2 × 10⁻¹⁶ · n = 1000 에서 평면과 차 8.3 × 10⁻⁵ · 축 위 (r_p → 0) S_r(0) = 2/3 · S_r(1) = 1/3 · T^(0) → 3/Δr · 자르지 않으면 2r_p/Δr = 0.05 에서 S_r(−1) = −1.43 (l_p = 1/2 의 −0.30 보다 크다 — 지지가 넓을수록 축 특이가 크다).
3. 그러나 우리 MLS-MPM 은 물질점 자리의 B-spline 가중 + APIC 아핀 C_p 로 옮기고 내부력을 MLS 대용 기울기 M_p⁻¹N_i(x_i − x_p) 로 쓴다 [다른 카드 `hu2018_…` §4-3] — 이 논문 식 (2) · (3) · (6)–(8) 과 꼴이 다르다.  **MLS-MPM 의 축대칭 꼴은 이 논문에 없다.**  필요한 것의 목록만: ① r 가중 전달 가중 (위 2 가 한 후보) ② 후프 항 (σ_θθ 의 내부력 · du_r/r 의 변형) ③ 축 처리 (자름 · 축 노드 · r 속도 0 · 축 넘김 정지) ④ 라디안당 질량 · 부피 ⑤ 다물질이면 면적 기울기 법선.

---

## 5. 결과 — 절별

### 5-1. 서론 (§1 · p.127–128)
MPM 은 큰 변형 [3] · 접촉 [4–6] · 파괴 [7–9] 에 쓰이고 Sandia CTH 에도 구현됐다 [10].  GIMP [11] · CPDI [3] 가 견고성 · 정확도를 크게 높였지만 축대칭은 점 질량 시절의 Sulsky–Schreyer [12] 하나뿐 — 충돌 · 크레이터 · 봉 관통 · 성형 작약 제트 같은 축대칭 문제를 위해 GIMP 판을 유도하고 확장을 다시 본다.

### 5-2. 정식화 (§2 · 식 1–39)
§4-1–4-3.  핵심: r 가중 S_ip · G_ip + 새 T_ip · 라디안당 질량 · 후프 변형률 · uGIMP / CPDI 닫힌 꼴 · 축 처리.

### 5-3. 확장 (§3 · 식 40–62)
*"Whenever deriving a new form of MPM, such as this new axisymmetric form of MPM, it is crucial to evaluate the consequences of the new form on all other MPM options."* (p.136) — 견인 (4-4) · 균열 (4-5) · 접촉 (4-6) · 열 · 확산 (4-7).

### 5-4. 균일 반지름 압축 (§4.1 · Fig. 5–7)
3-2.  자른 축대칭 형상 함수만 J 를 고르게 · 평면 형상 함수는 경계 처리를 잘하면 쓸 만하다 (거울) · 평균 응력은 정확해와 겹친다 · uGIMP 88 % · CPDI 약 93 % 에서 붕괴.

### 5-5. 견인 경계 (§4.2 · Fig. 8)
3-3.  견인 = 지정 응력 유지 (가장자리 포함) · 입자 힘 = 가장자리 낮음 + 면적 변화 드리프트 · CPDI 필요.

### 5-6. 관통 (§4.3 · Fig. 9 · 10 · Table I)
3-4.  코 · 꼬리 위치가 실험과 맞음 (정량 지표 없음) · 격자 수렴 *"not shown"*.

### 5-7. 결론 (§5 · p.145)
*"Reformulation of GIMP for axisymmetry leads to new shape functions and gradients that are recommended for use in MPM axisymmetric simulations.  The consequences of axisymmetry were considered for many MPM extensions, and all of them could be used in axisymmetric models with minor modifications, except for J integral calculations, which needs additional work."* + 체크리스트 9 항 (4-8).

---

## 6. 그림 · 표 · 식 · 근거 글 크롭별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions/` · 그림 10 장 (도구 크롭 10 장 전부 다시 자름 — 9 장은 글 단 전체 폭이라 벡터 그림의 잉크 경계 + 6 pt 로 · fig_4 는 위쪽 식 (33) 이 섞여서 · fig_9 는 내장 래스터 ± 6 pt · 300 dpi · 캡션은 렌더에서 다시 씀 — 글자 층 캡션은 기호가 깨짐) + 표 1 장 (손 크롭 · 'Table I' 로마 숫자라 도구가 놓침) + 식 69 장 (식 번호마다 하나 · 400 dpi · 사방 7 pt) + 근거 글 20 장 (300 dpi · 여러 토막은 회색 선으로 가름) + `digitized.csv`.  보충 자료 없음.  [우리 …] · [카드 …] 표지는 논문 밖 판단.

| 그림 · 표 | 파일 | 원 캡션 요지 | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| Fig. 1 | `fig_1.png` | 노드 i 둘레 S_r 의 다섯 구간 · 지지 ±(2 + l_p) = 둘째 이웃 셀까지 | 축대칭에서도 지지는 평면과 같다 (값만 다름) — 노드 i+1 아래 ξ 글자 '−2' 인쇄 (§12) |
| Fig. 2 | `fig_2.png` | S_r (실선 n_i = 0 · 1 · 2) ↔ 평면 (파선) ↔ 안 자른 판 (점선 · 'red' 라 적혔으나 인쇄는 검정) | ★ 차이는 축 셀 둘에 몰림 · 안 자른 n_i = −1 은 음의 꼬리 특이 [판독 · 실선 = 식 19–21 과 0.003 안] |
| Fig. 3 | `fig_3.png` | dS_r — 자르면 축까지 ±1/2 로 평평 · 안 자르면 특이 | 축 근처 기울기 = 축 노드와 첫 노드 사이 선형 보간 — 우리 축대칭 판의 기울기 점검 기준 |
| Fig. 4 | `fig_4.png` | 평행사변형 영역 · d_1 · d_2 · 모서리 1–4 · 변 1–4 (반시계 · 왼쪽 아래부터) | CPDI 영역 · 견인 변 번호 (§4.2 의 하중 = 변 3) |
| Fig. 5 | `fig_5.png` | 축 근처 입자 J — 자름 / 안 자름 × uGIMP / CPDI (ΔR/R₀ 0.6) | ★ 3-2 표 — 축 첫 입자: 안 자른 uGIMP 6.52 · CPDI 20.12 ↔ 자름 16.31 · 16.48 % [판독].  **우리 쪽**: 축대칭 판의 첫 단위 시험 꼴 (축 근처 입자 J 가 고른가) |
| Fig. 6 | `fig_6.png` | 축대칭 자름 uGIMP (파선) ↔ 평면 형상 함수 + 축 바깥 노드 처리 셋 (실선) | ★ 평면 형상 함수 첫 입자 23.33 % · BC 0 17.48 · 거울 16.02 % [판독].  **우리 쪽**: 평면 B-spline 을 r–z 에 그대로 쓰면 축 첫 셀이 틀린다는 원문 숫자 |
| Fig. 7 | `fig_7.png` | 평균 σ_rr = σ_θθ · σ_zz ↔ 정확해 (Neo-Hookean E 2300 · ν 0.33) | 정확해 단위 시험 (식 66–67) — 선은 V/V0 ≈ 9.3 % 까지 [판독] ↔ 본문 84 % (§12) |
| Fig. 8 | `fig_8.png` | 하중 변에서의 거리별 입자 σ_zz — 견인 ↔ 입자 힘 · 점선 = 지정 1000 MPa | ★ 3-3 표 — 가장자리 574.5 · 안쪽 1149.5–1203.1 (입자 힘) ↔ 991.8–1004.1 (견인) [판독].  **우리 쪽**: 하중을 입자에 걸면 가장자리 · 면적 인공물 |
| Fig. 9 | `fig_9.png` | 텅스텐 봉 → 강 · 10 · 30 · 60 µs · 등가 응력 색 · 아래 가장자리 = 축 | 색 막대 없음 → 값 판독 불가 · 축 근처에서 큰 변형 (봉 앞끝 버섯꼴) 이 생기는 예 |
| Fig. 10 | `fig_10.png` | 코 · 꼬리 위치 — 기호 = Anderson 외 실험 · 선 = 축대칭 MPM | ★ 3-4 표 — 차 코 −0.08 … +0.05 · 꼬리 −0.11 … +0.13 cm [판독] |
| Table I | `tab_1.png` | 관통 재료 상수 (Anderson 외 [21]) · Johnson–Cook + Mie–Grüneisen | 금속 상수 — 우리 재료 아님 · 맞춘 값 아님 |

**식 그림** (전부 손 크롭 · 400 dpi · 사방 7 pt 흰 여백 · 식 번호 포함 · 이웃 글줄 · 머리글 · 바닥글 · 내려받기 표지 없음 · 인쇄 그대로):

| 식 | 파일 · 쪽 | 내용 | 쓰임 |
|---|---|---|---|
| (1) | `eq_01_nodal_momentum_rate_force_sum.png` · p.128 | dp_i/dt = f_i^(int) + f_i^(ext) + f_i^(b) + f_i^(s) | 노드 운동량 식 |
| (2) | `eq_02_nodal_momentum_p2g.png` · p.128 | p_i = Σ_p p_p S_ip | 입자 → 노드 운동량 (축대칭 S_ip) |
| (3) | `eq_03_internal_force_hoop_stress_term.png` · p.128 | f_i^(int) = −Σ m_p [σ^(s)_rr σ^(s)_rz; σ^(s)_rz σ^(s)_zz] G_ip − Σ m_p (σ^(s)_θθ,p, 0) T_ip | ★ 내부력 + 후프 응력 항 (체크리스트 8) |
| (4) | `eq_04_external_and_body_forces.png` · p.128 | f^(ext) = Σ F_p S_ip · f^(b) = Σ m_p b_p S_ip | 입자 외력 · 체적력 |
| (5) | `eq_05_surface_traction_force_per_radian.png` · p.128 | f^(s) = (1/2π)∫ T N_i dS | 견인력 (라디안당) |
| (6) | `eq_06_axisym_gimp_shape_function_Sip.png` · p.129 | S_ip = (1/(A_p⟨r_p⟩))∫ r χ_p N_i dr dz | ★ 축대칭 GIMP 형상 함수 (r 가중) |
| (7) | `eq_07_axisym_gimp_gradient_Gip.png` · p.129 | G_ip = (1/(A_p⟨r_p⟩))∫ r χ_p ∇N_i dr dz | ★ 축대칭 GIMP 기울기 |
| (8) | `eq_08_axisym_gimp_hoop_function_Tip.png` · p.129 | T_ip = (1/(A_p⟨r_p⟩))∫ χ_p N_i dr dz | ★ 새 함수 T_ip (r 가중 없음 · 후프 항) |
| (9) | `eq_09_incremental_deformation_gradient_series.png` · p.129 | dF = exp(Δt∇v) = I + ∇u + Σ_{k≥2}(∇u)^k/k! | 변형 경사 증분 (회전이면 k ≥ 2) |
| (10) | `eq_10_displacement_gradient_hoop_term.png` · p.129 | ∇u = [[∂u_r/∂r, ∂u_r/∂z, 0], [∂u_z/∂r, ∂u_z/∂z, 0], [0, 0, du_r/r_p]] | ★ 후프 변형률 du_r/r_p |
| (11) | `eq_11_nodal_velocity.png` · p.129 | v_i = p_i / Σ m_p S_ip | 노드 속도 |
| (12) | `eq_12_ur_gradient_from_nodes.png` · p.129 | (∂u_r/∂r, ∂u_r/∂z) = Δt Σ v_i,r G_ip | r 변위 기울기 |
| (13) | `eq_13_uz_gradient_from_nodes.png` · p.129 | (∂u_z/∂r, ∂u_z/∂z) = Δt Σ v_i,z G_ip | z 변위 기울기 |
| (14) | `eq_14_hoop_strain_increment_Tip.png` · p.129 | du_r/r_p = Δt Σ v_i,r T_ip | ★ 후프 변형률 = T_ip (체크리스트 5) |
| (15) | `eq_15_dimensionless_node_coordinates.png` · p.130 | ξ = 2(r − r_i)/Δr · η = 2(z − z_i)/Δz | 무차원 좌표 (셀 = 2 × 2) |
| (16) | `eq_16_ugimp_separable_shape_function.png` · p.130 | S_ip = S_r(ξ_p, r_i) S_z(η_p) | uGIMP = r 몫 × z (평면) 몫 |
| (17) | `eq_17_ugimp_radial_shape_function_integral.png` · p.130 | S_r = (1/(W_p⟨r_p⟩))∫ r N_i dr = (1/(2l_p(ξ_p + 2n_i)))∫ (ξ + 2n_i) N_i dξ | ★ r 가중 정의 적분 |
| (18) | `eq_18_tent_grid_shape_function_dimensionless.png` · p.130 | N_i(ξ) = (2 + ξ)/2 · (2 − ξ)/2 · 0 | 무차원 텐트 격자 함수 |
| (19) | `eq_19_ugimp_axisym_Sr_piecewise.png` · p.130 | S_r(ξ_p, n_i) = 다섯 구간 (평면 + 1/(2n_i + ξ_p) 항) | ★ 축대칭 uGIMP 닫힌 꼴 (카드 수치 확인) |
| (20) | `eq_20_truncated_Sr_node_at_origin.png` · p.131 | S_r^(0) = (3 − l_p − ξ_p)/3 (0 ≤ ξ_p < l_p) | ★ 축 노드 · 자른 영역 |
| (21) | `eq_21_truncated_Sr_first_node.png` · p.131 | S_r^(1) = (2 + l_p + ξ_p)/3 (−2 ≤ ξ_p < −2 + l_p) | ★ 첫 노드 · 자른 영역 |
| (22) | `eq_22_ugimp_gradient_separable.png` · p.131 | G_ip = ((2/Δr) dS_r S_z, (2/Δz) S_r dS_z) | uGIMP 기울기 (나눔 꼴) |
| (23) | `eq_23_ugimp_radial_gradient_integral.png` · p.132 | dS_r = (1/(2l_p(ξ_p + 2n_i)))∫ (ξ + 2n_i) dN_i/dξ dξ | r 기울기 정의 적분 |
| (24) | `eq_24_ugimp_axisym_dSr_piecewise.png` · p.132 | dS_r(ξ_p, n_i) = 여섯 줄 (평면 + 1/(2n_i + ξ_p) 항) | 축대칭 uGIMP 기울기 닫힌 꼴 |
| (25) | `eq_25_truncated_dSr_node_at_origin.png` · p.132 | dS_r^(0) = −1/2 (0 ≤ ξ_p < l_p) | ★ 축 노드 기울기 (인쇄 적분 아래 끝 어긋남 §12) |
| (26) | `eq_26_truncated_dSr_first_node.png` · p.133 | dS_r^(1) = 1/2 (−2 < ξ_p < −2 + l_p) | 첫 노드 기울기 |
| (27) | `eq_27_ugimp_Tip_planar_over_rp.png` · p.133 | T_ip = 2/(Δr(2n + ξ_p)) S_z(ξ_p) S_z(η_p) | uGIMP T_ip = 평면 uGIMP ÷ r_p |
| (28) | `eq_28_truncated_Tip_node_at_origin.png` · p.133 | T^(0) = (1/Δr)(4/(l_p + x_p) − 1) S_z(η_p) (0 < ξ_p < l_p) | 축 노드 T (x_p = ξ_p 인쇄 · §12) |
| (29) | `eq_29_truncated_Tip_first_node.png` · p.133 | T^(1) = (1/Δr) S_z(η_p) (−2 < ξ_p < −2 + l_p) | 첫 노드 T |
| (30) | `eq_30_cpdi_axisym_Sip_integral.png` · p.134 | S_ip = (1/(A_p⟨r_p⟩))∫ r (Σ_α M_α N_i(r_p^(α))) dr dz | ★ CPDI — N_i 를 모서리 넷 보간으로 |
| (31) | `eq_31_cpdi_domain_vectors_from_F.png` · p.134 | d_1 = (F_rr Δr, F_zr Δz)/4 · d_2 = (F_rz Δr, F_zz Δz)/4 | 평행사변형 반 벡터 (Δr = Δz 일 때만 F 로 실어 나름과 같음 · §12) |
| (32) | `eq_32_parallelogram_natural_coordinates.png` · p.134 | (r, z) = r_p + ρd_1 + ζd_2 = Σ_α (r_α, z_α) M_α(ρ, ζ) | 자연 좌표 (등매개 4 절점) |
| (33) | `eq_33_cpdi_Sip_parent_integral.png` · p.134 | S_ip = (1/(A_p⟨r_p⟩))∫∫ (Σ r_α M_α)(Σ M_α N_i(r_p^(α))) \|J\| dρ dζ | CPDI 형상 함수 (부모 좌표) |
| (34) | `eq_34_jacobian.png` · p.135 | J = [[d_1r, d_1z], [d_2r, d_2z]] | 자코비안 (\|J\| = A_p/4) |
| (35) | `eq_35_cpdi_axisym_Sip_closed_form.png` · p.135 | S_ip = ¼ Σ (1 ± (d_1r ± d_2r)/(3r_p)) N_i(r_p^(α)) | ★ 축대칭 CPDI 닫힌 꼴 (카드 수치 확인) |
| (36) | `eq_36_cpdi_axisym_Gip_integral.png` · p.135 | G_ip = (1/(A_p⟨r_p⟩))∫∫ (Σ r_α M_α)(Σ J⁻¹ ∂M_α N_i) \|J\| dρ dζ | CPDI 기울기 (부모 좌표) |
| (37) | `eq_37_cpdi_axisym_Gip_closed_form.png` · p.135 | G_ip = (1/A_p)[r 성분 (d_1z ± d_2z ± β/(3r_p)) · z 성분 (d_1r ± d_2r)(1 ± …/(3r_p))] | ★ 축대칭 CPDI 기울기 닫힌 꼴 (카드 수치 확인) |
| (38) | `eq_38_beta_definition.png` · p.135 | β = d_1r d_1z − d_2r d_2z | 식 37 의 보조 항 |
| (39) | `eq_39_cpdi_axisym_Tip.png` · p.135 | T_ip = (1/(4r_p)) Σ_α N_i(r_p^(α)) | CPDI T_ip = 평면 CPDI ÷ r_p |
| (40) | `eq_40_traction_edge1_line_integral.png` · p.136 | f_ip,1^(s) = (1/2π)∫ T N_i dS = T\|d_1\|∫ (g(ρ)·(1,0)) (Σ M_α(ρ,−1) N_i) dρ | 견인 변 1 선적분 (dS = 2πr\|d_1\|dρ) |
| (41) | `eq_41_traction_edge1_cpdi.png` · p.136 | f_ip,1^(s) = \|d_1\|[(r_px − d_2x − d_1x/3) N_1 + (r_px − d_2x + d_1x/3) N_2] T | ★ 축대칭 견인 변 1 (카드가 식 40 에서 다시 유도) |
| (42) | `eq_42_traction_edge2_cpdi.png` · p.136 | f_ip,2^(s) = \|d_2\|[(r_px + d_1x − d_2x/3) N_2 + (r_px + d_1x + d_2x/3) N_3] T | 견인 변 2 |
| (43) | `eq_43_traction_edge3_cpdi.png` · p.136 | f_ip,3^(s) = \|d_1\|[(r_px + d_2x + d_1x/3) N_3 + (r_px + d_2x − d_1x/3) N_4] T | 견인 변 3 (§4.2 시험의 하중 변) |
| (44) | `eq_44_traction_edge4_cpdi.png` · p.136 | f_ip,4^(s) = \|d_2\|[(r_px − d_1x − d_2x/3) N_1 + (r_px − d_1x + d_2x/3) N_4] T | 견인 변 4 |
| (45) | `eq_45_traction_edge1_ugimp.png` · p.137 | f_ip,1^(s) = d_1x[(r_px − d_1x/3) N_1 + (r_px + d_1x/3) N_2] T | uGIMP 견인 변 1 (d_1 = (l_pΔr/2, 0)) |
| (46) | `eq_46_traction_edge2_ugimp.png` · p.137 | f_ip,2^(s) = d_2y(r_px + d_1x)[N_2 + N_3] T | uGIMP 견인 변 2 |
| (47) | `eq_47_traction_edge3_ugimp.png` · p.137 | f_ip,3^(s) = d_1x[(r_px + d_1x/3) N_3 + (r_px − d_1x/3) N_4] T | uGIMP 견인 변 3 |
| (48) | `eq_48_traction_edge4_ugimp.png` · p.137 | f_ip,4^(s) = d_2y(r_px − d_1x)[N_1 + N_4] T | uGIMP 견인 변 4 |
| (49) | `eq_49_planar_traction_edge1_line_integral.png` · p.137 | f_ip,1^(s) = ∫ T N_i dS = T\|d_1\|B ∫ (Σ M_α(ρ,−1) N_i) dρ | 평면 견인 선적분 (두께 B) |
| (50) | `eq_50_planar_traction_edge1.png` · p.137 | f_ip,1^(s) = \|d_1\|B[N_1 + N_2] T | 평면 견인 변 1 |
| (51) | `eq_51_planar_traction_edge2.png` · p.137 | f_ip,2^(s) = \|d_2\|B[N_2 + N_3] T | 평면 견인 변 2 |
| (52) | `eq_52_planar_traction_edge3.png` · p.137 | f_ip,3^(s) = \|d_1\|B[N_3 + N_4] T | 평면 견인 변 3 |
| (53) | `eq_53_planar_traction_edge4.png` · p.137 | f_ip,4^(s) = \|d_2\|B[N_1 + N_4] T | 평면 견인 변 4 |
| (54) | `eq_54_contact_normal_volume_gradient.png` · p.138 | ‖n_i,a‖n_i,a = −∇V_a(x_i) = Σ_{p∈a} V_p G_ip | 부피 기울기 법선 (축대칭에서 틀림 · 부호 §12) |
| (55) | `eq_55_contact_normal_area_gradient_axisym.png` · p.139 | ‖n_i,a‖n_i,a = −∇A_a(x_i) = Σ_{p∈a} A_p G_ip | ★ 축대칭 접촉 법선 = r–z 면적 기울기 (체크리스트 4) |
| (56) | `eq_56_conduction_weak_form.png` · p.139 | ∫ (∇·k∇T + q − ρC_p ∂T/∂t) w dV | 열 전도 약형 |
| (57) | `eq_57_conduction_divergence_theorem.png` · p.139 | ∫_∂Ω (w k∇T)·n̂ dS = ∫ (∇w·k∇T + qw − ρC_p w ∂T/∂t) dV | 발산 정리 뒤 (q · ρC_p 부호 §12) |
| (58) | `eq_58_nodal_temperature_rate.png` · p.139 | M_i dT_i/dt = f^(g) + f^(s) + f^(e) | 노드 열 수지 |
| (59) | `eq_59_nodal_heat_capacity_temperature.png` · p.139 | M_i = Σ m_p C_p S_ip · T_i = (1/M_i) Σ m_p C_p T_p S_ip | 노드 열용량 · 온도 |
| (60) | `eq_60_conduction_flux_source_boundary_terms.png` · p.139 | f^(g) = −Σ V_p k∇T_p·G_ip · f^(s) = Σ V_p q_p S_ip · f^(e) = ∫ N_i Φ dS | 전도 · 열원 · 경계 유속 |
| (61) | `eq_61_particle_temperature_gradient.png` · p.140 | ∇T_p = Σ_i T_i G_ip | 입자 온도 기울기 |
| (62) | `eq_62_particle_temperature_update_rate.png` · p.140 | T_p^(k+1) = T_p^(k) + Δt Σ_i (dT_i/dt) S_ip | ★ 입자 온도는 비율로 갱신 (T_i 외삽 금지 = 수치 전도) |
| (63) | `eq_63_radial_compression_deformation_gradient.png` · p.140 | F = diag(1 + ε_rr, 1, 1 + ε_rr) | 시험 1 — 균일 반지름 압축 (z 구속) |
| (64) | `eq_64_neohookean_energy.png` · p.140 | W = (K/2)[½(J² − 1) − ln J] + (G/2)(Ī₁ − 3) | Neo-Hookean 에너지 |
| (65) | `eq_65_isochoric_first_invariant.png` · p.140 | Ī₁ = (B_xx + B_yy + B_zz)/J^{2/3} | 등적 첫 불변량 (B = FFᵀ) |
| (66) | `eq_66_exact_sigma_rr_theta.png` · p.140 | σ_rr = σ_θθ = ((J − 1)/J)((K/2)(J + 1) + G₁/(3J^{2/3})) | ★ 정확해 (G₁ = G · §12) |
| (67) | `eq_67_exact_sigma_zz.png` · p.140 | σ_zz = ((J − 1)/J)((K/2)(J + 1) − 2G₁/(3J^{2/3})) | ★ 정확해 |
| (A.1) | `eq_A1_planar_ugimp_Sz.png` · p.146 | S_z(η) = ((4 − l_p)l_p − η²)/(4l_p) · (2 − \|η\|)/2 · (2 + l_p − \|η\|)²/(8l_p) · 0 | 평면 uGIMP ([11]) · l_p = 1 이면 2차 B-spline (카드 산술) |
| (A.2) | `eq_A2_planar_ugimp_dSz.png` · p.146 | dS_z(η) = −η/(2l_p) · −sgn(η)/2 · −sgn(η)(2 + l_p − \|η\|)/(4l_p) · 0 | 평면 uGIMP 기울기 (조건의 ξ_p = \|η\| · §12) |

**근거 글 크롭 20 장** (카드가 인용한 문장의 문단만 · 300 dpi · 파일 이름의 pN = PDF 쪽): `txt_p1_header_summary_received_keywords.png` (서지 · 요약 · 접수일 · 키워드) · `txt_p1_p2_only_axisym_mpm_dirac_artifacts.png` · `txt_p2_key_changes_cylindrical_integration.png` · `txt_p3_dF_higher_order_terms_rotation.png` · `txt_p3_p4_classic_recovered_main_differences.png` · `txt_p4_ugimp_undeformed_domain_regular_grid.png` · `txt_p5_partition_of_unity_origin_truncation_fig2.png` · `txt_p8_ugimp_50pct_strain_cpdi_deformed_domain.png` · `txt_p9_p10_cpdi_corner_cross_origin_shrink.png` · `txt_p10_evaluate_all_extensions_traction_rarely_done.png` · `txt_p11_planar_thickness_3d_six_faces.png` · `txt_p12_particle_forces_explicit_cracks_jintegral.png` · `txt_p12_p13_contact_normal_area_gradient_r0.png` · `txt_p14_conduction_no_extrapolation_diffusion.png` · `txt_p15_radial_compression_setup_classic_unstable.png` · `txt_p16_planar_shape_functions_extra_nodes_mirror.png` · `txt_p16_p17_fig7_84_88_93pct_four_reasons.png` · `txt_p18_traction_test_setup_cpdi_required.png` · `txt_p18_p19_penetration_setup_convergence_not_shown.png` · `txt_p19_conclusion_checklist.png`.

---

## 7. Post-processing

| 무엇 | 어떻게 | 우리에게 |
|---|---|---|
| 축 근처 입자 J | 처음 위치별 입자 J (상대 부피) + 전체 평균 J 의 가는 선 · 축에서 셀 셋 (7.5 mm) 만 | 축대칭 판의 첫 점검 그림 — 축 첫 셀의 입자가 평균선에서 벗어나는가 |
| 평균 응력 ↔ 정확해 | 모든 입자의 평균 σ_rr = σ_θθ · σ_zz 를 V/V0 에 대해 · 정확해 파선 | 정확해 단위 시험 (식 66–67) 의 보고 꼴 |
| 하중 변 근처 입자 응력 | 하중 변에서의 처음 거리별 입자 σ_zz · 지정 응력 점선 | 판 · 하중 경계의 가장자리 인공물을 보는 그림 |
| 실험 대조 | 코 · 꼬리 위치 시간 곡선 (선 = MPM · 기호 = 실험) | 오차 지표 없이 겹침만 — 우리 보고에는 차 · 실험 흩어짐을 같이 |
| **이 카드의 판독** (논문 밖) | 벡터 그림 경로 → 틀 모서리 · 눈금으로 축 사상 → 표지 중심 (네모 · 원 = 상자 중심) · Fig. 10 선 = 베지어 곡선을 표본화해 실험 시각에서 선형 보간 → `digitized.csv` | `[판독]` 의 출처 — 같은 PDF 가 있으면 다시 낼 수 있다 |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | 이 논문 | 우리 DEM | 우리 MPM |
|---|---|---|---|
| 기법 | 명시적 GIMP 계열 MPM (uGIMP · CPDI) · 축대칭 r–z | LIGGGHTS 구 입자 · hooke/hysteresis [우리 기록] | 명시적 MLS-MPM (Taichi · 2차 B-spline) 2D · 3D [우리 기록 · `hu2018_…` 카드] |
| 차원 | r–z 2D = 3D 회전체 (축대칭 하중만) | 3D | 2D (평면) · 3D [우리 기록] |
| 보간 | 선형 격자 + 입자 영역 평균 (r 가중) · 축에서 영역 자름 | — | 2차 B-spline (= 평면 uGIMP l_p = 1 [카드 산술 §4-10]) |
| 재료 | Neo-Hookean E 2300 MPa · ν 0.33 (가상) · Johnson–Cook 금속 | 탄성–이력 접촉 · E_eff 1.35 GPa (18 배 연화) · 순수 SE Heckel P_y 138 MPa [우리 기록] | J2 소성 · E 1.53 GPa · ν 0.49 (K 25.5 GPa) · σ_y 0.30 GPa [우리 기록] |
| 변형 | 부피 압축 84–93 % (J 16 → 7 %) · 인장 50 % · 관통 | 겹침 | 순수 SE · 복합 압밀 (기공 수십 % → 10 % 급) [우리 기록] — 고체 SE 자체의 부피는 거의 안 줄음 (K 25.5 GPa) |
| 응력 크기 | 원판 정확해 −12 GPa (J 16 %) · 견인 1000 MPa | 300 MPa 까지 | 300 MPa 까지 |
| 하중 | 강체 입자 일정 속도 (원판) · 견인 / 입자 힘 (원기둥) · 1.70 km/s 충돌 | 판 | 판 Mach 0.01–0.03 [우리 기록] |
| 해상도 | 셀 2.5 · 2 · 0.25 mm · 방향당 2 · 셀당 4 | 해당 없음 | 침대별 d_h/dx 점검 · 격자 사다리 [우리 기록] |
| 접촉 · 탈압 | 다물질 접촉 정식화만 · 탈압 없음 | 접촉 법칙 · 분리 | 한 속도장 (붙음) · AM 얼림 [우리 기록] |
| 검증 | 정확해 (원판) · 지정 응력 (견인) · 실험 (관통) | 실험 기공 (따로 보정) | 실험 기공 · 형상 (따로 보정) |

- 랩 기준 (순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정하지 않음): **이 논문에 기공 · 밀도 값이 없어 나란히 놓을 숫자 0 개.**  논문의 밀도 값 (텅스텐 17.6 · 강 7.85 g/cc · Table I) 은 금속 — 랩 표준과 다른 문헌 값 · 비교 대상 아님.
- 재료 값의 자릿수 (판정 아님): 시험 재료 E 2300 MPa · ν 0.33 ↔ 우리 MPM E 1.53 GPa · ν 0.49 · 우리 DEM E_eff 1.35 GPa — 같은 GPa 자릿수지만 구성식 (Neo-Hookean 초탄성 ↔ J2 소성 ↔ 접촉 법칙) · 뜻 (가상 시험 재료 ↔ 연화한 유효 강성) 이 다르다.

### 8-2. 전이되는 것 / 안 되는 것

| | 내용 |
|---|---|
| **전이 (방법)** | ① 축대칭 GIMP 식 (r 가중 S_ip · G_ip · 후프 T_ip · 라디안당 질량 · 후프 변형률) ② 축 r = 0 처리 (자름 · 축 노드 · r 속도 0 · 넘으면 정지) ③ 확장마다 바꿀 곳 (견인 r 가중 · 입자 힘 라디안당 · 면적 기울기 법선 · 축 성분 0 · 노드 면적 두 배 · 열 유속 라디안당) ④ 정확해 단위 시험 (균일 반지름 압축 · 식 63–67) ⑤ 체크리스트 9 항 ⑥ 평면 견인력 식 (49)–(53) |
| **전이 (경고)** | ⑦ 평면 형상 함수를 r–z 에 그대로 쓰면 축 첫 셀 오차 (Fig. 6) ⑧ 입자 힘 하중은 가장자리 낮음 + 면적 변화 드리프트 (Fig. 8) ⑨ uGIMP (영역 고정) 는 인장 50 % · 압축 88 % 에서 깨짐 ⑩ 회전이 크면 dF 를 두 항으로 자르면 부족 ⑪ 스칼라 장 (온도) 은 노드 외삽이 아니라 비율로 갱신 |
| **전이 안 됨** | 모든 값 (가상 Neo-Hookean · 금속 · 관통) — 우리 압밀의 응력 · 기공 · 반력 대조값이 아니다.  3D 대조 · 비용 · 접촉 · 탈압 · 구 · 분말에 대해서는 **아무 값도 없다** |

### 8-3. frame 판정

- **frame [5]**: MPM 쪽 절반 — 그중 **차원 축약 (회전체) 의 수치 기반**을 다룬다.  형상 변화 · 소성 흐름의 물리 결과는 관통 하나 (정성 그림 + 위치) 뿐.
- **frame [4]**: 실험 대조 = 관통 위치 하나 (맞춘 값 0 · 상수는 Anderson 외 [21] 의 값) · 나머지는 **코드 검증** (정확해 · 지정 응력).  보정 · 교차검증 근거로 쓰지 않는다.
- 연화 틀 (frame [2]) 과 중립.

---

## 9. 깊은 통찰

① **"축대칭이면 2D 비용으로 3D 답" 은 조건부다 — 조건은 축이다.**  같은 원판 · 같은 압축에서 축 첫 입자의 J 가 형상 함수 · 축 처리만으로 6.52 · 16.02 · 16.31 · 16.48 · 17.48 · 20.12 · 23.33 % 로 갈린다 [판독 · Fig. 5 · 6].  U1 (구 하나 누르기) · U3 (구–블록) 에서 하중이 모이는 곳 (꼭지 · 접촉 중심) 이 바로 축이다 → 축대칭 판의 첫 시험은 '축 근처 입자가 평균과 같은가' 여야 한다 [카드 추론].

② **축대칭 형상 함수는 축에서 셀 몇 개만 평면과 다르다 — 그런데 거기서 결과가 망가진다.**  S_r = 평면 + 1/(2n_i + ξ_p) 항이라 n = 100 에서 차 2 × 10⁻⁴ · n = 1000 에서 2 × 10⁻⁵ [카드 산술].  안 자르면 r_p → 0 에서 특이 (2r_p/Δr = 0.05 에서 S_r(−1) = −0.30 · l_p = 1 이면 −1.43 [카드 산술]) — 지지가 넓을수록 (= 우리 2차 B-spline 쪽) 축 특이가 크다.

③ **영역 고정 보간 (uGIMP) 은 큰 변형에서 끝이 있다.**  인장 약 50 % (p.134 · p.144) · 압축 88 % (p.143) 에서 깨지고 영역을 F 로 실어 나르는 CPDI 가 약 93 % 까지 간다.  우리 2차 B-spline = 셀당 1 · 폭 고정 GIMP 의 가중 [카드 산술 · `bardenhagen2004_…` §4-8] 이라 같은 부류 (영역 추적 없음) 다 [카드 추론] — 순수 SE 압밀에서 SE 덩어리의 국소 변형이 이 범위에 닿는지는 우리 쪽에서 잰 적이 없다 [미확인].

④ **하중을 어디에 거느냐가 응력 판독을 바꾼다.**  같은 1000 MPa 를 견인으로 걸면 입자 응력 991.8–1004.1, 입자 힘으로 걸면 가장자리 574.5 · 안쪽 1149.5–1203.1 MPa [판독].  가장자리 반값 = 힘이 입자 영역에 퍼진 하중이 되기 때문 · 안쪽 +15–20 % = 처음 치수로 정한 힘이 수축한 면에 걸리기 때문 (저자 설명 p.144).  우리 판 반력 (wallP) 은 격자 반력이라 입자 힘과 다르지만, 판 바로 아래 입자 응력을 '하중 응력' 으로 읽을 때는 같은 부류의 가장자리 인공물을 의심한다 [카드 추론].

⑤ **법선을 만드는 장에 기하 아닌 가중이 섞이면 법선이 기운다.**  부피 기울기 법선이 축대칭에서 틀리는 까닭 = V_p ∝ r (p.139) · 밀도가 다른 물질끼리 질량 대신 부피 기울기를 쓰는 까닭도 같다 (p.138).  ⇒ 우리 후보 A′ (입자별 속도장) 의 법선을 정할 때 SE · AM 밀도 차 (질량 기울기) · 축대칭 r 가중 · 셀 경계의 물질점 수 차 모두를 '기하가 아닌 가중' 으로 의심한다 [카드 추론].

⑥ **'3D 로 바로 확장된다' 는 견인력 한 문장이다.**  이 논문은 r–z 만 계산했다 — 3D 와 견준 숫자 · 비용 숫자 0 개.  축대칭 판이 3D 판과 같은 답을 내는지는 우리 쪽에서 같은 해상도로 한 번 견줘야 선다 [카드 추론].

⑦ **변형 경사 갱신의 절단.**  *"in problems involving rotation (less common in axisymmetry, but possible in penetration), the k = 2 or higher terms are needed"* (p.129) — 우리 MLS-MPM 의 F ← (I + ΔtC_p)F 는 두 항 판이다 [다른 카드 `hu2018_…`] · 판에 닿아 구르는 · 미끄러지는 SE 덩어리처럼 회전이 큰 곳에서 점검 대상 [카드 추론].

⑧ **관통 '일치' 의 크기.**  MPM − 실험 (−0.11 … +0.13 cm) 이 거의 같은 시각 두 실험점 사이의 흩어짐 (0.03–0.10 cm) 과 같은 자릿수 [판독 · 카드 산술] — 정량 지표 없이 '좋은 일치' 로 적혔다.  우리 쪽 실험 대조 보고에는 실험 흩어짐을 같은 표에 둔다.

---

## 10. ★ 자세한 분석 — 우리 계획에 무엇을 주나

(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 축대칭 GIMP 정식화 + Neo-Hookean · 금속 시험 — **재료 · 하중 · 문제가 모두 우리와 다르다**.  기공 · 밀도 값이 없어 랩 표준과 나란히 놓을 숫자는 0 개.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 축대칭에서는 부피 · 질량이 **라디안당** (V_p · m_p = ρA_p⟨r_p⟩) — 축대칭 판으로 기공을 센다면 r 가중 부피로 [카드 산술] · 보고 꼴: 입자별 J + 평균 J 를 정확해 (16 %) 와 견줌 (Fig. 5) | 기공 연산자 · 기준 0 |
| **단계 1** (3D 메모리 · 장 수) | 축대칭 ↔ 3D 셀 수 비 = 4N_r (전체) · N_r (¼ 대칭) [카드 산술 · 3-5] · uGIMP 지지 = 노드 양쪽 1.25 셀 (l_p = 1/2) → 입자 하나가 방향마다 노드 2–3 개 · 2D 에서 최대 3 × 3 노드 [카드 산술] · T_ip 를 3D 기울기 벡터의 셋째 칸에 두는 저장 요령 (체크리스트 3) | 3D 메모리 · 장 수의 수치 0 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★ 축대칭 판을 둘 경우의 **고칠 곳 목록** (체크리스트 9 항) + 단위 시험 셋: **균일 반지름 압축** (정확해 식 66–67 · 축 근처 J 균일 · Fig. 5–7) · **끝 견인** (지정 응력 대비 · Fig. 8) · (관통 = 실험) | 우리 MLS-MPM 의 축대칭 꼴 (r 가중 B-spline 전달 · MLS 기울기) 은 없다 — §4-10 의 후보 (식 19–21 에 l_p = 1) 는 카드 산술 · 구현 판단은 하지 않는다 |
| **단계 3** (2D 접촉 표현 비교) | 축대칭에서 다물질 (입자별 속도장) 로 갈 때 바꿀 곳 = 법선뿐 (면적 기울기 · 축 성분 0 · 노드 면적 두 배 · p.138–139) | 접촉 계산 예 0 · 한 속도장 ↔ 입자별 속도장 비교 0 · 다입자 층은 축대칭이 아니다 |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 없음 — 단 큰 변형 한계 (uGIMP 88 % · CPDI 93 % · 인장 50 %) 와 회전 시 dF 절단 경고 | σ_y · 기공 값 없음 |
| **단계 5** (3D 복합 압밀) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | 없음 ('unload' 0) | — |
| **단계 7** (형상 · 피복 · 수송) | 흐름 밖: 열 · 확산을 같은 MPM 위에서 풀 때 입자 값은 노드 비율로 갱신 (외삽 = 수치 전도) · 구성식에는 노드 외삽 값 (p.140) | 수송 계산 예 0 |
| **후보 D0** (지금 DEM) | 없음 (DEM 0 회) | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 판 하중 방식의 원문 비교: 강체 입자 일정 속도 (§4.1) · 견인 변 적분 (CPDI · 식 40–48) · 입자 힘 (가장자리 반값 · 면적 드리프트 · Fig. 8) · 견인을 전체 좌표 / 변 방향에 묶는 두 선택 (p.137) | 판–입자 접촉 규칙 (미끄럼 · 분리) 0 |
| **후보 A** (AM 강체 + SE 한 속도장) | 강체 입자로 원판을 누른 예 (§4.1) — 강체 결합 식은 없음 | — |
| **후보 A′** (입자별 속도장 · 다물체 마찰) | 다물질 모드의 축대칭 수정 (법선 · 축 · 노드 면적 · 불완전 계면 넓이 [17]) — 원문 *"experience has shown that accurate determination of the normal is crucial to accurate contact simulations [6]"* | 마찰 · 분리 계산 예 0 |
| **후보 B · C · C′ · M0** | 없음 | — |
| **U0–U6** | **U1** (입자 하나 압축 · 지름당 셀 수): 축대칭이면 구 하나 = r–z 반원 · 같은 셀 수에서 지름당 셀이 3D 의 수십 배 [카드 산술 · 3-5] · 축 근처 처리 필요 (식 20–29).  **U3** (구–블록 누르기 · 떼기): 축대칭 문제 · 법선 수정 필요 (식 55) — 원문 예제 없음 (관통 = 동적 · 둘 다 변형).  **U2 · U4 · U5 · U6 · U0** 없음 | '지름당 셀 수' 규칙 · 누르기 · 떼기 · 잔류 압흔 0 |
| **R1–R7** | **R2** (미끄럼 · 분리) — 다물질 접촉 정식화 (stick · frictional · imperfect interface) 의 축대칭 수정만.  **R5** (맞춘 값은 모델마다 하나) — 이 논문은 맞춘 값 0 (상수는 문헌 · 정확해 검증).  **R6** (SE 형상 변형) — 축대칭에서 큰 변형 (압축 93 % · 인장 50 %) 까지 연속체 형상 변화를 계산.  **R7** (AM 파괴) — 명시 균열 (CRAMP) 은 축대칭에서 그대로 · 점착력 라디안당 · 축대칭 J 적분 미개발 | R1 · R3 · R4 0 |
| **결과 전 대조 항목** | 우리 코드의 **검증용** 정확해 (식 66–67 · J 16 % 에서 σ_rr −12.0 · σ_zz +3.40 GPa [카드 산술]) · 축 근처 J 균일성 기준 (Fig. 5) | 물리 대조값 0 |

- **재료 · 차원 · 조건 차이**: 축대칭 연속체 (원판 · 원기둥 · 봉) ↔ 3D 알갱이 침대 · Neo-Hookean 초탄성 (E 2300 MPa · ν 0.33) ↔ J2 소성 (E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa) · 부피 압축 84–93 % (재료 자체가 줄어듦) ↔ 알갱이 사이 기공이 주는 압밀 (고체 부피 보존 · K 25.5 GPa) · 응력 수 GPa–수십 GPa ↔ 300 MPa · 동적 관통 1.70 km/s ↔ 준정적 판 Mach 0.01–0.03.

**구체 행동 (전부 [카드 추론] · 결과 전 등록 대상 · 구현 판단 아님)**
1. **축대칭 판이 단계 2 의 선택지인지 정하기 전에** 체크리스트 9 항을 우리 MLS-MPM 의 부품 (전달 가중 · 내부력 · F 갱신 · 구성식 · 경계 · 다물질 법선) 에 하나씩 대응시켜 '바꿀 곳 목록' 을 적는다 — 특히 r 가중 B-spline 전달의 정의 (§4-10 · 이 논문엔 없음).
2. **축대칭 판을 둔다면 첫 단위 시험 = 이 논문의 균일 반지름 압축** — Neo-Hookean (E 2300 MPa · ν 0.33) 원판을 J 16 % 까지 · 축 근처 입자 J (Fig. 5 꼴) + 평균 응력 ↔ 식 (66)–(67) 을 결과 전에 등록.  우리 재료 (ν 0.49) 판을 한 번 더 (이 논문은 ν 0.33 만).
3. **U1 · U3 의 축대칭 ↔ 3D 한 번 대조** — 같은 구 · 같은 지름당 셀 수 (3D 가 감당하는 수) 에서 판 반력 · 접촉 반지름 · 축 근처 응력을 두 판으로 풀어 차이를 기록 (이 논문이 안 한 대조).
4. **판 하중 방식 기록** — 우리 판 (격자 경계 · 강체) 이 이 논문의 '강체 입자 일정 속도' · '견인' · '입자 힘' 중 어디에 가까운지 적고, 판 바로 아래 입자 응력을 판 반력과 함께 그려 가장자리 인공물 (Fig. 8 꼴) 을 본다.
5. **인용 한정**: "축대칭이면 3D 와 같은 문제" 를 쓸 때 *"기하 · 하중 · 경계 · 접촉이 모두 축대칭일 때 · 축 r = 0 처리 (자름) 를 전제로 · 원 논문은 3D 와 견주지 않았다"* 를 같이 적는다.

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | uGIMP 는 영역이 변형하면 정확도를 잃는다 — 큰 변형 인장 약 50 % 한계 | p.134 |
| 2 | 변형한 영역 위 적분은 1D 에서 쉽고 2D · 3D 에서 *"very difficult"* → CPDI 근사 | p.134 |
| 3 | CPDI 모서리가 거친 계산 · 반올림으로 r = 0 을 넘을 수 있다 (실제로 넘었다) · uGIMP 식 자름은 쓸 수 없어 줄인다 | p.135–136 |
| 4 | 견인 경계는 가장 정확하지만 거의 안 쓰인다 · 평면 견인 식도 문헌에 없었다 | p.136–137 |
| 5 | 입자 힘은 하중 근처에 비물리적 응력 요동 · 축대칭에서는 라디안당 + 위치 의존 | p.138 |
| 6 | 축대칭 J 적분은 완성된 결과가 없다 · 기존 이론은 반지름 방향 균열만 · *"in need of additional development"* | p.138 |
| 7 | 부피 기울기 법선은 축대칭에서 안 된다 · 축에서 면적 기울기 r 성분도 외삽으로는 0 이 아니다 | p.139 |
| 8 | 평면 형상 함수는 경계 처리를 아주 조심해야만 쓸 만하다 | p.142–143 |
| 9 | uGIMP 88 % · CPDI 약 93 % 압축에서 붕괴 | p.143 |
| 10 | uGIMP 는 50 % 인장 견인에서 불안정 · 일정 응력 견인은 CPDI 필요 | p.144 |
| 11 | 관통의 격자 수렴은 보이지 않음 (*"not shown"*) | p.145 |
| 12 | 입자가 r = 0 을 넘으면 계산을 멈추거나 r ≥ 0 으로 옮겨야 한다 | p.145 (체크리스트 9) |

---

## 12. 불확실 · PDF 에 없는 것 · 인쇄 어긋남

**A. 논문에 없는 것 ([미확인])** — §3-6 의 목록.  특히 ① 3D 대조 · 비용 ② Δt · 압축 속도 · 입자 수 ③ 관통의 두 물체 처리 ④ 격자 수렴 수치 ⑤ 접촉 · 균열 · 열 · 확산 계산 예 ⑥ 코드 이름.

**B. 카드가 식 · 그림에서 역산한 것 (논문의 주장이 아님)** — ① 식 (19) · (24) · (20)–(21) · (25)–(26) · (35) · (37) · (39) 의 수치 확인 ② 식 (41) 의 재유도 ③ 정확해 값 (J 16 · 12 · 9.3 · 7 %) ④ l_p = 1 에서 (A.1) = 2차 B-spline · (19)–(21) 의 r 가중 판 ⑤ 입자 수 · 셀 수 · 3D 셀 비 ⑥ Fig. 5–8 · 10 의 판독값.  전부 [카드 산술 · 판독 · 카드 추론].

**C. 인쇄 어긋남 · 읽을 때 걸리는 곳**
1. 식 (25) 의 적분 아래 끝이 *"ξ_p − l_p"* 로 인쇄 — 인쇄된 결과 −1/2 는 자른 영역의 아래 끝 0 에서 나온다 (인쇄대로 적분하면 ξ_p = 0.25 · l_p = 1/2 에서 −0.556) [카드 산술].  식 (20) 은 아래 끝 0 으로 인쇄돼 있다.
2. p.132 *"For n_i = −1, dS_r^(0)(ξ_p) = 0"* — 윗첨자 (0) 가 (−1) 이어야 (p.131 같은 꼴 문장은 *"S_r^(−1)(ξ_p) = 0"*) [렌더 확인].
3. 식 (28) 의 *"x_p"* — ξ_p (자른 영역 적분으로 (4/(l_p + ξ_p) − 1)/Δr 이 나온다 [카드 산술]) · 식 (27) 의 *"2n"* (n_i 의 아래첨자 빠짐) · 식 (27)–(29) 의 S_z(ξ_p) 는 'r 방향에 쓴 평면 함수' 의 뜻 [카드 판독].
4. 식 (31): *"d_1 = (F_rr Δr, F_zr Δz)/4 · d_2 = (F_rz Δr, F_zz Δz)/4"* — 처음 반 벡터 (Δr/4, 0) · (0, Δz/4) 를 F 로 실어 나르면 (F_rr Δr, F_zr Δr)/4 · (F_rz Δz, F_zz Δz)/4 [카드 산술 · CPDI 원전의 영역 갱신 r_1 = F r_1⁰ = [다른 카드] `sadeghirad2011_…` 식 21] — Δr = Δz 일 때만 같다 (이 논문 시험 셋은 모두 Δr = Δz).  또 /4 는 셀당 방향마다 입자 2 (l_p = 1/2) 를 가정 [카드 판독].
5. 식 (54) · (55): *"‖n_i,a‖n_i,a = −∇V_a(x_i) = Σ_{p∈a} V_p G_ip"* — 같은 기울기 외삽이면 Σ V_p G_ip = +∇V_a(x_i) (식 7 의 G_ip 로) 라 둘째 등호의 부호가 어긋난다 (바깥 법선 = −∇V) [카드 판독].
6. 식 (57): q · ρC_p 항의 부호가 식 (56) (= 0 으로 읽음) 과 반대 — 발산 정리로 옮기면 ∫_∂Ω w k∇T·n̂ dS = ∫ (∇w·k∇T − qw + ρC_p w ∂T/∂t) dV.  식 (58)–(60) 은 맞는 부호를 따른다 [카드 산술].
7. 식 (66) · (67) 의 *"G₁"* — 식 (64) 의 G 와 같다 (K · G 수치로 J 16 % 에서 σ_rr −12,000 · σ_zz +3,402 MPa · 부피 · 편차 항으로 따로 계산해도 같음) [카드 산술].
8. 식 (A.2) 의 조건 *"l_p ≤ ξ_p < 2 − l_p"* · *"2 − l_p ≤ ξ_p < 2 + l_p"* — \|η\| 여야 [카드 판독].
9. 체크리스트 (1) *"m_p = ρA_p r_p"* ↔ p.129 *"m_p = ρA_p⟨r_p⟩"* · (5) *"du_r/r"* ↔ 식 (14) *"du_r/r_p"* — 작은 표기 차 (영역을 자르지 않은 uGIMP 면 ⟨r_p⟩ = r_p [카드 산술]).
10. Fig. 1 위 눈금 줄의 노드 i+1 아래 ξ 글자가 *"−2"* — 아래 눈금 *"2 − l_p"* · *"2 + l_p"* 와 맞추면 2 [렌더 확인].
11. Fig. 2 · 3 캡션 *"The dotted red lines"* — 인쇄 색은 검정 계열 (빨강 없음) [렌더 확인] · Fig. 2 y 눈금 글자 −0.2 · 0.2 · 0.8 이 실제 −0.25 · 0.25 · 0.75 자리 (한 자리 반올림 · 경로 좌표) · Fig. 3 y 글자 *"−0.0"* · 두 캡션의 *"lines shows"*.
12. Fig. 7: 본문 *"plotted up to 84% compression"* ↔ 실선이 V/V0 ≈ 9.3 % (≈ 90.7 % 압축) 까지 [판독] — 본문은 uGIMP 88 % 붕괴 · CPDI 93 % 붕괴 시작이라 적는다 (그림의 선이 어느 방법인지 · 왜 84 % 를 넘는지 [미확인]).
13. Fig. 5 ↔ Fig. 6 의 같은 이름 *"uGIMP (truncated)"* 의 5 · 6 번째 입자: 16.78 · 16.67 ↔ 16.57 · 16.53 % [판독] (처음 넷은 차 ≤ 0.013 = 판독 정밀도) — 다른 런인지 [미확인].
14. Fig. 5 의 평균 J 선 16.41 % [판독] ↔ 인쇄된 최종 J 16 % — 평균이 공칭보다 0.4 %p 높다 (까닭 [미확인]).
15. 캡션 · 본문 오탈자: Fig. 6 *"dsahed"* · Fig. 8 *"horiztonal"* · Fig. 9 *"show show"* · p.131 *"is required have nodes"* · p.130 *"those shape function are"* (렌더 확인) / p.136 *"the affect of axisymmetry"* · p.138 *"in principal"* · p.139 *"lose is connection"* · *"base it in on"* · *"close the the"* · p.142 *"different then"* · p.146 *"an subcontract"* (글자 층).
16. 쪽 머리 · 바닥: 첫 쪽 머리글 *"2015; 101:127–147"* ↔ 쪽마다 바닥글 *"2014; 101:127–147"* · 소속 *"Rasharon, TX"* (인쇄 그대로).
17. 참고문헌: [12] *"Sulsky D, Schreyer HK. Axisymnmetric form …"* (철자 그대로) · [1] *"118:179–186"* ↔ `bardenhagen2004_…` §15 의 같은 논문 *"pp. 179–196"* [다른 카드] · [11] *"5:477–496"* ↔ 그 논문 머리글 *"pp.477-495"* [다른 카드 §0-1] · [19] 제목이 *"… and high."* 에서 끝남 · [20] *"Wilkens ML"* (철자 그대로).

**D. 정본의 다른 카드와의 어긋남 (카드는 고치지 않음)**
- 값 · 서지 어긋남 없음.  `gritton2017_…` L597 (§9 ⑩) · L624 (§10 행동 4) 의 [카드 추론] 은 원문 (이 논문) 과 맞되 **한정어가 필요**하다 — '2D → 3D 문제가 사라진다' · '그대로 3D 문제' 는 기하 · 하중 · 경계 · 접촉이 모두 축대칭이고 축 처리 (자름 · 축 노드) 를 할 때만이며, 이 논문은 U1 · U3 같은 예제 · 3D 대조 · 비용을 싣지 않는다 (§0-1).

---

## 13. 인용 가능 문장 (덱 · 원고용)

- "GIMP 를 원통 좌표로 다시 유도하면 형상 함수와 기울기에 반지름 가중이 들어가고 후프 응력 · 후프 변형률을 위한 새 함수 T_ip 가 필요하다 — 점 질량 MPM 의 축대칭 판과 달리 평면 형상 함수를 그대로 쓸 수 없다 (Nairn & Guilkey, Int. J. Numer. Meth. Engng 101, 127, 2015 · 식 6–8 · p.130)."
- "축대칭 GIMP 에서 입자 영역이 축을 넘으면 형상 함수가 특이해지므로 영역을 r = 0 에서 자르며, 원판 균일 압축 (J 16 %) 에서 자르지 않으면 축 첫 입자의 J 가 6.5 % (uGIMP) · 20.1 % (CPDI) 로 틀렸다 (같은 문헌 Fig. 5 · 그림 판독)." — 판독값임을 밝힌다.
- "평면 형상 함수를 축대칭 계산에 그대로 쓰면 축에서 큰 오차가 생기고 (첫 입자 J 23.3 % ↔ 16 %), 축 바깥 노드에 거울 경계를 주어야 줄어든다 (같은 문헌 Fig. 6 · p.142)."
- "같은 문헌은 영역을 고정하는 uGIMP 가 압축 88 % 에서, 영역을 변형 경사로 실어 나르는 CPDI 가 약 93 % 에서 무너지고 (p.143), uGIMP 는 50 % 인장에서 불안정해 큰 변형과 일정 응력 견인에는 CPDI 가 필요하다고 적는다 (p.144)."
- "축대칭 다물질 접촉에서는 부피 기울기 대신 r–z 면적 기울기로 법선을 구하고, 축 노드의 법선 r 성분을 0 으로 두며, 접촉 판정의 노드 면적을 축에서 두 배로 한다 (같은 문헌 식 55 · p.139 · 체크리스트 4)." — 계산 예는 없다는 한정을 붙인다.
- "같은 문헌은 3D 계산과 견주지 않았고 계산 비용을 적지 않았다." — 축대칭 = 3D 대체라는 문장에 붙인다.

## 14. 기법 미니 용어집

- **축대칭 (axisymmetry)** — 회전체 + 축대칭 하중 · 경계 → 원통 좌표 (r, θ, z) 에서 θ 에 무관 → r–z 단면 하나만 계산 (양은 라디안당).
- **후프 (hoop) 성분** — θθ 방향 응력 · 변형률 (원주 방향).  반지름 변위 u_r 이 있으면 ε_θθ = u_r/r 가 생긴다.
- **GIMP · uGIMP** — 물질점에 영역 (입자 특성 함수 χ_p) 을 주어 격자 함수를 평균 (`bardenhagen2004_…`).  uGIMP = 영역을 처음 크기로 고정하고 입자와 함께 옮김.
- **CPDI** — 영역을 변형 경사 F 로 평행사변형으로 실어 나르고 격자 함수를 모서리 넷의 값으로 보간 (`sadeghirad2011_…`).
- **S_ip · G_ip · T_ip** — 축대칭 형상 함수 · 기울기 (r 가중 평균) · 후프 항 함수 (r 가중 없는 평균 ÷ ⟨r_p⟩ = 대략 평면 함수 ÷ r_p).
- **l_p** — 무차원 단위 (셀 폭 = 2) 의 입자 영역 반폭 · 셀당 방향마다 입자 2 개면 l_p = 1/2 · 1 개면 1.
- **n_i** — 노드 i 의 반지름을 셀 폭으로 나눈 수 (r_i/Δr) · 축 노드 = 0.
- **영역 자름 (truncation)** — 축을 넘는 영역 부분을 잘라 r ≥ 0 안의 영역으로 다시 적분 (uGIMP) · CPDI 는 평행사변형을 줄임 (shrink).
- **분할의 합 (partition of unity)** — 모든 노드 형상 함수의 합 = 1.
- **extra node · ghost node** — 계산 영역 바깥 노드 (축 바깥 r = −Δr) · 평면 형상 함수에서는 입자 영역이 걸쳐 쓰인다.
- **거울 경계 (mirror BC)** — 축 바깥 노드의 r 속도 = 거울 노드 (r = Δr) 의 r 속도 × (−1) · 3D 의 값을 흉내.
- **견인 (traction) 경계** — 물체 면에 단위 넓이당 힘 · 이 논문은 CPDI 변 위의 선적분으로.
- **입자 힘 경계** — 경계 입자 중심에 힘을 줌 · 입자 영역에 퍼진 하중이 되어 가장자리 인공물.
- **다물질 모드 (multimaterial mode)** — 물질마다 속도장을 따로 두고, 둘 이상이 닿는 노드에서 접촉 물리로 운동량을 고침.
- **CRAMP** — 노드–입자 선이 균열면을 넘는지로 속도장을 나누는 명시 균열 MPM (Nairn 2003 · ref. [9]).
- **J 적분** — 균열 끝 에너지 해방률의 경로 무관 적분 (Rice 1968 · ref. [14]).
- **Neo-Hookean** — 큰 변형 초탄성 (식 64) · K · G 두 상수.
- **Johnson–Cook · Mie–Grüneisen** — 금속의 변형률 · 속도 · 온도 의존 흐름 응력 / 충격 압력–부피 관계 (식은 이 논문에 없음 · ref. [19] · [20]).
- **flash x-ray** — 짧은 X선 섬광으로 관통 중인 봉의 위치를 찍는 실험법 (Anderson 외 [21]).

## 15. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 · 이유 한 줄 · 정본 카드 없음 확인 = `papers/` 파일 목록 + grep)

- 12. Sulsky D, Schreyer HK. Axisymnmetric form of the material point method with applications to upsetting and Taylor impact problems. Computer Methods in Applied Mechanics and Engineering 1996; 139:409–429. — 점 질량 축대칭 MPM 원전 · 원기둥 업세팅 (압축 큰 소성 변형) · 이 논문이 *"first, and thus far, only"* 라 한 판 (질문 g · l · f) — `wishlist.md` 에 이미 있음 (batch 의 다른 카드에서).
- 6. Lemiale V, Hurmane A, Nairn JA. Material point method simulation of equal channel angular pressing involving large plastic strain and contact through sharp corners. Computer Modeling in Engineering & Sciences 2010; 70(1):41–66. — MPM 큰 소성 변형 + 날카로운 모서리 접촉 · *"accurate determination of the normal is crucial"* 의 근거 (질문 l · f · 후보 A′).
- 17. Nairn JA. Modeling of imperfect interfaces in the material point method using multimaterial methods. Computer Modeling in Engineering & Sciences 2013; 92(3):271–299. — 다물질 MPM 의 불완전 계면 법칙 · 축대칭 계면 넓이 유도가 여기 있다 (질문 f · 흐름 밖: 계면 저항).
- 4. Bardenhagen SG, Brackbill JU. Dynamic stress bridging in granular material. Journal of Applied Physics 1998; 83:5732–5740. — 입상체 MPM 의 마찰 접촉 원전 하나 ([4–6]) · 응력 다리 (질문 d · f).
- 9. Nairn JA. Material point method calculations with explicit cracks. Computer Modeling in Engineering & Sciences 2003; 4:649–664. — CRAMP 원전 · 축대칭에서 그대로 쓰인다 (R7 AM 파괴 · 질문 f).

## 16. 관련 카드

- `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` — GIMP 원전 (이 논문 ref. [11] · 출발점) · 셀당 1 · 폭 고정 = 2차 B-spline (§4-10).
- `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` — CPDI 원전 (ref. [3]) · 영역 갱신 r_1 = F r_1⁰ (§12-C 4 의 대조).
- `gritton2017_mpm_chemomechanical_coupling_silicon_anode` — 이 논문을 ref. [41] (열 확산 선례 [41–43]) 로 인용 · 기둥을 축대칭 대신 3D 로 (고른 의도의 출처 · §0-1).
- `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 이 논문 ref. [5] · 다물질 마찰 접촉 · 분리 판정.
- `bardenhagen2000_mpm_granular_multibody_frictional_contact` — 같은 계열 다물체 마찰 접촉 원전.
- `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — 명시 균열 MPM (Nairn 계열) 과 DFG 분할 · GIMP · CPDI 를 나란히.
- `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MLS-MPM 이산화 (2차 B-spline · MLS 대용 기울기) 의 원전 — §4-10.
- `devaucorbeil2020_mpm_after_25_years_review` — MPM 리뷰 · 오픈 코드 목록 (NairnMPM).
- `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` — 입자 압밀 MPM (평면 2D 원판) — 축대칭 판과 견줄 2D 꼴.
- `bardenhagen2005_mpm_foam_densification_simulation` — GIMP 로 3D 압축 (공칭 90 %) 을 푼 선례 · 큰 압축에서의 보간 한계 (§9 ③ 과 함께).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

# MPM 에서 속도장을 알갱이 수만큼 늘리지 않는 접촉 — 손상장 (또는 표면 표지) 의 기울기로 노드마다 물질을 두 속도장으로 나눠 마찰 접촉 · 분리 · 파괴 · '자기 접촉' ★★★ 후보 A′ 의 '장 2 개' 길 + R7 (AM 파괴) 부품 — Homel & Herbold (IJNME 2017)

> slug `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` · DOI `10.1002/nme.5317` · type `MPM (명시적 CPDI-MPM · 손상장 / 표면 표지장의 기울기로 노드마다 두 속도장 분할 (DFG partitioning) → 마찰 접촉 · 분리 · 파괴 · 자기 접촉 — 2D 평면변형 검증 5 건 + 3D 시연 1 건 · 초탄성 + 스칼라 인장 손상 · 소성 없음)` · PDF `17._upload_0c6f3c50.pdf` (⚠ 조판 PDF 가 아니라 **출판사 웹 전문 페이지를 길게 캡처한 그림 두 장**을 감싼 2 쪽 PDF · 글자 층 없음 · 1저자 제공) · digested `2026-11-10` · status ✅
>
> ⚠ **먼저 읽을 것** — ① **원문 = 웹 전문 페이지 캡처 (PDF 아님).**  쪽 번호가 없으므로 이 카드는 위치를 **절 번호 · 식 번호 · 그림 / 표 / Algorithm 번호**로 단다.  캡처에 **없는 것**: 참고문헌 목록 (접힌 채 캡처됨) · 각주 본문 (‡ § ¶ 표지만 보임) · 저자 소속 · 접수 / 게재 확정일 · 키워드.  그래서 참고문헌 번호는 본문이 저자 이름을 같이 적은 것만 식별했고 나머지는 번호만 옮겼다.
> ② 재료는 단단한 초탄성 고체 (K 158.333 · G 73.077 GPa → E 190 GPa · ν 0.30 [카드 산술] — 어떤 실제 재료인지 밝히지 않으며, 파괴값은 다른 XFEM 해석 (Song 외) 에 맞춘 것 · §3.4 는 *"not meant to describe a particular material"*) + 인장 손상이다 — **LPSCl · NCM 이 아니다.  절대값 전이 0 건.**  가져오는 것은 알고리즘 · 검증 시험의 꼴 · 저자 스스로의 경고 · (2D 한정) 비용 비율뿐.
> ③ **소성 없음 · 준정적 압밀 없음 · 탈압 없음.**  하중은 전부 동적이다 (충격 20 · 33 m/s, 일정 견인력 200 · 650 MPa — 가하는 시간 이력은 미인쇄, 결과의 시간 척도 µs–ms).  **'DEM' · 'discrete element' 는 본문에서 한 번도 보지 못했다** [카드 정독 — 글자 층이 없어 전문 검색은 못 했다].
> ④ 정량 검증은 **전부 2D 평면변형**이다.  3D 는 그림 한 장 (Fig. 20) 이고 수치가 없다.
> ⑤ 자기 접촉 검증 (Fig. 8 · 9) 의 판정은 *"nearly identical"* · *"very similar"* — **눈 대조**다 (오차 노름 · 힘 비교 없음).  **한 노드에 셋 이상의 물체가 만나는 경우의 정량 시험은 없다** (정성 설명 한 문단 · §4-8).
> ⑥ 인쇄 어긋남이 여럿 있다 (법선 부호 규약 · Algorithm 3 의 22 행 · Table 1–3 의 값 · 시간-파괴 식) — §12 에 모았다.  구현 때 식을 그대로 베끼지 않는다.
> ⑦ 표지: `인쇄` = 본문 · 표 · 캡션에 적힌 값 · `[카드 산술]` = 인쇄값에서 산술로만 유도 (식 병기) · `[판독]` = 그림에서 읽은 값 (추세 전용) · `[미확인]` = 캡처에 없음 · `[카드 판독]` = 인쇄 어긋남에 대한 카드의 읽기 · `[우리 코드 판독]` · `[우리 기록]` · `[카드 추론]` = 논문 밖 판단.
>
> 짝 카드: `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 이 논문이 분할 **뒤에** 그대로 쓰는 접촉 알고리즘의 원전 (본문 *"identical to that for contact between predetermined material pairs as described by Bardenhagen et al. 42"*; 42 가 어느 판인지는 참고문헌 목록이 없어 [미확인]).  `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 같은 문제 ("격자 한 칸 = 속도 하나") 를 **강체 표면에 한해** 푼 다른 길 (CPIC).  `devaucorbeil2020_mpm_after_25_years_review` — 이 논문을 MPM 파괴의 세 접근 중 *mixed* (연속 손상 + 자기 접촉) 로 분류한 리뷰 카드 (그 카드와 `bucci2018_mechanical_instability_interface_delamination` 가 가리키던 원전이 이 카드다).

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

우리 MPM (`scripts/mpm3d_compaction.py`) 은 격자 속도장이 **하나**다 (`grid_v` · `grid_m` 한 벌 [우리 코드 판독 · 2808 행 · 파일 마지막 커밋 `cb5a6a445`]).  이 논문이 그 상태를 부르는 이름이 *single-field (SF)* 이고, 그 결과를 이렇게 적는다.

> *"The MPM algorithm outlined in Equations 1–10 computes the response for material in a single velocity field.  Within this velocity field, the method naturally produces a no-slip contact condition that prevents interpenetration between materials.  This behavior is similar to the response of an Eulerian hydrocode, which also assumes that each computational cell contains a single velocity gradient when multiple materials are present."* (§1.1.1)

> *"A single velocity-field MPM solution can produce artificial 'welding' of material interfaces or nonphysical localization when the constitutive response includes softening or damage 32."* (§1)

접촉을 넣는 전통 방식 (Bardenhagen 계열 = 우리 후보 A′) 은 **물체마다 속도장**을 둔다.  이 논문은 알갱이 계에서 그 길이 왜 막히는지를 적고 —

> *"The four-color theorem states that any 2-D domain can be partitioned to avoid edge-to-edge contact of matching fields with no more than four fields 45.  In 3-D, there is no analogous theorem limiting the number of required fields to ensure frictional contact between all entities, and even if the geometry can be initialized such that neighboring particles are in separate velocity fields, subsequent deformation and granular flow can change the contact points."* (§1.1.1)

— 대신 **입자에 실은 스칼라장 (손상 또는 표면 표지) 의 기울기 방향**으로 노드마다 물질을 **두 쪽**으로 나눈다.  장의 수가 알갱이 수와 무관해진다.

> *"In contrast, if a surface detection contact approach is used (such as the new approach described in Section 2.4), granular flow can be simulated from a single material group (divided into two velocity fields) with surface-particle flags as illustrated in Figure 2b."* (§1.1.1)

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| 후보 **A′** (입자마다 속도장) 의 장 수 · 메모리 문제의 출구 | 재료 묶음 하나를 노드마다 **두 장**으로 (Fig. 2b · §2.2 · §2.4 · Algorithm 1–3).  근거 문장: 4 색 정리 (2D) ↔ 3D 는 상한 없음 · N 장이면 접촉 쌍 N(N − 1) (§1.1.1) |
| "한 속도장 = 붙는다 · 가짜 소산" 의 제3자 진술과 **크기** | §1 *artificial 'welding'* · §1.1.2 *"a tensile member containing a single layer of failed (or even deleted) particles can still support a tensile load"* · Charpy 끝 에너지 SF 568 ↔ DFG 618 mJ (Δx 1 mm · [판독]) · Brazilian 평균 속도 SF ≈ 45 ↔ DFG ≈ 107 m/s (가장 거친 격자 · [판독]) |
| 단계 3 (2D 에서 **접촉 표현만 바꿔** 견주는 시험) 의 꼴 | Fig. 7–9: 같은 문제를 SF ↔ 미리 나눈 다중 장 ↔ 표면 표지 분할 세 가지로 — 다중 장 해를 '정답' 으로 삼는 검증 설계 |
| 조밀 알갱이 압밀에서 MPM 접촉이 기공률에 주는 계통 오차의 **저자 진술** | §4.2: 접촉은 셀 한 칸 안에서만 해상 → 비물리적 틈 → *"for compaction of granular materials … this could lead to a value of the continuum density that is inconsistent with the particle density.  This error decreases with mesh refinement"* |
| 조건 R7 (AM 파괴) — 깨진 뒤 파편끼리의 마찰 접촉 | 손상장 분할 + Weibull 크기 의존 강도 + Rankine 연화 / 시간-파괴 모델 (§2.7 · §3.4) |
| 비용 | 2D · 16 스레드: 입자 3.2 만–15 만에서 SF 대비 +30–50 % · 이웃 정렬 < 0.1 % (§3.5) — 3D 수치는 없음 |
| 소성 SE 의 준정적 압밀 · 탈압 · 기공률 | **없음** |
| 한 노드에 셋 이상 | 정성 설명뿐 (§2.2 끝) + *"they do not strictly prevent interpentrability for N > 2 fields"* (§1.1.1) |

### 0-2. 이 묶음의 네 질문 (DEM 한계 · 소성 · 2D/3D · 탈압)

| 질문 | 이 논문의 답 (원문 위치) |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | **말 없음.**  본문에서 'DEM' · 'discrete element' 를 보지 못했다 [카드 정독 · 참고문헌 목록은 캡처에 없음].  다른 방법 일반에 대한 말만 있다: *"A variety of computational methods to simulate fracture and large deformation have been developed for applications in solid mechanics, but each has its limitations with respect to either accuracy or robustness when simulating large-deformation fracture with subsequent frictional contact in complex 3-D geometries."* (§1) · *"This 'granular flow' phase occurs in fragmentation and comminution processes and can be exceedingly difficult to model with other numerical methods."* (§3.1) · *"… which cannot be solved adequately with traditional Eulerian, Lagrangian, or ALE/remapping schemes."* (§4.3).  한계를 직접 말하는 대상은 **MPM 의 한 속도장** (위 §0 인용) 과 **물체마다 속도장을 두는 MPM 접촉** (4 색 정리 · N(N − 1)) 이다 |
| (ii) 입자의 소성 · 큰 변형이 왜 어려운가 · 우회 · 비용 | 어렵다는 설명은 **없다** — 이 논문에 소성 계산이 없다 (초탄성 + 인장 손상).  큰 변형은 MPM 이 견딘다는 쪽의 말만 있다: *"The material state history is stored at the particles, so that advection errors are eliminated."* · *"The background grid is reset at each time step, so the method tolerates large deformation."* (§1.1) · *"by avoiding advection errors, it becomes possible to accurately use more sophisticated constitutive models for large-deformation solid mechanics.  However, for the examples presented herein, we use a relatively simplistic phenomenological model"* (§2.7).  비탄성은 한 마디 — 자기 접촉이 *"even if the solid material is undergoing large (potentially inelastic) deformation"* 에서도 선다는 **주장** (§3.1 · 시험 없음) 과, 연성 파괴에는 *"a non-local constitutive model 74 formulation"* 이 필요하다는 말 (§4.2).  우회 · 맞춘 값: 없음 (*"without requiring any parameter tuning"*, §3.2) — 다만 D̄^min · l^ch 는 저자 표현으로 *"can be tuned"* 인 수치 손잡이다 (§3.3).  비용은 §3-6 |
| (iii) 2D 인가 3D 인가 · 2D → 3D 전이 | **수치 예제 5 건 전부 2D 평면변형** (*"The 2-D computational examples in this work are all plane strain"*, §2.7).  방법 · 구현은 3D (*"the DFG-partitioning method is inherently 3-D, as is its implementation in the GEOS computational framework"*, §4) 이고 3D 그림 한 장 (Fig. 20) 은 *"included simply to demonstrate that the method is not limited to two dimensions"*.  2D → 3D 에서 달라지는 것으로 원문이 적은 것: ① 미리 나누는 장의 수 — 2D 는 4 색 정리, 3D 는 상한 없음 (§1.1.1) ② 핵 반경 · 특성 길이 = 셀 대각선 (2D √(Δx² + Δy²) · 3D √(Δx² + Δy² + Δz²)) ③ 평면변형에서도 입자 부피 (Weibull) 를 위해 두께를 정해야 함 ④ 비용 — *"Computational expense becomes an important factor when solving complex 3-D problems."* (§4).  2D 결과의 **물리량**을 3D 로 옮기는 것에 대한 말은 없다 |
| (iv) 압력을 뺄 때의 거동 | **다루지 않는다** ('unload' · 'rebound' · 'springback' 을 보지 못했다 [카드 정독]).  닿는 것은 둘: 접촉력을 다가올 때만 걸어 *"naturally allows separation of contact surfaces"* (§1.1.1 — 속도 판정) 와, 한 속도장에서는 실패한 층을 사이에 둔 부재가 **인장을 계속 전달한다**는 문장 (§1.1.2) |

---

## 1. 한 줄 요약

**KR:** MPM 에서 접촉 · 파괴에는 격자 노드에서 속도가 불연속일 수 있어야 하는데, 물체마다 속도장을 두는 전통 방식은 알갱이 · 균열이 많아지면 장 수 (3D 에는 상한 없음) 와 접촉 쌍 N(N − 1) 때문에 쓸 수 없고, 균열을 명시적으로 추적하는 방식은 3D 분기 · 합류에서 막힌다.  이 논문은 입자의 스칼라 손상 D_p 를 3차 핵 (반경 = 셀 대각선) 으로 합쳐 정규화한 **손상장 D̄(x)** 를 만들고, 그 **기울기 (DFG)** 를 입자 위치에서 구한 뒤, 노드에는 "얹히는 입자 중 기울기가 가장 큰 것" 을 대표값으로 주어 (Algorithm 1), 입자 기울기와 노드 기울기의 **내적 부호**로 입자를 노드마다 두 속도장 중 하나에 보낸다 (Algorithm 2).  두 장이 함께 있는 노드에서 분리 조건 (완전 손상 입자가 하나 이상 ∧ 장별 평균 손상의 작은 쪽 > D̄^min) 이 서면 Bardenhagen 식 마찰 접촉 (질량중심 속도 · 보정 법선 · Coulomb) 을 걸고, 안 서면 두 장을 질량중심 속도에 묶어 한 장처럼 다룬다 (Algorithm 3).  손상 자리에 **표면 표지 s_p** 를 넣으면 (max(s_p, D_p)) 처음에 한 묶음이던 재료의 표면끼리도 마찰 접촉 · 분리가 된다 — **자기 접촉**.  검증 (전부 2D 평면변형): 판 사이 빌릿 압축과 쐐기–원판–블록 문제에서 미리 나눈 다중 장 해와 눈으로 거의 같음 · Kalthoff–Winkler 균열 각 59.1° (XFEM 60° · 실험 70°) · 균열 속도 2.0 km/s · Charpy 에너지 수지에서 지정한 파괴 에너지 (354.1 mJ) 를 세 해상도에서 재현 · Brazilian 파쇄에서 파편 크기 · 속도의 격자 의존이 한 속도장 해보다 훨씬 작음.  비용은 2D 에서 +30–50 %.  한계는 저자가 적는다 — 접촉은 셀 한 칸까지만 해상되어 알갱이 압밀에서 밀도가 어긋나고, 장이 셋 이상이면 쌍별 힘이 침투를 엄밀히 막지 못한다.

**EN:** Homel and Herbold partition MPM material into two velocity fields *per grid node* using the gradient of a kernel-smoothed, normalized scalar damage field (cubic kernel, radius = grid-cell diagonal) evaluated at the particles: each node takes the gradient of the mapped particle with the largest gradient magnitude, and a particle is assigned to field 0 or 1 at that node by the sign of the dot product of the two gradients.  Where both fields carry mass and a separability condition holds (at least one fully damaged particle and the smaller field-averaged damage above a threshold D̄^min), the standard multi-field frictional contact (centre-of-mass velocity, corrected opposite normals, Coulomb limit, contact only when approaching) is applied; otherwise the two fields are tied to the centre-of-mass velocity.  Replacing damage by max(surface flag, damage) gives frictional "self-contact" between surfaces that start in a single material group, so the number of velocity fields no longer grows with the number of grains.  Implemented in the 3-D GEOS code with CPDI and domain scaling, the method is verified in 2-D plane strain only: two self-contact problems against the prescribed multi-field solution (visual agreement), the Kalthoff–Winkler test (crack angle 59.1° vs 60° XFEM and 70° experiment; crack speed 2.0 km/s), a Charpy-type energy balance (specified fracture energy recovered at three resolutions, while the single-field solution over-dissipates on coarse grids), and a Brazilian fragmentation/compaction problem (fragment sizes and velocities far less mesh dependent than single-field).  The added cost is 30–50 % for 3.2 × 10⁴–1.5 × 10⁵ particles in 2-D.  No plasticity, no quasi-static compaction, no unloading; contact is resolved only to one cell spacing, which the authors warn makes the continuum density inconsistent in granular compaction.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **Field-gradient partitioning for fracture and frictional contact in the material point method** |
| 저자 | **Michael A. Homel** (교신 — 이름 옆 편지 봉투 표시 [판독]) · **Eric B. Herbold** |
| 소속 | **[미확인]** — 캡처의 저자 줄에 소속이 없다.  감사의 글: *"performed under the auspices of the US Department of Energy by University of California, Lawrence Livermore National Laboratory"* |
| 저널 | **International Journal for Numerical Methods in Engineering, Volume 109, Issue 7 (17 February 2017), Pages 1013–1044** · *Research Article* · *First published: 11 June 2016* · *Copyright © 2016 John Wiley & Sons, Ltd.* (전부 캡처 머리에 인쇄) |
| DOI | **10.1002/nme.5317** (캡처에 `https://doi.org/10.1002/nme.5317` 인쇄 — 1저자 메모와 같음) |
| 키워드 · 접수 / 게재 확정일 | **[미확인]** (캡처에 없음) |
| 분량 | 본문 절 1–4 (번호 붙은 절 제목 22 개) · Fig. 1–20 · Table 1–4 · 번호 식 (1)–(27) (15a · 15b 포함 28 줄) · Algorithm 1–3 (10 · 10 · 32 행) · 참고문헌 **74 건 이상** (본문의 가장 큰 인용 번호 = 74 · 목록은 캡처에 없음) · 각주 표지 3 개 (‡ § ¶ — 본문 [미확인]) · 보충 자료 절은 보이지 않음 |
| 연구 유형 | 수치 방법 (MPM 의 접촉 · 파괴 알고리즘) + 2D 검증 예제 + 비용 측정.  실험 없음 (Kalthoff–Winkler 는 남의 실험 값 70° 와 대조) |
| 구현 기반 | **GEOS** 프레임워크 (ref 57 · 58) 의 3D MPM · **CPDI** (ref 39) + domain scaling (ref 32) · 구조 직교 격자 + 삼선형 형상함수 · *update stress last* (ref 40) · MPI 영역 분할 + OpenMP · 시각화 VisIt (ref 59) · 셀당 입자 방향당 2 개 (§1.1 · §2.5 · §2.6) |
| 자금 | *Joint DoD/DOE Munitions Technology Development Program (JMP)* (일부) · LLNL 계약 PND-L45911-WFO-DOD · *LLNL-JRNL-679544 DE-AC52-07NA27344* |
| 감사의 글 | Randolph Settgast — *"in the implementation of the field-gradient partitioning method within the GEOS computational framework"* |
| 원문 상태 | 출판사 웹 전문 페이지의 세로 캡처 두 장 (1399 × 28800 px · 1399 × 12924 px) · 글자 층 없음 → 카드의 모든 글 · 식은 2–5 배 확대한 그림에서 눈으로 옮겼다.  표 4 는 페이지의 스크롤 상자 안에 있어 **보이는 행만** 옮겼다 |

**자기 위치 (저자 원문 · Summary)**
> *"Contact and fracture in the material point method require grid-scale enrichment or partitioning of material into distinct velocity fields to allow for displacement or velocity discontinuities at a material interface.  A new method is presented in which a kernel-based damage field is constructed from the particle data.  The gradient of this field is used to dynamically repartition the material into contact pairs at each node.  This approach avoids the need to construct and evolve explicit cracks or contact surfaces and is therefore well suited to problems involving complex 3-D fracture with crack branching and coalescence.  A straightforward extension of this approach permits frictional 'self-contact' between surfaces that are initially part of a single velocity field, enabling more accurate simulation of granular flow, porous compaction, fragmentation, and comminution of brittle materials.  Numerical simulations of self contact and dynamic crack propagation are presented to demonstrate the accuracy of the approach."*

---

## 3. 핵심 수치

> **라벨 규약** · `인쇄` = 본문 · 표 · 캡션 · `[카드 산술]` = 인쇄값의 산술 (식 병기) · `[판독]` = 그림에서 읽음 (에너지 그림은 눈금 600–1000 mJ 를 화소로 환산 · ±5 mJ 정도 · 추세 전용) · `[미확인]` = 캡처에 없음.  ⚠ 아래 재료값은 전부 그 논문의 가상 재료다 — 우리 재료 값으로 쓰지 않는다.

### 3-1. 자기 접촉 검증 ① 판 사이 빌릿 압축 (§3.1 · Table 1 · Fig. 7–8)

| 양 | 값 | 표지 |
|---|---|---|
| 기하 (4 분면 · 대칭면 둘) | 판 w_p 1.2 mm × h_p 0.4 mm · 빌릿 w_b 1.0 mm × h_b 0.6 mm | 인쇄 (Table 1) |
| 하중 | 판 위에 일정 압축 견인력 σ_t = 200 MPa (*"A constant compressive normal force is applied to the platen"*) | 인쇄 |
| 빌릿 | K_b 158.333 GPa · G_b 73.077 GPa · ρ_b 2.3 g/cm³ → E 190.0 GPa · ν 0.300 | 인쇄 · [카드 산술: E = 9KG/(3K + G) · ν = (3K − 2G)/(2(3K + G))] |
| 판 | K_p 140 GPa · G_p 60 GPa · ρ_p 8 g/cm³ → E 157.5 GPa · ν 0.3125 | 인쇄 · [카드 산술] |
| 마찰계수 | μ = 0.04 | 인쇄 |
| 격자 · 입자 수 · 시간 간격 · 끝 시각 | — | **[미확인]** |
| 결과 | SF = 붙음 (no-slip) ↔ 다중 장 (판 · 빌릿) = 마찰 미끄럼 = '정답' ↔ 한 묶음 + 표면 표지 분할 = *"nearly identical to that of the multi-field solution"* | 인쇄 (판정은 눈 대조) |
| 그림의 색 막대 | 수평 속도 V_x 0–200 m/s | [판독] (Fig. 8) |

⚠ **표의 빌릿 탄성값은 본문과 안 맞는다** [카드 판독]: 본문은 *"a compliant hyperelastic billet between stiff steel platens"* 인데 Table 1 은 빌릿 (E 190 GPa) 이 판 (E 157.5 GPa) 보다 단단하고, 200 MPa 에서 E 190 GPa 면 변형률이 ≈ 0.1 % (200 MPa / 190 GPa [카드 산술]) 인데 Fig. 8 의 빌릿은 눈에 띄게 눌려 퍼진다.  단위 (GPa ↔ MPa) 오기일 가능성이 있으나 확인할 길이 없다 [미확인].  이 표의 재료값으로 시험을 재현하지 않는다.

### 3-2. 자기 접촉 검증 ② 쐐기 → 원판 → 블록 (§3.1 · Fig. 9)

- *"plane-strain large deformation of a low-stiffness hyperelastic material, for which the contact surfaces move and distort.  A distributed horizontal load acts on a wedge of material that moves to the right until it contacts a disk, pushing it to contact a square block.  The problem is designed to produce a dramatic difference between the no-slip and frictional results."*
- 프레임 시각 0.2 · 8.0 · 9.6 µs · 색 막대 0–200 m/s [판독].  재료값 · 치수 · 마찰계수 · 격자 표는 **없다** [미확인].
- 판정: *"with surface detection and frictional self-contact, it is possible to reproduce the frictional response, without the need to initially define distinct regions of contacting material"* — 수치 비교 없음.

### 3-3. Kalthoff–Winkler 동적 전단 파괴 (§3.2 · Table 2 · Fig. 10–11)

| 양 | 값 | 표지 |
|---|---|---|
| 기하 | 표적 폭 w_t **10 mm** (인쇄) · 높이 h_t 100 mm · 두께 t 2 mm · 노치 w_n 50 mm · 충격체 높이 h_i 25 mm · 폭 w_i 100 mm | 인쇄 (Table 2).  ⚠ w_t 는 노치 50 mm · 격자 100 × 100 · l^ch 1.414 mm 와 맞으려면 100 mm [카드 판독] |
| 충격 속도 | v_0 = 33 m/s | 인쇄 |
| 재료 (표적 · 충격체 같음) | K 158.333 GPa · G 73.0769 GPa · ρ 8 g/cm³ → E 190 GPa · ν 0.30 · c_S 3.02 km/s · Rayleigh 파속 ≈ 0.927 c_S ≈ 2.80 km/s | 인쇄 · [카드 산술] |
| 파괴 | σ_f 570 MPa · G_f **22.13 N/mm** (본문) ↔ **22.3 mJ mm⁻²** (Table 2) · *"selected to match those used by Song et al. 48 in their XFEM analysis"* | 인쇄 (두 값이 다르다 — §3-4 의 354.1 mJ 가 22.13 을 지지) |
| 격자 | 표적 영역 100 × 100 셀 → Δx 1 mm · l^ch 1.414 mm = √2 Δx | 인쇄 · [카드 산술] |
| 분리 문턱 | D̄^min = 0.25 | 인쇄 |
| 연화 계수 | H̄_s = σ_f²/(2EG_f) = 38.6 m⁻¹ · H̄_s l^ch = 0.055 · H_s = 0.058 | [카드 산술: (570 × 10⁶)²/(2 × 190 × 10⁹ × 22,130)] |
| **균열 각** | 실험 70° · XFEM (Song) 60° · **DFG 59.1°** · SF 60.8° — *"all these results underpredict the fracture angle by 10°"* | 인쇄 |
| **균열 속도** | **DFG 2.0 km/s** · SF 1.7 km/s · XFEM (ref 67 — 인쇄 철자 *Belytchko et al.*) ≈ 2.0–2.2 km/s (40 µs < t < 50 µs) · XFEM (Song) ≈ 2.8 km/s | 인쇄 |
| Rayleigh 파속 대비 | DFG 0.71 · SF 0.61 · Song 1.00 | [카드 산술: 2.0 · 1.7 · 2.8 / 2.80] |
| 그림 프레임 시각 | 0.04286 · 0.05358 · 0.08858 ms | [판독] (Fig. 11) |

저자 평가: *"it is reassuring that the results obtained using MPM with DFG-partitioning are generally comparable with published solutions with the XFEM method, without requiring any parameter tuning.  While the SF MPM solution gives a similar crack geometry, it may slightly underpredict the crack speed, perhaps due to spurious velocity-field smearing dissipation at the crack surface."*  그리고 스스로 단서: *"even when using Lagrangian FEM, the fracture behavior in the Kalthoff–Winkler simulations is highly sensitive to small variations in constitutive model parameters or support conditions"*.

### 3-4. 변형 Charpy — 계 전체 에너지 수지 (§3.3 · Table 3 · Fig. 12–14)

| 양 | 값 | 표지 |
|---|---|---|
| 기하 | 시편 폭 w_t 10 mm · 높이 h_t 55 mm · 두께 t 2 mm · 노치 w_n 2 mm · 타격체 (2D 원판) 지름 d_s 20 mm | 인쇄 (Table 3) |
| 타격 속도 | v_0 = 20 m/s | 인쇄 |
| 재료 | K 158.333 · G 73.0769 GPa · ρ 8.0 g/cm³ · σ_f 1.0 GPa · G_f 22.3 mJ mm⁻² (표) | 인쇄 |
| 수치 손잡이 (표) | l^ch 1.414 mm · D̄^min "0.25 mm" | 인쇄 (⚠ 단위 'mm' 는 오식 — 무차원 [카드 판독]) |
| 타격체 운동 에너지 | ½ m v² = **1005 mJ** (m = π × 10² × 2 mm³ × 8 g/cm³ = 5.03 g) | [카드 산술] — Fig. 13 의 처음 고원 ≈ 1005 mJ [판독] 과 일치 |
| 기대 파괴 에너지 | ΔE^tot = G_f A_f = **354.1 mJ** | 인쇄.  [카드 산술] A_f = (10 − 2) × 2 = 16 mm² → 22.13 × 16 = 354.1 ✓ (22.3 이면 356.8 ✗) ⇒ **실제 쓴 값은 G_f = 22.13** |
| 이상 끝 에너지 | 1005 − 354.1 = **651 mJ** | [카드 산술] — 'Ideal Fracture' 점선 ≈ 649 mJ [판독] |
| 탄성 충돌의 수치 소산 | Δx = 1 mm 에서 끝 에너지가 처음 운동 에너지보다 **2.5 %** 낮은 평균 주위로 진동 | 인쇄.  [카드 산술] ≈ 25 mJ → 노란 띠 626–651 mJ (띠 아래 끝 ≈ 624 [판독]) |
| 해상도 | Δx = 1.00 · 0.50 · 0.25 mm → 남은 단면 8 mm 에 8 · 16 · 32 셀 | 인쇄 · [카드 산술] |
| 연화 계수 | H̄_s = 118.9 m⁻¹ · H̄_s l^ch = 0.168 / 0.084 / 0.042 · H_s = 0.202 / 0.092 / 0.044 (Δx 1 / 0.5 / 0.25 mm · l^ch = √2 Δx) | [카드 산술] |

**끝 에너지 (Fig. 13 · [판독 ±5 mJ]) 와 소산 [카드 산술: 1005 − 끝값]**

| Δx | DFP (= DFG 분할 · 범례 표기) 끝 → 소산 (÷ 354.1) | SF 끝 → 소산 (÷ 354.1) |
|---|---|---|
| 1.00 mm | 618 → 387 mJ (1.09) | 568 → 437 mJ (1.23) |
| 0.50 mm | 632 → 373 mJ (1.05) | 598 → 407 mJ (1.15) |
| 0.25 mm | 637 → 368 mJ (1.04) | 627 → 378 mJ (1.07) |

저자: *"The DFG results produce approximately the correct fracture energy at all resolutions, with noise due to undamped high-frequency oscillations becoming more evident as the mesh is refined.  The SF solution shows a consistently lower post-fracture energy at all resolutions.  This is attributed to the velocity-field smearing error, which produces additional dissipation at the fracture surface, as well as additional 'noise' in the velocity field."*

**손잡이 민감도 (Fig. 14 · Δx 0.5 mm · [판독 ±5 mJ])**

| 경우 | D̄^min | l^ch | 끝 에너지 → 소산 |
|---|---|---|---|
| a · b · d | 0.01 · 0.125 · 0.25 | √(Δx² + Δy²) | ≈ 633 → 372 mJ (세 경우 겹침 — 캡션 인쇄) |
| c | 0.25 | ½ √(Δx² + Δy²) | ≈ 523 → 482 mJ (d 의 1.30 배) |
| e | 0.25 | 3/2 √(Δx² + Δy²) | ≈ 662 → 343 mJ (d 의 0.92 배 · 이상선 위) |
| f · g | 0.5 · 0.75 | √(Δx² + Δy²) | 속 그림에서 d 와 몇 mJ 차 |

저자: *"The characteristic length determines the softening response and thus has a strong impact on the fracture energy, regardless of whether a SF or DFG-partitioning solution is used.  Decreasing the value of D̄^min has no perceptible effect, but there is a change in dissipation as D̄^min is increased towards 1."* · *"With these parameters, the analyst is afforded a degree of control over the localization response, which can be tuned to more precisely reproduce a fracture energy release rate consistent with the constitutive modeling assumptions."*

### 3-5. 동적 Brazilian — 파쇄 뒤 알갱이 흐름 · 다짐 (§3.4 · Table 4 · Fig. 15–18)

| 양 | 값 | 표지 |
|---|---|---|
| 기하 | 판 w_p 12 mm × h_p 2 mm (위 · 아래) · 원판 지름 d_d 10 mm · 두께 t 2 mm · **옆면은 대칭면** (Fig. 15 의 sym 띠) | 인쇄 (Table 4) · [판독] |
| 하중 | 일정 압축 견인력 σ_t = 650 MPa (*"constant-stress loading"*) | 인쇄 |
| 원판 | K_d 158.333 · G_d 73.077 GPa · ρ_d 2.3 g/cm³ → c_P 10.5 km/s · c_S 5.64 km/s · Rayleigh ≈ 5.2 km/s | 인쇄 · [카드 산술] |
| 파괴 모델 | 시간-파괴 (식 24) · 균열 속도 c_{f,d} = 2 km/s (= Rayleigh 의 0.38 배 [카드 산술] — 본문 *"commonly on the order of 0.4v_r"*) | 인쇄 |
| Weibull | 기준 강도 σ_ref,d 140 MPa @ 기준 부피 V_ref,d 8 cm³ · 계수 m_d 6.0 | 인쇄 |
| 판 | K_p 260 · G_p 180 GPa · ρ_p 8 g/cm³ (→ E 439 GPa · ν 0.22 [카드 산술]) — *"a density and stiffness approximating steel"* | 인쇄 |
| 마찰계수 · D̄^min · l^ch | — | **[미확인]** (Table 4 의 보이는 행에 없음 — 스크롤 상자) |
| 해상도 | Δx = 0.181 · 0.094 · 0.063 mm ↔ n_p = 14441 · 57457 · 129553 (본문) — 그림 표지는 14,441 · 57,457 · **129,533** | 인쇄 (셋째 값이 본문 ↔ 그림에서 다르다) |
| 지름당 셀 수 | 55 · 106 · 159 | [카드 산술: 10 mm / Δx] |
| n_p 검산 | 원판 π/4 (2 × 10/Δx)² + 판 2 × 12 × 2 × 4/Δx² = 15,450 · 57,284 · 127,528 (인쇄값의 1.07 · 1.00 · 0.98 배) → n_p 는 판 입자를 포함하고 원판 몫이 ≈ 62 % | [카드 산술 · 셀당 2 × 2 가정] |
| Weibull 중앙 강도 | σ_f/σ̄_f = (V̄/V)^(1/m) (R = ½) = 8.9 · 11.0 · 12.6 → 1.24 · 1.55 · 1.77 GPa (V = (Δx/2)² × 2 mm) | [카드 산술] — Fig. 16–17 첫 열의 색 (0–24 눈금에서 초록 → 노랑 → 주황 [판독]) 과 맞음 |
| 그림 시각 | SF (Fig. 16) 0 · 5 · 10 · 15 · 20 µs ↔ DFG (Fig. 17) 0 · 2.5 · 5 · 7.5 · 10 µs — *"the time scales are different in the two figures, to account for the delayed onset of failure in the SF solution"* | 인쇄 · [판독] |
| 파편 분석 | 연결 성분 알고리즘 (ref 71) 으로 손상 안 된 조각 → 누적 크기 분포 · DFG 는 t = 10 µs, SF 는 t = 15 µs 에서 (*"for which the displacement fields are comparable"*) · 최소 분해 조각 *"approximately 50µs"* (인쇄 그대로 — 길이 단위여야 함 [카드 판독 · 미확인]) | 인쇄 |
| **평균 속도 (Fig. 18 속 그림)** | SF ≈ 45 → 113 → 132 m/s ↔ DFP ≈ 107 → 147 → 139 m/s (n_p 1.4 만 → 5.7 만 → 13 만) | [판독 ±5 m/s] |

진행 (본문): 탄성 예압 → 접촉점 근처에서 파괴 시작 (*"consistent with the location of the maximum principal stress predicted by Hertzian contact theory 70"*) → 수직 균열 → 원판 끝이 분쇄 · 가운데 큰 조각 안에 균열 핵생성 · 분기 → 전체가 조각나 바깥으로 흐름 (조각끼리 미끄럼) → *"When the fragments impact the side walls, they are pulverized, and the debris starts to fill the volume and become compressed."*  ⚠ 절 제목은 *Fragmentation and compaction response* 지만 **다짐 단계의 수치 (밀도 · 기공 · 응력 곡선) 는 없다**.

### 3-6. 비용 (§3.5 · Fig. 19)

| 양 | 값 | 표지 |
|---|---|---|
| 덧비용의 세 몫 | (i) 이웃 목록 만들기 · 유지 (ii) 입자에서 DFG 평가 (iii) 노드별 분류 | 인쇄 |
| 이웃 정렬 | *"less than 0.1% of the total runtime, even for the largest problems"* (마지막 정렬 위치에서 일정 거리 넘게 움직였을 때만 다시 정렬) | 인쇄 |
| 주된 몫 | *"evaluation of the DFG at the particles accounted for the majority of the additional computational expense"* — 이웃 수가 격자를 조여도 같으므로 n_p 에 선형일 것으로 기대 | 인쇄 |
| 계산기 | 노드 1 대 = 8 코어 2.6 GHz Intel Xeon E5-2670 × 2 · 1 코어 또는 OpenMP 16 스레드 | 인쇄 |
| 문제 | §3-5 의 Brazilian · 셀당 입자 2 × 2 × 1 고정 · 걸음 수 3,000–18,000 (해상도에 따라) 의 평균 | 인쇄 |
| **SF 대비 덧비용** | n_p ≤ 32,000 (16 스레드): 스레드를 다 못 써서 덧비용이 가려짐 · **32,000 < n_p < 150,000: +30–50 %** · n_p > 150,000: 더 빨리 늘어남 — 그래도 DFG 계산 자체는 전체의 **30 %** (*"some memory access inefficiencies in the implementation"* 탓으로 봄) | 인쇄 |
| 맞춤 기울기 (log–log) | DFP 1 스레드 **1.23** · SF 1 스레드 **1.01** · DFP 16 스레드 **1.27** · SF 16 스레드 **0.89** | 인쇄 (Fig. 19 그림 안) |
| MPI 전망 | 영역 분할 MPM 은 2.65 × 10⁵ 분할까지 (ref 55 · Uintah — 다른 곳에선 *256 K processing cores*) · 프로세서 하나의 영역은 보통 16 × 16 × 16 셀 ≈ 3.2 × 10⁴ 입자 이하 → 그 크기에서 덧비용은 감당할 만하다는 주장 | 인쇄.  [카드 산술] 16³ × 8 = 32,768 ✓ |
| GPU 전망 | 고정 반경 이웃 탐색이 O(kn) (ref 73) → *"it is expected that the DFG-partitioning method will transition well into next-generation high-performance computing systems"* (실측 없음) | 인쇄 |

**Fig. 19 점 [판독 — 축 눈금 (10⁴ · 10⁵ · 0.1 s · 1 s) 을 화소로 환산; 이 점들로 다시 맞춘 기울기 1.23 · 1.00 · 1.26 · 0.89 가 인쇄값과 일치 → 판독 검산]**

| n_p | DFP 1 스레드 | SF 1 스레드 | DFP 16 스레드 | SF 16 스레드 | 16 스레드 DFP/SF |
|---|---|---|---|---|---|
| 1.45 × 10⁴ | 0.46 s | 0.34 s | 0.11 s | 0.093 s | 1.2 |
| 3.2 × 10⁴ | 1.34 s | 0.73 s | 0.23 s | 0.21 s | 1.1 |
| 5.7 × 10⁴ | 2.44 s | 1.35 s | 0.50 s | 0.28 s | 1.8 |
| 7.3 × 10⁴ | — | — | 0.66 s | 0.35 s | 1.9 |
| 1.03 × 10⁵ | — | — | 0.95 s | 0.65 s | 1.5 |
| 1.29 × 10⁵ | — | — | 1.41 s | (점이 안 보임) | — |
| 2.3 × 10⁵ | — | — | 3.83 s | 1.08 s | 3.5 |

⚠ 5.7 만 · 7.3 만 입자의 판독 비 (≈ 1.8–1.9 배) 는 본문의 *"30–50%"* 보다 크다 — 로그 축 판독 오차 (점마다 ±10 % 정도) 로는 다 설명되지 않는다 [카드 판독].  1 스레드 비는 1.35 · 1.84 · 1.81 [판독 · 카드 산술].  **인용은 본문 문장 (+30–50 %) 으로 하고 이 표는 추세 확인용으로만** 쓴다.

**이웃 수 [카드 산술 — 논문에 없는 수]**: 핵 반경 = 셀 대각선, 입자 간격 = Δx/2 일 때 반경 안 입자 수 ≈ 2D π(√2)² × 4 = **25** · 3D (4/3)π(√3)³ × 8 = **174** — 3D 가 2D 의 **6.9 배**.  위 비용 비율은 2D (셀당 2 × 2 × 1) 값이라 3D 로 옮길 수 없다.

### 3-7. ★ 이 논문에 **없는** 값 (정직 목록)

- 소성 · 경화 · 크리프 · 항복 값: 없음 (재료는 neo-Hookean + 인장 손상).
- 압밀 곡선 (압력–기공 · 밀도) · 준정적 하중 · 탈압 · 되돌아옴: 없음.  §3.4 의 '다짐' 은 서술 한 문장.
- 자기 접촉의 정량 오차 (노름 · 접촉력 · 판 반력 · 미끄럼량): 없음.  해석해 대조 (경사면 · Hertz 등) 도 없음 — Bardenhagen 2000 · 2001 의 경사면 시험 같은 것이 없다.
- 한 노드에 셋 이상이 만나는 경우의 시험 · 오차: 없음.
- 시간 간격 · CFL 수 · 끝 시각: 없음 (걸음 수 3,000–18,000 만).
- 표면 탐지 문턱 (핵 합 S 가 얼마 아래면 표면인가) · 표지 띠 두께의 수 · 질량 하한 ε_m · 비국소 반경 r_g · K–W / Charpy / Brazilian 의 마찰계수: 없음.
- 3D 의 비용 · 정확도 · 입자 수 (Fig. 20 포함): 없음.
- 실험 대조: Kalthoff–Winkler 의 균열 각 70° 한 값뿐 (남의 실험).

---

## 4. 방법 ★

### 4-1. MPM 한 걸음 (§1.1, 식 1–10 · 그림 `eq_01_06_mpm_p2g_forces_grid_update.png` · `eq_07_10_velocity_gradient_g2p_update.png`)

> **m_i = Σ_p S̄\*_ip m_p (1)   v_i = (1/m_i) Σ_p S̄\*_ip m_p v_p (2)**
> **f_i^ext = Σ_p S̄\*_ip b_p m_p (3)   f_i^int = −Σ_p (∇S\*_ip)‾ · σ_p V_p (4)**
> **a_i = (f_i^int + f_i^ext)/m_i (5)   v̄_i^{n+1} = v_i^n + a_i Δt (6)**
> **L_p^{n+1} = Σ_i v_i^{n+1} ⊗ (∇S\*_ip)‾ (7)   F_p^{n+1} = F_p^n + (L_p^{n+1} · F_p^n) Δt (8)**
> **v_p^{n+1} = v_p^n + Σ_i S̄\*_ip a_i Δt (9)   x_p^{n+1} = x_p^n + Σ_i S̄\*_ip v_i^{n+1} Δt (10)**

- S̄\*_ip = i 번째 격자 형상함수의 **p 번째 입자 영역 평균**, (∇S\*_ip)‾ = 그 기울기의 평균.  원래 MPM 의 한 점 적분 (*'Dirac delta'*) 은 셀 넘김 오차를 내고, GIMP (ref 38) 는 유한 영역으로 줄이지만 다 없애지 못하며, **CPDI** (ref 39) 는 입자 영역을 변형하는 평행육면체로 둔다.  이 논문은 CPDI + *domain scaling* (ref 32 — *"allows for efficient parallelization, while controlling nonphysical numerical fracture"*) · 구조 직교 격자 · **삼선형 (tri-linear) 형상함수**.
- 식 (6) 의 윗줄 (v̄) 은 **접촉력을 넣기 전** 속도다.  접촉력이 v̄ → v 로 고치고 (식 13), 그 v 로 속도 기울기 · 변형구배 · 위치를 갱신한다.  구성 모델은 갱신된 F · L 로 부른다 — *'update stress last'* (ref 40 — *"most accurate for dynamic simulation with explicit time-stepping schemes"*).
- 저자가 꼽은 MPM 의 네 장점 (ref 41 · §1.1): ① 메시 생성 불요 (CT 복셀 자료를 바로) ② 상태 이력이 입자에 있어 이류 오차 없음 ③ 격자를 매 걸음 되돌리므로 큰 변형을 견딤 ④ 마찰 접촉이 효율적.
- ⚠ 식 (9) 의 a_i 에 접촉력이 어떻게 들어가는지는 식으로 인쇄돼 있지 않다 [미확인] — Algorithm 2 뒤의 *"Similar algorithms are used for mapping the momentum, accumulating forces, and for mapping velocity and acceleration from the grid to the particles"* 한 문장뿐.

### 4-2. 전통 접촉 — 미리 나눈 속도장 (§1.1.1, 식 11–16 · 그림 `eq_11_13_…` · `eq_14_16_…` · Fig. 1)

접촉 묶음마다 속도장 ς 를 두고, **두 장 이상의 질량이 있는 노드**에서 접촉력 f^ct 를 건다.  목적 셋: *"(i) prevent interpenetration; (ii) allow frictional sliding if the slip condition is met; and (iii) allow separation of the contact pair."*

1. **표면 법선** — 장별 질량의 기울기를 정규화: **n_ςi = Σ_p (∇S\*_ip)‾ m_ςp / ‖Σ_p (∇S\*_ip)‾ m_ςp‖ (11)** (본문: *"an outward surface normal based on the normalized local density gradient"*).
2. **보정 법선** — *"For perfect conservation of linear momentum, it is necessary that the surface normals for a contact pair are exactly opposite"* → **n\*_1i = −n\*_2i = ½(n_1i − n_2i)** 를 다시 정규화.  질량 · 부피 가중은 *"may improve the response, particularly when one field is present in a very small fraction, but this was not carried out"*.
3. **질량중심 속도**: **v_i^cm = Σ_ς m_ςi v̄_ςi / Σ_ς m_ςi (12)**.  접촉 뒤 **v_ςi = v̄_ςi + (f^ct_ςi/m_ςi) Δt (13)**.
4. **법선력** — KKT 조건 f_i^nor ≥ 0 · g_i ≤ 0 · f_i^nor g_i = 0 (g_i = 노드 겹침 · ref 43).  *"The kinematic constraint is enforced by applying a contact force directly at the node if interpenetration is detected (i.e., if Σ_{ς=1}^{2} n_ςi · v_ςi ≤ 0).  Otherwise, no contact force is applied, which naturally allows separation of contact surfaces."*
   > **f^nor_ςi = f^ct_ςi · n_ςi = (m_ςi/Δt)(v_i^cm − v̄_ςi) · n_ςi (14)**
5. **접선력 (붙음일 때)** — n 과 직교 정규 기저 s¹ · s² (두 장이 같은 기저를 쓴다):
   > **f^{1,tan}_ςi = (m_ςi/Δt)(v_i^cm − v̄_ςi) · s¹_ςi (15a)   f^{2,tan}_ςi = (m_ςi/Δt)(v_i^cm − v̄_ςi) · s²_ςi (15b)**
6. **Coulomb 마찰** — f^tan = f^{1,tan} s¹ + f^{2,tan} s² · f^tan_ςi = ‖f^tan‖ · s_ςi = f^tan/f^tan_ςi 로 두고
   > **f^ct_ςi = f^nor_ςi n_ςi + min(μ\|f^nor_ςi\|, \|f^tan_ςi\|) sgn(f^tan_ςi) s_ςi (16)**

**속도 꼴로 바꾸면 Bardenhagen 과 같은 갱신이다 [카드 산술]**: 식 (13) 에 (14)–(16) 을 넣으면 v_ς = v̄_ς + [(v^cm − v̄_ς)·n] n + min(μ\|Δv_n\|, \|Δv_t\|) s — 법선 성분은 질량중심 것으로 바뀌고, 접선 차이는 붙음이면 다 없어지고 (그 장의 속도 = v^cm = **한 속도장과 같음**) 미끄럼이면 μ\|Δv_n\| 만큼만 준다.  `bardenhagen2001…` 카드 §5-2 의 식 (10) ṽ = v − Δv_n (n + μ′ t), μ′ = min(μ, Δv_t/Δv_n) 과 같은 식이다.  다른 점 둘: ① 보정 법선으로 두 법선을 정확히 반대로 맞춤 (2001 판은 미끄럼에서 법선이 공선이 아니면 운동량이 안 맞는다고 적었다) ② **분리 판정이 속도뿐** — 2001 판의 수직 견인력 판정 (압축이 남아 있으면 접촉 유지) 은 이 논문에 **언급이 없다** [카드 판독].

⚠ **부호 규약이 인쇄에서 엇갈린다** [카드 판독 · 카드 산술].  식 (11) 은 본문 말대로 **바깥** 법선을 준다 — 1D 로 보면 물체가 x < 0 에 있고 노드가 x = 0 일 때 안쪽 입자에서 형상함수 기울기는 +x (입자 → 노드) 이므로 Σ_p ∇S_ip m_p 는 +x = 물체 밖.  바깥 법선이면 두 물체가 **다가올 때** (v̄_1 − v̄_2)·n_1 > 0 이라 Σ_ς n_ς · v_ς **> 0** · (v^cm − v̄_ς)·n_ς **< 0** · 식 (14) 의 f^nor **< 0** 이다.  그런데 인쇄는 접촉 조건이 "Σ n · v ≤ 0", KKT 가 f^nor ≥ 0, Algorithm 3 의 16 행이 (v^cm − v̄_ςi) · n_ς^cm > 0 — 셋은 서로는 맞지만 **안쪽 법선**일 때 '다가옴' 이 된다 (Bardenhagen 2001 식 (8) 은 바깥 법선에 (v^α − v^cm)·n^α > 0).  어느 쪽이 구현인지는 이 논문만으로 알 수 없다.  ⇒ **식을 그대로 옮기지 말고, 두 블록의 접근 / 이탈 단위 시험으로 규약을 고정한 뒤 쓴다.**

### 4-3. 왜 장을 늘리는 길이 막히는가 (§1.1.1 · Fig. 2)

- 장 N 개면 *"N(N − 1) possible contact pairs, so the computational cost and memory requirements for the contact algorithm become more significant as N becomes large.  This cost can be mitigated by only computing interactions for fields that are active at a single node."*
- **더 중요한 문제 (저자)**: *"while pairwise force calculations ensure conservation of linear momentum, they do not strictly prevent interpentrability for N > 2 fields.  We are currently developing other approaches to address this limitation, but this is beyond the scope of our current discussion."*
- 알갱이 계: 이웃 알갱이가 서로 다른 장에 있어야 한다 → 2D 는 4 색 정리로 4 장이면 되지만 (ref 45) **3D 는 상한이 없고**, 처음에 잘 칠해도 변형 · 흐름이 접촉점을 바꾼다 (§0 인용).  Fig. 2a: *"even in 2-D, a large number of velocity fields may be required"*.
- 다공체 (Fig. 2c): 큰 변형으로 한 물체의 기공 벽끼리 닿는 **자기 접촉**은 접촉면을 미리 알 수 없어 *"not possible with the traditional prescribed-field approach"*.  파괴면도 같다 — 벌어진 면이 **다른** 물체와 새 접촉 쌍을 만들면 기존 방법이 어렵다.
- 명시적 균열 방식 (Nairn, ref 34 · 35 · Fig. 3): 입자와 노드 사이에 균열이 있는지로 노드마다 두 장에 나눔 — 단일 균열에는 잘 되지만 *"it becomes difficult to implement for complex 3-D networks of branching and coalescing fractures"*, 그리고 벌어진 균열면이 다른 물체에 닿는 일반 마찰 접촉의 틀을 주지 못한다 (§1.1.2).  점착대 방식 (ref 49) 도 같은 한계.

### 4-4. 스칼라 손상장 (§2.1, 식 17–19 · 그림 `eq_17_19_kernel_damage_field_normalization.png` · Fig. 4)

> **D(x) = Σ_{p=1}^{n_p} D_p ω(r̄) (17)   ω(r̄) = 1 − 3r̄² + 2r̄³ (0 ≤ r̄ ≤ 1), 0 (r̄ > 1),  r̄ = ‖x − x_p‖/r_p (18)**
> **S(x) = Σ_{p=1}^{n_p} ω(‖x − x_p‖/r_p) (19)   D̄(x) = D(x)/S(x)**

- **핵 반경 = 셀 대각선**: *"Except where otherwise noted, the neighbor radius is the diagonal length of a background grid cell, r_p = √((Δx)² + (Δy)² + (Δz)²) in 3-D and r_p = √((Δx)² + (Δy)²) for 2-D plane strain."*
- 정규화하지 않은 D(x) 는 자유 표면에서 값이 꺼져 (Fig. 4a) 기울기가 표면을 가리킨다 → 핵 합 S(x) 로 나눈 D̄ 는 *"accurately captures only the effects of the damage geometry"* (Fig. 4c).  D̄ 는 핵 지지 밖 (S = 0) 에서 정의되지 않지만 **입자 중심에서만** 값 · 기울기를 구하므로 문제없다.
- SPH (ref 50) 와 닮았지만 *"we are only using the direction of the DFG to locate particles relative to fracture surfaces, and the kernel field is not used in the solution of the momentum equation.  As such, we do not require that the kernel functions have partition of unity and do not require the more complex corrections used in the reproducing kernel particle method 51."*
- **핵 합 자체가 표면 탐지기** (Fig. 4b) — §4-7 의 자기 접촉에 쓴다.
- 기울기의 식은 인쇄돼 있지 않다 (입자의 이웃을 훑는다고만).  몫의 미분으로 ∇D̄ = (S ∇D − D ∇S)/S² [카드 산술].  3차 핵은 ω′(0) = ω′(1) = 0 (ω′ = −6r̄ + 6r̄² [카드 산술]) 이라 중심 · 가장자리에서 매끈하다.

### 4-5. 기울기 분할 (§2.2, 식 20 · Algorithm 1–2 · 그림 `eq_unnumbered_s2_2_sign_rule_nonlocal_gradient.png` · `eq_20_alg_1_nonlocal_node_dfg.png` · `alg_2_p2g_dfg_partitioning.png` · Fig. 5)

- **생각**: 균열 (손상 능선) 의 양쪽에서 손상 기울기는 서로 반대를 향한다.  위상 단순화 (ref 52) 로 균열면을 찾아내는 대신 *"we compare the direction of the DFG for the particles mapping to a node.  If opposing gradients exist, the node is potentially at a contact surface"*.
- **장 번호는 노드마다 따로**다: *"it is not necessary that the ordering of the contact partitioning (i.e., whether the ς = 1 field is above or below the crack) be consistent along the fracture surface; it is only necessary that the orientation of the surface normal for each field at the node be consistent with the direction of the normal to the fracture or contact surface."*  같은 입자가 이웃 노드에서 다른 번호를 받아도 된다 (접촉력을 노드마다 따로 계산하므로).
- **단순 규칙과 그 실패**: sgn[(∇D̄_p) · (∇D̄_g)] (노드에서 잰 기울기 ∇D̄_g) — *"this simple method fails when the grid node lies at the maximum of the scalar field and ∇D̄_g = 0.  This pathological case can occur quite frequently at the border of a fully damaged region."*
- **비국소 기울기**: 노드 주변에서 \|n\*_i · ∇D(x)\| 의 적분을 최대로 하는 단위 벡터 n\*_i 의 배수로 정의 (해가 적어도 둘 — 방향 부호는 상관없다).  그 최적화는 비싸므로 *"it is sufficient to define the nonlocal DFG to be the gradient of the damage field evaluated at the point x^max within some radius (r_g) for which the gradient has the greatest magnitude"*:
  > **∇D̄\*_i = ∇D̄(x_i^max),   x_i^max = arg max_{x∈R} [∇D(x)] ∋ ‖x − x_i‖ < r_g (20)**
- **Algorithm 1 (10 행) — 근사 평가**: 모든 노드의 ∇D̄_i ← 0; 입자 p 마다, p 가 얹히는 노드 i 마다 **‖∇D̄_p‖ > ‖∇D̄_i‖ 이면 ∇D̄_i ← ∇D̄_p**.  즉 노드 대표 기울기 = 그 노드에 얹히는 입자 중 기울기가 가장 큰 것.  r_g 의 수치는 없다 — 구현상 '노드에 얹히는 입자 범위' 다 [카드 판독].
- **Algorithm 2 (10 행) — 분할 P2G**: 입자 p · 노드 i 쌍마다 **∇D̄_p · ∇D̄_i ≥ 0 이면 ς ← 0, 아니면 ς ← 1**; m_ςi ← m_ςi + S̄\*_ip m_p.  운동량 · 힘 · 격자 → 입자 사상도 같은 꼴 (식은 인쇄 없음).
- **기울기는 위상만 정한다 — 법선이 아니다**: *"while the DFG vector is approximately normal to the failure surface, it is used only to define the topology by partitioning the material into contact groups, and it does not define the surface normal.  Once the material is partioned, the normal for subsequent contact interactions is defined by Equation 11.  As such, we expect the accuracy of the surface normals to be comparable with that of the surface representation in generalized MPM contact, improving with the resolution of the discretization relative to the curvature of the surface."*
- Fig. 5 (굽은 균열 · 셀당 입자 3 × 3): 노드 기울기가 균열 전 길이에서 대략 법선.  균열 끝에서는 법선이 아니지만 거기서는 분리 조건이 안 서므로 무해.
- [카드 판독] 내적 0 (기울기 0 인 내부 입자) 은 ≥ 0 이라 장 0 에 간다 → 손상 · 표지에서 먼 노드는 모든 입자가 장 0 = 자동으로 한 장.

### 4-6. 분리 조건 (§2.3, 식 21 · Algorithm 3 · 그림 `eq_21_separability_condition.png` · `alg_3_frictional_contact_separability.png`)

- 뜻: *"For the topology to be consistent with the constitutive model predictions, the material should be allowed to separate only once a 'surface' of failure particles has formed."*
- 장별 평균 손상 (질량 가중) 과 장별 최대 손상:
  > **D̄_ςi = Σ_ςp φ_ip D_p m_p / Σ_ςp φ_ip m_p (21)** (Σ_ςp = 노드 i 에 얹히는 ς 장 입자 합 · φ_ip 는 다른 곳의 S̄\*_ip 와 표기가 다르다 [카드 판독])
- **분리 가능 조건**: (i) 노드에 얹히는 입자 중 **완전 손상 (D = 1) 이 하나 이상** (D̄_i^max = 1) **∧** (ii) **min(D̄_1i, D̄_2i) > D̄^min**, 0 < D̄^min < 1.  예제 값 D̄^min = 0.25.
- **Algorithm 3 (32 행)**: 두 장 질량이 모두 ε_m 보다 큰 노드에서 — 분리 가능 여부 판정 → q^cm = q_1i + q_2i · m^cm = m_1i + m_2i · v^cm = q^cm/m^cm → n_1^cm = (n_1i − n_2i)/‖n_1i − n_2i‖ · n_2^cm = −n_1^cm → 장마다: 접선 기저 [s^cm,A, s^cm,B] ← f(n_ς^cm) →
  - **분리 가능**: (v^cm − v̄_ςi) · n_ς^cm > 0 일 때만 f^nor · f^tan,A · f^tan,B 를 식 (14)(15) 꼴로 구해 f^ct_ςi += f^nor n_ς^cm + min(μ\|f^nor\|, \|f^tan\|) f^tan s^cm.
  - **분리 불가** (*Treat as single field*): 조건 없이 f^ct_ςi += f^nor n_ς^cm + f^tan,A s^cm,A + f^tan,B s^cm,B — 두 장이 질량중심 속도로 묶인다 (= 한 장).
  - ⚠ 22 행 끝의 "f^tan s^cm" 은 식 (16) 의 "sgn(f^tan) s" 와 다르다 — 크기를 한 번 더 곱한 꼴이라 차원이 안 맞는다 (오식으로 읽음 [카드 판독]).  16 행의 부호는 §4-2 의 주의 참조.  ε_m 의 값은 없다 [미확인].
- 입력: *"User inputs are the separability threshold (D̄^min) and the coefficient of friction (μ > 0)."*
- **접촉 묶음과의 결합**: 처음부터 다른 접촉 묶음 (다른 마찰계수 등) 이 여럿 있으면 *"each of these initial fields can then be further partitioned into one of two damage state fields.  When computing field interactions, the separability condition is always met for two velocity fields that were initially different contact groups."* → 묶음 G 개면 장 2G 개 [카드 산술].
- 스칼라 손상만 다룬다.  이방 텐서 손상은 *"a potential area for future development"* — 구성 모델의 파괴면이 분리면과 정렬될 때만 물리적으로 타당.

### 4-7. ★ 자기 접촉 — 표면 표지 (§2.4 · Fig. 2b · 4b · 6)

> *"With a slight modification, we can also achieve frictional self-contact with field-gradient partitioning.  Using the magnitude of the kernel sum field (S(x) from Equation 19) evaluated at a particle, we can detect surface particles in an initial porous or granular structure.  We define, for each particle, a surface flag s_p that is set to 1 for particles at the surface and 0 for interior particles.  Such kernel-based surface detection algorithms are common in mesh-free methods, (cf., 54).  If the grains are initially in contact (but not bonded), it would be necessary to 'paint in' the surface flag at initialization."*

> *"With the surface flag so-defined, the DFG can be constructed with Equation (17), using max(s_p, D_p) in place of D_p.  In this way, frictional contact and separation will occur between surface particles, even if those particles are undamaged.  By using the kernel fields to detect surface particles, the thickness of the surface-flagged region is consistent with the kernel radius in the DFG construction, which seems to improve the surface partitioning in large-deformation frictional contact."*

- 절차 [카드 판독]: ① 처음 배치에서 핵 합 S 가 작은 입자 (이웃이 모자란 입자 = 자유 표면 근처) 에 s_p = 1 (문턱 값 [미확인]) ② 손상 자리에 max(s_p, D_p) ③ 나머지는 §4-4 ~ §4-6 그대로.  표지는 입자가 싣고 다니므로 큰 변형 뒤에도 표면이 '기억' 된다.
- **처음부터 닿아 있는 알갱이**는 핵 합으로 못 찾는다 (이웃이 모자라지 않다) → 초기화 때 표지를 **칠해 넣어야** 한다 (*paint in*).
- 띠 두께에 대한 말은 *"consistent with the kernel radius"* · *"seems to improve"* 가 전부다 — 수 · 민감도 없음.
- 쓰임 (저자): CT 복셀 자료에서 바로 만든 중규모 (mesoscale) 모형 — *"MPM is particularly well suited for modeling porous and granular materials, where localized large deformation, self contact, and frictional effects may significantly affect the bulk material response"* · 적층 제조한 저밀도 메타물질 (3D 다중 척도 격자 = 나노트러스) 이 극한 변형에서 겪는 마찰 자기 접촉 (ref 53 — *"a challenging test for traditional numerical methods"*).
- **가치 (저자 · §3.1)**: *"it becomes possible to achieve frictional contact between surface pairs that cannot be easily identified at the initialization of the problem, (e.g., certain porous structures) or when the number of potentially contacting surfaces is so large that it becomes infeasible to prescribe a sufficient number of contact groups (e.g., polydisperse granular materials in 3-D)."*

### 4-8. ★ 한 노드에 셋 이상이 만날 때 (§1.1.1 · §2.2 끝)

원문이 말한 것은 둘뿐이다.

1. 장이 셋 이상이면 쌍별 접촉력은 운동량은 보존하지만 **침투를 엄밀히 막지 못한다** (§4-3 인용) — 다른 접근을 *"currently developing"*.
2. 분할은 **노드마다 접촉 평면 하나**를 가정한다:
   > *"This approach for material partitioning assumes that a local contact plane can be defined at each node to describe the contact interactions of two material regions (i.e., the fracture faces) at that node.  For crack intersection and branching, there can be three or more regions of material meeting at a single point.  However, a crack in a smeared-damage model has a finite width, because fracture and contact are resolved only to the resolution of the grid cell.  As a result, crack intersections generally manifest as grid cells containing fully damaged particles.  One could design a perfectly symmetric problem, for which the crack plane orientation within the intersection plane is arbitrary, but in practice, any deformation of the material will perturb the damage field, allowing the fracture surface to orient in a direction to allow separation/sliding at the intersection point."*
   그리고 근거로 §3.4 (Brazilian) 를 든다 — *"the crack paths … appear to be largely independent of mesh bias"* (정성).

[카드 추론] 표면 표지로 조밀한 알갱이 층을 풀 때 세 알갱이 A · B · C 가 한 노드에 얹히면, 노드 대표 기울기 하나에 대한 내적 부호로 **두 무리**로만 나뉜다 — 셋 중 둘 (또는 그 일부) 이 그 노드에서 같은 장이 되어 서로 붙는다 (미끄럼 · 분리 없음).  이 오차의 크기는 논문에 수치가 없고, 조밀 충전에서 그런 노드의 비율은 해상도 (지름당 셀 수) 에 달렸다 → §10 행동 1.

### 4-9. 구성 모델 (§2.7, 식 22–27 · 그림 `eq_22_24_…` · `eq_25_27_…`)

- **탄성**: 압축성 neo-Hookean 시험 응력 (ref 60) **σ^E = (λ ln J/J − μ/J) I + (μ/J) F·Fᵀ (22)**.
- **파괴 판정**: σ^E 의 주응력 최대값이 σ_f 를 넘으면 스칼라 손상을 갱신.
- **모델 A — Rankine 손상 + 선형 변형률 연화** (Cervera et al., ref 61):
  > **D^{n+1} = (1 + H_s)(1 − σ_f/max(σ_i^E)) (23)**,  H̄_s = σ_f²/(2EG_f),  H_s = H̄_s l^ch/(1 − H̄_s l^ch)

  파괴 에너지 G_f (Mode I) 와 특성 길이 l^ch 에 묶인다 → K–W · Charpy 에 사용.
- **모델 B — 시간-파괴 (time-to-failure)**: LEFM 은 균열 속도가 Rayleigh 파속에 다가간다고 하지만 관측값은 훨씬 낮다 (*"commonly on the order of 0.4v_r 62"* — 미세균열 탓).  *"the time-to-failure is defined as the transit time for a crack to propagate across a particle, τ = c_f/ℓ"* (인쇄 그대로 — 통과 시간이면 ℓ/c_f 여야 차원이 맞는다 [카드 판독]) · c_f = 균열 속도 (입력) · l^ch = 셀 대각선:
  > **D^{n+1} = min[1, D^n + Δt/τ] (24)**

  *"This approach should give a predictable value of the crack velocity, even as the mesh is refined."* → Brazilian 에 사용.
- **Weibull 크기 의존 강도** (ref 63 · 64) — 연속 손상 모델의 격자 의존을 막는 정칙화 (*"it is necessary to regularize the solution to avoid mesh dependence, for example, by introducing spatial heterogeneity"*):
  > **σ_f/σ̄_f = ((V̄/V)(ln R/ln ½))^{1/m} (25)** (V = 입자 부피 · σ̄_f, V̄ = 기준 강도 · 부피 · m = Weibull 계수 · R = (0, 1) 균일 난수)

  저자 단서: *"there is some evidence that a Weibull distribution may not be physically representative of flaw distributions in many engineering materials (cf., 65)"*.
- **손상의 적용 — 인장 주응력만 깎는다**:
  > **σ_i^+ = (1 − D) σ_i^E (σ_i^E > 0),  σ_i^E (σ_i^E ≤ 0) (26)   σ = Σ_{i=1}^{3} σ_i^+ v_i ⊗ v_i (27)**

  압축 주응력은 그대로 — 깨진 재료도 눌리면 버틴다.
- 범위: *"Both the empirical time-to-failure approach and the strain-softening fracture energy approach are strictly suitable only for Mode I dominated dynamic fracture"* · §3.4 의 재료는 *"not meant to describe a particular material"*.

### 4-10. 구현 · 병렬 (§2.5–2.6)

- **적용 범위**: *"The DFG-partitioning method described herein is applicable to a wide variety of MPM implementations (single-point, GIMP, CPDI, etc.)."*
- **domain scaling**: *"Scaling is applied to failed particles so that the particle diagonal length does not exceed the grid cell spacing Δx, which prevents nonphysical stretching of failed material across the domain."*  + 파괴면은 DFG 로 접촉 쌍으로 나누므로 *"all material separation is physical, as opposed to numerical fracture"*.
- **셀당 입자**: *"Particles are initialized with a resolution of two particles-per-cell in each direction."*
- **이웃 목록**: 처리기 경계 너머까지 유지해야 한다.  성기거나 불균일하면 OctTree (ref 56), 고르면 균일 칸 나누기 (binning) 가 낫다.  **다시 정렬하는 기준**: 정렬 때의 위치를 저장 → 걸음마다 그 위치에서의 변위를 재서 허용 한계 (*"e.g., a small fraction of the neighbor radius"*) 를 넘으면 다시.
- **병렬**: MPI 영역 분할 + OpenMP (정렬 · 입자 → 격자 사상).  Uintah 는 256 K 코어까지 거의 선형 확장 (ref 55).

### 4-11. 의사코드 — 한 걸음 (우리 전사 · 논문에 한 걸음 전체의 순서도는 없음)

```
# (논문 식 · Algorithm 번호) · [카드 판독] = 순서 · 세부는 카드가 이어 붙인 것
(가끔) 이웃 목록 갱신: 마지막 정렬 뒤 변위가 한계를 넘은 입자가 있으면      (§2.5)
for p:  c_p = max(s_p, D_p)                                              (§2.4)
        D̄_p, ∇D̄_p ← 반경 r_p (= 셀 대각선) 안 이웃의 3차 핵 합 / 핵 합    (17)(18)(19)
for i:  ∇D̄_i ← 0 ;  for p, i∈nodes(p): ‖∇D̄_p‖ > ‖∇D̄_i‖ 이면 ∇D̄_i ← ∇D̄_p   (Alg 1)
for p, i∈nodes(p):  ς = 0 if ∇D̄_p·∇D̄_i ≥ 0 else 1                         (Alg 2)
        m_ςi, q_ςi, f_ςi^int, f_ςi^ext, 법선용 Σ ∇S m_ςp, 평균/최대 손상 누적   (1)-(4)(11)(21)
for i, ς:  v̄_ςi = v_ςi + a_ςi Δt                                          (5)(6)
for i (두 장 질량 > ε_m):                                                 (Alg 3)
        separable = (max 손상 = 1) and (min(D̄_1i, D̄_2i) > D̄^min)
        v^cm, 보정 법선 n^cm, 접선 기저
        separable 이고 다가오는 중 → 법선력 + Coulomb 접선력               (14)-(16) ⚠ 부호 규약 §4-2
        separable 아님            → 두 장을 v^cm 에 묶음 (한 장)
        v_ςi = v̄_ςi + f^ct_ςi Δt / m_ςi                                    (13)
for p:  같은 ς(p, i) 로 격자 → 입자: L_p, F_p, v_p, x_p                    (7)-(10) [카드 판독]
        구성 모델: σ^E → 손상 갱신 → 인장 주응력 축소                      (22)-(27)
        실패 입자의 CPDI 영역 축소 (domain scaling)                        (§2.6)
```

### 4-12. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

| 축 | 이 논문 |
|---|---|
| 재료 표현 | **연속체** — 물질점은 구적점.  알갱이는 '표면 표지를 두른 연속체 조각' 으로 나타난다 |
| 형상 | 임의 (원판 · 쐐기 · 블록 · CT 복셀도 가능하다고 서술) — 구 가정 없음 |
| 입도 · 무작위성 | 알갱이 집합의 통계 없음 (Fig. 2 는 개념도).  무작위는 Weibull 강도 난수뿐 (해상도마다 다른 실현) |
| 변형 | 초탄성 큰 변형 (neo-Hookean) — **소성 없음** |
| 변형체–변형체 접촉 | **있음** — 노드마다 두 장 · Coulomb μ · 다가올 때만 접촉 (속도 판정) · 점착 없음 |
| 파괴 | 연속 스칼라 손상 (인장 주응력) + 분리 조건 → 파편끼리 다시 마찰 접촉 |
| 강체 | 없음 (판도 변형체 · 경계는 대칭면) |
| 접촉 해상도 | 셀 한 칸 (§4.2) — 그 안의 틈 · 곡률은 뭉개진다 |

---

## 5. 결과 — 절별

### 5-1. 자기 접촉 검증 (§3.1 · Fig. 7–9)

- 설계: *"we apply the method to problems for which the correct frictional contact solution can be easily obtained with an initialization of multiple material velocity fields and then show that the same solution is produced from a single material field with kernel-based surface detection."*  — 미리 나눈 다중 장 해가 **기준**이다.
- 빌릿 (Fig. 8): SF 는 판에 붙어 옆면이 불룩해지고, 다중 장과 표면 표지 분할은 판 면을 따라 미끄러져 옆면이 거의 곧다 [판독].  *"This verifies that the DFG-partitioning method correctly models self-contact for problems involving large sliding displacement at a contact surface."*
- 쐐기–원판–블록 (Fig. 9): 접촉면이 움직이고 찌그러지는 큰 변형.  SF 는 세 물체가 엉겨 붙고 (속도 낮음), 나머지 둘은 원판이 쐐기와 블록 사이로 밀려 나간다 [판독].
- 저자가 여기서 끌어내는 주장: *"These examples … also support the assertion that the method naturally models frictional contact of fracture surfaces during post-fracture deformation, even if the solid material is undergoing large (potentially inelastic) deformation."*  — 비탄성에 대한 시험은 없다.

### 5-2. 동적 파괴 — Kalthoff–Winkler (§3.2 · Fig. 10–11)

- 균열 각은 분할 방식과 거의 무관 (59.1° ↔ 60.8° ↔ XFEM 60°) 하고 모두 실험보다 10° 낮다 — 구성 모델의 한계.
- 차이는 균열 속도 (DFG 2.0 ↔ SF 1.7 km/s) 와 균열 끝 (*"some evidence that the SF solution favors a grid-aligned crack, but the effect is small"*).
- 요소 삭제 · 요소 사이 균열 방식은 Song et al. (ref 48) 이 *"unacceptable mesh dependence"* 로 보고 (인용).

### 5-3. 에너지 소산과 격자 의존 — Charpy (§3.3 · Fig. 12–14)

- 동기: *"While it is possible to compute the plastic work dissipated in a continuum damage model, this does not account for 'phantom' dissipation due to the velocity-field smearing error in a SF solution."* → 계 전체 에너지 수지.
- 기준선: 두 물체 모두 초탄성으로 푼 탄성 충돌에서 Δx 1 mm 일 때 끝 에너지가 2.5 % 낮다 (*"The MPM conserves mass and linear momentum by construction, but only approximately conserves energy … the less-dissipative methods sacrifice stability."*).
- 결과: DFG 는 세 해상도에서 기대 파괴 에너지 근처 · SF 는 거친 격자에서 과소산 (§3-4 표).  *"While the high-resolution SF and DFG-partitioning results are similar, there is significant error in the low-resolution SF response.  When modeling complex fracture systems … it is not always feasible to apply a high resolution for each fracture in the domain, so the ability of a method to perform reasonably at low resolutions is important."*
- 분리 문턱의 뜻: D̄^min 이 낮으면 균열이 **실패 입자 한 줄** (셀당 실패 입자 하나의 끊긴 줄일 수도), 높으면 균열 양쪽에 한 줄씩 또는 **셀 한 칸씩**.  *"The arbitrariness of this separability threshold seems undesirable, but it is important to understand that a conventional SF MPM solution also prescribes an arbitrary localization domain (that of one grid cell or more, depending on the relative alignment and orientation of the particles and background grid 32)."*
- 권고 값: l^ch = √(Δx² + Δy²) · D̄^min = 0.25 (*"gives reasonable results"*).

### 5-4. 파쇄 · 다짐 — Brazilian (§3.4 · Fig. 15–18)

- 왜 이 문제인가: 팽창 고리 같은 흔한 파쇄 시험은 Mode I 이고 파괴 뒤 접촉이 없다 → *"it is necessary to investigate the response of the method in a problem entailing mixed-mode fracture, crack interactions, large-displacement frictional contact, and large material deformation."*
- SF 의 결함 (Fig. 16): *"the SF solution is generally stiffer, delaying the onset of crack initiation and restricting the formation of new cracks and crack branches.  This is because the stress concentration effect from a single failed particle … is suppressed by the single velocity field over the cell containing that particle."* · 격자 정렬 균열 (거친 격자에서 뚜렷) · 손상이 넓게 번짐 (*"such behavior should be a result of the constitutive model response, not an artifact of the numerical solution"*) · *"This results in increased fragment size and decreased fragment velocity."* · 격자를 조이면 줄지만 *"here, this causes a dramatic dependence of the fragmentation response on mesh resolution"*.
- DFG (Fig. 17 · 18): 또렷한 균열 · 조각끼리 미끄럼 · 세 해상도에서 파편 크기 분포와 평균 속도가 비슷 (§3-5 의 판독값).  해상도마다 강도 난수 실현이 달라 균열 무늬 자체는 다르다 (같은 해상도의 SF ↔ DFG 는 같은 실현).
- 저자 단서: *"To fully capture the physical response of fragmentation, brittle materials will likely require a much more sophisticated constitutive model than the simple forms used for this example, and any such development would require significant experimental validation."*

### 5-5. 계산 효율 (§3.5 · Fig. 19)

§3-6 의 표.  요지: 정렬은 무시할 만하고 (< 0.1 %), 덧비용은 입자마다 이웃을 훑는 DFG 평가이며, 2D 중간 크기에서 +30–50 %.  큰 문제에서 더 느는 것은 구현의 메모리 접근 탓이라는 저자 해석 (측정 근거 = DFG 계산 블록이 전체의 30 %).

### 5-6. 3D · 응용 전망 (§4 · §4.1 · Fig. 20)

- 3D 시연: 강구가 두꺼운 세라믹 원판을 침 → 방사 균열 · 조각 분리.  값 없음.
- 응용으로 든 것: 취성 · 다공 재료의 중규모 모사 (손상 · 연화 · 유도 이방성 · 유체 · 속도 · 열-기계 효과의 이해 → 새 연속체 구성 모델) · 초고속 관통 (모래 · 암석 · 콘크리트) · *"moderate-rate applications, such as modeling powder processing, grain harvesting, excavation, or natural events such as land slides, avalanches, and ice floes"* · 자기 접촉만으로도 에너지 흡수 구조 (헬멧 폼 · 자동차 충격 흡수 구역) 의 붕괴.

### 5-7. 한계 (§4.2)

저자 원문은 §11 표에.  요지 셋: ① 방법의 타당성은 연속 손상 모델이 재료 파괴를 예측하는 능력에 묶인다 ② 연성 파괴 · 전단띠는 비국소 구성 모델이 필요 (구성 모델 쪽 문제) ③ **접촉면은 셀 한 칸까지만 해상** → 다가오는 두 물체 사이에 비물리적 틈 → 알갱이 압밀에서 연속체 밀도가 입자 밀도와 어긋남.

---

## 6. 그림별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/homel2017_mpm_field_gradient_partitioning_fracture_self_contact/` · **전부 손 크롭** (출판사 웹 페이지 캡처에서 PIL 로 · 글자 층이 없어 도구 자동 크롭 불가 · `figures.json` 의 `manual_crop`) · 그림 상자 안쪽 (그림 + 표지 + 캡션) 만 잘랐고 페이지의 '그림 보기 · PowerPoint' 링크는 지웠다 · 화면 캡처 해상도라 작은 글씨는 흐리다.  MPM 관점의 [카드 추론] · [우리 코드 판독] 은 논문 밖 판단이다.

| 그림 | 파일 | 원 캡션 요지 | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | 전통 접촉의 그림 — (a) 두 재료 묶음의 접촉 (b) 첫 속도장의 입자 + 둘째 장이 준 노드 접촉력 (c) 둘째 장의 입자 + 첫 장이 준 노드 접촉력 | 접촉 묶음을 **미리** 속도장으로 나누는 방식 (Bardenhagen 계열 = 후보 A′ 의 기본꼴).  우리 MPM 은 이 그림의 '나누기 전' — 장 하나 [우리 코드 판독] |
| 2 | `fig_2.png` | 알갱이 · 다공 계의 2D 마찰 접촉을 위한 속도장 분할 — (a) 전통 방식은 이웃 알갱이가 다른 장이 되도록 많은 장이 필요 (b) 표면 탐지 + 기울기 분할은 재료 묶음 하나에서 마찰 접촉 (c) 기공 안쪽 면 · 파괴면처럼 미리 알 수 없는 접촉 = '자기 접촉' 은 전통 방식으로 불가 | ★ 이 카드의 핵심 그림.  (a) 알갱이마다 다른 색 ↔ (b) 모두 한 색 + 붉은 표면 테.  후보 A′ 의 '장 수' 문제를 **장 2 개**로 바꾸는 길.  단 한 노드에 셋 이상이 만나는 자리의 정확도는 수치가 없다 |
| 3 | `fig_3.png` | 균열이 입자와 노드 사이에 있는지로 두 장에 분할 (ref 34) — (a) 명시적 균열 (b) 위 가운데 노드에서의 분할 (c) 아래 가운데 노드에서의 분할.  같은 입자가 노드마다 다른 장에 속할 수 있다 | 장 번호가 전역 꼬리표가 아니라 **노드별 판정**이라는 이 방법의 바탕.  우리가 '알갱이 = 장' 으로 생각하던 것과 다른 자료 구조 |
| 4 | `fig_4.png` | 인장 봉의 손상장 — (a) 정규화 안 한 핵 손상장 D(x) (b) 핵 합 S(x) 로 표면 탐지 (c) 정규화한 D̄(x).  정규화가 가장자리 효과를 없앤다 | (b) 의 등고선 띠 (≈ 1–2 셀 [판독]) 가 표면 표지 띠의 두께 규모.  (a) 처럼 정규화를 빼먹으면 자유 표면이 '균열' 로 읽힌다 — 구현 함정 |
| 5 | `fig_5.png` | 굽은 균열 둘레의 노드별 분할 — 노드의 비국소 기울기 (검은 화살표) 와 입자 기울기 (붉은 화살표) 의 상대 방향으로 입자를 색칠 (장 1 주황 · 장 2 파랑) | Algorithm 1 · 2 의 그림판.  셀당 입자 3 × 3 (이 그림만 · 본문).  균열 끝에서는 방향이 법선이 아니지만 분리 조건이 안 서 무해 |
| 6 | `fig_6.png` | 누적 손상 대신 **지정한 표면 표지**로 재료 경계면에 마찰 접촉을 만드는 그림 | ★ 자기 접촉.  오른쪽 확대의 두 표면 띠 사이 **흰 틈 ≈ 1 셀** [판독] = 저자가 §4.2 에서 가리키는 비물리적 틈 (*"This can be seen clearly in Figure 6"*) → 압밀 기공률에 계통 오차 |
| 7 | `fig_7.png` | 2D 평면변형 빌릿 자기 접촉 문제의 도식 | 판 사이 압축 (4 분면 · 대칭 둘 · 일정 견인력) = 우리 판–SE 접촉의 가장 가까운 꼴 → 단계 3 · U2 회귀 시험의 원형 |
| 8 | `fig_8.png` | 탄성 빌릿 평면변형 압축의 수평 속도 — 왼쪽 SF (붙음) · 가운데 다중 장 (마찰) · 오른쪽 한 묶음 + t = 0 표면 탐지 → 다중 장 해와 매우 비슷 | ★ 검증 1.  왼쪽 (= 우리 MPM 방식) 은 판에 붙어 불룩, 나머지는 미끄러져 옆면이 곧다 [판독].  **눈 대조** — 판 반력 · 오차 노름 없음.  우리가 재현할 때는 수치 (반력 · 옆면 변위) 를 같이 낼 것 |
| 9 | `fig_9.png` | 큰 변형 평면변형 마찰 접촉 — 아래 SF (붙음) · 가운데 미리 나눈 다중 장 · 위 한 묶음 + 표면 탐지 → 다중 장 해와 매우 비슷 | ★ 검증 2 (쐐기 → 원판 → 블록 · 0.2 · 8.0 · 9.6 µs).  세 물체지만 접촉은 쌍으로만 — **셋이 한 노드에 만나는 시험이 아니다**.  재료 · 격자 · μ 미인쇄 |
| 10 | `fig_10.png` | 2D 평면변형 동적 전단 파괴 문제의 도식 — Kalthoff–Winkler 실험은 노치에서 70° 로 균열 (ref 66) | 파괴 판 (R7) 의 벤치마크 후보.  압밀과 하중 양식이 다르다 |
| 11 | `fig_11.png` | K–W: (a) 실험의 초기 균열 방향 (ref 68) (b) 명시적 균열 MPM (Nairn, ref 69) (c) XFEM (Song, ref 48) (d) 이 논문 DFG 분할 (e) 이 논문 SF | 각 59.1° (DFG) · 60.8° (SF) · 60° (XFEM) ↔ 실험 70° (본문).  각은 구성 모델이 정하고 분할은 속도 · 끝 모양을 바꾼다.  (b) 의 명시적 균열 MPM 은 그림에 70 표지 [판독] |
| 12 | `fig_12.png` | 변형 Charpy 충격 문제의 도식 — 붉은 점선을 따라 균열 하나 | 에너지 수지 시험.  남은 단면 8 × 2 = 16 mm² [카드 산술] |
| 13 | `fig_13.png` | Charpy 의 에너지 소산 — SF ↔ DFG.  DFG 가 격자 의존이 덜하고 올바른 파괴 에너지를 낸다 | ★ 정량 검증.  처음 ≈ 1005 mJ → 이상선 ≈ 651 mJ · 노란 띠 = 수치 소산 2.5 % 몫.  끝값 [판독]: DFP 618 / 632 / 637 ↔ SF 568 / 598 / 627 mJ (Δx 1.00 / 0.50 / 0.25 mm) — 한 속도장의 '가짜 소산' 을 재는 시험 꼴 |
| 14 | `fig_14.png` | Charpy (Δx 0.5 mm) 에서 D̄^min · l^ch 를 바꾼 결과 — 왼쪽 속도 크기 + 손상 (검정), 오른쪽 에너지 · 속 그림은 l^ch = √(Δx² + Δy²) 에서 D̄^min 별 상세 (0.01 · 0.125 · 0.25 는 겹침) | 수치 손잡이 민감도.  l^ch ½ 배 → 끝 ≈ 523 mJ (소산 1.3 배) · 3/2 배 → ≈ 662 mJ [판독].  **특성 길이가 파괴 에너지를 정한다** — R5 (맞추는 값은 하나) 에서 세어 둘 숫자 |
| 15 | `fig_15.png` | 2D 평면변형 동적 Brazilian 문제의 도식 | 판 둘 + 원판 + **옆 대칭면** → 파편이 옆벽에 부딪혀 다시 다져진다 = 닫힌 다이 안 파쇄 · 다짐의 2D 꼴 |
| 16 | `fig_16.png` | **SF** 로 푼 Brazilian (세 해상도) — 첫 열 Weibull 상대 강도, 나머지는 속도 크기 + 손상.  속도장 번짐 오차가 응력 집중을 가리고 균열 형성을 누르며 알갱이 흐름에 비물리적 소산을 낸다 → 파편 크기 · 속도의 뚜렷한 격자 의존 | ★ 우리 MPM 방식으로 파쇄 뒤 흐름을 풀 때 생길 결함의 그림 — 늦은 균열 (시각 축이 DFG 의 두 배) · 격자 정렬 · 번진 손상.  행 표지 n_p 14,441 · 57,457 · 129,533 |
| 17 | `fig_17.png` | **DFG 분할**로 푼 Brazilian (세 해상도) — 깨끗한 균열 · 파편의 마찰 미끄럼 · 파편 크기 · 속도가 해상도에 걸쳐 비슷 (작은 차이는 강도 실현 차) | 균열이 만나는 자리 (셋 이상의 조각) 가 '완전 손상 셀' 로 나타난다는 §2.2 설명이 걸리는 장면 — 그 자리의 오차는 따로 재지 않았다 |
| 18 | `fig_18.png` | 파편 크기 분포 — SF (왼쪽) ↔ DFG (오른쪽) · 세 해상도.  속 그림 = 평균 속도.  DFG 가 속도 · 크기 분포 모두에서 격자 의존을 크게 줄인다 | 평균 속도 [판독]: SF ≈ 45 → 113 → 132 ↔ DFP ≈ 107 → 147 → 139 m/s.  비교 시각이 다르다 (DFG 10 µs ↔ SF 15 µs).  속 그림의 분홍 띠의 뜻은 캡션에 없음 [미확인] |
| 19 | `fig_19.png` | Brazilian 한 걸음의 평균 실행 시간 ↔ 입자 수 — 1 스레드 · 16 스레드 × SF · DFG.  점선 맞춤의 기울기 = 확장 효율 | 기울기 (인쇄) 1.23 · 1.01 · 1.27 · 0.89.  ⚠ 2D · 셀당 2 × 2 × 1 — 3D 는 이웃 수 ≈ 7 배 [카드 산술] 라 이 비율을 옮길 수 없다 |
| 20 | `fig_20.png` | 3D 충격 파쇄 예 — 속도 등고선.  DFG 분할 + 대규모 병렬 틀 | 유일한 3D 그림.  재료 · 격자 · 입자 수 · 시간 없음 — **3D 정량 검증 0 건** |
| Table 1 | `tab_1.png` | 빌릿 자기 접촉 모사의 입력값 | μ 0.04 · σ_t 200 MPa.  ⚠ 빌릿 탄성값이 본문 (*compliant*) · 그림과 안 맞음 (§3-1) — 이 표로 재현하지 않는다 |
| Table 2 | `tab_2.png` | Kalthoff–Winkler 문제의 입력값 | ⚠ w_t '10 mm' · G_f '22.3' 두 곳이 본문 · 산술과 어긋남 (§3-3) |
| Table 3 | `tab_3.png` | Charpy 충격 파괴 문제의 입력값 | ⚠ D̄^min '0.25 mm' · G_f 22.3 (354.1 mJ 는 22.13 을 지지) · l^ch 1.414 mm 는 Δx 1 mm 때 값 |
| Table 4 | `tab_4.png` | 동적 파쇄 / 다짐 모사의 입력값 | ⚠ 스크롤 상자 — 보이는 15 행만 (마찰계수 · D̄^min 행이 안 보임 [미확인]) |

**식 · 알고리즘 그림 (손 크롭 · 카드의 식은 이 그림들에서 옮겼다)**: `eq_01_06_mpm_p2g_forces_grid_update.png` · `eq_07_10_velocity_gradient_g2p_update.png` · `eq_11_13_surface_normal_cm_velocity_contact_update.png` · `eq_14_16_normal_tangential_coulomb_contact_force.png` · `eq_17_19_kernel_damage_field_normalization.png` · `eq_unnumbered_s2_2_sign_rule_nonlocal_gradient.png` · `eq_20_alg_1_nonlocal_node_dfg.png` · `alg_2_p2g_dfg_partitioning.png` · `eq_21_separability_condition.png` · `alg_3_frictional_contact_separability.png` · `eq_22_24_neo_hookean_rankine_time_to_failure.png` · `eq_25_27_weibull_strength_damage_stress_scaling.png`.

---

## 7. Post-processing

| 무엇 | 어떻게 | 우리에게 |
|---|---|---|
| 접촉 표현의 검증 | 같은 문제를 SF · 미리 나눈 다중 장 · 표면 표지 분할로 풀어 속도 등고선을 나란히 (Fig. 8 · 9) | 단계 3 의 설계 그대로.  단 우리는 판 반력 · 옆면 변위 · 미끄럼량을 **숫자로** 같이 낸다 (논문은 눈 대조) |
| 균열 각 · 속도 | 손상 지도에서 끝 각 · 시각별 균열 끝 위치 → 속도 (구하는 절차는 미인쇄) | R7 판의 검증 지표 후보 |
| **계 전체 에너지 수지** | 계 전체 에너지 (*total energy* — 운동 + 변형 에너지로 읽음 [카드 판독]) 의 시간 이력 · 탄성 충돌로 수치 소산 기준선 (2.5 %) 을 먼저 재고 · 기대값 G_f A_f 선과 띠를 같이 그림 (Fig. 13) | ★ 접촉 · 분리 알고리즘의 수치 소산을 재는 틀 — 탈압 · 되튐 단위 시험 (U3 · U4) 에 '해석 기대값 + 수치 소산 띠' 를 같이 그린다 [카드 추론] |
| 손잡이 민감도 | D̄^min · l^ch 를 하나씩 바꿔 에너지 이력을 겹침 (Fig. 14) | 수치 손잡이 (표지 띠 두께 · 핵 반경 · D̄^min) 의 민감도 표를 결과 전에 등록 |
| 파편 분석 | 손상 안 된 재료의 연결 성분 (ref 71) → 공칭 지름의 누적 분포 · 평균 속도 ↔ 입자 수 (Fig. 18) | AM 파괴 판에서 파편 크기 분포 — 우리 DEM 의 파괴 통계와 견줄 관측량 |
| 격자 민감도 | 세 해상도 (Δx 비 ≈ 1 : 0.52 : 0.35) 를 같은 그림 틀로 (Fig. 16–17) · 해상도마다 다른 난수 실현임을 명시 | 난수 실현 차와 격자 차를 구분해 적는 보고 방식 |
| 비용 | 걸음당 평균 시간 ↔ 입자 수 log–log · 맞춤 기울기를 그림에 인쇄 · 코드 블록별 시간으로 몫 분해 (Fig. 19) | 커널 프로파일 보고 꼴 |
| 도구 | GEOS · VisIt (입자를 CPDI 영역 모양으로 렌더) · 연결 성분 알고리즘 | — |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | Homel & Herbold 2017 | 우리 DEM (LIGGGHTS) | 우리 MPM (Taichi scaffold) |
|---|---|---|---|
| 이산화 | CPDI + domain scaling · 삼선형 형상함수 · ∇S 로 내부력 · USL · 명시 | 구 입자 · 접촉 법칙 | MLS-MPM · APIC · 2차 B-spline · 명시 [`hu2018…` 카드 §0] |
| 셀당 물질점 | 방향당 2 개 (2D 2 × 2 × 1) | — | 방향당 2 개 (셀당 8) [우리 코드 판독 · 2361–2362 행] |
| 재료 | neo-Hookean + 스칼라 인장 손상 (Rankine 연화 / 시간-파괴) + Weibull 강도 · **소성 없음** | hooke/hysteresis (탄성 + 이력) | fixed-corotated 응력 + J2 반환 (소성) [`hu2018…` 카드 §8-1] |
| 격자 속도장 | **노드마다 2 개** (접촉 묶음 G 개면 2G) — 알갱이 수와 무관 | — | **1 개** [우리 코드 판독 · 2808 행] |
| 변형체–변형체 접촉 | 마찰 (Coulomb μ) · 다가올 때만 (속도 판정) · 점착 없음 · 셀 한 칸 해상 | 있음 (마찰 · 분리 · 점착 선택) | 없음 (붙음) |
| 표면의 기억 | 입자의 표면 표지 s_p (처음 닿아 있으면 칠해 넣기) | 입자 자체 | 없음 — 단 `--se-dump` 씨앗은 점마다 SE 구 번호를 갖는다 (`se_id_base` [우리 코드 판독 · 2351–2352 행]) |
| 파괴 | 연속 손상 + 분리 조건 → 파편 마찰 접촉 | 힘 기반 파괴 판정 (Auerbach · 접촉 소실) [우리 기록] | 킷의 fracture-scaffold (선택 · crack-void) [우리 기록 · CLAUDE.md 2026-07-23 절] — 손상장 · 파편 접촉 없음 |
| 강체 / 경계 | 판도 변형체 · 대칭면 | 판 메시 | 노드 조건 (AM 마스크 · 판 · 벽) |
| 차원 · 규모 | 2D ≤ ≈ 2.3 × 10⁵ 입자 [판독] · 3D 시연 (값 없음) · CPU 16 스레드 | 3D 10⁴–10⁵ 입자 | 3D 10⁷–10⁸ 물질점 (GPU) [우리 기록] |
| 하중 | 동적 (충격 20 · 33 m/s · 일정 견인력 200 · 650 MPa · 결과가 µs–ms 척도) | ≈ 300 MPa 준정적 압축 | ≈ 300 MPa 급 압축 (판 Mach 0.01–0.03) |
| 검증 | 다중 장 해와 눈 대조 · K–W 각 · 속도 · Charpy 에너지 · Brazilian 격자 민감도 | 실험 기공 · 접촉 겹침 | 실험 기공 (보정) · DEM 두께 대조 |
| 탈압 | 없음 | 있음 | 부분 |
| 수송 (σ) | 없음 | 접촉망 | 복셀 (STEP3) |

### 8-2. 이 방법을 우리 MPM 에 얹는다면 — 저장 · 비용 산술 [카드 산술 · 전부 논문 밖]

- **격자**: 장 하나 = 속도 3 + 질량 1 = f32 16 B/노드 → 384³ 노드에서 0.906 GB.  **장 2 개 = 1.81 GB** ↔ 알갱이별 장 ≈ 30 TB (`comparison_vs_ours_DEM.md` §C [Bardenhagen00] 줄의 우리 산술 — SE 씨앗 32,832 개).  여기에 노드 대표 기울기 (12 B → 0.68 GB) · 장별 법선 (2 × 0.68 GB) · 장별 평균 / 최대 표지 (16 B → 0.91 GB) 를 다 저장해도 합 ≈ 4.8 GB.
- **입자**: 표지 + 기울기 (f32 × 4 = 16 B) → 10⁸ 점에서 1.6 GB.
- **이웃**: 3D 에서 반경 √3 Δx 안에 ≈ 174 점 (셀당 8 점) → 이웃 목록을 통째로 저장하면 174 × 4 B × 10⁸ ≈ 70 GB (불가) → 셀 묶음 (cell list) 으로 그때그때 훑어야 한다.  걸음당 핵 평가 ≈ 174 × 점 수.
- **이산화 차이**: 논문은 삼선형 (노드 지지 2 셀) + CPDI 영역, 우리는 2차 B-spline (지지 3 셀).  Algorithm 1 의 "노드에 얹히는 입자" 범위가 넓어지므로 표지 띠 두께 · 핵 반경의 권고 (*consistent with the kernel radius*) 를 그대로 옮길 수 없다 — 우리 이산화에서 다시 재야 한다.
- **칠해 넣기**: 우리 침대는 DEM 압축 뒤 좌표에서 씨앗을 뿌리므로 SE 구끼리 처음부터 닿아 (겹쳐) 있다 = 저자가 말한 *"it would be necessary to 'paint in' the surface flag at initialization"* 의 경우.  점마다 SE 구 번호가 있으므로 "자기 구 표면까지의 거리 < 띠 두께" 로 칠할 수 있다.  ⚠ DEM 구는 서로 겹쳐 있어 (렌즈) 겹친 부분의 점은 한쪽 구에만 속한다 (가장 가까운 구 중심) — 경계면이 구 표면이 아니라 두 구의 중간면 (Voronoi 면) 이 된다는 점을 띠 정의에 반영해야 한다.

### 8-3. 전이되는 것 / 안 되는 것

- ✅ **알고리즘**: 핵 손상장 (식 17–19) · 노드 대표 기울기 (Algorithm 1) · 내적 부호 분할 (Algorithm 2) · 분리 조건 + 접촉 (Algorithm 3) · 표면 표지 (§2.4) · 다시 정렬 기준 (§2.5).
- ✅ **검증 설계**: SF ↔ 다중 장 ↔ 분할 세 해 (Fig. 8 · 9) · 에너지 수지 + 수치 소산 띠 (Fig. 13).
- ✅ **저자의 경고 문장**: 접촉 틈과 알갱이 압밀의 밀도 불일치 (§4.2) · N > 2 장의 침투 (§1.1.1) · 실패 층이 인장을 전달 (§1.1.2) · 3D 에는 색 상한 없음 (§1.1.1).
- ✅ **정성 결론**: 한 속도장은 거친 격자에서 과소산 · 격자 의존 (Charpy · Brazilian).
- ❌ 재료값 · 에너지 · 속도 · 균열 각 · 파편 크기의 절대값 — 가상 재료 · 동적 하중.
- ❌ 비용 비율 (+30–50 %) 의 3D · GPU 전이 — 2D · 16 스레드 CPU · 이웃 25 개 기준.
- ❌ 해상도 규칙 — 지름당 셀 수 같은 규칙이 **없다** (Brazilian 은 지름당 55–159 셀로 우리 SE ≈ 7 셀보다 훨씬 곱다 [카드 산술 · 우리 기록]).
- ❌ "자기 접촉이 검증됐다" 는 지위 — 눈 대조 두 건 · 쌍 접촉뿐 · 소성 없음 · 조밀 충전 없음.
- ⚠ 인쇄된 식의 부호 · Algorithm 3 의 22 행 — 그대로 옮기지 않는다 (§12).

### 8-4. frame 판정

- **frame [5] (분업)**: 이 논문은 MPM 쪽에 **변형체끼리의 접촉 자유도** (미끄럼 · 분리) 와 **파괴 뒤 접촉**을 더한다 — DEM 고유로 둔 것의 일부 (R2 미끄럼 · 분리 · R3 입자 경계 기억 · R7 파괴) 를 MPM 틀로 가져올 길이고, Bardenhagen 식 (후보 A′) 의 3D 장 수 문제를 피한다.  그러나 접촉망 관측량 (배위수 · 접촉 면적 · 접촉별 힘) 은 나오지 않는다 — 노드 단위의 두 장일 뿐 '어느 알갱이와 어느 알갱이' 의 접촉 목록이 없다 [카드 판독].  수송 분업은 그대로.
- **frame [4] (교차 맞춤 금지)**: 이 논문에는 실험에 맞춘 값이 없다.  우리가 이 접촉을 넣으면 실험 (기공 · 두께) 에 따로 보정하고 DEM 과 맞추지 않는다.  D̄^min · 띠 두께 · 핵 반경은 **보정값이 아니라 수치 손잡이**로 결과 전에 고정한다.
- **frame [1]/[2] (연화)**: 중립 (소성 · 연화 영률을 다루지 않는다).  다만 *"artificial 'welding'"* 진술은 "한 속도장 안의 구성식만으로는 빠진 것이 접촉 자유도일 수 있다" 는 가설 (`comparison_vs_ours_DEM.md` §C [Bardenhagen00] 줄) 을 받치는 또 하나의 제3자 문장이다.

---

## 9. 깊은 통찰

① **장 수를 알갱이 수에서 떼어 낸다 — 비용이 '격자 메모리' 에서 '입자 이웃 훑기' 로 옮겨 간다.**  후보 A′ 를 Bardenhagen 꼴로 하면 3D 에서 장 수의 상한이 없고 (저자 문장), 우리 산술로 real_14 는 ≈ 30 TB 다.  이 방법은 노드당 두 장 (≈ 1.8 GB) 이지만 그 값으로 입자마다 반경 √3 Δx 의 이웃 ≈ 174 개 [카드 산술] 를 훑는다.  2D 의 +30–50 % 는 이웃 25 개일 때의 값이다 — 3D 덧비용은 논문에 없고, 우리가 재야 하는 첫 숫자다 (§10 행동 6).

② **얻는 것의 값은 '셋 이상이 만나는 노드' 에서 치른다.**  두 장은 노드마다 접촉 평면 **하나**를 뜻한다.  저자는 균열 교차에 대해 "손상 모델의 균열은 폭이 있어 교차점이 완전 손상 셀로 나타난다" 고 설명할 뿐 시험하지 않았고, 미리 나눈 장이 셋 이상일 때는 쌍별 힘이 침투를 엄밀히 막지 못한다고 스스로 적었다.  조밀한 알갱이 층은 세 알갱이가 만나는 선 (3D) 이 구조의 일부다.  ⇒ 이 방법의 근사 오차는 **노드당 알갱이 수 ≥ 3 인 노드의 비율**로 미리 가늠할 수 있다 — 그 통계는 Bardenhagen 2001 의 N ≤ 2 가정 점검으로 이미 계획한 것과 같은 계산이다 (GPU 불요).

③ **한 속도장의 결함에 크기가 붙었다 — 그리고 탈압과 직접 닿는다.**  *"a tensile member containing a single layer of failed (or even deleted) particles can still support a tensile load, when the particle width is less than the grid cell spacing"* — 한 속도장에서는 계면에 '끊긴 층' 을 두어도 인장이 건너간다.  우리 MPM 이 판을 물릴 때 SE–SE · SE–AM 계면이 열리지 않고 당겨지는 것이 원리적으로 그 경우다 [카드 추론].  크기: Charpy 에서 한 속도장은 거친 격자 (남은 단면 8 셀) 에서 파괴 에너지를 23 % 더 쓰고 (분할은 9 % · 둘 다 탄성 충돌의 기준 소산 ≈ 25 mJ ≈ 7 % 를 포함 · [판독 · 카드 산술]), Brazilian 에서는 평균 파편 속도가 가장 거친 격자에서 절반 아래다 (45 ↔ 107 m/s [판독]).  — 다른 재료 · 동적 하중이라 숫자는 옮기지 않지만, **"한 속도장의 오차는 격자를 조여야만 준다"** 는 방향은 우리 dx 수렴 시험이 접촉 표현에 따라 다른 답으로 수렴할 수 있다는 경고다.

④ **접촉 틈은 저자가 스스로 가리킨 압밀의 함정이다.**  *"Contact surfaces in the MPM are resolved to within a single grid cell spacing, which … can also result in a nonphysical gap at the contact surface between two approaching bodies. … for compaction of granular materials (or porous materials with a high internal surface area), this could lead to a value of the continuum density that is inconsistent with the particle density."*  접촉 MPM (A′ · 이 방법 모두) 으로 기공률을 재면 알갱이마다 표면에 ≈ ½ 셀의 '서 있는 거리' 가 붙는다 — 지름 7 셀인 SE 라면 지름의 ≈ 14 % 규모 [카드 산술 · 틈 = 1 셀 가정] 로, 기공률에 주는 영향이 실험 표적의 차이 (수 %p) 보다 클 수 있다 [카드 추론].  ⇒ 기공률 연산자 (단계 0) 는 '판 위치 ÷ 고체 질량' 으로 정의하되 **dx 사다리로 틈의 몫을 먼저 뺀 뒤** 실험과 견준다.  이 틈은 저자 말대로 MPM 접촉 일반의 성질이라 한 속도장에서도 '다가와서 만나는' 면에는 생긴다.  다만 우리 지금 MPM 은 SE 를 처음부터 이어진 연속체로 뿌리므로 SE–SE 면에는 틈이 없다 (붙음).  표지 분할을 넣으면 처음 닿아 있던 면은 틈 없이 시작하되, 미끄러져 **새로 만나는 면**은 ≈ 1 셀 거리에서 접촉이 걸린다 → 같은 침대라도 접촉 표현을 바꾸면 재배열이 많을수록 기공률이 큰 쪽으로 밀릴 수 있다 [카드 추론 — 크기는 재야 안다].

⑤ **검증의 꼴은 가져오고, 검증의 수준은 가져오지 않는다.**  "미리 나눈 다중 장 해를 정답으로 두고 새 방법을 견준다" 는 설계는 단계 3 에 그대로 쓸 수 있다.  그러나 이 논문의 판정은 그림 대조이고, 접촉 자체의 해석해 시험 (경사면 · Hertz) 이 없다.  접촉 알고리즘의 정량 근거는 여전히 Bardenhagen 2000 · 2001 (경사면 원판 · 구) 에 있고, 표면 표지 분할이 그 시험을 통과하는지는 **아무도 보이지 않았다** → 우리 U2 가 처음이다.

⑥ **에너지 수지 시험은 '알고리즘의 가짜 소산' 을 재는 일반 도구다.**  탄성 충돌로 기준 소산 (2.5 %) 을 먼저 재고, 기대값 (G_f A_f) 선과 그 띠를 그린 뒤 방법들을 겹친다.  우리 쪽 대응: 탄성 구 두 개의 접근–이탈 (접촉 · 분리 알고리즘의 소산) · 단단한 구를 소성 블록에 눌렀다 떼기 (U3: 소성 일 + 되돌아온 탄성 에너지 = 기대값) 에 같은 그림 틀 [카드 추론].

⑦ **수치 손잡이가 늘어난다 — R5 (맞추는 값은 모델마다 하나) 의 장부에 올릴 것.**  D̄^min (0.25) · 핵 반경 (셀 대각선) · 표지 띠 두께 (*"consistent with the kernel radius"*) · 표면 탐지 문턱 · 질량 하한 ε_m · 다시 정렬 한계 · μ.  Fig. 14 는 그중 하나 (l^ch) 가 결과 (소산) 를 30 % 바꿈을 보인다 — 저자도 *"can be tuned"* 라고 적는다.  우리는 이 값들을 **결과 전에 고정**하고 민감도 표만 낸다.

⑧ **표지 띠 · 핵 반경 · 노드 지지 폭의 관계가 분할의 성패를 정한다 [카드 추론].**  정규화장 D̄ 는 반경 r_p 안의 이웃이 모두 표지 입자면 1 로 평평해져 기울기가 0 이다 — 기울기는 표지 입자와 비표지 입자가 함께 보이는 곳에만 있다.  띠가 핵 반경보다 두꺼우면 접촉면 바로 옆 입자의 기울기가 0 이 되어 (내적 0 → 장 0) 두 알갱이가 같은 장에 들어가고, 너무 얇거나 알갱이가 가늘면 한 알갱이의 양쪽 면 기울기가 마주 보아 **스스로 갈라질** 수 있다.  논문은 이 관계를 한 구절로만 적는다.  ⇒ U1 (입자 하나 압축) 에 "표지를 두른 입자가 스스로 두 장으로 갈라지지 않는가" 를 넣고, 지름당 셀 수 사다리의 아래쪽 (≤ 6 셀) 에서 먼저 본다.

⑨ **분리는 속도 판정뿐이고 점착이 없다 — 탈압에서 둘 다 문제다.**  Bardenhagen 2001 이 고친 것 (압축이 남았는데 멀어지는 속도만으로 놓아 버림 → 되튈 때 에너지 오차) 이 그대로다.  그리고 표지는 지워지지 않는다 — 300 MPa 에서 SE–SE 가 냉간 접합 (소결 · 입계 형성) 되는 것을 나타내려면 표지를 지우는 규칙 (분리 조건의 반대) 이 따로 필요하다.  분리 조건 (Algorithm 3 의 separable) 이 바로 그 스위치 자리다 — 손상 대신 '접합 상태' 를 실으면 붙음 ↔ 미끄럼을 계면마다 고를 수 있다 [카드 추론].

⑩ **2D → 3D 에 대해 원문이 준 것은 "3D 가 더 어렵다" 는 방향뿐이다.**  색 수 (4 ↔ 상한 없음) · 핵 반경 · 비용.  정량 검증이 전부 2D 평면변형이므로, 우리 단계 2–3 (2D) 에서 이 방법이 통과해도 3D 의 정확도 (특히 세 알갱이 선 · 네 알갱이 점) 는 따로 보여야 한다.

⑪ **R7 (AM 파괴) 에는 '깨진 뒤' 가 핵심이다.**  손상 모델만 넣으면 (한 속도장) 깨진 조각이 서로 붙어 응력 집중이 가려지고 파편이 크고 느리게 나온다 (Fig. 16).  NCM 2차 입자의 파쇄 (우리 DEM 은 힘 기반 판정 뒤 접촉 소실로 처리 [우리 기록]) 를 MPM 에서 풀려면 손상 + 분할이 한 벌이어야 한다.  인장 주응력만 깎는 식 (26) 은 닫힌 균열이 압축을 전달하게 한다 — 300 MPa 압축 중 파괴에 맞는 꼴이다.  값 (σ_f · G_f · Weibull m) 은 이 논문에서 가져오지 않는다.

⑫ **인쇄된 식을 믿지 않는다.**  법선 부호 규약 (식 11 ↔ 접촉 조건 셋) · Algorithm 3 의 22 행 · τ = c_f/ℓ · 표 값들.  서로 다른 자리에서 같은 양이 다르게 적혀 있다 → 구현은 단위 시험이 정하고, 원고에 식을 옮길 때는 Bardenhagen 2001 식 (8)–(13) 의 속도 꼴을 쓴다.

---

## 10. [DEM 우선 (수영)] — 후보별 함의 + 구체 행동

| 후보 | 이 논문의 함의 | 판정 |
|---|---|---|
| **A′** (입자마다 속도장 · 다물체 마찰 접촉) | 장을 알갱이마다 두지 않고 **노드마다 두 장**으로 같은 접촉 (Bardenhagen 식) 을 건다 — 3D 장 수 · 메모리 문제의 출구.  값: 입자 이웃 훑기 (3D ≈ 174 개) · 셋 이상이 만나는 노드의 근사 · 수치 손잡이 여럿 | ✅ 구현 방식의 원전 · ⚠ 정량 검증 (접촉 해석해 · 조밀 충전 · 소성) 은 우리 몫 |
| **A′-0** (판 · 벽 · AM 자리에만 접촉 규칙) | 빌릿 시험 (Fig. 7–8) 이 판–재료 마찰의 2D 회귀 시험 꼴.  표면 표지 방식은 판을 '재료' 로 둘 때만 해당 — 우리 판은 노드 조건이라 식 (14)–(16) 을 노드 조건으로 쓰는 쪽이 싸다 (`hu2018…` 카드의 식 25 와 같은 내용) | ✅ 시험 꼴 |
| **A** (AM = 움직이는 강체 · SE 한 속도장) | 직접 닿지 않음.  다만 "SE 는 한 속도장" 인 한 SE–SE 는 붙는다는 것 (§1.1.1) 과, 접촉 묶음 G 개 × 2 장의 결합 규칙 (§2.3) 이 A + (SE 자기 접촉) 의 혼합 설계에 쓰인다 | 중립 (혼합 설계의 부품) |
| **B** (입자마다 유한요소 + 접촉) | 관련 없음 (라그랑주 FEM 은 K–W 민감도 언급 한 줄) | — |
| **C / C′** (접촉 법칙 DEM) | 관련 없음 (DEM 언급 없음) | — |
| **D0** (지금 DEM) | 관련 없음 | — |
| **M0** (균질화 압밀) | 관련 없음.  중규모 모사로 연속체 구성 모델을 만든다는 전망 (§4.1) 만 | — |
| 조건 **R7** (AM 파괴) | 손상 + Weibull + 분할이 한 벌 — 깨진 뒤 파편의 마찰 접촉까지.  한 속도장만으로는 파편 크기 · 속도가 격자에 묶인다 | ✅ 방법 · ⚠ 재료값은 따로 |
| 조건 **R4** (탈압) | 분리 = 속도 판정 · 점착 없음 · 시험 없음 | ⚠ 그대로 쓰면 Bardenhagen 2001 이 고친 문제가 남는다 |

**구체 행동 (순서 = 싼 것 → 비싼 것; 전부 [카드 추론] · 결과 전 등록 대상)**
1. **노드당 알갱이 수 통계 (GPU 불요)** — real_14 씨앗을 알갱이 번호별로 격자에 얹어 '두 알갱이 노드' · '셋 이상 노드' 의 비율을 지름당 셀 수와 함께 적는다.  셋 이상 비율 = 이 방법 (두 장) 이 근사가 되는 자리의 크기이자 Bardenhagen 2001 의 N ≤ 2 가정 위반 비율 (이미 계획한 선행 점검과 같은 계산).
2. **부호 규약 단위 시험** — 두 블록의 접근 / 이탈에서 접촉력의 방향 · 분리를 확인하고, 그 결과로 식 (11) · (14) · Algorithm 3 16 행의 규약을 우리 문서에 고정 (U0 · U2 앞).
3. **2D 빌릿 시험 재현 (단계 3)** — 판 사이 압축을 (i) 한 속도장 (ii) 판 · 빌릿 두 장 (iii) 표면 표지 분할로.  관측량은 판 반력 · 옆면 변위 · 접촉면 미끄럼량 · 에너지 — 논문이 내지 않은 숫자.  재료값은 Table 1 이 아니라 우리 것 (빌릿 = 무른 탄성 / J2).
4. **띠 두께 × 핵 반경 × 지름당 셀 수 사다리 (U1 · U5)** — 표지를 두른 입자 하나가 스스로 갈라지지 않는가 · 두 입자가 접촉면에서 제대로 두 장으로 나뉘는가.  우리 2차 B-spline (지지 3 셀) 에서.
5. **접촉 틈의 수치화 (U6 앞)** — 두 블록을 눌러 평형 틈 / dx 를 재고, 작은 조밀 충전에서 dx 사다리로 기공률의 틈 몫을 뺀다 (§4.2 저자 경고의 숫자판).  한 속도장 해와 나란히 (처음부터 이어 뿌린 면 ↔ 다가와 만나는 면을 구분해서).
6. **3D 비용 프로브** — 이웃 ≈ 174 개의 핵 기울기 한 번의 GPU 시간, 그리고 표지가 고정일 때 몇 걸음마다 갱신해도 분할이 안 바뀌는지 (논문의 다시 정렬 기준을 기울기 갱신에 확장).
7. **탈압 두 팔** — 속도 판정 (이 논문) ↔ 견인력 판정 (Bardenhagen 2001) 을 U3 · U4 의 두 팔로 (`hu2018…` 카드 행동 7 과 같은 등록).  + 접합 (표지 지움) 규칙을 넣을지 여부.
8. **R7 판은 재료값의 출처가 먼저** — NCM 2차 입자의 강도 분포 · 파괴 에너지 (예: `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`) 를 정한 뒤 Weibull + 인장 손상 + 분할.  이 논문의 값은 쓰지 않는다.

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | 장이 셋 이상이면 쌍별 접촉력이 침투를 엄밀히 막지 못한다 | §1.1.1 *"while pairwise force calculations ensure conservation of linear momentum, they do not strictly prevent interpentrability for N > 2 fields.  We are currently developing other approaches to address this limitation, but this is beyond the scope of our current discussion."* |
| 2 | 분할은 노드마다 접촉 평면 하나를 가정 — 셋 이상의 영역이 만나는 점은 근사 | §2.2 *"This approach for material partitioning assumes that a local contact plane can be defined at each node to describe the contact interactions of two material regions … there can be three or more regions of material meeting at a single point."* |
| 3 | **접촉면은 셀 한 칸까지만 해상 → 비물리적 틈 → 알갱이 압밀의 밀도 불일치** | §4.2 *"Contact surfaces in the MPM are resolved to within a single grid cell spacing, which not only has a beneficial smoothing effect at stair-step particle boundaries, but can also result in a nonphysical gap at the contact surface between two approaching bodies.  This can be seen clearly in Figure 6, but is a general characteristic of contact in MPM, not an effect of the surface detection or DFG-partitioning method.  When simulating contact between large bodies, the volume of this boundary gap is generally negligible, but for compaction of granular materials (or porous materials with a high internal surface area), this could lead to a value of the continuum density that is inconsistent with the particle density.  This error decreases with mesh refinement but should be accounted for when interpreting mesoscale results."* |
| 4 | 방법의 타당성은 연속 손상 모델의 예측력에 묶인다 | §4.2 *"The validity of the method is limited by the ability of the continuum damage model to predict failure of the material."* |
| 5 | 쓴 구성 모델은 단순 — Mode I 지배 동적 파괴에만 엄밀히 맞음 | §2.7 *"strictly suitable only for Mode I dominated dynamic fracture"* · §3 *"highly simplified constitutive models … generally not adequate to fully describe the complex rate-dependent fracture response of engineering materials"* |
| 6 | 연성 파괴 · 전단띠에는 비국소 구성 모델이 필요 | §4.2 *"In simulating ductile failure or shear band formation, it is generally necessary to employ a non-local constitutive model 74 formulation to avoid mesh dependence of the results; however, this is a constitutive modeling issue, independent of the methods presented herein."* |
| 7 | 스칼라 손상만 — 이방 텐서 손상은 향후 | §2.3 *"In this work, we have considered only scalar damage models … This is a potential area for future development"* |
| 8 | 분리 문턱은 임의적 | §3.3 *"The arbitrariness of this separability threshold seems undesirable"* (단 SF 도 임의의 국소화 폭을 갖는다고 덧붙임) |
| 9 | 법선 정확도는 해상도 ÷ 곡률에 달림 · 법선의 질량 / 부피 가중은 안 함 | §2.2 *"improving with the resolution of the discretization relative to the curvature of the surface"* · §1.1.1 *"this was not carried out in our present work"* |
| 10 | 처음부터 닿아 있는 알갱이는 표면 탐지로 못 찾음 | §2.4 *"If the grains are initially in contact (but not bonded), it would be necessary to 'paint in' the surface flag at initialization."* |
| 11 | MPM 은 에너지를 근사적으로만 보존 | §3.3 *"The MPM conserves mass and linear momentum by construction, but only approximately conserves energy."* (Δx 1 mm 탄성 충돌에서 2.5 %) |
| 12 | 큰 문제에서 덧비용이 더 빨리 늘어남 (구현의 메모리 접근) | §3.5 *"For very large problems, (n_p>150,000), the added expense of the DFG partitioning appears to increase more rapidly"* |
| 13 | K–W 는 모든 계산이 실험보다 10° 낮고, 결과가 지지 조건 · 구성 모델값에 민감 | §3.2 *"all these results underpredict the fracture angle by 10°"* · *"highly sensitive to small variations in constitutive model parameters or support conditions"* |
| 14 | 파쇄의 물리를 다 담으려면 훨씬 정교한 구성 모델과 실험 검증이 필요 | §3.4 *"brittle materials will likely require a much more sophisticated constitutive model … and any such development would require significant experimental validation"* |
| 15 | 3D 예는 시연일 뿐 | §4 *"This result is included simply to demonstrate that the method is not limited to two dimensions and that it can implemented in a massively parallel solution framework."* |
| 16 | Weibull 분포가 실제 결함 분포를 대표하지 못할 수 있음 | §2.7 *"there is some evidence that a Weibull distribution may not be physically representative of flaw distributions in many engineering materials (cf., 65)"* |

## 12. 불확실 · 원문 (캡처) 에 없는 것

- **캡처에 없는 부분**: 참고문헌 목록 (접힘) → ref 2 · 32 · 33 · 42 등 번호의 서지 [미확인] (본문이 이름을 적은 것만: 28 Sulsky et al. · 34 · 35 · 69 Nairn et al. · 37 Sadeghirad et al. · 42 Bardenhagen et al. · 48 Song et al. · 61 Cervera et al. · 66 Kalthoff and Winkler · 67 *Belytchko et al.* (인쇄 철자 그대로)) · 각주 ‡ (mesoscale) · § (변형구배 갱신) · ¶ (손상 측도) 의 본문 · 저자 소속 · 접수 / 게재 확정일 · 키워드 · 'Citing Literature'.  보충 자료가 있는지도 캡처로는 알 수 없다.
- **Table 4 의 가려진 행**: 스크롤 상자 아래쪽에 행이 더 있을 수 있다 (마찰계수 · D̄^min · l^ch 가 안 보임).
- **수치 설정**: 시간 간격 · CFL · 끝 시각 · 빌릿 / 쐐기 문제의 격자와 입자 수 · 쐐기 문제의 재료 · 치수 · μ · K–W / Charpy / Brazilian 의 μ · 표면 탐지 문턱 · 띠 두께 · ε_m · r_g · Fig. 20 의 모든 값.
- **식으로 인쇄되지 않은 것**: ∇D̄ 의 계산식 · 접촉력이 입자 속도 갱신 (식 9) 에 들어가는 꼴 · 분할 P2G 의 운동량 / 힘 판 · 균열 각 · 속도를 재는 절차 · 평균 속도 (Fig. 18 속 그림) 의 정의와 분홍 띠의 뜻.
- **인쇄 어긋남 [카드 판독]**:
  - 법선 부호: 식 (11) (바깥) ↔ "Σ n · v ≤ 0" · KKT f^nor ≥ 0 · Algorithm 3 16 행 (안쪽 법선일 때 '다가옴') — §4-2.
  - Algorithm 3 22 행 "min(μ\|f^nor\|, \|f^tan\|) f^tan s^cm" ↔ 식 (16) "… sgn(f^tan) s".
  - 식 (21) 의 φ_ip ↔ 다른 곳의 S̄\*_ip · Algorithm 2 의 장 번호 0 / 1 ↔ 본문 ς = 1, 2.
  - τ = c_f/ℓ (통과 시간이면 ℓ/c_f).
  - Table 1 빌릿 탄성값 ↔ 본문 *compliant* · Fig. 8 의 큰 변형.
  - Table 2 w_t 10 mm (↔ 노치 50 mm · 100 × 100 셀) · G_f 22.3 mJ mm⁻² ↔ 본문 22.13 N/mm (354.1 mJ 가 22.13 을 지지) · Table 3 도 22.3.
  - Table 3 D̄^min "0.25 mm" · v_0 "20 ms⁻1" · ρ "8.0 gcm³" (지수 표기 깨짐).
  - n_p 셋째 값: 본문 129553 ↔ Fig. 16–18 표지 129,533.
  - *"minimum fragment size … approximately 50µs"* (시간 단위).
  - 그림 범례의 'DFP' ↔ 본문의 'DFG' (같은 방법으로 읽음).
  - 본문의 오탈자 (interpentrability · partioned · gradient-partioning · brittlness · discrepency · Belytchko 등) 는 인용에 그대로 두었다.
- **이 카드의 [판독] 값**: Fig. 13 · 14 · 18 · 19 의 수치는 화면 캡처 해상도의 그림에서 읽은 것 — 추세 전용.
- **이 방법이 소성 재료의 준정적 조밀 압밀 · 탈압에서 어떻게 행동하는지는 이 논문으로 알 수 없다.**

## 13. 인용 가능 문장 (덱 · 원고용)

- "MPM 은 한 속도장 안에서 재료 사이에 미끄럼 없는 (no-slip) 접촉을 자동으로 만들며, 손상 · 연화가 있으면 계면의 인공적 '용접' 과 비물리적 국소화를 낼 수 있다 (Homel & Herbold, Int. J. Numer. Meth. Engng 109, 1013–1044, 2017, §1 · §1.1.1)."
- "물체마다 속도장을 두는 MPM 마찰 접촉은 2D 에서는 4 색 정리로 네 장이면 되지만 3D 에는 그런 상한이 없고, 변형 · 흐름이 접촉점을 바꾼다; 장이 N 개면 접촉 쌍은 N(N − 1) 이며 N > 2 에서는 쌍별 힘이 침투를 엄밀히 막지 못한다 (같은 문헌 §1.1.1)."
- "같은 문헌은 입자의 손상 (또는 표면 표지) 을 핵으로 합친 스칼라장의 기울기 방향으로 노드마다 물질을 두 속도장으로 나누어, 접촉면을 미리 정하지 않고 마찰 접촉 · 분리 · 파괴 뒤 접촉을 다룬다 (§2)."
- "MPM 의 접촉면은 격자 한 칸 안에서만 해상되어 다가오는 두 물체 사이에 비물리적 틈이 남으며, 알갱이 압밀에서는 연속체 밀도가 입자 밀도와 어긋날 수 있다 — 격자를 조이면 준다 (같은 문헌 §4.2)."  — 우리 기공률 dx 수렴 시험의 근거 문장.
- ⛔ 쓰지 않을 문장: "표면 표지 분할의 마찰 접촉은 정량 검증됐다" (눈 대조 두 건) · "이 방법은 조밀 알갱이 압밀에서 검증됐다" (시험 없음 · 저자 스스로 경고) · "덧비용은 30–50 % 다" 를 3D · GPU 에 (2D · CPU 값) · 이 논문의 재료값을 어떤 실제 재료의 값으로.

## 14. 기법 미니 용어집

- **한 속도장 (single-field · SF)** — 격자 노드마다 속도가 하나인 보통의 MPM.  닿은 재료는 붙는다 (no-slip).
- **다중 속도장 접촉 (multi-field)** — 접촉 묶음마다 격자 속도장을 따로 두고, 둘 이상이 질량을 가진 노드에서 접촉력을 거는 방식 (Bardenhagen 계열).
- **DFG (damage-field gradient)** — 핵으로 매끈하게 만든 손상장 D̄ 의 기울기.  그림 범례의 **DFP** 는 같은 방법 (분할) 을 가리키는 표기.
- **핵 손상장 · 핵 합** — D(x) = Σ D_p ω, S(x) = Σ ω, D̄ = D/S.  S 가 작으면 자유 표면 근처.
- **비국소 노드 기울기** — 노드에서 직접 잰 기울기 대신, 그 노드에 얹히는 입자 중 기울기가 가장 큰 것을 대표로 쓰는 것 (손상 능선 위에서 0 이 되는 문제를 피함).
- **분리 조건 (separability)** — 노드에서 두 장을 실제 접촉 쌍으로 다룰지의 판정: 완전 손상 입자 ≥ 1 ∧ 장별 평균 손상의 작은 쪽 > D̄^min.
- **자기 접촉 (self-contact)** — 처음에 한 속도장 (한 재료 묶음) 이던 재료의 표면끼리의 마찰 접촉 (기공 벽 · 파괴면 · 한 묶음으로 둔 알갱이들).
- **표면 표지 s_p** — 표면 근처 입자에 1 을 실어 손상 자리 (max(s_p, D_p)) 에 넣는 값.  처음부터 닿아 있는 알갱이는 '칠해 넣는다'.
- **CPDI (convective particle domain interpolation)** — 입자 영역을 변형하는 평행육면체로 두고 형상함수를 그 영역에서 평균하는 MPM 변형.
- **domain scaling** — 실패한 입자의 CPDI 영역이 셀보다 길게 늘어나지 않게 줄이는 것 (가짜 '수치 파괴' · 늘어짐 방지).
- **update stress last (USL)** — 격자 속도를 갱신한 뒤 그 값으로 응력을 갱신하는 순서.
- **속도장 번짐 (velocity-field smearing)** — 한 셀 안의 실패 · 온전 입자가 한 속도장을 나눠 써서 생기는 가짜 응력 · 소산.
- **KKT 조건** — 접촉의 부등식 조건: 법선력 ≥ 0 · 겹침 ≤ 0 · 둘의 곱 = 0.
- **Rankine 손상** — 최대 인장 주응력이 강도를 넘으면 손상이 자라는 모델.  **특성 길이 l^ch** 로 파괴 에너지 G_f 에 묶는다.
- **시간-파괴 모델** — 균열이 입자 하나를 지나는 시간에 걸쳐 손상을 1 로 올려 균열 속도를 입력값으로 맞추는 경험 모델.
- **Weibull 크기 효과** — 부피가 작을수록 강도가 높게 뽑히는 분포 (σ_f ∝ V^(−1/m)).  격자를 조이면 입자 강도가 오른다.
- **4 색 정리** — 평면의 영역은 네 색으로 이웃끼리 다르게 칠할 수 있다 → 2D 에서는 장 4 개면 이웃 알갱이를 다 가를 수 있다.  3D 에는 그런 상한이 없다.
- **Kalthoff–Winkler · Charpy · Brazilian** — 노치 판 충격 전단 파괴 · 노치 시편 충격 파괴 에너지 · 원판 지름 방향 압축 (간접 인장) 시험.

## 15. 관련 카드

- **분할 뒤에 쓰는 접촉 알고리즘의 원전**: `bardenhagen2000_mpm_granular_multibody_frictional_contact` (물체별 장 ↔ 질량중심 장 · Coulomb · 자유 분리 · 지름당 셀 수 규칙) · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` (견인력 분리 판정 · N ≤ 2 가정 · γ 안정화 — 이 논문에는 없는 것들).
- **같은 문제의 다른 길**: `hu2018_mls_mpm_cpic_two_way_rigid_coupling` (강체 표면에 한해 격자 한 장으로 불연속 — 우리 MLS-MPM 이산화의 원전) · `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` (입자별 격자 + contact dynamics 로 소성 입자 압밀 — 이 논문에 없는 압밀 · 소성).
- **MPM 지도**: `devaucorbeil2020_mpm_after_25_years_review` (이 논문 = 파괴의 *mixed* 접근) · `stomakhin2013_mpm_snow_elastoplastic` · `klar2016_dp_sand_animation`.
- **파괴 쪽 (R7 · 계면)**: `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` (NCM811 2차 입자 파괴의 실측) · `bucci2018_mechanical_instability_interface_delamination` · `bucci2017_chemomech_failure_assb_cycling_czm` (점착대 파괴 — 이 논문이 한계를 적은 접근) · `song2025_porous_argyrodite_modulus_fracture_toughness` (SE 파괴 인성 실측).
- **단위 시험의 표적 (이 논문이 주지 않는 것)**: `kogutetsion2002_ep_sphere_rigid_flat` (탄소성 구–평면) · `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` (강체 + 무른 입자 혼합 압밀의 관측량).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

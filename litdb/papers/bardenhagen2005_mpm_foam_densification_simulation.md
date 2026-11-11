# 입자 기법 (GIMP) 으로 발포체 단위 셀을 '완전 치밀화' (공칭 변형률 90 %) 까지 누른 3D 계산 ★★ 그 지점에도 기공 ≈ 35 % 가 갇힌다 · 소성 · 마찰 · 탈압 없음 — 탄성 neo-Hookean 뼈대 · 붙는 (no-slip) 자기 접촉 · 판 속도 ÷ 파속 0.03 의 명시적 준정적 (절반 속도 대조) · 물질점에서 뽑은 기공 p = (V_bulk − V_microstructure)/V_bulk 과 비압축 기준선 · 격자 수렴 시험 없음 — Bardenhagen, Brydon, Guilkey (J. Mech. Phys. Solids 2005)

> slug `bardenhagen2005_mpm_foam_densification_simulation` · DOI `10.1016/j.jmps.2004.09.003` · type `MPM (명시적 GIMP — contiguous-particle GIMP · 한 물체 뼈대의 붙는 (no-slip) 자기 접촉 · 압축성 neo-Hookean 탄성 (소성 없음) · 3D 발포체 단위 셀 2 종 (lattice φ 7.9 % · random φ 9.6 %) 을 공칭 변형률 90 % 까지 일축 변형 압축 · 판 속도 ÷ 파속 0.03 (절반 속도 대조 1 건) · 물질점 기반 기공 추출 · 검증 = 꽉 찬 블록 해석해 1 건 + 공학 지침 · 남의 실험과 정성 대조)` · PDF `78ceea61-19._Insight_into_the_physics_of_foam_densification_via_numerical_simulation.pdf` (21 쪽 · 글자 층 온전 · 보충 자료 없음) · digested `2026-11-11` · status ✅
>
> ⚠ **먼저 읽을 것** — ① 재료는 **발포체의 뼈대** (탄성 · 압축성 neo-Hookean · K 10.2 · G 7.2 GPa · ρ 1900 kg/m³ — 값의 출처 미인쇄 · 그림 제목은 *Bulk Polymer*) 이고 계산 대상은 **가는 뼈대 한 물체**다 — **LPSCl · NCM 이 아니고 분말 · 입자 층도 아니다.  절대값 전이 0 건** (남는 기공 35–38 % · 고원 응력 · 치밀화 반력 전부).  가져오는 것은 **방법** (기공 연산자와 그 기준선 · 명시적 풀이의 준정적 설정과 점검 꼴 · 꽉 찬 블록 해석해 시험) 과 **저자가 적은 한계**뿐이다.
> ② **소성이 없다** (탄성만) · **마찰 · 미끄럼이 없다** (*no-slip contact*) · **하중을 빼지 않는다** ('unload' 0 회) · **DEM 을 쓰지도 언급하지도 않는다** ('DEM' · 'discrete element' 0 회 [카드 전문 검색]).  저자 스스로 *"viscoelasticity for polymeric foams, plasticity for metallic foams, and frictional sliding contact, will be studied later"* 라고 적는다 (p.601).
> ③ **접촉 알고리즘의 이름이 없다** — *no-slip contact* · *contact between arbitrary network components* 라고만 적는다.  한 물체의 자기 접촉이므로 격자 한 벌의 속도장이 주는 붙는 접촉으로 읽힌다 [카드 판독].  같은 제1 저자의 다물체 마찰 접촉 (짝 카드 2000 · 2001) 은 서론에서 인용만 한다.
> ④ **정량 검증은 꽉 찬 블록의 일축 변형 해석해 1 건** (끝 오차 ≈ 5 %) 뿐이다.  **격자 수렴 시험이 없고**, 단위 셀 크기 · 셀당 물질점 수 · 물질점 수 · 시간 간격 · 인공 점성 계수 · 계산 시간이 인쇄돼 있지 않다 (§3-10).  준정적 판정은 절반 속도 런 1 건과의 **눈 대조**다.
> ⑤ **'완전 치밀화' 는 비압축을 가정한 운동학적 이름**이다 (공칭 변형률 ≈ 1 − φ ≈ 0.9) — 그 지점의 반력은 3.9–6.7 GPa (뼈대 K 의 0.38–0.65 배) 이고 뼈대 자체가 부피로 16–37 % 눌려 있다 [판독 · 카드 산술].  초록의 *"A surprising amount of porosity is found in fully-densified foams"* = 본문 *"about 35% porosity is retained near full densification"* (p.611) = Fig. 8 에서 lattice 0.345 · random 0.384 [판독].
> ⑥ 그림에서 읽은 값은 화소가 아니라 **PDF 그리기 명령의 경로 좌표**에서 읽었다 (Fig. 1 · 3–6 · 8–11 이 벡터 그림 · 축은 틀과 눈금 위치로 사상) — 그래도 원자료가 아니라 그림이므로 표지는 `[판독]` 이다.  **판독 원자료** = `litdb/figures/bardenhagen2005_mpm_foam_densification_simulation/digitized.csv` (2,173 행 — 곡선 27 개를 변형률 0.01 간격으로 보간한 값 + 요약 값 49 행 · 열 = figure, series, x_name, x, y_name, y, note).  Fig. 2 · 7 (내장 래스터) 의 판독은 화소에서 했다.
> ⑦ 표지: `인쇄` = 본문 · 캡션 · 범례에 적힌 값 · `[판독]` = 그림에서 읽은 값 · `[카드 산술]` = 인쇄값 · 판독값에서 산술로만 (식 병기) · `[미확인]` = 논문에 없음 · `[카드 판독]` = 모호한 곳에 대한 카드의 읽기 · `[카드 추론]` · `[우리 코드 판독]` · `[우리 기록]` = 논문 밖 판단.
>
> 짝 카드: `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 같은 제1 저자의 MPM 다물체 마찰 접촉 (이 논문이 인용만 하고 **쓰지 않은** 것).  `gritton2017_mpm_chemomechanical_coupling_silicon_anode` — 이 논문을 "큰 변형에 성공한 MPM" 의 근거 (그 논문 ref. [31]) 로 든 카드.  `devaucorbeil2020_mpm_after_25_years_review` — 이 논문을 응용 사례로 소개한 리뷰 카드 (그 카드의 *image-based* 표기는 이 논문 본문과 맞지 않는다 — §12).  `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — 한 물체의 자기 접촉을 속도장 분할로 다루는 쪽.  `nezamabadi2022_mpm_cd_plastic_particle_compaction` — 소성 입자 압밀까지 간 MPM (2D).

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

[DEM 우선 (수영)] 은 *"가압부터 탈압까지 한 모델 (MPM) 이 다 계산할 수 있는가"* 를 묻는다.  이 논문은 분말 논문이 아니다 — 그런데 **MPM 계열 기법으로 기공 90 % 인 구조를 '기공이 없어질 변형률' 까지 누르고 그 과정의 기공을 계산에서 뽑아낸** 가장 이른 선례이고 (정본 안에서), 읽을 까닭이 넷 있다.

**(1) 큰 변형 + 자기 접촉 + 복잡한 형상이 유한요소법에 왜 어려운지를 세 가지로 적었다** — 후보 B (입자별 유한요소) 를 견줄 때 인용할 원문이다 (p.599).

> *"Large strains result in numerical inaccuracies as Lagrangian meshes become too distorted or Eulerian meshes require extensive material advection."*

> *"Contact algorithms themselves are an area of ongoing research Zhong and Mackerie (1994).  Simulation results are often found to be strongly dependent on the specific values of the algorithm's parameters, which are generally only loosely tied to material properties.  Common algorithms, such as master and slave, require the identification a priori of candidate contact surfaces, which is only possible early in the deformation for foam microstructures, if at all."*

> *"The combination of discretizing complex microstructures and simulating large deformations and contact is extremely challenging numerically for the finite element method (FEM), easily the most widely used numerical solution procedure in solid mechanics.  Consequently, foam micromechanics simulations with FEM have been forced to focus on modest deformation foam behavior …"*

**(2) 기공을 계산에서 뽑는 연산자와 그 기준선이 식으로 있다** — 식 (1) p = (V_bulk − V_microstructure)/V_bulk · 식 (2) p_inc = 1 − φ/(1 − ε_eng) (p.610).  우리 MPM 의 기공 식 `1 − solid_vol/(area·height)` 은 고체 부피를 씨앗 때 값으로 고정한 **식 (2) 꼴**이다 [우리 코드 판독 · `scripts/mpm3d_compaction.py` 2794 · 3261 행 · 파일 마지막 커밋 `cb5a6a445`].  두 식의 차는 정확히 고체의 부피 변화다 (§3-6) — 단계 0 (기공 연산자) 의 재료.

**(3) 명시적 풀이로 준정적을 흉내 낼 때의 설정과 점검이 숫자로 있다** — 판 속도 = 종파속의 3 % · 90 % 압축에 파 통과 시간의 30 배 · 인공 점성 · 절반 속도 런과의 대조 (p.603 · p.606).  우리 MPM 의 `--platen-mach` 0.01–0.03 과 **같은 자릿수**다 [우리 코드 판독 · 3076–3077 행].  그리고 그 대조를 카드가 다시 읽으면 구조가 무너지는 구간의 평균 반력이 두 속도에서 35 % 다르다 (§3-4) — 저자 판정 (*"The responses for both rates are similar"*) 은 눈 대조다.

**(4) '완전 치밀화' 뒤에도 기공이 남는다는 결과와 그 한정이 있다.**

> *"For the numerical simulations, which are initially approximately 90% porous, about 35% porosity is retained near full densification.  Clearly details of contact geometry and material properties will strongly influence residual porosity."* (p.611)

탄성 뼈대 + 붙는 접촉에서는 기공을 메울 기전 (소성 유동 · 미끄럼 재배열) 이 없다 — 남은 기공은 '갇힌 틈 + 탄성으로 눌린 뼈대' 다 (§9 ②).  우리 SE (소성) 의 남는 기공 값으로 옮길 수 없지만, **"얼마까지 눌리는가" 를 접촉 규칙과 재료가 정한다**는 것의 한쪽 끝이다.

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| 기공 연산자와 판정 기준을 결과 전에 적는 일 (단계 0) | 식 (1) · (2) 한 쌍 + Fig. 8.  단 V_microstructure 의 **계산식은 없다** · 인쇄된 곡선은 lattice 에서 뼈대 부피가 11 % 느는 것으로 읽혀 물리 범위를 넘는다 (§3-6 · §9 ③) |
| 명시적 MPM 의 준정적 설정에 대한 제3자 근거 (단계 2 · 4) | 판 속도 ÷ 종파속 0.03 · 파 통과 30 번 · 인공 점성 · 절반 속도 1 건.  판정은 눈 · 반력의 속도 민감도는 구간마다 2–35 % [판독 · 카드 산술] |
| 접촉 없는 단위 시험 (단계 2) | 꽉 찬 블록 일축 변형 ↔ 해석해 (Fig. 1) — 끝 (ε 0.9) 오차 ≈ 5 % · 구간 평균 +5.5–6.6 % [판독] |
| 해상도 규칙 (지름당 셀 수 · U1 · U6) | **없음** — 셀 0.01 mm 한 가지 · 격자 수렴 시험 없음 · strut 당 셀 수 미인쇄 (그림으로는 지름 ≈ 셀 변의 0.10–0.14 [판독]) |
| 한 속도장 (붙는 접촉) 으로 조밀 끝까지 가도 수치가 버티는가 (후보 A) | 버틴다 — 공칭 90 % 까지 (격자 얽힘 없음).  단 붙는 접촉이 기공을 가두는 쪽으로 치우칠 수 있고 (§9 ⑩) 미끄럼 · 분리는 "나중" |
| 소성 SE 의 준정적 압밀 · 다입자 접촉 · 탈압 곡선 · 실험 정량 대조 | **없음** |

### 0-2. 이 묶음의 네 질문 (DEM 한계 · 소성 · 2D/3D · 탈압)

| 질문 | 이 논문의 답 (원문 위치) |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | **말 없음.**  DEM 을 쓰지도 언급하지도 않는다 ('DEM' · 'discrete element' 0 회 · 참고문헌 34 건 가운데 'granular' 는 제목 셋뿐 [카드 전문 검색]).  한계를 적은 대상은 **유한요소법**이고 (위 (1) 의 세 인용 · p.599), 다른 입자 기법은 한 구절뿐이다: *"The method uses a grid to interact particles, as opposed to pairwise interactions as used in Smooth Particle Hydrodynamics."* (p.601) |
| (ii) 입자의 소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용 | **소성은 넣지 않았다** (탄성만 · *"plasticity for metallic foams … will be studied later"* p.601).  어려움으로 든 것은 큰 변형 · 회전 (격자 뒤틀림 / 이류) · 미리 지정할 수 없는 자기 접촉 · 형상 이산화 — 전부 FEM 쪽 문장이다 (p.599).  우회 = **입자 기법** (GIMP: 물질점이 상태를 싣고 격자는 매 걸음 새로 · *"eliminating mesh tangling problems"* p.601).  두 번째 어려움 = **준정적**: *"To simulate quasi-static deformations an implicit numerical solution strategy is generally preferred.  Currently these algorithms are expensive …  While less elegant, it is also possible to obtain quasi-static results with an explicit code provided the loading is applied slowly enough."* (p.602) → 판 속도 ÷ 종파속 0.03.  **맞춘 값 = 0 개** (재료 상수를 정해 놓고 계산 · 실험에 맞춘 것 없음).  **검증** = 꽉 찬 블록 해석해 1 건 (≈ 5 %) + Gibson–Ashby 지침 (계산이 그 선의 1.5–3.9 배 [판독]) + 남의 실험과 정성.  **비용** = *"(serial) calculations"* (p.615) 라는 낱말뿐 — 물질점 수 · 걸음 수 · 시간 [미확인] |
| (iii) 2D 인가 3D 인가 · 2D → 3D 전이 | **3D** — 본문에 '3D simulation' 이라는 낱말은 없고 *1 mm³ block* · *cubic grid* · *spherical nodes* · 원근 그림 (Fig. 2 · 7) · *viewed from below* 로 알 수 있다 [카드 판독].  2D ↔ 3D 를 견준 문장은 없다 ('two-dimensional' 은 참고문헌 제목 *Effect of imperfections on the yielding of two-dimensional foams* 한 번).  대신 **크기** 에 대한 경고가 있다: *"Although it is tempting to suggest the results in Fig. 6 are representative of bulk foams with similar microstructures, it is unlikely to be the case.  Much bigger unit cells need to be considered …  Accurate determination of bulk foam response requires finding the necessary size of a representative volume element (RVE) of material."* (p.610) |
| (iv) 압력을 뺄 때의 거동 | **다루지 않는다** — 'unload' · 'recover' · 'rebound' 0 회 [카드 전문 검색].  하중은 일정 속도 피스톤의 한 방향 압축뿐이고 계산은 ε 0.9 에서 끝난다.  재료가 탄성이라 원리상 되돌아오겠지만 붙는 접촉으로 닿은 면이 떨어지는지 (분리 판정) 에 대한 말은 없다 [미확인] |

---

## 1. 한 줄 요약

**KR:** 발포체의 미세구조 (뼈대) 를 유한요소법으로 치밀화 구간까지 누르기 어려운 까닭 — 형상 이산화 · 큰 변형과 회전 · 미리 지정할 수 없는 자기 접촉 — 이 입자 기법의 강점과 맞물린다는 주장을, 일반화 보간 물질점법 (GIMP · MPM 을 특수한 경우로 포함 · contiguous-particle 변종 · 명시적 적분 · 격자는 매 걸음 처음 배치로) 으로 보인다.  뼈대 재료는 압축성 neo-Hookean 탄성 (K 10.2 · G 7.2 GPa · ρ 1900 kg/m³) · 접촉은 붙는 (no-slip) 접촉 · 준정적은 "충분히 천천히" (판 속도 = 종파속의 3 % · 90 % 압축에 파 통과 시간의 30 배 · 인공 점성) 로 맞춘다.  꽉 찬 블록 (1 mm³ · 셀 0.01 mm) 의 일축 변형 압축이 해석해와 90 % 변형률에서 약 5 % 안에 드는 것을 확인한 뒤, 상대밀도 약 10 % 인 열린 셀 단위 셀 둘 — 규칙 격자를 조금 흔든 lattice (φ 7.9 %) 와 손으로 만든 random (φ 9.6 %) · 위 = 일정 속도 피스톤 · 아래 = 대칭면 · 옆 = 주기 — 을 공칭 변형률 90 % (비압축이면 기공이 다 없어질 변형률) 까지 누른다.  반력–변형 곡선은 탄성 · 고원 · 치밀화 세 구간을 내고 (lattice 는 좌굴 비슷한 snap-through 로 평평한 고원 · random 은 단조 증가), Gibson–Ashby 의 고원 진입 응력과 같은 자릿수이며, 절반 속도 런과 "비슷" 하다.  물질점에서 뽑은 기공은 끝까지 0 이 되지 않고 약 35 % 가 남는다 — 뼈대가 서로 걸려 틈이 갇히기 때문이며, 저자는 치밀화 구간의 발포체를 기공 없는 연속체로 근사하면 (특히 응력파 문제에서) 틀린다고 결론짓는다.  재료 상수를 두 배로 하면 반력도 대체로 두 배가 된다.  소성 · 점탄성 · 마찰 · 실제 형상 (X 선 단층 영상) · 100–1000 기공 규모는 향후 과제다.

**EN:** Bardenhagen, Brydon and Guilkey use the generalized interpolation material point (GIMP) method — explicit, with the grid reset every step — to compress idealized open-cell foam unit cells (relative density ≈ 10 %) to 90 % engineering strain, i.e. to nominal full densification, which FEM studies had not reached because of meshing, mesh distortion and self-contact.  The strut material is compressible neo-Hookean elastic (K 10.2 GPa, G 7.2 GPa, 1900 kg/m³), contact is no-slip, and quasi-static conditions are approximated by a piston moving at 3 % of the longitudinal wave speed (90 % compression in 30 wave transit times, artificial viscosity).  A solid block compressed in uniaxial strain follows the analytical curve to within about 5 % at 90 % strain.  A slightly perturbed lattice cell (7.9 %) and a hand-built random cell (9.6 %), with a constant-velocity piston, a symmetry plane and periodic sides, show the elastic, plateau and densification regimes; the lattice snaps through to a flat plateau, the random cell hardens monotonically, and both are of the order of the Gibson–Ashby plateau-onset stress.  A run at half the piston speed is judged similar.  Porosity extracted from the material points stays near 35 % at full densification because the collapsed network pins and locks pore space in; doubling the material constants roughly doubles the response.  No plasticity, friction, unloading or grid-convergence study; realistic geometries and 100–1000-pore cells are left for future work.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **Insight into the physics of foam densification via numerical simulation** |
| 저자 | **S.G. Bardenhagen** (a · 교신 ∗) · **A.D. Brydon** (a) · **J.E. Guilkey** (b) |
| 소속 | (a) Theoretical Division, Los Alamos National Laboratory, Group T-14 MS B214, Los Alamos, NM 87545, USA · (b) Department of Mechanical Engineering, University of Utah Salt Lake City, UT 84112, USA |
| 교신 | *Corresponding author. Tel.: +1 505 665 5323; fax: +1 505 606 0455* · E-mail bard@lanl.gov (S.G. Bardenhagen) |
| 저널 | **Journal of the Mechanics and Physics of Solids 53 (2005) 597–617** — 첫 쪽 서지 줄은 *"Journal of the Mechanics and Physics of solids"* (끝 낱말 소문자 인쇄) · 머리글 *S.G. Bardenhagen et al. / J. Mech. Phys. Solids 53 (2005) 597–617* · **호 (issue) 미인쇄** · *0022-5096/$ - see front matter Published by Elsevier Ltd.* |
| DOI | **10.1016/j.jmps.2004.09.003** (첫 쪽 인쇄 · PDF 메타데이터의 제목 칸도 같은 DOI) — 1저자 메모와 같음 |
| 접수 · 게재 | Received 29 March 2004; received in revised form 3 September 2004; accepted 18 September 2004 · 온라인 게재일 미인쇄 (PDF 만든 날 2005-01-07 [PDF 메타데이터]) |
| 키워드 (인쇄) | Cellular solids; Foam mechanics; Material point method; Constitutive behavior; Microstructures |
| 분량 | 21 쪽 (p.597–617 · **PDF 쪽 = 논문 쪽 − 596**) · Fig. 1–11 · 번호 식 (1)–(2) · **표 없음** · 참고문헌 34 건 · 보충 자료 없음 |
| 절 구성 | 1 Introduction (p.598–600) · 2 Numerical technique (p.600–601) · 3 Numerical simulations (p.601–602) · 3.1 Constituent material response (p.602–603) · 3.2 Foam unit cell calculations (p.604–613) · 4 Conclusions and future work (p.613–615) · Acknowledgements (p.615) · References (p.615–617) |
| 연구 유형 | 수치 시연 (입자 기법으로 발포체 미세구조의 전 구간 압축) + 정성 검증.  실험 없음 (남의 실험 · 공학 지침과 대조) |
| 구현 기반 | *"The particle code used for these (serial) calculations is from the University of Utah's Accelerated Strategic Initiative project, and has been ported to both Department of Energy supercomputers and Linux clusters."* (p.615) — **코드 이름 미인쇄** (`gritton2017…` 카드의 Uintah 와 같은 대학이나 같은 코드인지는 이 논문으로는 [미확인]) |
| 자금 | US Department of Energy at Los Alamos National Laboratory · Center for the Simulation of Accidental Fires and Explosions, Grant **W-7405-ENG-48** (짝 카드 2001 판과 같은 과제 번호) |
| 감사 | M. Schraad · E. Kober (T-Division, LANL) · A. Kraynik · W. Scherzinger (Engineering Sciences, SNL) |
| PDF 상태 | 조판 PDF (creator *Elsevier* · Acrobat Distiller 4.05) · 글자 층 온전하나 수식 기호가 다른 글자로 나온다 (φ → 'f' · = → '¼' · ε · − · ≈ → 제어 문자) → 식 · 기호는 렌더로 확인 · 그림 9 장 (Fig. 1 · 3–6 · 8–11) 은 **벡터** (선 그림 · gnuplot 출력의 꼴) · Fig. 2 (660 × 276 px 회색조) · Fig. 7 (660 × 1007 px JPEG) 은 200 dpi 내장 래스터 · 글자 층 맨 위의 *ARTICLE IN PRESS* 는 흰 글자라 보이지 않는다 (크롭에 없음) |

**자기 위치 (저자 원문)**
> *"… to date, simulations over the full range of bulk deformations in which these materials operate have not been reported.  Here a particle technique is demonstrated to be well-suited for this computational challenge, permitting simulation of the compression of foam microstructures to full densification."* (초록 · p.597)

> *"Calculations are presented here in which, for the first time, simplified foam microstructures are compressed well into the densification regime."* (§1 · p.599)

> *"The primary goal of this manuscript is to establish a convincing capability perform these simulations.  …  A primary focus is on validation."* (§3 · p.601)

---

## 3. 핵심 수치

> **표지** · `인쇄` = 본문 · 캡션 · 범례 · `[판독]` = 그림 (벡터 경로 좌표 · 래스터는 화소) · `[카드 산술]` = 산술로만 · `[미확인]` = 논문에 없음.  판독값은 추세 · 자릿수 확인용이다 — 논문이 인쇄한 값처럼 쓰지 않는다.

### 3-1. 재료 · 모형 값

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 뼈대 재료의 구성식 | **압축성 neo-Hookean (비선형) 탄성** — *"A compressible Neo-Hookean (nonlinear) elastic formulation … Simo and Hughes (1998).  This is a large deformation constitutive model appropriate for natural rubbers and for polymers in which viscous response is not expected to be large."* | 인쇄 · §3.1 p.602 |
| 체적 계수 K · 전단 계수 G · 밀도 ρ | **10.2 GPa · 7.2 GPa · 1900 kg/m³** | 인쇄 · p.602 (값의 출처 · 근거 [미확인]) |
| ⇒ E · ν · 종파 탄성률 M = K + 4G/3 | **17.49 GPa · 0.214 · 19.8 GPa** | [카드 산술] E = 9KG/(3K + G) · ν = (3K − 2G)/(2(3K + G)) |
| ⇒ 종파속 c_L · 전단파속 c_S · 봉 파속 √(E/ρ) | **3,228 · 1,947 · 3,034 m/s** | [카드 산술] |
| 저장 에너지 함수 (식) | **미인쇄.**  Fig. 1 의 해석 곡선은 σ = (K/2)(1/J − J) + (2G/3)(J^(−5/3) − J^(1/3)), J = 1 − ε (= 체적항 (K/2)[(J² − 1)/2 − ln J] + 편차항 (G/2)(tr b̄ − 3) 의 일축 변형 응력) 과 ε 0.4–0.9 에서 0.1 % 안 · ε 0.1–0.3 에서 1.4 % 안에서 겹친다 → 이 꼴로 읽힌다 (체적항이 K ln J/J 나 K(J − 1) 꼴이면 ε 0.9 에서 455 · 230 GPa 로 그림의 271 GPa 와 안 맞는다) | [판독 + 카드 산술 — 역확인 · 논문 밖 식] |
| 소성 · 점탄성 · 손상 | **없음** (탄성 · 속도 무관) | 인쇄 · p.601 · p.603 (*"the material response is not rate dependent"*) |
| 'stiffened' 재료 | *"the material constants are doubled"* → K 20.4 · G 14.4 GPa (밀도 언급 없음) | 인쇄 p.611 · 값은 [카드 산술] |
| 접촉 | **no-slip** (마찰 계수 · 분리 판정 · 알고리즘 이름 없음) | 인쇄 p.601 |
| 발포체의 상대밀도 φ = ρ_foam/ρ_solid | lattice **7.9 %** · random **9.6 %** (Fig. 8 의 출발 기공으로 읽으면 7.82 · 9.71 %) | 인쇄 p.604–605 · 괄호는 [판독] |
| 값의 성격 | 그림 제목은 *Bulk Polymer* 인데 E 17.5 GPa · ρ 1900 kg/m³ 는 짝 카드 2001 판의 '가상 Plexiglas' (G 72 · K 102 GPa · ρ 1900 kg/m³) 의 **계수 1/10 · 같은 밀도**다 | [카드 판독 — 정본 카드 대조] |

### 3-2. 기하 · 이산화 · 시간 · 경계

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 차원 | **3D** | [카드 판독] (§0-2 (iii)) |
| 기법 | **GIMP** (generalized interpolation material point · MPM 을 특수한 경우로 포함) · *"the contiguous particle GIMP method used here"* · **명시적** 적분 · 격자는 매 걸음 처음 배치로 되돌림 | 인쇄 p.600–603 |
| 꽉 찬 블록 (§3.1) | **1 mm³** · 셀 **0.01 mm** → 한 변 100 셀 · 10⁶ 셀 | 인쇄 p.603 · 셀 수는 [카드 산술] |
| 발포체 단위 셀 (§3.2) | *"using the same compression rate and discretization specified in Section 3.1"* → 셀 0.01 mm · **단위 셀의 변 길이는 미인쇄** | 인쇄 p.605 · [미확인] |
| lattice 셀 | 규칙 격자의 꼭짓점에 둔 **구 노드**를 *"randomly shifted a distance of 3–8% of the unit cell size"* · 노드 사이를 strut 이 잇는다 · φ 7.9 % | 인쇄 p.604–605 |
| random 셀 | *"a pseudo-random structure generated by hand.  It was constrained to be periodic, and to have a similar relative density as the lattice"* · φ 9.6 % | 인쇄 p.605 |
| strut 지름 ÷ 셀 변 | ≈ **0.10–0.14** (원근 그림 · 보는 각을 몰라 범위로) — 셀 변이 블록과 같은 1 mm 라면 지름당 10–14 셀이지만 그 가정은 논문에 없다 | [판독 · Fig. 2] · 뒤 절은 [카드 산술 · 가정] |
| 셀당 물질점 수 · 물질점 수 | **[미확인]** | — |
| 경계 조건 | 위 = **일정 속도 피스톤** (*"The compressing piston is black and provides a constant velocity boundary condition"*) · 아래 = **대칭면** · 옆 (면내) = **주기** → *"the compression of an infinite, periodic, two unit cell thick layer of foam"* | 인쇄 p.604 |
| 피스톤의 정체 | Fig. 7 에서 물질점으로 그려진 판 (파랑 = 낮은 응력) · 밑에서 본 칸의 틈으로 보인다 → 물질점으로 된 물체로 읽힌다 | [판독] |
| 판 속도 | **종파속의 3 %** (*"3% the initial longitudinal wave speed"*) = 96.8 m/s · 대조 런은 그 절반 (0.015 = 48.4 m/s) | 인쇄 p.603 · p.606 · Fig. 4 범례 · m/s 는 [카드 산술] |
| 총 시간 | 90 % 압축 = **파 통과 시간의 30 배** (= 0.9/0.03 ✓) · 1 mm 블록이면 9.29 µs · 공칭 변형률 속도 ≈ 9.7 × 10⁴ s⁻¹ | 인쇄 p.603 · 뒤는 [카드 산술] |
| 인공 점성 | 있음 — *"artificial viscosity is added to the calculation to damp out numerical ringing at wave fronts"* · 꼴 · 계수 [미확인] | 인쇄 p.603 |
| 시간 간격 · 안전계수 · 걸음 수 | **[미확인]** — 셀 0.01 mm ÷ c_L = 3.1 ns 이므로 한 변 100 셀 · CFL 1 이면 90 % 까지 ≥ 3,000 걸음 (눌릴수록 파속이 커져 더 든다) | [카드 산술 · 가정] |
| 반력 · 변형률의 정의 | 반력 (traction) = 하중 ÷ 재는 넓이 (압축 +) · 공칭 변형률 = 길이 변화 ÷ 처음 길이 (압축 +) | 인쇄 p.603 |
| 반력을 재는 곳 | 발포체: *"The traction measurement is made on the bottom computational boundary"* (대칭면) · 블록: 명시 없음 — 수치 곡선이 ε ≈ 0.029 에서 뜨는 것 (파가 반대쪽에 닿는 때 = 0.03) 으로 보아 피스톤 반대쪽 | 인쇄 p.605 · 블록은 [판독 · 카드 산술] |

### 3-3. 검증 — 꽉 찬 블록의 일축 변형 압축 (§3.1 · Fig. 1)

| 항목 | 값 | 표지 |
|---|---|---|
| 문제 | *"uniaxial strain, constant strain-rate deformation of a solid cube"* — 옆으로 못 늘어나는 블록을 피스톤으로 90 % 까지 · 해석해 = neo-Hookean 의 정적 일축 변형 응력 | 인쇄 p.602 |
| 저자 판정 | *"quite good agreement"* · *"At the highest strain the numerical solution error is approximately 5%, and this is for the case when **all the material points are compressed into one-tenth the initial volume**"* (굵게 한 곳은 원문에서 기울임 강조) | 인쇄 p.603 |
| 끝 값 (ε 0.900) | 수치 **286,061** ↔ 해석 **271,063 MPa** → +5.5 % (곡선의 마지막 봉우리) · ε 0.90 으로 보간하면 281,834 ↔ 271,013 (+4.0 %) | [판독 · 벡터 경로] |
| 구간별 평균 치우침 (수치 ÷ 해석 − 1) | ε 0.1–0.3 **+6.6 %** (국소 −19 ~ +34 %) · 0.3–0.5 **+6.0 %** (−9 ~ +20 %) · 0.5–0.7 **+5.7 %** (−2 ~ +13 %) · 0.7–0.8 **+5.8 %** (+1 ~ +13 %) · 0.8–0.9 **+5.5 %** (+2 ~ +10 %) — **어느 구간에서나 수치가 평균 5.5–6.6 % 높다** | [판독 + 카드 산술] |
| 수치 곡선이 뜨는 변형률 | ε ≈ **0.029** (그 전은 0) · ε 0.035 · 0.04 에서 983 · 1,405 MPa ↔ 해석 680 · 830 MPa (첫 파의 울림 — 크기 ρ c_L v = 0.03 M ≈ 594 MPa 의 자릿수) | [판독 + 카드 산술] |
| 큰 변형률의 뾰족한 튐 | *"small errors associated with particles crossing computational cell boundaries, resulting in the spikes in the numerical result evident at large strains"* · 자세한 것은 Bardenhagen and Kober (2004) 로 넘김 | 인쇄 p.603 |
| 조밀 끝의 민감도 | 해석 곡선에서 d ln σ/dε = 4.1 (ε 0.5) · 5.5 (0.7) · 7.9 (0.8) · **15.6 (0.9)** → ε 0.9 에서 응력 5 % = 변형률 0.0032 = **판 위치 0.32 셀** (셀 0.01 mm · 블록 1 mm) · 반 셀이면 7.8 % | [카드 산술 — 위 식] |
| 본 그림 밖의 대조 | *"if a uniform body-fit (cubic) grid were used, the final deformation would result in cell aspect ratios of 10"* | 인쇄 p.603 |

### 3-4. 준정적 판정 — 판 속도 절반 런 (§3.2 · Fig. 4 · random 셀)

| 항목 | 값 | 표지 |
|---|---|---|
| 설계 | 같은 random 셀을 판 속도 ÷ 파속 **0.030** (파선 · 본 계산 속도) 과 **0.015** (실선) 로 · 처음 70 % 를 비교 + 5차 다항 맞춤 (일점쇄선) | 인쇄 p.605–606 · 범례 |
| 저자 판정 | *"The responses for both rates are similar.  …  It is concluded that the faster piston speed gives representative quasi-static results, and this speed is used for all remaining simulations."* | 인쇄 p.606 |
| 구간 평균 반력 (빠름 ↔ 느림) | ε 0.05–0.3: 21.0 ↔ 20.6 MPa (**×1.02**) · 0.3–0.55: 61.6 ↔ 45.8 MPa (**×1.35**) · 0.55–0.7: 181 ↔ 166 MPa (**×1.09**) · 0.05–0.7 전체 ×1.15 | [판독 + 카드 산술] (빠른 런은 Fig. 10 의 'original' 곡선 — 같은 곡선 · 최대 차 0.5 MPa — 에서 ε 0.7 까지 읽음) |
| 같은 변형률에서의 값 | ε 0.32: 62 ↔ 37 · 0.38: 71 ↔ 32 · 0.43: 76 ↔ 50 · 0.52: 101 ↔ 55 · 0.55: 56 ↔ 87 · 0.65: 186 ↔ 201 · **0.70: 361 ↔ 289 MPa** · 차의 rms 21 MPa · 최대 79 MPa | [판독] |
| ∫ 반력 dε (ε 0–0.7) | 47.9 ↔ 41.7 MJ/m³ (+15 %) | [판독 + 카드 산술] |
| 반력이 뜨는 변형률 | 0.0322 (빠름) · 0.0168 (느림) = 파가 바닥에 닿는 때 — 봉 파속으로 곧은 strut 을 지나면 0.03·c_L/√(E/ρ) = 0.0319 · 0.0160 | [판독 + 카드 산술] |
| 맞춤선에서 벗어난 정도 (ε 0.05–0.55) | 느림 rms 7.3 MPa · 빠름 15.9 MPa — 본문 *"generally smaller for the lower strain rate simulation"* 과 같은 방향 | [판독 + 카드 산술] |
| 맞춤선이 어느 런의 것인가 | 본문에 없다.  인쇄된 선은 **느린 런**의 5차 최소제곱 맞춤 (원점 통과) 과 rms ≈ 2 MPa · 빠른 런의 맞춤과는 ≈ 13 MPa — ε 0.7 의 값 289 MPa 도 느린 런 원자료 (288.6) 와 같고 빠른 런 (361) 과 다르다 → 느린 런 쪽에 맞춘 선으로 읽힌다.  (lattice 는 원자료의 원점 통과 5차 맞춤이 인쇄된 선과 rms 0.14 MPa 로 겹친다) | [카드 산술 — 재현] |
| 구조의 겉보기 파속으로 본 판 속도 | 맞춤선의 처음 할선 계수 (ε 0.02–0.05): random ≈ 120 MPa · lattice 370–500 MPa → √(E/(φρ)) ≈ 810 · 1,570–1,820 m/s → 판 속도 ÷ 그 파속 ≈ **0.12 · 0.05–0.06** (고체 종파속 기준 0.03 의 2–4 배) | [판독 + 카드 산술] |
| 잡음에 대한 저자 설명 | *"The magnitude of these fluctuations is an artifact of the small unit cell size.  Simulations of larger microstructures will have a higher frequency of strut contact events of similar magnitudes, but divided by a larger measurement area."* | 인쇄 p.606 |

### 3-5. 반력–변형 곡선 — 세 구간 (Fig. 3 · 5 · 6)

| 구간 | lattice (φ 7.9 %) | random (φ 9.6 %) | 표지 |
|---|---|---|---|
| 처음 (탄성) | 맞춤선 할선 계수 370–500 MPa (ε 0.02–0.05) · 원자료는 ε 0.033 에서 뜬다 | ≈ 120 MPa · 원자료는 ε 0.032 에서 | [판독 — 맞춤선의 꼴에 달린 값] |
| 봉우리 → 고원 | 원자료 봉우리 **34 MPa** (ε 0.071) → 고원 평균 **10.2 MPa** (ε 0.25–0.55 · 4.5–15.6) · 맞춤선 극대 21.6 MPa (ε 0.085) · 극소 9.6 MPa (ε 0.49) = *"much flatter stress plateau"* · 하중이 떨어지는 것 = snap-through | 평평한 고원 없음 — 맞춤선 12.4 (ε 0.1) · 23.9 (0.2) · 31.7 (0.3) · 38.4 (0.4) · 58.1 MPa (0.5) = *"For the random microstructure the response is monotonic"* | [판독] · 따옴표는 인쇄 p.606–608 |
| 치밀화 (처음 70 %) | 맞춤선 19.8 (ε 0.6) · 44.6 (0.65) · **98.7 MPa (0.7)** · 맞춤선이 고원 극소의 2 배가 되는 곳 ε ≈ 0.60 | 122.8 (0.6) · 188.6 (0.65) · **289 MPa (0.7 · 맞춤)** / 361 MPa (0.7 · 빠른 런 원자료) | [판독] · 2 배 기준은 카드가 정함 |
| 치밀화 (전 구간 · Fig. 3) | 77 (ε 0.7) · 377 (0.8) · 1,441 (0.85) · 2,705 (0.88) · **3,896 MPa (0.9)** (직전 최대 4,090) | 361 (0.7) · 1,138 (0.8) · 2,591 (0.85) · 4,473 (0.88) · **6,673 MPa (0.9)** | [판독 · 벡터 경로] |
| 끝 반력 ÷ 뼈대 계수 | 0.22 E · 0.38 K | 0.38 E · 0.65 K | [카드 산술] |
| 꽉 찬 블록 (Fig. 1) 대비 | 끝 값의 1/70 | 1/43 — 본문 *"approximately two orders of magnitude lower"* | [카드 산술] · 인쇄 p.605 |
| Gibson–Ashby '항복' (고원 진입) 응력선 (Fig. 6) | **5.53 MPa** | **8.13 MPa** | [판독 · 벡터 좌표] (값 · 식 미인쇄) |
| 그 선의 꼴 | 두 값의 비 1.468 ≈ (9.6/7.9)² = 1.477 (지수 1.5 이면 1.340) → σ ∝ φ² · E_s 17.49 GPa 로 나누면 계수 **0.0507 · 0.0504** ⇒ σ ≈ 0.05 E_s φ² 로 읽힌다 | ← | [카드 산술 — 역산 · 식과 계수는 논문에 없다] |
| 맞춤선 ÷ G&A 선 | 고원 1.7–1.9 · 봉우리 3.9 · 선을 넘는 곳 ε 0.010 | ε 0.1 에서 1.5 · 0.3 에서 3.9 · 선을 넘는 곳 ε 0.066 | [판독 + 카드 산술] |
| 저자 판정 | *"These numerical simulations results are as consistent with this guideline as many experimental data."* | ← | 인쇄 p.608 |

### 3-6. ★ 기공 (식 1 · 2 · Fig. 8)

**정의 (p.610 · 그림 `eq_01_porosity_definition.png` · `eq_02_incompressible_foam_porosity.png` · 문단째 `eq_01_02_porosity_definitions_in_text.png`)**

> *"Because material deformation is tracked at each material point, it is possible to extract the porosity throughout the simulation.  The porosity, p, is defined as*
> **p = (V_bulk − V_microstructure) / V_bulk,   (1)**
> *where V_bulk is the volume under the piston, or the "bulk" foam volume and V_microstructure is the volume occupied by the foam microstructural network.  …  The porosity of an incompressible foam, where V_microstructure = Const., may be expressed in terms of the relative density and engineering strain, ε_eng,*
> **p_inc = 1 − φ / (1 − ε_eng).   (2)"**

- 논문이 '기공을 어떻게 셌는가' 에 대해 적은 것은 이 문단이 **전부**다.  V_microstructure 를 물질점 부피의 합으로 구했는지 · GIMP 입자 영역의 부피로 구했는지 · 격자 점유로 구했는지는 인쇄돼 있지 않다 [미확인].
- 식 (2) 는 옆 변형이 0 (일축 변형) 이고 뼈대 부피가 그대로일 때의 산술이다.  p_inc = 0 이 되는 변형률 ε = 1 − φ 가 이 논문의 **'완전 치밀화'** 다 — lattice 0.921 · random 0.904 [카드 산술].  계산은 0.90 에서 멈춘다 (*"The maximum compression simulated is essentially that required to remove all void space from the microstructure, or "fully densify" them (assuming incompressibility)."* p.605).
- **항등식 [카드 산술]**: 식 (1) ÷ 식 (2) → (1 − p)/(1 − p_inc) = V_microstructure/V_microstructure,0 ≡ **J** (뼈대의 평균 부피비) ⇒ **p − p_inc = (φ/(1 − ε))(1 − J)**.  기공이 비압축 추정보다 크다 = 뼈대가 눌렸다 (J < 1), 작다 = 뼈대가 불었다 (J > 1) — 같은 말이다.

| ε | lattice p | lattice p_inc | lattice J | random p | random p_inc | random J |
|---|---|---|---|---|---|---|
| 0 | 0.9218 | 0.9218 | 1 | 0.9029 | 0.9029 | 1 |
| 0.1 | 0.9169 | 0.9132 | 0.957 | 0.8950 | 0.8919 | 0.972 |
| 0.3 | 0.8784 | 0.8882 | **1.088** | 0.8665 | 0.8611 | 0.961 |
| 0.5 | 0.8315 | 0.8436 | 1.078 | 0.8186 | 0.8056 | 0.933 |
| 0.7 | 0.7355 | 0.7393 | 1.014 | 0.7042 | 0.6760 | 0.913 |
| 0.8 | 0.6060 | 0.6088 | 1.007 | 0.5684 | 0.5140 | 0.888 |
| 0.85 | 0.4965 | 0.4778 | 0.964 | 0.4669 | 0.3516 | 0.822 |
| 0.88 | 0.4031 | 0.3471 | 0.914 | 0.4036 | 0.1892 | 0.736 |
| **0.9** | **0.3452** | 0.2176 | **0.837** | **0.3844** | 0.0283 | **0.634** |

(p · p_inc = [판독 · 벡터 경로] · J = (1 − p)/(1 − p_inc) [카드 산술])

| 항목 | 값 | 표지 |
|---|---|---|
| 출발 기공 | 0.9218 · 0.9029 → φ₀ = 0.0782 · 0.0971 (비압축 곡선을 식 2 에 맞추면 0.07825 · 0.09718) — 인쇄된 7.9 · 9.6 % 와 0.1 %p 다르다 | [판독] |
| ε 0.9 에 남은 기공 | lattice **0.345** · random **0.384** = 본문 *"about 35% porosity is retained near full densification"* | [판독] · 인쇄 p.611 |
| 비압축 추정과의 차 (ε 0.9) | lattice +0.128 (0.345 ↔ 0.218 — 계산이 lattice 의 '완전 치밀화' 0.921 에 못 미친 채 끝나 비압축이어도 0.218 이 남는다) · random +0.356 (0.384 ↔ 0.028) | [판독 + 카드 산술] |
| 뼈대의 평균 부피비 J (ε 0.9) | lattice **0.837** · random **0.634** = 뼈대가 부피로 16 · 37 % 눌렸다 | [카드 산술] |
| random 끝 상태의 맞아떨어짐 | 반력 ÷ 고체 분율 = 6,673/(1 − 0.384) = **10.8 GPa** ↔ J 0.634 인 neo-Hookean 일축 변형 응력 **11.0 GPa** — 끝 상태가 '틈을 낀 채 통째로 일축으로 눌린 뼈대 기둥' 과 같다.  lattice 는 5.9 ↔ 3.8 GPa 로 덜 맞는다 (더 불균일) | [판독 + 카드 산술 · §3-1 의 역확인 식] |
| lattice 가 비압축 추정 **아래**로 가는 구간 | ε **0.18–0.81** 에서 p < p_inc · 차의 최소 −0.0137 (ε 0.365) → J 최대 **1.11** (ε 0.36) | [판독 + 카드 산술] |
| 그 구간에 대한 저자 설명 | *"This is likely due to competition between regions of compression and tension during snap-through of this microstructure."* | 인쇄 p.610 |
| 그 설명의 산술 점검 | 정적 평형이면 뼈대 안 압력의 부피 적분 = 거시 평균 압력 × V_bulk 이고, §3-1 의 체적항이면 그 적분 = (K/2)(1 − ⟨J²⟩) V₀ 다.  ⟨J⟩ = 1.11 이면 ⟨J²⟩ ≥ 1.23 → 뼈대에 평균 **1.2 GPa 의 순 인장**이 있어야 한다 — 그 구간의 반력은 압축 10 MPa (÷ 고체 분율 0.14 ≈ 75 MPa) 다.  ⇒ 뼈대 부피가 11 % 느는 것은 이 구성식으로는 일어날 수 없고, **부피 측도 (V_microstructure) 의 오차**로 읽힌다 | [카드 산술 + 카드 추론 — 논문 밖] |
| random 의 '갇힘' | ε 0.88 → 0.90 에서 random 0.4036 → 0.3844 (느려짐) · lattice 0.4031 → 0.3452 (계속 내려감) · 두 곡선은 ε 0.88 에서 엇갈린다 — 본문 *"the microstructure becomes pinned near full densification and porosity is "locked in""* | [판독] · 인쇄 p.610 |
| 민감도 | dp/dJ = −φ₀/(1 − ε) = −0.16 · −0.19 (ε 0.5) → **−0.78 · −0.97 (ε 0.9)** : 조밀 끝에서 뼈대 부피의 상대 오차 10 % = 기공 8–10 %p | [카드 산술] |
| 실험과의 대조 (저자) | Smith et al. (2001) X 선 단층: 처음 기공 **48 %** 인 열린 셀 발포체가 ε_eng 0.5 (*near full densification*) 에서 **13 %** · 0.6 (*well past full densification*) 에서 **6 %** | 인쇄 p.611 |
| 밑에서 본 그림의 뚫린 넓이 (Fig. 7 맨 아래 칸) | random 5.1 % · lattice 12.5 % (가장 큰 구멍 2.1 % · 4.0 %) — 부피 기공 (0.384 · 0.345) 과 **순서가 반대** | [판독 · 내장 래스터 화소] |

### 3-7. 재료 상수를 두 배로 (Fig. 9–11)

| 항목 | 값 | 표지 |
|---|---|---|
| 저자 판정 | *"At any given strain the stiffer foams support approximately twice the load.  …  Given only two examples it is not conclusive, but it appears the bulk response scales with the network constitutive response as could be predicted based on Hertzian contact mechanics."* | 인쇄 p.611–612 |
| 치밀화 구간의 배율 | ε 0.9: random 6,673 → 13,631 MPa (**×2.04**) · lattice 3,896 → 8,222 MPa (**×2.11**) · ε 0.85–0.88: ×2.00 · ×1.88–1.94 | [판독] |
| 중간 변형률의 배율 (원자료) | ε 0.5–0.8 에서 random ×1.42–2.10 · lattice ×1.75–2.66 | [판독] |
| 처음 70 % 의 평균 배율 (원자료 · ε 0.05–0.68) | random ×1.81 (0.3–0.55 에서 ×1.65) · lattice ×1.74 (0.3–0.55 에서 ×2.37) | [판독 + 카드 산술] |
| 맞춤선의 배율 | random ε 0.3–0.68 에서 ×1.9–2.4 · lattice ×1.6–2.8 | [판독] |
| 곡선의 엇갈림 | 단단한 lattice 가 무른 random 을 ε ≈ **0.83** 에서 넘는다 — 본문: 상대밀도와 별개인 셀 형상 의존 · *"the collapse process for the lattice unit cell results in a less efficient packing of material during densification"* | [판독] · 인쇄 p.612 |
| stiffened 런의 판 속도 | 반력이 ε 0.0226–0.0228 에서 뜬다 = 0.0319/√2 = 0.0226 → **판의 절대 속도를 그대로 둔 것** (판 속도 ÷ 종파속 = 0.021) | [판독 + 카드 산술] |
| lattice 의 예외 | *"Here it is less clear that the stiffer foam supports approximately twice the load early in the stress plateau region.  This region is associated with the snap-through process which, if unstable, will be dominated by inertial effects."* | 인쇄 p.612 |

### 3-8. 실험 · 지침과의 대조 — 무엇과 견줬고 얼마나 맞았나

| 견준 것 | 논문의 문장 | 수준 |
|---|---|---|
| 꽉 찬 블록의 해석해 | Fig. 1 · ≈ 5 % (끝) | **정량** (1 건) |
| 절반 속도 런 | Fig. 4 · *similar* | 눈 대조 (카드 판독: 구간 평균 2–35 % 차) |
| Gibson and Ashby (1997) 의 '항복' 응력 | Fig. 6 수평선 · *as consistent with this guideline as many experimental data* | 같은 자릿수 (카드 판독: 1.5–3.9 배) |
| Zhu et al. (1997) 단일 기공 압축 실험 | 두 시편 가운데 하나는 *"a very flat stress plateau very much like the lattice simulation"* 이고 변형 뒤 규칙성이 깨졌다 · 다른 하나는 단조 (판에 **접착**돼 대칭 유지) | 정성 (그림 · 수치 대조 없음) |
| Shulmeister et al. (1998) FEM | 대칭을 지킨 큰 단위 셀에서 단조 응답 — 저자: *"these results are not representative of real foam pore collapse"* | 정성 (반론) |
| Smith et al. (2001) X 선 단층의 기공 | 48 % → 13 % (ε 0.5) → 6 % (ε 0.6) ↔ 계산 90 % → ≈ 35 % | "남는다" 는 **방향**만 (재료 · 처음 기공 · 값이 다르다) |
| 벌집 · 규칙 셀의 줄 단위 붕괴 (Gibson–Ashby · Papka–Kyriakides · Tanaka 외 · Meguid 외) | 규칙 구조 = 평평한 고원 + 큰 진동 · 발포체 = 매끈 · 단조 | 정성 (결론 절) |

### 3-9. 계산 비용

| 항목 | 값 | 표지 |
|---|---|---|
| 병렬 여부 | *"(serial) calculations"* | 인쇄 p.615 |
| 물질점 수 · 걸음 수 · 계산 시간 · 기계 | **[미확인]** | — |
| 앞으로 필요하다고 적은 규모 | *"a large scale computation capability in order to handle a microstructure containing 100–1000 pores"* (이 논문은 사실상 기공 하나: *"essentially, single pores of foam material"*) | 인쇄 p.614–615 |
| 암시적 풀이에 대한 말 | *"Currently these algorithms are expensive, and remain an area of algorithm research for GIMP methods Cummins and Brackbill (2002), Guilkey and Weiss (2003)."* | 인쇄 p.602 |

### 3-10. ★ 이 논문에 **없는** 값 (정직 목록)

| 찾은 것 | 상태 |
|---|---|
| 소성 · 점탄성 · 마찰 · 분리 판정 · 하중 제거 (되돌아옴 · 잔류 변형) | **없음** (탄성 · no-slip · 한 방향 압축) |
| 격자 수렴 시험 · 셀당 물질점 수 · 물질점 수 | **없음 / [미확인]** — 셀 0.01 mm 한 가지 |
| 단위 셀의 변 길이 · strut 지름 · strut 개수 · 격자 종류 | **[미확인]** (그림뿐) |
| 시간 간격 · 안전계수 · 인공 점성의 꼴과 계수 | **[미확인]** |
| 접촉 알고리즘의 이름 · 접촉이 걸리는 거리 | **[미확인]** (*no-slip contact*) |
| V_microstructure 의 계산식 | **[미확인]** |
| 저장 에너지 함수 · Gibson–Ashby 식과 계수 · 다항 맞춤의 계수와 맞춘 자료 | **[미확인]** (카드가 그림에서 역산 — §3-1 · §3-5 · §3-4) |
| Fig. 7 의 색 눈금 · 문턱 값 | **없음** |
| 운동 에너지 · 내부 에너지 시계열 (준정적 지표) | **없음** — 판정은 반력 곡선 두 개의 눈 대조 |
| 옆 (면내) 방향 반력 · 응력 텐서의 평균 | **없음** |
| 발포체 계산에서 피스톤 쪽 반력 (바닥 반력과의 대조) | **없음** |
| DEM · 분말 · 입자 층 | **없음** |

---

## 4. 방법 ★

### 4-1. 입자 기법 — PIC → MPM → GIMP (§2 · p.600–601 · 식 없음)

- **계보 (저자 서술)**: PIC (유체 · Harlow 1963) → 수치 확산을 줄인 개량 (Brackbill 외 1988 · Burgess 외 1992) → 물질점이 구성식의 상태 변수를 싣는 **MPM** (Sulsky 외 1994 · 1995) → 접촉 (Bardenhagen 외 2000 · 2001) → **GIMP** (Bardenhagen and Kober 2004): *"a general mathematical framework … which allows MPM to be derived as a special case.  The GIMP method framework addresses accuracy in handling large material deformations"*.
- **이산화**: 물체를 물질점으로 — 물질점이 구성 변수 · 응력 · 변형률 · 속도 · 온도를 전부 싣고 **계면도 암묵적으로 추적**한다.  형상 이산화는 *"A regular grid of candidate material point positions is generated.  At positions found to lie inside a given body material points are generated.  The resulting discretization is similar to using pixels to represent an image."* (p.600) — 몸에 맞춘 격자가 필요 없다.
- **풀이**: 물질점 정보를 겹쳐 놓은 격자로 보간 → 격자에서 **갱신 Lagrange 꼴 운동량 보존식**을 풂 (*"computational scratch pad"*) → 갱신을 물질점으로 보간 → 격자를 버림.  질량 보존은 물질점 질량을 고정해 자동.  *"A new grid is generated each computational time step … eliminating mesh tangling problems.  For the calculations presented here the grid is reset to it's original configuration each timestep for simplicity and hence appears stationary in space, or "Eulerian"."* (p.601)
- **성격 (저자)**: ALE 기법 (*"Lagrangian particles moving through an Eulerian mesh"*) · 가상일 원리의 Petrov–Galerkin 이산화 (*"a more general scheme than used in the FEM"*) · 입자 쌍 상호작용이 아니라 **격자를 거쳐** 상호작용 (SPH 와의 차이).
- **변종**: *"the contiguous particle GIMP method used here"* (p.603) — 물질점이 셀 경계를 넘을 때의 작은 오차가 큰 변형률에서 반력의 뾰족한 튐으로 나타난다 (Fig. 1).
- 알고리즘의 식 (보간 함수 · 격자 갱신 · 시간 적분) 은 **이 논문에 없다** — *"The interested reader is referred to the references in this section for algorithmic details."*  그래서 이 카드의 식 그림은 식 (1) · (2) 와 문장 속 정의 둘뿐이다.

### 4-2. 구성식 (§3.1 · p.602)

- 압축성 neo-Hookean (비선형) 탄성 · Simo and Hughes (1998) 인용 · K 10.2 · G 7.2 GPa · ρ 1900 kg/m³.  *"Note that the material model stiffens dramatically at large compressions, a realistic aspect of large compression material response."*
- 속도 무관 (*"the material response is not rate dependent"*) → 관성과 이산화 오차가 없으면 수치 해 = 해석해여야 한다는 것이 Fig. 1 시험의 논리다.
- 저자의 한정: *"It should be noted that elastic material models and no-slip contact are used in these simulations.  For polymeric foams these are probably reasonable approximations.  The philosophy adhered to is to include sufficient model complexity to credibly model foam compression into the densification regime.  Hence these simulations include network microstructures, finite deformation constitutive response, and contact between arbitrary network components."* (p.601)

### 4-3. 접촉 · 경계 (p.599–601 · p.604)

- **자기 접촉**: 뼈대가 접히며 strut 끼리 · strut 과 피스톤 · strut 과 바닥 (대칭면) 이 닿는다.  FEM 의 주–종 (master–slave) 접촉은 닿을 면을 미리 지정해야 하는데 발포체에서는 *"only possible early in the deformation …, if at all"* (p.599).
- **이 계산의 접촉 = no-slip** (p.601).  어떤 알고리즘인지 · 접촉이 걸리는 거리 · 닿았던 면이 다시 떨어지는지는 적혀 있지 않다.  물체가 하나 (뼈대) 라 물체마다 속도장을 두는 다물체 알고리즘 (짝 카드) 으로는 자기 접촉을 가를 수 없으므로, **격자 한 벌의 속도장이 주는 붙는 접촉** — 같은 격자 노드를 나눠 쓰게 된 물질점들이 한 속도로 움직임 — 으로 읽힌다 [카드 판독].  마찰 미끄럼은 *"will be studied later"*.
- **경계**: 위 = 일정 속도 피스톤 · 아래 = 대칭면 (바닥에서 반력을 잰다) · 옆 = 주기 → 옆 변형 0 (일축 변형) 의 무한 층 (두 셀 두께).

### 4-4. 준정적 · 시간 적분 (p.602–603 · p.606)

- GIMP 는 주로 동역학에 쓰여 **명시적 풀이가 가장 발달**했고, 준정적에는 암시적 풀이가 낫지만 비싸고 연구 중이라 (p.602) 명시적 코드를 **천천히** 돌린다.
- 조건 두 가지 (p.603): 판 속도가 재료 파속의 작은 분율 (3 %) · 총 시간이 파가 블록을 건너는 시간보다 길 것 (30 배).  + 파면의 수치 울림을 죽이는 인공 점성.
- 발포체에서는 구조 붕괴가 *"potentially an inertial process"* 라 절반 속도 런으로 관성 영향을 확인 (Fig. 4) → 빠른 속도를 채택.
- 반력 곡선의 '잡음' = 구조를 지나온 응력파의 도착 + strut 이 바닥에 닿는 충돌 사건 (p.605) → 5차 다항 맞춤을 *"a reasonable representation of the bulk static stress–strain curve"* 로 쓴다 (p.606).

### 4-5. 측정량

| 양 | 정의 | 위치 |
|---|---|---|
| 반력 (traction) | 하중 ÷ 재는 넓이 (압축 +) · 발포체는 바닥 경계에서 | p.603 · p.605 |
| 공칭 변형률 ε_eng | 길이 변화 ÷ 처음 길이 (압축 +) | p.603 |
| 상대밀도 φ | ρ_foam/ρ_solid (그림 `eq_unnumbered_s3_2_relative_density.png`) | p.604 |
| 기공 p · 비압축 기공 p_inc | 식 (1) · (2) | p.610 |
| 등가 응력 σ_eq | **σ_eq = √(1.5 Σ_ij σ′_ij σ′_ij)**, σ′ = 편차 응력 — *"a norm of the stress tensor …  This measure emphasizes regions of high shear."*  Fig. 7 의 색 (그림 `eq_unnumbered_s3_2_equivalent_stress.png` · 인쇄 그대로는 `…_in_text.png`) | p.608 |
| 매끈한 곡선 | 원자료의 5차 다항 맞춤 | p.606 |

### 4-6. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

| 축 | 이 논문 |
|---|---|
| 물체 | **뼈대 한 물체** (구 노드 + strut) + 피스톤 — 알갱이 집합이 아니다 |
| 무질서 | lattice = 노드 위치를 셀 크기의 3–8 % 흔듦 (시드 · 분포 미인쇄) · random = 손으로 만든 구조 **하나** — 통계 (여러 실현) 없음 |
| 크기 | 단위 셀 하나 (사실상 기공 하나) · 대표 부피가 아님을 저자가 명시 (p.610 · p.614) |
| 변형 | 탄성 큰 변형 (굽힘 · 좌굴 · 접힘) — **형상 변화는 있으나 소성 흐름은 없다** |
| 접촉 | 붙음 (no-slip) · 자기 접촉 |
| 강체 | 없음 (피스톤은 일정 속도 경계) |

---

## 5. 결과 — 절별

### 5-1. 서론의 논증 (§1 · p.598–600)

발포체의 준정적 압축 응답은 세 구간이다 — 고르게 변형하는 **탄성**, 약한 곳에서 굽힘이 국소화돼 퍼지는 **붕괴** (*"stress plateau" where large displacements occur at essentially constant force*), 뼈대가 스스로에게 접혀 닿으며 급격히 굳는 **치밀화**.  미세구조의 형상 효과와 재료 효과를 실험으로 가르기 어렵다 (발포가 곧 경화라 *"there is no corresponding "bulk material""*) → 수치 계산이 필요한데, FEM 은 세 가지 (형상 이산화 · 큰 변형 · 자기 접촉) 때문에 *modest deformation* 에 머물렀다.  같은 세 가지가 입자 기법의 강점이다.  목적은 치밀화 구간의 물리 — 특히 준정적에서 강한 충격까지의 속도 범위에서 쓸 **거시 (평균) 구성 모형**을 고치는 데 필요한 미세구조 정보이고, 결론을 미리 적는다: *"porosity is an important microstructural feature which must be accounted for (independently of bulk strain) by bulk constitutive models operating in the densification regime."* (p.600)

### 5-2. 구성 재료의 응답 (§3.1 · Fig. 1)

명시적 풀이가 준정적 큰 변형을 낼 수 있는지 먼저 본다.  꽉 찬 블록의 일축 변형 압축에서 수치 해는 해석해를 90 % 변형률까지 따라가고 끝 오차는 약 5 % 다 — 몸에 맞춘 격자였다면 셀 종횡비가 10 이 됐을 변형이다.  큰 변형률의 튐은 물질점이 셀 경계를 넘을 때의 오차다.  *"the numerical solution is accurate for larger strains than are expected in the compression of the foam microstructures (which are approximately 90% void)"* — 발포체 계산의 설정 (판 속도 · 셀 크기) 을 여기서 정한다.

### 5-3. 전 구간 응답 (Fig. 3)

두 셀 모두 약 90 % 가 빈 공간이므로 90 % 압축은 *"first to collapse the microstructure and remove void space, and second to compact the collapsed structure"*.  전 구간 눈금에서는 급격한 굳음 (*"the signature of compression in the densification regime where contact mechanics plays an important role"*) 만 보이고, random 이 조금 이른 변형률에서 굳는다 (상대밀도가 조금 높아서).

### 5-4. 처음 70 % — 잡음 · 속도 · 맞춤 (Fig. 4 · 5 · 6)

반력의 잡음은 물리 (strut 충돌) 이고 그 크기는 작은 단위 셀 탓이다.  절반 속도 런과 비슷하므로 빠른 속도를 준정적 대표로 쓴다.  lattice 는 훨씬 평평한 고원을, random 은 단조 증가를 보인다.  Gibson–Ashby 의 '항복' 응력 (상대밀도와 뼈대 물성만으로 계산 · 규칙성은 안 들어감) 은 고원으로 넘어가기 시작하는 응력의 좋은 근사로 알려져 있고, 계산은 *"as consistent with this guideline as many experimental data"*.

### 5-5. 변형 모양 — 굽힘 · 좌굴 · snap-through (Fig. 7 · p.608–610)

10 % 변형률에서 이미 응력 분포가 **굽힘과 strut 이음매 강성**이 지배함을 보인다.  30 · 50 % 에서 굽힘이 이어지고 높은 응력 재료가 서서히 는다.  70 % 에서 접촉이 넓어지고 낮은 응력 구역이 사라지기 시작한다 (치밀화).  90 % (밑에서 본 그림) 에는 낮은 응력 구역이 없다.  같은 압축에서 두 셀의 응력 분율은 비슷하다 (*"suggesting that similar microscale deformation mechanisms are occurring"*).
lattice 는 규칙성을 차츰 잃는다 — 30 % 에서는 반대칭 좌굴 모드 비슷한 질서가 남고 50 % 에서는 거의 사라진다.  완전한 격자는 대칭면을 가진 해를 가져야 하고 좌굴 뒤의 해가 불안정하면 snap-through 가 난다; 흔든 격자는 수학적 의미의 좌굴은 아니지만 10–30 % 사이에서 해의 성격이 빠르게 바뀌고 그 구간에 하중 극대가 있다.  random 은 깰 대칭이 없어 단조다.
실험 (Zhu 외 1997 · 단일 기공) 의 두 시편 가운데 평평한 고원을 보인 쪽은 변형 뒤 규칙성이 깨져 있었고, 단조였던 쪽은 판에 접착돼 대칭을 지켰다 — 저자는 대칭을 지킨 계산 · 실험이 *"not representative of real foam pore collapse"* 라고 주장한다.  그리고 자기 결과의 대표성도 한정한다 (RVE · §0-2 (iii)).

### 5-6. ★ 기공 (식 1 · 2 · Fig. 8 · p.610–611)

두 셀은 처음에 거의 비압축처럼 움직인다.  random 은 변형이 커질수록 실제 기공이 비압축 추정보다 **항상 크고** (압축 하중 + 재료 압축성과 맞는 방향), 완전 치밀화 근처에서 뼈대가 걸리며 (*pinned*) 크게 벌어진다 — 기공이 *"locked in"*.  lattice 는 고원과 이른 치밀화 구간에서 기공이 비압축 추정보다 **작고** (저자: snap-through 중 압축 · 인장 구역의 경쟁 때문일 것), 치밀화 구간에서 결국 더 커진다.  남은 기공은 Fig. 7 맨 아래 칸에서 보인다.
이 결과는 X 선 단층 실험 (Smith 외 2001) 과 방향이 같다.  그리고 공학적 가정에 대한 반박으로 쓴다:

> *"A tempting engineering assumption is that foams will have had all porosity removed at full densification.  Hence, while the stress state is clearly non-uniform, the material may be approximated as a continuous solid.  In fact, porosity is not easily removed from these materials under quasi-static deformation.  …  Consequently, the assumption that foams are essentially incompressible would be significantly in error near full densification, and would result in completely overlooking important physical processes."* (p.611)

근거로 드는 물리는 응력파다 — 빈 곳은 물성 대비의 극단이라 파면이 흐트러지고 분산이 생긴다.

### 5-7. 재료 상수 두 배 (Fig. 9–11 · p.611–613)

어느 변형률에서나 단단한 쪽이 약 두 배의 하중을 진다 → 같은 미세구조면 붕괴 · 치밀화 과정이 같고 응력만 두 배.  작은 압축에서는 당연하지만 큰 변형 접촉이 이 관계를 깰 수도 있다고 보았는데 그렇지 않았다 (*"Given only two examples it is not conclusive"*).  단단한 lattice 가 무른 random 을 넘는 것은 상대밀도와 별개의 셀 형상 의존이다.  lattice 의 고원 초입 (snap-through) 은 관성이 지배할 수 있어 두 배가 덜 분명하다.

### 5-8. 결론 · 향후 (§4 · p.613–615)

세 가지를 적는다 — ① 규칙 구조는 불안정한 snap-through 를 보일 수 있고 무질서한 셀은 그렇지 않다 (구조 안정 이론과 맞음 · 발포체가 매끈한 까닭이 기공 간 무질서인지 기공 수준 snap-through 가 없어서인지는 *"an open question"*) ② 완전 치밀화 뒤에도 기공이 상당히 남는다 → *"fully densified foams are not well approximated as void free, continuous material"* ③ 거시 응답이 뼈대 물성에 비례해 는다 (*"advanced tentatively as a possible "rule of thumb""* · 기공 하나짜리 계산이라는 단서).
실제 발포체에는 (1) 대표 미세구조 (Kraynik 2003 의 생성 기법 · X 선 단층 영상 — *"provides a data format which should be easily discretized via particle methods"*) (2) 100–1000 기공 규모의 계산 (3) 미세구조 변화를 뽑는 분석이 필요하다.  끝 목표는 기공 크기 분포의 변화를 쓰는 통계 구성 모형 (Schraad and Harlow 2004) 과의 대조이고, *"A first step toward this capability, extraction of porosity evolution, has been demonstrated."*

---

## 6. 그림별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/bardenhagen2005_mpm_foam_densification_simulation/` · 그림 11 장 (전부 손으로 다시 자름 · 400 dpi · 사방 6 pt · 캡션 글자 제외) + 식 그림 6 장 (400 dpi · 사방 7 pt).  표 없음.  [우리 …] 표지는 논문 밖 판단.

| 그림 | 파일 | 원 캡션 요지 | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | 압축성 neo-Hookean 재료의 일축 압축 — 해석해 ↔ 수치 해 | 꽉 찬 블록 (1 mm³ · 셀 0.01 mm) 을 일축 변형으로 90 % 까지 — 이 논문의 유일한 정량 검증.  [판독] 끝: 수치 286,061 ↔ 해석 271,063 MPa (+5.5 %) · 구간 평균은 어디서나 +5.5–6.6 % · 수치 곡선은 ε ≈ 0.029 에서 뜬다 (파가 반대쪽에 닿는 때).  해석 곡선은 §3-1 의 식과 0.1 % 안 [카드 산술].  ε 0.9 에서 응력 5 % = 판 위치 0.32 셀.  **우리 쪽**: 명시적 MPM 준정적 설정의 단위 시험 꼴 — 접촉 없는 꽉 찬 블록 + 해석해 · 오차는 변형률 구간별로 적는다 (단계 2 의 단위 시험) |
| 2 | `fig_2.png` | 두 단위 셀의 처음 모양 — 왼쪽 random · 오른쪽 lattice | 검은 판 = 일정 속도 피스톤 · 바닥 = 대칭면 · 옆 = 주기.  [판독] strut 지름 ÷ 셀 변 ≈ 0.10–0.14 — 셀 변 길이 · strut 당 셀 수는 미인쇄.  **우리 쪽**: 입자 층이 아니라 가는 뼈대 한 물체 — 접촉은 전부 자기 접촉 (붙음) 이다.  우리 SE 물질점들도 한 속도장 안에서는 '한 물체' 와 같은 처지다 [우리 코드 판독 · `grid_v` 한 벌 · 2808 행] |
| 3 | `fig_3.png` | 두 발포체의 준정적 일축 압축 응답 (전 구간) | [판독] ε 0.9: lattice 3,896 MPa · random 6,673 MPa = 뼈대 K 의 0.38–0.65 배 · Fig. 1 끝 값의 1/70 · 1/43.  **우리 쪽**: '완전 치밀화' 근처에서 반력이 뼈대 강성에 육박 — 탄성 뼈대가 기공을 낀 채 통째로 눌리는 체제 (우리 300 MPa ≈ SE 체적 계수의 1 % 와 다른 체제 · 값 전이 없음) |
| 4 | `fig_4.png` | random 셀을 두 속도로 누른 응답과 다항 맞춤 | ★ 준정적 판정의 전부.  [판독] 평균 반력의 비 (0.030 ÷ 0.015): ε 0.05–0.3 1.02 · 0.3–0.55 1.35 · 0.55–0.7 1.09 · ε 0.7 에서 361 ↔ 289 MPa.  맞춤선은 느린 런 쪽 (rms ≈ 2 ↔ 13 MPa).  0.030 곡선은 ε 0.68 에서 그림 위로 나간다 · x 축 이름의 g 아래 끝은 원본 PDF 에서 잘려 있다.  **우리 쪽**: 판 Mach 0.03 ↔ 0.015 쌍의 제3자 사례 — 구조가 무너지는 구간의 반력은 이 속도 수준에서 절반으로 줄이면 평균 35 % 달라졌고 저자 판정은 눈이다 |
| 5 | `fig_5.png` | lattice 셀의 응답과 다항 맞춤 (처음 70 %) | [판독] 원자료 봉우리 34 MPa (ε 0.071) → 고원 평균 10.2 MPa · 맞춤선 극대 21.6 · 극소 9.6 MPa.  봉우리 뒤 하중 감소 = snap-through.  **우리 쪽**: 반력 곡선을 다항식으로 매끈하게 하면 봉우리가 깎인다 (34 → 21.6) — 판독에는 원자료를 같이 둔다 |
| 6 | `fig_6.png` | 두 셀의 근사 준정적 응답 (맞춤선) 과 Gibson–Ashby 식의 항복 응력 추정 | [판독] G&A 선 lattice 5.53 · random 8.13 MPa → 0.05 E_s φ² 꼴로 읽힘 [카드 산술 · 식은 미인쇄].  맞춤선은 그 선의 1.5–3.9 배.  random 선은 Fig. 4 의 맞춤 (느린 런 쪽) · lattice 선은 빠른 런의 맞춤 — **속도가 다른 두 선**이 한 그림에 있다 [카드 산술 — §3-4].  범례 *plateau stress* ↔ 캡션 *yield stress*.  **우리 쪽**: 값 전이 없음 — '공학 지침의 1.5–3.9 배' 가 이 논문의 검증 수준이라는 것만 |
| 7 | `fig_7.png` | random (왼) · lattice 셀의 변형 — 위에서 아래로 10 · 30 · 50 · 70 · 90 % (맨 아래는 밑에서 봄) · 물질점을 등가 응력으로 칠함 | 색 눈금 · 문턱 값 없음.  [판독] 밑에서 본 칸의 뚫린 넓이 random 5.1 % · lattice 12.5 % ↔ 부피 기공 0.384 · 0.345 (순서 반대).  **우리 쪽**: ① 투영 · 단면으로 본 기공과 부피 기공은 순서가 다를 수 있다 (단면 SEM ↔ 질량 기준 기공의 대조에 주의) ② 붙는 (no-slip) 접촉으로 자기 접촉을 공칭 90 % 까지 끌고 간 그림 — 격자 얽힘이 없다 |
| 8 | `fig_8.png` | 압축 중 두 셀의 기공 — 계산값과 비압축 가정값 | ★ §3-6.  [판독] ε 0.9: lattice 0.345 (비압축 0.218) · random 0.384 (비압축 0.028).  (1 − p)/(1 − p_inc) = J → 0.837 · 0.634 [카드 산술].  lattice 는 ε 0.18–0.81 에서 비압축선 아래 (J 최대 1.11) — 물리 범위 밖 (§3-6).  **우리 쪽**: 단계 0 — 우리 MPM 기공은 고체 부피를 고정한 식 (2) 꼴이다; 두 꼴의 차와 평균 응력 점검을 결과 전에 적는다 |
| 9 | `fig_9.png` | 재료 상수를 두 배로 했을 때의 두 셀의 응답 (전 구간) | [판독] ε 0.9: ×2.04 (random) · ×2.11 (lattice) · ε 0.5–0.8 은 ×1.4–2.7 로 흩어진다 · 단단한 lattice 가 무른 random 을 ε ≈ 0.83 에서 넘는다 · stiffened 런의 판 속도 ÷ 파속은 0.021 [카드 산술].  **우리 쪽**: 탄성 · 속도 무관 재료에서 응력이 계수에 비례하는 것은 차원 논리다 — 배율이 2 에서 벗어난 구간은 관성 · 무너짐 경로의 민감도가 드러난 자리 |
| 10 | `fig_10.png` | random — 재료 상수 두 배의 효과 (처음 70 % · 원래 / stiffened + 맞춤) | ⚠ 'original' 실선 (ε 0.7 에서 362 MPa) 은 Fig. 4 의 빠른 런이고 그 'polynomial fit' (289 MPa) 은 Fig. 4 의 맞춤선 (느린 런 쪽) 이다 — 실선이 자기 맞춤선 위에 있다 [판독].  맞춤선끼리의 배율 ×1.9–2.4 · 원자료 평균의 배율 ×1.81.  **우리 쪽**: 값 전이 없음 — 매끈하게 만든 선끼리 견줄 때 어느 런의 선인지 적는다 |
| 11 | `fig_11.png` | lattice — 재료 상수 두 배의 효과 (처음 70 %) | [판독] 맞춤 극대 21.6 → 37.5 MPa (×1.7) · stiffened 는 ε 0.5–0.62 에 둘째 혹 (원자료 최대 53 MPa) · 원자료 평균의 배율 ×1.74 (ε 0.3–0.55 에서는 ×2.37).  본문: snap-through 구간은 관성이 지배할 수 있다.  **우리 쪽**: 불안정 (좌굴 · 무너짐) 이 끼는 구간의 반력은 재하율 점검 없이 재료 효과로 읽지 않는다 |

**식 그림** (전부 손으로 자름 · 400 dpi · 사방 7 pt 흰 여백):

| 식 | 파일 | 내용 | 쓰임 |
|---|---|---|---|
| (1) | `eq_01_porosity_definition.png` | p = (V_bulk − V_microstructure)/V_bulk | ★ 기공 연산자 — V_bulk = 피스톤 아래 부피 · V_microstructure = 뼈대가 차지한 부피 (계산식 미인쇄) |
| (2) | `eq_02_incompressible_foam_porosity.png` | p_inc = 1 − φ/(1 − ε_eng) | 뼈대 부피 고정의 기준선 — 우리 MPM 의 기공 식과 같은 꼴 [우리 코드 판독] |
| (1)–(2) 문단 | `eq_01_02_porosity_definitions_in_text.png` | *"Having established … also presented in Fig.8."* 문단 전체 | 기호의 뜻이 문장에만 있어 정의째 붙일 때 (문맥 크롭 — 식만 자른 것은 위 두 장) |
| 번호 없음 (p.604) | `eq_unnumbered_s3_2_relative_density.png` | φ = ρ_foam/ρ_solid | 상대밀도 — 식 (2) 의 φ |
| 번호 없음 (p.608) | `eq_unnumbered_s3_2_equivalent_stress.png` | σ_eq = √(1.5 Σ_ij σ′_ij σ′_ij) | Fig. 7 의 색.  인쇄에서 근호 윗줄이 윗줄 글자와 닿아 있어 이웃 낱말을 가린 사본에서 그렸다 (식의 글자는 그대로) |
| 번호 없음 (p.608 · 인쇄 그대로) | `eq_unnumbered_s3_2_equivalent_stress_in_text.png` | 그 식이 든 세 줄 | 인쇄 그대로의 모습 (근호가 위 · 아래 줄과 겹침) |

---

## 7. Post-processing

| 무엇 | 어떻게 | 우리에게 |
|---|---|---|
| 반력–변형 곡선 | 바닥 경계의 하중 ÷ 넓이 대 피스톤 변위 ÷ 처음 길이 · 원자료 + 5차 다항 맞춤 | 우리 MPM 의 판 반력 (`wallP`) 은 **판 쪽**에서 잰다 [우리 기록] — 이 논문은 반대쪽 (바닥) 이라 파가 닿기 전 (ε < 0.03) 은 0 이다.  두 쪽을 다 재면 그 차가 관성의 크기다 [카드 추론] |
| 기공 | 식 (1) (물질점 추적) ↔ 식 (2) (비압축) 을 한 그림에 | 단계 0 의 대조 꼴 그대로 — '고체 부피 고정' 과 '추적한 부피' 를 나란히 |
| 등가 응력 지도 | 물질점을 σ_eq 로 칠하고 문턱 위는 한 색 · 모든 칸 같은 범위 | 색 눈금 값이 없어 정량 대조 불가 — 우리 그림에는 눈금과 문턱을 적는다 |
| 지침과의 대조 | Gibson–Ashby 응력을 수평선으로 | 발포체 전용 — 꼴만 (결과 전 등록한 외부 값과의 대조선) |
| 속도 대조 | 두 속도의 곡선을 겹침 + 맞춤선 | 구간 평균의 비 · 차의 rms 같은 **수** 로 판정을 적는다 (이 논문은 눈) |
| 민감도 | 재료 상수 두 배 | 차원 논리의 점검 (탄성 · 관성 없음이면 정확히 2) |
| **이 카드의 판독** (논문 밖) | 벡터 그림 9 장의 경로 좌표 → 틀 · 눈금으로 축 사상 → `digitized.csv` (곡선 27 개 · 요약 49 행) · 인쇄값과의 맞음 확인 (끝 오차 ≈ 5 % · *about 35%* · 두 배) · 해석 곡선의 식 역확인 · lattice 5차 맞춤의 재현 (rms 0.14 MPa) · 평균 응력 점검 | `[판독]` · `[카드 산술]` 의 출처 — 같은 PDF 가 있으면 다시 낼 수 있다 |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | 이 논문 | 우리 DEM | 우리 MPM |
|---|---|---|---|
| 기법 | 명시적 GIMP (contiguous-particle) · 격자 매 걸음 재설정 | LIGGGHTS 구 입자 [우리 기록] | 명시적 MLS-MPM (Taichi · 2차 B-spline) [우리 기록 · `hu2018…` 카드] |
| 물체 | 뼈대 한 물체 (상대밀도 8–10 %) | 구 수만 개 | SE 물질점 + 얼린 AM 장애물 [우리 기록] |
| 재료 | 탄성 neo-Hookean · K 10.2 · G 7.2 GPa (실제 계수 그대로 · 연화 없음) | 탄성–이력 접촉 · 무르게 맞춘 E_SE 1.35 GPa [우리 기록] | J2 소성 · E 1.53 · ν 0.49 (K 25.5 GPa) · σ_y 0.30 GPa [우리 기록] |
| 접촉 | 붙음 (no-slip) · 자기 접촉 · 알고리즘 미기재 | 접촉 법칙 (마찰 · 분리) | 한 속도장 (붙음) [우리 코드 판독 · 2808 행] |
| 하중 | 일정 속도 피스톤 → 공칭 90 % · 끝 반력 3.9–6.7 GPa | 300 MPa 까지 | 300 MPa (판 반력 판독) |
| 준정적 | 판 속도 ÷ 종파속 0.03 (대조 0.015) · 인공 점성 | — | `--platen-mach` 0.01–0.03 [우리 코드 판독 · 3076–3077 행] |
| 기공 | 식 (1) 추적 + 식 (2) 기준선 | ε_sphere (구 부피 합) [우리 기록] | `1 − solid_vol/(area·height)` — 고체 부피 고정 = **식 (2) 꼴** [우리 코드 판독 · 2794 · 3261 행] |
| 조밀 끝 | 기공 0.345 · 0.384 가 남는다 (탄성 · 붙음) | — | 얼린 AM 이 하중을 지지 않는 설정에서는 거의 다 메워진다 (ε_sphere 1.13 % — `fam_platen_prereg_20260812.md` §11) [우리 기록] |
| 탈압 | 없음 | — | — |
| 격자 수렴 | 없음 | 해당 없음 | 침대별 해상도 점검 있음 [우리 기록] |
| 검증 | 해석해 1 건 · 지침 · 정성 | 실험 기공 (따로 보정) | 실험 기공 · 형상 (따로 보정) |

### 8-2. 우리 MPM 기공 식과의 관계 [카드 산술 · 전부 논문 밖]

- 우리 식은 식 (2) 꼴이므로 식 (1) 꼴 (물질점 부피 추적) 과의 차는 **(고체 분율) × (1 − J)** 다.  SE 의 평균 압력이 목표 300 MPa 라고 놓으면 1 − J ≈ P/K = 0.3/25.5 = 0.012 → 순수 SE 침대 (고체 분율 ≈ 0.9) 에서 **≈ 1.1 %p** · 복합 침대 (SE 가 전체 부피의 ≈ 0.25 · AM 은 굳힌 장애물) 에서 **≈ 0.3 %p**.  누른 채의 값이고 하중을 빼면 사라지는 몫이다 — 실험 기공 (뺀 뒤 잰 것) 과 견줄 때 어느 쪽 식 · 어느 시점인지를 적어야 하는 크기다.
- 이 논문에서 그 차가 0.13–0.36 (ε 0.9) 으로 큰 것은 P/K 가 0.4–0.65 이기 때문이다 — 우리 체제 (P/K ≈ 0.012) 로 옮기면 1 %p 급이다.  **값이 아니라 식을 가져온다.**

### 8-3. 전이되는 것 / 안 되는 것

| | 내용 |
|---|---|
| **전이 (방법)** | ① 기공 연산자 한 쌍 (식 1 · 2) 과 항등식 p − p_inc = (φ/(1 − ε))(1 − J) ② 꽉 찬 블록 ↔ 해석해 단위 시험 꼴 ③ 준정적 설정 (판 속도 ÷ 파속 · 파 통과 횟수) 과 절반 속도 대조 — 단 판정은 수로 ④ 반력 잡음이 재는 넓이에 달린다는 설명 ⑤ FEM 의 어려움 세 가지에 대한 원문 |
| **전이 (경고)** | ⑥ '완전 치밀화' 같은 이름은 정의 (비압축 가정) 를 함께 적는다 ⑦ 매끈하게 만든 선은 어느 런의 것인지 적는다 ⑧ 붙는 접촉의 잔류 기공은 해상도에 달릴 수 있는데 이 논문은 재지 않았다 ⑨ 투영 기공 ≠ 부피 기공 |
| **전이 안 됨** | 남는 기공 0.345 · 0.384 · 고원 응력 · 치밀화 반력 · '두 배 규칙' · Gibson–Ashby 대조 — 탄성 발포체 뼈대 · GPa 급 응력 · 기공 하나짜리 셀의 값이다.  소성 · 마찰 · 탈압 · 다입자 접촉에 대해서는 **아무 값도 없다** |

### 8-4. frame 판정

- **frame [5]**: 이 논문은 MPM 쪽 절반 (큰 변형 · 형상 변화 · 응력장 · 기공의 변화) 만 있고 수송 · 접촉망 · 입자 통계는 없다.  게다가 형상 변화가 **탄성** (굽힘 · 좌굴) 이라 우리 MPM 고유의 소성 흐름과도 다른 기전이다.
- **frame [4]**: 실험에 맞춘 값이 없고 (맞춘 값 0 개) 실험 대조는 정성이다 — 우리 쪽 보정 · 교차검증의 근거로 쓰지 않는다.
- 연화 틀 (frame [2]) 과는 중립 — 물체가 하나라 재배열이 없고 실제 계수를 그대로 썼다.

---

## 9. 깊은 통찰

① **'완전 치밀화' 는 운동학적 이름이다.**  정의는 "비압축이면 기공이 0 이 될 변형률" (ε = 1 − φ) 이고 그때의 실제 기공은 0.345 · 0.384 다.  둘의 차는 항등식으로 뼈대의 부피 변화와 같다.  우리 보고에서 '치밀화 변형률' · '완전 치밀화' 를 쓸 때는 (고체 부피 고정 기준인지 · 추적 기준인지) 를 함께 적는다.

② **남은 기공의 물리 = 갇힌 틈 + 탄성으로 눌린 뼈대.**  ε 0.9 에서 J 0.84 · 0.63 · 반력 3.9 · 6.7 GPa (K 의 0.38 · 0.65 배) [판독 · 카드 산술].  random 은 반력 ÷ 고체 분율 (10.8 GPa) 이 J 0.634 인 일축 변형 응력 (11.0 GPa) 과 맞는다 — 끝 상태는 '틈을 낀 채 통째로 눌린 기둥' 이다.  탄성 재료 + 붙는 접촉에는 틈을 메울 기전이 없다.  저자도 *"details of contact geometry and material properties will strongly influence residual porosity"* 라고 한정한다.  ⇒ 35 % 를 소성 SE 에 옮기지 않는다.  옮길 것은 "접촉 규칙과 재료 법칙이 남는 기공을 정한다" 는 틀이다 — 우리 MPM (붙음 + J2 소성) 에서 남는 기공은 갇힌 틈이 아니라 항복 세기와 압력의 비가 정하고, 얼린 AM 이 하중을 지지 않는 설정에서 목표 응력까지 누르면 ε_sphere 1.13 % 까지 메워진다 (`fam_platen_prereg_20260812.md` §11) [우리 기록].

③ **기공 연산자가 인쇄돼 있지 않고, 인쇄된 곡선이 물리 범위를 넘는다.**  lattice 는 ε 0.18–0.81 에서 뼈대 부피가 최대 11 % 는 것으로 읽히는데, 압축 하중을 받는 평형 계에서 이 구성식으로는 평균 1.2 GPa 의 순 인장이 있어야 가능한 값이다 [카드 산술].  저자는 압축 · 인장 구역의 경쟁으로 설명하지만 평균 응력으로 따지면 성립하지 않는다 — 부피 측도의 수치 오차로 읽힌다 [카드 추론].  ⇒ 단계 0 에 넣을 점검: **추적한 고체 부피의 변화 (1 − J) 는 거시 평균 압력 ÷ (K × 고체 분율) 과 같은 자릿수 · 같은 부호여야 한다.**

④ **조밀 끝에서 기공은 고체 부피 오차에 거의 1 : 1 로 민감하다.**  dp/dJ = −(고체 분율) — 이 논문 ε 0.9 에서 −0.78 · −0.97, 우리 침대 (고체 분율 0.85–0.9) 에서 −0.85 ~ −0.9.  고체 부피 1 % 의 정의 차 = 기공 0.9 %p.  우리가 겪은 관례 오프셋 1.251 %p (구 부피 합 ↔ 합집합) 가 바로 이 부류다 [우리 기록].  기공을 비교할 때는 분자 (고체 부피) 의 정의부터 맞춘다.

⑤ **우리 MPM 의 기공은 식 (2) 꼴이다** (§8-2).  누른 채의 '추적 기공' 은 그보다 순수 SE 에서 ≈ 1 %p 크다 [카드 산술 · 가정].  실험 기공 (하중을 뺀 뒤 · 질량 기준) 과 맞는 쪽은 고체 부피 고정 꼴이지만, 누른 채 잰 값 (두께 변화) 과 견줄 때는 다르다 — 결과 전에 어느 쪽인지 적는다.

⑥ **고체 파속 기준 Mach 0.03 은 구조가 무너지는 구간에서는 '준정적' 이 아니었다.**  절반 속도와 평균 35 % (ε 0.3–0.55) 다르고, 치밀화 초입 (0.55–0.7) 에서는 9 %, 탄성 구간에서는 2 % 다 [판독].  구조 자신의 겉보기 파속으로 보면 판 속도는 0.05–0.12 다.  ⇒ 느슨한 가루 침대의 초기 (접촉망이 막 생기는) 구간은 같은 문제를 가진다 — 판 Mach 를 고체 파속으로만 정하면 그 구간의 반력은 관성을 낀다.  한편 방향은 우리와 **반대**다: 이 논문은 빠를수록 반력이 크고 (충돌), 우리 MPM 은 느릴수록 응력이 크다 (판 Mach 0.03 → 0.01: 같은 침대 · 같은 변형에서 +4.8 % · 다른 침대의 정착 응력 +9.0 % [우리 기록]) — 재하율 효과의 부호는 무엇을 어디서 언제 재는지에 달려 있다 [카드 추론].

⑦ **매끈한 선이 속도 차를 가린다.**  Fig. 4 의 맞춤선은 느린 런 쪽이고, 그 선이 Fig. 6 (random) 과 Fig. 10 ('original' 의 맞춤) 에 그대로 쓰인다 — Fig. 10 에서는 빠른 런의 원자료 위에 느린 런의 맞춤선이 그려져 있다 [판독 · 카드 산술].  '두 배 규칙' 의 중간 변형률 근거 (맞춤선끼리의 배율 ≈ 2) 는 그래서 속도가 섞인 비교다 — 원자료 평균으로는 ×1.8 이다.  우리 쪽 교훈: 반력 곡선을 매끈하게 만들 때 창 · 차수 · 맞춘 런을 산출물에 적는다.

⑧ **'두 배 규칙' 은 관성이 없을 때의 차원 논리다.**  탄성 · 속도 무관 · 붙는 접촉이면 응력의 유일한 척도가 계수이므로 같은 변형 경로에서 응력은 정확히 계수에 비례한다.  치밀화 구간의 ×2.00–2.11 은 그 확인이고, 중간 구간의 ×1.4–2.7 은 경로가 달라졌다는 뜻이다 — stiffened 런은 판의 절대 속도를 그대로 둬 Mach 가 0.030 → 0.021 로 바뀌었다 [판독 · 카드 산술].  저자의 *"as could be predicted based on Hertzian contact mechanics"* 는 그보다 좁은 근거다.

⑨ **검증의 실제 크기.**  해석해 대조 1 건 — 끝에서 5 % 는 판 위치 0.32 셀에 해당하는 민감한 자리의 값이라 나쁘지 않지만, 전 구간 평균이 +5.5–6.6 % 한쪽으로 치우쳐 있고 [판독] 원인은 적혀 있지 않다.  발포체 계산 자체에는 격자 수렴 · 에너지 점검이 없다.  ⇒ 이 논문을 "MPM 이 큰 변형 압축에 검증됐다" 는 근거로 인용할 때는 *"꽉 찬 블록의 일축 변형에서 5 % (Fig. 1)"* 까지만 쓴다.

⑩ **붙는 접촉의 잔류 기공은 해상도에 달릴 수 있다 [카드 추론].**  한 속도장의 접촉은 표면이 실제로 닿기 전 — 두 표면이 같은 격자 노드를 나눠 쓰는 거리 (셀 크기 급) 에서 — 걸린다 (짝 카드 2001 판 §2.1: *"Resolution of the interface is commensurate with the computational grid cell size"*).  strut 지름이 10–14 셀이고 틈이 0.5–1 셀이면 그 틈은 뼈대 부피의 7–21 % 다 ((d + g)²/d² − 1) → ε 0.9 에서 기공 5–20 %p 에 해당하는 크기 [카드 산술 · 가정: 단위 셀 1 mm · 틈 0.5–1 셀].  남은 기공 35–38 % 가운데 얼마가 그 몫인지는 격자 수렴 시험이 없어 알 수 없다.  ⇒ 우리 U6 (조밀 충전 압축의 해상도 수렴) 의 관측량에 **기공 자체**를 넣는다 (반력만 보지 않는다).

⑪ **한 물체의 자기 접촉은 '물체별 속도장' 으로 못 가른다.**  같은 제1 저자가 다물체 마찰 접촉을 이미 갖고 있었는데도 여기서는 no-slip 을 썼다 — 뼈대가 한 물체라 물체 번호로 속도장을 나눌 수 없기 때문으로 읽힌다 [카드 추론].  이 문제를 겨냥한 것이 `homel2017…` 의 장 분할 (표면 표지의 기울기로 노드마다 두 장) 이다.  우리 후보 A′ 에서 SE 입자마다 번호가 있으면 이 제약은 없다 — 번호가 없는 (합쳐진) 상태로 출발하면 이 논문과 같은 처지가 된다.

⑫ **투영으로 본 기공과 부피 기공은 순서가 다를 수 있다.**  밑에서 본 뚫린 넓이는 lattice 가 random 의 2.4 배 (12.5 ↔ 5.1 %) 인데 부피 기공은 random 이 더 크다 (0.384 ↔ 0.345) [판독].  저자는 그 그림으로 lattice 의 *"less efficient packing"* 을 말한다.  단면 · 투영 영상의 기공과 질량 기준 기공을 섞어 순위를 매기지 않는다.

⑬ **반력의 잡음은 재는 넓이의 문제다.**  *"divided by a larger measurement area"* — 충돌 사건의 크기는 같고 넓이가 커지면 평균된다.  우리 RVE 의 판 반력에도 같은 논리가 선다: 침대 넓이가 작을수록 접촉 사건 하나의 몫이 크다.  잡음을 재하율 문제와 넓이 문제로 가르려면 넓이를 바꾼 런이 필요하다 [카드 추론].

---

## 10. [DEM 우선 (수영)] — 후보별 함의 + 구체 행동

| 후보 · 단계 | 이 논문의 함의 | 판정 |
|---|---|---|
| **단계 0** (기공 연산자) | 식 (1) · (2) 한 쌍과 항등식 · 민감도 · 평균 응력 점검 — 그리고 연산자를 적지 않으면 어떻게 되는가의 사례 (J 1.11) | ✅ 직접 쓸 것 |
| **단계 2** (2D MPM · 단위 시험) | 접촉 없는 꽉 찬 블록 ↔ 해석해 · 절반 속도 대조 — 판정을 수로 | ✅ 시험 꼴 |
| **U1 · U6** (해상도) | 규칙 없음 (셀 한 가지 · 수렴 시험 없음).  조밀 끝의 민감도 (응력 5 % = 0.32 셀) 와 '붙는 접촉의 틈' 걱정만 | ⚠ 근거로 못 씀 · 경고만 |
| **단계 4** (순수 SE 압밀) | 준정적 판정 — 구조가 무너지는 구간은 고체 파속 기준 Mach 로 부족 · 반력 잡음과 넓이 | ↗ 설정에 반영 |
| **단계 5** (복합) | 관련 값 없음 | — |
| **단계 6** (탈압) | 없음 | — |
| **후보 A** (AM 강체 + SE 한 속도장) | 한 속도장 (붙는 접촉) 으로 공칭 90 % 까지 수치가 버틴다는 선례.  단 미끄럼 · 분리 없음 · 잔류 기공의 해상도 의존 미확인 | ✅ 수치 견고성 · ⚠ 접촉 한계 |
| **후보 A′** (입자별 속도장) | 저자 스스로 마찰 접촉을 "나중" 으로 미룸 — 자기 접촉에는 물체 번호가 필요 (⑪) | ↗ 필요성의 방증 |
| **후보 B** (입자별 유한요소) | FEM 이 큰 변형 + 자기 접촉에서 어려운 세 가지의 원문 (p.599) — 2005 년 시점의 서술 | ↘ 인용처 (시점 한정) |
| **후보 C · C′ · D0 · M0** | 관련 서술 없음 (저자의 끝 목표는 균질화 구성 모형 — M0 류 — 을 고치는 것) | 중립 |

**구체 행동 (전부 [카드 추론] · 결과 전 등록 대상)**
1. **단계 0 — 기공 연산자를 두 꼴로 적는다**: p_fix = 1 − V_s0/V_bulk (지금 우리 MPM · 식 2 꼴) 과 p_trk = 1 − Σ(물질점 현재 부피)/V_bulk (식 1 꼴).  보고에는 둘과 시점 (누른 채 / 뺀 뒤) 을 함께.  점검 = p_trk − p_fix 가 (고체 분율) × (평균 압력 ÷ K) 와 같은 부호 · 같은 자릿수인가 (⑤ · ③).
2. **단계 2 — 접촉 없는 단위 시험**: 꽉 찬 블록의 일축 변형 압축 ↔ 우리 구성식의 해석해 (탄성 구간 + 항복 뒤) 를 판 Mach 두 단으로 · 오차를 변형률 구간별로 기록 (이 논문은 끝 값만 적었고 구간 평균은 +6 % 치우쳐 있었다).
3. **준정적 판정의 수**: 절반 속도 쌍에서 구간 평균 반력의 비와 차의 rms 를 통과 기준으로 등록 · 판 반력과 바닥 반력의 차 (관성) 를 함께 기록 · 느슨한 초기 구간에는 침대의 겉보기 파속 기준 Mach 를 병기 (⑥).
4. **반력 곡선의 매끈화 규칙**: 창 · 차수 · 맞춘 런을 산출물에 적고 원자료를 같이 둔다 (⑦).
5. **U6 의 관측량에 기공을 넣는다**: 같은 조밀 충전을 dx 세 단으로 눌러 같은 판 반력에서의 기공이 dx 에 따라 움직이는지 본다 (⑩ — 짝 카드 2001 판 행동 5 와 같은 시험).
6. **이름의 정의**: '완전 치밀화' · '치밀화 변형률' 을 쓰는 문서에는 식 (2) 꼴 정의 (고체 부피 고정 · 옆 변형 0) 를 한 줄로.
7. **결과 전 대조 항목으로 쓰지 않는다**: 이 논문의 어떤 값도 (35 % · 고원 응력) 우리 계산의 대조값이 아니다.

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | 탄성 재료 · 붙는 접촉뿐 — 점탄성 · 소성 · 마찰 미끄럼은 나중 | §3 p.601 |
| 2 | 단위 셀이 작다 — 대표 부피 (RVE) 가 아니고 결과는 실제 발포체의 **예비 지표**뿐 (*"give only preliminary indications"*) | §3 p.601 · p.610 · p.614 |
| 3 | 이상화한 형상 — 실제 형상 (비누 거품 모형 · X 선 단층) 은 향후 | p.601–602 · p.615 |
| 4 | 준정적을 명시적 풀이로 흉내 (*"less elegant"*) — 암시적 풀이는 비싸고 연구 중 | p.602 |
| 5 | 반력의 잡음은 작은 셀의 산물 | p.606 |
| 6 | 물질점이 셀 경계를 넘을 때의 오차 (큰 변형률의 튐) | p.603 |
| 7 | lattice 의 snap-through 구간은 불안정하면 관성이 지배 | p.612 |
| 8 | '두 배 규칙' 은 두 사례뿐 · 기공 하나짜리 계산 — *"not conclusive"* · *"advanced tentatively"* | p.612 · p.614 |
| 9 | 높은 상대밀도 (닫힌 셀 · 얇은 막 · 갇힌 기체와 기체 흐름) 는 다루지 않음 | p.604 |
| 10 | 직렬 계산 — 100–1000 기공 규모가 필요 | p.615 |
| 11 | 미세구조 정보를 공학 모형으로 옮기려면 균질화가 한 단계 더 필요 | p.615 |
| 12 | 실험과의 비교는 정성 (*"Macroscopic stress–strain curves agree qualitatively with experimental results"*) | p.599–600 |

---

## 12. 불확실 · PDF 에 없는 것 · 인쇄 어긋남

**A. 논문에 없는 것 ([미확인])** — §3-10 의 목록.  특히 ① 단위 셀의 변 길이 (→ strut 당 셀 수) ② 셀당 물질점 수 · 물질점 수 ③ 시간 간격 · 인공 점성 계수 ④ V_microstructure 의 계산식 ⑤ 접촉 알고리즘과 분리 여부 ⑥ 계산 시간 ⑦ 재료 상수의 출처 ⑧ 저널 호 (issue) 번호.

**B. 카드가 그림에서 역산한 것 (논문의 주장이 아님)** — ① neo-Hookean 저장 에너지의 꼴 (Fig. 1 해석 곡선과 0.1 % 안) ② Gibson–Ashby 선 = 0.05 E_s φ² 꼴 (두 선의 값에서 계수 0.0507 · 0.0504) ③ 다항 맞춤선이 느린 런 쪽이라는 것 (rms 2 ↔ 13 MPa) ④ stiffened 런의 판 속도 (반력이 뜨는 변형률에서) ⑤ J = (1 − p)/(1 − p_inc) 와 그에 딸린 응력 점검.  전부 [판독 + 카드 산술] 이고 원자료로 확인한 것이 아니다.

**C. 인쇄 어긋남 · 읽을 때 걸리는 곳**
1. 상대밀도 인쇄값 7.9 · 9.6 % ↔ Fig. 8 곡선의 출발점 7.82 · 9.71 % [판독] — 0.1 %p 차 (형상 정의값과 이산화 뒤 값의 차로 보이나 설명 없음).
2. Fig. 6 범례 *"G&A … plateau stress"* ↔ 캡션 · 본문 *"yield stress"* — 같은 선.
3. Fig. 6 의 두 선은 속도가 다른 런의 맞춤이고 (random = 느린 런 쪽 · lattice = 빠른 런), Fig. 10 의 'original' 실선과 그 'polynomial fit' 도 서로 다른 런이다 [판독 · 카드 산술] — 본문은 맞춤에 쓴 자료를 적지 않는다.
4. 본문 *"about 35% porosity"* 는 두 셀의 값 (0.345 · 0.384) 을 뭉뚱그린 것이고, lattice 는 계산이 자기 '완전 치밀화' 변형률 (0.921) 에 못 미쳐 비압축 추정으로도 0.218 이 남는 지점이다 [판독 · 카드 산술].
5. 본문 *"the maximum tractions registered for the foams are approximately two orders of magnitude lower"* ↔ 1/43 · 1/70 [카드 산술].
6. lattice 의 기공이 비압축 추정 아래로 가는 구간에 대한 저자 설명 (압축 · 인장의 경쟁) 은 평균 응력으로 따지면 성립하기 어렵다 (§3-6) [카드 추론].
7. 본문은 lattice 의 큰 구멍 (Fig. 7 맨 아래) 을 *"less efficient packing"* 의 표시로 읽지만 Fig. 8 의 부피 기공은 lattice 가 더 작다 (ε 0.9) [판독].
8. Fig. 4 의 x 축 이름 *Engineering Strain* 은 원본 PDF 에서 g 의 아래 끝이 잘려 있다 (그림을 넣을 때의 잘림 — 크롭 문제 아님).
9. p.608 의 σ_eq 식은 근호 윗줄이 윗줄 글자와 닿아 인쇄돼 있다 (조판).
10. 오탈자: *"establish a convincing capability perform these simulations"* (to 빠짐 · p.601) · *"reset to it's original configuration"* (p.601) · *"it's bulk behavior"* (p.609) · *"An qualitative indication"* (p.612) · 참고문헌 *"Wang, Y., Cuitiño, Y., 2000"* (본문 인용은 Wang and Cuitiño · 같은 목록의 Gioia, Wang, Cuitiño, A.M. 과 머리글자가 다름).

**D. 정본의 다른 카드와의 어긋남**
- `devaucorbeil2020_mpm_after_25_years_review` 카드 56–59 · 76 행은 이 논문을 *image-based (voxel → 입자) 치밀화 · multi-contact* 의 선례로 적고 *"우리 scaffold 접근의 직접 선례"* 라고 한다.  **이 논문의 계산은 손으로 만든 이상화 단위 셀 둘 · 붙는 (no-slip) 접촉**이고, 영상 기반 이산화는 전망으로만 적혀 있다 (*"for a particle method, an array of pixel intensities representing an image can be easily discretized"* p.602 · *"provides a data format which should be easily discretized via particle methods"* p.615).  리뷰 원문이 어떤 논문을 가리켰는지는 이 PDF 로 확인할 수 없다 [미확인] — 그 카드에 같은 날짜의 정오 줄을 붙였다.

---

## 13. 인용 가능 문장 (덱 · 원고용)

- "발포체 미세구조의 큰 변형 · 자기 접촉 계산은 격자 뒤틀림과 접촉면의 사전 지정 문제 때문에 유한요소법으로는 작은 변형 구간에 머물렀고, 입자 기법 (GIMP) 으로 처음 치밀화 구간까지 계산됐다 (Bardenhagen, Brydon, Guilkey, J. Mech. Phys. Solids 53, 597, 2005 · §1)." — 재료가 발포체 (탄성) 라는 한정을 붙인다.
- "그 계산에서 기공은 p = (V_bulk − V_microstructure)/V_bulk 로 뽑았고, 비압축이면 기공이 없어질 변형률에서도 약 35 % 가 남았다 (같은 문헌 식 1 · Fig. 8)." — 탄성 뼈대 · 붙는 접촉 · 기공 하나짜리 단위 셀 · 반력 GPa 급이라는 한정 없이는 쓰지 않는다.
- "명시적 입자 기법의 준정적 근사로 판 속도를 종파속의 3 % 로 두고 절반 속도 런과 견줬다 (같은 문헌 §3.1–3.2 · Fig. 4)." — 판정이 눈 대조였고 카드 판독으로는 구간 평균 2–35 % 차라는 것을 함께.
- "명시적 GIMP 는 꽉 찬 블록의 일축 변형 압축에서 90 % 변형률까지 해석해와 약 5 % 안에서 맞았다 (같은 문헌 Fig. 1)." — 검증의 범위는 여기까지다.

## 14. 기법 미니 용어집

- **GIMP (generalized interpolation material point)** — 물질점에 크기 (영역) 를 주어 격자 보간 함수를 일반화한 MPM 계열 기법.  MPM 은 그 특수한 경우 (이 논문의 서술).
- **contiguous-particle GIMP** — 물질점 영역이 변형을 따라 서로 이어지도록 갱신하는 변종 (이 논문은 이름만 적고 세부는 Bardenhagen and Kober 2004 로 넘긴다).
- **PIC** — particle-in-cell.  입자가 물질을, 격자가 풀이를 맡는 기법의 원형 (유체).
- **no-slip contact** — 닿은 면이 서로 미끄러지지 않는 접촉.
- **자기 접촉 (self contact)** — 한 물체의 서로 다른 부분이 접히며 닿는 것.
- **상대밀도 φ** — 발포체 밀도 ÷ 뼈대 재료 밀도 (= 1 − 처음 기공률).
- **고원 (stress plateau)** — 거의 일정한 힘에서 큰 변위가 나는 붕괴 구간.
- **치밀화 (densification)** — 뼈대가 스스로에게 접혀 닿으며 급격히 굳는 구간.  **완전 치밀화** = 비압축이면 기공이 0 이 될 변형률 (이 논문의 쓰임).
- **snap-through** — 좌굴 뒤의 해가 불안정할 때 하중이 떨어지며 다른 배치로 넘어가는 것.
- **일축 변형 (uniaxial strain)** — 한 방향으로만 줄고 옆으로는 변형이 없는 압축 (옆이 막힌 압축).
- **공칭 (engineering) 변형률** — 길이 변화 ÷ 처음 길이.
- **등가 응력 σ_eq** — 편차 응력의 노름 × √1.5 (von Mises).
- **인공 점성** — 파면의 수치 울림을 죽이려고 넣는 수치 감쇠.
- **RVE** — 대표 부피 요소.  평균 응답이 크기에 안 달라지는 최소 크기.

## 15. 관련 카드

- `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 이 논문이 서론에서 인용한 MPM 접촉 (물체별 속도장 · 마찰 · 견인력 분리).  이 논문의 계산에는 쓰이지 않았다.  2001 판의 재료값 (G 72 · K 102 GPa · ρ 1900) 의 1/10 이 이 논문의 값이다.
- `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — 한 물체의 자기 접촉을 속도장 분할로 (이 논문이 no-slip 으로 넘긴 문제).
- `gritton2017_mpm_chemomechanical_coupling_silicon_anode` — 이 논문을 ref. [31] 로 인용 · 같은 대학의 MPM 코드 · 명시적 MPM 의 준정적 장치 (밀도 증가) 를 형상의 눈 대조로 판정한 다른 사례.
- `devaucorbeil2020_mpm_after_25_years_review` — 리뷰 (§12 D 의 정오).
- `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` — MPM 으로 변형 입자의 압밀 (소성 포함 · 2D · 입자별 격자 + 접촉) — 이 논문에 없는 다입자 · 소성.
- `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MLS-MPM 이산화의 원전.
- `stomakhin2013_mpm_snow_elastoplastic` — 우리 탄소성 MPM 의 계보.
- `demirtas2021_mpfem_hollow_sphere_die_compaction` · `pycompact2025_dem_mpfem_workflow` — 입자별 유한요소 (후보 B) 로 큰 변형 압밀을 한 쪽 — 이 논문의 "FEM 은 작은 변형에 머문다" (2005) 와 나란히 읽을 것.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

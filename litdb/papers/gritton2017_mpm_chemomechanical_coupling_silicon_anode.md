# MPM 에 확산을 얹은 화학–역학 양방향 결합 — 입자에 실은 농도 · 응력 의존 확산계수 · 리튬화 자유 변형률을 변형률 속도에 더하는 hypoelastic–plastic + 밀도를 올려 준정적으로 (질량 스케일링) · 3D 규소 나노기둥의 리튬화 → 탈리튬화 한 바퀴 ★★ 접촉 없음 (한 속도장 = 붙음) · 정량 검증은 1D 확산뿐 — Gritton, Guilkey 외 4 인 (Modelling Simul. Mater. Sci. Eng. 2017)

> slug `gritton2017_mpm_chemomechanical_coupling_silicon_anode` · DOI `10.1088/1361-651X/aa6830` · type `MPM (명시적 CPDI-MPM · Uintah — 입자에 실은 정규화 농도의 확산 풀이 + 응력 의존 확산계수 (경험식) + 농도 의존 자유 변형률 (hypoelastic–plastic · 변형률 속도 덧셈 분해 · J2 완전 소성 / 선형 등방 경화) · 3D 규소 나노기둥 리튬화 / 탈리튬화 · 밀도 인위 증가 (질량 스케일링) · 물체 사이 접촉 알고리즘 없음 · 정량 검증 = 1D 확산 해석해 1 건)` · PDF `a02dabec-18._Using_the_material_point_method_to_model_chemicalmechanical_coupling_in_the_deformation_of_a_silicon_anode.pdf` (23 쪽 = 출판사 표지 1 쪽 + 논문 22 쪽 · 글자 층 온전 · 보충 자료 없음) · digested `2026-11-11` · status ✅
>
> ⚠ **먼저 읽을 것** — ① 재료는 **비정질 규소 (a-Si) 음극 나노기둥** + 이름 없는 기판이다 — **LPSCl · NCM 이 아니다.  절대값 전이 0 건** (물성 · 확산계수 · 부피 팽창 280 % · 유속은 전부 규소 전용이고, 물성값에는 출처도 인쇄돼 있지 않다 — 저자 표현 *"reasonable values"*).  가져오는 것은 **방법** (MPM 에 장 하나를 더 얹는 법 · 자유 변형률을 넣는 법 · 질량 스케일링과 그 점검 꼴) 과 **저자가 스스로 적은 한계**뿐이다.
> ② **가압 · 압밀 · 기공 · 분말이 없다.**  하중은 리튬이 들어오며 생기는 자체 팽창 (자유 변형률) 이고, "탈리튬화" 가 하중을 빼는 쪽에 해당한다.  물체는 기둥 하나 (+ 기판) — 입자 층이 아니다.
> ③ **물체 사이 접촉 알고리즘이 없다.**  본문 · 참고문헌 전체에 'contact' 가 0 회, 'friction' 은 참고문헌 [43] 의 제목 (*friction stir forming*) 한 번뿐이다 [카드 전문 검색].  기둥은 기판에 *affixed* — 한 속도장으로 붙어 있다.  'DEM' · 'discrete element' 도 0 회다.
> ④ **정량 검증은 1D 순수 확산의 해석해 대조 하나** (Fig. 1) 다.  결합 문제 · 역학 · 3D 격자 수렴 · 실험 · FEM 과의 정량 대조는 없다.  초록의 *"validation tests with experimental results show the accuracy of the approach"* 에 해당하는 본문은 Wang 외 [5] 의 관찰과 견준 정성 문장 (날카로운 전선 · 전선 뒤 농도 ~0.67 ↔ 계산 0.5–0.6 / > 0.7) 뿐이다.
> ⑤ 3D 본 계산의 **격자 간격 · 셀당 입자 수 · 입자 수 · 쓴 밀도 · 물리 시간 · 유속의 단위**가 인쇄돼 있지 않다 (§3-7) — 이 논문만으로는 재현할 수 없다.
> ⑥ 인쇄 어긋남이 여럿 있다 (식 13 의 지수에 t 없음 · 식 15 의 노름 · 식 18 의 번호 칸 · 식 46 의 값 · Fig. 3 · 4 캡션) — §12 에 모았다.  식 그림은 **인쇄된 그대로** 잘랐다.
> ⑦ 표지: `인쇄` = 본문 · 캡션에 적힌 값 · `[판독]` = 그림에서 읽은 값 (추세 전용 — 윤곽 · 화소 계수 · 도구는 scratchpad `gritton_work/`) · `[카드 산술]` = 인쇄값에서 산술로만 유도 (식 병기) · `[미확인]` = 논문에 없음 · `[카드 판독]` = 인쇄 어긋남 · 모호한 곳에 대한 카드의 읽기 · `[카드 추론]` · `[우리 코드 판독]` · `[우리 기록]` = 논문 밖 판단.
>
> 짝 카드: `devaucorbeil2020_mpm_after_25_years_review` — 이 논문을 *Si anode chemo-mechanical MPM (배터리 인접)* 으로 한 줄 소개한 리뷰 카드 (그 카드가 가리키던 원전이 이 카드다).  `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — 이 논문에 **없는** 것 (MPM 다물체 마찰 접촉 · 분리) 의 원전.  `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MPM 이산화 (MLS-MPM) 의 원전.  `bucci2017_chemomech_failure_assb_cycling_czm` · `tian2020_electrochemo_mechanical_stress_assb` — 화학–역학 결합을 FEM 으로 푼 쪽 (전고체 전지 · 이 논문과 재료 · 문제는 다르다).

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

[DEM 우선 (수영)] 은 *"가압부터 탈압까지 한 모델 (MPM) 이 다 계산할 수 있는가"* 를 묻는다.  이 논문은 가압 논문이 아니다 — 그런데도 읽을 까닭이 넷 있다.

**(1) 명시적 MPM 으로 느린 (준정적) 과정을 풀 때의 시간 척도 문제와 그 우회를 식 · 시험과 함께 적었다.**  탄성파가 정하는 시간 간격 (10⁻¹¹–10⁻¹² s) 과 확산이 정하는 시간 간격 (10⁻² s) 이 10 자리쯤 벌어지므로 밀도를 인위로 올린다.

> *"In order to increase the limiting time step size needed for the numerical solution to the momentum balance equation, the density of silicon is artificially raised to a value such that the limiting time step criteria is dependent upon the numerical solution of the diffusion equation and not the solution to the momentum balance equation.  The argument for the validity of artificially raising the density stems from the observations made in section 4.1 that within the time scale of chemical diffusion the momentum balance equation reaches a quasi-static state."* (§4.2.1 · p.12)

> *"An increase in density decreases the speed by which elastic waves travel through the material, but the elastic strain remains the same."* (식 49 아래 · p.13)

우리 MPM (`scripts/mpm3d_compaction.py`) 도 같은 부류의 장치로 돈다 — 밀도를 1 로 두는 규약 (`pm = pvol_p[p]  # per-point vol = mass (ρ=1)`) 위에서 시간 간격은 `0.4 * dx / (_M ** 0.5)` 이고, 준정적 여부는 판 속도 ÷ 파속 (`--platen-mach`) 으로 정한다 [우리 코드 판독 · 2962 · 1928 · 3076–3077 행 · 파일 마지막 커밋 `cb5a6a445`].  이 논문은 그 장치의 **제3자 선례**이고, 동시에 **판정을 눈으로만 한 사례**다 (Fig. 3 · 4: *"qualitatively the variations between the simulations are small"*).

**(2) 접촉 알고리즘 없는 MPM (한 속도장) 으로 '넣었다 빼는' 한 바퀴를 끝까지 돌린 그림이 있다 (Fig. 10).**  계면은 끝까지 붙어 있고, 저자는 그 가정의 한계를 스스로 적는다.

> *"Wang et al [5] have shown through experiments that the base of the electrode can expand in the radial direction by ∼20%.  It is unknown if the deformation comes as a result of the sliding between the anode and the substrate material or deformation in the substrate.  …  For the purposes of this paper the pillar is assumed to be affixed to the substrate and the substrate material is allowed to deform."* (§4.6 · p.17)

미끄럼인지 기판 변형인지 모르는데 계산은 뒤쪽만 시험할 수 있다 — 우리 MPM 의 SE–AM · SE–판 계면이 같은 상태다 (격자 속도장 `grid_v` 한 벌 [우리 코드 판독 · 2808 행]).

**(3) 자유 변형률 (eigenstrain) 과 두 번째 장 (확산) 을 MPM 에 얹는 식 일습이 있다** — 식 (4)–(8) · (16)–(18) · (25)–(39).  가압 · 탈압 흐름 밖이지만, 충방전에 따른 AM 부피 변화나 변형과 함께 푸는 수송을 MPM 에 넣는다면 이 논문이 출발점이다.

**(4) 무엇이 검증이 아닌지를 보여 준다.**  MPM 을 고른 근거는 한 문장이고 —

> *"MPM is chosen as the numerical method of choice because of its ability to handle large deformations."* (초록 · p.1)

— 그 '큰 변형' 계산의 정확도를 받치는 시험은 논문에 없다 (1D 확산뿐).

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| 명시적 MPM 의 준정적 판정 (판 Mach · ρ = 1 규약) 에 대한 제3자 근거 | 식 (40)–(49) + 밀도가 10⁵ 배 · 10⁶ 배 다른 두 쌍의 시험 (Fig. 3 · 4).  판정은 눈 대조 · 윤곽 판독으로는 높이 차 ≤ 1 % [판독] · **응력 비교 없음** |
| 큰 변형에서 어떤 MPM 변종을 쓰는가 | CPDI (ref. [38]) — 높이가 ×3.4 [판독] 까지 늘어나는 계산.  다른 변종과의 비교 · 수치 파괴 여부의 점검은 없다 |
| 하중을 넣었다 뺀 뒤 (단계 6) 한 속도장이 내는 것 | Fig. 10: 부피는 거의 돌아오고 (≈ ×1.1) 모양은 안 돌아온다 (높이 ×1.35) [판독] · 계면은 끝까지 붙어 있고 기판에 턱이 남는다 |
| 판 · 벽 · AM 자리의 미끄럼 · 분리 (후보 A′-0) 가 없을 때의 한계 | 저자 문장 *"It is unknown if … sliding … or deformation in the substrate"* — 붙은 계면으로는 둘을 가를 수 없다 |
| 자유 변형률 · 추가 장을 MPM 에 얹는 식 | 확산 5 단계 (식 4–8) · 표면 유속 (식 16–18) · hypoelastic–plastic + d^c (식 25–39) |
| 소성 SE 의 준정적 압밀 · 기공 · 다입자 접촉 · 탈압 곡선 · 실험 정량 대조 | **없음** |

### 0-2. 이 묶음의 네 질문 (DEM 한계 · 소성 · 2D/3D · 탈압)

| 질문 | 이 논문의 답 (원문 위치) |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | **말 없음.**  DEM 을 쓰지도 언급하지도 않는다 ('DEM' · 'discrete element' 0 회 · 참고문헌 52 건에도 없음 [카드 전문 검색]).  다른 방법에 대한 말은 한 문단뿐이고 한계가 아니라 성공을 적는다: *"A variety of numerical methods have been used to model large deformations.  Mesh based methdods such as FEM [27] and XFEM [28] have found success along with meshless methods such as SPH [29] and RPKM [30].  An alternative to these approaches that has been found to be successful in modeling large deformations is the material point method (MPM) [31]."* (§1 · p.3) |
| (ii) 입자의 소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용 | 어려움으로 든 것은 둘이다.  ① 결합 자체: *"The main challenges in modeling this process using the MPM is to simulate stress dependent diffusion coupled with concentration dependent stress within a material that undergoes large deformations."* (초록).  ② **시간 척도**: 명시 풀이의 탄성파 시간 간격으로는 *"10¹¹ time step integrations would be needed to reach 6.8 s of simulation time.  The number of time steps for this calculation would be intractable."* (§4.2.1 · p.12).  우회 = **밀도 인위 증가** (시험한 두 쌍은 10⁵ 배 · 10⁶ 배 차 · 2.33 × 10²⁴ kg m⁻³ 까지).  소성은 *history dependent* 라 하중 속도 (유속) 에 따라 끝 모양이 달라진다고만 적는다 (§4.4 · p.15).  **맞춘 값**: 실험에 정량으로 맞춘 값은 없다 — 손잡이 α · β · p_max · 유속 크기 · η 를 정하고 눈으로 견줬다 (*"tuning parameters"* · p.9 · p.16).  **검증**: 1D 확산 해석해 (Fig. 1) 뿐.  **비용**: 큰 기둥 + 기판 한 바퀴에 9 코어 · 27,472 걸음 · 48.57 h (§4.7 · p.19) · 입자 수 [미확인] |
| (iii) 2D 인가 3D 인가 · 2D → 3D 전이 | **3D** — *"while the pillar geometry lends itself to a 2D axisymmetric numerical solution for the purposes of this paper full 3D simulations will be performed"* (§4 · p.11).  왜 3D 를 택했는지 · 축대칭 해와의 대조는 없다.  차원을 줄이는 것에 대한 말은 서론 한 곳: *"While the reduction of dimensionality can lead to insights into the lithiation/delithation process without the higher computational costs of higher dimensional simulations, key features associated with anode geometries will be lost."* (§1 · p.3 — 구 대칭 1D 모형 [22, 23] 을 두고).  검증 (Fig. 1) 은 1D.  2D 결과를 3D 로 옮기는 문제는 다루지 않는다 |
| (iv) 압력을 뺄 때의 거동 | **압력 하중이 없다** ('unload' 0 회).  대응하는 것은 **탈리튬화** (자유 변형률을 되돌림 · §4.7 · Fig. 10): *"A comparison of the first and last images of the sequence found in figure 10 shows the amount of plastic deformation that occurs in both the nanopillar and the substrate during one full lithiation/delithaition cycle."* (p.19) — 잔류 변형의 **값은 없다**.  [판독] 끝 상태는 처음 대비 높이 ×1.35 · 최대 폭 ×0.98 · 회전체 부피 ≈ ×1.1.  되돌아오는 탄성량 · 응력 · 계면 열림은 다루지 않는다 (계면은 붙음) |

---

## 1. 한 줄 요약

**KR:** 규소 음극의 리튬화 / 탈리튬화 (부피 변화 ~280 %) 를 CPDI 변종 MPM (Uintah) 으로 푼다.  리튬의 정규화 농도 c 를 물질점에 싣고 (이류는 입자 이동으로 자동), 확산은 운동량 풀이와 같은 연산 다섯 단계 — 질량 · 농도를 격자로, 격자 농도의 기울기로 입자 유속, 유속의 발산으로 격자 변화율, 그 변화율을 입자로 — 로 푼다 (식 4–8; 1D 해석해와 견줘 O(h) 로 보고).  표면 유속은 처음 표시한 표면 입자의 농도 변화율로 걸고 (식 16–18), 응력 → 확산의 결합은 압축 압력에서 확산계수를 낮추는 경험식 하나 D = D₀ e^(αc − βp) (식 23) 로, 농도 → 응력의 결합은 변형률 속도의 덧셈 분해 d = d^e + d^p + d^c, d̄^c = η (∂c/∂t) I (η = 0.56) 를 넣은 hypoelastic–plastic 모형 (회전 전 자리에서 갱신 · J2 완전 소성 또는 선형 등방 경화 · K 67 · G 31 · σ_Y 1.4 GPa) 으로 한다.  탄성파 시간 간격이 확산 시간 간격보다 10 자리쯤 작아 **밀도를 인위로 올리고** (준정적 평형 근거 · 밀도가 10⁵ 배 · 10⁶ 배 다른 두 쌍의 해가 눈으로 거의 같음), 지름 0.1 µm 기둥으로 구성식 · 유속 · 확산 손잡이의 영향을, 지름 0.5 µm 기둥으로 변형하는 기판의 영향과 리튬화 → 탈리튬화 한 바퀴 (9 코어 · 27,472 걸음 · 48.57 h) 를 보인다.  물체 사이 접촉 알고리즘은 없고 (기둥은 기판에 붙음), 실험과는 정성으로만 견주며, 파괴와 전기화학은 향후 과제다.

**EN:** Gritton et al. add a diffusion solver to the CPDI material point method in the Uintah framework to model lithiation/delithiation of amorphous-silicon nanopillars.  The normalized lithium concentration is carried by the material points; diffusion is solved with the same particle–grid operations as the momentum balance (mass-weighted P2G of concentration, flux at the particles from the gradient of the grid concentration, divergence of the flux on the grid, explicit particle update — reported first-order accurate against a 1-D analytical solution).  A time-varying surface flux is applied through initially tagged surface particles with an ad hoc saturation factor.  Stress acts on diffusion only through an empirical concentration- and pressure-dependent diffusivity D₀e^(αc−βp) (capped at p_max), while concentration acts on stress through an isotropic stress-free strain rate η(∂c/∂t)I added to the elastic and plastic parts of the rate of strain in an unrotated hypoelastic–plastic (J2, perfect or linearly hardening) update.  Because the acoustic time step is about ten orders of magnitude smaller than the diffusive one, the density is raised artificially (justified by quasi-static equilibrium and by two pairs of runs whose densities differ by 10⁵ and 10⁶ (both called "five orders" in the text) and look alike).  Full 3-D runs show the influence of the constitutive model, flux magnitude, pressure sensitivity of the diffusivity and a deformable substrate, and one full lithiation–delithiation cycle (27 472 steps, 48.57 h on 9 cores).  There is no contact algorithm (the pillar is affixed to the substrate), no quantitative comparison with experiment or FEM, no grid-convergence study of the 3-D problem; fracture and the electrochemistry are left to future work.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **Using the material point method to model chemical/mechanical coupling in the deformation of a silicon anode** |
| 저자 | **Chris Gritton** (1, 4 — 교신) · **James Guilkey** (2) · **Justin Hooper** (3) · **Dmitry Bedrov** (3) · **Robert M Kirby** (1) · **Martin Berzins** (1) |
| 소속 | (1) Scientific Computing and Imaging Institute, University of Utah, United States of America · (2) Department of Mechanical Engineering, University of Utah · (3) Department of Materials Science and Engineering, University of Utah |
| 교신 | 각주 4 *"Author to whom any correspondence should be addressed."* = Chris Gritton · E-mail cgritton@sci.utah.edu |
| 저널 | **Modelling and Simulation in Materials Science and Engineering 25 (2017) 045005 (22pp)** · IOP Publishing · © 2017 IOP Publishing Ltd · 0965-0393/17/045005+22 |
| DOI | **10.1088/1361-651X/aa6830** (PDF 2 쪽 머리에 `https://doi.org/10.1088/1361-651X/aa6830` 인쇄 — 1저자 메모와 같음) |
| 접수 · 게재 | Received 26 October 2016, revised 6 March 2017 · Accepted for publication 21 March 2017 · Published 12 April 2017 |
| 키워드 (인쇄) | material point method, MPM, silicon anode, lithium ion batteries, large deformations |
| 분량 | 논문 22 쪽 (PDF 는 출판사 표지 1 쪽이 앞에 붙어 23 쪽 — **PDF 쪽 = 논문 쪽 + 1**) · Fig. 1–10 · 번호 식 (1)–(49) · **표 없음** · 참고문헌 52 건 · 보충 자료 없음 |
| 절 구성 | 1 Introduction (p.2–3) · 2 The MPM (p.3–7: 2.1 Modeling diffusion in MPM · 2.2 Verification of MPM diffusion · 2.3 Advected flux boundary conditions) · 3 Chemical/mechanical coupling in MPM (p.7–11: 3.1 Coupling stress to diffusion · 3.2 Coupling concentration to stress · 3.3 Perfect plasticity and linear strain hardening · 3.4 Stress update) · 4 Numerical solution of the model problem (p.11–19: 4.1 Time scales of governing equations · 4.2 Time integration and time step selection · 4.2.1 Time stepping issues · 4.3 Comparison of constitutive models · 4.4 Affects of flux boundary conditions · 4.5 Diffusivity · 4.6 Use of material substrate · 4.7 The full lithiation and delithiation cycle of the silicon anode) · 5 Conclusion (p.19–20) |
| 연구 유형 | 수치 방법 (MPM 위의 확산 풀이 + 화학–역학 결합) + 3D 시연 계산.  실험 없음 (남의 실험 [5] 관찰과 정성 비교) |
| 구현 기반 | **Uintah** computational framework 의 MPM component (ref. [39] · 사용자 안내서 [40]) · **CPDI** 변종 (ref. [38] Sadeghirad · Brannon · Burghardt 2011) · MPM 알고리즘은 ref. [34, 38] 대로 · 완전 소성 · 선형 등방 경화 모형은 Uintah 에 구현돼 있던 것 (p.10) |
| 자금 | Army Research Laboratory — Cooperative Agreement Number **W911NF-12-2-0023** |
| PDF 상태 | 조판 PDF · 글자 층 온전 (식은 글자 층에서 흩어져 나오므로 렌더 그림으로 옮김) · 그림 10 장은 500 dpi 내장 JPEG (계산 화면 갈무리) · 표지 쪽의 *"You may also like"* 세 편은 출판사가 붙인 다른 논문 |

**자기 위치 (저자 원문 · §1 · p.3)**
> *"MPM along with the multiple variants of the method are well described in the literature [32–37].  For the the purpose of this paper the convected particle domain interpolation (CPDI) variant, as described by Sadeghirad and Brannon [38], will be used.  The MPM algorithm as described in [34, 38] has been implemented in the Uintah compuational framework [39], and serves as the code base for this work.  …  The primary contribution of this paper is the chemical-mechanical coupling, including the concentration diffusion solver working in concert with the momentum balance solver."*

---

## 3. 핵심 수치

> **라벨 규약** · `인쇄` = 본문 · 캡션 · `[카드 산술]` = 인쇄값의 산술 (식 병기) · `[판독]` = 그림에서 읽음 (내장 래스터의 화소 계수 · 윤곽 · 추세 전용) · `[미확인]` = 논문에 없음.  ⚠ 아래 재료값은 전부 규소 음극 (과 이름 없는 기판) 의 값이다 — **우리 재료 값으로 쓰지 않는다.**

### 3-1. 재료 · 모형 값

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 비정질 규소 밀도 | **2.33 × 10³ kg m⁻³** | 인쇄 · §4.1 p.11 (*"reasonable values"* — 출처 미인쇄) |
| 체적계수 K · 전단계수 G | **67 GPa · 31 GPa** (농도와 무관하게 고정) | 인쇄 · p.11 · 13 · 14 · 15 · 16 · 19 (출처 미인쇄) |
| ⇒ 영률 · Poisson 비 | E = 80.6 GPa · ν = 0.300 | [카드 산술: E = 9KG/(3K + G) · ν = (3K − 2G)/(2(3K + G))] |
| 종파속 c_s | **6.8 × 10³ m s⁻¹** | 인쇄 · p.11 (✓ √((67 + 4·31/3) × 10⁹ / 2330) = 6.82 × 10³ [카드 산술]) |
| ⇒ 전단파속 | 3.65 × 10³ m s⁻¹ (c_s 의 1/1.87) | [카드 산술: √(G/ρ)] |
| 항복 응력 σ_Y | **1.4 GPa** (완전 소성 · 선형 경화 공통) | 인쇄 · p.13–16 · 19 (출처 미인쇄) |
| 소성 계수 (선형 등방 경화) | **1.15 GPa** | 인쇄 · 같은 곳 |
| ⇒ E/σ_Y | ≈ 58 | [카드 산술: 80.6/1.4] |
| 부피 팽창 계수 η | **0.56** (모든 계산) | 인쇄 · §4.3 p.14 (출처 미인쇄) |
| ⇒ (1 + η)³ | 3.80 = +280 % | [카드 산술] — 서론의 *"large volume change of up to ∼280% [5]"* 와 같은 값 |
| 포화 조성 | c_max = Li 3.75 : Si 1 | 인쇄 · §2.1 p.4 |
| 확산계수 손잡이 | **D₀ = 10⁻¹⁷ m² s⁻¹ · α = 6.0 · β = 0.5 · p_max = 3 GPa** | 인쇄 · p.9 · 15 · 19 (β 단위 미인쇄) |
| ⇒ 식 (23) 의 범위 | p ≤ 0: 1.0 × 10⁻¹⁷ → 4.0 × 10⁻¹⁵ · p = 3 GPa: 2.2 × 10⁻¹⁸ → 9.0 × 10⁻¹⁶ m² s⁻¹ (c 0 → 1) | [카드 산술: e⁶ = 403 · e^(−1.5) = 0.223] — Fig. 2a 의 두 선과 일치 (β 를 GPa⁻¹ 로 읽을 때) |
| 견줌용 삼차식 (식 24) | D_max = 10⁻¹⁵ m² s⁻¹ · 최솟값 8.3 × 10⁻¹⁸ (c ≈ 0.09) | 인쇄 p.9 · 최솟값은 [카드 산술] |
| 문헌 범위 (DFT) | 10⁻¹⁸–10⁻¹⁴ m² s⁻¹ (ref. [52]) | 인쇄 · §4.5 p.16 |
| β 민감도 | β = 0.0 ↔ 1.0 (α = 6.0 고정) | 인쇄 · §4.5 p.16 |
| 표면 유속 크기 | **10⁻⁹ · 10⁻⁸** (단위 미인쇄) | 인쇄 · §4.4 p.15 · §4.5 p.16 |
| 유속 제한 계수 | 1 + 0.25 log(1 − c_p) | 인쇄 · 식 (17) — 0 이 되는 농도: 자연로그면 0.982 · 상용로그면 0.9999 [카드 산술 · 밑 미인쇄] |
| 기판 | K **180.4** · G **76 GPa** · σ_Y **0.7 GPa** · 소성 계수 **1.15 GPa** · 밀도 = 기둥과 같음 · 리튬 확산 없음 | 인쇄 · §4.6 p.17 · §4.7 p.19 (재료 이름 [미확인]) |
| ⇒ 기판 E · ν | 199.9 GPa · 0.315 | [카드 산술] |
| 남의 실험에서 소환한 값 | 부피 변화 ~280 % · 전선 부근 변형률 160 % · 전선의 정규화 농도 ≈ 67 % (Li 2.5 : Si 1) · 바닥 반경 팽창 ~20 % (전부 Wang 외 [5]) · 이론 용량 3500–4200 ↔ 흑연 350 mAh g⁻¹ ([1–3]) | 인쇄 · p.2 · 15 · 17 — **이 논문의 측정이 아니다** |

### 3-2. 기하 · 이산화 · 시간

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 차원 | **3D** (*"full 3D simulations"*) · 검증 문제만 1D | 인쇄 · §4 p.11 · §2.2 |
| 작은 기둥 | 지름 **0.1 µm** · 높이 **0.1 µm** — 구성식 · 손잡이 · 경계조건 탐색용 | 인쇄 · p.11 (Fig. 3–8 이 이 기둥이라는 것은 [카드 판독 — 윤곽의 폭 ≈ 높이 · 그림마다 명시는 없음]) |
| 큰 기둥 | 지름 **0.5 µm** · 높이 **0.05 µm** — 기판 (Fig. 9) · 한 바퀴 (Fig. 10) | 인쇄 · p.11 · 19 |
| 기판의 크기 | [미확인] | — |
| MPM 변종 · 코드 | CPDI · Uintah MPM component | 인쇄 · p.3 · 10 · 20 |
| 격자 기저 함수 | CPDI 의 가중 함수 (ref. [38] 로 넘김) — 식으로는 φ_ip 한 기호 | 인쇄 · p.4 |
| 시간 적분 | 매 걸음 dt = min(dt_mb, dt_diff) 를 다시 계산해 앞으로 전진 (식 8 · 38 · 43–45) — 'explicit' 이라는 낱말은 본문에 없다 | [카드 판독 — 안정 조건 식과 갱신 식의 꼴로 양해 풀이] |
| 셀당 입자 수 | 1D 검증: **2** (*"two particle per cell"*) · 3D: [미확인] | 인쇄 · p.5 |
| 격자 간격 | 1D 검증: 0.1 · 0.05 · 0.02 · 0.01 · 0.005 · 0.002 · 0.001 (영역 0 ≤ x ≤ 1) · 3D: [미확인] — 시간 간격 예시에 쓴 dx_cell = 10⁻⁸ m (p.12) 뿐 | 인쇄 |
| 입자 수 | [미확인] · 작은 기둥의 면 분할선 (입자 영역) 은 지름당 ≈ 40 · 높이당 ≈ 40 → 간격 ≈ 2.5 nm · 기둥 하나 ≈ 5 × 10⁴ 개 | [판독: Fig. 5 · 7 · 8 밝기 줄무늬의 주기] · [카드 산술: (π/4) · 40² · 40] |
| 시간 간격 값 | [미확인] (식만) | — |
| 쓴 밀도 | 시험 두 쌍만 인쇄 (§3-4) · §4.3–4.7 본 계산: [미확인] | — |
| 경계 조건 | 바닥 고정 (Fig. 3–8 · *"the base of the pillar is fixed"* p.17 — 거는 방법 미인쇄) · 기판에 붙음 (Fig. 9 · 10) · 표면 유속 (식 16–18) · 외력 b = 0 | 인쇄 |
| 탈리튬화 | 확산계수를 리튬화 끝의 값으로 **고정** · 유속의 부호 · 크기 · 끝내는 조건은 [미확인] | 인쇄 · §4.7 p.19 |
| 온도 | [미확인] (R · T 는 쓰지 않은 식 19–21 에만 나온다) | — |

### 3-3. 검증 — 1D 확산 (§2.2 · Fig. 1)

문제: ∂c/∂t = D ∂²c/∂x², 0 ≤ x ≤ 1, c(x, 0) = 0, c(0, t) = 1, c(1, t) = 0 (식 9–12) · 해석해 = 식 (13) 의 Fourier 급수 1000 항 · 셀당 입자 2 · 시각 0.25 · 오차 = 식 (14)(15).  D 값은 인쇄돼 있지 않다 — Fig. 1a 의 점 40 개를 식 (13) (지수에 t 를 넣은 꼴) 에 맞추면 D·t ≈ 0.025 → **D ≈ 0.1** [판독 · 카드 산술 · 맞춤 잔차 RMS 0.002].

| 격자 간격 h | 입자 수 N = 2/h [카드 산술] | 인쇄된 'error' [판독 · Fig. 1b] | 입자별 상대오차의 RMS = error × √N [카드 산술] |
|---|---|---|---|
| 0.1 | 20 | 0.56 | 2.5 |
| 0.05 | 40 | 0.049 | 0.31 |
| 0.02 (빨강 = Fig. 1a) | 100 | 0.0123 | 0.123 |
| 0.01 | 200 | 0.0068 | 0.096 |
| 0.005 | 400 | 0.0037 | 0.075 |
| 0.002 | 1000 | 0.0016 | 0.050 |
| 0.001 | 2000 | 0.00079 | 0.035 |

- 저자 판정: *"From the data it can be seen experimentally that the order of accuracy of the MPM method appears to be O(h)"* (p.6).  [판독] 이웃 점 사이 기울기: h 0.001–0.02 에서 1.00 · 0.95 · 0.87 · 0.85, 0.02 → 0.05 는 1.5, 0.05 → 0.1 은 3.5 (가장 거친 격자는 급히 나빠진다).
- ⚠ **식 (15) 를 인쇄대로 읽으면** error = √(Σe_p²)/N = RMS/√N 이다.  입자별 오차가 그대로여도 N 이 늘면 N^(−1/2) 로 준다 → 인쇄된 O(h) 는 RMS 상대오차로는 **기울기 ≈ 0.42** (h 0.02 → 0.001 에서 0.123 → 0.035) 에 해당한다 [카드 산술].  저자가 실제로 어느 쪽으로 계산했는지는 식 (15) 밖에 근거가 없다.
- [판독] Fig. 1a (h = 0.02): 입자는 x = 0.005 · 0.015 · … (간격 0.01 = 격자의 절반) · 첫 입자 c ≈ 1.02 (경계값 1 을 넘는다) · 둘째 0.946 · x = 0.395 에서 0.078.  그림은 x ≤ 0.40 만 보인다.
- 이 검증이 **다루지 않는 것**: 응력 의존 D · 유속 경계 (식 16–18) · 변형하는 물체 · 3D · 결합 문제 전체.

### 3-4. 질량 (밀도) 스케일링 시험 (§4.2.1 · Fig. 3 · 4)

| 시험 | 밀도 [kg m⁻³] | 그 밖의 조건 (인쇄) | 비교 시각 (인쇄) | 저자 판정 (인쇄) |
|---|---|---|---|---|
| ① Fig. 3 | 2.33 × 10³ ↔ 2.33 × 10⁸ | K 67 · G 31 GPa · 선형 경화 σ_Y 1.4 · 소성 계수 1.15 GPa · D₀ 를 **10⁻¹⁰ m² s⁻¹ 로 인위 증가** | 6.0 · 26.0 · 48.0 × 10⁻⁹ s | *"even with a five order increase in density, qualitatively the variations between the simulations are small"* |
| ② Fig. 4 | 2.33 × 10¹⁸ ↔ 2.33 × 10²⁴ | 같은 재료 · D₀ = 10⁻¹⁷ m² s⁻¹ (*"within the range of published values [52]"*) | 4.0 · 16.0 · 28.0 s | *"it can be seen qualitatively that there is very little variation between the two simulations despite the five orders of magnitude difference in density"* |

두 시험 모두 판정은 **그림의 눈 대조**다 (오차 노름 · 응력 · 에너지 비교 없음).  ⚠ 본문은 두 쌍 모두 *five order(s)* 차라고 적지만, 인쇄된 값으로 ② 는 10²⁴/10¹⁸ = **10⁶ 배** 차다 [카드 산술 — 본문 p.13–14 와 Fig. 4 캡션의 두 값이 같다].  카드가 그림에서 읽은 것과 산술:

| 밀도 [kg m⁻³] | c_s [m s⁻¹] | dt_mb (dx = 10 nm) | 0.1 µm 를 종파가 지나는 시간 | [판독] 윤곽 높이 (세 시각 · px) |
|---|---|---|---|---|
| 2.33 × 10³ | 6.82 × 10³ | 1.47 × 10⁻¹² s | 1.47 × 10⁻¹¹ s | 510 · 552 · 580 |
| 2.33 × 10⁸ | 21.6 | 4.64 × 10⁻¹⁰ s | 4.64 × 10⁻⁹ s | 506 · 554 · 575 |
| 2.33 × 10¹⁸ | 2.16 × 10⁻⁴ | 4.64 × 10⁻⁵ s | 4.64 × 10⁻⁴ s | 517 · 597 · 675 |
| 2.33 × 10²⁴ | 2.16 × 10⁻⁷ | 0.0464 s | 0.464 s | 518 · 596 · 673 |

(c_s ∝ ρ^(−1/2) · dt_mb = dx/c_s · dx = 10⁻⁸ m 는 §4.2.1 의 예시 값을 그대로 둔 **가정** — 3D 계산의 실제 격자 간격은 [미확인].  전부 [카드 산술], 마지막 열만 [판독].)

- [판독] 같은 시각의 두 밀도: 윤곽 높이 차 ≤ 1 % (Fig. 3) · ≤ 0.3 % (Fig. 4) · 반쪽 윤곽을 회전체로 적분한 값의 차 0.2 · 1.3 · 1.9 % (Fig. 3) · 0.1 · 2.1 · 1.1 % (Fig. 4).  Fig. 3 은 실제 밀도 쪽 (왼쪽 반) 겉면이 더 거칠다 (c · e).
- [판독 · 카드 산술] 겉면이 올라가는 속도 ÷ 종파속: Fig. 3 ≈ 0.34 m s⁻¹ → **5 × 10⁻⁵ ↔ 1.6 × 10⁻²** · Fig. 4 ≈ 1.3 × 10⁻⁹ m s⁻¹ → **6 × 10⁻⁶ ↔ 6 × 10⁻³** (높이 증가분 × 화소 크기 ÷ 시각 차 · 화소 크기는 고정 바닥 폭 = 0.1 µm 로 정함).  즉 두 시험은 이 비가 10⁻² 근처일 때와 그보다 300 배 (①) · 1000 배 (②) 작을 때의 **형상**이 눈으로 같다는 것을 보인 것이다.
- [카드 산술 · dx 가정] 확산 쪽 시간 간격 dx²/2D 는 D₀ = 10⁻¹⁷ 에서 5 s (c = 0) → 0.0124 s (c = 1, p ≤ 0).  밀도 2.33 × 10²⁴ 의 dt_mb = 0.0464 s 와 같아지는 것은 D = 1.08 × 10⁻¹⁵ (c ≈ 0.78) 일 때다 → 저자가 목표로 적은 *"limiting time step criteria is dependent upon … the diffusion equation"* 은 그 밀도에서도 농도가 높은 곳에서만 선다.  시험 ① (D₀ 10⁻¹⁰) 에서는 두 밀도 모두 dt_mb 가 더 작다 (4.64 × 10⁻¹⁰ s ↔ dt_diff ≥ 1.24 × 10⁻⁹ s).

### 3-5. 본 계산에서 읽은 값 (Fig. 5–10 · 전부 [판독] — 논문에 인쇄된 결과 수치는 농도 띠와 걸음 수 · 시간뿐)

| 그림 | 인쇄된 것 | 카드가 읽은 것 [판독 · 카드 산술] |
|---|---|---|
| Fig. 5 (구성식 셋) | 조건: K 67 · G 31 GPa · σ_Y 1.4 GPa · 소성 계수 1.15 GPa · η 0.56 · 유속 · 확산 손잡이는 *"the same for all three"* (값 미인쇄) | 완전 리튬화 윤곽 (탄성 · 완전 소성 · 선형 경화): 최대 폭 743 · 741 · 743 px · 높이 770 · 794 · 785 px · 고정 바닥 폭 464 · 443 · 451 px → 폭 ×1.60–1.67 · 높이 ×1.66–1.79 · 회전체 부피 ×3.95 · 4.53 · 4.30 (바닥 폭을 처음 지름으로 둠).  중간 포화: 높이 544 · 519 · 523 px (탄성이 가장 높다) |
| Fig. 6 · 7 (유속 10⁻⁹ ↔ 10⁻⁸) | 전선 뒤 정규화 농도 **0.5–0.6** (10⁻⁹) ↔ **> 0.7** (10⁻⁸) ↔ 실험 ∼0.67 [5] (p.15) | 네 칸의 높이 (첫 칸 대비): 10⁻⁹ ×1.10 · 1.17 · 1.22 / 10⁻⁸ ×1.14 · 1.26 · 1.45 · 최대 폭 ×1.12 · 1.17 · 1.20 / ×1.19 · 1.30 · 1.40.  Fig. 7a (10⁻⁹ · 완전 리튬화): 폭 ×1.61 · 높이 ×1.72 · 회전체 부피 ≈ ×4.2 |
| Fig. 8 (β 0 ↔ 1) | 정성 문장만 | 수치 판독 없음 (a · b 는 바닥 모서리 확대) |
| Fig. 9 (기판) | 정성 문장만 | 수치 판독 없음 (기둥 왼쪽 가장자리 확대) |
| Fig. 10 (한 바퀴) | 9 코어 · **27,472 걸음** · **48.57 h** | 첫 칸: 폭 ÷ 높이 = 9.7 (치수 0.5/0.05 = 10 — 판독 방법의 점검).  완전 리튬화 (6 번째 칸): 최대 폭 ×1.45 · 가운데 높이 ×3.40 · 회전체 부피 ≈ **×5.0**.  탈리튬화 끝 (9 번째 칸): 최대 폭 ×0.98 · 높이 ×1.35 · 회전체 부피 ≈ ×1.1 |

- ⚠ **부피 팽창 값의 대조** [카드 판독 · 논문 밖]: 논문은 계산이 낸 부피 팽창률을 적지 않았다.  윤곽 판독은 ×4.0–5.0 (작은 기둥 ≈ 4.0–4.5 · 큰 기둥 ≈ 5.0; 방법 오차는 끝 상태 ≈ ×1.1 로 미루어 ± 10 % 안팎) 으로, 서론의 ~280 % (×3.8) 보다 크다.  η = 0.56 은 (1 + η)³ = 3.80 으로 고른 값으로 보이는데, 식 (33) 은 그 η 를 **변형률 속도**에 곱한다 — 속도를 적분하면 로그 변형률이므로 구속 없는 등방 팽창의 부피비는 exp(3ηc) = 5.37 (c = 1) 이 된다 [카드 산술].  판독값이 3.80 과 5.37 사이에 있는 것은 이 읽기와 어긋나지 않는다 (c < 1 에서의 유속 제한 · 고정 바닥 · 판독 오차).  ⇒ **속도 꼴로 자유 변형률을 넣을 때 계수는 로그 변형률 기준이어야 한다** (280 % 를 원하면 η = ln(3.8)/3 = 0.445).

### 3-6. 계산 비용

| 항목 | 값 | 표지 |
|---|---|---|
| 대상 | 큰 기둥 (Ø0.5 × 0.05 µm) + 변형 기판 · 리튬화 → 탈리튬화 한 바퀴 | 인쇄 · §4.7 |
| 기계 | 단일 계산 노드의 **9 코어** · Intel Xeon E5-2667 (물리 6 코어 → 하이퍼스레딩 12) · 2.9 GHz | 인쇄 · p.19 |
| 걸음 수 · 시간 | **27,472 걸음** · 벽시계 **48.57 h** (*"estimated"*) | 인쇄 · p.19 |
| ⇒ 걸음당 · 코어·시간 | 6.36 s/걸음 · 437 코어·시간 | [카드 산술: 48.57 × 3600/27472 · 48.57 × 9] |
| 입자 수 · 격자 수 · 물리 시간 | [미확인] | — |
| 다른 계산 (Fig. 3–9) 의 비용 | [미확인] | — |

### 3-7. ★ 이 논문에 **없는** 값 (정직 목록)

| 찾은 것 | 상태 |
|---|---|
| 3D 계산의 격자 간격 · 셀당 입자 수 · 입자 수 · 영역 크기 | **없음** (예시 dx_cell = 10⁻⁸ m 뿐) |
| 본 계산에 쓴 밀도 (스케일링 배수) · 시간 간격 값 · 물리 시간 | **없음** |
| 유속 10⁻⁹ · 10⁻⁸ 의 단위 · 시간 함수 J(t)_bc 의 꼴 · 탈리튬화의 유속 | **없음** |
| 응력 · 압력 · 소성 변형률의 분포 또는 값 | **없음** — 모든 결과 그림은 농도로 칠한 형상이다 |
| 계산이 낸 부피 팽창률 · 높이 · 폭 변화 | **없음** (카드 판독만 — §3-5) |
| 3D 격자 · 입자 수 수렴 시험 | **없음** |
| 결합 문제의 해석해 · FEM · 실험과의 정량 대조 | **없음** |
| 에너지 (운동 ÷ 변형) 같은 준정적 지표 | **없음** |
| 접촉 · 마찰 · 분리 | **없음** (붙음) |
| a-Si · 기판 물성의 출처 · 기판 재료 이름 · 온도 | **없음** |
| 바닥 고정 · 기판으로의 확산 차단을 거는 방법 | **없음** (결과만 서술) |
| 기공 · 바인더 · 집전체 · 전해질 · 다입자 전극 | **없음** (기둥 하나 + 기판) |

---

## 4. 방법 ★

### 4-1. MPM 정식화 (§1–§2 · 식 1 · 그림 `eq_01_momentum_balance.png`)

- 운동량 보존 **ρa = ∇·σ + ρb** (1) — ρ 밀도 · a 가속도 · σ 응력 · b 외력 가속도 (중력 등).
- MPM 의 전제 (p.3–4): 물체를 물질점으로 나누고 질량 · 운동량을 물질점에 싣는다 (Lagrange) · 배경 Euler 격자에 *"an appropriate choice of grid and particle basis functions"* 로 옮겨 격자에서 운동량 식을 풀고 · **상태의 변화량**을 입자로 보간해 시간 전진 · *"Variations in MPM come as a result of the choices made in grid and particle basis functions."*
- 이 논문의 선택: **CPDI** (convected particle domain interpolation · ref. [38]).  변종의 설명은 이 논문에 없다 — 이름과 ref. [38] 의 제목 (*"… to extend applicability of the material point method for problems involving massive deformations"*) 뿐이다.  [정본 카드의 설명: 입자 영역을 변형하는 평행육면체로 두고 형상함수를 그 영역에서 평균 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact` §4-1 · 용어집) · 극단 인장에서 수치적 끊김이 없다 (`devaucorbeil2020_mpm_after_25_years_review` 의 변종 표)].  알고리즘 세부 · 가중 함수는 ref. [34, 37, 38] 로 넘긴다.  코드 = Uintah.
- 논문이 **적지 않은 것**: 격자 종류 · 가중 함수의 식 · 셀당 입자 수 (3D) · 응력 갱신 순서 (USF / USL) · 속도 갱신 꼴 (FLIP / PIC) · 접촉.

### 4-2. MPM 위의 확산 — 다섯 단계 (§2.1 · 식 2–8 · 그림 `eq_02_…` – `eq_08_…` · `eq_unnumbered_s2_1_normalized_concentration.png`)

리튬은 두 가지로 옮겨진다 (p.4).  **이류**: *"lithium being assigned to a material point, the mass of the host material of each material point does not change.  The advection of the guest material is accounted for naturally when material points are advected."* — 농도를 입자에 실으면 끝.  **확산**: 정규화 농도 **c = c_g/c_max** (c_max = Li 3.75 : Si 1 의 몰농도 · c_g = 현재 몰농도) 에 대해

> **∂c/∂t = −∇·J** (2),   **J = −D∇c** (3)

를 *"many of the same numerical methods that are used in solving the momentum balance equations"* 로 푼다.

| 단계 | 식 | 운동량 풀이의 대응 연산 (원문) |
|---|---|---|
| 1 | **m_i = Σ_p φ_ip m_p** (4) | 입자 질량 → 격자 (*"grid values for m_i have already been computed"*) |
| 2 | **c_i = Σ_p φ_ip m_p c_p / m_i** (5) | *"similar fashion to mapping velocity values from particles to grid nodes"* (질량 가중) |
| 3 | **J_p = −D Σ_i ∇φ_ip c_i** (6) | 가중 함수의 기울기로 격자 농도를 입자에서 미분 |
| 4 | **∂c_i/∂t = Σ_p (J_p·∇φ_ip) m_p / m_i** (7) | *"in a manner similar to that used in computing the divergence of stress"* |
| 5 | **c_p^{n+1} = c_p^n + dt Σ_i φ_ip ∂c_i/∂t** (8) | 격자 변화율을 입자로 보간해 전진 |

- φ_ip = 가중 함수 (CPDI 것 · ref. [38]) · m_i · m_p = 격자 · 입자 질량 · c_i · c_p = 격자 · 입자 정규화 농도.
- 출처: *"This method of modeling concentration diffusion within MPM is similar to methods used previously in modeling heat diffusion [41–43]."* (p.5)
- [카드 판독] 식 (7) 에 음의 부호가 없는 것은 약형 (∫w ċ = ∫∇w·J − 경계 항) 과 맞다.  밀도 가중 (m_p) 꼴이라 격자 농도는 질량 평균이다.
- [카드 판독] 식 (5) 는 한 노드에 얹히는 모든 입자를 섞는다.  기둥과 기판이 노드를 나눠 가지면 기판 입자 (c = 0) 가 평균에 들어온다 — *"There was no diffusion of lithium into the substrate material"* (p.19) 를 어떻게 지켰는지 (재료별 풀이 · 기판 D = 0 등) 는 본문에 없다 [미확인].

### 4-3. 표면 유속 경계조건 (§2.3 · 식 16–18 · 그림 `eq_16_…` · `eq_17_…` · `eq_18_…` · `eq_18_…_no_tag.png`)

- 뜻: *"a flux was applied to the surface of the object … intended to mimic the flux induced by applying a voltage difference between the object and a far away cathode."* (p.6)
- 표면이 움직이므로 **처음에 표면 입자를 표시**하고 처음 겉넓이를 기록한다.  가정 둘 — ① 표면이 움직이고 늘어나도 어느 입자 · 어느 면이 표면인지는 안 바뀐다 (*"inspection of the results below validates this assumption"*), ② 입자마다의 표면 넓이는 일정 (*"probably less valid, and will be fixed in future work … Inspection of the subsequent results show that this is not a valid assumption, but … this is similar to prescribing a slightly lower flux than intended"*) (p.6–7).
- 표면 입자의 농도 변화율: **(∂c_pv/∂t)_bc = J(t)_bc A_p/V_p** (16) — J(t)_bc 사용자 지정 유속 · A_p 유속이 걸리는 입자 면의 넓이 · V_p 입자 부피.
- 포화 제한: **(∂c_pv/∂t)′_bc = (∂c_pv/∂t)_bc · (1 + 0.25 log(1 − c_p))** (17) — *"While the equation above is ad hoc, this reflects physically meaningful behavior."*
- 격자 식에 원천항으로: **∂c_i/∂t = Σ_p (J_p·∇φ_ip) m_p / m_i + Σ_p (∂c_pv/∂t)′_bc φ_ip m_p / m_i** (18).  ⚠ 이 식의 번호 칸은 **"(18rate of change of the elastic)"** 로 인쇄돼 있다 (조판 오류 — 식 19 아래 설명문의 조각으로 보임 [카드 판독]).

### 4-4. 응력 → 확산 (§3.1 · 식 19–24 · 그림 `eq_19_…` – `eq_24_…` · `eq_unnumbered_s3_1_*.png` · Fig. 2)

저자는 기존 모형을 둘로 나눈다 (p.7–8).

**첫째 군 — Larché–Cahn 화학 퍼텐셜** ([23, 45, 46] · 틀 [11–14]):

> **μ_Li = μ⁰_Li + RT ln(γ c/(1 − c)) + κ (dε^c_vol/dc) p − (κ/2) B_ijkl σ_ij σ_kl** (19)
> **J = −D (c/RT) ∇μ** (20)

μ⁰_Li 기준 화학 퍼텐셜 · R 기체 상수 · T 온도 · γ *activation coefficient* · κ 규소의 몰부피 · **ε^c_vol = ε^c_ii/3** (리튬 삽입 자유 변형률의 체적 몫) · **p = −σ_ii/3** (압축이 양수) · **B_ijkl = dS_ijkl/dc** (탄성 컴플라이언스의 농도 변화율).  컴플라이언스가 농도와 무관 (B = 0 — *"as is the case for the model discussed below"*) 하고 자유 변형률이 농도에 선형이면

> **J = −(Dγ/(1 − c)) ∇c − (Dκc/RT)(dε^c_vol/dc) ∇p** (21)

**둘째 군 — 경험식** ([5, 19–21]): *"a model is formulated that takes as input concentration and in some cases stress and then the user adjusts a set of parameters to produce the desired behavior"*

> **J = −D(c, σ)∇c** (22)

**이 논문은 둘째 군을 택한다** — 이유 (p.8): *"the greatest changes in pressure occur in regions where lithium is diffusing into the non-lithiated amorphous silicon, in the areas behind this region the changes in pressure are minimal and the contribution of the pressure gradient to the concentration flux is small.  The empirical based approach … provides a good first approximation of the diffusion process."*

> **D(c, p) = D₀ e^(αc)** (p ≤ 0) · **D₀ e^(αc − βp)** (0 < p < p_max) · **D₀ e^(αc − β p_max)** (p ≥ p_max)   (23)

D₀ 처음 확산계수 · α · β *tuning parameters* · p_max 압력의 상한.  *"It is through the diffusivity function that stress is coupled to the diffusion process."* (p.9)  견줌: Berla 외 [21] · Wang 외 [20] 의 농도만의 삼차식 **D(c) = D₀(1 − c)³ + D_max c³** (24).  값: D₀ = 10⁻¹⁷ m² s⁻¹ · D_max = 10⁻¹⁵ m² s⁻¹ · α = 6.0 · β = 0.5 · p_max = 3 GPa (Fig. 2).

- ⇒ **응력 기울기가 리튬을 미는 항 (식 21 의 둘째 항) 은 구현돼 있지 않다.**  응력은 "확산이 얼마나 빠른가" 만 바꾼다.
- [카드 산술] 식 (21) 의 첫 항: ∇ ln(γc/(1 − c)) = ∇c/(c(1 − c)) (γ 상수) 이므로 계수는 D/(1 − c) 가 되어야 한다 — 인쇄에는 γ 가 남아 있다.
- [카드 판독] D 를 어디서 평가하는지 (입자 c_p · 입자 압력으로 읽는 것이 자연스럽다) 는 인쇄돼 있지 않다.

### 4-5. 농도 → 응력 — hypoelastic–plastic (§3.2–§3.4 · 식 25–39 · 그림 `eq_25_…` – `eq_39_…` · `eq_unnumbered_s3_3_deviatoric_stress.png`)

**변형률 속도의 덧셈 분해** (p.9): *"The hypoelastic-plastic model allows for an additive decomposition of the rate of strain tensor into elastic, plastic, and stress-free volumetric components"*

> **d = d^e + d^p + d^c** (25)

**객관성** — 회전 전 자리에서 갱신 (p.9): 변형 구배의 극분해 **F = RU** (26) 의 회전 R 로 **σ̄ = Rᵀ σ R** (27) · **d̄ = Rᵀ d R** (28) · **d = ½ (l + lᵀ)** (29, l = 속도 기울기).

> *"The unrotated symmetric part of the velocity gradient is chosen as a rate of strain because of the relatively low computational cost relative to other possible choices for rates of strain and under conditions where the rotation of the principle referential directions is small the unrotated symmetric part of the velocity gradient is a good approximation for Hencky strain rate [47]."* (p.9 · [47] = Brannon 2017 personal communication)

**탄성** (p.10): **σ̄ = 2G ε^e_dev + 3K ε^e_vol** (30) → **σ̇ = 2G d̄^e_dev + 3K d̄^e_vol** (31 — 인쇄에는 σ 위에 점만 보인다).

**리튬화 자유 변형률** (p.10 — 비정질이라 등방 · [13] 의 모형 · 열팽창 [48] 과 같은 꼴): **ε^c = η (c − c₀) I** (32) → **d̄^c = η (∂c/∂t) I** (33).  η = *volume expansion coefficient* (0.56) · I 단위 텐서.

**소성** (§3.3 · p.10) — 두 가지:

> 완전 소성: **√(3/2 σ̄_dev : σ̄_dev) − σ_Y = 0** (34)
> 선형 등방 경화: **√(3/2 σ̄_dev : σ̄_dev) − (σ_Y + K ε^p_equiv) = 0** (35)

σ_Y 처음 항복 응력 · **σ̄_dev = σ̄ − 1/3 tr(σ̄)** (편차 응력 · 인쇄에 단위 텐서 없음) · K *plastic modulus* (⚠ 식 30 의 체적계수와 같은 글자) · ε^p_equiv 등가 소성 변형률.  d̄^p 를 구하는 방법은 *"beyond the scope of this paper"* — ref. [49] (Simo & Hughes) 로 넘긴다.  두 모형 모두 Uintah MPM 에 구현돼 있던 것.

**응력 갱신** (§3.4 · p.10–11):

> **d̄^e = d̄ − d̄^c − d̄^p** (36)
> **d̄^e_vol = ⅓ tr(d̄^e) I,   d̄^e_dev = d̄^e − d̄^e_vol** (37)
> **σ̄^{n+1} = σ̄^n + (2G d̄^e_dev + 3K d̄^e_vol) dt** (38)
> **σ^{n+1} = R σ̄^{n+1} Rᵀ** (39)

- 세 구성식 = 선형 탄성 (소성 끔) · 완전 소성 · 선형 등방 경화 (초록의 *"three different constitutive models"*).
- 탄성 계수는 농도와 무관 (B_ijkl = 0) — 리튬화에 따른 연화는 모형에 없다.

### 4-6. 시간 척도 · 시간 간격 · 질량 스케일링 (§4.1–§4.2.1 · 식 40–49 · 그림 `eq_40_…` – `eq_49_…`)

- 외력 무시 (b = 0): **ρa = ∇·σ** (40).  종파속 **c_s = √((K + 4/3 G)/ρ)** (41) = 6.8 × 10³ m s⁻¹.  확산계수 10⁻¹⁷–10⁻¹⁵ m² s⁻¹ 과 견주면 역학이 훨씬 빠르므로 확산의 시간 척도 안에서 운동량 식은 준정적 **∇·σ = 0** (42) 에 이른다 ([16, 50, 51]).
- 매 걸음 끝에 새 시간 간격 (p.12): **dt_mb = min(dx_cell/(c_s + v_x), dy_cell/(c_s + v_y), dz_cell/(c_s + v_z))** (43) · **dt_diff = min(dx²_cell/2D, dy²_cell/2D, dz²_cell/2D)** (44) · **dt = min(dt_mb, dt_diff)** (45).  (안전계수 · Courant 수는 인쇄돼 있지 않다.)
- 문제 (§4.2.1): c_s = 6.8 × 10³ m s⁻¹ · dx_cell = 10⁻⁸ m 이면 **dt_mb = dx_cell/c_s = 6.8 × 10⁻¹¹ s** (46 — ⚠ 인쇄값; 10⁻⁸/6.8 × 10³ = 1.47 × 10⁻¹² s [카드 산술]) → 6.8 s 에 10¹¹ 걸음 = *intractable*.  D = 10⁻¹⁵ m² s⁻¹ 이면 **dt_diff = dx²_cell/2D = 0.05 s** (47) = *tractable*.
- 우회: 밀도를 인위로 올린다 (§0 의 인용).  근거 식 — 탄성 관계 (30) 을 (40) 에 넣어 **ρa = 2G∇·ε^e_dev + 3K∇·ε^e_vol** (48) → **a = (2G/ρ)∇·ε^e_dev + (3K/ρ)∇·ε^e_vol** (49): 밀도를 올리면 탄성파만 느려지고 탄성 변형률은 같다.
- 시험: §3-4 의 두 쌍.

### 4-7. 접촉 · 계면 · 경계 — 이 논문이 **하지 않은 것**

| 묻는 것 | 이 논문 |
|---|---|
| 물체 사이 접촉 알고리즘 | **없다** — 'contact' 0 회.  기둥과 기판은 한 격자 속도장을 나눠 쓴다 (다물체 속도장 · 마찰 · 분리 판정에 대한 서술이 없으므로 그렇게 읽는다 [카드 판독]) |
| 기둥–기판 계면 | *"the pillar is assumed to be affixed to the substrate and the substrate material is allowed to deform"* (p.17) = 붙음 (미끄럼 · 분리 없음) |
| 미끄럼의 가능성 | *"It is unknown if the deformation comes as a result of the sliding between the anode and the substrate material or deformation in the substrate."* (p.17) — 시험하지 않음 |
| 계면을 통한 확산 | *"There was no diffusion of lithium into the substrate material."* (p.19) — 거는 방법 [미확인] |
| 바닥 고정 (Fig. 3–8) | *"the assumption that the base of the pillar is fixed"* (p.17) — 거는 방법 [미확인] |
| 자기 접촉 (접힌 옆면 · Fig. 7b) | 서술 없음 — 한 속도장이라면 접힌 면끼리는 붙는다 [카드 추론] |
| 자유 표면 | 표면 입자 표지는 유속을 걸기 위한 것이다 — 자유 표면에 역학 조건을 따로 거는 서술은 없다 |

### 4-8. 의사코드 — 한 걸음 (우리 전사 · 논문에 한 걸음 전체의 순서도는 없다)

```
# (번호) = 논문 식 · [카드 판독] = 순서와 평가 자리는 카드가 이어 붙인 것 · [34, 38, 49] = 논문이 넘긴 문헌
P2G   m_i = Σ_p φ_ip m_p                                   (4)   # 운동량 풀이와 공유
      (운동량 → 격자 속도)                                  [34, 38]
      c_i = Σ_p φ_ip m_p c_p / m_i                          (5)
확산  D_p = D(c_p, p_p)                                     (23)  [카드 판독: 평가 자리 미인쇄]
      J_p = −D_p Σ_i ∇φ_ip c_i                              (6)
      ċ_i = Σ_p (J_p·∇φ_ip) m_p / m_i                       (7)
      표면 입자:  r = J_bc(t) A_p / V_p                      (16)  # A_p 는 처음 값 고정
                  r′ = r · (1 + 0.25 log(1 − c_p))           (17)
      ċ_i += Σ_p r′ φ_ip m_p / m_i                          (18)
      c_p ← c_p + dt Σ_i φ_ip ċ_i                           (8)
역학  격자 내부력 · 가속도 · 속도 (ρa = ∇·σ)                  (40)  [34, 38]
      l_p = Σ_i ∇φ_ip v_i ;  d = ½ (l + lᵀ)                 (29)
      F = RU ;  d̄ = Rᵀ d R ;  σ̄ = Rᵀ σ R                    (26)–(28)
      d̄^c = η ċ_p I                                         (33)
      d̄^p ← J2 반환 (완전 소성 34 / 선형 경화 35)             [49]
      d̄^e = d̄ − d̄^c − d̄^p ;  체적 · 편차 분리                (36)(37)
      σ̄ ← σ̄ + (2G d̄^e_dev + 3K d̄^e_vol) dt                 (38)
      σ = R σ̄ Rᵀ                                            (39)
G2P · 입자 이동 · CPDI 영역 갱신                              [38]
dt ← min(dt_mb, dt_diff)                                    (43)–(45)  # 밀도는 인위로 키운 값
```

### 4-9. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

| 축 | 이 논문 |
|---|---|
| 물체 | 원기둥 하나 (Ø0.1 × 0.1 µm 또는 Ø0.5 × 0.05 µm) + 기판 블록 — **입자 층 · 패킹 · 입도가 없다** |
| 변형 | **진짜 형상 변화** (연속체 소성 유동 — 접촉 겹침의 대리가 아니다): 높이 ×1.7 (작은 기둥) · ×3.4 (큰 기둥 가운데) [판독] |
| 소성 | J2 · 완전 소성 또는 선형 등방 경화 · σ_Y 1.4 GPa · E/σ_Y ≈ 58 [카드 산술] |
| 접촉 | 없음 (붙음) |
| 강체 | 움직이는 강체는 없다.  "non-deformable substrate" (Fig. 9 a · c 의 격자선 없는 회색 판) 가 강체 물체인지 앞 절들의 바닥 고정 조건을 그린 것인지는 본문에 없다 [미확인] |
| 무작위성 | 없음 (결정론 · 기둥 하나) |
| 기공 | 없음 |

---

## 5. 결과 — 절별

### 5-1. 확산 풀이의 검증 (§2.2 · Fig. 1)

1D 문제에서 h = 0.02 의 MPM 해가 해석해와 겹치고 (Fig. 1a), 오차는 격자를 조이면 기울기 1 의 기준선을 따라 준다 (Fig. 1b) → *"appears to be O(h)"*.  값 · 한정은 §3-3.

### 5-2. 시간 간격 문제와 밀도 증가 (§4.2.1 · Fig. 3 · 4)

밀도가 10⁵ 배 (Fig. 3) · 10⁶ 배 (Fig. 4 — 본문은 둘 다 *five order(s)* 라 적는다) 다른 두 쌍의 계산이 같은 시각에 *qualitatively* 같다.  Fig. 3 은 날카로운 전선이 겉에서 안으로 들어가는 초기 (6–48 ns · D₀ 10⁻¹⁰), Fig. 4 는 농도가 거의 고르게 0.5–0.6 까지 차는 과정 (4–28 s · D₀ 10⁻¹⁷) 이다.  값 · 한정은 §3-4.

### 5-3. 구성식 비교 (§4.3 · Fig. 5)

- *"From the image it can be seen that at full saturation there is a noticeable difference between the linear elastic and the two plasticity models.  The largest noticeable difference is along the base of the pillars where the largest concentration of plastic deformation occurs."* (p.14)
- 중간 포화 (a–c) 에서 이미 바닥 둘레의 소성 변형이 탄성과 다른 모양을 만든다.  두 소성 모형 사이에도 *"qualitative differences"* 가 있다 (p.15) — 어떤 차이인지는 적지 않았다.
- [판독] 완전 리튬화에서 탄성 (d) 은 바닥 모서리가 둥글게 말려 들어가고, 소성 둘 (e · f) 은 바닥이 깎인 원뿔 꼴이다.  높이는 소성 쪽이 더 높다 (770 ↔ 794 · 785 px).
- *"A proper constitutive model needs to be selected in order to achieve the desired behavior that matches that of a silicon anode during lithiation."* (p.14) — 그러나 어느 모형이 실험과 맞는지의 판정은 없고, 뒤 절은 선형 등방 경화를 쓴다.

### 5-4. 유속 경계조건의 영향 (§4.4 · Fig. 6 · 7)

- *"Both the perfectly plastic and the linear strain hardening constitutive models are dependent upon the prior history of the material.  Because of this history dependent behavior the choice of flux boundary conditions affects the shape of the pillars."* (p.15)
- 유속 10⁻⁹ ↔ 10⁻⁸ (선형 경화 · α 6 · β 0.5 · p_max 3 GPa): 둘 다 날카로운 전선을 내고, 전선 뒤 농도는 0.5–0.6 ↔ > 0.7 (실험 ∼0.67).  큰 유속 쪽이 바닥 근처의 불룩함이 더 뚜렷하고 (p.15), 완전 리튬화 뒤에도 모양이 다르다 (Fig. 7 · p.16).
- [판독] Fig. 7b (10⁻⁸) 는 옆면이 세로로 접히고 바닥 위가 겹쳐 밀려 나온다 — 입자 영역이 길게 늘어난 띠가 보인다.

### 5-5. 확산계수 손잡이 (§4.5 · Fig. 8)

- *"The issue that has been discovered is that while the calculated values for diffusivity may fall within the computed range of values for a chosen set of tuning parameters, the deformation behavior can vary based on what tuning parameters are chosen."* (p.16)
- *"But it's clear that the mobility of lithium ions within amorphous silicon has to be a function of both lithium concentrations and pressure."* (p.16)
- β = 0 ↔ 1 (유속 10⁻⁹ · 선형 경화): 리튬화 중 바닥 모서리의 변형이 눈에 띄게 다르고 (Fig. 8 a · b), 완전 포화에서는 차이가 준다 (c · d).

### 5-6. 변형하는 기판 (§4.6 · Fig. 9)

- 단단한 (non-deformable) 기판: *"large deformations occur in the region where pillar attaches to the base"*; 변형 기판: *"the deformation due to the pillar swelling is shared between both the pillar and the substrate.  The deformable substrate reduces the accute deformations that occur in the pillar as highlighted by circled regions of figures 9(a) and (b)."* (p.18–19)
- 완전 리튬화의 기둥 모양도 다르다 (c · d).
- [판독] 변형 기판은 기둥 가장자리에서 끌려 올라와 턱이 되고, 기둥 밑은 눌려 파인다 (b · d).

### 5-7. 리튬화 → 탈리튬화 한 바퀴 (§4.7 · Fig. 10)

- 조건: 큰 기둥 · 선형 등방 경화 (K 67.0 · G 31.0 GPa · σ_Y 1.4 GPa · 소성 계수 1.15 GPa) · 리튬화 중 D₀ = 10⁻¹⁷ m² s⁻¹ · α = 6.0 · β = 0.5 · p_max = 3 GPa · 탈리튬화 중 확산계수는 리튬화 끝 값으로 고정 · 기판은 선형 등방 경화 (K 180.4 · G 76.0 GPa · σ_Y 0.7 GPa · 소성 계수 1.15 GPa) · 기판으로의 확산 없음 (p.19).
- 리튬화: 날카로운 전선 + 전선 뒤의 완만한 농도 기울기 (실험 [5] 의 두 특징과 같다고 서술).  탈리튬화: 확산계수를 큰 값으로 고정해 *"the rate of diffusion throughout the entire pillar appears to be more uniform"*.
- 첫 칸과 마지막 칸의 차이 = 한 바퀴의 소성 변형 (기둥과 기판 모두) — 값은 없다.  [판독] §3-5.

### 5-8. 결론 · 향후 (§5)

- *"In this paper it has been demonstrated that the full lithiation and delitiation of a silicon anode can be simulated using the MPM."* (p.19)
- 쓰임: *"a tool to for future work in examining different anode geometries, material substrates, and flux rates"* (p.20).
- 향후: 파괴 모형 · 완전한 전기화학 (§11).

---

## 6. 그림별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/gritton2017_mpm_chemomechanical_coupling_silicon_anode/` · 그림 10 장은 도구 크롭을 내장 래스터 테두리 ± 6 pt 로 다시 자름 (300 dpi · 캡션 문자는 `figures.json` 에) · 식 56 장은 손 크롭 (400 dpi · 사방 7 pt).  [판독] · [카드 …] 표지는 논문 밖 판단.

| 그림 | 파일 | 원 캡션 요지 (PDF 쪽 / 논문 쪽) | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | (a) h = 0.02 · t = 0.25 의 MPM 확산 해 ↔ 참 해 · (b) 오차 수렴 (빨강 선 = 기울기 1 · 빨강 점 = (a)) (p.7 / 6) | 이 논문의 **유일한 정량 검증**.  오차 0.56 → 0.00079 (h 0.1 → 0.001) [판독] · 인쇄된 노름은 RMS ÷ √N 꼴 (식 15) 이라 RMS 로는 기울기 ≈ 0.4 [카드 산술].  첫 입자가 경계값을 넘는다 (c ≈ 1.02).  우리 쪽: MPM 에 새 장을 얹을 때의 단위 시험 꼴 — 노름 정의를 결과 전에 적는다 |
| 2 | `fig_2.png` | (a) 제안 확산계수 (0 · 3 GPa) ↔ Berla 식 · (b) 농도 [0, 1] × 압력 [0, 3] GPa 의 곡면 (p.9 / 8) | 응력 → 확산 결합의 전부 (식 23).  압축만 확산을 늦추고 3 GPa 에서 잘린다.  규소 전용 값.  수송 계수를 입자 상태로 매 걸음 갱신하는 양방향 결합 ↔ 우리 STEP3 는 굳은 구조의 사후 풀이 |
| 3 | `fig_3.png` | 밀도 2.33 × 10³ (a · c · e) ↔ 2.33 × 10⁸ kg m⁻³ (b · d · f) (p.14 / 13) | 질량 스케일링 시험 ① (D₀ 10⁻¹⁰ · 6 · 26 · 48 ns).  칸마다 왼쪽 반 ↔ 오른쪽 반.  윤곽 높이 차 ≤ 1 % [판독] · 겉면 속도 ÷ 종파속 ≈ 5 × 10⁻⁵ ↔ 1.6 × 10⁻² [판독 · 카드 산술] — 우리 판 Mach 0.01–0.03 과 같은 자릿수에서 **형상**은 거의 같았다는 제3자 사례 · 응력은 비교하지 않음 |
| 4 | `fig_4.png` | 밀도 2.33 × 10¹⁸ (a · c · e) ↔ 2.33 × 10²⁴ kg m⁻³ (b · d · f) (p.14 / 13) | 질량 스케일링 시험 ② (D₀ 10⁻¹⁷ · 4 · 16 · 28 s).  높이 차 ≤ 0.3 % · 속도 비 ≈ 6 × 10⁻⁶ ↔ 6 × 10⁻³ [판독 · 카드 산술].  본 계산이 어느 밀도를 썼는지는 [미확인] |
| 5 | `fig_5.png` | 중간 포화 (a–c) · 완전 포화 (d–f) — 선형 탄성 · 완전 소성 · 선형 경화 (p.15 / 14) | 구성식의 차이는 고정 바닥 둘레에 몰린다 (탄성 = 말림 · 소성 = 깎인 원뿔).  완전 리튬화 부피 ≈ ×4.0–4.5 [판독] > (1 + η)³ = 3.80 — 속도 꼴 자유 변형률의 함정 (§3-5).  입자 영역 ≈ 40 개/지름 [판독].  응력 · 소성 변형률 지도 없음 |
| 6 | `fig_6.png` | 리튬화 과정 — 유속 10⁻⁹ (a–d) · 10⁻⁸ (e–h) · 선형 등방 경화 (p.16 / 15) | 하중 이력 의존: 유속 10 배면 중간 모양이 다르다 (바닥 위 불룩함 · 주름).  전선 뒤 농도 0.5–0.6 ↔ > 0.7 ↔ 실험 ∼0.67.  우리 쪽: 소성 계산은 재하 속도 · 순서를 결과 전에 고정 |
| 7 | `fig_7.png` | 완전 리튬화 — 유속 10⁻⁹ (a) · 10⁻⁸ (b) (p.17 / 16) | 같은 끝 농도에서도 이력의 흔적이 남는다.  (b) 는 옆면이 접혀 겹친다 — 입자 영역이 심하게 찌그러진 곳인데 수치 신뢰의 판정이 없다.  한 속도장이라면 접힌 면끼리는 붙는다 [카드 추론] |
| 8 | `fig_8.png` | α = 6.0 에서 β = 0.0 (a · c) ↔ 1.0 (b · d) — 리튬화 중 · 완전 포화 (p.18 / 17) | 압력 항의 세기가 리튬화 중 바닥 모서리 (타원) 의 변형을 바꾼다 · 포화 뒤엔 차이가 준다.  손잡이가 형상을 바꾼다는 저자 고백의 그림 |
| 9 | `fig_9.png` | 변형 않는 기판 (a · c) ↔ 변형 기판 (b · d) 에 붙은 기둥 (p.19 / 18) | ★ **접촉 없는 MPM = 붙은 계면.**  변형 기판은 기둥에 끌려 올라와 턱이 되고 밑이 파인다.  저자: 실험의 바닥 팽창이 미끄럼인지 기판 변형인지 *unknown* — 계산은 뒤쪽만 시험.  우리 SE–AM · SE–판 붙음과 같은 상태 → A′-0 의 필요성 |
| 10 | `fig_10.png` | 규소 나노기둥의 리튬화 · 탈리튬화 전 과정 (9 칸) (p.19 / 18) | 한 속도장으로 '넣었다 뺀' 사례.  완전 리튬화: 폭 ×1.45 · 가운데 높이 ×3.4 · 부피 ≈ ×5.0; 끝: 폭 ×0.98 · 높이 ×1.35 · 부피 ≈ ×1.1 [판독] — 부피는 돌아오고 모양은 안 돌아온다.  계면은 끝까지 붙어 있고 기판에 자국이 남는다.  9 코어 · 27,472 걸음 · 48.57 h |

**식 그림** (번호 식 49 + 번호 칸 뺀 식 18 + 번호 없는 정의 6 = 56 장 · 파일 이름 앞머리 = 식 번호)

| 식 | 파일 | 한 줄 뜻 |
|---|---|---|
| (1) | `eq_01_momentum_balance.png` | 운동량 보존 ρa = ∇·σ + ρb |
| (2) | `eq_02_diffusion_equation.png` | 농도 보존 ∂c/∂t = −∇·J |
| (3) | `eq_03_flux_fick.png` | 유속 J = −D∇c |
| (4) | `eq_04_p2g_grid_mass.png` | 확산 1 단계 — 질량 P2G |
| (5) | `eq_05_p2g_grid_concentration.png` | 2 단계 — 농도 P2G (질량 가중) |
| (6) | `eq_06_particle_flux_from_grid_gradient.png` | 3 단계 — 입자 유속 |
| (7) | `eq_07_grid_concentration_rate_flux_divergence.png` | 4 단계 — 유속 발산 → 격자 변화율 |
| (8) | `eq_08_particle_concentration_update.png` | 5 단계 — 입자 농도 갱신 |
| (9) | `eq_09_verification_1d_conservation.png` | 검증 문제 (1D) 보존식 |
| (10) | `eq_10_verification_initial_boundary_conditions.png` | 검증 문제 초기 · 경계 조건 |
| (11) | `eq_11_verification_1d_flux.png` | 검증 문제 유속 |
| (12) | `eq_12_verification_1d_diffusion_pde.png` | 검증 문제 확산 방정식 |
| (13) | `eq_13_verification_series_solution.png` | 해석해 (급수) — ⚠ 지수에 t 없음 (인쇄 그대로) |
| (14) | `eq_14_relative_error_per_particle.png` | 입자별 상대오차 |
| (15) | `eq_15_error_norm.png` | 오차 노름 — ⚠ ÷ N (인쇄 그대로) |
| (16) | `eq_16_flux_bc_particle_concentration_rate.png` | 표면 유속 → 입자 농도 변화율 |
| (17) | `eq_17_flux_restriction_factor.png` | 포화 제한 계수 (ad hoc) |
| (18) | `eq_18_grid_concentration_rate_with_flux_bc_source.png` | 경계 원천항을 더한 격자 식 — ⚠ 번호 칸 "(18rate of change of the elastic)" (인쇄 그대로) |
| (18) 번호 칸 뺌 | `eq_18_grid_concentration_rate_with_flux_bc_source_no_tag.png` | 같은 식의 본문만 (붙여 쓰기용) |
| (19) | `eq_19_larche_cahn_chemical_potential.png` | Larché–Cahn 화학 퍼텐셜 (쓰지 않음) |
| (20) | `eq_20_flux_from_chemical_potential.png` | 화학 퍼텐셜 기울기 유속 |
| (21) | `eq_21_flux_concentration_and_pressure_gradients.png` | 농도 · 압력 기울기 꼴 (구현 안 함) |
| (22) | `eq_22_empirical_flux_stress_dependent_diffusivity.png` | ★ 채택한 경험 꼴 J = −D(c, σ)∇c |
| (23) | `eq_23_diffusivity_concentration_pressure.png` | ★ 확산계수 D(c, p) |
| (24) | `eq_24_cubic_diffusivity_berla_wang.png` | 견줌용 삼차식 |
| (25) | `eq_25_strain_rate_additive_decomposition.png` | ★ d = d^e + d^p + d^c |
| (26) | `eq_26_polar_decomposition.png` | 극분해 F = RU |
| (27) | `eq_27_unrotated_stress.png` | 응력을 회전 전 자리로 |
| (28) | `eq_28_unrotated_rate_of_strain.png` | 변형률 속도를 회전 전 자리로 |
| (29) | `eq_29_rate_of_strain_from_velocity_gradient.png` | d = ½ (l + lᵀ) |
| (30) | `eq_30_unrotated_stress_strain_relation.png` | 탄성 관계 |
| (31) | `eq_31_unrotated_stress_rate.png` | 응력 변화율 |
| (32) | `eq_32_stress_free_lithiation_strain.png` | ★ 자유 변형률 ε^c = η (c − c₀) I |
| (33) | `eq_33_stress_free_strain_rate.png` | ★ 그 속도 꼴 d̄^c = η ċ I |
| (34) | `eq_34_yield_surface_perfect_plasticity.png` | 항복면 (완전 소성) |
| (35) | `eq_35_yield_surface_linear_isotropic_hardening.png` | 항복면 (선형 등방 경화) |
| (36) | `eq_36_elastic_strain_rate.png` | 탄성 변형률 속도 |
| (37) | `eq_37_elastic_strain_rate_vol_dev_split.png` | 체적 · 편차 분리 |
| (38) | `eq_38_stress_update.png` | 응력 갱신 |
| (39) | `eq_39_stress_rotate_to_current_frame.png` | 현재 자리로 되돌림 |
| (40) | `eq_40_momentum_balance_no_body_force.png` | 외력 없는 운동량 식 |
| (41) | `eq_41_sound_speed.png` | 종파속 |
| (42) | `eq_42_quasi_static_equilibrium.png` | 준정적 평형 ∇·σ = 0 |
| (43) | `eq_43_timestep_momentum_balance_cfl.png` | 운동량 쪽 시간 간격 |
| (44) | `eq_44_timestep_diffusion.png` | 확산 쪽 시간 간격 |
| (45) | `eq_45_timestep_minimum.png` | dt = min(둘) |
| (46) | `eq_46_timestep_momentum_balance_example.png` | 예시 값 — ⚠ 6.8 × 10⁻¹¹ s (인쇄 그대로) |
| (47) | `eq_47_timestep_diffusion_example.png` | 예시 값 0.05 s |
| (48) | `eq_48_momentum_balance_with_constitutive_relation.png` | 운동량 식 + 탄성 관계 |
| (49) | `eq_49_acceleration_density_scaling.png` | ★ 밀도 스케일링의 근거 식 |
| 번호 없음 §2.1 | `eq_unnumbered_s2_1_normalized_concentration.png` | c = c_g/c_max |
| 번호 없음 §3.1 | `eq_unnumbered_s3_1_volumetric_stress_free_strain.png` | ε^c_vol = ε^c_ii/3 |
| 번호 없음 §3.1 | `eq_unnumbered_s3_1_pressure_definition.png` | p = −σ_ii/3 |
| 번호 없음 §3.1 | `eq_unnumbered_s3_1_compliance_concentration_derivative.png` | B_ijkl = dS_ijkl/dc |
| 번호 없음 §3.1 | `eq_unnumbered_s3_1_diffusivity_parameter_values.png` | D₀ · D_max · α · β · p_max 의 값 |
| 번호 없음 §3.3 | `eq_unnumbered_s3_3_deviatoric_stress.png` | σ̄_dev = σ̄ − 1/3 tr(σ̄) |

---

## 7. Post-processing

| 무엇 | 어떻게 (논문) | 우리에게 |
|---|---|---|
| 확산 풀이의 수렴 | 일곱 격자의 오차를 log–log 로 · 기울기 1 기준선을 겹침 (Fig. 1b) | 단위 시험 보고 꼴.  단 노름은 RMS (√(Σe²/N)) 로 정의하고 절대 오차도 함께 — 상대오차는 c → 0 인 입자에서 분모가 사라진다 [카드 추론] |
| 질량 스케일링의 점검 | 밀도가 10⁵–10⁶ 배 다른 두 계산을 같은 시각에 **반쪽씩 나란히** 붙여 그림 (Fig. 3 · 4) | 판 Mach 사다리의 그림 꼴로 좋다 (좌우 반쪽 대조) — 단 우리는 두께 · 판 반력 · 정착 응력을 숫자로 같이 낸다 |
| 구성식 · 손잡이 · 경계의 영향 | 농도로 칠한 입자 영역의 형상을 나란히 (Fig. 5–9) · 관심 부위에 손으로 타원 (Fig. 8 · 9) | 판정이 전부 눈 대조 — 우리 쪽 대조에는 결과 전에 등록한 관측량 (윤곽 · 높이 · 반력) 이 필요 |
| 실험과의 대조 | 전선 뒤 농도의 범위를 색 눈금에서 읽어 실험값 ∼0.67 과 말로 견줌 | 정량 검증으로 인용하지 않는다 |
| 한 바퀴 | 아홉 칸 연속 그림 (Fig. 10) · 첫 칸 ↔ 끝 칸의 모양 차이를 소성 변형이라 부름 | 단계 6 의 보고 꼴: 처음 · 최대 하중 · 끝의 윤곽을 겹치고 **잔류 높이 · 폭 · 부피를 숫자로** |
| 시각화 | 입자를 CPDI 영역 (찌그러진 육면체) 으로 그림 — 면 분할선이 곧 입자 경계 [카드 판독] | 입자 영역이 길게 늘어난 곳 = 해상도가 무너지는 곳을 그림에서 바로 본다 |
| 도구 | Uintah · 시각화 도구는 미인쇄 | — |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | Gritton 외 2017 | 우리 DEM (LIGGGHTS) | 우리 MPM (Taichi scaffold) |
|---|---|---|---|
| 이산화 | CPDI (입자 영역을 변형 구배로 추적) · Uintah · 양해 [카드 판독] | 구 입자 · 접촉 법칙 | MLS-MPM · 2차 B-spline · APIC · 양해 [우리 코드 판독 · 2953 · 3017 행] |
| 셀당 물질점 | 1D 검증 2 · 3D [미확인] | — | 방향당 2 (셀당 8) [우리 코드 판독 · 2361–2362 행] |
| 구성식 | hypoelastic–plastic — 회전 전 자리에서 변형률 속도의 덧셈 분해 (d^e + d^p + d^c) · J2 완전 소성 / 선형 등방 경화 | hooke/hysteresis (탄성 + 이력) | fixed-corotated 응력 + 로그 (Hencky) 변형률의 J2 반환 (SVD · 경화 없음) [우리 코드 판독 · 2954–2957 · 3019–3029 행] |
| 강성 ÷ 항복 | E/σ_Y ≈ 58 [카드 산술] · 실제 계수 그대로 (연화 없음) | — | E/σ_y ≈ 5.1 (E 1.53 · σ_y 0.30 GPa — 연화한 값) [우리 기록] |
| 하중 | 자유 변형률 (리튬화 η 0.56) · 외력 없음 | 판 압축 ≈ 300 MPa | 판 압축 ≈ 300 MPa |
| 준정적 장치 | 밀도 인위 증가 (시험 두 쌍 10⁵ 배 · 10⁶ 배 차 · 최대 2.33 × 10²⁴ kg m⁻³) · dt = min(dt_mb, dt_diff) | 판 속도 지정 | ρ = 1 규약 + dt = 0.4 dx/√M + 판 Mach (`--platen-mach`) [우리 코드 판독 · 2962 · 1928 · 3076–3077 행] |
| 격자 속도장 | 1 개로 읽힘 (접촉 서술 없음 · 기둥–기판 붙음) [카드 판독] | — | 1 개 [우리 코드 판독 · 2808 행] |
| 물체 사이 접촉 | 없음 (*affixed*) | 있음 (마찰 · 분리) | 없음 (붙음) — 판 · 벽 · AM 은 노드 조건 |
| 추가 장 | 정규화 농도 (입자에 실음 · 격자에서 확산 · 응력과 양방향) | 없음 | 없음 (수송은 굳은 구조의 사후 풀이 = STEP3) |
| 하중 제거 | 탈리튬화 한 바퀴 (Fig. 10) · 값 없음 | 있음 | 부분 |
| 검증 | 1D 확산 해석해 · 나머지 눈 대조 | 실험 기공 · 접촉 겹침 | 실험 기공 (보정) · DEM 두께 대조 |
| 차원 · 규모 | 3D · 기둥 1 개 + 기판 · 입자 수 미인쇄 (작은 기둥 ≈ 5 × 10⁴ [판독 · 카드 산술]) · CPU 9 코어 | 3D 10⁴–10⁵ 입자 | 3D 10⁷–10⁸ 물질점 (GPU) [우리 기록] |
| 수송 | 확산 (변형과 함께) | 접촉망 | 복셀 (STEP3) |

### 8-2. 질량 스케일링 ↔ 우리 ρ = 1 규약 · 판 Mach [카드 산술 · 전부 논문 밖]

- **같은 장치의 두 표현**: 논문은 밀도를 올려 종파속을 낮춘다 (c_s ∝ ρ^(−1/2)).  우리는 밀도를 1 로 두고 탄성 계수를 GPa 로 넣어 시간의 단위가 임의가 되므로 (코드 주석 *"box/t.u., ρ=1 규약"* [우리 코드 판독 · 3073 행]), 뜻이 있는 양은 "움직이는 속도 ÷ 파속" 하나다.
- **같은 양으로 읽은 논문의 두 시험** (§3-4): 겉면 속도 ÷ 종파속 ≈ 5 × 10⁻⁵ ↔ 1.6 × 10⁻² (Fig. 3) · 6 × 10⁻⁶ ↔ 6 × 10⁻³ (Fig. 4) [판독 · 카드 산술].  우리 판 Mach 는 0.01–0.03 (종파 기준) [우리 기록] — 논문이 "눈으로 같다" 고 본 범위의 위쪽 끝과 겹친다.
- **무엇이 같았는가**: 논문이 본 것은 형상 (과 농도 색) 뿐이다 — 윤곽 높이 차 ≤ 1 % [판독].  우리 실측은 같은 방향의 더 자세한 판이다: 같은 스트로크면 기하는 소수점까지 같고 (`porosity 15.525` · `thickness 121.703`) 정착 응력 ÷ 목표만 0.6032 → 0.6577 (+9.0 %) 로 움직였으며 (Mach 0.03 → 0.01), 다른 침대에서는 σ +4.8 % 였다 [우리 기록 — 프로젝트 정본 09-22 · 08-06 절].  ⇒ **질량 스케일링 (재하율) 의 흔적은 형상이 아니라 응력에 먼저 난다** — 형상 비교만으로 준정적을 판정한 이 논문의 시험은 우리 판 반력 판독의 근거가 못 된다.
- **전단파 기준**: 논문 재료는 c_s/c_T = 1.87 (ν 0.30) 인데 우리 SE 는 c_P/c_S = 7.1 (ν 0.49) 이다.  소성 (등체적) 응답은 전단파로 퍼지므로, 같은 종파 기준 Mach 라도 우리 쪽이 전단 기준으로 3.8 배 빠르다 (7.14/1.87).
- **"확산이 시간 간격을 정한다" 의 실제**: dx = 10 nm 로 두면 밀도 2.33 × 10²⁴ 에서도 c ≲ 0.78 인 동안은 운동량 쪽이 시간 간격을 정한다 (§3-4).  설명과 실제 지배 조건이 다를 수 있다 — 우리 MPM 이 요청 dt · CFL 상한 · 실제 dt 를 산출물에 함께 적는 까닭과 같은 부류 (`dt_effective` · `dt_cfl_cap` · `dt_requested` [우리 코드 판독 · 1734–1737 행]).

### 8-3. 전이되는 것 / 안 되는 것

- ✅ **질량 스케일링의 근거 식과 시험 꼴**: 식 (42) · (48) · (49) + "스케일링 세기가 크게 다른 두 계산을 같은 물리 시각에 나란히" (Fig. 3 · 4).
- ✅ **MPM 위의 스칼라 확산 풀이** (식 4–8) 와 그 1D 검증 문제 (식 9–13) — 흐름 밖 (변형과 함께 푸는 수송).
- ✅ **자유 변형률을 구성식에 넣는 꼴** (식 25 · 32 · 33 · 36) 과 그 함정 (속도 꼴 ↔ 로그 변형률 · §3-5).
- ✅ **저자의 고백 문장**: 미끄럼 ↔ 기판 변형을 가를 수 없다 (p.17) · 입자 표면 넓이 고정은 타당하지 않다 (p.7) · 손잡이에 따라 변형이 달라진다 (p.16) · 소성은 이력 의존이라 하중 속도가 모양을 바꾼다 (p.15).
- ✅ **한 속도장 '넣었다 빼기' 의 정성 그림** (Fig. 9 · 10): 붙은 계면 · 끌려 올라온 턱 · 부피는 회복 · 모양은 비회복.
- ❌ 규소 · 기판의 물성 · 확산계수 · η · 유속 · 280 % — 전부.  **LPSCl · NCM 값으로 쓰지 않는다.**
- ❌ 계산 비용 (CPU · CPDI · Uintah · 입자 수 미상) 의 우리 GPU MLS-MPM 으로의 전이.
- ❌ 해상도 규칙 — 지름당 셀 수 · 셀당 입자 수가 인쇄돼 있지 않다 ([판독] 지름당 입자 영역 ≈ 40 은 규칙이 아니라 한 사례).
- ❌ "MPM 이 큰 소성 변형을 정확히 푼다" 는 지위 — 이 논문에는 역학의 정량 검증이 없다.
- ❌ 접촉 · 마찰 · 분리 · 압밀 · 기공 · 탈압 곡선 — 없다.
- ⚠ 인쇄된 식 가운데 (13) · (15) · (18) 의 번호 칸 · (21) · (46) 은 그대로 옮기지 않는다 (§12).

### 8-4. frame 판정

- **frame [5] (분업)**: 이 논문은 MPM 쪽 절반 (연속체 소성 · 진짜 형상 변화 · 큰 변형) 에 **화학 장**을 더한 것이다.  DEM 쪽 절반 (접촉망 · 패킹 · 퍼콜레이션 · 접촉 저항) 은 통째로 없다 — 기둥 하나라 필요도 없다.  분업은 그대로이고, MPM 이 "변형과 함께 장 하나를 더 풀 수 있다" 는 선례가 하나 는다.
- **frame [4] (교차 맞춤 금지)**: 실험에 맞춘 값이 없으므로 충돌은 없다.  반대로 **이 논문을 우리 MPM 역학의 검증 근거로 인용할 수도 없다** — 방법의 선례로만.
- **frame [1]/[2] (연화)**: 중립.  이 논문은 실제 계수 (E ≈ 81 GPa) 를 그대로 쓴다 — 물체가 하나라 입자 재배열이 없고, 연화가 대신할 빠진 기전이 없기 때문이다.  "연화 = 재배열의 대리" 라는 우리 틀과 어긋나지 않는다 [카드 추론].

---

## 9. 깊은 통찰

① **준정적의 근거를 '식' 으로 적은 것은 가져오고, 판정 수준 (눈) 은 가져오지 않는다.**  식 (42) (확산의 시간 척도에서 ∇·σ = 0) 과 식 (49) (밀도는 가속도에만 들어간다) 는 명시적 MPM 으로 느린 과정을 풀 때 질량을 키워도 되는 까닭을 가장 짧게 적은 꼴이다.  그러나 그 타당 범위는 논문이 재지 않았다 — 운동 에너지 비도, 응력 비교도 없다.

② **스케일링의 흔적은 형상보다 응력에 먼저 난다.**  논문의 두 쌍은 윤곽이 ≤ 1 % 로 같았고 [판독], 우리 실측도 기하는 같고 응력만 달랐다 (§8-2).  두 자료가 같은 방향을 가리킨다 → 준정적 사다리의 판정량에는 판 반력 · 정착 응력이 들어가야 하고, "두께가 같다" 는 통과 기준이 못 된다.

③ **저자의 설명 ('확산이 시간 간격을 정하게') 과 실제 지배 조건은 다를 수 있다.**  dx 10 nm 가정으로는 가장 무거운 밀도에서도 낮은 농도 구간은 여전히 탄성파가 시간 간격을 정한다 [카드 산술].  27,472 걸음이라는 숫자만으로는 어느 쪽이 지배했는지 알 수 없다.  ⇒ 시간 간격은 "요청 · 상한 · 실제" 를 산출물에 남겨야 뒤에서 읽을 수 있다.

④ **붙은 계면으로는 '미끄럼인가 변형인가' 를 가를 수 없다 — 저자가 그렇게 적었다.**  실험의 바닥 반경 팽창 ∼20 % 를 두고 *"It is unknown if …"* 라 쓰고는 기판을 변형시키는 쪽만 계산했다.  한 속도장 MPM 은 두 가설 가운데 하나를 **구조적으로** 지운다.  우리 MPM 의 SE–AM · SE–판 계면도 같다 → 판 · 벽 · AM 자리의 미끄럼 · 분리 규칙 (후보 A′-0) 은 정확도 개선이 아니라 **물을 수 있는 질문의 범위**를 넓히는 일이다.

⑤ **'넣었다 뺀 뒤' 를 한 속도장으로 돌리면 — 부피는 돌아오고 모양은 안 돌아오며 계면은 안 열린다.**  Fig. 10 의 끝 상태는 높이 ×1.35 · 폭 ×0.98 · 부피 ≈ ×1.1 [판독] 이고 기판에는 턱이 남는다.  수축하는 기둥은 기판을 놓지 못하고 끌고 온다.  우리 단계 6 (탈압) 에서 판이 물러날 때 SE 가 판 · AM 에서 떨어지지 못하는 것과 같은 그림이다 — 되돌아옴의 크기를 재기 전에 "무엇이 떨어질 수 있는가" 부터 정해야 한다.

⑥ **자유 변형률을 속도 꼴로 넣으면 계수의 뜻이 바뀐다.**  η = 0.56 은 선형 신장 (1.56³ = 3.80) 으로 고른 값인데, 식 (33) 처럼 변형률 속도에 곱해 적분하면 exp(3η) = 5.37 이 된다 [카드 산술].  그림 판독 (×4.0–5.0) 은 그 사이다.  논문은 이 차이를 말하지 않는다.  ⇒ 열 · 화학 · 상변화 팽창을 MPM 에 넣을 때는 "구속 없는 균일 팽창이 지정한 부피비를 내는가" 를 첫 단위 시험으로 둔다.

⑦ **소성은 경로 의존 — 같은 끝 상태가 같은 모양을 뜻하지 않는다.**  유속 10 배 차이가 완전 리튬화 뒤에도 남는다 (Fig. 7).  우리 압밀에서도 "같은 끝 압력" 은 상태를 정하지 못한다 — 판 속도 · 유지 · 순서를 결과 전에 고정해야 하는 까닭의 그림 한 장이다.

⑧ **손잡이가 다섯인데 맞춘 대상이 없다.**  α · β · p_max · 유속 크기 · η (+ σ_Y · 소성 계수).  저자 스스로 *"the deformation behavior can vary based on what tuning parameters are chosen"* 라 쓴다.  우리 조건 R5 (맞추는 값은 모델마다 하나) 의 반대편 사례 — 손잡이를 늘리면 무엇이든 그릴 수 있고, 그래서 정성 일치는 근거가 약하다.

⑨ **큰 변형을 견디는 것과 정확한 것은 다르다.**  CPDI 를 고른 까닭은 *"its ability to handle large deformations"* 한 줄이다.  입자 영역이 길게 찌그러진 곳 (Fig. 7b) 의 응력이 믿을 만한지는 아무도 보지 않았다.  우리 MLS-MPM 은 입자 영역을 추적하지 않으므로 [우리 코드 판독 — 2차 B-spline 가중만 씀 · 2953 행], 늘어나는 구역 (SE 가 틈으로 밀려 들어가는 자리) 에서 물질점 사이가 셀 크기보다 벌어지면 수치적으로 끊길 수 있다 [카드 추론 · `devaucorbeil2020_…` 카드가 CPDI 의 장점으로 적은 *numerical fracture* 의 반대편] → 물질점 간격 ÷ dx 를 감시량으로.

⑩ **축대칭으로 줄일 수 있는 문제를 3D 로 풀었다 — 그리고 2D 와 견주지 않았다.**  원문은 기둥이 *"lends itself to a 2D axisymmetric numerical solution"* 이라 적는다.  우리 2D 벤치마크 (단계 2 · 3) 에서 입자 하나 압축 (U1) · 단단한 구를 소성 블록에 누르기 (U3) 는 축대칭 문제다 — 평면 변형 대신 **축대칭 MPM** (이 논문 ref. [41]) 을 쓰면 2D 값을 3D 로 옮기는 문제의 일부가 사라진다 [카드 추론].

⑪ **표면 넓이를 처음 값으로 고정하면 걸리는 양이 틀린다 — 저자 고백.**  *"not a valid assumption … similar to prescribing a slightly lower flux than intended"*.  큰 변형에서 표면 · 계면에 걸리는 양 (유속 · 견인력 · 피복 넓이) 은 변형 구배로 넓이를 갱신해야 한다.  우리 MPM 의 피복 · 계면 넓이 정의에도 같은 주의가 걸린다 [카드 추론].

⑫ **'검증' 이라는 낱말의 무게.**  초록은 *"validation tests with experimental results show the accuracy of the approach"* 라 쓰지만 본문의 대조는 정성 문장이다.  오차 노름도 인쇄대로면 수렴 차수를 반 차수쯤 부풀린다 (식 15).  이 논문을 인용할 때는 "방법을 보였다" 까지만 쓴다.

---

## 10. [DEM 우선 (수영)] — 후보별 함의 + 구체 행동

| 후보 · 조건 | 이 논문의 함의 | 판정 |
|---|---|---|
| **A** (MPM · AM = 움직이는 강체 · SE 한 속도장) | 한 속도장으로 큰 소성 변형과 '넣었다 빼기' 를 끝까지 돌릴 수 있음을 보인다.  값: 계면이 붙는다 (Fig. 9 · 10) | ✅ 실행 가능성의 선례 · ⚠ 계면 물리는 빠짐 |
| **A′-0** (판 · 벽 · AM 자리에만 접촉 규칙) | 방법은 주지 않는다.  **필요성의 저자 문장**: 미끄럼 ↔ 기판 변형을 가를 수 없다 (p.17) | ↗ 필요성 근거 |
| **A′** (입자마다 속도장) | 관련 서술 없음 | — |
| **B** (입자마다 유한요소 + 접촉) | FEM 이 리튬화 계산의 *"popular choice"* 라는 소개뿐 (p.3) — 비교 계산 없음 | 중립 |
| **C / C′ / D0** (접촉 법칙 DEM) | 관련 없음 (DEM 언급 0) | — |
| **M0** (균질화 압밀) | 관련 없음 | — |
| 조건 **R4** (탈압 · 되돌아옴) | 탈리튬화 = 자유 변형률 제거의 사례.  값 없음 · 계면 열림 없음 | ⚠ 그림만 |
| 조건 **R6** (SE 입자 형상 변형) | 진짜 형상 변화 (높이 ×3.4) 를 CPDI 로 — 해상도 · 정확도 근거는 없음 | ✅ 정성 |
| 조건 **R2** (미끄럼 · 분리) | 없음 (붙음) | ✗ |
| 조건 **R5** (맞추는 값 하나) | 손잡이 다섯 · 맞춘 대상 없음 = 반면교사 | ⚠ |

**구체 행동 (싼 것 → 비싼 것 · 전부 [카드 추론] · 결과 전 등록 대상)**
1. **준정적 사다리의 판정량에 응력을 넣는다 (단계 2 · U0)** — 판 Mach 세 단에서 두께와 함께 판 반력 · 정착 응력을 견준다.  이미 하는 일의 문서화이고, 이 논문 (식 42 · 49 · Fig. 3 · 4) 은 "장치의 선례 · 형상만 본 사례" 로 인용한다.
2. **물질점 간격 감시 (U1 · 단계 4)** — 늘어나는 구역에서 물질점 최근접 거리 ÷ dx 의 분포를 산출물에 적는다.  1 셀을 넘으면 수치적 끊김 경고.  CPDI 를 쓰지 않는 우리 이산화의 대가를 숫자로.
3. **'한 속도장으로 눌렀다 떼기' 의 기준선 (U3 · U4 · 단계 6)** — 단단한 구 + 소성 블록에서 붙은 계면이 떼는 쪽으로 블록을 끌고 오는지 (Fig. 9 · 10 의 턱) 를 먼저 기록하고, 분리 규칙을 넣은 팔과 겹친다.
4. **2D 벤치마크에 축대칭 판을 검토 (단계 2 · U1 · U3)** — 축대칭이면 구 하나 · 구–블록 문제가 그대로 3D 문제다.
5. **(흐름 밖) AM 부피 변화를 MPM 에 넣는다면** — 자유 변형률은 곱셈 꼴 (탄성 · 소성 · 자유 부분) 로 넣고, 계수는 선형 ↔ 로그를 구분한다.  첫 단위 시험 = 구속 없는 균일 팽창의 부피비.
6. **(흐름 밖) 변형과 함께 푸는 수송을 넣는다면** — 식 (4)–(8) + 1D 해석해 시험 (식 9–13 · t 를 넣은 꼴) 부터.  오차는 RMS 와 최대 절대 오차로.
7. **표면 · 계면 넓이는 변형 구배로 갱신** — 처음 값 고정은 저자 스스로 타당하지 않다고 적은 가정이다.

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | 입자의 표면 넓이를 처음 값으로 고정 — 타당하지 않음 · 유속이 의도보다 작게 걸림 | §2.3 p.7 *"A current assumption that is probably less valid, and will be fixed in future work, is that the surface area associated with each particle remains constant.  Inspection of the subsequent results show that this is not a valid assumption, but given the relatively uniform expansion of the object that we are currently interested in, this is similar to prescribing a slightly lower flux than intended.  In future work, the particle area will be evolved according to the particle deformation gradient"* |
| 2 | 포화 제한식은 임시 | §2.3 p.7 *"While the equation above is ad hoc, this reflects physically meaningful behavior."* |
| 3 | 압력 기울기가 리튬을 미는 항을 넣지 않고 경험식을 택함 — 1차 근사 | §3.1 p.8 *"The empirical based approach is able to approximate the behavior of the lithiation of non-lithiated amorphous silicon and provides a good first approximation of the diffusion process."* |
| 4 | 변형률 속도는 Hencky 변형률 속도의 근사 (주축 회전이 작을 때) | §3.2 p.9 (§4-5 의 인용) |
| 5 | 밀도 스케일링의 확인은 정성 | §4.2.1 p.13–14 *"qualitatively the variations between the simulations are small"* · *"it can be seen qualitatively that there is very little variation"* |
| 6 | 손잡이에 따라 변형 거동이 달라진다 | §4.5 p.16 *"the deformation behavior can vary based on what tuning parameters are chosen"* |
| 7 | 바닥 팽창의 원인 (미끄럼 ↔ 기판 변형) 을 모른다 · 붙음을 가정 | §4.6 p.17 (§0 의 인용) |
| 8 | 탈리튬화 중 확산계수를 고정 | §4.7 p.19 *"During the delithiation phase diffusivity was fixed at the final diffusivity value during the lithation phase."* |
| 9 | 파괴가 없다 | §5 p.20 *"In future work methods for modeling fracture need to be introduced into the Uintah framework in order to better simulate the full physical effects of lithiation and delithation on a silicon anode."* |
| 10 | 전기화학이 없다 (전압 → 유속 근사) | §5 p.20 *"In this current work the affects of an applied voltage have been approximated using the flux boundary condition.  Future work needs to be done to implement the full electrochemistry in to the numerical models."* |
| 11 | 차원을 줄이면 기하의 특징을 잃는다 (남의 1D 모형에 대한 말) | §1 p.3 (§0-2 의 인용) |

저자가 **적지 않은** 한계 (카드가 본 것 — §12 와 겹침): 역학 · 결합 · 3D 수렴의 검증 부재 · 접촉 부재 · 응력 결과 부재 · 재현에 필요한 수치의 누락 · 부피 팽창률의 미대조.

## 12. 불확실 · PDF 에 없는 것 · 인쇄 어긋남

**없는 것** — §3-7 표.  요약: 3D 격자 · 입자 수 · 밀도 · 시간 간격 · 물리 시간 · 유속 단위 · 응력 결과 · 물성 출처 · 경계를 거는 방법.

**인쇄 어긋남** (전부 [카드 판독] — 식 그림은 인쇄 그대로 잘랐다)

| # | 자리 | 인쇄 | 카드의 읽기 |
|---|---|---|---|
| 1 | 식 (13) · p.5 | e^(−Dπ²n²) | 지수에 t 가 빠졌다 — 해라면 e^(−Dπ²n²t).  Fig. 1a 는 t = 0.25 · D ≈ 0.1 로 맞는다 [판독] |
| 2 | 식 (15) · p.6 | error = √(Σ e_p²)/N · 본문 *"L2 norm of the relative error"* | N 으로 나누면 RMS ÷ √N — 수렴 차수가 ½ 만큼 좋아 보인다 (§3-3) |
| 3 | 식 (18) 의 번호 칸 · p.7 | "(18rate of change of the elastic)" | 조판 오류 — 번호는 18 |
| 4 | 식 (21) · p.8 | 첫 항 계수 Dγ/(1 − c) | γ 가 상수면 D/(1 − c) |
| 5 | 식 (46) · p.12 | dt_mb = dx_cell/c_s = 6.8 × 10⁻¹¹ s · 이어서 *"10¹¹ time step integrations … to reach 6.8 s"* | 10⁻⁸ m ÷ 6.8 × 10³ m s⁻¹ = 1.47 × 10⁻¹² s · 6.8 s 에는 4.6 × 10¹² 걸음.  결론 (다루기 어렵다) 은 그대로 |
| 6 | Fig. 3 · 4 캡션 | *"(b), (c), (f) density of …"* | (b), (d), (f) |
| 7 | Fig. 5 · 6 캡션 | *"(a), (c) Are images …"* · *"(a), (d) Series …"* · *"(e), (h) Series …"* | 범위 (a)–(c) · (a)–(d) · (e)–(h) 의 뜻 |
| 8 | 식 (35) · p.10 | 소성 계수 기호 K | 식 (30) 의 체적계수 K 와 같은 글자 (값은 1.15 ↔ 67 GPa) |
| 9 | σ̄_dev 정의 · p.10 | σ̄ − 1/3tr(σ̄) | 단위 텐서 I 가 빠짐 |
| 10 | 식 (17) · p.7 | log | 밑 미인쇄 (자연로그 0.982 ↔ 상용로그 0.9999 에서 유속 0) |
| 11 | 식 (31) · p.10 | σ̇ (점만 보임) | 회전 전 응력 σ̄ 의 변화율 |
| 12 | §2.2 · p.5 | *"with the data again being captured at simulation time 0.25"* | 'again' 이 가리키는 앞 문장이 없다 (지워진 서술의 흔적) |
| 13 | 초록 ↔ 본문 | *"validation tests with experimental results show the accuracy of the approach"* | 본문의 실험 대조는 정성 문장뿐 (§0 ④) |
| 14 | §4.6 본문 ↔ Fig. 8 | 타원 표시를 Fig. 9 (a) · (b) 에서만 언급 | Fig. 8 (a) · (b) 에도 같은 타원이 있다 (본문 설명 없음) |
| 15 | §4.2.1 · p.14 ↔ Fig. 4 | *"despite the five orders of magnitude difference in density"* | 인쇄된 두 밀도 2.33 × 10¹⁸ · 2.33 × 10²⁴ kg m⁻³ 는 10⁶ 배 (여섯 자리) 차 — 본문 · 캡션 모두 이 두 값 |

**서지**: 1저자 메모와 원문이 같다 (제목 · 저널 · 권 · 논문 번호 · 연도 · DOI).  공저자 6 인은 원문에서 확인 (§2).

## 13. 인용 가능 문장 (덱 · 원고용)

- "명시적 MPM 으로 확산 같은 느린 과정을 풀 때는 탄성파 시간 간격이 병목이어서, 준정적 평형을 근거로 밀도를 인위로 올려 시간 간격을 키운 선례가 있다 (Gritton et al., Modelling Simul. Mater. Sci. Eng. 25, 045005, 2017, §4.1–4.2)." — 한정어: 그 논문의 확인은 형상의 정성 비교뿐이다.
- "접촉 알고리즘이 없는 MPM 에서는 서로 다른 물체의 계면이 붙어 있어, 계면 미끄럼과 상대 물체의 변형을 구분해 시험할 수 없다 (같은 문헌 §4.6 — 저자 스스로 *unknown* 이라 적음)."
- "MPM 에서 스칼라 장의 확산은 운동량 풀이와 같은 입자–격자 연산 (질량 가중 사상 · 격자 기울기 · 유속 발산 · 입자 갱신) 으로 풀 수 있다 (같은 문헌 §2.1, 식 4–8)."
- "소성 재료의 끝 모양은 하중 속도에 따라 달라진다 (같은 문헌 §4.4, Fig. 6–7)." — 규소 나노기둥의 리튬화 사례라는 한정어와 함께.

## 14. 기법 미니 용어집

- **CPDI (convected particle domain interpolation)** — 입자 영역을 변형하는 평행육면체로 두고 형상함수를 그 영역에서 평균하는 MPM 변종 (설명은 `homel2017_…` 카드의 것 — 이 논문은 이름과 ref. [38] 만 적는다).
- **Uintah** — 이 논문의 코드 기반인 계산 틀 (ref. [39] · MPM component).  저자 전원이 University of Utah 소속이다.
- **정규화 농도 c** — 현재 몰농도 ÷ 포화 몰농도 (Li 3.75 : Si 1).  0–1.
- **리튬화 전선 (lithiation front)** — 리튬화된 규소와 순수 비정질 규소 사이의 날카로운 농도 경계.
- **hypoelastic–plastic** — 응력의 변화율을 변형률 속도로 적는 (속도 꼴) 탄소성 모형.  변형률 속도를 탄성 · 소성 · 자유 부분으로 **더해** 나눈다.
- **회전 전 자리 (unrotated configuration)** — 극분해 F = RU 의 회전 R 을 되돌린 자리.  여기서 응력을 갱신하면 강체 회전에 대해 객관적이다.
- **자유 변형률 (stress-free strain · eigenstrain)** — 응력 없이 생기는 변형 (열팽창 · 리튬 삽입).  여기서는 η (c − c₀) I.
- **Larché–Cahn 화학 퍼텐셜** — 응력 받는 고체 안 손님 원자의 화학 퍼텐셜 (농도 항 + 정수압 항 + 탄성 계수의 농도 의존 항).
- **질량 (밀도) 스케일링** — 명시 풀이의 안정 시간 간격을 키우려고 밀도를 인위로 올리는 것.  준정적 문제에서만 정당하다.
- **CFL 시간 간격** — 한 걸음에 파동이 한 셀을 넘지 않게 하는 조건 (식 43).
- **유속 제한 계수** — 농도가 1 에 다가가면 표면 유속을 줄이는 임시 계수 (식 17).

## 15. 관련 카드

- `devaucorbeil2020_mpm_after_25_years_review` — 이 논문을 Si 음극 화학–역학 MPM 으로 소개한 리뷰 (MPM 변종 표 · 공개 코드 목록에 Uintah).
- `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — 이 논문에 없는 MPM 접촉 (다물체 · 견인력 분리 · 장 2 개 분할).  Guilkey 는 2001 판의 공저자다.
- `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MLS-MPM 이산화의 원전 · 강체 결합.
- `nezamabadi2022_mpm_cd_plastic_particle_compaction` (소성 원판) · `nguyen2017_mpm_bpm_deformable_particle_compaction` (탄성 입자 · 그 전신) — MPM 으로 변형 입자의 **압밀**까지 간 2D 선례 (이 논문에 없는 다입자 · 접촉).
- `bardenhagen2005_mpm_foam_densification_simulation` — 이 논문이 "큰 변형에 성공한 MPM" 의 근거로 든 ref. [31] (발포체 치밀화 · 같은 날 반입).  그 카드로 확인: 탄성 뼈대 · 붙는 (no-slip) 접촉 · 정량 검증은 꽉 찬 블록 해석해 1 건 (끝 오차 ≈ 5 %) · 준정적 판정은 절반 속도 런과의 눈 대조 — "성공" 의 범위는 거기까지다.
- `bucci2017_chemomech_failure_assb_cycling_czm` (FEM + 응집 영역) · `tian2020_electrochemo_mechanical_stress_assb` (연속체 화학–역학 FEM) · `kim2023_chemomech_failure_highstrain_anode` (실험 + FEM) — 화학–역학 결합을 FEM 쪽에서 다룬 카드.
- `stomakhin2013_mpm_snow_elastoplastic` — 우리 MPM 탄소성 갱신 (곱셈 꼴) 의 계보 — 이 논문의 덧셈 (속도) 꼴과 대비.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

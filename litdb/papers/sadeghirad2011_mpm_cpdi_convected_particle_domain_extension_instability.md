# MPM 이 큰 인장에서 끊기는 문제 (extension instability) 를 입자 영역을 변형 경사 F 로 실어 나르는 평행사변형 (CPDI) + 그 모서리 값의 Q4 보간 기저로 푼 원전 — 2D 평면 변형률 · 탄성 neo-Hookean · 동적 시험 다섯 (MMS 수렴 두 건 · 자중 막대 평균 신장 ×2.8 → ×9.7 · 외팔보 큰 회전 · 45° 돌린 영역) ★★ 신장 문턱 숫자 · B-spline · 소성 · 접촉 · 3D · 비용 수치는 없다 — Sadeghirad, Brannon, Burghardt (Int. J. Numer. Meth. Engng 2011)

> slug `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` · DOI `10.1002/nme.3110` · type `MPM (명시적 GIMP 계열 · USL · 입자 영역 = 평행사변형을 전체 변형 경사 F 로 실어 나름 (CPDI) + 표준 격자 기저를 영역 네 모서리에서 Q4 보간한 대체 기저로 φ_ip · ∇φ_ip 를 닫힌 꼴로 · 2D 평면 변형률 · 압축성 neo-Hookean (소성 없음) · 동적 · 검증 = MMS 해석해 2 건 (오차 수렴) + 자중 막대 · 외팔보 · 45° 돌린 영역에서 표준 MPM · uGIMP · cpGIMP · FEM 과 비교 · 물체 사이 접촉 알고리즘 없음)` · PDF `fa9d76bf-15._A_convected_particle_domain_interpolation_technique_to_extend_applicability_of_the_material_point_method_for_problems_involving_massive_deformations.pdf` (22 쪽 = 학술지 1435–1456 · 글자 층 온전 · 식의 그리스 문자는 글자 층에서 빠져 렌더로 옮김 · 그림 19 장 전부 벡터 · 표 0 · 보충 자료 없음) · digested `2026-11-12` · status ✅
>
> ⚠ **먼저 읽을 것** — ① 재료는 **검증용 가상 재료**다: 압축성 neo-Hookean (식 30) · E = 1 × 10⁶ 또는 1 × 10⁷ Pa · ν 0 · 0.3 · ρ₀ 1000 · 1050 kg/m³ — **LPSCl · NCM 이 아니다.  절대값 전이 0 건.**  가져오는 것은 **불안정의 정의 · CPDI 식 · 시험 문제 꼴 · 방법끼리의 상대 비교 수치 · 저자 진술**뿐이다.
> ② **2D 뿐이다** — *"for clarity, however, only two-dimensional case studies are described in this paper"* (p.1436).  평면 변형률이다 (식 A6 F_zz = 1 · 식 A7 P_zz = λ ln(F_xx F_yy) ≠ 0 [카드 판독]).  3D 는 *"it should be self-evident how to generalize the techniques to 3D"* (p.1452) 한 문장 · 3D 시험 0 건.  gritton2017 (Uintah) · homel2017 (GEOS) 가 쓴 3D CPDI 는 이 논문 밖의 구현이다.
> ③ **소성 · 물체 사이 접촉 알고리즘 · 압밀 · 준정적 · 하중 제거가 없다.**  하중은 MMS 체적력 (식 33–34) 과 t = 0 의 계단 중력뿐 (전부 동적).  'plastic' 은 서론의 응용 목록과 참고문헌 제목에만 · 'DEM' · 'discrete element' · 'friction' · 'unload' · 'quasi' 0 회 · 'contact' 본문 2 회 (*"no-slip contact between bodies automatically"* p.1436 · *"remain 'in contact' even when they are far from each other"* p.1446 · 그 밖 2 회는 참고문헌 제목) [카드 전문 검색].
> ④ **"어디까지 늘어나도 되는가" 의 숫자 문턱은 없다.**  원문의 기준 = 정의 (*"regions of influence no longer overlap"* · p.1440) + 그림 판정 (계산이 끝까지 갔는가 · 영역에 틈 · 겹침이 생겼는가) + *"if sufficient refinement is used"* 면 안정 (결과 미제시 · p.1448).  **계산 비용 · 시간 수치도 0 건** (*"computational cost comparable with original GIMP"* · p.1440 말뿐).
> ⑤ **오차 노름 (식 27) 은 √(ΣΣ e²) 를 제곱근 밖에서 N_t × N_p 로 나눈다** → 그림 (Fig. 4 · 7) 의 기울기는 RMS 수렴 차수보다 ≈ 1.5 크다 [카드 산술 · N_t = T/Δt 가정 · §3-2] — 같은 Utah 계열 `gritton2017_…` 식 (15) 의 ÷ N 과 같은 부류의 함정.
> ⑥ 인쇄 어긋남이 있다 (식 25 의 괄호 · 식 27 아래 문장의 N_t ↔ N_p 뒤바뀜 · Fig. 5 · 8 의 시각 라벨이 인쇄된 주기 T = 0.02 s 밖 · Fig. 2 의 r 화살표 ↔ 식 26) — §12 에 모았다.  식 그림은 **인쇄된 그대로** 잘랐다.
> ⑦ 표지: `인쇄` = 본문 · 캡션에 적힌 값 · `[판독]` = 그림에서 읽은 값 (전부 **PDF 벡터 경로 좌표** — 원자료 `litdb/figures/<slug>/digitized.csv` 922 행 = Fig. 4 · 7 표지 + 다섯 곡선의 시간 표본 · 최소 · 끝점 + Fig. 10 · 12a 의 영역 가로선 높이 · 줄 간격 189 행 · 방법은 그 파일의 method 열) · `[카드 산술]` = 인쇄 · 판독 값의 산술 (식 병기) · `[카드 판독]` = 인쇄 어긋남 · 모호한 곳에 대한 카드의 읽기 · `[카드 추론]` · `[다른 카드]` (slug 병기) · `[우리 기록]` = 논문 밖 판단 · `[미확인]` = 논문에 없음.  쪽 = **학술지 쪽** (PDF 쪽 = 학술지 쪽 − 1434) · 크롭 파일 이름의 p<n> 과 figures.json 의 page 는 PDF 쪽이다.
>
> 짝 카드: `gritton2017_mpm_chemomechanical_coupling_silicon_anode` · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — CPDI 로 3D 계산을 한 두 카드 (둘이 가리키던 원전이 이 카드).  `devaucorbeil2020_mpm_after_25_years_review` — 변종 표에서 CPDI 를 한 줄로 소개한 리뷰.  `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MPM 이산화 (MLS-MPM · 2차 B-spline) 의 원전 — 이 논문이 다루지 않는 기저.  `bardenhagen2000_…` · `bardenhagen2001_…` — 이 논문에 **없는** 다물체 마찰 접촉 · 분리의 원전.  `bardenhagen2005_mpm_foam_densification_simulation` — GIMP 로 큰 압축 (치밀화) 까지 간 선례.

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

[DEM 우선 (수영)] 의 MPM 은 2차 B-spline MLS-MPM 이다 [다른 카드 — `gritton2017_…` §8-1 · `hu2018_…`].  SE 를 300 MPa 로 누르면 SE 가 AM 사이 틈으로 밀려 들어가며 물질점이 국소적으로 크게 늘어나는 자리가 생긴다 — *"그 이산화는 어디까지 늘어나도 수치적으로 버티는가"* 를 묻는 출발점이 이 논문이다.  읽을 까닭이 넷이다.

**(1) "큰 신장에서 MPM 이 끊긴다" 의 원전 정의와 원인이 세 줄로 있다.**

> *"Another interesting feature of traditional MPM is that this method enforces no-slip contact between bodies automatically without any further computational costs.  However, the MPM suffers from a 'cell crossing instability' for problems involving large displacements.  This instability occurs whenever particles cross boundaries of any cell in the computational background grid and is due to the lack of smoothness of the grid basis functions used as the interpolation and mapping functions in the MPM."* (§1 · p.1436)

> *"The standard MPM is subject to a so-called ringing instability caused by a sudden jump in basis function gradient as a particle crosses a cell boundary.  The uGIMP suffers from the extension instability when the particles become separated to the extent that their regions of influence no longer overlap.  The cpGIMP rectifies the extension instability if the direction of loading is aligned with the rectangular grid.  However, the results are not indifferent to a frame change."* (§2.2 · p.1440)

원문 낱말은 **extension instability** (10 회 · 키워드 · 감사의 글 포함 · 초록은 *instability in extension*) 이다 — *numerical fracture* 는 0 회 [카드 전문 검색].  저자는 SPH 의 *tensile instability* 와 다른 것이라고 감사의 글에 적었다 (p.1454).

**(2) CPDI 의 식이 전부 있다** — 영역 추적 (식 21: r₁ⁿ⁺¹ = Fₚⁿ⁺¹ r₁⁰ · r₂ⁿ⁺¹ = Fₚⁿ⁺¹ r₂⁰) · 대체 기저 (식 22: 표준 격자 기저 S_i 를 영역 네 모서리에서 Q4 로 보간) · 닫힌 꼴 (식 25: φ_ip ≅ 모서리 넷의 평균 · 식 26: ∇φ_ip 를 모서리 값과 r 벡터로).  핵심 성질 둘: 1D 에서 노드 내부력이 **정확** (미적분 기본정리 · p.1441) 이고, 멀리 떨어진 입자도 대체 기저로 **이어진다** (p.1441 · p.1446).

**(3) 같은 시험으로 네 방법 (표준 MPM · uGIMP · cpGIMP · CPDI) 을 나란히 비교한 숫자가 있다** — 수렴 그림 두 장 (Fig. 4 · 7) 의 표지를 벡터에서 읽었다 (§3-2 · 3-3).  축 정렬 단위 정사각형 (±31 % 축 변형) 에서 가장 고운 격자의 오차: 표준 MPM 9.9 × 10⁻⁶ · uGIMP 2.0 × 10⁻⁷ · cpGIMP 1.76 × 10⁻⁸ · CPDI 1.72 × 10⁻⁸ [판독] — 표준 MPM 은 격자를 8 배 조여도 그림 값이 4.6 배밖에 안 줄고, 노름의 ÷ (N_t × N_p) 를 걷어 낸 RMS 로는 오히려 4.9 배 커진다 [카드 산술 · §3-2].  자중 막대 (Fig. 10) 에서는 표준 MPM · uGIMP · cpGIMP 가 끊기고 CPDI 만 이어진다.

**(4) '어디까지' 를 우리 쪽에서 재는 시험 꼴과 함정이 있다.**  원문은 숫자 문턱을 주지 않지만, 시험 문제 (자중 막대 1 × 1 m · 계단 중력 · 4 셀 · 셀당 3 × 3 입자) 와 그 크기 (q 위 평균 신장 ×2.8 · ×9.7 [카드 산술] · 스냅숏의 영역 가로선에서 읽은 꼭대기 줄 국소 신장 ×4.0 · ×15.2 [판독 · 벡터 · §3-4b]) 가 글 · 그림에 있어 우리 MLS-MPM 에 그대로 돌릴 수 있다.  함정 둘: 오차 노름의 ÷ (N_t × N_p) (식 27) · 시간 간격 Δt = 0.4h/C 의 C 가 **막대 파속** √(E/ρ₀) 이라는 점 (식 28–29 · 우리 ν 0.49 에서는 P파 기준 Courant 수가 1.66 이 된다 [카드 산술 · §8-1]).

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| MPM 이 큰 신장에서 수치적으로 끊기는 현상의 정의 · 원인 | cell crossing (기저 함수가 매끈하지 않음) · ringing (셀 경계에서 기저 기울기의 계단) · extension (입자 영향 영역이 더는 안 겹침) — 원문 문장 (p.1436 · 1440) |
| 입자 영역 추적 (CPDI) 의 식 | 식 (21)–(26) · Fig. 2 · 3 — 2D 평행사변형 · 3D 는 한 문장 |
| 방법끼리의 정량 비교 | Fig. 4 · 7 (오차 vs 셀 간격 · 4 해상도) · Fig. 11 · 12b · 15 · 18b · 19b (변위–시간) [판독 · 벡터] |
| "우리 B-spline MLS-MPM 은 어디까지 늘어나도 되는가" 의 기준 | **숫자 문턱 없음** · B-spline 시험 없음 (원문 격자 기저 = 선형 hat · Fig. 3).  정의 + 시험 범위 (±31 % · 원주 17–26 % · 평균 신장 ×2.8 · ×9.7 · 국소 ×4.0 · ×15.2 · 큰 회전) + 'refinement 하면 안정' 진술 + cpGIMP 에 틈이 난 때의 국소 신장 · 간격 (그림에서 읽힘 · §3-4b) |
| 우리 단위 시험의 해석해 | MMS 두 건 (식 31–38 · 체적력 식 33–34 · A5–A9 · MATLAB 기호 계산 스크립트) |
| 계산 비용 | **없음** (말로만 *"without significantly increasing computational cost"* p.1436 · *"comparable with original GIMP"* p.1440) |
| 소성 · 압밀 · 접촉 · 분리 · 탈압 · 3D · 실험 대조 | **없음** |

### 0-1. ★ 고른 의도 대조 (후보 표 N-15 의 '왜' 칸)

의도 원문 (후보 표 `S8_candidates.md` N-15 '왜' 칸 그대로): f · l — 큰 신장에서 MPM 이 수치적으로 끊기는 문제와 입자 영역 추적 (CPDI) 의 원전 · gritton2017 (§4-1 · §9 ⑨) 과 homel2017 이 둘 다 CPDI 로 계산했는데 원전 카드가 없음 → "우리 B-spline MLS-MPM 은 어디까지 늘어나도 되는가" 의 기준 (가리킨 카드 = gritton2017 §4-1 · §9 ⑨ · 정본 L86 · L91 · L234 · homel2017 언급)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "큰 신장에서 MPM 이 수치적으로 끊기는 문제" | **채움** | 정의 셋: cell crossing (p.1436 · *"lack of smoothness of the grid basis functions"*) · ringing (p.1440 · 표준 MPM) · **extension instability** (p.1440 · uGIMP · *"regions of influence no longer overlap"*).  시연: 자중 막대 (§4.3 · Fig. 10) 에서 *"The simulations using the standard MPM, uGIMP, and cpGIMP exhibit the extension instability"* (p.1446) · 외팔보 (§4.4) 에서 *"The standard MPM and cpGIMP simulations failed by spurious material separation"* (p.1446) · 돌린 막대 mesh(b) 에서는 CPDI 도 *"encounter the extension instability and cannot be completed"* (p.1448).  **조건**: 2D 평면 변형률 · 압축성 neo-Hookean E 1 × 10⁶ Pa · ν 0.3 · ρ₀ 1050 kg/m³ · g 1000 m/s² 계단 (동적) · 1 × 1 m 막대 = 격자 4 셀 × 셀당 3 × 3 입자 (일부러 거친 격자).  원문 낱말 = *extension instability* · *numerical fracture* 0 회 |
| "입자 영역 추적 (CPDI) 의 원전" | **채움** | §3 (p.1440–1442) · 식 (21) 영역 벡터 = 전체 F 로 실어 나름 (F 는 영역 안에서 일정하다고 가정) · 식 (22) 대체 기저 = 모서리 넷의 Q4 보간 · 식 (25)(26) 닫힌 꼴 · Fig. 2 · 3.  **2D 평행사변형만** (3D · 일반 다각형 · 다면체는 문장으로만 · p.1451–1452) |
| "gritton2017 (§4-1 · §9 ⑨) 과 homel2017 이 둘 다 CPDI 로 계산" | **채움 (가리킨 카드 기준)** | gritton2017 = Uintah 의 CPDI · ref [38] = 이 논문 (서지 일치) · homel2017 = GEOS 의 CPDI (ref 39) + domain scaling (ref 32) — 그 카드는 Homel 본문이 이름을 적은 번호로 *"37 Sadeghirad et al."* 을 따로 적는다 (homel 카드 L617) → 이 논문이 Homel 의 ref 37 인지 39 인지는 그 카드의 캡처에 참고문헌 목록이 없어 [미확인].  ⚠ 두 카드의 계산은 **3D 구현**이고 이 원전은 **2D 만** 시험했다 |
| "원전 카드가 없음" | 이 카드로 해소 | — |
| "→ '우리 B-spline MLS-MPM 은 어디까지 늘어나도 되는가' 의 기준" | **일부** (기준의 정의 · 시험 꼴 = 채움 / 숫자 문턱 = **없음** / B-spline · MLS-MPM = **없음**) | 정의 = *"regions of influence no longer overlap"* (p.1440).  시험 범위 [카드 산술]: 단위 정사각형 F_xx 0.69–1.31 · 링 원주 변형 17–26 % (반지름 ≤ 2.8 %) · 막대 q 위 평균 신장 ×2.78 (g 1000) · ×9.75 (g 3500 · CPDI 만) · 외팔보 자유 끝 쪽 ≈ 90° 회전 (Fig. 14).  국소 신장 [판독 · 벡터 · §3-4b]: CPDI 꼭대기 줄 영역 ×4.0 (g 1000) · ×15.2 (g 3500 · 이웃 줄 입자 간격 4.8 셀) 에서도 이어짐 · cpGIMP 는 꼭대기 줄 ×4.1 · 이웃 줄 간격 ≈ 1.25 셀에서 틈 (0.09 s).  원문 문장에는 **끊긴 순간의 국소 신장이 없고** (그림에서만 읽힘 · uGIMP · 표준 MPM 은 그림도 없음 [미확인]), 기저는 선형 hat (Fig. 3) 이다.  우리 MLS-MPM (2차 B-spline · 입자 영역 없음) 에 옮긴 '영향 영역이 안 겹치는' 신장 ×6 은 [카드 산술 · 원문 정의를 옮긴 상한 · §8-2] — 같은 식의 uGIMP 상한은 ×7 인데 uGIMP 는 CPDI 해의 국소 신장이 ×4.0 을 넘지 않는 문제 (g 1000) 에서 끊겼다 (끊긴 때 · 그때의 신장은 [미확인]) · cpGIMP 는 ×4 에서 틈 (원인 = 전단 무시 · p.1446) [판독 · 카드 추론] → **상한을 안전 문턱으로 쓰지 않는다** |
| (덧) "f — MPM 접촉 · 다물체 · 해상도 규칙 · 수치 오차 추정" | **일부** | 접촉 알고리즘 없음 · 한 속도장 = *no-slip* 자동 (p.1436) · 셀당 입자 방향당 2 (MMS) · 3 (막대 · 보) · 오차 = MMS 해석해 대비 노름 (식 27 — ÷ N_t N_p 함정) · *"if sufficient refinement is used"* (p.1448 · 1450 · 결과 미제시) · 지름당 셀 수 규칙 없음 |
| (덧) "l — 소성이 왜 어려운가" | **일부** | MPM 을 쓰는 까닭 = *"the constitutive model is history-dependent and therefore intolerant of advection errors"* (p.1435) · 입자가 이력을 싣는다.  이 논문의 계산은 **탄성** (neo-Hookean) 뿐 — 소성의 어려움 · 우회 · 비용은 다루지 않는다 |
| (덧) "k — DEM 의 한계" | **없음 (말 없음)** | 'DEM' · 'discrete element' 0 회 |

**가리킨 카드 · 같은 원전을 언급한 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `gritton2017_…` L86 | *"CPDI 변종 (ref. [38] Sadeghirad · Brannon · Burghardt 2011)"* | 저자 셋 · 2011 · IJNME 86:1435–1456 | **채움** |
| `gritton2017_…` L91 | Gritton 원문 인용 *"as described by Sadeghirad and Brannon [38]"* | 이 논문 저자는 셋 (Burghardt 포함) — Gritton 본문의 표기이고 카드는 그대로 옮겼다 | 문제 아님 |
| `gritton2017_…` L234 (§4-1) · L684 (§14 용어집) | *"입자 영역을 변형하는 평행육면체로 두고 형상함수를 그 영역에서 평균"* (homel 카드 전재) · *"극단 인장에서 수치적 끊김이 없다"* (devaucorbeil 카드 전재) | ① 원전은 **2D 평행사변형** (3D 평행육면체는 시험 없음 · 'polyhedra' 한 문장) ② 평균하는 것은 표준 격자 기저가 아니라 **그 모서리 값의 Q4 보간 (대체 기저)** — 영역 안에서 둘은 *"can differ significantly"* (p.1452) ③ '끊김 없음' 은 막대 mesh(a) · (c) 에서만 — 돌린 막대 **mesh(b) 에서는 CPDI 도 extension instability** (p.1448) ④ 원문 용어 = extension instability | **일부** — 카드 문제 |
| `gritton2017_…` §9 ⑨ (L595) · §10 행동 2 (L622) | *"물질점 사이가 셀 크기보다 벌어지면 수치적으로 끊길 수 있다"* · *"1 셀을 넘으면 수치적 끊김 경고"* [그 카드의 카드 추론] | 원전의 기준 = *"regions of influence no longer overlap"* (uGIMP) — '1 셀' 문턱은 원전에 없음 · B-spline 은 원전에 없음 | **일부** (그 카드가 추론으로 표지했으므로 오류는 아님 · 문턱 숫자의 원전 근거 없음) |
| `homel2017_…` L238 | *"CPDI (ref 39) 는 입자 영역을 변형하는 평행육면체로 둔다"* | Homel 의 3D (GEOS) 구현 서술로는 맞을 수 있음 · 원전은 2D 평행사변형 · ref 39 = 이 논문인지 [미확인] (같은 카드 L617 은 *"37 Sadeghirad et al."* 을 따로 적는다) | 일부 (경미) |
| `homel2017_…` L654 (§14 용어집) | *"CPDI (convective particle domain interpolation)"* | 원전 이름 = **convected** particle domain interpolation (제목 · p.1436) | 카드 문제 (경미 · Homel 원문의 표기인지는 그 카드의 캡처로 [미확인]) |
| `devaucorbeil2020_…` L38 (후보 표에서 '언급만') | *"CPDI (Sadeghirad 2011) \| 사변형/사면체 입자영역 \| 극단 인장서 numerical fracture 無 \| 미사용(meshing 필요)"* | ① 사면체 없음 (2D 평행사변형 · 3D 는 'polyhedra' 한 문장) ② 'numerical fracture' 0 회 ③ '無' 는 과대 — mesh(b) 에서 CPDI 도 실패 (p.1448) ④ 'meshing 필요' 라는 말은 없다 (처음부터 평행사변형 영역을 허용하고 경계에 맞춘 입자 배치 (CVT · ref [31]) 가 바람직하다고만 · p.1451–1452) | **일부** — 카드 문제 (gritton L234 의 출처) |
| 후보 표 `S8_candidates.md` N-15 | *"[38] Sadeghirad A, Brannon R M and Burghardt J 2011 … Int. J. Numer. Methods Eng. 86 1435–56"* | 원문 첫 쪽과 같다 | **채움** — 덧붙임: DOI 10.1002/nme.3110 · 온라인 2011-03-10 · 접수 2010-02-24 |

⇒ **의도 대조 결과: 일부** — ① 큰 신장에서의 수치 끊김 (extension instability) 의 정의 · 원인 · 시연 = **채움** ② CPDI 원전 (식 21–26) = **채움** ③ gritton2017 · homel2017 이 CPDI 를 쓴 것 = **채움** (단 그 둘은 3D 구현 · 원전은 2D) ④ "우리 B-spline MLS-MPM 은 어디까지 늘어나도 되는가" 의 **숫자 기준 = 없음** (원문 = 정의 + 시험 범위 + 'refinement 하면 안정' 진술 · B-spline 시험 · 문턱 숫자 · 국소 신장 없음) ⑤ 가리킨 카드의 2 차 인용 = **일부** (평행육면체 · '형상함수 평균' · '끊김 없음' · 'convective' · '1 셀' 문턱).

### 0-2. 이 묶음의 네 질문 (DEM 한계 · 소성 · 2D/3D · 탈압)

| 질문 | 이 논문의 답 (원문 위치) |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | **말 없음.**  'DEM' · 'discrete element' 0 회 · 참고문헌 32 건에도 없다 [카드 전문 검색].  다른 입자법에 대한 말은 SPH 의 *tensile instability* 와 이 논문의 *extension instability* 를 구별한 감사의 글 한 문장 (p.1454) 과 *"Extension instability, which is a common shortcoming of many particle methods"* (p.1446) 뿐 |
| (ii) 입자의 소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용 | 큰 변형의 **수치** 어려움을 적는다: ① 셀 넘김 (기저가 매끈하지 않음 · p.1436) ② ringing (기저 기울기의 계단 · p.1440) ③ extension (영향 영역이 안 겹침 · p.1440) ④ cpGIMP 는 대각 성분만 써서 순수 90° 회전에서 *"the particle domain vanishes"* (p.1446–1447) ⑤ 영역을 평행사변형으로 추적하면 GIMP 는 *"complicated division of the particle domain along cell boundaries and use of a numerical integration scheme … considerable computational costs"* (p.1440).  우회 = CPDI (영역을 전체 F 로 · 모서리 Q4 보간 기저).  **소성 자체는 계산하지 않는다** (MPM 이 이력 의존 재료에 맞다는 서론 문장 p.1435 뿐).  맞춘 값 = 없음 (검증 문제 · 재료값은 고른 값).  비용 = [미확인] (입자 수만 인쇄: 링 60–4019 · 막대 36 · 보 144 [카드 산술]) |
| (iii) 2D 인가 3D 인가 · 2D → 3D 전이 | **2D 평면 변형률** [카드 판독 — 식 A6 · A7].  3D 에 대한 말은 둘: *"The proposed method can be naturally generalized to higher order interpolation, as well as three-dimensional problems; for clarity, however, only two-dimensional case studies are described in this paper."* (p.1436) · *"Although the presentation of the new CPDI method was limited to 2D deformations, it should be self-evident how to generalize the techniques to 3D.  Furthermore, although the CPDI method has been here limited to the case of parallelograms deforming to parallelograms, the principles are applicable to general polygons (or polyhedra in 3D)."* (p.1452).  3D 의 증거 · 비용 · 시험은 없다 |
| (iv) 압력을 뺄 때의 거동 | **없다** ('unload' 0 회).  탄성 진동의 되돌아옴만 그림에 있다: 막대 q 가 0.19 s 에 −0.01 m 로 돌아온다 (Fig. 11 [판독]) · 외팔보 q 가 2.7 s 에 −0.12 m (CPDI) ↔ −0.22 m (uGIMP) (Fig. 15 [판독]).  에너지 수지 · 감쇠 · 접촉 분리는 다루지 않는다 |

---

## 1. 한 줄 요약

**KR:** MPM 의 입자 영역을 다루는 기존 두 길 — 영역을 그대로 두는 uGIMP 와 영역을 직사각형으로 두되 변형 경사의 대각 성분으로만 크기를 바꾸는 cpGIMP — 는 큰 인장에서 입자의 영향 영역이 더는 겹치지 않아 끊기거나 (extension instability), 전단 · 회전을 놓쳐 틀어진다 (90° 회전이면 영역이 0).  CPDI 는 처음 직사각형 (또는 평행사변형) 이던 영역을 **전체 변형 경사 F** 로 평행사변형으로 실어 나르고 (식 21), 평행사변형을 셀 경계로 쪼개 적분하는 대신 **표준 격자 기저를 영역 네 모서리에서 Q4 로 보간한 대체 기저** (식 22) 로 바꿔 φ_ip · ∇φ_ip 를 모서리 값의 닫힌 꼴로 구한다 (식 25–26) — 1D 에서는 노드 내부력이 정확하고 (미적분 기본정리), 대체 기저도 단위 분할이며, 멀리 떨어진 입자도 대체 기저로 이어진다.  2D 평면 변형률 · neo-Hookean · 동적 문제 넷 (+ 45° 돌린 영역) 에서 표준 MPM · uGIMP · cpGIMP (· FEM) 과 비교: 축 정렬 MMS 에서는 cpGIMP 와 같고, 원주 방향으로 찌그러지는 링 MMS 에서는 가장 정확하며, 자중 막대 (g 1000 → 3500 m/s²) 에서 유일하게 끊기지 않고, 큰 회전 외팔보에서 영역을 따라 돌린다.  단 계단 모양 영역 (mesh(b)) 에서는 CPDI 도 끊기거나 부정확하고, 같은 영역을 Q4 요소로 쓴 FEM 과도 정확히 같지 않다 (*"coarser than the FEM basis functions"*).  소성 · 접촉 · 3D · 비용 수치는 없다.

**EN:** Sadeghirad, Brannon and Burghardt replace the GIMP particle-domain treatments that either freeze the domain (uGIMP) or keep it an axis-aligned rectangle scaled by the diagonal of F (cpGIMP) — which respectively lose overlap of the particles' regions of influence in extension ("extension instability") and ignore shear and rotation (the domain vanishes under a 90° rotation) — by convecting each initially rectangular (or parallelogram) domain with the full deformation gradient into a parallelogram (Eq. 21) and, instead of splitting the parallelogram along cell boundaries for exact integration, replacing the grid basis by its 4-node (Q4) interpolation at the domain corners (Eq. 22).  The weighting function then becomes the average of the grid basis at the four corners (Eq. 25) and its gradient a closed form in the corner values and the current domain vectors (Eq. 26); nodal forces are exact in 1-D, the alternative basis is a partition of unity, and particles far apart remain connected.  In 2-D plane-strain, Neo-Hookean, dynamic tests — two manufactured-solution convergence studies (axis-aligned unit square: CPDI ≈ cpGIMP; radially expanding ring with rectangle-to-parallelogram distortion: CPDI most accurate, standard MPM unstable), a bar hanging under a suddenly applied gravity of 1000 and 3500 m/s² (only CPDI stays connected), a cantilever with large rotation, and 45°-rotated discretizations (CPDI with boundary-conforming parallelograms agrees with the original; staircase rectangles fail or are inaccurate for every method, including a Q4 FEM on the same domains) — CPDI is reported as more accurate and stable "without significantly increasing computational cost", though no timings are given.  There is no plasticity, contact algorithm, quasi-static loading, 3-D test or cost measurement.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **A convected particle domain interpolation technique to extend applicability of the material point method for problems involving massive deformations** |
| 저자 | **A. Sadeghirad** · **R. M. Brannon** (∗ 교신 · † E-mail Rebecca.Brannon@utah.edu) · **J. Burghardt** |
| 소속 | Department of Mechanical Engineering, University of Utah, Salt Lake City, UT, U.S.A. (세 저자 공통) |
| 저널 | **International Journal for Numerical Methods in Engineering 2011; 86:1435–1456** · John Wiley & Sons · © 2011 |
| DOI | **10.1002/nme.3110** (첫 쪽 머리글 인쇄) |
| 접수 · 게재 | Received 24 February 2010 · Revised 1 October 2010 · Accepted 10 November 2010 · Published online 10 March 2011 in Wiley Online Library |
| 호 | 첫 쪽 머리글에 호 표기 없음 · PDF 오른쪽 여백의 내려받기 워터마크 줄 *"10970207, 2011, 12, Downloaded from …"* 에서 **12 호**로 읽힌다 [카드 판독] |
| 키워드 (인쇄) | material point method; large deformations; extension instability; nodal integration; verification; particle methods |
| 분량 | 22 쪽 (PDF 쪽 n = 학술지 쪽 1434 + n) · Fig. 1–19 (전부 벡터) · **표 없음** · 번호 식 (1)–(38) + (A1)–(A9) · MATLAB 기호 계산 목록 1 (App. A.2) · 참고문헌 32 · 보충 자료 없음 |
| 절 구성 | 1 Introduction (p.1435–1437) · 2 Review of the MPM and GIMP methods (2.1 Equations common to all versions of the MPM · 2.2 Existing material point methods · p.1437–1440) · 3 Description of the CPDI method (3.1 Strategy for tracking particle domains as parallelograms · 3.2 Proposed alternative evaluation of φ_ip and ∇φ_ip · p.1440–1442) · 4 Numerical examples (4.1 Axis-aligned displacement in a unit square · 4.2 Radial expansion of a ring · 4.3 A vertical bar with large tensile deformation · 4.4 Large deformation vibration of a cantilever beam · 4.5 Investigation of particle domain shape in the initial configuration · p.1442–1451) · 5 Conclusion (p.1451–1452) · Appendix A (MMS body forces · A.1 · A.2 · p.1452–1454) · Acknowledgements (p.1454) · References (p.1455–1456) |
| 연구 유형 | 수치 방법 (MPM 변종) + 2D 검증 계산.  실험 없음 |
| 알고리즘 기반 | *"update stress last (USL)"* 판 GIMP (Bardenhagen [17]) · *"Using the cpGIMP, Wallstedt and Guilkey [23] demonstrated that the USL scheme performs dramatically better than an alternative 'update stress first (USF)' scheme"* (p.1437) · 양해 전진 Euler (식 10) · 코드 이름 [미확인] |
| 자금 | Schlumberger Technology Corporation · 감사: J. E. Guilkey (*"helpful comments and contribution"*) · D. Sulsky (SPH tensile ↔ extension instability 구별) · *"the MPM session of the World Congress on Computational Mechanics, 2010, and the MPM workshop in Albuquerque, NM, 2010"* 참가자 (p.1454) |
| PDF 상태 | 조판 PDF (도서관 내려받기본 — 오른쪽 여백에 세로 워터마크) · 글자 층 온전하나 그리스 문자 (φ · σ · χ · Ω · ρ · λ · μ) 가 빠진다 → 식은 렌더 그림에서 옮김 · 메타데이터 Subject *"Numerical Meth Engineering 2011.86:1435-1456"* |

**자기 위치 (저자 원문 · §1 · p.1436)**
> *"This work is called the convected particle domain interpolation (CPDI) method because it convects initially rectangular particle domains into parallelograms, and it constructs an alternative basis function field over the particle that exactly interpolates the grid basis function at the parallelogram's corners using the standard 4-node finite element interpolation.  The proposed method can be naturally generalized to higher order interpolation, as well as three-dimensional problems; for clarity, however, only two-dimensional case studies are described in this paper.  The proposed technique will be shown to eliminate instabilities observed in uGIMP and cpGIMP without significantly increasing computational cost."*

---

## 3. 핵심 수치

> **라벨 규약** · `인쇄` = 본문 · 캡션 · `[판독]` = PDF 벡터 경로 좌표에서 읽음 (`digitized.csv` · 축 = 격자선 · 눈금 글자 중심의 선형 맞춤 · 잔차 ≤ 0.004 데이터 단위) · `[카드 산술]` = 산술 (식 병기) · `[미확인]` = 논문에 없음.  ⚠ 재료값은 전부 검증용 가상 재료 — **우리 재료 값으로 쓰지 않는다.**

### 3-1. 시험 문제 · 재료 · 이산화 (전부 2D 평면 변형률 · 동적 · 압축성 neo-Hookean 식 30)

| 시험 (절 · 그림) | 문제 · 경계 (인쇄) | 재료 (인쇄) | 이산화 (인쇄) | 시간 (인쇄) | [카드 산술] |
|---|---|---|---|---|---|
| ① 축 정렬 단위 정사각형 MMS (§4.1 · Fig. 4 · 5) | 변위장을 미리 정함 (식 31–32 · A = 0.05 m · L = 1 m) · 그 장을 만드는 체적력 (식 33–34) | E 1 × 10⁷ Pa · ν 0.3 · ρ₀ 1000 kg/m³ | 격자 8×8 · 16×16 · 32×32 · 64×64 · **셀당 방향마다 입자 2** | T = 0.02 s (한 주기) · Δt = 0.4h/C (식 28) | C = √(E/ρ₀) = 100 m/s · h 0.125 → 0.0156 m · N_p 256 → 16 384 · Δt 5 × 10⁻⁴ → 6.25 × 10⁻⁵ s · N_t 40 → 320 · 최대 \|F_xx − 1\| = 2πA/L = **0.314** |
| ② 링 반지름 팽창 MMS (§4.2 · Fig. 6–8) | 반지름 대칭 변위 (식 37–38 · 두 면의 법선 응력 0 · u(r_o) = A sin(Cπt/2r̄)) · 사분원만 (대칭) | E 1 × 10⁷ Pa · **ν 0** · ρ₀ 1000 kg/m³ · r_i 0.4 · r_o 0.6 m · A 0.1 m | 입자 **60 · 248 · 1001 · 4019** · 셀당 방향마다 2 | T = 0.02 s (한 주기) · Δt = 0.4h/C | 사분원 넓이 0.1571 m² ÷ (h/2)² 가 인쇄 입자 수와 맞는 h = **0.1 · 0.05 · 0.025 · 0.0125 m** (62.8 · 251 · 1005 · 4021) · c₁ 6.667 · c₂ −13.889 · c₃ 9.259 · 최대 원주 변형 (A 0.1) 안쪽 **25.9 %** · 바깥 16.7 % · 반지름 방향 ≤ 2.8 % · N_t 50 → 400 |
| ③ 자중 수직 막대 (§4.3 · Fig. 9–12) | 위 끝 롤러 · 나머지 자유 · 중력을 t = 0 에 계단으로 · 1.0 × 1.0 m (Fig. 9 치수) | E 1 × 10⁶ Pa · ν 0.3 · ρ₀ 1050 kg/m³ | **격자 4 셀 · 셀당 3 × 3 입자** | T = 0.24 s · Δt = 0.00006 s · g = **1000 m/s²** → 다시 **3500** (CPDI 만) | 셀 0.5 m · 입자 36 · 4000 걸음 · c = √(E/ρ₀) = 30.9 m/s → Δt·c/h = 0.0037 · ρgL/E = **1.05 · 3.675** |
| ④ 외팔보 (§4.4 · Fig. 13–15) | 왼쪽 끝 고정 · 나머지 자유 · g = 10 m/s² 계단 · 4.0 × 1.0 m (Fig. 13 치수) | E 1 × 10⁶ Pa · ν 0.3 · ρ₀ 1050 kg/m³ (*"highly compliant"*) | **16 셀 · 셀당 3 × 3** | T = 3 s · Δt = 0.001 s | 셀 0.5 m · 입자 144 · 3000 걸음 · Δt·c/h = 0.062 · ρgL/E = 0.042 (L 4 m) |
| ⑤ 45° 돌린 ③ · ④ (§4.5 · Fig. 16–19) | 돌린 막대: 대칭 경계 = 반대쪽에 같은 막대를 두고 반대 방향 중력 · 돌린 보: 관련 격자 노드 고정 | ③ · ④ 와 같음 | mesh(a) = 원래 · **mesh(b) = 축 정렬 직사각형 계단** · mesh(c) = 원래 입자 영역을 45° 돌린 평행사변형 (CPDI 만 가능) | ③ · ④ 와 같음 | mesh(b) 의 입자 수 [미확인] · mesh(c) = 원래와 같은 수 (*"the same discretizations"*) |

### 3-2. 축 정렬 단위 정사각형 — 오차 vs 셀 간격 (§4.1 · Fig. 4 · [판독 · 벡터 표지])

| h (격자) | 표준 MPM | uGIMP | cpGIMP | CPDI |
|---|---|---|---|---|
| 0.125 (8 × 8) | 4.61 × 10⁻⁵ | 4.70 × 10⁻⁵ | 3.04 × 10⁻⁵ | 2.77 × 10⁻⁵ |
| 0.0625 (16 × 16) | 2.11 × 10⁻⁵ | 6.04 × 10⁻⁶ | 2.49 × 10⁻⁶ | 2.24 × 10⁻⁶ |
| 0.03125 (32 × 32) | 1.67 × 10⁻⁵ | 9.74 × 10⁻⁷ | 2.04 × 10⁻⁷ | 2.05 × 10⁻⁷ |
| 0.015625 (64 × 64) | **9.91 × 10⁻⁶** | **2.04 × 10⁻⁷** | **1.76 × 10⁻⁸** | **1.72 × 10⁻⁸** |
| 그림 기울기 (끝 ↔ 끝) [카드 산술] | 0.74 | 2.62 | 3.58 | 3.55 |

- 저자 판정: *"Since convergence curves of the cpGIMP and CPDI methods approximately coincide, it can be concluded that the alternative grid basis functions proposed in the CPDI method can accurately evaluate φ_ip and ∇φ_ip.  Also, the uGIMP that does not track the particle domains leads to less accurate results"* (p.1443) · 캡션: 겹치는 것은 *"to be expected since this verification test involves no shear distortions from rectangles to parallelograms"* (p.1444).
- [판독] 가장 고운 격자에서 표준 MPM 오차 ÷ CPDI = **577 배** · uGIMP ÷ CPDI = 11.9 배 · 표준 MPM 은 h 를 8 배 줄여 그림 값이 4.6 배만 준다 (RMS 로는 4.9 배 커짐 · 아래 표).
- ⚠ **식 (27) 을 인쇄대로 읽으면** Err = √(Σᵢ Σₚ ‖u^app − u^exact‖²) / (N_t × N_p) = RMS ÷ √(N_t N_p).  N_p ∝ h⁻² (방향당 2 입자) · N_t = T/Δt ∝ h⁻¹ (식 28) 이면 Err ∝ RMS · h^1.5 → **그림 기울기 = RMS 차수 + 1.5** [카드 산술 — N_t 를 계산 걸음 수로 읽음 · 원문에 'N_t = total number of … time steps' (p.1442, 기호 뒤바뀐 문장 · §12)].  RMS 로 되돌리면 (√(N_t N_p) = 101 · 286 · 810 · 2290):

| RMS 변위 오차 [카드 산술] | h 0.125 | 0.0625 | 0.03125 | 0.015625 | 이웃 기울기 (RMS 차수) |
|---|---|---|---|---|---|
| 표준 MPM | 4.67 mm (A 의 9.3 %) | 6.04 mm | 13.5 mm | **22.7 mm (45 %)** | −0.37 · −1.16 · −0.75 (**격자를 조일수록 커짐**) |
| uGIMP | 4.76 mm (9.5 %) | 1.73 mm | 0.79 mm | 0.47 mm (0.93 %) | 1.46 · 1.13 · 0.76 (차수가 떨어짐) |
| cpGIMP | 3.07 mm (6.1 %) | 0.71 mm | 0.165 mm | 0.040 mm (0.080 %) | 2.11 · 2.11 · 2.03 |
| CPDI | 2.80 mm (5.6 %) | 0.64 mm | 0.166 mm | **0.039 mm (0.079 %)** | 2.13 · 1.95 · 2.07 (**2 차**) |

(오차를 고정된 수의 출력 시각에서만 쟀다면 N_t 는 h 와 무관 → 그림 기울기 = RMS 차수 + 1.0 · 위 차수에 0.5 를 더한다 — 원문은 어느 쪽인지 적지 않았다 [미확인].)

### 3-3. 링 반지름 팽창 — 오차 vs 셀 간격 (§4.2 · Fig. 7 · [판독 · 벡터 표지])

| h (입자 수) | uGIMP | cpGIMP | CPDI |
|---|---|---|---|
| 0.1 (60) | 1.12 × 10⁻⁴ | 1.10 × 10⁻⁴ | 6.29 × 10⁻⁵ |
| 0.05 (248) | 2.34 × 10⁻⁵ | 2.26 × 10⁻⁵ | 1.67 × 10⁻⁵ |
| 0.025 (1001) | 6.71 × 10⁻⁶ | 5.83 × 10⁻⁶ | 2.87 × 10⁻⁶ |
| 0.0125 (4019) | **1.73 × 10⁻⁶** | **1.18 × 10⁻⁶** | **3.64 × 10⁻⁷** |
| 그림 기울기 (끝 ↔ 끝) [카드 산술] | 2.01 | 2.18 | 2.48 |
| RMS 변위 오차 (h 0.1 → 0.0125) [카드 산술 · 같은 가정] | 6.13 → 2.19 mm (A 0.1 m 의 6.1 → 2.2 %) | 6.02 → 1.49 mm (6.0 → 1.5 %) | 3.45 → 0.46 mm (3.4 → 0.46 %) · 이웃 차수 0.39 · 1.03 · 1.48 |

- 캡션: *"The simulations using the standard MPM are unstable at all four resolutions."* (p.1445) — 표준 MPM 곡선은 없다.  x 축 (1.00E-07) 선 위에 범례 없는 작은 네모 표지 넷이 각 해상도 자리에 있다 [판독] — 뜻은 인쇄돼 있지 않다 [미확인] (표준 MPM 의 자리로 보인다 [카드 판독]).
- 저자 판정: *"the results obtained from the CPDI method are more accurate because the CPDI method tracks the particle domains more accurately than other methods do"* (p.1444) · 가장 고운 격자에서 uGIMP ÷ CPDI = 4.75 · cpGIMP ÷ CPDI = 3.23 [판독 · 카드 산술].
- ⚠ 링 문제는 원주 변형이 크고 (17–26 %) 반지름 방향 변형은 작다 (≤ 2.8 %) [카드 산술] — 축에 붙은 처음 직사각형이 반지름 방향을 따라 회전 · 전단되므로 직사각형 → 평행사변형 시험이 된다 (§5 결론의 표현).

### 3-4. 변위–시간 곡선 (Fig. 11 · 12b · 15 · 18b · 19b · 전부 [판독 · 벡터 경로])

| 그림 · 곡선 | 최소 변위 (시각) | 다른 시각의 값 | 비고 |
|---|---|---|---|
| Fig. 11 · CPDI · 막대 g 1000 · q | **−1.633 m** (0.094 s) | 0.05 s −0.88 · 0.15 s −0.72 · 0.19 s **−0.01** · 0.24 s −0.76 m | 주기 ≈ 0.19 s · 감쇠가 눈에 띄지 않는다 |
| Fig. 12b · CPDI · 막대 g 3500 · q | **−8.02 m** (0.101 s) | 0.05 s −3.58 · 0.15 s −4.91 · 0.20 s −0.12 · 0.24 s −1.60 m | Fig. 12a 의 막대 길이 ≈ 9 m [판독] |
| Fig. 15 · 외팔보 · q · CPDI (실선) | **−3.237 m** (1.11 s) | 1.5 s −3.01 · 2.0 s −2.46 · 2.7 s **−0.12** · 3.0 s −0.66 m | — |
| Fig. 15 · 외팔보 · q · uGIMP (점선) | −3.259 m (1.11 s) | 1.5 s −3.02 · 2.0 s −2.54 · 2.7 s **−0.22** · 3.0 s −0.78 m | 첫 골은 CPDI 와 0.7 % · 2.7 s 봉우리에서 0.10 m 차 |
| Fig. 18b · 막대 mesh(a) (실선 · §4.3 과 같음) | −1.635 m (0.095 s) | 0.24 s −0.77 m | Fig. 11 과 같은 계산 |
| Fig. 18b · 돌린 막대 CPDI mesh(c) (점선) | −1.646 m (0.095 s) | 0.24 s −0.82 m | 골 0.7 % 차 · *"in a very good agreement"* (p.1450) |
| Fig. 19b · CPDI mesh(a) 수평 보 (가는 실선) | −3.236 m (1.10 s) | 2.6 s −0.24 · 3.0 s −0.65 m | Fig. 15 CPDI 와 같은 계산 |
| Fig. 19b · CPDI mesh(c) 돌린 보 (짧은 점선) | −3.307 m (1.08 s) | 2.6 s −0.36 · 3.0 s −0.68 m | *"very good agreement"* (p.1450) |
| Fig. 19b · CPDI mesh(b) 돌린 보 (일점쇄선) | **−4.177 m** (1.05 s) | 2.0 s −0.90 · 2.7 s −4.05 · 3.0 s −3.53 m | *"not accurate"* (p.1450) |
| Fig. 19b · uGIMP mesh(b) 돌린 보 (긴 점선) | −3.347 m (1.08 s) | 2.75 s −0.96 · 3.0 s −1.39 m | *"not accurate"* |
| Fig. 19b · FEM mesh(a) 수평 보 (실선) | −3.275 m (1.04 s) | 2.6 s **+0.03** · 3.0 s −0.81 m | CPDI (a) 와 첫 골 1.2 % · 2.6 s 에서 0.26 m 차 [카드 산술] |
| Fig. 19b · FEM mesh(b) 돌린 보 (중간 점선) | −3.638 m (2.21 s) | 1.0 s −3.44 · 3.0 s −2.09 m | *"the FEM with mesh(b) also failed to capture accurate results"* (p.1451) |

- '3.0 s' 칸 = 곡선의 마지막 경로 점 (2.99–3.00 s · `digitized.csv` 의 `end of curve` 행) · '0.24 s' 칸 = 0.24 s 표본 또는 끝점 (0.239–0.240 s).
- 선 모양 ↔ 범례 연결은 그림 화살표 끝의 좌표를 곡선 값과 대조해 정했다 [판독 — 화살표 끝 (2.46, −0.48) · (2.30, −1.18) · (1.69, −1.94) · (1.88, −3.26) · (2.46, −0.09) · (2.66, −3.35)].
- **막대의 늘어남** [카드 산술]: q 는 처음 롤러에서 11/12 m 아래 (Fig. 9b 의 아래 줄 입자 [판독]) → q 위 재료의 평균 신장 = (0.917 + \|u_q\|)/0.917 = **×2.78** (g 1000) · **×9.75** (g 3500).  위쪽일수록 더 늘어난다 (위 끝이 아래 무게를 다 진다) — 줄마다의 값은 아래 §3-4b (스냅숏에서 읽음 · 원문 문장에는 없다).

### 3-4b. 스냅숏의 영역 가로선에서 읽은 줄별 국소 신장 (Fig. 10 · 12a · [판독 · 벡터])

방법: PDF 벡터 경로에서 입자 영역의 가로 변 (실선 · 거의 수평인 선분 — Fig. 12a 는 영역이 좁아 길이 문턱 0.05 pt · 기울기 0.6 까지) 의 y 좌표를 모아 줄 경계로 묶고, 같은 그림의 점선 격자 간격 (= 0.5 m · Fig. 10 은 16.66 pt · Fig. 12a 는 10.20 pt) 으로 m 로 바꿨다 (원자료 = `digitized.csv` 의 `domain-edge level` · `interval` 행).  처음 줄 높이 = 1/6 m (셀당 3 입자) → 신장 = 높이 ÷ (1/6 m) — CPDI · cpGIMP 의 영역 세로 길이는 F_yy × 처음 높이다 (식 20 · 21 · 전단 기울기 몫은 작다).  검산: t = 0 스냅숏의 여섯 줄이 0.165–0.167 m · 막대 길이 1.000–1.005 m 로 읽힌다 · CPDI 0.10 s 의 q (맨 아래 줄 가운데) 위치가 Fig. 11 곡선과 0.02 m 안에서 맞는다.

| 그림 · 방법 · 시각 | 줄 높이 (m) — 위 → 아래 | 꼭대기 줄 신장 | 막대 길이 (m) | 그림이 보이는 것 |
|---|---|---|---|---|
| Fig. 10b · CPDI · g 1000 · 0.08 s | 0.662 · 0.545 · 0.475 · 0.376 · 0.276 · 0.215 | **×3.97** | 2.55 | 이어짐 |
| Fig. 10b · CPDI · 0.09 s | 0.667 · 0.571 · 0.513 · 0.401 · 0.279 · 0.213 | ×4.00 | 2.64 | 이어짐 |
| Fig. 10b · CPDI · 0.10 s | 0.661 · 0.586 · 0.526 · 0.399 · 0.267 · 0.203 | ×3.97 | 2.64 | 이어짐 · 첫째 · 둘째 줄 입자 중심 간격 0.62 m = **1.25 셀** [카드 산술] |
| Fig. 10b · CPDI · 0.11 s | 0.653 · 0.580 · 0.505 · 0.376 · 0.258 · 0.202 | ×3.92 | 2.57 | 이어짐 |
| Fig. 10a · cpGIMP · 0.08 s | 0.676 · 0.574 · 0.468 · 0.376 · 0.269 · 0.208 | ×4.06 | 2.57 | CPDI 와 거의 같은 늘어남 · 첫째 · 둘째 줄 간격 0.625 m = 1.25 셀 [카드 산술] |
| Fig. 10a · cpGIMP · 0.09 s | 첫째 줄 0.682 → **틈 0.126 m** → 둘째 · 셋째 줄 (서로 0.094 m 겹침) → **틈 0.055 m** → 넷째–여섯째 줄 (0.459 · 0.265 · 0.204) | ×4.09 | 2.69 (틈 포함) | 세 토막 = extension instability |
| Fig. 10a · cpGIMP · 0.10 s | 첫째 줄 0.638 → 틈 0.375 m → 둘째 · 셋째 (겹침 0.126 m) → 틈 0.123 m → 넷째–여섯째 | ×3.83 | 2.73 (틈 포함) | 틈이 커짐 |
| Fig. 10a · cpGIMP · 0.11 s | 첫째 줄 0.240 → **틈 1.191 m** → 둘째 · 셋째 (겹침 0.080 m) → 틈 0.109 m → 넷째–여섯째 | — | 2.64 (틈 포함) | 떨어진 첫째 줄이 줄어든 채 위에 남음 |

(틈 / 겹침 판정 = 두 가로선 사이의 가운데 높이를 지나는 영역 세로 변이 0 개면 틈 · 24 개 (두 줄 몫) 면 겹침 [판독 — 이 판의 한 줄 = 세로 변 12 개].)
| Fig. 12a · CPDI · g 3500 · 0.051 s | 1.557 · 1.196 · 0.832 · 0.512 · 0.326 · 0.233 | ×9.3 | 4.66 | 이어짐 |
| Fig. 12a · CPDI · g 3500 · 0.102 s | 2.534 · 2.225 · 1.732 · 1.344 · 0.920 · 0.394 | **×15.2** | **9.15** | 이어짐 · 첫째 · 둘째 줄 입자 중심 간격 2.38 m = **4.8 셀** [카드 산술] |

- ⇒ CPDI 는 이웃 입자 중심이 4.8 셀 떨어져도 (선형 hat 의 노드 공유 범위 밖) 대체 기저로 이어진다 — *"connected together based on these new grid basis functions"* (p.1441) 의 그림 증거.  cpGIMP 는 CPDI 와 같은 국소 신장 (×4 · 간격 1.25 셀) 에서 틈이 났다 → 원인은 영향 영역이 안 겹친 것이 아니라 (cpGIMP 영역은 F_yy 만큼 커진다) 원문 말대로 *"fails to account for the shear part of the deformation"* (p.1446) [카드 추론].
- uGIMP · 표준 MPM 의 막대 스냅숏은 없다 → 그 둘이 끊긴 시각 · 국소 신장은 [미확인].

### 3-5. ★ 원문이 시험한 변형의 크기 (의도 "어디까지 늘어나도 되는가" 의 원문 쪽 칸)

| 시험 | 변형 | 크기 | 결과 |
|---|---|---|---|
| ① 단위 정사각형 MMS | 축 방향 인장 · 압축 파 (전단 없음) | F_xx · F_yy ∈ [0.686, 1.314] [카드 산술 · 식 35–36] | 네 방법 모두 수렴 · 표준 MPM 만 느림 (§3-2) |
| ② 링 MMS | 원주 인장 · 압축 (직사각형 → 평행사변형) | 원주 0.74–1.26 (안쪽) · 0.83–1.17 (바깥) · 반지름 ≤ ±2.8 % [카드 산술] | 표준 MPM 불안정 (네 해상도 모두) · CPDI 가장 정확 |
| ③ 막대 g 1000 | 자중 인장 (동적) | q 위 평균 신장 ×2.78 [카드 산술] · 꼭대기 줄 국소 ×4.0 [판독 · §3-4b] · ρgL/E 1.05 | 표준 MPM · uGIMP · cpGIMP **extension instability** (cpGIMP 틈 = 0.09 s · 국소 ×4.1) · CPDI 안정 |
| ③′ 막대 g 3500 | 자중 인장 (동적) | 평균 신장 ×9.75 · 꼭대기 줄 국소 ×15.2 · 이웃 줄 간격 4.8 셀 [판독] · ρgL/E 3.675 | CPDI 안정 (다른 방법 미계산) |
| ④ 외팔보 | 큰 굽힘 · 회전 (고정 끝은 수평 · 자유 끝 쪽은 ≈ 90° 돌아 수직으로 매달림 · Fig. 14c [판독]) | q 수직 변위 −3.24 m (길이 4 m) | 표준 MPM · cpGIMP *spurious material separation* · uGIMP · CPDI 안정 |
| ⑤ 돌린 영역 | ③ · ④ + 영역 모양 | 같음 | mesh(b) (계단): 막대 = 세 방법 모두 실패 · 보 = 안정하나 부정확 (CPDI · uGIMP · FEM) |

- 격자 해상도가 일부러 거칠다: 막대는 폭 1 m = **2 셀** · 보는 두께 1 m = 2 셀 [카드 산술].  *"Numerical simulations which are not presented here show that both mesh types (b) and (c) lead to stable solutions using the uGIMP, cpGIMP, and CPDI methods if sufficient refinement is used."* (p.1448) → 끊김은 **해상도에 걸린 현상**이기도 하다 (얼마나 조여야 하는지는 [미확인]).

### 3-6. 계산 비용

| 항목 | 값 | 표지 |
|---|---|---|
| 시간 · 메모리 · 걸음당 비용 | **없음** | [미확인] |
| 원문의 말 | *"without significantly increasing computational cost"* (p.1436) · *"with a computational cost comparable with original GIMP"* (p.1440) · 결론 *"The efficiency improvement, which allows evaluation of the MPM integrals without having to partition the integration domain into element intersections"* (p.1451) | 인쇄 (수치 없음) |
| 입자 수 | 링 60 · 248 · 1001 · 4019 (인쇄) · 정사각형 256–16 384 · 막대 36 · 보 144 | [카드 산술] |
| 연산량 비교 (논문 밖) | 선형 격자 기저 (Fig. 3 의 hat) 에서 GIMP 입자 하나 (영역 ≤ 셀) 는 2D 3 × 3 노드 · CPDI 는 모서리 넷 × 2 × 2 = 최대 16 노드 (늘어난 영역이 여러 셀에 걸쳐도 16) · 3D 로 옮기면 모서리 8 × 8 = 64 노드 · 입자당 추가 저장 = 영역 벡터 성분 2D 4 개 (r₁ · r₂) · 3D 9 개 (벡터 셋) (F 는 원래 있음) | [카드 산술 — 원문 미인쇄] |

### 3-7. ★ 이 논문에 **없는** 값 (정직 목록)

| 찾은 것 | 상태 |
|---|---|
| 끊김이 시작되는 국소 신장 · 입자 간격 ÷ h 의 문턱 | **없음** (정의와 그림뿐 · cpGIMP 한 경우만 그림에서 읽힘 = §3-4b) |
| B-spline · MLS · 고차 기저에서의 시험 | **없음** (*"can be naturally generalized to higher order interpolation"* 한 구절) |
| 3D 시험 · 3D 비용 | **없음** |
| 계산 시간 · 메모리 | **없음** |
| 소성 · 이력 의존 재료 · 거의 비압축 재료 (ν → 0.5) | **없음** (ν 0 · 0.3 neo-Hookean 뿐) |
| 물체 사이 접촉 · 마찰 · 분리 · 파괴 | **없음** |
| 준정적 · 하중 제거 · 에너지 수지 | **없음** |
| refinement 하면 안정하다는 계산의 결과 | **없음** (*"not presented here"*) |
| mesh(b) 의 입자 수 · 돌린 보의 고정 노드 수 | **없음** |
| 오차 노름의 N_t 가 계산 걸음인지 출력 시각인지 | **없음** |
| CPDI 모서리 좌표를 r 로 적은 식 (x_α^p = ?) | **없음** (식 26 이 그 규약에 의존 · §4-4) |
| 코드 이름 · 구현 언어 | **없음** |

---

## 4. 방법 ★

### 4-1. MPM 한 걸음 (§2.1 · 식 1–15 · 그림 `eq_01_…` – `eq_15_…`)

- 세 단계 (p.1437): ① 입자의 재료 자료 · 외력을 격자로 (집중 질량 · 노드 힘) ② FEM 처럼 격자에서 운동방정식 → 노드 가속도 ③ 노드 운동으로 입자 위치 · 속도 · 변형 경사 갱신 → 격자는 버리고 다음 걸음에 같은 정규 격자 (*"large deformations are modeled by moving the particles through the grid"*).
- P2G: **m_i = Σ_p φ_ip m_p** (1) · **v_i = Σ_p φ_ip m_p v_p / m_i** (2) — φ_ip = *"effective grid basis function at particle p"* — *"the scheme used to assign values to φ_ip distinguishes one MPM method from the another"* (p.1437).
- 내부력의 유도 (p.1438): FEM 꼴 f_i^int = −∫_Ω ∇φ_i·σ dV (3) → 요소 합 (4) → **입자 영역 합** (5) → 영역 안 응력 일정 (6) → 유효 기울기 **∇φ_ip = (1/V_p) ∫_Ωp ∇φ_i dV** (7) → **f_i^int = −Σ_p ∇φ_ip·σ_p V_p** (8).  근거: *"Particle domains are often small and the variation of stress over them is negligible in comparison with the variation of basis function gradients, especially when the particle spans an element boundary where there can be a jump discontinuity in the basis function gradient."*
- 격자: **a_i = (f_i^int + f_i^ext)/m_i** (9) · **v_i^(n+1) = v_i^n + a_i Δt** (10, *"explicit forward-Euler"*).
- 입자 (USL — 격자 속도를 갱신한 뒤 그 값으로): **∇v_p^(n+1) = Σ_i ∇φ_ip v_i^(n+1)** (11) · **v_p^(n+1) = v_p^n + Σ_i φ_ip a_i Δt** (12) · **x_p^(n+1) = x_p^n + Σ_i φ_ip v_i^(n+1) Δt** (13) · **F_p^(n+1) = (I + ∇v_p^(n+1) Δt) F_p^n** (14) · **V_p^(n+1) = J V_p^0** (15) → *"Following this update of the kinematic state, the constitutive model is called to then update the particle stresses to the end of the time step."* (p.1439).

### 4-2. 기존 변종과 세 가지 불안정 (§1 · §2.2 · 식 16–20 · Fig. 1 · 그림 `eq_16_…` – `eq_20_…`)

| 변종 | φ_ip · ∇φ_ip 를 정하는 법 | 영역 추적 | 원문이 적은 결함 |
|---|---|---|---|
| 표준 MPM | 입자 = Dirac delta = 한 점 적분 (식 7 을 한 점으로) | 없음 (점) | **ringing instability** — *"caused by a sudden jump in basis function gradient as a particle crosses a cell boundary"* (p.1440) · 셀 넘김 불안정 (p.1436) |
| GIMP (Bardenhagen · Kober [3]) | **φ_ip ≡ S̄_ip = (1/V_p) ∫ χ_p(x − x_p) S_i(x) dx** (16) · **∇φ_ip = (1/V_p) ∫ χ_p(x − x_p) ∇S_i(x) dx** (17) · top-hat **χ_p = 1 (x ∈ Ω_p) · 0** (18) | — | 셀 넘김 오차를 *"reducing"* (p.1436) · 영역이 변하면 그 영역을 정확히 따라가야 함 |
| uGIMP | 식 16–17 + 영역 그대로: **{a, b}ⁿ⁺¹ = {a, b}⁰** (19) | 없음 | **extension instability** — *"when the particles become separated to the extent that their regions of influence no longer overlap"* (p.1440) |
| cpGIMP | 영역 = 직사각형 · **{a, b}ⁿ⁺¹ = diag(F_xx, F_yy) {a, b}⁰** (20) | 대각 성분만 | *"limited to problems for which deformation is along the grid directions"* (p.1436) · 하중이 격자 축과 나란할 때만 extension 을 바로잡음 · *"not indifferent to a frame change"* (p.1440) · 순수 90° 회전이면 *"the particle domain vanishes"* (p.1446–1447) |
| (참고 [21] Ma 외 의 크기 변경법) | — | — | 다루지 않음 — *"likewise has the shortcoming of neglecting shear distortion and has some challenging issues reported in [23]"* (p.1436) |

- ⚠ 표기: §2.1 은 노드 기저를 φ_i, §2.2 부터는 S_i 로 적는다 (같은 것) [카드 판독].
- 원문 Fig. 1 = uGIMP · cpGIMP 의 처음 · 갱신 영역 (직사각형 a⁰ × b⁰ → aⁿ⁺¹ × bⁿ⁺¹).

### 4-3. CPDI ① — 영역을 평행사변형으로 추적 (§3.1 · 식 21 · Fig. 2 · 그림 `eq_21_…`)

> *"By using the fully updated deformation gradient at each particle, all deformations and rotations computed at the particle are used for determining the updated particle domain at any time step.  The deformation gradient is typically already available since constitutive models often need it.  Assuming that the particle domains are parallelograms and that the deformation gradient is approximately constant over the particle domain, the particle domains deform according to"* (p.1440)

> **r₁ⁿ⁺¹ = Fₚⁿ⁺¹ r₁⁰ ,  r₂ⁿ⁺¹ = Fₚⁿ⁺¹ r₂⁰** (21)

- (r₁, r₂) = 영역을 정하는 두 벡터 (Fig. 2).  처음 직사각형 · 평행사변형 → 늘 평행사변형 (전단 · 회전 포함).
- 가정 = **F 가 영역 안에서 일정** (초록 · §3.1).  이 가정이 깨지는 곳 (영역 안에서 변형이 크게 변하는 곳) 의 오차는 다루지 않는다 [카드 판독].
- 왜 GIMP 로 하지 않나: 평행사변형을 셀 경계로 쪼개 수치 적분해야 해 *"considerable computational costs"* (p.1440) · 결론 *"In principle, the conventional GIMP approach could also convect its integration domain with the material but doing so would lead to a very high computational cost associated with dividing the particle domain along cell boundaries."* (p.1452).

### 4-4. CPDI ② — 대체 격자 기저와 닫힌 꼴 (§3.2 · 식 22–26 · Fig. 3 · 그림 `eq_22_…` – `eq_26_…`)

> **S_i^app(x) = Σ_(α=1..4) Q_α^p(x) S_i(x_α^p)   on Ω_p** (22)

Q_α^p = 영역의 α 번째 모서리에 붙은 표준 4 절점 (Q4) 형상함수 · x_α^p = 그 모서리 위치.  대체 기저로 쓰면 (식 23 · 24)

> **φ_ip ≅ ¼ {S_i(x₁^p) + S_i(x₂^p) + S_i(x₃^p) + S_i(x₄^p)}** (25 — 인쇄에는 닫는 괄호가 하나 더 있다)

> **∇φ_ip ≅ (1/2V_p) {(S_i(x₁^p) − S_i(x₃^p)) [r₁yⁿ − r₂yⁿ ; r₂xⁿ − r₁xⁿ] + (S_i(x₂^p) − S_i(x₄^p)) [r₁yⁿ + r₂yⁿ ; −r₁xⁿ − r₂xⁿ]}** (26)

- **1D 정확성**: *"since the alternative basis function is an interpolation, it identically equals the exact basis function at the particle corners.  This property makes the CPDI evaluation of nodal forces exact in 1D.  The proof is a straightforward application of the fundamental theorem of calculus"* (p.1441).  다차원에서 정확하다는 주장은 없다 [카드 판독].
- **단위 분할**: *"Similar to the standard grid basis, the alternative grid basis is a partition of unity."* (p.1451).
- **멀리 떨어진 입자의 연결**: *"When the particles are far apart in massive tensile deformations, the particles in the CPDI method are connected together based on these new grid basis functions."* (p.1441) · *"lead to particles that will remain 'in contact' even when they are far from each other"* (p.1446).
- **영역 안에서는 다르다**: *"In the interior of a particle, the CPDI alternative grid basis functions can differ significantly from the standard grid basis functions, yet they still provide very efficient and accurate approximations to the MPM integrals. … The CPDI method evaluates these averages accurately and efficiently even if the particle domain is stretched over many grid cells."* (p.1452).
- Fig. 3 (1D): 늘어난 입자 영역 안에 들어온 노드 k 는 *S_k^app = 0* — 영역 모서리가 다른 셀에 있으면 그 사이 노드는 대체 기저에서 빠진다 [판독] → FEM 보다 *"coarser"* (p.1451) 한 까닭의 그림 [카드 추론].
- ★ **식 (26) 의 검산 [카드 산술 · 논문 밖]**: 선형 S_i(x) = a·x + b (a = (0.7, −1.3)) 와 찌그러진 평행사변형 (r₁ = (0.30, 0.05) · r₂ = (−0.08, 0.25)) 으로 대입하면, **r₁ · r₂ 를 변 전체 벡터 (모서리 = x_p ± (r₁ ± r₂)/2 · V_p = \|r₁ × r₂\|) 로 읽고 모서리를 x_p − (r₁ + r₂)/2 부터 반시계로 1–4 번 매길 때만** 식 (26) 이 정확히 a 를 돌려준다.  Fig. 2 의 화살표처럼 r 을 중심에서 변까지의 **반 길이** (모서리 = x_p ± r₁ ± r₂ · V_p = 4\|r₁ × r₂\|) 로 읽으면 결과는 **a/2** 이고, 번호를 다르게 매기면 방향이 틀린다.  원문은 모서리를 r 로 적은 식을 인쇄하지 않았다 [미확인] → 구현할 때 이 규약을 단위 시험 (선형장 재현) 으로 먼저 고정한다.
- 식 (25) 는 평행사변형에서 Q4 형상함수의 적분이 각각 V_p/4 라서 나오는 꼴 [카드 산술 — 평행사변형 (쌍선형 사상의 야코비안 일정) 일 때].

### 4-5. 검증 설계 — MMS · 오차 노름 · 시간 간격 · 재료 (§4 · 식 27–38 · App. A · 그림 `eq_27_…` – `eq_A9_…` · `alg_A2_…`)

- **MMS (method of manufactured solutions)**: *"the solution of the model equations is assumed a priori, then the external force required to achieve this solution is analytically determined"* (p.1442) · 시험 꼴은 Wallstedt · Guilkey [23] 와 비슷 · 해는 총 Lagrange 꼴로 만들고 (식 A1 ∇₀·P + ρ₀b = ρ₀ü) 갱신 Lagrange (식 A2 ∇·σ + ρb = ρü · MPM 꼴) 결과와 견준다.
- 단위 정사각형: **u_x = A sin(2πX/L) sin(Cπt/L)** (31) · **u_y = A sin(2πY/L) sin(Cπt/L + π)** (32) · 체적력 (33)(34) · F 의 대각 (35)(36) · 벡터 꼴 (A5)–(A8).
- 링: **u(r, t) = A sin(Cπt/2r̄)(c₃r³ + c₂r² + c₁r)** (37) · 계수 (38) · 직교 좌표 꼴 (A9) · 체적력 = MATLAB 기호 계산 (App. A.2 목록 · ν = 0 이라 λ = 0 · P = μF⁻¹(FFᵀ − I) · BodyForce = ü − (1/ρ) Div P).
- **오차 노름**: **Err = √(Σᵢ Σₚ ‖u^app(x_p, t_i) − u^exact(x_p, t_i)‖²) / (N_t × N_p)** (27) — 제곱근은 분자만 덮는다 (렌더 확인) → §3-2 의 함정.
- **시간 간격**: **Δt = 0.4 h/C** (28) · **C = √(E/ρ₀)** (29) — *"C is the thin bar wave speed, not the uniaxial strain wave speed"* (p.1442).  [카드 산술] P파 (일축 변형) 속도 ÷ 막대 파속 = √((1 − ν)/((1 + ν)(1 − 2ν))) = 1.00 (ν 0) · 1.16 (ν 0.3) · **4.14 (ν 0.49)** → 같은 식의 P파 기준 Courant 수 = 0.40 · 0.46 · **1.66**.  막대 (Δt = 6 × 10⁻⁵ s) · 보 (10⁻³ s) 는 Δt 를 직접 정했다 (Δt·c/h = 0.0037 · 0.062).
- **재료**: **σ = (λ ln J/J) I + (μ/J)(FFᵀ − I)** (30) — *"While many complicated material models have been successfully used in many implementation of the MPM, this simple and frame-indifferent material model is sufficient for investigating the proposed modifications."* (p.1443) · 총 Lagrange 꼴 **P = λ ln J F⁻¹ + μF⁻¹(FFᵀ − I)** (A3 — 공칭 응력 (Jσ 의 F⁻¹ 곱) 꼴 [카드 판독]).

### 4-6. 경계 · 접촉 · 대칭 — 이 논문이 하는 것과 하지 않는 것

| 묻는 것 | 이 논문 |
|---|---|
| 물체 사이 접촉 알고리즘 | **없다** — 물체가 하나씩.  다만 서론: *"traditional MPM … enforces no-slip contact between bodies automatically without any further computational costs"* (p.1436) = 한 속도장 = 붙음 |
| 입자끼리의 연결 | CPDI 는 멀리 떨어진 입자도 *"remain 'in contact'"* (p.1446) — 연속체가 끊기지 않게 하는 성질이고, **물리적 분리 (파괴 · 탈착) 를 내지는 못한다** [카드 추론] |
| 막대 위 끝 | 롤러 (p.1446) — 거는 방법 (노드 조건) [미확인] |
| 외팔보 왼쪽 끝 | 고정 (p.1446) · 돌린 보: *"the fixed boundary conditions are enforced by fixing the related grid nodes"* (p.1448 · Fig. 17 의 검은 점) |
| 돌린 막대의 대칭 | *"enforced by adding the same bar on the other side of the boundary which is subjected to gravity with the same magnitude but opposite direction"* (p.1448) |
| 자유 표면 | 전부 traction free · 따로 거는 조건 없음 |
| 영역 사이 틈 · 겹침 | cpGIMP 는 *"unrealistic gaps and overlapping of the particle domains"* · CPDI 도 *"although present, are much smaller"* (p.1446) |

### 4-7. 의사코드 — 한 걸음 (우리 전사 · 원문에 한 걸음 전체의 순서도는 없다)

```
# (번호) = 원문 식 · [카드 판독] = 순서 · 평가 자리를 카드가 이어 붙인 것
모서리   x_α^p = x_p ± (r1 ± r2)/2   (α = 1..4, 반시계)             [카드 판독 · §4-4 검산 · 원문 미인쇄]
가중     φ_ip = ¼ Σ_α S_i(x_α^p)                                     (25)   # S_i = 선형 hat (Fig. 3)
         ∇φ_ip = (1/2V_p){(S_i1 − S_i3)[r1y − r2y; r2x − r1x] + (S_i2 − S_i4)[r1y + r2y; −r1x − r2x]}   (26)
P2G      m_i = Σ_p φ_ip m_p ;  v_i = Σ_p φ_ip m_p v_p / m_i           (1)(2)
힘       f_i^int = −Σ_p ∇φ_ip · σ_p V_p ;  f_i^ext (체적력 · 중력)      (8)
격자     a_i = (f_i^int + f_i^ext)/m_i ;  v_i ← v_i + a_i Δt          (9)(10)
입자     ∇v_p = Σ_i ∇φ_ip v_i^(n+1)                                   (11)
         v_p ← v_p + Σ_i φ_ip a_i Δt ;  x_p ← x_p + Σ_i φ_ip v_i^(n+1) Δt   (12)(13)
         F_p ← (I + ∇v_p Δt) F_p ;  V_p = J V_p^0                       (14)(15)
영역     r1 ← F_p r1^0 ;  r2 ← F_p r2^0                                (21)
응력     σ_p ← neo-Hookean(F_p)   # USL: 운동 갱신 뒤                  (30)
격자는 버리고 같은 정규 격자로 다음 걸음
```

### 4-8. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

| 축 | 이 논문 |
|---|---|
| 물체 | 연속체 하나 (정사각형 · 사분원 링 · 막대 · 보) — **입자 층 · 패킹 · 입도 없음** |
| '입자' | MPM 물질점 = 연속체를 나눈 적분점 (알갱이가 아니다) · 영역 = 직사각형 → 평행사변형 |
| 변형 | 진짜 연속체 변형 (탄성 · 큰 변형) — 접촉 겹침의 대리가 아니다 |
| 소성 | **없음** |
| 접촉 | 없음 (한 물체 · 한 속도장) |
| 무작위성 | 없음 (정규 배치) |
| 기공 | 없음 |

---

## 5. 결과 — 절별

### 5-1. 축 정렬 단위 정사각형 (§4.1 · Fig. 4 · 5)

- 전단이 없는 시험이라 cpGIMP 와 CPDI 가 같다 (*"approximately coincide"*) — 대체 기저가 φ_ip · ∇φ_ip 를 정확히 계산한다는 근거.  uGIMP 는 덜 정확하다.  표준 MPM 은 수렴이 거의 없다 (§3-2 [판독]).
- *"This example is not representative of general material deformations because displacements are axis aligned."* (p.1443).
- Fig. 5 = CPDI 16 × 16 셀 스냅숏 셋 — 라벨 t = 0.05 · 0.15 는 인쇄된 주기 밖 (§12).

### 5-2. 링 반지름 팽창 (§4.2 · Fig. 6–8)

- 표준 MPM 은 네 해상도 모두 불안정 · CPDI 가 가장 정확 (§3-3 [판독]).
- Fig. 8 (248 입자): CPDI 의 평행사변형 영역은 서로 맞물려 덮는다 · cpGIMP 의 직사각형 영역은 계단 모양 겹침 · 틈 (확대 원) [판독].

### 5-3. 자중 막대 (§4.3 · Fig. 9–12)

- *"The simulations using the standard MPM, uGIMP, and cpGIMP exhibit the extension instability.  However, more accurately tracking the particle domains in the CPDI method results in a stable simulation."* (p.1446).
- *"Because the cpGIMP fails to account for the shear part of the deformation, it predicts unrealistic gaps and overlapping of the particle domains, ultimately leading to the extension instability shown in Figure 10.  These gaps and overlapping, although present, are much smaller when using the CPDI method.  Thus this method does not suffer from extension instability in this example."* (p.1446) — **"in this example"** 의 한정이 원문에 있다.
- [판독 · 벡터 · §3-4b] Fig. 10a (cpGIMP) 는 0.08 s 까지 CPDI 와 거의 같은 줄 높이로 늘어나다가 (꼭대기 줄 ×4.06 · 길이 2.57 m) 0.09 s 에 틈 둘 (첫째–둘째 줄 0.126 m · 셋째–넷째 줄 0.055 m) 로 세 토막이 되고, 0.11 s 에 첫째–둘째 줄 틈이 1.19 m 가 된다 · Fig. 10b (CPDI) 는 0.08–0.11 s 에 길이 2.55–2.64 m (꼭대기 줄 ×3.9–4.0) 로 이어진다.
- g = 3500 (*"more than tripled"*): CPDI 안정 · q 최소 −8.02 m (Fig. 12b [판독]) · Fig. 12a 의 윗줄 영역은 여러 셀에 걸쳐 늘어난다.

### 5-4. 외팔보 (§4.4 · Fig. 13–15)

- *"The standard MPM and cpGIMP simulations failed by spurious material separation."* (p.1446).  cpGIMP 는 회전이 커질수록 영역이 줄어 결국 실패 (Fig. 14b — 1.10 · 1.20 s 에 굽은 곳의 영역이 점으로 줄고, 1.70 s 에는 자유 끝 쪽 입자들이 영역 없이 아래에 흩어진 채 남고 고정 끝 쪽만 위로 돌아간다 [판독]).
- uGIMP 는 계산은 끝나지만 영역이 회전하지 않아 고정 끝 근처에서 크게 겹친다 (Fig. 14a [판독]).  q 변위는 CPDI 와 첫 골 0.7 % · 2.7 s 봉우리에서 0.10 m 차 (§3-4).
- CPDI 는 전체 F 로 영역을 돌린다 (Fig. 14c).

### 5-5. 45° 돌린 영역 (§4.5 · Fig. 16–19)

- 돌린 막대: mesh(b) 는 **세 방법 모두** extension instability 로 계산 실패 · CPDI mesh(c) 만 안정 → §4.3 과 *"very good agreement"* (Fig. 18 [판독] 골 0.7 % 차).
- 돌린 보: uGIMP mesh(b) · CPDI mesh(b) · (c) 안정 · cpGIMP mesh(b) 불안정.  uGIMP · CPDI 의 mesh(b) 결과는 *"not accurate"* · CPDI mesh(c) 는 *"very good agreement"* (Fig. 19 [판독]).
- 같은 영역을 Q4 요소로 쓴 **FEM** 도 mesh(b) 에서 부정확 · FEM mesh(a) 와 CPDI mesh(a) 는 *"do not exactly coincide … because the CPDI uses the proposed alternative grid functions, which are coarser than the FEM basis functions"* (p.1451).
- 결론: *"particle distributions that conform to a boundary are desirable"* (p.1452) · 경계에 맞춘 배치는 CVT [31] 로 만들 수 있다 (p.1451).

### 5-6. 결론 (§5)

- *"The new CPDI method has been demonstrated to be efficient, accurate, and stable in several large deformation solid mechanics problems that were not solved satisfactorily with any previously existing MPM techniques."* (p.1451) — 시험 범위는 §3-5 까지다.

---

## 6. 그림별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability/` · 그림 19 장 = 벡터 그림 + 그 띠 안의 글자 ± 6 pt (300 dpi · 캡션 문자는 `figures.json` 에 · 도구 관례) — 도구가 16 장을 뽑았고 Fig. 1 · 2 · 11 은 건너뛰었으며 도구의 fig_6.png 는 Fig. 7 이었다 → Fig. 1 · 2 · 6 · 11 은 손 크롭 (`manual_crop`) · 나머지 15 장은 다시 자름 (`recrop` — 이웃 캡션 줄 섞임 2 · 패널 · 범례 잘림 4 · 여백 불균등 9).  식 48 장은 손 크롭 (400 dpi · 사방 7 pt).  근거 문단 20 장 (300 dpi · 사방 6 pt).  [판독] · [카드 …] 표지는 논문 밖 판단.

| 그림 | 파일 | 원 캡션 요지 (PDF 쪽 / 학술지 쪽) | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | uGIMP (식 19) · cpGIMP (식 20) 의 처음 · 갱신 영역 (p.5 / 1439) | 직사각형이 격자 축에 붙어 있다 — 전단 · 회전을 못 담는 구조 |
| 2 | `fig_2.png` | CPDI 의 처음 · 갱신 영역 (p.7 / 1441) | 평행사변형 + r₁ · r₂.  ⚠ 화살표는 중심 → 변 (반 길이) 인데 식 (26) 은 변 전체 벡터일 때 정확 [카드 산술 · §4-4] |
| 3 | `fig_3.png` | 1D 의 대체 격자 기저 (p.7 / 1441) | hat 기저를 입자 모서리 값으로 보간 · 늘어난 영역 안의 노드는 S^app = 0 — 멀리 떨어진 입자도 이어지지만 영역 안의 정보는 거칠어진다 |
| 4 | `fig_4.png` | 단위 정사각형 수렴 (MPM · uGIMP · cpGIMP · CPDI) (p.10 / 1444) | 가장 고운 격자 오차 9.9e-6 · 2.0e-7 · 1.76e-8 · 1.72e-8 [판독].  그림 기울기 0.74 · 2.62 · 3.58 · 3.55 → RMS 로 되돌리면 표준 MPM 은 격자를 조일수록 커지고 CPDI · cpGIMP 는 2 차 [카드 산술 · 식 27 의 ÷ N_t N_p] |
| 5 | `fig_5.png` | CPDI 16 × 16 셀 스냅숏 셋 (p.10 / 1444) | 축 방향 압축 · 인장 파가 입자 간격으로 보인다.  라벨 t 는 주기 밖 (§12) |
| 6 | `fig_6.png` | 사분원 링의 네 해상도 (p.11 / 1445) | 60 · 248 · 1001 · 4019 입자 · 계단 경계 |
| 7 | `fig_7.png` | 링 수렴 (uGIMP · cpGIMP · CPDI · 표준 MPM 은 불안정) (p.11 / 1445) | 가장 고운 격자 1.73e-6 · 1.18e-6 · 3.64e-7 [판독] · RMS 로는 CPDI 3.4 → 0.46 % (A 대비) [카드 산술] · 축 위 범례 없는 네모 넷 = 뜻 미인쇄 |
| 8 | `fig_8.png` | 248 입자 링 — (a) CPDI · (b) cpGIMP (p.11 / 1445) | 평행사변형은 맞물리고 직사각형은 겹치고 틈이 난다 (확대 원) — 영역 모양이 질량 · 힘 배분을 정한다 |
| 9 | `fig_9.png` | 수직 막대 기하 · 이산화 (p.12 / 1446) | 1 × 1 m · 4 셀 × 3 × 3 = 36 입자 · q = 맨 아래 줄 가운데 왼쪽 입자 — **우리 MLS-MPM 의 '늘어남' 단위 시험으로 그대로 옮길 수 있는 문제** |
| 10 | `fig_10.png` | 막대 스냅숏 다섯 — (a) cpGIMP · (b) CPDI (p.13 / 1447) | cpGIMP 는 0.08 s 까지 CPDI 와 같은 꼴 (꼭대기 줄 ×4.06) → 0.09 s 에 틈 둘 · 세 토막 (extension instability) · CPDI 는 길이 2.55–2.64 m 로 이어짐 [판독 · 벡터 · §3-4b] |
| 11 | `fig_11.png` | CPDI 막대 q 변위 (p.13 / 1447) | 최소 −1.63 m (0.094 s) · 0.19 s 에 −0.01 m 로 돌아옴 [판독] — q 위 평균 신장 ×2.8 [카드 산술] |
| 12 | `fig_12.png` | g 3500 — (a) 스냅숏 셋 · (b) q 변위 (p.14 / 1448) | 최소 −8.02 m · 0.102 s 막대 9.15 m · 꼭대기 줄 영역 ×15.2 · 이웃 줄 입자 간격 4.8 셀 [판독 · 벡터] — 영역 하나가 다섯 셀에 걸쳐도 이어진다 |
| 13 | `fig_13.png` | 외팔보 기하 · 이산화 (p.14 / 1448) | 4 × 1 m · 16 셀 × 3 × 3 = 144 입자 · q = 자유 끝의 맨 아래 줄 입자 |
| 14 | `fig_14.png` | 외팔보 스냅숏 — (a) uGIMP · (b) cpGIMP · (c) CPDI (p.15 / 1449) | (a) 영역 안 돌고 겹침 (b) 영역이 회전과 함께 줄어 점 → 1.70 s 에 자유 끝 쪽이 떨어져 흩어짐 (c) 평행사변형이 따라 돈다 (자유 끝 쪽 ≈ 90°) |
| 15 | `fig_15.png` | 외팔보 q 변위 — uGIMP · CPDI (p.15 / 1449) | 골 −3.24 ↔ −3.26 m · 2.7 s 봉우리 −0.12 ↔ −0.22 m [판독] |
| 16 | `fig_16.png` | 막대 이산화 — (a) 원래 · (b) (c) 45° 돌림 (p.16 / 1450) | mesh(b) = 계단 (축 정렬 직사각형) · mesh(c) = 돌린 평행사변형 (CPDI 만) |
| 17 | `fig_17.png` | 보 이산화 — (a) 원래 · (b) (c) 돌림 (p.16 / 1450) | 고정 = 격자 노드 고정 (검은 점) |
| 18 | `fig_18.png` | 돌린 막대 CPDI mesh(c) — (a) 스냅숏 · (b) q 변위 (p.16 / 1450) | 원래와 골 0.7 % 차 [판독] — 경계에 맞춘 영역이면 방향이 바뀌어도 같은 답 |
| 19 | `fig_19.png` | 돌린 보 — (a) CPDI mesh(c) 스냅숏 · (b) uGIMP · CPDI · FEM 의 q 변위 (p.17 / 1451) | mesh(b) 는 CPDI · uGIMP · FEM 모두 틀린다 (CPDI −4.18 m 골) · FEM (a) ↔ CPDI (a) 도 2.6 s 에서 0.26 m 갈라진다 [판독 · 카드 산술] — CPDI 기저가 FEM 보다 거칠다는 저자 진술의 그림 |

**식 그림** (번호 식 47 + MATLAB 목록 1 = 48 장 · 파일 이름 앞머리 = 식 번호)

| 식 | 파일 | 한 줄 뜻 |
|---|---|---|
| (1) | `eq_01_p2g_grid_mass.png` | P2G 질량 m_i = Σ φ_ip m_p |
| (2) | `eq_02_p2g_grid_velocity.png` | P2G 속도 |
| (3) | `eq_03_fem_internal_force_domain_integral.png` | 내부력 — FEM 꼴 |
| (4) | `eq_04_fem_internal_force_element_sum.png` | 요소 합 |
| (5) | `eq_05_mpm_internal_force_particle_domain_sum.png` | 입자 영역 합 (MPM) |
| (6) | `eq_06_internal_force_constant_particle_stress.png` | 영역 안 응력 일정 |
| (7) | `eq_07_effective_basis_gradient_definition.png` | 유효 기울기 = 영역 평균 |
| (8) | `eq_08_nodal_internal_force.png` | 노드 내부력 |
| (9) | `eq_09_grid_acceleration.png` | 격자 가속도 |
| (10) | `eq_10_grid_velocity_update.png` | 양해 전진 Euler |
| (11) | `eq_11_particle_velocity_gradient.png` | 입자 속도 기울기 |
| (12) | `eq_12_particle_velocity_update.png` | 입자 속도 갱신 |
| (13) | `eq_13_particle_position_update.png` | 입자 위치 갱신 |
| (14) | `eq_14_deformation_gradient_update.png` | 변형 경사 갱신 (CPDI 의 입력) |
| (15) | `eq_15_particle_volume_update.png` | 입자 부피 V = J V⁰ |
| (16) | `eq_16_gimp_weighting_function.png` | GIMP 가중 함수 |
| (17) | `eq_17_gimp_gradient_weighting_function.png` | GIMP 가중 기울기 |
| (18) | `eq_18_tophat_characteristic_function.png` | top-hat 특성 함수 |
| (19) | `eq_19_ugimp_fixed_domain.png` | uGIMP — 영역 그대로 |
| (20) | `eq_20_cpgimp_diagonal_F_domain.png` | cpGIMP — 대각 성분만 |
| (21) | `eq_21_cpdi_domain_vectors_convected_by_F.png` | ★ CPDI 영역 추적 |
| (22) | `eq_22_cpdi_alternative_basis_q4_interpolation.png` | ★ CPDI 대체 기저 (Q4 보간) |
| (23) | `eq_23_cpdi_weighting_function_integral.png` | 대체 기저의 가중 함수 |
| (24) | `eq_24_cpdi_gradient_weighting_integral.png` | 대체 기저의 가중 기울기 |
| (25) | `eq_25_cpdi_weighting_corner_average.png` | ★ 닫힌 꼴 — 모서리 넷 평균 (괄호 하나 더 · 인쇄 그대로) |
| (26) | `eq_26_cpdi_gradient_weighting_closed_form.png` | ★ 닫힌 꼴 기울기 (r 규약 §4-4) |
| (27) | `eq_27_error_norm.png` | ★ 오차 노름 (÷ N_t N_p · §3-2) |
| (28) | `eq_28_time_step.png` | Δt = 0.4h/C |
| (29) | `eq_29_thin_bar_wave_speed.png` | C = √(E/ρ₀) (막대 파속) |
| (30) | `eq_30_neo_hookean_cauchy_stress.png` | 압축성 neo-Hookean |
| (31) · (32) | `eq_31_mms_unit_square_ux.png` · `eq_32_mms_unit_square_uy.png` | MMS 변위 (단위 정사각형) |
| (33) · (34) | `eq_33_mms_body_force_bx.png` · `eq_34_mms_body_force_by.png` | MMS 체적력 |
| (35) · (36) | `eq_35_mms_Fxx.png` · `eq_36_mms_Fyy.png` | F 의 대각 (최대 ±31 %) |
| (37) | `eq_37_mms_ring_radial_displacement.png` | MMS 링 변위 |
| (38) | `eq_38_mms_ring_coefficients.png` | 링 계수 c₁ · c₂ · c₃ |
| (A1) · (A2) | `eq_A1_total_lagrangian_motion.png` · `eq_A2_updated_lagrangian_motion.png` | 총 / 갱신 Lagrange 운동방정식 |
| (A3) | `eq_A3_neo_hookean_first_piola.png` | neo-Hookean 공칭 응력 꼴 |
| (A4) | `eq_A4_deformation_gradient_from_displacement.png` | F = I + ∂u/∂X |
| (A5)–(A8) | `eq_A5_unit_square_displacement_vector.png` · `eq_A6_unit_square_deformation_gradient.png` · `eq_A7_unit_square_first_piola_diagonal.png` · `eq_A8_unit_square_body_force_vector.png` | 단위 정사각형 벡터 꼴 (A6 F_zz = 1 · A7 P_zz ≠ 0 → 평면 변형률) |
| (A9) | `eq_A9_ring_displacement_cartesian.png` | 링 변위 (직교 좌표) |
| App. A.2 | `alg_A2_matlab_ring_body_force.png` | 링 체적력 MATLAB 기호 계산 |

**근거 문단 크롭** (20 장 · 카드가 숫자 · 정의 · 단정의 근거로 인용한 문단)

| 파일 | 무엇의 근거 |
|---|---|
| `txt_p1_title_authors_abstract_doi.png` | 서지 · 초록 (*"crucial to eliminate instability in extension"*) · 접수일 · 키워드 |
| `txt_p1_intro_history_dependent_advection.png` | 이력 의존 재료 → 이류 오차에 민감 (l) |
| `txt_p2_noslip_cell_crossing_instability.png` | no-slip 자동 · cell crossing 의 원인 |
| `txt_p2_ugimp_cpgimp_rectangular_tracking.png` | uGIMP · cpGIMP 의 정의 · cpGIMP 의 한계 |
| `txt_p2_cpdi_parallelograms_2d_only_no_cost_increase.png` | CPDI 이름 · 2D 만 · 비용 주장 |
| `txt_p6_ringing_extension_instability_definitions.png` | ringing · extension · frame 의 정의 |
| `txt_p6_parallelogram_division_cost_cpdi.png` | 평행사변형 GIMP 의 비용 · CPDI '비용 비슷' |
| `txt_p7_exact_in_1d_far_apart_connected.png` | 1D 정확 · 멀리 떨어진 입자 연결 |
| `txt_p8_error_norm_nt_np_timestep_wave_speed.png` | N_t · N_p 문장 (뒤바뀜) · Δt · 막대 파속 · neo-Hookean |
| `txt_p9_unit_square_grids_material_period.png` | 단위 정사각형 격자 · 재료 · T |
| `txt_p10_ring_parameters_resolutions.png` | 링 재료 · 치수 · 입자 수 |
| `txt_p12_vertical_bar_extension_instability_g3500.png` | 막대 조건 · 세 방법 실패 · CPDI 안정 · g 3500 · 'in contact' |
| `txt_p12_cantilever_spurious_separation.png` | 외팔보 조건 · spurious material separation |
| `txt_p13_cpgimp_rotation_domain_vanishes.png` | 90° 회전에서 cpGIMP 영역 소멸 |
| `txt_p14_rotated_domains_mesh_b_refinement.png` | 돌린 막대 mesh(b) 실패 · refinement 진술 |
| `txt_p16_rotated_beam_mesh_b_inaccurate.png` | 돌린 보 mesh(b) 부정확 · mesh(c) 일치 |
| `txt_p17_fem_q4_comparison_coarser_basis.png` | FEM 비교 · *"coarser than the FEM basis functions"* · CVT |
| `txt_p17_conclusion_partition_of_unity.png` | 결론 · 단위 분할 |
| `txt_p18_stretched_over_many_cells_3d_polyhedra.png` | 여러 셀에 걸친 영역 · 3D 'self-evident' |
| `txt_p20_ack_extension_vs_sph_tensile_instability.png` | SPH tensile ↔ extension instability 구별 · 자금 |

---

## 7. Post-processing

| 무엇 | 어떻게 (논문) | 우리에게 |
|---|---|---|
| 수렴 | MMS 해석해 대비 노름 (식 27) 을 셀 간격 네 개에 대해 log–log (Fig. 4 · 7) · 방법 넷을 한 그림에 | 단위 시험 보고 꼴 — 단 노름은 RMS (√(ΣΣe²/(N_t N_p))) 로 정의하고 상대값 (÷ A) 과 최대 절대 오차를 함께 [카드 추론] |
| 안정 판정 | 계산이 끝까지 가는가 · 스냅숏에서 영역 틈 · 겹침 · 토막 (Fig. 10 · 14) | 눈 판정 대신 수 (물질점 최근접 간격 ÷ dx 의 최대 · F 주신장 분포 · 빈 셀 수) 를 결과 전에 등록 |
| 국소 변형의 시각화 | 입자를 **영역 모양 (평행사변형)** 으로 그림 — 찌그러짐이 바로 보인다 | 우리 물질점은 영역이 없다 → F 의 주신장 · 회전을 점 색으로 [카드 추론] |
| 기준 해 | 같은 영역을 Q4 요소로 쓴 FEM (Fig. 19b) | 후보 B (입자별 FE) 와 MPM 을 같은 구성 · 같은 이산 영역에서 겹쳐 보는 꼴 |
| 대칭 경계 | 반대 방향 중력의 거울 막대를 붙임 (§4.5) | 노드 조건 없이 대칭을 거는 우회 (격자와 경계가 안 맞을 때) |
| 도구 | MMS 체적력 = MATLAB 기호 계산 (App. A.2) · 코드 이름 [미확인] | 우리 MMS 도 기호 계산 (sympy) 으로 체적력을 만들어 둔다 [카드 추론] |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | Sadeghirad 외 2011 | 우리 DEM (LIGGGHTS) | 우리 MPM (Taichi scaffold) |
|---|---|---|---|
| 이산화 | GIMP 계열 · **선형 (hat) 격자 기저** (Fig. 3) · 입자 영역 (top-hat) · CPDI = 평행사변형 + 모서리 Q4 보간 · USL · 양해 | 구 입자 · 접촉 법칙 | **MLS-MPM · 2차 B-spline · APIC** · 입자 영역 없음 · 양해 [다른 카드 — `gritton2017_…` §8-1 (그 카드의 우리 코드 판독)] |
| 셀당 물질점 | 방향당 2 (MMS) · 3 (막대 · 보) | — | 방향당 2 (셀당 8) [같은 출처] |
| 물체 크기 ÷ 셀 | 막대 · 보 두께 1 m = **2 셀** (일부러 거침) · 링 두께 0.2 m = 2–16 셀 [카드 산술] | — | SE 지름 ≈ 1 µm ≈ **7 셀** (dx 0.141 µm · n_grid 384) · SE 채널 d_h/dx ≳ 3.5 규칙 [우리 기록 — `comparison_vs_ours_DEM.md` A · B 절의 같은 규칙] |
| 재료 | 압축성 neo-Hookean · E 1e6–1e7 Pa · ν 0 · 0.3 | hooke/hysteresis · E_eff 1.35 GPa (18 배 연화) | J2 · E 1.53 GPa · ν 0.49 (K 25.5 · μ 0.51 GPa) · σ_y 0.30 GPa [우리 기록] |
| 하중 | MMS 체적력 · 계단 중력 (동적) | 판 압축 ≈ 300 MPa | 판 압축 ≈ 300 MPa · 판 Mach 0.01–0.03 (준정적) [우리 기록] |
| 시간 간격 | Δt = 0.4h/C (C = √(E/ρ₀) 막대 파속) · 막대 · 보는 고정 Δt | — | 0.4 dx/√M (ρ = 1 규약) [다른 카드 — `gritton2017_…` §0] — M 이 P파 계수인지 이 카드에서 확인하지 않았다.  원문 식을 ν 0.49 에 그대로 쓰면 P파 기준 Courant 1.66 [카드 산술 · §4-5] |
| 물체 사이 접촉 | 없음 (한 물체 · no-slip 자동) | 있음 (마찰 · 분리) | 없음 (붙음 · `grid_v` 한 벌) [다른 카드] |
| 큰 신장 대책 | CPDI (영역 추적 · 멀리 떨어진 입자 연결) | — | 2차 B-spline (C¹ · 지지 3 셀) — 영역 추적 없음 |
| 검증 | MMS 해석해 2 건 + 방법끼리 · FEM 비교 | 실험 기공 · 접촉 겹침 | 실험 기공 (보정) · DEM 두께 대조 [우리 기록] |
| 차원 | **2D 평면 변형률** | 3D | 3D |

### 8-2. ★ "우리 B-spline MLS-MPM 은 어디까지 늘어나도 되는가" — 원문 시험 범위와 우리 범위를 나란히 (판정하지 않는다)

| 항목 | 원문 (2D · 탄성 · 동적) | 우리 MPM (3D · J2 · 준정적 압밀) |
|---|---|---|
| 변형의 꼴 | 축 정렬 파 · 원주 늘어남 (직사각형 → 평행사변형) · 자중 인장 · 큰 회전 | SE 가 AM 사이 틈 · 기공으로 흐르는 소성 유동 (등체적에 가깝다) · 판 · AM 에 눌린 납작해짐 |
| 크기 | F 0.69–1.31 (①) · 원주 0.74–1.26 (②) · 평균 신장 ×2.78 · 꼭대기 줄 국소 ×4.0 (③ g 1000) · ×9.75 · 국소 ×15.2 (③′ g 3500) · 자유 끝 쪽 ≈ 90° 회전 (④) [카드 산술 · 판독 · §3-4b] | 층 체적 변형 ε ≈ 0.1–0.3 (기공 닫힘 · 지시서의 우리 범위) → 옆이 막힌 일축 압밀이면 층 높이 비 0.7–0.9 [카드 산술] · 물질점의 체적 변형은 300 MPa ÷ K 25.5 GPa ≈ **1.2 %** [카드 산술] → 층의 부피 감소는 거의 전부 기공 닫힘 + 물질점의 **편차 (모양) 변형** · 물질점 하나가 등체적 일축으로 축 0.7 · 0.5 까지 눌리면 옆 ×1.20 · ×1.41 [카드 산술 · 예시 — 실제 물질점 값 아님] · 접촉부 · 틈의 국소 큰 변형 — **물질점 신장 분포는 미측정** |
| 해상도 | 막대 2 셀 폭 · 셀당 3 × 3 · 링 4 해상도 · *"if sufficient refinement is used"* 면 안정 | SE 지름 ≈ 7 셀 · 셀당 2 × 2 × 2 |
| 원문 기준을 우리 기저에 옮기면 [카드 산술 · 원문 시험 아님] | uGIMP (셀당 3 · 영역 h/3 · 영향 반폭 h + h/6) 의 '영향 영역 안 겹침' 신장 = **×7** — 그런데 uGIMP 는 CPDI 해의 국소 신장이 ×4.0 을 넘지 않는 막대 문제 (g 1000) 에서 끊겼다 (끊긴 때 · 그때 uGIMP 자신의 국소 신장은 [미확인]) · cpGIMP 는 국소 ×4 · 이웃 줄 간격 1.25 셀에서 틈 (원인 = 전단 무시) · CPDI 는 국소 ×15 · 간격 4.8 셀에서도 이어짐 [판독 · §3-4b] | 2차 B-spline 의 영향 반폭 1.5 dx · 처음 간격 0.5 dx → 축 하나로 **×6** 이면 이웃 물질점이 노드를 하나도 공유하지 않는다 — 원문 사례로 보아 **상한일 뿐 안전 문턱이 아니다** [카드 추론] |
| 판정 수단 | 그림 (토막 · 틈 · 겹침) · 계산 완주 여부 | 없음 — 제안 (§10 행동 1–2): 물질점 최근접 간격 ÷ dx · F 주신장 분포 · 질량 0 인 내부 노드 수 |

- 원문이 주는 것은 **"해상도를 조이면 안정해진다" 와 "격자 축과 안 맞는 계단 배치는 어떤 방법도 틀리게 한다"** 의 두 정성 사실과, 우리 코드에 그대로 돌릴 수 있는 **시험 문제 셋** (MMS 둘 · 자중 막대) 이다.
- 우리 압밀 범위 (층 높이 비 0.7–0.9 · 등체적 소성) 는 원문 시험의 아래쪽 (①② 의 ±30 % 와 같은 자릿수) 에 있고 막대 (평균 ×2.8 · ×9.7 · 국소 ×4 · ×15) 보다 작다 — 단 **우리 물질점의 국소 최대 신장은 재지 않았다** [우리 기록 없음 · 카드 추론].  우리 기저 (2차 B-spline) · 소성 · 거의 비압축 · 3D 는 원문 시험 범위 **밖**이다.

### 8-3. 전이되는 것 / 안 되는 것

- ✅ **세 불안정의 정의 · 원인 문장** (cell crossing · ringing · extension) — 원문 인용 그대로.
- ✅ **CPDI 식 (21)–(26)** — 후보 A′ 계열 (입자마다 영역 · 형상 추적) 이나 큰 신장 대책을 고를 때의 원전.  단 r 규약 (§4-4) 을 단위 시험으로 고정.
- ✅ **검증 문제 셋** — MMS 단위 정사각형 · 링 (식 31–38 · A5–A9 · MATLAB) + 자중 막대 (§4.3 조건 전부 인쇄) → 단계 2 의 단위 시험.
- ✅ **함정 둘** — 오차 노름의 ÷ (N_t × N_p) · 막대 파속 기준 Δt (ν 0.49 에서 CFL 위반).
- ✅ **방법끼리의 상대 수치** (Fig. 4 · 7 · 19) — "표준 MPM 은 이 시험에서 RMS 로 수렴하지 않는다" · "계단 배치는 FEM 도 틀린다" 같은 문장.
- ❌ 재료값 (E · ν · ρ · g · A) — 전부 가상 · 동적 검증용.
- ❌ 신장 문턱 숫자 — 원문에 없다 (§8-2 의 ×6 · ×7 은 카드 산술 상한).
- ❌ B-spline · MLS · 3D · 소성 · 거의 비압축 · 준정적의 성능 — 시험 밖.
- ❌ 비용 — 수치 없음.
- ⚠ CPDI 의 '멀리 떨어진 입자 연결' 은 **분리를 막는 성질**이다 → 단계 6 (탈압 · 판 · AM 에서 떨어짐) · R2 (분리) 에는 오히려 걸림돌일 수 있다 [카드 추론] — `homel2017_…` 은 실패 입자에 *domain scaling* 을 걸어 *"nonphysical stretching of failed material across the domain"* 을 막았다 [다른 카드 §4-10].

### 8-4. frame 판정

- **frame [5] (분업)**: 이 논문은 MPM 쪽 절반 (연속체 큰 변형) 의 **수치 기반**만 다룬다 — 소성 · 형상 변화의 물리도, DEM 쪽 절반 (접촉망 · 패킹) 도 없다.  분업은 그대로이고, "MPM 이 큰 변형에 강하다" 는 말의 **조건** (해상도 · 영역 처리 · 계단 배치) 을 적는 근거가 하나 는다.
- **frame [4] (교차 맞춤 금지)**: 실험에 맞춘 값이 없다 · 충돌 없음.  이 논문을 우리 MPM 결과의 검증 근거로 인용하지 않는다 (방법 · 시험 꼴의 원전으로만).
- **frame [1]/[2] (연화)**: 중립 — 단 우리 연화 SE (E 1.53 GPa · ν 0.49) 는 원문 재료 (ν ≤ 0.3) 와 달리 거의 비압축이라 Δt · 체적 거동의 시험 범위 밖이다 [카드 산술 · 카드 추론].

---

## 9. 깊은 통찰

① **"MPM 은 큰 변형에 강하다" 에는 조건이 셋 붙는다 — 원문이 스스로 보였다.**  (a) 기저가 매끈해야 (셀 넘김 · ringing) (b) 영향 영역이 겹쳐 있어야 (extension) (c) 입자 배치가 경계 · 변형 방향에 맞아야 (mesh(b) 는 CPDI 도 실패).  그리고 (d) *"if sufficient refinement is used"* 면 다 안정하다는 진술 — 끊김은 해상도 현상이기도 하다.  우리 원고 · 덱에서 "MPM 이 큰 변형을 푼다" 를 쓸 때 이 조건을 붙인다.

② **표준 MPM 의 오차는 이 시험에서 격자를 조일수록 커진다 (RMS) — 그림에서는 줄어드는 것처럼 보인다.**  식 (27) 의 ÷ (N_t × N_p) 때문에 그림 기울기가 1.5 커진다 [카드 산술].  표준 MPM 의 그림 기울기 0.74 를 RMS 로 되돌리면 −0.76 (끝 ↔ 끝 · 이웃 −0.37 · −1.16 · −0.75) — RMS 오차가 A 의 9 → 45 % 로 커진다.  같은 계열 `gritton2017_…` 식 (15) 도 ÷ N 이었다 — 노름의 정의를 결과 전에 적고 RMS 로 보고하는 것이 우리 규칙이어야 한다.

③ **CPDI 의 연결성은 양날이다.**  멀리 떨어진 입자를 대체 기저로 이어 extension instability 를 없앴는데 (*"remain 'in contact' even when they are far from each other"*), 같은 성질은 진짜 분리 (파괴 · 탈착 · 판에서 떨어짐) 도 막는다 [카드 추론].  homel2017 이 실패 입자에 domain scaling 을 건 까닭이 이것과 같은 줄에 있다.  우리 단계 6 (탈압) 의 분리는 기저가 아니라 **접촉 규칙** (후보 A′-0 · A′) 이 맡아야 한다.

④ **영역 안에서 기저가 거칠어진다는 대가가 FEM 비교로 숫자가 됐다.**  같은 영역을 Q4 요소로 쓴 FEM 과 CPDI 는 첫 골 1.2 % · 2.6 s 에서 0.26 m (흔들림 3.2 m 의 8 %) 갈라진다 [판독 · 카드 산술].  Fig. 3 의 S_k^app = 0 (늘어난 영역 안의 노드가 빠짐) 이 그 기전의 그림이다.  "CPDI = 정확" 이 아니라 "CPDI = 늘어나도 이어지는 거친 근사" 로 읽는다.

⑤ **방법을 바꾸기 전에 배치를 바꿔라.**  돌린 막대에서 계단 배치 (mesh(b)) 는 uGIMP · cpGIMP · CPDI 를 모두 실패시켰고, 돌린 보에서는 FEM 까지 틀리게 했다.  경계에 맞춘 평행사변형 배치 (mesh(c)) 만 원래 답을 냈다 (골 0.7 % 차).  우리 `--se-dump` 씨앗 (구를 복셀로 채움) 의 표면은 계단이다 [우리 기록] — SE 구 표면의 계단이 국소 응력 · 피복에 주는 몫은 아직 재지 않았다 [카드 추론].

⑥ **시간 간격 식에 들어가는 파속을 확인한다.**  원문의 Δt = 0.4h/C 는 C = 막대 파속 (*"not the uniaxial strain wave speed"*) — ν ≤ 0.3 에서는 P파 기준 Courant 0.4–0.46 이지만 우리 SE (ν 0.49) 에서는 1.66 이 된다 [카드 산술].  우리 코드의 √M 이 P파 계수라면 문제없다 — 원문 식을 가져올 때 파속의 정의부터 맞춘다.

⑦ **이 논문의 '거침' 은 의도된 시험 설계다.**  막대는 폭 2 셀 · 셀당 9 입자 (입자 36 개) 로 불안정을 일부러 끌어냈다.  우리 SE 는 지름 ≈ 7 셀로 훨씬 곱다 — 같은 현상이 우리에게서 나타날 자리는 SE 몸통이 아니라 **틈으로 밀려 들어간 얇은 목** (d_h/dx 가 작은 곳) 이다 [카드 추론].  우리 기존 해상도 규칙 d_h/dx ≳ 3.5 (응력 해상) 와 별개로, 그 목에서의 물질점 간격 ÷ dx 를 감시량으로 둘 근거다.

⑧ **2D → 3D 는 "self-evident" 한 문장이 전부다.**  3D 로 옮기면 모서리 8 개 × 노드 8 개 = 입자당 64 노드 · 영역 벡터 성분 9 개 (벡터 셋) [카드 산술 · 선형 격자 기저 기준] — 비용 · 정확도 · 6 면체 영역의 뒤틀림은 이 논문 밖이다.  gritton2017 · homel2017 의 3D 계산은 이 원전의 시험 범위를 넘어선 사용이다.

---

## 10. ★ 자세한 분석 — 우리 계획에 무엇을 주나 (정독 지시서 3 절의 이름)

> 우리 랩 기준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 안 함) 과 나란히 놓을 숫자: **이 논문에 없음** (기공 · 밀도 · 압력 · 실제 재료 0 건).  우리 DEM (18 배 연화 · E_eff 1.35 GPa · Heckel P_y 138 MPa) · MPM (E 1.53 · σ_y 0.30 GPa · ν 0.49) 과 견줄 재료값도 없다 — 견줄 자리는 **이산화 · 해상도 · 시간 간격 · 검증 꼴**뿐이다.

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 조건 차이 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준을 결과 전에) | 입자 부피 V_p = J V_p⁰ (식 15) = 물질점으로 추적한 고체 부피의 식 · 오차 노름의 함정 (식 27 · 결과 전에 RMS 로 정의) · "판정 = 그림" 의 반면교사 | 기공 · 밀도 연산자 없음 |
| **단계 1** (입자마다 속도장 · 3D 메모리) | CPDI 를 얹으면 입자당 영역 벡터 성분 (2D 4 · 3D 9 개) + 모서리 (3D 8 개) 의 기저 계산 · 노드 접근 2D 16 · 3D 64 [카드 산술 · 선형 격자 기저 기준 — 2차 B-spline 이면 모서리마다 3 × 3 (× 3) 노드라 더 많다] | 측정된 비용 0 · 3D 구현 0 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★ **시험 문제 셋이 그대로 있다**: MMS 단위 정사각형 (식 31–36 · ±31 %) · MMS 링 (식 37–38 · 원주 26 %) · 자중 막대 (§4.3 · 1 × 1 m · E 1e6 · ρ 1050 · g 1000 / 3500 · 4 셀 × 3 × 3) + 비교 수치 (Fig. 4 · 7 · 11 · 12b) · 막대 파속 Δt 의 함정 | 소성 · ν 0.49 · 2차 B-spline 의 결과는 없다 — 우리 코드로 돌려 얻는 값은 원문 수치와 **같은 기저가 아니므로 숫자 대조가 아니라 모양 대조** (끊기는가 · 수렴 차수) |
| **단계 3** (2D 접촉 표현 비교: 한 속도장 ↔ 입자별) | 한 속도장 = no-slip 자동 (p.1436) 의 원전 문장 · CPDI 의 연결성은 분리를 막는다는 점 [카드 추론] | 접촉 알고리즘 · 다물체 시험 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | "refinement 하면 안정" · 계단 배치 경고 → 씨앗 표면 계단의 영향을 따로 재라 [카드 추론] | 3D · 소성 · 압밀 · 실험 앵커 없음 |
| **단계 5** (3D 복합) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | 탄성 진동이 거의 감쇠 없이 되돌아오는 그림 (막대 q 0.19 s 에 −0.01 m · Fig. 11) — 우리 코드의 수치 감쇠 점검 꼴 [카드 추론] · CPDI 연결성 = 분리 방해 (§9 ③) | 하중 제거 · 소성 되돌아옴 · 분리 없음 |
| **단계 7** (형상 · 피복 · 수송) | 영역 (평행사변형) 으로 국소 찌그러짐을 그리는 꼴 (Fig. 8 · 14) | 피복 · 수송 없음 |
| **후보 D0** (지금 DEM) | 없음 (DEM 0 회) | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 필요성의 간접 근거 — 한 속도장은 붙음 (p.1436) | 방법 없음 |
| **후보 A** (AM 강체 · SE 한 속도장) | 큰 신장에서 한 속도장 MPM 이 끊기는 조건 (§8-2) — SE 가 틈으로 흐를 때의 해상도 점검 | 강체 결합 없음 |
| **후보 A′** (입자마다 속도장) | 입자 영역 추적 (CPDI) 을 입자별 장과 함께 쓸 때의 기저 원전 · Homel 2017 이 CPDI 위에서 장 분할을 했다 [다른 카드] | 다물체 없음 |
| **후보 B** (입자별 FE + 접촉) | FEM (영역 = Q4 요소) 비교 — 같은 이산 영역에서 CPDI 는 FEM 보다 거칠다 (Fig. 19 · §9 ④) · 계단 배치는 FEM 도 틀린다 | 접촉 · 소성 · 큰 압밀 비교 없음 |
| **후보 C · C′** (큰 변형 접촉 DEM · 캡 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0** (접촉 끈 것과 같은지) | — | — |
| **U1** (입자 하나 압축 · 해상도) | 해석해 대비 수렴 시험의 꼴 (MMS) · 노름 정의 | 입자 하나 압축 문제는 없음 |
| **U2–U5** | 없음 | — |
| **U6** (작은 조밀 충전 압축의 해상도 수렴) | "refinement 하면 안정" (결과 미제시) · 수렴 보고 꼴 | 충전 · 압축 없음 |
| (새 단위 시험 후보 — 이름 없음) | ★ **늘어남 시험**: 자중 막대 (§4.3) 를 우리 MLS-MPM 으로 — 끊기는 g · 해상도 · 물질점 간격 ÷ dx 를 기록 | 원문 숫자와 직접 대조 불가 (기저 다름) |
| **R1** (AM 이 움직이고 하중을 나눔) | 없음 | — |
| **R2** (미끄럼 · 분리) | 한 속도장 = 붙음 (p.1436) · CPDI = 멀리서도 연결 (p.1446) → 분리는 기저가 아니라 접촉 규칙의 몫 [카드 추론] | 분리 시험 없음 |
| **R3** (SE 입자 경계 기억) | 영역 추적 = 물질점 하나의 영역 경계를 기억 (알갱이 경계 아님) [카드 판독] | 알갱이 경계 없음 |
| **R4** (탈압 · 되돌아옴) | 탄성 진동의 되돌아옴 그림만 | 없음 |
| **R5** (맞추는 값 하나) | 맞춘 값 0 (검증 문제) | — |
| **R6** (SE 입자 형상 변형) | 큰 회전 · 전단에서 영역 (= 국소 형상) 을 F 로 따라가는 법 · cpGIMP 의 실패 (90° 에서 영역 0) | 소성 형상 변화 · 접촉 없음 |
| **R7** (AM 파괴) | 없음 — CPDI 는 오히려 끊김을 막는다 | — |
| **결과 전 대조 항목** | 우리 MLS-MPM 으로 MMS 두 건을 돌릴 때 견줄 것 = 수렴 **차수** (RMS 로 2 차 = CPDI · cpGIMP 의 정사각형 · §3-2 — N_t = T/Δt 로 읽은 [카드 산술]) — 값 자체는 기저가 달라 견주지 않는다 | — |

**구체 행동 (싼 것 → 비싼 것 · 전부 [카드 추론] · 결과 전 등록 대상)**
1. **물질점 간격 · 신장 감시 (단계 4 · R6 · 새 런 0)** — 기존 압밀 출력 (real_14 등) 에서 끝 상태의 F_p 주신장 분포 (최대 · 99 분위) 와 물질점 최근접 간격 ÷ dx 를 센다.  원문 시험 범위 (§3-5) 와 나란히 적는다 — 판정하지 않는다.  ⚠ `gritton2017_…` §10 행동 2 의 "1 셀" 문턱은 원전 근거가 없다 → 문턱은 아래 2 의 시험으로 정한다.
2. **늘어남 단위 시험 (단계 2)** — §4.3 의 자중 막대를 우리 2D MLS-MPM (2차 B-spline · 셀당 2 × 2 · 3 × 3) 으로: g 를 올리며 처음 끊기는 g 와 그때의 국소 신장 · 간격 ÷ dx 를 기록 · 해상도 (막대 폭 2 · 4 · 8 셀) 사다리.  원문 (uGIMP · cpGIMP 는 g 1000 에서 끊김 — cpGIMP 는 꼭대기 줄 국소 ×4 · 이웃 줄 간격 1.25 셀에서 틈 · CPDI 는 3500 에서 국소 ×15 · 간격 4.8 셀에도 이어짐 [판독 · §3-4b]) 과는 모양만 견준다.
3. **MMS 두 건 (단계 2 · U1)** — 식 31–38 의 체적력을 기호 계산으로 만들고 (App. A.2 꼴) RMS 노름 (÷ √(N_t N_p)) 으로 수렴 차수를 잰다.  ν 0.49 판 (거의 비압축) 을 하나 더 — 원문 밖이므로 우리 쪽 새 결과로 표지.
4. **Δt 식의 파속 확인 (단계 2 · 4)** — 우리 코드의 √M 이 P파 계수 (λ + 2μ) 인지 확인하고 산출물에 Courant 수 (P파 기준) 를 적는다.
5. **씨앗 표면 계단의 몫 (단계 4 · 7)** — 같은 SE 구를 복셀 채움 ↔ 경계에 맞춘 배치 (구면 껍질) 로 씨앗해 국소 응력 · 피복의 차를 한 번 잰다 (원문 §4.5 의 교훈).
6. **(분리가 필요해질 때) CPDI 형 기저를 넣지 않는다** — 분리 (단계 6 · R2) 는 접촉 규칙 (A′-0 · A′) 으로 · 영역 추적형 기저를 쓰게 되면 실패 입자의 영역 축소 (Homel 의 domain scaling) 를 같이 둔다.

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | 2D 사례만 | p.1436 *"for clarity, however, only two-dimensional case studies are described in this paper"* · p.1452 *"limited to 2D deformations"* |
| 2 | 평행사변형 → 평행사변형만 | p.1451 *"Although we have limited the scope in this paper to parallelogram particle domains"* · p.1452 *"limited to the case of parallelograms deforming to parallelograms"* |
| 3 | 영역 틈 · 겹침이 CPDI 에도 남는다 | p.1446 *"These gaps and overlapping, although present, are much smaller when using the CPDI method"* |
| 4 | 끊김 없음은 "이 예제에서" | p.1446 *"Thus this method does not suffer from extension instability in this example"* |
| 5 | 계단 배치에서는 CPDI 도 실패 · 부정확 | p.1448 (막대 mesh(b) · *"cannot be completed"*) · p.1450 (보 mesh(b) · *"not accurate"*) |
| 6 | 대체 기저는 영역 안에서 표준 기저와 크게 다르고 FEM 보다 거칠다 | p.1452 *"can differ significantly"* · p.1451 *"coarser than the FEM basis functions"* |
| 7 | F 를 영역 안에서 일정하다고 둠 | 초록 · p.1440 *"the deformation gradient is approximately constant over the particle domain"* |
| 8 | 1D 에서만 정확 (노드 내부력) | p.1441 |
| 9 | refinement 결과는 미제시 | p.1448 · 1450 *"not presented here"* |
| 10 | 축 정렬 시험은 대표성이 없다 | p.1443 *"This example is not representative of general material deformations"* |
| 11 | 일반 볼록 다각형 · 경계에 맞춘 영역으로의 확장은 Q4 를 일반화한 효율적 보간자가 있을 때만 | p.1451 *"the concept should be straightforward to generalize to more general convex polygons that conform to complicated boundaries, provided that an efficient interpolator (i.e. generalization of Q4 shape functions) is available"* |

저자가 **적지 않은** 한계 (카드가 본 것 — §12 와 겹침): 소성 · 거의 비압축 · 접촉 · 분리 · 준정적 · 3D 의 시험 부재 · 계산 시간 부재 · 끊김 문턱 숫자 부재 · 오차 노름의 ÷ (N_t N_p) · 모서리 규약 미인쇄.

## 12. 불확실 · PDF 에 없는 것 · 인쇄 어긋남

**없는 것** — §3-7 표.

**인쇄 어긋남** (전부 [카드 판독] — 식 그림은 인쇄 그대로 잘랐다)

| # | 자리 | 인쇄 | 카드의 읽기 |
|---|---|---|---|
| 1 | 식 (25) · p.1442 | *"¼{S_i(x₁) + … + S_i(x₄))}"* | 닫는 괄호 하나가 더 있다 — 뜻은 모서리 넷의 평균 |
| 2 | 식 (27) 아래 · p.1442 | *"in which Nt and Np are total number of particles and time steps, respectively"* | 기호가 뒤바뀜 — 식에서 i = 1..N_t 는 시각 t_i, p = 1..N_p 는 입자 x_p |
| 3 | 식 (27) · p.1442 | √(ΣΣ e²) / (N_t × N_p) | 제곱근 밖에서 개수로 나눔 → RMS ÷ √(N_t N_p) · 그림 기울기 = RMS 차수 + 1.5 (N_t ∝ 1/h 일 때) [카드 산술] |
| 4 | Fig. 5 · Fig. 8 라벨 | t = 0.0 · 0.05 · 0.15 | 인쇄 T = 0.02 s (한 주기 · p.1443 · 1444) 밖.  식 (31)(37) 대로면 t = 0.05 s 에서 sin(5π) = 0 (변위 0) 인데 그림은 크게 변형돼 있다 → 최대 · 최소 변위 시각 0.005 · 0.015 s 가 맞고 라벨은 **10 배**로 인쇄됐다고 읽는다 [카드 산술] |
| 5 | Fig. 2 ↔ 식 (26) | r 화살표 = 중심 → 변 (반 길이) | 식 (26) 은 r 을 변 전체 벡터로 읽을 때만 선형장에서 정확 (반 길이면 ½ 배) [카드 산술 · §4-4] — 그림이 개략일 수 있다 · 모서리 식 미인쇄 |
| 6 | 식 (11) | ∇φ_ip v_i 순서 | 속도 기울기의 텐서 곱 순서 (v ⊗ ∇φ) 를 적지 않은 표기 — 성분 규약 [미확인] |
| 7 | 식 (A3) | P = λ ln J F⁻¹ + μF⁻¹(FFᵀ − I) | 공칭 응력 (= (Jσ F⁻ᵀ)ᵀ) 꼴 · 두 MMS 장은 F 가 대칭 (정사각형 = 대각 · 링 = 반지름 대칭) 이라 두 규약의 차가 없다 [카드 산술] |
| 8 | §2.1 ↔ §2.2 | 노드 기저 φ_i ↔ S_i | 같은 것을 두 기호로 |
| 9 | Fig. 7 | x 축 위 범례 없는 네모 넷 | 뜻 미인쇄 [미확인] |

**서지**: 후보 표 N-15 의 서지 (저자 셋 · 제목 · IJNME 86 · 1435–56 · 2011) 와 원문이 같다.  덧붙임: DOI 10.1002/nme.3110 · 온라인 2011-03-10 · 호 12 (워터마크 줄 [카드 판독]).  Gritton 2017 본문의 *"Sadeghirad and Brannon [38]"* 은 저자 둘만 적은 Gritton 의 표기다.

## 13. 인용 가능 문장 (덱 · 원고용)

- "표준 MPM 은 입자가 셀 경계를 넘을 때 격자 기저 함수가 매끈하지 않아 생기는 '셀 넘김 불안정' 을 겪고, 입자 영역을 고정한 GIMP (uGIMP) 는 큰 인장에서 입자의 영향 영역이 더는 겹치지 않을 때 '확장 불안정 (extension instability)' 을 겪는다 (Sadeghirad, Brannon & Burghardt, Int. J. Numer. Meth. Engng 86, 1435–1456, 2011, §1 · §2.2)."
- "입자 영역을 전체 변형 경사로 평행사변형으로 실어 나르고 격자 기저를 영역 모서리에서 보간하는 CPDI 는, 2D 자중 막대 시험에서 표준 MPM · uGIMP · cpGIMP 가 끊기는 조건 (g = 1000 m/s²) 과 그 3.5 배 하중에서도 이어진 해를 냈다 (같은 문헌 §4.3)." — 한정어: 2D · 탄성 · 동적 · 격자 4 셀 · 계단 배치 (mesh(b)) 에서는 CPDI 도 실패 (§4.5).
- "MPM 의 큰 변형 안정성은 해상도와 입자 배치에 달려 있다 — 격자 축과 맞지 않는 계단 배치는 GIMP · CPDI 와 같은 영역의 FEM 모두를 틀리게 했고, 저자는 충분히 조이면 안정해진다고 적었다 (같은 문헌 §4.5)."
- ⛔ 쓰지 않을 문장: "CPDI 는 극단 인장에서 수치 파괴가 없다" (원문 = 이 예제 · mesh(b) 실패) · "MPM 은 신장 ×N 까지 안전하다 (Sadeghirad 2011)" (문턱 숫자 없음) · "CPDI 는 3D 에서 검증됐다" (2D 만) · "CPDI 는 비용 증가가 없다" 를 수치처럼 (측정 없음).

## 14. 기법 미니 용어집

- **CPDI (convected particle domain interpolation)** — 입자 영역을 전체 변형 경사 F 로 평행사변형으로 실어 나르고 (convect), 표준 격자 기저를 영역 네 모서리에서 Q4 로 보간한 대체 기저로 φ_ip · ∇φ_ip 를 닫힌 꼴로 계산하는 MPM 변종.  이 원전은 2D.
- **GIMP (generalized interpolation material point)** — 입자를 점 대신 유한 영역 (특성 함수 χ_p) 으로 두고 격자 기저를 그 영역에서 평균해 φ_ip 를 만드는 MPM 일반화 (Bardenhagen · Kober [3]).
- **uGIMP · cpGIMP** — 이 논문의 이름: 영역을 그대로 두는 GIMP · 영역을 직사각형으로 두고 F 의 대각 성분으로 크기만 바꾸는 GIMP.
- **cell crossing instability** — 입자가 셀 경계를 넘을 때 기저 함수 (특히 기울기) 의 매끈하지 않음 때문에 생기는 오차 · 불안정.
- **ringing instability** — 표준 MPM 에서 셀 경계를 넘는 순간 기저 기울기의 계단이 만드는 진동.
- **extension instability** — 큰 인장에서 입자들의 영향 영역이 더는 겹치지 않아 연속체가 수치적으로 끊기는 현상 (SPH 의 tensile instability 와 다르다 — 저자 감사의 글).
- **spurious material separation** — 물리적 원인 없이 재료가 떨어져 나가는 계산 결과 (외팔보의 표준 MPM · cpGIMP).
- **대체 격자 기저 (alternative grid basis) S_i^app** — 영역 모서리에서의 표준 기저 값을 Q4 형상함수로 보간한 함수.  단위 분할 · 모서리에서 표준 기저와 같음 · 영역 안에서는 다를 수 있음.
- **Q4** — 4 절점 사변형 유한요소의 쌍선형 형상함수.
- **MMS (method of manufactured solutions)** — 해를 먼저 정하고 그 해를 만드는 체적력을 거꾸로 구해, 코드가 그 해를 되찾는지로 검증하는 방법.
- **USL / USF** — 격자 속도를 갱신한 뒤 (Last) / 앞서 (First) 응력을 갱신하는 순서.
- **막대 파속 (thin bar wave speed)** — √(E/ρ₀).  일축 변형 (P파) 파속 √((λ + 2μ)/ρ₀) 보다 작다 (ν 0.49 에서 4.14 배 차).
- **평면 변형률 (plane strain)** — 두께 방향 변형 0 (F_zz = 1) · 두께 방향 응력은 0 이 아니다.
- **CVT (centroidal Voronoi tessellation)** — 경계에 맞춘 입자 배치를 만드는 방법 (ref [31]).

## 15. 관련 카드

- `gritton2017_mpm_chemomechanical_coupling_silicon_anode` — CPDI (Uintah · 3D) 로 규소 나노기둥 리튬화를 계산한 카드 (ref [38] = 이 논문 · 그 카드 §4-1 · §9 ⑨ 가 이 원전을 가리켰다).
- `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — CPDI (GEOS · 3D) + domain scaling 위에서 장 분할 접촉 · 파괴 (CPDI 의 연결성을 실패 입자에서 끊는 장치).
- `devaucorbeil2020_mpm_after_25_years_review` — MPM 변종 표의 CPDI 줄 (2 차 인용 대조 §0-1).
- `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MPM 이산화 (MLS-MPM · 2차 B-spline) 의 원전 — 이 논문이 다루지 않는 기저.
- `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 이 논문에 없는 다물체 마찰 접촉 · 분리 (이 논문의 ref [7] 이 2001 판).
- `bardenhagen2005_mpm_foam_densification_simulation` — GIMP 로 발포체를 치밀화 끝까지 누른 계산 (큰 **압축** 쪽 선례).
- `stomakhin2013_mpm_snow_elastoplastic` — 우리 MPM 탄소성 갱신의 계보 (소성 · 큰 변형 · 2차 B-spline 쪽).
- `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` — MPM 으로 변형 입자의 압밀까지 간 2D 선례 (이 논문에 없는 다입자 · 접촉).
- `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` — GIMP 원전 (입자 특성 함수 χ_p · 가중 일반 꼴 식 19–20 · contiguous particle GIMP · 1D 셀 넘김 잡음 · 수렴) — 이 카드의 uGIMP = 그 예제의 'GIMP' (폭 고정) · cpGIMP = 1D 에서 'Finite GIMP' (폭 추적) [카드 판독] · 2026-11-12 반입.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

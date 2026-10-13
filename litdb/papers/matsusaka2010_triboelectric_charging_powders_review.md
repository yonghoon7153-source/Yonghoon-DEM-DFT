<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_particle_size_consolidation_strain_lpscl.md · 같은 묶음 = johnson1971_jkr_surface_energy_contact_elastic_solids.md · begat2004_cohesive_adhesive_balance_afm_colloid_probe.md · deng2021_mechanical_surface_energy_tester_bond_number.md.
     원문 = 27 쪽 (p.5781–5807) · 리뷰 · SI 없음 · 쪽 표기 = 인쇄 쪽 (PDF n 쪽 = p.(5780 + n)).
     태생 디지털 PDF — 그림은 대부분 벡터 도면.  텍스트층은 µ 를 m 으로, − 를 빈칸으로 잃는다 → 단위 · 부호는 렌더한 글자로 확인했다 (원문 대조 기록).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 인쇄 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 벡터 경로 좌표) /
     [우리 산술] = 원문 값으로 한 계산 / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->
# Triboelectric charging of powders: A review — 분말은 손대는 공정마다 **마찰 대전**된다 · 전하 이동 기전 (전자 · 이온 · 물질) · **축전기 모형 Δq = k_c·C·V** 와 **전하 완화 (Paschen) 모형** 이 반복 충돌에서 같은 지수식 q = q₀e^{−n/n₀} + q∞(1 − e^{−n/n₀}) 을 낸다 · 습도 ↑ · 온도 ↑ 면 대전 ↓ · 코팅이 부호를 바꾼다 · 측정법 (Faraday 통 · blow-off · Kelvin–Zisman CPD · E-SPART · 충돌 시험 · AFM) · DEM 대전 모사 — Matsusaka · Maruyama · Matsuyama · Ghadiri (Chemical Engineering Science 2010)

> slug `matsusaka2010_triboelectric_charging_powders_review` · DOI `10.1016/j.ces.2010.07.005` · type `review (triboelectric / contact charging of powders: electron, ion and material transfer; condenser and charge-relaxation models; repeated-impact and gas–solids pipe-flow charging; Faraday cage, blow-off, Kelvin–Zisman CPD, charge-distribution, impact and AFM measurements; applications; Monte Carlo and DEM charging simulations)` · PDF `0c514d40-39._Triboelectric_charging_of_powders_A_review.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: S. Matsusaka\* (Dept. of Chemical Engineering, Kyoto University) · H. Maruyama (Kyoto University) · T. Matsuyama (Dept. of Environmental Engineering, Soka University) · M. Ghadiri (Institute of Particle Science and Engineering, University of Leeds) · \* 교신 (matsu@cheme.kyoto-u.ac.jp) · *Chemical Engineering Science* **65** (2010) 5781–5807 · Review · 접수 2010-01-23 · 수정 2010-07-04 · 승인 2010-07-08 · 온라인 2010-07-14 · doi:10.1016/j.ces.2010.07.005 · 0009-2509 [인쇄 p.5781].  PDF 메타에는 DOI 가 없다 (인쇄본에서만 확인).
> 핵심어 (원문): Powder technology · Particulate processes · Triboelectric charging · Charge transfer · Characterization · Electrostatic application.  연구비: IFPRI · JSPS Core-to-Core Program · MEXT S0901039 [인쇄 p.5804].
> ★ **이 카드가 맡는 일** — 이종기술 논지 (`docs/hetero_thesis.md`) §2-7 *"마찰 대전 (정전기) — 건식 혼합에서 서로 다른 재료가 반대 부호로 대전돼 AM–SE 가 정전기로 붙을 수 있다 (모델에 없음)"* 의 **원리 · 크기 · 측정법 카드**.  우리 믹서 DEM (SJKR 점착만) 이 빠뜨린 힘이 얼마나 큰지 · 어떻게 재고 넣는지.
> **판독 원자료**: `litdb/figures/matsusaka2010_triboelectric_charging_powders_review/digitized.csv` (141 행 — Fig 14 · 15 · 21 · 29 · 34 · 65 벡터 · Fig 10 산화물 (지시선으로 이름 대응) · Fig 20 인쇄값 · Fig 63 눈 판독).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 서로 다른 두 표면이 닿았다 떨어지면 **유효 일함수 차 (접촉 전위차 V_c)** 를 따라 전자가 옮겨 가고 (§2.1), 입자의 전하는 충돌 횟수 n 에 대해 **평형값 q∞ 로 지수 접근**한다 — 축전기 모형 (Δq = k_c·C·V, C = ε₀S/z₀) 과 전하 완화 (Paschen 방전) 모형이 같은 식을 준다 (식 19 · 22) [인쇄 p.5788–5791].  리뷰는 그 측정법 · 제어법 · 시뮬레이션을 모은다; 배터리 소재는 없다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ 무엇을 재나 | 입자 전하 q (pC · nC) · **비전하 q/m (mC/kg · µC/kg)** — Faraday 통 (Fig 40–41) · 관통형 Faraday 통 (실시간) · **blow-off** (토너–캐리어, Fig 42) · 전하 분포 (층류 + 전기장 Fig 43 · E-SPART Fig 44 · PMAS · q-test · 낙하 셀 Fig 47) · **접촉 전위차 CPD** (Kelvin–Zisman 진동 축전기, Fig 38–39, 식 42) · 단일 입자 충돌 시험 (Δq vs 초기 전하 → Δq₀ · 평형 전하 q_e, Fig 19–20) · 관 흐름 전류 I/W_p (Fig 30–33) · **AFM 콜로이드 탐침** (정전기 + 반데르발스 분리 · 감도 ≈ 10 전자) | [인쇄] p.5789 · 5795–5799 |
| 기전 | **전자 이동** (금속–금속 = 일함수 차 식 1 · 절연체 = 유효 일함수 식 3 · 표면 상태 식 4 · 분자-이온-상태 식 5–6 · 양자화학) 이 바탕 · **이온 이동** (흡착수 · 전하 조절제) · **물질 이동** (취성 입자가 금속 벽에 조각을 남김 — 이론 모형 없음) | [인쇄] p.5782–5785 · 요약 (1) |
| ★ 모형 (DEM 에 넣을 꼴) | 축전기: Δq = k_c·C·V · C = ε₀S/z₀ · **V = V_c − V_e − V_b + V_ex** (V_e = k_e·q 영상 전하 · V_b = k_b·q 공간 전하) → 반복 충돌 dq/dn → **q = q₀·exp(−n/n₀) + q∞{1 − exp(−n/n₀)}** · 관 흐름 포화 **q_m∞ = 3ε₀V_c / (ρ_p D_p z₀ (1 + α))** · n₀ = πD_p² / (2k_c S (1 + α)) | [인쇄] 식 (8)–(12) · (19)–(21) · (31)–(32) |
| ★ 크기 | 산화물 미분 (0.3–0.5 µm) 대 표면 산화 철: **MgO ≈ +270 … V₂O₅ ≈ −290 mC/kg** [판독] · 미크론 알루미나 관 흐름 평형 **+7.0 (SUS316) … −8.5 mC/kg (황동)** [판독] · 비산재 3.9 mC/kg [인쇄] · 설탕 과립 (500–600 µm) 평형 전하 **−16 pC** · Δq₀ −0.5 / −0.9 / −1.6 pC (7 · 9 · 13 m/s) [인쇄] → 표면 전하 밀도 **≈ 1.4–2.0×10⁻⁵ C/m²** [우리 산술] | [인쇄 · 판독] Fig 10 · 20 · 21 · 31 · 34 |
| ★ 충돌 세기 | 평형 전하 q_e 는 충돌 속도 (≈ 5–28 m/s) 에 **무관 · 재료에 의존** (Fig 21) · Δq₀ 는 속도와 함께 커짐 (Fig 20) → 평형까지 충돌 수 n₀ = q∞/Δq₀ (식 23) = **32 · 18 · 10 회** (7 · 9 · 13 m/s) [우리 산술] · 충돌각 ≈ 60° 에서 최대 (구름–미끄럼, Fig 23–24) | [인쇄] p.5789–5791 + [우리 산술] |
| ★ 습도 · 온도 | 12.7 mm 금속구: 10 °C 에서 RH 0.1 → 0.7 이면 **21.0 → 11.9 nC (−43 %)** · 30 °C 에서는 13.7 → 11.5 nC (−16 %) · RH 0.1 에서 10 → 30 °C 면 21.1 → 13.7 nC [판독 벡터] — 습기 = 표면 전도 · 누설 ↑ | [판독] Fig 14–15 · [인쇄] p.5787 |
| ★ 코팅 | 티타니아 (0.15–0.3 µm) 에 알루미나를 입히면 대전이 **양 (+) 으로**, 실리카는 **음 (−) 으로** 이동 (Fig 13) — 표면이 바뀌면 부호도 바뀐다 · 고분자는 자외선 · 플라스마 처리로 조절 | [인쇄] p.5787 |
| 기하평균 결합 규칙 · γ | 원문 밖 (정전기 리뷰 — 표면 에너지 · 반데르발스 점착은 다루지 않는다).  AFM 측정이 "정전기 + 반데르발스" 두 힘을 가른다는 언급만 | [인쇄] p.5799 |
| 재현성 · 불확도 | **"In general, the reproducibility of the triboelectric charging of particles is poor"** · 입자마다 전하가 분포 · 표면 산화층 때문에 CPD 가 문헌값과 크게 다를 수 있음 · 고분자 입자는 표면 전하가 국소화 (Fig 26–27) | [인쇄] p.5782 · 5790 · 5793 · 5795 |
| 공기 민감 황화물 | 원문 밖.  리뷰의 측정 · 제어 실험은 **대기 (RH 제어 또는 미기재)** 다.  Faraday 통 · blow-off · Kelvin–Zisman 은 불활성 분위기로 옮길 수 있는 장치 크기 [추정] · *"The same tendency is observed for metal fluorides and metal sulfides"* (전기음성도 경향) — 근거 자료는 실리지 않았다 | [인쇄] p.5786 + [추정] |
| ★ 우리 믹서 · 논지 | 정전기는 **우리 덱에 없는 힘**이다 (논지 §2-7).  µm 접촉에서는 매끈한 구 JKR 점착이 영상력보다 **10³ 배 안팎 크다** [우리 산술 §7-2] — 그러나 (가) 반대 부호 대전은 AM–SE 접촉을 **원거리에서** 끌어당기고 (나) 코팅은 ΔW 와 함께 **CPD 도 지운다** (Fig 13 의 뜻) → 비코팅 NCM–SE 가 정전기로 서로 붙는다면 논지 P1 (비코팅 = SE–SE 응집이 남음) 과 **반대 방향의 교란**이다 [추정] | §7-1 · §7-2 |

⛔ **한정어 (떼지 말 것)**: ① 리뷰 — 정량 예시 대부분이 저자 그룹 자신의 자료 (mm 과립 · 31 mm 고무구 · 고분자 입자 · 비산재 · 알루미나 · 토너) 이고 **배터리 소재 · 황화물 · 전도성 산화물 측정은 없다** ② 축전기 모형의 k_c · z₀ 는 **맞춤 상수** — 원리상 예측식이 아니다 ③ 대전 재현성이 나쁘다는 것을 원문이 스스로 적는다 ④ 단위 · 표기 결함 여럿 (§10).

---

## 1. 한 줄 요약
분말 공정 (공기 수송 · 유동층 · 호퍼 · 혼합) 에서 입자는 마찰 · 충돌로 대전되어 벽 부착 · 응집 · 방전 (화재 · 폭발) 을 일으키지만, 같은 원리로 정전 분리 · 분체 도장 · 전자사진 · 자기 조립 · 유량 계측도 된다.
리뷰는 (1) 전하 이동 기전 (금속 일함수 → 절연체 유효 일함수 · 표면 상태 · 분자-이온-상태 · 양자화학 · 이온 · 물질 이동), (2) 화학 · 환경 인자 (산화물은 금속 이온의 일반화 전기음성도, 유기물은 치환기, 코팅 · 전하 조절제, 습도 · 온도), (3) 입자 대전 모형 (축전기 · 전하 완화) 과 반복 충돌 · 관 흐름의 지수 해, 대전 제어 (서로 다른 관 재료 교대), (4) 측정 · 특성화 (일함수 · CPD · Faraday 통 · 분포 · 충돌 시험 · AFM), (5) 응용, (6) 몬테카를로 · DEM 모사를 정리한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| S. Matsusaka\* · H. Maruyama (Kyoto Univ.) · T. Matsuyama (Soka Univ.) · M. Ghadiri (Univ. Leeds) | Chem. Eng. Sci. **65** 5781–5807 (2010) | 10.1016/j.ces.2010.07.005 | 금속 · 고분자 · 산화물 미분 · 설탕 · 유당 · 아스피린 · 에틸셀룰로스 과립 · 비산재 · 석영사 · 알루미나 · 토너 — 배터리 소재 없음 | 리뷰 (이론 · 측정 · 응용 · 시뮬레이션) |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| 1 Introduction | 5782 | 대전의 해 (부착 · 방전) 와 쓸모 (응용 · 계측) |
| 2 Basic concepts | 5782–5785 | 전자 이동 (식 1–6, Fig 1–9) · 이온 이동 · 물질 이동 |
| 3 Chemical concept · environment | 5786–5787 | 무기 (Fig 10, 식 7) · 유기 (Fig 11–12, σ 표) · 코팅 · 전하 조절제 (Fig 13) · 습도 · 온도 (Fig 14–15) |
| 4 Mechanism of particle charging | 5787–5795 | 축전기 (Fig 16, 식 8–12) · 전하 완화 (Fig 17–18) · 벽 충돌 (Fig 19–24, 식 13–14) · 반복 충돌 (Fig 25–29, 식 15–23) · 관 흐름 (Fig 30–34, 식 24–38) · 제어 (Fig 35–37, 식 39–41) |
| 5 Characterization | 5795–5799 | CPD (Fig 38–39, 식 42) · 비전하 (Fig 40–42) · 분포 (Fig 43–48, 식 43–48) · 일반 기법 (Fig 49–53) · 충돌 시험 · 관 흐름 시험 · AFM |
| 6 Applications | 5799–5802 | 분리 (Fig 54–56) · 분체 도장 · 전자사진 · 자기 조립 (Fig 57) · 공기 수송 계측 (Fig 58–61, 식 49–56) |
| 7 Simulation · 8 Summary | 5802–5804 | 몬테카를로 (Fig 62–63) · DEM (Fig 64–65) · 관 흐름 · DEM–CFD · 요약 5 항 |
| Appendix A–C · References | 5804–5807 | 영상 전하 k_e · 공간 전하 k_b · 비전하 확률밀도 · 참고문헌 |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 같은 논문 없음 · `git grep -i` DOI · "Triboelectric charging of powders" · "Matsusaka" 0 건 → 새 카드.  정본에서 "triboelectr…" 를 언급하는 카드는 `hersey1975_ordered_mixing_concept` 하나 (정렬 혼합의 상호작용 후보 열거).

---

## 3. 핵심 식 · 수치 (★ 쪽 · 표지 병기)

### 3-1. 식 (원문 그대로 — 크롭 `eq_*.png`) [인쇄]
- (1) V_c = V_1/2 = −(φ₁ − φ₂)/e — 금속 1 대 금속 2 접촉 전위차 (p.5782)
- (2) Δq_c = C₀·V_c — C₀ = 전하 이동이 끊기는 임계 거리에서의 정전 용량 (p.5783)
- (3) Δq_c = C₀·{−(φ_I − φ_M)/e} — 절연체 유효 일함수 φ_I (p.5783)
- (4) φ₁ + Δ₁ + eE_f z₀ = φ₂ − Δ₂ — 표면 상태 모형, 접촉 뒤 페르미 준위가 같아짐 (p.5784)
- (5) q_IM = ∫_{E_F}^{E_F+ΔE} ρ_D(E) f(E) dE − ∫_{E_F−ΔE}^{E_F} ρ_A(E){1 − f(E)} dE — 창 ΔE ≈ 0.4 eV (p.5784)
- (6) q_2,1 = ∫_{⟨E₁⟩}^{⟨E₂⟩} min[ρ_D2, ρ_A1] f₂{1 − f₁} dE − ∫_{⟨E₁⟩}^{⟨E₂⟩} min[ρ_D1, ρ_A2] f₁{1 − f₂} dE (p.5784)
- (7) χ_i = (l + 2Z)χ₀ — 금속 이온의 일반화 전기음성도 · Z 원자가 · χ₀ Pauling 전기음성도 · ⚠ "l" 은 본문에 정의가 없다 (§10) (p.5786)
- (8) Δq = k_c·C·V · (9) C = ε₀S/z₀ · (10) V = V_c − V_e − V_b + V_ex · (11) V_e = k_e·q · (12) V_b = k_b·q — k_c 대전 효율 · S 접촉 면적 · z₀ "the critical gap including the geometrical factors" (p.5788)
- (13) Δq = Δq₀(1 − q_i/q_e) — 충돌 전하 대 초기 전하의 직선 · Δq₀ = 초기 전하 0 일 때 · q_e = 평형 전하 (p.5789)
- (14) I = −(W/m_p)·Δq — 입자 흐름이 표적에 주는 전류 (p.5789)
- (15)–(18) dq_c/dn = k_cCV · 누설 dq_r/dt = −k_r q · dq_r/dn = −(k_r/f) q · dq/dn = −{k_c k_e ε₀S/z₀ + k_r/f} q + k_c ε₀ S V_c/z₀ (p.5791)
- (19) **q = q₀·exp(−n/n₀) + q∞{1 − exp(−n/n₀)}** · (20) n₀ = 1/{(k_c k_e ε₀ S)/z₀ + k_r/f} · (21) q∞ = V_c / {k_e + (k_r z₀)/(k_c ε₀ S f)} (p.5791)
- (22) dq/dn = −(Δq₀/q∞) q + Δq₀ · (23) **n₀ = q∞/Δq₀** — 전하 완화 모형도 같은 꼴 · 축전기 모형은 n₀ 이 V_c 와 무관 · q∞ ∝ V_c, 전하 완화 모형은 둘 다 V_c 와 무관 (p.5791)
- (24)–(28) 관 흐름: I/W_p = (q_m0 − q_m∞) exp(−n(x)/n₀){1 − exp(−n(Δx)/n₀)} · q_m∞ = 6V_c / [πρ_p D_p³{(k_e + k_b) + (k_r z₀)/(k_c ε₀ S f)}] (p.5792)
- (29) k_e = 2z₀/(πε₀D_p²) · (30) k_b = 3z₀ m ρ_g D_i ū / (2πε₀ ρ_p D_p³ v̄) · (31) **n₀ = πD_p² / {2k_c S (1 + α)}** · (32) **q_m∞ = 3ε₀V_c / {ρ_p D_p z₀ (1 + α)}** · (33) α = (3/4) m (ρ_g D_i ū)/(ρ_p D_p v̄) · (34) I/W_p = a q_m0 + b (희박, α ≪ 1) (p.5793)
- (37) q̄_m(L) = q̄_m0 exp(−L/L₀) + q̄_m∞{1 − exp(−L/L₀)} · (38) γ_q = 1 − exp(−L/L₀) (p.5793)
- (41) 두 재료 A · B 교대의 극한 q̄_m\* = (q̄_mA∞ r L_B0 + q̄_mB∞ L_A0)/(L_A0 + r L_B0), r = ΔL_A/ΔL_B (p.5794)
- (42) V₀ = V_P/Au + ρ_c d_l²/(2ε_p) — Kelvin–Zisman 영점 전위 · 가루층 전하가 작으면 V₀ = V_P/Au (p.5795)
- (43)–(48) 전하 분광: qE = 3πμ v_E D_p/C_c · q_d = q/D_p · E-SPART D_p = √{18μ tanθ/(C_c ρ_p ω)} · q/m_p = (g/E)(x_d/y_d) (p.5796–5797)
- (A.1)–(A.3) k_e = (1/4πε₀)(1/r₁ − 1/r₂), r₁ = D_p/2, r₂ = D_p/2 + 2z₀ → (29) · (B.1)–(B.3) E(r) = n_p r q/(2ε₀) → (30) · (C.1)–(C.3) 비전하 확률밀도 (충돌 수 정규분포 · 초기 전하 · 대전 인자 분포의 합성곱) (p.5804–5805)
- [우리 산술] (29) 와 (32) 를 합치면 포화 입자의 **표면 전하 밀도 σ∞ = q∞/(πD_p²) = ε₀V_c / {2z₀(1 + α)}** — 크기와 무관, q_m∞ ∝ 1/(ρ_p D_p).

### 3-2. 재료 화학 — 무기 · 유기 · 코팅 [인쇄 · 판독]
| 항목 | 값 | 표지 |
|---|---|---|
| 산화물 미분 (0.3–0.5 µm) 대 표면 산화 철 (44–74 µm), blow-off (Fig 10) | MgO ≈ +273 · ZnO ≈ +169 · PbO ≈ +145 · HgO ≈ +94 · Al₂O₃ ≈ +85 · In₂O₃ ≈ +79 · 희토 세스퀴옥사이드 무리 +73…+99 · CeO₂ ≈ +49 · CuO · Ga₂O₃ · Sc₂O₃ · Cr₂O₃ 무리 −20…+37 · ZrO₂ · As₂O₃ · Fe₂O₃ 무리 −11…−20 · TiO₂ ≈ −122 · GeO₂ ≈ −191 · SiO₂ ≈ −203 · Nb₂O₃ ≈ −206 · V₂O₅ ≈ −289 mC/kg — 일반화 전기음성도 χ_i 에 대해 직선으로 음 (−) 쪽 이동 | [판독 벡터 · 지시선으로 이름 대응] · 축 단위 "mC · kg⁻¹" [인쇄] |
| 금속 불화물 · 금속 황화물 | *"The same tendency is observed for metal fluorides and metal sulfides."* — 자료 · 그림 없음 | [인쇄] p.5786 |
| 유기물 (Fig 11) | salicylaldehyde anil 막 (250 µm 강철 구슬 · RH 0 %, 막 양 (+) 대전) · 치환 폴리스티렌 (아연 분말 · RH 56 %, 막 음 (−) 대전) — log\|비전하\| (0.1–10 µC/kg) 이 Hammett 치환기 상수와 직선 | [인쇄 · 판독] |
| Hammett σ 표 (para / meta) | NH₂ −0.66 / −0.16 · OH −0.37 / 0.12 · CH₃ −0.17 / −0.07 · H 0 / 0 · Cl 0.23 / 0.37 · COCH₃ 0.50 / 0.38 · CN 0.66 / 0.56 · NO₂ 0.78 / 0.71 | [인쇄] p.5786 각주 표 (부호는 렌더 글자로 확인) |
| 유기물 방향 (Fig 12) | HOMO 가 금속 페르미 준위보다 높으면 유기물 (+) · LUMO 가 낮으면 (−) (Gibson) | [인쇄] p.5786 |
| ★ 코팅 (Fig 13) | 티타니아 (0.15–0.3 µm) + 알루미나 함량 0 → 0.04: 비전하 ≈ −20 → +110 mC/kg · + 실리카 함량 ≈ 0.008 → 0.073 (아래 축을 0–0.1 로 읽음 — §10): ≈ −80 → −290 mC/kg (상대 = 철) | [판독 ±10] |
| 전하 조절제 | 표면 (흄드 실리카 · 불소 고분자) · 벌크 (+: 아민 · 4 급 암모늄염 / −: 금속 착물 염료) · 반대 이온 이동 · 수막에서 H⁺ 이동 가능 · 전하 안정제 (폴리에스터 염) | [인쇄] p.5787 |

### 3-3. ★ 습도 · 온도 (Fig 14–15, Greason 2000 — 12.7 mm 금속구가 절연체와 접촉) [판독 벡터]
| RH (−) | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10 °C (nC) | 21.0 | 20.0 | 19.1 | 18.4 | 15.8 | 14.8 | 11.9 |
| 20 °C | 16.6 | 16.2 | 16.8 | 14.8 | 14.3 | 14.1 | 13.7 |
| 30 °C | 13.7 | 14.1 | 13.1 | 13.0 | 12.5 | 12.0 | 11.5 |

| 온도 (°C) | 10 | 15 | 20 | 25 | 30 |
|---|---:|---:|---:|---:|---:|
| RH 0.1 (nC) | 21.1 | 18.1 | 16.6 | 15.0 | 13.7 |
| RH 0.3 | 19.2 | 17.9 | 16.9 | 14.2 | 13.1 |
| RH 0.5 | 15.8 | 15.6 | 14.2 | 14.2 | 12.5 |
| RH 0.7 | 11.8 | 13.0 | 13.5 | 11.1 | 11.5 |

- ⇒ RH 0.1 → 0.7 에서 10 °C −43 % · 30 °C −16 % · RH 0.1 에서 10 → 30 °C −35 % [우리 산술].  원문: 습도 ↑ = 표면 저항 ↓ · 누설 ↑, 높은 습도에 두면 전하가 더 빨리 준다 (Nomura 2003), 온도 효과는 낮은 습도에서 두드러진다 [인쇄 p.5787].
- ⚠ **가장 낮은 측정 습도 = RH 0.1** — 드라이룸 · 글로브박스 (RH 수 % 이하) 는 이 자료의 범위 밖이다 [추정: 경향대로면 더 대전].

### 3-4. ★ 단일 입자 충돌 · 반복 충돌 [인쇄 · 판독 · 우리 산술]
| 실험 | 값 | 표지 |
|---|---|---|
| 충돌 시험 장치 (Fig 19, Watanabe 2006–2007) | 공기로 가속 → 관통형 Faraday 통 (FC1) 으로 충돌 전 전하 → 금속 표적 충돌 → FC2 로 충돌 뒤 전하 · **≈ 100 µm 단일 입자까지** | [인쇄] p.5789 · 5798 |
| 설탕 과립 500–600 µm (Fig 20) | q_e = **−16 pC** · Δq₀ = −0.5 / −0.9 / −1.6 pC (7 / 9 / 13 m/s) | [인쇄 — 그림 안 숫자] |
| ⇒ 평형까지 충돌 수 (식 23) | n₀ = 16/0.5 · 16/0.9 · 16/1.6 = **32 · 18 · 10 회** · Δq₀ ∝ v^1.9 (세 점) | [우리 산술] |
| 평형 전하 vs 충돌 속도 (Fig 21) | 에틸셀룰로스 +10 · 설탕 −16 · α-유당 −18 · 아스피린 −40 pC — 속도 (≈ 5–28 m/s) 무관 · 재료 의존 | [인쇄] · [판독 벡터] (점 산포 ±2–8 pC) |
| 충돌각 (Fig 23) | 법선 속도 고정에서 전류가 각도 ≈ 60° 까지 증가 후 감소 — 구름 (접촉 면적 ↑) → 미끄럼 (↓) | [인쇄] p.5789 · [판독] |
| 고분자 200 µm (Fig 26) | 충돌 전하 vs 초기 전하 ±10 pC 범위 — **표면 전하 국소화** 때문에 큰 산포 (Fig 27: 접촉 면 쪽 전하만 영향) | [인쇄] p.5790 |
| 31 mm 합성 고무구 (Fig 28–29) | 19 회 충돌 뒤 **17.0 · 14.7 · 11.0 nC** (충돌 간격 10 · 20 · 30 s) — 간격이 길수록 누설로 극한값 ↓ | [판독 벡터] · [인쇄] p.5790 |
| 몬테카를로 (Fig 62–63, ε = 6, D_p 3.2 mm) | 첫 충돌 ≈ 100 pC → ≈ 20 회 뒤 ≈ 0 · 누적 ≈ 840 pC 에서 포화 | [판독 — 눈] |

### 3-5. 관 흐름 · 대전 제어 [인쇄 · 판독]
| 항목 | 값 | 표지 |
|---|---|---|
| 비산재 · 스테인리스 검출관 (Fig 31) | I = 2.3 nA at W_p = 7.0×10⁻⁷ kg/s → I/W_p = 3.3 mC/kg = q_mIN 3.9 − q_mOUT 0.6 mC/kg (전하 수지 맞음) · 평균 공기 속도 30 m/s | [인쇄] p.5791–5792 |
| 석영사 320 µm (Fig 32) | 희박상에서 전류 ∝ 유량 (기울기 1) · q_m0 −3.7 … −1.0 mC/kg | [인쇄 · 판독] |
| 조밀상 · 미세 입자 | 주변 입자가 벽 접촉을 막아 효율 ↓ · **작은 입자는 응집 때문에 효율 ↓** | [인쇄] p.5792 |
| 초기 전하 (Fig 33) | I/W_p 가 q_m0 에 직선 (식 34) · 비산재 · 관 내경 6 mm · 0.8 m | [인쇄] |
| ★ 관 재료 (Fig 34, 미크론 알루미나, 40 m/s) | 3 m 뒤 **SUS316 +7.0 · SUS304 +6.5 · 알루미늄 −4.4 · 구리 −7.7 · 황동 −8.5 mC/kg** — 지수 포화 (식 37) | [판독 벡터] |
| 3 m 관의 대전 효율 | **93–99 %** → L₀ ≈ 0.65–1.13 m | [인쇄] p.5794 · [우리 산술] |
| 두 재료 교대 (Fig 35–37) | 황동 (−) · 스테인리스 (+) 1 m 씩 교대 → 비전하가 범위 안에 머묾 · 0.5 m 면 더 좁음 · 극한 (식 41) 으로 **양 · 음 · 중성** 조절 · 병렬 배치면 요동 없이 극한값 | [인쇄] p.5793–5794 |

### 3-6. 표면 전하 밀도로 바꾸면 [우리 산술 — 원문 값 + 구 면적 πD²]
| 원문 예 | 전하 | 크기 | σ = q/(πD²) |
|---|---|---|---|
| 설탕 과립 평형 (Fig 20–21) | 16 pC | 500–600 µm | 1.4–2.0×10⁻⁵ C/m² |
| 몬테카를로 누적 (Fig 63) | ≈ 840 pC | 3.2 mm | ≈ 2.6×10⁻⁵ |
| 합성 고무구 19 회 (Fig 29) | 17 nC | 31 mm | ≈ 5.6×10⁻⁶ |
| 금속구 (Fig 14, RH 0.1 · 10 °C) | 21 nC | 12.7 mm | ≈ 4.1×10⁻⁵ |
- ⇒ 리뷰의 정량 예는 **10⁻⁵ C/m² 자릿수**에 모인다.  ⚠ Fig 3 (Nylon 66, Davies 1969) 은 축이 "mC·m⁻²" 로 인쇄돼 최대 ≈ 0.75 mC/m² — 위 값들의 ≈ 40 배라 원전 단위 확인이 필요하다 [인쇄 · 우리 산술 · 미확인].

### 3-7. 측정 · 특성화 (§5) [인쇄]
| 방법 | 재는 것 | 비고 |
|---|---|---|
| 광전자 방출 · Kelvin–Zisman (Fig 38–39) | 일함수 · **가루층 대 금 기준의 CPD** (진동 상부 금 전극 · 직류 바이어스 · 전류 0 이 되는 V₀) | 표면 산화층 때문에 CPD 가 문헌값과 크게 다를 수 있다 · 장치에 항온항습기 · 전자기 차폐 |
| Faraday 통 (Fig 40) · 여과 Faraday 통 (Fig 41) · 관통형 | 총 전하 → 비전하 q/m | 단순 · 신뢰성 · 관통형 = 실시간 |
| blow-off (Fig 42) | 토너 (미분) 를 캐리어 (큰 구슬) 에서 질소로 불어 메시로 빼내고 **캐리어에 남은 반대 전하**를 잼 | ★ 미분 (SE) + 운반체 (NCM) 와 같은 꼴 [추정] |
| 층류 + 전기장 (Fig 43) · E-SPART (Fig 44) · PMAS (Fig 45) · q-test (Fig 46, 1–200 µm) · 낙하 셀 (Fig 47–48) | 입자별 q/D 또는 q/m · 크기 분포와 2 차원 분포 | 양 · 음 입자가 서로 붙고 고대전 입자는 측정 전에 벽에 붙으므로 **분산 · 시료 채취가 관건** |
| cascade (Fig 49) · 진동판 (Fig 50) · 유동층 (Fig 51) · 수직 Faraday 통 배열 (Fig 52) · 원심 (Fig 53) | 대전 경향 · 최대 전하 | 유동층: *"When different kinds of particles are mixed … charge transfer occurs during collision with different types of particle, with the same type of particle, and with the inner wall"* |
| 충돌 시험 (§5.5) · 관 흐름 시험 (§5.6) | Δq₀ · q_e · I/W_p — 평형 비전하 | 미크론 입자는 관 흐름 시험 |
| AFM 콜로이드 탐침 (§5.7) | 거리별 힘 → **국소 접촉 대전에 의한 정전기 + 반데르발스**를 분리 · 감도 ≈ 10 전자 | 단점: 탐침 제작이 어려워 통계에 부적합 · 반복 접촉보다 **문지르기 (scanning)** 가 더 대전 |

### 3-8. 응용 · 시뮬레이션 (§6–7) [인쇄]
- 응용: 정전 분리 (사이클론 대전 → 직류 전기장 · 루버 판 · 진동 컨베이어) · **분체 도장** (마찰 건 · 코로나 건 — 공간 전하장으로 숨은 면까지 · 영상력으로 부착) · 전자사진 (토너–캐리어 마찰 대전) · **정전 자기 조립** (나일론-6,6 · 테플론 구를 금속판에서 흔들면 반대 부호로 대전 → 개수 비 1 이면 정사각 격자, 한쪽이 많으면 5 · 6 배위) · 공기 수송 유량 · 전하 · 속도 (두 검출관, 식 49–56).
- 시뮬레이션: 몬테카를로 — 패치 전하를 무작위 → 축대칭 재분배 + 전하 완화 모형 (Fig 62–63) · **DEM (Yoshida 2003)** — 입자 표면을 대전 자리 32 · 200 · 392 개로 나누고 입자–입자 · 입자–벽 충돌마다 CPD · 국소 전기장으로 전하 이동 · 전하는 접촉 자리에 남음 → 진동 용기에서 비전하가 평형으로 (30 s 뒤 ≈ 5 µC/kg) · 자리 수 영향 작음 (Fig 64–65) · DEM (Matsuyama 2009 — 진탕기, 공간 전하 · 용기 경계 · 원거리 힘) · 관 흐름 k–ε + 라그랑주 추적 (Tanoue 2001b) · 통계 모형 + 전하 완화 (Cangialosi 2006) · DEM 접촉 면적 (Watano 2006) · DEM–CFD 정전 확산 (Lim 2006) · 대규모 DEM 1.5×10⁵ 입자 토너 현상 (Mio 2006).

---

## 4. ★ 방법 — 입자 처리 (DEM 판 "무질서 처리") · 용어집

### 4-1. 입자 처리
- **모형의 입자** = 균일 대전 구 (영상 전하 k_e · 공간 전하 k_b 를 구 중심 전하로 — 부록 A · B) · 접촉 면적 S · 임계 간극 z₀ 는 상수 (맞춤).
- **실험의 입자** = mm 과립 · 31 mm 고무구 · 100–300 µm 고분자 · 미크론 산화물 · 비산재.  고분자 (절연체) 는 **전하가 접촉 자리에 국소화** — 다음 충돌의 초기 전하가 어느 면이 닿느냐에 달린다 (Fig 26–27) → 몬테카를로 · DEM 은 표면을 **자리 (site)** 로 나눠 다룬다 (Fig 62 · 64).
- 금속 (전도체) 은 전하가 퍼져 접점에서 사라지지만 **고립되면 순전하가 남는다** (Harper 1951, Fig 2) [인쇄 p.5782].  ⇒ NCM (전자 전도체) · LPSCl (이온 전도 · 전자 절연) 이 어느 틀에 드는지는 원문 밖이다 [추정 — §7-4].

### 4-2. 기법 미니 용어집
- **마찰 대전 (triboelectric charging) · 접촉 대전 · 충돌 대전**: 원문은 미끄럼 · 구름 · 충돌을 가르기 어렵다고 보고 넓은 뜻으로 "triboelectric" 을 쓴다 (p.5782).
- **CPD (contact potential difference)**: 두 물질의 (유효) 일함수 차 ÷ e — 전자 이동의 구동력.
- **유효 일함수 · 표면 상태 · 분자-이온-상태**: 절연체에 자유 전자가 없다는 비판에 대응한 모형들 — 표면 준위 · 주개 · 받개 상태 밀도.
- **축전기 모형**: 접촉부를 축전기로 보고 Δq = k_c C V.
- **전하 완화 모형 (Matsuyama · Yamamoto 1995)**: 떨어질 때 간극 전위가 **Paschen 곡선**(기체 절연 파괴 한계) 을 넘으면 방전으로 초과 전하가 빠진다 → 남는 전하 = 관측 이동 전하 · 남는 양은 유전율 · 입경 · 기체 파괴 전압에 의존.
- **비전하 (specific charge)**: q/m (C/kg).
- **blow-off**: 미분을 큰 운반 입자에서 기체로 불어 분리해 전하를 재는 전자사진 업계 방법.
- **E-SPART**: 음향장 위상 지연으로 공기역학 지름 · 전기장 이동으로 전하를 입자마다 동시에.
- **전하 조절제 (CCA)**: 토너 대전 부호 · 크기를 정하는 첨가제.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 금속–금속 접촉 전 · 후 전자 퍼텐셜 (φ₁ · φ₂ · eV_c) | CPD 정의 |
| 2 | 크롬 구 (4 mm) 대 금속 구 (13 mm) 전하 vs CPD — 이론선 위 · 실험 0–0.65 pC | 금속 접촉 대전 원형 |
| 3 | Nylon 66 전하 밀도 vs 금 대비 CPD (−1.1 … 0 V) 직선 | 유효 일함수 근거 · 단위 "mC·m⁻²" 의문 (§3-6) |
| 4 | 절연체–절연체 표면 상태 에너지 준위 (Δ₁ · Δ₂ · eE_f z₀) | 식 (4) |
| 5 | 분자-이온-상태 (금속–절연체, 창 ΔE) | 식 (5) |
| 6 | 분자-이온-상태 (절연체–절연체) | 식 (6) |
| 7 | PTFE–알루미늄 계면 양자화학 모형 | 계산으로 대전 경향 — 우리 DFT 축의 먼 선례 |
| 8 | PTFE 표면 상태 밀도 (HOMO 기준) | 〃 |
| 9 | 전자 분포 · 대전 후 변화 (C 원자 쪽 증가) | 불소보다 결함 C 가 전자를 받는다 |
| 10 | ★ 산화물 미분 비전하 vs 일반화 전기음성도 (MgO +270 … V₂O₅ −290 mC/kg) | ★ 무기물 대전 부호 예측의 틀 (§3-2) — NCM 구성 산화물은 그림에 없음 |
| 11 | 유기물 비전하 vs Hammett 상수 (anil · 폴리스티렌) | 표면 화학 → 대전 |
| 12 | 금속–유기물 전자 이동 방향 (HOMO/LUMO 대 페르미 준위) | 〃 |
| 13 | ★ 알루미나 · 실리카 코팅 티타니아 비전하 vs 코팅 함량 | ★ **코팅이 대전 부호를 바꾼다** (§7-1) |
| 14 | ★ 금속구 전하 vs 상대습도 (10 · 20 · 30 °C) | ★ 건조 환경 = 대전 ↑ (§3-3) |
| 15 | 금속구 전하 vs 온도 (RH 0.1–0.7) | 〃 |
| 16 | 축전기 모형 (임계 간극 z₀ · 접촉 면적 S · CPD) | ★ DEM 충돌당 전하 이동식 (§7-3) |
| 17 | 접촉 · 전하 이동 · 분리 · 전하 완화 4 단계 | 전하 완화 모형 |
| 18 | Paschen 곡선 · 접근 입자 퍼텐셜 · 완화 시작 · 끝 | 최대 전하의 근거 |
| 19 | 단일 입자 충돌 시험 장치 (FC1 · FC2 · 표적) | ★ SE · NCM 입자 대전 측정 장치 형식 |
| 20 | 충돌 전하 vs 초기 전하 직선 (설탕 과립, 7 · 9 · 13 m/s) | ★ n₀ = q∞/Δq₀ 산술 (§3-4) |
| 21 | 평형 전하 vs 충돌 속도 (EC +10 · SG −16 · αLM −18 · ASP −40 pC) | ★ 혼합 세기는 평형이 아니라 접근 속도를 바꾼다 |
| 22 | 경사 표적 · 회전 표적 충돌 시험 | 충돌각 효과 |
| 23 | 정규화 전류 vs 충돌각 (≈ 60° 최대) | 미끄럼 성분 |
| 24 | 유효 접촉 면적 — 구름 · 구름 + 미끄럼 | 〃 |
| 25 | 연속 충돌 대전 시험 (표적 두 개) | 반복 충돌 |
| 26 | 고분자 입자 충돌 전하 vs 초기 전하 (D_p 200 µm · 100 Torr · 30 m/s) | 표면 전하 국소화 · 캡션 300 µm 와 불일치 (§10) |
| 27 | 초기 전하 국소화 개념 | 국소 전하 = DEM 대전 자리 |
| 28 | 탄성구 반복 충돌 시험 (끈 · 관통형 Faraday 통 · 고속 카메라) | 〃 |
| 29 | ★ 합성 고무구 전하 vs 충돌 수 (간격 10 · 20 · 30 s) — 지수 포화 · 이론선 | ★ 식 (19) 의 실물 · 누설 (§3-4) |
| 30 | 관 흐름 대전 분석 계통 (예비 대전관 · 검출관 · Faraday 통) | 공정 계측 형식 |
| 31 | 검출관 전류 2.3 nA · 입구 · 출구 비전하 3.9 · 0.6 mC/kg | 전하 수지 검증 |
| 32 | 발생 전류 vs 유량 (석영사 320 µm) — 기울기 1 | 희박상 선형 |
| 33 | I/W_p vs 초기 비전하 (비산재) | 식 (34) |
| 34 | ★ 미크론 알루미나 비전하 vs 관 길이 (SUS316 · SUS304 · Al · Cu · 황동) | ★ 벽 재료가 평형 부호 · 크기를 정한다 (§3-5) |
| 35 | 초기 전하 효과 (스테인리스 · 황동) | 식 (37) 검증 |
| 36 | 두 관 재료 교대 (1 m · 0.5 m) | 대전 제어 |
| 37 | 두 재료 일반 계산 | 식 (39)–(41) |
| 38 | Kelvin–Zisman CPD 측정 장치 (항온항습 · 차폐 · 진동 전극 · 가루) | ★ NCM · LPSCl 의 CPD 측정 형식 (§7-4) |
| 39 | Kelvin–Zisman 등가 회로 | 〃 |
| 40 | Faraday 통 | 비전하 측정 |
| 41 | 에어로졸용 Faraday 통 (필터) | 〃 |
| 42 | blow-off 법 | ★ SE 미분 + NCM 운반체 대전 측정 형식 [추정] |
| 43 | 층류 + 전기장 전하 분포 측정 | 분포 |
| 44 | E-SPART | 입자별 크기 + 전하 |
| 45 | PMAS (입자 운동 분석) | 〃 |
| 46 | 이성분 토너용 q-test | 〃 |
| 47 | 분산 공급 · 시료 채취 (전기 커튼) · 측정 셀 | 〃 |
| 48 | 비전하 × 입경 2 차원 빈도 분포 (2–14 µm · −8 … +2 mC/kg) | 미크론 분말 분포의 예 (재료 [미확인]) |
| 49 | cascade 법 | 대전 경향 |
| 50 | 진동판 법 | 〃 |
| 51 | 유동층 법 | 혼합 분말 대전의 복잡성 |
| 52 | 수직 Faraday 통 배열 + 유동층 | 〃 |
| 53 | 원심법 (최대 전하) | 〃 |
| 54 | 정전 분리기 (사이클론 대전) | 응용 |
| 55 | 루버 판 정전 분리기 | 〃 |
| 56 | 진동 정전 분리기 | 〃 |
| 57 | ★ 정전 자기 조립 — 나일론-6,6 · 테플론 정사각 · 5 · 6 배위 격자 | ★ 반대 부호 대전 → 이종 이웃 선호 (§7-1) |
| 58 | 두 검출관 전류 계측 | 계측 |
| 59 | 오실로스코프 신호 · 확대 | 〃 |
| 60 | 대전 상태별 신호 모양 | 〃 |
| 61 | 상관법 입자 속도 측정 (중간관 0.5 · 1 · 2 m) | 〃 |
| 62 | 몬테카를로 — 패치 전하 · 축대칭 재분배 | 시뮬레이션 |
| 63 | 몬테카를로 충돌 전하 · 누적 전하 (ε 6 · D_p 3.2 mm) | 지수 포화 |
| 64 | ★ DEM 대전 자리 32 · 200 · 392 개 모형 입자 | ★ DEM 대전 구현 형식 (§7-3) |
| 65 | ★ DEM 진동 용기 비전하 vs 시간 (≈ 5 µC/kg, 자리 수 영향 작음) | 〃 |
| Table σ | Hammett 치환기 상수 (para · meta) | 유기물 표면 → 대전 |
| 식 크롭 | 식 (1)–(7) — CPD · 유효 일함수 · 표면 상태 · 분자-이온-상태 · 전기음성도 | 기전 |
| 식 크롭 | 식 (8)–(23) — 축전기 · 반복 충돌 지수 해 · 전하 완화 꼴 | ★ DEM 이식 식 |
| 식 크롭 | 식 (24)–(41) — 관 흐름 · 영상 · 공간 전하 · q_m∞ · 두 재료 제어 | 포화 비전하 |
| 식 크롭 | 식 (42)–(55) · 부록 A–C — CPD · 전하 분광 · 유량 · 확률밀도 | 측정 · 계측 |

## 6. Post-processing ★
- **원문**: 충돌 전하 vs 초기 전하 직선 (Δq₀ · q_e) · 충돌 수 · 관 길이에 대한 지수 맞춤 (식 19 · 37) · 전하 수지 (I/W_p = q_mIN − q_mOUT) · 확률밀도 합성곱 (부록 C) · 전기장 이동 거리 → q/m (식 48).
- **안 한 것 (리뷰)**: 재료별 V_c · z₀ · k_c 값 표 · 오차 · 반복 · 배터리 · 황화물 · 전도성 산화물 자료.
- **이 카드에서 한 것**: Fig 10 · 14 · 15 · 21 · 29 · 34 · 65 의 PDF 벡터 경로 좌표를 눈금 글자 중심으로 축 보정해 판독 (`digitized.csv`) · Fig 10 은 지시선으로 이름 대응 (모호한 무리는 범위) · n₀ = q∞/Δq₀ · 표면 전하 밀도 환산 · 습도 · 온도 변화율 · 3 m 대전 효율 → L₀ · σ∞ = ε₀V_c/{2z₀(1 + α)} 유도 · 정전기 대 JKR 크기 비교 (§7-2).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 리포 출처를 병기)

### 7-1. ★ 논지 §2-7 · P1 에 주는 것 [추정 — 원문 근거 표시]
- **부호의 원리가 있다**: 서로 다른 두 재료가 닿으면 (유효) 일함수 차를 따라 반대 부호로 대전된다 (식 1–3) · 산화물 미분은 금속 이온의 일반화 전기음성도에 따라 +270 … −290 mC/kg 로 갈린다 (Fig 10) · 리뷰는 황화물도 같은 경향이라고 적는다 (근거 자료 없음) [인쇄].  ⇒ NCM 과 LPSCl 이 서로 (또는 용기 · 날개와) 반대 부호로 대전될 가능성은 열려 있다 — **값은 [미확인]** (정본 카드 어디에도 NCM · LPSCl 의 일함수 · CPD 가 없다).
- **코팅은 ΔW 만이 아니라 CPD 도 지운다**: 알루미나 · 실리카 몇 % 코팅이 티타니아의 대전을 양 · 음으로 옮긴다 (Fig 13).  SE 로 코팅한 NCM 은 바깥 표면이 SE 이므로 NCM–SE 사이의 일함수 차도 사라진다 [추정] ⇒ 우리 **LC 팔 (코팅 대리)** 은 *"ΔW = 0"* 이면서 *"정전기 인력도 0"* 인 세계다 — 실물 코팅 효과를 모델과 비교할 때 이 둘이 섞인다.
- **비코팅에서의 교란 방향**: 반대 부호 대전이면 AM–SE 가 **원거리에서 서로 끌린다** — 정전 자기 조립 (Fig 57) 은 반대 부호 구가 **이종 이웃**을 고르는 실물이고, 전자사진의 토너–캐리어 (미분이 운반 입자에 붙어 함께 움직임) 가 같은 꼴이다 [인쇄 · 추정].  같은 부호면 SE–SE 가 **서로 밀어** SE 덩어리가 덜 생긴다.  어느 쪽이든 논지 P1 (*"비코팅이면 SE–SE 응집이 남는다"*) 을 **약하게 만드는 방향**일 수 있다 ⇒ P1 을 시험하는 실험은 **대전을 같이 재야** 표면 에너지 효과와 가를 수 있다 (hersey1975 카드 §8 항목 7 과 같은 결론).
- 0.31 문턱 자체: 정전기는 그 산술 (떼는 힘 · 기하평균) 에 없는 항이다 — 문턱을 옮기는지는 아래 크기 비교로 보면 **접촉 순간에는 거의 아니다** (µm), **충돌 · 포획 단계에서는 열려 있다**.

### 7-2. ★ 크기 비교 — 접촉 점착 (JKR) 대 영상력 [우리 산술 — 쿨롱식은 교과서 식, 원문 식 아님]
- 가정: 균일 대전 구 (반지름 a, 표면 전하 밀도 σ) 가 접지 도체 평판에 닿음 → 영상력 F_es ≈ q²/{4πε₀(2a)²} = πσ²a²/ε₀ · 접촉 점착 F_JKR = (3/2)π W a (평판 R\* = a) · W = 0.09 J/m² (IGC 분산 성분 γ^d ≈ 44 mJ/m² 의 2 배 — `deng2021_mechanical_surface_energy_tester_bond_number` · `mohammadijam2014_inverse_gas_chromatography_review` 의 값 띠) · σ = 1–4×10⁻⁵ C/m² (§3-6 의 리뷰 값 띠).

| 지름 | σ = 1×10⁻⁵ | 2×10⁻⁵ | 4×10⁻⁵ C/m² |
|---|---:|---:|---:|
| 5 µm | F_es/F_JKR = 2×10⁻⁴ | 8×10⁻⁴ | 3×10⁻³ |
| 50 µm | 2×10⁻³ | 8×10⁻³ | 3×10⁻² |
| 500 µm | 2×10⁻² | 8×10⁻² | 0.33 |

- ⇒ **µm 입자의 접촉에서는 매끈한 구 점착이 압도적**이다 (F_es ∝ σ²D² · F_JKR ∝ D → 비 ∝ D).  ⚠ 단 (가) 실제 접촉 점착은 거칠기로 매끈한 구 JKR 보다 자릿수로 작을 수 있고 (deng2021 카드: 장치값이 매끈한 구 JKR 의 약 3×10⁻²–5×10⁻⁶ 배 · johnson1971 카드의 원문 p.312 경고) (나) 국소 패치 전하 (Fig 26–27) 는 평균 σ 보다 클 수 있으며 (다) 정전기는 **원거리**에서 작용해 충돌 빈도 · 포획 · 벽 부착을 바꾼다 — 이 셋 때문에 *"정전기는 무시 가능"* 이라고 쓰지 않는다.
- ★ **조립자화 (CG) 경고**: 같은 σ · W 를 parcel 에 그대로 쓰면 F_es/F_JKR 이 지름에 비례해 **CG 배율 f 배** 부풀려진다 (johnson1971 카드 §7-1 의 f = 151.4 이면 ≈ 150 배) [우리 산술] — 정전기를 덱에 넣는다면 Bo 와 **다른 CG 규칙**이 필요하다.

### 7-3. ★ 우리 믹서 DEM 에 넣으려면 (지금은 SJKR 점착만) [추정]
- 원문의 DEM 선례: **Yoshida 2003** (대전 자리 · 충돌마다 CPD + 국소 전기장 · 전하는 자리에 남음, Fig 64–65) · **Matsuyama 2009** (진탕기 · 공간 전하 · 용기 경계 · 원거리 힘) · Watano 2006 (DEM 접촉 면적으로 대전) · Lim 2006 (DEM–CFD) [인쇄 p.5802–5803].
- 최소 구현 = 충돌마다 Δq = k_c (ε₀ S/z₀)(V_c,ij − k_e q_i − k_b q_i) (식 8–12) — S 는 우리 SJKR · Hertz 접촉 면적에서 · + 입자 사이 쿨롱 힘 · 벽 영상력.  **입력 넷이 모두 [미확인]**: V_c (NCM–LPSCl · NCM–벽 · LPSCl–벽 CPD) · k_c · z₀ · k_r (누설).
- 원문의 지수식 (19) 은 우리 혼합 덱의 바퀴 수와 직접 비교할 수 있다: 평형까지 충돌 수 n₀ ≈ 10–30 (설탕 과립, §3-4) — 혼합기 안 SE 입자의 충돌 수가 이보다 훨씬 많다면 **혼합 초반에 평형 전하**에 이른다 [추정 — 우리 덱 충돌 수 미집계].
- frame[4]: 대전 모형도 **실험 (Faraday · CPD) 에 따로 보정**하고 DEM 혼합 결과와 비교한다 — 혼합 결과에 맞춰 V_c 를 고르지 않는다.

### 7-4. 황화물 (LPSCl) · NCM 에 적용하려면 — 측정 설계 메모 [추정 — 원문 밖]
- **CPD (Kelvin–Zisman, Fig 38)**: NCM · LPSCl · 코팅 NCM 가루층을 금 기준으로 — 장치가 이미 항온항습 · 차폐 상자 안에 있으므로 불활성 분위기 (Ar) 로 옮길 수 있다.  원문 경고대로 표면층 (잔류 리튬염 · 산화 · 수분 반응) 이 값을 바꾼다 → 시료 이력 기록.
- **Faraday 통 · blow-off**: 혼합 직후 NCM (운반체) · LPSCl (미분) 의 비전하를 메시로 갈라 — 메시 눈 = 두 입경 사이 (NCM / SE 입경 비가 토너–캐리어보다 작아 분리가 어려울 수 있다).
- **습도**: 리뷰 자료의 최저 RH 0.1 아래 (드라이룸 · 글로브박스) 는 측정이 없다 — 대전이 더 크고 누설이 느릴 것으로 보이나 [추정] 실측해야 한다.
- **전도성**: NCM 은 전자 전도체 (우리 원장 CL-92 의 측정 NCM811 σ_e 4.1–5.2 mS/cm) — 금속처럼 전하가 입자 안에 퍼지되 고립되면 순전하가 남는다 (Fig 2 틀).  LPSCl 은 Li⁺ 전도 · 전자 절연 — 전자 대전 + **Li⁺ 이온 이동** 경로가 겹칠 수 있다 (원문 §2.2 이온 이동 · 정본 `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` 의 Li 화학퍼텐셜 차) [추정].
- **AFM (begat2004 카드의 CAB 측정과 같은 장비)**: 거리-힘 곡선의 원거리 꼬리로 정전기를 따로 읽고 (원문 §5.7) CAB 비에서 빼야 W 비가 된다.

### 7-5. 기존 정본 카드와의 관계
- `hersey1975_ordered_mixing_concept`: 정렬 혼합의 상호작용 후보에 정전기를 열거 — 이 카드가 그 기전 · 크기 · 측정법을 채운다.  그 카드 §8 항목 7 (*"접착인지 마찰 대전인지 가르는 실험이 없으면 코팅 효과를 표면 에너지만으로 설명하지 않는다"*) 의 측정 수단 = 이 카드 §3-7.
- `begat2004_cohesive_adhesive_balance_afm_colloid_probe`: Begat 은 정전기를 "없거나 소산" 가정 — 이 리뷰의 AFM 절 (§5.7) 은 그 분리가 가능함을 보인다.
- `deng2021_mechanical_surface_energy_tester_bond_number`: 낙하 탈착 시험을 공기 분산기 (1.5 bar) 로 증착 — 증착 대전이 탈착을 바꿀 수 있다 (그 논문은 정전기 항 F_e 를 식 1 에 적고 다루지 않음).
- `johnson1971_jkr_surface_energy_contact_elastic_solids`: §7-2 의 접촉 점착 식 · CG 배율.
- `mun2025_dry_electrode_technology_assb_review`: 건식 전극 방법 중 정전 분무 (electrostatic spray) — 이 리뷰 §6.2 분체 도장과 같은 원리.
- `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`: 산화물 양극–황화물 SE 계면의 Li⁺ 재분배 (공간 전하층) — 접촉 대전의 이온 경로 후보 [추정].
- `jarray2019_cohesion_driven_mixing_segregation_drum` · `alizadeh2018_dem_adhesion_calibration_segregation_heap`: 점착만으로 혼합 ↔ 분리를 바꾼 실험 · DEM — 정전기 없는 대조의 예.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 접촉 · 충돌 단위 **전하 이동 법칙** (축전기 · 전하 완화) 과 그 반복 해 · 대전 측정법 · DEM 대전 선례 — DEM 쪽 (접촉망 · 충돌) 의 확장.
- **없는 것**: 우리 재료 (NCM · LPSCl) 값 · 점착 (표면 에너지) 과의 결합 · 압밀 · 수송.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **정전기는 "모델에 없는 힘" 목록의 첫 줄** — 부호는 CPD 가, 크기는 접촉 면적 · 충돌 수 · 습도가 정한다.  NCM · LPSCl CPD 를 먼저 재야 비코팅 혼합의 교란 방향을 말할 수 있다.
2. **µm 접촉에서는 점착이 우세, 원거리 · CG 에서는 정전기가 커진다** — 덱에 넣는다면 Bo 와 다른 CG 규칙.
3. **코팅 = ΔW 제거 + CPD 제거** — 실물 코팅 효과와 LC 팔의 비교에서 둘을 가를 대조 (예: 같은 SE 코팅 NCM 을 대전 · 제전 상태로) 가 필요하다.
4. **혼합 세기는 평형 전하를 바꾸지 않을 수 있다** (Fig 21) — 혼합 시간 · 세기 스윕에서 대전 효과는 초반에 포화.
5. **건조할수록 더 대전** (Fig 14) — 드라이룸 · 글로브박스 공정이 정전기 쪽으로는 가장 불리한 조건이다 [추정 — RH 0.1 아래 자료 없음].

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Contact (triboelectric) charging of powders is driven mainly by electron transfer across the effective work-function difference of the contacting surfaces; for repeated impacts both the condenser model and the charge-relaxation (Paschen) model give an exponential approach of the particle charge to an equilibrium value, q = q₀e^(−n/n₀) + q∞(1 − e^(−n/n₀)) (Matsusaka et al., Chem. Eng. Sci. 2010)."
- "In the data they review, oxide fines charged against oxidized iron from about +270 mC kg⁻¹ (MgO) to about −290 mC kg⁻¹ (V₂O₅) in proportion to the generalized electronegativity of the metal ion, and thin alumina or silica coatings shifted the charge of titania positive or negative, respectively."
- 국문: *"리뷰의 정량 예를 표면 전하 밀도로 바꾸면 10⁻⁵ C/m² 자릿수이고, 이 값이면 5 µm 입자의 접촉에서는 영상력이 매끈한 구 JKR 점착의 10⁻³ 배 안팎이다 — 정전기는 접촉보다 원거리 · 조립자화에서 커진다 (우리 산술)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **배터리 소재 자료가 없다** — 산화물 미분 (Fig 10) 에 Ni · Co · Mn 산화물도 없다.  "금속 황화물도 같은 경향" 은 자료 · 그림 없이 한 문장 (p.5786).
2. **축전기 모형의 k_c · z₀ 는 맞춤 상수** — "critical gap including the geometrical factors" (p.5788) 라 독립 측정이 안 된다 · 두 모형이 같은 지수식을 내므로 충전 곡선만으로는 기전을 못 가른다 (V_c 를 바꿔 n₀ · q∞ 의 의존을 봐야 — 식 20–23 아래 원문 문장).
3. **그림 · 본문 불일치**: Fig 26 캡션 "300 µm" ↔ 그림 범례 · 본문 "200 µm" [인쇄 대조] · Fig 13 아래 축 "0 · 0.05 · 0.01" (0.1 의 오기로 보임) [인쇄] · 식 (7) 의 "l" 미정의 [인쇄] · Fig 65 범례 "charging cites" (sites) · 전자사진 6 단계 목록에서 "(iv)" 가 두 번 (p.5800) · 식 (29) 는 z₀ ≪ D_p 근사인데 "=" 로 이어 씀 (부록 A, 정확식은 4z₀/{D_p(D_p + 4z₀)}·1/(2πε₀)) [우리 산술].
4. **Fig 3 단위** "mC·m⁻²" — 리뷰 다른 예의 표면 전하 밀도보다 ≈ 40 배 (§3-6) — 원전 (Davies 1969) 확인 전 숫자 인용 금지 [미확인].
5. **재료 · 조건 미기재**: Fig 34 알루미나 입경 · Fig 37 계산 매개변수 · Fig 48 재료 [미확인] · Fig 21 의 과립 크기 (설탕 외) [미확인].
6. **대기 조건 실험** — 습도 영향이 크다고 스스로 보이면서 (Fig 14) 최저 RH 0.1 · 건조 불활성 자료 없음.
7. **재현성 나쁨을 원문이 인정** (p.5793) — 개별 값을 정밀하게 옮기지 않는다 (경향 · 자릿수만).
8. **저자 그룹 자료 위주의 리뷰** — Matsusaka · Masuda · Matsuyama · Ghadiri 의 실험 · 모형이 정량 예의 대부분이다 (선택 편향 가능) [추정].
9. **AFM 절의 "≈ 10 전자" 감도** 는 인용 (Gady 1998) — 이 리뷰의 측정이 아니다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 서지 (원문 목록 그대로) | 왜 |
|---|---|
| Oguchi, T., Tamatani, M., 1986. Contact electrification in inorganic binary compounds. Journal of the Electrochemical Society 133, 841–847. | ★ 산화물 (및 불화물 · 황화물?) 대전 vs 전기음성도 원전 — 황화물 자료가 있는지 |
| Oguchi, T., Tamatani, M., 1993. Contact electrification phenomena and powder surface treatments. Wear 168, 91–98. | ★ 코팅이 대전을 바꾸는 원전 (Fig 13) |
| Itakura, T., Masuda, H., Ohtsuka, C., Matsusaka, S., 1996. The contact potential difference of powder and the tribo-charge. Journal of Electrostatics 38, 213–226. | 가루층 CPD ↔ 대전 — NCM · LPSCl CPD 측정 설계 |
| Watanabe, H., Ghadiri, M., Matsuyama, T., Ding, Y.L., Pitt, K.G., Maruyama, H., Matsusaka, S., Masuda, H., 2007a. Triboelectrification of pharmaceutical powders by particle impact. International Journal of Pharmaceutics 334, 149–155. | 미분 충돌 대전 측정 |
| Matsusaka, S., Oki, M., Masuda, H., 2007. Control of electrostatic charge on particles by impact charging. Advanced Powder Technology 18, 229–244. | 벽 재료 · 교대 제어 (Fig 34–36) — 혼합 용기 재료 선택 |
| Matsusaka, S., Ghadiri, M, Masuda, H., 2000. Electrification of an elastic sphere by repeated impacts on a metal plate. Journal of Physics D: Applied Physics 33, 2311–2319. | 반복 충돌 지수식의 실물 |
| Matsuyama, T., Yamamoto, H., 1995a. Charge relaxation process dominates contact charging of a particle in atmospheric conditions. Journal of Physics D: Applied Physics 28, 2418–2423. | 전하 완화 모형 원전 |
| Yoshida, M., Shimosaka, A., Shirakawa, Y., Hidaka, J., Matsuyama, T., Yamamoto, H., 2003. Estimation of electrostatic charge distribution of flowing toner particles in contact with metals. Powder Technology 135/136, 23–34. | ★ DEM 대전 자리 구현 |
| Matsuyama, T., Šupuk, E., Ahmadian, H., Hassanpour, A., Ghadiri, M., 2009. Analysis of tribo-electric charging of spherical beads using distinct element method. Powders and Grains 2009. AIP, New York, pp. 127–130. | ★ DEM 대전 + 원거리 힘 |
| Greason, W.D., 2000. Investigation of a test methodology for Triboelectrification. Journal of Electrostatics 49, 245–256. | 습도 · 온도 (Fig 14–15) |
| Nomura, T., Satoh, T., Masuda, H., 2003. The environment humidity effect on the tribo-charge of powder. Powder Technology 135/136, 43–49. | 분말 습도 효과 |
| Gady, B., Reifenberger, R., Rimai, D.S., 1998. Contact electrification studies using atomic force microscope techniques. Journal of Applied Physics 84, 319–322. | AFM 대전 측정 |
| Bunker, M.J., Davies, M.C., James, M.B., Roberts, C.J., 2007. Direct observation of single particle electrostatic charging by atomic force microscopy. Pharmaceutical Research 24, 1165–1169. | 의약 분말 AFM 대전 — begat2004 와 같은 계열 |
| Grzybowski, B.A., Winkleman, A., Wiles, J.A., Brumer, Y., Whitesides, G.M., 2003. Electrostatic self-assembly of macroscopic crystals using contact electrification. Nature Materials 2, 241–245. | 반대 부호 대전 → 이종 이웃 (논지 P1 교란의 실물) |
| Tanoue, K., Ema, A., Masuda, H., 1999. Effect of material transfer and work hardening of metal surface on the current generated by impact of particles. Journal of Chemical Engineering of Japan 32, 544–548. | 취성 입자 물질 이동 — 무른 황화물이 벽에 남는 경우 |
| Rowley, G., 2001. Quantifying electrostatic interactions in pharmaceutical solid systems. International Journal of Pharmaceutics 227, 47–55. | 의약 분말 정전기 정량 |
| Lowell, J., Rose-Innes, A.C., 1980. Contact electrification. Advances in Physics 29, 947–1023. | 접촉 대전 고전 리뷰 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 27 쪽 전부 텍스트층으로 읽고, 식 · 표 · 단위는 렌더한 쪽 이미지로 대조했다.  ⚠ 텍스트층은 µ 를 "m" 으로 (예: "0.3–0.5 mm" → 렌더 "0.3–0.5 µm") · 빼기 부호를 빈칸으로 잃는다 — 캡션 · 본문의 µm (0.15–0.3 · 0.3–0.5 · 44–74 · 100–300 · 200 · 250 · 300 · 320 · 500–600 µm), 축 단위 (Fig 3 · 10 · 13 · 33–37 = mC, Fig 11 · 65 = µC), σ 표의 부호를 글자 렌더로 하나씩 확인했다.
- Fig 10 · 14 · 15 · 21 · 29 · 34 · 65 는 PDF 벡터 경로 좌표를 눈금 글자 중심으로 보정해 읽었다 (축 잔차 ≤ 0.06 단위).  Fig 10 의 산화물 이름은 지시선을 따라 대응시켰고 모호한 무리는 범위로 남겼다.
- 크롭 92 장 = 그림 67 (Fig 1–65 · A.1 · B.1 — 캡션 기준 자동 영역, 전부 눈으로 확인, Fig 43 은 y 축 글자가 단 경계에 걸려 다시 자름) + 표 1 (σ) + 식 영역 24 (줄 단위로 바깥으로 맞춤 · 식 1 · 5 · 6 은 단이 갈려 따로).
- 정본 litdb 중복 확인: 파일 목록 + DOI · 제목 · "Matsusaka" `git grep` 0 건.

## 🔗 관련 카드
- 같은 묶음 (점착 · 혼합 상호작용): `johnson1971_jkr_surface_energy_contact_elastic_solids` · `begat2004_cohesive_adhesive_balance_afm_colloid_probe` · `deng2021_mechanical_surface_energy_tester_bond_number` · `mohammadijam2014_inverse_gas_chromatography_review` · `hersey1975_ordered_mixing_concept`.
- 건식 공정 · 계면: `mun2025_dry_electrode_technology_assb_review` · `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` · `lee2026_mechanical_halogen_argyrodite_drycoating`.
- 혼합 DEM (점착만): `jarray2019_cohesion_driven_mixing_segregation_drum` · `alizadeh2018_dem_adhesion_calibration_segregation_heap` · `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `otani2025_dem_se_dispersion_aggregation_compression`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

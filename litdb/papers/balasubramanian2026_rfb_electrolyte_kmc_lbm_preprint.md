<!-- digest 표준 양식 (standard depth — 1저자 우선순위 낮음 · ⛔ 프리프린트 = 미심사). 형식 이웃 = sankar2026_fiber_scale_dem_carbon_felt_manufacturing.md (같은 Franco 그룹 · ChemRxiv).
     쪽 표기 = PDF 쪽 1–36 (ChemRxiv 판 · p.1–2 = ChemRxiv 요약 · 키워드 쪽 · 원고 p.3–29 · 감사 · 참고문헌 p.30–36).  SI (Sections S1–S9 · Tables S4 · S6) 미보유.
     값 표지: [인쇄] = 본문 · 캡션 · 그림 안 글자 · [판독] = 그림에서 읽은 값 (대략 · TREND 전용) · [우리 산술] · [우리 대조] · [추정] · [미확인].
     본문 · 참고문헌 = PyMuPDF 쪽별 텍스트 정독 · 그림 8 장 = 크롭 직접 열람 (Fig. 1 · 4 · 5 · 6 은 값 판독용으로 다시 열람). -->
# ⛔프리프린트 — 수계 유기 레독스 흐름전지 (AORFB) 탄소펠트 전극에서 **전해질 농도 (메틸비올로겐 MV · NaCl/K₂SO₄) × 섬유 미세구조** 의 결합 — Debye 길이 축척 **kMC** (정전류 방전 초기 전위 감소율 δV) → RBF 대리모델 → 기공 축척 **LBM** (이류-확산, OpenLB) 일방 결합 · 지표 2 개 (섬유 평균 δV̄ · 대류 표면적 CA = Pe > 1 경계 복셀 %) · **비표면적–투과율 trade-off** — Balasubramanian · Fernandez · **Franco** (ChemRxiv 2026)

> slug `balasubramanian2026_rfb_electrolyte_kmc_lbm_preprint` · DOI `10.26434/chemrxiv.15009732/v1` · type `kMC + LBM (multiparadigm, one-way coupled via RBF surrogate; GeoDict FiberDict stochastic carbon felt microstructures; OpenLB 1.8.1) — 레독스 흐름전지 · ChemRxiv 프리프린트 (미심사)` · PDF `11._Insights_into_Electrolyte_Effects_on_Interfacial_Kinetics_and_Transport_in_Porous_Redox_Flow_Battery_Electrodes_A_Multiparadigm_Modelling_Study.pdf` · digested `2026-10-13` · status ✅
>
> ⛔ **인용 규율**: *"This is a preprint and has not been peer reviewed. Data may be preliminary."* [인쇄 p.1–2] — 인용 문장마다 "ChemRxiv 프리프린트 (미심사)" 병기.
> **저자**: Avaneesh Balasubramanian · Francisco Fernandez · **Alejandro A. Franco\*** (UPJV LRCS UMR CNRS 7314 · RS2E · ALISTORE · IUF — alejandro.franco@u-picardie.fr) [인쇄 p.3] · ChemRxiv 게시 **2026-10-01** · **CC-BY 4.0** [인쇄 p.1] · 36 쪽 · 연구비 EU MSCA PREDICTOR (101168943) · Horizon Europe DigiCell (101135486) · 계산 = UPJV Matrics HPC [인쇄 p.30].
> **정본 litdb 이웃**: [`sankar2026_fiber_scale_dem_carbon_felt_manufacturing`](sankar2026_fiber_scale_dem_carbon_felt_manufacturing.md) (같은 그룹 · 같은 공저자 Fernandez · 탄소펠트 섬유 DEM 제조) · [`zhang2026_polymer_electrolyte_modeling_perspective`](zhang2026_polymer_electrolyte_modeling_perspective.md) (같은 그룹 · 모델 분류 틀) · [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) (같은 그룹 ARTISTIC 제조 모델 — 이 논문은 자기 작업을 *"extend our ARTISTIC framework"* 로 위치시킨다 [인쇄 p.5]).

---

## 0. 결론 먼저 — 우리에게 쓸모 (정직하게: 낮음 — 방법 유비만)
- 계 (수계 유기 RFB · 흐르는 액체 전해질 · 탄소 섬유 펠트) 와 물리 (이류-확산 · 전기이중층) 가 우리 (전고체 황화물 복합양극 · 입자 접촉망 수송) 와 다르다 — **숫자는 하나도 옮기지 않는다**.
- 방법 유비 셋 (근거 아님 · 위치 표시) [우리 해석]:
  1. **미시 모델 → 보간 대리모델 → 메조 모델 일방 결합** (kMC → RBF → LBM 경계 복셀) — 우리 DEM → 접촉망 → STEP3/STEP4 의 단계 결합과 같은 구조.  저자도 양방향 결합은 *"computationally challenging"* [인쇄 p.6] 이라 하고, 결합을 *"one-way"* [인쇄 p.28] 로 명시하며, 활성화 시간 뒤의 수송 · 반응은 *"absence of two-way coupling"* 때문에 모델 밖이라고 적는다 [인쇄 p.29].
  2. **비표면적 ↔ 투과율 trade-off** — 얇은 섬유 · 높은 밀도 = 표면적 ↑ · 투과율 ↓ · 반응 지표 δV̄ 는 개선 (경계 농도가 유입값에 가까움), 대류 표면적 CA 는 악화 [인쇄 p.26–27].  우리 쪽에도 모양이 같은 교환이 있다: *"작은 NCM 이 많을수록 활물질 표면이 넓어 (0:10 은 10:0 의 2.25 배) SE 가 그 표면을 덮는 데 쓰이고, SE–SE 길이 끊긴다"* (`docs/symmetric_cell_ionic_plan_20261013.md` §2 — 모델 안 기전 · 그 문서는 1저자 비준 대기).  다른 계 · 다른 물리라 근거로 쓰지 않는다.
  3. **"대류 표면적" CA = 경계 복셀 중 Pe > 1 비율** — 경계에서 공급이 확산 지배인지 대류 지배인지 세는 계면 지표 · 우리 coverage (AM 표면 중 SE 접촉 비율) 와 같은 계열의 "표면 중 몇 % 가 활성 공급을 받나" 지표.

## 1. 한 줄 요약
MV 음극액 (50 % SOC, 지지염 NaCl 또는 K₂SO₄) 의 전기이중층을 Debye 길이 영역 kMC 로 −5 mA cm⁻² 정전류 방전해 초기 전위 감소율 **δV** 를 농도 격자에서 얻고 RBF 로 보간한 뒤, GeoDict 로 만든 탄소펠트 5 종 (섬유 4.7 · 22.3 µm × 밀도) 위에서 OpenLB 로 이류-확산을 풀어 경계 복셀 농도마다 δV 를 대리 계산 → 섬유 평균 δV̄ (작을수록 전위 유지) 와 Pe > 1 경계 비율 CA (클수록 확산층 지배 약함) 로 전극 × 전해질 쌍을 비교: **MV 농도 ↑ 는 이중층 동역학엔 좋고 기공 수송엔 나쁘다** [인쇄 p.1] — 그래도 대부분 구조에서 δV̄ 최저는 최고 농도 조합 (1M_0.5MNaCl) [인쇄 p.26] · **지지염 효과는 비단조** [인쇄 p.20] · **표면적 큰 전극은 δV̄ 유리 · 투과율 큰 전극은 CA 유리** [인쇄 p.26–27].

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| A. Balasubramanian, F. Fernandez, **A. A. Franco\*** (UPJV LRCS) | ChemRxiv 2026-10-01 · ⛔ 미심사 · CC-BY 4.0 | 10.26434/chemrxiv.15009732/v1 | MV⁺/MV²⁺ 음극액 + NaCl / K₂SO₄ (수계) · 탄소펠트 섬유 전극 | kMC + LBM 다패러다임 (일방 결합) · 실험 없음 |

---

## 3. 핵심 수치 · 설정
### 3-1. kMC (Debye 길이 영역)
- 단단한 구 이온 · 연속 용매 · 이산 정육면체 격자 [인쇄 p.8].  z = 전극 법선 · 상자 = 전극면 ~ L_D · **z = 0 = 전극에서 L_D 떨어진 가장 바깥 이온 층 (kMC 경계층) — 여기서 모든 이온 농도를 bulk 값으로 고정** · x, y 주기 [인쇄 p.8].  Poisson = 경계층 Dirichlet · 전극면 Neumann [인쇄 p.9].
- 전위 φ = φ_e (조밀층) + φ_d (확산층) · ∂σ/∂t = −(J_inp − J_F) · MV⁺ ⇌ MV²⁺ + e⁻ · Butler–Volmer 형 속도 [인쇄 p.8–9] · 산화 · 환원은 전자 터널링 거리 안의 MV 만 [인쇄 p.10].
- 이온 도약 K_hop = (D_i/A) exp(z_i e r_i E / k_B T), D 는 Stokes–Einstein · MV⁺ 이량화 · 다량화에 따른 농도 의존 점도 반영 · 이온-이온 쿨롱 상호작용은 계산 비용 때문에 생략 (SI S2 에서 영향이 작다고 보고) [인쇄 p.10].
- 50 % SOC (MV⁺ = MV²⁺, 짝음이온 Cl⁻) · 정전류 **J_inp = −5 mA cm⁻²** · 초기 φ = 형식전위 φ⁰′ [인쇄 p.9] · **δV = 초기 φ–t 기울기** (식 9 · 그림 단위 V/ns) [인쇄 p.10].  저자: δV 는 주로 활성화 과전압 · 낮은 전류는 kMC · LBM 축척의 물질전달 손실을 줄이려고 고른 값 [인쇄 p.18].
- Fig. 4a (지지염 없음, 점 4 개): δV ≈0.0076 (0.05 M) · ≈0.0059 (0.1 M) · ≈0.0034 (0.5 M) · ≈0.0017 V/ns (1 M MV) [판독] — MV ↑ → Debye 길이 ↓ → 터널링 거리 안 MV ↑ → δV ↓ [인쇄 p.19–20].  같은 [판독] 값을 SI 단위로: 0.0017–0.0076 V/ns = 1.7–7.6 × 10⁶ V/s [우리 산술] — 저자도 δV 가 *"seemingly large"* 라고 인정 [인쇄 p.29].
- Fig. 4c/d: 지지염 효과 **비단조** — (i) Debye 길이 압축 → δV ↓ (낮은 MV 0.05 · 0.1 M 에서 큼) (ii) Na⁺/K⁺ (작은 수화 반경 → 빠른 도약) 가 터널링 거리 안 · 근처 격자 자리를 먼저 차지 → δV ↑ (MV > 0.5 M 에서 지배) [인쇄 p.20] · NaCl ≈ K₂SO₄ 정성 같음 → LBM 엔 NaCl 대리모델만 사용 [인쇄 p.21].
- 열지도의 kMC 표본점 (검은 원) = 염마다 ≈14 점 (MV 0.05–1.0 × 염 0 · 0.1 · 0.5 M) [판독] — 나머지는 RBF 보간 (SciPy) [인쇄 p.11 · p.20] · 보간 성능 지표는 SI S7 (미보유).

### 3-2. LBM (기공 축척)
- 미세구조: GeoDict FiberDict · **1000 × 200 × 200 µm · 복셀 1 µm** · 섬유 지름 **4.7 · 22.3 µm** · 압축 없음 · 두께 방향 섬유 분율 2.3 % · 배향 8.55 (Yu 등 [23] 의 베이즈 최적화값) → **5 종: 4.7_0.08 · 4.7_0.14 · 4.7_0.26 · 22.3_0.14 · 22.3_0.26** (숫자 = 섬유 지름 µm _ 펠트 밀도 g cm⁻³) [인쇄 p.12].
- SSA = GeoDict MatDict 의 Minkowski 측도 · 투과율 = Darcy κ = µūX/p (OpenLB 1.8.1 대리 유체) [인쇄 p.12].
- 수송: MV · Na⁺ 만 이류-확산 (Cl⁻ 는 국소 전하중성으로 생략 · MV⁺/MV²⁺ 같은 확산계수로 구분 안 함 · bulk 수송에서 전기장 무시) [인쇄 p.12–13].
- 격자 · 충돌: NS = D3Q19 · 이류-확산 = D3Q7 · τ_NS = 1.5 고정 · δx = 1 µm (복셀) · 고투과 구조 = NS · 이류-확산 모두 BGK · 저투과 구조 (BGK 불안정) = NS 는 TRT (magic λ = 0.25), 이류-확산은 RLB [인쇄 p.13–14] · 입구 Dirichlet · 출구 영구배 (Neumann) · 고체 bounce-back · 총 시간 t_tot = 2X/ū [인쇄 p.14–15] · 압력차 **10 · 100 Pa** (Re < 1 Darcy · Re < 100 층류; 100 Pa = 실험 펌프 유량에 맞춤, SI S3) [인쇄 p.15].
- 유입 조합 4: [MV] 1 · 0.1 M × [Na⁺] 0.5 · 0.1 M (예: "1M_0.5MNaCl") [인쇄 p.22].
- Fig. 5 (투과율 × 10⁻¹⁰ m² vs SSA m⁻¹) [판독]: 22.3_0.14 ≈6.1 @ ≈1.5 × 10⁴ · 22.3_0.26 ≈1.8 @ ≈2.6 × 10⁴ · 4.7_0.08 ≈0.7 @ ≈3.7 × 10⁴ · 4.7_0.14 ≈0.3 @ ≈6.2 × 10⁴ · 4.7_0.26 ≈0.1 @ ≈1.1 × 10⁵ — 섬유 얇고 밀도 높을수록 SSA ↑ · 투과율 ↓ [인쇄 p.21–22].
- Fig. 6a (100 Pa) [판독]: 이중층 δV (점선 = 모든 경계 복셀이 유입 농도일 때) ≈0.0020 / ≈0.0023 / ≈0.0045 / ≈0.0063 V/ns (1M_0.5M · 1M_0.1M · 0.1M_0.5M · 0.1M_0.1M) · 점선 위 높이 = 기공 수송 한계에 따른 추가 δV [인쇄 p.22–23] · 22.3_0.14 가 모든 열에서 가장 높음 (≈0.0031 – ≈0.0067).
- Fig. 6c/d (100 Pa) [판독]: CA_MV ≈92–98 % (22.3_0.14) · ≈80 % (4.7_0.08) · ≈75 % (22.3_0.26) · ≈55 % (4.7_0.14) · ≈19–20 % (4.7_0.26) — 전해질 조성 영향 작음 [인쇄 p.26] · CA_Na ≈66–81 % (22.3_0.14) … ≈0–2 % (4.7_0.26).
- 압력: δV̄ 는 100 Pa 가 10 Pa 보다 높다 (관성 → 섬유 뒤 흐름 교란 · 저농도 구역) · 22.3 두 구조에서 뚜렷 [인쇄 p.28] · 10 Pa 에서 저투과 두 구조 (4.7_0.14 · 4.7_0.26) 는 포화가 ≈100 배 느려 **생략** (Fig. 6b 에 없음) [인쇄 p.28].
- 결합 가정: LBM 경계 복셀 농도 = kMC 경계층 농도 (L_LBM = 1 µm ↔ L_D ~ nm) — 복셀 안에 확산층이 생기면 무효 → 국소 Pe (확산계수는 별도 대리모델 g1 · g2) 로 점검 = CA [인쇄 p.16–17].

## 4. 방법 · 입자 처리
- kMC: 입자 (이온) 이산 · 연속 용매.  LBM: 복셀 연속 유체 · 섬유 = 고정 고체 복셀 (기계 없음).  **DEM 없음** (섬유 미세구조는 확률 생성 · 압축 없음).
- 결합: kMC 격자 결과 → SciPy RBF 보간 f([MV], [Na]) → LBM 경계 복셀마다 δV_v → 평균 δV̄ (식 17) · 확산계수 대리모델 g1 · g2 → Pe_v → CA (식 18) [인쇄 p.16–17].
- 위치: 같은 그룹의 kMC 이중층 모델 (Yu 2022 [40]) · MV 점도/확산계수 kMC+MSD 보정 (Yu 2025 [2]) · 탄소펠트 LBM+베이즈 최적화 (Yu 2023 [23]) 를 묶고 ARTISTIC 틀 [41] 의 RFB 확장으로 둔다 [인쇄 p.5–6].
- 용어: **Debye 길이** L_D = √(ε_A ε₀ k_B T / Σ[i](z_i e)²) (식 1) · **δV** (초기 전위 감소율) · **CA** (대류 표면적 = Pe > 1 경계 복셀 %) · **SSA** (비표면적, Minkowski 측도) · **BGK / TRT / RLB** (LBM 충돌 연산자 계열).

## 5. Figure set
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 다축척 틀 개관 (전해질 농도 → Debye 길이 · 점도 · 확산계수 → kMC / 섬유 지름 · 펠트 밀도 → 투과율 · SSA → LBM → 평균 전위 손실 · 대류 표면적) | 단계 결합 그림 언어 |
| 2 | 전 방전 φ–t 와 kMC 초기 구간 · δV 정의 | — |
| 3 | kMC–LBM 결합 흐름 (경계 복셀 v · Debye 길이 kMC 상자 · 대리모델 f · g · Pe) | ★ 미시 → 대리 → 메조 일방 결합의 명시적 그림 |
| 4 | (a) δV vs [MV] (b) kMC 스냅샷 1 M · 0.05 M (c, d) δV 열지도 [MV] × [NaCl] · [K₂SO₄] (검은 원 = kMC 표본) | — |
| 5 | 투과율 vs SSA (5 구조) | ★ 표면적–투과 trade-off 의 깨끗한 그림 |
| 6 | (a, b) δV̄ (100 · 10 Pa) (c, d) CA_MV · CA_Na (100 Pa) | 계면 지표 설계 예 |
| 7 | 경계 복셀 농도 · δV_v 의 흐름 방향 분포 (전해질 / 구조 4 조합) | 국소 분포 → 평균 지표 |
| 8 | Na⁺ 농도장 100 vs 10 Pa (1M_0.5MNaCl · 22.3_0.14) | — |

## 6. Post-processing
- 저자: 경계 복셀 평균 (δV̄) · 지시함수 비율 (CA) · Darcy 투과율 · Minkowski SSA · 농도/δV_v 분포.  우리: 본문 정독 · 그림 판독 (TREND 전용).

## 7. 우리 DEM+MPM 대비 (관련도 낮음)
| 항목 | 이 프리프린트 | 우리 | 판정 |
|---|---|---|---|
| 계 | 수계 유기 RFB · 액체 흐름 · 탄소 섬유 | 전고체 황화물 복합양극 · 입자 접촉 | 물리 다름 — 수치 전이 금지 |
| 미세구조 | 확률 생성 섬유 (GeoDict) · 비압축 · 1 µm 복셀 | DEM 압밀 침대 (300 MPa) · MPM 복셀 0.15–0.4 µm | 그들은 제조 · 압축 없음 (같은 그룹 sankar2026 이 섬유 DEM 제조를 따로 다룸) |
| 결합 | 일방 (kMC → RBF → LBM) | 일방 단계 (DEM → 망 → STEP3/4) | 같은 구조 · 같은 한계 (되먹임 없음) |
| 표면 지표 | CA (Pe > 1 경계 %) | coverage (AM 표면의 SE 접촉 %) · Stage-E 면적 | 같은 계열의 "표면 중 활성 몫" 지표 |
| trade-off | SSA ↑ ↔ 투과율 ↓ | AM 표면적 ↑ (작은 NCM 많음) ↔ SE–SE 망 약화 — ps45 Hertz σ_ion 0:10 → 7:3 1.52 배 (조성마다 시드 1 개 · 확정 전) (`docs/data/ps45_r45_network_g2_20261007/README.md`) | 다른 계 · 같은 모양의 교환 [우리 해석] |
- frame[5]: 이 연구는 **수송 (유체 · 계면 동역학)** 만 · 기계 (압축 · 변형) 없음.

## 8. 적용 인사이트
1. 지표 설계 참고 — 국소 상태 (경계 복셀) 를 "평균 반응 지표 + 활성 표면 비율" 두 개로 요약하는 방식은 우리 STEP4 깊이별 반응 분포를 요약할 때 참고할 수 있다 (예: 활성 AM 표면 비율) [추정].
2. 대리모델 결합 시 **결합 가정의 유효성 지표 (여기선 Pe)** 를 같이 내는 습관 — 우리 단계 결합에도 "가정이 깨지는 곳" 표지가 필요하다 [우리 해석].
3. 대리모델 표본 밀도 점검 — 이 논문 열지도는 염마다 ≈14 점에서 보간된다 [판독] · 우리도 대리모델 (예: 망 · 복셀 결과의 보간) 을 쓸 때 표본점을 그림에 같이 찍는다 [우리 해석].

## 9. 인용 가능 문장
- "In a kMC–LBM multiparadigm study of aqueous organic redox-flow electrodes (Balasubramanian et al., ChemRxiv 2026, not peer-reviewed), higher-surface-area felts kept the fibre-averaged potential-loss rate closer to the double-layer value, whereas higher-permeability felts increased the convective surface fraction — a surface-area/permeability trade-off."

## 10. 주의/한계
1. ⛔ **미심사 프리프린트** · SI 미보유 (물성 · 수렴 [S6] · 보간 성능 [S7] · 기공 분포 [Table S6 · S8] · 영역 대표성 [S9] = [미확인]).
2. 저자 인정: δV 절대값이 큼 (kMC 축척 · 확률성) · 옴 효과 무시 · 일방 결합 · 50 % SOC 고정 · 활성화 시간 뒤 수송/반응 미모델 [인쇄 p.29].
3. 복셀 1 µm 에 섬유 4.7 µm = 지름 ≈4.7 복셀 [우리 산술] — 얇은 섬유 쪽 경계 표현이 거칠다 (수렴 검토는 SI S6 · S9, 미보유).
4. 밀도 표기: 본문은 *"two carbon felt densities of 0.14 g/cm3 and 0.26 g/cm3"* 이고 같은 문단에 *"(corresponding to uncompressed density from 0.08 g/cm3 to 0.15 g/cm3)"* 가 붙는데 구조 목록에는 4.7_**0.08** 이 있다 [인쇄 p.12] — 0.08 구조를 고른 근거 문장이 본문에 없다.
5. 식 번호 · 약어 오기: 도약 속도를 *"equation (7)"* 로 두 번 지칭 (실제 식 (8)) [인쇄 p.20] · *"RFB interpolation functions"* (RBF 오기) [인쇄 p.17].
6. **참고문헌 번호 어긋남 [우리 대조]** — 본문 p.12 이후 일부 번호가 목록과 대개 +3–4 어긋난다.  예: *"GeoDict® software 49"* → 목록 (49) = Zn–Ce RFB 분극 논문 (GeoDict = 52) · *"OpenLB-1.8.1 52"* → (52) = GeoDict Releases (OpenLB = 56) · *"BGK collision operators 54"* → (54) = GeoDict User Guide (Qian lattice BGK = 58) · *"RLB model 56,57"* → (56) OpenLB · (57) Darcy 유도 (RLB = 60 · 61) · *"Peclet numbers 60"* → (60) = RLB 논문 (Péclet = 64) [인쇄 p.12–17 ↔ p.34–35].  ⇒ 이 프리프린트를 거쳐 2 차 인용할 때는 번호가 아니라 목록 서지로 확인한다.
7. 그림 ↔ 본문 서술의 예외 [판독]:
   (a) CA 가 *"clearly increase with … higher permeability"* [인쇄 p.27] 인데 CA_MV 는 4.7_0.08 (≈80 %) 이 22.3_0.26 (≈75 %) 보다 높다 (투과율은 ≈0.7 vs ≈1.8) — CA_Na 는 투과율 순서와 맞다.
   (b) *"Within any column … the δV̄ points go lower"* [인쇄 p.26] 인데 Fig. 6a 첫 열 (1M_0.5M) 에서 최고 SSA 의 4.7_0.26 (≈0.0024) 이 4.7_0.14 · 4.7_0.08 (≈0.0021) 보다 높다.
   (c) *"δV̄ values are higher at 100 Pa … than at 10 Pa"* [인쇄 p.28] 는 22.3 두 구조에 맞고, 4.7_0.08 은 1M 두 열에서 반대 (10 Pa ≈0.0028 · ≈0.0031 > 100 Pa ≈0.0021 · ≈0.0024).
8. 대리모델 표본 성김 — 염마다 kMC ≈14 점 [판독] · 열지도 내부 모양 (예: K₂SO₄ ≈0.15 M · MV ≈0.2 M 의 노란 봉우리) 은 표본점 사이 RBF 보간이다 [판독].
9. 실험 검증 없음 (경향을 문헌 실험 · 시뮬레이션과 정성 비교만 [인쇄 p.20–21 · p.26–27]).

## 11. 참고문헌 — 우리가 더 볼 것 (서지 = 이 프리프린트 목록 [인쇄 p.30–33])
| 번호 | 서지 | 왜 |
|---|---|---|
| 23 | Yu, J.; Duquesnoy, M.; Liu, C.; Franco, A. A. *Optimization of the Microstructure of Carbon Felt Electrodes by Applying the Lattice Boltzmann Method and Bayesian Optimizer*. J. Power Sources 2023, 575, 233182. doi:10.1016/j.jpowsour.2023.233182 | 섬유 분율 2.3 % · 배향 8.55 · 지름/밀도 범위의 출처 |
| 39 | Ma, Q. et al. *A Machine Learning-Assisted Multi-Scale Method for Understanding Reactive Transport Behaviors within Electrode of Redox Flow Battery*. J. Power Sources 2025, 658, 238356. doi:10.1016/j.jpowsour.2025.238356 | kMC–LBM 결합 선행 (VRFB · 정전위 kMC) |
| 40 | Yu, J. et al. (… Franco, A. A.) *Gaining Insight into the Electrochemical Interface Dynamics in an Organic Redox Flow Battery with a Kinetic Monte Carlo Approach*. Small 2022, 18 (43), 2107720. doi:10.1002/smll.202107720 | 이 kMC 이중층 모델의 원전 |
| 2 | Yu, J.; Baudrin, E.; Franco, A. A. *Diffusion Coefficient and Viscosity of Methyl Viologen Electrolyte Estimation Based on a Kinetic Monte Carlo Computational Approach Coupled with the Mean Square Displacement Method*. Batter. Supercaps 2025, 8 (3), e202400430. doi:10.1002/batt.202400430 | 농도 의존 점도 · 확산계수 보정 |
| 41 | Troncoso, J. F. et al. (… Franco, A. A.) *The ARTISTIC Battery Manufacturing Digitalization Initiative: From Fundamental Research to Industrialization*. Batter. Supercaps 2025, 8 (1), e202400385. doi:10.1002/batt.202400385 | 같은 그룹 제조 디지털화 틀 (alabdali2023 카드와 같은 계보) |

## 원문 대조 기록 (2026-10-13)
- 36 쪽 전부 PyMuPDF 쪽별 텍스트로 정독 (본문 · 결론 · 감사 · 참고문헌 73 편) · 쪽 표기 재대조 · 그림 8 장 크롭 (래스터 bbox · 벡터 그림 5 · 6 은 요소 합집합) 후 가장자리 흰 띠만 다듬음 (다듬은 띠 = 회색값 ≥ 251 확인) · Fig. 8 캡션은 p.28 머리.
- 정본 litdb 전수 검색 (papers/ 목록 + DOI · 제목 · "redox flow" · "Methyl Viologen" grep): 같은 논문 카드 없음 · 관련 = sankar2026 (같은 그룹 탄소펠트 DEM).

## 🔗 관련 카드
`sankar2026_fiber_scale_dem_carbon_felt_manufacturing` · `zhang2026_polymer_electrolyte_modeling_perspective` · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (같은 그룹 제조 모델).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

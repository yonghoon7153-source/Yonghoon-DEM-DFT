# batch 128 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-79)

대상: `sakuda2016_se_particle_size_electrode_morphology_ncm111_li2s_p2s5_cracking` — A. Sakuda · T. Takeuchi · H. Kobayashi, "Electrode morphology in all-solid-state lithium secondary batteries consisting of LiNi1/3Co1/3Mn1/3O2 and Li2S-P2S5 solid electrolytes", *Solid State Ionics* 285 (2016) 112–117 · DOI 10.1016/j.ssi.2015.09.010 (AIST).
LiNbO₃ 코팅 NCM111 (d50 9.4 / 5.3 µm) × 75Li₂S·25P₂S₅ 유리 SE (d50 16 / 3.8 µm) 의 2 × 2 를 75 : 25 wt · 무탄소 · vortex 1 분 건식 혼합 · 330 MPa 상온 성형으로 만든 Li–In 반쪽셀의 단면 SEM/EDX (정성) · 충방전 · 율속 — DEM · 모델 없음.
쪽 = 인쇄 쪽 p.112–117 (PDF 쪽 n = 111 + n) · 판독 원자료 = `litdb/figures/sakuda2016_se_particle_size_electrode_morphology_ncm111_li2s_p2s5_cracking/digitized.csv` (72 행) · 고른 의도 = '믹싱 · 측정 — 작은 SE 로 단순 혼합 · 반쪽셀 제작 절차의 출처' → 카드 §0-1 = **채움**.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 순수 SE 압력별 기공 · 밀도 · 진밀도 없음.  닿는 것 둘:
- [a] sakuda2016_… | 두 SE (as-prepared d50 16 µm · 분쇄 3.8 µm) 의 압분 펠릿 σ 가 **≈4 × 10⁻⁴ S cm⁻¹ @ 25 °C** 로 같다 · *"The grain boundary resistance is not a dominant resistance component in the compressed pellets of Li₂S–P₂S₅ glasses"* | 카드 §3-1 · p.113 | [인쇄] | 펠릿 성형압 · 두께 · 밀도 [미확인] · 유리 (LPSCl 아님)
- [a] sakuda2016_… | SE 층 (분리막 80 mg · 330 MPa) 의 공극이 SE-16 에서 보이고 SE-4 에서 안 보인다 (*"a homogeneous SE layer is also achieved using smaller-sized SE particles"*) | 카드 §3-4 · p.115 · Fig. 2a · b | [인쇄] 정성 + [판독] | 기공률 0 · 같은 SE 로 만든 분리막인지 [미확인]

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 탈압 · 되돌아옴 · 두께 변화 측정 없음.  상태만:
- [b] sakuda2016_… | 단면 = 330 MPa 성형 (+ Li–In 100 MPa) 뒤 셀에서 꺼내 Ar 이온 CP 로 깎은 시편 → 하중을 뺀 상태로 읽힌다 · 사이클 이력 · 꺼낸 방법 미기재 | 카드 §3-3 · §4-4 (4) · p.114–115 | [카드 해석] · [미확인] | —

## c — 항복 · 경도 · 크리프 값과 정의
- [c] sakuda2016_… | SE 탄성률 **≈20 GPa** (인용 [6,18] · 유리) — *"SE particles deform by compression at a high pressure and have a lower elastic modulus of approximately 20 GPa"* · 항복 · 경도 · 크리프 값 없음 · 일축 항복 환산 없음 | 카드 §3-5 · p.116 | [인쇄 · 인용값] | [6] = `sakuda2013_sulfide_mechanical_property` (18–25 GPa 초음파) · [18] J. Ceram. Soc. Jpn 2013 카드 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] sakuda2016_… | **정성**: *"At the interface between two NCM particles, a relatively large stress concentration develops owing to the high-pressure compression because NCM is a typical brittle material. However, the stress concentration is suppressed at the interface between NCM and the SE"* · 균열 위치 = NCM–NCM 맞닿은 곳 (Fig. 2e) · *"which becomes more significant in the composite electrode with higher NCM ratio"* | 카드 §3-5 · p.116 · Fig. 2e · f | [인쇄] 해석 | 하중 몫 · 접촉력 · 접촉 수 숫자 0 — 우리 DEM AM–AM 몫 (0.52–0.68 @ 100–600 MPa [우리 · CLAUDE.md]) 과 방향만

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · 계산 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 관찰은 3D 전극의 2D 단면뿐 · 2D/3D 진술 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 기공 수치 · 압력 축 없음.  정성 하나 + 대략 산술:
- [i] sakuda2016_… | *"The SE images indicate that the void volume in the electrode using SE-4 μm is smaller than that using SE-16 μm"* · *"The highly dense electrode layer and SE layer can be achieved using smaller-sized SE particles"* (330 MPa · 75 : 25 wt · 무탄소) | 카드 §3-4 · p.115 | [인쇄] 정성 | 'SE images' = SEM 오식으로 읽힘 · 기공률 · 진밀도 [미확인]
- [i] sakuda2016_… | 조밀 양극층 두께 ≈**37.5 µm** (기공 0) · 고체 부피 NCM 0.548 : SE 0.452 — 진밀도는 다른 카드 (NMC111 4.653 `ngandjong2021_…` · 유리 1.88 `sakuda2013_…`) | 카드 §3-1 · §3-7 | [카드 산술] | 원문 값 아님 · 기공 대조 불가

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압과 닿는 것)
- [j] sakuda2016_… | 저자: *"the mechanical properties of electrode materials differ for each material. The process used to prepare the electrode layer also affects the electrode morphology and performance … should be investigated in detail in a future study"* | 카드 §3-8 · p.117 | [인쇄] | —
- [j] sakuda2016_… | 카드가 본 한계: 단면 정성뿐 (기공 · 균열 수 0) · 압력 하나 (330 MPa) · 탈압 · 운전 적층압 없음 · 단면 시편 사이클 이력 미상 (가압 균열인지 사이클 균열인지 못 가름) · 분리막 SE 셀마다 다를 수 있음 · 셀 반복 [미확인] · 'D_SE < D_NCM' 문턱은 0.72 ↔ 1.70 사이 점 없음 | 카드 §11 · §13 | [카드 해석] | —

## k — DEM 의 한계 (서지: A. Sakuda, T. Takeuchi, H. Kobayashi, Solid State Ionics 285 (2016) 112–117)
- [k] sakuda2016_… (Sakuda · Takeuchi · Kobayashi 2016, Solid State Ionics 285, 112–117) | **말 없음** — DEM · simulation · model (기기 이름 빼고) 0 회.  DEM 의 단단한 구가 못 내는 현상의 실측 정성 그림은 있다: 330 MPa 뒤 SE 가 입자 경계 없는 **연속 기지**가 되고 NCM 이 그 안에 박힌다 (Fig. 2b · d · f) — 원문 문장 *"The SEM images also reveal that NCM particles are dispersed in the SE matrix"* (p.115) | 카드 §4-3 · §4-4 (1) | [인쇄] | DEM 에 대한 진술 아님 (카드 해석으로만 연결)

## l — 소성변형이 왜 어려운가 · 택한 우회와 값
- [l] sakuda2016_… (Sakuda · Takeuchi · Kobayashi 2016, Solid State Ionics 285, 112–117) | **계산 없음 → 우회 · 맞춘 값 없음.**  물리 서술만: *"The sulfide-based SEs exhibit the unique mechanical property that dense compacts are formable by pressing the powder at room temperature [6]"* (p.112) · *"SE particles deform by compression at a high pressure and have a lower elastic modulus of approximately 20 GPa [6,18]"* · *"NCM is a typical brittle material"* (p.116) — 무른 SE 의 변형이 단단한 NCM 사이 응력 집중을 덜어 준다는 정성 기전 | 카드 §4-4 (2) · p.112 · p.116 | [인쇄] | 항복 · 소성 변형량 · 비용 숫자 없음

## m — 받아들일 통찰
- [m] sakuda2016_… | **결과 전 대조 항목 (방향) — 입경비 규칙**: 같은 무게비에서 D_SE/D_AM > 1 이면 AM 덩이 · SE 덩이로 갈라지고 AM–AM 맞닿음 · 공극이 남으며, < 1 이면 AM 이 SE 기지에 흩어진다 → 우리 SE 입경 팔 (r_SE 0.5 ↔ 1.5 µm) 에서 AM–AM 배위수 · SE 영역 크기가 같은 쪽으로 움직이는지 (값 대조 아님 · 우리 침대는 모두 '< 1' 쪽 [우리 산술]) | 단계 5 · 후보 D0 · 후보 A | 근거 p.115–116 · Fig. 2a–d (d50 비 0.40 · 0.72 ↔ 1.70 · 3.02 [카드 산술])
- [m] sakuda2016_… | **AM 파괴 보고를 접촉 상대별로**: 균열은 NCM–NCM 맞닿은 곳에 몰리고 NCM–SE 계면에서는 드물다 → 우리 Auerbach 등급 (AM–AM 접촉에 거는 규약 [다른 카드 `dang2019_…` L24]) 을 AM–AM / AM–SE 로 나눠 내고, SE 입경만 바꾼 침대에서 AM–AM 등급 몫이 오르는지를 방향 항목으로 | 조건 R7 · 후보 D0 | 근거 p.116 · Fig. 2e · f
- [m] sakuda2016_… | **함정 — 반쪽셀 고율 전압 차를 양극 몫으로 다 읽지 않기**: 80 mg 유리 분리막 (조밀 ≈0.54 mm) 하나가 2.6 mA cm⁻² 에서 IR ≈0.35 V [카드 산술 · 어림 · σ 4 × 10⁻⁴ · 기공 0] ≈ Fig. 4f 시작 강하 0.42 · 0.53 V 의 대부분 [판독] · 게다가 SE-16 셀의 분리막도 SE-16 으로 보인다 (Fig. 2a ↔ 2b) → 문헌 반쪽셀 율속과 우리 복합 양극 예측을 견줄 때 분리막을 먼저 빼고 셀마다 같은지 확인 | 흐름 밖: STEP4 · Rint ② 반쪽셀 대조 | 근거 p.113 · p.114 · p.117 · Fig. 2a · b · 4f
- [m] sakuda2016_… | **혼합 질의 판정 시점**: 이 논문은 1 분 vortex 건식 혼합의 결과를 **330 MPa 뒤 단면**에서 '균질' 로 읽는다 · 같은 '1 분 진탕' 을 **분말** 에서 본 `kawaguchi2018_dry_coating_model_se_particle_powtec` (Na₂SO₄ 모델) 은 게스트가 덩이로 남는다 · 분쇄 SE 분말 자체가 ≈90–100 µm 덩이 (Fig. 1h [판독]) → 믹서 대조 항목에 '판정 시점 (분말 / 압밀 뒤 단면)' 칸을 둔다 | 흐름 밖: 믹서 (D3 · 확인 블록) | 근거 p.114 · Fig. 1h · Fig. 2b · d

## n — 논문 에이전트 후보
- [n] S. Teragawa, K. Aso, K. Tadanaga, A. Hayashi, M. Tatsumisago, J. Mater. Chem. A 2 (2014) 5095. (원문 ref [17]) | m · 흐름 밖 (믹서 · 코팅) — '작은 SE 단순 혼합 ≈ SE 코팅 전극의 형태' 비교의 **용액 공정** SE 코팅 쪽 (카드 §3-4 · p.115) | papers/ ls (teragawa* 없음) · grep 'Teragawa' = zhou2019 의 다른 논문 (J. Power Sources 2015) 뿐 · '5095' 없음 · wishlist · 후보 표 없음
- [n] A. Sakuda, A. Hayashi, T. Ohtomo, S. Hama, M. Tatsumisago, Electrochem. Solid-State Lett. 13 (6) (2010) A73–A75. (원문 ref [7]) | m · 흐름 밖 (코팅) — 같은 비교의 PLD 코팅 쪽 (refs [6–9]) · 서지 일부만 (제목 원문 목록에 없음) | papers/ ls (sakuda2010* 없음) · grep 'A73' = 이 카드뿐 · wishlist · 후보 표 없음
- (세지 않음) [18] Sakuda · Hayashi · Takigawa · Higashi · Tatsumisago, J. Ceram. Soc. Jpn 121 (11) (2013) 946–949 = `wishlist.md` L18 에 이미 있음 · [8] Sakuda 외 J. Power Sources 196 (2011) 6735–6741 = 후보 표 N-80.

## 카드 문제
1. **`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` L352** (가리킨 카드 아님) — 참고 11 (= 이 논문) 의 메모 *"SE 미립자 · AM 위 SE 코팅이 이온 경로를 개선한다는 근거 (p.A3963) — 입경비 가설의 같은 그룹 쪽 자료"* ↔ 이 원문은 이온 경로 (σ · EIS) 를 **재지 않았다** — 단면 형태 + 율속에서 *"suggests"* 로 낸 해석이고, 입경비 규칙 (D_SE < D_NCM) 은 있다 · 원문 소속은 **AIST** (Takeuchi · Kobayashi) — OPU (Hayashi · Tatsumisago) 그룹이 아니고 제1 저자 Sakuda 만 같은 사람.  값 오류는 아니고 '근거' 의 성격 · '같은 그룹' 표현이 느슨하다.
2. 가리킨 카드 셋 (`kawaguchi2017_…` L231 · `nakamura2020_…` L336 · `kawaguchi2023_…` L293) — 서지 · 메모 모두 원문과 같다 (문제 없음).  `kawaguchi2023_…` §3-2 의 셀 수치 (40 MPa · 180 / 360 MPa · 90 MPa · 298 K) 는 그 논문 자기 값이라 이 원문 (330 · 100 MPa · 30 °C) 과 다르지만 그 카드는 '출처' 로만 적었다 — 오류 아님.
3. `calpa2019_…` L48 · `yano2026_…` L49 — 원문과 같다 (calpa 의 '볼밀 분쇄 에너지 · 시간' 은 calpa 의 말 · 이 원문에 분쇄 시간 없음).
4. 이 카드 (sakuda2016) 자체 — 없음 (원문 쪽 어긋남 · 빈칸 8 항목은 카드 §3-8).

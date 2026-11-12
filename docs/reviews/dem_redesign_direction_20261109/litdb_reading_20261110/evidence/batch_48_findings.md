# 배치 48 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` (391 줄 · 원문 = J. Power Sources 본문 8 쪽 · SI 안내 없음 ·
그림 크롭 44 장 = 도구 8 (전부 다시 자름) + 그래픽 초록 1 + 패널 17 · 식 6 · 근거 문단 12 · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 81 행).
서지 (k · l 인용용) = Kodama M., Komiyama S., Ohashi A., Horikawa N., Kawamura K., Hirai S., *High-pressure in situ X-ray computed tomography and
numerical simulation of sulfide solid electrolyte*, J. Power Sources 462 (2020) 228160, DOI 10.1016/j.jpowsour.2020.228160.
⚠ 주 재료 = **Li₆PS₅Br (75–150 µm 체 분급)** — Li₆PS₅Cl 은 σ 비교 그림 하나 · 최대 103 MPa · 아래 값은 우리 LPSCl 값으로 옮기지 않는다.
쪽 = PDF 쪽 = 인쇄 쪽 (p.1–8).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **기공률 · 상대밀도 숫자 없음** — 누른 채 (in situ) CT 단면 (가압 8.4 · 31.4 · 62.2 · 103.0 · 감압 103.0 · 50.0 · 27.8 MPa) 과 변형률뿐 · 진밀도 분모 · 시료 질량 · 높이 · 지름 없음 ('porosity' 는 본문에 한 번 · 숫자 없이) | 카드 §0 ① · §3-3 (L111–123) · §원문 대조 · 원문 p.4–5 · Fig 3b · 4b | [미확인] | Li₆PS₅Br · 75–150 µm · ≤ 103 MPa
- [a] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 이 카드의 2D 판독: 계산 단면 흰 (기공) 면적 31.3 % (8.4 MPa) → 1.2 % (103.0 MPa · 경계 화소 포함 ≤ 4.3 %) · 인쇄 CT 단면 검은 면적 27–40 % (8.4) · 14–25 % (31.4) · 6–18 % (62.2) · 4–18 % (103.0) (문턱 64–128 · XY · ZX) | 카드 §3-3 표 · Fig 3b · 7b · 8b | [판독 · 단면 한 장] | 복셀 1.62 µm 미만 틈이 빠진 **하한** · 고압에서는 문턱 민감도 > 신호 · 기공률로 인용 금지
- [a] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 변형률 (CT 로 잰 집전체 거리) 0.264 (14.5) · 0.383 (27.1) · 0.431 (46.2) · 0.466 (73.7) · 0.491 (89.3) · 0.473 (99.9 MPa) → 다이면 D = D₀/(1 − ε), D ≤ 1 → **처음 충전 D₀ ≤ 0.51–0.53** · 103 MPa 변형의 81 % 가 27 MPa 까지 | 카드 §3-4 (L124–139) · Fig 3c | [판독] · [카드 산술 · 상한] | D₀ 없음 → D(P) · Heckel 불가 · PEEK 반경 변형 [미확인]
- [a] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 상태 = **누른 채** (스프링 하중 유지 중 CT · EIS) · EIS 25 °C · CT 중 온도 [미확인] · '고압' 정의 = XCT 셀 기준 *"high pressure (>1 MPa)"* | 카드 §3-1 · §0-1 · 원문 p.2 | [인쇄] | 우리 300 MPa 와 다른 뜻

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 103.8 → 28.2 MPa 감압 (0 아님): σ 0.789 → 0.634 mS/cm (**−19.7 %**) · 같은 압력 가압 σ 의 1.65 배 (28) · 1.30 (51) · 1.15 (61) · 1.02 (84 MPa) = 치밀화 비가역 | 카드 §3-5 (L140–154) · Fig 4a · 5b | [판독] · [카드 산술] | Br · 0 MPa 없음
- [b] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 변형률 (CT 집전체 거리) 0.462 → 0.473 (**+0.011**, 오차 막대 ±0.02 안 — 탄성 회복이면 줄어야 함) → 되돌아옴 **측정 불가** · 기대 회복 E 25 GPa 면 −0.003 · 2.5 GPa 면 −0.030 · 다이 기울기 = 구속 탄성률 M (Deng 의 Li₆PS₅Br E 25.3 · ν 0.35 이면 ≈40.6 GPa · 우리 MPM E 1.53 · ν 0.49 이면 ≈26.2 GPa) | 카드 §3-5 · §4-5 · §7-4 · Fig 4c | [판독] · [카드 산술] | 저자 *"the Young's modulus remained almost constant at 25 GPa"* 는 자료로 가를 수 없음 · Fig 4c 기준선은 감압하면 커지는 쪽 (부호 반대)
- [b] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 구조 유지 (영상) *"The structure was relatively unaffected by depressurization … maintained, even at 30 MPa"* | 카드 §3-5 · p.5 · Fig 4b | [인쇄] | 정성

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | *"The 0.2% proof stress of sulfide solid electrolyte (E = 20 GPa) is about 40 MPa"* — **인용 없음 · 재료 미지정 · 20 GPa × 0.002 와 정확히 같다** | 카드 §3-9 (L176–185) · p.5 | [인쇄] · [카드 산술] | 우리 σ_y 근거로 쓰지 않음 · 같은 Li₆PS₅Br 의 lee2025 카드 Heckel σ_y,eff 133 MPa · H/3 ≈0.56 GPa 의 1/3–1/14
- [c] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 일축 항복 환산 · 경도 · 크리프 **없음** · 가압 *"effective Young's modulus ranged from 25 MPa to 250 MPa"* (판독 할선 55–211 MPa · 34–100 MPa 접선 ≈0.7 GPa) = 분말 압밀 컴플라이언스 (재료 값 아님) | 카드 §3-4 · §7-4 · p.5 · Fig 3c | [인쇄] · [판독] · [카드 산술] | 우리 DEM E_eff 1.35 GPa · MPM E 1.53 과 같은 양 아님
- [c] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | *"From molecular dynamics simulation, the Young's modulus of Li6PS5Br is 25 GPa [17]"* — [17] Deng 2016 = 0 K 정적 DFT (정본 카드 Li₆PS₅Br E 25.3 GPa) — 값은 맞고 방법 이름이 틀림 | 카드 §3-9 · p.5 · 결론 1 | [인쇄] · 정본 카드 대조 | —

## d — 단단한 입자 + 무른 입자 혼합 압축의 하중 몫 · 재밍

- [d] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **없음** — 순수 SE 만 (AM · 복합 없음) | 카드 §2 | — | —

## e — 점접촉 법칙이 깨지는 범위와 대안 · 맞춘 값 수

- [e] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **없음** — DEM · 접촉 법칙을 쓰지 않는다 · 일반론만: *"the strain–stress characteristics become nonlinear [18] … for high-accuracy numerical simulation of solid electrolyte compression, nonlinear numerical simulation is required"* | 카드 §4-4 (i) · p.5 | [인쇄] | 맞춘 값 0

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차

- [f] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | MPM 없음 · **해상도 규칙의 실측 문장**: *"the resolution of 1.0 μm was insufficient to measure some microstructures, such as gaps between solid electrolyte particles … large solid electrolyte particles ranging in size from 75 μm to 150 μm were selectively used to prevent a formation of small scale void that is smaller than resolution"* → 입자 지름당 46–93 복셀 · 계산 격자 = CT 복셀 그대로 (350³ · 1.62 µm) · 격자 · 복셀 수렴 시험 · 수치 오차 추정 **없음** | 카드 §3-1 · §4-3 · p.2 · p.3 | [인쇄] · [카드 산술] | '분해능 1.0 µm' < 복셀 1.62 µm (원문 어긋남)

## g — 2D → 3D 경고 · 증거

- [g] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 측정 · 계산 모두 3D · 2D 는 표시 단면 (Fig 3b · 4b · 7 · 8) · 2D → 3D 전이 진술 **없음** | 카드 §4-4 (iii) | — | —

## h — DEM → FE · MPM 으로 넘긴 선례 · 시점

- [h] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **없음** (DEM · FE · MPM 없음) — 대신 '압밀은 **측정** (누른 채 CT) → 그 형상 위에서 **수송만 계산** (영상 기반 FV)' 의 선례 · 넘긴 시점 = 각 압력 단계 (8.4 · 31.4 · 62.2 · 103.0 가압 · 51.4 · ≈32 감압) | 카드 §4-2 · §4-3 · §7-5 | [인쇄] | 역학 · 하중 장 없음

## i — 복합 양극 (AM + SE) 압력별 기공

- [i] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **없음** — 순수 SE 만 | 카드 §2 | — | —

## j — 카드가 스스로 적은 한계 (가압 · 탈압과 닿는 것)

- [j] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 저자: 분해능 부족 → 큰 입자만 · 최대 ≈100 MPa (PEEK 내구) · *"the size of solid electrolyte particles used in this study was very large … but the principles revealed can be applied for smaller solid electrolyte particles"* (근거 = 입경별 σ '거의 같음' 한 문장 · 숫자 없음) · 비선형 계산 필요 | 카드 §0 ⑨ · p.2 · p.5 | [인쇄] | —
- [j] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | 카드: 감압 28 MPa 에서 멈춤 · 되돌아옴 해상도 밖 · 계산 영역 = 원 입자 3.8–7.6 개 (RVE 시험 없음) · 축척 막대 원통 ⌀ ≈0.58–0.61 mm ↔ 계산 영역 567 µm (들어가는 몫 82–87 %) · 기공 · 진밀도 · 입력 σ_400MPa 미인쇄 | 카드 §3-5 · §3-8 · §11 | [판독] · [카드 산술] · [미확인] | —

## k — DEM 의 한계 (인용 서지 병기)

- [k] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation (Kodama · Komiyama · Ohashi · Horikawa · Kawamura · Hirai, J. Power Sources 462 (2020) 228160) | **말 없음** — DEM 을 쓰지 않는다.  가장 가까운 원문: *"This tendency is a widely observed phenomenon for powder materials and highly porous media, and the strain–stress characteristics become nonlinear [18]. This finding suggests that, for high-accuracy numerical simulation of solid electrolyte compression, nonlinear numerical simulation is required."* (p.5).  단단한 구 · 형상 고정 모델에 없는 기전 셋을 실측 (3D · 누른 채) 으로 보인다: *"the size of the solid electrolyte particles decreased because they were crushed by the high pressure. Small solid electrolyte particles filled the pores"* · *"particle boundaries were difficult to see at 103.0 MPa"* (p.5 · Fig 3b) | 카드 §4-4 (i) · §3-3 | [인쇄] | Li₆PS₅Br 75–150 µm (파쇄 체제) · 정성 · 숫자 없음

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation (Kodama 외, J. Power Sources 462 (2020) 228160) | 계산에서 소성 · 큰 변형이 어려운 이유 **논의 없음**.  우회 = **압밀을 계산하지 않고 측정한다** (in situ CT) → 측정 형상 위에서 정상 전도만 푼다 (영상 기반 · 350³ = 42.9 M 셀 · 1.62 µm · SOR · OpenMP · 맞춘 값 0 · 입력 σ_400MPa 하나 (값 미인쇄) · 계산 시간 [미확인] · 비용은 실험 쪽 = XESC 최대 100 MPa · 75–150 µm 로 제한).  소성 문장: *"The concentrated pressure around the solid electrolyte particle's contact points can be high as or higher than the 0.2% proof stress, and therefore, the solid electrolyte can plastically deform."* (p.5 · 0.2 % 내력 출처 없음).  검증 = 계산 ÷ EIS 1.80 (8.7 MPa) → 1.07 (104 MPa) (Br) · 2.3–2.6 → 1.03 (Cl) | 카드 §4-3 · §4-4 (ii) · §3-6 | [인쇄] · [판독] · [카드 산술] | 역학 계산 없음 · 내력 출처 없음

## m — 받아들일 통찰

- [m] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **복셀 FV (접촉 저항 0) ÷ 실측의 크기** — 순수 SE 저밀도 ×1.8–2.6 · ≈100 MPa ×1.03–1.07 → STEP3 σ_ion 을 실험 옆에 놓을 때 CL-81 '상한' 한정어에 **기공 수준을 같이** 적는다 | 단계 7 · 흐름 밖: Rint ② (SE–SE 계면을 0 으로 둘 근거의 압력 범위) | 카드 §3-6 · §7-3 · Fig 5 · 6 | [판독] · [카드 산술] | 우리 복합체 · 해상도로 배수 전이 불가
- [m] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **해상도 규칙의 인용 문장** — 해상도보다 작은 틈 · 목은 영상 · 격자에서 사라져 σ 를 과대평가 → 지름당 셀 수 규칙 (U1 · U6 · MPM d_h/dx ≳ 3.5 · STEP3 vox 수렴) 의 실측 쪽 근거 | U1 · U6 · 단계 7 | 카드 §3-1 · §9-2 · p.2 | [인쇄] | 수렴 시험 자체는 없다
- [m] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **다이 감압의 기울기 = 구속 탄성률 M (E 아님)** — 언로딩 기대값을 M 으로: 우리 MPM (ν 0.49) M ≈26 GPa → 300 MPa 제하 탄성 회복 ≈1.1 % (기공 없는 SE 가정) · 측정 자료는 ±0.02 해상도로 이것을 못 가른다 | 단계 6 · R4 | 카드 §3-5 · §7-4 · §8 | [카드 산술] | 가정 = 순수 탄성 제하 · 다이
- [m] kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation | **인용 고리 함정** — '황화물 입자 사이 접촉 저항 무시' 는 이 논문 (refs 19 · 20 = Otani 그룹) ↔ otani2023 (ref 22 = 이 논문) 이 서로를 근거로 든다 · 자료는 고압 (≥ 60–100 MPa) 에서만 받친다 → 인용 때 압력 범위 표지 | 흐름 밖: Rint ② · 문헌 인용 규율 | 카드 §0-1 · §9-5 | [인쇄] · [카드 관찰] | —

## n — 논문 에이전트 후보

- [n] Y. Lei, S. Yan, S. Huang, W. Lu, S. Sun, M. Shou, F. Feng, Experimental and numerical investigation of densification behaviors during powder compaction, J. Adv. Mech. Design, Syst. Manuf. 12 (2018) 17–619 (서지 일부 이상 — 쪽 '17–619' 인쇄 그대로 · DOI 10.1299/jamdsm.2018jamdsm0022) | e · l — 분말 압밀의 비선형 응력–변형 · 수치 압밀 방법 (이 논문이 '비선형 계산 필요' 의 근거로 든 ref 18) · 카드 §12 | ls lei* = lei2026 (다른 논문) · "jamdsm" · "densification behaviors during powder compaction" grep 없음 → 카드 없음
- [n] T. Miyuki, Y. Morino, K. Otani, Denki Kagaku 88 (2020) 54–64 (제목 없음 — 서지 일부만 · DOI 10.5796/denkikagaku.20-TE0002) | a · m — 기공비 ↔ tortuosity 지수 상관 · '접촉 저항 무시' 의 공동 근거 (ref 20 · otani2023 과 같은 그룹) | ls miyuki* 없음 · "denkikagaku" grep 없음 (Miyuki 는 다른 카드의 공저자로만) → 카드 없음
- [n] K. Otani, T. Muta, T. Furuta, M. Murata, M. Iwasaki, T. Miyuki, G. Inoue, T. Kaburagi, Y. Ishiguro, Calculational Study of Ionic Conductivity Reduction Observed in All-Solid-State-Batteries, The 60th Battery Symposium, Japan, 2MH23, 2019 | m — otani2023 의 앞판 학회 초록 (ref 19 · 구하기 어려울 수 있음) | "2MH23" · "Battery Symposium" grep 없음 → 카드 없음
- [n] M.B. Dixit, M. Regala, F. Shen, X. Xiao, K.B. Hatzell, Tortuosity Effects in Garnet-Type Li7La3Zr2O12 Solid Electrolytes, 11, 2018, pp. 2022–2030 (학술지 이름 누락 — 서지 일부만 · DOI 10.1021/acsami.8b16536) | m · 단계 7 — CT 기반 SE tortuosity (산화물) · ref 13 (본문은 'Marm et al.') | "acsami.8b16536" · "Tortuosity Effects in Garnet" grep 없음 (Dixit 는 다른 논문으로만) → 카드 없음
- [n] C. Tan, S.R. Daemi, O.O. Taiwo, T.M.M. Heenan, D. Jl Brett, P.R. Shearing, Evolution of electrochemical cell designs for in-situ and operando 3D characterization, Materials 11 (2018) 2157 | 결과 전 대조 측정 설계 — in situ CT 셀 재료 (PEEK · PFA) · ref 12 | "ma11112157" · 제목 grep 없음 → 카드 없음
- (n 밖 — 이 논문이 인용하지 않은 같은 그룹 후속 · 다른 카드가 인용) M. Kodama, A. Ohashi, S. Hirai, J. Power Sources Adv. 4 (2020) 100019 (단일 SE 입자 고압 XCT · `faka2026` ref 21) · A. Ohashi, M. Kodama, … S. Hirai, J. Power Sources 470 (2020) 228437 (복합 전극 응력 분포 · `heck2026` ref 61) — 정본 카드 없음 ("100019" · "228437" grep = 그 카드들의 인용만).

## 카드 문제

(원문을 직접 읽고 이 논문을 가리킨 정본 카드의 표기를 대조 — 어느 카드도 고치지 않았다.  세 카드 모두 이 논문에서 **숫자를 옮기지 않았다** → 2 차 인용 값 어긋남 0 건.)

1. `otani2023_ionic_conductivity_path_resistance_separation_model` L265 "카드 없음 — 고압 in situ XCT · 황화물 입계 저항 무시 근거" — 이제 정본 카드가 있다 (이 카드) · 그리고 원문이 무시한 것은 **입자 사이 접촉 저항** (*"contact resistance between solid electrolyte particles"*) 이고 '입계 저항' 을 따로 다루지 않는다 (치밀 펠릿 안의 입계 몫은 입력 σ_400MPa 에 들어 있다) — 표현 차이.
2. 같은 카드 L30 · L81 "refs 7 · 22 의 황화물 입계 저항 무시와 정합" — 위와 같은 표현 차이 · 근거의 압력 범위 (고압 일치 · 저압 계산 ÷ 실측 ×1.8–2.6) 가 빠져 있다 · 인용 고리 (이 논문 refs 19 · 20 = Otani 그룹) 미기재.
3. `yadav2021_lpscl_sieved_psd_impedance_tortuosity` L321 · `faka2026_particle_size_consolidation_strain_lpscl` L251 "카드 없음" — 이제 있다 (서지는 원문과 같다 · faka2026 의 끝 저자 S. Hirai ✓).
4. `yadav2021_lpscl_sieved_psd_impedance_tortuosity` L51 — Yadav 원 논문이 [5] (= 이 논문) 에 *"compacity … morphology and size of individual particles and their distribution"* 를 귀속 — 이 논문은 입경 분포별 충전 밀도를 재지 않았다 (입경별 σ '거의 같음' 한 문장뿐) · **Yadav 원문의 인용 문제** (카드는 원문 그대로 옮김).
5. 후보 표 (S8) N-8 의 '왜' 칸 "고압에서 in situ XCT (누른 채 구조 · 공극)" — 원문 최대 ≈103 MPa (이 논문의 '고압' = > 1 MPa 정의) · 공극은 숫자 없이 영상뿐.

# batch_18 정독 근거 (카드 7 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `landesfeind2018_tortuosity_impedance_vs_tomography` (419 줄) · `lee2026_unveiling_ptfe_dry_electrode_digital_twin` (487) · `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` (469) · `matthews2024_ptfe_nanofibril_network` (772) · `morasch2018_binder_gradient_impedance_tortuosity` (402) · `nakamura2020_dry_coating_ncm_li3ps4_core_shell` (362) · `nguyen2020_electrode_tortuosity_factor` (255). 끝까지 못 읽은 카드 없음 (일곱 장 모두 두 – 네 번에 나눠 마지막 줄까지 읽음). 읽은 판 = scratchpad 사본 `litdb_read/litdb/papers/` (litdb_read/CANON_SHA.txt = `c8faad2d7919133f4679a3b9f326f774a763bcdf`). 그사이 움직인 정본 가지 끝 (코디네이터 알림) 은 읽지 않았다. 사용량 한도로 끊긴 뒤 이어 쓰기 전에 다시 확인: 일곱 장 줄 수가 처음 읽을 때와 같음 · md5 앞 12 자리 c0c89ff5beee · 9169d825c015 · 44ff953112ca · 158a927947ee · beeafe51bdc9 · da9c5161d35d · 5887a394f04a (목록 순서).

배치의 성격: 수송 값의 정의 · 측정법 묶음이다. **액체 전해질 LIB 의 tortuosity 논문 넷** (landesfeind2018 = EIS 값 검증 + 단층촬영 대조 · malifarge2017 = 두 레일 전송선 모델 · morasch2018 = 바인더 구배와 방향 의존 · nguyen2020 = 관통형 τ ↔ 전극 τ_e 의 복셀 계산), **LIB 건식 전극의 PTFE 피브릴 SEM 하나** (matthews2024), **황화물 ASSB 양극의 실험 + 측정 구조 위 복셀 수송 둘** (lee2026 = NCM + LPSCl + VGCF + PTFE · 370 MPa / nakamura2020 = NCM111 + Li₃PS₄ 유리 · 360 MPa). **DEM · MPM 을 쓴 카드는 없다.** 순수 SE 의 압력별 기공 곡선 = 0 · 되돌아온 양을 잰 카드 = 0 · 항복 · 경도 · 크리프 값 = 0. 복합 양극의 기공은 **한 압력 두 점** (nakamura2020 360 MPa · lee2026 370 MPa) 이 있다. 그래서 k (DEM 의 한계) · l (소성의 어려움) 은 일곱 장 모두 "말 없음" 이고, 그 아래에 (3) 실험이 보인 "단단한 구 · 점접촉 가정 밖의 것" 과 (4) 카드의 풀이를 구분해 적었다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `stated(그림)` · `[인쇄]` · `[판독]` · `판독` · `[우리 산술]` · `카드 산술` · `파생` · `derived` · `우리 유도` · `우리 재계산` · `🧮 DERIVED` · `[추정]` · `[미확인]` · `n/a`) · 없으면 "표지 없음". "카드 서술 · 카드의 풀이" = 논문 문장이 아니라 카드 작성자의 서술. 따옴표 안 영어 문장은 카드가 옮겨 둔 원문. "내 검산" = 이 정독에서 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님). 카드가 "인용 금지" 표지를 붙인 값은 숫자를 옮기지 않았다 — landesfeind2018 의 `판독` 값 (카드 머리 L8 "TREND 전용, 정밀 인용 금지" — L210–213 의 그림 판독) · matthews2024 의 디지타이즈 값 (L657 "어떤 디지타이즈 값도 물리 상수로 인용 금지" — §4.5 L246–251 · §8 L443–447 과 거기서 낸 L456 의 비). 그리고 matthews2024 L600–601 의 우리 σ_e 비 두 값도 옮기지 않았다 (이유는 "카드 문제" 2). "랩 표준과 다른 문헌 값" = 순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ 과 다른 값이라는 표시 (기준은 그대로다).

형식: `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계` (k · l 은 slug 옆에 인용할 서지 · m 은 `무엇을 | 우리 쪽 어디에 | 왜 (근거 위치)`)

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

압력별 곡선이 있는 카드 = **0**. 순수 황화물 SE 를 눌러 밀도 · 기공을 잰 카드 = **0**. 닿는 것은 부피 계산에 쓴 밀도 한 줄 (lee2026) 과 순수 SE 펠릿의 전도도 (nakamura2020) 뿐이다.

- [a] lee2026_unveiling_ptfe_dry_electrode_digital_twin | Li₆PS₅Cl 의 상 밀도 1.86 g/cm³ (부피분율 · 상대밀도 계산용 — NCM 4.44 · VGCF 2.10 · PTFE 2.06 g/cm³ 과 함께) | §3-1 L68 · SI p.17 | [인쇄] | 순수 SE 펠릿의 기공 · 압력 곡선 없음 · 1.86 은 랩 표준 (1.64) 과 다른 문헌 값 — 이 카드의 밀도 기반 기공 (15.4 · 12.6 %) 과 상대밀도 (82.5–87.4 %) 는 모두 그 1.86 기준 · 실측 밀도인지 결정 밀도인지는 카드에 없음
- [a] lee2026_unveiling_ptfe_dry_electrode_digital_twin | SE 분리막층 = LPSCl 150 mg (D50 5 µm) 을 ⌀13 mm PEEK 몰드에서 70 MPa 펠릿 → 전극을 올려 370 MPa 5 min → 적층압 50 MPa 로 시험. 펠릿 밀도 · 두께 없음 · 순수 LPSCl 펠릿의 σ₀ 측정도 없음 (복셀 계산의 σ_LPSCl 입력 0.1 S/m = 1.0 mS/cm 는 출처 미기재) | §3-1 L69 · §0 L30 · L33 · §4-4 L253 · §10-7 L436 | [인쇄] (조건) · [미확인] (밀도 · σ₀ 출처) | 기공 값 0
- [a] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 순수 SE (glassy Li₃PS₄ · 75Li₂S·25P₂S₅) 는 전도도만: 합성 직후 3 × 10⁻⁴ S/cm @ 298 K · 습식 분쇄 (개수 D50 0.49 µm) 뒤 압분 펠릿 0.84 × 10⁻⁴ S/cm @ 298 K. 펠릿 성형압 · 밀도 · 기공은 카드에 없음. 반쪽셀의 SE 층 = 분쇄 안 한 LPS 80 mg 을 양극 10 mg 과 함께 360 MPa 로 누름 (밀도 없음) | §3-1 L61–62 · §3-4 L92 · p.3 · p.4 · p.6 | [인쇄] | Li₃PS₄ 유리 — LPSCl 아님 · 기공 값 0 · 압력 곡선 없음
- [a] landesfeind2018 · malifarge2017 · matthews2024 · morasch2018 · nguyen2020 | 해당 없음 — 액체 전해질 LIB (SE 없음) | — | — | —

## b. 압력을 뺄 때 되돌아오는 양과 잰 방법

되돌아온 양을 잰 카드 = **0**. 닿는 것은 "언제 · 어떤 상태에서 쟀는가" 의 기록뿐이다.

- [b] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 재지 않음. 이력 = ⌀10 mm 일축 360 MPa → 303 K 50 회 충방전 → 완전 방전 뒤 분해 → FIB-SEM (하중을 뺀 뒤 · 사이클을 거친 구조). DC 분극은 따로 만든 새 80 mg 펠릿 (360 MPa). 누른 채의 두께 · 뺀 뒤의 두께 어느 것도 실측 없음 — 층 두께 ≈ 38 µm (반쪽셀 10 mg) · ≈ 300 µm (DC 80 mg) 는 복합 밀도 3387 kg/m³ 로 낸 카드 산술 | §3-4 L92–98 · §3-6 L124 · §10-7 L320 | [인쇄] (이력) · [우리 산술] (두께) | 같은 시료의 누른 채 ↔ 뺀 뒤 비교 없음 · Li₃PS₄ 유리
- [b] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 재지 않음. 전극을 370 MPa 5 min 누른 뒤 FIB-SEM · 셀은 적층압 50 MPa · 전도도 측정 중 압력 · 전극 두께는 [미확인]. 카드가 우리 대칭셀 계획의 기록 항목으로 "가압 중 / 놓은 뒤 두께" 를 적음 | §3-1 L69–72 · §3-2 L87 · §8-8 L420 · §10-10 L439 | [인쇄] (이력) · [미확인] | 되돌아온 양 0 건
- [b] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 탈압 아님 — 사이클 중 압력 변화 (OEP · NCM/LTO · 일정 체적 10 MPa · 0.2 C · 압력센서 분해능 0.1 kg): 첫 사이클 ΔP 최저 ≈ −0.44 MPa (PTFE 0) / ≈ −0.22 MPa (0.2 wt%) | §3-9 L192 · Fig S19 | [판독] | 전기화학 부피 변화 — 용량당 정규화 없음
- [b] matthews2024_ptfe_nanofibril_network | 재지 않음 — 캘린더 80 °C · 라인압 50 N/mm → ≈ 100 µm (porosity · 밀도 미보고). 카드가 옮긴 타 논문 값: Hippauf 2019 의 NMC + Li₆PS₅Cl + CNF + PTFE 0.1–1 wt% 막 ≈ 200 µm → 300 MPa 압축 뒤 ≈ 100 µm | §3.2 L140 · §8 L462 · §2 L99 | stated · [인쇄 p.3–5] (hippauf2019 카드 기준 · 카드의 2026-10-13 정정 표지) | 압축으로 준 두께지 되돌아온 양이 아님
- [b] landesfeind2018 · malifarge2017 · morasch2018 · nguyen2020 | 이 카드들에 없음 | — | — | —

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기 환산

항복 · 경도 · 크리프 값을 준 카드 = **0**. **일축 항복 세기로의 환산은 어느 카드에도 없다.**

- [c] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 값 없음 — 정성 서술뿐: 황화물 SE (Li₃PS₄ 유리) = 연하고 연성 (근거 ref 24 = Sakuda 2013) · NCM = 단단 · 취성. 원문: "a significant difference between the mechanical properties of the active material and solid electrolyte particle is a key property for successful dry coating" | §3-2 L78 · L16 · p.6 | [인쇄] (인용문) | 수치 0 · Li₃PS₄ 유리
- [c] matthews2024_ptfe_nanofibril_network | 기계 물성 (인장 강도 · 접착력 · 모듈러스) 미보고 — "flexible / fabric-like" 같은 정성 표현뿐 | §8 L466 · §4.2 L196 | n/a | LIB 건식 전극
- [c] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 논문 값 없음. 카드가 비교표에 우리 쪽 입력을 적음: DEM E_eff 1.35 GPa · MPM E 1.53 · σ_y 0.30 (3D) | §7-1 L330 | 표지 없음 (우리 값) | 논문의 측정이 아님 — 환산 없음
- [c] landesfeind2018 (L57) · morasch2018 (L52) · nguyen2020 (L62) · malifarge2017 | 카드가 "n/a" 로 적음 (E_SE · Heckel 같은 소재 물성 앵커를 주지 않는 논문) | — | n/a | —

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

하중 몫을 수로 준 카드 = **0**. 닿는 것은 (1) 눌렀을 때 단단한 AM 이 깨지는지와 무른 SE 껍질이 그것을 막는지 (nakamura2020 — 실측 구조), (2) 층 두께에 따른 응력 전달 (nakamura2020 — 저자 추정), (3) 섬유 바인더 함량에 따른 치밀화 (lee2026), (4) 압연에 따른 판상 입자 정렬 (malifarge2017) 이다.

- [d] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 막자 혼합 복합 (NCM111 + Li₃PS₄ 13.1 wt%) 을 360 MPa 로 누르면 NCM 2차 입자가 1차 입자 사이로 깨짐 (Fig 7a) → NCM 총 표면 1.51 µm²/µm³-전극 ↔ 코팅 (SE 껍질 0.1–0.2 µm) 은 1.26 (균열 없이 거의 구형). 원문: "the compressive stress acting on the NCM particles was damped by the soft and ductile LPS shell layer" | §3-6 L141–146 · §7-1 L249 · p.7–8 · Table 1b · Fig 7 | [인쇄] (면적 · 인용문) | 하중 몫 수치 없음 · FIB-SEM 은 50 회 사이클 뒤 시료 (L320) · 20 µm 정육면체 1 개 · NCM111 단봉 4.7 µm · Li₃PS₄ 유리 · 카드의 "+20 %" 는 1.51 ÷ 1.26
- [d] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 압축 뒤에도 남는 계면 미세공극 (IMV): NCM 표면 중 "NCM 사이 공극" 과 닿은 몫 = 혼합 36.7 % ↔ 코팅 16.4 % (NCM–LPS 접촉 몫 54.1 ↔ 67.8 %) | §3-6 L142–147 · p.8 · Table 1b | [인쇄] | 세 몫 합 = 100 % — NCM–NCM 맞닿은 면은 분모 밖 ([우리 산술] L31)
- [d] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 껍질이 있어도 누르면 AM–AM 접촉이 생김: "the continuous shell layer of LPS was partially pushed away when the cathode powder bed was compressed" → 이미지 기준 전자 σ_eff/σ_B 0.233 (혼합) → 0.208 (코팅) = −11 % | §3-6 L155 · L160 · p.8 · Table 1c | [인쇄] | 도전재 없는 전극 · 한 압력
- [d] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 층 두께와 응력 전달 (저자 추정): DC 분극 셀의 양극이 반쪽셀보다 ≈ 8 배 두꺼워 (카드 산술 ≈ 300 ↔ ≈ 38 µm) 압축 응력이 덜 전달되고 NCM–NCM 접촉이 줄었을 것 → DC σ_e 가 코팅에서 −94 % (5.9 × 10⁻⁶ → 3.6 × 10⁻⁷ S/cm) 인데 이미지는 −11 % | §0 L33 · §3-4 L98 · §3-7 L167–169 · p.8–9 · Table 2 | [인쇄] (값) · 원문 "speculated" · [우리 산술] (두께) | 시험하지 않은 설명 (§10-11 L324) · 두 측정의 시료 상태도 다름
- [d] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 같은 370 MPa 에서 PTFE 함량에 따른 치밀화: 상대밀도 84.6 (PTFE 0) → 87.4 (0.2) → 86.8 (0.5) → 82.5 % (1.0 wt%). 저자: "excessive PTFE increased electrode porosity and impeded mass transport" | §3-7 L163–168 · Table S2 · p.9 | [인쇄] | 하중 몫 아님 — 결과 밀도만 · LPSCl 1.86 g/cm³ 기준 (랩 표준과 다른 문헌 값)
- [d] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 누른 뒤가 아니라 사이클 뒤의 AM 균열: 200 회 뒤 PTFE 0 전극은 NCM 균열 · 0.2 wt% 는 "no noticeable cracks" · OEP 에서 0.2 wt% 가 압력 감소가 작음 (저자 해석 = 고른 분포가 응력을 고르게 나눔) | §3-9 L192–194 · p.9–11 · Fig S19 · S20 | [인쇄] (정성) · [판독] (ΔP) | 압밀 직후의 균열 정량 없음
- [d] malifarge2017_tortuosity_symmetric_cell_impedance_tlm | (하중 몫 아님 — 누르면 입자가 돌아눕는다는 근거) 판상 흑연 가운데 집전체와 평행에 가까운 입자가 압연압에 따라 같은 배치에서 30–60 % ([21] 의 XRD 정량). "The tortuosity values increase as the amount of graphite particles parallel to the current collector increases" | §0 L43 · §8-1 L343 · E3332 | stated | 방향 분율과 τ₂ 를 전극별로 짝지은 자료는 이 논문에 없음 (문장뿐) · 액체 LIB
- [d] matthews2024_ptfe_nanofibril_network | (하중 몫 아님 — 혼합 전단) 10–20 µm NMC 가 100–200 µm PTFE 원료 입자에 눌려 표면 거칠기가 PTFE 결정자와 맞물리고, 이어지는 전단에서 실이 뽑힘. 압축 중 피브릴이 끊어지는지는 문헌이 갈림 (Hippauf 2019: NMC–Li₆PS₅Cl 복합양극 압축 중 끊어질 것 ↔ Lee 2023: 과도한 캘린더링 뒤에도 조밀한 망) | §4.3 L205–215 · §5.4 L311–315 · §12-6 L662–663 | stated (정성 · 문헌 대비) | LIB · 관찰 기반 — 측정 아님
- [d] landesfeind2018 · morasch2018 · nguyen2020 | 이 카드들에 없음 | — | — | —

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값의 수

**이 배치에 없음** — 접촉 법칙을 다룬 카드가 없다 (DEM 을 쓴 카드 0). nakamura2020 은 같은 비교 (코팅 ↔ 혼합 · 360 MPa) 를 DEM 으로 돌린 카드 (`so2022_dem_compaction_coated_particles_assb`) 를 링크로만 가리킨다 (L16 · L261).

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정

**이 배치에 없음** — MPM 을 쓴 카드가 없다. 아래는 MPM 이 아니라 복셀 · 사다리 수송 계산의 해상도와 오차 추정 자료 (참고용 — 쓸 수 있는 부분은 m 에 옮김).

- [f] nakamura2020_dry_coating_ncm_li3ps4_core_shell | (MPM 아님 · 측정 구조 위 복셀 Poisson) 복셀 0.2 µm · 100³ = 20 µm 정육면체 1 개 (NCM 약 4 지름) · 저자 "sufficient spatial resolution" · 경계 = 두께 방향 1.0 / 0.0 V + 나머지 면 주기 · 계면 저항 항 없음. 카드 산술: SE 개수 D50 0.49 µm ≈ 2.5 복셀이라 SE–SE 목이 부분적으로만 풀림 · 측정 f ÷ 복셀 f = 1.65 (코팅) · 1.55 (혼합) = 복셀 값이 측정보다 **낮다**. 수렴 · 반복 · RVE 시험은 안 함 | §3-6 L124–125 · §4-2 L196 · §3-7 L170 · §6 L228 · §7-2 L253 | [인쇄] (설정) · [우리 산술 · 추정] (해상 · 비) | 수송 계산 — 역학 · 접촉 없음 · 측정과 복셀의 시료가 다름 (L320)
- [f] lee2026_unveiling_ptfe_dry_electrode_digital_twin | (MPM 아님 · GeoDict FVM) 복셀 20.83 × 20.83 × 50 nm (비등방 — 그림 범례는 "Voxel size: 20 nm") · 25 µm 정육면체 1 개 (NCM D50 7 µm 의 약 3.6 배) · 검증 = 부피분율 ↔ 밀도 기반 대조 (Table S1) 하나 (기공 차 −2.5 · −0.7 %p) · 분할 정확도 지표 · RVE 수렴 · 재구성 반복 [미확인]. 시뮬 ÷ 실측: σ_e 0.99 · 0.97 · σ_ion 1.46 · 1.42 (σ_LPSCl 입력 1.0 mS/cm 에 조건부) | §3-2 L84–86 · §4-2 L243 · §3-12 L226–228 · §10-2 L431 · §10-8 L437 | [인쇄] · [우리 산술] · [미확인] | 수송 계산 — 역학 없음
- [f] nguyen2020_electrode_tortuosity_factor | (MPM 아님 · 복셀 유한차분 TauFactor) 3D 구 충전 A: 입경 2 µm · 100³ 복셀 · 250 nm (내 검산: 지름당 8 복셀 · 한 변 12.5 지름) ↔ B: 입경 5 µm · 50³ 복셀 (지름당 20 복셀 · 한 변 2.5 지름) — B 는 모사 임피던스가 TLM 에서 벗어남 = 대표성 부족 신호 (p6–7). 오차 추정 대신 쓴 것 = 가장 단순한 구조의 교차검증 (곧은 관통 기공에서 두 방법 모두 τ = 1) + "TLM 45° 에서 벗어나면 부피가 비대표이거나 균질화 불가" 진단. 반복 실현 · 시드 통계 없음 | §3-1 L31 · L37–38 · §6 L126 · §6-bis L131 · L134 · §10 L217 | stated(그림) · stated · 내 검산 (지름당 복셀) | Table 1 은 복셀 1 µm (가정) ↔ Fig 5 캡션 250 nm (원문 불일치 L60) — 지름당 복셀 수는 캡션 값 기준 · 액체 LIB
- [f] landesfeind2018_tortuosity_impedance_vs_tomography | (MPM 아님 · X선 단층촬영 재구성 위 수치 확산) voxel 325 nm · 통계적으로 의미 있는 부피 (입자 수천 개) 를 보려면 ~1 mm³ 가 필요하고 그 해상도로는 바인더 · 탄소가 안 보임. 불확도로 보고한 것은 이진화 문턱 변화 (± 0.03–0.06) 뿐 · 고해상 재구성 (15 µm 큐브 · 입자 ~8 µm) 의 τ 2–7 은 비대표 (인용 Ref 17) | §4-6 L157–159 · §3 L78 · §8-2 L306–307 · §10 L369 | stated | 수송 · 영상 — 해상도 ↔ 대표 부피 맞바꿈의 실례
- [f] malifarge2017_tortuosity_symmetric_cell_impedance_tlm | (MPM 아님 · 1D 사다리 회로) 이산 사다리 (행렬 Kirchhoff · Eq 2–10) 는 해석식 Eq 11 로 O(1/n) 수렴 — n × 상대차 ≈ 0.89 (n = 101 · 401 · 1601 에서 같은 값) → n ≥ 100 이면 < 1 %. 원문은 n 을 적지 않음 | §4-3 L184 · 원문 대조 기록 L455 | 우리 재계산 | 카드 작성자의 검산 — 논문 수치 아님
- [f] morasch2018_binder_gradient_impedance_tortuosity | (MPM 아님 · RC 사다리) 카드가 원문 매개변수로 RC 사다리 4000 요소를 다시 풀어 원문 겉보기 저항 비 (0.750 · 1.250 · 0.531 · 1.656) 를 재현 · 균질 기준은 de Levie 해석해와 대조 (위상 극소 43.40°) | §3 L65 · §4-4 L128–129 | 파생 | 카드 검산
- [f] matthews2024_ptfe_nanofibril_network | (논문 내용 아님 — 카드가 적은 우리 복셀 규칙) 구 스탬프 게이트 d/vox ≥ 2 · 생산 복셀 0.15 µm · 30 nm 섬유를 풀려면 vox ≤ 0.015 µm (≈ 16 TB · dof ∝ vox⁻³ 외삽) → "격자로 닫히지 않는다" | §10.2 L568–583 | 🧮 DERIVED (ours) | 수송 격자의 첨가제 표현 — MPM 해상도 규칙 아님

## g. 2D 결과를 3D 로 옮길 때의 경고나 증거

직접 닿는 카드 = **1** (nguyen2020 — 2D 손그림 사례와 3D 구 충전이 한 논문에 같이 있음). 나머지는 간접.

- [g] nguyen2020_electrode_tortuosity_factor | 같은 두 정의 (관통형 τ ↔ 전극 τ_e) 의 차가 2D 손그림 구조에서는 +1.0 … +46.7 % (Fig 4 A–D · 300 × 300 px) 인데 3D 구 무작위 충전에서는 +0.8 / +3.9 % (Fig 5 · 퍼콜레이션 > 99 % · 막힌 기공 4 / 8 %) | §3-1 L33–38 · L43 · p4–6 | stated(그림) · derived (비) | 2D 구조는 MS Paint 로 그린 개념 증명용 (L105) — 2D 와 3D 가 같은 구조의 두 표현이 아님 · 액체 LIB
- [g] nguyen2020_electrode_tortuosity_factor | 카드의 경고: 2D 사례 (Fig 2–4) 의 절대 크기 (예 +46.7 %) 를 3D 침대 기대치로 쓰지 말 것 — 3D 의 근거는 구 충전 2 개 (Fig 5) 와 설계된 2 층 1 개 (Fig 6) 뿐 · 반복 · 시드 없음 | §7 L198 · §10 L217 | 카드 서술 | 논문 문장 아님
- [g] nguyen2020_electrode_tortuosity_factor | 2D 와 3D 의 계산 설정 자체가 다름: 2D 는 전극 기공과 정렬된 곧은 기공 분리막 · 3D 는 분리막 기공망 대신 전해질만 있는 자유 층을 두 전극 사이에 둠 (데이터 준비 단순화) | §4-C L101 · p10 | stated | —
- [g] morasch2018_binder_gradient_impedance_tortuosity | 2D → 3D 는 아님 — 모의는 2D (전극 50 × 260 µm) 인데 저자가 "1D 로도 충분" 이라 적음 (가로로 균질한 연속체라 차원을 내려도 같다는 쪽의 사례) | §3 L56 · §4-9 L167 · A3460 | stated | 입자가 없는 균질 모형 — 입자 계산의 2D ↔ 3D 근거가 아님
- [g] malifarge2017 · landesfeind2018 | 2D → 3D 아님 — 1D 균질 TLM 이 dead-end 기공 · 두께 방향 구배를 못 본다는 한계 (malifarge §10 L395) · 강구 검증은 균질 구 충전 한 기하뿐 (landesfeind2018 §10 L365) | — | 카드 서술 | —
- [g] lee2026 · matthews2024 · nakamura2020 | 이 카드들에 없음 (3D 재구성 또는 표면 SEM — 차원을 옮기는 논의 없음) | — | — | —

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

**이 배치에 없음** — DEM 을 쓴 카드가 없다. 닿는 것은 "눌린 구조를 계산하지 않고 재서 (FIB-SEM) 복셀 수송으로 넘긴" 두 건이다 (우회의 성격은 l 에).

- [h] lee2026_unveiling_ptfe_dry_electrode_digital_twin | DEM 아님 — 370 MPa 로 누른 전극 → FIB-SEM 500 장 → U-Net 분할 → 복셀 FVM (σ_e · σ_ion) → 반쪽셀 2 C 시뮬 (25 µm). 카드 분류: 측정 재구성 = 하향식 ↔ 우리 DEM + MPM = 상향식 | §4-1–4-5 L237–257 · §4-8 L267 | [인쇄] · 카드 서술 | 구조를 만드는 단계의 계산 없음
- [h] nakamura2020_dry_coating_ncm_li3ps4_core_shell | DEM 아님 — 360 MPa 반쪽셀 (50 회 뒤) → FIB-SEM 100 장 → 네 상 분할 → 복셀 Poisson (σ_eff/σ_B · τ) | §3-6 L124–125 · §4-1 L192 | [인쇄] | —
- [h] 그 밖의 카드 | 이 배치에 없음 | — | — | —

## i. 복합 양극 (AM + SE) 의 압력별 기공

AM + SE 복합의 **압력별** 기공 곡선 = **0**. **한 압력 한 점씩** 이 두 카드에 있다 (360 MPa · 370 MPa).

- [i] nakamura2020_dry_coating_ncm_li3ps4_core_shell | NCM111 : Li₃PS₄ = 86.9 : 13.1 wt% (도전재 · 바인더 없음) · 일축 360 MPa. FIB-SEM 부피분율 — 코팅: NCM 63.02 · LPS 20.44 · NCM 사이 공극 12.19 · NCM 안 공극 4.35 % / 막자 혼합: 62.42 · 21.65 · 12.01 · 3.91 % → 총 공극 16.5 / 15.9 % · SE ÷ 고체 24.5 / 25.8 vol% · 본문의 복합 밀도 3387 kg/m³ | §3-6 L126–136 · Table 1a · p.7–8 | [인쇄] · [우리 산술] (총 공극 · SE 몫) · [미확인] (밀도 산출 근거) | 한 압력 · 50 회 사이클 · 완전 방전 뒤 분해한 시료 (뺀 뒤 · 사이클 영향 포함 가능) · 20 µm 정육면체 1 개 · 회색조 분할 (오차 미확인) · Li₃PS₄ 유리 · NCM111 단봉 4.7 µm
- [i] lee2026_unveiling_ptfe_dry_electrode_digital_twin | NCM (Ni 0.7 · D50 7 µm) : LPSCl (D50 1 µm) : VGCF = 85 : 13 : 2 wt% (+ PTFE) · 370 MPa 5 min. 기공 — 밀도 기반 15.4 % (PTFE 0) · 12.6 % (0.2 wt%) ↔ FIB-SEM 재구성 12.9 · 11.9 % · SE ÷ 고체 25.7–27.0 vol% | §3-2 L78–84 · Table S1 · SI p.17 | [인쇄] · [우리 산술] (SE 몫 · 차) | 한 압력 · LPSCl 1.86 g/cm³ 로 계산 (랩 표준과 다른 문헌 값) · 재구성 1 개씩 · PTFE 는 분할 안 됨 · 누른 채인지 뺀 뒤인지는 "가압 뒤" 로만 (L87)
- [i] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 같은 조성 · PTFE 함량별 상대밀도 84.6 / 87.4 / 86.8 / 82.5 % (0 / 0.2 / 0.5 / 1.0 wt%) → 기공 15.4 / 12.6 / 13.2 / 17.5 % (내 검산: 100 − 상대밀도 · 앞 두 값은 Table S1 과 같음) | §3-7 L163–166 · Table S2 | [인쇄] · 내 검산 | 측정 압력 · 시료 수 [미확인] · 1.86 기준
- [i] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 후막 (PTFE 0.2 wt%): 25 / 35 / 45 mg/cm² → 두께 78 / 109 / 139 µm → 겉보기 밀도 3.21 / 3.21 / 3.24 g/cm³ · 상대밀도 0.87 / 0.87 / 0.88 | §3-11 L205–209 · p.11 · Fig 6a–c | [인쇄] (로딩 · 두께) · [우리 산술] (밀도) | 두께를 잰 상태 (누른 채 / 뺀 뒤) 는 카드에 없음 · 로딩이 달라도 밀도가 거의 같다는 한 줄
- [i] matthews2024_ptfe_nanofibril_network | porosity · 밀도 · tortuosity 가 한 번도 나오지 않음 (LIB 건식 전극 100–110 µm · 30–32 mg/cm²) | §8 L462 · §3.3 L156 | n/a | SE 없는 액체계
- [i] landesfeind2018 · malifarge2017 · morasch2018 | (ASSB 아님) 액체 LIB 전극의 다공도만: Custom Cells 전극 40–51 % (landesfeind2018 Table II) · 판상 흑연 ≈ 10–44 % (malifarge2017 · 판독) · 미압축 흑연 ~55 % (morasch2018) — 누른 압력 값은 세 카드 모두 없음 | landesfeind2018 L72–74 · malifarge2017 L126 · morasch2018 L68 | stated · 판독 | SE 없음 — 수치 전이 불가
- [i] nguyen2020 | 해당 없음 (합성 구조) | — | — | —

## j. 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 논문이 안 한 것: 압력 · 조성 · 시간 축 (360 MPa · 30 °C 한 점) · 반복 · 오차 · RVE 수렴 · 사이클 전 시료의 3D · DC 셀 시료의 3D | §0 L36 · §6 L228 · §10-7–8 L320–321 | [미확인] · 카드 서술 | —
- [j] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 저자 자신의 미검증: σ_e 가 DC 에서 크게 떨어진 이유 (두꺼운 층에 압축 응력이 덜 전달) 는 "speculated" · 코어–쉘이 이후 슬러리 전단에서도 유지될 것이라는 함의도 시험 안 함 | §3-7 L169 · §3-3 L86 · §10-11 L324 | [인쇄] | —
- [j] nakamura2020_dry_coating_ncm_li3ps4_core_shell | 카드가 적은 우리 쪽 한계: DEM = 강체 구 + 겹침 · AM 파괴는 접촉 단위 판정뿐 조각을 만들지 않음 · MPM = 압축 중 SE 소성 흐름 (혼합 · 코팅 단계 없음) → 이 논문의 두 기전 (SE 망의 연속성 · NCM 파쇄 억제) 가운데 그릴 수 있는 것은 앞쪽뿐. 우리 "코팅" 팔은 표면 성질만 바꿈 (껍질 · 파쇄 완충 · 전자 차폐 없음) | §4-2 L197 · §7-1 L240 · L249 · §8-3 L288–291 | 카드 서술 · [추정] | 논문 문장 아님
- [j] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 논문에 없는 것: 공정 → 구조 예측 (혼합 · 압축 모델) · 응력 · 변형장 · 두꺼운 전극의 해상 시뮬 (25 µm 만 — "these behaviors will be exacerbated as electrode loading increases") · 반복 통계 · PTFE 상 | §7-4 L373 · §3-10 L201 · §6 L320 | 카드 서술 · [인쇄] (인용문) | —
- [j] lee2026_unveiling_ptfe_dry_electrode_digital_twin | 카드가 적은 우리 쪽 한계: 코팅은 혼합 단계의 전단에서 생기는데 DEM (겹침 δ 가 대리) · MPM (압축 중 공극 채움 흐름) 둘 다 혼합 전단 소성이 없음 → 코팅 상태는 결과가 아니라 입력 | §4-7 L263–264 · §7-1 L331 · §7-2 L354 | 카드 서술 | 논문 문장 아님
- [j] matthews2024_ptfe_nanofibril_network | 압축과 닿는 미해결: 압축 중 PTFE 피브릴이 끊어지는지 문헌이 갈림 (본편의 "without breakage" 는 관찰 기반 주장) · 캘린더 라인압 50 N/mm 는 접촉폭 미기재라 MPa 로 못 바꿈 → 성형 300 MPa 와 직접 비교 불가 | §5.4 L311–318 · §12-6 L662–663 · §12-9 L667 · §10.0 L503 | stated (문헌 대비) · 카드 서술 | LIB
- [j] matthews2024_ptfe_nanofibril_network | 카드가 적은 우리 쪽 한계: 피브릴화 (결정자가 풀려나옴) 는 우리에게 없는 기전 — 씨앗을 사후에 뿌림 · primary 피브릴 (길이 수백 µm) 은 우리 RVE (50 µm) 에 한 가닥도 온전히 안 들어감 | §1 L76 · §6 L371 · §10.1 L553–557 | 카드 서술 · 🧮 DERIVED | —
- [j] morasch2018_binder_gradient_impedance_tortuosity | 저자 문장: 바인더 구배와 이온 저항 구배의 정량 연결은 "not yet possible" · 바인더의 면내 분포는 "Entirely unclear" · 구배가 있으면 임피던스 τ 는 겉보기 값 — "the tortuosities extracted from impedance analysis are apparent tortuosties which obviously cannot be directly applied to a macro-homogeneous battery model" | §4-9 L168–169 · §8-4 L292 · §10 L346 · A3466 | stated (인용문) | 가압 계산 없음 (미압축 전극) — "두께 방향으로 고르지 않은 구조는 수송 값 하나로 대표되지 않는다" 는 점에서 닿음
- [j] morasch2018 · nguyen2020 | 카드가 적은 우리 쪽 한계: 우리 두 수송 솔버 (접촉망 · 복셀) 는 관통 (투과) 형이라 방향을 못 봄 → 판 · 벽 근처 충전 층 · 플래튼 근처 밀도 구배 · 설계 구배를 그 값으로 순위 매길 수 없음 | morasch2018 §7 L214–216 · §8-8 L331 / nguyen2020 §5 L117 · L177 · §8 L205 | 카드 서술 (원문 근거 = Morasch A3463 · Nguyen Fig 6) | 눌린 구조를 평가하는 쪽의 한계
- [j] nguyen2020_electrode_tortuosity_factor | 저자: τ_e 를 P2D 에 쓰라는 권고는 실제 전극 · 성능 자료로 입증되지 않음 ("follow-up study" 로 미룸 · p8) · TLM 과의 일치도를 수치화하는 지표는 제안만. 카드: 입자 물리 0 (접촉 법칙 · 압밀 · 소성 · 형상 변화 없음) | §10 L215 · §6 L126 · §4-D L107 | stated · 카드 서술 | —
- [j] malifarge2017_tortuosity_symmetric_cell_impedance_tlm | 저자가 적은 후속 계획 (다른 입자 형상 · 양극 재료로 확장 · Wheeler 법과 비교) 은 이 논문에서 수행되지 않음 · 균질 1D 모형은 dead-end 기공 · 방향성 · 두께 방향 구배를 못 봄. 카드: 압연으로 정렬이 만들어지는 과정 (기계 쪽) 은 이 논문에도 없고 우리 DEM (강체 구) 도 줄 수 없음 | §10 L395 · L397 · §7 L318 | stated · 카드 서술 | LIB
- [j] landesfeind2018_tortuosity_impedance_vs_tomography | 카드: "압밀 · 형상 · 기계 물리 없음" (수송 절반만) · 실제 전극 (dead-end · 구배 · 바인더 덩어리) 에서 차단 대칭셀 τ 가 관통형 τ 와 같다는 검증은 아님 (강구 한 기하뿐) | §7 L244 · §10 L365 | 카드 서술 | —

## k. DEM 의 한계 (논문이 직접 말한 문장 · 수치)

**DEM 을 쓴 논문이 이 배치에 없다** → "DEM 을 쓰면서 한계를 말한 문장" 은 0 건이고 일곱 장 모두 "말 없음" 이다. 아래는 (3) 실험이 보인 "단단한 구 · 점접촉 가정 밖의 것" 과 (4) 카드의 풀이다 — 인용할 때 "DEM 논문의 고백" 으로 쓰지 않는다.

- [k] nakamura2020_dry_coating_ncm_li3ps4_core_shell — Nakamura, Kawaguchi, Masuyama, Sakuda, Saito, Kuratani, Ohsaki, Watano, J. Power Sources 448 (2020) 227579 | DEM 을 쓰지 않음 — 말 없음. (3) 실험: 무른 SE 입자가 모양을 바꿔 합쳐짐 — 30 s 에는 낱알로 붙고 (불연속) · 120 s 에 합체 시작 · 300 s 에 0.1–0.2 µm 연속 껍질 (13,000 rpm). 원문: "a significant difference between the mechanical properties of the active material and solid electrolyte particle is a key property for successful dry coating" | §3-2 L77–78 · §3-3 L83 · p.5–6 · Fig 4 · 5 | [인쇄] (인용문) | 코팅 장치 안의 충격이지 일축 압밀이 아님 · Li₃PS₄ 유리
- [k] nakamura2020_dry_coating_ncm_li3ps4_core_shell — 같은 서지 | (3) 실험: 누르면 단단한 입자가 깨짐 — 막자 혼합은 360 MPa 에서 NCM 이 1차 입자 사이로 깨져 총 표면이 1.26 → 1.51 µm²/µm³ · 껍질이 있으면 안 깨짐: "the compressive stress acting on the NCM particles was damped by the soft and ductile LPS shell layer" · 껍질은 눌리면서 밀려남: "the continuous shell layer of LPS was partially pushed away when the cathode powder bed was compressed" · 저자의 수송 해석: "These differences in the ion conductivity and tortuosity were thought to be due to the breakage or non-breakage of the NCM particles" | §3-6 L141–146 · L159–160 · p.7–8 · Table 1b · Fig 7 | [인쇄] (인용문 · 면적) | 사이클 뒤 시료 · 한 압력. (4) 카드의 풀이: "DEM = 강체 구 + 겹침 · AM 파괴는 접촉 단위 판정뿐 조각을 만들지 않는다" (L197) — 논문 문장 아님
- [k] lee2026_unveiling_ptfe_dry_electrode_digital_twin — Lee, Hong, Shin, Kim, Lim, Jung, McDowell, Jung, Lee, Small 2026, e75974 (DOI 10.1002/smll.75974) | DEM 을 쓰지 않음 — 말 없음. (3) 실험: LPSCl 입자가 혼합 전단에서 부서지고 문질러져 NCM 위에 100–500 nm 막이 됨 (혼합 2 → 10 → 20 min 시간 열 · Fig S7). 원문: "PTFE fibrils confined the LPSCl particles near the NCM through entanglement, preventing them from escaping the NCM surface and subjecting them to continuous shear deformation" | §3-3 L97 · L102 · p.3–4 · Fig 1 · S3 · S7 | [인쇄] (인용문 · 두께) | 압축이 아니라 100 °C 손 혼합 단계 · Fig 1c = Fig S7a 같은 사진 (L430). (4) 카드의 풀이: "우리 DEM 의 강체 구 + 접촉 소성 (겹침 δ 대리) 으로는 코팅을 만들 수 없다" (L264) · "강체 구 하한 ≈ 20 % (소성 없이는 못 내려감)" (L332 — 출처 서지가 카드의 이 줄에 없음) — 논문 문장 아님
- [k] malifarge2017_tortuosity_symmetric_cell_impedance_tlm — Malifarge, Delobel, Delacourt, J. Electrochem. Soc. 164 (11) E3329–E3334 (2017) | DEM 을 쓰지 않음 — 말 없음. (3) 실험: 판상 흑연은 기공 tortuosity 가 구형 입자 Bruggeman 의 2.3–3.7 배 — "It appears like a translated Bruggeman relation which would account for a peculiar electrode microstructure resulting from the anisotropic shape of graphite particles" · 평행 정렬 입자 30–60 % (압연압 의존) | §0 L42–43 · §8-1 L342–343 · E3332 · 그림 6 | stated (인용문) · 카드 산술 (배수) | 액체 LIB. (4) 카드의 풀이: "우리 DEM 은 판상 정렬 이방성을 표현할 수 없다" (L312) — 논문 문장 아님
- [k] landesfeind2018_tortuosity_impedance_vs_tomography — Landesfeind, Ebner, Eldiven, Wood, Gasteiger, J. Electrochem. Soc. 165 (3) A469–A476 (2018) | DEM 을 쓰지 않음 — 말 없음. (3) 실험: 입자만 본 구조 (단층촬영 325 nm) 의 τ 는 EIS 의 1/1.5–1/2.3 (tortuosity factor 척도) — 저자가 지목한 원인 = 안 보이는 바인더 · 탄소 ("the most likely cause") · 같은 다공도에서 바인더 1.5 → 10 wt% 만으로 τ 2.7 → 5.0 · 구형 NMC 3.6 ± 0.3 ↔ 판상 흑연 5.1 ± 0.8 | §3 L65–66 · L72–76 · §8-2 L304–305 · A472 · A474–A475 | stated · 파생 (비) | 액체 LIB — 단층촬영 재구성에 대한 문장 (DEM 아님). (4) 카드의 풀이: "형상 · 이방성 효과는 우리 tau2 에 없다" (L240) · "DEM 접촉망엔 CBD 없음" (L237)
- [k] matthews2024_ptfe_nanofibril_network — Matthews, Wheeler, Ramírez-González, Grant, Front. Energy Res. 11, 1336344 (2024) | DEM 을 쓰지 않음 — 말 없음 (시뮬레이션 0). (3) 실험: 100–200 µm PTFE 분말이 압축 + 전단으로 풀려 "primary fibrils of a few µm in diameter and 100's µm in length that branched into secondary and then ever finer fibrils, down to diameters of 10s nm or below" — 입자가 실로 바뀌는 상 | 한 문장 결론 L9–13 · §4.4 L228 · 초록 | stated (인용문) | LIB · 분포 · n 없음. (4) 카드의 풀이: 우리는 피브릴화를 모사하지 않고 결과만 씨앗으로 뿌린다 (L371)
- [k] morasch2018_binder_gradient_impedance_tortuosity — Morasch, Landesfeind, Suthar, Gasteiger, J. Electrochem. Soc. 165 (14) A3459–A3467 (2018) | DEM 을 쓰지 않음 — 말 없음 (모형 안에 입자가 없음 · 바인더는 저항 프로파일로만) | §4-9 L167–168 | 카드 서술 | —
- [k] nguyen2020_electrode_tortuosity_factor — Nguyen, Demortière, Fleutot, Delobel, Delacourt, Cooper, npj Comput. Mater. 6:123 (2020) | DEM 을 쓰지 않음 — 말 없음. 입자는 기하로 생성한 강체 구 (GeoDict GrainGeo) — 접촉 법칙 · 압밀 · 소성 · 형상 변화 없음 · 점접촉 협착 개념도 없음 | §4-D L106–107 | 카드 서술 | 한계를 말한 문장이 아니라 계산 설정

## l. 소성변형이 왜 어려운가 (논문의 설명 · 택한 우회 · 그 값)

**입자 계산에 소성을 넣은 논문이 이 배치에 없다.** "왜 어려운가" 를 설명한 문장도 없다 (일곱 장 모두 "말 없음"). 아래는 닿는 주변 근거다 — 두 ASSB 논문은 변형을 계산하지 않고 눌린 구조를 재서 쓰는 길을 택했다.

- [l] nakamura2020_dry_coating_ncm_li3ps4_core_shell — Nakamura et al., J. Power Sources 448 (2020) 227579 | 말 없음 (입자 · 압축 계산 없음). 택한 우회 = 눌린 구조를 재서 계산: 360 MPa 반쪽셀 → FIB-SEM 100 장 → 네 상 분할 → 복셀 Poisson. 맞춘 값 0 · 검증 = DC 분극과의 비 (σ_ion +48 % 복셀 ↔ +58 % DC — 절대값은 복셀이 측정의 1/1.55–1/1.65) · 비용 = 20 µm 정육면체 1 개씩 (반복 없음) | §3-6 L124–125 · §3-7 L166–170 · §6 L228 | [인쇄] · [우리 산술] (절대값 비) | 압밀을 계산하지 않고 건너뛴 것이지 소성 계산의 우회가 아님
- [l] nakamura2020_dry_coating_ncm_li3ps4_core_shell — 같은 서지 | 실험이 준 소성의 성격 (모델이 담아야 할 것): SE 는 충격 에너지가 쌓이면서 낱알 → 합체 → 연속 막으로 모양이 바뀌고 (30 · 120 · 300 s) · 압축에서는 껍질이 응력을 완충하면서 일부 밀려남 — 하중 이력에 따라 SE 의 자리 자체가 바뀜 | §3-2 L77–78 · §3-6 L146 · L160 · p.6–8 | [인쇄] | 정성 · 한 조건
- [l] lee2026_unveiling_ptfe_dry_electrode_digital_twin — Lee et al., Small 2026, e75974 | 말 없음 (공정 · 압축 모델 없음). 택한 우회 = 측정 재구성 (FIB-SEM 25 µm 정육면체 1 개씩 · U-Net 분할) 위 복셀 FVM. 맞춘 값 0 (고유 전도도 셋은 입력 — 출처 미기재) · 검증 = 부피분율 ↔ 밀도 기반 (기공 차 −2.5 · −0.7 %p) + 전도도의 시뮬 ÷ 실측 (σ_e 0.97–0.99 · σ_ion 1.42–1.46) | §4-2 L242–243 · §4-4 L252–254 · §3-12 L226–228 | [인쇄] · [우리 산술] | 압밀을 계산하지 않음. 카드: SE 의 형상 소성 · 파쇄는 혼합 단계의 전단에서 일어나고 "우리 둘 다 혼합 전단 소성은 없다" (L331)
- [l] matthews2024_ptfe_nanofibril_network — Matthews et al., Front. Energy Res. 11, 1336344 (2024) | 말 없음 (모델링 · 시뮬레이션 0). 형성 기전은 다수 관찰에 기반한 정성 모델 + 문헌 (Ariawan 2002 · Ardakani 2013 — 압축과 전단의 조합이 필요) | §4.3 L217–220 · §7 L397 | stated | LIB · PTFE
- [l] nguyen2020_electrode_tortuosity_factor — Nguyen et al., npj Comput. Mater. 6:123 (2020) | 말 없음. 입자 물리를 건너뛴 설정: 구를 기하로 채움 (압밀 없음) → 복셀 위에서 Laplace · 임피던스만 | §4-D L106–107 | 카드 서술 | —
- [l] landesfeind2018 · malifarge2017 · morasch2018 | 말 없음 (입자 계산 없음 — 회로 · 연속체 모형과 실험) | — | — | —

## m. 받아들일 통찰 (무엇을 · 우리 쪽 어디에 · 왜)

**nakamura2020_dry_coating_ncm_li3ps4_core_shell**

- [m] nakamura2020 | (관측량 정의) 눌린 복합의 공극을 "입자 사이 공극" 과 "AM 입자 안 공극" 으로 나눠 센다 — 360 MPa 에서 12.0–12.2 % + 3.9–4.4 % (입자 안 공극이 총 공극의 약 1/4 · 내 검산) | 단계 0 (기공률 연산자가 입자 안 공극을 넣는지 빼는지를 결과 전에 적는다) · 단계 5 의 결과 전 대조 항목 | Table 1a (p.8 · [인쇄]) · L126–136 — 정의에 따라 약 4 %p 가 갈린다
- [m] nakamura2020 | (관측량 정의 · AM 파괴) AM 이 깨졌는지를 재구성의 "AM 총 표면적 (µm²/µm³-전극)" 으로 잰다 — 혼합 1.51 ↔ 코팅 1.26 · 함께 "AM 표면 중 공극과 닿은 몫" (36.7 ↔ 16.4 %) | 조건 R7 의 결과 전 대조 항목 (비코팅 혼합은 360 MPa 에서 2차 입자가 깨지고 SE 껍질이 있으면 안 깨진다 — 방향만) · 단계 7 의 피복 정의 (AM–AM 면은 분모 밖) | Table 1b · Fig 7a · p.7–8 · L141–147 · L31
- [m] nakamura2020 | (함정) 같은 성형압이라도 시료 두께 · 시료 상태가 다르면 같은 구조가 아니다 — 층이 ≈ 8 배 두꺼운 DC 펠릿에서 σ_e 변화가 −94 % 인데 얇은 반쪽셀의 이미지는 −11 % (저자 "speculated": 응력이 덜 전달) · FIB-SEM 은 50 회 뒤 시료 · DC 는 새 펠릿 | 단계 5 · 6 의 실험 대조 (견줄 실험 값마다 펠릿 질량 · 두께 ÷ 지름 · 사이클 여부를 같이 적는다) · 흐름 밖: 대칭셀 계획 | p.8–9 · Table 2 · L98 · L167–169 · L320
- [m] nakamura2020 | (실험 설계) "같은 총 SE" 비교는 코팅 뒤의 순 조성을 재서 (UV-vis · 투입 15.0 → 13.1 wt% 로 벽 부착 손실) 대조 혼합을 그 값에 맞추고 · 자유 SE 미분 (< 3 µm) 이 남았는지 입도로 확인 · 차단 셀 이름 (이온 차단 → σ_e · 전자 차단 → σ_ion) 을 결과 전에 고정 | 흐름 밖: 코팅 활물질 믹싱 실험 설계 | p.4–6 · Fig 4d · L76 · L84 · §7-4 L264–267 · §10-1 L314

**lee2026_unveiling_ptfe_dry_electrode_digital_twin**

- [m] lee2026 | (검증 시험) 기공을 두 연산자로 나란히 낸다 — 밀도 기반 (질량 · 두께 · 상 밀도) ↔ 분할 재구성. 이 논문의 차 = −2.5 %p (PTFE 0) · −0.7 %p (0.2 wt%) — 재구성이 기공을 적게 · SE 를 많이 잡고, 두 전극의 편향이 서로 다르다 | 단계 0 (연산자 사이 차를 판정 기준의 허용폭으로 미리 적는다) · 단계 5 의 결과 전 대조 항목 | Table S1 · L78–84 · §10-2 L431
- [m] lee2026 | (출발 상태) SE 코팅은 누를 때가 아니라 혼합 단계의 가둠 + 전단에서 생긴다 (2 → 10 → 20 min 시간 열) → 압축 계산의 출발 상태에 코팅을 입력으로 넣고 결과로 기대하지 않는다. PTFE 를 쓰는 건식 공정의 "비코팅" 대조군은 이미 부분 코팅일 수 있다 | 조건 R6 · 단계 5 의 출발 상태 정의 · 흐름 밖: 믹싱 실험 설계 (PTFE 함량 고정 + PTFE 없는 분말 대조 두 축) | Fig S7 · p.4 · L102 · L264 · §8-1 L383–384 ([추정] 포함)
- [m] lee2026 | (규칙 · 함정) 균질도 (칸 분산) 는 무작위 혼합 기준 · 완전 분리 기준 · 칸 크기 사다리와 함께 내고 칸 평균 = 전체 분율인지 검산한다 — 이 논문은 칸 2.5 µm < 입자 7 µm 이고 칸 평균 (VGCF 5.1 · 5.2 vol%) 이 전체 (3.5 · 3.3 vol%) 와 다르다. "전류가 거의 없는 SE" 문턱도 절대값이 아니라 평균 대비 비율로 (같은 절대 문턱이 평균의 0.13 → 0.09 배) | 흐름 밖: 믹싱 지표 · 단계 7 의 구조 지표 | L122–123 · L156 · §8-2 L387–389 · §10-3–5 L432–434
- [m] lee2026 | (기준 상태) 복셀 수송 ↔ 실측을 견주려면 같은 성형 · 측정 조건의 순수 LPSCl 펠릿 전도도가 있어야 한다 — 이 논문은 없어서 시뮬 ÷ 실측 1.42–1.46 이 출처 없는 입력 1.0 mS/cm 에 걸린다 (1.5 면 2.1–2.2 · 3.0 이면 4.3–4.4 배). 측정 중 적층압 · 반복 수 · 적합 회로 · 가압 중 / 놓은 뒤 두께를 기록 항목으로 | 단계 7 · 흐름 밖: 대칭셀 계획 | §0 L30 · §3-12 L226–227 · §8-4 L399–400 · §8-8 L420

**landesfeind2018_tortuosity_impedance_vs_tomography**

- [m] landesfeind2018 | (검증 순서) 실제 전극을 해석하기 전에 답을 아는 기준 기하로 측정 · 계산 사슬을 통과시킨다 — 1 mm 강구 충전 (ε 38–39 %) 에서 τ 1.56 ↔ Bruggeman 1.60–1.62. 단 Bruggeman 은 기공이 전도상일 때의 기준이라 입자가 전도상인 망의 기준값은 아니다 | 단계 7 (수송 솔버 검증 순서) · U0 류 단위 시험 | A472–A474 · Table I · L67–69 · L185 · L236
- [m] landesfeind2018 | (검증 시험) 입력 불변 검사 — 같은 전극에서 전해질 전도도를 바꿔도 R_Ion·κ 가 같으면 전자 저항이 무시된다는 증명 ("…is thus a proof that electronic resistance contributions are negligible"). 정확한 창 = R_El/R_Ion < 10⁻² · 10⁻²–10⁻¹ 이면 오차 최대 ~20 %. 계산 쪽 짝 = 고유 전도도 두 값으로 풀어 수송 tortuosity 가 같은지 | 단계 7 의 자기검사 · 흐름 밖: 결과 전 대조 항목으로 쓸 EIS 값의 선별 | Fig 1–3 · A470–A472 · L61 · L124 · §8-8 L351
- [m] landesfeind2018 | (함정) 구조에서 막는 상 (바인더 · 탄소) 을 빼고 계산하면 수송 tortuosity 가 낮게 나온다 — 같은 코팅에서 EIS ÷ 단층촬영 = 1.75 · 2.31 · 1.51 · 같은 다공도에서 바인더 1.5 → 10 wt% 로 τ 2.7 → 5.0 | 단계 7 (첨가제 없는 구조의 값을 바인더 · 탄소가 든 실험 전극과 견줄 때 결손 방향을 먼저 적는다) | Table II · Fig 6 · A474–A475 · L72–76
- [m] landesfeind2018 | (보고 방식) 배수를 옮길 때 척도 (tortuosity factor ↔ 제곱근) 와 저항의 전극 수 규약 (전극 하나 ↔ 대칭셀 합) 을 같이 적는다 — 이 논문 안에서도 강구 790 Ω 은 두 전극 합 · 바인더 실험 145 / 213 Ω 은 전극 하나 값이다 | 흐름 밖: 문헌 EIS 값 재사용 · 보고 표기 | §4-1 L97–99 · §8-3 L315–317 · §8-8 L355–356 (파생)

**malifarge2017_tortuosity_symmetric_cell_impedance_tlm**

- [m] malifarge2017 | (함정) 두 레일 전송선 해 (Eq 11) 는 전자 레일 저항과 이온 레일 저항을 맞바꿔도 같다 → 차단 대칭셀 스펙트럼 하나로는 어느 쪽이 이온인지 못 가른다 → 이온 차단 셀로 전자 전도도를 먼저 재서 고정한다 (원문은 문헌값으로 고정) | 흐름 밖: 대칭셀 EIS 계획 (탄소 없는 · 저 σ_e 조성) · 단계 7 의 실험 대조 | §4-4 L193 (우리 유도 · 수치 확인) · §8-1 L359 · L365
- [m] malifarge2017 | (선별 기준) 전자 레일을 무시한 그래프법은 이온 저항을 [(1+β) − 3β/(1+β)] 배로 읽는다 (β = R_e/R_i · 0.1 → 0.827 · 0.3 → 0.608 · 2 에서 부호가 뒤집힘). Minnmann 의 값으로는 질량비 70 : 30 에서 × 0.61 · 80 : 20 이상에서만 6 % 안 | 결과 전 대조 항목으로 쓸 EIS 값의 선별 (단계 7) | §4-4 L194–202 · §8-1 L356–357 · §8-2 L372 (우리 유도 · 카드 산술 — 원문 식 아님 · 그래프법 기준)
- [m] malifarge2017 | (규칙) 수송 tortuosity 는 상 분율 입력에 정비례한다 — 저항이 정해지면 Δτ/τ = Δε/ε (기공률 < 15 % 에서 1 % 차 → 0.75). 설계 평균 분율을 쓰면 시료별 오차가 그대로 들어간다 | 단계 0 (φ 를 세는 법을 결과 전에 고정) · 단계 7 | E3332 (stated) · L44 · L113 · L138 · L338
- [m] malifarge2017 | (검증 시험) 이산 사다리 (행렬 풀이) ↔ 해석식 ↔ 극한 (고주파 = 두 레일 병렬 · 저주파 실수부 = (R_e + R_i)/3) 을 서로 대조 — 사다리는 O(1/n) 로 수렴 (n ≥ 100 이면 < 1 %) | 흐름 밖: 망 · 임피던스 솔버의 단위 시험 | §4-3 L184 · §4-4 L190–191 · 원문 대조 기록 L454–456 (우리 재계산)

**matthews2024_ptfe_nanofibril_network**

- [m] matthews2024 | (측정법) 사진 속 치수를 아는 물체를 자로 쓴다 — 같은 프레임의 CNF (명시 Ø 150–200 nm) 대비 굵기비 3–5 배 → PTFE 피브릴 Ø ≈ 30–70 nm. 절대 픽셀 측정보다 인쇄 해상도 한계에 강하다 | 흐름 밖: SEM 단면 대조 · 그림 판독 규칙 | Fig 6A · §4.5 L253–258 (🧮 DERIVED)
- [m] matthews2024 | (함정) 두 자릿수에 걸친 계층 (수십 nm – 수 µm) 을 한 굵기로 접어 격자에 찍으면 표현 부피 오차의 부호가 굵기에 따라 뒤집힌다 (30 nm 를 1 셀 폭으로 찍으면 32–45 배 과대 · 0.25 µm 는 0.46 배) · 긴 가닥 (수백 µm) 은 50 µm 상자에 온전히 안 들어간다 | 단계 7 (첨가제의 격자 표현 — 부피를 고정하고 절대 표현 부피를 근거로 삼지 않는다) | §10.1 L553–564 · §10.2 L577–583 (카드의 🧮 DERIVED — 논문 값 아님)
- [m] matthews2024 | (시료 설계) 미세구조 관찰용 시료에서 헷갈릴 상 (CNF) 을 일부러 뺀다 → 사진의 실이 전부 PTFE 임이 보장된다 | 흐름 밖: SEM 대조 실험 설계 | §3.2 L145–148
- [m] matthews2024 | (보고 방식) 배수 헤드라인은 분모의 절대값과 같이 적는다 (2C "+146 %" 는 두 전극 모두 크게 무너진 자리 · ≤ 1C 이득은 +4.5 ~ +27 %) · 면적이 안 적힌 EIS 저항은 Ω·cm² 로 바꾸지 않고 · 라인압 (N/mm) 은 MPa 로 바꾸지 않는다 | 흐름 밖: 보고 방식 · 실험 값 옮길 때의 단위 규칙 | §5.2 L286–296 · §5.5 L362–363 · §12-8–9 L665–667

**morasch2018_binder_gradient_impedance_tortuosity**

- [m] morasch2018 | (경계조건) 차단 EIS (반사 경계) 의 겉보기 값은 분리막 쪽을 무겁게 센다 — 균질 전극에서도 겉보기 저항의 57.8 % 가 분리막 쪽 1/4 두께에서 오고, 같은 총저항이라도 ±25 % (선형) · −46 / +66 % (계단) 갈린다. 관통형 계산은 뒤집어도 같은 값이다 → 눌린 구조가 판 쪽과 바닥 쪽이 다르면 두께 방향 단면 저항 프로파일을 같이 낸다 | 단계 7 (수송 값에 경계 종류와 어느 면이 분리막인지를 같이 적는다) · 단계 5 결과의 두께 방향 불균일 평가 | A3462–A3463 (stated) · §4-1 L93–96 · §4-4 L128 (우리 유도 · 파생) · §7 L214–216
- [m] morasch2018 | (실험 설계) 자립 전극은 뒤집어서 한 번 더 잰다 — 선형 구배면 정 · 역 두 값의 평균이 관통형 값과 같고 일반 분포면 [평균/1.5, 평균/0.75] 안. 실험 예: 같은 125 °C 전극이 5.73 ↔ 2.70 (2.12 배) | 흐름 밖: 대칭셀 계획 (건식 PTFE 전극은 자립 막) | A3465 · 그림 6d (판독 · TREND 전용) · §4-4 L130 · §8-4 L293 · §8-8 L333 (파생)
- [m] morasch2018 | (진단 · 함정) 두께 방향 구배는 직렬 저항을 뺀 위상 그림의 저주파 극소로 본다 (균질 기준 ~43.4°) · 극소보다 높은 주파수의 위상은 직렬 저항 ±1–2 % 오차로 못 쓴다 · 저주파 외삽 절편은 맞춤 창에 ±10 % 안팎 민감하니 창을 기록한다 | 흐름 밖: EIS 측정 · 해석 규칙 | A3462–A3465 · 그림 6c · L74 · §4-6 L147 (창 민감도는 파생)
- [m] morasch2018 | (보고 방식) 겉보기 τ 가 같아도 (4.4–4.6) 구배가 다르면 충전 율속이 크게 다르다 → 수송 값 하나로 전극을 대표시키지 않는다. "Any calculated tortuosity is a mere apparent tortuosity and is, in the case of strong binder gradients, not representative for the entire electrode." | 단계 7 의 보고 방식 | 그림 7 · A3465–A3466 · L75 · L292

**nguyen2020_electrode_tortuosity_factor**

- [m] nguyen2020 | (단위 시험) 가장 단순한 구조로 구현을 교차검증한다 — 곧은 관통 기공에서 두 방법 모두 τ = 1 · 곧은 막힌 기공은 관통형 ∞ ↔ 전극 τ_e ≈ 0.81 | U0 류 (단계 7 수송 솔버의 해석해 시험) | Fig 3 · p4 · L31–32 · L131
- [m] nguyen2020 | (장부 함정) 막힌 부피는 흐름에는 0 · 상 분율에는 + 로 들어가 τ 를 키운다 — 수송량 N_M 6.49 가 같은데 τ 2.25 → 1.47 (ε 34.7 → 22.6 %). "even though the dead-end pores do not contribute to species transport at steady-state, their presence does have an effect on the determination of tortuosity, via their additional volume fraction" → f (= σ_eff/σ₀ = 1/N_M) 를 1차 수송량으로 보고 | 단계 0 (상 분율 장부) · 단계 7 의 보고 | Fig 2 · p3–5 · L50–52 · L176
- [m] nguyen2020 | (대표 부피 진단) 모사 임피던스가 전송선의 45° 에서 벗어나면 계산 부피가 대표성이 없거나 균질화가 안 되는 구조다 — 한 변이 입경의 2.5 배뿐인 구 충전이 그 예 · 잘 퍼콜된 3D 구 충전 (막힌 기공 4–8 %) 에서는 두 정의 차가 ≤ 4 % | 단계 7 (대표 부피 충분성의 진단) | p6 · p8 · L43 · L126 · L134 · 내 검산 (2.5 배)
- [m] nguyen2020 | (방향 · 차원 경고) 관통형 τ 는 층 순서를 못 본다 — 같은 2 층 구조가 τ 7.4 하나인데 전극 τ_e 는 4.0 ↔ 11.9. 그리고 2D 손그림 사례의 크기를 3D 기대치로 쓰지 않는다 (3D 근거는 세 구조뿐) · 막힌 기공 판정 문턱 (최대 flux 의 2 % · 코드는 0.5 %) 은 자의적이라 기록한다 | 단계 7 · 단계 3 의 2D 결과를 3D 로 옮길 때의 한정어 | Fig 6 · p7 · L39–42 · L123 · L198 · L217

## 카드 문제

**철회된 출처 (Minnmann 의 순수 SE 10 % @ 300 MPa) 를 실험 근거로 적은 서술** — **0 건** (일곱 장 전수 검색 · Minnmann 은 전도도 · TLM 맥락으로만 나옴).

**우리 쪽 값 · 서술이 카드 안 (또는 배치 안 카드끼리) 에서 어긋남**
1. matthews2024 — 우리 VGCF 함량이 한 카드 안에서 둘: 비교표 L501 "VGCF 3 wt%" ↔ L539 "생산 레시피 AM:SE:VGCF:PTFE = 80:18:1:1" (VGCF 1 wt%). 같은 표 L500 은 PTFE 를 "SBE 1.0 / DBE 0.5 wt%" 로 적음.
2. matthews2024 L600–601 — 우리 쪽 σ_e 값 (PTFE 스탬프 전 → 뒤 · 감소율은 L605 · L702 에도 다시 나옴) 과 σ_e 비 두 값을 표지 없이 적음. 카드에는 금지 표지가 없으나, 카드 밖 근거 (프로젝트 지침) 로는 그 비 계열이 인용 금지 · 한 팔이라 정량 인용 불가로 적혀 있어 숫자를 옮기지 않았다 (카드는 09-04 작성본).
3. matthews2024 L573 — "vox ≤ 0.125 µm → ≈ 22 GB" ↔ 같은 표 머리 (L571) 의 외삽 규칙 (dof ∝ vox⁻³ · 0.115 → 35.6 GB · 0.10 → 54 GB) 으로는 ≈ 27.6–27.7 GB (내 검산). 아래 두 행 (≈ 11 TB · ≈ 16 TB) 은 0.10 → 54 GB 기준과 맞음.
4. 우리 σ₀ 표기 — 10-03 작성 세 장 (landesfeind2018 L234 · malifarge2017 L284 · L310 · morasch2018 L218 · L232) 은 "σ₀ 3.0 mS/cm (펠릿값)" 만, 10-13 작성 두 장 (lee2026 L30 · L399 · nakamura2020 L241) 은 "보고 기준 1.5 · 솔버 상수 3.0" (작성일 차 — 배치 안 카드끼리 다름).
5. 접촉망 값의 세대 — malifarge2017 L314–315 는 우리 수송 tortuosity 를 "T_H 중앙 6.21 · Bruggeman 배수 H 중앙 3.40 · P 5.42" (Physics > Hertz · L314 에만 "1세대 협착식" 표지) 로, lee2026 L337 · nakamura2020 L246 은 "ps45 Hertz 5.03–7.24 · Tabor 2.78–4.12" (Tabor < Hertz) 로 적음 — 두 모드의 대소가 카드끼리 반대 (세대 차 · malifarge2017 L315 줄 자체에는 세대 표지 없음).
6. nguyen2020 L193 "우리: RVE ≥ 7.5 × 최대입자" ↔ morasch2018 L303 "우리 침대 두께 ÷ 최대 AM 지름 중앙 4.7" — 규칙과 실제 침대 값이 배치 안 두 카드에서 어긋나 보임 (규칙이 어느 방향에 걸리는지는 카드에 없음).
7. lee2026 L339 — 우리 NCM 전자 전도도가 한 줄에 두 값 (STEP3 1.0 × 10⁻² S/cm ↔ 접촉망 σ_AM 50 mS/cm). 카드가 솔버가 다르다고 구분해 적음 (모순 아님 · 참고).
8. nguyen2020 — 우리 쪽 양의 이름을 "T = τ_Lap,eff²" 로 적음 (L8 · L146 · L158 이하). 같은 날 (10-03) 작성된 landesfeind2018 · malifarge2017 · morasch2018 은 "tau2" — 같은 양의 이름이 카드끼리 다름.
9. 날짜 붙은 관찰 — nguyen2020 L201 "웹앱이 τ_Lap,eff 를 'COMSOL/EIS input' 으로 표시" 는 HEAD 1afd37a9a (L142) 기준 서술이라 현재 상태는 이 카드로 알 수 없음. landesfeind2018 L226 · lee2026 L325 · malifarge2017 L301 · morasch2018 L208 · nakamura2020 L233 · nguyen2020 L183 은 our_dem_baseline.md 가 "값 자리표시 상태" 라고 적음.

**카드 안의 숫자 · 서술 모순 · 오기**
10. landesfeind2018 L116 — "R_Ion^app → R_El/3 근처로 발산 (100/1 에서 ~33 Ω)" ↔ 같은 카드 L63 은 ~33 Ω 를 "저주파 외삽 실축 절편" 으로 적고, 카드의 닫힌 꼴 (L64 · L119) 로는 x = 100 에서 R_Ion^app/R_Ion ≈ 98 (내 검산: 101 − 300/101). 절편과 겉보기 R_Ion 을 섞어 적은 것으로 보임 (malifarge2017 L198 의 β = 10 → 8.27 과도 같은 쪽).
11. nakamura2020 — 혼합 전극의 이온 τ 인쇄 8.86 ↔ 카드 재계산 8.56 (3.5 % 차 · 카드가 L28 · L158 · L315 에 표지). 껍질 두께가 세 값: 단면 0.1–0.2 µm ([인쇄]) · 부피 환산 ≈ 0.23 µm · 입도 D50 차의 절반 0.35 µm ([우리 산술] L85) — 카드가 차이를 적어 둠.
12. lee2026 L209 "첫 면적 용량 7.24 mAh/cm²" ↔ L212 "7.26 mAh/cm² @ 0.7 mA/cm²" (둘 다 [인쇄] · 45 mg/cm² · 0.2PTFE). 다른 시험 구간의 값으로 읽히나 카드에 설명 없음.
13. matthews2024 — 같은 비 (우리 Ø 0.25 µm ↔ primary 피브릴) 를 "8 배" (L527 · L692) · "~10 배" (L533 · L762) · "8–10 배" (L32 · L738) 로 적음 (primary 를 2 µm 로 볼지 "수 µm" 로 볼지의 차).
14. nguyen2020 L33 — Fig 4a 구조 A 의 τ_e/τ = +1.0 % (derived) ↔ 본문 "<1 %" (카드가 병기).

**배치 안 카드끼리의 서술 어긋남 (뒤에 쓴 카드가 "정정 후보" 로 표지 — 앞 카드는 그대로)**
15. nguyen2020 L135 "분리막 쪽 고다공도 구배 설계 지지 (Morasch ref 33)" ↔ morasch2018 L361 "Morasch 는 다공도를 균일 (55 %) 로 고정했다 — 지지하는 것은 분리막 쪽 저 이온 저항이지 다공도 구배가 아니다 (Nguyen 원문 p7 문장은 미열람)".
16. nguyen2020 L231 (ref 29 행 "정의 차의 실측 크기") ↔ landesfeind2018 L388 "방법 (해상도 · 바인더) 차의 실측 크기 — 정의 차는 분리 안 됨".
17. nguyen2020 L228 (ref 18 행 "ASSB 처럼 r_el ≪ r_ion 이 안 설 때 필요") ↔ malifarge2017 L415 "원문에 ASSB 언급 없음 · 해석식은 Tröltzsch–Kanoun 의 것 · 전자 저항이 의미 있는 영역은 시험 안 됨".
18. nguyen2020 L235 "(Morasch — litdb 에 이름만 2 곳 등장, 카드 없음)" · L9 "landesfeind2016 카드는 작성 중" — 이 배치에 morasch2018 카드가 있음 (낡은 서술).
19. morasch2018 L362 — 다른 카드들 (`kim2025_impedance_decoupling_tlm_assb` · `interfacial_impedance_formulation_assb_cathode` · comparison_vs_ours_DEM.md) 의 "Morasch R_int/R_i 비" 는 이 2018 논문이 아니라 Morasch 2021 (JES 168, 080519 · 미열람) 이라는 표지. 2021 논문의 카드는 없음.
20. malifarge2017 L417 — pouraghajan 카드의 "β 보정의 독립 출처" 서술은 원문과 어긋남 (Malifarge 원문에 β 보정식이 없음 — 세 카드가 각자 유도한 식).
21. malifarge2017 L89–90 · L425 — 분리막 값: Table I (Djian 표지) ε 0.55 · τ 6.25 ↔ landesfeind2016 카드 기록 (Djian 의 Celgard 2500 = 23 µm · 0.47 · N_M 13 / Landesfeind 실측 τ 2.5 ± 0.2). Djian 원문 없이 판정 불가.
22. landesfeind2018 L66 · L370 — 흑연 τ 평균 5.1 ± 0.8 (2018 Fig. 3) ↔ 4.3 ± 0.6 (2016 카드) — 같은 자료라고 적혀 있으나 값이 다름 · 원인 [미확인].

**카드가 스스로 표지한 원문 불일치 · 미확인 (고치지 않고 위치만)**
23. landesfeind2018 §10 L364–382 — 원문 오식 9 항 (벽 효과 문장의 lower ↔ higher · Eq. 6 ↔ Eq. 8 · Table III ↔ II · 바인더 시험 전극 48 % · 90 µm ↔ 51 % · 109 µm / 50 % · 85 µm · "(1 % – 5 %)" · R_Ion 전극 수 규약이 절마다 다름 등) · 단층촬영 τ 의 식 · 계산 ε 가 원문에 없음 (L367) · Table II 세 전극 자체의 κ-불변 검사는 없음 (L368) · Minnmann 원문 p.9 는 미열람 (L334) · 판독 값은 "정밀 인용 금지" (L8).
24. lee2026 §10 L430–444 — Fig 1c = Fig S7a 같은 사진 · 하위부피 평균 ≠ 전체 분율 (정규화 미기재 둘) · Fig 4f 칸 이름에 1–2 칸 없음 · "LiNbO₂" (LiNbO₃ 오식 가능성) · Table S1 "0.02TFE" · "Voxel size: 20 nm" ↔ 20.83 × 20.83 × 50 nm · p.2 (온도 없음) ↔ p.13 (100 °C) · 코팅 "100–500 nm" ↔ 주석 최소 67 nm · σ 입력 셋의 출처 없음 · 전도도 측정 압력 · 시료 수 · 등가회로 [미확인] · PTFE 복셀이 어느 상으로 갔는지 [미확인] · C-rate 기준이 셀마다 다름.
25. malifarge2017 §10-3 L419–429 — τ₂ 범위 "5.5–9" ↔ "5–9" · 기공 "10–40 %" ↔ "45–10 %" · ε₁ 이름 셋 · Table I 의 σ 가 고유인지 유효인지 미기재 · n · 적합 창 · 오차막대 정의 미기재 · 그림 3 · 4 의 고주파 시작점 ↔ Table I Z_sep · "TLM 으로 τ 를 낸 첫 논문" 주장 (Landesfeind 2016 미인용).
26. matthews2024 §9 L473–488 — 결론의 "30–32 mAh/cm²" (→ mg/cm²) · NMC "10 µm" ↔ "10–20 µm" · +146 % ↔ "150 %" · 43 % ↔ "40 %" · 등가회로 식이 본문에 없음 (C · CPE 값 미보고) · SI 가 받은 PDF 에 없음 (L58 · L469) · 디지타이즈 값은 "물리 상수로 인용 금지" (L657).
27. morasch2018 §10 L344–359 — st 위상 극소 본문 "~39.1°" ↔ 그림 ≈ 33.6° (카드 재계산 33.58°) · 그림 4 의 주파수 축이 매개변수 계산보다 ≈ 16 배 낮음 [미확인] · "2/3 × Re(Z)" 문구 · 그림 번호 오기 둘 · τ 식 미인쇄 (Ref. 18 로 넘김) · 저주파 외삽 창 미기재 · 대칭셀 분리막 종류 없음 (L142) · 정 / 역 조립이 같은 시편인지 미명시 (L223).
28. nakamura2020 §10 L314–326 — SI 의 이온 차단 / 전자 차단 셀 이름이 뒤바뀜 (그래서 본문 p.8 의 "ion-blocking cell … approximately 8 times thicker" 가 어느 셀인지 모호) · 13 회부터 방전 하한 3.1 → 2.6 V · C 기준 미기재 · "sodium sulfide" (→ sulfate) · "2600 G rpm" · 복합 밀도 3387 kg/m³ 산출 근거 없음 · FIB-SEM (50 회 뒤) ↔ DC (새 펠릿) 시료 상태 불일치 · 반복 n · 오차 [미확인] · 장치 모델명 · 회전자 지름 · 입력 에너지 [미확인] · So 2022 카드의 "Nakamura [17]" 대응은 [추정] (L16).
29. nguyen2020 §10 L220 · L25 — Fig 5 B 의 ε (캡션 20 % ↔ τ/N_M 로는 0.230) · Table 1 voxel 1 µm ↔ Fig 5 캡션 250 nm · 막힌 기공 문턱 2 % (논문) ↔ 0.5 % (TauFactor 1.424.0 코드) · 인용번호 오기 (ref 30 · 41) · "McMullin" / "Mullin" · 게재일 [미확인] · Fig 5 는 크롭 없음 (p6 직접 렌더) · TauFactor mode 6 의 유도 [미확인].

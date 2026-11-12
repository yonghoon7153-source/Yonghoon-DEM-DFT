# batch_23 정독 근거 (카드 7 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `jeong2025_tough_adhesive_binder_shield_ncm811` (544 줄 · 3 번에 나눠) · `jun2026_ppma_econductive_binder_si_lowpressure_assb` (254 · 2 번) · `kang2025_bollard_anchored_binder_dry_electrode` (796 · 5 번) · `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` (423 · 6 번) · `kawaguchi2017_dry_coating_parametric_na2so4_model_se` (254 · 2 번) · `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` (311 · 3 번) · `kim2026_charge_engineered_cnf_binder` (427 · 2 번). 끝까지 못 읽은 카드 없음 (모두 마지막 줄까지 읽음).

배치의 성격: 바인더 실험 · 액체 LIB 3 편 (jeong2025 = PVDF 개질 · NCM811 / kang2025 = 건식 bollard 바인더 · NMC622 · NNP 흡착 · MD / kim2026 = c-CNF 바인더 · NCM811 · 분자 DFT) · 황화물 ASSB 실험 3 편 (jun2026 = Si 음극 전도성 바인더 · LPSCl · 저압 운전 / kawaguchi2017 = 건식 충격 코팅 · 모델 물질 Na₂SO₄ / kawaguchi2023 = 건식 코팅 NCM111@Li₃PS₄ · 압축압 · 체결 토크 2³ DOE) · FEM + ML 1 편 (kang2026 = PTFE 섬유화 미시 FEM (2D 로 보임) + GPR · SiO₂ 모형 · LFP 액체). **DEM · MPM 을 쓴 카드는 없다. 순수 SE 의 압력별 기공 곡선 · 성형 뒤 탈압 되돌아옴 실측 · SE 항복 / 경도 · 큰 변형 접촉 법칙 (MDR · EEPA · Thornton–Ning · Storåkers · 다접촉) 을 준 카드도 없다.** 가압 · 탈압 계획에 쓸 것 = 기공 연산자의 함정 (kang2025) · 압력에 따라 줄어드는 코팅 이점과 무탄소 전자 경로 붕괴 (kawaguchi2023) · 무른 상의 우회 모형 · 크기 상사 · 응력 척도 (kang2026) · 무른 상 완충과 AM 파쇄 (kawaguchi2017 · 2023) · 성형 뒤 운전 / 체결 스택압 의존 (jun2026 · kawaguchi2023).

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`figure-read` / `fr≈` · `stated` · `[인쇄]` · `[판독]` · `[우리 산술]` (= 카드 작성자의 산술) · `[추정]` · `[미확인]` · `[SI 코드]`) · 없으면 "표지 없음". "카드 풀이" = 논문 문장이 아니라 카드 작성자의 서술. "카드 판정" = 카드가 내린 판단. 큰따옴표 안 영어 = 카드가 옮겨 둔 원문. "내 대조" = 카드에 적힌 숫자끼리 맞춰 본 것 (새 측정 아님 · 카드 문제 절에만 씀). 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 — 이 배치에는 LPSCl 진밀도 · 순수 SE 기공의 문헌 값이 나오지 않는다 (kawaguchi2023 의 Li₃PS₄ 1.9 g/cm³ 는 카드가 가정한 값).

**인용 금지 표지가 붙은 값 (숫자로 옮기지 않음 · 위치만)**: jeong2025 L231 · L373 · L411 (DFT 결합에너지 절대값 · 이온 간 순위) · L401 (필름 인성 절대값 — 비율 8× 만 허용) · L434 (CEI 절대 두께) · L435 (GITT D_Li⁺ 절대값) · L511 (쓰면 안 되는 것 목록 — 내부저항 Ω · TM ppb 를 다른 논문 값과 병치 등) · L425 (문장 '접착 · 인성이 동시에 지배'); kang2025 L263 (E_ads 숫자를 estimand 로 이식 금지) · L251 (PTFE dimer 값을 'vdW 흡착 세기' 로 인용하지 않음) · L381 · L456 (영상 픽셀 판독의 Å 절대값 · 정량) · L654 (E_ads 절대값을 우리 값과 나란히 · 'cell-level Wh/kg' 문장) · L727 (Fig S1 의 퍼센트 전부) · L612 · L749 (문장 '다공성이 전자전도를 올린다'); jun2026 L232 (문장 'PPMA 가 항상 우월').

---

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

이 배치에 없음 (순수 SE 의 압력별 기공 곡선 · LPSCl 진밀도를 준 카드 없음). 관련만:
- [a] jun2026_ppma_econductive_binder_si_lowpressure_assb | 상용 LPSCl (POSCO JK · σ 4.2 mS/cm @30 °C · Ti / SE / Ti AC) 150 mg → ~700 µm 펠릿 70 MPa (13 mm PEEK 몰드) → 전극 · 음극을 얹어 전체 370 MPa 압착 — 펠릿 밀도 · 기공은 카드에 기록 없음 | §6 L98 · §5 L89 | 표지 없음 | 곡선 아님 · 370 MPa 뒤 두께 없음 · 진밀도 없음
- [a] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | Li₃PS₄ 분리막 80 mg (다이 10.1 mm) 를 40 MPa · 5 s 예비 압축 → 복합 양극과 함께 P 180 / 360 MPa · 300 s 로 다시 압축 — 두께 · 기공 측정 없음 · 카드 어림 (밀도 1.9 g/cm³ · 완전 치밀 가정) ≈0.53 mm | §3-2 L73 · §8-5 L260 · §10-3 L270 | [추정] (가정 포함) | Li₃PS₄ (LPSCl 아님) · 1.9 g/cm³ 는 카드 가정 (원문에 밀도 없음) · 측정값 아님
- [a] kawaguchi2017_dry_coating_parametric_na2so4_model_se | 'room-temperature pressure sintering' = 황화물 SE 가 상온에서 눌리기만 해도 변형 · 합체해 입계 · 공극이 거의 사라지는 성질 (ref 16 Sakuda 2013 을 근거로 듦) · 값 없음 | §4-3 L140 · §3-1 L62 | 카드 용어집 (ref 16) | 정성 · 모델 물질 선정 근거로 쓰인 서술
- jeong2025 · kang2025 · kang2026 · kim2026: SE 없음 (액체 LIB · SiO₂ 모형).

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

이 배치에 없음 (성형 압밀 뒤 탈압 되돌아옴을 잰 카드 없음). 관련만 (성형 뒤 운전 · 체결 스택압):
- [b] jun2026_ppma_econductive_binder_si_lowpressure_assb | 370 MPa 성형 뒤 운전 압력을 load cell 로 실측 유지 (5 또는 70 MPa) — PVDF-Si 0.2C 용량 2490 (70 MPa) → 1820 mAh/g (5 MPa) · 해석 = 탈리튬화 수축 → 공동 · 균열 → 전자망 붕괴 (PVDF 2.0×10⁻³ → 4.3×10⁻⁵ S/cm) | §6 L98 · §5 L76 · L82 · §7.1 L108 · Supp 1 · Fig 3e | 표지 없음 | 탈압 되돌아옴 측정 아님 (사이클 중 스택압 효과) · Si 음극
- [b] jun2026_ppma_econductive_binder_si_lowpressure_assb | OEP (operando electrochemical pressiometry) — 가압 셀 안 압력 센서 (0.1 kg 분해능) 로 충방전 중 압력 변동을 Δ(ΔP)/Q_discharge 로 기록 · 부피 변화 가역성 지표 | §6 L100 · §12 L190 · §17 L247 · Supp 37 | 표지 없음 | 구속 아래 치수 변화를 압력으로 재는 방법 (탈압 되돌아옴과 다른 양)
- [b] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | 성형 (180 / 360 MPa) 뒤 볼트 체결 토크 Ts 0.5 → 2.5 N·m 에서 Xs 0.1 첫 방전 이득 단순 +22.3 · 코팅 +42.1 mAh/g — 토크 → 압력 환산 원문 없음 · 카드 어림 ≈21 → ≈106 MPa (K = 0.2 가정 · 마찰 · 절연 시트 무시) | §0 ⑥ L32 · §3-2 L75–76 · §8-1 L242 | [우리 산술] · [추정] | 되돌아온 양 측정 없음 · 조건마다 셀 1 개

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기와 견줄 환산

SE 의 항복 · 경도 · 크리프 값은 이 배치에 없음. 일축 항복 세기와 견줄 환산 (H/3 류) 도 없음 — 응력 척도 환산 메모 하나 (kang2026) 뿐. 관련만:
- [c] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | PTFE 구성식 모수 (SI 표 1): 초기 전단 223.7 · 거시 전단 200 MPa · 체적 2.72 GPa · locking stretch 5.6 · 흐름 저항 9.014 / 4.845 MPa · 응력 지수 1 · 80 °C → 카드 환산 E 585.6 MPa · ν 0.464 · AB 급수 초기 전단 203.9 MPa (표 223.7 과 9.7 % 차) | §3-2 L103–104 | [인쇄] · [우리 산술] | 바인더 (SE 아님) · 본문 식 (순수 초탄성) 과 표 (점탄소성 다중 가지 계열 [추정]) 가 다른 모형을 가리킴 · 원문 확인 전 우리 입력 금지 (L292)
- [c] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 문턱 45 MPa = 데이터시트 인장 강도 (보통 공칭) ↔ 출력 P_lm = 2nd Piola–Kirchhoff — 단축 비압축이면 P = λS · σ = λ²S 라 변형률 2–3 에서 수 배 차 · 변형률 정의 · '최종' 값을 뽑는 점 미기재 | §10-6 L347 · §4-4 L221 · §3-2 L107 | [추정] · [미확인] | 이 배치에서 응력 척도 환산이 적힌 유일한 자리 (SE 항복과 무관)
- [c] kang2025_bollard_anchored_binder_dry_electrode | 필름 E PVdF_PTFE 0.83 · CMC_PTFE 0.80 · PC_PTFE 0.15 · PAA_PTFE 0.66 · PTFE 3.50 MPa · 파단 strain 10.8 / 7.4 / 21.9 / 1.2 / 5.2 % (UTM 인장 1 × 3 cm · 0.5 mm/min) | §3a L85–86 · L93 · Fig 3e,f | stated (그림에서만 읽힘) | 다공 fibril 시트의 유효값 · MPM 입력 불가 · 서열만 (L195 · L709)
- [c] jeong2025_tough_adhesive_binder_shield_ncm811 | 바인더 자립 필름 UTS PVDF fr≈18.5 · PVDFA 12.3 · N1 25.4 · N2 36.0 · N5 42.5 MPa · 파단 신율 7.8 / 2.7 / 19.2 / 22.5 / 26.7 % (ASTM D638-M type V · 10 mm/min · n ≥ 5) · PVDFA 는 소성 구간 없이 ≈3 % 에서 취성 파단 | §3b L87–97 | figure-read | 바인더 필름 (SE 아님) · 나노압입 0 (L393)
- [c] jun2026_ppma_econductive_binder_si_lowpressure_assb | 바인더 나노압입 경도 · 영률 = "PVDF·PAA와 comparable" — 수치는 SI 에만 (카드에 값 없음) | §5 L93 · Supp 22 | 표지 없음 | 값 없음
- [c] kim2026_charge_engineered_cnf_binder | 슬러리 항복응력 (진동 G′/G″ 교차) c-CNF 120 vs PVDF 0.2 Pa · 필름 toughness 16.3 MJ/m³ | §4.2 L194 · §4.1 L185 | 표지 없음 | 슬러리 유변 (입자 항복과 다른 양)
- [c] kawaguchi2017_dry_coating_parametric_na2so4_model_se | 게스트 Na₂SO₄ 의 강성 · 탄소성이 황화물과 비슷하다는 근거 = 압입 시험 (ref 18) · 수치는 이 논문에 없음 | §3-1 L62 · §10-1 L219 | [미확인] | 값 없음
- kawaguchi2023: 항복 · 경도 값 없음.

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

하중 몫 · 재밍의 수치는 이 배치에 없음. 관련만 (정성 — 무른 상이 단단한 입자의 파쇄를 줄인다):
- [d] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | 단순 혼합 Xs 0.1 에서 NCM 안 균열 · Xs 0.3 에서 억제 — 저자 해석 "높은 Xs 가 NCM 에 걸리는 압축 응력을 완화" · 코어–셸도 압축 응력 완화 (180 / 360 MPa 압축) | §3-7 L147–148 · p.12–13 | [인쇄] (저자 해석 · SEM 정성) | 하중 몫 계산 없음 · 셀 1 개
- [d] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | 단순 혼합은 Xs 0.3 에서도 NCM–NCM 접촉이 남음 (Fig 5d) · 코팅은 Xs 가 오르면 NCM–NCM 접촉이 줄어 NCM 이 LPS 기지 안 섬이 됨 (Fig 6c,d) | §3-7 L145 · §5 L181–182 | [인쇄] · SEM 정성 | 접촉 수 정량 없음
- [d] kawaguchi2017_dry_coating_parametric_na2so4_model_se | 충격 코팅 중 게스트 20–30 wt% 는 300 s 까지 NCM 파쇄 없음 (완충) · 10 wt% 이하 (100 m/s) · 1800 s 는 파쇄 — 원인 후보 = 막이 얇아져 충격 전달 · 피로 (둘 다 "may be") | §3-4 L96 · §3-5 L103 · §0 ④ L29 | [인쇄] · '이하' 읽기는 [추정] | 압축이 아니라 충격 공정 · 모델 물질
- [d] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 미시 FEM 의 AM 원 = PTFE 에 압력을 거는 단단한 몸 (재질 무감 — SiO₂ ↔ LFP 곡선 겹침, SI Fig 6) · 하중 몫 계산 없음 | §4-3 L216 · §10-26 L367 | [판독] · [추정] | 2–4 원 정적 모형 (충전 · 힘 사슬 없음)

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값 수

이 배치에 없음 (DEM 접촉 법칙을 다룬 카드 없음 · MDR · EEPA · Thornton–Ning · Storåkers · 다접촉 0 회).

## f. MPM 의 접촉 · 다물체 · 강체 결합 · 해상도 규칙 (지름당 셀 수) · 수치 오차 추정

이 배치에 없음 (MPM 카드 없음 · 지름당 셀 수 규칙 없음). 관련만:
- [f] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 미시 FEM 의 PTFE 띠 두께 ≲1 µm (입자 10–20 µm 보다 한 자릿수 얇음) · 메시 크기 · 수렴 시험 미기재 — 카드: 우리 MPM `d_h/dx ≳ 3.5` 규칙과 같은 질문을 던질 그림 | §7-2 L279 · SI Fig 1c–d | [판독] · [추정] | FEM (MPM 아님) · 메시 미기재
- [f] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 변형률 3–6 (학습표 최대 5.91) 의 대변형을 라그랑주 메시로 · 재메시 · 메시 수렴 언급 없음 — 카드 풀이: MLS-MPM 은 메시 엉킴이 없어 이런 대변형 바인더에 원리적으로 맞는 도구 (구성식 · 섬유화 판정은 새로 정의해야) | §7-2 L278 | [추정] · [미확인] | 카드 풀이
- [f] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 오차 추정 = GPR 5-겹 CV (응력 모형만 · 무작위 폴드 = 같은 입경 곡선 안 보간) R² 0.989 / 0.995 · 메시 수렴 · 하중 속도 의존 · 입경 하나 빼기 검증 없음 | §3-7 L194 · §6 L256 · §10-12 L353 | [SI 코드] | 대리 모형 오차이지 FEM 이산화 오차 아님
- [f] kang2025_bollard_anchored_binder_dry_electrode | XRM (Xradia 810 Ultra) FOV 18×18×18 µm³ · 화소 128 nm — 카본 · 바인더는 X 선 투명이라 NMC 만 보이고 porosity 를 뽑지 못함 | §6.2 L564 · §6.3 L582 | stated | 영상 해상도 (계산 해상도 아님)

## g. 2D 결과를 3D 로 옮길 때의 경고 · 증거

이 배치에 2D → 3D 전이 경고 · 증거 없음. 관련만:
- [g] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 미시 FEM 의 차원이 인쇄되지 않음 — SI Fig 1 · Fig 1b 축이 x · y (µm) 라 2D 단면으로 보이고 · 카드의 PTFE 몸체 크기 환산도 '2D 비압축 가정' · 그 결과를 3D 실물 (SiO₂ 막 · LFP 후막) 에 바로 대응시키며 2D → 3D 전이에 대한 논문 서술은 카드에 없음 | §3-2 L99–100 · §0 L34 | [판독] · [우리 산술] · [미확인] | 경고나 증거가 아니라 '차원 미기재' 표지
- [g] kang2025_bollard_anchored_binder_dry_electrode | MD 영상 (3D 궤적의 렌더) 의 픽셀 궤적 재측정 — "2D 투영 중심이다. 논문 지표는 3D 평균거리 → 같은 추정량이 아니다" · 쓸 수 있는 것은 시점 · 서열 · 배수 | §4.10-B L455–456 | 카드 판독 한계 | 3D → 2D 투영 (2D 계산을 3D 로 옮기는 문제 아님)
- jeong2025 · jun2026 · kawaguchi2017 · kawaguchi2023 · kim2026: 2D 계산 없음.

## h. DEM 에서 FE · MPM 으로 넘긴 선례 · 넘긴 시점

이 배치에 DEM → FE · MPM 선례 없음. 관련만:
- [h] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 거시 유동 FEM (반죽기 · 압출기 · 멱법칙 유체 K · n 미기재) 의 전단 응력 → 미시 FEM 의 경계 하중 PLP 로 넘김 — "Shear rates obtained from macroscale simulations were subsequently converted into PLP values" (환산식 미기재) · 실물 PLP 측정 없음 | §3-5 L144 · §10-15 L356 · §4-1 L206 | [인쇄] · [미확인] | 거시 → 미시 하중 넘김 (DEM 아님) · 넘김 규칙 없음
- [h] kim2026_charge_engineered_cnf_binder | 실측 매개변수 (τ · OCV · 저항) → 다공전극 PDE (GA 100 회 매개변수 추정 → 확률밀도) | §4.5 L264–266 | 표지 없음 | 측정 → 연속체 전기화학 (DEM 아님)

## i. 복합 양극 (AM + SE) 의 압력별 기공

AM + SE 복합의 압력별 기공 값은 이 배치에 없음. 관련만:
- [i] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | NCM111 + Li₃PS₄ (무탄소) · 180 → 360 MPa — 단순 혼합 Xs 0.3 에서 LPS 영역 미세공극 (흰 화살표) 이 360 MPa 에서 거의 사라짐 (LPS 소성 · 합체 → Rs ↓) · 공극률 미측정 | §3-7 L144 · Fig 5c,d · §0 ④ L30 | [인쇄] (SEM 정성) | 기공 값 없음 · 조건마다 셀 1 개
- [i] kawaguchi2017_dry_coating_parametric_na2so4_model_se | NCM111 + Na₂SO₄ (모델) 90:10 압분체 360 MPa 단면 — NCM 이 응집 없이 기지에 흩어지고 계면 접촉 형성 | §3-7 L112 · Fig 7e,f | [인쇄] (정성) | 모델 물질 · 기공 값 없음
- [i] kang2025_bollard_anchored_binder_dry_electrode | LIB 양극 NMC622 : Super P : 바인더 93:5:2 · 3.0 g/cm³ 에서 25.90 / 19.47 / 17.68 % (PC_PTFE73 / PTFE / PVdF) = tap density 가정 계산 · 명시 입력 재계산 28.1 / 21.7 / 19.9 % (+2.2 %p) · 순위 · 격차만 | §3c L114–115 · §6.3 L569–582 · Table S3 | 표 · 카드 재계산 (표지 없음) | SE 없음 · 압력 축 없음 (밀도 정지) · 측정 아님
- [i] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | SiO₂ : CB : PTFE 90:5:5 자립막 MIP 공극 37.2 / 32.2 / 46.7 % (20 / 10 / 1.5 µm) · 32.2 / 29.9 / 36.1 % (10+10 / 10+5 / 10+1.5) — 캘린더 압력 · 두께 · 밀도 미기재 | §3-3 L124 · §3-4 L134 · §10-24 L365 | [인쇄 그림] | SE 없음 · 압력 없음
- [i] kim2026_charge_engineered_cnf_binder | NCM811 LIB 전극 기공률 c-CNF 30.9 vs PVDF 29.7 % (120 °C roll-press · 압력 값 없음) | §4.3 L230 · §2.3 L113 | 표지 없음 | SE 없음 · 압력 없음
- jeong2025 · jun2026: 기공 값 없음.

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압 계산과 닿는 것

- [j] kang2025_bollard_anchored_binder_dry_electrode | "성형압 ↔ porosity / Heckel … 0건" — 압밀이 압력이 아니라 목표밀도 (3.0 g/cm³) 로 규정 → "다압력 곡선·Heckel 불가" | §3e-(다) L193 | 카드 판정 | —
- [j] kang2025_bollard_anchored_binder_dry_electrode | 카드 풀이: 산업 건식라인의 실제 규약은 밀도 정지 (우리 `hold` 쪽) — 동시에 "hold 에서 porosity 는 정지 프레임의 함수" 이고 이 논문 porosity 가 밀도 역산 계산값인 것도 같은 구조 → "둘 다 정지규약이 값을 정한다 는 공통 취약점이지, 상호 검증이 아니다" | §7b L611 | 카드 풀이 | 우리 MPM 과의 대응은 카드 해석
- [j] kang2025_bollard_anchored_binder_dry_electrode | 필름 E (MPa 스케일) → MPM 재료 입력 직접 사용 ⛔ · soft-phase 서열 · 비율만 | §10.4 L709 · §3e-(다) L195 | 카드 판정 | 카드 안 우리 PTFE 값 두 개 (카드 문제 6)
- [j] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 실물 공정 조건 (rpm · 시간 · 온도 · 간극 · 캘린더 압력) 미기재 · '섬유화' 는 구성식에 없음 (사후 구간) · 2D / 3D · 원 치수 · PTFE 초기 크기 · 메시 · 접촉 · 하중 속도 · 해석 시간 미확인 · COMSOL 모델 미공개 | §0 한정어 L46 · §3-2 L99 · §10-5 · 7 · 13 · 16 L346 · L348 · L354 · L357 | 카드 판정 · [미확인] | —
- [j] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | MIP 공극의 교락 — 막의 캘린더 상태 · 두께 · 밀도 미기재 → 공극 차이를 섬유화 차이로 읽을 근거 부족 · LFP 전극 공극 미보고 | §10-24 L365 | 카드 판정 | —
- [j] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | Rs = 분리막 + 복합 양극 — 분리막 (80 mg) 도 같은 P 로 다시 눌려 치밀해지므로 P 효과의 일부는 분리막일 수 있음 · 분리막만 어림 ≥ 0.7 kΩ (Rs 791–2,520 Ω 와 같은 자릿수) | §10-3 L270 · §8-5 L260 | [추정] (가정 포함) | 압력 효과 귀속 문제
- [j] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | 공극률 · σ 가 없어 우리 모델 (DEM · MPM) 의 보정 · 검증 앵커가 되지 못한다 (frame [4]) · 조건마다 셀 1 개 · 체결 토크 → 압력 환산 없음 · Xs 0.2 반응표면 = 측정 없는 선형 보간 | §10-10 L277 · §7-4 L235 · §3-2 L75 · §10-6 L273 | 카드 판정 | —
- [j] kawaguchi2017_dry_coating_parametric_na2so4_model_se | 모델 물질 Na₂SO₄ 는 이온 전도 없음 · 강성 · 탄소성 · 가압 소결 유사성의 수치 (ref 18) 가 이 논문에 없음 · 피복 정량 없음 · 조건마다 1 회 | §10-1–3 L219–221 | 카드 판정 | —
- [j] jun2026_ppma_econductive_binder_si_lowpressure_assb | 이점은 실용 저압 (≈5 MPa) 전용 — 70 MPa 에선 PVDF 142 > PPMA 131 mAh/g 역전 · "PPMA가 항상 우월" 인용 금지 · 조성 교란 (90:10 vs 97:3) | §16 L231–232 | 카드 판정 | 운전 스택압 축 (성형 압밀 축 아님)
- jeong2025 · kim2026: 가압 · 탈압과 닿는 한계 서술 없음 (압력 축 없음).

## k. DEM 의 한계 (인용 서지 병기)

이 배치의 일곱 편은 모두 DEM 을 쓰지 않는다 → 논문의 말은 일곱 편 모두 없음. 아래 "카드 풀이" 는 카드 작성자가 우리 DEM 을 두고 적은 서술이다 (논문 문장 아님 — 인용할 때 논문 근거로 쓰지 않는다).
- [k] jeong2025_tough_adhesive_binder_shield_ncm811 (Y. H. Jeong, Won, Kim, Jo, Seo, Shim + D. Jeong (카드 표기 순), Adv. Energy Mater. 2025, 15, e02765) | 말 없음 (DEM 안 씀 · 입자 계산 없음) | — | — | —
- [k] jun2026_ppma_econductive_binder_si_lowpressure_assb (Jun, Jeong … Kim, Jung, Nat. Commun. 2026, 17:156) | 말 없음 — 카드: "계산 0 (DFT·MD·결합에너지·시뮬레이션 일절 없음)" | §10 L162 | 카드 판정 | —
- [k] kang2025_bollard_anchored_binder_dry_electrode (Kang, Eom, Jang … Han, Nam, Song, Adv. Mater. 2025, 37, 2416872) | 말 없음 (DEM 안 씀) · 카드 풀이: SI 영상 3 편은 MD 궤적 렌더라 "우리 DEM/MPM 압밀의 실시간 대조군으로는 쓸 수 없다" | §4.10-A L418–419 | 카드 풀이 | DEM 한계 문장 아님
- [k] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode (Kang, Jeong … Choi, Cho, Commun. Mater. 2026, 7:34) | 말 없음 (DEM · MPM 없음) · 카드 판정: 본문의 "particle dynamics" 는 2–4 개 원의 정적 연속체 FEM (입자 운동 · 충돌 · 충전 없음) · 카드 풀이: 우리 DEM (강체 구 · Hertz/hysteresis · Auerbach · SJKR) 은 PTFE 섬유 · 막 · 바인더 다리를 표현하지 못하고 · 점착 없는 압밀 DEM 은 미세 분획 응집이 기하 충전 이득을 뒤집는 역전을 낼 수 없다 | §4-2 L212 · §4-3 L217 · §7-6 L303 · §10-27 L368 | [추정] (카드 풀이) | 카드가 우리 DEM 을 두고 쓴 서술
- [k] kawaguchi2017_dry_coating_parametric_na2so4_model_se (Kawaguchi, Nakamura, Watano, Powder Technol. 305 (2017) 241–249) | 말 없음 (DEM 없음) · 카드 풀이: 믹서 DEM (강체 구 · SJKR 점착) 에는 게스트 소성 · 합체 · 호스트 파쇄가 없다 → 코팅 상태는 우리 모델에서 입력 (결과가 아님) · AM 파괴 = 접촉 판정 (Auerbach) 만 · 조각 없음 → 파쇄 완충 몫을 못 그린다 · 충격 블렌더 흐름 (고체 ca. 1 vol% — Nakamura 2020 진술) 은 우리 조밀 드럼과 다른 영역 | §4-2 L132 · §7-1 L171–172 · §8-4 L212 | 카드 풀이 | —
- [k] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps (Kawaguchi, Nakamura, Hayakawa, Ohsaki, Watano, Adv. Powder Technol. 34 (2023) 104264) | 말 없음 (DEM 없음) · 카드 풀이 (카드 문장 그대로): "DEM 은 강체 구 + 겹침 (E_SE 1.35 GPa 연화 · 형상 소성 없음 · AM 파괴는 접촉 판정만) · MPM 은 SE 형상 소성 (σ_y 0.30 GPa) 이 있으나 AM 은 얼린 골격 · 둘 다 껍질 (코어–셸) 을 표현하지 않는다" · "우리 DEM 에는 껍질이 없어 이 붕괴를 예측하지 못한다" | §4-2 L159 · §7-3-2 L227 | [추정] (카드 풀이) | —
- [k] kim2026_charge_engineered_cnf_binder (Kim, Kim … Lee, Lee, Nat. Commun. 2026, DOI 10.1038/s41467-026-73909-0 · Article in Press) | 말 없음 (DEM 안 씀 · 분자 DFT + MD + PDE) | — | — | —

## l. 소성변형이 왜 어려운가 (인용 서지 병기)

입자 계산에 소성을 넣기 어려운 이유를 논문이 설명한 카드는 이 배치에 없다. 택한 우회가 적힌 것은 kang2026 하나.
- [l] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode (Kang, Jeong … Choi, Cho, Commun. Mater. 2026, 7:34) | 우회 = 무른 상 (PTFE) 을 가역 초탄성 (Arruda–Boyce 8사슬 — "eight-chain molecular network theory, where the Helmholtz free energy is derived from the inverse Langevin function") 으로 두고 소성 · 섬유화 · 막을 응력–변형 곡선 위 사후 구간으로 정의 (I 탄성 · II 소성 · III 섬유화 "shear-induced deformation leads to fiber formation" · IV 막 "If the applied stress exceeds the PTFE tensile strength, the fibrillar structure collapses into the film-like morphology") · 카드 판정: "초탄성은 가역이고 '소성 · 섬유화 · 막 · 파단' 은 구성식에 없다" · 합 항을 "plastic deformation region" 이라 부르고 "We employed Simo-Taylor" 를 정의 없이 씀 | §3-2 L101 · L105 · §10-5 L346 | [인쇄] · [추정] | 어려운 이유의 설명은 없음 (우회만)
- [l] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode (같은 서지) | 맞춘 값 · 검증: 실험 응력 한 점과 대조 — "the model identifies the fibrillation onset at a strain of 1.13 … where the simulated stress was 16.9 MPa — a value comparable to the experimental result of 16.4 MPa" (실험 곡선은 그림에 없음 · 문장 끝 인용 ref 33 = PTFE 굽힘 응력 곁사슬 절단 논문) · 파단 연신 불일치는 "likely due to variations between the PTFE grades" · 물성 = 데이터시트 인장 강도 (제약으로만 등장) + ref 41 (PTFE 마찰 논문) 의 E · ν (값 미기재) + SI 표 1 모수 12 줄 · 대리 모형 = FEM 결과 270 (단봉) + 200 (쌍봉) 점 GPR · 검증 범위 = SiO₂ 입경 순서의 정성 일치 (SEM · 응집 강도 · MIP) · 계산 비용 카드에 없음 | §3-2 L102–106 · §3-7 L193 · §7-8 L312 · §10-4 L345 | [인쇄] · [SI 코드] | 실물 공정 측정 (토크 · 온도 · 응력 · 섬유화 정도) 과 독립 대조 0
- [l] kawaguchi2017_dry_coating_parametric_na2so4_model_se (Kawaguchi, Nakamura, Watano, Powder Technol. 305 (2017) 241–249) | 관찰만 (모델 없음): 연한 게스트가 강한 충격으로 단단한 호스트 위에서 소성 변형 · 합체 → 낱알이 막이 됨 (ref 18 이 밝혔다고 인용) · 과다 충격의 즉시 파쇄는 관찰이 아니라 예상 ("it is expected that host particles can be immediately broken") · 상온 가압 소결 = 눌리기만 해도 입계 · 공극이 사라짐 (ref 16) | §3-3 L88 · §3-6 L107 · §4-2 L131 · §4-3 L140 | [인쇄] · 카드 용어집 | 어려움을 직접 말하지 않음 — 공정 중 입자 단위의 정체가 사라진다는 서술
- [l] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps (Kawaguchi, Nakamura, Hayakawa, Ohsaki, Watano, Adv. Powder Technol. 34 (2023) 104264) | 관찰만 (모델 없음): 충격으로 무른 LPS 가 단단한 NCM 위에서 소성 변형 · 합체 → 껍질 · 압축 중 LPS 소성 · 합체로 미세공극 소멸 (180 → 360 MPa · SEM) | §3-1 L62 · §3-7 L144 · §4-2 L158 | [인쇄] | 어려움을 직접 말하지 않음
- jeong2025 (Adv. Energy Mater. 2025, 15, e02765) · jun2026 (Nat. Commun. 2026, 17:156) · kang2025 (Adv. Mater. 2025, 37, 2416872) · kim2026 (Nat. Commun. 2026, DOI 10.1038/s41467-026-73909-0): 말 없음 (입자 계산 없음).

## m. 받아들일 통찰 (무엇 → 우리 쪽 어디 → 왜)

- [m] kang2025_bollard_anchored_binder_dry_electrode | 문헌 기공값의 정체부터 확인 — 기공이 측정 (수은 · 가스 · 토모) 이 아니라 밀도 · 조성에서 역산한 계산이면 입력 밀도 (여기서는 tap density) 가 순위를 전부 정하고, 명시 입력으로 다시 계산하면 +2.2 %p 어긋남 → 결과 전 대조에 넣기 전에 측정 / 계산을 가르고 역산이면 상별 진밀도 입력을 같이 기록 → 자리: 단계 0; 결과 전 대조 항목 | §6.3 L569–582 | 표 · 카드 재계산 (표지 없음) | 액체 LIB
- [m] kang2025_bollard_anchored_binder_dry_electrode | 밀도 정지 규약 = 산업 건식 롤의 실제 규약 (3.0 g/cm³ 에 닿을 때까지 반복 통과 · 압력 수치 0) — 그때의 기공은 정지 규칙이 정한 값이라 독립 검증이 아님 → 우리 정지 규약 (판 정지 · hold) 결과를 밀도-정지 문헌값과 맞았다고 '일치' 로 부르지 않는다 → 자리: 단계 0; 단계 4 | §7b L611 · §3e-(다) L193 | 카드 풀이 | —
- [m] kang2025_bollard_anchored_binder_dry_electrode | 짝 값 역산으로 숨은 조건 · 단위 복원 — Fig 3b (R_s) 와 3c (σ_e) 짝에서 t = 1/(σ·R_s) 가 건식 5 시편 99.3 ± 1.4 µm 로 수렴해 양의 정체 (시트저항 Ω/□) 와 빠진 두께를 확정 · σ_ion 식의 L 에 분리막 두께가 들어가 겉보기값임을 원문 식에서 찾음 → 문헌 수송 앵커를 반입할 때 짝 값 · 정의식을 한 번 검산 → 자리: 단계 7 (결과 전 대조 항목의 입력 검사) | §3e L153–186 · §10.1b ⑦ ⑧ L725–726 | 카드 역산 (표지 없음) · SI p.6 원문 | 액체 LIB · 무가압 시트
- [m] kang2025_bollard_anchored_binder_dry_electrode | PTFE 섬유화 하한 실측 — 앵커 바인더 동반 0.6 wt% 에서 dough 성립 · 0.2 wt% 는 갈라짐 (Fig S10 사진) · PTFE 단독은 2 wt% 필요 → 자리: 흐름 밖: PTFE fibril 축 (`--ptfe-fibril`) 하한 앵커 후보 | §3c L117 · §7 L599 · §8 ⑤ L641 | stated · Fig S10 | 건식 LIB (fibrillation 공정 물리는 공통이라는 카드 판단)
- [m] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 크기 상사 시험 — 길이척도 없는 구성식 (초탄성 · J2) 은 기하를 상사로 키우고 같은 압력을 걸면 응력장이 같아야 하는데 학습표는 같은 13 MPa 에서 P_lm ∝ d^0.73 → 그 입경 효과는 AM : PTFE 크기비나 '압력 × 면적 = 힘' 하중 정의에서 온 것 [추정] → 입경 · 해상도 효과를 물리로 부르기 전에 상사 시험을 단위 시험으로 등록 → 자리: 단계 2 (U1 · U6 옆 상사 시험); 단계 3 | §7-2 L276 · §8-2 L323–326 · §3-5 L161 | [우리 산술] · [추정] | CL-64 부류 (카드 인용)
- [m] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 응력 척도 선언 — 계산 출력 (2nd PK) 을 문헌 문턱 (공칭 인장 강도) 과 큰 변형률에서 비교하면 λ · λ² 배 차 · 변형률 정의 · 값을 뽑는 점도 미기재 → 항복 세기 하나를 실험 기준에 맞추거나 문헌 항복과 견줄 때 응력 척도 · 정의를 결과 전에 적는다 → 자리: 단계 4; 결과 전 대조 항목 | §10-6 L347 · §4-4 L221 | [추정] | —
- [m] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 얇은 띠 해상도 — 입자 (10–20 µm) 사이 무른 상 띠 (≲1 µm) 가 응력을 정하는데 메시 · 수렴 미기재 → 가장 얇은 무른 상 띠를 가로지르는 셀 수를 해상도 규칙에 넣고 수렴 시험 → 자리: 단계 2 (U6); 단계 5 | §7-2 L279 · SI Fig 1c–d | [판독] · [추정] | FEM 사례
- [m] kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode | 대리 모형 검증 · 재현의 함정 — 무작위 5-겹 CV 는 같은 입경 곡선 안 보간이라 R² 0.989 / 0.995 가 입경 일반화를 말하지 않고 변형률 모형은 검증 0 · 저장된 Fig 5e 가 노트북의 다른 행 ('10' 행) 을 그렸고 실행 순서가 뒤섞임 → 입경 하나 빼기 검증 · 그림과 코드 상태를 같이 기록 → 자리: 흐름 밖: ML 설계 대리 모형 검증 · 재현성 보고 | §7-7 L307 · §3-7 L199 · §10-9 · 12 · 13 L350 · L353–354 | [SI 코드] | —
- [m] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | 코팅 이점은 압축압에 걸린다 — 같은 Xs 0.1 에서 첫 방전 비 ×3.2–3.6 (180 MPa) → ×1.09–1.21 (360 MPa) · Rs 비 ×0.63 → ×0.88–1.06 → 300 MPa 비교에서는 차이가 작게 나올 것을 결과 전에 적거나 낮은 압력 한 수준을 더 둔다 → 자리: 결과 전 대조 항목; 흐름 밖: 코팅 믹싱 비교 설계 | §7-3-1 L226 · §0 ⑤ L31 · §8-1 L241–244 | [우리 산술] · [추정] | 셀 1 개씩 · Rs 에 분리막
- [m] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | 무탄소 코팅 + 많은 SE = 전자 경로 붕괴 (코팅 Xs 0.3 → 1.8–11.0 mAh/g · NCM 이 LPS 기지 안 섬) — 껍질이 없는 우리 접촉망은 이 붕괴를 못 냄 → 코팅 팔은 σ_e 를 같이 계산하고, 카드 제안 대리 = '코팅 쌍의 AM–AM 전도를 끊은 σ_e' (미등록 · 미실행) → 자리: 단계 7 | §7-3-2 L227 · §8-2 L246–249 | [인쇄] · [추정] | —
- [m] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | 같은 총 SE ≠ 같은 껍질 몫 — Xs 0.1 → 0.3 에서 껍질 몫이 53 → 14 % 로 같이 움직이고 '코팅 전극' 도 자유 LPS 를 47 · 86 % 품음 → 총 SE 를 고정하고 껍질 몫을 따로 움직이는 설계 · 코팅 뒤 순조성 (투입 10 → 순 5.6 wt%) 먼저 측정 → 자리: 흐름 밖: 코팅 믹싱 실험 설계 | §7-3-3 L228 · §7-3-4 L229 · §7-2 L221 · §0 ③ L29 | [우리 산술] · [인쇄] | —
- [m] kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps | EIS 고주파 저항 Rs 는 함께 눌린 SE 분리막을 품는다 (어림 ≥ 0.7 kΩ = Rs 와 같은 자릿수) → 복합 양극 이온 수송을 실험과 견줄 때 TLM 으로 R_ion · R_ele 를 가른 값만 결과 전 대조로 쓴다 → 자리: 단계 7; 결과 전 대조 항목 | §8-5 L259–261 · §10-3 L270 | [추정] (가정 포함) | —
- [m] kawaguchi2017_dry_coating_parametric_na2so4_model_se | 코팅 형태는 SE 비율에 걸린다 — 같은 300 s · 100 m/s 에서 게스트 ≤20 wt% 는 연속 막 · 30 wt% 는 불연속 (게스트 단위 질량당 에너지) → SE 함량 수준을 바꾸면 막 형태가 같이 바뀌는 교락 · 수준마다 SEM 으로 형태를 고정해 보고 → 자리: 흐름 밖: 코팅 활물질 믹싱 (V1 · V3 설계) | §3-5 L101 · §7-3-1 L183 · §8-2 L201–203 | [인쇄] · [추정] | 모델 물질
- [m] kawaguchi2017_dry_coating_parametric_na2so4_model_se | 값싼 연속성 대리 지표 — 압분체 (0.50 g · ⌀10 mm · 360 MPa) DC 저항 증가를 게스트 질량분율로 나눈 R_inc (식 1) 가 덮임 · 연속을 가름 (50 → 80 m/s 에서 ≈20 배) → 코팅 연속성이 전자 차폐 (σ_e 하락) 로 나타나는 방향의 실험 대조 → 자리: 단계 7; 결과 전 대조 항목 | §3-8 L116–121 · §3-3 L89 · §7-3-4 L186 | [인쇄] · [판독] · [추정] | 선형 정규화 가정 · 실제 황화물은 σ_ion 과 함께 재야 뜻이 있음 (L186)
- [m] kawaguchi2017_dry_coating_parametric_na2so4_model_se | 무른 상 완충이 AM 파쇄를 막는다 — 게스트 20–30 wt% 는 300 s 까지 파쇄 없음 · 막이 얇거나 게스트가 적으면 파쇄 → AM 파괴 판정은 둘레 무른 상과 묶여야 하고 조각 없는 DEM 은 이 몫을 못 냄 (실험–모델 차이 후보로 미리 적어 둠) → 자리: 조건 R7 | §8-4 L210–212 · §7-1 L172 | [인쇄] · [추정] | 충격 공정 (압축 아님)
- [m] jun2026_ppma_econductive_binder_si_lowpressure_assb | 상태별 전자망 측정법 — 전극과 SE 층 사이에 Ni mesh 를 제3전극으로 넣고 충방전을 멈춘 상태에서 집전체–mesh DC 로 전극층 σ_e 만 분리 (충방전 깊이별 곡선) → 접촉 붕괴 시점을 직접 보는 실험 대조 → 자리: 흐름 밖: 열화 (사이클 중 접촉 손실 · R_int(N)) 대조 | §6 L99 · §12 L185 · §17 L245 | 표지 없음 | Si 음극 · ex situ
- [m] jun2026_ppma_econductive_binder_si_lowpressure_assb | 비교 설계의 교락 — 바인더 정체와 함량을 동시에 바꾼 비교 (90:10 vs 97:3) 는 순수 재료 비교가 아님 → 우리 첨가제 비교 (예: SBE ↔ DBE) 에서 첨가제 정체 · 함량 · 운전 압력을 따로 표지 → 자리: 흐름 밖: SDCP 첨가제 비교 보고 | §16 L231 | 카드 판정 | —
- [m] jun2026_ppma_econductive_binder_si_lowpressure_assb | OEP — 일정 구속 셀의 압력 변동을 용량당 Δ(ΔP)/Q 로 기록해 부피 변화 가역성을 봄 → 사이클 부피 변화 · 접촉 열화 계산의 실험 관측량 후보 → 자리: 흐름 밖: 열화 (사이클 화학-기계) 관측량 | §6 L100 · §7.9 L145 · §12 L190 | 표지 없음 | 지표 정의는 ref 33 방법
- [m] jeong2025_tough_adhesive_binder_shield_ncm811 | 접착 (180° peel) 과 층내 응집 (SAICAS · 깊이 10 µm) 을 따로 잰다 — PVDF → PVDFA 에서 peel 3× 인데 SAICAS 1.5× 뿐 = PAA 이득은 대부분 집전체 접착 → 바인더 점착을 보정할 때 입자–입자 응집 값으로 peel 을 쓰지 않는다 → 자리: 흐름 밖: 믹싱 · 건식 DEM 바인더 점착 보정 | §3c L115 · §7d L346–350 | figure-read · 카드 풀이 | 액체 LIB 전극 · 값이 아니라 시험 설계만
- [m] jeong2025_tough_adhesive_binder_shield_ncm811 | 문헌 물성 반입 때 단위 검산 — 응력–변형 곡선을 적분해 인성을 다시 구하면 축 단위가 1000 배 틀린 것이 드러남 · 같은 결함이 다른 바인더 카드에도 있음 (장르 반복) → 반입 값마다 원 곡선 · 정의식으로 한 번 다시 계산 → 자리: 흐름 밖: 문헌 값 반입 규칙 (결과 전 대조 항목 입력 검사) | §3b L99 · §10-① L399–402 | 카드 계산 (표지 없음) | 숫자는 인용 금지 (비율만)
- [m] jeong2025_tough_adhesive_binder_shield_ncm811 | 흡착 · 결합 에너지는 기준 상태와 대상을 같은 제약으로 — 기준 (PVDF) 값이 이온마다 3 배 달라 차분이 흔들리고 · 스핀 상태 · 조각 크기 (작용기당 정규화) · 자세 탐색이 미선언 → SDCP 흡착 계산에서 상태 선택 · 집계 규칙 · 크기 정규화를 결과 전에 적는다 → 자리: 흐름 밖: SDCP DFT 보고량 | §10-② L404–411 · §7b L310–322 | 카드 판정 | 숫자 인용 금지 (L411)
- [m] kim2026_charge_engineered_cnf_binder | 쌍별 부착일 균형 판정 — 접촉각 (물 · DIM) → Fowkes 로 γᵈ · γᵖ 분해 → 쌍마다 부착일 · 응집일 (2γ) · 응집일 < 다른 상 부착일이면 자기응집 · 상분리 (PVDF 59.58 < 78.40) · 균형이면 균질 (c-CNF 106.9 ≈ 107.1 / 103.6) → 믹서 점착 세기 (상별 표면 에너지) 를 재는 실측 경로 후보 → 자리: 흐름 밖: 믹싱 점착 행렬 입력 · 이종기술 논지의 표면 에너지 비 측정 후보 | §4.3 L207–217 · §6 L321–323 | 표지 없음 (Table S1) | 바인더–전극 쌍 (SE–SE · SE–AM 아님) · 액체 LIB
- [m] kim2026_charge_engineered_cnf_binder | 문헌 τ 의 정의부터 — 이 논문 τ 는 N_M = K_bulk/K_eff = τ/ε 로 정의 (EIS 대칭셀 · τ = R_ion·A·k·ε/2d) → 값을 가져올 때 이 정의식으로 tortuosity factor (제곱) 인지 제곱근 꼴인지 먼저 대조 → 자리: 흐름 밖: τ 명명 규약 (수송 tortuosity) | §4.3 L231–237 · §6 L326–328 | 표지 없음 | 액체 기공 경로 (폼 · 수치 차용 금지 · L328)
- [m] kim2026_charge_engineered_cnf_binder | 기공률이 같아도 수송이 2 배 다를 수 있다 — 30.9 vs 29.7 % 에서 τ ~3.6 vs ~6.8 (분산 · 표면화학 차이) → 수송을 기공률 하나로 판정하지 않고 분산 · 연결 기술자를 같이 → 자리: 흐름 밖: 수송 해석 규칙 (단계 7 해석) | §4.3 L229–237 | 표지 없음 | 액체 LIB

---

## 카드 문제

jeong2025_tough_adhesive_binder_shield_ncm811
1. 풀셀 손실 "≈35 %" (L255 · L368 · L448) ↔ 같은 줄에 적힌 판독값 2.4 → 1.7 · 2.2 → 1.6 mAh/cm² 는 약 29 % · 27 % 손실 (내 대조).
2. N5 최대 응력 두 값: §3b 표 UTS fr≈42.5 MPa (L95) ↔ Fig 1d 곡선 최대 fr≈46 MPa @≈15 % (L97) — 대표 곡선 vs 평균 막대일 수 있으나 카드에 설명 없음.
3. TOF-SIMS 시간 → 깊이 환산: L167 의 스퍼터 속도 (0.2 nm/s) × L175 의 시간 (≈2900 s · ≈1400 s) 이 카드가 적은 nm 범위의 아래쪽에 떨어짐 (nm 값은 인용 금지 표지 L434 라 숫자 생략).

jun2026_ppma_econductive_binder_si_lowpressure_assb
4. 메타 'methods:' 줄 (L10) 에 서론 분석 문장이 섞여 있고 'functional, md, mlip' 태그가 붙음 ↔ §10 L162 "계산 0 (DFT·MD·결합에너지·시뮬레이션 일절 없음)".
5. PVDF-Si 반쪽셀 (97:3 · 0.2C · 5 MPa) 용량 두 값: L80 · L130 초기 탈리튬화 2010 mAh/g (Fig 3a) ↔ L82 · L108 1820 mAh/g (Supp 1) — 측정 사이클 · 셀이 다른지 카드에 설명 없음.

kang2025_bollard_anchored_binder_dry_electrode
6. 카드 안의 '우리' PTFE 영률 두 값: L195 "우리 `PTFE 1.8 GPa` 와 ~500–1000× 차이" ↔ L709 "bulk PTFE ~0.3–0.5 GPa (우리 ADD dict 0.30 GPa) 와 1000× 차이".
7. SI 영상 사양 두 값: L367 "14.04 s · 10.04 fps · … ≈ 141 프레임" ↔ L411 "14.04 s @ 24 fps = 337 프레임" (L36 · L414 · L781–783 도 337).
8. §3a 표 (L82) 는 Fig 3b 양을 아직 "시트저항 [Ω cm⁻²]" 로 둠 ↔ §0b ⑩ (L39) · §3e (L166) · §10.1b ⑦ (L725) 는 Ω/□ 로 정정 — 정정이 표에 반영되지 않음.
9. L44 "문서 전체에 MPa/kPa/bar/psi/ton/kgf 가 한 번도 안 나온다" ↔ L195 필름 E 가 MPa (Fig 3e 그림에서만 읽힘 · 본문 텍스트에는 없음) — '문서 전체' 는 과한 표현.
10. PTFE 단독 MD 의 '뜬 거리' 두 값: L522 "(d) PTFE 장쇄만 — 표면에서 9 Å 뜸 / (e) … 3 Å" ↔ §4.7 · §4.10 Fig 4f 평균 거리 4.75 → 6.60 Å (≈1.9 Å 들뜸) — 지표 (스냅샷 vs 부분집합 평균) 가 다를 수 있으나 대응 설명 없음.

kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode
11. §9 인용 문장 (L337) 이 "a 2D COMSOL hyperelastic … model" 로 차원을 단정 ↔ 카드 본문은 [판독 — 차원 미기재] (L34 · L99).
12. '우리' 믹서 PTFE 서술 두 갈래: L288 "우리 믹서 조성 PTFE 1 wt% (make_mixer_deck.py WT)" ↔ L217 · L269 · L295 "믹서 DEM 은 PTFE 를 뺀 3 상" — 조성표 값과 덱의 상 구성이 구분돼 적히지 않음 (모순인지 미확인).

kawaguchi2017_dry_coating_parametric_na2so4_model_se
13. 제목 (L8) · §0 ④ (L29) · §9 인용 문장 (L215) 이 파쇄 조건을 "≤ 10 wt%" 로 단정 ↔ §3-5 L103 은 원문 "less than 10 wt%" 를 '10 wt% 이하' 로 읽은 것이 [추정] 이라고 적음.
14. "≤ 10 wt% 에서는 손실 없음" (L28) ↔ "거의 손실 없음" (L83) · 같은 카드 Table 1 Run 9 투입 10 → 순 9.2 wt% · Run 10 5 → 4.8 wt% — 논문 문장을 따른 요약이지만 표 값과 어긋나 보임 (kawaguchi2023 L229 · kawaguchi2017 L247 도 같은 요약을 재인용).

kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps
- 없음 (§0 ③ ⑤ ⑥ · §3-2 · §7-1 의 카드 산술을 표 1a · 2a 값으로 맞춰 봄 — 어긋남 없음).

kim2026_charge_engineered_cnf_binder
15. Minnmann 을 σ / porosity 절대 앵커로 적음 — L45 "σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann이 담당" · L64 · L345–346 "Minnmann(LPSCl cold-press)" · L396 · L425 — 그 출처는 철회됨 (순수 SE 기공 실험 앵커로 쓰면 안 됨).
16. Al₂O₃ MD 결합에너지 두 값: §3 L148 "c-CNF … −1193.8 kJ/mol" ↔ §5 L304 · §8 L417 "−1204.8" — L252 에 따르면 −1204.8 = 1 c-CNF · −1193.79 = 2 c-CNF 인데 요약마다 다른 쪽을 'c-CNF' 로 씀.
17. 고로딩 밀도: L116 · L175 "밀도 3.65 g/cm³ 유지하며 80 / 90 / 113 mg/cm²" ↔ L176 두께 225 / 260 / 320 µm 로 나누면 약 3.56 / 3.46 / 3.53 g/cm³ (내 대조 · 두께에 집전체가 들었는지 · 로딩이 활물질 기준인지 카드에 없음).
18. τ 대응: L327 "★ 우리 σ_ionic의 C(τ) 항과 같은 변수" ↔ 이 논문 τ 는 N_M = τ/ε (L235) 로 정의된 양 — 우리 쪽 τ 명명 규약 (제곱 / 제곱근) 과의 대조가 필요 (카드 안에서는 판정 불가 · 확인 필요).

카드 사이 (참고)
19. '우리' SDCP E_bind 표기가 카드마다 다름: kang2025 L590 (−4.797 eV doped · uma-s-1p1 / −3.02 neutral) ↔ jun2026 L200 (−1.52 eV · QE Phase-B doped preview · UMA 클린슬랩 챔피언 −5.196 eV) — 계산 판 · 방법이 달라 모순인지 미확인.

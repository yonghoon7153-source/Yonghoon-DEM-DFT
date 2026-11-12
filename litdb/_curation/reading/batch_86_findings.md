# batch 86 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-13)

대상: `greenwood1966_constriction_resistance_microcontact_cluster_real_area` — J. A. Greenwood, "Constriction resistance and the real area of contact", *Brit. J. Appl. Phys.* 17 (1966) 1621–1632 · DOI 10.1088/0508-3443/17/12/310 (PDF 1 쪽 IOP 표지 링크 · 스캔 쪽에는 인쇄 없음) (후보 표 N-46 · 가리킨 카드 = `pan2026_thesis_rate_capable_energy_dense_cathode_composites` L465).
정전기 대응 (전위론) 으로 두 반무한 도체 사이 미세접촉 군집의 협착 저항을 푼 이론 + 무차원 수치 배열 (~70 개 · 최대 120 점) + 금 Brinell 압흔의 표면 단면 한 장 · DEM · 입자 계산 · 역학 계산 없음.
쪽 = 인쇄 p.1621–1632 (PDF 쪽 = 인쇄 − 1619 · PDF p.1 = IOP 표지) · 판독 원자료 = `litdb/figures/greenwood1966_constriction_resistance_microcontact_cluster_real_area/digitized.csv` (152 행 · 그림 2 · 3 · 7).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE · 압력 · 기공 0 — 무차원 협착 이론).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (하중 · 탈압 0).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] greenwood1966_constriction_resistance_microcontact_cluster_real_area | 값 없음 · 경도의 뜻만: 하중 ÷ bulk 경도로 구한 면적 = **겉보기 면적** (저항 · 압흔 관찰과 맞음 · Bowden and Tabor 1954 인용) · 실면적은 그 작은 일부 — *"the use of the bulk hardness is wrong, and quite badly so"* · 하중에 비례한다는 실험 증거가 있는 것은 겉보기 면적 (*"it is doubtful whether there is* any *experimental evidence that the real area of contact is proportional to the load, but rather good experimental evidence that the apparent area is"*) | 카드 §3-8 · p.1630 · 그림 1 | [인쇄] | 금속 (금) · 하중 · 경도 값 [미확인] · 일축 항복 세기와의 환산 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (입자 · 하중 분담 0).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] greenwood1966_constriction_resistance_microcontact_cluster_real_area | (역학 법칙 아님 · 수송 쪽 대응) '접촉끼리 독립' 협착 (평행 항 ρ/2Σa 만) 이 깨지는 범위 = 군집 크기 l 이 반지름 합 Σa = nā 와 같은 자릿수 (상호작용 항 ≈ 2ρ/πl) · 10 점 배열 독립 0·106 ↔ 연립 해 0·174 (×1·64) · 대안 = 연립방정식 (3) (맞춘 값 0) · 근사식 (4) (변분 상한 · 맞춘 값 0) · 권장 식 (7) (경험 계수 3π²/32 하나 — *"cannot be derived rigorously"*) · 근사 오차 70 배열 절반 < 1 % · 최대 5 % · 예외 9·4 % 한 건 | 카드 §3-2 · §3-3 · §3-5 · p.1623–1626 · 그림 2 · 표 2 | [인쇄] · [카드 산술] (재현) | 반무한 두 몸 · 평행 군집 · 무차원 — 역학 (Hertz) 쪽의 같은 '독립 접촉' 가정은 `gonzalez2012_nonlocal_contact_confined_granular` · `giannis2021_stress_based_multicontact_dem`

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 0 — 격자가 협착을 해상하는지 볼 수송 해석 기준은 m 절).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] greenwood1966_constriction_resistance_microcontact_cluster_real_area | 3D 반무한 전위론 (점 상호 저항 1/s · 원판 자기 저항) 위의 **평면 (2D) 배치** · 면에 퍼진 군집은 상호작용이 점 수와 거의 무관 (Holm 반지름 15–100 점 9·17–9·91) · **선 위 배치는 상호작용이 점 수에 로그로 커진다** (반지름 1·0 고리 30 · 60 · 120 점 → 0·425 · 0·496 · 0·567 · *"it appears to increase logarithmically as expected theoretically"*) — 2D 계산을 3D 로 옮기는 말은 없다 | 카드 §3-6 · §4-4 · p.1628–1629 (각주 †) · 그림 4(e)(f) · 그림 5 표 | [인쇄] · 고리 값은 카드 재현 안 됨 ([카드 산술] 고른 고리 0·357 · 0·428 · 0·498 — 증분 0·071 만 같음) | 배치 차원 (면 ↔ 선) 의 효과이지 계산 차원 (2D ↔ 3D) 경고가 아니다

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (넘김 선례 0 — 조각난 접촉면을 수송으로 넘길 때의 규칙 (Holm 반지름) 은 m 절).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] greenwood1966_constriction_resistance_microcontact_cluster_real_area | 가압 쪽에 닿는 원문 한계: 저항으로는 실접촉 면적의 **상한**만 (*"impossible to deduce anything about the real area of contact directly from measurements of the constriction resistance, except an upper limit; and the actual value can be a small fraction of this"*) · 경도로 구한 면적은 실면적이 아니다 → 가압 중 접촉 면적 (F/H) 을 '실접촉' 이라 부르지 않는다 · 그 밖 = 연립방정식 (3) 은 작거나 멀리 떨어진 극한에서만 정확 (p.1624) · 식 (7) 계수 엄밀 유도 아님 (p.1626) · 경험 규칙은 선 배치에서 깨짐 (p.1629) | 카드 §11 · p.1624 · p.1626 · p.1629 · p.1630 | [인쇄] | 탈압 · 하중 이력 없음

## k — DEM 의 한계
- [k] greenwood1966_constriction_resistance_microcontact_cluster_real_area (Greenwood 1966 · Brit. J. Appl. Phys. 17, 1621–1632) | **말 없음** — DEM · discrete 0 회 (1966 · 입자 계산 없음).  수송 쪽 '접촉끼리 독립' 의 깨짐은 일반 형식으로 있다: *"When the microcontacts are far apart they will act independently and the current through each will be inversely proportional to its self-resistance"* (p.1623) · *"The resistance for the same contacts acting independently was only 0·106, showing the importance of the interaction term"* (p.1624) · *"The contacts are not acting independently since the currents are not proportional to the radii"* (p.1624) · 조건 = *"when the linear dimensions of the cluster are comparable with the sum of the linear dimensions of the contacts"* (p.1623) | 카드 §0-1 · §3-2 · §3-3 · §4-4 | [인쇄] | 반무한 두 몸 사이 한 군집 · 평행 전류 — 우리 접촉망 (유한 구 · 한 입자에 들고 나는 접촉) 은 원문 가정 밖 (*"We consider a single cluster which is small compared to the size of the nominal contact area and to the distance from any other cluster"* p.1622) → DEM 접촉망의 독립 가정 오차 크기 · 부호는 이 논문에서 못 얻는다

## l — 소성변형이 왜 어려운가
- [l] greenwood1966_constriction_resistance_microcontact_cluster_real_area (Greenwood 1966 · Brit. J. Appl. Phys. 17, 1621–1632) | 계산 없음 · 문장만: *"The mechanical area of contact is often very much less than that deducible from the bulk properties. The remarkable persistance of surface asperities during bulk plastic flow is well-known (Moore 1948, Greenwood and Rowe 1965): the consequence, that the real area of contact is a small fraction of that predicted from the bulk hardness (see figure 1), is usually ignored"* · 원인 (가공 경화 · 마찰 구속 · 표면 막의 전위 차단) 은 *"irrelevant"* · *"the use of the bulk hardness is wrong, and quite badly so"* · 우회 = 실면적을 몰라도 되게 — 전도에는 겉보기 면적이 맞다 (*"the resistance can be calculated in the usual way from the load, hardness and resistivity"*) · 맞춘 값 0 · 비용: 연립방정식이 *"rapidly becomes impracticable as the number of spots increases"* (최대 120 점) | 카드 §3-8 · §4-4 · p.1623 · p.1630 · 그림 1 | [인쇄] | 금속 (금 압흔 단면 한 장 · 하중 · 경도 [미확인]) · 입자 모양 변화 · 부피 보존 유동 · 탈압 계산 없음 · 원문 철자 'persistance'

## m — 받아들일 통찰
- [m] greenwood1966_constriction_resistance_microcontact_cluster_real_area | 무엇: **수송 쪽 해석 기준 넷 (결과 전 등록)** — 단일 원 R·σ·a = 0·5 (두 몸) / 0·25 (한 몸) · 표 2 76 점 배열 (간격 1 · a 0·02–0·5 → R 0·4226 · 0·2577 · 0·1581 · 0·1238 · 0·1012 — 식 (3) 으로 재현) · 그림 2 10 점 (0·174 · ×2 0·141 · ×½ 0·240 · 중심 = digitized.csv) · 맞닿은 육각 7 점 0·1790 (1 차) → STEP3 (CF 가지) 에서 기하 협착이 풀리는 격자 규칙 · 접촉망 Holm 간선 코드 점검 · 어디에: 단계 7 · 흐름 밖: STEP3 협착 해상도 · 접촉망 단위 시험 · 왜: 카드 §3-5 · §9 1 · p.1624–1626 · 표 2
- [m] greenwood1966_constriction_resistance_microcontact_cluster_real_area | 무엇: **'접촉끼리 독립' 의 정의역 표지 + 시험** — 독립은 군집 크기 l ≫ (4/π)Σa 일 때만 [카드 산술] · 우리 순수 SE 겹침 (⟨δ⟩ ≈ 지름 11 % → a ≈ 0·33–0·46 R · CN 3–7 → 한 입자 Σa ≈ 1–3 R ↔ 입자 2R [우리 · 카드 산술]) 은 상호작용이 독립 항과 같은 자릿수인 구간 → 3–7 구 군을 STEP3 로 풀어 독립 Holm + 원기둥 bulk 와 견준다 (최소 발열 원리: 시행 전류 저항 = 상한 → 점검) · 어디에: 후보 D0 · 흐름 밖: 접촉망 σ_ion · σ_e 정의역 · 왜: 카드 §3-2 · §7-1 · §9 2 · p.1623 · 그림 2
- [m] greenwood1966_constriction_resistance_microcontact_cluster_real_area | 무엇: **조각난 접촉면 → Holm 반지름** — 식 (8) α = (2R/ρ − 1/Σa)⁻¹ 또는 경험 규칙 (바깥 점마다 최근접 간격만큼 밖으로 둘러 등면적 원) · √(ΣA/π) 로 두지 않는다 · 저항에서 거꾸로 구한 면적 = 실면적의 상한 (표 2: 실면적 ×625 ↔ 저항 ÷4) · 어디에: 후보 B · 후보 A′ · 흐름 밖: MPM · FE 변형 접촉 · 거칠기의 수송 넘김 · 왜: 카드 §3-6 · §7-3 · p.1628–1630 · 표 2
- [m] greenwood1966_constriction_resistance_microcontact_cluster_real_area | 무엇: **막 · 선 접촉** — 절연 막에 작은 틈이 많으면 막 없는 것과 거의 같은 저항 (값 없음 · Cocks 1954 · Archard 1959 · 그림 4(d)) · 선 위 접촉은 상호작용 로그 증가 → 막 개구 · 섬유 접촉을 개구율 비례 · 반지름 하나로 두지 않고 개구 수 · 크기 분포를 함께 기록 · 어디에: 흐름 밖: Rint ② S1 PTFE 면 개구율 · 탄소 접합 · 왜: 카드 §3-6 · §3-8 · §9 4 · 5 · p.1629–1630

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] HOLM, R., 1929, *Wiss. Veröff Siemens-Werken*, 7 (2), 217–58. (원문 참고문헌 · 인쇄 그대로) | k · m — 군집 협착 식 (1) R = ρ(1/2na + 1/2α) 의 원전 · 원문이 *"rarely used … perhaps because it does not occur in Holm's more accessible publications"* 라 한 그 식 · 10 % 조건 (a < α/3n^½) 의 출처 후보 · 카드 §3-5 · §12 · §13-8 | litdb 확인: papers/ 파일 목록에 holm* 없음 · 'Holm 1929' · 'Wiss. Ver' grep 0 건 (wishlist 0 · S8 = N-46 행뿐)
- [n] HOLM, R., 1958, *Electric Contacts Handbook* (Berlin: Springer-Verlag). (원문 참고문헌 · 인쇄 그대로 · 책) | k · m — 단일 원 협착 식의 판본 · 우리 카드들이 인용하는 Holm 1967 (판이 다름) 과 대조 · 10 % 조건의 출처 후보 · 카드 §12 | litdb 확인: holm* 없음 · 'Electric Contacts' · 'Holm 1958' grep 0 건 (정본 카드들은 'Holm 1967' 만 인용)
- [n] GREENWOOD, J. A., and ROWE, G. W., 1965, *J. Appl. Phys.*, 36, 667. (원문 참고문헌 · 인쇄 그대로 · 제목 없음 = 서지 일부만) | l · c — 소성 유동 중 표면 요철이 남는다 → 실면적 ≪ 경도 면적 (원문 §4.3 의 근거) · 카드 §3-8 · §12 | litdb 확인: greenwood* = 이 카드뿐 · 'Greenwood and Rowe' · 'Rowe 1965' grep 0 건 (S8 의 'Rowe' 는 Rowe 1989 = 다른 논문)
- [n] MOORE, A. J. W., 1948, *Proc. Roy. Soc.*, 195, 231–44. (원문 참고문헌 · 인쇄 그대로 · 제목 없음 = 서지 일부만) | l — 요철 지속의 첫 근거 (Greenwood and Rowe 와 짝) · 카드 §3-8 · §12 | litdb 확인: moore* 없음 · 'Moore 1948' grep 0 건
- [n] ARCHARD, J. F., 1959, *Wear*, 2, 438–55. (원문 참고문헌 · 인쇄 그대로 · 제목 없음 = 서지 일부만) | m — 절연 막의 작은 틈이 많으면 막 없는 것과 거의 같은 저항 (원문 §4.3 의 인용) → PTFE · 코팅 막 개구 (Rint ② S1 · 흐름 밖) · 카드 §3-8 · §9 4 · §12 | litdb 확인: archard* 없음 · 'Archard' grep 0 건 (wishlist · S8 0 건)

## 카드 문제
- `pan2026_thesis_rate_capable_energy_dense_cathode_composites` L66 — 학위논문 p.5 *"Holm contact resistance formula R c = ρ / (2na)"* [22,23] — 원문 (= [22]) 에서 ρ/2na 는 **Holm 식 (1) 의 첫 항 (평행 · 독립) 뿐**이고 식 (1) 전체는 ρ(1/2na + 1/2α) (p.1622) · 원문의 요지는 첫 항만으로는 군집 저항이 작게 나온다는 것 (그림 2: 0·106 ↔ 0·174) · 단일 원 식은 ρ/2a (p.1621) — 카드는 학위논문 문장을 옳게 옮겼다 (카드 잘못 아님 · 학위논문의 인용 범위 문제) · 같은 산술의 L223 (1.9×) · L361 도 평행 항만 쓴 것 · 고치지 않음.
- `pan2026_thesis_rate_capable_energy_dense_cathode_composites` L465 — 이유 칸 *"카드 없음 — 다접촉 협착 (우리 Holm 망의 상호작용 항)"* — 서지 ✓ · 상호작용 항 ✓ · 단 원문의 상호작용은 **한 접촉 면 안 미세접촉 군집 (평행 전류)** 의 것이고 입자망의 서로 다른 접촉 사이 상호작용은 원문 가정 밖 (*"a single cluster which is small compared to … the distance from any other cluster"* p.1622) — 범위 한정 · 고치지 않음.
- `electromechanical_contact_model_particulate_systems` L36 — *"Greenwood/Renouf-Fillot Hertz 전기전도 [26,27]"* — 이 논문에는 Hertz (하중 → 면적) 식이 없다 · 그 카드의 [26] 이 이 논문인지 확인할 수 없다 ([미확인]) · 고치지 않음.
- (참고 · 문제 아님) `bielefeld2019_microstructural_modeling_composite_cathode` L74 · L177 (Bielefeld 2019 본문 p.1629 *"… a large number of interacting microcontacts"* — ref 36 = Greenwood 1966) · `bielefeld2020_effective_ionic_conductivity_binder` L141 · L506 (*"R∝1/(σ·r_c), Greenwood 1966 / Holm 1967"*) = 원문과 맞다.  'Greenwood' 를 적은 `jacksongreen2005_…` L22 · `kogutetsion2002_…` L17 · `morrissey2013_…` L275 · `thorntonyin1991_…` L402 는 다른 Greenwood 논문 (Greenwood–Williamson 1966 · Johnson–Greenwood 1997 · Greenwood–Johnson 1981).

<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-46 · 정독 86) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     수송 쪽 이웃 = bielefeld2020_effective_ionic_conductivity_binder.md (Holm/Greenwood 협착 표기) · bazzoun2026_dem_fem_rnm_ionic.md (RNM = Holm) · pan2026_thesis_rate_capable_energy_dense_cathode_composites.md (가리킨 카드).
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음 카드들과 같은 꼴.
     원문 = 출판본 스캔 (Brit. J. Appl. Phys. 17 (1966) 1621–1632 · 본문 12 쪽 + IOP 표지 1 쪽 = PDF 13 쪽 · 보충 자료 없음).
     쪽 표기 = 학술지 인쇄 쪽 "p.1621–1632" (PDF 쪽 = 인쇄 쪽 − 1619 · PDF p.1 = IOP 표지 · 논문 아님).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 152 행 — 쪽마다 1 비트 스캔 1876 × 2876 px ≈ 300 dpi 라 300 dpi 렌더 = 원 해상도 · 원 중심 = Kåsa 원 맞춤 · 곡선 = 눈금 보정 뒤 열마다 선 중심) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · 연립방정식 (3) 은 numpy 로 직접 풀었다) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 원문 12 쪽 전수에 없음.
     원문 12 쪽은 전 쪽 300 dpi 렌더로 읽었다 (OCR 글자층은 식 · 일부 낱말 · 숫자가 깨져 있어 (예: 'Table I.' · '1621' 머리) 숫자 · 식은 렌더에서만 옮겼다).
     DEM · 입자 계산 · 압밀 · 역학 계산은 없다 — 정전기 대응 (전위론) 으로 푼 협착 저항 이론 + 무차원 수치 배열 + 표면 단면 그림 한 장. -->
# 미세접촉 군집의 협착 저항 = 평행 항 ρ/2Σa + 상호작용 항 (미세접촉의 수 · 크기가 아니라 군집의 크기 = Holm 반지름 α 로 정해지는 ≈ ρ/2α) — 정전기 대응 · 자기 저항 ρ/4a · 점 상호 저항 ρ/2πs · 연립방정식 (3) · 최소 발열 시행 전류 상한 (식 4) · '접촉끼리 독립' 은 군집 크기 l ≫ Σa 일 때만 (그림 2: 독립 0.106 ↔ 연립 0.174) · 고차 근접 보정 ≤ 3 % · 저항으로 구한 면적은 실접촉 면적의 상한 (표 2: 저항 ÷4 ↔ 실면적 ×625) · 절연 막의 작은 틈이 많으면 막 없는 것과 거의 같다 — Greenwood (Br. J. Appl. Phys. 1966)

> slug `greenwood1966_constriction_resistance_microcontact_cluster_real_area` · DOI `10.1088/0508-3443/17/12/310` (스캔 쪽에는 인쇄 없음 — PDF 1 쪽 IOP 표지의 'View the article online' 링크 주석) · type `theory + numerical (constriction resistance of a cluster of microcontacts between two large conductors — electrostatic analogue · self rho/4a and point mutual rho/2pi s resistances · simultaneous equations (3) · minimum-heat trial-current bound (4) · Holm radius (8) · about 70 synthetic arrays up to 120 spots) + one Talysurf profile (Brinell impression · annealed gold) — no DEM · no particle simulation · no compaction` · PDF `32d38dce-46._Constriction_resistance_and_the_real_area_of_contact.pdf` · digested `2026-11-13` · status ✅
>
> **저자**: **J. A. Greenwood**† (단독) — Burndy Corporation Research Division, Norwalk, Connecticut, U.S.A. († *"Now at the Department of Mechanical Engineering, The University, Liverpool 3"*) — *Brit. J. Appl. Phys.* **1966**, **17**, **1621–1632** (쪽 머리 *"BRIT. J. APPL. PHYS., 1966, VOL. 17"* · 호 미인쇄 — DOI 경로 '17/12' 로 보아 12 호 [카드 해석]) · *"MS. received 20th June 1966, in revised form 25th July 1966"* · 감사 = Dr. J. H. Tripp · Dr. J. B. P. Williamson · 연구비 [미확인] (인쇄 없음).
> **이웃 카드 (링크만)**: [`pan2026_thesis_rate_capable_energy_dense_cathode_composites`](pan2026_thesis_rate_capable_energy_dense_cathode_composites.md) (가리킨 카드 · 학위논문 참고 [22] = 이 논문 · L66 · L465) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) (L141 · L506 "R∝1/(σ·r_c), Greenwood 1966 / Holm 1967") · [`bazzoun2026_dem_fem_rnm_ionic`](bazzoun2026_dem_fem_rnm_ionic.md) (RNM 접촉 R = 1/(2σr_c) · 전극 경계 1/(4σr_c) = 이 논문의 두 몸 · 한 몸 식) · [`ketter2025_resistor_network_models_predict_transport_properties`](ketter2025_resistor_network_models_predict_transport_properties.md) (복셀 RN · 협착 없음) · [`sangros2020_dem_electrical_conductive_paths_assb`](sangros2020_dem_electrical_conductive_paths_assb.md) (원기둥 R = ρl/A · 협착 없음) · [`nam2026_primer_layer_dry_electrode_collector`](nam2026_primer_layer_dry_electrode_collector.md) (전류 집중 ∝ A^−0.54 ↔ Holm 1/√A) · [`giannis2021_stress_based_multicontact_dem`](giannis2021_stress_based_multicontact_dem.md) · [`varkey2026_multicontact_elastoplastic_dem`](varkey2026_multicontact_elastoplastic_dem.md) (역학 쪽 'multi-contact' — 이름만 같다).
> **판독 원자료**: `litdb/figures/greenwood1966_constriction_resistance_microcontact_cluster_real_area/digitized.csv` (152 행 — 그림 2 원 10 개 중심 · 그림 3 점 76 개 배치 · 그림 7(a)(b) 곡선) · 그림 크롭 **39 장** (도구 4 장 전부 다시 자름 + 손 크롭 35 = 그림 4 · 패널 2 · 표 1 · 식 13 · 근거 문단 15) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 두 큰 도체 사이의 접촉이 실제로는 n 개의 작은 원형 미세접촉 군집일 때, 그 협착 저항은 **평행 항 ρ/(2Σa_i) (= 미세접촉끼리 독립이라고 둔 값) + 상호작용 항**이고 (식 (4) · (5) · (7) · p.1623 · p.1626), 상호작용 항은 미세접촉의 수 · 크기가 아니라 **군집의 크기**로 정해져 ρ/2α (α = Holm 반지름) 에 가깝다 (식 (1) · (8) · 초록 · p.1622 · p.1628).  군집의 크기 l 이 반지름의 합 Σa_i = nā 와 같은 자릿수가 되면 두 항이 같아지고 (p.1623), "접촉끼리 독립" 으로 계산한 값은 실제보다 크게 작다 — **그림 2 의 10 점 배열: 독립 0.106 ↔ 연립 해 0.174 (×1.64) · 간격 절반이면 0.240 (×2.26) [인쇄 · 비 = 카드 산술]** (p.1624).  거꾸로 저항에서 단일 원 가정으로 구한 면적은 **실접촉 면적의 상한일 뿐**이다 (표 2: 저항 ÷4.18 → 단일 원 가정 면적 ×16 ↔ 실면적 ×625 · p.1630).

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 단일 접촉 협착 식 (우리 Holm R = 1/(2σa) 의 원형) | 두 큰 도체가 반지름 a 원으로 닿으면 **ρ/2a** (*"very widely used"* · 인용 없이 표준식으로) · 한 몸만 보면 자기 저항 **ρ/4a** (Smythe 1950) · 같은 재료 두 몸 기준 — 비저항이 크게 다르면 *"the theory also applies to the high resistance member"* (각주 †) | [인쇄] p.1621 · p.1622 |
| ② ★ 다접촉 상호작용 항 (형식) | 점 근사 상호 저항 **b_ij ≈ ρ/2πs_ij** · 연립방정식 (3) **U/2 = (ρ/4)(I_i/a_i + (2/π)Σ_{j≠i} I_j/s_ij)** · 시행 전류 (독립 가정 I_i ∝ 1/b_ii) 를 최소 발열 원리에 넣은 **식 (4) R = ρ/(2Σa_i) + (ρ/π)(ΣΣ_{i≠j} a_ia_j/s_ij)/(Σa_i)²** = **상한** · 식 (5) (평균 반지름) · 권장 식 (7) (상호작용 × 3π²/32) | [인쇄] p.1622–1626 |
| ③ ★ '독립' 이 깨지는 조건과 크기 | *"When the microcontacts are far apart they will act independently"* (p.1623) · 상호작용 항 ≈ 2ρ/πl → **l ~ Σa_i = nā** 이면 평행 항과 같은 자릿수 (p.1623) · 그림 2 (n 10 · Σa 4.7 [카드 산술]): 독립 0.106 ↔ 0.174 · 간격 ×2 0.141 · ×½ 0.240 · 전류 비 I/a 0.89–1.39 (ρ = 1 · U = 1 에서 독립이면 모두 2 [카드 산술]) | [인쇄] p.1623–1624 · 그림 2 |
| ④ ★ 고차 (근접) 보정 | 자기 · 상호 저항의 오차 O(a³/s⁴) (쌍극) · O(a²/s³) (사중극) · 맞닿은 육각 7 점 (반지름 1.0) 에서도 전체 저항 변동 **3 %** (표 1) · 중심 간격 두 지름이면 **0.3 %** → 1 차 (점 상호 저항) 로 충분 | [인쇄] p.1625 · 표 1 |
| ⑤ ★ 면적 → 저항 (실접촉 ↔ 겉보기) | *"Whenever we have a reasonably large number of not-too-small contacts … the constriction resistance is close to that observed if the entire area of the cluster were in electrical contact"* · 저항 · 경도 · 눈으로 본 면적이 서로 맞는 것은 모두 겉보기 면적이라서 · 실면적은 그 작은 일부 (그림 1) · 저항으로는 실면적의 **상한**만 | [인쇄] p.1621 · p.1630 |
| ⑥ 막 · 틈 | 절연 막에 **작은 틈이 많으면 막 없을 때와 거의 같은 저항** (Cocks 1954 · Archard 1959 · 그림 4(d)) — 값 없음 | [인쇄] p.1630 |
| ⑦ ★ 해석 기준 배열 (결과 전 대조 · 단위 시험) | 표 2 (76 점 정사각 · 간격 1 · a 0.02–0.5 → R 0.4226 · 0.2577 · 0.1581 · 0.1238 · 0.1012) · 그림 2 (10 점) · 표 1 (육각 7 점) · 그림 5 (Holm 반지름 9.17–9.91) · 고리 각주 (30 · 60 · 120 점 → 0.425 · 0.496 · 0.567) — **[카드 산술] 식 (3) 을 직접 풀어 표 2 의 인쇄 숫자 전부와 표 1 1 차 행을 재현 · 그림 2 판독 배치로 0.1736 · 0.1403 · 0.2382 재현** | [인쇄] · [판독] · [카드 산술] |
| ⑧ 이 묶음의 네 질문 | DEM **없음** (1966) · 소성: *"The remarkable persistance of surface asperities during bulk plastic flow is well-known"* → 경도로 구한 면적은 실면적이 아니다 (계산 없음) · 3D 반무한 전위론 위의 평면 (2D) 배치 · 탈압 **없음** | [인쇄] p.1630 |

⛔ **한정어 (떼지 말 것)**: ① 원문의 기하 = **반무한 두 도체 사이의 한 군집** — *"We consider a single cluster which is small compared to the size of the nominal contact area and to the distance from any other cluster"* (p.1622) · 미세접촉의 전류는 **모두 같은 방향 (평행)** 이다.  유한 입자 · 들고 나는 전류 · 한 입자의 서로 다른 면에 있는 접촉 (우리 접촉망) 은 원문 **밖**이다 ② 같은 재료 두 몸 (다른 비저항은 각주 한 줄) ③ 수치는 무차원 — *"they must be multiplied by the resistivity expressed in appropriate units"* (p.1624) ④ 식 (7) 의 3π²/32 는 *"cannot be derived rigorously … found only by combining mathematics and physics"* (p.1626) — 경험 계수 하나 ⑤ 실험은 금 Brinell 압흔의 표면 단면 한 장 (하중 · 경도 · 압흔 지름 [미확인]) — 재료 물성 앵커 없음.
⇒ **절대값 전이: 0 건 (재료 값이 없다).**  옮겨지는 것은 **식 · 꼴 · 해석 기준** — ρ 를 곱한 무차원 Laplace 해이므로 이온 · 전자 · 열 수송에 수학적으로 같다 [카드 해석 — 원문은 전기만 말함].  **우리 입자망 (유한 구 · 직렬) 의 상호작용 크기 · 부호는 이 논문에서 옮길 수 없다** (기하가 다르다).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-46 의 '왜' 칸)

의도 원문: *"k (수송 쪽) · m — '접촉끼리 독립' 가정: 다접촉 협착의 상호작용 항 · 우리 Holm 망은 접촉마다 독립 직렬 (pan2026 L465 '카드 없음 — 다접촉 협착 (우리 Holm 망의 상호작용 항)')"* (가리킨 카드 = `pan2026_thesis_rate_capable_energy_dense_cathode_composites` L465 · 정독 배치 b35)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "k (수송 쪽)" — DEM 한계 가운데 수송 쪽 (접촉끼리 독립 가정) | **일부** | 원문은 DEM 을 말하지 않는다 (1966 · 입자 계산 0) · 대신 **독립 가정이 깨지는 조건과 크기**를 식 · 수치로 준다: *"When the microcontacts are far apart they will act independently and the current through each will be inversely proportional to its self-resistance"* (p.1623) · *"The resistance for the same contacts acting independently was only 0·106, showing the importance of the interaction term"* (p.1624) · *"The contacts are not acting independently since the currents are not proportional to the radii"* (p.1624) · 조건 l ~ Σa_i = nā (p.1623) — 단 **반무한 두 몸 사이 평행 군집** 한정 · 압력 · 온도 · 재료 조건 없음 (무차원) |
| "m" — 받을 통찰 | **채움** | §8 · §9: 해석 기준 배열 (표 2 = 식 (3) 으로 정확 재현) · 변분 상한 (식 (4)) · 겉보기 면적 규칙 (Holm 반지름 · 경험 규칙) · 막 틈 · 선 배치 로그 증가 |
| "'접촉끼리 독립' 가정: 다접촉 협착의 상호작용 항" | **채움** (한 군집 안 미세접촉 사이) | 상호 저항 b_ij ≈ ρ/2πs_ij (p.1622) · 식 (3)–(8) · 상호작용 항 = 군집 크기로 정해짐 (초록 · §3.1–3.2) · 고차 근접 보정 ≤ 3 % (표 1 · p.1625) |
| "우리 Holm 망은 접촉마다 독립 직렬" | **일부** (형식 · 도구만 · 우리 기하의 값 없음) | 원문은 **다른 군집 (= 다른 접촉) 사이 상호작용을 가정으로 뺐다** (p.1622 위 인용) · 평행 전류만 · 유한 입자 · 직렬 (들어오고 나가는 전류) 없음 → 우리 망에서 한 입자에 붙은 접촉끼리의 상호작용은 크기도 부호도 이 논문에서 못 얻는다 [카드 해석 — 같은 쪽 면에서 같은 방향이면 저항 ↑ (원문) · 들고 나는 접촉 사이면 상호 전위가 반대 부호로 들어가 저항 ↓ 쪽 (원문에 없는 추론)] |
| "(pan2026 L465 '카드 없음 — 다접촉 협착 (우리 Holm 망의 상호작용 항)')" | **채움** (카드 없음 해소) · 범위 한정 | 서지 ✓ (저자 · 제목 · 권 17 · 1621–1632 · 1966) · DOI = PDF 1 쪽 IOP 표지 링크 `10.1088/0508-3443/17/12/310` (스캔 쪽에는 인쇄 없음) · 원문의 '상호작용 항' 은 한 접촉 면 안 군집의 것 (위 행) |

**가리킨 카드 · 같은 논문을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 정독 출력 batch_86 의 "카드 문제" 로):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `pan2026_…` L465 (학위논문 참고 22) | *"J.A. Greenwood, Constriction resistance and the real area of contact, Br. J. Appl. Phys. 17 (1966) 1621–1632."* · 이유 *"카드 없음 — 다접촉 협착 (우리 Holm 망의 상호작용 항)"* | 서지 ✓ · 상호작용 항 ✓ — 단 원문의 것은 한 접촉 면 군집 안 (평행) | **채움** (범위 한정) |
| `pan2026_…` L66 | 학위논문 p.5 *"Holm contact resistance formula R c = ρ / (2na)"* [22,23] · n = 접촉 수 · a = 접촉 반지름 | 원문에서 ρ/2na 는 **Holm 식 (1) 의 첫 항 (평행 · 독립) 뿐** — 식 (1) 전체는 ρ(1/2na + 1/2α) (p.1622) · 원문의 요지는 첫 항만으로는 군집 저항이 작게 나온다는 것 (그림 2 · 표 2) · 단일 원 식은 ρ/2a (p.1621) | **일부** — 카드는 학위논문 문장을 옳게 옮겼다 (카드 잘못 아님) · 학위논문의 [22] 인용이 상호작용 항을 뺐다 |
| `pan2026_…` L223 (§3-2-9 Holm 산술 1.9×) · L361 (비교표) | R = ρ/(2na) · a = 점당 접촉 길이 절반 → CB thin / Hybrid mid ≈ 1.9× | 평행 항만 쓴 비 — 상호작용 항 (≈ ρ/2α · α = 군집 크기) 을 넣으면 α 가 비슷한 두 시료의 비는 1 쪽으로 줄어든다 [카드 해석 · 2D 단면의 탄소 접촉을 평면 군집으로 본 가정] → 그 카드의 판단 (Holm 협착 ≠ EIS R2) 은 오히려 강해진다 | 참고 (카드 잘못 아님) |
| `bielefeld2020_…` L141 · L506 | *"constriction resistance, R∝1/(σ·r_c), Greenwood 1966 / Holm 1967"* | p.1621 ρ/2a = 1/(2σa) ✓ | **채움** |
| `bielefeld2019_…` L74 · L177 (+ L18 · L20 · L160 · L239 · L276) | Bielefeld 2019 본문 p.1629 인용 *"… constriction resistances … regarded as a large number of interacting microcontacts"* — ref 36 = Greenwood 1966 · "constriction = future work" | 원문 주제 (서로 상호작용하는 미세접촉 군집의 협착) 와 같다 ✓ — 단 원문의 미세접촉은 **한 접촉 면 안 군집 (평행 전류)** 이고 입자–입자 계면 사이의 상호작용은 원문 가정 밖 (p.1622) | **채움** (범위 한정) |
| `bielefeld2020_…` L42 · L51 · L150 · L396 · L471 · `shi2019_…` L698 · `lee2024_multiphysics_…` L170 · `taufactor_…` L111 · L164 · L198 · `wet_processing_…` L77 · L162 · L227 · L282 | "constriction = future work (Greenwood 1966)" · "점접촉 구속저항 (Holm/Greenwood) 없음 → σ_eff 상한" | 이 논문이 협착 이론의 출처라는 점은 맞다 · 옮긴 값 없음 | 대조할 값 없음 (이름만) |
| `electromechanical_contact_model_particulate_systems` L36 | *"Greenwood/Renouf-Fillot Hertz 전기전도 [26,27]"* | 이 논문에는 Hertz (하중 → 면적) 식이 없다 — 그 카드의 [26] 이 이 논문인지 [미확인] | 확인 불가 |

⇒ **의도 대조 결과: 일부** — 다접촉 협착의 상호작용 항 (형식 · 식 · 크기 · 깨짐 조건 · 해석 기준 배열) 은 **채움**; 그러나 그것은 반무한 두 몸 사이 한 군집 (평행 전류) 의 것이고, 우리 Holm 망 (유한 입자 · 직렬 · 다른 면의 접촉) 의 상호작용 값은 원문 가정 밖이라 **없음**; DEM 의 한계를 직접 말한 문장은 **없음** (수송 쪽 독립 가정의 깨짐만 일반 형식으로).

---

## 1. 한 줄 요약
접촉 이론에서 쓰는 단일 원 협착식 ρ/2a 는 실제 금속 접촉 (많은 미세접촉의 군집) 에 맞지 않는다는 문제의식에서, 전류 문제를 정전기 문제로 바꿔 (미세접촉 = 원판 도체 · 전류 = 전하) 자기 · 상호 저항으로 군집의 저항을 구하는 연립방정식 (3) 과, 그것을 피하는 근사식 (4) · (5) · (7) 을 세우고, 70 개쯤의 배열에서 정확도를 확인했다 (절반이 1 % 안).
결과: 군집 저항 = 평행 항 + 군집 크기로 정해지는 상호작용 항 ≈ Holm 의 1929 식 ρ(1/2na + 1/2α) · α (Holm 반지름) 는 점이 10–15 개를 넘으면 거의 일정 · 그래서 저항은 군집 전체가 닿은 것과 비슷하고, 저항 · 경도 · 압흔 관찰로 구한 면적이 서로 맞는 것은 모두 겉보기 면적이기 때문이며 실면적은 그보다 훨씬 작을 수 있다.
저자의 결론: *"Thus it is impossible to deduce anything about the real area of contact directly from measurements of the constriction resistance, except an upper limit; and the actual value can be a small fraction of this"* (p.1630).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **J. A. Greenwood** (Burndy Corp. Research Division, Norwalk CT · † Liverpool 대 기계공학과) | Brit. J. Appl. Phys. **17** (1966) **1621–1632** | 10.1088/0508-3443/17/12/310 (IOP 표지 링크) | 일반 도체 (비저항 ρ · 무차원 해) · 실험 그림 1 = *"annealed bead-blasted gold block"* 의 Brinell 압흔 | 이론 (전위론 · 정전기 대응) + 수치 배열 (~70 개 · 최대 120 점) + 표면 단면 한 장 |

- **1저자 메모 (후보 표 N-46) 와의 대조**: 저자 · 제목 · 학술지 · 권 17 · 쪽 1621–1632 · 1966 — **같다**.  덧붙임 ① DOI = `10.1088/0508-3443/17/12/310` (후보 표의 *"DOI 카드에 없음"* — 스캔에는 인쇄되지 않았고 PDF 1 쪽 IOP 표지의 링크 주석에만 있다) ② 호 = 12 (DOI 경로에서 · 인쇄 없음 [카드 해석]) ③ 원고 접수 1966-06-20 · 수정 1966-07-25.  PDF 문서 정보 (Title · Author) 는 비어 있다 (지시서의 *"Title: · Author:"* 빈칸과 같음).
- **글의 꼴**: 초록 → 1 서론 (그림 1 · 식 (1)) → 2 수학적 접근 (식 (2) · (3)) → 2.1 근사식 (식 (4) · (5)) → 2.2 전형적 군집 (그림 2) → 2.3 기본 방법의 정확도 (표 1) → 3 물리적 해석 → 3.1 Holm 의 식 (식 (6) · (7) · 그림 3 · 표 2) → 3.2 일반 군집의 Holm 반지름 (식 (8) · 그림 4–6) → 4 논의 → 4.1 정확도 (그림 7) → 4.2 협착 저항과 실접촉 면적 → 4.3 하중과 실접촉 면적 → 감사 → 부록 (두 원형 접촉의 상호작용) → 참고문헌 11 (+ 본문의 Cocks 1954 학위논문).  그림 7 · 표 2 · 번호 식 (1)–(8) (식 (1) 은 p.1625 에 다시) · 보충 자료 없음.
- **맥락** [카드 해석]: 같은 해 같은 저자의 Greenwood–Williamson (1966, Proc. R. Soc., 거친 면의 접촉) 과는 **다른 논문**이다 (정본 `kogutetsion2002_ep_sphere_rigid_flat` L17 의 *"GW (Greenwood–Williamson 1966 [5])"* 는 그쪽) — 이 논문은 접촉 역학이 아니라 접촉이 주어진 뒤의 **전류 (협착)** 만 다룬다.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 단일 접촉 · 자기 저항 · 상호 저항 (p.1621–1622 · `txt_p2_intro_single_spot_rho_2a.png` · `txt_p3_electrostatic_analogy.png` · `txt_p3_self_mutual_resistance.png`)
| 항목 | 식 · 값 | 표지 · 쪽 |
|---|---|---|
| 두 큰 도체가 반지름 a 원으로 닿을 때 | **R = ρ/2a** — *"This equation is very widely used in the design and study of electrical contacts"* (인용 없음) | [인쇄] p.1621 |
| 그 식의 한계 | *"There is evidence, however, that contact between metals rarely, if ever, occurs in this way"* · Brinell 압흔의 겉보기 면적이 *"subdivided into a multitude of microcontacts"* (그림 1) | [인쇄] p.1621 |
| 군집의 생김새 | 평평한 면끼리의 접촉 = 미세접촉 군집 여럿 (Dyson and Hirst 1954) — 군집 위치 = 큰 규모 물결 (waviness) · 미세접촉 = 작은 규모 거칠기 | [인쇄] p.1621 |
| 풀이 방법 | *"Current-flow problems are completely analogous to electrostatic charge distribution problems"* — 접촉 = 원판 도체 · 전류 = 전하 · 같은 전위 조건 → 연립방정식 (Smythe 1950) | [인쇄] p.1622 |
| 계 | 군집 하나 (공칭 접촉 면적 · 다른 군집과의 거리보다 작다) · n 개 미세접촉 · k 번째 전류 I_k · b_ij = 접촉 j 에 단위 전류 · 나머지는 등전위 (전류 0) 일 때 접촉 i 의 전위 (무한원 기준) — i ≠ j 상호 저항 · i = j 자기 저항 | [인쇄] p.1622 |
| 자기 저항 (한 몸) | **b_ii = ρ/4a_i** (*"We consider the situation in one of the contacting bodies only"*) — 다른 등전위 면이 있으면 전류가 재분배되어 달라지나 이 절에서는 무시 (§2.3 에서 다룸) | [인쇄] p.1622 |
| 상호 저항 (점 근사) | 접촉 j 에서 거리 s 의 전위 ρI_j/2πs (정전기의 ½Q/s) → **b_ij ≈ ρ/2πs_ij** | [인쇄] p.1622 |
| 두 몸 · 다른 비저항 | 같은 재료 두 몸이면 전위는 걸린 전위차의 절반 (U/2) · *"With some obvious minor changes, the theory also applies to the high resistance member of contact between conductors of very different resistivities"* (각주 †) | [인쇄] p.1622 |

[카드 산술] 단일 원: 두 몸 R = 2 × ρ/4a = ρ/2a ✓ · σ = 1/ρ 로 쓰면 **1/(2σa) = 우리 접촉망의 Holm 식** [우리 · CLAUDE.md · `bazzoun2026_dem_fem_rnm_ionic` 식 8 같은 꼴] · 한 몸 ρ/4a = Bazzoun 전극 경계 1/(4σr_c) [다른 카드 · 그 카드 L36].

### 3-2. ★ 연립방정식 · 근사식 (식 (2)–(5) · p.1622–1623 · `eq_02_…` · `eq_03_…` · `eq_04a_…` · `eq_04_…` · `eq_05_…` · `eq_05b_…`)
- (2) **φ_i = Σ_j b_ij I_j** · 원형 점 배열이면 **φ_i = (ρ/4)(I_i/a_i + (2/π) Σ_{j≠i} I_j/s_ij)**.
- (3) 같은 재료 두 몸 사이 군집: 모든 φ_i = U/2 → **U/2 = (ρ/4)(I_i/a_i + (2/π) Σ_{j≠i} I_j/s_ij)** (i = 1…n) — I_i 를 풀면 R = U/ΣI_i.  *"exact in the limits as the microcontacts become smaller or infinitely separated"* (p.1624).
- 최소 발열 원리: 실제 전류 분포는 발열 W 를 최소로 하는 것 → W 는 전류 추정이 조금 틀려도 둔감 (정류점).  **W = 2Σ_i φ_iI_i = 2Σ_iΣ_j b_ij I_iI_j** (2 = 대칭인 두 몸).  독립 가정의 시행 전류 **I_i ≈ λ/b_ii** → I = λΣ1/b_ii · W = 2λ²ΣΣ b_ij/(b_ii b_jj) → **R = W/I² = 2(ΣΣ b_ij/(b_ii b_jj))/(Σ1/b_ii)²**.
- (4) b_ii = ρ/4a_i · b_ij = ρ/2πs_ij 를 넣으면 **R = ρ/(2Σa_i) + (ρ/π)(ΣΣ_{i≠j} a_ia_j/s_ij)/(Σa_i)²** — *"From the minimum property of the heat production it follows that this will give an overestimate of the resistance"* · 연립방정식 (*"which rapidly becomes impracticable as the number of spots increases"*) 을 합만으로 피한다.
- (5) 크기와 위치가 상관없으면 이중합의 반지름을 평균으로: **R ~ ρ/(2Σa_i) + (ρ/πn²) ΣΣ_{i≠j} 1/s_ij** — 같은 크기면 (4) 와 같음 · 다르면 오차 부호는 어느 쪽이든 *"usually again an overestimate"*.
- 해석 (p.1623): *"The first term in both approximations is the usual expression for the resistance of a number of contact spots in parallel; it ignores their positions. To this is added a term which expresses the interaction between the spots"* · 크기 l 인 군집에서 점 쌍의 평균 거리 ~½l → 이중합 ≈ n(n−1)·2/l → n 이 크면 둘째 항 **≈ 2ρ/πl** → **l ~ Σa_i = nā** 이면 첫 항과 같은 자릿수 (*"when the linear dimensions of the cluster are comparable with the sum of the linear dimensions of the contacts"*).
- [카드 산술] 둘째/첫째 항 비 ≈ (2/πl)/(1/(2Σa)) = 4Σa/(πl) — 독립 (둘째 항 무시) 이 되려면 **l ≫ (4/π)Σa** 이어야 한다: 점 사이 간격 s 가 반지름 a 보다 크다는 것만으로는 부족하고 **군집 크기가 반지름 합보다 커야** 한다.

### 3-3. ★ 그림 2 — 무작위 10 점 배열 (p.1624 · `fig_2.png` · `txt_p5_random_array_results.png` · `txt_p5_70_arrays_errors_basic_method.png` · digitized.csv fig2)
| 접촉 | a | b | c | d | e | f | g | h | i | j |
|---|---|---|---|---|---|---|---|---|---|---|
| 반지름 a [인쇄] | 0·6 | 0·3 | 0·8 | 0·5 | 0·2 | 0·5 | 0·6 | 0·7 | 0·4 | 0·1 |
| 전류 I [인쇄] | 0·836 | 0·317 | 1·036 | 0·513 | 0·178 | 0·638 | 0·758 | 0·888 | 0·445 | 0·129 |
| I/a [인쇄] | 1·39 | 1·06 | 1·29 | 1·03 | 0·89 | 1·28 | 1·26 | 1·27 | 1·11 | 1·29 |

- 저항 [인쇄 p.1624]: 연립 해 **0·174** · 식 (4) **0·175** (0·7 %) · 식 (5) **0·179** (2·9 %) · 독립 **0·106** · 거리 ×2 → **0·141** (오차 0·2 · 1·6 %) · 거리 ×½ → **0·240** (2·1 · 5·3 %) · *"A further decrease in separation would be meaningless, since the contacts have already begun to overlap"*.
- 전류 분배: *"Contact a carries an unduly high current while e carries an unduly low one … a is the most isolated contact and e the most enclosed"*.
- 70 배열 [인쇄 p.1624]: *"half the errors are less than 1 % using either approximate formula: larger errors, up to 5 %, occur only in extreme cases … such as the array containing touching spots"* · 5 % 를 넘은 것은 한 건 — 식 (5) 로 **9·4 %** (그림 2 자리에 b–j 반지름 0·5 · a 반지름 2·0).
- [카드 산술] Σa = 4·7 → 독립 ρ/(2Σa) = 0·1064 ✓ · ΣI = 5·738 → 1/ΣI = 0·1743 ✓ (= 인쇄 0·174 → 표의 전류는 ρ = 1 · U = 1 정규화) · 독립이면 I/a = 2 (식 (3) 에서 s → ∞) 인데 0·89–1·39 → 미세접촉마다 전류가 30–55 % 깎였다 · 연립/독립 = **1·64** · ×2 에서 1·33 · ×½ 에서 2·26.
- **[판독 + 카드 산술] 재현**: 원 10 개의 중심을 Kåsa 원 맞춤으로 읽고 (반지름 맞춤 ≤ ±0·011 · 축척 75·88 px/단위 @300 dpi) 인쇄 반지름으로 식 (3) 을 풀면 **R 0·1736** (인쇄 0·174) · 전류 0·842 · 0·319 · 1·035 · 0·514 · 0·178 · 0·640 · 0·761 · 0·894 · 0·446 · 0·130 (인쇄와 차 ≤ 0·006) · ×2 **0·1403** (0·141) · ×½ **0·2382** (0·240) · 식 (4) · (5) 의 오차 +0·7 · +2·9 % (×1) · +0·2 · +1·6 % (×2) · +2·1 · +5·3 % (×½) — 인쇄와 **같다**.  식 (7) 이면 −0·3 · −0·4 · +0·7 %.

### 3-4. ★ 고차 근접 보정 · 표 1 (p.1625 · `tab_1.png` · `txt_p6_higher_order_dipole_quadrupole.png` · `txt_p6_table1_resistance_insensitive.png` · 부록 `eq_A1_…` · `eq_A2_…`)
- 오차의 크기: 두 접촉의 자기 · 상호 저항 오차 = **O(a³/s⁴) (쌍극 — 다른 접촉에 유도된 전하가 자기 전위를 바꿈) · O(a²/s³) (사중극 — 전하가 면에 퍼짐)** · n 접촉이면 모든 쌍의 사중극 · 모든 세 쌍의 쌍극 → 일반적으로 다 넣기 어렵다.
- **표 1** (육각 7 점 = 그림 4(a) · 반지름 1·0 · 맞닿음) [인쇄]:

| 근사 | 가운데 전류 | 바깥 전류 | 전체 저항 |
|---|---|---|---|
| 1 차 (s⁻¹ 까지) | 0·3259 | 0·8765 | 0·1790 |
| 사중극 (s⁻³) | 0·2122 | 0·8641 | 0·1853 |
| 쌍극 (s⁻⁴) | 0·4254 | 0·8587 | 0·1743 |

- 저자: *"The dipole effects more than outweigh the quadrupole effects … the overall resistance is insensitive to the inclusion of the higher terms. It varies only by 3 % in an example which has the maximum possible number of touching neighbours"* · 중심 간격 두 지름이면 *"0·2529, 0·2538 and 0·2521 which vary by only 0·3 %"*.
- [카드 산술] 식 (3) 을 7 점에 풀면 (대칭으로 2 × 2): 가운데 **0·3259** · 바깥 **0·8765** · R **0·17904** — 1 차 행 **정확히 재현**.  R = 1/(I_가운데 + 6 I_바깥) 로 각 행을 검산하면 0·1790 ✓ · 0·1853 ✓ · **0·1793 ≠ 인쇄 0·1743** — 쌍극 행의 세 숫자가 서로 맞지 않는다 (어느 숫자의 인쇄 오류인지 [미확인]).  두 지름 예: 반지름 1·0 이면 1 차 R = 0·1260 · 반지름 0·5 (중심 간격 2) 이면 **0·2521** — 인쇄 셋은 반지름 0·5 축척과 맞고 1 차 값은 셋째 수와 같다 (원문은 그 예의 반지름 · 값의 순서를 적지 않았다).
- 부록 (p.1631): 두 같은 원 (반지름 a · 간격 s) 의 **C⁻¹ = ½(π/2a + 1/s + a²/3s³ − 4a³/3πs⁴ + …)** · 협착 저항 **(ρ/π)C⁻¹** → [카드 산술] 앞 두 항 = ρ/4a + ρ/2πs = 식 (5) 의 n = 2 와 같다 · 맞닿은 두 원 (s = 2a) 에서 뒤 두 항의 몫 **+0·7 %**.

### 3-5. ★ Holm 의 식 · 균일 군집 · 표 2 (§3.1 · p.1625–1626 · `eq_01_…` · `eq_06_…` · `eq_07_…` · `fig_3.png` · `tab_2.png` · `txt_p7_both_limits_table2_setup.png` · `txt_p7_interaction_large_vs_small_self.png`)
- **식 (1)** (Holm 1929): 반지름 α 원 안에 같은 작은 점 n 개가 고르고 빽빽하면 **R = ρ(1/2na + 1/2α)** — *"this equation is rarely used — a notable exception being Cocks (1954 Ph.D. Thesis, University of Reading) — perhaps because it does not occur in Holm's more accessible publications (e.g. Holm 1958)"* (p.1622).
- 식 (5) 를 평균 반지름 ā 로: R = ρ/2nā + (ρ/πn²)ΣΣ1/s_ij → 반지름 α 원 안 균일 분포의 역거리 합 **ΣΣ1/s = 16n²/3πα** (Timoshenko and Goodier 1951) → **식 (6) R = ρ(1/2nā + 16/3π²α)** · *"Since 16/3π² = 0·5404, this is seen to be close to Holm's result"* (½).  차이의 뜻: (16/3π²)ρ/α = 반지름 α 원판에 **전류가 고르게 흐르도록 강제했을 때** (Rayleigh 1871) · 자유롭게 분포하면 ρ/2α — 식 (1) 은 자기 저항이 작을 때 · (6) 은 클 때 맞다 (p.1626).
- **표 2** (그림 3 배열 · 간격 1 · 같은 자리에서 반지름만 바꿈) [인쇄]:

| a | R (연립) | 1/2na | 상호작용 R − 1/2na | Holm 반지름 α (식 8) | 같은 저항 단일 원 반지름 |
|---|---|---|---|---|---|
| 0·02 | 0·4226 | 0·3289 | 0·0937 | 5·34 | 1·18 |
| 0·04 | 0·2577 | 0·1645 | 0·0932 | 5·36 | 1·94 |
| 0·1 | 0·1581 | 0·0658 | 0·0923 | 5·42 | 3·16 |
| 0·2 | 0·1238 | 0·0329 | 0·0909 | 5·50 | 4·04 |
| 0·5 | 0·1012 | 0·0132 | 0·0880 | 5·68 | 4·94 |

- 저자 (p.1626): 자기 저항이 크면 상호작용 ≈ 식 (5) 값 (πn²)⁻¹ΣΣs⁻¹ = **0·0941** · 접촉이 맞닿으면 거의 **3π²/32** 배로 줄어 (**0·0870**) 식 (6) → 식 (1) · 변화가 작아 무시할 수 있지만 상호작용이 지배할 때 맞게 잡는 것이 중요하므로 **식 (7) R = ρ(1/2Σa_i + (3π/32n²)ΣΣ1/s_ij)** 를 권장 — *"This cannot be derived rigorously by the present approach: it has been found only by combining mathematics and physics"*.
- [카드 산술 · 판독] 그림 3 의 점을 세면 행마다 4 · 6 · 8 · 10 · 10 · 10 · 10 · 8 · 6 · 4 = **76 개** (= 1/(2·0·02·0·3289) = 76·0 ✓) · 이 배치 (간격 1 · 반정수 격자) 로 식 (3) 을 풀면 **표 2 의 R · Holm 반지름 · 단일 원 반지름이 인쇄 자릿수까지 전부 같고** (R 0·422607 · 0·257749 · 0·158051 · 0·123799 · 0·101202 → 0·4226 · 0·2577 · 0·1581 · 0·1238 · 0·1012) 상호작용은 a 0·04 에서만 끝자리 1 차이 (0·093275 → 0·0933 ↔ 인쇄 0·0932 = 반올림한 R 에서 1/2na 를 뺀 값과 같다) · ΣΣ1/s = 1707·0 → 식 (5) 상호작용 0·0941 ✓ · × 3π²/32 (= 0·9253) = 0·0871 ✓.  근사식 오차 (이 배열): 식 (5) **+0·1 · +0·3 · +1·1 · +2·6 · +5·9 %** (a 0·02 → 0·5 · 맞닿을수록 커짐) · 식 (7) **−1·6 · −2·4 · −3·4 · −3·2 · −1·0 %** — 이 정사각 배열에서 식 (7) 의 오차는 §4.1 의 *"less than 1 %"* 보다 크다 (그 말의 '보통의 경우' 범위는 원문에 없다).  그림 3 의 그림은 a ≈ 0·1 의 경우로 보인다 (점 ≈ 0·1 칸 · 빗금 원 ≈ 3·0–3·2 칸 ↔ 3·16 · 바깥 원 ≈ 5·4–5·5 칸 ↔ 5·42 [판독 ±3 %] · 캡션은 a 를 적지 않았다).
- [카드 산술] 표 2 의 a 0·02 → 0·5: 실면적 (0·5/0·02)² = **625 배** · 저항 0·4226/0·1012 = **4·18 배** 감소 · 같은 저항 단일 원 면적 (4·94/1·18)² = **17·5 배** (본문 *"suggesting … the area had increased 16 times, whereas in fact it had increased by a factor of 625"* — p.1630).

### 3-6. ★ Holm 반지름 · 그림 4–6 · 선 배치 (§3.2 · p.1627–1629 · `eq_08_…` · `fig_4.png` · `fig_5.png` · `fig_6.png` · `txt_p10_holm_radius_rule_of_thumb.png` · `txt_p10_footnote_line_ring_log_growth.png`)
- **식 (8) α = (2R/ρ − 1/Σa_i)⁻¹** — 식 (1) 이 주어진 저항을 내도록 하는 α = *"Holm radius"* (p.1628).
- *"When the number of contacts is small they do not form a well-defined cluster and the Holm radius is large. As the number of spots increases, a definite Holm radius emerges, and varies little as the area of the cluster is filled up"* (p.1628).
- **그림 5 의 표** [인쇄]: 점 수 5 · 10 · 15 · 20 · 30 · 40 · 50 · 60 · 70 · 80 · 90 · 100 → Holm 반지름 **10·73 · 8·75 · 9·17 · 9·78 · 9·73 · 9·71 · 9·76 · 9·91 · 9·60 · 9·57 · 9·64 · 9·63** — [카드 산술] 15 점부터 100 점까지 9·17–9·91 (가운데 9·54 ± 0·37 = ±3·9 % · 열 개 평균 9·65).
- 경험 규칙 (p.1629): *"the Holm radius is not the envelope of the contacts. A general rule of thumb for an irregular cluster is to draw an envelope lying outside each peripheral spot by a distance equal to the centre-to-centre separation from its nearest neighbour: the Holm radius is approximately that of the circle containing the same area"*.
- 각주 † (p.1629): 점이 **선 (선들) 위에** 놓이면 (그림 4(e) 방사선 · 4(f) 고리) 규칙이 깨진다 — *"The interaction term is then not independent of the number of contacts and it appears to increase logarithmically as expected theoretically"* · 반지름 1·0 고리에 **30 · 60 · 120 점 → 상호작용 0·425 · 0·496 · 0·567** [인쇄].  [카드 산술] 증분 0·071 · 0·071 (배마다 같음 = ln2/π² = 0·0702 꼴) · 그러나 반지름 1 고리에 고르게 놓은 점으로 식 (5) (작은 a 의 식 (3) 해도 같음) 을 계산하면 0·357 · 0·428 · 0·498 — **증분은 같고 절대값은 한 배수 (n 을 두 배로) 만큼 어긋난다** → 재현 안 됨 (원문은 고리의 점 반지름 · 배치를 더 적지 않았다).
- 그림 4 (6 패널) · 그림 6 (빽빽한 군집 둘 — 작은 것 = 행 2 · 4 · 4 · 2 = 12 점 · 큰 것 = 행 4 · 6 · 8 · 10 · 10 · 10 · 10 · 8 · 6 · 4 = 76 점이 맞닿은 것 = 그림 3 배치의 a 0·5 [판독 · 셈] · 큰 것의 빗금 원 ≈ 4·9 칸 · 바깥 원 ≈ 5·6 칸 ↔ 표 2 a 0·5 행 4·94 · 5·68 [판독 · 눈대중 ±0·2 칸 · 칸 = 점 간격]) 는 값 없이 '같은 저항 단일 원 (빗금)' 과 Holm 반지름 원을 그렸다.

### 3-7. 정확도 (§4.1) · 그림 7 (p.1629 · `eq_4p1_well_filled_cluster_accuracy.png` · `fig_7.png` · `fig_7a.png` · `fig_7b.png` · digitized.csv fig7a · fig7b)
- 정리 식 [인쇄 p.1629]: 잘 채워진 군집 **R = ρ(1/2nā + 1/2α)** · **α⁻¹ ≡ (3π/16n²)ΣΣ1/s_ij**.
- *"Holm originally suggested that an equation of this form was accurate to 10 % provided a < α/3n^1/2, which is the condition for the mean separation of the contacts to be greater than three times their radius. This estimate is now shown to be unduly pessimistic"* · 오차 셋: ① 근접 (고차) 항 무시 — 저항에 거의 영향 없음 ② 자기 저항이 크고 작음에 따른 상호작용의 계통 변화 — 3π/16 로 정의하면 (원래 2/π 대신) 무시할 만함 ③ 식 (5) 의 평균 반지름 — 점 수가 늘면 줄어듦 · *"In normal cases the total error due to these approximations will be less than 1 %"*.
- **그림 7(a)** (그림 5 군집 · 점을 더해 갈 때) [판독 · 곡선 · ±0·005 (N 10 은 ±0·01)]: 전체 저항 N 10 ≈ 0·30 → 20 ≈ 0·145 → 50 ≈ 0·091 → 100 ≈ 0·072 · 자기 저항 0·24 → 0·094 → 0·035 → 0·019 · 상호작용 ≈ 0·044–0·050 로 거의 일정 · **자기 = 상호작용 교차 N ≈ 40** [판독] (본문 p.1630 은 *"there were then 50 contacts, and the self-resistance and the interaction had become equal"* — 그림과 ≈10 점 차).  [카드 산술] 1/2α (그림 5 표 α 9·57–9·91) = 0·050–0·052 ≈ 판독 '전체 − 자기' (N 20–100 에서 0·051–0·056) · 그런데 판독한 상호작용 선은 0·044–0·048 로 그보다 ≈0·005 낮다 — 세 곡선이 서로 더해지지 않는 것처럼 보이나 판독 오차 (±0·005) 와 같은 크기라 단정하지 않는다 (상호작용을 어떻게 계산해 그렸는지 원문에 없다).  상호작용을 0·051 로 두어도 교차는 N ≈ 38.
- **그림 7(b)** [판독 · ±2 면적 단위 · ±0·2 비]: 겉보기 면적 (저항에서 단일 원으로) N 10 ≈ 7·5 → 50 ≈ 91 → 100 ≈ 141 · 실면적 ≈ 1 → 11 → 21 · 비 4·7 (10) → **≈8·0–8·3 (40–55)** → 7·2 (100) — 본문 *"the ratio of the two rose rapidly to 8 … It then slowly decreased"* · *"With a larger number of smaller spots, the ratio will be greater"*.  [카드 산술] π(ρ/2R)² (그림 7(a) 의 R 로 · ρ = 1) 가 판독 겉보기 면적보다 1–16 % 크다 (N 10 · 15 · 20 · 30 · 40 · 50 · 60 · 70 · 80 · 100 = 8·7 · 21 · 37 · 57 · 77 · 95 · 114 · 120 · 126 · 152 ↔ 7·5 · 20 · 35 · 53 · 73 · 91 · 105 · 116 · 125 · 141 — R 판독 ±0·005 (N 10 은 ±0·01) 가 면적으로 ±7–14 % · 면적 판독 ±2 를 합치면 판독 오차 안) · 실면적 21 / 자기 저항 0·019 → 평균 반지름 ≈ 0·26 (두 경로가 같은 값).

### 3-8. ★ 실접촉 면적 · 하중 · 경도 (§4.2–4.3 · p.1630 · `txt_p11_real_area_upper_limit.png` · `txt_p11_load_hardness_apparent_area.png` · `fig_1.png`)
- 관행 비판: 저항에서 단일 원 가정으로 접촉 면적을 구하는 것은 그림 3–6 의 군집과 *"there is no agreement"* · 표 2 (÷4 ↔ ×625) · 그림 7(b) (비 8) → *"impossible to deduce anything about the real area of contact directly from measurements of the constriction resistance, except an upper limit"*.
- **많고 너무 작지 않은 접촉 → 저항 ≈ 군집 전체가 닿은 것** · 절연 막: *"if an insulating film covers the mechanical area of contact, so that electrical contact occurs by a large number of small breaks in the film, the resistance may be almost as low as with no film (compare figure 4(d))"* (Cocks 1954 · Archard 1959).
- 경도 · 면적: *"The mechanical area of contact is often very much less than that deducible from the bulk properties. The remarkable persistance of surface asperities during bulk plastic flow is well-known (Moore 1948, Greenwood and Rowe 1965): the consequence, that the real area of contact is a small fraction of that predicted from the bulk hardness (see figure 1), is usually ignored"* · 원인 (가공 경화 · 마찰 구속 · 막이 전위 운동을 막음) 은 이 논의에서 상관없다 · *"the important thing is that the use of the bulk hardness is wrong, and quite badly so"*.
- 왜 들키지 않았나: *"the areas of contact found from the constriction resistance, from the bulk hardness, or from visual observation of the contact impression all agree (Bowden and Tabor 1954). From the point of view of electrical contact study this is highly satisfactory: the resistance can be calculated in the usual way from the load, hardness and resistivity"* — 마찰 쪽은 마찰력이 실면적에 비례하리라 보므로 덜 만족스럽다: Parker and Hatch (1950) 는 유리 위에 미끄러뜨린 납 구의 **눈에 보이는 접촉 면적 (하중에 비례)** 을 겉보기 면적으로 보고 실면적과 겉보기 면적이 어떤 까닭으로 비례한다고 결론지었다 · 저자: *"it is doubtful whether there is* any *experimental evidence that the real area of contact is proportional to the load, but rather good experimental evidence that the apparent area is"* · Amontons 법칙의 설명이 옳다면 Parker and Hatch 의 가설이 *"of very general validity"* 여야 한다.
- 그림 1 (Talysurf 단면 · 풀림 · 비드 블라스트 금 블록의 Brinell 압흔 · 곡률 대부분은 반지름 부착 장치로 지움 · 위 = 변형 안 된 면): 눈금 세로 **5 µm** · 가로 **250 µm** [인쇄] → 세로 확대 50 배 [카드 산술] · 하중 · 경도 · 압흔 지름 [미확인].

### 3-9. ★ 원문 안 어긋남 · 재현 안 되는 곳 (카드가 본 것 — 고치지 않고 적는다)
1. **표 1 쌍극 행**: 1/(0·4254 + 6 × 0·8587) = 0·1793 ↔ 인쇄 0·1743 (1 차 · 사중극 행은 같은 검산이 맞음) [카드 산술].
2. **'두 지름 간격' 육각 예** (p.1625): 반지름을 적지 않음 · 값은 반지름 0·5 축척 (1 차 해 0·2521) 과 맞고 표 1 (반지름 1·0) 축척이면 0·1260 [카드 산술].
3. **고리 각주** (0·425 · 0·496 · 0·567): 반지름 1 고리 · 고른 점으로는 0·357 · 0·428 · 0·498 — 증분 (배마다 0·071) 만 같다 [카드 산술].
4. **그림 7(a) 교차 N ≈ 40 ↔ 본문 50 개** [판독].
5. 식 (7) 의 오차가 표 2 배열에서 −1·0 … −3·4 % (§4.1 *"less than 1 %"* 는 '보통의 경우' 라는 한정 · 범위 미정) [카드 산술].
6. 참고문헌 Dyson and Hirst 1954 *"Proc. Phys. Soc. B, 47, 309–12"* — 인쇄 그대로 옮긴다 (권 번호 대조 [미확인]).
7. 표기: *"persistance"* (원문 철자) · OCR 글자층의 쪽 머리 '1621' (p.1627 쪽) · 'Table I.' — 스캔 글자층의 결함이지 인쇄 결함이 아니다.

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬
- 전류 문제 → 정전기 대응 (미세접촉 = 같은 평면의 원판 도체 · 전류 = 전하 · 반무한 몸) → 자기 저항 ρ/4a (원판 정전 용량) · 상호 저항 ρ/2πs (점 전하) → 등전위 조건으로 n × n 연립방정식 (3) → 정확 해 (배열마다) 와 근사식 (4) · (5) · (7) 비교 → 상호작용 항을 Holm 의 식 (1) 로 기하 해석 → Holm 반지름 (8) 로 일반 군집 → 실접촉 면적 · 경도 논의.
- 근사의 근거 = **최소 발열 (Thomson) 원리**: 시행 전류로 계산한 W/I² ≥ 참 저항 → 식 (4) 는 상한.
- 고차 보정의 근거 = 부록의 두 원판 해 (점 전하 + 두 직교 사중극 · 유도 쌍극) → 오차 차수 a²/s³ · a³/s⁴.

### 4-2. 무엇을 풀었나 · 비용
- 배열: 그림 2 (10 점) + 거리 ×2 · ×½ · 9·4 % 사례 · "some 70 arrays" · 표 1 (7 점 · 3 근사) · 그림 3 / 표 2 (76 점 · 반지름 5 가지) · 그림 5 / 7 (5 → 100 점) · 고리 (30 · 60 · 120 점) · 그림 4 · 6 (값 없음).
- 풀이 도구 · 시간 [미확인] — 원문은 연립방정식이 *"rapidly becomes impracticable as the number of spots increases"* 라고만 (1966).  [카드 산술] 오늘은 76 × 76 밀집 행렬 한 번 풀이 = 밀리초.
- 모든 수치는 무차원 (ρ · 길이 단위를 곱해 쓴다 — 배열 치수가 µm 이면 ρ 는 Ω·µm).

### 4-3. 입자 처리 ★
- **입자가 없다.**  계는 두 반무한 도체와 그 경계면의 원판 미세접촉들이다.  접촉 역학 (하중 → 면적) 도 없다 — 면적 · 위치는 주어진다.
- 기하의 가정: 군집이 공칭 접촉 면적과 다른 군집과의 거리보다 작다 · 미세접촉은 같은 평면의 원 · 전류는 모두 한 몸에서 다른 몸으로 (평행).
- DEM 처럼 구 · 점접촉으로 두는 부분은 없다.  [카드 해석] 우리 접촉망에 대응시키면 이 논문의 '미세접촉 군집' 은 **한 입자 쌍 사이 접촉 하나의 속 구조** (거칠기 · 막 틈 · 조각난 접촉면) 이고, 우리 망의 '서로 다른 입자 접촉' 은 이 논문의 '다른 군집' 이다 — 후자의 상호작용은 원문이 가정으로 뺐다.

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete 0 회 · 1966).  수송 쪽 '접촉 독립' 의 깨짐은 일반 형식으로 있다: *"When the microcontacts are far apart they will act independently"* (p.1623) · *"The contacts are not acting independently since the currents are not proportional to the radii"* (p.1624) · 조건 l ~ Σa_i (p.1623).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 계산하지 않았다.  문장만: *"The remarkable persistance of surface asperities during bulk plastic flow is well-known (Moore 1948, Greenwood and Rowe 1965): the consequence, that the real area of contact is a small fraction of that predicted from the bulk hardness … is usually ignored"* · *"the use of the bulk hardness is wrong, and quite badly so"* (p.1630) — 소성 유동 중에도 요철이 남아 **경도로 구한 (소성) 면적 ≠ 실면적**, 그러나 전도에는 그 겉보기 면적이 맞다.
3. **2D / 3D** — 3D 반무한 전위론 (점 전하 1/s · 원판 정전 용량) 위에 **평면 (2D) 배치**의 미세접촉.  배치의 차원이 결과를 바꾼다는 문장은 있다: 면에 퍼진 군집은 상호작용이 점 수와 무관 · **선 위 배치는 로그로 커진다** (각주 · p.1629).  2D 계산 → 3D 전이 말은 없다.
4. **압력을 뺄 때의 거동** — **다루지 않는다** (하중 · 탈압 없음).

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| 협착 저항 (constriction resistance) | 넓은 도체에서 작은 접촉 면으로 전류가 모이며 생기는 저항 — 원 하나면 두 몸 ρ/2a |
| 자기 저항 b_ii | 접촉 i 에 단위 전류 · 나머지 등전위 (전류 0) 일 때 접촉 i 의 전위 — 한 몸 ρ/4a |
| 상호 저항 b_ij | 접촉 j 의 단위 전류가 접촉 i 에 만드는 전위 — 점 근사 ρ/2πs_ij |
| 평행 항 | ρ/2Σa_i — 미세접촉을 서로 무관한 병렬 저항으로 본 값 (위치 무시) |
| 상호작용 항 | 전체 저항 − 평행 항 — 군집 크기로 정해짐 · ≈ ρ/2α |
| Holm 반지름 α | 식 (1) 이 그 저항을 내게 하는 군집 반지름 (식 (8)) |
| 최소 발열 원리 | 실제 전류 분포는 발열을 최소로 함 → 시행 전류로 구한 저항 = 상한 |
| 겉보기 면적 (apparent area) | 미세접촉을 감싼 면적 — 저항 · 경도 · 압흔 관찰이 주는 면적 |
| 실접촉 면적 (real area) | 미세접촉 면적의 합 — 겉보기의 작은 일부일 수 있음 |
| Rayleigh 균일 전류 원판 | 원판에 전류를 고르게 강제한 저항 (16/3π²)ρ/α — 자유 분포 ρ/2α 보다 8 % 큼 |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png` · 손 크롭) | 금 블록 Brinell 압흔의 Talysurf 단면 (세로 5 µm · 가로 250 µm 눈금) · 위 = 변형 안 된 면 | 겉보기 압흔 면적이 미세접촉으로 쪼개진다는 그림 근거 — 값 없음 |
| **Fig. 2** (`fig_2.png` · 손 크롭 · 표 포함) | 무작위 10 점 (a–j) · 반지름 · 전류 · I/a 표 | ★ 해석 기준 배열 (R 0·174 · 독립 0·106) · 판독 중심 = digitized.csv fig2 |
| **Fig. 3** (`fig_3.png` · 다시 자름) | 76 점 정사각 배열 · 같은 저항 단일 원 (빗금) · Holm 반지름 원 | ★ 표 2 의 배치 (재현 = digitized.csv fig3) |
| **Fig. 4** (`fig_4.png` · 다시 자름) | (a) 맞닿은 육각 7 점 (표 1) (b) 큰 점 몇 개 (c)(d) 흩어진 점 (e) 방사선 6 줄 (f) 고리 둘 | 군집 꼴에 따른 Holm 반지름 · 선 배치의 실패 (e)(f) |
| **Fig. 5** (`fig_5.png` · 손 크롭 · 표 포함) | 점을 10 개씩 더한 군집 (1–5 표지) · Holm 반지름 표 | ★ Holm 반지름의 안정 (15 점부터 ±4 %) |
| **Fig. 6** (`fig_6.png` · 다시 자름) | 맞닿은 빽빽한 군집 둘 (12 점 · 76 점) | 빽빽하면 단일 원 ≈ 겉보기 면적 |
| **Fig. 7** (`fig_7.png` · 손 크롭 · 패널 `fig_7a` · `fig_7b`) | (a) 전체 · 자기 · 상호작용 저항 vs 점 수 (b) 겉보기 · 실면적 · 비 vs 점 수 | 상호작용 거의 일정 · 비 ≈ 8 — 판독 = digitized.csv fig7a · fig7b |
| **Table 1** (`tab_1.png` · 손 크롭) | 육각 7 점: 1 차 · 사중극 · 쌍극 전류 · 저항 | 고차 보정 ≤ 3 % · 쌍극 행 검산 어긋남 (§3-9) |
| **Table 2** (`tab_2.png` · 다시 자름) | 반지름 0·02–0·5 의 R · 1/2na · 상호작용 · α · 단일 원 반지름 | ★ 결과 전 대조 · 단위 시험 표적 (식 (3) 으로 정확 재현) |
| 식 크롭 13 (`eq_01` … `eq_08` · `eq_04a` · `eq_05b` · `eq_4p1` · `eq_A1` · `eq_A2`) · 근거 문단 15 (`txt_p*`) | 식 (1)–(8) · §4.1 정의 · 부록 · 인용 문장 | 보고서 붙임 |

## 6. 재현 · 판독 방법 ★
- **원문 숫자**: 전부 300 dpi 쪽 렌더에서 옮겼다 (1 비트 스캔 원 해상도) · OCR 글자층은 쓰지 않았다 (식 · 숫자 깨짐).
- **표 2 재현** [카드 산술]: 그림 3 점 셈 (76 · 행 4 · 6 · 8 · 10 · 10 · 10 · 10 · 8 · 6 · 4) → 간격 1 · 반정수 격자 중심 → 식 (3) (ρ = 1 · U = 1: I_i/a + (2/π)Σ I_j/s_ij = 2) 을 numpy 로 풀어 R = 1/ΣI.
- **그림 2 판독** [판독 + 카드 산술]: 300 dpi 렌더 · 원마다 눈으로 고른 중심 둘레 0·6–1·35 r 고리의 검은 화소 → Kåsa 대수 원 맞춤 → |d − R| < 4 px 로 한 번 더 · 축척 = 인쇄 반지름 10 개에 r_px = 75·88 r + 1·07 (선 두께) 최소제곱 → 중심 좌표 (단위 = 인쇄 반지름 단위) → 식 (3).
- **표 1 검산** [카드 산술]: 육각 7 점 (반지름 1 · 중심 간격 2) 의 식 (3) — 대칭으로 2 원 연립 (가운데: I_c + (6/π) I_o = 2 · 바깥: 2·16331 I_o + 0·31831 I_c = 2).
- **그림 7 판독**: 눈금 보정 (a: 0·7 ↔ 31 행 … 0 ↔ 580·1 행 · N 40 · 80 ↔ 436 · 734 열 / b: 면적 = (573·2 − 행)/3·887 · 비 = (572 − 행)/39·3 · N = (열 − 1037·6)/7·46) 뒤 그 N 의 3 화소 열에서 곡선 선의 중심 — digitized.csv note 에 방법 전부.
- **고리 각주 검산**: 반지름 1 고리에 n 점을 고르게 → s_ij = 2 sin(π|i−j|/n) → 식 (5) 상호작용 (작은 a 의 식 (3) 해와 같음).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **기하 · 재료 · 전류 방향이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 단일 접촉 협착 | 두 몸 ρ/2a · 한 몸 ρ/4a (반무한 · 같은 재료) | 접촉망 간선마다 Holm **R = 1/(2σa)** + 입자 원기둥 bulk (FULL) · CF = bulk 만 [우리 · CLAUDE.md] · Bazzoun RNM 식 8 · 전극 경계 1/(4σr_c) [다른 카드] | **식은 같다** — 단 우리 a/R 은 작지 않다 (아래) → 반무한 가정의 유한 크기 보정은 이 논문에 없다 |
| 접촉끼리 독립 | 독립 = 군집 크기 l ≫ Σa 일 때만 · 그림 2: 독립이면 R 이 ×0·61 (0·106/0·174) | 접촉마다 독립 직렬 · 한 입자의 접촉들이 입자 노드 하나를 공유 · 상호 저항 항 없음 [우리] | **같은 가정** — 원문은 평행 군집에서 그 가정의 오차를 보였다 · 우리 기하의 오차는 미측정 |
| 접촉 반지름 크기 | 무차원 (a 0·02–0·8 · 간격 1–10) | 순수 SE DEM 겹침 ⟨δ⟩ ≈ 지름의 11 % (E_eff 1.35 GPa · 300 MPa) [우리 · CLAUDE.md] → Hertz a = √(R*δ) ≈ **0·33 R** · 렌즈 (기하 교차원) ≈ 0·46 R [카드 산술] · SE–SE CN ≈ 3–7 [우리 · σ_ionic 절의 CN 2·7 · 3·3 · 'CN ≥ 7' 구간] → 한 입자의 Σa ≈ **1·0–3·2 R** ↔ 입자 크기 2R | [카드 산술 · 원문 기하를 입자에 옮긴 정성 추정] 원문 기준 (l ~ Σa) 으로는 **상호작용이 독립 항과 같은 자릿수인 구간** — 단 원문은 평행 · 반무한이라 부호 · 크기는 따로 재야 한다 |
| 협착의 몫 | — | ps45 Hertz 수송 tortuosity 의 **73–75 %** = SE–SE 접촉 협착 (협착 뺀 같은 망 1·25–1·79) · real_14 이온 협착 전력 몫 **78·6 %** (Hertz) [우리 · CLAUDE.md 10-13 · ④a] | Holm 항이 결과의 대부분 → 상호작용 보정이 있다면 σ 에 크게 걸린다 |
| 면적 → 저항 | 많고 너무 작지 않은 점이면 겉보기 (군집) 면적이 저항을 정함 · 경도 F/H 면적 ≈ 겉보기 (금속) · **하중에 비례한다는 실험 증거가 있는 것은 겉보기 면적이고 실면적 비례는 증거가 의심스럽다** (p.1630) | Stage-E Physics: A = max(Hertz πR*δ, A_ligg) 와 min(Tabor F/H, V/h_min, 2πR_min²) [우리] · T1 σ_ionic 폼은 cov_Hertz^½ (Spearman 0·697 > cov_physics 0·476) [우리] · B3 거칠기 피복 = 수송 전용 보정 [우리] | [카드 해석] 원문은 하중에 비례하는 F/H 면적을 겉보기 면적으로 읽고 그것을 전도 면적으로 받친다 — 단 우리 T1 의 cov 는 AM 피복률이라 같은 양이 아니다 · B3 가 실면적 비례로 컨덕턴스를 깎는다면 원문과 어긋난다 (구현 미확인) |
| 복셀 FV (STEP3) | — | 면을 조화평균으로만 잇는다 → 계면 저항 항 0 · 기하 협착은 격자가 해상하면 풀린다 = CONTACT_FREE 가지 (CL-81) [우리] | 원문의 식 (3) · 표 2 = 복셀이 해상도로 수렴해야 할 **해석 기준** (§9-1) |
| 막 · 틈 | 작은 틈이 많으면 막이 없는 것과 거의 같은 저항 | Rint ② S1 = PTFE 면 개구율 α [우리 · CLAUDE.md 10-20 계획] · Lee 2025 PTFE 0·5 → 5 wt% σ_e 3,000 배 붕괴 = 표면 코팅 효과 (CL-46/49) [우리] | [카드 해석] 컨덕턴스 ∝ 개구율은 틈의 수 · 크기에 따라 크게 틀린다 · 3,000 배 붕괴는 '틈이 적고 작아질 때' 쪽 (자기 저항 지배) 과 같은 방향 — 정량 근거 아님 |
| 선 접촉 | 선 위 배치 = 상호작용이 점 수와 함께 로그로 증가 | 탄소 접합 길이 법칙 G_j = max(1, L_c/L_par)/R_j,0 (Rint ②) [우리] | [카드 해석] 섬유 · 줄지은 접촉의 협착을 면적 반지름 하나로 두지 않는 근거 — 탄소 접합 (터널 · TLM) 과는 다른 물리 |

### 7-2. ★ 우리 접촉망의 '독립' 을 어떻게 읽나
- 원문이 확실히 말하는 것: **같은 방향으로 전류를 나르는 가까운 접촉들은 서로의 협착을 키운다** (상호작용 ≥ 0) · 그 크기는 군집 크기로 정해지고 근접 고차 보정은 작다 (≤ 3 %).
- 원문이 말하지 않는 것: 한 입자에서 **들어오는 접촉과 나가는 접촉** 사이의 상호작용 (우리 망의 직렬 통로) · 유한 입자 (a/R 0·3–0·5) 의 협착 · 서로 다른 접촉 (= 원문의 '다른 군집') 사이 상호작용.
- 역학 쪽에는 같은 꼴의 결합 (같은 입자의 다른 접촉에서 오는 반무한 원거리 1/r 항으로 Hertz 의 '독립 접촉' 을 깸) 을 다룬 정본 카드가 있다 — `gonzalez2012_nonlocal_contact_confined_granular` · `giannis2021_stress_based_multicontact_dem` [다른 카드] · 전기 (협착) 쪽 같은 계산은 이 논문에 없다 [카드 해석].
- [카드 해석] 직렬 통로에서는 상호 전위가 반대 부호로 들어가 '독립 협착 + 원기둥 bulk' 합보다 실제 저항이 작아지는 쪽이 자연스럽다 (퍼짐 영역이 겹침) — 같은 방향의 관찰: 독립 Holm 접촉망 (RNM) 이 같은 구조의 연속체 FEM 보다 고 CAM 에서 σ 를 낮게 낸다 (*"RNM 구속저항만 (field spreading X) → 고-CAM 과소"* [다른 카드 · `bazzoun2026_dem_fem_rnm_ionic` L58 · L76 · L94]) — 그 카드는 원인을 *"field spreading 부재"* 로만 적고 상호작용 · 유한 입자 몫으로 나눈 값은 없다 → **우리 망의 독립 가정 오차의 부호 · 크기는 시험으로만** (§9-2).

### 7-3. 겉보기 면적 규칙 ↔ Stage-E · B3 · MPM 넘김
- 원문 (금속): 저항 · 경도 · 압흔 관찰의 면적이 서로 맞는다 = 모두 겉보기 → **전도 계산에는 겉보기 면적을 쓴다** (*"the resistance can be calculated in the usual way from the load, hardness and resistivity"*).
- 우리에게 [카드 해석]: ① Stage-E 의 Tabor F/H 면적을 전도 면적으로 쓰는 쪽을 받친다 (단 금속 · 원문 실험 근거는 Bowden and Tabor 인용뿐) ② 조각난 접촉면 (MPM · FE 의 변형 접촉 · 거칠기 · 막 틈) 의 협착 반지름은 **Holm 반지름** (식 (8) 또는 경험 규칙: 바깥 점마다 최근접 간격만큼 밖으로 둘러 등면적 원) 으로 · 조각 면적의 합 → √(A/π) 로 두지 않는다 ③ 저항에서 거꾸로 구한 면적을 '실접촉 면적' 이라 부르지 않는다 (상한).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **수송 (협착) 이론의 원형** — 우리 분업에서 DEM 접촉망 (접촉당 Holm) 쪽의 이론 뿌리 · 역학 (접촉이 어떻게 생기나) 반쪽은 없다.
- 없는 반쪽: 하중 → 접촉 면적 · 소성 · 유한 입자 · 다른 접촉 사이 상호작용 · 탈압.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 무차원 금속 전기 접촉 이론 — **기공 · 밀도 · 압력 · 역학 값이 하나도 없다** → 랩 기준 · DEM · MPM 값과 나란히 놓을 숫자 없음.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 판정 기준을 미리 적는 꼴의 예: 근사식을 정확 해와 견준 오차 분포 (70 배열 · 절반 < 1 % · 최대 5 % · 예외 9·4 % 한 건) — 우리 수송 근사 (독립 Holm 망) 를 해석 기준 배열 (§9-1) 로 결과 전에 등록할 자리 [카드 해석] | 기공 · 진밀도 · 압력 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 — [카드 산술] 상호작용을 넣은 협착은 접촉 수 n 의 밀집 n × n (76 점 = 5,776 원소) · 원문 *"rapidly becomes impracticable"* (1966) | 장 · 메모리 숫자 없음 |
| **단계 2 · 3** (2D 코드 · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 맞춤) | 없음 — §4.3 의 경도 → 면적 문장은 역학 맞춤 표적이 아니다 | — |
| **단계 5** (3D 복합 압밀) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | ★ **주 자리**: ① Holm R = ρ/2a (두 몸) · ρ/4a (한 몸) 의 원문 근거 ② 독립 가정이 깨지는 조건 l ~ Σa + 우리 DEM 접촉 크기로는 그 구간 [카드 산술 · §7-1] ③ 조각난 접촉면 → Holm 반지름 (식 (8) · 경험 규칙) = MPM · FE 변형 접촉을 수송에 넘길 때의 규칙 ④ 겉보기 면적 규칙 (Stage-E F/H · B3) ⑤ 막 틈 (PTFE · 코팅) ⑥ 선 접촉 로그 — 협착이 수송 tortuosity 의 73–75 % (ps45 Hertz) · 이온 협착 전력 몫 78·6 % (real_14 Hertz) [우리] 라 ①–② 의 영향이 크다 | 우리 기하 (유한 구 · 직렬) 의 상호작용 값 · 이온 계면 저항 (막 · 입계 · 화학) — 기하 협착만 다룬다 |
| **후보 D0** (지금 DEM) | 독립 Holm 망의 **정의역 표지**: "접촉끼리 독립 · 반무한 협착 (a ≪ R) · 같은 재료" — 해석 반례 (그림 2: 0·106 ↔ 0·174 · ×½: 0·240) = 사전 공격 ③ 의 "보장마다 작은 해석 반례" 후보 [카드 해석] | DEM 역학 (18 배 연화 · 겹침) 평가 없음 |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 없음 (역학) — 다만 MPM 변형 접촉면을 수송에 넘길 때 ③ 의 규칙 | — |
| **후보 B** (입자별 FE + 접촉) | 변형 접촉면이 비원형 · 조각이면 협착 반지름 = Holm 반지름 (식 (8) · 경험 규칙) · 저항 해에서 거꾸로 면적을 부르지 않는다 [카드 해석] | FE 접촉 역학 없음 |
| **후보 C** (MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 · 다접촉 DEM) | **이름만 같고 양이 다르다** — 역학의 'multi-contact' (`giannis2021_…` · `varkey2026_…` 응력 결합 · `gonzalez2012_…` 원거리 변위 결합) ↔ 이 논문의 '다접촉' (수송 협착의 상호작용) · 섞지 않는다 — 다만 '접촉끼리 독립' 을 깨는 반무한 1/s 꼴은 같다 [카드 해석] | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | 해당 없음 (전부 역학 단위 시험) — **수송 쪽 단위 시험 넷을 따로 제안** (§9-1: 단일 원 · 표 2 · 그림 2 · 육각 7 점) | — |
| **R1–R7** | **R6** (SE 형상 변형) 쪽 근거 하나: 소성 유동 중에도 표면 요철이 남아 실면적 ≪ 경도 면적 (*"persistance of surface asperities"*) — 그래도 전도에는 겉보기 면적이 맞다 (금속) [카드 해석] · R1 · R2 · R3 · R4 · R5 · R7 없음 | 값 없음 |
| **결과 전 대조 항목** | (수송 · 흐름 밖) ① 단일 원 ρ/2a · ρ/4a ② 표 2 (R 0·4226 · 0·2577 · 0·1581 · 0·1238 · 0·1012 — 식 (3) 정확 재현) ③ 그림 2 (0·174 · ×2 0·141 · ×½ 0·240 · 독립 0·106) ④ 표 1 1 차 행 (0·3259 · 0·8765 · 0·1790) ⑤ 그림 5 Holm 반지름 (15–100 점 9·17–9·91) ⑥ 고리 로그 증분 (배마다 +0·071) — 맞추는 데 쓰지 않음 | 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 금속 전기 접촉 (일반 ρ · 금 압흔 그림 한 장) ↔ LPSCl 이온 · NCM 전자 · 열 · 반무한 두 몸 ↔ 유한 구 (a/R 0·3–0·5) · 평면 군집 · 평행 전류 ↔ 3D 입자망 (직렬 + 병렬) · 하중 없음 (면적 주어짐) ↔ 300 MPa 압밀 겹침 · 무차원 ↔ 차원값.

## 9. 적용 인사이트 (행동)
1. **수송 쪽 단위 시험 넷 (해석 기준 · 흐름 밖 · STEP3 · 접촉망 공통)**: (a) 두 블록을 원 하나로 이음 → R·σ·a = 0·5 (두 몸) · 0·25 (한 몸) 로 수렴하는 지름당 셀 수 (U1 의 수송판) (b) 표 2 배열 (76 점 · 간격 1 · a 0·02–0·5) → 0·4226 … 0·1012 (c) 그림 2 배열 (digitized.csv fig2 중심 · 인쇄 반지름) → 0·174 · ×2 0·141 · ×½ 0·240 (d) 맞닿은 육각 7 점 → 0·1790 (1 차).  STEP3 는 계면 항 0 이지만 기하 협착은 해상하면 풀리므로 (CL-81) 이 넷이 그 해상도 규칙을 정한다 [카드 해석].
2. **접촉망 독립 가정 시험 (D0 · 정의역 표지)**: 작은 입자 군 (3–7 구 · 우리 겹침 a/R 0·3–0·5) 을 STEP3 로 풀어 접촉망 (독립 Holm + 원기둥 bulk) 과 견준다 — 원문의 최소 발열 원리 (시행 전류 → 상한) 를 그 비교의 점검으로 쓴다.  협착이 수송 tortuosity 의 73–75 % · 이온 전력 몫 78·6 % [우리] 라 결과가 크게 달라질 수 있다 — 결과 전 등록 뒤 (CLAUDE.md '복셀 ÷ 접촉망 대조' 1 순위 미실행 과 같은 자리) [카드 해석].
3. **조각난 접촉면의 협착 반지름 = Holm 반지름**: MPM · FE · 거칠기 · 막 틈에서 나온 접촉 조각을 Holm 의 식 (8) (또는 경험 규칙) 으로 원 하나로 — 조각 면적 합의 √(A/π) 로 두지 않는다.  저항에서 구한 면적은 '실접촉' 이 아니라 상한.
4. **막 · 코팅의 틈 (Rint ② S1 · PTFE · 코팅 껍질)**: 면 컨덕턴스를 개구율에 비례로 두지 않는다 — 같은 개구율이라도 틈이 많고 작으면 막 없는 면에 가깝다 (자기 저항 항 ρ/2Σa 작음) · 개구의 수 · 크기 분포를 함께 기록할 근거 (구현 미확인 — 이 카드는 우리 코드를 보지 않았다) [카드 해석].
5. **선 접촉은 로그**: 섬유 · 줄지은 접촉 (VGCF · 줄 모양 SE 다리) 의 협착을 면적 반지름 하나로 두지 않는다 (각주 · 그림 4(e)(f)) [카드 해석].
6. **인용 규칙**: 단일 원 ρ/2a 는 원문 p.1621 의 표준식 (인용 없이 *"very widely used"*) · 군집 식 (1) = Holm 1929 · 이 논문 = 상호작용 항 · Holm 반지름 · 겉보기 면적 결론 — **"ρ/2na" 를 군집 협착 식이라 부르지 않는다** (평행 항뿐 · pan2026 L66 의 학위논문 인용이 그 예).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "For a cluster of n microcontacts, the constriction resistance is the parallel resistance ρ/2Σa_i plus an interaction term set by the extent of the cluster rather than by the number or size of the contacts; the independent-contact value can be well below the actual one (10-spot random array: 0.106 vs 0.174ρ in array units) (Greenwood, *Br. J. Appl. Phys.* 17 (1966) 1621)."
- "Greenwood (1966) showed that areas of contact deduced from constriction resistance, bulk hardness or visual observation agree because all are apparent areas; the resistance gives only an upper limit to the real area of contact."
- 국문 (한정어와 함께): *"미세접촉 군집의 협착 저항은 평행 항 ρ/2Σa 에 군집 크기로 정해지는 상호작용 항을 더한 것이며, 군집 크기가 반지름 합과 같은 자릿수면 접촉끼리 독립이라는 가정이 크게 틀린다 (Greenwood 1966 · 반무한 두 도체 사이 한 군집 · 평행 전류 — 입자망의 직렬 접촉은 원문 범위 밖)."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: ① 연립방정식 (3) 은 미세접촉이 작거나 무한히 떨어진 극한에서만 정확 (p.1624) ② 식 (5) 오차는 부호가 어느 쪽이든 (p.1623) ③ 식 (7) 의 계수는 엄밀 유도가 아님 (p.1626) ④ 경험 규칙은 선 배치에서 깨짐 (p.1629) ⑤ 저항으로는 실면적의 상한만 (p.1630).
**카드가 본 한계**
1. **기하 범위**: 반무한 두 몸 · 한 군집 · 평행 전류 — 우리 접촉망 (유한 구 · 직렬 · 다른 면 접촉) 의 상호작용 값은 주지 않는다.
2. **유한 입자 보정 없음**: a/R 이 0·3–0·5 인 우리 접촉에서 ρ/2a 자체의 오차는 이 논문 밖 [미확인].
3. **재료 · 실험 앵커 없음**: 무차원 해 · 금 압흔 단면 한 장 (값 없음) — 이온 계면 저항 (막 · 입계 · 화학) 과는 다른 양 (기하 협착만).
4. **원문 안 어긋남** (§3-9): 표 1 쌍극 행 · 두 지름 예의 반지름 · 고리 각주 · 그림 7(a) 교차 (≈40 ↔ 50).
5. **식 (7) 오차**: 표 2 배열에서 −1·0 … −3·4 % — "1 % 안" 을 일반 보증으로 인용하지 않는다.
6. **판독**: 그림 2 · 7 값은 스캔 판독 (그림 2 는 식 (3) 재현으로 확인 · 그림 7 은 ±0·005 · ±2 · ±0·2).
7. **[카드 해석] 표지**: §7–9 의 우리 쪽 연결 (직렬 부호 · Stage-E · B3 · Rint ② S1 · 선 접촉) 은 원문에 없는 추론 — 결과 전 등록 · 시험 전에는 판단 근거로 쓰지 않는다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 원문 목록 | 서지 (인쇄 그대로) | 왜 |
|---|---|---|
| Holm 1929 | HOLM, R., 1929, *Wiss. Veröff Siemens-Werken*, **7** (2), 217–58. | ★ 군집 식 (1) R = ρ(1/2na + 1/2α) 의 원전 — 카드 없음 |
| Holm 1958 | —— 1958, *Electric Contacts Handbook* (Berlin: Springer-Verlag). | ★ 원문이 *"Holm's more accessible publications (e.g. Holm 1958)"* 에는 식 (1) 이 없다고 한 책 · 단일 원 식의 판본 · 10 % 조건 (a < α/3n^½) 의 출처 후보 (원문은 출처를 적지 않음) — 우리 카드들은 Holm 1967 (판이 다름) 을 인용 · 카드 없음 |
| Greenwood and Rowe 1965 | GREENWOOD, J. A., and ROWE, G. W., 1965, *J. Appl. Phys.*, **36**, 667. | ★ 소성 유동 중 요철이 남는다 (실면적 ≪ 경도 면적) — 질문 l · c · 카드 없음 |
| Archard 1959 | ARCHARD, J. F., 1959, *Wear*, **2**, 438–55. | 막의 작은 틈이 많으면 막 없는 것과 비슷 — 코팅 · PTFE 막 (흐름 밖) · 카드 없음 |
| Moore 1948 | MOORE, A. J. W., 1948, *Proc. Roy. Soc.*, **195**, 231–44. | 요철 지속 (Greenwood and Rowe 와 짝) · 카드 없음 |
| Rayleigh 1871 | RAYLEIGH, Lord, 1871, *Phil. Trans. Roy. Soc.*, **161**, 77–118. | 균일 전류 원판 (16/3π²)ρ/α · 카드 없음 |
| Bowden and Tabor 1954 | BOWDEN, F. P., and TABOR, D., 1954, *Friction and Lubrication of Solids*, Part I (Oxford: Clarendon Press). | 저항 · 경도 · 관찰 면적이 맞는다 — 정본 `johnson1971_jkr_surface_energy_contact_elastic_solids` L283 은 1950 판 인용 · 카드 없음 |
| Dyson and Hirst 1954 | DYSON, J., and HIRST, W., 1954, *Proc. Phys. Soc.* B, **47**, 309–12. | 미세접촉 군집 관찰 (권 번호 인쇄 그대로) · 카드 없음 |
| Smythe 1950 | SMYTHE, W. R., 1950, *Static and Dynamic Electricity* (New York: McGraw-Hill). | 원판 정전 용량 · 유도 전하 분포 (책) |
| Timoshenko and Goodier 1951 | TIMOSHENKO, S., and GOODIER, J. N., 1951, *Theory of Elasticity* (New York: McGraw-Hill). | 원 안 균일 분포 역거리 적분 (책) |
| Parker and Hatch 1950 | PARKER, R. C., and HATCH, D., 1950, *Proc. Phys. Soc.*, **63**, 185–97. | 마찰 쪽 (흐름 밖) |
| (본문) Cocks 1954 | Cocks (1954 Ph.D. Thesis, University of Reading) | 식 (1) 을 쓴 드문 예 · 막 틈 · 서지 일부만 |

## 13. [미확인] 목록 (원문 12 쪽 전수에 없음)
1. 연립방정식 풀이 방법 · 계산 도구 · 시간 (1966).
2. 그림 2 · 5 의 좌표 (그림에만 — 판독) · 그림 5 의 확률 분포 · 반지름 분포.
3. 표 1 쌍극 행의 세 숫자 가운데 어느 것이 인쇄 오류인지.
4. 고리 각주 (반지름 1·0 · 30 · 60 · 120 점) 의 점 반지름 · 배치 (재현 안 됨).
5. '두 지름 간격' 육각 예의 반지름 · 세 값의 순서.
6. 그림 1 의 하중 · 경도 · 압흔 지름 · Talysurf 조건.
7. 유한 크기 몸 · 다른 군집 사이 상호작용 · 다른 비저항 몸의 식 (각주 한 줄뿐).
8. Holm 10 % 조건 (a < α/3n^½) 의 출처 (원문은 *"Holm originally suggested"* 뿐 · Holm 1929 · 1958 어디인지).
9. 호 번호 (인쇄 없음 · DOI 경로 '17/12').
10. §4.1 *"less than 1 %"* 의 '보통의 경우' 범위.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-13)
- PDF 13 쪽 = IOP 표지 1 + 본문 12 (인쇄 1621–1632) 를 전 쪽 300 dpi 렌더로 읽음 (OCR 글자층은 대조용으로만).  서지 = p.1621 머리 (제목 · 저자 · 소속 · 접수 · 수정 · 쪽 머리 권 17) · IOP 표지 (*"To cite this article: J A Greenwood 1966 Br. J. Appl. Phys. 17 1621"* · 링크 주석 DOI) · 감사 (p.1630).
- 원문 낱말: DEM · discrete · particle simulation 0 회 · plastic 1 회 (*"bulk plastic flow"* p.1630) · unload · springback 0 회.
- 그림 크롭 **39 장** = 도구 4 장 (그림 3 · 4 · 6 · 표 2) **전부 다시 자름** (스캔 쪽 전체 폭 · 표 2 는 쪽 거의 전체) + 손 크롭 35 (그림 1 · 2 · 5 · 7 = 도구가 '거의 백지' 로 버리거나 캡션을 못 잡음 · 패널 7a · 7b · 표 1 = OCR 'Table I.' · 식 13 · 근거 문단 15).  본 뒤 다시 렌더한 것 = fig_7 (첫 판이 두 축 제목을 잘라 쪽 전체 폭으로) · eq_02 · eq_04a (위 가장자리에 앞 줄 꼬리 조각) · txt_p3 둘 · txt_p5 둘 (행 윤곽에서 빈 줄로 경계 옮김).  39 장 전부 Read 로 열어 확인.  `figures.json` 의 `recrop` · `manual_crop` · `note_manual`.
- 재현: 표 2 = 식 (3) 으로 인쇄 숫자 전부 · 표 1 = 1 차 행 · 그림 2 = 판독 배치로 0·1736 · 0·1403 · 0·2382 + 근사식 오차 여섯 (§3-3 · §3-5 · §6).
- 2 차 인용 대조: 정본 카드 pan2026 (L66 · L223 · L361 · L465) · bielefeld2020 (L42 · L51 · L141 · L150 · L396 · L471 · L506) · bielefeld2019 (L18 · L20 · L74 · L160 · L177 · L239 · L276) · shi2019 (L698) · lee2024_multiphysics (L170) · taufactor (L111 · L164 · L198) · wet_processing (L77 · L162 · L227 · L282) · electromechanical (L36) — 고치지 않았다 (정독 출력 batch_86 의 '카드 문제').
- 'Greenwood' 를 적은 나머지 정본 카드는 **다른 논문**이다: `jacksongreen2005_…` L22 · `kogutetsion2002_…` L17 (Greenwood–Williamson 1966) · `morrissey2013_…` L275 (Johnson–Greenwood 1997) · `thorntonyin1991_…` L402 (Greenwood–Johnson 1981).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (561 장 · 2026-11-13) + 'greenwood' · 'real area of contact' · 'Br. J. Appl. Phys' · '1621' grep — 카드 없음 (인용만).

## 🔗 관련 카드
- 가리킨 카드 · 인용 계보: `pan2026_thesis_rate_capable_energy_dense_cathode_composites` (학위논문 [22]) · `bielefeld2020_effective_ionic_conductivity_binder` · `bielefeld2019_microstructural_modeling_composite_cathode` · `shi2019_high_am_loading_particle_size_assb` · `lee2024_multiphysics_dem_fem_initial_pressure_assb` · `electromechanical_contact_model_particulate_systems`.
- 접촉망 수송 (Holm 협착 쓰는 쪽 · 안 쓰는 쪽): `bazzoun2026_dem_fem_rnm_ionic` · `sangros2020_dem_electrical_conductive_paths_assb` · `ketter2025_resistor_network_models_predict_transport_properties` · `taufactor_tortuosity_factor_tomography_tool` · `wet_processing_resolved_am_ssb_cathode_manufacturing` · `nam2026_primer_layer_dry_electrode_collector`.
- 탄소 접합 · 선 접촉 (Rint ②): `hamasaki2022_single_parallel_contact_mwcnt_conductivity` · `banerjee2019_tunneling_tlm_parallel_nanoscale_contacts`.
- 역학 쪽 '다접촉' (이름만 같다): `giannis2021_stress_based_multicontact_dem` · `varkey2026_multicontact_elastoplastic_dem` · `brodu2015_multiple_contact_dem_dense_granular` · `gonzalez2012_nonlocal_contact_confined_granular` (역학의 '접촉끼리 독립' Hertz 가정을 같은 입자의 다른 접촉에서 오는 반무한 원거리 항으로 깬 카드 — 이 논문의 전기 상호 저항 ρ/2πs 와 같은 1/s 꼴 [카드 해석]).
- 접촉 역학 (면적이 어떻게 생기나): `kogutetsion2002_ep_sphere_rigid_flat` · `jacksongreen2005_fem_elastoplastic_hemispherical_contact` · `johnson1971_jkr_surface_energy_contact_elastic_solids`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

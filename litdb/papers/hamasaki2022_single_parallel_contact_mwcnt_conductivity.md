# Electrical conductivity of a single parallel contact between carbon nanotubes — Hamasaki (Nanoscale 2022) · TEM 안에서 두 MWCNT 의 나란한 겹침 길이를 바꿔 가며 잰 접합 저항 — 짧은 겹침은 R ∝ 1/x (G ∝ 길이) · 계면 전도도 10²–10³ S/m · 계면↔본체 문턱 길이 수백 nm

> slug `hamasaki2022_single_parallel_contact_mwcnt_conductivity` · DOI `10.1039/D2NR04112J` · type `exp (in-situ TEM nanomanipulation · two-terminal I–V vs overlap length · FEM check in SI) — CNT–CNT parallel contact resistance · transfer length (TLM) · carbon-network junction` · PDF `1._Electrical_conductivity_of_a_single_parallel_contact_between_carbon_nanotubes.pdf` · digested `2026-11-03` · status ✅
> SI `1._Sup_Electrical_conductivity_of_a_single_parallel_contact_between_carbon_nanotubes.pdf` (9 pp) · evidence `fulltext + SI` · 그림 `8/8 육안 확인` (본문 Fig. 1–4 · SI Fig. S1–S4 · **Fig. 1 손 크롭** (도구가 번호를 놓침) · **Fig. 2 재크롭** (자동 크롭이 왼쪽 단 본문을 끌어들임) — `figures.json` 의 `manual_crop` · `recrop`) · 약칭 `[Hama22]`
> **계기** — Rint ② 다음 세대 탄소 접합 (STEP3 복셀 · VGCF–VGCF 접합 간선 · 길이 법칙 v0 `G_j = max(1, L_c/L_par)/R_j,0` · L_par 0.30 µm · 1저자 10-20 밤 Q17) 의 **한정어 · 장부 · sanity band** 를 위한 원문 확인 (1저자 11-03 요청 · 다섯 편 묶음: `banerjee2019_tunneling_tlm_parallel_nanoscale_contacts` · `fuhrer2000_crossed_nanotube_junctions` · `li2007_tunneling_resistance_cnt_composites` · `nirmalraj2009_swcnt_network_junction_resistance`).  ⛔ v0 범위는 R 런 (11-22–29) 까지 **동결** — 이 카드의 어떤 수도 모형에 넣지 않는다.
> 수치 등급: **stated** = 본문 · SI 에 인쇄 · **figure-read ≈** = 그림 판독 (판독 오차 함께) · **derived(ours)** = 우리 산술 (식 · 가정 함께 · 인용 시 "우리 계산" 명시).

---

## 0. ★ 이 카드가 답하는 것 (1저자 질문 (a)–(d) 중 이 논문 몫)

| 질문 | 이 논문의 답 | 등급 · 자리 |
|---|---|---|
| **(a) 접합 컨덕턴스는 겹침 길이에 선형인가, 포화하는가** | **짧은 겹침에서는 선형** — 15 nm MWCNT 쌍에서 R_total 이 1/x 에 대해 "almost linear … at least for contact lengths smaller than ∼50 nm" (계면 저항 R_inter = α/x ⇒ 계면 컨덕턴스 ∝ x) · 겹침이 길어지면 계면 몫이 줄고 **튜브 본체 저항이 지배** — 문턱 √(α/β) ≈ **100–300 nm** (ρ_CNT ≈ 10⁻⁶ Ω m 가정) · "the effect of the interface becomes negligible at contact lengths longer than a few hundred nanometers" | stated · p. 11531–11533 · Eq. (2)–(4) · Fig. 3 · Fig. 4 |
| (a) 그 모형은 '포화' 를 담는가 | **명시적 포화 항은 없다** — R_total ≈ α/x − βx + R″₀ (Eq. 4) 는 계면 항 (∝ 1/x) 과 본체 항 (∝ x) 의 합이고, 접합 자체의 컨덕턴스는 끝까지 x 에 선형이다.  SI 의 FEM (Fig. S2) 은 긴 겹침에서 이 근사가 저항을 "slightly underestimated" 한다고 적는다 = 전류 쏠림 (전송선, TLM) 효과의 흔적 | stated (SI p. 4–5) · 해석 = derived(ours) §3-5 |
| (a) 그 문턱은 전송선 (TLM) 전달 길이와 같은 양인가 | **사실상 같다** — 같은 두 튜브 · 같은 계면을 전송선으로 풀면 겹침 구간 저항 = (r/2)x + rλ·coth(x/2λ), λ = 1/√(2gr) (g = 1/α · r = ρ_CNT/S) 이고 Hamasaki 의 √(α/β) = **1.155 λ** 다 | derived(ours) · §3-5 (Banerjee 2019 Eq. 8 과 같은 식 — `banerjee2019_…` 카드) |
| (a) Ø0.15 µm 흑연화 섬유로 옮기면 | 같은 계면 저항률 · 같은 간극 창 (0.34–0.68 nm) · Endo 단섬유 저항률 (1 × 10⁻⁴ Ω cm = 10⁻⁶ Ω m, Hamasaki 의 가정값과 같다) · 꽉 찬 단면을 두면 **λ ≈ 0.36–1.7 µm** (α 45–990 kΩ·nm 에 따라) · 문턱 √(α/β) ≈ **0.41–1.9 µm** — 기하만으로 λ ∝ d^(3/4) | derived(ours) · §3-5 (가정 다섯 — §11) |
| (a) 우리 L_par = 0.30 µm 는 그 밴드 안인가 | **밴드의 아래 끝 · 그보다 짧다.**  단 L_par 는 전달 길이가 **아니다** — 직교 교차의 닿음 길이 2(r_fi + r_fj) 로 정한 *접합 instance 의 단위 길이*다.  분산판 v0 (k = ⌈L_c/L_par⌉ 간선 · 섬유 축저항 복셀) 은 **이산 전송선**이라 포화는 풀이 안에서 생기고, 그 λ 는 보정된 R_j,0 가 정한다: λ_model = √(R_j,0·L_par/(r′_i + r′_j)) — R_j,0 = 10³ · 10⁴ · 10⁶ Ω 에서 1.6 · 5.1 · 51 µm | derived(ours) · §7-2 · 우리 코드 `scripts/carbon_junction.py:182` · `scripts/ca_ext_cjunc.py:37` |
| **(b) 접합 하나의 저항 크기** | 접촉 길이 ~5–200 nm 에서 **R_total 27–277 kΩ** (두 단자 · 튜브 · 전극 몫 포함 — 접합만의 값 아님) · 계면 항 기울기 **α = 990 · 270 · 45 kΩ·nm** (15 nm 쌍 셋) ⇒ 겹침 100 nm 에서 R_inter ≈ 0.45–9.9 kΩ · 계면 전도도 **2 × 10² – 4 × 10³ S/m** | R_total = figure-read ≈ (Fig. 2) · α · σ_inter = stated · R_inter(100 nm) = derived(ours) |
| (c) 터널 간극 | 간극 분석은 없다 — 다만 계면 전도의 **기하 창**을 벽 간격 **l₀ = 0.34 nm ~ l₁ = 0.68 nm** 로 잡았다 (SI) — 우리 검출 허용 (tol_ff = min(u, r_f) ≤ 75 nm) 보다 **두 자릿수 이상 좁다** | stated (SI p. 2) |
| **(d) 망 수준** | "macroscopic MWCNT assemblies such as ropes and films can show electrical conductivities comparable to those of individual MWCNTs if each contact is sufficiently long (… more than a few hundred nanometers)" — 접합이 길면 망이 접합에 묶이지 않는다 | stated · p. 11533 |

**한 줄 판정** — 이 논문은 *"접합 컨덕턴스 ∝ 겹침 길이"* 를 **짧은 겹침에서** 실측으로 받쳐 주고 (우리 법칙의 선형 부분과 같은 꼴), 그 선형이 섬유 축저항에 가려지기 시작하는 길이를 MWCNT 에서 수백 nm 로 준다.  VGCF 로 옮기면 그 길이는 µm 대로 길어지지만 (기하 산술), **VGCF–VGCF 계면을 잰 값은 아니다**.

## 1. 한 줄 요약

오사카대 Hamasaki · Nagahama · Hirahara 는 TEM 안의 나노조작기로 한 MWCNT 를 Joule 가열로 끊어 **같은 튜브에서 나온 두 토막**을 만들고, 그 둘을 반데르발스 힘으로 나란히 붙인 뒤 **겹침 길이 x 를 바꿔 가며** 두 단자 I–V 를 쟀다 (±1 µA).  짧은 겹침 (x ≲ 50 nm) 에서 R_total 은 1/x 에 선형이라 계면 저항이 R_inter = α/x (계면 컨덕턴스 ∝ 접촉 면적 ∝ x) 로 서고, 긴 겹침 (x > 150 nm) 에서는 R_total 이 x 에 선형으로 줄어 기울기에서 튜브 전도도 (2–4 × 10⁵ S/m) 를 뽑는다.  계면 기울기 α (45–990 kΩ·nm) 를 간극 창 (0.34–0.68 nm) 으로 환산한 **계면 전도도 2 × 10² – 4 × 10³ S/m** 는 흑연 c 축의 단결정 (~10⁴) 과 열분해 흑연 (~10²) 사이다.  두 항의 미분이 같아지는 **문턱 길이 √(α/β) ≈ 100–300 nm** 를 넘으면 계면은 무시해도 되고, 그러면 긴 겹침으로 이어진 조립체는 단일 튜브 전도도에 닿을 수 있다고 결론짓는다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Hiromu Hamasaki**ᵃ (교신) · Sougo Nagahamaᵃ · Kaori Hiraharaᵇ |
| 소속 | ᵃ Dept. Mechanical Engineering, Osaka University · ᵇ 같은 학과 + Center for Atomic and Molecular Technologies, Osaka University |
| 서지 | *Nanoscale* **14**, 11529–11534 (2022) · Communication · DOI `10.1039/D2NR04112J` (PDF 머리 `10.1039/d2nr04112j`) |
| 일자 | 접수 2022-07-26 · 승인 2022-07-29 · 게재 2022-08-03 |
| 자금 | JST CREST JPMJCR17I5 · 이해상충 없음 |
| 재료 | 아크방전 MWCNT (Sigma-Aldrich 412988) · 외경 8–18 nm (Fig. 2 · Fig. 4 범례) · 벽 수 "typically 10 to 20" · 망원경식 (telescoped) 쌍 1 개 (외경 20–24 nm · core 추출 TEM = Fig. S3) |
| 연구유형 | 실험 (in-situ TEM 나노조작 · 두 단자 I–V) + SI 의 FEM 근사 검증 · **DEM/MPM/복셀 없음** |
| 같은 묶음 카드 | `banerjee2019_tunneling_tlm_parallel_nanoscale_contacts` (같은 식의 TLM 해석해) · `fuhrer2000_crossed_nanotube_junctions` (교차 접합 · 이 논문 ref 15) · `nirmalraj2009_swcnt_network_junction_resistance` (망 접합 · ref 16) · `li2007_tunneling_resistance_cnt_composites` (터널 접합) · `endo2001_vgcf_basic_properties_battery_applications` (VGCF 단섬유 1 × 10⁻⁴ Ω cm) |

## 3. 핵심 수치 ★

### 3-1. 실험 조건 (stated)

| 항목 | 값 | 자리 |
|---|---|---|
| 시편 준비 | Pt 코팅 Si 기판 가장자리에 MWCNT → Sn 진공증착으로 고정 → Sn 코팅 캔틸레버 탐침에 접촉 → Joule 가열로 탐침에 용접 → 더 큰 전류로 가운데를 끊음 (오염 · Sn 대부분 증발) → **같은 튜브의 두 토막** | p. 11529–11530 · Fig. 1(a)–(c) |
| 접촉 형성 | 조작기로 접근 → **반데르발스 힘으로 자발 접촉** (외력 없음) | p. 11530 |
| 측정 | 두 단자 · 전류 소인 **−1 … +1 µA** (자기 가열 회피) · 조사량 무관 확인 · TEM 가속 **90 kV** | p. 11530 |
| 겹침 바꾸기 | 한 튜브를 축 방향으로 평행 이동 (Fig. 1(d)–(f)) | p. 11530 |
| 대표 I–V | 겹침 **177 · 69 · 35 nm** — 거의 선형 · 겹침이 짧을수록 저항 큼 | Fig. 1(g) |
| 고온 확인 | ~50 µA 에서 Sn 이 녹음 = **> 200 °C** (그래서 ±1 µA) | p. 11533 |

### 3-2. 측정값

| 양 | 값 | 등급 · 자리 |
|---|---|---|
| R_total vs 겹침 (6 쌍 · x ≈ 5–200 nm) | 8 nm: ≈ 277 → ≈ 120 kΩ · 9 nm: ≈ 272 → ≈ 139 kΩ (x 74 nm 까지) · 14 nm: ≈ 270 → ≈ 78 kΩ · 15 nm (▲): ≈ 140 → ≈ 49 kΩ · 17 nm: ≈ 236 → ≈ 27 kΩ · 15 nm (+): ≈ 70 → ≈ 32 kΩ (x 36 nm 까지) | figure-read ≈ (±5 kΩ) · Fig. 2 |
| 계면 기울기 α (R vs 1/x 의 기울기, x ≲ 50 nm) | **990 kΩ·nm** (15 nm ▲) · **270 kΩ·nm** (15 nm +) · **45 kΩ·nm** (15 nm_2 ×, 같은 쌍의 반대쪽 면) | stated · p. 11531 · Fig. 3(a) |
| 8 nm 쌍 | R 이 1/x 에 비례하지 **않음** — 겹침이 길고 튜브가 가늘어 R_CNT 가 지배 | stated · p. 11532 |
| 튜브 전도도 (x > 150 nm 기울기 β = 3ρ/(2S)) | **2 × 10⁵ S/m** (8 nm) · **4 × 10⁵ S/m** (18 nm) · **3 × 10⁵ S/m** (망원경식 20–24 nm) — 문헌 (refs 9, 10) 과 정합 | stated · p. 11532 · Fig. 4(a) |
| 긴 겹침 R_total | 8 nm: ≈ 127 → 95 kΩ (x 160 → 345 nm) · 18 nm: ≈ 21 → 18 kΩ (x 230 → 440 nm) · 망원경식: ≈ 67 → 44 kΩ (x 270 → 980 nm) | figure-read ≈ · Fig. 4(a) |
| 망원경식 쌍의 α | **∼6000 kΩ·nm** — ~200 nm 부근에서 비선형 · "even though its contact should be wider and stabler" ⇒ 저자: MWCNT 의 **반경 방향 저항이 클 수 있다** | stated · p. 11532–11533 |
| 끊기 전 · 후 | 한 MWCNT **15 kΩ → 18 kΩ** (끊은 뒤 ~100 nm 겹침 계면 하나) ⇒ "the interfacial resistance was not dominant" | stated · SI p. 8 · Fig. S4 |
| Seebeck | 음 (n 형) — Joule 가열의 탈도핑 (산소 탈착) 으로 저자 해석 | stated · p. 11532 (ref 24 = "in preparation") |
| 지름 의존 | "One would expect the outer diameter to have an effect on the interfacial resistance, however, no significant relationship was detected" | stated · p. 11531 |
| Schottky | I–V 선형 · 대칭 ⇒ 무시 가능 (같은 튜브에서 나온 토막 = 같은 키랄 지수일 것 · 상온 · 큰 지름) | stated · p. 11531–11532 |

### 3-3. 계면 전도도로의 환산 (SI)

| 양 | 값 | 등급 |
|---|---|---|
| 간극 창 | 두 외벽이 전도에 기여하는 최소 · 최대 거리 **l₀ = 0.34 nm** (흑연 c 면 간격) · **l₁ = 0.68 nm** | stated (SI p. 2) — l₁ 은 "l/C 가 0.5 nm 위에서 크게 안 변한다" (Fig. S1(b)) 로 고른 값 |
| 크기 인자 (지름 15 nm) | **l = 0.51 nm** (= (l₀ + l₁)/2) · **C = 3.2 nm** (그 창 안의 호 길이) | stated · p. 11531 · SI |
| 계면 전도도 | **2 × 10² – 4 × 10³ S/m** | stated · p. 11531 |
| 재현 [derived(ours)] | ρ_inter = αC/l → α 990 · 270 · 45 kΩ·nm ⇒ σ_inter **161 · 590 · 3,542 S/m** (논문 "2 × 10² – 4 × 10³" 와 일치) · C 는 두 원기둥 간격 l₀ + 2(R − √(R² − y²)) = l₁ 인 호 길이로 **3.200 nm** 재현 (R = 7.5 nm) · l/C = 0.1594 (Fig. S1(b) 의 평탄값 ≈ 0.16 과 일치) | derived(ours) |
| 대조값 (인용) | 단결정 흑연 c 축 ~10⁴ S/m · 열분해 흑연 c 축 ~10² S/m (ref 22, Tsang & Dresselhaus 1976) | stated (인용) |
| 문턱 길이 | **√(α/β) = 100–300 nm** (ρ_CNT ≈ 10⁻⁶ Ω m 가정 · "though it depends on the cross-sectional area of MWCNTs") | stated · p. 11532 |
| 그 문턱의 재확인 [derived(ours)] | 15 nm · 벽 15 개 가정 (d_in ≈ 4.8 nm) · ρ = 10⁻⁶ Ω m → r ≈ 6.3 Ω/nm · β = 1.5r ⇒ √(α/β) ≈ **69 nm** (α 45) … **323 nm** (α 990) — 논문 범위와 같은 자릿수 | derived(ours) — 벽 수 · 내경은 우리 가정 |

### 3-4. FEM 근사 검증 (SI)

| 항목 | 값 | 등급 |
|---|---|---|
| 모형 | 높은 접촉 저항으로 맞닿은 **두 직육면체**, 위 막대 오른쪽으로 전류 주입 · 아래 막대 왼쪽 접지 (Fig. S2(c)) · 부분 저항 R_p ≈ α/x + β′x (Eq. S1) · β′ = β/3 = ρ_bulk/(2S) | stated (SI p. 4) |
| α/β′ | **2 × 10⁴** · **2 × 10⁵** (nm²) 두 경우 | stated · Fig. S2(d)(e) |
| 입력 → 되읽기 | σ_inter **1.00 × 10²** → **1.02 × 10²** S/m (x < 50 nm) · σ_CNT **1.00 × 10⁵** → **1.23 × 10⁵** S/m (x > 200 nm) — "slight overestimates" | stated (SI p. 5) |
| 근사의 편향 | Eq. (S1) 이 긴 겹침에서 저항을 "slightly underestimated" | stated (SI p. 5) · Fig. S2(d) 의 파란 점이 검은 선 위로 올라간다 |

### 3-5. ★ 전송선 (TLM) 과의 대응 · VGCF 로 옮긴 산술 — 전부 derived(ours)

**① 같은 기하의 전송선 해 (식만 · Banerjee 2019 Eq. 8 의 R̄sh2 = 1 경우와 같다).**  두 같은 튜브 (길이당 저항 r = ρ/S) 가 길이 x 로 겹치고 계면의 길이당 컨덕턴스가 g (= 1/α) 일 때, 한 튜브 끝에서 들어와 다른 튜브 끝으로 나가는 겹침 구간 저항은
`R_lap(x) = (r/2)·x + r·λ·coth(x / 2λ)`,   `λ = 1/√(2 g r) = √(α / 2r)`.
- x ≪ λ : `R_lap ≈ α/x + (2/3)·r·x` — Hamasaki 의 R_p ≈ α/x + β′x (β′ = r/2) 와 같은 꼴이고, 계수 2/3 > 1/2 이 SI 의 *"긴 겹침에서 근사가 저항을 약간 과소평가"* 를 설명한다.
- x ≫ λ : `R_lap → (r/2)·x + r·λ` — **접합 몫 (rλ) 이 포화**하고 남는 x 의존은 겹친 두 튜브의 병렬 본체 저항뿐이다.
- 측정 경로 전체 (끝-끝 길이 L₁ + L₂ 고정) 로 옮기면 `R_total = R′₀ − (3/2)·r·x + r·λ·coth(x/2λ)` → Hamasaki 의 β = 3ρ/(2S) 와 같고, 두 항 미분이 같아지는 길이 **√(α/β) = √(4/3)·λ = 1.155 λ**.
⇒ Hamasaki 의 "문턱 길이" 는 전송선의 **전달 길이 (transfer length) 와 같은 양 (1.15 배)** 이다.  접합 컨덕턴스 자체는 국소적으로 x 에 선형이고, **실효 접합 컨덕턴스의 포화는 튜브 축저항이 만드는 전류 쏠림**에서 나온다.

**② Ø0.15 µm 흑연화 섬유로 옮기기 (가정 다섯 · 그대로 인용 금지).**
가정: (i) 계면 저항률 ρ_inter 가 MWCNT 외벽–외벽과 같다 (ii) 간극 창 l₀ 0.34 · l₁ 0.68 nm 가 같다 → C ∝ √R (iii) 섬유 저항률 = Endo 2001 단섬유 **1 × 10⁻⁴ Ω cm = 10⁻⁶ Ω m** (Hamasaki 의 ρ_CNT 가정값과 같다 · 카드 `endo2001_…` · stated) (iv) 꽉 찬 단면 (중공 무시 — 우리 직경 보존 σ 7,854 S/cm 와 같은 규약) (v) 외력 없는 vdW 접촉 (압밀 압력 없음).

| 양 | 15 nm MWCNT (논문) | **Ø0.15 µm VGCF (우리 산술)** |
|---|---|---|
| C (간극 창 호 길이) | 3.200 nm | **10.10 nm** |
| α (계면 기울기) | 45 · 270 · 990 kΩ·nm | **14.3 · 85.5 · 313.6 kΩ·nm** (= α × 3.200/10.10) |
| 섬유 길이당 저항 r′ | (벽 수 의존) | **56.588 Ω/µm** (= 10⁻⁶ / (π · 0.075² µm²)) — 우리 모형의 섬유 복셀과 같은 값 |
| λ = √(α/2r′) | — | **0.355 · 0.869 · 1.665 µm** |
| √(α/β) (= Hamasaki 문턱) | 100–300 nm (stated) | **0.410 · 1.004 · 1.922 µm** |
| 길이 법칙 단위 L_par (0.30 µm) 에 해당하는 저항 α/L_par | — | **48 · 285 · 1,045 Ω** |
| 직교 교차 (90°) 의 같은 창 면적 A_x = π·2R·(l₁ − l₀) | 16.0 nm² | **160.2 nm²** |
| 직교 교차 접합 저항 ρ_inter·l/A_x | — | **≈ 0.90 · 5.4 · 19.8 kΩ** |
| 면적 동등 길이 A_x/C (교차 하나 = 나란한 접촉 몇 nm) | 5.0 nm | **15.9 nm** |

- 기하만으로 **λ ∝ d^(3/4)** (C ∝ d^(1/2) · r′ ∝ d⁻²) — 15 nm → 150 nm 에서 ×5.6.
- **같은 짝의 양 끝 α 가 6 배 다르다** (270 · 45 — §11 ②) ⇒ 위 VGCF 값은 자릿수 이상의 정밀도가 없다.

## 4. 방법 ★

### 4-1. 회로 모형 (본문 Eq. 1–4)
- **Eq. (1)** `R_total = R_CNT + R_inter + R₀` — R₀ = 두 단자 측정의 나머지 (탐침 · 기판 접촉 등) · "can be assumed to be a constant value".
- **Eq. (2)** `R_inter = ρ_inter·l/A = ρ_inter·l/(Cx) = α/x` — 접촉 면적 A = Cx (겹침 길이에 비례) · α = ρ_inter·l/C 를 상수로 둔다.
- **Eq. (3)** `R_CNT ≈ ρ_CNT(L₁ − x)/S + ρ_CNT(L₂ − x)/S + ρ_CNT·x/(2S) = R′₀ − βx` · β = 3ρ_CNT/(2S) — 겹친 구간은 두 튜브 병렬.  **반경 방향 저항률은 넣지 않았다** (같은 MWCNT 의 단면을 바꾼 실험에서 저항이 단면적에 반비례했다는 ref 24 를 근거로).
- **Eq. (4)** `R_total ≈ α/x − βx + R″₀` · R″₀ = R₀ + R′₀.  x = √(α/β) 에서 두 항의 미분이 같다.

### 4-2. 수치 처리
- x ≲ 50 nm: R vs 1/x 직선 기울기 = α (Fig. 3(a)).
- x > 150 nm: R vs x 직선 기울기 = β → ρ_CNT (단면 π(d_out² − d_in²)/4) → σ_CNT (Fig. 4(a)).
- 계면 전도도 = l/(αC) (크기 인자 l · C 는 SI Fig. S1 의 기하 정의).
- FEM (SI): 두 직육면체 · 높은 접촉 저항 · Eq. (S1) 근사와 비교 (도구 · 격자 · 소프트웨어 미기재 → n/a).

### 4-3. ★ 접합 처리 (DEM 의 "입자 처리" 칸)
- **기하**: 나란한 겹침 (parallel overlap) 하나 · 외벽–외벽 · 같은 튜브에서 나온 토막 (키랄 같음) · 망원경식 (core–housing) 대조 1 쌍.
- **간극**: vdW 평형 거리 (외력 없음) — 접촉력 · 변형 · 압력 변수 **없음**.
- **사이 물질**: 없음 (진공 · Joule 가열로 오염 제거 — 저자 서술).
- **도핑 상태**: Joule 가열 뒤 탈도핑 (n 형 Seebeck).
- ⇒ 우리 frame 으로: **접합 수송의 미시 물리만** (frame[5] 의 전달 절반 중 접점 단위) · 망 · 역학 · 압밀 없음.

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 모식도 (b) TEM 실물 설정 (c) Joule 가열로 끊은 뒤 (d)–(f) 겹침 177 · 69 · 35 nm 의 외벽–외벽 접촉 TEM (g) 그 셋의 I–V (±1 µA) | (d)–(f) = "나란한 접촉" 의 실물 기하 — 우리 L_c (중심선 닿음 길이) 가 가리키는 물체가 이런 겹침이다 · ⚠ 도구가 번호를 놓쳐 손 크롭 |
| **2** | R_total vs 겹침 x (6 쌍, 외경 8–17 nm) — 모두 x 가 늘면 R 감소 · 50 nm 아래에서 급감 | ★ **(b) 의 크기 밴드** (27–277 kΩ, 두 단자 총저항) · 짧은 겹침에서 G ∝ x 의 실측 꼴 · ⚠ 자동 크롭이 왼쪽 단 본문을 끌어들여 재크롭 |
| **3** | (a) R vs 1/x — 15 nm 쌍 셋의 직선 (기울기 α 990 · 270 · 45 kΩ·nm) · 8 nm 쌍은 비선형 (b)–(d) 해당 TEM | ★ **(a) 의 근거 그림** — "G ∝ 길이" 가 x ≲ 50 nm 에서 선다 · 같은 쌍 (+ · ×) 의 기울기가 6 배 다르다는 것도 이 그림에서 보인다 |
| 4 | (a) 긴 겹침 (x > 150 nm) 의 R vs x — 8 · 18 nm 외벽 접촉 + 망원경식 20–24 nm (b) 망원경식 모식도 | 긴 겹침에서 R 이 x 에 선형으로 준다 = 본체 지배 · 망원경식이 오히려 α 가 크다 (∼6000 kΩ·nm) ⇒ 반경 방향 (c 축) 저항이 접근 몫을 키울 수 있다 — 우리 R_j,0 가 묶는 "접근 몫" (한정어 ②) 의 문헌 그림 |
| S1 | (a) 두 원 단면 · 간극 창 l₀ · l · l₁ · 호 C (b) l/C vs l₁ (지름 15 nm) — 0.5 nm 위에서 평탄 ≈ 0.16 | 간극 창 정의 — 우리 tol_ff (≤ 75 nm) 와 **자릿수가 다른 '접촉'** 의 정의 · VGCF 환산 (§3-5) 의 출발점 |
| S2 | (a) 나란한 접촉의 사다리 등가회로 (b) R_total · R_p 정의 (c) FEM 모형 (d)(e) FEM vs Eq. (S1) — α/β′ 2 × 10⁴ · 2 × 10⁵ | (a) = **우리 분산판 v0 와 같은 사다리** (접합 간선 + 섬유 축저항) · (d) 의 긴 겹침 편향 = 전류 쏠림 · 우리 이산 TLM 시험의 그림판 |
| S3 | 망원경식 MWCNT 의 core 추출 TEM (a)–(c) · 모식도 (d) · 추출 뒤 housing (e) | 망원경식 대조의 실물 |
| S4 | 끊기 전 · 후 TEM (a)(b) 와 I–V (c) — 15 → 18 kΩ | ~100 nm 계면 하나가 튜브 대비 지배적이지 않은 사례 (긴 겹침의 망 수준 결론의 근거) |

## 6. Post-processing ★
- **무엇**: 두 직선 적합 (R vs 1/x · R vs x) → α · β → σ_inter · σ_CNT · 문턱 √(α/β).  기하 크기 인자 (l · C) 는 간극 창으로 해석적 계산.  FEM 으로 근사식 자기검증 (입력 σ 되읽기).
- **도구**: 미기재 (FEM 소프트웨어 · 적합 도구 n/a).
- **기록 방식**: 각 쌍을 외경으로 라벨 · 같은 쌍 반대쪽 면 재측정으로 재현성 확인 (± Sn 입자 분포 변화).  오차막대 · 적합 불확도 **없음**.

## 7. 우리 DEM+MPM 대비 ★★

> 대상 = **Rint ② 다음 세대 STEP3 복셀 전자 채널의 VGCF–VGCF 탄소 접합** (`scripts/carbon_junction.py` · `scripts/ca_ext_cjunc.py` · 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` · 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · 작업 브랜치 HEAD `57f1b2baf` 에서 읽음).  frame[5] 로는 **MPM 침대 위의 수송 (STEP3)** 이다 — DEM 접촉망 (`network_conductivity.py` · Holm) 이 아니다.

### 7-1. 법칙 대조

| 항목 | Hamasaki 2022 | 우리 v0 | 판정 |
|---|---|---|---|
| 짧은 접촉의 접합 컨덕턴스 | ∝ 겹침 길이 (R_inter = α/x · x ≲ 50 nm 실측) | instance 마다 `G_j = max(1, L_c/L_par)/R_j,0` — L_c > L_par 이면 ∝ L_c | **선형 부분은 같은 꼴** · 단 우리는 L_c ≤ L_par 에서 **바닥 1/R_j,0** (교차 = 점 접합) — 논문에 교차 데이터는 없다 |
| 긴 접촉 | 계면 몫이 줄어 본체 지배 · 문턱 √(α/β) 100–300 nm (MWCNT) | 분산판 v0: k = ⌈L_c/L_par⌉ 간선 · 간선마다 G_j/k · 섬유 축저항 = 복셀 (r′ = 56.588 Ω/µm) | **분산판 = 이산 전송선** (Fig. S2(a) 와 같은 사다리) → 포화는 풀이 안에서 생긴다 · 그 λ 는 R_j,0 가 정한다 (§7-2) |
| 접합의 '접촉' 정의 | 외벽 간격 0.34–0.68 nm 창 | 중심선 거리 ≤ r_fi + r_fj + tol_ff · tol_ff = min(u, r_f) ≤ 0.075 µm (`ca_ext_cjunc.py` 문턱 · 등록 R §2-1) | 두 자릿수 넘게 다른 '접촉' — 우리 것은 **MPM 경로 위치 불확도의 기하 근접**이지 물리 간극이 아니다 (한정어 ⑩ 그대로) |
| 지름 의존 | 유의한 관계 **검출 안 됨** (8–18 nm) | Ø0.15 µm 하나 (규약 고정 · 설계 §1-2 #3) | 단일 R_j,0 와 모순 없음 — 단분산이라 시험 대상도 아님 |
| 반경 방향 (접근) 저항 | 망원경식에서 α 가 커짐 → 반경 저항이 클 수 있다 (저자 추정) | 포트 직접 간선 · 반셀 없음 · **접근 몫이 R_j,0 에 묶인다** (등록 R 한정어 ② · `CJUNC_QUALIFIERS`) | 같은 방향의 한정어 — 문헌이 그 몫이 작지 않을 수 있음을 보인다 |
| 섬유 저항률 | 가정 ρ_CNT ≈ 10⁻⁶ Ω m · 측정 2–4 × 10⁵ S/m (= 2.5–5 × 10⁻⁶ Ω m) | Endo 단섬유 1 × 10⁻⁴ Ω cm = 10⁻⁶ Ω m (직경 보존 7,854 S/cm · 설계 §1-2 #2) | 같은 자릿수 — 우연 (재료 다름 · MWCNT 아크 vs VGCF 흑연화) |

### 7-2. ★ 모형 안의 전달 길이 — "선형 · 무포화 법칙" 의 진짜 뜻
- 우리 법칙의 **국소 길이당 컨덕턴스** g = 1/(R_j,0·L_par) 는 Hamasaki 의 1/α 와 같은 자리다.  분산판 v0 는 그 g 를 L_c/k (≤ L_par) 간격 간선으로 나누어 섬유 복셀 사이에 놓으므로, 풀이가 만드는 실효 접합 컨덕턴스는 **전송선처럼 포화**한다 (Codex 기하 검토의 손 회로: 분산 다섯 접합 G 1.366 S ↔ 한 포트 집중 5 S — `docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/geometry/geometry_review_notes.md`).
- 그 포화 길이 = **λ_model = √(R_j,0·L_par/(r′_i + r′_j))** [derived(ours) · 같은 노트가 처음 적은 식]:

| R_j,0 [Ω] | 10² | 10³ | 10⁴ | 10⁵ | 10⁶ |
|---|---|---|---|---|---|
| λ_model [µm] | 0.515 | 1.628 | 5.149 | 16.28 | 51.49 |

- ⇒ R_j,0 가 크면 (점 접합이 나쁘면) 긴 접촉의 길이당 컨덕턴스도 같이 나빠서 λ_model 이 길어지고, 실침대 L_c 대부분이 λ_model 보다 짧으면 **포화는 거의 드러나지 않는다**.  문헌 쪽 VGCF 환산 λ (0.36–1.7 µm · §3-5) 와의 차이는 **R_j,0 하나가 교차 (점) 와 길이당 (선) 컨덕턴스를 같이 정한다**는 데서 온다 (§7-3).
- 우리 L_par (0.30 µm) 는 이산화 간격 쪽이다: 간선 간격 L_c/k ∈ (L_par/2, L_par] 이 λ_model (≥ 0.5 µm @ R_j,0 ≥ 10² Ω) 보다 짧아 전송선이 **분해된다**.  알려진 이산화 오차 = k 가 바뀌는 정수 경계의 σ 계단 (등록 R 한정어 ⑫ · 설계 §4-5).

### 7-3. ★ 교차 ↔ 나란한 접촉의 가중 — 단일 R_j,0 가 못 가르는 것 (derived(ours) · 가정 의존)
- 같은 간극 창 그림에서 직교 교차의 컨덕턴스 ∝ A_x = π·2R(l₁ − l₀) · 나란한 접촉 ∝ C·L.  비 = L/(A_x/C) · Ø0.15 µm 에서 **A_x/C ≈ 15.9 nm**.
- 우리 법칙의 같은 비 = L/L_par = L/300 nm ⇒ **R_j,0 를 교차가 대부분인 침대로 보정하면, 그 그림 대비 긴 나란한 접촉의 가중이 ≈ 19 배 작다** (300/15.9).
- 단 비스듬한 교차 (각 θ) 는 두 그림이 같은 1/sin θ 로 자란다 (우리 L_c = 2(r_i + r_j)/sin θ · 물리 접촉 띠 길이 = 2√(2RΔl)/sin θ ≈ 14.3 nm/sin θ) — 차이는 **진짜 나란히 붙은 (θ → 0, 겹침 길이 = L) 접촉에서만** 열린다.
- 이 차이는 **결함이 아니라 모형 선택** (1저자 10-20 밤 Q17 · 새 손잡이 없음) 이고, 실침대에서 진짜 나란한 vdW 접촉이 얼마나 되는지 (압밀 섬유 사이에 SE · PTFE 가 끼는가) 는 **모른다** → §9 (나)-②.

### 7-4. frame[4]/[5] 메모
- 이 논문은 **접합 한 개의 수송**만 소유한다 — 망 · 압밀 · 접촉력이 없다.  우리 쪽은 접촉 역학을 풀지 않는다 (MPM 은 섬유 접촉 역학을 풀지 않는다 · 한정어 ⑩).  ⇒ 이 카드는 R_j,0 의 **교차검증 상대가 아니다** — 값이 아니라 *법칙의 꼴과 그 적용 범위*의 근거다.
- 등록 R §7-2 금지 문장 그대로: **R_j,0 를 이 논문의 α · 계면 전도도와 같은 양으로 부르지 않는다** (R_j,0 = 모형 내부 보정값 · 포트 반셀 · 접근 몫 포함).

## 8. 적용 인사이트
- ① **"선형 길이 법칙" 문장을 정확히 하자** — 문헌이 받쳐 주는 것은 *국소 길이당 컨덕턴스 일정* (짧은 겹침의 G ∝ x) 이다.  *총 접합 컨덕턴스가 끝없이 L_c 에 비례* 는 문헌 어디에도 없고, 우리 모형도 실제로는 그렇게 풀리지 않는다 (분산판 + 섬유 축저항 = 이산 전송선).  한정어 ⑫ 를 이 뜻으로 고쳐 쓰면 Codex 가 물을 *"전달 길이 미검증"* (`carbon_junction.py:145`) 에 답이 생긴다.
- ② **보정 뒤 진단 하나로 법칙의 위험을 잰다** — λ_model 을 보정된 R_j,0 로 계산하고 L_c 분포 (S0 census) 와 나란히 보고하면, 긴 접촉이 포화 영역 (L_c ≳ 2λ) 에 들어가는지 숫자로 보인다.  값 채택 없음.
- ③ **교차 ↔ 나란함 가중 (§7-3) 은 v1 질문** — v0 는 동결이므로 장부에만 올린다.
- ④ **반경 방향 접근 저항** — 망원경식 결과 (α ~6000 kΩ·nm) 는 "접근 몫이 R_j,0 에 묶인다" 한정어 ② 가 작지 않은 몫일 수 있다는 근거다.  흑연화 VGCF 의 c 축 저항률은 면내보다 자릿수로 크다 (이 논문 인용: 단결정 흑연 c 축 ~10⁴ S/m).

## 9. 적용 후보 (11-03)

### (가) 지금 v0 안에서 — 값 채택 없음 (한정어 · 장부 · 진단 · 시험)
1. **한정어 문장 (문서)** — 등록 R §7-1 필수 한정어 ⑫ (`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md:278`) · 설계 §4-5 (`docs/reviews/rint_carbon_additive_design_v1_20261020.md:336–337`) 에 한 줄: *"길이 법칙 v0 의 선형은 국소 길이당 컨덕턴스의 1차 근사다 (짧은 겹침의 G ∝ 길이 = Hamasaki 2022 Fig. 3 · 15 nm MWCNT · x ≲ 50 nm) — 실효 접합 컨덕턴스의 포화는 분산판 간선과 섬유 축저항이 풀이 안에서 만든다 (전달 길이 λ = √(R_j,0·L_par/(r′_i + r′_j))) · VGCF–VGCF 계면의 문헌값은 없다."*  ⚠ 같은 문장을 코드 상수 `CJUNC_QUALIFIERS` (`scripts/carbon_junction.py:138–145`) 에 넣는 것은 **문서 수정이 아니다** — 기록 검증기 (`scripts/ca_ext_cjunc.py:466`) 와 사슬 시험 (`scripts/test_rint_r_chain.py:619`) 이 그 문자열을 대조하므로 게이트 · Codex 를 거치는 코드 변경이다 (물리 변경은 아님).
2. **장부 항목 (후보)** — "전달 길이 미검증" (`carbon_junction.py:145` 의 표현) 을 원장 항목으로: 문헌 = CNT 계만 (Hamasaki · Banerjee) · VGCF 환산 = 우리 산술 0.36–1.7 µm (이 카드 §3-5) · 닫는 조건 = 보정 뒤 λ_model ↔ L_c 분포 보고 (아래 3).
3. **진단 (보고 전용 · 코드 변경 없이 기록에서)** — 보정된 R_j,0 마다 λ_model 을 계산하고, S0 census 의 L_c 목록 (`scripts/ca_s0_census.py:437` (L_c 정의) · `:776–786` (`long_contacts` · `Lc_um`)) 에서 **L_c > λ_model · > 2λ_model 인 instance 수와 그 접합 전류 몫**을 보고한다.  ⚠ 순서: SBE 는 지금 · **DBE 분포는 등록 R §2-1 개정 커밋 뒤에만** (S0 단계 2 규칙 그대로).
4. **진단 (보고 전용)** — S0 SBE L_c 분포를 문헌 환산 기준 길이 {0.41, 1.0, 1.9 µm} (이 카드의 √(α/β) 밴드) 위로 넘는 instance 수로 요약 — "포화가 문제 될 수 있는 접촉이 얼마나 있나" 의 첫 자릿수.  기준 길이는 **보고용 눈금**이지 문턱 · 법칙이 아니다.
5. **해석 시험 (물리 변경 없음 · 게이트 대상)** — 두 평행 복셀 섬유 + 분산판 간선의 단자 저항을 Banerjee Eq. (8) (R̄sh2 = 1 · 이 카드 §3-5 ① 식) 과 대조하는 시험을 `scripts/test_carbon_junction.py` 에: λ_model ≫ 간선 간격에서 이산화 오차 O((Δ/λ)²) 안 일치 · L_c ≫ λ_model 에서 포화 재현.  "보장마다 작은 해석 반례" (CLAUDE.md Codex 사전 공격 ③) 의 꼴이다.

### (나) 1저자 비준이 필요한 것 (물리 · 법칙 · 값이 바뀐다)
1. **포화하는 길이 법칙** (예: G_j = (2λ/L_par)·tanh(L_c/2λ)/R_j,0) — ⛔ 분산판 v0 가 이미 풀이 안에서 포화를 만들므로 **이중 계상**이 된다 · λ 가 새 손잡이 (SBE 한 점으로 식별 불가 — 설계 K1 위반) → 넣으려면 분산판을 버리고 lumped 로 돌아가야 해서 Codex RCA-05 결정과 충돌.  **권고: 하지 않는다** (진단 (가)-3 으로 충분).
2. **교차 ↔ 나란함 가중 바꾸기** (L_par 정규화를 간극 창 면적 동등 길이 ≈ 16 nm 쪽으로) — 긴 나란한 접촉의 가중이 ~19 배 커진다 (§7-3) · 대가 = 길이 법칙 개정 · S0 숫자 · 등록 재봉인 · R_j,0 재보정 · 간극 창 가정 자체가 VGCF 미검증.  **권고: v1 후보로 장부만.**
3. **반경 방향 접근 저항 분리** (R_j = R_contact + R_access(d)) — 손잡이 하나 더 · 단분산 Ø0.15 에서는 R_j,0 와 식별 불가.  **권고: 하지 않는다.**

## 10. 인용 가능 문장 (deck / paper 용)
- (EN) *"For two parallel-contacted MWCNTs (outer diameter ~15 nm) measured in situ in a TEM, the junction resistance scaled inversely with the overlap length for overlaps below ~50 nm, giving interfacial conductivities of 2 × 10²–4 × 10³ S m⁻¹; beyond a threshold of a few hundred nanometres the tube resistance dominated (Hamasaki et al., Nanoscale 14, 11529, 2022)."*
- (EN, 우리 모형) *"Our length-scaled junction law assumes a constant junction conductance per unit contact length, as observed for short CNT overlaps; the saturation of the effective conductance of long contacts is left to the distributed junction edges and the fibre's axial resistance (a discrete transmission line). No VGCF–VGCF junction measurement is available."*
- (KR) *"Hamasaki 등 (2022) 은 TEM 안에서 두 MWCNT 의 겹침 길이를 바꿔, 50 nm 이하의 짧은 겹침에서 접합 저항이 길이에 반비례함을 보였고 계면 전도도를 10²–10³ S/m 로 냈다."*

## 11. 주의 / 한계 (over-claim 방지) ★
1. **두 단자 측정** — R₀ (탐침 · 기판 접촉) 를 상수로 둘 뿐 따로 재지 않았다.  R_total (27–277 kΩ) 은 접합 저항이 아니다.
2. **같은 쌍의 양 면 α 가 6 배 다르다** (+ 270 · × 45 kΩ·nm, Fig. 3(a)) — 저자는 *"almost the same resistance … good reproducibility"* 라 적지만 그것은 절대 저항 이야기이고, 기울기 α (계면 전도도) 는 접촉 기하에 민감하다 (저자도 "sensitive to the geometry of the contact").  ⇒ σ_inter 는 **자릿수 밴드**로만.
3. **표본 수** — 짧은 겹침 15 nm 쌍 셋 (그중 둘은 같은 쌍) · 긴 겹침 둘 + 망원경식 하나.  오차막대 · 적합 불확도 없음.
4. **간극 창 (l₁ = 0.68 nm) 은 가정** — l/C 가 0.5 nm 위에서 평탄하다는 기하 논리로 고른 값이다.  C 를 바꾸면 σ_inter 가 그만큼 바뀐다.
5. **문턱 100–300 nm 는 ρ_CNT ≈ 10⁻⁶ Ω m 가정** — 측정된 σ_CNT (2–4 × 10⁵ S/m = 2.5–5 × 10⁻⁶ Ω m) 를 쓰면 문턱이 √ 만큼 짧아진다.
6. **반경 방향 저항 무시** — 저자 스스로 망원경식 결과 (α ~6000 kΩ·nm) 로 그 가정이 깨질 수 있음을 적는다.
7. **외력 없는 vdW 접촉 · 진공 · 탈도핑 상태** — 압밀 (수백 MPa) 하 · 고체전해질 · PTFE 사이 · 공기 노출 표면의 VGCF 접합과 다르다.
8. **MWCNT (아크 · 지름 8–24 nm) ≠ VGCF (흑연화 · Ø0.15 µm · 중공 · 나무테 구조)** — §3-5 환산은 기하 산술일 뿐이다.
9. **교차 접촉 데이터 없음** — 우리 침대의 접합은 대부분 교차 (점) 다.  교차 크기는 `fuhrer2000_…` · `nirmalraj2009_…` (SWCNT) 를 볼 것.
10. Seebeck 근거 (ref 24) 는 *"in preparation"* — 확인 불가.

## 12. 용어 미니-글로서리
- **나란한 접촉 (parallel contact)**: 두 선형 도체가 옆면을 맞대고 겹친 접촉 · 겹침 길이 x 가 접촉 면적을 정한다.
- **α (계면 기울기)**: R_inter = α/x 의 계수 [Ω·m] — 길이당 계면 컨덕턴스의 역수.
- **간극 창 l₀ · l₁**: 두 외벽이 전도에 기여한다고 보는 간격 범위 (0.34–0.68 nm) — 그 안의 호 길이 = C.
- **문턱 길이 √(α/β)**: 계면 항과 본체 항의 x 미분이 같아지는 겹침 길이 · 전송선 전달 길이 λ 의 1.155 배.
- **전달 길이 (transfer length, λ)**: 전송선에서 전류가 한 도체에서 다른 도체로 넘어가는 특성 길이 · 접합이 이보다 길면 실효 컨덕턴스가 포화한다.
- **전류 쏠림 (current crowding)**: 계면 저항이 작을수록 전류가 겹침의 끝 쪽으로 몰리는 현상.
- **망원경식 MWCNT (telescoped)**: 바깥 벽을 벗겨 안쪽 튜브 (core) 를 바깥 튜브 (housing) 에서 빼낸 동축 쌍.
- **λ_model**: 우리 분산판 v0 에서 R_j,0 · L_par · 섬유 r′ 가 정하는 모형 내부 전달 길이.

## 13. 이 카드가 확인하지 못한 것 (n/a)
- FEM 소프트웨어 · 격자 · 경계 세부 (SI 미기재) · 각 쌍의 정확한 내경 · 벽 수 · R₀ 의 크기 · 적합 불확도 · 측정 온도 (상온이라는 서술뿐) · ref 24 (in preparation) · **VGCF–VGCF 접합의 어떤 측정값도 이 논문에 없다**.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

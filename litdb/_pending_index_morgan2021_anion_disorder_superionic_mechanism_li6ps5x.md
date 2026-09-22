# 병합 대기 — `morgan2021_anion_disorder_superionic_mechanism_li6ps5x`

> ⚠ **번호 정정 2026-09-22**: 이 파일은 처음에 `§J-29` 를 제안했는데, 같은 날 먼저 병합된
> `he2018` 이 **J-29** 를 가져갔다(J-30 jung2026 · J-31 marcolongo · J-32 wang2026 까지 찼다).
> 그래서 **J-33** 으로 민다. 병합자는 이 번호가 아직 비어 있는지 `comparison_vs_ours.md` 에서
> 한 번 더 확인하고 넣어라 — 대기 파일이 여럿이면 또 겹친다.

> 작성 2026-09-22 · digest 본체 = `litdb/papers/morgan2021_anion_disorder_superionic_mechanism_li6ps5x.md`
> ⛔ **이 세션은 `INDEX.md` · `comparison_vs_ours.md` · `db/literature/refs.json` 을 건드리지 않았다.**
> 다른 에이전트가 그 파일들을 병합 중이라는 지시를 받았다. 아래는 **붙여넣기용 초안**이다.
> ⛔ **커밋도 하지 않았다.**

---

## ① `INDEX.md` 행 (SE 축 · 아지로다이트·DFT/AIMD 절에)

| `papers/morgan2021_anion_disorder_superionic_mechanism_li6ps5x.md` **(본문 15 pp + SI 2 pp · 그림 17장 중 12장 실독 — 미독 5장은 전부 도식)** | **[외부·AIMD·⭐⭐⭐ 아지로다이트 "무질서 → superionic" 기전의 정본 · ⛔ 물성값 0건 → A–D 4축 진입 금지]** ✅ **Benjamin J. Morgan\* (단독 저자)** (University of Bath 화학 + **The Faraday Institution**), "**Mechanistic Origin of Superionic Lithium Diffusion in Anion-Disordered Li₆PS₅X Argyrodites**" (***Chem. Mater.* 33, 2004−2018 (2021)**, DOI 10.1021/acs.chemmater.0c03738; **OPEN**; 접수 2020-09-21 / 게재 2021-03-03; refs **119** · `Fig. 1`–`Fig. 15` + `Table 1` · **SI 는 2 pp, `Fig. S1`·`S2` 뿐**; 데이터 Bath RDA `10.15125/BATH-00814` CC BY 4.0 + 분석 노트북 Zenodo `10.5281/zenodo.4338578` MIT — **아직 미확보**). **계**: `Li₆PS₅I`·`Li₆PS₅Cl` × S/X 자리반전 **0 % / 50 % / 100 %** = **6 궤적** (⚠ **Br 은 계산 안 했다** — 제목의 X = Cl,Br,I 에 속지 말 것). **AIMD 설정**: **VASP · PBEsol(⚠ PBE 아님) · PAW**(Li [He] · P [Ne] · S [Ne] · Cl [Ne] · I [Kr]) · 이완 **52 원자 단위셀 · ecut 700 eV · 2×2×2 MP · MP ID-985592** → MD **2×2×2 = 416 원자(N_Li 192) · ecut 280 eV · Γ 점만 · 500 K 단일온도 · dt 2 fs · NVE 2 ps(50 스텝 재규격화) + NVT 2 ps 평형 · 생산 70 ps · 격자는 0 % 배열 영압값으로 전 계 고정**. **후처리**: 50 스텝(100 fs)마다 **inherent structure**(CG 극소화, Stillinger–Weber 계보) → 사면체 자리 사상(Deiseroth type 0–5) → **전이행렬** → 자리–자리 g(r) + **퍼콜레이션 문턱**(`crystal-torture`) → **CSM 배위다면체 분류**(pymatgen ChemEnv) → **끈 길이 분포**(Donati/Glotzer 식, Δt = 5 ps). 도구는 저자 자신의 `vasppy`·`site-analysis`·`polyhedral-analysis`·**`Kinisi`**·`crystal-torture`. 🔴🔴 **우리 관점의 1순위 사실 — 이 논문에는 D·Ea·σ 가 한 개도 없다**: 온도가 **500 K 한 점**이라 아레니우스 자체가 없고, MSD 곡선 외에 확산계수 수치가 본문·SI 어디에도 없다. **무질서 배열은 수준당 1 개**(무작위, 선택 기준 미기재)이고 **I 와 Cl 이 같은 50 % 배열을 공유**하며 **속도 시드도 1 개**다 ⇒ **구조 산포(배열 간 Ea·D 폭)를 이 논문에서 얻을 수 없다.** 유일한 불확실도는 `Fig. 3` 의 **부트스트랩 95 % 띠**인데, **같은 저자의 `mccluskey2025`(공저) 가 MSD 의 계열상관+이분산 때문에 OLS/부트스트랩류가 D 오차를 한 자릿수 과소평가한다고 자기 손으로 증명했다** ⇒ 그 띠를 정량 근거로 인용 금지. 🔑 **핵심 주장 3층**: ① **`Fig. 3`** — 0 %·100 % 는 MSD 정체(D ≈ 0), 50 % 만 직선. **100 % 도 갇힌다** ⇒ *"S 가 4a 를 차지해서" 가 아니라 **4a/4c 무질서 자체가 필요조건***. ② **`Fig. 4` + `Fig. 5`** — 자리 *점유*는 100 % 가 최고(type 2 ≈0.47, type 4 ≈0.07)인데 확산은 0 ⇒ **점유가 아니라 경로 연결성**. 전이행렬 인쇄값: **0 %** 2→5 1.00 · 5→2 0.04(I)/0.30(Cl) · 5→5 **0.96(I)/0.70(Cl)**, **2→2 와 5→4 가 없다**; **100 %** 2→2 0.67(I)/0.35(Cl) · 4→5 1.00 · 5→2 0.91/0.78 · 5→4 0.09/0.22, **5→5 가 없다**; **50 %** 여섯 칸 전부 살아 있다. ⭐ **각주 76 이 우리 언어로 번역해 준다**: *"**2→2 와 5→4→5 가 Schlenker 의 두 intercage 경로**"* ⇒ **`deklerk2016` 의 doublet/intracage/intercage 와 잇는 명시적 사전**. ③ **`Fig. 7`·`Fig. 8`·`Fig. 9`·`Fig. 11`·`Fig. 15`** — 정렬 음이온은 Li 자리를 S 쪽으로 **규칙적으로** 밀어 긴 자리쌍을 만들고(죽은 경로), 무질서는 그 밀림을 **무작위화**해 짧은 경로가 퍼콜레이션한다; 동시에 이웃 4a·4c 의 S 가 **동시에 SLi₆ 를 만들 수 없어**(기하 좌절) **SLi₆/SLi₇ 가 섞이고**, 그래서 Li 이동이 **SLi₇+SLi₆ → SLi₆+SLi₇ = 순 배위수 불변**의 저에너지 과정이 된다(정렬계에서는 [SLi₆+SLi₆]→[SLi₅+SLi₇] 라 **Frenkel 쌍 형성**에 해당). **📐 figure-read 회수값**(논문에 숫자 없음): **퍼콜레이션 문턱** I **2.42 / 1.78 / 2.40** · Cl **2.32 / 1.80 / 2.28 Å** (0/50/100 %) ⇒ 무질서가 **≈0.5 Å (22–26 %)** 낮춘다 · **MSD(70 ps)** I 8.5 / **26.5** / 11 · Cl 11.5 / **46** / 12.5 Å² · **S–Li/X–Li 첫피크 차 Δ** I 0.62 / 0.40 / 0.45 · Cl 0.13 / **0.03(겹침)** / 0.15 Å · **7배위 분율** I 50 % **≈0.42** vs Cl 50 % **≈0.63** · **최대 끈 길이** I 0 % 4 · I 100 % 4 · Cl 0 % 6 · Cl 100 % 8 · I 50 % 8 · **Cl 50 % 13**. **각주 80 정확값**(본문 축자): 다면체 간 Li 교환률 **I 0 %·100 % = 0** · **Cl 0 % = 0.002 /polyhedron/ps** · **Cl 100 % = 0.019** ⇒ (우리 유도) 70 ps 동안 각각 0회 / ≈4.5회 / ≈43회. **각주 79**: 6배위 분율 I 0 % 100 % · I 100 % 100 % · Cl 0 % 99.98 % · Cl 100 % 99.57 %. ⛔⛔ **제일 자주 오인용되는 지점 — "협동 운동 = superionic" 이 이 논문에 정면으로 걸린다**: 본문 축자 *"lithium mobility is effected by **concerted ion motions in all our systems**"* — **확산 0 인 네 계에도 협동이 있다**(4-Li 강체 팔면체 회전 · 3-Li Bailar twist). 판별자는 협동의 **존재**가 아니라 **위상과 분포 모양**이다: 정렬계는 **닫힌 고리 + n ≤ 4 절벽**(I 0 % 는 ln P 가 n 에 대해 **증가**: −1.62 → −0.68), 무질서계는 **열린 끈 + 기하분포**. ⭐ **저자 자신이 과냉각 유리액체의 string-like 확산·동역학 불균일과 유비**(refs 56, 97, 99–101) ⇒ **우리 유리 캠페인으로 넘어오는 가장 값진 한 줄**. **🔴 비판**: **수준당 배열 1개 · 선택기준 0 · 시드 1개**(`kim2024` 는 같은 50 % 의 두 배열에서 σ_RT 23.3 vs 37.1 mS/cm = 1.6× 차를 보고한다) · **부트스트랩 띠가 저자 2025 기준으로 과소** · **이완 700 eV vs MD 280 eV**(수렴시험 미보고, 280 은 S/P PAW ENMAX 수준) · **격자를 0 % 값으로 전 계 고정**(무질서의 부피 기여가 설계상 제거, 민감도 0) · **thermostat 이름이 없다**(NVT 라고만) · **MSD 적합 창·절편 규약 미선언** · **끈 δ · 배위 `r_coord` · 모서리 `r_edge` 세 컷오프가 본문에 없다**(노트북에만) · **70 ps 는 짧다**(Cl 50 % 곡선이 ≈55 ps 이후 꺾인다) · **본문 vs 그림 불일치 2건**(§4.3 의 100 % 전이 목록이 `Fig. 5`·`Fig. 6c` 캡션과 다르다 / `Fig. 7` Cl 100 % 의 5−2·5−4 순서가 본문 서술과 반대로 보인다) · **"50 % = 실험 Li₆PS₅Cl" 이 실험값이 아니다**(Rayavarapu 중성자 4a:4c ≈ 3:7 · de Klerk 최적 75 % · Kim 2024 MTP 최적 25 %) · **실험 0 · 검증 0**(Minafra 의 Li₆PS₅I 중성자는 type 2 점유를 지지하지 않는데 *"2.5 % 는 회절로 못 본다"* 로 방어). ⛔ **인용금지**: *"Morgan 의 Ea/D/σ"*(존재하지 않는다) · *"Cl 이 I 보다 1.7× 빠르다"*(저자 주장 아님 + He-식 오차 ≈±23 % 로 경계선) · *"Morgan 이 disorder **앙상블** 을 돌렸다"*(수준당 1 배열) · *"Morgan 이 Li₆PS₅Br 를 계산했다"* · *"우리 유리엔 cage 가 없다(Morgan)"*(유리 0회) · `Fig. 3` 의 95 % 띠를 불확실도 근거로. | **🔧 방법 원전 = 기전 원전**(§J-33 신설 제안) · **§A 주석**(값 없이 기전 문장만) · ⛔ **A–D 물성 4축에 수치로 넣지 않는다 — 값이 0건이다** |

---

## ② `comparison_vs_ours.md` §📑 Reference key 행

| **[Morgan21Mech]** ⭐⭐⭐ **아지로다이트 "음이온 무질서 → superionic" 기전의 정본** · ⛔⛔ **D·Ea·σ 가 0건 → A–D 물성 4축 진입 금지** · 🔴 **"협동 운동 = superionic" 오인용의 정면 반례** | **Benjamin J. Morgan\*** (**단독 저자**, University of Bath 화학 + **The Faraday Institution**) 2021 ***Chem. Mater.* 33, 2004−2018** (DOI 10.1021/acs.chemmater.0c03738; **OPEN**; refs 119 · **SI 2 pp, `Fig. S1`·`S2` 뿐**) — "**Mechanistic Origin of Superionic Lithium Diffusion in Anion-Disordered Li₆PS₅X Argyrodites**". **AIMD 6 궤적** = `Li₆PS₅I`·`Li₆PS₅Cl` × 자리반전 0/50/100 % · **VASP · PBEsol · 416 원자 · Γ · 500 K 단일온도 · dt 2 fs · 생산 70 ps** · **수준당 무작위 배열 1개(I·Cl 공유) · 시드 1개**. 🔑 **핵심**: 100 % 자리반전도 갇힌다 ⇒ **무질서 자체가 필요조건**; 자리 *점유*는 100 % 가 최고인데 확산 0 ⇒ **점유 ≠ 연결**; **각주 76 이 "2→2 · 5→4→5 = intercage"** 라고 못박아 `[dK16]` 과 잇는다; 정렬은 Li 자리를 S 쪽으로 **규칙적**으로 밀어 경로를 죽이고, 무질서는 **무작위**로 밀어 퍼콜레이션 + **SLi₆/SLi₇ 좌절**로 배위수 불변 Li 교환을 연다. **figure-read 회수**: 퍼콜레이션 문턱 무질서 **≈1.8 Å** vs 정렬 **≈2.3–2.4 Å** · 7배위 분율 Cl 50 % 0.63 vs I 50 % 0.42 · 최대 끈 길이 Cl 50 % **13** vs 정렬 **4–6**. **각주 80**: 다면체 간 교환률 I 0 %·100 % **0** / Cl 0 % **0.002** / Cl 100 % **0.019** per polyhedron per ps. ⛔ **Ea 0 · D 0 · σ 0 · Br 미계산 · 실험 0 · thermostat 미기재 · MSD 창 미선언** | ✅ `papers/morgan2021_anion_disorder_superionic_mechanism_li6ps5x.md` — 판정은 **§J-33**(방법·기전 원전) + **§A 주석**(값 없이 기전만) | AIMD 전용 (실험 0 · MLIP 0 · NEB 0 · 전자구조 0) |

---

## ③ `comparison_vs_ours.md` 에 넣을 블록 — **§J-7 계열의 새 절 제안 `J-33`**

> ⛔ **A–D 물성 4축 표에 행을 만들지 않는다** — 이 논문은 **D·Ea·σ·gap·탄성·ESW 가 전부 0건**이다.
> 값 없는 행을 4축에 넣으면 표가 무의미해진다(§J-7 머리말 규율).
> 아래는 **`🔧 방법 원전`** 성격의 독립 절 초안이다. 절 번호는 병합 시점의 마지막 번호 + 1 로.

### J-33. 🔧 **기전 원전 — [Morgan21Mech] 가 "무질서 → superionic" 을 어떻게 세우나, 그리고 우리 지표에 무엇을 요구하나** (2026-09-22 신설 제안)

**J-33-a. 우리가 이 논문에서 **못** 가져오는 것 (먼저 못박는다)**

| 우리가 기대한 것 | 이 논문 | 결론 |
|---|---|---|
| 무질서 **배열 간** Ea·D 산포의 폭 | **배열이 수준당 1 개** · Ea·D 수치 **0 개** | ❌ **없다.** 우리 유리 분산비 판정의 외부 기대치가 **여기서 나오지 않는다** |
| Haven 비 / 상관 보정계수 | **미측정** ("Haven" 0회, σ 미계산, NE 미사용) | ❌ `marcolongo` 의 *"argyrodite 이식 근거 없음"* 판정 **그대로 유효** |
| MSD 적합 창·절편 규약 | **미선언** (D 를 적합하지 않으므로) | ❌ *"Morgan 도 같은 창"* 이라고 쓸 수 없다 |
| Ea 의 intra/inter 분해 | **없음** (온도 1 점) | ❌ 그 숫자는 `[dK16]` 에서 가져온다 (Cl intercage 0.18/0.27/0.25 eV @300/450/600 K) |

**J-33-b. MD 규약 한 줄 대조** (판정 아님 — 나란히만)

| 항목 | **[Morgan21Mech]** | 우리 결정계 (modelc·lpsocl) | 우리 유리 카드 (`lpscl_smallcell_glass_md_estimand_2026_09_21`) |
|---|---|---|---|
| 힘 | AIMD · VASP · **PBEsol** | MLIP · UMA-s-1p1 (omat) | 동일 |
| 셀 / N_Li | 416 원자 / **192** | box331 **558** | **120** 원자 |
| 격자 | **0 % 배열 값으로 전 계 고정** | 계별 이완 | 담금질 산출 |
| 온도 | **500 K 1 점** | **600/800/1000 K 3 점** | **400/465/550 K 3 점** |
| 각 온도 시간 | **70 ps** | 200 ps (box331 400 ps) | **400 ps** |
| 평형화 | NVE 2 ps(50 스텝 재규격화) + NVT 2 ps | 5 ps | 5 ps |
| dt | **2 fs** | 2 fs | 2 fs |
| thermostat | **NVT, 이름 미기재** | Langevin, friction 0.02 | 동일 |
| **MSD 창 / 절편** | **미선언 / 미선언** | **2–50 ps / 자유절편** | **2–50 ps / 자유절편** |
| 원점 평균 | 미선언 (쓴 패키지 `Kinisi` 는 다중원점 — **패키지에서 유추**) | 단일원점 | 단일원점 |
| Haven | 미측정·미사용 | **NE, H = 1 가정** | 동일 |
| 아레니우스 점 | **0** | 3 | 3 |
| 배열·시드 | **수준당 1 · 시드 1** | comp2 d-level × cfg 3 · Ea 오차막대 600 K 3-시드 | **담금질 구조 시드 5** |
| 불확실도 보고 | **MSD 부트스트랩 95 % 띠뿐** | Ea ± (3-시드) | Ea **중앙값 + IQR**, 풀링 금지 |

**J-33-c. 🔴 그들 오차막대에 대한 자기모순 — 저자 본인이 4년 뒤 뒤집었다**

`Fig. 3` 의 95 % 띠는 **부트스트랩**(ref 73 Efron 1979)이고 패키지는 **`Kinisi`** 다.
그런데 `papers/mccluskey2025_accurate_diffusion_coefficients_uncertainties.md`
(= **McCluskey, Coles, Morgan**, *JCTC* 2025, 21, 79−87 — **같은 Kinisi, 같은 Morgan**)가
**MSD 점의 계열상관 + 이분산 때문에 OLS·블록·부트스트랩류가 D 오차를 한 자릿수 이상 과소평가**하고
블록법은 **체계적 하한**임을 SI S-II 에서 정면 기각했다.
⇒ ⛔ **`Fig. 3` 의 띠를 "이 정도 불확실도다" 로 인용하지 않는다.**
🟢 **우리에게 좋은 소식**: 우리 유리 카드가 **Ea 중앙값 + IQR (시드 풀링 금지)** 를 택한 것이
이 함정 바깥에 있다 — 우리는 **적합 잔차가 아니라 독립 재현의 산포**를 보고한다.

**J-33-d. ⭐ 우리 지표에 대한 요구 — "점유·부피" 에서 "연결성" 으로**

`Fig. 4` + `Fig. 5` 는 **자리 점유율이 가장 높은 계(100 % 자리반전: type 2 ≈0.47, type 4 ≈0.07)의
확산계수가 0** 이라는 직접 반례다.
⇒ 🔴 **우리 BVSE 채널%(above-min ≤ iso) 도 부피·점유 지표다 — 같은 사거리 안에 있다.**
**작업거리**: comp1/modelc BVSE 맵에 **채널%와 함께 "연결 성분의 무한성(퍼콜레이션 여부)"** 을 찍는다.
저자가 쓴 `crystal-torture` (ref 71, O'Rourke & Morgan, *JOSS* 4, 1306 (2019))가 오픈소스라 바로 쓸 수 있다.
⚠ 새 스크립트를 만들기 전에 `tools/comp1_v3/` 의 기존 BVSE 도구에 **플래그로 붙일 수 있는지** 먼저 본다 (코드 규율 사다리 ③).

**J-33-e. ⭐⭐ 유리 카드에 `P(n)` (끈 길이 분포) 추가 제안 — 결과를 보기 전에**

식 (1) `min[|r_i(t+Δt) − r_j(t)|, |r_j(t+Δt) − r_i(t)|] < δ` 는 **자리 정의를 요구하지 않는다**
(좌표와 Δt 만 필요) ⇒ **비정질에 그대로 돌아가는 유일한 분석**이다.
현재 유리 카드 산출물은 `N_pass/15` · Ea 중앙값+IQR · D(465 K) 산포 셋뿐인데, `P(n)` 을 더하면
*"시드마다 Ea 가 다른 것이 **운동 기전이 달라서인가**"* 를 물을 수 있다 (Poisson vs 기하분포).
⚠ **보고량 카드 개정이 선행돼야 한다** — 결과를 본 뒤에 산출물을 늘리면 규율 위반.
구현은 **`tools/ionic/msd_diffusive_check.py` 에 `--strings` 플래그**로 (새 파일 금지).
⚠ **δ 값이 원 논문에 없다** — 우리가 선언해야 하고, 선언값에 대한 민감도를 같이 찍어야 한다.

**J-33-f. ⛔ 우리가 이 논문을 인용해 온 방식 중 과한 것 (정정 대상)**

| 지금 litdb 안의 서술 | 정정 |
|---|---|
| `dutra2025` digest §소득 ③ — *"`Fig. 4c`(Morgan 2021) … **우리 disorder-ensemble MD 의 개념적 정당화**"* | 🟡 **개념은 맞고 방법은 없다.** 원전은 **수준당 배열 1 개**다. 정확한 문장 = *"무질서가 확산을 지배한다는 **기전** 의 근거"* 이지 *"배열을 여러 개 돌려야 한다는 **방법론** 의 근거"* 가 아니다. (그 digest 는 이미 *"⚠ 단 무질서를 계산에 넣는 방법은 안 준다"* 를 적어 뒀다 — **그 단서가 옳았음이 원전으로 확인됐다**) |
| *"아지로다이트 superionic 기전 = 협동 운동"* (일반 서술) | ⛔ **원전에 정면으로 걸린다.** 협동은 **확산 0 인 네 계에도** 있다. 판별자는 **닫힌 고리 vs 열린 끈 + 기하분포**다 |
| `jeon2026_concerted_li_motion_argyrodite_assi` 를 단독 인용 | ⚠ **이 편을 견제로 함께 건다** |

---

## ④ `db/literature/refs.json` 정정/추가 **제안 문구** (직접 고치지 않았다)

현재 46 항목에 이 논문이 **없다.** 아래 항목을 `references` 배열에 추가할 것을 제안한다.

```json
{
  "id": "morgan2021",
  "authors": "Morgan, B. J.",
  "title": "Mechanistic origin of superionic lithium diffusion in anion-disordered Li6PS5X argyrodites",
  "journal": "Chem. Mater.",
  "volume": 33,
  "pages": "2004-2018",
  "year": 2021,
  "doi": "10.1021/acs.chemmater.0c03738",
  "affiliation": "University of Bath (Dept. of Chemistry) + The Faraday Institution (single author)",
  "key_content": "AIMD (VASP, PBEsol, PAW, 416-atom 2x2x2 supercell, Gamma-only, 500 K, 2 fs, 70 ps production) of Li6PS5I and Li6PS5Cl with 0/50/100% S/X site inversion. Long-ranged Li diffusion occurs ONLY for 50% (disordered); both 0% and 100% ordered models give plateauing MSD, so S/X disorder across 4a and 4c - not the halide identity and not S on 4a - is the necessary prerequisite. Mechanism is two-layered: (i) ordered anions displace average Li site positions toward S in a REGULAR pattern, leaving a non-percolating network of short site-site separations, so specific site-site pathways (2->2 and 5->4, i.e. the two intercage paths, for 0%; 5->5 for 100%) are inactive; disorder randomises those displacements and opens a percolating 3D network; (ii) adjacent S on 4a and 4c cannot both form regular SLi6 cages (geometric frustration), so Li are shared, giving mixed SLi6/SLi7 in which transfer proceeds SLi7+SLi6 -> SLi6+SLi7 with no net coordination change (low energy), versus Frenkel-pair-like [SLi6+SLi6] -> [SLi5+SLi7] in the ordered systems. Concerted motion is present in ALL six models including the four that do not diffuse; the superionic signature is open string-like motion with a geometric length distribution (n up to 13 for 50% Li6PS5Cl) rather than closed 3-4 ion loops.",
  "caveats": "NO diffusion coefficients, NO activation energies, NO ionic conductivities, NO Haven ratio - single temperature (500 K) so no Arrhenius. One random S/X configuration per disorder level (the same 50% configuration reused for both I and Cl), one velocity seed - no configurational or thermal spread is measurable. Br was NOT simulated despite the title. Lattice parameters fixed to the 0% ordered optimum for all systems. Relaxation at 700 eV but MD at 280 eV. Thermostat not named. MSD fitting window and intercept convention not stated. String cutoff delta, coordination cutoff r_coord and edge cutoff r_edge not given in the paper (public notebooks only). Only quantitative uncertainty is a bootstrap 95% band on the MSD, which the same author's later work (McCluskey, Coles & Morgan, JCTC 2025, 21, 79) shows underestimates D uncertainty by roughly an order of magnitude. No experiments.",
  "data_availability": "DFT inputs/outputs: University of Bath Research Data Archive 10.15125/BATH-00814 (CC BY 4.0). Analysis notebooks: Zenodo 10.5281/zenodo.4338578 (MIT). Neither retrieved as of 2026-09-22.",
  "litdb_digest": "litdb/papers/morgan2021_anion_disorder_superionic_mechanism_li6ps5x.md"
}
```

⚠ **기존 항목 정정 제안 — 없음.** 46 항목을 훑었고 이 논문을 잘못 귀속한 항목은 발견되지 않았다.
(단 `refs.json` 에 `deklerk2016`·`kim2024` 계열 항목이 있다면, 이 논문 각주 76 의
*"2→2 와 5→4→5 = intercage"* 사전을 `key_content` 에 교차참조로 한 줄 넣는 것이 유용하다 —
그 두 문헌을 한 문장에 쓸 수 있게 해 주는 유일한 근거다.)

---

## ⑤ 🎤 talk 역링크 — **해당 없음**

`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `litdb/talks/lee2026_skku_mlip_materials_design.md`
하나. 그 대기열에 **이 논문은 없다** (`morgan` · `Mechanistic Origin` · `anion-disorder` 전부 0회).
⇒ digest 머리에 `🎤 관련 발표` 줄을 넣지 않았고, talk 쪽도 손대지 않았다.

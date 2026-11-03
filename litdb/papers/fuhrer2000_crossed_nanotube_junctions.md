# Crossed Nanotube Junctions — Fuhrer (Science 2000) · 교차한 두 SWCNT 의 접합을 4/3/2 단자로 직접 잰 첫 실험 — 금속–금속 접합 ≈ 200 kΩ (0.086–0.26 e²/h · 투과율 2–6 %) · 금속–반도체는 Schottky 로 두 자릿수 낮은 컨덕턴스 · 계산: 접촉력 변형이 투과율을 200 배 올린다

> slug `fuhrer2000_crossed_nanotube_junctions` · DOI `10.1126/science.288.5465.494` · type `exp (crossed SWNT junction contact resistance · 4-, 3- and 2-terminal I–V on SiO2 back-gated devices · AFM) + ab-initio junction transmission (in supplementary)` · PDF `3._Crossed_nanotube_junctions.pdf` · digested `2026-11-03` · status ✅
> *Science* Report 3 쪽 (pp. 494–496 · PDF 5 쪽 = 앞 기사의 끝 · 뒤 기사 (Nepal U–Pb 지르콘) 의 첫 쪽 · AAAS 표지 쪽 포함) · 온라인 보충자료 (계산 세부) 는 **받지 않았다** (n/a) · evidence `fulltext (report only)` · 그림 `4/4 육안 확인` — **4 장 모두 손 크롭** (Science 옆 캡션 판형이라 도구가 그래픽을 못 찾고 뒤 기사의 "Fig. 1. Geologic map of Nepal" 을 대신 잘랐다 → 버림 · `figures.json` `manual_crop`) · 약칭 `[Fuhr00]`
> **계기** — Rint ② 탄소 접합 R_j,0 (모형 내부 보정값 · SBE 1.63 mS/cm 한 점) 의 **sanity band** 와 교차 (점) 접합의 물리 (1저자 11-03 · 다섯 편 묶음).  ⛔ v0 동결 — 값 채택 없음 · 등록 R §7-2: R_j,0 를 문헌 접합 저항과 같은 양으로 부르지 않는다.
> 수치 등급: **stated** · **figure-read ≈** · **derived(ours)**.

---

## 0. ★ 이 카드가 답하는 것

| 질문 | 이 논문의 답 | 등급 · 자리 |
|---|---|---|
| **(b) 접합 하나의 저항** | **MM (금속–금속) 교차 SWCNT**: 4 단자 · 200 K · **200 kΩ (0.13 e²/h)** + 다른 셋 **0.086 · 0.12 · 0.26 e²/h** → **≈ 99–300 kΩ** · 투과율 T_j = G/(4e²/h) ≈ **0.02–0.06** | stated (G · 200 kΩ · T_j) · R 환산 = derived(ours) |
| (b) SS · MS | **SS**: 2 단자 G **≥ 0.011 · 0.06 e²/h** (하한 · 접점 저항 포함) → R ≤ 2.3 MΩ · 0.43 MΩ · **MS**: 저바이어스 투과율 **T_MS ≈ 2 × 10⁻⁴** (두 소자) = MM 보다 **두 자릿수** 낮은 컨덕턴스 → R ≈ 32 MΩ · Schottky 장벽 190 · 290 meV | stated (G · T) · R = derived(ours) |
| (b) 접합 면적 | *"despite the extremely small junction area (on the order of 1 nm²)"* | stated · p. 494 |
| **접촉력 의존** | 계산 (5,5)–(5,5): vdW 간격 0.34 nm 그대로면 **T_j ≈ 2 × 10⁻⁴**, SiO₂ 기판과의 상호작용으로 생기는 **접촉력에 의한 변형**을 넣으면 **T_j ≈ 0.04** (실험과 일치) — **200 배** | stated · p. 494–495 · Fig. 1(B)(C) |
| (a) 길이 법칙 | 해당 없음 — 교차 (점) 접합만 | — |
| (c) 터널 간극 | 별도 간극 분석 없음 — MM · SS 접합을 *"relatively good tunnel contacts"* 로, MS 에는 터널 장벽 + 공핍층 (7 nm, Odintsov) 두 장벽 | stated |
| (d) 망 수준 | 없음 (소자 하나씩) — 동기는 다단자 회로 | — |

**한 줄 판정** — 우리 v0 의 *점 접합 (L_c ≤ L_par)* 에 해당하는 물체를 직접 잰 원전이다.  크기 (≈ 10⁵ Ω) 보다 값진 것은 **같은 기하에서 접촉력 (변형) 하나로 투과율이 200 배** 움직인다는 계산 — R_j,0 는 압밀 상태 (MPM 이 풀지 않는 섬유 접촉 역학) 를 묶은 값이라는 한정어의 근거다.

## 1. 한 줄 요약

UC Berkeley (McEuen · Zettl · Louie) 와 서울대 (임지순) 는 SiO₂/Si 뒤게이트 기판 위에서 우연히 교차한 두 SWCNT (또는 < 3 nm 작은 다발) 의 네 끝에 Cr/Au 전극을 달아, 각 튜브를 금속 (M) · 반도체 (S) 로 판별한 뒤 **MM · SS · MS 교차 접합**을 재었다.  MM 접합의 4 단자 저항은 200 kΩ (0.13 e²/h) 이고 다른 셋도 0.086–0.26 e²/h — 접합 면적이 ~1 nm² 인데도 투과율 2–6 % 의 *"surprisingly good tunnel contacts"* 다.  밀도범함수 계산은 vdW 간격 (0.34 nm) 의 (5,5) 교차가 T_j ≈ 2 × 10⁻⁴ 밖에 안 되지만, 기판이 누르는 접촉력으로 튜브가 변형되면 T_j ≈ 0.04 가 되어 실험과 맞는다고 보였다.  SS 접합도 좋은 터널 접촉 (하한 0.011 · 0.06 e²/h) 이고, MS 접합은 금속 튜브가 반도체 튜브를 공핍시켜 **Schottky 장벽** (190 · 290 meV ≈ E_g/2) 을 만들어 저바이어스 컨덕턴스가 두 자릿수 낮고 정류한다 (+700 mV / −700 mV 에서 ~100 배) — 3 단자로 공핍층 투과율 T_d ≈ 5 × 10⁻³ 을 따로 확인했다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | M. S. Fuhrer¹ · J. Nygård¹ · L. Shih¹ · M. Forero¹ · Young-Gui Yoon¹ · M. S. C. Mazzoni¹ · Hyoung Joon Choi² · Jisoon Ihm² · Steven G. Louie¹ · A. Zettl¹ · **Paul L. McEuen**¹ (교신) |
| 소속 | ¹ Dept. Physics, UC Berkeley + Materials Sciences Division, LBNL · ² Dept. Physics + Center for Theoretical Physics, **Seoul National University** |
| 서지 | *Science* **288** (5465), 494–496 (2000-04-21) · DOI `10.1126/science.288.5465.494` |
| 일자 | 접수 1999-12-23 · 승인 2000-03-09 |
| 시료 | 레이저 증발 SWCNT (Rinzler · Smalley 제공) · 디클로로에탄 초음파 분산 → 기판에 ~15 s 올렸다 씻음 · 높이 ≈ 1.4 nm (단일) 우선 · 일부 < 3 nm 다발 |
| 소자 | 축퇴 도핑 Si 위 **SiO₂ 1 µm** · Cr/Au 정렬표지 (전자빔) · AFM 태핑으로 교차 위치 찾기 → PMMA · 전자빔 · Cr/Au 리프트오프 |
| 연구유형 | 실험 (4 · 3 · 2 단자 I–V · 50–200 K · 게이트) + 제일원리 접합 투과 계산 (보충자료) |
| 같은 묶음 카드 | `nirmalraj2009_swcnt_network_junction_resistance` (망 속 접합 수백 개) · `li2007_tunneling_resistance_cnt_composites` (이 논문을 "100–400 kΩ" 으로 인용) · `hamasaki2022_…` (ref 15 로 인용) · `banerjee2019_…` |

## 3. 핵심 수치 ★

### 3-1. MM · SS 접합

| 양 | 값 | 조건 | 등급 · 자리 |
|---|---|---|---|
| MM 대표 접합 | **200 kΩ** = **G 0.13 e²/h** | **4 단자** (한 튜브 한 팔로 주입 · 다른 튜브 한 팔로 빼기 · 나머지 팔 = 전압 탐침) · **200 K** | stated · p. 494 · Fig. 2(A) □ |
| MM 다른 셋 | **0.086 · 0.12 · 0.26 e²/h** | 같은 측정 | stated |
| (R 환산) | 300.1 · 215.1 · 99.3 kΩ (대표 198.6 kΩ) | R = h/(e²G) · h/e² = 25,812.8 Ω | derived(ours) |
| 투과율 | **T_j = G/(4e²/h) ≈ 0.02–0.06** — "an electron arriving at the junction … has chance of a few percent of tunneling into the other SWNT" | — | stated |
| 접합 면적 | **~1 nm²** | — | stated |
| 두 단자 MM | 튜브 하나의 두 단자 컨덕턴스와 비슷 → 접합 저항이 튜브 + 금속 접점과 **같은 자릿수** | — | stated · p. 494 |
| SS | 두 단자 **0.011 e²/h · 0.06 e²/h** (높은 쪽 = Fig. 2(A) ○) — **하한** (반도체 튜브의 접점이 흔히 매우 저항적) | 200 K | stated · p. 495 |
| (SS R 환산) | ≤ 2,347 kΩ · ≤ 430 kΩ | — | derived(ours) |
| I–V 판독 | MM □: ≈ 100 nA @ ≈ 21 mV (≈ 210 kΩ) · SS ○: ≈ 100 nA @ ≈ 42 mV (≈ 420 kΩ) · ±100 mV 안 선형 | Fig. 2(A) | figure-read ≈ |

### 3-2. 제일원리 계산 (보충자료 · 본문 서술만 확인)

| 구조 | T_j | 자리 |
|---|---|---|
| (5,5)–(5,5) 교차 · **vdW 간격 0.34 nm** (Fig. 1(B)) | **≈ 2 × 10⁻⁴** | stated · p. 494–495 |
| 같은 교차 · **SiO₂ 상호작용이 주는 접촉력 → 접합부 변형** (Fig. 1(C) · ref 16 Hertel 1998) | **≈ 0.04** — 실험과 일치 · "charge density in the contact region became sizeable as the nanotubes became closer and more deformed" | stated · p. 495 |
| 비 | **≈ 200 배** | derived(ours) = 0.04 / 2 × 10⁻⁴ |

### 3-3. MS 접합 (Schottky)

| 양 | 값 | 등급 · 자리 |
|---|---|---|
| 저바이어스 투과율 | **T_MS ≈ 2 × 10⁻⁴** (두 소자 모두) — MM · SS 보다 **두 자릿수 작은** 컨덕턴스 | stated · p. 495 |
| (R 환산) | G = 4 × 2 × 10⁻⁴ e²/h = 8 × 10⁻⁴ e²/h → **≈ 32 MΩ** | derived(ours) |
| 공핍층 투과율 | T_j ≈ 0.04 가정 → **T_d ≈ 5 × 10⁻³** (Odintsov 계산 T_d ≈ 5 × 10⁻³ · 공핍 폭 **7 nm** 와 일치) | stated |
| 장벽 높이 | 순바이어스 선형 구간의 V 절편 → **E_barrier = 190 · 290 meV** (기대 E_g/2 ≈ 250–350 meV · 1–1.5 nm s-SWCNT 의 E_g ≈ 500–700 meV) | stated · p. 496 · Fig. 3 |
| 3 단자 | 반도체 튜브 자체의 선형 컨덕턴스 **4.3 nS** → **T_S = 2.8 × 10⁻⁵** → T_d ≈ T_S^½ ≈ **5.3 × 10⁻³** (2 단자 결과와 일치) | stated · p. 496 · Fig. 4 |
| 정류 | 반도체 튜브 전류 **+700 mV 가 −700 mV 의 ≈ 100 배** · 능동 길이 **~15 nm** | stated · p. 496 |
| 측정 조건 | MS = **50 K · V_g = −25 V** (2 단자) · 3 단자 **100 K** | stated (Fig. 2 · 3 · 4 캡션) |
| 게이트 · 도핑 | V_g 1 V 당 ≈ 2 × 10⁵ e/cm · V_g −25 V 에서 ≈ 5 × 10⁶ holes/cm · E_F ≈ 75 meV (원자가띠 기준) | stated · 주 19 |
| 열활성 | E_barrier 250 meV 에서 T < 300 K 이면 Boltzmann 인자 < 10⁻⁴ → 선형 응답은 터널이 지배 | stated · 주 18 |
| 온도 의존 | MM 은 Luttinger 액체 예상보다 다소 강한 온도 의존 (Coulomb blockade 로 해석) · MS 는 50 K 위에서 약함 | stated · 주 14 · 18 |

## 4. 방법 ★
- **소자 제작**: §2 표 그대로 — 우연히 교차한 튜브를 AFM 으로 찾아 네 팔에 전극 (Fig. 1(A)).
- **튜브 판별**: 상온에서 금속 튜브 = V_g 에 거의 무관한 유한 컨덕턴스 · 반도체 = p 형 (음 V_g 에서 전도).
- **4 단자 (MM)**: 접점 저항을 뺀 **접합만의 저항** — 이 논문의 MM 값이 문헌에서 '접합 저항' 기준점으로 쓰이는 이유.
- **2 단자 (SS · MS)**: 반도체 튜브 접점이 저항적이라 접합 컨덕턴스의 **하한**만.
- **3 단자 (MS)**: 반도체 튜브 양 끝 + 금속 튜브 한 끝 — 반도체 튜브를 곧장 지나는 투과 (T_S) 를 금속 튜브 경유와 분리 (Fig. 4).
- **계산**: Landauer 투과 (ref 15) · 제일원리 (보충자료) · (5,5) 교차 · vdW 간격 vs 기판 접촉력 변형 (Fig. 1(B)(C)).
- ★ **접합 처리**: 교차 (점) 접합 · 접촉력 = 기판 vdW 가 누르는 힘 (외부 하중 없음) · 사이 물질 없음 · 튜브 Ø ~1.4 nm (다발 < 3 nm).

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | (A) 교차 SWCNT 소자의 태핑 AFM (진폭 신호) — 두 튜브 (초록) 가 Cr/Au 전극 (노랑) 넷 사이에 걸침 (B)(C) 계산 구조 — (5,5) 둘 · vdW 간격 (B) vs 접촉력 변형 (C) | (A) = 교차 (점) 접합의 실물 · ★ (B)→(C) 가 **투과율 200 배** — 압밀 상태가 접합을 바꾼다는 한정어의 그림 · 손 크롭 |
| **2** | (A) I–V: MM (4 단자 · 200 K · □) · SS (2 단자 · 200 K · ○) · MS 둘 (2 단자 · 50 K · V_g −25 V · + ×) (B)–(D) MM · SS · MS 의 띠 그림 — MS 에 Schottky 장벽 E_barrier | ★ **(b) 크기 밴드의 근거 그림** — MM ≈ 200 kΩ · SS ≈ 400 kΩ (판독) · MS 는 ±100 mV 에서 거의 0 · 손 크롭 |
| 3 | MS 두 소자의 2 단자 I–V (50 K · ±900 mV) + 순 · 역바이어스 띠 그림 · 점선 = 순바이어스 선형 적합 (V 절편 = 장벽) | 정류 · 장벽 높이 190 · 290 meV · 손 크롭 |
| 4 | (A) MS 소자 3 단자 측정 (100 K) — I_S (반도체 튜브) · I_M (금속 튜브) · 측정 배치 삽도 (B)–(D) 영 · 역 · 순바이어스의 공핍 장벽 | T_S 2.8 × 10⁻⁵ → T_d 5.3 × 10⁻³ · 손 크롭 |

## 6. Post-processing ★
- G 를 양자 단위 e²/h 로 · 투과율 T = G/(4e²/h) (스핀 · 띠 두 겹 = 4 채널) · MS 는 T_MS ≈ T_j·T_d 분해 · 3 단자 T_S ≈ T_d².
- 장벽 높이 = 순바이어스 I–V 선형 구간 외삽의 V 절편.
- 불확도 · 소자 간 산포 통계 없음 (MM 4 개 · MS 2 개 · SS 2 개).

## 7. 우리 DEM+MPM 대비 ★★

> 대상 = Rint ② STEP3 복셀 전자 채널 VGCF–VGCF 접합 v0 (작업 브랜치 HEAD `57f1b2baf`).  frame[5]: MPM 침대 위 수송.  ⚠ 등록 R §7-2 금지: R_j,0 를 *"물성 · 접합 저항 측정값 · 문헌값과 같은 양"* 으로 부르지 않는다.

| 항목 | Fuhrer 2000 | 우리 v0 | 판정 |
|---|---|---|---|
| 접합 꼴 | 교차 (점) · 면적 ~1 nm² | instance · L_c ≤ L_par (0.30 µm) 이면 G = 1/R_j,0 (점 접합) | **같은 범주** (교차) · 크기 범주는 다르다 (Ø 1.4 nm ↔ Ø 150 nm) |
| 크기 | MM 99–300 kΩ (4 단자 · 200 K) | R_j,0 = SBE 보정 (아직 없음) | sanity band 의 한 기둥 — **같은 양 아님** (포트 반셀 · 접근 몫 · 격자에 묶인 모형 내부값) |
| 재료 상태 | SWCNT 의 금속 · 반도체 혼재 → MM · SS 는 좋은 터널 접촉 · MS 는 100 배 나쁨 | VGCF = 흑연화 (반금속) · 모든 VV instance 에 같은 R_j,0 | VGCF 는 MS 같은 이봉 분포의 근거가 없다 (흑연화 섬유 = 금속적) — 단일 R_j,0 와 모순 없음 |
| 접촉력 · 변형 | 계산상 T_j 를 200 배 바꾼다 | MPM 은 섬유 접촉 역학을 풀지 않는다 (등록 R 한정어 ⑩) · instance = 관통 포함 기하 근접 | ★ **R_j,0 는 압밀 (300 MPa 급) 의 접촉 상태를 묶는다** → 압력 · 밀도가 다른 침대로 옮기지 못한다 |
| 측정 온도 | 50–200 K | 상온 (전극 DC 분극) | 온도 의존이 약하다는 서술 (MS > 50 K) 뿐 — 상온 MM 값 없음 |

### 7-1. 왜 SWCNT 값을 VGCF 로 '면적 비례' 시키면 안 되나
- SWCNT 교차 접합은 채널 몇 개의 양자 투과 (G = T·4e²/h) 다 — 면적 비례 법칙이 아니다.  흑연화 Ø0.15 µm 섬유의 교차는 **수백 nm² 의 흑연–흑연 vdW 계면** (Hamasaki 간극 창 산술로 ≈ 160 nm² · `hamasaki2022_…` §3-5) 이라 다른 영역이다.
- 그래도 자릿수 감각은 남는다 [derived(ours) · 가정 의존]: 같은 간극 창의 흑연 계면 전도도 (Hamasaki 2 × 10² – 4 × 10³ S/m) 로 Ø0.15 µm 직교 교차를 셈하면 **≈ 0.9–20 kΩ** — SWCNT 교차 (10⁵ Ω) 보다 1–2 자릿수 낮다.  ⇒ 보정된 R_j,0 가 10⁵ Ω 이상으로 나오면 **깨끗한 흑연–흑연 vdW 교차만으로는 설명이 안 되고** 막 (SE · PTFE · 바인더) · 접근 몫 · 모형 산물이 묶여 있다고 읽어야 한다 (판정 아님 · 읽는 눈금).

### 7-2. 우리 리포의 SWCNT (A14 sheath) 에 대한 메모
- CLAUDE.md 07-21 기록: A14 SWCNT sheath (STEP3 sid 8) 가 있다.  **SWCNT 를 접합 모형에 넣을 일이 생기면** MS 접합이 MM 의 1/100 (Fuhrer) 이라 VGCF 와 같은 R_j,0 하나로 묶을 수 없다 — v0 범위 밖 (VGCF–VGCF 만 정량 · `CJUNC_QUALIFIERS` 둘째 줄).

## 8. 적용 인사이트
- ① **접촉력 (압밀) 한정어** — "R_j,0 = 압밀 · 침대 상태의 묶음 · 다른 압력 · 밀도로 옮기지 않는다" 를 한 줄로.  근거 = 같은 교차의 T_j 가 변형으로 ×200 (계산 · 이 논문).
- ② **sanity band 의 기둥 하나** — 교차 SWCNT MM ≈ 1–3 × 10⁵ Ω (4 단자 · 200 K).  우리 R_j,0 를 그 옆에 적을 때 **같은 양이 아니라는 문장**과 함께 (등록 R §7-2).
- ③ **'좋은 터널 접촉' 의 뜻** — MM 접합 하나가 튜브 + 금속 접점과 같은 자릿수 → SWCNT 망은 접합과 튜브가 비슷하게 기여할 수 있다 (망 수준은 `nirmalraj2009_…` 가 접합 지배를 실측).

## 9. 적용 후보 (11-03)

### (가) 지금 v0 안에서 — 값 채택 없음
1. **한정어 (문서)** — 등록 R §7-1 ⑩ (`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md:278`) "접합 instance = 관통 포함 기하 근접 (MPM 은 섬유 접촉 역학을 풀지 않는다)" 뒤에: *"… 따라서 R_j,0 는 압밀이 만든 접촉력 · 변형 상태를 묶는다 (교차 SWCNT 계산에서 변형이 투과율을 ≈ 200 배 바꾼다 — Fuhrer 2000) — 다른 압력 · 밀도의 침대로 옮기지 않는다."*
2. **sanity band 표 (보고 전용)** — 보정된 R_j,0 를 보고할 때 (등록 R §8 불합격 · 무정보 보고 · 또는 판정 기록 옆) 문헌 접합 크기를 **같은 양이 아니라는 문장과 함께** 나란히: 교차 SWCNT MM 99–300 kΩ (이 카드) · SWCNT 망 접합 평균 34 kΩ–6.8 MΩ (`nirmalraj2009_…`) · 나란한 MWCNT 계면 α 45–990 kΩ·nm (`hamasaki2022_…`) · 계산 터널 5 kΩ–10 MΩ (`banerjee2019_…`) · 우리 산술 Ø0.15 µm 흑연 교차 ≈ 0.9–20 kΩ.  자리 후보 = 설계 §1-2 #10 (`docs/reviews/rint_carbon_additive_design_v1_20261020.md:56`) 비고 칸.
3. **금지 문장 보탬 (문서)** — 등록 R §7-2 에: *"R_j,0 가 CNT 접합 문헌 밴드 안 · 밖이라는 이유로 '물리적으로 타당 · 비물리적' 이라 쓰기 (VGCF–VGCF 측정값 없음 · 지름 · 흑연화 · 막 · 압력 · 온도가 다르다)."*

### (나) 1저자 비준 필요
1. **압력 · 밀도 의존 R_j** (접촉력 → 간극 → 투과) — 섬유 접촉 역학 (MPM 미해결) 과 간극 → 투과 법칙이 둘 다 없다.  **권고: 하지 않는다** (한정어로).
2. **SWCNT 첨가제 접합 (A14) 을 넣는다면 M/S 이봉 R_j** — 금속 1/3 · 반도체 2/3 같은 통계 가정 + MS = MM × 100 (이 논문) — 새 법칙 · 손잡이.  **권고: 장부만 (v0 = VGCF–VGCF 만).**

## 10. 인용 가능 문장
- (EN) *"Four-terminal measurements on crossed metallic single-walled carbon nanotubes gave junction resistances of about 200 kΩ (0.086–0.26 e²/h, transmission 2–6 %) at 200 K despite a junction area of order 1 nm², whereas metal–semiconductor junctions were two orders of magnitude less conductive because of a Schottky barrier (Fuhrer et al., Science 288, 494, 2000)."*
- (EN) *"First-principles calculations in the same work showed that contact-force-induced deformation raises the junction transmission from ~2 × 10⁻⁴ (van der Waals spacing) to ~0.04, i.e., the junction conductance depends strongly on the mechanical contact state."*
- (KR) *"교차한 금속성 SWCNT 의 접합 저항은 4 단자로 ≈ 200 kΩ (200 K) 이고, 같은 기하에서 접촉력에 의한 변형이 투과율을 약 200 배 바꾼다 (계산) — 접합 저항은 재료값이 아니라 접촉 상태의 함수다."*

## 11. 주의 / 한계
1. **소자 수가 적다** — MM 4 · SS 2 · MS 2 · 3 단자 1.  산포 통계 없음.
2. **온도 50–200 K** — 상온 MM 값은 이 논문에 없다.  MM 의 온도 의존은 *"somewhat stronger … than expected"* (Coulomb blockade 해석).
3. **SS 는 하한** (2 단자 · 반도체 접점 저항 포함) — "R ≤" 로만 쓴다.
4. **계산 세부 (보충자료) 를 보지 않았다** — 함수 · 기저 · 접촉력 크기 · 변형 크기는 n/a.  T_j 2 × 10⁻⁴ · 0.04 는 본문 서술값.
5. **Li 2007 의 "100–400 kΩ" 인용은 이 논문의 반올림** — MM 4 단자 값 (99–300 kΩ) 과 SS 2 단자 하한 (≤ 0.43 · ≤ 2.3 MΩ) 을 합친 표현이다.  원값은 이 카드 §3 을 쓸 것.
6. **SWCNT (Ø ~1.4 nm · 양자 채널) ≠ VGCF (Ø 0.15 µm · 흑연화 다벽)** — 크기 전이 금지 (§7-1).
7. 기판 위 교차 · 대기 노출 이력 · 계면 오염 정보 없음.

## 12. 용어 미니-글로서리
- **MM · SS · MS 접합**: 금속–금속 · 반도체–반도체 · 금속–반도체 SWCNT 교차.
- **e²/h**: 컨덕턴스 양자 단위 (≈ 38.7 µS · h/e² ≈ 25.8 kΩ) · SWCNT 의 이상 컨덕턴스 = 4e²/h.
- **투과율 T**: 전자가 접합을 건너갈 확률 · G = T·4e²/h (Landauer).
- **4 단자 측정**: 전류 · 전압 단자를 나눠 접점 저항을 뺀 측정.
- **Schottky 장벽**: 금속–반도체 접촉의 전하 이동으로 반도체 쪽에 생기는 공핍 장벽 — 정류 · 저바이어스 컨덕턴스 감소.
- **공핍층 투과율 T_d**: 공핍 장벽을 터널하는 확률 (여기 7 nm 폭 · ≈ 5 × 10⁻³).
- **접촉력 변형**: 기판 vdW 가 튜브를 눌러 교차부가 찌그러지며 간격이 줄고 파동함수 겹침이 커지는 것.

## 13. 이 카드가 확인하지 못한 것 (n/a)
- 보충자료 (계산 · 추가 그림) · 각 소자의 튜브 지름 · 교차 각 · 상온 MM 값 · Fig. 1(A) 축척 막대의 길이 (캡션 · 본문에 숫자 없음) · VGCF 나 다벽 섬유 교차에 대한 어떤 값도 이 논문에 없다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

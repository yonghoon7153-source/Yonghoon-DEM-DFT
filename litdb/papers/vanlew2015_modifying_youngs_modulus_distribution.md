# 단일 pebble 압쇄실험의 E 분포로 DEM 입자별 Young률을 수정 (Hertz 접촉) — Van Lew (Fusion Eng. Des. 2015)

> slug `vanlew2015_modifying_youngs_modulus_distribution` · DOI `10.1016/j.fusengdes.2015.06.012` · type `DEM (Hertz 접촉 + 단일입자 압쇄실험 → 입자별 E)` · PDF `90f2f374-Modifying_Young_s_modulus_in_DEM_simulations_based_on_distributions_of_experimental_measurements.pdf` · digested `2026-08-25` · status ✅

---

## 0. 왜 이 논문을 읽었나 (독해 목적 — 결론 먼저)

지도교수 질문: **"E_eff = 1.35 GPa (DEM) / 1.53 (MPM) 의 출처가 있나? 합리적인가?"**
`coetzee2017_dem_calibration_review.md` §8(p.136)이 **이 논문[236]** 을 우리 연화의 *방향* 근거로 재인용했다.
1차 출처를 열어 확인한 결과 — **세 줄 요약**:

1. ✅ **방향은 지지된다. 단, 재인용이 전한 것보다 *더 강하고 다른* 형태로.**
   이 논문의 실측 결론은 "분포가 있으면 무르다"가 **아니라** —
   **"개별 입자의 겉보기 E 는 소결 벌크 문헌값보다 실측으로 훨씬 낮다"**(κ̄ ≈ 0.54 stated-derived,
   개별 최소 κ ≈ 0.14 digitized).  즉 **입자 ↔ 벌크 격차 자체가 측정으로 존재한다.**
2. ⛔ **크기는 지지되지 않는다.**  그들의 평균 연화는 **1.84×** (90 → 49 GPa), 배치 내 최연약 입자도
   **~7×** 다.  우리 **18×** 는 그 평균의 **~10배**, 최극단의 **~2.6배** 밖이다.
   ⇒ **이 논문으로 18× 를 정당화하면 안 된다.**  게다가 **연화의 *종류*가 다르다** (§7-2).
3. ⚠ **재인용에 실질적 드리프트가 있다.**  Coetzee 가 전한 *"a distribution vs a constant"* 대비는
   **평균이 같은 두 계의 비교가 아니다** — 이 논문의 Set B 는 분포를 가지면서 **동시에 평균이 1.84× 낮다**.
   **상수 Ē = 49 GPa 통제군이 없다.**  ⇒ **"불균질성 자체가 무르게 한다"는 이 논문으로 말할 수 없다.**
   (상세 검증 = §9-c)

---

## 1. 한 줄 요약

세라믹 breeder pebble(Li₄SiO₄ · Li₂TiO₃) **개별 입자를 앤빌 사이에서 압쇄**해 얻은 힘–변위 곡선에
**Hertz 식을 역으로 피팅**해 입자마다 겉보기 Young률 E_peb 를 뽑고, 소결 벌크값 대비 비
**κ = E_peb/E_bulk ∈ [0,1]** ("softening coefficient")의 **확률분포**를 실측한 뒤,
그 분포를 **10종의 입자 타입으로 이산화해 DEM 침대의 입자에 무작위 배정**한다.
6 MPa 단축압축에서 **수정-E 침대가 더 무르고(변형 1.9 → 2.6 %), 접촉력 꼬리가 얇으며, 압쇄 예측 입자수가
(대부분) 적다** — ⇒ *"과거 DEM 압쇄 연구는 문헌 벌크 E 를 써서 파단을 과대예측했을 가능성이 크다."*

**핵심 성격**: 이것은 **Coetzee 분류의 Direct Measuring Approach**(입자 물성을 직접 재서 넣기)의
교과서적 사례다.  그리고 그것이 가능한 이유는 **입자가 0.5–1 mm 라 낱개로 잡아 누를 수 있기 때문**이다.

---

## 2. 메타

| 저자 | 소속 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|---|
| J.T. Van Lew, **Y.-H. Park**, A. Ying, M. Abdou | UCLA MAE + **National Fusion Research Institute (대전)** | Fusion Engineering and Design **98–99** (2015) **1893–1897** | `10.1016/j.fusengdes.2015.06.012` | **Li₄SiO₄** (KIT 제공) · **Li₂TiO₃** (NFRI 제공) — 핵융합 블랭킷 tritium breeder | 실험(단일입자 압쇄) + DEM |

- SOFT 2014 (Symposium on Fusion Technology) 논문집. 접수 2014-10-23 / 개정 2015-06-03 / 게재 2015-07-22.
- **5쪽 학회 논문** — 이 길이가 아래 "n/a" 목록의 길이를 설명한다(§12).
- 자금: US DOE FES DE-FG02-86ER52123 + UCLA–NFRI Task Agreement.
- ⚠ **배터리 무관.** 소재는 리튬 세라믹이지만 **breeder pebble**(중성자 → 삼중수소 증식용)이다.
  Li₄SiO₄·Li₂TiO₃ 는 이온전도체로 쓰이는 물질이 아니고, 여기서 중요한 물성은 **E 와 압쇄강도뿐**이다.

---

## 3. 핵심 수치 — stated / digitized / DERIVED 를 엄격히 분리

### 3.1 STATED (본문·표에 적힌 값)

| 양 | 값 | 조건 | 비고 |
|---|---|---|---|
| **E_bulk (Li₄SiO₄)** | **90 GPa** | 소결 펠릿, RT | ⚠ **그 문장에 출처 인용이 없다** (ref [9] Reimann 은 소재 설명용) |
| **E_bulk (Li₂TiO₃)** | **124 GPa** | 소결 펠릿, RT | ⚠ 동일 — ref [7] Gierszewski 가 intro 에 있으나 이 수치에 직접 안 붙음 |
| **Ē (Li₄SiO₄ 배치 평균, = DEM Set B 입력)** | **49 GPa** | — | *"we fit to lithium orthosilicate pebbles where the average stiffness was Ē = 49 GPa"* |
| 압쇄 시험 개수 (Li₄SiO₄, KIT) | **31** 개 | RT, 습도 **비제어** | |
| 압쇄 시험 개수 (Li₂TiO₃, NFRI) | **42** 개 | RT, 습도 **비제어** | Fig 2b 에 그려진 것이 **이쪽** |
| κ 정의 | **κ = E_peb / E_bulk ∈ [0, 1]** | — | 벌크가 **상한**이라는 가정 |
| DEM 입자 | **Li₄SiO₄, d_p = 0.5 mm (R_p = 0.25 mm)** | — | |
| 침대 입자수 | **8000** | — | ⚠ 아래 기하와 모순 (§3.3) |
| 벽 | **E = 220 GPa** ("강철 모사"), 무한 반경·무한 질량, Hertz 힘법칙 | x_lim = ±20 R_p | |
| 주기경계 | y_lim = ±15 R_p | | |
| 침대 높이 | z_lim ≈ 20 R_p | "approximate" | |
| Set B 타입 수 | **10 종** | E 를 **이산·무작위**로 배정 | |
| 반경 분포 (A.3, B.3, B.4) | Gaussian, 평균 R_p, **sd = R_p/15** | CV ≈ **6.7 %** | A.1·A.2·B.1·B.2 는 단분산 |
| 마찰계수 μ | **0.2** (A.1, A.3, B.1, B.3) / **0.3** (A.2, B.2, B.4) | | 입자-입자. 벽마찰 n/a |
| 하중 | **6 MPa 까지 단축(oedometric) 압축, 1 사이클** | | ⚠ §3.4 "stress-controlled" vs §4 "constant-velocity" **상충** |
| **거시 변형 @ 6 MPa** | **Set A(상수 E) 1.9 %** / **Set B(수정 E) 2.6 %** | 그룹 평균 | ★ **논문이 준 유일한 정량 대비** |
| **압쇄 예측** (Table 1) | A.1 **0.3** · A.2 **1.0** · A.3 **0.9** · B.1 **0.6** · B.2 **0.8** · B.3 **0.4** · B.4 **0.7** | 최대응력 시점 | ⚠ 표 머리에 **단위가 없다**; 본문은 *"percentages"* 라 부름 |

### 3.2 DIGITIZED — **추세 전용, 절대값 인용 금지**

**Fig 2b (κ 히스토그램, Li₂TiO₃ n=42):**

| 양 | 값 | 근거 |
|---|---|---|
| κ 범위 | ≈ **0.14 → 1.00** | 축 눈금 |
| ⇒ **배치 내 E 산포** | ≈ **7×** (E ≈ 17 → 124 GPa) | 1/0.14 |
| 10-bin 카운트 | 15 · 6 · 3 · 3 · 4 · 2 · 2 · 2 · 2 · 3 | 막대 높이 |
| **합** | **42** ✓ | **정확히 stated 배치 크기와 일치** → 10 등폭 bin(폭 0.086) 재구성이 맞다는 강한 방증 |
| κ̄ (bin 중심 가중평균) | ≈ **0.42** | ⇒ E_peb ≈ 52 GPa (Li₂TiO₃) |
| 최빈 bin | κ 0.14–0.23 에 **15/42 = 36 %** | 분포가 **약한 쪽으로 강하게 치우침** |

**Fig 1 (압쇄 곡선):**

| 양 | Li₂TiO₃ (Fig 1a) | Li₄SiO₄ (Fig 1b) |
|---|---|---|
| 공칭 직경 | 1 mm | 0.5 mm |
| **실측 직경 범위**(컬러바) | ≈ 0.885 – 0.975 mm | ≈ 0.42 – 0.60 mm |
| 힘 범위 | 0 – **48 N** | 0 – **11 N** |
| 앤빌 이동(s) 범위 | 0 – **0.034 mm** | 0 – **0.017 mm** |

**Fig 4 (응력–변형, 단일 곡선 판독):**

| 양 | Set A (상수 E) | Set B (수정 E) | 비 |
|---|---|---|---|
| 최대 변형 @6 MPa | ≈ 2.08 % | ≈ 2.75 % | 1.32 |
| **제하 후 잔류 변형** | ≈ **1.20 %** | ≈ **1.33 %** | **1.11** |
| ⇒ 회복(탄성) 변형 | ≈ 0.88 %p | ≈ 1.42 %p | **1.61** |

★ **논문이 말하지 않는 분해**: 추가 컴플라이언스 **+0.67 %p** 중 잔류로 남는 것은 **+0.13 %p 뿐**
   ⇒ **~80 % 가 제하 시 회복된다** (0.54/0.67).
   ⇒ **연화가 바꾼 것은 주로 *탄성 접촉 컴플라이언스*이고, 남는 치밀화(잔류 변형)는 거의 안 바뀌었다.**
   (§7-4 에서 우리 porosity 축과 대조 — 우리에게 매우 중요한 지점)

**Fig 5 (접촉력 확률분포, log–log):**

| 양 | 값 |
|---|---|
| 분포 본체 | 피크 F ≈ 0.5–1 N, P ≈ 0.5 — **7개 침대 전부 한 곡선으로 겹침** |
| 갈리는 곳 | **꼬리만** (F ≳ 3 N, P ≲ 10⁻²) |
| 꼬리 최대 | **A.2 (상수 E, μ=0.3) ≈ 15–20 N** — 압도적 최우측 |
| | 나머지 상수-E ≈ 8–9 N · 수정-E(원) ≲ 9 N |
| ⚠ 표본 | P ≈ 4×10⁻⁴ 는 접촉 **수십 개** 수준 — 시드 1개라 꼬리는 통계가 없다 |

### 3.3 DERIVED (ours) — 두 stated 수치의 산술 / 그들 식의 대수

| 양 | 값 | 유도 |
|---|---|---|
| **κ̄ (Li₄SiO₄, DEM 이 실제로 쓴 값)** | **49/90 = 0.544** | ⇒ **평균 연화 1.84×** |
| 변형비 B/A @6 MPa | **2.6/1.9 = 1.37×** | 반올림 밴드 **1.31 – 1.43** (1.9·2.6 이 2자리) |
| Hertz 팩 예측 (ε ∝ E^(−2/3)) | **1.84^(2/3) = 1.50×** | σ ∝ E·ε^{3/2} ⇒ 고정 σ 에서 ε ∝ E^(−2/3) |
| **⇒ 판정** | 관측(1.37, 밴드 1.31–1.43)과 회복-변형 판독(1.61)이 **1.50 을 사이에 둔다** | **"평균 E 하나로 전부 설명된다"와 모순 없음** = 분포 고유효과의 증거 **없음** |
| Eq.(7) 상수 C | **(4/3)(15/8)^{3/5} = 1.944** | |
| **압쇄 문턱의 E 의존** | **F_c ∝ E*^{2/5}** ⇒ Set B 문턱이 **1.84^{0.4} = 1.27× 낮다** | ★★ **논문이 전혀 언급하지 않는 역효과** (§5.3) |
| 압쇄시험 접촉당 겹침 | δ = s/2 ⇒ **δ/d ≈ 1.7 %** (양 배치 동일) | Eq.(2) 대수에서 s = 2δ 확인 |
| **⇒ 우리 대비** | 우리 pure-SE ⟨δ⟩ = **직경의 11–12 %** = 그들 실측 상한의 **~7배 깊이** | 그들 Hertz 피팅의 **검증구간 밖**에서 우리가 돈다 |
| ⚠ **침대 기하 모순** | φ = 8000·(4/3)π R³ / (40·30·20 R³) = **1.40** | **1 을 넘는다 = 불가능.** z 를 ±20R_p 로 읽어도 φ = 0.70 > RCP 0.64 ⇒ **{8000, 상자} 중 하나가 오기.** 침대 부피·초기 packing fraction **재현 불가** |

### 3.4 n/a — **논문에 없는 것 (크게 적는다)**

| 없는 것 | 왜 문제인가 |
|---|---|
| **ν_p, ν_a (Poisson 비)** — 한 번도 안 나온다 | κ 역산이 E* 를 통과하므로 **ν 없이는 κ 재현 불가** |
| **앤빌 재료·E_a** | 동일. 게다가 저자들이 ref [11](Zhao, *"Influence of **plate material** on the contact strength"*)을 인용하면서 자기 앤빌은 안 밝힌다 |
| **DEM 코드명** | LIGGGHTS·LAMMPS·EDEM·Yade·PFC 전부 **0회**. ref [6](저자 본인 2014)로 넘김 |
| **COR / 감쇠 / 타임스텝 / 회전마찰 / 벽마찰** | 접촉모델이 "Hertz" 라는 것 외 전부 미상 |
| **시드/실현 개수** | 침대당 **1개로 보인다** — Table 1 에 오차막대 없음 |
| **초기 packing fraction / porosity** | 압밀 축 대조 **원천 불가** |
| **W_ε,l (압쇄 변형에너지) 분포의 수치** | Eq.(7)의 무작위화 입력인데 파라미터·범위 모두 미보고 |
| **Weibull 형상·척도 모수** | *"Weibull"* 이라는 낱말이 **Fig 2b 부캡션 한 곳**에만 있고 **모수는 0개** |
| **DEM 이 실제로 쓴 Li₄SiO₄ κ 분포 그림** | *"omitted for brevity"* — **쓴 분포는 안 보여준다**. 보이는 것(Fig 2b)은 **다른 배치(Li₂TiO₃)** |
| **침대 스케일 실험 검증** | **없다.** 논문이 스스로 미래과제로 미룸(§4 마지막) |
| **6 MPa 초과 압력 / 온도 의존 / 습도 수치** | 단일 압력·RT·습도 "비제어" |
| **porosity·상대밀도 어떤 형태로도** | ⇒ **이 논문은 우리 porosity floor 축에 아무것도 주지 않는다** |

---

## 4. 시뮬레이션 방법 ★

### 4.1 접촉법칙 — **순수 Hertz, 소성 없음**

```
Eq.(1)   F_n = (4/3) · E* · √R* · δ^{3/2}
         1/E* = (1−ν_i²)/E_i + (1−ν_j²)/E_j        1/R* = 1/R_i + 1/R_j
```
- **탄성 Hertz 뿐이다.** 항복캡(Thornton–Ning) 없음 · 이력(hooke/hysteresis) 없음 · 점착 없음 ·
  EEPA 없음 · multi-contact 결합 없음.  전단(Mindlin) 항은 μ 만 언급되고 식이 안 나온다.
- ⇒ **`elasto-plastic` 축에서 이 논문은 우리보다 *뒤*에 있다.**  우리 LIGGGHTS 는 hooke/hysteresis
  (접촉 소성)를 쓰고, Varkey/Giannis/Zunker 는 그 위에 있다.

### 4.2 ★ 입자 처리 (우리 "무질서 처리"의 DEM 대응) — **가장 중요한 칸**

| 축 | 이 논문 | 판정 |
|---|---|---|
| 형상 | **완전 강체 구** | 형상 변화 0 |
| 크기 분포 | 단분산 **또는** Gaussian(CV 6.7 %) — **둘 다 시험** | 매우 좁다 |
| **강성 분포** | ★ **입자마다 다른 E** — 10 종을 **무작위·공간 무상관**으로 배정 (Fig 3 우측이 그 증거) | ★ **이 논문의 유일한 신규성** |
| 소성 | **없음** (탄성 Hertz) | δ 프록시조차 없다 |
| 파쇄 | **후처리 판정만** — 입자가 실제로 쪼개지지 않는다 (§5.3) | 기하 불변 |
| 결합/bond | 없음 | |

⇒ **이 논문의 "불균질"은 *물성(E)의 입자간 분산*이지, 형상·크기·소성의 불균질이 아니다.**
   우리와 대비하면: 우리는 **PSD(12:4:1 bimodal)로 기하 불균질**을 주고 **E 는 전 입자 단일값**이다.
   **정확히 직교하는 선택**이다.

### 4.3 침대·경계·프로토콜

- 벽: Hertz 힘법칙을 따르는 **가상 평면**(R→∞, m→∞), **E_wall = 220 GPa**.
- x 방향 벽 ±20 R_p · **y 주기경계** ±15 R_p · z 높이 ≈ 20 R_p · N = 8000.
  ⚠ 이 네 수치는 **서로 모순**한다 (§3.3 — φ = 1.40).
- **7 침대 = 2 (E 규약) × {단분산/Gaussian R} × {μ 0.2 / 0.3}** 중 6조합 + B.4.
  ⚠ **A.4 (상수 E, Gaussian R, μ=0.3)가 없다** → B.4 는 짝이 없다 ⇒ **완전한 factorial 이 아니다.**

| 침대 | E 규약 | 반경 | μ | 짝 |
|---|---|---|---|---|
| A.1 | E = 90 GPa | 단분산 | 0.2 | ↔ B.1 |
| A.2 | E = 90 | 단분산 | 0.3 | ↔ B.2 |
| A.3 | E = 90 | Gaussian | 0.2 | ↔ B.3 |
| — | *(A.4 없음)* | | | ⚠ **B.4 무짝** |
| B.1 | Ē = 49 (10종 분포) | 단분산 | 0.2 | |
| B.2 | Ē = 49 | 단분산 | 0.3 | |
| B.3 | Ē = 49 | Gaussian | 0.2 | |
| B.4 | Ē = 49 | Gaussian | 0.3 | |

---

## 5. ★★ 절차를 식 수준으로 — "어떻게 E 를 수정했는가"

### 5.1 STEP 1 — 압쇄시험을 Hertz 식으로 다시 쓴다

구를 **두 평면 앤빌** 사이에 놓고 한쪽 앤빌 이동 s 를 잰다.  접촉이 위·아래 2개이므로 **s = 2δ**,
그리고 구–평면이라 R* = R_p = d_p/2.  Eq.(1)에 넣으면

```
Eq.(2)   F_n = (1/3) · E* · √(d_p · s³)          1/E* = (1−ν_p²)/E_p + (1−ν_a²)/E_a
```

> ✅ **대수 검증(ours)**: (4/3)·E*·√(d_p/2)·(s/2)^{3/2} = (4/3)·(1/√2)·(1/2√2)·E*√(d_p s³) = **(1/3)E*√(d_p s³)** ✓
> ⇒ Eq.(2)는 Eq.(1)과 **정확히 일치**한다.  동시에 **s 는 앤빌 총이동 = 접촉당 겹침의 2배**임이 확정된다
> (이게 §3.3 의 δ/d ≈ 1.7 % 를 확정하는 근거다).

**논문의 논증 (§2 마지막)** — 인용 가치 높음:
> *"From Eq. (2), we see that standard Hertz theory, wherein a **single value for Young's modulus** is used,
> is **not appropriate** for pebbles studied in ceramic breeders.  If single values of E_p and ν_p are employed,
> then **variation in pebble diameters can not alone explain the variation of curves** of Fig. 1."*

⇒ **논리 구조**: Eq.(2)에서 곡선을 흩뜨릴 수 있는 자유도는 d_p 와 E* 둘뿐이다.  d_p 산포는 실측돼 있고
(Fig 1 컬러바: 0.885–0.975 mm = ±5 %) **F ∝ √d_p 이므로 ±2.5 % 밖에 못 흩뜬다.**
관측 산포는 **수 배**다.  ⇒ **남은 자유도는 E 뿐이다.**  ★ 이것이 이 논문의 핵심 추론이고,
**깔끔한 소거 논증**이다 (우리가 배울 수 있는 논증 형식).

### 5.2 STEP 2 — κ 를 역산한다 (자유변수 실질 0)

```
Eq.(3)   κ = E_peb / E_bulk  ∈ [0, 1]
```
절차: E_bulk 를 문헌 소결 펠릿값으로 **고정**(90 / 124 GPa) → κ ∈ [0,1] 을 **전수 격자탐색**
(*"we iterate over all values of κ ∈ [0,1]"*) → 각 pebble 의 실측 F–s 곡선에 **최소잔차 피팅**.

**물리적 가정 (§3.2, 원문)**:
> *"the production technique yields pebbles with **slightly different internal structures**.
> The differences in internal structure then cause the pebble to have a **different apparent modulus of
> elasticity**; which will vary from some strong limit value. … Assuming this strong value is the **upper limit**,
> **imperfections in the pebbles will lead only to a reduction, or softening** of the pebble."*

⇒ **κ ≤ 1 은 물리가 아니라 *가정*이다.**  "벌크 = 상한, 결함은 낮추기만 한다"를 **선언**하고 탐색을
[0,1] 로 자른다.  Fig 2b 의 최우측 bin 이 정확히 1.0 에 붙어 있는 것은 **그 절단의 그림자일 수 있다**
(1.0 이 자연스러운 최빈값이 아니라 경계).  ⚠ 논문은 이 가능성을 논의하지 않는다.

- **보정인가 실측유도인가?** → **실측유도에 가깝다.**  거시 응답(porosity·벌크강성)을 타깃으로
  되맞추는 단계가 **없다**.  E 는 **입자 단위 실험에서만** 나온다.
- ⚠ 다만 **완전 무보정은 아니다**: ① E_bulk 선택(출처 미인용) ② ν_p·ν_a·E_a 선택(미보고) ③ bin 개수 10
  ④ [0,1] 절단 — **네 개의 판단**이 들어간다.  "자유변수 0" 이라고 쓰면 과장이다.

### 5.3 STEP 3 — 압쇄 예측: 랩 시험 ↔ 침대 접촉의 **변형에너지 등가**

Hertz 힘을 겹침에 대해 적분해 접촉 변형에너지를 얻는다:

```
Eq.(4)(5)  W_ε = ∫₀^{δ_c} (4/3)E*√R* δ'^{3/2} dδ' = (8/15) E*_b √R*_b δ_{c,b}^{5/2}
```
**가정 (원문)**: *"if each contact interaction is integrated to the proper critical overlap, **the strain
energies will be equal at that contact**"* ⇒ **W_ε,l (랩, 앤빌 사이 압쇄까지) = W_ε,b (침대 접촉)**.
그래서 침대 안의 임계 겹침과 임계 힘이 나온다:

```
Eq.(6)  δ_{c,b} = [ 15 W_ε,l / (8 E*_b √R*_b) ]^{2/5}
Eq.(7)  F_{c,b} = C · (E*_b)^{2/5} · (R*_b)^{1/5} · (W_ε,l)^{3/5},    C = (4/3)(15/8)^{3/5} ≈ 1.944
```
> ✅ **대수 검증(ours)**: Eq.(4)→(5), (5)→(6), (6)→(7) **전부 맞다** (지수 2/5·1/5·3/5 재유도 일치).

**이 방식의 정체성 — 우리 litdb 안에서 정확히 어느 편인가:**
> *"The methodology of this crush prediction, based on **a critical contact force**, stands in contrast to a
> similar approach reported by **Zhao et al.** where they based crush prediction on the **total strain energy of a
> pebble summed among all contacts** acting upon it [11].  This prediction is based on the results of
> **Russell et al.** where they showed that the mechanics of a contact between spheres in an ensemble are
> **highly localized** and therefore the internal stresses of the contact are **independent of the number or
> magnitude of neighboring contacts** [12]."*

⇒ ★★ **Van Lew 는 *이진(binary) 접촉* 가정을 명시적으로 채택하고, 입자 전체 합산(다접촉)을 명시적으로 기각한다.**
   이것은 우리 litdb 의 **`giannis2021_stress_based_multicontact_dem`(입자 응력텐서 trace 로 모든 접촉을 결합)**
   · **`varkey2026_multicontact_elastoplastic_dem`** 과 **정반대 입장**이다.
   ⚠ 그리고 이 가정은 **저응력에서만** 안전하다 — Giannis/Varkey 자신이 다접촉 결합이 **ρ > 0.7 에서만
   중요하다**고 한다.  6 MPa 침대는 거기 못 간다.  ⇒ **Van Lew 의 선택은 자기 응력영역에서 정당하고,
   우리 300 MPa 영역으로 옮기면 정당하지 않다.**

**★★ 논문이 놓친 것 (ours) — 왜 압쇄 효과가 작고 한 쌍은 뒤집히는가:**
Eq.(7)은 **F_c ∝ (E*_b)^{2/5}** 다.  ⇒ **E 를 낮추면 접촉력만 내려가는 게 아니라 *압쇄 문턱도 같이 내려간다*.**
- 문턱 하락: 1.84^{0.4} = **1.27× (−21 %)**
- 힘 하락: **평균 접촉력은 사실상 안 내려간다** — Fig 5 본체가 7침대 전부 겹친다(고정 거시응력에서
  평균 접촉력은 힘균형이 정하지 E 가 정하지 않는다).  **꼬리만** 얇아진다.
⇒ **"더 적은 파단"은 [꼬리 삭감] vs [문턱 21 % 하락]의 경합 결과다.**  꼬리 삭감이 작은 침대에서는
**역전이 나야 한다** — 그리고 실제로 **A.1(0.3) < B.1(0.6) 으로 역전한다** (§6, Table 1).
Fig 5 에서 μ=0.2 짝(빨강)의 꼬리가 거의 안 갈리는 것과 정합적이다.  ⇒ **역전은 오기가 아니라 물리일 수 있다.**

---

## 6. 결과 — 절 단위 상세

### 6.1 거시 응력–변형 (Fig 4)

- **6 MPa 도달 변형: Set A 1.9 % · Set B 2.6 %** (그룹 평균, stated) ⇒ **1.37×**.
- 논문의 설명은 **한 문장**이고, 그 문장이 이 카드의 핵심 반전이다:
  > *"**Intuitively**, the pebble beds **with smaller Young's modulus** (with circle markers) are more compliant
  > to external loads."*
  ⇒ ★ **논문 자신은 원인을 "분포"가 아니라 "더 작은 E(=평균)"로 돌린다.**
- Fig 4 캡션: *"The constant Young's modulus beds all had **much firmer responses** for all parametric cases."*
- **파라미터 서열 (stated)**: *"the **largest contributor** to stress–strain response is the **Young's modulus**.
  The coefficient of friction and radius distribution had comparatively **insignificant** influence."*
  ⇒ **구속 단축압축이 강성을 고립시키는 시험**이라는 Coetzee §5.5 규범과 **독립 일치**
  (우리 300 MPa 냉간압축이 정확히 그 칸 — `coetzee2017` 카드 §③).
- ★ **논문이 안 한 분해 (digitized, ours)**: 추가 컴플라이언스 +0.67 %p 중 **~80 % 가 제하 시 회복**된다
  (잔류 변형은 1.20 → 1.33 %p 로 +0.13 %p 만 증가).
  ⇒ **연화는 탄성 접촉 컴플라이언스를 키웠지 남는 치밀화는 거의 안 바꿨다.**
  ⚠ **우리 계로 곧장 옮기지 말 것** — 6 MPa 는 재배열이 거의 안 일어나는 영역이고, 우리 300 MPa 는
  잔류(소성·재배열)가 지배한다.  실제로 **우리 사내 E-스윕에서는 porosity 가 E 에 반응한다**
  (E_SE 1.35/1.5/2.0 → ε_sphere 13.47/12.77/15.01 %) ⇒ **압력영역이 다르면 E 가 무엇을 움직이는지가 다르다.**

### 6.2 접촉력 분포 (Fig 5)

- *"the **majority of the contacts in all the beds are equally small**"* — 본체는 7침대 공통.
- *"The pebble beds with the constant Young's modulus are **always higher** for their comparable version with
  distributed Young's modulus."* ← **꼬리 얘기다** (본체는 겹치므로).
- *"For pebble beds with comparable Young's modulii and radii, **higher coefficients of friction generally have
  higher peak contact forces**."* ⇒ **꼬리는 μ 가 지배한다.**
- *"Pebble beds' radius distributions have **much less impact** on peak contact forces than either coefficient
  of friction or Young's modulus."*

★ **우리에게 중요한 구조**: **평균 응답은 E 가 지배하고, 힘의 꼬리는 μ 가 지배한다.**
   ⇒ **거시 응답에 맞춘 E 보정은 힘의 꼬리를 고정하지 못한다.**  파단은 꼬리에서 일어난다.

### 6.3 압쇄 예측 (Table 1) — ⚠ **논문의 헤드라인이 자기 표와 어긋난다**

| 짝 (같은 μ·같은 반경규약) | A (상수 E) | B (수정 E) | 방향 |
|---|---|---|---|
| μ=0.2, 단분산 | A.1 = **0.3** | B.1 = **0.6** | ⛔ **B 가 2배 더 많다 — 반례** |
| μ=0.3, 단분산 | A.2 = 1.0 | B.2 = 0.8 | ✅ B 가 적다 (−20 %) |
| μ=0.2, Gaussian R | A.3 = 0.9 | B.3 = 0.4 | ✅ B 가 적다 (−56 %) |
| μ=0.3, Gaussian R | *(A.4 없음)* | B.4 = 0.7 | ⚠ 비교 불가 |

**논문의 주장 (두 곳)**:
- Abstract: *"**In all cases** studied here, the pebble beds with modified Young's modulus had smaller overall
  contact forces and **fewer predicted crushed pebbles**."*
- §4: *"we compare similar parameteric pebble beds and **in each case** pebble beds with modified Young's modulus
  overall predict **smaller percentages** of broken pebbles."*

⛔ **둘 다 자기 Table 1 이 반증한다.**  짝지을 수 있는 3쌍 중 **1쌍(A.1/B.1)이 반대**이고,
   그것이 하필 **가장 온건한 기준 케이스**(최저 마찰·단분산)다.
> ✅ **검증**: 두 개의 독립 텍스트 추출기(pdftotext 계열 · PyMuPDF)로 Table 1 을 각각 뽑아 **동일**하게 나왔다
> — 추출 오류가 아니다.

**추가 정직 고지 (ours)**:
- **Set A 내부 산포만으로 0.3 → 1.0 = 3.3배**다 (μ 와 반경규약만 바꿔서).
  ⇒ **다른 파라미터의 효과가 A↔B 효과만큼 크다.**
- 침대당 **실현 1개, 오차막대 없음** ⇒ 0.3 vs 0.6 의 차가 잡음인지 판별할 수단이 논문 안에 없다.
- ⇒ **"수정 E 가 파단을 줄인다"는 이 논문 데이터로 *경향*조차 확정되지 않는다.**
  살아남는 문장은 **"파단 예측이 입력 E 에 강하게 의존한다"** 까지다.

### 6.4 논문 자신이 인정한 미완성

> *"A pebble bed geometry **more directly comparable to oedometric compression experiments should be used
> to allow direct comparison and validation** of the numerical models."*

⇒ ★★ **침대 스케일 검증이 0 이다.**  실측은 **단일입자 레벨에서만** 있고, DEM 침대 결과는
   **어떤 실험과도 대조되지 않았다.**  §9-b 판정의 결정적 근거.

---

## 7. Figure set ★

파일: `litdb/figures/vanlew2015_modifying_youngs_modulus_distribution/` (5장, 이 카드에서 추출)

| Fig | 무엇을 보여주나 | 우리가 쓸 것 / 주의 |
|---|---|---|
| **1** | 압쇄 F–s 곡선 다발. **(a) Li₂TiO₃ d=1 mm · (b) Li₄SiO₄ d=0.5 mm**, 컬러 = **개별 직경**(0.885–0.975 / 0.42–0.60 mm) | ★ **"같은 배치인데 강성이 수 배 흩어진다"의 원자료.**  δ/d ≤ 1.7 % 로 **얕은 겹침**임을 확정하는 그림.  ⚠ 몇몇 곡선은 평탄역+점프(표면 asperity 좌굴)를 보이는데 논문이 논의 안 함 |
| **2** | (a) 실측(실선) vs **입자별 수정-E Hertz 곡선**(점선) 중첩 — 피팅 품질.  (b) **κ 히스토그램** | ★★ **이 논문의 정본 그림.**  (b)는 **Li₂TiO₃ (n=42)** 이고 **DEM 이 쓴 Li₄SiO₄ 분포가 아니다.**  ⚠⚠ **부캡션이 이미지 안에 있어 텍스트 추출에 안 잡힌다** — "Weibull" 이라는 낱말이 **오직 여기에만** 있다 |
| **3** | 침대 렌더링. 좌 = Set A **단일 타입(전부 파랑)**, 우 = Set B **10 타입 컬러맵(type 1–10)** | ★ **E 배정이 공간적으로 무상관(랜덤)**임을 시각적으로 확증 — 군집/구배가 없다.  우리가 "분포를 넣는다"고 할 때 **어떤 분포인지**(공간 상관 유무)를 명시해야 함을 보여줌 |
| **4** | 응력–변형 7침대, **사각=상수 E · 원=수정 E**, 재하+제하 1사이클 | ★ 유일한 정량 대비.  ⚠⚠ **축 제목이 아예 없다** (단위는 본문에서 역추정: y=MPa, x=%).  ⚠ 캡션은 *"**Gaussian** distribution of Young's modulus"* 라 하는데 본문은 *"discrete, random … to satisfy the distribution seen from experimental data"* — **상충**(§12-③) |
| **5** | 접촉력 확률분포(log–log) + 꼬리 확대 inset | ★ **본체 붕괴 / 꼬리만 분기** 구조.  우리 fracture 축에 직접 대응(파단은 꼬리 사건).  ⚠ 꼬리는 접촉 수십 개 · 시드 1개 |

---

## 8. Post-processing ★

| 무엇 | 어떻게 | 우리 대응 |
|---|---|---|
| **κ 역산** | Hertz Eq.(2)에 κ ∈ [0,1] **전수 격자탐색** 최소잔차 피팅, pebble 1개당 1값 | 우리에겐 대응 절차가 **없다** (E 를 거시 porosity 로 맞춤) |
| **분포 추정** | 히스토그램(10 bin) → **Weibull 로 모델링**(부캡션 1회, 모수 미보고) | — |
| **DEM 투입** | 분포를 **10 종 이산 타입**으로 잘라 입자에 **무작위 배정** | 우리 PSD 배정과 자리는 같으나 **물성 축**이라는 점이 다름 |
| **거시 응답** | σ(플래튼) – ε(침대 높이), 1 사이클 재하/제하 | 우리 wallP·Heckel 과 같은 계열 (단 6 MPa, Heckel 없음) |
| **접촉력 분포** | 최대응력 시점 스냅샷의 **정규화 PDF, log–log** | 우리 force-chain/fracture 통계와 대응 |
| **압쇄 판정** | Eq.(7) 로 **접촉당 임계력 F_c** 계산, 강도값을 **입자에 무작위 배정**(W_ε,l 분포에서), 초과 접촉 집계 | ★ 우리 **Auerbach 취성 판정**의 구조적 형제 (§10-③) |
| ❌ 없는 것 | **Heckel · porosity · 배위수 · tortuosity · coverage · 전달 σ · 응력장** — 전부 0 | ⇒ 이 논문은 **우리 전달 삼중항·압밀 축에 아무 데이터도 주지 않는다** |

---

## 9. ★★★ 판정 3개 (지도교수 질문에 대한 직답)

### (a) 우리 18× 연화의 **방향**을 지지하는가?  **크기**는?

| | 판정 |
|---|---|
| **방향** | ✅ **지지한다 — 단, 재인용보다 더 강한 형태로.**  "실측된 개별 입자의 겉보기 E 는 소결 벌크 문헌값보다 **낮다**" 가 **31+42 = 73 개 입자의 직접 측정**으로 확립된다.  즉 **DEM 에 문헌 벌크 E 를 그대로 넣는 것이 틀렸다**는 명제가 실측으로 서 있다. |
| **크기** | ⛔ **지지하지 않는다.**  평균 **1.84×** (κ̄ = 0.544, stated-derived) · 다른 배치 평균 ≈ **2.4×** (κ̄ ≈ 0.42, digitized) · **배치 내 최연약 개체도 ~7×** (digitized).  우리 **18×** 는 그 평균의 **~10배**, 최극단의 **~2.6배** 밖. |
| **분포 고유효과** | ⛔ **이 논문으로 말할 수 없다.**  Set B 는 *분포* + *평균 1.84× 하락* 을 **동시에** 바꿨고 **상수 Ē = 49 GPa 통제군이 없다**.  게다가 우리 판독(§3.3)에서 관측 변형비가 **순수 평균-E Hertz 예측(1.50×)과 모순이 없다** ⇒ **분포가 평균 너머로 추가 연화를 냈다는 증거 0.** |
| **종류** | ⚠⚠ **연화의 *범주*가 다르다.**  그들 κ = **실제 입자가 실제로 무르다**(내부 기공·미세결함으로 겉보기 탄성률이 낮다) = **물성 측정**.  우리 18× = **강체구 DEM 이 못 하는 재배열·GB 슬라이딩·미세파쇄를 유효 E 에 럼핑** = **모델 결손 보상**(frame[2]).  ⇒ **같은 숫자축 위에 있어도 같은 양이 아니다.** |

**★ 그런데 여기서 진짜 쓸모가 나온다 — 18× 의 *분해*:**
```
E_eff = E_bulk × κ_material × κ_model
        22–24     [실측 대상]   [모델 결손 럼핑, 이름이 붙은 잔차]
```
Van Lew 가 확립한 것은 **κ_material 이 0 이 아니고 세라믹계에서 0.4–0.55 수준**이라는 것이다.
만약 LPSCl 에서 κ_material 을 실측하면, 우리 18× 는 **"측정된 한 조각 × 이름 붙은 나머지"** 로 쪼개진다.
⇒ **지도교수 질문에 대한 정직하고 방어 가능한 답의 형태가 이것이다** (§10-①).

### (b) 이 논문의 방법(실측 분포 → E)이 **우리 보정보다 나은 길인가?**

**⚠ 단순 우위가 아니다. 교환이다.**

| 축 | Van Lew (Direct Measuring) | 우리 (Bulk Calibration) |
|---|---|---|
| E 의 출처 | **입자 실측** | 거시 porosity 역보정 |
| E 축 자유변수 | ~0 (단, E_bulk·ν·E_a·bin 수·[0,1] 절단 = **판단 4개**) | **1개** (그러나 물성을 18× 왜곡) |
| **거시 검증** | ⛔ **없다** — 논문이 스스로 인정 (§6.4) | ✅ porosity·Cronau overlap·Heckel·두께 |
| 적용 응력 | 6 MPa | **300 MPa (50×)** |
| 겹침 영역 | δ/d ≤ **1.7 %** | δ/d = **11–12 % (~7배 깊이)** |
| 구성 거동 | 탄성 Hertz | 접촉 소성 (hooke/hysteresis) + Stage-E |
| 입자 크기 | **0.5–1 mm** | **1–3 µm (2–3 자릿수 아래)** |

⛔ **드롭-인 대체는 불가능하다.  이유 3가지:**
1. **영역이 다르다.**  그들 절차는 **탄성 Hertz 구간에서만 정의**된다.  우리 LPSCl 은 300 MPa 에서
   **소성**이고 δ/d 가 그들 실측 상한의 7배다.  거기서 "겉보기 탄성 E" 는 정의부터 흔들린다.
2. **크기가 다르다.**  Coetzee 는 직접측정 시도가 전부 *"millimetre and above"*, 최소 사례 500 µm 라고 기록한다.
   ★ **Van Lew 의 0.5 mm pebble 은 정확히 그 하한 근처다** ⇒ **이 논문은 "우리 입경대에서는 직접측정이
   불가능하다"는 우리 방어를 *반박하지 않고 오히려 그 경계선을 실증*한다.**
3. **그들 쪽에 검증이 없다.**  실측 E 로 갈아타면 **보정은 잃고 검증은 못 얻는다** — 그들 침대는
   어떤 실험과도 대조되지 않았다.

✅ **그래도 해야 할 것은 있다 — 대체가 아니라 *분해*로.**
필요한 측정 (⚠ 우리가 이 데이터를 갖고 있는지는 이 카드가 판단할 수 없다 — **필요 목록만**):

| # | 측정 | 왜 |
|---|---|---|
| 1 | **LPSCl 단일입자 압축 F–δ 곡선, ≥30 개** (in-SEM flat-punch micro-compression 또는 나노압입) | κ_material 역산의 원자료 |
| 2 | 같은 입자의 **개별 직경** | Eq.(2)에 d_p 가 들어감. Van Lew 는 컬러바로 이걸 관리한다 |
| 3 | **압자/앤빌 E·ν 명시** | E* 를 통과하므로 없으면 κ 재현 불가 (Van Lew 의 결함 그대로 반복 금지) |
| 4 | **ν_SE** | 우리 DFT 쌍 (B₀ 26.23, ν 0.360) 보유 ✅ |
| 5 | **E_bulk 기준** | 우리 DFT E_VRH **22.06** (comp1) 보유 ✅ — Van Lew 가 못 한 "출처 명시" 를 우리는 할 수 있다 |
| 6 | **같은 압력영역 확인** | 우리 δ/d 11–12 % 를 재려면 시험이 **소성까지** 가야 함 ⇒ 탄성 Hertz 피팅 대신 **소성 접촉모델 피팅** 필요 (Zunker MDR 계열이 그 자리) |
| 7 | **AM(NMC811) 도 동일** | 우리 E_CAM 140 GPa 도 같은 검사를 안 받았다 |

⇒ **판정: (b) = "더 나은 길"이 아니라 "우리가 아직 안 한 *다른 종류의* 측정".
   그것은 18× 를 대체하지 못하고, 18× 를 *설명 가능한 두 조각으로 쪼갠다*.**

### (c) Coetzee 재인용 ↔ 원문 대조 (재인용 오류 점검)

`coetzee2017_dem_calibration_review.md` §Q2(c)/§8/§12-10 및 `comparison_vs_ours_DEM.md` §A-⑥ 의 서술을 1차 대조:

| # | 재인용이 전한 것 | 원문 확인 | 판정 |
|---|---|---|---|
| 1 | *"the sample with a **distribution** in Young's modulus showed a **softer response** compared to the sample with a **constant** Young's modulus"* | 이 문장은 **Van Lew 본문에 없다**.  가장 가까운 것 = Fig 4 캡션 *"The constant Young's modulus beds all had much firmer responses"* + §4 *"beds with **smaller** Young's modulus … are more compliant"* | ⚠ **Coetzee 의 패러프레이즈**.  ⇒ **인용 시 반드시 "as summarised by Coetzee (2017)" — Van Lew 직접인용으로 쓰면 안 된다.** |
| 2 | **"Weibull 분포"** | ✅ **맞다.**  단 **Fig 2b 부캡션 딱 한 곳** — *"This distribution is modeled as a Weibull distribution function in DEM simulations."*  본문 어디에도 "Weibull" 이 **없고**, **모수도 없다** | ✅ 사실이나 **극히 얇은 근거**.  게다가 **Fig 4 캡션은 같은 것을 "Gaussian"**, **본문은 "discrete, random … experimental distribution"** 이라 부른다 = **한 논문이 세 이름** ⇒ **"Weibull 을 썼다"고 단정 인용 금지** |
| 3 | **"세라믹 펠릿 42개"** | ⚠ **두 군데 틀렸다.**  ① 측정 대상은 **pebble(구)** 이고, **pellet 은 문헌 기준값(E_bulk)의 형태**다 — 뒤바뀌었다.  ② **42 = Li₂TiO₃ 배치**(Fig 2b 에 그려진 것)이고, **DEM 이 쓴 것은 Li₄SiO₄ 31 개**다 | ⚠ **정정 필요.**  올바른 표기: *"Li₄SiO₄ 31 개 + Li₂TiO₃ 42 개 = 73 개 pebble; 그림에 나온 κ 분포는 Li₂TiO₃ 42 개, DEM 에 들어간 것은 Li₄SiO₄ (분포 그림 미게재)"* |
| 4 | **"파단 입자 비율도 낮아졌다"** | ⚠ Van Lew 는 그렇게 **주장**하지만 **자기 Table 1 이 3쌍 중 1쌍에서 반증**한다 (A.1 0.3 < B.1 0.6) | ⚠ **원문 자체의 과장.**  Coetzee 는 그 과장을 그대로 옮겼다 (리뷰가 표를 확인하지 않은 것) |
| 5 | **"배수는 n/a — 두 논문 모두 미보고"** | ⚠ **부분적으로 틀렸다.**  Van Lew 는 **90 GPa 와 49 GPa 를 둘 다 stated 로 준다** ⇒ **배수 1.84× 가 산술로 나온다.**  또 거시 변형비 **1.37×** 도 stated | ⚠ **상향 정정 가능**: *"배수 n/a"* → *"평균 배수 **1.84×**, 거시 변형비 **1.37×** (둘 다 stated 수치에서 유도).  ⛔ 그러나 그것이 **18× 를 지지하지 않는다** — 오히려 **10배 부족**을 정량화한다"* |
| 6 | **암묵 프레이밍**: "불균질 → 더 무름" | ⛔ **원문이 지지하지 않는다.**  Set B 는 **평균도 1.84× 낮다**.  **상수 Ē 통제군이 없다** ⇒ **분포 효과와 평균 효과가 분리 불가** | ⛔ **가장 중요한 정정.**  ⇒ 우리가 쓸 수 있는 명제는 **"불균질 → 무름"이 아니라 "실측 입자 E < 문헌 벌크 E"** 다 |

**요약**: 재인용은 **거짓은 아니지만 세 군데(대상·프레이밍·배수)에서 드리프트**했고,
정정하면 **우리에게 오히려 유리해진다** — 근거가 "방향뿐"에서 **"방향 + 측정된 배수 1.84× + 그 배수가
우리 18× 에 10배 못 미친다는 정량"** 으로 바뀌기 때문이다.  후자가 훨씬 방어하기 쉽다.

---

## 10. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

| 항목 | Van Lew 2015 | 우리 | 같음/다름 · 왜 |
|---|---|---|---|
| **소재** | Li₄SiO₄ / Li₂TiO₃ 세라믹 breeder | LPSCl + NMC811 | **완전히 다름.** 절대값 전이 **전면 금지** |
| **E_bulk** | 90 / 124 GPa (출처 미인용) | **22–24 GPa** (DFT E_VRH 22.06 · Bazzoun 22.1) — 출처 명시 | 우리가 **출처 품질에서 앞선다** |
| **E → DEM** | **입자별 실측 분포**, 10종 이산 | **전 입자 단일 E_eff = 1.35 GPa** | **다름 (직교).** 그들 = 물성 축 불균질, 우리 = **PSD 기하 축 불균질(12:4:1)** |
| **연화 배수** | **1.84×** (평균) · ~7× (최극단 개체) | **18×** (24 → 1.35) | ⚠ **10배 차.  방향만 정합.** |
| **연화의 성격** | **측정된 물성**(입자 겉보기 E) | **모델 결손 럼핑**(재배열/GB/미세파쇄) — frame[2] | **범주가 다름.** 한 표에 나란히 놓지 말 것 |
| **접촉법칙** | 순수 탄성 Hertz | hooke/hysteresis (**접촉 소성**) + Stage-E(Tabor+volume 소성면적) | **우리가 앞섬** |
| **입자 형상 소성** | ❌ 없음 (강체구) | ❌ DEM 없음 / ✅ **MPM 있음** | frame[5] — 그들은 MPM 절반이 통째로 없다 |
| **응력** | **6 MPa** | **300 MPa (50×)** | ⚠ Coetzee 규범(*"보정 응력 = 응용 응력"*) 기준으로 **두 논문은 서로의 영역 밖** |
| **겹침 δ/d** | ≤ **1.7 %** (실측 구간) | **11–12 %** | **~7배.**  그들 Hertz 검증구간 **밖**에서 우리가 돈다 |
| **다접촉 결합** | ❌ **명시적으로 기각** (Russell 이진접촉) | 우리도 이진 (⚠ Giannis/Varkey 가 밀집영역 결손 지적) | **같음** — 단 우리는 ρ 가 높아 **더 불리** |
| **porosity / Heckel** | ❌ **0** | ✅ ε_sphere · Heckel R²=0.965, P_y=138 | **이 논문은 우리 압밀 축에 아무것도 안 준다** |
| **전달 σ (ion/e/thermal)** | ❌ 0 | ✅ 삼중항 (Kirchhoff/Holm + STEP3 복셀 FV) | 우리 고유 |
| **배위수·percolation·coverage·τ** | ❌ 0 | ✅ 전부 | 우리 고유 |
| **파쇄** | **후처리 판정만** (Eq.7 임계력, 입자는 안 쪼개짐) | **Auerbach 취성 + fracture-aware Holm(f_intact)** — 접촉 소실이 σ 에 반영 | ★ **구조는 형제, 우리가 한 단계 더 나감**(전달까지 연결) |
| **파쇄 강도의 출처** | ★ **실측 W_ε,l 분포에서 입자마다 무작위** | 우리 = 파괴역학 법칙 | ⇒ **그들에게 배울 것이 있는 유일한 칸** (§11-③) |
| **거시 검증** | ⛔ **없음** | ✅ porosity·Cronau·두께·Bazzoun EIS | **우리가 앞섬** |
| **시드/오차막대** | ⛔ 침대당 1 실현 | 우리 다중시드 관행 | **우리가 앞섬** |
| **입자 크기** | 0.5–1 mm | **1–3 µm** | 2–3 자릿수 — **직접측정 가능성의 경계가 그들 쪽에 있다** |

---

## 11. 적용 인사이트 (실행 항목)

- **① ★★★ 18× 를 *하나의 숫자*에서 *두 조각*으로 재서술한다 (원고·발표 즉시 적용, 새 계산 불필요).**
  현행: *"E 24 → 1.35 GPa, 18× 연화"* (해명 없는 단일 배수)
  개정: *"E_eff = E_bulk × κ_material × κ_model"*, 그리고 —
  · **κ_material 은 실재한다** — 세라믹 breeder pebble 73개 직접 측정에서 **0.4–0.55** (Van Lew 2015).
    ⇒ *"입자의 겉보기 E 가 문헌 벌크값보다 낮은 것은 우리 계의 변명이 아니라 다른 계에서 측정된 현상이다."*
  · **κ_model 은 우리 것이고 이름이 붙어 있다** — 재배열·GB 슬라이딩·미세파쇄 (frame[2]).
  ⛔ **경계선**: κ_material 의 *배수*(1.84×)를 LPSCl 에 옮겨 적지 말 것.  **존재와 방향만** 인용.

- **② ★★ 우리 E-보정이 *힘의 꼬리*를 고정하지 못한다는 것을 명시적으로 인정·검사한다.**
  Van Lew 실측: **거시 응력–변형은 E 가 지배**하는데 **접촉력 꼬리는 μ 가 지배**한다(§6.2).
  ⇒ 우리는 E_eff 를 **porosity(거시 평균)** 에 맞췄으므로, **fracture(꼬리 사건)는 그 보정으로 고정되지 않았다.**
  실행: **OAT 민감도 1장** — `f_broken@300 = f(μ_pp, μ_pw, COR)` at E_eff 고정.
  (⚠ `coetzee2017` 카드 §11-① 이 요구한 OAT 표와 **같은 런으로 동시에** 뽑을 수 있다 — 비용 공유.)

- **③ ★★ 파쇄 문턱의 E-의존을 감사한다 (미확인 결함 후보).**
  Van Lew Eq.(7): **F_c ∝ E*^{2/5}** ⇒ E 를 낮추면 **압쇄 문턱도 같이 내려간다**(1.84× → −21 %).
  그들은 이걸 논의하지 않았고, 그 결과 **자기 Table 1 에서 한 쌍이 뒤집혔다**(§6.3).
  **우리 질문**: 우리 **Auerbach 취성 판정의 임계력이 E_SE 에 의존하는가?**
  의존한다면 **18× 연화가 파단 예측에 감사되지 않은 부작용**을 남기고 있다
  (Auerbach/cone-crack 임계하중은 일반적으로 E 를 통해 들어간다).
  · 판정 방법: E_SE 만 {1.35, 2.0, 24} 로 바꾼 pure-SE 침대에서 **접촉력 분포**와 **f_broken** 을 **따로** 찍어
    "힘이 줄어서" 인지 "문턱이 내려가서" 인지 **분리**.  ⚠ 이건 **런 전에 등록**할 만한 사전등록 대상.

- **④ ★ 강도(strength)에 분포를 주는 것은 우리가 안 하고 있고, 할 수 있다.**
  Van Lew 는 **E 뿐 아니라 압쇄강도(W_ε,l)도 입자별 무작위**로 준다.  우리 AM 파쇄는 (확인 필요)
  결정론적 문턱으로 보인다.  세라믹 파단은 **Weibull 통계가 정본**이므로 이건 물리적으로 옳은 방향이다.
  ⚠ **선행조건**: NMC811 / LPSCl **단일입자 압쇄강도 분포 실측**.  없으면 §F1 훅만.

- **⑤ ★ "직접측정 불가" 방어의 *경계선*을 이 논문으로 정밀화한다.**
  Coetzee: 직접측정 = *"millimetre and above"*, 최소 500 µm.
  Van Lew: **0.5 mm 에서 실제로 성공** ⇒ **경계는 대략 거기다.**
  우리 1–3 µm 는 **2–3 자릿수 아래** ⇒ *"the Direct Measuring Approach is not available at our particle scale"*
  이 **리뷰 + 1차 사례 두 겹**으로 방어된다.  (⚠ 나노압입은 다른 시험이다 — "불가"는 *압쇄식 직접측정* 한정.)

- **⑥ ★ 우리 단일 E 가 이미 *분포의 붕괴*라는 인식.**
  Fig 2b: **같은 배치 안에서 E 가 ~7× 흩어진다**(digitized).  우리 LPSCl 에도 그런 산포가 있다면
  **E_SE 단일값은 이미 mean-field 붕괴**다.  ⇒ **E 를 "물성"이 아니라 "모델 파라미터"로 표기**하라는
  Coetzee §1 규범이 **실측으로 뒷받침**된다.  (우리 3층 보고 규약: real / DEM-eff / MPM — **유지**)

---

## 12. ⚠ 이 논문의 결함 목록 (인용 전 반드시 읽을 것)

| # | 결함 | 심각도 |
|---|---|---|
| ① | **Abstract·§4 의 "in all cases / in each case 파단 감소" 가 자기 Table 1 에 반증됨** (A.1 0.3 < B.1 0.6) | ★★★ 헤드라인 무효화 |
| ② | **상수 Ē = 49 GPa 통제군 부재** ⇒ *분포 효과*와 *평균 효과* 분리 불가 | ★★★ 재인용 드리프트의 근원 |
| ③ | **분포 이름이 세 개** — 본문 "discrete/experimental" · Fig 2b "Weibull" · Fig 4 "Gaussian".  모수 0개 | ★★ 재현 불가 |
| ④ | **DEM 이 쓴 분포(Li₄SiO₄)를 안 보여준다** (*"omitted for brevity"*).  보이는 Fig 2b 는 **다른 배치** | ★★ 재현 불가 |
| ⑤ | **ν_p·ν_a·E_a 전부 미보고** ⇒ κ 역산 재현 불가 | ★★ (자기가 인용한 ref[11]이 "앤빌 재료가 중요하다"는 논문인데도) |
| ⑥ | **침대 기하가 산술적으로 불가능** — 8000 입자 / (40×30×20 R_p³) ⇒ φ = **1.40** | ★★ |
| ⑦ | **DEM 코드·타임스텝·COR·감쇠 전부 미보고** | ★★ |
| ⑧ | **침대 스케일 실험 검증 0** (논문이 자인) | ★★★ |
| ⑨ | **시드 1개, 오차막대 0** — Set A 내부 산포(0.3→1.0 = 3.3×)가 A↔B 효과만큼 큼 | ★★ |
| ⑩ | **Fig 4 축 제목 없음** (단위를 본문에서 역추정해야 함) | ★ |
| ⑪ | **"stress-controlled"(§3.4) vs "constant-velocity"(§4) 상충** | ★ |
| ⑫ | **습도 비제어**인데 κ 산포를 **전적으로 "미세구조"에 귀속**.  리튬 세라믹은 흡습성 — **수분 연화 교란 미배제** | ★★ |
| ⑬ | **κ ∈ [0,1] 절단이 물리가 아니라 가정** — Fig 2b 최우측 bin 이 1.0 에 붙는 것이 경계 효과일 수 있음 | ★ |
| ⑭ | **B.4 에 짝(A.4)이 없다** ⇒ 완전 factorial 아님 | ★ |
| ⑮ | **F_c ∝ E*^{2/5} 역효과 미논의** — ①의 물리적 원인일 가능성이 높은데 논문이 인지 못 함 | ★★ (우리에겐 오히려 정보) |

---

## 13. 인용 가능 문장 (deck / 원고용) — **각각 무엇이 근거인지 붙여서**

**✅ 안전 (1차 출처 직접인용):**
1. > *"up to now, values of Young's modulii used in numerical models are taken from values measured for
   > **large sintered pellets** of ceramic materials."* (§5)
   → **"DEM 에 벌크 문헌 E 를 그대로 넣는 관행" 자체가 문제제기 대상이라는 1차 근거.**
2. > *"If **single values** of E_p and ν_p are employed, then variation in pebble diameters **can not alone
   > explain** the variation of curves."* (§2)
   → **소거 논증**: 관측된 강성 산포는 크기로 설명되지 않는다 ⇒ E 가 입자마다 다르다.
3. > *"Imperfections in the pebbles will lead **only to a reduction, or softening** of the pebble."* (§3.2)
   → **"입자는 벌크보다 무르다"의 방향 명제.**
4. > *"the **largest contributor** to stress–strain response is the Young's modulus.  The coefficient of
   > friction and radius distribution had comparatively **insignificant** influence."* (§4)
   → 구속 단축압축이 **강성을 고립시키는 시험**이라는 우리 보정 설계의 정당화 (Coetzee §5.5 와 이중화).
5. > *"past DEM work on pebble crushing was **likely over-predicting** the extent of crushing if the Young's
   > modulus used in the study was **much larger than the realistic response** of individual pebbles."* (§4)
   → **파단 예측이 입력 E 에 강하게 의존한다**는 방향 (⚠ 아래 ⛔-2 참조).

**✅ 안전 (우리 산술, "derived from stated values" 로 표기):**
6. *"Van Lew 등은 세라믹 breeder pebble 배치의 평균 겉보기 Young률이 소결 벌크 문헌값의 **0.54 배**
   (90 → 49 GPa, **1.84× 연화**)임을 단일입자 압쇄 실험으로 보고했다."*
7. *"같은 실험에서 6 MPa 단축압축 변형이 1.9 % → 2.6 % (**1.37×**)로 커졌다."*

**⚠ 조건부:**
8. *"배치 내 겉보기 E 산포는 약 7 배에 이른다"* — **digitized (Fig 2b), TREND only, Li₂TiO₃ 한정.**
9. *"Weibull 분포로 모델링했다"* — **Fig 2b 부캡션 1회, 모수 미보고, 본문·Fig 4 캡션과 상충** 을 병기할 것.

**⛔ 금지:**
- ⛔ *"Van Lew 가 우리 18× 를 지지한다"* — **10배 못 미친다.  방향만.**
- ⛔ *"분포를 주면 더 무르다"를 Van Lew 직접인용으로 쓰기* — **그 문장은 Coetzee 의 패러프레이즈**이고,
  **상수-Ē 통제군이 없어 원문이 분리하지 못한다.**
- ⛔ *"수정 E 가 파단을 줄인다"* — **자기 Table 1 이 3쌍 중 1쌍에서 반증.**  쓸 수 있는 것은
  *"파단 예측이 입력 E 에 강하게 의존한다"* 까지.
- ⛔ **90 / 124 / 49 GPa · κ 값 · 1.84× 를 LPSCl 표에 옮겨 적기.**
- ⛔ *"실측 기반이라 자유변수가 0"* — **E_bulk·ν·E_a·bin 수·[0,1] 절단 = 판단 4개.**

---

## 14. 기법 미니 용어집

| 용어 | 뜻 (이 논문 맥락) |
|---|---|
| **breeder pebble** | 핵융합 블랭킷에서 중성자로 삼중수소를 증식하는 리튬 세라믹 구슬(Li₄SiO₄·Li₂TiO₃). 지름 0.5–1 mm 급 |
| **softening coefficient / elasticity reduction factor κ** | κ = E_peb/E_bulk. **입자 겉보기 탄성률 ÷ 소결 펠릿 문헌값**. 정의상 [0,1] 로 **자름** |
| **apparent Young's modulus** | 입자를 Hertz 구로 **가정했을 때** 곡선을 맞추는 E. 진짜 재료 탄성률이 아니라 **내부 기공·미세결함까지 포함한 유효값** |
| **single pebble crush test** | 구 하나를 두 평면 앤빌 사이에서 파괴까지 압축, F–s 기록. **s = 접촉당 겹침의 2배** |
| **oedometric / confined uniaxial compression** | 측면 구속 상태 단축압축. **강성을 고립시키는 시험**(마찰 영향 작음) |
| **strain energy equivalence (Eq. 5)** | 랩에서 잰 압쇄 변형에너지 = 침대 안 그 접촉의 변형에너지, 라는 **전이 가정** |
| **binary contact assumption (Russell)** | 접촉의 내부응력이 **이웃 접촉의 수·크기와 무관**하다는 가정. Van Lew 가 **채택**, Zhao(전체 합산)를 **기각** |
| **Direct Measuring vs Bulk Calibration** | Coetzee(2017)의 두 학파. Van Lew = **전자**(입자를 직접 잼), 우리 = **후자**(거시응답에 역보정) |
| **Furnas dip / Heckel / percolation / coverage** | ⚠ **이 논문에 전부 없다** — 압밀·전달 축 용어는 여기서 조달할 수 없음 |

---

## 15. 🗨️ Q&A 로그

**Q. Coetzee 가 전한 "distribution → softer" 를 우리 원고에 그대로 써도 되나?**
A. ⛔ 안 된다. 세 겹으로 문제다 — ① 그 문장은 **Van Lew 원문에 없다**(Coetzee 패러프레이즈).
② Van Lew 의 Set B 는 **평균도 1.84× 낮아** 분포 효과가 분리되지 않는다. ③ 우리 판독에서
관측 변형비가 **순수 평균-E Hertz 예측과 모순이 없다**. ⇒ 쓸 수 있는 명제는
**"실측된 개별 입자 E 가 소결 벌크 문헌값보다 낮다 (κ̄ ≈ 0.54)"** 이고, 이게 더 강한 문장이다.

**Q. 그러면 18× 는 여전히 근거가 없나?**
A. **배수의 근거는 여전히 없다.** 그러나 이 논문 덕분에 18× 를 **κ_material(측정 대상, 세라믹계 0.4–0.55)
× κ_model(재배열 럼핑, 이름 있음)** 로 **분해해 서술**할 수 있게 됐다. "설명 없는 18×" → "측정 가능한 한
조각 + 명명된 나머지" 는 방어 등급이 다르다. 그리고 **우리가 아직 안 한 측정이 무엇인지**가 §9-b 표로 확정됐다.

**Q. 그들 방식으로 갈아타면 되나?**
A. 안 된다. **탄성 Hertz 구간(δ/d ≤ 1.7 %)에서만 정의된 절차**이고 우리는 **δ/d 11–12 %, 300 MPa 소성**에서
돈다. 게다가 **그들 침대는 어떤 실험과도 대조되지 않았다**(논문 자인) — 보정을 잃고 검증을 못 얻는 교환이다.
쓸 자리는 **대체가 아니라 분해**다.

**Q. 우리 fracture 축에 진짜로 쓸 것이 있나?**
A. ★ 있다, 두 개. ① **F_c ∝ E*^{2/5}** — 연화가 파단 **문턱까지** 내린다는 것. 우리 Auerbach 판정이
E_SE 에 의존하면 **18× 가 파단 예측에 감사되지 않은 부작용**을 남긴다(§11-③, 사전등록 대상).
② **강도를 입자별 분포로 무작위 배정** — 세라믹 파단의 정본 통계(Weibull)와 맞고, 우리는 안 하고 있다.
⚠ 선행조건 = LPSCl/NMC811 단일입자 압쇄강도 분포 실측.

**Q. 압밀·porosity 축에는?**
A. **아무것도 없다.** porosity·상대밀도·Heckel 이 **한 번도 안 나오고**, 압력이 **6 MPa 단일점**이며,
침대 기하가 산술적으로 모순이라 **packing fraction 조차 재구성 불가**하다(§3.3-⑥).
⇒ *"E-강성이 porosity floor 를 정한다"* 축에는 **Varkey(halide E 10.58 → floor 21/37 %)** 를 계속 쓴다.

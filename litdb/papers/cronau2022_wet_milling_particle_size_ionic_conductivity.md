# 습식 저에너지 볼밀링(LWM) 시간 ↔ SE 입자크기·이온전도도의 상충과 "2 h 최적" — gc-Li₅.₅PS₄.₅Cl₁.₅ / NCM-85 복합양극 — Cronau (Batteries & Supercaps 2022)

> slug `cronau2022_wet_milling_particle_size_ionic_conductivity` · DOI `10.1002/batt.202200041` · type `experiment` · PDF `ce19f839-Batteries___Supercaps_-_2022_-_Cronau_-_Ionic_Conductivity_versus_Particle_Size_of_Ball_Milled_Sulfide_Based_Solid.pdf` · digested `2026-09-25` · status ✅
>
> SI = `53052ebd-batt202200041-sup-0001-misc_information.pdf` (3 pp, Fig. S1–S4, 표 없음).  본문 6 pp + SI 3 pp **전부 실독**, 그림 9장(본문 5 + SI 4) 전부 크롭·육안 확인 (`litdb/figures/cronau2022_wet_milling_particle_size_ionic_conductivity/`).
> 작성 계기 = 작업 브랜치 원장 **`SELF-51`** — 우리 코드가 `σ_grain = 3.0 mS/cm` 와 입자크기 계수 `Cronau(r_SE)` 를 "Cronau 2022" 출처로 적어 왔는데 **원문 대조가 한 번도 없었다**. 이 카드가 그 원문 대조다.
> 자매 카드: [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) (같은 그룹, ACS Energy Lett. 2021 — stack pressure 프로토콜). **두 논문은 별개다** (DOI 가 다르다: 2021 = `10.1021/acsenergylett.1c01299`, 2022 = 이 논문).

---

## 0. ★ SELF-51 판정 요약 (먼저 읽을 것)

| 우리가 쓰던 것 | 이 논문에 있는가 | 판정 |
|---|---|---|
| `σ_grain = 3.0 mS/cm` — "Cronau 2022 **Li₆PS₅Cl single-crystal**" | ⛔ **없다.** 이 논문이 **잰 재료는 Li₅.₅PS₄.₅Cl₁.₅**(LPSC+)뿐이고 Li₆PS₅Cl 은 **한 번도 측정하지 않았다.** 단결정 측정 없음 ("single crystal" 이라는 낱말 자체가 본문·SI 에 없다). "3 mS/cm" 은 **서론 p.1 의 인용 없는 일반 서술** *"Li6PS5Cl (LPSC) … exhibiting an ionic conductivity of about 3 mS/cm"* 한 문장뿐이다 — 바로 앞 인용 `[4–10]` 은 **앞 문장**(argyrodite 일반 장점)에 붙어 있다 (§2-1, 렌더로 확인). | **오귀속.** 이 논문은 1차 출처가 될 수 없다. 최대한 = "LPSC 가 약 3 mS/cm 급이라는 **2차·무인용 서술**". `se_material.py` 의 09-25 정정 라벨(*"project-adopted, no direct literature source"*)이 **맞다**. |
| `Cronau(r_SE)` 계수 — r ≥ 0.5 µm → 1.00 · 0.3–0.5 → 0.90 · 0.1–0.3 → 0.65 · ≤ 30 nm → 0.33 ("Cronau 2022 amorphization", "Cronau extreme-milling limit", "1/3 reduction … D50 < 0.3 µm") | ⛔ **구간값이 하나도 없다.** 이 논문은 σ 를 **입자 반경 r 의 함수로 보고하지 않는다** — 독립변수는 **밀링 시간 · 볼 크기 · 결정도(gc/µc)** 다. 가장 작은 평균입경이 **d ≈ 1.0 µm (r ≈ 0.5 µm, stated)** / λ 역산 **d ≈ 0.9 µm (50 h, derived)** 이라 **r = 0.3 · 0.1 · 0.03 µm 에 해당하는 데이터가 존재하지 않는다.** "D50 < 0.3 µm" 도 없다. | **방향만 (교란된 채로) 지지, 수치는 전부 프로젝트 채택값.** 게다가 이 논문 자신의 데이터가 "σ = f(r)" 해석을 **반박**한다 (다음 행). |
| (0.33 하한의 뿌리 추정) | p.2 의 *"extended LWM exceeding 40 h leads to … about 1/3 of the original value"* 는 **문헌 인용 [20,25]** (Shi 2020 · Minnmann 2021) 이고 **밀링 시간 서술**이다 — 입자크기가 없다. 이 논문 **자체** 50 h 값은 0.36/2.5 = **0.14 (≈1/7, stated 값으로 계산)** 로 1/3 도 아니다. | 0.33 = "1/3" 문장을 **입자크기 축에 잘못 옮긴 것**으로 보인다 (**가설** — 코드 이력만으로는 증명 불가). |
| **"입자크기 자체" 효과인가?** | 아니다. ① **같은 4 h** 에서 볼 크기만 바꿔 입경이 1.0 / 1.6 / (Ø≈20 µm 덩어리 잔존) µm 로 크게 달라져도 σ ≈ **1.38 / 1.41 / 1.51 mS/cm** (Fig. 2 digitized) — 입경 차에 비해 σ 차는 ≈ 9 % (1.51/1.38). ② **4 h → 50 h** 에 입경은 1.0 → ≈0.9 µm (λ 역산) 로 거의 그대로인데 σ 는 1.52 → 0.39 (**×1/3.9**, Fig. 5b digitized). | σ 하락은 **밀링 손상(부분 비정질화 — 저자 XRD 해석; 문헌: 입자경계 저항 + 잔류 용매)** 의 함수다. **입자크기와 교란**되어 있고, 교란을 풀면 크기 몫은 작다. |

> ⛔ **인용 금지 (이 카드의 판정)**: *"Cronau 2022 — Li₆PS₅Cl single-crystal 3.0 mS/cm"* · *"Cronau 2022 — σ falls to 1/3 for particles ≤ 30 nm / D50 < 0.3 µm"* · *"Cronau 2022 measured σ as a function of particle radius"* — 셋 다 원문에 없다.

⇒ **처방 (값은 안 건드린다 — 라벨만):** `σ_grain = 3.0` 은 "프로젝트 채택값 (문헌 1차 출처 없음)" 유지. `Cronau(r_SE)` 는 **이름에서 "Cronau" 를 떼거나 "Cronau 2022 는 방향만(밀링↑→σ↓, 손상 기원)" 으로 각주**하고 구간값은 "프로젝트 채택(가정)" 으로 표기. 코드 위치는 §7-4.

---

## 1. 한 줄 요약

고에너지 건식밀링(HDM)으로 만든 **유리-세라믹 Li₅.₅PS₄.₅Cl₁.₅ (gc-LPSC+, σ 2.5 mS/cm)** 를 헵탄/다이부틸에터 속에서 **저에너지 습식밀링(LWM, 200 rpm)** 하면 **입자는 1 µm 까지 작아지지만 이온전도도도 같이 떨어진다** (2 h 1.73 · 50 h 0.36 mS/cm). 입자가 작아지면 CAM(NCM-85, d 3.5 µm)과의 접촉(λ = d_CAM/d_SE)이 좋아져 용량이 오르고, σ 하락이 그 이득을 넘어서면 다시 떨어진다 → **1 mm 볼·LWM ≈ 2 h 가 최적** (0.6 C 첫 방전 179 mAh/g). 저자는 σ 하락을 XRD 근거로 **부분 비정질화**에 돌린다. **제목("Ionic Conductivity versus Particle Size")과 달리 σ 를 입자크기의 함수로 분리해 재지 않았다** — 둘 다 밀링 시간의 함수로 함께 움직인다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE / CAM) | 연구유형 |
|---|---|---|---|---|
| **Marvin Cronau⁺**, **Marc Duchardt⁺** (공동 1저자), Marvin Szabo, **Bernhard Roling\*** (Philipps-Universität Marburg, Dept. of Chemistry) | *Batteries & Supercaps* **5** (2022) **e202200041** (6 pp), received 2022-01-21, revised 2022-02-24, OA CC BY-NC-ND | `10.1002/batt.202200041` | SE = **Li₅.₅PS₄.₅Cl₁.₅** (gc = HDM 그대로, µc = 550 °C 12 h 어닐; 실험절에서는 µc 를 "**c-LPSC+**" 로 표기) · CAM = **LiNi₀.₈₅Co₀.₁₀Mn₀.₀₅(O₂)** "**NCM-85∣10∣05**" (BASF, **LiNbO₃ 코팅**, 이론 200 mAh/g, d 3.5 µm) · 도전재 CNF (Nanografi) · 음극 **In** | 실험 (합성 · 밀링 · SEM · XRD · EIS · 갈바노스태틱) — **시뮬레이션 0** |

- 데이터 공개: *"Research data are not shared."* (p.6) → 원자료 없음, 그림 디지타이즈가 유일한 수치 경로.
- 자금: MARA 장학금 (Duchardt), BASF (CAM 제공), Projekt DEAL (OA).

### 2-1. ★ 서론의 "3 mS/cm" 두 문장 — 원문 그대로 (p.1, 인용 위치는 렌더로 확인)

> **(p.1, 서론 2문단)** "During the last years, a clear focus of the research community on crystalline argyrodites Li6PS5X (X=Cl, Br) as sulfide-based SEs could be observed, since these argyrodites are very well conductive, kinetically quite stable towards both Li metal and cathode active materials, and they do not contain any expensive or hazardous elements.**[4–10]** Most prominently, Li6PS5Cl (LPSC) has been utilized, exhibiting an ionic conductivity of about 3 mS/cm. This conductivity is similar to that of Li6PS5Br, but chloride is the more readily available halogenide."

- ⚠ **인용 위치**: 위첨자 `[4–10]` 은 *"… hazardous elements."* 뒤에 붙어 있다. **"about 3 mS/cm" 문장 자체에는 인용이 없다.** 즉 `[4–10]` 은 "argyrodite 가 잘 전도하고 안정하고 싸다" 는 앞 문장의 근거이고, 3 mS/cm 의 출처로 **이 논문이 지목한 것은 없다.**
- 같은 문단 이어서: *"Importantly, a further increase in conductivity could recently be achieved by raising the Cl content in Li6−xPS5−xCl1+x, with an optimum conductivity of 8–10 mS/cm observed for the composition Li5.5PS4.5Cl1.5 (LPSC+), which thus rivals the well-known Li10GeP2S12.**[11–14]**"*

> **(p.1, 서론 3문단)** "Interestingly, a recent study has shown that the glass ceramic LPSC+ might boast competitive ionic conductivities even without any annealing step, but solely through mechanical milling synthesis.**[11]** Its conductivity after 6 h of ball milling amounts to about 3 mS/cm, being on a par with the one of crystalline LPSC."

- 여기서 "about 3 mS/cm" 은 **[11] (Jung 2020 Nano Lett.) 의 gc-LPSC+ (6 h 볼밀) 값의 요약**이고, *"on a par with the one of crystalline LPSC"* 가 앞 문단의 "LPSC ≈ 3" 을 다시 가리킨다. 역시 Li₆PS₅Cl 의 1차 측정 인용이 아니다.

### 2-2. ★ "1/3" 문장 — 원문 그대로 (p.2) · 인용은 `[20,25]` 다

> **(p.2, 좌단)** "Common particle size distributions with a considerable amount of particles having diameters >20 μm are therefore not viable for the separator layer either.**[4,18]**
> Unfortunately, extended LWM exceeding 40 h leads to a significant reduction of ionic conductivity of the SE to about 1/3 of the original value, which has been attributed to increased particle boundary resistances and inclusion of residual solvent.**[20,25]**"

- ⚠ **`[4,18]` 은 "1/3" 문장의 인용이 아니다** — 앞 문장("> 20 µm 입자는 분리막에도 부적합")의 인용이다. "1/3" 문장의 인용은 **`[20,25]`** = Shi *et al.* 2020 (Ceder) · Minnmann *et al.* 2021 (Janek). (렌더로 위첨자 위치 확인.)
- 이 문장은 **문헌 요약**이다 (이 논문의 측정 아님). 입자크기 값이 **없다** — "40 h 넘는 LWM" 이라는 **시간** 조건뿐이다.
- 정본 카드 대조 (우리 쪽 확인 범위):
  - `[20]` = [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (DOI `10.1002/aenm.201902881` 일치): 카드는 *"작은 LPS(75Li₂S–25P₂S₅ 유리) = wet ball-mill(헵탄+다이부틸에터) → 1.5/3/5/8 µm, 작을수록 σ_ion 감소 (입계저항↑ + 잔류용매, Table S3)"* 까지 적었다. **"40 h" · "1/3" 숫자는 카드에 없다** (Table S3 수치 미전사) → `[미확인]`. 재료도 **LPS 유리**(argyrodite 아님)이고 최소 입경 **1.5 µm**(서브-µm 아님).
  - `[25]` = [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (DOI `10.1149/1945-7111/abf8d7` 일치): 카드는 *"LPSCl coarse 1.6 → fine 1.2 mS/cm, wet-mill (헵탄/다이부틸에터 8:1, 200 rpm, 10 h)"* (= ×0.75) 를 적었다. **"40 h → 1/3" 은 카드에 없다** → `[미확인]`.
  - ⇒ **"40 h → 1/3" 의 1차 근거는 우리 정본 어디에서도 아직 확인되지 않았다.** 확인하려면 Shi 2020 SI Table S3 원문을 연다.

### 2-3. 참고문헌 — 이 논문의 목록 **그대로** (p.6, 렌더로 글자 대조; 원 목록에 제목은 없다)

규율 ⑥(원문 안 본 서지는 채우지 않는다)에 따라 **제목을 붙이지 않는다.** "정본 카드" 열은 우리 litdb 에 **원문 확인된 카드가 있는 것만** 적었다. 없으면 그 문헌의 **내용**은 `[미확인]`.

| # | 서지 (원 목록 그대로) | 이 논문에서 인용된 자리 | 정본 카드 (내용 확인) |
|---|---|---|---|
| [4] | Y. G. Lee, S. Fujiki, C. Jung, N. Suzuki, N. Yashiro, R. Omoda, D. S. Ko, T. Shiratsuchi, T. Sugimoto, S. Ryu, J. H. Ku, T. Watanabe, Y. Park, Y. Aihara, D. Im, I. T. Han, *Nat. Energy* **2020**, *5*, 299–308. | p.1 `[4–10]` (argyrodite 일반 장점) · p.2 `[4,18]` (> 20 µm 분리막 부적합) · p.3 `[4,20]` (평균 < 1 µm 필요) | 없음 → `[미확인]` |
| [5] | A. Banerjee, X. Wang, C. Fang, E. A. Wu, Y. S. Meng, *Chem. Rev.* **2020**, *120*, 6878–6933. | p.1 `[4–10]` | 없음 → `[미확인]` |
| [6] | J. M. Doux, H. Nguyen, D. H. S. Tan, A. Banerjee, X. Wang, E. A. Wu, C. Jo, H. Yang, Y. S. Meng, *Adv. Energy Mater.* **2020**, *10*, DOI 10.1002/aenm.201903253. | p.1 `[4–10]` | [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) — LPSCl 펠릿(370 MPa cold-press, ~1 mm) **σ_ion 2–2.5 mS/cm** (EIS). **3.0 아님.** |
| [7] | J. Kasemchainan, S. Zekoll, D. Spencer Jolly, Z. Ning, G. O. Hartley, J. Marrow, P. G. Bruce, *Nat. Mater.* **2019**, *18*, 1105–1111. | p.1 `[4–10]` | 전용 카드 없음 (타 카드에서 인용만) → `[미확인]` |
| [8] | Q. Zhao, M. Avdeev, L. Chen, S. Shi, *Sci. Bull.* **2021**, *66*, 1401–1408. | p.1 `[4–10]` | 없음 → `[미확인]` |
| [9] | Q. Zhao, L. Zhang, B. He, A. Ye, M. Avdeev, L. Chen, S. Shi, *Energy Storage Mater.* **2021**, *40*, 386–393. | p.1 `[4–10]` | 없음 → `[미확인]` |
| [10] | M. Cronau, M. Szabo, B. Roling, *Mater. Adv.* **2021**, *2*, 7842–7845. | p.1 `[4–10]` | 없음 → `[미확인]` (⚠ ACS Energy Lett. 2021 = [16] 과 **다른 논문**) |
| [11] | W. Dum Jung, J.-S. Kim, S. Choi, S. Kim, M. Jeon, H.-G. Jung, K. Yoon Chung, J.-H. Lee, B.-K. Kim, J.-H. Lee, H. Kim, *Nano Lett.* **2020**, *20*, 2303–2309. | p.1 `[11–14]` (LPSC+ 8–10 mS/cm) · p.1 `[11]` (gc-LPSC+ 6 h 볼밀 ≈ 3 mS/cm) | 없음 → `[미확인]` |
| [12] | L. Zhou, K. H. Park, X. Sun, F. Lalère, T. Adermann, P. Hartmann, L. F. Nazar, *ACS Energy Lett.* **2019**, *4*, 265–270. | p.1 `[11–14]` | 없음 → `[미확인]` |
| [13] | P. Adeli, J. D. Bazak, K. H. Park, I. Kochetkov, A. Huq, G. R. Goward, L. F. Nazar, *Angew. Chem. Int. Ed.* **2019**, *58*, 8681–8686; *Angew. Chem.* **2019**, *131*, 8773–8778. | p.1 `[11–14]` | [`adeli2019_halide_substitution_boosting_argyrodite`](adeli2019_halide_substitution_boosting_argyrodite.md) — **x = 0.5 (Li₅.₅PS₄.₅Cl₁.₅) 9.4 mS/cm** (cold-press, 298 K, In 블로킹; 소결 12.0) = "8–10" 문장 지지 ✓ · **x = 0 (Li₆PS₅Cl) 2.5 mS/cm** (같은 시리즈) |
| [14] | S. V. Patel, S. Banerjee, H. Liu, P. Wang, P. H. Chien, X. Feng, J. Liu, S. P. Ong, Y. Y. Hu, *Chem. Mater.* **2021**, *33*, 1435–1443. | p.1 `[11–14]` | 없음 → `[미확인]` |
| [15] | C. Yu, S. Ganapathy, J. Hageman, L. Van Eijck, E. R. H. Van Eck, L. Zhang, T. Schwietert, S. Basak, E. M. Kelder, M. Wagemaker, *ACS Appl. Mater. Interfaces* **2018**, *10*, 33296–33306. | p.1 `[15,16]` (결정 argyrodite 는 고온 어닐 필요) | 없음 → `[미확인]` |
| [16] | M. Cronau, M. Szabo, C. König, T. B. Wassermann, B. Roling, *ACS Energy Lett.* **2021**, *6*, 3072–3077. | p.1 `[15,16]` | [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) — 3.0 mS/cm 없음 · 단결정 없음 · 측정 argyrodite = Li₆PS₅Br |
| [18] | S. Spannenberger, V. Miß, E. Klotz, J. Kettner, M. Cronau, A. Ramanayagam, F. di Capua, M. Elsayed, R. Krause-Rehberg, M. Vogel, B. Roling, *Solid State Ionics* **2019**, *341*, 115040. | p.1 `[18,19]` (볼밀 LPSC+ 입경 ≈ 다른 기계합성 황화물) · p.2 `[4,18]` | 없음 → `[미확인]` |
| [19] | M. Kroll, M. Duchardt, S. L. Karstens, S. Schlabach, F. Lange, J. Hochstrasser, B. Roling, U. Tallarek, *J. Power Sources* **2021**, *505*, 230064. | p.1 `[18,19]` | 없음 → `[미확인]` |
| [20] | T. Shi, Q. Tu, Y. Tian, Y. Xiao, L. J. Miara, O. Kononova, G. Ceder, *Adv. Energy Mater.* **2020**, *10*, 1902881. | p.1 (λ ≥ 2:1 · HDM 으로는 작은 입경 불가) · p.2 `[20,22–24]` (LWM) · **p.2 `[20,25]` (1/3)** · p.3 `[4,20]` · p.5 (λ≈2.5 충분) | [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) — 방향(습식밀링 작은 LPS → σ↓) 확인, "40 h · 1/3" 수치는 카드에 없음 |
| [21] | F. Strauss, T. Bartsch, L. de Biasi, A. Y. Kim, J. Janek, P. Hartmann, T. Brezesinski, *ACS Energy Lett.* **2018**, *3*, 992–996. | p.1 (CAM < 5 µm 전형) | 없음 → `[미확인]` |
| [22]–[24] | T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, M. Tatsumisago, *J. Electrochem. Soc.* **2017**, *164*, A3960–A3963 · A. Sakuda, K. Kuratani, M. Yamamoto, M. Takahashi, *J. Electrochem. Soc.* **2017**, *164*, A2474–A2478 · C. Park, S. Lee, K. Kim, M. Kim, S. Choi, D. Shin, *J. Electrochem. Soc.* **2019**, *166*, A5318–A5322. | p.2 `[20,22–24]` (불활성 용매 + 1–3 mm 볼 LWM 이 입경 감소에 성공) | 없음 → `[미확인]` |
| [25] | P. Minnmann, L. Quillmann, S. Burkhardt, F. H. Richter, J. Janek, *J. Electrochem. Soc.* **2021**, DOI 10.1149/1945-7111/abf8d7. | **p.2 `[20,25]` (1/3)** | [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) — wet-mill 10 h: 1.6 → 1.2 mS/cm (×0.75); "40 h · 1/3" 은 카드에 없음 |
| [26] | S. Wang, W. Zhang, X. Chen, D. Das, R. Ruess, A. Gautam, F. Walther, S. Ohno, R. Koerver, Q. Zhang, W. G. Zeier, F. H. Richter, C. Nan, J. Janek, *Adv. Energy Mater.* **2021**, 2100654. | p.3 (결정 SE 가 유리-세라믹보다 전자전도↑·접촉손실↑) | 없음 → `[미확인]` |
| [27] | A. L. Santhosha, L. Medenbach, J. R. Buchheim, P. Adelhelm, *Batteries & Supercaps* **2019**, *2*, 524–529. | p.5 (R_In–Li∣SE ≈ 10 Ω cm²) | 없음 → `[미확인]` |
| [28] | A.-Y. Kim, F. Strauss, T. Bartsch, J. H. Teo, T. Hatsukade, A. Mazilkin, J. Janek, P. Hartmann, T. Brezesinski, *Chem. Mater.* **2019**, *31*, 9664–9672. | p.5 실험절 (LNO 코팅 프로토콜) | 없음 → `[미확인]` |

([1]–[3] = Li 금속·필라멘트 일반 서론, [17] = Duchardt 2020 *ACS Appl. Energ. Mater.* 3, 6937–6945 (Cl↑ → Li₂S↓ 가격). 판정에 무관해 표에서 뺐다 — 서지는 PDF p.6.)

**"3 mS/cm 의 1차 출처 후보" 로서의 판정:** 문장 자체가 무인용이다. 인접 블록 `[4–10]` 중 우리가 원문 확인한 것은 **[6] Doux 2020 하나**이고 거기 LPSCl 값은 **2–2.5 mS/cm** 다. 같은 서론의 `[13]` Adeli 2019 도 Li₆PS₅Cl(x = 0) **2.5 mS/cm** 다. ⇒ "about 3" 은 **펠릿 문헌값(2–2.5)을 반올림한 일반 서술**로 읽는 것이 가장 정직하다. **3.0 을 준 1차 문헌은 이 논문의 인용 사슬 안에서 확인되지 않는다** (나머지 후보 [4]·[5]·[7]–[10] 은 `[미확인]`).

---

## 3. 핵심 수치

범례 — **stated** = 본문 숫자 그대로 · **digitized** = 그림에서 읽음 (방법·오차는 §6-2; **TREND 전용** — 1차 수치로 쓰지 않는다) · **derived** = 우리 산수 (가정 명시).

### 3-1. 전도도 (EIS, 98 MPa stack pressure, 온도 **n/a — 본문 미기재**)

| 양 | 값 | 조건 | 라벨 |
|---|---|---|---|
| gc-LPSC+ (HDM 직후, "untreated") | **2.5 mS/cm** | HDM 10 mm 볼 (가능한 최대 볼), 850 rpm 8.25 h | stated (p.2) · Fig. 2 ≈ 2.50 ✓ |
| gc-LPSC+ LWM **2 h** (1 mm 볼) | **1.73 mS/cm** | 셀용 SE | stated (p.5) · Fig. 2 (1 mm) ≈ 1.71 · Fig. 5b ≈ 1.75 |
| gc-LPSC+ LWM **50 h** | **0.36 mS/cm** | 셀용 SE | stated (p.5) · Fig. 5b ≈ **0.39** (⚠ 불일치, §10) |
| 2 h / 50 h σ 비 | **≈ 4.8** | — | stated (p.5); Fig. 5b 로는 1.75/0.39 ≈ 4.5 (derived) |
| 2 h / untreated | 1.73 / 2.5 = **0.69** | — | derived (stated 값) |
| 50 h / untreated | 0.36 / 2.5 = **0.14** (≈ 1/7) | — | derived (stated 값) — ⚠ 서론 문헌의 "1/3" 보다 **더 크게** 떨어짐 |
| µc-LPSC+ (어닐, untreated) | **≈ 3.97 mS/cm** | 550 °C 12 h | digitized (Fig. 2 우) — ⚠ 98 MPa 는 µC 의 stack-pressure 비포화 구간 (§10) |
| HDM 볼 크기별 σ (gc, 건식) | 1 mm **0.231** · 3 mm **0.603** · 10 mm **2.501 mS/cm** | Fig. S1 | **digitized-exact** (벡터 경로 좌표, ±0.001) |
| 문헌: LPSC | "about 3 mS/cm" | 무인용 | stated (p.1) — 2차 서술 |
| 문헌: LPSC+ (결정, 최적) | "8–10 mS/cm" | `[11–14]` | stated (p.1) |
| 문헌: gc-LPSC+ 6 h 볼밀 | "about 3 mS/cm" | `[11]` | stated (p.1) |
| 문헌: LWM > 40 h | "about 1/3 of the original value" | `[20,25]` | stated (p.2) — 시간 서술, 입경 없음 |

### 3-2. 입자크기 (방법 **미기재** — SEM 육안 평균으로 보임, 개수·분포 통계 없음)

| 조건 | 평균 입경 d_SE | 라벨 |
|---|---|---|
| HDM 직후 (pristine gc) | **"about 20 μm"** (p.3, Fig. 3a) ⚠ 같은 쪽 뒤에서 **"4 μm (untreated material)"** (p.3, Fig. 3a 를 다시 가리킴) — **자기모순** | stated ×2 |
| LWM 4 h, 200 rpm, **10 mm** 볼 | "drastic reduction" + **Ø ≈ 20 µm 덩어리 잔존** | stated (p.3, Fig. 3b) |
| LWM 4 h, **3 mm** 볼 | **1.6 µm** (개별 > 5 µm 존재) | stated (p.3, Fig. 3c) |
| LWM 4 h, **1 mm** 볼 | **1.0 µm**, 매우 좁은 분포 | stated (p.3, Fig. 3d) |
| LWM 1 mm, **30 min** | 4 µm → **1.8 µm** | stated (p.3, Fig. 4a) |
| LWM 1 mm, **1 h · 2 h** | **1 µm** | stated (p.3, Fig. 4b,c) |
| LWM 1 mm, **4 h** | "no significant further reduction" | stated (p.3, Fig. 4d) |
| LWM **50 h** | **미보고** — λ 역산 ≈ 0.9 µm | derived (Fig. 5b λ, d_CAM 3.5) |
| CAM (NCM-85, LNO 코팅) | **3.5 µm** | stated (p.3) |
| 요구 조건 | λ = d_CAM/d_SE ≥ 2 `[20]` · CAM < 5 µm 전형 `[21]` → d_SE < 2.5 µm | stated (p.1) |

### 3-3. 셀 (In 음극, 25 °C, 98 MPa, 0.6 C = 1.27 mA/cm²)

| LWM | 첫 방전 (stated) | 과전압 (stated, **정의 미기재**) | Fig. 5a 방전 끝 (digitized) | Fig. 5a 충전 끝 (digitized) | 첫 사이클 CE (derived) |
|---|---|---|---|---|---|
| untreated | **152 mAh/g** | **100 mV** | ≈ 154 | ≈ 222 | ≈ 70 % |
| 0.5 h | **160** | **60 mV** | ≈ 162 | ≈ 214 | ≈ 75 % |
| 1 h | "further improvements" | — | ≈ 170 | ≥ 211 (다른 곡선에 가림) | — |
| **2 h** | **179** (최대) | η_2h **60 mV** | ≈ 179 | ≈ 234 | ≈ 76 % |
| 4 h | **172** | **80 mV** | ≈ 172 | ≈ 220 | ≈ 78 % |
| 50 h | **< 140** | η_50h **150 mV** | ≈ 136 | ≈ 188 | ≈ 72 % |
| untreated (본문 기준 — ⚠ SI 캡션은 "2 h LWM"), **0.1 C** | **187** (Fig. S3) | — | S3 ≈ 186 | S3 ≈ 227 | ≈ 82 % |

- ⚠ 첫 충전 용량 (최대 ≈ 234 mAh/g) 이 **명시된 이론용량 200 mAh/g 을 넘는다** — 첫 충전에 CAM 외 기여(부반응)가 섞였다는 뜻이지만 논문은 다루지 않는다.
- 전압축 라벨 "V vs Li" (Fig. 5a · S3 · S4) ↔ 본문·S3 범례는 **vs In/Li** (컷오프 3.7 / 2.2 V vs In/Li). 축 라벨 오기로 본다.

### 3-4. 저항 분해 (p.5, stated) + 우리 점검

| 항 | 값 | 출처 |
|---|---|---|
| R_2h = η_2h/j | 60 mV / 1.27 mA cm⁻² = **47 Ω cm²** | stated |
| R_50h | 150 / 1.27 = **118 Ω cm²** | stated |
| R_separator (500 µm, σ 2.5) | **20 Ω cm²** | stated (L/σ = 0.05 cm / 2.5e-3 S cm⁻¹ ✓) |
| R_In–Li∣SE | **≈ 10 Ω cm²** | **문헌값** `[27]` (이 셀에서 측정 안 함) |
| R_cathode,2h / R_cathode,50h | **≈ 17 / ≈ 88 Ω cm²** → 비 ≈ 1/5 | stated |
| σ 역비 (1.73 / 0.36) | ≈ **4.8** → "매우 가깝다" | stated |
| ⚠ 분리막 밀도 점검 | 100 mg ÷ (π·(0.5 cm)² × 0.05 cm) = **2.55 g/cm³** | derived — LPSCl 이론밀도 1.64 (Bazzoun 카드) ~ 1.87 g/cm³ (Minnmann 카드) 의 **136–155 %** → **불가능**. 100 mg 이 맞다면 완전치밀이어도 **681–776 µm** |
| ⚠ 그 경우 분해 | L = 0.68 mm (완전치밀, ρ 1.87) ~ 0.80 mm (상대밀도 85 % **가정**) → R_sep 27–32 → R_cathode,2h 10–5 · R_cathode,50h 81–76 → 비 **8–15** | derived — "≈ σ 역비 4.8" 일치가 **분리막 두께 값에 민감**하다 (어느 쪽 숫자가 틀렸는지는 논문만으로 판정 불가) |
| C-rate 규약 | 13 mg × 70/103 ÷ 0.785 cm² = 11.25 mg_CAM/cm² → 1 C ≈ 2.12 mA/cm² ≈ **188 mA/g** | derived (LNO@NMC 질량 = CAM 질량 가정; 논문 미기재) |
| 복합양극 조성 | SE : LNO@NMC : CNF = **30 : 70 : 3 wt** → SE ≈ **52–56 vol % of (SE+CAM)** | wt stated · vol derived (ρ_SE 1.87/1.64, ρ_CAM 4.77 — 둘 다 **다른 조성의 카드값** 차용) |

---

## 4. 방법 ★ (실험 논문 — 시뮬레이션 없음)

### 4-1. 합성 (p.5 실험절)
- **gc-LPSC+ (HDM)**: LiCl (99.9 %) · Li₂S (99.99 %) · P₂S₅ (99 %) (모두 Sigma Aldrich) 화학량론 → **20 mL ZrO₂ 용기, ZrO₂ 볼 10개 (Ø 10 mm)**, **Fritsch Pulverisette 7 premium line**, **850 rpm, 8.25 h** → 마노 막자사발 분쇄. 어닐 없음 = "glass-ceramic".
- **µc-LPSC+** (실험절 표기 "c-LPSC+"): gc 펠릿을 석영 앰플에서 **550 °C 12 h** (승온 60 °C/h) 어닐 → 막자 분쇄.
- HDM 볼 크기: gc 는 **10 mm 가 최고 σ (2.5 mS/cm)** — 더 작은 볼(1·3 mm)로는 σ 0.23·0.60 (Fig. S1). 원인은 **논문이 논하지 않는다** — 기계화학 반응 에너지 부족으로 읽는 것은 **우리 해석**이다 (저자 서술은 "가장 큰 볼이 최고" 까지; S1 시료의 rpm·시간도 미기재). µc 는 어닐이 σ 를 정해 볼 크기 무관 (stated).

### 4-2. 입자 미세화 = LWM (p.5)
- 같은 20 mL ZrO₂ 용기. ZrO₂ 볼 **10 mm (10개)** 또는 **3 mm / 1 mm (각 30 g)**.
- 용매 **헵탄 4.0 mL + 다이부틸에터 0.8 mL** (볼 크기 무관), **200 rpm**, **30–240 min** (**30 min 밀링 / 30 min 휴지** 반복), 진공 건조 → 막자 분쇄.
- ⚠ **50 h 시료는 이 명시 범위 (30–240 min) 밖**이다 — 50 h 의 절차는 기술되지 않았다. "밀링 시간" 이 **순수 밀링 시간인지 휴지 포함 경과 시간인지** 미기재.

### 4-3. 전도도 측정 (p.5)
- **rhd instruments CompreDrive** 자동 다이프레스 안에서: 분말 **105 mg → 394 MPa, 60 s 성형** → **압력 완전 해제** → **stack pressure 98 MPa** 걸고 EIS.
- Metrohm Autolab **PGSTAT302N**, **10⁵–10¹ Hz**, AC **10 mV**.
- **미기재**: 측정 **온도**, 전극 재질, 펠릿 두께·직경, σ 추출 방식(등가회로/절편), 반복 수·오차. **Nyquist 선도 미제시** → bulk/GB 분리 **불가**.

### 4-4. 셀 (p.5–6)
- CAM: NCM-85∣10∣05 (BASF, 이론 200 mAh/g) 에 **LiNbO₃ 코팅** (`[28]` 프로토콜: 1 M LiOEt/EtOH + Nb(OEt)₅, 6 g CAM, 75 °C 초음파조에서 EtOH 증발, 공기 중 **400 °C 1 h** (20 °C/h)). 코팅 두께·함량 미기재.
- 복합양극: SE : LNO@NMC : CNF = **30 : 70 : 3 wt**, 마노 막자 혼합.
- 분리막: **LWM 안 한 HDM LPSC+ 100 mg**, PEEK 몰드 **Ø 10 mm**, **294 MPa 60 s**.
- 적층: 복합양극 **13 mg** + In 시트 (**25 mg**, 300 MPa 예비압착) 양면 → **392 MPa** 치밀화 (SS 피스톤 2개).
- 운전: **25 °C**, **98 MPa**, 컷오프 **3.7 / 2.2 V vs In/Li**, 0.6 C = 1.27 mA/cm² (Fig. 5), 0.1 C (Fig. S3·S4). **조건당 셀 1개** (Fig. 5) · 2 h 조건만 3셀 (Fig. S4).

### 4-5. 입자 처리 (DEM 의 "무질서 처리" 에 해당) — n/a (실험)
- 실제 분말. **PSD 측정 없음** (레이저 회절 등 없음) — "평균 입경" 은 SEM 에서 본 값으로 보이며 **추출법·표본 수 미기재**. SEM 은 실험절에 **절 자체가 없다** (장비는 사진 데이터바에서만 보인다: ZEISS, 2 kV, SE2, WD 5 mm, 20 kX (Fig. 3) / 25 kX (Fig. 4), 촬영일 2021-03-26 · Fig. 3a 만 2021-04-03).
- XRD 도 실험절에 절이 없다 (방사선·장비 미기재; 2θ 10–90°).

---

## 5. Figure set ★ (9장 전부 크롭·실독)

| Fig | 무엇을 보여주나 (실독) | 우리가 가져갈 점 |
|---|---|---|
| **Fig. 1** | **개념도(수치 없음)**. x = 밀링 시간. 파란 점선 λ = d_CAM/d_SE 가 가파르게 올라 포화, 주황 점선 Li⁺ 전도도는 **직선 하강**, 초록 실선 용량은 **최대(별표)** 후 하강. | "밀링 → 접촉↑ vs σ↓" **상충 구조**의 교과서 그림. 수치로는 쓰지 않는다 (축 눈금 없음). |
| **Fig. 2** | σ vs LWM 시간 (0–240 min, 선형축), **좌 = gc-LPSC+ · 우 = µc-LPSC+**, 볼 10/3/1 mm + untreated. gc: 2.50 → 1.38–1.51 (240 min). µc: 3.97 → 1.47–2.44. 볼 크기별 순서가 **비단조** (예: gc 60 min 은 3 mm > 10 mm > 1 mm). 50 h 점은 **없다**. y축 라벨 오타 "conductivitiy". | 표 §6-2a. **같은 시간에서 볼 크기(=입경) 차보다 시간 차가 σ 를 지배** (저자: "ball size does not have a profound impact"). ⚠ µc 는 98 MPa stack 에서 비포화 (§10). |
| **Fig. 3** | SEM, LWM **4 h · 200 rpm**, 볼 크기별: a) pristine (둥근 덩어리 ~2–10 µm 이 시야 46 × 31 µm 에 보임) · b) 10 mm: 매끈한 판상 덩어리 (figure-read ≈ 13–15 µm, 본문 "Ø ≈ 20 µm") + 미분 · c) 3 mm: 평균 1.6 µm, 판상 파편 섞임 · d) 1 mm: 균일한 ~1 µm 응집체. 스케일바 4 µm, 20 kX. | **입경이 볼 크기에 강하게 의존**하는 것의 실물. Fig. 2 의 240 min 점들과 짝지으면 "입경 크게 다름 ↔ σ 거의 같음" (§0). ⚠ a) 에서 "평균 20 µm" 는 이 한 시야에서 눈에 띄지 않는다 — **figure-read, PSD 아님**. |
| **Fig. 4** | SEM, 1 mm 볼 · 200 rpm, **0.5 / 1 / 2 / 4 h** (25 kX, 스케일바 3 µm). 0.5 h: 각진 파편 (최대 ~4–5 µm, figure-read) · 1 h: ~1 µm 둥근 입자 + 일부 2–3 µm · 2 h · 4 h: ~1 µm 응집, 육안 차이 작음. **Fig. 3d 와 Fig. 4d 는 같은 조건 (1 mm·4 h) — 사진번호 5509 · 5510, 1분 간격 촬영**. | "1–2 h 면 입경은 끝난다" 의 실물 → 그 뒤 σ 하락은 **입경이 아닌 손상**. |
| **Fig. 5a** | 0.6 C 첫 사이클 충·방전 곡선 6개 (0.5 / 1 / 2 / 4 / 50 h + untreated). 2 h 가 가장 긴 방전 (≈179), 50 h 가 가장 짧고 방전 곡선이 가장 낮음 (≈136). | 표 §3-3. 조건당 셀 1개. |
| **Fig. 5b** | **로그 x (10–5000 min)**, 세 y축: 용량 (녹, 120–200) · **λ = d_CAM/d_SE (청, 0–5; 범례는 "Particle size")** · σ (주황, 0–2.7). 점: 30/60/120/240/3000 min. 점선 = **설명 없는 guide** (용량 포물선, λ 포화, σ 는 log t 에 직선). | 이 논문의 **요약 그림** — 표 §6-2b. ⚠ **λ 가 본문과 불일치** (2 h: 그림 2.90 vs 본문 "around 2.5" vs 본문 입경 1 µm → 3.5). |
| **Fig. S1** | 건식밀링(HDM) σ vs **볼 크기** — x축 라벨 **"Ball size / µm" (mm 의 오기)**. 1 → 0.23 · 3 → 0.60 · 10 → 2.50 mS/cm. | HDM 은 **큰 볼이어야 반응 완결** — 입경이 작을수록 σ 가 낮은 게 아니라 **반응 에너지** 문제. 크기-σ 서사와 섞지 말 것. |
| **Fig. S2** | gc-Li₅.₅PS₄.₅Cl₁.₅ **XRD, LWM 0.5 / 1 / 2 / 4 h** (2θ 10–90°, A.U., 오프셋). 반사 위치 ≈ 15.5·18·25.5·30·31.5·45·48·52.5° (figure-read) 로 전 시료 argyrodite 상 유지. 0.5 h 의 반사가 가장 날카롭고 높고, 1–4 h 는 서로 비슷하게 낮다. **pristine · 50 h 없음**. 정량(결정도·결정자 크기) 없음. | 저자의 "부분 비정질화" 근거의 **전부**. 50 h 의 σ 붕괴를 직접 받치지 않는다 (50 h XRD 없음). |
| **Fig. S3** | 0.1 C 첫 사이클 1셀, 98 MPa. 방전 ≈ 186 · 충전 ≈ 227 mAh/g (digitized). **캡션: "optimized SE (2 h LWM)"** ↔ **본문 p.3: "Without any LWM treatment … 187 mAh/g … (Figure S3)"** — **모순**. | 0.1 C 기준용량 187. 어느 SE 셀인지 확정 불가. |
| **Fig. S4** | 2 h LWM SE 셀 3개, 캡션 "0.1 C". 방전 ≈ 179 / 178 / 174, 충전 ≈ 234 / 234 / 226 (digitized). | ⚠ **Cell 1 (179/234) 이 Fig. 5a 의 2.0 h 곡선 (0.6 C, 179/234.5) 과 판독 정밀도 안에서 일치**하고, S3 (0.1 C) 보다 방전 시작 곡선 모양·충전 시작 전압(≈3.05 V vs S3 ≈2.96 V)이 Fig. 5a 쪽과 같다 → **S4 는 0.6 C 재현성 세트일 가능성** (캡션 오기 **가설**, 확정 불가). 셀간 산포 ≈ 5 mAh/g. |

---

## 6. Post-processing ★

### 6-1. 논문이 한 것
- σ: EIS 에서 추출 (방식 미기재). 수치화 = 그림 점 + 본문 몇 값.
- 입경: SEM 평균 (방식 미기재) → **λ = d_CAM/d_SE** (d_CAM = 3.5 µm) 로 환산해 Fig. 5b 에 표시.
- 셀: 첫 방전 용량 + "과전압" (정의 미기재) → **R = η/j** 옴 환산 → 분리막 (L/σ) · In 계면 (`[27]` 문헌값) 을 빼서 R_cathode → σ 역비와 대조 (p.5).
- 구조 인과: XRD (Fig. S2) 로 "부분 비정질화" 제시 — 정량 없음.
- 도구: 명시 없음 (그림 양식은 Origin 계열로 보임).

### 6-2. 우리 디지타이즈 (재현 가능한 방법 — 스크립트는 세션 스크래치, 결과는 아래 표가 정본)
- **Fig. 2**: 임베디드 래스터 (6784 × 2765 px) 를 그대로 추출 → 패널별 **y 주눈금 10개 · x 주눈금 6개 자동 검출**로 보정 (1 px = 0.0019 mS/cm) → 계열 색 마스크 → **고정 반경 원 맞춤** (배경과 맞닿은 경계 화소만, rms ≤ 0.7 px) — 1 mm 계열에 **가려진 3 mm 점 3개**(30·120·240 min)도 보이는 호에서 중심을 복원. 판독 오차 **±0.01 mS/cm** (가려진 점 ±0.02).
- **Fig. 5b**: 래스터 3203 × 1237 px, 세 y축을 **각 축 색의 눈금**으로 따로 보정 (녹 9개 · 청 11개 · 주황 11개), x 는 로그 주눈금 10/100/1000. 해상도: 용량 0.08 mAh/g/px · λ 0.005/px · σ 0.003 mS/cm/px. 점 중심 원 맞춤 → 오차 용량 ±0.3 · λ ±0.02 · σ ±0.01.
- **Fig. 5a**: 곡선 색 마스크 → 방전 끝 = 2.19–2.23 V 창의 x, 충전 끝 = 3.60–3.72 V 창의 최우측 x (0.21 mAh/g/px). 판독 **±1 mAh/g**. 1.0 h 충전 끝은 다른 곡선에 가려 **하한만**.
- **Fig. S1**: **벡터** 그림 → PDF 그리기 경로에서 원 3개와 눈금선 좌표를 직접 읽음 (±0.001, 사실상 정확).
- **Fig. S3·S4**: SI 래스터가 소프트마스크를 가져 페이지 렌더 (4×) 에서 판독, ±1 mAh/g.

**(a) Fig. 2 — σ (mS/cm) vs LWM 시간 (digitized, ±0.01; * = 가려진 점 ±0.02)**

| 재료 | t (min) | untreated | 10 mm | 3 mm | 1 mm |
|---|---|---|---|---|---|
| gc-LPSC+ | 0 | ≈ 2.50 | | | |
| | 30 | | ≈ 2.23 | ≈ 2.45* | ≈ 2.42 |
| | 60 | | ≈ 2.22 | ≈ 2.39 | ≈ 1.97 |
| | 120 | | ≈ 2.14 | ≈ 1.74* | ≈ 1.71 |
| | 240 | | ≈ 1.51 | ≈ 1.41* | ≈ 1.38 |
| µc-LPSC+ | 0 | ≈ 3.97 | | | |
| | 30 | | ≈ 3.76 | ≈ 3.66 | ≈ 3.27 |
| | 60 | | ≈ 3.62 | ≈ 2.84 | ≈ 2.52 |
| | 120 | | ≈ 2.92 | ≈ 2.53 | ≈ 2.35 |
| | 240 | | ≈ 2.44 | ≈ 1.47 | ≈ 2.08 |

정규화 (σ/σ_untreated, derived): gc 1 mm 0.97 → 0.79 → 0.68 → **0.55** (30→240 min) · gc 240 min 볼별 **0.60 / 0.56 / 0.55** (10/3/1 mm) · µc 1 mm 0.82 → 0.64 → 0.59 → **0.52**.

**(b) Fig. 5b — 셀용 gc-LPSC+ (digitized) + λ 역산 입경 (derived)**

| t (min) | 용량 (mAh/g) | λ | σ (mS/cm) | d_SE = 3.5/λ (µm) | 본문 입경 → λ | Fig. 2 (1 mm) σ |
|---|---|---|---|---|---|---|
| 30 | ≈ 162 (본문 160) | ≈ 1.16 | ≈ 2.40 | ≈ 3.0 | 1.8 µm → **1.94** | ≈ 2.42 |
| 60 | ≈ 170 | ≈ 1.75 | ≈ 1.90 | ≈ 2.0 | 1 µm → **3.5** | ≈ 1.97 |
| 120 | ≈ 179 (본문 179) | ≈ **2.90** (본문 "around 2.5") | ≈ 1.75 (본문 1.73) | ≈ 1.2 | 1 µm → **3.5** | ≈ 1.71 |
| 240 | ≈ 172 (본문 172) | ≈ 3.50 | ≈ 1.52 | ≈ 1.0 | 1.0 µm → **3.5** ✓ | ≈ 1.38 |
| 3000 (50 h) | ≈ 136 (본문 < 140) | ≈ 3.88 | ≈ **0.39** (본문 0.36) | ≈ 0.9 | 미보고 | (없음) |

→ λ 는 **240 min 에서만** 본문 입경과 맞는다. σ 는 30/120 min 에서 Fig. 2 (1 mm) 와 맞고 60 min (−0.07) · 240 min (+0.14) 에서 어긋난다 — Fig. 5b 의 σ 가 **별도 배치 측정인지** 논문은 말하지 않는다.

**(c) Fig. S1 (exact)**: HDM 볼 1 / 3 / 10 mm → **0.231 / 0.603 / 2.501 mS/cm**.

---

## 7. 우리 모델 대비 ★  (`our_dem_baseline.md` 는 정본에서 **값 없는 자리표시** — "우리" 값은 작업 브랜치 `claude/stoic-knuth-NObVQ` @ `766c0405b` 코드에서 직접 인용)

### 7-1. 대조표

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| SE 재료 | **Li₅.₅PS₄.₅Cl₁.₅** (gc · µc) | Li₆PS₅Cl (LPSCl) | **다른 조성.** Cl-rich 라 결정상 σ 가 원래 높다 (문헌 8–10 vs LPSC 2–3). 절대값 전이 금지. |
| σ_SE 앵커 | gc 2.5 (98 MPa stack, T 미기재, 펠릿) · µc ≈ 4.0 (비포화 stack) | `σ_grain = 3.0 mS/cm` (`se_material.py:85`, 25 °C **규약**, "grain interior", **1차 출처 없음**으로 09-25 정정됨) | 이 논문은 3.0 을 **주지 않는다** (§0). 펠릿 σ 는 GB·공극 포함이라 grain-interior 와 **다른 양**. |
| 입자크기 계수 | σ(밀링 시간) 만; **σ(r) 없음**, 최소 d ≈ 1.0 µm | `Cronau(r_SE)`: ≥ 0.5 µm 1.00 · 0.3–0.5 0.90 · 0.1–0.3 0.65 · 0.03–0.1 보간 · < 0.03 0.33 (`generate_comparison_plots.py:4342` · `run_network_full_corrections.py:110`) | **구간값 전부 이 논문 밖.** 방향(밀링↑·입경↓ ↔ σ↓)만 교란된 채 지지. |
| r = 0.5 µm (우리 생산) | 2 h (d ≈ 1 µm): σ/σ_untreated = **0.69** (stated) · 4 h (d 1.0): **0.55–0.61** (digitized) | 계수 **1.00** | **밀링으로 만든 1 µm 분말이라면** 이 논문·Minnmann 2021 (×0.75)·Lee 2025 (×0.75, 볼밀 LPSCl, [`lee2025_corolling_dryprocess_lpscl_ptfe`](lee2025_corolling_dryprocess_lpscl_ptfe.md)) 모두 **25–45 % 손실**을 보인다. 단 그 손실은 **펠릿**의 **이력**(밀링) 효과이고 우리 3.0 은 grain-interior 규약값 — 같은 축이 아니다. |
| 긴 밀링 한계 | 50 h: **0.14** (stated) · 문헌 > 40 h: "≈ 1/3" | < 30 nm: **0.33** | 0.33 은 **입경 축에 놓인 "1/3"**. 이 논문 자신의 긴 밀링 값은 0.14 이고, 그때 입경은 ≈ 0.9 µm 다. |
| 크기 효과의 **기원** | 부분 비정질화 (XRD, 자체 해석) · 입자경계 저항 + 잔류 용매 (문헌 [20,25]) | CLAUDE.md: "SE **material** property (amorphization at sub-µm)" · 일부 주석: "GB factor" | "비정질화" 라는 **기전 단어는 맞다** — 틀린 것은 그것을 **r 의 함수**로 둔 것. 비정질화는 **밀링 에너지·시간·용매**의 함수다. |
| 독립 교차 | — | [`schlautmann2023_se_particle_size_composite_transport`](schlautmann2023_se_particle_size_composite_transport.md): 순수 LPSCl 펠릿 σ **2.2 mS/cm, D50vol 4 → 40 µm 에서 평평** (XRD·PDF·Raman 불변) | **밀링 손상 없이 입경만 바꾸면 σ 는 안 변한다** (> 4 µm 구간). Cronau 2022 의 σ 하락이 **손상**이라는 읽기와 정합. 서브-µm 는 두 논문 모두 미검정. |
| 셀 수준 | R_cathode ∝ 1/σ_SE (λ 포화 후, p.5) | σ_ionic 폼이 `σ_grain` 에 **선형** (배율 인자) | **방향 정합** (고정 미세구조에서 복합체 R ∝ 1/σ_SE). 단 이 논문의 확인은 분리막 두께 값에 민감 (§3-4) → 약한 지지. |
| 측정 규약 | 394 MPa 성형 → 해제 → 98 MPa stack | STEP3·DEM 은 σ_SE 를 입력으로 받음 | Cronau **2021** 카드: GC 는 stack > 30–50 MPa 에서 포화, **µC 는 ≳ 200–250 MPa 에서야 포화** → 이 논문 µc 값은 **비포화 구간** 측정일 가능성 (이 논문은 언급 안 함). |

### 7-2. frame[5] — 이 논문이 가진 절반 / 없는 절반
- **가진 것**: **SE 재료 입력** (σ_SE 의 공정 이력 의존성) + **셀 성능** (용량·과전압). 우리 쪽에서는 **두 수송 솔버가 공유하는 입력**에 해당한다 — `σ_grain` 은 DEM 접촉망 σ_ionic 폼과 STEP3 복셀 FV (`step3_sigma.py:76`) 가 **같은 정의** (`se_material.py`) 를 쓰고, `Cronau(r_SE)` 는 **DEM σ_ionic 쪽에만** 곱해진다 (`run_network_full_corrections.py` · `generate_comparison_plots._sat_baselog`).
- **없는 것**: 미세구조 (공극률·굴곡도·배위수), 복합체 **유효 σ_ion,eff** 측정, 역학 (압밀·형상) — DEM·MPM 어느 쪽에도 **구조 앵커는 주지 않는다.**
- frame[4] 관점: 이 논문은 우리 두 모델 **어느 쪽의 교정 앵커도 아니다** — 재료 상수 **라벨**의 출처 감사 대상일 뿐이다.

### 7-3. 판정 정리 (주의사항을 먼저 떼어 낸 뒤)
1. **재료 전이 금지** — LPSC+ ≠ LPSCl. σ 절대값 대조는 불가, "밀링 → σ↓" 의 **비율 추세**만 참고.
2. **디지타이즈 ≠ stated** — §3 은 두 층을 분리해 적었다. 인용은 stated 만 (2.5 · 1.73 · 0.36 · 4.8 · 20/4 · 1.8 · 1.6 · 1.0 µm · 187/179/172/160/152 mAh/g · 47/118/20/10/17/88 Ω cm²).
3. **교란** — 입경과 손상이 같은 노브 (밀링 시간)로 움직인다. 이 논문으로 "입경 자체의 σ 효과" 를 주장할 수 없다.
4. ⇒ **실제 차이는 "라벨" 에 있다 — 값 자체는 이 논문으로 옳다/그르다 판정되지 않는다.** `σ_grain 3.0` 은 펠릿 문헌 밴드 (1.0–4.8, `se_material.py:81–84` 주석) 안이고, `Cronau(r_SE)` 구간값은 **검증도 반증도 되지 않은 가정**이다 (이 논문에 해당 입경 데이터가 없으므로).

### 7-4. 작업 브랜치에서 "Cronau" 를 근거로 달고 있는 자리 (`766c0405b` 기준 — **수정은 사용자 비준 후, 이 카드는 목록만**)
- σ_grain 3.0 ↔ "Cronau": `scripts/step3_sigma.py:76` `(Cronau)` · `scripts/step3_transport_resolution.py:39` `(Cronau, se_material)` · `scripts/mpm_webapp_payload.py:1232` `(Cronau — production σ_grain anchor)` · `scripts/electronic_locked_sigma_test.py:5` (`se_material.py` · `final_form_status.py:58` · `generate_fitting_report.py` 는 09-25 에 이미 정정됨).
- 입자크기 계수 ↔ "Cronau 2022": `scripts/run_network_full_corrections.py:12–13` (모듈 docstring — **현재 함수와도 다른 옛 표** 1.5→1.00 · 1.0→0.85 · 0.5→0.70 · <0.3→0.33 가 남아 있다) · `:115–123` ("Cronau optimum", "Cronau extreme-milling limit", "**Cronau 2022's 1/3 reduction … D50 < 0.3 μm**" ← 이 논문에 없는 서술) · `:1195` (출력 문구 "(Cronau 2022)") · `scripts/generate_comparison_plots.py:4268–4275` · `:4343` ("Cronau 2022 … amorphization").
- 이력 (원장 SELF-51 · git): 04-30 `ceee1d812` 가 처음 "Cronau 2022" 를 달 때의 근거 문장은 *"assuming Cronau's 0.70 overall reduction at r_SE=0.5/1.5 splits roughly half-half"* 였다 — **0.70 ≈ 이 논문의 2 h/untreated = 0.69** 와 수치가 맞지만, 기준 상태는 **r = 1.5 µm 가 아니라 "untreated (20 µm 또는 4 µm)"** 이고 독립변수는 **밀링 시간**이다. (이 대응은 **추정**이다 — 그 커밋이 이 논문을 봤다는 증거는 코드에 없다.)

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

- ① **라벨 정정의 원문 근거 확보** — SELF-51 2단계(σ_grain) 는 이 카드로 **확정**, 3단계(Cronau(r_SE) 구간값) 는 "문헌 근거 없음 · 방향만" 으로 닫을 수 있다. 원고·SI·웹앱 문구에서 *"Cronau 2022 single-crystal"* · *"Cronau: σ drops to 1/3 below 30 nm"* 는 **쓸 수 없다.**
- ② **"크기 계수" 를 "공정 이력 계수" 로 재해석할 여지** — 세 정본 카드가 **적당한 밀링 → ×0.69–0.75** (Cronau 2 h · Minnmann 10 h · Lee 2025 볼밀) 로 모인다. 우리가 SE 를 "밀링으로 만든 1 µm" 로 가정한다면 그 몫은 r 의 함수가 아니라 **별도 이력 인자**로 두는 것이 물리에 맞다. ⚠ **제안일 뿐** — 폼 변경은 σ_ionic 동결 규약 (CLAUDE.md "DO NOT add more form terms") 과 부딪히므로 **1저자 판단**.
- ③ **λ ≥ 2 기준** (Shi 2020 경유) 은 우리 크기비 논의 (`d_h`, Furnas dip, "size = packing") 와 같은 방향이다 — 단 이 논문의 λ 값 자체는 내부 불일치 (§6-2b) 라 **수치 앵커로 쓰지 않는다.**
- ④ **측정 규약 경고의 재확인** — σ_SE 를 문헌에서 가져올 때 **stack pressure · 결정도 클래스 · 온도** 를 같이 적지 않으면 비교가 성립하지 않는다 (이 논문은 온도를 안 적었다).

## 9. 인용 가능 문장 (deck/paper용)

- ✅ *"Low-energy wet milling of glass-ceramic Li₅.₅PS₄.₅Cl₁.₅ reduces the particle size to ~1 µm but also lowers the ionic conductivity from 2.5 to 1.73 mS cm⁻¹ after 2 h and to 0.36 mS cm⁻¹ after 50 h (EIS at 98 MPa stack pressure), which the authors attribute to partial amorphization during milling (Cronau et al., Batteries & Supercaps 2022, 5, e202200041)."*
- ✅ *"An optimum wet-milling time of about 2 h (1 mm ZrO₂ balls) balances the CAM/SE size ratio against the conductivity loss, giving the highest first discharge capacity (179 mAh g⁻¹ at 0.6 C, NCM-85/In cells at 98 MPa) (Cronau et al., 2022)."*
- ✅ (우리 모델 주석용) *"The size-dependent conductivity factor used in our model is a project-adopted assumption. Cronau et al. (2022) support only the qualitative trend that extended milling lowers argyrodite conductivity, which they attribute to milling-induced amorphization; they report no conductivity for sub-µm particles."*
- ⛔ **인용 금지**: "Cronau 2022: Li₆PS₅Cl single-crystal 3.0 mS/cm" · "Cronau 2022: σ falls to 1/3 for particles ≤ 30 nm / D50 < 0.3 µm" · "Cronau 2022 measured σ as a function of particle radius".

## 10. 주의/한계 (over-claim 방지) — 논문 자체의 문제 포함

1. **재료**: 측정은 **Li₅.₅PS₄.₅Cl₁.₅** 뿐. Li₆PS₅Cl 측정 **0**, 단결정 측정 **0**.
2. **교란**: 입경·손상이 밀링 시간으로 함께 움직인다. 제목의 "versus Particle Size" 는 **분리 측정이 아니다**.
3. **입경 방법 부재**: SEM 평균의 산출법·표본 수 없음. pristine 이 **"about 20 μm"** 와 **"4 μm (untreated material)"** 로 **같은 쪽에서 두 번 다르게** 적혔다 (둘 다 Fig. 3a 를 가리킴).
4. **λ 불일치**: 2 h 에서 Fig. 5b **≈ 2.90** · 본문 **"around 2.5"** · 본문 입경 1 µm 에서 **3.5**. 30 min 은 그림 1.16 vs 본문 입경 → 1.94.
5. **σ 불일치**: 50 h 본문 **0.36** vs Fig. 5b **≈ 0.39**; Fig. 5b σ 가 Fig. 2 의 1 mm 계열과 60·240 min 에서 어긋남 (−0.07 · +0.14).
6. **EIS 보고 부족**: 온도 미기재, Nyquist 없음, bulk/GB 분리 없음, 반복·오차 없음.
7. **µc 측정 압력**: 98 MPa 는 Cronau **2021** (같은 그룹) 이 보인 µC 의 **stack-pressure 비포화 구간** (포화 ≳ 200–250 MPa) → Fig. 2 우측 µc 값과 "µc 가 더 가파르게 떨어진다" 는 결론이 **접촉 한계에 오염**됐을 수 있다 (이 논문은 논의 안 함 — 카드 간 추론).
8. **프로토콜 범위**: 실험절 LWM 은 30–240 min 인데 **50 h 시료**가 쓰였다 (절차 미기재). 밀링 시간이 순수 밀링인지 휴지 포함인지 미기재.
9. **분리막 질량·두께 모순**: 100 mg · Ø 10 mm · 500 µm → 2.55 g/cm³ (이론의 136–155 %). p.5 의 "R_cathode 비 ≈ σ 역비" 확인이 이 값에 민감 (두께가 질량 쪽이 맞으면 비 8–15). R_In–Li∣SE 도 **문헌값** (`[27]`).
10. **셀 통계**: Fig. 5 는 **조건당 1셀**. S4 의 3셀 산포 ≈ 5 mAh/g 를 적용하면 1 h (170) · 4 h (172) 차는 분해 불가, 2 h (179) 우위도 산포의 ~1.5배 수준.
11. **캡션/라벨 오류**: S3 캡션 (2 h LWM) ↔ 본문 (LWM 없음) · S4 캡션 "0.1 C" ↔ Cell 1 이 Fig. 5a 2 h (0.6 C) 와 일치 · Fig. S1 x축 "µm" (실제 mm) · Fig. 5a/S3/S4 "V vs Li" (실제 vs In/Li) · CAM 표기 "NCM-85∣10∣05" (본문) ↔ "NMC-85∣05∣10" (실험절 제목·감사의 글).
12. **첫 충전 > 이론용량**: 최대 ≈ 234 mAh/g > 200 — 부반응 기여 미논의.
13. **데이터 비공개** — 모든 그림 값은 디지타이즈 (TREND) 로만 쓸 수 있다.

---

## 🔤 기법 미니 용어집

- **HDM (high-energy dry milling)**: 원료 분말을 큰 볼·고속 (여기 10 mm · 850 rpm · 8.25 h) 으로 건식 기계화학 합성. 반응 에너지가 부족하면 (작은 볼) σ 가 낮다 (Fig. S1).
- **LWM (low-energy wet milling)**: 합성된 SE 를 불활성 용매 (헵탄 + 소량 다이부틸에터) 속 작은 볼·저속 (200 rpm) 으로 **분쇄만** 하는 단계. 입경은 줄지만 결정 손상·잔류 용매를 남길 수 있다.
- **gc / µc (glass-ceramic / microcrystalline)**: gc = HDM 직후 (비정질 매트릭스 + argyrodite 결정자), µc = 550 °C 어닐로 결정화. Cronau 2021 에서 두 클래스는 **stack pressure 응답이 다르다** (µC 가 더 높은 압력에서야 포화).
- **argyrodite Li₆₋ₓPS₅₋ₓCl₁₊ₓ**: x = 0 이 LPSC (Li₆PS₅Cl), x = 0.5 가 LPSC+ (Li₅.₅PS₄.₅Cl₁.₅). Cl↑ → Li 공공·자리 무질서↑ → σ↑ (Adeli 2019 카드).
- **λ = d_CAM/d_SE**: 양극활물질 대 SE 입경비. Shi 2020 (`[20]`): **λ ≥ 2** 면 CAM 표면을 SE 가 잘 덮어 이용률↑.
- **fabrication vs stack pressure**: 펠릿을 **만드는** 압력 (여기 394 MPa, 해제) 과 측정 중 **걸어 두는** 압력 (98 MPa). 측정 σ 는 둘 다에 의존한다 (Cronau 2021).
- **EIS 이온전도도**: 블로킹 전극 사이 펠릿의 교류 임피던스에서 저항 R 을 읽어 σ = L/(R·A). 저주파 확산·전극 효과와 bulk/GB 반원을 분리해야 "grain" 값이 된다 — 이 논문은 분리를 보이지 않았다.
- **In/Li 음극 전위**: In–Li 합금 기준 전압은 Li/Li⁺ 기준보다 수백 mV 낮게 읽힌다 → 3.7 V vs In/Li 는 Li 기준으로 그만큼 높다. ⚠ **이 논문은 오프셋 값을 주지 않는다** — 우리 CLAUDE.md STEP4 절이 적는 후보값 (Li–In 0.62 V) 은 이 논문 출처가 아니다.
- **LiNbO₃ (LNO) 코팅**: 층상 산화물 CAM 과 황화물 SE 사이 계면 반응을 막는 얇은 산화물 층 (`[28]` 프로토콜).
- **C-rate**: 1 C = 1 시간에 공칭 용량을 다 쓰는 전류. 여기 0.6 C = 1.27 mA/cm² (stated) → 1 C ≈ 188 mA/g (derived).
- **과전압 η (이 논문)**: 정의 미기재 — 저자는 η/j 를 셀 전체 저항으로 읽었다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

---
title: "Huo, Li, Fan, Zhang, Han, Wang, Zhou, Chen, Jia 2025 — Characterization of cathode degradation and development of a coupled electrochemical-aging model for sulfide-based all-solid-state batteries (J. Power Sources 627, 235830)"
source_url: local-upload/09._Characterization_of_cathode_degradation_and_development_of_a_coupled_electrochemical-aging_model_for_sulfide-based_all-solid-state_batteries.pdf
source_url_note: "본문 11쪽 + SI .docx. ★ SI 는 파라미터 표가 아니라 *Journal of Power Sources* 투고 체크리스트다 — 보충 그림 0, 보충 데이터 0. 그럼에도 N/P 와 쿨롱 효율의 제출 거부 사유가 SI 에만 있고 본문 결론에 직결된다. `.docx` 는 zipfile + word/document.xml 태그 제거로 전수 읽었다."
source_doi: 10.1016/j.jpowsour.2024.235830
pdf_sha256_main: 9f2496907f7e65a0a44ad9eebedb92149604b43d1c2eac0862d4785140ac9d29
docx_sha256_si: cee297a20e00d37e616960f7014c165873a388d5b24acb7fb21ca8878441b391
ingested: 2026-09-22
sha256: 6e5a6471b9233090b7db442c5d83f36a07d9b73470311fd23cf251cd33b911c1
---

# 수집 목적

Dexin Huo, Guoliang Li, **Guodong Fan**(교신), **Xi Zhang**(교신), Jingbo Han,
Yansong Wang, Boru Zhou, Shun Chen, Linan Jia (Shanghai Jiao Tong University,
School of Mechanical Engineering + National Engineering Research Center of
Automotive Power and Intelligent Control)
— **"Characterization of cathode degradation and development of a coupled
electrochemical-aging model for sulfide-based all-solid-state batteries"**,
*Journal of Power Sources* **627** (2025) 235830,
doi `10.1016/j.jpowsour.2024.235830`,
`[인쇄]` Received 28 Aug 2024 / Revised 31 Oct 2024 / Accepted 9 Nov 2024 /
Available online 15 Nov 2024. Elsevier, 구독.
`[인쇄]` 교신 `guodong.fan@sjtu.edu.cn` · `braver1980@sjtu.edu.cn`.
`[인쇄]` 자금: NSFC 52307246 · 52177218 · Shanghai NSF 23ZR1429100.
`[인쇄]` 이해상충 없음 선언. `[인쇄]` "Data will be made available on request."

의 **절별 해체분석** — 본문 PDF **11 쪽** + SI **.docx**.
두 파일 모두 sha256 을 frontmatter 에 봉인했다.

**이 위키 `assb` 섹션의 9호 자료이고, 앞 8 편 중 어느 것과도 성격이 다르다.**

- 1–3호(Bielefeld · Clausnitzer · Liu)는 **순수 시뮬레이션**, 4–7호(Shi · Doux ·
  Lee · Spencer-Jolly)는 **순수 실험**, 8호(Li et al.)는 **Mini Review** 였다.
- **9호는 이 계보 최초로 실험과 역문제(파라미터 식별)를 한 논문 안에서 잇는다.**
  그리고 그 때문에 **이 닻 카드의 Q4(유일성)에 처음으로 실질적으로 걸린다** —
  1–3호는 forward 전용이라 원리적으로 못 쟀고, 5–7호는 역문제를 아예 안 풀었으며,
  4호는 EIS 등가회로만 풀었다. **9호는 열화 모드의 지분 자체를 적합으로 정한다.**

> ⚠ **이 digest 의 표기 3분**: `[인쇄]` = 본문/SI 지면에 문자 그대로 있는 것.
> `[도표]` = 그림을 실제로 열어 눈으로 읽은 것 (판독 오차를 같이 적는다).
> `[재현]`/`[해석]` = 이 위키가 원문의 값으로 **계산하거나 추론한 것** — 원문에 없다.
>
> ★ **크로핑한 그림 9 장(Fig. 1–8 + Fig. A.1)을 전부 열어 보았다.**
> Fig. A.1 은 `wiki/tools/extract_figures.py` 가 **통째로 빠뜨려서**(06번에서 물린
> 것과 같은 실패) 10 쪽 이미지 bbox 를 직접 잘라
> `fig_a1_manual.png` 로 따로 저장했다. Table 1–3 은 PDF 텍스트가 정확해서
> 이미지로 읽지 않았다.

---

# 0. 원문에 없어서 확인이 필요한 것 (먼저 적는다)

| # | 공백 | 왜 걸리는가 |
|---|---|---|
| **G1** | **`U_ocp^p`·`U_ocp^n` 의 출처가 없다.** Table 1 은 `[인쇄]` "obtained by interpolating the positive and negative chemical equivalents θp and θn" 이라고만 쓴다. 어느 반쪽전지 자료인지, 액체셀인지 고체셀인지, 율은 얼마인지 **한 줄도 없다.** | **우리 α·β 재구성의 입력이 바로 이 두 곡선이다.** 이게 없으면 이 논문의 모든 수치가 옮겨지지 않는다 |
| **G2** | **Table 3 에 provenance 열이 없다.** 30 개 파라미터 중 무엇이 **측정**이고 무엇이 **PSO 적합**인지 구분이 없다. 본문은 `[인쇄]` "The PSO method was used for obtaining the model parameters" 라고만 적는다 | 자유 파라미터 개수를 셀 수 없다 = 식별 가능성 논의가 원천적으로 불가능 |
| **G3** | **6 개 파라미터 값이 비공개다** — `[인쇄]` `cp0, cn0, kp, kn, Dp, Dp_se` "these values are not disclosed in this paper" | **`cp0`·`cn0` 는 리튬 재고(LLI) 좌표다.** 그것을 비공개로 얼리고 "LLI 없음" 을 결론한다 (→ D3) |
| **G4** | **PSO 설정 전무** — 목적함수 식, 탐색 경계, 개체수, 반복수, 초기값, 시드, 종료 조건, 재시작 **하나도 없다** (`objective function`·`bounds`·`initial guess`·`iteration`·`population` 전수 0 회) | 재현 불가 + 다중 최적해 여부를 논할 근거가 없다 |
| **G5** | **`ε_se` 를 노화 중 갱신하는지 안 하는지 안 적혀 있다.** Fresh 에서 `ε_p + ε_se = 0.321 + 0.679 = 1.000` (정확히) | 어느 쪽이어도 모순이 나온다 (→ D2). `κ_eff = κ_se·ε_se^brug` 가 여기 달려 있다 |
| **G6** | **전압 창이 본문에 없다.** `[도표]` Fig. 3 의 충전이 4.3 V 까지, Fig. 7a/8a 의 방전이 2.0 V 까지 — **그림 축에서만 읽힌다.** ⚠ SI 체크리스트는 "Voltage (or potential) range" 에 **✓** 를 찍었다 | 컷오프는 이 계보의 `Q_apparent` 를 정하는 1 차 좌표다 |
| **G7** | **RPT 주기가 안 적혀 있다.** `[도표]` Fig. 7b 의 식별 사이클 ≈0/20/40/52/64/75/85/95/104/114/125, Fig. 8b ≈0/16/32/48/64/80/92/104/116/128/140 → **간격이 12~20 으로 불균일** | 열화 곡선의 모양(곡률) 판정이 표본 위치에 의존한다 |
| **G8** | **HPPC 를 매 RPT 마다 재고 한 번도 보고하지 않는다** (`[도표]` Fig. 2 흐름도에 2 회 등장). **EIS 도 100/50/0 % SOC 셋을 재고 100 % 만 쓴다** (`[인쇄]` "the EIS data measured at full charge was selected") | **동역학을 용량과 따로 묶을 유일한 채널을 수집해 놓고 버렸다.** §4 의 `A_eff·ε_p/R_s` 곱 축퇴를 깰 수 있었던 자료다 |
| **G9** | **셀이 2 개뿐이고 반복이 0 이다.** `n =`·`error bar`·`standard deviation`·`replicate`·`uncertaint*` **본문 11 쪽 + SI 전수 0 회** | `k_LAM` 의 셀 간 산포가 **2.15 배**인데(→ §8) 모집단이 2 다 |
| **G10** | **음극 명칭이 논문 안에서 둘이다** — 셀 이름과 Eq. (1) 은 **Li4.4Si**, §3.1 조립 절차는 **Li3.75Si** | Li:Si 가 17 % 다른 상이다. `θn` 의 분모(`cn_max`)가 어느 쪽 기준인지 정해지지 않는다 |
| **G11** | **Fig. 6 의 압력 축 단위가 `Kg` 다** (`[도표]`). 논문 전체에 `MPa`·`kPa` **0 회**. 센서 교정·수압면적·프레임 예압 여부 **없음** | 압력을 이 계보의 다른 편(2–490 MPa)과 비교하려면 우리가 환산해야 한다 (→ §9 Fig. 6) |
| **G12** | **Fig. A.1(a) 반쪽전지의 측정 조건이 없다** — 율·전해질(액체/고체)·온도·전압창 전부 없음. x 축이 **SOC/%** 인데 그 SOC 의 정의도 없다 | 이 논문의 **유일한 전극 분해 관측**인데 완전지와 겹쳐 볼 수 없다 (→ D5) |

---

# 1. 서지 · TYPE · **SI 의 정체**

★★★ **SI 는 파라미터 표가 아니다. *Journal of Power Sources* 의 투고 체크리스트다.**

`.docx` 를 `zipfile` 로 열어 `word/document.xml` 의 태그를 벗겨 전수 읽었다
(119 줄, `<w:tbl>` 2 개). 내용은 Table 1 "Information Checklist" ·
Table 2 "Performance Reporting" · NA 사유 5 문장 · 참고문헌 2 편.
**보충 그림 0 · 보충 표(데이터) 0 · 보충 수치 0.**

그럼에도 **SI 에만 있는 것이 다섯 개** 있고, 그중 셋은 본문의 결론을 직접 건드린다.

| SI 항목 | `[인쇄]` 값 | 왜 중요한가 |
|---|---|---|
| Cell type | **Other** (Coin 아님 · Pouch 아님) | 10 mm 몰드형 가압 셀 |
| Cell configuration | **2-electrode** (3-electrode **미체크**) | **참조극 없음** → 전극 분해 관측 0 (Q2) |
| Mass loading | **>8 mg cm⁻²** | `[재현]` 15 mg × 56 % ÷ 0.7854 cm² = **10.7 mg cm⁻²** ✓ 자기 일관 |
| Number of cycles at ≤1C (Full cell) | **50–200** | `[도표]` Fig. 7b/8b 의 125 / 140 사이클과 일치 |
| Number of cycles at >1C | **전부 미체크** | 1C 단일 조건 확인 |

그리고 **NA 사유 다섯 문장이 이 논문의 자백이다** (전문, `[인쇄]`):

> "The request for **Composition of the electrodes including supplier and purity**
> … is not presented … because the batteries used in this paper were prepared in-house;
>
> The request for **Ratio of N/P capacities**, is not presented … because the negative
> electrode … **was overloaded in order to fully utilize the capacity potential of the
> positive electrode**;
>
> The request for **Initial electrochemical profile**, is not presented … because the
> data … is the data of the state of the battery **stabilized after running for a
> certain number of cycles**;
>
> The request for **Coulombic efficiency associated with cycling data**, is not
> presented … because **these data are not involved in our analysis and modeling**."

★★★ 세 번째와 네 번째가 결정적이다.

- **N/P 를 숫자로 안 준다.** 그런데 본문의 열화 모드 판정 전체가 "음극이 과적재라
  음극 손실은 영향이 없다" 라는 **단 하나의 정성 논거**에 걸려 있다
  (`[인쇄]` §4.1.1 · §5). **그 논거의 크기를 논문이 보고하지 않는다.**
  → `[재현]` **그런데 Table 3 에서 계산된다** (§3.4): 모델 자신의 N/P ≈ **3.1**.
- **쿨롱 효율을 "우리 분석과 모델링에 쓰이지 않는다" 며 안 준다.** `LLI` 를 세는
  유일한 전하 수지 채널이 CE 다. **"LLI 가 거의 없다" 를 결론하면서 LLI 를 재는
  관측을 의도적으로 버린다.** (6·7호에서 이 위키가 겪은 것과 같은 자리 —
  [[anode-free-li-inventory-accounting]].)

---

# 2. 셀 · 제작 · 실험 (§3, `[인쇄]`)

## 2.1 복합양극

- 조성 **56 % 단결정 NCM811 (H₃BO₃ 표면 코팅) : 40 % Li₆PS₅Cl : 4 % 도전탄소(VGCF)**
  ★ 이 계보 최초의 **붕산(H₃BO₃) 코팅**이다 (1–8호는 LiNbO₃·Li₂ZrO₃·LZO 계열).
- 볼밀 2 단: ① AM 280 mg + SE 200 mg + 비드 1500 mg (1:3 wt) **4 h**,
  자전 정회전 30 min ↔ 역회전 30 min, 사이 휴지 5 min, 공전 동시.
  ② 도전탄소 20 mg 추가 후 같은 조건 **4 h**.
  `[재현]` 280:200:20 = **56 : 40 : 4** ✓ 본문 조성과 일치.
- **볼밀 총 8 h.** ⚠ 논문은 이 공정이 NCM 단결정을 깨는지 검토하지 않는다.

## 2.2 조립 (아르곤 글러브박스)

`[인쇄]` SE **90–100 mg** → **10 mm 직경** 가압 몰드에 수동 정제기로 시트 성형
→ 복합양극 **≈15 mg** + Al 박 합착 → 반대면에 **≈12 mg Li3.75Si** 시트 + Cu 박.
조립 후 **구조 지지 프레임**에 넣어 운전 중 압력 유지.

★ **성형 압력값이 논문 어디에도 없다** (`MPa` 0 회). 1–8호 전부가 제작 압력을
숫자로 줬던 것(100/300/370/400/490 MPa)과 대비된다.

## 2.3 시험 (`[인쇄]` + `[도표]` Fig. 2)

흐름: **Battery assembly → Pre-cycle → SCT → EIS → HPPC →
[Cycle aging → SCT → HPPC] 반복 → EIS → SEM**

- Pre-cycle(화성): **0.1C CC 충·방전 3 사이클**.
  `[인쇄]` 목적 = "stabilize the internal state … and **pressure changes due to the
  relaxation of battery components and plastic deformation of materials**" [31].
- 용량 교정: **1C CC 충·방전 3 사이클**, 충↔방 사이 **1 h 휴지**, **3 회 방전 용량의
  평균**을 기준 용량으로.
- EIS: **2 h 휴지 후 100 / 50 / 0 % SOC** 세 점. (⚠ 100 % 만 보고 — G8)
- 노화: **1C CC 충전 + 1C CC 방전 (~135 mA/g)**, 온도 `[인쇄]` Table 3 `T = 301.15 K`
  (= **28.0 °C**), `[도표]` Fig. 2 사진에 항온조.
- RPT: **SCT**(1C CC 충·방, 사이 1 h 휴지) + **HPPC**.
- 종료 후 EIS 재측정 → **해체 → SEM**, 신품 셀 별도 제작·해체·촬영.

## 2.4 ★ **셀이 둘뿐이고, 둘은 "다른 조건" 이 아니라 "다른 종료점" 이다**

`[인쇄]` "Due to the **scarcity of experimental equipment**, in order to save
experimental period and ensure sufficient experimental data at the same time,
there are two batteries named **Battery A and Battery B**, for the condition which
are aged to **80 % and 90 %** of their initial capacity, respectively."

`[해석]` **같은 프로토콜의 두 셀을 서로 다른 지점에서 멈춘 것**이다. 즉 B 는 A 의
부분집합이어야 한다 — 그런데 `[도표]` **A 는 125 사이클에 77 %, B 는 140 사이클에
90 %** 다. `[재현]` 열화율 **A 0.184 %/cycle · B 0.070 %/cycle → 2.6 배 차이**
(동일 조건 · 동일 설계 · 동일 시료 배치). 논문은 이 사실을 §4.2 에서
`[인쇄]` "this parameter would be **slightly** different from battery to battery"
한 구절로 처리한다.

---

# 3. 모델 (§2 · Table 1 · Table 3) — **구조를 먼저 적는다**

## 3.1 무엇을 푸는가

`[도표]` Fig. 1 과 Table 1 을 합치면:

```
좌표    −Ln ≤ x ≤ 0 : 음극(Li-Si 합금, 1-D 평판, 입자 없음)
          0 ≤ x ≤ Lse : 고체전해질(분리막)
        Lse ≤ x ≤ Lse+Lp : 복합양극(구형 NCM 입자 + SE 연속상 + 탄소)
           0 ≤ r ≤ Rs : 양극 입자 내부
```

지배식 (Table 1, `[인쇄]`):

| 축 | 식 |
|---|---|
| 양극 고체 | `∂cp/∂t = (Dp/r²)·∂/∂r(r²·∂cp/∂r)`, BC `Dp·∂cp/∂r|_{Rs} = −I/(a_{s,p}·A·Lp·F)` |
| 음극 고체 | `∂cn/∂t = Dn·∂²cn/∂x²`, BC `Dn·∂cn/∂x|_0 = I/(A·F)` (**2-D 접촉 가정**) |
| 전해질 | 분리막 `∂c_se/∂t = Dse·∂²c_se/∂x²`; 양극 내 `ε_se·∂c_se/∂t = D^p_se·∂²c_se/∂x² + (1−t⁰₊)(I−I^p_dl)/(F·A·Lp)` |
| 전해질 전위 | `κ_eff·∂²φ_se/∂x² + κ_eff_d·∂²ln c_se/∂x² + a_s·j_Li = 0`, `κ_eff = κ_se·ε_se^brug` |
| 계면 | Butler–Volmer, **`j^p_ct = (I − I^p_dl)/(A^p_eff · a_{s,p} · A · Lp)`** |
| 단자 | `U_bat = U^p_ocp − U^n_ocp + η^p_ct + η_se + η^n_ct + η_dc`, `η_dc = R_dc·I` |
| 기하 | **`a_{s,p} = 3·ε_p / Rs`** |

`[인쇄]` 해법은 Laplace 변환 → 전달함수, 상세는 자기 선행논문 [27]
(Li, Fan, Zhang et al., *eTransportation* **20** (2024) 100315) 에 위임.
**이 논문 안에 수치 해법·격자·시간 적분에 관한 서술은 없다.**

## 3.2 ★★★ **모델의 접촉 손실 좌표는 `A_eff` 이고, 그것이 이 계보에 처음 나온다**

`[인쇄]` Table 3:

| 기호 | 설명 | 값 |
|---|---|---|
| `A^p_eff` | **Effective contact area ratio of positive active material to electrolyte** | **0.4938** |
| `A^n_eff` | Effective contact area ratio of the negative electrode to electrolyte | **0.4095** |

★ **이것이 `assb` 1–8호를 통틀어 "양극 접촉 면적 분율" 이라는 이름과 무차원 값을
동시에 가진 첫 숫자다** (Q1). 4호 Shi 2020 의 10.4 % 는 **실측 면적분율**이지
모델 파라미터가 아니었고, 1·2호의 `θ` 는 **부피**분율이었다.

⚠ **그러나 세 가지가 이 숫자를 쓸 수 없게 만든다** — §4 와 §9(Fig. 5) 에서 전개한다:
(a) **적합값이지 측정값이 아니다**, (b) **노화 중 고정된다** → `θ(N)` 이 안 나온다,
(c) **`ε_p`·`R_s` 와 곱으로만 데이터에 들어간다** → 값이 유일하지 않다.

## 3.3 Table 3 자기 일관성 검사 (`[재현]`)

원문이 하지 않은 검산을 했다. **세 개는 맞고 세 개는 안 맞는다.**

| 검사 | 식 | 결과 |
|---|---|---|
| ✅ 비표면적 | `a_{s,p} = 3ε_p/Rs = 3×0.321/9.466e−6` | **1.0173e5 m⁻¹** ↔ 인쇄 **1.017e5** ✓ |
| ✅ 유효 전도도 | `κ_eff = κ_se·ε_se^brug = 0.3985 × 0.679^3.67` | **0.0963 S/m** ↔ 인쇄 **0.0962** ✓ |
| ✅ 1C 전류 | 8.4 mg AM × 135 mA/g | **1.134 mA** ↔ 인쇄 `Q = 1.128e−3 Ah` ✓ |
| ⚠ 체적 폐합 | `ε_p + ε_se = 0.321 + 0.679` | **= 1.000 정확** → **공극률 0 가정**, 탄소(≈4 wt%)가 `ε_se` 안에 흡수됨 |
| ⚠ 이론 용량 | `ε_p·A·Lp·c^p_max·F` = 0.321×7.854e−5×9.8e−5×2.741e4×96485 | **1.815 mAh** ↔ 실사용 1.128 mAh → **가용 분율 62.2 %** (`Δθ_p ≈ 0.62`) |
| ❌ 기하 `ε_p` | 15 mg·(56:40:4 wt%) 를 `A·Lp = 7.697e−3 cm³` 에 넣으면 | AM 부피 = 8.4 mg / 4.8 g cm⁻³ = 1.75e−3 cm³ → **`ε_p,기하` ≈ 0.227**, 잔여 **공극 ≈26 vol%** |

★★ 마지막 줄이 크다. `[해석]` **0.321 은 "공극률 0" 일 때의 값이다**
(`[재현]` 벌크 밀도 NCM811 4.8 · LPSCl 1.64 · VGCF 2.0 g cm⁻³ 로 56:40:4 wt% 를
환산하면 AM 부피분율 = 11.67/(11.67+24.39+2.00) = **0.307**, 0.321 과 5 % 이내).
그런데 **자기 Lp = 98 µm 와 자기 로딩 15 mg 을 쓰면 고체가 전체의 74 % 밖에 안 채운다.**
→ **실제 AM 부피분율은 ≈0.23 이고 모델의 `ε_p` 는 그 1.4 배다.**
⚠ 이 계산은 **밀도 3 개를 가정한다** (논문은 밀도를 주지 않는다) 그리고 `Lp` 가
측정인지 적합인지도 모른다 (G2). 방향만 취한다: **`ε_p` 는 기하량이 아니라
공극을 `ε_se` 에 밀어 넣은 유효량이다.**

## 3.4 ★ **N/P 를 논문 대신 계산한다** (`[재현]`)

SI 가 `[인쇄]` "not presented … because the negative electrode … was overloaded"
라고 거절한 값이 Table 3 에서 나온다.

```
음극 용량 = c^n_max · (A · Ln) · F
          = 1.065e4 mol/m³ × (7.854e-5 × 1.58e-4) m³ × 96485 C/mol
          = 1.065e4 × 1.2410e-8 × 96485 = 12.75 C = 3.543e-3 Ah = 3.54 mAh
양극(셀) 용량 = 1.128 mAh
⇒ 모델 N/P = 3.54 / 1.128 = 3.14
⇒ 사이클당 음극 화학량론 스윙 Δθn = 1/3.14 = 0.318 (= 음극 용량의 31.8 %)
```

★★★ **세 가지가 여기서 나온다.**

1. **"과적재" 는 무한대가 아니라 ≈3.1 배다.** 논문이 열화 모드 판정 전체를 걸어 둔
   논거의 크기가 처음으로 숫자가 됐다.
2. **음극은 매 사이클 자기 용량의 32 % 를 훑는다.** 그리고 모델은 `U^n_ocp` 를
   `θn` 의 **보간 함수**로 둔다 — 즉 **이 모델의 상대극은 평탄하지 않다.**
   → **이 카드의 "전고체에서는 음극 OCP 가 평탄해서 5 → 3 파라미터로 붕괴한다"**
   (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1, [[fitting-degeneracy]] 말미)
   **가 이 셀에는 적용되지 않는다.** Li-In·Li 금속·무음극이 아니라 **Li-Si 합금**이기
   때문이다. 9호는 이 계보 최초의 **합금(비평탄) 상대극** 셀이다.
3. ⚠ **단 `c^n_max` 가 적합값일 수 있다** (G2). `[재현]` Li3.75Si 완전 리튬화의
   Li 농도는 ≈8.2e4 mol/m³ 이므로 표의 1.065e4 는 그 **13 %** 다. 따라서 위 N/P 는
   **셀의 N/P 가 아니라 모델의 N/P** 다. 그 구별을 논문이 하지 않는다.

---

# 4. ★★★ 질문 1 — **식별 절차의 정체**

과제가 물은 다섯 가지 중 첫째. 원문(§4.2)을 그대로 분해한다.

## 4.1 절차 (`[인쇄]`, 2 단계)

> **1 단계 (신품)**: "Firstly, we established the electrochemical model of the fresh
> battery … The PSO method was used for obtaining the model parameters, and details
> about the implementation approaches can be found in our previous articles [27].
> The parameter values for the electrochemical model of the fresh battery are shown
> in Table 3."
>
> **2 단계 (노화)**: "Next, **the volume fraction of active material in the cathode
> was considered as a variable** at different aging stages. Using the **extracted SCT
> discharge data** at different aging stages, we obtained the parameter value through
> parameter identification by PSO [44], thereby quantifying the loss of positive
> active material."

## 4.2 그래서 답은 이렇다

| 물음 | 답 | 근거 |
|---|---|---|
| **무엇을 무엇으로 맞췄나** | **SCT 1C 방전 전압곡선** (V–Q) 을 모델 단자전압에 | `[인쇄]` "extracted SCT discharge data" · `[도표]` Fig. 7a/8a |
| **자유 파라미터 개수 (노화 단계)** | **정확히 1 개 — `ε_p`** | `[인쇄]` "the volume fraction … was considered as a variable" (단수) |
| **자유 파라미터 개수 (신품)** | **알 수 없다** (G2) — 최소 6 개는 확실(G3), 최대 Table 3 의 30 개 | provenance 열 없음 |
| **목적함수** | **식이 없다.** 보고 지표가 RMSE(mV) 이므로 전압 잔차 L² 로 **추정**되지만 인쇄되지 않았다 | `objective function`·`cost function` **0 회** |
| **최적화 알고리즘** | **PSO** (Particle Swarm Optimization), ref [44] = Rahman, Anwar, Izadian, *JPS* **307** (2016) 86 | `[인쇄]` |
| **초기값·경계** | **없다** | `initial guess`·`bounds`·`search range`·`upper and lower` **0 회** |
| **개체수·반복수·시드·종료조건** | **없다** | `population`·`iteration` **0 회** |
| **다중 시작 / 재시작** | **없다** | `multi-start`·`multistart`·`restart` **0 회** |
| **쓴 데이터** | **1C 방전 V–Q 만.** dV/dQ 는 **쓰지 않는다** (Appendix A 의 DVA 는 적합에 안 들어간다) · IC 도 안 쓴다 · EIS 도 안 쓴다 · **HPPC 는 재고 버렸다**(G8) | `[인쇄]` §4.2 + `[도표]` Fig. 2 |
| **율** | **1C 한 점** | `[인쇄]` §3.2 |
| **온도** | **301.15 K 한 점** | `[인쇄]` Table 3 |

## 4.3 ★★★★ **그리고 `ε_p` 는 데이터에 혼자 들어가지 않는다** (`[해석]`, 계산은 이 위키)

Table 1 의 **인쇄된 식만으로** 다음이 나온다.

```
BV 분모:      j^p_ct = (I − I^p_dl) / (A^p_eff · a_{s,p} · A · Lp)
              a_{s,p} = 3·ε_p / Rs
   ⇒ 과전압 η^p_ct 가 보는 것은  ★ A^p_eff · ε_p / Rs  한 조합뿐이다 ★

고체확산 BC:  Dp·∂cp/∂r|_{Rs} = −I / (a_{s,p}·A·Lp·F)      (A_eff 없음)
   ⇒ 표면 플럭스가 보는 것은  ε_p / Rs

전해질:       κ_eff = κ_se · ε_se^brug,  ε_se = 1 − ε_p (?)   (G5)

용량:         Q_max = ε_p · A · Lp · c^p_max · F · Δθ_p
   ⇒ 방전곡선 길이가 보는 것은  ε_p · c^p_max · Δθ_p
```

**즉 `ε_p` 를 `A^p_eff` 로부터 떼어내는 채널은 셋뿐이고, 압도적으로 강한 것은
"방전곡선 길이"(용량) 하나다.**

★ **결론 (`[해석]`)**: 이 절차에서 **식별되는 것은 사실상 `용량 ÷ 신품 용량` 이다.**
"positive active material 의 부피분율" 이라는 물리 이름은 **모델이 붙여 준 것**이지
데이터가 가른 것이 아니다. 접촉 손실이든, 균열에 의한 고립이든, 구조 열화든,
코팅 열화든 — **용량을 같은 만큼 줄이면 이 절차는 같은 `ε_p` 를 낸다.**

이것이 [[fitting-degeneracy]] 의 flat valley 를 **1 차원에서** 본 형태이고,
이 논문 전용 개념 페이지를 만든 이유다 → [[assb-lampe-contact-product-degeneracy]].

## 4.4 ★★ 그런데 그 `ε_p` → SOH 사상이 **선형이 아니다** (`[재현]`)

```
Battery A: Eq.(2) 로 125 사이클 →  Δε_p/ε_p = 0.0003667×125 / 0.321 = 14.28 %
           `[도표]` Fig. 7c 의 SOH  1.000 → ≈0.771          ⇒ ΔSOH = 22.9 %
           증폭 = 22.9 / 14.28 = ★ 1.60

Battery B: 0.0001707×140 / 0.321 = 7.44 %
           `[도표]` Fig. 8c 의 SOH  1.000 → ≈0.902          ⇒ ΔSOH = 9.8 %
           증폭 = 9.8 / 7.44 = ★ 1.32
```
(판독 오차 `[도표]` SOH ±0.005 → 증폭 ±0.04)

`[해석]` **`ε_p` 를 14 % 줄이면 모델은 용량을 23 % 줄인다.** 남는 8.6 %p 는
**활물질이 사라져서가 아니라 `a_{s,p} = 3ε_p/Rs` 가 같이 줄어 분극이 커지고
2.0 V 컷오프에 더 일찍 닿기 때문**이다 (1C 방전이다).

★★★ **따라서 논문이 "LAM_PE 가 주 기구" 라고 부르는 용량 감소의
`[재현]` 약 37 %(= 8.6/22.9)는, 모델 안에서조차 활물질 손실이 아니라 율 특성
저하다.** 그리고 두 셀의 증폭이 1.60 vs 1.32 로 다르다 — 상수가 아니라
동작점에 의존한다. **논문은 이 분해를 한 번도 하지 않는다.**

---

# 5. ★★★ 질문 2 — **유일성 증거가 있는가: 없다. 낱말 하나도 없다.**

본문 11 쪽 + SI **전수 카운트** (de-hyphenation 후, 대소문자 무시):

| 용어 | 본문 | SI |
|---|---:|---:|
| `uncertaint*` / `uncertain*` | **0** | **0** |
| `identifiab*` | **0** | **0** |
| `sensitiv*` | **0** | **0** |
| `confidence` / `confidence interval` | **0** | **0** |
| `Fisher` | **0** | **0** |
| `Cramér` / `Cram` | **0** | **0** |
| `condition number` | **0** | **0** |
| `posterior` | **0** | **0** |
| `bootstrap` | **0** | **0** |
| `Monte Carlo` | **0** | **0** |
| `covariance` | **0** | **0** |
| `correlat*` | **0** | **0** |
| `initial guess` | **0** | **0** |
| `multi-start` / `multistart` / `restart` | **0** | **0** |
| `error bar` / `standard deviation` / `replicate` | **0** | **0** |
| `degenerac*` / `non-unique` / `uniqueness` | **0** | **0** |
| `ill-posed` / `well-posed` / `regulariz*` | **0** | **0** |
| `bounds` (경계조건의 `boundary` 제외) | **0** | **0** |
| `objective function` / `cost function` | **0** | **0** |
| `cross-valid*` / `test set` / `extrapolat*` | **0** | **0** |
| `R²` / `R2` (적합 우수도) | **0** | **0** |
| — 참고: `RMSE` | 2 | 0 |
| — 참고: `PSO` | 4 | 0 |
| — 참고: `accura*` | 11 | 0 |

⚠ **방법론적 주의**: `MPa` 를 대소문자 무시로 세면 "co**mpa**red / co**mpa**rison"
때문에 10 이 나온다. **대소문자를 지키면 `MPa` = 0 회다.** 같은 이유로
`void` 4 회는 전부 "a**void**" 이고 `bound` 5 회는 전부 "**bound**ary" 다.
(07번의 µ 탈락과 같은 계열의 추출 함정 — 카운트는 전부 손으로 확인했다.)

★★ **그러므로 답은 단정형이다: 이 논문에는 유일성을 재는 장치가 하나도 없다.**
신뢰구간 없음 · 오차막대 없음 · 조건수 없음 · Fisher/CRB 없음 · 민감도 분석 없음 ·
profile likelihood 없음 · 다중 초기값 재시작 없음 · 후험 분포 없음 · 부트스트랩 없음.
**`assb` 9 / 9 편이 Q4 에서 0 이다.**

## 5.1 ★ 그러나 **축퇴의 지문은 이 논문이 인쇄한 표 안에 있다** (`[재현]`)

논문 Table 2(EIS 등가회로 적합 결과) 를 우리가 다시 집계했다.

| | A 신품 | A 노화 | Δ | | B 신품 | B 노화 | Δ |
|---|---:|---:|---:|---|---:|---:|---:|
| `R_b` / Ω | 12.44 | 15.52 | **+24.8 %** | | 13.68 | 29.24 | **+113.7 %** |
| `R_SEI` / Ω | 8.937 | 12.25 | **+37.1 %** | | 8.706 | **1.767** | ★ **−79.7 %** |
| `R_ct` / Ω | 78.66 | 95.5 | **+21.4 %** | | 81.67 | 91.97 | **+12.6 %** |
| **합계** | **100.04** | **123.27** | **+23.2 %** | | **104.06** | **122.98** | **+18.2 %** |

★★★ **합계는 두 셀에서 같은 방향으로 비슷하게 움직이고(+23 % / +18 %),
분해는 전혀 맞지 않는다** — `R_b` 가 +25 % vs +114 %, `R_SEI` 가 **+37 % vs −80 %**.
**같은 화학 · 같은 공정 · 같은 프로토콜의 두 셀이다.**

그리고 `[도표]` Fig. 4b·4c 를 실제로 보면 **분해 가능한 원호가 하나뿐**인데
등가회로는 `R_b` + (`R_SEI`∥CPE) + (`R_ct`∥CPE) + `W` 로 **두 개의 RC 계열 + Warburg**
를 뽑는다. `[해석]` **하나의 병합 원호에서 두 시상수를 뽑고 있고, 그 분할이 셀에
따라 부호까지 바뀐다.**

**논문은 이것을 축퇴라고 부르지 않는다.** `[인쇄]`:

> "As for the R_SEI, Battery A is increasing, Battery B is decreasing, **which is
> unexpected**. Considering that the R_SEI of the ASSBs in this paper is too small
> and research on the growth of SEI for ASSBs is still developing [38], the
> inconsistency in R_SEI changes is probably because **the limitations of the
> measurement equipment's accuracy, the error introduced by the fitting process,
> or the influence of the battery's thermal equilibrium state**."

`[해석]` 세 후보 중 **두 번째("the error introduced by the fitting process")가
정답에 가장 가깝다 — 그리고 논문은 그것을 장비 오차와 나란히 놓고 지나간다.**
**식별 불가능한 분해를 "예상 밖" 이라 부르고 원인 목록의 가운데에 묻는 것** —
이것이 이 계보에서 Q4 가 비어 있는 방식의 9번째 변주다.
⚠ **공정하게**: 두 셀은 **다른 노화 수준**(A 77 % · B 90 %)에서 측정됐으므로
합계 변화율의 유사성은 강하게 주장하지 않는다. **부호가 반대인 것만이 모호하지 않다.**

## 5.2 ★★★ 그리고 **저자들이 자기 산포를 보고 숨겼다** (`[인쇄]` 전문)

> "The values of certain parameters, such as `cp0`, `cn0`, `kp`, `kn`, `Dp` and
> `Dp_se`, **exhibit significant variations** (as demonstrated in Figs. 3 and 4),
> likely due to the hand-assembled nature of the batteries. **To avoid potential
> misinterpretation, these values are not disclosed in this paper.** While such
> variations are expected in manual assembly processes, **the robustness of the
> overall model and its predictive capabilities remain unaffected, as confirmed by
> our experimental results.** Further refinement and standardization of the assembly
> process may reduce these variations in future work."

★★★ **이 한 문단이 이 논문에서 우리 프로젝트에 가장 중요하다.**

1. **적합 파라미터의 셀 간 산포를 관측했다** ("significant variations").
2. **그 산포를 지면에서 제거했다** ("not disclosed").
3. **제거의 정당화가 적합도다** ("robustness … remain unaffected, as confirmed by
   our experimental results").

→ `[해석]` **"적합이 잘 되니 파라미터가 흔들려도 괜찮다" 는 명제가 문자 그대로
인쇄되어 있다.** [[fitting-degeneracy]] 와 `degradation-degeneracy/` 가 측정으로
반박한 바로 그 명제다. 그리고 감춰진 6 개 중 **`cp0`·`cn0` 는 리튬 재고 좌표**이므로,
**LLI 를 정하는 두 수를 비공개로 얼려 놓고 "LLI 없음" 을 결론한다** (→ D3).

⚠ 부수 어긋남: "(as demonstrated in **Figs. 3 and 4**)" — Fig. 3 은 IC 곡선,
Fig. 4 는 EIS 다. **두 그림 어디에도 파라미터 값이 없다.** 셀 간 차이가 보인다는
뜻으로 읽을 수는 있으나, 산포의 크기를 독자가 확인할 방법은 없다.

---

# 6. ★★★ 질문 3 — **"주 기구" 판정이 어떻게 나왔는가**

## 6.1 판정의 실제 구조

`[인쇄]` 초록/하이라이트: "**The loss of positive active material is identified as
the main aging mechanism.**"
`[인쇄]` 결론(§5): "we find that the loss of positive active material is **likely**
the main cause of battery aging **considering the overloading of the anode material**"

★ **하이라이트는 단정형("is identified"), 결론은 조건부 추정형("is likely …
considering the overloading")이다.** 같은 주장이 앞뒤에서 강도가 다르다.

논거 사슬 (`[인쇄]` §4.1 전체):

```
(1) ICA — 세 봉우리가 "비슷한 크기로" 낮아짐 ⇒ LAM_PE, "minimal or no LLI"
(2) ICA — 봉우리 위치 불변                  ⇒ 저항 증가 없음
(3) EIS — R_b 증가가 작음(3.08 / 15.56 Ω)   ⇒ (2) 와 일치
(4) SEM — 단결정 NCM 입자는 안 깨짐, 대신 황화물 전해질이 균열
(5) 압력 — 충전 시 상승·방전 시 하강 ⇒ 주기 응력 ⇒ 피로 균열 (문헌 [42,43])
(6) 음극은 과적재 ⇒ 음극 손실 "영향 없음"
(A.1) DVA — 완전지에 NCM811 봉우리만 보임 ⇒ 양극이 주범
```

## 6.2 ★★★★ **여러 모드를 같이 놓고 지분을 비교한 적이 없다**

과제가 물은 핵심. 답:

> **없다. 열화 모드는 단 한 번도 자유 파라미터가 아니었다.**

- `LLI` 는 모델에 **좌표가 없다.** `cp0`·`cn0` 가 그 역할을 하지만 신품에서 한 번
  적합된 뒤 **노화 전 구간에서 고정**이고, 값은 **비공개**다 (G3).
- `LAM_NE` 는 모델에 **좌표가 없다.** `ε_n` 이라는 파라미터 자체가 없다
  (음극은 평판이고 부피분율을 쓰지 않는다).
- **`ε_p` 하나만 푼다.** 따라서 **잔차는 전부 `ε_p` 로 간다** — 다른 갈 곳이 없다.

`[해석]` **이것은 "단독 모드 스윕으로 분리 가능을 주장" 하는 것보다 한 단계 더
약하다. 스윕조차 없다.** 지분은 **적합 전에 설계로 정해졌고**, 적합은 그 설계
안에서 크기만 정했다.

## 6.3 ★★★ **다른 조합으로 같은 적합도가 나오는지 확인했는가: 안 했다.
그리고 확인할 수 없게 되어 있다.**

- 대안 모델 비교 **0 건** (LLI 를 켠 판본, `A_eff` 를 푸는 판본, 둘 다 푸는 판본 —
  전부 없다).
- §4.3 이 보인 `A^p_eff · ε_p / Rs` 곱 축퇴 때문에, **`A_eff` 를 같이 풀었다면
  `ε_p` 는 데이터가 아니라 초기값이 정했을 것이다.**
- 그리고 **그 곱을 가를 수 있었던 데이터(HPPC · 다중 SOC EIS)를 수집해 놓고
  보고하지 않는다** (G8).

## 6.4 ★★★★ **DVA 논거는 구조적으로 실패할 수 없는 시험이다**

부록 A 전문 (`[인쇄]`):

> "To further illustrate that it is reasonable to attribute the main aging of this
> ASSB to the loss of active material in the composite cathode, differential voltage
> analysis (DVA) of the battery is provided … By comparing the dV/dQ curves on the
> half-cell (Fig. A.1(a)) and the full-cells (Fig. A.1(b) and (c)), **the dV/dQ curves
> of the full-cells display only the characteristic peaks corresponding to NMC811**,
> from the beginning to the end of life for both Battery A and Battery B, which
> further indicates that **the aging of this type ASSB is mainly caused by the cathode**."

DVA 의 존재 이유는 **음극 특징점을 보는 것**이다. 그런데 §4.1.1 이 이미 인쇄한다:

> `[인쇄]` "Considering that the previously mentioned anode material is **overloaded**,
> it is reasonable that **the anode peak is not obvious** and the loss of negative
> material has no effect."

★★★ `[해석]` **음극 봉우리가 안 보이는 것은 노화의 결과가 아니라 셀 설계의
귀결이다.** 과적재 음극은 **음극이 어떻게 열화하든** 완전지 dV/dQ 에 봉우리를 안
남긴다. 따라서 "NCM811 봉우리만 보인다 ⇒ 양극이 주범" 은 **어떤 실험 결과가
나와도 같은 결론을 내는 시험**이다. 논문은 이것을 "further indicates" 라고 부른다.

→ 우리 어휘로: **관측을 고른 방식이 한쪽 가설을 반증 불가능하게 만들었다.**
이 계보에서 Q2(독립 관측)가 비어 있는 방식 중 가장 날카로운 형태다.

## 6.5 ⚠ 그리고 ICA 는 자기 한계를 인쇄하고 결론을 낸다

`[인쇄]` "It must be acknowledged that **more subtle details may be obtained using
micro-current (e.g., 1/20C) charging or discharging curves**. However, considering
the experimental period and the fact that **the ICA in this paper is only a
qualitative analysis**, 1C constant current charging curves were used."

★ `[해석]` **모드 진단이 되게 만들 수 있었던 유일한 조치(저율)를 일정 사유로
포기하고, 그 위에서 "LLI 없음 · 저항 증가 없음" 이라는 정량적 성격의 결론 둘을
낸다.** 1C IC 봉우리 높이는 열역학과 동역학이 섞인 양이다.
→ `[도표]` 실제로 세 봉우리의 감소율이 같지 않다 (→ D1).

---

# 7. ★★★ 질문 4 — **독립 관측이 있는가**

| 채널 | 있나 | 무엇을 주나 | 한계 |
|---|---|---|---|
| **SEM (해체 후 표면)** | ★ **있다** | `[도표]` 황화물 전해질의 균열, 단결정 NCM 입자의 파쇄 **없음** | **정성 전용.** 균열 길이·밀도·면적분율 **0**. 단면 아님(표면만). 노화 1 셀 + 신품 1 셀 |
| **EIS (완전지 2-전극)** | ★ 있다 | Table 2 의 `R_b`/`R_SEI`/`R_ct` | **분해가 셀 간 부호까지 어긋난다** (§5.1). 참조극 없음 → 전극 귀속은 명목뿐 |
| **압력 센서 (in operando)** | ★★ **있다** | `[도표]` Fig. 6 의 12 사이클 힘 시계열 | **단위가 `Kg`**, MPa 환산 없음, 교정 없음, 노화 전 구간 추세 없음 |
| **ICA / DVA** | 있다 | 정성 | **적합 밖의 관측이 아니다** — 같은 V–Q 데이터의 미분이다 |
| XRD · XPS · TEM · ICP · 적정 | **없다** | — | `XPS`·`TEM`·`ICP`·`titration` **0 회**, `XRD` 1 회(남의 논문 인용) |
| **3-전극 / 참조극** | **없다** | — | SI 가 `[인쇄]` **2-electrode** 체크 |
| **노화 재료의 반쪽전지** | **없다** | — | Fig. A.1(a) 의 반쪽전지는 **신품 NCM811 기준선**이고 노화 셀이 아니다 |
| **해체 후 용량 측정 / 잔여 활물질 정량** | **없다** | — | Q1 을 깰 수 있었던 유일한 측정 |

★★★ **결론: `LAM_PE` 를 적합 밖에서 확인한 관측이 0 건이다.**
SEM 은 "균열이 있다" 를 보이지 `[인쇄]` "some NCM particles being unable to
repeatedly release lithium ions" 의 **양**을 재지 않는다. 논문 자신이 그 사슬을
가정법으로 쓴다: `[인쇄]` "This cracking primarily obstructed the Li⁺ transport
channels, **which may have led to** the inability of some … particles to properly
de-embed Li⁺, **potentially causing** the loss of positive active material."

→ **Q1(양극 접촉 손실 정량)은 9호에서도 0 이다.** `A^p_eff = 0.4938` 이라는
숫자가 새로 생겼지만 그것은 **적합값**이고, **노화 중 고정**이며, §9(Fig. 5)에서
보듯 **자기 SEM 과 9 배 어긋난다.**

## 7.1 ★ 그리고 SEM 대조 자체의 조건이 다르다 (`[도표]`, 이미지의 정보 띠)

| | (a) 노화 | (b) 신품 |
|---|---|---|
| 장비 | EMCRAFTS | EmCrafts |
| WD | **10.86 mm** | **9.94 mm** |
| HV | 20.00 kV | 20.00 kV |
| **Probe** | **2.00** | **13.00** |
| 배율 | ×15000 | ×15000 |
| 스케일바 | **0.8 µm** | **0.8 µm** |
| 촬영일 | **2024.2.29** | **2024.5.24** |

★ **Probe(전류) 설정이 6.5 배 다르고 촬영일이 ≈3 개월 떨어져 있다.**
`[해석]` 대비·표면 대전·2 차전자 수율이 달라지는 조건이며, "균열이 노화에서
생겼다" 는 이 논문의 유일한 형태학 논거가 그 대조 위에 서 있다. 논문은 언급하지 않는다.

---

# 8. ★★★ 질문 5 — **SOH 오차 1 % 의 정체: 보간이다. 그것도 훈련 잔차다.**

## 8.1 무엇이 무엇에 맞춰졌는지 (`[인쇄]` + `[도표]`)

```
(a) 각 노화 단계의 SCT 방전곡선  ──PSO──▶  ε_p(N)  [Fig. 7b/8b 의 파란 동그라미]
(b) 그 점들에 직선 적합           ──────▶  Eq.(2): ε_p = ε_p,fresh − k_LAM·N
(c) Eq.(2) 를 모델에 넣고 재실행  ──────▶  SOH-Sim  [Fig. 7c/8c 의 빨간 ×]
(d) "Error" = |SOH-Sim − SOH-Exp|, 같은 셀·같은 사이클
```

★★★ **(a)–(d) 가 전부 같은 셀의 같은 사이클 집합이다.**
**hold-out 셀 0 · hold-out 사이클 0 · 외삽 0 · 교차검증 0**
(`cross-valid*`·`test set`·`extrapolat*` **0 회**, `valid` 는 CRediT 의
"Validation" 1 회가 전부).

`[인쇄]` "its accuracy is **verified by comparing the simulation results with
experimental SOH data**" — 그 비교 대상이 학습에 쓴 바로 그 데이터다.

## 8.2 `k_LAM` 은 **셀마다 다시 적합된다** — 그리고 2.15 배 차이난다

| | `k_LAM` (1/cycle) | `[재현]` 상대율 `k_LAM/ε_p,fresh` | 종료 | `[도표]` RMSE |
|---|---:|---:|---|---:|
| Battery A | **3.667e−4** | **0.1142 %/cycle** | 125 cyc → SOH ≈0.771 | 24.2 mV |
| Battery B | **1.707e−4** | **0.0532 %/cycle** | 140 cyc → SOH ≈0.902 | 14.2 mV |
| **비** | **2.148 ×** | **2.148 ×** | | |

`[재현]` 두 값의 차이는 작은 쪽 기준 **+114.8 %**, 평균 기준 **±72.9 %**.
논문의 표현은 `[인쇄]` "**slightly** different from battery to battery".

★★★★ **그러므로 이 모델의 예측 오차는 1 % 가 아니다.**

```
보고된 것 :  같은 셀 안의 적합 잔차       평균 <1 % (A) · <0.5 % (B), 최대 <2 % (A)
보고 안 된 것: 셀이 바뀌었을 때의 오차     k_LAM 이 2.15 배 → 100 사이클에서
                                          SOH 예측이 ≈11 %p 어긋난다
                                          (`[재현]` 0.1142 % vs 0.0532 % × 100 cyc ≈ 11.4 %p)
```

`[해석]` **셀 간 파라미터 산포(115 %)가 보고된 적합 오차(1 %)보다 두 자릿수 크다.**
그리고 모집단은 **2** 다 (G9). **`k_LAM` 이 이 화학의 성질인지, 이 조립자의
성질인지, 이 셀의 성질인지 구별할 자료가 없다.**

## 8.3 08번(Su 2024) 패턴과의 대조 — **같지 않다. 더 단순하다.**

과제가 "평균을 상한처럼 말하고 대조군이 제안 방법을 이기는데 언급 안 함" 을
확인하라고 했다. **정직하게 대조한 결과**:

| Su 2024 패턴 | 9호에 있나 |
|---|---|
| 평균을 상한처럼 제시 | ⚠ **부분적으로만.** 하이라이트가 `[인쇄]` "The **average** error … is within 1 %" 로 **"average" 를 명시**한다. 본문도 A 의 최대를 `[인쇄]` "within 2 %" 로 밝힌다. `[도표]` Fig. 7c 실측 최대 ≈**1.45 %** — 두 진술 모두 참이다 |
| 셀별 오차표의 최악 셀을 안 밝힘 | ⚠ **표가 없다.** 셀별 오차는 `[도표]` Fig. 7c/8c 의 막대로만 있다. `[도표]` 최대: **A ≈1.45 %(사이클 40) · B ≈0.57 %(사이클 32)** |
| 대조군이 제안 방법을 이기는데 언급 안 함 | ❌ **대조군이 아예 없다.** 다른 방법과의 비교 0 건. 베이스라인 0 건 |
| 보고 비대칭 | ★ **있다**: A 는 평균+최대 둘 다, **B 는 평균만**(`[인쇄]` "within 0.5 %"). B 의 최대는 인쇄되지 않는다 |

★ `[해석]` **9호의 문제는 수사가 아니라 설계다.** 숫자 자체는 대체로 정직하게
적혀 있다. 문제는 **그 숫자가 예측 성능이 아니라는 것**, 그리고 **논문이 그 구별을
하지 않는다는 것**이다. 08번이 "평균을 상한처럼" 이었다면, 09번은
**"훈련 잔차를 검증 오차처럼"** 이다.

## 8.4 ⚠ 그리고 오차가 가장 큰 곳이 **초반**이다 (`[도표]` Fig. 7c)

`[도표]` Battery A 의 오차 막대 (오른쪽 축 0–0.05, 판독 ±0.001):

| cycle | 20 | 40 | 52 | 64 | 75 | 85 | 95 | 104 | 114 | 125 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Error | **0.0115** | **★0.0145** | 0.0075 | 0.0085 | 0.0090 | 0.0080 | 0.0035 | 0.0005 | 0.0022 | 0.0038 |

그리고 `[도표]` Fig. 7b 의 `ε_p` 점들은 **직선 위로 볼록**하다 — 초반 점들이
직선 위, 후반 점들이 직선 아래 (판독 ±0.001, 10 점 중 7 점이 부호 일관).
`[해석]` **실제 `ε_p(N)` 은 직선이 아니라 가속형이고**, Eq. (2) 의 직선이 그
곡률을 흡수하지 못해 **초반에 SOH 를 과소 예측한다**(사이클 20: Exp 0.982 vs
Sim 0.970). 논문은 `[인쇄]` "The `ε_p` exhibits a **linear** decreasing trend"
라고만 쓰고 **잔차·R²·적합 우수도를 보고하지 않는다**.

⚠ Battery B 는 반대 방향으로 보인다 (초반 아래 · 후반 위 = 감속형, `[도표]`
판독차 ±0.001 로 **경계선**이다). `[해석]` **두 셀의 곡률 부호가 다를 가능성이
있고**, 그렇다면 "선형" 은 두 셀 모두에 대해 **모양이 아니라 근사**다.
★ 그리고 이 논문에는 **그 모양을 결정할 반복이 없다** (G9).

---

# 9. 그림별 판독 — **9 장 전부 열어 보았다**

## Fig. 1 (p3) — 모델 구조 모식도 `[도표]`

좌→우: Cu 집전체 / **회색 균질 슬래브 음극**(입자 없음, `−Ln ≤ x ≤ 0`) /
**베이지 연속상 SE**(`0 ≤ x ≤ Lse`) / **복합양극**(초록 구 AM + 검정 점 탄소가
베이지 SE 에 박힘, `Lse ≤ x ≤ Lse+Lp`) / Al 집전체. 우측에 `Rs` 구형 좌표.
`c^n_dl`·`c^p_dl` 이 두 계면에 커패시터로 달림.

★★ **그림에 공극이 없다** — AM 과 탄소가 SE 를 빈틈없이 채운다.
`ε_p + ε_se = 1` 과 일치하고 §3.3 의 ≈26 vol% 공극 계산과 어긋난다.
★★★ **그리고 균열도, 접촉 손실도, 분리된 입자도 그려져 있지 않다.**
논문의 기구 서술(§4.1.3–4.1.4)의 주인공이 **모델 그림에 없다.**
`A_eff` 도 그림에 나타나지 않는다 (Table 3 의 숫자로만 존재한다).

## Fig. 2 (p4) — 실험 흐름 `[도표]`

블록: Battery assembly → Pre-cycle → SCT → EIS → HPPC → **Cycle aging** → SCT →
HPPC → EIS → SEM. Cycle aging↔HPPC 사이에 **되돌이 화살표**(RPT 루프).
사진 3 장: **볼트 4 개로 죄인 원통형 가압 프레임 + 계장 스터드**(노란 케이블) ·
채널 다수의 충방전기 랙 · **항온조**.

★ **HPPC 가 루프 안에 두 번 등장한다 — 논문 어디에도 HPPC 결과가 없다** (G8).

## Fig. 3 (p5) — IC 곡선 `[도표]` ★ 본문과 어긋난다

축: x = Voltage/V **3.3 → 4.3**, y = **dQdV/mAh/V** 0 → 1.65 (정규화 아님).
(a) Battery A · (b) Battery B, 각 **≈10 곡선** + "Aging" 하향 화살표.
봉우리 3 개: **≈3.65 V · ≈3.95 V · ≈4.17 V**.

`[도표]` 봉우리 높이 (판독 ±0.03):

| | 봉우리 1 (3.65 V) | 봉우리 2 (3.95 V) | 봉우리 3 (4.17 V) |
|---|---|---|---|
| **A** 신품→노화 | 1.62 → 1.17 (**−27.8 %**) | 1.30 → 1.02 (−21.5 %) | 1.38 → 1.10 (−20.3 %) |
| A 같은 구간 용량 변화 | | **−23 %** | |
| **B** 신품→노화 | 1.66 → 1.30 (**−21.7 %**) | — | 1.27 → 1.13 (**−11.0 %**) |
| B 같은 구간 용량 변화 | | **−10 %** | |

★★★ **→ D1**: `[인쇄]` "The degradation of the three peaks was of **approximately
the same magnitude**". `[도표]` **B 에서는 봉우리 1 이 용량 감소의 2.2 배, 봉우리 3 이
1.1 배로 준다** — 판독 오차(±2 %p)의 5 배 차이다.

★★ 그리고 `[도표]` **저전압 상승 엣지가 이동한다**: 신품(빨강)의 엣지가 노화
곡선들보다 **≈100 mV 오른쪽**에 있고 더 가파르다 (A·B 양쪽, 판독 ±30 mV).
`[인쇄]` "the position of each peak remained **almost unchanged**" 는 **봉우리**에
대해서는 맞지만, **엣지에는 해당하지 않는다.** 1C IC 이므로 이 이동은 열역학과
동역학이 섞인 양이고, 논문은 이 특징을 언급하지 않는다.

## Fig. 4 (p6) — EIS `[도표]` ★ 하나의 원호에서 둘을 뽑는다

(a) 등가회로: **`R_b` — (`R_SEI` ∥ CPE_SEI) — (`R_ct` ∥ CPE_ele) — `W`(Warburg 유한)**.
→ 자유 파라미터 **≥8 개**(R 3 + CPE 4 + W ≥1). **Table 2 는 그중 3 개만 보고한다.**
CPE 지수 `n`, 용량성 항, Warburg 계수 **전부 없음**.

(b) Battery A: Fresh(파랑) · Aged(주황). 둘 다 `Z_RE` ≈14–16 Ω 에서 출발,
**분해 가능한 원호 1 개**(정점 `Z_RE` ≈65–78, `−Z_IM` ≈25–30) → `Z_RE` ≈120 에서
골 `−Z_IM` ≈12 → 저주파 꼬리 상승.

(c) Battery B: Fresh 정점 `−Z_IM` ≈**42**, Aged 정점 ≈**28**.
★ **노화 원호가 신품보다 눈에 띄게 작다.** 그런데 Table 2 는 B 의 `R_ct` 가
81.67 → 91.97 로 **커졌다**고 적는다. `[해석]` 눌린 원호의 높이는 `R` 과 CPE 지수
`n` 둘 다에 걸리므로 원리적으로 양립 가능하지만, **`n` 이 보고되지 않아 확인할 수
없다.** → **D4**.

★★ **두 패널 어디에도 적합 곡선(모델 오버레이)이 없다.** 데이터만 그려져 있다.
**Table 2 의 숫자를 그림으로 검증할 방법이 없다.**

## Fig. 5 (p6) — SEM `[도표]` ★★★ **자기 파라미터표를 9 배로 배반한다**

(a) 노화: 초록 원 2 개 = NCM 입자, **주황 화살표 7 개 + "Crack" 라벨** = 황화물
전해질의 균열. (b) 신품: 균열 표시 없음, 밝은 다면체 입자들이 연속상에 박힘.
둘 다 ×15000, 스케일바 **0.8 µm** (µ 정상 표시 — 07번 함정 해당 없음).

★★★ **스케일바로 NCM 입자를 쟀다** (`[재현]`, 픽셀 계측):

```
스케일바 = 40 px (원본 2218×702 기준)  ⇒ 0.8 µm / 40 px = 50.0 px per µm
초록 원 ①  외곽 bbox 102 × 124 px, 선폭 ≈8 px ⇒ 입자 ≈94 × 116 px = 1.88 × 2.32 µm
초록 원 ②  외곽 bbox 131 ×  95 px             ⇒ 입자 ≈123 × 87 px = 2.46 × 1.74 µm
⇒ 등가 직경 ≈ 2.1 µm  ⇒ ★ 관측 반경 R_s,SEM ≈ 1.05 µm
```

**Table 3 의 `Rs` = 9.466e−6 m = 9.47 µm** (직경 18.9 µm).

★★★★ **비 = 9.47 / 1.05 ≈ 9.0 배.**
(단결정 NCM811 의 통상 크기 2–5 µm 와도 SEM 쪽이 일치한다.)

**결과가 두 가지로 갈리고 둘 다 논문의 주장을 깬다** (`[해석]`):

```
a_{s,p} = 3ε_p / Rs :  표의 Rs 로는 1.017e5 m⁻¹,  SEM 의 Rs 로는 9.17e5 m⁻¹ (9 배)
BV 가 보는 것은 A^p_eff · a_{s,p} :  표의 조합 = 0.4938 × 1.017e5 = 5.02e4 m⁻¹
   SEM 의 R_s 로 같은 곱을 맞추려면  A^p_eff = 5.02e4 / 9.17e5 = ★ 0.055 (5.5 %)
```

→ **"유효 접촉 면적비" 라는 이름의 수가 어느 반경을 쓰느냐에 따라
`0.055` 와 `0.494` 사이를 9 배로 움직인다.** 이것은 측정량이 아니라
**`A_eff · ε_p / Rs` 라는 곱의 임의 분해**다.

★★★ **그리고 이것이 논문의 §1.2 주장과 정면으로 부딪친다**:
`[인쇄]` "A coupled electrochemical-aging model for the ASSB is established,
**retaining the actual physical significance of the parameters**."

→ 전용 개념 페이지: [[assb-lampe-contact-product-degeneracy]].

⚠ **판독 한계**: 스케일바 길이는 픽셀 단위로 정확히 셌으나(40 px, 8 px 두께),
입자 경계는 **저자가 그린 초록 원**으로 잡았고 SEM 은 **표면 투영**이라 최대
단면이 아닐 수 있다. 그래도 9 배를 뒤집으려면 원이 실제 입자의 1/9 이어야 한다.

## Fig. 6 (p6) — 사이클 중 압력 `[도표]` ★★ 이 계보 최초의 **연속 힘 시계열**

축: x = **Cycle 0–12**, 좌 y = Voltage/V **1.9–4.4**(빨강), 우 y = **Pressure/Kg
294–300**(파랑).

`[도표]` 판독 (±0.2 kg):
- 전압: 충전 상한 ≈**4.3 V**(첨두 4.35 까지 오버슈트), 방전 하한 ≈**2.0 V**.
- 압력: **충전 중 상승 · 방전 중 하강** (논문의 설명 = Li-Si 음극이 리튬화하며 팽창).
- 고점 ≈**296.6 kg**, 저점 ≈**294.0 kg** → **스윙 ≈2.6 kg**.
- 12 사이클에 걸친 저점 드리프트 ≈**294.2 → 293.7 kg** (−0.5 kg).

★★★ `[재현]` **MPa 로 환산** (논문은 하지 않는다 — `MPa` 0 회):

```
가압 면적 = Table 3 의 A = 7.854e-5 m² (= 10 mm 직경 몰드, π·(5 mm)² ✓)
평균     295.3 kgf × 9.80665 = 2896 N  ⇒ P ≈ 36.9 MPa
스윙       2.6 kgf × 9.80665 =   25 N  ⇒ ΔP ≈ 0.32 MPa (평균의 ≈0.9 %)
12 사이클 드리프트 −0.5 kgf            ⇒ ≈ −0.06 MPa
```

★ **이 값이 이 카드의 Q6 에 붙는다**:
- 운전 압력 **≈37 MPa** → 4호 2 MPa · 5호 5–25 MPa · 6·7호 2–4 MPa 보다 **한 자릿수
  높고**, 5호의 **Li 금속 상한 75 MPa 의 절반**이며, 8호가 재인용한
  **산업 요구치 <≈1 MPa 의 ≈37 배**다 ([[assb-stack-pressure-operating-window]]).
- **주기적 변조 ΔP ≈0.32 MPa 자체가 그 산업 예산의 1/3 이다.**
⚠ **환산은 "kg 표시가 셀 스택에 걸린 축방향 힘" 이라는 가정에 달려 있다.**
논문은 센서 종류·교정·측정 위치·프레임 예압 중 아무것도 적지 않는다 (G11).
가정이 틀리면 이 세 줄은 전부 무효다.

★★ 그리고 `[해석]` **압력은 모델에 들어가지 않는다.** Table 1 에 역학 방정식이
없고, Table 3 에 응력·체적변화·압력 파라미터가 없다. Eq. (2) 는 `ε_p` 를
**사이클 수만의 함수**로 둔다. 즉 **"coupled electrochemical-aging model" 의
결합 변수는 물리 상태가 아니라 사이클 색인이다.**
논문 자신이 그 귀결을 인쇄한다:
`[인쇄]` "it only involves the aging conditions of 1C charging and 1C discharging,
all conducted at room temperature, which presents certain limitations."

★ 또 하나: `[도표]` 12 사이클 동안 **압력 포락선이 거의 변하지 않는다.**
피로 균열 서사는 **누적 손상**을 요구하는데, 보여 준 창은 **125–140 사이클 중 12** 이고
그 안에서 변화가 없다. 논문의 문장도 하나 건너 인용이다:
`[인쇄]` "Based on some existing studies of fatigue cracking …, **it is suggested
that** periodic pressure changes lead to cracking" (근거는 [42] Budiman 2022 ·
[43] Yadav 2022 — **둘 다 남의 논문**).
⚠ 그리고 `[도표]` **Fig. 6 이 어느 사이클 구간인지 표시가 없다**(x 축이 0–12).

## Fig. 7 (p9) — Battery A 모델 결과 `[도표]`

(a) **Exp(검정 실선) vs Sim(빨강 파선)**, ≈10 쌍. 축 V **2–4**, Q **0–1.15e−3 Ah**.
- 곡선 길이가 사이클에 따라 **≈1.15e−3 → ≈0.88e−3** 으로 줄어든다.
- `[도표]` **잔차가 구조적이다**: `Q ≈ 0` 에서 Sim 이 ≈4.05 V 로 **Exp(≈3.90 V)를
  위로 벗어나고**, 3.3–3.5 V 구간에서는 Sim 이 **아래로** 눕는다.
  RMSE 24.2 mV 는 이 편향을 평균한 값이다.
- ★ 컷오프 **2.0 V** 가 여기서만 읽힌다 (G6).

(b) `ε_p` vs Cycle. `[도표]` 동그라미 11 점 (≈0.3255 @0 → ≈0.2735 @125),
직선 1 개. `[도표]` 잔차 부호가 **초반 + / 후반 −** 로 정렬 → **가속형 곡률**(§8.4).
★ **cycle 0 의 식별값 ≈0.3255 가 Eq.(2) 의 `ε_p,fresh = 0.321` 과 다르다**
(Fig. 8b 의 cycle 0 은 ≈0.3215 로 0.321 에 가깝다). `[인쇄]` 는 0.321 을
"the batteries involved in this study" 의 **공통값**으로 쓴다 → **D6**.

(c) SOH-Exp(파란 ○) · SOH-Sim(빨간 ×) · Error(검정 막대, 우축 0–0.05).
`[도표]` SOH 1.000 → **≈0.771**. 오차 최대 **≈0.0145 @cycle 40**, 최소 ≈0.0005 @104.

## Fig. 8 (p9) — Battery B 모델 결과 `[도표]`

(a) 같은 구조, 곡선들이 훨씬 빽빽(10 % 만 감쇠). RMSE 14.2 mV.
`Q ≈ 0` 의 Sim 상향 편향은 A 와 **동일**(≈3.83 vs Exp ≈3.90 — 방향은 반대로 보인다,
판독 ±0.05 V 로 단정하지 않는다).
(b) `ε_p` 0.3215 @0 → ≈0.2978 @140, 축 0.29–0.33. 직선 기울기 `[재현]`
0.0237/140 = **1.69e−4** ↔ 인쇄 **1.707e−4** ✓.
(c) SOH 축 0.88–1.00. `[도표]` 1.000 → ≈0.902. 오차 최대 ≈**0.0057 @cycle 32**.
★ **논문은 B 의 최대 오차를 인쇄하지 않는다** (평균 <0.5 % 만).

## Fig. A.1 (p10, 부록) — DVA `[도표]` ★★★ **크로퍼가 빠뜨린 그림**

(a) **NCM811 반쪽전지**: x = **SOC/%** 0–100, y = **dVdQ·Qc/V** 0–4.
곡선 1 개(검정). `[도표]` 특징: 0–2 % 에서 급강하 → 3–30 % 완만한 골(≈0.5) →
상승 → **화살표 ① SOC ≈49 %**(≈0.95) → 얕은 골 → **화살표 ② SOC ≈72 %**(≈1.05)
→ SOC ≈80 % 에서 골(≈0.57) → 85 % 이상 급상승(→3.9).

(b)(c) **완전지 A·B**: x = **Q/Ah ×10⁻³** 0–1.15, y = dVdQ·Qc/V **0.5–2.5**,
≈11 곡선. "NCM" 화살표 2 개가 `Q ≈ 0.45e−3` 과 `≈0.68e−3` 을 가리킴.
`[도표]` **노화 곡선(분홍/갈색)이 신품(빨강)보다 위에 있고 더 짧다.**

★★★ **세 가지 문제** (`[해석]`):

1. **x 축이 다르다.** (a) 는 **SOC/%**, (b)(c) 는 **Q/Ah**. `[인쇄]` 는
   "**By comparing** the dV/dQ curves on the half-cell … and the full-cells" 라고
   쓰지만 **두 축 사이의 사상이 주어지지 않아 겹쳐 볼 수 없다.**
2. **특징점 위치가 안 맞는다.** `[재현]` 완전지의 NCM 화살표를 신품 용량
   (≈1.12e−3 Ah)으로 정규화하면 **40.2 % 와 60.7 %** 인데, 반쪽전지 화살표는
   **≈49 % 와 ≈72 %** 다 → **각각 9–11 %p 어긋난다.** (완전지 SOC 정의가 다를 수
   있으나 논문이 그 정의를 주지 않는다 — G12.)
3. **`Qc` 가 정의되지 않았다.** 축 라벨 `dVdQ·Qc/V` 의 `Qc` 가 본문에 **0 회**.
   신품 용량인지 당시 용량인지에 따라 **"순수 LAM 이면 곡선이 불변" 이라는 검정이
   가능해지기도 하고 불가능해지기도 한다.** `[도표]` 노화 곡선이 NCM 봉우리에서
   신품의 **≈1.3 배**로 올라가는데, `Qc` = 당시 용량이면 이 상승은 순수 LAM 과
   **모순**이고, `Qc` = 신품 용량이면 `1/(1−0.23) = 1.30` 으로 **정확히 일치**한다.
   → **그 구별을 논문이 독자에게 주지 않는다.**

★★★★ 그리고 §6.4 의 근본 문제: **이 DVA 는 음극 봉우리를 볼 수 없는 셀에서
음극 봉우리가 없음을 확인한 것이다.**

---

# 10. 어긋남 원장 (실제로 어긋난 것만 — 개수를 맞추지 않았다)

## D1 ★★★ IC 봉우리 감소가 "거의 같은 크기" 가 아니다
`[인쇄]` §4.1.1 "The degradation of the three peaks was of approximately the same
magnitude, indicating minimal or no loss of lithium inventory (LLI)."
`[도표]` Fig. 3b(Battery B): 봉우리 1 −21.7 % vs 봉우리 3 −11.0 %, **같은 구간
용량 변화는 −10 %**. 판독 오차 ±2 %p. → **봉우리 1 만 용량의 2 배로 준다.**
`[해석]` 원인이 LLI 인지 1C 분극인지는 이 자료로 가를 수 없다 —
**바로 그것이 저율 ICA 를 포기한 대가다**(§6.5).

## D2 ★★★ `ε_se` 의 처리가 어느 쪽이든 모델이 깨진다
`ε_p + ε_se = 1.000` 이 신품에서 정확히 성립하고 `κ_eff = κ_se·ε_se^brug` 다.
노화 중 `ε_p` 가 줄 때:
- **`ε_se = 1 − ε_p` 를 유지하면**: `[재현]` A 의 125 사이클 `ε_p = 0.2752` →
  `ε_se = 0.7248` → `κ_eff = 0.3985 × 0.7248^3.67 = 0.1223 S/m`
  → **신품 0.0963 대비 +27 %.**
  ★ **모델은 셀이 늙을수록 복합양극의 이온 전도가 좋아진다고 말한다.**
  그런데 같은 논문 §4.1.4 는 `[인쇄]` "the occurrence of cracking … **increases the
  tortuosity** of the lithium-ion transport path and **reduces the effective
  conductivity** of the sulfide electrolyte" 라고 쓴다. **정반대다.**
- **`ε_se = 0.679` 로 고정하면**: `ε_p + ε_se = 0.954` → **9.5 vol% 의 유령 공극**이
  생기고 복합양극의 체적 폐합이 깨진다.

**논문은 어느 쪽을 택했는지 적지 않는다** (G5). 둘 중 하나는 반드시 참이고
**둘 다 논문의 서술과 충돌한다.**

## D3 ★★★ "LLI 없음" 이 관측이 아니라 파라미터 동결의 결과다
리튬 재고를 정하는 두 수(`cp0`·`cn0`)는 (i) 신품에서 한 번 적합되고 (ii) 노화 전
구간에서 **고정**되며 (iii) **값이 공개되지 않는다**(`[인쇄]` "not disclosed").
그 위에서 `[인쇄]` "minimal or no loss of lithium inventory (LLI)" 를 결론한다.
그리고 SI 가 `[인쇄]` **쿨롱 효율을 "our analysis and modeling 에 쓰이지 않는다"**
며 제출하지 않는다 — **LLI 를 셀 수 있는 유일한 전하 수지 채널이다.**
`[해석]` **LLI 는 측정되지 않았고, 모델에서 변할 수 없게 되어 있다.**

## D4 ★★ Fig. 4c 의 원호와 Table 2 의 `R_ct` 가 반대 방향이다
`[도표]` Battery B 의 **노화 원호 정점이 신품의 2/3**(≈28 vs ≈42). Table 2 는
`R_ct` 81.67 → 91.97(**+12.6 %**). CPE 지수 `n` 이 바뀌면 양립 가능하지만
**`n` 이 보고되지 않는다**. 그리고 **적합 곡선 오버레이가 없어** 독자가
확인할 수 없다.

## D5 ★★ 부록의 "비교" 가 비교 불가능한 두 축 위에서 이루어진다
Fig. A.1(a) = `dVdQ·Qc/V` vs **SOC/%**, (b)(c) = 같은 y vs **Q/Ah**.
`[인쇄]` "By comparing …" 에 해당하는 사상이 없고, `[재현]` 특징점 위치가
**9–11 %p 어긋난다**. `Qc` 는 정의되지 않았다.

## D6 ★ `ε_p,fresh` 가 논문 안에서 둘이다
`[인쇄]` Eq. (2) 아래: "`ε_p,fresh` … has a value of **0.321** in the batteries
involved in this study"(복수, 공통값). `[도표]` Fig. 7b 의 cycle 0 식별값은
**≈0.3255**, Fig. 8b 는 **≈0.3215**. → A 의 시작점이 Eq. (2) 가 쓰는 값과
`[재현]` ≈1.4 % 다르다. 이 차이는 SOH 로 환산하면 `[재현]` ≈2 %p 로
**보고된 평균 오차(1 %)보다 크다.**

## D7 ★ 음극 이름이 둘이다
셀 명칭과 Eq. (1) 은 **Li4.4Si**, §3.1 조립은 **Li3.75Si**.
Li:Si 가 4.4 vs 3.75 (**17 % 차**)이고 `θn = c^n_left/c^n_max` 의 분모가 어느
기준인지 정해지지 않는다. `c^n_max = 1.065e4 mol/m³` 는 `[재현]` Li3.75Si 완전
리튬화(≈8.2e4)의 **13 %** 라 **어느 쪽도 아니다** (유효 적합값).

## D8 ★ SI 체크리스트가 본문에 없는 항목에 ✓ 를 찍는다
`[인쇄]` SI Table 1 에서 ✓ 된 것 중 본문에서 확인되지 않는 것:
- **"Voltage (or potential) range"** — 본문에 없다. `[도표]` 그림 축에서만 읽힌다 (G6).
- **"Apparent electrode density (areal mass loading ÷ thickness)"** — 본문에 없다.
  `[재현]` 계산은 가능하다 (10.7 mg cm⁻² ÷ 98 µm = **1.09 g cm⁻³**) — 그런데
  그 값이 §3.3 의 ≈26 vol% 공극과 짝이 된다.
- **"Current collector type and thickness"** — 종류(Al/Cu)는 있고 **두께가 없다**.

## D9 ⚠ (어긋남보다 관측) 하이라이트와 결론의 강도가 다르다
하이라이트 `[인쇄]` "**is identified as** the main aging mechanism" (단정) ↔
결론 `[인쇄]` "is **likely** the main cause … **considering the overloading of the
anode material**" (조건부). **조건절이 하이라이트에서 사라진다.**

---

# 11. Q1~Q8 채움 (닻 카드에 넣을 행의 근거)

| 축 | 9호가 준 것 |
|---|---|
| **Q1 접촉 손실 정량** | **부분 — 그리고 자기 모순이다.** `[인쇄]` `A^p_eff = 0.4938` (무차원, 양극, BV 분모에 정의) = 이 계보 최초의 **모델 파라미터로서의 양극 접촉 면적비**. ⚠ (a) **적합값**, (b) **노화 중 고정** → `θ(N)` 0, (c) `[재현]` 자기 SEM 의 입자 반경(≈1.05 µm)을 쓰면 **0.055 로 9 배 움직인다**. `contact loss` 3 회는 전부 **남의 논문 인용**(refs 17,18,21) |
| **Q2 독립 관측** | **부분.** SEM(표면, 정성, 노화 1 + 신품 1, `[도표]` Probe 6.5 배 차) · EIS(2-전극, 등가회로) · **압력 센서 연속 시계열(★ 계보 최초)**. **XRD·XPS·TEM·ICP·적정·3-전극·반쪽전지(노화품) 전부 0.** `LAM_PE` 를 적합 밖에서 확인한 관측 **0 건** |
| **Q3 라벨 층위** | ★★ **새 층위: `fitted-single-parameter`.** 노화 라벨 = **1-파라미터 PSO 적합**(`ε_p`), 정답축이 **자기 자신의 방전곡선**이다. 오차막대 0 · 셀 2 · 반복 0 · `n =` 0 회. ★ **Table 3 에 provenance 열이 없고 6 개 값이 비공개**(`[인쇄]` "not disclosed") |
| **Q4 유일성** | **0 (9/9 편).** `uncertaint*`·`identifiab*`·`sensitiv*`·`confidence`·`Fisher`·`condition number`·`bootstrap`·`initial guess`·`multi-start`·`error bar`·`regulariz*`·`objective function` **전수 0 회**. ★★★ **그러나 성질이 또 바뀐다**: 8호가 "이름을 실패 모드 목록에 올렸다" 였다면 **9호는 자기 표 안에 축퇴의 지문 셋을 인쇄해 놓고 다르게 부른다** — ① `R_SEI` 분해가 두 셀에서 **+37 % / −80 %** 인데 `[인쇄]` "장비 정확도·적합 오차·열평형" 탓 ② `A_eff·ε_p/R_s` 곱 축퇴 ③ `k_LAM` 셀 간 **2.15 배**를 `[인쇄]` "slightly different" |
| **Q5 상대극 기준 전위** | **해당 없음 → 그러나 새 형태로 열린다.** `indium`·`Li-In` 0 회. ★ **계보 최초의 합금(Li-Si) 음극**이고 모델은 `U^n_ocp(θn)` 를 **비평탄 보간 함수**로 둔다. `[재현]` 모델 N/P ≈ **3.14** → **사이클당 음극 화학량론 스윙 31.8 %**. → **이 카드의 "전고체 음극은 평탄 → 5→3 붕괴" 가 이 셀에는 성립하지 않는다.** ⚠ N/P 는 SI 가 `[인쇄]` 제출 거부한 값이고 우리가 Table 3 에서 계산했다 |
| **Q6 압력** | ★★ **있다 — 계보 최초의 `in operando` 연속 힘 시계열.** `[도표]` Fig. 6 이 12 사이클의 힘을 `Kg` 로 기록(고점 296.6 · 저점 294.0 · 스윙 2.6). `[재현]` 면적 7.854e−5 m² 로 환산 → **평균 ≈36.9 MPa · 주기 변조 ≈0.32 MPa**. ⚠ **`MPa` 0 회 · 제작 압력값 0 · 교정 0 · 스윕 0 · 노화 전 구간 추세 0**. ★★ **압력이 모델에 들어가지 않는다** — Eq. (2) 는 사이클 수만의 함수다 |
| **Q7 dead Li** | **해당 없음** (Li-Si 합금 음극). `dead li`·`isolated` 0 회. ⚠ 그리고 **CE 를 SI 에서 명시적으로 제출 거부**한다 → `LLI` 의 전하 수지 채널이 닫힌다 |
| **Q8 화학·OCP** | **있다(CC).** **단결정 NCM811 + H₃BO₃ 코팅**(★ 계보 최초의 붕산 코팅) : Li₆PS₅Cl : VGCF = **56:40:4 wt%**, `[재현]` **10.7 mg cm⁻²**, 1C ≈135 mA/g ≈1.128 mAh, `[도표]` **2.0–4.3 V**, 전 구간 기울기 있음. ★ `[도표]` Fig. A.1(a) = **NCM811 반쪽전지 dV/dQ vs SOC** (계보 최초의 양극 반쪽셀 미분곡선) ⚠ **측정조건 전무**(G12). **OCV·GITT 0 회** — 모델의 `U_ocp` 두 곡선은 출처가 없다 (G1) |

**8편 누적 ≈7.0 → 9편 누적 ≈7.5 칸.**
늘어난 것은 **Q6(압력이 "점·스윕" 에서 "시계열" 로)** 반 칸과 **Q3 의 새 층위**다.
**Q1 과 Q4 는 9호도 채우지 못했다** — 그러나 **Q4 의 성질이 세 번째로 바뀌었다**
(안 쟀다 → 이름이 목록에 올랐다 → **지문이 표 안에 있고 다르게 불린다**).

---

# 12. 우리 프로젝트와의 접점

## 12.1 ★★★ 가장 날카로운 것 — **우리 논지의 야생 실측이 이 논문 안에 있다**

`degradation-degeneracy/` 와 [[fitting-degeneracy]] 의 명제는
**"적합도가 좋다는 것은 분해가 유일하다는 근거가 아니다"** 다.
9호는 그 명제의 **부정을 문자로 인쇄한다**:

> `[인쇄]` "… these values are **not disclosed** in this paper. While such variations
> are expected …, **the robustness of the overall model and its predictive
> capabilities remain unaffected, as confirmed by our experimental results.**"

그리고 **같은 논문이 그 명제의 반례 셋을 자기 지면에 남긴다**:

| # | 반례 | 크기 |
|---|---|---|
| 1 | `R_SEI` 분해가 두 동일 셀에서 부호까지 어긋남 (합계는 같은 방향) | **+37 % vs −80 %** |
| 2 | `A^p_eff · ε_p / R_s` 곱 축퇴 — 자기 SEM 이 `R_s` 를 9 배 배반 | `A_eff ∈ [0.055, 0.494]` |
| 3 | `k_LAM` 의 셀 간 산포 ↔ 보고된 적합 오차 | **115 % vs 1 %** |

`[해석]` **3번이 특히 인용 가치가 크다: 보고된 "정확도" 가 그 정확도를 만드는
파라미터의 셀 간 산포보다 두 자릿수 작다.** 이것은 우리가 합성 격자에서 재는
**근최적 집합의 폭**([[near-optimal-set-width-measurement]])을 **실셀 모집단의 폭**
으로 바꿔 말한 것이고, 모집단이 2 뿐이라 폭조차 못 재는 상태다.

## 12.2 ★★ 우리가 이 논문에 공급할 수 있는 것

1. **`A_eff · ε_p / R_s` 의 근최적 폭.** 우리 폭 측정기는 화학 무관이다.
   Table 1 의 인쇄된 식 + Table 3 의 공개된 값이면 **이 곱의 등가선이 방전곡선
   공간에서 얼마나 평평한지**를 곧바로 그릴 수 있다 (`J^T J` 최소 고유벡터 —
   [[fitting-degeneracy]] 의 "그리는 법" 절차를 그대로).
   → **필요한 것은 G1(반쪽전지 OCP 두 곡선)과 G3(6 개 비공개 값)뿐이다.**
2. **`ε_p` → SOH 의 증폭 인자 분해.** §4.4 의 1.32–1.60 을
   "활물질 손실분 / 율 특성분" 으로 가르는 것은 **같은 모델을 `i → 0` 으로
   한 번 더 돌리면 끝난다** — 2호(Clausnitzer)에서 우리가 세운 **율 분리 시험**과
   같은 계열이다 ([[assb-apparent-capacity-decomposition]]).
3. **HPPC 의 값어치.** 이 논문이 수집하고 버린 HPPC 는 정확히
   `A_eff·ε_p/R_s` 곱을 용량으로부터 떼어낼 수 있는 여기(excitation)다.
   **"무엇을 더 재야 분해가 유일해지는가" 에 대한 구체적 답이 이 논문 안에 있다.**

## 12.3 ⚠ 가져올 수 있는 관측/feature — **거의 없다. 그리고 그게 정보다**

| 후보 | 쓸 수 있나 |
|---|---|
| `A^p_eff = 0.4938` | ❌ **수치로 못 쓴다** (9 배 불확정). **형태**(BV 분모의 곱셈 인자)만 가져온다 |
| `k_LAM` (3.667e−4 / 1.707e−4) | ❌ 셀 2 개 · 산포 115 % · 하수동조립. **`θ(N)` 시간축의 값으로 못 쓴다** |
| `ε_p,fresh = 0.321` | ⚠ **공극률 0 가정의 값**이다. 기하값은 ≈0.23 (§3.3) |
| 압력 ≈37 MPa · ΔP ≈0.32 MPa | ⚠ **우리 환산**이다 (G11). 조건부로만 |
| 2.0–4.3 V · 1C · 28 °C · 10.7 mg cm⁻² | ✅ 프로토콜 좌표로 쓸 수 있다 |
| NCM811 반쪽전지 dV/dQ (Fig. A.1a) | ⚠ 모양만. 측정조건 없음 |

★ `[해석]` **이 계보에서 9 편을 읽는 동안 "접촉 손실" 이라 불린 양이 아홉 개다.**
1호 기하 부피분율 · 2호 연결성 · 3호 계면 응력 · 4호 접촉 면적분율 + void 부피 ·
5호 전기적 대리량(음극) · 6호 없음(공정으로 대체) · 7호 없음(양극 없음) ·
8호 없음(종설) · **9호 BV 분모의 적합 곱셈 인자.**
**아홉 번째가 처음으로 "양극 접촉 면적비" 라는 정확한 이름을 달았는데,
그 값이 유일하지 않다.**

---

# 13. 추가로 받아야 할 원 논문 후보

| 순위 | 서지 (이 논문의 ref 번호) | 어느 Q 축 | 왜 |
|---|---|---|---|
| **1** | **[27] G. Li, G. Fan, X. Zhang, J. Han, Y. Wang, Y. Liu, L. Jia, B. Guo, C. Zhu, M. He, "Modeling of an all-solid-state battery with a composite positive electrode", *eTransportation* **20** (2024) 100315** | **Q1 · Q4 · Q8** | ★★★ **9호가 모델·PSO·해법·`A_eff` 정의를 전부 여기에 위임한다.** G1(OCP 출처)·G2(provenance)·G4(PSO 설정)의 답이 여기 있을 가능성이 가장 높다. **같은 연구실, 같은 셀 계열** |
| **2** | **[30] G. Conforto, R. Ruess, D. Schröder, E. Trevisanello, R. Fantin, F.H. Richter, J. Janek, "Editors' choice — Quantification of the impact of chemo-mechanical degradation on the performance and cycling stability of NCM-based cathodes in solid-state Li-ion batteries", *J. Electrochem. Soc.* **168** (2021) 070546** | **Q1 ★ · Q2** | ★★★ **9호 스스로 "정량한 몇 안 되는 문헌" 으로 지목한다** — `[인쇄]` "quantified the changes of active material in the cathode and tracked the length of the lithium diffusion path in a 40-cycle … by means of **relaxed open-circuit potential** and **EIS-PSD** analyses". **Q1 을 깰 1 순위이고, 방법이 OCP 기반이라 우리 축과 직결된다.** 9호는 이것을 `[인쇄]` "the error … is relatively large" 로 기각한다 — **그 오차의 크기를 우리가 직접 봐야 한다** |
| **3** | **[21] C.-Y. Yu, J. Choi, J. Dunham, R. Ghahremani, K. Liu, P. Lindemann, Z. Garver, D. Barchiesi, R. Farahati, J.-H. Kim, "Time-resolved impedance spectroscopy analysis of aging in sulfide-based all-solid-state battery full-cells using **distribution of relaxation times**", *J. Power Sources* **597** (2024) 234116** | **Q2 · Q4** | ★★ 9호가 "접촉 손실이 심했다면 EIS 변화가 더 컸을 것" 이라는 **자기 논거의 근거로 두 번 인용**한다. **DRT 는 병합 원호를 가르는 바로 그 도구** — §5.1 의 축퇴가 DRT 에서 어떻게 보이는지가 여기 있다. 8호(Li 2026)의 DRT 처방과도 이어진다 |
| 4 | [17] R. Koerver et al., "Capacity fade in solid-state batteries: interphase formation and chemomechanical processes in nickel-rich layered oxide cathodes and lithium thiophosphate solid electrolytes", *Chem. Mater.* **29** (2017) 5574 | **Q1** | 이 닻의 **오랜 1 순위**. 9호가 서론 첫 인용으로 쓴다 (`[인쇄]` "contact loss between NCM811 particles and sulfide SSE … led to increased resistance and decreased capacity"). 8호는 인용조차 안 했다 |
| 5 | [39] Y. Han, S.H. Jung, H. Kwak, S. Jun, H.H. Kwak, J.H. Lee, S.T. Hong, Y.S. Jung, *Adv. Energy Mater.* **11** (2021) 2100126 | **Q8 · Q2** | 9호의 "단결정은 안 깨진다" 논거의 실험 근거. **단결정 ↔ 다결정 대조**가 `LAM_PE` 의 기구를 가른다 |
| 6 | [22] W. Huang et al., "Unrecoverable lattice rotation governs structural degradation of single-crystalline cathodes", *Science* **384** (2024) 912 | **Q1** | 9호가 결론에서 `[인쇄]` "unavoidable … can be also considered a reason for the loss of active materials" 로 인정하면서 **모델에 넣지 않은** 두 번째 기구 |
| 7 | [44] M.A. Rahman, S. Anwar, A. Izadian, "Electrochemical model parameter identification of a lithium-ion battery using particle swarm optimization method", *J. Power Sources* **307** (2016) 86 | **Q4** | 9호의 PSO 절차가 통째로 위임된 곳 (G4). **초기값·경계·수렴 기준이 여기 있다면 그게 9호의 실제 설정이다** |

---

# 14. 이 digest 가 주장하지 않는 것

- **이 논문이 틀렸다고 주장하지 않는다.** 단결정 NCM811 + 황화물 복합양극에서
  양극 활물질 손실이 지배적일 **가능성은 충분히 있다**. 주장하는 것은
  **이 논문의 절차가 그것을 가려낸 절차가 아니라는 것**이다.
- **`A^p_eff = 0.4938` 이 틀렸다고 주장하지 않는다.** 주장하는 것은
  **`R_s` 와의 곱으로만 데이터에 들어가므로 단독으로 해석될 수 없다**는 것이다.
- **§9(Fig. 5)의 9 배**는 우리 픽셀 계측이다. 스케일바는 정확히 셌지만
  입자 경계는 저자가 그린 초록 원을 썼고 SEM 은 표면 투영이다.
- **§9(Fig. 6)의 37 MPa 환산**은 "kg 표시 = 셀 스택 축방향 힘" 가정에 달려 있다.
  가정이 틀리면 무효다 (G11).
- **§3.3 의 공극 ≈26 vol%** 는 밀도 3 개를 가정한 계산이고 `Lp` 의 출처도 모른다.
  **방향만** 취한다.
- **우리 저장소의 수치를 이 페이지에 복사하지 않았다.** 정본은 artifact +
  `degradation-degeneracy/docs/RESULTS*.md` 다.

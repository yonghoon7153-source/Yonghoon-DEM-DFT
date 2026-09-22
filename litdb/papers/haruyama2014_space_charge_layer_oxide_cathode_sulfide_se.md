<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-22 초판 — 본문(8 pp) + SI(10 pp) 전문, 크롭 17장(그림 12 + 표 5) 중 **그림 9장 실독**.
     ⭐ 이 digest 의 1번 임무는 **우리 v5 계면 기하의 원전 확인**이다 (`db/literature/refs.json[37]`
        이 이 논문을 "v5 single-interface + vacuum 의 1차 근거" 로 이미 등록해 두고 있다).
        결론: **기하 원전은 맞다. 다만 재현에 필요한 수가 반쯤 비어 있다** —
        총 원자수·슬랩 층수·계면법선 셀길이가 본문·SI 어디에도 없다 (§3c-4).
     ⚠ **공간전하층(SCL)은 이 논문에서 한 번도 정량되지 않는다.** 두께(nm)·전위(V)·Debye 길이가
        전부 없고 `Fig. 5` 는 **축 라벨이 아예 없는 만화**다. SCL 의 *현상* 원전이지 *정량* 원전이 아니다 (§10-①).
     ⚠ "Li migration" 이 초록에 있지만 **NEB 0회 · 배리어 0개**다. 끝점 에너지차 2개뿐 (§3g). -->

# Space−Charge Layer Effect at Interface between Oxide Cathode and Sulfide Electrolyte in All-Solid-State Lithium-Ion Battery — Haruyama, Sodeyama, Han, Takada, Tateyama (*Chem. Mater.* **26**, 4248–4255 (2014))

> slug `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` · DOI `10.1021/cm5016959` · type `계산 100 % (정적 DFT+U 슬랩 계면 — MD·NEB·AIMD 0회)` · PDF `inbox/11. ChemMater_2014_Haruyama_Space_charge_layer_oxide_cathode_sulfide_SE_MAIN.pdf` (본문 8 pp, `Fig. 1`–`5` + `Table 1`) + **SI** `inbox/11. Sup) ChemMater_2014_Haruyama_Space_charge_layer_SI.pdf` (10 pp, S1–S3 절 · `Fig. S1`–`S7` · `Table S1`–`S4`) · digested `2026-09-22` · status ✅ · 태그 **[외부]**

> elements: Li, Co, O, P, S, Nb
> methods: DFT, DOS, PDOS

> **저자**: **Jun Haruyama**(NIMS MANA + GREEN) · **Keitaro Sodeyama**(NIMS MANA + 京都大 ESICB) · **Liyuan Han**(NIMS Photovoltaic Materials Unit) · **Kazunori Takada**(NIMS MANA + GREEN — *버퍼층 실험의 원저자 중 하나*) · **Yoshitaka Tateyama\***(NIMS + 京都大 ESICB + JST PRESTO/CREST) · 접수 2014-05-11 / 개정 2014-06-16 / 게재 2014-07-03 (ASAP 재게재 2014-07-09 — `Figure 1` 오류 + **SI 파일 교체**) · KAKENHI 23340089 · SPIRE(MEXT) + CMSI · 계산 = NIMS · 九州大 · ISSP · 東大 ITC(Oakleaf-FX)
>
> **계보**: 실험 원점 **[Ohta 2006 *Adv. Mater.* 18, 2226](ref 9 — Li₄Ti₅O₁₂ 버퍼)** · **[Ohta 2007 *Electrochem. Commun.* 9, 1486](ref 10 — **LiNbO₃ 버퍼, 저항 최소**)** · **[Takada 2008/2013](refs 8, 5, 13 — SCL 가설의 제창)** → **본 논문(그 가설의 첫 원자단위 검증)** → **자기 후속 [Haruyama 2017 *ACS AMI* 9, 286](`papers/haruyama2017_cation_mixing_co_diffusion_lco_lps.md`)** 가 *같은 세 계면을 그대로 물려받아* **Co 양이온 혼합**을 얹는다. 본 논문 마지막 문단이 그 후속을 예고한다: *"this study did not deal with the significant mixture of Cobalt in the sulfide side … will be examined in a future study."*
>
> ⭐⭐ **우리 repo 안에서의 지위 — 이 편은 이미 우리 방법의 근거로 등록돼 있다.**
> `db/literature/refs.json` **`references[37] = haruyama2014`** 가 우리 paper #1 **v5 single-interface + vacuum** 방법의 **1차 근거(method-anchor-PRIMARY)** 이고, 동시에 **anti-sandwich 논거**(= v10b 샌드위치 기하에 반대하는 근거)로 태깅돼 있다. **즉 우리는 digest 없이 이 논문을 6개월째 인용해 왔다.** 이 digest 가 그 공백을 메운다.

> **본 digest 에서 실제로 본 그림 (2026-09-22)** — 크롭 **17장**(본문 그림 5 + SI 그림 7 + 표 5) 중 **그림 9장 실독**.
> **본문 5/5**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` — **전부 봤다.**
> **SI 4/7**: `Fig. S2`(고립 슬랩 종단) · `Fig. S4`(**초기 계면 + 정합 방향**) · `Fig. S6`(**완화 계면, 측면+정면 2뷰**) · `Fig. S7`(VBM/CBM 분자궤도).
>   · `Fig. S6`(c) 는 **2배 확대 크롭**을 따로 떠서 층수를 셌다 (§3c-4 의 원자수 추정 근거).
> **안 본 것 (그림 3장 + 표 5장)**: `Fig. S1`(벌크 단위셀 그림 — 셀 조성·k격자가 SI 본문에 활자로 있다) · `Fig. S3`(고립 슬랩 PDOS — 갭은 `Table S2` 에 활자로 있고 정성뿐) · `Fig. S5`(이동 샘플링 격자 도식 — 개수 16/4/9 가 SI 본문에 활자로 있다) · **`Table 1`·`Table S1`–`S4`**(표 = PDF 텍스트가 정확, 전량 전사했다).
> **그림 ↔ 본문 불일치**: 이 논문은 **거의 없다** — `Fig. 3`의 점선(계면 LCO 1층)이 (a)에서는 갭 안에서 0, (b)에서는 갭 안에 존재 ⇒ 본문 서술과 정확히 일치한다. 다만 **`Fig. 5` 는 축 라벨·눈금·단위가 하나도 없고**, **LCO(110)/LNO(110) 계면의 PDOS 는 논문 어디에도 없는데 본문은 *"거의 같다"* 고 단언한다** — 이 둘은 §10 에 적었다.
> **우리가 직접 한 산수**는 `*우리 산수*` 로 표시했다 (논문 주장 아님). 그림에서만 읽은 값은 **`figure-read ≈`**.

---

## 0. 이 digest 를 읽는 법 — 왜 지금 이 논문을 구했나

**세 가지 임무를 안고 왔다.**

1. ⭐ **기하 원전 확인.** 우리 v5 계면 슬랩(LiNiO₂|LPSCl)이 *이 계열에서 왔다*는 것이 `refs.json[37]` 의 주장이다. **그 주장이 원문으로 지지되는가, 그리고 우리가 옮겨온 것이 정확히 무엇인가.**
   → **§3c 가 이 digest 의 본체다.** 면지수·종단·정합·두께·진공·샘플링을 **표로 전수** 옮겼다.
   → **판정: 방법론(단일계면 + 진공 + W_ad 식 + 계통적 횡방향 이동)은 전부 원문에 있다. 그런데 *수치 재현*에 필요한 3개(총 원자수 · 슬랩 층수 · 법선방향 셀 길이)가 논문에 없다** (§3c-4). 그 3개는 **내가 그림에서 재서 추정**했고, 추정임을 명시했다.

2. **SCL 이 무엇으로 정량됐나.**
   → **정량된 적이 없다.** 전위 프로파일 0개 · 층별 전하적분 0개 · 두께(nm) 0개 · Debye 길이 0개. 있는 것은 **자리별 Li 공공 형성에너지 21개**(`Table 1`)와 **축 없는 개념도**(`Fig. 5`)뿐이다. 저자들도 인정한다: *"long-range variation of the concentration needs to be analyzed by methods involving the long-range electrostatic interaction."*
   → ⭐ **이것이 우리에게 좋은 소식이다.** `kb/methodology/computational_methods_canonical.md` §2 말미가 이미 **"공간전하층 정량(두께·전위·Debye 길이) — 문헌도 정성뿐이라 '계산했다'고 말할 수 없다"** 를 우리 경계로 선언해 뒀는데, **이 논문이 그 선언의 실물 증거**다 (§7c).

3. **NEB 값을 회수.**
   → **없다.** 초록의 *"the Li migration"* 은 **NEB 가 아니라 끝점 에너지차 2개**다 (−1.6 eV / −0.3 eV, §3g). 배리어·saddle·경로 0회. 우리 NEB 와 **방법 대조 자체가 성립하지 않는다.**

> **⚠ 물질계 근접도.** SE 가 **β-Li₃PS₄**(Pnma, PS₄³⁻ 골격, Lepley 의 *β-Li₃PS₄-b* 정렬모형)이고 양극이 **LiCoO₂**다. 우리는 **Li₆PS₅Cl(아지로다이트) | LiNiO₂/NCM** 이다. 골격(PS₄³⁻)은 공유하지만 **free S²⁻ 도 Cl⁻ 도 없다**. ⇒ **수치는 한 줄도 우리 원장에 이식하지 않는다.** 이 논문에서 가져오는 것은 **기하 프로토콜과 기전 서사**뿐이다.

---

## 1. 한 줄 요약

**LiCoO₂(110)|β-Li₃PS₄(010) 계면에서 황화물 쪽 Li 은 "고갈" 되기 전에 먼저 "빨려간다".** CoO₆ 팔면체를 (110) 면으로 자르면 **산소 두 개가 능선(ridge)으로 노출**되고, LPS 표면·차표면(subsurface)의 Li 이 그 능선 위로 **흡착**한다. 그 결과 ① LPS 슬랩이 **결정 질서를 잃고**(비정질화) ② 흡착 Li 을 내준 **LP2 자리의 Li 공공 형성에너지가 1.44 eV 까지 떨어진다**(벌크 LPS 3.2 eV 대비 **−1.76 eV**, *우리 산수*). 저자들은 이 **1.44 eV ≈ 1.44 V** 를 *"실험에서 충전이 시작되는 전압"* 과 동일시하고, 충전 초기 전압 프로파일의 **기울기(slope) = SCL 성장**이라고 읽는다.

**LiNbO₃ 버퍼는 그 고리의 첫 단추를 끊는다.** LNO 를 끼우면 LCO 표면의 산소 능선이 **LNO 의 O 로 덮여 CoO₆ 팔면체가 재생**되고, 그러면 **Li 흡착 자리 자체가 사라진다**. LNO(1̄0)|LPS 계면에서는 Nb–S 결합도 안 생기고 두 슬랩 모두 벌크 결정성을 유지하며, LPS 쪽 Li 공공 형성에너지가 **2.42–3.18 eV 로 벌크(3.2) 근처로 복귀**한다. LPS 쪽 자리 간 **편차도 1.83 eV → 0.76 eV 로 58 % 줄어든다**(*우리 산수*) — 그것이 곧 "전압 기울기가 사라진다" 의 계산판 표현이다.

**접착 강도는 화학이 아니라 *산소를 몇 개 내미느냐* 로 갈린다.** W_ad(eV/nm²) = LCO|LNO(1̄0) **10.6** > LCO|LNO(110) **6.1** > LCO|LPS **4.3** > LNO|LPS **3.8**. 저자의 한 줄 설명이 이 논문에서 가장 재사용 가치가 높다: *"최외곽층에 **능선 산소**(두 O 를 잇는)가 나오면 Li 을 세게 당기고, **꼭짓점 산소**(apical)가 나오면 안 당긴다."* LCO(110)은 능선, LNO(1̄0)은 꼭짓점이다.

**전자구조는 버퍼가 절연체로 작동함을 보인다.** LCO|LNO 에서 LNO 점유준위 꼭대기가 LCO VBM 보다 **≈1 eV 아래**(`figure-read ≈ −0.9 eV`), LNO|LPS 에서는 LPS 가 LNO 보다 **`figure-read ≈ 1.6 eV` 위**다 ⇒ 양쪽 모두 LNO 가 전자 장벽이다. 반면 **LCO|LPS 는 갭 안에 계면 LCO(Co 3d) 상태가 들어앉는다**(`Fig. 3`b 점선, `Fig. S7`) — 저자는 이를 *"무질서의 징표"* 로만 쓰지만, 실은 **계면 전자 누설 경로 후보**다 (§8-③).

⚠ 이 서사의 취약점은 **여섯 겹**이다(§10): ① **SCL 이 한 번도 정량 안 됨**(`Fig. 5` 는 축 없는 만화) ② **1.44 eV ↔ "실험 충전 개시 전압" 일치 주장에 실험값이 안 적혀 있다** ③ **LCO 면이 (110) 하나뿐인데 저자 스스로 (104)가 더 안정하다고 인용한다** — 핵심 기전(산소 능선)이 **(110) 전용 특징**이다 ④ **LCO|LPS 횡방향 표본이 4개뿐**이고 그 4개의 에너지 폭이 **6.19 eV** 다 ⑤ **spin-unpolarized** 인데 기전의 주체가 Co 3d 국소준위다 ⑥ **W_ad 의 변형(strain) 상쇄가 불명** — `Table S2`↔`S3` 대조하면 LPS 가 한 축 **+6.2 %**, LNO 는 **−8.4 %** 늘어나/줄어 있다(*우리 산수*).

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| **저자** | Jun Haruyama, Keitaro Sodeyama, Liyuan Han, Kazunori Takada, **Yoshitaka Tateyama\*** (NIMS + 京都大 ESICB + JST) |
| **저널/년** | *Chemistry of Materials* **26**, 4248–4255 (**2014**) |
| **DOI** | `10.1021/cm5016959` |
| **계 (조성)** | 양극 **LiCoO₂ (LCO)** · 전해질 **β-Li₃PS₄ (LPS)** · 버퍼 **LiNbO₃ (LNO)** |
| **계면 4종** | LCO(110)\|LNO(1̄0) · LCO(110)\|LNO(110) · **LCO(110)\|LPS(010)** · LNO(1̄0)\|LPS(010) |
| **연구유형** | **계산 100 %** — 정적 DFT+U 슬랩 계면. 실험 0회 · AIMD 0회 · NEB 0회 · MLIP 0회 |
| **자기 주장** | *"the first DFT calculation study on the LCO cathode/solid electrolyte as well as the buffer layers effect"* |
| **후처리** | **PDOS** + **Li 공공 형성에너지** + **부착에너지 W_ad** + **표면에너지 W_surf** + 분자궤도 시각화. (COHP·Bader·ELF·NEB·grand-potential **전부 0회**) |
| **참고문헌** | 55 (본문) + 11 (SI) |

---

## 3. 결과 — 절별 전수

### 3a. 벌크 검증 (`Table S1`, `Fig. S1` — S1 은 안 봄)

셀 설정 (SI §S1):
- **LCO**: 12원자 육방정 셀, k = **8×8×4**
- **LNO**: 30원자 육방정 셀, k = **8×8×4**
- **LPS**: 32원자 사방정 셀, k = **4×6×8**. ⭐ **무질서 처리** — *"In order to treat fractional occupations of the Li site in LPS, we use the **β-Li₃PS₄-b structure proposed by Lepley et al., which removes the Li atoms of 4c site**"* (ref S1 = Lepley, Holzwarth, Du *PRB* **88**, 104103 (2013)). ⇒ **SQS 아님 · enumerate 아님 · 단일 정렬 배열 하나**다.

| 물질 | a (Å) 계산 | b (Å) 계산 | c (Å) 계산 | E_g (eV) 계산 | a 실험 | b 실험 | c 실험 | E_g 실험 |
|---|---|---|---|---|---|---|---|---|
| **LCO** | **2.835** | — | **14.04** | **2.2** | 2.815 | — | 14.05 | 2.7 |
| **LNO** | **5.183** | — | **13.96** | **3.6** | 5.148 | — | 13.86 | 3.8 |
| **LPS** | **13.13** | **8.062** | **6.178** | **2.8** | 13.07 | 8.015 | 6.101 | n/a |

*우리 산수* — 격자 오차: LCO a **+0.71 %** / c **−0.07 %**; LNO a **+0.68 %** / c **+0.72 %**; LPS a **+0.46 %** / b **+0.59 %** / c **+1.26 %**. **전부 ±1.3 % 이내** — PBE(+U) 로는 매우 좋은 편.
갭: LCO 2.2 (실험 2.7, **−0.5**), LNO 3.6 (실험 3.8, **−0.2**). **LPS 갭 2.8 eV 에는 실험 대조가 없다** (`not available`).

> ⚠ **갭 판독법이 안 적혀 있다.** 고정점유 nscf 고유값인지 DOS 문턱인지 불명 ⇒ **우리 comp1 2.066 / modelc 2.099 eV 와 숫자로 비교 금지** (§7b).

---

### 3b. 표면 (`Table S2`, `Fig. S2` ✅ 실독, `Fig. 1` ✅ 실독)

**면 선택의 근거 (본문 §2.1 — 여기가 기하 원전의 출발점이다)**

| 물질 | 채택 면 | 채택 이유 (원문) | 저자가 스스로 인정한 반례 |
|---|---|---|---|
| **LCO** | **(110)** | 실험·이론이 **(110) 배향 LCO 표면**의 증거를 준다 (refs 24 Shao-Horn 2003, 25 Dahéron 2009). 게다가 **⟨110⟩ 방향이 Li 전도 경로**다 (ref 27 Van der Ven 2001) | ⚠ *"Although larger stability of the **(104)** surface was recently suggested (ref 26 = **Kramer & Ceder 2009**), the (110) surface still exists in the LCO particles"* — **더 안정한 면을 알면서 안 썼다** |
| **LPS** | **(010)** | **LPS 의 Li 전도 경로가 b 방향**이므로 (ref 28 Maruyama 2002) | — |
| **LNO** | **(1̄0)** 과 **(110)** 둘 다 | *"Few structural reports of the buffer layer LNO are available"* ⇒ **격자 미스핏 평가만으로** 이 둘을 골랐다 | ⚠ 표면 안정성 근거 없음 |

**종단 (termination)**
- **LNO(1̄0) = `−Li₂−Nb₂−O₆`**, **LNO(110) = `Li₆Nb₆−O₉`** (ref S6 = Sanna & Schmidt *PRB* **81**, 214116 (2010)) — **SI 에 활자로 명시**.
- **LCO(110)·LPS(010) 의 종단은 활자로 안 적혀 있다.** 공통 규정만 있다: *"**All these cleavage planes comprise a stoichiometric ratio** of the constituent atoms."* ⇒ **화학양론 종단**(non-polar). `Fig. 1`(a)·`Fig. S2`(a) 실독 결과 LCO(110)은 **CoO₆ 층을 옆에서 자른 면**이라 **두 산소를 잇는 능선(ridge)이 노출**되고 그 사이에 **Li 기둥**이 선다 — 이것이 뒤에 나오는 Li 흡착 자리의 정체다.

**슬랩 셋업**
- 진공 **≈1.5 nm** 추가.
- 슬랩 두께 **1–2 nm** — *"thick enough to show the bulk character in the central region"*.
- **횡방향 셀은 계산된 벌크값에 고정**하고 **원자 위치만 이완** (고립 슬랩 단계).
- 표면 k (면 평행만): **8×4×1** LCO(110)·LNO(1̄0) · **4×4×1** LNO(110) · **4×8×1** LPS(010).
- **W_surf = (E_slab − n·E_bulk) / 2S**

| 표면 | a (Å) | b (Å) | **W_surf (eV/nm²)** | *우리 산수* **J/m²** | E_g (eV) |
|---|---|---|---|---|---|
| **LCO(110)** | 4.910 | 14.04 | **14.08** | **2.256** | **0.70** |
| **LNO(1̄0)** | 5.183 | 13.96 | **5.63** | 0.902 | 3.0 |
| **LNO(110)** | 8.977 | 13.96 | **6.45** | 1.033 | 3.1 |
| **LPS(010)** | 13.13 | 6.178 | **1.94** | **0.311** | 2.6 |

> *우리 산수* 환산: **1 eV/nm² = 0.16022 J/m²**.
> *우리 산수* 표면셀 정체: LCO(110) a = **√3 × 2.835 = 4.910** ✓, b = **c_hex = 14.04** ✓ (CoO₂ 층 3장이 들어간다 — `Fig. 1`a 에서 실제로 3개 보인다). LNO(110) a = **√3 × 5.183 = 8.977** ✓. LPS(010) = **a_bulk × c_bulk** ✓.
> **관찰**: LCO(110) 표면에너지가 **LPS(010)의 7.3배**(14.08 vs 1.94). 황화물은 자르기 쉽고 산화물은 어렵다 — 우리 γ 축의 정성 앵커로 쓸 수 있다.
> **관찰 2**: 슬랩 갭이 벌크보다 낮다 — LCO 2.2→**0.70**(−1.5), LNO 3.6→3.0/3.1(−0.5), LPS 2.8→**2.6**(−0.2). LCO(110)의 갭 붕괴는 뒤에 나오는 **표면 중갭 상태**의 원인이다.

---

### 3c. ⭐⭐ 계면 구성 — **기하 전수** (`Table S3`, `Table S4`, `Fig. S4` ✅ 실독, `Fig. S5` 안 봄)

#### 3c-1. 4단계 구축 절차 (본문 §2.1 원문 그대로)

| 단계 | 내용 | 원문 근거 |
|---|---|---|
| **Step 1** | 각 성분의 **벌크 격자를 DFT+U 로 결정** | `Table S1` |
| **Step 2** | **화학양론 표면을 잘라 슬랩**을 만들고 **전 원자 좌표 이완**. 진공 **≈1.5 nm**, 슬랩 **1–2 nm** | `Fig. S2`, `Table S2` |
| **Step 3** | 슬랩을 **횡방향으로 배수**해 계면 슈퍼셀을 만들고 **붙는 두 면의 횡방향 격자상수를 맞춘다**. ⭐ **맞추는 방향이 비대칭이다** — *"Considering the **high elastic modulus of LCO**, the **LPS and LNO lattice constants are set to that of the LCO**"* (LCO/LNO·LCO/LPS). *"On the other hand, the **average of the two lattices** is taken for the **LNO/LPS**."* 미스핏 **3–5 %** | `Table S3` |
| **Step 4** | **계통적 횡방향 미끄럼(lateral slide)** — 대칭을 고려해 **LCO/LNO 16개 · LCO/LPS 4개 · LNO/LPS 9개** 표본을 만들어 **전부 DFT+U 로 이완**하고 **최저에너지 구조를 계면으로 채택** | `Fig. S5`, `Table S4` |
| **공통** | **계면 슬랩 바깥에 진공 ≈1.5 nm 를 또 넣는다** (⭐ anti-sandwich 논거, 아래 인용) · 이완 시 **전 원자 위치 + 횡방향 셀 파라미터 자유** | 본문 §2.1 |

> ⭐⭐ **우리 v5 의 근거 문장 — 원문 그대로 (`refs.json[37]` 이 인용하고 있는 바로 그 대목)**
> *"Note that a vacuum region with about 1.5 nm width is still added in the outside of the interface slab (consisting of two attached surface slabs). **Without this vacuum, the supercell approach always involves two interfaces, which are atomically different in most cases. Besides, artificial interaction between the two interfacial polarizations may arise, preventing accurate estimation of the stability of each interface. Therefore, the presence of the vacuum region is quite crucial.**"*
> ⇒ **비대칭 종단의 산화물/황화물 이종계면에서 샌드위치(PBC 양쪽 계면) 기하를 쓰지 말라**는 명시적 주장. 우리 v10b 샌드리치 철회의 문헌 근거가 정확히 이 문장이다.

#### 3c-2. 미스핏 · 완화된 셀 · 부착에너지 (`Table S3` — 원문 값 그대로)

| 계면 | **μ (%)** | **a (Å)** | **b (Å)** | **γ (°)** | **W_ad (eV/nm²)** | *우리 산수* **J/m²** |
|---|---|---|---|---|---|---|
| **LCO(110)/LNO(1̄0)** | **3.4** | 14.32 | 9.98 | 89.8 | **10.6** | **1.698** |
| **LCO(110)/LNO(110)** | **5.2** | 14.05 | 9.63 | 88.6 | **6.1** | 0.977 |
| **LCO(110)/LPS(010)** | **3.7** | **13.94** | **24.46** | **87.4** | **4.3** | **0.689** |
| **LNO(1̄0)/LPS(010)** | **3.6** | 12.79 | 31.15 | 90.0 | **3.8** | 0.609 |

정의 (SI §3.1, §3.3):
- **미스핏** `μ = 1 − 2·S_{A∩B} / (S_A + S_B)` — **면적 중첩** 정의 (refs S10 Liu 2003, S11 Martin 2012). ⚠ **선형 변형률이 아니다.**
- **부착에너지** `W_ad = (E_A^tot + E_B^tot − E_{A/B}^tot) / S`, 여기서 `E_A^tot`·`E_B^tot` 는 ***relaxed isolated slabs*** 의 총에너지, `S` 는 계면 면적, `γ` 는 두 횡방향 셀 벡터 사이 각.
- **정렬 규약**: *"We aligned the **LCO [001]** direction with the **LNO [001]** and the **LPS [100]**."* (`Fig. S4` 에서 화살표로 확인 ✅)

#### 3c-3. ⭐ *우리 산수* — 슈퍼셀 배수와 **실제 선형 변형률** (논문이 안 적은 것)

`Table S2`(고립 표면셀)와 `Table S3`(완화된 계면셀)을 나누면 배수와 변형이 나온다. **아래는 전부 우리 산술이다.**

| 계면 | 정렬축 **a** 의 정체 | **a 배수** | a 변형 (A쪽/B쪽) | **b 배수** | b 변형 (A쪽/B쪽) |
|---|---|---|---|---|---|
| LCO/LNO(1̄0) | LCO c 14.04 ∥ LNO c 13.96 → 14.32 | 1 : 1 | **+2.0 % / +2.6 %** | 2 × 4.910 = 9.82 ∥ 2 × 5.183 = 10.37 → 9.98 | +1.6 % / **−3.7 %** |
| LCO/LNO(110) | 14.04 ∥ 13.96 → 14.05 | 1 : 1 | +0.1 % / +0.6 % | 2 × 4.910 = 9.82 ∥ 1 × 8.977 → 9.63 | −1.9 % / **+7.3 %** |
| **LCO/LPS** | LCO c 14.04 ∥ **LPS a 13.13** → **13.94** | **1 : 1** | **−0.7 % / +6.2 %** | **5 × 4.910 = 24.55 ∥ 4 × 6.178 = 24.71** → 24.46 | −0.4 % / −1.0 % |
| **LNO/LPS** | LNO c 13.96 ∥ LPS a 13.13 → **12.79** | 1 : 1 | **−8.4 % / −2.6 %** | **6 × 5.183 = 31.10 ∥ 5 × 6.178 = 30.89** → 31.15 | +0.2 % / +0.8 % |

> 🔴 **여기서 두 가지가 드러난다 (둘 다 §10 로 간다).**
> ① **"미스핏 3–5 %" 는 면적 정의라 한 축의 선형 변형을 가린다.** LCO/LPS 에서 **LPS 는 한 축이 +6.2 % 늘어나 있다**. LNO/LPS 에서는 **LNO 가 −8.4 % 압축**돼 있다.
> ② **LNO/LPS 의 a = 12.79 Å 은 논문이 밝힌 초기 설정(두 벌크의 평균 = 13.545 Å)보다 5.6 % 작다.** 횡방향 셀을 자유이완했으니 물리적일 수는 있으나, 그러면 **−8.4 % 압축 상태의 W_ad(3.8)** 를 **−0.7 % 인 LCO/LPS 의 W_ad(4.3)** 와 나란히 표에 올린 것이 된다. `E_A^tot`·`E_B^tot` 가 **변형된 셀에서 계산됐는지 원래 벌크 셀에서 계산됐는지 논문이 말하지 않는다** — 후자면 변형에너지가 **상쇄되지 않고 W_ad 에 섞인다**. (우리 v5 보고서가 스스로 잡았던 *"STRAIN ARTIFACT: NCM strained to SE cell, but E_NCM_iso uses original cell"* 와 **같은 함정**이다.)
> ③ **LCO/LPS 의 5 : 4 정합이 `Fig. S5`(d) 의 "super periodic structure"** 다 — 그래서 횡방향 표본이 16개가 아니라 **4개로 줄었다**.

#### 3c-4. ⭐ 슬랩 두께 · 진공 · **총 원자 수** — 논문에 **없다**

| 항목 | 논문 값 |
|---|---|
| 슬랩 두께 | **"1–2 nm"** (각 성분) — 층수·Å 값 **없음** |
| 진공 | **"about 1.5 nm"** (고립 표면 단계 + 계면 슬랩 바깥 모두) |
| 법선방향 셀 길이 | ⛔ **없음** (`Table S3` 은 횡방향 a·b·γ 만 준다) |
| **총 원자 수 (nat)** | ⛔ **없음** — 본문·SI 어디에도 한 번도 안 나온다 |
| 원자 좌표 파일 | ⛔ **없음** (2014년 논문, CIF/POSCAR 미첨부) |

> 🔧 ***우리 산수* — 재현용 추정 (⛔ 논문 값 아님, 검산용으로만)**
> **근거 3가지를 겹쳤다.**
> 1. `Fig. S3` 캡션이 고립 LCO(110) 슬랩의 표면층을 **"the 1st and 8th layer"** 라 부른다 ⇒ **LCO(110) = 8층**.
> 2. LCO(110) 층간거리 `d₁₁₀ = a_hex/2 = 1.4175 Å` ⇒ 8층 = **11.34 Å ≈ 1.1 nm** ✓ (*"1–2 nm"* 와 일치).
> 3. `Fig. S6`(c) 를 2배 확대해 **진공 1.5 nm 를 자로 삼아** 화면에서 실측: LCO 두께 **≈11.5 Å (= 8.1 층 ✓)**, LPS 두께 **≈16.7 Å (= 2.07 × b_LPS 8.062 ✓)**, **법선방향 셀 전장 ≈ 43 Å**.
>
> 층당 원자수: LCO(110) 표면셀(4.910 × 14.04) × d₁₁₀ = **97.7 Å³ = 벌크 육방정 셀 부피** ⇒ **층당 3 f.u. = 12 원자**.
>
> | 계면 **LCO(110)/LPS(010)** | 배수 | 두께 | 원자수 |
> |---|---|---|---|
> | LCO | 1 × **5** 표면셀 | **8 층** | 8 × 3 f.u. × 5 = **120 f.u. = 480 원자** (Li₁₂₀Co₁₂₀O₂₄₀) |
> | LPS | 1 × **4** 표면셀 | **≈2 × b** | 4 × 2 × 32 = **256 원자** (Li₉₆P₃₂S₁₂₈) |
> | **합** | — | — | **≈ 736 원자** |
>
> ⚠ 오차원: 진공을 정확히 15.0 Å 로 잡은 것 · 그림 경계가 원자 반지름만큼 뭉개진 것 · LPS 두께가 2.0 인지 2.5 인지. **±15 % 로 본다.** LNO 계면들은 종단 주기(`−Li₂−Nb₂−O₆`)만 알고 층수 단서가 없어 **추정하지 않았다**.
> ⇒ **Γ-only 로 ~700 원자**는 2014년 K-computer 계열(SPIRE/CMSI, Oakleaf-FX) 자원과 정합한다. 다만 이 규모로 **29회 횡방향 이완 + 21개 공공 계산**을 돌린 것이 된다.

#### 3c-5. 횡방향 미끄럼 표본의 에너지 (`Table S4`, 상대에너지 eV, 각 열의 최소 = 0.00)

| Index | LCO/LNO(1̄0) | LCO/LNO(110) | **LCO/LPS** | LNO/LPS |
|---|---|---|---|---|
| 1 | 7.22 | 3.71 | 6.19 | 1.07 |
| 2 | 6.12 | 2.58 | 1.77 | × |
| 3 | 8.70 | 1.99 | 1.41 | × |
| 4 | 4.77 | 3.73 | **0.00** | × |
| 5 | 3.85 | 3.58 | — | 5.04 |
| 6 | 5.70 | 2.58 | — | × |
| 7 | 4.30 | 1.32 | — | × |
| 8 | 9.07 | 2.84 | — | × |
| 9 | 3.84 | 3.20 | — | **0.00** |
| 10 | 3.42 | 3.57 | — | — |
| 11 | 5.03 | 1.47 | — | — |
| 12 | 6.79 | 2.46 | — | — |
| 13 | 5.97 | 1.66 | — | — |
| 14 | **0.00** | 1.97 | — | — |
| 15 | 8.74 | **0.00** | — | — |
| 16 | 8.72 | 2.69 | — | — |

(`×` = *"we did not calculate some of the LNO/LPS interface samples because they have relatively higher initial energies"*, `—` = 해당 표본 없음)

> 🔴 **표본 폭이 크다.** LCO/LNO(1̄0) **0 → 9.07 eV**, LCO/LPS **0 → 6.19 eV**. 즉 **미끄럼 하나로 총에너지가 6–9 eV 움직인다.** 그런데 **정작 이 논문의 결론이 걸린 LCO/LPS 는 4개**뿐이고, **LNO/LPS 는 9개 중 3개만 계산**했다. 게다가 계산을 건너뛴 판정 기준이 **"초기(이완 전) 에너지가 상대적으로 높아서"** 다 — 이완 후 순서가 뒤집힐 수 있는데 그것을 확인하지 않았다.
> *우리 산수*: `Fig. S5`(d)의 초주기(super periodicity)로 4개가 **16개와 등가**라는 것이 저자 주장이지만, 그 등가성은 **미끄럼 격자 대칭** 논거이지 **이완 후 국소최소 개수**의 논거가 아니다.

---

### 3d. 계면 구조 — 완화 결과 (`Fig. 2` ✅ 실독, `Fig. S6` ✅ 실독)

#### (a,b) LCO|LNO — **매끄럽게 붙는다**
- 계면 중간영역에서 **CoO₆ 팔면체 대신 유사사면체 CoO₄** 가 나타나고, **NbO₄ 사면체가 LCO 쪽으로 기운다.**
- 그 결과 **최외곽 Co 가 LNO 쪽 O 를 빌려 새 CoO₆ 팔면체를 만든다** (`Fig. 2`a,b 인셋에서 실제로 파란 팔면체 옆에 초록 팔면체가 산소를 공유하는 것이 보인다 ✅).
- **LCO(110)/LNO(1̄0) 이 더 단단히 결합**하고 W_ad 도 크다 (10.6 vs 6.1) — *"Its well-fitted nature is the consequence of the **similar crystal structures** of LCO and LNO."*
- ⚠ **LCO(110)/LNO(1̄0) 의 LCO 층이 눈에 띄게 기울어 있다**(`Fig. 2`a·`Fig. S6`a 에서 파란 띠 3개가 전부 사선 ✅). 저자 설명: *"due to the **overbalance of the Li atoms**"*, 계면 Li 을 몇 개 빼면 왜곡이 사라지며 **PDOS·공공형성에너지에는 영향이 거의 없다**.

#### (c) **LCO|LPS — 이 논문의 주인공**
- **S 원자 하나가 Co 에 끌려가 `CoO₄S` 오면체(pentahedron)가 부분적으로 생기고**, 그 PS₄ 사면체는 빈 공간 쪽으로 밀린다 (`Fig. 2`c 인셋에서 파란 다면체에 **노란 S** 가 붙은 것이 명확히 보인다 ✅).
- 그러나 **계면 결합은 매우 불완전**하다 — *"quite incomplete, compared with the LCO/LNO interface"*. 원인: 황화물의 격자상수·결합길이가 LNO 와 크게 다름.
- ⭐ **LPS 쪽 Li 이 LCO 로 강하게 끌려가 흡착한다** — **CoO₆ 층 위**와 **Li 층 위** 두 곳. 전자는 **CoO₆ 팔면체의 "산소 능선(ridge/bridge)" 에 결합**한다.
- **그 결과 LPS 슬랩이 벌크 결정 질서를 잃는다**(LCO 슬랩은 원자망 유지). `Fig. 2`c / `Fig. S6`c 실독: **LPS 쪽 PS₄ 사면체 방향이 제각각**이고 LiS₄(연두 다면체)가 흐트러져 있다 — (d) 의 정연한 LPS 와 나란히 놓으면 차이가 분명하다 ✅.

#### (d) LNO|LPS — **불활성 계면**
- **Nb–S 결합 없음 · Li 흡착 자리 없음.** 남는 것은 **이온성 O–Li · Li–S 인력**뿐. `Fig. 2`d 실독: 두 슬랩 사이에 **뚜렷한 간격**이 있고 양쪽 다 결정성 유지 ✅.
- W_ad 는 LCO/LPS 와 비슷 (3.8 vs 4.3).
- **Li 이동 방향이 반대다**: LNO 쪽 Li 이 LPS 쪽으로 **약간 치우친다** (LCO/LPS 에서는 LPS→LCO 였다).

#### ⭐ 저자의 통합 설명 — **"능선 산소 vs 꼭짓점 산소"** (이 논문에서 가장 재사용 가치 높은 한 줄)
> *"This can be understood with the **number of outermost O atoms** in the oxide interface. **The ridge connecting two oxygen atoms is exposed in the LCO interface**, whereas **the apical oxygen appears in the outermost layer of the LNO**. The former may have **larger electrostatic attraction with Li ions**, accounting for the Li adsorption behavior on the LCO interface. **This simple analysis of the outermost layer can be useful for estimation of the interfacial stability.**"*

---

### 3e. 전자상태 — PDOS (`Fig. 3` ✅ 실독, `Fig. S7` ✅ 실독, `Fig. S3` 안 봄)

`Fig. 3` 공통: **가로축 = 에너지(eV), 원점 = 점유상태(가전자대) 꼭대기**. 검정 = 총 DOS, 파랑 = LCO 원자, 초록 = LNO, 주황 = LPS, **검정 점선 = LNO/LPS 슬랩을 마주한 첫 번째 LCO 층**. 세로축은 "Density of states" 로 **눈금 없음**.

#### (a) LCO(110)/LNO(1̄0) — 범위 −2 … +2 eV
- LCO(파랑)가 VB 꼭대기를 지배.
- **LNO(초록) 점유상태 꼭대기가 LCO VBM 보다 아래** — 본문 *"lower … by about 1 eV"*, **`figure-read ≈ −0.9 eV`** (초록이 0 으로 떨어지는 지점).
- **+0.75 … +1.1 eV 에 고립된 중갭 봉우리** (`figure-read ≈`). 본문: **진공을 마주한 LCO(110) 표면**에서 온 것이고 고립 슬랩 PDOS(`Fig. S3`)에도 나온다. 기원 = **3d 궤도의 결정장 갈라짐** — *"A pseudotetrahedral crystal field breaks the degeneracy of both t₂g and e_g"* (ref 42 = Qian 2012).
- ⭐ **점선(계면 첫 LCO 층)은 그 중갭 영역에서 ≈0 이다** ✅ (실독 확인). 본문 해석: **CoO₆ 팔면체가 재형성돼 표면상태가 사라졌다** ⇒ *"crystal structures are smoothly connected at the interface."*
- LCO 가 p-형 반도체(ref 43)이므로 **LNO 는 좋은 전자 절연체로 보인다.**

#### (b) LCO(110)/LPS(010) — 범위 −2 … +2 eV
- **중갭 상태에 계면 LCO 가 들어 있다** — 점선이 **+0.55 … +0.95 eV 에서 분명히 솟는다** (`figure-read ≈`) ✅. (a)와 정반대.
- LPS(주황) 가전자대 꼭대기 **`figure-read ≈ −0.7 eV`**.
- **총 DOS 가 0 인 창이 `figure-read ≈ +0.05 … +0.35 eV` 뿐**이다 ⇒ **계면의 실효 갭이 ≈0.3 eV 로 무너져 있다**(그 위는 중갭 상태). 논문은 이 수를 말하지 않는다.
- 본문 기전: **Co 3d 가 S 또는 Li 과 상호작용** — *"the 3d orbitals **near the rather negative S ions shift upward**, while those **near the positive Li ions are stabilized**"* ⇒ 중갭 상태가 에너지적으로 **퍼진다(delocalization in energy)** ⇒ 저자는 이를 **"무질서의 징표"** 로 읽는다.
- **`Fig. S7` 실독 ✅**: **VBM(a)·CBM(b) 둘 다 계면 CoO₂ 층의 Co 에 국소화된 로브**다(노랑/청록 등가면). VBM 은 Co–O 와 인접 S 쪽으로, CBM 은 Co 와 인접 Li/S 쪽으로 뻗는다. ⇒ **계면이 점유·비점유 Co 3d 준위를 갭 안에 동시에 만든다.**

#### (c) LNO(1̄0)/LPS(010) — 범위 −4 … +4 eV (다른 두 패널보다 2배 넓다)
- LNO·LPS 각각의 PDOS 가 **고립 슬랩의 것과 거의 동일** ⇒ 원자·전자 구조가 거의 안 변한다. 결합은 **O–Li, Li–S 이온성**.
- **가전자대 오프셋: LPS 가 LNO 보다 위** — 본문은 부호만 말하고 값을 안 준다. **`figure-read ≈ 1.6 eV`** (초록이 0 으로 떨어지는 지점 −1.6 eV, 주황 꼭대기 0).
- 총 DOS 전도대 개시 **`figure-read ≈ +1.0 … +1.2 eV`**.
- 결론: **LNO 는 LPS 에 대해서도 전자 장벽**이다.

> ⚠ **LCO(110)/LNO(110) 계면의 PDOS 는 논문 어디에도 없다.** 본문은 *"shows almost the same PDOS"* 라고만 한다 (§10-⑦).

---

### 3f. ⭐ Li 공공 형성에너지 — **SCL 의 유일한 정량 지표** (`Table 1`, `Fig. 4` ✅ 실독)

**정의 (본문 식 1)**: `E_v(Li_i) = { E_tot(Li_i 없음) + μ_Li } − E_tot(완전체)`, **μ_Li = Li 금속**.
⇒ **eV 값이 그대로 Li/Li⁺ 기준 전압(V)으로 읽힌다** (중성 셀, 전자는 셀 안에 남는다).

**벌크 기준값** (본문): **LCO 4.0 · LNO 5.1 · LPS 3.2 eV** — *"in good agreement with the values in the previous DFT calculations"* (refs 44 Koyama 2012, 45 **Lepley 2013**, 46 Li 2007).

**자리 라벨** (`Fig. 4` 실독 ✅): `LC`=LCO 유래, `LN`=LNO 유래, `LP`=LPS 유래. 번호가 클수록 대체로 계면에 가깝거나 특수 환경.
- `Fig. 4`b(LCO/LPS)에서 **LP1 은 CoO₂ 층 끝(산소 능선) 바로 위**, **LP4 는 아래쪽 CoO₂ 층에 붙어** 있다 — 둘 다 **흡착 자리**. LP5·LP6 은 **연두색 LiS₄ 사면체 안**(골격 자리).
- 본문 분류(ref 28 Maruyama): **LP1–3 = 이동성(mobile) 자리** · **LP4–6 = LPS 골격 사면체의 비이동(immobile) 자리**.

| 계면 | LC1 | LC2 | LC3 | LN1 | LN2 | LN3 | LP1 | LP2 | LP3 | LP4 | LP5 | LP6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **LCO(110)/LNO(1̄0)** | 3.84 | 3.60 | 3.59 | 3.53 | 3.85 | 3.86 | — | — | — | — | — | — |
| **LCO(110)/LPS(010)** | 3.49 | 3.98 | **3.18** | — | — | — | 3.27 | **1.44** | 3.03 | 2.90 | 2.71 | 2.62 |
| **LNO(1̄0)/LPS(010)** | — | — | — | 3.13 | 3.32 | 3.26 | 2.90 | **2.42** | 3.18 | 2.99 | 3.07 | 3.14 |

**본문 해석 (전수)**
- **LCO/LNO** — LCO 쪽 3.59–3.84 로 **벌크 LCO(4.0) 근처**. 가장자리 자리가 조금 낮은 것은 **변형된 LiO₆ 팔면체** 탓. ⭐ **LNO 쪽은 벌크 LNO(5.1) 대비 1.2 eV 이상 낮다** — 원인은 **밴드 오프셋**이다: *"In the bulk LNO, the electron extracted with Li vacancy formation locates at the valence band top of LNO, while **in the LCO/LNO interface, the electron is extracted from the LCO band**. This electron transfer effect makes E_v(Li_LNn) similar to E_v(Li_LCn)."*
- **LCO/LPS** — LC3 가 LC1·LC2 보다 낮은 이유: **Li–O 결합 부족**(LC3 는 `LiO₄` 사면체). **LP2 가 1.44 eV 로 압도적으로 낮다** — *"because the crystal structure is largely deformed here."* **LP1·LP4 는 LCO 에 흡착한 Li 이라 형성에너지가 크다, ca. 3 eV**(실제 3.27 · 2.90) ⇒ **흡착된 Li 이 LPS 차표면의 Li 보다 안정하다.**
- **LNO/LPS** — LPS 쪽 2.9–3.2 로 **벌크 LPS(3.2) 를 거의 회복**(LP2 제외). *"Since the LNO/LPS interface keeps the bulk crystal structure, significant decrease … does not occur."* LNO 쪽 3.13–3.32 는 **LCO/LNO 와 같은 밴드 오프셋 기원**.

> 🔧 ***우리 산수* — 벌크 대비 낙폭으로 다시 쓰면 "버퍼 효과" 가 숫자가 된다** (논문 미보고)
>
> | 지표 (LPS 쪽 6자리) | **LCO/LPS** | **LNO/LPS** | 버퍼가 회복한 양 |
> |---|---|---|---|
> | 최저 E_v (= LP2) | **1.44** eV → 벌크 3.2 대비 **−1.76** | **2.42** eV → **−0.78** | **+0.98 eV** |
> | 평균 E_v (LP1–6) | **2.662** eV → **−0.54** | **2.950** eV → **−0.25** | **+0.29 eV** (낙폭 **54 % 감소**) |
> | 자리 간 편차 (max−min) | **1.83** eV (3.27−1.44) | **0.76** eV (3.18−2.42) | **58 % 감소** |
> | 골격자리 LP4–6 낙폭 | −0.30 / −0.49 / −0.58 | −0.21 / −0.13 / **−0.06** | 거의 벌크 |
>
> ⇒ **"버퍼가 SCL 을 억제한다" 를 이 세 줄로 정량화할 수 있다.** 특히 **자리 간 편차 1.83 → 0.76 eV** 가 곧 *"충전 초기 전압 기울기의 폭"* 이다 — 저자가 말로만 한 것을 숫자로 옮긴 것.
> (LNO 쪽 낙폭: LCO/LNO 에서 −1.57/−1.25/−1.24, LNO/LPS 에서 −1.97/−1.78/−1.84 — **버퍼 자신은 늘 크게 낮아진다**. 이것은 SCL 이 아니라 **밴드 오프셋 인공물**이므로 혼동하면 안 된다.)

---

### 3g. Li 전달(transfer) 에너지 — **NEB 가 아니다**

논문이 계산한 "Li 이동" 은 **끝점 총에너지 차 2개**가 전부다. **배리어·saddle·경로 0개. NEB 0회.**

| 계 | 이동 | 값 | 방법 |
|---|---|---|---|
| **LCO/LPS** | **LP2 → LP1 이웃의 흡착 자리** | **−1.6 eV** | 기하 이완 포함한 두 끝점의 총에너지 차 |
| **LNO/LPS** | **LP2 → LNO·LPS 슬랩 사이 빈 공간** | **−0.3 eV** (이득) | 같음 |

추가 정성 실험 하나: **Li 간극자(interstitial)** 를 LC1·LC2·LC3 로 둘러싸인 공간에 넣고 이완 → **추가 Li 이 주변 Li 을 밀어내고 LC3 의 Li 이 LCO 계면 흡착 자리로 이동**한다. ⇒ *"the Li adsorption sites are more stable than the interstitial sites in the bulk LPS and LCO."*

Li 수송 **경로** 논의는 **전부 문헌 인용**이다 (이 논문에서 계산한 것이 아니다):
- 고전도 황화물(**LGPS** refs 51 Mo 2011, 52 Xu 2011; **Li₇P₃S₁₁** ref 53 Lepley 2012)은 **1차원 Li 경로**를 공유 ⇒ **결함·불순물 병목에 쉽게 막힌다.** ⇒ **LCO 에 흡착한 Li 이 바로 그 방해물**이 될 수 있다.
- 벌크 **LNO 는 육방 대칭에서 오는 ⟨22̄1⟩ 6등가 방향의 Li-공공 이동 경로**를 갖는다 (refs 54 Xu 2010, 55 Rahn 2013) ⇒ **3차원 다중 경로라 병목을 우회**한다.
- ⚠ 저자 스스로 단 단서: *"the **diffusion barrier itself in the oxide buffer layers is usually high**, and thus the resistance increases when the buffer thickness grows over a critical value."* — **버퍼는 얇아야 한다**는 뜻인데, 이 논문은 그 임계 두께를 계산하지 않는다.

---

### 3h. SCL 논증 (`Fig. 5` ✅ 실독 — **축 라벨이 없다**)

**`Fig. 5` 실독 기록**: 6패널 전부 **세로축 = "계면 Li 농도"(라벨·눈금·단위 없음)**, **가로축 = 위치(라벨 없음)**. 파랑=LCO, 초록=LNO, 주황=LPS 색면 + 검은 곡선. 회색 점선 = 각 벌크 기준 농도.

| 패널 | 무엇 | 실독한 모양 |
|---|---|---|
| **(a)** 기존 모형 · 평형 · LCO\|LPS | Maier 류 이온 재분배 (ref 47) | LCO 쪽이 계면으로 갈수록 **위로**, LPS 쪽은 계면에서 **아래로** 떨어졌다가 벌크로 서서히 회복 |
| **(b)** 기존 모형 · 평형 · LCO\|LNO\|LPS | 절연 버퍼라 재분배 량이 작다 | LCO·LNO 거의 평탄, LPS 쪽만 계면에서 약간 아래 |
| **(c)** **이 논문** · 평형 · LCO\|LPS | ⭐ **경계 바로 위에 뾰족한 Li 스파이크**(=흡착층) + 그 **뒤로 급격한 고갈**, 짧은 거리에서 회복. **LCO 쪽은 평탄** | 기존 모형과 모양이 다르다 — 재분배가 아니라 **표면 흡착**이 SCL 의 본체 |
| **(d)** **이 논문** · 평형 · LCO\|LNO\|LPS | LCO·LNO **완전 평탄**, LNO\|LPS 경계에서만 **작은 딥 + 작은 봉우리** | 버퍼가 SCL 을 거의 없앤다 |
| **(e)** **이 논문** · 충전 초기 · LCO\|LPS | 점선 = 평형, 실선 = 충전 초기. **LCO 전체 농도가 내려가고**, **흡착 스파이크는 더 커지며**, **LPS 고갈이 깊어지고 더 멀리 퍼진다** | = SCL **성장** |
| **(f)** **이 논문** · 충전 초기 · LCO\|LNO\|LPS | 변화가 훨씬 완만, LNO\|LPS 딥만 약간 | = SCL 성장 **억제** |

**본문 논증 사슬**
1. `E_v` 를 **Li 화학퍼텐셜**로 읽는다.
2. **평형**: 황화물의 Li 화학퍼텐셜이 낮으므로 고전 모형은 LPS→LCO 재분배를 예측(a). **우리 계산은 그것을 *표면 흡착*으로 구체화한다**(c). 선행 개념: **Uvarov 의 Stern 모형 기반 이온염 계면 공간전하**(ref 50) — *"The SCL distribution is concentrated in the interface region and similar to our Li-ion concentration."*
3. **충전 초기**: LCO/LPS 의 `E_v` 범위가 **1.5 – 4.0 eV**. *"**The former energy coincides with the experimental voltage where the charging is initiated.**"* ⇒ 그 전압 부근에서 **LP2 의 Li 이 벌크 LPS 로 빠지면서 전자를 양극에 넘긴다** ⇒ **황화물 쪽 SCL 이 커진다** ⇒ **충전 초기 전압 프로파일의 기울기**가 그것이다 (refs 5, 8–10, 13, 14).
4. **버퍼 있을 때**: `Table 1` 이 말하길 LCO·LNO 양쪽의 Li 이 **LCO 의 Li 화학퍼텐셜(= 플래토 전압)** 부근에서 함께 빠지기 시작한다. LNO/LPS 에서는 LP2 가 LP1·LN3 보다 각각 **0.5 / 0.8 eV** 낮지만 (실측 0.48 / 0.84), **LCO/LPS 보다 작다** ⇒ **기울기 억제.**
5. ⚠ **한계 자인**: *"the present supercell calculations well describe the nanoscale region in the interface, although **long-range variation of the concentration needs to be analyzed by methods involving the long-range electrostatic interaction**."*

> ⛔ **따라서 이 논문에서 회수할 수 있는 SCL 수치는 다음뿐이다.**
> · **두께**: **없음** (nm 로 적힌 값이 한 개도 없다). 굳이 말하면 **계산 셀의 LPS 쪽 ≈1.7 nm 안에서 일어나는 일**만 본 것이다.
> · **크기(eV)**: **자리별 E_v** 21개와 **끝점 전달에너지** 2개. **전위(V) 프로파일·전하(e) 적분·Debye 길이 = 전부 없음.**

---

## 4. DFT/계산 방법 ★ — 전수

| 항목 | 값 (원문) |
|---|---|
| **code** | **QUANTUM ESPRESSO** (ref 31 = Giannozzi 2009). 버전 미기재 |
| **기저** | 평면파 + 유사퍼텐셜 |
| **functional** | **PBE** (ref 32). **vdW 보정 없음** |
| **스핀** | ⚠ **spin-unpolarized** (자세한 근거는 아래) |
| **pseudo** | **ultrasoft** (refs 33 Vanderbilt 1990, 34 Rappe 1990). **가전자 배치**: Li `1s²2s¹` · O `2s²2p⁴` · P `3s²3p³`+**NCC** · S `3s²3p⁴`+NCC · Co `3d⁸4s¹`+NCC · Nb `4s²4p⁶4d⁴5s¹`+NCC (NCC = nonlinear core correction, ref 35) |
| **DFT+U** | **Anisimov 류**(ref 36). **U(Co 3d) = 5.9 eV** (refs 37 Juhin 2010, 38 Mattioli 2013). *"essential to describe the electronic properties of LCO"* (ref 39). ⚠ **Nb 4d 에는 U 없음** |
| **ecut** | **40 Ry** (파동함수 smooth part) / **320 Ry** (augmented charge) |
| **k-points** | **벌크**: LCO 8×8×4 · LNO 8×8×4 · LPS 4×6×8. **표면**(면 평행만): LCO(110) 8×4×1 · LNO(1̄0) 8×4×1 · LNO(110) 4×4×1 · LPS(010) 4×8×1. ⚠ **계면: Γ 점 하나만** |
| **PDOS** | **nscf** — **2×1×1**(LCO/LPS, LNO/LPS) · **2×2×1**(LCO/LNO), **Γ점 전자밀도를 써서** |
| **수렴** | 힘 **< 0.001 Ry/bohr** (*우리 산수* = **0.0257 eV/Å**) · 응력 **< 0.5 kbar** |
| **스미어링** | **Gaussian, 0.001 Ry** (*우리 산수* = 13.6 meV). ⚠ 후속 2017 편은 **0.01 Ry** 로 10배 크다 |
| **전하** | **항상 중성 셀** (결함 계산 포함). 결함 계산 시 **셀 파라미터는 무결함 계면의 이완값에 고정** |
| **쌍극자/정전 보정** | ⚠ **쌍극자 보정(dipole correction) 안 씀.** 대신 **ESM 법**(refs 40 Otani & Sugino 2006, 41 Hamada 2009)으로 분극 효과를 **점검만** 했다: *"Maximum differences of the total and the formation energies between the periodic boundary condition and the non-repeated slab approach are about **0.1 and 0.01 eV**"* ⇒ PBC 로 진행 |
| **supercell / nat** | ⛔ **nat 미기재.** 계면 횡방향 셀만 `Table S3`. 법선 셀 길이 미기재. (*우리 산수* 추정 §3c-4) |
| **무질서 처리** | ⭐ **LPS 의 Li 부분점유를 Lepley 의 `β-Li₃PS₄-b` 정렬모형(4c 자리 Li 제거)으로 대체.** **SQS·enumerate·앙상블 전부 아님 — 단일 배열 1개** |
| **AIMD** | ⛔ **0회** |
| **MLIP** | ⛔ **0회** |
| **NEB** | ⛔ **0회** |
| **시각화** | **VESTA** (ref 30 Momma & Izumi 2008) |
| **계산자원** | NIMS · 九州大 · ISSP · **東大 ITC Oakleaf-FX** (SPIRE/CMSI) |

**스핀 판정의 원문 (그대로)**
> *"We also examined the spin polarization of LCO surfaces. A previous study reported stabilization of spin-polarized states on the LCO surfaces due to the missing Co−O bonds (ref 42). **Our calculations reproduce this tendency.** However, we have investigated the Li passivation of the LCO(110) with and without spin polarization and found that **the energy difference among the low, intermediate, and high spin states are within 0.2 eV**. Thus, **we limit the present discussion to the spin-unpolarized case.** The argument about the spin states will be reported elsewhere."*

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | **표면 4종의 측면 구조** — LCO(110)/LNO(1̄0)/LNO(110)/LPS(010). 화살표가 각 면의 법선 방향. LCO(110)은 CoO₂ 층(파랑)이 **수직 3장**, 그 사이에 Li 기둥 | ⭐ **LCO(110)의 정체 확인** — CoO₆ 를 옆에서 자른 면이라 **산소 능선이 노출**된다. 우리 NCM 슬랩이 어느 면인지 다시 볼 때의 대조군 |
| 2 | **완화된 계면 4종**(측면). (a,b) LCO\|LNO 는 매끄럽게 붙고 **(a)는 LCO 층이 사선으로 기울어 있다**; **(c) LCO\|LPS 는 인셋에서 `CoO₄S` 오면체가 보이고 LPS 가 무질서**; (d) LNO\|LPS 는 간격이 뚜렷하고 양쪽 다 결정성 유지 | ⭐ **우리 v5 계면 xyz 와 눈으로 대조할 1순위 그림.** "황화물이 산화물에 닿으면 표면 1–2 nm 가 비정질화한다" 의 시각 증거 |
| 3 | **계면 3종의 PDOS**(원점 = VB 꼭대기). **점선 = 계면 첫 LCO 층**이 핵심 — (a)에선 중갭에 0, **(b)에선 중갭에 존재** | ⭐ 축 D(전자구조). **버퍼 유무로 계면 중갭 상태가 켜지고 꺼진다.** 값: LNO 오프셋 `figure-read ≈ −0.9 eV`(a) · LPS/LNO VBO `figure-read ≈ 1.6 eV`(c) · LCO\|LPS 실효갭 `figure-read ≈ 0.3 eV`(b) |
| 4 | **Li 자리 인덱스**(LC1–3 / LN1–3 / LP1–6) — `Table 1` 을 읽는 열쇠 | **LP1·LP4 가 흡착 자리**, **LP5·LP6 은 LiS₄ 골격 자리**임을 눈으로 확인. 우리 계면 Li 분류 체계의 선례 |
| 5 | **SCL 개념도 6패널** — 기존 모형(a,b) vs 이 논문(c,d), 평형 vs 충전초기(e,f) | ⚠ **축 라벨·눈금·단위가 하나도 없다.** 서사용으로만 쓰고 **정량 근거로 인용 금지** (§10-①) |
| S2 | **고립 슬랩 4종의 완화 구조**(3뷰: 법선-a, 법선-b, 단면) | **종단 확인용.** LCO(110)은 Li 행–CoO₂ 층 교대, LPS(010)은 PS₄ 망 |
| S4 | **초기 계면 4종 + 두 면의 단면 + 표면 원시벡터**(점선 화살표) | ⭐ **정합 규약의 시각 증거** — `LCO[001] ∥ LNO[001] ∥ LPS[100]` 이 화살표로 확인된다. 우리 정합 기록에 그대로 옮길 수 있는 서술 |
| S6 | **완화된 계면 4종을 2뷰(a-c, b-c)로** — `Fig. 2` 보다 정보가 많다 | ⭐ **여기서 층수를 셌다.** 진공을 자로 삼아 LCO ≈8층(11.5 Å), LPS ≈2 셀(16.7 Å), 셀 전장 ≈43 Å (*우리 산수*, §3c-4) |
| S7 | **LCO(110)/LPS(010)의 VBM·CBM 분자궤도** 등가면(측면·정면) | ⭐ **VBM·CBM 둘 다 계면 Co 3d 에 국소화**돼 있다 ⇒ 저자는 "무질서" 로만 읽지만 **전자 누설 경로 후보**로 읽을 수 있다 (§8-③) |
| S1 | 벌크 단위셀 3종 (안 봄 — 셀 조성·k 격자가 SI 활자에 있다) | — |
| S3 | 고립 슬랩 4종의 PDOS (안 봄 — 갭은 `Table S2` 활자) | 캡션이 *"the 1st and 8th layer"* 라 한 것이 **LCO 8층의 유일한 단서** |
| S5 | 횡방향 미끄럼 표본 도식 16/4/9 + LCO/LPS 초주기 (안 봄 — 개수가 SI 활자) | LCO/LPS 가 4개로 줄어든 이유(초주기)의 근거 그림 |
| Table 1 | Li 공공 형성에너지 21개 (텍스트 전사, §3f) | ⭐ **SCL 의 유일한 정량 지표** |
| Table S1 | 벌크 격자·갭 계산 vs 실험 (전사, §3a) | 격자 오차 ±1.3 % 확인 |
| Table S2 | 표면 셀·표면에너지·갭 (전사, §3b) | γ 정성 앵커 (LCO 14.08 vs LPS 1.94 eV/nm²) |
| Table S3 | **미스핏·계면 셀·부착에너지** (전사, §3c-2) | ⭐⭐ **기하 원전의 본체** |
| Table S4 | 횡방향 표본 상대에너지 (전사, §3c-5) | ⚠ 표본 폭 6–9 eV, LCO/LPS 는 4개뿐 |

---

## 6. Post-processing ★

- **무엇을 했나**
  1. **표면에너지** `W_surf = (E_slab − n·E_bulk)/2S` — 4개 면.
  2. **부착에너지** `W_ad = (E_A + E_B − E_{A/B})/S` — 4개 계면.
  3. **미스핏** `μ = 1 − 2S_{A∩B}/(S_A+S_B)` — 면적 정의.
  4. **PDOS** (nscf, 원자군별 투영: LCO 전체 / LNO 전체 / LPS 전체 / **계면 첫 LCO 층**).
  5. **Li 공공 형성에너지** (중성 셀, μ_Li = Li 금속) — **21개 자리**.
  6. **Li 전달 에너지** — 끝점 2쌍.
  7. **분자궤도 등가면** (VBM·CBM) 시각화.
  8. **ESM 대조** — PBC vs 비반복 슬랩의 총·형성에너지 차이 점검 (0.1 / 0.01 eV).
- **도구**: **VESTA**(구조·궤도 시각화). pymatgen·LOBSTER·Bader·VASPKIT **전부 미사용**(2014년 논문).
- **수치화·기록 방식**: `Table 1`(본문) + `Table S1`–`S4`(SI) 에 **표로** 준다. **원시 총에너지는 공개하지 않는다** (⚠ 2017 편은 `Table S3` 로 벌크 결함 총에너지 9개를 Ry 단위로 줘서 우리가 재현할 수 있었는데, **2014 편에는 그 자료가 없다** ⇒ **이 논문의 값은 재현 검산이 불가능**하다).
- ⛔ **안 한 것**: NEB · AIMD · MD · COHP/ICOHP · Bader · ELF · BVSE · grand-potential ESW · 포논 · 탄성 · 전위(전기) 프로파일 · 층별 전하적분 · Debye 길이.

---

## 7. 우리 대비

### 7a. ⭐⭐ **우리 v5 계면 기하와 대조할 항목** — *판정하지 않고 나란히만 둔다*

> 사용자 지시대로 **같다/다르다 판정은 하지 않았다.** 원문 값과 우리 기록을 **같은 줄에 올려 두기만** 한다.
> 우리 쪽 출처: `kb/results/adhesion_v5_full_report.md` · `db/properties/adhesion.json` · `db/literature/refs.json[37]`.

| # | 대조 항목 | **[Haru14] 원문** | **우리 v5 (현재 기록)** | 비고 |
|---|---|---|---|---|
| 1 | **계면 형식** | **단일 계면 + 진공** (샌드위치 명시적 반대) | **단일 계면 + 진공** | `refs.json[37]` 가 "동일" 로 기록 |
| 2 | **진공 두께** | **≈1.5 nm (15 Å)** | **30 Å** (UMA vacuum-sensitivity 때문 — 60 Å 에서 W_ad 10× 폭주) | 값이 다름 |
| 3 | **산화물 면지수** | **LCO (110)** (저자 스스로 (104)가 더 안정하다고 인용) | v5 보고서에 **면지수 미기재**. v26/v27 은 LiNiO₂ **(003)/(110)/(012)/(104)** 를 방법독립성 시험에 씀 | ⚠ **우리 v5 의 면지수를 원장에서 확인할 것** |
| 4 | **SE 면지수** | **β-Li₃PS₄ (010)** (Li 전도축 b 가 법선) | LPSCl **cubic 2×2×3** — **면지수 미기재** | ⚠ 같은 항목 |
| 5 | **종단** | **화학양론 종단**. LNO 는 활자 명시(`−Li₂−Nb₂−O₆` / `Li₆Nb₆−O₉`), **LCO·LPS 는 미기재** | v5 보고서에 **종단 기술 없음** | 양쪽 다 공백 |
| 6 | **격자 정합 방법** | **탄성계수가 큰 쪽(LCO)에 맞춘다**. LNO/LPS 만 **두 격자의 평균** | **SE 를 NCM 에 맞춘다**(SE strained) | 규약 방향 |
| 7 | **정합 배수** | **LCO 5×1 vs LPS 1×4** (*우리 산수*) | **SE 2×2×3(624원자) + NCM 7×7×1(196원자)** (Li6 계열) | — |
| 8 | **미스핏 / 변형** | μ **3.7 %**(면적 정의) · **실제 선형변형 LPS +6.2 %** (*우리 산수*) | **strain +0.2 %**(comp1/2B) · **+1.1 %**(comp3/4/5) | 정의가 다르다 |
| 9 | **슬랩 두께** | **각 1–2 nm**. LCO ≈**8층 / 1.13 nm**, LPS ≈**2 셀 / 1.66 nm** (*우리 산수*) | SE **30 Å**, NCM 7×7×1 (두께 미기재) | — |
| 10 | **총 원자 수** | ⛔ **미기재** (*우리 산수* ≈ **736**) | **820** (624 + 196) | — |
| 11 | **법선 셀 길이** | ⛔ **미기재** (*우리 산수* ≈ **43 Å**) | `cell_z = atoms_max + 30 Å` | — |
| 12 | **횡방향 샘플링** | **계통적 lateral slide** — 16 / **4** / 9 표본, 전부 이완 후 최저 채택. 표본 폭 **최대 9.07 eV** | **xy-shift 샘플링** (z-shift 는 슬랩 절단 때문에 폐기) | **발상이 같다** |
| 13 | **이완 자유도** | **전 원자 + 횡방향 셀 파라미터 자유.** FixAtoms 없음 | **하단 33 % FixAtoms 고정** (UMA 안정화용) | `refs.json[37]` 가 이미 "우리만의 추가" 로 기록 |
| 14 | **초기 간격** | ⛔ 미기재 | **gap 2.5 Å** | — |
| 15 | **힘 수렴** | **0.001 Ry/bohr = 0.0257 eV/Å** | **fmax 0.01 eV/Å** (LBFGS, 200 steps) | — |
| 16 | **응력 수렴** | **0.5 kbar** | n/a (셀 고정) | — |
| 17 | **힘 계산기** | **DFT+U** (QE · PBE · USPP · U(Co)=5.9 eV · **Γ-only**) | **UMA-s-1p1 (MLIP)** | ⭐ **여기가 제일 큰 차이** |
| 18 | **W_ad 식** | `(E_A + E_B − E_AB)/S` | **동일** | ✅ |
| 19 | **W_ad 값** | LCO\|LPS **4.3 eV/nm² = 0.689 J/m²**; LNO\|LPS 3.8 = 0.609; LCO\|LNO(1̄0) 10.6 = 1.698 | comp1 LiNiO₂\|LPSCl **≈1.25 J/m²** (v5_working) | ⚠ 소환값 — **방법·물질 둘 다 다르다** |
| 20 | **표면에너지 γ** | LPS(010) **1.94 eV/nm² = 0.311 J/m²** (DFT+U); LCO(110) 14.08 = 2.256 | comp1 γ_SE **1.211 J/m²** (UMA, `adhesion.json`) | ⚠ 우리 γ 는 정본 등록 없음(`canonical_registry` 밖) |
| 21 | **변형에너지 상쇄** | ⛔ **불명** — `E_A`·`E_B` 가 변형된 셀인지 원래 셀인지 안 적음 | v5 보고서가 **스스로 이 함정을 기록**해 둠 (method_A 의 "STRAIN ARTIFACT ~30 eV") | ⭐ **같은 함정, 우리는 알고 있고 저쪽은 안 밝혔다** |
| 22 | **SCL 정량** | ⛔ **없음** (두께·전위·Debye 전부) | ⛔ **없음** — `computational_methods_canonical.md` §2 가 **경계로 선언** | ✅ **우리 경계 선언이 문헌으로 지지된다** |

### 7b. `our_dft_baseline.md` 대비 (물성 축)

| 항목 | **[Haru14]** | **우리 (comp1 / modelc)** | 차이 / 이유 |
|---|---|---|---|
| **Band gap (황화물)** | **β-Li₃PS₄ 벌크 2.8 eV** · **LPS(010) 슬랩 2.6 eV** (PBE+U, U 는 Co 에만 ⇒ LPS 는 사실상 PBE) | **Li₆PS₅Cl 2.066 / Li₅.₄PS₄.₄Cl₁.₆ 2.099 eV** (PBE, **fixed-occ nscf 고유값**) | ⛔ **숫자 비교 금지.** ① **물질이 다르다**(β-LPS 는 free S²⁻·Cl⁻ 가 없다) ② **판독법이 안 적혀 있다** ③ PBE 과소평가·무질서 민감. **"둘 다 wide-gap 절연체"** 까지만 |
| **Ea / σ / D** | ⛔ **없음** (NEB·MD 0회). 인용된 실험값 하나: 나노다공성 LPS **1.64×10⁻⁴ S/cm @RT** (ref 21 Liu 2013) — **이 논문의 계산값이 아니다** | Ea 0.253 / 0.224 eV, D(600 K) 3.09 / 7.90 ×10⁻⁶ cm²/s (MLIP-MD) | **대조 불가** |
| **산화 onset / ESW** | ⛔ **없음** (grand-potential 0회) | 2.256 V (S²⁻-limited) | **대조 불가** |
| **기계적 (E/B/G)** | ⛔ **없음.** 정성 언급만: *"high elastic modulus of LCO"*(정합 방향의 근거) · *"sulfide is soft enough"*(미스핏이 문제 안 되는 이유) | comp1 E_VRH 22.06 / modelc 27.66 GPa | **대조 불가** — 다만 *"황화물이 무르다"* 는 정성 서술은 우리 값과 같은 방향 |
| **표면·계면 (γ, W_ad)** | **γ_LPS(010) 0.311 J/m²** · **W_ad(LCO\|LPS) 0.689 J/m²** | γ_SE(comp1) 1.211 J/m² (UMA) · W_ad ≈1.25 J/m² (UMA) | ⚠ 물질·방법 둘 다 다름. **순위·방향만**, 절대값 비교 금지 |
| **Li 공공 형성에너지** | **벌크 LPS 3.2 eV**, 계면 최저 **1.44 eV** | 우리 원장에 **β-LPS 대응값 없음** | ⭐ **우리가 안 가진 축** — 계면 Li 자리별 E_v 는 우리 계에서 아직 계산한 적 없다 (§8-①) |

### 7c. ⭐ **우리 방법론 경계 선언의 외부 증거**

`kb/methodology/computational_methods_canonical.md` §2 말미:
> *"현재 명시적 경계 3개 — K_IC · μm 급 입자 역학 · **공간전하층 정량(두께·전위·Debye 길이 — 문헌도 정성뿐이라 '계산했다'고 말할 수 없다)**."*

**이 논문이 그 선언의 실물 증거다.** SCL 을 최초로 원자단위 계산한 논문이, 10년 뒤까지 인용되는 그 논문이, **두께도 전위도 한 번도 내지 않았다.** ⇒ *"문헌도 정성뿐"* 은 추측이 아니라 **확인된 사실**로 격상할 수 있다.

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

① ⭐ **우리 계면에서 "자리별 Li 공공 형성에너지" 를 아직 한 번도 안 냈다 — 이게 제일 싼 공백 메우기다.**
   이 논문의 지표는 **E_v(자리) 하나**뿐인데도 SCL 서사 전체를 떠받친다. 우리 v5 LiNiO₂|LPSCl 계면 구조는 **이미 있다**. 거기서 **계면 근처 Li 자리 6–10개의 중성 공공 형성에너지**(μ_Li = Li 금속)를 QE 로 뽑으면 **곧바로 같은 축의 값이 나온다**. 보고량 카드로 미리 정의해야 할 것: ⓐ **자리 선택 규칙**(무질서 배열이라 등가자리가 없다 — 앙상블/최저/분포 중 무엇인가) ⓑ **전자가 어디로 가는가**(중성 셀이면 밴드정렬이 값을 정한다 — 이 논문이 LNO 에서 보인 그대로) ⓒ **셀 크기 수렴**.
   ⚠ 이 논문이 쓴 정의를 그대로 쓰면 **아지로다이트의 free S²⁻ 자리 · Cl⁻ 자리 · 무질서 배열**에서 "자리" 가 유일하지 않다 ⇒ **스칼라 보고량이 정의되지 않는다**(우리 보고량 규율의 위험신호 그대로). **분포로 보고**하는 설계가 맞다.

② ⭐ **"능선 산소 vs 꼭짓점 산소" 는 우리 NCM 면 선택에 바로 쓰이는 판정 기준이다.**
   저자의 주장은 화학이 아니라 **기하**다 — *최외곽층이 두 O 를 잇는 능선을 내밀면 Li 을 세게 당기고, 꼭짓점 O 면 안 당긴다.* 우리 v26/v27 이 이미 **(003)/(110)/(012)/(104)** 를 놓고 Cl–O 상관을 봤는데, **그 면들이 능선형인지 꼭짓점형인지로 한 번 분류**해 보면 `R_Li–O` 의 면 의존성(부호가 뒤집힌 그 건)이 설명될 가능성이 있다. **계산 없이 구조만 보고 할 수 있는 분석이다.**

③ **계면 중갭 Co 3d 상태 = 우리 축 D 의 확장 지점.**
   `Fig. 3`b + `Fig. S7` 은 **LCO|LPS 계면이 갭 안에 점유·비점유 Co 3d 를 동시에 만든다**는 것을 보인다. 저자는 이를 "무질서" 로만 읽고 지나가지만, **전자가 흐르면 SE 가 계속 분해된다**(우리 B 축의 핵심 우려). 우리는 LiNiO₂|LPSCl 계면 PDOS 를 낸 적이 없다 ⇒ **Ni 3d 가 같은 일을 하는지**가 열린 질문이고, 이것은 **W_ad 보다 논문 기여도가 높은 축**일 수 있다.
   ⚠ 단 **spin-unpolarized · PBE+U 로 국소 3d 준위를 논하는 것 자체가 취약**하다(§10-⑤) — 우리가 한다면 **스핀 자유 + 상태선택 정책 선언**이 전제다.

④ **버퍼층 서사의 정량 고리를 우리가 만들 수 있다.**
   *우리 산수* 로 뽑은 **"LPS 쪽 자리 간 E_v 편차 1.83 → 0.76 eV (58 % 감소)"** 는 논문에 없는 수다. 우리 LiNbO₃/Li₂ZrO₃ 코팅 캠페인이 열리면 **"코팅의 목표는 계면 Li 자리 에너지의 *편차* 를 줄이는 것"** 이라는 **정량 목표함수**로 쓸 수 있다 (평균이 아니라 편차라는 점이 포인트).

⑤ **anti-sandwich 논거는 이미 우리 것이다 — 이제 원문 문장까지 확보했다.**
   §3c-1 의 인용문을 원고 Methods 에 그대로 붙일 수 있다. `refs.json[37]` 이 요약으로 갖고 있던 것을 **원문 검증 완료** 상태로 승격.

---

## 9. 인용 가능 문장 (deck/paper 용)

- "산화물 양극|황화물 전해질 계면의 첫 원자단위 DFT 연구는 **비대칭 이종계면에 대해 샌드위치가 아니라 *단일 계면 + 진공*** 을 써야 한다고 명시적으로 논증했다 [Haruyama *et al.*, *Chem. Mater.* **26**, 4248 (2014)]."
- "LiCoO₂(110)|β-Li₃PS₄(010) 계면에서 전해질 쪽 Li 은 **CoO₆ 팔면체의 산소 능선 위로 흡착**하며, 그 결과 황화물 차표면 Li 자리의 공공 형성에너지가 **벌크 3.2 eV 에서 1.44 eV 로 떨어진다** [같은 문헌]."
- "LiNbO₃ 버퍼를 끼우면 Li 흡착 자리가 사라지고 황화물 쪽 Li 공공 형성에너지가 **2.42–3.18 eV 로 벌크값 부근으로 복귀**한다 [같은 문헌]."
- "계산된 부착에너지는 **LiCoO₂|LiNbO₃(1̄0) 10.6 > LiCoO₂|β-Li₃PS₄ 4.3 > LiNbO₃|β-Li₃PS₄ 3.8 eV/nm²** 순이며, 저자들은 이를 **최외곽 산소의 기하(능선 vs 꼭짓점)** 로 설명한다 [같은 문헌]."
- ⚠ (조건부) "공간전하층의 **두께·전위는 이 문헌에서도 계산되지 않았다** — 정량 지표는 자리별 Li 공공 형성에너지뿐이다." ← **우리 경계 선언을 방어할 때만** 쓴다.
- ⛔ **쓰면 안 되는 문장**: *"Haruyama 가 SCL 두께를 ○ nm 로 계산했다"* · *"SCL 전위가 ○ V 다"* · *"Li 이동 배리어가 ○ eV 다"* — **전부 이 논문에 없다.**

---

## 10. 주의 / 한계 (over-claim 방지) — **비판**

① 🔴 **"공간전하층" 이 제목인데 SCL 이 한 번도 정량되지 않는다.**
   전위 프로파일 0 · 층별 전하적분 0 · 두께(nm) 0 · Debye 길이 0. `Fig. 5` 는 **세로축 라벨도 눈금도 단위도 없는 손그림**이다(실독 확인). 실제로 계산된 것은 **≈1.7 nm 두께 LPS 슬랩 안의 자리별 Li 공공 형성에너지 21개**다. 저자들도 장거리 정전기가 빠졌음을 인정한다. ⇒ **현상 원전이지 정량 원전이 아니다.**

② 🔴 **논문의 정량적 클라이맥스인 "1.44 eV ↔ 실험 충전 개시 전압" 일치 주장에, 그 실험 전압이 적혀 있지 않다.**
   원문은 *"The former energy coincides with the experimental voltage where the charging is initiated"* 로 끝나고 **값도, 그 값이 나오는 문헌의 페이지·그림도 지정하지 않는다** (refs 5, 8–10, 13, 14 를 뭉쳐 인용). **가장 중요한 수치 일치 주장이 검증 불가능하게 제시**돼 있다.

③ 🔴 **LCO 면이 (110) 하나뿐인데, 저자 스스로 (104)가 더 안정하다고 인용한다** (ref 26 = Kramer & Ceder 2009).
   그런데 이 논문의 **핵심 기전(= Li 이 흡착하는 "산소 능선")은 (110) 전용 기하 특징**이다. (104) 는 CoO₆ 를 다른 각도로 자르므로 같은 능선을 같은 방식으로 내밀지 않는다. ⇒ 결론부의 일반화 — *"the current discussion … can be generally applied to the other oxide components such as LiMn₂O₄ and LiFePO₄"* — 는 **면 하나에서 나온 기하 논거를 물질 전체로 확대**한 것이다. **면 의존성이 시험되지 않았다.**

④ 🔴 **결론이 걸린 계면의 표본이 가장 적다.** LCO/LNO 는 16개씩 돌렸는데 **LCO/LPS 는 4개**(초주기 등가성 논거), **LNO/LPS 는 9개 중 3개만** 계산했고 나머지는 *"초기 에너지가 상대적으로 높아서"* 건너뛰었다 — **이완 전 에너지로 이완 후를 판정**한 것이다. 표본 폭이 **6–9 eV** 인 지형에서 4점 표본은 전역최소 탐색이라 부르기 어렵다.

⑤ 🔴 **spin-unpolarized 인데 기전의 주체가 Co 3d 국소준위다.**
   저자는 *"Li passivation 의 저/중/고 스핀 에너지차가 0.2 eV 이내"* 를 근거로 면제했지만, ⓐ 그 시험은 **LCO(110) 표면의 Li passivation** 에서 한 것이고 ⓑ 정작 논문이 기전으로 내세우는 것은 **계면의 CoO₄ 유사사면체와 갭 안 Co 3d 준위**다. 0.2 eV 면제 근거가 **그 준위의 위치·점유에는 적용되지 않는다.** (2017 후속편에도 같은 비판이 남아 있다 — 우리 `haruyama2017` digest §10-①.)

⑥ 🔴 **W_ad 의 변형에너지 상쇄가 불명이고, 실제 선형 변형이 표의 "미스핏" 보다 훨씬 크다.**
   `Table S2`↔`S3` 를 나누면 (*우리 산수*) **LCO/LPS 의 LPS 가 한 축 +6.2 %**, **LNO/LPS 의 LNO 가 −8.4 %** 다. SI 는 `E_A^tot`·`E_B^tot` 를 *"relaxed isolated slabs"* 라고만 쓰는데, 그것이 **변형된 셀**인지 **원래 벌크 셀**인지 밝히지 않는다. 후자면 **변형에너지가 W_ad 에 그대로 섞인다**. 특히 **LNO/LPS(−8.4 %)와 LCO/LPS(−0.7 %)의 W_ad 를 나란히 비교**한 것이 문제다. 게다가 **LNO/LPS 의 a = 12.79 Å 은 논문이 밝힌 초기값(두 벌크 평균 13.545 Å)보다 5.6 % 작다** — 설명이 없다.

⑦ ⚠ **보이지 않은 것을 "거의 같다" 고 단언한다.** LCO(110)/LNO(110) 계면의 PDOS 는 **논문 어디에도 없는데** 본문은 *"shows almost the same PDOS"* 라고 쓴다. `Fig. 3` 은 3패널, `Fig. S3` 은 고립 슬랩이다.

⑧ ⚠ **초록의 "Li migration" 이 오도한다.** 배리어·NEB·MD 0회. 실제 계산은 **끝점 에너지차 2개**(−1.6 / −0.3 eV)와 **간극자 삽입 1회(정성)** 뿐이다. 수송 경로(1D vs 3D) 논의는 **전부 타 문헌 인용**이다.

⑨ ⚠ **재현이 불가능하다.** 총 원자수 · 슬랩 층수 · 법선 셀 길이 · 좌표파일 · **원시 총에너지** 가 전부 없다. 2017 후속편은 `Table S3` 로 벌크 결함 총에너지를 Ry 로 공개해 우리가 검산할 수 있었는데, **2014 편은 검산할 자료가 하나도 없다.** (우리가 §3c-4 에서 한 것은 **그림에서 잰 추정**이지 재현이 아니다.)

⑩ ⚠ **무질서가 단일 배열 하나다.** LPS 는 Lepley 의 `β-Li₃PS₄-b`(4c Li 제거) **정렬모형 1개**. `E_v(LP2) = 1.44 eV` 는 *"결정구조가 크게 변형된"* **그 배열의 그 자리** 값이다. SQS·앙상블·온도 평균이 없으므로 **"1.5 V 에서 충전 개시" 는 단일 배열에서 나온 단일 수**다.

⑪ ⚠ **계면에 Γ 점 하나만 썼다.** 법선 ≈43 Å 이면 그 방향은 Γ 로 충분하지만, **횡방향 13.9 × 24.5 Å** 에서 Γ-only 는 빠듯하다. PDOS 만 2×1×1 nscf 로 보정했고 **총에너지·E_v·W_ad 는 전부 Γ-only 값**이다. `Table 1` 의 자리 간 0.2 eV 급 차이를 논하는 데에 이 수준이 충분한지 **수렴 시험이 제시되지 않았다**.

⑫ ⚠ **E_v 는 순수한 이온 항이 아니다.** 중성 셀이라 **빠진 전자가 어디에 앉느냐가 값을 정한다** — 저자 자신이 LNO 에서 그것을 보였다(벌크 5.1 → 계면 3.5, 전자가 LCO 밴드로 감). ⇒ **"자리별 Li 화학퍼텐셜" 로 읽을 때 밴드정렬 성분과 자리 성분이 섞여 있다.** LNO 쪽 낙폭(−1.2 ~ −2.0 eV)을 "SCL" 로 읽으면 틀린다.

⑬ ⚠ **버퍼 두께의 최적점을 말하면서 계산하지 않는다.** *"resistance increases when the buffer thickness grows over a critical value"* 라고 쓰지만 임계 두께도, LNO 벌크 확산 배리어도 계산하지 않는다 (문헌 인용뿐).

---

## 11. 🔻 불리한 결론 — 따로 적는다

> 사용자 요청대로, **우리에게 유리하지 않은 것**만 모았다.

**① 우리가 "v5 의 1차 근거" 로 써 온 이 논문은, 정작 *재현에 필요한 수를 안 준다*.**
`refs.json[37]` 은 이 논문을 **method-anchor-PRIMARY** 로 등록했고 그 서술은 원문과 맞다. 그러나 **총 원자수 · 슬랩 층수 · 법선 셀 길이 · 좌표 · 원시 에너지가 전부 없다.** ⇒ *"우리 기하는 Haruyama 2014 를 따랐다"* 라고 쓸 수 있는 범위는 **프로토콜(단일계면+진공, W_ad 식, 계통적 횡방향 이동)까지**이고, **셀 크기·두께·정합 수치를 "따랐다" 고 말할 근거는 이 논문에 없다.** 원고 Methods 문장을 그 선까지만 쓰도록 조정해야 한다.

**② 우리 v5 와 이 논문은 *힘 계산기가 다르다* — 그런데 그 사실이 refs.json 요약에 안 드러나 있다.**
`refs.json[37]` 의 `v5_method_vs_haruyama` 는 geometry·W_ad 식·FixAtoms 세 줄로 비교하고 **"v5 = Haruyama method + UMA stability hack"** 으로 결론짓는다. 맞는 말이지만, **저쪽은 DFT+U(PBE, USPP, U=5.9 eV)이고 우리는 UMA-s-1p1 MLIP** 다. **W_ad 절대값을 나란히 놓는 순간(0.689 vs ≈1.25 J/m²) 그 차이가 물질 차이(Co vs Ni)인지 방법 차이(DFT vs MLIP)인지 가를 수 없다.** 현재 `refs.json` 의 `_relative_to_us` 주석은 그 비율(1.86×)을 **물질 차이(Komatsu Ni > Co 반응성)로 귀속**하고 있는데, **그 귀속은 방법 축을 통제하지 않은 것이다.** ⇒ **원장 주석을 고쳐야 한다** (§12-병합 메모에 적었다).

**③ 우리가 인용하고 싶어 하는 "SCL" 서사는, 이 논문 기준으로 *정량 근거가 없다*.**
슬라이드·원고에서 *"계면에 공간전하층이 형성되어 저항이 생긴다"* 를 쓰면서 이 논문을 각주로 다는 순간, **각주가 지지하는 것은 "그런 서사가 제안됐다" 까지**다. **두께·전위·저항 수치는 지지되지 않는다.** 우리 `computational_methods_canonical.md` §2 의 경계 선언이 옳았고, **그 경계를 넘는 문장을 쓰면 안 된다.**

**④ 이 논문의 핵심 기전은 *면 하나*에 걸려 있고, 우리 계가 그 면인지 모른다.**
"산소 능선" 은 **LCO(110) 전용** 기하다. 우리 v5 의 LiNiO₂/NCM 면지수가 **v5 보고서에 기록돼 있지 않다** (v26/v27 만 (003)/(110)/(012)/(104) 를 명시). ⇒ **우리가 이 기전을 우리 계면에 이식하려면 먼저 우리 면이 무엇인지부터 확정**해야 한다. 지금은 못 한다.

**⑤ "버퍼가 좋다" 는 결론에 두께 상한이 붙어 있는데, 우리 코팅 캠페인은 그 상한을 다룰 도구가 없다.**
저자가 단 단서(*"버퍼가 임계 두께를 넘으면 저항이 늘어난다"*)는 **버퍼 벌크 확산 배리어 × 두께** 문제다. 우리는 코팅층 **벌크 확산**을 계산한 적이 없다. ⇒ 코팅 슬라이드에서 *"코팅이 계면 저항을 낮춘다"* 만 말하고 **두께 최적점을 말하면 근거가 없다.**

---

## 12. 관련 연구 — **2014 vs 2017, 두 편의 관계**

**같은 그룹(Tateyama/NIMS)·같은 계면·다른 질문.** 중복 digest 가 아니다.

| 축 | **[Haru14]** (본 편) | **[Haru17]** `papers/haruyama2017_cation_mixing_co_diffusion_lco_lps.md` |
|---|---|---|
| **연도/저널** | 2014 · *Chem. Mater.* 26, 4248 | 2017 · *ACS AMI* 9, 286 |
| **저자** | Haruyama, Sodeyama, **Han**, **Takada**, Tateyama (5인) | Haruyama, Sodeyama, Tateyama (**3인** — Han·Takada 빠짐) |
| **무엇을 만들었나** | ⭐ **계면 4종을 처음 만든다** (면 선택 → 종단 → 정합 → 16/4/9 미끄럼 → 최저 채택) | **그 계면 3종을 그대로 물려받는다** (새로 안 만든다) |
| **질문** | **"Li 이 어디 앉고, 그것이 SCL 에 무엇을 하나"** | **"Co 가 어디로 가나"** (양이온 혼합) |
| **보고량** | **Li 공공 형성에너지** `E_v` + W_ad + W_surf + PDOS | **조성보존 in-place 스왑 에너지** `E_ex` + PDOS (+ 교환 후 `E_v` 재계산) |
| **핵심 수** | LP2 **1.44 eV**(벌크 3.2) · 전달 **−1.6 eV** · W_ad **10.6/6.1/4.3/3.8 eV/nm²** | Co↔P **−2.18 eV**(계면) vs **+1.98 eV**(벌크) · Co↔Li **전부 양수** · Co↔Nb **+0.93~1.27** |
| **방법 차이** | 스미어링 **0.001 Ry** · 4계면 (LNO(110) 포함) · 원시에너지 **비공개** | 스미어링 **0.01 Ry**(10×) · 3계면 · **`Table S3` 로 벌크 결함 총에너지 공개** (우리가 재현 성공) |
| **공통 방법** | QE · PBE · USPP 40/320 Ry · U(Co 3d)=5.9 eV · **spin-unpolarized** · **Γ-only** · 힘 0.001 Ry/bohr · 응력 0.5 kbar · 중성셀 · VESTA | **전부 동일** |
| **연결 고리** | 본문 마지막: *"this study **did not deal with the significant mixture of Cobalt** in the sulfide side … will be examined in a future study"* | 그 예고의 실행. 그리고 **되먹임**: Co↔P 교환 6회 후 `Fig. S7` 에서 **Li 공공 형성에너지가 전부 더 낮아진다** (LPS 최저 **1.4 → 0.9 eV**) ⇒ **양이온 혼합이 2014 의 SCL 을 가속한다** |

**요약 한 줄**: **2014 는 무대(계면 기하)와 배우(Li)를 만들었고, 2017 은 같은 무대에 두 번째 배우(Co)를 올린 뒤 그 배우가 첫 배우의 대사를 더 나쁘게 만든다는 것을 보였다.**

**그 밖의 이웃**
- **선행 실험**: Ohta 2006(ref 9, Li₄Ti₅O₁₂) · **Ohta 2007(ref 10, LiNbO₃ — 저항 최소)** · Takada 2008/2012/2013(refs 8, 14, 5, 13 — SCL 가설) · Sakuda 2009(ref 11, Li₂SiO₃).
- **Co 확산 실험**: Sakuda 2010(ref 15 — STEM-EDX 로 **50 nm 까지 Co**) · Ohtomo 2013(ref 16) · Woo 2012(ref 17, Al₂O₃ ALD).
- **SCL 이론 틀**: Maier(refs 19, 47) · Sata 2000 CaF₂/BaF₂ 다층(ref 48) · Guo 2007(ref 49) · **Uvarov 2011 Stern 모형(ref 50)**.
- **LPS 구조 원전**: Homma 2011(ref 22) · **Lepley 2013(ref 45/S1 — `β-Li₃PS₄-b` 모형)** · Maruyama 2002(ref 28 — b 방향 전도).
- **우리 litdb 안의 이웃**: `ncube2026_ionic_interdiffusion_lco_lgps_multiscale`(2017 편을 ref 13 으로 인용) · `barai2021_delamination_cathode_llzo_multiscale`(계면 박리 축) · `zuo2022_chlorination_cathode_interface`(양극 계면 화학 축).

---

## 13. 기술 미니 용어집 (이 digest 를 혼자 읽기 위한)

- **SCL (space-charge layer, 공간전하층)** — 두 이온전도체가 접하면 Li⁺ 화학퍼텐셜 차로 계면 부근에서 Li 이 한쪽으로 몰리고 반대쪽이 고갈된다. 고갈된 층은 Li 전도도가 낮아 **계면 저항**이 된다. **고전적으로는 Poisson–Boltzmann 으로 두께(Debye 길이)와 전위를 푼다** — **이 논문은 그것을 하지 않고**, 대신 원자단위 슈퍼셀 안에서 **자리별 Li 공공 형성에너지**로 대리 측정한다.
- **Li 공공 형성에너지 `E_v`** — Li 원자 하나를 빼서 Li 금속에 얹는 데 드는 에너지. **μ_Li = Li 금속**을 기준으로 잡으면 **eV 값이 곧 Li/Li⁺ 기준 전압(V)** 이다. 값이 낮은 자리 = **낮은 전압에서 먼저 Li 을 내놓는 자리**.
- **부착에너지 `W_ad` (work of adhesion)** — 계면을 뜯어 두 자유표면을 만드는 데 드는 에너지/면적. `W_ad = (E_A + E_B − E_AB)/S`. 클수록 잘 붙어 있다. ⚠ **두 슬랩이 변형된 채 계면을 이루면 변형에너지가 섞일 수 있다.**
- **표면에너지 `W_surf` / γ** — 벌크를 잘라 표면 둘을 만드는 비용/면적. `(E_slab − n·E_bulk)/2S` 의 2 가 "표면 둘".
- **미스핏 파라미터 μ** — 여기서는 **면적 중첩** 정의 `1 − 2S_{A∩B}/(S_A+S_B)`. **선형 변형률(%)과 다른 양**이다 (§3c-3).
- **산소 능선(ridge/bridge) vs 꼭짓점 산소(apical)** — 팔면체를 어느 면으로 자르느냐에 따라 최외곽에 **두 산소를 잇는 모서리**가 나오거나 **한 산소의 꼭짓점**이 나온다. 전자가 Li⁺ 를 훨씬 세게 당긴다는 것이 이 논문의 기하 논거.
- **DFT+U** — PBE 가 3d 전자를 과도하게 퍼뜨리는 것을 Hubbard U 로 교정. 여기선 **Co 3d 에 5.9 eV**. Nb 4d 에는 안 걸었다.
- **NCC (nonlinear core correction)** — 유사퍼텐셜에서 코어-원자가 전하 겹침의 비선형성을 보정. 3d/4d 원소·S/P 에 흔히 쓴다.
- **ESM (effective screening medium)** — 슬랩 계산에서 주기 이미지 간 정전 상호작용을 끊는 기법. 이 논문은 **채택하지 않고 점검용으로만** 썼다 (차이 0.1 / 0.01 eV).
- **β-Li₃PS₄-b** — β-Li₃PS₄ 의 Li 부분점유(4c 자리)를 **제거해 정렬시킨 모형**(Lepley 2013). 계산을 가능하게 하지만 **무질서·엔트로피는 사라진다.**
- **횡방향 미끄럼 표본(lateral slide sampling)** — 두 슬랩의 상대 registry 를 격자점마다 바꿔 여러 초기구조를 만들고 전부 이완해 최저를 고르는 절차. **우리 xy-shift 와 같은 발상**이다.
- **`figure-read ≈`** — **그림에서만 읽은 값**이라는 우리 관례 표기. 본문에 활자로 있는 값과 구분한다.

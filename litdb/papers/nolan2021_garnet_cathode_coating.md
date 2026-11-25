<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-12 신규 작성:
       ① 1저자 지정: "양극 코팅 계산 계보 8편" 세트의 **#5**. #1 aykol2014 / #2 aykol2016 / #3 xiao2019 / #4 nolan2019 기존.
       ② 계보 카드(kb/syntheses/cathode_coating_computational_lineage.md)가 #4 digest 끝에 남긴 물음
          — *"anodic limit 의 식을 누가 적어 두었나"* — 에 **이 편이 부분적으로 답한다**:
          **Methods Eq (5) `μ_Li(φ)=μ°_Li − eφ` 와 Eq (6) `E_D^open` 이 본문에 인쇄돼 있고**,
          **SI XLSX 에 `anodic limit`·`cathodic limit` 열이 89종 전부에 대해 수치로 들어 있다**(단위는 μ_Li eV).
          다만 *"anodic limit = E_D^open 이 0 을 벗어나는 φ"* 라는 **문장은 여전히 없다** (§4d·§7c).
       ③ 크로핑 그림 14장(본문 4 + 표 1 + SI 9) 중 **8장을 실제로 봤다**: `Fig. 1`·`2`·`3`·`4` 전량 +
          `Fig. S2`·`S3`·`S4`·`S5`·`S9`. ⛔ 안 본 것: `Fig. S1`·`S6`·`S7`·`S8` (전부 같은 Ed 데이터의 다른 슬라이스).
          `Table 1`·`Table 2` 는 이미지 대신 **PDF 좌표 판독으로 전 셀 복원**(회전 표라 평문 추출이 깨진다).
          `Fig. 3` 의 주기율표 인셋은 **4× 확대 재판독**해서 군번호 오류를 확인했다.
       ④ ★ 이 논문의 진짜 자산도 본문이 아니라 **Sup2 XLSX** 다(6 시트). 본 digest 가 전수 재분석해
          본문의 정성 주장을 정량으로 바꿨다(§12). 부수 소득: **Li 삼원 산화물 89종 중 LLZO·NMC·d-NMC
          세 상태 전부 Ed=0 인 것은 16종**이고 그 안에 **우리 계면 산물 `Li₂SO₄`·`Li₃PO₄` 가 또 들어 있다**.
       ⑤ ⚠ 무대가 **가넷(산화물 SE)** 이다. 우리 황화물과 *같은 기계·다른 계*다 — 수치 이식 전면 금지,
          이식 가능한 것은 **문법 4개**뿐(§7b).
       ⑥ 본문↔그림/데이터 어긋남 **7건** 발견(§10). 그중 3건은 우리가 이 논문을 인용할 때 실제로 걸린다. -->

# Computation-guided discovery of coating materials to stabilize the interface between lithium garnet solid electrolyte and high-energy cathodes for all-solid-state lithium batteries — Nolan, Wachsman, Mo (*Energy Storage Materials* **41** (2021) 571–580)

> slug `nolan2021_garnet_cathode_coating` · DOI `10.1016/j.ensm.2021.06.027` · type `DFT 전용 고속 열역학 스크리닝 (Materials Project 에너지 + pseudo-binary 상호분해에너지 + grand-potential; 자체 DFT 계산 0 · 자체 실험 0)` · PDF `litdb/inbox/109. Nolan2021_Computation_Guided_Coating_Garnet_SE_High_Energy_Cathodes.PDF` (본문 10 pp) + `109. Sup) …docx` (SI: Fig S1–S9 + Table S1–S4) + **`109. Sup2) …xlsx`(materials_stability_results — 6 시트 · Ed·상평형·ESW 한계)** + **`109. Sup3) …xlsx`(stable_materials_list — 3 시트)** · digested `2026-09-12` · status ✅ · 태그 **[외부]**

> elements: Li, Be, B, C, N, O, F, Na, Mg, Al, Si, P, S, Cl, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, Se, Br, Rb, Sr, Y, Zr, Nb, Mo, Ru, Rh, Cd, In, Sn, Sb, Te, I, Cs, Ba, La, Ce, Pr, Nd, Sm, Eu, Gd, Dy, Er, Yb, Lu, Hf, Ta, W, Re, Pb, Bi, Th
> methods: DFT, ESW

> **저자**: **Adelaide M. Nolan**¹, **Eric D. Wachsman**^1,2, **Yifei Mo\***^1,2 (¹ University of Maryland, College Park — MSE · ² Maryland Energy Innovation Institute; 단일기관 3인) · 수신 2021-05-05 / 수정 2021-06-16 / 수락 2021-06-18 / 온라인 2021-06-25 · 지원 DOE-EERE Battery Materials Research **DE-EE0008858** + 2019 Engie Chuck Edwards Memorial Fellowship + 2020 Harry K. Wells Graduate Fellowship · 계산자원 UMD + **MARCC** · 계산 프레임 **Materials Project** (⚠ OQMD 가 아니다) · 시각화 **python-ternary**
>
> **계보 (1저자 지정 "양극 코팅 계산 계보" 8편 세트의 #5)**: [Aykol 2014 AENM](aykol2014_cathode_coating_thermodynamics.md)(#1) → [Aykol 2016 Nat Commun](aykol2016_ht_cathode_coating_design.md)(#2) → [Xiao 2019 Joule](xiao2019_cathode_coating_screening.md)(#3) → [**Nolan 2019 ACS Energy Lett**](nolan2019_chemistries_stable_high_energy_cathodes.md)(#4) → **본 논문**(#5) → Honrao 2021(#6) · 리뷰 2편(#7·#8).
> **이 편은 #4 의 자기인용 후속이다** — 본문 ref 41 이 [Nolan19] 이고, Methods 가 *"the same scheme established in previous studies [30, 41]"* 라고 적는다(ref 30 = [Zhu16] *JMCA* **4**, 3253). 즉 **#4 와 같은 기계를 가넷 무대로 옮긴 편**이고, 새로 얹은 것은 **① 조성공간(Gibbs 삼각형) 전면 스캔 ② 전압 인가 개방계 쌍둥이 식 ③ 문턱형 선정 규칙**이다.

---

## 0. 이 digest 를 읽는 법 — 범위부터

### 0a. 1저자가 이 편에 물은 다섯 가지 — 답 먼저

| # | 물음 | 답 (근거 절) |
|---|---|---|
| **1** | 주된 양이 #4 의 `E_d`(eV/atom) 그대로인가 | 🟢 **그대로다.** 식 (1)–(4) 가 #4 SI 의 4단 정의와 **문자 그대로 같다** — 1원자/f.u. 정규화 · 끝점 준안정성 제거 · `E_d = min_x` · 음수 = 반응성 · DB = MP. **여기에 개방계 쌍둥이**(식 5–7)가 추가돼, 인가전압 **3 V·5 V** 에서의 `ΔE_D,mutual^open` 이 같은 단위로 같이 보고된다. 단위 표기는 표/`Fig. 1` 이 **meV/atom**, `Fig. 2–4`·XLSX 가 **eV/atom** (§4a·§4c) |
| **2** | 가넷이 대상인 게 우리 황화물과 뭐가 같고 뭐가 다른가 | 기계는 같고 **실패 모드가 반대**다. LLZO 는 **μ_Li 가 높아 Li 를 잃는 쪽**(→ La₂Zr₂O₇ + 리튬화 TM 산화물), 우리 LPSCl 은 **S²⁻ 가 산화되는 쪽**(→ Li₂SO₄·Li₃PO₄·Co₉S₈). 이식 가능한 문법 **4개**·이식 불가 **5개** 를 §7b 에 표로 |
| **3** | anodic/cathodic limit 의 식이 여기 적혀 있나 | 🟡 **절반 채운다.** Methods **식 (5) `μ_Li(φ) = μ⁰_Li − eφ`** (기준 = Li 금속)과 **식 (6) `E_D^open(C,φ)`** 가 **본문에 인쇄돼 있다** — #4 가 생략한 바로 그 정의다. **그리고 SI XLSX 에 `cathodic limit`·`anodic limit` 열이 89종 전부 수치로 있다**(μ_Li, eV → `φ = −μ_Li/e`). ⛔ 그러나 *"anodic limit ≡ E_D^open 이 0 을 벗어나는 φ"* 라는 **문장은 끝내 없다**. ⇒ 우리 `2.256 V` 의 직계 원전은 여전히 [Zhu15]지만, **전압축 정의가 이 계보 안에서 처음 인쇄된 것이 이 편**이다 (§4d·§7c) |
| **4** | 선정 규칙이 #4 의 `E_d=0` 불리언과 같나 · Li 전도체를 자르나 | 🔴 **완화됐다.** `Table 2` 기준은 **`\|E_d\| < 0.05 eV/atom` 문턱**이고, 금속 열은 **원소별 등급**(Mg `<0.003` · Zr `<0.005` · Ti `<0.03`)이며, 본문은 *"약간의 반응은 접착에 오히려 좋다"*(ref 68)고 명시한다. 수치로: **Ed=0 3상태 전부 = 16/89(18 %) → \|Ed\|<0.05 = 53/89(60 %)** (§12b). **Li 전도체를 자르지는 않는다** — `Li₂ZrO₃`·`LiAlO₂` 둘 다 살아남는다([Aykol16] 은 `−E_c>3.5 V` 로 잘랐다). ⚠ 대신 **함정이 종류가 다르다: 전도도를 아예 안 본다**. `Table S4` 가 후보들의 실측 전도도를 싣는데 `LiAlO₂ ≈10⁻¹⁵`·`γ-Li₃PO₄ 10⁻¹⁸ S/cm` 다 (§7d·§10-1) |
| **5** | 우리 db 절대값과 섞으면 안 되는 값 | `E_d`(hull 세대·계가 다름) · `Fig. S5` 의 LLZO 창 **0→3.17 V** · `Fig. S4` 의 halides 분포 · `Table S4` 전도도 · 3 V/5 V 개방계 값(그림에만 있음). §7e 에 ⛔ 목록 |

### 0b. 본 그림 / 안 본 그림 (크로핑 14장 중 **8장 실독**)

- ✅ **본 것**: `Fig. 1`(Li 삼원 산화물 67행 × 7열 heatmap) · `Fig. 2`(Li-Al-O / Li-Nb-O Gibbs 삼각형 vs LLZO) · `Fig. 3`(17개 Li-M-O 삼각형 vs LLZO + 주기율표 인셋 **4× 확대 재판독**) · `Fig. 4`(Li-Al-O vs NMC 111) · `Fig. S2`(사원 인산염·규산염·붕산염) · `Fig. S3`(**삼원 할라이드** — 우리와 가장 가까운 화학) · `Fig. S4`(물질군별 boxplot, **픽셀 캘리브레이션으로 사분위 수치화**) · `Fig. S5`(**μ_Li 창** — 이 편에서 우리 축에 가장 직접 닿는 그림, **막대 끝 좌표 → 수치 복원**)
- ⛔ **안 본 것**: `Fig. S1`(이원 산화물 heatmap — XLSX 원자료로 대체) · `Fig. S6`(LNO/LMO/LCO 별 Li-Al-O — 본문이 "LCO·LNO·LMO·NMC 다 비슷" 이라 요약한 그림) · `Fig. S7`(15개 Li-M-O vs NMC — `Fig. 3` 의 NMC 판) · `Fig. S8`(Li-Al-O vs d-NMC). 넷 다 **같은 Ed 데이터의 다른 슬라이스**이고, 그 데이터는 XLSX 로 전수 갖고 있다.
- 📄 **표는 이미지 대신 좌표 판독**: `Table 1`(13행 × 4열)·`Table 2`(22행 × 5열) 은 PDF 가 회전/다단이라 평문 추출이 깨진다 → `pymupdf` 로 단어 좌표를 읽어 **전 셀 복원**했다(§3a·§3c). `Table S1`–`S4` 는 SI 가 `.docx` 라 표가 그대로 나온다.

### 0c. 가져올 수 있는 것 / 없는 것

| 🟢 가져올 수 있는 것 | 🔴 가져오면 안 되는 것 |
|---|---|
| **식 (5)–(7) 의 개방계 정의** — 우리 `oxidation_stability` / ESW 스캔의 **계보 안 인쇄본**. 특히 `μ_Li(φ) = μ⁰_Li − eφ` 와 기준(vs Li 금속) | **`Fig. S5` 의 LLZO 창 0→3.17 V 를 우리 2.256 V 옆에** — 계가 다르고, 같은 계보 안에서도 [Zhu15] 는 LLZO 를 0.05–2.91 V 로 준다(0.26 V 차) |
| **μ_Li 불일치 서사** — SE 와 양극이 Li 를 평형시키므로 코팅은 **중간 μ_Li** 에 있어야 한다. 우리 `LPSCl\|LiCoO₂` 산물 해석의 상위 프레임 | **그들의 `E_d` 절대값을 우리 −0.3227 eV/atom 옆에** — MP hull 세대(2021 vs 2026 pinned GGA_GGA+U)·접촉물질·SE 전부 다르다 |
| **"한 점이 아니라 조성영역"** — 코팅은 소결·확산으로 조성이 움직이므로 **stable region 의 폭**이 후보의 품질이다(#4 엔 없던 축) | **`Fig. S4` halides 분포(median ≈ −0.16 eV/atom)를 "염화물은 나쁘다"로** — 그건 **Li-M-할라이드 vs LLZO** 다. 우리 LPSCl 의 Cl 과 무관 |
| **`\|E_d\| < 0.05` 문턱 + "약간의 반응은 접착에 좋다"** — 0/1 불리언보다 실험에 가까운 게이트 | **`Table S4` 전도도를 우리 db 로** — 문헌 취합이고 측정 온도가 섞여 있다(454 K·650 K·"Fig. 4 에서 외삽") |
| **`Li₂SO₄`·`Li₃PO₄`·`Li₂ZrO₃` 의 양극 양립성 + ESW 창**(§12c) — 우리 계면 산물/코팅 논의의 문헌 다리 | **3 V·5 V 개방계 `E_d^open` 값** — XLSX 에 **없고** `Fig. 1`·`Fig. S9` 색으로만 있다. 주석 붙은 몇 점만 수치가 있다 |

---

## 1. 한 줄 요약

**가넷 LLZO 와 고에너지 층상 양극(NMC)은 열역학적으로 서로 안정할 수 없다 — LLZO 의 Li 화학퍼텐셜이 너무 높아서 양극에 Li 를 빼앗기기 때문이고**(E_d −87 ~ −132 meV/atom, 산물 La₂Zr₂O₇ + LaMO₃ + 리튬화 TM 산화물), **그래서 코팅은 "LLZO 와도 NMC 와도 안정" 이라는 서로 모순되는 두 조건을 동시에 만족해야 하는데, 그 해(解)는 Li 삼원 산화물 중 `Li₂O–MOₓ` 타이라인 근처에만 좁게 존재한다** — 본 논문은 원소 66종 · 이원 산화물 130종 · Li 삼원 산화물 89종(+ 사원 인산염/규산염/붕산염, 삼원 할라이드)을 Materials Project 에너지로 전수 계산해 그 좁은 해집합을 조성공간 지도(`Fig. 2`–`Fig. 4`)와 목록(`Table 2`)으로 그려 준다.

---

## 2. 메타

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| A.M. Nolan, E.D. Wachsman, **Y. Mo\*** (UMD) | *Energy Storage Materials* **41**, 571–580 (2021) | `10.1016/j.ensm.2021.06.027` | SE = `Li₇La₃Zr₂O₁₂`(+ `Li₇La₃Sn₂O₁₂`·`Li₅La₃Nb₂O₁₂`·`Li₅La₃Ta₂O₁₂`) · 양극 = `LiCoO₂`·`LiNiO₂`·`LiMnO₂`·`LiMn₂O₄`·NMC 111/622/811 (+ 각 탈리튬 `Li₀.₅…`) · 접촉물질 = 원소 66 · 이원 산화물 130 · **Li 삼원 산화물 89** · 사원 인산염/규산염/붕산염 ~85 · 삼원 할라이드 31 | **순수 계산** — 자체 DFT 0회, 실험 0회. MP 에너지 + pymatgen 상평형/grand-potential |

**무엇이 새로운가 (#4 대비)**
1. 무대가 **양극 일반**에서 **가넷 SE ↔ 양극 계면**으로 바뀌었다 → 조건이 **둘**(SE 와도 양극과도)이 됐다.
2. **조성공간 전면 스캔**: 알려진 화합물 점이 아니라 Li-M-O 삼각형의 **모든 조성**을 격자로 훑는다(`Fig. 2`–`Fig. 4`). 이유가 물리적이다 — 코팅은 소결·상호확산·비정질화로 **점이 아니라 영역**이 된다.
3. **개방계(인가전압) 쌍둥이 식** 도입: 식 (5)–(7), φ = 3 V·5 V.
4. **선정 규칙이 문턱화**: `E_d = 0` → `|E_d| < 0.05 eV/atom`.
5. **환경 변수 감도 시험**: CO₂ 미량 첨가(`Table S1`), μ_Li 스캔 0→−4 eV(`Table S2`), μ_O 스캔 0→−1 eV(`Table S3`).

---

## 3. 핵심 물성 (수치)

> ⚠ 이 논문에는 **σ·Ea·탄성계수·밴드갭이 하나도 없다**. 있는 물성은 (i) 분해에너지 `E_d` (ii) μ_Li 전기화학 창 (iii) `Table S4` 의 **문헌 취합** 이온전도도뿐이다.

### 3a. `Table 1` — LLZO ↔ 양극 (본 digest 가 PDF 좌표로 전 셀 복원)

| 양극 | x_LLZO | **E_d (meV/atom)** | x_LLZO 에서의 상평형 |
|---|---|---|---|
| `LiCoO₂` | – | **0** | – |
| `Li₀.₅CoO₂` | 0.33 | **−21** | **O₂**, La₂O₃, LiCoO₂, La₂Zr₂O₇ |
| `LiNiO₂` | – | **0** | – |
| `Li₀.₅NiO₂` | 0.46 | **−35** | Li₂NiO₃, NiO, La₂Zr₂O₇, **LaNiO₃** |
| `LiMnO₂` | – | **0** | – |
| `LiMn₂O₄` | 0.46 | **−60** | Li₂MnO₃, LiMnO₂, La₂Zr₂O₇, **LaMnO₃** |
| `MnO₂` | 0.70 | **−123** | La₂O₃, Li₂MnO₃, La₂Zr₂O₇ |
| **NMC 111** | 0.57 | **−87** | Li₂O, LiCoO₂, Li₆Zr₂O₇, Li₂NiO₃, NiO, **La₂MnCoO₆** |
| **d-NMC 111** | 0.60 | **−132** | LiCoO₂, Li₆Zr₂O₇, Li₂NiO₃, Li₂ZrO₃, Li₂O₂, La₂MnCoO₆ |
| NMC 622 | 0.44 | **−63** | Li₂O, Li₆Zr₂O₇, Li₂NiO₃, NiO, La₂MnCoO₆ |
| d-NMC 622 | 0.48 | **−117** | Li₂NiO₃, Li₂ZrO₃, ZrO₂, NiO, La₂MnCoO₆ |
| NMC 811 | 0.29 | **−38** | Li₂O, Li₆Zr₂O₇, Li₂NiO₃, NiO, La₂MnCoO₆ |
| d-NMC 811 | 0.44 | **−80** | Li₂NiO₃, ZrO₂, NiO, La₂MnCoO₆, La₂Zr₂O₇ |

**읽는 법 3가지**
- **탈리튬이 항상 더 나쁘다**: 모든 짝에서 d- 쪽이 1.5–2.1배 더 음수 (111 −87→−132 · 622 −63→−117 · 811 −38→−80). #4 의 결론(*"충전상태가 병목"*)이 SE 상대로도 그대로다.
- **Mn 이 많을수록 나쁘다**: NMC 811(Mn 0.1) −38 < 622(Mn 0.2) −63 < 111(Mn 0.33) −87. 단조. ✔ 본문 주장 성립.
- **La 페로브스카이트가 공통 산물**: `LaNiO₃`·`LaMnO₃`·`La₂MnCoO₆` — 이것이 소결 실험에서 실제로 관측되는 상이다(ref 18·19·31).

### 3b. `Table S1` — CO₂ 를 0.0004/atom 넣었을 때 (SI, docx 표 그대로)

| 양극 | x | E_d with LLZO-CO₂ (meV/atom) | CO₂ 없을 때(`Table 1`) |
|---|---|---|---|
| `Li₀.₅CoO₂` | 0.495 | **−18** | −21 |
| `Li₀.₅NiO₂` | 0.462 | **−35** | −35 |
| `LiMn₂O₄` | 0.462 | **−60** | −60 |
| `MnO₂` | 0.696 | **−123** | −123 |
| NMC 111 | 0.569 | **−87** | −87 |
| d-NMC 111 | 0.601 | **−132** | −132 |

🔑 **에너지는 사실상 안 변한다(1건만 3 meV 변화). 변하는 것은 상평형이다** — `Li₂CO₃` 가 전 반응에 들어오고 `La₂CO₅` 도 나온다. 본문이 *"소량의 CO₂ 첨가만으로도 LLZO 가 부분 분해된다"* 라고 쓴 것은 **에너지가 아니라 산물 이야기**다. (본 digest 가 두 표를 대조해 확인한 것이고, 논문은 이 대조를 인쇄하지 않는다.)

### 3c. `Table 2` — 선정 결과 (본 digest 가 회전 PDF 좌표로 복원, 22행)

> 표제: *"Materials stable (|E_d| < 0.05 eV/atom) with LLZO and NMC 111. `Li₂O` and `Li₂O₂` are stable with both LLZO and NMC and are not explicitly listed."*

| M | M(금속) 이 LLZO 와 안정? | LLZO 와 안정 | NMC 111 & d-NMC 와 안정 | **셋 다 안정 (최종 후보)** |
|---|---|---|---|---|
| B | – | LiBO₂, Li₆B₄O₉, Li₃BO₃ | Li₃BO₃, LiBO₂, Li₆B₄O₉, Li₃B₁₁O₁₈, Li₃B₇O₁₂ | **Li₃BO₃, LiBO₂, Li₆B₄O₉** |
| C | Stable | Li₂CO₃ | Li₂CO₃ | **Li₂CO₃** |
| N | Stable | LiNO₃ | LiNO₃ | **LiNO₃** |
| Mg | \|E_d\|<0.003 | MgO | MgO | **MgO** |
| Al | – | LiAlO₂, Li₅AlO₄ | Al₂O₃, LiAlO₂, Li₅AlO₄ | **LiAlO₂, Li₅AlO₄** |
| Si | – | Li₂SiO₃, Li₄SiO₄ | SiO₂, Li₂Si₂O₅, Li₂SiO₃, Li₄SiO₄ | **Li₂SiO₃** |
| P | – | Li₃PO₄ | Li₄P₂O₇, Li₃PO₄ | **Li₃PO₄** |
| Sc | – | Sc₂O₃, LiScO₂ | Sc₂O₃, LiScO₂ | **Sc₂O₃, LiScO₂** |
| Ti | \|E_d\|<0.03 | Ti₂O, TiO, Ti₃O, Ti₆O, LiTi₂O₄, Li₄TiO₄, Li₂TiO₃, LiTiO₂ | TiO₂, Li₄TiO₄, Li₂TiO₃ | **Li₄TiO₄, Li₂TiO₃** |
| V | Stable | LiVO₂, Li₃VO₄ | Li₃VO₄ | **Li₃VO₄** |
| Cr | Stable | LiCrO₂, Li₂CrO₄ | CrO₂, Cr₂O₃, LiCrO₂, Li₂CrO₄ | **LiCrO₂, Li₂CrO₄** |
| Zn | Stable | ZnO, Li₁₀Zn₄O₉, Li₆ZnO₄ | ZnO | **ZnO** |
| Ga | Stable | LiGaO₂, Li₅GaO₄ | Ga₂O₃, LiGaO₂, LiGa₅O₈, Li₅GaO₄ | **Li₅GaO₄, LiGaO₂** |
| Ge | Stable | Li₂GeO₃, Li₄GeO₄, Li₈GeO₆ | GeO₂, Li₄Ge₅O₁₂, Li₂GeO₃, Li₄GeO₄, Li₈GeO₆ | **Li₄GeO₄, Li₂GeO₃, Li₈GeO₆** |
| **Zr** | \|E_d\|<0.005 | Zr₃O, ZrO₂, Li₂ZrO₃, Li₆Zr₂O₇ | ZrO₂, Li₆Zr₂O₇, Li₂ZrO₃ | **ZrO₂, Li₆Zr₂O₇, Li₂ZrO₃** |
| Y | – | Y₂O₃, LiYO₂ | Y₂O₃, LiYO₂ | **Y₂O₃, LiYO₂** |
| Nb | Stable | Li₈Nb₂O₉, Li₃NbO₄, LiNbO₂ | Nb₂O₅, Li₈Nb₂O₉, LiNbO₃, Li₃NbO₄, LiNb₃O₈ | **Li₈Nb₂O₉, Li₃NbO₄** |
| Mo | Stable | MoO₂, Li₂MoO₄, Li₄MoO₅ | MoO₃, Li₂MoO₄, Li₄MoO₅ | **Li₂MoO₄, Li₄MoO₅** |
| Sn | Stable | SnO, Li₂SnO₃, Li₈SnO₆ | SnO₂, Li₂SnO₃ | **Li₂SnO₃** |
| Sb | Stable | Sb₂O₃, Li₅SbO₅, Li₃SbO₄ | LiSb₃O₈, Li₅SbO₅, LiSbO₃, Li₃SbO₄ | **Li₅SbO₅, Li₃SbO₄** |
| Ta | Stable | *"La₃TaO₄"* ⚠(§10-6) | LiTa₃O₈, LiTaO₃, *"La₃TaO₄"* | **Li₃TaO₄** |
| W | Stable | Li₄WO₅ | WO₃, Li₂WO₄, Li₄WO₅ | **Li₄WO₅** |

### 3d. `Table S4` — 후보 코팅의 **실측**(문헌 취합) 이온전도도 ⛔ 우리 db 이식 금지

| 코팅 | σ_total (S/cm) | 조건 |
|---|---|---|
| Li-B-O glass | 3.4 × 10⁻⁷ | RT |
| Li₃BO₃–Li₂CO₃ glass | 7.6 × 10⁻⁷ | RT |
| **LiAlO₂** | **≈ 10⁻¹⁵** | RT, *"Fig. 4 에서 외삽"* |
| Li₂SiO₃ | 2.5 × 10⁻⁸ | RT |
| Li₄SiO₄ | 4.1 × 10⁻⁷ | RT |
| **γ-Li₃PO₄** | **10⁻¹⁸** | RT |
| Li₄Ti₅O₁₂ | 5.7 × 10⁻⁷ | RT |
| Li₃VO₄ | 3.7 × 10⁻⁹ | RT, 고상합성 |
| Li₈ZrO₆ | 4.8 × 10⁻⁸ | **454 K** |
| LiNbO₃ | 6.7 × 10⁻⁸ | **650 K** |
| Li₂SnO₃ | 3.1 × 10⁻¹² | RT |

🔑 **최종 후보 전체가 10⁻⁷ S/cm 이하다.** 우리 comp1 벌크(mS/cm 급)보다 **4–5 자릿수 낮다**. 논문은 이것을 알고 있고 *"대부분 nm 두께면 문제없다 · 잘 쓰이는 Li-Nb-O 도 빠른 전도체가 아니다(ref 75)"* 로 방어한다 — 그 방어의 타당성은 §10-1 에서 따진다.

---

## 4. DFT/계산 방법 ★

- **code / version**: **자체 DFT 를 하지 않는다.** 에너지는 **Materials Project**(ref 43)에서 받아 쓰고, 해석은 **pymatgen**(ref 76)으로, 삼각형 그림은 **python-ternary**(ref 77)로 그린다. VASP 설정·컷오프·k-mesh 는 **논문에 하나도 없다** — *"evaluated by consistent parameters, allowing us to directly compare the energies"* 라는 MP 의 일관성 주장에 위임한다.
- **functional / pseudo / k-points / ecut / supercell / DFT+U**: **n/a (인쇄 없음)**. 실질적으로 MP 표준 = PBE + GGA/GGA+U 혼합 보정 + PAW 이지만 **이 논문이 그렇게 적지 않았다** — 인용할 때 우리가 보충하면 안 된다.
- **구조 선별 규칙**: *"we used materials that had an existing identification number in the **ICSD**"* — **실험적으로 합성/특성화된 상만** 쓴다. (→ MP 의 가상 구조·예측 구조는 배제. 이건 [Xiao19] 의 data-mined 후보 포함 정책과 다르다.)
- **AIMD**: **하지 않는다.** Discussion 에서 *"AIMD 로 한두 계를 더 볼 수 있다(ref 70, Tang/Ong 나트륨계)"* 고 **미래 과제로만** 언급.
- **MLIP**: 없음.
- **무질서 처리**: **없다 — 필요가 없는 방법이다.** 조성만 다루고 구조를 다루지 않으므로 LLZO 의 Li 부분점유·NMC 의 TM 배열 같은 무질서가 계산에 들어오지 않는다. ⚠ 바꿔 말하면 **무질서 효과를 이 방법으로는 볼 수 없다** (§10-4).
- **온도·PV**: **0 K DFT 에너지, PV 무시, 엔트로피 무시.** 본문이 스스로 한계로 적는다.

### 4a. 화학 안정성 — 닫힌계 4단 정의 (Methods 식 1–4) ★ #4 와 **문자 그대로 같다**

```
(1)  C_pseudo-binary(C_A, C_B, x) = x·C_A + (1−x)·C_B       ← C_A, C_B 는 "1 원자/화학식단위" 로 정규화
(2)  E_pseudo-binary(A, B, x)     = x·E_A + (1−x)·E_B        ← 선형보간(= 반응 전 에너지)
(3)  ΔE_D(A, B, x) = E_eq[C_pseudo-binary(C_A, C_B, x)] − E_pseudo-binary(A, B, x)
                                                              ← E_eq = 같은 조성의 최저에너지 상집합(hull)
(4)  ΔE_D,mutual(A, B, x) = ΔE_D(A, B, x) − x·ΔE_D(A) − (1−x)·ΔE_D(B)
                                                              ← ΔE_D(A)·ΔE_D(B) = 각 끝점의 energy above hull
     E_d ≡ min_{x∈[0,1]} ΔE_D,mutual(A, B, x)                 ← 부호: 음수 = 발열 = 반응성
     단위: eV/atom (pseudo-binary 조성 1원자당) — 표·Fig. 1 은 meV/atom
```

🟢 **이 네 줄이 우리 `tools/oxidation/interface_reactivity.py` 의 `InterfacialReactivity(..., use_hull_energy=True)` + `get_kinks()` 최솟값과 수학적으로 동일하다.** (4)의 끝점 hull 차감이 곧 `use_hull_energy=True` 다: (3)+(4) 를 정리하면 `E_eq − x·E_hull(C_A) − (1−x)·E_hull(C_B)`.

### 4b. 왜 x 를 훑는가 (물리)

`x` 는 계면에서 두 물질이 섞이는 몰비다. 실제 계면은 어떤 비율로 섞일지 모르므로 **가장 나쁜 비율(최소 에너지)** 을 대표값으로 잡는다. 그래서 `Table 1` 은 `E_d` 와 함께 **`x_LLZO` 를 같이 인쇄한다** — 예컨대 d-NMC 111 은 `x_LLZO = 0.60` 에서 최악이다(LLZO 가 60 %). ⚠ 이 최악점이 실제 계면의 조성일 필요는 없다 — **상한 추정**이다.

### 4c. 전기화학 안정성 — 개방계 3단 정의 (Methods 식 5–7) ★ **#4 에 없던 것**

```
(5)  μ_Li(φ) = μ⁰_Li − eφ                     ← φ 는 Li 금속 기준 전위. μ⁰_Li = Li 금속의 화학퍼텐셜
(6)  E_D^open(C, φ) = E_eq(C, μ_Li) − E(C) − Δn_Li·μ_Li(φ)
                                               ← Li 저장조와 평형인 계의 분해에너지.
                                                 Δn_Li = 반응에서 드나든 Li 몰수
(7)  ΔE_D,mutual^open(A, B, x, φ)
        = ΔE_D^open(A, B, x, φ) − x·ΔE_D^open(A, φ) − (1−x)·ΔE_D^open(B, φ)
     ΔE_d^open ≡ min_x ΔE_D,mutual^open
```

- **기준**: 식 (5) 가 φ 를 **Li 금속 기준**으로 못박는다 = 우리가 쓰는 **vs Li/Li⁺** 와 같은 기준.
- **적용 φ**: 본 논문은 **φ = 3 V 와 5 V 두 점만** 계산한다(*"typical cathode voltage range"*, ref 44–46). **연속 스캔이 아니다** — 그래서 이 논문의 본문에는 "창(window)" 이 없다.
- ⚠ 식 (6) 의 `E_eq(C, μ_Li)` 에서 나오는 상평형 문자열에는 **Li 저장조가 `Li` 라는 상으로 찍힌다** — 5 V 에서도 `Li` 가 산물로 인쇄된다(`Fig. S9a`, `Table S2`·`S3`). 이것을 실제 금속 Li 석출로 읽으면 안 된다 (§10-3).

### 4d. ★ `anodic limit`·`cathodic limit` — **XLSX 에만 있고 본문에 정의가 없다**

`Sup2 XLSX` 의 `ternary-oxides_llzo` / `ternary-oxides_NMC` 시트에는 본문 어디에도 언급되지 않는 두 열이 있다:

| 열 | 값의 성격 | 단위 | 우리 표기로 |
|---|---|---|---|
| `cathodic limit` | 음수 (0 ~ −4.3) | **μ_Li (eV)** | `φ_red = −μ_Li/e` |
| `anodic limit` | 음수 (−1.11 ~ −5.23) | **μ_Li (eV)** | `φ_ox = −μ_Li/e` |

**검증 3단** (본 digest 가 한 것):
1. `LiCoO₂` 의 두 값 −1.82199 / −3.64086 → **1.82–3.64 V**.
2. `Fig. S5`(μ_Li 창 막대그래프)의 `LiCoO₂` 막대 끝을 픽셀 캘리브레이션으로 읽으면 **−1.817 / −3.651** — 1 px(≈0.003 eV) 안에서 일치. ⇒ **`Fig. S5` 의 막대 = 이 두 열이다.**
3. `Li₃PO₄` 는 **0.69–4.20 V** 가 나오는데, 이는 [Zhu15](*ACS AMI* **7**, 23685)가 인쇄한 `Li₃PO₄` 창 **0.68–4.21 V** 와 일치. ⇒ **같은 grand-potential 양이고, [Zhu15] 와 같은 수치 체계**.

🟡 **그러나 논문은 이 열을 설명하지 않고, `anodic limit` 을 정의하는 문장도 없다.** 즉 *"E_D^open(C,φ) 가 0 을 벗어나는 φ 가 한계다"* 라는 마지막 한 줄이 이 편에도 없다. **#4 는 그림 축에만, #5 는 식 + 데이터파일에.** 다음 단계(#7 리뷰 *Joule* 2018)에서 문장까지 확인할 것.

### 4e. 감도 시험 3종 (SI)

| 시험 | 무엇을 흔들었나 | 결과 |
|---|---|---|
| `Table S1` | LLZO 에 **CO₂ 0.0004/atom** 첨가 | E_d 사실상 불변, **상평형에 Li₂CO₃·La₂CO₅ 등장** |
| `Table S2` | **μ_Li 를 0 → −4 eV 스캔** (LLZO–NMC 111 계면) | mutual Rxn. E. **−81 → −29 → 0(−0.5 eV) → −155(−1.75) → −168(−4)**. ⚠ **μ_Li = −0.5 eV 에서 정확히 0** 이 되는 구간이 있다 |
| `Table S3` | **μ_O 를 0 → −1 eV 스캔** | mutual −141 → −168. O 를 빼면 `O₂`·`ZrO₂` 가 산물로 나온다 |

⚠ `Table S2` 의 μ_Li = −0.5 eV 행(**mutual = 0.00**)은 *"LLZO 비율 0.00"* 즉 **LLZO 가 아예 들어가지 않은 해**다 — 계면이 안정해진 게 아니라 **최소화가 끝점으로 도망간 것**이다. 본문은 이 행을 언급하지 않고 *"비슷한 경향"* 으로 요약한다.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | Li 삼원 산화물 **67종 × 7열** heatmap. 열 = `NMC` · `d-NMC` · `LLZO`(화학) ‖ `LLZO,3V` · `LLZO,5V` · `NMC,3V` · `d-NMC,5V`(전기화학). 색 = E_d, **−0 (흰) ~ < −150 meV/atom (진청)**. 행은 양이온족별 4패널(nonmetals / transition metals / p-block metals / heavy transition metals)로 묶고 **패널 안에서는 Li 함량 증가 순** | **우리 cascade 후보표의 양식으로 쓸 수 있는 한 장**: "한 물질 × 여러 상대·여러 전압" 을 한 행으로. ⚠ 열 라벨이 비대칭(`NMC,3V` 인데 `d-NMC,5V`) — 캡션과 어긋난다(§10-5). ⚠ 데이터 89종 중 **67종만** 그렸다(§10-5) |
| 2a,b | **Li-Al-O**(a)·**Li-Nb-O**(b) Gibbs 삼각형 heatmap vs LLZO. 초록 점선 = 완전안정 영역, 파란 점 = 알려진 화합물. 색 0.0 ~ **< −0.15 eV/atom**. 주석: `Al₂O₃` **E_d = −0.094**(→ La₂Zr₂O₇, LaAlO₃, LiAlO₂) · `Nb₂O₅` **−0.135**(→ LaNbO₄, Li₃NbO₄, ZrO₂) · `Li₃NbO₄` **−0.012**(→ La₂Zr₂O₇, La₂O₃, Li₈Nb₂O₉) | **"점이 아니라 영역"** 이라는 발상 자체가 이식 가능하다. Li-Al-O 는 안정영역이 좁은 사각형(Li₂O·Li₂O₂·LiAlO₂·Li₅AlO₄ 로 둘러싸인)인데, **Li-Nb-O 는 Nb 코너까지 통째로 노랗다** — 그래서 실험에서 Li-Nb-O 코팅이 잘 듣는다는 설명 |
| 3 | **17개 Li-M-O**(M = B,C,N,Al,Si,P,Ti,V,Cr,Zr,Nb,Mo,Zn,Ga,Ge,Ta,W) 삼각형 vs LLZO. 색 0.0 ~ **< −0.10 eV/atom** (⚠ `Fig. 2` 와 **다른 스케일**) | **계 선택 규칙의 시각적 근거**: 비금속 M(B·Si·P)은 검은 영역이 넓다 = 안정영역이 좁다. 금속 M(Zn·Ga·Ge·Nb·Ta·Zr·Ti)은 노란 영역이 넓다. ⚠ 오른쪽 주기율표 인셋의 **군번호가 전부 1 씩 어긋나 있다**(§10-2) |
| 4 | **Li-Al-O vs NMC 111** 삼각형. 색 0.0 ~ **< −1.00 eV/atom**(⚠ `Fig. 2` 의 **10배 스케일**). 주석: `Al₂O₃` **E_d = −0.015**(→ Li₂Mn₃NiO₈, LiCoO₂, LiAlO₂, NiO) · `LiAl` **−0.872**(→ MnCo, LiAlO₂, Li₅AlO₄, NiO, MnNi₃, Co) | ★ **`Fig. 2a` 와 겹쳐 보는 것이 이 논문의 핵심 그림 쌍이다**: vs LLZO 는 **Li-rich 쪽**이 노랗고, vs NMC 는 **O-rich 쪽**(`Li₂O–Al₂O₃` 타이라인 아래 전부)이 노랗다 → **겹치는 곳이 타이라인 자체뿐**. "모순되는 두 요구" 의 그림 증명 |
| S1 | 이원 산화물 heatmap (LLZO·NMC·d-NMC + 3 V·5 V) | ⛔ 미판독 — XLSX 원자료(130종)로 대체 |
| S2 | **사원** 인산염(25)·규산염(22)·붕산염(~38) heatmap | 🔑 **삼원 `Li₃PO₄`(E_d=0) 는 완벽한데 사원 인산염은 전부 나쁘다** — 제3 양이온이 들어가면 LLZO 와의 양립성이 무너진다. `LiB(SO₄)₂`·`Li₅B(SO₄)₄` 등 황산-붕산염은 최악 |
| S3 | **삼원 할라이드 31종** heatmap. 우리 화학과 가장 가까운 그림 | ⛔⛔ **Cl 화합물은 `LiAlCl₄`·`LiGaCl₄`·`CsLiCl₂` 셋뿐이고 셋 다 LLZO 와 강반응**(짙은 보라). **`Li₃YCl₆`·`Li₃InCl₆` 같은 현대 할라이드 SE 도, 황화물도 한 종도 없다.** ⚠ `LiIO₃`(요오드산염=산화물)가 "halides" 패널에 들어 있다 |
| S4 | 물질군별 E_d **boxplot** — (a) LLZO 기준 7군, (b) LLZO·LLSnO·LLNbO·LLTaO 4가넷 비교 | ★ **본 digest 가 픽셀 캘리브레이션으로 수치화**(figure-read ≈, eV/atom): oxides 상자 **0 ~ −0.035**(가장 좁음, 중앙값 ≈ 0) · nitrides **0 ~ −0.076**(중앙 −0.015) · silicates −0.016 ~ −0.059(중앙 −0.031) · binary oxides 0 ~ −0.122(중앙 −0.030) · borates −0.009 ~ −0.086(중앙 −0.041) · **phosphates −0.096 ~ −0.183(중앙 −0.143)** · **halides −0.120 ~ −0.221(중앙 −0.164, 최악)**. (b) 네 가넷의 경향이 같다 → **도핑 가넷에도 적용 가능** 주장의 근거 |
| S5 | ★★★ **μ_Li 창** — LLZO + 양극 13상태의 안정 구간 막대. x축 **μ_Li (eV), 0 → −5 (역방향)** | ★ **이 편에서 우리 축에 가장 직접 닿는 그림.** 본 digest 판독(figure-read ≈, `φ = −μ_Li`): **LLZO 0 → 3.17 V** · LiCoO₂ 1.82–3.65 · Li₀.₅CoO₂ 3.66–3.94 · LiNiO₂ 2.65–3.56 · LiMnO₂ 1.50–2.64 · LiMn₂O₄ 3.28–3.52 · MnO₂ 3.53–5.02 · **NMC111 2.06–3.61** · **d-NMC111 3.50–4.02** · NMC622 2.57–3.63 · d-NMC622 3.46–3.83 · NMC811 2.61–3.60 · d-NMC811 3.43–3.77. ⇒ **LLZO(≤3.17) 와 d-NMC111(≥3.50) 은 겹치지 않는다** = 본문의 "little to no overlap" 의 수치 |
| S6 | Li-Al-O vs LiNiO₂ / LiMnO₂ / LiCoO₂ | ⛔ 미판독 — 본문이 "LCO·LNO·LMO·NMC 경향 동일" 로 요약 |
| S7 | 15개 Li-M-O vs NMC 111 (`Fig. 3` 의 NMC 판) | ⛔ 미판독 — 결론은 "안정영역은 `Li₂O–MOₓ` 타이라인뿐, O-rich 쪽이 관대" |
| S8 | Li-Al-O vs d-NMC | ⛔ 미판독 |
| S9 | **5 V 에서의 Li-Nb-O** — (a) vs LLZO, (b) vs NMC. 색 0.0 ~ **< −1.20 eV/atom** | ★ 주석 수치: (a) `Nb₂O₅` **−0.03**, `LiNbO₃` **−0.047**, `Li₈Nb₂O₉` **−0.057**, 산물 전부 **LaNbO₄, Li, O₂, ZrO₂**; (b) 셋 다 **stable**. 🔑 두 가지가 여기서 보인다 — ① **전압을 걸면 LLZO 쪽이 나빠지고 NMC 쪽이 좋아진다**(기구 확인) ② ⚠ 그런데 **Li-poor 멤버는 오히려 좋아진다**(Nb₂O₅ −0.135→−0.03) — 본문의 일반문장에 반례(§10-3) ③ ⚠ **5 V 에서 산물에 `Li` 금속이 인쇄된다** = 개방계 저장조 표기 |
| Table 1 | LLZO ↔ 양극 13종의 E_d·x_LLZO·상평형 | §3a 에 전 셀 복원 |
| Table 2 | `\|E_d\| < 0.05` 최종 후보 목록 (22행 × 5열) | §3c 에 전 셀 복원. ⚠ 본문 원소 목록(21종)에 **Zr 가 빠져 있다**(§10-7) |
| Table S1 | CO₂ 첨가판 `Table 1` | §3b |
| Table S2 | μ_Li 스캔 (0 → −4 eV) | §4e |
| Table S3 | μ_O 스캔 (0 → −1 eV) | §4e |
| Table S4 | 후보 코팅의 문헌 이온전도도 11종 | §3d ⛔ 우리 db 이식 금지 |

---

## 6. Post-processing ★

- **무엇**:
  ① **pseudo-binary 상호분해에너지**(닫힌계, 식 1–4) — 전 조합 × `x∈[0,1]`.
  ② **grand-potential 분해에너지**(개방계, 식 5–7) — φ = 3 V, 5 V.
  ③ **조성공간 격자 스캔** — Li-M-O 삼각형의 모든 조성점에 대해 ①을 반복해 heatmap.
  ④ **μ_Li 전기화학 창** — `Fig. S5` + XLSX 의 `cathodic/anodic limit` 열(본문 미설명).
  ⑤ **감도 시험** — CO₂ 첨가 · μ_Li 스캔 · μ_O 스캔.
- **도구**: **pymatgen**(상평형·hull·grand potential) · **Materials Project** API · **python-ternary**(Gibbs 삼각형) · ICSD id 필터.
- **수치화·플롯·기록 방식**:
  - heatmap 은 **meV/atom**(`Fig. 1`) 또는 **eV/atom**(`Fig. 2`–`Fig. 4`) — 그림마다 **컬러바 상한이 다르다**(−0.10 / −0.15 / −1.00 / −1.20). 그림끼리 색으로 비교하면 틀린다.
  - 원자료를 **XLSX 2본으로 공개**했다. `Sup2` = 값(6 시트: el/binary/ternary × LLZO/NMC), `Sup3` = 목록(3 시트: 화학안정 / 전기화학안정 / `< −60 meV` 완화판).
  - ⚠ **3 V·5 V 개방계 값은 XLSX 에 없다** — 그림 색으로만 존재. 재현하려면 다시 계산해야 한다.

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

### 7a. 양(quantity) 대조표

| 우리 값 | 이 논문의 대응물 | 어디에 | 같은 양인가 |
|---|---|---|---|
| `interface_reactivity` = **−0.3227 eV/atom** (comp1 vs LiCoO₂) · `−0.3308`(modelc) | **E_d** (min mutual decomposition energy) | 본문 전체 · `Table 1` · `Fig. 1`–`Fig. 4` · Sup2 XLSX | 🟢 **같은 양·같은 구현.** 식 (1)–(4) = `InterfacialReactivity(use_hull_energy=True).get_kinks()` 최솟값. #4 와 동일 |
| `oxidation_limit` = **2.256 V**, `reduction_limit` = **1.242 V** (grand-potential onset) | **anodic limit / cathodic limit** | **Sup2 XLSX 열 + `Fig. S5`** (본문 정의 없음) | 🟡 **같은 양 + 이번엔 식도 있다.** 식 (5)(6) 이 본문 Methods 에 인쇄. `Li₃PO₄` 0.69–4.20 V 가 [Zhu15] 의 0.68–4.21 V 를 재현 = 수치 체계까지 같다 |
| `sei_products` / `interface_reactivity_v2` (전압분해 `GrandPotentialInterfacialReactivity`) | **ΔE_d^open at φ = 3 V, 5 V** (식 7) | `Fig. 1` 뒤 4열 · `Fig. S9` | 🟢 **같은 양.** ⚠ 우리는 **연속 스캔**, 그들은 **두 점**. 우리 쪽이 정보가 많다 |
| `oxidation_stability` 의 산물 집합 | 상평형 문자열 | `Table 1`·`Fig. 2`·`Fig. S9` 주석 | 🟢 같은 성격. ⚠ 둘 다 **기체 `O₂` 를 고체와 같은 자격**으로 쓴다(§10-3) |
| `σ`(MLIP-MD) · `Ea` · `E_VRH` · `band gap` | **없음** | — | 🔴 **이 논문에 대응물이 없다**. 물성 4축 중 A·C·D 는 이 편에 0 |

### 7b. ★ 가넷 vs 우리 황화물 — 같은 것 / 다른 것 (1저자 물음 #2)

| | **같다** | **다르다** |
|---|---|---|
| **기계** | pseudo-binary + hull + grand potential, MP, 0 K, pymatgen — **문자 그대로 같은 코드 경로** | — |
| **SE 의 μ_Li 위치** | 둘 다 Li-rich | **LLZO 는 μ_Li 창이 `0 → −3.17 eV`(0–3.17 V) 로 Li 금속까지 닿는다.** 우리 comp1 은 **1.242–2.256 V** — 아래도 위도 잘려 있다. ⇒ 가넷은 **음극쪽이 공짜, 양극쪽이 문제**, 우리는 **양쪽 다 문제** |
| **실패 모드** | 둘 다 "SE 가 양극과 반응해 저항층" | **LLZO: Li 를 *잃는다*** → La₂Zr₂O₇ + 리튬화 TM 산화물 + LaMO₃. **LPSCl: S²⁻ 가 *산화된다*** → Li₂SO₄ + Li₃PO₄ + Co₉S₈ + LiCl. 원인 원소가 다르다(La/Zr 골격 vs S 음이온) |
| **공정** | — | **가넷은 600–800 °C 동시소결**이 필수 → 이 논문의 절반이 소결 화학(CO₂·Li₂CO₃·LaMO₃). **황화물은 냉간가압** → 우리 계엔 이 축이 없다 |
| **환경 취약점** | — | 가넷: **CO₂ → Li₂CO₃ 표면층**(제거해야 저항이 낮아짐). 황화물: **H₂O → H₂S**. 같은 "공기 반응" 이지만 화학이 다르다 |
| **양극 상태 의존** | 🟢 **완전히 같다** — 탈리튬(충전)이 항상 더 나쁘다 | — |

**이식 가능한 문법 4개** (수치 0)
1. **μ_Li 불일치 프레임** — SE 와 양극은 Li 를 평형시키려 하므로, 코팅은 **두 μ_Li 사이**에 창을 가져야 한다. `Fig. S5` 가 그 프레임의 표준 그림이다. **우리도 `LPSCl(1.242–2.256) ↔ LiCoO₂(1.82–3.64)` 를 같은 그림으로 그릴 수 있다** — 추가 계산 0, 이미 둘 다 우리 db 에 있다. (⚠ 우리 창·그들 창을 **한 막대그래프에 섞지 말 것** — hull 세대가 다르다. 우리 값만으로 그린다.)
2. **"코팅은 점이 아니라 영역"** — 소결·확산·비정질화로 조성이 움직이므로 **안정영역의 폭**이 후보 품질이다. 우리 cascade 후보표에 **"조성 여유(composition margin)"** 열을 붙일 수 있다.
3. **양 끝 SOC 를 둘 다 걸어라** — #4 에서 이미 받은 교훈이 여기서도 반복된다.
4. **`|E_d| < 0.05` + "약간의 반응은 접착에 좋다"** — 0/1 대신 등급. 다만 그 완화가 어디까지 정당한지는 §10-1.

**이식 불가 5개**: ① `E_d` 절대값 ② LLZO 창 수치 ③ `Table 2` 후보 목록(전부 산화물, 황화물 무대에서 다시 계산해야 한다) ④ `Fig. S4` 의 군별 분포(특히 halides) ⑤ `Table S4` 전도도.

### 7c. ★ 전압축 계보 — #4 가 남긴 물음에 이 편이 답하는 만큼 (1저자 물음 #3)

| 층 | 무엇이 인쇄돼 있나 | 어디 |
|---|---|---|
| **형식화** | `μ_Li(φ) = μ⁰_Li − eφ`, 기준 = Li 금속 | ✅ **Methods 식 (5)** — 본문 |
| **개방계 분해에너지** | `E_D^open(C,φ) = E_eq(C,μ_Li) − E(C) − Δn_Li·μ_Li(φ)` | ✅ **Methods 식 (6)** — 본문 |
| **계면판(mutual)** | `ΔE_D,mutual^open` | ✅ **Methods 식 (7)** — 본문 |
| **한계(limit) 의 정의** | *"E_D^open 이 0 을 벗어나는 φ"* | ⛔ **없다** (#4 와 마찬가지) |
| **한계의 수치** | 89 Li-M-O + 130 이원 산화물 + LLZO/양극 13상태 | ✅ **Sup2 XLSX 열 + `Fig. S5`** (본문 미언급) |

⇒ **판정**: 우리 `2.256 V` 의 **직계 원전은 여전히 [Zhu15] → Mo/Ong/Ceder 2012** 다. 그러나 *"우리 onset 은 이 코팅 문헌 계보와 같은 틀"* 이라는 원고 문장은 **이제 [Nolan21] 식 (5)(6) 을 가리켜 쓸 수 있다** — 계보 8편 중 **그 식이 본문에 인쇄된 첫 편**이기 때문이다. (#1·#2 는 액체·닫힌계, #3 은 [Zhu15] 인용 승계, #4 는 그림 축뿐.)

🔑 **그리고 이 편은 우리가 즉시 할 수 있는 검증을 하나 준다**:
`Li₃PO₄` **0.69–4.20 V** · `Li₂SO₄` **1.57–4.66 V** · `Li₂CO₃` **1.27–4.10 V** · `LiAlO₂` **0.22–3.77 V** · `Li₂ZrO₃` **0.34–3.41 V** · `LiNbO₃` **1.74–3.87 V** (XLSX exact, μ_Li → V 변환).
**우리 `tools/oxidation` 로 `Li₃PO₄` 를 돌려 0.69/4.20 이 나오는지 보면, 우리 파이프라인이 Mo 그룹 인쇄값을 재현하는지가 한 번에 갈린다.** 계보 8편 중 **이런 대조가 가능한 편은 이것이 처음**이다(#4 는 값이 없었다). → §8-①.

### 7d. ★ 선정 규칙과 Li 전도체 배제 여부 (1저자 물음 #4)

| | [Aykol16] (#2) | [Nolan19] (#4) | **[Nolan21] (#5)** |
|---|---|---|---|
| 규칙 | `E_d < 3 V` **and** `−E_c > 3.5 V` (절대 문턱, 단위 **V**) | **`E_d = 0` 불리언** (eV/atom) | **`\|E_d\| < 0.05 eV/atom` 문턱** + 원소별 등급(Mg<0.003·Zr<0.005·Ti<0.03) |
| 통과율 | 5,225 → 2,229 (43 %) | 236종 × 8상태 중 8/8 안정 = **2종(0.85 %)** | **Li 삼원 89종 중 3상태 전부: Ed=0 16종(18 %) → \|Ed\|<0.05 53종(60 %)** |
| `Li₂ZrO₃` | ⛔ **탈락**(−E_c 3.5 V 컷) | 미평가 | ✅ **통과** — `Table 2` Zr 행 최종열 |
| `LiAlO₂` | ⛔ **탈락** | ✅ 통과 | ✅ **통과** — `Table 2` Al 행 최종열 |
| 전도도 축 | 없음 | 없음 | **없다. 다만 `Table S4` 로 자백한다** |

**답**: ① 규칙은 **완화됐다**(불리언 → 문턱, 그리고 *"약간의 반응은 접착에 좋다"* 라는 반대 방향 논거까지 붙었다). ② **[Aykol16] 의 함정(전도체를 컷으로 잘라버림)은 여기 없다** — `Li₂ZrO₃`·`LiAlO₂` 둘 다 살아남는다. ③ **그러나 다른 함정이 있다: 전도도를 보지 않는다.** 그리고 이건 우연이 아니라 **구조적**이다 — 이 논문의 두 제약(LLZO 와 안정하려면 μ_Li 높아야, d-NMC 와 안정하려면 μ_Li 낮아야)이 후보를 `Li₂O–MOₓ` 타이라인 위의 **닫힌껍질 광대역 산화물**로 몰아넣는데, 그게 정확히 **Li⁺ 이동도가 낮은 물질군**이다. 선택하는 성질과 원하는 성질이 서로 반대 방향이다 (§10-1).

### 7e. ⛔ 우리 db 절대값과 섞으면 안 되는 값 (1저자 물음 #5)

| 값 | 왜 금지 |
|---|---|
| `E_d` 전부 (`Table 1`·`Fig. 1`–`Fig. 4`·XLSX) | MP hull 세대가 다르고(2021 vs 우리 2026 pinned GGA_GGA+U), **SE 가 LLZO 다**. 우리 −0.3227 과 같은 표 금지 |
| `Fig. S5` 의 LLZO 창 **0 → 3.17 V** | ① figure-read ② 같은 계보 안에서도 [Zhu15] 는 LLZO 를 **0.05–2.91 V** 로 준다(0.26 V 차) — hull 세대 차가 이만큼이다 ③ 우리 2.256 V 와 **계가 다르다** |
| `Fig. S4` halides 중앙값 **≈ −0.16 eV/atom** | **Li-M-할라이드 vs LLZO** 다. "염화물은 나쁘다" 로 일반화하면 우리 LPSCl 의 Cl 에 오적용된다 |
| `Table S4` 전도도 | 문헌 취합 · 측정온도 혼재(RT/454 K/650 K) · 1건은 **그림에서 외삽** |
| 3 V·5 V `E_d^open` | XLSX 에 없다 = **figure-read 색뿐**. 주석 붙은 6점만 수치 |
| `Table S2`·`S3` 의 mutual Rxn. E. | μ_Li=−0.5 eV 행은 **끝점 해**(LLZO 비율 0.00) — "안정" 이 아니다 |
| 상평형 문자열의 `Li`·`O₂` | 개방계 저장조/기체 표기. **실제 석출물로 읽으면 안 된다** |

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

**① ★★★ 대조 잡 1건으로 우리 ESW 파이프라인을 Mo 그룹 인쇄값에 맞춰볼 수 있다 (추가 DFT 0)**
`tools/oxidation` 의 grand-potential 경로로 `Li₃PO₄`·`Li₂SO₄`·`Li₂CO₃`·`Li₂ZrO₃`·`LiAlO₂` 다섯을 돌려 [Nolan21] XLSX 의 **0.69–4.20 / 1.57–4.66 / 1.27–4.10 / 0.34–3.41 / 0.22–3.77 V** 와 대조한다. 맞으면 **우리 2.256 V 가 "같은 기계에서 나온 값" 이라는 주장이 실측으로 보강**되고, 어긋나면 그 차이가 곧 **hull 세대차의 크기**다(계보 카드가 #4 에서 남긴 물음 ③의 다른 버전). ⚠ 보고량 카드 먼저 — 비교 대상이 "한계 전위" 로 잘 정의되는지(둘 다 min-over-x 가 아니라 단일상 창인지) 확인할 것.

**② ★★ `Li₂SO₄`·`Li₃PO₄` 가 **두 번째** 독립 데이터셋에서도 최상위다 — CEI 자기부동태화 서사의 다리가 두 개가 됐다**
우리 `interface_reactivity_results.json` 의 `LPSCl|LiCoO₂` 최발열 산물은 `Co₉S₈ + Li₂SO₄ + Li₃PO₄ + Li₂S + LiCl` 다. [Nolan19] 에서 `Li₂SO₄` 는 양극 8상태 중 **8/8**, `Li₃PO₄` 는 **6/8** 로 1·2위였다. 이번 [Nolan21] 에서는 **전혀 다른 SE(LLZO) 상대로 다시** 둘 다 **LLZO·NMC·d-NMC 3상태 전부 E_d = 0** 인 16종에 들어간다. 게다가 XLSX 의 창이 **Li₃PO₄ 4.20 V · Li₂SO₄ 4.66 V** 로, **모체 SE(우리 2.256 V)보다 2 V 이상 높다**.
⇒ 원고 문장으로: *"계면에서 생기는 산화물 산물 자체가 모체 황화물보다 훨씬 넓은 전기화학 창을 갖는다 — 문헌의 독립 두 데이터셋에서 이 두 상은 층상 산화물 양극·가넷 SE 양쪽과 모두 열역학적으로 안정하다."* ⚠ 그들 수치는 **정성 근거로만**, 우리 수치와 같은 표 금지.

**③ ★★ `Li₂ZrO₃` 가 계보 안에서 갈린다 — 그리고 우리 계에 직접 닿는다**
[Aykol16] 은 `−E_c > 3.5 V` 로 `Li₂ZrO₃` 를 **잘랐고**, [Nolan21] 은 **최종 후보로 남긴다**(E_d: LLZO −0.0029 · NMC 0 · d-NMC −0.0165, 창 0.34–3.41 V). 그리고 계보 **#9 [Lu 2024]** 는 **바로 그 `Li₂ZrO₃` 를 Li₆PS₅Cl|Ni90 계면에 코팅해** 계면 Ea 를 0.624 → 0.429 eV 로 낮췄다. ⇒ *"같은 후보가 필터에 따라 죽었다 살았다 한다"* 는 것이 **필터 설계가 결론을 만든다**는 우리 cascade 규율의 문헌 사례다. 우리 cascade 대조표에 `Li₂ZrO₃` 행을 놓고 **[Aykol16] ⛔ / [Nolan21] ✅ / [Lu24] 실험 ✅** 세 칸을 나란히 두면 바로 쓸 수 있는 그림이 된다.

**④ ★ 우리 cascade 에 "조성 여유" 열을 붙일 근거가 생겼다 (추가 DFT 0~1)**
이 논문의 새 기여는 후보 목록이 아니라 *"코팅은 점이 아니라 영역"* 이라는 발상이다. 우리 후보(예: `Li₃PO₄`, `LiCl`, `B₂O₃`)마다 **Li-M-O(또는 Li-M-S) 삼각형에서 E_d ≈ 0 인 영역의 넓이**를 재면, "소결·확산으로 조성이 흔들려도 살아남는가" 를 한 숫자로 보고할 수 있다. pymatgen 만으로 되고, 우리 `interface_reactivity.py` 를 조성 격자 루프로 감싸면 된다.

**⑤ ★ `Fig. S5` 형식의 μ_Li 창 그림을 우리 값으로 그린다 (추가 DFT 0)**
우리는 이미 `comp1 1.242–2.256`·`modelc 1.242–2.256`·`+B₂O₃`·`LPSOCl` 를 갖고 있고, `LiCoO₂` 는 `interface_reactivity` 경로로 같은 코드에서 뽑을 수 있다. **한 막대그래프에 우리 계만** 올리면 "왜 코팅이 필요한가" 를 한 장으로 말할 수 있다 (하우스 스타일: 원소 팔레트 + gap 밴드 관례).

---

## 9. 인용 가능 문장 (deck/paper용)

- *"Thermodynamic screening of cathode coatings for garnet electrolytes defines the target quantity as the minimum mutual pseudo-binary decomposition energy `E_d = min_x ΔE_D,mutual(x)` in eV/atom, evaluated against both the lithiated and delithiated cathode, with the coating required to satisfy `|E_d| < 0.05 eV/atom` against **both** the electrolyte and the cathode [Nolan 2021, ESM 41, 571]."*
- *"In the same framework, the applied potential enters through `μ_Li(φ) = μ⁰_Li − eφ` referenced to Li metal, and the open-system decomposition energy `E_D^open(C,φ) = E_eq(C,μ_Li) − E(C) − Δn_Li·μ_Li(φ)` [Nolan 2021, Eqs. 5–6] — the same grand-potential construction underlying our oxidation onset."*
- *"The instability between a Li-rich oxide electrolyte and a high-energy layered cathode is intrinsic and originates from the mismatch of their equilibrium Li chemical potentials; the delithiated cathode is systematically the harder endpoint (LLZO–NMC 111: −87 → −132 meV/atom on delithiation) [Nolan 2021, Table 1]."*
- *"Coating candidates that are simultaneously compatible with a Li-rich electrolyte and a delithiated cathode are confined to a narrow composition window along the `Li₂O`–`MOₓ` tie-line [Nolan 2021, Figs. 2 and 4]."*
- ⚠ **쓰면 안 되는 문장**: *"가넷 연구에서 코팅 XX 가 4.2 V 까지 안정하다고 보고됐으므로 우리 황화물에서도…"* — 계가 다르고 hull 세대가 다르다. 반드시 *"in the garnet system, with Materials Project energies"* 를 붙인다.

---

## 10. 주의/한계 (over-claim 방지) — 본문↔그림/데이터 어긋남 **7건 포함**

**10-1. ★ 가장 큰 구멍: 선택하는 성질과 원하는 성질이 반대 방향인데, 논문은 그걸 각주로 처리한다**
논문의 두 제약은 코팅을 `Li₂O–MOₓ` 타이라인 위의 닫힌껍질 산화물로 몬다. `Table S4` 는 그 후보들이 **10⁻⁷ S/cm 이하**(LiAlO₂ ≈10⁻¹⁵, γ-Li₃PO₄ 10⁻¹⁸)임을 스스로 싣는다. 방어는 두 줄이다 — *"nm 두께면 된다"*, *"Li-Nb-O 도 빠른 전도체가 아닌데 잘 듣는다(ref 75)"*. **두 줄 다 근거가 약하다**: (i) 두께 논거에는 목표 면저항도, 허용 두께도, 터널링·공간전하 논의도 없다 — 정량이 0이다. (ii) LiNbO₃ 가 잘 듣는다는 것은 *"전도도가 낮아도 된다"* 의 증거가 아니라 *"실제 코팅은 비정질/오프스토이키오메트리라 결정 LiNbO₃ 의 전도도가 대표값이 아니다"* 의 증거일 수 있다 — 논문 자신이 §2.3 에서 그 말을 한다(Kato ref 35: Nb 금속이 리튬화돼 **비정질** LiNbO_x 가 된다). ⇒ **인용할 때 "열역학 단일축 스크리닝" 이라고 반드시 범위를 박는다.**

**10-2. ⚠ `Fig. 3` 오른쪽 주기율표 인셋의 군번호가 전부 1 씩 어긋나 있다** (4× 확대 재판독 확인)
인쇄된 열 머리는 `11 · 12 · 13 · 14` 인데 그 아래 칸은 **11 = Zn, 12 = B/Al/Ga, 13 = C/Si/Ge, 14 = N/P** 이다. 실제 IUPAC 군은 **Zn = 12, B/Al/Ga = 13, C/Si/Ge = 14, N/P = 15**. (구 CAS 표기로도 Zn 은 IIB = 12 다 — 어떤 관례로도 11 이 아니다.) 왼쪽 인셋(`4 · 5 · 6` ↔ Ti/Zr · V/Nb/Ta · Cr/Mo/W)은 **정확하다**. 과학적 결론에는 영향이 없지만, **이 인셋을 우리 슬라이드에 옮겨 그리면 오류가 따라온다.**

**10-3. ⚠ "전압을 걸면 LLZO-코팅 계면이 나빠진다" 는 자기 그림에 반례가 있다**
본문 §2.2: *"the LLZO-coating interface tends to be less stable at higher voltage, whereas the NMC-coating interface tends to be more stable."* 그런데 `Fig. S9a`(Li-Nb-O, 5 V vs LLZO)를 `Fig. 2b`(화학, vs LLZO)와 대조하면: `Nb₂O₅` **−0.135 → −0.03**(좋아짐) · `LiNbO₃` **−0.072 → −0.047**(좋아짐) · `Li₈Nb₂O₉` **0 → −0.057**(나빠짐). ⇒ **Li-rich 멤버만 나빠진다.** 이건 그들의 μ_Li 기구와 완벽히 일관되지만(전압↑ = μ_Li↓ = Li-rich 가 불리), **본문 문장은 그 조건을 빼고 일반화했다**. 우리가 인용하려면 *"for the Li-rich members"* 를 붙여야 한다.

**10-4. ⚠ 개방계 산물 문자열에 `Li` 금속과 `O₂` 기체가 고체와 같은 자격으로 들어간다**
`Fig. S9a` 는 **5 V** 에서 `LaNbO₄, **Li**, O₂, ZrO₂` 를 산물로 인쇄한다. `Table S2` 는 μ_Li = −2.75 ~ −4 eV(= 2.75–4 V)에서 `… **Li**, Li₂NiO₃, …` 를 인쇄한다. 이것은 **개방계 Li 저장조의 표기**이지 금속 Li 석출이 아니다 — 산화 조건에서 Li 금속이 나올 수는 없다. 우리 쪽은 같은 자리를 `Li⁺ + e⁻` 로 쓰므로 혼동이 없지만, **이 논문의 산물 목록을 그대로 옮기면 물리적으로 틀린 문장이 된다**. 그리고 [Aykol14] 의 **산물 물리상태 게이트**(기체·저융점 산물은 보호막이 못 된다)는 **#5 에서도 복원되지 않았다** — 계보 카드가 #4 에 물었던 것의 답이 #5 에서도 "아니오" 다.

**10-5. ⚠ `Fig. 1` 은 자기 데이터의 일부만 그린다 — 그리고 그 필터가 어디에도 안 적혀 있다**
XLSX 의 Li 삼원 산화물은 **89종**인데 `Fig. 1` 은 **67종**만 그린다(빠진 22종을 본 digest 가 전수 대조: `Li₂Eu₅O₈·Li₂MnO₃·Li₂NiO₃·Li₂Te₂O₅·Li₂TeO₃·Li₃CuO₃·Li₅BiO₅·Li₅ReO₆·Li₆CoO₄·LiBiO₃·**LiClO₄**·LiCoO₂·LiCrO₂·LiCuO·LiCuO₂·LiEu₃O₄·**LiIO₃**·LiNbO₂·LiReO₄·LiTi₂O₄·LiTiO₂·LiVO₂`). 그중 **5종은 "3상태 전부 Ed=0" 16종 안에 있다**(`LiClO₄`·`LiIO₃`·`Li₂MnO₃`·`Li₂NiO₃`·`LiCoO₂`). 즉 **자기 최우수 후보 16 중 5 를 헤드라인 그림에서 뺐다.** 짐작 가능한 이유는 있다(양극 물질 자신 / 과염소산염·요오드산염은 산화제) — **그런데 그 이유가 인쇄돼 있지 않다.** ⚠ [Aykol16] 의 `Fig. 1` 에서도 같은 "숨은 필터" 를 찾아냈다. 계보 전체의 패턴이다.
같은 그림에서 하나 더: **열 라벨이 `NMC,3V` 인데 짝이 `d-NMC,5V`** 로 비대칭인데, 캡션은 *"coating-LLZO and coating-NMC mixture under applied voltage 3 V and 5 V"* 라고만 쓴다. 물리적으로는 옳은 짝(방전=리튬화·저전압 / 충전=탈리튬·고전압)이지만 **캡션이 그 사실을 말하지 않는다**.

**10-6. ⚠ 공개 데이터 자체에 오기가 있다 (3건)**
- `Sup3` **electrochemical stability** 시트의 **Ta 행** `Ternary/NMC` 칸에 **`Li₄WO₅`** — W 행에서 복사된 값이다(Ta 화합물이 아니다).
- `Sup3` **echem < −60 meV** 시트의 Ta 행에 **`LaTaO₃`** — **Li 가 없는 상**이 "Li-M-O ternary" 목록에 들어 있다.
- 본문 `Table 2` 의 Ta 행이 **`La₃TaO₄`** 로 읽힌다 — 존재하지 않는 상. 문맥·XLSX 로 보아 **`Li₃TaO₄`** 여야 한다.
⇒ **Ta 계 결론은 쓰지 않는 것이 안전하다.**

**10-7. ⚠ 본문의 최종 원소 목록에서 Zr 가 빠졌다**
§2.4 마지막 문단: *"(M = B, C, N, Mg, Al, Si, P, Sc, Ti, V, Cr, Zn, Ga, Ge, Y, Nb, Mo, Ta, Sn, Sb, and W)"* — **21종**. `Table 2` 는 **22행**이고 **Zr 행의 최종열이 비어 있지 않다**(`ZrO₂, Li₆Zr₂O₇, Li₂ZrO₃`). 하필 `Li₂ZrO₃` 는 실제로 가장 많이 쓰이는 코팅 중 하나이고, **계보 #9 [Lu 2024] 가 우리 계(LPSCl|Ni90)에 실제로 쓴 물질**이다. ⇒ **본문 문장만 인용하면 Li₂ZrO₃ 를 놓친다. `Table 2` 를 봐야 한다.**

**10-8. ⚠ "LCO 가 LLZO 와 가장 안정하고 LMO 가 가장 불안정" 은 `Table 1` 이 반만 받쳐준다**
리튬화 상태에서 `LiCoO₂ = LiNiO₂ = LiMnO₂ = **0**` 으로 **셋이 동률**이다. 순위는 **탈리튬/스피넬 상태에서만** 생긴다(`Li₀.₅CoO₂ −21` < `Li₀.₅NiO₂ −35` < `LiMn₂O₄ −60`). 본문은 그 조건을 적지 않는다. (본문의 LMO 는 `LiMn₂O₄` 를 가리키므로 정의상 틀린 문장은 아니지만, `LiMnO₂` 가 0 인 것과 나란히 읽으면 오해를 부른다.)

**10-9. 방법 자체의 한계 (논문이 스스로 적는 것 + 우리가 더할 것)**
- 논문 자백: 0 K · 온도·시간·분위기·속도론 없음 · 실험 검증은 "기존 문헌과의 정성 일치" 뿐.
- 우리가 더할 것: **① 구조가 없다** — 조성만 다루므로 계면의 실제 원자배열·정합성·`W_ad`·두께가 전혀 안 들어온다. ② **무질서가 없다** — LLZO 의 Li 부분점유, NMC 의 TM 배열이 계산에 없다. ③ **`E_d = 0` 은 부동태화가 아니다** — 열역학 불리언이지 계면층 성장·저항을 말하지 않는다. ④ **DFT 파라미터가 한 줄도 없다** — MP 일관성에 전적으로 위임한다. 재현성 관점에서 이건 약점이다.

---

## 11. 용어 미니사전 (이 편을 읽는 데 필요한 것만)

| 용어 | 뜻 | 우리 쪽 대응 |
|---|---|---|
| **pseudo-binary** | 두 물질 A·B 를 몰비 x 로 섞은 가상의 이성분계. 계면을 "완전히 섞인 최악의 경우" 로 근사 | `InterfacialReactivity` 의 `x` 축 |
| **mutual decomposition energy** | 끝점 자체의 준안정성(`energy above hull`)을 뺀 분해에너지 — "둘이 만나서 *추가로*" 잃는 에너지 | `use_hull_energy=True` |
| **phase equilibria (E_eq)** | 같은 조성에서 가장 에너지가 낮은 상들의 집합 = convex hull 위의 분해 산물 | `PhaseDiagram.get_decomposition()` |
| **grand potential / open system** | Li 를 저장조와 교환할 수 있게 열어둔 계. 전압을 걸면 μ_Li 가 정해지고 평형 상집합이 바뀐다 | `GrandPotentialPhaseDiagram`, `get_element_profile` |
| **anodic / cathodic limit** | 그 물질이 산화/환원되기 시작하는 φ. 이 논문은 **μ_Li(eV) 로 기록**하고 `φ = −μ_Li/e` | 우리 `oxidation_limit 2.256 V` / `reduction_limit 1.242 V` |
| **Gibbs triangle heatmap** | 삼원계 조성공간을 삼각형으로 펼치고 각 점에 스칼라(E_d)를 색으로 | `python-ternary` |
| **tie-line** | 삼각형 안에서 두 상을 잇는 직선. 그 위의 조성은 두 상의 혼합으로 표현된다 | — |
| **d-NMC** | delithiated NMC = `Li₀.₅Ni₁₋ₓ₋ᵧMnₓCoᵧO₂` (충전 상태) | 우리 `Li₀.₅CoO₂` 대응 |
| **LLZO / LLSnO / LLNbO / LLTaO** | `Li₇La₃Zr₂O₁₂` / `Li₇La₃Sn₂O₁₂` / `Li₅La₃Nb₂O₁₂` / `Li₅La₃Ta₂O₁₂` | — |
| **La₂Zr₂O₇** | 파이로클로어. **LLZO 가 Li 를 잃었을 때의 잔해** — 이 논문의 "Li 손실" 지표 상 | 우리 계의 `Li₃PS₄`(LPSCl 가 Li 를 잃은 잔해)에 해당하는 자리 |

---

## 12. ★ 본 digest 의 독립 재분석 (Sup2/Sup3 XLSX 전수) — **논문에 인쇄돼 있지 않은 것**

> 방법: `tools/litdb/docx_to_text.py --xlsx` 로 6+3 시트를 텍스트화 → 파이썬 집계. 아래 숫자는 **논문의 어느 표·그림에도 없다.**

### 12a. 물질군별 E_d 분포 — `Fig. S4` 를 **exact 로 승격**

| 데이터셋 | n | 중앙값 E_d (eV/atom) | 평균 | 최솟값 | `E_d = 0` 비율 |
|---|---|---|---|---|---|
| **Li 삼원 산화물 vs LLZO** | 89 | **0.0000** | −0.0243 | −0.1939 (`LiPO₃`) | **54/89 (61 %)** |
| 이원 산화물 vs LLZO | 130 | −0.0389 | — | −0.7611 | 46/130 (35 %) |
| Li 삼원 산화물 vs NMC 111 | 89 | **0.0000** | — | −0.2244 | 64/89 (72 %) |
| Li 삼원 산화물 vs **d-NMC 111** | 89 | **−0.0116** | — | −0.3127 | **39/89 (44 %)** |
| 이원 산화물 vs NMC / d-NMC | 129 | −0.0348 / −0.0476 | — | −0.8888 / −1.2454 | 38 / 36 |
| **원소 vs NMC / d-NMC** | 62 | **−0.5220 / −0.7419** | — | −1.2029 / −1.6955 | 5 / **0** |

🔑 `Fig. S4` 캡션의 *"lithium ternary oxides have the lowest median reaction energy with LLZO, at approximately 0 eV/atom"* 은 **정확히 맞다 — 중앙값이 0.0000 이다**(figure-read 로는 판정이 애매했는데 원자료로 확정).
🔑 **원소(금속)는 d-NMC 와 62종 중 0종이 안정**하다. 금속 중간층은 탈리튬 양극과 절대 양립하지 않는다.

### 12b. ★ "3상태 전부 안정" 목록 — **논문이 인쇄하지 않은 목록**

| 기준 | n / 89 | 목록 |
|---|---|---|
| **`E_d = 0` with LLZO **and** NMC 111 **and** d-NMC 111** | **16 (18 %)** | `Li₂CO₃` · `Li₂CrO₄` · `Li₂MnO₃` · `Li₂NiO₃` · **`Li₂SO₄`** · `Li₂SnO₃` · **`Li₃PO₄`** · `Li₃TaO₄` · `Li₃VO₄` · `Li₄WO₅` · `LiAlO₂` · `LiClO₄` · `LiCoO₂` · `LiGaO₂` · `LiIO₃` · `LiNO₃` |
| `\|E_d\| < 0.05` with all three (= `Table 2` 기준) | **53 (60 %)** | (53종 — `Li₂ZrO₃`·`Li₂SiO₃`·`Li₃BO₃`·`Li₈Nb₂O₉`·`Li₄TiO₄` 등 포함) |

⇒ **#4 의 불리언(18 %) → #5 의 문턱(60 %) 으로 후보가 3.3배가 된다.** 규칙 완화의 크기를 수치로 말할 수 있다.
⇒ 🔑 **우리 `LPSCl|LiCoO₂` 계면 산물 중 산화물 2종(`Li₂SO₄`·`Li₃PO₄`)이 이번에도 16종 안에 있다.** [Nolan19] 에 이어 **두 번째 독립 데이터셋**이다.

### 12c. ★ Li 함량 규칙의 정량화 — **논문은 색으로만 말한다**

본문 §2.2 주장: *"Li 함량이 높으면 LLZO 와 안정, 낮으면 NMC(특히 d-NMC)와 안정"*.

**(i) Pearson r** (Li 원자분율 vs E_d, n = 89):

| 상대 | r |
|---|---|
| LLZO | **+0.572** (Li 많을수록 **덜** 반응) ✔ 주장대로 |
| NMC 111 | **+0.291** (여전히 +) ✖ 주장과 반대 방향 |
| **d-NMC 111** | **−0.002** (무상관) ✖ |

**(ii) 그런데 중앙값·안정비율로 가르면 주장이 정확히 성립한다** — 경계를 **LLZO 자신의 Li 분율 7/24 = 0.292** 로 잡으면:

| Li 원자분율 | n | `E_d = 0` with **LLZO** | with NMC 111 | with **d-NMC 111** |
|---|---|---|---|---|
| **< 7/24** (LLZO 보다 Li-poor) | 46 | 45 % | 52 % | **52 %** |
| **≥ 7/24** (LLZO 보다 Li-rich) | 43 | **76 %** | 93 % | **34 %** |

⇒ **Li-rich 로 가면 LLZO 와는 45 → 76 % 로 좋아지고, 탈리튬 NMC 와는 52 → 34 % 로 나빠진다.** 이것이 "모순되는 요구" 의 숫자다.
⇒ 🔑 **그리고 리튬화 NMC 와는 오히려 52 → 93 % 로 *좋아진다*.** 즉 **갈등은 "양극" 이 아니라 "충전된 양극" 과의 갈등**이다 — 논문 본문보다 한 단계 날카로운 진술이고, 우리 `LiCoO₂ → Li₀.₅CoO₂` 확장(§8-①)의 동기를 강화한다.
⇒ Pearson r 이 실패하는 이유: 분포가 **0 에 심하게 몰려 있고(zero-inflated)**, 가장 음수인 꼬리가 **양쪽 상대 모두에서 Li-poor 쪽에 있다**. 선형상관은 이런 분포에서 방향을 잘못 짚는다. (⚠ 우리 쪽 스크리닝 보고에도 같은 함정이 있다 — 중앙값/비율을 같이 낸다.)

### 12d. ★ ESW 창의 계 전체 통계 — **논문에 한 줄도 없다**

Li 삼원 산화물 89종의 XLSX `anodic/cathodic limit` 열(μ_Li → V 변환):

| 지표 | 값 |
|---|---|
| **anodic limit 중앙값** | **3.57 V** (범위 **1.11 – 5.23 V**) |
| cathodic limit 중앙값 | **1.36 V** |
| 산화 상위 5 | `Li₂S₂O₇` 5.23 · `LiSb₃O₈` 5.18 · `LiPO₃` 5.02 · `Li₂Se₂O₇` 4.86 · `LiNO₃` 4.81 V |
| Li 분율 ↔ anodic limit 상관 | **r = +0.319**(Li 많을수록 μ 가 덜 음수 = **산화전위가 낮다**) |

🔑 [Nolan19] 은 *"대부분 산화물의 산화한계 3.5–4 V"* 라고 boxplot 으로만 말했는데, **여기 원자료 중앙값이 3.57 V** 다 — 그 서술의 수치 근거가 이 편의 XLSX 에 있다.
🔑 `Li₃PO₄` **0.69–4.20 V** 가 [Zhu15] 인쇄값 0.68–4.21 V 를 재현 ⇒ **이 열이 우리 2.256 V 와 같은 수치 체계임이 독립 확인된다**(§4d).

### 12e. 재현 대조 3건 (그림 주석 ↔ XLSX)

| 그림 주석 | XLSX | 판정 |
|---|---|---|
| `Fig. 2a` `Al₂O₃` E_d = **−0.094**, → La₂Zr₂O₇, LaAlO₃, LiAlO₂ | −0.09412, 같은 산물 | ✅ |
| `Fig. 2b` `Nb₂O₅` **−0.135** → LaNbO₄, Li₃NbO₄, ZrO₂ | −0.13457, 같은 산물 | ✅ |
| 본문 "Al–LLZO pseudo-binary **−181 meV/atom**" | 원소 Al: −0.18089 → LaAl₃, Li₅AlO₄, ZrAl₃, LiAlO₂ | ✅ |
| `Fig. S5` `LiCoO₂` 막대 끝 (픽셀 판독) −1.817 / −3.651 | −1.82199 / −3.64086 | ✅ (1 px 이내) |

⇒ **그림 주석과 공개 데이터는 서로 일치한다.** ([Nolan19] 에서는 `Table S1` 40종 중 8종이 XLSX 에 없었다 — 이 편은 그 문제가 없다.) 어긋나는 것은 **본문 서술**과 **일부 라벨**이다(§10).

---

## 13. 한 줄 결론

**#5 는 #4 와 같은 기계를 가넷 무대로 옮기면서 세 가지를 더했다 — 전압 인가 개방계 식(우리 ESW 정의가 이 계보에서 처음 인쇄된 곳), 조성공간 지도(점이 아니라 영역), 문턱형 선정 규칙.** 우리가 실제로 가져갈 것은 후보 목록이 아니라 **① `Li₃PO₄` 창 0.69–4.20 V 를 우리 코드로 재현하는 대조 잡 ② μ_Li 창 그림 형식 ③ "갈등의 상대는 양극이 아니라 *충전된* 양극" 이라는 정량 진술** 셋이다. 그리고 이 편이 남긴 경고가 하나 있다 — **열역학 한 축으로 후보를 고르면, 그 축이 이온전도성과 반대 방향일 때 아무도 알려주지 않는다.**
</content>
</invoke>

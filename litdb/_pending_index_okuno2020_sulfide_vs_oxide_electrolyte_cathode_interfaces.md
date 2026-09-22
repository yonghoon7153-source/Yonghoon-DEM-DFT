# ⏸ 병합 대기 — `okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces`

> **왜 이 파일이 있나.** 2026-09-22 현재 다른 에이전트가 `litdb/INDEX.md` · `litdb/comparison_vs_ours.md` ·
> `db/literature/refs.json` 세 파일을 병합 중이라, 이번 digest 작업은 **`papers/<slug>.md` 와 이 파일 둘만**
> 썼다. 아래 블록을 **그대로 잘라 넣으면** 병합이 끝난다.
>
> digest 원본: `litdb/papers/okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces.md`
> 그림: `litdb/figures/okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces/` (그림 38 + 표 13, **그림 9장 실독**)
>
> 🔴 **이 논문의 1번 성과는 값 추가가 아니라 *값 철회*다.**
> **`W_ad(황화물) = 0.8 J/m²` 는 Okuno 2020 에도, Haruyama 2014 에도 없다.** 아래 ④ 를 반드시 같이 처리한다.

---

## ① `INDEX.md` **`## ✅ Digest 완료 (paper-level)`** 절에 추가할 행

(`barai2021_delamination_cathode_llzo_multiscale` 행 **바로 위**가 자연스럽다 — 0.8 의 원전 검증이라 붙어 있는 게 낫다.)

| slug | 논문 | 축 |
|---|---|---|
| `papers/okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces.md` **(본문 12 pp + SI 22 pp — 크롭 51장 중 본문 그림 9장 실독)** | **[외부·⭐⭐ Tateyama 3부작의 완결편 · 🔴 우리 `W_ad = 0.8 J/m²` 각주를 *부인*하는 편]** ✅ **Yukihiro Okuno\***(**FUJIFILM**)/**Jun Haruyama**(東大 ISSP)/**Yoshitaka Tateyama\***(NIMS+京大), "**Comparative Study on Sulfide and Oxide Electrolyte Interfaces with Cathodes in All-Solid-State Battery via First-Principles Calculations**" (***ACS Appl. Energy Mater.* 3, 11061–11072 (2020)**, DOI 10.1021/acsaem.0c02033, **open access**; MEXT **Fugaku 배터리 프로젝트** + KAKENHI JP19H05815; **K computer**; `Fig. 1`–`16` (본문 표 **0개**) + `Fig. S1`–`S23` + `Table S1`–`S13`). **계 = LiCoO₂((104)·(110)) × β-Li₃PS₄(010) / γ-Li₃PO₄(001·010) / LLZO(001) + 버퍼 Li₄Ti₅O₁₂(111) = 계면 8종**. **보고량 = 자리별 Li 공공 형성에너지 `E_f(V_Li_j)` 의 *분포*(총 271자리) + 상호 양이온 교환에너지 `E_ex` + PDOS 밴드오프셋** (⛔ **NEB·MD·AIMD·Bader·COHP·ELF·ESW·포논·탄성 전부 0회** — `NEB`/`barrier`/`molecular dynamics` 전수 grep 0건). **방법**: QE·PBE·**USPP**·**40/320 Ry**·**U(Co 3d)=4.9 eV**(⚠ Haruyama 2014 는 **5.9**)·Ti/Zr/La **U 없음**·**spin-unpolarized**·Gaussian **0.001 Ry**·중성셀·진공 **1–1.5 nm**·슬랩 **1–2 nm**·**k = Γ-only 또는 2×1×1 (계면마다 다름)**·⛔ **힘·응력·에너지 수렴기준 0건 · 이완 자유도 0건 · β-Li₃PS₄ 무질서 처리 0건 · QE 버전 0건**. **★ 결과**: ① ***우리 산수* 저(低)E_f 사다리(논문 미보고)** — `E_f < 2.0 eV` 자리 비율 **LPS(110) 30.4 % > LPS(104) 18.5 % ≫ LLZO 6.2 % > LPO(001) 2.8 % > LPO(010) 0 % = LTO/LPS 0 % = LCO/LTO 0 %** (막대→자리수 환산이 캡션의 65/23/28/36 과 **정확히 일치** = 읽기 자체검증) ② **기전 = 가전자대 오프셋** — LPO **≈1 eV**, LLZO **≈0.2 eV**(둘 다 본문 명시, `Fig. 7`·`Fig. 11` 실독 일치), LPS **`figure-read ≈ 0.1–0.5 eV`**(논문 미보고) ③ **면방위가 레버** — (110) 이 (104) 보다 저E_f 자리 **1.6배**, Co↔P 교환 **−1.25 → ≈−2 eV** ④ **양이온 혼합이 Li 고갈을 가속** — Co↔P 6개 혼합 후 같은 자리 `E_f` **2.40→1.39 · 2.27→1.12** (`Table S4`, *우리 산수* 평균 **2.278 → 1.558, −0.72 eV**) ⑤ **LTO 버퍼가 LPS 쪽 E_f 를 벌크로 복귀**(**2.95–3.05** vs 벌크 2.9–3.2, 2.0 미만 0개). **🔴🔴 W_ad 는 4개뿐이고 단위는 eV/Å² 다**: LCO(104)/LPS **0.025** · LCO(104)/LPO(010) **0.028** · LCO(104)/LPO(001) **0.021** · LTO(111)/LPS **0.019** (*우리 산수* ×16.0218 = **0.400 / 0.449 / 0.337 / 0.304 J/m²**) — ⛔ **LCO(110)/LPS·LCO/LLZO·LCO/LTO 의 W_ad 는 아예 없다** ⇒ **`0.8 J/m²` 는 이 논문에 없다**(아래 ④). **🎉 [Haru14] 의 최대 공백을 메운다** — **8계면 전부의 총 원자수·성분별 원자수·반복수·μ 가 SI 에 있다**: LCO(104)/LPS **696** · **LCO(110)/LPS 736**(본문 "756" 은 오타) · LCO(104)/LPO(001) **888** · LCO(104)/LPO(010) **760** · LCO(110)/LPO(010) **384** · LCO(104)/LLZO **448** · LTO/LPS **1056** · LCO/LTO **424**. *우리 산수* 로 misfit 을 역검산해 셀을 복원했다(**LCO(104)/LPS μ 8.90 % ↔ 논문 8.9 ✓**, **LCO(110)/LPS μ 4.51 % ↔ 4.6 ✓**) ⇒ **LCO(110)/LPS = LCO 8층 11.34 Å(480원자) + LPS 2셀 16.32 Å(256원자), 면적 ≈320–345 Å², 법선 ≈38–45 Å** — **우리 `haruyama2014` digest 가 그림에서 재서 추정한 ≈736 원자·≈43 Å 과 원자 단위로 일치**. 🔴 **비판 15건**(digest §10): ① **W_ad 를 4개만, 결론이 걸린 (110) 은 빼고** 준다 ② **`Fig. 2` 패널 라벨이 캡션과 뒤바뀜**(그림 안 라벨이 맞다 — 실독) ③ **표본 개수가 본문↔캡션↔SI 에서 세 번 어긋남**(LPS: 본문 3/8, 캡션 8/3, SI 8/4 · LPO: 본문 5/4, 캡션 4/5) ④ **면방위 비교가 서로 다른 k-격자**(104=Γ-only vs 110=2×1×1)에서 이뤄짐 + *"LCO(110)/LPO(001)"* 은 **존재하지 않는 계면** ⑤ **VBO 단일기전 주장이 자기 숫자와 비단조**(LLZO 0.2 eV < LPS 인데 저E_f 는 LLZO 가 1/3–1/5) ⑥ **구조 표본 산포가 W_ad 보다 크다** — *우리 산수* ΔE/S ÷ W_ad = **21 % / 82 % / 495 %**, LCO(104)/LPO(001) 은 최고구조를 골랐으면 **W_ad 음수** ⑦ **중갭 상태가 *진공면*("LCO vac") 기여 우세인데 본문은 *계면* 탓** (`Fig. 3` 90 vs 35, `Fig. 7` 100 vs 40 — 실독) + `Fig. 3` **영점이 자기 캡션("갭 중심")과 불일치** ⑧ **무질서 미선언** — β-Li₃PS₄ Li 배열 0줄이고 **격자가 [Haru14] 와 1–2 % 다르다**; LLZO 공공 50/40 % 는 **정수 해가 없다** ⑨ **SI 복붙 오류 8건**(506↔504 · 756↔736 · LCO(110) 단위 `2.815`→**4.910** · "LCO(104)/LTO 의 μ" 오지정 · "LPS 를 LCO 에 맞춤"(그 계면에 LCO 없음) · "LTO and LPS units"(LCO and LTO) · LCO(104) 단위 18 vs 16 · "ZrO₆ tetrahedrons") ⑩ **다른 논문(U=5.9)의 값과 직접 비교해 "LNO > LTO" 결론 — *우리 산수* 로는 반대**(LPS 쪽 평균 LNO 2.95 vs LTO 2.994, 최소 2.42 vs 2.95) ⑪ **수렴·이완 조건 전무**(2014 보다 후퇴) ⑫ **재현 불가**(좌표·원시에너지·히스토그램 원자료 전무) ⑬ **`E_f` 는 밴드정렬 성분이 섞인 양** ⑭ **반응 동역학 0**(배리어 없음 — 저자 자인) ⑮ **실험 대조 0회**(전부 타 문헌 인용). **계보**: [Haru14] → [Haru17] → **본 편**, 그리고 ref 24 = **[Gao20]** Gao·Jalem·Ma·Tateyama *Chem. Mater.* **32**, 85 (2020)(계면 구조예측 자동화 — **확보 후보 1순위**), ref 60/S8 = **Butler·Sai Gautam·Canepa 2019**(W_ad 정의 원전, `wang2022_…` 와 같은 계보). **⛔ 이식 금지**: E_f·E_ex·W_ad 절대값(β-Li₃PS₄·LiCoO₂ 전용) · 갭(**벌크 갭이 논문에 0개**) · *"LNO > LTO"* | **🆕 계면 보고량 설계(분포 통계) 원전 · 면방위 의존성 원전 · [Haru14] 셀 수치의 *공개본* · 🔴 `0.8 J/m²` 부인** |

---

## ② `comparison_vs_ours.md` **`## 📑 Reference key (출처 약칭)`** 에 추가할 행

| 약칭 | 출처 | digest |
|---|---|---|
| **[Okuno20]** | Okuno, Haruyama, Tateyama, *ACS Appl. Energy Mater.* **3**, 11061–11072 (2020), DOI `10.1021/acsaem.0c02033` (open access) | `papers/okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces.md` |

---

## ③ `comparison_vs_ours.md` **물성 4축(A/B/C/D)** 에 넣을 것 — **없다**

이 편은 **우리 4축(이온전도·산화안정·기계·전자구조) 어디에도 수치로 들어가지 않는다.**

| 축 | 이유 |
|---|---|
| **A 이온전도** | **NEB·MD 0회.** Ea·σ·D 가 **한 개도 없다**. 인용된 σ 하나(**1.64×10⁻⁴ S/cm**, 나노다공성 LPS)는 **ref 41 Liu 2013 실험값**이지 이 논문 계산값이 아니다 |
| **B 산화안정 4축** | **grand-potential 0회 · ESW 0회.** 축 ④(계면 반응)에 **정성** 기여만 있고, LPS 분해산물(P₂S₇·Co(PO₃)₂·Co₂S)조차 **ref 30 Richards/Ceder 인용**이다. ⛔ 우리 축 ①(S²⁻ 산화, 2.256 V)과 **같은 양이 아니다** |
| **C 기계** | **탄성 0회.** *"the rather low elastic modulus of LPS"* 라는 **정성 한 줄**이 전부 (격자 정합 방향의 근거로만 쓰임) |
| **D 전자구조** | 🔴 **벌크 밴드갭이 0개다** — `Table S1` 에 E_g 열이 없다([Haru14] 에는 있었다). 계면 실효갭은 `figure-read ≈ 0.8/0.9/0.95 eV` 뿐이고 **계(계면 vs 벌크)·물질·판독법이 전부 다르다** ⇒ 우리 comp1 2.066 / modelc 2.099 와 **숫자 비교 금지** |

⇒ **§J 의 🔧 방법 원전 블록으로 간다** (아래 ⑤).

---

## ④ 🔴🔴 **정정 제안 — `W_ad(황화물) = 0.8 J/m²` 의 귀속** (내가 직접 안 고쳤다)

### ④-1. 사실관계 (전수 확인)

| 항목 | 확인 결과 |
|---|---|
| **Okuno 2020 본문·SI 전문에 `J/m²` 표기** | **0건** (`J/m`·`J m`·`fracture`·`toughness` 전수 grep) |
| **Okuno 2020 의 W_ad 전수** | **4개뿐, 단위 eV/Å²** — LCO(104)/LPS **0.025** · LCO(104)/LPO(010) **0.028** · LCO(104)/LPO(001) **0.021** · LTO(111)/LPS **0.019** |
| **환산** (*우리 산수*, 1 eV/Å² = 16.02177 J/m²) | **0.4005 / 0.4486 / 0.3365 / 0.3044 J/m²** |
| **황화물 계면 값** | **0.4005 J/m² 하나.** **0.8 의 정확히 절반** |
| **LCO(110)/LPS(010) 의 W_ad** | ⛔ **보고되지 않음** — Barai 가 *"thiophosphate (Li₃PS₄) structure"* 로 지목한 바로 그 계면인데 값이 없다 |
| **Haruyama 2014 의 LCO(110)/LPS W_ad** | **4.3 eV/nm² = 0.043 eV/Å² = 0.6889 J/m²** — **0.8 이 아니다** |
| **Barai 2021 원문** (`inbox/11._Investigation_of_delamination…MAIN.pdf`) | *"The bottom stability limit corresponds to sulfide-based electrolytes, which shows smaller magnitudes of fracture energy at the cathode/electrolyte interface, **around 0.8 J/m².⁶⁹,⁷⁰** … sulfide electrolytes with thiophosphate (Li₃PS₄) structure are being considered.**⁶⁹**"* · **ref 69 = Haruyama 2014**, **ref 70 = Okuno 2020** |

> **판정: `0.8 J/m²` 는 Barai 2021 이 채택한 수이고, 인용된 두 원전 어디에도 그 값이 없다.**
> 재구성 가능한 경로는 ⓐ **Okuno 0.4005 × 2** (= 0.801 — 자유표면 2개로 잘못 센 경우) 또는 ⓑ **Haruyama 0.689 를 "around 0.8" 로 올려 읽은 것** 이고, **어느 쪽도 논문이 지지하지 않는다.**
> 그리고 **정의가 셋 다 다르다**: Okuno/Haruyama = **0 K 정적 DFT 정합계면의 *부착일***, Barai Ψ_t = **연속체 lattice-spring 의 *난수 파단문턱***, Barai 산화물 2.0 = **자기 DFT NMC/LLZO 벽개에너지**.

### ④-2. `litdb/INDEX.md` — barai2021 행 정정 **제안 문구** (직접 안 고쳤다)

**현재** (line 39 근처):
> `… 안정한계선 **Ψ_t 2.0(산화물) / 0.8 J/m²(황화물, ref 70 Okuno 2020)** …`

**제안**:
> `… 안정한계선 **Ψ_t 2.0(산화물, 자체 DFT) / 0.8 J/m²(황화물 — ⚠ Barai 채택값. refs 69/70 에 귀속돼 있으나 두 원전 어디에도 0.8 은 없다: Haruyama 2014 = 0.689 J/m²(LCO(110)|LPS), Okuno 2020 = 0.400 J/m²(LCO(104)|LPS, 0.8 의 정확히 절반), 그리고 Okuno 는 (110)|LPS 의 W_ad 를 아예 보고하지 않는다 — `papers/okuno2020_…` §3g·§11-①)** …`

그리고 같은 행 끝의 **🟠 Nd 인산염 판정** 부분:
> **현재**: *우리 산수* √(2.0/0.8) = **1.58**
> **제안**: *우리 산수* √(2.0/0.8) = **1.58** ⚠ **분모 0.8 이 문헌값이 아니다** — 문헌 실측치로 바꾸면 √(2.0/0.689) = **1.70**(Haruyama) 또는 √(2.0/0.400) = **2.24**(Okuno) 로 **결론 크기가 최대 41 % 커진다.** ⇒ **이 비교는 분모 선택에 민감하므로, 원고에 쓰려면 분모를 명시하고 두 경우를 같이 보여야 한다.**

### ④-3. `litdb/papers/barai2021_delamination_cathode_llzo_multiscale.md` 정정 **제안** (직접 안 고쳤다)

- **line 44 · 72 · 207 · 445 · 530 · 598** 의 `0.8 J/m²` 마다 **`(⚠ Barai 채택값 — 원전 미확인, → okuno2020 §3g)`** 을 붙인다.
- **line 659** 의 "확보 후보" 행(Okuno = *"0.8 J/m² 출처"*)을 **`✅ 확보·digest 완료 — 결론: 이 논문에 0.8 은 없다(0.400 J/m² · (110)|LPS 는 미보고). papers/okuno2020_… §3g`** 로 바꾼다.
- **§9 인용문장**(line 598)의 *"(≈0.8 vs ≈2.0 J m⁻²)"* 는 **그대로 두되** *"[Barai 2021 이 채택한 값; 인용된 1차 문헌에는 0.689 / 0.400 J m⁻² 만 있다]"* 를 붙인다.

### ④-4. `db/literature/refs.json` 정정 **제안 문구** (직접 안 고쳤다)

> ⚠ `refs.json` 에는 **Okuno 항목이 없다**(전수 grep 0건). 아래는 **기존 haruyama2014 항목(`references[37]` 계열)의 주석 정정 제안**이다.

**(가) `_relative_to_us` (line 2031 부근)**
- **현재**: `"Our paper #1 v5 LiNiO2/LPSCl comp1 = 1.28 J/m² is ~2× their LCO/LPS = 0.69 J/m². Reasonable: LiNiO2 more reactive than LCO per Komatsu (-424 vs -321 meV/atom)."`
- **제안**: `"Our v5 comp1 = 1.28 J/m² (UMA MLIP, FixAtoms 33%, vacuum 30 A, xy-shift best-of / 20-seed mean 1.153+-0.392) vs their 0.689 J/m² (DFT+U, U_Co=5.9 eV, LCO(110)|LPS, all-atom relax, vacuum 15 A, lowest of 4 lateral samples). RATIO NOT INTERPRETABLE AS CHEMISTRY: the same group's Okuno 2020 (DFT+U, U_Co=4.9 eV) gives 0.400 J/m² for LCO(104)|LPS - i.e. literature-internal spread is 1.72x from facet+U alone, and Okuno reports NO W_ad for LCO(110)|LPS. Uncontrolled axes between us and them: force engine (MLIP vs DFT+U), cathode (LiNiO2 vs LiCoO2), SE (Li6PS5Cl vs beta-Li3PS4), cathode facet (ours unrecorded vs theirs (104)/(110)), relaxation DOF (FixAtoms 33% vs unspecified/all-free), vacuum (30 vs 10-15 A), representative-value rule (best-of vs 20-seed mean/median 0.962). The former 'LiNiO2 more reactive than LCO per Komatsu' attribution is WITHDRAWN - method axes were not controlled. See litdb/papers/okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces.md 7a-2."`

**(나) `Quantitative anchor` (line 2075 부근)**
- **현재**: `"Quantitative anchor: Haruyama LCO/LPS = 0.69 J/m². Our LiNiO2/LPSCl 1.28 (paper #1 v5) = 1.86× - consistent with LiNiO2 more reactive than LCO (Komatsu Ni > Co reactivity ranking)."`
- **제안**: `"Literature anchors for sulfide|oxide-cathode W_ad, SAME definition (E_A+E_B-E_AB)/S, same group, same code: Haruyama 2014 LCO(110)|beta-Li3PS4 = 4.3 eV/nm2 = 0.689 J/m2 (U_Co 5.9 eV); Okuno 2020 LCO(104)|beta-Li3PS4 = 0.025 eV/A2 = 0.400 J/m2 (U_Co 4.9 eV). Spread 1.72x within the literature itself. Use as RANGE (0.40-0.69 J/m2), never as a single anchor, and never to attribute our 1.28 to Ni-vs-Co chemistry."`

**(다) 신규 항목 추가 제안** — `references[]` 에 Okuno 2020 을 **새 항목**으로 넣는다 (골격만):
```
{ "authors": "Okuno, Y.; Haruyama, J.; Tateyama, Y.",
  "title": "Comparative Study on Sulfide and Oxide Electrolyte Interfaces with Cathodes in All-Solid-State Battery via First-Principles Calculations",
  "journal": "ACS Appl. Energy Mater.", "volume": 3, "pages": "11061-11072", "year": 2020,
  "doi": "10.1021/acsaem.0c02033", "open_access": true,
  "litdb_digest": "litdb/papers/okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces.md",
  "role": ["method-anchor-SECONDARY(single-interface+vacuum, W_ad formula)",
           "geometry-disclosure(nat/slab-thickness for the Haruyama2014 LCO(110)|LPS cell = 736 atoms)",
           "CITATION-CORRECTION(does NOT contain 0.8 J/m2)"],
  "prohibitions": ["do not cite 0.8 J/m2 to this paper",
                   "do not cite a W_ad for LCO(110)|LPS - not reported",
                   "do not transport E_f / E_ex / W_ad absolute values (beta-Li3PS4 + LiCoO2 only)",
                   "no band gaps exist in this paper",
                   "do not cite 'LNO buffer superior to LTO' - contradicted by the paper's own numbers"] }
```

---

## ⑤ `comparison_vs_ours.md` **§J** 에 넣을 🔧 방법 원전 블록

### J-(배정). 🔧 **방법 원전 — [Okuno20] 계면 보고량을 *분포*로 정의하는 법 + 우리 v5 기하의 공개 검산본** (2026-09-22 신설)

> ⛔ **물성 4축 아님.** 이 편에는 Ea·σ·D·ESW·탄성·벌크 갭이 **하나도 없다**. 여기 두는 이유는 **보고량 설계**와 **기하 수치** 때문이다.

| 항목 | **[Okuno20] 이 하는 것** | **우리 현재** | 판정 |
|---|---|---|---|
| **계면 보고량의 형태** | **분포**. 계면당 구조 **3–8개** × 자리 **23–65개** → 히스토그램 + 스칼라 요약(*"E_f < 2.0 eV 비율"*). 저자 문장: *"Calculating the **statistics** of the physical properties is important to obtain reliable results."* | 우리 W_ad 는 **20 seeds 를 돌려 놓고 대표값을 best-of 로 쓴다**(`adhesion_final.md` comp1 1.28 vs 20-seed 평균 1.153 / 중앙값 0.962) | 🔴 **우리가 표본은 더 많은데 집계 규칙이 없다.** 보고량 카드에 **대표값 규칙**을 박아야 한다 |
| **자리 정의** | 계면 수직 방향 각 Li 층에서 뽑음. 라벨 체계 `LC*`(양극) / `LP*`·`LZ*`·`LT*`(SE·버퍼) | 우리 계면 Li 자리 분류 체계 **없음** | ⭕ **그대로 차용 가능** |
| **결함 기준상태** | `E_f = {E_tot(V_Li) + E_Li} − E_tot`, **E_Li = bcc Li 금속**, **중성 셀**. 저자 단서: *"valid when the electron can be extracted simultaneously"* | 우리 원장에 **계면 Li 공공 형성에너지 0건** | ⭕ **우리가 안 가진 축** |
| **양이온 교환** | `E_ex = E_tot(A↔B) − E_tot`, **조성 보존 in-place 스왑** (화학퍼텐셜 불필요). Co↔P(1층) **−0.76 / −1.25 / −1.00 eV**, Co↔Li **+2.25 ~ +3.31 eV** | 우리 원장에 **0건** | ⭕ **grand-potential 계면 확장보다 싸다.** 우리만 물을 수 있는 축: **Cl↔O · Cl↔S** |
| **면방위** | **(104) vs (110) 을 둘 다 돌려 비교** — 저E_f 비율 **18.5 → 30.4 %**, Co↔P **−1.25 → ≈−2 eV** | 🔴 **v5 보고서에 NCM 면지수가 없다**(v26/v27 만 (003)/(110)/(012)/(104)) | 🔴 **우리 최대 미기재 항목.** 면을 확정하기 전엔 문헌 W_ad 와 비율 비교 금지 |
| **단일계면 + 진공** | ✅ 채택. 단 논거는 *"a supercell without a vacuum usually involves **two interfaces, atomically different**"* 한 줄뿐 — **[Haru14] 의 "계면 분극 간 인공 상호작용" 논거는 빠졌다** | v5 동일 형식 | ⚠ **우리 anti-sandwich 인용의 정본은 여전히 [Haru14] 다** |
| **진공 두께** | **10–15 Å** | **30 Å** (UMA 분포밖 회피 — 60 Å 에서 24.5 J/m²) | 🔴 **우리 30 Å 은 문헌 2–3배이고 근거가 물리가 아니라 MLIP 병리다.** 원고에 "문헌 프로토콜 계승" 으로 쓰면 안 된다 |
| **이완 자유도** | ⛔ **미기재** (*"local structure optimization"*) | **FixAtoms 33 %** | 🔴 **대조 불가.** [Haru14] 는 "전원자 자유" 를 명시했으므로 **우리 구속은 문헌 대비 추가 제약**이고 방향 시험을 한 적이 없다 |
| **수렴 기준** | ⛔ **힘·응력·에너지 전부 0건** | fmax 0.01 eV/Å | ⚠ **문헌이 후퇴했다**(2014 는 0.001 Ry/bohr + 0.5 kbar) |
| **⭐ 셀 수치 공개** | ✅ **8계면 전부 nat·성분별 원자수·반복수·μ**. *우리 산수* misfit 역검산으로 **LCO(110)/LPS = 480+256 = 736 원자, LCO 8층 11.34 Å, LPS 2셀 16.32 Å, 면적 ≈320–345 Å², 법선 ≈38–45 Å** 복원(μ 4.51 % ↔ 논문 4.6 ✓) | v5: **820 원자(SE 624 + NCM 196), 면적 351 Å², cell_z = atoms_max + 30 Å** | 🎉 **면적이 거의 같다(344 vs 351 Å²).** 그리고 **우리 `haruyama2014` digest 의 그림 기반 추정(≈736 원자)이 원자 단위로 맞았다** — 추정 방법론이 검증됐다 |
| **무질서** | ⛔ **β-Li₃PS₄ Li 배열 0줄**, 게다가 **격자가 [Haru14] 와 1–2 % 다르다**; LLZO 공공 50/40 % 는 **정수 해 없음** | 우리는 조성별 배열을 선언하고 시드를 돌린다 | ✅ **이 항목만은 우리가 낫다** |
| **중갭 상태의 출처** | 🔴 **본문은 "계면" 이라 하지만 그림은 "진공면" 기여가 우세** (`Fig. 3` LCO vac 90 vs LCO 1st 35; `Fig. 7` 100 vs 40 — 실독) | 우리 계면 PDOS **0건** | 🔴 **우리 v5 도 자유표면이 2개다.** 계면 PDOS 를 내는 날 **층별 투영으로 계면 vs 자유표면을 반드시 갈라야** 한다 |

**⛔ 이 축에서 인용하면 안 되는 것**
- *"Okuno 2020 이 황화물 계면 파괴에너지를 0.8 J/m² 로 계산했다"* — **없다** (④).
- *"Okuno 2020 의 LCO(110)\|LPS 부착에너지는 ○ 다"* — **보고 안 됨.**
- *"Okuno 2020 이 Li 이동 배리어/확산을 계산했다"* — **NEB·MD 0회.**
- *"LNO 버퍼가 LTO 보다 우수하다 [Okuno 2020]"* — **자기 숫자와 반대** (digest §3f-2, §10-⑩).
- E_f·E_ex·W_ad **절대값 이식** — β-Li₃PS₄ + LiCoO₂ 전용.
- ⛔ **`wang2022_…` 의 접합일(음극측)과 같은 표 금지** — 그쪽은 Li 금속\|이원화합물, 이쪽은 양극\|SE.

---

## ⑥ `comparison_vs_ours.md` **§H. 우리가 아직 못 하는 것 (정직 목록)** 에 추가할 행 (3행)

| 못 하는 것 | 문헌은 어떻게 하나 | 우리에게 필요한 것 |
|---|---|---|
| **계면 자리별 Li 공공 형성에너지 분포** | [Okuno20] 이 8계면 **271자리**를 QE DFT+U 로. 스칼라 요약은 *"E_f < 2.0 eV 비율"* | **QE 계면 셀**(저쪽 384–1056 원자) + 자리 선택 규칙 + **집계 규칙**(분포/문턱) 을 보고량 카드에 선언. ⚠ **UMA 로는 못 한다**(0.1 eV 급 차이) |
| **계면 양이온 교환에너지** | [Okuno20] 의 `E_ex` (조성 보존 스왑). Co↔P −0.76~−2 eV(황화물) vs LPO/LLZO 전부 흡열 | 같은 QE 셀에서 **Ni↔P · Ni↔Li · Cl↔O · Cl↔S**. 화학퍼텐셜 불필요라 grand-potential 확장보다 싸다 |
| **계면 PDOS / 밴드 오프셋** | [Okuno20] 이 계면 3종 + 버퍼 2종. LPO ≈1 eV, LLZO ≈0.2 eV | LiNiO₂\|LPSCl 계면 PDOS **0건**. ⚠ 낼 때 **자유표면 층을 따로 투영**해야 한다(§⑤ 마지막 행) |

---

## ⑦ 병합자 체크리스트

- [ ] ① INDEX 행을 `## ✅ Digest 완료 (paper-level)` 에 삽입 (barai 행 바로 위 권장)
- [ ] ② Reference key 에 `[Okuno20]` 행 추가
- [ ] ③ **물성 4축에는 넣지 않는다** (값이 없다)
- [ ] ④-2 INDEX 의 barai 행 `0.8 J/m²` 정정 + Nd 인산염 √ 비교의 분모 단서
- [ ] ④-3 `papers/barai2021_…md` 의 `0.8` 6곳 + line 659 "확보 후보" 행 갱신
- [ ] ④-4 `db/literature/refs.json` — (가)(나) 주석 정정 + (다) Okuno 신규 항목
- [ ] ⑤ `comparison_vs_ours.md` §J 에 방법 원전 블록 삽입 (번호는 병합자가 배정)
- [ ] ⑥ §H 에 3행 추가
- [ ] 이 `_pending_*` 파일 삭제
- [ ] `python3 tools/litdb/build_index.py --check` 로 미등록 digest 0 확인

> ⛔ **하지 않은 것**: `INDEX.md` · `comparison_vs_ours.md` · `db/literature/refs.json` **수정 없음** · **커밋 없음** · `litdb/figures/` **재생성 없음**(기존 크롭 그대로 사용, `--clean`/`--force_clean` 미사용).

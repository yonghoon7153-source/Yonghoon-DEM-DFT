<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md
     2026-09-22 초판 — 본문(12 pp) + SI(22 pp) 전문, 크롭 51장(그림 38 + 표 13) 중 **그림 9장 실독**.
     ⭐ 이 digest 의 1번 임무는 **`W_ad = 0.8 J/m²` 출처 검증**이다.
        결론: **이 논문에 0.8 J/m² 는 없다.** 이 논문의 유일한 황화물 계면 부착에너지는
        LCO(104)/LPS(010) = **0.025 eV/Å² = 0.400 J/m²** 이고, 정확히 **0.8 의 절반**이다.
        LCO(110)/LPS(010) 의 W_ad 는 **아예 보고되지 않는다** (§3g, §11-①).
     ⭐ 2번 임무는 **셀 수치의 원전 확인**. Haruyama 2014 에 없던 **총 원자수·슬랩 층수**가
        **이 논문 SI 에는 있다** — 그리고 **LCO(110)/LPS(010) = 736 원자**로,
        우리가 `haruyama2014` digest §3c-4 에서 그림으로 추정한 **≈736 과 원자 단위로 일치**한다 (§3b-4).
     ⚠ NEB·MD·AIMD **0회**. "Li migration" 이라는 말조차 이 논문엔 없다 (§3j).
     🔴 그림 실독으로 잡은 것 4건: `Fig. 2` **패널 라벨이 캡션과 뒤바뀜** · `Fig. 3` **영점 규약이
        자기 캡션과 불일치** · `Fig. 3`/`Fig. 7` **중갭 상태가 계면이 아니라 *진공면* 기여 우세** ·
        본문 §3.1/§3.2 의 **표본 개수가 그림 캡션과 정반대** (§10). -->

# Comparative Study on Sulfide and Oxide Electrolyte Interfaces with Cathodes in All-Solid-State Battery via First-Principles Calculations — Okuno, Haruyama, Tateyama (*ACS Appl. Energy Mater.* **3**, 11061–11072 (2020))

> slug `okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces` · DOI `10.1021/acsaem.0c02033` (ACS AuthorChoice, open access) · type `계산 100 % (정적 DFT+U 슬랩 계면 — MD·AIMD·NEB 0회 · 실험 0회)` · PDF `inbox/5. ACSAEM_2020_Okuno_Haruyama_Tateyama_Sulfide_vs_oxide_interfaces_cathodes_MAIN.pdf` (본문 12 pp, `Fig. 1`–`16`, 본문 표 **0개**) + **SI** `inbox/5. Sup) ACSAEM_2020_Okuno_Sulfide_vs_oxide_SI.pdf` (22 pp, §S1–S7 · `Fig. S1`–`S23` · `Table S1`–`S13`) · digested `2026-09-22` · status ✅ · 태그 **[외부]**

> elements: Li, Co, O, P, S, La, Zr, Ti
> methods: DFT, DOS, PDOS

> **저자**: **Yukihiro Okuno\***(**FUJIFILM** Corporation R&D 본부 — 산업계 1저자) · **Jun Haruyama**(**東大 ISSP** — 2014·2017 편의 1저자, NIMS 에서 이적) · **Yoshitaka Tateyama\***(NIMS GREEN+MANA + 京都大 ESICB) · 접수 2020-08-22 / 수락 2020-10-13 / 게재 2020-10-28 · MEXT **Fugaku 배터리·연료전지 프로젝트** JPMXP1020200301 · 元素戦略 JPMXP0112101003 · Materealize JPMXP0219207397 · JSPS KAKENHI JP19H05815 · 계산 = **RIKEN AICS K computer** (HPCI hp160081 / hp170292 / hp190039)
>
> **계보 (같은 그룹 3부작의 3편)**: **[Haru14]** `papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md` (계면 4종을 처음 만듦, LNO 버퍼) → **[Haru17]** `papers/haruyama2017_cation_mixing_co_diffusion_lco_lps.md` (같은 계면에 Co 양이온 혼합) → **본 편 [Okuno20]** (**황화물 vs 산화물 SE 를 같은 자로 잰다** + **면방위 의존성** + LTO 버퍼). 본 편은 **[Haru14]·[Haru17] 의 계면 모형을 물려받아 확장**하고, 같은 연도의 **[Gao20]**(Gao·Jalem·Ma·Tateyama, *Chem. Mater.* **32**, 85 (2020) — 계면 구조예측 자동화)을 *"더 포괄적인 탐색기법"* 으로 인용하면서 **자기는 그 간단판(simpler version)만 썼다**고 밝힌다.
>
> ⭐⭐ **우리 repo 안에서의 지위 — 이 편은 우리가 *간접적으로* 인용해 온 값의 지목된 출처다.**
> `litdb/papers/barai2021_delamination_cathode_llzo_multiscale.md` 의 `Fig. 11` 상도에서 **황화물 계면 안정한계선 Ψ_t ≈ 0.8 J/m²** 가 Barai 의 **ref 69(=[Haru14]) + ref 70(=본 편)** 에 귀속돼 있고, 우리 `INDEX.md` 의 barai 행이 그 0.8 을 그대로 나른다. **이 digest 의 1번 임무가 그 귀속의 검증**이고, 결론은 §3g·§11-① 이다.
> ⚠ `db/literature/refs.json` 에는 **Okuno 항목이 없다**(전수 grep 결과 0건). 즉 0.8 은 **원장이 아니라 digest·INDEX 산문에만** 살아 있다.

> **본 digest 에서 실제로 본 그림 (2026-09-22)** — 크롭 **51장**(본문 그림 16 + SI 그림 23 + 표 13) 중 **그림 9장 실독**.
> **본문 8/16**: `Fig. 2`(계면 구조) · `Fig. 3`(LPS PDOS) · `Fig. 4`(LPS E_f 분포) · `Fig. 5`(양이온 교환) · `Fig. 7`(LPO PDOS) · `Fig. 8`(LPO E_f 분포) · `Fig. 11`(LLZO PDOS) · `Fig. 12`(LLZO E_f 분포) · `Fig. 16`(LTO/LPS E_f 분포) ← 9장(본문 9)
> **SI 1/23**: `Fig. S1`(**LCO/LPS 슬랩 모형 — 기하 원전**).
> **안 본 것 (본문 그림 7 + SI 그림 22 + 표 13)**: `Fig. 1`(표면 6종 — 면지수·종단이 본문 활자) · `Fig. 6`·`Fig. 9`·`Fig. 10`·`Fig. 13`·`Fig. 14`·`Fig. 15` · `Fig. S2`–`S23` · **표 전량**(표는 PDF 텍스트가 정확 — §3 에 전수 전사했다).
> **그림 ↔ 본문 불일치 4건 (전부 실독으로만 잡힌다 — §10)**: ① **`Fig. 2` 의 (a)/(b) 라벨이 캡션과 뒤바뀌어 있다** ② **`Fig. 3` 의 영점이 자기 캡션("밴드갭 중심")과 안 맞는다** ③ **`Fig. 3`·`Fig. 7` 의 중갭 상태는 *진공을 마주한* LCO 층 기여가 우세한데 본문은 *계면* 탓으로 돌린다** ④ **본문 §3.1·§3.2 의 표본 개수가 `Fig. 4`·`Fig. 8` 캡션과 정반대다.**
> **우리가 직접 한 산수**는 `*우리 산수*` 로 표시했다 (논문 주장 아님). 그림에서만 읽은 값은 **`figure-read ≈`**.

---

## 0. 이 digest 를 읽는 법 — 왜 지금 이 논문을 구했나

**여섯 가지 임무를 안고 왔다.** 답을 먼저 적는다.

| # | 임무 | 답 | 근거 절 |
|---|---|---|---|
| ① | 🔴 **`W_ad = 0.8 J/m²` 가 정말 이 논문 값인가** | **아니다.** 이 논문에 0.8 은 **어떤 단위로도 없다**. 황화물 계면 W_ad 는 **LCO(104)/LPS(010) 0.025 eV/Å² = 0.400 J/m²** 하나뿐이고, 0.8 의 **정확히 절반**이다. **LCO(110)/LPS(010) 의 W_ad 는 보고되지 않는다.** [Haru14] 쪽 값(4.3 eV/nm² = **0.689 J/m²**)도 0.8 이 아니다 ⇒ **0.8 은 Barai 2021 이 만든 수**이고 인용된 두 원전 어디에도 없다 | §3g · §11-① |
| ② | **방법 통제축 전수** | functional·U·pseudo·cutoff·k·스미어링·스핀은 **전부 명시**. **이완 자유도·힘/에너지 수렴기준·응력기준·쌍극자 보정·QE 버전은 한 줄도 없다**. **총 원자수·슬랩 두께는 SI 에 있다**(8계면 전부) — **이것이 [Haru14] 대비 최대의 개선** | §4 · §7a |
| ③ | **[Haru14]/[Haru17] 과의 계보** | 프로토콜은 물려받되 **셋이 바뀌었다**: **U(Co) 5.9 → 4.9 eV** · 횡방향 탐색이 **계통적 격자 → 무작위(random) 이동** · **k-격자가 계면마다 다르다**(Γ vs 2×1×1). **원시 총에너지는 여전히 비공개** ([Haru17] 만 공개했다) | §3b-5 · §7c |
| ④ | **sulfide vs oxide 비교 설계** | 양극 **LiCoO₂ 하나**(104·110 두 면) × SE **LPS·LPO·LLZO** + 버퍼 **LTO** = **계면 8종**. 보고량은 **자리별 Li 공공 형성에너지의 *분포*** 와 **양이온 교환에너지**. 우리 축(아지로다이트\|NCM)으로 **전달되는 것은 *기전과 프로토콜*, 전달 안 되는 것은 *값 전부*** | §3c–3f · §7b |
| ⑤ | **NEB·MD 가 있는가** | **0회.** NEB·nudged·barrier·MD·AIMD 가 본문·SI 전문에 **한 단어도 없다**. [Haru14] 에 있던 "끝점 전달에너지" 조차 없다 | §3j |
| ⑥ | **불리한 결론** | **여섯 개**를 따로 뽑았다 — 우리 0.8 각주가 틀린 것 · 우리 W_ad 비율 해석이 무의미해진 것 · 우리 v5 의 진공면이 중갭 상태를 만들 수 있다는 것 등 | §11 |

> **⚠ 물질계 근접도.** SE 가 **β-Li₃PS₄**(Pnma, PS₄³⁻ 골격)이고 양극이 **LiCoO₂**다. 우리는 **Li₆PS₅Cl(아지로다이트) \| LiNiO₂/NCM** 이다. 골격(PS₄³⁻)은 공유하지만 **free S²⁻ 도 Cl⁻ 도 없고, 전이금속도 Co vs Ni 로 다르다**. ⇒ **수치는 한 줄도 우리 원장에 이식하지 않는다.** 가져오는 것은 **기하 프로토콜 · 보고량 설계 · 기전 서사**뿐이다.

---

## 1. 한 줄 요약

**"황화물 계면이 나쁜 이유는 계면에 Li 이 *쉽게 빠지는 자리*가 많기 때문이고, 산화물 SE 는 그 자리를 덜 만든다."** 저자들은 [Haru14] 가 만든 보고량 — **자리별 Li 공공 형성에너지 `E_f(V_Li_j)`**, Li 금속 기준이라 **eV 값이 곧 Li/Li⁺ 전압(V)** — 을 **단일 값이 아니라 *분포*로** 바꿔 놓고, 계면 8종에서 **총 271개 Li 자리**를 계산해 히스토그램으로 비교한다. 결론은 **"2.0 eV 미만 자리의 비율"** 하나로 요약된다.

> 🔧 ***우리 산수* — 논문이 끝내 표로 만들지 않은 그 사다리** (`Fig. 4`·`Fig. 8`·`Fig. 12`·`Fig. 16` 막대 실독 + 캡션의 표본수로 역산)
>
> | 계면 | 표본 구조 | Li 자리 | **E_f < 2.0 eV 자리 비율** | 그중 SE 쪽 |
> |---|---|---|---|---|
> | **LCO(110)/LPS(010)** | 3 | 23 | **≈30.4 %** (7/23) | 7/7 전부 SE |
> | **LCO(104)/LPS(010)** | 8 | 65 | **≈18.5 %** (12/65) | 11/12 |
> | **LCO(104)/LLZO(001)** | 4 | 36 | **≈6.2 %** (2/32~36) | 2/2 |
> | **LCO(104)/LPO(001)** | 5 | 36 | **≈2.8 %** (1/36) | 1/1 |
> | **LCO(104)/LPO(010)** | 4 | 28 | **0 %** (2.5 eV 미만도 0) | — |
> | **LTO(111)/LPS(010)** (버퍼) | 4 | 31 | **0 %** | — |
> | **LCO(104)/LTO(111)** (버퍼) | 3 | 24 | **0 %** (2.5 eV 미만도 0) | — |
>
> ⇒ **황화물 18–30 % ≫ 산화물 0–6 %**, 그리고 **버퍼를 끼우면 황화물도 0 %** 가 된다. 이것이 논문 전체다.

**기전은 전자 쪽이다.** Li⁺ 하나가 SE 쪽에서 빠지려면 **전자도 같이 빠져야** 하는데, 중성 셀에서는 그 전자가 **밴드정렬이 허락하는 가장 낮은 곳**으로 간다. LCO 의 가전자대가 SE 보다 아래에 있으면 전자는 **SE → LCO 로 넘어가고**, 그만큼 `E_f` 가 내려간다. 따라서 **가전자대 오프셋(VBO)이 크면 Li 고갈이 억제**된다. 저자들이 준 숫자: **LPO 는 LCO VBM 보다 ~1 eV 아래**(본문), **LLZO 는 겨우 ~0.2 eV 아래**(본문), **LPS 는 `figure-read ≈ 0.3–0.5 eV` 아래**(논문 미보고, `Fig. 3` 실독). 그래서 LPO ≫ LLZO 순서가 나온다.

**두 번째 보고량은 양이온 교환이다.** `E_ex = E_tot(A_j ↔ B_k) − E_tot`. **LCO(104)/LPS 에서 Co↔P(1층) 는 `figure-read` −0.76 / −1.25 / −1.00 eV 로 발열**이고, 2층은 거의 흡열이다. [Haru17] 의 **LCO(110)/LPS 값(≈−2 eV)** 과 비교하면 **면방위 하나로 발열량이 절반 이하**가 된다. 산화물은 전부 흡열이다 — **LPO 는 Co↔P·Co↔Li 모두 3 eV 이상 흡열**, **LLZO 는 Co↔Zr 0.7–1 · Co↔La 1–3 · Co↔Li 2–3 eV 흡열**. ⇒ **반응층(reaction layer) 형성 경향도 황화물 ≫ LLZO > LPO.**

**그리고 양이온 혼합은 Li 고갈을 *가속*한다.** `Table S4`: Co↔P 혼합 6개를 넣으면 같은 자리의 `E_f` 가 **2.40→1.39 · 2.18→1.69 · 2.40→2.11 · 2.27→1.12 · 2.14→1.48 eV** 로 **전부 내려간다**(*우리 산수*: 평균 **2.28 → 1.56 eV, −0.72 eV**). 기전은 `Fig. S6` — **혼합이 Fermi 준위 근처에 Co d 중갭 상태를 늘려** 전자 이동 비용을 낮춘다. ⇒ **[Haru17] 의 양이온 혼합과 [Haru14] 의 Li 고갈이 하나의 고리로 닫힌다.**

**부착에너지는 곁다리다.** 네 개만 보고되고(0.025 / 0.028 / 0.021 / 0.019 eV/Å²), 본문에서 **한 번도 비교·해석되지 않으며**, *"정의는 SI 에 있다"* 한 줄로 끝난다. ⚠ 그런데 **우리 repo 는 바로 그 곁다리 수를 (Barai 를 거쳐) 인용해 왔다** — §11-①.

⚠ 이 서사의 취약점은 **열 겹**이다(§10): ① **0.8 J/m² 귀속 오류의 원인 제공**(W_ad 를 4개만, 그것도 (110)/LPS 를 빼고 준다) ② **`Fig. 2` 패널 라벨이 캡션과 뒤바뀜** ③ **표본 개수가 본문 ↔ 그림 캡션에서 두 번 정반대** ④ **면방위 비교가 서로 다른 k-격자에서 이뤄짐**(Γ vs 2×1×1) ⑤ **결론이 걸린 (110)/LPS 표본이 23자리 3구조로 가장 적다** ⑥ **구조 표본 산포가 W_ad 보다 크다** — LCO(104)/LPO(001) 은 **4.95배** ⑦ **중갭 상태가 진공면 기여로 보인다** ⑧ **β-Li₃PS₄ 무질서 처리를 한 줄도 안 밝힌다**(그리고 [Haru14] 와 격자상수가 다르다) ⑨ **수렴기준·이완 자유도가 전무** ⑩ **[Haru14] 와 U 가 1.0 eV 다른데 두 논문의 `E_f` 를 직접 비교해 "LNO > LTO" 를 결론**한다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| **저자** | Yukihiro Okuno\* (**FUJIFILM**), Jun Haruyama (**東大 ISSP**), Yoshitaka Tateyama\* (**NIMS**) |
| **저널/년** | *ACS Applied Energy Materials* **3**, 11061–11072 (**2020**) · ACS AuthorChoice (open access) |
| **DOI** | `10.1021/acsaem.0c02033` |
| **양극** | **LiCoO₂ (LCO)** — **(104)** 와 **(110)** 두 면 |
| **SE** | 황화물 **β-Li₃PS₄ (LPS, 010)** · 산화물 **γ-Li₃PO₄ (LPO, 001·010)** · 산화물 **Li₇La₃Zr₂O₁₂ (LLZO, 001)** |
| **버퍼** | **Li₄Ti₅O₁₂ (LTO, 111)** |
| **계면 8종** | LCO(104)/LPS(010) · LCO(110)/LPS(010) · LCO(104)/LPO(001) · LCO(104)/LPO(010) · LCO(110)/LPO(010) · LCO(104)/LLZO(001) · LTO(111)/LPS(010) · LCO(104)/LTO(111) |
| **연구유형** | **계산 100 %** — 정적 DFT+U 슬랩 계면. 실험 0회 · AIMD 0회 · **NEB 0회** · MLIP 0회 |
| **보고량** | ① **자리별 Li 공공 형성에너지 분포** `E_f(V_Li_j)` (271자리) ② **양이온 상호교환에너지** `E_ex` ③ **PDOS / 밴드 오프셋** ④ (곁다리) **부착에너지 W_ad** 4개 |
| **후처리** | PDOS + 결함 형성에너지 + 교환에너지 + W_ad. (**COHP·Bader·ELF·NEB·grand-potential·포논·탄성 전부 0회**) |
| **참고문헌** | 62 (본문) + 8 (SI) |
| **그림/표** | 본문 `Fig. 1`–`16` (**본문 표 0개**) · SI `Fig. S1`–`S23`, `Table S1`–`S13` |

---

## 3. 결과 — 절별 전수

### 3a. 벌크 검증 (`Table S1` — 전사)

| 결정 | a (Å) 계산 (실험) | b (Å) 계산 (실험) | c (Å) 계산 (실험) | **E_v (eV)** |
|---|---|---|---|---|
| **β-Li₃PS₄** (사방정, ref S1 Mercier 1982) | **13.02** (13.07) | **8.161** (8.015) | **6.234** (6.101) | **2.9–3.2** |
| **LiCoO₂** (육방정, ref S2) | **2.835** (2.815) | — | **14.04** (14.05) | **4.0** |
| **Li₄Ti₅O₁₂** (입방, ref S3) | **8.419** (8.357) | — | — | **5.0–5.1** |
| **γ-Li₃PO₄** (사방정, ref S4) | **10.53** (10.49) | **6.14** (6.12) | **4.95** (4.93) | **5.1–5.2** |
| **Li₇La₃Zr₂O₁₂** (입방, ref S5) | **13.03** (12.97) | — | — | **3.5–3.6** |

*우리 산수* — 격자 오차: LPS **a −0.38 / b +1.82 / c +2.18 %** · LCO **a +0.71 / c −0.07 %** · LTO **+0.74 %** · LPO **+0.38 / +0.33 / +0.41 %** · LLZO **+0.46 %**.

> 🔴 ***우리 산수* — 같은 그룹, 같은 물질, 같은 방법인데 β-Li₃PS₄ 벌크가 [Haru14] 와 다르다.**
> [Haru14] `Table S1`: **13.13 / 8.062 / 6.178** · 본 편: **13.02 / 8.161 / 6.234**. 차이 **−0.84 / +1.23 / +0.91 %**.
> QE·PBE·USPP·40/320 Ry 가 전부 같은데 격자가 1 % 움직였다는 것은 **Li 배열(무질서 처리)이 달라졌다**는 뜻이다. [Haru14] 는 *"Lepley 의 β-Li₃PS₄-b (4c 자리 Li 제거)"* 를 **명시**했는데, **본 편은 그 문장을 통째로 뺐다** — SI 는 `Table S1` 각주로 Mercier 1982(실험 구조)만 달고 32원자 셀이라고만 한다. ⇒ **무질서 처리 미선언**(§10-⑧).

> ⚠ **밴드갭이 한 개도 없다.** [Haru14] `Table S1` 에는 계산 갭(LCO 2.2 / LNO 3.6 / LPS 2.8 eV)이 있었는데 본 편 `Table S1` 은 **E_v 만** 준다. 갭을 알 수 있는 것은 **PDOS 그림에서 눈으로 재는 것뿐**이다 ⇒ **우리 band gap 축(§7b)과 숫자 비교 불가.**

---

### 3b. ⭐⭐ 계면 구성 — **기하 전수** (본문 §2.1 + SI §S3–S7, `Fig. S1` ✅ 실독)

#### 3b-1. 면 선택의 근거 (본문 §2.1 원문)

| 물질 | 채택 면 | 채택 이유 (원문) | 저자가 스스로 인정한 반례 |
|---|---|---|---|
| **LCO** | **(104)** 와 **(110)** | *"energetically probable"* · (110) 은 *"still exists in the LCO particles and is one of the theoretically well-studied LCO surfaces"* (refs 38–40) | ⚠ *"Although the larger stability of the **(104)**-oriented LCO surface was suggested (ref 37 = **Kramer & Ceder 2009**)"* — [Haru14] 가 무시했던 그 반례를 **이번엔 면으로 추가해 정면으로 다룬다** ✅ |
| **LPS** | **(010)** | *"the Li⁺ conduction path in LPS is in the b direction"* (ref 42 Maruyama) | — |
| **LPO** | **(010)** 과 **(001)** | *"b and c directions are Li⁺ conduction paths in LPO"* (refs 46, 47) | — |
| **LLZO** | **(001)** 입방상 | ZrO₆ 팔면체를 보존하는 면 | ⚠ *"On the outermost surface of the LLZO slab, **few LaO₈ dodecahedrons were broken**"* — **화학양론 때문에 깨질 수밖에 없다**(§3e) |
| **LTO** | **(111)** | *"the Li ions can migrate through"* (ref 52 Ziebarth) · **Li 종단**이 벌크 적층과 같아 안정 | — |

**종단 규약 (공통)**: *"we chose the surface termination **so as not to break the polyhedrons** constructed by the transitional metal and anion atoms as much as possible **within the stoichiometric surface slab**. These slabs were **approximately dipole-free** as well."*
- **LPO**: *"to keep the structure of the PO₄ tetrahedron at the interface, the **outermost interface layer is composed of Li ions**."*
- **LTO**: *"To maintain the TiO₆ octahedron structures, the **outermost surfaces were composed of Li ions (8a sites)** on the TiO layers."*
- **LCO·LPS 의 종단은 활자로 없다** — [Haru14] 와 같은 공백.

#### 3b-2. 구축 절차 (본문 §2.1 원문)

| 단계 | 내용 |
|---|---|
| **Step 1** | 벌크를 DFT+U 로 최적화 (`Table S1`) |
| **Step 2** | 화학양론·다면체 보존 면을 잘라 슬랩. **두께 "around 1–2 nm"** |
| **Step 3** | *"the surface slab of **LCO or LTO was set first**, and the second material (SE) slab was put on it"* — **양극/버퍼가 기준, SE 가 얹히는 쪽** |
| **Step 4** | ⭐ **횡방향 강체 이동 + 국소 이완**. *"we explored several **rigid lateral shifts** of the second slab followed by **local structure optimization**"* · *"We constructed several interface structures by **randomly moving** one side of the slab model in lateral directions"* ⇒ **[Haru14] 의 계통적 16/4/9 격자 탐색이 *무작위* 로 바뀌었다** |
| **Step 5** | ⭐ **통계를 낸다.** *"calculated **statistics** of physical quantities such as Li vacancy-formation energies and cation exchange energies. Calculating the statistics of the physical properties is important to obtain reliable results."* — **이것이 [Haru14] 대비 가장 큰 방법론 진보**다 (최저구조 1개 → 분포) |
| **Step 6** | **표본 배제 규칙**: *"the structure with the energy difference of **1 order of magnitude higher** than the others was excluded"* |
| **진공** | *"There was vacuum in the region surrounding the slabs (**up to 1.5 nm**)"* · *"we also introduced a vacuum region with **about 1–1.5 nm** width in the outside of the interface slab"* |

> ⭐ **anti-sandwich 논거 — [Haru14] 보다 *약해졌다* (원문 그대로)**
> *"Note that a supercell without a vacuum usually involves two interfaces, which are **atomically different in most cases**."*
> ⇒ [Haru14] 의 두 번째 논거 — *"artificial interaction between the two interfacial polarizations may arise … the presence of the vacuum region is **quite crucial**"* — 가 **통째로 빠졌다.** 우리가 v10b 샌드위치를 철회할 때 쓴 문장은 **[Haru14] 것이지 이 편 것이 아니다.**

#### 3b-3. 격자 정합 규약 (원문)

- **LCO/LPS**: *"Considering the rather **low elastic modulus of LPS**, the LPS lattice constants are **adjusted to that of LCO**"* (본문) = *"Considering the **high elastic modulus of LCO**, the lattice constants of LPS is set to that of the LCO"* (SI). **같은 규약, [Haru14] 와 동일.**
- **LCO/산화물(LPO·LTO·LLZO)**: *"the **average of the two lattices** is considered"* (본문 §2.1).
- ⚠ **그런데 SI §S7 은 반대로 말한다**: *"The **lattice constants of LTO are set to that of LCO**"* (LCO(104)/LTO(111)). 본문의 "평균" 규약과 **충돌**.
- ⚠ **SI §S6 은 계에 없는 물질을 든다**: LTO(111)/LPS(010) 절에 *"The lattice constant of **LPS is set to that of LCO**"* — 이 계면에 **LCO 는 없다**. 복붙 오류(§10-⑨).

#### 3b-4. ⭐⭐⭐ **총 원자수 · 슬랩 두께 · 계면 면적** — **[Haru14] 에 없던 것이 여기 있다**

**논문이 준 것 (SI §S3–S7 + `Table S2/S5/S8/S10/S12`, 전사):**

| 계면 | **총 nat** | 양극/버퍼 쪽 | SE 쪽 | **반복수 (양극 : SE)** | **μ (%)** |
|---|---|---|---|---|---|
| **LCO(104)/LPS(010)** | **696** | 504 (본문 "506" — 오타) | 192 | 7×2×2 : 1×2×3 | **8.9** |
| **LCO(110)/LPS(010)** | **736** (본문 "756" — 오타) | 480 | 256 | 5×1×4 : 1×2×4 | **4.6** |
| **LCO(104)/LPO(001)** | **888** | 504 | 384 | 7×2×2 : 2×2×3 | **7.0** |
| **LCO(104)/LPO(010)** | **760** | 504 | 256 | 7×2×2 : 1×2×4 | **3.9** |
| **LCO(110)/LPO(010)** | **384** | 192 | 192 | 2×1×4 : 1×2×3 | **6.2** |
| **LCO(104)/LLZO(001)** | **448** | 256 | 192 | 4×2×2 : 1×1×1 | **13.0** |
| **LTO(111)/LPS(010)** | **1056** | 672 | 384 | 1×4×1 : 3×2×2 | **4.9** |
| **LCO(104)/LTO(111)** | **424** | 256 | 168 | 4×2×2 : 1×1×1 | **7.5** |

**단위 셀 (SI 활자)**: LCO(104) `2.815 × 5.700 × 8.012` · LCO(110) `2.815 × 14.04 × 2.835` · LPS(010) `13.02 × 8.161 × 6.234` (32원자) · LPO(001)=LPO(010) `10.529 × 6.137 × 4.948` (32원자) · LLZO(001) `13.03³` (192원자) · LTO(111) `11.907 × 10.311 × 14.58` (168원자).

> 🔧 ***우리 산수* — 이 표에서 *진짜 셀*을 복원했다. 두 군데가 오식이고, 복원하면 misfit 이 소수점까지 맞는다.**
>
> **(가) 밀도 검산** — 각 "단위"의 원자밀도를 벌크와 대조:
> LPS 32/662.4 Å³ = **0.0483** ✓ · LPO 32/319.8 = **0.100** ✓ · LLZO 192/2212 = **0.0868** ✓ · LTO 168/1790 = **0.0939** ✓(벌크 56/596.8 = 0.0938) — **네 개 다 정확하다.**
> **LCO(110)** `2.815 × 14.04 × 2.835` @24원자 → 0.2142 at/Å³ = **벌크(0.1228)의 1.74배 = 불가능**. 첫 수를 **√3 × 2.835 = 4.910** 으로 고치면 195.4 Å³ @24원자 = **0.1228 ✓ 정확히 벌크**. ⇒ **SI 의 `2.815` 는 `4.910` 의 오식**(LCO(104) 줄에서 복붙된 것으로 보인다).
>
> **(나) misfit 역검산** — `μ = 1 − 2S_A∩B/(S_A+S_B)`, S_A∩B = 두 직사각형의 겹침으로 풀면:
> · **LCO(104)/LPS**: LCO 면내 (7×2.815) × (2×5.700) = **19.705 × 11.40 = 224.6 Å²**; LPS 면내 13.02 × (3×6.234) = **13.02 × 18.70 = 243.5 Å²**; 겹침 = 18.70 × 11.40 = 213.2 → **μ = 8.90 %** ✓✓ **논문값 8.9 와 완전 일치**
> · **LCO(110)/LPS** (4.910 보정): LCO (5×4.910) × 14.04 = **24.55 × 14.04 = 344.7**; LPS 13.02 × (4×6.234) = **13.02 × 24.94 = 324.7**; 겹침 = 24.55 × 13.02 = 319.6 → **μ = 4.51 %** ✓ **논문값 4.6 과 일치** (보정 전 `2.815` 로 하면 **30 %** 가 나와 완전히 빗나간다 ⇒ 오식 확정)
>
> **(다) 복원된 계면 기하 — 이것이 우리가 원했던 표다**
>
> | 계면 | **계면 면적 (Å²)** | **양극 두께** | **SE 두께** | **법선 셀 길이 (진공 포함)** |
> |---|---|---|---|---|
> | **LCO(104)/LPS(010)** | ≈ **213–225** | **9 층 × d₁₀₄ 2.003 Å = 18.0 Å** (504원자 = 14 표면셀 × 9층 × 4원자 ✓) | **2 × b = 16.32 Å** | ≈ **45–50 Å** |
> | **LCO(110)/LPS(010)** | ≈ **320–345** | **8 층 × d₁₁₀ 1.4175 Å = 11.34 Å** (480원자 = 20 표면셀 × 8층 × 3원자 ✓) | **2 × b = 16.32 Å** | ≈ **38–45 Å** |
> | **LCO(104)/LLZO(001)** | ≈ **128** | **8 층 = 16.0 Å** (256원자) | **1 × 13.03 Å** | ≈ **40–45 Å** |
> | **LTO(111)/LPS(010)** | ≈ **487–491** | **1 × 14.58 Å** | **2 × b = 16.32 Å** | ≈ **42–47 Å** |
>
> ⇒ **법선 셀 길이는 논문에 없지만 위 재구성으로 ≈ 38–50 Å 이 나온다** (슬랩 두께 합 + 진공 10–15 Å + 간격).
>
> 🎉 **그리고 이것이 이번 digest 최대의 성과다.**
> **LCO(110)/LPS(010) = 480 원자 LCO(8층, 11.34 Å) + 256 원자 LPS(2 셀, 16.32 Å) = 736 원자**, 면내 ≈ 24.5 × 14.0 Å.
> [Haru14] 의 같은 계면 셀은 **a 13.94 / b 24.46 Å** 이었다 ⇒ **같은 셀이다** (24.55↔24.46, 14.04↔13.94 — 이완 오차 내).
> 그리고 우리 `haruyama2014` digest §3c-4 가 **그림에서 자로 재서 추정한 값**이 **"LCO 8층 = 480원자 + LPS 2셀 = 256원자 = ≈736 원자, 법선 ≈43 Å"** 이었다.
> ⇒ **원자 단위로 맞았다.** [Haru14] 가 감춘 수를 [Okuno20] SI 가 6년 뒤에 공개한 셈이고, 우리 추정은 그 검산을 통과했다.

**논문이 *여전히* 안 주는 것**: ⛔ **법선방향 셀 길이(활자)** · ⛔ **진공의 정확한 값**(1–1.5 nm 범위만) · ⛔ **초기 계면 간격** · ⛔ **좌표 파일(CIF/POSCAR)** · ⛔ **원시 총에너지**.

#### 3b-5. 구조 표본의 에너지 산포 (본문 + SI, 전사)

계면당 *"가장 안정한 구조와 가장 높은 구조의 **단위면적당** 에너지 차"*:

| 계면 | **ΔE/S (eV/Å²)** | *우리 산수* **J/m²** | *우리 산수* **같은 계면 W_ad 대비** |
|---|---|---|---|
| LCO(104)/LPS(010) | **0.0053** | 0.085 | **21 %** (W_ad 0.025) |
| LCO(110)/LPS(010) | **0.0054** | 0.087 | W_ad 미보고 |
| LCO(104)/LPO(010) | **0.023** | 0.368 | **82 %** (W_ad 0.028) |
| **LCO(104)/LPO(001)** | **0.104** | **1.666** | 🔴 **495 %** (W_ad 0.021) |
| LCO(104)/LLZO(001) | **0.038** | 0.609 | W_ad 미보고 |
| LCO(110)/LPO(010) (SI) | **0.019** | 0.304 | W_ad 미보고 |
| LTO/LPS · LCO/LTO | ⛔ 미보고 | — | — |

> 🔴 **LCO(104)/LPO(001) 은 표본 산포가 부착에너지의 5배다.** 즉 **표본 중 가장 높은 구조를 골랐다면 W_ad 가 0.021 − 0.104 = −0.083 eV/Å² (음수 = 반발)** 이 된다 (*우리 산수*). ⇒ **이 논문의 W_ad 는 "가장 안정한 한 구조" 의 값이고, 계면의 성질이 아니라 *구조 선택*의 값이다.** §10-⑥ · §11-①.

---

### 3c. LCO/LPS 계면 (황화물) — 본문 §3.1 (`Fig. 2` ✅ · `Fig. 3` ✅ · `Fig. 4` ✅ · `Fig. 5` ✅)

#### (1) 원자구조 — 면방위가 화학을 바꾼다

| 면 | 계면에서 생기는 것 (원문) |
|---|---|
| **LCO(104)/LPS(010)** | *"**almost half** of the outermost Co cations in the LCO side attract S anions to form **CoO₅S octahedrons**, and the remaining outermost Co … form **CoO₅ quadrangular cones**."* Li 은 **O 의 top 자리(on-top)** 에 앉는다 |
| **LCO(110)/LPS(010)** | *"**CoO₄ pseudotetrahedrals** appear instead of typical CoO₆ octahedrons, and **CoO₄S pentahedrons** are also partly formed"* (= [Haru14] 와 동일). Li 은 **O–O 다리(bridge) 자리** |

> **`Fig. 2` 실독 ✅ — 🔴 패널 라벨이 캡션과 뒤바뀌어 있다.**
> 그림 안 라벨은 **(a) LCO(110)/LPS(010) · (b) LCO(104)/LPS(010)** 인데, 캡션은 **"(a) LCO(104)/LPS(010) and (b) LCO(110)/LPS(010)"** 이라고 쓴다.
> 구조를 보면 **그림 안 라벨이 맞다**: (a) 는 파란 CoO₂ 띠가 **수평 3장**에 그 사이 초록 Li 열 = `Fig. S1`(b) 의 (110) 컷 ✓, (b) 는 파란 다면체가 **사선**으로 늘어선 = `Fig. S1`(a) 의 (104) 컷 ✓.
> 인셋도 내용과 맞는다 — (a) 인셋에 **노란 S 가 파란 다면체에 붙은 CoO₄S**, (b) 인셋에 **Li 이 O 위에 on-top** 으로 얹힌 모습.
> ⇒ **본문 서술은 맞고 캡션의 (a)/(b) 글자만 틀렸다.** 그림만 보고 인용하면 방위를 뒤집어 쓰게 된다.

#### (2) 전자구조 — `Fig. 3` ✅ 실독 (LCO(104)/LPS(010))

- **축**: x = Energy [eV] **−2 … +4**, y = Density of States [/eV] **0 … 1000**. 곡선 5개: **빨강 Total · 연두 LCO · 파랑 LPS · 갈색 "LCO vac"(진공 마주한 LCO 층) · 하늘색 "LCO 1st"(LPS 마주한 첫 LCO 층)**.
- **가전자대 꼭대기 `figure-read ≈ +1.5 eV`** · **총 DOS 가 0 인 창 `figure-read ≈ +1.6 … +2.4 eV`(폭 ≈0.8 eV)** · **+2.6 … +3.0 eV 에 고립 봉우리**(`figure-read` 높이 ≈150) · **+3.2 eV 부터 전도대 본체**.
- **LPS(파랑) 가전자대 꼭대기 `figure-read ≈ +1.0 … +1.45 eV`** ⇒ ***우리 산수* VBO(LCO−LPS) ≈ 0.1–0.5 eV** — **작다**. (본문은 LPS 의 오프셋 값을 **한 번도 주지 않는다**. *"LPO has a larger bandgap and a **lower valence-band maximum than that of LPS**"* 라는 정성 서술이 전부다.)
- 본문: *"the VBM and the CBM are composed of the orbitals originating from the LCO. In particular, the **CBM is observed to be an in-gap state, consisting of the Co3d orbitals of CoO₅ quadrangular cones at the interface**."*
- 🔴 **실독 반론**: **+2.85 eV 의 그 중갭 봉우리는 갈색("LCO vac", `figure-read ≈ 90`)이 하늘색("LCO 1st", `figure-read ≈ 35`)보다 2배 이상 크다.** 즉 **진공을 마주한 자유표면** 기여가 우세하다. 본문은 이것을 **계면** 상태로 돌린다 (§10-⑦).
- 🔴 **캡션 불일치**: 캡션은 *"We set zero reference energy as **the center of the band gap**"* 라는데, **0 eV 지점의 총 DOS 는 `figure-read ≈ 500`** 으로 가전자대 한복판이다. 갭은 +2.0 근처에 있다 ⇒ **`Fig. 3` 의 영점은 갭 중심이 아니다**. (같은 캡션 문구를 쓴 `Fig. 7`·`Fig. 11` 은 **맞다** — 그쪽은 0 이 정확히 갭 안이다.)
- `Fig. S2`(안 봄): Co 원자별 PDOS. SI 본문 — **CoO₅ 사각뿔 Co 가 중갭 상태를 만들고, S 를 끌어당겨 CoO₅S 가 된 Co 는 중갭 상태를 안 만든다.** ⇒ **"S 와 결합하면 오히려 갭이 깨끗해진다"** 는 반직관적 결과.

#### (3) Li 공공 형성에너지 — `Fig. 4` ✅ 실독 + `Table S3` 전사

**`Fig. 4` 실독**: x = Li vacancy formation energy [eV], **6 구간**(1.0–1.5 / 1.5–2.0 / 2.0–2.5 / 2.5–3.0 / 3.0–3.5 / >3.5), y = Normalized Li site distribution **0–0.5**. **파랑 = 전체 자리 · 빨강 = LPS 쪽 자리.**

| 구간 | **(a) LCO(104)/LPS** 파랑 (`figure-read`) | *우리 산수* 자리수 (×65) | **(b) LCO(110)/LPS** 파랑 | *우리 산수* 자리수 (×23) |
|---|---|---|---|---|
| 1.0–1.5 | 0.06 | **4** | 0.045 | **1** |
| 1.5–2.0 | 0.12 | **8** | 0.26 | **6** |
| 2.0–2.5 | **0.415** | **27** | 0.087 | **2** |
| 2.5–3.0 | 0.14 | **9** | **0.39** | **9** |
| 3.0–3.5 | 0.23 | **15** | 0.175 | **4** |
| >3.5 | 0.03 | **2** | 0.045 | **1** |
| **합** | 1.00 ✓ | **65 ✓** | 1.00 ✓ | **23 ✓** |

> ✅ **검산 통과**: 환산한 자리수가 캡션의 **65자리 / 23자리**와 **정확히** 맞는다 ⇒ 내 막대 읽기가 정확하다는 자체 증명.
> ⇒ **E_f < 2.0 eV 비율: (104) 12/65 = 18.5 % · (110) 7/23 = 30.4 %** — **(110) 이 1.6배**. 본문 주장(*"Such sites appear more frequently in the less stable LCO(110)/LPS(010) interfaces"*)을 **그림이 지지한다** ✓
> 🔴 **그러나 캡션의 표본 배정이 본문과 정반대다.** 캡션: *"65 Li sites in **8** different interface structures (**23** sites in **three**…) … for LCO(104)/LPS(010) and (LCO(110)/LPS(010))"*. 본문 §3.1: *"we sampled **three and eight** different structures for the **LCO(104)** and **LCO(110)** interfaces, respectively"* — **반대**. SI §S3: *"We had calculated **8 and 4** slab models for LCO(104) and LCO(110)"* — **또 다르다**(4 vs 3). ⇒ **세 진술이 서로 안 맞는다**(§10-③).

**`Table S3` (자리별 값, eV — 전사)** — `LC` = LCO 쪽, `LP` = LPS 쪽:

| 모형 | LC1 | LC2 | LC3 | LP4 | LP5 | LP6 | LP7 | LP8 |
|---|---|---|---|---|---|---|---|---|
| **(a) LCO(104)/LPS — 최저구조** | 3.37 | 3.41 | 2.41 | 2.43 | **2.17** | 2.40 | **2.15** | 2.27 |
| **(b) LCO(104)/LPS — 최고구조** | 3.48 | 3.18 | 2.21 | 2.20 | 2.22 | **1.23** | **1.48** | 1.61 |
| **(c) LCO(110)/LPS — 최저구조** | 2.98 | 3.30 | 2.75 | 2.51 | 2.84 | **1.97** | **1.86** | — |
| **(d) LCO(110)/LPS — 최고구조** | 3.23 | 3.73 | 3.01 | 2.95 | 2.76 | 2.30 | **1.25** | — |

**본문·SI 해석 (전수)**
- **LP4 는 계면 산소에 강하게 흡착된 Li** 이라 **형성에너지가 높다**(2.20–2.95) — [Haru14] 의 "흡착 Li 은 안정" 과 같은 결론.
- **LC3(LCO 최외곽 Li)** 는 LC1·LC2 보다 낮다 (2.21–3.01).
- **LP5·LP8**(최저구조)은 *"**mobile Li sites** in the original β-Li₃PS₄ crystal"* — **원래 이동성 자리가 먼저 빠진다.**
- ⭐ **핵심**: **(110) 은 *최저* 구조에서도 2.0 eV 미만 자리가 나온다**(LP6 1.97, LP7 1.86). **(104) 는 최저구조에서 최솟값 2.15** 로 2.0 을 안 깬다. *"Li sites with vacancy formation energy below 2.0 eV are seen **even in most stable interface model**"* (SI §S3).
- **고에너지 준안정 구조일수록 낮은 자리가 는다** — 두 방위 모두.

#### (4) 양이온 교환 — `Fig. 5` ✅ 실독 + `Fig. S4`·`Table S4`(안 봄, 본문 전사)

**`Fig. 5` 실독**: (a) 구조 + 자리 라벨(Co1·Co2·Co3 / Li1·P1 · Li2·P2), (b) Co↔P 교환에너지 [eV] **y 축 −2 … +0.5**, (c) Co↔Li **y 축 0 … 4**.

| 교환 | **P1 (1층)** `figure-read` | **P2 (2층)** `figure-read` |
|---|---|---|
| Co1↔P | **−0.76** | **+0.38** |
| Co2↔P | **−1.25** | **−0.09** |
| Co3↔P | **−1.00** | **≈0.00** |

| 교환 | **Li1** `figure-read` | **Li2** `figure-read` |
|---|---|---|
| Co1↔Li | **+2.25** | **+3.18** |
| Co2↔Li | **+2.29** | **+2.57** |
| Co3↔Li | **+2.96** | **+3.31** |

- 본문: *"the mixing reaction energies are around **−0.7 to −1.2 eV**, which are **smaller than the energy of the LCO(110)/LPS(010) case (around −2 eV)**"* (ref 22 = [Haru17]) ✓ **그림과 일치**.
- 본문: Co↔Li 은 *"about **2−3 eV endothermic** even for the first layer"* ⇒ *"the Co cations **cannot migrate** to the neighboring Li sites."* ✓ (실독 범위 2.25–3.31, **상한이 3 을 살짝 넘는다**).
- **Co1 = CoO₅S 팔면체 · Co2 = CoO₅ 사각뿔 · Co3 = CoO₆ 팔면체** (본문 명시). **가장 발열인 것은 Co2(사각뿔)↔P1 = −1.25 eV** — 즉 **배위가 덜 찬 Co 가 가장 잘 섞인다**.
- `Fig. S4`(안 봄): **고에너지 계면구조일수록 Co↔P 가 더 발열**이다 (Co1↔P1 제외).

#### (5) ⭐ 양이온 혼합 → Li 고갈 가속 (`Table S4` 전사, `Fig. S5`·`Fig. S6` 안 봄)

LCO(104)/LPS 최저구조에 **Co↔P 를 1층에서 6개 넣고** 같은 Li 자리의 `E_f` 를 다시 계산:

| 자리 | L1 | L2 | L3 | L4 | L5 | *우리 산수* 평균 |
|---|---|---|---|---|---|---|
| **혼합 전** | 2.40 | 2.18 | 2.40 | 2.27 | 2.14 | **2.278** |
| **혼합 후** | **1.39** | **1.69** | 2.11 | **1.12** | **1.48** | **1.558** |
| *우리 산수* Δ | −1.01 | −0.49 | −0.29 | **−1.15** | −0.66 | **−0.72 eV** |

기전 (본문 + `Fig. S6`): *"The Co↔P mixing **increases the in-gap states** composed of Co d-orbitals around the Fermi level, which **lowers the electron transfer energy from LPS to LCO** … consequently, E_f(V_Li_j) in the LPS side decreases. As a result, **the cation mixing introduces the Li⁺ depletion phase and becomes the origin of the high-resistance phase**."*

> ⭐ **이것이 3부작을 닫는 고리다.** [Haru17] 이 "Co 가 계면에서 P 자리로 간다"(−2.18 eV)를 보였고, 본 편이 **"그 결과 Li 고갈이 평균 0.72 eV 만큼 심해진다"** 를 수치로 잇는다.

---

### 3d. LCO/LPO 계면 (산화물 #1) — 본문 §3.2 (`Fig. 7` ✅ · `Fig. 8` ✅ · `Fig. 6`·`Fig. 9` 안 봄)

- **구조**: *"more than half of the outermost Co atoms at the LCO surface **formed CoO₆ octahedrons by sharing the O atoms in the PO₄ tetrahedrons**"* ⇒ **팔면체가 재생되어 계면이 매끄럽다.** 이온 위치 변형이 LPS 보다 **작다**. (= [Haru14] 의 LNO 버퍼 기전과 **똑같은 논리**: 산화물은 O 를 빌려줘 CoO₆ 를 복원한다.)
- **W_ad**: LCO(104)/LPO(010) **0.028** · LCO(104)/LPO(001) **0.021 eV/Å²**.
- **PDOS `Fig. 7` ✅ 실독** (LCO(104)/LPO(001)): x **−3 … +3 eV**, y **0 … 1000 /eV**. **영점이 갭 중심 ✓** — 총 DOS 가 `figure-read ≈ −0.45` 에서 0 이 되고 `≈ +0.45` 에서 다시 올라온다 ⇒ **실효 갭 `figure-read ≈ 0.9 eV`**.
  - **LPO(파랑) 가전자대**: −3 에서 ≈320 이었다가 `figure-read ≈ −2.35` 에서 0, 그리고 **−1.45 근처에 고립 봉우리(≈90)**. ⇒ **LPO 꼭대기 ≈ −1.35 vs VBM −0.45 ⇒ 오프셋 ≈ 0.9 eV** ✓ 본문의 *"lies ∼1 eV lower than the VBM"* **와 일치**.
  - **전도대 첫 구조 `figure-read ≈ +0.9–1.0 eV`** — 본문은 *"the in-gap state around **0.7 eV** originated from Co's d-orbital at the **interfacial** LCO"* 라 하지만, 실독하면 **그 봉우리도 진한 빨강("LCO_vac", ≈100)이 하늘색("LCO_1st", ≈40)보다 크다** ⇒ `Fig. 3` 과 **같은 문제**(§10-⑦).
- **E_f 분포 `Fig. 8` ✅ 실독**: 같은 6구간, y **0 … 1.0**, 파랑 Total / 빨강 LPO.

| 구간 | **(a) LCO(104)/LPO(010)** `figure-read` | *우리 산수* (×28) | **(b) LCO(104)/LPO(001)** `figure-read` | *우리 산수* (×36) |
|---|---|---|---|---|
| 1.0–1.5 | **0** | 0 | **0** | 0 |
| 1.5–2.0 | **0** | 0 | 0.028 | **1** |
| 2.0–2.5 | **0** | 0 | 0.14 | **5** |
| 2.5–3.0 | 0.045 | **1** | 0.277 | **10** |
| 3.0–3.5 | **0.765** | **21** | 0.277 | **10** |
| >3.5 | 0.19 | **6** | 0.277 | **10** |

> ✅ 검산: (b) 는 1+5+10+10+10 = **36 ✓** 캡션과 일치. (a) 는 1+21+6 = **28 ✓**.
> ⇒ **LPO(010) 은 2.5 eV 미만 자리가 0개**, **LPO(001) 은 2.0 미만이 1개(2.8 %)**.
> 🔴 **또 반대다**: 본문 §3.2 는 *"**five and four** … for the LCO(104)/LPO(**010**) and LCO(104)/LPO(**001**)"*, 캡션은 *"28 sites in **four** … and 36 sites in **five** … for LCO(104)/LPO(**010**) and LCO(104)/LPO(**001**)"* ⇒ **본문이 또 뒤집혀 있다**(§10-③).

**`Table S6`(LCO(104)/LPO(001), 전사)**

| 모형 | LC1 | LC2 | LC3 | LP1 | LP2 | LP3 | LP4 |
|---|---|---|---|---|---|---|---|
| (a) 최저 | 3.51 | 3.53 | 3.52 | 2.46 | 2.78 | 2.56 | **2.39** |
| (b) 최고 | 3.41 | 3.64 | 3.30 | 3.06 | 2.83 | 2.58 | 2.63 |

**`Table S7`(LCO(110)/LPO(010), 전사)**

| 모형 | LC1 | LC2 | LC3 | LP1 | LP2 | LP3 | LP4 |
|---|---|---|---|---|---|---|---|
| (a) 최저 | 3.05 | 3.57 | 2.89 | 3.51 | 3.08 | 3.37 | 3.11 |
| (b) 최고 | 3.04 | 3.23 | 2.98 | 3.48 | **2.18** | 3.14 | 2.80 |

- ⭐ **LCO 쪽 값이 거의 안 떨어진다**(3.30–3.64, 벌크 4.0). SI: *"the outermost Co atoms form CoO₆ octahedrons by sharing the O atoms of the PO₄ tetrahedrons and **create an environment close to the bulk LCO state**."* — LPS 계면의 LC3(2.21–2.41)와 대조적.
- **LPO 쪽은 벌크(5.1–5.2)보다 2 eV 이상 낮다**(2.39–3.06) — **밴드 오프셋 효과**이지 구조 파괴가 아니다. (본문은 벌크 LPO 를 *"about 5.0"* 이라 하는데 `Table S1` 은 **5.1–5.2** — 소소한 불일치.)
- **면방위**: LCO(110)/LPO(010) 은 LCO(104)/LPO(010) 보다 낮은 자리가 는다 (`Fig. S10`, 안 봄) — *"strong chemical activity of the LCO(110) surface"*.
- **양이온 교환 (`Fig. 9`, 안 봄 — 본문 전사)**: *"the reaction energies of cation exchange between LCO and LPO are **highly endothermic** … Co↔P and Co↔Li are **over 3 eV**"* ⇒ **LPO 는 반응층을 안 만든다.**

---

### 3e. LCO/LLZO 계면 (산화물 #2) — 본문 §3.3 (`Fig. 11` ✅ · `Fig. 12` ✅ · `Fig. 10`·`Fig. 13` 안 봄)

- **LLZO 무질서 처리 (본문 §2.1, 원문)**: 입방 Ia3̄d, *"On the Li sites …, **7/9 of 24d and 96h sites** … are occupied. According to the previous calculations (ref 48), we introduced the vacancy in **50 % and 40 % of the 96h and 24d sites**"* (refs 49 Adams, 50 Jalem).
  ⚠ *우리 산수*: 24d(24) + 96h(96) = **120 자리**에 Li 56개(= Li₇La₃Zr₂O₁₂ ×8, 192원자 셀 ✓). 공공 50 %/40 % 를 그대로 적용하면 점유 **48 + 14.4 = 62.4 ≠ 56** 이고 **정수도 아니다**. ⇒ **서술이 부정확하다**(§10-⑧).
- **μ = 13.0 %** — **8계면 중 최대**. 448원자(LCO 256 + LLZO 192).
- **구조**: *"more than half of the outermost Co atoms form CoO₆ octahedrons by sharing O atoms in the ZrO₆ **tetrahedrons**"* (⚠ ZrO₆ 는 팔면체다 — 오기).
- ⭐ **금속성 계면을 배제했다**: *"we **excluded** the interface structures that became **metallic** due to the in-gap state originated from the **LLZO surface**. The metallic interface structures had energies per interface area that were **2 orders of magnitude larger**…"* ⇒ **표본 선별 기준이 에너지 하나가 아니라 "금속성이면 버린다" 가 추가돼 있다.**
- **PDOS `Fig. 11` ✅ 실독**: x **−4 … +3**, y **0 … 600**. **영점이 갭 중심 ✓** (총 DOS 0 인 창 `figure-read ≈ −0.5 … +0.45`, 갭 ≈0.95 eV).
  - **LLZO(파랑) 가전자대 꼭대기 `figure-read ≈ −0.75`, LCO(연두) ≈ −0.55** ⇒ **오프셋 `figure-read ≈ 0.2 eV`** ✓ 본문 *"just around 0.2 eV lower than the VBM"* **와 일치**.
  - **LLZO 의 전도대 기여는 `figure-read ≈ +2.6 eV` 부터** (CBM +0.45 대비 **+2.1 eV 위**) ✓ 본문 *"at least 1 eV above the CBM"* 와 정합(보수적 서술).
  - ⚠ **"LCO vac"(진한 빨강)이 전 구간 거의 0 인 톱니선**이다 — `Fig. 3`·`Fig. 7` 에서는 큰 기여를 했는데 여기선 사라졌다. **세 PDOS 그림의 "LCO vac" 규격이 서로 다르다**(§10-⑦).
- **E_f 분포 `Fig. 12` ✅ 실독**: y **0 … 0.4**. 파랑 `figure-read` **0.031 / 0.031 / 0.22 / 0.344 / 0.344 / 0.031**, 빨강(LLZO) **0.031 / 0.031 / 0.188 / 0.282 / 0.061 / 0**.
  - *우리 산수*: 막대 최소치 0.031 = **1/32** 에 더 가깝고(1/36 = 0.028), 전 막대를 32로 환산하면 **1+1+7+11+11+1 = 32** 로 딱 떨어진다 ⇒ **캡션의 "36 Li sites" 와 어긋날 가능성**(저신뢰, `figure-read` 한계).
  - **E_f < 2.0 자리 = 2개 (≈6.2 %)** — **LPS 보다 훨씬 적고 LPO 보다는 많다** ✓ 본문 주장과 일치.
- **`Table S9` (전사)**

| 모형 | LC1 | LC2 | LC3 | LZ1 | LZ2 | LZ3 | LZ4 | LZ5 |
|---|---|---|---|---|---|---|---|---|
| (a) 최저 | 3.36 | 3.17 | 3.43 | 2.51 | 2.60 | 3.04 | 2.92 | 2.89 |
| (b) 고에너지 | 3.28 | 3.20 | 2.87 | **2.03** | 2.72 | **2.22** | 2.63 | 2.66 |

- **양이온 교환 (`Fig. 13`·`Fig. S16`, 안 봄 — 본문 전사)**: **Co↔Zr +0.7 ~ +1 eV** · **Co↔La > +1 eV (2층은 > +3.0)** · **Co↔Li +2 ~ +3 eV**. 전부 흡열이지만 *"if we compare the LCO/LPO surface, where all … are endothermic by over 3 eV, the reaction layer formation … at the LCO/LLZO interface **seems easier than at the LCO/LPO**."*
- **LLZO 의 약점**: *"some **LaO₈ complexes** in LLZO are **broken at the interface by stoichiometric reason** and it would disturb the atomic structure. Then, the LLZO interface tends to generate the **rather high energy interface structure**"* ⇒ **LLZO 는 고에너지 준안정 계면이 되기 쉽고, 그것이 Li 수송 저항의 기원이 될 수 있다.**

---

### 3f. 버퍼층 LTO — 본문 §3.4 (`Fig. 16` ✅ · `Fig. 14`·`Fig. 15` 안 봄)

#### (1) LTO(111)/LPS(010) — **1056 원자, 이 논문 최대 셀**

- **구조**: *"**no TiO₆ octahedron is broken** at the boundary to LPS, and **the interface bond with S atoms is not formed**, unlike in the case of LCO/LPS. Thus, the interface **preserves the atomic structure of the bulk crystal**."* LPS 쪽 Li 은 **LTO 표면 O 사이의 bridge 자리**에 앉는다.
- **PDOS (`Fig. 15`, 안 봄 — 본문 전사)**: *"there is **no gap state** around the interface. The CBM is composed of LTO and the **LPS states are located 1 eV higher than the CBM**, while the VBM consists of the LPS state and the states of LTO are **lower than −1.5 eV** with respect to the VBM."*
  ⇒ ⭐ **LPS 가 VBM 을 지배하고 LTO 가 1.5 eV 아래** — **[Haru14] 의 LNO/LPS 와 같은 방향**(SE 가 위, 버퍼가 아래). **버퍼는 양쪽에 전자 장벽**이다.
- **W_ad = 0.019 eV/Å²** — *"**smaller than those of the LCO/LPS interfaces**"* (본문 명시 비교, 이 논문에서 W_ad 를 비교한 **유일한** 문장).
- **E_f 분포 `Fig. 16` ✅ 실독**: y **0 … 0.5**. 파랑 `figure-read` **0 / 0 / 0.303 / 0.272 / 0.211 / 0.211**, 빨강(LPS) **0 / 0 / 0.303 / 0.272 / 0.060 / 0**.
  - **2.0 eV 미만 = 0개** ✓ 본문 *"no site with E_f less than 2.0 eV was found"*.
  - *우리 산수*: 33으로 환산하면 10+9+7+7 = 33 (캡션은 **31**) — `Fig. 12` 와 같은 소소한 어긋남(저신뢰).
- **`Table S11` (전사)**: LT1 3.30 · LT2 3.80 · LT3 3.60 / **LP1 3.03 · LP2 2.97 · LP3 2.95 · LP4 2.97 · LP5 3.05**
  > 🔧 ***우리 산수* — 버퍼 효과의 정량**: LPS 벌크 **2.9–3.2** 대비 **LPS 쪽 계면값 2.95–3.05 = 완전히 벌크 범위 안**. 낙폭 **≈0**. LCO/LPS 의 최저 1.23 과 비교하면 **버퍼가 1.7 eV 를 되돌린다**.
  > LTO 쪽은 벌크 5.0–5.1 → 계면 3.30–3.80 으로 **−1.3 ~ −1.7 eV** 떨어지는데, 이는 **SCL 이 아니라 밴드 오프셋 인공물**이다 (본문도 그렇게 설명한다). [Haru14] 의 LNO 와 **동일한 함정** — 혼동하면 안 된다.
- **양이온 교환 (`Fig. S19`·`S20`, 안 봄)**: **Ti↔P · Ti↔Li 모두 1 eV 이상 흡열** ⇒ *"the LTO buffer layer is **inert to the LPS surface**."*

#### (2) ⭐ LNO vs LTO — **다른 논문의 값과 직접 비교한다** (본문 §3.4 말미)

> 원문: *"We previously evaluated the values of E_f(V_Li_j) around the interface region between **LiNbO₃ (LNO) and LPS** and demonstrated that the vacancy formation energies have an **average of around 3.0 eV and a minimum of 2.4 eV** (ref 21 = [Haru14]). These are **larger than those of the present LTO/LPS interfaces**, implying that the **LNO buffer layer is superior to LTO** for decreasing the interfacial resistance."*

> 🔴 ***우리 산수* — 이 비교는 성립하지 않는다.**
> ① **U(Co 3d) 가 다르다**: [Haru14] **5.9 eV**(refs Juhin/Mattioli) vs 본 편 **4.9 eV**(ref 58 Zhou/Ceder). `E_f` 는 전자가 LCO 밴드로 가는 비용을 포함하므로 **U 에 직접 민감**하다.
> ② **인용한 수가 [Haru14] 에 그대로 없다**: [Haru14] `Table 1` 의 LNO/LPS 행 LPS 쪽 6자리는 **2.90 / 2.42 / 3.18 / 2.99 / 3.07 / 3.14** ⇒ 평균 **2.95**(본문 "around 3.0" ✓), 최소 **2.42**(✓ "2.4"). **값 자체는 맞다.**
> ③ 그런데 **본 편 LTO/LPS 의 LPS 쪽 5자리는 2.95 / 2.97 / 2.97 / 3.03 / 3.05 ⇒ 평균 2.994, 최소 2.95** 다. **평균은 LTO 가 *더 높고*(2.994 > 2.95), 최소도 LTO 가 *훨씬 높다*(2.95 > 2.42).**
> ⇒ **"LNO 가 LTO 보다 우수하다" 는 결론이 자기가 인용한 숫자와 정반대다.** (저자가 "these" 로 LTO 쪽 LT1–LT3 3.30–3.80 을 가리켰을 가능성도 있으나, 그러면 LNO 쪽 LN 자리 3.13–3.32 와 비교해야 하고 그래도 LTO 가 높다.) **§10-⑩ 로 간다.**

#### (3) LCO(104)/LTO(111) (`Fig. S22`·`Table S13`, 안 봄 — 전사)

- 424원자(LCO 256 + LTO 168), μ **7.5 %**, **3구조 평균**.
- **2.5 eV 미만 자리 0개.** `Table S13`: LC1 3.74 · LC2 3.71 · LC3 3.64 / LT1 3.20 · LT2 3.75 · LT3 3.90 · LT4 3.12 · LT5 3.73.
- 결론: *"the coating of LTO on the LCO surface **do not produce the interfacial resistive phase**."*

---

### 3g. 🔴 **부착에너지 W_ad — 전수** (본문 §3.1·§3.2·§3.4 + SI §S2)

**정의 (SI §S2 원문 그대로)**
> *"We define the adhesion energy W_ad as **W_ad = (E_totA + E_totB − E_totA/B)/S** where E_totA and E_totB are the total energies of **relaxed isolated slabs**, respectively, E_totA/B is the total energy of the A/B interface system, and **S is the interface area**"* (ref S8 = **Butler, Sai Gautam, Canepa, *npj Comput. Mater.* 5, 19 (2019)**).
> ⇒ **[Haru14] 와 완전히 같은 식.** 분모가 **S**(1 계면)이지 2S 가 아니다.
> ⚠ **`E_totA`·`E_totB` 가 *변형된* 셀인지 *원래 벌크* 셀인지 밝히지 않는다** — [Haru14] 와 같은 공백 (§10-⑥).

**논문에 있는 W_ad 는 이것이 전부다 (전수, 본문 grep 확인):**

| 계면 | **W_ad (eV/Å²)** — 논문값 | *우리 산수* **J/m²** | 위치 |
|---|---|---|---|
| **LCO(104)/LPS(010)** | **0.025** | **0.4005** | 본문 p. 11064 |
| **LCO(104)/LPO(010)** | **0.028** | **0.4486** | 본문 p. 11066 |
| **LCO(104)/LPO(001)** | **0.021** | **0.3365** | 본문 p. 11066 |
| **LTO(111)/LPS(010)** | **0.019** | **0.3044** | 본문 p. 11069 |
| ⛔ **LCO(110)/LPS(010)** | **보고 없음** | — | — |
| ⛔ **LCO(110)/LPO(010)** | **보고 없음** | — | — |
| ⛔ **LCO(104)/LLZO(001)** | **보고 없음** | — | — |
| ⛔ **LCO(104)/LTO(111)** | **보고 없음** | — | — |

*우리 산수* 환산: **1 eV/Å² = 1.602177×10⁻¹⁹ J / 10⁻²⁰ m² = 16.02177 J/m².**
→ 0.025 × 16.0218 = **0.4005** · 0.028 × 16.0218 = **0.4486** · 0.021 × 16.0218 = **0.3365** · 0.019 × 16.0218 = **0.3044**.

> 🔴🔴 **임무 ① 의 답 — `0.8 J/m²` 는 이 논문에 없다.**
> · **전수 grep 결과**: 본문·SI 전문에 `J/m`·`J m⁻²`·`fracture`·`toughness` 는 **0건**이다. 단위는 **오직 eV/Å²** 이고, 값은 **위 네 개뿐**이다.
> · 황화물 계면 값은 **0.025 eV/Å² = 0.400 J/m²** 하나. **0.8 의 정확히 절반**이다.
> · 이 논문이 **LCO(110)/LPS(010)** — 즉 [Haru14]·[Haru17] 이 쓴 그 계면 — 의 W_ad 는 **아예 보고하지 않는다.**
> · **[Haru14]** 쪽 값은 **4.3 eV/nm² = 0.043 eV/Å² = 0.6889 J/m²** 로, 역시 0.8 이 아니다.
> · Barai 2021 원문 (`inbox/11.…MAIN.pdf` p. 5537 확인): *"The bottom stability limit corresponds to sulfide-based electrolytes, which shows smaller magnitudes of fracture energy at the cathode/electrolyte interface, **around 0.8 J/m².⁶⁹,⁷⁰** … sulfide electrolytes with thiophosphate (Li₃PS₄) structure are being considered.**⁶⁹**"* — **ref 69 = [Haru14], ref 70 = 본 편.**
> ⇒ ***우리 산수* 판정: 0.8 J/m² 는 두 원전 어디에도 없는 수다.** 나올 수 있는 경로는 ⓐ **Okuno 0.400 × 2**(= 0.801, 자유표면 2개로 잘못 센 경우) 또는 ⓑ **Haruyama 0.689 를 "around 0.8" 로 올려 읽은 것** 둘 중 하나이고, **논문은 어느 쪽도 지지하지 않는다.**
> ⇒ **그리고 정의도 다르다.** Okuno·Haruyama 의 W_ad 는 **0 K 정적 DFT, 결함 없는 정합(strained) 이상계면의 *부착일*** 이고, Barai 의 Ψ_t 는 **연속체 lattice-spring 의 *파단문턱*(난수)** 이다. Barai 자신의 산화물 2.0 J/m² 는 **자기 DFT NMC/LLZO 벽개에너지**라 **세 번째 정의**다. ⇒ **세 수를 같은 표에 놓으면 안 된다.**

---

### 3h. 면방위 의존성 — 이 논문의 두 번째 축 (본문 §4 요약)

| 축 | (104) | (110) | 판정 |
|---|---|---|---|
| **E_f < 2.0 자리 비율 (LPS)** | 18.5 % | **30.4 %** | (110) 이 나쁨 |
| **최저구조에서 2.0 미만 출현** | 없음 (min 2.15) | **있음** (1.86) | (110) 이 나쁨 |
| **Co↔P(1층) 교환에너지** | **−0.76 ~ −1.25 eV** | **≈−2 eV** ([Haru17]) | (110) 이 나쁨 |
| **계면 화학** | CoO₅S + CoO₅ 사각뿔, Li on-top | CoO₄ 유사사면체 + CoO₄S, Li bridge | — |
| **LPO 에서도 같은 경향** | (104)/LPO(010) 0 % | (110)/LPO(010) 증가 | 재현됨 |
| **k-격자** | **Γ only** | **2×1×1** | 🔴 **통제 안 됨** (§10-④) |

결론 (원문): *"the LCO(110) surface is **more reactive** to LPS and generates more sites with low E_f … the **LCO(110) surface has a higher interface resistance than that of LCO(104)**."*
⇒ ⭐ **양극 입자의 *배향 제어*가 계면 저항을 바꾼다**는 주장. 이 논문이 [Haru14] 대비 새로 연 축이다.

---

### 3i. 밴드 오프셋 사다리 — 기전의 심장 (본문 §4)

| 계 | **VBO (SE 가 LCO VBM 보다 아래, eV)** | 출처 | **E_f < 2.0 비율** |
|---|---|---|---|
| **LPS** | **`figure-read ≈ 0.1–0.5`** (논문 미보고) | `Fig. 3` 실독 | **18.5–30.4 %** |
| **LLZO** | **≈0.2** (본문 명시) | `Fig. 11` ✓ 실독 일치 | **6.2 %** |
| **LPO** | **≈1.0** (본문 명시) | `Fig. 7` ✓ 실독 일치 | **0–2.8 %** |
| **LTO(버퍼)** | **≥1.5** (LTO 가 LPS VBM 보다 아래) | 본문 (`Fig. 15` 안 봄) | **0 %** |

요약문 (원문): *"In the oxide SE, the **large valence band offset** at the cathode−SE interface **suppresses the electron transfer** from the electrolyte to the cathode; this causes a **decrease in the number of sites with low E_f(V_Li_j)**."*

> ⚠ ***우리 산수* — 이 사다리는 단조가 아니다.** **LLZO(0.2 eV)가 LPS(`figure-read` 0.1–0.5 eV)와 같거나 더 작은 오프셋인데도 저(低)E_f 자리는 1/3–1/5 수준**이다. ⇒ **VBO 하나로는 설명이 안 되고, 음이온 화학(S²⁻ 의 높은 분극률·낮은 전기음성도)과 구조 변형이 따로 기여한다.** 논문은 요약에서 **VBO 를 단일 기전처럼** 제시한다 (§10-⑤).

---

### 3j. ⛔ NEB · MD — **0회**

**전수 grep (본문 + SI)**: `NEB` 0건 · `nudged` 0건 · `barrier` 0건 · `molecular dynamics` 0건 · `AIMD` 0건 · `diffusion coefficient` 0건.
- `migrat*` 은 3곳뿐이고 전부 **타 문헌 인용이거나 면 선택 이유**다: ① Haruta 2015 실험 인용 ② LTO(111) 을 고른 이유(*"the Li ions can migrate through"*, ref 52) ③ *"the Co cations **cannot migrate** to the neighboring Li sites"*(= 교환에너지가 2–3 eV 흡열이라는 정성 결론, **경로·배리어 계산 아님**).
- ⚠ **[Haru14] 에 있던 "끝점 전달에너지 2개"(−1.6 / −0.3 eV)조차 이 논문엔 없다.** 이 편은 **순수하게 정적 결함·교환 에너지 논문**이다.
- ⇒ **우리 NEB·MLIP-MD 와 방법 대조가 성립하지 않는다.** `Ea`·`D`·`σ` 어느 것도 회수할 수 없다.

---

## 4. DFT/계산 방법 ★ — 전수 (임무 ②)

### 4a. 논문이 **명시한** 것

| 항목 | 값 (원문) | [Haru14] 대비 |
|---|---|---|
| **code** | **Quantum ESPRESSO** (ref 54). **버전 미기재** | 동일 |
| **기저** | 평면파 + **ultrasoft** 유사퍼텐셜 (ref 56 Vanderbilt) | 동일 (⚠ **가전자 배치는 이번엔 안 적었다** — [Haru14] 는 원소별로 다 적었다) |
| **functional** | **PBE** (ref 57). **vdW 보정 0** | 동일 |
| **DFT+U** | Anisimov (ref 55). ⭐ **U(Co 3d) = 4.9 eV** (ref 58 = **Zhou, Cococcioni, Marianetti, Morgan, Ceder, PRB 70, 235121 (2004)**) · **Ti·Zr·La 에는 U 없음** | 🔴 **5.9 → 4.9 eV 로 1.0 eV 내렸다. 인용 근거도 바뀌었다** |
| **ecut** | **40 Ry** (파동함수) / **320 Ry** (전하밀도) | 동일 |
| **k-points (계면)** | ⭐ **2×1×1**: LCO(110)/LPS(010), "LCO(110)/LPO(001)"[**존재하지 않는 계면 — LPO(010) 오기**] · **그 외 전부 Γ 점 하나** | [Haru14] 는 **전 계면 Γ-only**. **이번엔 계면마다 다르다** |
| **k-points (벌크·표면)** | ⛔ **한 줄도 없다** | [Haru14] 는 벌크·표면 k 를 전부 줬다 (**후퇴**) |
| **스미어링** | **Gaussian, 0.001 Ry** (*우리 산수* = 13.6 meV) | 동일 ([Haru17] 만 0.01 Ry) |
| **스핀** | ⚠ **spin-unpolarized.** 근거: *"energy difference among the low-, intermediate-, and high-spin states are **within 0.2 eV per Co atom**"* (LCO(110) Li passivation 시험, ref 59 Qian 2012). LLZO·LTO 계면도 *"Spin nonpolarization is assumed"* | 동일 논리 (⚠ *"per Co atom"* 이 추가됐다 — [Haru14] 는 그냥 "0.2 eV") |
| **전하** | **중성 셀** (*"We set the system to be neutral"*). 결함 계산에도 전하보정 없음 | 동일 |
| **슬랩 두께** | *"around **1–2 nm**"* | 동일 |
| **진공** | *"**up to 1.5 nm**"* / *"about **1–1.5 nm**"* | [Haru14] 는 *"about 1.5 nm"* (**약간 느슨해졌다**) |
| **쌍극자** | *"These slabs were **approximately dipole-free**"* — **보정은 안 함** | [Haru14] 는 **ESM 대조**(차이 0.1 / 0.01 eV)를 했다. **이번엔 그것도 없다 (후퇴)** |
| **supercell / nat** | ⭐ **8계면 전부 SI 에 총 원자수·성분별 원자수·반복수·μ 기재** | 🎉 **[Haru14] 의 최대 공백을 메운다** |
| **시각화** | **VESTA** (ref 53) | 동일 |
| **자원** | **RIKEN AICS K computer** (HPCI) | [Haru14] 는 NIMS·九州大·ISSP·Oakleaf-FX |

### 4b. 🔴 논문이 **안 밝힌** 것 (우리 v5 와 나란히 놓으려면 통제해야 하는데 불가능한 축)

| 통제축 | 논문 | 비고 |
|---|---|---|
| **이완 자유도 (전원자 자유? 층 고정? 몇 %?)** | ⛔ **없다.** *"local structure optimization"* 한 마디뿐. `fixed`·`frozen`·`constrain` 전수 grep **0건** | 🔴 **우리 FixAtoms 33 % 와 대조할 근거가 없다.** [Haru14] 는 *"전 원자 위치 + 횡방향 셀 파라미터 자유"* 를 **명시했다** — **후퇴** |
| **셀 파라미터 이완 여부** | ⛔ **없다** | [Haru14] 는 이완했다고 명시 |
| **힘 수렴 기준** | ⛔ **없다** (`force`·`Ry/bohr`·`converg` 전수 grep **0건**) | [Haru14] **0.001 Ry/bohr** (= 0.0257 eV/Å) — **후퇴** |
| **응력 수렴 기준** | ⛔ **없다** | [Haru14] **0.5 kbar** — **후퇴** |
| **에너지 수렴 기준 (SCF)** | ⛔ **없다** | — |
| **벌크·표면 k-격자** | ⛔ **없다** | [Haru14] 는 전부 명시 — **후퇴** |
| **PDOS nscf 조건** | ⛔ **없다** | [Haru14] 는 2×1×1 / 2×2×1 명시 — **후퇴** |
| **β-Li₃PS₄ 무질서 처리** | ⛔ **없다** (SQS·enumerate·Lepley 모형 언급 0건). `Table S1` 각주는 실험 구조(Mercier 1982)만 | 🔴 [Haru14] 는 **Lepley β-Li₃PS₄-b** 를 명시했다. **그리고 격자상수가 서로 다르다**(§3a) — **후퇴** |
| **LLZO Li 무질서** | 부분 명시(50 %/40 %)지만 **정수 해가 없다** | §3e |
| **QE 버전** | ⛔ **없다** | 동일 |
| **좌표 파일 / 원시 총에너지** | ⛔ **없다** | [Haru17] 만 `Table S3` 로 공개했다 |
| **법선방향 셀 길이** | ⛔ **없다** (*우리 산수* ≈38–50 Å, §3b-4) | [Haru14] 와 동일한 공백 |
| **초기 계면 간격** | ⛔ **없다** | 동일 |
| **표본 개수** | 🔴 **본문 ↔ 그림 캡션 ↔ SI 가 서로 다르다** (§10-③) | — |

> ⇒ **임무 ② 의 답**: **① functional PBE ② U(Co) 4.9 eV, Ti/Zr/La 는 U 없음 ③ USPP ④ 40/320 Ry ⑤ k = Γ 또는 2×1×1(계면마다 다름) ⑥ spin-unpolarized ⑦ Gaussian 0.001 Ry ⑧ 쌍극자·ESM 보정 없음 ⑨ 진공 1–1.5 nm ⑩ nat·슬랩두께는 SI 에 있음(본 §3b-4 에 복원)** 까지는 통제 가능하다. **그러나 ⑪ 이완 자유도 ⑫ 힘·응력 수렴 ⑬ 무질서 처리 세 축은 논문이 말을 안 해서 통제 자체가 불가능하다.** ⇒ **우리 v5 의 1.28 J/m² 와 이 논문의 0.400 J/m² 를 "차이" 로 해석하면 안 된다** (§7a-2).

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | **표면 6종의 구조** — LCO(104)/LCO(110)/LPS(010)/LPO(001)/LLZO(001)/LTO(111). 다면체 색: CoO₆ 파랑, PS₄ 초록, PO₄ 회색, ZrO₆ 연두, LaO₈ 갈색, TiO₆ 하늘 (**안 봄** — 면지수·종단이 본문 활자) | 우리 NCM 면 선택의 대조군 |
| **2** | ✅ **완화된 LCO\|LPS 계면 2종(측면 + 인셋)**. **(a)=110**: CoO₂ 띠 수평 3장, 인셋에 **CoO₄S**; **(b)=104**: CoO₂ 사선, 인셋에 **Li 이 O 위 on-top** | 🔴 **캡션의 (a)/(b) 가 뒤바뀌어 있다** — 그림 안 라벨이 맞다. 우리 v5 계면 xyz 와 눈으로 대조할 1순위 |
| **3** | ✅ **LCO(104)/LPS(010) PDOS**. 5곡선(Total/LCO/LPS/LCO vac/LCO 1st), x −2…+4 | ⭐ 축 D. **VBO(LCO−LPS) `figure-read ≈ 0.1–0.5 eV`**(논문 미보고). 🔴 **영점이 캡션과 안 맞고, 중갭 봉우리가 *진공면* 기여 우세** |
| **4** | ✅ **LPS 계면 2종의 E_f 히스토그램**(6구간, 파랑=전체·빨강=LPS쪽) | ⭐⭐ **이 논문의 본체.** *우리 산수* E_f<2.0 = **18.5 %(104) / 30.4 %(110)**. 막대→자리수 환산이 캡션(65/23)과 **정확히 일치** = 읽기 검증됨 |
| **5** | ✅ **LCO(104)/LPS 양이온 교환**: (a) 자리 라벨, (b) **Co↔P −0.76/−1.25/−1.00**(1층) · **+0.38/−0.09/≈0**(2층), (c) **Co↔Li +2.25 … +3.31** | ⭐ 우리 계면 반응성 축의 보고량 설계 선례. **배위 덜 찬 Co(사각뿔)가 가장 잘 섞인다** |
| 6 | 완화된 LCO(104)\|LPO 계면 2종 (**안 봄**) | CoO₆ 재생 = 산화물이 매끄러운 이유 |
| **7** | ✅ **LCO(104)/LPO(001) PDOS**, x −3…+3 | ⭐ **VBO ≈0.9 eV `figure-read`** ✓ 본문 "∼1 eV" 와 일치. **영점 = 갭 중심 ✓**(`Fig. 3` 과 규격이 다르다) |
| **8** | ✅ **LPO 계면 2종의 E_f 히스토그램** | ⭐ *우리 산수* E_f<2.0 = **0 %(010) / 2.8 %(001)**. 🔴 본문의 표본 개수와 캡션이 **정반대** |
| 9 | LCO(104)/LPO(001) 양이온 교환 Co↔P·Co↔Li (**안 봄** — 본문이 *"over 3 eV"* 로 준다) | LPO 는 반응층 안 만듦 |
| 10 | 완화된 LCO(104)\|LLZO(001) (**안 봄**) | LaO₈ 파손 확인용 |
| **11** | ✅ **LCO(104)/LLZO(001) PDOS**, x −4…+3 | ⭐ **VBO ≈0.2 eV `figure-read`** ✓ 본문 일치. **LLZO 전도대는 CBM 보다 ≈2.1 eV 위**. ⚠ "LCO vac" 곡선이 **거의 0** — 세 PDOS 그림의 규격 불일치 |
| **12** | ✅ **LLZO 계면 E_f 히스토그램**, y 0–0.4 | *우리 산수* E_f<2.0 = **6.2 %**. ⚠ 막대는 **N=32** 에 맞고 캡션은 36 |
| 13 | LCO/LLZO 양이온 교환 Co↔Zr·Co↔La (**안 봄** — 본문이 수치로 준다) | Co↔Zr 0.7–1 < Co↔La 1–3 |
| 14 | 완화된 LTO(111)\|LPS(010) (**안 봄**) | **S–Ti 결합 없음 · TiO₆ 무손상** |
| 15 | LTO/LPS PDOS (**안 봄** — 본문이 수치로 준다) | **중갭 상태 0 · LTO 가 VBM 보다 1.5 eV 아래** |
| **16** | ✅ **LTO/LPS E_f 히스토그램** | ⭐ **2.0 eV 미만 0개.** LPS 쪽 2.95–3.05 = **벌크 복귀** |
| **S1** | ✅ **LCO/LPS 슬랩 모형 2종, top+side 2뷰** | ⭐⭐ **기하 원전.** (b) 우측 뷰에서 **LCO(110) 의 CoO₂ 띠 3장 + Li 열**을 셀 수 있다. 계면 법선은 **c(수평)**. ⚠ 크롭 안에서 **진공 영역이 안 보인다**(크롭 경계에 잘렸을 수 있다) |
| S2 | LCO(104)/LPS 의 Co 원자별 PDOS (**안 봄**) | **CoO₅ 사각뿔이 중갭 상태를 만들고, CoO₅S 는 안 만든다** (SI 본문) |
| S3, S9, S11, S15, S18, S21, S23 | 각 계면의 Li 자리 라벨 그림 (**안 봄** — 값은 `Table S3/S6/S7/S9/S11/S13` 전사) | 자리 분류 체계 |
| S4 | LCO(104)/LPS 최저 vs 최고 구조의 Co↔P (**안 봄**) | **고에너지 구조일수록 더 발열** |
| S5, S6 | Co↔P 혼합 후 Li 자리 / 혼합 후 DOS (**안 봄**) | **혼합 → 중갭 Co d 증가 → E_f 하락** |
| S7, S8, S13, S17 | LPO·LLZO·LTO 계면의 슬랩 모형 (**안 봄**) | 기하 확인용 |
| S10, S22 | LCO(110)/LPO(010), LCO(104)/LTO(111) E_f 히스토그램 (**안 봄**) | 각각 "(110) 이 더 나쁨", "2.5 미만 0" |
| S12 | 벌크 LLZO DOS (**안 봄**) | VB=O, CB=Zr/La |
| S14 | LCO/LLZO 원소별 PDOS (**안 봄**) | LLZO VBM 은 O 주도 |
| S16, S19, S20 | Co↔Li(LLZO), Ti↔P·Ti↔Li 교환 (**안 봄**) | 전부 흡열 |
| **Table S1** | 벌크 격자 + **E_v** (전사, §3a) | ⭐ **벌크 기준선**. ⚠ **밴드갭 없음** |
| **Table S2/S5/S8/S10/S12** | **반복수 + μ** (전사, §3b-4) | ⭐⭐ **기하 원전의 본체.** *우리 산수* 로 셀·두께·면적 복원 |
| **Table S3/S6/S7/S9/S11/S13** | 자리별 E_f (전사, §3c–3f) | ⭐ 히스토그램의 원자료 |
| **Table S4** | **Co↔P 혼합 전후 E_f** (전사, §3c-5) | ⭐ **평균 2.28 → 1.56 eV** (*우리 산수*) |

---

## 6. Post-processing ★

- **무엇을 했나**
  1. **Li 공공 형성에너지** `E_f(V_Li_j) = {E_tot(V_Li_j) + E_Li} − E_tot`, **E_Li = bcc Li 금속**, **중성 셀** — **총 271 자리**(65+23+28+36+28+36+31+24).
     저자 주석: *"This scheme is **valid when the electron can be extracted simultaneously**"* — 즉 `LiₙX → Liₙ₋₁X + Li⁺(sol) + e⁻` 와 `Li⁺ + e⁻ → Li(s)` 두 전기화학 반응으로 나뉠 때만 유효.
  2. **상호 양이온 교환에너지** `E_ex = E_tot(A_j ↔ B_k) − E_tot` (조성 보존 in-place 스왑). 저자 주석: *"the full evaluation of the exchange probability **requires a consideration of the reaction kinetics**"* — **동역학은 안 했다.**
  3. **PDOS** (원자군별 투영: SE 전체 / 양극 전체 / **진공 마주한 첫 층** / **SE 마주한 첫 층**, 일부는 원소별·다면체별).
  4. **부착에너지 W_ad** — **4개만**.
  5. **미스핏 μ** — 면적 중첩 정의 (refs S6 Liu 2003, S7 Martin 2012), [Haru14] 와 동일.
  6. **구조 표본 통계** — 이 논문의 방법론적 기여.
- **도구**: **VESTA** (구조 시각화). pymatgen·LOBSTER·Bader·VASPKIT **전부 미사용**.
- **수치화·기록**: SI 표 13개. **그림은 전부 정규화 히스토그램**(자리수 자체는 캡션에만). **원시 총에너지 비공개** ⇒ **재현 검산 불가.**
- ⛔ **안 한 것**: NEB · AIMD · MD · MLIP · COHP/ICOHP · Bader · ELF · BVSE · grand-potential ESW · 포논 · 탄성 · 전위(전기) 프로파일 · Debye 길이 · 계면 저항(Ω cm²) 계산 · **전하보정(Makov–Payne 등)** · **쌍극자 보정**.

---

## 7. 우리 대비

### 7a-1. ⭐⭐ **우리 v5 계면 기하와 대조** — *판정하지 않고 나란히만 둔다*

> 우리 쪽 출처: `kb/results/adhesion_final.md` · `db/properties/adhesion.json` · `kb/results/adhesion_v5_full_report.md`.
> ⚠ **우리 adhesion 은 `db/properties/canonical_registry.json` 에 없다** (원장 바깥 값). 이 표의 우리 수는 **작업기록값**이다.

| # | 대조 항목 | **[Okuno20] 원문 / *우리 산수* 복원** | **우리 v5 (현재 기록)** |
|---|---|---|---|
| 1 | **계면 형식** | **단일 계면 + 진공** (샌드위치 반대 — 단, [Haru14] 보다 약한 논거) | **단일 계면 + 진공** ✅ 같다 |
| 2 | **진공 두께** | **10–15 Å** (*"up to 1.5 nm"*, *"about 1–1.5 nm"*) | **30 Å** (UMA vacuum-sensitivity: 60 Å 에서 W_ad 24.5 J/m² 로 폭주) |
| 3 | **양극 면지수** | **LCO (104)** 와 **(110)** — **둘 다** 돌려 비교 | v5 보고서 **면지수 미기재**; v26/v27 은 LiNiO₂ (003)/(110)/(012)/(104) |
| 4 | **SE 면지수** | **β-Li₃PS₄ (010)** (Li 전도축 b 가 법선) | LPSCl **prim 2×2×3 (624원자)** — **면지수 미기재** |
| 5 | **종단** | 다면체 보존 + **화학양론** + *"approximately dipole-free"*. LPO·LTO 는 **Li 종단 명시**, **LCO·LPS 는 미기재** | v5 보고서에 **종단 기술 없음** |
| 6 | **격자 정합 방향** | **LPS 를 LCO 에 맞춘다**(탄성계수 논거). 산화물끼리는 **평균** (⚠ SI 는 LTO 도 LCO 에 맞췄다고 씀) | **SE 를 NCM 에 맞춘다** (SE strained) — **같은 방향** |
| 7 | **정합 배수** | LCO(110) **5×1** 표면셀 : LPS **1×4** (*우리 산수*) | SE 2×2×3(624at) + NCM 7×7×1(196at) |
| 8 | **미스핏** | **μ 3.9–13.0 %** (면적 중첩 정의). LCO(110)/LPS **4.6 %** | **strain +0.2 %**(Li6 계열) / **+1.1 %**(Li5.4) — **정의가 다르다** |
| 9 | **계면 면적** | **LCO(110)/LPS ≈ 320–345 Å²** (*우리 산수*) | **351 Å²** — 🎯 **거의 같다** |
| 10 | **총 원자수** | **736** (LCO 480 + LPS 256) · 8계면 384–1056 | **820** (SE 624 + NCM 196) |
| 11 | **슬랩 두께** | LCO(110) **11.34 Å (8층)** · LPS **16.32 Å (2셀)** (*우리 산수*) | SE **30 Å** · NCM 7×7×1 (두께 미기재) |
| 12 | **법선 셀 길이** | ⛔ 미기재 (*우리 산수* **≈38–45 Å**) | `cell_z = atoms_max + 30 Å` |
| 13 | **횡방향 샘플링** | **무작위 lateral shift** + 통계. 표본 **3–8개/계면** | **xy-shift 20 seeds** (comp1) — **우리가 표본이 더 많다** |
| 14 | **이완 자유도** | ⛔ **미기재** (*"local structure optimization"* 뿐) | **하단 33 % FixAtoms** (UMA 안정화) — 🔴 **대조 불가** |
| 15 | **힘 수렴** | ⛔ **미기재** | **fmax 0.01 eV/Å** (LBFGS) — 🔴 **대조 불가** |
| 16 | **초기 간격** | ⛔ 미기재 | **gap 2.5 Å** |
| 17 | **힘 계산기** | **DFT+U** (QE · PBE · USPP · **U(Co)=4.9** · Γ 또는 2×1×1) | **UMA-s-1p1 (MLIP)** — ⭐ **최대 차이** |
| 18 | **W_ad 식** | `(E_A + E_B − E_AB)/S`, 분모 **S**(1 계면) | **동일** ✅ |
| 19 | **W_ad 값** | **LCO(104)\|LPS 0.400 J/m²** · LPO 0.337–0.449 · LTO\|LPS 0.304. ⛔ **LCO(110)\|LPS 는 없음** | **comp1 1.28 J/m²** (`adhesion_final.md`) · xy_shift 20-seed **평균 1.153 ± 0.392, 중앙값 0.962** | 
| 20 | **구조 산포** | **ΔE/S 가 W_ad 의 21–495 %** (*우리 산수*) | **std/mean = 34 %** (comp1 20-seed) — ⚠ **양쪽 다 크다** |
| 21 | **변형에너지 상쇄** | ⛔ **불명** (`E_A`·`E_B` 가 변형 셀인지 원 셀인지 안 적음) | v5 보고서가 **스스로 이 함정을 기록** (method_A "STRAIN ARTIFACT") |
| 22 | **무질서 처리** | ⛔ **미기재** (β-LPS Li 배열) | 우리는 **조성별 배열을 선언**하고 시드를 돌린다 — **우리가 낫다** |

### 7a-2. 🔴 **그래서 우리 1.28 과 이 논문의 0.400 을 나란히 놓을 수 있나 — 아니다**

**비율만 보면 3.20×** (1.28 / 0.4005). 그런데 그 3.20 안에 **최소 일곱 개의 통제 안 된 축**이 섞여 있다:

| 축 | 저쪽 | 우리 | 이 축 하나로 얼마나 움직이나 |
|---|---|---|---|
| **힘 계산기** | DFT+U | **UMA MLIP** | 미지 — **우리도 DFT 대조를 안 했다** |
| **양극 물질** | LiCoO₂ | **LiNiO₂** | 미지 |
| **SE 물질** | β-Li₃PS₄ | **Li₆PS₅Cl** (free S²⁻ + Cl⁻) | 미지 |
| **양극 면지수** | **(104)** | 미기재 | 🔴 **같은 논문 안에서 (104) vs (110) 의 E_f·교환에너지가 1.6–2배 갈린다** |
| **이완 자유도** | 미기재 | **FixAtoms 33 %** | 🔴 **통제 불가** |
| **진공** | 10–15 Å | **30 Å** | 🔴 우리 쪽 실측: **60 Å 에서 24.5 J/m²** (20배) |
| **구조 표본** | 3–8개, 최저값 채택 | 20 seeds, **평균 1.153 / 중앙값 0.962** | 🔴 **대표값 정의가 다르다** |

> ⇒ ***우리 산수* 판정: 1.28 vs 0.400 의 "3.2배" 는 물리가 아니라 *방법 축의 합*이다.**
> 특히 **대표값 정의만 바꿔도** 우리 쪽이 1.28 → 0.962(중앙값)로 25 % 내려가고, **저쪽은 최저구조 1개** 값이다.
> 그리고 **저쪽 자신의 같은-계열 값이 0.400(104) ↔ 0.689(110, [Haru14]) 로 1.72배 갈린다** — 즉 **문헌 내부 산포만으로도 우리 비율의 절반이 설명된다.**
> 🔴 **따라서 `db/literature/refs.json` 의 `"Our … 1.28 J/m² is ~2× their LCO/LPS = 0.69 J/m². Reasonable: LiNiO₂ more reactive than LCO per Komatsu"` 주석은 유지 불가하다.** (§11-② · 병합대기 파일 ④)

### 7b. `our_dft_baseline.md` 대비 (물성 4축)

| 축 | **[Okuno20]** | **우리 (comp1 / modelc)** | 판정 |
|---|---|---|---|
| **A 이온전도 (Ea/σ/D)** | ⛔ **없음** (NEB·MD 0회). 인용된 실험값 하나: 나노다공성 LPS **1.64×10⁻⁴ S/cm @RT** (ref 41 Liu 2013) — **이 논문 계산값 아님** | Ea 0.253 / 0.224 eV, D(600 K) 3.09 / 7.90 ×10⁻⁶ cm²/s (MLIP-MD) | **대조 불가** |
| **B 산화안정 (4축)** | ⛔ **grand-potential 0회 · ESW 0회.** 다만 **축 ④(계면 반응/반응층)** 에 정성 기여: Co↔P 발열, LPS 분해 산물은 **ref 30(Richards/Ceder) 인용**(P₂S₇, Co(PO₃)₂, Co₂S) | 2.256 V (S²⁻-limited, 축 ①) | **축이 다르다** — 우리 ①(음이온 산화) vs 저쪽 ④(양이온 교환). ⛔ **같은 표 금지** |
| **C 기계** | ⛔ **없음.** 정성 언급만: *"the rather **low elastic modulus of LPS**"*(정합 방향 근거) | comp1 E_VRH 22.06 / modelc 27.66 GPa | **대조 불가**. *"황화물이 무르다"* 방향만 일치 |
| **D 전자구조 (gap)** | ⛔ **벌크 갭 0개** (`Table S1` 에 E_g 열이 없다). 계면 실효갭 `figure-read`: LPS 계 **≈0.8 eV** · LPO 계 **≈0.9** · LLZO 계 **≈0.95** | comp1 2.066 / modelc 2.099 eV (PBE, fixed-occ nscf) | ⛔ **숫자 비교 금지** — 물질·판독법·계(계면 vs 벌크) 전부 다름. **"둘 다 wide-gap"** 까지만 |
| **계면 (γ, W_ad)** | **W_ad 4개 (0.304–0.449 J/m²)**. γ(표면에너지) **0개** — [Haru14] 는 4개 줬는데 **후퇴** | W_ad comp1 1.28 (또는 20-seed 1.153±0.392) · γ_SE 1.211 J/m² (UMA) | ⚠ **소환값. 순위·방향만** (§7a-2) |
| **Li 공공 형성에너지** | **271 자리** (계면 8종) + 벌크 5종 | ⛔ **우리 원장에 없다** | ⭐ **우리가 안 가진 축** (§8-①) |
| **양이온 교환에너지** | **LCO/LPS·LPO·LLZO·LTO 전수** | ⛔ **우리 원장에 없다** | ⭐ **우리가 안 가진 축** (§8-②) |

### 7c. 🔧 **방법 원전으로서의 가치** — 물성값이 아니라 *설계*를 가져온다

1. **"분포로 보고하라"** — [Haru14] 는 최저구조 1개의 `Table 1` 이었다. 본 편은 **표본 3–8개 × 자리 23–65개 → 히스토그램**이다. 저자 문장: *"**Calculating the statistics of the physical properties is important to obtain reliable results.**"*
   ⇒ **우리 보고량 규율(`kb/templates/estimand_card.md`)이 요구하는 "집계 규칙"의 문헌 선례**다. 무질서 아지로다이트에서 `E_f(자리)` 는 스칼라가 아니라 **분포**이고, 이 논문이 그 보고 형식을 이미 쓴다.
2. **"2.0 eV 미만 비율"이라는 단일 스칼라 요약** — 분포를 쓰면서도 **의사결정용 스칼라 하나**를 뽑는 방식. 우리가 조성 6종을 비교할 때 그대로 쓸 수 있다.
3. **단일계면 + 진공 + W_ad 식 + 횡방향 registry 탐색** — [Haru14] 와 동일. **우리 v5 프로토콜의 2차 근거**.
4. ⚠ **동시에 "이렇게 쓰면 안 된다"의 교보재**이기도 하다 — 수렴기준·이완 자유도·무질서를 안 적으면 **6년 뒤 누구도 통제 비교를 못 한다**(§4b).

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

**① ⭐⭐ "계면 자리별 Li 공공 형성에너지 분포" 는 우리가 안 가진 축이고, 지금이 제일 싸다.**
우리 v5 LiNiO₂|LPSCl 계면 구조는 **이미 있다**(820원자, A=351 Å², 20 seeds). 거기서 **계면 근처 Li 자리 20–40개**의 중성 공공 형성에너지(μ_Li = bcc Li)를 뽑으면 **이 논문과 같은 축의 값**이 나온다. 보고량 카드에 미리 박을 것:
ⓐ **자리 선택 규칙** — 아지로다이트는 등가자리가 없다 ⇒ **"계면에서 n Å 이내 전 Li"** 같은 기하 규칙으로 정의하고 **분포로 보고**한다 (스칼라 금지).
ⓑ **집계 스칼라** — 이 논문의 **"E_f < 2.0 eV 비율"** 을 그대로 쓰되, **문턱값을 우리가 정당화**해야 한다 (저쪽도 근거를 안 댔다).
ⓒ **전자가 어디로 가나** — 중성 셀이면 **밴드정렬이 값을 정한다**. 우리는 LiNiO₂ 의 VBM 이 LPSCl 보다 어디 있는지 **PDOS 를 낸 적이 없다** ⇒ ⓒ 가 ⓐ보다 먼저다.
ⓓ **계산기** — 이 축은 **총에너지 차이 ~0.1 eV 를 논한다**. UMA 로는 못 한다. **QE DFT 가 필요**하고, 그러면 820원자 × 자리 30개는 비싸다 ⇒ **작은 계면 셀을 따로 만들어야 한다**(저쪽은 384–1056원자로 했다).

**② ⭐ "양이온 교환에너지" 는 우리 B축 ④(계면 반응)에 바로 붙는 보고량이다.**
`E_ex = E_tot(A↔B) − E_tot` 는 **조성 보존 in-place 스왑**이라 화학퍼텐셜 기준이 필요 없다 — **우리가 지금 못 하는 grand-potential 계면 확장보다 훨씬 싸다**. 우리 계에서 물어볼 것: **Ni↔P** (저쪽 Co↔P = −0.76 ~ −2 eV) · **Ni↔Li** · ⭐ **Cl↔O / Cl↔S** (저쪽엔 없는, **우리만 물을 수 있는 축**). Cl-rich 가 계면 반응층을 억제하는지 여부가 **우리 서사의 빈칸**이다.

**③ ⭐⭐ 면방위 의존성이 우리 v5 의 최대 미기재 항목을 겨눈다.**
이 논문의 가장 견고한 결론은 *"같은 물질쌍이라도 면방위가 바뀌면 Li 고갈 비율이 1.6배, 양이온 혼합 에너지가 2배 갈린다"* 이다. **그런데 우리 v5 보고서에는 NCM 면지수가 없다.** ⇒ **우리 W_ad 1.28 이 어느 면의 값인지부터 확정**해야 하고, 그전까지는 **문헌 W_ad 와의 비율을 물질 차이로 해석하면 안 된다**(§11-②). v26/v27 이 (003)/(110)/(012)/(104) 를 이미 돌렸으니 **연결만 하면 된다.**

**④ 🔴 "진공면이 중갭 상태를 만든다" 는 우리 v5 에도 그대로 적용된다.**
`Fig. 3`·`Fig. 7` 실독에서 **중갭 봉우리의 우세 기여가 "LCO vac"(진공 마주한 층)** 이었다. 우리 v5 도 **단일계면 + 진공 30 Å** 이므로 **자유표면이 두 개**(SE 위, NCM 아래) 있다. ⇒ 우리가 계면 PDOS 를 내는 날 **"계면 상태"와 "자유표면 상태"를 층별 투영으로 반드시 갈라야** 한다. 이 논문은 **투영은 했는데 해석에서 섞었다** — 같은 실수를 피할 수 있다.

**⑤ 버퍼/코팅 캠페인의 정량 목표함수.**
LTO/LPS 에서 **LPS 쪽 E_f 가 2.95–3.05 = 벌크(2.9–3.2) 완전 복귀**, LCO/LPS 최저 1.23 대비 **+1.7 eV**. ⇒ 우리 Nd 인산염/코팅 캠페인이 열리면 **"코팅의 목표 = SE 쪽 계면 Li 자리의 E_f 를 벌크값으로 되돌리기(= 저E_f 자리 비율 0 %)"** 라는 **측정 가능한 목표**를 쓸 수 있다. ⚠ 단 **§3f-(2) 의 LNO vs LTO 결론은 자기 숫자와 모순**이므로 **"LNO > LTO" 를 인용하면 안 된다.**

---

## 9. 인용 가능 문장 (deck/paper 용)

- "동일한 LiCoO₂ 양극에 대해 황화물(β-Li₃PS₄)과 산화물(γ-Li₃PO₄, Li₇La₃Zr₂O₁₂) 전해질 계면을 **같은 제1원리 방법으로 비교**한 결과, **황화물 계면에서만 Li 공공 형성에너지가 2.0 eV 미만인 자리가 다수 나타났다** [Okuno, Haruyama, Tateyama, *ACS Appl. Energy Mater.* **3**, 11061 (2020)]."
- "그 차이의 기전으로 저자들은 **양극–전해질 가전자대 오프셋**을 든다 — 오프셋이 크면 전해질에서 양극으로의 **전자 이동이 억제**되어 동적 Li⁺ 고갈이 덜 일어난다. 보고된 오프셋은 **Li₃PO₄ 약 1 eV, LLZO 약 0.2 eV** 다 [같은 문헌]."
- "계면 저항은 물질쌍뿐 아니라 **결정 면방위**에도 의존한다 — **LiCoO₂(110)** 은 **(104)** 보다 β-Li₃PS₄ 에 더 반응성이 크고 저(低)공공형성에너지 자리를 더 많이 만든다 [같은 문헌]."
- "**양이온 상호혼합(Co↔P)이 Li 고갈을 가속한다** — 혼합 후 같은 Li 자리의 공공 형성에너지가 **2.40 → 1.39 eV 까지 내려간다** (`Table S4`) [같은 문헌]."
- "**Li₄Ti₅O₁₂ 버퍼층**을 끼우면 β-Li₃PS₄ 쪽 Li 공공 형성에너지가 **2.95–3.05 eV 로 벌크값(2.9–3.2 eV)에 복귀**하고 2.0 eV 미만 자리가 **사라진다** [같은 문헌]."
- ⚠ (조건부) "정적 DFT 로 계산된 LiCoO₂(104)\|β-Li₃PS₄(010) 계면의 **부착일은 0.025 eV Å⁻² (= 0.40 J m⁻²)** 이다" ← **면지수와 단위를 반드시 같이** 쓴다.
- ⛔ **쓰면 안 되는 문장**:
  · *"Okuno 2020 이 황화물 계면 파괴에너지를 **0.8 J/m²** 로 계산했다"* — **이 논문에 그 수는 없다** (§3g).
  · *"Okuno 2020 의 LCO(110)\|LPS 부착에너지는 ○ 다"* — **보고되지 않았다.**
  · *"Okuno 2020 이 Li 이동 배리어를 계산했다"* — **NEB 0회.**
  · *"LNO 버퍼가 LTO 보다 우수하다 [Okuno 2020]"* — **자기 숫자와 모순된다** (§3f-2, §10-⑩).
  · *"이 논문이 공간전하층 두께/전위를 냈다"* — **SCL 이라는 말조차 기전 후보 나열에만 나온다.**

---

## 10. 주의 / 한계 (over-claim 방지) — **비판**

① 🔴 **W_ad 를 4개만, 그것도 결론이 걸린 계면을 빼고 준다.**
LCO(104)/LPS · LCO(104)/LPO ×2 · LTO/LPS **넷뿐**이고, **LCO(110)/LPS · LCO(110)/LPO · LCO/LLZO · LCO/LTO 는 없다.** 본문에서 W_ad 를 **비교·해석한 문장은 단 하나**(*"LTO/LPS 는 LCO/LPS 보다 작다"*)이고, 나머지는 값만 던진다. **면방위 의존성이 이 논문의 두 축 중 하나인데, 정작 부착에너지의 면 의존성은 측정조차 안 했다.** ⇒ 뒤에 인용하는 쪽(Barai 2021)이 **"황화물 계면 파괴에너지"** 라는 단일 수를 만들어 쓰게 된 구조적 원인이다.

② 🔴 **`Fig. 2` 의 패널 라벨이 캡션과 뒤바뀌어 있다** (실독으로만 잡힌다).
그림 안: (a) LCO(110)/LPS(010), (b) LCO(104)/LPS(010). 캡션: *"(a) LCO(104)/LPS(010) and (b) LCO(110)/LPS(010)"*. 구조·인셋·`Fig. S1` 대조 결과 **그림 안 라벨이 맞다.** 캡션만 보고 인용하면 **면방위가 뒤집힌다.**

③ 🔴 **표본 개수가 본문 ↔ 그림 캡션에서 *두 번* 정반대다.**
· **LPS**: 본문 §3.1 *"three and eight … for (104) and (110)"* ↔ `Fig. 4` 캡션 *"65 sites in **8** … (23 sites in **three** …) for (104) and ((110))"* ↔ SI §S3 *"**8 and 4** slab models for (104) and (110)"*. **세 진술이 서로 다르다.**
· **LPO**: 본문 §3.2 *"**five and four** … for (010) and (001)"* ↔ `Fig. 8` 캡션 *"28 sites in **four** … and 36 sites in **five** … for (010) and (001)"*. **반대.**
*우리 산수* 로 막대 높이를 자리수로 환산하면 **캡션 쪽이 맞다**(65/23/28/36 전부 정확히 떨어진다). ⇒ **본문 문장이 틀렸다.** 결론이 걸린 **LCO(110)/LPS 의 실제 표본은 3구조 23자리**로 **8계면 중 가장 적다.**

④ 🔴 **면방위 비교가 서로 다른 k-격자에서 이뤄졌다.**
*"we set **2 × 1 × 1** for LCO(110)/LPS(010) … and for **other interface models, we set only the Γ-point**."* ⇒ **LCO(104)/LPS 는 Γ-only, LCO(110)/LPS 는 2×1×1.** 이 논문의 핵심 결론 중 하나인 **(104) vs (110) 비교가 k-수렴이 통제되지 않은 상태**에서 나왔다. 게다가 두 번째 2×1×1 대상으로 적힌 **"LCO(110)/LPO(001)" 은 이 논문에 존재하지 않는 계면**이다(LPO(010) 오기). **k-수렴 시험은 제시되지 않는다.**

⑤ 🔴 **요약이 VBO 단일 기전을 주장하는데, 자기 숫자가 단조가 아니다.**
저(低)E_f 자리 비율 **LPS 18–30 % > LLZO 6 % > LPO 0–3 %** 인데, 보고된 VBO 는 **LLZO 0.2 eV** 가 **LPS(`figure-read` 0.1–0.5 eV)** 와 같거나 작다. ⇒ **VBO 만으로는 LPS↔LLZO 순서가 안 나온다.** 음이온 화학(S vs O) 기여를 분리하지 않았다. (본문 §3.3 은 *"smaller offset … allows easier electron transfer"* 로 LLZO 를 **나쁜 쪽**으로 설명하는데, 분포는 LLZO 를 **LPS 보다 훨씬 좋게** 만든다.)

⑥ 🔴 **구조 표본 산포가 W_ad 보다 크다 — 그런데 W_ad 는 최저구조 1개 값이다.**
*우리 산수*: ΔE/S ÷ W_ad = **LCO(104)/LPS 21 % · LCO(104)/LPO(010) 82 % · LCO(104)/LPO(001) 495 %**. 마지막 경우 **최고에너지 구조를 골랐다면 W_ad 가 음수(−0.083 eV/Å²)** 가 된다. ⇒ **이 논문의 W_ad 는 계면의 성질이 아니라 구조 선택의 성질이다.** E_f 는 분포로 보고하면서 **W_ad 만 최저구조 스칼라**로 준 것이 비일관적이다.

⑦ ⚠ **중갭 상태를 "계면" 탓으로 돌리는데, 그림은 "진공면" 기여가 더 크다고 말한다.**
`Fig. 3` +2.85 eV 봉우리: **갈색 LCO vac `figure-read ≈ 90` vs 하늘색 LCO 1st ≈ 35**. `Fig. 7` +0.95 eV 봉우리: **진한 빨강 LCO_vac ≈ 100 vs 하늘색 LCO_1st ≈ 40**. 본문은 두 경우 모두 *"in-gap state … of CoO₅ quadrangular cones **at the interface**"* 라 쓴다. 게다가 `Fig. 11`(LLZO)에서는 **LCO vac 곡선이 거의 0** 이어서 **세 PDOS 그림의 규격이 서로 다르다.** ⇒ **자유표면 상태와 계면 상태가 섞여 있을 가능성**이 남고, 저자는 그 구분을 논하지 않는다. (우리에게 직접 해당 — §8-④)

⑧ ⚠ **무질서 처리가 두 군데서 무너진다.**
· **β-Li₃PS₄**: Li 부분점유를 어떻게 처리했는지 **한 줄도 없다**. [Haru14] 는 Lepley `β-Li₃PS₄-b` 를 명시했는데 본 편은 뺐고, **격자상수마저 [Haru14] 와 1–2 % 다르다** ⇒ **다른 배열을 쓴 것으로 보이나 확인 불가.**
· **LLZO**: *"50 % / 40 % 공공"* 을 그대로 풀면 점유 Li 이 **62.4개(비정수)** 가 되어 **192원자 셀(Li 56)과 안 맞는다.** SQS·enumerate·앙상블은 **전부 0회**.

⑨ ⚠ **SI 에 복붙 오류가 다섯 건 이상이다.**
(a) *"506 + 192 = 696"* (504 여야 맞다) · (b) *"480 + 256 = **756**"* (**736** 이 맞다) · (c) **LCO(110) 단위셀 첫 수 `2.815`** (**4.910** 이어야 misfit 4.6 % 가 나온다 — *우리 산수* §3b-4) · (d) LTO/LPS 절에 *"misfit parameter of **LCO(104)/LTO(111)** is 4.9 %"* (해당 계면이 아니다) · (e) LTO/LPS 절에 *"lattice constant of LPS is set to that of **LCO**"* (그 계면에 LCO 가 없다) · (f) LCO/LTO 절에 *"repeated number of **LTO and LPS** units"* (LCO and LTO 여야 한다) · (g) LCO(104) 단위 원자수가 **18** 과 **16** 두 값으로 쓰인다 (*우리 산수*: LPS/LPO 계면은 **9층 504원자**, LLZO/LTO 계면은 **8층 256원자**라 **둘 다 "단위" 정의가 슬랩과 정확히 안 맞는 것**이 원인) · (h) *"ZrO₆ **tetrahedrons**"* (팔면체다).

⑩ ⚠ **다른 논문의 값과 직접 비교해 결론을 내는데, U 가 다르고 숫자마저 반대다.**
*"LNO 버퍼가 LTO 보다 우수하다"* 는 [Haru14](**U=5.9 eV**)의 LNO/LPS 값을 본 편(**U=4.9 eV**)의 LTO/LPS 와 직접 비교해 얻은 결론이다. ***우리 산수***: LPS 쪽 평균 **LNO 2.95 vs LTO 2.994**, 최소 **LNO 2.42 vs LTO 2.95** ⇒ **두 지표 모두 LTO 가 더 좋다.** 결론이 자기 인용값과 **반대**다.

⑪ ⚠ **수렴·이완 조건이 통째로 없다.** 힘·응력·에너지 수렴 기준 0건, 이완 자유도 0건, 벌크·표면 k 0건, PDOS nscf 조건 0건, QE 버전 0건. **[Haru14] 가 전부 적었던 것을 이 논문은 안 적는다** — **6년 뒤에 더 불투명해졌다.**

⑫ ⚠ **재현이 불가능하다.** 좌표 파일 없음 · **원시 총에너지 없음** · 히스토그램 원자료 없음(정규화 막대만). [Haru17] 은 `Table S3` 로 벌크 결함 총에너지를 Ry 로 공개해 우리가 검산할 수 있었는데, **본 편에는 그런 자료가 하나도 없다.** (§3b-4 에서 한 것은 **misfit 역검산으로 셀을 복원한 것**이지 에너지 재현이 아니다.)

⑬ ⚠ **`E_f` 는 순수한 이온 항이 아니다.** 중성 셀이라 **빠진 전자가 어디 앉느냐가 값을 정한다** — 저자 자신이 LPO·LTO·LLZO 에서 그것을 보인다(벌크 5.1 → 계면 2.4–3.1 은 **구조가 아니라 밴드정렬**). ⇒ **"SE 쪽 E_f 가 낮다" 를 "그 SE 가 불안정하다" 로 읽으면 틀린다.** 버퍼 쪽 낙폭(−1.3 ~ −1.7 eV)은 **SCL 이 아니다.**

⑭ ⚠ **반응 동역학이 없다.** *"the full evaluation of the exchange probability requires a consideration of the reaction kinetics"* — 저자가 직접 단 단서. **배리어 0개**이므로 *"반응층이 형성된다"* 는 **열역학적 선호**까지만이다.

⑮ ⚠ **실험 대조 0회.** 실험 수치는 전부 타 문헌 인용(Haruta 2015 LiPON, Kawasoko 2018 **7.6 Ω cm²**, Sharafi 2017 LLZO). **이 논문이 계산한 것과 그 실험값을 잇는 정량 고리는 없다** — *"can be associated with"* 수준의 서술만 있다.

---

## 11. 🔻 불리한 결론 — 따로 적는다 (임무 ⑥)

> 사용자 요청대로, **우리에게 유리하지 않은 것**만 모았다.

**① 🔴🔴 우리가 6개월간 실어 온 `W_ad(황화물) = 0.8 J/m²` 각주는 *원전에 없는 수*다.**
· Barai 2021 `Fig. 11` 의 황화물 안정한계선 0.8 J/m² 는 **ref 69 ([Haru14]) + ref 70 (본 편)** 에 귀속돼 있다.
· **[Okuno20] 에는 0.8 이 없다** — 황화물 계면 값은 **0.400 J/m² 하나**이고 **0.8 의 정확히 절반**이다. 게다가 **Barai 가 지목한 Li₃PS₄ 계면(ref 69 = LCO(110)/LPS)의 W_ad 는 [Okuno20] 에 아예 없다.**
· **[Haru14] 에도 0.8 이 없다** — **0.689 J/m²** 다.
⇒ **0.8 은 Barai 가 만든 수이고, 두 원전 중 어느 쪽도 그 값을 담고 있지 않다.** 우리 `INDEX.md` 의 barai 행과 barai digest §7c·§9 가 **"refs 69, 70" 을 근거로 0.8 을 쓰고 있으므로, 그 문장은 "Barai 2021 이 채택한 값" 으로 **재귀속**해야 한다.
⇒ 그리고 **Nd 인산염 W_ad 를 0.8 과 비교하려던 계획**(barai digest §7c: *"√(2.0/0.8) = 1.58"*)은 **분모가 문헌값이 아니므로 다시 세워야 한다.** 분모 후보를 0.400(Okuno (104))로 바꾸면 √(2.0/0.400) = **2.24** 로 결론의 크기가 **41 % 커진다** — 즉 **우리 결론이 분모 선택에 민감하다.**

**② 🔴 우리 W_ad 비율 해석(`refs.json`)이 방법을 통제하지 않았다 — 이제 그게 확정됐다.**
`db/literature/refs.json` 의 haruyama2014 항목은 *"Our … **1.28 J/m² is ~2× their 0.69**. Reasonable: **LiNiO₂ more reactive than LCO** per Komatsu"* 라고 **물질 차이로 귀속**한다. 그런데 **[Okuno20] 이 같은 방법·같은 그룹으로 낸 값이 0.400** 이다.
⇒ **문헌 내부에서만 0.400 ↔ 0.689 로 1.72배가 갈린다** (면방위 + U 5.9→4.9 + 무질서 배열). **우리 비율 1.86× 중 대부분이 그 산포 안에 들어간다.** ⇒ **"Ni 가 Co 보다 반응성이 커서" 라는 귀속은 근거가 없다.** (병합대기 ④ 에 정정 문구를 넣었다 — 나는 직접 안 고쳤다.)

**③ 🔴 우리 v5 의 면지수 미기재가 이제 *정량적으로* 문제가 된다.**
이 논문은 **같은 물질쌍에서 면방위 하나로** 저E_f 자리 비율 **18.5 → 30.4 %**, Co↔P 교환에너지 **−1.25 → −2 eV** 가 갈린다는 것을 보인다. **우리 v5 보고서에는 NCM 면지수가 없다.** ⇒ *"우리 계면은 Haruyama/Okuno 프로토콜을 따랐다"* 라고 쓸 수 있는 범위는 **기하 형식(단일계면+진공, W_ad 식, 횡방향 registry 탐색)까지**이고, **면·종단·수렴은 "따랐다" 고 말할 근거가 없다.**

**④ 🔴 우리 v5 의 "진공 30 Å + FixAtoms 33 %" 는 이 계열 문헌 어디에도 근거가 없다.**
· 진공: [Haru14] 15 Å, [Okuno20] **10–15 Å** — **우리 30 Å 은 문헌의 2–3배**이고, 그 이유는 물리가 아니라 **UMA 의 분포 밖 거동**(60 Å 에서 24.5 J/m²)이다. **MLIP 의 병리를 피하려고 잡은 값**을 DFT 문헌 프로토콜의 계승으로 서술하면 안 된다.
· FixAtoms 33 %: **[Okuno20] 은 이완 자유도를 아예 안 적었고, [Haru14] 는 "전원자 자유" 를 명시했다.** ⇒ **우리 구속은 문헌 대비 *추가 제약*이고, 그것이 W_ad 를 올리는 방향인지 내리는 방향인지 우리는 시험한 적이 없다.**

**⑤ 🔴 이 논문의 중심 서사는 "황화물이 나쁘다" 이고, 그것은 우리 축에 불리하다.**
초록·요약이 말하는 것은 *"산화물 SE 가 Li 고갈도 적고 반응층도 덜 만든다"* 이다. 우리는 **황화물(아지로다이트) 캠페인**이다. ⇒ **이 논문을 우리 서사의 지지 근거로 쓸 수 없다.** 쓸 수 있는 것은 ⓐ **방법 원전**(§7c) ⓑ **버퍼/코팅이 황화물을 구제한다는 부분**(§3f) ⓒ **면방위 제어가 레버라는 부분**(§3h) 셋이고, ⓑ·ⓒ 는 **우리가 아직 계산한 적 없는 축**이다.

**⑥ ⚠ "Cl-rich 가 계면에 유리하다" 를 이 논문으로 받칠 수 없다.**
이 논문에 **Cl 은 한 번도 안 나온다**(아지로다이트 언급은 마지막 문단의 전망 한 줄 — *"more complicated interfaces such as **Li₆PS₅Cl/Li₂S**"*, ref 61 Yu 2016 — 이 전부다). ⇒ **조성축(할로겐 함량)은 이 논문의 공백이고, 동시에 우리 공백이기도 하다** — 우리도 계면 E_f·교환에너지를 조성별로 낸 적이 없다.

---

## 12. 관련 연구 — **Tateyama 그룹 3부작 + 인용 사슬**

| 축 | **[Haru14]** (2014) | **[Haru17]** (2017) | **[Okuno20]** (본 편, 2020) |
|---|---|---|---|
| **저널** | *Chem. Mater.* 26, 4248 | *ACS AMI* 9, 286 | *ACS AEM* 3, 11061 |
| **1저자 소속** | NIMS | NIMS | **FUJIFILM (산업계)** |
| **계면** | LCO(110)\|LNO ×2, LCO(110)\|LPS, LNO\|LPS (**4종**) | 그 중 **3종 계승** | **8종** (LCO 2면 × LPS/LPO/LLZO + LTO 2종) |
| **질문** | "Li 이 어디 앉나 → SCL" | "Co 가 어디로 가나" | **"황화물 vs 산화물 + 면방위"** |
| **보고량** | E_v (자리별, **최저구조 1개**) + W_ad + W_surf + PDOS | E_ex + PDOS + 교환후 E_v | ⭐ **E_f 분포(271자리)** + E_ex + PDOS + W_ad 4개 |
| **U(Co 3d)** | **5.9 eV** | **5.9 eV** | 🔴 **4.9 eV** |
| **스미어링** | 0.001 Ry | **0.01 Ry** | 0.001 Ry |
| **k (계면)** | Γ-only 전부 | Γ-only 전부 | **Γ 또는 2×1×1 (혼합)** |
| **횡방향 탐색** | **계통적 격자 16/4/9** | 계승 | 🔴 **무작위 3–8** |
| **무질서(LPS)** | **Lepley β-Li₃PS₄-b 명시** | 계승 | 🔴 **미기재 · 격자도 다름** |
| **nat 공개** | ⛔ 없음 | ⛔ 없음 | ✅ **8계면 전부** |
| **원시 에너지** | ⛔ 없음 | ✅ `Table S3` | ⛔ 없음 |
| **수렴기준** | ✅ 힘 0.001 Ry/bohr, 응력 0.5 kbar | ✅ 동일 | ⛔ **없음** |
| **핵심 수** | LP2 **1.44 eV** · W_ad **10.6/6.1/4.3/3.8 eV/nm²** | Co↔P **−2.18 eV**(계면) vs **+1.98**(벌크) | **E_f<2.0 비율 30.4/18.5/6.2/2.8/0 %** · W_ad **0.025/0.028/0.021/0.019 eV/Å²** |

**요약 한 줄**: **2014 가 무대를 만들고, 2017 이 두 번째 배우를 올렸고, 2020 이 그 무대를 *여러 세트로 복제해 통계를 냈다* — 대신 무대 도면(수렴·이완·무질서)을 지웠다.**

**인용 사슬 (우리 repo 기준)**
- **위로**: ref 21 = [Haru14] (`papers/haruyama2014_…`) · ref 22 = [Haru17] (`papers/haruyama2017_…`) · ref 24 = **[Gao20]** Gao·Jalem·Ma·Tateyama, *Chem. Mater.* **32**, 85 (2020) — **계면 구조예측 자동화**, 본 편이 *"a comprehensive structure search technique"* 로 인정하면서 안 쓴 방법 (**확보 후보 1순위**) · ref 23 = Tateyama 그룹 *Curr. Opin. Electrochem.* **17**, 149 (2019) 리뷰.
- **옆으로**: ref 30 = **Richards & Ceder 2016** (열역학 계면 안정성 — 우리 grand-potential 계보) · ref 28/29 = **Zhu, He, Mo 2015/2016** (ESW 원전) · ref 31 = **Deng & Ong 2017** · ref 60/S8 = **Butler, Sai Gautam, Canepa 2019** (W_ad 정의 원전 — ⭐ `papers/wang2022_resistive_decomposing_interfaces_se_alkali_metal.md` 의 Canepa 그룹과 **같은 계보**).
- **아래로**: **Barai 2021** (`papers/barai2021_delamination_cathode_llzo_multiscale.md`) 이 ref 70 으로 인용해 **Ψ_t ≈ 0.8 J/m²** 를 만든다 — **§11-① 의 대상**.
- **우리 litdb 안의 이웃**: `haruyama2014_…` (기하 원전) · `haruyama2017_…` (양이온 혼합) · `barai2021_…` (0.8 의 소비처) · `wang2022_…` (음극측 접합일, **같은 W_ad 정의 계보 · ⛔ 같은 표 금지**) · `ncube2026_ionic_interdiffusion_lco_lgps_multiscale` · `zuo2022_chlorination_cathode_interface`.

---

## 13. 기술 미니 용어집 (이 digest 를 혼자 읽기 위한)

- **Li 공공 형성에너지 `E_f(V_Li_j)`** — Li 원자 하나를 j 번째 자리에서 빼서 **bcc Li 금속**에 얹는 비용. 기준이 Li 금속이라 **eV 값이 곧 Li/Li⁺ 기준 전압(V)**. 낮은 자리 = **낮은 전압에서 먼저 Li 을 내놓는 자리**. ⚠ **중성 셀**이므로 **빠진 전자가 앉는 곳(밴드정렬)이 값의 큰 몫을 차지한다** — 순수 이온 항이 아니다.
- **동적 Li⁺ 고갈 (dynamical Li⁺ depletion)** — 이 그룹이 **고전적 SCL 과 구별해 쓰는 말**. 평형 이온 재분배가 아니라, **충전 초기에 낮은 E_f 자리의 Li 이 *전자 산화와 함께* 빠져나가며** 생기는 고갈층. 원문: *"this dynamical Li⁺ depletion is **different than the conventional static SCL formation mechanism**."*
- **상호 양이온 교환에너지 `E_ex`** — `E_tot(A_j ↔ B_k) − E_tot`. **조성 보존 in-place 스왑**이라 화학퍼텐셜 기준이 필요 없다. **음수 = 섞이는 게 유리.** ⚠ **동역학(배리어)은 포함 안 된다.**
- **부착에너지 `W_ad`** — 계면을 뜯어 두 자유표면을 만드는 비용/면적. `(E_A + E_B − E_AB)/S`. 분모가 **S**(단일 계면)이지 2S 가 아니다. ⚠ **두 슬랩이 변형된 채 계면을 이루면 변형에너지가 섞일 수 있다** (이 논문은 그 처리를 안 밝힌다).
- **미스핏 파라미터 μ** — **면적 중첩** 정의 `1 − 2S_A∩B/(S_A+S_B)`. **선형 변형률(%)과 다른 양**이다. (*우리 산수* 로 이 정의를 써서 SI 의 셀 오식을 잡아냈다 — §3b-4.)
- **가전자대 오프셋 (VBO)** — 두 물질의 VBM 이 계면에서 얼마나 어긋나 있는가. **SE 의 VBM 이 양극보다 훨씬 아래면** SE 에서 양극으로 전자가 못 넘어가고 ⇒ **SE 산화·Li 고갈이 억제**된다. 이 논문의 중심 기전.
- **중갭 상태 (in-gap state)** — 밴드갭 안에 생긴 국소 준위. 여기선 **배위가 덜 찬 계면/표면 Co 의 3d 준위**. ⚠ **계면에서 왔는지 자유표면에서 왔는지 층별 투영으로 갈라야 한다** (§10-⑦).
- **CoO₅S 팔면체 / CoO₅ 사각뿔 / CoO₄S 오면체** — LCO 표면을 어떻게 자르느냐에 따라 최외곽 Co 의 배위가 달라진다. **(104) 는 CoO₅S + CoO₅ 사각뿔**, **(110) 은 CoO₄ 유사사면체 + CoO₄S**. **사각뿔(배위 5, S 없음)이 중갭 상태를 만들고 양이온 교환도 가장 잘 한다.**
- **DFT+U** — PBE 가 3d 전자를 과도하게 퍼뜨리는 것을 Hubbard U 로 교정. 여기선 **Co 3d 에 4.9 eV**(ref Zhou/Ceder 2004). **Ti·Zr·La 에는 안 걸었다.** ⚠ [Haru14]·[Haru17] 은 **5.9 eV** 였다.
- **β-Li₃PS₄ / γ-Li₃PO₄ / LLZO / LTO** — 순서대로 황화물 SE(Pnma, b 방향 Li 전도) · 산화물 SE(Pnma, LiPON 의 모체) · 가넷 산화물 SE(Ia3̄d, 산화물 중 최고속) · 스피넬 버퍼(Fd3̄m, (111) 로 Li 이 지난다).
- **`figure-read ≈`** — **그림에서만 읽은 값**이라는 우리 관례 표기. 본문에 활자로 있는 값과 구분한다. (이 digest 에서는 `Fig. 4`·`Fig. 8` 의 막대를 자리수로 환산해 **캡션의 65/23/28/36 과 정확히 일치**시켜 읽기 정확도를 자체 검증했다.)

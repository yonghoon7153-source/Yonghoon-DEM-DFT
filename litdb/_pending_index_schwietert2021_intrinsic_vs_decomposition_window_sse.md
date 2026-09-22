# 병합 대기 — `schwietert2021_intrinsic_vs_decomposition_window_sse`

> 2026-09-22 litdb-curator 작성. **나는 `litdb/papers/<slug>.md` 와 이 파일만 썼다.**
> `INDEX.md` · `comparison_vs_ours.md` · `db/literature/refs.json` · `db/` · `kb/` **미수정, 커밋 없음** (다른 에이전트 병합 중).
> 그림은 `litdb/figures/schwietert2021_intrinsic_vs_decomposition_window_sse/` 에 **이미 만들어져 있다**(29장, sources 정상). **재생성 금지.**
>
> **§J 번호 확인 실측 (2026-09-22)**: `comparison_vs_ours.md` 의 최대 번호는 **J-36**(J-33 morgan2021 · J-34 haruyama2014 · J-35 okuno2020 · J-36 wang2022)이다. ⇒ 아래 블록은 **§J-37** 로 제안한다. 병합 시점에 J-37 이 이미 차 있으면 **다음 빈 번호로 옮기되, digest 본문의 §J 참조는 없다**(digest 는 §B①/§E 만 가리킨다).

---

## ① `INDEX.md` 행 (제안)

| `papers/schwietert2021_intrinsic_vs_decomposition_window_sse.md` **(본문 9 pp · SI 11 pp · 크로핑 29장 = 그림 14 + 표 15 · 그림 8장 실독)** | **[외부·🔴🔴 `[Zhu15]` 3.4× 감사의 열쇠 · `[Schw20]` 의 직계 후속 · 아지로다이트 포함]** **Tammo K. Schwietert**/Alexandros Vasileiadis/**Marnix Wagemaker\*** (**TU Delft** Storage of Electrochemical Energy — `[Schw20]` 과 같은 그룹·같은 과제 NWO VICI 16122), "**First-Principles Prediction of the Electrochemical Stability and Reaction Mechanisms of Solid-State Electrolytes**" (***JACS Au* 1(9), 1488–1496 (2021)**, DOI `10.1021/jacsau.1c00228` · 접수 2021-05-22 / 게재 2021-08-16 · **오픈액세스** · ⛔ **데이터 리포지터리 없음, Data availability 절 자체가 없다**) — ✅ **서지 PDF 직독 확인**. `[Dutra25Rev]` **ref 218** 의 원전. **★★★ 기여 = 창에 이름을 붙이고 12종으로 확장**: **decomposition window**(Li grand potential 상도 · 분해산물 기준 = `[Zhu15]` 계열 = `[Xiao20Rev]` **층①**) ↔ **intrinsic window**(SE 자신의 (탈)리튬화 평균전압 = **층②**). **`Table 2` 전수**(환원/산화 V): `Li₃PS₄` **1.72/2.30 → 1.24/2.47** · `Li₆PS₅Br` **1.72/2.01 → 1.09/2.23** · **`Li₆PS₅Cl` 1.72/2.01 → 1.11/2.19** · `Li₁₀GeP₂S₁₂` 1.63/2.14 → 1.19/2.38 · `LiBH₄` 0.54/2.10 → 0/3.43 · `Li₃YBr₆` 0.67/3.06 → 0/3.43 · `Li₃OCl` 0/2.68 → 0/3.17 · `Li₂PO₂N` 0.68/2.64 → **0/4.12** · `LLZO` 0.05/2.68 → **0/3.61** · **`LLTO` 1.71/3.36 → 2.10/3.68(좁아짐)** · **`LATP` 2.17/3.86 → 2.74/3.77(좁아짐)** · `LAGP` 2.71/3.98 → 2.31/4.30. **🔴🔴 우리 감사에 대한 답**: `Table 2` 캡션이 *"Values in Agreement with the Calculations in Literature⁸"*(ref 8 = **`[Zhu15]`**)라고 못박아 **`Li₆PS₅Cl` 0.29 V 를 독립 재현**한다 ⇒ **3.4× 는 저쪽 전사 오류가 아니다.** 창 정의도 **같은 양**이다(*"Li **grand potential** phase diagram"* · *"**the decomposition potential closest to the stable solid electrolyte phase** defines the reduction and oxidation redox potentials"* · 조성 = `Li₆PS₅Cl` 행, `Li₃PS₄` 는 별도 행). ⇒ **저들 정의로 우리 프로파일을 다시 읽으면 `1.717–2.256 = 0.539 V`** 이고, 우리가 "환원 한계" 라 불러 온 **1.242 V 는 *두 번째* 환원 평탄(P → `LiP₇`)**, 진짜 환원 가장자리는 우리가 "OCV" 라 부르던 **1.717 V**(저들 **1.72** 와 **0.003 V**) 다. **⇒ 3.4× 중 0.475 V(66 %)가 우리 라벨 오류이고, 남는 진짜 격차는 산화 한 변 +0.246 V 뿐이다**(그 중 0.116 V 는 우리 `LiS₄` 배제 몫 — `our_dft_baseline.md` L19 *"LiS₄ 포함 시 2.14"*). **근거 3개(우리 유도)**: ① 우리 프로파일의 완전환원(`+8 Li → Li₃P+5Li₂S+LiCl`)이 정확히 **0.000 V = Li 금속 전위** ⇒ 행의 전압은 그 조성의 *Li-rich 쪽* 평탄이다 ② `Table 2` 의 환원한계가 `Li₃PS₄`·`Li₆PS₅Br`·`Li₆PS₅Cl` **셋 다 1.72** — 셋의 Li-보존 평형이 전부 `Li₃PS₄` 를 품기 때문이고, **우리 1.717 V 행의 평형이 바로 `Li₃PS₄+Li₂S+LiCl`** 이다 ③ `Table 1` LPSC 환원용량 **798.85 mAh/g = 8.00 Li**(우리 산수) = **우리 0 V 단계의 8 Li** ⇒ 최종 환원산물 상집합 일치. **⚠ 위험한 우연**: 저들 **층② 폭이 1.08 V** 라 우리 오표기 1.014 V 와 0.07 V 차 — ⛔ *"우리 hull 이 간접 경로를 이미 머금었다"* 로 읽으면 안 된다. **새 기여 = hull 모양이 창 밖의 운명을 가른다**(`Fig. S8`·`Fig. 3b,c`): **V자 hull = 상분리 → 준안정 중간상 경유**(LGPS·LAGP) / **볼록 hull = 고용체 → 중간상 없음, 끝을 정하는 것은 분해전압**(LATP·LLTO). **⭐ 활자 소득 2개**: *"for complex solid electrolytes, it is expected that **the direct decomposition stability window is a lower limit**"*(우리 worst-case 하한 프레이밍의 가장 직접적 외부 근거 — **단 그 하한은 저들 기준 2.01 V 이지 우리 2.256 V 가 아니다**) · *"CV experiments ... performed **without conductive additive** ... and are thus **unable to capture the intrinsic electrochemical window**"*(`[Du22LMR]`·`[Zuo]` CV onset 인용 시 필수 단서). **`Table S4`(우리 계, 소환값)**: `Li₆PS₅Cl` V **965.21 Å³**(a 9.882 Å, 우리 산수)·gap **1.984 eV**(⛔ **DOS 판독**)·σ **95.78 S/m@600 K** → 탈리튬 `Li₄PS₅Cl` 935.80(a −1.03 %)·**2.391**(↑)·43.83(−54 %) → 리튬화 `Li₁₁PS₅Cl` 1168.50(a +6.6 %)·**1.219**(↓)·59.53(−38 %) ⇒ **`[Schw20]` 의 DFT 격자(−1.0 % / +6.6 %)·XRD(−1.09 %)와 같은 계산**. **DFT**: VASP·PBE(⚠ ref 13 이 PBE 가 아니라 Perdew–Burke–**Wang** PRB 54, 16533 — `[Schw20]` 과 **같은 오기**; ref 14 도 PAW 논문이 아니라 Kresse–Hafner 1993)·전하중성·0 K·**U 없음**·vdW 없음·스핀 미언급; Li 배열 **랜덤 1만 → 정전기 선별 → 최저 10개만 DFT**(⚠ `[Schw20]` 은 20개였다); 참조에너지 **MP(판본 미기재)**; AIMD 는 **σ 전용**(해석 = de Klerk 2018). 🔴 **재현 불가 3건**: **ecut 이 없다**(본문은 `Table S1` 에 있다고 쓰는데 **cutoff 열 자체가 없다**) · **`Li₆PS₅Cl`·LLZO·LAGP 는 k-점·슈퍼셀이 "−"** · **무질서 처리가 한 줄도 없다**(`[Schw20]` 은 단언이라도 했다). 🔴 **비판**: ① **중심 가정(핵생성 장벽)이 또 측정 안 됨** — NEB 0·전이상태 0·eV 0, `Fig. 3b` 는 눈금 없는 손그림, `Fig. S8` 흐름도에 장벽 상자 없음 ② **"복잡할수록 장벽이 크다" 에 지표가 없다**(원소 수뿐이고 LYB 가 반례) ③ **Ti⁴⁺→Ti³⁺ 를 U 없이** — LLTO·LATP 결론 전체가 여기 걸려 있다 ④ **"12종에서 실험과 훌륭히 일치" 의 실제 크기 = 정량 대조 7종·실패 1종(LYB, 저자 자인)·대조 없음 1종(LOC)** ⑤ **intrinsic 값이 셀 크기의 함수라고 저자가 직접 쓴다**(*"artificially defined by the smallest composition step of the supercell"*, 수렴시험 0) ⑥ **방향 라벨이 논문 안에서 뒤집힌다** — `Table 2` 머리글 "ox/red" 가 값(red−ox)과 반대, 본문 LLZO 를 *"oxidation and reduction ... 0.05 and 2.68 V"* 로 **거꾸로** 씀 ⑦ SI 라벨 오류 8건(`Fig. S2` 캡션 Cl ↔ 축 Br · `S7` 캡션이 `S6` 복붙인데 실제는 LLTO · `Table S4` 캡션 Br/Cl · `Table S6`·`S10` 의 (탈)리튬화 조성이 pristine 과 동일 · `Table S11` 행 순서 · `Li₃YB₆` 오타 · `Figure 11`) ⑧ **AIMD σ 온도가 600 K 과 1000 K 로 갈리는데 단서 없음** ⑨ **`Table 1` LPS 산화용량 96.23 = LAGP 값과 동일 = 오류 후보**(3 Li 면 ≈447 mAh/g, 우리 산수) ⑩ **자기 값 변경을 안 알린다**(LPSC 층② 가 `[Schw20]` 2.24/1.08 → 2.19/1.11 ⇒ **층② 재현성 ≈0.05 V**). **그림 14장 중 8장 실독**(`Fig. 1`·`2`·`3`·`S2`·`S7`·`S8`·`S9`·`S11`), **미열람 6장**(`S1`·`S3`·`S4`·`S5`·`S6`·`S10` — 전부 우리 물질계 밖), 표 15장은 PDF 텍스트로. | **🔴 §B①(산화 onset)·§E(환원) 본표 편입 + §J-37(창 정의·감사)** |

---

## ② `Reference key` 행 (제안 — `comparison_vs_ours.md` §📑 Reference key 표)

| **[Schw21]** ⭐⭐⭐ **`[Zhu15]` 3.4× 감사의 열쇠 — 창 정의를 활자로 준 편** · **[Schw20] 의 직계 후속(= 그 논문의 ref 7 관계가 역방향)** · ⭐ **`[Dutra25Rev]` ref 218 의 원전** | **Tammo K. Schwietert**/**Alexandros Vasileiadis**/**Marnix Wagemaker\*** (전원 **TU Delft**, Storage of Electrochemical Energy, Dept. Radiation Science and Technology) 2021 ***JACS Au* 1(9), 1488–1496** (DOI `10.1021/jacsau.1c00228`; 접수 2021-05-22 / 게재 2021-08-16; OA; NWO **VICI 16122** + eScience **680.91.087** = `[Schw20]` 과 동일 과제; 본문 9 pp · SI 11 pp · `Fig. 1`–`3` + `Fig. S1`–`S10`+`S11` · `Table 1`–`2` + `Table S1`–`S13` · refs 39) — "**First-Principles Prediction of the Electrochemical Stability and Reaction Mechanisms of Solid-State Electrolytes**". **SE 12종**(`Li₃PS₄`·`Li₆PS₅Br`·**`Li₆PS₅Cl`**·`Li₁₀GeP₂S₁₂`·`LiBH₄`·`Li₃YBr₆`·`Li₃OCl`·`Li₂PO₂N`·`LLZO`·`LLTO`·`LATP`·`LAGP`)에 **두 창**을 같은 틀로 계산: **decomposition window**(= 층①, `[Zhu15]` 계열 재현) ↔ **intrinsic window**(= 층②, Aydinol 평균 (탈)리튬화 전압). **`Li₆PS₅Cl` = 1.72–2.01 V ↔ 1.11–2.19 V.** 🔑 **우리 감사에 대한 답**: 저들 정의(*"the decomposition potential **closest to the stable solid electrolyte phase**"*)로 **우리 프로파일을 다시 읽으면 1.717–2.256 V(0.539 V)** 이고 **환원 가장자리가 저들 1.72 와 0.003 V 차** ⇒ **3.4× 의 66 %가 우리 `reduction_V` 라벨 오류**, 남는 것은 **산화 한 변 +0.246 V**. **새 기여** = hull 모양 분기(**V자=상분리 / 볼록=고용체**)와 **intrinsic 이 더 *좁은* 계 2종(LLTO·LATP)**. ⛔ **자체 실험 0 · NEB 0 · 핵생성 장벽 수치 0 · U 0 · 무질서 처리 미기재 · ecut 미기재 · MP 판본 미기재 · 데이터 공개 0** | ✅ `papers/schwietert2021_intrinsic_vs_decomposition_window_sse.md` | DFT(VASP-PBE) 전용 + AIMD(σ 전용) · 실험 0 (전 대조가 문헌 소환값) |

---

## ③ `comparison_vs_ours.md` 블록 (제안)

### ③-1. **§B①** 에 추가할 행 2개 (산화안정성 4축 표)

| **B① 🔴🔴 🆕 감사 종결 후보 — `[Zhu15]` 3.4× 의 **2/3 은 우리 라벨 오류였다** (2026-09-22 신설)** | (우위 아님 — **우리 쪽 정정**) | **[Schw21]** `Table 2` + 정의 활자. *"Li **grand potential** phase diagram"* · *"**The decomposition potential closest to the stable solid electrolyte phase** defines the reduction and oxidation redox potentials of the window"* · 조성 = **`Li₆PS₅Cl`** 행. 캡션이 *"Values in Agreement with the Calculations in Literature⁸"*(ref 8 = **`[Zhu15]`**) ⇒ **0.29 V 가 2021 년에 독립 재현됐다 — 전사 오류가 아니다** | 🔴 **저들 정의로 우리 `esw_lis4excluded.json` 프로파일을 다시 읽으면**(우리 유도): **Li 교환 0 구간 = [1.717, 2.256] V = 0.539 V**. 우리가 "환원 한계" 라 인쇄해 온 **1.242 V 는 *두 번째* 환원 평탄(P → `LiP₇`)** 이고, 진짜 가장자리는 우리가 "OCV" 라 부르던 **1.717 V** 다 — 저들 **1.72 V** 와 **0.003 V**. ⇒ **격차 0.724 V 중 0.475 V(66 %) = 우리 라벨**, 남는 것은 **산화 한 변 +0.246 V**(2.256 ↔ 2.01), 그 중 **0.116 V 는 우리 `LiS₄` 배제 몫**(`our_dft_baseline.md` L19). **근거 3개**: ① 우리 완전환원(`+8 Li → Li₃P+5Li₂S+LiCl`)이 **정확히 0.000 V = Li 금속 전위** ⇒ 행 전압 = 그 조성의 *Li-rich 쪽* 평탄 ② `Table 2` 환원한계가 `Li₃PS₄`·`Li₆PS₅Br`·`Li₆PS₅Cl` **셋 다 1.72**(= 셋 다 Li-보존 평형에 `Li₃PS₄` 를 품는다) 이고 **우리 1.717 V 행의 평형이 바로 `Li₃PS₄+Li₂S+LiCl`** ③ `Table 1` LPSC 환원용량 **798.85 mAh/g = 8.00 Li**(우리 산수) = 우리 0 V 단계의 8 Li. ⛔ **미검증 1건**: pymatgen 재실행 대조는 아직 안 했다 — **재실행 전까지 "1.717 V 가 우리 환원 한계" 를 원고에 인쇄하지 않는다**. 📎 출처: `papers/schwietert2021_intrinsic_vs_decomposition_window_sse.md` §7 |
| **B① ⚠ 🆕 그리고 그 정정은 **우리에게 불리하다** (2026-09-22 신설)** | (⚠ **문헌 우위**) | **[Schw21]** LPSC 산화 **2.01 V** · **[Zhu15]** 산화 **2.01 V** — **2015·2021 두 독립 계산이 같다** | ⚠ 우리 **2.256 V** 가 같은 방법 계열에서 **혼자 0.246 V 높다** ⇒ *"우리 2.256 V 가 worst-case 하한"* 이라고 쓸 때, **이 문헌에 대해서는 하한이 아니다**. 게다가 우리 값은 **`LiS₄`·`SCl₃`·`Li₅PS₄Cl₂` 3상을 뺀 뒤**의 값이고 `LiS₄` 하나만 되넣어도 **2.14 V** 로 내려간다 ⇒ *"우리가 더 최신 상집합을 쓴다"* 는 **그 배제를 정당화하기 전에는 못 쓴다**. ✅ **다만 프레이밍 자체는 저자가 활자로 지지한다**: *"for complex solid electrolytes, it is expected that **the direct decomposition stability window is a lower limit**"*. ⚠⚠ **위험한 우연**: 저들 LPSC **층② 폭이 1.08 V** 라 우리 오표기 **1.014 V** 와 0.07 V 차다 — ⛔ **"우리 hull 이 간접 경로를 이미 포함한다" 로 읽으면 안 된다**(우리 값은 층① 을 잘못 읽은 것이고 근접은 무의미하다). 📎 출처: 같은 digest §7-5 |

### ③-2. **§E** (환원/음극) 에 추가할 행 1개 + **정정 1건**

| **E 🔴 🆕 `[Schw20]` 환원 델타 **−0.162 V 는 정정 대상**이다 (2026-09-22 신설)** | (정정) | **[Schw21]** LPSC **층① 환원 1.72 → 층② 환원 1.11 V = −0.61 V**(저들 자신의 델타) | 🔴 **종전 기록**(`papers/schwietert2020_…md` §7-3, `comparison_vs_ours.md` §E): *"저들 간접 1.08 V vs 우리 1.242 V ⇒ −0.162 V"*. **우리 1.242 V 가 환원 한계가 아니므로 이 델타는 무효다.** **정정(우리 유도)**: 우리 층① 환원 **1.717 V** ↔ 저들 층② **1.11 V** ⇒ **−0.607 V**, 이는 **저들 자신의 델타 −0.61 V 와 일치한다** ⇒ **라벨을 고치면 정합이 *좋아진다*.** 📎 출처: `papers/schwietert2021_intrinsic_vs_decomposition_window_sse.md` §7-5-4 |

### ③-3. **§D** (전자구조) · **§A** (이온전도) — **값 이식 금지, 부호만**

| 축 | 제안 | 이유 |
|---|---|---|
| **§D** | **행 신설하지 말고 주석만** — `[Schw21]` `Table S4` 의 `Li₆PS₅Cl` **1.984 eV** 는 **DOS 판독**(*"determined from the density of states"*)이라 **우리가 금지한 방법**이다. 우리 comp1 **2.066 eV**(fixed-occ nscf)와 **같은 셀에 놓지 않는다.** 쓸 수 있는 것은 *"리튬화가 갭을 닫는다(1.984 → 1.219 eV), 탈리튬화는 오히려 올린다(→ 2.391 eV)"* 는 **방향**뿐 | 절대 비교 금지 규율 |
| **§A** | **행 신설하지 말고 주석만** — 600 K AIMD σ 가 pristine **95.78** → 탈리튬 **43.83**(−54 %) → 리튬화 **59.53 S/m**(−38 %). **부호만**(= (탈)리튬화가 σ 를 절반 가까이 떨군다). ⛔ 궤적길이·시드·**MSD 창** 0건, 계 간 온도가 600/1000 K 로 갈린다 | MLIP-MD ↔ AIMD 절대값 금지 |

### ③-4. **§J-37 블록** (신설 제안 — 번호는 병합 시 재확인)

```
### J-37. 🔧🔴 **방법 원전 — [Schw21] 이 "창" 을 두 개로 나누는 법, 그리고 그것이 우리 `reduction_V` 를 잡아낸 경위** (2026-09-22 신설)

📎 출처: `papers/schwietert2021_intrinsic_vs_decomposition_window_sse.md`
🔗 형제: §B①(`[Schw20]`, 같은 그룹의 직전 편 · `papers/schwietert2020_redox_activity_vs_electrochemical_stability.md`) — 기전 서사는 그쪽이 정본이다.

**J-37-a. 두 창의 조작적 정의 (활자 그대로)**

| | decomposition window | intrinsic window |
|---|---|---|
| 정의 | *"formation energy of the most favorable decomposition products at a specific potential, ... determined from the **Li grand potential phase diagram**"* + *"**The decomposition potential closest to the stable solid electrolyte phase** defines the reduction and oxidation redox potentials of the window"* | *"determined from the change in calculated formation energies upon Li insertion and extraction ... **average oxidation/reduction potential** ... referencing the formation energies to the Li-metal chemical potential **similar to intercalation electrodes**"* |
| `[Xiao20Rev]` 층 | **층①** (worst case) | **층②** (topotactic) |
| 우리 대응 | ✅ **같은 양** (`esw_lis4excluded.json`) | ❌ 우리에게 없다 |
| 흐름도 | `Fig. S8` 좌 | `Fig. S8` 우 → 볼록=고용체 / V자=상분리 |

**J-37-b. 🔴 그 정의가 우리 라벨 오류를 잡아냈다 (감사 종결 후보)**
`reduction_V` = "Li 교환이 0 에서 벗어나기 시작하는 가장 높은 φ" 로 읽으면 우리 값은 **1.717 V**(현재 "OCV" 라 부르는 것)이고 저들 **1.72 V** 와 0.003 V 다. 현재 도구는
`tools/oxidation/constrained_esw.py:91-94` 와 `tools/oxidation/esw_cascade_batch.py:417-421` 에서
`red = max(V | evolution > 0)` 을 쓰는데, **`evolution == 0` 행(= Li-보존 구간)이 필터에서 빠져** 한 계단 아래가 잡힌다.
⇒ 🔴 **`esw_cascade_batch.py:435` 의 `window_V = ox − red` 가 cascade 전수에 계통적으로 넓다. 정정 전 인용 금지.**
⇒ 제안 hazard: **`HZ-esw-reduction-limit-label`**.

**J-37-c. ⚠ 이 논문은 방향 표기의 *본보기가 아니라 반례*다** (우리 `HZ-anode-b2o3-reaction-direction` 의 참고)
- `Table 2` 머리글 **"ox/red"** 인데 값은 **red−ox**(낮은 쪽이 환원).
- 본문 p.1491 이 LLZO 를 *"**oxidation and reduction** potential of **0.05 and 2.68 V** ... respectively"* 라 쓴다 — **뒤바뀐 것**(바로 다음 문단이 스스로 반대로 쓴다).
- 기계가 읽을 수 있는 방향 표지는 **부호 있는 Li 교환량** 하나뿐이고, 이 논문에서 그에 해당하는 것은 `Table 1` 이 **산화·환원 용량을 다른 열에 둔 것**뿐이다(검산 가능: `n_Li = C×M/26801.5`, 12행 중 11행이 정수·반정수).
⇒ **우리 도구에 넣을 것**: ① `evolution`(부호 있는 Li 수) **기록 필수** ② 분기 라벨을 **부호에서 유도**(손으로 적지 않는다) ③ **`rxn_at(v) = min|ΔV|` 짝짓기 금지**(`esw_cascade_batch.py:433`) — 행 안에서 이미 짝지어진 쌍만 쓴다 ④ **용량(mAh/g) 동시 출력**으로 사람이 부호를 눈으로 검산.

**J-37-d. ⭐ 이식 가능한 규칙 1개 — hull 모양이 "창 밖의 운명" 을 가른다**
**V자 hull → 상분리 → 준안정 중간상 경유**(LGPS `Fig. 2c`, LAGP) / **볼록 hull → 고용체 → 중간상 없음, 끝을 정하는 것은 분해전압**(LATP `Fig. 2a`, LLTO).
우리 cascade 는 이미 조성별 hull 을 만들므로 **모양 판정 한 줄**이면 후보를 두 부류로 라벨할 수 있다.
⚠ 단 **셀 크기 의존이 그대로 따라온다** — 저자 축자: *"The intrinsic window limits ... are **artificially defined by the smallest composition step of the supercell considered**."*

**J-37-e. ⛔ 이 논문에서 가져오면 안 되는 것**
- **장벽**: NEB 0 · 전이상태 0 · 핵생성 이론 0 · eV 0. `Fig. 3b` 는 **눈금 없는 손그림**이고 `Fig. S8` 에 장벽 상자가 없다 ⇒ *"장벽이 낮음을 계산했다"* 인용 금지.
- **σ 표로 계 간 순위**: 온도가 600 K / 1000 K 로 갈린다. MSD 창·시드·궤적길이 0건.
- **밴드갭 절대값**: DOS 판독(우리 금지 방법).
- **LLTO·LATP 결론**: Ti⁴⁺→Ti³⁺ 를 **U 없이** 계산했다.
- **"12종에서 실험과 훌륭히 일치"**: 정량 대조 **7종**, 실패 **1종**(LYB — 저자 자인 *"the decomposition window has a better predictive value"*), 대조 없음 **1종**(LOC).
- **재현 파라미터**: **ecut 이 없다**(본문은 `Table S1` 에 있다고 쓰는데 cutoff 열 자체가 없다) · **`Li₆PS₅Cl`·LLZO·LAGP 는 k-점·슈퍼셀이 "−"** · **무질서 처리 0줄** · **MP 판본 미기재**.

**J-37-f. ✅ 반대로 가져올 활자 2개**
- 하한 프레이밍: *"for complex solid electrolytes, it is expected that **the direct decomposition stability window is a lower limit**"* — ⚠ **하한의 값은 저들 2.01 V 이지 우리 2.256 V 가 아니다**(§B①).
- CV 단서: *"CV experiments ... performed **without conductive additive** ... are thus **unable to capture the intrinsic electrochemical window**"* — `[Du22LMR]`·`[Zuo]` CV onset 인용 시 필수 동반.

**J-37-g. 📏 층② 값의 재현성 눈금 (우리 유도)**
같은 저자·같은 방법·1년 차로 LPSC 층② 가 **`[Schw20]` 2.24/1.08 → `[Schw21]` 2.19/1.11** 로 바뀌었다(**0.05 / 0.03 V**). 논문은 이 변경을 **언급하지 않는다**.
⇒ 우리가 층② 를 계산하게 되면 **0.05 V 이내를 "일치" 라 부를 외부 근거**가 이것이다.
```

---

## ④ `db/literature/refs.json` 정정 제안 (**제안 문구만 — 나는 수정하지 않았다**)

### ④-1. 기존 `zhu2015` 엔트리 — **제목·저자가 부정확**

현재:
```json
{"id": "zhu2015", "authors": "Zhu, Y. et al.",
 "title": "Electrochemical stability window of Li solid electrolytes from DFT",
 "journal": "ACS Appl. Mater. Interfaces", "volume": 7, "pages": "23685", "year": 2015,
 "key_content": "Band gap vs decomposition voltage relationship for solid electrolytes.",
 "tags": ["SE", "stability", "DFT", "band_gap"]}
```
제안 (근거: **이 논문 ref 8 의 인쇄 서지**):
```json
{"id": "zhu2015", "authors": "Zhu, Y.; He, X.; Mo, Y.",
 "title": "Origin of Outstanding Stability in the Lithium Solid Electrolyte Materials: Insights from Thermodynamic Analyses Based on First-Principles Calculations",
 "journal": "ACS Appl. Mater. Interfaces", "volume": 7, "issue": 42, "pages": "23685-23693", "year": 2015,
 "key_content": "Li grand-potential phase diagram; decomposition window of 20+ SEs. Li6PS5Cl = 1.71-2.01 V; Li3PS4 = 1.71-2.31 V. 우리 grand-potential ESW 의 방법 원전.",
 "tags": ["SE", "stability", "DFT", "grand_potential", "ESW"]}
```
⚠ **현행 `key_content`("Band gap vs decomposition voltage")는 `[Zhu15]` 가 아니라 `zhu2021`(Adv. Energy Mater. 11, 2100370) 쪽 내용으로 보인다** — 두 엔트리가 붙어 있어 섞였을 가능성. **병합자가 원문으로 재확인할 것.**
⛔ 쪽수·issue 는 **이 논문의 참고문헌 인쇄값**에서 옮긴 것이다. 원문 표지 직독은 아직 안 했다.

### ④-2. 신규 엔트리 추가 제안

```json
{"id": "schwietert2021", "authors": "Schwietert, T. K.; Vasileiadis, A.; Wagemaker, M.",
 "title": "First-Principles Prediction of the Electrochemical Stability and Reaction Mechanisms of Solid-State Electrolytes",
 "journal": "JACS Au", "volume": 1, "issue": 9, "pages": "1488-1496", "year": 2021,
 "doi": "10.1021/jacsau.1c00228",
 "key_content": "decomposition window(층①, Zhu15 재현) vs intrinsic window(층②) 를 SE 12종에 적용. Li6PS5Cl 1.72-2.01 V / 1.11-2.19 V. hull 모양(V자=상분리 / 볼록=고용체)이 분해 경로를 가른다. 우리 [Zhu15] 3.4x 감사의 열쇠.",
 "tags": ["SE", "stability", "DFT", "grand_potential", "ESW", "argyrodite", "intrinsic_window"]}
```
(선택) `[Schw20]` 이 아직 없다면 같이:
```json
{"id": "schwietert2020", "authors": "Schwietert, T. K.; Arszelewska, V. A.; Wang, C.; Yu, C.; Vasileiadis, A.; de Klerk, N. J. J.; Hageman, J.; Hupfer, T.; Kerkamm, I.; Xu, Y.; van der Maas, E.; Kelder, E. M.; Ganapathy, S.; Wagemaker, M.",
 "title": "Clarifying the relationship between redox activity and electrochemical stability in solid electrolytes",
 "journal": "Nature Materials", "volume": 19, "issue": 4, "pages": "428-435", "year": 2020,
 "doi": "10.1038/s41563-019-0576-0",
 "key_content": "간접(indirect) 분해 경로의 원전. Li6PS5Cl 2.24 V 탈리튬화 / 1.08 V 리튬화 = 층②.",
 "tags": ["SE", "stability", "DFT", "AIMD", "argyrodite", "ESW"]}
```

---

## ⑤ 병합자에게 — 이 digest 가 **다른 파일에 요구하는 것** (나는 건드리지 않았다)

| 대상 | 요구 | 근거 |
|---|---|---|
| `kb/open_items.md` "Zhu15 3.4× 감사" 블록 | **3.4× → 1.86×** 로 갱신 · 원인 분해(66 % 라벨 / 34 % 산화 한 변) · *"OCV 1.717 vs 1.71 은 우연이 아니라 **같은 양**"* 확정 | digest §7-3 |
| `db/properties/citation_hazards.json` | **`HZ-esw-reduction-limit-label`** 신설 (level: **HOLD** 제안) — 대상: `our_dft_baseline.md` L20 *"환원 한계 1.242 V"* · `esw_lis4excluded.json` `reduction_V` · `esw_cascade_batch.py` 산출 `window_V` 전수 | digest §7-5-1 |
| `litdb/our_dft_baseline.md` L20 | 라벨 교체 제안: *"환원 한계 **1.717 V** (= 종전 'OCV') / 두 번째 환원 평탄 1.242 V"*. ⚠ **pymatgen 재실행 후에 인쇄**한다 | digest §7-8 |
| `papers/schwietert2020_…md` §7-3 | 환원 델타 **−0.162 V → −0.607 V** 정정 (정정하면 저들 델타 −0.61 과 일치) | digest §7-5-4 |
| `papers/schwietert2020_…md` §9 | `Fig. 2b` figure-read **≈1.70 / ≈2.01 V** 가 **인쇄값 1.72 / 2.01** 로 확인됨 ⇒ 불확실 표기 해제 | digest §7-1 |
| `comparison_vs_ours.md` 1021행 | `[Dutra25Rev]` ref 218 에 달린 **`Fig. 5c`** 는 **이 논문의 그림이 아니다**(본문 그림 3장뿐). 내용상 **리뷰 자신의 `Fig. 5c` 가 이 논문 `Fig. 3b,c` 를 옮긴 것**으로 보인다 ⇒ 귀속 문구 재확인 | digest 머리말 |
| (계산 1건, 선택) | `pymatgen` 으로 comp1 프로파일 재실행 — `evolution == 0` 구간의 양 끝을 직접 출력 + `LiS₄`/`SCl₃`/`Li₅PS₄Cl₂` **포함·배제 두 판**. ⚠ 던지기 전에 `kb/templates/estimand_card.md` (*"환원 한계 ≡ Li 교환이 0 에서 벗어나기 시작하는 가장 높은 φ"*) | digest §7-8 |

⛔ **`db/`·`kb/`·`INDEX.md`·`comparison_vs_ours.md`·`refs.json` 은 전부 미수정이다. 커밋도 하지 않았다.**

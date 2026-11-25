<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-11-16 초판 — 본문 14 pp + SI 30 pp 전문. 크롭 46장 (그림 39 = 본문 6 + SI 33 · 표 7) 중 그림 15장 실독.
     fig_S21 은 도구가 놓쳤다 (그림은 SI p.16 아래 · 캡션은 p.17 위로 쪽이 갈림) → 손으로 잘라 figures.json 에 manual_crop 사유를 달았다.
     2026-11-16 재크롭 (본 세션): SI 그림 9 장의 아래 ≈12–13 pt 가 잘려 있었다 (추출기가 캡션 블록 위 끝 — 공백 머리 줄 — 에서 멈춤 · wei2026 SI 와 같은 결함).
     8 장 (S4 · S9 · S12 · S14 · S20 · S22 · S29 · S33) 은 그래픽이 크롭 밖으로 나간 것으로 찾았고, S6 은 축 제목 · 눈금 숫자가 **글자**라 그 측정이 놓쳤다 —
     고친 추출기 (`extract_figures.page_blocks`) 의 bbox 와 비교해서 찾았다. 다시 렌더 · 옛 bbox 는 figures.json `bbox_extractor` 로 보존. 이 9 장은 이 digest 가 실독한 그림이 아니다 (S20 은 쪽 렌더로 봄) — 판독 내용은 안 바뀐다.
     이 digest 의 임무 둘: (1) Haruyama 2014 의 계면 Li 공공 형성에너지(E_v) 방법을 **아지로다이트 Li6PS5Cl (= 우리 comp1) + NCM622** 로
     옮긴 편으로서 그 계산을 감사한다 (2) 셀 창 1.9–3.6 V vs Li-In (논문 환산 2.5–4.2 V vs Li) 이 우리 작동창 2.5–4.25 V 와 같아서
     양극 계면·CEI 판단의 실험 사례로 정리한다.
     결론 요약: SCL 은 이 논문에서도 정량되지 않는다 (두께·전위·전하·Debye 길이 0). 자기 데이터는 '두꺼운 결정성 코팅 =
     화학 보호를 사고 동역학을 판다' 로 더 간단히 설명된다 (§10). -->

# Elucidating and Minimizing the Space-Charge Layer Effect between NCM Cathode and Li₆PS₅Cl for Sulfide-Based Solid-State Lithium Batteries — Chen et al. (*Adv. Energy Mater.* **2024**, 14, 2304443)

> slug `chen2024_space_charge_layer_ncm_linbo3_lpscl` · DOI `10.1002/aenm.202304443` · type `mixed — 실험 주 (합성·TEM·XPS·EIS·CV·operando Raman·GITT·셀) + 정적 DFT+U 슬랩 1절 (MD·NEB·AIMD 0회)` · PDF `litdb/inbox/e57c17f4-Elucidating_and_Minimizing_…_Lithium_Batteries.pdf` (본문 14 pp, `Fig. 1`–`6`) + `litdb/inbox/9c2a20d3-Sup_Elucidating_and_Minimizing_…_Lithium_Batteries.pdf` (SI 30 pp, `Fig. S1`–`S33` · `Table S1`–`S7`) · digested `2026-11-16` · status ✅ · 태그 **[외부]**
> elements: Li, Ni, Co, Mn, O, Nb, P, S, Cl
> methods: DFT, DOS, PDOS, XPS, Raman

> **저자**: **Ya Chen**§ · **Ling Huang**§ · **Deli Zhou**§ (§ 공동 1저자) · Xin Gao · Tengfei Hu · Zhiyuan Zhang · Zheng Zhen · **Xiaodong Chen\*** · **Lifeng Cui\*** · **Guoxiu Wang\*** — 上海交通大 College of Smart Energy (Y. Chen·X. Gao·Z. Zhen·L. Cui) · 上海科技大 School of Physical Science and Technology (L. Huang) · 香港城市大 Mechanical Engineering (D. Zhou·X. Chen) · 中科院 上海硅酸盐研究所 (T. Hu) · 上海理工大 (Z. Zhang) · UTS Centre for Clean Energy Technology (G. Wang) · 접수 2023-12-22 / 개정 2024-04-03 / 온라인 2024-05-22 · NSFC 21804008·52102209 외 · 데이터 *"available from the corresponding author upon reasonable request"* — **구조 파일 공개 0**
> 랩 표기: *Adv. Energy Mater.*, 14, 2304443 (2024).
>
> **계보**: 실험 원점 Ohta 2006/2007 (LiNbO₃ 버퍼 · 본문 ref [14]) → 계산 원점 **Haruyama 2014** (`papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md` · 본문 ref [10]=[11d] · SI ref [6]) 의 **"세 계면 × 자리별 E_v"** 설계를 **LiCoO₂ → NCM622 · β-Li₃PS₄ → Li₆PS₅Cl** 로 바꿔 다시 한 것이 본문 §2.3 이다. XPS 결합에너지 이동을 SCL 표지로 읽는 틀은 본문 ref [11b] (Wang 2020 *Nat. Commun.*) 를 따른다.

> **본 digest 에서 실제로 본 그림 (2026-11-16)** — 크롭 **46장** (그림 39 + 표 7) 중 **그림 15장**.
> **본문 6/6**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` — 전부.
> **SI 9/33**: `Fig. S3` (LNO-300 TEM — 두께 라벨 대조) · `Fig. S15` (⁷Li NMR) · `Fig. S16` (DFT 계면 구조) · `Fig. S18`·`Fig. S19` (사이클 후 EIS — `Table S5` 대조) · `Fig. S20` (SI p.16 쪽 렌더로 봄) · `Fig. S21` (손 크롭) · `Fig. S30` (3.9 V vs Li-In 사이클) · `Fig. S32` (GITT D).
> **안 본 것 (그림 24장)**: `Fig. S1` `S2` `S4`–`S14` `S17` `S22`–`S29` `S31` `S33` — 캡션·본문 서술만 옮겼고 그 자리에 *(안 봄)* 을 달았다. **표 7장** (`Table S1`–`S7`) 은 PDF 텍스트로 전사했다 (이미지로 안 읽음).
> **그림 ↔ 본문 어긋남 7건** (근거는 §3·§10): ① 코팅 두께 배정 — 본문 첫 문장은 LNO-300 ≈20 · LNO-600 ≈7 nm 인데 그림 라벨은 LNO-600 **"20 nm"** (`Fig. 1c`) · LNO-300 **"7 / 6 / 7 nm"** (`Fig. S3b`), 바로 다음 문단도 "LNO-300 의 더 얇은 층" 을 설명한다 ② `Table S5` LNO-300 R_CT **181 Ω** ↔ `Fig. S19` 원호 폭 `figure-read ≈` **310 Ω** ③ ⁷Li NMR "LNO-600 이 가장 넓다" ↔ `Fig. S15` 세 곡선이 겹치고 인셋에선 LNO-600 이 오히려 안쪽 ④ Raman "LNO-300 의 총 신호가 낮다 (`Fig. 5b`)" ↔ 가장 약한 것은 `Fig. 5j` (LNO-850) ⑤ 사이클 후 XPS 본문 "P–S–Li = 160.4 eV" ↔ `Fig. 6e` 의 P–S–Li 띠 `figure-read ≈` 161.5 eV (160.4 eV 는 S²⁻ 띠) ⑥ "LNO-850 에서 P–S–Li 가 안 보인다" ↔ `Fig. 6e` LNO-850 S 2p 에 작은 P–S–Li 성분이 그려져 있다 ⑦ "LNO-600 의 개선된 쿨롱효율" ↔ `Fig. 6a` 첫 사이클 효율 LNO-850 **81.4 %** ≥ LNO-600 **81.3 %**.
> **우리가 직접 한 산수**는 *우리 산수* 로, 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다. ⚠ 문헌 수치는 소환값이다 — 우리 `db/` 절대값과 섞지 않는다.

---

## 0. 이 digest 를 읽는 법 — 왜 우리에게 중요한가

**세 가지가 우리 무대와 겹친다.**

1. **작동창이 우리 셀과 같다.** 모든 주 시험이 **1.9–3.6 V vs Li-In** 이고 논문 자신이 이를 **2.5–4.2 V vs Li⁺/Li** 로 환산한다 (`Table S7` "This work" 행 · `Fig. 5e,i,m` 가로축 "Voltage vs Li⁺/Li" — 눈금 2.4 · 3.2 · 4.0, 곡선은 ≈4.2 까지). 우리 셀 창은 **2.5–4.25 V vs Li⁺/Li** (사용자 2026-11-09). ⇒ 이 논문의 사이클 후 XPS 산물은 **우리 창에서 실제로 생기는 CEI 산물 클래스의 실측 사례**다. 예외: `Fig. S29`·`Fig. S30` 의 **3.9 V vs Li-In (= 4.5 V vs Li)** 시험은 우리 창 위다.
2. **SE 가 우리 comp1 그대로다.** Li₆PS₅Cl (볼밀 + 550 °C 6 h) · 양극 NCM622 · 코팅 LiNbO₃ · 대극 Li-In. 우리 양극 계면·CEI 트랙과 같은 계다.
3. **Haruyama 2014 E_v 방법의 아지로다이트판이다.** 우리 `kb/methodology/computational_methods_canonical.md` 의 "SCL 정량" 표는 *계면 Li 공공 형성에너지 (자리별)* 의 문헌 출처로 Haruyama 2014 하나만 갖고 있다. 이 논문이 **아지로다이트 계면의 자리별 E_v 9개**를 더한다 — 다만 그 계산에는 **화학량론 문제**가 있다 (§4c).

> ⚠ **전압 기준** — 이 논문은 **+0.6 V** 로 환산한다 (`Table S7`: 1.9–3.6 → 2.5–4.2 · 1.9–3.9 → 2.5–4.5). In/InLi 평탄부 통상값 0.62 V 로 하면 2.52–4.22 V 다. CV·GITT·EIS·dQ/dV 축은 전부 **vs Li-In** 이고 `Fig. 5` 의 전압 패널만 vs Li⁺/Li 다. 섞으면 0.6 V 가 통째로 날아간다.

> 🧭 **이 digest 의 판정 축** — 논문 제목의 *"SCL 을 밝히고 최소화했다"* 를 그대로 옮기지 않는다. 자기 데이터로 판정할 수 있는 것은 (a) 열처리 온도에 따른 **표면 상태 세 갈래** (얇은 비정질 코팅 · 두꺼운 결정성 코팅 · 코팅 없는 Nb 도핑 표면) (b) **동역학 대 내구성의 맞교환** (c) **사이클 후 SE 분해 산물 클래스** 셋이다. SCL 은 그 위에 얹힌 **해석**이다 (§7 논증 사슬, §10).

---

## 1. 한 줄 요약

NCM622 에 LiNbO₃ 전구체를 유동층으로 입힌 뒤 **300 / 600 / 850 °C (공기, 3 h)** 로 열처리해 표면이 다른 세 시료를 만들고, Li₆PS₅Cl 복합양극 (Li-In 반쪽셀, 1.9–3.6 V vs Li-In) 에서 **600 °C 시료 (그림 라벨 기준 ≈20 nm 결정성 LNO)** 가 0.2 C **100 사이클 90.6 % (144.8 mAh g⁻¹)** · **800 사이클 136.2 mAh g⁻¹** 로 가장 오래 버틴다. 저자는 이것을 **"SCL (공간전하층) 최소화"** 로 설명하고, 근거로 **XPS 결합에너지 이동** · **DFT 자리별 Li 공공 형성에너지 9개** · **EIS 주파수 어긋남과 CV 용량성 분해** · **operando Raman 피크 이동** 을 든다.

⚠ 그러나 **SCL 자체 (두께·전위·전하) 는 어디서도 측정·계산되지 않았고**, 동역학 지표 (R_CT · 분극 · CV 전류 · 0.5 C 초기 용량) 는 **코팅이 없는 850 °C 시료가 최고**다. 그 시료는 사이클 후 P–S–P·SOx 가 가장 많고 가장 빨리 열화한다. ⇒ 자기 데이터는 **"두꺼운 결정성 LNO 는 화학 보호를 사고 동역학을 판다"** 로 더 간단히 설명된다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | 양극 **LiNi₀.₆Mn₀.₂Co₀.₂O₂ (NCM622)** · 코팅 **LiNbO₃ (LNO)** · SE **Li₆PS₅Cl (LPSC)** · 대극 **Li-In** · 복합양극 NCM@LNO : LPSC : Super P = **70 : 25 : 5 wt** (손 막자) · 활물질 적재 **≈6.2 mg cm⁻²** |
| 시료 넷 | **Bare NCM** (건조만) · **NCM@LNO-300 / -600 / -850** (코팅 후 각 온도 공기 3 h). 대조: **Bare-300 / -600 / -850** (코팅 없이 같은 열처리) |
| 던진 질문 | (서론) *"interfacial ionic conductivity … poses the major concern as rate-determining"* 라는 전제 + 계면 Li⁺ 수송을 막는 셋 — **접촉 상실 · 계면 반응 · SCL** — 중 SCL 을 *"crucial role"* (초록) 로 보고, **코팅을 조절해 SCL 두께를 "whole-process control" 할 수 있나** |
| 문헌 갭 (저자 주장) | SCL 은 *"not been well resolved owing to the difficulty in quantitatively measuring its corresponding physicochemical state at the atomic-scale level"* — 그래서 이 논문이 *"in situ inspection and visualization"* 을 한다고 초록에서 말한다 |
| 실험 축 | XRD (Rietveld 는 GSAS — 결과 표 없음) · SEM · TEM/HRTEM/EDS · **XPS (깊이 0 / <3 nm)** · ⁷Li NMR · **EIS** (전후) · **CV 0.05–1.0 mV s⁻¹** · **operando Raman** · **GITT (60 °C)** · 정전류 사이클 · 율속 |
| 계산 축 | **VASP PAW · PBE+U+D3 · 계면 슬랩 3종 · 자리별 E_v 9개 · PDOS** (§4b) |
| 연구유형 | **mixed** — 실험이 주, DFT 는 §2.3 한 절 + SI §1.5 |

---

## 3. 결과 — 절별 전수 (수치 + 그림 실독)

### 3a. 시료 — 코팅 온도가 만든 세 표면 (`Fig. 1` ✅ · `Fig. S3` ✅ · `Table S1` · `Fig. S1`·`S2`·`S4`–`S7` 안 봄)

**XRD (`Fig. S1` 안 봄 · 본문)**: 전 시료 R-3m, ≈65° (108)/(110) 갈라짐 유지, LNO 회절선 없음 (함량이 낮아서라고 저자). ⚠ **LNO 함량 (wt%) 은 논문 어디에도 없다.**

**`Table S1` — I(003)/I(104)** (낮을수록 Li/Ni 혼합 ↑)

| Bare | LNO-300 | LNO-600 | LNO-850 | Bare-300 | Bare-600 | Bare-850 |
|---|---|---|---|---|---|---|
| **1.72** | 1.50 | **1.66** | **1.09** | 1.34 | 1.32 | 1.28 |

- 열처리만 해도 비 1.72 → 1.28–1.34 로 떨어진다 (혼합 ↑). 코팅이 300·600 °C 에서는 그 하락을 막는다 (1.50 · 1.66). **850 °C 는 1.09** — 저자 표현 *"serious cation mixing"*.
- ⚠ 본문은 Bare 를 **1.73** 이라 적는다 (표 1.72). 사소.
- *관례 (논문 밖 지식)*: I(003)/I(104) 1.2 를 경험 문턱으로 쓰는 일이 흔하다 — 논문은 문턱을 말하지 않는다. 850 시료는 그 아래다 ⇒ **"코팅 없음" 과 "심한 양이온 혼합" 이 850 시료에 겹쳐 있다** (§10-⑬).

**TEM / HRTEM — 두께 (그림 라벨 실독)**

| 시료 | 그림 | 라벨 | 본문 첫 문장 | 판정 |
|---|---|---|---|---|
| LNO-300 | `Fig. S3b` ✅ | **"7 nm · 6 nm · 7 nm"** (50 nm 축척) · `Fig. S3c` d₀₁₂ = 0.375 nm (흐린 격자) | "≈20 nm" | 본문 첫 문장과 **반대** |
| LNO-600 | `Fig. 1c` ✅ | **"20 nm"** 두 곳 (50 nm 축척) · `Fig. 1d` d₀₁₂ = 0.375 nm 선명 · NCM d₀₀₃ = 0.478 nm | "≈7 nm" | 본문 첫 문장과 **반대** |
| LNO-850 | `Fig. S4` 안 봄 | 코팅층 없음, 표면에 NCM (104) 격자 → **Nb 도핑** (저자) | — | — |

- 본문 바로 다음 문단: *"the **thinner LNO layer** observed by TEM for **NCM@LNO-300** sample could be ascribed to the stripping possibility during annealing process and structural damage by electronic beam"* ⇒ **그림 라벨과 이 문단이 맞고, 첫 문장의 배정이 뒤바뀐 것**으로 읽는다. 이 digest 는 **LNO-300 ≈ 6–7 nm (비정질에 가까움) · LNO-600 ≈ 20 nm (결정성)** 으로 쓴다.
- 전 시료 공통 격자 0.237 / 0.478 / 0.143 nm = NCM (006)/(102) · (003) · (110).

**XPS — 코팅 화학 (`Fig. 1f–h` ✅)**

| 신호 | 값 (본문) | 온도에 따라 (`figure-read`) |
|---|---|---|
| Nb 3d₅/₂ "Bul. Nb" (LNO 의 Nb–O) | **206.2 eV** (3d₃/₂ 209.0) | 300 °C 에서 우세 |
| Nb 3d₅/₂ "Int. Nb" (Nb 도핑 NCM) | **205.7 eV** (3d₃/₂ 208.5) | 300 < 600 < 850 — 850 에서 압도적 |
| O 1s CO₃²⁻ | **531.0 eV** | `figure-read ≈` **300 → 600 → 850 으로 봉우리가 커진다** — 본문은 *"originates from the bulk NCM"* 이라고만 하고 증가를 논하지 않는다 |
| O 1s 격자 O / 계면 O | 529.3 / **528.6 eV** | 850 에서 계면 O 우세 |
| Ni 2p₃/₂ · 2p₁/₂ | 854.4 · 872.0 eV (300·600) → **854.7 · 872.3 eV (850)** | +0.3 eV — Nb 도핑 탓 (저자) |

- 깊이 분석 (`Fig. S7c–e` 안 봄): LNO-600 은 **30 nm · 60 nm 깊이에서 Nb 3d 가 안 보인다** → 도핑은 얕다. Co 2p · Mn 2p 불변 (Co³⁺ · Mn⁴⁺).

### 3b. LPSC 전해질 (`Fig. 2a–f` ✅ · `Table S2`·`Table S3` · `Fig. S8`·`S9` 안 봄)

**`Table S3`** — 온도별 펠릿 EIS (온도마다 R 세 번)

| T (K) | 293.15 | 303.15 | 313.15 | 323.15 | 333.15 | 343.15 | 353.15 |
|---|---|---|---|---|---|---|---|
| R (Ω, 셋) | 60.19/60.29/60.21 | 43.11/43.19/42.26 | 28.71/28.80/28.62 | 25.88/25.95/26.35 | 20.04/20.12/20.03 | 16.03/16.01/16.05 | 12.35/12.34/12.38 |
| σ (mS cm⁻¹) | **2.117** | **2.995** | 4.437 | 4.923 | 6.356 | 7.946 | 10.315 |

- ⚠ **"RT 2.995×10⁻³ S cm⁻¹" 은 30 °C 값**이다. 20 °C 는 2.117 mS cm⁻¹.
- **Ea = 0.259 eV** (`Fig. 2f`, ln(σT) vs 1000/T). *우리 산수*: 7점 단순 최소제곱 **0.254 eV** (0.005 eV 차 — 무시 가능). `Table S3` 의 30 °C ln(σT) **−0.110** 은 σ·T 로 다시 내면 **−0.097** (나머지 여섯은 맞는다).
- `Fig. 2e` 실독: 20–80 °C 전부 **원호 없이 전극 스파이크만** — 절편 `figure-read ≈` 60 → 12 Ω, `Table S3` 과 일치. `Fig. 2f` 의 오차막대는 **가로 방향** (1000/T 쪽) 으로 그려져 있다 — 측정 반복의 R 산포라면 세로여야 한다.
- 본문: Ea 가 *"consistent to result of reported literatures [12]"* — 그런데 **같은 SI 의 `Table S2` 는 그 [12] 의 Li₆PS₅Cl 을 Ea 0.33 eV · 3.5 mS cm⁻¹ 로 싣는다.** 자기 비교표와 어긋난다.
- **홉 수 검산** (규약 · ν₀ 10¹³ s⁻¹ **가정** · 298 K): Γ = ν₀·exp(−0.259 eV / kT) ≈ **4×10⁸ s⁻¹** · 평균 대기 1/Γ ≈ **2.4 ns** — "빠른 이온전도체" 서술과 차수 모순 없음. (이 Ea 는 펠릿 전체의 겉보기 활성화에너지지 한 홉의 장벽이 아니다.)
- 🔧 **펠릿 기하 검산** (*우리 산수* — 전도도 펠릿이 SI §1.1 의 **"200 mg · Ø14 mm · 200 MPa"** 펠릿이라는 **가정**): σ = L/(R·A) 에 30 °C 값 (σ 2.995 mS cm⁻¹ · R 43.1 Ω · A 1.539 cm²) 을 넣으면 **L ≈ 0.199 cm** → 밀도 **≈0.65 g cm⁻³** = 결정밀도 (a ≈ 9.85 Å **가정** · Z 4 → ≈1.87 g cm⁻³) 의 **≈35 %**. 200 MPa 냉간압착 펠릿으로는 너무 낮다 ⇒ 다른 펠릿·다른 면적을 썼거나 σ 가 과대다. **두께는 논문에 없다** — 판정 불가, 표시만.

### 3c. XPS 로 읽은 "SCL" — S 2p 결합에너지 이동 (`Fig. 2g–l` ✅ · `Fig. S13`·`S14` 안 봄)

**설계**: 복합양극 (사이클 전) 의 S 2p 를 **"NCM/LPSC 계면에서 0 nm (왼쪽) 와 <3 nm (오른쪽)"** 두 깊이에서 잰다. 기준: LPSC 의 **PS₄³⁻ 162.3 eV · S²⁻ 161.0 eV** (본문).

| 비교 | 본문 서술 | `figure-read ≈` (주봉 2p₃/₂ 위치, ±0.1 eV) |
|---|---|---|
| **ΔE₁** 계면 (0 nm) | 코팅 없는 Bare NCM · Bare-600 이 코팅 시료보다 **낮은 결합에너지** 쪽 | 코팅 셋 ≈162.3 · 무코팅 둘 ≈162.0 → **≈0.3 eV** |
| **ΔE₁** 차표면 (<3 nm) | 같은 방향 유지 | LNO-300·850 ≈162.5 · 무코팅 ≈162.1 → **≈0.4 eV** |
| **ΔE₂** 차표면 | **LNO-600 만 더 높은 결합에너지** — *"disappearance or dramatic decline of BEF driven by SCL at this depth"* | LNO-600 ≈163.0–163.1 vs LNO-300·850 ≈162.5 → **≈0.5–0.6 eV** |

- `figure-read`: **S²⁻ (녹색) 성분이 무코팅 시료에서 더 크다** (`Fig. 2k`·`2l`). 사이클 전인데도 그렇다.
- 저자 논리: 계면에서 Li⁺ 가 LPSC → NCM 으로 넘어가 **LPSC 쪽이 Li 결핍 (음전하) → 내장전기장 (BEF) → 결합에너지 하향 이동** ⇒ 이동이 클수록 SCL 이 크다. Bare-600 대조로 "열처리 자체의 영향" 을 뺐다고 한다. P 2p (`Fig. S13`) 도 같은 패턴 — 본문은 이것을 **"ΔE₁ and ΔE₄"** 라 부르는데 **ΔE₃·ΔE₄ 라는 XPS 표지는 다른 곳에 정의가 없다** (`Fig. S13` 안 봄).
- TM 2p (Ni·Co·Mn, `Fig. S14` 안 봄) 는 시료 간 **거의 같다** → *"the shift of S 2p and P 2p are irrelevant to the external factors"* — 장비 대전 보정 문제를 배제하려는 내부 기준이다 (이건 좋은 설계다).
- 🔴 **빠진 것**: 스퍼터 (이온·에너지·속도) · 결합에너지 보정 기준 · **무대기 이송 여부** — 황화물이라 셋 다 결과를 움직인다. 그리고 **무작위 복합체에서 "NCM/LPSC 계면으로부터 0 nm / <3 nm"** 는 기하적으로 정의되지 않는다 (계면이 모든 방향으로 나 있다) — 평판 모델 시료를 쓴 기록이 없다 (§10-⑥).
- ⁷Li NMR (`Fig. S15`) 은 §3k.

### 3d. ⭐ DFT — 계면 세 개의 자리별 Li 공공 형성에너지 (`Fig. 3` ✅ · `Fig. S16` ✅)

**정의 (SI §1.5)**: `E_f = E_v + E_Li − E_Pure`, **E_Li = Li 금속**, 두 계 모두 DFT+U 이완. ⇒ **eV 값이 그대로 "그 자리에서 Li 하나를 빼는 국소 전압 (V vs Li)" 으로 읽힌다** (중성 공공 — 전자는 셀 안 공통 페르미 준위에서 빠진다). Haruyama 2014 와 같은 정의다.

**9개 값 전수** (자리 위치는 `Fig. 3a,d,g` 실독)

| 계면 | P1 | P2 (계면) | P3 | 논문 지표 (P2 − P3) | *우리 산수* P2 − P1 |
|---|---|---|---|---|---|
| **NCM(110)/LNO(1-10)** | **3.702** (NCM 안 Li 층) | **3.932** | **3.739** (LNO 안) | **ΔE_v1 = 0.193** | +0.230 |
| **NCM(110)/LPSC(100)** | **3.643** (NCM 안) | **3.742** (첫 LPSC 층) | **3.254** (LPSC 차표면) | **ΔE_v2 = 0.488** | +0.099 |
| **LNO(1-10)/LPSC(100)** | **2.165** (LNO 안) | **2.904** (LPSC 쪽 계면) | **2.825** (LPSC 안) | **ΔE_v3 = 0.079** | **+0.739** |

- `Fig. 3b,e,h` 실독: **세로축 E_v(Liᵢ) 에 눈금·숫자가 없다** — 값은 점 위 글자로만 있다. 가로축 "Positions" 는 모식.
- **본문 해석 (전수)**
  - NCM/LNO: NCM 쪽 3.702 ≈ 벌크 (ref [26] Koyama 2012) · **LNO 쪽이 벌크 LNO (ref [27]) 와 다른 것은 전자가 LNO VBM 이 아니라 NCM VBM 에서 빠지기 때문** (밴드 오프셋 — Haruyama 와 같은 설명) · ΔE_v1 이 작아 *"homogeneous distribution of Li⁺"*.
  - NCM/LPSC: 계면 3.742 → 차표면 3.254 로 **0.488 eV 낙하** ⇒ *"NCM surface with plenty of sites for Li adsorption facilitates the formation of highly concentrated layer at NCM/LPSC interface and Li-deficient layer at subsurface in LPSC region, which is driven by chemical potential difference"*.
  - LNO/LPSC: LPSC 쪽 두 자리 차 0.079 eV ⇒ LNO 버퍼가 *"effectively restrains the redistribution of Li⁺ ions in NCM/LNO/LPSC system and significantly mitigates blockage of Li⁺ ions transport caused by SCL"*.
- 🔎 ***우리 산수* — 논문이 말하지 않은 것**: LNO/LPSC 의 **P1 (LNO 쪽) → P2 가 0.739 eV** 로 **세 계면 통틀어 가장 큰 단차**다. 저자 자신의 읽는 법 (낮은 E_v = Li 가 잘 빠진다 = Li 결핍) 을 그대로 적용하면 **LNO/LPSC 접촉에서 LNO 쪽이 Li 결핍층**이 된다 — 코팅 안에 SCL 이 생긴다는 뜻인데 논의가 없다. ΔE_v3 를 P2–P3 로만 정의해서 이 단차가 지표에서 빠졌다. (정의 자체는 세 계면에 일관되게 P2 − P3 이다 — 선택이 부당하다는 게 아니라 **지표가 그 단차를 못 본다**는 것.)
- **Haruyama 식 "편차" 지표로 옮기면** (*우리 산수* · `computational_methods_canonical.md` §2 가 권하는 목표함수): SE 쪽 자리 간 차 NCM/LPSC **0.488 → LNO/LPSC 0.079 eV (−84 %)** — 단 **SE 쪽 자리가 계면당 2개뿐**이다 (Haruyama 는 6개: 1.83 → 0.76 eV, −58 %). 방향은 같고 크기는 비교 못 한다.
- ⚠ **계면 간 절대값 비교 금지**: E_v 의 절대값은 전자가 빠지는 공통 페르미 준위가 정한다 — NCM 이 있는 두 계면은 NCM 의 Ni d 가, LNO/LPSC 는 LPSC 가 정한다 (§4c 의 정공까지 겹친다). 그래서 LNO/LPSC 의 2.2–2.9 eV 가 나머지 3.25–3.93 eV 보다 낮은 것은 **SCL 이 아니라 전자 저장소 차이**다.

**PDOS (`Fig. 3c,f,i` 실독 — 전부 `figure-read ≈`, Γ 점 하나에서 낸 뾰족한 DOS)**

| 계면 | 본문 서술 | 그림에서 읽은 것 |
|---|---|---|
| NCM/LNO (`Fig. 3c`) | NCM 이 VBM 을 만들고 갭 **"0 to 0.5 eV"** · LNO 의 낮은 VBM = 전자 절연 | TDOS 가 0–0.7 eV 에서 **0 이 아니라 낮은 골** (가성 갭). LNO (청록) VB 주 가장자리 ≈ −2.3 eV (꼬리 ≈ −1.5 eV) · CB 시작 ≈ +0.8–1.0 eV ⇒ 이 계면의 LNO 갭 ≈2–3 eV |
| NCM/LPSC (`Fig. 3f`) | NCM 표면 상태가 0–1 eV 에 비편재 (Ni/Co/Mn 3d 와 S·Li 상호작용) · **E_F 에서 높은 TDOS = 전자 수송** | **LPSC (노랑) VB 가 E_F 바로 밑에서 끊긴다 (LPSC VBM ≈ E_F)** · LPSC 성분은 ≈ +3.5 eV 까지 거의 0 · NCM 상태는 E_F 를 가로질러 이어진다 |
| LNO/LPSC (`Fig. 3i`) | **LNO 의 VBM 이 LPSC 보다 낮다 → "LNO acts as electronic insulator against LPSC"** · E_F TDOS 감소 | LNO VB 가장자리 ≈ −2.7 eV 로 낮은 건 맞다. 그런데 **LNO (청록) 성분이 E_F 바로 위 (≈0–0.2 eV) 에서 솟아 ≈1.5–2 eV 에서 최대** — **LPSC VB 꼭대기와 LNO 전도대 바닥이 같은 높이**로 그려져 있다. 전자 차단에는 VB 오프셋만이 아니라 CB 오프셋도 필요하다 |

- **"E_F 의 TDOS 가 줄었다" 는 그림으로 읽기 어렵다** — 세 셀의 원자 수가 **372 / 284 / 272** 로 다르고 TDOS 는 셀당 값 (정규화 없음) 이며, `figure-read` 로 `Fig. 3f` 와 `Fig. 3i` 의 E_F 근처 TDOS 는 같은 크기 (수십 eV⁻¹) 다.
- SI 자인: *"The reduced band gap could be observed in all three kinds of heterojunction interface … which seems to exerts electronic conduction characteristic and **not completely consistent with the conclusions of previous studies**."* 저자 설명 = **반도체 표면상태 + "PN junction"**. 🔎 *더 간단한 대안 둘* — ① 이 기하는 진공에 면한 **자유 표면이 두 개** 있고 그 상태가 갭에 들어온다 ② LPSC 쪽 **화학량론이 맞지 않아 정공 6개**가 있다 (§4c).

**계면 구조 (`Fig. S16` 실독 + SI 서술)**
- 세 셀 모두 **계면 법선 (c) 방향 양끝에 진공**이 있다 — 단일 계면 + 진공 기하 (우리 v5 와 같은 계통, Haruyama 원전).
- **NCM/LNO**: NbO₆ 가 MnO₆·CoO₆·NiO₆ 와 **O 를 공유**해 결합 · 이종 다면체 없음 (저자: *"intrinsic match and strong interface bonding"*).
- **LNO/LPSC**: **NbO₄S₂** 다면체가 PS₄ 와 S 를 공유 · **NbO₄Cl** 단위 — 저자는 *"intrinsic affinity"* · *"tightly combined interface"* 로 읽는다. 🔎 **Nb–S · Nb–Cl 결합 형성은 계면 반응 (S/O 교환 경향) 의 신호이기도 하다** — Haruyama 2014 의 LNO/β-LPS 는 *Nb–S 결합 없음* 이었다 (§7c).
- **NCM/LPSC**: *"obvious S/O exchange"* — **NiO₄S₂ 팔면체 · NiO₄S 다면체 · CoO₄S** 형성 → *"unconsolidated interface and vast Li⁺ adsorption sites"*. `figure-read`: 인셋에서 **계면 TM 이 S 와 결합**한 것은 보이지만 **O 가 LPSC 쪽으로 넘어간 모습은 그림에서 확인되지 않는다** ("교환" 의 절반만 보인다).
- `figure-read`: 두 LPSC 슬랩 모두 PS₄ 방향이 제각각이라 **결정 질서가 눈에 띄지 않는다** (투영 그림이라 단정은 못 한다).
- 🔎 **결합 자리 배위수 규약** (우리 2026-10-05 결정): 구조 파일이 공개되지 않아 **P2 (계면 "흡착" 자리) 의 배위수는 미확인**이다.

### 3e. EIS — 사이클 후 계면 저항 (`Fig. 4a–c` ✅ · `Fig. S18`·`S19` ✅ · `Table S5` · `Fig. S17` 안 봄)

**회로**: R₀ + (R_gb ‖ CPE_gb) + (R_CT ‖ CPE_CT) + CPE_w (`Fig. 4b` 삽입). 음극 쪽 R_CT′ 는 *"tiny"* 하다며 뺀다 (Li-In 근거). 측정: Autolab · 10 mV · 1 MHz–0.1 Hz · 사이클 전 OCP 1.9 V vs Li-In · 사이클 후 *"fully discharged to 1.9 V … and then EIS tests were conducted with OCPs maintained at 3.1 V vs Li⁺/Li-In"* (⚠ 방전 끝 1.9 V 와 OCP 3.1 V 가 한 문장에 있다 — 측정 SOC 가 불분명).

**`Table S5`** (사이클 후로 읽힌다 — 캡션엔 언제인지 없음)

| 시료 | R_g [Ω] (본문은 R₀) | R_gb | R_CT | R_total |
|---|---|---|---|---|
| Bare | 39.9 | 36.0 | 293 | 368.9 |
| LNO-300 | 22.0 | 15.5 | **181** | 218.5 |
| LNO-600 | 20.4 | 16.3 | **263** | 299.7 |
| LNO-850 | 23.3 | 9.88 | **11.7** | **44.88** |

**그림 실독 (원호 끝 = 저주파 극소점, `figure-read ≈`)**

| 시료 | Nyquist 정점 | 원호 범위 (Ω) | Bode 위상 정점 |
|---|---|---|---|
| Bare (`Fig. S18`) | 27 Hz | ≈40 → **≈425** (극소 2 Hz) | 100 Hz |
| LNO-300 (`Fig. S19`) | 27 Hz | ≈20 → **≈330** (극소 2 Hz) | 100 Hz |
| LNO-600 (`Fig. 4b`) | 37 Hz | ≈30 → **≈265** (극소 4 Hz) | 139 Hz (≈41°) |
| LNO-850 (`Fig. 4b`) | 720 Hz | ≈20 → **≈60** (극소 100 Hz) | 1400 Hz |

- 🔴 **`Table S5` 의 LNO-300 R_CT 181 Ω 은 `Fig. S19` 의 원호 (폭 ≈310 Ω) 와 안 맞는다.** 그림 순위는 Bare > LNO-300 > LNO-600 ≫ LNO-850 이고 본문 *"the minor R_CT of NCM@LNO-600 sample compared to NCM@LNO-300 sample after cycling"* 도 그림 쪽이다 — **표가 틀렸거나 다른 상태의 값**이다.
- **가장 낮은 저항은 코팅 없는 LNO-850** (R_CT 11.7 Ω · 원호 ≈40 Ω). 저자 설명: *"shorter interfacial Li⁺ ions transport range with no apparent overlayer observed, which surpasses the influence of SCL"* — 그리고 §2.6 에서 *"seems to not match the its low total resistance"* 라고 스스로 긴장을 인정한다.
- **사이클 전** (`Fig. S17` 안 봄, 본문): 전부 직선 · R₀ ≈20 Ω · *"Bare NCM … minimum R₀"* · 코팅 중 LNO-600 최저 · LNO-300 최대 (부분 비정질) · LNO-850 중간 (Nb 도핑). 수치 표는 없다.
- **식 (1) — "주파수 어긋남 = SCL 용량 효과"**: 저자는 Nyquist 정점 ω₀ 와 Bode 정점 ωₙ 이 다른 것을 *"effects caused by capacitances and could be related to SCL"* 이라 읽고 `ωₙ = √((R_s + R_ct)/R_s)·ω₀` 를 적는다. 🔴 **이 식은 R_s + (R‖C) 회로라면 언제나 성립하는 항등식이다** (위상 tan φ 를 ω 로 미분하면 그대로 나온다). *우리 산수*로 저자 자신의 값을 넣으면: LNO-600 37 Hz × √((20.4 + 263)/20.4) = **138 Hz** (관측 **139 Hz**) · LNO-300 (그림 R) ≈110 Hz (관측 100) · Bare ≈82–88 Hz (관측 100) · LNO-850 ≈0.9–1.0 kHz (관측 1.4 kHz — 원호가 작고 R_gb 원호와 겹친다). ⇒ **어긋남은 직렬저항 하나로 설명된다 — SCL 의 증거가 아니다.**

### 3f. CV · b 값 · "용량성 기여" (`Fig. 4d–i` ✅ · `Fig. S20` ✅ p.16 렌더)

- 창 1.9–3.9 V vs Li-In (≈2.5–4.5 V vs Li), 0.05–1.0 mV s⁻¹.
- `figure-read`: **LNO-600 (`Fig. 4d`) 의 산화 전류는 창 안에서 봉우리 없이 3.9 V 꼭짓점까지 오른다** (1 mV s⁻¹ 에서 ≈1.55 mA cm⁻²) · 환원 봉우리 ≈ −0.75 mA cm⁻² @ ≈2.3–2.4 V. **LNO-850 (`Fig. 4e`)** 은 산화 봉우리 ≈3.95 mA cm⁻² @ ≈3.75 V · 환원 ≈ −2.45 @ ≈2.9 V ⇒ **같은 주사속도에서 LNO-850 전류가 2.5–3 배 크다.**
- **b 값** (log i = log a + b log v): **Bare 0.629 · LNO-600 0.464 · LNO-850 0.653**. 저자: 600 은 확산 지배, Bare·850 은 확산 + 용량성 혼합.
  - `Fig. 4f` 세로축 단위는 **mA** (면적 정규화 없음) · **어느 봉우리 (산화/환원) 를 썼는지 명시 없음**. LNO-600 은 산화 쪽 봉우리가 없으니 산화 쪽이라면 **꼭짓점 전류**를 쓴 셈이다.
  - `figure-read`: LNO-600 의 0.8·1 mV s⁻¹ 점이 직선 **아래로 휜다** — 저항 제한의 전형. b < 0.5 자체가 순수 확산 (0.5) 보다 느리다는 뜻이라 *"mainly controlled by diffusion process"* 보다는 **저항·분극 제한**으로 읽힌다.
- **Dunn 분해** (i = k₁v + k₂v^½, `Fig. 4g–i`, `figure-read ≈`): 용량성 비율 0.05 → 1 mV s⁻¹ — **LNO-600 ≈3 → 28 %** · **LNO-850 ≈43 → 94 %** · Bare (`Fig. S20d`) ≈20 → 80 %. 0.5 mV s⁻¹ 에서 600 ≈12 % · 850 ≈64 %.
  - 저자 해석: 용량성 비율이 큰 시료 = *"plenty of sites for Li⁺ ions adsorption"* = SCL 큼.
  - 🔎 *우리 산수*: 0.05 mV s⁻¹ 로 2 V 창을 한 번 쓰는 데 **≈11 h** 다. 그 속도에서 전하의 **43 %** 가 "용량성" 이라면 이중층으로는 설명이 안 되는 크기다 — Dunn 식의 k₁v 항은 **"전류가 v 에 비례하는 모든 것"** (빠른 표면 산화환원 · SE 분해 전류 · 오믹 왜곡) 을 받는다. 그것을 "Li 흡착 자리 수" 로 바꿔 읽을 근거는 논문 안에 없다.

### 3g. operando Raman — "응력" 으로 읽은 PS₄³⁻ 피크 이동 (`Fig. 5` ✅ · `Table S6` · `Fig. S23`–`S27` 안 봄)

- 장비 Renishaw inVia Qontor · 100–800 cm⁻¹ · 0.1 C (1 C = 180 mA g⁻¹) 첫 충방전 · *"cells … sealed in the test mold"*. ⚠ **레이저 파장·출력·격자·창 (광학 접근 방법)·보정 미기재.** `Fig. 5a` 모식은 **양극 윗면**에 빛을 쏜다 — 측정 대상은 복합양극 표면의 LPSC 이지 "양극 계면 근처" 로 골라진 LPSC 가 아니다.
- **`Table S6`**: ≈195 (PS₄³⁻) · ≈270 (S–P–S 변형) · ≈570 (PS₄³⁻) cm⁻¹ = LPSC · **≈372 cm⁻¹ = Li₂S T₂g** (기준). 추적 대상은 최강선 **≈422 cm⁻¹**.
- 해석 전제: *"positive correlation between Raman peak frequency change and applied pressure in SEs with cubic phase"* (ref [35]) → **양의 이동 = 응력 증가**. ⚠ **cm⁻¹/GPa 계수가 없어서 "응력" 은 정성**이다.
- **`figure-read` (`Fig. 5d,h,l` — 가로축 ≈418–425 cm⁻¹, 눈금 420·424)**: 위치값이 **≈1 cm⁻¹ 간격 계단으로만 움직인다** (CCD 화소 간격 수준). 맞춤 불확도 표시 없음.

| 시료 | 충전 | 방전 | 끝 vs 처음 |
|---|---|---|---|
| LNO-300 (`Fig. 5d`) | ≈424 (처음 2점) → ≈422 | ≈422 → ≈420.5–421 | ≈ −3 cm⁻¹ (비가역) |
| LNO-600 (`Fig. 5h`) | ≈420.8 일정 (끝 1점 ≈419.5) | ≈422.3 일정 | ≈0 (가역) |
| LNO-850 (`Fig. 5l`) | ≈422.8 → ≈419.5 → ≈421.2 | ≈419.3 | ≈ −3.5 cm⁻¹ (비가역) |

- 본문 결론: LNO-300 은 *"more frequent and irregular stress changes"* · LNO-600 은 *"steady levels"* 로 접촉 유지 → 장기 수명. **그림의 "가역 / 비가역" 구분 자체는 읽힌다.** 다만 크기가 1–4 cm⁻¹ 로 분해능 근처다.
- 🔴 본문 *"its **lower total signal intensities** during cycling (**Figure 5b**)"* (LNO-300) — `figure-read`: `Fig. 5b` (LNO-300) 와 `Fig. 5f` (LNO-600) 는 둘 다 ≈20 k 의 붉은 띠이고 **가장 약한 것은 `Fig. 5j` (LNO-850, ≈10–13 k)** 다. operando 원세기는 초점·위치에 따라 바뀌어 정규화 없이 구조 지표로 쓰기도 어렵다.
- Eg(Mn) ≈600 cm⁻¹ (`Fig. S27` 안 봄): 300·600 의 경향이 같아 *"excludes the influence of different states of charge"* (저자).

### 3h. 셀 성능 (`Fig. 6a,b,d,f` ✅ · `Fig. S21` ✅ · `Fig. S30` ✅ · `Table S4` · `Table S7` · `Fig. S22`·`S28`·`S29` 안 봄)

**첫 사이클 0.05 C (`Fig. 6a`, 1.9–3.6 V vs Li-In)**

| 시료 | 충전 (mAh g⁻¹) | 방전 | 첫 효율 (그림 라벨) |
|---|---|---|---|
| LNO-600 | **210.8** | **171.3** | **81.3 %** |
| LNO-850 | `figure-read ≈`195 | 157.9 | **81.4 %** |
| LNO-300 | `figure-read ≈`197 | 157.7 | 80.7 % |
| Bare | `figure-read ≈`161 | 123.2 | 76.4 % |

- 본문 *"comprehensive advantages of preferable charge capacity (210.8) and improved coulombic efficiency (81.3 %)"* — **효율은 850 이 0.1 %p 높다.** 600 의 이점은 **용량**이다.

**`Table S4`** — 0.05 C ×2 → 0.1 C ×2 → 0.2 C ×31 → 0.5 C ×36 (1.9–3.6 V vs Li-In)

| 시료 | 1st @0.05C | 3rd @0.1C | 5th / 35th @0.2C | 36th / 71st @0.5C |
|---|---|---|---|---|
| Bare | 123.2 | 112.2 | 102.2 / 95.4 | 70.3 / 36.0 |
| LNO-300 | 157.7 | 146.7 | 132.5 / 127.2 | 100.4 / 68.3 |
| LNO-600 | **171.3** | **161.7** | 149.2 / 142.1 | 117.4 / **108.1** |
| LNO-850 | 157.9 | 155.3 | 148.7 / **147.1** | **134.1** / 71.9 |

- ⇒ **0.2 C 30 사이클은 850 이 600 만큼 버티고 (147.1 vs 142.1), 0.5 C 첫 값은 850 이 최고 (134.1 vs 117.4)** — 그리고 0.5 C 36 사이클 동안 850 은 71.9 로 무너지고 600 은 108.1 로 남는다. **850 = 빠르지만 오래 못 간다 · 600 = 느리지만 오래 간다.**
- **`Fig. S21` 실독**: 분극 (평균 충전 − 방전 전압) 0.2 C 에서 **850 ≈0.05 V vs 300·600 ≈0.10–0.20 V** · 0.5 C 에서 **850 ≈0.11 V vs ≈0.38–0.40 V** · 작동전압 0.5 C 에서 850 ≈3.14 · 600 ≈2.97 · 300 ≈2.95 V vs Li-In · dQ/dV 봉우리 간격도 850 이 가장 좁다. 저자는 850 의 안정한 분극을 *"Li⁺/Ni⁺ cation mixing and doping effect"* 로 돌린다.
- **율속 (`Fig. 6b`, 4 사이클씩)**: LNO-600 **160.7 / 146.4 / 128.7 / 114.2 / 101.7 / 90.4** mAh g⁻¹ (0.1 / 0.2 / 0.4 / 0.6 / 0.8 / 1 C) → 0.1 C 복귀 **156.3**. `figure-read ≈`: LNO-300 · 850 은 0.4 C 부터 거의 겹친다 (≈118 / 104 / 92 / 83) · Bare ≈116 / 98 / 76 / 60 / 45 / 33.
  - ⚠ **`Table S4` 와 `Fig. 6b` 의 순위가 0.5 C 근처에서 뒤집힌다** (표: 850 > 600 · 그림: 600 > 850). 다른 셀·다른 이력이라 모순은 아니지만, **셀 간 산포가 순위만큼 크다**는 뜻이다.
- **장기 0.2 C (`Fig. 6d`)** — ⚠ 그림 캡션에 C-rate 가 없고 초록·`Table S7` 이 0.2 C 라 한다:
  - LNO-600: 초기 **159.8** → 100 사이클 **144.8 (90.6 %)** → 800 사이클 **136.2 (85.2 %)** (`Table S7`; *우리 산수* 136.2/159.8 = 0.852 ✓).
  - LNO-850: 100 사이클 **106.5 (79.4 %)** → *우리 산수* 초기 ≈134.1 — 그런데 `Table S4` 의 다른 LNO-850 셀은 0.2 C 5회째가 **148.7** 이다 ⇒ **같은 시료 두 셀의 0.2 C 초기값이 ≈15 mAh g⁻¹ 다르다** (600 도 149.2 vs 159.8).
  - LNO-300: 200 사이클 후 *"over 105"* · Bare: `figure-read ≈`85 → 75 (≈50 사이클에서 끝).
- **1 C (`Fig. S28` 안 봄)**: LNO-600, 0.1 C 3회 활성화 후 **350 사이클 88.2 %**.
- **3.9 V vs Li-In (≈4.5 V vs Li) — LNO-600 만** (`Fig. S29` 안 봄 · `Fig. S30` ✅): `figure-read ≈` 0.1 C ≈168 → 0.2 C 첫 ≈148 → 100 사이클 ≈141 · `Table S7` **148.8 → 95.0 %**. ⚠ **이 전압에서 Bare·850 대조 셀이 없다.** 저자도 *"LiNbO₃ exerts intrinsic instability at high cutoff voltage"* 를 언급한다.
- **`Table S7`** — 문헌 비교 25행 + "This work" 4행 (2.5–4.5/0.2C 148.8 · 95.0 %/100 · 2.5–4.2/0.2C 159.8 · 90.6 %/100 · 같은 셀 85.2 %/800 · 2.5–4.2/0.5C 117.4 · 92.1 %/35). `Fig. 6f` 는 그 표를 3D 산점도로 그린 홍보 그림이다 (셀 조건이 다른 문헌을 한 축에 놓는다).

### 3i. GITT — "계면 D_Li⁺" (`Fig. S32` ✅ · `Fig. S31` 안 봄)

- 0.1 C · **60 °C** (다른 시험은 전부 상온) · τ = 600 s (휴지 시간 미기재) · Fick 식 `D = (4/πτ)(m_B V_M / M_B S)²(ΔE_s/ΔE_t)²` · **V_M = 38.37 cm³ mol⁻¹** · M_B = 96.9301 g mol⁻¹ · **S = 0.785 cm²**.
- `figure-read ≈` (`Fig. S32`): 탈리튬 3.2–3.65 V 평탄 log D **LNO-600 ≈ −8.1 · LNO-850 ≈ −8.15 · LNO-300 ≈ −8.27** (cm² s⁻¹) · 3.0 V 근처 ≈ −9.0 으로 패임 · 리튬화 끝 (2.6–2.7 V) ≈ −10.8. **시료 간 차는 0.1–0.2 decade.**
- 🔎 *우리 산수*: ① NCM622 결정 몰부피는 M 96.93 g mol⁻¹ · a ≈2.868 · c ≈14.21 Å (**전형값 가정** · Z = 3) 로 **≈20.3 cm³ mol⁻¹** — 논문 V_M 38.37 은 **≈1.9 배**이고 D ∝ V_M² 라 **절대 D 가 ≈3.6 배 부풀었다** (세 시료에 같은 배율이라 순위는 안 바뀐다) ② S = 0.785 cm² = **지름 10 mm 원의 기하 면적** — 실제 NCM/LPSC 접촉 면적이 아니다 (D ∝ 1/S²) ③ GITT 는 **"계면" D 를 분리하지 못한다** — 복합양극 전체의 겉보기 값이다.

### 3j. 사이클 후 XPS — 분해 산물 (`Fig. 6c,e` ✅ · `Fig. S33` 안 봄)

- **띠 위치 (`Fig. 6e`, `figure-read ≈`)**: SOx **≈168.0** (본문 168.0 ✓) · **P–S–P ≈162.4** (본문 162.4 ✓) · **P–S–Li ≈161.5** · **S²⁻ ≈160.4 eV**. ⚠ 본문은 *"the main peaks at **160.4** and 162.4 eV correspond to **P-S-Li** unit (cyan) and P-S-P unit (yellow)"* 라 쓰고 몇 줄 뒤 *"S²⁻ signal (green) at **160.4** eV"* 라 쓴다 — **160.4 를 두 번 배정**했다. 그림대로면 P–S–Li ≈161.5 다.
- **시료별 (`figure-read`)**:
  - **LNO-600** — S 2p 는 P–S–Li 주봉 + P–S–P 어깨 · SOx 미량. P 2p 도 P–S–Li 주봉 (≈132.3).
  - **LNO-300** — P–S–Li 주봉이지만 P–S–P 가 600 보다 크다 (본문 *"less proportion of P-S-P signal in NCM@LNO-600"* ✓) · SOx 미량.
  - **LNO-850** — **P–S–P 가 주봉 · S²⁻ 가 크다 · SOx 가 가장 크다.** 본문 *"the P-S-Li unit … is invisible"* ↔ 그림엔 **작은 P–S–Li 성분이 맞춰져 있다**. P 2p 는 맞춘 성분들이 표지 띠보다 **≈1 eV 낮은 쪽**에 놓여 있다 — 저자는 이것을 *"most evident shift toward lower binding energy"* (SCL) 로 읽는데, **"이동한 P–S–P" 와 "이동 안 한 P–S–Li" 를 가르는 기준이 없다.**
- **식 (5) / `Fig. 6c`**: `2 Li₃PS₄ (단위) → Li₄P₂S₇ (단위) + Li₂S (단위)` — **전자 이동이 없는 축합 (condensation) 반응**이다. 저자는 S²⁻ 성분을 이 반응의 **Li₂S** 로 읽는다.
  - ⚠ 그런데 **S²⁻ 는 아지로다이트 자체의 자유 S²⁻ 자리에도 있다** — 저자 자신의 `Fig. 2` 가 사이클 전 LPSC 의 S²⁻ 를 161.0 eV 로 배정한다. 사이클 후 S²⁻ 를 Li₂S 로만 읽을 근거가 논문 안에 없다 (Raman `Table S6` 의 Li₂S 372 cm⁻¹ 도 operando 에서 표시되지 않는다).
  - 우리 grand-potential 로 보면 이 창 (2.5–4.2 V vs Li) 에서 **Li₂S 는 평형상이 아니다** (§7a).
- Co 2p · Mn 2p (`Fig. S33` 안 봄): LNO-850 만 사이클 후 이동 → *"serious parasitic reactions and formation of metal sulfide"* (ref [39]).

### 3k. ⁷Li NMR (`Fig. S15` ✅)

- 본문: *"The width of the peak represents the capability of Li⁺ transfer across the interface, where SCL should be dominant [6]"* · *"NCM@LNO-600 sample delivers the **widest** peak"* → 교환 속도가 *"a little higher"*.
- `figure-read`: 세 곡선이 **≈0.2 ppm 에서 거의 완전히 겹친다** (반치폭 ≈1 ppm). 인셋 (−2…2 ppm) 의 화살표가 가리키는 왼쪽 어깨에서 **LNO-600 (청록) 이 오히려 안쪽 (좁은 쪽)** 에 있다.
- 🔴 ① 1D ⁷Li 선폭은 보통 **움직임이 빠를수록 좁아진다** (motional narrowing) — "넓을수록 교환이 빠르다" 는 2D 교환 (EXSY) 같은 설계 없이 성립하지 않는다 ② 근거로 단 **ref [6] = Haruyama 2014 는 NMR 이 없는 DFT 논문**이다 ③ NMR 실험 조건 (자기장·MAS·기준) 이 Methods 에 없다 ④ 표기 "Li7NMR" (⁷Li NMR).

---

## 4. 방법 — 실험 조건 전수 + DFT/계산 방법 ★

### 4a. 실험 조건 (SI §1)

| 항목 | 값 |
|---|---|
| LPSC 합성 | Li₂S (99.9 %, Thermo) : P₂S₅ (99 %, Sigma) : LiCl (99.99 %, Sigma) = **5 : 1 : 2 mol** · ZrO₂ 볼밀 **600 rpm 10 h** · **550 °C 6 h** (5 °C min⁻¹) |
| 전도도 펠릿 | LPSC **200 mg · Ø14 mm · 200 MPa 5 min** 냉간압착 (두께 미기재 — §3b 검산) |
| 코팅 | 리튬 에톡사이드 (1 M in EtOH, Aladdin) + 니오븀 에톡사이드 (99.999 %, Alfa Aesar) 를 무수 에탄올에 녹여 **유동층 코팅기 (Powrex MP-01D)** 로 NCM622 에 증착 → **공기 중 300 / 600 / 850 °C 3 h**. "Bare" = 건조 (desiccation) 만 |
| 셀 | PEEK 셀 · SE LPSC **150 mg** · 복합양극 70 : 25 : 5 (막자) · **300 MPa** 냉간압착 · 적재 ≈6.2 mg cm⁻² · Li-In 을 대극 겸 기준극으로 압착 |
| 전기화학 | LAND · 상온 · 1 C = 180 mA g⁻¹ · CV 0.05–1.0 mV s⁻¹ · EIS Autolab 10 mV 1 MHz–0.1 Hz · GITT 0.1 C **60 °C** τ 600 s |
| 분석 | TEM/HRTEM JEM-2100F · XRD Rigaku Ultima IV (Cu Kα, 10–80°) · Rietveld GSAS · XPS Thermo ESCALAB250 · Raman Renishaw inVia Qontor |
| **빠진 것** | **LNO 함량 (wt%)** · **사이클 중 적층압** · 셀 지름 (GITT S 로 보아 10 mm 추정) · XPS 스퍼터·보정·무대기 이송 · Raman 레이저·격자·광학창 · NMR 조건 전부 · GITT 휴지 시간 · **셀 반복 수·오차막대 (전 그림 단일 곡선)** |

### 4b. DFT/계산 방법 ★ — 전수 (SI §1.5)

| 항목 | 값 (원문) |
|---|---|
| code | **VASP** (PAW, ref Kresse & Joubert 1999). 버전 미기재 |
| functional | **PBE** + **DFT-D3** (Grimme 2010) |
| DFT+U | Ni · Co · Mn d — **U = 6.88 / 5.95 / 5.2 eV** (원문 순서 "Ni, Co, an Mn", 출처 Longo 2016 *J. Phys. Chem. C* 120, 8540). Nb 에는 없음 |
| 스핀·자기 질서 | ⛔ **미기재** (U 를 건 Ni/Co/Mn 계인데 스핀 분극·자기 배열 언급 0) |
| ecut | **450 eV** |
| k-points | **1×1×1 (Γ only)** — 이완·PDOS 모두 (PDOS 용 조밀 격자 언급 없음) |
| 수렴 | 전자 **1×10⁻⁵ eV** · 이온 **0.03 eV/Å** |
| 진공 | 슬랩에 수직으로 **15 Å** |
| 쌍극자 보정 | ⛔ **미기재** (두 물질 비대칭 슬랩 + 진공인데) |
| 계면 셀 | **LNO(1-10)/LPSC(100)**: Li 74 · Nb 36 · O 108 · P 8 · S 38 · Cl 8 = **272 원자** · **LNO(1-10)/NCM(110)**: Li 84 · Nb 36 · O 204 · Co 9 · Mn 9 · Ni 30 = **372** · **NCM(110)/LPSC(100)**: Li 86 · Co 9 · Mn 9 · Ni 30 · O 96 · P 8 · S 38 · Cl 8 = **284** |
| 면 선택 근거 | NCM (110) = ⟨110⟩ Li 경로 (Van der Ven 2001) · LNO (1-10) = *"preferable choice for the stable heterojunction structures with NCM and LPSC"* (근거로 **Haruyama 2014** — 그 논문은 NCM·LPSC 가 아니라 LCO·β-LPS 다) · LPSC (100) = 입방 대칭 Li 경로 (Cheng 2017 · Wu 2018) |
| 횡방향 셀·변형·층수·종단·정합 표본 | ⛔ **전부 미기재** (Haruyama 2014 는 정합 16 / 4 / 9 개를 이완해 최저를 골랐다) |
| 무질서 처리 | ⛔ **미기재** — LPSC 의 Li 부분점유 · S/Cl 자리 무질서를 어떻게 정했는지 없다 → 단일 배열로 읽힌다 |
| 결함 | 중성 Li 공공, 자리당 **1개**, 영역당 1자리 (P1–P3) · μ_Li = Li 금속 |
| 후처리 | PDOS (원소/영역 투영) · 구조 그림. **NEB · Bader · COHP · ELF · 정전 퍼텐셜 프로파일 · 띠 정렬 · grand-potential 0회** |
| 구조 공개 | ⛔ 없음 (*"upon reasonable request"*) |

### 4c. 🔎 우리 감사 — SI 원자수로 한 전하 산수 (*우리 산수* · 논문 미언급)

형식 산화수 Li⁺ · Nb⁵⁺ · P⁵⁺ · O²⁻ · S²⁻ · Cl⁻ 로 SI 의 원자수를 세면:

| 셀 | 고정 이온 합 | 결론 |
|---|---|---|
| **LNO/LPSC** (272) | 양 +74 +180 +40 = **+294** · 음 −216 −76 −8 = **−300** | **형식 전하 −6** — 산화·환원될 양이온이 없으니 **정공 6개가 음이온 (S 3p / O 2p) 에 들어간다** |
| **NCM/LPSC** (284) | TM 을 빼면 −150 → **TM 평균 +3.125** 필요 | LiTMO₂ 의 +3.000 보다 0.125 높다 = NCM 이 **형식상 Li₀.₈₇₅ 만큼 미리 산화** (정공 6개가 Ni 로) |
| **LNO/NCM** (372) | TM 평균 **+3.000** | 화학량론 ✓ |

- 원인은 **LPSC 부분이 Li₃₈P₈S₃₈Cl₈** 이라는 것이다 — Li₆PS₅Cl 8 화학식 (Li₄₈P₈S₄₀Cl₈) 보다 **Li 10개 · S 2개가 적다**. 두 LPSC 계면이 똑같이 그렇다.
- 이것이 건드리는 것: ① **LNO/LPSC PDOS 의 "갭 축소 · E_F 상태"** — 정공이 있으면 E_F 는 LPSC VB 안으로 들어간다 (SI 가 "표면상태·PN 접합" 으로 돌린 현상의 더 간단한 원인 후보) ② **NCM/LPSC 의 "E_F 의 높은 TDOS"** — 형식상 이미 산화된 NCM 은 금속성이다 (탈리튬 NCM 이 전자 전도체라는 실측은 `asano2017` §7c) ③ **E_v 절대값** — 공통 페르미 준위가 정공 때문에 옮겨 간다. 자리 간 차 (ΔE_v) 는 같은 셀 안이라 덜 흔들리지만 0 은 아니다.
- ⚠ 이것은 **형식 산화수 셈**이다. 실제 전자 분포 (예: S–S 결합 형성으로 정공이 짝지어 사라지는 경우) 는 구조 파일 없이 판정할 수 없다. **"계산이 틀렸다" 가 아니라 "화학량론이 선언되지 않았고, 세어 보면 맞지 않는다"** 까지가 우리 주장이다.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a | 합성 모식: 건조 → 에톡사이드 코팅 → 열처리 · bare 계면에 P₂S₇⁴⁻·Li₂S, 코팅 계면에 PS₄³⁻ 유지 | 저자 가설의 그림판 — 증거 아님 |
| 1b–e | LNO-600 TEM (**"20 nm" 라벨 두 곳**) · HRTEM d₀₁₂ 0.375 (LNO) / d₀₀₃ 0.478 nm (NCM) · EDS 균일 | ✅ 실독. **두께 배정이 본문 첫 문장과 반대** (§3a) — 인용 시 그림 라벨을 쓴다 |
| 1f–h | XPS Nb 3d (Bul. 206.2 / Int. 205.7) · O 1s (CO₃²⁻ 531.0 · 528.6) · Ni 2p (850 에서 +0.3 eV) | ✅ 실독. **CO₃²⁻ 가 열처리 온도와 함께 커진다** (`figure-read`) — 850 의 교락 변수 |
| 2a–d | LPSC 결정 구조 (VESTA 식 그림) | 정보 없음 |
| 2e,f | LPSC EIS 20–80 °C · Arrhenius Ea 0.259 eV | ✅ 실독. 30 °C 2.995 mS cm⁻¹ · 오차막대가 가로 방향 |
| 2g | BEF 모식 (NCM · NCM@LNO · NCM-Nb) | 모식 — 축·값 없음 |
| 2h–l | S 2p, 계면 0 nm / 차표면 <3 nm, 다섯 시료 | ✅ 실독. ΔE₁ ≈0.3–0.4 · ΔE₂ ≈0.5–0.6 eV (`figure-read`). 복합체에서 "계면으로부터 깊이" 정의 불가 (§10-⑥) |
| 3a,d,g | 세 계면 구조 + 공공 자리 P1–P3 | ✅ 실독. 자리 위치 확인 · 구조 비공개 |
| 3b,e,h | 자리별 E_v (3.702/3.932/3.739 · 3.643/3.742/3.254 · 2.165/2.904/2.825) | ✅ 실독. **세로축 눈금 없음** · LNO/LPSC P1→P2 0.739 eV 미논의 · 우리 SCL 표의 아지로다이트 행 후보 |
| 3c,f,i | 세 계면 PDOS (Γ only) | ✅ 실독. LPSC VBM ≈ E_F (f) · **LNO CB 가 E_F 바로 위 (i)** · 정공 6 개 교락 (§4c) |
| 4a | 셀 모식 (고정틀 · PEEK · Li-In) | 적층압 값 없음 |
| 4b,c | 사이클 후 Nyquist (600: 정점 37 Hz · 850: 720 Hz) · Bode (139 / 1400 Hz) | ✅ 실독. **식 (1) 은 R_s+(R‖C) 항등식** — 138 vs 139 Hz 로 재현 (§3e) |
| 4d–f | CV 0.05–1 mV s⁻¹ (600 · 850) · b 0.464 / 0.653 | ✅ 실독. 600 산화쪽 봉우리 없음 (꼭짓점 전류) · 850 전류 2.5–3 배 |
| 4g–i | Dunn 용량성 분해 (0.5 mV s⁻¹) · 비율 막대 | ✅ 실독. 850 ≈43 → 94 % — 이중층으로 설명 불가한 크기 |
| 5a | operando Raman 모식 + "Uncontrolled / Controlled SCL" 만화 | 만화 — 증거 아님 |
| 5b–m | 422 cm⁻¹ 등고선 · 위치 계단 (300 / 600 / 850) · 전압 곡선 (vs Li⁺/Li) | ✅ 실독. ≈1 cm⁻¹ 계단 · 600 만 가역 · "LNO-300 세기 낮음" 은 그림과 안 맞음 |
| 6a | 첫 충방전 0.05 C (효율 81.3 / 81.4 / 80.7 / 76.4 %) | ✅ 실독. 효율 우위는 없다 — 용량 우위 |
| 6b | 율속 0.1–1 C | ✅ 실독. `Table S4` 와 0.5 C 근처 순위 반대 |
| 6c | 축합 반응 2 Li₃PS₄ → Li₄P₂S₇ + Li₂S 모식 | 비산화환원 반응 · Li₂S 는 우리 창에서 평형상 아님 (§7a) |
| 6d | 장기 사이클 (600: 800 사이클) · 쿨롱효율 | ✅ 실독. 캡션에 C-rate 없음 (본문 0.2 C) |
| 6e | 사이클 후 S 2p · P 2p (SOx · P–S–P · P–S–Li · S²⁻) | ✅ 실독. **우리 창의 CEI 산물 클래스 실측** — P–S–P 는 우리 P₂S₇ 예측과 같은 클래스 |
| 6f | 문헌 대비 3D 산점도 | 조건이 다른 셀을 한 축에 — 쓰지 않는다 |
| S1 | XRD (코팅 / 열처리 bare) | (안 봄) `Table S1` 로 대체 |
| S2 | SEM 입도 | (안 봄) |
| S3 | LNO-300 TEM **"7 / 6 / 7 nm"** · HRTEM | ✅ 실독. 두께 배정 판정 근거 |
| S4, S5 | LNO-850 · Bare TEM (코팅 없음) | (안 봄) |
| S6, S7 | LNO-850 EDS 선분석 · Co/Mn 2p · 깊이 30/60 nm Nb 없음 | (안 봄) |
| S8, S9 | LPSC XRD · SEM/EDS | (안 봄) |
| S10, S11, S12 | 복합양극 SEM/EDS (300 / 600 / 850) | (안 봄) |
| S13 | P 2p 계면 / 차표면 (ΔE₁ · "ΔE₄") | (안 봄) "ΔE₄" 정의 없음 |
| S14 | Ni/Co/Mn 2p 복합양극 — 시료 간 불변 | (안 봄) XPS 내부 기준 논거 |
| S15 | ⁷Li NMR 세 시료 | ✅ 실독. 세 곡선 겹침 · "LNO-600 최대 폭" 안 보임 |
| S16 | 세 계면 구조 (진공 양끝) · NbO₄S₂ · NbO₄Cl · NiO₄S₂ · CoO₄S 확대 | ✅ 실독. **Nb–S/Nb–Cl 형성 = 반응 신호이기도** · 단일 계면 + 진공 기하 |
| S17 | 사이클 전 EIS 네 시료 | (안 봄) |
| S18 | Bare 사이클 후 EIS (27 / 100 Hz · 원호 ≈425 Ω) | ✅ 실독 |
| S19 | LNO-300 사이클 후 EIS (27 / 100 Hz · 원호 ≈330 Ω) | ✅ 실독. **`Table S5` R_CT 181 Ω 과 불일치** |
| S20 | Bare CV · b 0.629 · 용량성 ≈20 → 80 % | ✅ (p.16 렌더) |
| S21 | 율속 방전곡선 · 분극 · 사이클 · dQ/dV · 작동전압 (300 / 600 / 850) | ✅ 실독 (손 크롭). **850 분극 ≈0.05 V vs ≈0.2 V** — 동역학 최고는 850 |
| S22 | Bare dQ/dV · 작동전압 · 분극 · 사이클 | (안 봄) |
| S23 | LPSC · Li₂S Raman 기준 | (안 봄) |
| S24, S25, S26 | 195 / 270 / 570 cm⁻¹ 위치 추적 (300 / 600 / 850) | (안 봄) |
| S27 | Eg(Mn) ≈600 cm⁻¹ (300 · 600) | (안 봄) |
| S28 | 1 C 350 사이클 88.2 % (600) | (안 봄) 값은 본문 |
| S29 | 3.9 V vs Li-In 충방전 곡선 (600) | (안 봄) |
| S30 | 3.9 V vs Li-In 0.2 C 100 사이클 (600) | ✅ 실독. ≈148 → ≈141 · **대조 셀 없음** |
| S31 | GITT 전압 곡선 60 °C | (안 봄) |
| S32 | GITT log D (탈리튬 / 리튬화) | ✅ 실독. 시료 간 0.1–0.2 decade · V_M 1.9 배 |
| S33 | 사이클 후 Co/Mn 2p | (안 봄) |
| Table S1 | I(003)/I(104) 7 시료 | 전사. 850 = 1.09 |
| Table S2 | 주요 무기 SE σ·Ea 문헌표 | 전사. LPSC [12] 0.33 eV — 본문 "consistent" 와 어긋남 |
| Table S3 | LPSC 펠릿 온도별 R · σ · ln(σT) | 전사. "RT" = 30 °C |
| Table S4 | 네 시료 율·사이클 용량 | 전사. **850 이 0.2 C 유지 · 0.5 C 초기 최고** |
| Table S5 | EIS 맞춤 R | 전사. LNO-300 행이 `Fig. S19` 와 불일치 |
| Table S6 | Raman 봉우리 배정 | 전사 |
| Table S7 | 코팅 양극 + 황화물 셀 문헌 25행 + This work 4행 | 전사. 전압이 vs Li 로 환산돼 있다 (+0.6 V) |

---

## 6. Post-processing ★

- **무엇**: (DFT) 자리별 중성 Li 공공 형성에너지 (μ_Li = Li 금속) · 영역 투영 PDOS (NCM / LNO / LPSC / TDOS) · 계면 다면체 판독 (VESTA 식 그림). (실험) XPS 피크 맞춤 · 회로 맞춤 EIS · Bode 위상 정점 · Dunn b 값 / k₁·k₂ 분해 · Raman 피크 위치 추적 · GITT Fick 식 · Arrhenius.
- **도구**: VASP · Rietveld 는 GSAS · 나머지 (피크 맞춤·회로 맞춤 소프트웨어) 미기재. 그림은 Origin 식.
- **수치화·기록 방식**: E_v 는 **점 위에 숫자를 적은 눈금 없는 그림**뿐 (`Fig. 3b,e,h`) — 표가 없다. ΔE 는 "같은 셀 안 두 자리의 차" 로 정의 (P2 − P3). PDOS 는 셀당 원값 (원자수·면적 정규화 없음). XPS 이동량 ΔE₁·ΔE₂ 는 **숫자로 보고되지 않는다** (그림 화살표뿐 — 이 digest 의 값은 `figure-read`). Raman 위치는 시료별 계단 그림 · 맞춤 불확도 없음.
- ⛔ **하지 않은 것**: 정전 퍼텐셜의 계면 법선 프로파일 · 층별 전하 적분 · 띠 정렬 (vacuum level 기준) · 충전된 결함 형식 · 여러 정합·여러 배열 통계 · NEB · Bader · COHP — **SCL 을 숫자로 만들 수 있는 후처리는 하나도 없다.**

---

## 7. 우리 DFT · 원장 대비 ★ (`../our_dft_baseline.md` · `db/properties/`)

### 7a. 축별 대조

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **A 이온전도** | LPSC 펠릿 실측 **σ(30 °C) 2.995 mS cm⁻¹** · **Ea 0.259 eV** (EIS 20–80 °C) | comp1 **Ea 0.253 eV** (MLIP-MD UMA-s-1p1 · 600/800/1000 K · 단일 궤적) | **다른 양** — 펠릿 (입계·기공 포함) 실온 근처 vs 벌크 MLIP 고온 외삽. 숫자가 가까운 것을 일치로 쓰지 않는다 |
| **B① 산화 개시** | 셀 창 2.5–4.2 V vs Li 전체에서 SE 분해 산물 관측 (P–S–P · SOx · S²⁻) | comp1 **2.256 V** (GG 상집합 · grand-potential 경계의 Li-rich facet 값 · LiS₄ 포함 시 2.14 V) — 우리 hull 에서 이 개시는 **Li₂S 산화 전위**다 (E2b 진단) | **방향 일치**: 창 전체가 열역학적 산화 구간이다 ⇒ 코팅의 역할은 "분해 금지" 가 아니라 **접촉·속도 제한** (우리 2.5–4.25 V 창 규칙과 같은 읽기) |
| **B② 산물 클래스** | 식 (5) 축합 `2 Li₃PS₄ → Li₄P₂S₇ + Li₂S` (비산화환원) · SOx 168 eV | 창 안 평형: **2.385 V 부터 P₂S₇ + S** (P–S–P 다리) · **3.326 V SCl** · Li₂S 는 2.256 V 위에서 산화된다 | **P–S–P = 우리 P₂S₇ 예측과 같은 클래스 ✓** · **Li₂S 귀속은 창 안 평형과 어긋나고** 아지로다이트 자유 S²⁻ 와 구분도 안 된다 · SOx 는 **양극 O 경로** (우리 O-열림 grand-potential `cei_esw_O_2026_09_16.json` 축) |
| **B③ 계면 반응** | DFT: NCM/LPSC 에 NiO₄S₂·CoO₄S (S 가 TM 에 결합) · LNO/LPSC 에 NbO₄S₂·NbO₄Cl | comp1\|LiCoO₂ 닫힌계 반응 **−0.3227 eV/atom** (산물 Co₉S₈ · Li₂SO₄ · Li₃PO₄ · Li₂S · LiCl) · cascade 축 ① (NCM 대리 LiNiO₂, `cascade_axis_ncm_interface_estimand_2026_11_04.json`) | 정성 일치 (TM–S 결합 = TM 황화물 경향). 저자의 정적 이완 1 개 대 우리 hull 반응에너지 — **다른 양** |
| **D 전자구조** | 계면 슬랩 PDOS (PBE+U+D3 · Γ only) — 세 계면 모두 갭 축소 · E_F 상태 | comp1 **bulk gap 2.066 eV** (PBE · fixed-occ nscf) | **비교 불가** — 계면 vs 벌크 · U · Γ only · 비화학량론 (§4c). 이 PDOS 로는 "넓은 갭" 수준도 말할 수 없다 |
| **C 기계** | Raman 피크 이동 = "응력" (정성 · GPa 없음) | comp1 E_VRH 22.06 · B₀ 26.23 GPa | **비교 불가** — 탄성값 없음 |
| **계면 계산 기하** | 단일 계면 + 진공 15 Å (`Fig. S16`) · 정합 1 · Γ · D3 · 쌍극자 보정 미기재 · **LPSC 부분 비화학량론** | 우리 v5 single-interface + vacuum (원전 Haruyama 2014 · `refs.json[37]`) | 기하 계통은 같다 ✓ (anti-sandwich). 차이는 화학량론 선언 · 정합 표본 · 쌍극자 처리 |
| **SCL 정량** | **없음** (두께·전위·전하·Debye 0) · 자리별 E_v 9 개 | **없음** (`computational_methods_canonical.md` §2: *"공간전하층을 계산했다고 쓰지 않는다"*) | 이 논문도 원전과 같은 상태 — 그 표에 **"아지로다이트 E_v 9자리 (Chen 2024)"** 를 출처 하나로 더할 수 있다 (§7b) |
| **작동창** | 1.9–3.6 V vs Li-In = **2.5–4.2 V vs Li** (논문 환산) | **2.5–4.25 V vs Li** (사용자 2026-11-09) | **같은 창** — 이 논문 산물 표는 우리 CEI 판단 창의 실측 사례다. 3.9 V vs Li-In (4.5 V vs Li) 결과만 창 밖 |

> ⛔ **E_v (V 단위로 읽힘) 를 우리 2.256 V 옆에 놓지 않는다.** E_v 는 "전자를 NCM 의 페르미 준위에 두고 한 자리에서 Li 하나를 뺄 때의 국소 에너지" 이고, 우리 값은 "벌크 LPSC 가 분해되기 시작하는 평형 경계" 다. NCM/LPSC 의 LPSC 차표면 3.254 eV 가 우리 값보다 1 V 높은 것은 **양이 달라서**지 어느 쪽이 틀려서가 아니다.

### 7b. `computational_methods_canonical.md` "SCL 정량" 표에 대한 제안 (⛔ 이 digest 는 kb 를 고치지 않는다 — 제안만)

| 양 | 우리 상태 | 문헌 상태 (현재 → 제안) |
|---|---|---|
| SCL 두께 · 전위 · 전하 · Debye 길이 | 없음 | 원전에도 없음 → **Chen 2024 에도 없음** (원전 둘 다 정량 0) |
| 계면 Li 공공 형성에너지 (자리별) | 미계산 | Haruyama 2014 21 자리 → **+ Chen 2024 9 자리 (아지로다이트 · NCM622)** — 단 LPSC 부분 비화학량론 (§4c) · 자리 편차는 계면당 SE 쪽 2 자리뿐 |

### 7c. 가까운 digest 와 겹치는 것 · 어긋나는 것

| digest | 겹치는 것 | 어긋나는 것 |
|---|---|---|
| **`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`** | 같은 E_v 정의 (μ_Li = Li 금속) · 같은 "세 계면" 설계 · 같은 LNO (1-10) 면 · 같은 밴드 오프셋 설명 (LNO 쪽 E_v 가 벌크와 다른 이유) · 같은 결론 방향 (버퍼가 SE 쪽 자리 차를 줄인다: Haruyama 1.83 → 0.76 eV / Chen 0.488 → 0.079 eV *우리 산수*) · 단일 계면 + 진공 · 계면 Γ only | ① **LNO/SE 결합**: Haruyama LNO/β-LPS 는 *Nb–S 결합 없음* — Chen LNO/LPSC 는 **NbO₄S₂ · NbO₄Cl 형성** ② **LNO/SE 계면 E_v 순서가 반대**: Haruyama LNO 쪽 3.13–3.32 > LPS 쪽 2.42–3.18 / Chen LNO 쪽 **2.165** < LPSC 쪽 2.83–2.90 ③ 표본: Haruyama 21 자리 · 정합 16/4/9 / Chen 9 자리 · 정합 1 ④ 스핀: Haruyama spin-unpolarized **명시** / Chen 미기재 ⑤ 양극/SE 낙폭: Haruyama 벌크 대비 −1.76 eV (LP2) / Chen 자리 간 0.488 eV — 정의가 달라 크기 비교 불가 ⑥ 화학량론: Haruyama 는 화학량론 종단 슬랩을 명시 / Chen 은 LPSC 부분이 맞지 않는다 |
| **`cha2024_dualcompatible_halide_ncm_lpscl_interface`** (우리 그룹) | 같은 질문 (NCM–LPSCl 사이 8–20 nm 코팅) · 같은 무대 (Ni-rich NCM + Li₆PS₅Cl) · 계면저항 하락을 성능과 엮는다 | **기전 언어가 다르다** — Cha = **화학 호환 ("dual compatibility", 부반응 억제)** / Chen = SCL. Chen 의 자기 데이터 (LNO-850: R_CT 최저인데 SOx·P–S–P 최다·가장 빨리 열화) 는 **Cha 식 화학 호환 틀로 더 잘 읽힌다** |
| **`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`** | LNO 코팅 층상 양극 + 황화물 복합양극 · 전자 경로 문제 | Chen 은 NCM/LPSC 의 "E_F 의 높은 TDOS" 를 **계면** 전자전도의 근거로 쓴다. 그런데 이 계산의 NCM 은 형식상 이미 산화돼 있고 (§4c) **탈리튬 NCM 자체가 전자 전도체**라는 것이 Asano 실측 (SOC 50 % 에서 σ_e 26–45 배 ↑) ⇒ "E_F 의 TDOS" 는 계면 성질이 아니라 **양극 벌크 성질**일 수 있다 |
| **`doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density`** | LNO 코팅 NMC + LPSCl · 첫 효율·초기 용량 보고 | 수치 비교 금지 (NMC83 단결정 vs NCM622 다결정 · 압밀 500 vs 300 MPa). 그리고 Doerrer 는 **압밀·입자 기계·적층압**을 성능 변수로 세우는데 Chen 은 적층압조차 안 적는다 — Chen 의 Raman "응력" 서사는 그 통제 없이 나온다 |
| `bong2023_linbo3_thickness_uniformity_ncm523` | LNO 두께 ↑ → 내구성 ↑ (Bong 은 두께·균일도 3 단계 단조) | Bong 은 **"보호 = SE 산화 억제" 가 성능을 설명 못 한다**는 반례 (첫 단계 셀이 무코팅보다 SE 산물이 더 많은데 성능은 좋다) — Chen 처럼 "산물 감소 → 성능" 을 충분조건으로 쓰면 안 된다 |
| `wei2023_linbo3_coating_cutoff_voltage_lco_argyrodite` | 같은 3.6 V vs Li-In 창 · LNO 코팅 · 아지로다이트 | Wei (LCO · ≈3 nm 비정질 LNO) 는 3.6 V 에서 **고율에서만** 이득 / Chen (NCM622) 은 0.05 C 에서도 bare 123 vs 코팅 158–171 mAh g⁻¹. 양극이 달라 모순은 아니지만, Chen 의 "Bare" 는 건조만 한 시료라 bare 열세가 계면만의 효과인지 불명 |
| `nisar2021_cathode_coating_review_critical_thickness` | 코팅 두께 ↔ Li 수송 시간 논증 | 그 digest 의 표 (Rahn 2015 · 단결정 LiNbO₃ 자기확산 · 423 K) 대로면 **결정성 LiNbO₃ 10 nm 통과에 수백 년** — Chen 은 결정성 LNO-600 을 *"high Li⁺ conductivity"* 라 부르는데 측정이 없다. 결정성 20 nm 층을 Li 가 실제로 무엇으로 통과하는지 (입계 · 비정질 잔여 · 불연속 피복) 를 묻지 않는다 |

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

- ① **작동창 판단의 실례 하나 더**: 우리 창 (2.5–4.25 V vs Li) 과 같은 창에서 코팅 유무가 가르는 것은 **분해 유무가 아니라 산물 클래스** (P–S–Li 유지 vs P–S–P 우세 + SOx) 와 **그 속도**다. 우리 `cei_interface_V` (4.00 / 4.50 V) 와 O-열림 grand-potential 의 산물 표가 바로 그 클래스를 예측하는 축이다 — 이 논문 `Fig. 6e` 가 대조 사례다.
- ② **우리가 계면 E_v 를 할 날을 위한 체크리스트** (이 논문이 반면교사): ⓐ 원자수로 **형식 전하를 먼저 센다** (정공·전자 0 인지) ⓑ 스핀·자기 배열 선언 ⓒ 쌍극자 보정 ⓓ 정합 여러 개 + 최저 채택 ⓔ SE 쪽 자리 **여러 개 → 편차** (평균 말고) ⓕ PDOS 는 원자수 정규화 + 조밀 k ⓖ 구조 파일 공개. 이 일곱 줄이면 이 논문의 계산 비판 대부분을 미리 막는다.
- ③ **싼 확인 하나 (새 DFT 없이)**: `Fig. S16c` 의 Nb–S · Nb–Cl 결합이 열역학적으로 밀리는지는 우리 MP 기반 닫힌계 반응 도구 (`tools/cascade/cathode_reactivity.py` 계열 — 양극 대신 LiNbO₃ 를 짝으로) 로 LiNbO₃\|Li₆PS₅Cl 반응에너지를 내면 갈린다. ⚠ 제안이지 실행 승인 아님 — 결과 전 보고량 카드부터.
- ④ **EIS 를 읽을 때**: "Nyquist 정점 ≠ Bode 정점 = 특별한 용량 효과" 라는 주장은 **R_s 를 넣어 항등식부터 확인**한다 (§3e — 이 논문은 1 Hz 단위까지 항등식으로 재현된다).
- ⑤ **GITT·Dunn 함정 두 개를 기억해 둔다**: V_M·S (기하 면적) 를 확인하지 않은 D 는 절대값으로 쓰지 않는다 · 느린 주사에서 "용량성 수십 %" 는 분해법의 인공물을 먼저 의심한다.
- ⑥ **CEI 트랙 (Nd 계면) 원고에서 이 논문을 인용한다면 역할은 둘뿐이다**: "LNO 코팅 NCM622 \| Li₆PS₅Cl 셀이 우리와 같은 창에서 이렇게 돌았다" (실험 사례) · "SCL 이 제안된 기전이다" (현상). **SCL 정량 근거로는 쓰지 않는다.**

---

## 9. 인용 가능 문장 (deck/paper 용 · 영문 초안)

- "LiNbO₃-coated NCM622 annealed at 600 °C retained 90.6% of its capacity (144.8 mAh g⁻¹) after 100 cycles at 0.2 C in Li₆PS₅Cl-based cells cycled between 1.9 and 3.6 V vs Li–In (*Adv. Energy Mater.*, 14, 2304443 (2024))."
- "The space-charge layer was invoked to explain this improvement, but its thickness and potential were not quantified; the supporting evidence consisted of XPS binding-energy shifts and DFT Li-vacancy formation energies at three interface models (*Adv. Energy Mater.*, 14, 2304443 (2024))."
- "In the same study, the uncoated Nb-doped surface (850 °C) showed the lowest charge-transfer resistance but the fastest capacity fade, together with more bridging-sulfur (P–S–P) and SOₓ species after cycling (*Adv. Energy Mater.*, 14, 2304443 (2024))."
- ⛔ 쓰지 말 것: *"the space-charge layer thickness was controlled to X nm"* · *"DFT showed that LiNbO₃ is an electronic insulator against Li₆PS₅Cl"* (그 PDOS 는 정공이 든 셀이고 LNO CB 가 E_F 에 붙어 있다) · *"Li₂S forms at the cathode interface"* (S²⁻ 귀속 불확정).

---

## 10. 주의 / 한계 — 비판 (over-claim 방지)

1. **제목·초록이 말하는 SCL 은 한 번도 측정·계산되지 않는다.** 두께 (nm) · 전위 (V) · 층별 전하 · Debye 길이 0. *"in situ inspection and visualization of SCL"* (초록) 의 실체는 PS₄³⁻ Raman 피크 위치 추적이다. ⇒ Haruyama 2014 와 같은 상태 — **SCL 은 이 논문에서도 해석이지 측정량이 아니다.**
2. **동역학과 내구성이 갈리는데 서사는 하나다.** 코팅 없는 850 시료가 R_CT 최저 (11.7 Ω) · 분극 최소 (≈0.05 V @0.2 C) · CV 전류 2.5–3 배 · 0.5 C 초기 용량 최고 (134.1) 다. 저자는 그 빠름을 "용량성 = Li 흡착 자리 = 통제 안 된 SCL" 로 바꿔 읽는다 — **낮은 저항이 SCL 의 증거가 되는 순환**이다. 850 의 몰락은 사이클 후 SOx · P–S–P · TM 2p 이동 (부반응) 과 함께 오므로 **"보호막 없음 → 화학 열화"** 로 충분하다.
3. **코팅 두께 배정이 본문 첫 문장과 그림에서 반대다** (LNO-300 ≈20 · LNO-600 ≈7 nm vs 라벨 LNO-600 "20 nm" · LNO-300 "7/6/7 nm"). "두께로 SCL 을 통제" 하는 논문의 핵심 변수다.
4. **식 (1) 은 R_s + (R‖C) 회로의 항등식이다.** 저자 값으로 LNO-600 을 138 Hz (관측 139 Hz) 로 재현한다 — SCL 용량의 증거가 아니다.
5. **`Table S5` 와 `Fig. S19` 가 안 맞는다** (LNO-300 R_CT 181 Ω vs 원호 ≈310 Ω) · 표의 "R_g" 와 본문 "R₀" 이름이 다르다 · 사이클 후 EIS 의 SOC 문장이 모순 (1.9 V 방전 후 "OCP 3.1 V").
6. **XPS "계면으로부터 0 nm / <3 nm"** 는 무작위 복합체에서 기하적으로 정의되지 않는다. 스퍼터·보정·무대기 이송이 없다. ΔE 크기는 숫자로 보고되지 않는다 (`figure-read` ≈0.3–0.6 eV). 사이클 후 S 2p 에서 160.4 eV 를 두 번 배정했고 · "LNO-850 에서 P–S–Li 가 안 보인다" 는 자기 맞춤과 다르며 · P 2p 의 이동 성분 배정 기준이 없다 · "ΔE₄" 는 정의가 없다.
7. **DFT 의 화학량론**: LPSC 부분 Li₃₈P₈S₃₈Cl₈ → LNO/LPSC 형식 정공 6 · NCM/LPSC TM 평균 +3.125 (*우리 산수* §4c). SI 가 "표면상태 · PN 접합" 으로 돌린 갭 축소 · E_F 상태의 더 간단한 원인 후보다.
8. **DFT 의 나머지**: Γ only 로 이완과 PDOS · 스핀·자기 배열 미기재 · 쌍극자 보정 미기재 · 정합 1 개 · 영역당 공공 1 자리 · LPSC 무질서 처리 미기재 · E_v 그림에 눈금 없음 · TDOS(E_F) 를 원자수 다른 셀 사이에서 정규화 없이 비교 · LNO/LPSC 의 P1→P2 0.739 eV (가장 큰 단차) 미논의 · `Fig. 3i` 에서 LNO 전도대가 E_F 에 붙어 있어 *"electronic insulator"* 와 긴장 · 구조 비공개 (P2 배위 미확인) · LNO (1-10) 선택 근거로 LCO/β-LPS 논문을 인용.
9. **Dunn 분해의 과용**: LNO-600 은 산화쪽 봉우리가 없어 b 값이 꼭짓점 전류에 기댈 수 있고 · 고속 점이 직선 아래로 휜다 (저항 제한) · 850 의 "용량성 43 % @0.05 mV s⁻¹" 는 이중층으로 불가능한 크기 → k₁v 항은 부반응·오믹 왜곡을 받는다.
10. **Raman**: 위치가 ≈1 cm⁻¹ 계단 (분해능 근처) · 맞춤 불확도 없음 · cm⁻¹/GPa 계수 없음 · 레이저·광학창 미기재 · "LNO-300 세기 낮음 (`Fig. 5b`)" 은 그림과 안 맞는다 (가장 약한 것은 850).
11. **⁷Li NMR**: "넓을수록 교환 빠름" 은 1D 스펙트럼에서 성립하지 않고 (운동 좁아짐) · 그림에 차이가 거의 없으며 · 근거 ref [6] 은 NMR 없는 DFT 논문이다.
12. **GITT**: V_M 이 NCM622 결정 몰부피의 ≈1.9 배 (D ≈3.6 배 과대) · S 는 기하 면적 · 60 °C 단독 · 시료 간 차 0.1–0.2 decade 는 단일 셀 산포 안이다 · "계면 D" 를 분리하지 못한다.
13. **850 시료의 교락**: "코팅 없음" 에 **심한 Li/Ni 혼합 (I(003)/I(104) 1.09)** · **Nb 도핑** · **CO₃²⁻ 증가** (`figure-read`) 가 겹친다 — SCL 차이로 귀속할 수 없다.
14. **통계·통제**: 모든 그림이 단일 곡선 (반복 셀·오차막대 0) · 같은 시료 두 셀의 0.2 C 초기값이 ≈10–15 mAh g⁻¹ 다르다 · `Table S4` 와 `Fig. 6b` 의 0.5 C 근처 순위가 반대 · LNO 함량·적층압 미기재 · 3.9 V vs Li-In 시험은 LNO-600 하나 (대조 없음).
15. **전해질 수치**: "RT 2.995 mS cm⁻¹" 은 30 °C 값 · 기술된 펠릿 기하로는 밀도 ≈35 % (*우리 산수* — 펠릿 동일성 가정) · "Ea 가 [12] 와 일치" 인데 자기 `Table S2` 는 [12] 를 0.33 eV 로 싣는다.
16. **결정성 LNO 의 "high Li⁺ conductivity"** 는 측정 없이 단정됐다 (결정성 LiNbO₃ 의 Li 확산이 매우 느리다는 문헌 표는 `nisar2021` §3e 참조).
17. ⚠ **우리 쪽 경계 (공정성)**: 위 2·13 은 대안 해석이지 반증이 아니다 — 이 논문의 데이터로는 **SCL 기여를 0 으로 만들 수도 없다.** 우리가 말할 수 있는 것은 *"SCL 은 필요한 가정이 아니다"* 까지다.

---

## 11. 기법 미니 용어집 (이 digest 를 혼자 읽기 위한)

- **SCL (space-charge layer, 공간전하층)**: 두 고체가 닿을 때 Li⁺ 화학퍼텐셜 차 때문에 Li⁺ 가 한쪽으로 몰리고 반대쪽이 비면서 생기는 **전하가 남은 얇은 층**. 산화물 양극 \| 황화물 SE 에서는 SE 쪽이 Li 결핍이 되어 계면 저항을 키운다는 가설 (Takada · Haruyama).
- **BEF (built-in electric field)**: SCL 의 전하가 만드는 계면 전기장. XPS 에서는 그 영역의 내각 준위가 같은 방향으로 밀려 **결합에너지 이동**으로 나타난다고 읽는다.
- **E_v (Li 공공 형성에너지, μ_Li = Li 금속)**: 한 자리에서 중성 Li 하나를 빼서 Li 금속에 붙일 때의 에너지. 전자가 셀의 페르미 준위에서 빠지므로 **값이 "그 자리의 국소 전압 (V vs Li)"** 처럼 읽힌다. 같은 셀 안 자리끼리의 차는 Li⁺ 자리 선호를, 셀끼리의 차는 전자 저장소 (페르미 준위) 차이를 주로 반영한다.
- **밴드 오프셋**: 두 물질의 VBM (또는 CBM) 높이 차. 코팅이 전자를 막으려면 **VB·CB 양쪽** 오프셋이 다 필요하다.
- **형식 전하 셈**: 원자마다 정해진 산화수 (Li⁺ · P⁵⁺ · S²⁻ …) 를 더해 셀 전체가 0 인지 보는 것. 0 이 아니면 그만큼 정공·전자가 어딘가에 생긴다 — 슬랩 계산의 첫 점검.
- **Γ only (1×1×1 k)**: 브릴루앙 영역에서 한 점만 쓰는 것. 큰 셀이면 에너지는 그럭저럭 맞지만 DOS 는 뾰족해지고 금속성 계에서는 부정확해진다.
- **DFT+U / D3**: 국소 d 전자의 자기상호작용 오차를 U 로 보정 · 분산 (vdW) 힘을 D3 로 더함.
- **쌍극자 보정**: 진공을 둔 비대칭 슬랩은 표면 사이에 인공 전기장이 생긴다 — 그것을 상쇄하는 보정.
- **Nyquist 정점 vs Bode 위상 정점**: R_s + (R‖C) 회로에서 Nyquist 반원 꼭대기는 ω₀ = 1/RC, 위상 최대는 ω₀·√((R_s+R)/R_s) 에서 난다 — **늘 다르다** (식 (1) 이 이것이다).
- **CPE (constant phase element)**: 이상 축전기 대신 쓰는 비이상 용량 요소.
- **b 값 / Dunn 분해**: 봉우리 전류 i ∝ v^b — b = 0.5 확산, 1 표면 (용량성). i = k₁v + k₂v^½ 로 전류를 두 몫으로 가른다. 전고체 복합양극에서는 오믹 강하가 커서 해석이 흔들린다.
- **GITT**: 짧은 전류 펄스 + 휴지를 반복해 전압 응답에서 확산계수를 내는 법. 식에 몰부피 V_M 과 면적 S 가 제곱으로 들어간다.
- **I(003)/I(104)**: 층상 양극 XRD 의 두 회절선 세기비. 낮을수록 Li 층에 Ni 가 섞인다 (양이온 혼합).
- **유동층 코팅**: 공기로 띄운 분말에 전구체 용액을 뿌려 입자마다 고르게 입히는 공정.
- **operando Raman**: 셀이 도는 동안 같은 자리의 라만을 연속 측정. 피크 위치가 압력에 따라 움직이는 성질로 응력을 정성적으로 본다.
- **motional narrowing (운동 좁아짐)**: NMR 에서 원자가 빠르게 움직이면 국소 자기 환경이 평균돼 선이 **좁아지는** 현상.
- **축합 반응 (2 PS₄³⁻ → P₂S₇⁴⁻ + S²⁻)**: 두 PS₄ 사면체가 S 하나를 공유하며 이어지는 반응. 전자가 오가지 않는다 (산화가 아니다). P–S–P 다리 S 가 XPS 에서 PS₄³⁻ 보다 높은 결합에너지에 나온다.

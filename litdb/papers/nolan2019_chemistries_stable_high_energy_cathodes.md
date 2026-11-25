<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-12 신규 작성:
       ① 1저자 지정: "양극 코팅 계산 계보 8편" 세트의 **#4**. #1 aykol2014 / #2 aykol2016 / #3 xiao2019 기존.
       ② 계보 카드(kb/syntheses/cathode_coating_computational_lineage.md)의 핵심 물음
          — "우리 산화 onset 2.256 V 의 계보가 Mo 그룹 본류인가" — 에 **이 편이 직접 답한다**.
          결론: **이 편은 우리 두 양을 *둘 다* 갖고 있다.** 헤드라인 Ed ↔ 우리 `interface_reactivity`(같은 양·같은 구현),
          SI 의 anodic limit ↔ 우리 `2.256 V`(같은 양·같은 계보). 다만 **anodic limit 의 정의를 이 논문은 안 적는다**
          — [Zhu15]/[Zhu16] 로 인용 승계할 뿐이다 (§4c·§7b).
       ③ 크로핑 그림 16장 중 **11장을 실제로 봤다**: 본문 Fig 1·2·3·4·5 전량 + SI Fig S1·S3·S7·S8·S9·S10.
          ⛔ 안 본 것: Fig S2·S4·S5·S6 (전부 같은 Ed 데이터의 다른 표현 — XLSX 원자료로 대체) + Table S1 이미지
          (PDF 텍스트를 좌표로 읽어 4열을 복원했으므로 이미지 불필요). §0 에 명시.
          Fig 2 의 행 라벨은 래스터라 PDF 텍스트가 없어 **700 dpi 로 재크로핑해 확대 판독**했다.
       ④ ★ 이 논문의 진짜 자산은 본문이 아니라 **Sup2 XLSX** 다. 236종 × 8 양극상태 = **1,888 쌍**의
          Ed + 상평형이 통째로 들어 있고, 본 digest 가 그것을 **전수 재분석**해 본문의 정성 주장을
          정량으로 바꿨다(§12). 부수 소득: **8/8 전부 안정한 물질은 단 둘**(Li₂SO₄·BeO)이고,
          Fig 2 의 행 라벨과 XLSX 의 물질 목록이 **전이금속 패널에서 3종 어긋난다**(§10-5).
       ⑤ ⚠ 무대는 **액체/고체를 가리지 않는 '접촉 고체 화학'** 이다 — #1·#2 의 액체 HF 축과 다르고,
          #3 [Xiao19] 의 SSB 축과도 다르다. 황화물·염화물 SE 는 Ed 데이터셋에 **한 종도 없다**(§7d). -->

# Solid-State Chemistries Stable with High-Energy Cathodes for Lithium-Ion Batteries — Nolan, Liu, Mo (*ACS Energy Lett.* **2019**, 4, 2444−2451)

> slug `nolan2019_chemistries_stable_high_energy_cathodes` · DOI `10.1021/acsenergylett.9b01703` · type `DFT 전용 고속 열역학 스크리닝 (Materials Project 에너지 + pseudo-binary 상호분해에너지; 자체 DFT 계산 0 · 자체 실험 0)` · PDF `litdb/inbox/108. Nolan2019_Solid_State_Chemistries_Stable_with_High_Energy_Cathodes.pdf` (본문 8 pp) + `108. Sup) …pdf` (SI 8 pp: Table S1 + Fig S1–S10) + **`108. Sup2) …xlsx`(Supplementary Data — Ed·상평형 1,896행 / 4 시트)** · digested `2026-09-12` · status ✅ · 태그 **[외부]**

> elements: H, Li, Be, B, C, N, O, F, Na, Mg, Al, Si, P, S, Cl, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, As, Se, Rb, Sr, Y, Zr, Nb, Mo, Pd, Ag, Cd, In, Sn, Sb, Te, I, Cs, Ba, La, Ce, Nd, Sm, Eu, Gd, Dy, Ho, Er, Tm, Yb, Lu, Hf, Ta, W, Re, Pt, Au, Tl, Pb, Bi
> methods: DFT, ESW

> **저자**: **Adelaide M. Nolan**, **Yunsheng Liu**, **Yifei Mo\*** (University of Maryland, College Park — MSE + Maryland Energy Innovation Institute; 단일기관 3인) · 수신 2019-08-06 / 수락 2019-09-10 / **출판 2019-09-11** (ASAP) · ⚠ **2019-09-23 에 `Fig. 4` 라벨 오류 정정본이 재출판됨**(논문 말미 "NOTE ADDED AFTER ASAP PUBLICATION") · 지원 DOE-EERE DE-EE0007807 / DE-EE0008858, NSF 1550423 · 계산자원 UMD + MARCC · 계산 프레임 = **Materials Project**(⚠ OQMD 가 아니다)
>
> **계보 (1저자 지정 "양극 코팅 계산 계보" 8편 세트의 #4)**: [Aykol 2014 AENM](aykol2014_cathode_coating_thermodynamics.md)(#1, 액체·HF·닫힌계 ΔH) → [Aykol 2016 Nat Commun](aykol2016_ht_cathode_coating_design.md)(#2, OQMD 13만종·MOOP) → [Xiao 2019 Joule](xiao2019_cathode_coating_screening.md)(#3, SSB 전환) → **본 논문**(#4, **Mo 그룹 본류** — Ed 를 양극 SOC 두 상태에 전수 적용) → Nolan 2021(#5, 가넷) · Honrao 2021(#6, ML) · 리뷰 2편(#7·#8).
> **이 편의 방법 조상**은 Aykol 계열이 아니라 **Zhu/He/Mo** 2015 *ACS AMI* **7**, 23685 [Zhu15] + 2016 *JMCA* **4**, 3253 [Zhu16] 이고, 그 위에 **Mo/Ong/Ceder 2012 grand-potential** 이 있다. ⇒ **우리 `2.256 V` 의 직계 가족이 맞다** (§7b).

---

## 0. 이 digest 를 읽는 법 — 범위부터, 그리고 ★ **이 편은 우리 두 양을 *둘 다* 갖고 있다**

계보 8편 중 **처음으로** 우리 파이프라인의 두 숫자가 한 논문 안에 같이 들어 있다.

| 우리 값 | 이 논문의 대응물 | 어디에 | 같은 양인가 |
|---|---|---|---|
| `interface_reactivity` = **−0.3227 eV/atom** (comp1 vs LiCoO₂) | **E_d** (minimum mutual decomposition energy) | **헤드라인** — 본문 전체·Fig 2–5·Sup2 XLSX | 🟢 **완전히 같은 양.** 같은 식·같은 정규화(eV/atom)·같은 부호·같은 DB(MP)·**같은 구현**(pymatgen `InterfacialReactivity`) |
| `oxidation_limit` = **2.256 V** (grand-potential onset) | **anodic limit** | **SI 만** — `Fig. S7`·`Fig. S9`·`Fig. S10` 의 축, 본문은 "3.5–4 V" 한 문장 | 🟢 **같은 양이지만 이 논문이 정의를 안 적는다** — [Zhu15]/[Zhu16] 인용 승계. 수치는 **그림에서만** 읽힌다 |

⚠ 그래서 이 digest 의 §7 은 *"계보가 확정됐다"* 로 끝나지 않는다. **어느 축에서 확정됐고 어느 축이 아직 간접인지**를 갈라 적는다.

| 가져올 수 있는 것 | 가져오면 안 되는 것 |
|---|---|
| 🟢 **E_d 의 4단 정의**(§4a) — 우리 `interface_reactivity` 의 **문헌 원전**. 지금까지 우리는 이 값을 [Richards16]/pymatgen docstring 으로만 귀속하고 있었다 | 🔴 **그들의 E_d 절대값을 우리 −0.3227 옆에 나란히** — MP hull 세대가 다르고(2019 vs 2026 pinned GGA_GGA+U), 접촉물질이 안 겹친다. **정의 대조까지만** |
| 🟢 **"양극은 한 상태가 아니다"** — 리튬화·탈리튬화 **둘 다** Ed=0 이어야 안정. 우리는 `LiCoO₂` **하나**만 봤다(§7c 의 작업거리 #1) | 🔴 `Fig. S7` 의 **chlorides ≈ 4.3 V** 를 우리 LPSCl 에 쓰기 — 그건 **Li–M–Cl 할라이드**(Li₃YCl₆ 계열, 자매논문 Wang *et al.* Angew 2019)이고 우리 onset 은 **S²⁻ 가 pin** 한다 |
| 🟢 **Li 함량 규칙**(탈리튬 양극은 Li-rich 접촉물질에서 Li 를 뽑아간다) — 본 digest 가 **Pearson r 로 정량**(§12c) | 🔴 본문 "대부분 산화물의 산화한계 **3.5–4 V**" 를 우리 수치로 인용 — 그들 산화물 계 boxplot 의 서술이다 |
| 🟢 **Ed=0 을 8/8 전 상태로 요구했을 때 남는 목록**(§12b) — 본 digest 가 XLSX 에서 뽑은 것으로 **논문에 인쇄돼 있지 않다** | 🔴 `Ed = 0` 을 **부동태화/속도론적 안정**으로 읽기 — 0 K 열역학 불리언이다. 계면 성장·저항은 이 양이 말하지 않는다 |
| 🟢 **Li₃PO₄ · Li₂SO₄ 의 양극 양립성** — 우리 LPSCl\|LiCoO₂ 계면 **산물 5종 중 2종**이 정확히 이 둘이다(§7c 의 🔑) | 🔴 `Table S1` 중 **XLSX 에 없는 8종**(LiClO₄·Li₅IO₆·LiAuO₂·Li₂PdO₃·Li₂PtO₃·LiReO₄·LiCuO₂·LiBiO₃)을 **검증된 값**으로 쓰기 — 재현 불가(§10-4) |

**본 그림 / 안 본 그림 (16장 크로핑 중 11장 실독)**
- ✅ 본 것: `Fig. 1`(방법 예시) · `Fig. 2`(Li 삼원 산화물 heatmap, 700 dpi 재크로핑 확대 판독) · `Fig. 3`(이원 산화물) · `Fig. 4`(폴리음이온) · `Fig. 5`(불화물 + boxplot) · `Fig. S1`(swarmplot) · `Fig. S3`(NMC/NCA 프록시) · `Fig. S7`(**anodic limit**) · `Fig. S8`(**cathodic limit**) · `Fig. S9`(창 겹침 산점도) · `Fig. S10`(**Ed ↔ 전기화학 한계 상관**)
- ⛔ 안 본 것: `Fig. S2`(상평형 산점도) · `Fig. S4`·`Fig. S5`(Ed boxplot — `Fig. 5b`·XLSX 와 같은 데이터) · `Fig. S6`(이원 산화물군 cathodic limit) · `Table S1` 이미지(PDF 텍스트를 x-좌표로 읽어 **4열을 정확히 복원**했으므로 이미지가 불필요)

---

## 1. 한 줄 요약

**고전압/고용량 양극과 접촉해도 반응하지 않는 고체 화학이 무엇인지를, "유사이원 혼합물의 최소 상호분해에너지 E_d 가 정확히 0 인가" 라는 **불리언**으로 정의하고, Materials Project 에너지만으로 **236종 × 8 양극상태 = 1,888 쌍**을 전수 평가한 편.** 결론은 낙관적이지 않다 — 리튬화·탈리튬화 **양쪽 모두**에서 안정한 물질은 극소수이며, 탈리튬화 양극(특히 CoPO₄·Ni₀.₅Mn₁.₅O₄)이 병목이다. 살아남는 화학은 **리튬 인산염**(고전압 양극)과 **리튬 삼원 불화물**(탈리튬 고전압 양극, 산화물과 경향이 **역전**), 그리고 Li 를 안 가진 **이원 산화물**(대신 Li⁺ 수송이 없다)이다.

---

## 2. 메타

| 저자 | 저널/년 | DOI | 조성(계) | 연구유형 |
|---|---|---|---|---|
| A. M. Nolan, Y. Liu, **Y. Mo\*** (UMD) | *ACS Energy Lett.* **4**, 2444–2451 (2019) | `10.1021/acsenergylett.9b01703` | 양극 8상태 × 접촉 고체 236종 (Li 삼원 산화물 72 · 이원 산화물 40 · 4원 폴리음이온 97 · Li 삼원 불화물 27) | **순수 계산** — 자체 DFT 0회, 자체 실험 0회. MP 에너지 + 상평형 조합론 |

**양극 8상태** (모두 MP 기준 조성):

| 약칭 | 조성 | 상태 | 역할 |
|---|---|---|---|
| LCO | LiCoO₂ | 리튬화(방전) | 상용 기준 |
| L0.5CO | Li₀.₅CoO₂ | 탈리튬화(충전) | 상용 기준의 충전상태 |
| LNO | LiNiO₂ | 리튬화 | **Ni-rich(NMC·NCA) 프록시** |
| L0.5NO | Li₀.₅NiO₂ | 탈리튬화 | ↑ 의 충전상태 |
| LMNO | LiNi₀.₅Mn₁.₅O₄ | 리튬화 | 고전압 스피넬(5 V급) |
| MNO | Ni₀.₅Mn₁.₅O₄ | 탈리튬화 | ↑ 의 충전상태 |
| LCP | LiCoPO₄ | 리튬화 | 고전압 올리빈(4.8 V급) |
| CP | CoPO₄ | 탈리튬화 | ↑ 의 충전상태 |

추가로 `Fig. S3` 에 **NMC111**(LiMn₀.₃Co₀.₃Ni₀.₃O₂) · d-NMC111 · **NCA**(LiAl₀.₀₅Co₀.₁₅Ni₀.₈O₂) · d-NCA, `Table S1` 에 **Li₀.₂₅NiO₂**(더 깊은 탈리튬).

---

## 3. 핵심 수치

### 3a. 데이터셋 규모 (Sup2 XLSX 전수 — 본 digest 가 센 것)

| 물질군 | 접촉물질 수 | 쌍 수 | Ed=0 비율(8상태 평균) | 최악 쌍 |
|---|---|---|---|---|
| Lithium ternary oxides (Li–M–O) | **72** | 576 | 40 % | Li₆ZnO₄ + CoPO₄ **−289.7 meV/atom** |
| Binary oxides (M–O, Li 없음) | **40** | 320 | 42 % | Rb₂O + CoPO₄ **−533.7 meV/atom** |
| Quaternary polyanion (Li–M–X–O, X=B/Si/P) | **97** | 784(중복 8행 포함) | 42 % | K₂LiBO₃ + CoPO₄ **−195.0 meV/atom** |
| Lithium ternary fluorides (Li–M–F) | **27** | 216 | 31 % | LiAuF₆ + LiNiO₂ **−373.6 meV/atom** |
| **합계** | **236 (고유)** | **1,888 (고유) / 1,896 행** | — | — |

> ⚠ `Li₂B₃PO₈` 8행이 XLSX 에 **완전 중복**으로 들어 있다(값 동일). 고유 쌍은 1,888.

### 3b. 본문이 명시한 Ed (전부 XLSX 와 **소수점까지 일치** — §12a 검증)

| 반응 | 본문 표기 | XLSX 실값 | 상평형(산물) |
|---|---|---|---|
| LiCoO₂ + LiTa₃O₈ (Eq 1) | −19 meV/atom | **−19.2** | Li(CoO₂)₂, LiTaO₃, Co₃O₄ |
| Li₀.₅CoO₂ + Li₅TaO₅ (Eq 2) | −33 | **−33.3** | Li₇Co₅O₁₂, Li₃TaO₄, Li₅Co₃O₈ |
| LiNiO₂ + LiTa₃O₈ (Eq 3) | −39 | **−39.0** | Ni₃O₄, Li(NiO₂)₂, LiTaO₃ |
| Li₀.₅NiO₂ + Li₅TaO₅ (Eq 4) | −32 | **−31.9** | **Li₂NiO₃**, **NiO**(암염), Li₃TaO₄ |
| LiCoO₂ + LiPO₃ | −71 | **−71.3** | Li(CoO₂)₂, **Li₃PO₄**, Co₃O₄ |
| Li₀.₅CoO₂ + LiPO₃ | −19 | **−18.8** | CoPO₄, Li₄P₂O₇, CoO₂ |
| LiCoO₂ / Li₀.₅CoO₂ + **Li₃PO₄** | (stable) | **0 / 0** | — |

### 3c. 전기화학 창 — **figure-read ≈** (논문은 이 값들을 숫자로 적지 않는다)

`Fig. S7` **anodic limit (V vs Li/Li⁺)** — 중앙값 / 박스(Q1–Q3) / 수염:

| 물질군 | 중앙값 | 박스 | 수염 |
|---|---|---|---|
| oxides | ≈ **3.7** | 3.25–4.1 | 2.45–5.25 |
| **fluorides** | ≈ **6.7** | 6.55–7.0 | 6.4–7.4 |
| **phosphates** | ≈ **4.6** | 4.3–5.0 | 3.9–5.25 |
| borates | ≈ 3.6 | 3.5–3.9 | 3.25–4.45 (이상치 4.6–4.8) |
| silicates | ≈ 3.65 | 3.45–3.85 | 3.15–4.1 |
| **chlorides** | ≈ **4.35** | 4.3–4.4 | 4.25–4.45 (박스가 극도로 좁다) |

`Fig. S8` **cathodic limit (V)** — 중앙값 / 박스 / 수염:

| 물질군 | 중앙값 | 박스 | 수염 |
|---|---|---|---|
| oxides | ≈ 1.35 | 0.9–2.1 | 0.0–3.5 |
| fluorides | ≈ 2.27 | 1.35–3.3 | 0.28–5.35 |
| phosphates | ≈ 2.45 | 2.2–3.05 | 1.57–4.13 (이상치 4.25·0.72) |
| borates | ≈ 0.98 | 0.8–1.5 | 0.25–2.17 (이상치 3.25) |
| silicates | ≈ 0.9 | 0.55–1.3 | 0.25–2.05 |
| chlorides | ≈ 1.6 | 0.7–2.15 | 0.0–2.5 |

> ⚠ **이 표는 전부 `figure-read ≈` 다.** 본문·SI 텍스트에 숫자가 없고, Sup2 XLSX 에도 **한계 전압 열이 없다**. 재현 불가능한 수치이므로 **경향 비교에만** 쓴다.

`Fig. S9`(a) 산점도에서 읽히는 계군 분포: **불화물만 anodic 6.4–7.4 V 로 완전히 분리**되고 나머지 전 계열이 2.4–5.3 V 에 뭉친다. 점선 격자는 x≈1.8·3.4 / y≈1.8·3.4 — **LiCoO₂ 자신의 창**(cathodic 1.8 / anodic 3.4 V)으로 읽힌다.

---

## 4. 계산 방법 ★ — "안정" 의 조작적 정의를 **식으로**

### 4a. 유사이원(pseudo-binary) 4단 정의 (SI "Computation methods", Zhu16 승계)

**① 조성** — 두 물질을 **각각 1원자/화학식단위로 정규화**한 뒤 선형 혼합:
```
C_pb(x) = x·C_cathode + (1−x)·C_contacting          x ∈ [0,1] (원자분율)
```

**② 에너지** — 혼합물 자체는 **아무 것도 완화하지 않는다**. 두 끝점 에너지의 **선형 보간**:
```
E_pb(x) = x·E_cathode + (1−x)·E_contacting
```

**③ 그 조성의 분해에너지** — 조성 C 에서 가능한 **최저 총에너지 상평형**과의 차:
```
ΔE_D(phase) = E_eq(C) − E(phase)            ( ≤ 0 )
ΔE_D(x)     = E_eq[C_pb(x)] − E_pb(x)
```

**④ 끝점 자신의 준안정성 제거 → 상호(mutual) 분해에너지**:
```
ΔE_D,mutual(x) = ΔE_D(x) − x·ΔE_D(cathode) − (1−x)·ΔE_D(contacting)
```

**⑤ 최종 지표**:
```
E_d = min_x  ΔE_D,mutual(x)         [eV/atom, 그림은 meV/atom]
```

부호 규약: **E_d ≤ 0**. `E_d = 0` ⇔ 모든 x 에서 유사이원이 볼록껍질 위에 있다 ⇔ **"안정"**. 더 음수일수록 **반응성이 크다**.

`Fig. 1b` 가 이 곡선 그 자체다: x축 = *fraction of Li phosphate*, y축 = E_d (meV/atom), 별표 = 최소점. LiCoO₂|LiPO₃ 는 x≈0.33 에서 **−71**, Li₀.₅CoO₂|LiPO₃ 는 x≈0.67 에서 **−19**, Li₃PO₄ 쌍은 두 양극 모두 **전 구간 0**(수평 초록선). ⇒ **최소점의 위치(x)가 양극 상태에 따라 바뀐다**는 것까지 그림이 보여준다.

### 4b. ⚠ 이 논문은 **새 DFT 를 한 번도 돌리지 않는다**

| 항목 | 값 |
|---|---|
| **code / version** | **n/a** — 자체 DFT 계산 없음. 모든 에너지가 **Materials Project**(Jain 2013, ref 24)에서 옴 |
| **functional / vdW** | **n/a** (MP 상속 = VASP PBE + GGA/GGA+U mixing, Wang 2006 계열 U). 논문은 이것을 **명시하지 않는다** |
| **pseudo / PAW** | **n/a** (MP 상속) |
| **k-points / ecut / supercell / nat** | **n/a** (MP 상속) |
| **DFT+U** | **n/a** — 언급 없음. MP 규약상 TM 산화물에 U 가 걸려 있을 것이나 **논문이 확인하지 않는다** |
| **AIMD / MLIP** | 없음 (마무리 토론에서 "NEB·MD 로 후속 평가 가능" 이라고 *제안*만 한다) |
| **무질서 처리** | **해당 없음** — 조성만 다루는 상평형 조합론. `LiNi₀.₅Mn₁.₅O₄`·`LiMn₀.₃Co₀.₃Ni₀.₃O₂` 같은 혼합점유 조성도 **MP 엔트리 하나**로 처리 |
| **온도 / 압력** | **0 K, PV 무시** (엔트로피·기체분압 없음). ⚠ 산물에 `O₂` 가 자주 등장하는데 **고체와 같은 자격으로** 계산된다(§10-2) |
| **특이사항** | E_d 계산 자체는 조합론이므로 계산비용이 사실상 0 — 그래서 1,888 쌍 전수가 가능하다 |

### 4c. anodic / cathodic limit — **이 논문은 정의를 적지 않는다**

`Fig. S6`–`Fig. S10` 의 축은 *anodic limit* / *cathodic limit* 인데, **SI 의 "Computation methods" 절에 이 두 양의 식이 없다.** SI 참고문헌은 딱 3개다: [Zhu16] JMCA · [Zhu15] ACS AMI · [Jain13] MP. ⇒ 두 한계는 **[Zhu15] 의 grand-potential 전기화학창** 을 인용 승계한 것으로 읽을 수밖에 없다.

그 [Zhu15] 의 정의(우리가 이미 `tools/oxidation/esw_grand_potential.py` 에 구현해 둔 것):
```
Li 저장고를 열고(open system) μ_Li 를 훑으면서, 조성이 볼록껍질 위에서
'다른 상영역으로 넘어가는' 전압을 찾는다.
V (vs Li/Li⁺) = [μ_Li(metal) − μ_Li] / e
cathodic limit = 환원 개시 전압,  anodic limit = 산화 개시 전압
```
**기준 전극은 Li/Li⁺** (0 V = Li 금속). 우리 `oxidation_stability.json` 의 `voltage_convention` 과 **문자 그대로 같다**.

⚠ 그러나 이 논문은 ① 식을 안 적고 ② 계 목록을 안 주고 ③ 값을 XLSX 에 안 넣었다. **그래서 §3c 의 표는 전부 figure-read 다.**

### 4d. 우리 도구와의 1:1 대응 (★ 이것이 이 digest 의 핵심 소득)

| Nolan 2019 SI 식 | 우리 구현 | 일치 |
|---|---|---|
| `C_pb(x) = x·C_cat + (1−x)·C_contact`, 1원자/f.u. 정규화 | pymatgen `InterfacialReactivity(..., norm=True)` **(기본값)** | 🟢 |
| 끝점 준안정성 제거 (`− x·ΔE_D(cat) − (1−x)·ΔE_D(contact)`) | `use_hull_energy=True` — 두 끝점을 **hull 에너지에 앉힌다** | 🟢 **정확히 같은 조작** |
| `E_d = min_x ΔE_D,mutual(x)` | `tools/oxidation/interface_reactivity.py` → `ir.get_kinks()` 의 `react_energy_per_atom` **최솟값** | 🟢 |
| 단위 **eV/atom**, **음수 = 반응성** | `min_reaction_energy_eV_per_atom`, 음수 = 반응성 (`interface_reactivity.py` docstring) | 🟢 |
| DB = **Materials Project** | MP, `thermo_types=["GGA_GGA+U"]` 고정 | 🟡 같은 DB, **다른 세대**(2019 ↔ 2026 pinned) |
| 상평형 산물 기록 | `most_exothermic_reaction` + `all_kinks` | 🟢 |

⇒ **우리 `nd2o3_interface_reactivity_2026_06_17` 블록의 `min_dE_rxn_eV_per_atom_vs_LiCoO2` 는 Nolan 2019 의 E_d 와 이름만 다른 같은 양이다.**

⚠ **귀속을 정확히 한다 (우리 원장과 충돌하지 않게)**: `comparison_vs_ours.md` 의 Reference key 는 이미 **[Rich16]**(Richards/Miara/Wang/Kim/Ceder, *Chem. Mater.* 2016, 28, 266)을 *"pseudo-binary 계면 원전"* 으로 등재하고 있고 **그 등재는 맞다** — 닫힌 형식 `ΔE = min_x {E_pd[xc_a+(1−x)c_b] − xE[c_a] − (1−x)E[c_b]}` 를 세운 것이 그 편이다. Nolan 2019 의 SI 는 [Rich16] 이 아니라 **[Zhu16]**(Zhu/He/Mo, *JMCA* 2016, 4, 3253)과 **[Zhu15]** 를 인용하며, **끝점 준안정성 제거**(`− xΔE_D(cat) − (1−x)ΔE_D(contact)`)가 붙은 *mutual* 판이 그쪽 계열이다. ⇒ 정확한 문장은:
> **형식화 = [Rich16] · mutual(준안정성 제거) 판 = [Zhu16] · *양극 SOC 두 상태에 전수 적용* = [Nolan19]**.
우리 값은 `use_hull_energy=True` 를 쓰므로 **[Zhu16]/[Nolan19] 판**이다.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a | LCO ↔ L₀.₅CO 사이클 동안 Li₃PO₄ 코팅이 **양 끝 상태 모두에서** 안정하다는 개념도 | **양극은 한 상태가 아니다** — 우리 `interface_reactivity` 는 `LiCoO₂` 하나만 봤다 |
| 1b | **E_d 곡선 그 자체**: x축 *fraction of Li phosphate*, y축 E_d (meV/atom). LiCoO₂\|LiPO₃ 는 x≈0.33 에서 −71, Li₀.₅CoO₂\|LiPO₃ 는 x≈0.67 에서 −19, Li₃PO₄ 쌍은 전 구간 0 | 우리 `all_kinks` 리스트와 **같은 곡선**. 최소점 x 가 양극 SOC 에 따라 이동하는 것까지 동일 |
| 1c | 인산염 3종(LiPO₃·Li₄P₂O₇·Li₃PO₄) × 양극 2상태 미니 heatmap. Li₃PO₄ 행만 초록 테두리 | Li 함량이 **낮을수록**(LiPO₃) 리튬화 양극과 더 반응한다는 규칙의 최소 예시 |
| 2 | **Li 삼원 산화물 72종 × 8 양극상태** heatmap. 3 패널(nonmetals 24 / p-block 24 / transition metals 26), 각 M 족 안에서 **Li 함량 증가 순** 정렬 | 우리 `Li₃PO₄`·`Li₂SO₄` 위치 확인용. ⚠ **행 라벨이 XLSX 와 전이금속 패널에서 3종 어긋난다**(§10-5) |
| 3 | **이원 산화물 40종** heatmap (alkali 5 / alkaline-earth 5 / nonmetal 5 / TM 16 / p-block 9). 알칼리 산화물(Li₂O·Na₂O·K₂O·Rb₂O·Cs₂O) 행이 **거의 전부 포화 암색**, BeO·SiO₂ 행은 **거의 백색** | **우리 계 직결**: `B₂O₃` 행이 여기 있다 — LiCoO₂ **−56.8**, LiNiO₂ **−85.9** meV/atom (§7c) |
| 4 | **선택된 4원 폴리음이온 45종**(phosphates 15 / silicates 15 / borates 15) heatmap. K·Rb·Cs 를 품은 규산염·붕산염이 MNO·CoPO₄ 열에서 가장 짙다 | ⚠ **ASAP 출판 시 라벨 오류가 있었고 2019-09-23 정정본이 나온 그림**이다 — 값은 XLSX 에서 확인할 것 |
| 5a | **Li 삼원 불화물 27종** heatmap. 색축이 −150 meV/atom 까지 확장되고, **LiCoO₂·LiNiO₂ 열이 가장 짙고 LiCoPO₄·CoPO₄ 열이 가장 옅다 = 산화물과 정반대** | **역전 현상의 원자료.** 우리가 "할로겐화물 SE 가 양극 쪽에서 유리하다" 를 말할 때의 계산 근거 |
| 5b | 8 양극 × 4 물질군 **grouped boxplot** (x축 decomposition energy, 0 → −500 meV/atom) | 한 장으로 보는 결론: **CoPO₄ 행이 가장 넓고 가장 음수**, LMNO 행이 가장 좁다 |
| S1 | **swarmplot** — 8 양극 × 전체 Li–M–O, 점 색 = **접촉물질의 Li 분율**(0.05–0.55). LiCoO₂ 클러스터는 **어두운(저-Li) 점**이 아래로 처지고, CoPO₄ 클러스터는 **밝은(고-Li) 점**이 아래로 처진다 | **논문의 중심 기전이 그림 하나로 보인다.** 본 digest 가 이것을 Pearson r 로 정량(§12c) |
| S3 | NMC111·d-NMC111·NCA·d-NCA 열을 LNO·LCO 옆에 붙인 heatmap | **LNO 가 NMC/NCA 의 좋은 프록시**임을 검증 — 뒤집으면 **LCO 는 Ni-rich 프록시로 낙관적**이다(우리 db caveat 에 직결) |
| S7 | **anodic limit boxplot** — oxides/fluorides/phosphates/borates/silicates/**chlorides** 6군 | 🔑 **우리 2.256 V 가 놓일 축.** 불화물만 6.4–7.4 V 로 분리, 염화물 박스는 4.3–4.4 V 로 극히 좁다 |
| S8 | **cathodic limit boxplot** — 같은 6군 | 우리 `reduction_limit_V` **1.242 V** 는 oxides 중앙값(≈1.35)·chlorides 중앙값(≈1.6) 근처 |
| S9 | (a) 계군별 **cathodic vs anodic** 산점도 (b) 같은 점을 **LiCoO₂ 와의 E_d 로 채색**. 초록 테두리 + 1–4 번 창 겹침 유형 범례 | 🔑 **두 양을 한 평면에 놓은 유일한 그림.** ⚠ (b) 에서 **가장 짙은(가장 반응성 큰) 점이 anodic 6.5–7.4 V 쪽에 있다** — "산화한계가 높으면 안정" 의 **반례**(§10-3) |
| S10 | **LiCoPO₄ 와의 E_d vs 전기화학 한계** 산점도 (●=anodic, ×=cathodic; M = Bi/Ge/Ta/Si) | 🔑 **두 양의 상관을 직접 그린 그림.** anodic 3.9–4.05 V 군은 E_d ≈ −0.002…−0.023, anodic 2.5–3.0 V 군은 E_d ≈ −0.08…−0.118 |
| Table S1 | LCO&L₀.₅CO / LNO&L₀.₅NO / LNO&L₀.₅NO&L₀.₂₅NO / **stable with all** 4열의 화합물 목록 | 논문의 **명시적 산출 목록**. 본 digest 가 4열을 좌표로 복원: **40 / 28 / 14 / 14 종**(§12d) |

---

## 6. 절별 결과 — 전부

### 6a. `Fig. 1` — 방법을 한 예시로 (Li 인산염 3종 × LCO 2상태)

- `Li₃PO₄` 는 LCO·L₀.₅CO **양쪽 모두 E_d = 0**. 곡선이 x 전 구간에서 0 (Fig. 1b 초록 수평선).
- `LiPO₃` 는 LCO 와 **−71 meV/atom**, L₀.₅CO 와 **−19 meV/atom**.
  → 산물은 각각 `Li(CoO₂)₂ + Li₃PO₄ + Co₃O₄` 와 `CoPO₄ + Li₄P₂O₇ + CoO₂`.
  🔑 **LiPO₃ 가 LCO 에게서 Li 를 뺏어 Li₃PO₄ 가 되면서 양극을 탈리튬시킨다** — 코팅이 양극을 망가뜨리는 전형.
- `Li₄P₂O₇` 는 중간 (LCO −41.2 / L₀.₅CO −3.3).

### 6b. Li 삼원 산화물 (`Fig. 2`, `Table S1`, `Fig. S1`, `Fig. S2`)

**리튬화 LCO 와 탈리튬 L₀.₅CO 는 서로 반대 방향으로 까다롭다.**

- **LCO 쪽 실패 모드 = Li 를 빼앗긴다.** `LiCoO₂ + LiTa₃O₈ → Li(CoO₂)₂ + Co₃O₄ + LiTaO₃` (**−19.2 meV/atom**, Eq 1). 산물의 `Co₃O₄` 는 실험에서 사이클 후·고전압 보관 후 LCO 표면에 실제로 관찰된 상(ref 38·39). ⇒ *"양극을 망가뜨릴 수 있는 코팅은 피해야 한다"*.
- **L₀.₅CO 쪽 실패 모드 = Li 를 빨아들인다.** `Li₀.₅CoO₂ + Li₅TaO₅ → Li₃TaO₄ + Li₇Co₅O₁₂ + Li₅Co₃O₈` (**−33.3 meV/atom**, Eq 2). Li-rich 코발트 산화물이 생기고 코팅은 Li 가 빠져 저-Li 상으로 간다.
- LCO 는 `LiTaO₃`·`Li₃TaO₄`·`Li₅TaO₅` 전부와 안정(0)인데 `LiTa₃O₈` 하고만 반응한다 — **같은 Li–Ta–O 안에서도 Li 함량이 판정을 가른다**.
- 통계(본 digest 재계산): Li 삼원 산화물 72종 중 Ed=0 인 비율은 **LCO 81 % → L₀.₅CO 54 %**, **LNO 62 % → L₀.₅NO 40 %**. 탈리튬화가 확실히 더 까다롭다.

### 6c. Ni-rich 층상 (`Fig. S3`)

- **LNO 는 LCO 보다 일관되게 나쁘다**: 같은 `LiTa₃O₈` 에 대해 LCO −19.2 → **LNO −39.0** meV/atom (Eq 3).
- 탈리튬 L₀.₅NO 는 `Li₅TaO₅` 와 **−31.9 meV/atom**, 산물에 **`Li₂NiO₃` + 암염 `NiO`** (Eq 4). 암염 NiO 표면층은 Ni-rich 양극 실험의 표준 관찰(ref 42–44).
- 저자 해석: LNO 의 층상상 자체가 LCO 보다 덜 안정하고, **암염 NiO 로 가려는 구동력**이 Co₃O₄ 보다 크다.
- `Fig. S3` 로 **NMC111·NCA 가 LNO 패턴을 따른다**는 것을 확인 — LNO 를 프록시로 써도 된다는 근거.

### 6d. 고전압 양극 (LMNO·LCP)

- 산화물과 **더 크게, 더 많이** 반응한다. 탈리튬 상태(MNO·CP)에서 Li 삼원 산화물 중 Ed=0 은 **MNO 3 % · CP 8 %** 뿐 (본 digest 재계산).
- 원인: 탈리튬 고전압 양극의 **Li 흡인력**이 크다.

### 6e. 일반 경향 — **Li 함량 규칙**

> 탈리튬 양극은 **Li 가 많은** 접촉물질과 반응한다(Li 를 뽑아간다).
> 리튬화 양극은 **Li 가 적은** 접촉물질과 반응한다(Li 를 뺏긴다).
> ⇒ **두 상태를 동시에 만족하는 단일 물질이 드물다.** 그리고 탈리튬 쪽 구동력이 크므로 **탈리튬 보호가 우선**.

본 digest 의 정량화(§12c): 접촉물질 Li 분율 vs E_d 의 Pearson r = **LiCoO₂ +0.32 · LiNiO₂ +0.37** (양수 = Li 많을수록 덜 반응) ↔ **MNO −0.60 · CoPO₄ −0.61** (음수 = Li 많을수록 더 반응). **부호가 정확히 뒤집힌다.**

### 6f. 이원 산화물 (`Fig. 3`)

- Li 를 안 가지므로 **탈리튬 양극이 뽑아갈 Li 가 없다** → 탈리튬 쪽에서 유리. 실제로 이원 산화물은 **L₀.₅CO 에서 65 %** Ed=0 (LCO 48 % 보다 **높다** — 유일하게 방향이 반대인 군).
- 실험 코팅 재현: `Al₂O₃`·`SiO₂`·`ZrO₂`·`MgO`·`ZnO` 가 L₀.₅CO 와 전부 0.
- **군 차이가 크다**: 알칼리·알칼리토 산화물과 비금속 산화물은 대체로 불안정(예외 BeO·MgO·SiO₂). 전이금속·p-block 산화물은 LMNO·LCP 와 좋다.
- 저자의 균형 잡힌 코멘트: Li 가 없으면 **Li⁺ 전도가 없다**. 그런데 `Al₂O₃`·`SiO₂` 같은 **약한 반응은 오히려 좋을 수 있다** — Li 가 코팅 안으로 들어가 수송을 만들고 결합을 강화한다. 실험적으로 LCO 위 Al₂O₃ 가 **LiAlO₂** 를 만드는 것이 계산과 일치(ref 54).
- 최악: **알칼리 산화물 + CoPO₄** — Rb₂O −533.7, K₂O −521.7, Cs₂O −487.6, Na₂O −430.9 meV/atom.

### 6g. 폴리음이온 (`Fig. 4`)

- 폴리음이온 계열은 Li 삼원 산화물보다 **탈리튬 L₀.₅CO·L₀.₅NO 와 더 좋다**.
- **리튬 인산염이 고전압 양극(LMNO·LCP)과 가장 좋다** — 본 digest 재계산: 4원 인산염 25종 중 Ed=0 비율 **LCP 76 % · CP 56 %** (붕산염 17 %/2 %, 규산염 15 %/0 % 와 대비).
- **붕산염·규산염은 반대로 층상 산화물과 좋다** — LCO 에서 붕산염 81 % · 규산염 93 %.
- 저자의 귀속: 인산염의 강점은 **높은 산화한계**(`Fig. S7` — phosphates 중앙값 ≈4.6 V) 가 탈리튬 고전압 양극의 전위와 맞물리기 때문.
- 실험 대응: LNMO(ref 55)·LCP(ref 56·57) 인산염 코팅, NASICON 계 SE(ref 58–62), NMC 위 `Li₁.₄Al₀.₄Ti₁.₆(PO₄)₃`(ref 62).

### 6h. Li 삼원 불화물 (`Fig. 5a`) — **경향 역전**

- 산화물과 **정반대**다. 본 digest 재계산: Ed=0 비율 **LCO 4 % · LNO 4 %** ↔ **LCP 67 % · CP 81 %**.
- 고-Li 불화물도 탈리튬 양극과 좋다 — Li 삼원 산화물의 "Li 많으면 탈리튬 양극이 뽑아간다" 규칙이 **불화물에서는 깨진다**.
- ⇒ **고전압 양극과 안정하면서 Li 수송 캐리어도 있는 유일한 조합**이라는 것이 저자의 셀링 포인트.
- 실험 대응: `CeF₃`·`AlF₃` 코팅(ref 64·65), 그리고 **`Li₃YCl₆` 할라이드 SE + LCO**(ref 63·66 — 자매논문 Wang/Bai/Nolan/Liu/Gong/Sun/Mo, *Angew* 2019).
- 최악 쌍은 **귀금속 불화물 + 리튬화 층상**: LiAuF₆+LiNiO₂ −373.6, LiAgF₄+LiNiO₂ −264.7, **LiPF₆+LiNiO₂ −250.3** meV/atom. (LiPF₆ 가 리튬화 양극과 극도로 반응성이라는 것은 액체 전해질 염 관점에서도 시사적이다.)

### 6i. 토론 · 결론

- **검증**: 실험적으로 쓰인 코팅 — `ZrO₂`·`Al₂O₃`·`SiO₂`(층상), ASSB 의 `Li₃PO₄`·`LiNbO₃`·`LiTaO₃`(ref 68 Culver/Zeier/Janek) — 이 전부 계산 기준을 통과.
- **일반 원리**: 탈리튬 양극의 산화전위(**≥4.5 V**)가 대부분 산화물의 산화한계(**3.5–4 V**)를 넘는다 → 산화물 코팅은 Li 함량이 낮거나 0 이어야 살아남는다. 그런데 Li 수송에는 Li 가 필요하다. ⇒ **본질적으로 높은 산화한계를 갖는 인산염(폴리음이온)**, 그리고 **불화물**이 답.
- **저자 스스로 인정한 공백**: 계면/계면상 이온수송은 이 연구가 못 본다. NEB·MD·결함 형성에너지로 따로 봐야 한다(ref 23·51·69–71).
- 마지막 확장 제안: 같은 틀을 **유전체 게이트·뉴로모픽 소자**에도 쓸 수 있다(ref 72 Hubbard & Schlom — 실리콘 위 이원 산화물 열역학).

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md` ★★

> 1저자가 digest 에 **반드시 답하라고 지정한 5개 물음**을 절 번호로 받는다.

### 7a. Q1 — **"안정" 의 조작적 정의가 정확히 무엇인가**

| 물음 | 답 |
|---|---|
| grand-potential 개시 전압인가? | **아니다.** 헤드라인 기준은 전압이 아니다 |
| 구간(창)인가? | **아니다.** |
| 평균 전환전압인가? | **아니다** ([Aykol14] 의 것과 다르다) |
| 그럼 무엇인가 | **스칼라 위의 불리언**: `E_d = 0` — 유사이원 상호분해에너지의 **최솟값이 정확히 0** 인가. 0 이면 안정, 음수면 그 크기가 반응성 |
| 어떤 조건에서 | **양극의 리튬화·탈리튬화 *두 이산 상태 각각*에서**. μ_Li 를 연속으로 훑지 않는다 — 양극 SOC 를 **두(또는 세) 점으로 샘플링**한다 |
| 기준 전극 | **E_d 에는 없다** — 전압이 아니라 에너지다. 기준 전극은 **부차 지표(anodic/cathodic limit)에만** 있고 그것은 **vs Li/Li⁺** |
| DB | **Materials Project** (ref 24 Jain 2013). ⚠ **OQMD 가 아니다** — [Aykol14]/[Aykol16] 과 여기서 갈린다 |
| 온도·압력 | **0 K, PV 무시** |

🔑 **정리**: 이 논문의 "안정" 은 **[Aykol16] 의 `E_d`(리튬화 개시 전압)와 기호만 같고 완전히 다른 양이다.** Aykol 의 `E_d` 는 **V** 단위, Nolan 의 `E_d` 는 **eV/atom** 이다. ⛔ 두 문헌의 `E_d` 를 같은 표에 넣으면 즉시 틀린다.

### 7b. Q2 — **그 정의가 우리 2.256 V 와 같은 양인가 · 계보가 확정되는가** ★★★

**두 갈래로 답이 갈린다. 먼저 결론:**

> 🟢 **계보는 확정된다 — 단, 이 논문의 *헤드라인* 을 통해서가 아니라 *SI* 를 통해서다.**
> · Nolan 2019 의 **E_d** 는 우리 **`interface_reactivity`(−0.3227 eV/atom)** 와 같은 양이다 → **새 확정 1건**.
> · Nolan 2019 의 **anodic limit**(`Fig. S7`·`S9`·`S10` 축)은 우리 **`2.256 V`** 와 같은 양이다 → **[Zhu15] 계보 확인**.
> · 그러나 **anodic limit 은 이 논문의 산출물이 아니다** — 정의도 안 적고 값도 안 적는다. 따라서 **원전은 여전히 [Zhu15](→[Mo/Ong/Ceder 2012])이고, Nolan 2019 는 그 계보의 *형제 적용*이지 *조상*이 아니다.**

**세부 대조 (우리 `oxidation_stability.json` ↔ Nolan SI):**

| 항목 | 우리 (`esw_grand_potential.py`) | Nolan 2019 anodic limit | 판정 |
|---|---|---|---|
| 방법 | `PhaseDiagram.get_element_profile(Li, comp)` — μ_Li 개방 grand-potential | [Zhu15] grand-potential 전기화학창 (인용 승계) | 🟢 **같은 방법** |
| 기준 전극 | **vs Li/Li⁺**, 0 V = Li 금속, `V = μ_Li(metal) − μ_Li` | **vs Li/Li⁺** (그림 축 `anodic limit (V)`) | 🟢 **같은 기준** |
| DB | MP, `GGA_GGA+U` pinned (2026) | MP (2019 세대) | 🟡 같은 DB, **다른 세대** |
| 의미 | **첫 산화 단계 개시 전압** (comp1: `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻`) | 같은 의미 | 🟢 |
| 값 | **2.256 V** (LiS₄ 제외) / 2.14 (포함) | 계군 boxplot 만 (`figure-read`) | ⚠ **절대값 대조 불가** |

**[Aykol 두 편에 대한 종전 판정이 바뀌는가?** → **바뀌지 않는다. 오히려 정리된다.**]

| 계보 | 우리 `2.256 V` 와의 관계 | 우리 `interface_reactivity` 와의 관계 |
|---|---|---|
| [Aykol14] (#1) | ❌ 다른 양 (닫힌계 ΔH, 평균 전환전압, eV per HF) | ❌ 다른 양 (산물 가정, HF 정규화) |
| [Aykol16] (#2) | ❌ 다른 양 (`E_c` = **액체로의 양이온 용출** 전위) · 🟡 `E_d` 는 **환원축**에만 대응 | ❌ 다른 양 (OQMD hull 불리언) |
| [Xiao19] (#3) | 🟢 **같은 양** (grand-potential V_ox) | 🟢 **같은 양** (pseudo-binary ΔE_rxt) |
| **[Nolan19] (#4)** | 🟢 **같은 양** — 단 **SI 의 부차 지표**로만 등장 | 🟢🟢 **같은 양 + 같은 구현** — 헤드라인 |
| [Zhu15]/[Zhu16] | 🟢🟢 **직계 원전** | 🟢🟢 **직계 원전** |

🔑 **한 문장 판정**: *"우리 산화 onset 2.256 V 의 계보는 Mo/Ong/Ceder 2012 → [Zhu15] → {[Xiao19], [Nolan19]} 이고, Aykol 두 편은 **다른 양**이다"* — 계보 카드의 종전 판정이 **그대로 유지되면서, Nolan 2019 가 그 가지에 추가된다.** 그리고 **`interface_reactivity` 쪽에서는 Nolan 2019 가 [Zhu16] 다음 가는 1차 참조가 된다** (지금까지 우리는 pymatgen/[Richards16] 으로만 귀속했다).

⚠ **"Mo 그룹이니 본류일 것" 이라는 사전 가설은 절반만 맞았다.** Mo 그룹 본류가 맞지만, **이 편의 본론은 전압축이 아니라 계면 반응에너지축**이다. 전압축의 본류는 같은 그룹의 **[Zhu15]** 다.

### 7c. Q3 — `interface_reactivity`(eV/atom) 대응: **정규화·부호 규약이 같은가**

**전부 같다.** §4d 표 그대로다. 추가로 확인한 것:

| 항목 | Nolan E_d | 우리 `interface_reactivity` |
|---|---|---|
| 정규화 | **1 원자/화학식단위**로 두 조성 정규화 후 원자분율 혼합 | pymatgen `norm=True` (기본) = 동일 |
| 끝점 준안정성 | **뺀다** (mutual) | `use_hull_energy=True` = 동일 |
| 최소화 | **x 전 구간 최소** | `get_kinks()` 최솟값 = 동일 |
| 부호 | 음수 = 반응 | 음수 = 반응 |
| 값 예 | Li₃PO₄+LCO **0**, LiPO₃+LCO **−0.0713** | comp1+LiCoO₂ **−0.3227** |

🔑🔑 **가장 값진 발견 — 우리 계면 산물이 그들의 "가장 양극 양립적인 화학" 과 정확히 겹친다**

우리 `interface_reactivity_results.json` 의 최발열 반응:
```
0.7423 LiCoO₂ + 0.2577 Li₆PS₅Cl
  → 0.08247 Co₉S₈ + 0.1134 Li₂SO₄ + 0.2577 Li₃PO₄ + 0.5155 Li₂S + 0.2577 LiCl
```
이 **산물 5종 중 2종이 Nolan 데이터셋에서 양극 양립성 최상위**다:

| 산물 | Nolan 데이터셋에서 | Ed=0 인 양극상태 |
|---|---|---|
| **Li₂SO₄** | 🥇 **Li 삼원 산화물 72종 중 유일하게 8/8 전부 Ed=0** | LCO·L₀.₅CO·LNO·L₀.₅NO·LMNO·MNO·LCP·CP **전부** |
| **Li₃PO₄** | 🥈 **6/8** (MNO −11.5, CP −1.1 meV/atom 만 미세 음수) | 나머지 6 전부 |
| Li₂S / LiCl / Co₉S₈ | ⛔ **데이터셋에 없다** (황화물·염화물 0종) | n/a |

⇒ **우리 열역학이 예측하는 CEI 의 산화물 성분은, 이 논문이 독립적으로 1·2위로 꼽는 양극 양립 화학이다.** 이것은 *"LPSCl|양극 계면이 자기 부동태화 쪽으로 기운다"* 는 서술의 **문헌 근거**가 된다. ⚠ 단, **Li₂S·LiCl 은 그들 축에서 평가된 적이 없으므로** 그 성분에 대해서는 아무 말도 못 한다.

**우리 계 물질 직격 데이터 (XLSX 에서 뽑음)**

| 물질 | LCO | L₀.₅CO | LNO | L₀.₅NO | LMNO | MNO | LCP | CP |
|---|---|---|---|---|---|---|---|---|
| **B₂O₃** (우리 `+B₂O₃` 계의 첨가상) | **−56.8** | −16.0 | **−85.9** | −58.1 | −10.9 | **0** | −16.5 | −16.3 |
| **Li₂O** (우리 환원 산물) | −10.0 | −79.6 | 0 | −77.1 | −95.8 | **−218.9** | −154.6 | **−334.4** |
| Al₂O₃ | −19.9 | **0** | −34.7 | −15.6 | **0** | **0** | −13.6 | −82.6 |
| Li₃PO₄ | **0** | **0** | **0** | **0** | **0** | −11.5 | **0** | −1.1 |
| Li₂SO₄ | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| LiNbO₃ (ASSB 표준 코팅) | **0** | **0** | −16.6 | **0** | **0** | −45.4 | −15.3 | −64.9 |
| LiTaO₃ (ASSB 표준 코팅) | **0** | **0** | −12.7 | **0** | **0** | −25.3 | −7.8 | −68.8 |
| LiTi₂(PO₄)₃ (LATP 모체) | −51.4 | **0** | −86.1 | −39.8 | **0** | −5.2 | **0** | **0** |

> 단위 meV/atom. ⛔ **이 값들을 우리 db 절대값과 같은 표에 놓지 말 것** — MP hull 세대가 다르다(§7e).
> 🔑 **B₂O₃ 읽기**: 우리 `+B₂O₃` 계는 층상 산화물 양극 쪽에서 **−57…−86 meV/atom** 의 반응 여지가 있다(특히 LNO). 다만 고전압 올리빈·탈리튬 스피넬 쪽에서는 **0…−16** 으로 훨씬 얌전하다. *"B₂O₃ 는 Ni-rich 와 붙이면 위험하고 고전압 인산염계와는 무난하다"* 는 **소환 가능한 문헌 관찰**이다.
> 🔑 **Li₂O 읽기**: Li₂O 는 탈리튬 양극과 **−219…−334 meV/atom** 로 데이터셋 최악급이다. 우리 음극쪽 환원산물이 양극쪽으로 넘어가면 안 된다는 것의 열역학적 근거.

**⚠ 우리 쪽 방법 공백 2건 (추가 DFT 계산 0 으로 메울 수 있다)**

1. **양극 SOC 를 한 점만 봤다.** 우리는 `LiCoO₂` 만 계산했다. Nolan 이 보여준 것은 **탈리튬 상태가 병목**이라는 것이다 — 우리도 `Li₀.₅CoO₂`(또는 `CoO₂`)를 추가로 돌려야 한다. `tools/oxidation/interface_reactivity.py --contacts` 에 조성 하나 추가하면 끝이다.
2. **LiCoO₂ 를 NCM 프록시로 쓴 caveat 이 이제 정량화된다.** `oxidation_stability.json` 의 `caveats` 는 *"LiCoO₂ proxy (experiment may use NCM)"* 라고만 적혀 있다. Nolan 의 답: **LCO 는 Ni-rich 의 낙관적 프록시**(같은 접촉물질에 대해 LNO 의 |E_d| 가 일관되게 크다; `Fig. S3` 이 NMC111·NCA ≈ LNO 를 확인). ⇒ 우리 caveat 을 *"LCO 프록시는 반응성을 **과소평가**한다 (방향 확정)"* 로 강화할 수 있다.

### 7d. Q4 — **목록의 판정 규칙과, 우리 LPSCl/LPSOCl 이 그 목록의 어디에 놓이는가**

**판정 규칙 (논문이 실제로 쓴 것)**

```
"X 와 안정하다"  ⇔  E_d(X_lithiated, M) = 0  AND  E_d(X_delithiated, M) = 0
```
`Table S1` 은 이 규칙을 LCO 쌍 / LNO 쌍 / LNO 3점(Li₀.₂₅NiO₂ 포함) / **전부** 에 대해 적용한 결과다. 본 digest 가 좌표로 복원한 열 크기: **40 / 28 / 14 / 14 종**.
⚠ **"stable with all" 의 "all" 은 LCO·L₀.₅CO·LNO·L₀.₅NO·L₀.₂₅NO 5 상태다** — **LMNO·MNO·LCP·CP 는 포함되지 않는다.** (고전압 양극까지 요구하면 목록은 훨씬 짧아진다 — §12b 에서 8/8 은 **단 2종**.)

**우리 계는 어디에 놓이는가 — 정직하게: *놓이지 않는다*.**

| | Nolan 데이터셋 |
|---|---|
| 황화물(S²⁻) 접촉물질 | **0 종** (Li₂SO₄·Li₂S₂O₇ 는 산소산염이지 황화물이 아니다) |
| 염화물(Cl⁻) 접촉물질 | **0 종** (Ed 데이터셋 236종 중 Cl 함유 0) |
| 티오인산염(PS₄³⁻) | **0 종** |
| 염화물의 흔적 | `Fig. S7`·`Fig. S8` boxplot 의 *chlorides* 군 **뿐** — Ed 없이 **한계 전압만**, 데이터 미공개. 출처는 자매논문 Wang *et al.* *Angew* **2019**, 58, 8039 (ref 63) |

⇒ **LPSCl·LPSOCl 은 이 논문의 목록에 이름이 없다.** 우리 계를 이 지도 위에 얹는 **유일하게 정당한 방법**은 §7b 에서 확정된 **anodic limit 축**이다:

| | anodic limit (V vs Li/Li⁺) | 출처 |
|---|---|---|
| **우리 comp1 / modelc** | **2.256** (LiS₄ 제외) / 2.14 (포함) | `db/properties/esw_lis4excluded.json` |
| Nolan oxides (계군) | 중앙값 ≈3.7, 최저 수염 ≈**2.45** | `Fig. S7` figure-read |
| Nolan phosphates | ≈4.6 | `Fig. S7` figure-read |
| Nolan chlorides (Li–M–Cl) | ≈4.35 | `Fig. S7` figure-read |
| Nolan fluorides | ≈6.7 | `Fig. S7` figure-read |
| 탈리튬 고전압 양극의 전위 | **≥4.5** (본문) | 본문 결론 |

🔑 **읽기**: 우리 LPSCl 은 **그들이 그린 산화물 분포의 최저 수염보다도 아래**에 있다. 그리고 `Fig. S10` 이 보여준 상관(anodic limit ↑ ⇒ E_d 덜 음수)을 그대로 외삽하면, anodic ≈2.26 V 인 물질은 LiCoPO₄ 와 **E_d ≈ −0.12 eV/atom 이하**여야 한다. 우리 실측은 LiCoO₂ 상대 **−0.3227 eV/atom** 으로 **더 나쁘다** — 방향이 일치한다(⚠ 다른 양극·다른 화학이므로 **정량 외삽은 금지**, 부호/방향만).

⇒ **정직한 한 문장**: *"Nolan 2019 의 지도에서 우리 계는 '목록에 든 물질' 이 아니라 **그 목록이 배제한 영역(저 산화한계 + 강한 계면 반응)에 있는 물질**이고, 우리가 코팅/양극 조합을 말할 때 이 논문은 **우리 SE 를 옹호하는 근거가 아니라 우리가 넘어야 할 기준선**이다."*

**그 기준선 위에서 우리에게 유리한 두 가지**:
① 우리 계면 산물의 산화물 성분(**Li₃PO₄·Li₂SO₄**)이 그들 목록의 **1·2위**다 (§7c).
② 그들 자신이 **Li₃YCl₆ 할라이드 SE + LCO** 를 긍정적으로 인용한다(ref 63·66) — 즉 **할로겐 축은 열려 있다.** 다만 그것은 Li–M–Cl 이지 Li–P–S–Cl 이 아니다.

### 7e. Q5 — ⛔ **우리 db 절대값과 섞으면 안 되는 값**

| ⛔ 금지 | 이유 |
|---|---|
| Nolan 의 **E_d 절대값**을 우리 `−0.3227 eV/atom` 과 **같은 표에** | MP hull **세대가 다르다**(2019 ↔ 2026 `GGA_GGA+U` pinned). 게다가 접촉물질이 하나도 안 겹친다. **정의 대조까지만** |
| `Fig. S7` 의 **chlorides ≈ 4.35 V** 를 "염화물계 SE 산화한계" 로 우리 표에 | Li–M–Cl **할라이드**(Li₃YCl₆ 계열)다. 우리 2.256 V 는 **S²⁻ 가 pin** 한다 — 같은 "Cl" 이라는 글자뿐 |
| 본문의 **"대부분 산화물 산화한계 3.5–4 V"** 를 수치 인용 | 계군 boxplot 을 말로 요약한 문장이다. 출처 값이 SI·XLSX 어디에도 없다 |
| `Fig. S7`·`S8`·`S9`·`S10` 의 **모든 수치** | **전부 figure-read**. 원 데이터 미공개. `figure-read ≈` 표기 없이 인용 금지 |
| `Table S1` 중 **XLSX 에 없는 8종**(LiClO₄·Li₅IO₆·LiAuO₂·Li₂PdO₃·Li₂PtO₃·LiReO₄·LiCuO₂·LiBiO₃)을 검증값으로 | 재현 불가 (§10-4) |
| `E_d = 0` 을 **"부동태화한다"·"계면저항이 낮다"** 로 번역 | 0 K 열역학 불리언이다. 속도론·계면상 두께·전자전도도는 이 양이 말하지 않는다 (저자 본인이 결론에서 인정) |
| Nolan 의 `E_d`(eV/atom) 와 **[Aykol16] 의 `E_d`(V)** 를 같은 기호로 취급 | **단위부터 다르다.** 우리 비교표에서 반드시 `E_d^{Nolan}` / `E_d^{Aykol}` 로 구별 |
| `Fig. 2` 의 **색**에서 값을 읽기 | 색축이 −80 meV/atom 근처에서 포화된다. **XLSX 를 써라** |

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

1. **★ `interface_reactivity` 의 문헌 귀속이 *세 층으로* 정리된다.** 형식화 **[Rich16]** → 끝점 준안정성 제거한 *mutual* 판 **[Zhu16]** → **양극 SOC 두 상태 전수 적용 [Nolan19]**. 우리는 `use_hull_energy=True` 를 쓰므로 **[Zhu16]/[Nolan19] 판**이다. 원고 methods 절 문장: *"the minimum mutual decomposition energy of the cathode|electrolyte pseudo-binary (Richards et al. 2016; mutual formulation of Zhu et al. 2016), evaluated as applied to cathode compatibility by Nolan et al. 2019"*.
2. **★ 추가 계산 0 → 1 짜리 작업거리: 탈리튬 양극 상태를 추가한다.** `interface_reactivity.py --contacts LiCoO2 Li0.5CoO2 CoO2 C` 한 줄. Nolan 의 전 데이터가 말하는 것은 **충전 상태가 병목**이라는 것인데, 우리 db 에는 그 열이 없다.
3. **★ `LiCoO₂ 프록시` caveat 의 방향이 확정됐다** — 과소평가 쪽이다(§7c). caveat 문구를 강화할 근거가 생겼다.
4. **★ CEI 자기부동태화 서사에 문헌 다리가 생겼다** — 우리 산물 `Li₃PO₄`·`Li₂SO₄` 가 그들 목록의 1·2위(§7c). 단 `Li₂S`·`LiCl` 은 미평가이므로 **"산화물 성분에 한해"** 라고 범위를 박아야 한다.
5. **B₂O₃ 계의 양극쪽 리스크가 수치로 잡힌다** — LNO −85.9 / LCO −56.8 meV/atom. 우리 `b2o3_esw.json`(산화 2.03 V) 과 **다른 축**의 정보다: 하나는 자기 분해, 하나는 양극과의 상호 반응.
6. **우리가 아직 안 하는 게이트 하나 더**: Nolan 은 **양극 자신이 망가지는 방향**(코팅이 양극에서 Li 를 뽑아 Co₃O₄·NiO 를 만드는 것)을 산물 목록에서 읽는다. 우리 `interface_reactivity` 산물 파싱에 **"양극 유래 상이 산물에 있는가"** 플래그를 붙이면 같은 판정이 공짜로 나온다. (계보 카드 §Answer 의 "산물 물리상태 열 / Li 소모 몰수 열" 에 이어 **세 번째 열**.)
7. **할로겐 축의 문헌 지지**: 불화물의 경향 역전(`Fig. 5a`)은 *"할로겐이 많을수록 양극쪽 고전압에 유리"* 라는 우리 modelc 서사와 **같은 방향**이다. ⚠ 단 우리 계의 onset 은 Cl 이 아니라 S²⁻ 가 정하므로(`our_dft_baseline.md`), **"Cl-rich 가 산화 onset 을 올린다" 로 번역하면 틀린다** — 우리 축은 *분해 양·산물·계면* 이다.

---

## 9. 인용 가능 문장 (deck/paper 용)

- "Nolan et al. evaluated 236 solid-state chemistries against eight cathode states (lithiated and delithiated LiCoO₂, LiNiO₂, LiNi₀.₅Mn₁.₅O₄, LiCoPO₄) using the pseudo-binary mutual decomposition energy E_d from Materials Project energies, and found that the **delithiated (charged) state imposes the binding stability constraint**." [본문 General Trends]
- "In that screening, **lithium phosphates** emerge as the most cathode-compatible chemistry for high-voltage cathodes, which the authors attribute to their intrinsically high anodic limits." [본문 Polyanion Oxides + `Fig. S7`]
- "**Lithium ternary fluorides reverse the oxide trend**: they are largely unstable with lithiated layered oxides but stable with delithiated high-voltage cathodes, making them the one class that combines high-voltage stability with Li carriers." [본문 Lithium Ternary Fluorides, `Fig. 5a`]
- "Our interfacial reaction energy is the same quantity (minimum mutual decomposition energy of the pseudo-binary, per atom, with reactant metastability removed) used by Zhu et al. and applied to cathode compatibility by Nolan et al." [§4d]
- ⚠ 조건부: "Two of the oxide products our thermodynamics predicts at the LPSCl|LiCoO₂ interface — **Li₃PO₄ and Li₂SO₄** — are, in Nolan's dataset, the two most cathode-compatible lithium ternary oxides (Li₂SO₄ is the only one stable with all eight cathode states)." *(우리 계산 + 그들 데이터의 **교차 관찰**이지 그들의 주장이 아니다 — 그렇게 밝히고 쓴다.)*
- ⛔ 쓰면 안 되는 문장: ~~"Nolan 2019 confirms our oxidation onset of 2.256 V"~~ — 그들은 황화물을 한 번도 계산하지 않았다.

---

## 10. 주의 / 한계 (over-claim 방지) — **비판적으로**

**10-1. 헤드라인 지표가 이산 SOC 두 점이다.** 실제 셀은 연속적으로 충방전한다. 중간 SOC(Li₀.₇₅CoO₂ 등)에서 더 나쁜 E_d 가 나오는 물질이 **구조적으로 잡히지 않는다**. [Xiao19] 가 μ_Li 를 연속으로 열어 같은 문제를 다루는 것과 대비된다. 논문은 이 한계를 **언급하지 않는다**.

**10-2. 상평형 산물에 `O₂` 가 고체와 같은 자격으로 들어 있다.** XLSX 상평형 문자열에 `O₂` 가 빈번하다(예: LiNiO₂+B₂O₃ → `O₂, Li₃B₇O₁₂, Ni₃BO₅`; LiTi₂(PO₄)₃+LiNiO₂ → `O₂, TiO₂, Li₃PO₄, Ni₃O₄`). **0 K·PV 무시 계산에서 기체 O₂ 는 에너지가 심하게 부정확**하고, 실제로는 셀 밖으로 빠져 반응을 비가역으로 만든다. [Aykol14] 가 가졌던 **산물 물리상태 게이트**를 이 편도 갖고 있지 않다 — **계보 카드가 #4–#7 에 물었던 물음의 답은 "복원하지 않았다"** 이다.

**10-3. "산화한계가 높으면 양극과 안정하다" 는 주장이 자기 그림에 반례를 갖고 있다.** 본문은 `Fig. S10`(LiCoPO₄ 상대, Li–M–O 만, **4개 M 족 = 약 14점**)을 근거로 이 상관을 말한다. 그런데 `Fig. S9b`(전 계군, LiCoO₂ 상대)에서 **가장 짙은 = 가장 반응성 큰 점들이 anodic limit 6.5–7.4 V 구간(불화물)에 몰려 있다.** 즉 상관은 **산화물 안에서, 탈리튬 고전압 양극 상대일 때만** 성립한다. 논문은 이 조건을 명시하지 않고 결론 문단에서 **일반 원리처럼** 쓴다. ⚠ 우리가 이 논거를 빌릴 때 **범위를 반드시 붙여야 한다**.

**10-4. `Table S1` 이 released 데이터로 재현되지 않는다.** `Table S1` 1열(LCO&L₀.₅CO 안정) 40종 중 **8종**(LiClO₄·Li₅IO₆·LiAuO₂·Li₂PdO₃·Li₂PtO₃·LiReO₄·LiCuO₂·LiBiO₃)이 **XLSX 에 아예 없다**. 나머지 32종은 XLSX 에서 정확히 재현된다(§12d). 원인은 `Fig. S1` 이 *"all the Li–M–O compounds"* 를 쓰고 `Fig. 2`/XLSX 는 *"only compositions where M is at its highest common oxidation state"* 를 쓰기 때문으로 보이나, **LiClO₄ 는 Cl 이 최고산화수(+7)인데도 빠져 있어** 이 설명이 깔끔하지 않다. `Fig. S1` 의 y 범위가 −0.44 eV/atom 까지 내려가는데 XLSX 최솟값은 −0.29 인 것도 같은 이야기다 — **공개 데이터가 논문 산출물의 부분집합**이다.

**10-5. `Fig. 2` 의 행 라벨과 XLSX 의 물질 목록이 어긋난다.** 700 dpi 확대 판독 결과 `Fig. 2` 전이금속 패널 26행은 `LiScO₂, Li₄Ti₅O₁₂, Li₂TiO₃, Li₄TiO₄, LiVO₃, Li₃VO₄, Li₂CrO₄, **Li₂NiO₃**, Li₁₀Zn₄O₉, Li₆ZnO₄, LiYO₂, Li₂ZrO₃, Li₆Zr₂O₇, LiNbO₃, Li₃NbO₄, Li₈Nb₂O₉, Li₂MoO₄, Li₄MoO₅, **Li₂PdO₃**, **LiAgO₂**, LiTa₃O₈, LiTaO₃, Li₃TaO₄, Li₅TaO₅, Li₂WO₄, Li₄WO₅` 인데, XLSX 의 전이금속 함유 26종은 그 중 `Li₂NiO₃·Li₂PdO₃·LiAgO₂` 자리에 **`Li₂CuO₂·Li₅FeO₄·LiFeO₂`** 를 갖고 있다. **3종이 맞바꿔져 있다.** (p-block 패널의 Bi 계열도 `LiBiO₃/Li₃BiO₄/Li₅BiO₅/Li₇BiO₆`(그림) ↔ `LiBiO₂/Li₃BiO₃`(XLSX) 로 달라 보이나 이쪽은 저배율 판독이라 **잠정**.) 이 논문은 이미 `Fig. 4` 라벨 오류로 **정정본을 낸 전력**이 있다 — ⇒ **그림에서 특정 물질의 값을 읽지 말고 XLSX 를 쓴다.**

**10-6. MP 세대·계산 설정이 전혀 기술되지 않는다.** functional·U 값·k-mesh·엔트리 수·스냅샷 날짜 중 **아무것도 없다**. MP hull 은 해마다 바뀌므로 **이 논문의 E_d 는 원리적으로 재현 불가**다(XLSX 덕에 *값의 재사용*은 가능하지만 *재계산 검증*은 불가). 우리 파이프라인이 `thermo_types` 를 pin 하고 엔트리 수를 기록하는 것과 대비된다 — **우리 쪽이 이 점에서는 낫다**.

**10-7. 인산염 최우수 주장이 MNO 열에서는 성립하지 않는다.** 본문은 *"among all materials considered, the lithium phosphates exhibit the best stability with lithiated and delithiated high-voltage cathodes LMNO and LCP"* 라고 쓴다. 본 digest 의 재계산으로는 **LCP·CP 에서는 압도적으로 맞다**(4원 인산염 Ed=0 비율 76 %·56 %). 그러나 **MNO 열에서는 인산염 8 % < 이원 산화물 28 % < 불화물 19 % > 붕산염 13 %** 로, 인산염이 최우수가 아니다. (⚠ 우리 군 분류가 `Fig. 5b` 의 *Li phosphates* 정의와 다를 수 있다 — 그럼에도 본문 문장이 **MNO 까지 포함하는 것처럼 읽히는 것은 과잉**이다.)

**10-8. 이온수송이 없다.** 저자 스스로 마지막 문단에서 인정한다. `E_d = 0` 이지만 Li⁺ 전도가 0 인 물질(BeO·ZrO₂·HfO₂)이 목록 상위에 그대로 남아 있다 — **8/8 안정 2종 중 하나가 BeO 다**(독성). [Aykol16] 이 갖고 있던 **역할별 게이트·공급위험(HHI) 축**이 여기엔 없다.

**10-9. 다만 공정하게 — 이 편이 잘한 것.** ① **전 데이터 공개**(XLSX 1,896행 + 상평형 문자열까지) — #1·#2·#3 을 통틀어 가장 검증 가능하다. ② **양극 SOC 를 두 상태로 분리**한 것은 이 계보에서 이 편이 처음이고, 결론(충전 상태가 병목)은 실험 관찰(Co₃O₄·암염 NiO)과 맞는다. ③ 프록시(LNO↔NMC/NCA)를 **따로 검증**했다. ④ 자기 예측이 기존 실험 코팅을 재현하는지 **명시적으로 대조**했다.

---

## 11. 기법 미니 용어집 (이 논문을 읽는 데 필요한 것만)

| 용어 | 뜻 | 우리 쪽 대응 |
|---|---|---|
| **pseudo-binary** | 두 물질을 "가상의 이성분계" 로 보고 조성축 x 를 훑는 것. 계면을 원자 모형 없이 **조성 혼합**으로 근사 | `InterfacialReactivity` 의 x |
| **phase equilibria (PE)** | 그 조성에서 총에너지가 최소가 되는 상들의 조합 (convex hull 의 해당 simplex 꼭짓점들) | `Reaction` 문자열 |
| **decomposition energy ΔE_D** | 어떤 상이 자기 조성의 상평형보다 얼마나 높은가 (= −E_hull) | `e_above_hull` 의 부호 반대 |
| **mutual decomposition energy** | ΔE_D 에서 **두 끝점 자신의 준안정성**을 뺀 것. "섞어서 새로 생긴 반응성" 만 남긴다 | `use_hull_energy=True` |
| **E_d** (이 논문) | `min_x` mutual decomposition energy, **eV/atom**, 음수 | `min_reaction_energy_eV_per_atom` |
| **anodic / cathodic limit** | μ_Li 개방 grand-potential 에서의 산화 / 환원 개시 전압 (vs Li/Li⁺) | `oxidation_limit_V` / `reduction_limit_V` |
| **L₀.₅CO / MNO / CP** | 탈리튬화(충전) 양극 상태의 약칭 (`Li₀.₅CoO₂` / `Ni₀.₅Mn₁.₅O₄` / `CoPO₄`) | — |
| **highest common oxidation state** | `Fig. 2` 의 포함 필터 — 각 M 의 "통상 최고 산화수" 조성만 heatmap 에 넣음 | §10-4 참조 |
| **swarmplot** | 점을 겹치지 않게 흩뿌린 1차원 분포도 (`Fig. S1`) | — |

---

## 12. ★ 독립 재현 — SI XLSX **1,888 쌍 전수 재분석**

> 이 절의 모든 숫자는 `litdb/inbox/108. Sup2) …xlsx` 를 직접 파싱해 계산한 것이다.
> 논문에 **인쇄돼 있지 않은** 정량이 여럿 나온다.

### 12a. 본문 인용값 검증 → **7/7 일치**

§3b 표 참조. 본문이 meV 단위로 반올림해 쓴 6개 값과 "stable" 5개가 **전부 XLSX 와 일치**. ⇒ 본문↔데이터의 무결성은 좋다 (문제는 §10-4·10-5 의 **목록 범위**이지 값이 아니다).

### 12b. 🔑 **논문에 없는 산출: "전부 안정" 목록** (8 양극상태 전부 Ed=0)

| 조건 | 통과 물질 |
|---|---|
| **8/8** | **`Li₂SO₄`(Li 삼원 산화물), `BeO`(이원 산화물)** — **단 2종 / 236종 (0.85 %)** |
| **7/8** | `CsLi(B₃O₅)₂`(LNO −4.4) · `LiNO₃`(MNO −5.5) · `Li₂SeO₄`(MNO −1.7) · `ZrO₂`(CP −59.5) · `HfO₂`(CP −63.7) |
| **6/8** | 13종 — 그중 **`Li₃PO₄`**(MNO −11.5, CP −1.1) · `Li₃AsO₄` · `Li₂MoO₄` · `Li₂CrO₄` · `LiYF₄` · `ZnO` · `TiO₂` · `SnO₂` · `Sc₂O₃` · `PbO₂` · `In₂O₃` · `Tl₂O₃` · `BaLi(B₃O₅)₃` |

전체 분포 (Ed=0 인 양극상태 수):

| 8/8 | 7/8 | 6/8 | 5/8 | 4/8 | 3/8 | 2/8 | 1/8 | 0/8 |
|---|---|---|---|---|---|---|---|---|
| 2 | 5 | 13 | 43 | 46 | 25 | 70 | 16 | 16 |

🔑 **이것이 이 논문의 진짜 결론이다**: *"고전압 양극까지 포함해 전 상태에서 열역학적으로 안정한 고체 화학은 사실상 존재하지 않는다."* 그리고 남은 둘은 **BeO(독성·Li 전도 0)** 와 **Li₂SO₄(흡습성·저 전도)** 로, 실용성이 없다. ⇒ 실무 결론은 *"완전 안정" 이 아니라 **"어느 상태에서 얼마나 타협하는가"*** 가 된다. 그 관점에서 **`Li₃PO₄` 가 사실상의 승자**다(잔여 반응이 −11.5/−1.1 meV/atom 로 열적 소음 수준).

### 12c. 🔑 Li 함량 규칙의 **정량화** (논문은 `Fig. S1` 로 정성만 보여준다)

접촉물질의 **Li 원자분율** vs `E_d` 의 Pearson r (Li 함유 물질 196종, 이원 산화물 제외):

| 양극 | r | 읽기 |
|---|---|---|
| **LiCoO₂** (리튬화) | **+0.321** | Li 많을수록 **덜** 반응 |
| **LiNiO₂** (리튬화) | **+0.367** | 〃 |
| Li₀.₅CoO₂ (탈리튬) | −0.176 | Li 많을수록 **더** 반응 (약함) |
| **MNO** (탈리튬 고전압) | **−0.601** | 〃 (강함) |
| **CoPO₄** (탈리튬 고전압) | **−0.612** | 〃 (강함) |

⇒ **부호가 SOC 에 따라 정확히 뒤집힌다.** 본문의 정성 서술이 데이터에서 깨끗하게 확인된다. 이것은 *"단일 코팅으로 양 상태를 다 만족시키기 어렵다"* 의 **수치 근거**다.

### 12d. `Table S1` 재현

| Table S1 열 | 인쇄된 종 수 (좌표 복원) | XLSX 에서 재현 | 차이 |
|---|---|---|---|
| Stable with LCO & L₀.₅CO | **40** | **32** | XLSX 에 **아예 없는 8종**: LiClO₄·Li₅IO₆·LiAuO₂·Li₂PdO₃·Li₂PtO₃·LiReO₄·LiCuO₂·LiBiO₃ |
| Stable with LNO & L₀.₅NO | 28 | (부분) | 〃 |
| Stable with LNO·L₀.₅NO·L₀.₂₅NO | 14 | **재현 불가** — XLSX 에 `Li₀.₂₅NiO₂` 열이 없다 | — |
| **Stable with all** (= 위 5 상태) | **14** | 〃 | — |

**XLSX 에 있는 32종은 전부 정확히 일치**(누락도 과잉도 0). ⇒ 값은 맞고 **범위가 다르다**.
🔑 그리고 3열과 4열이 **글자 그대로 동일한 14종**이다 — 즉 `Li₀.₂₅NiO₂` 까지 버티는 물질은 자동으로 LCO 쌍도 통과한다.

### 12e. 계군 × 양극 **Ed=0 비율** 전표 (논문 `Fig. 5b` 의 정량판)

| 물질군 | LCO | L₀.₅CO | LNO | L₀.₅NO | LMNO | MNO | LCP | CP |
|---|---|---|---|---|---|---|---|---|
| Li 삼원 산화물 (72) | **81 %** | 54 % | 62 % | 40 % | 49 % | **3 %** | 18 % | 8 % |
| 이원 산화물 (40) | 48 % | **65 %** | 32 % | 38 % | 62 % | 28 % | 48 % | 22 % |
| 4원 폴리음이온 (97) | 67 % | 65 % | 47 % | 49 % | 56 % | 8 % | 31 % | 15 % |
| Li 삼원 불화물 (27) | **4 %** | 26 % | **4 %** | 7 % | 37 % | 19 % | **67 %** | **81 %** |
| └ 4원 **인산염**(25) | 8 % | 52 % | 4 % | 8 % | 48 % | 8 % | **76 %** | **56 %** |
| └ 4원 **붕산염**(47) | 81 % | 72 % | 60 % | 60 % | 53 % | 13 % | 17 % | 2 % |
| └ 4원 **규산염**(27) | **93 %** | 67 % | 63 % | 67 % | 67 % | 0 % | 15 % | 0 % |

계군 **중앙값 Ed** (meV/atom):

| 물질군 | LCO | L₀.₅CO | LNO | L₀.₅NO | LMNO | MNO | LCP | CP |
|---|---|---|---|---|---|---|---|---|
| Li 삼원 산화물 | 0.0 | 0.0 | 0.0 | −12.2 | −4.3 | −57.1 | −33.1 | **−95.9** |
| 이원 산화물 | −4.0 | 0.0 | −30.5 | −20.3 | 0.0 | −9.6 | −2.9 | −61.6 |
| 4원 폴리음이온 | 0.0 | 0.0 | −2.8 | −0.3 | 0.0 | −32.7 | −11.1 | −67.0 |
| Li 삼원 불화물 | **−75.2** | −13.1 | **−113.0** | −70.7 | −12.3 | −14.4 | **0.0** | **0.0** |

⇒ **불화물 행의 좌우 대칭 반전**이 한눈에 보인다. 그리고 **CoPO₄ 열이 어느 군에서나 최악**이다(불화물만 예외).

---

## 13. 남은 물음 (다음 digest 로 넘김)

- **Q-A.** `Fig. S7`·`S8` 의 anodic/cathodic limit 데이터는 어느 논문의 것인가 — Wang/Bai/**Nolan**/Liu/Gong/Sun/Mo *Angew* **2019**, 58, 8039 (ref 63, "Lithium Chlorides and Bromides as Promising Solid-State Chemistries…") 로 보인다. **그 편이 우리 2.256 V 와 *직접* 비교 가능한 값을 갖고 있을 가능성이 높다** (Li–Cl/Li–Br 계의 grand-potential 창). → 세트에 없는 편이지만 **다음 우선순위 후보**.
- **Q-B.** #7 리뷰(Nolan/Zhu/He/Bai/Mo *Joule* 2018 — 본 논문 ref 23)가 **anodic limit 의 식을 적어 두었을 것이다.** 본 논문이 생략한 정의를 거기서 확정할 것.
- **Q-C.** [Xiao19] 의 `|ΔE_rxt| < 100 meV/atom` 게이트와 Nolan 의 `E_d = 0` 게이트는 **같은 양에 다른 문턱**이다. 우리 `interface_reactivity` 에 문턱을 도입할 때 어느 쪽을 따를지 — **[Xiao19] digest 와 대조 필요**.
- **Q-D.** 우리 `−0.3227 eV/atom`(= −323 meV/atom) 은 Nolan 데이터셋의 **최악 구간**(이원 산화물 CoPO₄ 쌍 −334…−534)에 해당한다. 이것이 **황화물이라서**인지 **hull 세대 차이**인지 — 같은 MP 세대에서 `Li₃PO₄+LiCoO₂` 를 우리 코드로 돌려 **0 이 나오는지** 확인하면 즉시 갈린다. **대조 잡 1건으로 검증 가능** (추천).

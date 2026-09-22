<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-22 초판 — 본문(7 pp) + SI(8 pp) 전문, 그림 14장 크롭 중 **9장 실독**.
     ⭐ 이 digest 의 1번 임무는 `ncube2026_…` 이 남긴 미결(치환에너지 정의 부재)의 해소였다.
        결론: **5/5 다 적혀 있다**(§4.2). 그리고 Ncube 의 두 수치는 이 논문과 **부호가 안 맞는다**(§7a).
     ⚠ 본문에 수치 표가 없다 — **교환에너지 ~40개가 전부 막대그래프 안에 있다**.
        그래서 §3b–3d 는 전량 `figure-read ≈` 이고, 본문이 활자로 준 두 값(−2.18 / −1.1 eV)으로
        눈금을 교정했다(오차 ±0.05 eV). 본문 서술과 어긋나는 것 6건은 §10-⑨ 에 모았다. -->

# Cation Mixing Properties toward Co Diffusion at the LiCoO₂ Cathode/Sulfide Electrolyte Interface in a Solid-State Battery — Haruyama, Sodeyama, Tateyama (*ACS Appl. Mater. Interfaces* **9**, 286–292 (2017))

> slug `haruyama2017_cation_mixing_co_diffusion_lco_lps` · DOI `10.1021/acsami.6b08435` · type `계산 100 % (정적 DFT+U 슬랩 계면 — MD·NEB 0회)` · PDF `inbox/10. ACSAMI_2017_Haruyama_…_MAIN.pdf` (본문 7 pp, Fig 1–4) + **SI** `inbox/10. Sup) …_SI.pdf` (8 pp, S1–S4 절 · Fig S1–S7 · Table S1–S3) · digested `2026-09-22` · status ✅ · 태그 **[외부]**

> elements: Li, Co, O, P, S, Nb
> methods: DFT, DOS, PDOS

> **저자**: **Jun Haruyama\***(NIMS GREEN) · **Keitaro Sodeyama**(NIMS CMI² + Kyoto ESICB + JST PRESTO) · **Yoshitaka Tateyama\***(NIMS CMI²/GREEN + Kyoto ESICB) · 접수 2016-07-10 / 수리 2016-12-06 / 온라인 2016-12-19 · JSPS·MEXT KAKENHI JP16K17969·JP15K05138·JP15H05701 · HPCI hp150055/hp150068/hp160040/hp160080
>
> **계보**: 실험 원점 [Sakuda 2010 *Chem. Mater.* 22, 949](ref 24 — LCO\|Li₂S–P₂S₅ TEM-EDX, **Co 가 계면에서 50 nm 까지 퍼진 것을 처음 본 편**) + [Ohtomo 2013](ref 25 — 버퍼층이 Co 유출을 줄임) + [Woo 2012 Al₂O₃ ALD](ref 26) → **자기 선행 [Haruyama 2014 *Chem. Mater.* 26, 4248](ref 21 — 같은 세 계면을 처음 만든 편, SCL 기전)** → **본 논문**(그 계면에 **양이온 교환**을 넣는다). 열역학 이웃 = [Zhu 2015](ref 27)·[Zhu 2016](ref 28)·[**Richards 2016**](ref 29 — **우리 §B 의 방법 원전**)·[Yokokawa 2016](ref 30). **후속**: [**Ncube 2026**](`papers/ncube2026_ionic_interdiffusion_lco_lgps_multiscale.md`) 이 이 논문을 **ref 13 으로 인용**하며 같은 질문을 ns·μm 으로 올린다.
>
> ⚠ **우리 db 에 이미 선행편이 있다** — `db/literature/refs.json` `references[37] = "haruyama2014"` 가 **이 논문의 계면 3종을 만든 편**이고, 우리 paper #1 v5 **single-interface + vacuum** 방법의 **1차 근거**로 등록돼 있다. 즉 **우리는 이미 이 그룹의 기하를 쓰고 있다.** 이 2017 편은 그 위에 얹힌 화학이다.

---

## 0. 이 digest 를 읽는 법 — 왜 이 논문을 구했나

**두 가지 임무를 안고 왔다.**

1. **미결 해소.** 방금 들어온 `ncube2026_ionic_interdiffusion_lco_lgps_multiscale` 의 DFT 층은 **치환에너지 2개**(−1.109 / +0.144 eV)가 전부였고 **정의가 한 줄도 없었다** — 참조상태·전하규약·셀 크기·자리 샘플링·스핀 5개 전부 미기재. 우리 보고량 카드 규율로는 *스칼라 보고량이 정의되지 않은 상태*였다. **그 정의가 이 논문(= Ncube 의 직계 선행, ref 13)에 있는가?**
   → **§4.2 에 답이 있다. 5/5 다 적혀 있고, 원시 총에너지까지 `Table S3` 로 공개돼 있어 우리가 재현했다**(3개 값 전부 소수 셋째 자리까지 일치, §3e).
   → **그리고 더 값진 것이 나왔다: Ncube 의 두 수치가 이 논문과 부호·크기가 안 맞는다**(§7a).

2. **우리 §B 의 원자단위 짝 찾기.** 우리 `comp1|LiCoO₂ −0.3227 eV/atom`(MP hull grand-potential)의 **산물이 `Co₉S₈ + Li₃PO₄ + Li₂SO₄ + Li₂S + LiCl`** 이다. 즉 우리 계산은 *"Co 는 S 로, P 는 O 로 간다"* 를 **종점**으로 말한다. 이 논문은 **그 교환의 첫 원자 한 걸음**(`Co ↔ P` 스왑)을 계면에서 직접 계산한다.
   → **§6·§7b 가 이 digest 의 최고 수확이다: 두 방법이 벌크에서는 부호가 반대고, 계면에서 비로소 같아진다.**

> **⚠ 물질계 근접도 — Ncube 보다 훨씬 가깝다.**
> SE 가 **β-Li₃PS₄**(Pnma, PS₄³⁻ 골격)다. 우리 Li₆PS₅Cl 은 **같은 PS₄³⁻ 골격** + free S²⁻(4a/4d) + Cl⁻ 다. Ncube 의 LGPS 는 GeS₄ 가 섞여 있다. ⇒ **Co↔P 화학은 우리 계로 이식 가능성이 가장 높은 문헌 항목**이다.
> ⛔ 그래도 **어떤 수치도 우리 원장에 이식하지 않는다.** 아지로다이트에는 β-LPS 에 없는 **free S²⁻ 와 Cl⁻** 가 있고, 우리 ESW onset 은 바로 그 free S²⁻ 가 정한다(`our_dft_baseline.md`). Co 가 **PS₄ 의 P 자리**로 갈지 **free S 자리 주변**으로 갈지 **Cl 자리**로 갈지는 **이 논문이 답할 수 없는 질문**이다 (§11-③ 의 계산 제안).

> **본 digest 에서 실제로 본 그림 (2026-09-22)** — 크롭 14장(본문 4 + SI 7 + 표 3) 중 **9장 실독**.
> **본문 4/4**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` — **전부 봤다. 이 논문의 수치가 거기 말고는 없기 때문이다.**
> **SI 5/7**: `Fig. S1`(계면 3종 pristine) · `Fig. S3`(Co1↔P3 vs Co2↔P3 완화구조) · `Fig. S5`(벌크 PDOS) · `Fig. S6`(6회 교환 구조) · `Fig. S7`(Li 공공 형성에너지).
> **안 본 것 (2장 + 표 3장)**: `Fig. S2`(Co↔Li 완화구조 — 수치 없음, 본문 서술로 충분) · `Fig. S4`(결합길이 — **PDF 텍스트 레이어에 12개 값이 전부 그대로 있고 우리가 평균까지 검산했다**, 이미지로 볼 이유 없음) · `Table S1`·`S2`·`S3`(표 — PDF 텍스트가 정확).
> 🔴 **수치의 소재가 특이하다**: 이 논문은 **본문에도 SI 에도 교환에너지 표가 없다.** ~40개 값이 **전부 막대그래프 안에** 있다. 그래서 §3b–3d 는 전량 **`figure-read ≈`** 이고, 본문이 활자로 준 **−2.18 eV**(Co2↔P3)와 **−1.1 eV**(P1↔Nb1)로 눈금을 맞췄다 — 두 점 모두 내 판독과 **±0.05 eV 이내**로 일치했으므로 나머지 값도 그 정도 정밀도로 본다.
> **우리가 직접 한 산수**는 `*우리 산수*` 로 표시했다 (논문 주장 아님).

---

## 1. 한 줄 요약

**LiCoO₂\|β-Li₃PS₄ 계면에서 Co 는 Li 자리로 가지 않는다 — P 자리로 간다.** `Co ↔ Li` 교환은 전부 흡열(`figure-read ≈` **+0.20 ~ +3.38 eV**)이라 Co 가 LPS 의 Li 격자를 타고 확산하는 경로는 막혀 있는데, `Co ↔ P` 교환은 **16개 조합 전부 발열**(`figure-read ≈` **−0.95 ~ −3.78 eV**, 본문 인용값 **Co2↔P3 = −2.18 eV**)이다. 즉 **Co 는 PS₄ 사면체의 P 와 자리를 바꿔 CoS₄ 가 되고, 쫓겨난 P 는 CoO₂ 층으로 들어가 PO₆/PO₄ 가 된다.**

**왜 그렇게 유리한가 — 이 논문의 진짜 발견은 여기다.** 같은 교환을 **LCO 벌크와 LPS 벌크에서 따로** 하면 **+1.98 eV(흡열)** 다. 계면에서만 **−2.18 eV** 다. **부호가 뒤집히고 차이가 4.16 eV** 다(*우리 산수*). 원인은 계면에만 있는 **CoO₄ 유사사면체 유래 갭 내 준위**다 — P_Co 결함이 내놓는 **전자 2개**가 벌크에서는 LCO 전도대(`figure-read ≈` VBM+2.05 eV)까지 올라가야 하는데, 계면에서는 그 낮은 준위에 그냥 앉는다. **Li 를 건너보내 전하를 갚는 경로**(P_Co+2V_Li \| Co_P+2Li_i)는 계면에서 **−0.9 eV** 로 오히려 **1.28 eV 손해**라 주된 원인이 아니다 — **전자적 효과가 지배한다.**

**버퍼층(LiNbO₃)은 그 고리를 끊는다.** `Co ↔ Nb`(LCO\|LNO)는 `figure-read ≈` **+0.93 ~ +1.27 eV** 로 흡열이다. 이유는 **Co 와 Nb 가 둘 다 팔면체**라 CoO₄ 사면체 준위가 안 생기기 때문이다. ⚠ **단 예외가 하나 있고 논문이 스스로 적어 뒀다** — LNO\|LPS 계면의 **사면체 NbO₄ 자리(Nb1)** 에서는 `P1↔Nb1 = −1.1 eV` 로 **발열**이다. 저자는 *"코팅은 비정질이지만 사면체 자리가 그리 많지는 않을 것"* 이라고 **가정으로** 넘긴다.

**마지막 고리 — 이게 우리 축에 제일 아프다.** Co↔P 가 6회 일어난 계면에서 **Li 공공 형성에너지가 전부 낮아진다** (`Fig. S7`, LCO 쪽 **3.2–4.0 → 2.2–2.8 eV**, 계면 Li **3.3 → 1.6 eV**, LPS 쪽 최저 **1.4 → 0.9 eV**). ⇒ **양이온 혼합이 Li 고갈층(SCL) 성장을 가속한다.** 저자 표현: *"one P_Co defect can produce two additional Li vacancies."*

⚠ 이 서사의 취약점은 **네 겹**이다(§10): ① **스핀 비편극** — 그런데 기전을 떠받치는 CoO₄ 가 저자 자신이 *"스핀이 중요해지는 유일한 구조"* 라고 적은 바로 그것이다 ② **동역학이 0** — NEB·장벽·MD 가 한 건도 없는데 결론은 *"proceed rapidly"* 다 ③ **버퍼층 표본이 1/5** (LCO\|LPS 28조합 vs LCO\|LNO 6조합) ④ **4.16 eV 를 전자항에 전부 귀속**했지만 밴드정렬로 설명되는 것은 그중 **~2.5–3.3 eV** 뿐이다(*우리 산수*).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| **계 1 (문제)** | **LCO(110) \| LPS(010)** — LiCoO₂ 층상 양극 × **β-Li₃PS₄** 황화물 SE |
| **계 2 (해법)** | **LCO(110) \| LNO(1̄10)** 과 **LNO(1̄10) \| LPS(010)** — LiNbO₃ 버퍼층을 **두 계면으로 쪼개서** 각각 계산 |
| 던지는 질문 | (a) Sakuda 의 TEM 이 본 **"Co 가 SE 쪽 50 nm 까지 퍼짐"** 의 **원자 단위 첫 걸음**이 무엇인가 (b) 그 걸음이 **에너지적으로 유리한가** (c) **왜** 유리한가 (구조? 정전기? 전자구조?) (d) **LNO 버퍼가 왜 막는가** (e) 그 혼합이 **Li 수송에 무엇을 하는가** |
| 문헌 갭 (저자 주장) | 계면저항의 두 후보 기전 중 **① SCL** 은 자기 선행(2014)에서 다뤘지만 *"작동 셀에서 Li 고갈을 직접 본 증거가 없고"* Debye 차폐길이로 크기가 설명 안 된다. **② 미세구조·조성 변화(상호확산)** 는 실험(Sakuda·Ohtomo·Woo)과 열역학 예측(Zhu·Richards·Yokokawa)이 **둘 다 가리키는데 원자 기전이 없다** |
| 그들의 답 | **양이온 교환(cation exchange)을 기본 단위 사건(elementary step)으로 놓고** 그 에너지를 계면에서 전수 계산한다 |
| 방법 스탠스 (저자 자인, 중요) | *"the slabs of these interfaces are assumed to be sharp and the materials are largely intact with small distortions. … **this study only corresponds to either the early stage of interfacial reaction, or if the interface is kinetically stabilized.**"* ⇒ **중간층(interlayer) 형성 이후는 다루지 않는다고 스스로 못박았다** |
| ⛔ **안 다룬 것 (저자 자인 + 우리 확인)** | **전압을 직접 안 건다**(*"our simulation interface cell does not treat the cathode voltage directly"*, 전압 논의는 전부 Li 공공 형성에너지 경유) · **동역학 전무**(NEB·장벽·MD 0회) · **최종 배열이 아님**(*"not necessarily the final configurations"*) · **비정질화·핵생성은 추론만** · **Li 확산장벽 변화는 future work 로 명시** |

---

## 3. 핵심 수치 총정리 ★

> ⚠ **전부 소환값이다.** 물질계(β-Li₃PS₄)와 보고량(교환에너지)이 우리와 다르므로 `db/properties/*` 와 같은 표에 놓지 않는다.
> 🔴 **§3b–3d 는 전량 막대그래프 판독**이다 — 이 논문에 교환에너지 표가 없다.

### 3a. 계·계면 건설 (`Table S1` · `Table S2` · `Fig. S1`)

| 항목 | 값 | 출처 |
|---|---|---|
| 계면 3종 | **LCO(110)/LPS(010)** · **LCO(110)/LNO(1̄10)** · **LNO(1̄10)/LPS(010)** | 본문 Methods |
| 계면 출처 | ⭐ **이 논문이 만든 게 아니다** — *"The three interfaces were constructed in our previous study"* = **[Haruyama 2014 *Chem. Mater.* 26, 4248]** | 본문 |
| 기하 | **단일 계면 + 진공** (`Fig. S1` 의 셀 상자 양끝이 비어 있다 · `figure-read ≈` **14–16 Å**, 2014 편 기록 **~1.5 nm** 와 일치) | `Fig. S1`·`Fig. S6` |
| 슬랩 두께 | **1–2 nm/쪽** (2014 편 기록, `db/literature/refs.json`) | 외부 |
| LCO/LPS 셀 | **a 13.94 · b 24.46 · c 43.61 Å · γ 87.4°** — *우리 산수*: 면내 **A = 340.6 Å²**, 셀부피 14,854 Å³ | `Table S1` |
| LCO/LNO 셀 | **a 14.32 · b 9.98 · c 38.03 Å · γ 89.8°** — *우리 산수*: **A = 142.9 Å²** | `Table S1` |
| LNO/LPS 셀 | **a 12.79 · b 31.15 · c 44.90 Å · γ 90.0°** — *우리 산수*: **A = 398.4 Å²** | `Table S1` |
| 격자 부정합 | **LCO/LNO(1̄10) 3.4 % · LCO/LNO(110) 5.2 % · LCO/LPS 3.7 % · LNO/LPS 3.6 %** (2014 편) | 외부 `refs.json` |
| 계면 탐색 절차 (2014 편) | 벌크 완화 → 화학량론 슬랩+진공 완화 → 측방 확대 후 상대 슬라이드 **16 / 4 / 9 표본**(LCO/LNO, LCO/LPS, LNO/LPS) → **전 원자 + 측방 격자 완화** → 최저에너지 채택. **FixAtoms 없음** | 외부 `refs.json` |
| LPS 구조 처리 ⭐ | **β-Li₃PS₄-b** (Lepley 2013, ref S9) — **4c 자리 Li 를 제거해 분율점유를 정수화**. Li_i 계산 때는 **그 4c 자리에 넣는다** | SI §S1 |
| LCO 벌크 셀 | **144 원자** `Li₃₆Co₃₆O₇₂` · SI 본문은 *"tetragonal"* 인데 `Table S2` 는 **Hexagonal a=b=9.821 · c=14.04 Å** (⚠ 내부 불일치, §10-⑩) · k **2×2×1** | SI §S1 · `Table S2` |
| LPS 벌크 셀 | **128 원자** `Li₄₈P₁₆S₆₄` · Orthorhombic **a 13.13 · b 16.12 · c 12.36 Å** · k **2×2×2** | SI §S1 · `Table S2` |
| 시각화 | **VESTA** (ref 44) | 본문 |

> 🔑 **여기가 우리 방법과 직접 이어진다.** `db/literature/refs.json` 이 이미 *"v5 = Haruyama 방법 + UMA 안정화 핵"* 으로 판정해 뒀다. 차이는 **FixAtoms 하나뿐**이다 — 그들은 전 원자를 푼다, 우리는 UMA 의 진공 OOD 때문에 하단 1/3 을 묶는다. ⇒ **이 논문의 교환에너지를 우리가 재현하려 한다면, 그 FixAtoms 가 첫 번째 계통오차 후보다.**

### 3b. `Co ↔ Li` 교환에너지 — **LCO/LPS**, 전부 양수 (`Fig. 1b`, 전량 `figure-read ≈`)

> 자리 정의: **Li1–3 = LiS₆ (Pnma 4b)** · **Li4–6 = LiS₄ (8d)** · Li1·Li4 는 **CoO₂ 층 모서리에 흡착**된 것 · **Co1 = CoO₄** · **Co2 = CoO₆**.

| Li 자리 | Co1 ↔ Li (eV) | Co2 ↔ Li (eV) |
|---|---|---|
| **Li1** (LiS₆, 흡착) | **≈ +0.25** | **≈ +0.20** ← 전체 최저 |
| Li2 (LiS₆) | ≈ +0.92 | ≈ +2.86 |
| Li3 (LiS₆) | ≈ +1.32 | ≈ +2.10 |
| Li4 (LiS₄, 흡착) | ≈ +0.73 | ≈ +2.40 |
| Li5 (LiS₄) | ≈ +1.65 | **≈ +3.38** ← 전체 최고 |
| Li6 (LiS₄) | ≈ +1.82 | ≈ +2.40 |

- 본문 요약: *"the Co atoms can only migrate to the neighboring Li sites, while Co diffusions through the Li sites in the LPS seems unlikely."*
- 본문: *"the LiS₄ sites have slightly higher exchange energies than those of the LiS₆ sites"* — ✅ 판독으로 확인. *우리 산수*: 흡착 자리(Li1·Li4) 제외 시 Co1 은 LiS₆ 평균 1.12 vs LiS₄ 1.74 / Co2 는 2.48 vs 2.89.
- 본문: *"the exchange energies of distant Co atoms show no significant differences compared with that of Co2"* ⇒ **깊은 Co 는 Co2 와 같다**(값 미제시).
- 🔴 **본문 vs 그림 ①**: 본문은 Li2–6 을 *"1−3 eV"* 라 쓰는데, **Co1↔Li2 ≈ 0.92 · Co1↔Li4 ≈ 0.73 은 1 eV 아래**고 **Co2↔Li5 ≈ 3.38 은 3 eV 위**다. 실범위는 **≈ 0.7–3.4 eV**.
- 🔴 **본문 vs 그림 ②**: 본문은 저에너지 경로를 **Co1 관점에서만** 서술하는데, 그림에서 **가장 낮은 막대는 Co2↔Li1 (≈ 0.20)** 이다.

### 3c. `Co ↔ P` 교환에너지 — **LCO/LPS**, 16개 전부 음수 ★★ (`Fig. 2b`, 전량 `figure-read ≈`)

> 자리: **Co1 = CoO₄(계면 모서리)** · **Co2 = CoO₆(계면 근접)** · **Co3·Co4 = CoO₆(안쪽)** · **P1–P4 = 전부 PS₄**, P1 이 경계에 가장 가깝고 P4 가 가장 멀다.

| P 자리 | Co1↔P | **Co2↔P** | Co3↔P | Co4↔P |
|---|---|---|---|---|
| **P1** (경계 최근접) | ≈ −2.78 | **≈ −3.78** ← **논문 전체 최저** | ≈ −2.92 | ≈ −2.83 |
| P2 | ≈ −2.25 | ≈ −2.40 | ≈ −1.33 | ≈ −1.02 |
| P3 | ≈ −1.45 | **−2.18 (본문 활자값 ✅)** | ≈ −1.15 | ≈ −1.28 |
| P4 (가장 멂) | ≈ −1.38 | ≈ −1.75 | ≈ −1.38 | ≈ −0.95 |

- ✅ **눈금 교정점**: `Co2↔P3` 을 본문이 **−2.18 eV** 로 활자로 준다. 내 판독도 −2.18 ⇒ **이 표의 판독 정밀도 ≈ ±0.05 eV**.
- 경향 ①: **P 가 경계에 가까울수록 더 음수** (P1 열이 전부 −2.8 이하).
- 경향 ②: 본문 — *"Except for the Co1 atom, the Co atoms close to the LCO/LPS boundary show lower exchange energies than those far from the boundary"* ✅ P3 열에서 Co2(−2.18) < Co3(−1.15)·Co4(−1.28).
- **Co1 이 예외인 이유(구조)**: `Co1↔P3` 에서는 들어온 P 가 **2층 CoO₆ 의 O 를 빼앗아** `PO₄ + CoO₅` 를 만든다(구조 재배열 비용). `Co2↔P3` 에서는 그 재배열 없이 **PO₆ 팔면체가 바로 생긴다**. (`Fig. S3` 실독으로 확인 — (a) 에서 P3 다면체가 층 모서리에 걸쳐 일그러져 있고 O 가 돌출한다. 두 경우 모두 **쫓겨난 Co 는 LPS 안에서 짙은 파란 CoS₄ 사면체**가 된다.)
- 🔴 **본문 vs 그림 ③**: 본문은 *"negative (less than −1 eV)"* 인데 **Co4↔P4 ≈ −0.95 는 −1 보다 위**다.
- 🔴 **본문 vs 그림 ④ (제일 중요)**: **논문 전체 최대 구동력은 `Co2↔P1 ≈ −3.78 eV` 인데 본문·초록·결론 어디에도 이 값이 없다.** 본문이 끌고 가는 수는 −2.18 이다.

### 3d. 버퍼층 — **LCO/LNO** 과 **LNO/LPS** (`Fig. 3c,d`, 전량 `figure-read ≈`)

**(i) LCO(110)/LNO(1̄10)** — Co 가 버퍼로 들어갈 수 있나. **Co 는 경계 최근접 CoO₆ 1개(Co1)만 골랐다.**

| 상대 자리 | Co1 ↔ Li (eV) | Co1 ↔ Nb (eV) |
|---|---|---|
| 1 | ≈ +1.27 | ≈ +1.27 |
| 2 | ≈ +2.00 | ≈ +1.01 |
| 3 | ≈ +2.36 | ≈ +0.93 |

- 본문: *"positive, being 1−2 and 1 eV, respectively"*. 🔴 **본문 vs 그림 ⑤**: Co↔Li 최대는 **≈ 2.36** 으로 *"1–2"* 밖이다.
- ⇒ **Co 는 LNO 로 못 들어간다** (모든 경로 흡열).

**(ii) LNO(1̄10)/LPS(010)** — P 가 버퍼를 먹을 수 있나. **P 는 경계 최근접 PS₄ 1개(P1)만 골랐다.** **Nb1 은 NbO₄ 사면체, Nb2·Nb3 은 NbO₆ 팔면체.**

| 상대 자리 | P1 ↔ Li (eV) | P1 ↔ Nb (eV) |
|---|---|---|
| 1 | ≈ +2.25 | 🔴 **≈ −1.05** (본문 활자 **−1.1** ✅) ← **사면체 NbO₄** |
| 2 | ≈ +4.55 | ≈ +1.22 |
| 3 | ≈ +3.30 | ≈ +1.60 |

- ✅ **두 번째 눈금 교정점**: 본문 −1.1 vs 내 판독 −1.05.
- 본문 해석: *"The negative exchange energy of P1↔Nb1 (−1.1 eV) indicates that the **NbO₄ tetrahedrons can be replaced by PO₄ tetrahedrons**. If LNO contains a large amount of NbO₆ octahedrons, the P atom cannot alternate the Nb atom. Although coated buffer layers are regarded to be an amorphouslike phase, **we expect that there are not too many tetrahedral sites.**"*
- 🔴 **이 한 줄이 이 논문에서 가장 약한 논증이다** — 실제 코팅은 비정질이고, 비정질 니오베이트의 사면체 Nb 분율은 **가정이 아니라 측정·계산 대상**이다 (§10-④).
- 🔴 **본문 vs 그림 ⑥**: `P1↔Li2 ≈ +4.55 eV` 라는 큰 값을 본문은 *"higher than 1 eV"* 로만 처리한다.

### 3e. 벌크 vs 계면 — **부호가 뒤집힌다** ★★★ (`Table S3`, **우리가 전부 재현했다**)

`Table S3` 이 **원시 총에너지(Ry)** 를 준다. 이것이 이 논문이 Ncube 와 갈리는 지점이다 — **독자가 직접 검산할 수 있다.**

| LCO 벌크 (`Li₃₆Co₃₆O₇₂` 기준) | 조성 | E (Ry) |
|---|---|---|
| None | Li₃₆Co₃₆O₇₂ | −5507.216 |
| **P_Co** | Li₃₆Co₃₅PO₇₂ | −5448.608 |
| P_Co + V_Li | Li₃₅Co₃₅PO₇₂ | −5433.616 |
| **P_Co + 2V_Li** | Li₃₄Co₃₅PO₇₂ | −5418.618 |
| **2V_Li** | Li₃₄Co₃₆O₇₂ | −5476.961 |

| LPS 벌크 (`Li₄₈P₁₆S₆₄` 기준) | 조성 | E (Ry) |
|---|---|---|
| None | Li₄₈P₁₆S₆₄ | −2430.364 |
| **Co_P** | Li₄₈P₁₅CoS₆₄ | −2488.826 |
| Co_P + Li_i | Li₄₉P₁₅CoS₆₄ | −2503.805 |
| **Co_P + 2Li_i** | Li₅₀P₁₅CoS₆₄ | −2518.753 |

> ✅ *우리 검산* (1 Ry = 13.605693 eV) — **논문의 세 값이 전부 재현된다**:
> - `[P_Co(LCO) + Co_P(LPS)] − [pristine + pristine]` = **+1.986 eV** (논문 **+1.98**) ✔
> - `[P_Co+2V_Li + Co_P+2Li_i] − [pristine + pristine]` = **+2.844 eV** (논문 **+2.84**) ✔
> - `[P_Co+2V_Li + Co_P] − [2V_Li + pristine]` = **−1.619 eV** (논문 **−1.62**) ✔
> **세 조합 모두 원소 개수가 정확히 보존된다**(Li/Co/P/O/S 전부). ⇒ **화학퍼텐셜 저수지가 필요 없는 완전 균형 반응**이다. 이것이 이 보고량이 *잘 정의된* 이유다.

**그 셋을 계면 값과 나란히 놓으면:**

| 비교 | 벌크(따로) | **계면(한 셀)** | 차이 (*우리 산수*) |
|---|---|---|---|
| `Co ↔ P` (전하보상 없음) | **+1.98 eV** | **−2.18 eV** (Co2↔P3) | **−4.16 eV** ← 이 논문의 핵심 수 |
| `Co ↔ P` + **Li 2개 이동** (P_Co+2V_Li \| Co_P+2Li_i) | **+2.84 eV** | **≈ −0.9 eV** | **−3.74 eV** |
| **Li 이동을 얹는 비용** (같은 계 안에서) | **+0.86 eV** | **+1.28 eV** | 둘 다 **양수 = 손해** |
| `Co ↔ P`, **부분 탈리튬 LCO 기준** (LCO+2V_Li 출발) | **−1.62 eV** | (미계산) | 벌크 기준에서 **−3.60 eV 스윙** |

> ⭐⭐ ***우리 산수* — 탈리튬 스윙의 크기가 밴드갭 2개다.**
> `2V_Li` 를 넣은 셀은 `Li₃₄Co₃₆O₇₂` = **Li₀.₉₄₄CoO₂** 다. 즉 **겨우 5.6 % 탈리튬**인데 벌크 교환에너지가 **+1.98 → −1.62 eV** 로 **3.60 eV** 뒤집힌다.
> 전자당 **1.80 eV** 이고, 이는 `Fig. S5c` 의 LCO 갭 `figure-read ≈` **2.05 eV** 와 같은 크기다 ⇒ **기전이 명확하다: V_Li 가 만든 정공 2개가 P_Co 의 전자 2개를 받아 주면, 그 전자가 전도대까지 올라갈 필요가 없어진다.**
> ⚠ **논문은 이 수치적 대응을 쓰지 않는다.** 그리고 여기서 **본문이 과외삽한다** — 계산한 것은 **x = 0.944 한 점**인데 결론은 *"Li_xCoO₂ (0.5 < x < 1) cathode can easily introduce the P_Co defects"* 다 (§10-⑥).

### 3f. 결합길이 — 교환 전/후 (`Fig. S4`, **PDF 텍스트 레이어에서 12개 값 전부 확보**)

| | pristine | Co2↔P3 이후 |
|---|---|---|
| **Co2–O ×6 (CoO₆)** | 1.93 · 1.90 · 1.87 · 1.90 · 1.96 · 1.97 Å (*우리 평균* **1.922**) | → **P3–O ×6 (PO₆)**: 1.67 · 1.63 · 1.74 · 1.74 · 1.84 · 1.84 Å (*우리 평균* **1.743**) |
| **P3–S ×4 (PS₄)** | 2.06 · 2.06 · 2.07 · 2.09 Å (*우리 평균* **2.070**) | → **Co2–S ×4 (CoS₄)**: 2.08 · 2.12 · 2.09 · 2.15 Å (*우리 평균* **2.110**) |

- 본문 요약값 *"Co−O 1.92 / P−S 2.06 Å"* 와 *우리 평균* 1.922 / 2.070 이 일치 ✅.
- 해석(본문): **PO₆ 는 −0.18 Å 수축**하고 P 가 팔면체 중심에서 **밀려나 CoO₂ 층 모서리 쪽으로 기운다**; **CoS₄ 는 +0.04 Å 팽창**하되 Co 는 **중심을 지킨다**.
- 본문 판정: *"These deformations do not seem to mainly contribute to the negative exchange energies."* ⚠ **정량 분해는 없다 — 눈으로 본 판정이다** (§10-③).

### 3g. Li 공공 형성에너지 — 혼합이 SCL 을 키운다 ★★ (`Fig. S7`, 전량 `figure-read` 라벨값)

> 정의(SI): `E_f(Li_i) = [E_tot(V_Li) + μ_Li] − E_tot`, **μ_Li = Li 금속**. ⇒ **값이 곧 추출전압(V vs Li/Li⁺)에 대응**한다.
> 계 = **LCO/LPS 계면에 Co↔P 를 6회** 넣은 것. 교환 횟수는 *"to reproduce the observed Co concentration"* (Sakuda ref 24) 로 정했다.

| 위치 | **6× Co↔P 이후** | (pristine) | 변화 |
|---|---|---|---|
| LCO 층간 Li — ① | 2.6 | (3.5) | **−0.9** |
| LCO 층간 Li — ② | 2.8 | (4.0) | **−1.2** |
| LCO 층간 Li — ③ | 2.2 | (3.2) | **−1.0** |
| **계면 Li (CoO₂ 모서리 흡착, 상)** | **1.6** | (3.3) | 🔴 **−1.7** ← 최대 강하 |
| 계면 Li (CoO₂ 모서리 흡착, 하) | 3.0 | (3.1) | −0.1 |
| **LPS 아표면 Li (최저)** | **0.9** | (1.4) | **−0.5** ← 절대 최저 |
| LPS 내부 Li — ⓐ | 2.7 | (3.0) | −0.3 |
| LPS 내부 Li — ⓑ | 2.6 | (2.7) | −0.1 |
| LPS 내부 Li — ⓒ | 2.6 | (2.6) | 0.0 |

> ✅ **외부 교차검증 2건 (우리 db 로)**:
> ① **pristine 1.4 = 2014 편의 "LP2 자리 E_v = 1.44 eV"** (`db/literature/refs.json` `haruyama2014.key_results`). **같은 자리다.** ⇒ 내 판독이 소수 첫째 자리에서 맞다.
> ② **pristine LCO 층간 3.2–4.0 eV ≈ LCO 방전 평탄부 3.9 V** ⇒ 이 값들이 **전압처럼 읽히는 것이 맞다**는 내부 sanity check.
> ⭐ **그러면 헤드라인은 이렇게 된다**: 2014 편이 *"LPS 아표면 Li 가 **1.44 V 저전압에서 이미 빠진다** → SCL"* 이라 했는데, **양이온 혼합이 그 문턱을 0.9 V 로 더 내린다.** 그리고 **LCO 쪽 Li 도 3.3 → 1.6 V 로 내려온다** — pristine 에서는 **LPS 쪽에서만** 일어나던 저전압 Li 이탈이 **혼합 뒤에는 양극 쪽에서도** 일어난다.
> ⚠ *우리 해석*이 한 발 더 나간 부분: 논문은 **"LCO 쪽이 더 크게 내려간다"** 를 쓰지 않는다. 논문 서술은 *"formation energies … are lower than those of pristine"* 까지다.

---

## 4. 계산 방법 — 전부 ★★

### 4.1 DFT 사양 (SI §S1, 본문 Methods)

| 항목 | 값 |
|---|---|
| **code** | **QUANTUM ESPRESSO** (ref 34 / S1) — ⭐ 우리와 같은 코드 |
| **범함수** | **PBE** (ref S3) |
| **스핀** | 🔴 **spin-unpolarized (비편극)** — 명시 + 근거 + 영향범위 자인 (아래 §4.2-⑤) |
| **DFT+U** | **U(Co 3d) = 5.9 eV**, Anisimov 계열 (ref S7). ⚠ **비편극 틀 안의 +U** (§10-①) |
| **pseudo** | **ultrasoft (Vanderbilt)** + Rappe 최적화 (ref S4·S5), PBE 로 생성 |
| **원자가 배치** | Li `1s²2s¹` · O `2s²2p⁴` · **P `3s²3p³` +NCC** · **S `3s²3p⁴` +NCC** · **Co `3d⁸4s¹` +NCC** · **Nb `4s²4p⁶4d⁴5s¹` +NCC** (NCC = nonlinear core correction, ref S6) |
| **cutoff** | **40 Ry (파동함수) / 320 Ry (augmented charge)** — USPP 라 비율 8:1. *우리 환산*: 40 Ry ≈ **544 eV** |
| **k-점** | **계면 = Γ 점 하나.** 벌크는 수렴시킴 (LCO 2×2×1 · LPS 2×2×2) |
| **PDOS 전용** | **nscf 2×1×1**, Γ 점 전자밀도를 써서 |
| **완화 기준** | 힘 **< 0.001 Ry/bohr** (= *우리 환산* **0.0257 eV/Å**) · 응력 **< 0.5 kbar** |
| **결함 계산의 셀** | ⭐ **pristine 완화값에 격자 고정, 이온만 완화** (명시) |
| **전하** | ⭐ **"We set the systems always neutral"** (SI 에 두 번) |
| **점유수** | **Gaussian smearing, σ = 0.01 Ry** (= 0.136 eV) |
| **정전 보정** | **ESM**(effective screening medium, ref 35·36)으로 계면 분극 점검 → *"differences … between conventional PBC and nonrepeated slab approach are negligible"* ⇒ **PBC 결과만 보고**. ✅ **보고는 안 하지만 대조는 했다** |
| **vdW** | **없음** (D2/D3 언급 0) — 2017 년 관례 |

### 4.2 ★★★ **보고량의 정의 — Ncube 가 안 적은 다섯을 하나씩 대조**

**Eq. (1)** (본문, 활자 그대로):

```
E_ex(A_i , B_j)  =  E_tot(A_i ↔ B_j)  −  E_tot^pristine
```

> *"E_tot^pristine is the total energy of the unmixed interface evaluated by the DFT+U calculation and E_tot(A_i ↔ B_j) represents the total energy of a **relaxed** interface in which the position of the **i-th A atom is replaced with the j-th B atom** from the pristine interface."*

**이것은 조성보존 in-place 스왑(swap)이다.** 두 원자의 자리만 맞바꾼다. ⇒ **화학퍼텐셜 저수지도, 참조 벌크도, 전하상태도 필요 없다.**

| 정의 요소 | **Ncube 2026** (ref 13 으로 이 논문을 인용) | **Haruyama 2017** |
|---|---|---|
| **① 참조상태** | ⛔ **미기재** | ✅ **Eq. (1) 이 명시** — 참조는 **같은 셀의 pristine 계면**. 스왑이라 조성이 정확히 보존되고 **μ 가 식에 안 들어간다**. 벌크 대조(§3e)도 `Table S3` 의 조성을 확인하면 **원소 개수가 전부 보존**된다 |
| **② 전하규약** | ⛔ **미기재** | ✅ **"We set the systems always neutral"** (SI, 2회). 하전결함 없음 ⇒ **Makov–Payne/Freysoldt 유한크기 전하보정이 원리적으로 불필요**. 점유수는 Gaussian σ = 0.01 Ry |
| **③ 셀 크기** | ⛔ **미기재** | ✅ **`Table S1`** 이 계면 3종 격자상수 전부 · 벌크는 **LCO 144 원자(k 2×2×1) · LPS 128 원자(k 2×2×2)** · **결함 계산은 격자 고정·이온만 완화** · 힘 0.001 Ry/bohr · ⚠ **계면 원자수는 이 논문에 없다**(2014 편에 있다) |
| **④ 자리 샘플링** | ⛔ **미기재** | ✅ **자리마다 이름을 붙여 전부 그림에 표시**(Li1–6 · Co1–4 · P1–4 · Nb1–3) + **배위환경 명시**(LiS₆/LiS₄ · CoO₄/CoO₆ · NbO₄/NbO₆ · PS₄). **LCO/LPS 만 28 조합 보고.** SI: *"The formation energies of almost all possible choices were calculated"* + ⚠ **"we tried to calculate many other exchange defects, and the exchange energies indicate almost the same values (within the 0.5 eV deviation)"** ← **표본 산포를 숫자로 자인했다** |
| **⑤ 스핀** | ⛔ **미기재** | ✅ **명시적으로 비편극** + 근거(ref S2 = Qian 2012) + **영향범위 자인**: *"which become important only in the presence of the **CoO₄ structure**. Namely, the exchange energies related to only the **Co1** atom … are expected to be slightly changed"* 🔴 **그런데 그 CoO₄ 가 §5.4 기전의 주인공이다** (§10-①) |

> **⇒ 5/5. Ncube 는 0/5.** 그 위에 이 논문은 **원시 총에너지를 공개**(`Table S3`)해서 **우리가 세 값을 전부 재현했다**(§3e). **재현 가능성 축에서 두 논문은 같은 등급이 아니다.**

> ⚠ **그래도 이 보고량이 완전무결한 것은 아니다.** 스왑이라 μ 는 필요 없지만, 남는 자유도가 셋 있고 **논문은 그중 둘만 다룬다**:
> - **(a) 자리 쌍의 거리** — 스왑은 **두 결함을 특정 거리에 놓는다**. 그 거리의 정전상호작용이 값에 들어간다. 논문은 P1–P4·Co1–Co4 로 **거리 의존성을 실제로 보여준다**(경향 ①②) ✅ — 다만 **그 성분을 분리하지는 않는다**.
> - **(b) 주기 이미지** — 중성 스왑이라 monopole 은 없고 쌍극자/사중극자만 남는다. **셀 크기 수렴검사는 없다** ⛔.
> - **(c) 배열 산포** — SI 의 *"within the 0.5 eV deviation"* 이 그것이다. ⇒ **±0.5 eV 는 이 논문의 모든 값에 붙는 오차막대로 읽어야 한다** (§10-⑤).

### 4.3 안 한 것 (우리 축 기준 전수 확인)

⛔ **AIMD 0 · 고전 MD 0 · MLIP 0 · NEB 0 · 확산장벽 0 · 포논 0 · 탄성상수 0 · Bader 0 · COHP/LOBSTER 0 · ELF 0 · BVSE 0 · hull/pseudo-binary 0 · ESW/grand-potential 0 · 전하밀도차(CDD) 0 · Löwdin/Mulliken 전하 0 · 부착일 W_ad 0**(← 이건 2014 편에 있다).
**후처리는 PDOS 하나뿐이고, 그것도 정성 서술용이다.** 산화수 논의(*"P 는 +5, Co 2개가 +2 로 환원"*, *"Co 를 +5 로 볼 수 있다"*)는 **전하 분석이 아니라 조성에서 센 형식전하**다.

---

## 5. 결과 — 절별 상세

### 5.1 Co 는 Li 격자로 안 간다 (`Fig. 1`)

`Fig. 1a` 는 LCO(110) 을 왼쪽, LPS(010) 을 오른쪽에 두고 `a–c` 면에서 본 그림이다. LCO 는 **파란 CoO₆ 팔면체가 c 방향으로 층을 이루고 그 사이에 연두색 Li**, LPS 는 **보라 PS₄ 사면체 + 연두 LiS₄ 다면체 + 노란 S**. Li1–3 이 윗줄(LiS₆·4b), Li4–6 이 아랫줄(LiS₄·8d)이고, **Li1 과 Li4 는 CoO₂ 층의 끊긴 모서리에 붙어 있다**(= 2014 편이 말한 SCL 흡착 자리).

결과(§3b)는 단순하다 — **전부 흡열.** 유일하게 싼 것은 **Co 가 바로 옆 흡착 Li 자리로 한 칸 나가는 것**(≈0.2–0.25 eV)이고, 거기서 **더 들어가려면 0.7–3.4 eV 를 내야 한다.** ⇒ **Co 가 LPS 의 Li 서브격자를 타고 50 nm 를 가는 그림은 성립하지 않는다.**

> 🔑 **이 음성 결과가 이 논문의 논증 구조를 만든다.** Co↔Li 를 배제했기 때문에 Co↔P 가 유일한 후보로 남고, 그래서 다음 절이 필요해진다. **Ncube 가 Li↔Co 를 (그것도 음수로) 보고한 것과 정면으로 어긋나는 지점이 바로 여기다**(§7a).

### 5.2 Co 는 P 자리로 간다 (`Fig. 2`)

`Fig. 2a` 는 **다른 시야각**(`b–c` 면)이다 — 본문이 *"the atomic structures of Figures 1 and 2 correspond to different view angles"* 라고 경고한다. 왼쪽 LCO 는 이제 CoO₆ 팔면체를 **위에서 본 삼각 타일링**으로 보이고, Co1 이 경계 바로 옆(CoO₄), Co2 가 그 아래 CoO₆, Co3·Co4 가 한 층 안쪽이다.

결과(§3c): **16개 전부 음수, 범위 ≈ −0.95 ~ −3.78 eV.** 본문 결론:

> *"These exchange energies indicate strong mixing of the Co and P atoms **not only near but also far from the boundary**. The preference of cobalt (relative to phosphorus) **for sulfur** could be driving the defect formation."*

그리고 저자가 스스로 다는 단서 — **이 문단이 §10-② 의 근거다**:

> *"the defected interface structures considered here are **not necessarily the final configurations**. … more defects are likely to occur because of the large driving force … This tendency of mixing **might lead to amorphization** of a layer at the interface or **nucleation of an interfacial phase** in extreme cases (and with sufficiently high temperature). The calculated defected states here can be regarded as the **intermediates** between the pristine structure and the final state; the negative calculated energy shows that there is a **minimal energetic barrier in the beginning** of this process."*

⚠ **"minimal energetic barrier" 는 계산된 것이 아니다** — 반응에너지가 음수라는 데서 유추한 것이다(Bell–Evans–Polanyi 식 손짓). **장벽은 이 논문에 단 하나도 없다.**

### 5.3 버퍼층 (`Fig. 3`)

`Fig. 3a` (LCO\|LNO): 파란 CoO₆ 와 **초록 NbO₆ 가 매끄럽게 맞물려** 있다 — 2014 편의 *"smoothly matched, crystalline order preserved"* 와 같은 그림. `Fig. 3b` (LNO\|LPS): 왼쪽 초록 NbO₆ 망, 오른쪽 PS₄/LiS₄, **경계에 Nb–S 결합이 없다**(2014 편 판정과 일치).

결과(§3d): **Co↔Nb 전부 +0.93~1.27 eV**, **P↔Nb 는 팔면체에서 +1.22~1.60 eV 인데 사면체 Nb1 에서만 −1.05 eV.**

**저자의 기전 설명(중요 — Ncube 와 다르다)**:

> *"Note that the Co ↔ Nb exchanges **do not have this effect** significantly, because the Co and Nb at the LCO/LNO interface **mostly form the octahedrons**, in contrast to the **Co insertion into the tetrahedron** in the LCO/LPS case."*

⇒ **버퍼가 막는 이유 = "Nb 가 산화환원에 뻣뻣해서" 가 아니라 "그 계면에는 사면체 배위가 안 생겨서 낮은 받개 준위가 안 만들어져서"** 다. **기하가 먼저고 전자구조가 그 결과다.**

### 5.4 왜 계면에서만 유리한가 — 이 논문의 중심 논증 (`Fig. 4` · `Fig. S5` · `Table S3`)

논문은 **가능한 설명 네 개를 차례로 세우고 셋을 깎는다.**

**(a) 구조 변형인가 → 아니다.** `Fig. S4` 의 결합길이 변화(§3f)는 PO₆ 수축·CoS₄ 팽창인데, *"These deformations do not seem to mainly contribute."* ⚠ 정량 분해 없음.

**(b) 벌크 결함준위만으로 설명되나 → 아니다 (`Fig. S5` 실독).**
- `Fig. S5c` (**LCO + P_Co**): 가전자대는 −3~0 eV(Co 3d 파랑 + O 2p 빨강, 피크 `figure-read ≈` −1.45·−0.5), **갭 안에 결함준위가 없고**, 전도대는 `figure-read ≈` **+2.05 eV** 에서 시작해 2.55·2.95 에 쌍봉. **E_F 가 딱 전도대 바닥(`figure-read ≈` +2.1 eV)에 있다** ⇒ **P_Co 가 내놓은 전자 2개가 전도대에 올라앉아 있다.** 형식전하: P⁵⁺ 유지, **Co 2개가 +2 로 환원**.
- `Fig. S5d` (**LPS + Co_P**): 가전자대는 S 3p(노랑 ≈ 검정) −2.9~0, **갭 안에 고립된 Co 3d 피크가 `figure-read ≈` +1.35 eV 에 있고 그것이 비어 있다**(E_F `figure-read ≈` +0.7 eV), 전도대 onset `figure-read ≈` +2.85 eV(본문 *"around 3 eV"* ✅). 형식전하: **Co 를 +5 로 봐야 한다** (사면체 CoS₄, S 는 산화 안 됨).
- ⇒ **벌크에서는 전자가 갈 곳이 비싸다. 그래서 +1.98 eV.**

**(c) 계면 준위인가 → 그렇다 (`Fig. 4` 실독).**
- `Fig. 4a` (pristine 계면): 에너지 원점이 **pristine 점유대 최상단 = 0**. 주 가전자대는 −4~−0.7 이고, **−0.5~0 에 작은 어깨**(총 DOS `figure-read ≈` 100–200)가 따로 있다 — 본문이 *"states near the Fermi levels are attributed to **pseudotetrahedral CoO₄ placed at the edge of the CoO₂ layer**"* (ref 46 = Qian 2012)라고 한 그것. **E_F 는 `figure-read ≈` +0.1 eV**, 빈 상태는 `figure-read ≈` **+0.4 eV** 부터. ⇒ **계면 유효 갭 `figure-read ≈` 0.4 eV** — 벌크 LCO 2.05 / LPS ~2.6 보다 훨씬 좁다.
- `Fig. 4b` (Co2↔P3): **E_F 가 `figure-read ≈` +0.35–0.4 eV 로 오른쪽으로 옮겨 갔고**, 0~0.35 구간이 채워졌다. ⇒ **P_Co 의 전자 2개가 그 낮은 CoO₄ 준위에 들어앉았다. 전도대까지 안 올라간다.**
- 본문 결론: *"we attribute the lower exchange energy to the **electronic occupations of the lower interfacial states**."*

**(d) Li 이동에 의한 전하보상인가 → 아니다 (정량으로 깎는다).** §3e 표의 셋째 행 — 계면에서 Li 2개를 LCO→LPS 로 보내면 −2.18 → −0.9 eV 로 **1.28 eV 손해**다. 벌크에서도 +1.98 → +2.84 로 **0.86 eV 손해**. ⇒ *"charge compensation by the Li transfer together with the cation exchange is **not the main cause**."* 정전 인력(하전 결함쌍 간)도 후보로 언급하지만 **Co↔Nb 가 같은 이득을 못 보는 것**을 근거로 깎는다.

> ⚠ ***우리 산수* — 저자의 귀속이 수치적으로 절반만 맞는다.**
> 계면 −2.18 vs 벌크 +1.98 = **4.16 eV**. 전자 2개니까 **전자당 2.08 eV** 가 필요하다.
> 그런데 `Fig. S5c` 와 `Fig. 4` 로 밴드정렬을 대면: 벌크 LCO 에서 전자는 **VBM+2.05 eV**(전도대 바닥)로 가고, 계면에서는 **계면 VBM+0.4~0.8 eV** 의 CoO₄ 준위로 간다 ⇒ **전자당 낙차 ≈ 1.25–1.65 eV, 2개면 ≈ 2.5–3.3 eV.**
> **남는 ≈ 0.9–1.7 eV 는 전자 준위로 설명되지 않는다** — 구조 완화 + 정전 + 계면 자체의 안정화로 가야 하는데, **논문은 그 셋을 이미 "주된 원인이 아니다" 로 깎아 놓았다.** ⇒ 전자항이 **지배적**이라는 말은 지지되지만, **"거의 전부" 라는 읽기는 이 논문 자체의 그림으로 반박된다** (§10-③).

### 5.5 그래서 Li 가 더 잘 빠진다 (`Fig. S6` · `Fig. S7`)

`Fig. S6` 실독: 6회 교환 후 구조는 **여전히 결정질이다** — LCO 층도 LPS 골격도 유지되고, 윗면도(top view) 에서 **LPS 영역에 짙은 파란 CoS₄ 사면체가 6개** 흩어져 있고 LCO 층 안에 창백한 PO₆ 가 보인다. **Co 는 계면에서 PS₄ 한두 층 안쪽까지만 들어가 있다.** ⇒ **이 정적 계산은 "비정질화" 를 보여주지 않는다 — 본문이 그것을 추론이라고 스스로 적은 이유다.**

`Fig. S7` (§3g): 모든 Li 자리의 공공 형성에너지가 **낮아지거나 같다.** 저자 설명 — *"additional electrons from P_Co defects in the interface are **easily extracted**. Consequently, **one P_Co defect can produce two additional Li vacancies**."* 그리고 열역학적 재해석을 하나 더 얹는다:

> *"LiCoS₂ has a **lower voltage** than LiCoO₂ (ref 47 = Aydinol 1997), and so as **Co is increasingly surrounded by sulfur the interface takes on more of the character of LiCoS₂.**"*

⇒ **Co↔P 혼합은 계면을 국소적으로 "LiCoS₂ 같은 저전압 상" 으로 만든다.** 그래서 그 자리의 Li 가 싸게 빠지고, **Li 고갈층이 더 자란다.**

---

## 6. 메커니즘 종합 — 이 논문이 세운 인과 그래프

```
 LCO(110) | β-Li3PS4(010) 접촉
        │
        ├─(A) 계면에 **CoO4 유사사면체**가 생긴다 (CoO2 층의 끊긴 모서리)
        │        └→ 갭 안에 **낮은 빈 준위** (figure-read ≈ VBM+0.4~0.8 eV)  … Fig. 4a
        │
        ├─(B) Co ↔ Li 는 전부 흡열 (+0.2 ~ +3.4 eV)  … Fig. 1b
        │        └→ ⛔ Li 격자를 타는 Co 확산 경로 **차단**
        │
        └─(C) Co ↔ P 는 전부 발열 (−0.95 ~ −3.78 eV)  … Fig. 2b
                 │   ├ 벌크끼리면 **+1.98 eV (흡열!)**          … Table S3 (우리 재현)
                 │   └ 계면이면   **−2.18 eV**                  ⇒ Δ = −4.16 eV
                 │
                 ├─ 왜? P_Co 가 내놓는 **전자 2개**가 (A) 의 낮은 준위로 들어간다  … Fig. 4b
                 │     (벌크였다면 LCO 전도대 +2.05 eV 까지 올라가야 한다  … Fig. S5c)
                 │     ⚠ 밴드정렬로 설명되는 것은 4.16 중 ≈2.5–3.3 eV (우리 산수)
                 │
                 ├─ Li 이동 전하보상은 **오히려 +1.28 eV 손해** ⇒ 주원인 아님
                 ├─ 구조 변형(PO6 수축·CoS4 팽창)도 주원인 아님 (정성 판정)
                 │
                 └─(D) 결과: 계면이 국소적으로 **LiCoS2 성격**을 띤다
                          └→ Li 공공 형성에너지 전면 하락 (LCO쪽 −0.9~−1.7 / LPS쪽 −0.1~−0.5 eV)
                          └→ **Li 고갈층(SCL) 성장 가속** — 2014 편 SCL 기전과 접속
                          └→ 계면저항 ↑

 [완화] LiNbO3 버퍼
        └─ Co↔Nb 는 **둘 다 팔면체** ⇒ (A) 의 사면체 준위가 안 생긴다 ⇒ +0.93~1.27 eV  … Fig. 3c
        └─ ⚠ 예외: **사면체 NbO4** 자리에서는 P1↔Nb1 = −1.1 eV (발열)               … Fig. 3d
             └→ 비정질 코팅의 사면체 분율이 문제가 된다 (저자는 "많지 않을 것" 으로 가정)

 [탈리튬] LCO + 2V_Li (= Li0.944CoO2) 에서 출발하면
        └─ 벌크 Co↔P 조차 **−1.62 eV** ⇒ 부호 반전, 스윙 3.60 eV ≈ 2 × 밴드갭 (우리 산수)
             └→ **충전(탈리튬)이 혼합을 열어 준다** — 계면 준위 없이도
```

> 🔑 **이 그래프의 미학은 "(A) 기하 → 전자 → 열역학" 이라는 방향성이다.** 그리고 그것이 **완화 전략을 예측 가능하게** 만든다 — *"계면에 사면체 배위가 생기지 않게 하라."* Ncube 의 *"redox-flexible 하지 않은 양이온을 써라"* 와 **결론은 같지만 설계 규칙이 다르다.**

---

## 7. 우리 DFT / 우리 원고 축과의 대조 ★★★

> 기준: `our_dft_baseline.md` · `comparison_vs_ours.md` §B③·§H · `db/literature/refs.json[37]`
> ⚠ 물질계가 다르다(β-Li₃PS₄ vs Li₆PS₅Cl). 아래 어느 행도 **값 대 값 비교가 아니다**.

### 7a. 🔴🔴 **1번 임무 — Ncube 의 미정의 치환에너지를 이 논문으로 고칠 수 있나**

**답: 고칠 수는 없다. 대신 *대체* 할 수 있고, 그 과정에서 Ncube 의 값이 이 논문과 어긋난다는 것이 드러난다.**

| | **Ncube 2026** (`Table` 없음, 본문 §3.2) | **Haruyama 2017** (본 논문) |
|---|---|---|
| 보고한 양 | *"Li↔Co substitution energy"* | `E_ex = E_tot(스왑) − E_tot(pristine)`, **Eq. (1)** |
| 개수 | **2개** | **~40개** (LCO/LPS 28 + LNO 12) |
| 정의 5요소 | **0/5** | **5/5** |
| 원시 데이터 | 없음 | ✅ `Table S3` 총에너지 — **우리가 3개 값 재현 완료** |
| LCO\|황화물 값 | **−1.109 eV** (LGPS) | **Co↔Li: +0.20 ~ +3.38 eV (전부 양수)** / **Co↔P: −0.95 ~ −3.78 eV (전부 음수)** |
| LCO\|산화물 버퍼 값 | **+0.144 eV** (LNTO) | **Co↔Nb: +0.93 ~ +1.27 eV** (LCO\|LNO) |

**세 가지가 나온다:**

1. 🔴 **부호가 안 맞는다.** Ncube 가 *"Li↔Co"* 라고 부른 양이 음수(−1.109)인데, **정의가 적힌 유일한 선행 계산에서 Co↔Li 는 조사한 12개 전부 양수**다. 두 계가 다르다는 것(LGPS vs β-LPS)으로 **부호 반전까지** 설명하기는 어렵다 — Li 자리에 들어간 Co 는 두 계 모두 **S 배위**이고, 부호를 정하는 것은 Co 를 Li 자리에 넣는 비용이다.
2. ⭐ **더 그럴듯한 읽기: Ncube 의 −1.109 는 Haruyama 의 `Co↔P` 계열과 크기가 겹친다** (−0.95 ~ −3.78, 본문 인용값 −2.18). 즉 **Ncube 가 실제로 계산한 것은 "Li 자리로의 Co 치환" 이 아니라 "양이온 골격 자리로의 Co 치환" 일 가능성이 높다.** ⛔ **확인 불가** — Ncube 에 정의가 없다.
3. 🔴 **버퍼 값은 부호는 맞고 크기가 7~9배 작다.** Ncube +0.144 vs Haruyama +0.93~1.27. Haruyama 의 SI 가 자인한 **배열 산포 ±0.5 eV** 를 감안해도 **+0.144 는 그 밴드 밖**이다. ⇒ **Ncube 의 "LNTO 가 막는다" 는 결론은 옳지만, 그 결론을 떠받치는 수치 여유는 선행편의 1/7 이다.**

> ⇒ **우리 처리 방침 (이 digest 로 확정)**:
> - `comparison_vs_ours.md` 에서 **Ncube 의 두 치환에너지는 "정의 없는 값" 으로 격하**하고, **양이온 혼합 열역학의 소환값은 Haruyama 2017 로 바꾼다.**
> - Ncube 의 **나머지 층(MLMD·연속체)** 판정은 그대로 둔다 — 이 대조는 **DFT 층에만** 적용된다.
> - ⛔ **"Ncube 가 틀렸다" 로 쓰지 않는다.** 쓸 수 있는 것은 *"정의가 없어 검증 불가이고, 정의가 있는 선행편과 부호가 다르다"* 까지다.

### 7b. ⭐⭐⭐ **2번 수확 — 우리 §B 의 원자단위 짝**

우리 `comp1|LiCoO₂ = −0.3227 eV/atom` 의 산물이 **`Co₉S₈ + Li₂SO₄ + Li₃PO₄ + Li₂S + LiCl`** 이다. 풀어 쓰면 **"Co 는 S 와, P 는 O 와 짝을 이룬다"** — [Xiao20Rev] 가 이 계열의 기전을 *"S↔O 교환 + Li₃PO₄ 싱크"* 라고 한 바로 그것이다.

**Haruyama 2017 의 `Co ↔ P` 스왑은 정확히 그 교환의 첫 한 걸음이다** (Co → CoS₄, P → PO₆/PO₄).

| | **우리 (§B)** | **Haruyama 2017** | 관계 |
|---|---|---|---|
| 방법 | MP hull **pseudo-binary grand-potential** (Richards 2016 = 이 논문의 ref 29) | **정적 DFT+U 계면 슬랩, 점결함 스왑** | 같은 화학, 다른 층위 |
| 양 | **반응 에너지 / 원자** (조성 공간) | **교환 에너지 / 사건** (실공간) | ⛔ 단위가 다르다 — **같은 표 금지** |
| 값 | **−0.3227 eV/atom** (min @ x=0.5302) | **−2.18 eV/교환** (계면) / **+1.98 eV** (벌크끼리) | — |
| 무엇을 말하나 | **종점**: 완전 상분리했을 때의 최대 이득 | **첫 걸음**: 원자 하나 바꾼 순간의 이득 | ⭐ **상보** |
| 기하 | **없다** (조성만) | **면(110)/(010) 지정 + 배위환경 지정** | 그들이 위 |
| 동역학 | 없다 | **없다** (§10-②) | 둘 다 없다 |

> ⭐⭐ **여기가 이 digest 의 최대 수확이다 — 그리고 예상 밖의 형태로 왔다.**
> **벌크에서는 두 방법의 부호가 반대다.** 우리 hull 은 −0.32 eV/atom(발열), Haruyama 의 벌크 스왑은 **+1.98 eV(흡열)**.
> **모순이 아니다.** hull 은 **완전 상분리한 종점**을 재고, 스왑은 **상분리하기 전의 점결함 한 쌍**을 잰다. 점결함 상태는 종점에서 멀리 떨어진 고에너지 중간체다 ⇒ **+1.98 eV 는 사실상 "핵생성 비용" 의 열역학 대역이다.**
> **그리고 계면이 그 비용을 없앤다** (−2.18 eV). 저자가 결론에서 정확히 그 말을 한다:
> > *"These results imply that the **Co-interdiffusion is likely to occur without requiring the nucleation and growth of an interfacial layer**, and can be therefore expected to proceed rapidly."*
> ⇒ **우리 §B 의 큰 음의 hull 값이 "열역학은 원하지만 핵생성이 막는 것 아니냐" 는 반론을 받을 때, 이 논문이 그 반론을 원자 단위로 닫아 준다.** [Wu26MLIF] §2.5 의 *"convex-hull 단독 의존은 현실성이 제한된다"* 에 대한 **문헌 기반 부분 답변**이다.
> ⚠ **부분** 인 이유: 이 논문도 **장벽(saddle)을 계산하지 않았다.** "핵생성 비용이 없다" 와 "빠르다" 사이에는 여전히 **확산 장벽**이 있고, 그 칸은 아직 [Ncube26] 밖에 없다 (§10-②).

### 7c. 🔴 **우리 §B·§D 주장의 선행연구 점검 (1저자 지시 — 이것부터)**

| 우리가 "신규" 로 쓰려는 것 | 이 논문에 있나 | 판정 |
|---|---|---|
| **§B** grand-potential 계면 반응성 6 조성 × 4 양극 × 6 전압 · 전 kink 보존 | **없다** — hull·pseudo-binary·grand-potential **0회**. 열역학 이웃(Zhu·Richards·Yokokawa)을 **인용만** 한다 | ✅ **선점 없음** |
| **§C** Nd 효과와 O 효과의 **가법성** | **없다** | ✅ **선점 없음** |
| **§D** Nd 가 **Li 를 안 쓰는 인산염 경로**를 연다 (NdPO₄ Li/P=0 vs Li₃PO₄ Li/P=3) | **없다** — Li **인벤토리** 개념이 없다. ⚠ **다만 인접한 어휘가 있다**: *"charge compensation by the **Li transfer across the interface**"* 를 정량으로 다루고 **기각**한다(§5.4-d) | ⚠ **선점 아님 — 그러나 어휘 충돌 위험.** 그들의 "Li transfer" 는 **전하보상**이고 우리 §D 는 **Li 재고(capacity inventory)** 다. **원고에서 두 개념을 구분해 쓰지 않으면 심사자가 "이미 2017 에 있다" 고 읽는다.** ⇒ *"Li budget / inventory"* 로 못박고 charge compensation 과 명시적으로 구분할 것 |
| **§2b** 보호율 = min(1, k·x/(1−x)), 맞춘 매개변수 0 | **없다** | ✅ **선점 없음** |
| **§E** dual compatibility (CEI 산물이 전해질 쪽과도 지내야 한다) | **없다** — 버퍼층을 **두 계면으로 쪼개서 각각 계산한다**(LCO\|LNO 와 LNO\|LPS). ⚠ **그것이 구조적으로 "양쪽 다 봐야 한다" 의 실행이다** | ⚠ **부분 선점 — 논지의 *형태*.** 값·축·양 전부 다르지만 **"중간상은 양쪽 계면에서 동시에 평가돼야 한다" 는 실천이 2017 년에 활자화돼 있다.** ⇒ **인용하면 해소**되고, 오히려 *"우리 §E 는 그 실천을 조성 열역학으로 일반화한 것"* 으로 쓰는 편이 방어적으로 강하다 |
| **기전 어휘**: "도펀트/버퍼가 전하를 못 갚아서 막는다" | ⚠ **여기는 다르다.** 이 논문의 차단 기전은 **"사면체 배위가 안 생겨 낮은 받개 준위가 없다"**(기하 우선)이고, **redox-flexibility 라는 말을 쓰지 않는다** (그 어휘는 [Ncube26]) | ✅ **이 논문에는 선점 없음.** 단 `ncube2026…` §7b 에 이미 기록한 **redox-inflexibility 어휘 선점은 그대로 유효** |

> **결론: 우리 핵심 주장 5개 중 선점 0건.** 겹치는 것은 **① 논지 형태 1건(§E 의 "양쪽 계면 동시 평가")** 과 **② 어휘 충돌 위험 1건(Li transfer ↔ Li budget)**. 둘 다 **인용 + 용어 구분으로 해소**된다.

### 7d. 🔴 **이 논문 때문에 약해지는 / 강해지는 우리 주장**

| 우리 주장 | 이 논문의 효과 | 판정 |
|---|---|---|
| **§B 의 큰 음의 hull 값이 실제 열화를 뜻한다** | 🟢 **강해진다.** 계면에서 첫 걸음이 −2.18 eV 로 내리막이고 *"핵생성 없이 진행"* 이라는 활자가 생겼다 (§7b) | ✅ **[Wu26MLIF] 비판에 대한 부분 답변으로 인용 가능** |
| **고전압(탈리튬) 축이 옳은 방향이다** | 🟢 **강해진다.** `Li₀.₉₄₄CoO₂` 만으로 **벌크 교환이 +1.98 → −1.62 eV** 로 뒤집힌다. **겨우 5.6 % 탈리튬**이다. [Jiang22Se] 의 hull 결과(Li₀.₅CoO₂ −434.98 vs LiCoO₂ −302.12 meV/atom)와 **방법이 전혀 다른데 같은 방향** | ✅✅ **독립 교차검증 1건 추가** |
| **0 K hull 열역학으로 계면을 말할 수 있다** (암묵 전제) | 🔴🔴 **약해진다 — 그리고 [Ncube26] 과 다른 방향에서 약해진다.** Ncube 는 *"면에 따라 반응이 있고 없다"*(기하)로 쳤다. **이 논문은 "같은 조성인데 벌크냐 계면이냐로 부호가 뒤집힌다"(전자구조)로 친다.** 벌크 +1.98 vs 계면 −2.18. **조성 공간에서 정의된 우리 지표는 원리적으로 이 4.16 eV 를 볼 수 없다** | 🔴 **우리 §B 의 가장 날카로운 한계 지적.** ⇒ 원고에 **"본 지표는 조성 수준 구동력이며 계면 전자구조에 의한 국소 안정화는 포함하지 않는다"** 는 범위 선언 필요 |
| **§2b 보호율(화학 소모)이 계면 건강의 지표다** | 🔴 **약해진다 (새 경로).** 이 논문이 보여주는 **혼합 → Li 공공 형성에너지 하락 → SCL 성장** 은 **소모(consumption)가 아니라 수송(transport) 손상**이다. 우리 보호율은 그걸 못 센다 | 🟠 **중간.** [Ncube26] 이 연 "기계 경로" 에 이어 **"SCL/수송 경로" 가 하나 더 열렸다.** 범위 선언을 그만큼 넓혀야 한다 |
| **Nd 인산염이 계면에 생기면 좋다** | ⚠ **새 질문이 생긴다.** 이 논문의 규칙은 *"사면체 배위가 생기면 받개 준위가 생기고 혼합이 열린다"* 다. **NdPO₄(모나자이트)의 Nd 는 9배위, P 는 사면체 PO₄** 다 ⇒ **그 PO₄ 가 황화물과 만나는 계면에서 `P ↔ (SE 양이온)` 스왑이 열리는가?** 이 논문의 `P1↔Nb1 = −1.1 eV` 는 **"사면체 자리는 P 에게 먹힌다"** 를 보여준다 | 🟠 **미해결 — 계산 가능한 질문으로 승격**(§11-③) |
| **MLIP-MD 상대차 인용정책** | 무관 (이 논문에 MD 없음) | — |

### 7e. ✅ 우리가 더 나은 곳 / 그들이 더 나은 곳 (정직하게)

| 축 | **우리** | **Haruyama 2017** |
|---|---|---|
| **열역학 폭** | hull · 전 kink · 전압 분해 · 산물 동정 · 산물 밴드갭 · 6 조성 × 4 양극 | **교환에너지 ~40개** — 폭은 없고 **깊이가 있다** |
| **보고량 정의** | 보고량 카드 규율 보유 | ✅ **5/5 + 원시 총에너지 공개.** ⭐ **우리 카드 §1–3 의 외부 모범 사례로 쓸 수 있다** |
| **스핀 처리** | ⚠ 우리 계는 비자성이라 쟁점이 적다 | 🔴 **비편극 + Co²⁺/Co⁵⁺ 를 다룬다** — 여기는 우리가 더 안전하다 |
| **계면 기하** | v5 single-interface + vacuum 30 Å + **FixAtoms 하단 1/3** (UMA OOD 대응) | ✅ **FixAtoms 없이 전 원자 + 측방 격자 완화** + **슬라이드 4~16 표본 탐색** — **그들이 더 엄밀하다** |
| **동역학** | ⛔ 0 | ⛔ **0** — 비긴다. 이 칸은 아직 [Ncube26] 뿐 |
| **전자구조 후처리** | LOBSTER ICOHP · fixed-occ nscf gap · CDD | **PDOS 하나** (정성) — 우리가 위 |
| **셀/수렴 검사** | 우리도 부족 | ⛔ **계면 셀 크기 수렴 0 · k 수렴 0(Γ만) · 산포는 "±0.5 eV" 한 줄** |
| **재현성** | db 원장 + 해시 | ✅ **`Table S3` 로 독자가 검산 가능** — 2017 년 논문치고 이례적이다 |

### 7f. `our_dft_baseline.md` 접점 (값 비교가 **아님**)

| baseline 항목 | 이 논문의 대응물 | 왜 비교 못 하나 |
|---|---|---|
| band gap comp1 **2.066** / modelc **2.099** eV | LCO 벌크 갭 `figure-read ≈` **2.05 eV** · LPS 벌크 갭 `figure-read ≈` **2.6 eV** · **계면 유효 갭 `figure-read ≈` 0.4 eV** | ⛔ **물질이 다르다.** ⭐ 다만 **개념 하나는 가져온다**: *"계면 갭 ≪ 두 벌크 갭"* — 우리는 **계면 갭을 계산한 적이 없다**(§11-②) |
| 산화 onset **2.256 V** (S²⁻-limited) | ⛔ ESW 없음 | 대응물 부재 |
| E_VRH 22.06 / 27.66 GPa | ⛔ 탄성 없음 | 대응물 부재 |
| Ea 0.253 / 0.224 eV · D(600 K) | ⛔ **MD·NEB 없음** | 대응물 부재 |
| ICOHP(Li–Cl) −1.86 / −2.10 | ⛔ COHP 없음 | 대응물 부재 |
| `adhesion.json` γ_SE comp1 **1.211 J/m²** · v2 W_ad **1.107 J/m²** | ⛔ **이 편엔 없다.** 2014 편에 **LCO/LPS = 4.3 eV/nm² = 0.69 J/m²** | ⚠ **2014 편 값이지 이 논문 값이 아니다.** 인용할 때 **연도를 틀리지 말 것** |
| `comp1\|LiCoO₂` **−0.3227 eV/atom** | **−2.18 eV/교환** (계면) · **+1.98 eV** (벌크) | ⛔ **단위·층위가 다르다** — §7b 의 서술 관계로만 |

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | LCO(110)\|LPS(010) 계면의 `a–c` 측면도. Li1–3 = LiS₆(4b) 윗줄 · Li4–6 = LiS₄(8d) 아랫줄 · Li1·Li4 는 **CoO₂ 층 모서리 흡착**(= 2014 편 SCL 자리) · Co1 = CoO₄(계면) · Co2 = CoO₆ | **우리 LPSCl\|NCM 슬랩에서 "모서리 흡착 Li" 를 같은 방식으로 명명할 근거.** 우리 v10/v10b 에서 관측한 Li_mig 와 같은 자리다 |
| 1b | `Co↔Li` 교환에너지 막대 (2 계열 × 6 자리). **전부 양수**, `figure-read ≈` +0.20(Co2↔Li1) ~ +3.38(Co2↔Li5) | ⭐ **[Ncube26] 의 Li↔Co = −1.109 eV 와 부호가 반대**라는 증거의 1차 출처. §7a |
| 2a | 같은 계면의 **`b–c` 시야각** (Fig 1 과 각도가 다름 — 본문 경고). Co1 CoO₄ · Co2 CoO₆(경계 근접) · Co3·Co4 안쪽 · P1(경계 최근접)–P4 | 계면 배위환경 명명법 — 우리 digest/원고 그림 캡션에 그대로 차용 가능 |
| 2b | `Co↔P` 교환에너지 막대 (4 × 4 = **16개 전부 음수**). `figure-read ≈` −0.95 ~ **−3.78**(Co2↔P1, **본문에 없는 최대값**); 본문 활자 −2.18(Co2↔P3) = 눈금 교정점 | ⭐⭐ **우리 §B 산물(Co₉S₈+Li₃PO₄)의 원자단위 첫 걸음.** §7b 의 핵심 근거 |
| 3a,b | (a) LCO\|LNO — CoO₆ 와 NbO₆ 가 매끄럽게 맞물림. (b) LNO\|LPS — **Nb–S 결합 없음**, Nb1 만 NbO₄ 사면체 | 버퍼층 기하 기준. 우리 Nd-인산염 *in-situ* 상과 대비할 그림 |
| 3c | LCO\|LNO 의 `Co1↔Li/Nb`. `figure-read ≈` Li +1.27/+2.00/+2.36 · **Nb +1.27/+1.01/+0.93** | **[Ncube26] LNTO +0.144 eV 와 7~9배 차**. §7a-③ |
| 3d | LNO\|LPS 의 `P1↔Li/Nb`. `figure-read ≈` Li +2.25/**+4.55**/+3.30 · Nb **−1.05**(사면체 Nb1)/+1.22/+1.60 | 🔴 **버퍼층의 구멍**: 사면체 자리는 P 에게 먹힌다. Zhang 2018 의 *"300 사이클 뒤 Co 재출현"* 과 이어지는 고리 |
| 4 | 계면 PDOS (a) pristine (b) Co2↔P3. 원점 = pristine 점유대 상단. `figure-read ≈` **E_F 0.1 → 0.4 eV 이동**, 계면 유효 갭 ≈ 0.4 eV, 0.4–0.8 eV 에 **CoO₄ 유래 받개 준위** | ⭐ 기전의 유일한 직접 증거. **우리도 계면 갭·계면 준위를 낸 적이 없다**(§11-②) |
| S1 | 계면 3종 pristine (측면 + 상면). **셀 상자 양끝이 비어 있다 = 단일계면 + 진공** `figure-read ≈` 14–16 Å | ✅ 우리 v5 기하(single + vacuum 30 Å)의 문헌 근거 재확인 |
| S3 | (a) Co1↔P3 (b) Co2↔P3 완화구조. (a) 는 P 가 2층 CoO₆ 의 O 를 빼앗아 **PO₄+CoO₅**, (b) 는 **PO₆ 직접**. **둘 다 쫓겨난 Co 는 LPS 안에서 CoS₄ 사면체** | Co1 이 예외인 구조적 이유. "Co 는 S 사면체로 간다" 의 시각 증거 |
| S4 | Co2↔P3 전/후 결합길이 12개. Co–O 1.92 → P–O 1.63–1.84 (수축) · P–S 2.06 → Co–S 2.08–2.15 (팽창) | ⚠ **이미지로 안 봤다** — PDF 텍스트에 12개 값이 전부 있고 평균까지 검산했다 |
| S5c,d | 벌크 PDOS. (c) **LCO+P_Co**: 갭 내 결함준위 **없음**, 갭 `figure-read ≈` 2.05 eV, **E_F 가 전도대 바닥**. (d) **LPS+Co_P**: **고립 Co 3d 준위 `figure-read ≈` +1.35 eV(비점유)**, E_F ≈ 0.7, CB ≈ 2.85 | ⭐ **"벌크에서는 전자가 갈 곳이 비싸다" 의 직접 증거.** §5.4-b |
| S6 | 6× Co↔P 계면 구조. LPS 영역에 **CoS₄ 사면체 6개**, LCO 안에 PO₆. **구조는 여전히 결정질** | 🔴 **"비정질화" 가 계산된 적 없다는 증거** — 본문 추론과 그림의 거리. §10-② |
| S7 | 6× Co↔P 계면의 **Li 공공 형성에너지**(괄호 = pristine). LCO 층간 3.2–4.0 → 2.2–2.8 · **계면 Li 3.3 → 1.6** · **LPS 최저 1.4 → 0.9** | ⭐⭐ **혼합 → SCL 가속** 의 유일한 정량. **pristine 1.4 = 2014 편 LP2 1.44 eV** 로 교차검증됨 |
| Table S1 | 계면 3종 최적화 격자상수 (γ 포함) | *우리 산수*로 면내 면적 341 / 143 / 398 Å² 환산 |
| Table S2 | 벌크 LCO(Hexagonal 9.821/9.821/14.04) · LPS(Ortho 13.13/16.12/12.36) | ⚠ SI 본문은 LCO 를 *"tetragonal"* 이라 쓴다(내부 불일치) |
| Table S3 | **LCO·LPS 벌크 결함 총에너지 (Ry)** — 9개 값 | ⭐⭐⭐ **이 논문의 재현성 그 자체.** 우리가 +1.986 / +2.844 / −1.619 eV 를 전부 재현했다 |

---

## 9. Post-processing ★

| 항목 | 내용 |
|---|---|
| **한 것** | **PDOS 만.** QE nscf **2×1×1** (Γ 밀도 기반) → 원소별 투영. `Fig. 4`(계면) · `Fig. S5c,d`(벌크) |
| 구조 시각화 | **VESTA** (ref 44) — 다면체 렌더로 배위환경(CoO₄/CoO₆/PS₄/PO₆/NbO₄/NbO₆)을 **논증 도구로** 쓴다 |
| 에너지 해석 | **손계산**. 교환에너지 = 총에너지 차; 벌크 대조 = `Table S3` 의 합차. **스크립트·툴 언급 0** |
| 전하 분석 | ⛔ **Bader·Löwdin·Mulliken 전부 없다.** 산화수(P⁵⁺ / Co²⁺ / Co⁵⁺)는 **조성에서 센 형식전하**다 |
| 결합 분석 | ⛔ **COHP/COBI 없다.** 결합 논의는 **길이(Å) 비교**뿐 |
| 정전 해석 | **ESM** 으로 분극 점검만 하고 **결과는 안 싣는다**(*"negligible"*) |
| ⛔ **안 한 것** | NEB · 장벽 · MD · 포논 · 탄성 · ELF · CDD · BVSE · hull/ESW · W_ad · 결함 형성에너지 vs E_F 도표 · 유한크기 보정 · 셀크기 수렴 |

> 🔑 **우리가 배울 점 하나**: 후처리가 **PDOS 하나**뿐인데도 논증이 닫힌다. 이유는 **벌크 vs 계면이라는 대조군을 셋업에 심어 뒀기 때문**이다(`Table S3`). ⇒ **도구를 늘리는 것보다 대조군을 설계하는 것이 싸고 강하다.**

---

## 10. 비판 — 이 논문의 약한 곳 ★★

### ① 🔴🔴 **스핀 비편극 — 그런데 기전을 떠받치는 구조가 하필 그 예외다**

SI 는 이렇게 쓴다:

> *"we neglect spin polarization effects, which become important **only in the presence of the CoO₄ structure**. Namely, the exchange energies related to only the **Co1** atom … are expected to be **slightly** changed by spin polarization. Therefore, the spin polarization effects for exchange energies **will not change our conclusions**."*

그런데 §5.4 의 기전은 **"계면의 pseudotetrahedral CoO₄ 가 만드는 낮은 준위"** 다 (`Fig. 4` 캡션·본문 ref 46). **면제 대상과 논증 주체가 같은 구조다.** 게다가:
- **Co1 만의 문제가 아니다.** `Co↔P` 는 **Co 를 사면체 CoS₄ 로 보낸다** — 16개 전부. 사면체장의 Co 는 고스핀이 기본이다.
- **벌크 대조의 P_Co 는 Co²⁺(d⁷)를 2개 만든다** — 팔면체 Co²⁺ 는 자성이다. 즉 **비편극은 +1.98 eV 쪽도 흔든다.**
- **비편극 틀 안의 DFT+U** 자체가 특수하다. Dudarev/Anisimov +U 의 통상 효과(국소 d 준위 분리)는 스핀 분해를 전제한다.
⇒ **"결론은 안 바뀐다" 는 검증이 아니라 선언이다.** 스핀편극 대조 계산이 **단 하나도 없다.** 우리 규율(보고량 카드 §판정 기준: *"열린 껍질 · 산화환원 활성은 위험 신호"*)로 보면 **여기가 P0 다.**
🟡 **완화 요인**: 부호 스윙이 **4.16 eV** 로 매우 크다. 스핀 안정화가 보통 0.3–1 eV 대인 것을 감안하면 **결론의 부호는 살아남을 가능성이 높다.** 흔들리는 것은 **크기와 자리별 순위**다.

### ② 🔴🔴 **동역학이 0인데 결론은 "rapidly" 다**

*"can be therefore expected to **proceed rapidly**"* (결론) · *"there is a **minimal energetic barrier** in the beginning of this process"* (본문).
**둘 다 계산된 적이 없다.** 이 논문에 있는 것은 **두 완화 상태의 에너지 차**뿐이고, **saddle point 는 한 번도 안 찾았다.** 반응이 내리막이라고 장벽이 낮은 것은 아니다 — 특히 **양이온 스왑은 두 원자가 서로를 지나가야 하므로 조밀한 골격에서 장벽이 클 수 있다.**
⇒ ⛔ **인용할 때 *"쉽게 일어난다"* 로 옮기면 안 된다.** 쓸 수 있는 것은 *"열역학적으로 내리막이고 중간상 핵생성을 요구하지 않는다"* 까지다.
🟢 다만 **"핵생성을 요구하지 않는다" 는 진짜 주장**이고, 그건 계산으로 뒷받침된다(벌크 +1.98 → 계면 −2.18).

### ③ 🟠 **4.16 eV 를 전자항에 전부 귀속했는데 밴드정렬로는 ~2.5–3.3 eV 뿐이다**

§5.4 의 *우리 산수*: 전자 2개 × (전도대 2.05 − 계면준위 0.4~0.8) ≈ **2.5–3.3 eV**. 관측 차는 **4.16 eV**. **남는 0.9–1.7 eV** 를 설명할 것은 구조 완화·정전·계면 자체의 안정화인데, 논문은 그 셋을 **전부 "주된 원인이 아니다" 로 깎아 놓았다**(구조는 정성 판정, 정전은 Co↔Nb 대조로 간접 기각).
⇒ **분해(decomposition)가 없다.** 우리가 이식할 때 *"계면 준위가 지배한다"* 까지는 되고 *"계면 준위가 전부다"* 는 안 된다.

### ④ 🔴 **버퍼층의 구멍을 스스로 찾아 놓고 가정으로 덮는다**

`P1↔Nb1 = −1.1 eV` (사면체 NbO₄). 저자 대응: *"Although coated buffer layers are regarded to be an **amorphouslike phase**, we **expect** that there are **not too many** tetrahedral sites."*
- **비정질에서 사면체 Nb 분율은 가정할 것이 아니라 계산·측정할 것**이다. 비정질화는 보통 저배위 자리를 **늘린다.**
- 실제 LNO 코팅은 **비정질로 쓰는 것이 표준**이다(ref 17 이 그렇게 말한다).
- **그리고 이 구멍이 후속 실험과 맞아떨어진다** — [Ncube26] 이 인용하는 Zhang 2018 은 **LNTO 코팅에도 300 사이클 후 Co 확산을 다시 관측**한다.
⇒ 🔑 **이 논문의 버퍼층 결론은 "결정질 LNO 에서, 팔면체 Nb 가 지배적일 때" 라는 조건부다.** 인용할 때 그 조건을 떼면 안 된다.

### ⑤ 🟠 **±0.5 eV 의 배열 산포를 자인해 놓고 오차막대로 쓰지 않는다**

SI: *"we tried to calculate many other exchange defects, and the exchange energies indicate almost the same values (**within the 0.5 eV deviation**)."*
그 산포를 **본문 어느 값에도 붙이지 않는다.** 결과:
- `Co↔Nb` 의 **+0.93 ~ +1.27 eV** 는 산포 ±0.5 와 **거의 같은 크기**다 ⇒ *"1 eV"* 라는 차단 여유는 **오차막대 한 개 폭**이다.
- `Co↔P` 는 −0.95 ~ −3.78 로 산포보다 훨씬 커서 **결론이 안전하다**.
⇒ **버퍼층 결론이 혼합 결론보다 훨씬 약하다.** 논문은 둘을 같은 확신으로 쓴다.

### ⑥ 🟠 **탈리튬 결론이 한 점에서 구간으로 외삽된다**

계산한 것: `2V_Li / 144원자 LCO` = **x = 0.944**. 쓴 문장: *"Li_xCoO₂ (**0.5 < x < 1**) cathode can easily introduce the P_Co defects."*
- x = 0.5 는 계산 안 됐다. 그 영역에서는 **Co³⁺→Co⁴⁺ 산화, 격자 c 축 팽창, 상전이**가 일어나 정공의 에너지 위치가 달라진다.
- 게다가 이 계산은 **벌크끼리**다 — 계면에서의 탈리튬 효과는 **계산되지 않았다**(가장 궁금한 칸인데).
⇒ ✅ **방향은 신뢰할 만하다**([Jiang22Se] hull 이 독립으로 같은 방향). ⛔ **"0.5 < x < 1 전 구간" 은 인용하지 않는다.**

### ⑦ 🟠 **Γ 점 하나로 계면 총에너지를 다 낸다**

계면 셀의 짧은 축이 **13.94 Å**(LCO/LPS)·**9.98 Å**(LCO/LNO)이다. 특히 LCO/LNO 의 9.98 Å 는 Γ-only 로는 얇다. 그리고 이 계는 **E_F 근처에 계면 준위가 있어** 부분점유가 생기는데, **부분점유 밴드의 Γ-only 적분은 위험하다.** 저자 자신도 **PDOS 에는 2×1×1 을 썼다** — 즉 Γ-only 가 얇다는 것을 알고 있었다. 그런데 **에너지는 전부 Γ-only 다.** k 수렴 검사 **0건**.

### ⑧ 🟠 **셀 크기 수렴·결함 상호작용 검사 0건**

중성 스왑이라 monopole 은 없지만 **쌍극자·사중극자 이미지와 계면 분극**은 남는다. 그리고 **스왑은 두 결함을 특정 거리에 놓는 연산**이라 거리 의존성이 값에 들어간다 — 논문은 그 의존성을 **보여주기는 하지만**(P1→P4) **분리하지는 않는다.** 더 큰 셀에서의 재현 검사가 없다.

### ⑨ 🟡 **본문 서술과 그림이 6곳에서 어긋난다** (전부 내가 판독으로 잡은 것)

| # | 본문 | 그림(`figure-read`) |
|---|---|---|
| 1 | Li2–6 은 *"1−3 eV"* | Co1↔Li2 **0.92** · Co1↔Li4 **0.73** (1 미만) · Co2↔Li5 **3.38** (3 초과) |
| 2 | 저에너지 경로를 **Co1 관점에서만** 서술 | 최저 막대는 **Co2↔Li1 (0.20)** |
| 3 | Co↔P 는 *"less than −1 eV"* | Co4↔P4 **−0.95** |
| 4 | 인용값은 **−2.18**(Co2↔P3) | 🔴 **최대 구동력은 Co2↔P1 −3.78 — 본문에 단 한 번도 안 나온다** |
| 5 | LCO\|LNO 의 Co↔Li 는 *"1−2 eV"* | **2.36** |
| 6 | LNO\|LPS 의 P↔Li 는 *"higher than 1 eV"* | **4.55** |

전부 **결론을 바꾸지는 않지만**, 📌 **#4 는 성격이 다르다** — **논문 전체에서 가장 큰 구동력을 서술에서 누락**했다. 인용할 때 우리는 **범위(−0.95 ~ −3.78)로 쓰는 편이 정직하다.**

### ⑩ 🟡 **SI 내부 불일치 1건** — SI 본문은 LCO 벌크를 *"144-atom **tetragonal** cell"* 이라 쓰는데 `Table S2` 는 **Hexagonal (a=b=9.821, c=14.04 Å)** 이다. a=b 이므로 **Table 이 맞고 본문이 오기**로 보인다. 결과에 영향 없음.

### ⑪ 🟡 **"관측된 Co 농도를 재현하도록 6회" 의 근거가 없다**

*"The number of exchange was set to reproduce the observed Co concentration"* (ref 24 = Sakuda). **그 농도가 몇인지, 6회가 그 셀에서 몇 %인지, 어떻게 환산했는지 한 줄도 없다.** `Fig. S7` 의 모든 수치가 이 "6" 위에 서 있다.

### ⑫ 🟡 **전압이 간접이다 (저자 자인)**

*"our simulation interface cell does **not treat the cathode voltage directly**, and discussion for applied voltage is simply based on Li-vacancy formation energies. A more sophisticated approach such as that used in ref 37 (Leung & Leenheer) is necessary in future studies."*
⇒ **Li 공공 형성에너지 ≈ 추출전압** 이라는 대응은 **중성 셀 근사**다. 실제 계면에는 전위 강하와 전기이중층이 있다. **정직하게 자인했다는 점은 인정할 만하다.**

### ⑬ 🟢 **오래된 것은 흠이 아니다 — 다만 관례 차이 3개는 적어 둔다**

| 2017 관례 | 2026 관례 | 영향 |
|---|---|---|
| **vdW 없음** (PBE 순정) | 계면·흡착엔 D3(BJ) 가 사실상 표준 | 🟡 **산화물\|황화물 계면은 이온결합 지배**라 vdW 민감도가 흡착계보다 낮다. 그래도 **계면 간격·부착일은 흔들린다**(교환에너지는 덜) |
| **ultrasoft PP 40/320 Ry** | PAW 500–600 eV | 🟢 USPP 40/320 은 당시 수렴 관례로 적절. 우리 comp1(70/560 Ry)보다 낮지만 **차이 에너지라 상쇄된다** |
| **무질서 처리 = 없음** (β-Li₃PS₄-b 로 분율점유를 제거) | SQS/enumeration | 🟡 **β-LPS 의 Li 분율점유를 "4c 를 뺀 정렬 구조" 하나로 대표**한다. 이건 **당시 표준**(Lepley 2013)이고, 우리 아지로다이트 S/Cl 무질서 문제와 **같은 종류의 미해결**이다 — 우리가 그들을 나무랄 처지가 아니다 |

---

## 11. 적용 인사이트 — 우리 연구에 어떻게 ★

### ① ⭐⭐⭐ **계산 0회로 지금 당장: 우리 §B 의 "핵생성 반론" 을 닫는 인용**

우리 `comp1|LiCoO₂ −0.3227 eV/atom` 은 **종점 열역학**이고, 예상 반론은 *"평형은 그렇더라도 중간상 핵생성이 막지 않느냐"* 다. [Wu26MLIF] §2.5 가 이미 그 형태로 왔다.
**이 논문이 그 칸에 딱 들어간다** — 같은 양극(LCO), 같은 음이온 화학(PS₄ 황화물), **첫 원자 교환이 −2.18 eV 내리막**, 그리고 활자로:
> *"the Co-interdiffusion is likely to occur **without requiring the nucleation and growth of an interfacial layer**"*
⛔ **단 "rapidly" 는 안 가져온다**(§10-②). 가져오는 것은 **"핵생성 요구 없음"** 까지.

### ② ⭐⭐ **계산 소규모: 우리 계면의 "갭 내 준위" 를 처음 본다**

이 논문의 기전은 전부 **계면 갭 준위**다. 그런데 우리는 **벌크 갭만 있다**(comp1 2.066 / modelc 2.099 eV, fixed-occ nscf). **계면 갭도 계면 준위도 계산한 적이 없다.**
**우리 기존 자산으로 바로 된다** — `adhesion.json` 의 v5 계면 구조(LiNiO₂\|LPSCl)가 이미 있다. 거기에 **fixed-occ nscf + PDOS** 를 붙이면:
- **계면 유효 갭**이 벌크 2.07 보다 얼마나 좁아지는가 (Haruyama 계면은 `figure-read ≈` 0.4 eV 로 **벌크의 1/5**)
- **그 준위의 성격이 무엇인가** — 우리는 **LOBSTER 가 이미 돌아가므로 ICOHP 로 배위까지 짚을 수 있다** (그들은 못 했다)
⚠ **선결**: 보고량 카드. *"계면 갭" 의 정의*(어느 원자층까지를 계면으로 볼 것인가 · 층분해 PDOS 인가 전체 DOS 인가 · fixed-occ 인가)를 **돌리기 전에** 적는다. 우리 band gap 규율(DOS-threshold 금지)이 그대로 적용된다.

### ③ ⭐⭐ **계산 중간: 아지로다이트에서 `Co ↔ ?` 스왑 — 이 논문이 답 못 하는 질문**

β-Li₃PS₄ 에는 **PS₄ 하나**뿐이지만 **Li₆PS₅Cl 에는 세 종류의 음이온 자리**가 있다: **PS₄ 의 S(16e) · free S²⁻(4a/4d) · Cl⁻**. ⇒ **Co 가 어디로 가는가는 우리 계에서 다시 물어야 한다.**
**Eq. (1) 을 그대로 쓰면 된다** (조성보존 스왑 ⇒ μ 불필요, 중성 ⇒ 전하보정 불필요). 후보:
- `Co ↔ P` (PS₄ 의 P) — Haruyama 와 직접 대조
- `Co ↔ Li` (4d Li) — 음성 대조군
- **`Co` 가 free S 근방 / Cl 근방에 갈 때의 차이** — ⭐ **이것이 우리 고유 질문이다.** 우리 ESW 가 S²⁻-limited 이므로 **free S 가 Co 의 우선 표적일 수 있다.**
- **Nd 치환계**(`comp1+Nd`)에서 같은 스왑 — **Nd 가 그 자리를 선점해 Co 를 막는가?** ⇒ **우리 §D 보호 기전의 원자단위 증거가 될 수 있다.**
⚠ **선결 3개**: (a) 우리 무질서 배열 규율 — 어느 S/Cl 배열에서 재는가, 배열 산포를 몇 개로 잡는가(Haruyama 의 **±0.5 eV** 가 참고 눈금) (b) **스핀** — 우리는 Co 를 다루므로 **반드시 스핀편극**으로 간다(§10-① 을 반복하지 않는다) (c) **UMA 로 할 것인가 QE 로 할 것인가** — 교환에너지는 **결함 화학**이라 UMA 외삽 위험이 크다. **QE DFT+U 가 맞다.**

### ④ ⭐ **범위 선언 — 우리 §2b 보호율에 한 줄 더**

[Ncube26] 이 **기계 경로**를 열었고, 이 논문이 **SCL/수송 경로**를 하나 더 연다. 둘 다 우리 보호율(화학 소모)이 못 세는 칸이다. ⇒ 원고 문구를 이렇게 넓힌다:
> *"본 보호율 지표는 P 매개 TM 소모 경로에 한정된다. 계면 기계 손실(박리), 계면 전자구조에 의한 국소 안정화, 그리고 양이온 혼합이 유도하는 Li 고갈층 성장은 포함하지 않는다."*

### ⑤ ⭐ **방법 이식 2건 (값이 아니라 절차)**

| 가져올 것 | 왜 | 어디에 |
|---|---|---|
| **"벌크 대조군을 셋업에 심는다"** | 이 논문의 논증력 전부가 **+1.98(벌크) vs −2.18(계면)** 이라는 **한 쌍**에서 나온다. 도구를 안 늘리고도 인과가 닫힌다 | 우리 계면 계산 전부. **보고량 카드 §2 "대조 잡" 칸에 벌크 짝을 명시** |
| **원시 총에너지 공개** | `Table S3` 덕분에 우리가 9년 뒤에 3개 값을 재현했다. Ncube 는 못 한다 | 우리 SI 관례로 채택 — `db/properties/*.json` 에 이미 하고 있지만 **논문 SI 에도 싣는다** |

### ⑥ ⚠ **하지 말 것**

- ⛔ **교환에너지를 우리 hull 값(eV/atom)과 같은 표에** — 단위도 층위도 다르다.
- ⛔ **−2.18 eV 를 "LPSCl 에서도" 로 옮기기** — free S·Cl 이 없는 계다.
- ⛔ **"Co↔P 가 빠르게 일어난다"** — 장벽이 없다(§10-②).
- ⛔ **"LNO 버퍼가 Co 를 막는다" 를 무조건으로** — 결정질·팔면체 Nb 조건부다(§10-④).
- ⛔ **0.69 J/m² 부착일을 이 논문 값으로** — **2014 편 값**이다.

---

## 12. 인용 가능 문장 (영문 초안)

> **(a) 우리 §B 를 원자단위로 떠받칠 때**
> *Haruyama et al. showed by DFT+U that the elementary Co↔P cation exchange across a LiCoO₂(110)/β-Li₃PS₄(010) interface is exothermic for every site pair examined (−0.95 to −3.78 eV; −2.18 eV for the representative Co2↔P3 pair), whereas the same exchange performed between the two **isolated bulk** crystals costs **+1.98 eV**. The sign reversal — which we reproduce from their tabulated total energies — indicates that the interface removes the energetic penalty normally associated with nucleating a mixed phase, consistent with their conclusion that Co interdiffusion "is likely to occur without requiring the nucleation and growth of an interfacial layer."*

> **(b) 우리 hull 산물과 이어 붙일 때**
> *Our grand-potential interfacial-reactivity calculation predicts Co₉S₈ and Li₃PO₄ among the products of the Li₆PS₅Cl|LiCoO₂ reaction, i.e. a net Co→S / P→O anion re-partitioning. Haruyama et al. resolved the atomistic elementary step of exactly this re-partitioning at a LiCoO₂/β-Li₃PS₄ interface, and attributed its driving force to low-lying interfacial states derived from pseudo-tetrahedral CoO₄ units at the edge of the CoO₂ layers.*

> **(c) 탈리튬(고전압) 축**
> *The same work reports that introducing only two Li vacancies into the LiCoO₂ supercell (Li₀.₉₄CoO₂) reverses the bulk Co↔P exchange energy from +1.98 to −1.62 eV, indicating that partial delithiation alone can open cation mixing even in the absence of an interface.*

> **(d) SCL / 수송 손상**
> *Cation mixing also lowers the Li-vacancy formation energies throughout the interfacial region (from 1.4 to 0.9 eV at the most labile Li₃PS₄ subsurface site, and from 3.3 to 1.6 eV at the interfacial Li site), so that "one P_Co defect can produce two additional Li vacancies" — i.e. the mixing accelerates growth of the Li-depletion (space-charge) layer.*

> **(e) 버퍼층을 조건부로 인용할 때**
> *A LiNbO₃ buffer suppresses the exchange (Co↔Nb: +0.93 to +1.27 eV), which the authors ascribe to Co and Nb both occupying octahedral sites so that no low-lying tetrahedral acceptor state forms. **Notably, the same work finds P↔Nb to be exothermic (−1.1 eV) at the one tetrahedral NbO₄ site present**, so the protection is conditional on the buffer remaining octahedrally coordinated.*

> **(f) 보고량 정의의 모범으로 인용할 때**
> *We adopt the composition-conserving exchange energy of Haruyama et al., E_ex = E_tot(A_i↔B_j) − E_tot(pristine), evaluated on charge-neutral cells with the lattice fixed at the relaxed pristine geometry; because the operation conserves stoichiometry exactly, no chemical-potential reservoir and no finite-size charge correction are required.*

---

## 13. 주의 / 한계 (인용 규율) — ⛔ 금지 목록

| ⛔ 금지 | 이유 |
|---|---|
| 교환에너지를 **우리 `db/properties/*` 나 hull 값과 같은 표에** | 단위(eV/사건 vs eV/atom)·층위(점결함 vs 상평형)·물질계(β-LPS vs LPSCl) 전부 다름 |
| *"Co↔P 가 빠르게/쉽게 일어난다"* | **장벽이 계산된 적 없다**(§10-②). 허용은 *"열역학적으로 내리막이고 핵생성을 요구하지 않는다"* |
| *"LNO 버퍼가 Co 확산을 막는다"* 를 **무조건으로** | 결정질·팔면체 Nb 조건부. **사면체 자리에서는 −1.1 eV 로 뚫린다**(§10-④) |
| *"Li_xCoO₂ 0.5 < x < 1 에서 혼합이 유리"* | 계산된 것은 **x = 0.944 한 점**(§10-⑥) |
| **−1.109 / +0.144 eV**([Ncube26])를 이 논문 값과 **나란히 "같은 양"** 으로 | **Ncube 에 정의가 없다.** 나란히 놓을 수 있는 것은 *"정의 유무"* 와 *"부호"* 뿐(§7a) |
| **−2.18 eV 만** 인용 | 범위가 **−0.95 ~ −3.78** 이고 **최대값이 본문에 없다**(§10-⑨-4). **범위로 쓸 것** |
| **0.69 J/m²** 부착일을 이 논문 것으로 | **[Haruyama 2014]** 값이다 (`refs.json[37]`) |
| 계면 유효 갭 `≈ 0.4 eV` 를 **수치로** | **순수 figure-read** 이고 본문에 활자값이 없다. *"벌크보다 크게 좁다"* 까지 |
| 이 논문을 **동역학 근거로** | MD·NEB 0회. 동역학 칸은 여전히 [Ncube26] 뿐 |
| *"spin 은 무시해도 된다"* 를 우리가 따라 하기 | 저자 자신의 면제 근거가 **논증 주체와 겹친다**(§10-①). **우리는 스핀편극으로 간다** |

---

## 14. 우리 원장 매핑 (요약표)

| 우리 축 | 이 논문이 주는 것 | 등급 |
|---|---|---|
| **§B③ 양극 계면 반응성** | **종점(hull) ↔ 첫 걸음(스왑)** 의 연결 + *"핵생성 불요"* 활자 | ⭐⭐⭐ **인용 필수** |
| **§B 고전압(탈리튬) 축** | Li₀.₉₄CoO₂ 만으로 벌크 부호 반전 (+1.98 → −1.62 eV) — [Jiang22Se] hull 과 독립 교차검증 | ⭐⭐ |
| **§D Nd 기전** | ⚠ 어휘 충돌 경고(Li transfer ≠ Li budget) + **NdPO₄ 의 사면체 PO₄ 가 새 질문을 연다** | ⭐⭐ (경고 + 질문) |
| **§E dual compatibility** | **부분 선점(형태)** — 버퍼를 두 계면으로 쪼개 각각 평가 | ⚠ 인용으로 해소 |
| **§2b 보호율** | 🔴 **범위 선언 필요** — SCL/수송 경로를 못 센다 | 🔴 |
| **§H 운동학 공백** | ⛔ **못 채운다.** 이 논문도 0 K 정적이다 | — |
| **계면 전자구조 (신규 칸)** | **계면 갭 준위** 개념 — 우리에게 아예 없던 축 | ⭐⭐ **§11-②** |
| **방법(보고량 정의)** | **5/5 모범 사례** + 원시 총에너지 공개 | ⭐⭐⭐ **보고량 카드 외부 표본** |
| **방법(계면 기하)** | 2014 편이 이미 우리 v5 의 1차 근거. 이 편이 그 기하의 **화학적 활용 예** | ✅ 기존 판정 유지 |
| **A 이온전도 / C 기계 / D 전자구조 4축** | ⛔ **대응물 없음** (Ea·D·C_ij·ESW·COHP 전부 0) | — |

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **교환에너지 (exchange energy, E_ex)** | 두 원자의 **자리를 맞바꾼** 뒤의 에너지 − 바꾸기 전 에너지. **조성이 정확히 보존**되므로 화학퍼텐셜 저수지가 필요 없다 | Eq. (1). 이 논문의 유일한 보고량 |
| **antisite / 반자리 결함** | 원래 A 가 있어야 할 자리에 B 가 앉은 것. 표기 `B_A` | `P_Co`(LCO 의 Co 자리에 P), `Co_P`(LPS 의 P 자리에 Co) |
| **Kröger–Vink 표기** | 결함 표기 관례. `V_Li` = Li 공공, `Li_i` = Li 격자간(interstitial) | `P_Co + 2V_Li`, `Co_P + 2Li_i` |
| **SCL (space-charge layer)** | 두 이온전도체가 만나면 화학퍼텐셜 차 때문에 이온이 한쪽으로 쏠려 생기는 **전하 분리층**. 황화물 SE 쪽이 Li 고갈되면 저항이 된다 | 2014 편의 주제. 이 논문은 **혼합이 SCL 을 키운다**를 더한다 |
| **DFT+U (Dudarev/Anisimov)** | 전이금속 d 궤도의 자기상호작용 오차를 Hubbard U 로 보정. LCO 의 Co 3d 처럼 국소화된 전자에 필요 | U(Co 3d) = **5.9 eV**. ⚠ **비편극 틀 안에서** 썼다 |
| **USPP (ultrasoft pseudopotential)** | 파동함수를 매우 부드럽게 만들어 cutoff 를 낮추는 대신, **augmented charge 에 별도의 높은 cutoff** 가 필요 | 40 Ry / 320 Ry (8배 비) |
| **NCC (nonlinear core correction)** | 반심(semicore) 전자가 있는 원소에서 교환상관을 제대로 내기 위해 **코어 전하를 명시적으로 넣는** 보정 | P·S·Co·Nb 에 적용 |
| **ESM (effective screening medium)** | 슬랩 계산에서 주기 이미지 사이의 가짜 정전 상호작용을 없애기 위해 **가상의 유전/금속 매질**을 넣는 방법 | 분극 점검용으로만 쓰고 *"차이 없음"* 으로 PBC 결과만 보고 |
| **pseudo-tetrahedral CoO₄** | 층상 LCO 의 CoO₂ 층이 **끊긴 모서리**에서 Co 가 O 를 4개만 갖게 되는 국소 구조. 팔면체와 달리 **갭 안에 낮은 준위**를 만든다 | 이 논문 기전의 **전부** (`Fig. 4`, ref 46 = Qian 2012) |
| **β-Li₃PS₄-b** | β-Li₃PS₄ 의 Li 분율점유를 계산 가능하게 만든 정렬 근사 — **4c 자리 Li 를 제거**한 것 (Lepley 2013) | 벌크 LPS 128 원자 셀. Li_i 는 그 4c 에 되넣는다 |
| **BEP 관계 (Bell–Evans–Polanyi)** | 발열 반응일수록 장벽이 낮다는 **경험적 상관**. **장벽 계산의 대체물이 아니다** | 저자의 *"minimal energetic barrier"* 가 이 유형의 유추 (§10-②) |
| **grand-potential / pseudo-binary** (대조용, 이 논문엔 없음) | 조성 공간에서 Li 화학퍼텐셜을 열어 두고 hull 까지의 거리를 재는 방법 (Richards 2016 = 이 논문 ref 29) | **우리 §B 의 방법.** 이 논문은 인용만 하고 쓰지 않는다 |

<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# 탄소 인터레이어 ↔ LPSCl 계면의 **박리 인성 Γ** 가 anode-free 전지의 **Li 석출 위치**를 정한다 — lamination(제조 압착)압 100 → 400 MPa 에서 Γ **9 → 41 J m⁻²** · 문턱 **≈10 J m⁻²** · 180° peel + tape 소성굽힘 보정 — Liao · Zeng · Mulla · Madanchi · Kawakami · Aihara · Aotani · Thouless · Dasgupta (*Adv. Mater.* 37, 2502114 (2025))

> slug `liao2025_interfacial_adhesion_li_plating_carbon_interlayer` · DOI `10.1002/adma.202502114` · type `exp (180° peel 박리시험 + tape 소성굽힘 보정 해석 · adhesive/cohesive failure 판정 · PFIB-SEM; anode-free Li6PS5Cl)` · PDF `13a03ed5-1._Effects_of_Interfacial_Adhesion_on_Lithium_Plating_Location_in_Solid_State_Batteries_with_Carbon_Interlayers.pdf` (+ SI `1057dbe5-1._Sup_Effects_of_Interfacial_Adhesion_….pdf`, 14 pp) · digested `2026-09-23` · status ✅

> elements: Li, C, P, S, Cl
> methods: adhesion

> ⚠⚠ **세 줄 경고 — 인용 전에 반드시.**
> ① **압력 축은 *lamination(제조 압착)* 압력이다** (100–800 MPa, 1 분 유지). 사이클 중 적층압(stack)은 **5 MPa · 60 °C 고정**이다.
>    "stack pressure 100→400 MPa 에서 4배" 로 옮기면 틀린다 (작업 브랜치 `docs/adhesion_agc_interlayer_20260923.md` §6 표의 "적층압" 표기가 이 오해를 부른다 — §7-4).
> ② **인터레이어에 Ag 가 없다.** 카본블랙(Denka Li-100, ≈30 nm) 또는 하드카본(≈3 µm) + **PVDF 14 wt%** 뿐이다 → Ag–C 인터레이어에 값을 그대로 옮기지 않는다.
> ③ **Γ 는 실용 계면 인성(G_c 부류)** 이다 — 박리 팔(Kapton)의 소성굽힘만 빼고, 탄소/PVDF 층 안의 소산·거칠기 맞물림은 **그대로 들어 있다**.
>    **W_ad(열역학 점착일) 가 아니다** — 같은 줄에 놓지 않는다 (§7-1).

---

## 1. 한 줄 요약

**anode-free 황화물 전지에서 탄소 인터레이어는 Li 를 "집전체(CC) 쪽"에 석출시키는 것으로 알려져 있는데, 그 위치를 정하는 것은 수송만이 아니라 *탄소 ↔ SE 계면 점착*이다.**
lamination 압을 100 → 400 MPa 로 올리면 탄소/LPSCl 계면 인성이 **9 ± 2 → 41 ± 5 J m⁻² (≈4.6배)** 로 오르고,
**Γ_carbon–SE 가 ≈10 J m⁻² 문턱을 넘으면 Li 가 CC 쪽에만**, 그 아래면 **SE 쪽(또는 양쪽)** 에 석출된다.
입자 크기·재질이 다른 **하드카본(≈3 µm)** 에서도 문턱이 **비슷한 범위(≈10 J m⁻²)** 에서 나타난다.
같은 탄소를 **액체 전해질**에 넣으면 Li 가 반대편(분리막 쪽)에 석출된다 → 고체계의 CC-쪽 석출을 **수송만으로는 설명할 수 없다**.
⇒ 이 트랙(Ag–C 인터레이어 임계 점착)의 **유일한 정량 실험 앵커**: *G_c(P_lamination)* 곡선 + *"G_c 가 석출 위치를 가른다"* 는 기능적 의미.

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | **Daniel W. Liao**¹, Davy Zeng², Muzamil Mulla¹, Ali Madanchi¹, Hiroki Kawakami³, Yuichi Aihara³, Koichiro Aotani³, **M. D. Thouless**¹²(계면 파괴역학), **Neil P. Dasgupta**¹²\* |
| 소속 | ¹Univ. Michigan Mechanical Eng. · ²Univ. Michigan Materials Sci. & Eng. · ³**Nissan Research Center**, Nissan Motor Co. (Yokosuka) |
| 서지 | *Adv. Mater.* **2025**, 37, 2502114 (issue 29) · DOI `10.1002/adma.202502114` · **Open access CC BY** |
| 일정 | Received 2025-01-30 · Revised 2025-04-09 · Published online 2025-05-12 |
| 자금 | Nissan Motor Co. · NSF GRFP DGE-1256260 (D.W.L.) |
| 키워드 | adhesion, anode-free, carbon interlayer, lithium metal anode, mechanical properties, solid-state battery |
| 계보 | 같은 그룹 전작 **Liao et al., *J. Mater. Chem. A* 12, 5990 (2024)** (ref 36) = 같은 탄소 인터레이어의 전류밀도·리튬화 경로 연구. Ag–C 원조는 ref 29 (**Lee et al., *Nat. Energy* 5, 299 (2020)** — Aihara 공저). Li–Ag 기전은 ref 37 (**Spencer-Jolly et al., *Joule* 7, 503 (2023)**). 박리 해석은 Kendall 1971/1975 · Kim & Aravas 1988 · Yu & Spaepen 2004 |
| 연구 유형 | **실험 전용** — 시뮬레이션(DEM/MPM/FEM) 없음. 해석은 박리 팔(tape)의 탄소성 굽힘 에너지 수지(SI) 뿐 |
| 데이터 | "available from the corresponding author upon reasonable request" (원자료 비공개) |

## 3. 핵심 수치 ★

### 3.1 박리 시험 원장 — SI **Table S1** 전체 (인쇄값) + 파괴 위치

> 2F/b = 탄성·비신장 가정의 180° 박리 인성 (N m⁻¹ = J m⁻²). Γ = tape 소성굽힘 보정 후 계면 인성.  n = 3 (평균 ± 표준편차).

| 인터레이어 | lamination P [MPa] | 2F/b [N m⁻¹] | **Γ [J m⁻²]** | 파괴 위치 · 지위 | 출처 |
|---|---|---|---|---|---|
| amorphous carbon | "5" | 12 ± 2 | **7 ± 1** | ⚠ 본문은 이 값을 **CC(스테인리스)/탄소 계면**(주조·건조 직후, lamination 전) 인성으로 쓴다. 5 MPa 조건의 탄소/SE 계면은 **전사가 안 돼 < 7** 로만 묶인다 | Table S1 · p3 · p4 · Fig. 2d 점선 화살표 |
| amorphous carbon | 100 | 16 ± 4 | **9 ± 2** | 탄소/SE 계면 박리 (탄소가 tape 로 완전 전사) | Table S1 · Fig. 2d · Fig. 5a |
| amorphous carbon | 200 | 29 ± 4 | **15 ± 2** | 탄소/SE | 〃 |
| amorphous carbon | 300 | 55 ± 6 | **26 ± 4** | 탄소/SE (Fig. 2b,c 사진이 이 조건) | 〃 |
| amorphous carbon | 400 | 96 ± 11 | **41 ± 5** | 탄소/SE | 〃 |
| amorphous carbon | 600 | 157 ± 12 | 65 ± 5 | ⚠ **Kapton/탄소 계면**에서 떨어짐 → 탄소/SE 인성은 **≥ 65 (하한)** | Table S1 · Fig. S9d |
| hard carbon | 100 | 1 ± 0.5 | **1 ± 0.5** | 탄소/SE (보정 불필요 — 순탄성) | Table S1 · Fig. 5a |
| hard carbon | 200 | 3 ± 1 | **3 ± 0.5** | 탄소/SE | 〃 |
| hard carbon | 300 | 11 ± 2 | **7 ± 1** | 탄소/SE | 〃 |
| hard carbon | 400 | 19 ± 4 | **11 ± 2** | 탄소/SE | 〃 |
| hard carbon | 500 | 22 ± 6 | ⚠ 인쇄 "**128 ± 3**" | 탄소/SE. 🔴 **SI 오타로 판정** — Fig. 5a 의 채운 원은 figure-read ≈**12**(막대 ≈9–15)이고 2F/b = 22 와도 12 급이 맞다 ⇒ **12 ± 3 으로 읽는다** | Table S1 ↔ Fig. 5a |
| hard carbon | 600 | 33 ± 1 | 16 ± 1 | ⚠ **Kapton/탄소** → 탄소/SE **≥ 16 (하한)** | Table S1 · Fig. 5a 빈 원 · Fig. S9d |
| hard carbon | 800 | 36 ± 1 | 18 ± 1 | ⚠ **Kapton/탄소** → 탄소/SE **≥ 18 (하한)** | 〃 |

- **헤드라인 배수**: amorphous 100 → 400 MPa = 41/9 = **4.6배** (초록의 "4-fold"). 같은 400 MPa 에서 amorphous/hard = 41/11 ≈ **3.7배** (본문 "approximately four times lower").
- **전사 조건 (논리 하한)**: amorphous 탄소가 SE 로 넘어가려면 Γ_carbon–SE > Γ_CC–carbon(7 ± 1) 이어야 한다 → 측정된 탄소/SE 값은 전부 7 초과 (p3). 하드카본은 **mylar** 위에 주조해 이 하한이 없다 (그래서 1 ± 0.5 까지 잴 수 있었다).

### 3.2 Li 석출 위치 지도 (0.1 mA cm⁻² · 2.0 mAh cm⁻² · 5 MPa · 60 °C)

| 인터레이어 | lamination | Γ_carbon–SE [J m⁻²] | **Li 석출 위치** | 근거 그림 |
|---|---|---|---|---|
| amorphous | **5 MPa (lamination 없음)** — 주조 탄소/CC 를 400 MPa 로 미리 치밀화한 SE 에 5 MPa 로만 누름 | **< 7** (전사 안 됨, Fig. S6) | **탄소/SE 계면에만** | Fig. 3c |
| amorphous | 100 MPa | 9 ± 2 | **양쪽 혼재** — 어떤 자리는 CC 쪽, 어떤 자리는 SE 쪽 · 일부 자리에서 **탄소층 응집(cohesive) 파괴** | Fig. 3b · Fig. S4 |
| amorphous | 100 MPa, 초기 단계 (0 V 까지 0.01 mA cm⁻² 리튬화 후 +0.15 mAh cm⁻² @0.1) | 9 ± 2 | 계면 **미세 공동(cavity)** 에 우선 핵생성 | Fig. S5 |
| amorphous | 400 MPa | 41 ± 5 | **CC/탄소 계면에만** (여러 위치 확인) | Fig. 3a · Fig. S2 |
| amorphous | 600 MPa | ≥ 65 | **CC 쪽** | Fig. S3 |
| hard | 200 MPa | 3 ± 0.5 | **탄소/SE 에만** | Fig. 5b · Fig. S11a,b |
| hard | 400 MPa | 11 ± 2 | **탄소/SE** ("threshold had not yet been reached") | Fig. S10 |
| hard | 600 MPa | ≥ 16 (tape 파괴 하한) | **CC 쪽에만** (여러 위치 확인) | Fig. 5c · Fig. S11c,d |
| amorphous, **액체 전해질** (1 M LiTFSI DOL/DME + 1 wt% LiNO₃, Celgard, 무가압, RT) | 주조 상태 | — | **분리막 쪽 탄소 표면** (고체계와 반대) | Fig. S7 |

- **문턱**: 본문·결론 모두 **"≈10 J m⁻²"** 이고 두 탄소계에서 **비슷한 범위**. Fig. 5a 는 이를 단일 값이 아니라 노란 **"Threshold Regime"** 띠(figure-read ≈5–15 J m⁻² 의 그라데이션)로 그린다 — *"실험 불확도 + 그 범위 안에서는 가끔 양쪽에 석출"* 이라는 이유.
- ⚠ **실제로 괄호 친 구간** (이 digest 의 재구성, §10-6): hard carbon 은 **11 ± 2 → SE**, **≥ 16 → CC** ⇒ 문턱 ∈ (≈11, ≈16]; amorphous 는 **9 ± 2 → 혼재**, 41 ± 5 → CC (200·300 MPa 석출 시험 없음).

### 3.3 재료 · 공정 수치

| 항목 | 값 | 출처 |
|---|---|---|
| SE | **Li₆PS₅Cl (LPSCl)**, MSE Supplies 입수 그대로, **평균 입경 10 µm** | Experimental |
| SE 펠릿 | **두께 1 mm · 지름 6 mm**, 200 MPa 냉간압착 green pellet | 〃 |
| amorphous 탄소 | **carbon black Denka Li-100**, 평균 입경 **≈30 nm**, 인터레이어 두께 **≈13 µm** | p2 · Experimental |
| hard carbon | Pred. Materials International, 입경 **≈3 µm** | p7 · Experimental |
| 바인더 · 슬러리 | **탄소 : PVDF = 86 : 14 wt%**, NMP, Thinky ARE-310 원심 유성 믹서 | Experimental |
| 주조 기판 | amorphous → **스테인리스 박**, hard carbon → **mylar 필름**(전사를 돕기 위해) | 〃 |
| 주조 · 건조 | screen printer · 공기 중 80 °C 20 min → 100 °C 12 h | 〃 |
| lamination | **100 / 200 / 300 / 400 / 500 / 600 / 800 MPa, 1 분 유지** (단축 압착, SS 핀) | Experimental · Fig. 1a |
| lamination 후 SE 표면 거칠기 | **0.5–1.0 µm** (amorphous 탄소 계면) | Experimental |
| 집전체 | **10 µm 스테인리스 박** (전 셀 공통). ⚠ 주조 박은 lamination 후 떼어낸다 | 〃 · p2 |
| 상대극 | Li 박 1.5 mm (Thermo) 긁어 광택 → **17.7 MPa** 로 압착 | 〃 |
| 셀 | PEEK 슬리브 내경 6 mm · CC 와 금속 핀 사이 **전도성 탄성체**(균일 압력) | 〃 |
| 운전 | **적층압 5 MPa · 60 °C** · OCV 1 h 평형 · Arbin LBT · **0.1 mA cm⁻² → 2.0 mAh cm⁻²** | 〃 |
| amorphous 탄소 리튬화 용량 | **≈0.25 mAh cm⁻²** (ref 36) — 2.0 mAh cm⁻² 는 이를 크게 넘겨 금속 Li 석출을 보장 | p3 |
| PFIB | Thermo Fisher **Helios G4 PFIB UXe**, **Xe** 플라즈마, **0.2 µA · 30 kV** (Li 반응 최소화) | Experimental |
| 광학 | Keyence VHX-7000 4k, Ar 글러브박스 안 | 〃 |

### 3.4 박리 팔(Kapton tape) 상수 — SI

| 상수 | 값 | 비고 |
|---|---|---|
| tape 폭 b | **3 mm** | 본문 Peel Test |
| tape 두께 t | **25 µm** (보정 곡선은 25 · 100 µm 둘 다 계산, 변환은 25 µm 로) | SI p3 · p6 |
| tape 영률 E | **3.6 GPa** | SI p3 |
| 경화 법칙 σ = Aεⁿ | **n = 0.51 · A = 381 MPa · ε_Y = 0.01** (Yu & Spaepen 2004 자료 적합) | SI p6 |
| 비신장 가정 근거 | 측정 F 가 **2Ebt 보다 세 자릿수 작다** | SI p3 |

## 4. 방법 ★ (실험 전용 — 시뮬레이션 슬롯은 "없음" 으로 명시)

### 4.1 시뮬레이션 방법 — **없음**
- **DEM / MPM / FEM / CZM: 수행하지 않았다.** 계면 에너지 수지(Fig. 4)는 **정성 도식**이고 어떤 항에도 값이 없다.
- 선행 계산 인용은 한 줄뿐: *"a previous computational study … predicted that weak adhesion can lead to interfacial separation"* (ref 53, Yang·Mo *Adv. Mater.* 2021).
- **입자 처리 ★**: n/a (모델 없음). 실물 입자는 탄소 ≈30 nm / ≈3 µm, LPSCl ≈10 µm. *"lamination 압이 높을수록 소성이 커져 계면이 conformal 해진다"* 는 서술(p2)이 유일한 형상-변형 언급이고 **정량 없음**.

### 4.2 lamination 절차 (Fig. 1a)
주조한 탄소층(CC 위)을 잘라 6 mm LPSCl 펠릿 위에 올리고 **SS 핀으로 단축 압착** → 1 분 유지 → 주조 박을 떼면 탄소층이 SE 로 **완전 전사**. 5 MPa 대조군만 lamination 없이 주조 상태를 **400 MPa 로 미리 치밀화한 SE** 에 5 MPa 로 누른다 (Fig. S6: 탄소가 SE 로 넘어가지 않는다).

### 4.3 박리 시험 (Fig. 2a · Experimental)
- Ar 글러브박스 안. lamination 후 **CC 를 떼고** 3 mm 폭 Kapton tape 를 탄소층에 붙인다.
- LPSCl 펠릿을 **수직으로 고정**하고 tape 를 기판에 대해 **α = 180°** 로 당긴다 — **추를 조금씩 더해 과부하**시켜 박리가 날 때의 하중 F 를 기록 (정하중 증분 방식).
- 조건당 **n = 3**, 평균 ± 표준편차.
- 박리 후 광학으로 **파괴 위치**를 판정 (Fig. 2b,c · Fig. S9b,c): 100–400 MPa 는 전부 **탄소/SE 계면** (탄소층이 tape 로 통째로 전사, *"rapid … complete removal … across the length of the LPSCl pellet"*); >500 MPa(hard) · 600 MPa(amorphous) 는 **tape/탄소 계면**.

### 4.4 ★ 박리 해석 — 탄성식 + tape 소성굽힘 보정 (SI pp 3–7)

**(i) 탄성 · 비신장 180° 박리 (Kendall):**  `Γ = 2F/b`  (SI Eq. 2)
유효 조건 두 가지(본문 p3): 박리 팔의 탄성 변형에너지가 무시 가능 + 계면이 충분히 취성이어서 **박리 팔 소성굽힘 없이** 박리.

**(ii) 문제:** 박리 후 Kapton 이 **영구적으로 말려 있었다** → 균열선단의 굽힘모멘트 M 이 tape 를 항복시킨다 (Fig. S1a, `M = Fd`).

**(iii) 에너지 수지 (Kim & Aravas 계열):**
- 균열 평형: `Γ b = M_max κ_max − ∫₀^κmax M dκ`  (Eq. 3)
- 180° 박리의 단위 균열진전당 소산 일: `2F = M_max κ_max − 6 M_max² / (E b t³)`  (Eq. 4) — 굽힘 전체 일 − 제하 시 회수되는 탄성에너지
- 재료: 항복 전 선형탄성, 이후 `σ = A εⁿ` (Eq. 5), 제하는 탄성. `ε = y κ` (Eq. 6), `M = 2b ∫₀^{t/2} σ y dy` (Eq. 7)
- 탄성 구간 `M = E t³ b κ / 12` (κ ≤ 2ε_Y/t, Eq. 9)
- 탄소성 구간 (Eq. 10, **이 digest 의 재유도** — PDF 텍스트층이 깨져 있어 Eq. 8 로부터 다시 적분했다; 인쇄 구조와 일치):
  `M = [ (2/3) E ε_Y³ − 2A ε_Y^{n+2}/(n+2) ] · b/κ²  +  [ 2A (t/2)^{n+2}/(n+2) ] · b κⁿ`   (2ε_Y/t ≤ κ ≤ κ_max)
  (검산: 항복점 연속성 `A ε_Yⁿ = 381 × 0.01^0.51 ≈ 36 MPa = E ε_Y = 36 MPa` ✓ — 이 digest 산술)
- Eq. 3 + Eq. 4 를 연립해 **측정 F → Γ** 곡선을 얻는다 (Fig. S1b: 탄성선 `Γ = 2F/b` 대비 t = 100 µm · 25 µm 곡선이 아래로 휜다).
- 결과: **가장 낮은 값(≈1.2 J m⁻², 표의 1 ± 0.5)만 보정이 필요 없고**(선단이 탄성), 나머지는 전부 보정 → Γ/(2F/b) = **0.41–0.64** (§13-2).

### 4.5 전기화학 · 단면 관찰
- 0.1 mA cm⁻² 정전류로 2.0 mAh cm⁻² 석출 (in-situ Li 음극 형성) → Xe-PFIB 단면을 **여러 위치**에서 (400 MPa: Fig. S2 두 위치 · 100 MPa: Fig. S4 두 위치 · hard 200/600: Fig. S11 각 두 위치).
- Fig. S5 의 초기단계 시료는 **0 V 까지 0.01 mA cm⁻² 로 먼저 완전 리튬화** → 이후 0.1 mA cm⁻² 로 0.15 mAh cm⁻² 추가 (석출 Li 가 탄소로 다시 삽입되지 않게).

### 4.6 대조 실험 — 액체 전해질 (Fig. S7)
같은 주조 탄소/SS 를 작동극으로 코인셀: Li 14 mm ≈500 µm · 1 M LiTFSI in DOL/DME + 1 wt% LiNO₃ · Celgard · RT · **무가압** · Maccor 4000. 2 mAh cm⁻² @ 0.1 mA cm⁻² 후 **분리막에 닿은 탄소 윗면**에 Li.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | a) lamination 모식 (SS 핀 / CC / 탄소 / LPSCl, 100–400 MPa) · b,c) PFIB 단면 **100 MPa: 계면 공동(cavities) · 400 MPa: conformal** (스케일바 5 µm) · d,e) 저압 = "lower bonded area" / 고압 = 밀착 모식 | **A_real(P) 의 정성 증거** — 우리 Tabor A=F/H · MPM 소성 coverage 축과 같은 자리. 정량(접촉 분율) 없음 |
| 2 | a) 180° 박리 기하 (α, b, F) · b,c) 300 MPa 박리 후 펠릿·tape 광학 (탄소가 tape 로 통째 전사 = **계면 파괴**) · d) **Γ vs lamination P** (amorphous 100–400) + CC/탄소 7 J m⁻² 점선 | ★ **우리 DEM 박리 G_c(P) 의 대조 곡선** (보정 Γ 열과 비교) · 파괴 위치 판정 방식 그대로 차용 |
| 3 | 2.0 mAh cm⁻² 석출 후 PFIB 단면 — a) **High 41 J m⁻²: CC 쪽 Li** · b) **Moderate 9 J m⁻²: i) SE 쪽 Li(탄소 위로 들림) ii) CC 쪽 Li** · c) **Low (< 7) : SE 쪽 Li** | 기능적 의미 — G_c 가 석출 위치를 가른다. 우리 모델엔 석출이 없으므로 **G_c 쪽 절반만** 대조 가능 |
| 4 | 에너지 수지 모식 — 저항 ρ_Li+, ρ_e- · 과전압 η_CC–carbon, η_carbon–SE · 응력 σ_CC, σ_carbon, σ_SE, σ_Li · 계면에너지 γ(CC–Li, Li–carbon, carbon–SE, Li–SE) · 인성 Γ(CC–carbon, carbon–SE); 고Γ(a,b) vs 저Γ(c,d) | **두 계면의 상대 인성**이 핵심 변수 — Ag–C 트랙은 인터레이어/SE 와 **인터레이어/CC** 둘 다 재야 한다 (§8-④). 모든 항이 **값 없는 정성** |
| 5 | a) **Γ vs lamination P, amorphous(■) vs hard(●)**, 빈 원 = Kapton/탄소 파괴, 배경 = SE 쪽 석출(파랑)·**Threshold Regime(노랑)**·CC 쪽(초록) · b) hard 200 MPa (3 J m⁻²) → SE 쪽 · c) hard 600 MPa ("16 J m⁻²") → CC 쪽 | ★ 두 탄소계의 문턱 공유 주장 근거. ⚠ c) 의 16 은 **tape 파괴 하한**이다 (§10-3) |
| S1 | a) 180° 박리 선단의 굽힘모멘트 M = Fd, 곡률 1/κ · b) **Γ vs 2F/b**: 탄성선 vs t = 25 · 100 µm 보정 곡선 (0–160 N m⁻¹) | 박리 팔 소성 보정의 크기 — 2F/b 를 그대로 쓰면 최대 **2.4배 과대** |
| S2 | amorphous 400 MPa, 두 위치 — Li 전부 CC 쪽 | 위치 반복성 증거 (위치 수 2) |
| S3 | amorphous 600 MPa — Li CC 쪽 | 〃 |
| S4 | amorphous 100 MPa, 두 위치 — **탄소층 응집 파괴**로 SE 쪽 ↔ CC 쪽 석출이 넘어가는 전이부 | "혼재" 영역의 기하 — 탄소층 cohesive 파괴 |
| S5 | amorphous 100 MPa 초기 석출 — 계면 공동 안의 Li (스케일바 2.5 µm) | 공동 = 삼상 경계(전자·이온·빈공간) 핵생성 자리 |
| S6 | 5 MPa 대조 — a) LPSCl 펠릿(깨끗) b) 주조 탄소/SS (탄소가 CC 에 남음) | Γ_carbon–SE < 7 의 근거 |
| S7 | 액체 전해질 — Li 가 분리막 쪽 탄소 표면에 | 수송만으로는 CC 쪽 석출 설명 불가 |
| S8 | hard carbon 400 MPa lamination 단면 — 3 µm 입자, 덜 conformal | 입자 크기 → conformality → Γ ↓ |
| S9 | 600 MPa: a) tape/탄소 박리 모식 · b,c) 펠릿에 탄소 잔존·tape 노랑 · d) **Kapton/탄소 인성 막대 amorphous ≈65 · hard ≈16** | 상한 쪽 값이 **하한**임을 보여주는 그림 |
| S10 | hard 400 MPa 석출 — Li 가 여전히 SE 쪽 | 11 ± 2 는 문턱 **아래** |
| S11 | hard 200 MPa (a,b: SE 쪽) vs 600 MPa (c,d: CC 쪽) | 문턱 괄호의 양 끝 |
| Table S1 | 2F/b · Γ 전 조건 | §3.1 전사 |

### 5.1 크롭 색인 — `litdb/figures/liao2025_interfacial_adhesion_li_plating_carbon_interlayer/`

| 파일 | 대상 | 확인 |
|---|---|---|
| `fig_1.png` · `fig_2.png` · `fig_3.png` · `fig_4.png` · `fig_5.png` | 본문 Fig. 1–5 (**본문 그림 5개 = 크롭 5장**) | 5장 전부 Read 로 봄 |
| `fig_S1.png` … `fig_S11.png` | SI Fig. S1–S11 (11장) | 11장 전부 Read 로 봄 |
| `tab_S1.png` | SI Table S1 | Read 로 봄 — 500 MPa hard carbon "128±3" 인쇄 확인 |

전부 `tools/litdb/extract_figures.py` 의 캡션 앵커 영역 렌더 (쪽 전체 스크린샷 아님). 본문 서술과 어긋난 그림 = **Fig. 5c 라벨 "16 J m⁻²"** (tape 파괴 하한인데 계면 인성처럼 표기) · **Table S1 "128±3"** (Fig. 5a 와 불일치).

## 6. Post-processing ★

- **무엇**: 180° 박리의 **임계 하중 F** → 탄성 인성 2F/b → tape 탄소성 굽힘 보정 Γ (Eq. 3–10) · 광학 파괴 위치 판정(계면 vs tape/탄소) · PFIB 단면의 **Li 위치 범주화** (CC / SE / 양쪽).
- **도구**: 추 증분 하중 (로드셀 없음) · Keyence 광학 · Xe-PFIB SEM. 통계는 조건당 n = 3 평균 ± 표준편차 (*"No additional pre-processing"*).
- **수치화·플롯**: Γ vs P_lam 선+점 (Fig. 2d, 5a), 파괴 위치는 **채운/빈 기호**로 부호화, 석출 위치는 **배경색 3 영역**으로 겹쳐 그림 (Fig. 5a). 석출 위치는 **정량 지표 없이** 대표 단면으로 보고.
- ⚠ **없는 것**: 하중-변위 곡선(정상상태 박리력), 박리 속도, 모드 혼합각 ψ, 박리 시 온도(셀은 60 °C), 공동 면적 분율, 석출 위치의 자리별 통계.

## 7. 우리 대비 — 점착 트랙 + DEM+MPM (→ `our_dem_baseline.md` 는 정본에 값 0 개 자리표시; 우리 값은 작업 브랜치 CLAUDE.md · `docs/adhesion_agc_interlayer_20260923.md` 기준)

| 항목 | 이 논문 | 우리 | 같은가 / 다른가 · 이유 |
|---|---|---|---|
| 계면 | **카본블랙(+PVDF 14 wt%)/LPSCl**, 하드카본/LPSCl | 목표: **LPSCl ↔ Ag–C 인터레이어**, **Ag–C ↔ VGCF 호스트** | **다름** — Ag 없음, 바인더 PVDF 가 점착에 섞임. 값 전이 금지, **형태(Γ–P 관계·문턱 개념)만** 전이 |
| 측정량 | **Γ = 실용 계면 인성** (박리 팔 소성만 제거) | DFT 팀 **W_ad** (가역, 원자) + 우리 DEM **G_c,eff(P)** (하한, 소성 소산 미포함) | Liao Γ 는 **DEM G_c 와 같은 부류**, W_ad 와는 **다른 부류** (§7-1) |
| 크기 | **1–65 J m⁻²** | W_ad 가설: 물리흡착 ~0.01–0.3 · 화학결합 ~1–5 J m⁻² (트랙 문서 §1) | 400 MPa 의 41 J m⁻² 는 화학결합 W_ad 상한(5)의 **≥ 8배** → 소산·면적 증폭 없이는 설명 불가 = 트랙 §1 "섞지 말 것" 의 실례 |
| 압력 축 | **lamination 100–800 MPa (1 min)**, 운전은 5 MPa | 트랙 §3 DEM 박리: "구동압 P 로 누른 뒤 → θ 로 당김" | **프로토콜 형태는 같다**(누르고 당김). 단 대조하려면 DEM 을 **100–400 MPa lamination 압**에서 돌려야 한다 (트랙 §2 의 "수~수십 MPa" 구간은 Liao 에 대응점이 없다) |
| 박리 기하 | 180°, b = 3 mm, Kapton E 3.6 GPa · t 25 µm | 트랙 §3: `G = (F/b)(1 − cos θ)`, 탄성 보정 Kendall | θ = 180° 에서 두 식이 같다 (2F/b). ★ 실물의 지배 보정은 **탄성 신장이 아니라 박리 팔 소성**(§4.4) — 신장 항은 ≈0.03 J m⁻² 로 무시 가능 (§13-3). DEM 결과는 **보정 Γ 열**과 비교 |
| 형상 소성 | "lamination 압↑ → 소성↑ → conformal" (정성, Fig. 1) | MPM: 참 소성 형상 변화 · 소성 vs 강체 coverage (CLAUDE.md "MPM coverage PLASTIC vs RIGID") · DEM: Tabor A = F/H (Stage-E) | **우리가 정량할 수 있는 절반** — A_real(P) 를 우리가 내면 Γ(P) = W_eff · A_real(P)/A_nom + 소산 을 **분해**할 수 있다 (§8-③) |
| 기능적 결과 | Γ_carbon–SE ≳ 10 → CC 쪽 석출 | 석출·전기화학 모델 없음 | 우리 모델 **밖**. 문턱 자체는 대조 불가, G_c 쪽만 |
| frame[4] | 실험 → **독립 대조 표적** | DEM 은 W_ad 입력으로 돌리고 결과만 Liao 와 나란히 | ⛔ sjkr cohesion 을 9 → 41 에 맞춰 튜닝하지 않는다 |
| frame[5] | 실험이 가진 반쪽 = **G_c(P) + 석출 위치** | 없는 반쪽 = **A_real, 소산 분해, W_ad, traction–separation** | DEM(접촉면적·박리력) + MPM(소성 conform) 이 그 빈 반쪽을 채울 수 있다 |

### 7-1. ⛔ W_ad 와 Γ 를 섞지 않는 이유 — 이 논문 자체가 실례
Γ(400 MPa) = 41 J m⁻² 인데 **같은 LPSCl 의 벌크 파괴에너지**는 K_IC 환산으로 ≈3–5 J m⁻² (트랙 문서 §6 결론 ②의 산술: K 0.3·E 24 → 3.2 · K 0.17·E 4.7 → 5.3; ⚠ 이 digest 가 한 값이 아니다). 그런데 박리는 **SE 안이 아니라 계면**에서 났다 (Fig. 2b: tape 가 지나간 띠의 LPSCl 표면이 광학 해상도에서 대체로 깨끗 — 검은 점 몇 개뿐).
⇒ 측정 Γ 의 대부분은 **계면 분리일이 아니라 박리되는 층(탄소/PVDF) 안의 소산**이어야 한다 (이 digest 의 추론 — 논문은 소산 분해를 하지 않았다).
⇒ 트랙 문서 §6 결론 ① *"실효 박리값은 계면 W_ad 와 SE 자체 벽개 중 약한 쪽이 상한"* 은 **가역 분리일(W_ad·γ) 층위에서만** 성립하고, 실용 Γ 에는 **상한으로 쓰면 안 된다** — Γ 는 소산 때문에 그 상한을 쉽게 넘는다.

### 7-2. 우리 DEM 박리 시험(트랙 §3 단계 3)에 주는 설계 사양
1. **lamination 압 스윕 = {100, 200, 300, 400} MPa** — Liao amorphous 4 점과 1:1.
2. 비교 열 = **Γ (보정)**, 2F/b 아님.
3. 파괴 위치를 기록 (계면 / 인터레이어 응집 / 박리 팔) — Liao 가 채운/빈 기호로 한 것과 같은 판정.
4. 하한 라벨: 우리 sjkr 는 PVDF 소성 소산이 없으므로 **G_c,eff ≪ Γ_Liao 가 정상**이다 — 차이는 "소산 몫" 의 정량 (frame[4] 의 정보이지 실패가 아니다).

### 7-3. 우리 그룹 원고와의 접점
정본 `papers/ahn2026_cej_agno3_pvp_li3n_anodefree.md` (Hanyang Jong-Won Lee 그룹 · AgNO₃–C 인터레이어 anode-free, 미출판) 가 같은 **"인터레이어가 Li 핵생성 자리를 정한다"** 축이다. 그 원고엔 점착 수치가 없다 ⇒ Liao 의 "Γ 문턱" 개념이 그 원고 계열의 **빠진 기계 축**을 가리킨다 (값 이식 아님).

### 7-4. 🔴 트랙 문서 표기 정정 권고 (작업 브랜치, 이 digest 는 고치지 않음)
`docs/adhesion_agc_interlayer_20260923.md` §6 표의 Liao 행 *"적층압 100 → 400 MPa 에서 4배"* → **"lamination(제조 압착)압 100 → 400 MPa 에서 9 ± 2 → 41 ± 5 J m⁻² (4.6배); 운전 적층압은 5 MPa"** 가 원문에 맞다. 그리고 결론 ⇒ 줄의 "구동압" 대조는 lamination 압 축으로 바꿔 읽어야 한다.

## 8. 적용 인사이트 (우리 연구에 어떻게)

### ① ★★★ 점착 트랙의 **첫 정량 독립 대조 표적** — 그러나 "보정 Γ · lamination 축 · Ag 없음" 세 한정어와 함께
DEM 박리 G_c(P) 를 Liao amorphous 4 점(9/15/26/41 J m⁻² @ 100/200/300/400 MPa)과 **나란히** 놓는다. 튜닝 금지. 같은 계면이 아니므로(Ag 없음·PVDF) 비교 결론은 **자릿수와 P-의존 형태**까지다.

### ② ★★ 크기 판정 — "mJ 냐 J 냐" 는 W_ad 가 정하지만, **실용 G_c 는 수십 J m⁻² 급**이 가능하다
트랙 §0 의 목표(자릿수)에 대해: Liao 는 탄소/LPSCl 계면의 **실용** 인성이 **1–65 J m⁻²** 임을 보인다. W_ad 가 물리흡착 급(0.01–0.3)이어도 실용 Γ 는 J m⁻² 급일 수 있다 ⇒ 트랙 결론을 쓸 때 **"W_ad 의 자릿수" 와 "G_c 의 자릿수" 를 두 줄로** 적어야 한다.

### ③ ★★ **Γ ∝ P_lam (amorphous)** — Bowden–Tabor 면적 가설의 검정 가능한 예측
이 digest 산술(§13-4): amorphous 의 Γ/P = **0.090 / 0.075 / 0.087 / 0.103 J m⁻² MPa⁻¹** (100–400 MPa) — 원점 통과 기울기 **0.094** 로 거의 **선형**이다.
소성 접촉에서 A_real/A_nom ≈ P/H (Tabor) 이고 W_eff 가 일정하면 Γ ∝ P 가 나온다 ⇒ **우리 DEM 도 cohesion 에너지 밀도 일정에서 G_c,eff ∝ P 를 내야 한다** (못 내면 우리 접촉면적-압력 관계가 다른 것).
반면 하드카본은 **1 → 3 → 7 → 11** (Γ/P 0.010 → 0.028) 로 **초선형 개시** — 3 µm 입자가 0.5–1.0 µm SE 거칠기를 못 채우는 conformality 한계로 읽힌다(논문 p7 의 정성 설명). ⇒ **입자 크기 / 기판 거칠기 비**가 우리 DEM 의 두 번째 스윕 축이 된다. ⚠ n = 3·4 점 — TREND ONLY.

### ④ ★★ **"약한 계면이 벌어진다"** — Ag–C 트랙은 계면을 **둘** 재야 한다
Liao 의 기준은 절대 문턱이 아니라 **상대 비교**다 (Fig. 4 에 Γ_CC–carbon 과 Γ_carbon–SE 가 함께 있다). 우리 트랙 문서는 **인터레이어/SE** 와 **Ag–C/VGCF** 를 잡았는데, 석출 위치 문제로 보면 **인터레이어/CC** 가 세 번째 필수 계면이다. (단 Liao 는 적층 CC 의 Γ 를 재지 않았다 — §10-7.)

### ⑤ ★ MPM 쪽 — conformality(A_real) 를 **소성 유동**으로 재는 것이 우리 고유 기여
Fig. 1b,c 의 "공동 → 밀착" 은 우리 MPM 의 **소성 vs 강체 coverage 차**(CLAUDE.md 2026-06-21 절)와 같은 현상이다. P_lam 에 따른 계면 접촉 분율을 MPM 으로 내면, Liao Γ(P) 를 **면적 몫 × 소산 몫** 으로 쪼개는 데 쓸 수 있다 (frame[5]: DEM = 박리력·접촉망, MPM = 소성 conform).

## 9. 인용 가능 문장 (deck/paper 용)

- "Peel tests on carbon interlayers laminated onto Li₆PS₅Cl show that the interfacial toughness rises from 9 ± 2 to 41 ± 5 J m⁻² as the **lamination** pressure increases from 100 to 400 MPa (Liao et al., *Adv. Mater.* 2025)."
- "Above an interfacial toughness of ≈10 J m⁻² between the carbon interlayer and the solid electrolyte, Li plates preferentially at the current-collector side (Liao et al. 2025)."
- "Such practical interfacial toughness values (1–65 J m⁻²) exceed typical thermodynamic works of adhesion by orders of magnitude and must not be compared with them directly." — ⚠ 뒷문장은 **우리 해석**; 인용 시 우리 문장으로 표기.

## 10. 주의 / 한계 (over-claim 방지) — 비판적으로

1. **압력 축 = lamination(제조) 압**. 사이클 적층압(5 MPa)·온도(60 °C)는 전 조건 고정. "stack pressure 의존성" 으로 인용 금지.
2. **Γ = 개시(initiation) 실용 인성**. 추를 증분해 과부하 → 박리가 *"rapid"* 하게 전 길이를 달린다(불안정 전파). 정상상태 박리력·하중–변위 곡선·추 증분 크기(분해능)·박리 속도 미보고. **모드 혼합각**(180° 박리는 혼합 모드) 논의 없음.
3. **상단 값 3개는 하한** — amorphous 600 (65 ± 5), hard 600/800 (16 ± 1 / 18 ± 1) 은 **tape/탄소** 파괴다. **Fig. 5c 의 "High (16 J m⁻²)" 라벨은 탄소/SE 인성이 아니라 그 하한**이다.
4. **SI 오타 2건**: Table S1 hard carbon 500 MPa Γ **"128±3"** (Fig. 5a ≈12 와 불일치 → 12 ± 3 으로 읽음, figure-read) · SI p6 *"relationship between F and G shown in Fig. S11"* 은 **Fig. S1(b)** 를 가리켜야 한다.
5. **Table S1 의 "5 MPa" 행(7 ± 1)** 은 본문상 **CC(스테인리스)/탄소 주조 계면** 값이다. 5 MPa 조건의 탄소/SE 인성은 **측정되지 않았고 < 7 로만** 묶인다.
6. **문턱 괄호가 성기다** — amorphous 는 석출 시험이 5·100·400·600 MPa 뿐이라 9 (혼재) 와 41 (CC) 사이가 비어 있다. hard 는 11 ± 2 → SE · ≥16 → CC. ⇒ "≈10" 은 **괄호 (≈11, ≈16] (hard) + 혼재 ≈9 (amorphous)** 를 한 숫자로 요약한 것. 노란 띠는 적합값이 아니다. 박리 n = 3, 석출은 단면 "여러 위치"(보고된 단면은 조건당 1–3 장) — **자리 통계 없음**.
7. **실제 셀의 CC/탄소 인성은 미측정** — lamination 후 주조 박을 떼고 **10 µm SS 박을 CC 로 적층**한다(5 MPa). 7 ± 1 J m⁻² 는 **주조 상태** CC 계면(5 MPa 대조군)에만 해당. "어느 계면이 약한가" 의 한쪽 항이 laminated 셀에서는 비어 있다.
8. **두 탄소계가 여러 변수를 동시에 바꾼다** — 입경(30 nm vs 3 µm), 이온전도, 공극, 주조 기판(SS vs mylar). "같은 문턱" 은 **2점 일반화**다.
9. **Ag 부재** — Ag–C 인터레이어로 문턱을 옮기려면 Li–Ag 합금화(ref 37, Spencer-Jolly 2023)가 에너지 수지를 바꾸는 것을 먼저 따져야 한다.
10. **교란 변수** — lamination 압은 Γ 외에도 탄소층 밀도·공극·두께와 SE 표면 치밀화(거칠기 0.5–1.0 µm 는 amorphous 계면에서만 측정)를 함께 바꾼다. 에너지 수지(Fig. 4)는 **정성 가설**이고 γ·σ·η 어느 항에도 수치가 없다 ⇒ 인과는 상관 + 액체 대조(Fig. S7)로 **지지**될 뿐 증명되지 않았다.
11. **박리 온도 ≠ 운전 온도** — 박리는 글러브박스(온도 미기재), 셀은 60 °C. PVDF 가 섞인 층의 Γ 는 온도 의존일 수 있다 — 논문은 60 °C Γ 를 내지 않았다.
12. **frame 한정** — 이 논문은 형상 소성·접촉면적·W_ad 를 **재지 않는다**. "conformality ↑ 는 소성 때문" 은 단면 사진 2장 기반의 정성 서술.

## 11. 논증 흐름 (절별)

1. **서론** — anode-free 는 부피·공정 이점, 그러나 불균일 핵생성·SEI·필라멘트·박리 문제. Ag/Au/Mg/In 합금 인터레이어는 사이클 후 붙어 있지 못할 수 있어 **다공 탄소(–Ag) 인터레이어**가 대안(ref 29–31). 석출 위치가 CC 쪽/SE 쪽으로 보고마다 다르다(ref 29, 31, 33). 기존 기전 = 탄소 리튬화 → 과포화 → 석출, Ag 가 있으면 합금 형성(ref 37); Ag 없이도 CC 쪽 석출(ref 36) ⇒ 탄소 자체가 원인. 전류밀도 의존(ref 36). **"약한 계면이 벌어져 그 자리에 Li 가 자란다"** 는 제안(ref 31, 39, 42)은 있으나 **정량 계면 역학 데이터가 없다** → 이 논문의 빈칸.
2. **점착 제어 (Fig. 1)** — lamination 압으로 계면 형태를 바꾼다: 100 MPa 공동 / 400 MPa 밀착.
3. **정량 (Fig. 2, S1, Table S1)** — 180° 박리 + 소성 보정 → 9 → 41 J m⁻² 단조 증가. 파괴는 항상 탄소/SE 계면. CC/탄소 7 ± 1 은 측정 하한.
4. **석출 위치 (Fig. 3, S2–S6)** — 41: CC · 9: 혼재(+탄소 응집파괴·공동 핵생성) · <7: SE.
5. **수송만으로는 안 된다 (Fig. S7)** — 혼합전도체에서 이온 옴손실 > 전자 옴손실이면 SE 쪽 석출이 유리해야 하고, 액체계에선 실제로 분리막 쪽. 고체계 CC 쪽 석출은 **기계 항**이 필요하다.
6. **에너지 수지 가설 (Fig. 4)** — 5 묶음 항(저항·과전압·응력·계면에너지·인성) + 기하(두께·공극). 문턱 = SE 에서 탄소를 떼는 에너지 벌칙이 다른 구동력을 이길 때. 공동은 삼상 경계로 초기 핵생성 자리(전류 집중 + 주변 가압 없이 채울 수 있음). 이후 **"균열 같은 Li 층"** 이 계면을 따라 전파 — Γ_carbon–SE 가 크면 불리.
7. **두 번째 계 (Fig. 5, S8–S11)** — 하드카본: Γ 가 모든 P 에서 낮고(입자 큼 → conformal ↓), >500 MPa 에서 tape/탄소 파괴. 200 → SE, 400 → SE, 600 → CC ⇒ **비슷한 문턱 범위(≈10)**.
8. **결론** — 문턱 ≈10 J m⁻², 탄소 종류에 배타적이지 않음, 공정–구조(lamination–접촉–점착) 관계의 중요성, 향후 표면에너지·형태 공학과 모델링의 정량 입력으로.

## 12. 용어 미니 사전

| 용어 | 뜻 (이 카드의 용법) |
|---|---|
| **lamination pressure** | 인터레이어를 SE 에 **옮겨 붙이는 제조 단계의 단축 압착압** (여기서 100–800 MPa, 1 분). 운전 중 적층압(stack pressure, 여기 5 MPa)과 다르다 |
| **interfacial toughness Γ** | 계면 균열을 단위 면적 전진시키는 데 드는 **실용** 에너지 (J m⁻²). 박리 팔 외의 소산을 포함한 G_c 부류 |
| **W_ad (work of adhesion)** | 두 이상 표면을 떼는 **가역 열역학 일** γ_A + γ_B − γ_AB. 원자 계산량. Γ ≥ W_ad |
| **180° peel · 2F/b** | 박리 각 180° 에서 비신장·탄성 박리 팔이면 G = F(1 − cos θ)/b = 2F/b (Kendall) |
| **박리 팔 소성 보정** | 선단 굽힘모멘트로 tape 가 항복하면 일부 일이 tape 에서 소산 → Γ < 2F/b. Kim–Aravas 식 에너지 수지로 역산 |
| **adhesive vs cohesive failure** | 계면을 따라 떨어짐(adhesive, 여기 탄소/SE 또는 tape/탄소) vs 한 층 **내부**가 쪼개짐(cohesive, 여기 Fig. S4 의 탄소층) |
| **anode-free** | Li 금속 음극 없이 조립하고 첫 충전에서 in-situ 형성 |
| **PFIB (Xe)** | 제논 플라즈마 집속이온빔 단면 — Ga FIB 보다 Li 반응이 적다 |
| **threshold regime** | Fig. 5a 의 노란 띠 — 석출 위치가 넘어가는 Γ 범위(≈10 J m⁻²), 그 안에서는 양쪽 석출이 섞인다 |

## 13. 🧮 파생 계산 원장 (`derived(ours)`) — 전부 인쇄값에 산술만

### 13-1. 박리력 크기 (b = 3 mm, F = (2F/b)·b/2)
- hard 100 MPa: 2F/b = 1 N m⁻¹ → **F ≈ 1.5 mN** (≈0.15 gf) · amorphous 400 MPa: 96 → **F ≈ 0.144 N** (≈14.7 gf) · amorphous 600 MPa: 157 → **F ≈ 0.236 N** (≈24 gf).
- ⇒ 추 증분 방식으로 **두 자릿수 넘는 힘 범위**를 다뤘다 — 저 Γ 쪽(1–3 J m⁻²)의 상대 분해능이 가장 나쁘다 (증분 크기 미보고).

### 13-2. 소성 보정 계수 Γ/(2F/b)
- amorphous: 7/12 **0.58** · 9/16 **0.56** · 15/29 **0.52** · 26/55 **0.47** · 41/96 **0.43** · 65/157 **0.41**
- hard: 1/1 **1.0** · 3/3 **1.0** · 7/11 **0.64** · 11/19 **0.58** · 12/22 **≈0.55**(오타 보정값) · 16/33 **0.48** · 18/36 **0.50**
- ⇒ Γ 가 클수록 보정이 커진다 (tape 소성 몫 ↑). 2F/b 를 그대로 쓰면 최대 **2.4배 과대**.

### 13-3. 비신장 · 탄성 신장 항 검산
- 2Ebt = 2 × 3.6 GPa × 3 mm × 25 µm = **540 N** vs F_max ≈ 0.236 N → 비 ≈ **4×10⁻⁴** (SI 의 "세 자릿수" ✓).
- Kendall 신장 항 (F/b)²/(2Et): F/b = 78.5 N m⁻¹ 에서 6162/(2 × 3.6e9 × 25e-6) ≈ **0.034 J m⁻²** — 157 대비 무시 가능 ✓.

### 13-4. Γ–P 선형성 (TREND ONLY, n = 3 × 4 점)
- amorphous Γ/P_lam: **0.090 · 0.075 · 0.087 · 0.103 J m⁻² MPa⁻¹** (100/200/300/400). 원점 통과 최소제곱 기울기 = Σ(PΓ)/ΣP² = 28100/300000 = **0.094** → 예측 9.4/18.7/28.1/37.5 vs 측정 9/15/26/41.
- 절편 허용 직선: 기울기 **0.107**, 절편 **−4.0 J m⁻²** (x 절편 ≈37 MPa).
- hard Γ/P_lam: **0.010 · 0.015 · 0.023 · 0.028 · ≈0.024** (100–500) — 초선형 개시 후 포화.
- amorphous/hard 비 (같은 P): **9.0 (100) · 5.0 (200) · 3.7 (300) · 3.7 (400)**.

### 13-5. W_ad 대비 배수 (트랙 문서 §1 의 W_ad 범위 사용)
- Γ(400 MPa) 41 J m⁻² ÷ 화학결합 W_ad 상한 5 J m⁻² ≈ **8배 이상**; ÷ 물리흡착 0.3 J m⁻² ≈ **140배**. ⇒ 실용 Γ 의 대부분이 소산·면적·맞물림 몫이라는 정성 결론의 산술 근거 (W_ad 는 이 논문이 재지 않았다).

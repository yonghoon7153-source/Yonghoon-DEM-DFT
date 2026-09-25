# Cronau 2021 (ACS Energy Lett. 6, 3072−3077) — Stack-pressure 딜레마: 미세결정 황화물 SE의 "신뢰할 수 있는" σ_ion 측정법

> slug `cronau2021_stack_pressure_ionic_conductivity` · DOI `10.1021/acsenergylett.1c01299` · type `experiment` · PDF `02. How to Measure a Reliable Ionic Conductivity….pdf` · SI `nz1c01299_si_001.pdf` · digested `2026-07-28` · SI 보강 `2026-09-25` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_cronau2021_stack_pressure_ionic_conductivity.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.
>
> ⛔⛔ **SI 보강 2026-09-25 — 이 카드의 §0 판정 (A) 가 SI 를 안 읽어서 틀렸다** (stoic-knuth 원장 `SELF-51`).
> 2026-07-28 digest 는 **본문 6쪽만** 읽었다 (§10-6 에 "SI 미업로드" 라고 스스로 적어 두었다).  SI (10쪽, Fig. S1–S7 +
> Table S1) 에는 **GC-Li₆PS₅Cl (Fig. S1e) 과 µC-Li₆PS₅Cl (Fig. S2c)** 의 적층압 의존 σ 가 있고, µC-Li₆PS₅Cl 은
> 적층압 ≥ 146 MPa 에서 **2.88–3.46 mS/cm (digitized)** 로 평탄하다.  ⇒ *"Li₆PS₅Cl 미측정"* 과 *"3.0 mS/cm 은 이
> 논문에 없다"* 는 **철회**.  *"Cronau 2021 → LPSCl ≈ 3 mS/cm"* 은 **펠릿·고적층압 평탄값으로서 성립**하고, 틀린 것은
> **"단결정" 라벨**뿐이다 (SI 에도 단결정은 없다).  원문 판정 줄은 **이력으로 남기고** 줄마다 ⛔ 정정을 달았다.
> SI 전체 digest = **§S** (합성·측정법·Table S1 전문·Fig. S1/S2 디지타이즈 표·S3–S7).  S1/S2 판독 원자료 =
> `litdb/figures/cronau2021_stack_pressure_ionic_conductivity/si_digitized.csv` (재현: `tools/litdb/cronau2021_si_digitize.py`).




> elements: Br Cl Ge Li P S
> methods: dft

**인용:** M. Cronau, M. Szabo, C. König, T. B. Wassermann, B. Roling\*,
"How to Measure a Reliable Ionic Conductivity? The Stack Pressure Dilemma of
Microcrystalline Sulfide-Based Solid Electrolytes," *ACS Energy Letters*
**2021**, *6*, 3072−3077. DOI 10.1021/acsenergylett.1c01299.
Philipps-Universität Marburg (Roling 그룹). **Viewpoint** (6쪽). Open Access
(ACS AuthorChoice). Received 2021-06-23 / Accepted 2021-08-04.

**소재:** 황화물(thiophosphate) SE **6종**, **3개의 결정도 클래스(class)** ×
조성으로 구성. 우리 LPSCl(Li₆PS₅Cl)과 같은 **황화물(sulfide)** 패밀리 — 따라서
LIB 논문들과 달리 σ_grain은 **직접 전사 가능**한 시스템이다. 단, ⚠ **본 논문에
single-crystal Li₆PS₅Cl 측정은 없다**(아래 PROVENANCE §0 참조).
> ⛔ **정정 2026-09-25 (SI)** — "6종" 은 **본문 그림**의 수다.  SI 까지 합치면 **10 시료**: 본문 6종 +
> **GC-Li₆PS₅Cl · µC-Li₆PS₅Cl · GC-Li₅.₅PS₄.₅Cl₁.₅ · µC-Li₅.₅PS₄.₅Cl₁.₅** (Fig. S1e,f · S2c,d; 목록은 Fig. S6/S7 캡션과 일치).
> "single-crystal 측정 없음" 은 **SI 에서도 그대로**다 — 10 시료 전부 분체 압분체이고 SI 텍스트에 "single crystal" 은 없다.

동반 데이터 파일:
- `docs/data/cronau2021_stack_pressure_ionic.csv` — Fig 2/3/4 디지타이즈 (TREND 전용, 근사).
- ⭐ **`litdb/figures/cronau2021_stack_pressure_ionic_conductivity/si_digitized.csv`** (2026-09-25, 정본 브랜치) —
  SI Fig. S1a–f · S2a–d **전 점**(870 행) 서브픽셀 판독 + S3·S4·S5 보조 판독.  **전부 `digitized`**.
  S1a–d · S2a–b 는 본문 Fig. 2a–f 와 **같은 데이터**(시각 대조로 점 위치 일치 — 292.03/389.30 계열 색만 다름)라 위 옛 CSV 의 Fig 2 눈대중 값을 대체한다.
- 기존 `docs/data/lpscl_electrolyte_params.md` 의 "exact single-crystal digit NOT verified
  (proxy)" 플래그를 본 digest가 **해소**한다 (→ §0 / §8).

---

## ★★★ §0. PROVENANCE 판정 (미션 핵심) — 가장 먼저 읽을 것 ★★★

> ⛔⛔ **정정 2026-09-25 (SI 정독) — 판정 (A) 를 이렇게 바꾼다** (근거 §S, 값은 전부 digitized):
>
> | 질문 | 옛 판정 (2026-07-28, 본문만) | **SI 반영 판정** |
> |---|---|---|
> | Li₆PS₅**Cl** 을 측정했나 | ✗ "Br 만" | ✅ **했다** — GC (Fig. S1e) · µC (Fig. S2c) · 그리고 Cl-rich Li₅.₅PS₄.₅Cl₁.₅ (S1f · S2d) |
> | 3.0 mS/cm 이 있나 | ✗ "없다 (오귀속)" | 🔶 **숫자로는 없다** (SI 텍스트에 σ 숫자 0개) — 그러나 **Fig. S2c µC-Li₆PS₅Cl 이 적층압 ≥146 MPa 에서 2.88–3.46 mS/cm**, ≥195 MPa 에서 2.97–3.46 → **3.0 은 그 평탄 범위의 하단** |
> | 단결정인가 | ✗ | ✗ **그대로** — 볼밀 → 550 °C 어닐 → 재분쇄한 **µm 분체의 압분체**. 입계 포함 · 적층압 하 측정 |
> | 이 인용의 유형 | 유형 A "안 쟀다" | **유형 B "쟀는데 다른 양이다"** — 값은 맞아 보이지만 양이 **펠릿·고적층압 σ** 다 (`comparison_vs_ours.md` §I 규율) |
>
> ⇒ 한 줄: **"Cronau 2021 → LPSCl ≈ 3 mS/cm" 은 성립한다 — 단 "µC-Li₆PS₅Cl 펠릿, 적층압 ≥ 150 MPa 평탄의 하단" 으로서.**
> "단결정 grain-interior" 라벨은 틀렸고, 그 라벨 위에 세운 추론(예: *"펠릿 1.0–2.0 < Cronau 단결정 3.0 = 입계 서열"*)은 전제를 잃는다 (§9-6).

우리 σ_ionic 생산식(Stage-E, T1)은 이 논문을 **두 군데**에서 근거로 든다:
`σ_grain = 3.0 mS/cm` ("Cronau 단결정 LPSCl") 와 `Cronau(r_SE)` sub-µm 3-시그모이드.
본 PDF를 전수 정독한 결과, 두 귀속 모두 **부분적으로 부정확**하다. 정직한 판정:

### (A) σ_grain = 3.0 mS/cm 의 출처 판정 → **이 논문에 그 숫자는 없다 (오귀속/연도 오기)** — ⛔ 2026-09-25 정정: SI Fig. S2c µC-Li₆PS₅Cl 평탄의 하단 (유형 B, 아래 표 정정 행)

| 질문 | 판정 |
|---|---|
| 3.0 mS/cm 이 본문/그림/표에 **직접** 나오는가? | ✗ **아니오.** "3.0 mS/cm" 라는 숫자는 본 논문 어디에도 없다. |
| ⛔ **정정 2026-09-25 (SI)** | **텍스트 숫자로는 여전히 없다** (SI 텍스트에도 σ 숫자가 하나도 없다). 그러나 **그림에는 있다**: SI **Fig. S2c µC-Li₆PS₅Cl** 의 적층압 ≥146 MPa 점 16개가 **2.88–3.46 mS/cm** (digitized, 판독 ±0.01; ≥195 MPa 13점의 중앙값 3.17, 3.0 미만은 2점뿐), 저자 자신의 신뢰조건(Table S1: 제작압 ≥400 · µC 적층압 ≥250)을 만족하는 유일한 곡선(제작압 486.73 MPa, 적층압 292–487)이 **3.06–3.23**. ⇒ 3.0 은 **이 평탄의 하단**이다 (§S-5). |
| **single-crystal Li₆PS₅Cl** 을 측정했는가? | ✗ **아니오.** 본 논문은 **단결정을 측정한 적이 없다.** 6종 모두 **분체-압분체(powder pellet)** — amorphous / glass-ceramic / **micro**crystalline. "single crystal" 이라는 단어는 논문에 **등장하지 않는다.** |
| ✅ **유지 2026-09-25 (SI 포함)** | SI 에도 단결정은 없다 — 10 시료 전부 압분체이고, µC 는 볼밀 → 펠릿으로 눌러 550 °C 10 h → **재분쇄**한 분체다 (SI §1b). "single crystal" 단어도 SI 에 없다. |
| Li₆PS₅**Cl** 자체를 측정했는가? | ✗ **아니오.** Cl-argyrodite는 **intro 인용**(ref 4 Feng, ref 13)으로만 언급. 측정한 argyrodite는 **Li₆PS₅Br** (Br!) 이다. 측정 6종: AM-Li₇P₃S₁₁, AM-80Li₂S·20P₂S₅, GC-Li₇P₃S₁₁, **GC-Li₆PS₅Br**, **µC-Li₆PS₅Br**, µC-Li₁₀GeP₂S₁₂. |
| ⛔ **정정 2026-09-25 (SI)** | ✅ **예 — 측정했다.** SI **Fig. S1e GC-Li₆PS₅Cl** · **Fig. S2c µC-Li₆PS₅Cl** (각 제작압 5단 × 적층압 ~0–490 MPa), 더해 **Li₅.₅PS₄.₅Cl₁.₅** GC/µC (S1f · S2d), 밀도(S3) · XRD(S6e,f) · SEM(S7e,f). 합성은 Br 과 **같은 절차**(Li₂S·P₂S₅·LiCl, 850 rpm 8.5 h). 옛 판정은 **본문 그림만** 보고 내렸다 (이 카드 §2 표가 이미 "µC-Li₆PS₅Cl(준비됨)" 이라 적어 **스스로 모순**이었다). |
| 연도 "Cronau **2022**" (우리 코드/baseline) 가 맞는가? | ✗ **틀림.** PDF 명시 = **2021** (Received 2021-06-23, ACS Energy Lett. 2021, 6, 3072). 우리 docs의 "Cronau 2022"는 **본 2021 논문의 연도 오기**이다 (별도 Cronau 논문이 아님 — DOI 1c01299 동일). |

> ⛔ **정정 2026-09-25** (stoic-knuth 원장 `SELF-51`) — 위 행의 *"Cronau 2022 = 이 2021 논문의 연도 오기 (별도 논문이 아님)"* 판정은 **틀렸다**.  별도 논문이 실재한다: M. Cronau, M. Duchardt, M. Szabo, B. Roling, *Ionic Conductivity versus Particle Size of Ball-Milled Sulfide-Based Solid Electrolytes: Strategy Towards Optimized Composite Cathode Performance in All-Solid-State Batteries*, **Batteries & Supercaps 5 (2022) e202200041** (DOI 10.1002/batt.202200041 — 서지는 출판사 페이지 제목·검색으로 확인, **원문 미확인**; 초록상 대상은 습식 볼밀링한 **Li₅.₅PS₄.₅Cl₁.₅**).  stoic-knuth 코드가 2026-04-30 (`ceee1d812`) 에 입자 크기 보정 계수의 출처로 붙인 *"Cronau 2022"* 는 이 논문을 가리킨 것으로 보인다.
> ⇒ **이 카드의 나머지 판정은 그대로다** — 이 2021 논문에 3.0 mS/cm 은 없고, 단결정 측정도 없고, 측정한 argyrodite 는 Li₆PS₅Br 다.  달라지는 것은 "2022 는 오기" 한 줄뿐이다: 어느 문서가 DOI `1c01299` 를 'Cronau 2022' 에 붙였다면 **그 DOI 표기**가 틀린 것이고, 크기 보정 계수값이 Cronau 2022 원문에 있는지는 **PDF 로 따로 확인해야 한다** (Li₆PS₅Cl 이 아니라 Li₅.₅PS₄.₅Cl₁.₅ 연구).
>
> ⛔ **정정 2026-09-25 (같은 날, SI 정독)** — 위 블록은 **유지**한다 (연도 판정 철회 자체는 옳다).  그러나 그 둘째 문단의
> *"나머지 판정은 그대로다 — … 3.0 mS/cm 은 없고 … 측정한 argyrodite 는 Li₆PS₅Br 다"* 는 **본문만 보고 한 확인**이었다.
> SI 로 두 조각이 뒤집힌다: **Li₆PS₅Cl 은 측정됐고**(Fig. S1e · S2c), **µC-Li₆PS₅Cl 고적층압 평탄이 ≈2.9–3.5 mS/cm**(digitized)다.
> 남는 것은 *"단결정 측정 없음"* 과 *"2022 는 별도 논문"* 둘이다.  ⚠ 덧붙여 Cronau **2022** (Li₅.₅PS₄.₅Cl₁.₅ 볼밀 입도 연구)
> 는 **같은 그룹(Roling)이 같은 조성을 다룬 이듬해 논문**이고, 이 2021 SI 에 그 조성의 GC/µC 데이터(S1f · S2d)가
> 이미 있다 — 두 논문의 관계(같은 시료인지 등)는 2022 원문이 미확인이라 **판단 보류**.
>
> ⓘ **갱신 2026-09-25 (같은 날 늦게)** — 2022 원문은 정본 카드 [`cronau2022_wet_milling_particle_size_ionic_conductivity`](cronau2022_wet_milling_particle_size_ionic_conductivity.md)
> 로 **정독됐다** (다른 세션): 측정 재료는 Li₅.₅PS₄.₅Cl₁.₅ 뿐 · Li₆PS₅Cl·단결정 측정 0 · *"about 3 mS/cm"* 은 서론 p.1 의 **무인용** 문장.
> ★ 두 논문의 판독이 **같은 조건에서 맞는다**: 그 카드가 읽은 µc-LPSC+ 무처리 **≈3.97 mS/cm** (394 MPa 제작 · 98 MPa 적층, digitized) ↔
> 이 SI **Fig. S2d µC-Li₅.₅PS₄.₅Cl₁.₅** 389.30 MPa 제작 · ~97 MPa 적층 **3.97** (digitized) — 서로 다른 판독기·다른 논문의 교차 확인.
> (gc 는 2.50 (2022, stated) ↔ 1.97 (S1f) 로 안 맞는다 — 두 해의 gc 합성 대조는 미실행.)  그리고 2022 의 무인용 *"about 3"* 은
> 같은 그룹의 이 2021 SI 수치(µC-Li₆PS₅Cl ≈2.9–3.5)와 **맞는다** — 단 그 연결은 **우리 추정**이다 (2022 가 2021 SI 를 인용하지 않는다).
> ⚠ 그 카드 §0·참고문헌표는 이 2021 카드의 **SI 이전 판정**("3.0 mS/cm 없음")을 인용하고 있다 → 그 줄들은 이 정정을 따라가야 한다 (미수정).


**그렇다면 3.0 mS/cm 의 진짜 출처는?** 본 논문이 측정한 값들 중 우리 LPSCl에 가장
가까운 µC-Li₆PS₅Br (Br-argyrodite, 미세결정) 의 **고압-plateau σ ≈ 2.0–2.4 mS/cm**
(Fig 2e, 486 MPa 제작 + 고 stack pressure)이다. 즉 **3.0 은 "이 논문이 준 단결정
값"이 아니라, 이 논문의 미세결정 Br-argyrodite plateau(~2.4) 와 다른 LPSCl 문헌
(예: cold-press 1–3, 소결 3–6 mS/cm; `lpscl_electrolyte_params.md`)을 종합한
프로젝트 채택값**이다. 본 논문은 그 **상한 근거(미세결정도 고압에서 ~2.4까지 도달)**
는 제공하지만, "3.0 single-crystal" 이라는 **정밀 라벨은 지지하지 않는다.**

> ⛔ **정정 2026-09-25 (SI)** — 위 문단의 *"3.0 은 이 논문이 준 값이 아니라 … Br plateau(~2.4) 와 다른 LPSCl 문헌을
> 종합한 프로젝트 채택값"* 은 **틀렸다.**  이 논문의 SI 가 **같은 Cl 조성**으로 직접 준다:
> **Fig. S2c µC-Li₆PS₅Cl 고적층압 평탄 2.88–3.46 mS/cm** (≥146 MPa, digitized), 가장 가까운 대응점은
> "적층압 = 제작압" 끝점 **3.04 (292 MPa) · 3.39 (389) · 3.06 (487)** (§S-5).  Br 에서 Cl 로 외삽할 필요가 없다.
> ⇒ 3.0 은 **"Cronau 2021 SI Fig. S2c 의 하단"** 으로 추적된다.  마지막 문장(*"'3.0 single-crystal' 정밀 라벨은
> 지지하지 않는다"*)만 **그대로 참**이다.

> **재귀속 권고:** 코드 주석 `σ_grain = 3.0 mS/cm "Cronau 2022 Li6PS5Cl single-crystal"`
> →  `σ_grain = 3.0 mS/cm — LPSCl grain-interior 프로젝트 채택값. 근거: Cronau **2021**
> (µC-Li₆PS₅**Br** 고압 plateau ~2.0–2.4 mS/cm, 본 논문) + cold-press/소결 LPSCl 문헌
> 1–6 mS/cm 종합. ⚠ single-crystal LPSCl 직접측정 아님.`
> 이는 `lpscl_electrolyte_params.md`가 이미 단 플래그("exact single-crystal digit
> NOT verified (proxy)")를 **확정**해준다 — 본 정독으로 그 플래그는 "확인됨: 단결정값
> 아님" 으로 닫힌다.
>
> ⛔ **정정 2026-09-25 (SI) — 재귀속 권고 문구를 바꾼다:**
> `σ_grain = 3.0 mS/cm — Cronau 2021 (ACS Energy Lett. 6, 3072) SI Fig. S2c: µC-Li₆PS₅Cl 압분체, 적층압 ≥150 MPa
> 평탄 ≈2.9–3.5 mS/cm (digitized) 의 하단.  ⚠ 단결정·grain-interior 아님 = 입계·잔류기공 포함 펠릿을 적층압 하에서 잰 값.
> ⚠ 같은 시료가 적층압 ~50 MPa 에서는 ≈1.7–2.4 (§S-5).`
> "grain-interior" 라는 낱말을 **빼는 것**이 핵심이다 — 우리 STEP3 가 이 값을 "계면항 없는 결정 내부 σ" 로 쓰는 해석
> (stoic-knuth CLAUDE.md §CL-81 의 문장)이 이 라벨에 기대고 있다 (§9-6).

### (B) Cronau(r_SE) sub-µm 크기 인자의 출처 판정 → **(c) 느슨함 / 재명명 필요 (measured 아님, defensible-하지만-class-기반)**

논제에서 요구한 a/b/c 중 답:

| 옵션 | 판정 |
|---|---|
| (a) sub-µm 입자반경 → σ 감소가 본 논문에 **직접 측정**되어 있다 | ✗ **아님.** 본 논문은 **입자 반경(particle radius) r 의 함수로 σ 를 측정하지 않았다.** σ 의 독립변수는 **(i) stack pressure, (ii) fabrication pressure, (iii) 결정도 클래스(AM/GC/µC)** 뿐이다. r_SE → σ 곡선·표·breakpoint(0.03/0.1/0.3/0.5 µm)는 **논문에 존재하지 않는다.** |
| (b) 결정도/GB 논증의 **방어 가능한 외삽**이다 | △ **부분적.** 본 논문의 핵심 메커니즘 — "µC 입자는 서로 **소결(sinter)되지 않아** grain 사이에 gap/pore가 남고, 이것이 σ 를 낮춘다; pressure가 그 gap을 닫아야 한다" — 은 "미세결정성 → grain contact 불량 → σ 감소" 라는 **방향성**을 강하게 지지한다. 우리 인자가 "미세결정 → σ↓" **부호**를 옳게 잡은 점은 이 논문이 뒷받침한다. **그러나 그것은 입자크기 r 의 연속함수가 아니라 결정도 클래스의 이산(discrete) 효과**이다. |
| (c) 느슨하게 귀속됨 | ✅ **이것이 가장 정직한 판정.** 3-시그모이드의 **구체적 breakpoint(0.5/0.3/0.1/0.03 µm)와 plateau(1.0/0.90/0.65/0.33)** 는 본 논문에서 **측정·도출된 적이 없다.** 이 값들은 (아마도) 다른 출처 또는 프로젝트 경험에서 왔고, 본 논문은 그 **정성적 방향(미세결정·sub-µm → σ↓)** 만 보증한다. |

> **재명명 권고:** `Cronau(r_SE)` 인자의 물리적 의미를 **"입자크기 σ_grain 감쇠"**가
> 아니라 **"결정도/grain-contact 효율 인자"**로 재명명하라. 본 논문의 메커니즘은
> _입자가 작아서_ σ 가 낮은 게 아니라, _미세결정이 소결 안 되어 grain-boundary contact가
> 나빠서_ σ 가 낮은 것이다 (amorphous/GC는 가압-소결되어 이 문제가 없다). breakpoint
> 수치(0.5/0.3/0.1/0.03 µm)는 "Cronau가 측정" 이 아니라 **"미세결정-GB 논증을 따른
> 경험적 sub-µm 외삽"** 으로 정직하게 표기. (Trevisanello digest가 σ_S/σ_P 오귀속을
> 잡아낸 것과 동일한 정밀도.)
>
> **단, 인자를 폐기할 필요는 없다.** 부호와 정성적 메커니즘은 이 논문이 강하게 지지하고,
> LOOCV +0.0043 의 실측 개선도 있으므로 — **유지하되 라벨/근거만 정직화**하면 된다.

### (C) 한 줄 요약
- **연도:** 2021 (우리 "2022"는 오기, 같은 DOI).  ⛔ 정정 2026-09-25: *"2022 는 오기"* 는 틀렸다 — 별도 Cronau 2022 (Batteries & Supercaps, Li₅.₅PS₄.₅Cl₁.₅) 가 실재한다 (§(A) 정정 참조).
- **σ_grain=3.0:** single-crystal LPSCl 직접값 **아님**. 본 논문 µC-Li₆PS₅Br plateau(~2.4) + 타 LPSCl 문헌(1–6) 종합 채택값. 사용 자체는 합리적, **라벨만 부정확**.
  ⛔ 정정 2026-09-25 (SI): *"Br plateau + 타 문헌 종합"* 이 아니다 — **SI Fig. S2c µC-Li₆PS₅Cl 펠릿의 고적층압 평탄 ≈2.9–3.5 mS/cm (digitized) 하단**이 직접 근거다. "단결정 아님 · 라벨만 부정확" 은 그대로 참.
- **Cronau(r_SE):** sub-µm 반경 법칙은 본 논문에 **없음**. 본 논문은 **결정도-클래스·압력** 효과. 인자의 **방향(미세결정→σ↓)은 지지**, **breakpoint 수치는 미지지** → **(c) 느슨, 재명명 권고.**

---

## 1. 동기 / 핵심 질문 (Intro)

ASSB가 LIB 대비 (i) Li-metal 음극으로 부피에너지밀도 ~70 %↑, (ii) 불연성 SE로
화재위험↓ 의 두 이유로 유망. 황화물 SE는 합성 쉽고 액체전해질에 필적하는 Li⁺ σ 를
내는 가장 유망한 클래스. 본 Viewpoint가 던지는 질문:

> **"보고된 σ_ion 값을 어떻게 믿을 것인가?"** 같은 소재라도 **(1) 펠릿 제작 시 압력
> (fabrication pressure) 과 (2) σ 측정 시 셀에 가하는 압력 (stack pressure) 에 따라
> σ 가 크게 달라진다.** 특히 **비-어닐링(non-annealed) 시료**에서 문헌값 산포가 극심하다.**

핵심 동기 사실 (intro에서 인용):
- **Tatsumisago et al. (ref 21):** amorphous 75Li₂S·25P₂S₅ 는 **fabrication pressure**
  를 높이면(펠릿 압축) σ 가 크게 증가.
- **Meng et al. (ref 22, Doux 2020):** crystalline Li₆PS₅Cl 는 **fabrication pressure
  AND stack pressure** 둘 다 높이면 σ 가 유의하게 증가.
- ★ **Round-robin (ref 23, Ohno/Zeier 2020 interlab study):** **같은 합성 배치**의
  같은 소재를 **8개 연구실**이 각자의 프로토콜로 측정 → σ 산포가 **약 1 order of
  magnitude (10배)**. (→ 우리 σ_ionic 포락선 ~0.03–0.14 mS/cm 의 lab-간 허용오차
  논증과 직결, §6.)

**연구 갭:** 위 선행연구들은 amorphous **또는** crystalline 한쪽에 집중. 본 논문은
**amorphous (AM) / glass-ceramic (GC) / microcrystalline (µC)** 세 클래스를
**fabrication pressure × stack pressure** 평면에서 **체계적·동시** 비교한 최초.

**다루는 4개 황화물 sub-class (intro):**
1. LGPS형 결정질 Li₁₀MP₂S₁₂ (M=Ge,Sn)
2. argyrodite형 결정질 Li₆₋ₓPS₅₋ₓCl₁₊ₓ ← (우리 시스템 패밀리; 단 **본 논문 측정은 Br**)
   ⛔ 정정 2026-09-25 (SI): 본문 **그림**은 Br 뿐이지만 SI 가 **x = 0 (Li₆PS₅Cl) 과 x = 0.5 (Li₅.₅PS₄.₅Cl₁.₅)** 를 GC·µC 둘 다 쟀다 (Fig. S1e,f · S2c,d).
3. glass-ceramic, 예: Li₇P₃S₁₁
4. amorphous Li₂S–P₂S₅, Li₂S–P₂S₅–LiI

---

## 2. 측정 소재 6종과 클래스 정의 (Methods)

ball-milling 으로 제작. 합성 직후(as-prepared) 상태에 따라 클래스가 갈린다:

| 클래스 | 정의 (논문) | 본 논문 측정 소재 |
|---|---|---|
| **AM (amorphous)** | 합성 직후 대부분 **비정질**. | AM-Li₇P₃S₁₁, AM-80Li₂S·20P₂S₅ |
| **GC (glass-ceramic)** | 비정질 매트릭스 + **nanocrystallite** 부분결정화. Li₇P₃S₁₁ 은 ~260 °C **저온 어닐링**으로 AM→GC 전환. | GC-Li₇P₃S₁₁, GC-Li₆PS₅Br |
| **µC (microcrystalline)** | **고온 어닐링(~550 °C)** 으로 고결정화 → **micron-크기 결정립**. | µC-Li₁₀GeP₂S₁₂, µC-Li₆PS₅Cl(준비됨), µC-Li₆PS₅Br, µC-Li₅.₅PS₄.₅Cl₁.₅ |

> ⛔ **보강 2026-09-25 (SI §1–2, 상세 §S-2·S-3)** — ① GC 행에 **GC-Li₆PS₅Cl · GC-Li₅.₅PS₄.₅Cl₁.₅** 가 빠져 있다 (SI Fig. S1e,f).
> ② µC 행의 "µC-Li₆PS₅Cl(준비됨)" 은 **준비만 된 게 아니라 σ-vs-적층압을 잰 시료**다 (Fig. S2c).
> ③ 아지로다이트의 **"GC" = 볼밀만 한 분체** (850 rpm 8.5 h → 막자사발; 열처리 없음) — SI 스스로 이 물질을 그림마다
> **GC(S1d) · AM(S3 범례) · BMO(S4 범례 — 약어 정의 없음, "ball-milled only" 는 우리 추정)** 세 이름으로 부른다
> (S4 캡션은 같은 파란 점을 "GC-Li₆PS₅Br" 라 적어 GC = BMO 임은 확인된다).  Li₇P₃S₁₁ 의 GC 전환 온도는
> **240–260 °C · 2 h**.  ④ µC = GC 분체를 펠릿으로 눌러 **550 °C 10 h → 재분쇄** (LGPS 는 석영앰플 **500 °C 36 h**).
> "소결 펠릿"(Fig. 4d)은 µC 분체를 다시 눌러 **550 °C 10 h** 한 뒤 Au 스퍼터.

★ 본 논문 결과의 **중심 대비**는 **{AM, GC} (비정질상 함유) vs µC (완전결정·micron-grain)**.
- AM·GC: 비정질 입자가 fabrication pressure로 **소결(sinter)·치밀화** → grain 사이 결합.
- µC: micron 결정립이 **소결되지 않음**(서로 안 붙음) → grain 사이 gap/pore 잔존.

**측정 셋업 (Methods):**
- SE 펠릿을 두 **tungsten-carbide(WC) 전극** 사이에 끼움. 펠릿 면에 metal film(미스퍼터)
  또는 sputtered metal. **최대 ~500 MPa** stack pressure 인가.
- 대안: 펠릿 면에 metal film을 **sputter** 한 뒤 전용 셀에서 **낮은 stack pressure
  (~10 MPa)** 로 측정 (전극접촉 확보됨).
- σ 는 **stack pressure 의 함수**로 plot (각 fabrication pressure 별 곡선).
- ⛔ **보강 2026-09-25 (SI §2a,b — 상세 §S-3)**: 가압 측정 = **CompreCell + CompreDrive (rhd instruments)** — 제작압 120 s →
  **5 분에 걸쳐 0 으로 제거** → 적층압을 걸고 **120 s 대기 후** EIS (Autolab PGSTAT302N) → **측정이 끝난 뒤** 마이크로미터로
  두께.  저압 측정 = ⌀6 mm 펠릿(유압 프레스 **10 min**) + Au 스퍼터 + 밀폐셀, Novocontrol Alpha-AK **1 MHz–0.1 Hz ·
  −120…25 °C · 10 mV**.  ★ 그림에서 읽히는 규약: **각 곡선은 적층압이 그 제작압에 닿으면 끝난다** (적층압 ≤ 제작압 —
  97.34 MPa 곡선은 ~97 MPa 에서 멈춘다; SI 본문엔 명시 없음, 그림 판독).

---

## 3. Figure 1 — 압력의존 형태(morphology) 모식도 (논문의 중심 그림)

논문 1쪽 우측. **fabrication pressure 가 µC vs AM/GC 입자에 미치는 형태변화** 만화.

| 구분 | High fabrication pressure 일 때 | High fabrication pressure 해제(release) 후 |
|---|---|---|
| **µC (microcrystalline)** | micron 결정립들이 압력으로 가까워지나 **서로 소결 안 됨** (boundary 유지). | 압력 해제 → 결정립 사이 **gap/pore 다시 벌어짐** → grain contact 손실. |
| **AM / GC (amorphous·glass-ceramic)** | 비정질 입자가 **pressure-induced sintering** → 입자끼리 융합·치밀화. | 소결은 **비가역(irreversible)** → 압력 해제해도 **치밀상태 유지**. |

**캡션 핵심 (그대로):** "while the particles in amorphous or glass ceramic materials
undergo a **pressure-induced sintering process**, the microcrystalline particles are
**only densified** by the fabrication pressure, **but not sintered together**. This
distinct morphology exerts a strong influence on the Li⁺ ion conductivity after
**release** of the fabrication pressure."

→ ★ **이것이 (B) Cronau(r_SE) 인자의 진짜 물리다:** µC(미세결정)의 낮은 effective σ 는
**"입자가 작아서"가 아니라 "소결 안 되어 grain-boundary contact가 나빠서"**다.
우리 인자가 "미세결정→σ↓" 부호를 옳게 잡은 근거가 바로 이 그림 — 단 **r 의 함수가
아니라 클래스(소결가능성)의 함수**라는 점이 핵심 차이.

---

## 4. Figure 2 — σ_ion vs Stack Pressure (6 패널, 핵심 데이터)

6개 소재 각각에 대해 **5개 fabrication pressure** (97.34 / 194.69 / 292.03 / 389.30 /
486.73 MPa) 별로 σ vs **stack pressure** (0–500 MPa) 곡선. 배경 색띠 = 거동 regime.

### 패널별 (a)–(f) — 디지타이즈 TREND 값 (★ 근사, 그림에서 읽음)

| 패널 | 소재 | 클래스 | y축 단위 | 고압-plateau σ (최고 fab.) | regime 띠 |
|---|---|---|---|---|---|
| (a) | Li₇P₃S₁₁ | AM | S/cm (×10⁻⁴) | ~2.0–2.5 ×10⁻⁴ S/cm = **~0.20–0.25 mS/cm** | red→green |
| (b) | 80Li₂S·20P₂S₅ | AM | S/cm (×10⁻⁴) | ~6 ×10⁻⁴ S/cm = **~0.6 mS/cm** | red→green |
| (c) | Li₇P₃S₁₁ | GC | **mS/cm** (×10⁻³ 표기) | ~2.0–2.5 ×10⁻³ S/cm = **~2.0–2.5 mS/cm** | red→green |
| (d) | Li₆PS₅Br | GC | S/cm (×10⁻⁴) | ~8–9 ×10⁻⁴ S/cm = **~0.8–0.9 mS/cm** | red→green |
| (e) | **Li₆PS₅Br** | **µC** | S/cm (×10⁻³) | ~2.0–2.4 ×10⁻³ S/cm = **~2.0–2.4 mS/cm** ★ | red→**yellow**→green |
| (f) | Li₁₀GeP₂S₁₂ | µC | S/cm (×10⁻³) | ~5–6 ×10⁻³ S/cm = **~5–6 mS/cm** | red→**yellow**→green |

> ⚠ y축 prefactor 가 패널마다 다르다(×10⁻⁴ vs ×10⁻³) — 절대 비교 시 주의. 위 값은
> 그림 눈금에서 읽은 **TREND 근사**이며 false precision 금지.

> ⛔ **보강·정정 2026-09-25 (SI 판독)** — SI **Fig. S1a–d · S2a–b** 는 이 Fig. 2a–f 와 **점 위치가 일치**한다 (시각 대조;
> 292.03/389.30 계열의 **색만** 다르다) ⇒ 같은 데이터로 보고 SI 쪽을 서브픽셀로 판독했다 (§S-11 방법).
> 적층압 ≥146 MPa 점의 제작압별 범위, **mS/cm, digitized** (97.34 열 = 그 곡선의 끝점, 적층압 ~97 MPa):
>
> | 패널 (SI) | 97.34 | 194.69 | 292.03 | 389.30 | 486.73 | 위 표 눈대중과 대조 |
> |---|---|---|---|---|---|---|
> | (a) AM-Li₇P₃S₁₁ (S1a) | 0.111 | 0.151–0.154 | 0.191–0.194 | 0.209–0.215 | 0.211–0.225 | ~0.20–0.25 ✓ |
> | (b) AM-80Li₂S·20P₂S₅ (S1b) | 0.328 | 0.433–0.434 | 0.508–0.514 | 0.541–0.559 | 0.543–0.584 | ~0.6 — 다소 높게 읽음 |
> | (c) GC-Li₇P₃S₁₁ (S1c) | 1.448 | 1.943 | 2.134–2.182 | 2.176–2.311 | 2.180–2.388 | ~2.0–2.5 ✓ |
> | (d) GC-Li₆PS₅Br (S1d) | 0.545 | 0.721–0.725 | 0.814–0.822 | 0.896–0.906 | **0.947–0.992** | ⛔ *"~0.8–0.9 (최고 fab.)"* 틀림 — 최고 제작압은 **0.95–0.99**; 0.8–0.9 는 292–389 MPa 곡선 |
> | (e) µC-Li₆PS₅Br (S2a) | 1.519 | 1.924–1.971 | 2.139–2.185 | 2.228–2.250 † | 2.183–2.290 | ~2.0–2.4 ✓ |
> | (f) µC-Li₁₀GeP₂S₁₂ (S2b) | 3.939 | 4.918–5.141 | 5.008–5.444 | 5.312–5.718 | 5.218–5.966 | ~5–6 ✓ |
>
> † 486.73 곡선에 대부분 가려 초승달만 보이는 점 (146 MPa 점은 완전히 가려져 없음) — 판독 ±0.02.
> ⛔ **(c) 의 y축 제목 "mS·cm⁻¹" 은 원본 오기다** (SI Fig. S1c 도 같다).  글자 그대로 읽으면 GC-Li₇P₃S₁₁ 이 ≈2.3 **µS**/cm 가
> 되어 같은 조성의 AM 판(0.21 mS/cm, 단위 S·cm⁻¹ 표기)보다 **100 배 낮아진다** — 저온 결정화로 σ 가 오른다는 본문 서사와
> 정반대라 오기로 판정, **S·cm⁻¹ 로 읽었다**.  본문 Fig. 3a,b 의 "mS·cm⁻¹" 도 같은 오기다 (§5 정정).

### 거동 regime (배경 색)의 의미 (본문)

- **red regime (저 stack pressure, ~0–30/50 MPa):** **모든** 소재에서 σ 가 stack
  pressure 와 함께 **급격히 상승**. 원인 = **펠릿/WC전극 접촉 불량** (전극접촉 인공물,
  소재 본질 아님). → 이 구간 σ 는 **신뢰 불가**.
- **green regime (AM·GC, stack pressure > 30–50 MPa):** σ 가 **거의 일정(plateau)** →
  전극접촉 충분 → **참(true bulk) σ 에 근접**. **stack pressure 무관.**
- ★ **yellow regime (µC만, ~50–200/250 MPa):** **두 번째** stack-pressure 의존 구간.
  σ 가 약하지만 **계속 상승** (green처럼 평평해지지 않음). 원인 = µC 결정립 사이의
  **gap/pore 를 닫으려면 추가 stack pressure 필요**. µC 는 ~200–250 MPa **이상**에서야
  비로소 plateau (green).

**핵심 대비 (본문):**
- **AM·GC:** stack pressure > ~50 MPa 면 σ plateau (stack-pressure 무관). **σ 는 주로
  fabrication pressure 에 의해 결정**(비가역 소결로 치밀도 고정).
- **µC:** stack pressure 의존성이 **훨씬 강함**(yellow regime). fabrication pressure
  의존성은 **훨씬 약함** (소결 안 되므로 fab.로 치밀화가 잘 안 됨).

---

## 5. Figure 3 — σ_ion vs Fabrication Pressure (GC vs µC 직접대비)

GC-Li₆PS₅Br (a) 와 µC-Li₆PS₅Br (b) 를 **fabrication pressure(0–500 MPa)** 축으로 plot,
**4개 stack pressure** (5 / 50 / 100 / 300 MPa) 별 곡선. (Fig 2와 축을 바꾼 cut.)

### (a) GC-Li₆PS₅Br
- stack pressure **5 MPa**(낮음): fabrication pressure 올려도 σ 가 오히려 **감소**처럼
  보임 — 본문 설명: 저 stack pressure 에서는 전극접촉 불량이 지배 → **비재현 접촉의
  인공물**(σ 의 겉보기 감소는 실제 아님).
- stack pressure **≥ 50 MPa**: σ 가 **fabrication pressure 와 함께 명확히 상승**
  (~3×10⁻⁴ → ~9×10⁻⁴ mS/cm). 펠릿 **치밀화(densification)** + 비정질입자 **소결**로
  tortuosity↓·입자간 장벽↓. 400–500 MPa 에서 fab. 의존성이 약화(leveling, 밀도 포화).
  ⛔ **정정 2026-09-25** — 단위: Fig. 3 y축 제목의 **"mS·cm⁻¹" 은 원본 오기**(§4 정정)라 값은 **S/cm** 다.  그리고 적층압
  50 MPa 곡선은 ~3×10⁻⁴ 에서 시작하지 않는다 — 같은 데이터인 SI Fig. S1d 판독으로 **50 MPa: 0.53 → 0.91 mS/cm ·
  ~97 MPa: 0.55 → 0.98 mS/cm** (제작압 97 → 487 MPa, digitized).  *~3×10⁻⁴* 는 **5 MPa 곡선**의 저제작압 쪽 값이다
  (본문 Fig. 3a 네모: ≈3.7 · 3.2 ×10⁻⁴ S/cm @ 97 · 195 MPa 제작 — 눈대중).
- ★ σ 가 **stack pressure 5→50 MPa 에서 사실상 동일**(50 이상 plateau) = **GC 는
  stack-pressure 무관**(전극접촉만 확보되면).

### (b) µC-Li₆PS₅Br
- 모든 stack pressure 에서 fabrication pressure 의존성이 **GC 보다 훨씬 약함**(거의
  평탄) → micron 결정립이 fab. 압력으로 **소결되지 않으므로** 치밀화 효과가 작다.
- 대신 **stack pressure 가 곡선을 위로 평행이동** → µC 는 **stack-pressure 가 σ 의
  주 레버**(yellow regime 의 그림-3 표현).

→ ★ **(B) 인자의 핵심 증거:** **같은 조성(Li₆PS₅Br)**, 결정도만 다를 때(GC vs µC)
σ-압력 거동이 **질적으로 다르다.** GC(부분비정질)는 fab.로 소결·치밀 → 높고 안정한 σ;
µC(완전결정·소결불가)는 fab. 둔감·stack 민감 → 압력 해제시 grain gap 으로 σ 손실.
**"미세결정 = 페널티"** 는 입자크기가 아니라 **소결가능성(=비정질상 함유 여부)** 의 문제.

---

## 6. Figure 4 — FIB-SEM 단면 (메커니즘의 직접 시각증거 + ★ 절대 σ 숫자)

4개 대표 펠릿의 FIB 단면 SEM. **여기 캡션에 본 논문에서 가장 신뢰할 σ 절대값들이 명시됨**:
> ⓘ **정밀화 2026-09-25** — 네 값은 캡션 텍스트가 아니라 **그림 패널 안에 인쇄된 문구**(각 패널 아래 "Li⁺ conductivity: …")다.
> 명시값(stated)인 것은 같다.  원 데이터는 **SI Fig. S4a** (Au 스퍼터 · 적층압 ~10 MPa 의 σ vs 제작압) 이고, 판독으로
> 대조하면 0.15 → **0.145** · 0.65 → **0.654** · 2.40 → **2.45** (≤3 %, 로그축 1 px ≈ 1.7 %) 로 맞는다.
> ⚠ **(c) 0.59 만 안 맞는다** — S4a 의 같은 시료(µC 비어닐, ~387 MPa)는 **≈0.53** (6 px 차 = 판독 오차 아님).  SEM 을 찍은
> 펠릿이 S4a 의 펠릿과 다른지 SI 는 말하지 않는다 → 인용 시 **0.53–0.59** 로 폭을 적을 것.

| 패널 | 시료 | fabrication pressure | **Li⁺ σ (캡션 명시값)** | 형태 관찰 |
|---|---|---|---|---|
| (a) | GC-Li₆PS₅Br | **98 MPa** | **0.15 mS/cm** | 다공성·입자경계 보임 |
| (b) | GC-Li₆PS₅Br | **392 MPa** | **0.65 mS/cm** | **치밀화**, 비정질입자 **융합**·크기증가 (소결) |
| (c) | µC-Li₆PS₅Br (**펠릿어닐링 전**) | 392 MPa | **0.59 mS/cm** | micron 결정립 **개별 식별**, **서로 안 붙음(미소결)** |
| (d) | µC-Li₆PS₅Br (**550 °C 펠릿어닐링 후**) | 392 MPa | **2.40 mS/cm** ★ | 결정립 **소결됨** → σ **4×↑** |

**메커니즘 결론 (본문):**
- **GC (a)→(b):** fabrication pressure 98→392 MPa → 비정질입자 **pressure-induced
  sintering** → 입자 융합·크기↑ → 치밀화 → σ 0.15→0.65 mS/cm (**~4.3×**). 이 소결은
  **비가역** → 압력 해제 후에도 치밀상태·높은 σ 유지.
- **µC (c):** fabrication 392 MPa 로도 micron 결정립이 **소결 안 됨** (단면에서 결정립
  사이 경계 뚜렷). 원인 추정 = **결정립 간 격자방위 불일치(lattice misorientation)**
  로 소결 방해. → fab. 압력 해제시 **gap/pore 형성** → σ 측정 중 stack pressure 로 그
  gap 을 닫아줘야 함(yellow regime).
- **µC (d):** 펠릿을 **550 °C 추가 어닐링** → 결정립 **소결** → σ 0.59→**2.40 mS/cm**
  (**~4×↑**). = µC 도 **열처리하면** GC 수준 σ 도달 가능 (단 압력만으로는 불가).

★ **(A) σ_grain 출처 정밀화:** 본 논문의 **µC-Li₆PS₅Br 최고 σ = 2.40 mS/cm**
(어닐링 펠릿, Fig 4d) = 이 논문이 보고하는 LPSCl-친척(argyrodite)의 **최선 plateau**.
우리 채택 **3.0** 은 이보다 **약간 높고**(Br→Cl 차이 + 소결/단결정 외삽 + 타 문헌 1–6
종합), 따라서 "이 논문이 3.0 을 줬다"가 아니라 "이 논문이 **상한 ~2.4** 를 주고, 우리가
약간 위로 채택" 이 정확한 서술이다.

> ⛔ **정정 2026-09-25 (SI)** — 2.40 은 이 논문 아지로다이트의 **최선값이 아니다**.  같은 논문 SI 에:
> **µC-Li₆PS₅Cl 2.88–3.46** (S2c) · **µC-Li₅.₅PS₄.₅Cl₁.₅ 3.85–4.68** (S2d) · 소결 µC-Li₆PS₅Br 도 ~195 MPa 제작에서
> **2.68** (S4a) — 전부 mS/cm, digitized.  따라서 *"이 논문이 상한 ~2.4 를 주고 우리가 약간 위로 채택"* 은 틀렸고,
> 정확한 서술은 **"이 논문 SI 가 같은 Cl 조성의 펠릿 평탄 ≈2.9–3.5 를 주고, 우리 3.0 은 그 하단"** 이다.

---

## 7. Figure 5 — "신뢰할 수 있는 σ 측정" 프로토콜 (논문의 처방, 4 시나리오)

µC vs AM/GC 형태를 4개 압력시나리오로 만화화. **green hook(✓) = 신뢰값, red X(✗) =
비신뢰값.** "측정 프로토콜을 어떻게 짜야 참 bulk σ 에 가까운가"의 시각 가이드.

| 시나리오 | µC (미세결정) | AM/GC (비정질함유) |
|---|---|---|
| **Low fab. & low stack** | ✗ (gap 안닫힘 + 전극접촉 불량) | ✗ (치밀화 부족 + 전극접촉 불량) |
| **High fab. & high stack** | ✓ (gap 닫힘) | ✓ (소결·치밀 + 접촉확보) |
| **Low stack after high fab.** | ✗ (압력해제 → gap 다시 열림) | ✓ (소결 비가역 → 치밀 유지) ★ |
| **Annealed pellet under low stack** | ✓ (어닐링으로 결정립 소결됨) | ✓ |

★ 결정적 칸 = **"Low stack after high fabrication"**: AM/GC 는 ✓ (소결 비가역이라
저 stack 에서도 참값), µC 는 ✗ (소결 안 됐으니 압력 풀면 gap 재형성 → σ 손실).
이 한 칸이 µC 와 AM/GC 를 가르는 본질.

### 논문의 측정 프로토콜 처방 (본문 요약)

- **AM / GC:** fabrication pressure **400–500 MPa** 로 강하게 압축(비가역 치밀화 확보)
  → 그 뒤 σ 측정은 **낮은 stack pressure** 면 충분. metal sputter 전극이면 **5–10 MPa**,
  WC 직접접촉이면 **~30–50 MPa** 면 plateau(참값).
- **µC:** 압력만으론 소결 안 되므로 두 갈래:
  - (i) 펠릿 면 metal **sputter 없이**: σ 측정 중 **stack pressure 200–250 MPa 이상**
    필요(grain gap 강제로 닫기).
  - (ii) **펠릿 어닐링(550 °C) + metal sputter** 후: **5–10 MPa** 저 stack 으로 충분.
- **요지:** **고 fabrication pressure(400–500)는 필수**(치밀화), 그러나 **σ 측정 시
  stack pressure 는 — 비가역치밀이 됐다면 — 낮게**(전극접촉만). µC 는 어닐링 없이는
  이 "저 stack 신뢰값" 이 불가능.
- ⛔ **보강 2026-09-25 (SI Table S1, 전문 §S-4)** — 저자 자신의 표는 위 요약보다 **보수적**이다: 무스퍼터 AM/GC 최소 적층압 **100 MPa**
  (본문의 30–50 이 아니다), **µC 는 Au 스퍼터를 해도 250 MPa** (스퍼터는 전극 접촉만 고치고 펠릿 안 결정립 틈은 못 고친다), 소결 µC +
  스퍼터만 **5 MPa**.  전 행 **제작압 ≥400**.  ⚠ 표 1·2행의 표기는 "GC- or µC-SE" 인데 3·4행과 모순이라 **"AM- or GC-SE" 의 오기**로 읽었다.

### ASSB 적용 함의 (본문, 우리와 직결)

- 고에너지밀도엔 **Li-metal 음극** → 운전 stack pressure 를 **100 MPa 충분히 아래**로
  유지해야 함 (ref 25 Doux). → 그런데 **µC 는 저 stack 에서 σ 가 낮음**(gap) → **µC 는
  ASSB 운전조건에서 잠재력 발휘 못 함.** AM/GC 가 유리.
- 단 ASSB 내부 SE 입자는 **고온 어닐링 불가**(바인더·CAM 의 열안정성 한계) → µC 를
  ASSB 안에서 소결시킬 수 없음 → "µC 는 ASSB 에서 최대 σ 도달 어렵다"고 결론.

---

## 8. 핵심 숫자 총정리 (본 논문에서 실제로 측정/명시된 값만)

| 항목 | 값 | 출처(논문 위치) | digitized? |
|---|---|---|---|
| GC-Li₆PS₅Br σ @ 98 MPa fab. | **0.15 mS/cm** | Fig 4a 캡션 | 명시(stated) |
| GC-Li₆PS₅Br σ @ 392 MPa fab. | **0.65 mS/cm** | Fig 4b 캡션 | 명시 |
| µC-Li₆PS₅Br σ @ 392 fab., 어닐링 **전** | **0.59 mS/cm** | Fig 4c 캡션 | 명시 |
| µC-Li₆PS₅Br σ @ 392 fab., 550 °C **어닐링 후** | **2.40 mS/cm** ★ | Fig 4d 캡션 | 명시 |
| µC-Li₆PS₅Br plateau (고 fab., 고 stack) | ~2.0–2.4 mS/cm | Fig 2e | digitized(근사) |
| µC-Li₁₀GeP₂S₁₂ plateau | ~5–6 mS/cm | Fig 2f | digitized |
| GC-Li₇P₃S₁₁ plateau | ~2.0–2.5 mS/cm | Fig 2c | digitized |
| AM-80Li₂S·20P₂S₅ plateau | ~0.6 mS/cm | Fig 2b | digitized |
| AM-Li₇P₃S₁₁ plateau | ~0.2–0.25 mS/cm | Fig 2a | digitized |
| GC-Li₆PS₅Br plateau (Fig 2d) | ~0.8–0.9 mS/cm | Fig 2d | digitized |
| red→green 전이 (전극접촉 확보) | stack pressure **~30–50 MPa** | 본문/Fig 2 | 명시 |
| µC yellow regime 폭 | stack ~**50→200–250 MPa** | 본문/Fig 2e,f | 명시 |
| µC plateau 도달 stack pressure | **> 200–250 MPa** (어닐링 없을 때) | 본문 | 명시 |
| AM/GC 권장 fabrication pressure | **400–500 MPa** | 본문/Fig 5 | 명시 |
| AM/GC 권장 측정 stack (sputter 전극) | **5–10 MPa** | 본문 | 명시 |
| AM/GC 권장 측정 stack (WC 직접) | **~30–50 MPa** | 본문 | 명시 |
| 측정 fabrication pressure 세트 | 97.34 / 194.69 / 292.03 / 389.30 / 486.73 MPa | Fig 2 범례 | 명시 |
| inter-lab σ 산포 (round-robin, ref 23) | **~1 order of magnitude (10×)**, 8개 연구실 | intro | 명시(인용) |
| ★ **3.0 mS/cm** (우리 σ_grain) | **본 논문에 없음** | — | **오귀속** |
| ⛔ 정정 2026-09-25 (SI) — 3.0 | **SI 그림에 있다**: µC-Li₆PS₅Cl 적층압 ≥146 MPa **2.88–3.46** · Table S1 조건(제작 486.73 · 적층 ≥250) **3.06–3.23** · 적층압=제작압 끝점 **3.04 / 3.39 / 3.06** (292 / 389 / 487 MPa) ⇒ **3.0 = 평탄의 하단** | SI Fig. S2c | **digitized** |
| ★ **single-crystal LPSCl σ** | **본 논문에 없음** (단결정 미측정, Cl 미측정) | — | **오귀속** |
| ⛔ 정정 2026-09-25 (SI) — 단결정·Cl | 단결정은 **SI 에도 없다** (유지).  **"Cl 미측정" 은 틀림** — GC/µC-Li₆PS₅Cl · GC/µC-Li₅.₅PS₄.₅Cl₁.₅ 측정 | SI Fig. S1e,f · S2c,d | — |
| ★ **r_SE → σ sub-µm 법칙** | **본 논문에 없음** (압력·클래스만) | — | **미지지** |
| ✅ 유지 2026-09-25 (SI) — r_SE | SI 에도 **입도 변수는 없다** (Fig. S7 SEM 은 정성, PSD 수치 없음 = n/a) | SI Fig. S7 | — |
| **[SI] GC-Li₆PS₅Cl 평탄** (제작 194.69 / 292.03 / 389.30 / 486.73 MPa) | 0.70–0.71 / 0.75–0.76 / 0.89–0.91 / 0.99–1.05 mS/cm | SI Fig. S1e | digitized |
| **[SI] µC-Li₆PS₅Cl 평탄** (같은 순서) | 2.97 † / 2.88–3.04 / 3.26–3.46 / 2.94–3.23 mS/cm | SI Fig. S2c | digitized |
| **[SI] µC-Li₆PS₅Cl @ 적층압 ~49 / ~68 MPa** (제작 5단) | 1.70–2.43 / 2.02–2.60 mS/cm | SI Fig. S2c | digitized |
| **[SI] µC-Li₅.₅PS₄.₅Cl₁.₅ 평탄** (≥146 MPa) | 3.85–4.68 mS/cm | SI Fig. S2d | digitized |
| **[SI] GC-Li₅.₅PS₄.₅Cl₁.₅ 평탄** (≥146 MPa) | 1.54–2.25 mS/cm | SI Fig. S1f | digitized |
| **[SI] 소결 µC-Li₆PS₅Br** (Au 스퍼터, 적층 ~10 MPa) | 2.68 (~195 MPa 제작) · 2.45 (~387) mS/cm | SI Fig. S4a | digitized |
| **[SI] Ea** (Au, ~10 MPa): GC-Br / µC-Br 비어닐 / 소결 µC-Br | 0.339–0.354 / 0.317–0.340 / 0.285–0.310 eV | SI Fig. S4b | digitized |
| **[SI] 펠릿 밀도** µC-Li₆PS₅Cl (195 / 292 MPa) · GC-Li₆PS₅Cl (195→487) | 1.47 / 1.54 · 1.37 (195) → 1.46–1.50 (292–487) g/cm³ (절대밀도, 이론밀도 SI 에 없음) | SI Fig. S3 | digitized |
| **[SI] 가역 압축 무시 근거** | Young·bulk 탄성률 **20–35 GPa** (500 MPa 까지 가역압축 무시) | SI §2a, ref S4 (Deng 2016 JES) | stated (인용) |
| **[SI] 신뢰 측정 최소조건** | 제작압 **≥400** 전 행 · 적층압 5 / 100 / 250 MPa (Table S1 전문 §S-4) | SI Table S1 | stated |

† 194.69 MPa 제작 곡선은 적층압 ≥146 에서 **~195 MPa 1점만** 읽힌다 — 위에 그려진 292.03 점(초록)에 가려 아래 초승달만
보인다 (판독 ±0.02).  ~146 MPa 점은 292.03·486.73 점 뒤에 **완전히 가려져** 판독 불가.

---

## §S. Supporting Information 정독 (2026-09-25) — SI 10 pp · Fig. S1–S7 · Table S1

> 원본 `nz1c01299_si_001.pdf` (ACS SI, 10 쪽; Word 2019 → PDF, 2021-08-03).  텍스트 **전수 추출** + 그림 7장·표 1장을
> **렌더해 전부 육안 확인**.  SI 그림은 전부 **임베디드 래스터**(~200 dpi; S1·S5·S7 = JPEG, S2·S3·S4·S6 = 무손실) →
> 벡터 좌표가 없어 **픽셀 판독**만 가능하다.
> ⛔ **SI 텍스트에는 σ 숫자가 하나도 없다.**  이 절의 σ·밀도·Ea·임피던스 값은 **전부 digitized** (판독 방법·오차 §S-11).
> 명시값(stated)은 합성·측정 조건 · Table S1 · 탄성률 인용 · 그림 범례/축뿐이다.
> 표기 규약: 이 카드의 **`digitized` = 정본 CLAUDE.md 의 `figure-read ≈`** (그림에서만 읽은 값) — 여기선 눈대중이 아니라
> 축 보정 서브픽셀 판독이라 소수 둘째 자리까지 적었지만, **지위는 똑같이 "그림에서 읽은 값"** 이다.

### S-0. SI 가 이 카드를 어떻게 바꾸나 — 세 줄

1. **Li₆PS₅Cl 은 측정됐다** — GC (Fig. S1e) · µC (Fig. S2c), 더해 Cl-rich **Li₅.₅PS₄.₅Cl₁.₅** GC/µC (S1f · S2d).
   ⇒ §0 (A) 의 *"Br 만 쟀다"* 철회.  시료는 본문 6 + SI 4 = **10 종**.
2. **µC-Li₆PS₅Cl 고적층압 평탄 ≈ 2.9–3.5 mS/cm** (≥146 MPa 16점 2.88–3.46) ⇒ 우리 **σ_grain 3.0 은 그 평탄의 하단**으로 추적된다.
   단 **펠릿**(입계·잔류기공 포함)을 **적층압 하에서** 잰 값이지 단결정이 아니다.  같은 펠릿이 적층압 ~50 MPa 에선 1.7–2.4.
3. **같은 실험실·같은 절차의 대조가 생겼다** — Li₆PS₅Cl 은 **µC 가 GC 의 ×3.1–4.0** (클래스 효과), µC 에서 **Cl₁.₅ > Cl > Br
   ≈ 2.0 : 1.4 : 1** (Br 기준).  ⇒ "우리 SE 가 어느 클래스인가" (§10-5) 가 σ_grain 을 **3–4 배** 흔드는 정량 질문이 됐다.

### S-1. SI 그림 세트 (Figure set)

| Fig | 무엇을 보이나 | 우리가 쓸 것 |
|---|---|---|
| S1 | AM/GC 6종 σ vs 적층압 (제작압 97.34–486.73 MPa 5단) — a AM-Li₇P₃S₁₁ · b AM-80Li₂S–20P₂S₅ · c GC-Li₇P₃S₁₁ · d GC-Li₆PS₅Br · **e GC-Li₆PS₅Cl** · f GC-Li₅.₅PS₄.₅Cl₁.₅.  배경 빨강(0–50 MPa, 전극접촉) → 초록 | e: **GC-LPSCl 평탄 0.70–1.05 mS/cm** = "우리 SE 가 GC 급이라면" 의 σ_grain 후보 · a–d 는 본문 Fig. 2a–d 와 같은 데이터 |
| S2 | µC 4종 σ vs 적층압 — a µC-Li₆PS₅Br · b µC-LGPS · **c µC-Li₆PS₅Cl** · d µC-Li₅.₅PS₄.₅Cl₁.₅.  노랑 띠 ~50–225 MPa = µC 전용 2차 적층압 의존 | ★ **c = σ_grain 3.0 의 출처** (평탄 2.9–3.5 의 하단) · 운전압 50–70 MPa 값 1.7–2.6 · a,b = 본문 Fig. 2e,f |
| S3 | 펠릿 **절대밀도**(g/cm³) vs 제작압, 10 시료 | 치밀화 추세 · "고제작압 leveling" (본문이 인용) — 이론밀도가 없어 **기공률 환산 불가** |
| S4 | Au 스퍼터 · 적층압 ~10 MPa: (a) σ vs 제작압 (로그축) (b) Ea vs 제작압 — GC-Br / µC-Br 비어닐 / **소결 µC-Br** | 본문 Fig. 4 표기값(0.15 / 0.65 / 0.59 / 2.40)의 원 데이터 · 소결 µC 의 Ea 가 셋 중 최저 |
| S5 | GC-Li₆PS₅Br EIS, **−80 °C**, 제작 97.34 vs 389.30 MPa (Nyquist, Ω·cm², 10⁵–10⁻¹ Hz) | 반원 끝 ≈3.9×10⁶ vs 0.9×10⁶ Ω·cm² → 제작압 효과 ≈4.4× (저온에서 분해해 읽음) |
| S6 | 분말 XRD 10 시료 (Cu Kα, Debye–Scherrer) | **클래스 정의의 근거**: GC = 넓은 아지로다이트 피크, µC = 날카로움 |
| S7 | 분말 SEM 10 시료 | 입도는 **정성뿐** (PSD 수치 없음 = n/a) |
| Table S1 | 신뢰 측정 최소조건 (제작압 · 스퍼터 여부 · 적층압) | 우리 계산·운전 조건이 **어느 칸**인가 (§S-4) |

### S-2. 합성 (SI §1 — 전 단계 Ar 분위기, stated)

| 시료 | 전구체 (공급사·순도) | 볼밀 | 후처리 | SI 문헌 |
|---|---|---|---|---|
| **µC-Li₁₀GeP₂S₁₂** | Li₂S (Sigma 99.9 %) · P₂S₅ (Sigma 99 %) · GeS₂ (순도 미기재) | **500 rpm · 22 h**, ZrO₂ 볼 ⌀10 mm | 석영앰플 밀봉 **500 °C 36 h** → 상온 → 재분쇄 | S1 (Wenzel 2016) |
| **GC 아지로다이트** Li₆PS₅Cl · Li₆PS₅Br · Li₅.₅PS₄.₅Cl₁.₅ | Li₂S (Alfa Aesar 99.9 %) · P₂S₅ (Sigma 99 %) · LiCl 또는 LiBr (Sigma 99.9 %) | **850 rpm · 8.5 h**, ZrO₂ 볼 | 막자사발 분쇄 → **GC** (열처리 없음) | S2 (Jung 2020) |
| **µC 아지로다이트** | 위 GC 분말 | — | 펠릿으로 눌러 유리앰플 밀봉 **550 °C 10 h** → **재분쇄** | S2 |
| **소결 펠릿** (Fig. 4d · S4 초록) | µC 분말 | — | 펠릿 압축 → **550 °C 10 h** → 양면 **Au 스퍼터** | — |
| **AM-Li₇P₃S₁₁** | Li₂S · P₂S₅ | **510 rpm · 60 h** | 재분쇄 | S3 (Xu 2017) |
| **GC-Li₇P₃S₁₁** | AM 과 동일 | 동일 | 펠릿 → 유리앰플 **240–260 °C 2 h** → 재분쇄 | S3 |
| **AM-80Li₂S–20P₂S₅** | Li₂S · P₂S₅ | **850 rpm · 8.25 h** | 분쇄 | — |

- ★ **할로겐 비교는 절차가 같다** — Cl · Br · Cl₁.₅ 가 같은 볼밀(850 rpm 8.5 h)·같은 어닐(550 °C 10 h)을 거친다 ⇒
  S2a/c/d 의 순위는 **조성 효과**로 읽어도 된다 (단 실험실 내부 대조 1세트, 반복수 미기재).
- ★ **µC 는 "어닐 후 재분쇄" 분말**이다 — 그 분말로 만든 펠릿은 **소결되지 않은** 압분체이고, 이것이 본문 Fig. 1 의
  "µC 는 치밀화만 되고 소결되지 않는다" 의 물질적 내용이다.  µm 결정립은 **어닐로부터의 추론**이지 측정값이 아니다 (S7 정성).
- ⚠ **표기 오기 (원문 그대로)**: §1d 제목 *"80 Li2 – 20 P2S5"* · Fig. S1 캡션 b) *"AM-80 Li2O – 20 P2S5"* — 패널 제목은 **Li₂S**.
  볼밀만 한 Li₆PS₅Br 이 **GC (S1d) · AM (S3 범례) · BMO (S4 범례)** 세 이름으로 불린다 (S4 캡션이 "GC" 라 적어 동일물 확인).
- **n/a (SI 에 없음)**: 볼:분말 비, 용기 재질·부피, 승온 속도, 입도 분포, 조성 분석(ICP 등).

### S-3. 측정법 (SI §2 — stated)

**(a) 가압 σ — 본문 Fig. 2 · 3 과 SI Fig. S1 · S2 의 출처.**
분말을 **CompreCell** (rhd instruments) 에 넣고 **CompreDrive** 로 **제작압 120 s** → **5 분에 걸쳐 0 으로 제거** →
적층압을 걸고 **120 s 대기** 후 EIS (**Autolab PGSTAT302N**) → **측정이 다 끝난 뒤** 마이크로미터(Mitutoyo)로 두께.
전극은 본문대로 WC (스퍼터 없음).
- ★ SI 의 한 문장: *"500 MPa 까지 가역 압축은 무시할 수 있다 — Young·bulk 탄성률이 **20–35 GPa** 이므로"* (ref S4, Deng 2016).
  ⇒ 모든 적층압에서 **측정 후 두께 하나**로 σ = L/(R·A) 를 낸다.  `derived(ours)`: ε ≈ P/K ≈ 0.5/25 ≈ **2 %**(부피) → 두께 오차
  ≲1–2 % 로, 관측된 2–4 배 σ 변화에 비해 작다 — 적층압 효과가 **기하 인공물이 아니라는** 저자 논리가 선다.
- ★ 같은 문장이 **우리 논리와 같다**: DPC cap 교차점검(stoic-knuth CLAUDE.md, 2026-06-09)의 *"LPSCl 은 bulk ~24 GPa ≫ 300 MPa
  라 입자 내부는 치밀화되지 않는다 → 치밀화는 재배열 + 등부피 형상변화"* 와 **같은 부등식**을 저자가 독립적으로 쓴다.
- ★ 그림 규약 (본문에 명시 없음, 판독): **각 곡선은 적층압이 자기 제작압에 닿으면 끝난다** (97.34 MPa 제작 곡선은 ~97 MPa 에서 멈춤)
  = 적층압이 펠릿을 **재압밀하지 않는 범위**만 잰다.
- **n/a**: CompreCell 셀 직경, EIS 주파수·진폭·온도, 등가회로, 반복수·오차막대.

**(b) 저압 σ — 본문 Fig. 4 와 SI Fig. S4 · S5 의 출처.**
⌀6 mm 펠릿을 유압 프레스(P/O/Weber) + 연마한 스테인리스 압출다이로 **상온 10 min** 성형 → 두께 측정 → 글러브박스 안 스퍼터
(Cressington 108auto)로 **양면 Au** → 밀폐 셀 → **Novocontrol Alpha-AK, 1 MHz–0.1 Hz, −120…25 °C, 10 mV**.
적층압은 "**~10 MPa 범위**" (S4 캡션).  온도 스캔이 S4b 의 Ea 를 준다.
- ⚠ 두 프로토콜은 **유지시간(120 s vs 10 min)·다이가 다르다** — S4a(저압)와 S1/S2(가압)를 같은 제작압끼리 직접 빼지 말 것.

**(c) XRD** — STOE StadiMP, Mythen 1K 검출기, Cu Kα₁ **1.54056 Å**, Debye–Scherrer, Ar 밀봉 유리모세관(Hilgenberg).
**(d) SEM** — Zeiss Gemini II + Ga-FIB 단면 (스퍼터 시료 = 본문 Fig. 4).  S7 메타데이터: EHT 2.00 kV · SE2 · 2021-03-19/20 (i 만 05-31).

### S-4. Table S1 — 전문 (원문 그대로)

*Table S1. Summary of favorable measurement conditions for obtaining reliable ionic conductivities.*

| Sample type | Minimum fabrication pressure / MPA [sic] | Sputtered sample faces | Minimum Stack pressure / MPa |
|---|---|---|---|
| GC- or µC-SE | 400 | No | 100 |
| GC- or µC-SE | 400 | Yes | 5 |
| µC-SE | 400 | No | 250 |
| µC-SE | 400 | Yes | 250 |
| µC-SE pellet annealed | 400 | Yes | 5 |

읽는 법 (우리 해석 — 저자 정오표 없음):
1. ⚠ **1·2행 "GC- or µC-SE" 는 3·4행과 모순이다** — 2행은 µC + 스퍼터 = 5 MPa, 4행은 µC + 스퍼터 = 250 MPa.  본문과 Fig. 5
   ("AM/GC 는 저적층압도 신뢰, µC 는 250 또는 어닐 필요")에 맞추면 1·2행은 **"AM- or GC-SE" 의 오기**로 읽힌다.
2. 1행(AM/GC · 무스퍼터) **100 MPa** 는 본문의 *"초록 regime > 30–50 MPa"* 보다 **보수적**이다.
3. **전 행이 제작압 ≥ 400 MPa** 를 요구한다 ⇒ 측정한 다섯 제작압 중 **486.73 MPa 곡선만** 해당 (389.30 < 400).
4. 4행 (µC + 스퍼터도 250) = 스퍼터 전극은 **전극 접촉**만 고치고 **µC 펠릿 내부의 결정립 틈**은 못 고친다 → 5행처럼 **펠릿 어닐**이 있어야 5 MPa.

⇒ **우리 칸**: 구조는 **300 MPa** 에서 계산 (제작압 < 400 → 저자 기준 "신뢰" 문턱 아래), 운전 적층압 **40–70 MPa** (µC 기준
250 의 한참 아래 = **노랑 띠**).  우리 SE 가 µC 같다면 운전 σ 는 평탄값이 아니다 (§9-6).

### S-5. ★ Fig. S2 (µC) — 디지타이즈 표

판독 오차: S2c 1 px = 0.0101 mS/cm → **±0.01**; † 가려진 점 ±0.02; * 같은 계열 이웃과 겹친 점 ±0.01–0.02 (10 MPa 간격이
마커 지름보다 좁다).  "—" = 그 제작압을 넘는 적층압은 측정하지 않음.  "n/r" = 완전히 가려져 판독 불가.

**Fig. S2c µC-Li₆PS₅Cl** (mS/cm, digitized)

| 제작압 \ 적층압 (MPa) | ~49 | ~68 | ~97 | ~146 | ~195 | ~243 | ~292 | ~389 | ~487 |
|---|---|---|---|---|---|---|---|---|---|
| 97.34 | 2.06 | 2.16* | 2.33 | — | — | — | — | — | — |
| 194.69 | 2.43 | 2.60 | 2.74 | n/r | 2.97† | — | — | — | — |
| 292.03 | 1.81 | 2.22 | 2.56 | 2.88 | 2.99 | 3.01 | 3.04 | — | — |
| 389.30 | 2.22 | 2.55 | 2.87 | 3.26 | 3.41 | 3.46 | 3.44 | 3.39 | — |
| 486.73 | 1.70 | 2.02 | 2.42 | 2.94 | 3.15 | 3.23 | 3.23 | 3.17 | 3.06 |

**Fig. S2a µC-Li₆PS₅Br** (mS/cm, digitized)

| 제작압 \ 적층압 (MPa) | ~49 | ~68 | ~97 | ~146 | ~195 | ~243 | ~292 | ~389 | ~487 |
|---|---|---|---|---|---|---|---|---|---|
| 97.34 | 1.36* | 1.44* | 1.52 | — | — | — | — | — | — |
| 194.69 | 1.65 | 1.75* | 1.84 | 1.92 | 1.97 | — | — | — | — |
| 292.03 | 1.82 | 1.94 | n/r | 2.14 | 2.18 | 2.18 | 2.19 | — | — |
| 389.30 | 1.75 | 1.92 | n/r | n/r | 2.23† | 2.25† | 2.24† | 2.23† | — |
| 486.73 | 1.70 | 1.89 | 2.04 | 2.18 | 2.24 | 2.27 | 2.26 | 2.24 | 2.29 |

**Fig. S2d µC-Li₅.₅PS₄.₅Cl₁.₅** (mS/cm, digitized)

| 제작압 \ 적층압 (MPa) | ~49 | ~68 | ~97 | ~146 | ~195 | ~243 | ~292 | ~389 | ~487 |
|---|---|---|---|---|---|---|---|---|---|
| 97.34 | 2.74* | 2.87* | 3.08 | — | — | — | — | — | — |
| 194.69 | n/r | 3.56 | 3.75† | 3.87 | 3.89 | — | — | — | — |
| 292.03 | 3.20 | 3.48* | 3.72 | 3.96 | 3.97 | 3.90 | 3.85 | — | — |
| 389.30 | 3.28 | 3.64 | 3.97 | 4.31 | 4.41 | 4.38 | 4.27 | 3.99 | — |
| 486.73 | 3.66 | 4.00 | 4.29 | 4.60 | 4.68 | 4.65 | 4.55 | 4.25 | 3.91 |

**Fig. S2b µC-Li₁₀GeP₂S₁₂** (mS/cm, digitized)

| 제작압 \ 적층압 (MPa) | ~49 | ~68 | ~97 | ~146 | ~195 | ~243 | ~292 | ~389 | ~487 |
|---|---|---|---|---|---|---|---|---|---|
| 97.34 | 3.36 | 3.64* | 3.94 | — | — | — | — | — | — |
| 194.69 | 3.91† | n/r | 4.51 | 4.92 | 5.14 | — | — | — | — |
| 292.03 | n/r | 4.21 | 4.59 | 5.01 | 5.25 | 5.37 | 5.44 | — | — |
| 389.30 | 4.18 | 4.55* | 4.93 | 5.31 | n/r | 5.65 | 5.72 | 5.71 | — |
| 486.73 | 3.86 | 4.29 | 4.72 | 5.22 | 5.52 | 5.72 | 5.84 | 5.97 | 5.93 |

**관찰 (S2)**
- **µC-Li₆PS₅Cl 평탄**: 적층압 ≥146 MPa 16점 **2.88–3.46**, ≥195 MPa 13점 **2.97–3.46** (중앙값 3.17; 3.0 미만 2점).
  Table S1 조건 곡선(486.73 · ≥250 MPa): **3.06–3.23**.  "적층압 = 제작압" 끝점: **3.04 (292) · 3.39 (389) · 3.06 (487)**.
- **노랑 띠의 크기** (µC-Li₆PS₅Cl, 49 → 146 MPa): 292.03 **+59 %** · 389.30 **+47 %** · 486.73 **+73 %** (`derived(ours)`).
  ⇒ 운전압 ~50 MPa 의 σ 는 자기 평탄의 **53–82 %** 다 (194.69 가 82 %, 486.73 이 53 %).
- **제작압 의존이 비단조이고, 저적층압에서 뒤집힌다** — ~49 MPa 에서 **194.69 (2.43) > 389.30 (2.22) > 97.34 (2.06) >
  292.03 (1.81) > 486.73 (1.70)**: 가장 세게 누른 펠릿이 **가장 낮다**.  평탄에서도 389.30 > 486.73 > 292.03.
  본문 Fig. 3b (µC-Br, 적층압 5 MPa) 의 "고제작압일수록 낮음" 과 같은 부호.  SI 는 이유를 **설명하지 않는다** (n/a).
- **고적층압 쇠퇴**: µC-Li₅.₅PS₄.₅Cl₁.₅ 486.73 곡선이 4.68 (~195) → **3.91 (~487)** = **−16 %** (µC 중 유일하게 뚜렷);
  µC-Li₆PS₅Cl −5 % (3.23 → 3.06); µC-Br 는 평탄(2.24–2.29); **LGPS 는 ~390 MPa 까지 계속 오른다** (5.22 → 5.97).
- **할로겐 순위** (486.73 제작, 적층압 195–292): **Cl₁.₅ 4.55–4.68 > Cl 3.15–3.23 > Br 2.24–2.27** (Br 기준 ≈2.0 : 1.4 : 1), LGPS 5.52–5.84.
- ★ **외부 교차 확인 (판독기 검증)**: 같은 그룹 2022 논문을 **다른 세션이 따로** 디지타이즈한 µc-Li₅.₅PS₄.₅Cl₁.₅ 무처리 σ ≈ **3.97**
  (394 MPa 제작 · 98 MPa 적층; [`cronau2022_…`](cronau2022_wet_milling_particle_size_ionic_conductivity.md) Fig. 2) ↔ 이 표 **S2d 389.30 · ~97 = 3.97**.
  조건이 거의 같은 두 논문·두 판독이 소수 둘째 자리까지 맞는다 — 이 절 판독의 절대 수준을 **외부에서** 받쳐 준다 (한 점, TREND 등급).

### S-6. Fig. S1 (AM/GC) — 디지타이즈 표

S1e 1 px = 0.0030 mS/cm → 판독 **±0.003** (JPEG 원본; 중심 불확실 ≤1 px).  a–d 는 §4 의 정정 표에 요약.

**Fig. S1e GC-Li₆PS₅Cl** (mS/cm, digitized)

| 제작압 \ 적층압 (MPa) | ~49 | ~68 | ~97 | ~146 | ~195 | ~243 | ~292 | ~389 | ~487 |
|---|---|---|---|---|---|---|---|---|---|
| 97.34 | 0.45* | 0.46* | 0.47 | — | — | — | — | — | — |
| 194.69 | 0.64* | 0.66* | 0.68 | 0.70 | 0.71 | — | — | — | — |
| 292.03 | 0.69 | 0.72* | 0.73 | 0.75 | 0.76 | 0.76 | 0.76 | — | — |
| 389.30 | n/r | 0.88* | 0.89 | 0.90 | 0.91 | 0.90 | 0.90 | 0.89 | — |
| 486.73 | 0.85 | 0.95 | 1.01 | 1.04 | 1.05 | 1.04 | 1.03 | 1.01 | 0.99 |

**Fig. S1f GC-Li₅.₅PS₄.₅Cl₁.₅** (mS/cm, digitized)

| 제작압 \ 적층압 (MPa) | ~49 | ~68 | ~97 | ~146 | ~195 | ~243 | ~292 | ~389 | ~487 |
|---|---|---|---|---|---|---|---|---|---|
| 97.34 | 1.07* | 1.14* | 1.19 | — | — | — | — | — | — |
| 194.69 | 1.37 | 1.44* | 1.49 | 1.54 | 1.55 | — | — | — | — |
| 292.03 | 1.64† | 1.73* | 1.78 | 1.83 | 1.84 | 1.82 | 1.79 | — | — |
| 389.30 | 1.68 | 1.87 | 1.97 | 2.06 | 2.08 | 2.07 | 2.04 | 1.97 | — |
| 486.73 | 1.61 | 1.94 | 2.14 | 2.24 | 2.25 | 2.23 | 2.20 | 2.13 | 2.03 |

**관찰 (S1)**
- AM/GC 는 **~50–100 MPa 에서 평탄**, 그리고 **모든 적층압에서 제작압과 단조** 증가 (µC 와 대조) — 본문 결론 그대로.
- **고적층압 쇠퇴가 전 패널에 있다** (486.73 곡선, 최고점 → 487 MPa): S1e **−5 %** · S1a −6 % · S1b −7 % · S1c −9 % · S1f −10 %.
  SI 무설명 (n/a).  단일 두께 규약(§S-3a)으로는 설명 안 되는 크기다 (가역 압축 ≲2 %).
- ★ **클래스 효과 (Li₆PS₅Cl, 같은 제작압·적층압 195–292)**: µC/GC = 2.99–3.04 / 0.76 ≈ **4.0** (292.03) · 3.41–3.46 / 0.90–0.91
  ≈ **3.8** (389.30) · 3.15–3.23 / 1.03–1.05 ≈ **3.1** (486.73) → **×3.1–4.0** (`derived(ours)`).
- **GC 할로겐 순위** (486.73): Cl₁.₅ 2.20–2.25 > **Cl 1.03–1.05 ≈ Br 0.98–0.99** — GC 에서는 Cl 과 Br 이 **≤7 %** 차.
- 우연한 수치 일치 하나: GC-Li₆PS₅Cl 486.73 평탄 **≈1.0** 과 Bazzoun 2026 의 LPSCl 펠릿 **1.02** (400 MPa) — 시료·장비·결정도가
  달라 **근거로 쓰지 말 것** (클래스를 가리키는 증거가 아니다).

### S-7. Fig. S3 — 펠릿 밀도 (g/cm³, digitized ±0.01; 겹친 마커는 분리 불가)

| 시료 | 97.34 | 194.69 | 292.03 | 389.30 | 486.73 |
|---|---|---|---|---|---|
| µC-Li₆PS₅Cl (■ 초록) | ≈1.35 (GC 원과 겹침) | 1.47 | 1.54 | 안 보임 | 안 보임 |
| GC-Li₆PS₅Cl (● 초록) | ≈1.35 | 1.37 | 1.46 | 1.50 | 1.47 |
| µC-Li₆PS₅Br (■ 주황) | ≈1.49 (겹침) | 1.68 | ≈1.74 (겹침) | 1.82 | 1.98 |
| µC-Li₅.₅PS₄.₅Cl₁.₅ (■ 보라) | 겹침 | 1.59 | 겹침 | 1.63 | 1.66 |

- **절대밀도**다 — 이론(결정)밀도가 SI 에 **없다** ⇒ 상대밀도·기공률 환산은 이 SI 만으로 **n/a** (다른 출처의 결정밀도를 끌어오면
  가능하지만 그건 우리 산수가 된다).  본문이 말하는 *"고제작압의 밀도 leveling"* 은 GC-Cl(292 이후 1.46–1.50)에서 보인다.
- µC-Cl 이 같은 제작압에서 GC-Cl 보다 **조밀**하다 (1.47 vs 1.37 @195 · 1.54 vs 1.46 @292) — σ 순위(µC > GC)와 같은 방향.

### S-8. Fig. S4 — 저압(Au 스퍼터, ~10 MPa) σ·Ea vs 제작압 + 본문 Fig. 4 대조

| 시료 | ~97 | ~195 | ~292 | ~387 MPa (제작) |
|---|---|---|---|---|
| GC-Li₆PS₅Br (범례 "BMO") σ | **0.145** | 0.56 | 0.51 | **0.654** |
| µC-Li₆PS₅Br 비어닐 σ | 0.63 | 0.41 | 0.73 | **0.53** |
| µC-Li₆PS₅Br **소결** σ | — | **2.68** | — | **2.45** |
| GC-Li₆PS₅Br Ea (eV) | 0.339 | 0.354 | 0.343 | 0.350 |
| µC-Li₆PS₅Br 비어닐 Ea | 0.329 | 0.340 | 0.320 | 0.317 |
| µC-Li₆PS₅Br 소결 Ea | — | **0.285** | — | **0.310** |

(σ 는 mS/cm, 로그축 판독 1 px ≈ 1.7 %; Ea 판독 ±0.001 eV.  전부 digitized.)
- **본문 Fig. 4 표기값 대조**: 0.15 ↔ 0.145 ✓ · 0.65 ↔ 0.654 ✓ · 2.40 ↔ 2.45 ✓ (≤3 %) · ⚠ **0.59 ↔ 0.53 ✗** (6 px — 판독 오차 아님).
  ⇒ 판독기 자체는 검증됐다.  0.59 는 SEM 펠릿이 S4a 의 펠릿과 **다른 시료**일 가능성 (SI 무언급) — 인용은 **0.53–0.59** 폭으로.
- ★ **"고적층압 ≈ 소결" 등가** (`derived(ours)`): 비어닐 µC-Br 은 ~10 MPa 에서 **0.41–0.73** 인데 가압(S2a) 평탄은 **1.92–2.29**
  (같은 제작압끼리 **×2.9–4.8**, ≥195 MPa 제작 — ⚠ S4a 는 10 min·⌀6 mm 다이, S2a 는 CompreCell 120 s 라 **배수는 TREND**) — 그리고 **소결 펠릿을 ~10 MPa 에서 잰 값(2.45–2.68)** 이 그 가압 평탄과 **같은 급**이다.  = 본문 Fig. 5 의 두 ✓ 칸
  ("고제작+고적층" · "소결+저적층")이 **숫자로도 같은 곳에 떨어진다**.
- **Ea**: 소결 µC (0.285–0.310) < 비어닐 µC (0.317–0.340) < GC (0.339–0.354).  같은 제작압에서 소결 µC 는 비어닐 µC 보다
  **0.055 eV (~195)** · **0.007 eV (~387)** 낮다 — 크기가 제작압에 따라 크게 다르다.  방향은 입계(결정립 접촉) 기여가 줄어든 것과
  **정합** (우리 해석 — SI 는 S4b 를 해석하지 않는다).

### S-9. Fig. S5 — GC-Li₆PS₅Br EIS, −80 °C

- 반원이 끝나는 곳(저주파 스파이크 시작): **≈3.9×10⁶ Ω·cm² (97.34 MPa 제작)** vs **≈0.9×10⁶ (389.30)** → **≈4.4 배**
  (최저 −Z″ 점군의 중심 판독 — 근사).  같은 비가 상온 Fig. 4a/b 의 0.65/0.15 = **4.3** 과 비슷하다 — 단 같은 펠릿 쌍인지 SI 가
  말하지 않고, **Ω·cm² 는 두께를 포함**하므로 σ 비와 같지 않다 (`derived(ours)`, TREND).
- −80 °C 를 쓴 이유 = 상온에선 반원이 고주파 한계 밖으로 나가 **벌크 저항이 분해되지 않기** 때문 (우리 해석, SI 무언급).
  그림의 실선은 맞춤 곡선인데 **등가회로는 명시 안 됨** (n/a).

### S-10. Fig. S6 (XRD) · Fig. S7 (SEM) — 정성

- **XRD**: GC 아지로다이트 (a Cl₁.₅ · c Br · e Cl) = **넓은** 아지로다이트 반사 + 들린 배경 (나노결정 + 비정질) ↔ µC (b · d · f) =
  **날카로운** 반사 = 550 °C 어닐로 결정립 성장.  AM-Li₇P₃S₁₁ (g) = 비정질 헤일로 ↔ GC-Li₇P₃S₁₁ (h) = 헤일로 위 결정 반사.
  AM-80:20 (i) = 헤일로 위에 **날카로운 반사 몇 개**(≈27 · 45 · 53°) — SI 가 **동정하지 않는다** (잔류 결정상 가능성은 우리 추측).
  µC-LGPS (j) = 날카로움.  ⇒ "GC / µC" 라벨은 **XRD 피크 폭**으로 정의된 것이지 입경 측정이 아니다.
- **SEM** (배율·스케일바): a 40 µm (1.93 kX) · b 10 µm (5.10 kX) · c,d,e,g 20 µm · **f µC-Li₆PS₅Cl 5 µm (16.3 kX)** · h 10 µm ·
  i 40 µm (248 X) · j 20 µm.  µC-Cl (f) 은 **수 µm 급 각진 입자 + 미세 파편** — 정량 입도는 **n/a**.

### S-11. 디지타이즈 절차 · 불확실도 (재현 가능)

- **원본**: SI 임베디드 래스터를 **SMask(알파) 합성**해 흰 바탕으로 복원 (알파를 버리면 축 글자가 검게 묻힌다 — 첫 시도에서 실제로).
  S1 = 1260×1447 JPEG · S2 = 1258×987 무손실.
- **축 보정**: 축선 중심 서브픽셀 → 바깥쪽 **주눈금**(길이 ≥6 px) 명암가중 중심 → 선형 최소제곱.  잔차 **y ≤ 3×10⁻⁶ S/cm ·
  x ≤ 0.19 MPa** (10 패널 전부).  1 px = 0.0101 (S2c) · 0.0030 (S1e) · 0.0063 (S2a) · 0.0127 (S2d) mS/cm.
- **계열 색**: 범례 마커에서 추출 = Origin 기본색 (S2 는 정확히 (0,0,128) · (255,128,0) · (0,128,0) · (0,128,192) · (128,0,0)).
- **마커 중심**: 영역 띠가 x 로만 변하므로 **열별 중앙값 배경** → **가림 인지 고정반경 원 맞춤** (제 색 = 안, 배경 = 밖, 다른 색·
  반투명 가장자리 = 무시; 0.1 px 격자, 동률 최적의 중심).  R = 반투명 가중 면적으로 고립 마커에서 **4.85 px (S2) · 4.87 px (S1)**.
  그리는 순서 = 범례 순서 (486.73 맨 위) — 겹침에서 확인.  평탄 구간 점은 **전부 불일치 0** 으로 맞았다.
- **검증**: 확대 오버레이 육안 대조 (가려진 초승달 포함) + 같은 판독기로 S4a 를 읽어 **본문 Fig. 4 표기값 3개를 ≤3 % 로 재현**.
- **오차의 범위**: 위 ±값은 **그림 판독**만이다.  측정 자체의 산포(반복·오차막대)는 SI 에 없다 = **n/a** — 조건당 곡선 1개.
- **재현**: `python3 tools/litdb/cronau2021_si_digitize.py --pdf <nz1c01299_si_001.pdf>` →
  `litdb/figures/cronau2021_stack_pressure_ionic_conductivity/si_digitized.csv` (870 행: S1/S2 821 · S3 27 · S4 20 · S5 2; 열 `flag` =
  ok / occluded / neighbor_overlap / overlap_not_separable / cluster_centroid; 전 행 `provenance = digitized`).

### S-12. SI 참고문헌 (전문)

- **S1** Wenzel, S.; Randau, S.; Leichtweiß, T.; Weber, D. A.; Sann, J.; Zeier, W. G.; Janek, J. *Direct Observation of the Interfacial
  Instability of the Fast Ionic Conductor Li₁₀GeP₂S₁₂ at the Lithium Metal Anode.* Chem. Mater. **2016**, 28 (7), 2400–2407.
  DOI 10.1021/acs.chemmater.6b00610 — LGPS 합성.
- **S2** Jung, W. D.; Kim, J.-S.; Choi, S.; Kim, S.; Jeon, M.; Jung, H.-G.; Chung, K. Y.; Lee, J.-H.; Kim, B.-K.; Lee, J.-H.; Kim, H.
  *Superionic Halogen-Rich Li-Argyrodites Using In Situ Nanocrystal Nucleation and Rapid Crystal Growth.* Nano Lett. **2020**, 20 (4),
  2303–2309. DOI 10.1021/acs.nanolett.9b04597 — 아지로다이트 합성.
- **S3** Xu, R.; Xia, X.; Wang, X.; Xia, Y.; Tu, J. *Tailored Li₂S–P₂S₅ glass-ceramic electrolyte by MoS₂ doping, possessing high ionic
  conductivity for all-solid-state lithium-sulfur batteries.* J. Mater. Chem. A **2017**, 5 (6), 2829–2834. DOI 10.1039/C6TA10142A — Li₇P₃S₁₁.
- **S4** Deng, Z.; Wang, Z.; Chu, I.-H.; Luo, J.; Ong, S. P. *Elastic Properties of Alkali Superionic Conductor Electrolytes from First
  Principles Calculations.* J. Electrochem. Soc. **2016**, 163 (2), A67–A74. DOI 10.1149/2.0061602jes — **"Young·bulk 20–35 GPa"** 의
  출처 (DFT).  ⇒ 우리 SE 실물 강성 층(stoic-knuth: E_VRH 22.06 · B₀ 26.23 GPa, DFT)이 **이 밴드 안** — 그리고 우리 E_eff 1.35 (DEM)
  / 1.53 (MPM) 은 물성이 아니라 **재배열 연화 프록시**라 밴드 밖이 정상이다 (frame [2]).  ⚠ SI 는 **밴드만** 인용하고 조성별 값은
  주지 않는다.

### S-13. SI 에 없는 것 (n/a 목록 — 채우지 말 것)

σ 의 **텍스트 숫자** · 오차막대/반복수 · EIS 등가회로 · CompreCell 직경·EIS 주파수/온도 · 입도 분포 · 이론(결정)밀도 · 조성 분석 ·
**저적층압 제작압 역전**(S2c)과 **고적층압 쇠퇴**(S1 전 패널 · S2d)의 원인 · Table S1 1·2행 모순의 정오.

---

## 9. 비교 vs 우리 DEM+MPM (focused §)

### 9-1. σ_grain = 3.0 mS/cm — 값과 조건 판정
- **값 출처:** 위 §0/§6 — 본 논문은 **3.0 도, single-crystal LPSCl 도 주지 않는다.**
  가장 가까운 측정은 **µC-Li₆PS₅Br 어닐링 σ = 2.40 mS/cm** (Br, 미세결정-소결).
  우리 3.0 은 **이 ~2.4 + 타 LPSCl 문헌(cold-press 1–3, 소결 3–6)** 의 종합 채택값.
- **GB 포함 여부:** 본 논문 값은 **전부 압분체(pellet) σ** = **grain-boundary 포함**.
  단결정(GB 제거) σ 가 **아니다.** 따라서 우리 σ_grain 을 "grain-interior(단결정)"
  로 부르는 것은 **물리적으로도 부정확**(이 논문값은 GB-inclusive). Bazzoun digest 의
  "pellet 1.02 mS/cm (GB-incl) < Cronau 단결정 3.0" 대비와 일관되게, **"3.0 은
  GB-제거된 grain-interior가 아니라 잘-소결된 압분체 plateau의 상단"** 으로 봐야 한다.
- **stack-pressure 특정값인가?** 본 논문의 모든 σ 는 **고 fabrication + plateau(고
  stack)** 조건. 즉 우리 3.0 은 "압력무관 본질 grain σ" 라기보다 **"최적압력에서
  달성가능한 최선 σ"** 에 가깝다. 우리 식이 이를 **포화 상한**처럼 쓰는 것은 합리적이나,
  "단결정 본질값" 이라는 함의는 과대.
- **판정:** **사용값 3.0 mS/cm 은 합리적 범위**(Br 2.4 ~ 소결 LPSCl 3–6 사이). **라벨만
  교정**: "Cronau **2021** µC-Li₆PS₅Br plateau(~2.4) + LPSCl 문헌 종합; single-crystal
  아님, GB-inclusive pellet 기준 상한."
- ⛔ **정정 2026-09-25 (SI)** — ① *값 출처*: "가장 가까운 측정은 µC-Br 2.40" 이 아니다 — **SI Fig. S2c µC-Li₆PS₅Cl 이 같은 조성으로
  2.88–3.46** 을 준다.  ② *"잘-소결된 압분체 plateau 의 상단"* → **"소결되지 않은 µC 압분체가 고적층압에서 닿는 평탄의 하단"**
  (µC 는 어닐 후 재분쇄한 분체라 펠릿 안에서 소결되지 않았다; 평탄에 닿게 하는 것은 소결이 아니라 **적층압**).  ③ *stack-pressure
  특정값인가?* 에 대한 정량 답: **예** — 3.0 은 적층압 **≥150 MPa** 상태에 대응하고, 같은 펠릿이 **~50 MPa 에선 1.70–2.43**.
  ④ 판정 문구: "**Cronau 2021 SI Fig. S2c µC-Li₆PS₅Cl 펠릿 고적층압 평탄(≈2.9–3.5) 의 하단; 단결정·grain-interior 아님**" (§0 권고와 같다).

### 9-2. Cronau(r_SE) sub-µm 인자 — measured / defensible / loose 판정
- **measured?** ✗ — 본 논문에 r 의존 σ 곡선 없음.
- **defensible?** △ — "미세결정·소결불량 → grain-contact↓ → σ↓" **부호·메커니즘은
  강하게 지지**(Fig 1/3/4/5 전체가 이 논증). 단 **이산 클래스 효과**(AM/GC vs µC)이지
  연속 r-법칙이 아님.
- **loose?** ✅ — 3-시그모이드 breakpoint(0.5/0.3/0.1/0.03 µm)·plateau(1/0.90/0.65/0.33)
  의 **구체적 수치는 본 논문에서 도출 불가**. 다른 출처/경험 추정.
- **판정·권고:** **인자 유지**(부호 옳음 + LOOCV +0.0043 실측 개선), 그러나
  (i) **라벨 재명명** → "결정도/grain-contact 효율 인자(Cronau 2021 미세결정-소결
  메커니즘 기반 경험적 sub-µm 외삽)", (ii) breakpoint 수치는 "Cronau 측정" 이 아니라
  "경험 외삽" 으로 정직 표기, (iii) 이상적으로는 **r 보다 "결정도/소결상태" 변수**
  (또는 합성 클래스 플래그)로 재파라미터화하는 것이 물리적으로 더 정확. (현 corpus 에
  sub-µm 케이스가 1개뿐이라 실측 구분 불가 → 당장은 라벨 교정으로 충분.)

### 9-3. stack pressure vs fabrication pressure — 우리 압력 스토리와 매핑 ★
이 논문의 **두 압력 구분**은 우리 DEM/MPM 의 **두 압력 단계**와 정확히 대응한다:

| Cronau 2021 | 의미 | 우리 모델 대응 |
|---|---|---|
| **fabrication pressure** (펠릿 제작, 400–500 MPa) | 비가역 치밀화·소결 결정 | 우리 **cold-press 300 MPa** (DEM/MPM compaction target). Minnmann 10 %@300 anchor. |
| **stack pressure** (운전·측정, 5–250 MPa) | 전극접촉·grain gap 폐쇄 (가역) | 우리 **운전 압력 40–70 MPa** + EIS 측정조건. |
| red regime 전이 ~30–50 MPa | 전극접촉 확보 임계 | — (우리는 전극접촉을 모델링 안 함; 우리 σ 는 내부 network) |
| µC yellow plateau > 200–250 MPa | grain gap 폐쇄 임계 | 우리 **DEM Heckel P_y = 138 MPa** / σ-saturation. Bazzoun·Varkey 의 "σ-vs-P 가 ~400 MPa 에서 포화"와 같은 계열의 knee. |

- ★ **E_eff softening 스토리 지지 여부:** **간접 지지.** 이 논문은 "압분체 σ 는 저
  stack 에서 grain-contact 불량으로 **본질값보다 낮게** 측정된다(전극·grain gap 인공물);
  고압에서야 참값 도달" 을 보인다. 우리 DEM 의 **18× E softening** 은 "강체구 DEM 이
  못 잡는 granular rearrangement/GB-slide/micro-fracture 를 effective modulus 로
  lumping" 하는 것 — **둘 다 "압력으로 닫히는 grain-contact 결함"이 σ/치밀화를
  지배한다는 같은 물리**를 다른 층위에서 본다. 단 **직접 정량매핑은 아님**(이 논문은
  σ-vs-stack 의 거시현상, 우리는 contact-network 의 미시모델).
- ★ **Heckel knee 매핑:** 우리 DEM Heckel **P_y = 138 MPa** + 운전 40–70 MPa 는, 이
  논문의 **"red→green 전이 30–50 MPa(접촉확보) / µC yellow 종료 200–250 MPa(gap폐쇄)"**
  사이에 위치. 즉 우리 운전압력대(40–70 MPa)는 **AM/GC 라면 plateau(참 σ), µC 라면
  아직 yellow(σ 미포화)** 구간 — **"우리 SE 가 AM/GC 처럼 거동해야 운전압에서 σ 가
  믿을만하다"** 는 함의. (우리 LPSCl 이 실제로 어느 클래스인지가 중요 → §10.)
- ⛔ **정량 보강 2026-09-25 (SI, digitized)** — 위 함의가 이제 숫자로 선다 (Li₆PS₅Cl, 적층압 ~49 / ~68 MPa):
  **µC** 1.70–2.43 / 2.02–2.60 mS/cm = 자기 평탄(≥146 MPa 최댓값)의 **53–82 % / 63–88 %** (노랑 띠 49→146 MPa 에서
  +47…+73 % 더 오른다) · **GC** 0.45–0.85 / 0.46–0.95 mS/cm = **81–91 % / 91–97 %** (GC 도 ~50 MPa 는 빨강→초록 전이 끝자락)
  — 전부 `derived(ours)` 비율, 97.34 MPa 제작은 평탄이 없어 제외.  그리고 Table S1 이
  µC 의 신뢰 적층압을 **250 MPa** 로 못박는다 ⇒ 우리 운전대 40–70 MPa 에서 **µC 급 SE 의 σ 는 3.0 이 아니다** (§9-6).

### 9-4. inter-lab 1 order 산포 → 우리 σ 포락선 허용오차
- round-robin(ref 23) 의 **8-lab × 10배 산포**는, 우리 σ_ionic 포락선 **~0.03–0.14
  mS/cm** (Bazzoun exp anchor)·우리 식 LOOCV 0.975(median |err| ~7.7 %) 의 **정량
  맥락**을 준다: **문헌 σ 자체가 프로토콜로 10× 흔들리므로**, 우리 모델-실험 일치를
  "±몇 %" 가 아니라 **"이 lab-간 10× 산포 안에서 일관"** 으로 논증해야 정직하다. 즉
  **단일 "참 σ" 가 존재하지 않는다** — 압력·프로토콜 의존이라는 게 이 논문의 메시지.

### 9-5. 정직성 — 전사 가능성 (이건 우리 시스템이다)
- LIB 양극 논문들(Trevisanello 등)과 **결정적으로 다름:** 이건 **황화물 SE, 우리
  LPSCl 의 친척(argyrodite Li₆PS₅Br + LGPS + Li₇P₃S₁₁)**. → **σ_grain 의 절대값·압력
  거동은 직접 전사 가능**한 드문 논문.
- **단, 두 단서:** (i) 측정은 **Br-argyrodite**(우리는 **Cl**) — 같은 패밀리지만
  조성차로 σ 절대값 다름(Cl 가 보통 약간 더 높음). (ii) 값은 **GB-포함 압분체** σ —
  우리가 "grain-interior" 라 부르는 것과 물리적 층위가 다름(GB 미제거).
- ⇒ **σ_grain=3.0 의 사용은 정당, 라벨·연도만 교정.** Cronau(r_SE) 는 부호 정당,
  수치 외삽임을 명기.
- ⛔ **정정 2026-09-25 (SI)** — 단서 (i) *"측정은 Br(우리는 Cl)"* 는 **해소**: SI 가 Cl 을 쟀고, 같은 절차에서 µC-Cl/µC-Br ≈ **1.4**
  (486.73 제작, 적층 195–292) — *"Cl 가 보통 약간 더 높음"* 이 같은 실험실 안에서 정량으로 확인된다.  단서 (ii) *"GB 포함 압분체"* 는
  **그대로이고 오히려 핵심이 된다** (§9-6).

### 9-6. ★ (SI) σ_grain 3.0 ↔ µC-Li₆PS₅Cl 평탄 — 같은 숫자, 다른 양 (2026-09-25 신설)

| 항목 | Cronau 2021 SI Fig. S2c (digitized) | 우리 (stoic-knuth) | 판정 |
|---|---|---|---|
| 값 | 평탄 **2.88–3.46** (≥146 MPa) · Table S1 조건 3.06–3.23 · 적층압=제작압 끝점 3.04 / 3.39 / 3.06 | `σ_grain = 3.0 mS/cm` | ✅ **3.0 = 평탄의 하단** |
| 양의 정체 | **µC 압분체**(소결 안 됨) σ, 적층압 하 — **입계·결정립 접촉저항 + 잔류기공이 값 안에 있다** | STEP3 복셀 SE 셀의 σ · DEM 망의 σ_grain ("grain-interior" 라벨) | ⚠ **다른 양** — 펠릿 vs 결정 내부 |
| 계면항 | (총 σ 만 잼 — 입내/입계 분리 없음) | 복셀 FV: SE–SE 면 harmonic mean, **계면항 0** (`CONTACT_FREE`) | 구조적 차이 (아래 a) |
| 압력 상태 | 평탄 = 적층압 ≥150; **~50 MPa 에선 1.70–2.43** | 구조 = 300 MPa 압밀(하중 하); 운전 40–70 MPa | 매핑 필요 (아래 b) |
| 결정도 | µC (550 °C, µm 결정립) — **같은 조성 GC 는 0.70–1.05** | 클래스 미지정 (`Cronau(r_SE)` = 1 @ r ≥ 0.5 µm) | 미해결 — **×3–4 의 선택** (아래 c) |

**(a) `CONTACT_FREE` 해석이 한쪽 방향이 아니게 된다.**  우리 복셀 솔버엔 입계·접촉 항이 없다 (stoic-knuth CLAUDE.md §CL-81:
*"계면 저항 항이 정확히 0 이고, 먹이는 σ 도 Cronau 단결정 grain-interior 다 (펠릿 아님)"*).  SI 로 보면 **뒷문장이 틀렸다** — 먹이는
3.0 은 **펠릿값**이다.  그러면 두 효과가 반대로 걸린다: ① 순수-SE 펠릿의 **입계·결정립 접촉 저항이 3.0 안에 이미 lumping** 돼 있다
(우리 σ_VGCF = 100 이 섬유 접촉저항을 lumping 한 것과 같은 인식론, CL-47) → 복셀 σ_ion 은 결정 내부 σ 대비 **"접촉 없는 상한"
이 아니다**. ② 그 펠릿의 **잔류기공·굴곡 벌점도 3.0 안에** 있는데 STEP3 는 복합체 기공을 **따로 해상**한다 → 일부 **이중계상**
(크기는 이 SI 로 **n/a** — 절대밀도만 있고 이론밀도가 없다).  ⇒ STEP3 σ_ion 절대값을 실험 옆에 놓을 때 *"CONTACT_FREE 상한"* 한 마디로
끝내지 말고 **"펠릿-기준 입력(입계 일부 포함) + 계면항 0"** 이라고 적어야 정직하다.

**(b) 압력 상태 매핑.**  우리 구조는 300 MPa **하중 하** 압밀 상태다 → Cronau 에서 가장 가까운 것은 **"적층압 = 제작압" 끝점
(3.04 @292 · 3.39 @389 · 3.06 @487)** 이고, 3.0 은 그와 맞는다.  그러나 **운전(해제 후 40–70 MPa)** 을 말할 때는 µC 급 SE 라면
**1.7–2.6** (평탄의 53–88 %) 가 대응값이다 — "운전 σ_ion" 이라는 문장에 3.0 을 쓰면 µC 기준 그 값보다 **+15…+76 % 높다**
(3.0/2.60 · 3.0/1.70, `derived(ours)`).

**(c) 클래스가 3–4 배를 정한다.**  같은 실험실·같은 조성에서 GC 0.70–1.05 vs µC 2.9–3.5.  우리 LPSCl 의 합성·열이력이 어느 쪽에
가까운지 모르면 σ_grain 의 **클래스 불확실도는 ×3–4** 이고, 이것이 입도·라벨 논쟁보다 크다 (§10-5).

**(d) 파급 — 이 라벨 위에 세운 추론.**  `comparison_vs_ours_DEM.md` 의 *"펠릿 밴드 1.0–2.0 (Bazzoun 1.02 · Kim/Minnmann 1.6 ·
Luan 2.0) 이 Cronau 단결정 3.0 아래 = 입계 포함 서열 일관 ✓"* 는 **전제를 잃는다** — 양쪽 다 펠릿이다.  그 간격은 입계 유무가 아니라
**측정 적층압 · 결정도 클래스 · 합성/입도** 로 설명해야 하고, 각 앵커의 **측정 적층압을 카드별로 확인**해야 한다 (이 digest 에선 안 했다).
`σ_grain × Cronau(r_SE)` 는 r_SE < 0.5 µm 에서 **펠릿값(입계 포함)에 입계 인자를 한 번 더** 곱할 수 있다 — 생산 r_SE = 0.5 µm 는
인자 1.0 이라 **생산 무영향**, sub-µm 케이스에만 걸린다.

⬜ **정본 안의 라벨 전파 (2026-09-25 전수, 이 커밋에서 고치지 않음)** — *"Cronau (2022) 단결정 3.0"* 을 옮겨 적은 카드 **31장**:
`bazzoun2025_dem_parameter_sensitivity_assb_cathode` · `bazzoun2026_dem_fem_rnm_ionic` · `bielefeld2019_microstructural_modeling_composite_cathode` ·
`boschpadros2014_dem_liggghts_msc_thesis` · `cho2024_conflicting_roles_conductive_additive` · `dem_mechanical_stresses_ssb_electrode_cycling` ·
`electromechanical_contact_model_particulate_systems` · `frankenberg2024_dem_high_intensity_mixer_assb` · `hong2026_sulfide_cathode_binder_digitaltwin` ·
`interfacial_impedance_formulation_assb_cathode` · `islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell` · `kim2025_impedance_decoupling_tlm_assb` ·
`lee2024_multiphysics_dem_fem_initial_pressure_assb` · `lee2025_corolling_dryprocess_lpscl_ptfe` · `luan2025_graded_cathode_400whkg_pouch` ·
`lyu2025_3d_dem_drying_calendering_lib` · `minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2022_designing_cathodes_solidstate` ·
`nisar2024_dem_effective_electrical_conductivity_sps` · `oh2026_bimodal_composite_cathode` · `park2026_thiolene_sbr_binder_assb` ·
`reisacher2023_percolation_sulfide_carbon_matrix` · `sakuda2013_sulfide_mechanical_property` · `sangros2019_dem_calendering_lib_electrode` ·
`schlautmann2023_se_particle_size_composite_transport` · `schreiner2020_dem_calendering_lib` · `so2021_dem_fabrication_degradation_ductile_particles` ·
`so2022_dem_compaction_coated_particles_assb` · `so2022_dem_contact_model_assb_compaction_sintering` · `wang2026_dryprocess_thick_cathode_failure_ncm94` ·
`wet_processing_resolved_am_ssb_cathode_manufacturing` (+ `yonsei_dtbl_lab_triage_2026.md` 1곳, 동결 스냅샷 `INDEX_DEM_snapshot_2026-07-16.md` 1곳).
값은 어느 카드에서도 바꿀 필요가 없다 — **라벨만** ("µC 펠릿·고적층압 평탄").  그중 **"펠릿 < 단결정 = 입계 서열"** 을 논증으로 쓰는 카드
(bazzoun2026 · hong2026 · islam2026 · schlautmann2023 · minnmann2022 · luan2025 등)는 라벨보다 **논증**이 먼저 흔들린다.
일괄 정정은 **비준 대상**이라 여기엔 목록만 둔다 (원장 `SELF-51`).
⚠ **같은 날 반대 방향의 라벨 정정이 이미 나갔다** — 작업 브랜치 `se_material.py` 의 09-25 라벨 *"project-adopted, no direct literature
source"* (근거: [`cronau2022_…`](cronau2022_wet_milling_particle_size_ionic_conductivity.md) §0, `comparison_vs_ours.md` §I [Cronau22] 행 "확정",
`comparison_vs_ours_DEM.md` §B [Cronau22] 블록).  그 판정은 **2022 논문에 대해서는 옳지만**, "1차 문헌 출처 없음" 은 이 SI 로 뒤집힌다 →
권고 라벨은 §0 의 새 재귀속 문구 ("Cronau 2021 SI Fig. S2c µC-Li₆PS₅Cl 펠릿 고적층압 평탄 ≈2.9–3.5 의 하단 — 단결정·grain-interior 아님").
**비준 필요** — 코드 라벨은 이 카드가 고치지 않는다.

**(e) 무엇이 안전한가.**  SE 가 **유일한 이온 전도상**이면 σ_ion 은 σ_grain 에 **정확히 비례**(선형 문제)하므로 **같은 SE 를 쓴 구조끼리의
σ_ion 비는 σ_grain 선택과 무관**하다 — 절대값만 움직인다.  ⚠ AM 에 이온 σ 를 주는 경로가 하나라도 있으면 이 불변성은 깨진다 (확인 대상).
frame[4]/[5] 관점: 이것은 DEM↔MPM 문제가 아니라 **두 수송 솔버(접촉망·복셀)가 공유하는 재료 입력**의 문제다 — 둘 다 같이 움직인다.

---

## 10. 정직한 한계 / 우리가 주의할 점 (§10 critical caveats)

1. ★ **single-crystal 도, Cl-argyrodite 도, r-법칙도 본 논문에 없다** (§0). 우리 코드
   주석 3곳(`generate_comparison_plots.py` 근방 σ_grain 주석, `our_dem_baseline.md`,
   `lpscl_electrolyte_params.md`)의 "Cronau 2022 single-crystal Li6PS5Cl" 는 **연도
   오기 + 소재 오기 + 라벨 오기** 의 3중 부정확. 사용값 자체(3.0)는 합리적이나 **출처
   서술을 교정**해야 manuscript 에서 안전.
   ⛔ **정정 2026-09-25** — "3중 부정확" 중 둘이 무너졌다: **연도**는 별도 Cronau 2022 가 실재해 "오기" 가 아니고(§0 09-25 블록),
   **소재**는 SI 에 Li₆PS₅Cl 이 있어 "오기" 가 아니다.  남는 것은 **라벨 하나** — "single-crystal / grain-interior" → **"µC 펠릿·고적층압
   평탄"**.  ⚠ 단 그 라벨 하나가 CL-81 의 해석(§9-6 a)과 펠릿 서열 논증(§9-6 d)을 떠받치고 있어 **가볍지 않다**.
2. **클래스(소결가능성)가 입자크기보다 본질.** 본 논문의 σ 페널티는 "작은 입자"가
   아니라 "미세결정(=소결 안 되는 완전결정)" 때문. 우리 Cronau(r_SE) 가 **반경**을
   변수로 쓰는 한, 이 논문을 근거로 대는 것은 **메커니즘 불일치**(반경≠소결상태).
   다행히 "sub-µm→σ↓" 방향은 우연히 일치(작은 ball-milled 입자는 종종 미세결정·고결함).
3. **digitized vs stated 엄격구분:** Fig 4 캡션 4값(0.15/0.65/0.59/2.40 mS/cm)만
   **명시값**. Fig 2/3 plateau 는 **그림 눈금 근사(TREND)** — y축 prefactor 패널별
   상이(×10⁻⁴/×10⁻³)하니 false precision 금지.
   ⛔ **보강 2026-09-25** — Fig. 4 네 값은 캡션이 아니라 **패널 안 문구**(명시값인 것은 같다).  SI S1/S2 는 이제 **서브픽셀 판독**
   (축 잔차 ≤3×10⁻⁶ S/cm, 판독 ±0.003–0.01 mS/cm; §S-11)이지만 **여전히 digitized** 다 — "판독이 정밀하다" 와 "명시값이다" 는 다르다.
   SI 텍스트에는 σ 숫자가 **없다**.
4. **이건 SE-only 펠릿(blocking electrode) σ** — composite(CAM+SE) 도, transport
   network 도, 입자형상도 다루지 않음. **frame[5] 측면에서 이 논문은 "재료 σ_grain 의
   상한·압력의존" 만 주고**, 우리 DEM(contact-network transport)·MPM(morphology) 의
   어느 절반도 대체하지 않는다 — **재료 baseline 입력**일 뿐.
5. **우리 LPSCl 이 어느 클래스인가가 미해결:** 우리 LPSCl 이 ball-milled 미세결정(µC)
   이면, 운전압력 40–70 MPa(yellow 구간)에서 σ 가 **포화 안 됨**(이 논문). 우리 식의
   σ_grain=3.0 plateau 가정은 **"AM/GC 처럼 잘 소결된 SE"** 를 암묵 가정 — 실제
   ball-milled LPSCl 이 µC 라면 운전 σ 는 더 낮을 수 있다. (→ 우리 Cronau(r_SE)
   감쇠가 부분적으로 이걸 보정 중이라 볼 수도 있으나, 명시적 "클래스" 변수가 더 정확.)
   ⛔ **정량 보강 2026-09-25 (SI)** — 이 질문의 크기가 나왔다: 같은 실험실·같은 조성(Li₆PS₅Cl)에서 **GC 0.70–1.05 vs µC 2.9–3.5**
   (**×3.1–4.0**).  그리고 방향이 위 문장과 **반대**다 — *"AM/GC 처럼 잘 소결된 SE 를 암묵 가정"* 이 아니라, **3.0 자체가 µC 값**이다.
   즉 3.0 은 "우리 SE 가 µC 급이고 고적층압 상태" 라는 가정을 싣고 있다.  µC 면 운전압에서 1.7–2.6, GC 면 평탄이 0.7–1.05.
6. **SI 미업로드:** Table S1(권장 측정조건 요약), Fig S1–S7(추가 AM/GC/µC σ-vs-압력,
   XRD, SEM)은 본 digest 범위 밖 — 본문 6쪽 기준. SI 의 정확한 σ 수치/추가 소재가
   §8 표를 더 채울 수 있음(추후 SI 입수 시 보강).
   ⛔ **해소 2026-09-25** — SI 입수·정독 완료 (§S).  이 항목이 예고한 대로 SI 가 **§0 판정을 바꿨다** — "SI 를 안 봤다" 는 한정어를
   판정 문장 자체에 붙여 두었으면 오인용이 덜했을 것이다 (교훈: 부분 정독의 판정엔 **범위 한정어를 판정 줄에** 단다).
7. 🆕 **(SI) 원문 표기 오류 셋 — 읽을 때 보정할 것**: ① 본문 Fig. 2c · 3a,b 와 SI Fig. S1c 의 y축 **"mS·cm⁻¹" 은 S·cm⁻¹ 의 오기**
   (§4 정정) ② Table S1 1·2행 **"GC- or µC-SE"** 는 3·4행과 모순 → "AM- or GC-SE" 로 읽힘 (§S-4) ③ Fig. 4c 표기 **0.59** 와 SI S4a 판독
   **0.53** 불일치 (§6).  셋 다 **저자 정오표 없음** — 우리 판독이다.
8. 🆕 **(SI) 설명되지 않은 두 거동** — µC-Li₆PS₅Cl 의 **저적층압 제작압 역전**(~49 MPa 에서 486.73 제작이 최저)과 **고적층압 쇠퇴**
   (S1 전 패널 −5…−10 %, S2d −16 %).  SI 는 둘 다 말하지 않는다.  우리 모델 검증에 이 두 거동을 **표적으로 쓰지 말 것** — 원인 미상인
   곡선 모양을 재현했다고 기전을 주장할 수 없다.

---

## 11. 우리 작업에 가장 날카로운 3가지 insight (+ SI 1 — 2026-09-25)

1. ★ **provenance 교정 (manuscript-blocking):** σ_grain=3.0 의 주석을 "Cronau **2021**
   µC-Li₆PS₅**Br** plateau ~2.4 + LPSCl 문헌 종합 (single-crystal 아님, GB-inclusive)"
   로, 연도 2022→2021 로, "single-crystal" 라벨 제거로 교정. Trevisanello σ_S/σ_P
   오귀속과 **쌍을 이루는** 두 번째 출처-교정 항목. (값은 그대로 둬도 됨.)
   ⛔ **정정 2026-09-25 (SI)** — 교정 문구를 **"Cronau 2021 SI Fig. S2c: µC-Li₆PS₅Cl 펠릿, 적층압 ≥150 MPa 평탄 ≈2.9–3.5 mS/cm
   (digitized) 의 하단 — 단결정·grain-interior 아님"** 으로 바꾼다.  "연도 2022→2021" 은 **하지 말 것** (2022 는 별도 논문; 어느 쪽을
   가리켰는지 문서별로 본다).  Trevisanello 와의 쌍은 **유형이 갈린다** — Trevisanello 는 유형 A(안 쟀다), Cronau 는 **유형 B(쟀는데
   다른 양)** — 유형 B 가 더 위험하다 (숫자가 원문과 맞아 검증을 통과한 것처럼 보인다).
2. ★ **Cronau(r_SE) 재명명·재근거:** "입자크기 σ 감쇠" → **"결정도/소결-grain-contact
   효율 인자"**. 부호·메커니즘은 이 논문이 강력 지지(Fig 1/3/4/5), **breakpoint 수치는
   경험 외삽** 명기. 이상적 개선 = r 대신 **합성-클래스/결정도 플래그**로 재파라미터화.
3. ★ **두 압력 구분을 우리 압력 스토리에 명시 도입:** fabrication(우리 300 MPa
   cold-press) vs stack(우리 40–70 MPa 운전) 를 분리하고, **운전압력대가 이 논문의
   "µC yellow(σ 미포화) / AM·GC green(σ 포화)" 어디에 떨어지는지**를 명시. 이는 (i)
   우리 E_eff softening(압력으로 닫히는 grain-contact 결함의 lumping)·(ii) Heckel
   P_y=138·(iii) Bazzoun/Varkey 의 σ-vs-P ~400 MPa 포화 knee 를 하나의 **"압력으로
   grain-contact 가 닫히며 σ 가 포화한다"** 서사로 묶는 결정적 문헌 앵커.
4. 🆕 ★ **(SI, 2026-09-25) σ_grain 의 불확실도는 라벨이 아니라 "클래스 × 적층압" 이다.**  같은 실험실·같은 조성에서 **GC→µC ×3.1–4.0**,
   µC 안에서 **적층압 50 → ≥150 MPa 가 ×1.5–1.7** — 이 두 곱이 우리 3.0 을 **0.45 ~ 3.5 mS/cm** 사이 어디로든 옮긴다.  ⇒ σ_grain 을
   하나의 문헌 상수로 두지 말고 **(클래스, 적층압) 두 축의 조건부 입력**으로 적는 것이 이 논문 SI 의 정직한 사용법이다.  그리고
   STEP3 σ_ion 을 실험과 대조할 때는 **실험이 어느 적층압에서 쟀는지**를 먼저 물을 것 (§9-6 b·d).

---

## 12. 미니 용어집 (technique glossary)

- **fabrication pressure (제작압력):** SE 분말을 펠릿으로 **압축**할 때 가하는 압력
  (본 논문 400–500 MPa 권장). 비정질·GC 에서는 **비가역 소결·치밀화**를 일으켜 σ 를
  영구히 높임. 우리의 cold-press 300 MPa 에 해당.
- **stack pressure (스택압력):** σ 를 **측정**할 때(또는 ASSB **운전** 시) 셀/전극에
  지속적으로 가하는 압력. 가역적 — 전극접촉·grain gap 폐쇄에 관여. 우리 운전 40–70 MPa.
- **microcrystalline (µC):** 고온(~550 °C) 어닐링으로 **micron 크기 결정립**이 된 SE.
  결정립끼리 **소결 안 됨**(격자방위 불일치) → 압력 해제시 grain gap → σ 손실. ASSB
  운전조건(저 stack)에서 불리.
- **glass-ceramic (GC):** 비정질 매트릭스 + nanocrystallite. fabrication pressure 로
  **비가역 소결** 가능 → 높고 안정한 σ. (Li₇P₃S₁₁ 은 저온 어닐링으로 AM→GC.)
- **amorphous (AM):** 합성 직후 대부분 비정질. GC 와 함께 **pressure-induced sintering**
  으로 치밀화.
- **pressure-induced sintering (압력유도 소결):** 비정질입자가 압력으로 표면에너지를
  낮추며 **융합·치밀화**하는 과정. **비가역** → 압력 해제 후에도 치밀상태 유지. (µC
  결정립은 이게 안 일어남.) → Fig 4a→4b 의 입자 융합·크기증가가 직접 증거.
- **stack pressure dilemma (제목의 딜레마):** "고 fabrication 으로 치밀화는 해야 하나,
  σ 측정/운전 시 stack pressure 를 얼마로? — µC 는 저 stack 에서 gap 으로 σ 가 낮고,
  AM/GC 는 (소결 비가역이라) 저 stack 으로도 참값" 이라는, **소재 클래스마다 답이 다른**
  측정-프로토콜 딜레마.
- **round-robin / interlaboratory study (ref 23):** 같은 시료를 여러 연구실이 각자
  측정 → 프로토콜 의존 산포 정량. 본 논문 인용값 = **8-lab, ~10× 산포**.
- **red/green/yellow regime:** Fig 2 배경색. red=전극접촉불량(σ 상승, 비신뢰),
  green=plateau(참값), yellow=µC 전용 2차 stack 의존(grain gap 폐쇄 중).
- 🆕 **CompreCell / CompreDrive (SI):** rhd instruments 의 가압 EIS 셀·구동기.  같은 셀 안에서 **제작압 → 해제 → 적층압 스윕**을
  이어서 할 수 있어 Fig. 2 · S1 · S2 의 "제작압 × 적층압" 격자가 가능했다.
- 🆕 **"적층압 ≤ 제작압" 규약 (SI 그림 판독):** 각 곡선은 적층압이 자기 제작압에 닿으면 끝난다 — 적층압이 펠릿을 **다시 압밀하지
  않는 범위**만 재기 위한 것으로 읽힌다 (SI 본문 명시 없음).
- 🆕 **BMO (SI Fig. S4 범례):** 정의 없는 약어 — 캡션이 같은 점을 "GC-Li₆PS₅Br" 라 부르므로 **볼밀만 한(아지로다이트) GC** 와 동일물.
- 🆕 **Table S1 (SI):** 저자 자신의 "신뢰 σ 최소조건" 표 — 전 행 제작압 ≥400 MPa; 적층압 5 / 100 / 250 MPa (§S-4).
- 🆕 **유형 A / 유형 B 출처 오류 (`comparison_vs_ours.md` §I):** A = 그 논문이 그 양을 **안 쟀다** · B = **쟀는데 다른 양**이다.
  Cronau→3.0 은 SI 를 보고 A → **B** 로 옮겨졌다.

---

## 13. 한 줄 결론

Cronau **2021**(2022 아님)은 **우리 황화물 시스템 패밀리**(argyrodite Li₆PS₅Br + LGPS
+ Li₇P₃S₁₁, 단 **Cl/단결정 미측정**)에서 **σ 가 fabrication·stack 두 압력과 결정도
클래스(AM/GC vs µC)에 따라 ~10× 흔들린다**는 측정-신뢰성 Viewpoint. **우리 σ_grain=3.0
은 이 논문이 준 "단결정값"이 아니라 µC-Br plateau(~2.4)+LPSCl 문헌 종합 채택값(라벨
교정 필요)**, **Cronau(r_SE) 인자의 "미세결정→σ↓" 부호는 이 논문이 강력 지지하나
sub-µm 반경 breakpoint 수치는 미지지(재명명 필요)**, 그리고 **두 압력 구분은 우리
cold-press(300)/운전(40–70) · E_eff softening · Heckel P_y=138 압력 서사에 바로
들어맞는 결정적 앵커**다.

> ⛔ **정정 2026-09-25 (SI 반영 한 줄 결론)** — Cronau **2021**(별도 2022 논문 있음)은 SI 까지 합쳐 **Li₆PS₅Cl · Li₅.₅PS₄.₅Cl₁.₅ 를
> 포함한 10 시료**로 σ 가 두 압력과 결정도 클래스에 따라 흔들림을 보인 Viewpoint 다.  **우리 σ_grain = 3.0 은 SI Fig. S2c
> µC-Li₆PS₅Cl 펠릿의 고적층압 평탄(≈2.9–3.5 mS/cm, digitized) 하단으로 추적된다** — 단결정·grain-interior 가 아니라 **입계를 품은
> 펠릿을 적층압 하에서 잰 값**이고, 같은 펠릿이 운전급 적층압(~50 MPa)에선 1.7–2.4, 같은 조성의 GC 는 0.7–1.05 다.
> Cronau(r_SE) 판정과 두 압력 서사는 그대로다.

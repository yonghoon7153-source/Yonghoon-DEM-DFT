# 셀 분극에 의한 이차전지의 성능 — 오승모 (연세대 · Tutorial I)

> slug `oh2026_kecs_cell_polarization` · type `talk` (**외부 심포지엄 튜토리얼 덱 + 녹취**) ·
> **axis: `device-electrochemistry`** (⛔ 물성 4축 A–F 어느 행에도 **수치로 넣지 않는다**) ·
> 발표 **2026-08-20 (목) 제1일차 Tutorial I**, **2026년도 전지기술 심포지엄** (주최 **한국전기화학회 KECS**) ·
> 발표자 **오승모 (吳承模)** · **연세대학교 Department of Battery Convergence Engineering** · seungoh@yonsei.ac.kr ·
> 겸 **Min Tech Co., Ltd, Daejeon 34026, Korea** · 슬라이드 로고 **CECS = Research Center for Energy Conversion and Storage** ·
> 원본 자료집 PDF `litdb/inbox/oh2026_kecs_cell_polarization.pdf` (**26 pp = 표지 1 + 목차성 공백 1 + 2-up 슬라이드 24 pp**, 595×841 pt, **텍스트 레이어 0자 = 전면 스캔**) ·
> 덱 **48 슬라이드** (크롭 50컷 = 자료집 표지 2컷 + 덱 48컷) ·
> 녹취 **83분 13초 / 마지막 타임스탬프 1:23:11**, 80 블록 (기록자 안용훈) ·
> digested 2026-08-25 · status ⚠ **citable = no** (아래 coverage 참조)

## 📋 coverage · 증거 상태 (2026-08-25 codex E 스키마)

| 축 | 상태 | 뜻 |
|---|---|---|
| **슬롯** | **52 / 52 전수 보존** | 26 pp × 2-up. 백지 2건(2a·2b)도 PNG·행 모두 남겼다 (사람이 열어 `blank_confirmed`) |
| **덱 판독** | 50 / 50 컷 (내용 있는 전부) + 6–8× 재판독 5건 | |
| **음성** | ⛔ **absent — 한 번도 듣지 않았다** | 파일이 존재하지 않는다 |
| **STT** | 전문 확보 (80 블록) | **음성의 오류 많은 파생물**이다 |
| **STT 엔진** | ⛔ **unknown** | ⚠ 이전 판에 "CLOVA Note" 라고 적었으나 **원문 어디에도 그런 표기가 없다** — 형식만 보고 추정한 것이라 내렸다 |
| **권리 / Q&A 동의 / off-record** | ⛔ unknown | 사람만 채울 수 있다 |
| **⛔[불일치] 미해결** | 1 건 (슬 43 Levich ν 방향) | |

**⇒ `citable = no`.** 원본 사슬·해시는 `_transcripts/oh2026_kecs_cell_polarization_source_manifest.json`.

**이 digest 로 해도 되는 것**: 탐색 질문 생성 · 계산/실험 후보 우선순위 · 검색어와
확보할 논문 찾기 · 우리 방법의 공백 식별 · 후속 검증 계획.
**하면 안 되는 것**: canonical property 등록 · cascade 점수/랭킹/GO-NO GO 근거 ·
논문 수치와 같은 표에 배치 · **원고의 사실 주장이나 직접 인용** ·
발표자 권위를 근거로 한 방법 채택.
>
> `> elements:` **(none)** — 이 튜토리얼은 **소자 물리축**이다. 등장하는 물질(LiCoO₂·LiFePO₄·graphite·Ni-Cd·
> Daniell(Cu/Zn)·납축전지)은 전부 **개념 예시**이고, 조성을 설계하거나 물성을 재지 않는다.
> Co/Fe/Cd/Ni/Cu/Zn/Pb 를 붙이면 argyrodite 원소 페이지가 오염된다.
> `> methods:` **(none)** — DFT·AIMD·MLIP·NEB·ICOHP·DOS·Bader·ESW 가 **0건**. 실제 기법은
> `Nernst 식 · Butler–Volmer · 확산 경계층(Nernst diffusion layer) · Levich(RDE) 한계전류 · 열역학 ΔH/ΔG/TΔS` — 전부 해석식이다.
> (참고: webapp 의 원소/기법 자동링크는 `litdb/papers/` 만 훑는다 — `talks/` 에 두는 것만으로 오염이 차단된다.)
>
> ⚠ **덱 인용 규율**: `litdb/talks/README.md`. 여기 수치는 **발표 소환값**이며 `papers/` 논문값보다 한 등급 낮다.
> 우리 `db/properties/*` 절대값과 **같은 표에 넣지 않는다**.
> ⚠ **증거층은 셋이다** — 덱 · **실제 음성** · **STT(음성의 파생물)**. 우리는 음성을
> 들은 적이 없으므로 **`[말]` 배지를 쓰지 않는다.** 2026-08-25 이전 판의 `[말]` 77건은
> 전부 `[STT]` 로 내렸다 (그대로 두면 **STT 환각이 발표자의 실제 발언으로 승격**된다).
> **[덱]** = 인쇄된 것 / **[STT mm:ss]** = 녹취 문자열에만 있는 것 /
> **[덱+STT]** = 둘이 일치 / **⛔[불일치]** = 둘이 다름.
> **숫자는 원칙적으로 [덱] 만 인용**하고, [STT] 의 숫자는 `구두 ≈` 로 표기했다.
>
> ⚠ **`transcript_error` 라는 판정을 쓰지 않는다.** `a미타` 가 실재 낱말이 아니라는 것
> (비어휘성)은 관측되지만, **오류가 STT 에서 났는지 발표자의 실언인지는 음성 없이
> 관측 불가**다. 그래서 우리가 말할 수 있는 것은 `stt_status = normalized_unique`
> (한 가지로만 읽힌다) + `normalization_basis = deck+context` 까지다.

---

## 0. 한 줄 · 왜 이 세션인가

**한 줄**: 이차전지가 내주는 전압·용량·에너지·발열이 왜 이론값에 못 미치는가를 **단 하나의 양
— 셀 분극 `cell polarization = η_a + η_c + iR_total`** 로 환원하고, 그 세 항이 각각 *어떤 물리에서
왜 생기는지*를 평형에서부터 한 걸음씩 끌어내는 튜토리얼이다. [덱 슬 2·10·23·47]

**왜 이 세션을 남기나** — 세 가지다.

1. **우리가 계산하는 σ_ion 이 소자에서 어떤 얼굴로 나타나는지**를 이 발표가 정확히 지정한다.
   슬 44 의 `R_separator = l / (κ_separator · A)` 한 줄이 **우리 MLIP-MD 의 κ 와 셀의 iR_total 을
   잇는 유일한 다리**다. 그리고 덱 슬 44 의 파란 박스에 그 결론이 **인쇄돼 있다** —
   *"What really matters is not the conductivity but the resistance !!"* `[덱 44]`
   (같은 취지가 `[STT 1:17:17]` 에도 있으나 문구는 음성 미확인이라 귀속하지 않는다).
   우리가 "modelc 가 comp1 보다 D 2.6× 빠르다"고 말할 때
   빠져 있는 것이 정확히 `l` 과 `A` 다.
2. **우리 ESW onset(2.256 V)을 셀 전압과 직접 비교하면 안 되는 이유**를 슬 23–26 이 유도해 준다.
   전극이 실제로 겪는 전위는 `E^a = E^a_eq + η_a` 라서, **고율일수록 SE 가 보는 산화 구동력이
   공칭 셀 전압보다 더 세진다**. 우리 축 ②(산화안정)의 해석 문장이 여기서 한 칸 정확해진다.
3. **양식의 기준판**. 심포지엄 세션 10편 이상이 같은 형식(덱 + STT 녹취)으로 들어온다.
   이 문서가 §2 정렬표 · §5 STT 교정표 · §6 "접점 없으면 없다고 쓰기" 의 본보기다.

**⚠ 이 발표는 우리 물성 4축(A 이온전도 / B 산화안정 / C 기계 / D 전자구조) 에 *수치를 하나도*
공급하지 않는다.** 층위가 다르다 — 우리는 **재료 내부(Å–nm, 0 K–1000 K MD)**, 이 발표는
**소자(µm–cm, 실동작 전류)** 다. 접점은 §6 에 **개념 다리 4개 + 우리가 안 다루는 것 5개**로만 적었다.

---

## 1. 메타

| 항목 | 값 | 근거 |
|---|---|---|
| 세션 | **2026년도 전지기술 심포지엄 · 제1일차 8월 20일(목) · (Tutorial I)** | [덱] 자료집 표지 (fig_1a) |
| 제목 | **셀 분극에 의한 이차전지의 성능** / *Effects of cell polarization on cell performances* | [덱] 표지 + 슬 1 |
| 발표자 | **오승모** | [덱] 슬 1 (STT `오승목` 은 오인식) |
| 소속(덱 인쇄) | `Department of Battery **Conflation** Engineering, Yonsei University` | [덱] 슬 1 — **8× 재판독 확정.** `Conflation` 은 **덱 오타**이며 정식 명칭은 **Battery Convergence Engineering (배터리융합공학과)** |
| 이메일 | seungoh@yonsei.ac.kr | [덱] 슬 1 |
| 겸직 | Min Tech Co., Ltd, Daejeon 34026, Korea | [덱] 슬 1 |
| 주최 | 한국전기화학회 (KECS) | [덱] 표지 로고 |
| 연구센터 | CECS = Research Center for Energy Conversion and Storage | [덱] 전 슬라이드 하단 |
| 자료집 분량 | PDF **26 pp** (p.1 표지 · p.2 **공백/구분면**(추출 제외) · p.3–26 = 2-up 슬라이드 24 pp) | 도구 산출 + 직접 확인 |
| 덱 분량 | **슬라이드 48장** | 슬 48 하단 소번호 |
| 녹취 | **83분 13초**, 80 블록, 화자 2인(참석자 1 = 좌장/사회, 참석자 2 = 오승모) | `_transcripts/*.json` |
| 참고문헌(덱 명시) | **"전기화학" 5판, 오승모 저 (자유아카데미, 2025)** | [덱] 슬 48 — 이 튜토리얼의 정본 |
| 공개 질의응답 | **없음** — 좌장이 "질문이 없으실 것 같기도 그래서 나중에 쉬는 시간에 질문 따로 해요" [STT 1:22:59] | 녹취 |

### 1b. ⚠ 녹취 파일 헤더 시각은 **발표 시각이 아니다**

STT 원문 헤더는 `2026.08.25 화 오전 9:22 ・ 83분 13초` 다. 그러나 발표는 **8월 20일(목)** 이다 [덱 표지].
그리고 **같은 `2026-08-25 09:22` 가 다른 발표 녹취(`yang2026_ncm_radial_microstructure_ml`, 40분 16초,
발표일 8/18)에도 똑같이 찍혀 있다.** ⇒ 이 시각은 **CLOVA Note 업로드/처리 시각**(여러 파일 일괄 업로드)
이지 발표 시각이 아니다. **앞으로 오는 10편에서도 헤더 시각을 발표 시각으로 인용하지 말 것.**
(내부 정황상 실제 발표는 오전 세션이었다 — 종료 직후 좌장이 "11시에 다시 시작하겠습니다" [STT 1:23:11].
하지만 시작 시각을 확정할 근거가 없으므로 **판독 불가**로 남긴다.)

### 1c. 📐 판독 메타 (`talks/README.md` §3c 준수)

| 항목 | 값 |
|---|---|
| 1차 통독 배율 | **2-up 크롭 1124×795 px (≈136 dpi, native ≈1.35×)** — 50컷 **전부** 이미지로 열어 판독 |
| 고배율 재판독 | **5건 / 6×–8×** (아래 표) |
| 텍스트 레이어 | **0자 (전 26쪽)** — 키워드 매칭 원리적으로 불가, 자동 정렬 없음 |
| 판독 불가로 남긴 것 | 슬 22 SEM 스케일바 **"10"** 의 단위(노란 텍스트박스가 가림) — µm 로 **추정**되나 인용 금지 |

| # | 대상 | 배율 | 결과 |
|---|---|---|---|
| 1 | 슬 1 소속명 | 8× | `Battery **Conflation** Engineering` **확정** (덱 오타) |
| 2 | 슬 9 Ni-Cd 삽입그림 라벨 | 8× | **우리 1차 전사 오류 발견·정정**: 상단 점쇄선은 `E_cal = 1.44 V`(우리가 처음 `E_cell` 로 잘못 읽음), 그 아래가 `E° = 1.30 V`, 파란 굵은 선이 `E_cell`. 곡선 라벨 `2×I₁₀ / 10×I₁₀ / 50×I₁₀ / 100×I₁₀`, y=Cell voltage/V 0.8–1.5, x=0–100 |
| 3 | 슬 9 본문 E⁰ 3줄 | 6× | `E⁰=−0.81` / `E⁰=0.47` / `E⁰_cell = **1.28 V**` **확정** |
| 4 | 슬 32 용량 수치 | 6× | `750 mAh` / `600 mAh` / `560 mAh` / `560 mAh` **확정**, 곡선 라벨 `0.2C·0.5C·1C·2C·4C` **확정** |
| 5 | 슬 43 확산 문장 | 6× | `solid-state bulk diffusion is **10³~10⁵** slower than in solution` **확정** |

> 🔁 **교훈(다음 10편에 그대로 적용)**: 1차 통독(≈1.35×)에서 **슬 9 의 `E_cal` 을 `E_cell` 로 잘못 읽었다.**
> `lee2026_skku`·`moon2026_cau` 재판독에서 나온 것과 **똑같은 실패 모드**다 —
> **삽입 그림(외부 출처)의 라벨은 무조건 6× 이상 재렌더**한다.

### 1d. 🔢 PDF 쪽 ↔ 덱 슬라이드 번호 대응 (**둘이 다르다 — 반드시 이 표로 환산**)

크롭 파일명은 **PDF 쪽 + a(위)/b(아래)** 이고, 덱 자체 인쇄번호(슬라이드 우하단 오렌지 소번호)와 **다르다**.
자료집 하단의 `- N -` 은 **PDF 쪽번호**다(덱 번호가 아니다).

```
덱 슬라이드 번호 = 2 × (PDF 쪽) − 5     (a = 위 컷)
덱 슬라이드 번호 = 2 × (PDF 쪽) − 4     (b = 아래 컷)
```

| PDF 쪽 | `a` 컷 = 덱 슬 | `b` 컷 = 덱 슬 |   | PDF 쪽 | `a` 컷 | `b` 컷 |
|---|---|---|---|---|---|---|
| 1 | (자료집 표지 상) | (자료집 표지 하) | | 14 | **23** | **24** |
| 2 | *(공백 — 추출 제외)* | *(공백)* | | 15 | **25** | **26** |
| 3 | **1** | **2** | | 16 | **27** | **28** |
| 4 | **3** | **4** | | 17 | **29** | **30** |
| 5 | **5** | **6** | | 18 | **31** | **32** |
| 6 | **7** | **8** | | 19 | **33** | **34** |
| 7 | **9** | **10** | | 20 | **35** | **36** |
| 8 | **11** | **12** | | 21 | **37** | **38** |
| 9 | **13** | **14** | | 22 | **39** | **40** |
| 10 | **15** | **16** | | 23 | **41** | **42** |
| 11 | **17** | **18** | | 24 | **43** | **44** |
| 12 | **19** | **20** | | 25 | **45** | **46** |
| 13 | **21** | **22** | | 26 | **47** | **48** |

⚠ **크롭 프레임이 반 슬라이드씩 어긋나 있다.** `a` 컷은 위쪽에 앞 슬라이드의 잘린 아랫단이,
`b` 컷은 아래쪽에 자료집 쪽번호가 함께 들어온다. 그래도 **각 컷에 목표 슬라이드 1장이 온전히 들어간다**
(다만 `a` 컷 일부는 해당 슬라이드의 하단 소번호가 잘린다 — 그 경우 위 공식으로 환산).

---

## 2. 슬라이드 ↔ 녹취 정렬 표

> 채우는 규칙: **슬라이드 이미지를 실제로 본 뒤에만** 채운다. `?` 는 "발화를 그 슬라이드에 못 붙였다"는 기록이고
> 지우지 않는다. 시각은 녹취 블록 시작 시각.

| 덱 슬 | 크롭 | 제목 (덱 인쇄) | 시각 | 무엇을 말했나 | 슬라이드에 **없는** 말 |
|---|---|---|---|---|---|
| — | `fig_1a/1b` | (자료집 표지) | 00:00–00:06 | 좌장이 약력 소개 (서울대 화생공 → 연세대) | 약력 자체는 [STT]만 — **STT 붕괴가 심해 인용 금지** |
| **1** | `fig_3a` | 타이틀 | 00:40 | "오승모입니다" | — |
| **2** | `fig_3b` | Cell polarization (셀 분극)? | 00:40–05:41 | 충방전 곡선에서 `E_charge = E_cell + (η_a+η_c+iR)`, `E_discharge = E_cell − (…)`; 면적 = 에너지; 분극=0이면 손실 0 | "이런 전지는 쓸데가 없는 전지죠" — 손실을 **직관적 반칙**으로 부르는 어투 [STT 02:00] |
| **3** | `fig_4a` | E_cell in secondary batteries? | 05:41–07:48 | 반쪽전지 2개 → Nernst → `E_cell = E^c_eq − E^a_eq`; 아래 6개 미니그래프로 "일정할 수도, 변할 수도" | graphite 반쪽반응을 즉석 예시로 듦 [STT 05:41] |
| **4** | `fig_4b` | 평형 전압; Equilibrium potential (E_eq) | **?** | 이 슬라이드를 **명시적으로 짚은 발화를 특정하지 못했다.** 05:41–07:48 의 Nernst 설명이 여기일 수도, 슬 3 일 수도 있다 | ? |
| **5** | `fig_5a` | E_eq profiles — FePO₄/LiFePO₄ | 07:48–11:00 | 2상 반응 → 두 상이 순수상이라 a=1 → E_eq 불변 | **얼음–물 비유**: "얼음이 녹을 때 물이 많아지고 얼음이 없어지듯" [STT 08:50] |
| **6** | `fig_5b` | E_eq profiles — LiCoO₂ | 11:00–12:48 | 단상 인터칼레이션 → `<>` 줄고 `<Li⁺>` 늘어 → E_eq 감소 | — |
| **7** | `fig_6a` | E_cell ? (emf 정의) | **?** (내용은 07:48·42:32 에 흩어짐) | emf·최대 방전전압 정의는 두 번(초반·중반) 말했으나 이 슬라이드에서 말했는지 특정 불가 | ? |
| **8** | `fig_6b` | E_cell ; Daniell cell | 12:01–13:55 | Cu/Zn 반쪽전지, `E⁰_cell = 0.34 − (−0.76) = 1.1 V`, 방전 중 E_cell 감소 | — |
| **9** | `fig_7a` | E_cell ; Ni-Cd cell | 13:55–15:00 | 고체 activity=1 → **Ni-Cd 는 E_cell 이 안 변한다**; 납축·리튬이온은 감소 | — |
| **10** | `fig_7b` | Cell polarization ? | 15:00–16:05 | η_c·η_a·iR_total 의 정의를 한 줄씩 | "뒤에 나중에 다시 설명드릴게요" — **정의를 먼저 던지고 나중에 되짚는 구조**를 명시 [STT 15:00] |
| **11** | `fig_8a` | Current is an expression of reaction rate | 16:05–17:10 | `i = nF·dN/dt` → **전류 = 반응속도**; 고율충전 = 고전류; CC = 일정속도 | "전기화학에서 전류는 반응 속도인 거예요" 를 **세 번 반복** — 이 튜토리얼의 축 [STT 16:05·17:10] |
| **12** | `fig_8b` | Two processes for an electrode reaction | 17:10–19:25 | 전자 터널링 ∝ e^(−d) → 반응은 표면 근처에서만 → mass transfer 필요; 직렬 2단계 중 **느린 쪽이 전체 속도** | "멀리 있는 애는 반응에 참여를 못한다" [STT 18:17] |
| **13** | `fig_9a` | η_c and η_a | 19:25–21:40 | 평형에서 mass/charge transfer 모두 0 → 전류 0 → 충전하려면 E_eq 를 벗어나야 함 | **"풀셀의 평형전압 이런 말은 없어요"** — 아래 §4B-B1 로 [STT 20:22] |
| **14** | `fig_9b` | Charge transfer rate is zero at E_eq ?? | 21:40–23:59 | `rate = k[O]_s`, `k ∝ e^η`, `η = |E_appl − E_eq|`; E_eq 는 상수, E_appl 이 우리 손잡이 | "이게 변수죠, 이게 어플라이드는 변수야" — **무엇이 상수이고 무엇이 노브인지**를 반복 [STT 22:51] |
| **15** | `fig_10a` | Charge transfer rate is zero at E_eq ?? (BV 그림) | 23:59–26:10 | 점선 i_c·i_a 는 **안 보이는 전류**, 실선 i_net 만 측정됨 | — |
| **16** | `fig_10b` | Butler-Volmer equation | 26:10–28:13 | `i₀ = FAk⁰C_O*^(1−α)C_R*^α`, α=0.3~0.7; E_eq 에서 net=0 | "이 리터블(=invisible)이라고 얘기를 해, 우리가 측정되는 전류가 아닌 거죠" [STT 26:10] |
| **17** | `fig_11a` | Activation overpotential | 28:13–29:28 | 밀어준 만큼 net rate 가 생긴다; 더 큰 전류 → 더 큰 η_act | 불 비유가 여기서부터 시작 ("불씨를 살린다") |
| **18** | `fig_11b` | Mass transfer (diffusion) rate is zero at E_eq ?? | 29:28–34:02 | 확산/migration/convection 중 **표면 근처는 확산뿐**; 평형=농도구배 0=확산 0; E_appl↓ → C_O(0,t)↓ → 구배↑ | migration 제거 근거를 **supporting electrolyte** 로, convection 제거 근거를 **고체 표면에서 v=0** 으로 각각 댐 [STT 30:39] |
| **19** | `fig_12a` | Concentration overpotential | 34:02–36:16 | 확산속도를 0보다 크게 만들려고 더 걸어주는 전압 | — |
| **20** | `fig_12b` | iR voltage drop ? | 36:16–37:19 | 전류는 **닫힌 고리** 안에서만 흐른다 | — |
| **21** | `fig_13a` | Current flows in a closed-loop | 36:16–37:19 | `i_c = |i_a| = i(electrolyte)`; 전해질에서는 **migration** 이 전류를 나름 | — |
| **22** | `fig_13b` | Shut-down mechanism in LIBs | 37:19–39:22 | PE 분리막 135 °C 용융 → i_separator=0 → **전 회로 전류 0** | "이거 자꾸 반복해서 설명드리는 게 아니고" — closed-loop 원칙 하나로 셧다운을 유도하는 게 요지 [STT 38:17] |
| **23** | `fig_14a` | Why cell polarizations?? | 39:22–40:18 | ① E_eq 에서 i=0 이라 과전압 필요 ② closed loop 의 모든 IR 를 넘어야 | **불 비유 완성**: "전극에서 불씨를 살리고, 그다음엔 회로를 타고 흐르면서 IR 를 넘어야" [STT 39:22·40:18] |
| **24** | `fig_14b` | E_charge of graphite/LiCoO₂ cell | 40:18–41:27 | 충전 시 graphite=cathode, LiCoO₂=anode; `E^c = E^c_eq − η_c`, `E^a = E^a_eq + η_a` | — |
| **25** | `fig_15a` | Additional iR_total | 41:27–42:32 | `E_charge = E_cell + cell polarization` 완전 유도; `R_total = R^a_circuit + R_anolyte + R_separator + R_catholyte + R^c_circuit` | — |
| **26** | `fig_15b` | E_cell (요약 + Graphite/LiCoO₂ 표) | 42:32–44:50 | emf = 최대 방전전압 / 열역학 분해전압 = 최소 충전전압; 충·방전에서 **anode·cathode 가 뒤바뀐다** | 표의 0.2 V·4.0 V 로부터 **구두 ≈ 3.8 V** 를 즉석 계산 [STT 43:37] · "여러분 자꾸 헷갈리는 거예요" [STT 43:37] |
| **27** | `fig_16a` | E_discharge for secondary cells | 41:27–42:32 | 방전도 같은 구조, 부호만 반대 | — |
| **28** | `fig_16b` | Another notation of cell polarization | 44:50–46:xx | (a,c) 분해 ↔ (activation, concentration) 분해 — **같은 첨자를 두 가지 뜻으로 쓴다** | **§4A-A2 의 핵심 경고**가 여기 [STT 45:57] |
| **29** | `fig_17a` | Contributions to cell polarization | 46:xx–48:21 | 세 항의 i–V 기울기: `1/R_ct`, `1/R_mt`, `1/R_total`; **activation=저전류 / concentration=고전류 / iR=중간전류 지배** | — |
| **30** | `fig_17b` | Cell polarization vs. current | 47:15–49:35 | (a)저전류=활성화, (b)중간=옴, (c)고전류=농도 | ⚠ **"이건 실제적인 데이터예요"** [STT 47:15] — 그러나 덱 그림엔 **축 눈금도 출처도 없다** (§7-3) |
| **31** | `fig_18a` | Impact of cell polarization on cell performances | 48:21–50:53 | 0.2C→4C 로 분극 증가 → 방전전압↓ → cut-off 3.0 V 조기 도달 → **실제 용량·에너지 동시 감소** | 화살표를 그리며 "0.5C 에서는 매우 작아, 4C 에서는 이만큼" [STT 49:35] |
| **32** | `fig_18b` | Discharge capacity | 50:53–55:33 | **dischargeable 750 mAh** vs **actual at 2C 560 / at 4C 50 mAh** (cut-off 3.0 V); 750 짜리와 600 짜리가 2C 에서 **똑같이 560** | **§4A-A3 가성비 논지** — "저도 그랬고" 라는 자기반성 포함 [STT 54:14] |
| **33** | `fig_19a` | Heat effects in battery | 55:33–57:42 | `ΔH = ΔG + TΔS`; `ΔG = −nFE_cell`, `ΔH = −nFE_cal`; **E_cal 은 가상(imaginary) 기전력** | "별로 중요한 얘기는 안 해요" 라며 **E_cal 을 비교용 눈금으로만** 쓰겠다고 선 그음 [STT 56:35] |
| **34** | `fig_19b` | Thermodynamic origin for heat: Ni-Cd | 57:42–59:51 | 방전 `ΔH=−282 / ΔG=−256 / TΔS=−26 kJ mol⁻¹`(발열), 충전은 전부 부호 반전(흡열) | 구두 수치는 반올림·실언(≈−280, ≈−250, "플러스 1") → §5 |
| **35** | `fig_20a` | Total heat effects: **discharge** | 59:51–1:04:06 | `Q_total = Q_rev + Q_Joule`; `Q_rev = ∫(E_cal − E_cell)i dt`, `Q_Joule = ∫(E_cell − E_discharge)i dt = ∫(η_a+η_c+iR)i dt`; **Q_Joule 은 kinetic origin, 항상 발열** | "얘는 항상 발열이란 말이에요. 한쪽으로만 갑니다" [STT 1:02:07] |
| **36** | `fig_20b` | Total heat effects: **charge** | 1:04:06–1:05:18 | 충전에서 Q_rev 는 흡열이 될 수 있으나 **Q_Joule 은 여전히 발열** | — |
| **37** | `fig_21a` | Energy efficiency in secondary batteries | **1:05:18 — 건너뜀** | **"이거 아까 설명드렸으니까 그냥 넘어갈게요"** [STT 1:05:18] | 덱에는 `Energy efficiency = 방전에너지 / 충전에너지` 정의가 있으나 **구두 설명 없음** |
| **38** | `fig_21b` | (Q&A 슬라이드) 방전 시 셀이 식을 수 있나 | 1:05:18–1:07:40 | **Yes, if Q_rev(흡열) > Q_Joule(발열)**; 예시 **VRLA 저전류 방전** | 구두는 "납축전지" 로만 부름 — 덱의 `VRLA` 와 [덱+STT] 일치 |
| **39** | `fig_22a` | Heat effects in a lead-acid cell | 1:07:40–1:10:17 | E_cell > E_cal 인 계 → ΔG > ΔH → TΔS 를 **밖에서 받아온다** = 흡열 | "옆에서 보내는 게 뭐야? 흡열이죠" [STT 1:08:46] |
| **40** | `fig_22b` | Thermal runaway triggered by internal short | 1:10:17–1:11:16 | 내부단락 → R≈0 → 자가방전 고율 → 분극↑ → **Q_Joule ≫ Q_rev** → 80–100 °C 넘김 → SEI 붕괴 → 폭주 | **"SEI 가 LIB 의 가장 약한 지점"** [덱] 을 구두로 강조 |
| **41** | `fig_23a` | Charging voltage and charged capacity | 1:11:16–1:12:43 | 고율 충전 → 분극↑ → E_charge↑ → 충전 cut-off 조기 도달 → **충전 용량 감소** | "고속 충전이 원활히 되려면 셀 분극이 작아야" [STT 1:12:12] |
| **42** | `fig_23b` | How to minimize activation overpotential? | 1:12:43–1:14:56 | `R_ct = RT/(i₀F)`, `i₀ = FAk⁰C_O*^(1−α)C_R*^α` → **A↑, k⁰↑, C↑** | "지금 5분 남았어요" — 이후 급가속 [STT 1:12:43] |
| **43** | `fig_24a` | How to minimize concentration overpotential? | 1:14:56–1:16:10 | `R_mt = RT/(nF·i_L,c)`, Levich `i_L,c = 0.62nFAD_O^(2/3)C_O*ω^(1/2)/ν^(1/6)`; **고체 벌크 확산은 용액보다 10³~10⁵ 느리다** | ⛔ ν 방향 불일치 (§5-B) |
| **44** | `fig_24b` | How to minimize iR_total? | 1:16:10–1:18:33 | `R_total = R_separator + R_solution + R_circuit + R_SEI + R_others`; 대개 **R_separator > R_solution > R_circuit**; `R = l/(κA)` | **"진짜 중요한 건 전도도가 아니라 저항이란 말이에요"** [덱+STT 1:17:17] — §4A-A1 |
| **45** | `fig_25a` | Lithium-ion cells: Jelly-roll type | 1:18:33–1:19:25 | 젤리롤은 A 가 극단적으로 크고 l 이 짧아, **비수계 전해질의 낮은 κ 를 기하로 상쇄** | "얘가 작더라도 면적을 키웠단 말이죠" [STT 1:18:33] |
| **46** | `fig_25b` | R_SEI in lithium-ion cells | 1:19:25–1:21:57 | 노화 셀에서 **R_SEI 가 다른 저항보다 큰 경우가 잦다**; 고온 노출 → 전해질 분해 → 더 두껍고 더 치밀한 SEI | "방금 만든 셀은 별로 문제가 안 되지만 오래된 셀은…" [STT 1:20:52] |
| **47** | `fig_26a` | Summary (Why / Adverse effects) | 1:21:57–1:22:59 | 왜 분극이 생기나 3줄 + 나쁜 영향 4줄 | — |
| **48** | `fig_26b` | Summary (How to minimize) + 참고서 | 1:21:57–1:22:59 | 8개 처방 + `R_total = R_separator + R_solution + R_electrode + R_SEI` | 참고서 **"전기화학" 5판(자유아카데미, 2025)** 은 [덱]만 |

**커버리지 요약**: 48 슬라이드 중 **46장에 발화를 붙였다.** `?` 2장 = **슬 4, 슬 7**
(내용상 다뤄지긴 했으나 *어느 슬라이드에서* 말했는지 특정 불가). 슬 37 은 **명시적으로 건너뛰었다**
(덱에는 있으나 구술 없음 — 정렬표에 그렇게 기록).

---

## 3. 내용 — 개념의 사슬 (슬라이드 순서)

> 이 절은 **결론 나열이 아니라 유도 순서**로 적었다. 이 튜토리얼은 "왜 그렇게 되는가"의 순서 자체가 내용이다.
> 각 항목 끝의 `[덱]`/`[STT]`/`[덱+STT]` 이 근거 등급이다.

### 3-1. 출발점 — 잃어버린 에너지의 정체 (슬 2)

- **[덱]** 충방전 곡선 위에 수평 빨간선 하나(`E_cell`, 예시 그림에서 2.0 V)를 긋고, 그 위/아래를
  `E_charge`, `E_discharge` 로 나눈다.
  ```
  E_charge    = E_cell + (η_a + η_c + iR_total)
  E_discharge = E_cell − (η_a + η_c + iR_total)
  Cell polarization ≡ η_a + η_c + iR_total
  ```
- **[덱]** `Electrical energy = voltage × capacity` 이므로 곡선 **아래 면적 = 에너지**.
  충전에 쓴 면적과 방전으로 되찾은 면적의 **차이**가 손실이고, 그 손실이
  ```
  Q_Joule = ∫₀ᵗ (η_a + η_c + iR_total) · i · dt      (충전 과정 / 방전 과정 각각)
  ```
- **[덱]** 결론 3줄: `Discharged energy ≪ charged energy` / 그 원인은 충·방전 **양쪽**에서 생기는 Q_Joule /
  **분극이 0 이면** `E_charge = E_discharge = E_cell` 이고 에너지 손실이 0.
- **[STT 02:00–04:27]** 같은 내용을 그림 위 손짓으로: "빨간선 **위** 면적이 충전 중 Q_Joule,
  **아래** 면적이 방전 중 Q_Joule"; "이런 전지는 쓸데가 없는 전지죠"; "그런 전지는 없죠"(분극 0 은 이상).

> **여기가 튜토리얼의 뼈대다.** 남은 46장은 전부 이 한 식의 세 항 — `E_cell`, `η`, `iR` — 을 하나씩
> 해부하는 순서다. **① E_cell 이 뭔가(슬 3–9) → ② η 가 왜 필요한가(슬 10–19) → ③ iR 은 왜 생기나(슬 20–22)
> → ④ 다시 합쳐서 E_charge/E_discharge 유도(슬 23–27) → ⑤ 결과(용량·에너지·열·안전, 슬 28–41)
> → ⑥ 처방(슬 42–46) → ⑦ 요약(슬 47–48).**

### 3-2. E_cell 은 무엇인가 — 반쪽전지 두 개의 차 (슬 3–4, 7)

- **[덱 슬 3]** 배터리는 반쪽전지 2개다. 각각 `O + ne = R`, `O' + ne = R'`.
  Nernst 로 각각의 평형전압을 얻고,
  ```
  E^a_eq = E⁰(O/R)   + (RT/nF) ln(a_O /a_R )
  E^c_eq = E⁰(O'/R') + (RT/nF) ln(a_O'/a_R')
  E_cell = E^c_eq − E^a_eq          (a = 산화 일어나는 쪽, c = 환원 일어나는 쪽)
  ```
- **[덱 슬 3]** 아래 6개 미니그래프가 이 절의 핵심 **그림 논증**이다: 반쪽전지 E_eq 가 **평평할 수도**
  (위 3개) **변할 수도**(아래 3개) 있고, 그 조합으로 full-cell E_cell 이 평평하거나 감소한다.
- **[덱 슬 4]** Nernst 를 활동도(a) → 활동도계수(γ) → 농도(C) 로 풀어 쓰고
  `E⁰' = formal potential`, `E⁰ ≈ E⁰'` 를 도입. 예시 **`Li⁺+e=Li : E⁰ = −3.045 V (vs NHE, 25 °C)`**,
  **`Cu²⁺+2e=Cu : E⁰ = 0.34 V`**. 노란 강조: **"반쪽전지의 평형전압은 변할 수 있다."**
- **[덱 슬 7]** `E_cell` 의 이름표 정리 — **기전력(electromotive force)**, **완전지가 가질 수 있는
  최대 방전전압**, 그리고 **변화할 수 있음**. 표준상태 값 `E⁰_cell = E⁰_c − E⁰_a` 는 **상수**.
- **[STT 20:22]** ★ 평형전압은 반쪽전지에 대한 개념이고 풀셀에는 그 말이 성립하지 않는다는
  취지 (우리 의역 — 문구는 음성 미확인). → §4B-B1, **가설 전용**.

### 3-3. E_eq 가 언제 변하고 언제 안 변하나 — 2상 vs 단상 (슬 5–6)

이 대비가 튜토리얼 전반부의 **개념적 클라이맥스**다.

**2상 반응 (슬 5, FePO₄/LiFePO₄)** — **[덱]**
```
FePO₄ + Li⁺ + e = LiFePO₄
E_eq = E⁰ + (RT/F) ln [ a(Li⁺,electrolyte) · a(FePO₄) / a(LiFePO₄) ]
```
- FePO₄ 와 LiFePO₄ 는 **서로 다른 순수상**이라 각각의 활동도가 **정확히 1.0**.
- 전해질의 Li⁺ 는 충분히 많아 **상수**로 볼 수 있다.
- ⇒ 로그 안이 전부 상수 ⇒ **E_eq 가 방전 내내 불변**.
- **[덱] 파란 결론**: *"E_eq of half-cells does **not** change for **two-phase** reactions."*
- **[STT 08:50]** 비유: "얼음이 녹을 때 얼음과 물이 공존하는데, 물이 많아지면 얼음이 없어지잖아요."

**단상 반응 (슬 6, LiCoO₂)** — **[덱]**
```
Discharge:  Li₀.₅CoO₂ → Li₀.₇CoO₂ → Li₀.₉CoO₂ → LiCoO₂     (+ Li⁺ + e)
반쪽반응을 "자리(site)" 로 쓰면:   < >  + Li⁺(electrolyte) + e  =  <Li⁺>
E_eq = E⁰ + (RT/F) ln [ a(Li⁺) · a(< >) / a(<Li⁺>) ]
```
- 방전이 진행되면 **빈자리 `< >` 는 줄고(↓), 채워진 자리 `<Li⁺>` 는 는다(↑)** — 덱에 화살표로 표시.
- ⇒ 로그 항이 계속 작아짐 ⇒ **E_eq 가 방전에 따라 감소**.
- **[덱] 파란 결론**: *"E_eq of half-cells **changes** for **single-phase** reactions."*

> **왜 이게 중요한가**: 셀 전압 곡선의 *기울어짐* 은 분극 탓이 아니라 **E_cell 자체가 기울어져서**
> 생길 수도 있다. 이 둘을 구분하지 못하면 "분극이 크다"는 오진을 하게 된다. 슬 31 에서
> 점선(E_cell profile)을 따로 그리는 이유가 정확히 이것이다.

### 3-4. 실물 3계로 확인 (슬 8–9)

| 계 | 반응 | E_cell 거동 | 덱 수치 |
|---|---|---|---|
| **Daniell (슬 8)** | Cu²⁺+2e=Cu (c) / Zn²⁺+2e=Zn (a) | `E_cell = (E⁰_Cu − E⁰_Zn) + (RT/2F)ln(a_Cu²⁺/a_Zn²⁺)`; 방전하면 a_Cu²⁺↓·a_Zn²⁺↑ → **감소** | **`E⁰_cell = 0.34 − (−0.76) = 1.1 V`** [덱] |
| **Ni-Cd (슬 9)** | Cd+2NiOOH+2H₂O → Cd(OH)₂+2Ni(OH)₂ | 반응물·생성물이 **전부 고체(a=1)** + H₂O 는 용매라 상수 → **완전히 평평** | `E⁰(−)=−0.81 V`, `E⁰(+)=0.47 V`, **`E⁰_cell = 1.28 V`** [덱] |
| **납축·리튬이온** | — | **감소** | 수치 없음 [덱 슬 9 진술만] |

- **슬 9 삽입 그림(외부 출처, 8× 재판독)**: y = Cell voltage/V (0.8–1.5), x = 0–100(방전 진행),
  점쇄선 **`E_cal = 1.44 V`**, 그 아래 **`E° = 1.30 V`**, 파란 굵은 선이 `E_cell`;
  방전곡선 라벨 **`2×I₁₀ / 10×I₁₀ / 50×I₁₀ / 100×I₁₀`** — **전류가 클수록 곡선이 아래로 처지고
  더 일찍 끊긴다**(분극의 시각적 정의).
- ⚠ **덱 내부 수치 불일치(사소, 출처 차이)**: 본문은 `E⁰_cell = 1.28 V`(표준전극전위 차),
  삽입 그림과 슬 34 는 `E_cell = 1.30 V`(ΔG 로부터). **0.02 V 차이는 표준값 출처가 달라서**이며
  오류로 단정할 근거는 없다. **우리가 인용할 일이 있으면 반드시 어느 쪽 유래인지 명시.**

### 3-5. 셀 분극의 세 항 정의 (슬 10)

**[덱]** `Cell polarization = η_c + η_a + iR_total`
- **η_c (cathodic overpotential)**: cathode 에서 전극 반응(**mass transfer + charge transfer**)을
  **활성화시키기 위해 추가로 필요한 전압**.
- **η_a (anodic overpotential)**: anode 에서 같은 뜻.
- **iR_total (iR voltage drop)**: 전류가 **닫힌 고리(closed loop)** 를 통해 흐를 때
  저항에 의한 IR drop 을 **넘어가야 하므로** 생기는 현상.

> **[STT 15:00–16:05]** 이 구간의 STT 는 **과전압을 전극 반응 층, iR 을 회로 층**으로 갈라
> 놓고 시작한다 (우리 의역 — 문구는 음성 미확인). 이 층 구분이 뒤(슬 23, 슬 47)에서
> 그대로 요약 문장이 된다.

### 3-6. 전류 = 반응속도 (슬 11) — 이 튜토리얼의 축

**[덱]**
```
Q = nF·N                (N = 생성된 R 의 몰수, n = 전자수, F = 9.6485×10⁴ C/equiv.)
i = dQ/dt = nF·dN/dt    ⇒  Rate (mol/s) = dN/dt = i/(nF)
```
- `Current (i) ∝ reaction rate`
- `High-rate charging = High-current charging`
- `A constant-current charging: the charging rate is constant.`
- **[STT 16:05·17:10]** STT 문자열에서 **전류 = 반응속도**라는 등가가 세 번 반복된다
  (반복 횟수는 문자열에서 셀 수 있다. 문구·어조는 음성 미확인이라 옮기지 않는다).

> **여기가 사슬의 관절이다.** 이 등가 덕분에 이후 모든 논증이 "속도를 올리려면 무엇이 필요한가"
> 라는 **화학반응속도론 언어**로 전개된다 — 전압은 속도의 손잡이가 된다.

### 3-7. 전극반응은 직렬 2단계 (슬 12)

**[덱]**
- charge transfer 는 **전자 터널링**으로 일어나고, **터널링 속도 ∝ e^(−d)** (d = 거리).
- ⇒ **전기화학 반응은 전극 표면 근처에서만 일어난다**.
- ⇒ 멀리 있는 반응물은 표면까지 와야 한다 = **mass transfer 가 필요**.
- 두 단계는 **직렬**이므로 **느린 쪽이 전체 속도를 결정**하고, 그 느린 쪽의 속도가 **전류로 나타난다**.
  - `charge transfer ≪ mass transfer` → 전체 속도 = charge transfer rate
  - `mass transfer ≪ charge transfer` → 전체 속도 = mass transfer rate

### 3-8. 평형에서는 모든 속도가 0 (슬 13) — 과전압의 존재 이유

**[덱]** 반쪽전지의 평형전압 `E_eq` 에서:
- mass transfer(확산) rate = 0
- charge transfer rate = 0
- 전체 반응속도 = 0 → **전류 = 0**

⇒ **평형에 있는 셀은 충전도 방전도 안 된다.** 전류를 흘리려면 전극 전위가 `E_eq` 를 **벗어나야** 하고,
그 벗어난 양이 **과전압(overpotential)** 이다.
```
[덱 슬 13]  E_cathode = E^c_eq + overpotential(η_c)   ,  E_anode = E^a_eq + overpotential(η_a)
[덱 슬 23·24] E^c = E^c_eq − η_c   ,  E^a = E^a_eq + η_a
```
⚠ **덱 내부 부호 표기가 흔들린다** — 슬 13 은 부호를 η 안에 흡수한 표현이고, 슬 23/24 가
**부호까지 드러낸 정본**이다(cathode 는 더 음으로, anode 는 더 양으로). **인용할 땐 슬 23/24 를 쓴다.**

### 3-9. 왜 평형에서 전하이동 속도가 0인가 (슬 14–17) — Butler–Volmer

**(a) 속도상수의 지수 의존 [덱 슬 14]**
```
Charge transfer rate = k′[O]_s[e] = k[O]_s ,     k ∝ e^η ,     η = |E_appl − E_eq|
```
`E_eq` 는 계가 정해지면 **상수**, `E_appl` 이 **우리가 조종하는 변수**. ⇒ **전류는 E_appl 로 지수적으로 조종된다.**

**(b) 두 방향 전류의 차 [덱 슬 15–16]**
```
i_net = i₀ [ e^(−αFη/RT) − e^((1−α)Fη/RT) ]          (Butler–Volmer)
i₀ = F·A·k⁰·C_O*^(1−α)·C_R*^α                        (exchange current)
α = symmetry factor (0.3 ~ 0.7)
η_activation = E_appl − E_eq
```
- 덱의 예시 그림 수치: **`i₀ = 2.2 µA`**, **`E_eq = −0.11 V (vs. SCE)`** [덱 슬 15·16].
- **점선 `i_c`·`i_a` 는 "보이지 않는" 전류이고, 실선 `i_net` 만 측정된다.** [덱+STT 26:10]
- `E_appl < E_eq` → 환원 net, `E_appl > E_eq` → 산화 net; `E_appl = E_eq` → **net = 0**.

**(c) 활성화 과전압의 정의 [덱 슬 17]**
> **활성화 과전압 = charge transfer rate 를 올리기 위해 추가로 걸어주는 전극 전위.**
> 더 큰 전류를 원하면 더 큰 η_activation 이 필요하다.

### 3-10. 왜 평형에서 확산 속도가 0인가 (슬 18–19) — 농도 과전압

**[덱 슬 18]**
- 표면 근처의 물질전달 경로 3가지: **확산 / migration / mechanical convection**.
  - migration → **supporting electrolyte 가 충분하면 무시 가능**
  - mechanical convection → **고체 표면에서 유속 0 이라 무시 가능**
  - ⇒ **표면 근처의 물질전달은 사실상 확산뿐**.
- 확산속도 → 전류:
  ```
  D_O · (dC_O(x,t)/dx)|_(x=0)  ≈  D_O · [ C_O* − C_O(0,t) ] / Δx
  ```
- **평형에서는 `C_O* = C_O(0,t)`** ⇒ 기울기 0 ⇒ **확산속도 0**.
- 탈출법: `E_appl` 을 더 음으로 → `C_O(0,t)` 감소 → **농도구배 증가 → 확산속도 증가**.
  덱의 3연 미니그래프가 이 과정을 (평탄 → 구배 생김 → `C_O(0,t)≈0` 포화) 로 보여준다
  (`δ`, `Δx`, `ideal/real` 표기 포함).
- **[덱 슬 19]** **농도 과전압 = 확산속도를 올리기 위해 추가로 걸어주는 전위.**
  i–E 곡선이 **한계전류 `i_L,a`·`i_L,c` 로 포화**하고, 거기서 **η_conc → ∞**.
- **[덱 슬 19 요약]** *"At E_eq, both charge transfer rate and diffusion rate are zero.
  To speed up two processes, we need overpotentials."*

### 3-11. iR_total — 닫힌 고리 (슬 20–22)

**[덱 슬 21]**
```
i_c = |i_a| = i(electrolyte)      ← 고리 어디서나 같은 전류
```
- 전해질 안에서는 **이온이 migration 으로** 전류를 나른다(전해질 = ion-conducting **solution or solid**).
- 음전하 종은 반시계, 전류는 시계 방향.

**[덱 슬 22] 셧다운 — 이 원칙 하나로 유도되는 안전 기능**
- 분리막 = **porous PE film, 융점 135 °C**; 기공 속 전해액이 이온전도를 담당.
- `i_c = |i_a| = i_separator` 이므로 **`i_separator → 0` 이면 양쪽 전극 전류가 동시에 0**
  = 충·방전이 멈춘다.
- 덱에 Before/After 단면 SEM(− 전극 / 분리막 / + 전극) 이 붙어 있고, After 는 분리막이 녹아
  기공이 사라진 모습. (스케일바 `10` — **단위 판독 불가**, §1c)

### 3-12. 다시 합치기 — E_charge / E_discharge 완전 유도 (슬 23–27)

**[덱 슬 23] 왜 분극이 생기나 (2줄 답)**
1. `E_eq` 에서 전류가 0이므로, 일정 속도로 충전하려면 **anode·cathode 양쪽에 활성화 + 농도 과전압**이 필요하다.
   `E^a = E^a_eq + η_a` (더 양으로), `E^c = E^c_eq − η_c` (더 음으로).
2. 전류가 흐르려면 **closed loop 상의 모든 IR drop 을 넘어야** 한다.

**[덱 슬 24] graphite/LiCoO₂ 충전 회로**
```
(−) C₆ + xLi⁺ + xe → Li_xC₆        : Reduction, Cathode, ⊖ electrode
(+) LiCoO₂ → Li₁₋ₓCoO₂ + xLi⁺ + xe : Oxidation, Anode,  ⊕ electrode
i_a = i_anolyte = i_separator = i_catholyte = i_c
E_charge = (E^a − E^c)      ← "But, ??"
```

**[덱 슬 25] 빠진 항을 넣는다**
```
E_charge = (E^a − E^c) + iR_total
         = (E^a_eq + η_a) − (E^c_eq − η_c) + iR_total
         = (E^a_eq − E^c_eq) + η_a + η_c + iR_total
         = E_cell + cell polarization
R_total = R^a_circuit + R_anolyte + R_separator + R_catholyte + R^c_circuit
```

**[덱 슬 26] 두 얼굴의 E_cell — 이름이 바뀐다**

| | 식 | E_cell 정의 | 이름 | 뜻 |
|---|---|---|---|---|
| 방전 | `E_discharge = E_cell − cell polarization` | `E_cell = E^c_eq − E^a_eq` | **기전력 (emf)** | 완전지가 가질 수 있는 **최대 방전전압** |
| 충전 | `E_charge = E_cell + cell polarization` | `E_cell = E^a_eq − E^c_eq` | **열역학 분해전압** | 완전지 충전을 위한 **최소 전압** |

**[덱 슬 26 표]**

| | Graphite | LiCoO₂ |
|---|---|---|
| `E_eq` | **~ 0.2 V** | **~ 4.0 V** |
| Charge | cathode | anode |
| Discharge | anode | cathode |

- ⇒ `E_cell ≈ 4.0 − 0.2 =` **구두 ≈ 3.8 V** [STT 43:37] (덱에 3.8 은 인쇄돼 있지 않다).
- **[덱+STT]** 충·방전 때마다 anode/cathode 가 뒤바뀐다는 점 `[STT 43:37]`.
  ⚠ STT 에는 이것이 혼동되기 쉬운 지점이라는 **어조**가 붙어 있으나, 어조는 음성을
  들어야 발표자에게 귀속할 수 있어 옮기지 않았다.
- **[덱]** `Cell polarization = η_c + η_a + iR_total` — **전류가 커지면 커진다.**
  ⇒ `E_charge is larger for a higher i_charge` (슬 26) / `E_discharge is lower for a higher i_discharge` (슬 27).

### 3-13. 같은 분극, 두 가지 분해법 (슬 28) — ★ 혼동 주의

**[덱]** 같은 `cell polarization` 을 **두 방식**으로 쪼갤 수 있다.
```
분해 ①(전극별):    η_a          +  η_c
                    ↓                ↓
분해 ②(기구별):  η^a_act + η^a_conc   η^c_act + η^c_conc
                    ↓
      E_discharge = E_cell − ( η_activation(a+c) + η_concentration(a+c) + iR_total )
```
- **[STT 45:57]** ★ *"불행하게도 a, c 가 똑같아. 얘는 **anode/cathode** 인데 얘는 **activation/concentration**
  이야. 영어가 참 그렇게 나와요."* → §4A-A2.

### 3-14. 세 항이 전류에 따라 다르게 큰다 (슬 29–30)

**[덱 슬 29]** i–V 그림 3개, 기울기 = 1/저항:

| 항 | 기울기 | **지배 영역** |
|---|---|---|
| **활성화 과전압** (η^a_act + η^c_act) | `1/R_ct` (지수 → 저전류에서 곡선) | **저전류** |
| **농도 과전압** (η^a_conc + η^c_conc) | `1/R_mt` (한계전류로 포화) | **고전류** |
| **옴 iR drop** (`iR_total`) | `1/R_total` (직선) | **중간 전류** |

- (덱 오타: 첫 상자 `Activaton` — `Activation` 이어야 함.)
- **[덱 슬 30]** 같은 내용을 `x = Voltage(V)`, `y = Discharge current` 축의 **S자 곡선** 한 장으로:
  아래(a)=활성화 지배, 중간(b)=옴 지배, 위(c)=농도 지배. `E_cell` 은 왼쪽 점선, `Cell polarization` 은
  `E_cell` 과 곡선 사이의 **가로 화살표**.
- **[덱+STT 47:15–48:21]** 구두 설명도 같다: 저전류 쪽 모양은 (a) 를 닮았고, 고전류 쪽은 (c) 를 닮았고,
  중간은 직선(b) 이다.
- ⚠ **[STT 47:15]** STT 는 이 그림을 **실측 데이터로 지칭**한다 (우리 의역 — 문구 미확인).
  그러나 **덱 그림에는 축 눈금도 셀 정보도 출처도 없다** `[덱 30]`.
  ⇒ 덱 근거만으로 **도식으로 취급한다** (§7-3). 이 판정은 STT 와 무관하게 선다.

### 3-15. 결과 ① — 방전전압·용량·에너지가 동시에 깎인다 (슬 31–32)

**[덱 슬 31]** graphite/LiCoO₂ 셀의 **정전류(galvanostatic) 방전곡선**,
`0.2C / 0.5C / 1C / 2C / 4C`, x = Capacity 0–800 mAh, y = E_discharge 3.0–4.0+ V.
- 점선 = **E_cell profile**(분극 0 극한).
- **`Cell polarization = E_cell − E_discharge`** ← 그림에서 세로 간격으로 읽는 정의.
- 셀은 **discharge cut-off voltage(3.0 V)** 까지만 방전한다.
- 전류 증가(0.2C→4C) ⇒ 분극 증가 ⇒
  1. **방전전압 감소**
  2. **cut-off 에 더 일찍 도달 → 실제 방전 용량 감소**
  3. **실제 방전 에너지 감소** (= 방전전압 × 실제 용량, **두 인자 모두** 줄어든다)

**[덱 슬 32] 두 용량을 구별하라**

| 용어 | 정의 [덱] | 값 [덱] |
|---|---|---|
| **Dischargeable cell capacity** | 어떤 완전지가 방전을 통해 발현할 수 있는 **최대** 셀 용량 | **750 mAh** |
| **Actual discharged cell capacity** | 방전을 통해 **실제 발현한** 용량. **방전 전류 크기와 cut-off voltage 에 따라 다름** | cut-off 3.0 V 기준 **2C: 560 mAh**, **4C: 50 mAh** |

**[덱] 비교 막대**: `dischargeable 750 mAh` 짜리와 `600 mAh` 짜리가 **2C 에서 둘 다 560 mAh** 를 낸다.
→ §4A-A3.

### 3-16. 결과 ② — 열 (슬 33–36, 38–40)

**(a) 열역학적 기원 [덱 슬 33]**
```
ΔH = ΔG + TΔS
ΔG = −nF·E_cell   →  E_cell : electromotive force
ΔH = −nF·E_cal    →  E_cal  : calorific voltage, **imaginary** emf estimated from ΔH
```
- **ΔH** = 방출/흡수되는 **총 화학에너지**, **ΔG** = **전기에너지로 바꿀 수 있는** 부분,
  **TΔS** = 방전 시 흡수/방출되는 **열**.
- **[STT 56:35]** `E_cal` 은 "가상적인" 값 — **ΔG 전부를 전기로 바꿀 수 있다면 나왔을 기전력**.
  비교용 눈금일 뿐이다.

**(b) 실제 수치 — Ni-Cd [덱 슬 34]**

| | 방전 (2NiOOH+2H₂O+Cd → 2Ni(OH)₂+Cd(OH)₂) | 충전 (역반응) |
|---|---|---|
| ΔH | **−282 kJ/mol** (`E_cal = 1.44 V`) | **+282 kJ/mol** (`E_cal = −1.44 V`) |
| ΔG | **−256 kJ/mol** (`E_cell = 1.30 V`) | **+256 kJ/mol** (`E_cell = −1.30 V`) |
| TΔS | **−26 kJ/mol (exothermic)** | **+26 kJ/mol (endothermic)** |

- 방전: ΔH 중 ΔG 만 전기로 나가고 **남은 TΔS 는 열로** → **발열**.
- 충전: ΔH 만큼 필요한데 전기로는 ΔG 만 공급 → **모자란 TΔS 를 밖에서 받아온다** → **흡열**.
- `TΔS → Q_rev` : **reversible heat effect**.

**(c) 운전 중 총 발열 [덱 슬 35 방전 / 슬 36 충전]**
```
Q_total = Q_rev + Q_Joule
Q_rev   = ∫₀ᵗ (E_cal − E_cell) i dt          ,   ∫₀ᵗ i dt = −nF
Q_Joule = ∫₀ᵗ (E_cell − E_discharge) i dt = ∫₀ᵗ (η_a + η_c + iR_total) i dt   (방전)
Q_Joule = ∫₀ᵗ (E_charge − E_cell) i dt      = ∫₀ᵗ (η_a + η_c + iR_total) i dt   (충전)
```
| | 기원 | 부호 |
|---|---|---|
| **Q_rev** | **열역학** (TΔS) | 반응 방향 따라 **흡열도 발열도** 된다 |
| **Q_Joule** | **kinetic (셀 분극)** — 전류 의존 | **항상 발열** [덱 슬 35 `Exothermic`; 같은 취지 `[STT 1:02:07]` — 문구는 음성 미확인] |

- **[덱 슬 35]** `ΔG` = `i = 0` 일 때 전기로 바꿀 수 있는 **최대** 에너지.
  `i > 0` 이면 분극 → `Q_Joule` 이 그만큼을 갉아먹는다.
  **`Actually discharged energy = ΔH − Q_total`**.
- **[덱 슬 36]** 충전에서는 `ΔG` 가 **최소** 전기에너지이고, `i>0` 이면 분극만큼 **더** 넣어야 한다.

**(d) 셀이 식을 수도 있다 [덱 슬 38 — 준비된 Q&A 슬라이드]**
> **Q.** 방전하면 배터리가 뜨거워진다고들 하는데, 열 발생의 기원을 열역학·동역학으로 나눠 밝히고,
> 방전이나 충전 중에 온도가 **내려가는** 것이 가능한가?
> **A.** 열역학 기원 `Q_rev(=TΔS)` + 동역학 기원 `Q_Joule`(셀 분극).
> **가능하다 — `Q_rev`(흡열) > `Q_Joule`(발열) 이면.** 예: **VRLA 셀의 저전류 방전.**
> `낮은 전류 → 작은 분극 → 작은 Q_Joule`.

- **[덱 슬 39] 납축전지의 그림 논증**: 이 계는 `E_cell > E_cal` (즉 `ΔG` 면적 > `ΔH` 면적)라서,
  전기로 내보내는 양이 반응이 주는 양보다 크다 ⇒ **모자란 `TΔS` 를 주변에서 가져온다 = 흡열**.
  ⚠ 덱 문장은 *"The energy that can be converted into electric energy (ΔG) is larger than the
  available chemical energy (ΔH)"* — 부호 관례가 헷갈리게 쓰여 있다. **그림(빨간 `E_cell` 선이
  파란 `E_cal` 선보다 위)이 정본**이다.

**(e) 열폭주 [덱 슬 40]**
- 개시: **셀 온도 > 80–100 °C**; **SEI 가 LIB 의 가장 약한 지점**.
- 단계도(외부 그림): `Safe → 80–100 SEI layer breakup → 120 anode–solvent reaction →
  150–180 electrolyte decomposition → 200 O₂ release from cathode material and combustion → Flame/Fire/Explosion`.
- **내부단락 논증**: 정상 방전은 `R > 0` 이라 전류가 제한되지만, 단락이면 `R ≈ 0`
  → **고율 자가방전 → 분극 大 → `Q_Joule ≫ Q_rev`** → `Q_rev` 가 흡열이든 발열이든 상관없이
  온도가 빠르게 오른다 → 셀 부품 분해 → O₂ 방출 → 화재.
- 유발 요인: **내부단락 / 외부단락 / 과충전** (모두 셀 온도 80–100 °C 초과 유발) + **고온 노출**.

### 3-17. 결과 ③ — 충전 쪽 (슬 41)

**[덱]** `E_charge = E_cell + (η_a + η_c + iR_total)` 이므로 고율 충전에서:
분극↑ → `E_charge`↑ → **충전 cut-off 전압에 더 일찍 도달** → **충전된 용량이 작다**.
⇒ **"Cell polarization should be minimized for high-rate charging."**
그림은 충전곡선과 방전곡선을 위·아래로 놓고, `charging cut-off ≈ 4.0 V`, `discharge cut-off ≈ 1.7 V`,
x = Cell capacity 0–10 Ah 로 표시(예시 셀).

### 3-18. 처방 (슬 42–46) — 세 항을 각각 어떻게 줄이나

**(a) 활성화 과전압 [덱 슬 42]**
```
R_ct = RT / (i₀ F)          ← 기울기 1/R_ct 가 클수록 η_act 가 작다
i₀   = F·A·k⁰·C_O*^(1−α)·C_R*^α
```
⇒ **i₀ 를 키워라**: **① 전극 면적 A ② k⁰ 가 큰 전극 선택/표면 개질 ③ 반응물 농도 C**.

**(b) 농도 과전압 [덱 슬 43]**
```
R_mt  = RT / (nF · i_L,c)
i_L,c = 0.62 · nFA · D_O^(2/3) · C_O* · ω^(1/2) / ν^(1/6)        ← Levich (RDE) 한계전류
```
⇒ **i_L,c 를 키워라**: **① 전극 면적 ② 확산계수 D_O ③ 반응물 농도 C_O* ④ 동점성계수 ν 를 낮춰라.**
- ★ **[덱]** *"solid-state bulk diffusion is **10³~10⁵** slower than in solution"* (6× 확정).
- ⛔ 구두는 ν 도 "커야 한다"고 말한 것으로 들린다 [STT 1:15:00] → **불일치, 덱 채택** (§5-B).

**(c) iR_total [덱 슬 44]**
```
R_total = R_separator + R_solution + R_circuit + R_SEI + R_others
일반적으로  R_separator > R_solution > R_circuit        (⇒ non-divided cell 이 유리)
R_separator = l / (κ_separator · A)     ,     R_solution = l / (κ_solution · A)
```
⇒ **κ 최대화 · 전극 면적 최대화 · 분리막 박막화 · 전극 간격 최소화.**
- ★★ **[덱, 파란 강조]** **"What really matters is not the conductivity but the resistance !!"**
  (같은 취지가 `[STT 1:17:17]` 에도 있으나 문구는 귀속하지 않는다) → §4A-A1.

**(d) 그 처방이 실물에 구현된 예 [덱 슬 45] — 젤리롤**
- 원통형 Li-ion 셀 분해도(safety vent, PTC device, gasket, separator film, +/− electrode plate, casing).
- **A(마주보는 전극 면적)가 극단적으로 크고, 전극 간 간격 l 이 매우 짧다.**
- ⇒ *"R_separator 와 R_solution 은, 비수계 전해질이라 κ 가 나빠도, 그렇게 크지 않다."*
- **[STT 1:18:33]** *"리튬이온전지는 (고전압 때문에) 수용액 전해질 대비 전도도가 나빠. 얘가 작으니까
  얘들(저항)이 클 수 있잖아. 그러나 얘가 작더라도 **면적을 키웠단 말이죠**."*

**(e) R_SEI [덱 슬 46]**
```
R_total = R_separator + R_solution + R_electrode + R_SEI
```
- `R_SEI` = SEI 층을 통한 **이온 전도**에 관련된 저항.
- **[덱]** *"Frequently, R_SEI is larger than other resistances in **aged** cells: SEI layer becomes
  thicker or more compact."*
- **[덱]** *"In particular, when LIB cell is exposed to **high temperature**, electrolyte decomposes to
  produce thicker or compacter SEI layer."*
- **[STT 1:20:52]** *"방금 만든 셀은 별로 문제가 안 되지만, 오래된 셀·특히 고온 노출이 많았던 셀은
  SEI 저항이 상당히 크다."* → §4A-A4.

### 3-19. 요약 (슬 47–48)

**[덱 슬 47] Why cell polarization?**
- 충·방전 모두 전류가 **closed-loop** 를 따라 흐른다.
- 두 반쪽전지에서 **charge transfer 와 diffusion rate 를 올리려면 과전압**이 필요하다.
- 그리고 closed loop 를 따라 **iR drop 을 넘어야** 한다.

**[덱 슬 47] Adverse effects** — 방전전압/충전전압 · **실제** 방전용량/충전용량 ·
**실제** 방전 에너지 · **열손실에 의한 에너지 효율**.

**[덱 슬 48] How to minimize** — ① k⁰ 큰 전극 선택 ② 반응물 농도 ③ **전극 면적; 더 작은 입자**
④ 물질전달 속도 ⑤ **이온전도도 κ(분리막·용액) 최대화** ⑥ 전극 간격 최소화 ⑦ 분리막 박막화
⑧ **표면막(SEI) 박막화**.
**[덱]** 참고서: **"전기화학" 5판, 오승모 저 (자유아카데미, 2025)**.

---

## 4. 전문가 관찰 · 가설 — 두 갈래로 나눈다

> **⛔ 이름을 낮췄다** (2026-08-25 codex E): 이전 판의 "전문가 판단" 은 **판단이 확정된
> 것처럼** 읽힌다. 우리는 음성을 듣지 않았고 여기 문장은 전부 STT 문자열에서 왔다.
>
> **직접 인용을 전부 걷어냈다.** "wording 만 STT" 라고 적는다고 해서 STT 에만 있는
> **강조와 양태**(*"진짜 중요한 건"*, *"저도 그랬고"*)까지 살리면 안 된다 —
> 강조도 의미의 일부이고, 그건 음성을 들어야 발표자에게 귀속할 수 있다.
>
> 그래서 §4 를 둘로 나눈다:
> **4A** 덱이 **독립적으로** 지지하는 것 (내용 인용 가능, 문구는 우리 의역) ·
> **4B** STT 에만 있는 것 (**내부 가설 생성만**, 발표자 주장으로 인용 금지).
>
> 공개 질의응답은 없었다 (좌장이 쉬는 시간으로 넘김 [STT 1:22:59]).

### 4A. 덱이 독립적으로 지지하는 실무자 추론

```json
{"claim_source": ["deck"], "wording_source": "editorial_paraphrase",
 "audio_verified": false, "direct_quote_allowed": false,
 "allowed_use": "deck_supported_paraphrase"}
```

#### A1. ★★ 셀 수준의 설계량은 전도도가 아니라 저항이다 `[덱 44]` `[STT 1:17:17]`

**덱 슬 44 의 파란 박스에 인쇄돼 있다**: *"What really matters is not the conductivity
but the resistance !!"* — 이건 덱 원문이라 그대로 인용해도 된다.
우리 의역: **셀 수준에서는 전도도 자체보다 형상(`l`·`A`)까지 포함한 저항이 직접적인 설계량이다.**
덱 슬 45(젤리롤)가 실물 예 — 비수계 전해질의 낮은 κ 를 `A↑`·`l↓` 라는 **기하**로 상쇄한다.

- **우리에게 무슨 뜻인가** ★★: 우리 헤드라인 *"modelc(Cl-rich)가 comp1 보다 D 2.6× 빠르다"* 는
  **κ 축의 진술**이고 셀 분극에 대한 진술이 아니다. `R_SE = l/(κ·A)` 에서 우리는 κ 만
  건드리고 `l`·`A` 는 손대지 않는다. ASSB 에서 `l`(SE 층 두께)은 σ 못지않은 설계 변수이고,
  그건 우리 축이 아니라 **DEM/미세구조 축**이다.
- **다리 판정** (codex D 기준): 허용 — *"원자수준 이온전도도는 셀 ohmic polarization 을
  구성하는 **한 입력 변수**다."* 금지 — *"우리 bulk σ 향상이 실제 셀 분극 감소를 **입증**한다."*
- **확인 가능성**: **부분** — σ 와 문헌의 `l` 을 곱해 면적비저항(Ω·cm²)을 어림할 수는 있으나
  **새 계산이 아니라 산술**이고, 전제(치밀도 100 %·GB 저항 0·접촉 완전)가 비현실적이라
  **상한값**으로만 유효하다.

#### A2. 같은 총량의 두 가지 분해 — `a`,`c` 첨자가 겹친다 `[덱 28]` `[STT 45:57]`

덱 슬 28 이 같은 분극을 **전극별**(anode/cathode)과 **기구별**(activation/concentration)
두 방식으로 분해해 나란히 보여준다 (§3-13). 첨자 `a`·`c` 가 두 분해에서 서로 다른 뜻이다.

- **왜 중요한가**: `η_a + η_c` 를 "활성화 + 농도"로 읽으면 **전극 2개가 사라지고**,
  `η_act + η_conc` 를 "anode + cathode" 로 읽으면 **기구 구분이 사라진다.**
- **우리에게**: 문헌 digest 를 옮길 때 `η_a` 가 어느 분해인지 매번 확인해야 한다.
  임피던스 논문의 `R_ct`(활성화 계열)와 셀 논문의 `η_anode`(전극 계열)는 다른 축이다.
- **확인 가능성**: 표기 규약 문제 — 우리 `comparison_vs_ours.md` 어느 행에도 η 분해가
  없으므로 **현재 오염 없음**. 앞으로 셀 데이터가 들어올 때 적용.

#### A3. 최대 발현 용량과 실제 발현 용량은 다른 스펙이다 `[덱 32]` `[STT 54:14]`

덱 슬 32 의 두 막대가 근거다: **750 → 560** vs **600 → 560 mAh**.
낮은 정격이라도 율특성이 좋으면 **같은 실제 발현 용량**에 도달한다.

- **우리에게** ★: 우리 캠페인에도 **같은 형태의 구분**이 필요하다. `σ_ion`(재료 최대 성능)
  축에는 정교하지만(MLIP-MD 다중시드·Arrhenius 3점), 그 σ 가 **셀에서 얼마나
  realize 되는가**(`R = l/(κA)`, 접촉·GB·기공)에는 계산이 **0** 이다 —
  `comparison_vs_ours.md` §H "시트/펠릿 microstructure σ" 행이 이미 그 공백을 적어 두었다.
- **확인 가능성**: **미확인** — 우리 db 에 device σ 대응값이 없다. 외부로는
  `[KimICCF]`(device σ ≠ bulk σ), `[YMLee26-DTBL]` 덱의 소재 5.4×10⁻⁴ → 셀 내부
  7.9×10⁻⁷ S/cm(≈3자릿수 강하)가 같은 취지.
- ⚠ **"다들 소홀했다 · 저도 그랬고" 라는 자기반성은 여기 없다** — 그건 STT 에만 있고
  태도 진술이라 4B 로 내렸다.

#### A4. 노화 셀에서는 SEI 저항이 무시 못 할 항이 된다 `[덱 46]` `[STT 1:19:25·1:20:52]`

덱 슬 46 이 `R_SEI` 를 셀 저항 항목으로 세운다. STT 는 노화·고온 이력 셀에서 이 항이
커지는 이유로 SEI 가 **두꺼워지거나 치밀해지는 것**을 든다 (이 인과 부분은 덱 미확인).

- **왜 중요한가**: 신품 셀 임피던스로 SE 를 평가하면 이 항이 안 보인다. **수명 축**에서 지배적.
- **우리에게** ★: 우리는 계면에서 **무엇이** 생기는지(`Li₃PS₄ + LiCl + S`)와 **몇 V 에서**
  생기는지(2.256 V)는 계산하지만, **얼마나 두꺼워지는지·저항이 얼마인지는 전혀 계산하지 않는다.**
  `comparison_vs_ours.md` §H "Li‖SE 계면 반응 MD(SEI 두께·성장 시간)" 행과 정확히 같은 구멍.
- **확인 가능성**: **미확인**. `sei_products.json` 은 결정상 band gap(전자 절연성)만 본다.
  **이온 저항률은 0건.**

### 4B. STT 에만 있는 전문가 가설 — ⛔ 내부 가설 생성 전용

```json
{"claim_source": ["stt"], "wording_source": "editorial_paraphrase",
 "audio_verified": false, "direct_quote_allowed": false,
 "allowed_use": "hypothesis_generation_only"}
```

> ⛔ **아래를 발표자의 주장으로 인용하지 않는다.** 원고·발표·canonical 어디에도 넣지 않는다.
> 음성을 확보해 **해당 구간을 다시 들은 뒤에만** 4A 로 승격한다 (구간별로, 일괄 승격 금지).

| | 가설 (우리 의역) | 근거 | 우리 쪽 함의 |
|---|---|---|---|
| **B1** | 평형전압은 반쪽전지에 대한 개념이고, 풀셀에는 그 말이 성립하지 않는다 | `[STT 20:22]` 만 · 덱 미확인 | 우리 산화 onset 2.256 V·환원 한계 1.242 V·OCV 1.717 V 는 전부 **vs Li/Li⁺ 반쪽전지 전위**다. "셀 전압"과 같은 축에 놓으면 **기준전극이 다른 두 수를 뺀 셈**. ⇒ 원고 문장 점검 항목 (§6-B) |
| **B2** | 분야가 최대 발현 용량 쪽에 자원을 쏠아 왔고 실제 발현 용량은 상대적으로 소홀했다 | `[STT 54:14]` 만 · **태도·자기반성 진술** | A3 와 같은 방향이지만 **분야 전체에 대한 평가**라 덱으로 뒷받침되지 않는다. 우리 축 배분을 되묻는 **질문**으로만 쓴다 |

### 4C. 판독 메타 — 구술이 얇은 구간 (인용이 아니라 coverage 정보)

발표 진행에 대한 메타 정보다. 주장이 아니므로 4A/4B 어디에도 넣지 않는다.

- `[STT 48:21]` 시간 압박 언급 → 슬 29–32 구간이 빨라진다.
- `[STT 1:12:43]` 5분 남음 → **슬 42–48(처방 전체)이 급가속**된다.
- `[STT 1:05:18]` 슬 37(Energy efficiency)은 **명시적으로 건너뜀**.
- **판단**: 이 덱에서 **처방부(슬 42–46)가 구술로 가장 얇다.** 그런데 §6 의 접점은 대부분
  거기 있다 ⇒ **처방부는 [덱] 을 정본으로 읽어야 하고 [STT] 로 보강할 게 적다.**
  (음성을 확보하면 **이 구간부터** 재청취한다.)

---

## 5. STT 교정표

> 규율: **고치지 않고 인용하면 없는 말을 만든 것**이 된다. 도구가 15건을 후보로 띄웠고,
> 아래는 **우리가 슬라이드로 대조해 확정한 것 + 확정 못 해 추정으로 남긴 것**이다.

### 5-A. 확정 (슬라이드로 대조 완료)

| 들린 것 (STT) | 확정 | 근거 슬라이드 |
|---|---|---|
| `오승목` | **오승모** | 슬 1 |
| `셀 코리라리제이션` · `셀 콜라리제이션` · `세레콜라겐` · `셀 콜라겐` · `세 폴레틴` · `셀 폴라리스` · `셀프롤라이즘` · `세 코리라` · `세포라인선` | **cell polarization (셀 분극)** | 슬 2·10·20·47 |
| `a미타 c` | **η_a + η_c** | 슬 2 |
| `IR 포탈` · `아이알 브라우` · `알랑 포탈` · `IR 드럼` · `IR 드락` · `IR 토탈` | **iR_total / IR drop** | 슬 2·10·20 |
| `2세` · `이 셀` · `이색` · `2세기` · `e셀` | **E_cell** | 슬 2·3·7·26 |
| `큐줄` · `q 줄` · `추줄` · `퀴즈` · `큐순` · `큐즐` | **Q_Joule** | 슬 2·35·36 |
| `큐 리버서블` · `큐 리버소블` · `큐 이버서블` · `q 리버스` | **Q_rev (reversible heat)** | 슬 35·38 |
| `너 시리케이션` · `내스틱 뮤지션` · `노런스 디케이션` · `발음식` | **Nernst equation** | 슬 3·4·5·6 |
| `투 페이지 리액션` | **two-phase reaction** | 슬 5 |
| `싱글 페이지 리액션` | **single-phase reaction** | 슬 6 |
| `인터컬레이션 디인터퍼레이션` | **intercalation / de-intercalation** | 슬 6 |
| `90사이트` · `브레파이트` | **graphite** | 슬 24 (`C₆ + xLi⁺ + xe → Li_xC₆`) |
| `아이언니 파이 파스테이트` | **iron phosphate (FePO₄)** | 슬 5 |
| `데니엘` · `이스트` | **Daniell cell** | 슬 8 |
| `니켈 카드뮴 셀` · `니켈 카트색` · `니켈 카드세` | **Ni-Cd cell** | 슬 9 |
| `매스트렌스퍼` · `에스 트랜스퍼` · `매스랜스가` | **mass transfer** | 슬 12·13 |
| `차지 트랜스퍼` · `차디리데스` · `좌디 트랜스` · `처리 트랜스퍼` | **charge transfer** | 슬 12·13·14 |
| `일렉트론 터미널링` | **electron tunneling** | 슬 12 |
| `버트롤볼레비테이션` · `버트럴 로케이션` · `버드럴레이케이션` · `버틀러 볼모 이큐에이션` | **Butler–Volmer equation** | 슬 15·16 |
| `익스프렌셜` · `익스퍼레지` | **exponential** | 슬 14 |
| `액티베이션 오버포턴셜` · `애플레이션 오버 편전` · `액티베이션 오버 탄성` · `액티비션 오크 단열` | **activation overpotential** | 슬 17 |
| `칸센처에` · `콘텐츠웨이션 로터` · `컨센트레이션 오버까지` | **concentration overpotential** | 슬 19 |
| `마이그레이션` | **migration** | 슬 18·21 |
| `미케니컬 컨벡션` / `컨백션` (도구가 *convection vs conversion* 로 띄운 건) | **mechanical convection** — **convection 으로 확정** | 슬 18 (`Diffusion, migration and mechanical convection`) |
| `서포팅 일렉트로라이트` | **supporting electrolyte** | 슬 18 |
| `클로즈` · `끌로드` · `크로 이러면서` | **closed loop** | 슬 20·21 |
| `세퍼레이트` · `세프레드` · `세플레이트` · `셀프라이트` | **separator** | 슬 21·22·44 |
| `셧다운` · `메트 다운` | **shut-down / melt down** | 슬 22 |
| `포로스콜레트랜스분` | **porous polyethylene(PE) film** | 슬 22 |
| `135도` | **135 °C** | 슬 22 |
| `에놀라이트` · `캐롤라이트` | **anolyte / catholyte** | 슬 24·25 |
| `열적 분해절압` | **열역학 분해전압 (thermodynamic decomposition voltage)** | 슬 26 |
| `일렉트로 모티 포스` · `에모리 원파` | **electromotive force (emf)** | 슬 26·27 |
| `에로드 캐버드` | **anode & cathode (a, c 첨자)** | 슬 28 |
| `캘러리디폴트` · `피티 모델` · `이 탭` · `이 캡` | **E_cal (calorific voltage)** | 슬 33 |
| `델타h` · `델드h` · `대타 진` · `델타 지` · `델타처` | **ΔH / ΔG** | 슬 33·34 |
| `썸모롤레이` | **thermal runaway** | 슬 40 |
| `인터넷 쇼트` · `내력당` | **internal short (내부 단락)** | 슬 40 |
| `압축 전지` · `납축전지` · `낙소리` | **납축전지 (lead-acid, VRLA)** | 슬 38·39 |
| `갤버` | **galvanostatic** | 슬 31 |
| `서로프` · `커더프` · `코더플` | **cut-off** | 슬 31·41 |
| `750ml 안피아` · `750ml 패` | **750 mAh** | 슬 32 |
| `20에서 500 60` · `4시` · `40억` | **2C 에서 560 mAh · 4C** | 슬 32 |
| `맥스 미시 차드 셀캔` | **max dischargeable cell capacity** | 슬 32 |
| `액츄얼 디슈트 세케` · `액트 미트라스` | **actual discharged capacity** | 슬 32 |
| `RCT` · `아스트` · `초기 트랜스퍼 저항` | **R_ct (charge transfer resistance)** | 슬 42 |
| `체인지 카운트` · `아이한테` · `다이렉트` | **i₀ (exchange current)** | 슬 42 |
| `케이아트` · `펠란트` · `페란트` · `스탠나드 웨이드 카스턴트` | **k⁰ (standard rate constant)** | 슬 42 |
| `RMD` · `RNT` · `RNG` · `rat` · `내 트랜스퍼 저항` | **R_mt (mass transfer resistance)** | 슬 43 |
| `RLS` · `리미티드 클럽` | **i_L (limiting current)** — ⚠ STT 가 `R` 로 시작하는 기호처럼 들려주지만 덱은 `i_L,c` | 슬 43 |
| `킬라티 비스코시키` | **kinematic viscosity (ν)** | 슬 43 |
| `카파` | **κ (ionic conductivity)** | 슬 44 |
| `리피니어들의 타입 세이` · `리트리언설` | **Li-ion cell (jelly-roll type)** | 슬 45 |
| `런 hot 일렉트론` | **non-aqueous electrolyte** | 슬 45 |
| `수용성 전화` | **수용액(aqueous) 전해질** | 슬 45 |
| `sei` · `SDI` · `SI층` · `STI` · `sig` | **SEI (solid electrolyte interphase)** | 슬 46 |
| `모어 컴팩트` | **more compact** | 슬 46 |
| `볼티지 곱하기 캠패시` · `케페시트` | **voltage × capacity** | 슬 2 |

### 5-B. ⛔ 불일치 — 어느 쪽도 그대로 인용하지 않고, 불일치 자체를 기록

| # | 항목 | [덱] | [STT] | 판정 |
|---|---|---|---|---|
| **1** | **동점성계수 ν 의 방향** (슬 43) | `i_L,c = 0.62nFAD_O^(2/3)C_O*ω^(1/2)/**ν^(1/6)**` → ν 는 **분모** → 덱 처방 **"Minimize ν (kinematic viscosity; solution viscosity)"** | *"면적 커야 돼, 확산계수, 농도, 그다음에 **kinematic viscosity 이런 것들이 커야지만**"* [STT 1:15:00] | ⛔ **덱 채택.** 식에서 ν 는 분모이므로 **작아야** i_L,c 가 커진다. 구두는 앞 항목들("커야 한다")에 ν 까지 묶어 말한 **실언**이거나 STT 붕괴로 보이나, **구분 불가** — 그래서 불일치로 남긴다 |

### 5-C. 구두 근사·실언 (⛔ 아님, 그러나 [STT] 숫자를 쓰면 안 되는 실증)

| 항목 | [덱] | [STT] | 처리 |
|---|---|---|---|
| Ni-Cd ΔH (슬 34) | **−282 kJ/mol** | 구두 ≈ **−280** [STT 57:42] | **덱 사용.** 구두는 반올림 |
| Ni-Cd ΔG (슬 34) | **−256 kJ/mol** | 구두 ≈ **−250** [STT 57:42] | **덱 사용.** 구두는 반올림 |
| 충전 TΔS (슬 34) | **+26 kJ/mol** | *"방전에서 −26 이면 충전에서 **플러스 1**"* [STT 58:46] | **덱 사용.** 명백한 실언 또는 STT 절단 |
| 열폭주 개시온도 (슬 40) | **> 80–100 °C** | *"80도 100도를 넘어가면… **100도**를 넘으면"* [STT 1:10:17] | **덱 사용.** 사실상 일치, 구두가 범위를 상단으로 단순화 |
| graphite/LiCoO₂ E_cell (슬 26) | 표에 `~0.2 V`, `~4.0 V` 만 | 구두 ≈ **3.8 V** [STT 43:37] | **`구두 ≈ 3.8 V` 로 표기.** 덱에 3.8 은 인쇄돼 있지 않다 |

### 5-D. 추정 (슬라이드로 확정 못 함 — **인용 금지**)

| 들린 것 | 추정 | 왜 확정 못 했나 |
|---|---|---|
| `인젤리티 월드 사이드` [STT 11:00] | **empty Li⁺ storage site** (슬 6 의 `< >`) | 음절 대응이 약하고, 슬 6 인쇄어와 1:1 로 못 맞춤 |
| `에너지가 오고 현실` [STT 44:50] | **anodic and cathodic (overpotential)** | 슬 28 문맥상 그럴듯하나 음절 붕괴가 심함. 같은 취지의 확정 발화는 [STT 45:57] 에 따로 있으니 **그쪽을 인용** |
| `익자적인 커런트` [STT 31:52] | **limiting current** | 슬 19·43 에 `i_L` 이 있으나 이 문장 시점의 슬라이드가 슬 18 이라 대응 불확실 |
| 좌장의 오승모 약력 [STT 00:00–00:06] | (서울대 화학생물공학부 재직 → 연세대) | STT 붕괴가 심해 학위·연도를 하나도 못 읽음. **약력은 덱·공식 프로필로만** |

### 5-E. 덱 자체의 오류 (우리 전사 오류가 아님 — 고배율 확정)

| # | 슬 | 인쇄된 것 | 옳은 것 | 확인 배율 |
|---|---|---|---|---|
| 1 | 1 | `Department of Battery **Conflation** Engineering` | **Convergence** (배터리융합공학과) | **8×** |
| 2 | 29 | `**Activaton** overpotential` | `Activation` | 1.35× (명백) |
| 3 | 39 | *"The energy that can be converted into electric energy (ΔG) is larger than the available chemical energy (ΔH)"* | 부호 관례상 혼동을 부르는 문장. **그림(E_cell 선 > E_cal 선)이 정본** | 1.35× |

### 5-F. 덱 내부 표기 흔들림 (오류라기보다 **일관성 결여** — 인용 시 슬 번호 명시 필수)

| 항목 | 어디서 어떻게 |
|---|---|
| **η 부호** | 슬 13 `E_cathode = E^c_eq + η_c` ↔ 슬 23·24 `E^c = E^c_eq − η_c`. **슬 23/24 가 정본** |
| **분극 항 순서** | 슬 2 `η_a + η_c + iR` ↔ 슬 10·26 `η_c + η_a + iR`. 합이라 무해 |
| **`R_total` 분해가 3가지** | 슬 25 `R^a_circuit + R_anolyte + R_separator + R_catholyte + R^c_circuit` / 슬 44 `R_separator + R_solution + R_circuit + R_SEI + R_others` / 슬 46·48 `R_separator + R_solution + R_electrode + R_SEI`. **모순은 아니지만 항 이름이 다르다** — 인용할 땐 어느 슬라이드인지 밝힌다 |
| **Ni-Cd E_cell** | 슬 9 본문 `E⁰_cell = 1.28 V`(E⁰ 차) ↔ 슬 9 삽입그림·슬 34 `1.30 V`(ΔG 유래) |

---

## 6. 우리 캠페인과의 접점

> **결론 먼저**: **물성 4축(A 이온전도 / B 산화안정 / C 기계 / D 전자구조)에 넣을 *수치*는 0 건이다.**
> 층위가 다르다 — 우리는 재료 내부(Å–nm), 이 발표는 소자(µm–cm, 실동작 전류).
> 그러나 **개념 다리 4개는 진짜다.** 억지로 만든 것이 아니라, 발표가 **우리 계산량이 소자에서
> 어느 항으로 들어가는지를 명시적으로 지정**하기 때문이다.

### 6-A. ★★ 다리 ① — 우리 `σ_ion` 이 셀에 들어가는 **유일한 통로**: `R_SE = l / (κ · A)` → `iR_total`

```
[우리 계산]                            [이 발표의 항]
MLIP-MD(UMA-s-1p1) → D(T) → Arrhenius → Ea
D → Nernst–Einstein(Haven=1) → σ_ion  ≡  κ_separator   ────┐
                                                            ├── R_separator = l/(κ·A)  [덱 슬 44]
SE 층 두께 l  ── 우리 계산에 **없음** ──────────────────────┤
전극 면적 A   ── 우리 계산에 **없음** ──────────────────────┘
                                        → iR_total → cell polarization → E_charge/E_discharge
                                        → Q_Joule = ∫(η_a+η_c+iR)i dt (항상 발열)
```

- **ASSB 에서는 이 다리가 특히 직접적이다.** 액체 셀에서는 분리막(PE)과 전해액이 따로지만,
  ASSB 에서는 **SE 가 곧 분리막이자 catholyte** 다. 즉 우리가 계산하는 그 κ 가
  `R_separator` 와 `R_catholyte` **양쪽에 동시에** 들어간다.
- **그래서 이 발표의 경고가 우리 문장에 그대로 걸린다** `[덱 44]`:
  **"What really matters is not the conductivity but the resistance !!"** (덱 인쇄 원문).
  *"modelc 가 comp1 대비 D 2.6×"* 는 **κ 축의 진술**이지 셀 분극 축의 진술이 아니다.
  같은 κ 라도 `l` 을 절반으로 줄이면 `R` 이 절반이 된다 — **그건 우리 축이 아니라 공정/미세구조 축**이다.
- **젤리롤 논증 [덱 슬 45]** 이 이 점의 실증이다: 비수계 전해질은 κ 가 나쁜데도,
  A 를 극단적으로 키우고 l 을 줄여서 R 을 감당 가능한 값으로 만든다.
  ⇒ **ASSB 에서 우리가 κ 로 벌 수 있는 이득의 상한**을 판단하려면 반드시 `l/A` 를 같이 말해야 한다.
- ⚠ **우리 σ 는 상한이다**: 주기셀 벌크 MLIP-MD 값이므로 **GB·기공·접촉저항·tortuosity 가 0** 인
  이상 조건이다. 실제 `κ_effective` 는 그보다 낮고, 그 차이가 `R_others` 로 나타난다.
  (`comparison_vs_ours.md` §H "시트/펠릿 microstructure σ" · `[KimICCF]` device σ ≠ bulk σ ·
  `[YMLee26-DTBL]` 3자릿수 강하와 같은 축.)

### 6-B. ★★ 다리 ② — 우리 ESW onset 은 **셀 전압이 아니라 전극 전위**와 비교해야 하고, 고율이면 더 가혹하다

**발표의 유도 [덱 슬 23–25]**:
```
E^a = E^a_eq + η_a        (anode 는 평형보다 **더 양의 전위**를 실제로 겪는다)
E^c = E^c_eq − η_c        (cathode 는 **더 음의 전위**)
E_charge = E_cell + (η_a + η_c + iR_total)
```
**우리에게 무슨 뜻인가** ★
1. 우리 `산화 onset 2.256 V (vs Li/Li⁺)` 는 **반쪽전지 전위 축**의 수다 (§4B-B1).
   셀 공칭 전압(예: 4.2 V)과 **같은 축이 아니다** — 비교하려면 양극의 `E^c_eq` 로 환산해야 한다.
2. 더 중요한 점: **충전 중 양극(산화가 일어나는 쪽)의 실제 전위는 `E^a_eq + η_a` 로 평형보다 높다.**
   ⇒ **고율 충전일수록 SE 가 겪는 산화 구동력이 공칭보다 커진다.**
   우리 grand-potential ESW 는 **평형(η=0) 열역학**이므로, **고율 조건은 우리 계산보다 항상 불리한 쪽**이다.
   ⇒ 우리 문장은 *"2.256 V 이상에서 열역학적으로 산화된다(평형 기준). 실제 셀에서는 anodic
   overpotential 만큼 더 일찍 그 조건에 도달한다"* 로 쓰는 것이 정확하다.
3. **반대로 iR 은 안전 방향이 아니다**: `iR_total` 은 셀 단자 전압에만 실리고
   전극 전위 자체를 밀지 않는 성분이 섞여 있으므로, **η 와 iR 을 뭉뚱그려 "다 더 가혹하다"고 쓰면
   과장**이 된다. 밀어주는 것은 **η_a** 다.

### 6-C. 다리 ③ — 우리 `Ea`/`NEB` 는 **농도 과전압 가지**로 들어가지, **활성화 과전압 가지가 아니다**

발표는 두 가지를 **끝까지 분리**한다 [덱 슬 42 vs 슬 43]:

| 가지 | 지배 물리량 | 우리 계산 |
|---|---|---|
| **활성화 과전압** | `R_ct = RT/(i₀F)`, `i₀ = FAk⁰C^…` — **계면 전하이동 속도상수 k⁰** | **0 건.** 우리는 k⁰ 도 i₀ 도 α 도 계산하지 않는다 |
| **농도 과전압** | `R_mt = RT/(nF·i_L)`, `i_L ∝ D_O` — **확산계수 D** | **여기.** 우리 `D(600 K) 3.09/7.90 ×10⁻⁶ cm²/s`, `Ea 0.253/0.224 eV`, BVSE 채널%가 이 가지 |

- ⇒ **"우리 NEB/Ea 가 낮으니 과전압이 낮다"는 문장은 반만 맞다.** 활성화 과전압에 대해서는
  **우리는 아무 말도 할 수 없다.**
- 실무적으로도 갈린다: ASSB 계면 저항을 임피던스로 재면 나오는 것은 대개 **R_ct + R_interphase**
  인데, 우리 계산은 그 어느 쪽도 예측하지 않는다.

### 6-D. 다리 ④ — `R_SEI` ↔ 우리 계면 분해산물: **"무엇이 생기나"는 있고 "얼마나 저항인가"는 없다**

- **발표** [덱 슬 46]: 노화·고온 셀에서 `R_SEI` 가 다른 저항을 압도할 수 있고, 원인은
  **두꺼워지거나(thicker) 더 치밀해져서(more compact)**.
- **우리**: grand-potential 로 **산물**(`Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻`)과
  **onset 전압**(2.256 V)은 낸다. `sei_products.json` 은 그 산물의 **결정상 band gap**(전자 절연성)을 본다.
- **없는 것**: 그 interphase 의 **이온 저항률**, **두께 성장 kinetics**, **치밀도**.
  ⇒ `R_SEI` 에 해당하는 우리 값은 **0** 이다. `comparison_vs_ours.md` §H 의
  "Li 금속‖SE 계면 반응 MD(SEI 두께·상·성장 시간, `open_items` T3)" 행이 정확히 이 구멍이다.
- **가치**: 이 발표는 그 구멍이 **왜 실무에서 치명적인지**(수명·고온 이력에서 지배항이 된다)를
  소자 언어로 설명해 준다. 우리 T3 항목의 **동기 문장**으로 쓸 수 있다.

### 6-E. ⛔ 접점이 **없는** 것 — 억지로 잇지 말 것

| 발표 내용 | 왜 우리 축이 아닌가 |
|---|---|
| **Levich 한계전류식** `i_L,c = 0.62nFAD^(2/3)C*ω^(1/2)/ν^(1/6)` [덱 슬 43] | **회전원판전극(RDE) 전용 식**이다. `ω`(회전속도)와 `ν`(동점성계수)는 **액체 + 강제대류** 전제 — 고체전해질에는 **대류가 없고 ω 가 정의되지 않는다**. ⛔ ASSB 로 이식 금지 |
| **분리막 셧다운 135 °C** [덱 슬 22] | PE 분리막 고유 기능. ASSB 에는 PE 분리막이 없다(무기 SE 가 대신). 안전 기구가 근본적으로 다르다 |
| **`Q_rev = TΔS`, `E_cal`** [덱 슬 33–35] | 우리는 0 K DFT 형성에너지·grand potential 만 본다 — **엔트로피 항이 아예 없다.** 대응값 없음 (§6-F) |
| **`E_eq` 2상/단상 거동** [덱 슬 5–6] | 양극 활물질 얘기다. 우리 SE 는 산화·환원되는 활물질이 아니라 **전위창 안에서 안 변해야 하는 물질**이다 |
| **가성비 논지(750 vs 600)** [덱 32; `[STT 54:14]`] | **소자 경제성**. 개념적 교훈(§4A-A3)일 뿐 우리 4축에 수치로 대응 없음 |

### 6-F. 이 발표가 드러낸 **우리 공백 목록** (정직하게)

| 소자 항 | 우리 대응 계산 | 상태 |
|---|---|---|
| `κ_SE`(재료) | MLIP-MD σ_ion | ✅ 있음 (단 **벌크 상한**) |
| `l`, `A`(기하) | — | ❌ **0** (DEM/미세구조 축 소관) |
| `κ_effective`(GB·기공·접촉) | — | ❌ **0** (§H 기존 행) |
| `η_activation` / `k⁰` / `i₀` / `R_ct` | — | ❌ **0** |
| `D` (전극 활물질 내부 Li 확산 → 농도 과전압) | — | ❌ **0** (우리는 SE 내부 확산만) |
| `R_SEI` / interphase 이온 저항 | 분해 **산물·onset** 만 | ❌ **저항은 0** |
| `Q_rev = TΔS` | — | ❌ **0** (0 K 근사) |
| `Q_Joule` | (원리적으로 σ·기하에서 유도 가능) | ❌ **계산 0** |

---

## 7. ⛔ 인용 금지 목록

1. **덱 수치를 우리 `db/properties/*` 절대값과 같은 표에 넣지 않는다.**
   `750/600/560/50 mAh`, `−282/−256/−26 kJ/mol`, `1.28/1.30/1.44 V`, `i₀ = 2.2 µA`,
   `E_eq = −0.11 V`, `~0.2 V / ~4.0 V`, `135 °C`, `80–100 °C` — **전부 튜토리얼 예시**이고,
   출처(측정 셀·문헌)가 덱에 없다. **원고 인용 금지.**
2. **[STT] 의 숫자는 인용하지 않는다.** 구두 `≈−280`, `≈−250`, `"플러스 1"`, `"3.8 V"` 는
   §5-C 대로 반올림·실언이 섞여 있다. 필요하면 **`구두 ≈`** 를 붙인다.
3. **슬 30 을 "실제 데이터"로 인용 금지.** [STT 47:15] 에서 그렇게 불렀지만, 덱 그림에
   **축 눈금·셀 정보·출처가 없다.** 도식으로만 취급.
4. **Levich 식(슬 43)을 고체전해질에 이식 금지** (§6-E).
5. **"오승모 교수님이 그랬다"를 논거로 쓰지 않는다.** §4 는 전부 **미확인 전문가 판단**이다.
   우리 데이터로 확인 가능한 것은 확인하고, 못 하면 미확인이라고 쓴다.
6. **부재의 증거로 쓰지 않는다.** 덱은 튜토리얼용으로 잘라낸 것이다 — "이 발표에 없으니
   중요하지 않다"는 서술 금지 (`talks/README.md` §3).
7. **소속명은 `Battery Convergence Engineering` 으로 쓴다.** 덱 인쇄 `Conflation` 은 오타 (§5-E).
8. **녹취 헤더 시각(2026-08-25 09:22)을 발표 시각으로 인용 금지** (§1b).
9. **슬 22 SEM 스케일바 단위 인용 금지** — 판독 불가 (§1c).
10. **좌장의 약력 소개 인용 금지** — STT 붕괴 (§5-D).

---

## 8. 안 본 것 / 못 하는 것

### 8-a. 본 것
- **크롭 50컷 전부(50/50) 이미지로 판독.** = 자료집 표지 2컷 + **덱 48 슬라이드 전부**.
- 고배율(6×–8×) 재판독 **5건** (§1c).
- 녹취 **전문 683행 / 80블록 전부** 통독.

### 8-b. 못 본 것 / 못 한 것
| 항목 | 상태 |
|---|---|
| PDF **p.2** | 도구가 blank 로 판정해 추출하지 않았다. **텍스트 0자**이고 앞뒤 쪽번호가 연속(`-1-` → `-3-`)이므로 **자료집 구분면**으로 판단. **내용 없음 — 미검증** |
| 슬 22 스케일바 단위 | **판독 불가** (§1c) |
| 슬 4·슬 7 의 구술 대응 | **정렬 실패** — `?` 로 남김 (§2) |
| 슬 37 (Energy efficiency) 구술 | **발표자가 건너뜀** — 덱만 존재 |
| 좌장 소개(00:00–00:06) 내용 | STT 붕괴로 **복원 불가** |
| 덱 인용 문헌 | **본문 참고문헌이 없다.** 슬 8 에 `<2-8>`(교재 그림번호), 슬 48 에 교재명(*"전기화학" 5판*)만. 슬 9·31·32·39·40 의 삽입 그림은 **출처 미표기** |
| 질의응답 | **없음** (쉬는 시간으로 이관) — 즉 이 자료에는 **청중 질문에서 나오는 정보가 0** |

### 8-c. 이 자료로 **할 수 없는 것**
- 어떤 **실측값의 출처**도 추적할 수 없다 (모든 그림이 출처 미표기).
- **황화물 ASSB 특유의 항**(스택압, SE|양극 계면, 복합양극 tortuosity)에 대해서는
  **아무 말도 하지 않는다** — 이 튜토리얼은 액체 LIB 중심이다.
- 우리 4축 어느 값도 **검증하거나 반박하지 못한다.**

---

## 9. INDEX·comparison 에 넣을 줄

### 9-a. `INDEX.md` → **§🎤 학회 발표자료** (papers/ 와 섞지 않는다)
```
| `talks/oh2026_kecs_cell_polarization.md` | **오승모**(연세대 Battery Convergence Engineering + Min Tech),
"**셀 분극에 의한 이차전지의 성능 / Effects of cell polarization on cell performances**"
(2026년도 전지기술 심포지엄 **Tutorial I**, 8/20(목), 주최 한국전기화학회 KECS, 자료집 26 pp = 2-up 덱 48장,
**텍스트레이어 0 = 전면 스캔**; 녹취 83분 13초 확보) | **소자 전기화학 축 — 물성 4축에 수치 0건**.
`cell polarization = η_a + η_c + iR_total` 한 식으로 전압·용량·에너지·발열·안전을 전부 설명하는 튜토리얼.
**우리와 닿는 진짜 다리 4개**: ①`R_SE = l/(κA)` — 우리 σ_ion 이 셀에 들어가는 유일한 통로 +
덱 슬 44 **"진짜 중요한 건 전도도가 아니라 저항"** ②`E^a = E^a_eq + η_a` — 우리 ESW onset(2.256 V)은
**반쪽전지 전위**이고 고율일수록 산화 구동력이 더 커진다 ③우리 Ea/NEB 는 **농도 과전압 가지**이지
**활성화 과전압(k⁰·i₀·R_ct) 가지가 아니다(우리 0건)** ④`R_SEI` — 우리는 계면 분해 *산물·onset* 만 알고
*저항*은 모른다. **덱 50/50 전 컷 이미지 판독 + 6–8× 재판독 5건**(우리 1차 전사 오류 1건 자체 발견·정정:
슬 9 `E_cal`→`E_cell` 오독). ⛔[불일치] 1건(슬 43 ν 방향). 덱 오타 3건(`Conflation`/`Activaton`/슬 39 부호문장) |
```

### 9-b. `comparison_vs_ours.md` → **🎤 TALK note [Oh26-Pol]** 블록 (물성 4축 표에는 **넣지 않는다**)
§A 직전 TALK note 군에 추가. 내용은 §6-A~6-D 요지 + §6-E 금지 목록.

### 9-c. `properties/*` · `db/properties/*`
**변경 없음.** 이 발표는 우리 물성 db 에 대응 항목이 하나도 없다.

---

## 10. 비판 — 이 자료의 한계

1. **모든 삽입 그림의 출처가 없다.** 슬 9(Ni-Cd 방전곡선)·슬 22(분리막 SEM)·슬 31/32(graphite/LiCoO₂
   레이트 곡선)·슬 39(납축전지)·슬 40(열폭주 단계도)은 전부 외부에서 가져온 것으로 보이는데
   캡션·인용이 없다. 튜토리얼이라 관행상 넘어가지만, **우리가 그 수치를 쓰려면 원출처를 따로 찾아야 한다.**
2. **슬 30 을 "실제 데이터"라고 부른 것** [STT 47:15] 은 덱과 어긋난다 — 축 눈금이 없다. §7-3.
3. **슬 29 의 "옴 iR drop = 중간 전류 지배"** 는 도식적 단순화다. 실제로는 iR 이 전 구간에서
   선형으로 존재하고, 저·고전류에서 다른 항이 더 빨리 자라서 *상대적으로* 중간에서 두드러질 뿐이다.
   덱 문장만 떼어 인용하면 "저전류에서는 iR 이 없다"로 오독될 수 있다.
4. **표기 일관성이 낮다** — η 부호(슬 13 vs 23), `R_total` 분해 3종, Ni-Cd `E_cell` 1.28/1.30.
   §5-F. 튜토리얼에서는 표기 일관성이 곧 교육 품질이다.
5. **전 구간이 액체 전해질 전제**다. `R_solution`, `supporting electrolyte`, `mechanical convection`,
   Levich `ω`·`ν` — 전부 액상 개념이다. **고체전해질 셀에서는 어느 항이 살아남고 어느 항이 죽는지**를
   덱이 다루지 않는다. (우리가 §6-E 에서 직접 갈라야 했던 이유.)
6. **시간 압박으로 처방부(슬 42–46)가 얇다** — 그런데 **우리와의 접점은 대부분 거기 있다** (§4C).
7. **질의응답이 없다** — 이 등급 자료의 가장 큰 값어치(전문가의 즉석 판단)가 절반만 확보됐다.
   §4 는 전부 본문 방백에서 건진 것이다.

---

## 11. 기법 미니 용어집 (우리 팀 기준)

| 용어 | 이 발표에서의 뜻 | 우리 쪽 대응 |
|---|---|---|
| **cell polarization** | `η_a + η_c + iR_total`. 셀이 이론값을 못 내게 하는 전압 손실 총량 | **대응 계산 없음** |
| **E_cell (emf)** | 두 반쪽전지 평형전압의 차. 최대 방전전압 / 최소 충전전압 | grand-potential OCV 1.717 V 와 **다른 축** (우리 건 반쪽전지) |
| **η_activation** | charge transfer 를 빠르게 하려고 더 거는 전위. `R_ct = RT/(i₀F)` | **0 건** |
| **η_concentration** | 확산을 빠르게 하려고 더 거는 전위. `R_mt = RT/(nF i_L)` | 우리 `D`·`Ea`·BVSE 가 여기로 들어간다 |
| **iR_total** | 닫힌 고리 저항이 만드는 전압 강하 | 우리 `σ_ion` → `R = l/(κA)` |
| **i₀ (exchange current)** | 평형에서 양방향으로 똑같이 흐르는 (보이지 않는) 전류 크기 | **0 건** |
| **k⁰ (standard rate constant)** | 계면 전하이동 고유 속도 | **0 건** |
| **Q_rev (= TΔS)** | 열역학 기원 열. **흡열도 발열도** 된다 | **0 건** (0 K 근사) |
| **Q_Joule** | 동역학(분극) 기원 열. **항상 발열**, 전류 의존 | **0 건** |
| **E_cal (calorific voltage)** | `ΔH = −nF·E_cal` 로 정의한 **가상** 기전력. 비교용 눈금 | 없음 |
| **dischargeable vs actual capacity** | 낼 수 있는 최대 용량 vs 그 전류·cut-off 에서 실제로 낸 용량 | 우리는 **재료 이론용량 축**만 |
| **shut-down** | PE 분리막 용융(135 °C)으로 `i_separator → 0` → 전 회로 정지 | ASSB 에 대응 기구 없음 |
| **VRLA** | valve-regulated lead-acid. 저전류 방전에서 **셀이 식는** 예 | 없음 |

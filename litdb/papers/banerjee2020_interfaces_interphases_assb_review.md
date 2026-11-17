<!-- digest (paper-level standalone) · 2026-11-17 첫 작성 · 리뷰 (자체 계산 0 · 자체 실험 0) · 한 논문이 PDF 두 파일로 왔다.
     그림 34 장 중 19 장 실독 (Fig. 17 · 18b · 26 은 확대 + 픽셀 캘리브레이션) · 표 2 장은 PDF 텍스트 · 참고문헌 341 편 전수 대조 (부록 R). -->

# Interfaces and Interphases in All-Solid-State Batteries with Inorganic Solid Electrolytes — Banerjee · Wang (공동 1저자) 외 (*Chem. Rev.* **2020**, 120, 6878–6933)

> slug `banerjee2020_interfaces_interphases_assb_review` · DOI `10.1021/acs.chemrev.0c00101` · type `review (자체 계산 0 · 자체 실험 0 — 문헌 종합 · refs 341 · Fig. 1–34 + Table 1–2)` · PDF **두 파일 = 한 논문**: `95e3257f-1-1_Interfaces_and_Interphases_in_All-Solid-State_Batteries_with_Inorganic_Solid_Electrolytes.pdf` (30 pp = 지면 6878–6907 · sha256 `02aa46ea73c4345a…`) + `2f93ea34-2_Interfaces_and_Interphases_in_All-Solid-State_Batteries_with_Inorganic_Solid_Electrolytes.pdf` (26 pp = 지면 6908–6933 · sha256 `7c8d39c0640d38e8…`) · digested `2026-11-17` · status ✅ · 태그 **[외부·리뷰·⭐⭐ 참고문헌 허브 (341 편)]**
> elements: Li, P, S, Cl, Br, I, O, N, F, Ni, Co, Mn, Al, Nb, Ti, Zr, La, Ge, Si, Sn, Y, In, Na, Sb
> methods: DFT, AIMD, ESW, XPS, Raman

> **저자**: **Abhik Banerjee**\*⊥ · **Xuefeng Wang**\*⊥ (⊥ 공동 1저자) · Chengcheng Fang · Erik A. Wu · **Ying Shirley Meng**\* — UCSD NanoEngineering (X. Wang 은 중국과학원 물리연구소 겸 · A. Banerjee 는 TCG CREST (콜카타) 겸) · 접수 2020-02-05 · 출판 2020-06-30 · 특집 *Beyond Li-Ion Battery Chemistry* · 이해상충 없음 선언.
> **관련 카드**: `xiao2020_interface_stability_ssb_review` (같은 해 다른 계면 리뷰 · Ceder 그룹 — 그 digest 가 이 편의 서지를 *미확정* 으로 남겨 뒀다 → §0a 에서 닫는다) · `banerjee2019_tunneling_tlm_parallel_nanoscale_contacts` (**다른 논문** — *Sci. Rep.* 2019 나노 접촉 터널 TLM · 주제 무관 · 같은 저자인지는 확인 안 함) · 원전 digest 21 편 (§9a 목록).
> **계기**: 사용자 2026-11-17 *"지금 가장 reference 가 많이 있는 논문"* — 참고문헌 허브로서의 지도 (§9) · 양극–황화물 계면 + 코팅 정독 (§3b–3d · §7b) · [혁주] 요청서가 인용한 그림의 확인 (§0c).

---

## 0. 이 digest 를 읽는 법

### 0a. 서지 — 두 PDF 는 한 논문이다 · `xiao2020` 의 미확정 서지가 여기서 닫힌다
- **Part 1** = 지면 6878–6907: §1 – §5.1 의 *"2. Kinetically stable SE"* 까지 · `Fig. 1`–`Fig. 27`.
- **Part 2** = 지면 6908–6933: §5.1 *"3. Thermodynamically stable interface with no decomposition energy"* 부터 · `Fig. 28`–`Fig. 34` · `Table 1`–`Table 2` · 저자 정보 · 약어 · **참고문헌 1–341 전부**.
  ⚠ 의뢰서는 *"참고문헌 목록 안에서 끝난다 (refs ≥ 330)"* 고 했는데 실물은 **341 번 (Han 2019 *Nat. Energy* 4, 187) 에서 끝나는 완본**이다 — 지면 6933 이 논문 끝이고 본문 최대 인용 번호도 341 이다.
- 두 파일 사이 쪽 겹침 없음 (6907 → 6908) · 그림 번호 연속 · 크롭 도구는 두 파일을 다 본문으로 판정 (SI 오분류 없음 · 그림 34 + 표 2 = 36 장 · 번호 공백 0 · `missing_labels` 빈 목록).
- ⛔ `xiao2020_interface_stability_ssb_review` §0a 는 *"흔히 Banerjee, Wang, Meng 으로 인용되는 UCSD 리뷰 … 이 digest 는 Banerjee 편 PDF 를 갖고 있지 않다 — 그 편의 서지를 여기서 확정하지 않는다"* 고 적었다. **이 편이 그 리뷰다**: *Chem. Rev.* **120** (14), 6878–6933 (2020) · DOI 10.1021/acs.chemrev.0c00101. 제목부터 다르다 — Xiao 편 *"Understanding interface stability in solid-state batteries"* (*Nat. Rev. Mater.* 5, 105) · 이 편 *"Interfaces and Interphases in All-Solid-State Batteries with Inorganic Solid Electrolytes"*.

### 0b. 본 그림 / 안 본 그림 — 그림 34 장 중 **19 장 실독** · 표 2 장은 PDF 텍스트
- **본 것 (19)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 8` `Fig. 10` `Fig. 11` `Fig. 12` `Fig. 13` `Fig. 14` `Fig. 15` `Fig. 17` `Fig. 18` `Fig. 19` `Fig. 20` `Fig. 26` `Fig. 27` `Fig. 33`.
  `Fig. 17` (전압 막대) · `Fig. 18b` (Nyquist) · `Fig. 26` (안정창 막대) 은 확대 크롭 + **픽셀 캘리브레이션** (축 눈금 라벨 중심에 선형 맞춤 · 막대 끝 색 경계 · 오차 ≈ ±0.03 V) 으로 읽었다. 검산: `Fig. 17` 의 LTO · LiNbO₃ · Li₂SiO₃ · LLZO 막대가 `zhu2015_esw_grand_potential_origin` 의 SI Table S3 값과 ±0.03 V 안에서 다 맞는다 (§3d).
- **안 본 것 (15)**: `Fig. 6` `Fig. 7` `Fig. 9` `Fig. 16` `Fig. 21` `Fig. 22` `Fig. 23` `Fig. 24` `Fig. 25` `Fig. 28` `Fig. 29` `Fig. 30` `Fig. 31` `Fig. 32` `Fig. 34` — 이 그림들에 대한 서술은 **캡션 · 본문만**이다. `Table 1` · `Table 2` 는 PDF 텍스트에서 옮겼다 (이미지로 안 읽음).
- 크롭 상태: 36 장 자동 · `Fig. 15` · `Fig. 32` 의 *"continued"* 캡션 쪽 (지면 6893 · 6916) 은 *영역 없음* 으로 제외됐다 — `Fig. 15` 는 앞쪽 크롭에 패널 a–i 가 다 들어 있음을 확인했고 `Fig. 32` 는 안 봤다.
- 등급 표기: **stated** (본문 · 캡션 인쇄값) · **figure-read ≈** (내가 그림에서 읽음) · **우리 산수** (이 digest 의 계산) · **추정**.

### 0c. ★ 의뢰 질문 ③ — 이 리뷰의 `Fig. 4` · `Fig. 8` 은 [혁주] 요청서가 말한 그림이 아니다
프로젝트 노트 `kb/projects/hyeokju_lzo_interface_2026_11_16.md` (34 행) 의 *"Banerjee 2019 ACS Appl. Mater. Interfaces Fig. 4 (LPSCl–NCA · LPSCl–LNO 혼합 반응에너지 · AIMD) 와 Fig. 8 (코팅 물질 표)"* 를 이 리뷰의 크롭과 대 보았다 (전부 실독):

| 이 리뷰 | 캡션 (원문 발췌) | 요청서 서술과 |
|---|---|---|
| `Fig. 4` | *"Possible interfacial reactions of sulfide SEs at a wide range of operating voltages … Reproduced with permission from ref 45."* — 전압 지도 (눈금 없는 도식 · 표지 0 · 0.7 · 2 · 4.3 V · 흑연 0–0.7 · S/MS₂ ≈ 2 부근 · NCA 는 2 와 4.3 사이에서 4.3 까지) + PS₄³⁻ 산화환원 사다리 (Li₃P + Li₂S ⇌ Li₄P₂S₆ ⇌ Li₃PS₄ ⇌ Li₄P₂S₇ + S⁰ ⇌ Li₂P₂S₆ + 2S⁰) | ❌ 혼합 반응에너지 곡선 없음 · AIMD 없음 · LNO 없음 |
| `Fig. 8` | *"(a) Cyclic voltammograms … of LPSCl-carbon composite … (b) Nyquist plots … (c) Schematic of … reversible oxidation and reduction pathway of Li6PS5Cl. Reproduced … from ref 41."* | ❌ 코팅 물질 표 아님 (Tan 2019 의 CV · EIS · 산화환원 도식) |
| **`Fig. 18a`** | *"Pseudobinary phase diagram of NCA−LPSCl and LNO−LPSCl. Reproduced with permission from ref 51. Copyright 2019 American Chemical Society."* | ✅ 요청서의 **'혼합 반응에너지'** 내용 — 단 **AIMD 는 없다** |
| **`Fig. 17`** | *"Necessary criteria for an effective cathode coating for ASSBs. Reproduced with permission from ref 51. Copyright 2019 American Chemical Society."* — 그림 제목 *"Screening of Coating Materials"* | ✅ 요청서의 **'코팅 물질 표'** |
| (본문 한 줄) | 지면 6890 *"Banerjee et al. also used AIMD to study the NCA−LPSCl interface where the P−O bond forms along with the S−S, Ni−S, and Co−S bonds, agreeing well with the thermodynamic calculations."* — 번호 없는 인용 · 그림 0 | AIMD 는 **문장 한 줄**로만 있다 |

⇒ **답**: 요청서의 그림은 이 리뷰가 아니라 **원전 ref 51 = Banerjee et al., *ACS Appl. Mater. Interfaces* 11, 43138–43145 (2019)** (*"Revealing Nanoscale Solid−Solid Interfacial Phenomena for Long-Life and High-Energy All-Solid-State Batteries"*) 의 그림이고, 이 리뷰에서는 **`Fig. 18a` (혼합 곡선) · `Fig. 17` (코팅 표)** 로 다시 실렸다. 요청서의 'Fig. 4 · Fig. 8' 은 **원전 안의 그림 번호일 가능성이 높다 (추정 — 원전 PDF 가 없어 확인 못 함)**. 원전은 **지금도 litdb 에 없다** (이 리뷰 참고문헌에 ref 51 과 ref 327 로 두 번 실렸다 · §9a).
이 리뷰의 재수록에서 확인되는 사실 둘: ① 혼합 곡선의 세로축은 **eV/f.u.** 이고 f.u. 정의가 그림 · 캡션 · 본문 어디에도 없다 (§4c — 우리 meV/atom 과 단위부터 다르다) ② 코팅 표에서 **Li₂ZrO₃ 는 σ · 띠틈 칸에만** 있고 반응에너지 · 전압창 칸에는 없다 (§3d).

### 0d. 가져올 것 / 못 가져올 것
- ✅ **가져올 것**: 계면 지도 (13 시나리오 · `Fig. 1`) · 화학 반응과 전기화학 분해를 **실험으로 가르는 설계** (`Fig. 14` — 액체 셀로 충전한 NCA 를 LPSCl 과 섞기) · 코팅 5 요건 (`Fig. 17`) · 계산 세 접근의 분류 (§6.1) · 341 편 참고문헌 지도 (§9).
- ⛔ **못 가져올 것**: 계산 조건 (functional · U · k · 셀 · 시간 — 전부 0) · 모든 수치는 **소환값**이라 원전 ref 번호와 같이 쓴다 · 그런데 **ref 번호 자체가 내용과 안 맞는 곳이 최소 9 곳**이다 (§9d) ⇒ 원전을 제목으로 확인하기 전에는 번호만 믿고 인용하지 않는다.

---

## 1. 한 줄 요약

고전도 황화물 SE 가 나온 뒤 ASSB 의 병목은 SE 안의 확산이 아니라 **계면** (공극 · 화학 반응 · 전기화학 분해 · 입계 · 기계적 접촉 상실) 이라는 진단 아래, 양극–SE (§4) · 음극–SE (§5) 계면을 *화학 / 전기화학 / 물리 접촉 / 기계* 네 갈래로 정리하고 코팅 선정 5 요건 (상안정 · 화학 양립 · 전기화학 안정 · 이온/전자 전도 · 기계) 과 분석 기법 (§6) 을 묶은 UCSD Meng 그룹의 341 편 리뷰다. 결론의 무게중심은 *"양극 전하이동 저항이 고출력 ASSB 의 병목"* (§7) 이고, 새 SE 는 전도도보다 **전극 계면 성질로 먼저 걸러야 한다** (요약 I).

## 2. 메타 · 구조

| 절 | 지면 | 내용 | 우리 축 |
|---|---|---|---|
| §1–2 | 6879–6881 | 계면 13 시나리오 (`Fig. 1`) · 공극 / 화학 / 전기화학 / 입계 4 분류 | — |
| §3 | 6881–6886 | SE 전기화학 창 (HOMO/LUMO 도식 `Fig. 2` · grand potential `Fig. 3`) · 작동창 조정 · 분해 속도론 (탄소) · SE 자체 redox | **B① · B②** |
| §4.1 | 6886–6898 | 양극–SE 화학 반응: 계산 (`Fig. 10` · `Fig. 12`) · 실험 (`Fig. 13` · `Fig. 14`) · 공간전하층 · **코팅** (`Fig. 17` · `Fig. 18` · `Fig. 19`) | **B③** · [혁주] |
| §4.2–4.5 | 6898–6907 | SE 기계 물성 (`Fig. 20` · `Fig. 21`) · Li–S · 등각 (용액) 코팅 · 하이브리드 (액체 첨가) | C |
| §5 | 6907–6917 | 음극: 세 유형 (`Fig. 26` · `Fig. 27`) · 보호층 (`Table 1`) · 접촉 · 기계 · 스택압 (`Fig. 30`–`Fig. 32`) · 액체 대비 (`Table 2`) | E |
| §6 | 6917–6921 | 계산 세 접근 · EM · TXM/CT/ToF-SIMS/AFM · XAS/XPS/Raman · NMR/EIS · NDP | 방법 |
| §7 | 6921–6922 | 요약 + 과제 I–V | — |

---

## 3. 핵심 수치 총정리 — 전부 소환값 (원전 ref 번호를 같이 쓴다)

### 3a. 전기화학 창 (우리 축 B①)

| 물질 | 값 | 출처 · 등급 |
|---|---|---|
| **LPSCl (Li₆PS₅Cl)** | 환원 **< 1.7 V** · 산화 개시 **2.3 V** vs Li/Li⁺ · 환원 산물 Li₃P · Li₂S · LiCl · 산화 산물 S · P₂S₅ | 지면 6881 stated (grand potential · 원전 번호 없음) |
| 〃 `Fig. 3b` 계단 (Li 흡수 수 / f.u.) | **+8** (0–0.88 V · Li₃P, LiCl, Li₂S) → 6 · 5.4 · 5.2 → **+5** (≈1.3–1.73 V · LiCl, Li₂S, P) → **0 (1.73–2.36 V · Li₂S, LiCl, Li₃PS₄)** → **−2** (2.36–2.64) → **−5** (2.64–3.30 · P₂S₅, LiCl, S) → **−6** (> 3.30 V) | figure-read ≈ (±0.03 V) |
| 〃 `Fig. 26` (ref 30 Richards 2016 재수록) | **≈ 2.08–2.29 V** (빨강 = Li 금속과 불안정) | figure-read ≈ — ⚠ 같은 리뷰 안 **두 번째 LPSCl 창** (§10-2) |
| LGPS · LPS | 산화 개시 2.15 · 2.41 V (서론 · ref 8) · 0 V 분해에너지 −1.23 · −1.42 eV/atom (ref 11) · `Fig. 3d` LGPS 1.71–2.14 V | stated |
| LLZO | 환원 0.05 V · 0 V 분해 −0.02 eV/atom · 산화 2.91 V (`Fig. 3d` 0.05–2.91) | stated (refs 11 · 52) |
| LLTO · LATP | 환원 1.7 · 2.4 V (Ti⁴⁺ → Ti³⁺) · LATP 산화 4.31 V · 5 V 분해 −65 meV/atom | stated |
| LiPON | 본문 **0.68–2.63 V** (지면 6884 · ref 56) vs `Fig. 3d` **0.7–1.1 V** | ⚠ 본문 ↔ 그림 불일치 (§10-2) |
| Li₃YCl₆ | `Fig. 3d` 0.6–4.23 V · 실험 분해 개시 *"4.2 V"* (`Fig. 5a` 평탄 figure-read ≈ 4.1 V) | stated · figure-read |
| 산화 순서 | 염화물 > 산화물 > 황화물 > 질화물 (Li₃YCl₆ > LLZO > LPS > LiPON) · 음이온 전하밀도 N³⁻ > S²⁻ > O²⁻ > Cl⁻ 와 대응 (지면 6882) | stated |
| 측정 규약 | 평판 Ti 집전체 CV = 반응 면적 부족 → 창 과대 (5–10 V 주장의 원인) · **SE + 탄소 복합 전극**으로 재면 grand potential 과 맞는 봉우리 (`Fig. 3a,c`) · *"should be widely applied for all kinds of SEs"* | stated |
| LPSCl 가역 redox | 0–4 V 가역 · 4 V 산화에 S · P₂S₅ (XPS) · 계면 임피던스 **2 자릿수 ↑** · 1.3 V 방전 뒤 PS₄³⁻ 복귀 · LiCl 은 첫 산화 뒤 redox 불참 · 0 V 에 Li₃P · Li₂S (ref 41) — `Fig. 8b` 막대 figure-read ≈ OCV 10^1.7 → 4.2 V 10^3.8 → 1.3 V 10^2.2 → 0 V 10^2.6 Ω | stated + figure-read |

### 3b. 양극–황화물 화학 반응 — 계산 (축 B③)

| 쌍 | 값 | 출처 · 등급 |
|---|---|---|
| LCO–LGPS · LCO–LPS (Li₃PS₄) | **−340 · −405 meV/atom** · Li₀.₅CoO₂ 와 **−499 · −564** | ref 11 (Zhu 2016 · litdb ✅) stated · `Fig. 10` figure-read 과 일치 (LPS–LCO 최소 x ≈ 0.42–0.48 · L0.5CO 최소 x ≈ 0.40) |
| LLZO–LCO / Li₀.₅CoO₂ | *"1/53 meV per atom"* (부호 생략 인쇄) · `Fig. 10` L0.5CO 점선 figure-read ≈ −40 | stated / figure-read (얇은 점선이라 판독 불확실) |
| 산물 (LCO–황화물) | Co₉S₈ · Li₂SO₄ · Li₃PO₄ · Co⁴⁺ 가 반응을 키운다 · 황화물이 TM 을 Co²⁺ 로 환원 (산화물 SE 와는 반대로 Li₀.₅CoO₂ 가 생김) | stated |
| **NCA–LPSCl · LNO–LPSCl** (`Fig. 18a`, ref 51) | **NCA 최소 ≈ −21 eV/f.u. @ x ≈ 0.37** · **LNO 최소 ≈ −1.3 eV/f.u. @ x ≈ 0.5–0.6** · 산물 주석 *"Li₃PO₄, LiCl, Ni₃S₄, etc"* (x ≈ 0.07–0.12 구간) | figure-read ≈ — ⛔ **세로축 eV/f.u. · f.u. 정의 없음 · NCA 의 충전 상태 표기 없음** (§4c) |
| Na 계 (`Fig. 12a`, ref 80) | 층상 산화물 (특히 NaNiO₂ · NaCoO₂) 이 Na₃PS₄ · Na₃PSe₄ 와 가장 크게 반응 · 폴리음이온 양극 (NaFePO₄ 등) 은 작다 · SbS₄ 계가 PS₄ · PSe₄ 보다 안정 · 산화물 SE (Na₃Zr₂Si₂PO₁₂) 가 가장 안정 · 반응 부피 변화도 같이 표시 | stated + 색지도 (눈금 −0.6–0 · 단위 *"eV"* 만 · per atom 표기 없음) |

### 3c. 양극–황화물 반응 — 실험

- **휴지 실험** (ref 85 = litdb `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb`): NMC + Li₆PS₅Cl 펠릿 (본문 *"1:1 wt. ratio"* ↔ `Fig. 13d` 라벨 *"1:1, v/v"* ⚠) · 48 h 휴지 셀이 용량 ↓ · 분극 ↑ (`Fig. 13a` 그림 주석 ΔV ≈ 0.10 → 0.28 V) · bulk + 입계 저항 **48 h 에 400 %** 증가 (stated · 그림 축은 40.6 h 까지).
- **방전 상태 계면 산물**: NiS · CoS · MnS · Li₂S · LiPₓCl_y · LiCl / **사이클 뒤**: Mn₃(PO₄)₂ 또는 Ni₃(PO₄)₂ · Li₃PO₄ · POₓ · SOₓ (2 < x < 3) — *"electrochemical delithiation makes oxygen more reactive with P and S"* (지면 6891).
- ★ **화학 반응만 떼는 설계** (`Fig. 14`, ref 51): NCA (LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂) 를 **액체 반쪽전지에서 4.3 V 까지 충전** (C/100 + 4.3 V 정전압 · figure-read ≈ 200 mAh g⁻¹ ≈ Li₀.₂₈ — 위 가로축) → 꺼내 LPSCl 과 막자 혼합 → XRD · Raman: **결정성 Ni₃S₄ (그림 범례) · Li₃PO₄ · LiCl** 이 충전 상태에서 뚜렷 · 미충전 혼합은 약함 · **LNO 코팅 NCA@4.3 V + LPSCl 은 산물 피크 없음 · Raman PS₄³⁻ (≈ 420 cm⁻¹) 유지** (본 그림). ⚠ 본문은 *"NiS"* 라 쓰고 그림은 *"Ni₃S₄"* (§10-2). ⛔ 이 Li₀.₂₈ (4.3 V) 를 [혁주] y 격자의 전압 라벨로 옮기지 않는다 (stage 1 카드 §5b · G5 — §7b).
- TEM: LCO–Li₂S·P₂S₅ 계면 비정질 층 (ref 10) · Co · P · S 상호확산 **≈ 50 nm** · Li₂SiO₃ 코팅이 **≈ 30 nm** 로 줄임 (§6.2).
- XPS: NCA–LPSCl 사이클 뒤 **PO₃⁻ · SO₃⁻ · PSO⁻** (ref 51).
- cryo-STEM (`Fig. 33`, 본 그림): NCA–LPSCl 계면에 **Co · S 편석** (점선 띠 · 50 nm 눈금자 대비 수십 nm — 저자가 그린 점선이라 정량 아님) · Cl 도 계면 쪽에 몰린 것처럼 보인다 (본문 언급 없음) · LNO 코팅이 이를 막음 (본문 · ref 327).
- 산화물 SE (대조): LLZO–LCO 어닐 → Co · La · Zr 상호확산 · 계면 ≈ 20 nm (250 °C) / ≈ 100 nm (500 °C) · La₂CoO₃ (Ogumi · ref 89) · LaCoO₃ · Li₂CO₃ · *"Li₂ZrO₇"* (⚠ 오기로 보임 — La₂Zr₂O₇) (Vardar · ref 91) · Al 이 어디로든 확산 → 정방정 LLZO (10⁻⁷ S/cm) · Li₂CO₃ 는 산소 분위기 350 °C 처리로 제거.

### 3d. 코팅 — 선정 5 요건과 표 (`Fig. 17`, ref 51 재수록) ★

`Fig. 17` (본 그림 · 확대 판독) 은 네 칸이다 — ① 상안정 (R_c · E_hull) ② 화학 양립 (E_rxn · ΔV) ③ 전기화학 안정 (전압 막대) ④ 이온/전자 이동 (표):

| 코팅 | R_c | E_hull | E_rxn^NCA | E_rxn^SE (LPSCl) | ΔV^NCA | ΔV^SE | 창 (figure-read ≈ V vs Li/Li⁺) |
|---|---|---|---|---|---|---|---|
| LiNbO₃ | 1.2 | 0 | −0.013 | −0.16 | 2.8 | −17 | 1.77–3.91 |
| Li₄Ti₅O₁₂ | 1.4 | 0 | −0.02 | −0.11 | −1.2 | −9.5 | 1.77–3.71 |
| LiAlO₂ | 1.5 | 0 | 0 | −0.041 | 0 | −14 | 0.19–3.71 (연한 연장 → 4.11) |
| Li₂SiO₃ | 1.4 | 0 | 0 | −0.045 | 0 | 4 | 0.79–3.73 (→ 3.82) |
| Li₂PNO₂ (LiPON) | 1.4 | 0 | **−0.34** | 0 | 6.8 | 0 | 0.70–2.65 (→ 3.65) |
| Li₇La₃Zr₂O₁₂ | 1.3 | 0.0073 | −0.0059 | −0.19 | 11 | −9 | 0.06–2.92 (→ 3.32) |
| Li₂La₂Ti₃O₁₀ | 1.5 | 0.02 | −0.015 | −0.13 | 5.5 | −9.3 | 1.16–3.71 |
| (기준) Li₆PS₅Cl | — | — | — | — | — | — | 1.73–2.36 (→ 3.30) |
| (기준) NCA | — | — | — | — | — | — | 2.63–4.30 (작동 범위로 보인다) |

- R_c = 확산 채널 반경 (Å · 본문 *"in Å"*) · E_hull 은 eV/atom (본문). **E_rxn · ΔV 는 단위가 인쇄돼 있지 않다** — E_rxn 은 eV/atom 으로 보이고 (§4c 의 LNO 내부 대조가 그 읽기와 맞는다 · 추정) ΔV 는 % 로 보인다 (추정).
- 연한 막대 = 첫 산화 계단 뒤 다음 계단까지로 읽힌다 (LLZO 2.91 → 3.30 V 가 [Zhu15] 의 O₂ 방출 개시와 같다 — 우리 해석 · 범례 없음). 세로 점선 둘: 파랑 ≈ 2.36 V (LPSCl 산화 한계와 같은 자리) · 빨강 ≈ 2.52 V (의미 범례 없음).
- 🔎 창 막대는 **[Zhu15] SI Table S3 값과 같다** (`zhu2015_esw_grand_potential_origin`: LTO 1.75–3.71 · LiNbO₃ 1.74–3.88 (3.92 Nb₂O₅) · Li₂SiO₃ 0.76–3.74 (3.78 SiO₂) · LLZO 0.05–2.91) — figure-read 가 ±0.03 V 안에서 다 맞는다 ⇒ 이 칸은 Zhu 2015 값을 옮긴 것이다 (우리 판독 근거).
- ④ 이온/전자 표 (그림 안 인쇄 텍스트):

| 코팅 | σ_ion (S/cm, 온도) | 띠틈 (eV) |
|---|---|---|
| **Li₂ZrO₃** | **10⁻⁴ (598 K)** | **3.99** |
| LiPO₃ | 10⁻⁶ (333 K) | 2.26 |
| LiTi₂(PO₄)₃ | 2.5×10⁻⁸ (553 K) | 5.60 |
| *"LiLa(PO₄)₃"* ⚠ | 6.35×10⁻⁸ (553 K) | 5.22 |

  이 표는 **[Xiao19] Table 2 와 같은 값이다** (`xiao2019_cathode_coating_screening` §4a: Li₂ZrO₃ mp-31941 · Ea 0.48 eV · ~10⁻⁴ (598 K) · 3.99 eV) · ⚠ *"LiLa(PO₄)₃"* 는 전하가 안 맞는다 — [Xiao19] 의 **LiLa(PO₃)₄** 를 잘못 옮긴 것 (§10-6).
- ⭐ **Li₂ZrO₃ 는 이 표에만 있다** — 반응에너지 칸 (E_rxn^NCA · E_rxn^SE) · 전압창 칸에는 없다. 리뷰 안에서 LZO 라는 이름이 다시 나오는 곳은 `Fig. 15` 도식 (*"Apply Resistive Coating (LNO, LTO, LZO etc.)"*) 과 본문의 *"Li₂O-ZrO₂"* (삼원 코팅 목록) 둘뿐이다.

**본문의 5 요건** (지면 6895–6896 · stated):
1. **상안정** — E_hull 낮을수록 (`Fig. 17` 첫 칸 · refs 51, 99–101 ⚠ 100–101 은 내용이 안 맞는다 · §9d).
2. **화학 양립** — 양극 · SE 둘 다와의 pseudo-binary 분해에너지 · 산화물은 대개 0 에 가깝다 · *"LiPON, LiAlO₂, and Li₂SiO₃ are the most stable whereas LNO, LTO, and LLZO are comparatively less stable"* (LPSCl 쪽 기준 — ⚠ LiPON 은 NCA 쪽 **−0.34 로 표에서 가장 반응성이 크다**는 것을 본문이 말하지 않는다 · §10-8) · *"the decomposition energy for LNO−LPSCl is lower than for NCA−LPSCl"*.
3. **전기화학 안정** — TM redox 띠와 코팅의 O 2p 띠가 떨어져야 한다 · ⭐ *"most of the oxide-based coating materials are not stable at voltages greater than 4 V versus Li/Li⁺ as O²⁻/O₂ redox will take place"* · 불화물 유망: LiAlF₄ **5.7 ± 0.7 V** (ref 102 로 인쇄 · LiAlF₄ ALD 실험 원전은 ref 104 Xie 2017) → 4.5 V NMC.
4. **전도** — R_c 클수록 빠름 · Li₂O–SiO₂ · Li₃BO₃–Li₂CO₃ 이중 코팅이 단일 (SiO₂ · Li₃BO₃) 보다 낫다 · 띠틈 큰 것 (전자 전도 코팅은 SE 분해를 키움) · 그러나 전자 경로까지 막으면 율속 저하 — 균형.
5. **기계** — *"volume change of 10% and 30% (of the cathode) produces 1% and 10% strain"* (stated · 근거 없음 — 등방이면 부피 10 % ≈ 선변형 3.2 %, 우리 산수) · LNO 는 강성이 높아 소성 변형 대신 균열 (refs 104–106) · 비정질이 유리.

**코팅 효과 소환값**:
- LNO 2 wt% on NCA: CE · 방전 용량 · 양극 전하이동 저항 개선 (ref 51) · 장기 임피던스 안정 (`Fig. 13c–e`) — ⚠ `Fig. 13e` 에서 코팅 복합체의 **절대 임피던스는 모든 시각에서 무코팅보다 크다** (§10-2).
- LTO on LCO: 양극 저항 **900 → 20 Ω** (stated · refs 51, 82 ⚠ 82 는 LBO 논문) · `Fig. 18b` figure-read ≈ (반원 지름 · 0.5 Hz 점 기준): 무코팅 ≈ 890 Ω → 1 nm ≈ 114 · 2 ≈ 66 · **5 ≈ 44 (최소)** · 7 ≈ 57 · 10 ≈ 59 · 20 ≈ 65 · **30 nm ≈ 111 Ω** (비단조) · `Fig. 18c` 첫 충전 기울기는 **≥ 20 nm 에서 사라진다** (ref 83 Ohta 2006).
- ZrO₂ 0.7 wt% on NMC: 50 사이클 용량 120 mAh/g · 유지 95 % vs 무코팅 110 mAh/g · < 30 % · 무코팅 임피던스 600 → 1550 Ω/cm² · 코팅은 거의 불변 (ref 115).
- 이원 산화물 (ZrO₂ · Al₂O₃ · SiO₂) 은 Li 운반자가 없어 *활성화* 가 필요 — ① 충방전 중 전기화학 리튬화 ② 전극 열처리 중 양극 → 코팅 Li 확산 ③ 표면 LiOH · Li₂CO₃ · Li₂O 와의 반응 · 삼원 산화물 (Li₂SiO₃ · LTO · LiTaO₃ · LiAlO₂ · **Li₂O–ZrO₂** · LiNbO₃) 이 가장 흔하다 (refs 114–122) · Li₂SiO₃ > SiO₂ (ref 117).
- 비정질 LNO **10⁻⁵ S/cm** vs 결정 **10⁻¹¹ S/cm** (지면 6897) ⚠ 같은 쪽 앞 문단은 비정질 LiNbO₃ / Li₃Nb₄O₆ 를 **10⁻⁶ S/cm** 로 적는다.
- 산화물 SE 쪽: Nb 층 → LCO–LLZO 계면 2600 → 150 Ω/cm² · 확산 길이 100 → 20 nm (refs 107–108) · LBO: 35 → 80 mAh/g · CE 54 → 84 % (ref 109) · NbO₂ 가 LATP–LCO 의 Co₃O₄ 상변화 억제 (ref 110).
- 할라이드 SE (Li₃InCl₆ · Li₃YCl₆) 를 코팅으로 (LCO 와 안정 · 4.2 V) · 5 V 급은 불화물.
- **장기 열화**: Al₂O₃ 45 층 ALD 가 LCO–LGPS 33 사이클 Co 분포를 35 → 17 nm (Woo · ⚠ ref 82 로 인쇄 · Woo 2012 는 ref 86) · LNO 층에 100 사이클 뒤 Co (`Fig. 19a,b` EELS — 본 그림: 코팅 ≈ 2.5–3 nm · 사이클 뒤 코팅 안 Co 신호 figure-read ≈ 3.3×10⁵ counts vs 벌크 ≈ 5×10⁵) · XPS 에 Co–S · −S⁰− · 아황산 · 황산 (`Fig. 19c` — ⚠ *"c-LCO"* 행 Ge 3d 창에 **Ta 4f** 봉우리가 보인다 → Ta 를 포함한 코팅이다 · 본문은 *"LNO-coated"* 로만 씀).

### 3e. 작동창 · 첫 CE · 탄소 (축 B② · B③)
- LSiPSCl (25 mS/cm) 첫 CE **39 %** vs Li₉.₆P₃S₁₂ (10⁻⁴ S/cm) **73 %** (ref 6 = litdb `kato2016_high_power_assb_lsipscl_superionic`).
- LCO 셀: LYC **94.8 %** · LYC/LYB 94.2 % · LPS **84.0 %** (`Fig. 5b` · ⚠ 전압축이 vs Li₀.₅In/Li⁺) (ref 48).
- LPSCl 은 첫 충전 2.5 V 부터 분해 · 250 mAh/g 충전 · 방전 용량 0 · NCA 셀에서 2.5–3.6 V 기울기가 둘째 충전에 사라짐 = **CEI 자기 부동태** (지면 6884) · Zhu 의 해석 = 열역학 (CEI 가 SE 보다 안정) + 속도론 (둘 다 전자 절연) (ref 52).
- NMC 4.3 → 4.8 V 에서 CEI 증가 (Koerver · XPS · ref 45) · LiI–Li₃PS₄ + NCA 는 I⁻/I₃⁻/I₂ 짝이 추가 분해 (ref 46).
- 탄소: SE σ_e **10⁻⁸–10⁻¹² S/cm** · 탄소가 많을수록 계면 저항 ↑ · 첫 CE ↓ (ref 66) · VGCF (≈ 24 m²/g) vs CB (≈ 80 m²/g): 첫 CE **71 → 78 %** (NCM811 · 탄소 1 wt% · ref 41) · NMC622 < 10 µm 가 유리 · 복합체 σ_e 2 자릿수 ↑ (ref 64 = litdb `strauss2018_…`).
- SE 자체 redox: Li₃PS₄:C 7:3 · 0.5–3 V · **185 mAh/g** 가역 (refs 69–71) · Li₇P₃S₁₁–C 225 mAh/g · Li₂S–Li₇P₃S₁₁–C **1182 mAh/g** (Li₂S 이론 초과 · `Fig. 9`).

### 3f. 기계 (축 C)
- 황화물 SE 영률 **18–25 GPa** vs 산화물 **160–180 GPa** (refs 130, 137–140 · 원전 litdb: `sakuda2013_sulfide_mechanical_property` · `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` · `deng2016_elastic_superionic_electrolytes_dft`).
- 70(0.5Li₂S·0.5P₂S₅)·30LiI 유리: E 23 → 19 GPa · σ 2.2×10⁻⁴ S/cm 로 같아도 Si 음극 용량 10 % ↑ · 첫 CE ↑ (Kato · refs 140–142).
- 75Li₂O·25P₂O₅ 유리는 같은 황화물 유리보다 변형성이 2 자릿수 낮다 · Na 황화물 유리가 Li 유리보다 잘 변형된다 · Li₂S 함량 ↑ → 변형성 ↓ · E ↑.
- LPS 유리 G **7.1 ± 0.3 GPa** · Li G ≈ 4 GPa → Monroe–Newman 기준 G_SE > 8 GPa · Li 탄성의 방위 의존 (111) 1.5 – (100) 11 GPa · 입계 강성 20–60 % 낮음 · MD 로 입계 전단계수 50 % ↓ (Siegel · ref 290).
- 파괴: LPS 유리 파괴에너지 **2.8 ± 1.8 J/m²** · Bucci CZM: 팽창 < 7.5 % 이고 SE 파괴에너지 > 4 J/m² 면 파괴 없음 (refs 150–151 = litdb `bucci2018_…` · `bucci2017_…`).
- operando 압력 (Koerver · `Fig. 20a,b` · 본 그림): ⚠ 본문 *"LCO/LTO 셀 +0.6 MPa"* — 그림 축은 *σ₁₁ / 10⁵ Pa* 라 **+0.6 × 10⁵ Pa = 0.06 MPa** (figure-read · `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` 판독과 같다) ⇒ **본문이 10 배 틀렸다** (§10-2) · NMC811 쪽은 음 (≈ −0.5 ~ −0.6 × 10⁵ Pa).
- 무가압 LCO–In 셀 11.4 mAh/g · 첫 CE 77.4 % (ref 145) · NMC–β-Li₃PS₄ 첫 CE **70.5 % vs 액체 85.9 %** (`Fig. 20e` — 본문은 *"Figure 20g"* 로 인용 ⚠).
- 응력 수용 4 전략 (`Fig. 21`): 연성 고분자 바인더 · 음/양 체적변화 짝 (NMC811 + 흑연) · 섞어서 상쇄 · 무변형 전극 (LTO · NMC532).
- **Li 금속** (§5.3): 항복 0.8 MPa · 자기확산 Ea 50 kJ/mol · 크리프 두 종 (확산 · power-law) · Doux (ref 146 = litdb `doux2020_stack_pressure_assb`): 상대밀도 87 % LPSCl 펠릿 · 25 MPa 로 젖힌 뒤 **75 MPa 즉시 단락 · 10 MPa 가 25 MPa 보다 단락까지 ≈ 5 배 · 5 MPa 무단락** (0.075 mA/cm²) · Kasemchainan (ref 292): 0.5 · 3 · **7 MPa (1 mA/cm² · 100 사이클 분극 불변) · 2 mA/cm² 에서 단락** · J_Li⁺migration ≤ J_diffusion + J_creep 꼴의 유속 균형.

### 3g. 음극 · Li 금속 (축 E)
- 세 유형 (`Fig. 26` · `Fig. 27` · 본 그림): ① 열역학 안정 (이원 Li₂S · Li₃P · Li₃N · LiCl · LiF · 분해 0) ② 이온전도 · 전자절연 SEI (LiPON · Li₃PS₄ · 아지로다이트) ③ 혼합전도 SEI · 계속 성장 (LGPS → Li–Ge 합금 · LATP · LLTO → Ti³⁺) + 동역학 안정 (LLZO · 0.05 V · −0.02 eV/atom · 젖음 불량).
- LGPS 분해에너지 −1.2 eV/atom · 산물 Li₂S (절연) · **Li₃P (*"an ionic conductor"*)** · Li–Ge 합금 (전자) → MIEC (ref 11 · in situ XPS `Fig. 28`).
- *"Only phosphorus-based sulfide SEs are known to be relatively stable with Li metal since the expected decomposition products … (Li₂S, Li₃P, and LiX) are insulating materials"* (지면 6910) — ⚠ 우리 원장과 충돌 (§7d).
- LPS 유리 + Li: 24 h 에 임피던스 +40 % · 이후 500 h 동안 < 10 % (ref 214) · Wenzel: Li₇P₃S₁₁ · Li₆PS₅Cl 의 계면 성장 속도가 LGPS 보다 느리다 (이 문장엔 번호가 없다 — 원전은 ref 213 Wenzel 2018 로 보인다 · 이어지는 *"LPS- or LPSX-based SEs can act as a thin protective layer between Li metal and LGPS"* 의 ref 59 = Shin 2014 는 `Table 1` 의 Li–In · LGPS · Li₃PS₄ 행과 맞다).
- Li₀.₅In 은 ≈ 1 mA/cm² 까지 덴드라이트 없음 vs Li 는 0.075 mA/cm² 에도 LPS 공극으로 성장 (Tatsumisago) · 반대 보고 (> 0.5 mA/cm² Li 사용) 도 있다 — 셀 제작 (압력 · Li 출처 · 양) 차이로 설명.
- O 치환 LGPS: Li₁₀GeP₂S₁₁.₇O₀.₃ **8.43×10⁻² S/cm** vs LGPS **1.12×10⁻² S/cm** (stated · ⚠ 원전 대조 필요 — 84 mS/cm 는 보통 보고되는 LGPS 계 값보다 한 자리 높다) (ref 229) · Li₆PS₄.₇O₀.₃Br · MoS₂ · ZnO 도핑 계열.
- Li₃N · Li₃P 상온 σ 10⁻⁴–6×10⁻³ S/cm · 산화 안정 낮음 · LiCl · LiF 는 산화 안정 높고 σ 매우 낮음 · LiF 얇은 층이 유망.
- 산화물 SE: CCD < 0.5 mA/cm² · Si 10 nm (PECVD) on LLZO: 925 → 127 Ω/cm² · Mg 5–10 nm 는 좋고 100 nm 는 나쁨 · PVDF-HFP 겔 1400 → 214 Ω cm² · 깨끗한 LLZO 표면 2 Ω/cm² (0.3 mA/cm² 수백 h) · 습기 σ 6.46 → 3.62×10⁻⁴ S/cm · Ga-LLZO 입계 2.4×10⁻³ vs Al-LLZO 2.4×10⁻⁴ S/cm · 입경 5 → 600 *"mm"* (⚠ µm 오기) 에 CCD 0.3 → 0.6 mA/cm².
- `Table 1` (음극 보호층 17 행 · PDF 텍스트 · 본문 지면 6910 은 같은 층을 *"LiHPO₄"* 로 적고 표는 *"LiH₂PO₄"*): 예) Li–LGPS–LiH₂PO₄ 0.1 mA/cm² · 950 h · TiS₂ 86.7 %/500 · Li–Li₇P₃S₁₁–LiF 0.5 · 400 h · LCO 96.8 %/200 · Li–Li₃PS₄–LiₓSiSₓ 0.5 · 2000 h · LCO 94 %/100 · Li–LATP–ZnO 0.2 · 1000 h · LFP 99 %/200 · Li–LGPS–1 M LiTFSI DOL/DME 0.1 · 1600 h · TiS₂ 91.7 %/200.
- `Table 2` (Li 금속 — 액체 vs 고체): 고체 *"cyclable at very low current density (0.075 mA/cm²) with optimized stacking pressure"* · 액체 CE ≤ 99.4 % (0.5 mA/cm²) · > 500 Wh/kg 셀은 Li 효율 99.98 % 가 필요 (1000 사이클 80 %).

### 3h. 분석 기법 수치 (§6)
- EIS 주파수 구간: > 1 MHz bulk · 1 kHz–100 Hz 계면 전하이동 · ≈ 1 Hz Warburg (ref 338).
- 교환 NMR: **Li₆PS₅Cl–Li₂S 계면 자기확산 1×10⁻¹¹ vs LPSCl 벌크 9×10⁻⁷ cm²/s** (ref 172) — 계면이 Li⁺ 수송의 병목 · DFT-MD · 임피던스 · NMR SLR · 교환 NMR 로 10⁻¹² s – 0.1 s 를 잇는다.
- XAS 탐사 ≈ 100 nm vs XPS < 10 nm · Raman 공간분해 ≈ 1 µm vs XPS ≈ 50 µm.
- AFM 전위: LATP 코팅 NCM622 의 평균 전위 **0.214 V** — 무코팅보다 낮다 (stated · 무코팅 값은 리뷰에 없다) → 공간전하층 약화 (ref 330).
- in situ XPS: Li–Li₃PS₄ 계면 다층 Li⁰ / Li₂O / Li₃P / Li₂S / Li₃PS₄ (ref 334).
- 창 없는 EDS: Li Kα 54 eV · NDP: ⁶Li + n → ⁴He (2055 keV) + ³H (2727 keV) · LLZO · Li₃PS₄ 안 Li 직접 석출 → 높은 σ_e 가 덴드라이트 원인 (ref 341).

---

## 4. 계산 방법 ★ — 이 리뷰는 계산 0 · 소개하는 방법의 내용과 한계

- **code / functional / pseudo / k / ecut / U / 셀 / 시간 / 무질서 처리**: 전부 **n/a** — 리뷰이고, 소환한 계산의 조건도 하나도 적지 않는다.

### 4a. 계산 세 접근 (§6.1 — ref 80 Tang 2018 의 분류)

| 접근 | 리뷰 서술 | 주는 것 | 우리 대응 |
|---|---|---|---|
| 1 | *"fast diffusion of an alkali ion in a SE"* → *"predicted electrochemical window"* | 알칼리만 빨리 움직인다고 보고 μ_Li 를 연 grand potential → 전기화학 창 (이름이 낯설지만 내용은 Li 열린계) | `esw_grand_potential.py` (층 ①) |
| 2 | *"multispecies equilibrium between two materials"* | 모든 원소가 평형하도록 섞은 pseudo-binary 반응에너지 · 상도 | `interface_reactivity_v2.py --closed` (pymatgen `InterfacialReactivity`) |
| 3 | *"explicit interface simulation by finite-temperature AIMD"* — *"the most realistic picture"* | 계면 결합 형성의 시간 순서 (RDF-시간) | [혁주] MD 카드 (UMA · proposed) |

리뷰의 단서 (stated): 셋 다 한계가 있고 섞어 써야 한다 · 계산은 작은 셀 · 짧은 시간이라 실제 운전과 멀다.

### 4b. grand potential (`Fig. 3b`)
세로축 *"Li uptake per f.u."* — 0 인 구간이 안정. 이 그림은 1.73–2.36 V 의 0 구간을 **Li₂S + LiCl + Li₃PS₄ 중성 분해**로 표시한다 ⇒ LPSCl 을 hull 위 (준안정) 그대로 둔 판으로 읽힌다 — [Zhu15] 의 *E_hull → 0 규약*과 다르고 우리 꼴과 같다 (우리 해석 · `zhu2015_…` §10b 판정 ③).

### 4c. pseudo-binary — **단위 함정** (`Fig. 10` vs `Fig. 18a`) ★★
- `Fig. 10` (ref 11 Zhu 2016): **meV/atom** · x = SE 몰분율 — 우리 `InterfacialReactivity(norm=True)` 와 같은 정규화.
- `Fig. 18a` (ref 51 Banerjee 2019): **eV/f.u.** · x 는 *"(1−x) LiPSCl + x NCA"* (위 축 *"x LiNbO₃"*) — **f.u. 정의가 그림 · 캡션 · 본문 어디에도 없다**.
- **우리 산수 (원전 안의 내부 대조)**: LNO 곡선을 *혼합 화학식단위* (LPSCl 13 원자 + LiNbO₃ 5 원자 · x = 화학식 분율) 로 읽으면 최소 −1.3 eV/f.u. @ x ≈ 0.5–0.6 → **−0.14 ~ −0.16 eV/atom** — 같은 원전의 `Fig. 17` E_rxn^SE(LiNbO₃) **−0.16** 과 맞는다. 같은 읽기를 NCA 곡선 (NCA = LiMO₂ 4 원자) 에 적용하면 −21 eV/f.u. @ x ≈ 0.37 → **≈ −2.2 eV/atom** — 문헌 · 우리 범위 (−0.3 ~ −0.7 eV/atom) 의 3–7 배라 맞지 않는다 ⇒ NCA 쪽은 **더 큰 화학식단위 (정수 슈퍼셀 꼴 조성)** 로 넣었을 가능성이 높다 (추정 · 예: 80 원자 꼴이면 ≈ −0.56 eV/atom).
- ⇒ **`Fig. 18a` 두 곡선의 깊이 비 (≈ 16 배) 를 반응성 비로 읽지 않는다** — 같은 축에 그렸지만 f.u. 크기가 다를 수 있다. 원전 (ref 51) 의 방법 절로 확정할 때까지 이 그림에서는 **곡선 모양 (최소 위치 · 산물 이름)** 만 쓴다.

### 4d. AIMD
- **Tang 2018** (`Fig. 12b` · 본 그림): NaCoO₂ / Na₀.₅CoO₂ – Na₃PS₄ 계면 AIMD (캡션 *"70 ps"* · 그림 세로축 ≈ 60 ps) · S–O · Co–S 쌍 RDF 를 **시간 축 히트맵**으로 · 기준상 RDF (Na₆S₂O₉ · Na₂S₂O₇ · CoSO₄ · Co₂(SO₄)₃ · Co₉S₈ · CoS₂ · Co₃S₄) 와 겹쳐 산물을 판정 · **S–O 는 충전 (Na₀.₅CoO₂) 에서만 즉시 생기고 · Co–S 는 둘 다** · Na–Na 결합은 충전 계면에서 사라진다 (stated).
- **Banerjee (NCA–LPSCl)**: P–O · S–S · Ni–S · Co–S 결합 형성 (본문 한 줄 · 조건 0).
- ⚠ 두 계산 다 functional · 온도 · 셀 · 앙상블이 리뷰에 없다 → 우리 MD 관측창 규칙 (`D-2026-10-05-md-observation-window` · Ea₁ = kT ln(ν₀ t n)) 을 대려면 원전이 필요하다.

### 4e. 코팅 스크리닝 지표 (`Fig. 17`)
E_hull · E_rxn (양극 · SE 각각) · ΔV (반응 부피 변화 — Tang 2018 의 짝 지표) · grand-potential 창 · R_c · σ · 띠틈 — Xiao 2019 (ref 99) 다목적 깔때기와 같은 계열이고, 실제로 σ · 띠틈 표와 창 막대는 각각 [Xiao19] · [Zhu15] 값을 옮긴 것이다 (§3d).

### 4f. 공간전하층
AIMD · DFT 가 산화물 양극–황화물 SE 계면의 Li 결핍층을 예측 (refs 92–94 · ref 92 = litdb `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`) · **직접 관측 0** (LiPON–LCO 에서 Kelvin probe · 전자 홀로그래피만 · refs 97–98) · LTO 가 첫 충전 기울기를 없애는 해석도 *"still based on hypotheses"* (리뷰 자인 · 지면 6897).

### 4g. 안 주는 것
계산 조건 전부 · hull 판 (MP 몇 년판인지) · LPSCl 준안정 처리 규약 · AIMD 관측창 — n/a.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | 계면 13 시나리오 — 공극 (5 · 7 · 8 · 9 · 10 · 12) / 화학 (1 · 6) / 전기화학 (2 · 3 · 6 · 13) / 입계 (4 · 11) · **코팅 양극–SE 접촉 (2) 은 '전기화학' 칸** (본 그림) | 계면 지도 — 우리 계산 위치: 무코팅 양극–SE 화학 (1) · 코팅–SE (2) · Li–SE (6) |
| 2 | HOMO/LUMO 띠 도식 (액체 · 황화물 · 산화물 · 염화물 · 축 값 없음 · 본 그림) | ⛔ 띠틈 = 창 으로 읽게 만드는 도식 — 우리 규율 (띠틈 ≠ 안정 전압) 의 반례로만 |
| 3a–d | 평판 CV 무반응 / LPSCl grand potential 계단 / SE–C CV 봉우리 / 창 막대 4 종 (본 그림) | LPSCl 창 1.73–2.36 V (figure-read) · 계단 산물 — 우리 ESW 대조 (§7a) |
| 4 | 전압 지도 + PS₄³⁻ redox 사다리 (ref 45 · 저작권 표기 불일치 · 본 그림) | B② 산물 사다리 (Li₄P₂S₇ · Li₂P₂S₆ · S⁰) — 우리 P₂S₇ + S 계단과 같은 계열 |
| 5a,b | LPSCl–C vs LYC–C 충전 (2.3 V 기울기 vs ≈ 4.1 V 평탄) · LCO 셀 첫 CE 94.8 / 94.2 / 84.0 % (b 축 vs Li₀.₅In · 본 그림) | 할라이드 vs 황화물 산화의 실측 대조 |
| 6a,b | NCM 입경 효과 · LCO–LGPS 탄소 유무 첫 충전 기울기 (안 봄) | — |
| 7a–d | CB vs VGCF SEM · 충전 곡선 · 첫 CE 71 → 78 % (안 봄) | 탄소 표면적 ↔ 분해 속도 |
| 8a–c | LPSCl–C CV 0–4.2 V · 상태별 Nyquist · 가역 경로 도식 (ref 41 · 본 그림) | 4.2 V 산물 S · P₂S₅ · LiCl · 임피던스 10^1.7 → 10^3.8 Ω (figure-read) |
| 9a,b | Li₇P₃S₁₁–C · Li₂S–Li₇P₃S₁₁–C 용량 · dQ/dV (안 봄) | — |
| 10 | SE–LCO / SE–L0.5CO mutual 반응에너지 (meV/atom · ref 11 · 본 그림) | ✅ 우리와 같은 정규화 · LPS −405 / −564 · LGPS −340 / −499 |
| 11a,b | NCM–LPS vs NCM–LATP 50 사이클 · EIS (ref 79 · 캡션 '150 °C' 의문 · 본 그림) | 인산염 SE 의 낮은 반응성 실측 (50 사이클 figure-read ≈ 86 vs 77 mAh/g) |
| 12a,b | Na 전극 × SE 반응에너지 · 부피 변화 / AIMD RDF-시간 히트맵 (ref 80 · 본 그림) | ★ [혁주] MD 판독법 후보 (결합쌍 RDF 의 시간 진화) |
| 13a–e | 휴지 유무 충방전 · 유지율 · 시간 EIS (무코팅 vs LNO · ref 85 · 본 그림) | 화학 반응의 시간 축 · `jung2019_…` 와 짝 |
| 14a–d | 액체 충전 NCA@4.3 V + LPSCl → XRD · Raman (Ni₃S₄ · Li₃PO₄ · LiCl · ref 51 · 본 그림) | ★ 화학 / 전기화학 분리 설계 · [혁주] XPS 해석의 대조 산물 |
| 15a–i | 황화물 · 산화물 계면 반응 도식 (코팅 *"LNO, LTO. LZO etc."* 명시 · 본 그림) | 코팅 = 화학 반응 차단 · 충전 상태 전기화학 분해 (S · P₂S_y) 는 남음 (e) — [혁주] 해석 틀 |
| 16a–c | LLZO–LCO 500 °C XRD · FIB · EDX (ref 91 · 안 봄) | — |
| 17 | 코팅 스크리닝 네 칸 (ref 51 · 창 = [Zhu15] · σ / 띠틈 = [Xiao19] · 본 그림 · 확대 판독) | ★ 요청서의 '코팅 표' · Li₂ZrO₃ 는 σ · 띠틈 칸만 |
| 18a–c | NCA–LPSCl · LNO–LPSCl pseudo-binary (eV/f.u.) · LTO@LCO 두께별 Nyquist · 충전 곡선 (refs 51 · 83 · 본 그림 · 확대 판독) | ★ 요청서의 '혼합 반응에너지' · ⛔ 단위 함정 (§4c) · 두께 비단조 |
| 19a–c | LNO@LCO 100 사이클 Co 확산 EELS · LGPS XPS 1/10/100 사이클 (ref 127 · 본 그림) | 코팅의 장기 열화 실측 · Ta 4f (코팅 조성 확인 필요) |
| 20a–f | operando 압력 · SEM · FIB 균열 · 첫 CE · X선 CT (Sn) (본 그림) | ⚠ 압력 축 단위 10⁵ Pa — 본문 10 배 오기 |
| 21a–h | 체적 변화 상쇄 도식 (안 봄) | — |
| 22a,b | Li₂S–Li₆PS₅Br 2D-EXSY NMR · Li₂S–LiI 고용체 (안 봄) | — |
| 23a–f | 용액 등각 코팅 공정 · NaCrO₂ 단면 EDX (안 봄) | — |
| 24 | 용액 코팅 장단점 표 (안 봄) | — |
| 25a–d | 하이브리드 계면 (용매화 IL · 도전 바인더 · LiF-rich SEI) (안 봄) | — |
| 26 | Li 금속 대비 안정창 막대 (ref 30 재수록 · 본 그림 · 확대 판독) | ★ Li₂ZrO₃ ≈ 0.27–3.40 V · LPSCl ≈ 2.08–2.29 V (figure-read) |
| 27a–f | Li 금속 계면 세 유형 + 친리튬 코팅 도식 (본 그림) | E 축 — Li₃P 를 '안정 계면' 칸에 둔다 (우리와 충돌 · §7d) |
| 28a–c | LGPS + 증착 Li in situ XPS · 임피던스 (ref 333 ⚠ · 안 봄) | — |
| 29a–i | Na₃PS₄ · Na₃SbS₄ 와 Na 금속 · CPEO 보호 (refs 222 · 225 · 안 봄) | — |
| 30a–d | 스택압 · Li 대칭셀 · NCA 셀 5 vs 25 MPa (ref 146 · 안 봄) | `doux2020_stack_pressure_assb` 로 |
| 31a–c | Li 이동 · 공공 확산 · 크리프 도식 (안 봄) | — |
| 32a–k | 스택압 · 공극 · 덴드라이트 도식 + nano-CT (안 봄) | — |
| 33 | NCA–LPSCl cryo-STEM EDS (Ni · Co · P · S · Cl · ⚠ 'ref 52' 로 인쇄 · 본 그림) | Co · S 계면 편석 — 산물 위치의 직접 증거 |
| 34a–d | in situ CT · XPS · Raman · NDP 장치 (안 봄) | — |
| Table 1 | 음극 보호층 17 행 (PDF 텍스트) | E 축 보호층 목록 |
| Table 2 | Li 금속 — 액체 vs 고체 비교 (PDF 텍스트) | — |

---

## 6. Post-processing ★

- **무엇** — grand-potential Li 흡수 계단 (`Fig. 3b`) · pseudo-binary 최소 kink (`Fig. 10` · `Fig. 18a`) · 코팅 히트맵 (`Fig. 17`) · RDF-시간 히트맵 (`Fig. 12b`) · Li 금속 대비 창 막대 (`Fig. 26`) · XPS S 2p / P 2p / Ge 3d 분해 (`Fig. 19c`) · 충전 분말 혼합 XRD / Raman (`Fig. 14`) · cryo-STEM EDS (`Fig. 33`) · 시간 / 상태별 EIS (`Fig. 8b` · `Fig. 13d,e` · `Fig. 18b`) · operando 응력 (`Fig. 20a,b`).
- **도구** — 리뷰는 안 적는다 (원전 기준으로 Materials Project · pymatgen 계열로 보인다 — 추정).
- **우리가 가져올 판독법 둘**: ① **RDF-시간 히트맵** — 계면 MD 에서 결합쌍이 *언제* 생기는지를 기준상 RDF 와 대어 산물로 판정한다 ② **'액체로 충전한 양극 + SE 혼합'** — 전기화학 바이어스 없이 화학 반응만 떼는 실험 · 계산 쪽 짝은 양극 y 별 닫힌계 혼합 곡선 (우리 stage 1).

---

## 7. 우리 DFT 대비 ★★ (`../our_dft_baseline.md` · `db/properties/`)

### 7a. 양 대조표 — 무엇이 같은 양인가

| 항목 | 이 리뷰 (소환값) | 우리 | 같은 양인가 / 차이 이유 |
|---|---|---|---|
| LPSCl 산화 개시 | 2.3 V (본문) · ≈ 2.36 (`Fig. 3b` · `Fig. 17` figure-read) · ≈ 2.29 (`Fig. 26`) | **2.256 V** (MP2026 · GG 집합 · LiS₄ · SCl₃ · Li₅PS₄Cl₂ 제외 · `our_dft_baseline.md`) | 같은 양 (grand potential 층 ①) · 0.03–0.10 V 차 = hull 세대 · S 음이온 보정 · LiS₄ entry (`zhu2015_…` §10b 판정 ②) — **실차이가 아니라 방법 의존** |
| LPSCl 환원 한계 | 1.7 V (본문) · ≈ 1.73 (`Fig. 3b`) · ≈ 2.08 (`Fig. 26`) | **1.717 V** (교환 0 의 아래 가장자리 · 창 0.539 V) | 본문 · `Fig. 3b` 와 같은 양 · Δ ≤ 0.02 V ✓ · `Fig. 26` 은 구성이 다르다 (§10-2) |
| LPSCl 산화 계단 | 2.36 (−2) → 2.64 (−5 · P₂S₅, LiCl, S) → 3.30 V (−6) | 2.256 (−2 · 원소 S) → 2.385 (P₂S₇ + S) → 3.326 V (SCl) | 끝 계단 3.30 ≈ 3.33 V (Δ 0.03 · figure-read) · 중간 산물은 DB 의존 (P₂S₅ vs P₂S₇) |
| SE–LCO 혼합 | LPS −405 · LGPS −340 · 탈리튬 −564 · −499 meV/atom (Zhu 2016) | LPSCl×LiCoO₂ −322.7 · ×Li₀.₅CoO₂ −454.9 meV/atom (cascade 앵커) | 같은 정규화 · **다른 SE** (Li₃PS₄ ≠ Li₆PS₅Cl) — 값 비교 안 함 · 탈리튬하면 ≈ −130 ~ −160 meV/atom 더 음으로 가는 방향은 같다 |
| NCA–LPSCl · LNO–LPSCl 혼합 | eV/f.u. (≈ −21 · −1.3 figure-read) | [혁주] stage 1 (meV/atom · 닫힌계) | ⛔ 같은 축 비교 금지 (stage 1 카드 §5b) · 단위 · 정규화부터 다르다 (§4c) |
| 코팅 창 Li₂ZrO₃ | `Fig. 26` (Richards 2016) ≈ 0.27–3.40 V | **0.05–3.40 V** (MP2026 · LiO8 제외 판 · stage 1b) | 같은 양 (MP grand potential) · **산화 한계 Δ ≈ 0** (판독 ±0.03 V) · 환원 쪽 ≈ 0.2 V 차 = hull 세대 (우리 환원 첫 계단 Li₆Zr₂O₇ + Zr₃O) |
| 코팅 창 LTO 등 | `Fig. 17` = [Zhu15] SI (LTO ≈ 1.77–3.71) | (안 돌림) | — |
| Li₂ZrO₃ 띠틈 | 3.99 eV (`Fig. 17` 표 = [Xiao19] Table 2) | 위치만: `hyeokju_lzo_stage2a_li2zro3_gap_card_2026_11_16.json` `결과_2026_11_17` | ⛔ 같은 축에 놓지 않는다 (2a 카드 §5b *"문헌 그림 값과 같은 축에 놓지 않는다"*) |
| Li₃P 성격 | *"an ionic conductor"* · 안정 계면 칸 (`Fig. 27a`) · *"insulating"* (지면 6910) | `sei_products.json` **conductor-LEAK** (MP 띠틈 0.70 eV · 문턱 < 2 eV) | 🔴 충돌 — [Xiao20Rev] 에 이은 둘째 문헌 (§7d) |
| 영률 | 황화물 18–25 GPa (여러 원전 혼합) | comp1 22.06 · modelc 27.66 GPa (E_VRH · relaxed-ion) | 다른 양 (실험 유리 · 펠릿 · DFT 가 섞인 범위) — 원전 digest 로 대조 |

### 7b. ★ [혁주] LZO 코팅 트랙과 닿는 곳 (의뢰 질문 ②)

**우리 원장** (2026-11-16/17 · [혁주] 1저자 = 혁주 · 계산 = 사용자 · 아래는 각 카드의 허용 문장 그대로):
- **stage 1** (`db/properties/hyeokju_lzo_stage1_reactivity_card_2026_11_16.json` `결과_2026_11_16` · MP GGA/GGA+U · pymatgen · 닫힌계 · 0 K · 혼합물 원자당): *"LZO (Li₂ZrO₃)–Li₆PS₅Cl 혼합의 최소 반응에너지는 −92 meV/atom 이고 산물 후보는 Li₃PO₄ · ZrO₂ · Li₂S · LiCl"* · *"NCA_y–LZO 는 y 1.0 에서 0 (반응 없음) 이고 y 0.2 에서도 −25 ~ −28 meV/atom · NCA_y–Li₆PS₅Cl 은 −377 ~ −389 (y 1.0) → −681 ~ −696 (y 0.2)"* (이름 추정 조성 NCA721 · NCA811) · *"산물 후보는 열역학 후보이고 실제 CEI 성분 확정이 아니다"*.
- **stage 1b** (`…_stage1b_li2zro3_window_card_2026_11_17.json` `결과_2026_11_17`): *"Li₂ZrO₃ 는 0.05 V 아래에서 환원 분해하고 3.40 V 위에서 산화 분해한다 (산화 첫 계단 산물 ZrO₂ + O₂)"* (LiO8 제외 판).
- **stage 2a**: Li₂ZrO₃ PBE 띠틈 (fixed-occ nscf) — 값은 카드에만 둔다 (§7a 마지막 줄 규칙).

| 우리 원장의 물음 | 이 리뷰 | 판정 |
|---|---|---|
| LPSCl–LZO 반응에너지의 문헌값 | **없다** — `Fig. 17` 반응 칸에 Li₂ZrO₃ 가 없다 | 같은 양의 문헌값은 **[Xiao19]** (litdb ✅ `xiao2019_cathode_coating_screening` §4c): **LPSCl/Li₂ZrO₃ −88 meV/atom (MP2018) · 산물 Li₂S · Li₃PO₄ · Li₂ZrS₃ · LiCl** — 우리 −92 와 4 meV/atom 차 · **Zr 쪽 산물이 다르다 (Li₂ZrS₃ ↔ ZrO₂)** = hull 세대가 산물 목록을 바꾼다 |
| NCA–LPSCl 혼합 곡선 | `Fig. 18a` (eV/f.u. · NCA 충전 상태 미표기 · AIMD 없음) | ⛔ 같은 축 비교 금지 (stage 1 §5b) — **각자 축 안의 순서만**: 문헌 LNO–LPSCl ≪ NCA–LPSCl · 우리 LZO–LPSCl (−92) ≪ NCA–LPSCl (−377 ~ −696) — 같은 방향 |
| 산물 | NCA@4.3 V + LPSCl: **Ni₃S₄ · Li₃PO₄ · LiCl** (XRD · Raman) · 방전 상태 NiS · CoS · MnS · Li₂S · LiPₓCl_y · LiCl · 사이클 뒤 POₓ · SOₓ · Ni₃(PO₄)₂ | 우리 LPSCl–NCA 산물 Li₃PO₄ · Li₂SO₄ · Ni₃S₂ · Co₉S₈ (또는 Co₂NiS₄) · LiAlO₂ / Li₅AlO₄ · Li₂S · LiCl — **클래스 일치 (TM 황화물 + Li₃PO₄ + LiCl)** · Ni 황화물 화학량은 다르다 (실측 Ni₃S₄ · 우리 Ni₃S₂) · Li₂SO₄ 는 리뷰의 XRD 에 없다 (SOₓ 는 XPS) |
| LZO 의 산화 한계 | *"most of the oxide-based coating materials are not stable at voltages greater than 4 V … O²⁻/O₂"* · *"Although the electrochemical stability of these oxide materials is limited to 4 V, their low electronic conductivity … may result in long cycle life"* · `Fig. 26` Li₂ZrO₃ ≈ 3.40 V | 우리 3.40 V 와 **같은 양 · 같은 값** (판독 범위 안). 리뷰의 *'열역학 창은 위치 · 속도론이 수명을 정한다'* 는 1b 카드 §5b (*'LZO 코팅이 4.4 V 에서 분해된다 / 보호하지 못한다' 를 말하지 않는다*) 와 같은 선이다 |
| 'LZO' 라는 이름 | `Fig. 15` 도식 *"Apply Resistive Coating (LNO, LTO. LZO etc.)"* — 코팅이 화학 반응을 막고 (d) 충전 상태 전기화학 분해 (S · P₂S_y) 는 남는다 (e) | 혁주 문서의 *'두 계면 따로로는 차단 효과를 증명하지 못한다'* 선과 같은 틀 (도식이지 데이터가 아니다) |
| 문헌 셀 전압의 기준 | `Fig. 5b` 는 vs Li₀.₅In · `Fig. 14a` 는 vs Li⁺/Li⁰ | 문헌 셀 전압을 옮길 때 기준 전극부터 본다 (혁주 셀은 Li/Li⁺ · 11-17 확인) |
| 4.3 V ↔ Li 함량 | `Fig. 14a`: NCA (Ni₀.₈Co₀.₁₅Al₀.₀₅) 4.3 V ≈ Li₀.₂₈ (figure-read · 액체 반쪽전지 C/100 + CV) | ⛔ 우리 y 격자의 전압 라벨로 쓰지 않는다 (stage 1 §5b · G5 — 혁주 충전 용량 대기) · 문헌 참고값으로만 |

### 7c. ESW — 우리 B① 과
- 리뷰의 LPSCl 창 (본문 1.7 / 2.3 V · `Fig. 3b` 1.73–2.36 V) 은 **우리 정의 (Li 교환 0 구간) 와 같은 구성**이고 값도 0.1 V 안이다 — 우리 1.717–2.256 V (창 0.539 V).
- 우리 셀 작동창 2.5–4.25 V (vs Li/Li⁺) 에서 보면: LPSCl 산화 개시 (우리 2.256 · 리뷰 2.3) 는 창 아래 → **창 전체가 열역학적 산화 구간** → '안정' 은 창 안의 산물 · 부동태로 판단한다 (CLAUDE.md 규율) — 리뷰의 *'첫 사이클 CEI 자기 부동태'* (지면 6884) 가 바로 그 서술의 실측 쪽이다.

### 7d. 산물 · 음극 (E)
- 리뷰는 Li₃P 를 *"an ionic conductor"* (지면 6908) · *"insulating materials that are thermodynamically stable with Li metal"* (지면 6910) 로 두 번 쓰고 `Fig. 27a` 에서 '안정 계면' 칸에 넣는다. 우리 `sei_products.json` 은 MP 띠틈 0.70 eV (< 2 eV 문턱) 로 **conductor-LEAK** 이다 ⇒ [Xiao20Rev] 에서 정한 처리와 같이, 인용할 때 *"MP 띠틈 기준 전자 누설 후보 (연속성 · 두께 · 이웃 상에 따라 부동태일 수 있다)"* 라는 조건절을 붙인다.

### 7e. 섞으면 안 되는 것
- `Fig. 18a` 의 eV/f.u. 를 우리 meV/atom 옆에 — 금지 (단위 + stage 1 §5b).
- `Fig. 17` 의 띠틈 3.99 eV 를 우리 PBE 띠틈과 같은 축에 — 금지 (2a §5b).
- `Fig. 17` 의 E_rxn · ΔV (단위 미인쇄) 를 우리 표에 — 단위를 원전으로 확정하기 전 금지.
- 리뷰가 인쇄한 ref 번호를 원전 확인 없이 인용 — §9d.

---

## 8. 적용 인사이트

- ① **[혁주] 요청서의 '참고 그림' 을 바로잡을 근거**: 그 그림은 원전 ref 51 의 그림이고, 이 리뷰의 재수록에서 보이는 세로축은 eV/f.u. (정의 없음) 다 — 우리 stage 1 곡선 (meV/atom) 과 같은 축에 놓으면 안 되는 이유가 카드 규칙 (§5b) 말고도 **물리적으로** 하나 더 생겼다 (§4c).
- ② **LZO 의 같은 양 문헌값은 [Xiao19] 에 있다** (−88 meV/atom · 산물에 Li₂ZrS₃): 혁주의 XPS 해석에서 Zr 3d 로 가를 후보가 ZrO₂ (우리 MP2026) 와 Li₂ZrS₃ (MP2018 판) 로 갈린다 — 추가 계산 0 건으로 말할 수 있는 'hull 세대가 산물을 바꾼다' 사례다 (사용자 판단으로 혁주에게 알릴지).
- ③ **실험 설계 차용**: `Fig. 14` 의 *'액체로 충전한 양극 + SE 혼합'* 은 우리 닫힌계 y-스캔의 실험 짝이다 — 혁주에게 같은 설계 (충전 NCA + LPSCl · LZO 코팅 유무) 를 제안할 수 있다 (사용자 결정).
- ④ **MD 판독법**: `Fig. 12b` 의 결합쌍 RDF-시간 히트맵 (S–O · Co–S) 을 [혁주] MD 카드의 판독 정의 후보로 (Zr–S · P–O · S–O · Ni–S) — 관측창 한 줄 (Ea₁ · Ea₉₅) 을 같이 싣는다.
- ⑤ **인용 감사**: 이 리뷰를 거쳐 원전을 찾을 때는 번호가 아니라 제목 · 저자로 찾는다 (§9d · 9 곳).

---

## 9. 참고문헌 지도 ★★ (의뢰 질문 ①)

### 9a. 머리 수치
- **341 편** (번호 1–341 · 마지막 = Han 2019 *Nat. Energy* 4, 187) · 같은 작품 중복 수록 **3 쌍** (51 = 327 Banerjee 2019 *ACS AMI* · 167 = 174 Hakari 2017 · 175 = 177 Lin 2013) ⇒ 서로 다른 작품 **338 편**.
- **litdb 에 이미 자기 digest 가 있는 것: 21 편** (6.2 % · 제목 문자열 + slug 첫 저자·연도 두 경로로 찾고 하나씩 눈으로 확인 — 같은 성 · 같은 해의 다른 논문 (slug 경로 11 건) 과 제목 앞부분만 같은 다른 논문 (제목 경로 10 건) 은 걸러냈다):
  ref 5 `kamaya2011_lgps_lithium_superionic_conductor` · 6 `kato2016_high_power_assb_lsipscl_superionic` · 11 `zhu2016_first_principles_interface_stability_assb` · 12 `haruyama2017_cation_mixing_co_diffusion_lco_lps` · 30 `richards2016_interface_stability_pseudobinary` · 52 `zhu2015_esw_grand_potential_origin` · 64 `strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation` · 85 `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` · 92 `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` · 99 `xiao2019_cathode_coating_screening` · 136 `sakuda2013_sulfide_mechanical_property` · 138 `deng2016_elastic_superionic_electrolytes_dft` · 139 `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` · 143 `tian2017_contact_area_loss_assb_simulation` · 144 `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` · 146 `doux2020_stack_pressure_assb` · 150 `bucci2018_mechanical_instability_interface_delamination` · 151 `bucci2017_chemomech_failure_assb_cycling_czm` · 153 `bielefeld2019_microstructural_modeling_composite_cathode` · 181 `sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode` · 206 `kawaguchi2018_dry_coating_model_se_particle_powtec`.
- 자기 카드는 없고 **다른 digest 에 2 차 인용으로만** 나오는 원전 (같은 제목 문자열 검색): ref 75 Koerver 2017 *Chem. Mater.* (digest 6 곳) · 145 Zhang 2017 *JMCA* 압력 모니터 (4) · 87 Auvergniot 2017 (2) · 66 Zhang 2017 탄소 (2) · 37 Wenzel 2016 (2) · 338 Zhang 2017 *ACS AMI* (2) · 그 밖에 1 곳씩 ref 1 · 10 · 31 · 38 · 42 · 43 · 93 · 94 · 95 · 119 · 125 · 140 · 147 · 193 · 194 · 197 · 213 · 286 · 288 · 322.

### 9b. 주제별 지도 (첫 인용 절 기준 · 14 묶음 · ✅ = litdb 자기 digest)

| 묶음 | 편수 · ✅ | 핵심 원전 (ref 번호 · 1저자 연도 · 무엇) |
|---|---|---|
| **T1 개관 리뷰 · SE 소재** (§1) | 15 · ✅ 2 | ✅ 5 Kamaya 2011 (LGPS) · ✅ 6 Kato 2016 (LSiPSCl · 고출력 셀) · 3 Wang 2015 *Nat. Mater.* (bcc 음이온 골격 설계 원리) · 4 Mizuno 2005 (Li₇P₃S₁₁) · 7 Xu 2018 *Joule* (계면 리뷰) · 13 Wang 2020 *Chem. Rev.* (가넷) · 17 Zhao 2020 *Nat. Rev. Mater.* · 2 Manthiram 2017 |
| **T2 ESW · 전기화학 창** (§3.1 등) | 22 · ✅ 2 | ✅ 30 Richards 2016 (pseudo-binary · `Fig. 26`) · ✅ 52 Zhu 2015 (ESW 원전 · `Fig. 17` 창 칸) · 8 Han 2016 *AEM* (LGPS · LLZO 창 실측) · 31 Ong 2008 (grand potential 원전) · 37 Wenzel 2016 *Chem. Mater.* (LGPS–Li) · 40 Swamy 2019 · **41 Tan 2019 *ACS Energy Lett.* (LPSCl 가역 redox · `Fig. 7` · `Fig. 8`)** · **42 Dewald 2019 *Chem. Mater.* (실용 산화 안정)** · 43 Wang 2019 *Angew.* (염화물 · 브롬화물 창) · 21 Goodenough–Kim 2010 (HOMO/LUMO 도식 원전) · 53 Perdew 1985 (띠틈 문제) · 56 Yu 1997 (LiPON) |
| **T3 작동창 · 분해 속도론 · 탄소 · SE redox** (§3.2–3.4) | 23 · ✅ 1 | ✅ 64 Strauss 2018 · **45 Koerver 2017 *JMCA* (redox-active CEI · `Fig. 4` 출처)** · 48 Asano 2018 *Adv. Mater.* (할라이드 4 V · `Fig. 5`) · 49 Banerjee 2019 (산황화물 motif 설계) · 50 Suzuki 2016 (LPSO) · 65 Oh 2016 (5 V LNMO–LGPS) · **66 Zhang 2017 *ACS AMI* (탄소 첨가제의 해)** · 67 Culver 2018 · 68 Ates 2019 · 69 · 70 Hakari 2017 (Li₃PS₄ 자체 활물질) · 72 Suzuki 2018 |
| **T4 양극–SE 계면 반응** (§4.1.1–4.1.2 · 4.1.5) | 25 · ✅ 3 | ✅ 11 Zhu 2016 (`Fig. 10`) · ✅ 12 Haruyama 2017 (Co 확산 · 양이온 혼합) · ✅ 85 Jung 2019 (`Fig. 13`) · **51 Banerjee 2019 *ACS AMI* 11, 43138 (`Fig. 14` · `Fig. 17` · `Fig. 18a` · `Fig. 33` 원전 · = ref 327)** · 9 Takada 2008 · 10 Sakuda 2010 (TEM 비정질 계면) · **75 Koerver 2017 *Chem. Mater.* (NCM–β-Li₃PS₄ 용량 감쇠)** · 79 Yoshinari 2019 (`Fig. 11`) · **80 Tang 2018 *Chem. Mater.* (Na 계면 반응 + AIMD · 세 접근 분류 · `Fig. 12`)** · 81 Lacivita 2019 (Na 계면 ab initio) · **87 Auvergniot 2017 *Chem. Mater.* (LPSCl vs LCO · NMC · LMO XPS)** · 89 Kim 2011 · 90 Park 2016 · 91 Vardar 2018 (LLZO–LCO) · 127 Zhang 2018 *ACS AMI* (LGPS–LCO 열화 · `Fig. 19`) · 128 Wang 2019 *Small Methods* |
| **T5 공간전하층** (§4.1.3) | 7 · ✅ 1 | ✅ 92 Haruyama 2014 · 93 Swift 2019 *PRL* (전위 · 공간전하 제1원리) · 94 Tateyama 2019 · 95 Ohta 2007 (LiNbO₃ 코팅 LCO 원전) · 96 Takada 2015 · 97 Masuda 2017 (KPFM) · 98 Yamamoto 2010 (전자 홀로그래피) |
| **T6 양극 코팅** (§4.1.4) | 28 · ✅ 1 | ✅ 99 Xiao 2019 (`Fig. 17` σ / 띠틈 표) · 104 Xie 2017 *ACS Nano* (LiAlF₄ ALD) · 105 · 106 LiNbO₃ 기계 · 107–110 산화물 SE 쪽 (Nb 층 · LBO · NbO₂) · 111 Hu 2009 (ZrO₂ · 액체 LIB) · 113 Sakuda 2009 · **115 Machida 2012 (ZrO₂ 코팅 NMC · 120 mAh/g 95 %)** · **116 Seino 2011 (LTO 코팅 NCA)** · 117 Sakuda 2010 (Li₂SiO₃) · 118 Noh 2013 (LLTO) · **119 Ito 2014 (Li₂O–ZrO₂ 코팅 NCA)** · 120 Sakuda 2008 · 121 Okada 2014 (LiAlO₂) · 122 Visbal 2016 (DLC) · 123 Ito 2015 · 124 Yubuchi 2016 (Li₃PO₄ 코팅 LNMO) · 125 · 126 Li 2019 (Li₃InCl₆) — ＋ T4 번호대에 있는 코팅 원전: 82 Jung 2018 (LBO–Li₂CO₃) · **83 Ohta 2006 (LTO 두께 · `Fig. 18b,c`)** · 84 Cao 2020 · 86 Woo 2012 (Al₂O₃ ALD) |
| **T7 기계 · 체적 변화** (§3 서두 · §4.2) | 34 · ✅ 9 | ✅ 136 Sakuda 2013 · ✅ 138 Deng 2016 · ✅ 139 McGrogan 2017 · ✅ 143 Tian 2017 · ✅ 144 Koerver 2018 · ✅ 146 Doux 2020 · ✅ 150 Bucci 2018 · ✅ 151 Bucci 2017 · ✅ 153 Bielefeld 2019 · 140 Kato 2018 (LiX 유리 기계) · 137 Nose 2015 · 145 Zhang 2017 (압력 모니터) · 147 Strauss 2020 (준무변형 NCM) · 148 Wu 2019 (operando CT) · 152 Hao 2018 · 154 Lewis 2019 · 22–29 SEI 기계 (액체계) |
| **T8 Li–S · Li₂S 양극** (§4.3) | 24 · ✅ 0 | 172 Yu 2016 (LPSCl–Li₂S 교환 NMR · ps → s 수송 · 아지로다이트) · 171 Yu 2017 · 167 Hakari 2017 (Li₂S–LiX 고용체) · 177 Lin 2013 (폴리설피도인산) · 176 Han 2016 · 162 Yue 2018 (리뷰) |
| **T9 등각 · 용액 · 하이브리드** (§4.4–4.5) | 32 · ✅ 2 | ✅ 181 Sakuda 2011 (PLD) · ✅ 206 Kawaguchi 2018 (건식 하이브리다이저) · 183 Park 2016 (Li₄SnS₄:LiI 용액) · 188 Banerjee 2016 (Na₃SbS₄) · 192–196 용액 아지로다이트 · 204 Kim 2017 (침투) · 208 · 209 Oh 2015 · 2019 · 210 Fan 2018 (LiF-rich SEI) |
| **T10 음극 화학 · 보호층** (§5.1 · `Table 1`) | 39 · ✅ 0 | 211 Chen 2017 · 212 Hartmann 2013 (NASICON–Li MCI) · **213 Wenzel 2018 *SSI* (아지로다이트–Li 계면 성장)** · 217 Bron 2017 · 218 Zhang 2018 · 222 Tian 2019 *Joule* (반응성 기반 Na 계면 설계) · 229 Sun 2016 (O 치환 LGPS) · 230 Zhang 2019 (O 치환 LPSBr) · 233 Li 2010 (Li₃N) · 237 Li 2018 · `Table 1` refs 269–278 |
| **T11 음극 접촉 · LLZO 젖음** (§5.2) | 29 · ✅ 0 | 240–243 (LLZO–Li 계면) · 248 Wang 2017 (ZnO) · 249 Luo 2016 · 253 Fu 2017 (Mg 두께) · 255 Liu 2017 · 261 · 268 Sharafi 2017 (표면 화학) · 267 Taylor 2018 |
| **T12 Li 기계 · 덴드라이트 · 스택압** (§5.3) | 26 · ✅ 0 | 283 Cheng 2017 · **284 Porz 2017** · 286 Yu 2016 (LLZO 탄성) · **288 Monroe 2005** · 290 Yu 2018 · 291 Masias 2019 · **292 Kasemchainan 2019** · **294 Krauskopf 2019** · 299 Sharafi 2017 · 304 Pesci 2018 |
| **T13 액체 vs 고체 Li 금속** (§5.4) | 17 · ✅ 0 | 305 Xu 2014 *Chem. Rev.* · 307 Fang 2019 *Nature* (불활성 Li 정량) · 310 Cao 2019 · 316 Fang 2019 · 321 Albertus 2018 |
| **T14 분석 기법 · 계산 방법** (§6) | 20 · ✅ 0 | 322 Zhu 2017 (질화물 Li 안정) · 323 Wang 2016 (in situ STEM-EELS LCO–LiPON) · 326 Lee 2019 (cryo-FIB) · 329 Seitzman 2018 · 330 Liang 2018 (AFM 전위) · 333 Wenzel 2015 · **334 Wood 2018 *Nat. Commun.* (operando XPS)** · 338 Zhang 2017 · 340 Wang 2017 (NDP) · **341 Han 2019 *Nat. Energy* (전자전도 = 덴드라이트 원인)** |

- 묶음 합 = 341 (빠진 번호 0). litdb 덮개는 **기계 (T7) 9 편**에 몰려 있고, 이번 의뢰의 중심인 **T4 + T6 (양극 계면 + 코팅) 53 편 중 4 편**뿐이다.

### 9c. 다음 인입 후보 — Top 5 (계면 반응에너지 · 코팅 그림의 원전 우선)

| 순위 | 원전 | 왜 | 우리 어디 |
|---|---|---|---|
| 1 | **ref 51 (= 327)** A. Banerjee, H. Tang, X. Wang, J.-H. Cheng, H. Nguyen, M. Zhang, D. H. S. Tan, T. A. Wynn, E. A. Wu, J.-M. Doux, *et al.* (리뷰가 인쇄한 저자 목록 그대로) — *ACS Appl. Mater. Interfaces* **11**, 43138–43145 (2019) | `Fig. 14` · `Fig. 17` · `Fig. 18a` · `Fig. 33` 의 원전 · NCA–LPSCl AIMD 원문 · [혁주] 요청서가 직접 인용 · `kim2025_lto_pald_conformal_coating_nca` 가 LTO 창 *"1.75–4.25 V"* 를 이 논문 (그쪽 ref [52]) 에서 인용 — 그런데 **이 논문 자신의 표 (`Fig. 17` 재수록) 는 LTO 상한 ≈ 3.71 V** 를 그린다 ⇒ eV/f.u. 의 f.u. · NCA 충전 상태 · AIMD 조건 · 4.25 V 의 출처를 원문으로 확정 | [혁주] stage 1 · MD · B③ · `kim2025` 대조 |
| 2 | **ref 119** Ito, …, Machida, *J. Power Sources* **248**, 943–950 (2014) — *"A Rocking Chair Type All-Solid-State Lithium Ion Battery Adopting Li₂O−ZrO₂ Coated LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂ and a Sulfide Based Electrolyte"* | LZO 계 코팅 + NCA + 황화물의 가장 가까운 실험 선례 (이 리뷰가 Li₂O–ZrO₂ 를 '흔한 삼원 코팅' 으로 꼽는 근거) | [혁주] 1 · 2 단계 해석 |
| 3 | **ref 80** Tang, …, Ong, *Chem. Mater.* **30**, 163–173 (2018) — *"Probing Solid−Solid Interfacial Reactions in All-Solid-State Sodium-Ion Batteries with First-Principles Calculations"* | `Fig. 12` 원전 · §6.1 '세 접근' 분류의 출처 · RDF-시간 판독법 · 반응 부피 변화 지표 | [혁주] MD 판독 정의 |
| 4 | **ref 87** Auvergniot, …, Dedryvère, *Chem. Mater.* **29**, 3883–3890 (2017) — *"Interface Stability of Argyrodite Li₆PS₅Cl toward LiCoO₂, LiNi₁/₃Co₁/₃Mn₁/₃O₂, and LiMn₂O₄ in Bulk All-Solid-State Batteries"* | 아지로다이트 + 양극 CEI 산물의 XPS 원전 ([Xiao20Rev] 도 인용 · litdb 2 곳 2 차 인용) — 혁주 XPS 해석의 기준 봉우리 | B② · [혁주] XPS |
| 5 | **ref 41** Tan, …, Meng, *ACS Energy Lett.* **4**, 2418–2427 (2019) — *"Elucidating Reversible Electrochemical Redox of Li₆PS₅Cl Solid Electrolyte"* | `Fig. 7` · `Fig. 8` 원전 · 4.2 V 산물 · 상태별 임피던스 · 우리 B① 2.256 V 의 실측 짝 | B① · B② |

**차순위**: ref 83 Ohta 2006 *Adv. Mater.* (LTO 두께 → 공간전하 · `Fig. 18b,c`) · ref 95 Ohta 2007 *Electrochem. Commun.* (LiNbO₃ 코팅 원전) · ref 115 Machida 2012 (ZrO₂ 코팅 NMC — LZO 산물 ZrO₂ 와 직결) · ref 75 Koerver 2017 *Chem. Mater.* · ref 127 Zhang 2018 *ACS AMI* (`Fig. 19` · 코팅 조성 Ta 확인) · ref 45 Koerver 2017 *JMCA* · ref 42 Dewald 2019 · ref 66 Zhang 2017 · ref 93 Swift 2019 *PRL* · ref 213 Wenzel 2018 · ref 334 Wood 2018 · ref 341 Han 2019 · ref 3 Wang 2015 *Nat. Mater.*.

### 9d. ⚠ 인용 번호 신뢰도 — 번호가 내용과 안 맞는 곳 (최소 9 곳)

| 자리 | 인쇄된 번호 | 그 번호의 실제 논문 | 맞는 원전 (추정) |
|---|---|---|---|
| `Fig. 33` 캡션 | ref 52 | Zhu 2015 (ESW 열역학) | ref 51 / 327 Banerjee 2019 (cryo-STEM NCA–LPSCl · 본문은 326 · 327 — 326 은 Li 금속 cryo-FIB 논문) |
| `Fig. 28` 캡션 | ref 333 · *"Copyright 2016 ACS"* | Wenzel 2015 *Solid State Ionics* (in situ XPS 방법 · ACS 아님) | ref 37 Wenzel 2016 *Chem. Mater.* (LGPS–Li) |
| `Fig. 4` 캡션 | ref 45 · *"Copyright 2017 ACS"* | Koerver 2017 *J. Mater. Chem. A* (RSC 학술지) | 번호 또는 저작권 줄 중 하나가 틀렸다 (ref 75 Koerver 2017 *Chem. Mater.* 일 수 있다) |
| 지면 6890 *"good agreement with DFT calculations.86"* | 86 | Woo 2012 (Al₂O₃ ALD 실험 · DFT 아님) | 불명 |
| 지면 6897 Woo HAADF · Al₂O₃ 45 층 | 82 | Jung 2018 (LBO–Li₂CO₃) | ref 86 Woo 2012 |
| 지면 6895 *"LTO-coated LCO … 900 to 20 Ω.51,82"* | 82 | Jung 2018 (LBO) | ref 83 Ohta 2006 |
| 지면 6895 *"Li₂O−SiO₂ … Li₃BO₃−Li₂CO₃ coated cathodes … .103"* | 103 | Rong 2016 (이온 이동 경로 알고리즘) | ref 82 Jung 2018 등 |
| 지면 6895 *"phase stability for several coating materials.51,99−101"* | 100 · 101 | Wang 2017 · Choi 2019 (SE 이온전도 기원) | 코팅 상안정과 무관 |
| 지면 6909 *"verified … by Wenzel et al. … .211"* | 211 | Chen 2017 (Li–LGPS 계면) | ref 37 Wenzel 2016 |

⇒ 이 리뷰를 '인용 허브' 로 쓸 때는 **번호가 아니라 제목 · 저자**로 원전을 찾는다. 부록 R 의 litdb 칸은 제목으로 대조했으므로 이 오류의 영향을 받지 않는다.

---

## 10. 비판 — 이 리뷰의 약한 곳 ★

1. **그림 상호참조 오류** — *"As shown in Figure 13a (with LPSCl), LiPON, LiAlO₂, and Li₂SiO₃ are the most stable"* · *"Rc … (Figure 13a)"*: `Fig. 13a` 는 휴지 유무 충방전 곡선이다 (코팅 표는 `Fig. 17`) · *"Figure 17 shows the pseudo binary phase diagram"*: 실제는 `Fig. 18a` · *"four key challenges for all-solid-state Li−S batteries (Figure 17)"*: `Fig. 17` 은 코팅 표 · *"(Figure 20g)"*: `Fig. 20` 은 a–f 뿐 (CE 는 20e) · 본문이 `Fig. 18b` · `Fig. 18c` 를 뒤바꿔 부른다 (본문 *"slope can be eliminated (Figure 18b)"* · *"lowered … impedance (Figure 18c)"* ↔ 캡션 b = 임피던스 · c = 전압) — 원전 ref 51 의 그림 번호가 남은 흔적으로 보인다 (추정).
2. **본문 ↔ 그림 수치 불일치** (본 그림 기준):
   - operando 응력 *"+0.6 MPa"* ↔ `Fig. 20a` 축 *σ₁₁ / 10⁵ Pa* → **0.06 MPa** (10 배).
   - *"NiS"* ↔ `Fig. 14c,d` 범례 **Ni₃S₄**.
   - LiPON 창 0.68–2.63 V (본문) ↔ `Fig. 3d` **0.7–1.1 V**.
   - LPSCl 창: `Fig. 3b` · `Fig. 17` ≈ 1.73–2.36 V ↔ `Fig. 26` ≈ 2.08–2.29 V (figure-read) — 같은 리뷰가 두 구성 (자기 그림 꼴 vs Richards 2016 재수록) 을 설명 없이 같이 싣는다 ([Xiao20Rev] 의 'LLZO 창 셋' 과 같은 꼴).
   - *"Increasing thickness of LTO coating reduces the impedance"* (`Fig. 18` 캡션) ↔ 그림은 **5 nm 최소 비단조** (30 nm ≈ 1 nm) · 첫 충전 기울기 소거 (≥ 20 nm) 와 저항 최소 (≈ 5 nm) 가 다른 두께에서 일어난다 — 둘을 공간전하 하나로 설명하는 서술과 긴장한다.
   - LNO 코팅의 *"lower cathodic charge transfer impedance … stable impedance values over long durations (Figure 13c−e)"* ↔ `Fig. 13e` 에서 코팅 복합체의 **절대 임피던스가 모든 시각에서 무코팅보다 크다** (figure-read ≈ 0 h 에 ≈ 320 vs ≈ 75 Ω) — 그 그림이 보여 주는 것은 *'낮다'* 가 아니라 *'안 자란다'* 다 (`jung2019_…`: LNO 코팅이 t = 0 전자 입계 저항을 키운다 296.7 vs 50.6 Ω).
   - *"1:1 wt. ratio"* ↔ `Fig. 13d` *"1:1, v/v"*.
   - 비정질 LNO σ **10⁻⁶** (지면 6897 앞 문단) ↔ **10⁻⁵ S/cm** (같은 쪽 뒤 문단).
   - LLZO–L0.5CO *"53 meV per atom"* ↔ `Fig. 10` figure-read ≈ 40 (얇은 점선 · 판독 불확실).
   - 산화물 SE 창 (LLZO 2.91 V 본문) ↔ `Fig. 26` LLZO ≈ 3.06 V (figure-read) — 원전 세대가 섞였다.
3. **단위 · 정규화 미정의**: `Fig. 18a` eV/f.u. (§4c) · `Fig. 17` E_rxn · ΔV 단위 미인쇄 · `Fig. 12a` *"eV"* (per atom 표기 없음) · 계면 저항을 *"Ω/cm²"* 로 적는다 (Ω·cm² 여야 한다).
4. **HOMO/LUMO 도식 (`Fig. 2` · §3 첫 문단) 과 grand potential (§3.1) 을 구분 없이 같이 쓴다** — 고체의 띠 가장자리는 열역학 분해 전위가 아니다 (우리 규율: 띠틈 ≠ 안정 전압). 리뷰 자신이 §3.1 에서 grand potential 을 쓰면서 이 차이를 말하지 않는다.
5. **'속도론으로 안정' 주장에 속도 자료가 없다** (CEI 자기 부동태 · LLZO 동역학 안정 · 산화물 코팅의 낮은 σ_e 로 긴 수명) — 서술은 맞을 수 있지만 정량 0 이고, 요약 III 이 스스로 *"> 500 사이클 코팅 안정성 연구 없음"* 을 인정한다.
6. **오기**: *"Li₂ZrO₇"* (지면 6893 — La₂Zr₂O₇ 로 보인다) · *"Li₃CO₃"* (지면 6897 — Li₂CO₃) · *"LiLa(PO₄)₃"* (`Fig. 17` — [Xiao19] 의 LiLa(PO₃)₄) · `Fig. 28` 캡션 *"Ga 3d"* (Ge 3d) · `Fig. 27` 캡션 *"Binary oxides, such as LiX …, Li₃P, Li₃N"* · `Fig. 20a` 라벨 *"LCO (811)"* · 입경 *"5 to 600 mm"* (µm) · 이름 오기 (*"Seigel"* · *"Pallab et al."* · *"Federico et al."* — 이름을 성처럼 · *"Yang Oh et al."* · *"Sun at al."*) · `Fig. 5a` 범례 *"LPLSCl"* · *"aquatic impulse method"* (acoustic 로 보인다) · `Fig. 11` 캡션 *"at 150 °C"* (본문은 60 °C) 이고 캡션은 (b)(c) 를 말하는데 그림은 (a)(b) 뿐 · `Fig. 20d` 캡션 *"intramolecular cracks"* (입자 내부 균열을 말하는 것으로 보인다).
7. **참고문헌 중복 3 쌍 · 번호 오류 9 곳** (§9d) — 허브 리뷰로서 가장 아픈 약점.
8. **코팅 표의 NCA 쪽 반응성을 본문이 빠뜨린다**: Li₂PNO₂ (LiPON) 의 E_rxn^NCA −0.34 가 표에서 가장 큰데 본문은 LiPON 을 *'가장 안정'* 으로만 쓴다 (SE 쪽 기준).
9. *"10 % · 30 % 부피 변화 → 1 % · 10 % 변형"* — 근거 없음 (§3d).
10. **AIMD 를 '가장 현실적' 이라 하면서** 소환한 두 AIMD (Tang · Banerjee) 의 조건을 하나도 적지 않는다 — 관측창 · 셀 크기를 모르면 *"60 ps 안에 결합이 생겼다"* 를 운동학적 주장으로 쓸 수 없다.

---

## 11. 인용 가능 문장 (영문 초안)

- "Banerjee et al. classify ASSB interfaces into voids, chemical reactions, electrochemical reactions, and grain boundaries, and identify the cathode charge-transfer resistance as the bottleneck for high-power sulfide ASSBs (*Chem. Rev.*, 120, 6878 (2020))."
- "Mixing liquid-cell-charged NCA (4.3 V) with Li₆PS₅Cl yields crystalline Ni₃S₄, Li₃PO₄, and LiCl, whereas LiNbO₃-coated NCA shows no product reflections (reproduced in *Chem. Rev.*, 120, 6878 (2020), Fig. 14, from *ACS Appl. Mater. Interfaces*, 11, 43138 (2019))."
- "Thermodynamic stability windows of most oxide coatings end below ~4 V vs. Li/Li⁺; their practical operation is attributed to sluggish kinetics (*Chem. Rev.*, 120, 6878 (2020))."
- ⛔ 쓰지 않을 문장: *"LNO reacts 16× less with LPSCl than NCA"* (eV/f.u. 축 · §4c) · *"Li₂ZrO₃ band gap 3.99 eV vs. our …"* (2a §5b) · 리뷰의 ref 번호만 붙인 원전 인용 (§9d).

---

## 12. 기법 용어 미니사전

- **grand potential** Φ = E − n_Li μ_Li — Li 만 연 열린계 에너지. 전압 V 는 μ_Li = μ⁰_Li − eV 로 들어간다. 'Li 흡수 수 0' 구간이 창.
- **pseudo-binary (mutual) 반응에너지** — 두 상을 x : (1−x) 로 섞어 hull 로 떨어뜨린 에너지. 최솟값 (kink) 이 '최대 구동력'. 정규화 (원자당 vs 화학식당) 를 반드시 같이 적는다.
- **E_hull** — 볼록 껍질 위 거리 (eV/atom). 0 이면 열역학 안정상.
- **R_c (diffusion channel radius)** — 골격 안 Li 통로의 가장 좁은 반경 (Å) · 큰 쪽이 빠르다는 경험 지표.
- **공간전하층 (SCL)** — 화학 퍼텐셜 차로 계면 SE 쪽 Li⁺ 가 빠진 층. 계산 예측 · 직접 관측 없음.
- **MIEC** — 혼합 이온 · 전자 전도 계면상. 계속 자란다.
- **친리튬 (lithiophilic) 코팅** — Li 와 반응 · 합금해 젖음을 만드는 얇은 층 (Si · Mg · ZnO · Au …).
- **Monroe–Newman 기준** — 전해질 전단계수가 Li 의 두 배면 덴드라이트가 억제된다는 선형 안정성 결과 (다결정 · 입계에는 안 맞는다).
- **크리프 (확산 / power-law)** — 낮은 응력에서 입계 확산 (응력에 선형) · 높은 응력에서 전위 운동 (고차) — 스택압이 Li 를 SE 공극으로 밀어 넣는 기전.
- **CCD** — 덴드라이트 단락이 시작되는 임계 전류밀도.
- **2D-EXSY** — 두 상 사이 Li 교환을 보는 교차 봉우리 NMR.
- **NDP** — ⁶Li(n, α)³H 반응 입자의 에너지 손실로 Li 깊이 분포를 재는 법.
- **RDF-시간 히트맵** — AIMD 궤적의 결합쌍 동경분포를 시간 축으로 펼친 그림 · 기준상 RDF 와 겹쳐 산물을 판정.
- **TGC** — 적정 기체 크로마토그래피 · 불활성 금속 Li 정량.

---

## 13. 한 줄 결론

이 리뷰는 **계산 0 · 실험 0 의 지도**다 — 양극–황화물 계면 · 코팅에 관한 수치는 전부 원전 (Zhu 2015 · Zhu 2016 · Xiao 2019 · Banerjee 2019) 에서 왔고, [혁주] 요청서가 가리킨 그림은 원전 ref 51 의 그림이 이 리뷰에 `Fig. 18a` · `Fig. 17` 로 다시 실린 것이며 그 혼합 곡선은 정의 없는 eV/f.u. 축이다. 우리에게 남는 쓸모는 셋 — 화학 / 전기화학 분리 실험 설계 (`Fig. 14`) · RDF-시간 판독법 (`Fig. 12b`) · 341 편 참고문헌 지도 (21 편 이미 litdb · 양극 계면 + 코팅 53 편 중 4 편만 덮였다 · 다음은 ref 51 → 119 → 80 → 87 → 41).

---

## 부록 R. 참고문헌 341 편 전체 — 기계 추출 · litdb 대조

> 추출: 두 번째 PDF 의 *REFERENCES* 절을 PyMuPDF 텍스트로 뽑아 번호 순서로 나눴다 (341 편 · 번호 빠짐 0). 제목 · 학술지 칸은 **원문 표기 그대로** (ACS 판이 화학식 대소문자를 깨뜨린 것 — 예 *"Licoo2"* · *"Li10gep2s12"* — 과 줄바꿈 하이픈 *"Solid- State"* 를 고치지 않았다) · 120 자에서 자름. '첫 인용' = 번호 순서로 추정한 첫 인용 절 (ACS 는 첫 인용 순으로 번호를 매긴다). litdb 칸 = 제목 문자열과 slug (첫 저자 · 연도) 두 경로로 찾은 뒤 눈으로 확인한 자기 digest · *"= ref N"* 은 같은 작품의 중복 수록.

| ref | 1저자 · 연도 | 제목 · 학술지 (기계 추출 · 원문 표기 그대로) | 첫 인용 | litdb |
|---|---|---|---|---|
| 1 | Gao 2018 | Promises, Challenges, and Recent Progress of Inorganic Solid-State Electrolytes for All-Solid-State Lithium Batteries.… | §1 | — |
| 2 | Manthiram 2017 | Lithium Battery Chemistries Enabled by Solid-State Electrolytes. Nature Reviews Materials | §1 | — |
| 3 | Wang 2015 | Design Principles for Solid-State Lithium Superionic Conductors. Nat. Mater. | §1 | — |
| 4 | Mizuno 2005 | New, Highly Ion-Conductive Crystals Precipitated from Li2S−P2S5 Glasses. Adv. Mater. | §1 | — |
| 5 | Kamaya 2011 | A Lithium Superionic Conductor. Nat. Mater. | §1 | ✅ `kamaya2011_lgps_lithium_superionic_conductor` |
| 6 | Kato 2016 | High-Power All-Solid-State Batteries Using Sulfide Superionic Conductors. Nature Energy | §1 | ✅ `kato2016_high_power_assb_lsipscl_superionic` |
| 7 | Xu 2018 | Interfaces in Solid-State Lithium Batteries. Joule | §1 | — |
| 8 | Han 2016 | Electrochemical Stability of Li10gep2s12 and Li7la3zr2o12 Solid Electrolytes. Adv. Energy Mater. | §1 | — |
| 9 | Takada 2008 | Interfacial Modification for High-Power Solid- State Lithium Batteries. Solid State Ionics | §1 | — |
| 10 | Sakuda 2010 | Interfacial Observation between Licoo2 Electrode and Li2S−P2S5 Solid Electrolytes of All- Solid-State Lithium Secondar… | §1 | — |
| 11 | Zhu 2016 | First Principles Study on Electrochemical and Chemical Stability of Solid Electrolyte−Electrode Interfaces in All- Sol… | §1 | ✅ `zhu2016_first_principles_interface_stability_assb` |
| 12 | Haruyama 2017 | Cation Mixing Properties toward Co Diffusion at the LiCoO2 Cathode/Sulfide Electrolyte Interface in a Solid-State Batt… | §1 | ✅ `haruyama2017_cation_mixing_co_diffusion_lco_lps` |
| 13 | Wang 2020 | Garnet-Type Solid-State Electrolytes: Materials, Interfaces, and Batteries. Chem. Rev. | §1 | — |
| 14 | Wolfenstine 2018 | Mechanical Behavior of Li-Ion-Conducting Crystalline Oxide-Based Solid Electrolytes: A Brief Review. Ionics | §1 | — |
| 15 | Bi 2020 | Interface Engineering on Cathode Side for Solid Garnet Batteries. Chem. Eng. J. | §1 | — |
| 16 | Zhao 2019 | Solid Garnet Batteries. Joule | §1 | — |
| 17 | Zhao 2020 | Designing Solid- State Electrolytes for Safe, Energy-Dense Batteries. Nature Reviews Materials | §1 | — |
| 18 | Li 2020 | Progress and Perspective of Ceramic/Polymer Composite Solid Electrolytes for Lithium Batteries. Advanced Science | §1 | — |
| 19 | Lopez 2019 | Designing Polymers for Advanced Battery Chemistries. Nature Reviews Materials | §1 | — |
| 20 | Zhang 2019 | Editors’ ChoiceReview Innovative Polymeric Materials for Better Rechargeable Batteries: Strategies from Cic Energigu… | §1 | — |
| 21 | Goodenough 2010 | Challenges for Rechargeable Li Batteries. Chem. Mater. | §3 서두 | — |
| 22 | Moeremans 2019 | In Situ Mechanical Analysis of the Nanoscopic Solid Electrolyte Interphase on Anodes of Li-Ion Batteries. Advanced Sci… | §3 서두 | — |
| 23 | Bedrov 2017 | Li+ Transport and Mechanical Properties of Model Solid Electrolyte Interphases (SEI): Insight from Atomistic Molecular… | §3 서두 | — |
| 24 | Peled 2017 | ReviewSei: Past, Present and Future. J. Electrochem. Soc. | §3 서두 | — |
| 25 | Horstmann 2019 | Review on Multi-Scale Models of Solid-Electrolyte Interphase Formation. Current Opinion in Electro- chemistry | §3 서두 | — |
| 26 | Verma 2010 | A Review of the Features and Analyses of the Solid Electrolyte Interphase in Li-Ion Batteries. Electrochim. Acta | §3 서두 | — |
| 27 | Wang 2018 | Review on Modeling of the Anode Solid Electrolyte Interphase (SEI) for Lithium-Ion Batteries. npj Computational Materi… | §3 서두 | — |
| 28 | Cannarella 2014 | Stress Evolution and Capacity Fade in Constrained Lithium-Ion Pouch Cells. J. Power Sources | §3 서두 | — |
| 29 | Baggetto 2009 | On the Electrochemistry of an Anode Stack for All-Solid-State 3d- Integrated Batteries. J. Power Sources | §3 서두 | — |
| 30 | Richards 2016 | Interface Stability in Solid-State Batteries. Chem. Mater. | §3.1 | ✅ `richards2016_interface_stability_pseudobinary` |
| 31 | Ong 2008 | Li−Fe−P−O2 Phase Diagram from First Principles Calculations. Chem. Mater. | §3.1 | — |
| 32 | Han 2015 | A Battery Made from a Single Material. Adv. Mater. | §3.1 | — |
| 33 | Chen 2001 | Ionic Conductivity, Lithium Insertion and Extraction of Lanthanum Lithium Titanate. Solid State Ionics | §3.1 | — |
| 34 | Xu 2006 | High Lithium Ion Conductivity Glass-Ceramics in Li2O−AL2O3−TIO2−P2O5 from Nanoscaled Glassy Powders by Mechanical Mill… | §3.1 | — |
| 35 | Kotobuki 2010 | Compatibility of Li7La3Zr2O12 Solid Electrolyte to All-Solid-State Battery Using Li Metal Anode. J. Electrochem. Soc. | §3.1 | — |
| 36 | Wolfenstine 2013 | Chemical Stability of Cubic Li7La 3Zr 2O 12 with Molten Lithium at Elevated Temperature. J. Mater. Sci. | §3.1 | — |
| 37 | Wenzel 2016 | Direct Observation of the Interfacial Instability of the Fast Ionic Conductor Li10GeP2S12 at the Lithium Metal Anode. … | §3.1 | — |
| 38 | Hakari 2015 | All-Solid- State Lithium Batteries with Li3ps4 Glass as Active Material. J. Power Sources | §3.1 | — |
| 39 | Machida 2005 | Preparation of Amorphous 75L2S·xP2S3·(25−x)P2S5 (Mol%) Solid Electrolytes by a High-Energy Ball-Milling Process and Th… | §3.1 | — |
| 40 | Swamy 2019 | Electrochemical Redox Behavior of Li Ion Conducting Sulfide Solid Electrolytes. Chem. Mater. | §3.1 | — |
| 41 | Tan 2019 | Elucidating Reversible Electrochemical Redox of Li6PS5Cl Solid Electrolyte. ACS Energy Letters | §3.1 | — |
| 42 | Dewald 2019 | Experimental Assessment of the Practical Oxidative Stability of Lithium Thiophosphate Solid Electrolytes. Chem. Mater. | §3.1 | — |
| 43 | Wang 2019 | Lithium Chlorides and Bromides as Promising Solid-State Chemistries for Fast Ion Conductors with Good Electrochemical … | §3.1 | — |
| 44 | Kokal 2011 | Sol−Gel Synthesis and Lithium Ion Conductivity of Li7La3Zr2O12 with Garnet-Related Type Structure. Solid State Ionics | §3.1 | — |
| 45 | Koerver 2017 | Redox-Active Cathode Interphases in Solid-State Batteries. J. Mater. Chem. A | §3.2 | — |
| 46 | Wu 2016 | J., Iv; Deng, D. Z.; Yang, J.; Xiao, J. Interfacial Behaviours between Lithium Ion Conductors and Electrode Materials … | §3.2 | — |
| 47 | Trevey 2011 | High Power Nano- composite TiS2 Cathodes for All-Solid-State Lithium Batteries. J. Electrochem. Soc. | §3.2 | — |
| 48 | Asano 2018 | Solid Halide Electrolytes with High Lithium-Ion Conductivity for Application in 4 V Class Bulk-Type All-Solid-State Ba… | §3.2 | — |
| 49 | Banerjee 2019 | Motif-Based Design of an Oxysulfide Class of Lithium Superionic Conductors: Toward Improved Stability and Record-High … | §3.2 | — |
| 50 | Suzuki 2016 | Synthesis, Structure, and Electrochemical Properties of Crystalline Li−P−S−O Solid Electro- lytes: Novel Lithium-Condu… | §3.2 | — |
| 51 | Banerjee 2019 | Revealing Nanoscale Solid−Solid Interfacial Phenomena for Long-Life and High-Energy All-Solid-State Batteries. ACS App… | §3.2 | — |
| 52 | Zhu 2015 | Origin of Outstanding Stability in the Lithium Solid Electrolyte Materials: Insights from Thermodynamic Analyses Based… | §3.2 | ✅ `zhu2015_esw_grand_potential_origin` |
| 53 | Perdew 1985 | Density Functional Theory and the Band Gap Problem. Int. J. Quantum Chem. | §3.2 | — |
| 54 | Julien 2019 | Sputtered LiCoO (2) Cathode Materials for All-Solid-State Thin-Film Lithium Micro- batteries. Materials | §3.2 | — |
| 55 | Li 2015 | Solid Electrolyte: The Key for High-Voltage Lithium Batteries. Adv. Energy Mater. | §3.2 | — |
| 56 | Yu 1997 | A Stable Thin-Film Lithium Electrolyte: Lithium Phosphorus Oxynitride. J. Electrochem. Soc. | §3.2 | — |
| 57 | Chen 2017 | Voltammetric Enhancement of Li-Ion Conduction in Al-Doped Li7−xLa3Zr2O12 Solid Electrolyte. J. Phys. Chem. C | §3.3 | — |
| 58 | Rangasamy 2012 | The Role of Al and Li Concentration on the Formation of Cubic Garnet Solid Electrolyte of Nominal Composition Li7La3Zr… | §3.3 | — |
| 59 | Shin 2014 | Comparative Study of TiS2/Li-in All-Solid-State Lithium Batteries Using Glass-Ceramic Li3PS4 and Li10GeP2S12 Solid Ele… | §3.3 | — |
| 60 | Minami 2007 | Lithium Ion Conductivity of the Li2S−P2S5 Glass-Based Electrolytes Prepared by the Melt Quenching Method. Solid State … | §3.3 | — |
| 61 | Li 2014 | Artificial Solid Electrolyte Interphase to Address the Electrochemical Degradation of Silicon Electrodes. ACS Appl. Ma… | §3.3 | — |
| 62 | Le Van-Jodin 2013 | Dielectric Properties, Conductivity and Li+ Ion Motion in Lipon Thin Films. Solid State Ionics | §3.3 | — |
| 63 | Su 2015 | Lipon Thin Films with High Nitrogen Content for Application in Lithium Batteries and Electrochromic Devices Prepared b… | §3.3 | — |
| 64 | Strauss 2018 | Impact of Cathode Material Particle Size on the Capacity of Bulk-Type All-Solid-State Batteries. ACS Energy Letters | §3.3 | ✅ `strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation` |
| 65 | Oh 2016 | Bulk- Type All Solid-State Batteries with 5 V Class LiNi0.5Mn1.5O4 Cathode and Li10GeP2S12 Solid Electrolyte. Chem. Ma… | §3.3 | — |
| 66 | Zhang 2017 | The Detrimental Effects of Carbon Additives in Li10GeP2S12-Based Solid-State Batteries. ACS Appl. Mater. Interfaces | §3.3 | — |
| 67 | Culver 2018 | Designing Ionic Conductors: The Interplay between Structural Phenomena and Interfaces in Thiophosphate-Based Solid-Sta… | §3.3 | — |
| 68 | Ates 2019 | Development of an All-Solid-State Lithium Battery by Slurry-Coating Procedures Using a Sulfidic Electrolyte. Energy St… | §3.3 | — |
| 69 | Hakari 2017 | Structural and Electronic-State Changes of a Sulfide Solid Electrolyte During the Li Deinsertion−Insertion Processes. … | §3.4 | — |
| 70 | Hakari 2017 | Favorable Carbon Conductive Additives in Li3PS4 Composite Positive Electrode Prepared by Ball-Milling for All-Solid-St… | §3.4 | — |
| 71 | Hayashi 2010 | Characterization of Li2S−P2S5−Cu Composite Electrode for All- Solid-State Lithium Secondary Batteries. J. Mater. Sci. | §3.4 | — |
| 72 | Suzuki 2018 | High Cycle Capability of All-Solid-State Lithium−Sulfur Batteries Using Composite Electrodes by Liquid-Phase and Mecha… | §3.4 | — |
| 73 | Wang 2018 | High-Conductivity Argyrodite Li6PS5Cl Solid Electro- lytes Prepared Via Optimized Sintering Processes for All-Solid-St… | §3.4 | — |
| 74 | Takada 2013 | Progress and Prospective of Solid-State Lithium Batteries. Acta Mater. | §4 서두 | — |
| 75 | Koerver 2017 | Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxid… | §4 서두 | — |
| 76 | Ma 2018 | Progress and Prospect on Failure Mechanisms of Solid-State Lithium Batteries. J. Power Sources | §4 서두 | — |
| 77 | Pervez 2019 | Interface in Solid-State Lithium Battery: Challenges, Progress, and Outlook. ACS Appl. Mater. Interfaces | §4 서두 | — |
| 78 | Jain 2011 | A High-Throughput Infra- structure for Density Functional Theory Calculations. Comput. Mater. Sci. | §4.1.1 | — |
| 79 | Yoshinari 2019 | Interfacial Stability of Phosphate-Nasicon Solid Electro- lytes in Ni-Rich NCM Cathode-Based Solid-State Batteries. AC… | §4.1.1 | — |
| 80 | Tang 2018 | Probing Solid−Solid Interfacial Reactions in All-Solid-State Sodium-Ion Batteries with First-Principles Calculations. … | §4.1.1 | — |
| 81 | Lacivita 2019 | Ab Initio Investigation of the Stability of Electrolyte/Electrode Interfaces in All-Solid-State Na Batteries. J. Mater… | §4.1.1 | — |
| 82 | Jung 2018 | Li3BO3−Li2CO3: Rationally Designed Buffering Phase for Sulfide All-Solid-State Li-Ion Batteries. Chem. Mater. | §4.1.2 | — |
| 83 | Ohta 2006 | Enhancement of the High-Rate Capability of Solid-State Lithium Batteries by Nanoscale Interfacial Modification. Adv. M… | §4.1.2 | — |
| 84 | Cao 2020 | Stable Thiophosphate-Based All-Solid-State Lithium Batteries through Conformally Interfacial Nanocoating. Nano Lett. | §4.1.2 | — |
| 85 | Jung 2019 | Understanding the Effects of Chemical Reactions at the Cathode−Electrolyte Interface in Sulfide Based All- Solid-State… | §4.1.2 | ✅ `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` |
| 86 | Woo 2012 | Nanoscale Interface Modification of LiCoO2 by Al2O3 Atomic Layer Deposition for Solid-State Li Batteries. J. Electroch… | §4.1.2 | — |
| 87 | Auvergniot 2017 | Interface Stability of Argyrodite Li6PS5Cl toward LiCoO2, LiNi1/3Co1/3Mn1/3O2, and LiMn2O4 in Bulk All-Solid- State Ba… | §4.1.2 | — |
| 88 | Ohta 2012 | Electrochemical Performance of an All-Solid-State Lithium Ion Battery with Garnet- Type Oxide Electrolyte. J. Power So… | §4.1.2 | — |
| 89 | Kim 2011 | Characterization of the Interface between Licoo2 and Li7La3Zr2O12 in an All-Solid-State Rechargeable Lithium Battery. … | §4.1.2 | — |
| 90 | Park 2016 | Electrochemical Nature of the Cathode Interface for a Solid-State Lithium-Ion Battery: Interface between LiCoO2 and Ga… | §4.1.2 | — |
| 91 | Vardar 2018 | Structure, Chemistry, and Charge Transfer Resistance of the Interface between Li7La3Zr2O12 Electrolyte and LiCoO2 Cath… | §4.1.2 | — |
| 92 | Haruyama 2014 | Space−Charge Layer Effect at Interface between Oxide Cathode and Sulfide Electrolyte in All-Solid-State Lithium-Ion Ba… | §4.1.3 | ✅ `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` |
| 93 | Swift 2019 | First-Principles Prediction of Potentials and Space-Charge Layers in All-Solid-State Batteries. Phys. Rev. Lett. | §4.1.3 | — |
| 94 | Tateyama 2019 | Theoretical Picture of Positive Electrode−Solid Electrolyte Interface in All-Solid- State Battery from Electrochemistr… | §4.1.3 | — |
| 95 | Ohta 2007 | LiNbO3-Coated LiCoO2 as Cathode Material for All Solid-State Lithium Secondary Batteries. Electrochem. Commun. | §4.1.3 | — |
| 96 | Takada 2015 | Recent Progress in Interfacial Nanoarchitectonics in Solid-State Batteries. J. Inorg. Organomet. Polym. Mater. | §4.1.3 | — |
| 97 | Masuda 2017 | Internal Potential Mapping of Charged Solid-State-Lithium Ion Batteries Using in Situ Kelvin Probe Force Microscopy. N… | §4.1.3 | — |
| 98 | Yamamoto 2010 | Dynamic Visualization of the Electric Potential in an All-Solid-State Recharge- able Lithium Battery. Angew. Chem., In… | §4.1.3 | — |
| 99 | Xiao 2019 | Computational Screening of Cathode Coatings for Solid-State Batteries. Joule | §4.1.4 | ✅ `xiao2019_cathode_coating_screening` |
| 100 | Wang 2017 | Theoretical Design of Solid Electrolytes with Superb Ionic Conductivity: Alloying Effect on Li+ Transportation in Cubi… | §4.1.4 | — |
| 101 | Choi 2019 | Electronic and Mechanistic Origins of the Superionic Conductivity of Sulfide-Based Solid Electrolytes. J. Power Sources | §4.1.4 | — |
| 102 | Xu 2019 | First Principle Material Genome Approach for All Solid-State Batteries. Energy & Environ- mental Materials | §4.1.4 | — |
| 103 | Rong 2016 | An Efficient Algorithm for Finding the Minimum Energy Path for Cation Migration in Ionic Materials. J. Chem. Phys. | §4.1.4 | — |
| 104 | Xie 2017 | Atomic Layer Deposition of Stable LiAlF4 Lithium Ion Conductive Interfacial Layer for Stable Cathode Cycling. ACS Nano | §4.1.4 | — |
| 105 | de Bernabe 1996 | Effect of Stoichiometry on the Dynamic Mechanical Properties of Linbo3. J. Appl. Phys. | §4.1.4 | — |
| 106 | Sosunov 2017 | Features of Structure and Mechanical Properties Linbo3. Ferroelectrics | §4.1.4 | — |
| 107 | Du 2015 | All Solid State Lithium Batteries Based on Lamellar Garnet-Type Ceramic Electro- lytes. J. Power Sources | §4.1.4 | — |
| 108 | Kato 2014 | In-Situ Li7La3Zr2O12/LiCoO2 Interface Modification for Advanced All-Solid-State Battery. J. Power Sources | §4.1.4 | — |
| 109 | Ohta 2014 | Co- Sinterable Lithium Garnet-Type Oxide Electrolyte with Cathode for All-Solid-State Lithium Ion Battery. J. Power So… | §4.1.4 | — |
| 110 | Okumura 2011 | Depth-Resolved X-Ray Absorption Spectroscopic Study on Nanoscale Observation of the Electrode−Solid Electrolyte Interf… | §4.1.4 | — |
| 111 | Hu 2009 | Cycle Life Improvement of ZrO2-Coated Spherical LiNi1/3Co1/3Mn1/3O2 Cathode Material for Lithium Ion Batteries. J. Pow… | §4.1.4 | — |
| 112 | Tatsumisago 2006 | All-Solid-State Lithium Secondary Batteries Using Sulfide-Based Glass−Ceramic Electrolytes. J. Power Sources | §4.1.4 | — |
| 113 | Sakuda 2009 | All-Solid-State Lithium Secondary Batteries with Oxide-Coated LiCoO2 Electrode and Li2S−P2S5 Electrolyte. J. Power Sou… | §4.1.4 | — |
| 114 | Hayashi 2014 | Improved Chemical Stability and Cyclability in Li2S−P2S5−P2O5−ZnO Composite Electrolytes for All-Solid-State Rechargea… | §4.1.4 | — |
| 115 | Machida 2012 | Electrochemical Properties of All-Solid-State Batteries with ZrO2- Coated LiNi1/3Mn1/3Co1/3O2 as Cathode Materials. So… | §4.1.4 | — |
| 116 | Seino 2011 | High Rate Capabilities of All- Solid-State Lithium Secondary Batteries Using Li4Ti5O12-Coated LiNi0.8Co0.15Al0.05O2 an… | §4.1.4 | — |
| 117 | Sakuda 2010 | Electrochemical Performance of All-Solid-State Lithium Secondary Batteries Improved by the Coating of Li2O−TiO2 Films … | §4.1.4 | — |
| 118 | Noh 2013 | Surface Modification of LiCoO2 with Li3xLa2/3−xTiO3 for All-Solid-State Lithium Ion Batteries Using Li2S−P2S5 Glass−Ce… | §4.1.4 | — |
| 119 | Ito 2014 | A Rocking Chair Type All- Solid-State Lithium Ion Battery Adopting Li2O−ZrO2 Coated LiNi0.8Co0.15Al0.05O2 and a Sulfid… | §4.1.4 | — |
| 120 | Sakuda 2008 | Improvement of High-Rate Performance of All- Solid-State Lithium Secondary Batteries Using LiCoO2 Coated with Li2O−SiO… | §4.1.4 | — |
| 121 | Okada 2014 | Preparation and Electrochemical Properties of LiAlO2-Coated Li(Ni1/3Mn1/3Co1/3)O2 for All-Solid- State Batteries. Soli… | §4.1.4 | — |
| 122 | Visbal 2016 | The Effect of Diamond-Like Carbon Coating on LiNi0.8Co0.15A- l0.05O2 Particles for All Solid-State Lithium-Ion Batteri… | §4.1.4 | — |
| 123 | Ito 2015 | Application of LiCoO2 Particles Coated with Lithium Ortho-Oxosalt Thin Films to Sulfide-Type All-Solid-State Lithium B… | §4.1.4 | — |
| 124 | Yubuchi 2016 | 5V Class LiNi0.5Mn1.5O4 Positive Electrode Coated with Li3PO4 Thin Film for All-Solid-State Batteries Using Sulfide So… | §4.1.4 | — |
| 125 | Li 2019 | Water-Mediated Synthesis of a Superionic Halide Solid Electrolyte. Angew. Chem., Int. Ed. | §4.1.4 | — |
| 126 | Li 2019 | Air-Stable Li3InCl6 Electrolyte with High Voltage Compatibility for All-Solid-State Batteries. Energy Environ. Sci. | §4.1.4 | — |
| 127 | Zhang 2018 | Degradation Mechanisms at the Li10GeP2S12/LiCoO2 Cathode Interface in an All- Solid-State Lithium-Ion Battery. ACS App… | §4.1.5 | — |
| 128 | Wang 2019 | Manipulating Interfacial Nanostructure to Achieve High-Performance All-Solid-State Lithium- Ion Batteries. Small Methods | §4.1.5 | — |
| 129 | Reimers 1992 | Electrochemical and in Situ X-Ray Diffraction Studies of Lithium Intercalation in LixCoO2. J. Electrochem. Soc. | §4.2 | — |
| 130 | Cho 2001 | LiCoO2 Cathode Material That Does Not Show a Phase Transition from Hexagonal to Monoclinic Phase. J. Electrochem. Soc. | §4.2 | — |
| 131 | Tsai 2005 | In-Situ X-Ray Absorption Spectroscopic Study on Variation of Electronic Transitions and Local Structure of LiNi1/3Co1/… | §4.2 | — |
| 132 | Yoon 2006 | A Comparative Study on Structural Changes of LiCo1/3Ni1/3Mn1/3O2 and LiNi0.8Co0.15Al0.05O2 During First Charge Using i… | §4.2 | — |
| 133 | Gu 2012 | In Situ Tem Study of Lithiation Behavior of Silicon Nanoparticles Attached to and Embedded in a Carbon Matrix. ACS Nano | §4.2 | — |
| 134 | Wang 2012 | In Situ Tem Investigation of Congruent Phase Transition and Structural Evolution of Nano- structured Silicon/Carbon An… | §4.2 | — |
| 135 | Sokolov 2003 | Structure and Physicochemical Properties of Glasses in the Li2S−LIPO3 System. Glass Phys. Chem. | §4.2 | — |
| 136 | Sakuda 2013 | Sulfide Solid Electrolyte with Favorable Mechanical Property for All-Solid-State Lithium Battery. Sci. Rep. | §4.2 | ✅ `sakuda2013_sulfide_mechanical_property` |
| 137 | Nose 2015 | Evaluation of Mechanical Properties of Na2S−P2S5 Sulfide Glass Electrolytes. J. Mater. Chem. A | §4.2 | — |
| 138 | Deng 2016 | Elastic Properties of Alkali Superionic Conductor Electrolytes from First Principles Calculations. J. Electrochem. Soc. | §4.2 | ✅ `deng2016_elastic_superionic_electrolytes_dft` |
| 139 | McGrogan 2017 | Compliant yet Brittle Mechanical Behavior of Li2S−P2S5 Lithium-Ion-Conducting Solid Electrolyte. Adv. Energy Mater. | §4.2 | ✅ `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` |
| 140 | Kato 2018 | Mechanical Properties of Li2S−P2S5 Glasses with Lithium Halides and Application in All-Solid-State Batteries. ACS Appl… | §4.2 | — |
| 141 | Makishima 1973 | Direct Calculation of Young’s Moidulus of Glass. J. Non-Cryst. Solids | §4.2 | — |
| 142 | Soga 1976 | Elastic Properties and Structure of Alkaline-Earth Silicate Glasses. J. Non-Cryst. Solids | §4.2 | — |
| 143 | Tian 2017 | Simulation of the Effect of Contact Area Loss in All-Solid-State Li-Ion Batteries. J. Electrochem. Soc. | §4.2 | ✅ `tian2017_contact_area_loss_assb_simulation` |
| 144 | Koerver 2018 | Chemo-Mechanical Expansion of Lithium Electrode Materials −on the Route to Mechanically Optimized All-Solid-State Batt… | §4.2 | ✅ `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` |
| 145 | Zhang 2017 | (Electro)Chemical Expansion During Cycling: Monitoring the Pressure Changes in Operating Solid-State Lithium Batteries… | §4.2 | — |
| 146 | Doux 2020 | Stack Pressure Considerations for Room-Temperature All-Solid-State Lithium Metal Batteries. Adv. Energy Mater. | §4.2 | ✅ `doux2020_stack_pressure_assb` |
| 147 | Strauss 2020 | Rational Design of Quasi-Zero- Strain NCM Cathode Materials for Minimizing Volume Change Effects in All-Solid-State Ba… | §4.2 | — |
| 148 | Wu 2019 | Operando Visualization of Morphological Dynamics in All-Solid-State Batteries. Adv. Energy Mater. | §4.2 | — |
| 149 | McDowell 2013 | In Situ Tem of Two-Phase Lithiation of Amorphous Silicon Nanospheres. Nano Lett. | §4.2 | — |
| 150 | Bucci 2018 | Mechanical Instability of Electrode-Electrolyte Interfaces in Solid-State Batteries. Physical Review Materials | §4.2 | ✅ `bucci2018_mechanical_instability_interface_delamination` |
| 151 | Bucci 2017 | Modeling of Internal Mechanical Failure of All-Solid-State Batteries During Electrochemical Cycling, and Implications … | §4.2 | ✅ `bucci2017_chemomech_failure_assb_cycling_czm` |
| 152 | Hao 2018 | Mesoscale Analysis of the Electrolyte- Electrode Interface in All-Solid-State Li-Ion Batteries. J. Electrochem. Soc. | §4.2 | — |
| 153 | Bielefeld 2019 | Microstructural Modeling of Composite Cathodes for All-Solid-State Batteries. J. Phys. Chem. C | §4.2 | ✅ `bielefeld2019_microstructural_modeling_composite_cathode` |
| 154 | Lewis 2019 | Chemo-Mechanical Challenges in Solid-State Batteries. Trends in Chemistry | §4.2 | — |
| 155 | Wild 2015 | Lithium Sulfur Batteries, a Mechanistic Review. Energy Environ. Sci. | §4.3 | — |
| 156 | Zhang 2013 | Liquid Electrolyte Lithium/Sulfur Battery: Fundamental Chemistry, Problems, and Solutions. J. Power Sources | §4.3 | — |
| 157 | Umeshbabu 2019 | Recent Progress in All- Solid-State Lithium−Sulfur Batteries Using High Li-Ion Conductive Solid Electrolytes. Electroc… | §4.3 | — |
| 158 | Lin 2013 | Lithium Superionic Sulfide Cathode for All-Solid Lithium-Sulfur Batteries. ACS Nano | §4.3 | — |
| 159 | Hassoun 2010 | Moving to a Solid-State Configuration: A Valid Approach to Making Lithium-Sulfur Batteries Viable for Practical Applic… | §4.3 | — |
| 160 | Hayashi 2003 | All-Solid-State Li/S Batteries with Highly Conductive Glass−Ceramic Electrolytes. Electrochem. Commun. | §4.3 | — |
| 161 | Nagao 2011 | Sulfur−Carbon Composite Electrode for All-Solid-State Li/S Battery with Li2S−P2S5 Solid Electrolyte. Electrochim. Acta | §4.3 | — |
| 162 | Yue 2018 | Progress of the Interface Design in All-Solid-State Li−S Batteries. Adv. Funct. Mater. | §4.3 | — |
| 163 | Ji 2009 | A Highly Ordered Nanostructured Carbon−Sulphur Cathode for Lithium−Sulphur Batteries. Nat. Mater. | §4.3 | — |
| 164 | Luo 2018 | Solid-State Electrolyte Anchored with a Carboxylated Azo Compound for All-Solid-State Lithium Batteries. Angew. Chem.,… | §4.3 | — |
| 165 | Aso 2013 | All-Solid- State Lithium Secondary Batteries Using Nis-Carbon Fiber Composite Electrodes Coated with LI2S−P2S5 Solid E… | §4.3 | — |
| 166 | Kinoshita 2014 | All-Solid-State Lithium Battery with Sulfur/Carbon Composites as Positive Electrode Materials. Solid State Ionics | §4.3 | — |
| 167 | Hakari 2017 | Li2s-Based Solid Solutions as Positive Electrodes with Full Utilization and Superlong Cycle Life in All-Solid-State Li… | §4.3 | — |
| 168 | Suzuki 2017 | Yano, T.-a.; Hirayama, M.; Hara, M.; Kanno, R. Composite Sulfur Electrode Prepared by High- Temperature Mechanical Mil… | §4.3 | — |
| 169 | Nagao 2013 | Electrochemical Performance of All-Solid-State Li/S Batteries with Sulfur-Based Composite Electrodes Prepared by Mecha… | §4.3 | — |
| 170 | Kobayashi 2008 | All Solid-State Battery with Sulfur Electrode and Thio-Lisicon Electrolyte. J. Power Sources | §4.3 | — |
| 171 | Yu 2017 | v.; Wang, H.; Basak, S.; Li, Z.; Wagemaker, M. Accessing the Bottleneck in All-Solid State Batteries, Lithium-Ion Tran… | §4.3 | — |
| 172 | Yu 2016 | Unravelling Li-Ion Transport from Picoseconds to Seconds: Bulk Versus Interfaces in an Argyrodite Li6PS5Cl−Li2S All-So… | §4.3 | — |
| 173 | Hakari 2015 | Highly Utilized Lithium Sulfide Active Material by Enhancing Conductivity in All- Solid-State Batteries. Chem. Lett. | §4.3 | — |
| 174 | Hakari 2017 | Li2S-Based Solid Solutions as Positive Electrodes with Full Utilization and Superlong Cycle Life in All-Solid-State Li… | §4.3 | = ref 167 (중복 수록) |
| 175 | Lin 2013 | Lithium Polysulfidophosphates: A Family of Lithium-Conducting Sulfur-Rich Compounds for Lithium−Sulfur Batteries. Ange… | §4.3 | — |
| 176 | Han 2016 | High-Performance All-Solid-State Lithium−Sulfur Battery Enabled by a Mixed-Conductive Li2S Nanocomposite. Nano Lett. | §4.3 | — |
| 177 | Lin 2013 | Lithium Polysulfidophosphates: A Family of Lithium-Conducting Sulfur-Rich Compounds for Lithium−Sulfur Batteries. Ange… | §4.3 | = ref 175 (중복 수록) |
| 178 | Ulissi 2018 | High Capacity All-Solid-State Lithium Batteries Enabled by Pyrite- Sulfur Composites. Adv. Energy Mater. | §4.3 | — |
| 179 | Liu 2019 | Practical Evaluation of Energy Densities for Sulfide Solid-State Batteries. eTransportation | §4.4 | — |
| 180 | Sakuda 2010 | Preparation of Highly Lithium-Ion Conductive 80Li2S·20P2S5 Thin-Film Electro- lytes Using Pulsed Laser Deposition. J. … | §4.4 | — |
| 181 | Sakuda 2011 | All-Solid-State Lithium Secondary Batteries Using LiCoO2 Particles with Pulsed Laser Deposition Coatings of Li2S−P2S5 … | §4.4 | ✅ `sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode` |
| 182 | Ito 2017 | Electrochemical and Structural Evaluation for Bulk-Type All-Solid- State Batteries Using Li4GeS4-Li3PS4 Electrolyte Co… | §4.4 | — |
| 183 | Park 2016 | Kim, J.- Y.; Xin, H.; Lin, F.; Oh, S. M.; Jung, Y. S. Solution-Processable Glass Lii- Li4sns4 Superionic Conductors fo… | §4.4 | — |
| 184 | Choi 2017 | Coatable Li4sns4 Solid Electrolytes Prepared from Aqueous Solutions for All-Solid-State Lithium-Ion Batteries. Chem- S… | §4.4 | — |
| 185 | Heo 2018 | New Na-Ion Solid Electrolytes Na4−xSn1−xSbxS4 (0.02 ≤X ≤0.33) for All-Solid-State Na-Ion Batteries. Adv. Energy Mater. | §4.4 | — |
| 186 | Park 2018 | Solution-Derived Glass-Ceramic Nai·Na3SbS4 Superionic Conductors for All-Solid-State Na-Ion Batteries. J. Mater. Chem. A | §4.4 | — |
| 187 | Uematsu 2018 | Preparation of Na3PS4 Electrolyte by Liquid-Phase Process Using Ether. Solid State Ionics | §4.4 | — |
| 188 | Banerjee 2016 | Na3SbS4: A Solution Processable Sodium Superionic Conductor for All-Solid-State Sodium-Ion Batteries. Angew. Chem., In… | §4.4 | — |
| 189 | Park 2018 | Design Strategies, Practical Considerations, and New Solution Processes of Sulfide Solid Electrolytes for All-Solid-St… | §4.4 | — |
| 190 | Hayashi 2013 | Improvement of Chemical Stability of Li3PS4 Glass Electrolytes by Adding MxOy (M = Fe, Zn, and Bi) Nanoparticles. J. M… | §4.4 | — |
| 191 | Muramatsu 2011 | Structural Change of Li2S−P2S5 Sulfide Solid Electrolytes in the Atmosphere. Solid State Ionics | §4.4 | — |
| 192 | Rosero-Navarro 2018 | Composite Cathode Prepared by Argyrodite Precursor Solution Assisted by Dispersant Agents for Bulk-Type All-Solid-Stat… | §4.4 | — |
| 193 | Yubuchi 2015 | Preparation of High Lithium-Ion Conducting Li6ps5cl Solid Electrolyte from Ethanol Solution for All-Solid-State Lithiu… | §4.4 | — |
| 194 | Yubuchi 2018 | Lithium-Ion-Conducting Argyrodite-Type Li6PS5x (X = Cl, Br, I) Solid Electrolytes Prepared by a Liquid-Phase Technique… | §4.4 | — |
| 195 | Yubuchi 2019 | An Argyrodite Sulfide-Based Superionic Conductor Synthesized by a Liquid-Phase Technique with Tetrahy- drofuran and Et… | §4.4 | — |
| 196 | Chida 2018 | Liquid-Phase Synthesis of Li6PS5Br Using Ultrasonication and Application to Cathode Composite Electrodes in All-Solid-… | §4.4 | — |
| 197 | Yao 2016 | High-Energy All-Solid-State Lithium Batteries with Ultralong Cycle Life. Nano Lett. | §4.4 | — |
| 198 | Zhang 2017 | Fe3S4@Li7P3S11 Nanocomposites as Cathode Materials for All-Solid- State Lithium Batteries with Improved Energy Density… | §4.4 | — |
| 199 | Xu 2018 | Rational Coating of Li7P3S11 Solid Electrolyte on MoS2 Electrode for All-Solid-State Lithium Ion Batteries. J. Power S… | §4.4 | — |
| 200 | Wan 2018 | Hu, Y.- S.; Yao, X. Core−Shell Fe1−xS@Na2.9PS3.95Se0.05 Nanorods for Room Temperature All-Solid-State Sodium Batteries… | §4.4 | — |
| 201 | Wan 2018 | Nanoscaled Na3PS4 Solid Electrolyte for All- Solid-State FeS2/Na Batteries with Ultrahigh Initial Coulombic Efficiency… | §4.4 | — |
| 202 | Long 2017 | Facile Synthesis of Co9s8 Nanosheets for Lithium Ion Batteries with Enhanced Rate Capability and Cycling Stability. Ne… | §4.4 | — |
| 203 | Homma 2011 | Crystal Structure and Phase Transitions of the Lithium Ionic Conductor Li3PS4. Solid State Ionics | §4.4 | — |
| 204 | Kim 2017 | Infiltration of Solution-Processable Solid Electrolytes into Conventional Li-Ion-Battery Electrodes for All-Solid- Sta… | §4.4 | — |
| 205 | Kim 2019 | Sheet-Type Li6PS5Cl-Infiltrated Si Anodes Fabricated by Solution Process for All-Solid-State Lithium-Ion Batteries. J.… | §4.4 | — |
| 206 | Kawaguchi 2018 | Dry Coating of Electrode Particle with Model Particle of Sulfide Solid Electrolytes for All-Solid-State Secondary Batt… | §4.4 | ✅ `kawaguchi2018_dry_coating_model_se_particle_powtec` |
| 207 | Han 2017 | Negating Interfacial Impedance in Garnet-Based Solid-State Li Metal Batteries. Nat. Mater. | §4.5 | — |
| 208 | Oh 2015 | Excellent Compatibility of Solvate Ionic Liquids with Sulfide Solid Electrolytes: Toward Favorable Ionic Contacts in B… | §4.5 | — |
| 209 | Oh 2019 | Slurry-Fabricable Li+-Conductive Polymeric Binders for Practical All-Solid-State Lithium-Ion Batteries Enabled by Solv… | §4.5 | — |
| 210 | Fan 2018 | Fluorinated Solid Electrolyte Interphase Enables Highly Reversible Solid-State Li Metal Battery. Science Advances | §4.5 | — |
| 211 | Chen 2017 | An Insight into Intrinsic Interfacial Properties between Li Metals and Li10GeP2S12 Solid Electrolytes. Phys. Chem. Che… | §5.1 | — |
| 212 | Hartmann 2013 | Degradation of Nasicon- Type Materials in Contact with Lithium Metal: Formation of Mixed Conducting Interphases (MCI) … | §5.1 | — |
| 213 | Wenzel 2018 | Interfacial Reactivity and Interphase Growth of Argyrodite Solid Electrolytes at Lithium Metal Electrodes. Solid State… | §5.1 | — |
| 214 | Hayashi 2004 | Characterization of Li2S−P2S5 Glass-Ceramics as a Solid Electrolyte for Lithium Secondary Batteries. Solid State Ionics | §5.1 | — |
| 215 | Nagao 2013 | In Situ Sem Study of a Lithium Deposition and Dissolution Mechanism in a Bulk-Type Solid-State Cell with a Li2S− P2S5 … | §5.1 | — |
| 216 | Trevey 2012 | Electrochemical Investigation of All-Solid-State Lithium Batteries with a High Capacity Sulfur-Based Electrode. J. Ele… | §5.1 | — |
| 217 | Bron 2017 | Impedance Characterization Reveals Mixed Conducting Interphases between Sulfidic Superionic Conductors and Lithium Met… | §5.1 | — |
| 218 | Zhang 2018 | Interface Re-Engineering of Li10GeP2S12 Electrolyte and Lithium Anode for All-Solid-State Lithium Batteries with Ultra… | §5.1 | — |
| 219 | Sahu 2014 | Air-Stable, High-Conduction Solid Electrolytes of Arsenic-Substituted Li4sns4. Energy Environ. Sci. | §5.1 | — |
| 220 | Liu 2018 | Stabilizing the Interface of Nasicon Solid Electrolyte against Li Metal with Atomic Layer Deposition. ACS Appl. Mater.… | §5.1 | — |
| 221 | Hao 2019 | Constructing Multifunctional Interphase between Li1.4Al0.4Ti1.6(PO4)3 and Li Metal by Magnet- ron Sputtering for Highl… | §5.1 | — |
| 222 | Tian 2019 | Reactivity-Guided Interface Design in Na Metal Solid-State Batteries. Joule | §5.1 | — |
| 223 | Yu 2019 | Insights into a Layered Hybrid Solid Electrolyte and Its Application in Long Lifespan High-Voltage All-Solid-State Lit… | §5.1 | — |
| 224 | Bosubabu 2019 | Lagp/ Li Interface Modification through a Wetted Polypropylene Interlayer for Solid State Li-Ion and Li−S Batteries. A… | §5.1 | — |
| 225 | Hu 2019 | Stabilizing the Interface between Sodium Metal Anode and Sulfide-Based Solid-State Electro- lyte with an Electron-Bloc… | §5.1 | — |
| 226 | Zhou 2016 | Plating a Dendrite-Free Lithium Anode with a Polymer/Ceramic/Polymer Sandwich Electrolyte. J. Am. Chem. Soc. | §5.1 | — |
| 227 | Liang 2018 | Stabilization of All-Solid-State Li−S Batteries with a Polymer−Ceramic Sandwich Electrolyte by Atomic Layer Deposition… | §5.1 | — |
| 228 | Yamamoto 2019 | Freestanding All-Solid-State Rechargeable Lithium Batteries with in-Situ Formed Positive Electrodes. Solid State Ionics | §5.1 | — |
| 229 | Sun 2016 | Yano, T.-a.; Hara, M.; Hirayama, M.; Kanno, R. Oxygen Substitution Effects in Li10GeP2S12 Solid Electrolyte. J. Power … | §5.1 | — |
| 230 | Zhang 2019 | All-in-One Improvement toward Li6PS5Br-Based Solid Electrolytes Triggered by Compositional Tune. J. Power Sources | §5.1 | — |
| 231 | Xu 2017 | Xu, R.-c.; Xia, X.-h.; Wang, X.-l.; Xia, Y.; Tu, J.-p. Tailored Li2S−P2S5 Glass-Ceramic Electrolyte by MoS2 Doping, Po… | §5.1 | — |
| 232 | Liu 2019 | High Air-Stability and Superior Lithium Ion Conduction of Li3 + 3xP1-xZnxS4-xOx by Aliovalent Substitution of Zno for … | §5.1 | — |
| 233 | Li 2010 | Li+ Ion Conductivity and Diffusion Mechanism in Α-Li3N and Β-Li3N. Energy Environ. Sci. | §5.1 | — |
| 234 | Park 2017 | Dendrite-Suppressed Lithium Plating from a Liquid Electrolyte Via Wetting of Li3N. Adv. Energy Mater. | §5.1 | — |
| 235 | Kızılaslan 2019 | Assembling All-Solid-State Lithium− Sulfur Batteries with Li3N-Protected Anodes. ChemPlusChem | §5.1 | — |
| 236 | Xu 2018 | Li3N-Modified Garnet Electrolyte for All-Solid-State Lithium Metal Batteries Operated at 40 °C. Nano Lett. | §5.1 | — |
| 237 | Li 2018 | Robust Pinhole-Free Li3N Solid Electrolyte Grown from Molten Lithium. ACS Cent. Sci. | §5.1 | — |
| 238 | Court-Castagnet 1993 | Ionic Conductivity-Enhancement of Licl by Homogeneous and Heteroge- neous Dopings. Solid State Ionics | §5.1 | — |
| 239 | Li 2012 | Enhancement of the Li Conductivity in Lif by Introducing Glass/Crystal Interfaces. Adv. Funct. Mater. | §5.1 | — |
| 240 | Sudo 2014 | Interface Behavior between Garnet-Type Lithium-Conducting Solid Electrolyte and Lithium Metal. Solid State Ionics | §5.2 | — |
| 241 | Suzuki 2015 | Transparent Cubic Garnet-Type Solid Electrolyte of Al2O3-Doped Li7La3Zr2O12. Solid State Ionics | §5.2 | — |
| 242 | Ishiguro 2013 | Stability of Nb-Doped Cubic Li7La3Z- r2O12 with Lithium Metal. J. Electrochem. Soc. | §5.2 | — |
| 243 | Basappa 2017 | Contact between Garnet- Type Solid Electrolyte and Lithium Metal Anode: Influence on Charge Transfer Resistance and Sh… | §5.2 | — |
| 244 | Zhang 2001 | Understanding Solid Electrolyte Interface Film Formation on Graphite Electrodes. Electrochem. Solid-State Lett. | §5.2 | — |
| 245 | Liu 2010 | Aging Mechanisms of LiFePO4 Batteries Deduced by Electrochemical and Structural Analyses. J. Electrochem. Soc. | §5.2 | — |
| 246 | Aurbach 2000 | Review of Selected Electrode−Solution Interactions Which Determine the Performance of Li and Li Ion Batteries. J. Powe… | §5.2 | — |
| 247 | Broussely 2005 | Main Aging Mechanisms in Li Ion Batteries. J. Power Sources | §5.2 | — |
| 248 | Wang 2017 | Conformal, Nanoscale Zno Surface Modification of Garnet-Based Solid-State Electrolyte for Lithium Metal Anodes. Nano L… | §5.2 | — |
| 249 | Luo 2016 | Transition from Superlithiophobicity to Superlithiophilicity of Garnet Solid-State Electrolyte. J. Am. Chem. Soc. | §5.2 | — |
| 250 | Tsai 2016 | Li7La3Zr2O12 Interface Modification for Li Dendrite Prevention. ACS Appl. Mater. Interfaces | §5.2 | — |
| 251 | Lu 2018 | An in Situ Element Permeation Constructed High Endurance Li− LLZO Interface at High Current Densities. J. Mater. Chem. A | §5.2 | — |
| 252 | Luo 2017 | Reducing Interfacial Resistance between Garnet-Structured Solid-State Electrolyte and Li-Metal Anode by a Germanium La… | §5.2 | — |
| 253 | Fu 2017 | Transient Behavior of the Metal Interface in Lithium Metal−Garnet Batteries. Angew. Chem., Int. Ed. | §5.2 | — |
| 254 | Zhou 2018 | Polymer Lithium-Garnet Interphase for an All-Solid-State Rechargeable Battery. Nano Energy | §5.2 | — |
| 255 | Liu 2017 | Garnet Solid Electrolyte Protected Li- Metal Batteries. ACS Appl. Mater. Interfaces | §5.2 | — |
| 256 | Wang 2013 | Exploring Polymeric Lithium Tartaric Acid Borate for Thermally Resistant Polymer Electrolyte of Lithium Batteries. Ele… | §5.2 | — |
| 257 | Zhang 2011 | Stability of Li/Polymer Electrolyte-Ionic Liquid Composite/Lithium Conducting Glass Ceramics in an Aqueous Electrolyte… | §5.2 | — |
| 258 | Zhang 2017 | High-Voltage and Free-Standing Poly(Propylene Carbonate)/Li6.75La3Zr1.75Ta0.25O12 Composite Solid Electrolyte for Wide… | §5.2 | — |
| 259 | Zhang 2016 | Flexible and Ion-Conducting Membrane Electrolytes for Solid-State Lithium Batteries: Dispersion of Garnet Nanoparticle… | §5.2 | — |
| 260 | Croce 1998 | Nano- composite Polymer Electrolytes for Lithium Batteries. Nature | §5.2 | — |
| 261 | Sharafi 2017 | Impact of Air Exposure and Surface Chemistry on Li−Li7La3Zr2O12 Interfacial Resistance. J. Mater. Chem. A | §5.2 | — |
| 262 | Cheng 2014 | The Origin of High Electrolyte−Electrode Interfacial Resistances in Lithium Cells Containing Garnet Type Solid Electro… | §5.2 | — |
| 263 | Shimonishi 2011 | Synthesis of Garnet-Type Li7−xLa3Z- r2O12−1/2x and Its Stability in Aqueous Solutions. Solid State Ionics | §5.2 | — |
| 264 | Galven 2012 | Instability of Lithium Garnets against Moisture. Structural Characterization and Dynamics of Li7-xHxLa3Sn2O12 and Li5-… | §5.2 | — |
| 265 | Toda 2013 | Low Temperature Cubic Garnet-Type Co2-Doped Li7La3Zr2O12. Solid State Ionics | §5.2 | — |
| 266 | Xia 2016 | Ionic Conductivity and Air Stability of Al-Doped Li7La3Zr2O12 Sintered in Alumina and Pt Crucibles. ACS Appl. Mater. I… | §5.2 | — |
| 267 | Taylor 2018 | Demonstration of High Current Densities and Extended Cycling in the Garnet Li7La3Zr2O12 Solid Electrolyte. J. Power So… | §5.2 | — |
| 268 | Sharafi 2017 | Surface Chemistry Mechanism of Ultra-Low Interfacial Resistance in the Solid-State Electrolyte Li7La3Zr2O12. Chem. Mat… | §5.2 | — |
| 269 | Wang 2018 | Stabilizing Interface between Li10Sn2S12 and Li Metal by Molecular Layer Deposition. Nano Energy | Table 1 | — |
| 270 | Xie 2018 | High Ion Conductive Sb2O5-Doped Β-Li3PS4 with Excellent Stability against Li for All-Solid-State Lithium Batteries. J.… | Table 1 | — |
| 271 | Gao 2018 | Salt-Based Organic−Inorganic Nanocomposites: Towards a Stable Lithium Metal/Li10GeP2S12 Solid Electrolyte Interface. A… | Table 1 | — |
| 272 | Xu 2018 | Interface Engineering of Sulfide Electrolytes for All-Solid-State Lithium Batteries. Nano Energy | Table 1 | — |
| 273 | Zheng 2018 | Stabilizing Li10SnP2S12/Li Interface Via an in Situ Formed Solid Electrolyte Interphase Layer. ACS Appl. Mater. Interf… | Table 1 | — |
| 274 | Sang 2018 | Understanding the Effect of Interlayers at the Thiophosphate Solid Electrolyte/Lithium Interface for All-Solid-State L… | Table 1 | — |
| 275 | Umeshbabu 2019 | Stable Cycling Lithium−Sulfur Solid Batteries with Enhanced Li/ Li10GeP2S12 Solid Electrolyte Interface Stability. ACS… | Table 1 | — |
| 276 | Liang 2019 | An Air-Stable and Dendrite-Free Li Anode for Highly Stable All-Solid-State Sulfide-Based Li Batteries. Adv. Energy Mat… | Table 1 | — |
| 277 | Wang 2019 | Solid-State Plastic Crystal Electrolytes: Effective Protection Interlayers for Sulfide-Based All-Solid-State Lithium M… | Table 1 | — |
| 278 | Philip 2019 | Improving Cell Resistance and Cycle Life with Solvate-Coated Thiophosphate Solid Electrolytes in Lithium Batteries. AC… | Table 1 | — |
| 279 | Shen 2018 | Unlocking the Energy Capabilities of Lithium Metal Electrode with Solid-State Electrolytes. Joule | §5.3 | — |
| 280 | LePage 2019 | Lithium Mechanics: Roles of Strain Rate and Temperature and Implications for Lithium Metal Batteries. J. Electrochem. … | §5.3 | — |
| 281 | Wang 2018 | Correlating the Interface Resistance and Surface Adhesion of the Li Metal-Solid Electrolyte Interface. J. Power Sources | §5.3 | — |
| 282 | Wood 2017 | Lithium Metal Anodes: Toward an Improved Understanding of Coupled Morpho- logical, Electrochemical, and Mechanical Beh… | §5.3 | — |
| 283 | Cheng 2017 | Intergranular Li Metal Propagation through Polycrystalline Li6.25Al0.25La3Zr2O12 Ceramic Electrolyte. Electrochim. Acta | §5.3 | — |
| 284 | Porz 2017 | Mechanism of Lithium Metal Penetration through Inorganic Solid Electrolytes. Adv. Energy Mater. | §5.3 | — |
| 285 | Wu 2018 | The Role of the Solid Electrolyte Interphase Layer in Preventing Li Dendrite Growth in Solid-State Batteries. Energy E… | §5.3 | — |
| 286 | Yu 2016 | Elastic Properties of the Solid Electrolyte Li7La3Zr2O12 (LLZO). Chem. Mater. | §5.3 | — |
| 287 | Sundström 1995 | On Morphological Instability During Electrodeposition with a Stagnant Binary Electrolyte. Electro- chim. Acta | §5.3 | — |
| 288 | Monroe 2005 | The Impact of Elastic Deformation on Deposition Kinetics at Lithium/Polymer Interfaces. J. Electrochem. Soc. | §5.3 | — |
| 289 | Barai 2017 | Effect of Initial State of Lithium on the Propensity for Dendrite Formation: A Theoretical Study. J. Electrochem. Soc. | §5.3 | — |
| 290 | Yu 2018 | Grain Boundary Softening: A Potential Mechanism for Lithium Metal Penetration through Stiff Solid Electrolytes. ACS Ap… | §5.3 | — |
| 291 | Masias 2019 | Elastic, Plastic, and Creep Mechanical Properties of Lithium Metal. J. Mater. Sci. | §5.3 | — |
| 292 | Kasemchainan 2019 | Critical Stripping Current Leads to Dendrite Formation on Plating in Lithium Anode Solid Electrolyte Cells. Nat. Mater. | §5.3 | — |
| 293 | Wang 2019 | Temperature Dependent Flux Balance of the Li/Li7La3Zr2O12 Interface. Electro- chim. Acta | §5.3 | — |
| 294 | Krauskopf 2019 | Toward a Fundamental Understanding of the Lithium Metal Anode in Solid-State Batteriesan Electrochemo-Mechanical Stud… | §5.3 | — |
| 295 | Koshikawa 2018 | Dynamic Changes in Charge-Transfer Resistance at Li Metal/Li7La3Zr2O12 Interfaces During Electrochemical Li Dissolutio… | §5.3 | — |
| 296 | Janek 2000 | Oscillatory Kinetics at Solid/Solid Phase Boundaries in Ionic Crystals. Solid State Ionics | §5.3 | — |
| 297 | Swamy 2018 | Lithium Metal Penetration Induced by Electrodeposition through Solid Electrolytes: Example in Single-Crystal Li6La3ZrT… | §5.3 | — |
| 298 | Shen 2018 | Effect of Pore Connectivity on Li Dendrite Propagation within LLZO Electrolytes Observed with Synchrotron X-Ray Tomogr… | §5.3 | — |
| 299 | Sharafi 2017 | Controlling and Correlating the Effect of Grain Size with the Mechanical and Electrochemical Properties of Li7La3Zr2O1… | §5.3 | — |
| 300 | Cheng 2015 | Interrelationships among Grain Size, Surface Composition, Air Stability, and Interfacial Resistance of Al-Substituted … | §5.3 | — |
| 301 | Tschopp 2012 | Probing Grain Boundary Sink Strength at the Nanoscale: Energetics and Length Scales of Vacancy and Interstitial Absorp… | §5.3 | — |
| 302 | David 2015 | Microstructure and Li-Ion Conductivity of Hot-Pressed Cubic Li7La3Zr2O12. J. Am. Ceram. Soc. | §5.3 | — |
| 303 | Saylor 2004 | Habits of Grains in Dense Polycrystalline Solids. J. Am. Ceram. Soc. | §5.3 | — |
| 304 | Pesci 2018 | Elucidating the Role of Dopants in the Critical Current Density for Dendrite Formation in Garnet Electrolytes. J. Mate… | §5.3 | — |
| 305 | Xu 2014 | Electrolytes and Interphases in Li-Ion Batteries and Beyond. Chem. Rev. | §5.4 | — |
| 306 | Cheng 2017 | Toward Safe Lithium Metal Anode in Rechargeable Batteries: A Review. Chem. Rev. | §5.4 | — |
| 307 | Fang 2019 | Quantifying Inactive Lithium in Lithium Metal Batteries. Nature | §5.4 | — |
| 308 | Niu 2019 | High-Energy Lithium Metal Pouch Cells with Limited Anode Swelling and Long Stable Cycles. Nature Energy | §5.4 | — |
| 309 | Peled 1997 | Advanced Model for Solid Electrolyte Interphase Electrodes in Liquid and Polymer Electrolytes. J. Electrochem. Soc. | §5.4 | — |
| 310 | Cao 2019 | Monolithic Solid−Electrolyte Interphases Formed in Fluorinated Orthoformate- Based Electrolytes Minimize Li Depletion … | §5.4 | — |
| 311 | Li 2016 | An Artificial Solid Electrolyte Interphase Layer for Stable Lithium Metal Anodes. Adv. Mater. | §5.4 | — |
| 312 | Xu 2019 | Zhao, C.- Z.; Huang, J.-Q.; Zhang, Q. Artificial Interphases for Highly Stable Lithium Metal Anode. Matter | §5.4 | — |
| 313 | Liu 2018 | An Ultrastrong Double-Layer Nano- diamond Interface for Stable Lithium Metal Anodes. Joule | §5.4 | — |
| 314 | Gu 2018 | Designable Ultra- Smooth Ultra-Thin Solid-Electrolyte Interphases of Three Alkali Metal Anodes. Nat. Commun. | §5.4 | — |
| 315 | Lu 2015 | Failure Mechanism for Fast-Charged Lithium Metal Batteries with Liquid Electrolytes. Adv. Energy Mater. | §5.4 | — |
| 316 | Fang 2019 | Key Issues Hindering a Practical Lithium-Metal Anode. Trends in Chemistry | §5.4 | — |
| 317 | Nagpure 2018 | Impacts of Lean Electrolyte on Cycle Life for Rechargeable Li Metal Batteries. J. Power Sources | §5.4 | — |
| 318 | Pei 2017 | Nanoscale Nucleation and Growth of Electrodeposited Lithium Metal. Nano Lett. | §5.4 | — |
| 319 | Wang 2019 | Improving Cyclability of Li Metal Batteries at Elevated Temperatures and Its Origin Revealed by Cryo-Electron Microsco… | §5.4 | — |
| 320 | Weber 2019 | Long Cycle Life and Dendrite-Free Lithium Morphology in Anode-Free Lithium Pouch Cells Enabled by a Dual- Salt Liquid … | §5.4 | — |
| 321 | Albertus 2018 | Status and Challenges in Enabling the Lithium Metal Electrode for High-Energy and Low-Cost Rechargeable Batteries. Nat… | §5.4 | — |
| 322 | Zhu 2017 | Strategies Based on Nitride Materials Chemistry to Stabilize Li Metal Anode. Advanced Science | §6 | — |
| 323 | Wang 2016 | In Situ Stem-Eels Observation of Nanoscale Interfacial Phenomena in All-Solid-State Batteries. Nano Lett. | §6 | — |
| 324 | Brazier 2008 | First Cross-Section Observation of an All Solid-State Lithium-Ion “Nanobattery” by Transmission Electron Microscopy. C… | §6 | — |
| 325 | Wang 2017 | New Insights on the Structure of Electrochemically Deposited Lithium Metal and Its Solid Electrolyte Interphases Via C… | §6 | — |
| 326 | Lee 2019 | Cryogenic Focused Ion Beam Characterization of Lithium Metal Anodes. ACS Energy Letters | §6 | — |
| 327 | Banerjee 2019 | Cheng, J.-h.; Nguyen, H.; Zhang, M.; Tan, D.; Wynn, T.; Wu, E.; Doux, J.-M.; et al. Revealing Nanoscale Solid-Solid In… | §6 | = ref 51 (중복 수록) |
| 328 | Harry 2014 | Detection of Subsurface Structures Underneath Dendrites Formed on Cycled Lithium Metal Electrodes. Nat. Mater. | §6 | — |
| 329 | Seitzman 2018 | Toward All-Solid-State Lithium Batteries: Three-Dimensional Visualization of Lithium Migration in Beta-Li3PS4 Ceramic … | §6 | — |
| 330 | Liang 2018 | Mitigating Interfacial Potential Drop of Cathode−Solid Electrolyte Via Ionic Conductor Layer to Enhance Interface Dyna… | §6 | — |
| 331 | Gittleson 2017 | Non-Faradaic Li+ Migration and Chemical Coordination across Solid-State Battery Interfaces. Nano Lett. | §6 | — |
| 332 | Fingerle 2017 | Reaction and Space Charge Layer Formation at the LiCoO2−Lipon Interface: Insights on Defect Formation and Ion Energy L… | §6 | — |
| 333 | Wenzel 2015 | Interphase Formation on Lithium Solid Electrolytesan in Situ Approach to Study Interfacial Reactions by Photoelectron… | §6 | — |
| 334 | Wood 2018 | Operando X-Ray Photo- electron Spectroscopy of Solid Electrolyte Interphase Formation and Evolution in Li2s-P2s5 Solid… | §6 | — |
| 335 | Rettenwander 2018 | Interface Instability of Fe-Stabilized Li7La3Zr2O12 Versus Li Metal. J. Phys. Chem. C | §6 | — |
| 336 | Sang 2017 | Evolution at the Solid Electrolyte/Gold Electrode Interface During Lithium Deposition and Stripping. Chem. Mater. | §6 | — |
| 337 | Otoyama 2016 | Raman Imaging for LiCoO2 Composite Positive Electrodes in All-Solid-State Lithium Batteries Using Li2S−P2S5 Solid Elec… | §6 | — |
| 338 | Zhang 2017 | Interfacial Processes and Influence of Composite Cathode Microstructure Controlling the Performance of All-Solid-State… | §6 | — |
| 339 | Wang 2012 | In Polymers for Energy Storage and Delivery: Polyelectrolytes for Batteries and Fuel Cells; American Chemical Society | §6 | — |
| 340 | Wang 2017 | In Situ Neutron Depth Profiling of Lithium Metal−Garnet Interfaces for Solid State Batteries. J. Am. Chem. Soc. | §6 | — |
| 341 | Han 2019 | High Electronic Conductivity as the Origin of Lithium Dendrite Formation within Solid Electrolytes. Nature Energy | §6 | — |

<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     서식 참고 = papers/kim2026_li_argyrodite_sei_reactive_md.md · papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md (같은 계면 · MLIP 반응 MD)
     2026-10-13 신규 (litdb-curator) — 사용자가 "중요한 새 논문" 으로 지정.
     ① 그림: 자동 추출 7장 (본문 Fig. 1–7) + 손 크롭 7장 (SI 캡션이 'FIG. S.1.' 꼴이라 추출기가 SI 에서 0 개를 냈다 →
        Fig. S1–S5 · Table S1–S2 를 figures.json 에 manual_crop 사유와 함께 넣었다) + Fig. 4 재크롭 (자동 크롭이 아래 절반만 잡았다 → recrop).
        14장 전부 실제로 봤다. 판독용 확대 렌더 5장 (Fig. 3f 삽입 · Fig. 5a · Fig. 5b 삽입 · Fig. 7d · Fig. 7e) 은 스크래치에만 있다.
     ② 그림에서만 읽은 값 = 'figure-read ≈' · 우리가 유도한 값 = '✎ 우리 산수' · 그림을 디지타이즈해 다시 맞춘 값 = '✎ 우리 재독'.
     ③ CLAUDE.md 데이터 규율 3종 (홉 수 검산 · 관측창 · 결합 자리 배위수) 을 이 논문에 적용했다 → §7-5.
     ④ PDF 안 문장은 자료로만 읽었다. -->

# Reversible Ion Transport Through an Irreversibly Percolating Li₂S Interphase at the Li/Li₆PS₅Cl Interface — Yuan, Chen & Dawson (ChemRxiv preprint 2026)

> slug `yuan2026_percolating_li2s_interphase_efield_md` · DOI `10.26434/chemrxiv.15010110/v1` · type `MLIP-MD (fine-tuned CHGNet + GFN1-xTB 동적 전하 + 외부 전기장) + DFT 보조 (VASP PBEsol: 학습용 AIMD · 잘라낸 슬랩 DOS) — 실험 0` · PDF 본문 `ffa686c4` (17 pp = ChemRxiv 표지 1 + 원고 16) · SI `33e40a5a` (13 pp · `Fig. S1`–`S5` · `Table S1`–`S2`) · digested `2026-10-13` · status ✅ · 태그 **[외부·⛔ PREPRINT 미심사]** · **사용자가 중요 신규 논문으로 지정 (2026-10-13)**

> elements: Li, P, S, Cl
> methods: DFT, AIMD, MD, MLIP, DOS, PDOS

> **저자** Tianmu Yuan¹ (교신 · tianmu.yuan@newcastle.ac.uk) · Zhimin Chen¹² · **James A. Dawson**¹² (교신) — ¹Newcastle University, Chemistry – School of Natural and Environmental Sciences · ²The Faraday Institution (Didcot).
> 게시 **2026-10-08** (ChemRxiv **v1** · CC-BY 4.0 · 매 쪽 *"This is a preprint and has not been peer reviewed. Data may be preliminary."*) · 저널 투고 정보 없음 · refs **62** (SI refs 2).
> 자금: UKRI Horizon Europe guarantee **EP/Z000254/1** · Faraday Institution **FIRG026** · ARCHER2 (UK HEC Materials Chemistry Consortium, EPSRC **EP/X035859/1**) · Google Cloud Research Credits **GCP19980904**. **데이터 공개 없음** — *"available from the corresponding author upon reasonable request"*.
> 원본 (git 무시 폴더): `litdb/inbox/Yuan2026 ChemRxiv Reversible Ion Transport Through an Irreversibly Percolating Li2S Interphase at the Li-Li6PS5Cl Interface.pdf` + 같은 이름 앞에 `Sup) `.
> 🎤 관련 발표: **인입 대기열 등재 없음** (2026-10-13 `talks/*` 대기열 확인). 주제상 `talks/lee2026_skku_mlip_materials_design.md` §3 의 *시뮬레이션–실험 괴리 4번 = 외부 환경 (비평형 · 전기장 · 농도구배)* 에 정면으로 해당하는 문헌 사례다 — ⛔ 그 talk 은 citable=no, 방향은 논문 → talk 뿐이고 이 digest 는 talk 을 고치지 않았다.
> ⚠ **`[Yuan26LCE]` (`papers/yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal.md`) 와 다른 논문 · 다른 저자다** (그쪽은 Qunyao Yuan · Fudan · 고분자 전해질).

---

## 0. 이 digest 를 읽는 법 — 트랙을 먼저

**질문 하나**: Li 금속과 Li₆PS₅Cl (LPSCl) 이 닿은 계면에 전기장을 걸어 Li 를 한쪽으로 보냈다가 장을 뒤집으면, **Li 흐름뿐 아니라 계면상(interphase) 구조도 되돌아가나?**
**답 하나**: Li 흐름은 장을 따라 바로 뒤집힌다. 그런데 한번 생긴 **Li₂S-like 연결망**과 사라진 **아르지로다이트 배위**는 돌아오지 않는다 → *"구조 기억(structural memory)이 Li 가 실제로 건너는 계면상을 정한다."*

| 트랙 (1저자) | 이 논문과 닿는 곳 | 한 줄 판정 | 절 |
|---|---|---|---|
| **SEI NEB (사용자)** — Li₂S V_Li⁻ c→c CI-NEB 셀 수렴 · Li₃Nd | 'Li₂S-like' 망을 지나는 Li 수송 | **다른 양이다.** 우리 = 0 K 결정 Li₂S 단일 홉 장벽 · 이 논문 = 425 K Li-과잉 비정질 혼합 영역의 in-plane D 와 장 구동 σ. **논문은 장벽(Ea)을 하나도 내지 않는다** | §7-1 |
| **ESW · 분해 계면 (사용자)** | 반응식 (7) 의 방향 · '비가역' 의 열역학 · 산물의 전자구조 | 방향은 우리 음극 게이트 (Li 흡수 · 원소 S 없음) 와 같은 쪽 · **'비가역' 은 우리 hull 이 이미 말하는 것** (LPSCl 환원 가장자리 ≈ 1.72 V ≫ 음극 ≈ 0 V) | §7-2 |
| **li2s (외부 1저자 · 사용자 ≠ 1저자)** | 'Li₂S' · 'interphase' 라는 낱말만 같다 | **같은 계가 아니다** — 이 논문 = Li 금속 음극의 **환원 산물** (P⁵⁺ → P³⁻ · Li 과잉), li2s = Li–S 양극 **볼밀 LPSCl@Li₂S** (환원 없음). 가져올 것은 분석 방법뿐 · 해석은 잠정 | §7-3 |

⚠⚠ **먼저 알고 읽을 것 셋**
1. **PREPRINT** — 이 digest 의 수치·주장을 쓸 때마다 **"[Yuan ChemRxiv 2026, 미심사]"** 를 붙인다.
2. **제목의 'Li₂S' 는 결정 Li₂S 가 아니다.** 본문은 일관되게 *Li₂S-like* 라 쓰고, 그 정의는 *"남은 아르지로다이트형 P 에서 4.50 Å 밖에 있는 S"* 다 (§4-5). 저자 스스로 *"this is not evidence of their separate crystalline domains or stoichiometries"* 라 적는다.
3. **전자가 없는 MD 다.** MLIP 는 원자 위치로만 에너지를 주고, 장은 원자 부분전하에 **F = qE** 로만 작용한다. 그래서 Li 는 '이온 + 외부회로의 전자' 가 아니라 **전자를 데리고 다니는 원자**로 움직인다 (§6-3). 이 한 가지가 *reversible transport* 와 *irreversible interphase* 의 해석을 다 바꾼다.

**본 그림 (2026-10-13)**: `Fig. 1`–`Fig. 7` (`Fig. 4` 는 재크롭본) · `Fig. S1`–`Fig. S5` · `Table S1`–`Table S2` — **14장 전부 봤다. 안 본 그림 없음.** 표 두 장은 크롭이 맞는지만 보고 수치는 PDF 텍스트에서 옮겼다. 논문 표기는 `FIG. S.1` 꼴인데 이 digest 는 웹앱 링크를 위해 `Fig. S1` 로 쓴다.

---

## 1. 한 줄 요약

Li(100) ~50 Å ‖ Li₆PS₅Cl(010) ~50 Å 슬랩 (**2,524 원자** · 진공 15 Å) 을 **계면 데이터로 미세조정한 CHGNet** 으로 **425 K** 에서 돌리면 — (i) 장 없이 **1 ns** 동안 Li₂S-like 계면상이 **√t** 로 자라고 (τ_SEI = 24 Å + **0.99 Å ps^−½**·√t, R² 0.992), (ii) GFN1-xTB 로 **1 ps 마다** 다시 계산한 원자전하에 **+0.1 V Å⁻¹** 를 걸면 성장 계수가 **6.77 Å ps^−½ (≈ 7배)** 로 뛰어 전해질 슬랩 전체가 **~100 ps** 에 변환되고, (iii) 음이온 그래프상 **Li₂S-like S 만 하나의 연결망** (Φ_S → 1) 을 이루며 Li₃P-·LiCl-like 는 **~10 원자** 클러스터로 흩어지고, (iv) 350 ps 에 장을 **−0.1 V Å⁻¹** 로 뒤집으면 Li 순유속은 곧 반대로 흘러 **0.419 Li ps⁻¹** (σ_eff **0.166 S cm⁻¹**) 로 선형 증가하지만 **연결망과 아르지로다이트 배위는 돌아오지 않는다.** 저자 결론: *"structural memory, not instantaneous transport direction, determines the interphase that Li ions actually cross"* → 음극 계면 저항·반응성은 초기 사이클에 정해지고 전류 반전으로 리셋되지 않는다 (외삽).

---

## 2. 메타 / 계보 / 질문

| 항목 | 내용 |
|---|---|
| 계 | Li 금속 (bcc, **(100)**) ‖ Li₆PS₅Cl (**(010)**) · 계면 **1 면** + 진공 15 Å · **상대전극 없음** (반대쪽은 진공에 면한 SE 자유표면) |
| 질문 | ① 장 없이 계면이 어떻게 자라나 ② 방향성 Li 수송(장)과 계면 반응이 같이 가면 ③ 장을 뒤집으면 구조도 되돌아가나 ④ 산물이 연결망을 이루나 ⑤ 반응 영역이 전자를 막나 |
| 방법 | 미세조정 CHGNet (LAMMPS) + GFN1-xTB 동적 전하 (CP2K) + LAMMPS `efield` · 학습 AIMD 와 DOS 는 VASP PBEsol |
| 자체 실험 | **없음** |
| 같은 그룹 계보 | Dawson = `[Famprikis19]` (ref 6 · `papers/famprikis2019_fundamentals_inorganic_sse.md`) 공저자 · `[Dutra25Rev]` (ref 7 · `papers/dutra2025_atomistic_modelling_ml_se_review.md`) 교신저자 — 필드 표준 리뷰를 쓴 그룹이 직접 반응 MD 에 들어온 편 |
| litdb 에 있는 인용 원전 | ref 35 = `[Wang22Res]` (`papers/wang2022_resistive_decomposing_interfaces_se_alkali_metal.md`) — Li₂S·Li₃P·LiCl 이원 산물의 Li 수송 · ref 38 Aktekin 2023 Nat. Commun. = 반응식 (7) 의 출처 (digest 없음) |
| ⚠ **안 인용한 선행** (같은 계면 · 같은 MLIP 반응 MD) | `[Chaney24SEI]` (`papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md` · ACS AMI 2024 — 비정질 log t → 결정화 · antifluorite 고용체) · `papers/kim2026_li_argyrodite_sei_reactive_md.md` (SSRN preprint — S-rich 비정질 → Li₂S 핵생성 → 구조적 자기 부동태화). 서론의 *"order into an antifluorite-like phase"* · *"two stages"* 는 refs 40–42 (Baer 2026 *J. Mater. Chem. A* · Ding/Kozinsky arXiv 2025 · He & Luo 2026 *J. Energy Storage*) 로만 귀속된다. **성장 법칙이 Chaney 와 다르다는 점 (§10-6) 은 논의되지 않는다** |
| 장 크기 근거 | ref 48 (Zhang 2025 *Nat. Commun.*) 과 *"consistent with values used in previous atomistic studies"* 한 줄 |
| 면 방향 근거 | SI §III — Xie 2024 *Adv. Energy Mater.* 의 표면에너지 (010 0.34 · 110 0.37 · 111 0.22 J m⁻²) 와 4 조합 D 비교 (`Table S2`) |

---

## 3. 핵심 수치 총정리 ★

| 구분 | 양 | 값 | 출처 | 비고 |
|---|---|---|---|---|
| 셀 | 크기 · 원자수 | 23.81 × 17.02 × 140.38 Å · **2,524 원자** | §IV B | 면적 405.15 Å² (`Eq. 5`) — ✎ 23.81 × 17.02 = 405.25 (0.1 Å² 차 · 반올림) |
| | 슬랩 | Li ~50 Å + LPSCl ~50 Å (*"each at least 50 Å thick"*) · 진공 15 Å | §II A · §IV B | ✎ 우리 산수: N_S ≈ 150 / 0.29 ≈ **5.2×10²** (SI §V 의 S_max 와 Φ_S) → LPSCl ≈ **100 f.u.** (≈ 1.3–1.5k 원자) · Li 금속 ≈ **1.1–1.2k 원자** — 논문 미기재 |
| | 격자 정합 | **미기재** | — | ✎ Li(100) 을 7 × 5 로 놓으면 a ≈ 3.40 Å 가 된다 (우리 산수 · 어느 쪽을 얼마나 늘렸는지 본문 0 줄) |
| 조건 | T · dt · 열욕 | **425 K** · 1 fs · CSVR (평형 10 fs / 생산 50 fs) · NVT · 바로스탯 없음 · COM 병진 10 fs 마다 제거 | §IV B | 425 K = Li 융점 (≈ 454 K) 의 0.94 |
| | 평형 | 15 ps (그동안 반응이 이미 시작) | §II A | 장 없음 생산 시작 때 τ₀ = 24 Å · Φ_S ≈ 0.29 |
| | 길이 | 장 없음 ~1 ns · 장 +0.1 → 350 ps → −0.1 → 350 ps (총 **700 ps**) | §II A–B | 초록의 *"for nanoseconds"* 는 장 없음 런만 맞다 |
| MLIP | 검증 RMSE | 힘 **6.5–6.7 × 10⁻² eV Å⁻¹** · 에너지 **3.3–4.6 × 10⁻⁴ eV/atom** (4 세트) | `Fig. S1` | 검증셋 = **반응 전** 계면 AIMD 350·500 K |
| 장 없음 | D_xy (계면상) | 0.07 ns 창 ≈ 0.066 → 1 ns 창 ≈ 0.009 Å² ps⁻¹ (figure-read ≈) | `Fig. 2b` | 벌크 LPSCl **AIMD 0.031 Å² ps⁻¹** (본문 · AIMD 조건 미기재) |
| | σ_xy^NE | ≈ 1.3 → ≈ 0.18 S cm⁻¹ (figure-read ≈ · 마지막 점 = 본문 *"approximately 0.18"*) | `Fig. 2c` | 벌크 기준선 figure-read ≈ 0.35 S cm⁻¹ |
| | 조성 (Li 중심 환경) | Li 금속 **45 → 27 %** · LPSCl **25 → 13 %** · Li₂S-like **20 → 45 %** · unclassified → **~5 %** | 본문 · `Fig. 3e` | figure-read ≈ Li₃P 3.7 → 5.5 · LiCl 1.8 → 2.9 · LiP ≈ 0 % |
| | 성장 | τ_SEI = τ₀ + k_W√t · **τ₀ = 24 Å · k_W^eq = 0.99 Å ps^−½** · R² 0.992 | `Eq. 4` · `Fig. 3f` | ✎ 1 ns 에 ≈ 55 Å · ✎ 우리 재독 자유지수 ≈ 0.54 (§5-1) |
| 장 | 크기 · 방향 | **±0.1 V Å⁻¹** (= 10⁹ V m⁻¹) · +z = Li 금속 → SE | §II B | ✎ SE 슬랩 ~60 Å 에 걸리는 전위 ≈ 6 V |
| | 전하 갱신 | GFN1-xTB **1 ps** 마다 (사이에는 고정) | §IV C | |
| | LPSCl 소멸 | *"negligible within approximately the first 60 ps"* | 본문 · `Fig. 5a` | ⚠ figure-read ≈ 60 ps 에 ≈ 9 %, ≈ 95 ps 에 0 |
| | 금속 Li 분율 | 최소 ≈ 200 ps 뒤 반대편에 다시 쌓임 | 본문 · `Fig. 5a` | figure-read ≈ 55 → ~4 % (≈ 200 ps) → ~12 % (350 ps) → ~4 % (≈ 430 ps) → ~10 % (700 ps) |
| | Li₂S-like 분율 | — | `Fig. 5a` | figure-read ≈ ~150 ps 뒤 **67–70 %** 로 평탄 — 반전 뒤에도 그대로 |
| | 성장 | **k_W^ef = 6.77 Å ps^−½** (첫 100 ps 만) · R² 0.987 | `Fig. 5b` | 6.77 / 0.99 = 6.8 → ✎ 같은 두께까지 걸리는 **시간**으로는 (6.8)² ≈ **47 배** |
| | 연결망 | Φ_S **< 0.1 → 1** (~100 ps) · Φ_P, Φ_Cl **≈ 0.1** · 최대 P/Cl 클러스터 **~10 원자** | `Fig. 6b,c` | Φ_S = 1 은 반전 뒤에도 유지 |
| | S_max 지수 | **α = 0.77** (t < t* ≈ 6 ps) · **0.49** (≈ 10–100 ps) | `Fig. 6c` · `Eq. 8` | 플래토 figure-read ≈ 5.6×10² |
| | JMAK | **n = 0.74** (1–100 ps) | `Fig. 6d` · `Eq. 10` | 서술용 (저자 명시) |
| 반전 | Li 순 이동 | **dN_Li/dt = 0.419 ps⁻¹** (R² 0.9842 · 분석 구간 **450–700 ps**) | `Fig. 5c` | 250 ps 동안 ≈ 105 개 |
| | 유속 · 전류 | J = **1.034 × 10⁻³ ps⁻¹ Å⁻²** · j = **1.65 × 10¹⁰ A m⁻²** | `Eq. 5` | ✎ = 1.65 × 10⁶ A cm⁻² (실셀 1 mA cm⁻² 의 ~10⁹ 배) |
| | σ_eff = J/E | **16.6 S m⁻¹ = 0.166 S cm⁻¹** | `Eq. 6` | σ_xy^NE ≈ 0.18 과 *"order-of-magnitude comparison only"* (저자) |
| 장 없음 연결망 (SI) | Φ · 클러스터 수 | Φ_S **0.29 → 0.65** · S 클러스터 **≈ 1 개** · Φ_P 0.05 → 0.11 (250 ps 뒤 일정) · Φ_Cl 0.03–0.06 · P/Cl 클러스터 **≈ 20 → 34 / 38** | `Fig. S5b,e` | 최대 P/Cl 클러스터 ≤ ~10 원자 |
| | S_max · JMAK | **α = 0.47** · **n = 0.45 ± 0.02** (시간 오프셋 t₀ 맞춤 · R² 0.994) | `Fig. S5c,d` · `Eq. S1` | 이른 α = 0.77 구간 없음 (평형 15 ps 에 지나감) |
| 전자구조 | 벌크 LPSCl 갭 | *"approximately 2 eV"* | `Fig. 7e` | PBEsol · 6×6×6 k · Gaussian 0.05 eV · **DOS 판독** |
| | 슬랩 i | **Li₉₄P₆S₃₁Cl₈** · 음이온 수용 한도 2N_S + 3N_P + N_Cl = **88 e⁻** → **≥ 6 e⁻ 과잉** | `Fig. 7c` | E_F 가 S 띠 끝 (E − E_F ≈ −0.5 eV) 위 |
| | 슬랩 ii | **Li₈₅P₇S₃₁Cl₇** · 한도 **90 e⁻** → **≤ 5 e⁻ 부족** | `Fig. 7d` | E_F 가 S 띠 꼭대기 · 그 위 최소는 *"not a clean gap"* |
| 면 방향 (SI) | D_xy 4 조합 × 4 T | 275 / 325 / 375 / 425 K — (010)/Li(100) 0.0072 / 0.0109 / 0.0168 / 0.0207 · (010)/Li(111) 0.0090 / 0.0125 / 0.0197 / 0.0290 · (111)/Li(100) 0.0116 / 0.0138 / 0.0226 / 0.0219 · (111)/Li(111) 0.0125 / 0.0132 / 0.0161 / 0.0249 Å² ps⁻¹ | `Table S2` | 궤적 ≥ 200 ps · 시드 1 |
| | σ_xy^NE | figure-read ≈ 0.21–0.57 S cm⁻¹ (275 K 에서도 0.21–0.37) | `Fig. S3` | 비단조 2 조합 |
| 분류 컷오프 | P–S 결합 · S/Cl 소속 · P–P | **2.70** · **4.50 / 4.90** · **2.60 Å** | §IV D | Li 껍질: Li–S **3.58** (Li₂S) · Li–P **3.60** (Li₃P) / **3.15** (LiP) · Li–Cl **3.46 Å** |
| 그래프 컷오프 | S–S · P–P · Cl–Cl | **4.4 · 5.0 · 4.2 Å** | `Fig. S4` | 결정 Li₂S / Li₃P / LiCl 의 425 K g(r) 첫 극소 |

---

## 4. 계산 방법 ★ (DFT · MLIP · MD · 장 · 분석 정의)

### 4-1 DFT / AIMD — 학습 데이터 (§IV A · SI §I)
- **code** VASP · **PAW** · **functional PBEsol** · **vdW DFT-D3 (zero damping)** · **ecut 520 eV** · **spin-polarised** (*"required by CHGNet"* — 자기모멘트 헤드 때문으로 읽힌다)
- AIMD: NVT · **dt 2 fs** · CSVR
- ⛔ **미기재**: AIMD 의 k-점 · 길이 · 프레임 수·간격 · SCF 수렴 · DFT+U (해당 없음) · 이량체 배열의 수와 범위
- 학습셋 (`Table S1`, 14 줄):

| 계 | 형태 | 원자 | T (K) |
|---|---|---:|---|
| Li₆PS₅Cl | bulk | 104 | 2000, 5000 |
| Li₆PS₅Cl | bulk | 52 | 500 |
| Li | bulk | 90 | 2000, 5000 |
| Li | bulk | 54 | 500 |
| LiCl | bulk | 216 | 2000 |
| LiP | bulk | 64 | 2000 |
| Li₃P | bulk | 64 | 2000 |
| Li₂S | bulk | 324 | 2000 |
| Li₆PS₅Cl(010)/vacuum | surface | 78 | 500 |
| Li₆PS₅Cl(111)/vacuum | surface | 156 | 500 |
| Li(100)/vacuum | surface | 90 | 500 |
| Li(111)/vacuum | surface | 108 | 500 |
| Li₆PS₅Cl(010)/Li(100) | interface | 210 | 500 |
| Li₆PS₅Cl(111)/Li(100) | interface | 252 | 500 |

+ 짧은 거리 **이량체(dimer)** 배열 (강한 반발 영역 · *"reduces the likelihood of unphysical atomic overlap or collapse"*).
> 🔑 **설계 특징**: 반응 산물 (LiCl · LiP · Li₃P · Li₂S) 을 **2000 K 벌크** 로만 넣었고, 계면은 **500 K 두 조합**뿐이다. 프로덕션에서 대부분을 차지하는 **Li 과잉 비정질 혼합 영역**과 **장 구동 배열**은 학습에도 검증에도 직접 없다.

### 4-2 MLIP — CHGNet 미세조정 (SI §I · `Fig. S1`)
- 사전학습 **CHGNet** (Deng 2023 *Nat. Mach. Intell.*, ref 43) → 위 배열로 fine-tune · 프로덕션 전부 이 모델.
- 검증: 학습에 안 쓴 Li/LPSCl 배열 **4 세트** — (010)/Li(100) **350·500 K** · (010)/Li(111) **350·500 K**.

| 세트 | E RMSE (eV/atom) | F RMSE (eV Å⁻¹) |
|---|---|---|
| (a) (010)/Li(100) 350 K | 4.6 × 10⁻⁴ | 6.7 × 10⁻² |
| (b) (010)/Li(100) 500 K | 3.7 × 10⁻⁴ | 6.7 × 10⁻² |
| (c) (010)/Li(111) 350 K | 3.8 × 10⁻⁴ | 6.5 × 10⁻² |
| (d) (010)/Li(111) 500 K | 3.3 × 10⁻⁴ | 6.5 × 10⁻² |

- 그림 실독: 힘 분포는 대부분 ±2.5 eV Å⁻¹ 안. **(b) 에 대각선 아래로 휜 꼬리** (AIMD 0 ~ +0.8 → CHGNet −0.5 ~ −1.3 eV Å⁻¹, figure-read ≈) 가 보인다 — 본문 미논의.
- ⛔ **미기재**: CHGNet 버전 · 학습률·epoch·손실 가중 · train/val 개수 · 응력 · 자기모멘트 처리 · **반응 뒤 배열에 대한 DFT 단일점 대조** (kim2026 은 1 ns MD → 20 ps 간격 스냅샷 → DFT 단일점으로 했다). 본문이 *"described in the Supporting Information"* 라 한 **미세조정 절차 세부는 SI 에 없다** (§15).

### 4-3 MD (§IV B)
- LAMMPS · **dt 1 fs** · **CSVR** 425 K (결합 상수 평형 10 fs / 생산 50 fs) · **COM 병진 10 fs 마다 제거** · 3D 주기 + 진공 15 Å · **바로스탯 없음 · NVT**.
- 셀 **23.81 × 17.02 × 140.38 Å · 2,524 원자** · Li 금속·LPSCl 슬랩 각 ≥ 50 Å.
- 장 없음: 15 ps 평형 뒤 ~1 ns 분석. 장 구동: **같은 반응 전 초기 배열**에서 시작 (`Fig. 5b` 의 τ 가 0 에서 출발).
- **시드: 조건마다 궤적 1 개.** 그림의 음영 띠 (`Fig. 3e,f` · `Fig. 5b` · `Fig. S5b,e`) 가 무엇인지 설명 없음.
- 면 방향 비교 (SI §III): 4 조합 × 275/325/375/425 K · ≥ 200 ps.
- 벌크 기준 D (0.031 Å² ps⁻¹) 는 *"a separate AIMD calculation"* — **온도·셀·길이 미기재**.

### 4-4 장 + 동적 전하 (§II B · §IV C)
- **F_i = q_i E** — LAMMPS `efield` · E = **+0.1 V Å⁻¹** (0–350 ps) → **−0.1 V Å⁻¹** (350–700 ps) · 표면 법선 방향 · +z = Li 금속 → SE.
- **q_i = GFN1-xTB 단일점 원자전하** (CP2K · Ewald · 할로겐 결합 보정 켬 · OT + DIIS · inner/outer SCF 각 50 회 · 수렴 10⁻³) · **1 ps 마다** 갱신, 사이에는 고정.
- 왜: Li 는 금속(≈ 0) ↔ SE(양) 를 오가며 전하가 바뀌므로 고정 전하면 장의 힘을 잘못 준다.
- 전하 그림 실독 (`Fig. 4c,d`, figure-read ≈): 금속 Li ≈ 0 · LPSCl 의 Li ≈ +0.8 ~ +1 · 반응 영역 Li ≈ +0.4 ~ +0.8 · P: 초기 소폭 양 (≈ +0.2 ~ +0.4) → **100 ps 에 ≈ −1.5 ~ −2** (인화물 쪽) → 350·450 ps 진한·옅은 혼재 → **700 ps 에는 옅은 쪽 (≈ −0.5 ~ −1) 이 많다** — 이 변화는 본문이 논하지 않는다.
- ✎ **장 크기 감각 (우리 산수)**: SE 슬랩 ~60 Å 에 ≈ **6 V** · 홉 하나 (≈ 2.8 Å) 에서 Li (q ≈ +0.5e 로 가정 · 위 figure-read 범위 안) 가 받는 일 ≈ **0.14 eV ≈ 3.8 kT** (425 K) → **선형응답 밖**이다 (선형이려면 qEa ≪ kT). 전류밀도 1.65 × 10⁶ A cm⁻² = 실셀 1 mA cm⁻² 의 **~10⁹ 배**.
- ⚠ 장은 **원자 부분전하에만** 힘을 준다. CHGNet 에너지 자체는 장을 모른다 (전자 분극·차폐 없음).

### 4-5 조성 분류 (§IV D) — 'Li₂S-like' 의 정확한 정의
1. **P**: P–S < **2.70 Å** 인 S 이웃이 **≥ 2** 면 *argyrodite-like*. 나머지 = 환원 P → P–P < **2.60 Å** 가 있으면 *LiP-like*, 없으면 *Li₃P-like*.
2. **S**: 남은 argyrodite-like P 로부터 **4.50 Å 밖**이면 *Li₂S-like*. **Cl**: **4.90 Å 밖**이면 *LiCl-like*.
3. **Li**: 결정 RDF 첫 극소 컷오프 (Li–S **3.58** · Li–P **3.60** (Li₃P) / **3.15** (LiP) · Li–Cl **3.46 Å**) · 여러 상에 걸리면 **d/r_cut 이 가장 작은 상** · 아무 데도 안 걸리면 *unclassified*. (금속 Li 판정 기준은 명시 없음.)
4. 본문: *"the Li assignments were used primarily to characterise the local environment, rather than to determine the overall phase composition. The populations of … P/S/Cl centres were therefore used to quantify the evolution of the decomposition products."* — ⚠ 그런데 `Fig. 3e`·`Fig. 5a` 의 *Composition (%)* 는 캡션상 **Li 중심 환경 분율** (금속 Li 칸이 있다) 이다 → 방법 서술과 그림이 어긋난다 (§10-11).

> 🔑 **✎ 'Li₂S-like S' = "온전한 PS₄ 근처가 아닌 S".** 그래서 ① 환원된 P 에 아직 붙어 있는 S (P–S 조각) 도, ② S–S 결합을 가진 S 도 Li₂S-like 로 분류된다 — **S²⁻ 인지 확인하지 않는다.** ③ argyrodite-like P 가 하나도 안 남으면 **모든 S 가 정의상 Li₂S-like** 가 된다 (→ §6-1 의 Φ_S = 1 해석).
> 결정 LPSCl 의 P(4b)–S(4d, 자유 S²⁻) 거리 √3a/4 ≈ 4.27 Å 이 4.50 Å 안이라, 반응 전 자유 S²⁻ 는 Li₂S-like 로 안 잡힌다 (✎ 우리 산수 · 컷오프가 그걸 노린 값으로 보인다). P(4b)–Cl(4a) 거리 a/2 ≈ 4.9 Å 는 Cl 컷오프 4.90 Å 와 거의 같아서, Li 유입으로 격자가 부푼 반응 전선에서는 Cl 이 일찍 LiCl-like 로 넘어갈 수 있다 (✎ 우리 산수 · 검증 안 함) — **컷오프 민감도 분석은 없다.**

### 4-6 τ_SEI — SEI 두께 정의 (§IV E)
비-Li 전해질 슬랩을 주기 경계에서 펼침 (가장 큰 빈 영역에서 자름) → **2 Å bin** → f_reacted(z) = N_reacted / N_P,S,Cl (LiCl-, Li₂S-, Li₃P-, LiP-like 중심) → **Gaussian σ = 1 bin** 평활 → Li 쪽 SE 가장자리에서 **f = 0.5 를 처음 지나는 위치**까지 (선형 보간) · 교차가 여럿이면 **전체 등가 반응 두께에 가장 가까운 교차** 선택.
> ⚠ 이 '여럿 중 하나 고르기' 규칙이 `Fig. 5b` 삽입의 **≈ 3 Å 계단** (√t ≈ 5.8, t ≈ 34 ps · figure-read ≈) 의 후보 원인이다 (§5-2).

### 4-7 연결망 (§II C · SI §IV–V)
- 노드: Li₂S-like **S** · Li₃P-like **P** · LiCl-like **Cl** — 세 그래프 따로.
- 간선: 노드 간 거리 < 컷오프 (결정 425 K g(r) 첫 극소 · `Fig. S4`): **S–S 4.4 · P–P 5.0 · Cl–Cl 4.2 Å**.
- 클러스터 = 연결 성분 · **S_max** = 최대 클러스터 원자수 · **Φ_i = S_max / N_i** (N_i = 계 전체의 i 원자 수 — 반응 안 한 것 포함 → Φ 는 *변환율 × 연결성* 이 섞인 양 · 저자 명시).
- S_max(t) = B t^α + S₀ (`Eq. 8`) · JMAK Φ_S = 1 − exp(−k_A tⁿ) → ln[−ln(1 − Φ_S)] = n ln t + ln k_A (`Eq. 9`–`10`) · 장 없음은 시간 오프셋 t₀ 를 넣은 `Eq. S1`.
- ⛔ **없는 것**: 무작위 표지 대조 (null model) · 계면상 두께를 **관통(spanning)** 하는지의 검사 · Li 가 실제로 어느 음이온 환경을 따라 뛰는지 (경로 분해).

### 4-8 DOS (§IV F · `Fig. 7`)
- VASP **PBEsol** · 520 eV · spin · **z 쌍극 보정** · 장 없음 궤적 **마지막 프레임**에서 **5 Å 슬랩 두 장** (i · ii) 을 잘라 **진공 12 Å** · SCF → 빈 띠를 더한 NSCF · **Gaussian 0.05 eV** · 슬랩 **Γ** / 벌크 Li **5×5×5** / 벌크 LPSCl **6×6×6** · 10⁻⁶ eV · 원자 중심 구 사영 PDOS (분해능 ≈ 13 meV) · **spin-up 만** · **원자 수로 정규화 안 함** (패널끼리 세기 비교 금지 — 저자 명시).
- 기준 벌크: **Li₂₅₀** · **Li₂₄P₄S₂₀Cl₄**.
- ⛔ **미기재**: 잘라낸 슬랩의 이완 여부 (안 한 것으로 읽힌다 — *"cut from the last frame"*) · 벌크 LPSCl 의 S/Cl 자리 배치 · DOS 계산의 D3 여부.

### 4-9 무질서 처리 · 통계
- LPSCl 의 S/Cl (4a/4d) 자리 배치·무질서: **0 줄** (ref 46 Xie 2024 의 (010) 슬랩을 썼다는 말뿐 → 정렬 배치로 추정).
- 속도·배치 시드 반복: **0** — 모든 주장이 **조건당 궤적 1 개** 위에 있다.

---

## 5. 결과 — 절별 상세 (그림 실독 포함)

### 5-1 장 없음 — 계면이 스스로 자란다 (§II A · `Fig. 1`–`Fig. 3`)

**구조 (`Fig. 1`)**. `Fig. 1a` 는 반응 전: bcc Li (위) ‖ 결정 LPSCl (아래). `Fig. 1b` (~1 ns) 는 Li 금속 층이 얇아지고 (전체 스택 윗면이 아래로 내려옴 · Li 가 SE 로 들어감), 그 아래 넓은 무질서 영역이 생겼다. 저자는 이것을 *"chemically reacted interphase rather than a sharp Li/solid-electrolyte boundary"* 로 부르고, 이후 **interface = Li|LPSCl 경계 · interphase = 그 위에 생긴 Li₂S-rich 반응층** 으로 구분한다.
`Fig. 1c` (마지막 50 ps 평균 z 밀도): **Li 금속 z ≈ 22–50 Å** — 층 진동 피크 figure-read ≈ 0.08–0.09 Å⁻³ · **온전한 LPSCl z ≈ 115–130 Å** (S 밀도 진동이 강함) · 그 사이 **넓은 전이 영역** (Li ≈ 0.035–0.045 · S ≈ 0.01–0.02 Å⁻³, figure-read ≈ → Li : S ≈ 2.5–3). 반응은 한 원자층이 아니라 **수 nm** 로 SE 안쪽까지 간다.
`Fig. 1d` (계면상 중심 **60–85 Å** 의 in-plane Li–Li g(r), 50 ps 창): 첫 봉우리 **≈ 2.8 Å**, 둘째 **≈ 4.5 Å**. figure-read ≈ 0.00 ns 창만 첫 봉우리가 낮고 (≈ 1.9) 넓으며 0.07 · 0.50 · 1.00 ns 는 ≈ 2.1 로 거의 겹친다 — 본문도 *"positions … vary only modestly"* 라 쓴다. 근거로서는 약한 패널이다.

**Li 동역학 (`Fig. 2`)**. `Fig. 2a` in-plane MSD (50 ps 창 4 개): 0.00 ns 창은 **≈ 10 ps 에 20 Å²** 에 닿는다 (✎ 기울기/4 ≈ **0.5 Å² ps⁻¹** — `Fig. 2b` 축 (최대 0.08) 밖이라 안 실린 것으로 보인다) · 0.07 ns ≈ 12.5 Å² · 0.50 ns ≈ 3 Å² · 1.00 ns ≈ 2 Å² @ 50 ps (figure-read ≈).
`Fig. 2b` D_xy 10 점 (figure-read ≈): ~90 ps **0.066** → 170 ps 0.023 → 250 ps 0.021 → 300·370 ps 0.019 → 440 ps 0.016 → 580 ps 0.013 → 900 ps 0.007 → 960 ps 0.005 → 1030 ps **0.009 Å² ps⁻¹** · 벌크 AIMD 선 **0.031**. **~200 ps 안에 벌크 아래로 떨어지고** 1 ns 내내 아래에 머문다. 1 ns 값은 벌크의 ≈ **1/3.4** (figure-read ≈).
`Fig. 2c` σ_xy^NE (`Eq. 3`, ρ·Ze²/kT·D): 1.31 → 0.47 → 0.41 → 0.38 → 0.38 → 0.33 → 0.27 → 0.16 → 0.11 → **0.19 S cm⁻¹** · 벌크 선 ≈ **0.35** (figure-read ≈).
> ✎ **σ/D 비로 ρ 역산 (우리 산수)**: 계면상 점들은 σ/D ≈ 20 (S cm⁻¹)/(Å² ps⁻¹) 로 일정 → ρ ≈ **0.046 Å⁻³** (= Li 금속 밀도 수준 · 영역 안 Li 전부를 담체로 셈) · 벌크 선은 σ/D ≈ 11.4 → ρ ≈ 0.026 Å⁻³ (= LPSCl 의 Li 밀도). 그래서 **D 는 벌크의 ≈ 1/3.4 인데 σ^NE 는 ≈ 1/2** 다 — 계면상이 Li 를 ~1.8 배 더 많이 담고 있어서다.
> 🔑 즉 이 MLIP 계면상은 **"Li 를 막는 층"이 아니다.** 425 K in-plane σ^NE 가 벌크 LPSCl 의 절반 수준이다 (§6-1 · §7-6 에서 kim2026 과 같은 차수).

**화학 (`Fig. 3a–e`)**. in-plane g(r) 를 425 K 결정과 겹쳐 보면 (`Fig. 3a–c`): Li–S 첫 봉우리 **≈ 2.4 Å** (결정 Li₂S 와 같은 자리 · 높이 figure-read ≈ 5.7 vs 결정 ≈ 7.8) · Li–Cl ≈ 2.4 Å (≈ 3.5 vs 결정 ≈ 5.5) · Li–P ≈ 2.5 Å (반응 뒤 ≈ 6.3–6.8 로 결정 Li₃P ≈ 5.7 보다 높다). **둘째 껍질 (Li₂S 4.65 · LiCl 4.35 · Li₃P 4.9 Å) 은 셋 다 없다** → 저자: *"sulfide-like, phosphide-like and chloride-like local coordination. However, this is not evidence of their separate crystalline domains or stoichiometries."*
`Fig. 3d` 환경 색칠 스냅샷: 위 Li 금속 (빨강) · 가운데 Li₂S-like (보라) 바탕에 Li₃P-like (주황) · LiCl-like (청록) · unclassified (회색) 가 섞임 · 아래 LPSCl (파랑). 금속 Li 의 바깥 (진공 쪽) 표면에 회색 Li 줄이 있다.
`Fig. 3e` (Li 중심 환경 분율): 본문 수치 §3. ⚠ 생산 시작 때 이미 Li₂S-like 20 % — *"the interfacial reaction is very fast during equilibration"*.

**성장 법칙 (`Fig. 3f`)**. τ_SEI 는 ≈ 25.5 → ≈ 55 Å (0 → 1000 ps) · 삽입 √t 직선 **R² = 0.992** · `Eq. 4` τ₀ = 24 Å · k_W^eq = 0.99 Å ps^−½. 저자: *"The absolute values are unlikely to match experiment. However, the linear relationship of τ_SEI with respect to √t suggests the kinetic mechanism of the SEI growth is a diffusion-limited process."*
> ✎ **우리 재독** (삽입 10 점 디지타이즈 · figure-read): √t 적합 R² **0.993** (논문 0.992 재현) · 자유지수 tⁿ 최적 **n ≈ 0.54** (0.50–0.60 이 ΔR² < 0.002) · ln t 적합 R² **0.970** (t > 0, 9 점) · 선형 t R² **0.928**. ⇒ **장 없음 √t 는 그림이 지지한다.** (`[Chaney24SEI]` 의 같은 계면 성장곡선은 우리 재독 n ≈ 0.8 로 √t 가 안 섰다 — §7-6.) 단 창이 ~50–1000 ps (1.3 decade) 이고 τ₀ 가 자유 변수다.
> ✎ √t 를 그대로 외삽하면 **1 s 에 ≈ 10⁶ Å = 0.1 mm** — 실측 계면상 (cryo-TEM ~12 nm · `papers/luo2022_cryotem_li_dendrite_sulfide_interphase.md`) 과 자릿수가 안 맞는다. MD 성장은 **실제 율속 과정 (전자 수송) 을 담지 않는다** — 저자도 *"electrons are not treated explicitly … does not test whether electron transport limits reduction"* 라 적는다.

### 5-2 장 구동 + 반전 (§II B · `Fig. 4`·`Fig. 5`·`Fig. S2`)

**`Fig. 4` (재크롭본 실독)** — 위 시간축: **E = +0.1 V Å⁻¹ (0–350 ps · 화살표 ↓ = Li 금속 → SE)** · **E = −0.1 V Å⁻¹ (350–700 ps · ↑)**. 패널 a 구조 · b 조성 · c Li 전하 · d P 전하, 각 0/100/350/450/700 ps.
- **0 ps**: Li 금속 (위) ‖ LPSCl (아래, b 에서 전부 파랑).
- **100 ps**: 위에 얇은 금속 Li 만 남고 **나머지 전부 보라 (Li₂S-like)** + 주황·청록 점 — 파랑 (LPSCl) **없음**. P 는 진한 갈색 (≈ −1.5 ~ −2).
- **350 ps**: 원래 금속 Li **사라짐** · 슬랩 **아래쪽 (진공에 면한 SE 자유표면)** 에 빨강 Li-rich 층 + 청록 (LiCl-like) 점 · 그 Li 는 c 에서 흰색 (≈ 0, 금속).
- **450 ps**: 아래 빨강 층이 얇아지고 위 표면에 회색 (unclassified) 줄.
- **700 ps**: **위쪽에 금속 Li 층 (빨강 · c 에서 흰색) 이 다시 생김** · 보라 영역은 그대로 · 아래쪽 보라에 **가로 줄무늬 (층상 정렬)** — 본문 *"Some local structural ordering develops within the reconstructed region"*.
> 🔑 **"Li 는 돌아왔고 LPSCl 은 안 돌아왔다"** 가 그림으로 그대로 보인다. ⚠ 그런데 Li 가 쌓인 '아래 경계' 는 **Li 상대전극이 아니라 진공에 면한 SE 표면**이다 — 전자를 공급할 집전체가 없는데 금속 Li 가 생기는 것은 MLIP 에서 Li 가 **전자를 데리고 움직이기 때문**이다 (§6-3).

**`Fig. S2` (장 구간 z 밀도, figure-read ≈)**: 50–100 ps 에는 z ≈ 25–45 Å 에 결정 Li 층 진동이 남아 있고 S 는 z ≈ 46–130 Å · 150–200 ps 에 금속 층 진동 소멸, Li 가 z ≈ 34–136 Å 로 퍼짐 · 250–300 ps 에 Li 가 **S 끝 (≈ 128 Å) 을 넘어 z ≈ 128–140 Å 까지** 쌓이고 (셀 끝에 닿음) 반응 영역 Li ≈ 0.045 · S ≈ 0.015 Å⁻³ (**Li : S ≈ 3**). 완전 환원 산물 5Li₂S + Li₃P + LiCl 의 Li : S = 14 : 5 = 2.8 과 맞는다 (✎).

**`Fig. 5a` (Li 중심 조성 · 확대 렌더 실독, figure-read ≈)**: LPSCl **34 % → 60 ps ≈ 9 % → ≈ 95 ps 0** (⚠ 본문 *"negligible within approximately the first 60 ps"* 보다 늦다) · 금속 Li 55.5 % → ≈ 4 % (≈ 180–200 ps) → ≈ 12 % (≈ 340 ps) → ≈ 4 % (≈ 430 ps) → ≈ 10 % (700 ps) · Li₂S-like 8 % → **≈ 66 % (110 ps) → 67–70 % 평탄 (반전 뒤에도)** · Li₃P-like ≈ 11–12 % (금속 Li 가 많을 때 살짝 내려감) · unclassified ≈ 9–10 % · LiCl-like ≈ 4–5 % · LiP-like ≈ 0.

**`Fig. 5b` (장 구간 τ_SEI)**: 0 → ≈ 82 Å (100 ps) · 0–45 ps 오목, 45 ps 뒤 거의 직선 + 끝에서 살짝 위로 (figure-read ≈) · 삽입 √t (t ≈ 10–80 ps) **R² 0.987** · k_W^ef = **6.77 Å ps^−½**. *"because the electrolyte slab is finite, SEI growth occurs only during the first 100 ps."*
> ✎ **우리 재독** (삽입 22 점 디지타이즈): √t R² **0.989** (기울기 6.97 vs 논문 6.77) · ln t **0.980** · 선형 t **0.960** · 자유지수 **0.2–0.5 가 ΔR² < 0.002 안에서 구별되지 않는다** (최적 ≈ 0.35). ⇒ **장 구간의 √t 는 데이터가 고르지 않는다** — 창이 1 decade 미만이고 슬랩이 ~100 ps 에 바닥난다. 게다가 √t ≈ 5.8 (t ≈ 34 ps) 에 **≈ 3 Å 계단**이 있다 (교차 선택 규칙 전환 후보 · §4-6).
> ✎ "nearly seven-fold" 는 **k_W 의 비** (6.8) 다. 같은 두께까지 걸리는 **시간 비**로는 (6.8)² ≈ **47 배**다.

**`Fig. 5c` (반전 구간 누적 N_Li · 450–700 ps)**: 0 → ≈ 105 개 · 직선 기울기 **0.419 ps⁻¹** (R² 0.9842). 어느 평면을 셌는지 (*"the selected plane"* · *"interface-normal plane"*) · 순(net) 인지 총(gross) 인지 · 왜 350–450 ps 를 뺐는지 **미기재**. `Eq. 5`–`6` → J = 1.034 × 10⁻³ ps⁻¹ Å⁻² · j = 1.65 × 10¹⁰ A m⁻² · σ_eff = |J|/|E| = **16.6 S m⁻¹ = 0.166 S cm⁻¹** (각 Li 가 전하 1e 를 나른다고 가정). 저자 단서 셋: NE 는 상관 무시 · 장 구동값은 선형응답 밖일 수 있음 · 방향 (xy vs z) 이 다름 → *"order-of-magnitude comparison"* 만.
> ✎ 비교 둘이 다른 것을 하나 더 보탠다: σ^NE 0.18 은 **LPSCl 이 13 % 남은 1 ns 장 없음 구조**, σ_eff 0.166 은 **LPSCl 이 0 % 인 완전 변환 구조** 의 값이고, 장의 힘은 **부분전하 q (< 1e)** 로 줬는데 전류는 **1e** 로 셌다. 두 수가 가까운 것은 우연에 가깝다.

### 5-3 연결망 — Li₂S-like 만 이어진다 (§II C · `Fig. 6` · `Fig. S4` · `Fig. S5`)
- `Fig. 6a` (시점 미기재 그래프 스냅샷): S 그래프는 반응 영역 전체를 채운 3D 망 (윗부분에 층상 정렬 줄무늬) · P·Cl 은 2–6 노드 조각과 고립점.
- `Fig. 6b` Φ (figure-read ≈): Φ_S **0.05 → 0.65 (50 ps) → 0.9 (90 ps) → 1.0 (≈ 105 ps)**, 이후 700 ps 까지 1 (반전선 350 ps 근처 작은 홈) · Φ_P, Φ_Cl ≈ 0.05–0.12, 반전 뒤 끝으로 갈수록 조금 오름.
- `Fig. 6c` S_max (log–log): S ≈ 30 (1 ps) → 플래토 **≈ 5.6×10²** (≥ 200 ps) · Phase 1 **α = 0.77** (≈ 1–12 ps) · t* ≈ 6 ps · Phase 2 **α = 0.49** (≈ 10–200 ps 선) · P/Cl S_max ≈ 2 → ~10–15.
- `Fig. 6d` JMAK: ln[−ln(1−Φ_S)] = −2.9 → +1.0 (ln t 0 → 4.6) · 적합 **n = 0.74**.
- 해석 (저자): `Eq. 7` (LPSCl + 8Li → 5Li₂S + Li₃P + LiCl) 의 **5 : 1 : 1** 이 망을 유리하게 하지만 *"composition alone does not determine connectivity"* · α ≈ 0.5 와 τ 의 √t 는 *"qualitative correspondence"* 만 · n 은 *"only to describe the kinetics"*.
- **장 없음 (SI §V · `Fig. S5`)**: 같은 배치 — Li₂S-like S 는 **처음부터 끝까지 클러스터 ≈ 1 개** (`Fig. S5e`) → Φ_S 상승 (0.29 → 0.65) 은 **합체가 아니라 변환** · Φ_P 0.05 → 0.11 (250 ps 뒤 일정) · Φ_Cl 0.03–0.06 · P·Cl 클러스터 **수**가 20 → 34 · 38 로 는다 → 새 Li₃P-·LiCl-like 는 **기존 것에 붙지 않고 새 작은 클러스터로** 생긴다 (조대화 제한) · S_max **α = 0.47** (≈ 150 → ≈ 300 원자, 2 배밖에 안 변함) · JMAK **n = 0.45 ± 0.02** (t₀ 맞춤 · R² 0.994).
- `Fig. S4` 컷오프 근거: 결정 Li₂S S–S 첫 봉우리 ≈ 3.95 Å → rc 4.4 · Li₃P P–P ≈ 4.25 Å → rc 5.0 · LiCl Cl–Cl ≈ 3.55 Å → rc 4.2 (figure-read ≈ 봉우리 위치) · 셋 다 첫·둘째 껍질 사이에서 g(r) = 0.

### 5-4 전자구조 — 반응 영역이 전자를 막나 (§II D · `Fig. 7`)
- `Fig. 7b` 벌크 Li₂₅₀: E_F 를 지나 연속 (≈ −3.6 eV 부터) — 금속.
- `Fig. 7e` 벌크 LPSCl: 점유 띠 위 **≈ 2 eV 갭** (본문). figure-read ≈ 가장 위 점유 봉우리 ≈ −0.3 eV, 첫 빈 상태 ≈ +1.8–1.9 eV 의 작은 혹 → ≈ 2 eV 와 맞다. ⚠ figure-read: 그 **맨 위 점유 봉우리가 Cl 색 (보라)** 으로 칠해져 있다 (S 는 아래 −1 eV 근처) — 우리 comp1 은 VBM = **S 3p** 다 (`../our_dft_baseline.md`). 자리 배치 미기재라 원인 판정 불가 · 본문 미논의.
- `Fig. 7c,d` 슬랩 i · ii: −5 ~ 0 eV 점유 띠가 **S 3p** · Cl 3s/P 는 더 깊은 곳 (−17 ~ −8.5 eV) · S 사영 DOS 가 띠 꼭대기에서 급락하고 총 DOS 가 바로 위에서 **뚜렷한 최소**.
- **전자 세기 논리 (이 절의 핵심)**: S²⁻ · Cl⁻ · P³⁻ 가 가장 환원된 상태이므로 음이온은 최대 **2N_S + 3N_P + N_Cl** 개 전자를 받는다 → 슬랩 i **88** vs Li 94 → **≥ 6 e⁻ 과잉** (P 산화수와 무관) → 과잉 전자가 S 띠 (끝 E − E_F ≈ −0.5 eV) **위**를 채운다 · 슬랩 ii **90** vs Li 85 → 모든 P 가 인화물이어도 **≤ 5 e⁻ 부족** → E_F 가 S 띠 꼭대기, 최소는 그 바로 위.
- 결론 (저자): E_F 의 상태는 *"accounted for by the Li content of each extracted slab, which depends on where the cut is made, rather than by intrinsically metallic sulfide-like environments"* · 황화물 영역 자체는 S 띠 위에 **갭 같은 최소** → Li₂S-like 망과 합쳐 *"compatible with … passivation"*. 단서: 최소는 *"not a clean gap"* (DOS 유한) · 자른 면·표본·무질서 탓일 수 있음 · **더 큰 모델이 필요**.
> ✎ 우리 확대 렌더 (`Fig. 7d`): 0 ~ +2 eV 사이 총 DOS 가 0 근처까지 내려갔다가 여러 뾰족 봉우리 (≈ +1 eV 등) 를 가진다 (figure-read ≈ 5–25 states/eV) — '갭 같은 최소' 는 맞지만 갭은 아니다.

### 5-5 SI — 면 방향 (`Table S2` · `Fig. S3`)
- 4 조합 모두 D_xy 가 T 와 함께 대체로 오르지만 **(111)/Li(100) 은 375 → 425 K 에 내려가고**, (111)/Li(111) 은 275 → 325 K 가 거의 평평하다. 425 K 범위 0.0207–0.0290 Å² ps⁻¹ (같은 자릿수).
- `Fig. S3` σ^NE (figure-read ≈): (010)/Li(100) 0.21 → 0.40 · (010)/Li(111) 0.27 → 0.57 · (111)/Li(100) 0.345 / 0.344 / 0.49 / 0.42 · (111)/Li(111) 0.37 / 0.33 / 0.355 / 0.48 S cm⁻¹.
- 결론 (저자): *"no single orientation consistently produces either the highest or lowest Li mobility"* → (010)/Li(100) 을 대표로 선택.
- ⚠ 275 K 에서 0.2–0.37 S cm⁻¹ 는 어떤 실측 계면보다 수 자릿수 크다 — 이 '계면 in-plane σ' 는 금속 Li 에 가까운 Li 과잉 영역·반응 재배열이 섞인 양이다 (§7-5 홉 수 검산).

---

## 6. 주장 vs 근거 강도 ★★

### 6-1 'irreversibly percolating Li₂S' — 무엇으로 보였나

| 성분 | 근거 | 강도 | 빠진 것 |
|---|---|---|---|
| **Li₂S** | Li–S 첫 g(r) 봉우리 자리 (`Fig. 3a`) · 'S 가 온전한 PS₄ 에서 4.50 Å 밖' 분류 | **약** — 저자 스스로 결정상 아님 · 분류는 S²⁻ 를 확인 안 함 · 둘째 껍질 없음 | 결정성 판정 · S–S 결합 유무 · S 전하 |
| **percolating** | Φ_S → 1 · S 클러스터 1 개 (`Fig. 6b` · `Fig. S5e`) | **정의상 거의 확정** — 장 구간의 Φ_S = 1 (≈ 105 ps) 은 LPSCl 소멸 (≈ 95 ps) 과 같은 사건이다: argyrodite-like P 가 없으면 **모든 S 가 Li₂S-like** 이고, 조밀한 음이온 격자에서 4.4 Å 컷오프면 서로 이어진다 | **무작위 표지 대조** — ✎ 반응 영역 음이온의 S 분율 5/7 ≈ **0.71** 은 fcc 자리 퍼콜레이션 문턱 ≈ **0.20** 을 크게 넘고, P·Cl 각 1/7 ≈ **0.14** 는 그 아래다 → **무작위로 섞여도 S 는 이어지고 P·Cl 은 고립된다** (우리 산수 · 반응 영역을 fcc 음이온 격자로 근사한 기준) |
| **irreversibly** | 반전 350 ps 동안 Φ_S = 1 · LPSCl 0 % · Li₂S-like 67–70 % 유지 (`Fig. 5a` · `Fig. 6b`) | **관측은 확실, 의미는 제한적** — 닫힌 계 · 전자 저장소 없음 · 반전 장이 왕복시키는 것은 환원에 쓰고 남은 Li 뿐 (§6-3) · 350 ps · 425 K 관측창 ≈ 0.30–0.47 eV (§7-5) | 산화 쪽 구동력 (전위) 이 있는 대조 · 더 긴 시간 · 시드 |
| **Li 가 그 망을 지난다** | *"any continuous path through the interphase must pass through it"* (결론) | **논리 (기하)** 지 수송 측정이 아니다 | Li 홉을 이웃 음이온 환경별로 나눈 통계 · 망을 끊었을 때의 수송 대조 |

### 6-2 'reversible ion transport' — 무엇으로 보였나

| 성분 | 근거 | 강도 | 빠진 것 |
|---|---|---|---|
| 방향이 뒤집힌다 | `Fig. 4` 450·700 ps 스냅샷 · `Fig. 5a` 금속 Li 분율 · `Fig. 5c` 누적 N_Li 직선 | **확실** — F = qE 를 뒤집었으니 표류도 뒤집힌다 (자명에 가깝다) | 350–450 ps 구간의 유속 시계열 (*"almost immediately"* 는 정량으로 안 보임) |
| 'ion' transport | 부분전하 q 를 가진 원자의 표류 | **약** — Li 는 이온이 아니라 **전자를 데리고 다니는 원자** (§6-3) · 외부회로 없음 | 전자 경로를 따로 다루는 모델 (상수 전위 · 명시적 전자) |
| 계면상이 이온을 통과시킨다 | σ_eff 0.166 S cm⁻¹ | **장 세기에 종속** — qEa ≈ 3.8 kT (✎) · 전류 ~10⁹ 배 · 장 크기 한 점 | 장 크기 사다리 (0.01–0.1 V Å⁻¹) · 선형 구간 확인 |

### 6-3 두 주장이 동시에 성립하는 논리 — 쉬운 말로
1. **Li 는 원자째 움직인다.** MLIP 는 "전자가 항상 그 원자 배치의 바닥 상태에 있다" 고 본다. 그래서 Li 원자 하나가 SE 안으로 들어가면 **Li 하나 + 전자 하나 (= Li⁰)** 가 들어간 것과 같고, SE 는 그만큼 **화학적으로 환원**된다. 실제 전지에서는 Li⁺ 만 SE 로 가고 전자는 외부회로로 간다 — 그래서 실제 계면에서는 전자가 SEI 를 못 지나가면 환원이 멈춘다 (부동태화). **이 MD 에는 그 제동이 없다.**
2. **환원 산물은 Li 를 꽉 쥔다.** ✎ (우리 산수) LPSCl ≈ 100–110 f.u. 를 다 환원하려면 f.u. 당 Li 8 개 → **≈ 820–900 Li** 가 산물 (Li₂S·Li₃P·LiCl) 안으로 들어간다. Li 금속은 ≈ 1.1–1.2k 개이므로 남는 **'여분 Li' ≈ 170–360 개** (Li 전체의 ≈ 10–20 %) — 반전 뒤 `Fig. 5a` 의 금속 Li ≈ 10 % + unclassified ≈ 9 % (figure-read ≈) 와 같은 크기다.
3. **장을 뒤집으면 여분 Li 만 왕복한다.** `Fig. 5c` 의 105 개는 여분 Li 의 ≈ 30–60 % 다. 산물 안의 Li 는 그대로 있다 → 산물에서 전자를 빼낼 곳 (산화제·전위) 이 계에 없으므로 **P³⁻ 가 P⁵⁺ 로, S²⁻ 가 PS₄ 로 돌아갈 길이 원래 없다.**
4. **열역학도 같은 말을 한다.** 산물을 다시 LPSCl 로 묶으려면 계면 전위가 **LPSCl 환원 가장자리 (우리 hull ≈ 1.72 V vs Li⁺/Li)** 위로 올라가야 한다. 스트리핑 중 Li 음극은 0 V 근처에 머문다 (§7-2).
⇒ **"Li 는 오가고 계면상은 안 돌아온다"** 는 놀라운 결과라기보다 **닫힌 계 + Li⁰ 수송 + 0 V 근처 열역학의 귀결**이다. 이 논문의 진짜 새 내용은 ① 장이 성장을 얼마나 당기나 (k_W ≈ 7배) ② 산물의 **연결 위상** (Li₂S-like 망 · 흩어진 P/Cl) ③ 잘라낸 슬랩의 **전자 세기 규칙** 이다. 그리고 ② 는 무작위 혼합 기준과 구별되지 않았다 (§6-1).

### 6-4 저자가 보이지 않은 것 (요약)
- 반응 뒤 배열에 대한 MLIP 검증 · 시드 반복 · 장 크기 의존성 · 425 K 밖의 성장·장 런 (SI 의 '다른 온도' 는 `Table S2` 의 D 뿐) · 계면 수직 (z) 방향 장 없음 수송 · Li 경로의 환경 분해 · 퍼콜레이션 무작위 대조 · 저항·임피던스 계산 (결론의 *"resistance … set early"* 는 외삽) · 전자 수송 (DOS 는 5 Å 잘라낸 슬랩 두 장).

---

## 7. 우리와의 대조 ★★ (트랙별)

### 7-1 SEI NEB 트랙 (1저자 = 사용자) — Li₂S V_Li⁻ c→c CI-NEB 셀 수렴 · Li₃Nd

우리 기록: 카드 `db/properties/li2s_neb_cellconv_estimand_2026_10_09.json` (2×2×2 대조 기록 · proposed) · 판정 카드 `db/properties/li2s_cellconv_card_2026_09_01.json` (C1 |Ea(4×4×4) − Ea(3×3×3)| ≤ 30 meV · C2 · C3 · 4×4×4 메모리 실측 45.15 GB → gabia 단독 + 손잡이 재프로브) · 기준값은 `db/properties/sei_neb.json` v2/li2s — ⛔ **값을 여기 옮기지 않는다** (scientific_status provisional_single_cell · cell_convergence_status untested · **citable=false** · `HZ-sei-neb-retracted` **BLOCKED** · `forbidden_statement`: *"실험·문헌 값과 나란히 놓는 것"* 금지).

| 칸 | 우리 SEI NEB 보고량 | 이 논문 | 대응? |
|---|---|---|---|
| 물질 | **결정** antifluorite Li₂S (Fm-3m, mp-1153) · 화학량론 + V_Li⁻ 1 개 | 'Li₂S-like' = PS₄ 에서 떨어진 S 를 가진 **비정질 Li 과잉 혼합 영역** (Li : S ≈ 3 · Li₃P-·LiCl-like 클러스터 포함) | ✗ 다른 물질 |
| 온도 · 시간 | 0 K · 정적 | 425 K · ns | ✗ |
| 양 | 최근접 8c→8c **단일 홉 이동 장벽** (jellium · 담체 생성 제외) | in-plane **D_xy** (50 ps 창) · **σ^NE** · 장 구동 **σ_eff** | ✗ 다른 양 |
| 담체 | 하전 공공 1 개 (농도는 카드 밖 — *"공공 형성에너지 … 이 카드 밖"*) | 과잉 Li + 무질서 — 담체 농도가 제한 요인이 아니다 | ✗ |
| 장벽 | 있음 (비인용) | **없음 (논문 0 회)** — `Table S2` 기울기는 장벽이 아님 (§7-5 ①) | — |
| 셀 수렴 | 3×3×3 → 4×4×4 판정 대기 | 셀 크기 의존성 시험 없음 (2,524 원자 1 개) | — |

**연결되는 지점 (정성)**
1. **단계가 다르다.** 이 논문은 결정화 **전**의 Li 과잉 비정질 단계 (1 ns · 425 K) 를 본다. 결정 Li₂S 가 생기는 것은 같은 계면의 더 긴 MLIP (`[Chaney24SEI]` 결정화 · `kim2026` ~11 ns 핵생성) 과 실측 (`luo2022` 25 °C 단결정 Li₂S ~12 nm) 쪽이다. **우리 장벽은 결정화 뒤 SEI 의 미시 재료**다. 원고에 Li₂S 장벽을 쓸 때 *"crystalline Li₂S (post-crystallisation SEI)"* 로 단계를 적으면 이 논문과 충돌하지 않는다.
2. **이 논문의 '모든 Li 경로가 Li₂S-like 망을 지난다' 는 결정화 뒤에 우리 양을 중요하게 만드는 논거**다. 단 그때 계면 수송은 *[담체 농도] × exp(−E_m/kT)* 이고, 우리 카드는 앞 항을 명시적으로 뺐다 — 우리 장벽만으로 SEI 저항을 말할 수 없다는 것은 그대로다.
3. **MLIP 비정질 단계의 Li 이동도는 결정 Li₂S 와 수 자릿수 다르다.** 이 논문 계면상 σ^NE ≈ 0.18 S cm⁻¹ (425 K) vs 결정 Li₂S σ_RT figure-read ≈ 8 × 10⁻⁹ S cm⁻¹ (`papers/wu2026_asslsb_li2s_reaction_mechanisms_engineering_review.md` `Fig. 5a` · 2차 인용 · 온도도 다름). ⇒ 이 논문 수치로 우리 장벽의 타당성을 판정하지 않는다 (어느 방향으로도).
4. **Li₃Nd**: 이 논문에 Nd 는 없다 → **직접 대응 없음.** 다만 질문틀 하나를 빌릴 수 있다 — *"금속성 소수 산물 (Li₃Nd · class metal) 이 계면에서 연결망을 이루는가"*. 무작위 혼합 기준으로 소수 산물 (분율 < ~0.2) 은 고립되므로, Li₃Nd 가 전자 누설 경로가 되려면 **편석·연결**이 필요하다 (✎ 우리 추론 · 계산 없음).
5. **바꿀 것 없음**: 4×4×4 판정 (09-01 카드 C1–C3) · gabia 단독 + 메모리 재프로브 순서는 이 논문 때문에 바뀌지 않는다.

### 7-2 ESW · 분해 계면 (1저자 = 사용자)

1. **반응식 방향 — 우리 음극 게이트와 같은 쪽.** `Eq. 7` Li₆PS₅Cl + 8Li → 5Li₂S + Li₃P + LiCl 은 우리 `HZ-anode-b2o3-reaction-direction` (**BLOCKED**) 의 재실행 수용 게이트 두 줄 — ① 0 V 행의 **Li 계수가 양수 (흡수)** ② **원소 S 없음 · Li₂S 있음** — 을 둘 다 통과하는 꼴이다. MD 도 같은 방향을 보인다: 금속 Li 소모 (`Fig. 3e` 45 → 27 %) · Li₂S-like 주산물 · P 전하가 강한 음 (인화물 쪽, `Fig. 4d` figure-read).
   ⚠ 단서 셋: (가) `Eq. 7` 은 **유도가 아니라 ref 38 (Aktekin 2023) 인용**이다. (나) 이 논문의 분류는 S²⁻ 를 확인하지 않아 **'원소 S 없음' 의 독립 확인이 못 된다** (§4-5). (다) 그래서 그 원장이 말하는 '독립 줄기 둘' (Wenzel 2018 XPS · Chaney 2024 MLIP) 옆에 **'세 번째 독립 확인' 으로 세지 않는다** — 같은 방향을 보여 주는 **MLIP 동역학 그림 하나 (프리프린트)** 를 곁들일 수 있는 정도다 (Li 금속 소모 · P 전하 음 · Li₂S-like 주산물). ⛔ 이 편이 우리 `anode_interface_b2o3.json` 의 반응식 문자열을 고쳐 주지 않는다 (도구에 `evolution` 부호 기록 + 재실행이 여전히 수정 경로).
2. **'비가역' 은 우리 hull 이 이미 말한다.** 우리 comp1 (MP2020 · GG 상 제외) 의 **Li 교환-0 아래 가장자리 1.717 V** (`ocv_self_decomposition_V` · grand-potential 경계 · `[Zhu15]`·`[Schw21]` 1.72 V 와 0.003 V 차 · `HZ-esw-reduction-limit-label` CONDITIONAL — 값 자체는 금지 밖, *'환원 한계' 라벨·폭 인쇄값* 이 걸린다) 아래에서 LPSCl 은 환원 산물로 간다. 산물을 다시 LPSCl 로 묶으려면 계면이 그 위로 올라가야 하는데 **Li 금속 음극은 스트리핑 중에도 0 V 근처**다 ⇒ 이 논문의 *"argyrodite coordination does not recover"* 는 **열역학적으로 기대되는 결과**이고, MD 는 원래 그걸 시험할 수 없다 (전위 제어 · 전자 저장소 없음). 새 정보는 '안 돌아온다' 가 아니라 **'얼마나 빨리 가나 (k_W) · 어떤 위상으로 가나'** 다.
3. **산화 쪽 연결 (E2b 기록)**: `db/properties/esw_e2b_li2s_correction_2026_10_03.json` — 우리 hull 의 **산화 onset 2.256 V = Li₂S → S + 2Li** (보정·상 제외 네 칸 모두 Li₂S = comp1 = modelc onset · 축 ① S-limited). 이 논문의 Li₂S-like 망이 다시 산화될 전위는 그 쪽인데 음극은 거기에 가지 않는다 → 음극 SEI 의 Li₂S 는 정상 운전 전 구간에서 안정 쪽이다 (✎ 우리 연결 · 이 논문은 산화를 다루지 않는다). ⛔ 그 기록의 '보정끔' 진단값은 절대 전압으로 인용 금지.
4. **산물 전자구조 — 우리 음극 판정축에 주는 것.**
   - (가) `HZ-anode-b2o3-reaction-direction` 의 두 번째 ⚠ — `min_product_gap_eV` (순수 Li₃P 상의 MP 갭) 는 **"상분리 가정 하의 값"** 이다. 이 논문은 Li₃P-like 가 **~10 원자 클러스터로 흩어져 연결되지 않는다**고 본다 (`[Chaney24SEI]` 의 antifluorite 단일 고용체 그림과 같은 방향). ⇒ "Li₃P 가 작은 갭이라 전자가 샌다" 는 판정은 **상분리 + 연결** 두 가정 위에 서고, 이 논문은 둘 다 부정하는 쪽의 (MLIP · 전자 없음) 증거다.
   - (나) 반대로 **금속 쪽에 가까운 Li 과잉 영역 (슬랩 i, +6 e⁻) 은 E_F 에 상태가 있다** — 전자 누설은 Li₃P 보다 **과리튬화 영역**에서 올 수 있다. 우리 산물 갭 판정 (`db/properties/sei_electronic_class.json` 계열) 은 화학량론 상만 보므로 이것을 못 본다.
   - (다) ✎ **싼 사전 선별 규칙**: 잘라낸 영역의 **N_Li − (2N_S + 3N_P + N_Cl)** > 0 이면 과잉 전자 → 금속성 의심. 이 논문이 쓴 산수 그대로이고, 우리 계면 구조 (Nd 계면 · SEI 슬랩) 에 DFT 전에 걸 수 있다 (Nd·B·O 가 있으면 산화수 항을 더한다).
5. **갭 비교**: 이 논문 벌크 LPSCl **≈ 2 eV** (PBEsol · DOS 판독 · Gaussian 0.05 eV) vs 우리 comp1 **2.066 eV** (canonical · PBE fixed-occ nscf VBM/CBM 고유값). 범함수·판독법이 달라 **"둘 다 wide-gap" 이상으로 해석하지 않는다** (우리 규율: DOS 문턱 판독 금지 · 절대 비교 금지).

### 7-3 li2s 트랙 (외부 1저자 · 사용자 ≠ 1저자) — 같은 계가 아니다
- **계가 다르다.** 이 논문 = **Li 금속 음극 ‖ LPSCl** 의 **환원** 계면상 (P⁵⁺ → P³⁻ · Li 과잉 · 금속 Li 근처는 금속성). li2s 트랙 = **Li–S 양극 볼밀 LPSCl@Li₂S** 복합체 (`db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json` · host comp1 · Li₂S : LPSCl = 3 : 5 wt) — Li 금속도 환원도 없고, 질문은 *"bulk Li₂S 보다 Li 이동도가 높은 계면상이 생기나"* 다. **'Li₂S' 라는 낱말 말고는 화학이 다르다.**
- **닿는 것 (잠정 · 외부 1저자 판단 필요)**:
  1. ⛔ *"비정질 Li₂S-like 영역은 빠르다"* 로 읽고 li2s 가설의 지지로 쓰지 않는다 — 이 논문의 빠른 영역은 **Li 과잉 (담체 과다 · 일부 금속성) + 인화물** 이고 425 K · 시드 1 이다. 볼밀 복합체 계면 (Li 과잉 없음) 과 다른 물질이다.
  2. `wu2026` digest 의 **경쟁 기전 S3 "Li₂S–LiX 고용체"** (Cl 이 Li₂S 쪽으로 들어가 σ↑) 와 모양은 닮았다 — 이 논문의 Li₂S-like 망 안에 흩어진 LiCl-like 클러스터 = Cl 이 Li₂S 형 바탕에 녹아든 그림. 그러나 **환원·Li 과잉 조건**이라 양극 복합체의 근거가 아니다.
  3. **빌릴 수 있는 분석 방법**: 음이온 그래프 + 결정 RDF 첫 극소 컷오프 (`Fig. S4` 식) · Li 중심 환경 분류 (d/r_cut 동점 처리) · Φ = S_max/N — **반드시 무작위 표지 대조와 같이**. 사용 여부는 외부 1저자 몫.
- ⛔ li2s 트랙의 수송 계수·Ea 는 이 digest 어디에도 싣지 않았다 · 소셀 유리 캠페인은 2026-09-30 마감 (수송 미보고) · v2 카드 proposed — 이 논문은 그 어느 것도 재개·판정하는 근거가 아니다.

### 7-4 우리 MD/DFT 규약과 나란히 (판정 아님)

| 항목 | 이 논문 | 우리 (modelc/lpsocl 벌크 MD · DFT 기준선) |
|---|---|---|
| MLIP | CHGNet 사전학습 + 계면 fine-tune (PBEsol+D3 라벨) | UMA-s-1p1 (omat) 범용 · fine-tune 0 |
| 앙상블 · 열욕 | NVT · CSVR 50 fs · COM 10 fs 제거 | NVT · Langevin friction 0.02 |
| dt | 1 fs | 2 fs |
| 온도 | 425 K (계면) · 275–425 K (SI D) | 600 / 800 / 1000 K |
| 길이 · 크기 | ~1 ns · 0.7 ns · 2,524 원자 | 생산 200 ps (box331 400 ps) · 558 원자 |
| MSD | in-plane · 50 ps 창 · '선형 구간' (구간 미기재) | 2–50 ps 고정 · 자유절편 |
| σ | NE (Haven 1) · ρ = 영역 안 Li 전부 | NE (Haven 1) · ⛔ 절대값 인용 금지 · Ea 도 계 간 상대차만 |
| 시드 | 조건당 1 | 멀티시드 (비율은 멀티시드 판정만) |
| 반응 · 계면 | 허용 · Li 금속 계면 | 조성 고정 벌크 |
| 장 | ±0.1 V Å⁻¹ · 동적 전하 | 없음 |
| DFT | PBEsol · 520 eV · D3 · PAW | PBE · QE (ecut·PP 는 계별) |
| 갭 판독 | DOS (Gaussian 0.05 eV) | fixed-occ nscf 고유값만 |

### 7-5 CLAUDE.md 데이터 규율 3종 — 이 논문에 적용
**① 장벽 → 홉 수 검산 (`D-2026-09-27-barrier-hop-count`)**: 논문은 **Ea 를 하나도 보고하지 않는다 → 직접 해당 없음.** 다만 `Table S2` 를 누가 아레니우스로 읽을 수 있어 미리 잰다 — ✎ (우리 산수 · **논문 미보고 도출값**) 1/kT 기울기: (010)/Li(100) **0.073 ± 0.004 eV** (R² 0.994) · (010)/Li(111) 0.078 ± 0.010 · (111)/Li(100) 0.049 ± 0.013 · (111)/Li(111) 0.043 ± 0.016 eV.
홉 수 검산 (ν₀ 1e+13 s⁻¹ 가정 · 425 K): Γ ≈ 1.36e+12 s⁻¹ · 평균 대기 ≈ 7.34e-13 s (Ea 0.073 eV) → 모든 Li 가 그 속도로 2.8 Å 씩 뛰면 D_xy ≈ Γa²/4 ≈ **2.7 Å² ps⁻¹** — 표의 0.0207 보다 **≈ 130 배** 크다 (275 K 도 0.90 vs 0.0072 로 ≈ 125 배). ⇒ **차수에서 모순 — 이 기울기는 단일 홉 장벽이 아니다** (이동하는 Li 의 분율·반응 재배열·금속 Li 운동이 섞인 유효값). '0.07 eV 장벽' 으로 인용하지 않는다.
**② 짧은 MD '무반응·안정' → 관측창 (`D-2026-10-05-md-observation-window`)**: 해당한다 — 논문의 *"argyrodite coordination does not recover"* · *"the percolating Li₂S network persists unchanged"* 는 **반전 350 ps · 425 K** 의 '무반응' 서술이다.
관측창 (ν₀ 1e+13 s⁻¹ 가정 · 425 K · 궤적 3.5e-10 s): Ea ≳ **0.30 eV** 인 반응은 이 궤적에서 못 본다 · 반응 자리 ~100 (P 수 · ✎) 이면 ≳ **0.47 eV**. 장 없음 1 ns 의 *"Li₃P/LiCl coarsen only to a limited extent"* 는 (425 K · 1e-09 s) ≳ **0.34 eV** · 자리 100 이면 ≳ **0.51 eV**. ⇒ PS₄ 재조립 · 음이온 조대화처럼 음이온 이동이 필요한 과정이 이보다 높은 장벽이면 **"안 일어났다" 가 아니라 "이 창에서 못 본다"** 다. (저자도 조대화에는 *"on the simulated time scale"* 단서를 달았다.)
⚠ 도구 주의: `tools/sei/collect_neb.py --obs_window T t n` 은 셋째 값을 **n_sites 가 아니라 ν₀ 로** 넘긴다 (`observation_window(*a.obs_window)` 위치 인자) — 자리 100 이 ν₀ = 100 s⁻¹ 로 들어가 0.00 eV 가 찍힌다. 위 자리 100 값은 함수를 `n_sites=` 키워드로 직접 불러 냈다. (도구 수정은 이 digest 범위 밖 — 보고만.)
**③ 화학결합 규모 흡착·결합에너지 → 결합 자리 배위수 (`D-2026-10-05-adsorption-site-coordination`)**: **해당 없음** — 흡착·결합에너지 계산이 없다.

### 7-6 litdb 안 다른 편과의 교차 (그 파일들은 고치지 않았다)
- **`[Chaney24SEI]`** (MTP · NPT · 10 ns · Li(110)/LPSC(110) 샌드위치): 같은 계면에서 **비정질 log t (Δη 제한 · 확산 제한 아님) → 결정화 (√t/선형 주장)** · antifluorite **Li₂(S,P,Cl) 고용체**. 이 논문은 **장 없음 τ ∝ √t (확산 제한)** 로 다른 법칙을 낸다 — 둘 다 MLIP 인데 비정질 단계의 율속이 갈린다. 우리 재독: 이 논문 √t 는 그림이 지지 (n ≈ 0.54 · log t R² 0.970) · Chaney 는 n ≈ 0.8 로 이분법이 안 섰다. 관측량이 다르다 (τ_SEI 두께 vs 환원율 α) — 직접 대조는 안 된다. **이 논문은 Chaney 를 인용하지 않는다.** 산물 그림 ('Li₂S-like 망 안의 흩어진 P/Cl') 은 Chaney 의 고용체와 **같은 방향**이다.
- **`kim2026_li_argyrodite_sei_reactive_md`** (SSRN preprint · MTP · 350 K · 20 ns): S-rich 비정질 ~6 nm → Li₂S 결정 핵생성 ~11 ns → PS₄ 분해 정지 (구조적 자기 부동태화) · 결정영역 D 0.4 vs pristine 1.6 × 10⁻⁷ cm² s⁻¹ (≈ 1/4). 이 논문 계면상 D / 벌크 ≈ **1/3.4** (figure-read) — **두 MLIP 가 같은 차수**: MLIP 가 만든 계면상은 벌크 LPSCl 보다 몇 배 느릴 뿐이다. 둘 다 전자를 안 본다. 이 논문 1 ns 는 kim2026 의 핵생성 (~11 ns) 전 단계에 해당한다.
- **`luo2022_cryotem_li_dendrite_sulfide_interphase`** (cryo-TEM 실측): 25 °C 48 h → **단결정 Li₂S ~12 nm** (부동태화) · 60 °C → 다결정 + 비정질 ~3 nm · R_SEI 2 → 204 Ω. 'Li₂S 가 망의 주성분' 은 실측과 맞고, **'얼마나 저항성인가' 는 결정성·입계가 정한다** — 이 논문의 비정질 425 K 모델은 그 축을 못 본다.
- **`lai2020_li2s_interfacial_layer_amorphous_sulfide_cse`**: Li₂S '층 관통' NEB 0.22 eV (다중 홉 · 다른 양 — 우리 09-01 카드가 이미 비교 금지로 적었다). 이 논문과는 장벽 대응 없음.
- **`[Wang22Res]`** (ref 35): MTP 이원 산물 — Li₂S+Vac Ea 0.313 · 완전결정 Li₂S 1.573 eV · **400 K Li 금속 전융 의심**. 이 논문 425 K 에서 Li 금속은 층 진동이 유지된다 (`Fig. 1c` · `Fig. S2` 50–100 ps · figure-read) — 적어도 슬랩 안쪽은 결정. 고체 유지 점검은 이 논문도 따로 안 한다.
- **`wu2026_asslsb_li2s_reaction_mechanisms_engineering_review`**: 결정 Li₂S σ_RT figure-read ≈ 8 × 10⁻⁹ S cm⁻¹ (2차) · S/Li₂S 전자전도 ~10⁻³⁰ S cm⁻¹ (2차) → 'Li₂S-like' (MLIP) ≠ Li₂S (실측) 를 수치로 보여 준다. 경쟁 기전 S3 (Li₂S–LiX 고용체) 는 §7-3.
- **`li2026_mci_vs_sei_na3ps4_na_mlip_md`** (Persson · Na₃PS₄‖Na): **결합 그래프 퍼콜레이션으로 MCI ↔ SEI 를 가르는** 방법의 가장 가까운 친척. 그쪽은 Na–P 다리 (전자 경로 대리), 이쪽은 S–S 음이온 망 (Li 경로 대리) 을 본다 · 둘 다 *"필요조건이지 충분조건 아님"* 수준. 이 논문의 전자 세기 규칙은 MCI 질문 (금속 쪽 과리튬화 영역) 으로 한 걸음 간 것이다.
- **`li2026_functionally_differentiated_interphase`** (실험 · 인공 계면 LiF + LiCl/LiBr + Li₃N): "계면상은 처음 닿을 때 정해지고 리셋되지 않는다" 는 이 논문의 함의는 **첫 접촉 전에 인공 계면을 깔아야 한다**는 그 설계 논리와 같은 방향이다 (약한 연결).
- **`liu2026_li4sns4_mediator_low_barrier_li2s`** (양극 Li₂S 산화) · **`huang2022_li2sis3_anomalous_conductivity_bvse`** (Li₂SiS₃ 전도체): **직접 연결 없음** — 전자는 양극 쪽 Li₂S 산화 (ESW 산화축 ① 과만 닿음), 후자는 다른 물질.

---

## 8. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a,b | 반응 전 / ~1 ns 스냅샷 — Li 금속이 얇아지고 SE 쪽에 넓은 무질서 영역 | 계면 MD 셀 기하 (진공 15 Å · 상대전극 없음) 참고 |
| 1c | Li·S 수밀도 z 프로파일 (마지막 50 ps) — Li 금속 z ≈ 22–50 Å 층 진동 · 온전 LPSCl z ≈ 115–130 Å | 계면상 범위를 밀도로 정하는 법 |
| 1d | 계면상 (60–85 Å) in-plane Li–Li g(r) — 2.8 / 4.5 Å · 시간 변화 작음 | 근거 약함 (변화 거의 없음) |
| 2a | in-plane MSD 50 ps 창 4 개 | ✎ 0.00 ns 창 D ≈ 0.5 Å² ps⁻¹ (그림 2b 축 밖) |
| 2b | D_xy(t) 10 점 + 벌크 AIMD 0.031 선 | 계면상 D ≈ 벌크 1/3.4 (figure-read) — kim2026 의 1/4 와 같은 차수 |
| 2c | σ^NE_xy(t) + 벌크 선 (figure-read ≈ 0.35) | ✎ σ/D 로 ρ ≈ 0.046 Å⁻³ 역산 → σ 는 벌크의 ≈ 1/2 |
| 3a–c | in-plane Li–S / Li–Cl / Li–P g(r) vs 425 K 결정 | 첫 껍질만 맞고 둘째 껍질 없음 → '상' 이 아니라 '국소 배위' |
| 3d | 환경 색칠 스냅샷 | 분류 결과 시각화 예 |
| 3e | Li 중심 환경 분율 (0–1 ns) | §3 수치 · 방법 서술과 어긋남 (§10-11) |
| 3f | τ_SEI(t) + √t 삽입 (R² 0.992) | ✎ 우리 재독 n ≈ 0.54 · log t R² 0.970 → 장 없음 √t 지지 |
| 4a–d | 장 구동 0/100/350/450/700 ps: 구조 · 조성 · Li 전하 · P 전하 (재크롭본) | "Li 는 돌아오고 LPSCl 은 안 돌아온다" 의 그림 근거 · P 전하 700 ps 에 옅어짐 (미논의) |
| 5a | 순/역 구간 Li 중심 조성 | LPSCl ≈ 95 ps 에 0 (본문 '60 ps' 보다 늦음) · Li₂S-like 67–70 % 고정 |
| 5b | 장 구간 τ_SEI + √t 삽입 (R² 0.987) | ✎ 우리 재독: 지수 0.2–0.5 구별 불가 · log t 0.980 · ≈ 3 Å 계단 |
| 5c | 반전 구간 누적 N_Li (450–700 ps) · 0.419 ps⁻¹ | 장 구동 '전도도' 정의 사례 — 선형응답 밖 |
| 6a | S / P / Cl 그래프 스냅샷 | 산물 위상 시각화 |
| 6b | Φ_S, Φ_P, Φ_Cl (0–700 ps) | Φ_S = 1 (≈ 105 ps) = LPSCl 소멸 (≈ 95 ps) — 정의상 귀결 |
| 6c | S_max log–log · α 0.77 / 0.49 · t* ≈ 6 ps | 플래토 figure-read ≈ 5.6×10² (≈ N_S) |
| 6d | JMAK · n 0.74 | 서술용 지수 |
| 7a–e | 슬랩 위치 · 벌크 Li₂₅₀ · 슬랩 i · 슬랩 ii · 벌크 Li₂₄P₄S₂₀Cl₄ DOS | 전자 세기 규칙 (N_Li vs 2N_S + 3N_P + N_Cl) — 우리 음극 전자 분류의 사전 선별 후보 · 벌크 VB 꼭대기 Cl 색 (figure-read) |
| S1 | CHGNet 힘 parity 4 세트 | 검증셋이 반응 전 계면뿐 · (b) 대각선 아래 꼬리 |
| S2 | 장 구간 Li·S z 프로파일 3 창 | Li : S ≈ 3 · Li 가 S 끝 넘어 진공 쪽 표면에 쌓임 |
| S3 | 4 면 조합 σ^NE_xy vs T | 비단조 · 275 K 에도 0.2–0.37 S cm⁻¹ |
| S4 | 결정 Li₂S S–S · Li₃P P–P · LiCl Cl–Cl g(r) + 컷오프 | 그래프 컷오프를 정하는 법 |
| S5 | 장 없음 그래프 분석 (Φ · S_max · JMAK · 클러스터 수) | S 클러스터 ≈ 1 개 · P/Cl 은 수만 늘고 크기는 그대로 |
| Table S1 | 학습 AIMD 14 계 | 학습셋 설계 참고 (2000·5000 K 벌크 + 500 K 표면·계면) |
| Table S2 | 4 면 조합 × 4 T D_xy | ✎ 기울기 0.04–0.08 eV — 장벽 아님 (§7-5 ①) |

---

## 9. Post-processing ★
- **무엇**: in-plane MSD → **D_xy** (Einstein, 2D 라 1/4) · **Nernst–Einstein σ** (Haven 1 · ρ = 영역 Li 전부) · **J/E σ_eff** (평면 통과 Li 수 기울기) · in-plane **g(r)** (Li–Li · Li–S · Li–Cl · Li–P) · **국소 환경 분류** (거리 컷오프 · d/r_cut 동점) · **τ_SEI** (2 Å bin 반응분율 · Gaussian 평활 · 0.5 교차) · **음이온 그래프** 연결 성분 (S_max · Φ · 클러스터 수) · **멱법칙** (S_max) · **JMAK 선형화** · **PDOS** (VASP 구 사영) · **전자 세기** (음이온 수용 한도).
- **도구**: LAMMPS · CP2K (GFN1-xTB) · VASP · CHGNet 만 명시. 그래프·분류·밀도 분석 코드 (OVITO · ASE · pymatgen · networkx 등) **0 줄** · 코드·데이터 공개 없음.
- **수치화·기록**: 대부분 본문 문장 + 그림 · 표는 SI 2 장 · 오차막대 없음 · 음영 띠 의미 미기재 · 적합 구간은 일부만 (Φ 1–100 ps · τ 첫 100 ps).

---

## 10. 비판 — 이 논문의 약한 곳 ★
1. **제목 'Li₂S' ↔ 본문 'Li₂S-like'.** 'Li₂S-like S' 는 온전한 PS₄ 근처가 아닌 S 일 뿐이고 S²⁻·결정성을 확인하지 않는다 (§4-5). 장 구간 Φ_S = 1 은 PS₄ 의 완전 소실과 같은 사건이다 (정의상).
2. **MLIP 검증이 프로덕션 영역을 덮지 않는다.** 검증 4 세트는 반응 전 계면 AIMD 350·500 K (그중 (010)/Li(100) 500 K 는 학습 계와 같은 계·같은 온도) · 에너지 RMSE 0.3–0.5 meV/atom 은 근평형 배열의 값이다. Li 과잉 비정질 · 장 구동 · 완전 변환 배열에 대한 DFT 단일점 대조가 없다. `Fig. S1b` 에 체계적 꼬리 (figure-read).
3. **전자 없음 → 해석이 바뀐다.** Li 는 Li⁰ 로 움직인다 → '장 구동 수송' 은 SE 의 화학적 리튬화 · '가역 수송' 은 닫힌 계의 여분 Li 왕복 · '비가역' 은 산화 경로 부재의 귀결 (§6-3). 저자는 성장에 대해서만 전자 단서를 단다.
4. **퍼콜레이션에 무작위 대조가 없다.** S 5/7 ≈ 0.71 · P·Cl 1/7 ≈ 0.14 vs fcc 자리 문턱 ≈ 0.20 → 무작위여도 같은 결과 (✎). 관통(spanning) 검사도, Li 경로의 환경 분해도 없다 — *"any continuous path … must pass through it"* 은 기하 논리다.
5. **장 세기**: 0.1 V Å⁻¹ ≈ SE 에 6 V · qEa ≈ 3.8 kT (✎ q ≈ 0.5e 가정) → 비선형 · 전류 ~10⁹ 배 · 장 크기 한 점. σ_eff ≈ σ^NE 일치는 구조·방향·체제가 다른 두 수의 우연 (§5-2).
6. **성장 법칙**: 장 없음 √t 는 그림이 지지하지만 (✎ n ≈ 0.54), 같은 계면의 `[Chaney24SEI]` (log t · 비인용) 와 갈린다. 장 구간은 일정한 장 아래 표류라면 선형 성장이 단순 기대인데 √t 로 맞췄고, 창이 1 decade 미만 · 슬랩 고갈 · 지수 0.2–0.5 구별 불가 · ≈ 3 Å 계단 (✎).
7. **"nearly seven-fold"** 는 k_W 비 — 시간으로는 ≈ 47 배 (✎).
8. **시드 1 · 음영 미설명** — 모든 곡선이 궤적 하나.
9. **온도 하나**: 성장·장 런은 425 K (Li 융점의 0.94) 뿐. 서론의 *"additional results at other temperatures"* 는 `Table S2` 의 D 뿐 → 성장 속도의 온도 의존·Ea 없음.
10. **수송 방향**: 장 없음 수송은 in-plane (xy) 만 — 계면을 **건너는** (z) 수송은 장 없이 안 쟀다. '계면상 영역' 의 원자 출입 처리 미기재.
11. **조성 서술 불일치**: 방법은 'P/S/Cl 중심으로 산물을 센다', 그림 (`Fig. 3e`·`5a`) 은 Li 중심 분율. 분류·그래프 컷오프 민감도 분석 없음 (Cl 4.90 Å 는 결정 P–Cl(4a) ≈ 4.9 Å 와 거의 같다 · ✎).
12. **경계 조건**: 상대전극이 없어 Li 가 **진공에 면한 SE 표면**에 쌓인다 (`Fig. S2` · figure-read). 어느 계면이 도금/박리인지 정의가 없는데 초록은 *"survives stripping"* 이라 쓴다.
13. **DOS**: 이완 안 한 5 Å 슬랩 · Γ · spin-up 만 · 저자가 정성임을 밝힘 (좋음). 벌크 LPSCl VB 꼭대기 봉우리가 Cl 색 (figure-read) — 우리 comp1 (S 3p) 과 다르게 보이나 미논의.
14. **선행 누락**: `[Chaney24SEI]` · kim2026 (SSRN) 비인용. **데이터 비공개** (요청 시).
15. **초록 과장 둘**: *"for nanoseconds"* (장 런 0.7 ns) · *"negligible within ~60 ps"* (그림상 ≈ 9 %).
16. **미기재**: 격자 부정합 처리 · LPSCl 무질서 · CHGNet 세부 · AIMD 조건 · 벌크 D 의 AIMD 조건 · 자체 표면에너지 수치.

**잘한 것 (공정하게)**: 2,524 원자 · ns · 계면 데이터 fine-tune · **장 + 동적 전하**라는 새 설정 · 분석이 다층 (분류 · 성장 · 그래프 · JMAK · DOS) · 저자가 단서를 꽤 성실히 단다 (σ_eff 는 *effective* · n 은 *descriptive* · DOS 는 *qualitative* · 절대값은 실험과 안 맞을 것). **전자 세기 규칙**은 깔끔하고 재사용 가치가 있다.

---

## 11. 적용 인사이트 · 우리가 할 수 있는 다음 수 (결정은 사용자)
1. **[SEI NEB]** 원고에 Li₂S 장벽을 쓸 때 **단계 (결정 Li₂S · 결정화 뒤 SEI)** 를 명시 — 이 논문 (비정질 Li 과잉 단계) 과 충돌하지 않는다. 비용 0. 4×4×4 판정 계획은 그대로.
2. **[ESW·음극]** `HZ-anode-b2o3-reaction-direction` 재실행 때 이 편을 '같은 방향의 MLIP 동역학 그림 (프리프린트 · 독립 확인으로는 세지 않음)' 으로 곁들일 후보 · `min_product_gap_eV` 의 '상분리 가정' 라벨에 이 편 (Li₃P-like ~10 원자 클러스터) 을 근거로 보탤 후보 · 음극 계면 기록에 **전자 세기 플래그** (N_Li − (2N_S + 3N_P + N_Cl)) 를 넣는 안 — 비용: 산수뿐 (분 단위).
3. **[도구]** `tools/sei/collect_neb.py --obs_window` 셋째 인자 버그 (n_sites → ν₀) — 한 줄 수정 + CLI 경로 음성 selftest. 비용 ~10 분.
4. **[선택 · 메일 한 통]** 교신저자에게 궤적 요청 (*"upon reasonable request"*) → 받으면 무작위 표지 대조 (S/P/Cl 표지를 같은 음이온 자리에서 섞어 Φ 재계산) 와 원자료 τ(t) 의 log t vs √t 를 CPU 로 수 분에. 결과가 '무작위와 같다' 면 퍼콜레이션 주장은 화학량론의 귀결로 정리된다.
5. **[li2s · 외부 1저자 몫]** 계면상 구조를 볼 때 그래프 + 무작위 대조 분석을 제안할 수는 있다 — 제안만.
6. **[나중 · 큰 것]** 우리 UMA 로 같은 계면을 재현하려면 먼저 T3 게이트 (반응 계면 스냅샷의 UMA ↔ QE 단일점 대조 · `kim2026` digest §3.5) 가 필요하다. 2,500 원자 · 1 ns UMA MD 는 GPU 하루 안팎 어림 + QE 단일점 ~20 개 (GPU) — kgy (cascade v7) · gabia (탄성·Li₃Nd) 가 차 있어 **지금은 권하지 않는다**.

**가장 날카로운 통찰 셋**
- ① **'비가역' 은 발견이 아니라 장부다** — 닫힌 계에서 장이 왕복시키는 것은 환원에 쓰고 남은 여분 Li (✎ ≈ 10–20 %) 뿐이고, 산물을 되돌리려면 ≈ 1.72 V 가 필요하다. 진짜 새 것은 속도 (k_W ≈ 7 배) 와 위상이다.
- ② **연결 위상은 화학량론이 정한다 (무작위 기준)** — 5 : 1 : 1 이면 S 는 이어지고 P·Cl 은 흩어진다. 이 논문은 무작위와 구별되는 무엇을 보이지 않았다.
- ③ **MLIP 계면상은 '느린 Li₂S' 가 아니라 '빠른 Li 과잉 비정질'** — D 는 벌크 LPSCl 의 ≈ 1/3 (이 편) · ≈ 1/4 (kim2026). 실측 SEI 의 저항성은 결정화 뒤에 생긴다 → 우리 결정 Li₂S 장벽의 자리가 거기다.

---

## 12. 인용 가능 문장 (영문 초안) · ⛔ 인용 금지
**인용 가능** (전부 *"[Yuan, Chen & Dawson, ChemRxiv 2026, preprint, not peer reviewed]"* 병기):
- "Fine-tuned MLIP simulations with field-updated atomic charges suggest that, at the Li/Li₆PS₅Cl contact, the Li₂S-like decomposition product forms a single connected network, whereas Li₃P- and LiCl-like products remain as small, isolated clusters."
- "In these simulations, reversing an applied field reverses the net Li flux but does not restore the argyrodite coordination."
- "Without an applied field, MLIP-MD interphase growth at 425 K followed √t kinetics over ~1 ns."
- (방법) "Atom-centred charges recomputed with GFN1-xTB every 1 ps allow field-induced forces to follow the changing charge state of Li between metallic and ionic environments."

**⛔ 인용 금지**
- σ_eff 0.166 S cm⁻¹ · σ^NE ≈ 0.18 S cm⁻¹ 를 **SEI·Li₂S 의 이온전도도**로 (장 구동 · 비선형 · 425 K · Li 과잉 혼합 영역).
- 'percolating Li₂S' 를 **결정 Li₂S** 로 · 'seven-fold' 를 **시간 가속**으로.
- '장 아래에서도 √t → 확산 제한' 을 입증된 것으로 (§5-2 우리 재독).
- *"anode-interface resistance … set early in cycling"* 을 **결과**로 (저항 계산 없음 · 외삽).
- `Table S2` 기울기를 **Ea** 로 (§7-5 ① 홉 수 모순).
- 이 편의 D·σ 를 **우리 db 값과 같은 표에** (문헌 소환값 · 방법 다름 · 우리 MD 절대값은 인용 정책상 안 씀).
- '독립 확인 3건' 식으로 우리 음극 반응식 방향 근거에 합산 (반응식은 인용 · 분류는 S²⁻ 미확인).

---

## 13. 주의 / 한계 (인용 규율)
- **PREPRINT · v1 · 미심사** — 수치가 바뀔 수 있다. 출판본이 나오면 이 digest 를 대조한다.
- **MLIP + 전자 없음 + 시드 1 + 425 K + 장 한 점** — 모든 수치에 이 다섯이 붙는다.
- 문헌 수치는 **소환값** — 우리 db 절대값과 섞지 않는다 (CLAUDE.md §litdb).
- 우리 Li₂S NEB 값 · li2s 트랙 수송값 · 우리 MD 절대 σ 는 이 digest 에 **싣지 않았다** (각각 BLOCKED/citable=false · 외부 1저자 트랙 금지 · 인용 정책).
- 우리 ESW 수치 (1.717 · 2.256 V) 는 라벨 (교환-0 아래 가장자리 · 산화 onset 축 ①) 과 규약 (MP2020 · GG 제외 · grand-potential) 을 붙여서만.

---

## 14. 기법 용어 미니사전
- **CHGNet** — 결정 그래프 신경망 MLIP (Deng 2023). 자기모멘트를 같이 예측해 전하 상태를 암묵적으로 담는다. 여기서는 계 특화 AIMD 로 **fine-tune**.
- **fine-tuning** — 사전학습 MLIP 의 가중치를 계 특화 데이터로 조금 더 학습시키는 것.
- **GFN1-xTB** — 반경험적 강결합 DFT (Grimme 2017). 빠르게 원자 부분전하를 준다 (여기서는 장의 힘 F = qE 용).
- **LAMMPS `efield`** — 모든 원자에 q_i E 의 힘을 더하는 명령. 전자 분극·차폐는 없다.
- **CSVR** — 확률적 속도 재조정 열욕 (Bussi 2007). 바른 정준 앙상블을 준다.
- **in-plane MSD / D_xy** — 계면에 평행한 두 방향만 본 평균제곱변위 · D = 기울기/4.
- **Nernst–Einstein σ** — σ = ρ(Ze)² D / kT. 이온 간 상관을 무시 (Haven 비 = 1).
- **σ_eff = J/E** — 장이 만든 순유속을 장으로 나눈 '유효' 전도도. 선형응답 (qEa ≪ kT) 일 때만 영장 전도도와 같다.
- **Wagner (포물선) 성장** — 성장층을 통한 확산이 율속이면 두께 ∝ √t. 실제 SEI 에서는 이온·**전자** 둘 다 층을 지나야 한다.
- **JMAK (Avrami)** — 변환분율 Φ = 1 − exp(−k tⁿ). n 은 핵생성·성장 양식을 시사하지만 여기서는 서술용.
- **퍼콜레이션 · 자리 문턱** — 격자 자리를 무작위로 p 만큼 채울 때 무한 연결 클러스터가 생기는 최소 p. fcc 자리 문턱 ≈ 0.20.
- **연결 성분 · S_max · Φ** — 그래프에서 서로 이어진 노드 묶음 · 가장 큰 묶음의 크기 · 그 크기 / 전체 노드 수.
- **g(r) 첫 극소 컷오프** — 결정 RDF 의 첫·둘째 껍질 사이 골을 이웃 판정 거리로 쓰는 관례.
- **PBEsol / DFT-D3 / PAW** — 고체용 GGA 범함수 / Grimme 분산 보정 / 투영 증강파.
- **전자 세기 (음이온 수용 한도)** — 음이온이 가장 환원된 상태 (S²⁻ · P³⁻ · Cl⁻) 까지 받을 수 있는 전자 수 2N_S + 3N_P + N_Cl 을 Li 수와 비교해 과잉 전자 (금속성) 를 예측하는 산수.
- **관측창 (우리 규율)** — Ea_max ≈ kT·ln(ν₀·t·n): 그 궤적이 한 번이라도 볼 수 있었던 장벽의 상한.

---

## 15. 누락 점검 · 미해결
- **PDF 온전성**: 본문 17 pp (표지 1 + 원고 16, 쪽 번호 2–16 연속 · refs 62 끝까지) · SI 13 pp (§I–V + refs 2) — 빠진 쪽 없음.
- **본문이 가리키는 그림·표**: `Fig. 1`–`7` · `Fig. S1`–`S5` · `Table S1`–`S2` 전부 있다.
- **본문이 "SI 에 있다" 고 했는데 SI 에 없는 것**: CHGNet **미세조정 절차·하이퍼파라미터** · AIMD **k-점·길이·프레임 수** · *"reference electronic-structure settings"* (본문 방법 절의 PBEsol·520 eV·D3 뿐) · **자체 표면에너지 수치** (*"reproduce the same relative ordering"* 만) · *"additional results at other temperatures"* 는 `Table S2`·`Fig. S3` 의 D 뿐.
- **어디에도 없는 것**: 벌크 기준 D 의 AIMD 조건 · 음영 띠의 의미 · N_Li 평면 위치·순/총 · 슬랩 이완 여부 · 격자 부정합 처리 · 무질서 · 데이터 공개.
- **추출기**: SI 캡션 `FIG. S.1.` (S 와 번호 사이 점) 을 `CAP_RE` 가 못 잡아 SI 에서 0 개 → 7 장 손 크롭 (`figures.json` `manual_crop` 사유) · `Fig. 4` 자동 크롭이 아래 절반만 → 재크롭 (`recrop` 사유). `missing_labels` 는 비어 있다 (SI 캡션을 아예 못 봤기 때문 — 번호 공백 절도 그래서 안 떴다).
- **읽지 못한 부분**: 없음. 그림 14장 전부 봤다.

---

## 🗨️ Q&A 로그
(아직 없음)

<!-- digest 초판 2026-10-03 (논문 에이전트 · 심층판). 제1 목적 = 사용자 요청
     "NEB 를 어떻게 진행했는지 · 논리에 모순은 없는지 · DFT 실행 오류 · 우리와 뭐가 달라서 이런 결과" → `## 6. NEB 감사`.
     ① 본문 그림 5장 전부 실독. `Fig. 2d`(FFT)·`Fig. 2e`(사슬·슬랩 4–5×)·`Fig. 2f`·`Fig. 4d`·`Fig. 5e` 는 원본 래스터를 잘라 확대해 읽었고,
        `Fig. 5a` 는 막 두께를 픽셀로 쟀다.
     ② SI 그림 24장 = 13장 원본 크기 실독 + 11장 축소판(재크롭 검수 시트). `Fig. S15`·`Fig. S16` 은 PDF 에 박힌 원본 래스터(584×514 · 213×481 px)를
        뽑아 2–4× 확대해 셀·원자·궤적을 셌다.
     ③ 크롭 정정 (figures.json 에 사유): `Fig. S10` 손 크롭(도구 번호 공백) · `Fig. S4` 오크롭(S5 사진이 들어 있었다) 교체 ·
        SI 그림 14장 아래쪽 13–25 pt 잘림(축 제목 소실) 재크롭 · `Table S1`–`S3` 재크롭 + 여러 쪽 표 이어붙임.
     ④ SI 계산 조건 문단은 페이지를 렌더해 원문 대조 (텍스트층은 "10–5"·"~105 nm" 처럼 윗첨자를 잃는다).
     ⑤ 홉 수 검산 = `tools/sei/collect_neb.py::hop_check` (ν₀ 10¹³ s⁻¹ 가정 · 303.15 K) — `D-2026-09-27-barrier-hop-count`.
     ⑥ 대피 세션(브랜치 claude/evac-2026-10-02) — INDEX/comparison 반영은 부모 세션이 한다. -->

# Dual-Binder-Enabled 18-µm-Thick High-Conductivity Sulfide Electrolyte Film for High-Energy-Density All-Solid-State Batteries — Cao, Wang et al. (*Adv. Mater.* 2026, e74533)

> slug `cao2026_dual_binder_18um_sulfide_electrolyte_film` · DOI `10.1002/adma.74533` · type `exp (건식 열압연 막 · 전기화학 · 7Li ssNMR · cryo-TEM · 나노압입 · MIP) + DFT 보조 (VASP PBE-D3 CI-NEB 3건)` · PDF `litdb/inbox/Cao 2026 - Dual-binder 18 um sulfide electrolyte film (Adv Mater e74533).pdf` (본문 11 pp) + `litdb/inbox/Cao 2026 - Sup) Dual-binder 18 um sulfide electrolyte film (Adv Mater e74533) SI.pdf` (SI 25 pp: Experimental · `Fig. S1`–`S24` · `Table S1`–`S3`) · digested `2026-10-03` · status ✅ · 태그 **[외부]**

> elements: Li, P, S, Cl, C, H, O, N, F
> methods: DFT, NEB, ESW, XPS, Raman

> **저자**: **Defu Cao**¹²‡ · **Chao Wang**³‡ · Weiping Li²⁴ · Yang Li¹ · Jiacheng Zhu²⁴ · Hong Liu⁵ · Zhaoxiang Wang²⁴ · **Yejing Li**⁶\* · **Hao Zhang**⁷\* · **Xuefeng Wang**²⁴\* · Ce-Wen Nan⁵ · **Li-Zhen Fan**¹\* (‡공동 1저자) — ¹USTB Institute for Advanced Materials and Technology ²IOP-CAS 응집물리 국가연구센터 ³Eastern Institute of Technology (Ningbo) ⁴UCAS ⁵Tsinghua 신세라믹 국가중점실험실 ⁶USTB 전기화학 에너지저장 북경중점실험실(SI 에는 'State Key Lab of Advanced Metallurgy') ⁷Chemical Defense Institute (Beijing) · 접수 2026-03-18 · 개정 06-27 · 수락 07-25 · **OA 아님** (© Wiley-VCH, 'rights for text and data mining … reserved') · 자금: 국가 R&D 2023YFB2503902 · NSFC 22479009·52402275 · 북경 NSF 2244094 · 데이터: "SI 에 있다" (원구조·NEB 경로 파일은 **없다**)
>
> **계보**: 같은 USTB **Li-Zhen Fan** 그룹 — `[LiInF]` `li2024_inf3_argyrodite_ultrathin_film` (같은 국가 R&D 과제 2023YFB2503902 · 슬랩 CI-NEB pristine **0.662 eV**, 톱니 프로파일) · `[LiGaF]` `liyaru_gaf3_codoping_argyrodite` · `[Fan26]` `fan2026_sulfide_assb_stability_review_ECERD2600097` (공저 Yang Li · Hong Liu · Ce-Wen Nan). 1저자 Cao 의 선행 = ref 39 *Adv. Mater.* 33, 2105505 (2021, amphipathic binder 박막).
>
> **관련 digest**: `deklerk2016_diffusion_site_disorder_argyrodite` (**[dK16Arg]** — all-4a 정렬이면 intercage 가 사실상 0) · `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` (**[Kraft]** — 실제 Li₆PS₅Cl 4d 무질서 ≈62 %) · `adeli2019_halide_substitution_boosting_argyrodite` (**[Adeli19]** — intercage 점프 2.88 Å · Haven ≈0.3) · `morgan2021_anion_disorder_superionic_mechanism_li6ps5x` (**[Morgan21Mech]**) · `he2018_statistical_variances_diffusional_aimd` (**[He18Var]**) · `marcolongo_ionic_correlations_failure_nernst_einstein` (**[Marc17NE]**) · `li2026_li_kinetic_promoter_aqueous_mn_sulfur` (**[Li26MnS]** — 0.97 eV 홉 수 선례) · 건식막/바인더(DEM 쪽, 읽기만): `matthews2024_ptfe_nanofibril_network` · `lee2025_dual_fibrous_ptfe_dry_electrode` · `mun2025_dry_electrode_technology_assb_review` · `bielefeld2020_effective_ionic_conductivity_binder` · `kang2025_bollard_anchored_binder_dry_electrode`.

> **본 digest 에서 실제로 본 그림 (2026-10-03)**: 본문 `Fig. 1`–`Fig. 5` **전부** (확대: `Fig. 2d` FFT · `Fig. 2e` 사슬·슬랩 · `Fig. 2f` · `Fig. 4d` · `Fig. 5e` · `Fig. 5a` 픽셀 측정). SI **원본 크기 13장**: `Fig. S2` · `S5` · `S6` · `S10` · `S12` · `S13` · `S15` · `S16` · `S17` · `S18` · `S19` · `S21` · `S23` (`S15`·`S16` 은 원본 래스터 2–4× 확대). SI **축소판으로만 11장**: `Fig. S1` · `S3` · `S4` · `S7` · `S8` · `S9` · `S11` · `S14` · `S20` · `S22` · `S24` (재크롭 검수 시트 ≈640 px 폭 — 판독값은 이 11장에서 따지 않았다). 표는 PDF 텍스트로 읽고 재크롭본으로 행 정렬만 확인했다.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 논문에 없는 우리 계산은 **(우리 산수)** 로 표시했다. ⛔ 우리 σ·D·Ea 는 1저자 인용정책(2026-09-18)상 **우리 계 사이 상대차로만** 쓴다 — 이 논문의 장벽·σ 와 같은 줄에 숫자로 놓지 않는다.

---

## 0. 이 digest 를 읽는 법 — NEB 감사 결론 먼저

이 논문은 **막 공정 논문**이다(LPSCl + 1 wt% PTFE 전구막에 Li⁺ 전도성 고분자 LiTFSI-PMEMA 4 wt% 를 접어 넣고 40회 열압연 → 18 µm · 1.56 mS cm⁻¹). DFT 는 `Fig. 2e,f` + `Fig. S15`·`Fig. S16` 의 **CI-NEB 3건**뿐이고, 그 세 값(**0.55 / 0.85 / 1.20 eV**)이 "LPSCl 이 주 경로, 고분자/접촉부는 보조" 라는 **수송 모형(`Fig. 2g`)의 이론 근거**로 쓰인다.

| 사용자 질문 | 한 줄 답 | 절 |
|---|---|---|
| ① 무엇을 어떻게 계산했나 | VASP · PBE-D3 · PAW · 550 eV · Γ(구조) / 3×3×1(단일점) · CI-NEB **"중간 이미지 4개, 선형 보간"** · 벌크 "3×3×3" · 슬랩 "(100) 5층 3×3 · 진공 20 Å". **고분자 계산은 방법 문단에 한 줄도 없다.** 전하·끝점·무질서·스프링·수렴 여부 **미기재** | §6.1 |
| ② 논리 모순 | **있다.** 0.85 eV(접촉부)면 30 °C 에서 한 자리 **13.5 s 에 한 번**, 1.20 eV(고분자)면 **≈103 일에 한 번** 뛴다 — 그런데 같은 논문이 고분자 막 σ = **1.04×10⁻⁴ S cm⁻¹** 를 쟀다. 그 σ 는 Li 하나가 **~10⁸ 회/s** 움직여야 나온다(우리 산수) → 1.20 eV 는 **10¹⁵ 배** 틀린 차수다. 0.55 eV(벌크)도 자기 실측 σ 3.23 mS cm⁻¹ 대비 **2×10⁴ 배** 느리다. 저자는 "Ea 와 같지 않다" 고 단서를 달았지만, 결론에서 "contact-assisted transfer"·"active ionic mediator" 를 **그 계층에서** 끌어낸다 | §6.2 |
| ③ DFT 실행상 오류 | **확인**: 이미지 수 불일치(방법 4 ↔ `Fig. 2f` **7**) · "LiTFSI-PMEMA" 모형에 **TFSI⁻ 가 없다** · 고분자 사슬이 **PMEMA 가 아니다**(긴 곁사슬 하나에 에테르 O 4–5 개) · 고분자 계산 방법 0 줄 · 서로 다른 세 모형의 장벽을 한 줄 계층으로 비교. **의심**: 벌크 셀이 그림상 정육면체 **1개(≈a)** · 슬랩 가로도 **≈a** · 세 경로 끝점이 **모두 정확히 0.00** · 6–8 Å 경로에 **중간 극소 없음** · 정렬 Cl@4a 모형 · 전하(Li⁰ 라디칼 가능성) | §6.3 |
| ④ 우리와 뭐가 달라서 | **계산 조건**(정렬 모형 = [dK16Arg] 에서 intercage 점프가 사라지는 배열 · 셀 · 손으로 고른 한 경로 · 전하 미선언) · **보고량**(0 K 한 안장점 vs 우리 MLIP-MD 유효 Ea 는 모든 점프·배치를 평균한 거시량 · BVSE 는 정적 채널) · **서술**(다른 세 모형의 숫자를 한 계층으로 vs 우리는 같은 프로토콜 안 상대차만 + 홉 수 검산 한 줄) | §6.4 |

⇒ **가져갈 것**: 이 논문의 **실험**(막 두께·기공·σ·σ_e·셀)은 DEM 축 앵커로 쓸 만하다(§12). **DFT 3값은 인용 금지**(§14) — 대신 *"정렬 모형 + 미선언 전하 + 다른 모형 간 비교"* 가 어떻게 실측과 10⁴–10¹⁵ 배 어긋나는지 보여 주는 **방법 반례**로 쓴다.

---

## 1. 한 줄 요약

건식 공정에서 Li⁺ 절연 바인더(PTFE)만 쓰면 막이 성기거나(1 wt%) 전도도가 무너진다(5 wt%: 0.42 mS cm⁻¹). 저자들은 **LiTFSI-PMEMA**(MEMA:LiTFSI 7:3, 70 °C 열중합 · RT σ 1.04×10⁻⁴ S cm⁻¹)를 **두 번째 바인더**로 1 wt% PTFE 전구막에 4:96 으로 겹쳐 **40 회 접고 100 °C 열압연** → **18 µm · 1.56 mS cm⁻¹ · 겉보기 기공률 14.36 %** 의 자립막(USF)을 만들고, LCO‖USF‖LiIn **1500 사이클 70.3 %** · NCM721‖USF‖nSi 파우치 **322.7 Wh kg⁻¹(스택)** 를 보였다. 수송 기전은 ⁷Li NMR(중간 성분 0.88 ppm) · cryo-TEM(≈7 nm 고분자 피막) · DFT 장벽 계층(LPSCl 0.55 < 접촉 0.85 < 고분자 1.20 eV)으로 "LPSCl 주도 + 접촉부 보조" 모형을 **제안**한다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 동기 | 습식은 용매가 황화물을 상하게 하고 비극성 용매는 바인더를 못 녹인다 → 건식. 그러나 PTFE·PVDF·SBR·TPA 같은 **Li⁺ 절연 바인더**는 ≤5 wt% 에서도 σ 를 "한 자릿수" 깎는다 (본문 p.2) |
| 질문 | ① 이온 전도성 바인더로 얇고(≤20 µm) 전도도 높은 자립막을 건식으로 만들 수 있나 ② 세라믹–고분자 혼성막에서 Li⁺ 는 어디로 가나 (특히 SE/고분자 이종계면) |
| 조성 | **Li₆PS₅Cl** (중국자동차배터리연구원 상용 분말 · 1–3 µm, `Fig. S1`) + PTFE (Sigma) + **LiTFSI-PMEMA** (MEMA Macklin ≥98 % + LiTFSI Innochem · 7:3 질량 · AIBN 1 mol%) |
| 연구유형 | 실험 주 + DFT 보조(CI-NEB 3건). AIMD·MD·NMR 계산 **없음** |
| 본문 구성 | 2.1 제작·구조(`Fig. 1`) → 2.2 전도 기전(`Fig. 2`) → 2.3 셀(`Fig. 3`–`Fig. 5`). Experimental 은 **전부 SI** (pp.3–6) |
| 편집 흔적 | 본문 p.6 *"revised ⁷Li ssNMR analysis"* — 심사 대응 문구가 그대로 남았다 · 이해상충란 *"…no conflict of interest **is correct**"* · SI 제목이 본문과 다르다 (*"…Enabled an 18 μm-thickness and…"*) |

---

## 3. 핵심 수치 총정리 ★

### 3a. 막 제작·구조 (`Fig. 1`, `Fig. S5`, `Fig. S6`, `Fig. S8`, SI pp.3, 5–6)

| 시료 | 조성 (질량) | 두께 | 겉보기 기공률 (MIP) | D50 / 피크 기공 | 출처 |
|---|---|---|---|---|---|
| LPSCl-PTFE **전구막** | PTFE:LPSCl = **1:99** · 100 °C 롤압 | ⚠ **20 µm** (p.2) ↔ **≈30 µm** (p.2–3 · `Fig. S5a` 게이지 0.03 mm) | **34.99 %** | **630.0 nm** / figure-read ≈830 nm | 본문 p.4 · `Fig. S8` |
| LiTFSI-PMEMA 막 | MEMA:LiTFSI 7:3 · 70 °C 12 h | **≈26 µm** (`Fig. S5b` 0.026 mm) | n/a | n/a | 본문 p.2 |
| LPSCl-LiTFSI-PMEMA | 고분자 **5 wt%** 단독 | **≈50 µm** · 거시 균열 (`Fig. S5c`) | n/a | n/a | 본문 p.2–4 |
| LPSCl-PTFE **대조막** | PTFE:LPSCl = **5:95** (SI p.3) | 미기재 | n/a | n/a | SI p.3 |
| **USF** | 전구막:LiTFSI-PMEMA = **96:4** · 접기+100 °C 열압연 **40 회** | **18 µm** (SEM `Fig. 1c`) · 게이지 0.02 mm (`Fig. S5d`, 0.01 mm 눈금) · 최대 **10×5 cm** | **14.36 %** | **150.0 nm** / figure-read ≈150 nm | 본문 p.4 |

- 거대기공(≥500 nm) 비율 (`Fig. 1f`): 전구막 figure-read ≈56 % · USF figure-read ≈15 %.
- USF 최종 조성 (우리 산수, SI p.3 질량비로부터): **LPSCl 95.04 · PTFE 0.96 · LiTFSI-PMEMA 4.00 wt%** (그중 LiTFSI 1.20 · PMEMA 2.80). 본문 *"same total binder content (5 wt.%) … 4 wt.% LiTFSI-PMEMA and 1 wt.% PTFE"* 와 정합.
- 부피 (우리 산수 · 가정: LPSCl 1.86 g cm⁻³ = a 9.86 Å [Kraft] 중성자값에서 · PTFE 2.2 · 고분자 1.1–1.3 g cm⁻³): 고체 중 **LPSCl ≈93 vol% · LiTFSI-PMEMA ≈5.6–6.6 vol% · PTFE ≈0.8 vol%**. 고분자를 입자 표면에 고르게 바르면 두께 **≈10–36 nm** (d = 1–3 µm) → cryo-TEM 의 ≈7 nm 는 **양적으로 가능**하다(나머지는 틈에 고였거나 입자가 더 잘다).
- 비교 (`Fig. 1d` · `Table S3`): 건식 황화물막 13편 중 **가장 얇다**(직전 최박 S13 = 20 µm · 1.0 mS cm⁻¹). σ 는 S8 (40 µm · 8.4) · S10 (30 µm · 8.4) · S11 (30 µm · 6.5) 보다 **낮다**. ⭐ **S10 = Li₅.₄PS₄.₄Cl₁.₆ (우리 modelc 조성) · PTFE 0.2 % · 30 µm · 8.4 mS cm⁻¹** (ref 34 = Zhang 2021 *Nano Lett.* 21, 5233). ⚠ INDEX '실험값' 시트의 같은 편 행은 *10.8 mS/cm* — 막/분말 차인지 미확인.

### 3b. 이온·전자 수송 (`Fig. 2a,b`, `Fig. S13`, `Table S2`)

| 시료 | σ_ion (30 °C) | Ea (30–90 °C 아레니우스) | σ_e (DC 0.5 V · 3600 s) |
|---|---|---|---|
| pristine LPSCl | **3.23 mS cm⁻¹** | **0.24 eV** | **2.64×10⁻⁹ S cm⁻¹** |
| LPSCl-PTFE 전구막 (1 wt%) | **2.67 mS cm⁻¹** (p.2) | n/a | n/a |
| LPSCl-PTFE 막 (5 wt%) | **0.42 mS cm⁻¹** | **0.32 eV** | **7.04×10⁻¹⁰** |
| LPSCl-LiTFSI-PMEMA (5 wt%) | **1.81 mS cm⁻¹** | **0.28 eV** | **3.31×10⁻¹⁰** |
| **USF** | **1.56 mS cm⁻¹** | **0.29 eV** | **4.12×10⁻¹⁰** |
| LiTFSI-PMEMA 막 | **1.04×10⁻⁴ S cm⁻¹** (RT) | n/a | n/a |

- `Fig. 2a` 기울기 재검 (우리 산수, figure-read 끝점): LPSCl Δlog σ ≈0.65 / Δ(1000/T) 0.55 → ≈0.23 eV · PTFE ≈0.31 · USF ≈0.28 · LiTFSI-PMEMA ≈0.29 eV — 범례 값과 정합. ⚠ **Ea 오차막대 없음**(7 점 · 30–90 °C). 0.28 / 0.29 는 구별 불가 수준.
- σ 비 vs Ea 차 (우리 산수): USF/PTFE5 = **3.7** ↔ exp(0.03 eV/kT) = 3.2 (정합) · LPSCl/USF = **2.1** ↔ exp(0.05/kT) = 6.8 → USF 의 전인자가 ~3 배 커야 맞는다 (보상 효과 또는 맞춤 잡음).
- ⚠ **USF(1.56) < 전구막(2.67) < pristine(3.23)** — 전도성 바인더 4 wt% 를 **더했더니 σ 가 42 % 내려갔다**. "향상" 은 5 wt% PTFE(0.42) 대비일 때만 참이다 (§10-①).
- ⚠ σ 측정 셀(전극·압력·두께 실측법)은 **Experimental 에 없다**.

### 3c. ⁷Li ssNMR · cryo-TEM (`Fig. 2c,d`, `Fig. S14`)

| 항목 | 값 | 비고 |
|---|---|---|
| LPSCl | **1.35 ppm** (날카로움) | 1 M LiCl 기준 · MAS 10 kHz · π/2 2.0 µs · 지연 5 s · 64 회 |
| LiTFSI-PMEMA | **−1.14 ppm** (주) + **0.36 ppm** (어깨) | "고분자 관련 Li 환경" 으로 뭉뚱그려 배정 |
| USF 중간 성분 | **≈0.88 ppm** (넓음) | *"unresolved broadened … not direct evidence for a discrete interfacial Li⁺ species"* (저자 스스로) |
| USF 면적 분율 | LPSCl 관련 **68.9 %** · 중간 **21.7 %** · 고분자 관련 **9.4 %** | 저자: *"used only to describe the relative spectral contributions"* |
| cryo-TEM 피막 | **≈7 nm** 컨포멀 LiTFSI-PMEMA 층 (`Fig. 2d`) | JEOL JEM-F200 · 200 kV · ≈−180 °C · 글러브박스 절편 · 밀폐 이송 |

- 🔴 **화학양론 검산 (우리 산수)**: USF 의 Li 중 LiTFSI 가 가진 몫 = 0.00418 / (2.1248 + 0.00418) = **0.196 %**. "고분자 관련" **9.4 %** 는 그 **≈48 배**다 — 이완 지연(5 s)은 신호를 **줄이는** 쪽이라 이 차를 만들 수 없다. ⇒ −1.1 ppm 근처 성분은 고분자 Li 만이 아니다 (§10-③).

### 3d. DFT 장벽 (`Fig. 2f` 인쇄값 · 본문 p.6)

| 경로 | 장벽 | `Fig. 2f` 이미지별 에너지 (인쇄값, eV) | 그림 |
|---|---|---|---|
| LPSCl 벌크 | **0.55** | 0 · 0.16 · 0.28 · 0.42 · **0.55** · 0.44 · 0.37 · 0.13 · 0 | `Fig. S15` |
| LPSCl/LiTFSI-PMEMA 접촉부 | **0.85** | 0 · 0.26 · 0.50 · 0.70 · **0.85** · 0.67 · 0.45 · 0.21 · 0 | `Fig. 2e` |
| LiTFSI-PMEMA 상 | **1.20** | 0 · 0.42 · 0.74 · 1.01 · **1.20** · 0.92 · 0.71 · 0.33 · 0 | `Fig. S16` |

- **중간 이미지 7개 + 끝점 2개**(검은 막대, 세 곡선 공통 0.00). Methods 는 **"Four intermediate images"** (SI p.5) — 불일치.
- 홉 수 검산 (303.15 K · ν₀ 10¹³ s⁻¹ **가정** · `hop_check`): **0.55 eV → Γ ≈ 7.2×10³ s⁻¹ · 1/Γ ≈ 0.14 ms** / **0.85 eV → Γ ≈ 7.4×10⁻² s⁻¹ · 1/Γ ≈ 13.5 s** (1 h 동안 N ≈ 2.7×10²) / **1.20 eV → Γ ≈ 1.1×10⁻⁷ s⁻¹ · 1/Γ ≈ 8.9×10⁶ s ≈ 103 일** (대칭셀 1200 h 동안 N ≈ 0.5). 비교: 자기 실측 Ea **0.24 eV → 1/Γ ≈ 1.0 ns** · 0.29 eV → 6.6 ns. ⚠ 차수 검산이지 D·σ 가 아니다.

### 3e. 기계 (`Fig. 1g–i` · 본문 p.4 · Hysitron TI 980 · Oliver–Pharr)

| 시료 | Er | H | 소산 효율 | 최대 깊이 (figure-read) |
|---|---|---|---|---|
| LPSCl 냉간 펠릿 | figure-read ≈0.49 GPa | figure-read ≈30 MPa | **43.5 %** | ≈2.4 µm |
| LPSCl-PTFE 전구막 | **0.22 ± 0.021 GPa** | **12.56 ± 1.23 MPa** | **44.3 %** | ≈2.9 µm |
| **USF** | **0.038 ± 0.004 GPa** | **5.14 ± 0.37 MPa** | **47.7 %** | ≈4.7 µm |

- 최대 하중 figure-read ≈1.5 mN. 압입 깊이 2.4–4.7 µm ≈ **입자 크기(1–3 µm)** → 단결정 탄성이 아니라 **다공 성형체·막의 국소 응답**이다. ⛔ DFT 탄성과 비교 금지 (§7).
- 소산 효율 차(43.5 → 47.7 %)에 오차막대 없음.

### 3f. CV · 공기 · 열 (`Fig. S12`, `Fig. S17`, `Fig. S7`)

| 항목 | 값 | 비고 |
|---|---|---|
| 산화 개시 (CV 0.1 mV s⁻¹ · SE+CB 9:1 ‖ SE ‖ LiIn) | 본문 **"∼2.6 V vs Li/Li⁺"** (두 시료 동일) | figure-read: 산화 봉우리 LPSCl ≈2.65 V / USF ≈2.52 V · 개시 ≈2.3–2.4 V. 축 기준전극 표기 없음 (본문은 Li 눈금) |
| 산화 전류밀도 | LPSCl **6.4** vs USF **3.7 mA g⁻¹** | g 의 분모(SE? 복합체?) 미기재. 환원 전류도 USF 가 작다 (0 V figure-read ≈ −27 vs −37 · 2.0 V ≈ −1.8 vs −3.8 mA g⁻¹) |
| H₂S (30 °C · RH 20 % · 40 min) | figure-read pristine ≈1.39 · USF ≈1.19 cm³ g⁻¹ | 분말 vs 막 비교 · 저자도 "slightly" |
| 고분자 열분해 개시 | **239 °C** (TG, Ar, 5 °C min⁻¹) | 열압연 100 °C ≪ 239 °C |
| GPC (PS 표준) | Mn **28.4** · Mw **90.7 kg mol⁻¹** · Đ **3.19** · DPn **≈197** | 28 400/197 = **144.2 g mol⁻¹ = MEMA 단위체**(C₇H₁₂O₃ 144.17) (우리 산수) |

### 3g. 셀 (`Fig. 3`–`Fig. 5`, SI pp.3–4)

| 셀 | 조건 | 결과 |
|---|---|---|
| LiIn‖LPSCl-PTFE‖LiIn CCD | RT · 75 MPa | **0.9 mA cm⁻²** |
| LiIn‖USF‖LiIn CCD | 〃 | **2.2 mA cm⁻²** · 과전압 **<170 mV** |
| 대칭셀 정전류 | 0.5 mA cm⁻² · 0.5 mAh cm⁻² · RT | PTFE: **212 h 단락** · USF: **>1200 h**. figure-read 분극 ≈±0.15 V (PTFE) vs ≈±0.05 V (USF) |
| LCO‖SSE‖LiIn 율속 | 30 °C · LCO 8.0 mg cm⁻² (`Fig. 4d` 표기) · CO₂ 처리 LPSCl 양극 · 2.6–4.5 V (Li 눈금) | USF **161.6 / 153.5 / 139.4 / 124.7** (0.1/0.2/0.5/1 C) · 복귀 0.1 C **160.1** · PTFE **145.2 / 127.9 / 100.1 / 74.6 mAh g⁻¹** |
| LCO 장기 | 0.5 C · 30 °C | USF ICE **92.5 %** · **80 % @ 928 cycles** · **70.3 % @ 1500** · PTFE ICE **86.1 %** · **236 cycles 단락** (`Fig. S20`) |
| 압력 모니터 | 첫 10 사이클 | PTFE: 피크 압력 **≈0.18 MPa** 감소 (`Fig. 4e`) · USF: "negligible" (⚠ §10-⑨) |
| 계면저항 (EIS) | 5→100 cycles | figure-read PTFE ≈460→785 Ω · USF ≈260→288 Ω (`Fig. S21c`, Ω 그대로, 0.785 cm²) |
| NCM721‖USF‖nSi | LiNbO₂(원문 표기)-코팅 NCM721 · 10.2 mg cm⁻² · N/P 1.2 · 2.0–4.3 V · 30 °C | **185.2 / 174.4 / 158.0 / 137.8 mAh g⁻¹** · 0.5 C **300 사이클 81.3 %** · 에너지밀도 **366.8 Wh kg⁻¹** (양극+음극+전해질 질량) |
| 파우치 | CIP 조립 · 10 MPa 철판 체결 | **>40 사이클 @0.1 C**(본문) · **322.7 Wh kg⁻¹ 스택** · ⚠ `Fig. 5e` 는 "0.5C" 표지로 80 사이클 (§10-⑩) |

---

## 4. 재료 & 방법 — 원문 전부 (SI pp.3–6)

### 4a. 바인더 합성
MEMA(2-methoxyethyl methacrylate, Macklin ≥98 %) : LiTFSI(Innochem) = **7:3 (질량)** 불활성 분위기 혼합 → AIBN **1 mol%(vs MEMA)** → RT 2 h 교반(LiTFSI 완전 용해) → PTFE 몰드 캐스팅 → **70 °C 12 h 열중합** → LiTFSI-PMEMA 막. FTIR(`Fig. S3`): MEMA 의 C=C **1643 cm⁻¹** 소실 · GPC(`Fig. S4`, `Table S1`). Tg = **14 °C** (ref 34 인용 — 자체 측정 아님).

### 4b. 막 제작
건조 PTFE(Sigma) : LPSCl = **1:99** (대조막 **5:95**) → 마노 유발로 반죽 → **100 °C 롤압** → 전구막. 전구막 + LiTFSI-PMEMA 막을 **96:4** 로 적층 → **반복 접기 + 100 °C 열압연 40 회** → USF. 본문: *"the final USF thickness is not determined by the simple sum … but by the densification and lateral extension"*.

### 4c. 전극
- LCO 양극: LPSCl 을 **CO₂ 100 mL min⁻¹ · 1 h** 노출(Li₂CO₃ 표면층, ref 56) → LCO(Aladdin):CO₂-LPSCl = 7:3 → PTFE **0.2 wt%** → 평판 롤압.
- NCM721 양극: "LiNbO₂"-코팅 NCM721(구이린 전기과학연구원) : LPSCl = 7:3 + PTFE 0.2 wt% → 롤압. (원문 그대로 *LiNbO₂* — LiNbO₃ 오기로 보인다.)
- nSi 음극: 나노 Si(Aladdin) 전리튬화(SI ref 1) → PTFE 1 wt% → 열판 롤압.

### 4d. 셀
ZrO₂ 라이너 몰드(⌀10 mm) · SS 스탬프 **0.7854 cm²** · SE+C 셀은 SE:CB = **9:1** · 펠릿: LPSCl **80 mg · 100 MPa 1 min**, 전극 **370 MPa 3 min** · 운전 **75 MPa**. 막형: 100 °C · 75 MPa 적층 · N/P 1.2 · 운전 75 MPa. **대칭셀·LCO 셀은 RT 단계 냉간압착** (막·LiIn 각각 75 MPa 3 min 선가압 · *"No hot pressing or thermal lamination"*). 파우치: 적층·밀봉 · 철판으로 **10 MPa**. 글러브박스 O₂·H₂O < 0.1 ppm.

### 4e. 측정
EIS 7 MHz–100 mHz · 10 mV · CV Biologic SP-200 **0.1 mV s⁻¹** · 사이클 Neware **30 °C** · SEM Hitachi S-4800 · XPS ESCALAB 250Xi (Al Kα 150 W) · Raman LabRAM HR Evolution 532 nm · FTIR ALPHA II ATR · XRD D8 Advance Cu Kα 10–80° · 압력 DAYSENSOR DYHW-116 · MIP AutoPore V 9620 (⌀10 mm 원판 총 ≈1.5 g · 대기 노출 <1 min · *"apparent Hg-accessible porosity"*; SI p.6 *"upturn observed at ~105 nm"* — `Fig. 1e` 로 보면 **~10⁵ nm** 의 윗첨자 소실) · GPC Agilent 1260 · TG Hitachi STA200.

### 4f. 이론 (SI pp.4–5, 페이지 렌더로 원문 대조 — 전문)
> *"Spin-polarized density functional theory (DFT) calculations[2,3] were performed using the Vienna ab initio simulation package (VASP) with plane-wave basis sets and the projector-augmented wave (PAW) method.[4,5] The exchange-correlation interactions were described by the generalized gradient approximation (GGA) using the Perdew-Burke-Ernzerhof (PBE) functional.[6] Van der Waals interactions were included using the Grimme DFT-D3 correction.[7,8] A 3 × 3 × 3 supercell of Li₆PS₅Cl was constructed to investigate Li⁺ migration in the bulk phase. To model Li⁺ migration across the Li₆PS₅Cl/LiTFSI-PMEMA interface, a five-layer slab of the Li₆PS₅Cl (100) surface based on a 3 × 3 supercell was employed, with a vacuum layer of 20 Å to avoid interactions between periodic images. During structural relaxation, the top three layers were fully relaxed while the bottom two layers were fixed. The plane-wave energy cutoff was set to 550 eV. Brillouin zone sampling was performed using a Γ-centered Monkhorst-Pack mesh with a 1 × 1 × 1 grid for geometry optimizations and a 3 × 3 × 1 grid for single-point calculations.[8] The electronic energy convergence criterion was set to 10⁻⁵ eV with a Gaussian smearing of 0.01 eV, and the force convergence threshold was 0.02 eV Å⁻¹. Li⁺ migration pathways and activation energies were calculated using the climbing-image nudged elastic band (CI-NEB) method.[9] Four intermediate images were generated between the initial and final states via linear interpolation and subsequently optimized."*

- SI ref [7] = Grimme 2010 (D3) · **[8] = Monkhorst–Pack 1976** → D3 인용 "[7,8]" 의 [8] 은 **오인용** · [9] = Henkelman 2000 (CI-NEB).
- ⛔ **`Fig. S16` 의 고분자 단독 계산은 이 문단에 없다** — 모형·셀·진공·전하 모두 0 줄.

---

## 5. 결과 — 섹션별 상세 (그림 실독)

### 5.1 막 제작과 구조 (`Fig. 1`, `Fig. S5`, `Fig. S6`, `Fig. S8`)
- `Fig. 1a` 공정 만화: (위) 전구막 롤압 + 70 °C Ar 에서 고분자 캐스팅 → (아래) **LPSCl-PTFE / LiTFSI-PMEMA / LPSCl-PTFE 샌드위치를 100 °C 롤 사이로** → 접기 → 반복 → USF. 확대 원은 LPSCl 구 사이에 하늘색 고분자 리본과 분홍 PTFE 섬유를 그린다.
- `Fig. 1b` 윗면 SEM 은 매끈 · `Fig. 1c` 단면 18 µm (점선) + EDS S·C·O·F 가 막 전체에 고르게.
- `Fig. S6`: 전구막(a)·고분자 단독막(c)은 윗면·단면에 **Voids** 표지. USF(d) 는 윗면 치밀, 단면엔 **"PTFE fiber network"** 화살표 — ⚠ 단면에서 보이는 망은 **PTFE** 이지 LiTFSI-PMEMA 가 아니다.
- `Fig. 1e` MIP: 전구막은 ≈800 nm 에 높은 봉우리(figure-read ≈0.41 mL g⁻¹) + >10⁵ nm 치솟음 · USF 는 ≈150 nm 봉우리(≈0.175) 하나. `Fig. 1f` 기공률 34.99 → 14.36 %.
- 본문 기전 해석: *"lamination during hot-rolling process is mainly enabled by pressure-assisted contact and mechanical accommodation"* (TG 239 °C ≫ 100 °C 라 고분자는 녹지 않는다).

### 5.2 화학 호환성 (`Fig. S9`–`Fig. S11`)
- XRD: 세 시료 모두 ICSD 97-041-8490 Li₆PS₅Cl 패턴 + 18° 부근 넓은 혹(밀폐 홀더 배경으로 보임). Raman(`Fig. S10`, 손 크롭): PS₄³⁻ ≈425 cm⁻¹(figure-read) 주봉 + ≈197·265·575·600 cm⁻¹ 부봉, 새 봉우리 없음. XPS P 2p: PS₄³⁻ 이중선만.
- ⚠ 셋 다 **벌크·결정 민감** — 수 nm 비정질 반응층·소량 비정질화는 못 본다(§10-③ 의 NMR 과 연결).

### 5.3 CV — 산화 개시 (`Fig. S12`)
- 0–5 V 한 바퀴. 0 V 근처 큰 환원 + 0.07 V 산화 봉우리(Li 석출/박리로 보인다), 2.0 V 환원 봉우리, **2.5–2.65 V 산화 봉우리**, LPSCl 은 3.4 V 부근 두 번째 혹(figure-read).
- 본문: 개시 **"∼2.6 V"** 동일 → *"onset potential is primarily determined by the LPSCl bulk"*; 전류 감소(6.4 → 3.7 mA g⁻¹)를 *"increases the kinetic resistance against electrolyte oxidation"* 로 해석. ⚠ 환원 전류도 같이 줄었다 → 피복이 **LPSCl|C 접촉 면적**을 줄인 것으로도 같은 그림이 나온다 (§10-⑥).

### 5.4 이온·전자 전도 (`Fig. 2a,b`, `Fig. S13`, `Table S2`)
- `Fig. 2a`: log σ (−3.5 ~ −1.0) vs 1000/T (2.75–3.30 K⁻¹, 90–30 °C) · 4 직선 · 각 7 점. 위에서부터 LPSCl > LiTFSI-PMEMA 막 ≳ USF ≫ PTFE 5 % 막.
- `Fig. 2b`: 막대 — 이온(왼축 mS cm⁻¹ 0–5) · 전자(오른축 10⁻¹⁰ S cm⁻¹ 0–30, 빗금). 본문 값과 일치.
- `Fig. S13` (원본 크기): 0.5 V DC · 3600 s 감쇠 곡선 + 네 σ_e 인쇄값. ⚠ 색이 `Fig. 2` 와 다르다(USF 가 살구색, LPSCl 이 회녹색) — 그림 간 대조 때 주의.
- `Table S2`: 문헌 고분자 전해질 15종(대부분 SN·IL·가소제 포함) vs **LiTFSI-PMEMA 1.04×10⁻⁴ S cm⁻¹ (첨가제 없음)** · 표 제목의 "elevated-temperature" 행은 **없다**(전부 20–30 °C·RT).

### 5.5 ⁷Li ssNMR (`Fig. 2c`)
- 아래(분홍) 고분자: −1.14 ppm 넓은 주봉 + 0.36 ppm 날카로운 봉. 가운데(살구) LPSCl: 1.35 ppm. 위(파랑) USF: 1.35 ppm 주봉 + **0.88 ppm 어깨(파랑 채움)** + **−1.1 ppm 작은 봉(분홍 채움)**. 원그래프 68.9 / 21.7 / 9.4 %.
- 저자 해석은 조심스럽다 — 중간 성분을 *"intermediate/broadened spectral component rather than direct evidence for a discrete interfacial Li⁺ species"* 로 둔다. 그러나 §3c 화학양론상 **9.4 % 를 '고분자 관련' 으로 부르는 것 자체가 무리**다.

### 5.6 cryo-TEM (`Fig. 2d`, `Fig. S14`)
- 왼쪽: LPSCl 입자 가장자리에 점선으로 그은 **≈7 nm 띠 "LiTFSI-PMEMA"**. 오른쪽: LPSCl 영역 FFT — 점선 원에 (331)·(220)·(200)·(620) 라벨.
- 🔎 **FFT 지표 검산 (figure-read · 우리 산수)**: 축척 막대 "5 1/nm" 로 재면 (620) 원 ≈6.4 nm⁻¹ → d ≈1.56 Å = 계산 d₆₂₀ 1.559 Å (a 9.86 Å) **✓**. 그런데 **"(331)" 원은 ≈2.0 nm⁻¹ → d ≈4.9–5.1 Å = d₂₀₀(4.93 Å) 자리**, **"(200)" 원은 ≈3.9 nm⁻¹ → d ≈2.55 Å** (d₄₀₀ 2.47 · d₃₃₁ 2.26 Å 쪽) → 두 라벨(색)이 **뒤바뀐 것으로 보인다**. "(220)" ≈3.7 Å 는 d₂₂₀ 3.49 Å 와 ≈7 % 차 (원 중심 판독 ±5 % 감안하면 경계).
- ⚠ 7 nm 층의 **화학 정체**는 영상 대비로만 정했다 — 그 층을 가로지르는 EDS/EELS 선분석이 없다. `Fig. S14` EDS 는 500 nm 축척이라 7 nm 를 못 가른다.

### 5.7 DFT (`Fig. 2e,f`, `Fig. S15`, `Fig. S16`) — 상세는 §6
- 본문 p.6 원문: *"The calculated migration barriers follow the hierarchy: LPSCl bulk (0.55 eV) < model LPSCl/LiTFSI-PMEMA contact region (0.85 eV) < LiTFSI-PMEMA phase (1.20 eV) (Figure 2f). The DFT-calculated migration barriers represent local Li⁺ hopping barriers along selected pathways and should not be directly equated with the experimentally derived apparent activation energies from Arrhenius plots (Figure 2a)."* · *"…the contact region may act as a local Li⁺ transfer region between the ceramic and polymer phases. However, this DFT result should not be interpreted as direct proof that the entire 0.88 ppm ssNMR component originates from a discrete interfacial Li⁺ population."*

### 5.8 수송 모형 (`Fig. 2g`)
- 막 조각 만화 + 확대 원: 경로 I(LPSCl 안, 점선) · II(LPSCl→고분자 경계) · III(고분자 안). 결론부: *"LiTFSI-PMEMA … serving not only as a mechanical scaffold but also as an active ionic mediator facilitating a continuous Li⁺ percolation network."* — ⚠ 이 마지막 문장은 §6.2 홉 수 검산과 맞지 않는다.

### 5.9 공기 안정성 (`Fig. S17`)
- H₂S 누적: 40 min 에 pristine ≈1.39 vs USF ≈1.19 cm³ g⁻¹ (figure-read, ≈14 % 감소). 분말 vs 치밀막이라 비표면적부터 다르다 — 본문도 *"slightly improves"*.

### 5.10 대칭셀 (`Fig. 3`, `Fig. S18`, `Fig. S19`)
- `Fig. 3a,b`: 계단 전류(오른축 mA) · PTFE 는 ≈17·19 h 에 전압 튐 → CCD 0.9 · USF 는 ≈46 h 까지 버티다 2.2 mA cm⁻² 에서 튐.
- `Fig. 3c`: 1200 h · 삽입 확대 50–70 h · 200–220 h(PTFE 212 h 단락이 보인다) · 1100–1120 h.
- `Fig. 3d–g`: 200 h 후 단면 — PTFE 쪽 **Gaps·Cracks** + 만화(수지상이 균열로) / USF 쪽 치밀 + 만화(초록 고분자 망 위로 균일 Li⁺).
- 🔎 (우리 산수) 막의 **벌크 이온저항**은 USF 1.15 Ω cm² · 전구막 0.75–1.12 Ω cm² · 5 % PTFE 막(30 µm 가정) 7.1 Ω cm² → 0.5 mA cm⁻² 에서 **0.4–3.6 mV**. 실제 분극 ≈50 mV(USF)·≈150 mV(PTFE)(figure-read) = **100–300 Ω cm²** → 막 벌크 몫은 **≤1–4 %**. ⇒ 대칭셀 차이는 **계면·접촉** 차이지 막 σ 차이가 아니다 (§10-⑤).
- `Fig. S18` OCV 노화: 조립 직후 반원이 ≈200 Ω 까지 → 3·5 일 후 ≈70 Ω 로 **줄어든다**(figure-read, 접촉 개선 쪽). 고주파 절편 ≈40 Ω (figure-read) — σ 1.56 mS cm⁻¹·18 µm·0.785 cm² 로 기대되는 막 저항 **≈1.5 Ω 의 ≈27 배** (설명 없음).
- `Fig. S19` XPS (노화 셀의 USF): C 1s C–Fₓ·C=O·C–O–C·C–C · F 1s **C–Fₓ 하나(≈689.5 eV, LiF 봉 없음)** · P 2p PS₄³⁻ 만 → *"negligible PTFE reduction"* 의 근거.

### 5.11 LCO 셀 (`Fig. 4`, `Fig. S20`–`Fig. S22`)
- `Fig. 4a–c` 율속·곡선: USF 쪽이 모든 율속에서 분극 작고 용량 크다(본문 수치와 정합). 곡선 전압축 2.6–4.5 V · 평탄 ≈3.9 V → **Li 눈금으로 환산**된 값.
- `Fig. 4d` (확대): USF 0.5 C 초기 ≈135–140 → 1500 사이클 ≈95 mAh g⁻¹ · 점선(≈107) 을 ≈900 사이클 부근에서 지난다. PTFE 는 **≈100–104 mAh g⁻¹ 로 거의 평탄**하다가 ≈236 사이클 단락 — 본문의 *"rapid capacity fading"* 은 그림에서 **안 보인다** (§10-⑨).
- `Fig. 4e,f` 압력(오른축 MPa)·전압: PTFE 는 피크 압력이 ≈0.45 → ≈0.27 MPa 로 내려앉는다(Δ = 0.18 MPa 화살표) · USF 는 **사이클마다 0 → ≈0.4 MPa 를 오르내리되 피크가 일정**(figure-read). 본문 *"negligible pressure variation"* 은 **표류(drift)** 에만 맞다.
- `Fig. 4g,h` 200 사이클 후 단면: PTFE 막에 Cracks · USF 무균열.
- `Fig. S21` EIS: 반원 지름 PTFE 460 → 785 Ω · USF 260 → 288 Ω (figure-read) · `Fig. S22` 200 번째 곡선 PTFE ≈101 vs USF ≈138 mAh g⁻¹.

### 5.12 고에너지 셀·파우치 (`Fig. 5`, `Fig. S23`, `Fig. S24`)
- `Fig. 5a` 단면 nSi / USF / NCM721 + EDS Si·S·Ni. 🔎 **점선 사이 USF 띠 ≈79 px, 축척 20 µm = 128 px → ≈12 µm** (figure-read, 원본 래스터) — 명목 18 µm 보다 얇다 (100 °C·75 MPa 적층 압밀? 점선 위치 오차? — 저자 언급 없음).
- `Fig. 5b,c`: 0.1–1 C 곡선 · 300 사이클 81.3 % (초기 0.5 C ≈158 → ≈128 mAh g⁻¹, figure-read).
- `Fig. S23` (원본 크기): 전압별 in-situ EIS(3.3→4.3 V 충전 · 4.0→2.5 V 방전) + DRT τ1–τ4. τ4(저주파)만 SOC 따라 크게 변하고 τ2·τ3 는 4.2–4.3 V 에서도 안 자란다.
- `Fig. 5d,e` 파우치: CIP 조립 · 용량(mAh) vs 사이클 — §10-⑩.

---

## 6. NEB 감사 ★★★ (사용자 요청 핵심)

### 6.1 무엇을 어떻게 계산했나 — 전 항목

> 원문 = SI p.4–5 문단(§4f) · 본문 p.6. **그림 판독** = `Fig. 2e,f`·`Fig. S15`·`Fig. S16` 원본 래스터 확대. 없는 것은 **미기재**.

| 항목 | LPSCl 벌크 (`Fig. S15`) | 접촉부 (`Fig. 2e`) | 고분자 상 (`Fig. S16`) |
|---|---|---|---|
| 코드 | VASP (버전 **미기재**) | 〃 | 〃 (방법 문단에 이 계산 자체가 **없다**) |
| 범함수 | GGA-PBE + **Grimme D3** (감쇠형 미기재 · ref 7 = 2010 원판 D3) · **스핀분극** | 〃 | 〃 (추정) |
| PAW | PAW (전위 세트·Li_sv 여부 **미기재**) | 〃 | 〃 |
| ecut | **550 eV** | 〃 | 〃 (추정) |
| k점 | 구조 이완 **Γ 1×1×1** · 단일점 **3×3×1** (벌크에 3×3×1 을 썼는지, NEB 에너지가 Γ 값인지 단일점인지 **미기재**) | 〃 (3×3×1 은 슬랩용 꼴) | **미기재** |
| 셀 | 원문 **"3 × 3 × 3 supercell"** (원자 수 미기재 · 정육면체 단위포면 52×27 = **1404 원자**, 원시포면 13×27 = 351 원자 · 어느 쪽인지 미기재). 🔎 **그림은 정육면체 점선 셀 1개만** — 그 안의 Cl 이 모서리 8 + 면심 6 (= 단위포 1개분 4개)뿐이라, 그려진 셀은 단위포 1개(a ≈9.9 Å · 52 원자 규모). 3×3×3 이면 27 배가 보여야 한다 | 원문 **"(100) 5층 슬랩 · 3 × 3 supercell · 진공 20 Å · 위 3층 이완 / 아래 2층 고정"**. 🔎 그림의 주기 폭 = 투영 P–P 간격 **2개** ≈ **a(≈9.9 Å)** 1칸, 슬랩 두께 대략 ≈8 Å (투영 기울기 때문에 대략) | **미기재**. 🔎 점선 상자 안 고립 올리고머 1개 — 사슬이 상자 높이의 **≈90 %** 를 차지 |
| 격자상수 | **미기재** (실험값 고정? 이완? — 미기재) | 〃 | 해당 없음 |
| 이온 이완 | 힘 **0.02 eV Å⁻¹** · 에너지 **10⁻⁵ eV** · Gaussian **0.01 eV** | 〃 + 위 3층만 | 〃 (추정) |
| NEB 방식 | **CI-NEB** (Henkelman 2000) · **선형 보간** | 〃 | 〃 |
| 이미지 수 | 원문 **"Four intermediate images"** ↔ 🔎 `Fig. 2f` **7개** | 〃 | 〃 |
| 스프링 상수 · NEB 힘 수렴 · CI 수렴 확인 | **미기재** | 〃 | 〃 |
| 이동 기구 | **미기재** (공공? 격자간? 48h 반점유 자리 사이 재배치?) | Li 가 **슬랩 표면 → 고분자 에스터 O 쪽**으로 이동 (`Fig. 2e` 세 컷) | Li 가 **에스터 O 여럿의 우리(cage) → 위쪽 사슬 O** 로 (`Fig. S16` 세 컷) |
| 경로 끝점 | **미기재** (48h/24g 표기 없음). 🔎 궤적 = 겹친 Li 구 ≈10 개, 길이 ≈셀 모서리의 0.6–0.8 배 = **≈6–8 Å** (투영) | 슬랩 표면 Li ↔ 고분자 배위 자리 (그림) | 다배위 O 우리 ↔ 저배위 자리 (그림) |
| 전하 상태 | **미기재** ("Li⁺" 라 부름 · 배경전하·NELECT 언급 없음) | **미기재** · TFSI⁻ 없음 | **미기재** · **반대이온 없음** + 스핀분극 → **중성 Li 원자(라디칼)** 일 수 있다 |
| 무질서 처리 | **미기재**. 🔎 Cl 4개가 전부 **모서리+면심 부격자(4a)** = **완전 정렬**(ICSD 배열) | 슬랩도 정렬 단위포로 보인다 (범례에 Cl 없음 — 작은 진녹 구는 있다) | 해당 없음 |
| 바인더 모형 | — | 범례 **Li·P·S·C·O 뿐** — **N·F 없음 = TFSI⁻ 없음**. 그림 제목 **"PMEMA"**. 메타크릴레이트 **3단위** 올리고머 1개, 슬랩 위에 **수직으로 서 있다** | 범례 **C·H·O 뿐**. 같은 3단위 올리고머(형태 다름) · **TFSI⁻ 없음** · 이웃 사슬 없음 · 진공 속 |
| 사슬 화학 | — | 🔎 곁사슬 셋 중 둘은 **–C(=O)O–CH₂CH₂–O–CH₃** (= MEMA ✓) · 가운데 하나는 **에테르 O 4–5 개가 일렬인 올리고(EO) 사슬**(끝은 에틸) — **PMEMA 에 없는 구조** | 〃 (긴 사슬 그대로) |
| 결과 | **0.55 eV** | **0.85 eV** | **1.20 eV** |
| 프로파일 | 9 점 · 최고점 = 정가운데 이미지 · 중간 극소 없음 · 끝점 0.00/0.00 | 〃 · 끝점 0.00/0.00 | 〃 · 끝점 0.00/0.00 |

### 6.2 논리에 모순은 없나

**(a) 장벽 ↔ 주장하는 수송 이득 — 홉 수 검산 (`D-2026-09-27-barrier-hop-count`)**

> 홉 수 검산 (ν₀ 10¹³ s⁻¹ **가정** · 303.15 K = 측정 온도 30 °C): **0.55 eV** Γ ≈ 7.2×10³ s⁻¹ · 1/Γ ≈ 0.14 ms · **0.85 eV** Γ ≈ 7.4×10⁻² s⁻¹ · 1/Γ ≈ 13.5 s · **1.20 eV** Γ ≈ 1.1×10⁻⁷ s⁻¹ · 1/Γ ≈ 8.9×10⁶ s (≈103 일; 1200 h 시험 전체 동안 N ≈ 0.5). 자기 실측 Ea **0.24 eV** → 1/Γ ≈ 1.0 ns · **0.29 eV**(USF) → 6.6 ns.

- **고분자 상 1.20 eV ↔ 자기 측정 σ(LiTFSI-PMEMA) = 1.04×10⁻⁴ S cm⁻¹**: Nernst–Einstein 으로 거꾸로 풀면 (우리 산수 · 가정: 홉 길이 2.25–3 Å · 3D 무상관 · Haven 1 · LiTFSI 의 Li 전부 이동 · 고분자 밀도 1.2 g cm⁻³) 필요한 홉 빈도 **Γ ≈ 1.5–2.7×10⁸ s⁻¹** (= ν₀ 10¹³ 기준 유효 장벽 ≈0.28–0.29 eV). 1.20 eV 는 **10¹⁵ 배** 느리다 → 그 장벽이 맞으면 σ ≈ **8×10⁻²⁰ S cm⁻¹**. Haven 비가 1이 아니어도([Adeli19] H_R ≈0.3 · [Marc17NE]) **몇 배**일 뿐 10¹⁵ 를 못 메운다. ⇒ **1.20 eV 는 이 고분자의 이온 수송을 기술하지 않는다.**
- **벌크 0.55 eV ↔ 자기 측정 σ(LPSCl) = 3.23 mS cm⁻¹**: 같은 역산(n_Li = 24/a³ · a 9.86 Å [Kraft]) → 필요 Γ ≈ 1.4–2.5×10⁸ s⁻¹ (유효 ≈0.28–0.29 eV). 0.55 eV 는 **2×10⁴ 배** 느리다 → σ ≈ **1.7×10⁻⁷ S cm⁻¹** 예측. 독립 대조: [dK16Arg] 가 인용한 ⁷Li NMR 점프율 **~1×10⁹ s⁻¹ @350 K** ↔ 0.55 eV 의 350 K Γ ≈ **1.2×10⁵ s⁻¹** (우리 산수) — 역시 10⁴ 배.
- **접촉부 0.85 eV ↔ "neighboring SSE particles 사이 연속성을 돕는다"**: 그 접촉부가 전류 경로에 직렬로 끼면 (우리 산수 · 가정: 계면 Li 자리 10¹⁵ cm⁻²) 교환전류 ≈1×10⁻⁵ A cm⁻² · 접촉 하나 **≈2×10³ Ω cm²** — 막 전체 벌크 ASR **1.15 Ω cm²** 의 10³ 배. ⇒ 0.85 eV 접촉부는 **다리가 아니라 벽**이다. 저자의 "LPSCl 주도" 결론과는 맞지만, "보조"·"mediator" 는 이 숫자에서 나올 수 없다.

**(b) 0 K 한 홉 장벽을 실측 Ea·σ 와 같은 양처럼 쓰나**
- **반은 지켰다** — 본문이 명시적으로 *"should not be directly equated with the experimentally derived apparent activation energies"* 라 썼다(심사 대응 흔적으로 보인다: 같은 쪽에 *"revised ⁷Li ssNMR"*).
- **반은 어겼다** — 그 단서 직후 *"Combined with the conductivity results … these calculations support a LPSCl-dominated composite transport model"*, 결론에서 *"DFT results support the possible auxiliary role of SSEs/polymer contact regions in contact-assisted Li⁺ transfer"* · *"active ionic mediator facilitating a continuous Li⁺ percolation network"*. 장벽의 **절대값**은 안 쓴다고 하면서 **서열**은 실측 수송 기전의 근거로 쓴다. 그런데 서열이 의미를 가지려면 세 값의 오차가 같은 방향·같은 크기여야 하는데, 세 모형이 **서로 다른 종류**(3D 벌크 / 진공 위 슬랩+사슬 / 진공 속 고립 사슬)라 그 전제가 없다 (→ (e), §6.3).

**(c) 에너지 프로파일 모양 ↔ 서술**
- **이미지 7개** (Methods 4개와 불일치).
- **세 곡선 모두 끝점이 정확히 0.00 / 0.00** (공통 검은 막대). 벌크 대칭 홉이면 자연스럽지만, **접촉부**(슬랩 표면 Li → 고분자 속 Li)와 **고분자**(O 4개 우리 → O 1–2개 자리, `Fig. S16` 1·3컷)는 **처음과 끝이 다른 환경**이라 에너지가 같을 이유가 없다 → 끝점을 따로 이완하지 않았거나, 그림이 실제 값이 아닌 **대칭화된 도식**일 가능성 (의심).
- **최고점이 셋 다 정가운데 이미지** + **중간 극소 없음**. 벌크 궤적이 ≈6–8 Å 인데 아지로다이트의 단일 점프는 doublet **1.9 Å** · intracage **2.25 Å** · intercage **≈2.9 Å** ([dK16Arg] · [Adeli19]), 케이지 중심 간 거리 **7.0 Å** ([dK16Arg]) → 이 경로는 **케이지→케이지 여러 점프를 한 NEB 로 묶은 것**으로 보이는데, 그러면 중간 48h 자리에서 극소가 나와야 한다 (의심).
- 가로축이 거리(Å)가 아니라 **등간격 칸** — 경로 길이와 이미지 간격을 그림에서 확인할 수 없다. 세로축 이름 "Energy barrier (eV)" 는 실은 상대에너지.

**(d) 바인더 안 Li⁺ 이동 계산이 이 막의 σ 를 설명하는 데 쓰이나 — 체적분율·연결성**
- 고분자는 고체의 **≈6 vol%** (우리 산수, §3a). 측정 σ 서열은 **pristine 3.23 > 전구막 2.67 > LPSCl-LiTFSI-PMEMA 1.81 > USF 1.56 ≫ 5 % PTFE 0.42**, Ea 는 0.24 → 0.29 eV 로 **올랐다**. ⇒ 데이터가 말하는 것은 *"LiTFSI-PMEMA 는 PTFE 보다 **덜 막는다**"* 이지 *"Li⁺ 를 **더 빨리** 나른다"* 가 아니다.
- 실측 고분자 σ(1.04×10⁻⁴)로 7 nm 피막 두 겹(14 nm)의 저항을 재면 접촉 면적당 ≈0.0135 Ω cm² (우리 산수) — **측정값이 맞다면** 피막은 크게 막지 않는다. 그런데 **DFT 값(1.20 · 0.85 eV)이 맞다면** 그 피막은 절연막이다. 논문은 두 그림을 동시에 쓴다.
- "percolating network" 의 직접 증거(고분자 상의 연결성 · 3D 영상 · 고분자만의 전도 경로 차단 실험)는 **없다**. 단면 SEM 에서 보이는 망은 **PTFE 섬유**다(`Fig. S6d`). **LiTFSI 없는 PMEMA**(또는 같은 연성의 비전도 고분자) 4 wt% 대조군이 없어서, σ 이득이 **Li⁺ 전도** 때문인지 **치밀화(기공 35 → 14 %)·연성** 때문인지 갈리지 않는다.

**(e) 그림 값 ↔ 본문 값 ↔ SI 값**

| 대조 | 판정 |
|---|---|
| 0.55 / 0.85 / 1.20 eV — 본문 p.6 ↔ `Fig. 2f` | ✅ 일치 |
| Ea 0.24/0.32/0.28/0.29 — 본문 ↔ `Fig. 2a` 범례 ↔ 기울기 재검 | ✅ 일치 |
| σ 3.23/0.42/1.81/1.56 — 본문 ↔ `Fig. 2b` ↔ `Table S2` | ✅ 일치 |
| σ_e — 본문 ↔ `Fig. S13` | ✅ 일치 |
| 이미지 수 — Methods "4" ↔ `Fig. 2f` 7 | ❌ 불일치 |
| 셀 — Methods "3×3×3" ↔ `Fig. S15` 정육면체 1개 | ⚠ 불일치로 보임 (그림이 일부만 그렸을 가능성) |
| 슬랩 — Methods "3×3" ↔ `Fig. 2e` 주기 폭 ≈a | ⚠ 불일치로 보임 |
| 모형 이름 "LiTFSI-PMEMA" ↔ 원자 (TFSI 없음 · 그림 제목 "PMEMA") | ❌ 불일치 |
| 고분자 화학 — 이름 MEMA(에테르 O 1) ↔ `Fig. S2` 구조식(에테르 O **2**) ↔ DFT 긴 곁사슬(에테르 O 4–5) ↔ GPC 단위 질량 144.2 (= MEMA) | ❌ 세 표현이 서로 다르다 |

### 6.3 DFT 실행상 오류 — 확인 / 의심 / 미기재

| 등급 | 항목 | 근거 | 결과에 미치는 영향 |
|---|---|---|---|
| **확인** | 이미지 수 Methods 4 ↔ 그림 7 | SI p.5 ↔ `Fig. 2f` | 어느 쪽이 실제 계산인지 모른다 → 재현 불가 |
| **확인** | "LiTFSI-PMEMA" 계산에 **TFSI⁻ 없음** | `Fig. 2e` 범례 Li·P·S·C·O · `Fig. S16` 범례 C·H·O · 그림에 N·F 원자 없음 | 실제 막의 Li⁺ 는 TFSI⁻ 와 이온쌍·응집 · 고분자 안 Li 농도 30 wt% LiTFSI 가 모형에 없다 → 고분자 상 "장벽" 이 이 재료의 양이 아니다 |
| **확인** | 고분자 사슬이 **PMEMA 가 아니다** | `Fig. 2e`·`Fig. S16` 확대: 곁사슬 하나가 에테르 O 4–5 개의 올리고(EO) — MEMA 곁사슬은 에테르 O 1 개 (GPC 단위 질량 144.2 = MEMA 로 확인) | Li 배위 자리 수·사슬 유연성이 다른 고분자의 값 |
| **확인** | 고분자 단독 계산의 방법 **0 줄** | SI pp.4–5 (벌크·슬랩만 기술) | 셀·진공·전하·사슬 길이·형태 표본 전부 불명 |
| **확인** | 서로 다른 세 모형의 장벽을 **한 서열**로 비교 | 본문 p.6 *"hierarchy"* | 3D 주기 결정 / 진공 위 슬랩+단일 사슬 / 진공 속 고립 사슬 — 유전 차폐·이완 자유도·k점·끝점 기준이 다 다르다 |
| **확인** | 장벽 서열과 수송 서술의 **차수 모순** | §6.2(a) | 0.85·1.20 eV 로는 "보조 경로" 를 말할 수 없다 |
| **확인 (경미)** | D3 인용 [7,8] 의 [8] = Monkhorst–Pack | SI 참고문헌 | 서지 오류 |
| **의심** | 벌크 셀이 정육면체 1개(≈9.9 Å) | `Fig. S15` | 3×3×3 이 아니면 이동 Li 가 ≈9.9 Å 거리의 자기 상과 상호작용 · Li 24개 중 1개 이동(4 %) |
| **의심** | 슬랩 가로 ≈a, 두께 ≈8 Å | `Fig. 2e` | 3×3 이 아니면 서 있는 사슬이 옆 칸 상과 ≈1 nm 거리 |
| **의심** | 세 경로 끝점이 모두 정확히 0.00 | `Fig. 2f` | 비대칭 경로 둘(접촉·고분자)에서 끝점 독립 이완 여부 의문 — 우리 SEI NEB 철회 사유 중 하나가 **끝점 미이완**이었다 |
| **의심** | ≈6–8 Å 경로에 중간 극소 없음 | `Fig. S15` 궤적 + `Fig. 2f` | 다중 점프를 선형 보간 한 줄로 묶었으면 장벽은 **경로 선택의 산물** |
| **의심** | 정렬 Cl@4a 모형 | `Fig. S15` Cl 위치 (모서리+면심 4개) | [dK16Arg] AIMD 에서 이 배열(all-4a, Li₆PS₅Cl 0 % Cl@4c)은 450·600 K 에서 **intercage 점프 0** · 300 K 도 0.04(±0.13)×10¹⁰ s⁻¹ = 사실상 0 — 실제 Li₆PS₅Cl 은 4d 무질서 ≈62 % ([Kraft] 중성자) |
| **의심** | 전하 상태 — 중성 Li 원자 | 반대이온 없음 + "spin-polarized" | "Li⁺ 이동" 이 아니라 Li⁰ 라디칼 이동일 수 있다. 우리도 **전하 부호 오류**로 SEI NEB 전량을 철회했다 (§6.4) |
| **의심** | 고분자 상자가 사슬로 꽉 참 | `Fig. S16` 점선 상자 높이의 ≈90 % | 상자가 셀이면 사슬 끝과 주기상이 맞닿음 |
| **의심** | 사슬 형태 변화가 장벽에 섞임 | `Fig. S16` 1→3 컷에서 아래 덩어리가 크게 재배열 | 진공 속 단일 사슬은 형태 재배열 비용을 주변이 받아 주지 않는다 · 실제 고분자(Tg 14 °C < 30 °C, 고무상)의 Li⁺ 는 **분절 운동**과 같이 움직인다 — 얼린 사슬의 0 K 안장점은 그 양이 아니다 |
| **미기재** | VASP 버전 · PAW 세트 · D3 감쇠 · 격자상수/셀 이완 · 벌크 k점 · NEB 에너지의 k점 · 원자 수 · 슬랩 종단·화학량론·쌍극자 보정 · 스프링 · NEB 수렴 · CI 수렴 · 자기 상태 · 고분자 배치 수·형태 표본 · 경로 후보 수 · 구조 파일 | — | **재현 불가** — 같은 숫자를 다시 낼 방법이 없다 |

### 6.4 우리와 뭐가 달라서 이런 결과가 나왔나

**(i) 계산 조건이 다르다 — 그래서 장벽이 높게 나온다**

| 조건 | Cao 2026 | 우리 | 이 차이가 하는 일 |
|---|---|---|---|
| 무질서 | **정렬 단일 배열** (Cl 전부 4a — `Fig. S15` 판독) | MLIP-MD 에서 **무질서 앙상블을 따로 돈다** — comp2(Li₆PS₅Cl₀.₅Br₀.₅, 52 원자)는 정렬 챔피언 vs d=0.50 배치 3개, modelc 는 Cl-rich 조성 자체가 4a/4d 섞임 | [dK16Arg]: 정렬(all-4a)이면 450·600 K AIMD 에서 intercage 점프가 **0** (300 K 도 통계적으로 0) — 케이지가 고립된다. 이 배열에서 케이지→케이지 경로를 하나 고르면 장벽이 높을 수밖에 없다. 우리 comp2 도 **무질서(d=0.50) 배치 쪽 Ea 가 정렬보다 낮았다** (방향만 · 값 정밀 인용 금지 · provisional · d=1.00 은 게이트 FAIL · `md-ea-comp2-disorder-d050`) |
| 셀 | 진술 3×3×3 / 그림 ≈1×1×1 · 슬랩 진술 3×3 / 그림 ≈1 칸 | MD 셀 52 원자(comp2 앙상블) ~ **558 원자**(modelc·lpsocl box331) / NEB(SEI 상): **λ₁ ≥ 10 Å 셀 게이트** 통과해야 시작 · 단일 셀이면 `provisional_single_cell` | 작은 셀은 이동 Li–자기 상 상호작용과 강제된 국소 긴장을 장벽에 섞는다 |
| 경로 | 손으로 고른 **한 경로** · 선형 보간 | MD 는 경로를 고르지 않는다 (모든 점프가 궤적에 들어간다) | 한 경로의 안장점은 *가장 쉬운 길* 이라는 보장이 없다 |
| 전하 | **미선언** | NEB 도구가 상의 전자 부류로 **전하를 갈라 강제**: 절연체 = V_Li⁻ (tot_charge −1) + jellium · Gaussian / 금속 = 중성 공공 · mv. 결과마다 `electronic_class`·`tot_charge` 를 같이 싣는다 | 정공·전자가 남으면 장벽이 전자 구조 인공물로 오염된다 |
| 끝점 | 미기재 (그림상 대칭) | 끝점 이완이 기본값 · `endpoints_symmetry_equivalent`·`asymmetry_eV` 기록 | 비대칭 경로를 대칭으로 보이게 하면 장벽 정의 자체가 흔들린다 |
| 힘 | VASP PBE-D3 정적 | UMA-s-1p1(omat) MLIP 동역학 · NEB 는 QE PBE | 범함수 계열은 둘 다 PBE 급 — **주원인이 아니다** |
| 바인더 | 고립 단일 올리고머 · TFSI 없음 | **우리는 고분자 상 DFT 가 없다** | 비교 대상 없음 — 우리 바인더(SDCP 등)는 흡착 E 보고량 카드로만 다룬다 |

**(ii) 보고량이 다르다 — 그래서 숫자를 나란히 놓을 수 없다**

| 보고량 | 정의 | 무엇을 평균하나 | 이 논문과의 관계 |
|---|---|---|---|
| **NEB 장벽** (이 논문) | 0 K · 한 경로 · 한 배열의 최소에너지경로 최고점 | **아무것도** — 한 점이다 (오차막대 정의 불가, [He18Var] 류의 통계 자체가 없다) | — |
| **우리 MLIP-MD Ea** | 600/800/1000 K MSD(2–50 ps) 확산계수의 아레니우스 기울기 | doublet·intracage·intercage **모든 점프** · 열적 무질서 · 상관 일부 · (앙상블이면) 배치 | 거시 유효량. ⛔ 1저자 정책상 **우리 계 사이 상대차로만** 쓴다 — 이 논문 0.55 eV 와 나란히 쓰지 않는다 |
| **우리 BVSE** | softBV 결합원자가 에너지 지형에서 Li 채널이 이어지는 문턱 · 채널 % | 전자 구조 없음 · 정적 지형 | 경로 연결성 지표 — 장벽 크기 비교 불가 |
| **실측 Ea** (이 논문 `Fig. 2a`) | 30–90 °C 임피던스 총저항 | 벌크 + 입계 + (막이면) 바인더·기공 | 이 논문 자신이 0.55 eV 와 2.3 배 다르다 |

**(iii) 서술 규율이 다르다**
- 이 논문: 세 모형의 장벽을 한 서열로 묶고 → 실측 NMR·cryo-TEM 과 엮어 → "mediator / percolation network" 결론.
- 우리: ① 장벽을 인용할 때 **홉 수 검산 한 줄**을 같이 싣는다(`D-2026-09-27`) — 이 논문에 그 한 줄을 붙이는 순간 §6.2(a) 모순이 드러난다 ② 수송값은 **같은 프로토콜 안 상대차만** ③ 단일 셀 NEB 는 `provisional_single_cell` → 절대값 인용 금지.
- 🔴 **우리 NEB 이력 (`HZ-sei-neb-retracted`, BLOCKED)**: `db/properties/sei_neb.json` **전량 철회** (n_citable 0). 사유 = **`tot_charge = +1` 부호 오류**(중성 Li 를 뺀 뒤 전자를 하나 **더** 빼서 정공 2개 — 의도는 V_Li⁻, `tot_charge −1`) **+ 끝점 미이완**. 그 뒤 `tools/sei/build_neb_inputs.py` 가 전하 규약 분기 · 최소이미지 끝점 · 끝점 이완 기본 · λ₁ 게이트 · CI 단계 검사 · 프로토콜 해시를 **코드로** 막는다. ⇒ **Cao 논문은 바로 이 두 항목(전하·끝점)을 한 줄도 적지 않았다** — 우리가 철회한 종류의 오류가 들어 있어도 독자가 알 길이 없다. (철회된 우리 값은 여기 적지 않는다.)

**정리 — "왜 그들은 높은 장벽을 얻었나"**: ① 실제 재료(4d 무질서 ≈50–62 %)가 아닌 **정렬 배열**에서 ② 케이지 사이를 잇는 **긴 한 경로**를 ③ 작은(것으로 보이는) 셀에서 ④ 전하를 밝히지 않고 계산했고, 고분자 쪽은 ⑤ **TFSI 없는 · 다른 화학의 · 진공 속 단일 사슬**에서 형태 재배열까지 장벽에 넣었다. 그리고 ⑥ 그 셋을 실측 수송과 같은 축에서 읽었다. 우리 쪽 숫자가 다른 것은 "더 맞는 장벽" 이어서가 아니라 **애초에 다른 양**(유한 온도 · 모든 점프 · 무질서 평균)을 재기 때문이다.

### 6.5 그래도 건질 것
- 방법 반례 셋: (1) 같은 논문 실측 σ 로 장벽을 역산하는 **10초 검산**이 10⁴–10¹⁵ 배 모순을 바로 잡는다 → 우리 리뷰 프롬프트·원고 점검표의 한 줄로. (2) **"정렬 모형 + 단일 경로"** 장벽은 아지로다이트에서 실측 Ea 의 2배 이상으로 나온다 — 같은 그룹 [LiInF] 도 pristine **0.662 eV**(톱니 프로파일) — 이 그룹의 LPSCl NEB 는 일관되게 높다. (3) 고분자 전해질에 **얼린 사슬 NEB** 를 쓰면 안 되는 이유의 구체 사례.

---

## 7. 우리 DFT 대비 (`../our_dft_baseline.md` · `db/properties/`)

| 항목 | 이 논문 | 우리 | 같은가 / 다른가 · 이유 |
|---|---|---|---|
| Li 수송 보고량 | CI-NEB 0 K 한 경로 0.55 eV (정렬 모형) · 실측 Ea 0.24 eV · σ 3.23 mS cm⁻¹ | MLIP-MD 유효 Ea (UMA-s-1p1 · 600/800/1000 K · MSD 2–50 ps) · BVSE 채널 | **다른 양** — 숫자 비교 금지. ⛔ 우리 Ea·σ 는 우리 계 사이 상대차로만 (1저자 2026-09-18) |
| 무질서 | 정렬 Cl@4a 단일 배열 (figure-read) | comp2 d-level 앙상블 · modelc Cl-rich | 이 논문 장벽이 높은 1순위 원인 (§6.4) — 계산 조건 차이지 '실제 차이' 가 아니다 |
| 셀 / 전하 / 끝점 | 진술과 그림이 다름 / 미기재 / 미기재 | MD 558 원자급 · NEB λ₁ ≥ 10 Å · 전하 규약 강제 · 끝점 이완 | 우리 철회 사유(전하 부호·끝점 미이완)와 같은 축이 이 논문에선 **보이지 않는다** |
| 고분자·계면 이동 | 0.85 / 1.20 eV (TFSI 없음) | **없음** | 비교 대상 없음 |
| ESW (**B①** 산화 개시) | CV 0.1 mV s⁻¹ · SE+CB 9:1 · 본문 "∼2.6 V" · figure-read 봉우리 2.65 / 2.52 V · 개시 ≈2.3–2.4 V · 바인더가 개시를 **안 바꾼다**(저자도 인정) | comp1 = modelc **2.256 V** (0 K grand-potential, 층①) | **다른 양** (동역학 CV vs 열역학 onset) — 기존 B① 실측 개시 행([Du22LMR] ≈2.5 V 등)과 같은 계열. "산화 전류 감소" 는 B① 창 확대가 아니다 |
| 기계 (**C**) | 나노압입 Er: 펠릿 figure-read ≈0.49 GPa · 전구막 0.22 · USF 0.038 GPa | comp1 E_VRH **22.06 GPa** (DFT 0 K relaxed-ion) | **다른 양** — 다공 성형체/막의 국소 압입(깊이 ≈입자 크기) vs 단결정 탄성. 40–600 배 차는 기공·접촉 때문. ⛔ 비교 금지 |
| 전자 (**D**) | σ_e 2.64×10⁻⁹ (LPSCl) → 3–7×10⁻¹⁰ S cm⁻¹ (막) | PBE gap comp1 2.066 eV (fixed-occ) | 축이 다르다 — σ_e 는 결함·입계·불순물 양, gap 은 띠 구조. 대조하지 않는다 |
| 같은 그룹 선례 | 이 논문 0.55 eV (벌크) | — | [LiInF] 슬랩 0.662 eV · 둘 다 실측의 2–3 배 — 그룹 프로토콜의 경향 |

---

## 8. DFT/계산 방법 ★ (템플릿 §4 — 상세는 §6.1)
- **code**: VASP (버전 미기재) · **functional**: PBE + Grimme D3 (감쇠형 미기재) · 스핀분극 · **PAW** (세트 미기재)
- **ecut 550 eV** · **k**: Γ 1×1×1 (구조) / 3×3×1 (단일점) · **supercell**: 벌크 "3×3×3" (그림 ≈1×1×1) · 슬랩 "(100) 5층 3×3, 진공 20 Å, 위 3층 이완" (그림 ≈1 칸) · **nat 미기재**
- **DFT+U**: 없음 · **AIMD / MLIP**: 없음
- **무질서 처리**: 미기재 → 그림상 **정렬 단일 배열**
- **NEB**: CI-NEB · 선형 보간 · 이미지 "4" (그림 7) · 스프링·NEB 수렴 미기재 · 전하 미기재
- **특이사항**: 고분자 단독 계산 방법 0 줄 · TFSI 없음 · 사슬 화학이 PMEMA 와 다름

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 건식 열압연 공정 만화 (전구막 + 고분자막 샌드위치 → 100 °C 롤 → 접기 반복) | DEM 건식막 공정 단계 표현의 참고 |
| 1b,c | USF 윗면 SEM · 단면 18 µm + EDS S·C·O·F | 막 두께 앵커 (단, `Fig. 5a` 셀 속은 figure-read ≈12 µm) |
| 1d | 건식 황화물막 두께 vs σ 13편 + 본 연구 (`Table S3`) | DEM 막 축의 문헌 지도 · S10 = 우리 modelc 조성 막 |
| 1e,f | MIP 기공 분포 · 겉보기 기공률 34.99 → 14.36 % · 거대기공 비율 | DEM 압밀 축 기공률 앵커 (겉보기·Hg 접근 기공 · 연성막 압축 주의) |
| 1g–i | 나노압입 하중–깊이 · Er/H · 소산 효율 | ⛔ DFT 탄성과 비교 금지 · DEM 접촉 강성 보정에 그대로 쓰지 않는다 (막 응답) |
| 2a | 아레니우스 4종 (Ea 0.24/0.32/0.28/0.29 eV) | 오차막대 없음 · USF Ea 가 pristine 보다 높다 |
| 2b | 이온·전자 전도도 막대 | 바인더 종류별 σ 감소량 앵커 |
| 2c | ⁷Li NMR + 면적 분율 68.9/21.7/9.4 % | 🔴 '고분자 관련 9.4 %' 는 화학양론 0.2 % 의 48 배 — 분율을 개체수로 읽지 말 것 |
| 2d | cryo-TEM ≈7 nm 피막 + FFT | 피막 두께 ↔ 체적분율 검산 가능 · FFT (331)/(200) 라벨 뒤바뀜 의심 |
| 2e | 접촉부 NEB 세 컷 (슬랩 + 서 있는 3단위 올리고머, TFSI 없음) | 🔴 방법 반례: 다른 화학·반대이온 없음·주기 폭 ≈a |
| 2f | 세 경로 에너지 (9 점, 끝점 전부 0) | 🔴 홉 수 검산 교보재 · 이미지 수 불일치 |
| 2g | 경로 I/II/III 수송 모형 만화 | 결론의 '보조 경로' 는 2f 숫자와 차수 모순 |
| 3a,b | 대칭셀 CCD 0.9 vs 2.2 mA cm⁻² | 계면·접촉 효과 (막 벌크 저항 몫 ≤ 수 %) |
| 3c | 대칭셀 1200 h vs 212 h 단락 | 〃 |
| 3d–g | 200 h 후 LiIn/SE 단면 · 수지상 만화 | 기공·균열 → 단락 서사 (정성) |
| 4a–c | LCO 율속 · 곡선 (Li 눈금) | 셀 성능 앵커 |
| 4d | LCO 1500 사이클 · PTFE 236 단락 | 본문 'rapid fading' 과 그림(평탄 후 단락) 불일치 |
| 4e–h | 압력 모니터 · 200 사이클 후 단면 | 'negligible pressure variation' 은 피크 표류에만 맞다 |
| 5a | NCM721‖USF‖nSi 단면 + EDS | 셀 속 막 두께 figure-read ≈12 µm |
| 5b,c | 율속 · 300 사이클 81.3 % | 셀 성능 앵커 |
| 5d,e | 파우치 CIP 조립 · 사이클 | 캡션 '0.1 C >40' ↔ 그림 '0.5C · 80 사이클' 불일치 |
| S1 | LPSCl 분말 SEM (1–3 µm) | 입경 분포 정성 |
| S2 | 중합 반응식 | 🔴 단위체가 에테르 O **2개**로 그려짐 — 이름(MEMA, O 1개)·GPC 단위 질량과 불일치 |
| S3 | FTIR — C=C 1643 cm⁻¹ 소실 | 중합 확인 |
| S4 | GPC 곡선 (Mn 28.4 · Đ 3.19) | 손 크롭 (도구가 S5 사진을 넣어 두었다) |
| S5 | 사진 + 두께 게이지 (0.03 / 0.026 / 0.05 / 0.02 mm) | 전구막 30 µm (본문 20 µm 과 불일치) |
| S6 | 4종 막 윗면·단면 SEM (Voids · PTFE fiber network) | USF 단면의 망은 PTFE |
| S7 | TG — 분해 개시 239 °C | 공정 온도 여유 |
| S8 | D50 / 피크 기공 지름 막대 | 기공 크기 앵커 |
| S9 | XRD 3종 | 결정상 유지 (비정질화는 못 본다) |
| S10 | Raman 3종 — PS₄³⁻ ≈425 cm⁻¹ | 손 크롭 (도구 번호 공백) |
| S11 | XPS P 2p 3종 | 분해 흔적 없음 (표면) |
| S12 | CV SE+C‖SE‖LiIn 0–5 V | B① 실측 개시 계열 · 환원 전류도 줄었다 → 피복 면적 효과 가능 |
| S13 | DC 분극 σ_e 4종 | 바인더 막이 σ_e 를 3–8 배 낮춤 |
| S14 | cryo-TEM EDS C·O·F·P·S·Cl (500 nm) | 7 nm 층의 화학 확인에는 해상도 부족 |
| S15 | 벌크 NEB 구조 + Li 궤적 | 🔴 셀 ≈1 칸 · 정렬 Cl@4a · 궤적 ≈6–8 Å |
| S16 | 고분자 NEB 세 컷 (C·H·O, TFSI 없음) | 🔴 고립 사슬 · 긴 올리고(EO) 곁사슬 · 상자 ≈90 % 점유 |
| S17 | H₂S 발생 40 min (≈1.39 vs ≈1.19 cm³ g⁻¹) | 분말 vs 막 — 정성 |
| S18 | LiIn‖USF‖LiIn OCV 노화 EIS | 고주파 절편 ≈40 Ω ≫ σ 로 기대한 ≈1.5 Ω |
| S19 | 노화 셀 XPS C 1s / F 1s / P 2p | LiF 없음 → PTFE 환원 없음 (LiIn 조건 한정) |
| S20 | PTFE 셀 235·236 번째 곡선 (단락) | 단락 시점 증거 |
| S21 | LCO 셀 EIS 5–100 사이클 · 계면저항 추출 | 계면저항 증가 속도 비교 |
| S22 | 200 번째 곡선 | 분극 비교 |
| S23 | 전압별 in-situ EIS + DRT τ1–τ4 | DRT 귀속 사례 (τ2 CEI/USF · τ3 계면 전하이동) |
| S24 | NCM721‖USF‖nSi 사이클별 곡선 | 셀 성능 |
| Table S1 | GPC 수치 (DPn ≈197) | 단위 질량 144.2 = MEMA 검산 |
| Table S2 | 고분자 전해질 15종 σ 비교 + 본 연구 4행 | LiTFSI-PMEMA 1.04×10⁻⁴ S cm⁻¹ (첨가제 없음) · 3쪽 이어붙임 |
| Table S3 | 건식 황화물막 13편 (두께·바인더·σ) | DEM 막 축 문헌표 · 2쪽 이어붙임 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

**NEB 쪽 (상세 §6)** — 홉 수 모순 · 이미지 수 · TFSI 없음 · 다른 화학의 사슬 · 고분자 계산 방법 0 줄 · 모형 간 서열 비교 · 셀·끝점·전하 의심 · 정렬 모형.

**실험 쪽**
1. 🔴 **"전도성 바인더가 Li⁺ 수송을 가속" 은 대조군 선택에서 나온다.** 같은 1 wt% PTFE 전구막(2.67 mS cm⁻¹)에 4 wt% LiTFSI-PMEMA 를 더한 USF 는 **1.56 으로 내려갔다**. 비교 대상을 5 wt% PTFE(0.42)로 잡아야 "향상" 이 된다. 결론의 *"accelerates Li⁺ transport kinetics"* (서론) · *"active ionic mediator"* (결론) 는 데이터보다 크다 — 정확한 문장은 *"LiTFSI-PMEMA blocks Li⁺ transport less than PTFE at equal loading"*.
2. 🔴 **핵심 대조군 부재** — LiTFSI 없는 PMEMA(또는 같은 연성의 비전도 고분자) 4 wt%. 치밀화(기공 35 → 14 %)·연성 효과와 이온 전도 효과가 분리되지 않는다.
3. 🔴 **NMR 면적 분율의 개체수 해석 불가** — 고분자 Li 는 전체 Li 의 0.196 % (우리 산수)인데 '고분자 관련' 9.4 %. 중간 성분 21.7 % 도 표면 근방 Li(입자 1–2 µm 이면 1 nm 껍질 ≈0.3–0.6 %)로는 설명이 안 된다. 가능한 해석(우리 가설 · 검증 안 됨): 40 회 열압연에 따른 **부분 비정질화**·결함 LPSCl, 또는 피팅이 주봉을 쪼갠 것. XRD·Raman·XPS 는 수 % 비정질상을 못 본다.
4. ⚠ **시료 이름 충돌** — "LPSCl-PTFE" 가 1 wt% 전구막과 5 wt% 대조막 둘을 가리킨다. 본문은 *"the LPSCl-PTFE **precursor** film is used as the primary control sample"* (p.4), SI 는 *"5:95 for the LPSCl-PTFE **control** sample"*. `Fig. 3`·`Fig. 4` 의 대조가 어느 막인지 확정 불가 — 전구막이라면 *"Li⁺-insulating PTFE phase hinders Li⁺ transport"* (CCD 해석)는 전구막 σ 2.67 > USF 1.56 과 모순.
5. ⚠ **대칭셀 분극 차는 막 σ 로 설명되지 않는다** — 막 벌크 IR 은 0.4–3.6 mV, 실제 분극 50–150 mV (우리 산수 · figure-read). 차이의 원인은 계면·접촉·기공이고, 논문도 SEM 으로 그것을 보여 준다 — 그런데 문장은 바인더의 Li⁺ 전도로 돌린다.
6. ⚠ **CV 전류 감소 = "산화 동역학 저항" 이라는 해석** — 환원 전류도 같이 줄었다(figure-read). 피복이 LPSCl|C 접촉 면적을 줄인 것과 구별이 안 된다. 전류 분모(g of what) 미기재.
7. ⚠ **두께 불일치** — 전구막 20 µm (p.2) vs ≈30 µm (p.2–3, `Fig. S5a`). 셀 속 USF figure-read ≈12 µm (`Fig. 5a`).
8. ⚠ **σ 측정 셀·압력 미기재** + `Fig. S18` 고주파 절편 ≈40 Ω 이 σ 로 기대한 막 저항 ≈1.5 Ω 의 27 배.
9. ⚠ **글·그림 불일치** — `Fig. 4d` PTFE 셀은 평탄 후 단락인데 *"rapid capacity fading"* · `Fig. 4f` USF 는 사이클당 ≈0.4 MPa 오르내림인데 *"negligible pressure variation"* · 본문 패널 참조가 엇갈림 (*"internal cracking … (Figure 4f)"* → 4g 여야 · *"negligible pressure … (Figure 4g)"* → 4f 여야).
10. ⚠ **파우치** — 본문·캡션 *"over 40 cycles at 0.1 C"* ↔ `Fig. 5e` 는 ≈7–10 사이클 뒤 **"0.5C"** 표지로 80 사이클까지 (figure-read). 322.7 Wh kg⁻¹ 의 질량 내역 미기재.
11. ⚠ **고분자 화학 표기 셋이 다르다** — 이름 MEMA(에테르 O 1) · `Fig. S2` 구조식(에테르 O 2 = MEO₂MA 꼴) · DFT 모형(긴 올리고 EO). GPC 단위 질량 144.2 는 MEMA 를 지지 → `Fig. S2` 는 그림 오류로 보인다.
12. ⚠ **FFT 지표 라벨** — (331)·(200) 원의 반지름이 서로 뒤바뀐 것으로 보인다 (§5.6, (620) 으로 축척 검증).
13. ⚠ **7 nm 피막의 정체** — 대비만으로 LiTFSI-PMEMA 로 배정 (선분석 없음). 비정질 표면 반응층과 구별되지 않는다.
14. 경미: `Fig. 1d` 캡션 "Table S1" → `Table S3` · SI p.6 "~105 nm" → ~10⁵ nm · `Table S2` 제목의 고온 행 없음 · "LiNbO₂" · NCM721‖nSi 창을 "vs Li⁺/Li" 로 표기(전셀) · `Fig. S16` 캡션 "of l Li⁺" · D3 인용 [8] · 이해상충 문구 · "revised ⁷Li ssNMR" 흔적 · Ea·소산 효율 오차막대 없음 · "thinnest" 는 직전 20 µm 대비 2 µm 차(게이지 눈금 10 µm).

**잘한 점** — 대기 노출 <1 min MIP 프로토콜과 "apparent" 라는 정직한 명명 · NMR 중간 성분을 개별 계면종으로 단정하지 않은 것 · DFT 장벽을 Ea 와 같지 않다고 적은 것 · 파우치까지 간 실증 · σ_e 를 같이 잰 것.

---

## 11. Post-processing
- **무엇**: CI-NEB 3건 (장벽 = 최고 이미지 − 끝점) 뿐. Bader·DOS·COHP·ELF·MD 없음.
- **도구**: 구조 그림은 VESTA 양식(점선 셀 · 원소 범례) · 프로파일은 Origin 식 '에너지 준위' 도식(이미지마다 수평 막대 + 점선 연결 · 가로축 등간격).
- **기록**: 장벽 3값 + 이미지별 상대에너지(그림 인쇄값)뿐. 구조 파일·경로 좌표 **비공개**("SI 에 있다" 고 했으나 없다).

---

## 12. 적용 인사이트 ★
1. **원고·리뷰 점검표에 '자기 σ 로 장벽 역산' 한 줄** — NE 역산(가정 명시)이 홉 수 검산과 같은 10초 비용으로 10⁴–10¹⁵ 배 모순을 잡는다. `D-2026-09-27` 홉 수 한 줄의 짝으로 둘 만하다 (제안 · 결정 아님).
2. **아지로다이트 NEB 를 우리가 다시 한다면** (지금 계획 없음): 무질서 배열 선언(정렬 단일 배열 금지 · [dK16Arg] all-4a 는 intercage 가 사실상 0) + 셀 λ₁ 게이트 + 전하 규약 + 끝점 이완 + 경로가 다중 점프면 **점프별로 쪼갠 NEB**. 우리 SEI NEB 도구가 이미 앞의 넷을 강제한다.
3. **DEM 건식막 축 앵커** (comparison_vs_ours_DEM 쪽 · 부모 세션 판단): 1 wt% PTFE 전구막 기공 35 % · 18 µm USF 14 % · D50 630 → 150 nm · 바인더 종류·함량별 σ (3.23 / 2.67 / 1.81 / 1.56 / 0.42 mS cm⁻¹) — **바인더가 σ 를 얼마나 깎나** 의 실측 세트. ⚠ 나노압입 Er 는 접촉 강성 보정에 그대로 쓰지 않는다.
4. **S10 행 = 우리 modelc 조성 건식막** (`Table S3`, 30 µm · 8.4 mS cm⁻¹ · PTFE 0.2 %) — modelc 를 막으로 만든 외부 실측이 있다는 사실 하나. 원전(Zhang 2021 *Nano Lett.*) 인입 후보.
5. **대칭셀 분극 ≠ 막 σ** 의 크기 산수 (막 벌크 ≤ 수 %) — 우리 DEM σ_ionic 을 셀 분극에 바로 대응시키지 않는다는 규율의 외부 사례.

---

## 13. 인용 가능 문장 (영문 초안 — 방어 가능한 것만)
- "Cao et al. reported that replacing PTFE with an ion-conducting LiTFSI-PMEMA binder at equal 5 wt.% loading raises the conductivity of dry-processed Li₆PS₅Cl films from 0.42 to 1.81 mS cm⁻¹, whereas the dual-binder 18-µm film (1.56 mS cm⁻¹) remains below both the 1 wt.% PTFE precursor film (2.67 mS cm⁻¹) and the pristine pellet (3.23 mS cm⁻¹)."
- "Hot-rolling with the second binder reduced the apparent Hg-accessible porosity from 34.99% to 14.36% (median pore diameter 630 → 150 nm)."
- (방법 반례로) "A 0 K CI-NEB barrier of 1.20 eV for Li migration in an isolated polymer segment implies a hop rate of ~10⁻⁷ s⁻¹ at 30 °C (ν₀ = 10¹³ s⁻¹ assumed), incompatible with the measured 10⁻⁴ S cm⁻¹ conductivity of the same polymer; static barriers from ordered or isolated-chain models should not be ranked against macroscopic transport."

---

## 14. 주의 / 한계 (인용 규율)

**⛔ 인용 금지**
- DFT **0.55 / 0.85 / 1.20 eV** 를 LPSCl·계면·고분자의 Li⁺ 이동 장벽으로 (모형 불일치 · 전하 미기재 · 홉 수 모순). 쓰려면 *"정렬 단일 배열 · 미선언 전하 · TFSI 없는 고립 사슬 · 0 K 한 경로"* 조건을 붙여 **방법 반례로만**.
- 그 셋의 **서열**을 수송 기전 근거로.
- NMR 면적 분율(68.9/21.7/9.4 %)을 Li 개체수·계면 Li 비율로.
- "LiTFSI-PMEMA 가 Li⁺ 수송을 가속/percolation 망을 만든다" — 데이터는 *"PTFE 보다 덜 막는다"* 까지.
- 나노압입 Er·H 를 LPSCl 탄성으로 · 우리 E_VRH 와 같은 줄에.
- CV "∼2.6 V" 를 우리 B① onset(2.256 V)과 같은 양으로 · 산화 전류 감소를 "창 확대" 로.
- "18 µm" 를 셀 속 두께로 (셀 속 figure-read ≈12 µm).
- 우리 MLIP-MD Ea·D·σ 를 이 논문 값과 숫자로 나란히 (1저자 인용정책).

**⚠ 조건부**
- σ·σ_e·기공률·D50·셀 수치 — 실측 소환값으로 인용 가능 (측정 셀·압력 미기재 단서).
- 정렬 모형 장벽이 실측보다 높다는 **정성** 관찰 — [dK16Arg]·[Kraft] 와 함께일 때만.

---

## 15. 기법 용어 미니사전
- **CI-NEB (climbing-image nudged elastic band)**: 처음·끝 구조 사이에 이미지(중간 구조)를 늘어놓고 스프링으로 이어 최소에너지경로를 찾는 법. 최고 이미지 하나를 스프링에서 풀어 **안장점까지 밀어 올리는 것**이 CI. 이미지 수가 적거나 선형 보간이 실제 경로와 멀면 엉뚱한 안장을 잡는다.
- **끝점(endpoint) 이완**: NEB 의 처음·끝 구조를 먼저 각각 완전히 이완하는 것. 안 하면 장벽에 '끝점이 덜 풀린 에너지' 가 섞인다 (우리 SEI NEB 철회 사유 중 하나).
- **전하 상태 / jellium**: Li 하나를 빼면 절연체에는 정공이 남는다 → 전자를 하나 더해 V_Li⁻ (QE `tot_charge = −1`)로 만들고, 셀 전체 전하는 균일 배경(jellium)으로 상쇄. 부호를 틀리면 정공이 2개가 된다 (우리 실제 사고).
- **홉 수 검산**: Γ = ν₀·exp(−Ea/kT) 로 '한 자리에서 1초에 몇 번 뛰나' 를 차수로 본다. ν₀ 는 10¹³ s⁻¹ 가정.
- **Nernst–Einstein 역산**: σ = n e² D / kT, D = Γ a² / 6 → 측정 σ 에서 필요한 Γ 를 거꾸로 낸다. Haven 비(상관 보정)·홉 길이·운반자 수 가정이 붙는다 — 차수 검산용.
- **Haven 비**: 추적자 확산계수 / 전도 확산계수. 1 이면 무상관. 아지로다이트 실측 ≈0.3 ([Adeli19]).
- **4a / 4d 무질서**: 아지로다이트에서 Cl⁻ 와 '자유' S²⁻ 가 두 자리(4a·4d)를 섞어 앉는 정도. 섞일수록 케이지 사이 점프(intercage)가 열린다 ([dK16Arg] · [Kraft]: Li₆PS₅Cl ≈62 %).
- **doublet / intracage / intercage**: 48h 쌍 안(≈1.9 Å) / 케이지 안(≈2.25 Å) / 케이지 사이 점프. 거시 확산은 가장 느린 intercage 가 정한다.
- **분절 운동(segmental motion)**: Tg 위 고분자 사슬 토막의 열적 꿈틀거림. 고분자 전해질의 Li⁺ 는 이것에 실려 배위 O 를 갈아탄다 — 얼린 사슬의 0 K 장벽과 다른 양.
- **⁷Li MAS ssNMR 면적 분율**: 단일 펄스 스펙트럼을 성분으로 맞춘 면적 비. 이완·사중극·측띠 때문에 정량 조건을 따로 맞추지 않으면 개체수가 아니다.
- **cryo-TEM / FFT**: 저온에서 빔 손상을 줄여 찍은 고분해 영상과, 그 격자 무늬의 푸리에 변환(점 = 면간격 역수). 축척으로 d 를 재 지표를 검산할 수 있다.
- **MIP (수은 압입)**: 압력에 따른 수은 침투량으로 기공 크기 분포. 연성막은 압력에 눌려 '겉보기' 값이 된다.
- **Oliver–Pharr**: 압입 하중–깊이의 제하 곡선 기울기로 감소 탄성률(Er)과 경도(H)를 내는 표준법.
- **CCD (critical current density)**: 계단 전류에서 단락·전압 발산이 시작되는 전류밀도.
- **DRT**: 임피던스를 시간상수 분포로 풀어 겹친 과정을 가르는 해석.
- **Γ-only k점**: 브릴루앙 영역을 Γ 한 점으로만 표본. 큰 셀에서는 괜찮지만 ≈10 Å 셀에서는 부족할 수 있다.

---

## 16. 그림 크롭 기록 (`litdb/figures/cao2026_dual_binder_18um_sulfide_electrolyte_film/figures.json`)
- **manual_crop**: `Fig. S10` (도구가 '그래픽 없음' 으로 번호 공백 · 벡터 그림이 캡션 위) · `Fig. S4` (도구가 `Fig. S5` 사진 영역을 넣어 두었다 · 벡터 GPC 곡선으로 교체).
- **recrop** (아래쪽 13–25 pt 잘림 = 축 제목 소실 — Word SI 의 캡션 블록이 빈 줄로 시작해 그림과 겹친 탓): `Fig. S1` · `S2` · `S5` · `S7` · `S8` · `S9` · `S11` · `S12` · `S13` · `S14` · `S18` · `S20` · `S23` · `S24`.
- **recrop (표)**: `Table S1` (S24 캡션·S2 첫 행이 섞여 있었다) · `Table S2` (pp.18–20 세 쪽 이어붙임 — 'This work' 4행이 p.20) · `Table S3` (pp.20–21 이어붙임 — 'This work' 행이 p.21).
- 원래 PNG 는 지웠다 (같은 파일명 덮어씀) — 사유·이전 bbox 는 figures.json 각 항목에 남겼다.

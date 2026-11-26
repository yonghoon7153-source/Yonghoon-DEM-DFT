<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md (← zuo2022 계보)
     2026-11-26 신규 — 논문 에이전트 (API 실행 · 본문 13 pp + SI 40 pp 글자층 전문 정독 · 크롭 41 장 중 15 장 실독 + 확대 3 패널).
     그림 폴더는 `extract_figures.py --slug … --pdf <본문> <SI> --clean` 으로 만들었다 (손 크롭 없음 · missing_labels 0).
     공유 표 (INDEX · comparison_vs_ours · _sources.json · pdf_map) 는 이번 실행에서 건드리지 않는다 (호출자 지시) — _sources.json 은 실행 전 사본으로 되돌려 해시가 같다.
     우리 값 규율: band gap 은 상대차만 · MLIP-MD Ea/σ 는 O 효과로 쓰지 않는다 (HZ-cross-system-Ea BLOCKED · difference_with_lpsocl_as_O_effect) · BVSE 는 우리 것이 softBV 가 아니다. -->

# Function-Decoupled Dual-Anion Doping via Site-Preferential Regulation Enables High-Performance Lithium Argyrodite Electrolytes — Shi, Hu, Li et al. (*Adv. Energy Mater.* 2026, e71857)

> slug `shi2026_o16e_se4d_dual_anion_site_preferential_argyrodite` · DOI `10.1002/aenm.71857` · type `mixed — exp 주 (고상 합성 · XRD Rietveld · Raman · XPS · Se K-edge XANES/EXAFS/WT · EIS/Arrhenius · LSV · DC 분극 · H₂S 방출 · in situ Raman · Li‖Li CCD/장기 · NCM811 풀셀 · 파우치) + 계산 보조 (O '혼입 장벽' 4 개 · PDOS · 전하밀도차 · BVSE · PS₄ 가수분해 ΔG · H₂O 흡착 · Li|Li₂X 계면에너지 · Li₂X 이동 장벽 · VASP AIMD 2 계 50 ps) — 계산 방법은 AIMD 한 줄 말고 전부 미기재` · PDF `litdb/inbox/3. Function‐Decoupled Dual‐Anion Doping … Electrolytes.pdf` (본문 13 pp · sha256 앞 16 자 `535aacb7c3c78240`) + `litdb/inbox/3. Sup) Function‐Decoupled … Electrolytes.pdf` (SI 40 pp · Fig. S1–S29 · Table S1–S6 · 참고문헌 S1–S13 · sha256 앞 16 자 `4b2e464f9747d03f`) · digested `2026-11-26` · status ✅ · 태그 **[외부 · argyrodite 음이온 공도핑 · O(16e) / Se(4d) · 자리 선호]**
> elements: Li, P, S, Cl, O, Se
> methods: DFT, AIMD, NEB, PDOS, BVSE, XPS, Raman

> **저자**: **Yaru Shi**# · **Libin Hu**# · **Qiuhong Li**# (# 공동 1저자) · Wenhao Fang · Zheng Zhang · Xiaoyu Liu · Bing Zhao · **Yong Jiang\*** · **Shuixin Xia\*** · Xueliang Sun · **Jiujun Zhang\*** — 上海大学 环境与化学工程学院 (Shi · Hu · Li · Fang · Zhang · Zhao · Jiang) · 上海大学 理学院/可持续能源研究院 (Liu · Sun · J. Zhang) · 上海理工大学 材料与化学学院 (Xia) · 福州大学 新能源材料与工程研究院 (Sun · J. Zhang). 교신 jiangyong@shu.edu.cn · xiashx@usst.edu.cn · jiujun.zhang@i.shu.edu.cn.
> 접수 2026-07-24 · 수정 2026-10-28 · 수락 2026-11-11 · *Adv. Energy Mater.* 2026, 0: e71857 (권 · 쪽 미정). 자금: NSFC 22379091 · 22179080 · 52371230 · T2600758 · 中国博士后科学基金 2025M770115 · 上海大学 고성능 계산 센터 (계산 자원). 데이터는 '합당한 요청 시' 교신저자에게. 이해 상충 없음 선언.
> 기여 진술: Y. Shi 구상 · 조사 · 초고 · 방법 / Q. Li 구상 · 초고 · 형식 분석 · 데이터 / L. Hu · Z. Zhang 조사 / W. Fang 데이터 / X. Liu 구상 / B. Zhao 자금 · 관리 / Y. Jiang · S. Xia · J. Zhang 검토 — **DFT · AIMD 를 누가 했는지는 적혀 있지 않다.**
> **계보 (본문 인용)**: Kamaya 2011 LGPS (ref 5) · O 치환 argyrodite (Xu 2022 *EEM* ref 15 · Peng 2022 *ACS AMI* ref 16 · Cao 2025 *Small* Mo–O ref 17) → 양이온+O 공도핑 (In³⁺ Wang 2024 ref 18 · Shi 2024 *CEJ* ref 20 = **같은 1저자** · As⁵⁺ ref 21 · Sb⁵⁺ Liu 2025 ref 22 = litdb `liu2024_pband_center_sbo_dual_interface`) → **본 논문** (양이온 대신 **두 음이온** O · Se 를 '전구체로 자리를 고른다' 는 틀로).
> 🔗 **이어 읽기 (litdb)**: O 자리 = `park2026_oxygen_induced_li_intercage_conduction` (ND · O@16e) · `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal` · `zhang2026_odoping_argyrodite_o2_co2_dry_air` · `yang2025_lao_dualdoping_argyrodite_lacl3` / Se = `jiang2022_se_doped_lpscl_high_throughput_dft` (Se 를 **16e** 에 둔 DFT) / 공도핑 = `liu2024_pband_center_sbo_dual_interface` · `taklu2021_cucl_dualdoping_air_stability_argyrodite` · `li2025_cubr2_dualdoping_argyrodite` · `nosrati2026_anion_engineering_sulfide_se_review` — 대응은 §14.

---

## 0. 이 digest 를 읽는 법

**읽기축 (우리 트랙에서의 자리)**: 우리 LPSOCl (Li₅.₄PS₄.₂O₀.₂Cl₁.₆ · O 를 PS₄ 꼭짓점 = 16e 에 둔 **구성**) 과 같은 'O 치환 argyrodite' 계열이고, 우리 CEI 트랙 원고 (Nd/O · 1저자 = 실험 쪽) 의 O 자리 서술과 바로 닿는다. 가져올 것은 넷이다 — ① **O 자리 (4d vs 16e) 의 실험 증거 종류** (Rietveld 점유 · Raman 420 cm⁻¹ 세기 · P 2p 분율), ② **Se 자리 (4d vs 16e)** EXAFS 배위수 해석, ③ 계산 보고 규약의 **반례** (방법 미기재 장벽 · BVSE 1D/2D/3D 서술이 자기 그림과 어긋남 · 결정 계면 AIMD 50 ps 1 궤적), ④ 공기 안정성 · Li 금속 · 양극 성능 데이터 (σ · Ea · H₂S · CCD).

**판정 요약 (§6 · §10 상세)**:

| 주장 | 판정 | 핵심 근거 |
|---|---|---|
| 전구체가 O 자리를 정한다 — Li₂O → 4d · P₂O₅ → 16e (DFT '혼입 장벽' 1.33/2.17 vs 2.41/1.49 eV) | 🔴 계산 근거가 약하다 | 방법 전무 · 그림은 매끈한 사인 꼴 (영상 점 없음) · 슬랩 위 분자 덩어리 → 표면 아래 자리 경로 · **자리 에너지 (열역학) 를 안 냈다** · 500 °C 2 h 소성에서 '느린' 2.41 eV 경로도 ≈14 회 일어난다 (우리 홉 수 검산 §5.1) |
| 실험이 자리 차이를 보여 준다 | ⚠ 정성만 | Rietveld: A 는 4d 에 O 0.228/f.u. (명목 0.4 의 57 %) · B 는 16e 에 0.376/f.u. (94 %) · Raman 420 cm⁻¹ 세기 A 평탄 · B 감소 · P 2p PS₃O³⁻ 분율 A 10.7 % (= 무도핑 11.2 %) · B 17.1 %. 단 A 는 x ≥ 0.4 에서 Li₂S · LiCl 불순물 — 'O 가 4d 에 들어갔다' 와 'O 가 덜 들어갔다' 가 안 갈린다 |
| O(16e) 경로가 O(4d) 경로보다 수송 손해가 작다 | ✅ 방향 · ⚠ 교락 | x = 0.4 σ 2.51 vs 2.2 mS cm⁻¹ · Ea 0.365 ± 0.006 vs 0.391 ± 0.002 eV (세 셀) — 단 A 는 불순물상 포함 |
| Se 는 4d 에 '압도적으로' 앉는다 | ⚠ 과장 | EXAFS CN(Se–P) 0.45 ± 0.18 = 16e Se 비율 ≈ 27–63 % 와 맞는 값 · Rietveld 4d Se 0.247/f.u. = 명목 0.4 의 62 % → **둘 다 Se 의 ≈ 40 % 가 4d 밖** 을 시사 (§5.3 우리 산수) |
| Se 가 O 의 σ 손실을 메운다 | ✅ 본문 값 · ⚠ 그림과 어긋남 | 본문 LPSCl 3.19 · LPSSeCl 4.03 · LPSOSeCl 3.21 mS cm⁻¹ — `Fig. 3h` 298 K 점은 figure-read ≈3.2 · ≈6.5 · ≈4.1 mS cm⁻¹ |
| BVSE — O 는 '깊은 덫' · Se 는 1D → 2D 위상 전이 | 🔴 자기 그림이 부정한다 | 무도핑 (`Fig. S12`) 이미 1D = 2D = 3D = 0.354 eV · LPSOCl 0.361 · LPSSeCl 0.350/0.350/0.351 — 차 ≤ 0.011 eV · 무도핑에도 깊은 극소가 있다 |
| O 가 산화창을 넓힌다 | ⚠ LSV 문턱 정의 의존 · 자리 무관 | onset 2.84 (LPSCl) → 3.02 (A) · 3.00 (B) · 3.14/3.16 (LPSOSeCl) V — **A 와 B 가 같다** (자리가 상관없다) · 1.3 V 부터 전류가 흐른다 |
| 공기 안정성 (H₂S 40 %) — O(16e) 열역학 부동태 + Se 흡착 약화 | ✅ 측정 · ⚠ 계산 | H₂S 19.5 ppm (100 %) → LPSOSeCl 40 % · 계산 ΔG −2.28 → −1.17 eV 는 '첫 치환 vs 둘째 치환' 비교라 여전히 자발 · 이름이 본문 '반응 에너지' · 그림 'ΔG' · SI 캡션 '활성화 에너지' 셋 |
| CCD 2.6 mA cm⁻² · 4000 h · Li₂Se/Li₂O SEI | ✅ CCD · ⚠ 장기 서술 | `Fig. 5d` 범례대로면 **LPSO_BCl 이 ≈490 h 에서 단락 · LPSCl 은 ≈1150 h 까지** — 본문 (LPSCl 500 h · LPSO_BCl 1100 h) 과 반대 · LPSOSeCl 분극은 ≈±8 → ≈±30 mV 로 4 배 |
| AIMD — Se/O 가 계면 PS₄ 분해를 막고 Li₂Se/Li₂O 를 만든다 | 🔴 근거 약함 | 50 ps · 300 K · 1 궤적 · 셀 미기재 · Li–Se · Li–O RDF 띠는 **t = 0 부터** 일정 (SE 자체의 Li–Se/Li–O) · **Li/LPSOSeCl 에서도 LiₓPᵧ 가 생긴다** (`Fig. 5j` 오른쪽 · 그림 자체 주석) |
| NCM811 풀셀 500 cyc 70.7 % · 율 | ✅ 데이터 · ⚠ 비교 조건 | 적재량 4.45 / 4.58 / 5.47 mg cm⁻² 로 실험마다 다름 · 셀 1 개씩 · 비교표는 C-rate 가 섞임 |

**본 digest 에서 실제로 본 그림 (2026-11-26)** — 크롭 41 장 (본문 6 · SI 그림 29 · 표 6) 중:

- 원해상도로 본 것 **15 장**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. 6` (본문 전량) · `Fig. S1` · `Fig. S6` · `Fig. S7` · `Fig. S9` · `Fig. S10` · `Fig. S12` · `Fig. S17` · `Fig. S25` · `Fig. S26`.
- 확대해서 다시 읽은 패널: `Fig. 3c` · `Fig. 3h` · `Fig. 5d` (임시 확대 크롭 → 판독 뒤 지움).
- **안 본 것 (20 장)**: `Fig. S2` · `S3` · `S4` · `S5` · `S8` · `S11` · `S13` · `S14` · `S15` · `S16` · `S18` · `S19` · `S20` · `S21` · `S22` · `S23` · `S24` · `S27` · `S28` · `S29` — 이들에 대한 서술은 **본문 · SI 캡션 글자만** 근거다. 표 6 장 (`Table S1`–`Table S6`) 은 PDF 글자층으로 읽었다.
- 그림에서만 읽은 값은 **`figure-read ≈`** 로 적었다. 판독 정밀도는 눈금 간격의 ≈ ±3–5 %.

---

## 1. 한 줄 요약

Li₆PS₅Cl 에 O 를 넣을 때 **산소 원료가 Li₂O 면 O 가 4d (Li 우리 중심 '자유 S²⁻' 자리) 에, P₂O₅ 면 16e (PS₄ 꼭짓점) 에 주로 들어간다** 는 것을 DFT '혼입 장벽' 과 Rietveld · Raman · XPS 로 보이고, 그 규칙으로 O 는 P₂O₅ 로 16e 에 (공기 · 산화 안정), Se 는 Li₂Se 로 4d 에 (σ 보상 · Li₂Se 계면) 나눠 앉힌 **Li₆PS₄.₂O₀.₄Se₀.₄Cl (LPSOSeCl)** 을 만든다. 결과는 σ 3.21 mS cm⁻¹ (LPSCl 3.19 와 같음) · H₂S 40 % · CCD 2.6 mA cm⁻² · Li‖Li 4000 h (0.2 mA cm⁻²) · NCM811|Li-In 500 cyc 70.7 % (0.3 C). 실험 성능 데이터는 대체로 일관되지만, **'자리를 원료로 고른다' 의 계산 근거 (방법 없는 장벽 넷 · 자리 열역학 없음) 와 Se 의 '압도적 4d' 해석 (EXAFS · Rietveld 가 오히려 ≈40 % 가 4d 밖임을 시사)** 은 얇고, BVSE · AIMD · 장기 사이클 그림 몇 개는 본문 서술과 어긋난다.

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | Li₆PS₅Cl (LPSCl, 무도핑) · Li₆PS₅₋ₓOₓCl (x = 0.1–1.0, 0.1 간격) 두 갈래 — **LPSO_ACl** (O 원료 Li₂O) · **LPSO_BCl** (O 원료 P₂O₅) · Li₆PS₄.₆Se₀.₄Cl (**LPSSeCl**, Se 단독 · 조성은 본문에 안 적혀 있고 이름에서 추정) · **Li₆PS₄.₂O₀.₄Se₀.₄Cl (LPSOSeCl** = 본문 'LPSO_BSe_ACl' · 그림은 'LPSSeOCl' 로도 적음) |
| 양극 · 음극 | NCM811 : SE : Super P = 7 : 2 : 1 복합양극 · Li 금속 또는 Li-In |
| 질문 | O 치환은 공기 안정 · 산화창 · Li 금속 부동태를 주지만 Li⁺–O²⁻ 정전 인력으로 σ 를 깎는다. 기존 도핑은 PS₄³⁻ (중심 P · 꼭짓점 S) 만 건드렸다 — **4d 우리 중심 자리는 덜 탐색됐다.** 음이온이 4d 와 16e 에 어떻게 나뉘느냐가 수송 · 공기 · 계면을 어떻게 바꾸나? 그리고 고상 합성에서 자리를 '정확히' 고를 수 없다면, **원료 화학으로 자리 선호를 통계적으로 기울일 수 있나?** |
| 답 (저자) | Li₂O 는 O 를 4d 로, P₂O₅ 는 16e 로 '동역학적으로' 보낸다 → O 는 P₂O₅ 로 16e (P–O 로 사면체 안정화 · 산화창) · Se 는 Li₂Se 로 4d (격자 팽창 · 낮은 전기음성도 · Li₂Se 계면) 에 두어 **기능을 자리로 나눈다 ('function-decoupled')** (`Fig. 1`) |
| 저자 스스로 그은 선 | "absolute crystallographic site control … is experimentally challenging to achieve or verify" — **절대 자리 제어가 아니라 '우세 점유 (predominant)' · '통계적 농축'** 이라고 여러 번 적는다 |
| 연구 유형 | 실험 주 · 계산 보조 (계산 그림: `Fig. 2a,b` · `Fig. 3j–m` · `Fig. 4h,i` · `Fig. 5h–k` · `Fig. S1` · `S12` · `S17` · `S24`–`S26`) |
| 우리와의 거리 | 우리 LPSOCl (O@16e 구성) · CEI 트랙 O 자리 서술 · ESW (산화) 축 · 가수분해 축 · Li 금속 계면 축과 **정성적으로** 닿는다. 수치 비교는 방법이 달라 거의 안 된다 (§7) |

## 3. 핵심 수치 총정리 ★

> 규율: 아래는 전부 **문헌 소환값**이다 — 우리 db 절대값과 한 표에 섞지 않는다. 본문 명시값과 `figure-read ≈` 를 칸마다 구분한다. 온도는 따로 적지 않으면 실온.

### 3a. 구조 (Rietveld · `Table S1`–`Table S3` · `Fig. S9`)

| 시료 | a (Å) | V (Å³) | 자리 점유 (정련) | R_wp / R_p / χ² | 비고 |
|---|---|---|---|---|---|
| LPSCl (무도핑) | **10.28** (본문) | **1086.37** (`Fig. S9`) | 정련표 없음 | — | ⚠ 통상 LPSCl ≈ 9.85–9.86 Å (V ≈ 957 Å³) 와 크게 다르다 (§10-⑧) · 1086.37^(1/3) = 10.280 Å (우리 산수 — `Fig. S9` 와 본문은 서로 맞다) |
| Li₆PS₄.₆O₀.₄Cl (A, Li₂O) | 9.8556 (`Table S1`) · 본문 '9.857' | 957.3 | 4d: S 0.772 / **O 0.228** · 16e S 1.000 · 4a Cl 1.000 | 9.87 % / 3.15 % / **7.08** | Li1 48h (0.29, 0.025, 0.71) 0.370 · Li2 24g (0.25, 0.02, 0.75) 0.260 — 좌표 · 점유가 세 표 모두 같다 (고정으로 보인다) · 4d S/O U_iso 묶음 0.027 |
| Li₆PS₄.₆O₀.₄Cl (B, P₂O₅) | 9.8571 (`Table S2`) · 본문 '9.856' | 957.74 | 16e: S 0.906 / **O 0.094** · 4d S 1.000 | 7.44 % / 4.33 % / 2.94 | 본문의 A · B 격자상수 두 값이 표와 뒤바뀌어 있다 (≤ 0.0015 Å · 사소) |
| LPSOSeCl | **9.8970** (`Table S3`) | **969.42** | 4d: S 0.753 / **Se 0.247** · 16e: S 0.902 / **O 0.098** | 9.65 % / 6.76 % / 2.03 | 표 제목은 'Li₆PS₄.₂Se₀.₄O₀.₄Cl' · 표 안 시료명은 'Li₆PS₄.₆Se₀.₄O₀.₄Cl' (오기) · 본문 "close to the pristine LPSCl" ↔ `Fig. S9` (1086 vs 969) 모순 |
| 16e S 좌표 (세 표 공통) | x = 0.11643, −0.11643, 0.61643 | — | — | — | O 좌표를 S 좌표와 묶었다 (O 의 P–O 거리 수축을 모형이 허용하지 않는다) |

- **명목 대 정련 (우리 산수 · 4 f.u./셀 · 4d 1 개/f.u. · 16e 4 개/f.u.)**: x = 0.4 를 전부 4d 에 넣으면 4d 점유 **40 %**, 전부 16e 에 넣으면 16e 점유 **10 %**. 본문은 "designed 25 % and 10 %" 라 적는다 — **25 % 는 산수가 안 맞는다** (§10-⑨). 정련값을 f.u. 당 O 로 바꾸면 A 4d **0.228** (명목의 57 %) · B 16e 0.094 × 4 = **0.376** (94 %) · LPSOSeCl 16e 0.098 × 4 = **0.392** (98 %) · LPSOSeCl 4d Se **0.247** (명목 0.4 의 62 %).
- XRD: Rigaku D/max-2500 · Cu Kα (SI 는 λ = '1.50405 Å' — 1.5406 의 오기로 보인다 · 정련표는 Kα1 1.5406 / Kα2 1.5444) · 10–80° (`Fig. 4a` 는 90° 까지) · 2° min⁻¹. 표준 패턴은 Li₇PS₆ (PDF #34-0688). 무도핑 LPSCl 의 a = 10.28 Å 정련표는 없다.

### 3b. 수송 · 전자 · 산화 (실험)

| 양 | LPSCl | LPSO_ACl | LPSO_BCl | LPSSeCl | LPSOSeCl | 출처 · 비고 |
|---|---|---|---|---|---|---|
| σ_RT (mS cm⁻¹) | **3.19** | x 0.1→1.0: 2.82 · 2.66 · 2.35 · **2.2** · 1.98 · 1.86 · 1.7 · 1.65 · 1.42 · **1.34** | 2.99 · 2.87 · 2.73 · **2.51** · 2.36 · 2.22 · 2.06 · 1.92 · 1.53 · **1.42** | **4.03** | **3.21** | `Fig. S7` (막대 인쇄값) · `Fig. 3g` 삽입 막대 · 본문 — 차단 전극 · Ø 10 mm · ≈1 mm · 1 MHz–0.01 Hz · 5 mV · Rg–(Rgb‖CPE)–W 맞춤 |
| `Fig. 3h` 298 K 점 (1000/T ≈ 3.355) | figure-read log σ ≈ −2.50 → ≈3.2 | — | — | figure-read ≈ −2.19 → **≈6.5** | figure-read ≈ −2.39 → **≈4.1** | ⚠ Se 두 계는 본문 σ (4.03 · 3.21) 와 어긋난다 (§10-⑪) |
| Ea (eV) | **0.346** (그림 · 본문 '0.34') | **0.391 ± 0.002** (x = 0.4 · 세 셀 0.392 / 0.388 / 0.392) | **0.365 ± 0.006** (0.360 / 0.371 / 0.365) | **0.283** ('0.28') | **0.323** ('0.32') | `Fig. 3c,h` · `Table S5` · 온도 1000/T 2.79–3.36 (≈ 298–358 K · 7 점) · LPSCl 계열 Ea 는 셀 1 개 |
| x = 0.4 의 298 K σ (Arrhenius 그림) | — | figure-read log σ ≈ −2.66 → ≈2.2 | figure-read ≈ −2.62 → ≈2.4 | — | — | `Fig. 3c` (오른쪽 패널은 y 눈금 숫자 없음 · 왼쪽과 같은 축으로 가정) |
| 전자 전도도 | 기준 | ↓ | ↓ | — | LPSCl 보다 ↓ | `Fig. S8` · `Fig. S11` (DC 분극 · **안 본 그림** · 값은 본문에 없다) |
| LSV 산화 onset (V) | **2.84** | **3.02** | **3.00** | **2.97** | **3.16** (본문) · **3.14** (`Fig. 3i` 막대 · 화살표) | `Fig. 3i` · `Fig. S10` — 주사 속도 · 전극 구성 (탄소 혼합 여부) **미기재** · `Fig. S10` 에서 전류는 ≈1.3 V 부터 서서히 오른다 (figure-read ≈0.01–0.02 mA at 2.0–3.0 V) |
| Raman 420 cm⁻¹ (PS₄³⁻) 세기 | ≈15,300 (x = 0) | 13,500–16,700 사이 흩어짐 · 'relative range 21.0 %' | 15,300 → ≈6,900 (x = 1.0) · 'relative range 71.8 %' | — | — | `Fig. S6` (figure-read · 내부 표준 없음 · A 의 x = 0.9 점 없음) |
| P 2p 분율 (Argyrodite / PS₃O³⁻) | 88.8 / 11.2 % | 89.3 / 10.7 % | 82.9 / 17.1 % | — | — | `Fig. 2g` 원그래프 인쇄값 · 본문은 133 eV PO₄³⁻ 성분도 말하지만 그림 맞춤에는 성분 둘뿐 |
| S 2p 이동 | 161.1 eV (PS₄³⁻) | +0.2 eV | +0.4 eV | — | — | 본문 · `Fig. 2h` (sulfite 띠 ≈166.7 eV 표시 · 봉우리는 안 보임) |
| Li 1s | 55.5 eV (Li–S) | — | 55.5 | — | 55.5 + **53.2 eV (Li–Se)** · 약간 저결합 이동 | `Fig. S14` (안 본 그림) · 본문 |

### 3c. Se 국소 구조 (`Fig. 4b–e` · `Table S4` · S₀² = 1.03)

| 시료 | 경로 | CN | R (Å) | σ² (Å²) | ΔE₀ (eV) | R factor |
|---|---|---|---|---|---|---|
| Se 박 | Se–Se | 2 (고정) | 2.376 ± 0.004 | 0.0043 | 6.28 ± 1.21 | 0.0062 |
| Li₂Se | Se–Li | 8 (고정) | 2.600 ± 0.006 | 0.0067 | −0.33 ± 0.48 | 0.0095 |
| LPSOSeCl | Se–P/S | **0.45 ± 0.18** | **2.20 ± 0.052** | 0.0195 | −2.80 | 0.0184 |
| LPSOSeCl | Se–Li | **6.61 ± 0.60** | **2.50 ± 0.012** | 0.0083 | (같은 ΔE₀) | — |

### 3d. 공기 안정성

| 양 | LPSCl | LPSO_ACl | LPSO_BCl | LPSSeCl | LPSOSeCl | 출처 |
|---|---|---|---|---|---|---|
| H₂S 누적 (50 min · 30 % RH · RT) | **19.5 ppm (100 %)** | **68.2 %** (그림에만) | **48.2 %** | **83.1 %** | **40.0 %** | `Fig. 4f` · `Fig. S16` · 본문 — 200 mg · 0.785 cm² · 밀폐 ≈12 L · BAOSEAN BH-4 센서 |
| 공기 노출 뒤 σ | 3.19 → **0.53** (16.6 %) | — | — | — | 3.21 → **1.81** (56.4 %) | `Fig. S19` (안 본 그림) · 노출 시간 · 습도 본문 미기재 |
| 노출 뒤 XRD | 주상 거의 전부 → LiCl + Li₄P₂O₇ | — | — | — | 주봉 ≈50 % 유지 · LiCl 약간 | `Fig. S18` (안 본 그림) |
| in situ Raman (≈28 min) | ≈405 cm⁻¹ 봉우리가 figure-read ≈4–8 min 안에 사라짐 | — | — | — | 28 min 내내 유지 | `Fig. 4g` — **두 패널의 색 막대 범위가 다르다** (40–7800 vs 100–4780) · 봉우리 위치는 figure-read ≈405–410 (본문 '∼420') |

### 3e. 계산 (전부 문헌 소환값 · 방법은 §4e · §8)

| 양 | 값 | 출처 | 비고 |
|---|---|---|---|
| O '혼입 장벽' Li₂O → 4d / 16e | **1.33 / 2.17 eV** | `Fig. 2a` · 본문 | 끝점 에너지 figure-read ≈0 / ≈0.2 eV · 곡선은 매끈한 종 모양 (영상 점 없음) |
| O '혼입 장벽' P₂O₅ → 4d / 16e | **2.41 / 1.49 eV** | `Fig. 2b` · 본문 | 끝점 figure-read ≈0.2 / ≈0.1 eV · 모형 = 슬랩 위 원료 덩어리 (`Fig. S1`) |
| PDOS | O 2p–Li 2s 봉우리 figure-read ≈ −2.6 · −2.1 · −0.8 · −0.3 eV (LPSOCl) · Se 4p 봉우리가 0 eV (VBM) 바로 아래 (LPSSeCl) | `Fig. 3j` | 창 −4…+4 eV 에 전도띠 상태가 거의 안 보인다 · 범함수 미기재 |
| BVSE 이동 장벽 (1D / 2D / 3D) | LPSCl **0.354 / 0.354 / 0.354** · LPSOCl **0.361 / 0.361 / 0.361** · LPSSeCl **0.350 / 0.350 / 0.351** eV | `Fig. S12` · `Fig. 3l,m` | 본문은 LPSCl '1D' 0.354 · LPSSeCl '0.350 · 2D 로 전이' 만 적고 LPSOCl 0.361 은 안 적는다 · 국소 깊이 0.280 · 0.160 (LPSOCl) · 0.159 (LPSSeCl) · 0.093 · 0.161 · 0.283 (LPSCl 캡션) eV |
| PS₄ 가수분해 ΔG | PS₄ + H₂O → PS₃O + H₂S **−2.28 eV** · PS₃O + H₂O → PS₂O₂ + H₂S **−1.17 eV** | `Fig. 4h` · `Fig. S17` | 고립 음이온 (그림 표기 PS₄²⁻ · PS₃O²⁻ — 전하가 3− 가 아니라 2− 로 적혀 있다) |
| H₂O 흡착 (110) | LPSCl **−1.51 eV** · LPSSeCl **−0.77 eV** | `Fig. 4i` | LPSOSeCl 이 아니라 **LPSSeCl** 면 · 슬랩 · 자리 · 덮임 미기재 |
| Li(001)\|Li₂X(100) 계면에너지 | Li₂O **2.93** · Li₂S **2.04** · Li₂Se **1.32 J m⁻²** | `Fig. S26a` | 정의식 미기재 |
| Li₂X 내 Li 이동 장벽 | Li₂O **1.15** · Li₂S **1.07** · Li₂Se **0.86 eV** | `Fig. S26b` | 반응좌표 0–1 'Å' · 9 점 · 기구 (공공 · 틈새) 미기재 |
| AIMD 계면 RDF | P–S 2.02 Å · Li–P 새 봉우리 ≈2.5 Å · Li–Se 2.55 · Li–O 2.10 Å | `Fig. 5j,k` · `Fig. S24`–`S25` · 본문 | `Fig. S25` figure-read: Li–S ≈2.4 · Li–O ≈2.0 · Li–Se ≈2.6 Å |

### 3f. Li 금속 · 셀 성능

| 조건 | LPSCl | LPSO_ACl | LPSO_BCl | LPSSeCl | LPSOSeCl | 출처 · 비고 |
|---|---|---|---|---|---|---|
| CCD (mA cm⁻², RT) | **0.8** | **0.9** | **1.1** | **2.3** | **2.6** | `Fig. 5a–c` · `Fig. S20`–`S21` — 계단 figure-read ≈0.1 mA cm⁻² / ≈2 h · LPSOSeCl 2.5 mA cm⁻² 에서 분극 figure-read ≈ ±0.045 V |
| Li‖Li 0.2 mA cm⁻² · 0.2 mAh cm⁻² | 본문: ≈5 mV · 500 h 뒤 단락 · **그림 (범례대로): ≈1150 h 까지 · 끝 무렵 ±0.08 V** | — | 본문: ≈10 mV · > 1100 h · **그림: ≈450 h 에 전압 급등 · ≈490 h 에서 끝** | 1100 h (`Fig. S23` · 안 봄) | **4000 h** · figure-read ≈ ±0.008 V (0–20 h) → ≈ ±0.03 V (4000 h) | `Fig. 5d` — 본문과 그림이 LPSCl ↔ LPSO_BCl 에서 **반대** (§10-⑭) |
| Li‖Li 0.5 mA cm⁻² · 0.5 mAh cm⁻² | figure-read ≈330 h 까지 · ±0.06 V | — | — | — | **1600 h** · figure-read ≈ ±0.012 V (1200–1220 h) | `Fig. 5f,g` |
| NCM811\|SE\|Li · 0.1 C · 4.45 mg cm⁻² | 첫 figure-read ≈153 → 100 cyc **66.4 %** | — | — | — | **177.3 → 144.2 mAh g⁻¹ (81.33 %)** | `Fig. 6a` · 2.7–4.2 V vs Li⁺/Li · 1C = 200 mA g⁻¹ |
| NCM811\|SE\|Li-In · 0.1 C 첫 방전 | **156.2** | — | — | — | **200.3 mAh g⁻¹** | `Fig. 6c,d` — 2.4–3.7 V vs Li-In (≈3.0–4.3 V vs Li⁺/Li) · ⚠ 캡션은 (c) LPSOSeCl · (d) LPSCl 이지만 그림은 (c) LPSCl · (d) LPSSeOCl |
| 같은 셀 0.3 C · 5.47 mg cm⁻² | 3 cyc 뒤 93.6 · 100 cyc **64.6 %** | — | — | 사이 (`Fig. S29` · 안 봄) | **90.7 % (100) · 70.7 % (500)** | `Fig. 6e` · CE figure-read ≈100 % (LPSCl 은 ≈95–105 % 흩어짐) |
| 율 (0.1 / 0.3 / 0.5 / 1 / 2 C → 0.1 C) · 4.58 mg cm⁻² | 160.3 / 135.6 / 108.8 / 64.6 / **12.8** → 121.8 | — | — | 사이 | 199.2 / 173.5 / 128 / 85.5 / **43.1** → 195.5 mAh g⁻¹ | `Fig. 6b` · 본문 |
| 파우치 | — | — | — | — | LED 점등 · 접기 · 자르기 뒤 작동 (정성) | `Fig. 6h` — 용량 · 적재 · 사이클 없음 |

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 합성
- 원료 (Alfa Aesar): Li₂S > 99.9 % · P₂S₅ > 99 % · LiCl > 99.9 % · Li₂O 99.9 % (A) · P₂O₅ 99.9 % (B · LPSOSeCl) · Li₂Se > 99.9 % (LPSOSeCl).
- 고에너지 볼밀 (POWTEQ BM20) · ZrO₂ 용기 · ZrO₂ 볼 · **500 rpm 20 h** → **진공 500 °C 2 h** 소성. 볼 : 분말 비 · 볼 크기 · 냉각 · 분쇄 휴지 **미기재**.
- LPSOSeCl 설계: Li₂S 일부 → Li₂Se · P₂S₅ 일부 → P₂O₅ ("partially substituting Li₂S to Li₂Se and P₂O₅ to P₂S₅" — 문장 방향이 뒤집혀 있다). LPSSeCl 의 합성 · 조성 줄은 SI 에 없다 (셋 = A · B · LPSOSeCl 만).
- 수분 관리: Ar 글러브박스 H₂O · O₂ < 0.1 ppm. XPS 시료 이송 중 표면 수분 노출이 있었다고 저자가 스스로 쓴다 (P 2p PS₃O³⁻ 해석).

### 4b. 전기화학
- **σ · Ea**: 분말 → Ø 10 mm · ≈1 mm 펠렛 (압력 미기재) · Solartron 1400 · 1 MHz–0.01 Hz · 5 mV · 25–85 °C 대략 (그림 1000/T 2.79–3.36). x = 0.4 두 시료만 셀 3 개 (`Table S5`) · 나머지는 1 개.
- **LSV**: 조건 (전극 · 주사 속도 · 상대 전극) **완전 미기재** · onset 은 그림의 꺾인 점에 화살표.
- **DC 분극 (전자 전도도)**: 조건 · 값 미기재.
- **Li‖Li**: PEEK 셀 · SE 320 MPa 5 min → Li 두 장 120 MPa 2 min · LAND-CT2001A · RT · **스택 압력 (작동 중) 미기재** · Li 두께 미기재 · CCD 계단 시간 그림에서만 (≈1 h 증착 + 1 h 박리로 보인다).
- **풀셀**: 복합양극 NCM811 : SE : Super P = **7 : 2 : 1** (양극 코팅 없음으로 보인다 — 기재 없음) · SE 320 MPa 예압 → 양극 펴고 320 MPa → 음극 120 MPa 2 min · 볼트 체결 (토크 · 압력 미기재) · 적재 4.45 (Li) · 4.58 (율) · 5.47 (장기) mg cm⁻² · Li-In 2.4–3.7 V (≈3.0–4.3 V vs Li⁺/Li) · Li 2.7–4.2 V.
- **H₂S**: RT · 30 % RH · ≈12 L 밀폐 · 200 mg · 0.785 cm² · 50 min · BAOSEAN BH-4.

### 4c. 분석
- SEM/EDS JEOL JSM-7500F (5 kV) · XPS ESCALAB 250Xi Al Kα · Raman HORIBA XploRA PLUS (레이저 파장 · 출력 미기재) · Se K-edge XAS (빔라인 · 측정 모드 **미기재**) · EXAFS 맞춤 (프로그램 · k 범위 · R 범위 미기재 · S₀² 1.03 고정) · 웨이블릿 변환 (모 함수 미기재).

### 4d. 사이클 뒤 분석
- Li‖Li 사이클 뒤 Li 1s XPS (`Fig. S22` · 안 봄) — Li₂O/Li₂Se 계면 근거.
- NCM811/SE 10 사이클 뒤 P 2p · S 2p XPS (`Fig. 6f,g`).
- EIS 맞춤 (풀셀 50 cyc 전후 · `Fig. S28` · 안 봄).

### 4e. 계산 (전부) ★

| 계산 | 적힌 것 | 안 적힌 것 |
|---|---|---|
| **O '혼입 장벽'** (`Fig. 2a,b` · `Fig. S1`) | 결과 넷 · 구조 그림 (슬랩 + 진공 · 위에 Li₂O 또는 P₂O₅ 덩어리 · 빨간 점선 경로) | **전부** — 코드 · 범함수 · NEB 여부 · 영상 수 · 경로 정의 · 슬랩 면 · 두께 · 원료 덩어리 조성 · 끝점이 어떤 결함 상태인지 (무엇이 빠지고 들어가는지) · 전하 보상. Computational 절에 없다 |
| **PDOS · 전하밀도차** (`Fig. 3j,k`) | 그림 | 범함수 · k · 셀 · O/Se 배치 · 등치면 값 |
| **BVSE** (`Fig. 3l,m` · `Fig. S12`) | 결과 · 참고문헌 [34] | 프로그램 (softBV 로 보이나 확인 불가) · 격자 간격 · 구조 (실험 정련인지 DFT 인지) · 도펀트 배치 |
| **가수분해 ΔG** (`Fig. 4h` · `Fig. S17`) | 반응식 둘 · 값 둘 | 고립 음이온인지 결정인지 · 열 보정 (ZPE · 엔트로피 → 'ΔG' 근거) · 용매 · 전하 처리 |
| **H₂O 흡착** (`Fig. 4i`) | (110) 면 · 값 둘 | 슬랩 · 자리 · 덮임 · 기준 상태 · 분산 보정 |
| **Li\|Li₂X 계면 · Li₂X 이동** (`Fig. S26`) | 면 (Li(001) · Li₂X(100)) · 값 | 계면 정의 (계면 에너지 vs 점착일) · 변형 정합 · 이동 기구 |
| **AIMD** (`Fig. 5h–k` · `Fig. S24`–`S25`) | **VASP · NVT · 2 fs · 50 ps · 300 K** · RDF 는 `vasppy` | 범함수 · ENCUT · k · 셀 크기 · 원자 수 · Li 층 수 · SE 면 · 열욕 · 초기 평형 · 시드 수 (하나로 보인다) |

> 정리: Computational Section 은 **AIMD 한 문단뿐**이다. 나머지 계산 그림 여덟 개 (장벽 · PDOS · 전하밀도 · BVSE · ΔG · 흡착 · 계면 · 이동) 는 방법이 아예 없다.

---

## 5. 결과 — 절별 상세 (그림 실독 포함 · 모든 수치)

### 5.1 원료가 O 자리를 정한다 — DFT 장벽 (`Fig. 2a,b`, `Fig. S1`, `Fig. S2`) ★

- **주장**: Li₂O 에서 O 가 4d 로 들어가는 장벽 **1.33 eV** < 16e **2.17 eV** · P₂O₅ 에서는 16e **1.49 eV** < 4d **2.41 eV** → "원료 화학이 우세 경로를 정하고 · 무작위가 아니라 통계적 농축".
- **그림 실독 (`Fig. 2a,b`)**: 네 패널 모두 x 축 'Coordinate' 0–2 (단위 없음) · y 축 0–3 eV. 곡선은 **점 없는 매끈한 종 (사인) 모양** — NEB 영상 점이 하나도 안 찍혀 있다. 끝점 에너지 figure-read: Li₂O→4d ≈0 → ≈ −0.05 · Li₂O→16e ≈0 → ≈0.2 · P₂O₅→4d ≈0 → ≈0.2 · P₂O₅→16e ≈0 → ≈0.1 eV. 아래 구조 그림: 슬랩 위에 Li₂O (Li–O 덩어리 · 위쪽) 또는 P₂O₅ (분홍 사면체 세 개 덩어리) 가 있고, **빨간 점선 (O 경로)** 이 표면에서 격자 속 자리 (O@4d · O@16e · 'O@16' 오기) 로 내려간다.
- **`Fig. S1` 실독**: 진공층이 있는 **슬랩** 셀 네 개 (점선 상자) · 위쪽 원료 덩어리 · 화살표가 가리키는 대상 자리 (빨간 점선 원). 즉 '장벽' 은 **원료 덩어리 표면 → 슬랩 아래 자리로 O 하나가 몇 Å 넘게 옮겨 가는 경로** 의 꼭대기다. 무엇이 자리를 비워 주는지 (S 가 어디로 가는지) · 전하 균형이 어떻게 맞는지 그림에서 안 보인다.
- **`Fig. S2`** (안 봄): LPSCl · LPSO_ACl · LPSO_BCl 결정 구조 그림 (캡션).
- **우리 홉 수 검산** (`D-2026-09-27-barrier-hop-count` · ν₀ 10¹³ s⁻¹ **가정**):
  - 소성 500 °C (773 K) · 2 h (7200 s): 1.33 eV → Γ ≈ 2.1 × 10⁴ s⁻¹ (대기 ≈47 µs) · 1.49 eV → Γ ≈ 1.9 × 10³ s⁻¹ · **2.17 eV → Γ ≈ 0.072 s⁻¹ (대기 ≈14 s · N(2 h) ≈ 5 × 10²)** · **2.41 eV → Γ ≈ 2.0 × 10⁻³ s⁻¹ (대기 ≈8.5 min · N(2 h) ≈ 14)**.
  - 같은 온도에서 두 경로의 속도비는 e^{−0.84/kT} ≈ 3 × 10⁻⁶ (Li₂O) · e^{−0.92/kT} ≈ 1 × 10⁻⁶ (P₂O₅) — **'처음 어디로 들어가나' 의 비율** 로는 큰 차이다. 하지만 '느린' 경로도 소성 시간 안에 수십–수백 번 일어날 수 있으니, 최종 점유가 그 첫 비율에 **갇혀 있으려면** 들어온 뒤 4d ↔ 16e 재배치 장벽이 높아야 한다. 그 장벽과 두 자리의 **열역학 에너지 차** 를 논문은 내지 않았다 (§10-①).
  - 실온 (298 K) 에선 1.33 eV 도 대기 ≈ 3 × 10⁹ s (≈ 100 년) — 이 장벽들은 합성 온도에서만 의미가 있다. 20 h 볼밀 국소 온도는 미상.

### 5.2 두 갈래의 상 안정 · 자리 지문 (`Fig. 2c–h`, `Fig. S3`–`S6`, `Table S1`–`S2`)

- **XRD (`Fig. 2c,d` 실독 · 본문은 '`Fig. 2a`' 라고 잘못 가리킴)**: 둘 다 F-43m argyrodite 유지 (x = 0.1–1.0). 그림에 Li₂S · LiCl 위치 띠가 표시돼 있다. A (Li₂O): 본문 "x_A ≥ 0.4 에서 Li₂S (PDF#26-1188) · LiCl (PDF#04-0664) · x_A = 0.9 에서 심한 비정질화" — 그림에서 x_A 0.9 · 1.0 곡선의 봉우리가 낮고 넓다. B (P₂O₅): x_B 0.1–1.0 상 순수 · 날카로운 봉우리. 오른쪽 확대 (2θ ≈ 29.5–31.5°) 에서 B 의 x_B = 1.0 봉우리가 고각으로 더 많이 이동 (figure-read).
- **해석 (저자)**: 16e 자리는 셀당 16 개 · 4d 는 4 개라 **16e 가 O 를 더 많이 받아도 구조가 버틴다**.
- **Rietveld (`Table S1`–`S2` · `Fig. S5` 안 봄)**: x = 0.4 에서 A 는 4d O **22.8 %** · B 는 16e O **9.4 %** — 본문 "설계값 25 % · 10 % 에 가깝다" (§3a 산수: 4d 설계값은 40 %). a = 9.8556 (A) · 9.8571 Å (B) · 본문 "10.28 Å 에서 줄었다".
- **SEM (`Fig. S4` · 안 봄)**: 두 갈래 입자 크기 · 불규칙 응집 비슷 (캡션 · 본문).
- **Raman (`Fig. 2e,f` 실독 · 본문은 '2c/2d' 로 잘못 가리킴)**: 420 cm⁻¹ (PS₄³⁻) 열지도 · x 0.1–1.0. A (Li₂O): 전 범위에서 빨강 (최대 세기) 유지 · 봉우리 위치 figure-read ≈422–425 cm⁻¹ 로 살짝 흔들림. B (P₂O₅): x ≈ 0.1–0.2 에서만 빨강 · 그 위는 노랑-초록 (세기 ↓). 두 열지도 색 막대 모두 1–100 % 상대 눈금 — **각 열지도 안에서 정규화** 한 것으로 보여 두 패널 절대 세기 비교는 안 된다.
- **`Fig. S6` 실독 (정량)**: 세기 (a.u.) vs x. A: 16,700 (0.1) · 15,700 (0.2) · 14,500 (0.3) · 13,500 (0.4) · 13,900 (0.5) · 14,300 (0.6) · 16,200 (0.7) · 14,900 (0.8) · — (0.9 점 없음) · 15,900 (1.0) (figure-read) · 직선 맞춤 거의 평탄 · 'relative range 21.0 %'. B: 15,300 (0) · 15,200 · 13,300 · 12,700 · 11,500 · 11,850 · 11,300 · 10,800 · 10,700 · 8,800 · **6,900** (1.0) · 'relative range 71.8 %'. 내부 표준 · 초점 보정 없음 — Raman 절대 세기를 농도로 읽는 것은 시료 충전 · 초점에 민감하다 (§10-⑥).
- **P 2p XPS (`Fig. 2g` 실독)**: 맞춤 성분 둘 (Argyrodite ≈131.5 eV · PS₃O³⁻ ≈132.6 eV · 띠 표시). 원그래프: LPSCl 88.8 / 11.2 · LPSO_ACl 89.3 / 10.7 · LPSO_BCl 82.9 / 17.1 %. 본문은 '133 eV PO₄³⁻' 도 있다고 쓰지만 그림 맞춤 성분에는 없다. 저자: A 의 PS₃O³⁻ 는 "이송 중 표면 수분" 탓 · B 의 증가는 P₂O₅ 유래 P–O.
  - **우리 산수**: x = 0.4 의 O 가 전부 16e 에 PS₃O 로 하나씩 흩어지면 P 의 ≈40 % 가 PS₃O 여야 한다 (Rietveld B 0.376 O/f.u. 이면 ≈38 %). XPS 증가분은 **+5.9 %p** (11.2 → 17.1) 뿐이다. XPS 는 표면 수 nm 만 보니 벌크와 같을 이유는 없지만, 이 차는 "B 의 O 가 16e" 를 정량으로 받치지 못한다 (§10-⑦).
- **S 2p (`Fig. 2h` 실독)**: 161.1 eV 쌍 · sulfite 위치 띠 (≈166.7 eV) 에 눈에 띄는 봉우리 없음. 이동 A +0.2 · B +0.4 eV (본문). 저자 해석: "S–O 결합은 없지만 전기음성 O²⁻ 가 이웃 원자에 'metallic character' 를 유도해 결합에너지 ↑" — 이 문장은 물리적으로 이상하다 (§10-⑩).
- **결론 (저자)**: "Li₂O 는 4d · P₂O₅ 는 16e 농축을 이끈다".

### 5.3 O 의 자리별 수송 · Se 보상 (`Fig. 3a–i`, `Fig. S7`–`S11`, `Table S5`)

- **EIS (`Fig. 3a,b` 실독)**: 고주파 반원 (입계) + 저주파 Warburg 꼬리 · 등가회로 Rg–(Rgb‖CPE)–Ws. ⚠ `Fig. 3a` 는 A 갈래 (파랑) 인데 범례가 'X_B = 0.1 … 1.0' 이다 (라벨 오기). x = 1.0 (A) 은 ≈ 85–100 Ω 의 큰 반원 (figure-read) — 불순물상 · 비정질화와 맞는 모양.
- **σ 경향 (`Fig. S7` 실독)**: §3b 표 그대로 · 유지율 선 (오른쪽 축) — B 가 모든 x 에서 A 보다 높다 (x = 0.4 에서 2.51 vs 2.2 = 79 % vs 69 %). x = 1.0 에서 1.42 vs 1.34.
- **Ea (`Fig. 3c` 실독 + `Table S5`)**: 7 점 · 점마다 작은 오차막대 · 삽입 막대 0.391 (오차 figure-read 0.388–0.3945) · 0.365 (0.360–0.371). A 의 1000/T ≈ 3.15 점이 직선에서 아래로 벗어나 있다. 저자: "오차막대가 안 겹친다 → O(16e) 경로가 동역학 손해가 작다".
- **전자 전도도 (`Fig. S8` · 안 봄)**: O 도핑 두 갈래 모두 '현저히' 감소 (값 없음).
- **BVEL 그림 (`Fig. 3d–f` 실독)**: 셀 그림 · 청록 등치면 + 가운데 'Inter-cage zone' 붉은 다각형. 라벨: LPSCl 'Unmodified migration' · LPSO_ACl 'Inhibited migration & inter-cage jump' · LPSO_BCl 'Activated inter-cage jump'. 본문: 무도핑 = '얇–넓–얇 올리브 모양' · A = '납작한 모래시계 · 심하게 수축' · B = 'inter-cage 영역으로 경로 일부 확장 (주황색)'. **등치면 값 · 계산 조건이 없어서** 세 그림의 차이를 정량으로 비교할 수 없다 — 눈으로 봐도 세 등치면 모양 차이는 작다.
- **Se 도입**: "O(16e) 도 σ 손실을 다 못 막는다 → 큰 반경 · 낮은 전기음성도 Se 를 4d 에" → LPSOSeCl 설계.
- **`Fig. 3g` 실독**: 삽입 막대 3.19 · 4.03 · 3.21 mS cm⁻¹ · Nyquist 첫 절편 figure-read LPSSeCl ≈16 · LPSOSeCl ≈25 · LPSCl ≈28 Ω.
- **`Fig. 3h` 실독 (확대)**: 세 직선 · 범례 Ea LPSCl **0.346** · LPSSeCl **0.283** · LPSOSeCl **0.323 eV**. 298 K 점 figure-read LPSCl ≈ −2.50 (≈3.2 mS cm⁻¹ · 본문과 일치) · LPSSeCl ≈ −2.19 (**≈6.5**, 본문 4.03) · LPSOSeCl ≈ −2.39 (**≈4.1**, 본문 3.21). 고온 끝 (1000/T ≈ 2.79): LPSSeCl ≈ −1.39 · LPSOSeCl ≈ −1.49 · LPSCl ≈ −1.51.
- **LSV (`Fig. 3i` 실독 · 캡션은 '(l)' 로 오기)**: 0–4 V · 0–0.12 mA. 삽입 막대 2.84 · 2.97 · **3.14 V** (본문 LPSOSeCl **3.16 V**). 세 곡선 모두 ≈1.0 V 부터 전류가 서서히 올라 2.5 V 에서 figure-read ≈0.012–0.015 mA · 꺾임 뒤 3.5 V 근처 봉우리 (LPSCl ≈0.108 · LPSSeCl ≈0.11 이상 · LPSOSeCl ≈0.08 mA).
- **`Fig. S10` 실독**: LPSO_ACl 3.02 V · LPSO_BCl 3.00 V — **두 자리 갈래가 같다**. 둘 다 1.3–1.5 V 부터 전류가 흐르고 A 는 ≈2.3 V 에 작은 어깨.
- **`Fig. S11` (안 봄)**: LPSOSeCl 전자 전도도 < LPSCl (본문).

### 5.4 전자 구조 · BVSE — 'Se 가 왜 빠른가' (`Fig. 3j–m`, `Fig. S12`) ★

- **PDOS (`Fig. 3j` 실독)**: 위 LPSOCl (O 2p 청록 · Li 2s 빨강) · 아래 LPSSeCl (Se 4p 파랑 · Li 2s 빨강) · −4 … +4 eV · 점선 0 eV. LPSOCl: O 2p 날카로운 봉우리 ≈ −2.6 (가장 큼) · −2.1 · −0.8 eV · Li 2s 는 −2.1 · −0.3 eV 근처 봉우리. LPSSeCl: Se 4p 봉우리 ≈ −0.6 · −0.5 · **≈ 0 eV (가장자리)**. 두 패널 모두 **0 eV 위 (빈 상태) 에 거의 아무것도 없다** (LPSSeCl 4 eV 끝에 아주 작은 빨강) — 창 안에 전도띠가 안 보이는 이유가 설명되지 않는다.
  - 저자 해석: "LPSOCl 에서 Fermi 준위 근처 O 2p–Li 2s 혼성 = 공유결합적 상호작용 = '정전 덫'" · "Se 4p–Li 2s 는 약하고 비편재". ⚠ 원자 구 안 PDOS 에서 Li 2s 가 음이온 p 봉우리와 같은 에너지에 나오는 것은 이웃 음이온 꼬리가 Li 구에 들어온 것이라 흔한 모양이다 — '혼성 세기' 를 말하려면 COHP 같은 결합 분석이 필요하다 (§10-④). 오히려 그림이 보여 주는 것은 **Se 4p 가 가전자띠 꼭대기를 만든다 (갭이 줄 방향)** 인데 논문은 언급하지 않는다.
- **전하밀도차 (`Fig. 3k` 실독)**: O 주위 노랑 · 청록 등치면이 작고 조밀 · Se 주위는 넓다. 등치면 값 없음.
- **BVSE (`Fig. 3l,m` · `Fig. S12` 실독)**:
  - `Fig. S12` (LPSCl): y 0–0.5 eV · x 0–20 Å · **'1D = 0.354 · 2D = 0.354 · 3D = 0.354'** 가 그림에 인쇄돼 있다. 깊은 극소 두 개 (≈1.8 · ≈12.9 Å 에서 0 eV) · 봉우리 ≈0.354. 캡션은 "1D 경로 · 거시 장벽 0.354 eV · 주기 요동 0.093 · 0.161 · 0.283 eV".
  - `Fig. 3l` (LPSOCl): **E(1D) = E(2D) = E(3D) = 0.361 eV** · 깊은 극소 ≈0.06 eV (x ≈ 8.7 Å) · 주석 0.280 · 0.160 eV.
  - `Fig. 3m` (LPSSeCl): **E(1D) = 0.350 · E(2D) = 0.350 · E(3D) = 0.351 eV** · x 축 0–20 다음 끊김 → 55–60 Å (초록 곡선 한 봉우리) · 주석 0.159 eV.
  - 본문: "무도핑 = 1D 주기 지형 0.354 · O = 험한 지형 · 깊은 국소 덫 (예 0.280 eV) · Se = 매끈 · 0.350 eV 로 낮춤 · **파랑 곡선이 2D 침투망으로의 위상 전이** · 1D/2D (0.350) 와 3D (0.351) 차가 무시할 만 → 등방".
  - **그림과 대조**: ① 무도핑도 이미 1D = 2D = 3D 다 — 'Se 가 1D 를 2D 로 바꾼다' 는 자기 그림이 부정한다. ② 세 계의 장벽 차는 0.361 − 0.350 = **0.011 eV** — 실험 Ea 차 (0.346 → 0.283 · 0.063 eV) 의 1/6 이고 BVSE 의 매개변수 불확도 안이다. ③ '깊은 덫' 은 무도핑 지형에도 있다 (0 eV 극소 두 개 · 그 깊이 ≈0.28–0.35 eV). ④ 본문은 LPSOCl 의 0.361 을 안 적는다 — O 가 장벽을 0.007 eV 올린다는 것이 이 그림의 실제 결과다.
- **결론 (저자)**: "전자적 · 위상적 보상이 LPSOSeCl σ 회복을 설명한다" — BVSE 숫자로는 받쳐지지 않는다 (§10-③).

### 5.5 Se 의 자리 · 국소 배위 (`Fig. 4a–e`, `Fig. S13`, `Fig. S14`, `Table S3`, `Table S4`) ★

- **XRD Rietveld (`Fig. 4a` 실독)**: 10–90° · Observed/Calculated/Difference/Bragg · 차 곡선 평탄 · 15–20° 에 넓은 비정질 둔덕 (케이프톤 창 또는 비정질상 — 언급 없음). a = 9.8970 Å · V = 969.42 Å³ · LPSO_BCl 보다 큼 (Se 반경 · 낮은 전기음성).
- **SEM/EDS (`Fig. S13` · 안 봄)**: S · Se 고르게 분포 (본문).
- **Li 1s (`Fig. S14` · 안 봄)**: 55.5 eV (Li–S) + LPSOSeCl 에서 53.2 eV 새 봉우리 (Li–Se · ref 35) → "8 면체 우리가 4d 중심에 Se²⁻ 를 받는다" · 약간 저결합 이동 (LPSO_BCl 과 반대) = Se 의 약한 전자 끌기.
  - ⚠ Li 1s 에서 2.3 eV 떨어진 별도 봉우리는 이례적으로 크다 (Li 1s 화학 이동은 보통 1–2 eV 안). 그리고 Li–Se 결합은 Se 가 4d 든 16e 든 생긴다 (16e S 도 Li 3 개와 닿는다) — Li–Se 의 존재는 자리를 가르지 못한다 (§10-⑤).
- **XANES (`Fig. 4b` 실독)**: 12,500–13,000 eV · 확대 12,620–12,700 eV. LPSOSeCl 흡수단 · 백색선이 Li₂Se 와 같은 위치 (figure-read ≈12,657 eV) · Se 박은 더 낮은 쪽 날카로운 봉우리 → Se²⁻ · 금속 Se · Se–Se 없음.
- **FT-EXAFS (`Fig. 4c` 실독)**: y 축 라벨은 '|FTχ(k)·k²|' (캡션은 k³ 가중 — 불일치). 0–6 Å. LPSOSeCl: 첫 봉우리 ≈2.0 Å ('Se-Li (Se-P)' 라벨) · **둘째 봉우리 ≈3.4 Å 가 첫 봉우리보다 크다**. Li₂Se: 첫 ≈2.1 Å · 둘째 ≈4.0 Å (가장 큼). Se 박: ≈2.05 Å 한 봉우리 (가장 큼).
- **맞춤 (`Table S4`)**: Se–Li CN **6.61 ± 0.60** · R **2.50 Å** · Se–P/S CN **0.45 ± 0.18** · R **2.20 Å** · R factor 0.0184. 저자: "6.61 vs 0.45 의 큰 차 = 대다수 Se 가 4d 에서 Li 와 배위" · "소량이 16e 에서 P–Se".
- **WT (`Fig. 4d,e` 실독 · 본문은 '`Fig. 3l/3k`' 로 잘못 가리킴)**: LPSOSeCl — 가장 센 극대가 **R + ΔR ≈ 3.3 Å · k ≈ 4.5 Å⁻¹** (빨강) · 그 아래 R ≈ 1.9 Å · k ≈ 2–6 Å⁻¹ 에 'Se-Li' 라벨 · k ≈ 7 Å⁻¹ 쪽 꼬리에 'Se-P' 라벨. Li₂Se — 극대 R ≈ 3.9 Å · k ≈ 8 Å⁻¹ · 'Se-Li' 는 R ≈ 2 Å. 본문 "≈3.0 Å · 저 k 5–7 의 지배적 극대 = 가벼운 원소 (Li) 산란 = Se–Li 배위" — ⚠ 그림에서 'Se-Li' 라벨은 그 극대가 아니라 ≈1.9 Å 띠에 붙어 있다. ≈3.3 Å 극대는 **둘째 껍질** 이고, k ≈ 4.5 Å⁻¹ 의 둘째 껍질을 'Li' 로 판정하려면 경로 맞춤이 필요한데 그 껍질은 맞추지 않았다 (`Table S4` 는 첫 껍질만).
- **우리 산수 — Se 가 정말 '압도적' 4d 인가** (§10-②):
  - 16e 자리 Se 는 P 하나와 ≈2.1–2.2 Å 에서 결합하고 4d 자리 Se 는 P 와 직접 결합이 없다 (4d–P 거리 ≈ 4 Å 이상 — argyrodite 기하 일반 지식). 그러면 **CN(Se–P) ≈ 16e 에 앉은 Se 의 비율 f** 다. 맞춤값 0.45 ± 0.18 은 **f ≈ 0.27–0.63** 을 뜻한다.
  - Rietveld 는 4d Se 0.247 / f.u. → 명목 0.4 중 **62 %** 만 4d · 나머지 38 % 는 정련 모형 밖 (16e 에 Se 를 허용하지 않았다).
  - 두 독립 측정이 같은 방향 (**Se 의 ≈ 40 % 가 4d 가 아니다**) 을 말한다. "vast majority … 4d" · "only a trace amount of Se–P" 는 그 데이터보다 세다. 정직한 문장은 "Se 의 다수 (≈ 60 %) 는 4d · 상당 부분 (≈ 40 %) 은 16e" 다.
  - CN(Se–Li) 6.61 도 4d 와 16e 를 가르지 못한다 — 4d 자유 음이온의 Li 배위 (부분 점유 48h/24g) 와 16e S 의 Li 배위 수가 정확히 얼마인지에 따라 둘 다 3–7 범위가 나온다 (자리별 기대 CN 을 논문이 내지 않았다).
- **higher shell**: R > 4 Å 신호 위치가 Li₂Se 와 다르다 → "Li₂Se 불순물이 아니라 격자에 박혔다" — 이 부분은 그림이 받친다 (둘째 껍질 위치 ≈3.3–3.4 vs ≈4.0 Å).

### 5.6 공기 안정성 (`Fig. 4f–i`, `Fig. S15`–`S19`) ★

- **H₂S (`Fig. 4f` 실독)**: 0–50 min · 0–20 ppm. LPSCl ≈19.6 ppm (100 %) · LPSO₀.₄ₐCl **68.2 %** · LPSO₀.₄ᵦCl **48.2 %** · LPSOSeCl **40.0 %** (그림 인쇄). 넷 다 50 min 에 **포화하지 않았다** (LPSCl 은 계속 오름). 본문은 LPSO_ACl 68.2 % 를 언급하지 않는다 — 4d O 도 H₂S 를 32 % 줄이고, 16e O 는 52 % 줄인다. `Fig. S16` (안 봄): LPSSeCl 83.1 %.
- **in situ Raman (`Fig. 4g` 실독)**: 100–700 cm⁻¹ · 0–28 min. LPSOSeCl: ≈405 cm⁻¹ 선이 28 min 내내 진하다 (색 막대 100–4780). LPSCl: t ≈ 0–2 min 에 진한 점 · ≈4–8 min 안에 사라짐 (색 막대 40–7800). ⚠ 같은 습도 조건인지 · 레이저 손상 · 초점 이동을 어떻게 다뤘는지 미기재 · LPSCl 이 수 분 만에 PS₄ 신호를 다 잃는다는 것은 H₂S 곡선 (50 min 에도 증가 중) 과 시간 규모가 다르다.
- **노출 뒤 XRD · σ (`Fig. S18`–`S19` · 안 봄)**: LPSCl → LiCl + Li₄P₂O₇ · σ 0.53 mS cm⁻¹ (16.6 %) / LPSOSeCl 주봉 ≈50 % · σ 1.81 (56.4 %).
- **가수분해 DFT (`Fig. 4h` · `Fig. S17` 실독)**: PS₄ + H₂O → PS₃O + H₂S **ΔG = −2.28 eV** ('easy') · PS₃O + H₂O → PS₂O₂ + H₂S **ΔG = −1.17 eV** ('hard'). `Fig. S17` 은 (a) 'LPSCl' · (b) 'LPSSeOCl' 이라 제목을 달고 고립 음이온 공 막대 그림을 쓴다 · 전하 표기 PS₄²⁻ · PS₃O²⁻ · PS₂O₂²⁻ (오기로 보인다). SI 캡션은 '**Reaction activation energy**' · 본문은 'reaction energy' · 그림은 'ΔG'.
  - ⚠ 두 반응 모두 크게 **자발** 이다. 비교는 '무도핑 PS₄ 의 첫 가수분해' 대 'O 하나 이미 든 PS₃O 의 둘째 가수분해' — 즉 O 도핑은 **첫 단계를 합성에서 미리 치른 것** 이고, 남은 단계도 −1.17 eV 로 여전히 흘러간다. "열역학적으로 부동태화한다" 는 과장이다 (§10-⑫). 우리 문헌 지도 (`comparison_vs_ours.md` B④ · [Zhu20]) 의 "O 도핑 = 가수분해 구동력을 합성 단계에서 선지불" 과 같은 그림이다.
- **H₂O 흡착 (`Fig. 4i` 실독)**: LPSCl (110) **E_ad = −1.51 eV** · LPSSeCl (110) **−0.77 eV** · 슬랩 그림 (위에 H₂O 하나). 비교 대상이 LPSOSeCl 이 아니라 LPSSeCl 이고 · Se 가 표면 어디에 있는지 · H₂O 가 어느 원자 위인지 그림에서 구분이 어렵다. 저자: "Se 가 4d 에 주로 있으니 Se 의 효과는 '동역학적 원소 효과' (물을 밀어냄)".
  - 우리 규칙 (`D-2026-10-05-adsorption-site-coordination`) 문턱 (≳ 2 eV) 아래라 배위수 점검 대상은 아니지만, 자리 · 덮임 미기재라 '−1.51 vs −0.77' 은 한 자리 한 배치의 값이다.

### 5.7 Li 금속 쪽 (`Fig. 5a–g`, `Fig. S20`–`S23`, `Table S6`) ★

- **CCD (`Fig. 5a–c` 실독)**: 왼쪽 축 전압 ±0.06 V · 오른쪽 축 전류밀도 (LPSCl ±1.5 · 나머지 ±4 mA cm⁻²). LPSCl: 계단이 ≈16 h 에 0.8 mA cm⁻² 에서 전압이 떨어진다 (단락). LPSSeCl: ≈46 h 에 2.3. LPSOSeCl: ≈51 h 에 2.6 · 직전 분극 figure-read ≈ ±0.045 V → ASR ≈ 0.045 / 2.5 ≈ 18 Ω cm² (우리 산수 · 계면 + 벌크 합). 계단당 면적 용량 · 스택 압력 미기재.
- **장기 0.2 mA cm⁻² (`Fig. 5d` 실독 · 확대)**: 범례 LPSCl (밝은 청록) · LPSO_BCl (중간 파랑) · LPSOSeCl (옅은 파랑).
  - **그림이 보여 주는 것**: 중간 파랑 (= LPSO_BCl) 이 ≈420–450 h 에 위로 0.12 V 이상 튀고 ≈490 h 에서 끝난다 · 청록 (= LPSCl) 은 ≈1150 h 까지 이어지며 분극이 ±0.04 → ±0.08 V 로 커진다 · 옅은 파랑 (LPSOSeCl) 은 4000 h 까지 · ≈ ±0.008 V 에서 ≈ ±0.03 V 로 서서히 커진다.
  - **본문이 말하는 것**: "LPSCl ≈5 mV · 500 h 뒤 빠른 단락" · "LPSO_BCl ≈10 mV · 1100 h 넘게".
  - ⇒ **두 곡선의 색 (또는 본문 문장) 이 뒤바뀌어 있다.** 삽입 (0–20 h): 청록 ≈ ±0.012 V · 나머지 ≈ ±0.008 V — 본문의 'LPSCl ≈5 mV · LPSO_BCl ≈10 mV' 와도 순서가 반대. 삽입 (380–400 h): 청록 ≈ ±0.03 V (톱니 모양) · 중간 파랑 ≈ +0.015 / −0.01 V · 옅은 파랑 ≈ ±0.008 V. 어느 쪽이 맞는지 이 PDF 로는 가릴 수 없다 (§10-⑭).
  - LPSOSeCl '초저 분극 4000 h' — 분극이 약 4 배 커졌다 (figure-read). 단락은 없다.
- **0.5 mA cm⁻² (`Fig. 5f,g` 실독)**: LPSCl ≈330 h 까지 · ≈100–200 h 에 ±0.06 V 까지 커짐 · 200–220 h 확대에서 반주기마다 위로 휘는 톱니 (≈ ±0.06 V). LPSOSeCl 1600 h · 1200–1220 h 확대 ≈ ±0.012 V 평탄.
- **비교 (`Fig. 5e` · `Table S6`)**: CCD vs 사이클 시간 산점 — 'This work' (2.6, 4000) 가 오른쪽 위. `Table S6` 13 편: CCD 1.1–2.4 · 시간 350–3000 h · 조건 0.1–1 mA cm⁻² 섞임 (예: Ref. S12 Li-OPA|LPSClBr|OPA-Li 2.4 mA cm⁻² · 400 h · 1 mA cm⁻²). 같은 조건 비교가 아니다.
- **계면 XPS (`Fig. S22` · 안 봄)**: Li 1s 에서 Li₂O · Li₂Se 계면 (본문).
- **`Fig. S20`–`S21` (안 봄)**: CCD A 0.9 · B 1.1 mA cm⁻².

### 5.8 Li 계면 AIMD · 계면 DFT (`Fig. 5h–k`, `Fig. S24`–`S26`) ★

- **스냅숏 (`Fig. 5h,i` 실독)**: 그림의 (h) = 'LPSSeOCl/Li contact interface' (1 · 25 · 50 ps) · (i) = 'LPSCl/Li contact interface' — **캡션 순서 ((h) Li/LPSCl · (j) Li/LPSSeOCl) 와 다르다** · 캡션의 (j) · (k) 는 RDF 다. 왼쪽 Li 금속 (옅은 파랑 공 · ≈4–5 열) · 오른쪽 SE. LPSOSeCl 25 ps 에 'Formation of Li₂Se/Li₂O' 점선 원 · 50 ps 에 'PS₄ Reliable' 원 둘. LPSCl 25 ps 'unbroken PS₄' · 50 ps 'Reduce P' 원 둘. 두 계 모두 50 ps 에 Li 와 SE 가 크게 섞여 있다 (Li 층의 결정 배열이 사라짐).
- **RDF 열지도 (`Fig. 5j,k` 실독)**: (j) Li/LPSOSeCl — P–S 띠 ≈2.05 Å 가 50 ps 내내 선명 (색 막대 0–50) · **Li–P 띠 ≈2.5 Å 가 figure-read ≈14 ps 부터 나타나고 그림에 'Formation of reduced LiₓPᵧ' 화살표가 붙어 있다** (색 막대 0–30). (k) Li/LPSCl — P–S 띠가 ≈30 ps 까지 보이다 약해짐 ('Decomposition of PS₄ tetrahedra') (색 막대 0–90) · Li–P 띠 ≈2.5 Å 가 ≈2 ps 부터 ('Formation of reduced LiₓPᵧ').
  - ⇒ 그림이 말하는 것은 '**LPSOSeCl 에서도 LiₓPᵧ 가 생기는데 더 늦게 (≈14 vs ≈2 ps)**' 다. 본문은 LPSOSeCl 쪽 LiₓPᵧ 를 언급하지 않는다 (§10-⑬). 두 계의 색 막대 범위가 달라 띠 세기를 눈으로 비교할 수 없다.
- **`Fig. S25` 실독** (Li/LPSSeOCl): Li–S ≈2.4 Å (0–25) · Li–O ≈2.0 Å (0–70) · Li–Se ≈2.6 Å (0–40) — **세 띠 모두 t = 0 부터 50 ps 까지 같은 세기로 일정**. 본문 "Li–Se 2.55 · Li–O 2.10 Å 의 안정 봉우리가 나타나고 시간에 따라 안정화 → Li₂Se · Li₂O 형성" — ⚠ SE 안의 Se · O 는 처음부터 Li 에 둘러싸여 있으므로 (4d Se 는 Li 우리 중심 · 16e O 도 Li 와 닿는다) 이 띠는 **SE 자체의 Li–Se · Li–O** 다. 시간에 따라 자라지 않는 띠로는 'Li₂Se/Li₂O 가 새로 생긴다' 를 말할 수 없다.
- **`Fig. S24` (안 봄)**: Li/LPSCl Li–S RDF — 본문 "넓어지고 이동 → PS₄ 분해 · Li₂S · LiₓPᵧ".
- **관측창 (우리 규칙 `D-2026-10-05-md-observation-window` · ν₀ 10¹³ s⁻¹ **가정** · 정상성 가정)**: 300 K · t = 50 ps · 반응 기회 n (계면 PS₄ 수 · 미기재):
  - n = 1: 기대 사건 1 ≈ **0.16 eV** (검출 63 %) · 95 % 검출 ≈ **0.13 eV**.
  - n = 10: ≈0.22 / ≈0.19 eV · n = 100: ≈0.28 / ≈0.25 eV.
  - ⇒ Li/LPSOSeCl 에서 'PS₄ 가 유지된다' 는 이 창 위 장벽의 분해는 아직 못 본 것과 같은 말이다. 실험 셀은 수천 시간이다.
- **계면 DFT (`Fig. S26` 실독)**: (a) Li(001)|Li₂O(100) **2.93** · |Li₂S(100) **2.04** · |Li₂Se(100) **1.32 J m⁻²** — 슬랩 그림 (아래 Li ≈5 층 · 위 Li₂X 얇은 층 · 진공). 본문: "Li|Li₂O 가 가장 높은 계면 에너지 → 더 안정한 SEI · 덴드라이트 억제". ⚠ 그 논리대로면 Li₂Se 는 **가장 낮다** — 논문이 장려하는 Li₂Se 계면이 자기 기준에서 가장 나쁘다 (§10-⑮). (b) Li₂O **1.15** · Li₂S **1.07** · Li₂Se **0.86 eV** · x 축 'Reaction coordinate (Å)' 0–1 · 9 점 · 반형석 구조 삽입. 이 장벽들은 Li₂S 공공 이동으로 흔히 보고되는 값보다 꽤 크다 — 기구 (공공 · 틈새 · 협동) 를 안 적어서 다른 문헌과 놓을 수 없다.

### 5.9 양극 · 풀셀 (`Fig. 6`, `Fig. S27`–`S29`)

- **Li 음극 풀셀 (`Fig. 6a` 실독)**: 0.1 C · 4.45 mg cm⁻² ('mg cm⁻¹' 오기) · LPSOSeCl 첫 figure-read ≈178 → 100 cyc ≈145 (81.33 %) · LPSCl 첫 ≈153 → ≈103 (66.4 %). `Fig. S27` (안 봄): 충방전 곡선.
- **Li-In 율 (`Fig. 6b` 실독)**: 4.58 mg cm⁻² · 각 율 5 사이클 · 본문 값과 그림 일치 · LPSCl 2 C 는 figure-read ≈12 → ≈3 으로 계속 떨어짐.
- **충방전 곡선 (`Fig. 6c,d` 실독)**: y 3.0–4.4 V (vs Li⁺/Li 환산으로 보인다) · (c) LPSCl 1st 방전 끝 ≈157 · 10th ≈140 · 50th ≈112 · 100th ≈93 mAh g⁻¹ · (d) LPSSeOCl 1st ≈200 · 10th ≈186 · 50th ≈178 · 100th ≈168. 충전 1st LPSCl ≈213 · LPSOSeCl ≈227 mAh g⁻¹ → 첫 CE figure-read ≈74 % · ≈88 %. ⚠ 캡션은 (c) LPSOSeCl · (d) LPSCl — 그림 라벨과 반대 (본문은 그림 쪽이 맞다).
- **장기 0.3 C (`Fig. 6e` 실독)**: 5.47 mg cm⁻² · LPSOSeCl figure-read 첫 ≈200 → 100 cyc ≈170 (90.7 %) → 500 cyc ≈138 (70.7 %) · LPSCl ≈155 → ≈95 (64.6 %) 에서 100 cyc 로 끝. 유지율 기준 사이클 (활성화 뒤 몇 번째?) 미기재.
- **사이클 뒤 XPS (`Fig. 6f,g` 실독)**: P 2p — NCM/LPSCl 은 'Phosphorus oxides' (≈134 eV) 가 지배 · argyrodite (≈131.5) 작음 / NCM/LPSOSeCl 은 argyrodite 가 크고 산화물 작음. S 2p — LPSCl 쪽 sulfates (≈169.5) · sulfites (≈167.5) · S (≈164) 봉우리 뚜렷 / LPSOSeCl 쪽은 argyrodite (≈161.5) 가 지배 · 산화 성분 작음. 정량 (면적 %) 은 없다. ⚠ LPSOSeCl 은 처음부터 P–O (PS₃O) 를 갖고 있으니 'P 산화물' 비교는 출발점이 다르다.
- **`Fig. S28` · `S29` (안 봄)**: EIS 50 cyc 전후 · LPSSeCl 풀셀이 두 계 사이 → "Se 는 σ 로 율 · 수명을 올리지만 O(16e) 의 고전압 안정을 대신 못 한다".
- **파우치 (`Fig. 6h` 실독)**: LED 점등 · 접기 · 자르기 사진 세 장. 셀 사양 없음 — 정성 시연.
- **비교 (`Fig. 6i` 실독)**: 왼쪽 사이클 수 막대 11 개 (0.1–0.5 C 섞임) · 오른쪽 비용량 막대 11 개 (0.1–1 C 섞임 · LCO · NCM 섞임). 'This work' 는 Li-In/LPSSeOCl/NCM811 0.3 C 500 cyc · 0.1 C ≈198 mAh g⁻¹.

---

## 6. 메커니즘 · 논증 흐름 (`Fig. 1`) — 논증 사슬 판정

- **`Fig. 1` 실독**: (a) Li₂O-derived route — 원료 원 (LiCl · Li₂S · P₂S₅ · Li₂O) → 볼밀 · 소성 → LPSO_ACl 셀 (4d 우리 중심에 빨강-노랑 반반 구 = O/S 혼합) → 확대 원 (Li 우리 가운데 O) '**4d-favored incorporation tendency**'. (b) P₂O₅-derived route ('This work') → LPSO_BCl (PS₄ 꼭짓점 구에 빨강 조각) → 확대 PS₄ (꼭짓점 넷 모두 빨강 조각) '**16e-related incorporation tendency**'. (c) 'Role of O': √ electrochemical window · √ humid air stability · × Inhibit lithium ion transport / 'Role of Se': √ Li⁺ conductivity · √ interfacial kinetics · √ Uniform Li⁺ flu(x) · 가운데 'Balanced dual-anion electrolyte'. (d) NCM811 | LPSOSeCl | Li 셀 개념도 · 양극 'Stable CEI' · 음극 'Stable Li₂Se/Li₂O-Rich SEI'.

| 단계 | 주장 | 근거 | 판정 |
|---|---|---|---|
| ① | 원료가 O 의 첫 진입 자리를 정한다 (동역학) | `Fig. 2a,b` 장벽 넷 | 🔴 방법 전무 · 매끈한 곡선 · 슬랩 + 덩어리 모형 · **자리 열역학 · 재배치 장벽 없음** · 홉 수: 느린 경로도 2 h 안에 ≈14–500 회 |
| ② | 실험에서 A = 4d · B = 16e 우세 | Rietveld 점유 · Raman 420 세기 · P 2p 분율 · S 2p 이동 | ⚠ 정성 · A 는 불순물상 (x ≥ 0.4) 이 있어 '4d 에 들어감' 과 '덜 들어감' 이 안 갈린다 · P 2p 증가 (+5.9 %p) 가 16e O 0.376/f.u. 에 비해 작다 |
| ③ | O(16e) 가 O(4d) 보다 수송 손해가 작다 | σ (`Fig. S7`) · Ea (세 셀) | ✅ 방향 · ⚠ A 의 불순물 교락 |
| ④ | Se 는 4d 에 압도적으로 앉는다 | Li 1s 53.2 eV · EXAFS CN · WT | ⚠ CN(Se–P) 0.45 · Rietveld 62 % → Se 의 ≈40 % 는 4d 밖 |
| ⑤ | Se 가 σ 를 메운다 (전자 · 위상 보상) | σ 3.21 vs 3.19 · Ea 0.323 vs 0.346 · PDOS · BVSE | ✅ σ · Ea 실험 · 🔴 BVSE 1D → 2D 는 자기 그림이 부정 · 장벽 차 0.011 eV |
| ⑥ | O(16e) 가 산화창을 넓힌다 | LSV onset | ⚠ A (3.02) = B (3.00) → 자리 무관 · onset 정의 · 조건 미기재 |
| ⑦ | 공기 안정 = O(16e) 열역학 부동태 + Se 흡착 약화 | H₂S · Raman · ΔG · E_ad | ✅ H₂S 측정 · ⚠ ΔG 는 둘째 단계도 자발 · E_ad 는 LPSSeCl 면 한 배치 |
| ⑧ | Li₂Se/Li₂O SEI 가 CCD · 수명을 올린다 | CCD · 장기 · XPS (`Fig. S22`) · AIMD · 계면 DFT | ✅ CCD · ⚠ 장기 그림 범례 반대 · 🔴 AIMD RDF 는 SE 자체 결합 · LPSOSeCl 에서도 LiₓPᵧ · 계면 에너지 기준은 Li₂Se 가 최하 |
| ⑨ | 고전압 양극 호환 | 풀셀 · XPS | ✅ 데이터 · ⚠ 적재량 · 비교 조건 섞임 · 셀 1 개 |

**빠진 대조군 (가장 큰 교락)**: ① 'O 는 16e 가 낫다' 를 보이려면 **같은 O 함량 · 같은 상 순도** 의 4d 시료와 비교해야 하는데 A 는 x ≥ 0.4 에서 이미 불순물상이 있다. A 의 σ · H₂S · CCD 손해가 '자리' 때문인지 '덜 들어간 O · 불순물' 때문인지 갈리지 않는다. ② LPSOSeCl 의 Se 를 P₂Se₅ 같은 '16e 쪽 원료' 로 넣은 대조 (Se@16e 우세 시료) 가 없다 — 그래야 'Se 는 4d 라서 좋다' 가 '그냥 Se 라서 좋다' 와 갈린다 (`jiang2022` DFT 는 Se@16e 만으로 σ 가 크게 오른다고 계산했다). ③ LPSSeCl 의 합성 원료 · 조성 · 자리 정련이 없다.

---

## 7. 우리 계산 대비 ★★ (`../our_dft_baseline.md` · `db/properties/`)

> 규율: 문헌 수치는 소환값이다 — 이 논문의 숫자와 우리 절대값을 한 표에 놓지 않는다. 우리 값은 원장 (`canonical_registry.json` · `citation_hazards.json`) 의 허용 범위 안에서만 쓴다. Band gap 은 **상대차** 만 · MLIP-MD Ea/σ 는 **O 효과 서술에 쓰지 않는다** (`HZ-cross-system-Ea` BLOCKED · modelc box331 `difference_with_lpsocl_as_O_effect` 금지 · lpsocl multiseed Ea provisional · `HZ-lpsocl-Ea-diffusive-gate` HOLD).

### 7a. 방법 대조 — 같은가 다른가

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| O 치환 계의 조성 · 자리 | Li₆PS₅₋ₓOₓCl (x 0.1–1.0 · Cl 1.0) · O 원료 Li₂O / P₂O₅ · LPSOSeCl O 0.4 · Se 0.4 | LPSOCl = **Li₅.₄PS₄.₂O₀.₂Cl₁.₆** (Cl-rich · O 0.2) · O 는 **PS₄ 꼭짓점 (POS₃ · 16e) 에 둔 구성** — 자리 근거가 아니라 선택 (`comparison_vs_ours.md` 2026-11-09 행) | 조성 (Cl 1.6 vs 1.0 · O 0.2 vs 0.4) 이 달라 값 대조는 의미가 없다 · 우리 O 자리 = 이 논문의 'B 갈래' 와 같은 쪽 |
| O 자리 선호의 근거 | 원료 → 자리 '혼입 장벽' (방법 미기재) · 열역학 자리 에너지 **없음** | 허용 문장 **"O 는 16e 를 4d 보다 선호 (UMA · Nd@Li 셀)"** — 방향만 · 크기 금지 (`HZ-nd-site-cfg23-mislabeled` BLOCKED 맥락) · `db/properties/site_preference_raw_78.csv` | 우리 것은 **결정 안 자리 교환 에너지** (열역학) · 이 논문은 **원료에서 들어가는 경로** (동역학). 둘이 다른 질문이다. 우리 방향 (16e 선호) 이 맞다면 이 논문 A 갈래의 '4d 우세' 는 **열역학 반대편에 갇힌 상태** 여야 하는데, 그걸 지키는 재배치 장벽을 논문이 안 냈다 |
| 장벽 계산 | 방법 미기재 · 영상 점 없는 곡선 | NEB 는 `tools/sei/collect_neb.py` · 홉 수 검산 한 줄 의무 (`D-2026-09-27-barrier-hop-count`) | §5.1 에 우리 홉 수 검산을 붙였다 |
| BVSE | eV 단위 · 1D/2D/3D 침투 장벽 (softBV 류로 보임 · ref 34) | **softBV 가 아니다** — b = 0.37 고정 Brown 형식 BV 합 · BVSE = (BVS − 1)² (valence² · eV 아님) · 채널 % 지표 (`tools/comp1_v3/`) | **같은 축이 아니다** — 이 논문 0.350–0.361 eV 와 우리 BVSE 값을 한 줄에 놓지 않는다 |
| PDOS · 갭 | 범함수 · k 미기재 · 전도띠가 그림 창에 안 보임 | fixed-occ nscf VBM/CBM 고유값만 (DOS 판독 금지) · LPSOCl **2.2309** vs modelc **2.099 eV** (PBE) → **O 가 갭을 +0.13 eV 넓힌다 (상대 · 같은 방법)** · LPSOCl DOS 에서 O 는 띠 가장자리에 상태를 안 만든다 (`lpsocl_dos_gap.json`) | 이 논문은 갭 값을 안 낸다. 우리 그림 (O 2p 는 깊다 · VBM = S 3p) 은 이 논문 `Fig. 3j` 의 O 2p 봉우리 위치 (≈ −2.6 eV 가 가장 큼) 와 **정성적으로 같은 방향** · Se 4p 가 VBM 을 만든다는 그림 쪽 함의 (갭 ↓) 는 우리 계산에 없다 (Se 계 없음) |
| 결합 분석 | PDOS 겹침 + 전하밀도차로 '혼성 · 정전 덫' | LOBSTER ICOHP — **P–O ≫ P–S** (방향 · 위치 `comparison_vs_ours.md` B④ 행 · `lpsocl_icohp_persite_origin.csv`) | 이 논문의 'O 가 Li 를 붙든다' 는 결합 분석 없이 나왔다 — 우리 자리별 ICOHP (Li 앵커 세기) 가 그 질문의 맞는 도구다 (O 이웃 Li 의 ICOHP 를 따로 뽑을 수 있다 · 이번에 확인 안 함) |
| 산화 (ESW) | LSV 꺾임 onset 2.84 → 3.00–3.16 V (조건 미기재) | grand-potential 층① (분해 onset): 정본 comp1 · modelc **2.256 V** (LiS₄ 제외 · S²⁻ 한정) · CEI 장부 (`cei_esw_Li_x002_2026_09_28.json` · LiS₄ 포함) 에서 **comp1 = modelc = LPSOCl = 2.14 V** | ⇒ 우리 열역학 축에서는 **O 가 산화 onset 을 안 올린다.** 이 논문의 'O 가 창을 넓힌다' 는 **LSV 동역학 축** (분해 전류가 보이기 시작하는 전압) 이다 — 축이 다르다. 두 기준 (2.256 · 2.14) 도 서로 섞지 않는다. 우리 셀 작동창 2.5–4.25 V 는 전체가 열역학적 산화 구간이라, '안정' 은 창 안 분해 산물 · 부동태로 판단한다 (`CLAUDE.md` 양극 규칙) — 이 논문 `Fig. 6f,g` (사이클 뒤 P 산화물 ↓ · 황산염 ↓) 가 그쪽 증거다 |
| 가수분해 | 고립 음이온 ΔG 두 단계 (−2.28 · −1.17 eV) · 방법 미기재 | **계산 0** (가수분해 축은 [Zhu20] 절차 소환만 · `comparison_vs_ours.md` B④) | 우리 기록의 "O 도핑 = 가수분해 구동력 선지불" 정성 해석과 같은 그림 · 수치 대조 없음 |
| 계면 AIMD | VASP · 300 K · 50 ps · 1 궤적 · 셀 미기재 | Li 계면 반응 MD 를 이 계로 돌린 적 없음 · 관측창 규칙 (`D-2026-10-05-md-observation-window`) | §5.8 에 관측창 한 줄을 붙였다 (n = 1: Ea₁ ≈0.16 eV · Ea₉₅ ≈0.13 eV) |
| Li\|Li₂X 계면 · 점착 | 계면 에너지 2.93 / 2.04 / 1.32 J m⁻² (정의 미기재) | 우리 W_ad 기록 (`db/properties/adhesion.json` — **값은 옮기지 않는다**) | 계면 에너지 (γ) 와 점착일 (W) 은 다른 양 · 정의가 없어서 대조 불가 |
| 벌크 셀 이완 | 미기재 | argyrodite 는 고정셀 + EOS (압력 어림 먼저) | 이 논문의 장벽 · BVSE 가 어느 격자 (실험 10.28? 9.86?) 위에서 나왔는지도 모른다 |

### 7b. 개념 대조 — 우리 계와 닿는 곳

- **O 의 자리**: 우리 LPSOCl 은 O@16e (POS₃) 구성이고 · UMA 자리 교환은 '16e 선호' 방향 · `park2026_oxygen_induced_li_intercage_conduction` 의 ND Rietveld 도 16e (단 16e 만 허용한 모형). 이 논문 B 갈래 · LPSOSeCl 의 Rietveld (16e O 0.094–0.098) 도 같은 쪽이다. **새로운 것은 A 갈래 (Li₂O → 4d O 0.228)** — 우리 'O@4d' 배치 (Track 1B · cfg23) 는 Nd 셀에서 계산된 적이 있다 (값은 Nd 자리 근거로 BLOCKED · `HZ-nd-site-cfg23-mislabeled`). CEI 트랙 원고가 O 원료로 무엇을 쓰는지에 따라 이 논문은 "원료가 자리 분포를 바꿀 수 있다" 는 **실험 쪽 주장의 외부 선례** 가 된다 — 단 §10 의 한계 (불순물 교락 · 장벽 방법 없음) 를 같이 붙여야 한다.
- **4d 자리 = 우리 '자유 S²⁻' 자리**: 우리 b2o3 기록의 자리 이야기 (−8..0 eV 창) 에서 **자유 S²⁻ (4d) 가 가장 얕은 3p (가장 산화되기 쉬움)** 다 (`b2o3_dos_gap.json` note). 이 논문이 Se 를 4d 에 넣으면 그 가장 얕은 음이온 자리를 더 얕은 Se 4p 로 바꾸는 셈이다 — 우리 그림으로 읽으면 **4d Se 는 산화 쪽 (VBM) 에 불리** 할 수 있다. 이 논문의 LSV 는 LPSSeCl onset 2.97 > LPSCl 2.84 로 반대 방향인데, LSV onset 정의 문제를 감안하면 열역학 축 결론은 아니다. 우리 grand-potential 로 Se 계를 돌린 적은 없다 (판정 없음).
- **'O 는 수송을 깎는다'**: 방향은 문헌 합의 · 이 논문 (σ 3.19 → 2.2/2.51 · Ea 0.346 → 0.391/0.365) 도 같다. 우리 MLIP-MD 로 LPSOCl vs modelc 의 O 효과를 말하는 것은 **막혀 있다** (위 규율) — 이 논문을 근거로 그 금지를 풀지 않는다.
- **Li 금속 계면 산물**: 이 논문의 Li₂O · Li₂Se · LiₓPᵧ 는 `wang2022_resistive_decomposing_interfaces_se_alkali_metal` 의 '분해 뒤 이원화합물 계면' 그림과 같은 축 · 그 논문은 Li₃P 만 통한다고 했다 — 이 논문의 '이온 전도성 Li₂Se/Li₂O SEI' 서술과 비교할 거리.

### 7c. 🔑 층위를 갈라 쓴 결론 (원고 · 발표용 · 내부)

> **"이 논문은 O 원료 (Li₂O vs P₂O₅) 에 따라 Rietveld 상 O 점유가 4d (0.228/f.u.) 또는 16e (0.376/f.u.) 쪽으로 기우는 실험 관찰과, O(16e)+Se 공도핑 LPSOSeCl 의 σ (3.21 mS cm⁻¹) · H₂S (40 %) · CCD (2.6 mA cm⁻²) 개선을 보인다. 그러나 '원료가 자리를 동역학으로 정한다' 의 계산 근거는 방법이 없고 자리 열역학을 빠뜨렸으며, Se 의 4d 우세는 자기 EXAFS · Rietveld 로 보면 ≈60 % 수준이다. 우리 계산과는 '16e 선호' 방향만 맞대고, 산화 onset 개선은 우리 열역학 축 (O 가 onset 을 안 바꿈) 과 다른 LSV 축 결과로 구분해 쓴다."**

---

## 8. DFT/계산 방법 ★ (템플릿 항목별 · 상세는 §4e)

- **code / version**: AIMD = VASP (판 미기재) · 나머지 계산 전부 **미기재**.
- **functional + vdW**: 미기재 (어느 계산에도).
- **pseudo / basis**: 미기재.
- **k-points / ecut / supercell / nat**: 미기재. `Fig. S1` · `Fig. 2a,b` 장벽은 진공 있는 슬랩 · `Fig. 4i` 흡착은 (110) 슬랩 · `Fig. S26` 은 Li(001)|Li₂X(100) 슬랩 (그림에서만).
- **DFT+U**: 해당 없음 (언급 없음).
- **AIMD**: NVT · 300 K · 2 fs · 50 ps · RDF = vasppy · 계 2 (Li/LPSCl · Li/LPSOSeCl) · 열욕 · 셀 · 시드 미기재.
- **MLIP**: 없음.
- **무질서 처리**: 미기재 — O · Se · (16e/4d) 배치를 몇 개 봤는지 · 어떤 규칙으로 골랐는지 없음. 모든 계산이 배치 1 개로 보인다.
- **NEB**: 'migration energy barrier' 라 부르지만 NEB 라는 말 · 영상 수 · 수렴 기준 없음 (`Fig. 2a,b` 는 점 없는 곡선 · `Fig. S26b` 는 9 점).
- **BVSE**: ref [34] · 프로그램 · 격자 미기재.
- **후처리 · 기록**: RDF 시간 열지도 (vasppy) · PDOS · 전하밀도차 (VESTA 류 그림) · BVSE 1D/2D/3D 침투 장벽.
- **특이사항**: 계산 담당자가 기여 진술에 없다 · 계 이름이 LPSOSeCl / LPSSeOCl / LPSO_BSe_ACl 셋으로 쓰인다 · 'LPSeCl' 오기 (본문 BVSE 문단).

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | (a) Li₂O 경로 → O@4d '4d-favored' (b) P₂O₅ 경로 → O@16e '16e-related' (c) O = 창 · 공기 ✓ / 수송 ✗ · Se = σ · 계면 · 균일 Li⁺ ✓ (d) NCM811 \| LPSOSeCl \| Li 개념도 | 'function-decoupled' 개념도 — 원료 → 자리 → 기능 사슬의 그림판 (데이터 아님) |
| 2a,b | O '혼입 장벽' Li₂O→4d 1.33 · →16e 2.17 · P₂O₅→4d 2.41 · →16e 1.49 eV — 점 없는 매끈한 곡선 · 슬랩 + 원료 덩어리 그림 | 방법 미기재 장벽의 반례 · 홉 수 검산 예 (500 °C 2 h 에서 2.41 eV 도 N ≈ 14) |
| 2c,d | XRD x 0.1–1.0 — A 는 x ≥ 0.4 Li₂S · LiCl · 0.9 비정질 · B 상 순수 | O 원료별 고용 한계 (A ≈ 0.3 · B ≥ 1.0) |
| 2e,f | Raman 420 cm⁻¹ 열지도 — A 평탄 · B 감소 (각 패널 정규화로 보임) | 자리 지문 (정성) |
| 2g,h | P 2p 분율 88.8/11.2 · 89.3/10.7 · 82.9/17.1 % · S 2p +0.2 · +0.4 eV | 16e O 0.376/f.u. 대비 PS₃O 증가 +5.9 %p 가 작다 (§10-⑦) |
| 3a–c | EIS (3a 범례 'X_B' 오기) · Arrhenius x = 0.4 — Ea 0.391 ± 0.002 · 0.365 ± 0.006 eV (세 셀) | 자리별 수송 비교 (교락: A 불순물) |
| 3d–f | BVEL 등치면 — LPSCl · A 'Inhibited' · B 'Activated inter-cage jump' | 등치면 값 없는 그림 비교의 예 |
| 3g–i | σ 3.19 · 4.03 · 3.21 · Ea 0.346 · 0.283 · 0.323 · LSV onset 2.84 · 2.97 · 3.14 V | 3h 의 298 K 점은 ≈3.2 · ≈6.5 · ≈4.1 mS cm⁻¹ (본문과 어긋남) · 3i 막대 3.14 ↔ 본문 3.16 |
| 3j,k | PDOS (O 2p/Li 2s · Se 4p/Li 2s) · 전하밀도차 | Se 4p 가 VBM 을 만든다는 함의 · 'PDOS 겹침 = 혼성' 논리의 약점 (COHP 대조) |
| 3l,m | BVSE — LPSOCl 1D = 2D = 3D 0.361 · LPSSeCl 0.350/0.350/0.351 eV | 본문 '1D → 2D 전이' 를 그림이 부정 · 장벽 차 0.011 eV |
| 4a | LPSOSeCl Rietveld a = 9.8970 Å | 정련 품질 (차 곡선 평탄 · 15–20° 둔덕) |
| 4b–e | Se K-edge XANES (Se²⁻ · Li₂Se 유사) · FT-EXAFS (둘째 껍질 ≈3.4 Å 가 가장 큼 · y 라벨 k²) · WT (가장 센 극대 R ≈ 3.3 Å · k ≈ 4.5 Å⁻¹) | CN(Se–P) 0.45 → 16e Se ≈27–63 % (§5.5 산수) · WT 라벨과 본문 서술 불일치 |
| 4f | H₂S 50 min — 100 · 68.2 (A) · 48.2 (B) · 40.0 % (LPSOSeCl) · 포화 안 됨 | 4d O 도 32 % 줄인다 (본문 미언급) |
| 4g | in situ Raman — LPSOSeCl 28 min 유지 · LPSCl 수 분 내 소멸 · 색 막대 범위 다름 | 정성 |
| 4h | PS₄→PS₃O ΔG −2.28 · PS₃O→PS₂O₂ −1.17 eV | 둘째 단계도 자발 — '부동태' 과장 · [Zhu20] '선지불' 해석과 같은 그림 |
| 4i | H₂O E_ad (110) LPSCl −1.51 · LPSSeCl −0.77 eV | 자리 · 덮임 미기재 흡착값 |
| 5a–c | CCD LPSCl 0.8 · LPSSeCl 2.3 · LPSOSeCl 2.6 mA cm⁻² | CCD 데이터 (스택 압력 미기재) |
| 5d | Li‖Li 0.2 mA cm⁻² — 범례대로면 LPSO_BCl ≈490 h 단락 · LPSCl ≈1150 h · LPSOSeCl 4000 h (분극 ≈ ±8 → ±30 mV) | 본문과 범례가 반대 (§10-⑭) |
| 5e | CCD–사이클 시간 비교 산점 (조건 섞임) | 참고 |
| 5f,g | 0.5 mA cm⁻² — LPSCl ≈330 h · LPSOSeCl 1600 h (≈ ±12 mV) | 참고 |
| 5h,i | AIMD 스냅숏 1/25/50 ps — 그림 (h) = LPSSeOCl · (i) = LPSCl (캡션과 순서 다름) | 결정 계면 AIMD 1 궤적의 예 |
| 5j,k | RDF 열지도 — LPSOSeCl P–S 유지 · **Li–P (LiₓPᵧ) ≈14 ps 부터** · LPSCl P–S ≈30 ps 뒤 약화 · Li–P ≈2 ps 부터 | 관측창 (n = 1: Ea₁ ≈0.16 eV) · 본문이 빠뜨린 LPSOSeCl LiₓPᵧ |
| 6a | NCM811\|SE\|Li 0.1 C 100 cyc 81.33 vs 66.4 % (4.45 mg cm⁻²) | 성능 참고 |
| 6b | Li-In 율 0.1–2 C — 199.2 … 43.1 vs 160.3 … 12.8 mAh g⁻¹ (4.58 mg cm⁻²) | 성능 참고 |
| 6c,d | 충방전 곡선 (캡션 (c)/(d) 뒤바뀜) — 첫 CE ≈74 vs ≈88 % (figure-read) | 참고 |
| 6e | 0.3 C 500 cyc 70.7 % · LPSCl 100 cyc 64.6 % (5.47 mg cm⁻²) | 성능 참고 · 셀 1 개 |
| 6f,g | 사이클 뒤 P 2p · S 2p — LPSCl 쪽 P 산화물 · 황산염 · 아황산염 · S | 창 안 '분해 산물' 판단 근거 (우리 양극 규칙의 실험 쪽 증거 종류) |
| 6h,i | 파우치 LED 시연 · 문헌 비교 막대 (C-rate · 양극 섞임) | 정성 |
| S1 | 장벽 계산 모형 — 진공 슬랩 + Li₂O / P₂O₅ 덩어리 · 대상 자리 | '혼입 장벽' 의 모형이 무엇인지 보여 주는 유일한 그림 |
| S2–S5 | 결정 구조 · 합성 모식 · SEM · Rietveld A/B (안 봄) | — |
| S6 | Raman 420 세기 vs x — A 13,500–16,700 (0.9 점 없음) · B 15,300 → 6,900 · 'relative range' 21.0 / 71.8 % | 내부 표준 없는 Raman 절대 세기 정량의 예 |
| S7 | σ vs x 두 갈래 (§3b 값) · 유지율 선 | 자리별 σ 원자료 |
| S8 | DC 분극 (전자 전도도) A · B (안 봄) | — |
| S9 | 셀 부피 1086.37 · 957.3 · 957.74 · 969.42 (y 축 단위 'Å' 오기) | 무도핑 a = 10.28 Å 의 출처 · 이상값 (§10-⑧) |
| S10 | LSV A 3.02 · B 3.00 V | 자리가 onset 을 안 바꾼다는 자기 증거 |
| S11 | DC 분극 LPSCl · LPSSeCl · LPSOSeCl (안 봄) | — |
| S12 | BVSE LPSCl — 1D = 2D = 3D = 0.354 eV · 깊은 극소 두 개 | '1D → 2D 전이' 반례 |
| S13–S16 | EDS · Li 1s (53.2 eV) · H₂S 장치 · LPSSeCl H₂S 83.1 % (안 봄) | — |
| S17 | 가수분해 반응 그림 (ΔG −2.28 · −1.17 eV · 캡션 '활성화 에너지' · 전하 2− 표기) | 같은 양을 세 이름으로 부른 예 |
| S18–S24 | 노출 XRD · Nyquist · CCD A/B · Li 1s 사이클 뒤 · LPSSeCl 장기 · Li/LPSCl Li–S RDF (안 봄) | — |
| S25 | Li/LPSSeOCl RDF — Li–S ≈2.4 · Li–O ≈2.0 · Li–Se ≈2.6 Å · **t = 0 부터 일정** | 'SEI 형성' 주장의 반례 (SE 자체 결합) |
| S26 | Li\|Li₂O 2.93 · Li₂S 2.04 · Li₂Se 1.32 J m⁻² · 이동 장벽 1.15 · 1.07 · 0.86 eV | 정의 없는 계면 에너지 · 자기 논리로 Li₂Se 최하 |
| S27–S29 | 충방전 곡선 · 풀셀 EIS · LPSSeCl 풀셀 (안 봄) | — |
| Table S1 | Li₆PS₄.₆O₀.₄Cl (A) — 4d O 0.228 · a 9.8556 · χ² 7.08 | 명목 대비 57 % |
| Table S2 | Li₆PS₄.₆O₀.₄Cl (B) — 16e O 0.094 · a 9.8571 · χ² 2.94 | 명목 대비 94 % |
| Table S3 | LPSOSeCl — 4d Se 0.247 · 16e O 0.098 · a 9.8970 · χ² 2.03 | Se 명목 대비 62 % |
| Table S4 | Se K-edge 맞춤 — Se–Li 6.61 / 2.50 Å · Se–P 0.45 / 2.20 Å | 16e Se 비율 추정 근거 |
| Table S5 | Ea 세 셀 — A 0.392 / 0.388 / 0.392 · B 0.360 / 0.371 / 0.365 | 반복 측정이 있는 유일한 값 |
| Table S6 | Li‖Li CCD · 수명 비교 13 편 (조건 0.1–1 mA cm⁻²) | 참고 |

## 10. 비판 — 약한 곳 ★

**계산**

- ① **'원료가 자리를 정한다' 의 장벽**: 방법이 하나도 없다 (코드 · 범함수 · NEB · 영상 · 경로 정의). 그림은 점 없는 매끈한 곡선이라 실제 계산의 영상 에너지인지 알 수 없다. 모형은 진공 슬랩 위 원료 덩어리에서 O 가 몇 Å 아래 자리로 가는 경로 (`Fig. S1`) — 실제 고상 반응 (볼밀 20 h 로 이미 비정질 혼합 · 500 °C 소성) 과 거리가 멀다. 무엇보다 **두 자리의 열역학 에너지 차** 와 **결정 안 4d ↔ 16e 재배치 장벽** 이 없다. 우리 홉 수 검산으로는 '느린' 경로 (2.17 · 2.41 eV) 도 500 °C 2 h 안에 ≈500 · ≈14 회 일어날 수 있어, '동역학적으로 갇혔다' 를 말하려면 재배치 장벽이 필요하다.
- ② **Se '압도적 4d'**: EXAFS CN(Se–P) 0.45 ± 0.18 은 Se 의 27–63 % 가 16e 라는 뜻이고 (16e Se 는 P 하나와 결합), Rietveld 4d Se 0.247/f.u. 는 명목 0.4 의 62 % 다. 두 측정이 같이 'Se 의 ≈40 % 는 4d 밖' 을 가리킨다. WT 의 가장 센 극대는 둘째 껍질 (R ≈ 3.3 Å) 인데 본문은 그것을 Se–Li 첫 배위로 서술한다 · FT y 라벨 (k²) ≠ 캡션 (k³).
- ③ **BVSE**: 무도핑이 이미 1D = 2D = 3D (`Fig. S12` 인쇄값) — 'Se 가 1D 를 2D 로' 는 그림과 반대. 세 계 장벽 차 ≤ 0.011 eV (실험 Ea 차 0.063 eV 의 1/6) · LPSOCl 이 0.361 로 가장 높다는 결과는 본문에서 빠졌다 · '깊은 덫' 은 무도핑에도 있다.
- ④ **PDOS '혼성'**: 원자구 투영에서 Li 2s 가 음이온 p 봉우리를 따라가는 것은 흔한 모양 (이웃 꼬리) — 결합 세기 판정은 COHP 가 필요하다. 'Fermi 준위 근처' 의 O 2p 혼성은 그림에서 O 2p 가장 큰 봉우리가 −2.6 eV 라 맞지 않는다 · 빈 상태가 창에 안 보인다.
- ⑤ **Li 1s 53.2 eV = Li–Se = 4d**: Li 1s 2.3 eV 이동은 이례적으로 크다 · Li–Se 결합은 Se 자리와 상관없이 생긴다 → 자리 근거가 아니다.
- ⑫ **가수분해 ΔG**: 비교 대상이 '첫 치환 vs 둘째 치환' 이고 둘 다 자발 (−2.28 · −1.17 eV) — '열역학 부동태' 는 과장. 이름이 반응 에너지 / ΔG / 활성화 에너지 셋으로 쓰인다 · 고립 음이온 전하 표기 (2−) 오기 · 열 보정 방법 없음.
- ⑬ **계면 AIMD**: 50 ps · 300 K · 1 궤적 · 셀 미기재 · 관측창 (n = 1) Ea₁ ≈0.16 eV. **LPSOSeCl 에서도 LiₓPᵧ 가 생긴다 (그림 주석)** 는 것을 본문이 빠뜨렸다. Li–Se · Li–O RDF 띠는 t = 0 부터 일정한 SE 자체 결합이라 'Li₂Se/Li₂O SEI 형성' 근거가 아니다. 두 계의 색 막대 범위가 달라 띠 세기를 비교할 수 없다.
- ⑮ **계면 에너지 논리**: "Li|Li₂O 계면 에너지가 가장 높다 → 안정 SEI · 덴드라이트 억제" 라 쓰는데 그 기준이면 Li₂Se (1.32 J m⁻²) 가 가장 나쁘다 — 논문이 내세우는 Li₂Se 계면과 모순. 계면 에너지 정의 (γ vs W_ad) 도 없다. Li₂X 이동 장벽 0.86–1.15 eV 는 기구 미기재.

**실험 · 구조**

- ⑥ **Raman 절대 세기**: 내부 표준 · 초점 · 충전 보정 없이 420 cm⁻¹ 세기로 PS₄ 농도를 정량 (A 의 흩어짐 21 % 자체가 측정 잡음 크기) · `Fig. 2e,f` 는 패널마다 정규화로 보인다.
- ⑦ **P 2p 정량**: B 의 16e O 0.376/f.u. 면 P 의 ≈38 % 가 PS₃O 여야 하는데 XPS 증가분은 +5.9 %p · 무도핑부터 11.2 % 가 PS₃O (표면 수분) — 벌크 자리 근거로 약하다. 본문은 PO₄³⁻ 성분을 말하지만 그림 맞춤에 없다.
- ⑧ **무도핑 LPSCl 격자상수 10.28 Å (V 1086.37 Å³)**: 통상 LPSCl ≈ 9.85–9.86 Å (V ≈ 957 Å³) 다. 0.4 O 로 부피가 12 % 준다는 것은 비물리적이고, 오히려 도핑 시료 (957.3 · 957.74) 가 통상 LPSCl 값이다. 본문도 LPSOSeCl (969.42) 을 'close to pristine' 이라 써서 자기 `Fig. S9` 와 모순. 'O 가 격자를 줄인다 · Se 가 늘린다' 의 기준점이 흔들린다 (Se 쪽 957 → 969 비교는 그대로 성립).
- ⑨ **'설계 25 %'**: x = 0.4 를 4d 에 전부 넣으면 40 % (4d 는 f.u. 당 1 개) — 25 % 는 산수가 안 맞는다. 정련 22.8 % 는 명목의 57 % 이지 '설계값에 가깝다' 가 아니다.
- ⑩ **S 2p 해석**: "전기음성 O²⁻ 가 이웃 원자에 'metallic character' 를 유도해 결합에너지 ↑" — 물리적으로 맞지 않는 문장 (전자를 빼앗기면 결합에너지 ↑ 은 맞지만 '금속성' 과는 무관).
- **A 갈래 교락**: x ≥ 0.4 Li₂S · LiCl 불순물 · x = 0.9 비정질 — A 의 σ · Ea · H₂S · CCD 손해가 '4d 자리' 때문인지 '덜 들어간 O · 불순물상' 때문인지 갈리지 않는다. 정련 모형은 16e O 를 A 에서 허용하지 않았다 (A 의 O 가 16e 에 일부 있어도 모형이 못 본다).
- **정련 모형 제약**: Li 좌표 · 점유가 세 표에서 같다 (고정) · 16e O 좌표를 S 좌표와 묶었다 · 4d 와 16e 에 동시에 O 를 허용한 모형 · Se 를 16e 에 허용한 모형을 시험하지 않았다. χ² (A) 7.08 은 다른 둘 (2.94 · 2.03) 보다 크다 — 불순물상을 맞춤에 넣었는지 미기재.

**본문 수치 ↔ 자기 그림**

- ⑪ `Fig. 3h` 298 K 점 LPSSeCl ≈6.5 · LPSOSeCl ≈4.1 mS cm⁻¹ (figure-read) ↔ 본문 4.03 · 3.21 (LPSCl 은 일치) · `Fig. 3i` 막대 3.14 V ↔ 본문 3.16 V.
- ⑭ `Fig. 5d` 범례대로면 LPSO_BCl 이 ≈490 h 단락 · LPSCl 이 ≈1150 h 까지 — 본문 (LPSCl 500 h · LPSO_BCl 1100 h) 과 반대. 0–20 h 삽입의 초기 분극 순서도 본문과 반대 · LPSOSeCl '초저 분극 4000 h' 는 분극 ≈4 배 증가를 덮는다.
- 그림 번호 오기: XRD '`Fig. 2a`' (실제 2c) · Raman '2c/2d' (실제 2e,f) · XPS '2e,f' (실제 2g,h) · WT '`Fig. 3l/3k`' (실제 4e/4d) · `Fig. 3` 캡션 LSV '(l)' (실제 (i)) · `Fig. 3a` 범례 'X_B' (실제 A) · `Fig. 5` 캡션 (h)/(j) 순서 ↔ 그림 (h)/(i) · `Fig. 6` 캡션 (c)/(d) 뒤바뀜 · `Fig. 6a,b,e` 적재 단위 'mg cm⁻¹' · `Fig. S9` 부피 단위 'Å' · `Table S3` 시료명 'PS₄.₆' · 계 이름 LPSOSeCl / LPSSeOCl / LPSeCl 혼용 · XRD 파장 1.50405 Å.

**설계 · 보고**

- LSV 조건 · DC 분극 값 · XAS 빔라인 · Raman 레이저 · 스택 압력 · 계산 방법 (AIMD 외) 미기재.
- 반복: Ea x = 0.4 두 시료만 셀 3 개 · 나머지 (σ · CCD · 사이클 · H₂S) 는 셀 하나로 보인다 · 오차막대 없음.
- 풀셀 적재량이 실험마다 다르고 (4.45 · 4.58 · 5.47 mg cm⁻²) 비교표 (`Fig. 6i` · `Table S6`) 는 C-rate · 양극 · 전류 조건이 섞였다.
- '원료 → 자리' 를 가르는 결정적 대조 (같은 상 순도의 4d O 시료 · Se@16e 우세 시료 · 중성자 회절 · ¹⁷O/⁷⁷Se NMR) 가 없다.

## 11. 적용 인사이트 ★ (우리 연구에 어떻게)

- ① **O 자리 서술의 증거 사다리** (CEI 트랙 원고 · 우리 LPSOCl 서술용): 이 논문 · `park2026` · `kang2026` 을 나란히 놓으면 실험 쪽 자리 증거는 전부 **'그 자리만 허용한 Rietveld 모형' + 분광 정성** 이다. 4d 와 16e 를 **동시에** 허용한 정련 · ND · ¹⁷O NMR 이 나와야 '자리' 를 말할 수 있다. 우리 쪽은 UMA 자리 교환 (방향만 · 허용 문장) 이 이미 있다 — 이 논문을 근거로 크기를 쓰지 않는다.
- ② **'원료 의존 자리' 를 우리 계산으로 닫는 법 (제안 · 보고량 카드 먼저)**: 이 논문이 빠뜨린 두 양 — (i) 같은 셀에서 O@4d vs O@16e **자리 에너지 차** (우리 UMA 교환 · 필요하면 DFT 검증) · (ii) 결정 안 4d ↔ 16e **재배치 장벽** (NEB + 홉 수 검산). (i) 의 방향은 이미 있다. (ii) 가 500 °C · 2 h 홉 수 검산에서 N ≪ 1 이 나오면 '원료가 자리를 고정한다' 가 성립하고, N ≫ 1 이면 최종 분포는 열역학이 정한다. ⚠ 새 계산이므로 사용자 결정 사항이다 — 여기서는 제안만.
- ③ **EXAFS CN → 자리 비율 산수**: 16e 음이온은 P 하나와 결합하므로 CN(X–P) ≈ 16e 비율. Se · O 도핑 문헌을 읽을 때 이 한 줄로 '압도적 4d' 같은 서술을 바로 검산할 수 있다 (오차 ± 0.18 이면 비율 ± 18 %p).
- ④ **BVSE 보고 감사 체크**: 1D/2D/3D 장벽을 인쇄해 놓고 본문에서 '위상 전이' 를 말하는 경우 — 숫자부터 본다. 차가 0.01 eV 수준이면 BVSE 로 순위를 매기지 않는다 (우리 BVSE 도 채널 % 는 D₀ 쪽 지표라 Ea 순위를 못 매긴다는 규율과 같은 정신).
- ⑤ **'O 는 산화창을 넓힌다' 를 읽는 법**: LSV onset (동역학 · 조건 의존) 과 grand-potential onset (열역학 · 우리 LPSOCl = 무도핑) 은 다른 축이다. 우리 원고가 'O → 산화 안정' 을 말해야 하면 **분해 산물 · 부동태 (창 2.5–4.25 V 안)** 축으로 말한다 — 이 논문 `Fig. 6f,g` 의 사이클 뒤 XPS 가 그 종류의 실험 근거다.
- ⑥ **4d Se 와 산화**: 우리 자리 이야기에서 4d 자유 S²⁻ 가 가장 얕은 음이온 상태다. 4d 에 Se 를 넣는 설계는 그 자리를 더 얕게 만들 수 있다 (PDOS `Fig. 3j` 도 Se 4p 가 VBM). 양극 쪽 산화 판단에 Se 도핑 문헌을 가져올 때 이 점을 같이 적는다 (우리 계산 없음 · 판정 아님).
- ⛔ 하지 않는 것: 이 논문의 σ · Ea 를 우리 MLIP-MD 값 옆에 놓거나 우리 LPSOCl vs modelc 차를 'O 효과' 로 쓰는 근거로 삼지 않는다 (원장 금지 그대로).

## 12. 인용 가능 문장 (영문 초안 · 랩 표기 *Adv. Energy Mater.*, e71857 (2026))

- "When Li₆PS₅₋ₓOₓCl was synthesized with Li₂O as the oxygen source, Rietveld refinement placed 0.228 O per formula unit on the 4d site at x = 0.4 and Li₂S/LiCl impurities appeared from x = 0.4, whereas the P₂O₅ route gave a phase-pure product with 0.094 O occupancy on the 16e site."
- "At x = 0.4, the P₂O₅-derived (16e-rich) electrolyte retained a higher room-temperature ionic conductivity than the Li₂O-derived one (2.51 vs 2.2 mS cm⁻¹), with activation energies of 0.365 ± 0.006 and 0.391 ± 0.002 eV from three cells each."
- "Se K-edge EXAFS fitting of Li₆PS₄.₂O₀.₄Se₀.₄Cl gave a Se–P coordination number of 0.45 ± 0.18 in addition to Se–Li (6.61 ± 0.60), which, together with a refined 4d Se occupancy of 0.247 per formula unit, suggests that a substantial fraction of Se resides outside the 4d site."
- "Co-doping with O and Se reduced H₂S release in 30% RH air to 40% of that of Li₆PS₅Cl after 50 min and raised the critical current density from 0.8 to 2.6 mA cm⁻²."
- "The proposed precursor-dependent site selection rests on incorporation barriers reported without computational details, and neither the site energy difference nor the 4d–16e exchange barrier was reported."

## 13. 주의 / 한계 (인용 규율)

- **인용해도 되는 것 (조건을 붙여서)**: σ 경향 (`Fig. S7` 인쇄값) · x = 0.4 Ea (세 셀) · Rietveld 점유 (모형 제약 명시) · EXAFS 맞춤표 · H₂S 백분율 (50 min · 30 % RH · 포화 전) · CCD 0.8 / 2.3 / 2.6 mA cm⁻² · 풀셀 유지율 (적재량 · C-rate 명시 · 셀 1).
- ⛔ **인용 금지**:
  - O '혼입 장벽' 1.33 / 2.17 / 2.41 / 1.49 eV 를 자리 선호의 정량 근거로 (방법 전무 · 열역학 없음).
  - 'Se 가 4d 를 압도적으로 차지한다' (자기 EXAFS · Rietveld 가 ≈60 % 를 가리킨다).
  - BVSE '1D → 2D 위상 전이' · BVSE 장벽 차를 수송 차의 원인으로 (차 0.011 eV · 무도핑도 1D = 2D = 3D).
  - LPSCl 격자상수 10.28 Å / V 1086.37 Å³ (통상값과 어긋남).
  - '4000 h 초저 분극' 을 조건 없이 (분극 ≈4 배 증가) · `Fig. 5d` 의 LPSCl vs LPSO_BCl 수명 순서 (본문 ↔ 범례 반대).
  - AIMD 를 'Li₂Se/Li₂O SEI 형성' 의 근거로 (SE 자체 결합 띠 · 50 ps · LPSOSeCl 에서도 LiₓPᵧ).
  - 가수분해 ΔG 를 'O 가 가수분해를 열역학적으로 막는다' 로 (둘째 단계도 자발).
  - LSV onset (3.00–3.16 V) 을 우리 grand-potential onset 과 같은 표에 (축이 다르다).
- 우리 값과의 관계: band gap 상대차 (LPSOCl − modelc = +0.13 eV) 외 우리 수치는 이 digest 에서 대조값으로 쓰지 않는다 · 우리 W_ad · MLIP-MD 절대값은 싣지 않는다.

## 14. 이어 읽기 — litdb 의 관련 digest

| digest | 이 논문과 닿는 곳 | 같이 읽을 때 |
|---|---|---|
| `park2026_oxygen_induced_li_intercage_conduction` | Li₂SO₄ 로 넣은 O · **ND Rietveld 16e** (16e 만 허용한 모형) · σ −7 % 만 · T2→T5 Li 재배치 | O 원료가 또 다르다 (Li₂SO₄) — 같은 16e 결론 · 자리 증거의 종류 (ND vs lab XRD) 비교 · 둘 다 4d 대안을 정련에서 시험 안 함 |
| `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal` | 우리 그룹 · LPSOC (O 치환) 를 양극 촉매질에 · O@16e (lab XRD · [Park26] 인용) | 'O 는 양극 쪽' 이라는 같은 기능 배분 · CEI/우리 원고 쪽 O 자리 서술 사슬 |
| `zhang2026_odoping_argyrodite_o2_co2_dry_air` | Li₅.₃PS₄.₂O₀.₂Cl₁.₅ — 우리 LPSOCl 과 가장 가까운 조성 · 건조 O₂/CO₂ 안정 | 우리 조성 쪽 O 효과 문헌 · 습도 (이 논문) vs 건조 기체 (그 논문) 축 구분 |
| `yang2025_lao_dualdoping_argyrodite_lacl3` | La + O 공도핑 · 공기 · Li 금속 | 이 논문 서론의 '양이온 + O' 공도핑 계열의 대표 · '음이온 + 음이온' 인 이 논문과 대비 |
| `liu2024_pband_center_sbo_dual_interface` | Sb–O 공도핑 · S p-밴드 중심 (본문 ref 22) | 이 논문 `Fig. 3j` PDOS 논리의 정량판 (p-밴드 중심) — Se 4p 가 VBM 을 올리는 효과를 같은 지표로 읽을 수 있다 |
| `jiang2022_se_doped_lpscl_high_throughput_dft` | Se 를 **16e** 에 둔 고처리 DFT · σ ↑ · 양극 계면은 Se 가 악화 | 이 논문은 Se 를 4d 에 둔다 — 'Se 는 자리와 상관없이 빠르다' 대안의 계산 근거 · 양극 쪽 Se 악화 경고 |
| `taklu2021_cucl_dualdoping_air_stability_argyrodite` | CuCl 공도핑 · 공기 · Li 금속 (본문 ref 25 — Raman 420 근거) | 공도핑 계열 · 같은 Raman 해석 관례 |
| `li2025_cubr2_dualdoping_argyrodite` | 공도핑 계열 | 같은 '기능 나누기' 서사 |
| `nosrati2026_anion_engineering_sulfide_se_review` | '기능을 다른 음이온에 나눈다' 리뷰 | 이 논문이 그 리뷰 주장의 2026 사례 하나 |
| `morgan2021_anion_disorder_superionic_mechanism_li6ps5x` · `deklerk2016_diffusion_site_disorder_argyrodite` | 4a/4d 음이온 무질서가 수송을 정한다 | 이 논문은 4d 를 'Li 우리 중심' 으로만 다루고 4a/4d Cl/S 무질서를 언급하지 않는다 — Se 가 4d 에 들어가며 무질서를 바꾸는 효과가 대안 설명 |
| `zhu2020_air_stable_se_design_principles` · `hyun_han_argyrodite_moisture_degradation_design_principles` | 가수분해 열역학 지도 · PS₄ 비결합 3p 가 H₂O 해리를 받는다 | 이 논문 `Fig. 4h,i` 의 방법 미기재 ΔG · E_ad 를 놓을 기준 틀 |
| `rao2011_argyrodite_se_studies_bvse` | argyrodite BVSE 원전 계열 | BVSE 1D/2D/3D 장벽 해석의 기준 |
| `wang2022_resistive_decomposing_interfaces_se_alkali_metal` | Li 금속 분해 산물 (Li₂S · Li₃P · LiCl · Li₂O) 계면 DFT + MTP MD | 이 논문의 Li₂O/Li₂Se 'SEI' · LiₓPᵧ 서술과 같은 축 · 계면 정의 (W_ad) 가 명시된 비교 대상 |

## 15. 기법 용어 미니사전

- **4d · 16e · 4a · 48h · 24g (Wyckoff 자리)** — argyrodite (F-43m) 의 결정학적 자리 이름. 16e = PS₄ 사면체 꼭짓점 S (셀당 16 · f.u. 당 4) · 4d = Li 우리 중심의 자유 S²⁻ (셀당 4 · f.u. 당 1) · 4a = Cl (무질서 시 S/Cl 섞임) · 48h · 24g = Li.
- **우리 (cage) · inter-cage 이동** — 4d 음이온을 둘러싼 Li 6 개 묶음 안 이동 (intra-cage) 과 묶음 사이 이동 (inter-cage). 후자가 장거리 수송의 병목.
- **Rietveld 정련 · 점유 (occupancy)** — 회절 패턴 전체를 구조 모형으로 맞춰 자리별 원소 비율을 낸다. 모형에 허용하지 않은 배치 (예: 16e 의 Se) 는 볼 수 없다.
- **R_wp · R_p · χ²** — 정련 맞춤 지표 (작을수록 좋다 · χ² ≈ 1 이 이상).
- **EXAFS · CN · σ² · S₀²** — X 선 흡수 미세구조로 흡수 원자 주위 이웃 수 (CN) · 거리 (R) · 무질서 (σ²) 를 맞춘다. S₀² = 진폭 감쇠 인자 (여기선 1.03 고정).
- **WT-EXAFS (웨이블릿 변환)** — R 과 k 를 같이 보여 가벼운 이웃 (Li · 낮은 k) 과 무거운 이웃 (P · Se · 높은 k) 을 가른다.
- **XANES · 백색선** — 흡수단 근처 모양 · 산화 상태와 국소 대칭 지문.
- **BVSE / BVEL** — 결합원자가 합으로 Li 자리 에너지 지형을 만들어 1D · 2D · 3D 로 이어지는 최소 장벽을 낸다 (eV 형은 softBV 류). ⚠ 우리 BVSE 는 (BVS − 1)² 형이라 같은 축이 아니다.
- **PDOS · 전하밀도차** — 원자 · 궤도별로 나눈 상태 밀도 · 도핑 전후 전자 밀도 차 등치면.
- **CCD (critical current density)** — Li‖Li 셀에서 전류를 계단으로 올려 단락 (전압 급락) 이 나는 전류.
- **LSV onset** — 선형 주사 전류가 꺾여 오르는 전압 (정의 · 주사 속도 · 전극 구성에 민감 · 열역학 분해 전압과 다르다).
- **grand-potential (산화) onset** — 우리 열역학 축: Li 화학 퍼텐셜을 바꾸며 상 그림에서 첫 분해가 나는 전압.
- **H₂S 방출 시험** — 밀폐 용기 · 고정 습도에서 시료가 내는 H₂S 농도를 시간에 따라 잰다 (공기 안정 지표).
- **RDF 시간 열지도** — 시간 창마다 g(r) 을 계산해 띠의 생성 · 소멸을 본다. 띠가 처음부터 있으면 '새로 생긴' 상이 아니다.
- **홉 수 검산 · 관측창** — Γ = ν₀ exp(−Ea/kT) 로 장벽이 시간 창에서 몇 번 넘어지는지 · 짧은 MD 가 볼 수 있는 장벽 크기 (Ea₁ = kT ln(ν₀ t n)) 를 차수로 본다 (우리 규칙).
- **NCM811 · Li-In** — LiNi₀.₈Co₀.₁Mn₀.₁O₂ 고Ni 양극 · Li-In 합금 음극 (≈0.6 V vs Li⁺/Li).

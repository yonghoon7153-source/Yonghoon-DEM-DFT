# 끝 보고 — wang2020_lithium_free_insitu_plating_llzo (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/wang2020_lithium_free_insitu_plating_llzo.md` (622 줄 · 표 칸수 자체 검사 0 건) · `litdb/figures/wang2020_lithium_free_insitu_plating_llzo/` (그림 13 + 식 4 = 17 장 · 7.2 MB · figures.json) · 이 보고 파일.
공유 파일 · git 은 안 건드렸다 (예외: 추출 도구가 `litdb/figures/_sources.json` 을 다시 씀 — 허용 범위).
`build_index.py --check`: 이 slug 는 "어느 인덱스에도 없음 **[dem]**" · "**comparison_vs_ours_DEM.md** 미편입" 두 곳에만 뜬다 — 분류가 DEM 트랙이다 (제목의 'manufacturing' 등). INDEX_DEM.md 는 메인이 `build_index.py` (생성) 를 돌리면 자동으로 실린다.
웹앱 확인 (읽기만): `paper_pis` → `['sakamoto']` · track `dem` · 원소 Cu · La · Li · Ni · O · Ta · Zr · methods `adhesion` (METHOD_MAP 에 있음 → 용어집 링크) · 그림 주석 13 키 (f1–f6 · fS1–fS7) 파싱 · `paper_figures` 17 (그림 13 + 식 4).
inbox 자동 매칭: `--inbox --only wang2020_lithium` 이 제목 75 % 로 본문 · SI 둘 다 붙인다. talks 인입 대기열: 이 논문 없음 (역링크 불필요).

## (a) INDEX.md 행

넣을 절 (권고): **`## 🧲 계면 점착 · 인터레이어 트랙`** 표 끝 — CC/SE 실용 점착 (G_c 부류) + in situ Li 핵생성의 원전이라 liao2025 · spencerjolly2023 옆이 맞다. ⚠ 절 머리 조건 'LPSCl 이 한쪽 면' 밖 (LLZO) → 행 안 ⚠ 표지를 유지한다. 대안: `## ⚠ EXTERNAL` 절 (argyrodite 아님). INDEX_DEM.md 는 생성물이라 손대지 않는다.

```
| `papers/wang2020_lithium_free_insitu_plating_llzo.md` **(본문 9 pp + SI 12 pp 통합 · 크롭 13장 (도구 13 중 다시 자름 4 — Fig. 2 · 3 · 5 · 6) + 식 크롭 4 · 그림 13장 전부 실독 (S2 · S3 는 쪽 렌더))** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp·⭐⭐⭐ 무음극(in situ) Li 핵생성 · CC/SE 실용 점착의 원전 · ⚠ LLZO(산화물 가넷) — 물성 4축 수치 진입 금지]** ✅ **Michael J. Wang**/E. Carmona/A. Gupta/P. Albertus/**Jeff Sakamoto\*** (Michigan · Maryland), "**Enabling "lithium-free" manufacturing of pure lithium metal solid-state batteries through in situ plating**" — ***Nat. Commun.* 11, 5201 (2020)**, DOI `10.1038/s41467-020-19004-4` (OA CC BY). LLZTO 2 mm 펠릿에 Cu 10 µm / Ni 35 µm 박을 **900–1100 °C · 3–6 MPa 확산 접합**, Li 박 원에서 **0.05 mA cm⁻² · ≈4 MPa · 25 °C** 로 CC/LLZO 계면에 Li 를 그 자리 도금: **5 mAh cm⁻² (≈25 µm) 무손상** · 핵생성 골 ≈**4–5 mV** (Fig. 1b 벡터 판독) · Li/LLZO **<10 Ω cm²** · **≥0.09 mA cm⁻² 에서 단락** · in situ Li CCD **0.3** (Li 박 ≈1). 성장 = **핵 ≈10 mm⁻² → ≈100 µm 패치 옆성장 (15 % → ≈50 %) → ≈1 mAh cm⁻² 합체 → 수직** (박리면 SEM). 90° peel → **W_adh,CC·LLZO 1–10 J m⁻²** (저자 · 소성 보정 입력 미기재 · "upper bound") · 보정 전 상한 **Cu ≈69 · Ni ≈32 J m⁻²** (✎ 우리 산술). 식: W_open = W_CC·SE − W_Li·CC − W_Li·SE · r0 = −2WV̄/(Fη) · 성장 η = W(dA/dt)/I · 압력 η ≈ V̄p/F (4 MPa → 0.5 mV). NCA/PEO 풀셀 60 °C C/10 50 사이클 (퇴화 = 양극 쪽). ⚠ "CE ≈99 %" = **1.8 V 2 h 정전압 포함** (정전류만 0.929–0.966) · 풀셀 CE ≈100 % 는 Li 저장분 2.7 위 <0.8 순환 · "≈25 % 감소" = 충전 기준 (방전 −37 %) · Fig. 5b "micron range @1 J m⁻²" 문장 ≠ 그림 (54–135 nm) · 1–10 J m⁻² 재현 불가 · **G_c 부류 → DFT W_ad 와 같은 줄 금지** | 점착 트랙 · CC/SE 실용 G_c (확산 접합) · in situ Li 핵생성 · 성장 · 공극 · W_ad 보고서 §7 실험 앵커 |
```

## (b) comparison_vs_ours.md 에 넣을 줄

**없음** — LLZO · 실험 · 원자단위 계산 0 이라 물성 4축 (A 이온전도 · B 산화 · C 기계 · D 전자구조) 에 수치로 걸리는 값이 없고, build_index 도 이 slug 를 **DEM 트랙**으로 분류해 `comparison_vs_ours_DEM.md` 편입을 센다.
대신 **`comparison_vs_ours_DEM.md` §I (계면 점착 · 인터레이어 트랙) 끝에 I-11** 로 넣을 블록 (권고):

```
### I-11. `wang2020_lithium_free_insitu_plating_llzo` — (🏷 Jeff Sakamoto 공저 · ⚠ LLZO 산화물) **CC/SE 확산 접합 계면의 실용 박리 (G_c 부류) + in situ Li 핵생성의 '계면 여는 일' 틀**

> **무엇을 주나.** LLZTO 2 mm 펠릿 · Cu/Ni 박 900–1100 °C 확산 접합 · 0.05 mA cm⁻² · ≈4 MPa · 25 °C 에서 Li 를 CC/LLZO 계면에 5 mAh cm⁻² 까지 도금 (*Nat. Commun.* 11, 5201 (2020)). 90° peel (실측 박리각 Cu 81° · Ni 45°) → 저자 W_adh,CC·LLZO **1–10 J m⁻²** (박리 팔 소성 일 Q 를 모형으로 뺀 값 · σ_Y·E 입력 미기재 · "upper bound"). 소성 보정 전 상한 G = P(1−cos φ) = **Cu ≈69 · Ni ≈32 J m⁻²** (✎ digest §6-2 · Fig. S4 평균선 판독).
>
> **★ 우리 축에 닿는 곳.**
> ① **식 (1) W_open = W_adh,CC·SE − W_adh,Li·CC − W_adh,Li·SE** — 새 계면 두 항을 논문은 0 으로 두었다 → **우리 DFT W (Li|CC · Li|SE) 가 들어갈 자리** (W_ad 보고서 §7 · 값은 보고서에만).
> ② 고전 장벽 산술 (✎ digest §6-3): 처녀 계면 균질 핵생성은 mV 과전압에서 불가 (η 4.6 mV · W ≥ 0.1 J m⁻² → ΔG* ≥ 90 eV) → 핵생성 = **기존 계면 공극 가장자리의 Li 젖음** 문제 (Fig. 3a 계면 공극 ≈47 % · 픽셀 판독).
> ③ DEM · 연속체 입력: 적층압 4 MPa · Li σ_Y <1 MPa (인용) · **1 mV ≈ 7.4 MPa** (V̄_Li/F) · 핵 ≈10 mm⁻² · ≈100 µm · 피복 15 % → ≈50 % → 합체 ≈1 mAh cm⁻² · 탈리 공극 5–10 µm · 정전류 CE 0.955 → 0.932 (탈리 0.05 → 0.3 mA cm⁻²).
> ④ 검증 표적 (보정 아님): 옆성장 동안 도금 전위 크기 ≈6 mV 감소 (Fig. 4g 벡터 판독) vs 고립 원판 수축 저항 추정 1–4 mV (✎ digest §6-5).
>
> **⛔ 인용 금지 / 한정어**
> · 1–10 J m⁻² 는 **G_c 부류 · 재현 불가** (SI 식 S2 그대로면 Cu ≈30–60 · Ni ≈9–24 J m⁻² — 박 물성은 우리 가정) · DFT W_ad 와 같은 줄 금지 · liao2025 (탄소/LPSCl Γ 9–41) 와 같은 자릿수라는 것까지만.
> · **LLZO 계** — 900–1100 °C 확산 접합은 황화물에 불가능 (황화물 CC/SE 는 상온~온간 압착) · LLZO 는 Li 와 안정, LPSCl 은 반응.
> · CE ≈99 % 는 1.8 V 정전압 포함 · 풀셀 CE ≈100 % 는 Li 저장분 위 · frame[4]: 대조 표적이지 보정 표적이 아니다.
> 상세: digest §6-2 · §6-3 · §6-5 · §7a · §11.
```

## (c) pdf_map.tsv

**필요 없음** — 자동 매칭이 제목 75 % 로 본문 · SI 를 붙인다 (`wang2020_br_rich_argyrodite…` 와 안 섞인다). 안전줄을 원하면:
```
wang2020_lithium_free_insitu_plating_llzo	wang2020_insitu_plating
```

## (d) 추가로 먹일 만한 논문 (8 편 · 최근 먼저)

같은 배치 18 편 (sandoval2025 · metzler2025/2026 · cicvaric2026 · kim2026 · shi2026 · lu2026 · fuchs2023 · lee2022 · kazyak2020 · wang2019 · sharafi2017 · masias2019 · seymour2021 · yang2021 ×2 · chatterjee) 은 뺐다. 크로스레프 조회는 프록시가 막아서 **서지는 기억 기준이다 — 넣기 전에 DOI 확인** (확신도 표시). 2025–2026 편은 이 배치가 이미 덮고, 서지를 확신하는 추가 2025–2026 편이 없어 지어내지 않았다.

| # | 서지 (기억) | 왜 (축) | litdb | 확신 |
|---|---|---|---|---|
| 1 | T. Fuchs et al., "Imaging the microstructure of lithium and sodium metal in anode-free solid-state batteries using electron backscatter diffraction", *Nat. Mater.* (2024) | in situ 도금 Li/Na 의 결정립 · 미세구조 (무음극) → 연속체 · DEM 의 Li 물성 (크기 · 결정립 의존) 입력 | 없음 (fuchs2023 는 다른 편) | 제목·저널·연도 중상 · 권·쪽·저자 확인 |
| 2 | S. E. Sandoval et al., "Structural and electrochemical evolution of alloy interfacial layers in anode-free solid-state batteries", *Joule* 7 (2023) | 합금 박막층 (Ag 등) 이 무음극 첫 도금에서 어떻게 바뀌나 (황화물 계로 기억) → Ag–C · 친Li 층 · 핵생성 | 없음 (sandoval2025 와 다른 편) | 중 · 권·쪽 확인 |
| 3 | E. Kazyak et al. (Dasgupta · **Jeff Sakamoto**), "Understanding the electro-chemo-mechanics of Li plating in anode-free solid-state batteries with operando 3D microscopy", *Matter* 5 (2022) | 이 논문 Fig. 4 (박리면 시점별) 를 operando 3D 로 — 핵생성 · 옆성장 · CC 변형 · 공극 | 없음 (kazyak2020 는 다른 편) | 중 · 🏷 가능 |
| 4 | J. A. Lewis et al., "Linking void and interphase evolution to electrochemistry in solid-state batteries using operando X-ray tomography", *Nat. Mater.* 20, 503 (2021) | **황화물** (Li₁₀SnP₂S₁₂) / Li 계면의 공극 · 계면상 operando XCT — 공극 축의 황화물 짝 | 없음 | 상 |
| 5 | Y.-G. Lee et al., "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes", *Nat. Energy* 5, 299 (2020) | 이 논문 ref 23 · **Ag–C 층 원전** (LPSCl) — '핵생성 에너지를 낮춘다' 가설의 출처 | digest 없음 · `_curation/wishlist.md` 에 [n] 두 번 | 상 |
| 6 | T. Krauskopf et al., "Lithium-metal growth kinetics on LLZO garnet-type solid electrolytes", *Joule* 3, 2030 (2019) | 이 논문 ref 19 · 얇은 CC/LLZO 의 핵생성 과전압 (이 논문보다 ≈10× 크다고 인용) — CC 두께 · 전류 의존 | 없음 | 상 (권·쪽 중) |
| 7 | J. Kasemchainan et al., "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells", *Nat. Mater.* 18, 1105 (2019) | 탈리 전류 → 공극 → 다음 도금 덴드라이트 (Li/LPSCl) — 이 논문 Fig. 2b '탈리 전류 ↑ → CE ↓' 의 황화물 짝 | 없음 | 상 |
| 8 | V. Pande & V. Viswanathan, "Computational screening of current collectors for enabling anode-free lithium metal batteries", *ACS Energy Lett.* 4, 2952 (2019) | **DFT 로 CC 표면의 Li 흡착 · 핵생성 지표** — W_ad 보고서 §7 Li 친화성 정량화의 계산 선례 | 없음 | 상 (쪽 중) |

## (e) DEM-DFT 보고서 (W_ad 보고서 7 절 · 연속체 · DEM 입력) 에 쓸 거리

전부 **LLZO · 2 mm 펠릿 · 25 °C · ≈4 MPa · 0.05 mA cm⁻²** 한정 (황화물로 숫자 이식 금지) · 이 논문에는 **표가 없다** (그림 · 식 · 본문만).

- **7 절 Li 친화성** — 식 (1) (본문 p.4 · 크롭 `eq_01` · **직접 봄**): W_open = W_adh,CC·SE − W_adh,Li·CC − W_adh,Li·SE · 새 계면 두 항을 논문은 0 으로 가정 (p.6 · *"< 1 J m⁻²"* · ref 24 = 같은 배치 `sharafi2017`). → 우리 Li 슬랩/재료 W 와 2γ_Li 가 들어갈 자리 (보고서 §7 의 2 번 방법).
- **7 절 핵생성** — η_nuc ≈ 4–5 mV (`Fig. 1b` · **직접 봄 · 벡터 판독**: 골 −25.9 mV @ 4.6 µAh cm⁻² · 정상 −21.3 mV) · 상자 2.4–4.5 mV (`Fig. 5b` · 봄) · 식 (2)–(3) (p.6 · `eq_02_03` · 봄). ✎ 우리 산술: r0 = 59 nm (1 J m⁻²) – 4 µm (69) @ 4.6 mV · **ΔG* ≈ 9 × 10⁴ eV (W = 1)** → 처녀 계면 균질 핵생성 불가 → 핵생성은 **기존 계면 공극 가장자리의 Li 젖음** 문제 (`Fig. 3a` 계면 공극 ≈47 % · 길이 7–9 µm · 열림 ≈1 µm · **직접 봄 · 픽셀 판독 · 단면 하나**). 핵 ≈10 mm⁻² · ≈100 µm (p.6 · `Fig. 4b` · 봄).
- **7 절 점착과 공극** — CC/LLZO 박리 = **G_c 부류** 1–10 J m⁻² (SI p.9–10 · `Fig. S4` · `eq_S1_S2` · **직접 봄**) · ✎ 보정 전 상한 Cu ≈69 · Ni ≈32 · SI 식 S2 그대로면 Cu ≈30–60 · Ni ≈9–24 J m⁻² (박 물성은 우리 가정) → 보고서 W 표와 **다른 줄**. 탈리 공극 5–10 µm (p.4 · `Fig. 3c` · 봄) · 정전류 CE 0.929–0.966 · 탈리 전류 0.05 → 0.3 에서 0.955 → 0.932 · 정전압 포함 0.975–1.001 (`Fig. 2b` · **봄 · 벡터 판독**) → CE 손실 = 접촉 손실 (`Fig. 2c` 고주파 호 ≈250 → ≈430 Ω cm² · 재도금 회복 · 봄).
- **연속체 · DEM 입력** — 적층압 ≈4 MPa (p.5 · p.8) · Li σ_Y <1 MPa (p.4 · ref 28 = 같은 배치 `masias2019`) · 압력 과전압 η = V̄p/F (p.6 · `eq_04` · 봄) ⇔ ✎ **1 mV ≈ 7.4 MPa** · 피복률 시계열 15 % (30 µAh) → ≈50 % (620 µAh · 높이 ≈6 µm) → 합체 ≈1000 µAh cm⁻² → 수직 (p.4 · `Fig. 4a–f` · 봄) · 전위 구간 경계 0.03 · 1.03 mAh cm⁻² (`Fig. 4g` · 봄) · 성장 기구 셋 수직+간극 / 소성 옆흐름 / 가장자리 도금 (`Fig. 5c–e` · 봄) · Li/LLZO 계면 저항 <10 Ω cm² (p.3 · `Fig. 1c` · 봄) · 형성 단락 문턱 0.09 · in situ Li CCD 0.3 mA cm⁻² (p.4 · `Fig. S5` · 봄).
- **검증 표적 (보정 아님)** — 옆성장 동안 도금 전위 크기 ≈21 → ≈15 mV (`Fig. 4g` · **봄 · 벡터 판독**) vs ✎ 고립 원판 수축 저항 1–4 mV (ρ_LLZO ≈1750 Ω cm · a 50 µm · n 10–19 mm⁻²) — 접촉 면적 → 계면 저항 모형의 자릿수 점검. 식 (4) 역산 ✎: 초기 1 h 초과 과전압 → W ~10¹ J m⁻² (`Fig. 1b` + Fig. 4 피복률 · 셀이 다르다는 단서).
- **LLZO 한정 단서** — 900–1100 °C 확산 접합 (황화물 불가) · LLZO 는 Li 와 안정 (LPSCl 은 반응 → SEI) · 2 mm 펠릿 · 25 °C · 셀 하나 · 오차막대 없음.

## (f) 그림 크롭 요약

- 도구 13 장 (본문 Fig. 1–6 · SI Fig. S1–S7) · **본문 4 장을 손으로 다시 잘랐다** (figures.json `recrop` 사유): Fig. 2 (도구가 맨 아래 띠 244 px 만 자름) · Fig. 3 (위 패널 글자 a–c · 'Plated Li' 잘림) · Fig. 5 (패널 a · b 글자 + r0 축 10⁻³ 잘림) · Fig. 6 (패널 a 위쪽 절반 · 범례 잘림).
- **식 크롭 4 장** 손으로 추가 (`manual_crop`): Eq. 1 · Eq. 2–3 · Eq. 4 + 압력 항 · Supplementary Eq. 1–2 (`eq_*.png`).
- 도구의 '놓친 번호' fS8–fS36 = **오탐** (본문 p.7 'Supplementary Fig. S6' 뒤 위첨자 참고문헌 31–36 이 'S631–36' 으로 읽힘) — figures.json `missing_labels_note` 에 적었다. 실제 빠진 그림 없음 · 본문 · SI 모두 표 없음.
- 점검: 17 장 테두리 잉크 0 (잘림 없음) · `--audit` 이 이 slug 에 경고 없음 · 손작업 표지가 있어 `--clean` 재실행은 가드에 막힌다 (보존).
- 실제로 본 것: 본문 Fig. 1–6 전부 · SI Fig. S1 · S4 · S5 · S6 · S7 (크롭) · 식 크롭 4 · **Fig. S2 · S3 은 SI 쪽 렌더로만** (크롭 파일은 안 열었다). 벡터 경로 판독: Fig. 1b · 2a · 2b · 4g · 6b.
- 본문 서술과 어긋난 그림 7 곳 (digest §10): Fig. 1b 범위 (5 mAh 서술 vs 0–0.05 축) · Fig. 2b '> 99 %' (사이클 3–5 는 97.5–98.3 %) · Fig. 3a 'minimal gaps' (공극 ≈47 %) · Fig. 3b 33 µm (패널은 ≈21–27 µm) · Fig. 5b 'micron range @ 1 J m⁻²' (그림은 54–135 nm) · Fig. 6b '≈25 %' (방전 −37 % · 충전 −24 %) · Fig. S7b 용량 축 (0.27 vs 0.85).
- 글자 출처 대조 (공용 임시 파일 건): 공용 이름 임시 파일을 쓴 적 없다 — 글자는 inbox PDF 를 Read · pymupdf 로 직접 읽었고, PDF 정체를 다시 대조했다 (sha256 앞자리 본문 05348aeb · SI 1950c9f8 = batch.json 과 같음 · p.1 제목·저자·DOI · p.4 '0.09' · SI p.9 '45° · 81°'). 내 임시 파일은 scratchpad 의 `wang2020_lithium_free_insitu_plating_llzo/` 로 옮겼다.

## (g) Jeff Sakamoto 저자 여부

**예 — 교신저자** (✉ jeffsaka@umich.edu · 소속 1, 2, 4 = Michigan MSE · Maryland CBE · Michigan ME). digest 저자 줄에 `**Jeff Sakamoto**` → 웹앱 PI 배지 `sakamoto` 확인 · (a) 행 둘째 칸 맨 앞에 `🏷 **Jeff Sakamoto 공저** · `.

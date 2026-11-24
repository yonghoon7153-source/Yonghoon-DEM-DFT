# 끝 보고 — metzler2025_ag_particle_distribution_carbon_interlayer_anode_free (2026-11-24 · 병렬 논문 에이전트)

- digest: `litdb/papers/metzler2025_ag_particle_distribution_carbon_interlayer_anode_free.md` (560 행 · §0–§14)
- 그림: `litdb/figures/metzler2025_ag_particle_distribution_carbon_interlayer_anode_free/` (19 장 + figures.json)
- 쓴 파일은 위 둘 + 이 보고 파일뿐. git · 공유 파일 손대지 않음. `build_index.py --check` 만 돌림 (이 slug 는 "어느 인덱스에도 없는 것" · DFT 쪽 비교문서 미편입 목록에 뜬다 — 아래 (a) · (b) 를 합치면 풀린다).

## (a) `litdb/INDEX.md` 에 넣을 행

넣을 절 = **`## 🧲 계면 점착 · 인터레이어 트랙 — LPSCl 이 한쪽 면인 계면/벌크 역학의 실측 앵커 (2026-09-23 신설)`** — `spencerjolly2023_ag_graphite_interlayer_operando_xrd` 행 바로 아래.

```
| `papers/metzler2025_ag_particle_distribution_carbon_interlayer_anode_free.md` **(본문 8 pp + SI 19 pp 통합 · 크롭 19장 중 16장 실독 + Fig. 1 쪽 렌더)** | **[외부·exp·⭐⭐⭐ Ag–C 인터레이어 "Ag 두께 방향 분포 → Li 석출 위치" · 탄소 = Asahi F-200GS 카본블랙 (BET·Raman·O/N 미기재)]** ✅ **Michael Metzler**/C. Doerrer/Y. Sun/G. Matthews/E. Liotti/**Patrick S. Grant\*** (Oxford · Faraday Institution), "**Effect of Silver Particle Distribution in a Carbon Nanocomposite Interlayer on Lithium Plating in Anode-Free All-Solid-State Batteries**" — ***ACS Appl. Mater. Interfaces* 17, 39089–39096 (2025)**, DOI `10.1021/acsami.5c06550` (OA CC-BY). 분무 인쇄 Ag(~60 nm)/CB(NTA ~80 nm)/PVDF = **22.5/67.5/10 wt%**, 20 µm → 500 MPa 압착 ~13 µm · 구조화 = Ag **87.5 %** 를 CC 쪽 절반에 (~5 µm Ag-rich 부층). NMC83 ‖ Li₆PS₅Cl ‖ Ag/CB‖SS (60 °C · 4 MPa · 1 mA cm⁻²): 첫 방전 **172 → 198 mAh g⁻¹** · ICE **72 → 83 %** · 100 cy 방전 유지 **37 → 47 %**. 핵생성 과전압 SS 대비 ~13 mV 덜 음 · **Ag 위치는 핵생성 과전압을 안 바꾼다**. P-FIB SEM/EDS + ⁷Li⁺ SIMS (Li:LPS 36:100 vs 기준 38:100): **구조화 = CC 위 ~20 µm Li · 인터레이어가 SE 쪽으로 밀림 / 비구조화 = 층은 CC 쪽 · Li 는 층 ↔ SE 사이**. ⚠ 판독 셀 = **열간 500 MPa · 200 °C · 3전극 · 2.5 mA cm⁻² → 5 mAh cm⁻²** (성능 셀과 다름) · 장기 n = 1 · `Fig. S6` 3셀 퍼짐 > 평균차 · 점착 미측정 (Liao 2025 와 교란) · 구조화 배합 "C:Ag 1:13 · 1:1" 질량 수지 불일치 | 점착 트랙 (Li 석출 위치 · 인터레이어\|CC · 계면 셋) · W_ad 보고서 7 절 탄소 표면 모형 (터보스트래틱 CB) · DEM Ag/C 층 구조 |
```

- Jeff Sakamoto 배지: **해당 없음** (저자 아님).
- 🎤 talk 역링크: `litdb/talks/*.md` 인입 대기열 · INDEX · INDEX_DEM · pdf_map · topics · comparison 에서 `metzler` · `silver particle distribution` · `acsami.5c06550` · `agdist` 전부 0 건 → 역링크 없음.

## (b) `comparison_vs_ours.md` 에 넣을 줄

- **물성 4축 (A–D) 표: 없음** — 계산 0 · 우리 4축과 같은 양이 없다 (`~5 mS/cm` 는 60 °C 풀셀 EIS 묶음값이라 A 축 비교 금지).
- 방법 · 구조 원전 줄 (같은 표 · `[SJ23AgC]` 행 바로 아래 — 그 행과 같은 꼴):

```
| **[Met25AgD]** ⭐⭐ **Ag–C 인터레이어 *Ag 두께 방향 분포* → Li 석출 위치 (P-FIB SEM/EDS + ⁷Li⁺ SIMS)** · ⛔ **점착·물성값 없음 → A–D 물성 4축 수치 진입 금지** · ⚠ 판독 셀 = 열간 500 MPa · 200 °C · 2.5 mA cm⁻² (성능 셀과 다름) · 탄소 = Asahi F-200GS 카본블랙 (BET·Raman 미기재) | **Michael Metzler**/C. Doerrer/Y. Sun/G. Matthews/E. Liotti/**Patrick S. Grant\*** (Oxford + Faraday Institution) 2025 ***ACS Appl. Mater. Interfaces* 17, 39089** (DOI 10.1021/acsami.5c06550, OA CC-BY) — "Effect of Silver Particle Distribution in a Carbon Nanocomposite Interlayer on Lithium Plating in Anode-Free All-Solid-State Batteries" | ✅ `papers/metzler2025_ag_particle_distribution_carbon_interlayer_anode_free.md` — 판정은 digest **§7** (+ 넣으면 `comparison_vs_ours_DEM.md` **§I-11**) | 실험 (분무 인쇄 · 3전극 · P-FIB SEM/EDS/SIMS · XPS · EIS · 계산 0) |
```

- (선택) `comparison_vs_ours_DEM.md` §I 에 I-11 블록 초안 (I-4 꼴):

```
### I-11. `metzler2025_ag_particle_distribution_carbon_interlayer_anode_free` — ★★ Ag–C 인터레이어에서 **Ag 를 어디 두느냐가 Li 를 어디 쌓느냐를 바꾼다** — 계면 셋 (CC\|층 · 층 안 · 층\|SE) 중 어느 것이 벌어지나

> **무엇을 주나.** 분무 인쇄 Ag(~60 nm)/CB(Asahi F-200GS)/PVDF 22.5/67.5/10 wt% · 20 → ~13 µm (500 MPa) · 구조화 = Ag 87.5 % 를 CC 쪽 절반에. 열간(500 MPa · 200 °C) 3전극 · 2.5 mA cm⁻² → 5 mAh cm⁻² · 60 °C · 4 MPa 단면: 구조화 = **CC 위 ~20 µm Li + 층이 SE 쪽으로 밀림** · 비구조화 = **층은 CC 쪽 · Li 는 층↔SE**. 핵생성 과전압은 둘이 같다 (SS 대비 ~13 mV 덜 음).
>
> **★ DEM 쪽에 닿는 곳.**
> ① **계면 셋을 다 등록한다** — 그림 판독으로는 구조화에서도 Ag/CB 조각이 CC 에 남았다 (층 안 갈라짐 · 논문 언급 없음). I-1 (Liao) 의 "탄소\|SE Γ ≳ ≈10 J m⁻² 면 CC 쪽" 과 **같은 방향을 예측**해서 이 논문 자료로는 Ag 위치 효과와 점착 효과를 못 가른다 (점착 미측정).
> ② **층 압축** — 밀린 층이 압착 13 µm 의 1/4–1/2 (`figure-read ≈` 3–6 µm) 로 얇다 · 저자 *"spongy · compliant CB-rich region"* (측정 없음) → DEM 이 시험할 가설.
> ③ **다공도 미기재** — 원료 277.9 mg / 100 cm² 만 있고 부착 질량이 없다 → 훑는 변수.
>
> **⛔ 인용 금지 / 한정어**
> · **점착 · 응력 · G_c 수치 없음** — 대조 표적 아님 (대조 표적은 I-1 · I-3).
> · 석출 위치는 **열간 판독 셀 조건**과 함께 · 냉간 풀셀 (1 mA cm⁻²) 의 위치는 직접 본 적 없음.
> · 그림 판독 두께는 기울기 보정 미기재 · 스케일바 불일치로 ±30 % 이상.
> 상세: digest §3h · §4 · §6.6–6.9 · §7-3 · §7-4 · §10.
```

## (c) `pdf_map.tsv` 에 필요한 줄

필요하다 — 업로드 파일명이 `agdist2025_…` 라 slug 토큰과 안 겹친다 (`extract_figures.py --inbox --only metzler2025 --dry` = 매칭 0 편 · 두 PDF 가 "짝 못 찾음" 에 뜸). 이번 크롭은 `--pdf` 로 직접 줬다.

```
# ── Ag/CB 인터레이어 Ag 두께 방향 분포 (Metzler 외 2025 · ACS Appl. Mater. Interfaces 17, 39089) — litdb 2026-11-24 · 업로드 파일명이 'agdist2025_…' 라 slug 토큰과 안 겹친다 (--inbox --only metzler2025 --dry = 0편) · 본문 · SI 공통 조각 ──
metzler2025_ag_particle_distribution_carbon_interlayer_anode_free	agdist2025_ag_c_interlayer
```

## (d) 추가로 먹일 만한 논문 (최근 먼저 · 전부 이 논문 참고문헌에서 — 서지는 PDF 의 참고문헌 목록 그대로)

| # | 제목 · 저널 · 연도 | 왜 | litdb |
|---|---|---|---|
| 1 | Xie, Diallo, Kim, Tu, Ceder, "The Microscopic Mechanism of Lithiation and Delithiation in the Ag/C Buffer Layer for Anode-Free Solid-State Batteries", *Adv. Energy Mater.* 14, 2302960 (2024) — ref 30 | Ag/C 층 기전 · Li–Ag 합금 순서 (합금 구동력) | 없음 |
| 2 | Wang, Xia, Ji, Liu, Zhang, He, Zhang, Wan, Wang, "Lithium Anode Interlayer Design for All-Solid-State Lithium-Metal Batteries", *Nat. Energy* 9, 251–262 (2024) — ref 16 | 인터레이어 설계 원리 (Li 친화 · 수송 · 위치) | 자체 digest 없음 (`kang2026_stress_regulated_…` 가 제목만 인용) |
| 3 | Song, Li, Zhu, Li, Liu, Peng, Fan, Yao, "Deeply Lithiated Carbonaceous Materials for Great Lithium Metal Protection in All-Solid-State Batteries", *Adv. Mater.* 36, 2400165 (2024) — ref 22 | 탄소 종류 · 리튬화 탄소 (W_ad 7-1 의 'LiC₆ 쪽이 운전 조건' 근거) | 없음 |
| 4 | Doerrer, Metzler, Matthews, Bu, Spencer-Jolly, Bruce, Pasta, Grant, "Spraying Li6PS5Cl and Silver-Carbon Multilayers to Facilitate Large-scale Fabrication of All-Solid-State Batteries", *Device* 2, 100468 (2024) — ref 13 | 같은 그룹 분무 Ag–C 층 공정 (면밀도 · 두께 — 이 논문에 없는 DEM 입력 보충 기대) | 없음 |
| 5 | Jun, Park, Jung, Lee, Kim, Kim, Bae, Son, Lee, "Ultra-Stable Breathing Anode for Li-Free All-Solid-State Battery Based on Li Concentration Gradient in Magnesium Particles", *Adv. Funct. Mater.* 34, 2310259 (2024) — ref 15 | 두께 방향 '구배' 설계의 Li–Mg 판 (합금 구동력 비교) | 없음 |
| 6 | Haslam, Sakamoto, "Stable Lithium Plating in 'Lithium Metal-Free' Solid-State Batteries Enabled by Seeded Nucleation", *J. Electrochem. Soc.* 170, 040524 (2023) — ref 37 · 🏷 **Jeff Sakamoto 공저** | 씨앗 핵생성 · Li \| 집전체 (Li 친화 · 핵생성 과전압) | 없음 |
| 7 | Risal, Wu, Wang, Robles Hernandez, Zhu, Yao, "Silver-Carbon Interlayers in Anode-Free Solid-State Lithium Metal Batteries: Current Development, Interfacial Issues, and Instability Challenges", *Carbon* 213, 118225 (2023) — ref 50 | Ag–C 층 리뷰 — 탄소 종류 · Ag 함량 비교 정리 기대 | 없음 |
| 8 | Futscher, Amelal, Sastre, Müller, Patidar, Aribia, Thorwarth, Siol, Romanyuk, "Influence of Amorphous Carbon Interlayers on Nucleation and Early Growth of Lithium Metal at the Current Collector-Solid Electrolyte Interface", *J. Mater. Chem. A* 10, 15535–15542 (2022) — ref 34 | 비정질 탄소 층 × Li 핵생성 (탄소 종류 → Li 친화) | 없음 |

- 번외 (오래됐지만 원조): Lee 외, *Nat. Energy* 5, 299–308 (2020) — ref 19 · 자체 digest 없음 (여러 digest 가 인용만).
- 추천에서 뺀 것 (같은 묶음에서 이미 digest 됨): `metzler2026_sputtered_ag_carbon_interlayers_anode_free` (같은 1저자 후속 · digest 이웃 카드에 링크함) · `lu2026_li_ag_interface_thermodynamics_kinetics` · `sandoval2025_electro_chemo_mechanics_anode_free_ssb` · `cicvaric2026_li_nucleation_ni111_cu111_anode_free`.

## (e) DEM-DFT 보고서에 쓸 거리 (쪽 · 그림 · 직접 봤는지)

**W_ad 보고서 7 절 (Li 친화성 · Ag 와 탄소 종류별 표면 모형 · 합금 구동력)**

| # | 쓸 거리 | 근거 위치 | 직접 봤나 |
|---|---|---|---|
| e1 | 탄소 = **Asahi F-200GS 카본블랙 · 터보스트래틱** (비정질 기지 + 미세 결정 부영역 · XRD (002) 24.0° · (101) 43.3° · [우리 환산] d₀₀₂ ≈3.70 Å) → 7-1 표 '결함 · 작용기 탄소' 행 + 기저면 · 가장자리 · LiC₆ 를 **범위**로 (digest §4-4 표) · BET · Raman · O/N 없음 → 결함 밀도 못 정함 | S-1 · S-7–S-8 · `Fig. S3a–d` | ✅ |
| e2 | Ag ~60 nm (50–80) → **Ag(111) 평판 근사 무리 없음** · 층 안 응집 2–4 µm | S-1 · p.39091 · `Fig. S2a` · `Fig. 2` | ✅ |
| e3 | 합금 끝 상태는 **속도 의존**: 2.5 mA cm⁻² 에서 Li–Ag 상 증거 없음 · Li 안 Ag 고용 가능 (흐린 Ag 신호) ↔ 저율 Li₁₀Ag₃ (Spencer-Jolly) | S-13 (글자) · `Fig. S13g` | ✅ (EDS 지도) |
| e4 | 운전 중 탄소 = **리튬화 탄소** · 그러나 양은 작다 — 도금 전 저장 `figure-read ≈` 0.14–0.35 mAh cm⁻² · SIMS CB 띠 Li 세기 낮음 | `Fig. S5b,d` · `Fig. S11b` · S-13 | ✅ |
| e5 | Li 친화성 정성 순서는 **"Ag/CB 층 > 맨 SS"** 까지만 (최소점 ≈ −14.5 vs −26 mV) · Ag 위치는 핵생성 과전압 불변 → W 순서를 '석출 위치' 예측에 단독으로 쓰지 말 것 | p.39091 · `Fig. 3a` · `Fig. S5` | ✅ |

**연속체 · DEM (Ag/C 층 구조 · Li 가 쌓이는 위치)**

| # | 쓸 거리 | 근거 위치 | 직접 봤나 |
|---|---|---|---|
| e6 | 층 구조 — 20 → ~13 µm · 22.5/67.5/10 wt% ([우리 환산] Ag ≈5 vol%) · 구조화 87.5 % CC 쪽 절반 · ~5 µm 부층 · `figure-read ≈` 누적 Ag 90 % CC 쪽 (구조화) / 73 % SE 쪽 (비구조화 — '균일' 아님) | p.39090–39091 · S-2 · `Fig. 2` · `Fig. S4` | ✅ |
| e7 | CB 1차 입자 `figure-read ≈` 40–60 nm · 응집체 ~80 nm (NTA) · 사슬 망 | `Fig. S3a,b` · `Fig. S2b` | ✅ |
| e8 | **다공도 · 면밀도 미기재** → 자유 변수 ([우리 환산] 277.9 mg 이 100 cm² 에 다 붙었다면 13 µm 층 다공도 3–11 % — 'spongy porous' 와 모순 → 실제 부착률 < 100 %) | p.39090 · S-2 | 그림 없음 (글자) |
| e9 | **Li 위치 정답지** — 구조화: CC 위 ~20 µm (20–25) · 층이 SE 쪽으로 / 비구조화: 층은 CC 쪽 · Li 는 층 ↔ SE | p.39092–39093 · S-16–S-18 · `Fig. 4a–i` · `Fig. S13` · `Fig. S14` | ✅ |
| e10 | **계면 셋 + 층 안 갈라짐** — 구조화에서도 Ag/CB 조각이 CC 에 남음 · 밀린 띠 `figure-read ≈` 3–6 µm (압착 13 µm 의 1/4–1/2) · 논문 언급 없음 | `Fig. 4a` · `Fig. S13e` | ✅ |
| e11 | 운전 조건 — 60 °C · 4 MPa (2–20) · 1 / 2.5 mA cm⁻² · 실패 3 mA cm⁻² (풀셀 · 2 MPa) / 3.5 mA cm⁻² (열간 3전극) · 장치 = 나사 + 토크 렌치 조인 틀 ([다른 카드] doerrer2021) | p.39090–39092 · S-11–S-12 · `Fig. S10` | ✅ |
| e12 | 점착 교란 — Liao 2025 와 같은 방향 예측 → DEM 박리에 **층\|CC · 층\|SE · 부층 경계** 셋을 등록 (digest §7-3) | 논문 자료 없음 (우리 종합) | — |
| e13 | 성장 과전압 — 1 mA cm⁻² 에서 Ag/CB 가 SS 보다 1–2 mV 더 음 ([우리 환산] ≈1.5 Ω cm²) · 2.5 mA cm⁻² 에서 구조화가 ≈5 mV 작다 (자릿수 참고만) | `Fig. 3a` · `Fig. S10b,c` | ✅ |
| e14 | 비구조화 Li 국부 두께 `figure-read ≈` 37–43 µm (이론 24–27 µm 보다 큼 → 국부 집중 단서 · 스케일 불확실 ±30 % 이상) | `Fig. 4g` · `Fig. S13a` | ✅ |

## (f) 그림 크롭 요약

- `extract_figures.py --slug … --pdf <본문> <SI> --clean` → **19 장** (본문 `Fig. 1–5` · SI `Fig. S1–S14`) · **놓친 캡션 0** (`missing_labels` 빈 목록 · 경고 절 안 뜸) · 논문에 표 없음 · 손 크롭 불필요 · 오탐 없음.
- 실독 **16 장**: `Fig. 2` · `3` · `4` (a · g 확대) · `5` · `S2` · `S3` · `S4` · `S5` · `S6` · `S8` · `S9` · `S10` · `S11` · `S12` · `S13` (a · e 확대) · `S14` + `Fig. 1` 은 본문 쪽 렌더로만. 안 본 것: `S1` · `S7`.
- 본문 서술과 어긋난 그림: `Fig. S4b` (비구조화 '대략 균일' ↔ 73 % SE 쪽) · `Fig. S6` ('셀 간 편차보다 큰 이득' ↔ 구조화 셀 3 꼴찌) · `Fig. 4a` · `Fig. S13e` (CC 에 남은 조각 · 밀린 띠 3–6 µm · Li 두께 횡편차 — 언급 없음) · `Fig. 3a` (성장 과전압은 SS 가 덜 음 — 언급 없음) · `Fig. S12` (BE 참조 보정 안 된 것으로 보임).
- **글자 대조 (병렬 충돌 점검)**: 처음 글자를 scratchpad 공용 이름 `main.txt` · `si.txt` 로 뽑아 읽었고, 지금 그 두 파일은 다른 논문 (Fuchs 2023 SI 등) 으로 덮여 있다 → 전용 폴더 (`scratchpad/<slug>/`) 에 다시 뽑아 제목 · 저자 · 쪽 (본문 39089–39096 · SI S-1–S-19) 과 digest 에 쓴 숫자 · 문구 ≈100 개를 대조 — **전부 일치 (어긋남 0)**. 그림 크롭 · figures.json 은 도구가 PDF 에서 직접 만들어 영향 없음.

## (g) Jeff Sakamoto 저자 여부

**아니다.** 저자 = Metzler · Doerrer · Sun · Matthews · Liotti · Grant (Oxford). Sakamoto 는 참고문헌 7 (Masias 외 2019) · 37 (Haslam · Sakamoto 2023) 에만 나온다.

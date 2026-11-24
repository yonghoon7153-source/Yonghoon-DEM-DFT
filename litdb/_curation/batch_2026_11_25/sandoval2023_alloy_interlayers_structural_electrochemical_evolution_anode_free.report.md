# 끝 보고 — sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free (2026-11-24 · litdb-curator · 배치 2026-11-25 #2)

쓴 파일은 셋이에요.
- digest `litdb/papers/sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free.md` (16 절 · 표 칸 수 어긋남 0 — `build_index.py --check` 표 셀수 점검 4 문서 모두 ✅)
- 그림 `litdb/figures/sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free/` (크롭 17 장 + figures.json · 전부 `viewed: true`)
- 이 보고 파일

공유 파일 · git 은 안 건드렸어요. 단, 지시받은 추출 명령이 `litdb/figures/_sources.json` 에 이 slug 항목을 자동으로 넣었어요 (손 안 댐 · JSON 멀쩡 · 같은 배치 kotakadi2025 · park2025 항목도 살아 있음 · 이 slug 는 `figures: 16` 으로 적혀 있어요 — 손 크롭 `fig_5.png` 는 안 셌어요).
Sup2 엑셀 넷은 batch.json 의 sha256 과 맞는 것을 확인하고 `python3 -I` + openpyxl 로 scratchpad 에 CSV 로 풀어 읽었어요 (inbox 파일 자체는 안 바꿈).

확인한 것
- 웹앱 테스트 클라이언트 `/paper/<slug>` 200 · 그림 17 장이 다 붙고 `paper_figure_notes` 가 17 개 키 전부 (f1–f6 · fS1–fS11) 에 붙어요.
- 원소 태그 Li · Ag · Au · Cu · P · S · Cl · Ni (선언 정본) · 원소 쪽 순위 Ni 3 · Au 5 · Cu 9 · Ag 14 · Li 22 위. 기법 태그는 비웠어요 (`methods: —` · EIS · FIB · µCT 가 METHOD_MAP 에 없어요).
- Sakamoto 배지 오탐 없음 (`_paper_pis` = `[]` · 저자 줄의 '저자가 아니다' 마디가 걸러져요).
- `pytest webapp/tests/test_v3_literature.py` → 20 passed.
- `build_index.py --check` → 이 slug 는 두 곳에만 떠요: "어느 인덱스에도 없음 **[dem]**" · "comparison_vs_ours_DEM.md 미편입". 아래 (a) · (b) 를 넣으면 풀려요. 분류기가 **[dem]** 으로 봐요 (haslam2025 · sandoval2025 와 같은 쪽).
- `extract_figures --inbox` → digest 를 쓴 뒤 본문 · SI 가 **제목 100 %** 로 자동 짝지어져요 (보고 양식 PDF 만 짝 없음 — 그림이 없어 괜찮아요).
- talk 인입 대기열 (`litdb/talks/` 에서 그 표가 있는 유일한 파일 `lee2026_skku_mlip_materials_design.md`) 에 이 논문은 없어요.
- 우리 점착 W 값은 digest 에 없어요 (위치만 — 보고서 §2 · §2-3 · `db/properties/adhesion.json`).

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 + 11-24b 12 편)` — `becker2026_…` 행 (LPSCl 금속 층) 과 `haslam2025_…` 행 (LLZO 금속 층) 사이가 맞아요. 절 머리의 편 수 · 묶음 표기는 메인이 고쳐요. 🏷 없음 (Jeff Sakamoto 저자 아님 · (g)).

```
| `papers/sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free.md` **(본문 21 pp + SI 10 pp + 표준 보고 양식 2 pp + 원자료 xlsx 4 (Sup2 13 중) · 크롭 17장 (도구 16 + 손 1 = `Fig. 5` — 캡션이 다음 쪽) 전부 실독 (확대 5 곳) · 엑셀로 전압 · CE · R₁ · R₂ · R_tot · Nyquist 대조 · 2026-11-24)** | **[외부·exp(정전류 · in situ EIS · PFIB/cryo-FIB-SEM · µCT) + 2D 전위 모형·⭐⭐ LPSC 무음극에서 Au · Ag 100 nm 층 — 균일 석출 · CE ↑ · 박리 끝 접촉 손실 ↓ · Au 입자 약 절반이 SE 에 붙어 남는다 · ✅ SE = Li₆PS₅Cl (우리 comp1 조성) · 젖음 · 점착 측정 0 · 원자단위 계산 0]** ✅ **Stephanie Elizabeth Sandoval**/John A. Lewis/Bairav S. Vishnugopi/Douglas Lars Nelson/Matthew M. Schneider/Francisco Javier Quintero Cortes/Christopher M. Matthews/John Watt/Mengkun Tian/Pavel Shevchenko/Partha P. Mukherjee/**Matthew T. McDowell\*** (Georgia Tech · Purdue · LANL · Argonne APS), "**Structural and electrochemical evolution of alloy interfacial layers in anode-free solid-state batteries**" — ***Joule* 7, 2054–2073 (2023)**, DOI `10.1016/j.joule.2023.07.022`. Li \| Li₆PS₅Cl (375 MPa) \| Cu 10 µm (± Au · Ag · Ni 100 nm 전자빔 증착) 반쪽 셀 · 0.25 mA cm⁻² · 1.0 mAh cm⁻² · 15 MPa · 25 °C: 맨 Cu 는 핵 골 (절대 −18.5 mV · 엑셀) · Li 불균일 (최대 3.4 µm · SE 기공 속 Li) · **≤ 5 사이클 단락 (8 셀)** · CE 96.9–98.2 % / Au · Ag 는 골 없음 · 5.0–5.3 µm 고름 · **10 사이클 CE 99.12 · 99.06 %** (엑셀 확인) · 단락 Au ≈15 · Ag ≈30 사이클 (완전 셀은 Au 19 > Ag 8) · **Au → Li–Au 입자가 Cu\|Li 와 Li\|LPSC 에 약 반씩** (저자 가설: Au–S 결합) · **Ag → 녹음 + Ag 풍부 입자 (첫 도금 Li\|LPSC 쪽 → 5 사이클 Cu\|Li 쪽 뭉침)** · µCT (2 mm · 2 mAh cm⁻²) 두께 Cu 0–40 µm (평균 6.7) 대 Ag 평균 10 µm · in situ EIS 박리 끝 R_tot 상승 (5 사이클) Cu +29.6 · Au +12.8 · Ag +5.3 Ω cm² (엑셀 산수) · 비합금 대조 (스테인리스 · Ni/Cu) 도 접촉 손실 원호 · 2D 모형 (κ 1.8 mS cm⁻¹ · 50 × 15 µm · BV) η 20 µm 섬 0.03 · 5 µm 0.085 V 대 탈합금 문턱 0.05 · 0.07 V. ⚠ 합금 셀 첫 박리는 **4 h 시간 제한에서 끊김** (첫 CE ≈100 % = 천장) · 'Pristine' (`Fig. 4A`) = `Fig. S8` t₁ (엑셀 61/61) · 모형 i₀ 미기재 (카드 산술 ≈0.5 mA cm⁻² · 같은 논문 EIS 와 10–50 배 차 · SSE 수송 몫 < 1 mV) · '합금이 계면으로 돌아온다' 는 박리 뒤 단면 없음 · µCT 셀 조건 다섯이 다름 · 셀 하나씩 | **무음극 합금 층 (Au · Ag) — LPSC 판 · 합금 상 자리 · 박리 끝 접촉 손실 (W_ad 보고서 §7 ③ · §8-1 · §8-3 · §8-4 · §8-5 실험 대조 · DEM 정성 입력)** (exp, 외부 · LPSCl) |
```

## (b) `comparison_vs_ours.md` 에 넣을 줄

물성 4축 (A–D) 에는 **넣을 것이 없어요** (σ · 탄성 · 띠틈 측정이 없고 κ 1.8 mS cm⁻¹ 는 남의 측정을 모형에 넣은 값이에요). **§E (환원 / 음극 Li 금속 계면)** 에 한 줄과 Reference key 한 줄이에요. 분류기가 [dem] 이라 `comparison_vs_ours_DEM.md` §I 카드도 넣어야 `--check` 가 풀려요.

§E 행 (haslam2025 · becker2026 행 근처):
```
| **🆕 (2026-11-25) LPSCl 무음극에서 얇은 합금 층 (Au · Ag 100 nm · Cu 위 증착) 은 SE 쪽에도 남는다 — Au 는 Li–Au 입자로 Cu\|Li 와 Li\|LPSC 에 약 반씩 (저자 가설 Au–S 결합) · Ag 는 Li 에 녹고 Ag 풍부 입자가 첫 도금 뒤 Li\|LPSC 쪽 → 5 사이클 뒤 Cu\|Li 쪽에 뭉침 · 합금 층이 박리 끝 접촉 손실 (EIS 저주파 원호 · R_tot 상승 5 사이클 Cu +29.6 · Au +12.8 · Ag +5.3 Ω cm²) 을 줄이고 10 사이클 CE ≈99.1 % (맨 Cu ≤ 5 사이클 단락)** | **[Sandoval23Alloy]** `Fig. 1` · `Fig. 2B,C,F–I` · `Fig. 4` · `Fig. 5` · `Fig. S8–S10` · p. 2056–2065 · Sup2 엑셀 (Li₆PS₅Cl · 15 MPa · 25 °C · 0.25 mA cm⁻² · 셀 하나씩 · 합금 셀 첫 박리는 4 h 시간 제한에서 끊김) | 환원 가장자리 **1.717 V** (Li 교환 0 · comp1 = modelc · grand-potential) — 같은 SE 조성 · 첫 도금에서 CC\|LPSC · 합금\|LPSC 는 환원된다 (속도는 계산 밖 · 카드 산술: LPSC 10 nm 가 0 V 산물이 되는 전하 ≈1.5 µAh cm⁻² = CE 0.15 % 라 이 논문 CE 로는 안 보인다) · Li–Au · Li–Ag 합금 · 고용 계산 없음 (W_ad 보고서 7 절 ③ 제안 단계) · Li\|SE · 합금\|SE 점착 계산은 보고서 §2-3 LPSCl\|Ag(111) 만 (값은 보고서 §2 · `db/properties/adhesion.json` — 옮기지 않는다 · Au 없음) | ⚪ 축 다름 (전제 대조) · ⚠ 가넷 [Haslam25Alloy] 의 'SE 에 안 남는다' 와 어긋남 (SE · 막 시작 자리 · Li 양이 다 다르다) · ⛔ 분극 · 단락 사이클 · 두께 · 모형 섬 크기 문턱 (i₀ 미기재) 을 우리 값 옆에 두지 않는다 |
```

Reference key 행:
```
| **[Sandoval23Alloy]** ⭐⭐ **LPSC 무음극의 Au · Ag 100 nm 층 — 합금 상 자리 (PFIB · cryo-FIB · EDS) · µCT 두께 지도 · in situ EIS 박리 끝 접촉 손실 · Li 섬 전위 모형** · ⛔ **exp + 2D 연속체 모형 · 젖음 · 점착 측정 0 — A–D 물성 4축 진입 금지** (§E 1 행만) | Stephanie Elizabeth Sandoval/John A. Lewis/Bairav S. Vishnugopi/…/Partha P. Mukherjee/Matthew T. McDowell\* (Georgia Tech · Purdue · LANL · Argonne APS) *Joule* 7, 2054 (2023) | `papers/sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free.md` ✅ | exp |
```

`comparison_vs_ours_DEM.md` §I 카드 (지금 마지막이 I-33 `xie2024_…` · 같은 배치 둘도 번호를 원할 수 있어 메인이 매겨요):
```
### I-34. `sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free` — ★★ (exp + 2D 전위 모형 · ⛔ 점착 정량 0 · ✅ LPSCl 계) **Au · Ag 100 nm 층이 LPSC 무음극의 박리 끝 접촉 손실을 줄인다 — Au 입자 약 절반이 SE 에 붙어 남는다 · Li 섬 전위 모형 = 덮임 분율 → 국부 η 의 식 (i₀ 미기재)**

> **무엇을 주나.** Li | Li₆PS₅Cl (375 MPa) | Cu 10 µm (± Au · Ag · Ni 100 nm) · 15 MPa · 25 °C · 0.25 mA cm⁻² · 1 mAh cm⁻²: 맨 Cu 는 불균일 석출 (≤ 3.4 µm · SE 기공 속 Li) · ≤ 5 사이클 단락 (8 셀) / Au · Ag 는 5.0–5.3 µm 고름 · 10 사이클 CE ≈99.1 % · Au → Li–Au 입자 Cu|Li · Li|LPSC 약 반씩 · Ag → 녹음 + Ag 풍부 입자 (Li|LPSC → 5 사이클 Cu|Li) · µCT 두께 지도 (2 mAh cm⁻² · Cu 0–40 µm 평균 6.7 · Ag 평균 10 µm) · in situ EIS 박리 끝 R_tot 상승 Cu +29.6 · Au +12.8 · Ag +5.3 Ω cm² (5 사이클 · 엑셀 산수) · 2D 모형 (κ 1.8 mS cm⁻¹ · 50 × 15 µm · BV) η 20 µm 0.03 · 5 µm 0.085 V.
>
> **★ DEM 쪽에 닿는 곳.**
> ① 박리 끝 국부 전류 = I/f (f = Li 덮임 분율) → η = (2RT/F)·asinh(I/(2 i₀ f)) — `Fig. 6C` 가 이 식 하나로 재현된다 (카드 산술 i₀ ≈0.5 mA cm⁻²) · SSE 수송 몫 < 1 mV → DEM 접촉 분율이 그대로 들어가는 자리 · 단 i₀ 를 먼저 정한다 (같은 논문 EIS 는 i₀ ≳5–26 mA cm⁻²).
> ② 접촉 손실의 상대 크기 (R_tot 상승 Cu ≫ Au > Ag) · 저주파 원호 10¹–10² Hz → 접촉 분율 → 임피던스 대조 표적 (kim2026 단일 주파수 법과 같은 대역).
> ③ 석출 두께 (FIB 5 µm 급 · µCT 0–40 µm 지도) → 석출 형태 대조 표적 (정성).
> ④ 압력 단계 펠릿 375 · 전극 붙이기 15 · 운전 15 MPa (µCT 225 · ≈10 MPa) — CC|SE 접촉은 15 MPa 로만 만들었다.
> ⑤ 합금 입자가 SE 쪽에 남는 배치 → 계면 접촉 모형에 '입자 덮임' 항 (W 순서 질문은 DFT 쪽).
>
> **⛔ 인용 금지 / 한정어**
> · 모형의 섬 크기 문턱을 수치로 옮기지 않는다 (i₀ 미기재 · 역산 i₀ 가 같은 논문 EIS 와 10–50 배 차 · 합금 = 비반응 경계).
> · 첫 CE ≈100 % 는 4 h 시간 상한 · 'Pristine' 라벨 의심 · '합금이 돌아온다' 는 박리 뒤 단면 없음.
> · 셀 하나씩 · µCT 셀은 지름 · 용량 · 전류 · 압착 · 적층압 · 분말이 실험실 셀과 다르다 · 젖음 · 점착 측정이 아니다 · 대조 표적이지 보정 표적이 아니다.
> 상세: digest §3e · §3f · §7c · §10 · §11.
```

## (c) `pdf_map.tsv`

**필요 없어요.** digest 가 생긴 뒤 `--inbox` 가 본문 · SI 를 **제목 100 %** 로 자동 짝지었어요. 보고 양식 PDF (`…_sup3_reporting_form.pdf`) 는 짝이 없지만 그림이 없어 그대로 두는 게 나아요 — slug 접두 한 줄 (`sandoval2023_alloy_interlayers`) 을 넣으면 보고 양식까지 SI 로 붙어 `--inbox --run` 이 빈 PDF 를 자르려 해요.

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

발견 검색은 Crossref REST 로만 했어요 — 제목 없이 주제어 + 2024-06 이후 3 번 (무음극 · 합금 층 · 황화물 / 무음극 · 접촉 손실 · 임피던스 · Li 섬) · 저자 (McDowell · Mukherjee/Vishnugopi) 2 번 · DOI 확인 조회 9 번. 출판사 페이지 · 본문은 안 열었어요. 같은 배치의 kotakadi2025 · park2025 (*Adv. Energy Mater.* 15, 2405129 · Ag–C 층 Li 동역학) 는 빼고 골랐어요.

| # | 논문 | 왜 (이 digest 와의 연결) | litdb | 확인 |
|---|---|---|---|---|
| 1 | T. Zhang, K. Huang, Y. Zheng, …, Z. Chen, "Loss and Recovery of Effective Lithium in Anode-Free Solid-State Lithium Metal Batteries", *Adv. Mater.*, 37, e05695 (2025) · DOI 10.1002/adma.202505695 | 무음극 SSB 의 '유효 Li' 손실 · 회복 — §10-① (CE 천장) · 맨 Cu 의 남은 Li 해석과 바로 이어진다 | 없음 | Crossref ✓ (제목 · 권 · 쪽 · 2025-08) |
| 2 | S. Banerjee, B. S. Vishnugopi, P. P. Mukherjee, "Probing the Impact of Vacancy Diffusion on Void Dynamics at the Lithium Metal–Solid Electrolyte Interface", *Adv. Sci.*, 13, e15827 (2026 · 온라인 2025-11) · DOI 10.1002/advs.202515827 | 같은 모형 그룹의 공극 동역학 — 이 논문 전위 모형이 안 푼 '공극 생성 · 공공 확산' 의 빈칸 | 없음 · **11-24b 목록 #5** | 목록에서 확인됨 |
| 3 | M. A. Thorpe, M. Zhang, D. W. Liao, S. E. Sandoval, Y. Kim, M. T. McDowell, M. D. Thouless, N. P. Dasgupta, "Controlling stack pressure inhomogeneity in anode-free solid-state batteries using elastomeric interlayers", *Matter*, 8, 101955 (2025) · DOI 10.1016/j.matt.2024.101955 | 같은 저자군 · 적층압 불균일 → 석출 불균일 — DEM 압력 분포 입력 · 이 논문은 15 MPa 하나 | 없음 · **11-24b 목록 #33** | 목록에서 확인됨 |
| 4 | S. G. Yoon, B. S. Vishnugopi, E. P. Alsaç, …, M. T. McDowell, "Synergistic Evolution of Alloy Nanoparticles and Carbon in Solid-State Lithium Metal Anode Composites at Low Stack Pressure", *ACS Nano*, 18, 20792 (2024) · DOI 10.1021/acsnano.4c07687 | 같은 그룹 · 합금 나노입자 + 탄소 복합 음극 (저압) — 우리 Ag–C 트랙의 McDowell 쪽 짝 · 같은 모형 저자 | 없음 | Crossref ✓ |
| 5 | M.-G. Jeong, K. B. Hatzell, S. Banerjee, …, P. P. Mukherjee, "Temperature Impact on Lithium Metal Morphology in Lithium Reservoir-Free Solid-State Batteries", *PRX Energy*, 3, 023003 (2024) · DOI 10.1103/PRXEnergy.3.023003 | 이 논문에 없는 온도 변수 · 같은 메조 모형 그룹 | 없음 | Crossref ✓ |
| 6 | J. A. Lewis, S. E. Sandoval, Y. Liu, …, M. T. McDowell, "Accelerated Short Circuiting in Anode-Free Solid-State Batteries Driven by Local Lithium Depletion", *Adv. Energy Mater.*, 13, 2204186 (2023) · DOI 10.1002/aenm.202204186 | ref 34 — 이 논문의 출발점 (박리 끝 국부 Li 고갈 → 섬 → 공극 → 단락 · LPSC) · 다른 report 셋에도 '없음' 으로 떠 있음 | 없음 | Crossref ✓ |
| 7 | J. K. Eckhardt, T. Fuchs, S. Burkhardt, …, C. Heiliger, "3D Impedance Modeling of Metal Anodes in Solid-State Batteries–Incompatibility of Pore Formation and Constriction Effect in Physical-Based 1D Circuit Models", *ACS Appl. Mater. Interfaces*, 14, 42757 (2022) · DOI 10.1021/acsami.2c12991 | ref 59 — 접촉 분율 ↔ 임피던스 (DEM → EIS 다리) · 이 논문이 `Fig. 5` 를 회로 적합하지 않은 이유 | 없음 | Crossref ✓ |
| 8 | B. S. Vishnugopi, K. G. Naik, H. Kawakami, …, P. P. Mukherjee, "Asymmetric Contact Loss Dynamics during Plating and Stripping in Solid-State Batteries", *Adv. Energy Mater.*, 13, 2203671 (2023) · DOI 10.1002/aenm.202203671 | ref 24 — 같은 모형 그룹의 도금 · 박리 비대칭 접촉 손실 메조 모형 (DEM 접촉 쪽) | 없음 | Crossref ✓ |

차순위 (8 편 밖): C. Lee et al., *ACS Energy Lett.*, 6, 3261 (2021) (ref 57 · 모형 κ 1.8 mS cm⁻¹ 의 출처 · Crossref ✓ · 10.1021/acsenergylett.1c01395) · D. K. Singh et al., *Cell Rep. Phys. Sci.*, 3, 101043 (2022) (ref 60 · LPSC 접촉 손실 EIS) · Y. Wang et al., *Adv. Mater.*, 35, 2206762 (2023) (ref 37 · Cu 위 Li₂Te 젖음 · 11-24 목록에 있음).

## (e) W_ad · DEM-DFT 보고서에 쓸 거리 (W_ad 보고서 7 절 · 8 절)

⛔ 전부 LPSC · 15 MPa · 25 °C · 0.25 mA cm⁻² · 셀 하나씩이에요. 숫자는 차수 · 순서로만. "봤나" = 이번에 그림을 직접 보고 읽었나 (✅ 원본 · 🔍 확대 · 📊 엑셀 · 📄 본문만).

| # | 보고서 자리 | 무엇 | 쪽 · 그림 | 봤나 | 11-24b digest 와 |
|---|---|---|---|---|---|
| 1 | **8-3** '얇은 합금 층은 첫 도금 뒤 고체전해질 쪽에 남지 않는다' (haslam2025 근거) | **LPSC 에서는 남는다** — Au 는 Li–Au 입자로 Cu\|Li 와 Li\|LPSC 에 약 반씩 (PFIB · cryo-FIB · EDS 띠 둘) · Ag 풍부 영역도 첫 도금 뒤 Li\|LPSC 쪽 (EDS) · 5 사이클 뒤 Ag 는 Cu\|Li 쪽에 뭉침 | p. 2058–2059 · `Fig. 2B,C,F–I` · `Fig. S4a` · `Fig. S6` | ✅🔍 | haslam2025 (LLZO · 막을 SE 위 · 6.1 mAh) 와 **어긋남** · becker2026 (LPSCl · 160 nm · Ti · 'Ti\|Li 근처가 대부분') 과 **부분 어긋남** (becker 근거는 지도 하나 · 입자 하나 — 그 digest §10-④) · ko2025 Ag (합금\|SE 접촉 유지) 와 **같은 방향** |
| 2 | **8-3** 끝 '그래서 W 를 낼 계면 후보에…' · **7-1** 표 | 후보 더하기: **Li–Au 입자\|LPSCl (또는 환원층 Li₂S 류)** · Li–Au\|Li · Li–Au\|Cu · Li(Ag)\|LPSCl · Ag 풍부 입자\|Cu — 7-1 표에 Au 행이 없다 | 같음 | ✅ | becker2026 digest §7e 의 후보 목록 (Li\|Li₁₅Au₄ · Li(Ag)\|LPSCl) 과 맞고, 'SE 쪽 Li–Au 입자' 가 더해짐 |
| 3 | **2-3** LPSCl\|Ag(111) (S 바깥 · Li·PS₄ 바깥) | 저자 가설 **'Au–S 결합'** 으로 Au 가 SE 에 붙어 남는다 — 같은 틀에 Au(111) 을 더하면 'Au 가 Ag 보다 SE 에 세게 붙나' 를 같은 방법 안의 순서로 잴 수 있다 (우리 해석 · 반응 전 고정 기하라고 먼저 선언 · 8-2) | p. 2059 | 📄 | 이웃 digest 에 없던 질문 (새로 생김) |
| 4 | **8-1** '실제 셀에서 먼저 막히는 쪽은 박리다' | 무음극 LPSC 판 근거: 비합금 극 (Cu · 스테인리스 · Ni/Cu) 은 박리 끝 저주파 원호 (≈50–150 Hz) 와 R_tot 상승이 사이클마다 커지고 (Cu +15 → +30 Ω cm²) 몇 사이클 안 단락 · Ag (+2 → +5) · Au (−1 → +13) 는 작다 · 맨 Cu 는 **첫 사이클부터** 박리 끝 R_tot +53 % (본문은 '접촉 유지' 라 했지만 엑셀로 반박) | p. 2061–2065 · `Fig. 4` · `Fig. 5` · `Fig. S8–S10` | ✅📊 | kasemchainan2019 (박리 공극 → 덴드라이트) 과 **맞음** — 무음극은 낮은 전체 전류에서도 같은 길 · kim2026 (≈10² Hz) 과 **같은 대역** |
| 5 | **8-4** '공극이 생기는 기준은 … 국부 전류다 — DEM 의 접촉 분율이 들어갈 자리다' | Li 섬 전위 모형 (Mukherjee): **말하는 것** — 덮임 분율 f 가 줄면 국부 전류 ≈ I/f 가 커지고 BV 과전압이 탈합금 전위 (Li–Ag 0.05 · Li–Au 0.07 V) 를 넘으면 합금이 Li 를 내놓을 수 있다 · **말하지 않는 것** — 합금 반응 · 합금 속 확산 (합금 = 비반응 경계) · 공극 생성 · 크리프 · 적층압 · 점착 · 젖음 · i₀ (미기재 · 카드 산술 0.5 mA cm⁻² · 같은 논문 EIS 가 주는 i₀ 5–26 이면 켜지는 덮임이 14–22 % → 0.3–2 %) · SSE 수송 몫 < 1 mV · **W 가 들어갈 자리가 모형 안에 없다** | p. 2065–2067 · p. 2070 · `Fig. 6` · `Fig. S11` | ✅ + 카드 산술 | 이웃 digest 에 메조 모형은 없음 — 2 편 (d #2 · #8) 이 빈칸 |
| 6 | **8-5** '실험과 견줄 것' | 핵 과전압 순서의 LPSC 판 **Cu > Au ≈ Ag ≈ 0** (맨 Cu 절대 −18.5 mV · 골 깊이 ≈7.5 mV · 엑셀) · 탈합금 전위 순서 **Au (70 · 160 mV 평탄) > Ag (경사)** — 셀 전압 (IR ≈6–8 mV 섞임) | p. 2056–2057 · `Fig. 1B,C` | ✅🔍📊 | haslam2025 · becker2026 의 순서 (Au > Ag) 와 **맞음** |
| 7 | **8-4** 압력 세 단계 | 실험실 단계 사례: 펠릿 375 MPa · CC 붙이기 15 MPa 5 min · 운전 15 MPa (µCT 셀 225 · ≈10 MPa) | p. 2068–2069 | 📄 | becker2026 (380 · 15 MPa) 와 같은 급 |
| 8 | **8-7** 읽은 논문 목록 | 새 줄: *Joule*, 7, 2054 (2023) · 무음극 Li₆PS₅Cl · Au · Ag 100 nm 층 · cryo/PFIB · µCT · in situ EIS · 전위 모형 · 쓴 곳 8-1 · 8-3 · 8-4 · 8-5 | — | — | — |
| 9 | (부피 변화 서술이 생기면) | 저자 결론: 합금의 제어되지 않은 부피 변화가 **뭉침을 가속** → 입자 고정 필요 — haslam2025 의 '팽창이 공극을 메운다' 가설과 반대 방향 강조 · 한쪽만 싣지 않는다 | p. 2067 | 📄 | haslam2025 §3d 가설과 **어긋남** |

보고서에 넣을 문장 초안 (공유 보고서 규칙대로 값 · 방법 · 한계만):
- 8-3: "황화물에서는 다르게 보였다. Cu 위에 증착한 Au · Ag 100 nm 층의 Li₆PS₅Cl 무음극 셀 (15 MPa · 1 mAh/cm²) 에서 Au 막은 Li–Au 입자로 쪼개져 약 절반이 Li | 고체전해질 계면에 붙어 남았고, Ag 풍부 영역도 첫 도금 뒤 고체전해질 쪽에 보였다 (사후 단면 · 5 사이클 뒤 Ag 는 집전체 쪽에 뭉쳤다). 저자는 Au–S 결합을 가능한 이유로 들었고 재지는 않았다 (Joule, 7, 2054 (2023)). 그래서 Li₆PS₅Cl 셀에서는 합금 입자 | 고체전해질도 운전 중 계면 후보다."
- 8-4: "박리 끝 국부 전류를 Li 섬의 과전압으로 본 연속체 모형은 섬이 줄면 과전압이 합금의 탈합금 전위 (Li–Ag 0.05 · Li–Au 0.07 V) 를 넘어 합금이 Li 를 내놓을 수 있다고 보았다. 이 모형은 Li 덮임 분율과 교환 전류 밀도로 정해지고 (교환 전류 밀도는 원문에 없다), 합금 반응 · 공극 생성 · 점착은 계산하지 않았다 (Joule, 7, 2054 (2023))."

다른 digest 에 남은 '기다림' 표시 (그 파일은 안 고쳤어요 — 메인이 🔗 이어 읽기 · 바로잡기 줄로 붙일 자리):
- `haslam2025_…` — §7b 첫 행 '황화물 쪽 같은 층 실험은 Sandoval 2023 *Joule* (ref 11 · litdb 없음)' · §12-④ · §16 끝 줄 '(litdb 없음)' → 이제 이 digest. 바로잡기 하나: §7c-② '얇은 금속 층을 SE 위에 두면 확인된 합금 자리는 CC 쪽' 은 LLZO 한정 — LPSC (막을 CC 위) 에서는 Au 가 양쪽.
- `sandoval2025_operando_xray_tomography_…` — 머리 '이어 읽기' 의 'Case B 셀의 단면 한 장은 *Joule* 7, 2054 (ref 12 · litdb 없음)' · 참고문헌 표 ref 12 '없음' → 이제 이 digest (`Fig. 3` Ag 셀 = Case B · 2 mAh cm⁻² 두께 평균 10 µm ↔ 그 원자료 9.66 ± 2.29 µm · 맞음).
- `sandoval2025_electro_chemo_mechanics_…` — **바로잡기 둘**: ① SI 표 1 행 Au · Ag 100 nm 'sputtered' → 원문은 **전자빔 증착** (CHA Mark 50 · 1 Å s⁻¹ · p. 2068) ② `Fig. 4b` 읽기 '금속 · 화합물 계열은 시드가 CC 쪽에 남고 Li 가 그 아래' → 원문은 Au 입자가 **두 계면에 약 반씩** (p. 2059 · 그 digest 도 '입자가 두 경계로 갈라져 보임' 단서를 달았어요). 참고문헌 표 ref 29 '—' → 이제 이 digest.
- `choi2025_silver_exsolution_argyrodite_anode_free` 끝 '다음 순번: Sandoval 외 *Joule* 7, 2054' · `metzler2026_…` '차순위' → 이제 이 digest.
- 11-24b 묶음의 '🔗 이어 읽기 · 바로잡기' 절 (fuchs2023 · cicvaric2026 · kim2026 · wang2019 · sandoval2025_electro_chemo · baer2026 · kang2026 · lu2026 · metzler2025 · metzler2026 · spencerjolly2023 · wang2020 · yang2021 · damore2022) 에는 이 편을 기다린다는 줄이 **없어요** (2026-11-24 grep).

## (f) 그림 · 자료 크롭 요약

- **크롭 17 장** = 도구 16 (본문 5 + SI 11) + **손 크롭 1** (`fig_5.png` — 그림은 PDF 10 쪽 래스터 · 캡션은 11 쪽이라 도구가 '번호 공백 · 영역 없음' 으로 건너뜀 · 래스터 bbox + 2 pt 를 300 dpi 로 · figures.json `manual_crop` 사유 · `missing_labels` f5 에 `resolved`). 표 0 · `auto_fallback` 표시 0 · 빈 크롭 0 · 오탐 0.
- **17 장 전부 봤어요** (Read · 원해상도). 키워 다시 본 곳: `Fig. 1B` 삽입도 (×3) · `Fig. 1C` (×1.6) · `Fig. 2B,C` 점선 상자와 EDS (×1.3–1.5) · `Fig. 2F–I` (×1.4). 방법 쪽 µ · × 기호는 쪽 렌더로 확인 (글자층이 µ 를 m 으로 깨뜨림 — 10 µm · 36 µL · 2× 렌즈).
- **엑셀 넷 (받은 것 · 다 썼어요)**: `figure4` (4a Nyquist 18 개 · 4b R₁ · R₂) · `figure5` (5a 첫 사이클 전압 1 s 간격 · 5b R_tot 120 점 · 5c Nyquist 18 개) · `figureS2` (평균 CE ± SD 15 사이클) · `figureS8` (Nyquist 18 개). 그림 판독을 엑셀 값으로 바꾼 곳 = '엑셀 확인', 새로 낸 값 = '엑셀 산수' (digest §3g 에 계산법). 엑셀로 찾은 것: 합금 셀 첫 박리가 **4 h 시간 제한에서 끊김** · Au 첫 CE 100.00 % (본문 99.98) · **'Pristine' = t₁** (61/61) · Cu 첫 박리 끝 R_tot +53 % · 박리 끝 2.0 V (방법 0.5 V) · EIS 간격 20 분 (본문 10 분) · 저주파 원호 정점 ≈50 Hz (본문 150 Hz).
- **안 온 엑셀 — digest 완성에 꼭 필요한 것은 없어요.** 있으면 좋은 것:
  - `Figure 1` 엑셀 (11 MB) — 2–30 사이클 박리가 시간으로 끝났나 전압으로 끝났나 (§10-① 의 '이후 CE ≈99 %' 판정) · `Fig. 1A` Ag 박리 중간 혹.
  - `Figure 6` 엑셀 (2.5 MB) — 모형 출력에서 i₀ · α 를 직접 확인 (§10-⑤ 카드 산술 0.5 mA cm⁻² 검증).
  - `Fig3_Li deposited on Ag.stl` · `Fig3_Li deposited on bare Cu.stl` (6.7 · 7.3 MB) + `Fig3e-f_heatmap_code.pdf` (1.6 MB) — µCT 두께 분포 (평균 · 편차 · 덮임 분율) 를 DEM 대조 표적으로 쓸 때.
  - `Figure S7` · `Figure S9` · `Figure S10` 엑셀 (5.3 · 4.5 · 4.7 MB) — 대칭 · 비합금 대조 셀 반주기가 ≈5–6 h 로 보이는 시간축 의문 (§4h) 확인용 (판정에는 안 쓰임).
  - `Figure S3` 엑셀 (14.8 MB) — 완전 셀 사이클 수 (본문 '19 사이클' · 그림은 13 까지) 확인용.

## (g) Jeff Sakamoto 저자 여부

**아니에요.** 본문 첫 쪽 저자 12 명 (Sandoval · Lewis · Vishnugopi · Nelson · Schneider · Quintero Cortes · Matthews · Watt · Tian · Shevchenko · Mukherjee · McDowell) · SI 표지 · Crossref 저자 목록 셋 다 대조했어요. Sakamoto 는 참고문헌 (9 · 25 · 27 · 29 · 32 · 33 · 40) 에만 나와요 (같은 MUSIC EFRC 자금이지만 공저 아님). INDEX 행에 🏷 를 달지 않아요 · 웹앱 배지도 안 붙어요 (`_paper_pis` = `[]` 확인).

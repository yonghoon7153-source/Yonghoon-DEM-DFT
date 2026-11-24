# 끝 보고 — haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free (2026-11-24 · litdb-curator · 배치 2026-11-24b #4)

쓴 파일은 셋이에요.
- digest `litdb/papers/haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free.md` (458 줄 · 표 13 개 · 칸 수가 어긋난 줄 0)
- 그림 `litdb/figures/haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free/` (크롭 9 장 + figures.json)
- 이 보고 파일

공유 파일 · git 은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 자동으로 넣었어요 (손 안 댐).
⚠ 메인 체크포인트 커밋 (7a9f8c62 그림 · 98271324 digest) 에 앞선 판이 들어가 있어요. 그 뒤 digest 를 세 줄 고쳤어요 (Ag 계면 수명 문장 둘 · 수송 해석을 '우리 해석' 으로 낮춤) — 최종본은 지금 작업 트리에 있는 파일이에요.

확인한 것
- 웹앱 `/paper/<slug>` 200 · Sakamoto 배지가 떠요 (`_paper_pis` = `['sakamoto']`). 그림 9 장이 다 붙고, `paper_figure_notes` 가 9 개 키 전부 (f1–f3 · fS1–fS6) 에 붙어요.
- 원소 태그 Li · Au · Ag · Cu · La · Zr · Ta · O (선언 정본). 원소 쪽 링크는 Au 3 위 · Ag 3 위 · Cu 4 위 · Ta 3 위 · Li 6 위예요. 기법 태그는 비웠어요 (`methods: —` · 이 논문 기법 (EBSD · SEM · 광학 3D) 이 METHOD_MAP 에 없어요).
- `pytest webapp/tests/test_v3_literature.py` → 20 passed.
- `build_index.py --check` (rc 1 · 배치 대기분 때문) → 이 slug 는 두 곳에만 떠요: "어느 인덱스에도 없음 **[dem]**" · "comparison_vs_ours_DEM.md 미편입". 아래 (a) · (b) 를 넣으면 풀려요.
  ⚠ 분류기가 이 slug 를 **[dem]** 으로 봐요 (slug 의 'morphology' · 'microstructure' 가 DEM 낱말). 이웃도 섞여 있어요 (wang2020 · sandoval2025 = dem · fuchs2023 · lee2022 = dft). 그래도 이웃 셋이 다 INDEX.md 🌱 절에 있고, `--check` 는 두 인덱스 · 두 비교 문서 어디에 있어도 받아요.
- `extract_figures --audit` → 이 slug 경고 없음 (본문 3 · SI 6 · 표 0). `--inbox --only haslam2025` → 본문 · SI 가 제목 55 % 로 자동 짝지어져요.
- talk 인입 대기열 (`litdb/talks/` 에서 그 표가 있는 유일한 파일 `lee2026_skku_mlip_materials_design.md`) 에 이 논문은 없어요. 역링크는 필요 없어요.
- 우리 점착 W 값은 digest 에 없어요 (위치만 — 보고서 §2 · `db/properties/adhesion.json`). digest 안의 J m⁻² 숫자는 liao2025 의 문헌 문턱 (≈10 J m⁻²) 하나뿐이에요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — wang2020 · fuchs2023 · sandoval2025 행 근처예요. (분류기가 [dem] 이라 `build_index.py` 를 다시 돌리면 INDEX_DEM.md 에도 생성돼요. 어느 쪽이든 `--check` 는 통과해요.)

```
| `papers/haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free.md` **(본문 7 pp + SI 10 pp · 크롭 9장 전부 실독 (확대 · 픽셀 측정 8 곳) · 2026-11-24)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp·⭐⭐ 무음극 LLZO 에서 Au · Ag 100 nm 합금 층이 석출 Li 의 형태 · 결정립 · 합금 상 행방을 바꾼다 — W_ad 보고서 7 절 Ag 의 실험 짝 · ⚠ LLZO 계 (LPSCl 로 수치 이식 금지) · 젖음 · 점착 측정 0 · 원자단위 계산 0]** ✅ **Catherine G. Haslam**/**Till Fuchs** (공동1)/D. W. Liao/J. Becker/N. P. Dasgupta/J. Janek/**Jeff Sakamoto\*** (Michigan · MUSIC EFRC + JLU Giessen + UCSB), "**The Effect of Alloying Interlayers on Lithium Anode Morphology and Microstructure in "Anode-Free" Solid-State Batteries**" — ***ACS Energy Lett.* 10, 2285–2291 (2025)**, DOI `10.1021/acsenergylett.5c00149`. Ta-LLZO (2–2.8 mm) · 25 °C · 2.5 MPa · 6.1 mAh cm⁻² (≈30 µm): 맨 Cu (900 °C 확산 접합) 는 0.10 안정 · **0.25 mA cm⁻² 에서 ≈0.4 mAh cm⁻² 단락** · Li 핵 골 figure-read ≈5 · ≈25–30 mV / Au (≈100 nm '추정') · Ag (100 nm) + 얹기만 한 Cu 는 0.10 · 0.25 모두 단락 없음 · 핵 골 없음 · Au 합금 평탄 ≈0.2 · 0.1 V · Ag 는 0.01 에서만 평탄 셋 (figure-read ≈0.08 · 0.054 · 0.008 V) · 높낮이 **±17.5 → ±3.5 µm** · **Au → Li₁₅Au₄ 입자 (Cu\|Li 계면 줄 + Li 속)** · **Ag → 6.1 mAh 뒤 따로 된 상 없음 (녹음) · 0.5 mAh 에서 Ag 풍부 상 (~5 at%) 이 CC 쪽에** · EBSD 결정립 폭 **37.8 ± 26.0 (Au) · 33.6 ± 18.7 (Ag) vs 40.8 ± 8.9 µm** (기둥형 → 비스듬 · 나란한 경계가 섞임). ⚠ 평균 차는 1 SD 안 (카드 산술 t ≈0.4 · 1.3) · `Fig. 3d` 가로축이 ≈70 µm 에서 잘려 ≈81 µm Au 결정립이 그림 밖 · `Fig. S6b` (Au 0.10) 에 ≈77 µm · 접합 유무 · 전류가 합금 층과 교락 · n = 1 · 3D 넓이 본문 0.16 vs 스케일바 ≈0.017 cm² · '> 6 µm' 는 카드 산술 ≈12.5 µm · 'Figure 1e' → 3e · 2 전극 · 박리 없음 | **무음극 합금 층 (Au · Ag) — Li 형태 · 결정립 · 합금 상 행방 (W_ad 보고서 §7 ③ · §8-3 실험 대조 · DEM 정성 입력)** (exp, 외부 · LLZO) |
```

## (b) `comparison_vs_ours.md` 에 넣을 줄

물성 4축 (A–D) 에는 **넣을 것이 없어요** (LLZO 의 σ · 탄성 · 띠틈이 이 논문에 없어요). **§E (환원 / 음극 Li 금속 계면)** 에 전제 대조 한 줄과 Reference key 한 줄이에요.

§E 행:
```
| **🆕 (2026-11-24) 얇은 합금 층 (Au · Ag 100 nm) 은 첫 도금 뒤 SE 에 남지 않는다 — LLZO 무음극에서 Au 는 Li₁₅Au₄ 입자로 CC 쪽 Li 에 남고 (Kikuchi), Ag 는 6.1 mAh cm⁻² 뒤 따로 된 상이 없다 (0.5 mAh cm⁻² · ~5 at% 에서만 Ag 풍부 상) · 합금 층 + 비접합 Cu 는 0.25 mA cm⁻² 에서 단락 없음 (접합 맨 Cu 는 ≈0.4 mAh cm⁻² 에 단락) · 높낮이 ±17.5 → ±3.5 µm** | **[Haslam25Alloy]** `Fig. 1` · `Fig. 2` · `Fig. 3e` · `Fig. S3` · p. 2287–2289 (가넷 LLZO · 25 °C · 2.5 MPa · 셀 하나씩 · 접합 유무 교락 · 확인된 합금 자리 = CC 쪽은 그림 배치에서 읽은 카드 해석) | 환원 가장자리 **1.717 V** (Li 교환 0 · comp1 = modelc · grand-potential) — LPSCl 위 같은 층은 첫 충전에서 SE 환원이 끼어든다 (속도는 계산 밖) · Li–Au · Li–Ag 합금 · 고용 계산은 아직 없다 (W_ad 보고서 7 절 ③ 제안 단계) · Li\|SE · 합금\|SE 점착 계산 없음 | ⚪ 축 다름 (전제 대조) · ⛔ 단락 전류 · 높낮이 · 결정립 · 평탄 전압을 LPSCl 값으로 옮기지 않는다 · 옮겨도 되는 것은 'Au 불용 → Li₁₅Au₄ · Ag 가용' 금속끼리의 사실뿐 |
```

Reference key 행:
```
| **[Haslam25Alloy]** ⭐⭐ **무음극 LLZO 의 Au · Ag 합금 층 — Li 형태 (높낮이) · 결정립 (cryo-EBSD) · 합금 상 행방** · ⛔ **LLZO · exp 전용 · 젖음 · 점착 측정 0 — A–D 물성 4축 진입 금지** (§E 1 행만) | Catherine G. Haslam/Till Fuchs/D. W. Liao/J. Becker/N. P. Dasgupta/J. Janek/Jeff Sakamoto\* (Michigan · MUSIC · JLU Giessen · UCSB) *ACS Energy Lett.* 10, 2285 (2025) | `papers/haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free.md` ✅ | exp |
```

(선택) 분류기가 [dem] 이라 `comparison_vs_ours_DEM.md` §I 카드도 맞는 자리예요 — 번호는 메인이 매겨요:
```
### I-xx. `haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free` — (🏷 Jeff Sakamoto 공저 · 인접 축 · 점착 정량 0 · ⚠ LLZO) 합금 층 (Au · Ag) 무음극 Li — 형태 · 결정립 · 합금 상 행방 · CC|SE 접합이 옆 성장을 막는다 (추론)

> **무엇을 주나.** Ta-LLZO · 25 °C · 2.5 MPa · 6.1 mAh cm⁻²: 900 °C 확산 접합 맨 Cu 는 섬 모양 Li · ±17.5 µm · Cu 파손 · 0.25 mA cm⁻² 단락 / Au · Ag 100 nm + 얹기만 한 Cu 는 ±3.5 µm · 단락 없음 · Au 는 Li₁₅Au₄ 입자 (CC|Li 계면 줄) · Ag 는 녹음 · 결정립 40.8 ± 8.9 → 37.8 ± 26.0 · 33.6 ± 18.7 µm (분포 확대 · 계면과 나란한 경계).
> **★ DEM 쪽에 닿는 곳.** ① CC|SE 분리 기준 (접합 대 얹기) 이 도금 형태를 가른다 (정성 · 값 없음) · ② 석출 Li 다결정의 차수 (≈10–90 µm · 기둥형 대 섞임) · ③ 얇은 합금 층은 첫 도금 뒤 SE 에서 떠난다 → '인터레이어|SE 접촉' 은 핵생성 단계 입력이고 운전 중 계면은 Li(M)|SE.
> **⛔ 인용 금지 / 한정어.** LLZO 수치를 LPSCl 로 옮기지 않는다 · 조건당 n = 1 · 접합 유무 · 전류 교락 · '결정립 감소' 대신 '분포 확대' · 젖음 · 점착 측정이 아니다 · 대조 표적이지 보정 표적이 아니다.
```

## (c) `pdf_map.tsv`

**필요 없어요.** `--inbox --only haslam2025` 가 본문 · SI 를 제목 55 % 로 자동 짝지었어요.

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

발견 검색은 Crossref REST (api.crossref.org) 로만 했어요 — 제목 없이 주제어 + 2025 이후로 8 번, 저자 (Haslam · Sakamoto) 로 2 번, 확인 조회 11 번이에요. 출판사 페이지 · 본문은 안 열었어요. '목록' = `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md`.

| # | 논문 | 왜 (우리에게) | litdb | 목록 | 서지 확인 |
|---|---|---|---|---|---|
| 1 | Chatterjee, Ayyaswamy, Vishnugopi, Yoon, Siegel, **Jeff Sakamoto**, Mukherjee · *ACS Energy Lett.* 11, 7406–7414 (2026) — "Understanding the Role of Lithium Metal Microstructure in Chemo-Mechanical Instability of Solid-State Batteries" · DOI 10.1021/acsenergylett.6c02372 · 🏷 | 이 논문의 전제 ('작은 결정립이 박리에 좋다') 를 이론으로 따지는 편 — 결정립 크기 ↔ 화학-기계 불안정 | 없음 | 없음 | Crossref 확인 (제목 · 저자 7 · 권 · 쪽) · 내용은 제목뿐 |
| 2 | Roman, Ravello, Poole, Haslam, Lee K., Jangid, **Jeff Sakamoto**, Dasgupta · *Matter* 9, 102949 (2026) — "Operando visualization of void formation and recovery at lithium-solid electrolyte interfaces" · DOI 10.1016/j.matt.2026.102949 · 🏷 | 이 논문이 안 한 **박리** 쪽 — 공극 생성 · 회복 operando. 보고서 8-1 '공극을 막는다' 의 실험 짝 | 없음 | 없음 | Crossref 확인 · SE 계는 미확인 |
| 3 | Li Z., Wu, Ji, Claus, Zhong, Ghose, Hatzell · *ACS Energy Lett.* 11, 1705–1713 (2026) — "Texture Evolution of Plated Lithium in Anode-Free Solid-State Batteries" · DOI 10.1021/acsenergylett.5c03205 | 석출 Li 의 결 (texture) — 보고서 7-1 에서 Li 슬랩 면 (Li(100) · Li(110)) 을 고를 근거. 이 논문은 방위 분포를 정량하지 않았어요 | 없음 | 없음 | Crossref 확인 · SE 계 · 방법은 미확인 |
| 4 | Becker J., Weintraut, Benz, Fuchs, Lerch, Becker P., Eckhardt, Henß, Richter, Janek · *Nat. Commun.* 16, 5395 (2025) — "Purity of lithium metal electrode and its impact on lithium stripping in solid-state batteries" · DOI 10.1038/s41467-025-61006-7 | Li 조성 (불순물) 이 박리를 바꾼다 — 'Ag 가 녹은 Li 는 다른 금속' 의 박리 쪽 | 없음 | 없음 | Crossref 확인 |
| 5 | Becker J., Fuchs, Ortmann, Kremer, Richter, Janek · *Adv. Energy Mater.* 15, 2404975 (2025 · 온라인 2024-12-15) — "Microstructure of Lithium Metal Electrodeposited at the Steel\|Li₆PS₅Cl Interface in "Anode-Free" Solid-State Batteries" · DOI 10.1002/aenm.202404975 | **LPSCl** 쪽 석출 Li 미세구조 (같은 cryo-EBSD 법) — 이 논문 결과를 우리 계로 옮길 때 가장 가까운 짝 (ref 15) | 없음 | 없음 | Crossref 확인 + 이 논문 참고문헌 |
| 6 | Thomas, Behara, Van der Ven · *Chem. Mater.* 36, 8936–8948 (2024) — "Thermodynamic and Kinetic Properties of the Lithium–Silver System" · DOI 10.1021/acs.chemmater.4c01903 | Li–Ag 상 · 이동 계산 — 7 절 ③ (Ag 합금 구동력 · 고용) 의 계산 앵커 · `Fig. S1` 평탄 해석의 출처 (ref 27) | 없음 (lu2026 · 이 digest 에 인용만) | **목록에 있음** ('그 밖' ≤ 2024) | 참고문헌 + Crossref DOI (Crossref 레코드엔 권 · 쪽이 없어서 권 · 쪽은 참고문헌 기준) |
| 7 | Fuchs, Ortmann, Becker, Haslam … Nazar, **Jeff Sakamoto**, Janek · *Nat. Mater.* 23, 1678–1685 (2024) · DOI 10.1038/s41563-024-02006-8 · 🏷 | 이 논문의 EBSD 법 · 맨 Cu 기둥형 기준 (ref 16 · SI ref 2) | 없음 | **목록에 있음** (표 2 #8) | 목록에서 Crossref 확인됨 |
| 8 | Sandoval … McDowell · *Joule* 7, 2054 (2023) — "Structural and electrochemical evolution of alloy interfacial layers in anode-free solid-state batteries" · DOI 10.1016/j.joule.2023.07.022 | 같은 Au/Ag 층의 **황화물** 판 (ref 11) — LLZO → LPSCl 로 옮길 때 짝 | 없음 | **목록에 있음** (표 2 #6) | 목록에서 Crossref 확인됨 |

그다음 후보 (짧게): Singh … Janek *Adv. Funct. Mater.* 33, 2211067 (2023 · 온라인 2022 · ref 14 · Li 미세구조 제어 · Crossref 확인 · 목록 없음) · Yoon, Sulaimon, Siegel *J. Mater. Chem. A* 11, 23288 (2023 · ref 19 · ≈1 µm 권고 · Crossref 에선 chemRxiv 판만 나와 저널 DOI 미확인 · 목록 없음) · Haslam & Sakamoto *J. Electrochem. Soc.* 170, 040524 (2023 · ref 25 · 목록에 있음) · Lee J. H. … Yu S.-H. *Energy Storage Mater.* 69, 103398 (2024 · In 도핑 Ag 막 · ref 28 · 참고문헌만 · DOI 미확인 · 목록 없음).
같은 배치에서 병렬로 도는 짝: #2 `chu2026_…` (이 논문을 ref 48 로 인용) · #3 `becker2026_…` (같은 EBSD 팀 · 사이클).

## (e) DEM-DFT 보고서에 쓸 거리 (W_ad 보고서 7 절 · 8 절)

⛔ 전부 **가넷 LLZO · 2.5 MPa · 25 °C · 셀 하나씩** 이에요. 값은 차수 · 순서로만 쓰고 우리 W 값과 같은 표에 놓지 않아요. "봤다" = 이번에 그 그림을 직접 보고 읽었다는 뜻이에요. 상세는 digest §7 · §11.

**1. 무엇을 · 어떻게 (층 · SE · 압력 · 온도 · 전류)**
- Au ≈100 nm (SPI 스퍼터 코터 20 mA · 5 min · '추정') · Ag 100 nm (RF 스퍼터 · '목표') 를 연마 Ta-LLZO (Li₆.₅La₃Ta₀.₅Zr₁.₅O₁₂ · 2–2.8 mm) 위에 · 그 위에 Cu 10 µm 박을 **얹기만** · 대조는 Cu 를 900 °C · 3.15 MPa · 5 min **확산 접합** — SI p. 2.
- 세 셀 모두 400 °C 열처리 · Li 박 상대극 170 °C 15–20 h 컨디셔닝 — SI p. 2.
- 25 °C · 2.5 MPa · 0.01 / 0.10 / 0.25 mA cm⁻² · 6.1 mAh cm⁻² (≈30 µm · 우리 산수 29.6 µm) · 2 전극 — SI p. 3 · p. 2286.
- ⚠ **SE 는 산화물 (LLZO) 이에요. 황화물이 아니에요.** 황화물 판은 Sandoval 2023 *Joule* 이에요 (litdb 없음 · (d) #8).

**2. 층마다 순서 (Cu · Au · Ag)**
- **젖음 · 점착 — 재지 않았어요.** 접촉각 · 흡착 · 박리 시험이 하나도 없어요. 이 논문을 Ag 젖음 · 점착 실측으로 인용하면 안 돼요. 점착 이야기는 CC 를 접합했는지에서 추론한 것뿐이에요 (p. 2288).
  - 대신 처음 막 모양이 달라요 — Au 는 떨어진 입자 미로, Ag 는 연속막 + 핀홀 (SI p. 7 · `Fig. S4` 봤다). 다만 증착법 (DC 코터 대 RF) · 열이력 (400 °C 전후인지 미기재) 이 달라서 W(금속|SE) 순서로 읽지 않아요.
- **핵생성 과전압**: Cu 골 있음 (figure-read ≈5 mV @ 0.10 · ≈25–30 mV @ 0.25) > Au ≈ Ag 골 없음. 숫자는 본문에 없어요 — p. 2286–2287 · `Fig. 1d–f` (봤다).
- **합금 평탄**: Au ≈0.2 · 0.1 V (0.10 · 본문) > Ag ≈0.08 · 0.054 · 0.008 V (0.01 · figure-read). Ag 는 0.10 · 0.25 에서 평탄이 없어요 (저자: 합금이 느리다) — p. 2287 · `Fig. 1e,f` · `Fig. S1` (봤다).
  - ⚠ 0.25 에서는 셀 분극만으로도 Ag 평탄이 0 V 아래로 숨어요 (digest §10-④).
- **Li 형태**: 접합 Cu 는 섬 모양 · ±17.5 µm · Cu 파손 · 0.25 에서 ≈0.4 mAh cm⁻² 단락 ≪ Au ≈ Ag 는 ±3.5 µm · 0.10 = 0.25 · 단락 없음 — p. 2287–2288 · `Fig. 2` · `Fig. S2` (봤다). 위스커 얘기는 없어요.
- **결정립 (EBSD)**: 폭 40.8 ± 8.9 (Cu · 기둥형) · 37.8 ± 26.0 (Au) · 33.6 ± 18.7 µm (Ag) · 정규화 높이 figure-read ≈89 · 73 · 73 % — p. 2289 · `Fig. 3a–d` · `Fig. S5` · `Fig. S6` (봤다).
  - ⚠ 평균 차는 1 SD 안이에요 (우리 산수 t ≈0.4 · 1.3).
  - ⚠ `Fig. 3d` 가로축이 ≈70 µm 에서 잘려 ≈81 µm Au 결정립 (`Fig. 3b` · 픽셀) 이 안 보여요. Au 0.10 (`Fig. S6b`) 에는 ≈77 µm 결정립이 있어요.
  - ⇒ '작아졌다' 가 아니라 **'분포가 넓어졌다'** 로 써요.

**3. 합금 상이 남나 · 어디 남나 → 보고서 7 절 ③ · 8-3**
- **Au → Li₁₅Au₄ 입자로 남아요** (Kikuchi · 전압이 가리키는 Li₃Au 가 아님). 확인된 자리는 **Cu|Li 계면을 따라 한 줄 + 계면 아래 ≈3–5 µm Li 속** (figure-read · 입자 ≈1–2 µm) — p. 2289 · `Fig. 3e` · `Fig. 2f` (봤다).
- **Ag → 6.1 mAh cm⁻² 뒤에는 따로 된 상이 없어요** (SEM · EBSD) — p. 2288–2289 · `Fig. 2i` (봤다).
  - 0.5 mAh cm⁻² (그림 제목 "~5 at% Ag in Li" · 우리 산수 ≈5.0 at% 로 같음) 에서는 Ag 풍부 렌즈 덩어리가 **Cu 쪽에 매달려** 있어요 (EDS) — `Fig. S3` (봤다).
  - 다 녹는 데 드는 Li 를 본문은 "> 6 µm (1 at% 가정)" 라 했는데, 우리 산수는 ≈12.5 µm 예요 (결론은 그대로).
- **7 절 ③ 에 붙일 점**: 같은 '합금하는 금속' 인데 Au 는 금속간 입자로 남고 Ag 는 고용체로 사라졌어요. 그래서 ③ 을 둘로 나누자고 제안해요.
  - (a) 합금 생성: 볼록 껍질 전압 · Au > Ag 순서가 대조 표적
  - (b) 고용: bcc Li 속 묽은 Au · Ag 고용 에너지 대 Li₁₅Au₄ · Li-풍부 Li–Ag 상 · 'Au 불용 · Ag 가용' 이 대조 표적
  - 둘 다 SE 와 무관한 금속 계산이에요.
- **8-3 에 붙일 점**: 얇은 금속막을 SE 위에 두면 합금 자리가 **CC 쪽** 이에요 (Li 가 SE 쪽에서 자람). 그래서 도금 뒤 SE 와 맞닿는 것은 Li (Ag 셀은 Ag 가 녹은 Li) 예요.
  - W(Ag|SE) · W(Au|SE) 는 첫 핵생성까지만 의미가 있고, 이후 계면 후보는 Li(M)|SE · Li₁₅Au₄|Li · Li₁₅Au₄|Cu 예요.
  - Ag/C 층 (metzler2026 · Li 가 Cu 와 탄소 사이) 과 Li 자리가 **반대** 예요.
  - ⚠ 이 배치는 그림에서 읽은 우리 해석이에요 (저자는 따로 논하지 않음). `Fig. 2f` 바닥 (Li|LLZO 쪽) 의 밝은 줄무늬는 판정 못 했어요.
- **8-1 에 붙일 점**: '어디가 붙어야 하나' 가 계면마다 달라요 — Li|SE 는 세야 (박리 공극), CC|SE 는 약해야 (도금 옆 성장 · 이 논문 · Kazyak 2022). W 표에 '바라는 방향' 칸을 두자고 제안해요 (digest §12-①).

**4. 우리 계산이 이 순서를 맞출 수 있나 (대조 표적 · 보정 표적 아님)**
- **맞춰 볼 수 있는 것** (SE 와 무관한 금속 쪽이라 LLZO 실험과 견줘도 계 차이 문제가 없어요)
  - 합금 전위 순서 Au > Ag (볼록 껍질 평균 전압 · 분극이 섞인 값이라 절대값은 안 맞춤)
  - 끝 상태 Au 불용 → Li₁₅Au₄ · Ag 가용 (고용 에너지)
- **이진 수준으로만 견줄 것**: 핵 골 유무 Cu > Au ≈ Ag. 7 절 ① · ② (흡착 · W → 젖음각) 의 Cu(111) 대 Au(111) · Ag(111) 순위로 견줄 수 있어요. 다만 Au · Ag 의 '골 없음' 은 합금 (③) 때문이라, ① · ② 만으로는 Au 와 Ag 를 가르지 못할 수 있어요.
- **맞추지 않을 것**: 높낮이 · 결정립 · 단락 전류 · 평탄 전압 절대값. 계산 범위 밖 (DEM · 연속체) 이고, **LLZO 값이라 LPSCl 로 옮기지 않아요**.
  - LPSCl 은 Li 전위에서 환원돼요 (우리 환원 가장자리 1.717 V). 같은 층이라도 첫 충전에 SE 환원이 끼어들어요.

## (f) 그림 크롭 요약

- `extract_figures.py --slug … --pdf <본문> <SI> --clean` → **9 장** (본문 Fig. 1–3 · SI Fig. S1–S6 · 표 0). `missing_labels` 는 [] 이고 '번호 공백 · 놓친 캡션 후보' 절도 안 떴어요. 오탐 · 손 크롭 없음. `--audit` 경고 없음. 동영상 없음.
- **9 장 전부 직접 봤어요.** 숫자를 읽은 8 곳은 키워서 다시 봤어요 (1d · 1e · 2c,f,i · 3d 3 배 · 3e · S3 · S6b). `Fig. 3b` 결정립 폭 · 3D 패널 넓이는 픽셀로 쟀어요. 안 본 그림은 없어요.
- **본문 서술과 어긋난 것** (digest §10)
  - `Fig. 3d` — 가로축 ≈70 µm 에서 잘림. 큰 Au 결정립이 그림 밖이고, 보이는 Au 점 평균 ≈28 µm 대 본문 37.8 µm 예요.
  - `Fig. S6b` — Au 0.10 이 거의 기둥형이고 ≈77 µm 결정립이 있어요. 본문 '두 전류 모두 작고 덜 기둥형' 과 잘 안 맞아요.
  - `Fig. 2b,e,h` · `Fig. S2` — 3D 영역이 스케일바로 ≈0.017 cm² 예요 (본문 0.16 cm²).
  - p. 2289 — "Figure 1e" 는 `Fig. 3e` 를 말하는 거예요.
  - S5 · S6 — 본문 설명과 SI 캡션이 뒤바뀌어 있어요. `Fig. S6` 캡션의 점선 상자는 그림에 없어요.
  - `Fig. 1e` — Au 두 셀의 합금 전하가 ≈2 배 달라요 (논문 언급 없음).
  - `Fig. 1g` — 0.25 분극이 ≈ −0.085 → ≈ −0.145 V 로 자라요 (언급 없음).
  - `Fig. 2f,i` — 단면 겉보기 Li 두께 ≈40 µm 가 공칭 30 µm 와 안 맞아요 (기울기 보정 미기재).
- 임시 파일은 전부 scratchpad `haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free/` 아래에만 썼어요 (PDF 글자 · 확대 그림 · Crossref 응답 · 점검 로그). 공용 이름은 안 썼어요.

## (g) Jeff Sakamoto 저자 여부

**예 — 교신저자예요** (UC Santa Barbara 재료과 + MUSIC DOE EFRC · `sakamoto@ucsb.edu` · 본문 p. 2290 · SI p. 1). digest 저자 줄에 'Jeff Sakamoto' 로 적었고 웹앱 배지가 붙는 것을 확인했어요 (`_paper_pis` = `['sakamoto']`). (a) 행 둘째 칸 맨 앞에 `🏷 **Jeff Sakamoto 공저** · ` 를 달았어요. 공동 1저자는 Catherine G. Haslam · Till Fuchs 예요.

# 끝 보고 — chu2026_solubility_guided_interlayer_li_plating_stripping_garnet (2026-11-24 · litdb-curator · 배치 2026-11-24b #2)

쓴 파일은 셋이다.
- digest `litdb/papers/chu2026_solubility_guided_interlayer_li_plating_stripping_garnet.md` (≈660 줄 · 표 21 개 · 칸 수 어긋난 줄 0 — 스크립트로 확인)
- 그림 `litdb/figures/chu2026_solubility_guided_interlayer_li_plating_stripping_garnet/` (크롭 44장 + figures.json + 영상 프레임 jpg 52장 `video_frames/`)
- 이 보고 파일

`litdb/figures/_sources.json` 은 추출 도구가 다시 썼다 (손 안 댐 · baer2026 항목과 chu2026 항목이 둘 다 남아 있는 것 확인). 공유 파일 · git 은 안 건드렸다.

## ⚠ 메인이 먼저 알아야 할 것 (셋)

1. **받은 영상 5편은 전부 도금 영상이다 — 박리 영상이 하나도 없다.** 'bN = Video S(N−1)' 가정이 틀렸다. 끝 장면을 `Fig. 6c` 와 맞대고 SEM 데이터바 파일 이름을 읽어 보니 **b7 = S3 (Ag 0.1) · b10 = S6 (Ag 0.5) · b11 = S7 (Cu 1) · b12 = S8 (Au 1) · b13 = S9 (Ag 1)** 이다 (bN = S(N−4)). RSC 가 파일을 글자 순 (S1 · S10 · S11 · S12 · S2 … S9) 으로 매겼다고 보면 다 맞는다 → **b3 = S10 (Cu 박리) · b4 = S11 (Au 박리) · b5 = S12 (Ag 박리)** (가설 · 다른 가능성은 b2–b4 = S10–S12). 어느 쪽이든 **Ag 박리 영상은 안 받은 b4 또는 b5** 다. 사용자가 'Ag 0.1 도금' 이라 여기고 빼기로 한 b4 가 실제로는 박리 영상일 수 있다. 확인법: b3 첫 장면이 Cu 원판에 이미 위스커가 올라온 상태면 글자 순 가설이 맞다.
2. **Ag 박리 공극은 'W ≥ 2γ_Li' 의 반례가 아니다.** 이 논문 자신의 접촉각 → W (γ 0.4 J m⁻²) 가 Cu 0.22 · Au 0.42 · Ag 0.52 J m⁻² 라 **W/2γ_Li 0.28 · 0.53 · 0.65 — 셋 다 문턱 아래**다 (카드 산술). 목록 요약의 '반박하는 자료' 는 '문턱 아래에서는 W 가 클수록 박리가 나아지지 않는다는 예 · 기전은 점착이 아니라 합금 층 Li 저장 · 확산' 으로 고쳐 읽는다.
3. **이 논문의 정량 근거가 약하다** — CA '핵 밀도' 10¹⁶–10¹⁷ cm⁻² 는 금속 표면 원자 밀도의 6–270 배 (핵 밀도일 수 없다) · LSV 흡수량 0.258 / 0.399 µAh cm⁻² 는 자기 그림 면적 · GITT 와 두 자릿수 어긋나고 GITT 로는 Au ≈ Ag · 유일한 박리 직접 영상 (`Fig. S18`) 에서 Ag 가 CE 72 % 로 가장 좋다. 보고서에는 방향만 가져온다.

확인한 것
- 웹앱: `paper_figure_notes` 가 39 개 키 (f1–f9 · fS1–fS28 · tS1 · tS2) 전부에 붙는다 · 이어지는 쪽 5장 (fS23cont · fS25cont · tS1cont1 · tS1cont2 · tS2cont) 은 주석 없이 그림 목록에만 뜬다 (의도) · `_paper_pis` = `[]` (Sakamoto 배지 없음 — 처음 쓴 저자 줄의 '저자가 아니다' 문장이 배지를 걸어서 고쳤다) · 원소 Ag · Au · Pt · Pd · Cu 페이지에 이 논문이 걸린다.
- `pytest webapp/tests/test_v3_literature.py` → 20 passed.
- `build_index.py --check` → 이 slug 는 '어느 인덱스에도 없음 [dft]' 와 'comparison_vs_ours.md 미편입' 두 곳에만 뜬다 (rc 1 · baer2026 도 같은 두 곳). 아래 (a) · (b) 를 넣으면 풀린다.
- `extract_figures --audit` → 이 slug 경고 없음 (본문 9 · SI 30 · 표 5 · 번호 구멍 없음 · `missing_labels` 빈 목록). `--inbox --only chu2026` → 본문 · SI 가 제목 77 % 로 자동 짝지어진다.
- talk 인입 대기열 (`litdb/talks/*`) 에 이 논문은 없다 — 역링크 필요 없음.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어` (build_index 분류 [dft] → INDEX.md). 행 순서상 **fuchs2023 (무음극 핵생성 · 성장) 다음 · metzler2025/2026 (Ag/C 인터레이어) 앞** — '금속 인터레이어 비교' 자리다. 머리말의 '18 편' 숫자와 batch 출처 (`batch_2026_11_24b/batch.json`) 는 메인이 고친다. 행에 `⚠ LLZO 계` 표지를 달았다.

```
| `papers/chu2026_solubility_guided_interlayer_li_plating_stripping_garnet.md` **(본문 21 pp + SI 79 pp 전부 · 크롭 44장 (그림 39 + 표 5 · 손 크롭 5 · 재크롭 6) · 그림 39장 전부 봄 (22 원해상도 · 17 접촉 시트) · 영상 5편 프레임 52장 · 2026-11-24)** | **[외부·exp 주 + DFT · MLIP-MD 보조·⭐⭐⭐ 금속 인터레이어 '친Li 성 화산형' — 도금은 친Li 성이, 박리는 머금은 Li 가 정한다 · ⚠ LLZO 계 (SEI 없음 · LPSCl 로 수치 이식 금지) · ⛔ 접촉각 W ≠ 우리 DFT W]** ✅ **Hyunwon Chu**/C. Lerch/S. Chong/L. Schulz/**Till Fuchs**/K. J. Kim/M. Balaish/H. L. Tuller/**Jürgen Janek**/**Jennifer L. M. Rupp\*** (MIT · TUM · JLU Giessen · EPFL/Oxford), "**Solubility-guided interlayer design toward balanced lithium metal plating and stripping in garnet solid-state batteries**" — ***Energy Environ. Sci.* 19, 5836–5856 (2026)**, DOI `10.1039/D6EE03852B` (OA). Ta-LLZO 양면 스퍼터 50 nm M · Li 200 °C 무압 부착 · 0.283 cm² · 0.520 MPa · 25 °C: CCD **Cu 0.26 · Au 1.13 · Ag 0.65 · Pt 1.16 · Pd 0.65 mA cm⁻²** (2차 셀 0.11 · 0.77 · 0.38 · 0.83 · 0.53 · 금속당 n = 2) · 친Li 순위 = M 의 Li(rt) 속 최대 고용도 (Ag 9 · Au 0.7 (그림 0.9) · Pt 0.4 · Cu 0 at% · 18 금속 4 등급 · '중간' = 0.1–2 at%) · 녹은 Li 접촉각 116 · 87 · 72 · 89° → W = γ(1+cosθ) 0.22 · 0.42 · 0.52 J m⁻² (**W/2γ_Li 0.28–0.65 · 셋 다 문턱 아래 · 카드 산술**) · Cu = 역방향 (CE 박리) 분극 · 박리 쪽 ≤ 25 µm 공극 · 핵 과전압 57 / 9 / 0 mV · Ag = 정방향 (WE 박리) 분극 DC 278 → 525 Ω cm² · 박리 쪽 서브 µm 공극 띠 (파괴 셀) · 저자 기전 = Ag 의 큰 Li 저장 + 느린 Li 확산 (GITT 겉보기 D ≈10⁻¹⁵ 대 Au ≈10⁻¹⁴ cm² s⁻¹ · PET-MAD MD 100 ps). ⚠ **CA '핵 밀도' 10¹⁶–10¹⁷ cm⁻² 는 표면 원자 밀도 초과 (카드 산술 — 핵 밀도 아님)** · **LSV 흡수량 0.258 / 0.399 µAh cm⁻² 는 자기 그림 면적 (≈4×10¹) · GITT (Au ≈ Ag) 와 두 자릿수 어긋남** · **operando 박리 CE 는 Ag 72 % 로 최고** (Cu 7 · Au 30) · MLIP DFT 대조 0 · 공개 영상 bN = Video S(N−4) (받은 5편 전부 도금) | **금속 인터레이어 친Li 성 — 도금 (핵생성) 과 박리 (Li 저장 · 확산) 를 가른다 (W_ad 보고서 8-1 '필요조건일 뿐' 의 실험 사례 · §7 ③ 고용도 축 · 8-2 MLIP · 흡착 경고)** (exp + 계산, 외부 · LLZO) |
```

## (b) `comparison_vs_ours.md` 에 넣을 줄

물성 4축 (A–D) 에는 **넣을 것이 없다** (LLZO σ 만 있고 우리 계가 아니다). **§E** 한 행 + Reference key 한 행 + **§J 방법 카드 하나** (검증 없는 MLIP · S–H N₀ · 엔트로피 대리 · 흡착 순위 — 방법 반례) 를 제안한다. 번호는 메인이 매긴다 (J-91 다음).

§E 행:
```
| **🆕 (2026-11-24b) 금속 인터레이어의 '친Li 성' 은 도금과 박리에서 반대로 작용한다 — Ta-LLZO 대칭 셀 CCD Cu 0.26 · Au 1.13 · Ag 0.65 · Pt 1.16 mA cm⁻² (화산형 · 금속당 n = 2) · Ag 는 박리 (WE) 쪽 분극 · 서브 µm 공극 띠 · 접촉각 W/2γ_Li 0.28–0.65 (셋 다 문턱 아래 · 카드 산술)** | **[Chu26Sol]** `Fig. 3a` · `Fig. 7` · `Fig. S4` · SI p.16 (LLZO · 0.520 MPa · 25 °C) | Li\|SE · Li\|금속 계면 계산은 W_ad 보고서 §7 · §8-1 (값은 보고서 §2 · `db/properties/adhesion.json` — 여기 옮기지 않는다) · LPSCl 은 Li 와 반응 (환원 산물 Li₂S + Li₃P + LiCl) | — 축 다름 (전제 · 기전 대조) · ⛔ CCD · R_int · 흡수량 · N₀ 를 LPSCl 값으로 옮기지 않는다 · 접촉각 W 를 우리 DFT W 와 같은 줄에 두지 않는다 · 'Ag 공극 = W ≥ 2γ 반례' 로 쓰지 않는다 |
```

Reference key 행:
```
| **[Chu26Sol]** ⭐⭐⭐ **금속 인터레이어 친Li 성 화산형 (Cu · Au · Ag · Pt · Pd · Ta-LLZO) — 고용도 지표 · 박리 공극 기전 · PET-MAD MD** · ⛔ **LLZO (SEI 없음) · A–D 물성 4축 진입 금지** (§E 1 행 · §J 방법 카드) | Hyunwon Chu/C. Lerch/S. Chong/L. Schulz/T. Fuchs/K. J. Kim/M. Balaish/H. L. Tuller/J. Janek/J. L. M. Rupp\* (MIT · TUM · JLU Giessen · EPFL) *Energy Environ. Sci.* 19, 5836 (2026) | `papers/chu2026_solubility_guided_interlayer_li_plating_stripping_garnet.md` ✅ | exp + DFT/MLIP 보조 |
```

§J 카드 (번호 메인):
```
### J-xx. 🔧🔴 **방법 반례 — [Chu26Sol] 금속 인터레이어 논문의 계산 · 해석 세 겹: 검증 없는 범용 MLIP 공극 MD · S–H 'N₀' 가 표면 원자 밀도를 넘는다 · 볼츠만 가중을 엔트로피로 읽는다** (2026-11-24 신설)

> 📎 출처: `papers/chu2026_solubility_guided_interlayer_li_plating_stripping_garnet.md` (그림 39/39 · 22 원해상도 · CA 식 재현 · 흡수량 재적분). ⛔ Ta-LLZO · 금속 인터레이어 — A–D 물성 4축에 행을 만들지 않는다. 우리 쪽 상대 = W_ad 보고서 §7 ① ② ③ · §8-1 · §8-2.

| 서술 | 논문 값 | 우리 규율로 다시 읽으면 | 판정 |
|---|---|---|---|
| 'Li–Ag 가 Li–Au 보다 큰 공극' (`Fig. 8b–d` · `Fig. S23`) | PET-MAD · 무작위 FCC Li₀.₅M₀.₅ · 가운데 70 Å Li 순간 제거 · NVT 100 ps · 3 벌 · Zeo++ 탐침 5 Å | MLIP ↔ DFT 대조 0 (Li\|Ag 면 의존 오차 선례 [Lu26LiAg]) · 평형상 아님 · Au 공극은 100 ps 에 아직 증가 (Ag 는 ≈30 ps 포화) · 관측창 (300 K · 100 ps · n 1 ↔ ≈3.7×10²): 기대 사건 1 ≈ 0.18 ↔ 0.33 eV (검출 63 %) · 95 % 검출 ≈ 0.15 ↔ 0.30 eV | 🔴 끝 상태 차이가 아니라 창 안 속도 차이일 수 있다 · 우리 '같은 배치 DFT 확인' 설계의 근거 하나 더 |
| 'Li–Ag 에서 Li 가 느리다' (MSD_z · GITT) | MSD_z @10 ps Ag ≈0.1 · Au ≈0.3 Å² · GITT D Ag 4–7×10⁻¹⁵ · Au 5–8×10⁻¹⁴ cm² s⁻¹ | 홉 수 검산 (D = a²Γ/6 · a 2.9 Å · ν₀ 10¹³ s⁻¹ 가정 · 298 K): Au ↔ Ea ≈0.62 eV · Γ ≈4×10² s⁻¹ · 100 ps 안 N ≈4×10⁻⁸ / Ag ≈0.68 eV · N ≈3×10⁻⁹ → GITT 확산은 MD 창에 안 나온다 · MSD 0.1–0.35 Å² 는 진동 진폭 차수 | 🔴 둘이 '서로 받친다' 는 서술 불성립 (다른 과정) · GITT 상대 비 (≈10 배) 만 |
| CA '핵 밀도' (`Fig. 5b` · `Fig. S16`) | N₀ 1.1×10¹⁶ – 3.7×10¹⁷ cm⁻² · Ag/Cu ≈14 배 | 식 재현 N₀ = 1.81×10⁴ / (t_m I_m)² (cm⁻² · s · A) · (111) 표면 원자 1.4–1.8×10¹⁵ cm⁻² 의 6–270 배 · t_m 까지 전하 = Li 단층 0.4–2 % · t_m 이 금속과 무관 (67.8 / 67.8 · 37.4 / 37.6 / 37.6 ms) · I_m ≈ ΔV / (0.5–3.4 kΩ) | 🔴 핵 밀도 아님 · 순위는 셀 저항 순서와 구별 불가 |
| '엔탈피만 보면 틀린다 → 배치 엔트로피' (`Fig. S5`) | FHI-aims Li 흡착 Au > Cu ≳ Ag (설정 n/a) · PET-OAM-XL 1000 배치 평균 가중 Ag > Au > Cu | 고정 조성의 이상 배치 엔트로피는 셋이 같다 → w 는 배치 에너지 퍼짐 (엔탈피 지형) · 흡착은 화학결합 규모인데 자리 · 배위 미확인 | 🔵 '흡착 순위 ≠ 젖음 순위' 는 보고서 8-2 경고의 사례 · 🔴 '엔트로피가 지배' 는 계산이 아니라 논증 |
| 고용도 지표 (`Fig. 9a` · SI p.17) | Li(rt) 속 M 최대 고용 = 혼합 자유에너지 대리 | 보고서 §7 ③ (합금 · 반응 구동력) 축 · §7 ② (W) 와 다른 양 | ⭕ 계산 없이 얻는 혼합 순위 — W 표에 '고용도' 열을 따로 다는 근거 |

⛔ 인용 금지 — N₀ 를 핵 밀도로 · LSV 흡수량 (0.258 / 0.399 µAh cm⁻² · 그림 면적과 ≈150 배 차) · MD 공극 부피 · MSD 를 속도 · 확산계수로 · 접촉각 W (0.22–0.52 J m⁻²) 를 우리 W 와 같은 줄에.
```

(선택) `comparison_vs_ours_DEM.md` §I 카드 (번호 메인 · I-22 다음):
```
### I-xx. `chu2026_solubility_guided_interlayer_li_plating_stripping_garnet` — (인접 축 · ⚠ LLZO 계) 금속 인터레이어 친Li 성 화산형 — 박리 공극의 꼴 (Cu 국부 ≤ 25 µm · Ag 서브 µm 넓게 흩어짐) · 박리 반주기 중 분극 상승 · 0.520 MPa

> **무엇을 주나.** Ta-LLZO 대칭 셀 (0.520 MPa · 25 °C): CCD Cu 0.26 · Au 1.13 · Ag 0.65 · Pt 1.16 mA cm⁻² · Cu 박리 쪽 국부 공극 ≤ 25 µm (`Fig. S15`) · Ag 박리 쪽 두께 ≈0.3–0.6 µm 공극 띠가 계면 전체 (`Fig. 7c` · `Fig. S20` · figure-read) · Ag 정방향 반주기 중 전압 0.15 → 0.29 V · DC 278 → 525 → 288 Ω cm² (재도금에 회복) · 10 nm Au 는 거칠기 RMS 86 nm 를 못 덮어 CCD 0.35.
> **★ DEM 쪽에 닿는 곳.** ① 계면 공극 분포의 정성 표적 두 꼴 (크고 국부 대 작고 넓게) · ② 공극이 박리 중 자라고 재도금에 닫히는 가역 꼴 — 연속체 공극 모델의 검증 꼴 · ③ 얇은 코팅은 표면 거칠기보다 두꺼워야 한다 (기하 문턱) · ④ 압력 단계: 실험실 셀 아래쪽 끝 (0.52 MPa).
> **⛔ 인용 금지 / 한정어.** LLZO 수치를 LPSCl 로 옮기지 않는다 · 파괴 셀 단면 하나 · 공극 정량 없음 · 금속당 셀 2 개 · 흡수량 · N₀ 숫자 금지 (본문 §10).
```

## (c) `pdf_map.tsv`

**필요 없다.** `--inbox --only chu2026` 가 본문 · SI 를 제목 77 % 로 자동 짝지었다. (mp4 5편은 추출기가 다루지 않는다 — 프레임은 ffmpeg 로 따로 뽑았고 명령은 digest §9b 에 남겼다.)

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

주제어 + 연도로 Crossref 를 먼저 찾았다 (2025-01-01 이후 · 제목 없이 'silver interlayer lithium stripping void' · 'Li-Ag alloy anode stripping void' · 'alloy interlayer garnet vacancy diffusion' 등 8 질의). 서지는 Crossref 메타로 확인했다.

| # | 논문 | 왜 | litdb | 목록 · 서지 |
|---|---|---|---|---|
| 1 | G. Hara, Y. Iwasaki, K. Fukada, X. Song, M. Sakakura, Y. Tsukada … Y. Iriyama · *Small Struct.* 7, e70555 (2026) — "Roles of an Ag Interlayer in Stabilizing the Li Stripping Reactions at the Lithium/Lithium Phosphorus Oxynitride Interface" · DOI 10.1002/sstr.70555 | **Ag 인터레이어가 박리를 '안정' 시킨다** 는 반대 방향 결과 (LiPON 박막) — 이 논문의 'Ag 박리 공극' 과 바로 맞대야 한다 | 없음 | 목록에 없음 · Crossref 확인 (권 · 논문 번호 · 저자) |
| 2 | J. Becker, L. Schuster, S. Kremer, T. Fuchs, J. Janek · *Energy Environ. Sci.* 19, 2367–2383 (2026) — "Microstructure of electrodeposited lithium and its evolution during cycling when using metal interlayers in 'anode-free' solid-state batteries" · DOI 10.1039/D5EE07230A | 같은 Giessen 그룹 · Au · Ag · Bi 층 위 Li 결정립 (EBSD) 이 박리하면 어떻게 바뀌나 — Ag 박리 쪽 미세구조의 직접 자료 | 없음 · **inbox 에 본문 + SI PDF 있음** (`becker2026_li_microstructure_interlayer_*`) | **목록에 있음** (표 1 #3) · Crossref 확인 |
| 3 | E. Roman, M. Ravello, B. Poole, C. Haslam, K. Lee, M. K. Jangid, **Jeff Sakamoto**, N. P. Dasgupta · *Matter* 9, 102949 (2026) — "Operando visualization of void formation and recovery at lithium-solid electrolyte interfaces" · DOI 10.1016/j.matt.2026.102949 · 🏷 Jeff Sakamoto (Crossref 저자 메타) | 박리 공극이 생기고 다시 닫히는 과정을 operando 로 — Ag 셀의 '정방향 악화 · 역방향 회복' 꼴의 일반 근거 · DEM 공극 닫힘 | 없음 | 목록에 없음 · Crossref 확인 |
| 4 | S. Banerjee, B. Vishnugopi, P. Mukherjee · *Adv. Sci.* 13, e15827 (2026 · 온라인 2025-11-23) — "Probing the Impact of Vacancy Diffusion on Void Dynamics at the Lithium Metal–Solid Electrolyte Interface" · DOI 10.1002/advs.202515827 (+ 같은 저자 *Adv. Sci.* e78028 (2026) 단일 공극 동역학) | 공공 확산 → 공극 동역학 모델 — '공공 원천 (Li 저장) + 이동도' 두 항을 연속체로 | 없음 | 목록에 없음 · Crossref 확인 |
| 5 | R. M. McMeeking, M. R. Begley, N. A. Fleck, V. S. Deshpande · *J. Electrochem. Soc.* 172, 100518 (2025) — "Vacancy Diffusion during Stripping of Metal Electrodes" · DOI 10.1149/1945-7111/ae0f5b | 박리 중 공공 확산 이론 — W/2γ_Li 문턱과 Li 이동도 항이 어떻게 맞물리나 (8-1 의 '필요조건' 뒤에 오는 충분조건 쪽) | 없음 | 목록에 없음 (같은 저자군의 Roach 2025 는 목록 #11) · Crossref 확인 |
| 6 | Q. Yin, M. Tang, Q. Liu, Z. Geng, W. Dai, Z. Chen … L. Shen · *Adv. Mater.* 38, e21469 (2026) — "Understanding and Designing Lithiophilic Alloyed Metal Anodes for Practical Metal Batteries" · DOI 10.1002/adma.202521469 | 이 논문 SI ref 68 · 친Li 합금 음극 정의 · 지표 정리 (리뷰) — '친Li 성 = 무엇' 의 최근 정리 | 없음 | 목록에 없음 · Crossref 확인 |
| 7 | Z. Tong, S. Wang, X. Wei, Y. Guo, H. Liang, X. Zhong … · *ACS Energy Lett.* 10, 6207–6214 (2025) — "A Nondeposition Solid-Solution Li Alloy Anode for Solid-State Batteries" · DOI 10.1021/acsenergylett.5c02665 | 고용체 Li 합금 음극의 박리 — '합금 속 Li 저장 · 확산이 박리를 정한다' 를 음극 전체로 | 없음 | 목록에 없음 · Crossref 확인 |
| 8 | C. G. Haslam, T. Fuchs, D. W. Liao, J. Becker, N. P. Dasgupta, J. Janek, **J. Sakamoto** · *ACS Energy Lett.* 10, 2285–2291 (2025) — "The Effect of Alloying Interlayers on Lithium Anode Morphology and Microstructure in 'Anode-Free' Solid-State Batteries" · DOI 10.1021/acsenergylett.5c00149 · 🏷 | 이 논문 ref 48 · 합금 층이 Li 형태를 어떻게 바꾸나 (같은 Fuchs · Janek 축) | 없음 · **inbox 에 본문 + SI PDF 있음** | **목록에 있음** (표 1 #4) |

그다음 후보 (≤ 2024 · 이 논문 참고문헌): Krauskopf 2019 *Adv. Energy Mater.* 9, 1902568 (SI ref 26 · Li–Mg 합금 음극의 확산 한계 — Ag 박리 기전의 가장 가까운 선례 · **목록에 있음**) · Lu Y. 2021 *Sci. Adv.* 7, eabi5520 (본문 ref 26 · 고체 Li 합금 음극에서 Li 원자 → Li 공공으로 운반체 전환 · 목록에 없음) · Siniscalchi 2022 *ACS Energy Lett.* 7, 3593 (ref 46 · 박리 용량을 정하는 Li 벌크 확산 대 계면 형태 · 목록에 없음) · Raj 2022 *Nat. Mater.* 21, 1050 (ref 45 · 인터레이어 셀의 공극 ↔ 덴드라이트 · 목록에 없음) · Ko 2025 *Nat. Commun.* 16, 1066 (**목록에 있음** #8 · inbox 에 PDF · 영상 있음).

## (e) DEM-DFT 보고서에 쓸 거리 — W_ad 보고서 8-1 · 8-2 · 7 절 · DEM

⛔ 전부 **가넷 LLZO 계**다 (SEI 없음 · 우리 LPSCl 은 Li 와 반응). 대칭 셀 0.520 MPa · 25 °C · 금속당 셀 2 개 · operando 는 조건당 1 회. 값은 차수 · 경향으로만 쓴다. "봤다" = 이번에 그 그림을 직접 보고 읽었다는 뜻이다. 상세 표는 digest §11.

**1. 'Li 용해도' 를 친Li 성 지표로 어떻게 정의 · 재나 · 순서 · 우리 지표와 같은 점 · 다른 점**
- 정의: **M 이 실온 Li 상 (Li(rt)) 에 녹는 최대 고용도** — ASM 상평형도에서 읽는다 (계산 · 측정 아님). 고용 한계가 Li 녹는점 181 °C 아래에서 나오면 그 값, 위면 181 °C 값 (SI p.60 · `Fig. 2a` · `Fig. 9a` · `Fig. S2` · `Fig. S25` — 봤다 · S2 · S25 는 접촉 시트).
- 순서 · 값: **Ag 9 at% (≈145 °C) > Au 0.7 at% (155 °C · `Fig. 2a` 라벨은 0.9) > Pt 0.4 (169 °C) > Pd ≈0 (합금은 만듦) ≈ Cu 0** (p.3 · p.12 · SI p.60 · p.67 · `Fig. S28a` — 봤다). 18 금속 4 등급: 강 (Mg 68 · Cd 15 · Ag 9) · 중 (Zn 1.5 · Au 0.7 · Al 0.6 · Sn 0.5 · Bi 0.5 · Pt 0.4) · 약 (Pd · In · Sb · Cu · Si · C) · 소Li (Ni · Fe · Ti).
- 검증: 녹은 Li 접촉각 (200 °C · 50 nm 막 · 5 min · 방울 하나) Cu 116 · Au 87 · Ag 72 · Pt 89° (`Fig. 2b` · `Fig. S4` · `Fig. 9b` — 봤다). 반응 젖음 — 각이 5 min 동안 4–8° 준다 (SI p.13).
- 계산: (i) Young–Dupré W = γ(1+cosθ) · γ 0.4 J m⁻² → 0.22 · 0.42 · 0.52 J m⁻² · f(θ) 0.80 · 0.46 · 0.27 (SI p.15–16) · (ii) FHI-aims Li 원자 흡착은 **Au 가 가장 세서 실험 순위와 반대** (SI p.17–18 · `Fig. S5a` — 봤다 · 설정 전부 미기재) · (iii) PET-OAM-XL 무작위 배치 평균 볼츠만 가중 Ag > Au > Cu (SI p.19–20 · `Fig. S5b,c` — 봤다) → 저자 결론: 고용도가 결합 (엔탈피) 과 배치 유연성 (엔트로피) 을 합쳐 담는다.
- **우리 지표와 같은 점**: 같은 Young–Dupré · '친Li (θ < 90°)' 로 젖음을 판정 · 단일 원자 흡착은 순위를 못 맞춘다 (우리 보고서 8-2 와 같은 결론 · 두 번째 사례).
- **다른 점**: ① 이 논문의 순위 지표 (고용도) 는 우리 §7 ② (W) 가 아니라 **§7 ③ (합금 · 반응 구동력)** 축이다. ② 접촉각 W 는 **녹은 Li · 200 °C · 반응 뒤 (합금) 계면 · 문헌 γ** — 우리 W 는 0 K · 고체 Li · 날카로운 계면 · 같은 방법 γ_Li. 같은 표에 놓지 않는다. ③ 우리 기준 (W/2γ_Li) 으로 그들의 W 를 다시 읽으면 0.28 · 0.53 · 0.65 (Pt 0.51) — **공극 억제 문턱을 넘는 금속이 없다** (카드 산술).

**2. Ag 박리 공극 — 증거 · 기전 · '균형' 기준 · 8-1 에 어떻게 붙나**
- 증거 (강한 것부터):
  - 정방향 (WE 박리) 반주기 중 전압이 ≈0.15 → 0.29 V 로 계속 오름 · DC 278 → 525 → 288 Ω cm² (p.8 · `Fig. 7a` — 봤다).
  - EIS R_int 52.8 → 60.6 Ω cm² · C_int −23 % → 역방향 뒤 회복 (p.9 · `Fig. 7b` · `Fig. S19` — 봤다 · S19 접촉 시트). ⚠ DC 변화 (+247) 가 EIS 합 변화 (+16 Ω cm²) 의 ≈15 배 — 분극 대부분이 휴지 뒤 EIS 에 안 남는다.
  - 파괴 (단락) 셀 단면: 박리 쪽 계면 전체에 두께 `figure-read ≈`0.3–0.6 µm 의 길쭉한 공극 띠 · 도금 쪽은 고른 띠 (p.9 · `Fig. 7c` · `Fig. S20` — 봤다 · 원해상도). Cu 는 국부 공극 ≤ 25 µm (`Fig. S15` — 접촉 시트).
  - Li 흡수량 Ag 0.399 > Au 0.258 µAh cm⁻² (p.10 · `Fig. 8a` — 봤다) — ⚠ 그림 면적을 다시 적분하면 ≈150 배 크고 (Au ≈4×10¹ µAh cm⁻²), GITT 로는 Au ≈ Ag (`Fig. S21c` · `Fig. S22c` — 봤다), 25 nm 핵 과전압 곡선에서는 Ag 가 오히려 적다 (`Fig. 5a`). **정량 근거로 쓰지 않는다.**
  - GITT 겉보기 D Au 5–8×10⁻¹⁴ · Ag 4–7×10⁻¹⁵ cm² s⁻¹ (`Fig. S24` — 봤다 · 저자도 상대 비만 의미) · EIS R_Li Au 23.5 · Ag 94.8 Ω (단 합금 없는 Cu 가 197.9 Ω 으로 최대 — 논증과 어긋남 · `Fig. S13` — 봤다).
  - PET-MAD MD: Ag 큰 · 연결된 공극 · Au 작고 흩어진 공극 · MSD_z Ag < Au (p.11 · `Fig. 8b–d` · `Fig. S23` — 봤다). ⚠ DFT 대조 0 · 비평형 초기 상태 · 100 ps · Au 공극은 아직 증가 중.
  - **반대 증거**: operando 박리 CE **Ag 72 % > Au 30 % > Cu 7 %** (`Fig. S18` — 봤다) · 1500 h 0.25 mA cm⁻² 에서 셋 다 안정 (`Fig. S10` — 접촉 시트).
- 기전 (저자): Ag 가 Li 를 많이 머금는다 (Ag 고용체 ≤ 45 at% Li · Li₉Ag) → 박리 때 합금 속 Li 가 먼저 빠진다 (합금의 높은 산화 전위 [85]) → 공공 다량 → Li–Ag 의 강한 친화가 Li 재분배를 막아 (느린 확산) → 공공이 공극으로 뭉침 → 오래 쌓이면 박리 (p.9 · p.10–11 · SI p.49 · p.58–59). 단 Ag 공극은 Cu 보다 작고 고르게 흩어져 재도금에 회복된다.
- 우리 대안 해석 (논문에 없음): SI p.32 스스로 **Ag 층이 200 °C 부착 때 녹은 Li 속으로 녹아 사라졌을 수 있다** 고 쓴다 (Ag 셀 초기 C_int 최저 · R_int 최고). 그러면 Ag 셀은 '희박 Li–Ag 합금 전극' 이고 (50 nm Ag 가 5 at% 로 퍼지면 ≈1.2 µm · 도금 쪽 띠 두께와 같은 차수 — 카드 산술), 박리 때 계면에 Ag 가 쌓여 Li 이동이 막히는 **Li–Mg 합금 음극 꼴** (Krauskopf 2019 *AEM* · SI ref 26) 이다. 어느 해석이든 **계면 점착이 아니라 합금 쪽 Li 수송 기전**이다.
- '균형' 기준: **'합금은 만들되 Li(rt) 속 고용도가 제한된 (0.1–2 at%) 금속'** (p.13 · SI p.60) — Au · Pt · Al · Zn · Sn · Bi. 화산: Cu 0.26 < Pd 0.65 < Pt 1.16 ≈ Au 1.13 > Ag 0.65 (1차 · 2차 0.11 · 0.53 · 0.83 · 0.77 · 0.38). ⚠ 꼭대기는 두 점 · Pt–Au 차는 반복 차 (Au 1.13 → 0.77) 안 · Pd = Ag (1차).
- **8-1 에 붙이는 법**: 8-1 은 '친Li (θ < 90°)' 와 '공극 억제 (W/2γ_Li ≥ 1)' 를 따로 판정하고 W ≥ 2γ_Li 는 필요조건일 뿐이라 쓴다. 이 논문은 (i) 세 금속 모두 문턱 아래라 판정식과 모순되지 않고, (ii) 문턱 아래에서 W (젖음) 순위가 박리 순위를 못 맞춘다는 실험 예이며, (iii) 박리 공극을 정하는 **다른 기전 — 반응 · 합금 층의 Li 저장량과 그 안의 Li 이동도** — 을 보여 준다. 그래서 8-5 의 판정 두 줄에 **셋째 줄 '반응 · 합금 층이면 Li 저장량 · 이동도를 따로 본다'** 를 더하자고 제안한다. 붙일 문장 (공유 보고서 꼴 · 내부 사정 없음):

  > 친Li 성이 가장 센 Ag 층은 도금을 고르게 했지만 박리에서 공극이 먼저 생겼다 (가넷 LLZO · 대칭 셀 · CCD Ag 0.65 대 Au 1.13 mA/cm²). 이 논문의 녹은 Li 접촉각으로 낸 W 는 Cu · Au · Ag 모두 2γLi 아래였다 (W/2γLi 0.28–0.65) — 그래서 W ≥ 2γLi 의 반례가 아니라, 문턱 아래에서는 W 가 클수록 박리가 나아지지 않는다는 예다. 저자는 그 원인을 계면 점착이 아니라 합금 층에 저장된 Li 와 그 안의 느린 Li 확산으로 본다 (Energy Environ. Sci., 19, 5836 (2026)).

  한정어 (같이 싣는다): 가넷 LLZO · 녹은 Li 접촉각 (200 °C · 반응 젖음) 으로 낸 W · 금속당 셀 두 개 · 박리 공극의 직접 증거는 파괴 셀 단면 하나 · 저자의 흡수량 숫자는 쓰지 않는다.

**3. MLIP · 계산 — 무엇을 어떤 설정으로 · 우리 UMA+D3 · DFT 대조와 견줄 점**
- ⚠ **MACE 는 이 논문에 한 번도 안 나온다** (본문 · SI 0 회). 본문의 MLIP 언급 셋은 'machine-learned interatomic potential' 2 번 (p.11 · p.17 — p.17 에 약어 MLIP) + 참고문헌 87 (PET-MAD) 이다 — 모델은 **PET-MAD** (MD · 본문) 와 **PET-OAM-XL** (배치 통계 · SI · ref 79) 이다.
- PET-MAD + LAMMPS (p.17 · SI p.54–55 · `Fig. 8b–d` · `Fig. S23` — 봤다): FCC 슈퍼셀 ≈50 × 50 × 125 Å · (111)/(110)/(100) 이 z · 자리 절반 무작위 Li (1:1) · CG → NpT 50 ps 475 K → 50 ps 냉각 300 K (Nosé–Hoover τ 100 fs · 바로스탯 1000 fs · 2 fs) → 가운데 70 Å 에서 Li 제거 → NVT 100 ps (온도 미기재) · 무작위 혼합 3 벌 · Zeo++ 탐침 5.0 Å · MSD_z (경계 2.5 Å 안 Li − 벌크 고정 Li).
- PET-OAM-XL (SI p.19–20 · `Fig. S5b,c` — 봤다): Li 200 원자 속 M 5 at% (캡션은 '5 at% Li' — 모순) · 무작위 1000 배치 최적화 · 최저 에너지 기준 평균 볼츠만 가중 (298 · 453 · 473 K).
- FHI-aims DFT (SI p.17–18): Li 원자 하나 흡착 · 설정 전부 미기재.
- **우리와 견줄 점**: ① **MLIP ↔ DFT 같은 배치 대조가 0** — 우리는 작은 모델 · 같은 원자 배치 DFT 단일점 · 허용 차이 사전 설정 (보고서 §3) · Li\|Ag 는 범용 MLIP 이 면마다 다르게 틀린 선례 (arXiv 2602.11430 · 보고서 8-2) 가 있는 바로 그 계다. ② 보고량: 그들은 공극 부피 (탐침 5 Å) · MSD_z (0–10 ps) · 우리는 W_sep (끝점 10 Å · 12 Å 점검). ③ 관측창: 300 K · 100 ps · n 1 ↔ ≈3.7×10² 에서 기대 사건 1 ≈ 0.18 ↔ 0.33 eV (검출 63 %) · 95 % 검출 ≈ 0.15 ↔ 0.30 eV (ν₀ 10¹³ s⁻¹ 가정). ④ 홉 수 검산 (GITT D → 장벽 · a 2.9 Å · ν₀ 10¹³ s⁻¹ 가정 · 298 K): Au ≈0.62 eV · Γ ≈4×10² s⁻¹ · 대기 ≈3 ms · 100 ps 안 N ≈4×10⁻⁸ / Ag ≈0.68 eV · N ≈3×10⁻⁹ — GITT 가 잰 확산은 MD 창에 안 나온다 (MD 의 MSD 0.1–0.35 Å² 는 진동 진폭 차수). ⑤ 초기 상태: 평형상 (B2 LiAg 등) 이 아닌 무작위 FCC · 순간 고갈 — 우리가 Li 계면 MD 를 설계할 때 피할 목록으로 쓴다.

**4. 실험 숫자 — 조건과 같이 (가넷 · LPSCl 로 옮기지 않음)**
| 양 | 값 | 조건 | 근거 |
|---|---|---|---|
| CCD | Cu 0.26 / 0.11 · Au 1.13 / 0.77 · Ag 0.65 / 0.38 · Pt 1.16 / 0.83 · Pd 0.65 / 0.53 mA cm⁻² | Li \| M 50 nm \| Ta-LLZO 700 µm \| M \| Li · 0.283 cm² · 0.520 MPa · 25 °C · 0.05 + 0.03 mA cm⁻² 계단 (반주기 시간 미기재 · 그림으로 ≈1.8 h/계단) | `Fig. 3a` · `Fig. S9` · `Fig. 9c` · `Fig. S26` · `Fig. S28` (봤다) |
| 초기 R_int | Cu 7.78 · Au 4.38 · Ag 17.06 · Pt 1.27 Ω cm² (양면 합) | 첫 사이클 뒤 · 25 °C | p.5 · `Fig. S13` |
| 핵 과전압 | Cu 57 · Au 9 · Ag 0 mV | 아래 M 25 nm · 10 µA cm⁻² | `Fig. 5a` (봤다) |
| operando 핵 밀도 | Cu 1.52 · 1.44 · 0.71 · Ag — · 2.05 · 1.49 ×10⁷ cm⁻² | 100 nm 증착 M · 지름 ≈49 µm 원판 (figure-read) · 0.1 · 0.5 · 1 mA cm⁻² · 0.05 mAh cm⁻² · 무압 · SEM 진공 | `Fig. 6b` · `Fig. S17b` (봤다) |
| CA 핵 밀도 | ⛔ 쓰지 않는다 (10¹⁶–10¹⁷ cm⁻² · 물리적으로 불가능) | — | `Fig. S16` |
| operando 박리 CE | Cu 7 · Au 30 · Ag 72 % | 0.5 mA cm⁻² · 0.05 mAh cm⁻² 도금 → 3 V 까지 박리 | `Fig. S18b` (봤다) |
| 공극 크기 | Cu ≤ 25 µm (국부) · Ag 띠 두께 ≈0.3–0.6 µm (figure-read · 계면 전체) | 파괴 셀 · 액체 N₂ 파단 · 대기 ≤ 30 min | `Fig. S15` · `Fig. S20` |
| 두께 | 인터레이어 49–55 nm · 10 nm Au 는 실패 (CCD 0.35 · R_int > 50 Ω cm²) · 표면 RMS 86 nm | 스퍼터 · 건식 연마 | `Fig. 2b` · `Fig. S8` |
| 압력 · 온도 | 0.520 MPa (스프링) · 25 °C · 부착 200 °C 무압 · 접촉각 200 °C · 장기 RT · 혼성 전지 30 °C | — | p.14–16 |
| 장기 | 0.25 mA cm⁻² · 0.125 mAh cm⁻² · 1500 h — 셋 다 안정 | RT | `Fig. S10` (접촉 시트) |
| 혼성 전지 | 0.2 C (0.37 mA cm⁻²) 200 사이클 94.34 % · CE 99.11 % / 0.125 C 300 사이클 85.18 % · 98.59 % | NMC811 9.08 mg cm⁻² · 양극 쪽 액체 전해질 · Pt · 30 °C · 셀 하나씩 | `Fig. S27` (접촉 시트) |

**5. Till Fuchs 앞 편 (`fuchs2023_cu_llzo_anode_free_li_growth_modes`) 과 어떻게 이어지나**
- **같은 기법 · 같은 사람들**: operando SEM 미세전극 (W 탐침 = WE · 시료대 = Li CE) — 이 논문에서 C. Lerch · T. Fuchs 가 수행 (p.17) · Fuchs 2023 을 ref 71 (= SI ref 121) 로 인용. Fuchs 2023 = 인터레이어 없는 Cu 기준선 → 이 논문 = **Cu · Au · Ag 합금 금속판** 비교.
- **기하**: Fuchs 100 nm Cu 패치 ≈150 µm² (지름 ≈15 µm) · 16 µAh cm⁻² ↔ 이 논문 100 nm Cu · Au · Ag 원판 지름 ≈49 µm (영상 데이터바로 잼) · 50 µAh cm⁻².
- **Cu 핵 밀도 방향이 반대**: Fuchs ≈0.7 → ≈6.1 ×10⁷ cm⁻² (50 → 1000 µA cm⁻² 에 증가) ↔ 이 논문 1.52 · 1.44 · 0.71 ×10⁷ cm⁻² (0.1 → 1 mA cm⁻² 에 감소). 저자는 위스커가 전류를 끌어간다고 해석 (SI p.45) · 세는 시점이 전하 3 배 뒤라 합쳐짐도 섞인다. 차수 (10⁷ cm⁻²) 는 같다.
- **같은 현상**: 얇은 Cu 막을 Li 가 뚫고 위스커로 (Fuchs `400 nm 이하 관통` ↔ 이 논문 영상 b11 · 1 mA cm⁻² 에서 결함점에서 시작한 ≈12–25 µm 위스커 — 봤다).
- **벗기기**: Fuchs Cu CE 13 % (50 µA cm⁻² · 덮임 낮음) ↔ 이 논문 Cu 7 % · Au 30 % · Ag 72 % — '덮임이 낮으면 dead Li' 결론을 금속별로 넓혔다.
- **같은 한계**: 조건당 1 회 · 탐침 근처 편중 가능성 · 빔 전류 미기재 (이 논문은 영상 데이터바에서만 2 kV · InLens · 조리개 30 µm). LLZO (SEI 없음).
- **CCD 절차**: 같은 그룹의 Fuchs 2023b (*Adv. Energy Mater.* 13, 2302383 · ref 30) 가 CCD 의 절차 의존성을 지적했는데, 이 논문은 반주기 시간을 적지 않았다.

## (f) 그림 · 동영상 크롭 요약

**PDF 그림 · 표 (44장)**
- 도구 출력 39 장 (본문 9 · SI 28 + 표 2) · 오탐 제외 4 (SI p.3 목차의 S20 · S23 · S24 캡션 · Table S1 p.9 '중복') · `missing_labels` 빈 목록.
- **손 크롭 5** (manual_crop 사유 기록): 도구가 '이어짐 (Cont'd)' 쪽만 남긴 네 항목의 첫 쪽 — `fig_S23.png` (SI p.56 · 캡션 있는 Au 쪽) · `fig_S25.png` (p.61) · `tab_S1.png` (p.7 · 캡션 포함) · `tab_S1_cont2.png` (p.9) · `tab_S2.png` (p.10 · 캡션 포함). 도구의 크롭은 이름을 바꿔 남겼다: `fig_S23_cont.png` (p.57 · Ag 쪽) · `fig_S25_cont.png` (p.62) · `tab_S1_cont1.png` (p.8) · `tab_S2_cont.png` (p.11). 정본 키 (fS23 · fS25 · tS1 · tS2) 는 첫 쪽을 가리킨다.
- **재크롭 6** (recrop 사유 기록): `fig_S7` · `fig_S8` · `fig_S9` · `fig_S18` · `fig_S20` · `fig_S24` — 그림 위 본문 글 한 줄이 섞여 있어 윗변을 래스터 위 6 pt 로 내렸다.
- 본 것: 그림 39/39 (원해상도 22 · 접촉 시트 17) · 표는 `tab_S1_cont1` 1 장만 이미지로 (나머지 4 장은 PDF 글자 층 · 표 추출로 읽음).
- 그림에서 찾은 본문 어긋남: Au 고용도 `Fig. 2a` 0.9 ↔ 본문 0.7 at% · Ag R_int 라벨 0.59 ↔ 본문 0.57 · Pt C_int 표 증가 ↔ 본문 '감소' · `Fig. 1b` 축 밖 점 넷 · `Fig. S21b` 머리 'Li/Ag' 오기 · GITT 용량축 ↔ 시간축 0.28 배.

**영상 (5편 · 52장 · `video_frames/` — figures.json 밖이라 `--clean` 때 지워진다 · 명령은 digest §9b)**
- 뽑기: `ffmpeg -vf "fps=1/2,showinfo"` (장면 시각 = 출력 시각 0 · 2 · 4 … s) + 끝 장면 `-sseof -0.1 -frames:v 1`. 1920×1080 · 24 fps · 18.1–19.7 s · **오디오 트랙 있음 · 무음** (−91 dB).
- 본 것: 52 장 전부 접촉 시트 (640 px 폭) · 원해상도 b7_001 · b10_end · b11_end · b13_end · 축소 (68 %) b7_end · b12_end · 비교용으로 `Fig. 6c` Cu · Au · Ag 줄 확대.
- 화면에 시간 · 전류 · 전압 표시 없음 · SEM 데이터바 (GeminiSEM 560 · 2.00 kV · InLens · 조리개 30 µm · 1.40 kX (b12 1.34) · 2024-07-17) 와 파일 이름 (`Ag_LLZO_05` · `Ag_LLZO_11` · `Cu_LLZO_01` · `Au_LLZO_12` · `Ag_LLZO_01`) 은 읽힌다.
- **어느 영상인가**: b7 = **S3 (Ag 0.1 도금)** · b10 = **S6 (Ag 0.5)** · b11 = **S7 (Cu 1)** · b12 = **S8 (Au 1)** · b13 = **S9 (Ag 1)** — 끝 장면이 `Fig. 6c` 의 해당 칸과 같다 (물결 선 · 검은 삼각 · 갈고리 위스커 · 세로 긁힘 · 부스러기 같은 특징으로 맞춤). **박리 셋 (b11–b13 으로 가정했던 S10–S12) 은 받지 않았다.**
- **판독 요약**:
  - b7 (Ag 0.1): 끝까지 낱개 핵 없이 매끈 · 고운 결 — `Fig. 6c` · 'Ag 0.1 핵 밀도 —' 와 맞다. 10–16 s 의 화면 전체 어두워짐 · 포화 · 가로 띠는 영상 (대전 · 주사) 변화라, '명암 변화 = 표면 아래 합금' 을 이 영상만으로 가를 수 없다.
  - b10 (Ag 0.5): 4–8 s 에 어두운 점 (≈0.5–1 µm) 이 원판 전체에 고르게 생겨 패인 결로 굳는다 · 위스커 없음 — '고른 결' 과 맞다. ⚠ Ag 의 '핵' 은 어두운 점이고 Cu 의 Li 입자는 밝은 돌출이라 세는 기준이 같았는지 모른다 · SI 의 '≈15 s' 는 시간 표시가 없어 확인 불가.
  - b11 (Cu 1): 처음부터 있던 결함점에서 위스커가 솟아 가운데 ≈25 µm 고리 · 원판 밖 갈고리 (굵기 ≈1–1.4 µm · figure-read) — 'pronounced filament growth' 와 맞다.
  - b12 (Au 1): 고운 결이 전체를 덮고 아래 · 왼쪽 테두리부터 명암이 번진다 · 오른쪽 아래 작은 덩어리 하나 — 'much finer structures' 와 맞다.
  - b13 (Ag 1): 결함 두 곳에서만 위스커 덩어리 (≈5–8 µm) · 나머지는 b10 꼴 패인 결 — 본문 *"only minor whisker signs"* 와 맞고, SI 의 *"whisker growth rapidly dominates"* 는 과장.
  - **요청된 셋과**: Ag 박리 공공 · 공극 뭉침 — **영상으로 판정 불가** (박리 영상 미수령) · Cu dead Li · CE 7 % — 영상으로 확인 불가 (S10 미수령) · `Fig. S18a` 정지 사진으로는 Cu 도금 · 박리 사진이 거의 같다 (dead Li 와 맞다) 는 것을 봤다.
- **받으면 볼 영상 · 왜**: b3 · b4 · b5 (글자 순 가설) 또는 b2 · b3 · b4 (되감기 가설) — **Video S10–S12 (Cu · Au · Ag 박리)**. 특히 **Ag 박리 (S12)** 는 이 논문 오른쪽 비탈 주장 (박리 때 공공 · 공극 뭉침) 의 유일한 operando 장면 후보이고, 같은 실험의 CE 72 % 와 어떻게 함께 가는지 (위에서 보는 열린 표면에 공극이 보이나) 를 판정할 수 있다. 받으면 같은 방식 (2 초 간격 + 끝 장면) 으로 뽑아 digest §9b · 이 보고 (e)-2 · (f) 를 고친다.
- b4 와 Cu · Au 도금 6 개 (합 7 개) 는 받지 않음 (본문 · SI 그림으로 대신).

## (g) Jeff Sakamoto 저자 여부

**아니다.** 저자 10 명 (Chu · Lerch · Chong · Schulz · Fuchs · Kim · Balaish · Tuller · Janek · Rupp) — PDF 첫 쪽 · SI 표지 · Crossref 저자 메타 셋 다 같다. 'Sakamoto' 는 참고문헌에만 나온다: 본문 refs 6 ('J. S. Sakamoto' · Ni 2012) · 11 · 12 (Sharafi 2017 두 편) · 30 (Fuchs 2023b CCD) · 48 (Haslam 2025) · 68 (Sharafi 2016) · 71 (Fuchs 2023) · 75 (Fuchs 2024 EBSD) = 8 곳 · SI refs 7 · 8 · 15 · 19 · 29 · 34 · 44 · 89 · 121 · 151 = 10 곳. INDEX 행에 🏷 를 달지 않는다. digest 저자 줄에는 사카모토 이름을 '저자 아님' 꼴로만 적었다 (처음에 'Jeff Sakamoto 는 저자가 아니다' 로 적었더니 웹앱이 배지를 걸어서 고쳤다 · `_paper_pis` = `[]` 확인). (d) 의 Roman 2026 *Matter* · Haslam 2025 은 Sakamoto 공저다.

# 끝 보고 — seymour2021_void_suppression_interfacial_adhesion_vacancy_transport (배치 2026-11-24 · #1)

- digest: `litdb/papers/seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md` (새 파일 · 533 줄 · 한국어 standalone · §0–§16)
- 그림: `litdb/figures/seymour2021_void_suppression_interfacial_adhesion_vacancy_transport/` — `fig_1`–`fig_6` · `fig_S1`–`fig_S11` · `tab_S1`–`tab_S7` · `figures.json` (24 항목 · 손 크롭 19 개에 `manual_crop` 사유 · `missing_labels` 18/18 `resolved` · 전 항목 `viewed`/`viewed_how` · 도구 캡션은 추출 잔재 (U+0003 → −, 'DEBulk' → 'ΔEBulk', 합자) 만 정리)
- 공유 파일은 안 건드렸다. `litdb/figures/_sources.json` 은 추출 도구가 다시 썼다 (손 안 댐). git 작업 없음.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 "어느 인덱스에도 없음 [dft]" + "comparison_vs_ours 미편입" 으로 뜬다 (아래 (a)·(b) 를 넣으면 풀린다) · 웹앱 `paper_figures` 24 · `paper_figure_notes` 24/24 (Figure set 표 행이 크롭마다 붙는다) · `_paper_pis` = [] (Sakamoto 배지 없음 — 맞다) · elements/methods 태그 줄 2 개뿐 · 시험: `test_v3_literature` 20 통과 · `test_v3_markdown` 23 통과 · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (INDEX · comparison 미편입 — 이 배치 전부 같은 이유 · 합치면 풀린다).

⚠ **메인에 알릴 것**
1. **다른 배치 digest 의 오기 의심** — `lu2026_li_ag_interface_thermodynamics_kinetics.md` 138 행이 이 논문 계면을 *"DFT BCC(111) Li 정합 계면"* 으로 적었다. 원전은 **BCC Li (100)** (+ HCP (0001) · (10-10)). 값 (LiMg 0.08301 · AlSc 0.10242 eV/Å² = 1.330 · 1.641 J m⁻²) 은 `Table S6` 과 맞다. lu2026 논문 본문 표기인지 digest 오기인지 그쪽에서 확인.
2. **Yang 압력 인용 불일치** — 이 논문은 Yang 문턱을 *"W > 0.7 J m⁻² + 10–20 MPa"* 로 인용한다. 같은 배치 `yang2021_atomistic_li_stripping_plating_interface_md` (원전 직접 읽음) 와 기존 `wang2022_…` digest 는 둘 다 **20–30 MPa** 다. digest §3g · §10-⑭ · §14 에 *"압력은 이 논문에서 가져오지 않는다 · Yang digest 에서"* 로 걸었다.
3. **이 논문 자체의 그림–표 불일치** (픽셀 판독): Li₂O 이완 ΔE 표 **0.346** 대 `Fig. 4` · `Fig. S9` **0.396** · `Fig. 5b` Cl top 범례가 표와 뒤바뀜 · 본문 hollow/Li top W 순서 반대 · Na/Li₃OCl 두 점 0.007–0.012 차. 인용 금지 규칙은 digest §14.
4. `extract_figures.py --audit --slug …` 를 한 번 돌렸다가 120 s 제한으로 끊겼다. 그 사이 프록시가 openalex · semanticscholar · crossref 연결을 거절했다는 알림이 떴다 (추출기 코드에는 네트워크 호출이 없어 다른 프로세스였을 수 있다). 파일 변화 없음 (git status 확인). 다시 안 돌렸다.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🧲 계면 점착 · 인터레이어 트랙 — LPSCl 이 한쪽 면인 계면/벌크 역학의 실측 앵커 (2026-09-23 신설)` — **DEM 쪽 트랙** (`INDEX_DEM.md` 는 자동 생성이라 따로 넣지 않는다 · 대조 서술은 `comparison_vs_ours_DEM.md` §I).

그 절 머리의 ⛔ 예외 목록에 한 줄 (giovannetti2008 · wang2015 와 같은 꼴):

> ⛔ 예외 (2026-11-24): `seymour2021` 도 G_c 가 아니라 **DFT(PBE · vdW 없음) 이완 W_ad** 다 — G_c 값과도, 우리 DFT W_sep (고정 기하) 와도 **같은 줄 금지**. 판정식 (W ≥ 2σ_m) · 부호 · 계 간 순서만 이식한다.

행 (3 칸):

| `papers/seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md` **(본문 13 pp + SI 11 pp (두 파일 · 글자 층 없음) · 크롭 24장 (도구 5 + 손 19) 전부 봄 — 13장 원해상도 · 11장 쪽 렌더 + 대조표 · 픽셀 판독 3장)** | **[외부·DFT(VASP-PBE · vdW 없음)·⭐⭐⭐ `W_ad ≥ 2σ_m` (θ = 0°) 공극 억제 판정식의 원전 · ⛔ G_c 실측과 다른 부류 — 0 K 이완 W_ad]** ✅ **Ieuan David Seymour\***/**Ainara Aguadero** (Imperial College London, Materials), "**Suppressing void formation in all-solid-state batteries: the role of interfacial adhesion on alkali metal vacancy transport**" — ***J. Mater. Chem. A* 9, 19901–19913 (2021)**, DOI `10.1039/d1ta03254b` (CC-BY 3.0). 결합 끊기 모형 ΔE_Vm^Bulk–Int = (σ_m − W_ad/2)/ρ → **W_ad ≥ 2σ_m (Young–Dupré θ = 0°) 이면 공공이 계면에 안 모인다** (정합에서 정확 · 비정합에선 하한). 정합 12 계 (Li 8 · Na 4) 검증 ✎ MAD 0.071 eV · 부호 11/12 (γ-Li₃PO₄ 만 틀림) · 기울기 0.97. 통과 = **LiMg · AlSc (✎ W/2σ 1.44–1.81) · Li₃OCl O 종결 (1.14 · Na 1.04)** 뿐 · 미달 = LiCl 0.25 · Li₂O 0.32 · γ-Li₃PO₄ 0.64 · 비정합 **Li₂S 0.40 · Li₃P 0.66** · 비정합 Li/LiCl ≈0.04. σ_m Li BCC (100) **0.463 J m⁻²** (변형셀 0.419–0.472) · registry 로 W 0.199 → 0.003 eV/atom (66×) · 비정합 Li/LiCl 평균 W 0.03 eV/atom 인데 자리 (ii)·(iii) 공공 0.063 · 0.039 eV ≪ 자유면 0.206. NEB 표면→버금층 0.238 (Li) · 0.182 (Na) eV vs 벌크 0.037 · 0.040 (✎ 300 K 대기 1.0 ns · 0.4 ps). **방법**: VASP 5.4.4 · PBE · 가장 무른 PAW (Li · O_s …) · 500 eV · 비스핀 · MP 0.1 eV · Γ 8³ (BCC) / 11×11×5 (HCP) · 진공 ≥15 Å · Li 11 층 · 고정층 없음 · cNEB 3 images · Fiorentini–Methfessel E_bulk. 🔴 그림·표 불일치 3 (Li₂O 이완 ΔE 표 0.346 대 그림 0.396 · `Fig. 5b` Cl top 범례 뒤바뀜 · 본문 W 순서) · strain 정의 (a−a₀)/a (Li₃OCl 13.1 % 를 11.58 % 로) · 참조 오기 5 · Yang 압력 인용 10–20 MPa (원전 쪽 기록 20–30). ⛔ 아르지로다이트 슬랩 0 · Ag · 탄소 0 · 우리 계 값 0 | 점착 트랙 Li 친화성 판정식 원전 (W_ad 보고서 7 절) · γ_Li 는 같은 면·같은 변형·같은 범함수로 · 금속 인터레이어 논거 (Ag 값 없음) |

---

## (b) `comparison_vs_ours.md` 에 넣을 줄

**A–D 물성 4축: 없음 (방법 논문)** — 아르지로다이트 슬랩 0 · 이온전도 0 · 산화창 0 · 탄성 0 · 밴드갭 0.

### b-1. `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Sey21Void]** 🔧 **공극 억제 판정식 `W_ad ≥ 2σ_m` (θ = 0°) 의 원전 — 결합 끊기 모형 + 정합 12 계 DFT** · ⛔ **A–D 4축 진입 금지 (아르지로다이트 슬랩 0)** | Ieuan David Seymour\*/Ainara Aguadero (Imperial) 2021 ***J. Mater. Chem. A* 9, 19901–19913** (DOI 10.1039/d1ta03254b · CC-BY 3.0) — "Suppressing void formation in all-solid-state batteries: the role of interfacial adhesion on alkali metal vacancy transport" | ✅ `papers/seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md` — 판정은 §E 1 행 + §J (방법 원전) | DFT (VASP-PBE 정적 + cNEB · 실험 0) |

### b-2. §E 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-24) 공극 억제 판정식의 원전 — `W_ad ≥ 2σ_m` (θ = 0°) 이어야 계면이 공공을 붙잡지 않는다 · 아르지로다이트 분해산물 Li₂S · Li₃P 도 미달** — ΔE^Bulk–Int = (σ_m − W/2)/ρ (정합에서 정확 · 비정합에선 하한) · 비정합 평균 W: Li₂S 0.361 · Li₃P 0.589 J m⁻² (✎ W/2σ 0.40 · 0.66) · Li/LiCl 0.03 eV/atom | **[Sey21Void]** `Table S6` · `Table S7` · `Fig. 4` · `Fig. 6` (VASP · PBE · vdW 없음 · 가장 무른 PAW · 500 eV · 0 K · 이완 W_ad · registry 1) | 음극 계면 슬랩 0 (`anode_interface_b2o3.json` 산물표뿐) | 🟡 **대조 불가 (우리 값 없음)** + 🔑 [Wang22Res] 행이 쓴 *'Seymour `W>2γ_metal`'* 의 원전 — 순위 LiCl ≪ Li₂S < Li₃P 가 두 논문에서 같다 (정의·셀·변형이 달라 값은 나란히 안 놓는다) · ⛔ 모형 오차 ±0.1 eV 라 W/2σ 0.6–1.1 은 판정 불가 |

### b-3. §J 끝에 블록 (지금 J-87 · 같은 배치 lu2026 이 J-88 을 제안 → **J-89** 제안 · 번호는 메인이 정한다)

### J-89. 🔧 **방법 원전 — [Sey21Void] `W_ad ≥ 2σ_m` (θ = 0°) 공극 억제 판정식: 결합 끊기 모형 ΔE = (σ_m − W/2)/ρ + 정합 12 계 DFT 검증 · 비정합에선 하한** (2026-11-24 신설)

📎 **출처**: `papers/seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md` (그림 24/24 · 13 장 원해상도 · `Fig. 4` · `Fig. 5b` · `Fig. S9` 픽셀 판독)

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** — 계가 Li/Na 금속 × 이온성·금속 기판 (+ 비정합 Li₂S · Li₃P · LiCl) 이고 **아르지로다이트 슬랩 0 · ESW 0 · 탄성 0 · DOS 0**. 판정은 **§E 1 행**. 우리 W 값은 위치만 (`db/properties/adhesion.json` · `db/properties/wad_*`).

| 항목 | [Sey21Void] 가 보이는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| 판정식 | ΔE^Bulk–Int = (σ_m − W_ad/2)/ρ → W ≥ 2σ_m (Young–Dupré θ = 0°) 이면 계면 편석 없음 · 정합에서 정확 · 비정합에선 하한 | W_ad 보고서 7 절이 Young–Dupré 로 같은 문턱을 제안 (Li 슬랩 0) | ✅ **원전 확보** — 7 절 근거로 댄다 |
| 모형 성적 (✎) | 정합 12 계 MAD 0.071 eV · 최대 0.136 · 부호 11/12 (γ-Li₃PO₄ 실패) · 기울기 0.97 | — | ⚠ W/2σ 0.6–1.1 은 판정 불가 구간 |
| 문턱 통과 | LiMg · AlSc (✎ W/2σ 1.44–1.81) · Li₃OCl O 종결 (1.14 · Na 1.04) | — | 🔵 금속 인터레이어 논거 (Ag 값은 없다) |
| 미달 | LiCl 0.25 · Li₂O 0.32 · γ-Li₃PO₄ 0.64 · 비정합 Li₂S 0.40 · Li₃P 0.66 · Li/LiCl ≈0.04 | 음극 계면 슬랩 0 | 🟡 대조 불가 · 서론 문장용 |
| W 정의 | **이완 W_ad** (분리 슬랩 각각 이완) · registry 1 (LiCl 만 3 · 66 배 차) · 고정층 없음 · PBE vdW 없음 · 가장 무른 PAW · 500 eV | 고정 기하 W_sep · registry 평균 · D3(BJ) | ⛔ **같은 표 금지** (정의상 W_sep ≥ W_ad) |
| γ 기준 | 같은 변형을 건 Li 슬랩 σ_m (0.419–0.472 · 무변형 0.463 J m⁻²) | 7 절 "같은 방법 · 같은 Li 면" | 🔑 **"같은 변형 · 같은 D3 · 같은 이완 기준"** 을 더한다 |
| 비정합 | 평균 W 0.03 eV/atom 은 맞는데 자리 (ii)·(iii) 공공 0.063 · 0.039 eV ≪ 자유면 0.206 | registry 평균 + 범위 | 🔑 판정엔 **최약 registry** 도 같이 |

**인용 위생**: Li₂O 이완 ΔE 표 0.346 대 그림 0.396 · `Fig. 5b` Cl top 범례 뒤바뀜 · 본문 hollow/Li top W 순서 반대 · strain 정의 (a − a₀)/a (Li₃OCl 13.1 % 를 11.58 % 로) · 참조 오기 5 · Yang 압력 10–20 MPa (원전 쪽 기록 20–30) · 장벽 0.037–0.444 eV 는 300 K 홉 0.4 ps–2.9 µs (ν₀ 10¹³ s⁻¹ 가정) 라 "공공이 막힌다" 로 쓰지 않는다.

### b-4. (권장 · 점착 트랙의 실제 집) `comparison_vs_ours_DEM.md` §I 에 블록 (lee2022 · lu2026 이 I-11 을 제안 → **I-12** 제안)

### I-12. `seymour2021_void_suppression_interfacial_adhesion_vacancy_transport` — ★★★ (DFT · ⛔ G_c 아님) **Li 친화성 → 공극 억제의 판정식 원전** — W_ad 보고서 7 절의 *"W ≥ 2γ_Li 면 θ = 0°"* 가 왜 2γ 인가

- **무엇**: 결합 끊기 모형으로 계면 층 Li 공공과 금속 속 공공의 에너지 차를 ΔE = (σ_m − W/2)/ρ 로 쓰고, W = 2σ_m (Young–Dupré θ = 0°) 을 공공 편석의 부호 전환점으로 세웠다. 정합 12 계 DFT 로 검증 (✎ MAD 0.071 eV · 부호 11/12).
- **점착 트랙에 주는 것 셋**: ① **친Li (θ < 90°) ≠ 공극 억제 (θ = 0°)** — γ-Li₃PO₄ 74° · Li₃P 71° 는 친Li 인데 공공이 계면에 모인다 ② **γ_Li 는 같은 면 · 같은 변형 · 같은 범함수 · 같은 이완 기준** — 변형만으로 σ_m 이 0.419–0.472 J m⁻² 로 움직여 문턱이 ±6 % 흔들린다 ③ **비정합이면 최약 자리가 판정** — 평균 W 가 맞아도 약한 자리가 자유면보다 공공을 더 잘 잡는다.
- **DEM 쪽 쓰임**: Li 증착 · 공극 모델에 Li–벽 접촉각 입력이 있으면 `Table S6` 의 θ 열이 문헌 앵커다 — 단 **0 K · 고체 · 변형셀로 낸 지표**라 녹은 Li 접촉각과 같은 양이 아니다 (보고서 7 절이 이미 그은 선).
- **금지**: G_c 와 같은 줄 · 우리 W_sep 와 같은 표 · Yang 압력을 이 논문에서 가져오기 · Ag · 탄소 값으로 쓰기 (이 논문에 없다).

---

## (c) `pdf_map.tsv`

**필요 없다** — `extract_figures.py --inbox --only seymour2021` (매칭표만) 이 본문 + SI 두 개를 자동으로 붙였다 (`[제목 50%]`). 50 % 가 문턱 근처라 굳히고 싶으면 한 줄:

```
seymour2021_void_suppression_interfacial_adhesion_vacancy_transport	seymour2021_void_adhesion
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8)

> 같은 배치 (2026-11-24) 에 **이미 digest 가 있는** 이 논문의 참고문헌·후속 (세지 않음): ref 17 Sharafi 2017 (`sharafi2017_…`) · ref 29 Wang–Choudhury–Sakamoto 2019 (`wang2019_li_se_…`) · ref 47 Yang 2021 (`yang2021_atomistic_…`) · 2026 후속 `lu2026_li_ag_interface_thermodynamics_kinetics` (이 논문의 LiMg · AlSc W 를 금속 계면 앵커로 인용).
> ⚠ 2024–2026 의 *이 논문 후속* 은 PDF 로 확인한 게 없다 (litdb 안에서는 lu2026 하나). 아래 서지는 #1 만 빼고 전부 **이 논문 참고문헌 목록**에서 — 그 목록에는 제목이 없어서 제목은 안 적었다. 8 편 모두 `litdb/papers` 파일 이름 대조로 **digest 없음**.

| # | 문헌 | 왜 (축) |
|---|---|---|
| 1 | Seymour, Quérel, Brugge, Pesci, Aguadero, *ChemSusChem* **16**, e202202215 (2023) — *"Understanding and Engineering Interfacial Adhesion in Solid-State Batteries with Metallic Anodes"* (서지·제목 = `kb/papers/adhesion_literature_review.md` #7 기록 · 미검증) | **직계 후속** — Li 금속 \| 기판 점착 · DFT 점착 계산법 · 금속 음극 (가장 최근) |
| 2 | K. Kim, D. J. Siegel, *ACS Appl. Mater. Interfaces* **11**, 39940 (2019) (ref 26) | 젖음 — DFT W 로 접촉각 예측 · Li/Li₃OCl O 종결 0.77 대 Cl 0.09 J m⁻² |
| 3 | N. D. Lepley, N. A. W. Holzwarth, *Phys. Rev. B* **92**, 214201 (2015) (ref 71) | DFT 점착 계산법 — Li 와 Li₂O · Li₂S · Li₃PO₄ · Li₃PS₄ 계면 (내용 = `wang2022_…` digest 기록) · 황화물 쪽 |
| 4 | K. S. Nagy, S. Kazemiabnavi, K. Thornton, D. J. Siegel, *ACS Appl. Mater. Interfaces* **11**, 7954 (2019) (ref 64 · SI ref 1) | γ_Li 기준값 — Li·Na 면별 표면 에너지 (2γ 문턱의 분모) |
| 5 | M. J. Wang, E. Carmona, A. Gupta, P. Albertus, J. Sakamoto, *Nat. Commun.* **11** (2020) (ref 86) | 무음극 · 집전체 위 Li 석출 — Li/SE 대 Li/집전체 공극 (Ag–C 무음극 문맥 · Sakamoto 그룹) |
| 6 | T. Krauskopf, B. Mogwitz, C. Rosenbach, W. G. Zeier, J. Janek, *Adv. Energy Mater.* **9**, 1902568 (2019) (ref 83) | 금속 인터레이어 — Li–Mg 합금이 공극을 막지만 합금 내 확산이 율속 |
| 7 | T. Krauskopf, H. Hartmann, W. G. Zeier, J. Janek, *ACS Appl. Mater. Interfaces* **11**, 14463 (2019) (ref 30) | 방전 중 공극 — 공공 확산 지배 · 50–200 µA cm⁻² 에서도 공극 |
| 8 | J. Gao, X. Guo, Y. Li, Z. Ma, X. Guo, H. Li, Y. Zhu, W. Zhou, *Adv. Theory Simul.* **2**, 1900028 (2019) (ref 65) | DFT · 공극 — 비정합 Li/LLZO 공공 형성 에너지가 자리별 최대 0.55 eV ("평균 W 로는 부족" 의 독립 근거) |

다음 순번 (이 논문 밖 · 2024 후속 계열 · lu2026 digest 가 이미 *"따로 먹여야 한다"* 고 적은 둘): Xie/Ceder *Adv. Energy Mater.* 2024 (Li–Ag 클러스터) · Thomas/Behara/Van der Ven *Chem. Mater.* 2024 (Li–Ag 합금상 이동 장벽) — Ag 의 Li 친화성 축 · 그리고 Lee et al. *Nat. Energy* 5, 299 (2020) (Ag–C 원전 · 세 digest 가 인용하지만 카드 없음).

---

## (e) DEM-DFT 보고서 (W_ad 보고서 7 절) 에 쓸 거리

| 7 절 항목 | 이 논문에서 쓸 점 | 위치 | 직접 봤나 |
|---|---|---|---|
| Li 친화성 (θ < 90° 친Li) | **친Li 와 공극 억제는 문턱이 다르다** — 공극 억제는 θ = 0° (W ≥ 2γ). γ-Li₃PO₄ 74.4° · Li₃P 71.1° 는 친Li 인데 공공이 계면에 모인다 | `Table S6` · `Table S7` (SI p.10) · digest §3d · §3f | ✅ 표 원해상도 (회전 크롭) |
| Young–Dupré cos θ = W/γ_Li − 1 | 본문은 W = σ_m(1 + cos θ) 꼴 (같은 식) · θ 열 12/12 를 ✎ 재현 · **θ 는 0 K 고체 · 변형 슬랩으로 낸 지표**라 녹은 Li 접촉각 아님 (보고서 한계 문장과 같은 선) | p.19905 오른쪽 단 · `Table S6` · `Table S7` | ✅ 본문 쪽 렌더 · 표 원해상도 |
| W > 2γ_Li 판정 | **왜 2γ 인가** — 식 (11) 에서 W = 2σ_m 이 계면 층 공공 에너지 = 벌크 공공 에너지가 되는 점 · "같은 금속 · 같은 방위 = 벌크" 에서 정확 · ✎ 퍼짐 계수 S = W − 2γ ≥ 0 과 같은 말 · 정합 12 계 검증 (✎ MAD 0.071 eV · 부호 11/12) · **비정합에선 하한** | 식 (4)–(12) p.19904–19905 · `Fig. 4` p.19908 · `Fig. S9` (SI p.7) · 하한 p.19910 첫 문단 | ✅ `Fig. 4` · `Fig. S9` 원해상도 + 픽셀 판독 |
| 공극 억제 기전 | 스트리핑 → 계면 층 공공 주입 → ΔE > 0 (W < 2γ) 이면 공공이 계면에 머물러 공극의 씨앗 · ΔE < 0 이면 금속 속으로 밀려남 · 이온성 기판 (LiCl +0.180) 대 금속 기판 (LiMg −0.223 eV) 의 부호 반전 한 장 · 비정합은 최약 자리가 정한다 · ⚠ 속도론 (전류 · 압력) 은 없다 — 장벽은 300 K ns–µs | p.19902 · `Fig. 1` p.19906 · `Fig. 2` · `Fig. 3` p.19907 · `Fig. 6` p.19909 | ✅ 전부 원해상도 |
| 금속 인터레이어 (Ag–C 층) | LiMg · AlSc 가 W/2σ 1.44–1.81 로 쉽게 넘는다 · 저자가 금속 인터레이어 · 반응성 젖음 · 집전체 (무음극) 를 명시적으로 권한다 · 단 인터레이어 안 Li 전도 유지 · **Ag · 탄소는 계산 안 했다** · 합금이 생기면 '날카로운 계면' 가정이 깨진다 (보고서 7 절 3 번과 같은 지점) | p.19911 · `Table S6` · `Fig. 3b,c` | ✅ |
| 그들의 DFT 설정 | VASP 5.4.4 · PBE · **vdW 없음** · 가장 무른 PAW (Li 1 가전자 · O_s) · 500 eV · 비스핀 · MP 0.1 eV · Γ 8³ / 11×11×5 · ab 같은 k 밀도 · c 1 점 · 진공 ≥15 Å · Li 11 층 · **고정층 없음** · 금속 쪽 변형 (strain 정의 (a−a₀)/a) · **이완 W_ad** (분리 슬랩 각각 이완) · 음이온 위 registry 1 · γ 는 같은 변형의 Li 슬랩 (E_bulk = Fiorentini–Methfessel 5 슬랩) | p.19903–19904 · SI pp.1–2 · `Table S1`–`S5` (SI pp.8–9) | ✅ `Table S5` 원해상도 · `Table S1`–`S4` 쪽 렌더 187 dpi |
| γ_Li 기준값 | Li BCC (100) **0.463** (as-cleaved 0.466) · HCP (0001) 0.583 · (10-10) 0.498 J m⁻² · 변형셀 0.419–0.472 → 2γ 문턱 0.838–0.944 · 소환값 EAM 0.368 · LLZO DFT 논문 0.471 | `Table S5` · `Table S6` · p.19910 | ✅ |
| 우리와 다른 점 (보고서가 지킬 것) | 이 논문 W_ad (이완) ≠ 우리 W_sep (고정 기하) — 정의상 W_sep ≥ W_ad · γ_Li 는 **우리 범함수 (D3 포함) · 우리 이완 기준 · 같은 Li 면 · 같은 변형**으로 새로 내서 비 W/2γ_Li 로만 판정 · 판정엔 최약 registry 도 | digest §7a–§7c | — |

보고서 7 절 문장 후보 (공유 보고서 문체 · 출처는 랩 표준 꼴):
- *W 를 2γ_Li 와 견주는 이유는, 계면 층의 Li 빈자리 (공공) 가 금속 속 빈자리와 같은 비용이 되는 점이 W = 2γ_Li 이기 때문이다 (J. Mater. Chem. A, 9, 19901 (2021)). W 가 그보다 작으면 방전 중 생긴 빈자리가 계면에 모여 공극의 씨앗이 된다.*
- *θ < 90° (친Li) 와 θ = 0° (W ≥ 2γ_Li) 는 다른 문턱이다 — 같은 계산에서 γ-Li₃PO₄ (74°) · Li₃P (71°) 는 친Li 였지만 빈자리가 계면에 모이는 쪽이었다.*
- *격자가 맞지 않는 계면에서는 평균 W 가 문턱을 넘어도 가장 약한 자리에서 빈자리가 모일 수 있어서, 2γ_Li 는 필요조건 (하한) 으로만 쓴다.*

---

## (f) 그림 크롭 요약

- **24 장** = 도구 5 (`Fig. 1` · `2` · `3` · `5` · `6`) + 손 19 — `Fig. 4` (캡션 블록 인식 실패 · 도구가 번호 공백으로 보고 · p.8 오른쪽 단 래스터) · SI 18 장 (`Fig. S1`–`S11` · `Table S1`–`S7` — **SI 두 PDF 에 글자 층이 없어** 도구가 0 장 · 잉크 띠로 영역을 정했다 · `Table S6`·`S7` 은 가로 쪽이라 90° 돌렸다). 크롭 경계는 축소 대조표로 전부 확인 (잘린 것 없음).
- **놓친 것: 없음** — 도구의 "번호 공백 · 놓친 캡션 후보" 18 건 전부 `resolved` (`fS11` 은 도구 목록에 없었지만 같이 잘랐다). SI 는 SI1 = SI pp.1–5 · SI2 = SI pp.6–11 로 한 SI 가 두 파일로 나뉜 것이다.
- **본 것: 24/24** — 13 장 원해상도 (`Fig. 1`–`6` · `Fig. S7` · `S9` · `S10` · `S11` · `Table S5` · `S6` · `S7`) · 11 장 SI 쪽 렌더 + 축소 대조표 (`Fig. S1`–`S6` · `S8` · `Table S1`–`S4`). 픽셀 판독 3 장 (`Fig. 4` · `Fig. 5b` · `Fig. S9`).
- **그림이 본문·표와 어긋난 것**: `Fig. 4`·`S9` 의 Li₂O 이완 점 0.396 대 `Table S6` 0.346 · `Fig. 5b` Cl top 범례 뒤바뀜 · 본문 hollow/Li top W 순서 반대 · Na/Li₃OCl 두 점 0.007–0.012 차 · 라벨 오기 (`Fig. S2` "Li₂O (100)" → (111) · `Fig. S3` "11 Li layers" · `Table S4` "a_Na,BCC") · 참조 오기 5.
- **임시 파일 점검 (병렬 충돌 주의 반영)**: 본문 글자 파일 (scratchpad 루트 `seymour_main.txt` · 이름에 seymour 접두) 은 PDF 를 다시 추출한 것과 **바이트 동일** (첫 줄 = 이 논문 제목 · 저자) — digest 의 본문 인용은 이 논문 글자다. SI 는 글자 층이 없어 글자 파일을 안 썼다 (이미지로만 읽음). 공용 이름 `crop_meta.json` 으로 넣은 `figures.json` 손 항목은 PNG 크기 · 원본 PDF 이름과 **24/24 일치**. 쪽 렌더 · 대조표 그림은 직접 본 내용이 이 논문 것이었다 (BCC Li · LiCl · `Table S1` 제목). 그 뒤 임시 파일은 scratchpad 의 `<slug>/` 하위로만 썼다.

---

## (g) Jeff Sakamoto 저자 여부

**아니다** — 저자는 Ieuan David Seymour (교신) · Ainara Aguadero 두 명 (Imperial College London). J. Sakamoto 공저 논문을 **7 편 인용**할 뿐이다 (refs 5 · 12 · 17 · 18 · 29 · 32 · 86 — 그중 ref 17 Sharafi 2017 · ref 29 Wang 2019 *Joule* 은 같은 배치 digest). digest 머리말에는 그 이름을 쓰지 않았고 `_paper_pis` = [] 다 — INDEX 행에 `🏷 Jeff Sakamoto 공저` 를 달지 않는다.

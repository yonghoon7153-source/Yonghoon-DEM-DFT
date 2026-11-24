<!-- digest 표준 양식 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 기준 = papers/liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md
     2026-11-24 신규 · 논문 에이전트 (병렬 묶음 — 이 파일과 litdb/figures/<slug>/ 만 썼다 · INDEX · comparison · pdf_map 은 메인 세션이 합친다).
     원문 = 본문 9 pp (Perspective · 인쇄 쪽 673–681) + SI 6 pp (표지 · 저자 · Table S1 · Fig. S1 · Fig. S2 · Table S2 · Table S3 · SI refs 17). 본문 refs 98.
     쪽 표기 = 인쇄 쪽 (p. 673 = PDF 1 쪽 … p. 681 = PDF 9 쪽). SI 는 'SI p. n' = SI PDF 쪽.
     크롭 9 장 = 그림 6 (본문 4 + SI 2) + 표 3. **그림 6 장 전부 Read 로 실제로 봤다.**
       도구 크롭 그대로 = Fig. S1 · Fig. S2
       손 크롭 1 = Fig. 1 (도구가 'p2 영역 없음' 으로 건너뜀 — 작은 래스터 ≈1,140 조각 + 벡터 상자로 된 도식)
       재크롭 3 = Fig. 2 (패널 라벨 a · F_stack pressure 줄이 잘림) · Fig. 3 (왼쪽 단만 잘려 b–d 패널과 확대 원 2 개가 빠짐) · Fig. 4 (패널 제목 줄 잘림)
       사유는 figures.json 의 manual_crop · recrop.  표 3 장은 이미지로 안 봤다 — PDF 텍스트 (Table S3 은 pymupdf find_tables 로 칸 대조).
     값 표지: [인쇄] = 본문 · SI 글자 · figure-read ≈ = 그림에서 읽은 값 (§3.6 · 방법 병기) · ✎ 우리 산술 = 인쇄값으로 이 카드가 계산한 값 (§13 식 병기) ·
     [1차] = 이 관점 논문이 인용한 원 논문의 주장 (원문 미확인 — 이 PDF 의 요약 문장만 옮김). -->

# 무음극 (anode-free) 전고체전지의 **전기-화학-역학** — 첫 석출 (접촉 · 핵생성 · 적층압 · 온도 · 집전체 두께 · Cu/Li₂O 화학 불균일 · SE 미세구조) → 사이클 (CE > 99.95 % · 방전 끝 **국부 Li 고갈** 공극 → 다음 충전 필라멘트) → 인터레이어 (탄소 · Au/Ag · Li₂Te · Ag–C) — Sandoval · Haslam (공동 1) · … · Jeff Sakamoto · McDowell (*Nat. Mater.* 24, 673–681 (2025) · Perspective)

> slug `sandoval2025_electro_chemo_mechanics_anode_free_ssb` · DOI `10.1038/s41563-024-02055-z` · type `review (Perspective · 자체 계산 0 · 자체 실험 0 · SI = 에너지밀도 산정 1 건)` · PDF `litdb/inbox/afssb2024_electro_chemo_mechanics_main.pdf` (+ SI `litdb/inbox/afssb2024_electro_chemo_mechanics_SI.pdf`, 6 pp) · digested `2026-11-24` · status ✅
> elements: Li, Cu, Ag, Au, C, Te, O, P, S, Cl, La, Zr
> methods: —  (해당 없음 — 관점 논문 · 자체 계산·측정 0 · SI 의 에너지밀도는 문헌 계산기 (SI ref 1 = *Joule* 5, 1371 (2021)) 로 낸 값)
> **저자**: Stephanie Elizabeth Sandoval (공동 1) · Catherine G. Haslam (공동 1) · Bairav S. Vishnugopi · Daniel W. Liao · Jeong Seop Yoon · Se Hwan Park · Yixian Wang · David Mitlin · Kelsey B. Hatzell · Donald J. Siegel · Partha P. Mukherjee · Neil P. Dasgupta · **Jeff Sakamoto** · **Matthew T. McDowell** (교신 · mattmcdowell@gatech.edu)
> 🏷 **Jeff Sakamoto 공저** — 소속 번호 3 · 4 · 6 · 12 · 13 (MUSIC EFRC · Michigan MSE · Michigan ME · UCSB Materials · UCSB ME)

> ⚠⚠ **세 줄 경고 — 인용 전에 반드시.**
> ① **이 논문은 자체 데이터가 없다** (Perspective). 본문의 숫자는 몇 개뿐이고 (10–500 MPa · ~1 MPa · > 99.95 % · < 99.6 % · ≈5 µm · 100–150 nm · 1,000 cycles) 전부 **인용한 1 차 논문의 값**이다.
>    이 논문 고유의 수치는 SI 의 에너지밀도 (`Fig. 1` · `Table S1`) 하나뿐이다. **값은 §4 지도의 1 차 출처로 가서 인용한다.**
> ② **'압력' 숫자 셋은 층위가 다르다** — 황화물 CC 접촉 **제조 압착 ~10–500 MPa** (p. 674) · 실험실 **운전 적층압 ~1 MPa – 수백 MPa** (p. 675) · 실용 한계 **> ~1 MPa 어려움 → 목표 < 1 MPa** (p. 675 · 678).
>    섞어 인용하지 않는다 (`doux2020_stack_pressure_assb` 의 제조 / 운전 구분과 같은 꼴).
> ③ **`Fig. 2` · `Fig. 3` 은 개념 도식**이다 (축 · 눈금 없음). **`Fig. 4` 만 실측 단면**이고 **다른 논문 4 편에서 가져온 것**이다 (a ref 88 · b ref 29 · c ref 95 · d ref 30) — 그 관찰은 원 논문으로 인용한다.

---

## 0. 이 digest 를 읽는 법 — 세 읽기축

1. ★ **주장 → 1 차 출처 지도** (§4) — 사용자 요청 5 축: **방전 중 공극 (§4.1) · 충전 중 Li 필라멘트 침투 (§4.2) · 적층압 요구 (§4.3) · 인터레이어 (§4.4) · 집전체 (§4.5)** + 보조 (핵생성 · 온도 · 계면상 · SE 미세구조 · CE, §4.6). 칸마다 쪽 · 그림 · 인용 번호 · litdb 상태.
2. ★ **W_ad 보고서 §7 (Li 친화성 · 점착과 공극 · 인터레이어)** 에 쓸 것 (§7-2 · §8). 우리 W 값은 여기 싣지 않는다 — **위치만** (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §2 · §7 · §7-1).
3. ★ **연속체 · DEM 모델 입력** (§7-3) — `Fig. 2a` 의 매개변수 11 개 · 압력 층위 셋 · 방전 끝 접촉 면적 축소 (`Fig. 3d`) · 집전체를 변형·파단하는 판으로 (`Fig. 2e`) · 석출 Li 두께 환산 (§13-2).

---

## 1. 한 줄 요약

**음극 활물질 없이 (방전 상태 양극 + 맨 집전체) 조립하는 무음극 전고체전지는, Li 과잉 (Li 박) 셀과 같은 고체–고체 계면 역학에 세 가지가 더 얹힌다.**
① 첫 Li 는 **집전체(CC)|SE 가 닿은 곳에서만** 핵생성할 수 있어서, 접촉 형성 · 점착 · CC 표면 화학 (Cu 는 친Li 인데 산화막 Cu₂O 는 Li 와 만나 **소Li 인 Li₂O** 로 바뀐다) · CC 두께 · 적층압 · 온도 · 전류가 첫 형태를 정한다 (`Fig. 2`).
② Li 재고가 없어서 평균 **CE > 99.95 %** 가 있어야 1,000 사이클을 간다 (ref 37).
③ 방전 끝에 Li 를 거의 다 벗겨야 하므로, 고르게 안 벗겨지면 **남은 Li 섬으로 전류가 몰려 *낮은 전체 전류에서도* 공극이 커지고 다음 충전에 필라멘트**가 생긴다 (`Fig. 3d` · ref 23) — Li 과잉 셀의 '임계 박리 전류' 기전과 다른 점이다.
해법 축은 **인터레이어** (탄소 · Au/Ag 합금 · Li₂Te · Ag–C 복합; `Fig. 4` · `Table S3`) 이고, 남은 과제는 **저압 (< 1 MPa) · 상온 운전**, **SE 와 Li 양쪽에 붙는 인터레이어**, 계면상 조절, CC 공학, 조립 조건 보고 표준이다.
⚠ 이 논문 고유 수치인 에너지밀도는 **부피 1,208 → 1,435 Wh l⁻¹ (+19 %)** 지만 **중량은 464 → 479 Wh kg⁻¹ (+3 %)** 뿐이다 (LPSCl · `Table S1` · ✎ §13-4).

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 (14) | Stephanie Elizabeth Sandoval¹²³† · Catherine G. Haslam³⁴† · Bairav S. Vishnugopi³⁵ · Daniel W. Liao³⁶ · Jeong Seop Yoon³⁶ · Se Hwan Park³⁷ · Yixian Wang³⁸ · David Mitlin³⁸⁹ · Kelsey B. Hatzell³⁷¹⁰ · Donald J. Siegel³⁸⁹¹¹ · Partha P. Mukherjee³⁵ · Neil P. Dasgupta³⁴⁶ · **Jeff Sakamoto**³⁴⁶¹²¹³ · **Matthew T. McDowell**¹²³\* († 공동 1 · \* 교신) |
| 소속 | ¹Georgia Tech MSE · ²Georgia Tech G. W. Woodruff ME · ³**MUSIC DOE Energy Frontier Research Center** (Univ. Michigan) · ⁴Michigan MSE · ⁵Purdue ME · ⁶Michigan ME · ⁷Princeton Andlinger Center · ⁸UT Austin Texas Materials Institute · ⁹UT Austin Walker ME · ¹⁰Princeton MAE · ¹¹UT Austin Oden Institute · ¹²UCSB Materials · ¹³UCSB ME (SI 의 소속 번호 매김은 본문과 다르다 — 본문을 따른다) |
| 서지 | *Nature Materials* **24**, 673–681 (2025, May issue) · DOI `10.1038/s41563-024-02055-z` · 기사 유형 **Perspective** |
| 일정 | Received 2024-06-04 · Accepted 2024-09-27 · Published online 2025-01-02 |
| 자금 | MUSIC (Center for Mechano-Chemical Understanding of Solid Ion Conductors) — DOE Office of Science · BES EFRC · contract DE-SC0023438 |
| 심사 | *"Nature Materials thanks Daniel Rettenwander and the other, anonymous, reviewer(s)"* |
| 기여 · 이해상충 | *"All authors contributed to writing the paper."* · competing interests 없음 |
| 분량 | 본문 그림 4 (도식 3 + 단면 모음 1) · 표 0 · refs **98** · SI: `Fig. S1` · `Fig. S2` (막대 그래프) · `Table S1` (에너지 지표) · `Table S2` (산정 입력) · `Table S3` (인터레이어 16 행) · SI refs 17 |
| 연구 유형 | **관점 (Perspective)** — 자체 실험 · 계산 · 시뮬레이션 0. 이 논문이 직접 낸 수치는 SI 의 에너지밀도 (문헌 계산기 사용) 뿐 |
| 데이터 | n/a (데이터 가용성 문장 없음) |
| 계보 (MUSIC EFRC 컨소시엄) | 공저자 그룹의 1 차 연구가 근거의 큰 몫이다 — 참고문헌의 **보이는 저자 이름**만 세어도 공저자가 든 편이 **≥ 27 / 98** (✎ — et al. 뒤 저자는 목록에 없어 못 센다 · §10-②). 예: Sandoval 2021 · 2023 (refs 93 · 29) · Haslam 2022 · 2023 (74 · 24) · Sakamoto 그룹 (10 · 21 · 36 · 37 · 44 · 61 · 84) · Dasgupta (15 · 37 · 66) · Liao 2024 (88) · Yoon 2023 · 2024 (34 · 25) · Siegel (26 · 34 · 60) · Vishnugopi (59 · 70 · 72) · Hatzell (5 · 31) · Park 2022 (86) · McDowell (11) · Wang Y. (57 · 95 — 동명 가능성) |
| 이 논문의 자리 | litdb 의 무음극 · 점착 카드들 (`liao2025_…` = ref 88 의 후속 · `spencerjolly2023_…` = SI ref 12 · `doux2020_stack_pressure_assb` = ref 79) 을 **한 장의 지도**로 묶는 field-map. 수치 앵커가 아니라 **출처 지도 + 개념 틀** 로 쓴다 |

---

## 3. 핵심 수치 ★ (이 논문에 인쇄된 것 전부 + figure-read)

### 3.1 에너지밀도 — `Fig. 1` · `Fig. S1` · `Fig. S2` · `Table S1` [인쇄]

| SSE | 구성 | 부피 Wh L⁻¹ | 중량 Wh kg⁻¹ | 비고 |
|---|---|---|---|---|
| — | Li-ion (액체 전해질 · 흑연) | 784 | 290 | `Table S1` 첫 행 |
| LPSCl | Li 과잉 (Li 20 µm) | **1,208** | **464** | `Fig. 1a` 의 1,208 Wh l⁻¹ |
| LPSCl | 무음극 | **1,436** (`Fig. 1b` 는 **1,435**) | **479** | ✎ 재현 1,435.8 → 표는 반올림 · 그림은 버림 (§13-1) |
| LLZO | Li 과잉 | 1,208 | 329 | 부피는 SE 밀도와 무관 → LPSCl 과 같다 |
| LLZO | 무음극 | 1,436 | 337 | |

- **본문 주장** (p. 673): SSB 는 Li-ion 보다 에너지밀도가 **최대 50 % 높을 수 있다** (refs 2–5 — 이 숫자는 1 차 인용값), 무음극은 *"even greater energy density"* (refs 10–13 · `Fig. 1b` · `Fig. S1` · `Fig. S2` · `Table S1` · `Table S2`).
- `Fig. S1` (본 그림): 막대 셋 Li-ion ≈ 784 · Li Excess ≈ 1,208 · **'Reservoir Free'** ≈ 1,436 (figure-read ≈ — SI 는 무음극을 'Reservoir Free' 로 부른다). 막대가 한 벌뿐 = LPSCl · LLZO 공통.
- `Fig. S2` (본 그림): ≈ 290 · ≈ 464 · ≈ 479 Wh kg⁻¹ = **LPSCl 값만** 그렸다 (라벨에 SE 이름 없음 · LLZO 329 · 337 은 표에만).
- ✎ 무음극 이득 (§13-4): 부피 **+18.9 %** · 중량 **+3.3 % (LPSCl) / +2.3 % (LLZO)**. Li-ion → 무음극 LPSCl 은 부피 ×1.83 · 중량 ×1.65.
- ✎ '과잉 Li' = **20 µm = 4.09 mAh cm⁻² ≈ 양극 용량의 1.02 배** (§13-3) — 과잉이 거의 1 배인 가벼운 시나리오다. 과잉을 더 크게 잡으면 무음극 이득은 더 커진다.

### 3.2 산정 입력 — `Table S2` 전부 [인쇄]

| 묶음 | 변수 → 값 |
|---|---|
| 공통 | 양극 면적 용량 **4 mAh cm⁻²** · 양극 비용량 200 mAh g⁻¹ · 양극 밀도 3.7 g cm⁻³ · Cu CC **5 µm** (8.9 g cm⁻³) · Al CC **5 µm** (2.7 g cm⁻³) |
| Li-ion | 양극 상대밀도 70 % · N:P 1.2 · 흑연 상대밀도 70 % · 흑연 372 mAh g⁻¹ · 흑연 밀도 2.26 g cm⁻³ · 평균 전압 3.7 V · 분리막 20 µm · 분리막 상대밀도 45 % · 분리막 밀도 0.71 g cm⁻³ · 전해액 밀도 1.26 g cm⁻³ |
| SSB | 양극 상대밀도 95 % · 양극 안 SE 부피분율 25 % · Li 두께 **0 / 20 µm** · Li 비용량 3,860 mAh g⁻¹ · Li 밀도 0.53 g cm⁻³ · 평균 전압 3.8 V · SE 두께 **20 µm** · SE 밀도 **LPSCl 1.64** / LLZO 5.1 g cm⁻³ · SE 상대밀도 LPSCl **90 %** / LLZO 99.5 % |
| 계산 도구 | *"Calculations were performed with the SSB energy density calculator published in supplementary reference 1."* — SI ref 1 = Wang · Kazyak · Dasgupta · Sakamoto, *Joule* 5, 1371 (2021) (= 본문 ref 37) |

- ⚠ **LPSCl 밀도 1.64 g cm⁻³ 는 출처 표기 없이** 쓰였다 — litdb `INDEX.md` 의 '🧮 LPSCl 펠릿 밀도 · 진밀도 1.64 출처 묶음' 에 걸리는 또 한 자리 (결정 밀도 ≈1.86 으로 바꾸면 중량값 −2.4 %, ✎ §13-6).
- ✎ 이 표 값만으로 `Table S1` 의 SSB 네 행과 Li-ion 부피값을 **소수 첫째 자리까지 재현**했다 (§13-1 — 양극 = CAM 75 vol % + SE 25 vol % · 상대밀도 95 % 로 읽으면 맞는다). Li-ion 중량값 290 은 이 표만으로는 재현 안 된다 (바인더 · 도전재 등 표에 없는 가정이 들어간 것으로 보임 — 미확인).

### 3.3 CE · 사이클 문턱 [인쇄 · 모두 1 차 인용값]

| 수치 | 쪽 | 문장 요지 | 출처 |
|---|---|---|---|
| **CE > 99.95 %** | p. 674 | 과잉 Li 가 없어 부반응 손실을 메울 수 없다 | (인용 없음 — p. 676 에서 ref 37) |
| **> 99.95 % to achieve 1,000 cycles** | p. 676 | 평균 CE 요구 | ref 37 (*Joule* 5, 1371) · ⚠ 수명 끝 기준 미기재 — ✎ CE^N 모형으로 0.9995¹⁰⁰⁰ = **0.61** (80 % 기준이면 99.978 % 필요, §13-7) |
| 액체 Li 금속 CE **대개 < 99.6 %** | p. 676 | 액체와의 연속 부반응 | refs 65–67 |
| Ag–C 복합 **1,000 사이클 넘게** 'excellent stability' | p. 678 | 단일 인터레이어의 장기 한계를 넘는 예 | refs 30 · 82 |
| 과잉 Li **≈5 µm** 이면 안정성 개선 | p. 677 | CE 요구 완화 + 석출·박리 균일 | refs 23 · 83 · 84 |

### 3.4 압력 · 온도 [인쇄 · 모두 1 차 인용값]

| 층위 | 값 | 쪽 | 출처 |
|---|---|---|---|
| **제조** — 황화물 (Li₆PS₅Cl) CC 접촉 | 일축 또는 등방 압착 **~10 MPa – ~500 MPa** | p. 674 | refs 29 · 30 |
| 제조 — 산화물 (LLZO) | CC 를 **900 °C** + *moderate* 일축압으로 접합 | p. 674 | ref 10 |
| 제조 — 산업 | 황화물 분리막과 CC 를 **롤 압착**으로 일체화 | p. 674 | ref 31 |
| **운전 (실험실)** | **~1 MPa – 수백 MPa** | p. 675 | refs 10 · 20 · 22 · 36 |
| 운전 — 기전 문턱 | **> 1 MPa** 에서 석출 Li 크리프 촉진 | p. 675 | refs 10 · 20 · 36 |
| **운전 (실용)** | **> ~1 MPa 는 걸기 어렵다** | p. 675 | ref 37 |
| 목표 | 인터레이어 = **zero or minimal (< 1 MPa)** 운전의 레버 · 저압 (< 1 MPa) 연구 시급 | p. 678 | refs 37 · 81 (결론 문장은 인용 없음) |
| 온도 | 수치 없음 — 고온은 Li 수송 · 크리프 · 핵 밀도를 바꾼다는 정성 서술 | p. 675 | refs 44–50 |

### 3.5 인터레이어 · 석출량 — `Fig. 4` · `Table S3` [인쇄]

**`Fig. 4` 패널** (캡션):

| 패널 | 인터레이어 | 석출량 | 기법 | CC · SE | 원 출처 |
|---|---|---|---|---|---|
| a | 탄소 | 2 mAh cm⁻² | 단면 **plasma FIB-SEM** | (CC) · LPSCl | ref 88 (CC BY 3.0) |
| b | Au **100 nm** 를 입힌 Cu | 1 mAh cm⁻² | **cryo-FIB-SEM** | Cu · (SSE) | ref 29 (Elsevier) |
| c | Cu₂Te | 3 mAh cm⁻² | 단면 cryo-FIB-SEM | (CC) · SSE | ref 95 (Wiley) |
| d | Ag–C | 5 mAh cm⁻² | 단면 SEM | **SUS** (스테인리스) · SSE | ref 30 (Springer Nature) |

**본문 두께**: *"100–150 nm silver or gold interlayers"* (황화물 · 산화물, refs 24 · 29 · p. 678).

**`Table S3` 전부** (16 행 · 원문 *"non-exhaustive"* · 성능 지표 칸 없음):

| # | 인터레이어 | 두께 | 제법 | 전해질 | CC | 출처 (SI ref → 본문 ref · litdb) |
|---|---|---|---|---|---|---|
| 1 | Au, Ag | 100 nm | sputtered | Li₆PS₅Cl (LPSC) | Cu | SI 2 = Sandoval 2023 *Joule* 7, 2054 (본문 29) |
| 2 | Au | 150 nm | sputtered | LLZO | Cu | SI 3 = Haslam & Sakamoto 2023 *JES* 170 (본문 24) |
| 3 | Cu₂Te | 1000 nm | evaporated | LPSC | Cu | SI 4 = Wang Y. *Adv. Mater.* 2206762 (본문 95 — SI 는 2022, 본문은 35 권 2023) |
| 4 | ZnO | 100 nm | ALD | PEO · LiTFSI · succinonitrile · Li₁.₅Al₀.₅Ge₁.₅(PO₄)₃ | Cu | SI 5 = Liu M. *ACS Mater. Lett.* (2020) (본문 없음) |
| 5 | Al₂O₃ | 20 / 4 nm | ALD | Li₁₀GeP₂S₁₂ (LGPS) | Mo | SI 6 = Davis 2020 *J. Mater. Chem. A* 8, 6291 (본문 없음) |
| 6 | Ag | 100 nm | (빈칸) | gel polymer | 도전 카본블랙 (1 µm) 코팅 Al | SI 7 = Hsueh 2023 *Electrochem. Commun.* 150, 107478 |
| 7 | LiCoO₂ | (빈칸) | aerosol deposition | LiPON | SUS/Pt | SI 8 = Yamamoto 2019 *Electrochem. Commun.* 105, 106494 (역적층 박막전지) |
| 8 | Carbon, Pt, Au | 50, 10, 10 nm | thermal evaporation | LiPON | Cu | SI 9 = Müller 2024 *ACS AMI* 16, 695 (본문 85) |
| 9 | Ag–카본블랙 (CB) | 10 µm | mechanically pressed | LPSC (thin film) | 스테인리스 | SI 10 = Lee 2020 *Nat. Energy* 5, 299 (본문 30) |
| 10 | 흑연 · CB · CB-Al · CB-Ag · CB-Ni · CB-Sn · CB-Zn | 10 µm | mechanically pressed | LPSC (thin film) | 스테인리스 | SI 11 = Suzuki 2021 *Adv. Energy Sustain. Res.* 2 (본문 90) |
| 11 | 흑연-Ag | 5 µm | spray coated | LPSC | Cu | SI 12 = Spencer-Jolly 2023 *Joule* 7, 503 (본문 없음 · litdb ✅ `spencerjolly2023_…` — ⚠ 그 카드는 분무 기판을 **스테인리스 CC** 로 적는다 · operando 셀 창 보호만 1 µm Cu) |
| 12 | 흑연 · CB | 3 µm | slurry casting | LLZO | Cu | SI 13 = Kim S. 2023 *ACS Energy Lett.* 8, 9 (본문 91 · SI 제목 'freferred' 오타) |
| 13 | 비정질 탄소 | 100 nm | sputtered | LiPON | (빈칸) | SI 14 = Futscher 2022 *J. Mater. Chem. A* 10, 15535 |
| 14 | ZnO 코팅 CNT | 벽 20 nm · 내경 100 nm | electrospinning | PEO | Cu | SI 15 = Chen Y. 2020 *Nature* 578, 251 (Coble creep) |
| 15 | 비정질 탄소 | 13 µm | mechanically pressed | LPSC | Cu | SI 16 = Liao 2024 *J. Mater. Chem. A* 12, 5990 (본문 88 · `Fig. 4a`) |
| 16 | 탄소 | 5 µm | solution cast | Li₃PS₄ (LPS) | 스테인리스 | SI 17 = Park 2022 *J. Mater. Chem. A* 10, 21995 (본문 86) |

- 두께 범위 **4 nm (ALD) – 13 µm** · 제법 8 종 · 전해질이 고분자 · 겔 · LiPON · LGPS · LLZO · LPSC 로 섞여 있다 → **순위표가 아니라 목록**이다. 우리 계 (LPSCl) 행은 1 · 3 · 9 · 10 · 11 · 15 (16 은 LPS).

### 3.6 figure-read — `Fig. 4` 단면의 Li 층 두께 (우리 판독)

방법: 300 dpi 크롭 (`fig_4.png`, 2224 × 516 px) 에서 패널마다 **축척 막대 길이 (흰 픽셀 연속 구간)** 와 **패널 가운데 띠의 밝기 단면**으로 Li 층 위·아래 경계를 잡았다. 치밀 Li 기대값은 `Table S2` 상수 (0.53 g cm⁻³ · 3,860 mAh g⁻¹) 로 ✎ **4.89 µm per mAh cm⁻²** (§13-2).

| 패널 | 석출량 | 축척 막대 | Li 층 (경계) | figure-read ≈ Li 두께 | ✎ 치밀 Li 기대 | 비 |
|---|---|---|---|---|---|---|
| a 탄소 | 2 mAh cm⁻² | 5 µm = 135 px | ≈210 px (CC 아래 → 탄소층 위) | **≈ 7.8 µm** | 9.8 µm | ≈ 0.80 |
| b Au | 1 mAh cm⁻² | 10 µm = 153 px | 74 px (검은 띠) | **≈ 4.8 µm** | 4.9 µm | ≈ 0.99 |
| c Cu₂Te | 3 mAh cm⁻² | 5 µm = 107 px | ≈267 px (Li₂Te–Cu 아래 → SSE 위) | **≈ 12.5 µm** | 14.7 µm | ≈ 0.85 |
| d Ag–C | 5 mAh cm⁻² | 10 µm = 89 px | ≈215 px (밝은 선 아래 → SUS 위) | **≈ 24 µm** | 24.4 µm | ≈ 0.99 |

- ⚠ **FIB 단면의 기울기 보정 여부가 캡션에 없다** (보정 안 하면 수직 길이가 짧게 보인다) · 경계 선택 오차 ±5–10 % · 원 그림의 재가공 여부 미상. **b · d 는 '치밀 Li 가 석출량만큼' 과 맞고, a · c 는 0.8–0.85** 다 — 기울기 · 탄소 기공 속 Li · 경계 판독 중 무엇 때문인지 이 PDF 로는 못 가른다.
- 쓰는 곳: DEM · 연속체에서 석출 Li 를 '치밀층 · 석출량 × 4.89 µm' 로 놓는 가정의 **자릿수 확인** (±20 % 안).

---

## 4. ★ 주장 → 1 차 출처 지도 (사용자 요청 5 축 + 보조 축)

> 읽는 법: '주장' 은 이 관점 논문의 문장 요지 (번역) 다 — **1 차 논문의 원문은 확인하지 않았다** [1차]. 숫자를 쓸 때는 오른쪽 출처로 간다.
> litdb 칸: ✅ = digest 있음 (slug) · 📥 = PDF 가 `litdb/inbox/` 에 있음 (2026-11-24 묶음 · 이 시점 digest 미확인) · — = 없음.
> 참고문헌 전체 (98 편) 와 역할은 §14.

### 4.1 방전 중 공극 (void) ★

| 주장 | 쪽 · 그림 | 인용 1 차 출처 | litdb |
|---|---|---|---|
| Li 과잉 셀: 박리가 Li 보급보다 빠르면 **공극 → 접촉 상실 · 고저항**. 액체 전지엔 없는 고체 고유 현상 | p. 674 | 20 Kasemchainan 2019 *Nat. Mater.* 18, 1105 · 21 Wang, Choudhury, Sakamoto 2019 *Joule* 3, 2165 | 20 — · 21 📥 `wang2019_li_se_stack_pressure_*` |
| 공극 = **임계 박리 전류밀도** 위에서 — Li 를 공공 확산이나 기계적 변형으로 계면에 충분히 빨리 못 보낼 때 | p. 676 | 20 · 21 | 〃 |
| 무음극도 같은 공극 (고전류 박리 · `Fig. 3c`) — 그러나 **거의 100 % DoD 로 다 벗겨야** 해서 차이가 생긴다 | p. 676 · `Fig. 3c` | 73 Heubner 2021 *Adv. Funct. Mater.* 31, 2106608 | — |
| ★ **무음극 고유**: 불균일 박리 → 박리 끝 무렵 다 벗겨진 곳 옆에 Li 가 남는다 → 벗겨진 곳은 (CC 가 SE 에 닿든 말든) 더 박리 못 함 → **남은 Li 섬으로 전류 집중 → 섬이 옆으로 줄며 공극 가속** | p. 676 · `Fig. 3d` | **23 Lewis 2023 *Adv. Energy Mater.* 13, 2204186** | — |
| 이 고장은 Li 과잉 셀의 '임계 박리 전류 초과' 공극과 다르다 — 국부 고전류가 **기하 접촉 면적 감소**에서 오므로 **낮은 전체 전류에서도** 생긴다 | p. 677 | 23 · 29 Sandoval 2023 *Joule* 7, 2054 | — |
| 표면 확산 · Li 기계 변형이 CC 위 Li 재분배를 도울 수 있는지 더 연구 필요 | p. 677 | 49 LePage 2019 *JES* 166, A89 · 74 Haslam 2022 *J. Power Sources* 520, 230831 | — |
| 적층압이 **공극 회복**에 영향 | p. 677 | 20 · 39 Zhang 2020 *Cell Rep. Phys. Sci.* 1, 100012 · 75 Shin 2024 *ACS Energy Lett.* 9, 1035 | — |
| 높은 적층압은 공극을 줄이지만 **석출 중 Li 침입을 늘린다** (§4.2) | p. 677 | 78–80 | 79 ✅ |
| 무압 안정 박리 = **Li 확산을 본질적으로 조절**하는 전략 — 음극 구조 개조 · 인터레이어 | p. 677 | 81 Fuchs 2022 *AEM* 12, 2201125 · 인터레이어 24 · 29 · 30 · 82 | — |
| 인터레이어가 접촉을 유지하며 계면으로 Li 수송을 도와 **저압에서 흔한 공극**을 줄인다 | p. 678 | 81 | — |
| **≈5 µm 과잉 Li** → CE 요구 완화 · 석출·박리 균일 — 조립 때 넣거나 (83) 방전 용량을 제한해 계면 Li 를 남김 (23 · 84) · 대가 = 분위기 제어 · 과잉 양극 → 비에너지↓ | p. 677 | 23 · 83 Wang D. 2023 *ACS Energy Lett.* 8, 5248 · 84 Lee & Sakamoto 2023 *Faraday Discuss.* 248, 250 | — |
| 거친 Li/SSE 계면 = **박리 용량 · CE 낮음** (거칠기가 달라도 in situ 석출은 됨) | p. 676 | 61 Lee & Sakamoto 2024 *AEM* 14, 2303571 | — |
| 다공 SSE 골격에 Li 를 담으면 박리 효율↑ · 비에너지↓ | p. 676 | 62 Alexander 2023 *Nat. Mater.* 22, 1136 | — |
| LPSCl 의 Li 환원 분해 → Li · SSE 미세구조 변화 · **반응 수축이 계면 공극을 만들 수 있다** | p. 676 | 56 Hao 2023 *AEM* 13, 2301338 · 57 Wang Y. 2024 *AEM* 14, 2304530 · 58 Lin 2024 *ACS Energy Lett.* 9, 2387 | — |
| Li 결정립 크기 → 질량 수송 · 소성 변형 → **박리 중 접촉 변화** (가설로 제시된 것) | p. 674 | 34 Yoon, Sulaimon, Siegel 2023 *JMCA* 11, 23288 | — |
| **점착 · 젖음 조절 = 저압 안정 사이클의 핵심** · 점착과 Li 내부 응력은 얽혀 있다 | p. 678 | 53 Seymour 2023 *ChemSusChem* 16, e202202215 · 74 | — |
| Li 와 계면상 구성물 · 이질 CC 사이 점착이 **접촉 상실 동역학**에 영향 | p. 676 | 53 | — |
| 무음극 Li 는 고순도 예상 (단이온 전도체) — Li 박의 불순물은 박리 중 계면에 쌓일 수 있다 | p. 679 | (인용 없음 — 저자 추론) | — |
| 방전 끝 전류 · 전압의 **폐루프 제어** | p. 679 | 37 Wang, Kazyak, Dasgupta, Sakamoto 2021 *Joule* 5, 1371 | — |

### 4.2 충전 중 Li 필라멘트 침투 ★

| 주장 | 쪽 · 그림 | 인용 1 차 출처 | litdb |
|---|---|---|---|
| 다음 충전 때 불완전 접촉 → 불균일 석출 · **공극 둘레 전류 집중 → 수지상·필라멘트가 SSE 를 뚫고 단락** | p. 674 | 14 Kazyak 2022 *Matter* 5, 3912 · 20 · 22 Krauskopf 2019 *ACS AMI* 11, 14463 | — |
| 필라멘트는 대개 **불균일 고체 접촉 + 전류 집중**에서 시작해 SSE 침투·파괴 확률을 높인다 | p. 676 | 22 · 69 Lewis 2021 *Nat. Mater.* 20, 503 · 70 Vishnugopi 2022 *AEM* 13, 2203671 · 71 Eckhardt 2022 *ACS AMI* 14, 35545 · 72 Vishnugopi 2021 *ACS Energy Lett.* 6, 3734 | — |
| 공극 성장 → 전류 집중 → 다음 석출에서 필라멘트 (Li 과잉의 사슬) | p. 676 | 20 · 21 | 21 📥 |
| 무음극: 고전류 공극 (`Fig. 3c`) · 불균일 박리 고립 섬 (`Fig. 3d`) 둘 다 **다음 석출에서 필라멘트** | p. 677 · `Fig. 3c,d` | 23 (도식) | — |
| SSE 파괴 · 필라멘트는 Li 과잉 셀에서 많이 연구됐고 **무음극도 같은 기전으로 '예상'** 된다 (직접 증거 제시 없음) | p. 676 | 52 Ning 2023 *Nature* 618, 287 | — |
| **두꺼운 CC** → 옆 성장은 좋지만 SSE 에 응력 축적 → **균열 전파 · 필라멘트** | p. 676 · `Fig. 2e` | 52 | — |
| 적층압 ↔ **SSE 안 Li 침투** · 기계적 파괴 | p. 677 | 59 Vishnugopi 2022 *AEM* 12, 2102825 · 76 Swamy 2018 *JES* 165, A3648 · 77 Ning 2021 *Nat. Mater.* 20, 1121 | — |
| ★ **높은 적층압 → 석출 중 Li 침입 경향 증가** (적층압 딜레마) | p. 677 | 78 Hänsel & Kundu 2021 *Adv. Mater. Interfaces* 8, 2100206 · **79 Doux 2020 *AEM* 10, 1903253** · 80 Fincher 2022 *Joule* 6, 2794 | 79 ✅ `doux2020_stack_pressure_assb` |
| 고립 Li 는 **크기 의존 항복 강도** 때문에 높은 응력을 받을 수 있다 → Li 변형 증폭 또는 **SSE 파괴** · SSE 역학에도 의존 | p. 675 | 41 Fincher 2020 *Acta Mater.* 186, 215 · 42 Xu 2017 *PNAS* 114, 57 | — |
| 불균일 응력 → 반응 불균일 · **전류 핫스팟** | p. 675 | 14 | — |
| SSE 미세구조 (입계 · 결정립) → 필라멘트 경로 | p. 676 | 52 · 57 · 59 · 60 Yu & Siegel 2018 *ACS AMI* 10, 38151 | — |
| `Fig. 3` 확대 원 (본 그림 · 도식): c = 남은 Li 층에서 SE 로 **쐐기형** 필라멘트 · d = CC 가 SE 에 닿은 자리 (공극 옆) 에서 **입자 경계를 따라 지그재그** | `Fig. 3c,d` | 도식 (인용 없음) | — |

### 4.3 적층압 요구 ★

| 주장 | 쪽 · 그림 | 인용 1 차 출처 | litdb |
|---|---|---|---|
| 실험실 적층압 범위 **~1 MPa – 수백 MPa** | p. 675 | 10 Wang 2020 *Nat. Commun.* 11, 5201 · 20 · 22 · 36 Lee 2022 *Joule* 6, 2547 | 10 📥 `wang2020_insitu_plating_*` · 36 📥 `lee2022_thin_li_void_rewetting_*` |
| 실용에서는 **> ~1 MPa 가 걸기 어렵다** | p. 675 | 37 | — |
| 무음극에서 **> 1 MPa 가 석출 Li 크리프를 촉진** (`Fig. 2c`) | p. 675 · `Fig. 2c` | 10 · 20 · 36 | 10 📥 · 36 📥 |
| Li 의 **점소성** → 옆으로 자라 공극을 메우고 밀착 유지 | p. 675 | 14 · 21 · 38 Lee C. 2021 *ACS Energy Lett.* 6, 3261 | 21 📥 |
| 고압 + 고온 사이클로 이 기전을 이용한 시도 | p. 675 | 39 · 40 Chang 2021 *Nat. Commun.* 12, 6369 | — |
| 지그 정렬 불량 · 계면 불균일 → **불균일 적층압** → 불균일 핵생성·성장 · **공칭 적층압 ≠ 국부 응력** | p. 675 | 14 | — |
| 섬이 합쳐질 때 석출 안 국부 응력이 시공간으로 변함 → 몰부피 (열역학) · 계면 반응속도 | p. 675 | 14 | — |
| **탄성층**으로 응력 분포 · Li 균일성 개선 | p. 675 | 14 · 43 Cao 2023 *Nano Lett.* 23, 9392 | — |
| 황화물 CC 접촉은 **~10–500 MPa 압착**으로 (제조) | p. 674 | 29 · 30 Lee 2020 *Nat. Energy* 5, 299 | — |
| 공극 완화 ↔ 침입 증가의 상충 (§4.2) | p. 677 | 78–80 | 79 ✅ |
| 적층압 · 온도로 박리 균일성을 높일 수 있지만, **무압 안정 박리**에는 Li 확산 조절 전략이 필요 | p. 677 | 81 · 24 · 29 · 30 · 82 | — |
| 인터레이어 = **zero or minimal (< 1 MPa)** 운전의 핵심 레버 | p. 678 | 37 · 81 | — |
| **저압 (< 1 MPa) 재료 거동 연구가 시급** · 고압 · 고온에선 다른 기전이 지배할 수 있다 | p. 678 (결론) | (인용 없음) | — |
| 조립 각 단계 압력의 **크기 · 지속시간** (펠릿화 · formation) 을 보고하라 | p. 679 | (권고 · 인용 없음) | — |
| 펄스 전착 · 온도 · 적층압 조절로 균일 석출 | p. 676 | 37 | — |

### 4.4 인터레이어 (Ag–C 등) ★

| 주장 | 쪽 · 그림 | 인용 1 차 출처 | litdb |
|---|---|---|---|
| 맨 CC · 상온 · 무압 석출/박리는 어렵다 → 나노–마이크로 인터레이어가 핵생성 · 성장 · 사이클을 바꾼다 (질량·부피 증가 최소) | p. 677 | (서술) | — |
| ★ 인터레이어는 **새 계면 둘 (CC\|인터레이어 · 인터레이어\|SSE)** 을 만든다 — 각자의 영향은 따로 풀어야 한다 | p. 677 | (서술) | — |
| 부류 = Li-rich 합금 · Li 화합물 · 둘의 조합 (`Table S3`) | p. 677 | 24 · 30 · 85 Müller 2024 *ACS AMI* 16, 695 | — |
| 이상적 인터레이어 = 충전 때 치밀·균일 Li 층 · 사이클 내내 구조 유지 (또는 박리 때 원 구조 회복) | p. 677 | (서술) | — |
| ★ **인터레이어의 SSE · CC 점착이 강해야** 접촉이 유지된다 | p. 678 | 86 Park 2022 *JMCA* 10, 21995 | — |
| 다공 탄소: 액체 Li 금속에서 먼저 (87) → 무음극 SSB 에서도 (88 · `Fig. 4a`) | p. 678 · `Fig. 4a` | 87 Martin 2020 *Joule* 4, 1296 · **88 Liao 2024 *JMCA* 12, 5990** | 88 — (후속 `liao2025_…` ✅) |
| 탄소 = **혼합 전자–이온 전도체** → 석출 때 탄소층 전체에서 Li 성장 · 박리 때 계면으로 확산 | p. 678 | 81 | — |
| 탄소는 상당한 석출 뒤에도 SSE 와 conformal 접촉 · SSE 와 자라는 Li 사이에 남아 접촉 유지 · 전류 집중 완화 | p. 678 | 89 Wu 2023 *Nano Lett.* 23, 1132 · 30 · 82 Kim J. S. 2023 *Nat. Commun.* 14, 782 · 90 Suzuki 2021 *Adv. Energy Sustain. Res.* 2, 2100066 | — |
| ★ **석출 위치 (CC\|탄소 vs 탄소\|SSE)** 를 계면에너지 · 기공 크기 · 탄소 종류로 바꿀 수 있다 | p. 678 | 86 · 90 | (점착 Γ 문턱 = `liao2025_…` ✅) |
| 탄소 안 Li 석출 동역학이 위치 · 형태에 영향 | p. 678 | 88 · 91 Kim S. 2023 *ACS Energy Lett.* 8, 9 · 92 Xie 2024 *AEM* 14, 2302960 | — |
| 순수 탄소 = 장기 사이클 제한 → 다른 재료 탐색 | p. 678 | 90 | — |
| ★ Li 합금 · 화합물 (Li₃Au · LiₓAg · Li₂Te) → **핵생성 과전압↓** · 공간 제어 → **순간 (instantaneous) 대신 연속 (continuous) 핵생성** → 균일층 | p. 678 | 85 · 93 Sandoval 2021 *JES* 168, 100517 · 94 Yan 2016 *Nat. Energy* 1, 16010 · 95 Wang Y. 2023 *Adv. Mater.* 35, 2206762 | — |
| 액체에서 먼저 보고 → 고체–고체에서도 이점 | p. 678 | 24 · 29 · 95 | — |
| 황화물 · 산화물에서 **100–150 nm Ag 또는 Au** → 균일 석출 | p. 678 | 24 Haslam & Sakamoto 2023 *JES* 170, 040524 · 29 | — |
| 처음 치밀한 **Au 막이 충전 중 입자로 쪼개져 Li 층에 흩어진다** → 인터레이어는 매우 동적 | p. 678 · `Fig. 4b` | 24 · 29 | — |
| Mg 인터레이어도 연구됨 | p. 678 | 96 Wang J. 2023 *Nano Res.* 16, 8338 | — |
| **Li₂Te**: Cu₂Te 표면막 + Li 의 전기화학 반응으로 석출 중 in situ 형성 · **구조 유지** (`Fig. 4c`) — 일부 금속 합금 (`Fig. 4b`) 과 대조 → 화학-역학 안정성 기대 | p. 678 · `Fig. 4c` | 95 | — |
| 여러 인터레이어가 균일 석출 + 효과적 박리 + **공극 완화** | p. 678 | 23 · 29 · 97 Thenuwara 2023 *ACS Energy Lett.* 8, 4016 | — |
| 단일 재료 인터레이어는 장기 효과 제한 → **Ag + C 복합이 1,000 사이클 넘게** | p. 678 · `Fig. 4d` | **30 Lee 2020 *Nat. Energy* 5, 299** · 82 | — (`Table S3` 9 행 · 같은 계 기전 `spencerjolly2023_…` ✅) |
| 친Li **Ag 나노입자 = CC 쪽 치밀 Li** · **탄소 = Li 수송 + SSE 접촉 유지** → 성분이 다른 역할을 나눈 설계 | p. 678 | (30 · 82 맥락) | (litdb 대조: `spencerjolly2023_…` 은 'Ag 는 CCD 를 안 올린다 · Ag 효과 = Li 층 균일화') |
| 다중 규모 모델링 · in situ/operando 로 설계 | p. 678 | (서술) | — |
| (결론) **SE 와 Li 양쪽에 붙는 인터레이어** = 저압 장기 사이클 전략 | p. 678 | (인용 없음) | — |

### 4.5 집전체 (CC) ★

| 주장 | 쪽 · 그림 | 인용 1 차 출처 | litdb |
|---|---|---|---|
| 무음극 = **완전 리튬화 (방전) 양극** (예 LiNi₀.₈Co₀.₁Mn₀.₁O₂) + **과잉 Li 없는 CC** · Li 는 충전 때 CC 에 석출 · 방전 때 박리 | p. 674 · `Fig. 1b` | (서술) | — |
| 첫 충전 석출 = **이질 CC (Cu 박)** 위 핵생성·성장 · CC\|SSE 국부 화학-역학 환경이 균일성 · 형태를 정한다 | p. 674 | 25 Yoon 2024 *ACS AMI* 16, 18790 | — |
| SSE\|CC 화학-역학 상호작용 → 첫 핵생성 · 이후 성장 (`Fig. 2a`) | p. 674 · `Fig. 2a` | 28 Motoyama 2015 *JES* 162, A7067 | — |
| CC 구속에서 오는 응력 → Li 소성 변형 → 형태 | p. 674 | 14 | — |
| ★ 변형시킬 과잉 Li 가 없으니 **첫 핵생성은 CC–SSE 접촉 영역에서만** — 접촉 형성 · **SSE–CC 점착력**이 핵심 | p. 674 | 10 · 14 | 10 📥 |
| 접촉 형성: 황화물 압착 ~10–500 MPa · LLZO 900 °C 접합 · 산업은 롤 압착 · 실험실과 산업 공정은 달라야 한다 | p. 674 | 29 · 30 · 10 · 31 Zaman & Hatzell 2022 *Curr. Opin. Solid State Mater. Sci.* 26, 101003 | — |
| 석출 중 계면 응력 → **CC/SSE 박리 · CC 소성 변형 또는 파단 · SSE 균열** | p. 674 | (서술 · `Fig. 2a` K_c,SSE/CC) | — |
| ★ **얇은 CC** = 응력 축적 시 기계적 실패 → **비가역 용량 손실** | p. 676 · `Fig. 2e` | 16 Neudecker 2000 *JES* 147, 517 · 28 · 32 Fuchs 2023 *AEM* 13, 2203174 | 32 📥 `fuchs2023_cu_llzo_growth_*` |
| **두꺼운 CC** = 파단 없이 변형 견딤 → 옆 성장 · 균일 석출 · 그러나 SSE 응력 → 균열 · 필라멘트 · 질량·부피↑ → 에너지밀도↓ | p. 676 | 14 · 51 Cheng 2023 *Nat. Nanotechnol.* 18, 1448 · 52 | — |
| Cu 위 Li 석출은 **불균일**할 수 있다 → CE↓ · 수지상 | p. 676 | 10 · 23 · 29 | 10 📥 |
| ★ **DFT 는 Cu · Cu₂O 표면 둘 다 친Li 로 예측 · sessile drop 은 깨끗한 Cu 에서만 쉽게 젖는다** → Cu₂O 표면 산화막이 Li 와 자발 전환해 **Li₂O** 가 되고 Li 은 Li₂O 를 잘 못 적신다 → Cu 위 Li 는 **친Li (Cu) + 소Li (Li₂O) 혼재 기판**을 만난다 (`Fig. 2f`) · Li₂O 전환 = 비가역 용량 손실 | p. 676 · `Fig. 2f` | **25 Yoon 2024 *ACS AMI* 16, 18790** | — |
| 석출 Li 와 CC 사이 열역학 · 점착 · 젖음이 성장에 영향 | p. 676 | 25 | — |
| 앞으로: 석출 전 **CC 를 제어 전위에 두어** 계면상 형성 조절 · SSE 표면 조성 개질 · 얇은 '인공 SEI' · CC · SSE 계면 미세구조 공학 | p. 679 | (권고 · 폐루프 제어는 37) | — |
| `Table S2`: 에너지 산정의 CC = Cu 5 µm · Al 5 µm | SI p. 4 | — | — |

### 4.6 보조 축 — 핵생성 · 온도 · 계면상 · SE 미세구조 · CE

| 주장 | 쪽 · 그림 | 인용 1 차 출처 | litdb |
|---|---|---|---|
| 석출 **전류밀도가 핵 밀도**를 바꾼다 (`Fig. 2b`) | p. 674 · `Fig. 2b` | 10 · 32 | 10 📥 · 32 📥 |
| 고전류 → 과전압↑ → **핵 면밀도↑** | p. 674 | 33 Pei 2017 *Nano Lett.* 17, 1132 (⚠ **액체 전해질** 연구) | — |
| 전류 펄스 → 핵 밀도↑ | p. 674 | 32 | 32 📥 |
| 핵이 촘촘하면 미세 결정립 또는 두께 균일 Li 기대 — 그러나 Li 는 상온에서 **상동 온도 (homologous T) 가 높아 조대화** → 막지 않으면 큰 결정립 | p. 674 | (서술) | — |
| 미세구조 = CC 상호작용 + 석출 조건 (전류 · 온도) · 고전류 · 저온 · 불순물이 결정립을 줄일 수 있다 (연구 필요) · 사이클 간 '미세구조 기억' 은 불명 | p. 674–675 | 35 Singh 2023 *Matter* 6, 1463 | — |
| 고온 → SSE\|CC 계면으로 · 계면을 따라 Li 수송 가속 | p. 675 | 44 Wang M. 2019 *Electrochim. Acta* 296, 842 · 45 Luo 2022 *Int. J. Heat Mass Transf.* 199, 123450 · 46 Kinzer 2021 *Matter* 4, 1947 | — |
| 결정립 · 집합조직 → Li 역학 · 고온 크리프 · 확산 속도 변화 | p. 675 | 47 Lu 2023 *Extreme Mech. Lett.* 61, 102022 · 48 Hull & Rosenberg 1959 *Philos. Mag.* 4, 303 · 49 | — |
| 고온 → 핵 밀도 변화 · 소성↑ → **크리프 변형률 속도↑** (`Fig. 2d`) | p. 675 · `Fig. 2d` | 50 Motoyama 2020 *ACS AMI* 12, 38045 | — |
| 크리프가 미세구조 따라 확산에 의존 → 미세구조 제어로 크리프↑ 가능 | p. 678 | 98 Ruano, Miller, Sherby 1981 *Mater. Sci. Eng.* 51, 9 | — |
| SSE 마다 Li 전위 환원 안정성이 달라 **이질 계면상** (전기화학 · 역학 물성이 벌크와 다름) | p. 676 | 15 Davis 2021 *JES* 168, 070557 | — |
| **운동학적으로 불안정한 계면상** (LGPS · Li₃InCl₆ …) → 안정 Li 석출 없이 계속 환원 · **부동태 계면상** (LLZO) → Li 석출 가능 | p. 676 | 4 Krauskopf 2020 *Chem. Rev.* 120, 7745 · 17 Richards 2016 *Chem. Mater.* 28, 266 · 54 Zhu 2016 *JMCA* 4, 3253 · 55 Wenzel 2018 *Solid State Ion.* 318, 102 | 17 ✅ `richards2016_…` · 54 ✅ `zhu2016_…` |
| 계면상이 핵생성 불균일에 주는 영향 (Li/SSE 계면 에너지 지형) 은 **잘 모른다** | p. 676 | (서술) | — |
| SSE 미세구조 (결정립 · 밀도 · 거칠기) → 석출 Li 형태 (`Fig. 2g`) | p. 676 · `Fig. 2g` | 52 · 57 · 59 | — |
| SSE 결정립 크기 → 석출 · 박리 | p. 676 | 57 · 60 | — |
| 작은 SSE 결정립 (연마 안 하면 거칠기↓ 와 상관) → 첫 접촉 · 막 균일 · CC 계면 SSE 미세구조가 **환원 분해량**을 바꿈 → **젖음 ↔ SSE 반응성 연결** | p. 676 | 57 Wang Y. 2024 *AEM* 14, 2304530 (LPSCl 밀링) | — |
| **CE** 요구: 액체 · 고체 무음극 공통 · 평균 > 99.95 % (1,000 사이클) | p. 676 · `Fig. 3a,b` | 63 Liu 2019 *Nat. Energy* 4, 180 · 64 Xiao 2020 *Nat. Energy* 5, 561 · 37 | — |
| 액체 Li 금속 CE 대개 < 99.6 % | p. 676 | 65 Hobold 2021 *Nat. Energy* 6, 951 · 66 Sanchez & Dasgupta 2024 *JACS* 146, 4282 · 67 Jagger & Pasta 2023 *Joule* 7, 2228 | — |
| 일부 SSE 는 Li 와 화학 안정이 높아 CE 를 올릴 수 있다 · 무음극 SSB 의 CE 개선 사례 | p. 676 | 17 · 18 · 68 · 30 · 62 | 17 ✅ · 18 ✅ `xiao2020_…` · 68 ✅ `zhu2015_…` |
| 수백 사이클 안정 무음극 SSB 시연이 Li 과잉보다 **적다** · 사이클 프로토콜 표준 부재 | p. 676 | 23 | — |
| 무음극 액체 셀 = 사이클마다 SEI 계속 생성 · SSB = SEI 가 평면 계면에 갇힌다 → SSB 쪽이 '아마 더 유망' | p. 674 | 19 Lin 2017 *Nat. Nanotechnol.* 12, 194 · 17 · 18 | 17 ✅ · 18 ✅ |

---

## 5. 방법 ★ — 자체 계산 · 실험 없음 (슬롯은 'n/a' 로 명시)

### 5.1 DFT / 계산 슬롯 — 전부 n/a

| 슬롯 | 이 논문 |
|---|---|
| code / functional (+vdW) / pseudo · PAW / k · ecut / supercell · nat / DFT+U | **n/a** — 계산을 하지 않았다 |
| AIMD · MLIP · 무질서 처리 | **n/a** |
| 계산 관련 문장 | 단 하나 — *"First-principles calculations have predicted that both copper and Cu₂O surfaces are lithiophilic"* (p. 676 · ref 25) — 방법 · 수치 · 표면 모형 언급 없음 → **ref 25 원문으로 가야** W · 표면 · 범함수를 알 수 있다 |
| '다중 규모 모델링' | 필요하다는 당위 문장만 (p. 678) — 모델 · 매개변수 · 결과 0 |

### 5.2 SI 의 에너지밀도 산정 — 이 논문이 직접 낸 유일한 수치

- 도구: *"SSB energy density calculator published in supplementary reference 1"* = Wang · Kazyak · Dasgupta · Sakamoto, *Joule* 5, 1371 (2021) (본문 ref 37). 입력은 `Table S2` 전부 (§3.2).
- 셀 정의 (`Table S2` 로 읽은 것 · ✎ 재현으로 확인 §13-1): 단면 1 cm² 당 **Al CC 5 µm + 복합양극 + SE 분리막 20 µm + (Li 20 µm 또는 0) + Cu CC 5 µm** · 포장 · 탭 없음 · 부피는 **조립 (방전) 상태 두께** 기준 (충전 때 석출 Li 두께는 안 넣음 — 논문은 기준 상태를 적지 않는다).
- 복합양극 = CAM 75 vol % + SE 25 vol % (고체 기준) · 상대밀도 95 % → 두께 ✎ 75.9 µm.

### 5.3 `Fig. 4` 원 출처와 기법 (이 논문은 재수록만)

| 패널 | 원 논문 (본문 ref) | 기법 | 이 논문이 붙인 해석 |
|---|---|---|---|
| a | Liao 2024 *JMCA* 12, 5990 (88) — CC BY 3.0 | plasma FIB-SEM 단면 | 탄소층 안팎 Li 성장 (p. 678) |
| b | Sandoval 2023 *Joule* 7, 2054 (29) | cryo-FIB-SEM | 치밀 Au 막 → 입자로 흩어짐 = 동적 인터레이어 |
| c | Wang Y. 2023 *Adv. Mater.* 35, 2206762 (95) | 단면 cryo-FIB-SEM | Li₂Te 구조 유지 |
| d | Lee 2020 *Nat. Energy* 5, 299 (30) | 단면 SEM · SUS CC | Ag 는 CC 쪽 치밀 Li · 탄소는 SE 접촉 |

### 5.4 저자들이 요구하는 보고 항목 (p. 679) — 우리 실험 · 모델 등록 체크리스트로 쓸 수 있다

재료 처리 · **세척 단계** · **표면 거칠기 값** · **탄성층 또는 포장재 사용 여부** · **조립 각 단계 압력의 크기와 지속시간** (펠릿화 압력 · formation 압력). 이유: 계면 품질이 성능을 정하고, 접촉이 나쁘면 전류 집중 → 빠른 고장.

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나 · 본 그림) | 우리가 참고할 점 |
|---|---|---|
| 1a,b | Li 과잉 SSB (위에서 음극 CC / Li 박 / SE / 복합양극 / 양극 CC) vs 무음극 SSB (CC 가 SE 위에 바로) 도식 · 아래에 1,208 vs 1,435 Wh l⁻¹ | 셀 단위 형상 입력: SE 20 µm · 복합양극 ✎ ≈75.9 µm · Cu / Al 5 µm · Li 0 / 20 µm (`Table S2`). 부피는 조립 (방전) 상태 기준 |
| 2a | Li 석출 하나가 CC 를 렌즈 모양으로 들어 올린 단면 · 적층압 F (화살표 셋) · 매개변수 11 개 = t_CC · σ_Li (사방 압축 요소) · σ_CC (경사면 따라) · σ_SSE · γ_SSE/Li · γ_Li/CC · **K_c,SSE/CC (석출 가장자리, CC 가 SE 에서 떨어지는 선단)** · K_c,SSE (석출 아래 SE 로 파고드는 Li 쐐기) · d_SSE · V_LiΔG_V · 계면상 (빨강 · 분홍 · 청록 구 — **석출 아래에만**) | 연속체 · DEM 입력 체크리스트. γ ↔ DFT W (Dupré W = γ_A + γ_B − γ_AB) · K_c,SSE/CC ↔ CC\|SE 계면 G_c (석출이 자라려면 CC 를 벗겨야 한다 = 블리스터 문제) · K_c,SSE ↔ SE 파괴 (`song2025_…` K_Ic) · d_SSE ↔ DEM 입도 |
| 2b–g | 첫 성장 조건 여섯: b 전류 (저 = 성긴 큰 핵 · 고 = 촘촘한 작은 핵, 화살표 길이로 전류) · c 압력 (저 = CC 가 물결치고 Li 섬 사이 틈 · 고 = 연속 Li 층) · d 온도 (저 = 촘촘한 작은 핵 · 고 = 성긴 큰 핵 · 사이에 '?' 양방향 화살표) · e CC 두께 (얇음 = CC 가 찢어지고 Li 가 버섯처럼 솟음 · 두꺼움 = 균일층) · f 화학 불균일 (CC 아래 표면 산화막 + Li₂O 혹) · g SE 미세구조 (Li 가 거친 SE 표면을 따라감) | 정성 방향표 — 숫자 없음. e 는 **CC 를 변형 · 파단하는 판**으로 모델링하라는 근거. d 의 '?' = 방향 미확정 (본문도 '바뀔 수 있다' 만 씀) |
| 3a–d | 사이클 도식: a 첫 석출 뒤 균일 Li 층 → b 균일 박리 (CC 가 SE 위에 평평히 · 검은 화살표 a↔b = 장수명) · c 고전류 박리 → Li 층 아래 반원 공극들 → 확대 원: 남은 Li 층에서 SE 로 **쐐기형** 필라멘트 · d 불균일 박리 → **고립 Li 섬 + 섬 가장자리 공극** · CC 가 섬 사이로 내려앉아 SE 에 닿음 → 확대 원: CC–SE 접촉 옆에서 **입자 경계를 따라 지그재그** 필라멘트 (빨간 화살표 a↔c · a↔d = 열화) | 무음극 고유 고장 = 방전 끝 **접촉 면적 축소** (ref 23). 연속체 모델은 박리 말기 접촉 분율을 추적해야 한다 · CC 는 남은 Li 를 따라 휘는 순응층으로 그려져 있다 |
| 4a | 탄소 인터레이어 2 mAh cm⁻² PFIB-SEM (LPSCl · ref 88): 위에서 CC (밝음) / 두꺼운 Li / Carbon (결이 보이는 층) / LPSCl | **Li 가 CC 와 탄소 사이에** 있다 (CC 쪽 석출 · `liao2025_…` 의 고 Γ 경우와 같은 꼴). figure-read ≈ Li 7.8 µm (치밀 기대 9.8 µm 의 0.8) |
| 4b | Au 100 nm 를 입힌 Cu 위 1 mAh cm⁻² cryo-FIB-SEM (ref 29): CC (결정립 대비) / 'Au' 밝은 입자 띠 / Li (검정) / 밝은 입자 띠 / SSE | Au 가 입자로 쪼개져 **CC\|Li · Li\|SSE 두 경계에 띠로** 보인다 — Li 층 가운데는 비어 보인다 (figure-read · 본문 *"distributed throughout"* 과 결이 다름 → §10-④). figure-read ≈ Li 4.8 µm (기대 4.9 µm) |
| 4c | Cu₂Te 인터레이어 3 mAh cm⁻² cryo-FIB-SEM (ref 95): CC / 얇은 Li₂Te–Cu 층 / Li / SSE | 화합물층은 **CC 에 붙은 채** 남고 Li 는 그 아래 (SE 쪽) 로 자란다. figure-read ≈ Li 12.5 µm (기대 14.7 의 0.85). ⚠ **석출 1 회 뒤** 단면 — '사이클 중 구조 유지' 의 직접 증거는 아니다 (§10-⑤) |
| 4d | Ag–C 인터레이어 5 mAh cm⁻² 단면 SEM (SUS CC · ref 30): 위에서 SSE / Ag–C / 밝은 얇은 선 / 'Li deposits' / SUS (방향이 a–c 와 반대) | Li 는 **Ag–C 아래 SUS 쪽** · Ag–C 는 SSE 에 붙어 남는다 → 점착 트랙 '어느 계면이 벌어지나' 의 그림 근거 (Ag–C\|SE 유지 · Ag–C\|CC 사이로 Li). figure-read ≈ Li 24 µm (기대 24.4 µm) · 밝은 선의 정체는 캡션에 없음 |
| S1 | 부피 에너지밀도 막대 (Wh/L): Li-ion ≈784 · Li Excess ≈1,208 · **Reservoir Free** ≈1,436 | 막대 한 벌 = LPSCl · LLZO 공통 (부피는 SE 밀도와 무관). SI 는 무음극을 'Reservoir Free' 로 표기 |
| S2 | 중량 에너지밀도 막대 (Wh/kg): ≈290 · ≈464 · ≈479 | **LPSCl 값만** 그림 (LLZO 329 · 337 은 `Table S1` 에만) · 무음극 이득 +3 % 가 눈으로도 보인다 |
| Table S1 | 에너지 지표 5 행 (Li-ion · LPSCl/LLZO × Li 과잉/무음극) | `Table S2` 로 ✎ 재현 (§13-1) · 1436 vs `Fig. 1` 1,435 |
| Table S2 | 산정 입력 전부 (양극 4 mAh cm⁻² · 200 mAh g⁻¹ · CC 5 µm · SE 20 µm · Li 0/20 µm · LPSCl 1.64 g cm⁻³ · 상대밀도 90 % …) | **LPSCl 1.64 g cm⁻³ 무인용** = litdb '진밀도 1.64' 묶음의 또 한 자리 · 셀 형상 입력 |
| Table S3 | 인터레이어 16 행 (종류 · 두께 · 제법 · 전해질 · CC · SI ref) | 두께 4 nm – 13 µm · 성능 지표 없음 → 순위표 아님. LPSC 계 행 1 · 3 · 9 · 10 · 11 · 15 만 우리 계 |

### 6.1 크롭 색인 — `litdb/figures/sandoval2025_electro_chemo_mechanics_anode_free_ssb/`

| 파일 | 원 그림 | PDF 쪽 | 크기 (px, 300 dpi) | 손작업 | Read 로 봤나 |
|---|---|---|---|---|---|
| `fig_1.png` | 본문 Fig. 1 | 2 | 1084 × 447 | **손 크롭** (도구가 '영역 없음' 으로 건너뜀) | ✅ |
| `fig_2.png` | 본문 Fig. 2 | 3 | 2115 × 1496 | **재크롭** (위 라벨 줄) | ✅ |
| `fig_3.png` | 본문 Fig. 3 | 5 | 2190 × 1153 | **재크롭** (전폭 — 도구는 왼쪽 단만) | ✅ |
| `fig_4.png` | 본문 Fig. 4 | 6 | 2224 × 516 | **재크롭** (패널 제목 줄) | ✅ (+ 픽셀 단면 판독 §3.6) |
| `fig_S1.png` | SI Figure S1 | SI 3 | 1961 × 741 | — | ✅ |
| `fig_S2.png` | SI Figure S2 | SI 3 | 1946 × 766 | — | ✅ |
| `tab_S1.png` · `tab_S2.png` · `tab_S3.png` | SI 표 | SI 3 · 4 · 5 | — | — | ✗ (PDF 텍스트로 읽음) |

### 6.2 그림별 실독 메모

**6.2-1 `Fig. 1`** — 두 셀 단면 도식. (a) 맨 위 주황 음극 CC · 남회색 'Lithium foil' · 노란 SE 입자층 · 남회색 (활물질) + 노랑 (SE) 이 섞인 'Composite cathode' · 아래 'Positive current collector'. (b) 주황 CC 가 노란 SE 위에 **바로** 놓이고 Li 층이 없다. 두께 눈금 없음 — 상대 두께도 정량 아님. 숫자는 그림 아래 두 줄 (1,208 · 1,435 Wh l⁻¹) 뿐.

**6.2-2 `Fig. 2`** — (a) 가 이 논문의 '모델 그림' 이다. 확인한 것: ① 적층압 F 는 CC 윗면 세 화살표로만 들어온다 (Li 섬 위만 누르는 꼴 — 섬 아닌 곳의 CC 는 SE 에 닿아 있다) ② σ_Li 는 네 방향 압축 화살표를 단 정육면체 요소 ③ **K_c,SSE/CC 화살표가 석출 오른쪽 끝 (CC 가 SE 에서 떨어지기 시작하는 곳)** 에 수평으로 그려져 있다 — 석출 성장 = CC\|SE 계면 균열 전파 ④ K_c,SSE 는 석출 아래 SE 안으로 비스듬히 파고든 회색 쐐기 (필라멘트) 옆 ⑤ 계면상 색 구는 석출 바닥 (Li\|SE) 에만, 맨 CC\|SE 에는 없다 (SEI 가 Li 접촉 면에만 생긴다는 그림). (b)–(g) 는 §6 표 그대로 — 축 · 눈금 · 수치 없음.

**6.2-3 `Fig. 3`** — 도구 크롭은 왼쪽 단 (a 와 화살표) 만이었다 → 전폭 재크롭으로 b · c · d 와 확대 원 둘을 살렸다. c 의 공극은 Li 층 바닥 (Li\|SE) 에 반원으로 · d 의 섬 가장자리 공극은 **섬과 CC 접촉 경계 바로 옆**에 그려져 있다. CC 는 c · d 에서 물결 모양 (남은 Li 를 덮고 휜다). 화살표 색 범례는 캡션에만 (검정 = 이상 · 빨강 = 열화).

**6.2-4 `Fig. 4`** — 네 단면 모두 원 논문 재수록. 방향 주의: **a–c 는 CC 가 위 · d 는 SSE 가 위**. 층 순서 (위 → 아래): a CC / Li / Carbon / LPSCl · b CC / Au 입자 / Li / 밝은 입자 띠 / SSE · c CC / Li₂Te–Cu / Li / SSE · d SSE / Ag–C / 밝은 선 / Li deposits / SUS. ⇒ **탄소 계열 (a · d) 은 인터레이어가 SE 에 붙어 남고 Li 가 CC 쪽에** · **금속 · 화합물 계열 (b · c) 은 시드가 CC 쪽에 남고 Li 가 그 아래 SE 쪽에** 선다 (b 는 SE 쪽에도 입자 띠). 이 대비는 본문이 명시적으로 정리하지 않았다 (우리 판독). 두께 판독 §3.6.

**6.2-5 `Fig. S1` · `Fig. S2`** — 단순 막대 (Origin 풍 · 무늬 채움). 값은 `Table S1` 과 같다 (figure-read ≈ 눈금 대조). `Fig. S2` 는 LPSCl 경우만이라는 것을 그림이 말하지 않는다.

---

## 6b. Post-processing ★

- **무엇**: 없음 (NEB · Bader · COHP · DOS · grand-potential · ELF … 0). 관점 논문.
- **도구**: SI 에너지밀도 = 문헌 계산기 (SI ref 1). `Fig. 4` 는 원 논문 그림 재수록 (CC BY 3.0 · Elsevier · Wiley · Springer Nature 허락).
- **수치화 · 기록**: `Table S1` (5 행) · `Table S2` (입력) · `Table S3` (16 행 목록). 오차 · 불확도 없음.
- **우리가 한 것**: `Table S2` → `Table S1` 손 재현 (§13-1) · `Fig. 4` 픽셀 단면 판독 (§3.6).

---

## 7. 우리 대비 ★ — 수치 비교는 거의 없고, **출처 · 틀 · 입력표**를 준다

> ⛔ 우리 점착 (W) 값은 이 digest 에 싣지 않는다 — **위치만**. 문헌 수치는 소환값이고 우리 db 절대값과 섞지 않는다.

### 7-1. 우리 DFT 기준선 (comp1 / modelc · `../our_dft_baseline.md`) 대비

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 이온전도도 σ · Ea | n/a | MLIP-MD (상대차 정책) | 비교 대상 없음 |
| 산화 onset / ESW (양극 쪽) | n/a (양극 쪽 서술 없음) | grand-potential (`our_dft_baseline.md` ESW 표) | 비교 대상 없음 |
| **환원 (Li 쪽)** | LPSCl 은 Li 와 (전기)화학 반응해 **환원 분해**되고 Li · SE 미세구조를 바꾸며 SE 수축이 공극을 낼 수 있다 (refs 56–58) · LGPS · Li₃InCl₆ = 운동학적으로 불안정 vs LLZO = 부동태 (refs 4 · 17 · 54 · 55) | grand-potential 환원 가장자리 (`our_dft_baseline.md` ESW 표 · ⚠ 창 폭 · 라벨은 `HZ-esw-reduction-limit-label` CONDITIONAL — 폭 인용 금지) | **같은 방향 (정성)** — Li 금속 전위의 LPSCl 은 열역학적으로 환원된다. 이 논문은 수치 · 생성물 · 부동태 여부를 말하지 않는다 → 정성까지만 |
| 기계 (E · B · G · C_ij) | n/a — `Fig. 2a` 에 σ_SSE · K_c,SSE **기호만** | DFT 탄성 (`our_dft_baseline.md` E_VRH · B₀ 행) | 수치 비교 대상 없음. K_c 는 우리 DFT 가 내지 않는 양 (실측 = `song2025_…`) |
| 전자구조 (gap) | n/a | fixed-occ nscf gap (canonical) | 비교 대상 없음 |
| 점착 W | 'DFT 가 Cu · Cu₂O 둘 다 친Li 로 예측' (ref 25 요약) 한 문장 · 값 없음 | W_ad 보고서 §2 (값 — 여기 안 싣는다) · §7 (Li 친화성 제안) | 같은 양을 비교할 값이 이 논문엔 없다 → ref 25 를 먹이면 Li\|Cu · Li\|Cu₂O · Li\|Li₂O 의 문헌 W 가 들어온다 (§8 ①) |

### 7-2. ★ W_ad 보고서 §7 (Li 친화성 · 점착과 공극 · 인터레이어) 에 쓸 점 — **위치만**

보고서 = `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` (§2 쌍별 값 · §7 Li 친화성 정량화 제안 · §7-1 대상 표면).

| 보고서 자리 | 이 논문이 주는 것 | 쪽 · 그림 (봤나) | 1 차 출처 |
|---|---|---|---|
| §7 서두 — 친Li / 소Li 정의 | 같은 어휘 · 'Li 가 쉽게 적시는가' 를 sessile drop 젖음과 **핵생성 과전압**으로 판정하는 실험 쪽 쓰임 | p. 676 · 678 | 25 · 85 · 93–95 |
| §7 방법 1 · 2 (Li 원자 흡착 · Li 금속\|재료 W → Young–Dupré θ) | ★ **명목 표면으로 계산한 친Li 판정이 실험과 어긋난 실례**: Cu₂O 는 DFT 로 친Li 인데 Li 와 닿는 순간 Li₂O 로 전환 → 소Li. ⇒ W 를 **반응 뒤 표면**에서도 내야 한다 (보고서 §7-1 의 'LiC₆ · Li–Ag 합금 면' 칸과 같은 원칙의 문헌 근거) | p. 676 · `Fig. 2f` (✅) | 25 |
| §7 방법 3 (합금 · 반응 구동력) | Li₃Au · LiₓAg · Li₂Te 가 **핵생성 과전압을 낮춰 순간 대신 연속 핵생성** → 균일층 · Au 막은 충전 중 입자로 쪼개짐 (동적) · Li₂Te 는 유지 → '합금이 생기는 재료' 와 '화합물로 남는 재료' 를 같은 W 잣대로 견주면 안 된다는 보고서 서술과 맞다 | p. 678 · `Fig. 4b,c` (✅) | 85 · 93–95 · 24 · 29 |
| §7 '할 수 없는 것' (산화막 · SEI 가 덮인 실제 표면) | 그 한계가 **Cu 에서 실제로 결론을 뒤집는다**는 근거 · 계면상이 핵생성 불균일에 주는 영향은 아직 모른다 (p. 676) | p. 676 | 25 · (서술) |
| §7 '쓰는 곳' (Ag/C 층 안에서 Li 가 어디에 먼저 붙나) | 석출 위치 (CC\|탄소 vs 탄소\|SSE) 가 **계면에너지 · 기공 크기 · 탄소 종류**로 바뀐다 · Ag–C 에선 Ag 가 CC 쪽 치밀 Li · 탄소가 SE 접촉 유지 · 단면 실례 둘 (탄소 · Ag–C 모두 **Li 가 CC 쪽**) | p. 678 · `Fig. 4a,d` (✅) | 86 · 90 · 30 · 82 · 88 |
| §7-1 대상 표면 표 | **CC 면 (Cu · SUS + 그 산화막) 이 표에 없다** — Ag–C 무음극 셀에서 Li 가 서는 곳이 CC 쪽 (`Fig. 4d`) 이고 Cu 산화막이 소Li 로 바뀌는 사례 (`Fig. 2f`) 가 있으므로 후보에 넣을 근거 | p. 676 · `Fig. 2f` · `Fig. 4d` (✅) | 25 · 30 |
| (새 절 후보) **점착과 공극** | 점착 · 젖음 조절 = **저압 안정 사이클의 핵심** · **점착과 Li 내부 응력은 얽혀 있다** · Li 와 계면상 · 이질 CC 사이 점착이 접촉 상실 동역학을 바꾼다 · 방전 끝 접촉 면적 축소 기전 | p. 676 · 677 · 678 · `Fig. 3d` (✅) | 53 · 74 · 23 |
| (새 절 후보) **인터레이어** | 인터레이어 = **새 계면 둘 (CC\|IL · IL\|SSE)** · IL 의 SSE · CC 점착이 강해야 · 결론의 'SE 와 Li 양쪽에 붙는 인터레이어' → W 쌍 목록에 **Li\|IL · CC\|IL** 이 있어야 석출 위치 질문에 답한다 (보고서 §2 쌍은 C–C · Ag–C · LPSCl\|Ag · LPSCl\|흑연) | p. 677 · 678 | 86 · (결론 · 인용 없음) |

### 7-3. ★ 연속체 · DEM 모델에 바로 쓸 점

| 우리 모델 자리 | 이 논문이 주는 것 | 쪽 · 그림 (봤나) | 비고 |
|---|---|---|---|
| 입력 체크리스트 | `Fig. 2a` 의 11 개: t_CC · σ_Li · σ_CC · σ_SSE · γ_SSE/Li · γ_Li/CC · K_c,SSE/CC · K_c,SSE · d_SSE · V_LiΔG_V · 계면상 | `Fig. 2a` (✅) | 우리가 채울 수 있는 칸 = γ (DFT, Dupré) · d_SSE (DEM 입도) · K_c,SSE/CC 의 **하한** (W ≤ G_c) — K_c 자체는 실측 (`liao2025_…` 류) 이 필요 |
| 압력 단계 등록 | 제조 **10–500 MPa** (황화물 CC 접촉) · 실험실 운전 **1 – 수백 MPa** · 실용 **< 1 MPa** · **> 1 MPa 크리프** | p. 674–675 · 678 · `Fig. 2c` (✅) | DEM 압밀 단계와 운전 스택 단계를 다른 압력으로 (`doux2020_stack_pressure_assb` 와 같은 결) |
| CC 경계조건 | 얇은 CC = 파단 · Li 분출 · 두꺼운 CC = 균일 · CC 는 남은 Li 를 따라 휜다 | p. 676 · `Fig. 2e` · `Fig. 3c,d` (✅) | CC 를 강체 벽이 아니라 **휘고 찢어지는 판**으로 · 두께 5 µm (`Table S2`) |
| 석출 성장 = 계면 균열 | 석출 가장자리에 K_c,SSE/CC — Li 섬이 커지려면 CC 를 SE 에서 벗겨야 한다 | `Fig. 2a` (✅) | 블리스터 (박막 들뜸) 문제로 놓을 자리 · 구동력 = 적층압 대 V_LiΔG_V |
| 방전 끝 접촉 분율 | 고립 Li 섬 → 기하 접촉 면적↓ → **낮은 전체 전류에서도 국부 고전류** | p. 676–677 · `Fig. 3d` (✅) | DEM 의 SE 표면 지형 (d_SSE · 거칠기 `Fig. 2g`) → 접촉 분포 → 전류 분포 모델로 넘길 자리 (제안 · 아직 안 함) |
| 석출 Li 형상 | 치밀 Li **4.89 µm per mAh cm⁻²** (✎) · `Fig. 4` 로 0.8–1.0 배 (figure-read) | §3.6 · §13-2 | 석출층 두께를 석출량에서 바로 놓아도 자릿수는 맞다 |
| 셀 형상 | SE 20 µm · 복합양극 ≈75.9 µm (✎) · CC 5 µm · Li 0 / 20 µm | `Table S2` (✗ 이미지 · 텍스트로) | 셀 단위 모델 기본값 후보 (출처 = 이 SI) |
| 적층압 상충 | 고압 = 공극↓ · 침입↑ | p. 677 | 압력 스윕을 하면 두 지표를 같이 낸다 |
| Li 역학 | 크기 의존 항복 (refs 41 · 42) · 크리프 (> 1 MPa) · 결정립 · 온도 | p. 675 | Li 를 단일 항복응력 탄소성체로 두면 섬 크기 효과를 놓친다 |

### 7-4. litdb 이웃 카드와의 관계

- `liao2025_interfacial_adhesion_li_plating_carbon_interlayer` ✅ — 이 논문 ref 88 (Liao 2024) 의 후속 · `Fig. 4a` 와 같은 탄소 인터레이어 계열. 이 논문이 '계면에너지 · 기공 · 탄소 종류' 로만 말한 **석출 위치**를 **점착 Γ 문턱**으로 정량한 편 (Liao 는 이 논문 공저자). 실용 G_c 부류 — W_ad 와 같은 줄 금지 (그 카드 규율 그대로).
- `spencerjolly2023_ag_graphite_interlayer_operando_xrd` ✅ — SI ref 12 · `Table S3` 11 행 · Ag–C 운전 중 상 변화 (흑연이 먼저 Li 를 받고 Li–Ag 합금으로). ⚠ `Table S3` 의 CC 'Cu' vs 그 카드의 분무 기판 '스테인리스'.
- `doux2020_stack_pressure_assb` ✅ — ref 79 · 적층압 딜레마 (공극↓ · 침입↑) 의 한 축 · 제조 / 운전 압력 구분.
- `song2025_porous_argyrodite_modulus_fracture_toughness` ✅ — `Fig. 2a` K_c,SSE 칸의 LPSCl 실측 출처 (값은 그 카드에서).
- `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` ✅ — SE 쪽 DFT 이상 벽개 · 필라멘트 (`comparison_vs_ours_DEM.md` §I-6).
- `zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector` ✅ — 무음극 · 변형되는 Na CC · 저압 0/1/4 MPa 운전 실측 — 이 논문의 'CC 공학 · 저압' 과제의 사례.
- `kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode` ✅ — Ag–C + 다공 CNF · operando 하중 셀 ΔP — 이 논문의 '탄성층 · 내부 압력 조절' (refs 14 · 43) 과 같은 질문.
- `ahn2026_cej_agno3_pvp_li3n_anodefree` ✅ (자체 · 미출판 투고본) — 무음극 · 전구체 전환으로 핵생성 + 수송을 함께 조절 — 이 논문 §4.4 '합금 · 화합물 인터레이어 · 핵생성 과전압' 틀 안에 놓이는 원고.
- 서론 · 계면 안정 인용 중 litdb 에 있는 것: `famprikis2019_…` (ref 2) · `janek2016_…` (6) · `richards2016_…` (17) · `xiao2020_…` (18) · `zhu2016_…` (54) · `zhu2015_…` (68).

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

### ① ★★★ W_ad 보고서 §7 의 '반응 뒤 표면' 원칙에 문헌 근거 한 줄 — Cu₂O → Li₂O (p. 676 · ref 25 · `Fig. 2f`)
명목 표면 (Cu₂O) 의 DFT 는 친Li 인데 실측은 소Li 다 — Li 와 닿아 Li₂O 로 바뀌기 때문이다. 보고서 §7-1 의 'LiC₆ · Li–Ag 합금 면' 칸은 이 원칙과 같고, **CC 면 (Cu · SUS + 산화막 → Li₂O) 을 후보에 더할 근거**가 된다. 정량 비교에는 ref 25 (Yoon 2024 *ACS AMI*) 원문이 필요하다 — (d) 추천 1 순위.

### ② ★★ '어디에 Li 가 서나' 는 W 쌍 목록을 바꾼다 (`Fig. 4a,d` · p. 677–678)
탄소 · Ag–C 단면 모두 Li 가 **CC 쪽 (인터레이어 아래)** 에 섰다. 석출 위치를 묻는 계산이라면 보고서 §2 의 쌍 (C–C · Ag–C · LPSCl\|Ag · LPSCl\|흑연) 만으로는 부족하고 **Li\|Ag (또는 Li–Ag 합금) · Li\|흑연 (LiC₆) · CC\|인터레이어** 가 같은 잣대로 있어야 한다 (이 논문의 '새 계면 둘').

### ③ ★★ `Fig. 2a` = 연속체 · DEM 입력표
11 개 중 우리가 채울 수 있는 칸: γ (DFT) · d_SSE (DEM) · K_c,SSE/CC 의 하한 (W ≤ G_c). 석출 가장자리의 K_c,SSE/CC 는 '석출 성장 = CC\|SE 계면 균열' 이라는 그림 — DEM 박리 시험 (`comparison_vs_ours_DEM.md` §I) 이 재려는 G_c 와 같은 양 부류다.

### ④ ★★ 압력 층위 셋을 등록 칸으로
제조 10–500 MPa · 실험실 1 – 수백 MPa · 실용 < 1 MPa. DEM 압밀과 운전 스택 단계를 다른 압력으로 등록하는 근거 (doux2020 카드와 같은 결) — 'stack pressure' 한 단어로 묶지 않는다.

### ⑤ ★ 방전 끝 접촉 면적 축소 (`Fig. 3d` · ref 23) — 우리 모델이 아직 안 하는 것
임계 박리 전류 (Li 과잉 셀 개념) 만으로는 무음극 고장을 못 잡는다. DEM 이 주는 실접촉 면적 분포를 전류 분포 모델의 입력으로 쓰면 '낮은 전체 전류에서도 국부 고전류' 를 정량화할 자리가 생긴다 (제안).

### ⑥ ★ LPSCl 환원의 '수축' (p. 676 · refs 56–58) — 우리 DFT 로 가를 수 있는 질문
반응 부피 (LPSCl + Li → Li₂S + Li₃P + LiCl) 를 **같은 방법의 부피**로 계산하면 '수축' 이 SE 부피 기준인지 (SE + 소모 Li) 기준인지 가를 수 있다 (제안 · 값 없음 · 이 논문은 계산하지 않았다).

### ⑦ `Table S2` 의 LPSCl 1.64 g cm⁻³ — 1.64 출처 묶음의 또 한 자리 (메인 세션 판단)
Nat. Mater. 관점 논문의 SI 가 출처 없이 1.64 를 썼다 (상대밀도 90 % 와 함께). 결정 밀도 ≈1.86 이면 중량 에너지밀도 −2.4 % (✎ §13-6).

### ⑧ 석출 Li 두께 환산 4.89 µm per mAh cm⁻² (✎ §13-2)
`Fig. 4b,d` 단면과 맞고 (0.99) a · c 는 0.80 · 0.85 (기울기 보정 미상). 모델에서 석출층을 치밀 Li 로 놓는 가정의 자릿수 근거.

---

## 9. 인용 가능 문장 (deck / paper 용 · 영어 · 랩 출처 표기)

- "In anode-free solid-state batteries, the first Li nuclei can form only where the current collector contacts the solid electrolyte, so contact formation and interfacial adhesion govern initial plating (*Nat. Mater.*, 24, 673 (2025))."
- "Without a Li reservoir, anode-free cells require average Coulombic efficiencies above 99.95% to reach 1,000 cycles (*Joule*, 5, 1371 (2021))."
- "Near the end of stripping, non-uniform Li removal leaves isolated Li domains, and the shrinking contact area concentrates current even at low global current densities, which accelerates voiding and subsequent filament growth (*Adv. Energy Mater.*, 13, 2204186 (2023))."
- "First-principles calculations predict both Cu and Cu₂O surfaces to be lithiophilic, whereas sessile-drop measurements show facile wetting only on pristine Cu, because Cu₂O converts to poorly wetted Li₂O on contact with Li (*ACS Appl. Mater. Interfaces*, 16, 18790 (2024))."
- "Contact between sulfide electrolytes and current collectors is typically formed by pressing at about 10–500 MPa, whereas stack pressures above about 1 MPa are difficult to apply in practical cells (*Nat. Mater.*, 24, 673 (2025))."
- "Composite Ag–C interlayers have enabled stable cycling beyond 1,000 cycles in anode-free cells, with Ag promoting dense Li deposition at the current collector and carbon maintaining contact with the electrolyte (*Nat. Energy*, 5, 299 (2020); *Nat. Commun.*, 14, 782 (2023))."
- ⚠ 숫자 문장은 1 차 출처를 같이 단다 — 이 관점 논문만 달면 2 차 인용이다.

---

## 10. 주의 / 한계 (over-claim 방지) — 비판적으로

① **자체 데이터 0.** 정량은 전부 2 차다. 문장 다수가 *may · could · probably · is expected* 다 (관점 논문이라 당연하다). 이 논문만 달고 숫자를 쓰면 2 차 인용이 된다 → §4 의 1 차 출처를 같이 단다.

② **근거가 컨소시엄 자기 연구에 쏠려 있다.** 참고문헌의 보이는 저자 이름만 세어도 공저자가 든 편이 **≥ 27 / 98** (✎ · et al. 뒤는 못 셈 · Wang Y. 2 편은 동명 가능성). 관점 논문에 흔한 꼴이라 편향이라고 단정하지는 않는다 — 다만 '무음극 고유 공극 기전' (ref 23 · 같은 그룹 계열로 보임 · 미확인) 처럼 핵심 주장 하나가 한 편에 기대는 자리는 독립 재현을 따로 찾는다.

③ **`Fig. 2` · `Fig. 3` 은 정성 도식이다.** 특히 `Fig. 2d` 는 고온 = 성긴 큰 핵으로 그렸지만 본문은 '핵 밀도가 바뀔 수 있다' 만 쓰고 방향을 정하지 않는다 (그림에도 '?'). `Fig. 2b` 의 방향 (고전류 = 촘촘한 핵) 은 ref 32 (Cu\|LLZO) · ref 10 과 **ref 33 (액체 전해질 나노 핵생성)** 에 기댄다 — 고체 계면 증거는 32 · 10 쪽이다.

④ **`Fig. 4b` ↔ 본문.** 본문: *"an initially compact gold film transforms into particulates distributed throughout the lithium layer during cell charging"*. 그림 (figure-read): 밝은 입자 띠가 **CC\|Li · Li\|SSE 두 경계**에 몰려 있고 Li 층 가운데는 어둡다 — 'throughout' 보다 '양쪽 경계로 갈라짐' 에 가깝게 보인다 (단면 한 장 · 원 논문 ref 29 미확인).

⑤ **`Fig. 4c` ↔ 본문.** 본문: *"The Li₂Te interlayer remains structurally intact during electrochemical cycling (Fig. 4c)"*. 캡션은 **'3 mAh cm⁻² 석출 뒤'** 단면이다 → 사이클 뒤 유지의 직접 증거가 아니다 (ref 95 에 사이클 뒤 단면이 있을 수 있음 — 미확인).

⑥ **`Fig. 4a` ↔ 본문.** 본문은 탄소가 *"promotes lithium growth throughout the carbon layer during plating"* 라고 쓰고 ref 81 (CNT) 을 단다. 같은 문단이 가리키는 `Fig. 4a` (ref 88) 는 Li 가 **CC 와 탄소 사이 치밀층**이다. 뒤 문장이 '석출 위치는 바뀔 수 있다' (refs 86 · 90) 고 덧붙이지만, 그림과 문장이 다른 거동을 가리키는 채로 놓여 있다 — 우리 점착 트랙은 그림 쪽 (CC 쪽 석출 · `liao2025_…` 와 같은 꼴) 을 따른다.

⑦ **에너지밀도의 숨은 가정.** (i) 'Li 과잉' = 20 µm (✎ 양극 용량의 1.02 배) — 가벼운 과잉이라 무음극 이득을 작게 잡은 쪽이다 (ii) 부피 = **조립 (방전) 상태 두께** — 충전 상태 두께 (석출 Li ✎ 19.6 µm 포함) 로 하면 무음극 ✎ ≈1,212 Wh L⁻¹ (§13-5) · 논문은 기준 상태를 적지 않는다 (iii) **중량 이득 +3 %** — 초록의 'high energy densities' 는 주로 부피 이야기다 (iv) LPSCl 밀도 1.64 g cm⁻³ 무인용 (v) 포장 · 탭 · 바인더 · 도전재 없음 (vi) SE 분리막 20 µm 는 목표 셀 가정이다 (근거 미기재) (vii) `Fig. 1` 1,435 vs `Table S1` 1436 (버림 vs 반올림).

⑧ **'CE > 99.95 % 로 1,000 사이클' 의 수명 끝 기준이 없다.** CE^N 모형이면 0.9995¹⁰⁰⁰ = 0.61 (✎ §13-7) — 80 % 잔존이면 99.978 % 가 필요하다. 인용할 때 기준을 같이 쓴다.

⑨ **'> 1 MPa 에서 크리프 촉진' 을 물리 문턱으로 읽지 않는다.** 크리프는 응력 · 온도 · 시간의 연속 함수다. 1 MPa 는 인용 연구들 (10 · 20 · 36) 의 조건에서 나온 경험 표현이다. 마찬가지로 '실용 > ~1 MPa 어려움' (ref 37) 도 공학 판단이지 재료 상수가 아니다.

⑩ **점착을 핵심으로 내세우면서 점착 수치가 하나도 없다** (W · G_c · Γ 0 건) · '다중 규모 모델링' 은 당위 문장뿐이다. ⇒ 우리 W_ad · DEM 이 채울 자리이고, 이 논문을 W · G_c 값의 출처로 쓸 수 없다.

⑪ **참고문헌 표기 오류 · 의심 (PDF 에 보이는 것)**: ref 36 저자 줄 *"Lee, K., Kazyak, E., Wang, M. J., Neil, P. & Sakamoto, J."* — 'Neil, P.' 는 Dasgupta, N. P. 의 오기로 보인다 · ref 75 제목 *"interfacial void **tegion**"* (region) · SI ref 13 *"**freferred**"* (preferred) · SI ref 4 는 2022, 본문 ref 95 는 35 권 2023 (온라인 vs 권호 — 오류는 아닐 수 있음) · ref 26 (Wolfenstine 2018 *Ionics* — 산화물 SE 기계 거동 리뷰) 이 *"These factors are all related to fundamental electro-chemo-mechanical phenomena in anode-free SSBs"* 의 근거로 달림 (결이 약함) · ref 33 과 ref 89 가 같은 쪽 범위 (*Nano Lett.* 1132–1139 · 권 17 vs 23 — 우연일 수 있음 · 미확인).

⑫ **`Table S3` 은 목록이지 순위가 아니다** — *"non-exhaustive"* · 성능 칸 없음 · 전해질 6 종 혼재 · CC 칸이 단순화됐을 수 있다 (11 행 'Cu' vs `spencerjolly2023_…` 카드의 '스테인리스').

⑬ **'SSB 가 액체 무음극보다 유망' 의 근거와 LPSCl.** 근거는 *"certain SSEs show good interfacial stability with lithium metal"* (refs 17 · 18) 인데, 같은 논문이 LPSCl 의 환원 분해 · 미세구조 변화 · 수축을 인정한다 (p. 676). LPSCl 무음극에 '계면상이 평면에 갇혀 CC 가 좋아진다' 를 그대로 옮기면 낙관적일 수 있다 — 우리 환원 축 (§7-1) 과 같이 본다.

⑭ **이 PDF 로 확인 못 한 것**: 인용된 1 차 논문의 값 · 조건 (원문 미확인) · `Fig. 4` 원 그림의 기울기 보정 · Au 입자 띠의 정체 (EDS 등) · 계산기 (SI ref 1) 의 세부 식.

---

## 11. 논증 흐름 (절별 상세 — 원문 순서)

**11.1 서론 (p. 673–674).** Li-ion 은 대형 차량 · 전기 비행 요구를 못 채운다 (ref 1). SSB 는 Li 금속 같은 고용량 전극을 써서 에너지밀도를 최대 50 % 올릴 수 있고 (refs 2–5) 넓은 창 · 비가연 안전 이점이 있다 (3 · 6). 그런데 Li 박 제조는 비싼 분위기 제어가 필요하다 (7–9) → **무음극**이 대안 (10–13 · `Fig. 1b`). 용어: anode-less (14 · 15) · reservoir free · zero-lithium excess · lithium free (16) — 전지는 두 전극이 필요하므로 정확한 말은 아니지만 널리 쓰여 따른다. 구성 = 방전 양극 (예 NMC811) + 맨 CC. 일부 SSE 가 Li 와 계면 안정이 좋고 (17 · 18) SEI 가 평면에 갇히므로, 사이클마다 SEI 가 새로 생기는 액체 무음극 (19) 보다 유망하다. Li 과잉 SSB 는 박리가 빠르면 공극 → 접촉 상실 · 고저항 (20 · 21) → 다음 충전에 공극 둘레 전류 집중 → 필라멘트 · 단락 (14 · 20 · 22). 무음극은 여기에 더 민감한 인자가 있다 (14 · 23 · 24): 첫 충전이 이질 CC (Cu 박) 위 핵생성 · 성장이고 CC\|SSE 국부 화학-역학이 균일성을 정한다 (25). 과잉 Li 가 없으니 CE > 99.95 % 가 필요하다.

**11.2 첫 Li 석출 (p. 674).** Li 과잉 셀과 다른 과제 (23 · 27). SSE\|CC 화학-역학 상호작용이 첫 핵생성과 성장을 정하고 (28 · `Fig. 2a`) 계면 구속 응력이 Li 를 소성 변형시켜 형태를 바꾼다 (14). 직접 관찰은 어렵다.

**11.3 계면 형성과 접촉 (p. 674).** 변형시킬 과잉 Li 가 없으니 핵생성은 **CC–SSE 접촉점에서만** — 접촉 형성과 점착력이 중요하다 (10 · 14). 황화물은 상온 변형이 쉬워 일축 · 등방 압착 ~10–500 MPa (29 · 30) · 산화물은 고온 접합 (LLZO 900 °C + 일축압, 10) · 산업은 롤 압착 (31) — 실험실과 산업 공정은 달라야 한다.

**11.4 Li 구조 변화와 응력 (p. 674–676).** 석출 중 응력 → CC/SSE 박리 · CC 소성 · 파단 · SSE 균열 → 결합 전기-화학-역학으로 봐야 한다. ① **전류** — 핵 밀도를 바꾼다 (10 · 32 · `Fig. 2b`) · 과전압↑ → 핵 밀도↑ (33) · 펄스 (32) · 촘촘한 핵 → 미세 결정립 · 두께 균일 기대 — 그러나 높은 상동 온도로 조대화. Li 결정립은 수송 · 소성 → 박리 중 접촉에 영향 (34) · 미세구조 = CC 상호작용 + 석출 조건 (35) · '미세구조 기억' 불명. ② **적층압** — 실험실 1 MPa – 수백 MPa (10 · 20 · 22 · 36) · 실용 > ~1 MPa 어려움 (37) · > 1 MPa 크리프 (10 · 20 · 36 · `Fig. 2c`) · 점소성으로 옆 성장 · 공극 메움 (14 · 21 · 38) · 고압 + 고온 (39 · 40) · 불균일 적층압 → 불균일 핵생성 (14) · 공칭 ≠ 국부 · 고립 Li 고응력 (크기 의존 항복, 41 · 42) → Li 변형 증폭 또는 SSE 파괴 · 섬 병합 응력의 시공간 변화 → 몰부피 · 반응속도 (14) · 탄성층 (14 · 43). ③ **온도** — 계면 수송 가속 (44–46) · 크리프 · 확산 (47–49) · 핵 밀도 · 크리프 속도 (50 · `Fig. 2d`) · 펄스 · 온도 · 압력 조절 최적화 (37). ④ **CC 두께** — 얇으면 파단 → 비가역 손실 (16 · 28 · 32 · `Fig. 2e`) · 두꺼우면 견디며 옆 성장 (14 · 51) 그러나 SSE 응력 → 균열 · 필라멘트 (52) · 질량 · 부피↑.

**11.5 계면 · 계면상 효과 (p. 676).** Li 핵과 CC 사이 열역학 · 점착 · 젖음 (25). Cu 위 석출 불균일 (10 · 23 · 29) → CE↓ · 수지상. **DFT: Cu · Cu₂O 둘 다 친Li · sessile drop: 깨끗한 Cu 만** → Cu₂O + Li → Li₂O (소Li) → 친Li/소Li 혼재 기판 (`Fig. 2f`) · Li₂O 전환 = 비가역 손실. Li–계면상 · 이질 CC 점착이 접촉 상실 · 형태에 영향 (53). SSE 환원 안정성 차이 → 이질 계면상 (15) · 불안정 (LGPS · Li₃InCl₆) vs 부동태 (LLZO) (4 · 17 · 54 · 55) · LPSCl 환원 → 미세구조 변화 · 수축 공극 가능 (56–58) · 계면상이 핵생성 불균일에 주는 영향은 미해결.

**11.6 SSE 미세구조 효과 (p. 676).** 결정립 · 밀도 · 거칠기 → Li 형태 (52 · 57 · 59 · `Fig. 2g`) · 결정립 → 석출 · 박리 (57 · 60) · 거칠기는 치밀화 · 연마에 의존 · 작은 결정립 (연마 안 하면 거칠기↓) → 첫 접촉 · 막 균일 (57) · 거친 계면 → 박리 용량 · CE↓ (61) · CC 계면 SSE 미세구조 → 환원 분해량 → 젖음–반응성 연결 (57) · 다공 SSE 골격 (62) · 미세구조 제어가 핵심.

**11.7 충방전 사이클 (p. 676–677).** 높은 CE (`Fig. 3a,b` · 63 · 64) · > 99.95 % for 1,000 cycles (37) · Li-ion 과 같은 요구 (음극에 과잉 재고 없음) · 액체 Li 금속 CE 대개 < 99.6 % (65–67) · SSE 의 화학 안정 (17 · 18 · 68) → CE 개선 가능 (30 · 62). 무음극 SSB 의 장기 시연이 적다 (23) · 프로토콜 표준 부재. 필라멘트 = 불균일 접촉 + 전류 집중 (22 · 69–72) · Li 과잉: 임계 박리 전류 위 공극 (20 · 21). **무음극**: 같은 공극 (`Fig. 3c`) + 거의 100 % DoD (73) → 불균일 박리 → 고립 섬 → 접촉 면적↓ → 낮은 전류에서도 국부 고전류 → 공극 가속 (23 · `Fig. 3d`) — Li 과잉의 임계 전류 공극과 다름 (23 · 29) · 표면 확산 · 변형 재분배 연구 필요 (49 · 74). 적층압 → 공극 회복 (20 · 39 · 75) · 침투 (59 · 76) · 파괴 (77) · 고압은 침입↑ (78–80) · 무압 안정 박리엔 Li 확산 조절 (81 · 24 · 29 · 30 · 82). ≈5 µm 과잉 Li (23 · 83 · 84) — 대가 (분위기 · 비에너지).

**11.8 계면 개질 — 인터레이어 (p. 677–678).** 맨 CC · 상온 · 무압은 어렵다 → 나노–마이크로 인터레이어 · **새 계면 둘** · 부류 (24 · 30 · 85 · `Table S3`) · 이상형 (치밀 균일 Li · 구조 유지 또는 회복) · **점착이 강해야** (86) · 저압 (< 1 MPa) 레버 (37 · 81) · 접촉 유지 + 수송 → 저압 공극↓ (81) · 확장성. 탄소: 액체 (87) → SSB (88 · `Fig. 4a`) · MIEC (81) · conformal (89) · Li 와 SSE 사이 유지 (30 · 82 · 89 · 90) · 위치 조절 (86 · 90) · 석출 동역학 (88 · 91 · 92) · 순수 탄소 한계 (90). 합금 · 화합물 (Li₃Au · LiₓAg · Li₂Te): 과전압↓ · 연속 핵생성 (85 · 93–95) · 고체-고체 (24 · 29 · 95) · 100–150 nm Ag · Au (24 · 29) · Au 막 → 입자 (`Fig. 4b`) · Mg (96) · Li₂Te (Cu₂Te 에서 in situ · 유지 · `Fig. 4c` · 95) · 공극 완화 (23 · 29 · 97). 단일 재료 한계 → **Ag–C 복합 1,000 사이클+** (30 · 82 · `Fig. 4d`) · Ag = CC 쪽 치밀 Li · C = 수송 + SE 접촉 → 성분 분업 설계 · 다중 규모 모델링 · operando.

**11.9 결론과 전망 (p. 678–679).** ① 상온 · **무압**에서 신뢰 운전 — 고압 · 고온은 쉽지만 다른 기전이 지배할 수 있다 → **< 1 MPa** 연구 시급 · **SE 와 Li 양쪽에 붙는 인터레이어** · 동적 Li/SSE 계면의 점착 · 젖음 조절 (53) · 점착 ↔ Li 응력 얽힘 (74) · 미세구조 따라 확산하는 크리프 (98) → 미세구조 제어로 크리프↑. ② **Li 순도** — 무음극 Li 는 고순도 (단이온 전도) vs Li 박 불순물 → 계면 축적 · 미세구조 영향 → 원자 불순물 영향 연구 필요. ③ **보고 표준** — 조립 세부 (처리 · 세척 · 거칠기 · 탄성층 · 포장 · 단계별 압력 크기와 시간). ④ **계면상 조절** — 석출 전 CC 전위 유지 · SSE 표면 조성 개질 · 인공 SEI. ⑤ 방전 끝 **폐루프 전류 · 전압 제어** (37). ⑥ CC · SSE 계면 미세구조 공학 · in situ / operando.

---

## 12. 용어 미니 사전

| 용어 | 뜻 (이 논문 맥락) |
|---|---|
| anode-free (= anode-less · reservoir free · zero-lithium excess · lithium free) | 조립 때 음극 쪽에 Li (활물질) 가 없는 셀. 방전 상태 양극의 Li 가 충전 때 맨 CC 에 석출된다 |
| Li 과잉 (lithium excess) | 조립 때 Li 박을 넣은 셀 (SI 산정은 20 µm) |
| CC (current collector) | 집전체 — 음극 쪽 Cu (또는 SUS) 박 · 양극 쪽 Al 박 |
| 친Li / 소Li (lithiophilic / lithiophobic) | Li 가 얇게 잘 퍼져 붙는가 / 방울로 뭉치는가 — 이 논문은 sessile drop 젖음 · 핵생성 과전압으로 말한다 |
| sessile drop | 판 위에 (녹인) 금속 방울을 올려 접촉각을 재는 젖음 측정 (ref 25 의 측정 조건은 이 PDF 에 없음) |
| 핵생성 과전압 (nucleation overpotential) | 첫 Li 핵을 만들 때 필요한 추가 전압 — 친Li 시드가 낮춘다 |
| 순간 vs 연속 핵생성 (instantaneous vs continuous) | 처음에 한꺼번에 핵이 생기고 그 핵만 자라는가 / 석출 내내 새 핵이 계속 생기는가 — 후자가 균일층에 유리하다는 주장 (p. 678) |
| 상동 온도 (homologous temperature) | T / T_m — Li 는 상온에서 ≈0.66 이라 확산 · 크리프 · 조대화가 쉽다 (✎ 298 K / 453.7 K · 이 논문은 값을 안 쓴다) |
| 크리프 · 점소성 (creep · viscoplastic) | 일정 응력에서 시간에 따라 계속 변형 — Li 가 옆으로 흘러 공극을 메우는 기전 |
| 크기 의존 항복 강도 | 작은 Li (마이크로 · 나노) 가 벌크보다 단단한 현상 (refs 41 · 42) — 고립 섬이 큰 응력을 받는 근거 |
| CE (Coulombic efficiency) | 박리 전하 / 석출 전하. 무음극은 손실분을 메울 재고가 없어 CE^N 으로 용량이 준다 |
| 임계 박리 전류 (critical stripping current) | 그 이상이면 Li 공급 (공공 확산 · 크리프) 이 못 따라와 계면 공극이 커지는 전류 (Li 과잉 셀 개념 · refs 20 · 21) |
| 국부 Li 고갈 (local lithium depletion) | 무음극 방전 끝에 Li 가 먼저 다 벗겨진 영역 — 이웃 섬으로 전류가 몰린다 (ref 23) |
| 전류 집중 (current focusing · constriction) | 접촉 면적이 줄어 남은 접촉점의 국부 전류밀도가 오르는 현상 |
| 필라멘트 (filament) | SE 를 뚫고 자라는 Li (수지상) — 단락 원인 |
| 인터레이어 (interlayer) · 시드층 (seed layer) | CC 와 SE 사이에 넣는 얇은 층 — 합금 (Au · Ag · Mg) · 화합물 (Li₂Te · 산화물) · 탄소 · 복합 (Ag–C) |
| MIEC (mixed ionic–electronic conductor) | 이온과 전자를 함께 나르는 물질 — 탄소 인터레이어 (리튬화 뒤) |
| conformal contact | 표면 굴곡을 따라 빈틈없이 닿는 접촉 |
| K_c (fracture toughness) | 파괴 인성 — `Fig. 2a` 의 K_c,SSE (SE 자체) · K_c,SSE/CC (SE\|CC 계면) |
| γ (interfacial energy) | 계면 에너지 — `Fig. 2a` 의 γ_SSE/Li · γ_Li/CC. 점착일 W 와는 Dupré 식 W = γ_A + γ_B − γ_AB 로 이어진다 (이 논문은 식을 쓰지 않는다) |
| V_LiΔG_V | Li 상 부피 × 부피당 자유에너지 변화 — 석출을 미는 구동력 (`Fig. 2a`) |
| DoD (depth of discharge) | 방전 깊이 — 무음극은 거의 100 % 로 다 벗겨야 에너지밀도가 산다 |
| N:P 비 | 음극 / 양극 용량 비 (SI Li-ion 산정 1.2) |
| PFIB-SEM · cryo-FIB-SEM | (플라스마) 집속 이온빔으로 단면을 깎아 보는 전자현미경 · 저온에서 깎아 Li 손상을 줄인 판 |
| ALD (atomic layer deposition) | 원자층 증착 (`Table S3` ZnO · Al₂O₃) |
